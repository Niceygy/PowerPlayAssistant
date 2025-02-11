from flask import render_template
from server.powers import get_system_power_info, is_system_anarchy
from server.tasks.bountyHunting import has_stations
from server.tasks.tasks import TaskDescription, getTaskType, is_task_own_strength, isPowersWeakness, isTaskACrime, systemNotes


def handle_bounty_hunting(request, database):
    system = request.args.get("system")
    task = request.args.get("taskName")
    power = request.args.get("power")

    stations = has_stations(system, database)
    if (stations == -1):
        stations = "No"
    
    powerInfo = get_system_power_info(system, database)
    systemState = powerInfo[0]
    controllingPower = powerInfo[1]
    if is_system_anarchy(system, database):
        #bounty hunting dosen't work in anarchy!
        return render_template(
            "does_not_work.html",
            ERRORDATA="Bounty hunting cannot be completed in anarchy systems",
            ERRORCODE="INCOMPLETABLE"
            )
    
    
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