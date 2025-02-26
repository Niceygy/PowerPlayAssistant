import time
from datetime import datetime, timedelta
import threading

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

def get_seconds_until_target(target_hour=7, target_minute=0):
    """
    How many seconds until the target time?
    """
    now = datetime.now()
    target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    
    if target < now:
        target += timedelta(days=1)
    
    return (target - now).total_seconds()

def update_cycle_week():
    """
    Watches for the tick, and updates accordingly
    """
    print(" * Started tick watcher")
    print(f" * Week is {get_cycle_week()}")
    while True:
        try:
            # Calculate initial delay to target time (e.g. 7:00)
            delay = get_seconds_until_target(8, 30)
            print(f" * There are {delay} seconds until tick")
            time.sleep(delay)
            
            now = datetime.now()
            if now.weekday() == 3:  # Thursday
                print("Updating cycle week...")
                write_cycle_week(get_cycle_week() + 1) 
                if get_cycle_week() > 6:
                    write_cycle_week(1)
                    print(f"CYCLE_WEEK updated to: {get_cycle_week()}")

            # Sleep until next check (24 hours)
            time.sleep(24 * 60 * 60)
            
        except Exception as e:
            print(f"Error in update cycle: {e}")
            time.sleep(60)  # Wait a minute before retrying on error


def watch_tick():
    """
    Starts the tick watcher in a seperate thread
    """
    thread = threading.Thread(target=update_cycle_week)
    thread.daemon = True
    thread.start()
    return
