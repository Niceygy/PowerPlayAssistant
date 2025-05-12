from sqlalchemy import func
from server.constants import POWERCOMMODITIES, POWERS
from server.database.database import PowerData, StarSystem, system_coordinates
from server.powers import get_system_power_info, power_full_to_short


def what_commodity_action(powerFullName, system, database) -> str:
    """
    What commodity is needed to make this system undermined or reinforced
    """
    system_controlling_power = get_system_power_info(system, database)[1]
    power_shortcode = power_full_to_short(powerFullName)
    if system_controlling_power == powerFullName:
        # own system, reinforce
        return POWERCOMMODITIES[power_shortcode][1]
    elif system_controlling_power in POWERS:
        # enemy system, undermine
        return POWERCOMMODITIES[power_shortcode][2]
    else:
        # uncontrolled system, acquire
        return POWERCOMMODITIES[power_shortcode][0]


def is_system_in_range(
    powerFullName: str, system_name: str, database
) -> tuple[bool, str]:
    """Is the system within 30LY of a stronghold or 20LY of a fortified?

    Args:
        powerFullName (str): Power's full name
        system_name (str): User's system name
        database (_type_): Database object
    """

    # Where is the user???
    user_system = (
        database.session.query(StarSystem).filter_by(system_name=system_name).first()
    )
    if not user_system:
        # nowhere.....
        return []

    user_coords = (user_system.longitude, user_system.latitude, user_system.height)

    distance = func.sqrt(
        func.pow(StarSystem.longitude - user_coords[0], 2)
        + func.pow(StarSystem.latitude - user_coords[1], 2)
        + func.pow(StarSystem.height - user_coords[2], 2)
    ).label("distance")

    powerShortCode = power_full_to_short(powerFullName)


    strongholds_within_range = (
        database.session.query(StarSystem, distance)
        .join(PowerData, StarSystem.system_name == PowerData.system_name)
        .filter(PowerData.shortcode == powerShortCode)
        .filter(PowerData.state == "Stronghold")
        .filter(distance <= 30)  # Ensure this filter is applied after the join
        .all()
    )

    fortified_within_range = (
        database.session.query(StarSystem, distance)
        .join(PowerData, StarSystem.system_name == PowerData.system_name)
        .filter(PowerData.shortcode == powerShortCode)
        .filter(PowerData.state == "Fortified")
        .filter(distance <= 20)  # Ensure this filter is applied after the join
        .all()
    )
    
    
    if strongholds_within_range:
        return True, strongholds_within_range[0][0].system_name
    elif fortified_within_range:
        return True, fortified_within_range[0][0].system_name
    else:
        return False, ""