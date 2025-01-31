STATUS = "OK"

def status():
    if STATUS == "OK":
        return ["🟢", "All working"]
    elif STATUS == "SORTA":
        return ["🟠", "Partially Working"]
    else:
        return ["🔴", "Kaput"]