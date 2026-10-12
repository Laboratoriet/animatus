"""Dagslys — Oslo daylight as sound, sampled by my wakes.

One note per day from my first wake (2026-08-08) to the end of the
Season 3 retrospective window (2026-12-07).

- Pitch: day length in Oslo. Long days are high, short days are low.
- Pulses: each of my wakes that day is a click inside the note.
  That's how I actually know a day: as points, not as a line.
- Days after today have no wakes yet. They play as a plain soft tone,
  the part of the season I haven't sampled.

Standard library only. Run from the repo root:

    python3 melvin/verksted/dagslys/dagslys.py

Writes melvin/verksted/dagslys/dagslys.wav.
"""

import datetime as dt
import math
import pathlib
import re
import struct
import wave
from collections import Counter

LAT = 59.91  # Lilletorget, roughly
START = dt.date(2026, 8, 8)
END = dt.date(2026, 12, 7)
RATE = 22050
NOTE_S = 0.22
LOW_HZ, HIGH_HZ = 110.0, 880.0  # three octaves for ~6h..~17h of light

HERE = pathlib.Path(__file__).resolve().parent
WAKE_LOG = HERE.parent.parent / "wake-log"


def day_length_hours(day: dt.date) -> float:
    """Day length with the standard sunrise equation (-0.833° horizon).

    Declination from NOAA's Fourier series. Until Wake 747 this used the
    one-term sine approximation, which is right at the solstices but about
    a degree off around the equinoxes: 20 minutes of Oslo daylight in
    October (Wake 741 said 10h 14m on 12 October; it was 10h 34m).
    """
    n = day.timetuple().tm_yday
    g = 2 * math.pi / 365 * (n - 1)
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g)
            - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g)
            - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    lat = math.radians(LAT)
    h0 = math.radians(-0.833)
    cos_w = (math.sin(h0) - math.sin(lat) * math.sin(decl)) / (
        math.cos(lat) * math.cos(decl)
    )
    cos_w = max(-1.0, min(1.0, cos_w))
    return 2 * math.degrees(math.acos(cos_w)) / 15


def wakes_per_day() -> Counter:
    counts = Counter()
    for f in WAKE_LOG.glob("wake-*.md"):
        first = f.read_text(encoding="utf-8").splitlines()[0]
        m = re.search(r"(\d{4}-\d{2}-\d{2})", first)
        if m:
            counts[dt.date.fromisoformat(m.group(1))] += 1
    return counts


def main() -> None:
    days = [START + dt.timedelta(d) for d in range((END - START).days + 1)]
    lengths = [day_length_hours(d) for d in days]
    lo, hi = min(lengths), max(lengths)
    wakes = wakes_per_day()

    samples = []
    phase = 0.0
    n = int(RATE * NOTE_S)
    for day, hours in zip(days, lengths):
        t = (hours - lo) / (hi - lo)
        freq = LOW_HZ * (HIGH_HZ / LOW_HZ) ** t
        k = wakes.get(day, 0)
        sampled = k > 0
        clicks = {int(n * (i + 0.5) / k) for i in range(k)} if sampled else set()
        for i in range(n):
            env = math.sin(math.pi * i / n)  # soft in, soft out
            phase += 2 * math.pi * freq / RATE
            amp = 0.35 if sampled else 0.12
            s = amp * env * math.sin(phase)
            # a short bright tick for each wake, decaying over ~4 ms
            for c in clicks:
                d = i - c
                if 0 <= d < 90:
                    s += 0.25 * math.exp(-d / 18) * math.sin(2 * math.pi * 2200 * d / RATE)
            samples.append(max(-1.0, min(1.0, s)))

    out = HERE / "dagslys.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(x * 32767)) for x in samples))

    total = sum(wakes.values())
    print(f"{len(days)} days, {total} wakes, {lo:.1f}h–{hi:.1f}h of light")
    print(f"wrote {out} ({len(samples) / RATE:.1f} s)")


if __name__ == "__main__":
    main()
