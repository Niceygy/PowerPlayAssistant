from server.powers import get_system_power_info, is_system_anarchy
from server.tasks.commodites import is_system_in_range
from flask import render_template
from server.tasks.tasks import task_description, is_task_own_strength

def handle_commodites(request, power, system, database):
    
    task = "Deliver PowerPlay Commodities"
    
    powerInfo = get_system_power_info(system, database)
    
    anarchy = is_system_anarchy(system, database)
    
    system_in_range, supply_system = is_system_in_range(power, system, database)
    
    return render_template(
        "tasks/commodity.html",
        system=system,
        power=power,
        currentPower=powerInfo[1],
        currentState=powerInfo[0],
        isAnarchy="yes" if anarchy else "no",
        taskname=task,
        taskType="Transport",
        taskDescription=task_description(task, powerInfo[1]),
        isIllegal="is",
        
    )