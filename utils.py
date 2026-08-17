"""
===========================================================
UTILS MODULE
Shared helper functions used across the app:
- format_time: pretty-print a datetime as 12-hour time
- current_event: find which event window "now" falls in
- next_event: find the next upcoming event
- clear_screen: clear the terminal (cross-platform)
===========================================================
"""

import os
from datetime import timedelta


def format_time(dt):
    """
    Formats a datetime as e.g. '05:42:10 AM'.
    """
    return dt.strftime("%I:%M:%S %p")


def current_event(now, events):
    """
    Returns the event dict whose start/end window contains
    'now'. If none match, returns a placeholder "Normal Time"
    event ending at the next event's start.
    """
    for event in events:
        if event["start"] <= now <= event["end"]:
            remaining = event["end"] - now
            event_copy = dict(event)
            event_copy["remaining"] = _format_timedelta(remaining)
            return event_copy

    # Not inside any special period right now
    upcoming = next_event(now, events)
    remaining = upcoming["start"] - now

    return {
        "name": "Normal Time",
        "start": now,
        "end": upcoming["start"],
        "remaining": _format_timedelta(remaining),
    }


def next_event(now, events):
    """
    Returns the next event (by start time) that hasn't
    started yet. If all events for today have passed,
    returns the earliest event (assumed to repeat tomorrow).
    """
    future_events = [e for e in events if e["start"] > now]

    if future_events:
        return min(future_events, key=lambda e: e["start"])

    # Everything today has passed; just show the earliest one
    return min(events, key=lambda e: e["start"])


def _format_timedelta(td):
    """
    Formats a timedelta as 'Hh Mm Ss', hiding zero components.
    """
    total_seconds = int(td.total_seconds())
    if total_seconds < 0:
        total_seconds = 0

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")

    return " ".join(parts)


def clear_screen():
    """
    Clears the terminal on both Windows and Unix-like systems.
    """
    os.system("cls" if os.name == "nt" else "clear")
