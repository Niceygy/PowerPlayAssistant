from server.database.database import RareGoods, distance_to_system
from server.database.cache import Cache
from server.constants import ITEMS_TO_RETURN
import json

def best_rare_goods(system_name, database):
    """
    Finds the 10 rare goods closest to 200 units away from the given system.

    Args:
        system_name (str): The name of the system.
        database (object): The current database connection.

    Returns:
        List of the 10 rare goods closest to 200 units away.
    """

    cache = Cache()
    res = cache.get(system_name, "raregoods")
    if res is not None:
        return res

    results = database.session.query(RareGoods).all()
    distances = []

    for item in results:
        distance = distance_to_system(system_name, item.system_name, database)
        if distance != None:
                distance = round(distance)
                distances.append((distance, item.good_name, item.station_name, item.system_name))

    # Sort the list by the absolute difference from 200
    distances.sort(key=lambda x: abs(x[0] - 200))

    cache.add(system_name, distances[:ITEMS_TO_RETURN], "raregoods")
    
    cache.__exit__()

    # Return 
    return distances[:ITEMS_TO_RETURN]
