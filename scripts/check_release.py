#!/usr/bin/env python3
"""Release-notes gate for the web — the app's deploy_ios.sh calls this before upload.

It reads content/pages/<lang>/changelog.md (langs come from games.json) and checks the
build notes titled "## <version> (N) — <date>". Date entries ("## YYYY-MM-DD — …") are
part of the page, not build notes — they are ignored.

Usage
  python3 scripts/check_release.py --build 2           # the build 2 note
  python3 scripts/check_release.py --build 1.0.0+2     # same, version pinned
  python3 scripts/check_release.py --build 2 --latest  # + no build heading newer than 2
  python3 scripts/check_release.py --all               # every build note passes checks 1-4

Checks (--build N):
  1. exactly one "## <version> (N) — <date>" heading in every language
  2. the heading's version and date agree across languages
  3. at least one "- " item under the heading, and no empty items
  4. every language has as many items as en (missing-translation guard)
  --latest: no build heading with a bigger number than N in any language (app = TF = notes)
  --all:    every build heading satisfies checks 1-4

Stdlib only. Exit 0 = pass. Otherwise one line per problem, exit 1.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# "## 1.0.0 (2) — 2026-11-11": version, build number in parens, em dash, KST date
HEADING_RE = re.compile(r"^## (\d+\.\d+\.\d+) \((\d+)\) — (\d{4}-\d{2}-\d{2})\s*$")
HEADING_ANY_RE = re.compile(r"^#{1,6}\s")
# a bullet: "- text"; a bare "-" (after strip) is an empty item
ITEM_RE = re.compile(r"^-(?:\s+(.*))?$")


def langs_of(root):
    g = json.loads((root / "games.json").read_text(encoding="utf-8"))
    return g["langs"]


def parse_changelog(text):
    """Build notes in one changelog: list of (version, build, date, [item, ...])."""
    notes, current = [], None
    for raw in text.splitlines():
        line = raw.rstrip()
        m = HEADING_RE.match(line)
        if m:
            current = [m.group(1), int(m.group(2)), m.group(3), []]
            notes.append(current)
            continue
        if HEADING_ANY_RE.match(line.strip()):
            current = None  # any other heading (date entries, page title) ends the section
            continue
        s = line.strip()
        if current is None or not s:
            continue
        m = ITEM_RE.match(s)
        if m:
            current[3].append((m.group(1) or "").strip())
    return notes


def changelog_path(root, lang):
    return root / "content" / "pages" / lang / "changelog.md"


def check_build(root, build, version=None, latest=False):
    """Checks 1-4 for one build number (+5 with latest). Returns a list of problem lines."""
    errs = []
    langs = langs_of(root)
    label = "%s (%d)" % (version, build) if version else "build %d" % build
    found = {}
    for lang in langs:
        f = changelog_path(root, lang)
        if not f.exists():
            errs.append("%s: changelog.md is missing" % lang)
            continue
        targets = [n for n in parse_changelog(f.read_text(encoding="utf-8"))
                   if n[1] == build and (version is None or n[0] == version)]
        if not targets:
            errs.append("%s: no note titled '## <version> (%d) — <date>'" % (lang, build))
        elif len(targets) > 1:
            errs.append("%s: the %s heading appears %d times, expected 1" % (lang, label, len(targets)))
        else:
            found[lang] = targets[0]

    if not found:
        return errs

    versions = {n[0] for n in found.values()}
    if version is not None and versions != {version}:
        errs.append("version: expected %s, found %s" % (version, ", ".join(sorted(versions))))
    elif len(versions) > 1:
        errs.append("version: %s disagree across languages" % ", ".join(sorted(versions)))
    dates = {n[2] for n in found.values()}
    if len(dates) > 1:
        errs.append("date: %s disagree across languages" % ", ".join(sorted(dates)))

    counts = {}
    for lang in sorted(found):
        items = found[lang][3]
        if not items:
            errs.append("%s: no '- ' items under the %s heading" % (lang, label))
        for i, it in enumerate(items, 1):
            if not it:
                errs.append("%s: item %d under %s is empty" % (lang, i, label))
        counts[lang] = len(items)
    if "en" in counts:
        for lang in sorted(counts):
            if lang != "en" and counts[lang] != counts["en"]:
                errs.append("%s: %d items, en has %d — translate the missing ones"
                            % (lang, counts[lang], counts["en"]))

    if latest:
        for lang in langs:
            f = changelog_path(root, lang)
            if not f.exists():
                continue
            bigger = [n[1] for n in parse_changelog(f.read_text(encoding="utf-8")) if n[1] > build]
            if bigger:
                errs.append("%s: build %d note is newer than build %d"
                            % (lang, max(bigger), build))
    return errs


def check_all(root):
    """Checks 1-4 for every build heading present in any changelog."""
    langs = langs_of(root)
    pairs = set()
    texts = {}
    for lang in langs:
        f = changelog_path(root, lang)
        if not f.exists():
            return ["%s: changelog.md is missing" % lang]
        notes = parse_changelog(f.read_text(encoding="utf-8"))
        texts[lang] = notes
        pairs.update((n[0], n[1]) for n in notes)
    errs = []
    for version, build in sorted(pairs, key=lambda p: (p[1], p[0])):
        errs.extend(check_build(root, build, version=version, latest=False))
    return errs


def parse_build_spec(s):
    m = re.fullmatch(r"(\d+\.\d+\.\d+)\+(\d+)", s)
    if m:
        return m.group(1), int(m.group(2))
    if s.isdigit():
        return None, int(s)
    raise argparse.ArgumentTypeError("expected a build number (2) or version+build (1.0.0+2), got %r" % s)


def main(argv=None):
    ap = argparse.ArgumentParser(description="check the web release notes (called by deploy_ios.sh)")
    ap.add_argument("--build", type=parse_build_spec, metavar="N", help="build to check: 2 or 1.0.0+2")
    ap.add_argument("--latest", action="store_true", help="with --build: also fail if any newer build heading exists")
    ap.add_argument("--all", action="store_true", help="check every build heading (web check.sh)")
    ap.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    errs = []
    if a.all:
        errs = check_all(a.root)
        what = "all build notes"
    elif a.build:
        version, build = a.build
        errs = check_build(a.root, build, version=version, latest=a.latest)
        what = "%s%s" % (version + " " if version else "", build)
        if a.latest:
            what += " (latest)"
    else:
        ap.error("one of --build N / --all is required")

    if errs:
        for e in errs:
            print("check_release: %s" % e)
        return 1
    print("check_release: ok (%s)" % what)
    return 0


if __name__ == "__main__":
    sys.exit(main())
