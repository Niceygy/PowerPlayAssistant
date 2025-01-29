from server.database.database import StarSystem

def system_coordinates(system_name, database):
    """
    Gets the coordinates for a system
    
    Requires:
        - [String] system_name: The name of the system
        - [Object] database: The current database connection.

    Returns:
        - [int[]] Coordinates: [latitude, longitude, height]
    """
    result = database.session.query(
        StarSystem.latitude, 
        StarSystem.longitude, 
        StarSystem.height
    ).filter(StarSystem.system_name == system_name).first()
    
    if result is None:
        return [0, 0, 0]
    
    return [result.latitude, result.longitude, result.height]

def query_star_systems(query, database):
    """"
    Returns a list of 10 systems that roughtly match the query by name.

    Expects: 
        - [String]
    """
    results = (
        StarSystem.query.filter(StarSystem.system_name.ilike(f"%{query}%"))
        .limit(10)
        .all()
    )
    
    try:
        if results != []:
            return [row.system_name for row in results]
        else:
            return ["No System Found"]
    except Exception:
        return ["No System Found"]