import json  # Add this to handle JSON file storage
from flask import render_template
from server.powers import calculate_powerpoints, how_many_systems
from server.constants import POWERS

def handle_powerpoints(request, database):
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
        
        comparison_message = ""
        if last_week_points > points:
            comparison_message = f"They are down {last_week_points - points} points this week, from {last_week_points} last week."
        elif last_week_points < points:
            comparison_message = f"They are up {points - last_week_points} points this week, from {last_week_points} last week."
        else:
            comparison_message = f"They have not changed points this week from last weeks total of {last_week_points}"

        message = ["", "", "", "", ""]
        message[0] = f"{item} has {points} points"
        message[1] = f"They have {exploited} Exploited systems, {fortified} fortified systems & {stronghold} stronghold systems"
        message[2] = f"This gives them a total of {total} systems!"
        message[3] = comparison_message

        result.append([key, item, message, 0, points])

    # Save current week's powerpoints only if not already updated this week
    from datetime import datetime
    current_week = datetime.now().isocalendar()[1]  # Get the current week number
    if last_updated != current_week:
        with open("cache/last_week_powerpoints.json", "w") as f:
            last_week_data["_last_updated"] = current_week
            json.dump({**{item[0]: item[4] for item in result}, "_last_updated": current_week}, f)

    result.sort(key=lambda x: x[4], reverse=True)
    place = 0
    for item in result:
        item[3] = place
        place += 1

    return render_template(
        "powerpoints.html",
        powerdata=result
    )

def handle_powerpoints_raw(request, database):
    result = []
    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)
        points = calculate_powerpoints(exploited, fortified, stronghold)
        result.append([exploited, fortified, stronghold, points])
    return result