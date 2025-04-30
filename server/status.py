import requests

def ed_status() -> str:
    """Returns the status of ED, as shown by the launcher

    Returns:
        str: Text to be shown
    """
    resp = requests.get("https://ed-server-status.orerve.net")
    if resp.ok:
        json_data = resp.json()
        if json_data['status'] == "Online":
            return "🟢 Online"
        else:
            return f"🔴 {json_data['status']}"
    else:
        return '🔴 Unknown Status Error'

def set_status(message: str, colour: str) -> None:
    """Sets the status for PPA

    Args:
        message (str): The message to be shown
        colour (str): green, yellow or red
    """
    if colour == "green":
        emoji = "🟢"
    elif colour == "yellow":
        emoji = "🟡"
    else:
        emoji = "🔴"
    try:
        open("cache/status.txt", "w").write(f"{message}\n{emoji}")
    except Exception:
        open("cache/status.txt", "x").write(f"{message}\n{colour}")
    return

def get_status() -> str:
    """Returns the status for PPA and Elite

    Returns:
        str: The text to be shown
    """
    try:
        data = open("cache/status.txt", "r").readlines()
        return f"{data[1]} PPA: {data[0]}, ED: {ed_status()}"
    except Exception:
        open("cache/status.txt", "x").write(f"All Operational\n🟢")
        return f"🔴 PPA: Status File Error, ED: {ed_status()}"