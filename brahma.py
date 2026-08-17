"""
===========================================================
BRAHMA MUHURTA MODULE
Brahma Muhurta is the auspicious period before sunrise,
traditionally lasting 48 minutes and ending 1 hour 36
minutes before sunrise... it actually STARTS 1h36m before
sunrise and lasts 48 minutes (i.e. it ends 48 minutes
before sunrise).
===========================================================
"""

from datetime import timedelta


def get_brahma_muhurta(sunrise):
    """
    Returns a dict describing today's Brahma Muhurta window.
    """
    start = sunrise - timedelta(minutes=96)  # 1 hour 36 minutes before sunrise
    end = sunrise - timedelta(minutes=48)    # 48 minutes before sunrise

    return {
        "name": "Brahma Muhurta",
        "start": start,
        "end": end,
    }
