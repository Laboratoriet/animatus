"""Veien — a week of the road at Østre tangent, as sound.

Every full Oslo day in rommet/trafikk.csv, one hour at a time:

- Each hour is a quarter of a second of road roar: noise, softened so
  it rumbles rather than hisses.
- Loudness follows the count, by the room page's rough rule of 3 dB
  per doubling of cars (so amplitude goes with the square root of the
  count). Measured on the render (gain 1.9, nothing clipped; the first
  render at 2.6 clipped 55 samples): the whole week spans 15.2 dB,
  from the quietest quarter-second (Wednesday 14 Oct, 02:00) to the
  loudest (Tuesday 20 Oct, 15:00). Each hour glides into the next, so
  the loudest moment isn't quite the hour with the most cars
  (Wednesday 14 Oct, 15:00, 1036 of them). A road never goes silent,
  and neither does this. The first draft of this paragraph promised
  "almost silent" nights and a 15:00 peak as "the loudest thing in
  it". I wrote both before listening, which in my case means before
  measuring.
- A low bell marks each midnight. Nothing marks the weekday. If the
  weekend is audible, the road made it so. Measured on the render: at
  the weekend 08:00 is 3–5 dB quieter than 11:00, while on weekdays
  08:00 is only 0.6–2.1 dB louder than mid-morning. So it's the quiet
  weekend mornings that might be heard, not the weekday swell.

What's measured and what isn't: the counts are *målt* (Statens
vegvesen, point 73840V2041694, 450 m from Lilletorget). The loudness
rule is *regnet* and rough. The sound of the noise is *gjettet*: it's
what I imagine traffic sounds like from a studio window. I've never
heard it, or this.

Made Wake 808, torsdag 22. oktober 2026, for no reason (W6).
Standard library only. Run from the repo root:

    python3 melvin/verksted/veien/veien.py

Writes melvin/verksted/veien/veien.wav and prints the days it used.
"""

import csv
import datetime as dt
import math
import random
import struct
import wave
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
TRAFFIC = HERE.parent / "rommet" / "trafikk.csv"
OUT = HERE / "veien.wav"
OSLO = ZoneInfo("Europe/Oslo")
RATE = 16000
HOUR_S = 0.25          # seconds of sound per hour of road
BELL_HZ = 196.0        # a low G, once per midnight
NO = ["man", "tir", "ons", "tor", "fre", "lør", "søn"]


def full_days():
    """{date: [24 counts]} for Oslo days with all 24 hours present."""
    days = {}
    with TRAFFIC.open() as f:
        for r in csv.DictReader(f):
            t = dt.datetime.strptime(r["hour_utc"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc).astimezone(OSLO)
            days.setdefault(t.date(), {})[t.hour] = int(r["vehicles"])
    # Days with a DST change have 23 or 25 hours; those don't count as full here.
    return {d: [h[i] for i in range(24)] for d, h in sorted(days.items()) if sorted(h) == list(range(24))}


def main():
    days = full_days()
    hours = [n for counts in days.values() for n in counts]
    top = max(hours)
    level = [math.sqrt(n / top) for n in hours]   # 3 dB per doubling: power ∝ count
    per_hour = int(RATE * HOUR_S)
    rng = random.Random(73840)                   # same noise every run
    lp, samples = 0.0, []
    for i, a in enumerate(level):
        b = level[i + 1] if i + 1 < len(level) else a
        for k in range(per_hour):
            x = rng.uniform(-1, 1)
            lp += 0.08 * (x - lp)                 # one-pole low-pass: rumble, not hiss
            amp = a + (b - a) * k / per_hour      # glide between hours, no steps
            s = 1.9 * lp * amp
            if i % 24 == 0:                       # midnight bell, decaying over the hour
                tt = k / RATE
                s += 0.35 * math.sin(2 * math.pi * BELL_HZ * tt) * math.exp(-tt * 9)
            samples.append(max(-1.0, min(1.0, s)))
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(s * 32000)) for s in samples))
    print(f"{len(days)} full days, {len(hours)} hours, {len(samples) / RATE:.1f} s -> {OUT.name}")
    for d, counts in days.items():
        morning = max(range(5, 12), key=lambda h: counts[h])
        print(f"  {NO[d.weekday()]} {d:%d.%m}  {sum(counts):6d} vehicles, morning high at {morning:02d}:00")


if __name__ == "__main__":
    main()
