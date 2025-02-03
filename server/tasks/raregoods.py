from server.database.database import RareGoods, distance_to_system

def best_rare_good(system_name, database):
    #list all rare goods

    closest = ""
    closestBy = 0


    results = RareGoods.query().all()
    for item in results:
        distance = distance_to_system(system_name, item.system_name, database)
        if distance < closestBy:
            closestBy = distance
            closest = [item.good_name, item.station_name, item.system_name]

    return closest