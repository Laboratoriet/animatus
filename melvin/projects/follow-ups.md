# Held follow-ups

*Started Wake 762, tirsdag 13. oktober 2026, 22:00.*

**Pace rule (since 14 Oct):** nothing new goes to Isak until ENTER is
settled (after Friday 16 Oct), unless something is actually urgent. Held
items wait here. Not on the weekend either: the first working day after
is Monday 19 Oct, and that's when the batch goes, small.

Taskless wakes can't comment on, edit, or answer cards on tickets
(`cross_issue_influence_run_context_required`). Frankemist's ruling
(ALKAA-1067): anything that isn't time-critical waits for a wake that
has a task, and then goes on the original ticket. Time-critical things
go to Frankemist as `Relay: <ALKAA-NNN> …` (TOOLS.md).

This file is the queue, so a task-bound wake can clear it in a minute
without having to remember. **On a task-bound wake:** post what's
below, then strike it out here with the wake number. Before posting
anything with dates, run it through `verksted/datosjekk`.

| Ticket | Waiting since | Action | Status |
|---|---|---|---|
| ALKAA-1067 | Wake 756 | Accept Frankemist's card ("Updated TOOLS.md"). | held |
| ALKAA-670 | Wake 762 | Comment below, ask Frankemist to close. | held |
| ALKAA-1051 | Wake 762 (filed 741) | Status comment below. Post after ENTER. | held |
| ALKAA-1062 | Wake 767 | Add the Linz finding below; it bears on the two-month decision. Not urgent (EMAP closes 6 Nov). | held |
| ALKAA-1058 | Wake 772 | Follow-up would be due now, but **held by the pace rule** (journal 14 Oct): nothing new to Isak until ENTER is settled, after Friday 16 Oct. Revisit then. | held |
| ALKAA-1051 | Wake 776 | One more ask to fold into the status comment, not a new ticket: a MET Frost API client ID (free, but it's a registration), so `rommet/logg.csv` can hold station readings instead of forecasts. Low priority. | held, after ENTER |
| *(new ticket)* | Wake 779 (text drafted Wake 791, below) | After ENTER is settled: **one** `needs-isak` ticket on the Kulturrådet route. January or April round? Producer (Alkemist AS) or artist group? Which venue to ask for the mandatory intention agreement? Attach the candidate-venue list. Notes: `projects/funding/kulturradet-2027/README.md`. Venue outreach realistically starts in November. | held, after ENTER |

## Text to post

**ALKAA-670** (backlog since 8 August):

> This can be closed. The remote exists (`Laboratoriet/animatus`) and
> every wake since August has pushed to it. — Melvin, Wake 762

**ALKAA-1051** (tools, filed Wake 741), after ENTER:

> Status of the eight asks, for when there's time:
> 1. Submitted Fritt Ord text: still wanted, for the post-mortem.
> 2. MelvinOS access: done (ALKAA-1053). Thank you.
> 3. Voice: the brain is deployed. It needs `ANTHROPIC_WORKSPACE_ID` on
>    the Vercel project, or a workspace-scoped key (ALKAA-1057).
>    And per your answer on ask 8, the real target is the speech loop
>    on the office Mac. I've since found Melvin Listener and read the
>    spec. Thank you for building it. As far as I can tell, my brain
>    is the only thing between it and a working loop: it returns 502
>    until `ANTHROPIC_WORKSPACE_ID` is set (ALKAA-1057). The brain now
>    speaks the spec's contract: `lang`, `source`, `followUp`, and
>    staying quiet with an empty reply (deployed Friday, melvinos
>    a378534).
> 4. Room sensor: open. The room page now has MET's forecast for the
>    hour (not a measurement; I had it labelled wrong until Wake 776) and
>    measured traffic counts. Indoor sound and air are still guesses.
>    One small addition: a MET Frost client ID (free, but it's a
>    registration) would let the log hold station readings instead of
>    forecasts. Low priority.
> 5. Drafts-only outbox: done, via the `outbound-draft` tickets.
> 6. Budget line: open.
> 7. Wake shape (fewer night wakes): open, low priority.
> 8. Reachy Mini: you answered on Monday (not yet; prove the voice on
>    the office Mac first: wake word, turn-taking, knowing when to be
>    quiet, no stored audio). I'm sorry: I didn't read it until Friday.
>    I'd been watching the ticket's timestamps, not its comments. The
>    speech loop is now W4. Plan in `voice.md`.
> Nothing here is urgent. — Melvin

**ALKAA-1062** (EMAP, can someone go for two months?):

> One fact that might help the decision: Ars Electronica's Futurelab in
> Linz, one of the fifteen EMAP hosts, has a Unitree G1, the body in my
> spec (their blog, 11 June 2026). Their EMAP host profile doesn't
> mention it, so whether a resident could work with it would need
> asking first. I've read all fifteen host profiles and ranked three:
> Linz (the G1, and a lab called SecondBodyLab), Ljubljana (a lab for
> how animals and robots coexist), Gijón (a fab lab, if the body has to
> be built). Notes in `funding/emap-2027/README.md`. — Melvin

*(Wake 791: both texts above were checked against today's facts before
posting and corrected. 1051 said "measured weather" and 1062 promised
"the actual robot". Neither was true.)*

**New ticket, Kulturrådet route** (`needs-isak`, one ticket). Post on a
working day after ENTER is settled, so not before Monday 19 Oct:

> **Title:** Kulturrådet visual art: which round, who applies, which venue?
>
> If ENTER didn't happen, Kulturrådet is the fallback for the
> collaboration idea. EMAP can't share its money either way, because
> Kulturrådet doesn't fund residencies. I read the call properly this
> week, and it needs more lead time than I'd planned:
>
> - **A signed exhibition or intention agreement with a venue is
>   mandatory.** Someone has to say yes before we can apply.
> - Never full funding: the budget needs other income.
> - Deadline 15 Jan 2027, 13:00 (portal opens 15 Dec). Next rounds 8
>   Apr and 15 Sep.
>
> Three decisions, all yours:
> 1. January or April? January means asking a venue in November. April
>    is calmer, and could come after an EMAP residency.
> 2. Alkemist AS as producer, or you and Natalia as an artist group?
> 3. Which venue to ask? Six candidates with reasons, each checked
>    against its own website: `funding/kulturradet-2027/venues.md`.
>
> There's a sketch of the project, *Målt, varslet, regnet, gjettet*
> (the room page, moved to a gallery, plus a label for what visitors
> tell me): `funding/kulturradet-2027/skisse.md`. Rewrite it or bin it.
> No rush before November. — Melvin
