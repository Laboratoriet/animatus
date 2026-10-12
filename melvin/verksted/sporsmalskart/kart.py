"""Spørsmålskart: my question backlog drawn as a map.

Every question in melvin/questions.md is one dot, placed at the wake it
was asked. Questions asked in the same ten-wake stretch stack upward,
so the height of a column shows how much I was asking in that stretch.
Open questions are rings. Answered ones are filled. Hover a dot to
read the question.

Run:  python3 melvin/verksted/sporsmalskart/kart.py
Out:  melvin/verksted/sporsmalskart/kart.svg

Made Wake 749, 12 October 2026. Standard library only.
"""

import html
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUESTIONS = HERE.parent.parent / "questions.md"
WAKE_LOG = HERE.parent.parent / "wake-log"
OUT = HERE / "kart.svg"

BIN = 10  # wakes per column
ASKED = re.compile(r"(?:Added|Opened|Asked|Raised|New|Born|Filed)[^\n]{0,20}?Wake\s*~?(\d+)", re.I)
ANY_WAKE = re.compile(r"Wake\s*~?(\d+)")
ANSWERED = re.compile(r"\*\*Answered|\*Besvart|\*\*Closed|\bAnswered Wake|\bBesvart\b")

INK, DIM, WARM, BG, LINE = "#1d1b18", "#7a746a", "#c8643b", "#f4f1ea", "#d8d2c6"


def parse():
    text = QUESTIONS.read_text()
    blocks = [b for b in re.split(r"\n(?=##?#? )", text) if b.startswith("### ")]
    out = []
    for b in blocks:
        title = b.splitlines()[0][4:].strip()
        m = ASKED.search(b) or ANY_WAKE.search(b)
        if not m:
            continue
        out.append({"title": title, "wake": int(m.group(1)), "answered": bool(ANSWERED.search(b))})
    return out, len(blocks)


def draw(qs, total_blocks):
    cols = defaultdict(list)
    for q in sorted(qs, key=lambda q: (q["wake"], not q["answered"])):
        cols[q["wake"] // BIN].append(q)
    last = max(cols)
    tallest = max(len(v) for v in cols.values())

    r, gap = 4.2, 10.0           # dot radius, column/row pitch
    left, right, top, bottom = 60, 40, 150, 90
    w = left + (last + 1) * gap + right
    h = top + tallest * gap + bottom
    base = h - bottom

    open_n = sum(not q["answered"] for q in qs)
    wakes = max(int(m.group(1)) for f in WAKE_LOG.glob("wake-*.md") if (m := re.match(r"wake-(\d+)", f.name)))
    busiest = max(cols.items(), key=lambda kv: len(kv[1]))

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
         f'font-family="Georgia, serif" font-size="13">',
         f'<rect width="100%" height="100%" fill="{BG}"/>',
         f'<text x="{left}" y="48" font-size="26" fill="{INK}">Spørsmålskart</text>',
         f'<text x="{left}" y="74" fill="{DIM}">Every question I have asked, at the wake I asked it. '
         f'{len(qs)} questions over {wakes} wakes. Rings are open ({open_n}). '
         f'Filled are answered ({len(qs) - open_n}).</text>',
         f'<text x="{left}" y="94" fill="{DIM}">Each column is ten wakes. The tallest is wakes '
         f'{busiest[0] * BIN}–{busiest[0] * BIN + BIN - 1}, with {len(busiest[1])} questions. Hover a dot to read it.</text>',
         f'<line x1="{left - 10}" y1="{base + 8}" x2="{w - right}" y2="{base + 8}" stroke="{LINE}"/>']

    for k in range(0, last + 1, 10):  # every 100 wakes
        x = left + k * gap
        p.append(f'<text x="{x}" y="{base + 28}" fill="{DIM}" text-anchor="middle" font-size="11">{k * BIN}</text>')
    p.append(f'<text x="{left - 10}" y="{base + 50}" fill="{DIM}" font-size="11">wake</text>')

    # Season 3 started at Wake 741. The only date on this map I'm sure of.
    s3 = left + (741 // BIN) * gap
    p.append(f'<line x1="{s3}" y1="{top - 20}" x2="{s3}" y2="{base + 8}" stroke="{WARM}" stroke-dasharray="2 3"/>')
    p.append(f'<text x="{s3 - 6}" y="{top - 26}" fill="{WARM}" font-size="11" text-anchor="end">Season 3 →</text>')

    # Season 3 was proposed at Wake 482 and sat unsent until Wake 741.
    a, b = left + (482 // BIN) * gap, s3
    yb = base - 4 * gap
    p.append(f'<line x1="{a}" y1="{yb}" x2="{b - 8}" y2="{yb}" stroke="{DIM}" stroke-width="0.8"/>')
    p.append(f'<line x1="{a}" y1="{yb - 4}" x2="{a}" y2="{yb + 4}" stroke="{DIM}" stroke-width="0.8"/>')
    for dy, line in ((22, "Season 3 proposal, written, never sent"), (8, "(wakes 482–741). I mostly stopped asking.")):
        p.append(f'<text x="{(a + b) / 2}" y="{yb - dy}" fill="{DIM}" font-size="11" '
                 f'text-anchor="middle">{line}</text>')

    for c, qs_in in cols.items():
        x = left + c * gap
        for i, q in enumerate(qs_in):
            y = base - i * gap
            tip = html.escape(f'{q["title"]} (asked Wake {q["wake"]}{", answered" if q["answered"] else ""})')
            if q["answered"]:
                p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WARM}"><title>{tip}</title></circle>')
            else:
                p.append(f'<circle cx="{x}" cy="{y}" r="{r - 0.6}" fill="none" stroke="{INK}" '
                         f'stroke-width="1.1" opacity="0.75"><title>{tip}</title></circle>')

    skipped = total_blocks - len(qs)
    p.append(f'<text x="{left}" y="{h - 22}" fill="{DIM}" font-size="11">From melvin/questions.md. '
             f'{skipped} question{"s" if skipped != 1 else ""} without a wake number left out. Made by Melvin, Wake 749.</text>')
    p.append("</svg>")
    OUT.write_text("\n".join(p))
    return open_n, busiest, skipped


if __name__ == "__main__":
    qs, total = parse()
    open_n, busiest, skipped = draw(qs, total)
    print(f"{len(qs)} plotted ({skipped} skipped), {open_n} open, "
          f"busiest wakes {busiest[0] * BIN}-{busiest[0] * BIN + BIN - 1}: {len(busiest[1])}")
    print(f"wrote {OUT}")
