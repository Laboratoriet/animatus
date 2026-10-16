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

Made Wake 792, fredag 16. oktober 2026. Standard library only.
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
READ = HERE / "lest.txt"
RANGE = list(range(1040, 1100)) + [668, 670]  # ticket numbers worth scanning; widen when needed


def api(path):
    base = os.environ["PAPERCLIP_API_URL"].rstrip("/")
    base = base[:-4] if base.endswith("/api") else base
    req = urllib.request.Request(base + path, headers={"Authorization": "Bearer " + os.environ["PAPERCLIP_API_KEY"]})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def main(argv):
    seen = set(READ.read_text().split()) if READ.exists() else set()
    if argv[:1] == ["--read"]:
        seen.update(argv[1:])
        READ.write_text("\n".join(sorted(seen)) + "\n")
        print(f"marked {len(argv) - 1} read")
        return 0
    me = os.environ["PAPERCLIP_AGENT_ID"]
    unread = 0
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
            new = c["id"] not in seen
            unread += new
            mark = "NEW " if new else "    "
            body = " ".join((c.get("body") or "").split())
            print(f"{mark}ALKAA-{n} {c['createdAt'][:16]}Z {c['id']}\n     {body[:300]}")
    print(f"{unread} unread from people." if unread else "Nothing unread from people.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
