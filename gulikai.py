"""
===========================================================
GULIKA KALAM MODULE
A third inauspicious ~90-minute daily period, calculated
the same way as Rahu Kalam and Yamaganda, with its own
segment assigned to each weekday.
===========================================================
"""

# datetime.weekday(): Monday=0, Tuesday=1, ..., Sunday=6
GULIKA_SEGMENT_BY_WEEKDAY = {
    0: 5,  # Monday    -> 6th part
    1: 4,  # Tuesday   -> 5th part
    2: 3,  # Wednesday -> 4th part
    3: 2,  # Thursday  -> 3rd part
    4: 1,  # Friday    -> 2nd part
    5: 0,  # Saturday  -> 1st part
    6: 6,  # Sunday    -> 7th part
}


def get_gulikai(now, sunrise, sunset):
    """
    Returns a dict describing today's Gulika Kalam window.
    """
    day_length = sunset - sunrise
    part_length = day_length / 8

    segment_index = GULIKA_SEGMENT_BY_WEEKDAY[now.weekday()]

    start = sunrise + part_length * segment_index
    end = start + part_length

    return {
        "name": "Gulika Kalam",
        "start": start,
        "end": end,
    }
