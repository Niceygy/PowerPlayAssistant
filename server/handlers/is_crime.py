from flask import redirect, render_template, url_for
from server.database.database import find_nearest_anarchy_systems, system_coordinates


def handle_is_crime(request, database):
    """
    Handler for page: /is_crime

    If the selected task is a crime, informs the user &
    asks if they want to find an anarchy system nearby.

    Methods: GET, POST

    Redirects to /results on POST, and adds a ?anarchy=
    Renders is_crime.html on GET

    """
    if request.method == "GET":
        task = request.args.get("taskName")
        power = request.args.get("power")
        system = request.args.get("system")
        return render_template("is_crime.html", task=task, power=power, system=system)
    else:
        task = request.form.get("taskName")
        power = request.form.get("power")
        system = request.form.get("system")
        anarchy = request.form.get("anarchy")

        if anarchy == "Yes":
            anarchy = True
            # we need to find an anarchy system!
            coords = system_coordinates(system, database)
            if coords == None:
                    return render_template(
                        "does_not_work.html", ERRORDATA="System could not be found", ERRORCODE="IRRETREVABLE"
                    )
            start_x = coords[0]
            start_y = coords[1]
            start_z = coords[2]
            
            system = find_nearest_anarchy_systems(
                start_x, start_y, start_z, database.session
            )
        else:
            anarchy = False

        if task == "Holoscreen Hacking":
            return redirect(
                url_for(
                    "handle_choice",
                    system=system,
                    taskName=task,
                    power=power,
                    anarchy=anarchy,
                )
            )
        else:
            return redirect(
                url_for(
                    "results",
                    system=system,
                    taskName=task,
                    power=power,
                    anarchy=anarchy,
                )
            )