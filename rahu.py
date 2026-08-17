"""
===========================================================
RAHU KALAM MODULE
Rahu Kalam is an inauspicious ~90-minute period each day.
Daytime (sunrise to sunset) is divided into 8 equal parts;
which part is "Rahu Kalam" depends on the day of the week.

Segment index (0-based, out of 8 parts) per weekday:
Monday=0 .. Sunday=6 (Python's datetime.weekday() numbering)
===========================================================
"""

# datetime.weekday(): Monday=0, Tuesday=1, ..., Sunday=6
RAHU_SEGMENT_BY_WEEKDAY = {
    0: 1,  # Monday    -> 2nd part
    1: 6,  # Tuesday   -> 7th part
    2: 4,  # Wednesday -> 5th part
    3: 5,  # Thursday  -> 6th part
    4: 3,  # Friday    -> 4th part
    5: 2,  # Saturday  -> 3rd part
    6: 7,  # Sunday    -> 8th part
}


def get_rahu_kalam(now, sunrise, sunset):
    """
    Returns a dict describing today's Rahu Kalam window.
    """
    day_length = sunset - sunrise
    part_length = day_length / 8

    segment_index = RAHU_SEGMENT_BY_WEEKDAY[now.weekday()]

    start = sunrise + part_length * segment_index
    end = start + part_length

    return {
        "name": "Rahu Kalam",
        "start": start,
        "end": end,
    }
