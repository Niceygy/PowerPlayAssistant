from server.powers import get_system_power_info, power_full_to_short
from server.constants import POWERRENFORCEACTIVITIES, TASKSHORTCODES


def what_can_you_do(system_name: str, powerFullName: str, database) -> str:
    state, current_power = get_system_power_info(system_name, database)
    if powerFullName == current_power:
        #reinforce!
        activities = POWERRENFORCEACTIVITIES[power_full_to_short(powerFullName)]
        result = "You can do: "
        for item in activities:
            result += f"{TASKSHORTCODES[item]} "
        return result