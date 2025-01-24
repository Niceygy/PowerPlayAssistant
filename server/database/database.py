from sqlalchemy import Column, Integer, String, Float, Boolean, func
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class StarSystem(database.Model):
    __tablename__ = "star_systems"
    id = Column(Integer, primary_key=True, autoincrement=True)
    system_name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Float)
    state = Column(String(255))
    shortcode = Column(String(255))
    is_anarchy = Column(Boolean)
    has_res_sites = Column(Boolean)


class Station(database.Model):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    system_name = Column(String(255))
    station_name = Column(String(255))
    station_type = Column(String(255))
    faction_name = Column(String(255))
    is_anarchy = Column(Boolean)

def find_nearest_anarchy_systems(start_x, start_y, start_z, session):
    """
    Finds the nearest star systems to a given starting point (x, y, z).

    Args:
        start_x (float): The x-coordinate of the starting point.
        start_y (float): The y-coordinate of the starting point.
        start_z (float): The z-coordinate of the starting point.
        session (Session): The SQLAlchemy session to use for querying the database.
        is_anarchy (bool): Whether to filter for anarchy systems.

    Returns:
        list: A list of dictionaries containing the system name, latitude, longitude, height, and distance
              of the nearest star system.
    """

    print(f" * Finding nearest systems to ({start_x}, {start_y}, {start_z})")

    distance = func.sqrt(
        (StarSystem.latitude - start_x) * (StarSystem.latitude - start_x) +
        (StarSystem.longitude - start_y) * (StarSystem.longitude - start_y) +
        (StarSystem.height - start_z) * (StarSystem.height - start_z)
    ).label('distance')

    nearest_systems = session.query(
        StarSystem.system_name,
        # StarSystem.latitude,
        # StarSystem.longitude,
        # StarSystem.height,
        distance,
        StarSystem.is_anarchy,
        StarSystem.shortcode        
    ).filter(StarSystem.is_anarchy == True).filter(StarSystem.shortcode != None).order_by(distance).limit(1).all()
    print(nearest_systems)

    return nearest_systems[0].system_name
