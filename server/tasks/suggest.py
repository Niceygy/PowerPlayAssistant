from flask import render_template
from server.handlers.notsure import what_can_you_do
from server.powers import get_system_power_info, is_system_anarchy


def handle_not_sure(request, power, database):
    system_name = request.args.get("system")
    powerInfo = get_system_power_info(system_name, database)
    controllingPower = powerInfo[1]
    systemState = powerInfo[0]
    return render_template(
        "tasks/suggest.html",
        system=system_name,
        currentPower=controllingPower,
        currentState=systemState,
        power=power,
        systemNotes="N/A",
        isAnarchy="yes" if is_system_anarchy(system_name, database) else "no",
        possibleTasks=what_can_you_do(system_name, power, database)
    )