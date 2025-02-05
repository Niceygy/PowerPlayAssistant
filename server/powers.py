from server.constants import POWERS
from server.database.database import StarSystem


def power_full_to_short(power):
    """
    Returns the shortcode of a power when supplied its full name
    """
    for key, value in POWERS.items():
        if value == power:
            return key
    return None

def short_to_full_power(power):
    """
    Retuns the full name of a power when supplied its shortcode
    """
    return POWERS[power]



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


def is_system_anarchy(system_name, database):
    result = database.session.query(StarSystem).filter(StarSystem.system_name == system_name).first()
    if result == None:
        return False
    #invert it, becuase mariadb is weird
    return result.is_anarchy#False if result.is_anarchy else True
    