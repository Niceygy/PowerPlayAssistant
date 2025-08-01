from flask import render_template
from server.constants import POWERNAMES
from server.powers import power_full_to_short
from server.tasks.findNear import find_nearby_system

def handle_system_search(request, database):
    if request.method == "GET":
        return render_template(
            "system_search/search.html",
            powers=POWERNAMES
        )
    else:
        system_name = request.form.get("system")
        power_short_code = power_full_to_short(request.form.get("power"))
        system_type = request.form.get("system_type")
        found_system_name = find_nearby_system(system_name, power_short_code,system_type, database.session)
        system_type_clean = ""
        match system_type:
            case "no_owner":
                system_type_clean = "Unoccupied"
            case "you_own":
                system_type_clean = "Reinforcing"
            case "enemy_owns":
                system_type_clean = "Undermining"
        return render_template(
            "system_search/found.html",
            original_system=system_name,
            power=request.form.get("power"),
            system_type=system_type_clean,
            found_system=found_system_name
        )