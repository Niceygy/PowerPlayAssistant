print(" * Loading...")
"""
IMPORTS
"""

# PACKAGES
from contextlib import contextmanager
from sqlalchemy import func
from dotenv import load_dotenv
import traceback
from flask import (
    Flask,
    jsonify,
    make_response,
    render_template,
    request,
    send_from_directory,
)

# OWN CODE
from server.api.api import frequency_map
from server.constants import API_KEYS, POWERS
from server.database.cache import Cache
from server.handlers.capi import handle_capi, handle_logout
from server.handlers.choice import handle_task_choice
from server.status import get_status, set_status
from server.handlers.index import handle_index
from server.database.systems import query_star_systems
from server.handlers.is_crime import handle_is_crime
from server.handlers.results import handle_results
from server.database.cycle import get_cycle_week, write_cycle_week
from server.handlers.powerpoints import handle_powerpoints
from server.handlers.conflict import handle_conflict_result, handle_conflict_search
from server.handlers.systemSearch import handle_system_search
from server.handlers.powerpoints import (
    nicey_powerpoints,
    kruger_powerpoints,
    fdev_powerpoints,
)
from server.powers import how_many_systems
from server.database.database import (
    database,
    StarSystem,
    Megaship,
)


"""
Cache
"""
cache = Cache()
cache.clean("megaship")
cache.clean("raregoods")
cache.clean("conflicts")
cache.__exit__()


"""
Flask and database
"""


def init():
    app = Flask(__name__)
    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://powerplay_assistant:elite.niceygy.net@10.0.0.52/elite"  # os.getenv("DATABASE_CONNECTION_STRING_PA")
    )
    app.config["SQLALCHEMY_POOL_SIZE"] = 10
    app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 280
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
    if "TEST" in app.config and app.config["TEST"]:
        print("PPA In testing mode")
    database.init_app(app)
    return app


app = init()


@contextmanager
def session_scope():
    session = database.session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        print(" * Closing session")
        session.close()


"""
Error Handlers
"""


@app.errorhandler(404)
def not_found(request):
    response = make_response(render_template("errors/404.html"), 404)
    return response


@app.errorhandler(Exception)
def internal_error(err):
    response = make_response(
        render_template("errors/500.html", info=str(err), stack=traceback.format_exc()),
        500,
    )
    return response


"""
Route Handlers - Main Pages
"""


@app.route("/", methods=["GET", "POST"])
def index():
    return handle_index(request)


@app.route("/is_crime", methods=["GET", "POST"])
def is_crime():
    return handle_is_crime(request, database)


@app.route("/results", methods=["GET", "POST"])
def results():
    return handle_results(request, database)


@app.route("/handle_choice", methods=["GET", "POST"])
def handle_choice():
    return handle_task_choice(request)

@app.route("/system_search", methods=["GET", "POST"])
def system_search():
    return handle_system_search(request, database)


@app.route("/conflict", methods=["GET"])
def conflicts():
    return handle_conflict_search(request, database)


@app.route("/conflict/result", methods=["POST", "GET"])
def conflicts_result():
    return handle_conflict_result(request, database)


@app.route("/weeklys", methods=["GET"])
def weekly():
    return render_template("weeklys/weekly.html")


"""
Route Handlers - Static Pages
"""


@app.route("/archnotepad", methods=["GET"])
def archnotepad():
    return render_template(
        "redirect.html",
        strong="Tool no longer in service",
        description="Architect's notepad has now been depriciated. I have linked to Inara, but other tools are also avalible.",
        url="https://inara.cz/elite/cmdr-architect/",
    )


@app.route("/changelog", methods=["GET"])
def changelog():
    return render_template("changelog.html")


@app.route("/robots.txt")
def robots():
    print(request.headers.get("User-Agent"))
    return send_from_directory(app.static_folder, "robots.txt")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "icons/favicon.ico")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/meritminer", methods=["GET"])
def meritminer():
    return render_template(
        "redirect.html",
        strong="There is a better tool for this!",
        description="The tool MeritMiner is better suited to helping you with this task.",
        url="https://meritminer.cc/",
    )


@app.route("/database", methods=["GET"])
def database_stats():
    systems = database.session.query(
        func.count(func.distinct(StarSystem.system_name))
    ).scalar()
    megaships = database.session.query(
        func.count(func.distinct(Megaship.name))
    ).scalar()
    return render_template(
        "database.html",
        systems=systems,
        megaships=megaships,
        stations=0,
        week=get_cycle_week(),
    )


"""
Route Handlers - cAPI
"""


@app.route("/import", methods=["GET"])
def handle_import():
    return handle_capi(request, database)


@app.route("/logout", methods=["GET"])
def logout():
    return handle_logout()


"""
Route Handlers - PowerPoints
"""


@app.route("/powerpoints", methods=["GET"])
def powerpoints():
    return handle_powerpoints(request, database)


"""
Route Handlers - Map
"""

@app.route("/map")
def map():
    return frequency_map(database.session)

"""
Route Handlers - APIs
"""



@app.route("/week", methods=["GET"])
def week():
    return get_cycle_week()


@app.route("/tickset", methods=["GET"])
def tickset():
    week = request.args.get("week")
    write_cycle_week(int(week))
    return f"Set week to {week}"


@app.route("/search_systems", methods=["GET"])
def search_systems():
    query = request.args.get("query")
    results = query_star_systems(query)
    return jsonify(results)


@app.route("/status")
def status_update():
    emoji = request.args.get("emoji")
    text = request.args.get("text")
    set_status(text, emoji)
    return f"Updated to {get_status()}"


@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "POST":
        auth_key = ""
        try:
            data = request.get_json(silent=True)
            if not data or "key" not in data:
                return jsonify(
                    {
                        "error": True,
                        "error_code": 401,
                        "error_message": "Invaid Key! Make sure you have included a json value named 'key' in the body of your request ",
                    }
                )
            auth_key = data["key"]
            if not auth_key in API_KEYS:
                return jsonify(
                    {
                        "error": True,
                        "error_code": 401,
                        "error_message": "Invaid Key! Make sure you have included a json value named 'key' in the body of your request ",
                    }
                )
        except Exception:
            return jsonify(
                    {
                        "error": True,
                        "error_code": 401,
                        "error_message": "Invaid Key! Make sure you have included a json value named 'key' in the body of your request ",
                    }
                )
        request_type = request.get_json()["type"]

        match request_type:
            case "pp_systems":
                result = []
                for key, item in POWERS.items():
                    exploited, fortified, stronghold, total = how_many_systems(
                        item, database
                    )
                    result.append(
                        {
                            "exploited": exploited,
                            "fortified": fortified,
                            "stronghold": stronghold,
                            "total": total,
                            "power": item,
                        }
                    )
                return jsonify(result)
            case "pp_points":
                result = []
                result.append(nicey_powerpoints(database))
                result.append(kruger_powerpoints(database))
                result.append(fdev_powerpoints(database))
                return jsonify(result)
    else:
        return jsonify(
            {
                "error": True,
                "error_code": 405,
                "error_message": "This endpoint only supports POST requests ",
            }
        )


"""
Request Assembly
"""


@app.after_request
def apply_headers(response):
    response.headers["X-Powered-By"] = "Nightspeed Connect"
    response.headers["Server"] = "Flask/3.1.0"
    response.headers["X-Created-By"] = "Niceygy (Ava Whale) - niceygy@niceygy.net"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
