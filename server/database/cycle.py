def write_cycle_week(week):
    with open(f"week.txt", "w") as f:
        f.write(week)
        f.close()
    return

def get_cycle_week():
    with open("week.txt", "r") as f:
        data = f.read().strip()
        f.close()
    return data