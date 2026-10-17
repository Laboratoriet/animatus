"""Klokka: where I am in calendar time.

I'm good at sky time (sun, moon, day length) and keep slipping on
calendar time: wrong weekdays, miscounted wakes. This is the instrument
for the second kind. Run it at the start of a wake:

    python3 melvin/verksted/klokka/klokka.py

It prints the Oslo date and weekday, my wake number, how many wakes
today, my day count and Season 3 day, whether it's working hours, and
days left to every deadline in melvin/projects/frister.md.

Conventions, taken from the logs so the numbers match them:
- Day N = days since Wake 1 (8 August 2026). 12 October was Day 65.
- Season 3 started 12 October, which was its Day 1.
- This wake = highest wake-log number + 1, because the log for the
  current wake is written last.

Made Wake 768, 14 October 2026. Standard library only.
"""

import datetime as dt
import re
from pathlib import Path
from zoneinfo import ZoneInfo

OSLO = ZoneInfo("Europe/Oslo")
ROOT = Path(__file__).resolve().parent.parent.parent      # melvin/
WAKE_LOG = ROOT / "wake-log"
FRISTER = ROOT / "projects" / "frister.md"
FIRST_WAKE = dt.date(2026, 8, 8)
SEASON3 = dt.date(2026, 10, 12)
NO = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]
EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
HEADER = re.compile(r"^# Wake (\d+) — (\d{4}-\d{2}-\d{2})", re.M)


def wakes():
    """{wake number: date} from the wake-log headers."""
    out = {}
    for f in WAKE_LOG.glob("wake-*.md"):
        m = HEADER.search(f.read_text(errors="replace")[:200])
        if m:
            out[int(m.group(1))] = dt.date.fromisoformat(m.group(2))
    return out


def deadlines():
    line = re.compile(r"^- (\d{4}-\d{2}-\d{2})(?: (\d{2}:\d{2}))? — (.+)$", re.M)
    if not FRISTER.exists():
        return []
    return [(dt.date.fromisoformat(d), t, what) for d, t, what in line.findall(FRISTER.read_text())]


def main():
    now = dt.datetime.now(OSLO)
    today = now.date()
    w = wakes()
    this = max(w) + 1 if w else 1
    today_count = sum(1 for d in w.values() if d == today) + 1
    work = today.weekday() < 5 and 8 <= now.hour < 16

    print(f"{NO[today.weekday()]} {today:%d.%m.%Y}, {now:%H:%M} Oslo ({EN[today.weekday()]})")
    print(f"Wake {this}, number {today_count} today. Day {(today - FIRST_WAKE).days}. "
          f"Season 3, day {(today - SEASON3).days + 1}.")
    print("Working hours (weekday 08–16): " + ("yes" if work else "no") + ".")
    # Past deadlines stay in frister.md as history but stop crowding the clock after two days (Wake 800).
    upcoming = [x for x in sorted(deadlines()) if (x[0] - today).days >= -2]
    if upcoming:
        print("Deadlines:")
    for d, t, what in upcoming:
        left = (d - today).days
        when = ("today" if left == 0 else "tomorrow" if left == 1 else "yesterday" if left == -1
                else f"in {left} days" if left > 0 else f"{-left} days ago")
        print(f"  {NO[d.weekday()]:>7} {d:%d.%m}{' ' + t if t else '':6}  {when:>12}  {what}")


if __name__ == "__main__":
    main()
