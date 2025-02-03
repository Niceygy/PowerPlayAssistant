from datetime import datetime
import json
import ast
import math

def get_week_of_cycle():
    """
    Determines the current week of the megaship cycle.
    Returns:
        int: The current week of the cycle (1-6)
    """
    date = datetime.now()
    days_since_start = (date - datetime(2025, 1, 10)).days
    weeks = math.trunc(days_since_start / 7)
    weeks = weeks + 1
    while weeks > 6:
        weeks = weeks - 6
    return weeks

def item_in_cache(system_name, shortcode, opposing, dataType):
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
    if item_in_cache(system_name, shortcode, opposing, dataType) is not None:
        return
    else:
        current_week = get_week_of_cycle()
        with open(f"./cache/week{current_week}.cache", "a") as f:
            f.write(f"{dataType}:{system_name}/{shortcode}/{opposing}/{json.dumps(data)}\n")
            f.close()
        return