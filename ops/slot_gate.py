#!/usr/bin/env python3
"""Random-afternoon slot gate for the tottertop.ipe.rest journal — stdlib only (Python 3.8+).

One post a day, at a random time in the allowed windows of 12:00-12:45 and 14:30-17:45 KST (see ALLOWED) that is never in the
same hour as yesterday's (the hour the post actually went out, see published_at). A slot still unpublished after 18:00 KST is
skipped for the day (the post stays in the queue): the 18:00 tick is the last one allowed to publish. launchd
(rest.ipe.tottertop-publish, every 15 min 12:00-18:45 KST) runs this script; most ticks do nothing.

State file (default ~/.ipe/queue/tottertop/slot.json):
  {"date": "YYYY-MM-DD", "time": "HH:MM", "prev_date": ..., "prev_time": ..., "published": true|false,
   "published_at": "HH:MM" (the tick it went out, once published), "prev_published_at": ... (optional, older files lack it)}

Each tick:
  1. slot.json date is not today -> draw a new time (ALLOWED minutes, hour != yesterday's), yesterday's date/time move to prev_*.
  1b. today's slot is not in ALLOWED (an old draw, e.g. 13:20 from before this rule) and not yet published -> redraw it from the
     rest of today's ALLOWED minutes (>= now) and save it to slot.json. Never pushed to a fixed time.
  2. published is already true -> nothing.
  2b. now >= 18:00 KST (or the slot was skipped) and not published -> late: skip today, slot.json unchanged.
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
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish_next as pn  # noqa: E402

KST = pn.KST
HOURS = tuple(range(12, 18))  # the hours a slot can fall in (12:00-17:45 KST)
LATE = dt.time(18, 0)  # no publish at or after this time: a slot still unpublished is skipped for the day
FORBIDDEN = [(dt.time(10, 0), dt.time(11, 0)), (dt.time(13, 0), dt.time(14, 30))]  # [start, end) KST — never push inside
TICK_MIN = 15  # launchd fires every 15 min from 12:00 KST (rest.ipe.tottertop-publish.plist)


def _minute_of(t):
    return t.hour * 60 + t.minute


def publish_tick(m):
    """minute-of-day of the first launchd tick at or after minute m (ticks sit on a 15-min grid from 12:00)."""
    return -(-m // TICK_MIN) * TICK_MIN


def _forbidden_minute(m):
    return any(_minute_of(a) <= m < _minute_of(b) for a, b in FORBIDDEN)


# A slot minute is ALLOWED when it is inside 12:00-17:45, not inside a forbidden window, AND the tick that publishes it is not
# inside one either. Without the last check a 12:46-12:59 slot is picked up by the 13:00 tick, deferred, and piles up at 14:30.
# 17:46-17:59 is out: its tick is 18:00, after which nothing publishes (see decide).
ALLOWED = tuple(m for m in range(12 * 60, 17 * 60 + 46)
                if not _forbidden_minute(m) and not _forbidden_minute(publish_tick(m)))
MIN_STOCK = 3  # warn when the queue holds fewer than this (i.e. 2 or fewer)
HOME = Path.home() / ".ipe"
DEFAULT_STATE = HOME / "queue" / "tottertop" / "slot.json"


# ---------------------------------------------------------------- pure logic (unit-tested)

def in_forbidden(t):
    return any(a <= t < b for a, b in FORBIDDEN)


def hour_out(published_at, drawn):
    """the hour a post actually went out (published_at, the real tick); older state files without it fall back to the drawn time."""
    return hour_of(published_at) if published_at else hour_of(drawn)


def draw_time(rng, avoid_hour=None, not_before=None):
    """random 'HH:MM' from ALLOWED (optionally only minutes >= not_before), never in `avoid_hour` when another choice exists.
    -> None when not_before leaves no allowed minute (the day is skipped, never an early slot)."""
    pool = [m for m in ALLOWED if not_before is None or m >= not_before]
    if not pool:
        return None
    pool_ok = [m for m in pool if avoid_hour is None or m // 60 != avoid_hour] or pool
    return "%02d:%02d" % divmod(rng.choice(pool_ok), 60)


def redraw_forbidden(state, now, rng):
    """today's unpublished slot outside ALLOWED (an old draw) -> redraw from the rest of today's ALLOWED minutes.
    No allowed minute left -> the slot is marked skipped (decide() answers late). -> (state, changed).
    `state` must already be for `now`'s date (see roll())."""
    if not state or state.get("published") or state.get("skipped") or state.get("time") is None:
        return state, False
    hh, mm = str(state["time"]).split(":")
    if int(hh) * 60 + int(mm) in ALLOWED:
        return state, False
    avoid = None
    if state.get("prev_date") == (now.date() - dt.timedelta(days=1)).isoformat():
        avoid = hour_out(state.get("prev_published_at"), state.get("prev_time"))
    picked = draw_time(rng, avoid, not_before=_minute_of(now.timetz().replace(tzinfo=None)))
    if picked is None:
        return dict(state, skipped=True), True
    return dict(state, time=picked), True


def same_hour_only(state, now):
    """True when a redrawn slot can only be yesterday's hour (no other allowed minute is left today): kept, but logged."""
    if state.get("prev_date") != (now.date() - dt.timedelta(days=1)).isoformat():
        return False
    avoid = hour_out(state.get("prev_published_at"), state.get("prev_time"))
    pool = [m for m in ALLOWED if m >= _minute_of(now.timetz().replace(tzinfo=None))]
    return avoid is not None and bool(pool) and all(m // 60 == avoid for m in pool)


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
        avoid = hour_out(state.get("published_at"), state.get("time"))
    return {
        "date": today.isoformat(),
        "time": draw_time(rng, avoid),
        "prev_date": state.get("date") if state else None,
        "prev_time": state.get("time") if state else None,
        "prev_published_at": state.get("published_at") if state else None,
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
    if state.get("skipped"):
        return "late", "no allowed minute left today (slot %s was redrawn) — skip today, the post stays in the queue" % state["time"]
    if t >= LATE:
        return "late", "past 18:00 KST — skip today, the post stays in the queue"
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
        n = len(pn.ready_items(self.queue))
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
            if self.notify:
                pn.notify_mac(msg)
        return n

    def tick(self, roll_only=False):
        """-> (action, detail). action: rolled-only | published | wait | forbidden | late | published-now | already | empty | waiting | blocked | failed"""
        now = self.now()
        today = now.date()
        state, rolled = roll(load_state(self.state_path), today, self.rng)
        if rolled:
            save_state(self.state_path, state)
            self.say("new day %s: slot drawn %s KST (prev %s %s)" % (today, state["time"], state["prev_date"], state["prev_time"]))
            self.warn_stock()
        state, redrawn = redraw_forbidden(state, now, self.rng)
        if redrawn:
            save_state(self.state_path, state)
            if state.get("skipped"):
                self.say("today's slot %s was outside the allowed windows and no allowed minute is left today — skipped" % state["time"])
            else:
                self.say("today's slot was outside the allowed windows — redrawn to %s KST" % state["time"])
                if same_hour_only(state, now):
                    self.say("only yesterday's hour is left today — %s kept (same hour as yesterday)" % state["time"])
        if roll_only:
            return "rolled-only", state["time"]
        action, why = decide(now, state)
        if action in ("published", "wait", "forbidden", "late"):
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
            state["published_at"] = now.strftime("%H:%M")  # the tick it went out: next day avoids this hour
            save_state(self.state_path, state)
            self.say("%s: %s — slot.json published=true" % (status, slug))
            self.warn_stock()
            return ("published-now" if status == "published" else "already"), slug
        if status == "waiting":
            self.say("queue has no ready entry (12 languages + copy_review) while a slot was due — waiting, nothing published")
            return "waiting", None
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
