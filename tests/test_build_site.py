import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO
import build_site as bs
import check_sitemap as cs
from ipe_web_kit import langswitch, redirects


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
        # every page slug (contact) is built for every language
        for l in ctx.langs:
            for slug in bs.PAGE_SLUGS:
                if slug not in bs.REQUIRED_PAGE_SLUGS and (l, slug) not in ctx.pages:
                    continue  # privacy/terms bodies exist in 7 languages only
                rel = bs.path_page(l, slug).lstrip("/") + "index.html"
                self.assertIn(rel, files, "%s/%s" % (l, slug))

    def test_sitemap_is_consistent(self):
        errs, urls = cs.check(REPO)
        self.assertEqual(errs, [])
        self.assertTrue(urls)

    def test_releases_redirects_to_each_home(self):
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        self.assertIn('url=%s/"' % bs.SITE, files["releases/index.html"])
        self.assertIn('url=%s/ja/"' % bs.SITE, files["ja/releases/index.html"])
        self.assertNotIn("/releases/", files["sitemap.xml"])


class JournalTests(unittest.TestCase):
    """Journal posts live in content/journal/<slug>.<lang>.md (all 12 languages, each with copy_review); validate and build them."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tt-journal-"))
        self.jdir = self.tmp / "content" / "journal"
        self.jdir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _write(self, name, body, published="2026-11-10T12:00+09:00", **meta):
        lang = name.rsplit(".", 1)[0].rsplit(".", 1)[-1]  # a.en.md -> en
        meta = dict({"copy_review": "iris 2026-11-14"}, **meta)
        head = ["---", "slug: x", "lang: %s" % lang, "title: T", "description: D",
                "published: %s" % published]
        for k, v in meta.items():
            if v is None:
                continue
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

    def test_missing_copy_review_is_error(self):
        self._write("a.en.md", "body a")
        self._write("a.ko.md", "몸 a", copy_review=None)
        posts, errs = bs.load_journal(self.tmp)
        self.assertEqual(posts, [])
        self.assertTrue(any("a.ko.md: copy_review" in e for e in errs), errs)

    def test_incomplete_post_fails_publish_gate(self):
        """en + ko only: loads fine, but make_ctx refuses it (kit check_post needs all 12 languages)"""
        root = self.tmp / "site"
        shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        (root / "content" / "journal" / "2026-11-10-what-tottertop-is.tr.md").unlink()
        ctx, errs = bs.make_ctx(root)
        self.assertTrue(any("언어판 없음: tr" in e for e in errs), errs)

    def test_bad_published_format_is_error(self):
        self._write("a.en.md", "body a", published="2026-11-10T12:00")
        self._write("a.ko.md", "몸 a", published="2026-11-10T12:00")
        posts, errs = bs.load_journal(self.tmp)
        self.assertEqual(posts, [])
        self.assertTrue(any("published must be" in e for e in errs), errs)

    def test_unknown_lang_file_is_error(self):
        self._write("a.ru.md", "body")
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
        import re
        for f in sorted((root / "content" / "journal").glob("*.md")):  # every post moves to the future (the queue adds posts over time)
            f.write_text(re.sub(r"(?m)^published: \d{4}-\d{2}-\d{2}T", "published: 2027-01-01T", f.read_text(encoding="utf-8")), encoding="utf-8")
        early, errs = bs.make_ctx(root, now=dt.datetime(2026, 11, 10, 12, 0, tzinfo=bs.KST))
        self.assertEqual(errs, [])
        self.assertEqual(early.posts, [])
        files = bs.build_all(early)
        self.assertIn("noindex", files["journal/index.html"])
        self.assertNotIn(bs.SITE + "/journal/", files["sitemap.xml"])
        late, errs = bs.make_ctx(root, now=dt.datetime(2027, 1, 2, 12, 0, tzinfo=bs.KST))
        self.assertEqual(errs, [])
        self.assertEqual(len(late.posts), len(list((root / "content" / "journal").glob("*.en.md"))))

    def test_journal_built_in_all_languages(self):
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        slug = "2026-11-10-what-tottertop-is"
        for l in bs.LANGS:
            base = bs.lp(l).lstrip("/") + "/" if l != "en" else ""
            for rel in (base + "journal/index.html", base + "journal/feed.xml", base + "journal/%s/index.html" % slug):
                self.assertIn(rel, files)
        post = files["ja/journal/%s/index.html" % slug]
        self.assertIn('"inLanguage":"ja"', post)
        self.assertEqual(len(re.findall(r'rel="alternate" hreflang="', post)), 13)  # 12 + x-default
        self.assertIn('hreflang="x-default" href="%s/journal/%s/"' % (bs.SITE, slug), post)
        sm = files["sitemap.xml"]
        self.assertEqual(sm.count("<loc>%s/pt-BR/journal/%s/</loc>" % (bs.SITE, slug)), 1)


class HeaderFooterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctx = bs.make_ctx(REPO, require_all=True)[0]
        cls.files = bs.build_all(cls.ctx)

    def _block(self, text, tag, cls):
        m = re.search(r'<%s class="%s".*?</%s>' % (tag, cls, tag), text, re.S)
        self.assertIsNotNone(m, "%s.%s missing" % (tag, cls))
        return m.group(0)

    def test_nav_has_no_legal_links(self):
        for l in self.ctx.langs:
            nav = self._block(self.files[bs.path_home(l).lstrip("/") + "index.html"], "nav", "nav")
            for slug in ("privacy", "terms"):
                self.assertNotIn("/%s/" % slug, nav, "%s nav links %s" % (l, slug))

    def test_footer_links_privacy_terms_to_built_pages(self):
        for l in self.ctx.langs:
            footer = self._block(self.files[bs.path_home(l).lstrip("/") + "index.html"], "footer", "site-footer")
            for slug in ("privacy", "terms"):
                want = bs.path_page(l if (l, slug) in self.ctx.pages else "en", slug)
                self.assertIn('href="%s"' % want, footer, "%s footer links %s" % (l, slug))
                self.assertIn(want.lstrip("/") + "index.html", self.files)

    def test_language_select_has_all_languages_and_current_selected(self):
        for l in self.ctx.langs:
            page = self.files[bs.path_home(l).lstrip("/") + "index.html"]
            header = self._block(page, "div", "tools")
            self.assertEqual(header.count("<select"), 1)
            sel = re.search(r'<select class="ipe-lang__select"[^>]*>(.*?)</select>', header, re.S)
            self.assertIsNotNone(sel)
            opts = re.findall(r'<option value="([^"]+)" lang="([^"]+)"( selected)?>', sel.group(1))
            self.assertEqual(len(opts), 12)
            self.assertEqual({o[1] for o in opts}, set(bs.LANGS))
            self.assertEqual([o[1] for o in opts if o[2]], [l])
            for value, _, _ in opts:
                self.assertIn(value.lstrip("/") + "index.html", self.files, value)
            self.assertIn('<noscript><nav class="ipe-lang__links"', header)

    def test_footer_has_no_language_switch(self):
        for l in self.ctx.langs:
            footer = self._block(self.files[bs.path_home(l).lstrip("/") + "index.html"], "footer", "site-footer")
            self.assertNotIn("<select", footer)
            self.assertNotIn("ipe-lang", footer)

    def test_detection_script_on_root_home_only(self):
        self.assertIn('<script src="%s" data-redirect defer></script>' % bs.LANG_JS, self.files["index.html"])
        for rel, text in self.files.items():
            if rel.endswith(".html") and rel != "index.html" and not rel.split("/")[0] in redirects.LEGACY_REDIRECTS:
                self.assertNotIn("ipe-lang.js", text, rel)
        self.assertEqual((REPO / "assets" / "ipe-lang.js").read_bytes(), langswitch.JS.read_bytes())

    def test_legacy_language_urls_redirect_and_stay_out_of_sitemap(self):
        self.assertIn('url=%s/pt-BR/"' % bs.SITE, self.files["pt/index.html"])
        self.assertIn('url=%s/zh-Hant/contact/"' % bs.SITE, self.files["zh/contact/index.html"])
        self.assertIn('url=%s/journal/"' % bs.SITE, self.files["ru/journal/index.html"])
        self.assertEqual(redirects.sitemap_leaks(self.files["sitemap.xml"]), [])

    def test_hreflang_links_kept(self):
        head = self.files["index.html"].split("</head>")[0]
        self.assertEqual(len(re.findall(r'rel="alternate" hreflang="[^"]+"', head)), len(bs.LANGS) + 1)

    def test_journal_json_ld_parses(self):
        pages = [f for f in self.files if f.endswith(".html")]
        for f in pages:
            for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.files[f], re.S):
                json.loads(block.replace("<\\/", "</"))


if __name__ == "__main__":
    unittest.main()
