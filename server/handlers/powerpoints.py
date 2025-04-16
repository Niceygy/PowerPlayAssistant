from flask import render_template
from server.powers import calculate_powerpoints, how_many_systems
from server.constants import POWERS

def handle_powerpoints(request, database):
    #[powerShortCode, PowerFullName, message, place]
    result = []
    for key, item in POWERS.items():
        exploited, fortified, stronghold, total = how_many_systems(item, database)
        points = calculate_powerpoints(exploited, fortified, stronghold)
        message = ["","","",""]
        message[0] = f"{item} has {points} points"
        message[1] = f"They have {exploited} Exploited systems, {fortified} fortified systems & {stronghold} stronghold systems"
        message[2] = f"This gives them a total of {total} systems!"
        
        result.append([key, item, message, 0, points])
    
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