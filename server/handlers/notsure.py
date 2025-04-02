from server.powers import get_system_power_info, power_full_to_short
from server.constants import (
    POWERRENFORCEACTIVITIES,
    POWERWEAKNESSES,
    TASKSHORTCODES,
    TASKDESCRIPTIONS,
)


def what_can_you_do(system_name: str, powerFullName: str, database) -> str:
    state, current_power = get_system_power_info(system_name, database)
    if powerFullName == current_power:
        # reinforce!
        activities = POWERRENFORCEACTIVITIES[power_full_to_short(powerFullName)]
        result = []
        for item in activities:
            taskfullname = TASKSHORTCODES[item]
            taskinfo = TASKDESCRIPTIONS[item]
            url = redirect_url_constructor(system_name, powerFullName, taskfullname)
            result.append([taskfullname, taskinfo, url])
        return result
    else:
        activities = POWERWEAKNESSES[power_full_to_short(powerFullName)]
        result = []
        for item in activities:
            taskfullname = TASKSHORTCODES[item]
            taskinfo = TASKDESCRIPTIONS[item]
            url = redirect_url_constructor(system_name, powerFullName, taskfullname, "&choice=Undermine")
            result.append([taskfullname, taskinfo, url])
        return result


def url_santise(input: str) -> str:
    return input.replace(" ", "+")

def redirect_url_constructor(system_name: str, powerFullName: str, taskName: str, extra: str) -> str:
    # results?system=Mazahuanses&taskName=notsure&power=Denton+Patrus
    system_name = url_santise(system_name)
    powerFullName = url_santise(powerFullName)
    taskName = url_santise(taskName)
    return f"/results?system={system_name}&taskName={taskName}&power={powerFullName}{extra}"
