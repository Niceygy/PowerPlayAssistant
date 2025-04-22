import json, math
from datetime import datetime, timedelta
from flask import render_template
from server.powers import calculate_powerpoints, how_many_systems, short_to_full_power
from server.constants import POWERS

POWERPOINT_CACHE = {
    "data": [],  # the data itself
    "time": 0,  # how many times it has only been read from cache.
}


def handle_powerpoints(request, database):

    # cache

    if (
        math.isclose(
            POWERPOINT_CACHE["time"],
            (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds(),
            abs_tol = 500,
        )
        and POWERPOINT_CACHE["data"] is not []
    ):
        # within 500S of cache being updated, all OK
        return render_template("powerpoints.html", powerdata=POWERPOINT_CACHE["data"])

    # Load last week's powerpoints and timestamp
    try:
        with open("cache/last_week_powerpoints.json", "r") as f:
            last_week_data = json.load(f)
            last_updated = last_week_data.get("_last_updated", None)
    except FileNotFoundError:
        open("cache/last_week_powerpoints.json", "w").write("{\n}")
        last_week_data = {}
        last_updated = None

    result = []
    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)
        points = calculate_powerpoints(exploited, fortified, stronghold)
        last_week_points = last_week_data.get(key, 0)  # Default to 0 if no data exists

        # comparison
        comparison_message = ""
        if last_week_points > points:
            comparison_message = f"They are down {last_week_points - points} points this week, from {last_week_points} last week"
        elif last_week_points < points:
            comparison_message = f"They are up {points - last_week_points} points this week, from {last_week_points} last week"
        else:
            comparison_message = f"They have not changed points this week from last weeks total of {last_week_points}"

        # assemble message
        message = ["", "", "", "", "", ""]
        message[0] = f"{item} has {points} points, from {total} systems"
        message[1] = (
            f"({exploited} Exploited systems, {fortified} fortified & {stronghold} strongholds)"
        )
        message[2] = comparison_message

        result.append([key, item, message, 0, points])

    # Save current week's powerpoints only if not already updated this week
    current_week = (
        datetime.now() - timedelta(days=(datetime.now().weekday() - 3) % 7)
    ).isocalendar()[1]
    # make sure the week starts on the tick (thurs)!
    if last_updated != current_week:
        with open("cache/last_week_powerpoints.json", "w") as f:
            last_week_data["_last_updated"] = current_week
            json.dump(
                {
                    **{item[0]: item[4] for item in result},
                    "_last_updated": current_week,
                },
                f,
            )

    # GH Copilot Magic, orders them from most to least points
    result.sort(key=lambda x: x[4], reverse=True)

    # points comparison across powers
    last_powers_points = 0
    last_power = ""
    place = 0
    for item in result:
        item[3] = place
        place += 1
        if last_powers_points != 0:
            if math.isclose(last_powers_points, item[4], abs_tol=30):
                item[2][2] += f", & are close to {last_power}"
        last_powers_points = item[4]
        last_power = short_to_full_power(item[0])

    # and return!
    POWERPOINT_CACHE["data"] = result
    POWERPOINT_CACHE["time"] = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    return render_template("powerpoints.html", powerdata=result)


def handle_powerpoints_raw(request, database):
    result = []
    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)
        points = calculate_powerpoints(exploited, fortified, stronghold)
        result.append([exploited, fortified, stronghold, points])
    return result
