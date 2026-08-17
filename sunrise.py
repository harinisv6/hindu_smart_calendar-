"""
===========================================================
SUNRISE MODULE
Calculates today's sunrise and sunset times for a given
latitude/longitude using the 'astral' library.
===========================================================
"""

from datetime import datetime, timezone
from astral import Observer
from astral.sun import sun


def get_sun_times(latitude, longitude):
    """
    Returns (sunrise, sunset) as naive LOCAL datetime objects
    for today's date at the given coordinates.
    """
    observer = Observer(latitude=latitude, longitude=longitude)

    s = sun(observer, date=datetime.now(timezone.utc).date())

    # astral returns UTC-aware datetimes; convert to local system time
    sunrise = s["sunrise"].astimezone().replace(tzinfo=None)
    sunset = s["sunset"].astimezone().replace(tzinfo=None)

    return sunrise, sunset
