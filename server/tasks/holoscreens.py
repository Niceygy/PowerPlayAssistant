from sqlalchemy import func
from server.database.database import PowerData, StarSystem, Station
from server.powers import power_full_to_short

# Global cache dictionary
cache = {}

def count_system_stations(user_system_name, power, opposing, session):
    """
    Counts the number of starports and outposts in the 100 nearest systems to the user.

    Args:
        - [String] user_system_name: The system the user is in
        - [String] power: powers full name 
        - [Boolean] opposing: Is the user supporting their own?
        - [Object] session: Database session

    Returns:
        list: A list of lists containing the system name, starport count, and outpost count.
    """
    # Check if the result is already in the cache
    if user_system_name in cache:
        return cache[user_system_name]

    # Get user system coordinates
    user_system = session.query(StarSystem).filter_by(system_name=user_system_name).first()
    if not user_system:
        return []

    user_coords = (user_system.longitude, user_system.latitude, user_system.height)

    # Calculate distance to other systems
    distance = func.sqrt(
        func.pow(StarSystem.longitude - user_coords[0], 2) +
        func.pow(StarSystem.latitude - user_coords[1], 2) +
        func.pow(StarSystem.height - user_coords[2], 2)
    ).label("distance")

    # Find the 100 nearest systems
    nearest_systems = None
    nearest_system_names = None

    if opposing == False:
        #make own stronger
        nearest_systems = (
            session.query(StarSystem.system_name)
            .join(PowerData, StarSystem.system_name == PowerData.system_name)
            .filter(StarSystem.is_anarchy == 0, PowerData.shortcode == power_full_to_short(power))
            .order_by(distance)
            .limit(30)
            .all()
            )
        nearest_system_names = [system.system_name for system in nearest_systems]
    else:
        #make other weaker
        nearest_systems = (
            session.query(StarSystem.system_name)
            .join(PowerData, StarSystem.system_name == PowerData.system_name)
            .filter(StarSystem.is_anarchy == 0, PowerData.shortcode != power_full_to_short(power))
            .order_by(distance)
            .limit(30)
            .all()
            )
        nearest_system_names = [system.system_name for system in nearest_systems]

    result = []
    # for system_name in nearest_system_names:
    i = 0
    sucsesses = 0
    while sucsesses < 15:
        system_name = nearest_system_names[i]
        starport_count = session.query(Station).filter(
            Station.star_system == system_name,
            Station.station_type == "Starport"
        ).count()

        outpost_count = session.query(Station).filter(
            Station.star_system == system_name,
            Station.station_type == "Outpost"
        ).count()

        # print(outpost_count + starport_count)
        
        if ((outpost_count + starport_count) > 0):
            sucsesses+=1 
            i+=1
            result.append([system_name, starport_count, outpost_count])
        else:
            i+=1

    print(f"Took {i} attempts")
    # Store the result in the cache
    cache[user_system_name] = result

    # print(result[0])

    return result