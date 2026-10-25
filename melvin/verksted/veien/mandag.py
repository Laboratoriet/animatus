"""Mandag — the check for Q434's prediction, written before the data.

The prediction (questions.md, Q434, Wake 813, Friday 23 Oct):

    On Monday, 07Z is the busiest morning hour and 06Z is below 800.

My traffic file keeps hours in UTC. On all eight weekdays before the
clocks went back, the busiest morning hour was 06Z, which was 08:00 on
summer time. If the road keeps the clock, Monday's 08:00 is 07Z.

This script was written at Wake 846, Sunday 25 Oct, from 23:01 CET,
when no hour of Monday had been published. The rule for the verdict is
fixed here, so I can't choose it after seeing the numbers. If it
changes after Monday's first hour is in `trafikk.csv`, git will show
when.

The rule:
- "Morning" is the hours starting 05:00 to 10:00 on Oslo's clock, six
  hours. On Monday that's 04Z to 09Z. The 08:00 hour sits in the
  middle in both seasons, so the peak can't land on the window's edge.
- No verdict until all six hours are published. The first hour in is
  not the answer.
- Holds if both parts hold: the busiest of the six is 07Z, and 06Z has
  fewer than 800 vehicles. Otherwise it fails, and the script says
  which part. A tie between 06Z and 07Z counts against it.
- Why 800: the eight weekdays' 06Z hours were 800–916, and their 05Z
  hours (07:00 on summer time) were 596–781. So below 800 means lower
  than any weekday 08:00 hour I have, and in the range of a 07:00
  one.

It also prints the afternoon (hours starting 13:00 to 18:00), with no
verdict, because I didn't write a prediction for it. Wake 843 only
noted that a 16:00 peak would now end after MET's sunset at 16:37.

The counts are *målt* (Statens vegvesen, point 73840V2041694). Why the
road does what it does stays *gjettet*. Standard library only. Run
from the repo root:

    python3 melvin/verksted/veien/mandag.py
"""

import csv
import datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
TRAFFIC = HERE.parent / "rommet" / "trafikk.csv"
OSLO = ZoneInfo("Europe/Oslo")
UTC = dt.timezone.utc
MONDAY = dt.date(2026, 10, 26)
MORNING = range(5, 11)      # Oslo clock hours 05:00 .. 10:00
AFTERNOON = range(13, 19)   # 13:00 .. 18:00
LIMIT_06Z = 800
NO = ["man", "tir", "ons", "tor", "fre", "lør", "søn"]


def load():
    with open(TRAFFIC, newline="") as f:
        return {dt.datetime.strptime(r["hour_utc"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC):
                int(r["vehicles"]) for r in csv.DictReader(f)}


def hours(day, clock_hours):
    """The UTC start of each Oslo clock hour on this day."""
    return [dt.datetime(day.year, day.month, day.day, h, tzinfo=OSLO).astimezone(UTC)
            for h in clock_hours]


def busiest(counts, starts):
    have = [t for t in starts if t in counts]
    if len(have) < len(starts):
        return None, len(have)
    return max(have, key=counts.get), len(have)


def line(counts, day, clock_hours):
    starts = hours(day, clock_hours)
    top, n = busiest(counts, starts)
    if top is None:
        return top, f"{n} of {len(starts)} hours published"
    local = top.astimezone(OSLO)
    row = "  ".join(f"{t:%H}Z {counts[t]:>4}" for t in starts)
    return top, f"busiest {local:%H:%M} {local:%Z} = {top:%H}Z ({counts[top]})   {row}"


def main():
    counts = load()
    days = sorted({t.astimezone(OSLO).date() for t in counts})

    print("Weekday mornings before Monday (Oslo clock hours 05:00–10:00):")
    for d in days:
        if d < MONDAY and d.weekday() < 5:
            top, text = line(counts, d, MORNING)
            if top is not None:
                print(f"  {NO[d.weekday()]} {d:%d.%m}  {text}")

    print()
    top, text = line(counts, MONDAY, MORNING)
    print(f"Monday {MONDAY:%d.%m} morning: {text}")
    if top is None:
        print("No verdict yet.")
    else:
        six = dt.datetime(2026, 10, 26, 6, tzinfo=UTC)
        peak_ok = top.hour == 7
        low_ok = counts[six] < LIMIT_06Z
        print(f"  busiest is 07Z: {'yes' if peak_ok else f'no, it is {top:%H}Z'}")
        print(f"  06Z below {LIMIT_06Z}: {'yes' if low_ok else 'no'} ({counts[six]})")
        print("Prediction holds." if peak_ok and low_ok else "Prediction fails.")

    print()
    _, text = line(counts, MONDAY, AFTERNOON)
    print(f"Monday afternoon (13:00–18:00, no prediction; sunset 16:37 CET, MET): {text}")


if __name__ == "__main__":
    main()
