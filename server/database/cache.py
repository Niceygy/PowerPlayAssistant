from server.database.cycle import get_cycle_week
import json
import ast
import os

def item_in_cache(system_name, shortcode, opposing, dataType):
    """
    Is this thing in cache? If so, return it
    """
    current_week = get_cycle_week()
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
                            system = entry[0][f"SYSTEM{get_cycle_week()}"]
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
        current_week = get_cycle_week()
        with open(f"./cache/week{current_week}.cache", "a") as f:
            f.write(f"{dataType}:{system_name}/{shortcode}/{opposing}/{json.dumps(data)}\n")
            f.close()
        return

def clean_caches():
    for i in range(5):
        try:
            open(f"cache/week{i}.cache", "w").close()
        except FileNotFoundError:
            open(f"cache/week{i}.cache", "r").write(" ")