from server.powers import get_system_power_info, is_system_anarchy
from server.tasks.commodites import is_system_in_range, what_commodity_action
from flask import render_template
from server.tasks.tasks import task_description, is_task_own_strength

def handle_commodites(request, power, system, database):
    
    task = "Deliver PowerPlay Commodities"
    
    powerInfo = get_system_power_info(system, database)
    
    anarchy = is_system_anarchy(system, database)
    
    system_in_range, supply_system, system_distance = is_system_in_range(power, system, database)
    
    return render_template(
        "tasks/commodity.html",
        system=system,
        power=power,
        currentPower=powerInfo[1],
        currentState=powerInfo[0],
        isAnarchy="yes" if anarchy else "no",
        taskName=task,
        taskType="Transport",
        taskDescription=task_description(task, powerInfo[1], system, powerInfo, database),
        isIllegal="isn't",
        isOwnStrength="is" if is_task_own_strength(task, powerInfo[1]) else "isn't",
        item_system=supply_system,
        item_name=what_commodity_action(powerInfo[1], system, database),
        item_dist=system_distance
    )