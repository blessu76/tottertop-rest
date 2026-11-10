import json
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO
import build_site as bs
import check_sitemap as cs


class SiteTests(unittest.TestCase):
    def test_games_json_drives_names(self):
        g = json.loads((REPO / "games.json").read_text(encoding="utf-8"))
        self.assertEqual(bs.DOMAIN, g["domain"])
        self.assertEqual((REPO / "CNAME").read_text().strip(), g["domain"])

    def test_all_languages_complete(self):
        ctx = bs.make_ctx(REPO, require_all=True)[0]
        self.assertEqual(set(ctx.langs), set(bs.LANGS))

    def test_build_has_required_files(self):
        ctx = bs.make_ctx(REPO, require_all=True)[0]
        files = bs.build_all(ctx)
        for want in ("index.html", "404.html", "sitemap.xml", "robots.txt", "llms.txt"):
            self.assertIn(want, files)
        # every page slug (contact + changelog) is built for every language
        for l in ctx.langs:
            for slug in bs.PAGE_SLUGS:
                rel = bs.path_page(l, slug).lstrip("/") + "index.html"
                self.assertIn(rel, files, "%s/%s" % (l, slug))

    def test_sitemap_is_consistent(self):
        errs, urls = cs.check(REPO)
        self.assertEqual(errs, [])
        self.assertTrue(urls)

    def test_changelog_in_nav_and_footer(self):
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        h = files["index.html"]
        self.assertIn('href="/changelog/"', h)


class JournalTests(unittest.TestCase):
    """Journal posts are en+ko pairs in content/journal/<slug>.<lang>.md; validate and build them."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tt-journal-"))
        self.jdir = self.tmp / "content" / "journal"
        self.jdir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _write(self, name, body, published="2026-11-10T12:00+09:00", **meta):
        lang = name.rsplit(".", 1)[0].rsplit(".", 1)[-1]  # a.en.md -> en
        head = ["---", "slug: x", "lang: %s" % lang, "title: T", "description: D",
                "published: %s" % published]
        for k, v in meta.items():
            head.append("%s: %s" % (k, v))
        head.append("---")
        (self.jdir / name).write_text("\n".join(head + ["", body]), encoding="utf-8")

    def test_pair_ok_and_newest_first(self):
        self._write("a.en.md", "body a")
        self._write("a.ko.md", "몸 a")
        self._write("b.en.md", "body b", published="2026-11-11T12:00+09:00")
        self._write("b.ko.md", "몸 b", published="2026-11-11T12:00+09:00")
        posts, errs = bs.load_journal(self.tmp)
        self.assertEqual(errs, [])
        self.assertEqual([p["slug"] for p in posts], ["b", "a"])

    def test_missing_ko_is_error(self):
        self._write("a.en.md", "body a")
        posts, errs = bs.load_journal(self.tmp)
        self.assertEqual(posts, [])
        self.assertTrue(any("missing the ko version" in e for e in errs), errs)

    def test_mismatched_published_is_error(self):
        self._write("a.en.md", "body a", published="2026-11-10T12:00+09:00")
        self._write("a.ko.md", "몸 a", published="2026-11-10T13:00+09:00")
        posts, errs = bs.load_journal(self.tmp)
        self.assertEqual(posts, [])
        self.assertTrue(any("same published time" in e for e in errs), errs)

    def test_bad_published_format_is_error(self):
        self._write("a.en.md", "body a", published="2026-11-10T12:00")
        self._write("a.ko.md", "몸 a", published="2026-11-10T12:00")
        posts, errs = bs.load_journal(self.tmp)
        self.assertEqual(posts, [])
        self.assertTrue(any("published must be" in e for e in errs), errs)

    def test_non_journal_lang_file_is_error(self):
        self._write("a.ja.md", "body")
        posts, errs = bs.load_journal(self.tmp)
        self.assertEqual(posts, [])
        self.assertTrue(any("file name must be" in e for e in errs), errs)

    def test_reserved_slug_feed_is_error(self):
        (self.jdir / "feed.en.md").write_text(
            "---\nslug: feed\nlang: en\ntitle: T\ndescription: D\npublished: 2026-11-10T12:00+09:00\n---\nbody", encoding="utf-8")
        (self.jdir / "feed.ko.md").write_text(
            "---\nslug: feed\nlang: ko\ntitle: T\ndescription: D\npublished: 2026-11-10T12:00+09:00\n---\n몸", encoding="utf-8")
        posts, errs = bs.load_journal(self.tmp)
        self.assertEqual(posts, [])
        self.assertTrue(any("must be lowercase" in e for e in errs), errs)

    def test_h1_in_body_is_error(self):
        self._write("a.en.md", "# A heading")
        self._write("a.ko.md", "# 제목")
        posts, errs = bs.load_journal(self.tmp)
        self.assertEqual(posts, [])
        self.assertTrue(any("must not contain a '# ' heading" in e for e in errs), errs)

    def _repo_copy(self):
        root = self.tmp / "site"
        shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return root

    def test_empty_journal_is_noindex_and_out_of_sitemap(self):
        root = self._repo_copy()
        shutil.rmtree(root / "content" / "journal", ignore_errors=True)
        ctx, errs = bs.make_ctx(root)
        self.assertEqual(errs, [])
        files = bs.build_all(ctx)
        self.assertIn("noindex", files["journal/index.html"])
        self.assertIn("noindex", files["ko/journal/index.html"])
        self.assertNotIn(bs.SITE + "/journal/", files["sitemap.xml"])
        self.assertNotIn(bs.SITE + "/ko/journal/", files["sitemap.xml"])

    def test_future_post_is_gated_by_make_ctx(self):
        """a post dated after `now` (KST) is validated but published nowhere"""
        import datetime as dt
        root = self._repo_copy()
        for f in sorted((root / "content" / "journal").glob("*.md")):
            f.write_text(f.read_text(encoding="utf-8").replace("2026-11-10T", "2027-01-01T"), encoding="utf-8")
        early, errs = bs.make_ctx(root, now=dt.datetime(2026, 11, 10, 12, 0, tzinfo=bs.KST))
        self.assertEqual(errs, [])
        self.assertEqual(early.posts, [])
        files = bs.build_all(early)
        self.assertIn("noindex", files["journal/index.html"])
        self.assertNotIn(bs.SITE + "/journal/", files["sitemap.xml"])
        late, errs = bs.make_ctx(root, now=dt.datetime(2027, 1, 2, 12, 0, tzinfo=bs.KST))
        self.assertEqual(errs, [])
        self.assertEqual(len(late.posts), 1)


if __name__ == "__main__":
    unittest.main()
