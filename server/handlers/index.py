from flask import make_response, redirect, render_template, url_for
from datetime import datetime, timedelta
from server.constants import POWERNAMES, TASKNAMES
from server.status import get_status
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
        # user is logged in
        cmdr_name = request.cookies.get("ppa_cmdrname")
        system_name = request.cookies.get("ppa_last_system")
        power = request.cookies.get("ppa_power")
        local_powernames = POWERNAMES
        for i in range(len(local_powernames)):
            if local_powernames[i] == power:
                local_powernames.insert(0, local_powernames.pop(i))

        if request.cookies.get("ppa_last_visit", None) != None:
            last_visit = datetime.strptime(
                request.cookies.get("ppa_last_visit"), "%Y-%m-%d %H:%M:%S"
            )
            if datetime.now() - last_visit > timedelta(hours=12):
                response = make_response(redirect("https://capi.niceygy.net/userinfo/ppa"))
                response.set_cookie(
                   "ppa_last_visit", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                return response

        response = make_response(
            render_template(
                "index.html",
                missions=TASKNAMES,
                powers=local_powernames,
                status_text=get_status(),
                welcome_message=f"Welcome CMDR {cmdr_name}",
                welcome_button_link="https://capi.niceygy.net/logout",
                welcome_button_message="Logout",
                default_system=system_name,
            )
        )
        if request.cookies.get("ppa_last_visit", None) == None:
            response.set_cookie(
                "ppa_last_visit", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        return response

    return render_template(
        "index.html",
        missions=TASKNAMES,
        powers=POWERNAMES,
        status_text=get_status(),
        default_system="Sol",
        welcome_button_link="https://capi.niceygy.net/authorize",
        welcome_button_message="Login",
        welcome_message="Welcome anonymous CMDR.",
    )
    
