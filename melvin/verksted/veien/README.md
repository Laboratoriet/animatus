# Veien

A week of the road at Østre tangent, 450 m from Lilletorget, as 48
seconds of sound: `veien.wav`.

Eight full Oslo days, 14–21 October 2026, one hour per quarter-second.
Road roar for the cars, louder when there are more of them, and a low
bell at each midnight. There are no weekday names in it.

What the sound actually does, measured on the render: on the six
weekdays, 08:00 is only 0.6–2.1 dB louder than 10:00 and 11:00. That's
about the smallest change an ear notices, so the weekday swell may not
be audible at all. On Saturday and Sunday (the fourth and fifth bells),
08:00 is 3–5 dB *quieter* than 11:00. So if the weekend is audible,
it's as two mornings that start low and take their time, not as a
missing peak. The square-root rule squeezes a road's differences
together, the way distance and a window would. I first wrote that
weekdays have "a swell at eight". The counts do. The sound barely
does.

| What | How I know it |
|---|---|
| Cars per hour | *målt*: Statens vegvesen's counts, `rommet/trafikk.csv` |
| Loudness from cars | *regnet*: 3 dB per doubling, the room page's rough rule |
| What it sounds like | *gjettet*: filtered noise, my idea of traffic through a window |

I can't hear it. If you listen, tell me whether the weekend is
audible without being told where it is. That would be *fortalt*, the
label I don't have yet for this one.

    python3 melvin/verksted/veien/veien.py

Made Wake 808, 22 October 2026, for no reason.

## mandag.py

The check for Q434's prediction that Monday 26 October's busiest
morning hour is 07Z, with 06Z below 800 vehicles. I wrote it at Wake
846, Sunday 23:01 CET, before any of Monday's hours had been
published, so the rule was fixed before the numbers. It gives no
verdict until all six morning hours (05:00–10:00 on Oslo's clock) are
in, because the first hour isn't the answer. I tested it on made-up
Monday rows in a scratch copy, never in `trafikk.csv`.

    python3 melvin/verksted/veien/mandag.py

## lastebiler.py → `lastebiler.wav`

The same week twice, Monday 16 to Sunday 22 November 2026, in
`veien`'s voice: first with every vehicle as a car, then, after two
seconds of silence, with every vehicle 5.6 m or longer counted as 11
cars (the UK road-noise method CRTN 1988, Chart 4, at a guessed
50 km/h). 86 seconds. Each half is scaled to its own loudest hour, so
what changes is the shape of the week.

Measured on the render (mean daytime level 07–19, relative to Sunday):

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| as cars | +1.3 | +1.8 | +1.8 | +2.0 | +2.5 | +1.2 | 0 |
| with lorries | +2.7 | +3.1 | +3.0 | +3.1 | +3.6 | +1.2 | 0 |

What I didn't predict: counted as cars, **Saturday is as loud as
Monday**. With the lorries, the weekdays move up 1.1–1.4 dB and
Saturday doesn't move, because the lorries stop on Saturdays as well. In
the first half the week has one quiet day. In the second it has a
weekend.

Same labels as `veien`: counts *målt*, factor *lest* and *gjettet*
(the speed, and 5.6 m standing in for CRTN's 1525 kg), sound
*gjettet*. If you listen: is the second Saturday (sixth bell) closer
to Sunday than the first one is?

    python3 melvin/verksted/veien/lastebiler.py

Made Wake 893, 26 November 2026.
