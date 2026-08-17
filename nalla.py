"""
===========================================================
NALLA NERAM MODULE
"Nalla Neram" (good time) traditionally depends on many
factors (nakshatra, tithi, moon position, etc.) that require
a full panchangam engine to calculate precisely.

This is a SIMPLIFIED approximation: it treats any daytime
window that does NOT fall inside Rahu Kalam, Yamaganda, or
Gulika Kalam as a "good time", and returns the single
largest such free window for today.

For precise, tradition-accurate Nalla Neram timings, please
cross-check with a proper printed panchangam or a dedicated
astrology service.
===========================================================
"""

from .rahu import get_rahu_kalam
from .yamakanda import get_yamaganda
from .gulikai import get_gulikai


def get_nalla_neram(now, sunrise, sunset):
    """
    Returns a dict describing the largest "good time" window
    today, avoiding Rahu Kalam, Yamaganda, and Gulika Kalam.
    """
    bad_periods = [
        get_rahu_kalam(now, sunrise, sunset),
        get_yamaganda(now, sunrise, sunset),
        get_gulikai(now, sunrise, sunset),
    ]

    # Sort bad periods by start time
    bad_periods.sort(key=lambda p: p["start"])

    # Build the list of free gaps between sunrise, the bad
    # periods, and sunset
    boundaries = [sunrise]
    for p in bad_periods:
        boundaries.append(p["start"])
        boundaries.append(p["end"])
    boundaries.append(sunset)

    # Pair them up into candidate windows and pick the widest one
    candidates = []
    for i in range(0, len(boundaries) - 1, 2):
        start = boundaries[i]
        end = boundaries[i + 1]
        if end > start:
            candidates.append((start, end))

    if not candidates:
        # Fallback: whole day, shouldn't normally happen
        best_start, best_end = sunrise, sunset
    else:
        best_start, best_end = max(candidates, key=lambda w: w[1] - w[0])

    return {
        "name": "Nalla Neram",
        "start": best_start,
        "end": best_end,
    }
