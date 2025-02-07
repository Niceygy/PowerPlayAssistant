import requests
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse

def get_week_of_cycle():
    """
    Determines the current week of the megaship cycle using data from tick.edcd.io.
    Returns:
        int: The current week of the cycle (1-6)
    """
    # Fetch the latest tick data from tick.edcd.io
    response = requests.get("https://tick.edcd.io/api/tick")
    if response.status_code != 200:
        raise Exception("Failed to fetch tick data")

    latest_tick = response.text.replace('"', '')

    # Convert the latest tick time to a datetime object
    latest_tick_datetime = parse(latest_tick)

    # Calculate the number of Thursdays since the latest tick
    current_date = datetime.now(timezone.utc)
    thursdays_count = 0
    while latest_tick_datetime <= current_date:
        if latest_tick_datetime.weekday() == 3:  # Thursday
            thursdays_count += 1
        latest_tick_datetime += timedelta(days=1)

    # Calculate the current week of the cycle
    weeks = thursdays_count % 6
    print(weeks)
    if weeks == 0:
        weeks = 6

    print(weeks)

    return weeks

get_week_of_cycle()