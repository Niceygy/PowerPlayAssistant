from flask import redirect, render_template, url_for
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

    return render_template(
        "index.html",
        missions=TASKNAMES,
        powers=POWERNAMES,
        status_emoji = status()[0],
        status_text = status()[1]
    )