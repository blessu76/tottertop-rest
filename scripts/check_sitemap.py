#!/usr/bin/env python3
"""Check sitemap.xml against the built site — stdlib only. Exit 1 on any problem.

  python3 scripts/check_sitemap.py            # offline checks
  python3 scripts/check_sitemap.py --live     # + every URL answers HTTP 200 (run after deploy)

Offline checks
  1. sitemap.xml is valid XML and every <loc> is on the game domain (games.json).
  2. every <loc> has a file on disk (index.html of that path).
  3. (reserved)
  4. home + every page in PAGE_SLUGS exist for every language that has a home page.
  5. hreflang: lists itself + x-default, every target is itself in the sitemap, references are reciprocal.
  6. no <lastmod> or post time is in the future.
"""
import argparse
import datetime as dt
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site as bs  # noqa: E402

NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}


def check(root, now=None):
    root = Path(root)
    now = now or dt.datetime.now(bs.KST)
    errs = []
    try:
        tree = ET.parse(root / "sitemap.xml")
    except (ET.ParseError, OSError) as ex:
        return ["sitemap.xml: %s" % ex], []
    urls, lastmod = {}, {}
    for u in tree.getroot().findall("s:url", NS):
        loc = (u.findtext("s:loc", namespaces=NS) or "").strip()
        urls[loc] = [(l.get("hreflang"), l.get("href")) for l in u.findall("x:link", NS)]
        lastmod[loc] = (u.findtext("s:lastmod", namespaces=NS) or "").strip()
    want = set()
    for u in sorted(urls):
        if not u.startswith(bs.SITE + "/"):
            errs.append("not an %s URL: %s" % (bs.SITE, u)); continue
        if not (root / u[len(bs.SITE) + 1:] / "index.html").is_file():
            errs.append("no file for sitemap URL: %s" % u)
        if lastmod[u] > now.strftime("%Y-%m-%d"):
            errs.append("lastmod in the future: %s %s" % (u, lastmod[u]))
    homes = [l for l in bs.LANGS if bs.url(bs.path_home(l)) in urls]
    for l in homes:
        for path in tuple(bs.path_page(l, p) for p in bs.PAGE_SLUGS):
            if bs.url(path) not in urls:
                errs.append("missing from sitemap: %s" % bs.url(path))
    for loc, links in urls.items():
        if not links:
            continue
        langs = [l for l, _ in links]
        if len(set(langs)) != len(langs):
            errs.append("%s: duplicate hreflang" % loc)
        if "x-default" not in langs:
            errs.append("%s: no x-default" % loc)
        mine = [l for l, h in links if h == loc]
        if not mine:
            errs.append("%s: does not list itself in hreflang" % loc)
        for lang, href in links:
            if href not in urls:
                errs.append("%s: hreflang %s -> %s is not in the sitemap" % (loc, lang, href))
            elif lang != "x-default" and href != loc and mine and (mine[0], loc) not in urls[href]:
                errs.append("%s: hreflang %s -> %s is not reciprocal" % (loc, lang, href))
    return errs, list(urls)


def live(urls):
    errs = []
    for u in urls:
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "check_sitemap/1"}), timeout=20) as r:
                if r.status != 200:
                    errs.append("HTTP %s: %s" % (r.status, u))
        except Exception as ex:  # noqa: BLE001
            errs.append("%s: %s" % (u, ex))
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--live", action="store_true")
    a = ap.parse_args(argv)
    errs, urls = check(Path(a.root).resolve())
    if a.live and not errs:
        errs += live(urls)
    if errs:
        print("sitemap: %d problem(s)\n  " % len(errs) + "\n  ".join(errs), file=sys.stderr)
        return 1
    print("sitemap: OK — %d URL(s)%s" % (len(urls), ", all HTTP 200" if a.live else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
