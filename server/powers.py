from server.constants import POWERS
from server.database.database import StarSystem, PowerData
import traceback

def power_full_to_short(power: str) -> str:
    """
    Returns the shortcode of a power when supplied its full name
    """
    for key, value in POWERS.items():
        if value == power:
            return key
    return None

def short_to_full_power(power: str) -> str:
    """
    Retuns the full name of a power when supplied its shortcode
    """
    if power == '':
        return None
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
            occuping power full name
        ]
    """
    
    try:
        result = database.session.query(PowerData).filter(PowerData.system_name == system).first()
        if result == None:
            return ["Uncontrolled", "Uncontrolled"]
        powerShortCode = result.shortcode
        systemState = result.state
        if powerShortCode == None or systemState == '':
            #no powerplay activity here
            return ["Uncontrolled", "Uncontrolled"]    
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
    