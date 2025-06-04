import json
import math
from flask import render_template, redirect, url_for
from sqlalchemy import and_, or_, func
from server.database.database import StarSystem, distance_to_system, Conflicts
from server.constants import POWERNAMES
from server.powers import power_full_to_short, short_to_full_power
from server.database.cache import Cache


def handle_conflict_search(request, database):
    return render_template("conflicts/search.html", powers=POWERNAMES)


def handle_conflict_result(request, database):
    power = None
    system_name = None
    if request.method == "POST":
        power = request.form.get("power")
        system_name = request.form.get("system")
        return redirect(
            url_for("conflicts_result", system_name=system_name, power=power)
        )
    else:
        power = request.args.get("power")
        shortcode = power_full_to_short(power)
        system_name = request.args.get("system_name")

        cache = Cache()
        res = cache.get(f"{power}_{system_name}", "conflicts")
        if res is not None:
            return render_template(
                "conflicts/result.html",
                systems=json.loads(res[0]),
                systemName=system_name,
                power=power,
            )

        user_system = (
            database.session.query(StarSystem)
            .filter_by(system_name=system_name)
            .first()
        )
        if not user_system:
            # nowhere.....
            return []

        user_coords = (user_system.longitude, user_system.latitude, user_system.height)

        distance = func.sqrt(
            func.pow(StarSystem.longitude - user_coords[0], 2)
            + func.pow(StarSystem.latitude - user_coords[1], 2)
            + func.pow(StarSystem.height - user_coords[2], 2)
        ).label("distance")

        query = (
            database.session.query(StarSystem, Conflicts )
            .join(Conflicts, StarSystem.system_name == Conflicts.system_name)
            .filter(
                and_(
                    Conflicts.cycle is not None,
                    or_(
                        Conflicts.first_place == shortcode,
                        Conflicts.second_place == shortcode,
                    ),
                ),
            )
            .order_by(distance)
            .limit(20)
        )

        result = []
        for item in query:
            item = item[1]
            result.append(
                {
                    "name": item.system_name,
                    "power1": short_to_full_power(item.first_place),
                    "power2": short_to_full_power(item.second_place),
                    "ly": math.trunc(
                        distance_to_system(system_name, item.system_name, database)
                    ),
                }
            )

        cache.add(f"{power}_{system_name}",  json.dumps(result), "conflicts", 1)
        cache.__exit__()

        return render_template(
            "conflicts/result.html", systems=result, systemName=system_name, power=power
        )
