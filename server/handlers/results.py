from flask import render_template, redirect, url_for

from server.handlers.bountyHunting import handle_bounty_hunting
from server.handlers.holoscreens import handle_holoscreens
from server.handlers.megaships import megaships_results
from server.handlers.raregoods import handle_rare_goods
from server.powers import get_system_power_info, is_system_anarchy
from server.tasks.tasks import (
    TaskDescription,
    getTaskType,
    is_task_own_strength,
    isPowersWeakness,
    isTaskACrime,
    systemNotes,
)


def handle_results(request, database):
    system = request.args.get("system")
    task = request.args.get("taskName")
    power = request.args.get("power")
    megaship_sys_type_choice = request.args.get("choice")

    powerInfo = get_system_power_info(system, database)
    controllingPower = powerInfo[1]
    systemState = powerInfo[0]

    if task == "Scan Megaship Datalinks" and megaship_sys_type_choice == None:
        return redirect(
            url_for("task_choice", system=system, power=power, taskName=task)
        )
    elif task == "Scan Megaship Datalinks" and megaship_sys_type_choice != None:
        return megaships_results(request, power, system, database)
    elif task == "Sell rare goods":
        return handle_rare_goods(request, database)
    elif task == "Holoscreen Hacking":
        return handle_holoscreens(request, power, system, database)
    elif task == "Bounty hunting":
        return handle_bounty_hunting(request, database)
    else:
        return render_template(
            "tasks/general.html",
            system=system,
            power=power,
            currentPower=controllingPower,
            currentState=systemState,
            isAnarchy="YES" if is_system_anarchy(system, database) else "NO",
            taskName=task,
            taskType=getTaskType(task),
            isIllegal="Is" if isTaskACrime(task, is_system_anarchy(system, database)) else "isn't",
            isOpposingWeakness=isPowersWeakness(power, task),
            taskDescription=TaskDescription(task, power, system, powerInfo, database),
            systemNotes=systemNotes(power, system, database),
            isOwnStrength="is" if is_task_own_strength(task, controllingPower) else "isn't"
        )
