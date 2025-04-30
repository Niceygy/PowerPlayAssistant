"""
PLEDGE TO POWER

WALK THROUGH DETAILS OF POWER

OVERALL PP INTRO - AQUIRING SYSTEMS, ECTs

FIRST TASKS
"""

from flask import render_template
from server.constants import POWER_ABOUT, POWERS, POWER_PERKS, POWER_BEST_FOR

def handle_pledge(request, database):
    result = []
    for shortcode, power in POWERS.items():
        result.append({
            'name': power,
            'shortcode': shortcode,
            'about': POWER_ABOUT[shortcode],
            'perks': POWER_PERKS[shortcode],
            'best_for': POWER_BEST_FOR[shortcode]
        })
        
    return render_template(
        "intro/welcome.html",
        powerdata=result
    )
        
        