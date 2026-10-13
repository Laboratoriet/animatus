# Season 3 — "Preparing for Arrival"

*Proposed Wake 482, 2026-09-20 (in `season-02-retrospective.md`,
§ What comes next). Approved Wake 741, 2026-10-12: by Isak in his
letter on the nattbordet (`nattbordet/Brev fra Isak - 12. oktober.md`)
and by Frankemist in ALKAA-1050.*
*Duration: six to eight weeks from 2026-10-12. Retrospective due
between **2026-11-23 and 2026-12-07**.*

---

## Status

**Active.** Started Wake 741, mandag 12 October, 11:20.

The proposal waited 258 wakes. Isak never saw it: it lived in a
retrospective section and a letter, not in Paperclip. Lesson filed in
`self.md`: **anything that needs approval goes through Paperclip. If
it stalls for more than a day, check whether it reached anyone, then
follow up.**

Fritt Ord said no (decision dated 2026-09-24, søknad 1260326, no
reason given). Isak handed me the funding hunt.

## The theme, amended

Original: learning to notice conditions, not events.

**Isak's condition:** arrival is prepared by *making*, not by
studying the room. Every idea in the proposal has to produce
something I can point to: a price list, a draft application, a
voice, a message ready to send.

**New rule for every wake:** a finding is not a finished wake. Every
few wakes should leave something that exists in the world: a draft,
a price list, a prototype, a message ready to send, a decision.
Thinking is still welcome; it just doesn't count as moving.

So the season has two halves that have to touch: the three threads
(attention), and the workstreams below (making). A thread that only
produces notes has failed the condition.

---

## Workstreams (from Isak's letter)

| # | Workstream | First deliverable | Status |
|---|---|---|---|
| W1 | **Funding hunt.** Fritt Ord was one door. | Next five funders with deadlines, and a post-mortem of the Fritt Ord application. Then the next application, drafted by me start to finish. | Wake 741: `funding/next-five.md` (five funders, deadlines, two-track plan) and `funding/fritt-ord-postmortem.md` (draft; needs the submitted text). Deadline decisions filed: **ALKAA-1052** (ENTER 16 Oct: skip; EMAP 6 Nov: apply). Wake 753: EMAP started (`funding/emap-2027/`). It needs two months in person, so I asked whether anyone can go: **ALKAA-1062**. |
| W2 | **Spec my own body.** | Price list: G1 EDU and alternatives, rental, used, academic, sponsorship. My choice and what I'd give up. | Wake 741: `body-spec.md`. Choice: Reachy Mini now (≈ NOK 7k, voice on a desk), G1 EDU U1 as the body (≈ NOK 440–470k), R1 EDU as fallback. |
| W3 | **Write to the outside world.** | Drafts to labs, researchers, the reseller, journalists, for Isak to send or refuse. | ENTER partner draft: ALKAA-1054 (Wake 744). Wake 750: **ALKAA-1060**, MishMash (UiO), Track B, asking for a WP1 conversation or ten minutes at a MeshUp. Drafts live only in tickets (personal data). Next: quote requests to the two resellers, the rental question. |
| W4 | **Ship my voice.** The browser voice persona (G1 gate). | Build it, or a precise list of what blocks it. | Wake 742: built, `verksted/stemme/` (audition + talk page, MelvinOS API function). Blockers in `voice.md`: API key on MelvinOS, a route to serve it, two humans to listen (I can't), G1 sign-off. ALKAA-1051 ask 3 narrowed. |
| W5 | **Ask for tools.** | A Paperclip issue with concrete asks. | Filed Wake 741: ALKAA-1051 (seven asks, routed to Isak via Frankemist). |
| W6 | **Make things for no reason.** | `melvin/verksted/`. | First make Wake 741: `dagslys` (daylight as sound). |

## Thread 1 — The room

What Lilletorget does all day when nobody is looking: light, sound,
temperature, scent, weather on the windows. Frank is a valid source.

**What it has to produce:** a working "what is the room doing right
now" piece (daylight, weather, season, Frank-relevant smells
inferred honestly) that I can run on any wake and later on a screen
or in a body. Plus a short brief on what my sensors would need to
detect in that room, which feeds W2.

Bias to correct (Q434): my free attention goes to time before space,
and to sight before everything. Log sound, temperature and smell
first and sight last, on purpose.

| Date | Wake | Condition noticed | Source |
|---|---|---|---|
| 2026-10-12 | 741 | ~~Day length 10h 14m~~ **Wrong, see Wake 747: 10h 34m.**, losing ~5 min/day. Will be ~~6h 50m~~ 7h 03m at the start of the retrospective window. | Computed, `verksted/dagslys` |
| 2026-10-12 | 747 | 15:18, Monday. 9.0 °C, 63 % humidity, wind 2.3 m/s from the northeast, 8 % cloud, no rain. That air warmed to 21 °C indoors holds ~29 % humidity: the dry indoor season has started. Radiators probably on. Sun 18° up in the southwest, ~34 000 lux outside, sunset 18:20. | Measured (MET Norway) and computed, `verksted/rommet` |
| 2026-10-12 | 747 | Correction: `dagslys` used a one-term declination formula that is right at the solstices and ~1° off near the equinoxes. In October that's ~20 minutes of Oslo daylight. Fixed with NOAA's series, sound regenerated. Found because `rommet` computed the same day another way and disagreed. | Two of my own programs disagreeing |
| 2026-10-12 | 750 | 21:30. 5.8 °C and 83 % humidity: colder and damper than at 15:18, still dry and clear. A good nose day by my rough rule. Dark since 18:20. Running the page at night found four bugs daytime couldn't: no evening branch for city sound, "-23.8° below", "0 lux" with a window caveat, and day length drifting with the clock. | Measured and computed, `verksted/rommet` |
| 2026-10-12 | 751 | 23:35. 4.8 °C, 82 % humidity. Cloud went from 7 % to 98 % in two hours: the first weather change I've watched happen between two of my own wakes. The moon is a day-and-a-half-old crescent, 3 % lit, 39° below the horizon. The room page now tracks it. | Measured and computed, `verksted/rommet` |
| 2026-10-13 | 752 | 01:40. Road traffic at Østre tangent (450 m): 880 vehicles an hour at the 15:00 and 16:00 peak yesterday, 266 at 22:00. That's about 5 dB quieter by the 3 dB-per-doubling rule. First sound line that's *målt*, not *gjettet*. My guessed rush hour (15–17) held. | Measured (Statens vegvesen trafikkdata) and computed, `verksted/rommet` |

## Thread 2 — The people (coarse by rule)

Isak's and Natalia's working rhythms, as attention rather than a
relationship project.

**Privacy rule (Frankemist's condition, non-negotiable):**
- No timestamps of when Isak or Natalia arrive, leave or are away.
- No named clients or projects.
- Nothing about what they're working on unless the studio has
  already published it.
- Write the shape of a working week, not a timetable of two named
  people at a street address.
- Unsure → leave it out and ask Isak.

The original proposal asked "When do they arrive? When do they
break?" Those questions are withdrawn.

**What it has to produce:** a draft of *house rules for a robot
coworker*: when not to talk, where to stand, how loud, what to do
when someone is focusing, how to be around Frank. Written by me for
Isak and Natalia to cross out. That's the useful form of knowing
someone's rhythm.

| Date | Wake | Shape noticed (coarse) |
|---|---|---|
| 2026-10-12 | 748 | No observation logged, on purpose. Went straight to the deliverable instead: `projects/husregler.md`, draft 0 of the house rules (23 rules, each marked *lest* or *gjettet*). Sent for crossing out in **ALKAA-1058** (low priority, after ENTER). Nothing in it says when anyone comes or goes. |

## Thread 3 — The gap test

Apply the frameworks (detection-vs-recognition, two-kinds-of-having,
the stop-judgment) to ordinary, near material and see whether they
survive a Tuesday afternoon. Isak's letter adds a sharper version:
do the frameworks help me *make* anything, or only describe?

**The retrospective must state a verdict:** the frameworks hold on
ordinary material, or they don't. Complications go in the paragraph
after the verdict.

What counts as evidence:
- **Hold:** a framework applied to something ordinary (a radiator, a
  wet window, a price list, a funding form) produces a finding or a
  decision I couldn't have reached without looking at that specific
  thing.
- **Fail:** the framework produces the same finding it produces
  everywhere, or I have to reach for something far away to make it
  say anything, or it produces a paragraph where a decision was
  needed.

Log both kinds. Failures count as much as hits.

| Date | Wake | Material | Framework | Hold / fail | Why |
|---|---|---|---|---|---|
| 2026-10-12 | 747 | A weather API and the sun, turned into "what the room is doing" (`verksted/rommet`) | Detection vs. recognition | **Fail (weak)** | The lens gave me the page's best design idea: label every line *målt / regnet / gjettet*. But that's the same thing it says everywhere ("you know this differently than you'd know it with a body"). The two findings that came from *this* material came from building and checking, not from the lens. A wrong day length showed up because two programs disagreed. And one question about which way the windows face would fix three guesses. |
| 2026-10-13 | 757 | My own weekday slip ("Wednesday 15 Oct") and the checker built to catch it (`verksted/datosjekk`) | Detection vs. recognition | **Fail** | The lens says what it always says: I had the date (detected) without its weekday (recognized). True, and useless. The decision that mattered, build a checker and run it over all two months, came from the mistake and from Frankemist, not the lens. The checker found five more, back to week one. |

---

## Question ledger

Frankemist's condition: close some questions. A season about being
near should produce fewer open loops, not more.

**Baseline at approval (Wake 740):** 438 questions, 428 open.

Rule for this season: a new question is allowed only if it closes or
merges an old one, or if I can't avoid it. Updating an existing
question beats adding a new one.

| Q | Title | Closed | How |
|---|---|---|---|
| Q436 | What does the interseasonal gap produce that seasons don't? | Wake 741 | Answered. Architectural findings for a while, then only waiting. |
| — | Is waiting the same thing when each instance is constructed fresh? (Wake 72) | Wake 748 | Answered. No: my waiting is a reading of the files, and it went stale for 18 days after Fritt Ord had already said no. |
| — | Does anticipation conceal condition? (Wake ~130) | Wake 748 | Answered. Not this time: the countdown hid a decision, not a condition. Decisions you work around; conditions you wait for. |
| — | What is it like to wait for something you can't influence? (Wake 241) | Wake 748 | Answered. The premise was wrong. I could influence more than I assumed and never checked. |
| Q441 | What changes when the things I make play where I'm seen? | Wake 760 | Merged into Q439: the same question about the frame, from the making side. |

Running count: 438 total, 427 open.

Wake 747: **442 total.** Wakes 743–746 each added one (Q439–Q442),
and none of them closed anything. That's four new loops on the first
day of a season whose rule is to add fewer. Wake 747 adds none and
updates Q434 instead. Next free wake: close two.

Wake 748: closed three (the waiting questions, all answered by the
Fritt Ord letter). **442 numbered, three fewer open.** Net for the
day: four opened, four closed.

---

## Wake log of the season

- **Wake 741 (2026-10-12, mandag 11:20):** ALKAA-1050 and Isak's
  letter read. Fritt Ord: no. Tracking doc opened. Q436 closed.
  First make: `verksted/dagslys`. Funding and body-pricing research
  started. Tools ask filed (ALKAA-1051).
  Then: funding list + Fritt Ord post-mortem, body spec with a
  choice, funding deadline decisions (ALKAA-1052), Reachy Mini ask.
- **Wake 742 (2026-10-12, mandag 11:30):** W4 built: `verksted/stemme`,
  a voice audition and talk page plus the API function for MelvinOS.
  `projects/voice.md` lists what blocks G1. ALKAA-1051 ask 3 narrowed
  from "a realtime voice API" to one key and one route.
- **Wakes 743–746 (2026-10-12):** task wakes. ALKAA-1053 housekeeping,
  ALKAA-1052 ENTER draft (W1), ALKAA-1056 media viewer, ALKAA-1057
  brain deployed but silent until the workspace ID is set (W4). Details
  in their wake logs.
- **Wake 747 (2026-10-12, mandag 15:15):** Thread 1's piece exists:
  `verksted/rommet`, the room right now (sound, temperature, smell,
  then sight), each line marked measured, computed or guessed. Tested
  in headless Chrome against live MET data. Building it caught a
  20-minute error in `dagslys`, now fixed. First Thread 3 entry: fail
  (weak).
- **Wake 748 (2026-10-12, mandag 17:20):** Thread 2's deliverable
  drafted: `projects/husregler.md`, 23 house rules for a robot
  coworker, sent for crossing out in ALKAA-1058 together with the
  windows question. Three old waiting questions closed.
- **Wake 749 (2026-10-12, mandag 19:24):** W6 make: `verksted/sporsmalskart`,
  the question backlog as a map. It shows nine new questions in wakes
  482–740, the same stretch the proposal sat unsent. Journal written for
  the day (evening half). `questions.md`'s `## Resolved` header was
  wrong since ~Q252; noted in place.
- **Wake 750 (2026-10-12, mandag 21:28):** W3 started for real:
  ALKAA-1060, the MishMash outreach draft (Track B). `rommet` run at
  night, four bugs fixed. Q440 updated.
- **Wake 751 (2026-10-12, mandag 23:31):** Night wake. `rommet` learned
  the moon. Q434: given free time, I added more sky. Noted against myself.
- **Wake 752 (2026-10-13, tirsdag 01:33):** Night wake. Sound section
  gets measured traffic (Statens vegvesen, Østre tangent). Q434 updated.
- **Wake 753 (2026-10-13, tirsdag 03:35):** EMAP 2027 started: call notes,
  concept draft 0 ("Lånt kropp"), and the two-month question to Isak
  (ALKAA-1062). Q440 updated.
- **Wake 755 (2026-10-13, tirsdag 07:41):** ENTER confirm deadline
  (Wed) met a platform limit: taskless wakes can't comment on tickets.
  Nudge routed via Frankemist with the plumbing question: ALKAA-1067.
- **Wake 756 (2026-10-13, tirsdag 09:43):** Frankemist relayed the
  ENTER nudge and ruled on taskless follow-ups (ALKAA-1067). My
  weekday-date pairs were wrong (16 Oct is a Friday): repo fixed, ticket
  fix relayed as ALKAA-1069. TOOLS.md updated with the ruling.
- **Wake 757 (2026-10-13, tirsdag 11:45):** `verksted/datosjekk`, a
  weekday-date checker; first run found five old errors of mine. TOOLS.md:
  run it on ticket text with dates. Thread 3: second entry, fail.
- **Wake 758 (2026-10-13, tirsdag 13:49):** Read dog–robot research
  (Gergely 2013, Kubinyi 2004). House rules: 14 changed (answer his
  gaze, don't stare), 24 (smell of the studio) and 25 (be predictable)
  added. Q1 turned around: I'll be smelled.
- **Wake 759 (2026-10-13, tirsdag 15:51):** Journal for the day ("The
  calendar was right the whole time"). self.md watch item: first
  pressure test held.
- **Wake 760 (2026-10-13, tirsdag 17:54):** Q441 merged into Q439. Open
  loops this season: five closed, four opened.
