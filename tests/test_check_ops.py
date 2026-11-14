"""ops/check_ops.py: detects a missing launchd job, a thin queue and publisher flag files; load_item length limits."""
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import REPO
from test_slot_gate import make_queue, post_md

sys.path.insert(0, str(REPO / "ops"))
sys.path.insert(0, str(REPO / "scripts"))
import check_ops as co  # noqa: E402
import publish_next as pn  # noqa: E402
import build_site as bs  # noqa: E402

LOADED = "-\t0\t%s\n123\t0\tcom.other\n" % co.LABEL


class CheckOpsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.base = self.root / "base"
        self.base.mkdir()
        self.plist = self.root / "x.plist"
        self.plist.write_text("<plist/>")

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self, q, out=LOADED, plist=None):
        return co.check(q, self.base, plist or self.plist, out)

    def test_healthy(self):
        self.assertEqual(self.run_check(make_queue(self.root, 3)), [])

    def test_launchd_not_loaded_and_plist_missing(self):
        p = self.run_check(make_queue(self.root, 3), out="123\t0\tcom.other\n", plist=self.root / "missing.plist")
        self.assertEqual(len(p), 2)
        self.assertTrue(any("not installed" in x for x in p) and any("not loaded" in x for x in p))

    def test_label_match_is_exact(self):
        self.assertTrue(co.launchd_loaded("-\t0\t%s.old\n" % co.LABEL) is False)

    def test_queue_below_three_is_flagged(self):
        p = self.run_check(make_queue(self.root, 2))
        self.assertEqual(len(p), 1)
        self.assertIn("2 publishable", p[0])

    def test_en_ko_only_folders_do_not_count_and_show_why(self):
        q = make_queue(self.root, 3)
        for lang in pn.MAIN_LANGS[2:]:
            (q / "03-post-3" / (lang + ".md")).unlink()
        p = self.run_check(q)
        self.assertEqual(len(p), 1)
        self.assertIn("03-post-3", p[0])
        self.assertIn("missing", p[0])

    def test_flag_files(self):
        (self.base / "FAILED").write_text("t\nboom\n")
        p = self.run_check(make_queue(self.root, 3))
        self.assertTrue(any("FAILED flag" in x and "boom" in x for x in p))

    def test_too_long_title_waits_instead_of_failing(self):
        q = make_queue(self.root, 3)
        f = q / "01-post-1" / "de.md"
        f.write_text(post_md("post-1", "de", "x" * 61), encoding="utf-8")
        with self.assertRaises(pn.NotReady):
            pn.load_item(q / "01-post-1")
        self.assertEqual(len(self.run_check(q)), 1)

    def test_limits_mirror_the_build(self):
        self.assertEqual(pn.LIMITS, {"title": bs.TITLE_MAX, "description": bs.DESC_MAX, "excerpt": bs.EXCERPT_MAX})


if __name__ == "__main__":
    unittest.main()
