from flask import render_template
from server.powers import get_system_power_info, is_system_anarchy
from server.tasks.raregoods import best_rare_goods
from server.tasks.tasks import TaskDescription, isPowersWeakness, isTaskACrime, systemNotes


def handle_rare_goods(request, database):
    """
    Handler for /results, when the task is rare goods

    Methods: GET

    Renders raregoods.html
    """
    system_name = request.args.get("system")
    system = request.args.get("system")
    task = request.args.get("taskName")
    power = request.args.get("power")

    powerInfo = get_system_power_info(system, database)
    controllingPower = powerInfo[1]
    systemState = powerInfo[0]
    rare_goods = best_rare_goods(system_name, database)
    return render_template(
        "tasks/raregoods.html",
        system=system,
        power=power,
        currentPower=controllingPower,
        currentState=systemState,
        isAnarchy="YES" if is_system_anarchy(system, database) else "NO",
        taskName=task,
        taskType="Trading",
        isIllegal="Is" if isTaskACrime(task, is_system_anarchy(system, database)) else "isn't",
        isOpposingWeakness=isPowersWeakness(power, task),
        taskDescription=TaskDescription(task, power, system, powerInfo, database),
        systemNotes=systemNotes(power, system, database),
        raregoods=rare_goods
    )
