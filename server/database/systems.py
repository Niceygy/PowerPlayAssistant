from server.database.database import StarSystem

def system_coordinates(system_name, database):
    result = database.session.query(
        StarSystem.latitude, 
        StarSystem.longitude, 
        StarSystem.height
    ).filter(StarSystem.system_name == system_name).first()
    
    if result is None:
        return [0, 0, 0]
    
    return [result.latitude, result.longitude, result.height]

def query_star_systems(query):
    """"
    Returns a list of 10 systems that roughtly match the 
    query by name
    """
    results = (
        StarSystem.query.filter(StarSystem.system_name.like(f"%{query}%"))
        .limit(10)
        .all()
    )
    
    try:
        return [row.system_name for row in results]
    except Exception:
        return []