import json
from datetime import datetime, timedelta
from server.constants import POWERS
from server.powers import how_many_systems


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
                    **{item["shortcode"]: item["points"] for item in result},
                    "_last_updated": current_week,
                },
                f,
            )
    return

def last_weeks_ppoints():
    try:
        with open("cache/week_before_last_powerpoints.json", "r") as f:
            last_week_data = json.load(f)
            last_updated = last_week_data.get("_last_updated", None)
            return last_week_data, last_updated
    except Exception:
        open("cache/week_before_last_powerpoints.json", "w").writelines(["{", "}"])
        last_week_data = {}
        last_updated = None
        return last_week_data, last_updated


def nicey_powerpoints(database):
    result = []
    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)
        points = exploited + (fortified * 2) + (stronghold * 4)

        last_week_data, last_updated = last_weeks_ppoints()
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

        save_powerpoints(last_updated, last_week_data, result)

    return result


def kruger_powerpoints(database):
    exploited_points = 12
    fortified_points = 45
    stronghold_points = 113
    
    result = []
    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)
        
        points = (exploited_points * exploited) + (fortified_points * fortified) + (stronghold_points * stronghold)
        
        last_week_data = {}
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

        # save_powerpoints(last_updated, last_week_data, result)
        
    return result