from datetime import datetime
from sqlalchemy import func
from server.database.database import StarSystem, Megaship
import math
import json
from sqlalchemy.orm import class_mapper


def get_week_of_cycle():
    """
    Determines the current week of a cycle.
    Returns:
        int: The current week of the cycle (1-based).
    """
    date=datetime.now()
    days_since_start = (date - datetime(2025, 1, 10)).days
    weeks = math.trunc(days_since_start / 7)
    weeks = weeks + 1
    while weeks > 6:
        weeks = weeks - 6
    return weeks


def megaships_in_cache(system_name, shortcode, opposing):
    current_week = get_week_of_cycle()
    try:
        #linear search
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
                    and _opposing == str(opposing)
                ):
                    f.close()
                    jsonData = json.loads(_data)
                    #only return the systems for this week
                    result =[]
                    for i in range(len(jsonData)):
                        entry = jsonData[i]
                        megaship_name = entry[0]["name"]
                        system = entry[0][f"SYSTEM{get_week_of_cycle()}"]
                        result.append([megaship_name, system])
                    # print(f"Returned {_data} from cache")
                    if result == None:
                        print("none")
                    else:
                        print("not none")
                    return result
            f.close()
    except FileNotFoundError:
        #create cache file
        with open(f"cache/week{current_week}.cache", "w") as f:
            f.write("")
            f.close()
        return None
    return None

def add_megaship_to_cache(system_name, shortcode, opposing, data):
    #is it in cache?
    if megaships_in_cache(system_name, shortcode, opposing) != None:
        return #yes
    else:
        #nope, add it
        current_week = get_week_of_cycle()
        with open(f"./cache/week{current_week}.cache", "a") as f:
            f.write(f"{system_name}/{shortcode}/{opposing}/{json.dumps(data)}\n")
            f.close()
        return


def row_to_dict(row):
    """
    Convert a SQLAlchemy row object to a dictionary.
    GH Copilot Magic
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
    cache = megaships_in_cache(system_name, shortcode, opposing)
    if cache != None:
        return cache
    
    current_week = get_week_of_cycle()
    system_column = f"SYSTEM{current_week}"

    # Where is the user???
    user_system = session.query(StarSystem).filter_by(system_name=system_name).first()
    if not user_system:
        #nowhere.....
        return []

    user_coords = (user_system.longitude, user_system.latitude, user_system.height)

    # find megaships
    if opposing:
        megaships_query = session.query(Megaship).join(StarSystem, getattr(Megaship, system_column) == StarSystem.system_name).filter(StarSystem.shortcode != shortcode).limit(500)
    else:
        megaships_query = session.query(Megaship).join(StarSystem, getattr(Megaship, system_column) == StarSystem.system_name).filter(StarSystem.shortcode == shortcode).limit(500)

    megaships = megaships_query.all()
    print(megaships_query)
    # Calculate distances and sort
    def calculate_distance(coords1, coords2):
        return ((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2 + (coords1[2] - coords2[2]) ** 2) ** 0.5

    megaship_distances = []
    for megaship in megaships:
        megaship_system = session.query(StarSystem).filter_by(system_name=getattr(megaship, system_column)).first()
        if megaship_system:
            distance = calculate_distance(user_coords, (megaship_system.longitude, megaship_system.latitude, megaship_system.height))
            megaship_distances.append((megaship, distance))

    # Sort by distance and return the 10 nearest megaships
    # print(f"Found {len(megaship_distances)} entries")
    megaship_distances.sort(key=lambda x: x[1])

    # Convert the nearest megaships to dictionaries for caching
    nearest_megaships_dicts = [(row_to_dict(megaship), distance) for megaship, distance in megaship_distances[:10]]

    # Cache the result
    add_megaship_to_cache(system_name, shortcode, opposing, nearest_megaships_dicts)

    #returned cached result

    return megaships_in_cache(system_name, shortcode, opposing)
