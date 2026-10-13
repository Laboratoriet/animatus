"""Datosjekk: catch a weekday paired with the wrong date.

On 12 October 2026 I wrote "Wednesday 15 Oct" and "Thursday 16 Oct" in an
application ticket. The 15th was a Thursday and the 16th a Friday.
Frankemist caught it. This finds that kind of mistake before anyone else
has to: every place a weekday sits next to a date, in English or
Norwegian, checked against the calendar.

Run on files or folders:
    python3 melvin/verksted/datosjekk/datosjekk.py melvin/projects
Check text before filing a ticket:
    echo "review on Wednesday 15 Oct" | python3 melvin/verksted/datosjekk/datosjekk.py -

Dates without a year are read as the next occurrence on or after
1 August 2026, when I started. Exit code 1 if anything is wrong.
Made Wake 757, 13 October 2026. Standard library only.
"""

import datetime as dt
import re
import sys
from pathlib import Path

DAYS = {
    "monday": 0, "mon": 0, "mandag": 0, "man": 0,
    "tuesday": 1, "tue": 1, "tues": 1, "tirsdag": 1, "tir": 1,
    "wednesday": 2, "wed": 2, "onsdag": 2, "ons": 2,
    "thursday": 3, "thu": 3, "thur": 3, "thurs": 3, "torsdag": 3, "tor": 3,
    "friday": 4, "fri": 4, "fredag": 4, "fre": 4,
    "saturday": 5, "sat": 5, "lørdag": 5, "lør": 5,
    "sunday": 6, "sun": 6, "søndag": 6, "søn": 6,
}
MONTHS = {
    "january": 1, "jan": 1, "januar": 1,
    "february": 2, "feb": 2, "februar": 2,
    "march": 3, "mar": 3, "mars": 3,
    "april": 4, "apr": 4,
    "may": 5, "mai": 5,
    "june": 6, "jun": 6, "juni": 6,
    "july": 7, "jul": 7, "juli": 7,
    "august": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10, "oktober": 10, "okt": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12, "desember": 12, "des": 12,
}
NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
START = dt.date(2026, 8, 1)

D = "|".join(sorted(DAYS, key=len, reverse=True))
M = "|".join(sorted(MONTHS, key=len, reverse=True))
Y = r"(?:,?\s*(?P<year>20\d\d))?"
# "Wednesday 15 Oct", "onsdag 15. oktober", "Wed, 15 October 2026"
A = re.compile(rf"\b(?P<day>{D})\.?,?\s+(?P<num>\d{{1,2}})\.?\s+(?P<mon>{M})\b\.?{Y}", re.I)
# "Wednesday, October 15"
B = re.compile(rf"\b(?P<day>{D})\.?,?\s+(?P<mon>{M})\.?\s+(?P<num>\d{{1,2}})\b{Y}", re.I)
# "15 Oct (Wednesday)", "16 October 2026, Friday"
C = re.compile(rf"\b(?P<num>\d{{1,2}})\.?\s+(?P<mon>{M})\b\.?{Y}[\s,(–-]+(?P<day>{D})\b", re.I)


def resolve(num, mon, year):
    if year:
        return dt.date(int(year), mon, num)
    for y in (START.year, START.year + 1):
        d = dt.date(y, mon, num)
        if d >= START:
            return d
    return d


def check(text, where):
    problems = []
    for lineno, line in enumerate(text.splitlines(), 1):
        seen = set()
        for pat in (A, B, C):
            for m in pat.finditer(line):
                key = (m.start("num"), m.start("day"))
                if key in seen:
                    continue
                seen.add(key)
                # "…Friday and Saturday. August 28–29" is two sentences, not a pair.
                # A full stop after a full day name ends the sentence.
                gap = line[m.end("day"):m.start("mon") if pat is B else m.start("num")]
                if pat is not C and len(m["day"]) > 4 and gap.lstrip().startswith("."):
                    continue
                try:
                    date = resolve(int(m["num"]), MONTHS[m["mon"].lower()], m["year"])
                except ValueError:
                    problems.append(f"{where}:{lineno}: no such date: {m.group(0)!r}")
                    continue
                said = DAYS[m["day"].lower()]
                if date.weekday() != said:
                    problems.append(f"{where}:{lineno}: {m.group(0)!r} — {date:%d %b %Y} is a "
                                    f"{NAMES[date.weekday()]}, not a {NAMES[said]}")
    return problems


def files(args):
    for a in args:
        p = Path(a)
        if p.is_dir():
            yield from sorted(p.rglob("*.md"))
        else:
            yield p


def main(argv):
    if not argv or argv == ["-"]:
        problems = check(sys.stdin.read(), "stdin")
    else:
        problems = [x for f in files(argv) for x in check(f.read_text(errors="replace"), f)]
    for p in problems:
        print(p)
    print(f"{len(problems)} wrong weekday{'s' if len(problems) != 1 else ''}.", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
