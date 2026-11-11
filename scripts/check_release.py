#!/usr/bin/env python3
"""Release-notes gate for the web — the app's deploy_ios.sh calls this before upload.

Reads content/releases.json (the site's release list) and runs the ipe_web_kit release lint on it:
required languages ko + en, the kit's rules (length, item count, banned words, Korean endings),
and a warning for any language still missing a translation.

Usage
  python3 scripts/check_release.py --build 2           # the build 2 entry
  python3 scripts/check_release.py --build 1.0.0+2     # same, version pinned
  python3 scripts/check_release.py --build 2 --latest  # + no build newer than 2
  python3 scripts/check_release.py --all               # every build entry (web check.sh)

Exit 0 = pass (warnings are printed). Exit 1 = at least one error.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "vendor"))
from ipe_web_kit import releases  # noqa: E402

RELEASES_FILE = "content/releases.json"
REQUIRED_LANGS = ["ko", "en"]


def parse_build_spec(s):
    m = re.fullmatch(r"(\d+\.\d+\.\d+)\+(\d+)", s)
    if m:
        return m.group(1), m.group(2)
    if s.isdigit():
        return None, s
    raise argparse.ArgumentTypeError("expected a build number (2) or version+build (1.0.0+2), got %r" % s)


def site_langs(root):
    return json.loads((root / "games.json").read_text(encoding="utf-8"))["langs"]


def check(root, build=None, version=None, latest=False, all_builds=False):
    site = releases.load_site(root / RELEASES_FILE)
    probs = releases.lint_site(site, REQUIRED_LANGS, build=build, check_all=all_builds,
                               site_langs=site_langs(root))
    errs = ["%s %s: %s" % (p.code, p.lang or "", p.msg) for p in probs if p.level == "error"]
    if build is not None:
        match = [r for r in site.releases if r.build == build and (version is None or r.version == version)]
        if not match:
            errs.append("build %s%s is not in %s" % (version + " " if version else "", build, RELEASES_FILE))
        if latest:
            newer = [r.build for r in site.releases if int(r.build) > int(build)]
            if newer:
                errs.append("build %s is newer than build %s" % (max(newer, key=int), build))
    for p in probs:
        if p.level != "error":
            print("WARN %s %s: %s" % (p.code, p.lang or "", p.msg))
    for e in errs:
        print("ERROR %s" % e)
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description="check the web release notes (called by deploy_ios.sh)")
    ap.add_argument("--build", type=parse_build_spec, metavar="N", help="build to check: 2 or 1.0.0+2")
    ap.add_argument("--latest", action="store_true", help="with --build: also fail if any newer build exists")
    ap.add_argument("--all", action="store_true", help="check every build (web check.sh)")
    ap.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    if a.all:
        what = "all builds"
        errs = check(a.root, all_builds=True)
    elif a.build:
        version, build = a.build
        what = "%s%s" % (version + " " if version else "", build) + (" (latest)" if a.latest else "")
        errs = check(a.root, build=build, version=version, latest=a.latest)
    else:
        ap.error("one of --build N / --all is required")

    if errs:
        print("check_release: FAIL (%s) — %d error(s)" % (what, len(errs)))
        return 1
    print("check_release: ok (%s)" % what)
    return 0


if __name__ == "__main__":
    sys.exit(main())
