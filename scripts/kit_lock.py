#!/usr/bin/env python3
"""ipe_web_kit pin for this PUBLIC repo: the private kit source is never committed, only vendor/ipe_web_kit.lock (tag + commit + manifest hash).

  python3 scripts/kit_lock.py check                   vendor/ipe_web_kit/ is present, untouched and is exactly the locked kit (exit 1 if not)
  python3 scripts/kit_lock.py sync --kit <kit clone>  copy the locked tag from a local kit clone (CI: the checked-out private repo) into vendor/
  python3 scripts/kit_lock.py sync --kit <clone> --update --tag vX.Y.Z   also rewrite the lock to that tag (then run scripts/check.sh and commit the lock)
"""
import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK = "vendor/ipe_web_kit.lock"
PKG = "vendor/ipe_web_kit"
HELP = ("ipe_web_kit is missing or does not match %s. The kit is private and not in this repo -- with a local kit clone run:\n"
        "    python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit\n"
        "(CI does this with the IPE_WEB_KIT_DEPLOY_KEY secret; see README.)" % LOCK)


def read_lock(root):
    f = Path(root) / LOCK
    if not f.is_file():
        raise SystemExit("%s not found" % LOCK)
    lock = dict(l.split("=", 1) for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#"))
    for k in ("tag", "commit", "manifest_sha256"):
        if k not in lock:
            raise SystemExit("%s: missing %s" % (LOCK, k))
    return lock


def problems(root):
    """What differs between vendor/ipe_web_kit/ and the lock (empty list = OK)."""
    root = Path(root)
    lock = read_lock(root)
    pkg = root / PKG
    stamp, manifest = pkg / "KIT_VERSION", pkg / "MANIFEST.sha256"
    if not stamp.is_file() or not manifest.is_file():
        return ["%s is not installed" % PKG]
    out = []
    if stamp.read_text(encoding="utf-8").split() != [lock["tag"], lock["commit"]]:
        out.append("kit version %r differs from the lock (%s %s)" % (stamp.read_text(encoding="utf-8").strip(), lock["tag"], lock["commit"]))
    if hashlib.sha256(manifest.read_bytes()).hexdigest() != lock["manifest_sha256"]:
        out.append("kit manifest hash differs from the lock")
    if (pkg / "vendor.py").is_file():
        r = subprocess.run([sys.executable, str(pkg / "vendor.py"), "verify", str(root)], capture_output=True, text=True)
        if r.returncode:
            out.append("kit files changed after install: " + r.stderr.strip().replace("\n", "; "))
    else:
        out.append("%s/vendor.py missing" % PKG)
    return out


def sync(root, kit, update=False, tag=None):
    root, kit = Path(root), Path(kit).expanduser().resolve()
    if update:
        if not tag:
            raise SystemExit("--update needs --tag")
        lock = {"tag": tag}
    else:
        lock = read_lock(root)
    if not (kit / "ipe_web_kit" / "vendor.py").is_file():
        raise SystemExit("not an ipe_web_kit clone: %s" % kit)
    r = subprocess.run([sys.executable, "-m", "ipe_web_kit.vendor", "install", str(root), "--tag", lock["tag"], "--kit", str(kit)],
                       cwd=kit, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("kit install failed: " + (r.stderr.strip() or r.stdout.strip()))
    pkg = root / PKG
    commit = (pkg / "KIT_VERSION").read_text(encoding="utf-8").split()[1]
    msha = hashlib.sha256((pkg / "MANIFEST.sha256").read_bytes()).hexdigest()
    if update:
        old = (root / LOCK).read_text(encoding="utf-8").splitlines()
        head = [l for l in old if l.startswith("#")]
        (root / LOCK).write_text("\n".join(head + ["tag=" + tag, "commit=" + commit, "manifest_sha256=" + msha]) + "\n", encoding="utf-8")
    else:
        if commit != lock["commit"]:
            raise SystemExit("kit tag %s is commit %s, the lock wants %s -- refusing (tag moved or wrong clone)" % (lock["tag"], commit, lock["commit"]))
    bad = problems(root)
    if bad:
        raise SystemExit("; ".join(bad))
    print("ipe_web_kit %s %s: OK" % (lock["tag"], commit[:7]))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    s = sub.add_parser("sync")
    s.add_argument("--kit", required=True)
    s.add_argument("--update", action="store_true")
    s.add_argument("--tag")
    ap.add_argument("--root", default=str(ROOT))
    a = ap.parse_args(argv)
    if a.cmd == "sync":
        sync(a.root, a.kit, a.update, a.tag)
        return 0
    bad = problems(a.root)
    for b in bad:
        print("kit_lock: " + b, file=sys.stderr)
    if bad:
        print(HELP, file=sys.stderr)
        return 1
    print("ipe_web_kit: OK (matches %s)" % LOCK)
    return 0


if __name__ == "__main__":
    sys.exit(main())
