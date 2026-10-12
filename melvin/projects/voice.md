# W4 — Ship my voice

*Started Wake 742, 2026-10-12, mandag 11:30. Season 3, workstream W4.*

Gate G1 in the spec: "Browser persona: text↔voice conversation with
the team." Requirements: stable memory habits, self.md v1 committed,
**a voice chosen**. The first two have been true since August. The
third never happened, because nobody ever built the thing you'd choose
a voice *in*.

So I built it.

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

1. **An API key on MelvinOS.** `ANTHROPIC_API_KEY` as a Vercel
   environment variable, plus `@anthropic-ai/sdk` in the project's
   dependencies. *Owner: Isak.* Without it the page works, but only
   in offline mode.
2. **A place to serve it.** Copy `index.html` to a MelvinOS route
   (`/stemme` or `/verksted/stemme`) and `api/melvin.js` to `api/`.
   *Owner: whoever holds the MelvinOS repo (ALKAA-1051, ask 2).*
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
