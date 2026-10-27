from fastapi import FastAPI
from fastapi.responses import FileResponse

from datetime import datetime
from pathlib import Path

from modules.location import get_location
from modules.sunrise import get_sun_times
from modules.brahma import get_brahma_muhurta
from modules.rahu import get_rahu_kalam
from modules.yamakanda import get_yamaganda
from modules.gulikai import get_gulikai
from modules.nalla_neram import get_nalla_neram
from modules.utils import current_event, next_event, format_time


# =========================================================
# HINDU SMART CLOCK - FASTAPI
# =========================================================

app = FastAPI(
    title="Hindu Smart Clock",
    description="Hindu auspicious and inauspicious timing API",
    version="2.0"
)


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"


# =========================================================
# LOCATION
# =========================================================

location = get_location()

sunrise, sunset = get_sun_times(
    location["latitude"],
    location["longitude"]
)


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/")
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# =========================================================
# CLOCK API
# =========================================================

@app.get("/clock")
def get_clock():

    now = datetime.now()

    events = [
        get_brahma_muhurta(sunrise),
        get_rahu_kalam(now, sunrise, sunset),
        get_yamaganda(now, sunrise, sunset),
        get_gulikai(now, sunrise, sunset),
        get_nalla_neram(now, sunrise, sunset)
    ]

    current = current_event(now, events)
    upcoming = next_event(now, events)

    return {
        "time": now.strftime("%I:%M:%S %p"),
        "date": now.strftime("%A, %d %b %Y"),

        "current": {
            "name": current["name"],
            "end": format_time(current["end"])
        },

        "next": {
            "name": upcoming["name"],
            "start": format_time(upcoming["start"])
        }
    }


# =========================================================
# TODAY'S SCHEDULE API
# =========================================================

@app.get("/schedule")
def get_schedule():

    now = datetime.now()

    events = [
        get_brahma_muhurta(sunrise),
        get_nalla_neram(now, sunrise, sunset),
        get_rahu_kalam(now, sunrise, sunset),
        get_yamaganda(now, sunrise, sunset),
        get_gulikai(now, sunrise, sunset)
    ]

    schedule = []

    for event in sorted(events, key=lambda x: x["start"]):

        schedule.append({
            "name": event["name"],
            "start": format_time(event["start"]),
            "end": format_time(event["end"])
        })

    return {
        "date": now.strftime("%A, %d %b %Y"),
        "events": schedule
    }


# =========================================================
# LOCATION API
# =========================================================

@app.get("/location")
def get_current_location():

    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"]
    }


# =========================================================
# SUNRISE / SUNSET API
# =========================================================

@app.get("/sun")
def get_sunrise_sunset():

    return {
        "sunrise": format_time(sunrise),
        "sunset": format_time(sunset)
    }
