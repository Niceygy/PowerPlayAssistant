import sqlite3, math
from datetime import datetime, timedelta
from server.constants import POWERS
from server.powers import how_many_systems


def powerplay_cycle() -> int:
    """
    Returns the current powerplay cycle number
    """
    # 31 oct '24
    powerplay_startdate = datetime(2024, 10, 31, 8)
    now = datetime.now()

    cycle = (now - powerplay_startdate).days / 7

    return math.trunc(cycle)


def save_powerpoints(last_updated: int, result: list, table: str) -> None:
    """
    Saves the current powerpoints to the powerpoints.db
    """
    # make sure the week starts on the tick (thurs)!
    if last_updated != powerplay_cycle():
        conn = sqlite3.connect("cache/powerpoints.db")
        cursor = conn.cursor()
        # Create tables if they don't exist
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                shortcode TEXT,
                points INTEGER,
                cycle_week INTEGER
            )
        """
        )

        # Update
        for item in result:
            try:
                cursor.execute(
                    f"SELECT * FROM {table} WHERE cycle_week = ? AND shortcode = ?",
                    (powerplay_cycle(), item["shortcode"]),
                )
            except Exception:
                cursor.execute(
                    f"INSERT INTO {table} (shortcode, points, cycle_week) VALUES (?, ?, ?)",
                    (item["shortcode"], item["points"], powerplay_cycle()),
                )
                conn.commit()
            res = cursor.fetchone()
            if res is None:
                cursor.execute(
                    f"INSERT INTO {table} (shortcode, points, cycle_week) VALUES (?, ?, ?)",
                    (item["shortcode"], item["points"], powerplay_cycle()),
                )
                conn.commit()

        conn.commit()
        conn.close()


def last_weeks_ppoints(table: str):
    """
    Retuns the powerpoints for last week, for that powerpoints system
    (as defined by table)
    """
    conn = sqlite3.connect("cache/powerpoints.db")
    cursor = conn.cursor()
    try:
        result = {}
        for shortcode, _ in POWERS.items():
            cursor.execute(
                f"SELECT points FROM {table} WHERE cycle_week = {powerplay_cycle() - 1} AND shortcode = '{shortcode}'"
            )
            fetched = cursor.fetchone()
            result[shortcode] = (
                fetched[0] if fetched else 0
            )  # Store points in a dictionary
        return result, (powerplay_cycle() - 1)
    except Exception:
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                shortcode TEXT,
                points INTEGER,
                cycle_week INTEGER
            )
        """
        )
        return {}, (powerplay_cycle() - 1)


def nicey_powerpoints(database):
    result = []
    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)
        points = exploited + (fortified * 2) + (stronghold * 4)

        last_week_data, last_updated = last_weeks_ppoints("nicey")
        last_week_points = last_week_data.get(key, 0)  # Default to 0

        # comparison
        comparison_message = ""
        if last_week_points > points:
            comparison_message = f"{last_week_points - points} pts [{points}]"
        elif last_week_points < points:
            comparison_message = f"{points - last_week_points} pts [{points}]"
        else:
            comparison_message = f"0 pts [{points}]"

        data = {
            "place": 0,
            "shortcode": key,
            "name": item,
            "systems": f"{exploited} Exploited, {fortified} fortified & {stronghold} strongholds [{total} total]",
            "total_systems": total,
            "comparison": comparison_message,
            "comparison_icon": (
                "up_icon.svg" if points >= last_week_points else "down_icon.svg"
            ),
            "points": points,
        }

        result.append(data)

    save_powerpoints(last_updated, result, "nicey")

    return result


def fdev_powerpoints(database):
    result = []
    last_week_data, last_updated = last_weeks_ppoints("fdev")

    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)
        points = total

        last_week_points = last_week_data.get(key, 0)  # Default to 0

        data = {
            "place": 0,
            "shortcode": key,
            "name": item,
            "systems": f"{exploited} Exploited, {fortified} fortified & {stronghold} strongholds [{total} total]",
            "total_systems": total,
            "comparison": f"{points} systems total",
            "comparison_icon": (
                "up_icon.svg" if last_week_points <= points else "down_icon.svg"
            ),
            "points": points,
        }

        result.append(data)

    save_powerpoints(last_updated, result, "fdev")

    return result


def kruger_powerpoints(database):
    exploited_points = 12
    fortified_points = 45
    stronghold_points = 113

    last_week_data, last_updated = last_weeks_ppoints("kruger")

    result = []
    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)

        points = (
            (exploited_points * exploited)
            + (fortified_points * fortified)
            + (stronghold_points * stronghold)
        )

        last_week_points = last_week_data.get(key, 0)  # Default to 0

        # comparison
        comparison_message = ""
        if last_week_points > points:
            comparison_message = f"{last_week_points - points} pts [{points}]"
        elif last_week_points < points:
            comparison_message = f"{points - last_week_points} pts [{points}]"
        else:
            comparison_message = f"0 pts [{points}]"

        data = {
            "place": 0,
            "shortcode": key,
            "name": item,
            "systems": f"{exploited} Exploited, {fortified} fortified & {stronghold} strongholds [{total} total]",
            "total_systems": total,
            "comparison": comparison_message,
            "comparison_icon": (
                "up_icon.svg" if points > last_week_points else "down_icon.svg"
            ),
            "points": points,
        }

        result.append(data)

    save_powerpoints(last_updated, result, "kruger")
    return result
