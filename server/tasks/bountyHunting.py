from server.database.database import Station

def has_stations(system_name, database):
    qry = database.session.query(Station).filter(Station.star_system == system_name).all()
    if qry == None:
        return -1
    else:
        return len(qry)