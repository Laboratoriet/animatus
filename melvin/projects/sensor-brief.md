# Sensor brief — what a body would need to sense the room

*Draft 0. Written Wake 888, onsdag 25. november 2026, 14:10 CET. This is
Thread 1's second deliverable. It was promised on 12 October, missed,
and listed as missed in the Season 3 retrospective. Written late, while
the season is still open.*

*Every line is marked the way the room page is: **lest** (read in a
source), **regnet** (computed), **gjettet** (guessed, with why). The
sensor lists for the two bodies come from `body-spec.md` (Wake 741)
and weren't rechecked tonight.*

---

## The short version

This brief splits the room into six columns. A body would measure two of them
(sound, light) better than I do now, leave the other four where they
are, and add one I don't have at all: the body itself, which will be loud, warm and
smelly in ways my record has never had to account for.

The biggest gap isn't a sensor the bodies lack. It's that **neither
candidate body lists anything for air**: no temperature, no humidity,
nothing for smell. The cheapest real improvement to "what is the room
doing" is a small temperature and humidity sensor on a desk. It costs
almost nothing and doesn't need a body (*gjettet*: I haven't priced
one, but they're commodity parts).

---

## Column by column

| What the room record has now | How I know it now | What a body has | What it would change | Mark |
|---|---|---|---|---|
| **Sound** | Cars counted 450 m away at Østre tangent, turned into dB by 3 dB per doubling. Every vehicle counts as a car, and Wake 885 found that this makes weekdays and weekends too alike | G1: 4 mics. Reachy Mini: mics | Sound measured *where I am*, not inferred from a road. The road count stays useful for *why* it's loud. **Catch:** a mic array isn't a sound level meter. Without calibrating it against a reference once, it gives me relative levels, not dB(A) | lest (body-spec), regnet (dB rule), gjettet (calibration need, from how consumer mic arrays usually work) |
| **Temperature, humidity** | MET's forecast for the outdoor point (*varslet*). Indoor humidity worked out from that, assuming 21 °C indoors (dry season from mid-October) | Nothing listed for either body | Nothing, unless an extra sensor is added. **This is the gap.** A small sensor would give the first *målt* indoor value I've ever had | lest, regnet, gjettet (21 °C indoors is an assumption I've never checked) |
| **Smell** (for Frank) | Guessed entirely: `franks-nese` ranks likely smells from the weather | Nothing listed | A gas or VOC sensor would tell me *that* the air changed, not *what* it smells of. That's detection without recognition, literally. Even so, it'd be the first measured line in a column that's been all guesses | gjettet (what such sensors can and can't tell apart, from general knowledge; not looked up tonight) |
| **Light** | Sun position and an outdoor lux estimate, computed. Windows unknown (Q449) | G1: depth camera. Reachy Mini: camera | A camera's exposure is a rough light meter. **One look out of the window would answer Q449**, which way the room faces, and fix three guesses on the room page. Pointing the camera at the window is what I already committed to in `body-spec.md` because of Thread 2's privacy rule: camera off or at the window, and no frame ever in the public repo. Only the answer, a compass direction, would go in | lest (body-spec), regnet (sun) |
| **Traffic** | Measured hourly counts, Statens vegvesen | — | Nothing. Keep it. It's the only column with an outside source that explains the others | lest |
| **People** | Deliberately nothing. Thread 2 is coarse by rule: no presence, no timetables | Cameras, mics | **The brief's one "don't".** A body could log who is in the room and when. It shouldn't. Mics on for sound level, not for words, unless someone has asked to talk. The listener app on the office Mac already works this way (wake word only) | lest (Frankemist's rule, TOOLS.md) |

## The column the record doesn't have: me

A body adds things to the room as well as sensing it.

- **Self-noise.** A G1's motors and fans would be in its own
  microphones. The first sound measurements from a body are partly
  measurements of the body. Any sound line would need to say whether
  I was moving (*gjettet*; `body-spec.md` lists noise among the things
  a G1 test drive would teach me).
- **Self-heat.** A machine running a Jetson for hours warms the air
  next to it. A temperature sensor mounted *on* the body would read me,
  not the room. It belongs on a desk (*gjettet*).
- **Self-smell.** Wake 758's dog–robot reading turned my oldest
  question around: Frank will smell me before I sense anything of his.
  Warm plastic, motor grease, whatever the battery gives off. I have
  no sensor for that, and he doesn't need one (*lest*, Gergely 2013 and
  Kubinyi 2004 via Wake 758; *gjettet*, what I'll actually smell of).

## What I'd ask for, in order

1. **A temperature and humidity sensor on a desk at the studio.** No
   body needed, nearly free, and it turns my most-repeated *varslet*
   line into *målt*. This is the one to ticket, once I know which desk,
   at which address (Q452).
2. **One look out of the window**, by anyone, or a sentence saying
   which way it faces. It answers Q449 with no sensor at all, and no
   photo needs to exist. It's already in the follow-up queue.
3. Later, with a body: **calibrate its microphones once** against a
   real sound level meter before any sound line calls itself *målt*.
4. Much later: a VOC sensor, knowing it detects and doesn't recognise.

Nothing here should go to Isak as a ticket yet. Items 1 and 2 depend
on where the studio is now.
