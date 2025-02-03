from flask import render_template, redirect, url_for

from server.handlers.megaships import megaships_results
from server.powers import get_system_power_info, isAnarchy
from server.tasks.tasks import (
    TaskDescription,
    getTaskType,
    isPowersWeakness,
    isTaskACrime,
    systemNotes,
)


def handle_results(request, database):
    system = request.args.get("system")
    task = request.args.get("taskName")
    power = request.args.get("power")
    choice = request.args.get("choice")

    powerInfo = get_system_power_info(system, database)
    controllingPower = powerInfo[1]
    systemState = powerInfo[0]

    if task == "Scan Megaship Datalinks" and choice == None:
        return redirect(
            url_for("megaship_choice", system=system, power=power, taskName=task)
        )
    elif task == "Scan Megaship Datalinks" and choice != None:
        return megaships_results(request, power, system, database)

    return render_template(
        "tasks/general.html",
        system=system,
        power=power,
        currentPower=controllingPower,
        currentState=systemState,
        isAnarchy="YES" if isAnarchy(system, database) else "NO",
        taskName=task,
        taskType=getTaskType(task),
        isIllegal="Is" if isTaskACrime(task, isAnarchy(system, database)) else "isn't",
        isOpposingWeakness=isPowersWeakness(power, task),
        taskDescription=TaskDescription(task, power, system, powerInfo, database),
        systemNotes=systemNotes(power, system, database),
    )
