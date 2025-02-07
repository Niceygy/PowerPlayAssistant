import threading
import time
from datetime import datetime, timedelta
from dateutil.parser import parse
import requests


def write_cycle_week(week):
    with open(f"cache/week.txt", "w") as f:
        f.write(week)
        f.close()
    return

def get_cycle_week():
    with open("cache/week.txt", "r") as f:
        data = f.read().strip()
        f.close()
    return data

def get_seconds_until_target(target_hour=7, target_minute=0):
    now = datetime.now()
    target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    
    if target < now:
        target += timedelta(days=1)
    
    return (target - now).total_seconds()

def update_cycle_week():    
    print(" * Started tick watcher")
    while True:
        try:
            # Calculate initial delay to target time (e.g. 7:00)
            delay = get_seconds_until_target(8, 0)
            time.sleep(delay)
            
            now = datetime.now()
            if now.weekday() == 3:  # Thursday
                print("Updating cycle week...")
                try:
                    edcd_tick = requests.get("https://tick.edcd.io/api/tick", timeout=30).text.replace('"', '')
                    tick_time = parse(edcd_tick)
                    if tick_time.isoweekday() == 4:
                        if tick_time.date() == now.date():
                            write_cycle_week(get_cycle_week() + 1) 
                            if get_cycle_week() > 6:
                                write_cycle_week(1)
                            print(f"CYCLE_WEEK updated to: {get_cycle_week()}")
                except (requests.RequestException, ValueError) as e:
                    print(f"Error fetching tick data: {e}")

            # Sleep until next check (24 hours)
            time.sleep(24 * 60 * 60)
            
        except Exception as e:
            print(f"Error in update cycle: {e}")
            time.sleep(60)  # Wait a minute before retrying on error


def watch_tick():
    # Start the update_cycle_week function in a separate thread
    thread = threading.Thread(target=update_cycle_week)
    thread.daemon = True
    thread.start()
    return