from server.database.database import PowerData

def find_largest_change(session):
    entries = (
        session.query(
            PowerData
        ).filter(
            PowerData.points_change != 0
        ).filter(
            PowerData.points_change != None
        ).order_by(PowerData.points_change.desc()
        ).limit(20)
    )
    return entries

