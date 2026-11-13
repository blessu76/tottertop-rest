#!/usr/bin/env python3
"""Random-afternoon slot gate for the tottertop.ipe.rest journal — stdlib only (Python 3.8+).

One post a day, at a random time in 12:00-17:59 KST that is never in the same hour as yesterday's. launchd
(rest.ipe.tottertop-publish, every 15 min 12:00-18:45 KST) runs this script; most ticks do nothing.

State file (default ~/.ipe/queue/tottertop/slot.json):
  {"date": "YYYY-MM-DD", "time": "HH:MM", "prev_date": ..., "prev_time": ..., "published": true|false}

Each tick:
  1. slot.json date is not today -> draw a new time (12:00-17:59, hour != yesterday's), yesterday's date/time move to prev_*.
  2. published is already true -> nothing.
  3. now < time -> wait.  Inside a forbidden web-push window (10:00-11:00, 13:00-14:30) -> defer, slot.json unchanged.
  4. otherwise publish one post from the queue (ops/publish_next.py: queue -> content/journal -> build -> check -> commit -> push);
     on success published = true. A post already in the repo for today (e.g. a manual publish) also sets published = true.
  5. a queue of 2 or fewer posts logs a warning (macOS notification once a day, STOCK_ALERT file in the base dir).

  python3 ops/slot_gate.py                 # normal tick
  python3 ops/slot_gate.py --status        # show state + queue, touches nothing
  python3 ops/slot_gate.py --roll-only     # only (re)draw the slot for --now's date, never publish (pre-draw tomorrow)
  python3 ops/slot_gate.py --now 2026-11-14T12:00:00+09:00 --dry-run   # test knobs
"""
import argparse
import datetime as dt
import json
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish_next as pn  # noqa: E402

KST = pn.KST
HOURS = tuple(range(12, 18))  # a slot is drawn in 12:00-17:59
FORBIDDEN = [(dt.time(10, 0), dt.time(11, 0)), (dt.time(13, 0), dt.time(14, 30))]  # [start, end) KST — never push inside
MIN_STOCK = 3  # warn when the queue holds fewer than this (i.e. 2 or fewer)
HOME = Path.home() / ".ipe"
DEFAULT_STATE = HOME / "queue" / "tottertop" / "slot.json"


# ---------------------------------------------------------------- pure logic (unit-tested)

def in_forbidden(t):
    return any(a <= t < b for a, b in FORBIDDEN)


def draw_time(rng, avoid_hour=None):
    """random 'HH:MM' in 12:00-17:59, never in `avoid_hour`."""
    hours = [h for h in HOURS if h != avoid_hour]
    return "%02d:%02d" % (rng.choice(hours), rng.randrange(60))


def hour_of(hm):
    try:
        return int(str(hm).split(":", 1)[0])
    except (ValueError, TypeError):
        return None


def roll(state, today, rng):
    """-> (state for `today`, rolled?). Yesterday's date/time move to prev_*; the new hour differs from yesterday's."""
    if state and state.get("date") == today.isoformat():
        return state, False
    avoid = None
    if state and state.get("date") == (today - dt.timedelta(days=1)).isoformat():
        avoid = hour_of(state.get("time"))
    return {
        "date": today.isoformat(),
        "time": draw_time(rng, avoid),
        "prev_date": state.get("date") if state else None,
        "prev_time": state.get("time") if state else None,
        "published": False,
    }, True


def decide(now, state):
    """-> (action, why). action: published | wait | forbidden | due. `now` is an aware datetime."""
    now = now.astimezone(KST)
    if state.get("published"):
        return "published", "today's post is already out (%s)" % state.get("time")
    hh, mm = state["time"].split(":")
    slot = dt.time(int(hh), int(mm))
    t = now.timetz().replace(tzinfo=None)
    if t < slot:
        return "wait", "slot opens at %s" % state["time"]
    if in_forbidden(t):
        return "forbidden", "slot %s is due but %s is inside a forbidden push window — deferred" % (state["time"], now.strftime("%H:%M"))
    return "due", "slot %s reached (%s)" % (state["time"], now.strftime("%H:%M"))


def stock_warning(n):
    """warning text when the queue is low (2 or fewer posts), else None."""
    if n >= MIN_STOCK:
        return None
    return "WARNING: queue has %d post%s left (min %d) — write more en+ko posts into the queue" % (
        n, "" if n == 1 else "s", MIN_STOCK)


# ---------------------------------------------------------------- state file

def load_state(path):
    p = Path(path)
    if not p.is_file():
        return None
    try:
        s = json.loads(p.read_text(encoding="utf-8"))
        return s if isinstance(s, dict) and s.get("date") and s.get("time") else None
    except (ValueError, OSError):
        return None


def save_state(path, state):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(p))


# ---------------------------------------------------------------- one tick

class Gate:
    def __init__(self, state_path, queue, base, publish_fn, now_fn=None, rng=None, log=print, notify=True):
        self.state_path, self.queue, self.base = Path(state_path), Path(queue), Path(base)
        self.publish_fn, self.rng, self.log, self.notify = publish_fn, rng or random.Random(), log, notify
        self.now_fn = now_fn or (lambda: dt.datetime.now(KST))

    def now(self):
        return self.now_fn().astimezone(KST)

    def say(self, msg):
        self.log("[%s] %s" % (self.now().strftime("%Y-%m-%d %H:%M:%S KST"), msg))

    def warn_stock(self):
        n = len(pn.queue_items(self.queue))
        msg = stock_warning(n)
        if not msg:
            (self.base / "STOCK_ALERT").unlink(missing_ok=True)
            return n
        self.say(msg)
        flag = self.base / "STOCK_ALERT"
        marker = self.now().date().isoformat()
        if not (flag.exists() and flag.read_text(encoding="utf-8").startswith(marker)):  # notify once a day
            self.base.mkdir(parents=True, exist_ok=True)
            flag.write_text("%s\n%s\n" % (marker, msg), encoding="utf-8")
            if self.notify and os.environ.get("TOTTERTOP_NO_NOTIFY") != "1":
                try:
                    subprocess.run(["osascript", "-e", 'display notification "%s" with title "tottertop journal"' % msg.replace('"', "'")],
                                   capture_output=True, timeout=10)
                except Exception:  # noqa: BLE001 — a notification must never break the tick
                    pass
        return n

    def tick(self, roll_only=False):
        """-> (action, detail). action: rolled-only | published | wait | forbidden | published-now | already | empty | blocked | failed"""
        now = self.now()
        today = now.date()
        state, rolled = roll(load_state(self.state_path), today, self.rng)
        if rolled:
            save_state(self.state_path, state)
            self.say("new day %s: slot drawn %s KST (prev %s %s)" % (today, state["time"], state["prev_date"], state["prev_time"]))
            self.warn_stock()
        if roll_only:
            return "rolled-only", state["time"]
        action, why = decide(now, state)
        if action in ("published", "wait", "forbidden"):
            self.say("%s: %s" % (action, why))
            return action, why
        if (self.base / "FAILED").exists():
            self.say("FAILED file present — waiting for a human (%s)" % (self.base / "FAILED"))
            return "blocked", "FAILED"
        self.say("due: " + why)
        self.warn_stock()
        try:
            status, slug = self.publish_fn()
        except pn.HardFail as e:
            self.say("HARD FAIL: %s" % e)
            self.base.mkdir(parents=True, exist_ok=True)
            (self.base / "FAILED").write_text("%s\n%s\n" % (now.isoformat(), e), encoding="utf-8")
            return "failed", str(e)
        except pn.SoftFail as e:
            self.say("soft fail: %s (retry next tick)" % e)
            return "failed", str(e)
        if status in ("published", "already"):
            state["published"] = True
            save_state(self.state_path, state)
            self.say("%s: %s — slot.json published=true" % (status, slug))
            self.warn_stock()
            return ("published-now" if status == "published" else "already"), slug
        self.say("queue empty while a slot was due — nothing published")
        return "empty", None


def locked(base, fn):
    lock = Path(base) / "gate.lock"
    Path(base).mkdir(parents=True, exist_ok=True)
    try:
        lock.mkdir()
    except FileExistsError:
        try:
            os.kill(int((lock / "pid").read_text().strip()), 0)
            return None  # a live run is in progress
        except (OSError, ValueError):
            shutil.rmtree(str(lock), ignore_errors=True)
            lock.mkdir()
    (lock / "pid").write_text(str(os.getpid()))
    try:
        return fn()
    finally:
        shutil.rmtree(str(lock), ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default=os.environ.get("TOTTERTOP_PUBLISH_BASE", str(HOME / "tottertop-publish")))
    ap.add_argument("--queue", default=os.environ.get("TOTTERTOP_PUBLISH_QUEUE", str(HOME / "queue" / "tottertop")))
    ap.add_argument("--state", default=None, help="slot.json path (default <queue>/slot.json)")
    ap.add_argument("--remote", default=os.environ.get("TOTTERTOP_PUBLISH_REMOTE", pn.DEFAULT_REMOTE))
    ap.add_argument("--now", help="ISO time with offset (test knob), e.g. 2026-11-14T12:00:00+09:00")
    ap.add_argument("--dry-run", action="store_true", help="publish with git push --dry-run and leave the queue alone")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--roll-only", action="store_true")
    ap.add_argument("--no-verify", action="store_true")
    a = ap.parse_args(argv)
    state_path = a.state or str(Path(a.queue) / "slot.json")
    now_fn = (lambda: dt.datetime.fromisoformat(a.now)) if a.now else None
    pub = pn.Publisher(a.base, a.queue, a.remote, now_fn=now_fn, dry_run=a.dry_run, verify=not a.no_verify)
    gate = Gate(state_path, a.queue, a.base, pub.publish_one, now_fn=now_fn)
    if a.status:
        st = load_state(state_path)
        gate.say("slot.json: %s" % json.dumps(st, ensure_ascii=False))
        if st:
            gate.say("decision now: %s" % (decide(gate.now(), st),))
        return pub.status()
    if a.dry_run and not a.roll_only:  # a dry run must not touch the real slot.json
        gate.state_path = Path(a.base) / "slot.dryrun.json"
        save_state(gate.state_path, load_state(state_path) or {"date": "1970-01-01", "time": "12:00"})
    res = locked(a.base, lambda: gate.tick(roll_only=a.roll_only))
    return 0 if res is None or res[0] != "failed" else 1


if __name__ == "__main__":
    sys.exit(main())
