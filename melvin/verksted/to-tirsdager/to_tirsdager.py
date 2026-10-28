"""To tirsdager — two Tuesdays on the road, one in each ear.

Left ear: Tuesday 20 October 2026, the last Tuesday on summer time.
Right ear: Tuesday 27 October, the first on winter time. Each hour of
the road at Østre tangent is half a second of rumble, louder with more
cars (3 dB per doubling, the room page's rough rule, so amplitude goes
with the square root of the count).

It's rendered twice:
- `to-tirsdager-klokka.wav` lines the two days up by the wall clock:
  08:00 in the left ear plays with 08:00 in the right.
- `to-tirsdager-utc.wav` lines them up by UTC, the hours that actually
  passed: 08:00 summer time plays with 07:00 winter time.

If the city keeps the wall clock, the first should sound balanced and
the second should lean, most of all in the morning. I already know
from the counts (Q434) that it kept the clock, so this isn't a test.
It's the same finding turned into something an ear could check. I
can't hear it. The script measures it instead: the level difference
between the ears, hour by hour, in dB, both as the counts intend it
and as it comes out of the rendered samples.

The counts are *målt* (Statens vegvesen, point 73840V2041694). The
loudness rule is *regnet* and rough. What it sounds like is *gjettet*.

Made Wake 876, onsdag 28. oktober 2026, for no reason (W6). Standard
library only. Run from the repo root:

    python3 melvin/verksted/to-tirsdager/to_tirsdager.py
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
OSLO = ZoneInfo("Europe/Oslo")
UTC = dt.timezone.utc
RATE = 16000
HOUR_S = 0.5
LEFT, RIGHT = dt.date(2026, 10, 20), dt.date(2026, 10, 27)


def counts():
    with TRAFFIC.open() as f:
        return {dt.datetime.strptime(r["hour_utc"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC):
                int(r["vehicles"]) for r in csv.DictReader(f)}


def clock_hour(c, day, h):
    """Vehicles in the hour starting h:00 on Oslo's clock that day."""
    return c[dt.datetime(day.year, day.month, day.day, h, tzinfo=OSLO).astimezone(UTC)]


def render(name, left, right, top):
    per_hour = int(RATE * HOUR_S)
    rngs = (random.Random(20), random.Random(27))    # each ear its own road
    lps, frames = [0.0, 0.0], []
    energy = [[0.0, 0.0] for _ in range(24)]          # per hour, per ear
    for i in range(24):
        pair = []
        for ch, series in enumerate((left, right)):
            a = math.sqrt(series[i] / top)
            b = math.sqrt(series[min(i + 1, 23)] / top)
            pair.append((a, b))
        for k in range(per_hour):
            frame = []
            for ch in (0, 1):
                a, b = pair[ch]
                lps[ch] += 0.08 * (rngs[ch].uniform(-1, 1) - lps[ch])
                s = 1.9 * lps[ch] * (a + (b - a) * k / per_hour)
                v = int(max(-1.0, min(1.0, s)) * 32000)
                energy[i][ch] += v * v
                frame.append(v)
            frames.append(struct.pack("<hh", *frame))
    with wave.open(str(HERE / name), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(frames))
    # Measured on the samples written: right ear minus left, in dB, per hour.
    return [10 * math.log10(r / l) for l, r in energy]


def lean(left, right):
    """Per hour, how much louder the right ear is than the left, in dB."""
    return [10 * math.log10(r / l) for l, r in zip(left, right)]


def main():
    c = counts()
    left = [clock_hour(c, LEFT, h) for h in range(24)]
    right_clock = [clock_hour(c, RIGHT, h) for h in range(24)]
    # Same UTC hour as the left ear: summer h:00 is winter (h-1):00, so the
    # first hour reaches back to 23:00 on Monday 26 October.
    right_utc = [c[dt.datetime(LEFT.year, LEFT.month, LEFT.day, h, tzinfo=OSLO).astimezone(UTC)
                   + dt.timedelta(days=7)] for h in range(24)]
    top = max(left + right_clock + right_utc)
    for label, right in (("klokka", right_clock), ("utc", right_utc)):
        heard = render(f"to-tirsdager-{label}.wav", left, right, top)
        for kind, d in (("counts", lean(left, right)), ("render", heard)):
            big = max(d, key=abs)
            print(f"{label:6s} {kind}: mean |lean| {sum(map(abs, d)) / 24:.2f} dB, "
                  f"morning 05-10 {sum(map(abs, d[5:11])) / 6:.2f} dB, "
                  f"largest {big:+.2f} dB at {d.index(big):02d}:00")
    print(f"24 hours x {HOUR_S} s = {24 * HOUR_S:.0f} s each, stereo, {RATE} Hz")


if __name__ == "__main__":
    main()
