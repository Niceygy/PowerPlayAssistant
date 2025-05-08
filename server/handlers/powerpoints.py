from flask import render_template
from server.database.powerpoints import nicey_powerpoints, kruger_powerpoints, fdev_powerpoints
import random

POWERPOINT_CACHE = {
    "data": [],  # the data itself
    "time": 0,  # last written time
}
"""
Stops it from overloading the database
"""


def handle_powerpoints(request, database):
    # Load last week's powerpoints and timestamp

    points_type = request.args.get("system", "nicey")

    result = []

    match points_type:
        case "nicey":
            result = nicey_powerpoints(database)
        case "fdev":
            result = fdev_powerpoints(database)
        case "kruger":
            result = kruger_powerpoints(database)

    # GH Copilot Magic, orders them from most to least points
    result.sort(key=lambda x: x["points"], reverse=True)

    place = 1
    for item in result:
        item["place"] = place
        place += 1
        
    title = "Short PP Report" if random.randint(0, 10) == 1 else "How is your power doing?"
    
    return render_template("powerpoints.html", powerdata=result, title=title)
