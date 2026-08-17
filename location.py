"""
===========================================================
LOCATION MODULE
Detects the user's approximate location using their IP
address. Falls back to a fixed default location if the
network request fails (no internet, firewall, etc.)
===========================================================
"""

import requests

# Fallback location used if IP-based lookup fails
DEFAULT_LOCATION = {
    "city": "Chennai",
    "latitude": 13.0827,
    "longitude": 80.2707,
}


def get_location():
    """
    Returns a dict with keys: city, latitude, longitude.
    Uses ipinfo.io for a free, no-API-key IP-based lookup.
    """
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        response.raise_for_status()
        data = response.json()

        loc = data.get("loc")  # "lat,lon" as a string
        if not loc:
            return DEFAULT_LOCATION

        lat_str, lon_str = loc.split(",")

        return {
            "city": data.get("city", "Unknown"),
            "latitude": float(lat_str),
            "longitude": float(lon_str),
        }

    except Exception:
        # No internet, request timeout, bad response, etc.
        return DEFAULT_LOCATION
