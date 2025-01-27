print(" * Loading...")
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from server.possibleTasks import get_system_power_info, isAnarchy, power_full_to_short
from server.database.systems import system_coordinates, query_star_systems
from server.tasks.tasks import (
    getTaskType,
    isPowersWeakness,
    TaskDescription,
    systemNotes,
    isTaskLegal,
)
from server.constants import POWERNAMES, TASKNAMES, DATABASE_CONNECTION_STRING
from server.database.database import (
    database,
    find_nearest_anarchy_systems,
)
from server.tasks.megaships import find_nearest_megaships
from contextlib import contextmanager

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


@app.route("/", methods=["GET", "POST"])
def index():
    selected_system = None
    selected_task = None
    selected_power = None

    if request.method == "POST":
        selected_system = request.form.get("system")
        selected_task = request.form.get("mission")
        selected_power = request.form.get("power")

        if isTaskLegal(selected_task):
            return redirect(
                url_for(
                    "is_crime",
                    task=selected_task,
                    # still good
                    power=selected_power,
                    system=selected_system,
                )
            )
        else:
            return redirect(
                url_for(
                    "results",
                    system=selected_system,
                    task=selected_task,
                    power=selected_power,
                )
            )

    return render_template(
        "index.html",
        missions=TASKNAMES,
        powers=POWERNAMES,
    )


@app.route("/is_crime", methods=["GET", "POST"])
def is_crime():
    if request.method == "GET":
        task = request.args.get("task")
        power = request.args.get("power")
        system = request.args.get("system")
        return render_template("is_crime.html", task=task, power=power, system=system)
    else:
        task = request.form.get("task")
        power = request.form.get("power")
        system = request.form.get("system")
        anarchy = request.form.get("anarchy")

        if anarchy == "Yes":
            anarchy = True
            #we need to find an anarchy system!
            start_x, start_y, start_z = system_coordinates(system, database)
            system = find_nearest_anarchy_systems(start_x, start_y, start_z, database.session)
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
    task = request.args.get("task")
    power = request.args.get("power")

    # calculated boxes
    powerInfo = get_system_power_info(system, database)
    controllingPower = powerInfo[1]
    systemState = powerInfo[0]
    powerShortCode = power_full_to_short(power)

    if task == "Scan Megaship Datalinks":
        megaships = find_nearest_megaships(system, powerShortCode, True, database.session)
        return render_template(
            "tasks/megaships.html",
            system=system,
            power=power,
            taskName=task,
            taskDescription=TaskDescription(task, power, system, powerInfo, database),
            taskType=getTaskType(task),
            isIllegal="Is" if isTaskLegal(task) else "isn't",
            isOpposingWeakness=isPowersWeakness(power, task),
            megaships=megaships
        )    

    return render_template(
        "tasks/general.html",
        system=system,
        power=power,
        currentPower=controllingPower,
        currentState=systemState,
        isAnarchy="YES" if isAnarchy(system, database) else "NO",
        taskName=task,
        taskType=getTaskType(task),
        isIllegal="Is" if isTaskLegal(task) else "isn't",
        isOpposingWeakness=isPowersWeakness(power, task),
        taskDescription=TaskDescription(task, power, system, powerInfo, database),
        systemNotes=systemNotes(power, system, database),
    )


@app.route("/search_systems", methods=["GET"])
def search_systems():
    query = request.args.get("query", "")
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
