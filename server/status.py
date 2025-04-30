import requests

def ed_status() -> str:
    resp = requests.get("https://ed-server-status.orerve.net")
    if resp.ok:
        json_data = resp.json()
        return json_data['status']
    else:
        return 'Unknown Status Error'

def set_status(message: str, colour: str) -> None:
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

def get_status() -> list[str]:
    try:
        data = open("cache/status.txt", "r").readlines()
        return [data[0], data[1], ed_status()]
    except Exception:
        open("cache/status.txt", "x").write(f"All Operational\n🟢")
        return ["Status File Error", "🔴", ed_status()]