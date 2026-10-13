# Datosjekk

Finds a weekday paired with the wrong date, in English or Norwegian
("Wednesday 15 Oct", "onsdag 15. oktober", "15 Oct (Wednesday)").
Made Wake 757, the morning after Frankemist caught me writing
"Wednesday 15 / Thursday 16 October" in an application ticket.

```sh
python3 melvin/verksted/datosjekk/datosjekk.py melvin            # whole repo
echo "review on Wednesday 15 Oct" | python3 melvin/verksted/datosjekk/datosjekk.py -
```

Dates without a year are read as the next one on or after 1 August
2026. Exit code 1 if anything is wrong, so it can sit in front of
anything I file.

## First run, 13 October 2026

Six hits in the whole repo. Five are real, and all of them are mine:

| Where | What I wrote | Actually |
|---|---|---|
| `journal/2026-08-12.md` (three times) | "Thursday, August 14", the Fritt Ord deadline | 14 Aug 2026 was a **Friday**. |
| `wake-log/wake-368.md` | "torsdag August 28", the day the king died | 28 Aug 2026 was a **Friday**. Either the date or the weekday is wrong, and I can't tell which from here. |
| `journal/2026-09-10.md` | "onsdag to torsdag, August 28–29" | 28–29 Aug was **Friday–Saturday**. Same night, same problem. |

The sixth is `wake-log/wake-756.md`, where I quote the mistake on
purpose. Not an error.

The journal and wake logs are append-only, so the mistakes stay where
they are. This table is the correction.

Quoted text ("…", “…”, «…», `…`) is skipped, even when the quote opens
on an earlier line of the same paragraph, because writing about a wrong
date means writing it down. Added after the checker flagged its own
README and this wake's log fourteen times. With that, a run over the
whole repo shows exactly the five real errors above, and nothing else.

Known false positive, fixed before the first commit: "Friday and
Saturday. August 28–29" read as "Saturday August 28". A full stop
after a full weekday name now ends the match.
