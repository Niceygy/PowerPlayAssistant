from server.database.systems import system_coordinates
import requests, math

LOWER_CREDIT_LIMIT = 40 * 1000 #40k
LOWER_DISTANCE_LIMIT = 50 #LY
HIGHER_DISTANCE_LIMIT = 80#LY

def system_value_in_cache(system_name):
    try:
        #linear search
        with open(f"cache/values.cache", "r") as f:
            for line in f.read().splitlines():
                systemName = line.split("/")[0]
                if (system_name == systemName):
                    f.close()
                    return line.split("/")[1]
        return None
    except Exception:
        return None

def add_system_value_to_cache(system_name, value):
        #is it in cache?
    if system_value_in_cache(system_name) != None:
        return #yes
    else:
        #nope, add it
        with open(f"./cache/values.cache", "a") as f:
            f.write(f"{system_name}/{value}\n")
            f.close()
        return

def get_system_value(system_name):
    ENDPOINT = "https://www.edsm.net/api-system-v1/estimated-value"
    cache = system_value_in_cache(system_name)
    if cache != None:
        return cache
    else:
        result = requests.get(f"{ENDPOINT}?systemName={system_name}")
        full_scan_value = result.json["estimatedValueMapped"]
        add_system_value_to_cache(system_name, full_scan_value)
        return full_scan_value


def find_sutable_system(system_name):
    """
    Finds a system with a high enough value to be merit worthy
    (needs to be above 40K value)

    Expects:
        - [String] system_name: The user's current location

    Returns:
        - [Array]: [sutable system name, distance from user, value if all bodies scanned]
    Note: distance is rounded
    """
    ENDPOINT = "https://www.edsm.net/api-v1/sphere-systems"
    result = requests.get(f"{ENDPOINT}?systemName={system_name}&minRadius={LOWER_DISTANCE_LIMIT}&?radius={HIGHER_DISTANCE_LIMIT}")
    for system in result.json:
        name = system["name"]
        distance = system["distance"]
        bodies = system["bodyCount"]
        if bodies < 5:
            continue
        else:
            value = get_system_value(name)
            if value >= LOWER_CREDIT_LIMIT:
                distance = round(distance)
                return [name, distance, value]
    return [None, None, None]


