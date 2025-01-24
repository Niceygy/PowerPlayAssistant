from server.database import StarSystem

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
    results = (
        StarSystem.query.filter(StarSystem.system_name.like(f"%{query}%"))
        .limit(10)
        .all()
    )
    return [row.system_name for row in results]