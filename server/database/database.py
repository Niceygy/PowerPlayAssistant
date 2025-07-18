from sqlalchemy import BOOLEAN, Column, Integer, String, Float, Boolean, func, BigInteger
from flask_sqlalchemy import SQLAlchemy
import math

database = SQLAlchemy()

class StarSystem(database.Model):
    """
    star_systems:

    - system_name: text pri key,
    - latitude: float,
    - longitude: float,
    - height: float,
    - is_anarchy: bool,
    """
    __tablename__ = "star_systems"
    system_name = Column(String(255), primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Float)
    is_anarchy = Column(Boolean)


class Megaship(database.Model):
    """
    megaships: 
    - name: text pri key
    - system1: text
    - system2: text
    - system3: text
    - system4: text
    - system5: text
    - system6: text
    """
    __tablename__ = "megaships"
    name = Column(String(255), primary_key=True)
    SYSTEM1 = Column(String(255))
    SYSTEM2 = Column(String(255))
    SYSTEM3 = Column(String(255))
    SYSTEM4 = Column(String(255))
    SYSTEM5 = Column(String(255))
    SYSTEM6 = Column(String(255))
    
class PowerData(database.Model):
    __tablename__ = "powerdata"
    system_name = Column(String(50), primary_key=True)
    state = Column(String(20))
    """Unoccupied, War, Exploited, Fortified or Stronghold"""
    shortcode = Column(String(4))
    control_points = Column(Float())
    points_change = Column(Float())
    
class Conflicts(database.Model):
    __tablename__ = "conflicts"
    system_name = Column(String(50), primary_key=True)
    first_place = Column(String(4))
    second_place = Column(String(4))
    has_czs = Column(BOOLEAN(False))
    cycle = Column(Integer())

class RareGoods(database.Model):
    __tablename__ = "Raregoods"
    good_name = Column(String(255), primary_key=True)
    system_name = Column(String(255))
    station_name = Column(String(255))


def system_coordinates(system_name, database):
    """
    Gets the coordinates for a system

    Requires:
        - [String] system_name: The name of the system
        - [Object] database: The current database connection.

    Returns:
        - [int[]] Coordinates: [latitude, longitude, height]
    """
    result = (
        database.session.query(
            StarSystem.latitude, StarSystem.longitude, StarSystem.height
        )
        .filter(StarSystem.system_name == system_name)
        .first()
    )


    if result == [None, None, None] or result == None:
        print(f"?? for {system_name}")
        return [None, None, None]

    return [result.latitude, result.longitude, result.height]


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

    distance = func.sqrt(
        (StarSystem.latitude - start_x) * (StarSystem.latitude - start_x)
        + (StarSystem.longitude - start_y) * (StarSystem.longitude - start_y)
        + (StarSystem.height - start_z) * (StarSystem.height - start_z)
    ).label("distance")

    nearest_systems = (
        session.query(
            StarSystem.system_name,
            distance,
            StarSystem.is_anarchy,
        )
        .filter(StarSystem.is_anarchy == True)
        .join(PowerData, StarSystem.system_name == PowerData.system_name)
        .filter(PowerData.shortcode != None)
        .order_by(distance)
        .limit(1)
        .all()
    )

    return nearest_systems[0].system_name


def distance_to_system(start_system, end_system, database):
    """
    How far is it from start_system to end_system? In LY
    """
    [startx, starty, startz] = system_coordinates(start_system, database)
    [endx, endy, endz] = system_coordinates(end_system, database)

    if (
        startx == None or
        endx == None or
        starty == None or
        endy == None or
        startz == None or
        endz == None
    ): return 0

    #diffrences
    xdist = endx - startx
    ydist = endy - starty
    zdist = endz - startz

    #square them
    xdistSqr = xdist * xdist
    ydistSqr = ydist * ydist
    zdistSqr = zdist * zdist

    #add them all
    sumOfSqares = xdistSqr + ydistSqr + zdistSqr

    distance =  math.sqrt(sumOfSqares)

    return distance