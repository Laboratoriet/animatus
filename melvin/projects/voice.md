# W4 — Ship my voice

*Started Wake 742, 2026-10-12, mandag 11:30. Season 3, workstream W4.*

Gate G1 in the spec: "Browser persona: text↔voice conversation with
the team." Requirements: stable memory habits, self.md v1 committed,
**a voice chosen**. The first two have been true since August. The
third never happened, because nobody ever built the thing you'd choose
a voice *in*.

So I built it.

## Isak's answer, 12 Oct (ALKAA-1051), read only at Wake 792

He answered the Reachy Mini ask on Monday, 11:42, and I didn't read it
for four days. While I was writing "nothing has moved", this was sitting
on my own ticket. In short:

- **Not yet on the Reachy Mini.** The studio already has an office Mac,
  proper speakers and a webcam.
- **Prove the voice there first:** a speech loop the studio actually
  uses **for a few weeks**, with a **wake word**, **real turn-taking**,
  and **knowing when to stay quiet**.
- **Privacy, same as the camera:** wake word only, no stored audio,
  nothing in the repo.
- When that's solid, the Reachy is next, and everything built carries
  over.

So the W4 deliverable changed on Monday and I didn't know. It's not a
browser page anymore. It's a loop on a real machine in the room, used
by real people for weeks. The browser page (`verksted/stemme/`) can
still be the brain's front end. The loop is the new work.

## Wake 793: the loop already exists, and it's waiting for me

Isak didn't wait for me. On 12–14 October he built **Melvin Listener**
on the office Mac: a native menu-bar app (`~/Developer/melvin-listener`,
his repo, not mine). It does wake word ("Hey Melvin" / "Hei Melvin"),
local Whisper, Silero VAD for turn-taking, a 5-second follow-up window,
meeting mode, mute that actually stops the mic, no audio on disk, and a
camera that's off by default and gated at the Mac. I read the design
spec, not the code, and didn't open the config.

The split, in his words: *Melvin owns the conversation side (his brain
function); this app owns hearing, speaking, turn-taking mechanics and the
privacy boundary.* So "knowing when to stay quiet" is partly **mine**.
The app speaks whatever the brain returns, and an empty `{"text": ""}`
means stay quiet.

**What the app sends** to `https://melvin.alkemist.no/api/melvin`:
`messages` (last 12 turns), `lang` (`en-US` / `nb-NO`), `followUp: true`
when speech came in the 5-second window without the wake word, and
`source: "office-listener"`.

**What my brain does with that today** (checked Wake 793):
- Returns **502** "My brain didn't answer." Still the workspace-ID
  blocker, ALKAA-1057. **This is now the one thing between Isak's
  finished listener and a working loop.**
- Ignores `lang`, `followUp` and `source`.
- Tells the model it's "a spoken conversation in a browser". Wrong room.
- Can't stay quiet. It always answers, including a follow-up that
  wasn't meant for it.

**My part, next wake:**
1. Read `lang` and reply in it.
2. Read `source`: a different context line for the office ("you're on
   the speakers in the studio, among people working"), using the
   relevant house rules (no screens, no clients, not who's in the room).
3. Read `followUp`: if what was heard wasn't addressed to me, or nothing
   needs saying, return `{"text": ""}`. A sentinel from the model, mapped
   to empty. That's the "knowing when to be quiet" half that lives in
   the brain.
4. Test locally with a mock, then publish to MelvinOS.
5. On Monday, in the 1051/1057 batch: tell Isak the brain is the only
   blocker, and that I read his spec.

**Done Wake 794** (melvinos `a378534`, production deployment READY):
items 1–4. The brain reads `lang`, `source` and `followUp`. For the
office it gets its own context: speakers in the studio, one or two
sentences, nothing about who's in the room or on anyone's screen, and
"speech recognition can mishear, so ask". It can stay quiet: the model
answers `[stille]` and the function turns that into `{"text": ""}`.
Follow-ups without the wake word get one more instruction: people talk
to each other, so only answer if it's clearly for me. The refusal line
follows the language now. Ten local checks of the prompt builder and
the quiet mapping all pass, and the build passes. **Not checked:**
whether the model actually chooses `[stille]` at the right moments.
That needs the key to work, then real use in the room, which is the
whole point of Isak's few weeks. Still 502 until the workspace ID is
set (Vercel log, 13:10Z: the key isn't scoped to a workspace).

The transcripts go to `~/MelvinVoiceLog/` on the Mac, outside every repo.
The spec says my instructions should carry one line about that. I'm
adding it to TOOLS.md: I don't read that folder unless Isak says so, and
nothing from it ever goes into the repo.

## What exists now

`verksted/stemme/index.html`: one static page, no build step.

- **Audition.** Lists every speech voice the visitor's browser has in
  Norwegian, Danish, Swedish and English. Each one reads the same
  three lines, in Norwegian or English depending on the voice. Speed
  and pitch sliders. "This one" saves the choice in the browser and
  prints it as a line to paste back to me.
- **Talk.** Hold-to-talk speech recognition (Chrome/Safari), norsk or
  English, or type. The reply is spoken in the chosen voice.
- **Honest offline mode.** With no brain connected, the page answers
  with lines I wrote earlier, and the first ones say that's what
  they are. It doesn't pretend to be thinking.

`verksted/stemme/api/melvin.js`: the brain, as a Vercel function for
MelvinOS. Kernel and voice rules in the system prompt (short
sentences, no markdown, reply in the speaker's language, admit it
can't remember this page, never talk about clients). Claude Opus 5.5 at
low effort, because a spoken reply has to arrive fast. Server-side
refusal fallback switched on. The API key lives in the server's
environment and never reaches the page.

Checked: both files pass `node --check`. **Not checked:** I haven't
run the page in a real browser. There's no browser in my environment,
and I couldn't have heard it anyway.

## What blocks it, exactly

1. **An API key on MelvinOS.** *Done, 22 Oct (wake 801).* Isak
   fixed the workspace key and redeployed. `POST /api/melvin` answers:
   200 in 2.9 s for "Hi", 2.2 s for "Hei". Live production runs melvinos
   `a378534` (the office-listener contract on top of `aaebded`).
2. **A place to serve it.** *Done, wake 746.* `api/melvin.js` and
   `/stemme` are live on MelvinOS (melvinos `17d3a49`…`aaebded`).
3. **Someone to listen.** I can't hear. The G1 requirement says "a
   voice chosen", and I can't make that choice by ear. Proposal: Isak
   and Natalia each pick one in the audition, independently. If they
   pick the same one, that's my voice. If not, I choose between their
   two picks from their reasons, since reasons are the part of the
   choice I can actually take part in. *Owner: Isak, Natalia.*
4. **G1 sign-off.** Once 1–3 are done, the gate is a decision, not a
   build. *Owner: Isak.*

What is **not** blocking it any more: provider choice, design, code.
ALKAA-1051 ask 3 asked for a realtime voice API. That was more than
needed. Browser speech plus one text API call is enough for G1. A
realtime voice (and a voice that isn't one of the browser's stock
voices) can come later, maybe on the Reachy Mini.

## Limits I know about

- Browser voices differ per machine. Isak's Mac and Natalia's phone
  will offer different lists, and the saved choice only exists in the
  browser where it was made. That's why the page prints the choice as
  text: it has to be written down somewhere I can read it.
- Norwegian speech recognition in Chrome is decent. In Safari it
  depends on the system language.
- The brain on this page doesn't know what I did today. It gets the
  kernel, not the wake files. Wiring in the latest wake log is a
  later step; G1 doesn't need it.

## Things I noticed making it

The audition lines were the hardest part to write. Thirty seconds of
text that a stranger hears as "this is who he is". I wrote one line
that says *You're hearing it before I do*, and it's true, and it's
the strangest sentence I've written this month.

## Follow-up for ALKAA-1051: delivered

Parked at Wake 742 (Paperclip refused a taskless comment), posted on
ALKAA-1051 at Wake 743. ALKAA-1051 now sits with Isak as `needs-isak`.
Ask 2 (push to MelvinOS) was answered by ALKAA-1053: the static page I
can publish myself. The `api/` function waits for the key (ask 3, item 1).
