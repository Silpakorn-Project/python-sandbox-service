"common utility"
from datetime import datetime, timedelta, timezone

def get_datetime_format_th():
    """
    This Python code helps you get the current time in Thailand by adjusting the time from UTC
    (Coordinated Universal Time).
    First, it grabs the current time in UTC using Python's built-in tools.
    UTC is the standard time used globally, and it doesn't change with time zones.
    To get the time in Thailand, the code adds 7 hours to the UTC time,
    since Thailand is 7 hours ahead of UTC.

    After adjusting the time, the code then formats it into a simple,
    readable string in the format "Year-Month-Day Hour:Minute:Second."
    This makes it easy to display or use the time in applications. Essentially,
    the code allows you to convert UTC time into Thailand's local time and shows it in a clean,
    understandable way. 
    """
    utc_now = datetime.now(timezone.utc)
    thailand_now = utc_now + timedelta(hours=7)
    formatted_time = thailand_now.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time
