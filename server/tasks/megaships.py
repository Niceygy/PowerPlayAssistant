from server.database.cycle import get_cycle_week
from server.database.database import StarSystem, Megaship, PowerData
from sqlalchemy.orm import class_mapper
from server.database.cache import item_in_cache, add_item_to_cache
from server.constants import ITEMS_TO_RETURN


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
        cache = item_in_cache(system_name, shortcode, opposing, "MEGASHIP")
        if cache is not None:
            return cache

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

        # find megaships
        if not opposing:
            megaships_query = (
                session.query(Megaship)
                .join(
                    StarSystem,
                    getattr(Megaship, system_column) == StarSystem.system_name,
                )
                .join(PowerData, StarSystem.system_name == PowerData.system_name)
                .filter(PowerData.shortcode != shortcode)
                .limit(50)
            )
        else:
            megaships_query = (
                session.query(Megaship)
                .join(
                    StarSystem,
                    getattr(Megaship, system_column) == StarSystem.system_name,
                )
                .filter(StarSystem.shortcode == shortcode)
                .limit(500)
            )

        # GET 'EM
        megaships = megaships_query.all()

        # sort by distance from the user
        def calculate_distance(coords1, coords2):
            return (
                (coords1[0] - coords2[0]) ** 2
                + (coords1[1] - coords2[1]) ** 2
                + (coords1[2] - coords2[2]) ** 2
            ) ** 0.5

        megaship_distances = []
        for megaship in megaships:
            megaship_system = (
                session.query(StarSystem)
                .filter_by(system_name=getattr(megaship, system_column))
                .first()
            )
            if megaship_system:
                megaship_coords = (
                    megaship_system.longitude,
                    megaship_system.latitude,
                    megaship_system.height,
                )
                if None in megaship_coords:
                    print(f"Skipping megaship {megaship.name} due to None coordinates.")
                    continue
                distance = calculate_distance(user_coords, megaship_coords)
                megaship_distances.append((megaship, distance))

        # Sort by distance and return the 10 nearest megaships
        # print(f"Found {len(megaship_distances)} entries")
        megaship_distances.sort(key=lambda x: x[1])

        # Convert the nearest megaships to dictionaries for caching
        nearest_megaships_dicts = [
            (row_to_dict(megaship), distance)
            for megaship, distance in megaship_distances[:ITEMS_TO_RETURN]
        ]

        # Cache the result
        add_item_to_cache(
            system_name, shortcode, opposing, nearest_megaships_dicts, "MEGASHIP"
        )

        # returned cached result
        return item_in_cache(system_name, shortcode, opposing, "MEGASHIP")
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
