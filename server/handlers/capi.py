from flask import make_response, redirect, render_template, request, url_for
from datetime import timedelta, datetime
from server.database.systems import query_star_systems

def handle_capi(request, database):
    #redirect(f"{POWERPLAY_ASSISTANT_URL}/import?name={cmdr_name}&power={power}&system={system}")
    cmdr_name = request.args.get("name")
    power = request.args.get("power")
    system_name = request.args.get("system")
    
    if query_star_systems(system_name) == None:
        #??
        system_name = "Sol"
    
    response = make_response(
        redirect(
            url_for("index")
        )
    )
    response.set_cookie("ppa_cmdrname", cmdr_name, expires=datetime.now() + timedelta(days=30))
    response.set_cookie("ppa_power", power, expires=datetime.now() + timedelta(days=300))
    response.set_cookie("ppa_last_system", system_name, expires=datetime.now() + timedelta(days=30))
    
    return response
    
def handle_logout():
    response = make_response(
        render_template(
        "redirect.html",
        strong="Logout Complete",
        description="You have been logged out from PowerPlay Assistant. Please press OK to complete the logout.",
        url="https://capi.niceygy.net/logout"
        )
    )
    
    response.set_cookie("ppa_cmdrname", None, expires=datetime.now(), path="/")
    response.set_cookie("ppa_power", None, expires=datetime.now(), path="/")
    response.set_cookie("ppa_last_system", None, expires=datetime.now() + timedelta(seconds=500), path="/")
    
    return response