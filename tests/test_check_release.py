import json
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO
import check_release as cr

LANGS = ["ko", "en", "ja", "zh", "es", "fr", "de", "pt", "ru", "ar", "hi"]


def entry(build, en_items=3, ko_items=3, ko_text="새 빌드입니다."):
    notes = {l: ["Item %d." % i for i in range(en_items)] for l in LANGS}
    notes["ko"] = [ko_text] + [("항목 %d입니다." % i) for i in range(1, ko_items)]
    return {"id": "1.0.0-%s" % build, "version": "1.0.0", "build": str(build), "status": "testflight",
            "date": "2026-11-11", "notes": notes}


def make_root(tmp, releases):
    (tmp / "content").mkdir(parents=True, exist_ok=True)
    (tmp / "content" / "releases.json").write_text(json.dumps({"releases": releases}, ensure_ascii=False), encoding="utf-8")
    (tmp / "games.json").write_text(json.dumps({"langs": LANGS}), encoding="utf-8")
    return tmp


class ParseSpecTests(unittest.TestCase):
    def test_bare_number(self):
        self.assertEqual(cr.parse_build_spec("2"), (None, "2"))

    def test_version_plus_build(self):
        self.assertEqual(cr.parse_build_spec("1.0.0+2"), ("1.0.0", "2"))

    def test_bad_spec(self):
        with self.assertRaises(Exception):
            cr.parse_build_spec("1.0.0+2+3")


class CheckReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tt-release-"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def root(self, *releases):
        return make_root(self.tmp, list(releases))

    def test_real_repo_passes(self):
        self.assertEqual(cr.main(["--all", "--root", str(REPO)]), 0)
        self.assertEqual(cr.main(["--build", "2", "--latest", "--root", str(REPO)]), 0)
        self.assertEqual(cr.main(["--build", "1.0.0+1", "--root", str(REPO)]), 0)

    def test_ok_root(self):
        r = self.root(entry(1), entry(2))
        self.assertEqual(cr.check(r, all_builds=True), [])
        self.assertEqual(cr.check(r, build="2", latest=True), [])

    def test_missing_build(self):
        r = self.root(entry(1))
        self.assertEqual(cr.main(["--build", "9", "--root", str(r)]), 1)

    def test_latest_fails_when_newer_build_exists(self):
        r = self.root(entry(1), entry(2))
        errs = cr.check(r, build="1", latest=True)
        self.assertTrue(any("newer than build 1" in e for e in errs), errs)

    def test_banned_internal_word_is_an_error(self):
        bad = entry(3, ko_text="내부 TestFlight 빌드입니다.")
        errs = cr.check(self.root(bad), all_builds=True)
        self.assertTrue(any("RN08" in e and "ko" in e for e in errs), errs)
        self.assertEqual(cr.main(["--all", "--root", str(self.root(bad))]), 1)


if __name__ == "__main__":
    unittest.main()
