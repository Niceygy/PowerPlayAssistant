print(" * Loading...")
"""
IMPORTS
"""
import os
pyver = os.getenv("PYTHON_VERSION")
print(f" * Using Python {pyver}")
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from sqlalchemy import func
from server.handlers.index import handle_index
from server.database.systems import query_star_systems
from server.handlers.is_crime import handle_is_crime
from server.handlers.results import handle_results
from server.constants import DATABASE_CONNECTION_STRING
from server.database.database import (
    database,
    StarSystem,
    Station,
    Megaship,
)
from server.database.cycle import watch_tick, get_cycle_week
from contextlib import contextmanager

print(" * All imports sucsessful")
watch_tick()

"""
Flask and database
"""

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_STRING
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


print(f" * Using database connection string: {DATABASE_CONNECTION_STRING}")

"""
Route Handlers
"""

@app.route("/", methods=["GET", "POST"])
def index():
    return handle_index(request)


@app.route("/is_crime", methods=["GET", "POST"])
def is_crime():
    return handle_is_crime(request, database)


@app.route("/results")
def results():
    return handle_results(request, database)


@app.route("/megaship_choice", methods=["GET", "POST"])
def megaship_choice():
    system = request.args.get("system")
    task = request.args.get("taskName")
    power = request.args.get("power")

    if request.method == "POST":
        choice = request.form.get("choice")
        system = request.form.get("system")
        task = request.form.get("task")
        power = request.form.get("power")
        return redirect(
            url_for("results", system=system, power=power, taskName=task, choice=choice)
        )

    return render_template(
        "tasks/megaship_choice.html", system=system, power=power, taskName=task
    )

@app.route("/database", methods=["GET"])
def database_stats():
    systems = database.session.query(func.count(func.distinct(StarSystem.system_name))).scalar()
    megaships = database.session.query(func.count(func.distinct(Megaship.name))).scalar()
    stations = database.session.query(func.count(func.distinct(Station.station_name))).scalar()
    return render_template(
        "database.html",
        systems=systems,
        megaships=megaships,
        stations=stations,
        week=get_cycle_week()
    )

@app.route("/search_systems", methods=["GET"])
def search_systems():
    query = request.args.get("query")
    results = query_star_systems(query)
    return jsonify(results)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "favicon.ico")

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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
