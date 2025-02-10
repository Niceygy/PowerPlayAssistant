from flask import redirect, render_template, url_for


def handle_task_choice(request):
    system = request.args.get("system")
    task = request.args.get("taskName")
    power = request.args.get("power")

    if request.method == "POST":
        choice = request.form.get("choice")
        system = request.form.get("system")
        task = request.form.get("task")
        power = request.form.get("power")

        return redirect(
            url_for("results", system=system, power=power, taskName=task, choice=choice)
        )
    
    else:
        return render_template(
            "tasks/task_choice.html", system=system, power=power, taskName=task
        )