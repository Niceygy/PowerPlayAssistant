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
from server.systems import system_coordinates, query_star_systems
from server.tasks import (
    getTaskType,
    isPowersWeakness,
    TaskDescription,
    systemNotes,
    isTaskLegal
)
from server.constants import POWERNAMES, TASKNAMES, DATABASE_CONNECTION_STRING
from server.database import StarSystem, Station, database, find_nearest_systems
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
                    #still good
                    power=selected_power,
                    system=selected_system
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
        print(f"{task} is task in is_crime")
        return render_template("is_crime.html", task=task, power=power, system=system)
    else:
        task = request.form.get("task")
        power = request.form.get("power")
        system = request.form.get("system")
        anarchy = request.form.get("anarchy")

        if anarchy == "Yes":
            anarchy = True
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

# @app.route("/specifed_system", methods=["POST"])
# def specifed_system():
#     action_type = request.form.get("task")
#     system_name = request.form.get("system")
#     power = request.form.get("power")
#     power = power if power != "Any" else "Unspecified Power"
#     is_anarchy = False
#     if request.form.get("anarchy") == "Yes":
#         is_anarchy = True
#     else:
#         is_anarchy = False

#     # Process the form data
#     # For example, find the nearest systems based on the provided system name
#     start_x, start_y, start_z = system_coordinates(system_name, database)
#     nearest_systems = find_nearest_systems(
#         start_x, start_y, start_z, database.session, is_anarchy
#     )
#     if len(nearest_systems) == 0:
#         return "No systems found"

#     # populate with user-useful data
#     results = []
#     loopSucseses = 0
#     loopCount = 0
#     while loopSucseses != 10 and loopCount != len(nearest_systems) - 1:
#         loopCount = loopCount + 1
#         _system_name = nearest_systems[loopCount][0]
#         _system_power = get_system_power_info(_system_name, database)[1]
#         _system_power = _system_power if _system_power != "Uncontrolled" else "No-One"
#         if isAnarchy(_system_name, database) == is_anarchy:
#             results.append([_system_name, _system_power])
#             loopSucseses = loopSucseses + 1

#     return render_template(
#         "results_systems.html",
#         system=system_name,
#         power=power,
#         results=results,
#         isAnarchy="yes" if is_anarchy else "no",
#         actionType=action_type,
#     )


@app.route("/results")
def results():
    system = request.args.get("system")
    task = request.args.get("task")
    power = request.args.get("power")
    print(f"{task} is task")
    print(f"{power} is power")
    print(f"{system} is system")

    # calculated boxes
    powerInfo = get_system_power_info(system, database)
    controllingPower = powerInfo[1]
    systemState = powerInfo[0]
    return render_template(
        "results.html",
        system=system,
        power=power,
        currentPower=controllingPower,
        currentState=systemState,
        isAnarchy="YES" if isAnarchy(system, database) else "NO",
        taskName=task,
        taskType=getTaskType(task),
        isIllegal="Is" if isTaskLegal(task) else "isn't",
        isOpposingWeakness=isPowersWeakness(power, task),
        taskDescription=TaskDescription(task, power, system, powerInfo),
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


@app.route("/changelog", methods=["GET"])
def changelog():
    return render_template("changelog.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
