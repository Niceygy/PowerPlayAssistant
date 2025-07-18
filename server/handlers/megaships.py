from flask import render_template
from server.powers import get_system_power_info, power_full_to_short
from server.tasks.megaships import find_nearest_megaships
from server.constants import ITEMS_TO_RETURN
from server.tasks.tasks import (
    task_description,
    getTaskType,
    is_task_own_strength,
    isPowersWeakness,
)


def megaships_results(request, power, system, database):
    """
    Handler for /results, when the task is megaships

    Methods: GET

    Renders megaships.html
    """
    task = "Scan Megaship Datalinks"
    # calculated boxes
    powerInfo = get_system_power_info(system, database)
    powerShortCode = power_full_to_short(power)
    choice = request.args.get("choice")
    extraInfo = ""
    if choice == "Undermine":
        extraInfo = f"Found {ITEMS_TO_RETURN} megaships in all but {power}'s systems, nearest to {system}"
        choice = False
    else:
        extraInfo = f"Found {ITEMS_TO_RETURN} megaships in {power}'s systems, nearest to {system}"
        choice = True

    megaships = find_nearest_megaships(system, powerShortCode, choice, database.session)
    return render_template(
        "tasks/megaships.html",
        type=request.args.get("choice"),
        system=system,
        power=power,
        taskName=task,
        taskDescription=task_description(task, power, system, powerInfo, database),
        taskType=getTaskType(task),
        isIllegal="isn't",
        isOpposingWeakness=isPowersWeakness(power, task),
        extraInfo=extraInfo,
        megaships=megaships,
        isOwnStrength="is" if is_task_own_strength(task, power) else "isn't"
    )
    
    
# def megaship_advanced_search(request, power, system, database):
#     """
#     Handler for /results, when the task is megaships

#     Methods: GET

#     Renders megaships.html
#     """
#     task = "Scan Megaship Datalinks"
#     # calculated boxes
    

#     megaships = find_nearest_megaships(system, powerShortCode, choice, database.session)
#     return render_template(
#         "tasks/megaships.html",
#         type=request.args.get("choice"),
#         system=system,
#         power=power,
#         taskName=task,
#         taskDescription=task_description(task, power, system, powerInfo, database),
#         taskType=getTaskType(task),
#         isIllegal="isn't",
#         isOpposingWeakness=isPowersWeakness(power, task),
#         extraInfo=extraInfo,
#         megaships=megaships,
#         isOwnStrength="is" if is_task_own_strength(task, power) else "isn't"
#     )
