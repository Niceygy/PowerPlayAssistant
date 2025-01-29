from server.constants import POWERCOMMODITIES, POWERS
from server.possibleTasks import get_system_power_info, power_full_to_short

def what_commodity_action(powerFullName, system, database):
    system_controlling_power = get_system_power_info(system, database)[1]
    power_shortcode = power_full_to_short(powerFullName)
    if system_controlling_power == powerFullName:
        #own system, reinforce
        # print("reinforce")
        return POWERCOMMODITIES[power_shortcode][1]
    elif system_controlling_power in POWERS:
        #enemy system, undermine
        # print("undermine")
        return POWERCOMMODITIES[power_shortcode][2]
    else:
        #uncontrolled system, acquire
        # print(power_shortcode)
        return POWERCOMMODITIES[power_shortcode][0]
    
