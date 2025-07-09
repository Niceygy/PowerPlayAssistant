from typing import List
from flask import redirect, render_template, url_for
from datetime import datetime
import requests, math
from server.constants import POWERNAMES, TASKNAMES, PP_TYPE_TRANSLATIONS, CG_FILTER_LIST
from server.status import get_status
from server.tasks.tasks import isTaskACrime


def load_community_goals() -> List[object]:
    OERVE_URI = "https://api.orerve.net/2.0/website/initiatives/list?lang=en"
    data = requests.get(OERVE_URI).json()

    goals = []

    for item in data["activeInitiatives"]:
        if any(f in item["title"].lower() for f in CG_FILTER_LIST):
            completion = math.trunc(
                (float(item["qty"]) / float(item["target_qty"])) * 100
            )
            expiry_dt = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
            days_remaining = (expiry_dt - datetime.now()).days
            goals.append(
                {
                    "title": f"{item['title']}",
                    "body1": f"Hand in {PP_TYPE_TRANSLATIONS[item['activityType']]} to {item['market_name']} in {item['starsystem_name']}",
                    "body2": f"You have {days_remaining} days remaining. Current completion: {completion}% ",
                }
            )
    return goals


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

    cg = load_community_goals()
    if cg == []:
        cg_title = ""
    else:
        cg_title = "Powerplay Commuinity Goals"

    return render_template(
        "index.html",
        missions=TASKNAMES,
        powers=POWERNAMES,
        status_text=get_status(),
        default_system="Sol",
        cg_title=cg_title,
        cg_data=cg,
    )
