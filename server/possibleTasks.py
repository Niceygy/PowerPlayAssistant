from server.constants import POWERS, POWERRENFORCEACTIVITIES
from server.database import StarSystem, Station


def power_full_to_short(power):
    for key, value in POWERS.items():
        if value == power:
            return key
    return None

def short_to_full_power(power):
    return POWERS[power]


#################################

def get_system_power_info(system, database):
    """
    get_system_power_info:

    Returns the system power info for the specified system.

    Expects:
        - [String] system: System name
        - [object] database: Database connection

    Returns:
        - [
            system state,
            system occuping power
        ]
    """
    
    # returns [state, powerShortCode]
    try:
        result = database.session.query(StarSystem).filter(StarSystem.system_name == system).first()
        if result == None:
            return ["Uncontrolled", "Uncontrolled"]
        powerShortCode = result.shortcode
        systemState = result.state
        powerFullName = short_to_full_power(powerShortCode)
        return [systemState, powerFullName]
    except Exception as e:
        print(e)
        return ["Uncontrolled", "Uncontrolled"]


# def possibleTasks(ownPower, isAnarchy, systemName, database):
#     result = []
#     #[["name", "description", "legality", "whosWeakness"]]
#     own_power_shortcode = power_full_to_short(ownPower)
#     opposing_power_shortcode = get_system_power_info(systemName, database)[1]
#     if (own_power_shortcode == opposing_power_shortcode):
#         #renforce
#         activities = POWERRENFORCEACTIVITIES[own_power_shortcode]
#         for activity in activities:
#             task = {}
#             task["name"] = activity
#             task["description"] 

#             #get description
#             #get legality
#             #get whos weakness it is
#             #add this all to TASK object
        

#     #create a list of tasks, with all the tasks that can be done in that system
#     #
    
#     return []# result


def isAnarchy(systemName, database):
    result = database.session.query(Station).filter(Station.system_name == systemName).first()
    if result == None:
        return False
    #invert it, becuase mariadb is weird
    return False if result.is_anarchy else True
    