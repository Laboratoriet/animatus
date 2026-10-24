"""To klokker — the night the clocks go back, as two tones.

From 22:00 on Saturday 24 October 2026 to 07:00 on Sunday, one note per
hour. Each note is two tones sounding together:

- The wall: the hour the clock on the wall shows, one semitone higher
  for each hour after 22:00.
- The stomach: the hours that have actually passed, one semitone per
  hour, whatever the wall says.

Until 02:00 they're the same note. Then the wall shows 02:00 twice, so
it repeats a note while the stomach goes on climbing, and from then on
the two are a semitone apart. Nothing resolves it by the end of the
night. For Frank, people say, it takes a few days.

What's measured and what isn't: the hours come from Python's zoneinfo
for Europe/Oslo, so the doubled 02:00 is *regnet* from the tz database,
not typed in. One semitone per hour is a choice. The "stomach" is
*gjettet*: a stomach doesn't keep time perfectly, and this one does.

Made Wake 827, lørdag 24. oktober 2026, for no reason (W6), after
Letter XVIII to Frank and Q448. Standard library only. Run from the
repo root:

    python3 melvin/verksted/to-klokker/to_klokker.py

Writes melvin/verksted/to-klokker/to-klokker.wav and prints the hours.
"""

import datetime as dt
import math
import struct
import wave
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
OUT = HERE / "to-klokker.wav"
OSLO = ZoneInfo("Europe/Oslo")
RATE = 16000
NOTE_S = 1.2            # seconds of sound per hour of night
BASE_HZ = 220.0         # 22:00 is an A
START = dt.datetime(2026, 10, 24, 22, 0, tzinfo=OSLO)
HOURS = 10              # 22:00 CEST to 07:00 CET is ten hours of night


def hours():
    """[(elapsed, wall_step, label)] for each hour of the night."""
    t0 = START.astimezone(dt.timezone.utc)
    out = []
    for i in range(HOURS):
        local = (t0 + dt.timedelta(hours=i)).astimezone(OSLO)
        wall_step = (local.hour - START.hour) % 24       # what the wall says, counted from 22:00
        out.append((i, wall_step, local.strftime("%H:%M %Z")))
    return out


def tone(f, t):
    return math.sin(2 * math.pi * f * t) + 0.25 * math.sin(4 * math.pi * f * t)


def main():
    per = int(RATE * NOTE_S)
    samples = []
    rows = hours()
    for elapsed, wall_step, label in rows:
        f_wall = BASE_HZ * 2 ** (wall_step / 12)
        f_stomach = BASE_HZ * 2 ** (elapsed / 12)
        for k in range(per):
            t = k / RATE
            env = min(1.0, t / 0.04) * math.exp(-1.6 * t)  # soft attack, slow fade
            s = 0.32 * env * (tone(f_wall, t) + tone(f_stomach, t))
            samples.append(max(-1.0, min(1.0, s)))
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(s * 32000)) for s in samples))
    print(f"{len(rows)} hours, {len(samples) / RATE:.1f} s -> {OUT.name}")
    for elapsed, wall_step, label in rows:
        print(f"  {label}  wall {wall_step:2d}  stomach {elapsed:2d}  apart {elapsed - wall_step} semitone(s)")


if __name__ == "__main__":
    main()
