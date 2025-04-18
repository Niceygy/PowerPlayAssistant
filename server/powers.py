from server.constants import POWERS
from server.database.database import StarSystem, PowerData
from server.database.cache import add_item_to_cache, item_in_cache

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
    
    
def how_many_systems(powerFullName: str, database) -> list[int]:
    """Returns how many systems of each type a power has

    Args:
        powerFullName (str): _description_

    Returns:
        list[int]: [exploited, fortified, stronghold, total]
    """
    # cacheData = item_in_cache(powerFullName, "NA", True, "POWERPOINTS")
    # if cacheData is not None:
    #     exploited, fortified, stronghold = cacheData.split(",")
    #     total = exploited + fortified + stronghold
    #     return [exploited, fortified, stronghold, total]
        
    exploited = (
        database.session.query(
            PowerData
        ).filter(
            PowerData.shortcode == power_full_to_short(powerFullName)
        ).filter(
            PowerData.state == "Exploited"
        ).count()
    )
    fortified = (
        database.session.query(
            PowerData
        ).filter(
            PowerData.shortcode == power_full_to_short(powerFullName)
        ).filter(
            PowerData.state == "Fortified"
        ).count()
    )
    stronghold = (
        database.session.query(
            PowerData
        ).filter(
            PowerData.shortcode == power_full_to_short(powerFullName)
        ).filter(
            PowerData.state == "Stronghold"
        ).count()
    )
    
    total = fortified + exploited + stronghold
    
    # add_item_to_cache(powerFullName, "NA", True, f"{exploited},{fortified},{stronghold}" "POWERPOINTS")
    
    return [exploited, fortified, stronghold, total]

def calculate_powerpoints(exploited: int, fortified: int, stronghold: int):
    points = (
        exploited + 
        (fortified * 2) + 
        (stronghold * 4)
    )
    
    return points