import json, math
from datetime import datetime, timedelta
from flask import render_template
from server.powers import calculate_powerpoints, how_many_systems, short_to_full_power
from server.constants import POWERS

POWERPOINT_CACHE = {
    "data": [],  # the data itself
    "time": 0,  # how many times it has only been read from cache.
}

def save_powerpoints(last_updated, last_week_data, result) -> None:
    # Save current week's powerpoints only if not already updated this week
    current_week = (
        datetime.now() - timedelta(days=(datetime.now().weekday() - 3) % 7)
    ).isocalendar()[1]
    # make sure the week starts on the tick (thurs)!
    if last_updated != current_week:
        with open("cache/last_week_powerpoints.json", "r") as f:
            week_before_last_data = f.read()  # Save current last week's data
        with open("cache/week_before_last_powerpoints.json", "w") as f:
            f.write(week_before_last_data)  # Write it to a new file
        with open("cache/last_week_powerpoints.json", "w") as f:
            last_week_data["_last_updated"] = current_week
            json.dump(
                {
                    **{item[0]: item[4] for item in result},
                    "_last_updated": current_week,
                },
                f,
            )
    return

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
        with open("cache/week_before_last_powerpoints.json", "r") as f:
            last_week_data = json.load(f)
            last_updated = last_week_data.get("_last_updated", None)
    except FileNotFoundError:
        open("cache/week_before_last_powerpoints.json", "w").write("{\n}")
        last_week_data = {}
        last_updated = None

    result = []
    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)
        points = calculate_powerpoints(exploited, fortified, stronghold)
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
            'place': 0,
            'shortcode': key,
            'name': item,
            'systems': f"{exploited} Exploited, {fortified} fortified & {stronghold} strongholds [{total} total]",
            'total_systems': total,
            'comparison': comparison_message,
            'comparison_icon': "up_icon.svg",
            'points': points
        }

        result.append(data)

    save_powerpoints(last_updated, last_week_data, result)

    # GH Copilot Magic, orders them from most to least points
    result.sort(key=lambda x: x['points'], reverse=True)

    place = 0
    for item in result:
        item['place'] = place
        place += 1


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
