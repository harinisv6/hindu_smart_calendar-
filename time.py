"""
===========================================================
HINDU SMART CLOCK
Author : Harini
Version : 2.0 (Widget)
===========================================================
"""

from tkinter import *
from tkinter import Toplevel
from datetime import datetime

from modules.location import get_location
from modules.sunrise import get_sun_times
from modules.brahma import get_brahma_muhurta
from modules.rahu import get_rahu_kalam
from modules.yamakanda import get_yamaganda
from modules.gulikai import get_gulikai
from modules.nalla_neram import get_nalla_neram
from modules.utils import (
    current_event,
    next_event,
    format_time,
)

# ----------------------------------------
# Window
# ----------------------------------------

root = Tk()
root.geometry("350x260")
root.resizable(False, False)
root.configure(bg="#1E1E1E")

# Uncomment if you want it always on top
# root.attributes("-topmost", True)

# ----------------------------------------
# Colors
# ----------------------------------------

BG = "#1E1E1E"
FG = "white"

status_colors = {
    "Nalla Neram": "#2ECC71",
    "Rahu Kalam": "#E74C3C",
    "Yamaganda": "#F39C12",
    "Gulikai": "#9B59B6",
    "Brahma Muhurta": "#3498DB",
    "No Event": "#95A5A6",
}

# ----------------------------------------
# Load Location and Sun Times (Only Once)
# ----------------------------------------

location = get_location()

sunrise, sunset = get_sun_times(
    location["latitude"],
    location["longitude"]
)



# ----------------------------------------
# Widgets
# ----------------------------------------


time_lbl = Label(
    root,
    bg=BG,
    fg="white",
    font=("Consolas", 26, "bold")
)
time_lbl.pack()

date_lbl = Label(
    root,
    bg=BG,
    fg="lightgray",
    font=("Arial", 10)
)
date_lbl.pack(pady=(0, 10))

Label(
    root,
    text="Current",
    bg=BG,
    fg="white",
    font=("Arial", 10, "bold")
).pack()

current_lbl = Label(
    root,
    bg=BG,
    fg="green",
    font=("Arial", 14, "bold")
)
current_lbl.pack()

end_lbl = Label(
    root,
    bg=BG,
    fg="lightgray",
    font=("Arial", 10)
)
end_lbl.pack(pady=(0, 12))

Label(
    root,
    text="Next",
    bg=BG,
    fg="white",
    font=("Arial", 10, "bold")
).pack()

next_lbl = Label(
    root,
    bg=BG,
    fg="orange",
    font=("Arial", 14, "bold")
)
next_lbl.pack()

start_lbl = Label(
    root,
    bg=BG,
    fg="lightgray",
    font=("Arial", 10)
)
start_lbl.pack()

# ----------------------------------------
# Update Function
# ----------------------------------------

def update_clock():

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

    time_lbl.config(text=now.strftime("%I:%M:%S %p"))
    date_lbl.config(text=now.strftime("%A, %d %b %Y"))

    current_lbl.config(
        text=current["name"],
        fg=status_colors.get(current["name"], "white")
    )

    end_lbl.config(
        text=f"Ends : {format_time(current['end'])}"
    )

    next_lbl.config(
        text=upcoming["name"],
        fg=status_colors.get(upcoming["name"], "white")
    )

    start_lbl.config(
        text=f"Starts : {format_time(upcoming['start'])}"
    )

    root.after(1000, update_clock)

# ----------------------------------------
# ----------------------------------------
# Today's Timings Window
# ----------------------------------------

def show_schedule():

    now = datetime.now()

    events = [
        get_brahma_muhurta(sunrise),
        get_nalla_neram(now, sunrise, sunset),
        get_yamaganda(now, sunrise, sunset),
        get_rahu_kalam(now, sunrise, sunset),
        get_gulikai(now, sunrise, sunset)
    ]

    win = Toplevel(root)
    win.title("Today's Timings")
    win.geometry("380x350")
    win.configure(bg="#1E1E1E")
    win.resizable(False, False)

    Label(
        win,
        text="🕉 Today's Timings",
        bg="#1E1E1E",
        fg="gold",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    for item in sorted(events, key=lambda x: x["start"]):

        color = status_colors.get(item["name"], "white")

        frame = Frame(
            win,
            bg="#2B2B2B",
            padx=10,
            pady=8
        )
        frame.pack(fill="x", padx=12, pady=5)

        Label(
            frame,
            text=item["name"],
            bg="#2B2B2B",
            fg=color,
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        Label(
            frame,
            text=f"{format_time(item['start'])}  →  {format_time(item['end'])}",
            bg="#2B2B2B",
            fg="white",
            font=("Arial", 10)
        ).pack(anchor="w")

Button(
    root,
    text="📅 Today's Timings",
    command=show_schedule,
    bg="#F39C12",
    fg="white",
    font=("Arial", 11, "bold"),
    relief=FLAT,
    padx=15,
    pady=5,
    cursor="hand2"
).pack(pady=15)


update_clock()

root.mainloop()


# ----------------------------------------
# Today's Schedule Window
# ----------------------------------------

def show_schedule():

    now = datetime.now()

    events = [
        get_brahma_muhurta(sunrise),
        get_nalla_neram(now, sunrise, sunset),
        get_rahu_kalam(now, sunrise, sunset),
        get_yamaganda(now, sunrise, sunset),
        get_gulikai(now, sunrise, sunset)
    ]

    schedule = Toplevel(root)
    schedule.title("Today's Timings")
    schedule.geometry("380x340")
    schedule.configure(bg="#1E1E1E")
    schedule.resizable(False, False)

    Label(
        schedule,
        text="🕉 Today's Schedule",
        font=("Arial", 16, "bold"),
        fg="gold",
        bg="#1E1E1E"
    ).pack(pady=12)

    for event in sorted(events, key=lambda x: x["start"]):

        color = status_colors.get(event["name"], "white")

        Frame(schedule, bg="#3A3A3A", height=1).pack(fill="x", padx=10, pady=3)

        Label(
            schedule,
            text=event["name"],
            font=("Arial", 12, "bold"),
            fg=color,
            bg="#1E1E1E"
        ).pack()

        Label(
            schedule,
            text=f"{format_time(event['start'])} → {format_time(event['end'])}",
            font=("Arial", 10),
            fg="white",
            bg="#1E1E1E"
        ).pack(pady=(0, 5))



# ----------------------------------------
# Start App
# ----------------------------------------

update_clock()

root.mainloop()
