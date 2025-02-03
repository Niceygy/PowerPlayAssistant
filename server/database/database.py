from sqlalchemy import Column, Integer, String, Float, Boolean, func
from flask_sqlalchemy import SQLAlchemy
import math

database = SQLAlchemy()

"""
TABLES:

star_systems:

    id: int pri key
    system_name text
    latitude float
    longitude float
    height float
    state text (powerplay state)
    shortcode text (power shortcode)
    is_anarchy bool
    has_res_sites bool

stations:

    id int pri key
    name text
    system text
    type text (Starport, Outpost, PlanetaryPort, Settlement, EngineerBase)

megaships: 
    name text pri key
    system1 text
    system2 text
    system3 text
    system4 text
    system5 text
    system6 text
"""


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
    station_name = Column(String(255))
    star_system = Column(String(255))
    station_type = Column(String(255))


class Megaship(database.Model):
    __tablename__ = "megaships"
    name = Column(String(255), primary_key=True)
    SYSTEM1 = Column(String(255))
    SYSTEM2 = Column(String(255))
    SYSTEM3 = Column(String(255))
    SYSTEM4 = Column(String(255))
    SYSTEM5 = Column(String(255))
    SYSTEM6 = Column(String(255))


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
        return [0, 0, 0]

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
            StarSystem.shortcode,
        )
        .filter(StarSystem.is_anarchy == True)
        .filter(StarSystem.shortcode != None)
        .order_by(distance)
        .limit(1)
        .all()
    )

    return nearest_systems[0].system_name


def distance_to_system(start_system, end_system, database):
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