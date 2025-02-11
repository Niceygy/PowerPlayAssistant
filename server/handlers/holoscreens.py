from flask import render_template
from server.powers import get_system_power_info, power_full_to_short
from server.tasks.megaships import find_nearest_megaships
from server.tasks.tasks import (
    TaskDescription,
    getTaskType,
    is_task_own_strength,
    isPowersWeakness,
)
from server.tasks.holoscreens import count_system_stations


def handle_holoscreens(request, power, system, database):
    """
    Handler for /results, when the task is Holoscren Hacking

    Methods: GET

    Renders holoscreens.html
    """
    task = "Holoscreen Hacking"
    # calculated boxes
    powerInfo = get_system_power_info(system, database)

    otherSystems = count_system_stations(system, power, False, database.session)
    return render_template(
        "tasks/holoscreens.html",
        system=system,
        power=power,
        taskName=task,
        taskDescription=TaskDescription(task, power, system, powerInfo, database),
        taskType=getTaskType(task),
        isIllegal="is",
        isOpposingWeakness=isPowersWeakness(power, task),
        otherSystems=otherSystems,
        extraInfo="Found the 10 nearest systems to you, with 2 or more stations",
        isOwnStrength="is" if is_task_own_strength(task, power) else "isn't"
    )
