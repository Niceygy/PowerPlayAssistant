import os
import requests
import json

def is_in_cache(systemName, cacheType="Stations"):
    """
    Checks if a given system is in the cache.
    If it is, return the system data.
    If not, return None

    Expects:
        -[String] systemName
        -[String] cacheType: Stations or Rings

    Cache Format:
        - Stations:
            systemName=[]

    """
    with open(os.getcwd() + f"/cache/{cacheType}.txt", "r") as f:
            filedata = f.read().splitlines()
            for line in filedata:
                 system_name = line.split("=")[0]
                 system_data = line.split("=")[1]
                 if system_name == systemName:
                      f.close()
                      return system_data
            f.close()
            return None

def add_to_cache(systemName, data, cacheType="Stations"):
     with open(os.getcwd() + f"/cache/{cacheType}.txt", "a") as f:
          f.writelines(f"{systemName}={data}")

    
def get_system_stations(systemName):
    cacheData = is_in_cache(systemName, "Stations")
    if cacheData != None:
         return cacheData
    url = "https://www.edsm.net/api-system-v1/stations" 
    params = {"systemName": systemName} 
    response = requests.get(url, params=params) 
    if response.status_code != 200: 
        raise Exception(f"Error fetching data: {response.status_code}") 
    data = response.json() 
    station_counts = {} 
    for station in data.get("stations", []): 
        station_type = station.get("type", "Unknown") 
        if station_type in station_counts: 
            station_counts[station_type] += 1 
        else: 
            station_counts[station_type] = 1
    add_to_cache(systemName, station_counts, "Stations")
    return station_counts
    
        
    
