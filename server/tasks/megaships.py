from server.database.cycle import get_cycle_week
from server.database.database import StarSystem, Megaship, PowerData
from sqlalchemy.orm import class_mapper
from server.database.cache import Cache
from server.constants import ITEMS_TO_RETURN
from sqlalchemy import func
import json


def row_to_dict(row):
    """
    Convert a SQLAlchemy row object to a dictionary.
    GH Copilot Magic
    """
    return {c.key: getattr(row, c.key) for c in class_mapper(row.__class__).columns}


def find_nearest_megaships(system_name, shortcode, opposing, session):
    """
    Finds the 10 nearest megaships

    Expects:
        -[String] shortcode: The power's shortcode.
        -[Bool] opposing: Is the user supporting this power?
            If yes, it will find megaships in that power's systems
            If no, it will find megaships in all but that power's systems.
            Note: "Supporting" means are they undermining or reinforcing, not pledged
        -[Object] Session: The database session

    Returns:
        List of nearest megaships
    """
    try:
        cache = Cache()
        cache_res = cache.get(f"{system_name}_{shortcode}_{opposing}", "megaship")
        if cache_res is not None:
            return json.loads(cache_res[0])

        current_week = get_cycle_week()
        system_column = f"SYSTEM{current_week}"

        # Where is the user???
        user_system = (
            session.query(StarSystem).filter_by(system_name=system_name).first()
        )
        if not user_system:
            # nowhere.....
            return []

        user_coords = (user_system.longitude, user_system.latitude, user_system.height)

        distance = func.sqrt(
            func.pow(StarSystem.longitude - user_coords[0], 2)
            + func.pow(StarSystem.latitude - user_coords[1], 2)
            + func.pow(StarSystem.height - user_coords[2], 2)
        ).label("distance")

        # find megaships
        if not opposing:
            megaships_query = (
                session.query(Megaship, distance)
                .join(
                    StarSystem,
                    getattr(Megaship, system_column) == StarSystem.system_name,
                )
                .join(PowerData, StarSystem.system_name == PowerData.system_name)
                .filter(PowerData.shortcode != shortcode)
                .order_by(distance)
                .limit(ITEMS_TO_RETURN)
            )
        else:
            megaships_query = (
                session.query(Megaship, distance)
                .join(
                    StarSystem,
                    getattr(Megaship, system_column) == StarSystem.system_name,
                )
                .join(PowerData, StarSystem.system_name == PowerData.system_name)
                .filter(PowerData.shortcode == shortcode)
                .order_by(distance)
                .limit(ITEMS_TO_RETURN)
            )

        # GET 'EM
        megaships = megaships_query.all()

        # Convert the nearest megaships to dictionaries for caching
        nearest_megaships_dicts = [
            (row_to_dict(megaship), distance) for megaship, distance in megaships
        ]
        
        #Format
        result = []
        for item in nearest_megaships_dicts:
            result.append({
                'name': item[0]['name'],
                'system': item[0][f'SYSTEM{current_week}']
            })

        #Cache result
        cache.add(f"{system_name}_{shortcode}_{opposing}", json.dumps(result), "megaship")
        
        # return result
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

