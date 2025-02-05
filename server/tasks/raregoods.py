from server.database.database import RareGoods, distance_to_system
from server.database.cache import item_in_cache, add_item_to_cache
from server.constants import ITEMS_TO_RETURN

def best_rare_goods(system_name, database):
    """
    Finds the 10 rare goods closest to 200 units away from the given system.

    Args:
        system_name (str): The name of the system.
        database (object): The current database connection.

    Returns:
        List of the 10 rare goods closest to 200 units away.
    """

    cache = item_in_cache(system_name, "NA", False, "RAREGOODS")
    if cache != None:
        return cache

    results = database.session.query(RareGoods).all()
    distances = []

    for item in results:
        distance = distance_to_system(system_name, item.system_name, database)
        distance = round(distance)
        distances.append((distance, item.good_name, item.station_name, item.system_name))

    # Sort the list by the absolute difference from 200
    distances.sort(key=lambda x: abs(x[0] - 200))

    add_item_to_cache(system_name, "NA", False, distances[:ITEMS_TO_RETURN], "RAREGOODS")

    # Return the 10 rare goods closest to 200 units away
    return distances[:ITEMS_TO_RETURN]