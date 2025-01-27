from datetime import datetime
from sqlalchemy import func
from server.database.database import StarSystem, Megaship

def get_week_of_cycle(date=datetime.now(), cycle_length=6, start_day=3):
    """
    Determines the current week of a cycle.

    Args:
        date (datetime): The date to check.
        cycle_length (int): The length of the cycle in weeks.
        start_day (int): The starting day of the week (0=Monday, 1=Tuesday, ..., 6=Sunday).

    Returns:
        int: The current week of the cycle (1-based).
    """
    # Calculate the number of days since the start of the cycle
    days_since_start = (date - datetime(2025, 1, 10)).days

    # Adjust for the start day of the week
    days_since_start += (7 - start_day)

    # Calculate the current week of the cycle
    current_week = (days_since_start // 7) % cycle_length + 1

    return current_week

def find_nearest_megaships(system_name, shortcode, opposing, session):
    """
    Finds the 10 nearest megaships

    Expects:
        -[String] shortcode: The power's shortcode.
        -[Bool] opposing: Is the user supporting this power?
            If yes, it will find megaships in that power's systems
            If no, it will find megaships in all but that power's systems.
            Note: "Supporting" means are they undermining or reinforcing, not pledged
        -[Object] Session: The database session

    Returns:
        List of nearest megaships
    """
    current_week = get_week_of_cycle()
    # system_column = f"SYSTEM{current_week}"
    system_column = "SYSTEM3"
    print(system_column)

    # Query to find the user's system coordinates
    user_system = session.query(StarSystem).filter_by(system_name=system_name).first()
    if not user_system:
        print("User system not found")
        return []

    user_coords = (user_system.longitude, user_system.latitude, user_system.height)
    print(f"User coordinates: {user_coords}")

    # Query to find the nearest megaships
    distance = func.sqrt(
        func.pow(StarSystem.longitude - user_coords[0], 2) +
        func.pow(StarSystem.latitude - user_coords[1], 2) +
        func.pow(StarSystem.height - user_coords[2], 2)
    ).label('distance')

    if opposing:
        megaships_query = session.query(
            Megaship.name,
            StarSystem.system_name,
            distance
        ).join(
            StarSystem, StarSystem.system_name == getattr(Megaship, system_column)
        ).filter(
            StarSystem.shortcode != shortcode
        ).order_by(distance).limit(10)
    else:
        megaships_query = session.query(
            Megaship.name,
            StarSystem.system_name,
            distance
        ).join(
            StarSystem, StarSystem.system_name == getattr(Megaship, system_column)
        ).filter(
            StarSystem.shortcode == shortcode
        ).order_by(distance).limit(10)

    nearest_megaships = megaships_query.all()
    print(f"Nearest megaships: {nearest_megaships}")

    return nearest_megaships