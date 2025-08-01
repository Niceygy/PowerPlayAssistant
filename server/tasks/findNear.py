from sqlalchemy import func

from server.database.database import PowerData, StarSystem


def find_nearby_system(
    system_name: str, power_short_code: str, system_type: str, session
) -> str:
    """
    Finds a nearby system matching the passed parameters
    Returns the name
    """
    # find user
    user_system = session.query(StarSystem).filter_by(system_name=system_name).first()
    if not user_system:
        # nowhere.....
        return []

    user_coords = (user_system.longitude, user_system.latitude, user_system.height)

    distance = func.sqrt(
        func.pow(StarSystem.longitude - user_coords[0], 2)
        + func.pow(StarSystem.latitude - user_coords[1], 2)
        + func.pow(StarSystem.height - user_coords[2], 2)
    ).label("distance")

    query = None

    match system_type:
        case "no_owner":
            query = (
                session.query(StarSystem, distance)
                .join(PowerData, PowerData.system_name == StarSystem.system_name)
                .filter(PowerData.state == "Unoccupied")
                .order_by(distance)
            )
        case "you_own":
            query = (
                session.query(StarSystem, distance)
                .join(PowerData, PowerData.system_name == StarSystem.system_name)
                .filter(PowerData.shortcode == power_short_code)
                .order_by(distance)
            )
        case "enemy_owns":
            query = (
                session.query(StarSystem, distance)
                .join(PowerData, PowerData.system_name == StarSystem.system_name)
                .filter(PowerData.state != "Unoccupied")
                .filter(PowerData.shortcode != power_short_code)
                .order_by(distance)
            )

    result = query.first()

    return result.StarSystem.system_name
    
    
