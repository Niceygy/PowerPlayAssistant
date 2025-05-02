from flask import render_template, request
from server.database.powerpoints import nicey_powerpoints, kruger_powerpoints
# from server.powers import calculate_powerpoints, how_many_systems
from server.constants import POWERS

POWERPOINT_CACHE = {
    "data": [],  # the data itself
    "time": 0,  # last written time
}
"""
Stops it from overloading the database
"""


def handle_powerpoints(request, database):

    # # cache

    # if (
    #     math.isclose(
    #         POWERPOINT_CACHE["time"],
    #         (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds(),
    #         abs_tol=500,
    #     )
    #     and POWERPOINT_CACHE["data"] is not []
    # ):
    # within 500S of cache being updated, all OK
    # return render_template("powerpoints.html", powerdata=POWERPOINT_CACHE["data"])

    # Load last week's powerpoints and timestamp

    points_type = request.args.get("system", "nicey")

    result = []

    match points_type:
        case "nicey":
            result = nicey_powerpoints(database)
        case "fdev":
            print()
        case "kruger":
            result = kruger_powerpoints(database)

    # GH Copilot Magic, orders them from most to least points
    result.sort(key=lambda x: x["points"], reverse=True)

    place = 1
    for item in result:
        item["place"] = place
        place += 1

    # # and return!
    # POWERPOINT_CACHE["data"] = result
    # POWERPOINT_CACHE["time"] = (
    #     datetime.utcnow() - datetime(1970, 1, 1)
    # ).total_seconds()
    return render_template("powerpoints.html", powerdata=result)


# def handle_powerpoints_raw(request, database):
#     result = []
#     for key, item in POWERS.items():
#         exploited, fortified, stronghold, total = how_many_systems(item, database)
#         points = calculate_powerpoints(exploited, fortified, stronghold)
#         result.append([exploited, fortified, stronghold, points])
#     return result
