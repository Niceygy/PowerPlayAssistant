print(" * Loading...")
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    make_response
)
from sqlalchemy import func
from server.possibleTasks import get_system_power_info, isAnarchy, power_full_to_short
from server.database.systems import system_coordinates, query_star_systems
from server.tasks.tasks import (
    getTaskType,
    isPowersWeakness,
    TaskDescription,
    systemNotes,
    isTaskACrime,
)
from server.constants import POWERNAMES, TASKNAMES, DATABASE_CONNECTION_STRING
from server.database.database import (
    database,
    find_nearest_anarchy_systems,
    StarSystem,
    Station,
    Megaship
)
from server.status import status
from server.tasks.megaships import find_nearest_megaships, get_week_of_cycle
from contextlib import contextmanager

print(" * All imports sucsessful")

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
        CACHE.close()
        session.close()


print(f" * Using database connection string: {DATABASE_CONNECTION_STRING}")


@app.route("/", methods=["GET", "POST"])
def index():
    selected_system = None
    selected_task = None
    selected_power = None

    if request.method == "POST":
        selected_system = request.form.get("system")
        selected_task = request.form.get("mission")
        selected_power = request.form.get("power")

        if isTaskACrime(selected_task):
            return redirect(
                url_for(
                    "is_crime",
                    taskName=selected_task,
                    power=selected_power,
                    system=selected_system,
                )
            )
        else:
            last_power = ""
            if "PPA-LastPower" in request.cookies:
                last_power = request.cookies.get("PPA-LastPower")
            return redirect(
                url_for(
                    "results",
                    system=selected_system,
                    taskName=selected_task,
                    power=selected_power,
                )
            )

    return render_template(
        "index.html",
        missions=TASKNAMES,
        powers=POWERNAMES,
        status_emoji = status()[0],
        status_text = status()[1]
    )


@app.route("/is_crime", methods=["GET", "POST"])
def is_crime():
    if request.method == "GET":
        task = request.args.get("taskName")
        power = request.args.get("power")
        system = request.args.get("system")
        return render_template("is_crime.html", task=task, power=power, system=system)
    else:
        task = request.form.get("taskName")
        power = request.form.get("power")
        system = request.form.get("system")
        anarchy = request.form.get("anarchy")

        if anarchy == "Yes":
            anarchy = True
            # we need to find an anarchy system!
            start_x, start_y, start_z = system_coordinates(system, database)
            system = find_nearest_anarchy_systems(
                start_x, start_y, start_z, database.session
            )
        else:
            anarchy = False

        return redirect(
            url_for(
                "results",
                system=system,
                task=task,
                power=power,
                anarchy=anarchy,
            )
        )


@app.route("/results")
def results():
    system = request.args.get("system")
    task = request.args.get("taskName")
    power = request.args.get("power")
    choice = request.args.get("choice")

    resp = None

    # calculated boxes
    powerInfo = get_system_power_info(system, database)
    controllingPower = powerInfo[1]
    systemState = powerInfo[0]
    powerShortCode = power_full_to_short(power)

    if task == "Scan Megaship Datalinks" and choice == None:
        return redirect(
            url_for("megaship_choice", system=system, power=power, taskName=task)
        )
    elif task == "Scan Megaship Datalinks" and choice != None:
        extraInfo = ""
        if choice == "Undermine":
            extraInfo = (
                f"Found megaships in all but {power}'s systems, nearest to {system}"
            )
            choice = False
        else:
            extraInfo = f"Found megaships in {power}'s systems, nearest to {system}"
            choice = True

        megaships = find_nearest_megaships(
            system, powerShortCode, choice, database.session
        )
        return render_template(
            "tasks/megaships.html",
            type=request.args.get("choice"),
            system=system,
            power=power,
            taskName=task,
            taskDescription=TaskDescription(task, power, system, powerInfo, database),
            taskType=getTaskType(task),
            isIllegal="Is" if isTaskACrime(task) else "isn't",
            isOpposingWeakness=isPowersWeakness(power, task),
            extraInfo=extraInfo,
            megaships=megaships,
        )

    resp = make_response(render_template(
        "tasks/general.html",
        system=system,
        power=power,
        currentPower=controllingPower,
        currentState=systemState,
        isAnarchy="YES" if isAnarchy(system, database) else "NO",
        taskName=task,
        taskType=getTaskType(task),
        isIllegal="Is" if isTaskACrime(task) else "isn't",
        isOpposingWeakness=isPowersWeakness(power, task),
        taskDescription=TaskDescription(task, power, system, powerInfo, database),
        systemNotes=systemNotes(power, system, database),
    ))
    resp.set_cookie("PPA-LastPower", power, 60*60*24*7)
    return resp


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
        week=get_week_of_cycle()
    )

@app.route("/search_systems", methods=["GET"])
def search_systems():
    query = request.args.get("query", "")
    results = query_star_systems(query, database)
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
