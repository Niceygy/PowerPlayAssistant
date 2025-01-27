from datetime import datetime
from sqlalchemy import func
from server.database.database import StarSystem, Megaship
import math
import json
from sqlalchemy.orm import class_mapper


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
    weeks = math.trunc(days_since_start / 7)
    weeks = weeks + 1
    while weeks > 6:
        weeks = weeks - 6
    print(f"Week {weeks}")
    return weeks


def megaships_in_cache(system_name, shortcode, opposing):
    current_week = get_week_of_cycle()
    try:
        with open(f"cache/week{current_week}.cache", "r") as f:
            for line in f.read().splitlines():
                if line == None:
                    continue
                temp = line.split("/", 3)
                _system_name = temp[0]
                _shortcode = temp[1]
                _opposing = temp[2]
                _data = temp[3]
                if (
                    _system_name == system_name
                    and _shortcode == shortcode
                    and bool(_opposing) == opposing
                ):
                    f.close()
                    print(f"Returned {_data} from cache")
                    return json.loads(_data)
            f.close()
    except FileNotFoundError:
        with open(f"cache/week{current_week}.cache", "w") as f:
            f.write("")
            f.close()
        return None
    return None

def add_megaship_to_cache(system_name, shortcode, opposing, data):
    if megaships_in_cache(system_name, shortcode, opposing) != None:
        return
    else:
        current_week = get_week_of_cycle()
        with open(f"./cache/week{current_week}.cache", "a") as f:
            f.write(f"{system_name}/{shortcode}/{opposing}/{json.dumps(data)}\n")
            f.close()
        return


def row_to_dict(row):
    """
    Convert a SQLAlchemy row object to a dictionary.
    """
    return {c.key: getattr(row, c.key) for c in class_mapper(row.__class__).columns}

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
    system_column = f"SYSTEM{current_week}"

    # Query to find the user's system coordinates
    user_system = session.query(StarSystem).filter_by(system_name=system_name).first()
    if not user_system:
        return []

    user_coords = (user_system.longitude, user_system.latitude, user_system.height)

    # Query to find megaships
    if opposing:
        megaships_query = session.query(Megaship).select_from(Megaship).join(StarSystem, Megaship.system_id == StarSystem.id).filter(StarSystem.shortcode != shortcode)
    else:
        megaships_query = session.query(Megaship).select_from(Megaship).join(StarSystem, Megaship.system_id == StarSystem.id).filter(StarSystem.shortcode == shortcode)

    megaships = megaships_query.all()

    # Calculate distances and sort
    def calculate_distance(coords1, coords2):
        return ((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2 + (coords1[2] - coords2[2]) ** 2) ** 0.5

    megaship_distances = []
    for megaship in megaships:
        megaship_system = session.query(StarSystem).filter_by(name=getattr(megaship, system_column)).first()
        if megaship_system:
            distance = calculate_distance(user_coords, (megaship_system.longitude, megaship_system.latitude, megaship_system.height))
            megaship_distances.append((megaship, distance))

    # Sort by distance and return the 10 nearest megaships
    megaship_distances.sort(key=lambda x: x[1])
    nearest_megaships = [megaship for megaship, distance in megaship_distances[:10]]

    # Convert the nearest megaships to dictionaries for caching
    nearest_megaships_dicts = [(row_to_dict(megaship), distance) for megaship, distance in megaship_distances[:10]]

    # Cache the result
    add_megaship_to_cache(system_name, shortcode, opposing, nearest_megaships_dicts)

    return nearest_megaships
