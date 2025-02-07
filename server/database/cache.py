import requests
from datetime import datetime, timedelta
import json
import ast
import math

def get_week_of_cycle():
    """
    Determines the current week of the megaship cycle using data from tick.edcd.io.
    Returns:
        int: The current week of the cycle (1-6)
    """
    # Fetch the latest tick data from tick.edcd.io
    response = requests.get("https://tick.edcd.io/api/tick")
    if response.status_code != 200:
        raise Exception("Failed to fetch tick data")

    tick_data = response.json()
    latest_tick = tick_data[0]["time"]

    # Convert the latest tick time to a datetime object
    latest_tick_datetime = datetime.strptime(latest_tick, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Calculate the number of days since the latest tick
    days_since_tick = (datetime.now(datetime.timezone.utc) - latest_tick_datetime).days

    # Calculate the current week of the cycle
    weeks = math.trunc(days_since_tick / 7)
    weeks = weeks + 1
    while weeks > 6:
        weeks = weeks - 6

    print(weeks)

    return 5#weeks

def item_in_cache(system_name, shortcode, opposing, dataType):
    """
    Is this thing in cache? If so, return it
    """
    current_week = get_week_of_cycle()
    try:
        with open(f"cache/week{current_week}.cache", "r") as f:
            for line in f.read().splitlines():
                if line is None:
                    continue
                if not line.startswith(f"{dataType}:"):
                    continue
                else:
                    line = line.removeprefix(f"{dataType}:")
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
                    
                    if dataType == "MEGASHIP":
                        result = []
                        jsonData = json.loads(_data)
                        for entry in jsonData:
                            megaship_name = entry[0]["name"]
                            system = entry[0][f"SYSTEM{get_week_of_cycle()}"]
                            result.append([megaship_name, system])
                        return result
                    else:
                        return ast.literal_eval(_data)
            f.close()
    except FileNotFoundError:
        with open(f"cache/week{current_week}.cache", "w") as f:
            f.write("")
            f.close()
        return None
    return None

def add_item_to_cache(system_name, shortcode, opposing, data, dataType):
    """
    Add this thing to the cache
    """
    if item_in_cache(system_name, shortcode, opposing, dataType) is not None:
        return
    else:
        current_week = get_week_of_cycle()
        with open(f"./cache/week{current_week}.cache", "a") as f:
            f.write(f"{dataType}:{system_name}/{shortcode}/{opposing}/{json.dumps(data)}\n")
            f.close()
        return
