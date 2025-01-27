from server.constants import POWERS
from server.database.database import StarSystem


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


def isAnarchy(systemName, database):
    result = database.session.query(StarSystem).filter(StarSystem.system_name == systemName).first()
    if result == None:
        return False
    #invert it, becuase mariadb is weird
    return False if result.is_anarchy else True
    