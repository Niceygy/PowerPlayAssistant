global STATUS
STATUS = "OK"
global STATUS_EMOJI
STATUS_EMOJI = "🟢"

def status():
    return [STATUS_EMOJI, STATUS]

def update_status(new_status, emoji):
    global STATUS
    global STATUS_EMOJI
    STATUS = new_status
    if emoji == "green":
        STATUS_EMOJI = "🟢"
    elif emoji == "yellow":
        STATUS_EMOJI = "🟠"
    else:
        STATUS_EMOJI = "🔴"