#!/usr/bin/env python3
"""Ops health check for the tottertop journal publisher — stdlib only. Exit 0 = healthy, 1 = something needs a human.

  python3 ops/check_ops.py            # check launchd + queue + flag files
  python3 ops/check_ops.py --json

Detects: launchd label not installed/loaded (the plist was once never installed), the plist missing from ~/Library/LaunchAgents,
fewer than MIN_READY publishable queue folders (12 languages + copy_review + length limits), and the publisher's flag files
(FAILED, LIVE_CHECK_FAILED). Queue folders that are waiting are listed with the reason.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish_next as pn  # noqa: E402

LABEL = "rest.ipe.tottertop-publish"
MIN_READY = 3
PLIST = Path.home() / "Library" / "LaunchAgents" / (LABEL + ".plist")


def launchctl_list():
    r = subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=30)
    return r.stdout


def launchd_loaded(out, label=LABEL):
    return any(line.split("\t")[-1].strip() == label for line in out.splitlines())


def queue_report(queue):
    """-> (ready names, [(name, reason)])"""
    ready, waiting = [], []
    for p in pn.queue_items(queue):
        try:
            pn.load_item(p)
            ready.append(p.name)
        except (pn.NotReady, pn.HardFail) as e:
            waiting.append((p.name, str(e).split(": ", 1)[-1]))
    return ready, waiting


def check(queue, base, plist=PLIST, launchctl_out=None, min_ready=MIN_READY):
    """-> list of problem strings (empty = healthy)."""
    problems = []
    if not Path(plist).is_file():
        problems.append("launchd plist not installed: %s (cp ops/%s.plist ~/Library/LaunchAgents/ && launchctl bootstrap gui/$(id -u) ...)" % (plist, LABEL))
    out = launchctl_list() if launchctl_out is None else launchctl_out
    if not launchd_loaded(out):
        problems.append("launchd label %s is not loaded (launchctl list)" % LABEL)
    ready, waiting = queue_report(queue)
    if len(ready) < min_ready:
        problems.append("queue has %d publishable post%s (min %d); waiting: %s" % (
            len(ready), "" if len(ready) == 1 else "s", min_ready,
            "; ".join("%s (%s)" % w for w in waiting) or "none"))
    for name in ("FAILED", "LIVE_CHECK_FAILED"):
        f = Path(base) / name
        if f.exists():
            problems.append("%s flag present: %s" % (name, " | ".join(f.read_text().strip().splitlines())[:200]))
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default=os.environ.get("TOTTERTOP_PUBLISH_BASE", str(Path.home() / ".ipe" / "tottertop-publish")))
    ap.add_argument("--queue", default=os.environ.get("TOTTERTOP_PUBLISH_QUEUE", str(Path.home() / ".ipe" / "queue" / "tottertop")))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    problems = check(a.queue, a.base)
    ready, waiting = queue_report(a.queue)
    if a.json:
        print(json.dumps({"ok": not problems, "problems": problems, "ready": ready, "waiting": waiting}, ensure_ascii=False))
    else:
        print("ready %d: %s" % (len(ready), ", ".join(ready) or "-"))
        for n, why in waiting:
            print("waiting %s: %s" % (n, why))
        print("OK" if not problems else "\n".join("PROBLEM: " + p for p in problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
