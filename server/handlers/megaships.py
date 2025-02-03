from flask import render_template
from server.powers import get_system_power_info, isAnarchy, power_full_to_short
from server.tasks.megaships import find_nearest_megaships
from server.tasks.tasks import (
    TaskDescription,
    getTaskType,
    isPowersWeakness,
    isTaskACrime,
)


def megaships_results(request, power, system, database):
    task = "Scan Megaship Datalinks"
    # calculated boxes
    powerInfo = get_system_power_info(system, database)
    powerShortCode = power_full_to_short(power)
    choice = request.args.get("choice")
    extraInfo = ""
    if choice == "Undermine":
        extraInfo = f"Found megaships in all but {power}'s systems, nearest to {system}"
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
        isIllegal="Is" if isTaskACrime(task, isAnarchy(system, database)) else "isn't",
        isOpposingWeakness=isPowersWeakness(power, task),
        extraInfo=extraInfo,
        megaships=megaships,
    )
