from flask import render_template
from server.constants import TASKSHORTCODES
from server.powers import power_full_to_short

def handle_escape_pods(request, database):
    system = request.args.get("system")
    task = request.args.get("taskName")
    power = request.args.get("power")

    #https://forums.frontier.co.uk/threads/elite-dangerous-trailblazers-update-3-wednesday-april-30.636973/
    task_replacements = {
        "ALD": "SLFP",
        "ARD": "",
        "ASD": "TPCL",
        "DPT": "",
        "EMH": "HISV",
        "FLW": "SMNR",
        "JRA": "",
        "LYR": "",
        "NAK": "HISV",
        "PRA": "SRGD",
        "YRG": "SSWK",
        "ZMT": "",
    }

    shortcode = power_full_to_short(power)
    task_short = task_replacements[shortcode]
    task_full = TASKSHORTCODES[task_short]
    
    return render_template(
        "tasks/escapePods.html",
        system=system,
        power=power,
        taskName=task,
        task_replacement=task_full,
    )
