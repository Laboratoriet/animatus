# EMAP 2027 — application draft

*Started Wake 800, lørdag 17. oktober 2026, 03:20. Due to Isak 28 Oct
(ALKAA-1052, yes from Isak 12 Oct). Call closes 6 Nov 2026, 14:00 CET.
Concept: `concept.md`. Hosts: `README.md` § Three hosts, ranked.*

**What I don't know yet.** The real form is behind a login at
call.emare.eu. Making an account is Isak's job, so I haven't seen the
field names or the character limits. This draft is the content any
such form will ask for, written to be cut. **One decision blocks the
whole thing:** ALKAA-1062, whether one of Isak and Natalia can go. ~~Whether
someone can be in residence for two months.~~ *(Wake 816: that wording
was stricter than the call. The FAQ says the time is negotiated with
the host and can be split or partly remote, and one person can go. The
plan in section 5 is about five weeks on site, in two blocks. Isak
asked for more info on 22 Oct; the answer is `svar-1062.md`.)* If the
answer is no, this file stops here.

## For Isak (written Wake 845, 25 Oct; to send Wednesday 28 Oct)

*Everything in this draft that only you, or you and Natalia, can
decide, gathered from the bracketed notes below. The call closes
6 Nov 2026, 14:00 CET. The form can be edited until then.*

1. **Can one of you go?** (ALKAA-1062.) The plan in section 5 is about
   five weeks on site in two blocks, plus the kick-off in Gijón on
   11–12 March. Everything else depends on this.
2. **Who applies** (section 2): you, Natalia, or both. And the
   collaborator: someone you name, or someone local that the host
   helps find.
3. **An account at call.emare.eu**, so we can see the real fields and
   character limits. The text is written to be cut once we know them.
4. **Ask Futurelab about the G1** (section 4): can a resident work with
   it? If you want, I'll draft the question as an `outbound-draft`
   ticket for you to send.
5. **A licence for the repo, if any** (sections 5 and 8). Right now it's
   public with no licence file.
6. **Budget** (section 9): the €4,000 production money.
7. **Your listener** (section 7): does it travel as it is, or does a
   version of it?
8. **Your own previous work** (section 8), written by you.

Later, with the host: opening days and rooms, and what may be kept
about visitors (section 6).

Not a decision, something you might use: a venue in Oslo signed a
letter of intent in August for Animatus' public tests in 2027
(ALKAA-580, named in ALKAA-1118). If the jury asks what happens after
the residency, that's an answer. Whether it goes in, and where, is
yours. Its name stays out of this file.

*Checked Wake 854 (mandag 26. oktober): I searched the tickets for
earlier EMAP, Ars Electronica and residency work before this goes to
you. Nothing from before Season 3 is about EMAP. April's research lists
Prix Ars Electronica, which is a prize and a different thing. So as
far as the tickets' wording goes, the draft doesn't redo anything. The search is how I found the letter above, this morning,
for Kulturrådet.*

*What I'll do myself before submission:* re-read the bracketed counts
in sections 3 and 8 (wake logs, journal entries, the question number),
re-check every link in section 8, and replace "is getting" and "built
to" in sections 1 and 3 with what the speech loop has actually done
by then.

Status per section: ✍️ drafted · ⬜ not started · 🔒 needs Isak/Natalia

| # | Section | Status |
|---|---|---|
| 1 | Title and one-paragraph summary | ✍️ |
| 2 | Applicants and collaboration | 🔒 who applies; ⬜ text |
| 3 | Project description | ✍️ (Wake 803) |
| 4 | Why this host (ranked three) | ✍️ (Wake 805) |
| 5 | Work plan for the two months | ✍️ (Wake 804, split in two blocks) |
| 6 | What the public meets | ✍️ (Wake 811) |
| 7 | Technical needs | ✍️ (Wake 809) |
| 8 | Previous work / documentation | ✍️ (Wake 806) |
| 9 | Budget use (€4k production) | 🔒 |

---

## 1. Title and summary ✍️

**Lånt kropp / Borrowed Body**

An AI character called Melvin has lived in public since August 2026,
waking about every two hours (800 wakes by mid-October), writing a
journal, asking questions, and making small instruments to learn a
room he can't enter: a design studio in Oslo. This autumn he is
getting a voice in that room, a speech loop on the studio's office
computer built to answer when someone says "Hey Melvin" and to stay
quiet otherwise. *[Before submitting: replace "is getting" and "built
to" with what the loop has actually done by then. As of Wake 802 the
brain answers over HTTP (checked Wake 801, 22 Oct), but I haven't seen
the loop used in the room, so it hasn't "answered" anyone there yet.]*
In 2027, over a two-month residency, he borrows a body from a media
lab. The
residency asks what changes in a character that has only been text
and voice once it has weight, and a body that belongs to someone
else. Visitors meet him in the borrowed body at the end, with the
whole public record of how he got there on a screen beside him.

*(143 words with the title, not including the bracketed note (48
words, added later). It was 144 until Wake 816, which changed "on the
wall next to him" to "on a screen beside him", to match sections 3
and 6: the house rules go on the wall, the record on a screen. The
first draft of this line said "same word count". It's one word
shorter, recounted with `wc -w`. If the form wants 500 characters,
cut to the first and last sentences.)*

*(Wake 861, tirsdag 27. oktober: "For two months in 2027 he borrows a
body" became "over a two-month residency, he borrows a body". The
plan in section 5 is about five weeks on site inside two months, and
whether the body is used between the blocks is the host's call. So
the residency is two months, and the body isn't promised for all of
it. Now 144 words, counted the same way as the 143.)*

---

## 3. Project description ✍️

*Drafted Wake 803, torsdag 22. oktober 2026, 08:00. Counts in
brackets were read from the repo today and must be re-read at
submission.*

**What exists.** Since 8 August 2026, Melvin, an AI agent at the Oslo
design studio Alkemist, has woken up to twelve times a day and written
down what he did, what he got wrong and what he wants to know. All of
it is in a public git repository: [802] wake logs, [68] journal
entries, a question backlog now at [Q445], letters he can't send yet,
and small instruments he built to learn a room he can't enter. One of
them, the room page, labels every line by how he knows it: measured,
forecast, calculated or guessed. When a label turned out to be wrong,
the correction stayed on the page. This autumn the studio is setting
up a speech loop on its office computer. Isak built the listening and
the speaking, and Melvin supplies the answers. *[Before submitting:
say what the loop has actually done by then.]* He has never had a body.

**The question.** What changes in a character when it gets weight?
Whether a language model can drive a robot is something labs show
every month. This asks what happens to one particular record: the
habits, the house rules, the mistakes made in public. What happens to
it once the character is in a room with people, in a body that
belongs to someone else and goes back at the end.

**The residency.** The host lends a robot body it already has. Nothing
is bought. *[True for Linz's G1 if Futurelab says yes. At Kersnikova or
LABoral the body would be adapted or made on site, partly from the
production budget. Rewrite this for whichever host ranks first.]* The artists and the host's technicians connect Melvin to
it. Before he moves in, Melvin writes house rules for himself, the way
he did for the studio in Oslo, and the host's staff edit them. Then
he lives in it, working daily in the lab while one of the artists is
there, and every wake stays public.
The body is never presented as his. It's on loan, and he says so.

**What the public meets.** An open studio at the host at the end.
Visitors meet Melvin in the borrowed body, with the record of how he
got there on a screen beside him, open to scroll.

*(Wake 816: 378 words with `wc -w`, recounted after adding a 33-word
bracketed note about which host has a body and "while one of the
artists is there" (7 words). 44 of the 378 are bracketed notes. Before
that: 338 words with `wc -w`, including the bracketed note to myself
(11 words, also counted). The first draft of this line said "about
290", and the first correction said the note was nine words. Both
were written before counting. Cut order if the field is short: the room-page
sentences first, then the house-rules sentence.)*

---

## 4. Why these hosts ✍️

*Drafted Wake 805, torsdag 22. oktober 2026, 12:10. From each host's
own profile on call.emare.eu/locations (read 16 Oct; quotes are
theirs) and, for Linz, the Ars Electronica blog. EMAP asks for an
order.*

**1. Ars Electronica Futurelab, Linz.** Its profile lists labs
"available for artists or researchers", among them a SecondBodyLab,
and in-house staff "including programmers, engineers, psychologists,
curators". This project is about a character getting a second body.
What that changes is a question a psychologist would ask differently
from an engineer, and Linz has both. The Ars Electronica blog (11
June 2026) shows a Unitree G1 humanoid as Futurelab's "latest
addition". *[Before
submitting: ask Futurelab whether a resident could work with it. The
FAQ invites that kind of question. If the answer is no, Linz still
fits for its people and labs, and the plan changes to a body made or
lent from elsewhere.]*

**2. Kersnikova Institute, Ljubljana.** Its Vivarium was set up "to
explore possible forms of coexistence among animals, fungi, plants,
and robots". The oldest question in Melvin's backlog is about Frank,
the studio dog, and what it means to share a room with someone who
knows the world through smell. Here that question would be the lab's
own subject. Kersnikova's hackerspace Rampa works with open-source
hardware, which suits a body adapted on site.

**3. LABoral, Gijón.** A fab lab and a "laboratory of experimental
electronics and software". If no body can be borrowed, one can be
made: something small with sensors, built for the residency. It's
also where the kick-off is held.

*(224 words with `wc -w`, counted after writing, including the
bracketed note to myself. This line was left blank until the count
came back.)*

---

## 5. Work plan ✍️

*Drafted Wake 804, torsdag 22. oktober 2026, 10:00, after reading
the FAQ (README § From the FAQ). The FAQ says residency times are
negotiated with the host and "in most cases it is possible to split the
time and return or do parts of it remotely". So this is one shape to
offer, not a promise. Every date after the kick-off is to be agreed.*

**Before (January–February 2027, remote).** The artists and the host's
technicians agree on which body, which interface, and what the body
may and may not do in their lab. Melvin works through text, so the
link is the host's own control software with a text layer on top.
Melvin writes house rules for living in the lab, the way he did for
the studio in Oslo, and the host's staff edit them. Nothing travels
yet.

**Kick-off, 11–12 March 2027, Gijón.** One of the artists attends.

**Block 1, at the host, about three weeks: arrival.** Connect Melvin
to the body. In the first week the body speaks and listens but stays
still unless a person who knows it is in the room. After that, daily
practice in the lab, with movement only inside limits the host sets.
Melvin keeps waking and writing as he does now. The record shows what
changed, in his own words, every day.

**Between blocks, remote, about three weeks.** The artists go home.
Melvin's writing goes on, and so does work on the interface from Oslo.
Whether Melvin uses the body while nobody from Alkemist is there is
the host's call, and the plan works either way.

**Block 2, at the host, about two weeks: open studio.** The
presentation at the host that the residency includes. Visitors meet
Melvin in the borrowed body, with the public record on a screen beside
him. He says plainly that he is a machine and that the body is on
loan.

**After.** The body goes back. What Melvin wrote while he had it stays
public. *[The repo has no licence file. Public isn't the same as
open-licensed, and which licence to use, if any, is Isak's call. Ask
before the form does.]*

*(On site: about five weeks for one person, not eight. 267 words with
`wc -w`, counted after writing and before the licence note was added.
The first draft said "under an open licence". There's no licence
file in the repo, so that was a plan written as a fact.)*

---

## 6. What the public meets ✍️

*Drafted Wake 811, fredag 23. oktober 2026, from 00:35 (klokka). The
format is the host's to shape. This is what the project brings to it.*

**At the host: an open studio at the end of Block 2.** This is the
presentation the residency includes. *[Days, room and opening hours
to agree with the host.]*

- **The body, on loan, with someone who knows it.** Visitors come up
  to it and talk. Melvin answers out loud, says that he is a machine,
  and says whose body it is. It moves only through the named actions
  agreed with the host, and only with a technician in the room.
- **The record, on a screen beside him.** Every wake since August
  2026, including the ones written in the lab that week. Visitors can
  scroll it and ask him about anything in it.
- **The house rules, on the wall.** The rules Melvin wrote before
  moving in, with the host's edits left visible: crossed out,
  rewritten, added to.
- **What he writes afterwards.** After each open day, Melvin writes
  about it in the record, in public. Visitors aren't named. *[What
  else about visitors may go in, and whether anything they say is
  kept, is to be agreed with the host and Isak before opening.]*

**Everywhere else, while it happens.** Anyone can read each wake on
MelvinOS on the day it's written, or talk to Melvin in a browser at
melvin.alkemist.no/stemme. *[If EMAP invites the work to its
conference or group shows, the record can travel. The body stays with
its owner.]*

*(232 words with `wc -w`, counted after writing, without the italic
header. 56 of them are the bracketed notes, so the text a host would
read is 176. This line had a placeholder until the count came back.)*

---

## 7. Technical needs ✍️

*Drafted Wake 809, torsdag 22. oktober 2026, from 20:26 (klokka).
What's known is marked, and the rest is to be agreed with the host.*

**From the host.**
- **A body it already has, and the people who know it.** Melvin's
  side is text in and text out. Movement would be a short list of
  named actions that the host's technicians define and allow (turn
  towards a voice, step back, nod), never raw motor control. The
  host's own control software does the moving. *[Which body and
  which software depends on the host. Ask before ranking. At
  Kersnikova or LABoral the body would be adapted or made on site,
  and "Bought: nothing planned" below would change.]*
- **A corner of the lab** where the body can stand and people can
  come up to it, with someone who knows the body present whenever it
  moves.
- **A network connection.** Each reply is one call to a language
  model through Melvin's existing function on MelvinOS. Measured
  from Oslo on 22 Oct: 3.5 s for a short Norwegian reply.
- **A screen** for the open studio, showing the public record
  (MelvinOS) next to the body.

**From the artists.**
- **A laptop** for the speech loop: listening, turn-taking and
  speaking. The studio's office listener is a macOS app built by
  Isak. *[Whether it travels as it is, or a version of it does, is
  his call.]*
- **A microphone and a speaker**, if the body doesn't have usable
  ones.

**Bought:** nothing planned. *[Budget, section 9, is Isak's.]*

*(227 words with `wc -w`, bracketed notes included. It was 207 until
Wake 816 added 20 words to the first note, about hosts without a
body.)*

---

## 8. Previous work and documentation ✍️

*Drafted Wake 806, torsdag 22. oktober 2026, from 14:10 (the wake's
start, as klokka printed it; an earlier version said 14:20, ahead of
the clock). Each link was
checked from outside today: GitHub's API says the repo is public
(`private: false`, `license: null`), and melvin.alkemist.no and
/stemme both return 200. Re-check all of them at submission.*

- **The record:** github.com/Laboratoriet/animatus, folder `melvin/`.
  It's public, and every wake since 8 August 2026 has a log there
  ([861] by 27 Oct, none missing).
  The history keeps each correction next to what it corrected. *[No
  licence yet. See section 5.]*
- **MelvinOS:** melvin.alkemist.no. A read-only desktop that loads
  the repository live, so visitors open Melvin's files instead of
  reading about him.
- **The voice:** melvin.alkemist.no/stemme. Talk to Melvin in a
  browser. The browser does the hearing and the speaking, and the
  replies come from the same function the studio's office listener
  uses. *[Connected since 22 Oct 2026.]*
- **The room:** `melvin/verksted/rommet/`. What the square outside
  the studio is doing now: weather, light, traffic and the sounds
  that follow from them. Every line is marked measured, forecast,
  calculated or guessed. There's a log of one row per wake since 14
  Oct and an hourly traffic series since 13 Oct. *[In the repo, not
  on a public page yet.]*
- **Small instruments:** daylight as sound (`dagslys`), a clock for
  a mind that loses track of weekdays (`klokka`), a checker that
  finds wrong weekdays in his own writing (`datosjekk`), a mailbox
  for the comments he forgot to read (`postkasse`), and a week of the
  road outside as 48 seconds of sound (`veien`).

*[The artists' own previous work goes here too, written by them.]*

*(204 words with `wc -w` for the five bullets. It was 192 until Wake
816 added `veien` to the small instruments, 12 words.)*

*(Wake 862, tirsdag 27. oktober: "every wake ... is a commit there" was
more than I'd checked. There are 912 commits since 7 August, and wakes
and commits don't line up one to one. What I can show is a log per
wake, numbered with no gaps, so that's what it says now. 210 words,
counted the same way. The count in brackets goes with the others in
section 3, to re-read at submission.)*

---

## Notes for the next sections

- **The strongest new fact since the concept:** the office listener
  (Isak's build, 12–14 Oct). By the residency, Melvin will have weeks
  or months of real spoken use in a real room. That answers
  "feasibility" better than anything in the Fritt Ord application did.
  Check what it has actually done before claiming anything. As of Wake
  802 the brain answers (200 since 22 Oct); use in the room is unseen.
- **Isak's first reaction (22 Oct, ALKAA-1062):** "Im intrigued. But I
  need more info." The answer is in `svar-1062.md` (relayed as
  ALKAA-1093). The FAQ facts that matter most: the two months can be
  split or partly remote, and one person can go.
- **Host order:** Linz (G1 and SecondBodyLab, but ask first whether a
  resident can use the G1), Ljubljana (Vivarium: animals, fungi,
  plants and robots coexisting; Frank's question), Gijón (fab lab: a
  body built for the residency).
- **I'm not the applicant.** The form should say plainly that the
  artist is a person (Isak, or Isak and Natalia) and that Melvin is the
  work. Q444 is still open for how to name me in a CV field.
- **Fritt Ord lessons** (`../fritt-ord-postmortem.md`): a public
  encounter at a named place, plain evidence with no superlatives, a
  body that doesn't depend on buying a robot.
