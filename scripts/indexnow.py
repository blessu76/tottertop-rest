#!/usr/bin/env python3
"""Notify IndexNow (Bing, Naver, Yandex, ...) about new or changed URLs — the logic lives in the web kit
(ipe_web_kit/indexnow.py; the private kit is installed from vendor/ipe_web_kit.lock by scripts/kit_lock.py).

Run AFTER the site is published (the key file must already be live):

    python3 scripts/indexnow.py                 # every <loc> in sitemap.xml
    python3 scripts/indexnow.py URL [URL ...]   # only these URLs
    python3 scripts/indexnow.py --today         # only <loc> whose <lastmod> is today (KST)
    python3 scripts/indexnow.py --dry-run       # print the payload, send nothing

The key is the repo-root file named <32 hex>.txt whose single line is the key
itself. It is a public file (not a secret). Standard library only.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "vendor"))
try:
    from ipe_web_kit import indexnow as _kit  # noqa: E402
    from ipe_web_kit.indexnow import ENDPOINT, build_payload, find_key, send, sitemap_urls  # noqa: E402,F401
except ImportError:
    sys.exit("ipe_web_kit is not installed (private, not in this repo). Run: python3 scripts/kit_lock.py sync --kit <local ipe_web_kit clone>")


def main(argv=None):
    # send is looked up here at call time, so tests can swap indexnow.send
    return _kit.main(argv, root=ROOT, sender=lambda payload: send(payload))


if __name__ == "__main__":
    sys.exit(main())
