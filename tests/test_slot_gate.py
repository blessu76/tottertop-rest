"""Slot gate + queue publisher (ops/): same-hour exclusion, date rollover, already-published ignored, stock warning,
forbidden-window deferral, and a publish round trip against a local bare remote."""
import datetime as dt
import json
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

from helpers import REPO

sys.path.insert(0, str(REPO / "ops"))
import publish_next as pn  # noqa: E402
import slot_gate as sg  # noqa: E402

KST = dt.timezone(dt.timedelta(hours=9))


def at(day, hm):
    h, m = hm.split(":")
    return dt.datetime.combine(dt.date.fromisoformat(day), dt.time(int(h), int(m)), tzinfo=KST)


def post_md(slug, lang, title="T", review=True):
    rv = "copy_review: iris 2026-11-14\n" if review else ""
    return "---\nslug: %s\nlang: %s\ntitle: %s\ndescription: D\nexcerpt: E\n%s---\nbody %s\n" % (slug, lang, title, rv, lang)


def make_queue(root, n, langs=pn.MAIN_LANGS):
    q = Path(root) / "queue"
    for i in range(n):
        d = q / ("%02d-post-%d" % (i + 1, i + 1))
        d.mkdir(parents=True)
        for lang in langs:
            (d / (lang + ".md")).write_text(post_md("post-%d" % (i + 1), lang, "Title %d" % (i + 1)), encoding="utf-8")
    q.mkdir(parents=True, exist_ok=True)
    return q


class SlotLogicTests(unittest.TestCase):
    def test_draw_is_in_the_afternoon_window(self):
        rng = random.Random(1)
        for _ in range(2000):
            h, m = map(int, sg.draw_time(rng).split(":"))
            self.assertTrue(12 <= h <= 17 and 0 <= m <= 59)

    def test_yesterdays_hour_is_never_drawn(self):
        today = dt.date(2026, 11, 14)
        for hour in range(12, 18):
            state = {"date": "2026-11-13", "time": "%02d:%02d" % (hour, 20), "published": True}
            for seed in range(200):
                new, rolled = sg.roll(state, today, random.Random(seed))
                self.assertTrue(rolled)
                self.assertNotEqual(int(new["time"][:2]), hour)

    def test_date_rollover_moves_yesterday_into_prev(self):
        state = {"date": "2026-11-13", "time": "15:42", "prev_date": "2026-11-12", "prev_time": "13:05", "published": True}
        new, rolled = sg.roll(state, dt.date(2026, 11, 14), random.Random(7))
        self.assertTrue(rolled)
        self.assertEqual((new["date"], new["prev_date"], new["prev_time"], new["published"]), ("2026-11-14", "2026-11-13", "15:42", False))

    def test_same_day_is_not_rolled_again(self):
        state = {"date": "2026-11-14", "time": "13:30", "prev_date": None, "prev_time": None, "published": False}
        new, rolled = sg.roll(state, dt.date(2026, 11, 14), random.Random(7))
        self.assertFalse(rolled)
        self.assertEqual(new, state)

    def test_first_run_without_state(self):
        new, rolled = sg.roll(None, dt.date(2026, 11, 14), random.Random(3))
        self.assertTrue(rolled)
        self.assertIsNone(new["prev_time"])
        self.assertFalse(new["published"])

    def test_decide(self):
        st = {"date": "2026-11-14", "time": "16:10", "published": False}
        self.assertEqual(sg.decide(at("2026-11-14", "16:00"), st)[0], "wait")
        self.assertEqual(sg.decide(at("2026-11-14", "16:15"), st)[0], "due")
        self.assertEqual(sg.decide(at("2026-11-14", "16:15"), dict(st, published=True))[0], "published")
        inside = {"date": "2026-11-14", "time": "13:20", "published": False}
        self.assertEqual(sg.decide(at("2026-11-14", "13:30"), inside)[0], "forbidden")
        self.assertEqual(sg.decide(at("2026-11-14", "14:15"), inside)[0], "forbidden")
        self.assertEqual(sg.decide(at("2026-11-14", "14:30"), inside)[0], "due")

    def test_allowed_minutes_skip_forbidden_and_the_ticks_that_would_defer(self):
        self.assertEqual((sg.ALLOWED[0], sg.ALLOWED[-1]), (12 * 60, 17 * 60 + 59))
        for m in sg.ALLOWED:
            self.assertFalse(13 * 60 <= m < 14 * 60 + 30, m)  # forbidden web-push window
            self.assertFalse(10 * 60 <= m < 11 * 60, m)
            self.assertFalse(13 * 60 <= sg.publish_tick(m) < 14 * 60 + 30, m)  # the tick that would publish it is not forbidden
        self.assertNotIn(12 * 60 + 46, sg.ALLOWED)  # 13:00 tick would defer it to 14:30
        self.assertIn(12 * 60 + 45, sg.ALLOWED)
        self.assertIn(14 * 60 + 30, sg.ALLOWED)

    def test_hundreds_of_draws_never_land_in_a_forbidden_window(self):
        rng = random.Random(42)
        for _ in range(1000):
            h, m = map(int, sg.draw_time(rng).split(":"))
            self.assertFalse(13 * 60 <= h * 60 + m < 14 * 60 + 30)
            self.assertIn(h * 60 + m, sg.ALLOWED)
        state, today = None, dt.date(2026, 11, 21)
        for day in range(500):
            state, _ = sg.roll(state, today + dt.timedelta(days=day), rng)
            self.assertIn(sg._minute_of(dt.time(*map(int, state["time"].split(":")))), sg.ALLOWED)

    def test_draws_vary_across_days(self):
        state, seen = None, set()
        for day in range(30):
            state, _ = sg.roll(state, dt.date(2026, 11, 21) + dt.timedelta(days=day), random.Random(day))
            seen.add(state["time"])
        self.assertGreaterEqual(len(seen), 20)
        self.assertGreaterEqual(len({t[:2] for t in seen}), 3)  # several different hours

    def test_redraw_moves_a_forbidden_slot_into_the_rest_of_today(self):
        state = {"date": "2026-11-14", "time": "13:20", "prev_date": "2026-11-13", "prev_time": "15:10", "published": False}
        for seed in range(200):
            new, changed = sg.redraw_forbidden(dict(state), at("2026-11-14", "12:10"), random.Random(seed))
            self.assertTrue(changed)
            h, m = map(int, new["time"].split(":"))
            self.assertIn(h * 60 + m, sg.ALLOWED)
            self.assertGreaterEqual(h * 60 + m, 12 * 60 + 10)
            self.assertNotEqual(h, 15)  # yesterday's hour still avoided

    def test_redraw_after_the_window_opens_only_picks_from_now_on(self):
        state = {"date": "2026-11-14", "time": "13:20", "published": False}
        for seed in range(200):
            new, changed = sg.redraw_forbidden(dict(state), at("2026-11-14", "13:45"), random.Random(seed))
            self.assertTrue(changed)
            self.assertGreaterEqual(new["time"], "14:30")

    def test_allowed_or_published_slots_are_left_alone(self):
        for st in ({"date": "2026-11-14", "time": "12:40", "published": False},
                   {"date": "2026-11-14", "time": "13:20", "published": True}):
            new, changed = sg.redraw_forbidden(dict(st), at("2026-11-14", "12:00"), random.Random(1))
            self.assertFalse(changed)
            self.assertEqual(new, st)

    def test_stock_warning_at_two_or_fewer(self):
        for n in (0, 1, 2):
            self.assertIn("WARNING", sg.stock_warning(n))
        self.assertIsNone(sg.stock_warning(3))


class GateTickTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tt-gate-"))
        self.logs, self.calls, self.now = [], [], at("2026-11-14", "12:00")

    def tearDown(self):
        shutil.rmtree(str(self.tmp))

    def gate(self, n_queue, outcome=("published", "2026-11-14-post-1"), seed=5):
        q = make_queue(self.tmp, n_queue)

        def publish():
            self.calls.append(self.now)
            if isinstance(outcome, Exception):
                raise outcome
            return outcome

        return sg.Gate(q / "slot.json", q, self.tmp / "base", publish, now_fn=lambda: self.now,
                       rng=random.Random(seed), log=self.logs.append, notify=False)

    def state(self, g):
        return json.loads(g.state_path.read_text(encoding="utf-8"))

    def test_rollover_then_publish_once(self):
        g = self.gate(5)
        g.state_path.write_text(json.dumps({"date": "2026-11-13", "time": "15:30", "published": True}), encoding="utf-8")
        self.now = at("2026-11-14", "12:00")
        action, _ = g.tick()
        st = self.state(g)
        self.assertEqual((st["date"], st["prev_date"], st["prev_time"], st["published"]), ("2026-11-14", "2026-11-13", "15:30", False))
        self.assertNotEqual(st["time"][:2], "15")
        self.assertIn(action, ("wait", "forbidden", "published-now"))
        self.now = at("2026-11-14", "18:45")  # well past any slot and outside the forbidden windows
        self.assertEqual(g.tick()[0], "published-now")
        self.assertEqual(len(self.calls), 1)
        self.assertTrue(self.state(g)["published"])

    def test_already_published_is_ignored(self):
        g = self.gate(5)
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "12:00", "published": True}), encoding="utf-8")
        self.now = at("2026-11-14", "17:00")
        self.assertEqual(g.tick()[0], "published")
        self.assertEqual(self.calls, [])

    def test_waits_before_the_slot(self):
        g = self.gate(5)
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "16:40", "published": False}), encoding="utf-8")
        self.now = at("2026-11-14", "16:30")
        self.assertEqual(g.tick()[0], "wait")
        self.assertEqual(self.calls, [])

    def test_forbidden_window_defers_without_touching_state(self):
        # an allowed slot (12:40) whose ticks were missed (Mac asleep) is found inside the window: defer, state unchanged
        g = self.gate(5)
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "12:40", "published": False}), encoding="utf-8")
        self.now = at("2026-11-14", "13:05")
        self.assertEqual(g.tick()[0], "forbidden")
        self.assertEqual(self.calls, [])
        self.assertEqual(self.state(g), {"date": "2026-11-14", "time": "12:40", "published": False})
        self.now = at("2026-11-14", "14:30")
        self.assertEqual(g.tick()[0], "published-now")

    def test_old_forbidden_slot_is_redrawn_and_saved_not_pushed_to_14_30(self):
        g = self.gate(5)
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "13:20", "published": False}), encoding="utf-8")
        self.now = at("2026-11-14", "13:10")
        action, _ = g.tick()
        st = self.state(g)
        self.assertNotEqual(st["time"], "13:20")
        self.assertIn(int(st["time"][:2]) * 60 + int(st["time"][3:]), sg.ALLOWED)
        self.assertGreaterEqual(st["time"], "14:30")  # only the rest of today's window is left
        self.assertEqual(action, "wait")
        self.assertEqual(self.calls, [])
        self.now = at("2026-11-14", "17:59")
        self.assertEqual(g.tick()[0], "published-now")
        self.assertEqual(len(self.calls), 1)

    def test_roll_only_redraws_an_old_forbidden_slot(self):
        g = self.gate(5)
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "13:20", "published": False}), encoding="utf-8")
        self.now = at("2026-11-14", "12:05")
        self.assertEqual(g.tick(roll_only=True)[0], "rolled-only")
        self.assertIn(int(self.state(g)["time"][:2]) * 60 + int(self.state(g)["time"][3:]), sg.ALLOWED)

    def test_manual_publish_in_repo_sets_published(self):
        g = self.gate(5, outcome=("already", "2026-11-14-manual"))
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "12:00", "published": False}), encoding="utf-8")
        self.now = at("2026-11-14", "12:15")
        self.assertEqual(g.tick()[0], "already")
        self.assertTrue(self.state(g)["published"])

    def test_low_queue_logs_a_warning(self):
        g = self.gate(2)
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "12:00", "published": False}), encoding="utf-8")
        self.now = at("2026-11-14", "12:15")
        g.tick()
        self.assertTrue(any("WARNING: queue has 2 posts" in l for l in self.logs))

    def test_healthy_queue_logs_no_warning(self):
        g = self.gate(5)
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "12:00", "published": False}), encoding="utf-8")
        self.now = at("2026-11-14", "12:15")
        g.tick()
        self.assertFalse(any("WARNING" in l for l in self.logs))

    def test_hard_fail_blocks_later_ticks(self):
        g = self.gate(5, outcome=pn.HardFail("check red"))
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "12:00", "published": False}), encoding="utf-8")
        self.now = at("2026-11-14", "12:15")
        self.assertEqual(g.tick()[0], "failed")
        self.assertFalse(self.state(g)["published"])
        self.now = at("2026-11-14", "12:30")
        self.assertEqual(g.tick()[0], "blocked")
        self.assertEqual(len(self.calls), 1)

    def test_soft_fail_retries_next_tick(self):
        g = self.gate(5, outcome=pn.SoftFail("push rejected"))
        g.state_path.write_text(json.dumps({"date": "2026-11-14", "time": "12:00", "published": False}), encoding="utf-8")
        self.now = at("2026-11-14", "12:15")
        self.assertEqual(g.tick()[0], "failed")
        self.now = at("2026-11-14", "12:30")
        self.assertEqual(g.tick()[0], "failed")
        self.assertEqual(len(self.calls), 2)

    def test_roll_only_predraws_without_publishing(self):
        g = self.gate(5)
        g.state_path.write_text(json.dumps({"date": "2026-11-13", "time": "22:41", "published": True}), encoding="utf-8")
        self.now = at("2026-11-14", "00:05")
        self.assertEqual(g.tick(roll_only=True)[0], "rolled-only")
        st = self.state(g)
        self.assertEqual((st["date"], st["prev_time"], st["published"]), ("2026-11-14", "22:41", False))
        self.assertEqual(self.calls, [])


class LiveCheckTests(unittest.TestCase):
    """verify_live: a failing live check warns in the log, flags it, and notifies once per slug (never fails the run)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tt-live-"))
        self.logs = []
        (self.tmp / "base").mkdir()
        self.p = pn.Publisher(self.tmp / "base", self.tmp / "queue", remote="unused", live="http://127.0.0.1:9",
                              now_fn=lambda: at("2026-11-14", "14:31"), verify=False, check_cmds=[], log=self.logs.append)

    def tearDown(self):
        shutil.rmtree(str(self.tmp))

    def test_failed_live_check_warns_flags_and_notifies_once(self):
        notes = []
        with mock.patch.object(pn.urllib.request, "urlopen", side_effect=urllib.error.URLError("boom")), \
                mock.patch.object(pn.time, "sleep", lambda s: None), mock.patch.object(pn, "notify_mac", notes.append):
            self.assertFalse(self.p.verify_live("2026-11-14-x"))
            self.assertTrue(any("WARNING: live check failed — deploy 확인 필요" in l for l in self.logs))
            self.assertTrue((self.tmp / "base" / "LIVE_CHECK_FAILED").is_file())
            self.assertEqual(len(notes), 1)
            self.assertFalse(self.p.verify_live("2026-11-14-x"))  # same slug again: no second notification
            self.assertEqual(len(notes), 1)
            self.assertFalse(self.p.verify_live("2026-11-15-y"))  # a new slug notifies again
            self.assertEqual(len(notes), 2)

    def test_live_ok_clears_the_flag_and_does_not_notify(self):
        notes = []
        (self.tmp / "base" / "LIVE_CHECK_FAILED").write_text("old\n", encoding="utf-8")
        resp = mock.MagicMock()
        resp.__enter__.return_value.status = 200
        with mock.patch.object(pn.urllib.request, "urlopen", return_value=resp), mock.patch.object(pn, "notify_mac", notes.append):
            self.assertTrue(self.p.verify_live("2026-11-14-x"))
        self.assertFalse((self.tmp / "base" / "LIVE_CHECK_FAILED").exists())
        self.assertEqual(notes, [])


class QueueItemTests(unittest.TestCase):
    def test_stamp_prefixes_slug_and_adds_published(self):
        out = pn.stamp(post_md("why", "en"), dt.date(2026, 11, 13), "22:40")
        meta = pn.front_meta(out)
        self.assertEqual(meta["slug"], "2026-11-13-why")
        self.assertEqual(meta["published"], "2026-11-13T22:40+09:00")
        self.assertTrue(out.endswith("body en\n"))

    def test_stamp_refuses_a_published_line(self):
        with self.assertRaises(pn.HardFail):
            pn.stamp(post_md("why", "en").replace("excerpt: E", "excerpt: E\npublished: 2026-11-01T10:00+09:00"), dt.date(2026, 11, 13), "22:40")

    def test_load_item_needs_all_languages_review_and_equal_slugs(self):
        tmp = Path(tempfile.mkdtemp(prefix="tt-item-"))
        try:
            for lang in ("en", "ko"):
                (tmp / (lang + ".md")).write_text(post_md("a", lang), encoding="utf-8")
            with self.assertRaises(pn.NotReady):
                pn.load_item(tmp)  # ten languages missing: wait, not HardFail
            for lang in pn.MAIN_LANGS:
                (tmp / (lang + ".md")).write_text(post_md("a", lang, review=(lang != "tr")), encoding="utf-8")
            with self.assertRaises(pn.NotReady):
                pn.load_item(tmp)  # tr has no copy_review
            (tmp / "tr.md").write_text(post_md("a", "tr").replace("iris 2026-11-14", "claude 2026-11-14"), encoding="utf-8")
            with self.assertRaises(pn.NotReady):
                pn.load_item(tmp)  # copy_review must be `iris YYYY-MM-DD`
            (tmp / "tr.md").write_text(post_md("b", "tr"), encoding="utf-8")
            with self.assertRaises(pn.HardFail):
                pn.load_item(tmp)  # reviewed but slugs differ
            (tmp / "tr.md").write_text(post_md("a", "tr"), encoding="utf-8")
            self.assertEqual(pn.load_item(tmp)["slug"], "a")
        finally:
            shutil.rmtree(str(tmp))

    def test_stamp_keeps_copy_review(self):
        out = pn.stamp(post_md("why", "ja"), dt.date(2026, 11, 13), "22:40")
        self.assertEqual(pn.front_meta(out)["copy_review"], "iris 2026-11-14")

    def test_main_langs_order(self):
        self.assertEqual(pn.MAIN_LANGS, ("en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr"))

    def test_check_staged_guards(self):
        pn.check_staged("A\tcontent/journal/2026-11-14-a.en.md\nM\tindex.html\nM\tko/journal/index.html\nM\tsitemap.xml\n")
        pn.check_staged("A\tcontent/journal/2026-11-14-a.pt-BR.md\nA\tcontent/journal/2026-11-14-a.zh-Hant.md\n"
                        "A\tzh-Hant/journal/2026-11-14-a/index.html\nM\tpt-BR/index.html\nM\tth/journal/feed.xml\n")
        with self.assertRaises(pn.HardFail):
            pn.check_staged("A\tcontent/journal/2026-11-14-a.xx.md\n")
        with self.assertRaises(pn.HardFail):
            pn.check_staged("M\tja/contact/index.html\n")
        with self.assertRaises(pn.HardFail):
            pn.check_staged("D\tcontent/journal/old.en.md\n")
        with self.assertRaises(pn.HardFail):
            pn.check_staged("M\tassets/site.css\n")
        with self.assertRaises(pn.HardFail):
            pn.check_staged("A\tcontent/journal/x.en.md\n", leftovers="?? stray.txt")


class PublishRoundTripTests(unittest.TestCase):
    """real git against a local bare remote; build/check/kit steps are stubbed (they are scripts/check.sh's job)."""

    def sh(self, *cmd, cwd=None):
        subprocess.run(list(cmd), cwd=str(cwd) if cwd else None, check=True, capture_output=True)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tt-rt-"))
        self.remote = self.tmp / "remote.git"
        seed = self.tmp / "seed"
        (seed / "content" / "journal").mkdir(parents=True)
        (seed / "content" / "journal" / "2026-11-10-first.en.md").write_text(
            "---\nslug: 2026-11-10-first\nlang: en\ntitle: T\ndescription: D\npublished: 2026-11-10T22:13+09:00\n---\nb\n", encoding="utf-8")
        self.sh("git", "init", "-q", str(seed))
        self.sh("git", "checkout", "-q", "-b", "main", cwd=seed)
        self.sh("git", "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A", cwd=seed)
        self.sh("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init", cwd=seed)
        self.sh("git", "clone", "-q", "--bare", str(seed), str(self.remote))
        self.queue = make_queue(self.tmp, 3)
        self.now = at("2026-11-14", "15:20")

    def tearDown(self):
        shutil.rmtree(str(self.tmp))

    def publisher(self, **kw):
        p = pn.Publisher(self.tmp / "base", self.queue, remote=str(self.remote), now_fn=lambda: self.now, verify=False,
                         check_cmds=[], log=lambda m: None, **kw)
        p.build_cmd = ["true"]
        p.ensure_kit = lambda: None
        return p

    def remote_files(self):
        out = subprocess.run(["git", "--git-dir", str(self.remote), "ls-tree", "-r", "--name-only", "main"], check=True,
                             capture_output=True, text=True).stdout
        return out.split()

    def test_publish_moves_queue_entry_and_pushes_all_languages(self):
        status, slug = self.publisher().publish_one()
        self.assertEqual((status, slug), ("published", "2026-11-14-post-1"))
        files = self.remote_files()
        self.assertIn("content/journal/2026-11-14-post-1.en.md", files)
        for lang in pn.MAIN_LANGS:
            self.assertIn("content/journal/2026-11-14-post-1.%s.md" % lang, files)
        self.assertIn("2026-11-10-first.en.md", " ".join(files))  # nothing deleted
        self.assertEqual(len(pn.queue_items(self.queue)), 2)
        self.assertTrue((self.queue / ".published" / "01-post-1").is_dir())

    def test_second_run_same_day_sees_todays_post_and_publishes_nothing(self):
        self.publisher().publish_one()
        status, slug = self.publisher().publish_one()
        self.assertEqual((status, slug), ("already", "2026-11-14-post-1"))
        self.assertEqual(len(pn.queue_items(self.queue)), 2)

    def test_empty_queue(self):
        shutil.rmtree(str(self.queue))
        self.queue.mkdir()
        self.assertEqual(self.publisher().publish_one(), ("empty", None))

    def test_unready_folders_wait_and_the_next_ready_one_goes(self):
        q = self.queue
        for lang in pn.MAIN_LANGS[2:]:  # folder 01: only en+ko -> waiting
            (q / "01-post-1" / (lang + ".md")).unlink(missing_ok=True)
        (q / "02-post-2" / "ja.md").write_text(post_md("post-2", "ja", review=False), encoding="utf-8")  # unreviewed
        logs = []
        p = self.publisher()
        p.log = logs.append
        self.assertEqual(p.publish_one(), ("published", "2026-11-14-post-3"))
        self.assertTrue(any("01-post-1" in l and "WARN" in l for l in logs))
        self.assertTrue(any("02-post-2" in l and "copy_review" in l for l in logs))
        self.assertFalse((self.tmp / "base" / "FAILED").exists())
        self.assertTrue((q / "01-post-1").is_dir() and (q / "02-post-2").is_dir())

    def test_nothing_ready_means_waiting_not_failed(self):
        for d in pn.queue_items(self.queue):
            (d / "tr.md").unlink()
        self.assertEqual(self.publisher().publish_one(), ("waiting", None))
        self.assertEqual(len(pn.queue_items(self.queue)), 3)
        self.assertNotIn("content/journal/2026-11-14-post-1.en.md", self.remote_files())

    def test_status_shows_ready_and_waiting(self):
        (self.queue / "02-post-2" / "tr.md").unlink()
        logs = []
        p = self.publisher()
        p.log = logs.append
        p.status()
        txt = "\n".join(logs)
        self.assertIn("01-post-1 -> ready", txt)
        self.assertIn("02-post-2 -> 대기 (waiting — missing tr)", txt)

    def test_dry_run_pushes_nothing_and_keeps_the_queue(self):
        self.publisher(dry_run=True).publish_one()
        self.assertNotIn("content/journal/2026-11-14-post-1.en.md", self.remote_files())
        self.assertEqual(len(pn.queue_items(self.queue)), 3)


if __name__ == "__main__":
    unittest.main()
