"""Lastebiler — the same week of the road twice: first as cars, then with the lorries.

`veien` plays the road with every vehicle counted as one car. Wake 885 found the
counter sorts vehicles by length, and Wake 889 found a source for how much louder a
long one is: the UK road-noise method, Calculation of Road Traffic Noise (1988),
Chart 4, whose heavy-vehicle term works out to 1 + 500/V cars per heavy vehicle.
At a guessed 50 km/h that's 11.

This renders Monday 16 to Sunday 22 November 2026, 168 hours, twice, in the same
voice as `veien` (a quarter-second of low-passed noise per hour, a bell at each
midnight):

  1. every vehicle as a car (the old rule)
  2. every vehicle of 5.6 m and over as 11 cars

with two seconds of silence between. Each half is scaled to its own loudest hour,
so what changes is the shape of the week, not the volume. Then it measures both
halves on the render and prints what it finds, so the README can say what's
audible rather than what I expect.

What's measured and what isn't: the counts are *målt* (trafikkdata, point
73840V2041694, rommet/trafikk.csv and trafikk-lang.csv). The factor 11 is
*lest* (CRTN 1988) and *gjettet* (the speed, and 5.6 m standing in for CRTN's
1525 kg). The sound is *gjettet*.

Made Wake 893, torsdag 26. november 2026. Standard library only. From the repo root:

    python3 melvin/verksted/veien/lastebiler.py
"""

import csv
import datetime as dt
import math
import random
import struct
import wave
from pathlib import Path

from veien import BELL_HZ, HOUR_S, OSLO, RATE

HERE = Path(__file__).resolve().parent
ROMMET = HERE.parent / "rommet"
OUT = HERE / "lastebiler.wav"
FIRST_DAY = dt.date(2026, 11, 16)   # a Monday
DAYS = 7
HEAVY_AS_CARS = 1 + 500 / 50        # CRTN 1988 Chart 4, at a guessed 50 km/h
NO = ["man", "tir", "ons", "tor", "fre", "lør", "søn"]


def week():
    """[(oslo_datetime, total, long)] for the 168 hours of the week, in order."""
    def load(name, col):
        with (ROMMET / name).open() as f:
            return {r["hour_utc"]: int(r[col]) for r in csv.DictReader(f)}
    total, long_ = load("trafikk.csv", "vehicles"), load("trafikk-lang.csv", "long_vehicles")
    hours = []
    for h, n in sorted(total.items()):
        t = dt.datetime.strptime(h, "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc).astimezone(OSLO)
        if FIRST_DAY <= t.date() < FIRST_DAY + dt.timedelta(days=DAYS):
            hours.append((t, n, long_[h]))
    assert len(hours) == 24 * DAYS, f"expected {24 * DAYS} hours, got {len(hours)}"
    return hours


def render(levels, rng):
    per_hour = int(RATE * HOUR_S)
    lp, out = 0.0, []
    for i, a in enumerate(levels):
        b = levels[i + 1] if i + 1 < len(levels) else a
        for k in range(per_hour):
            lp += 0.08 * (rng.uniform(-1, 1) - lp)      # one-pole low-pass: rumble, not hiss
            s = 1.9 * lp * (a + (b - a) * k / per_hour)
            if i % 24 == 0:                              # midnight bell
                tt = k / RATE
                s += 0.35 * math.sin(2 * math.pi * BELL_HZ * tt) * math.exp(-tt * 9)
            out.append(max(-1.0, min(1.0, s)))
    return out


def hour_db(samples, i):
    """RMS level of hour i's quarter-second, in dB, skipping its first 0.12 s
    where a midnight bell would sit."""
    per_hour = int(RATE * HOUR_S)
    seg = samples[i * per_hour + int(0.12 * RATE):(i + 1) * per_hour]
    return 10 * math.log10(sum(x * x for x in seg) / len(seg))


def main():
    hours = week()
    cars = [n for _, n, _ in hours]
    weighted = [n - l + HEAVY_AS_CARS * l for _, n, l in hours]
    halves = []
    for counts in (cars, weighted):
        top = max(counts)
        halves.append(render([math.sqrt(c / top) for c in counts], random.Random(73840)))
    gap = [0.0] * (2 * RATE)
    samples = halves[0] + gap + halves[1]
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(s * 32000)) for s in samples))
    clipped = sum(1 for s in samples if abs(s) >= 1.0)
    print(f"{len(samples) / RATE:.1f} s -> {OUT.name}, {clipped} samples clipped")

    # Measured on the render: mean daytime level (07–19) per day, relative to Sunday.
    for name, half in (("as cars", halves[0]), ("with lorries", halves[1])):
        day = [sum(hour_db(half, d * 24 + h) for h in range(7, 19)) / 12 for d in range(DAYS)]
        rel = "  ".join(f"{NO[d]} {day[d] - day[6]:+.1f}" for d in range(DAYS))
        print(f"  {name:13s} daytime dB vs Sunday:  {rel}")


if __name__ == "__main__":
    main()
