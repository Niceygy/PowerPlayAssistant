print(" * Loading...")
"""
IMPORTS
"""

# PACKAGES
import os
from contextlib import contextmanager
from sqlalchemy import func
from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

# OWN CODE
from server.handlers.choice import handle_task_choice
from server.status import status, update_status
from server.handlers.index import handle_index
from server.database.systems import query_star_systems
from server.handlers.is_crime import handle_is_crime
from server.handlers.results import handle_results
from server.database.cycle import get_cycle_week, write_cycle_week
from server.database.cache import clean_caches
from server.handlers.powerpoints import handle_powerpoints, handle_powerpoints_raw
from server.database.database import (
    database,
    StarSystem,
    Station,
    Megaship,
)


pyver = os.getenv("PYTHON_VERSION")
print(f" * Using Python {pyver}")
print(" * All imports sucsessful")
clean_caches()
print(" * Caches cleaned")


"""
Flask and database
"""

app = Flask(__name__)
load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://powerplay_assistant:elite.niceygy.net@10.0.0.52/elite"#os.getenv("DATABASE_CONNECTION_STRING_PA")
app.config["SQLALCHEMY_POOL_SIZE"] = 10
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
app.config["SQLALCHEMY_POOL_RECYCLE"] = 280
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
database.init_app(app)


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
Error Handler
"""


def uhoh(error):
    """
    Returns an error page, when somthing goes REALLY WRONGs
    """
    return render_template(
        "does_not_work.html", ERRORDATA=error, ERRORCODE="IRRECONCILABLE"
    )


"""
Route Handlers
"""


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        return handle_index(request)
    except Exception as e:
        return uhoh(str(e))


@app.route("/is_crime", methods=["GET", "POST"])
def is_crime():
    try:
        return handle_is_crime(request, database)
    except Exception as e:
        return uhoh(str(e))


@app.route("/results")
def results():
    try:
        return handle_results(request, database)
    except Exception as e:
        return uhoh(str(e))


@app.route("/handle_choice", methods=["GET", "POST"])
def handle_choice():
    try:
        return handle_task_choice(request)
    except Exception as e:
        return uhoh(str(e))

@app.route("/powerpoints", methods=["GET"])
def powerpoints():
    return handle_powerpoints(request, database)

@app.route("/powerpoints/raw", methods=["GET"])
def powerpoints_raw():
    return handle_powerpoints_raw(request, database)

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/meritminer", methods=["GET"])
def meritminer():
    return render_template(
        "redirect.html",
        description="The tool MeritMiner is better suited to helping you with this task.",
        url="https://meritminer.cc/"
    )

@app.route("/tickset", methods=["GET"])
def tickset():
    week = request.args.get("week")
    write_cycle_week(int(week))
    return f"Set week to {week}"


def get_database_stats():
    """
    Returns the number of systems, megaships and stations in the database
    """
    systems = database.session.query(
        func.count(func.distinct(StarSystem.system_name))
    ).scalar()
    megaships = database.session.query(
        func.count(func.distinct(Megaship.name))
    ).scalar()
    stations = database.session.query(
        func.count(func.distinct(Station.station_name))
    ).scalar()
    return systems, megaships, stations


@app.route("/database", methods=["GET"])
def database_stats():
    try:
        systems, megaships, stations = get_database_stats()
        return render_template(
            "database.html",
            systems=systems,
            megaships=megaships,
            stations=stations,
            week=get_cycle_week(),
        )
    except Exception as e:
        return uhoh(str(e))


@app.route("/search_systems", methods=["GET"])
def search_systems():
    query = request.args.get("query")
    results = query_star_systems(query)
    return jsonify(results)

@app.after_request
def apply_headers(response):
    response.headers["X-Powered-By"] = "Nightspeed Connect"
    response.headers["Server"] = "Flask/3.1.0"
    response.headers["X-Created-By"] = "Niceygy (Ava Whale) - niceygy@niceygy.net"
    return response

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "icons/favicon.ico")


@app.route("/copy_icon.svg")
def copy_icon():
    return send_from_directory(app.static_folder, "copy_solid_icon.svg")


@app.route("/changelog", methods=["GET"])
def changelog():
    return render_template("changelog.html")


@app.route("/robots.txt")
def robots():
    print(request.headers.get("User-Agent"))
    return send_from_directory(app.static_folder, "robots.txt")


@app.route("/status")
def status_update():
    emoji = request.args.get("emoji")
    text = request.args.get("text")
    update_status(text, emoji)
    return f"Updated to {status()}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
