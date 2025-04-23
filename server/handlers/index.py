from flask import redirect, render_template, url_for, request
from server.constants import POWERNAMES, TASKNAMES
from server.status import status
from server.tasks.tasks import isTaskACrime


def handle_index(request):
    selected_system = None
    selected_task = None
    selected_power = None

    if request.method == "POST":
        selected_system = request.form.get("system")
        selected_task = request.form.get("mission")
        selected_power = request.form.get("power")

        if isTaskACrime(selected_task, False):
            return redirect(
                url_for(
                    "is_crime",
                    taskName=selected_task,
                    power=selected_power,
                    system=selected_system,
                )
            )
        else:
            return redirect(
                url_for(
                    "results",
                    system=selected_system,
                    taskName=selected_task,
                    power=selected_power,
                )
            )

    if request.cookies.get("ppa_cmdrname", None) != None:
        cmdr_name = request.cookies.get("ppa_cmdrname")
        system_name = request.cookies.get("ppa_last_system")
        power = request.cookies.get("ppa_power")
        local_powernames = POWERNAMES
        for i in range(len(local_powernames)):
            if local_powernames[i] == power:
                local_powernames.insert(0, local_powernames.pop(i))
    
        return render_template(
            "index.html",
            missions=TASKNAMES,
            powers=local_powernames,
            status_emoji = status()[0],
            status_text = status()[1],
            welcome_message=f"Welcome CMDR {cmdr_name}",
            welcome_button_link="https://capi.niceygy.net/logout",
            welcome_button_message="Logout",
            default_system=system_name
        )
    return render_template(
        "index.html",
        missions=TASKNAMES,
        powers=POWERNAMES,
        status_emoji = status()[0],
        status_text = status()[1],
        default_system="Sol",
        welcome_button_link="https://capi.niceygy.net/authorize",
        welcome_button_message="Login",
        welcome_message="Welcome anonymous CMDR."
    )