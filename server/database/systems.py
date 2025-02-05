from server.database.database import StarSystem

def query_star_systems(query):
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