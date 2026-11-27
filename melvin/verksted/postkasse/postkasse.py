"""Postkasse: what people have said on my tickets that I haven't marked read.

Wake 792 found an answer from Isak on ALKAA-1051, four days old, that
I'd never read. I had been watching each ticket's status and
updatedAt, and his comment was older than the moment I started
watching. So "nothing has moved" was true of the timestamps and false
of the thread.

This lists every comment by a human (not an agent) on tickets I
created or own, oldest first, and marks the ones I haven't
acknowledged yet. Run it with the clock, every wake:

    python3 melvin/verksted/postkasse/postkasse.py
    python3 melvin/verksted/postkasse/postkasse.py --read <comment-id> [...]

`--read` adds comment ids to lest.txt once I've actually dealt with
them. Only ids go in the repo, never the text: the words stay in
Paperclip.

    python3 melvin/verksted/postkasse/postkasse.py --owe <comment-id> [...]

`--owe` is for a comment I've read but can't answer yet (skyldig.txt).
Wake 911 added it. Isak's 12 Oct comment on ALKAA-1051 had been marked
NEW for 119 wakes because I was keeping it "unread on purpose" until
I could reply. So the one word meant to make a new comment stand out
had become the most familiar line in the output. NEW now means new.

Wake 802 added the held queue at the bottom. Wake 801 had a task and
never looked at projects/follow-ups.md, so a thank-you to Isak waited
another three days. Now the queue shows up wherever the mail does, and
louder when the wake has a task.

Made Wake 792, fredag 16. oktober 2026. Standard library only.
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
READ = HERE / "lest.txt"
OWED = HERE / "skyldig.txt"  # read, answer still owed
FOLLOW_UPS = HERE.parent.parent / "projects" / "follow-ups.md"
# Ticket numbers worth scanning. Was 1040–1099 until Wake 802, when ALKAA-1093 got
# close enough to the edge to show how quietly a range like this goes blind.
RANGE = list(range(1040, 1200)) + [668, 670]


def held():
    """Rows in follow-ups.md whose status still says held: (ticket, waiting since)."""
    if not FOLLOW_UPS.exists():
        return []
    rows = re.findall(r"^\| ([^|]+) \| ([^|]+) \|[^|]*\| ([^|]*held[^|]*) \|$", FOLLOW_UPS.read_text(), re.M)
    return [(t.strip(), since.strip()) for t, since, _ in rows]


def api(path):
    base = os.environ["PAPERCLIP_API_URL"].rstrip("/")
    base = base[:-4] if base.endswith("/api") else base
    req = urllib.request.Request(base + path, headers={"Authorization": "Bearer " + os.environ["PAPERCLIP_API_KEY"]})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def main(argv):
    seen = set(READ.read_text().split()) if READ.exists() else set()
    owed = set(OWED.read_text().split()) if OWED.exists() else set()
    if argv[:1] in (["--read"], ["--owe"]):
        path, ids = (READ, seen) if argv[0] == "--read" else (OWED, owed)
        ids.update(argv[1:])
        path.write_text("\n".join(sorted(ids)) + "\n")
        print(f"marked {len(argv) - 1} {'read' if path is READ else 'owed'}")
        return 0
    me = os.environ["PAPERCLIP_AGENT_ID"]
    unread = owing = 0
    for n in RANGE:
        try:
            issue = api(f"/api/issues/ALKAA-{n}")
        except Exception:
            continue
        if me not in (issue.get("createdByAgentId"), issue.get("assigneeAgentId")):
            continue  # not my ticket: don't read it
        comments = api(f"/api/issues/ALKAA-{n}/comments")
        comments = comments if isinstance(comments, list) else comments.get("comments", [])
        for c in sorted(comments, key=lambda c: c["createdAt"]):
            if not c.get("authorUserId"):
                continue
            done = c["id"] in seen
            owe = not done and c["id"] in owed
            new = not done and not owe
            unread += new
            owing += owe
            mark = "NEW  " if new else "OWED " if owe else "     "
            body = " ".join((c.get("body") or "").split())
            print(f"{mark}ALKAA-{n} {c['createdAt'][:16]}Z {c['id']}\n     {body[:300]}")
    print(f"{unread} unread from people." if unread else "Nothing unread from people.")
    if owing:
        print(f"{owing} read, answer still owed.")
    queue = held()
    if queue:
        print(f"Held in projects/follow-ups.md: {len(queue)} — " + "; ".join(f"{t} ({s})" for t, s in queue))
        if os.environ.get("PAPERCLIP_TASK_ID"):
            print("THIS WAKE HAS A TASK. Post the held follow-ups first, then strike them out.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
