"""
===========================================================
YAMAGANDA MODULE
Another inauspicious ~90-minute daily period, calculated
the same way as Rahu Kalam but with a different segment
assigned to each weekday.
===========================================================
"""

# datetime.weekday(): Monday=0, Tuesday=1, ..., Sunday=6
YAMA_SEGMENT_BY_WEEKDAY = {
    0: 3,  # Monday    -> 4th part
    1: 2,  # Tuesday   -> 3rd part
    2: 1,  # Wednesday -> 2nd part
    3: 0,  # Thursday  -> 1st part
    4: 6,  # Friday    -> 7th part
    5: 5,  # Saturday  -> 6th part
    6: 4,  # Sunday    -> 5th part
}


def get_yamaganda(now, sunrise, sunset):
    """
    Returns a dict describing today's Yamaganda window.
    """
    day_length = sunset - sunrise
    part_length = day_length / 8

    segment_index = YAMA_SEGMENT_BY_WEEKDAY[now.weekday()]

    start = sunrise + part_length * segment_index
    end = start + part_length

    return {
        "name": "Yamaganda",
        "start": start,
        "end": end,
    }