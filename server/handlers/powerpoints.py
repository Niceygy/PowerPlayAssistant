from flask import render_template
from server.powers import calculate_powerpoints
from server.constants import POWERS

def handle_powerpoints(request, database):
    #[powerShortCode, PowerFullName, message, place]
    result = []
    i = 0
    for key, item in POWERS.items():
        points = calculate_powerpoints(item, database)
        message = f"{item} has {points[0]} points!"
        result.append([key, item, message, i])
        i+=1
    
    return render_template(
        "powerpoints.html",
        powerdata=result
    )