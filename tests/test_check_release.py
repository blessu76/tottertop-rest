import json
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO
import check_release as cr

BUILD = "## 1.0.0 (%d) — 2026-11-11"


def note(build, n_items=1, item="An item.", extra=""):
    return BUILD % build + "\n" + "".join("- %s\n" % item for _ in range(n_items)) + extra


def make_repo(tmp, en_body, ko_body, langs=("en", "ko")):
    (tmp / "content" / "pages").mkdir(parents=True, exist_ok=True)
    for lang in langs:
        d = tmp / "content" / "pages" / lang
        d.mkdir(exist_ok=True)
        (d / "changelog.md").write_text(
            ("---\ntitle: Release notes\n---\n%s\n\n## 2026-11-09 — A date entry\n- kept as is\n" %
             (en_body if lang == "en" else ko_body)),
            encoding="utf-8")
    (tmp / "games.json").write_text(json.dumps({"langs": list(langs)}), encoding="utf-8")
    return tmp


class ParseSpecTests(unittest.TestCase):
    def test_bare_number(self):
        self.assertEqual(cr.parse_build_spec("2"), (None, 2))

    def test_version_plus_build(self):
        self.assertEqual(cr.parse_build_spec("1.0.0+2"), ("1.0.0", 2))

    def test_bad_spec(self):
        with self.assertRaises(Exception):
            cr.parse_build_spec("1.0.0+2+3")


class CheckReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tt-release-"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def repo(self, en_body, ko_body=None):
        ko_body = en_body if ko_body is None else ko_body
        return make_repo(self.tmp, en_body, ko_body)

    def ok_repo(self):
        body = note(1) + "\n" + note(2, 2)
        return self.repo(body, body)

    def test_pass_on_repo(self):
        self.assertEqual(cr.check_build(self.ok_repo(), 1), [])
        self.assertEqual(cr.check_build(self.ok_repo(), 2), [])
        self.assertEqual(cr.check_build(self.ok_repo(), 2, version="1.0.0"), [])
        self.assertEqual(cr.check_all(self.ok_repo()), [])

    def test_real_repo_passes(self):
        self.assertEqual(cr.check_build(REPO, 1, version="1.0.0"), [])
        self.assertEqual(cr.check_build(REPO, 2, version="1.0.0"), [])
        self.assertEqual(cr.check_all(REPO), [])
        self.assertEqual(cr.check_build(REPO, 2, version="1.0.0", latest=True), [])

    def test_missing_note_in_one_language(self):
        r = self.repo(note(2, 2), note(1))  # ko has no build 2
        errs = cr.check_build(r, 2)
        self.assertTrue(any("ko:" in e and "no note" in e for e in errs), errs)

    def test_duplicate_heading(self):
        body = note(2) + "\n" + note(2)
        errs = cr.check_build(self.repo(body, body), 2)
        self.assertTrue(any("en:" in e and "appears 2 times" in e for e in errs), errs)
        self.assertTrue(any("ko:" in e and "appears 2 times" in e for e in errs), errs)

    def test_version_mismatch(self):
        ko = "## 2.0.0 (2) — 2026-11-11\n- An item.\n"
        errs = cr.check_build(self.repo(note(2, 2), ko), 2)
        self.assertTrue(any("version" in e and "1.0.0" in e and "2.0.0" in e for e in errs), errs)

    def test_date_mismatch(self):
        ko = "## 1.0.0 (2) — 2026-11-10\n- An item.\n- Another.\n"
        errs = cr.check_build(self.repo(note(2, 2), ko), 2)
        self.assertTrue(any("date" in e for e in errs), errs)

    def test_no_items(self):
        errs = cr.check_build(self.repo("## 1.0.0 (2) — 2026-11-11\n", note(2, 2)), 2)
        self.assertTrue(any("en:" in e and "no '- ' items" in e for e in errs), errs)

    def test_empty_item(self):
        body = note(2, 2, item="")  # "- \n- An item."
        errs = cr.check_build(self.repo(body, note(2, 2)), 2)
        self.assertTrue(any("en:" in e and "empty" in e for e in errs), errs)

    def test_item_count_must_match_en(self):
        ko = note(2, 3)  # en has 2, ko has 3
        errs = cr.check_build(self.repo(note(2, 2), ko), 2)
        self.assertTrue(any("ko:" in e and "en has 2" in e for e in errs), errs)

    def test_date_entries_are_ignored(self):
        body = note(2) + "\n## 2026-11-09 — Something else\n- old item\n"
        self.assertEqual(cr.check_build(self.repo(body, body), 2), [])

    def test_latest_pass_and_fail(self):
        r = self.ok_repo()  # builds 1 and 2
        self.assertEqual(cr.check_build(r, 2, latest=True), [])
        # building 1 while a build 2 note exists means the notes run ahead — must fail
        errs = cr.check_build(r, 1, latest=True)
        self.assertTrue(any("newer than build 1" in e for e in errs), errs)
        bigger = note(3) + "\n" + note(2, 2)
        r2 = self.repo(bigger, bigger)
        errs = cr.check_build(r2, 2, latest=True)
        self.assertTrue(any("build 3 note is newer" in e for e in errs), errs)

    def test_all_flags_a_bad_note(self):
        r = self.ok_repo()
        self.assertEqual(cr.check_all(r), [])
        bad_ko = note(1) + "\n" + note(2, 3)  # ko build 2 has 3 items, en has 2
        r2 = self.repo(note(1) + "\n" + note(2, 2), bad_ko)
        errs = cr.check_all(r2)
        self.assertTrue(any("ko:" in e and "en has 2" in e for e in errs), errs)

    def test_main_exit_codes(self):
        r = self.ok_repo()
        self.assertEqual(cr.main(["--build", "2", "--root", str(r)]), 0)
        self.assertEqual(cr.main(["--build", "1.0.0+2", "--latest", "--root", str(r)]), 0)
        self.assertEqual(cr.main(["--all", "--root", str(r)]), 0)
        self.assertEqual(cr.main(["--build", "9", "--root", str(r)]), 1)


if __name__ == "__main__":
    unittest.main()
