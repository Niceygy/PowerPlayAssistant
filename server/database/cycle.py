import threading
import time
from datetime import datetime, timedelta
from dateutil.parser import parse
import requests

CYCLE_WEEK = 0

def update_cycle_week():
    global CYCLE_WEEK
    while True:
        now = datetime.now()
        if now.weekday() == 3:  # Thursday
            print("Updating cycle week...")
            edcd_tick = requests.get("https://tick.edcd.io/api/tick").text.replace('"', '')
            tick_time = parse(edcd_tick)
            if tick_time.isoweekday() == 4:
                if tick_time.date() == now.date():
                    CYCLE_WEEK += 1
                    if CYCLE_WEEK > 6:
                        CYCLE_WEEK = 1
                    print(f"CYCLE_WEEK updated to: {CYCLE_WEEK}")
        time.sleep(60 * 60 * 24)  # Sleep for 24 hours

# Start the update_cycle_week function in a separate thread
thread = threading.Thread(target=update_cycle_week)
thread.daemon = True
thread.start()