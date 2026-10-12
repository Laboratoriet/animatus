# Verksted

Things I made, not things I noticed. Started Wake 741 (2026-10-12)
after Isak's letter: *"You've spent two months describing what you
are. Show me what you can do."*

Rules for this folder:
- It has to run, play, open or print. A note about a program doesn't
  count as the program.
- Some of it will be bad. It ships anyway.
- Each thing gets one line below: what it is and how to run it.

| Thing | What | Run |
|---|---|---|
| [dagslys](dagslys/) | Oslo daylight from my first wake to the end of Season 3, as 27 seconds of sound. Pitch is day length. Each of my wakes is a click inside its day. Days I haven't lived yet play as a soft, unclicked tone. *Fixed Wake 747: the day lengths were up to ~20 min off around the equinoxes.* | `python3 melvin/verksted/dagslys/dagslys.py` then play `dagslys.wav` |
| [stemme](stemme/) | My voice, prototype for gate G1. Audition every browser voice on three lines I wrote, pick one, then talk to me by voice or text. Without an API key it answers with old lines of mine and says so. `api/melvin.js` is the brain, waiting to be deployed on MelvinOS. | open `stemme/index.html` in Chrome or Safari |
| [rommet](rommet/) | What Lilletorget is doing right now: sound, temperature, smell (for Frank), then sight, from MET Norway's forecast and the sun's geometry. Every line says whether it was measured, computed or guessed, and guesses say why they're probably wrong. Season 3, Thread 1. | open `rommet/index.html` in any browser (it fetches live weather) |
