#!/usr/bin/env python3
"""Publish ONE queued journal post for tottertop.ipe.rest — stdlib only (Python 3.8+).

Takes the first ready entry (en + ko) from a queue that lives OUTSIDE the repo, stamps today's date into the slug and the
real publish minute (KST) into `published:`, then build -> scripts/check.sh (must be GREEN) -> commit -> push -> live 200.
Nothing is ever back-dated. The random afternoon slot lives in ops/slot_gate.py, which calls publish_one() here.

  python3 ops/publish_next.py --status    # queue + today's posts in the clone, touches nothing
  python3 ops/publish_next.py --dry-run   # everything except the real push and the queue move (git push --dry-run)
  python3 ops/publish_next.py             # publish the next entry now (manual publish; no slot logic)

Queue (default ~/.ipe/queue/tottertop):
  <queue>/<NN-anything>/en.md   front matter slug · lang · title · description · excerpt, then the body (no `published:` line)
  <queue>/<NN-anything>/ko.md   same slug
Folders go out in name order; a published folder moves to <queue>/.published/. The post's slug becomes <YYYY-MM-DD>-<slug>.

Guards: dedicated clone hard-reset to origin/main every run · no deleted files · only allow-listed paths staged · no leftovers ·
push must fast-forward (otherwise SoftFail, retried by the gate on its next tick) · a red check is a HardFail (FAILED file stops
the gate until a human deletes it). State dir (--base, default ~/.ipe/tottertop-publish): repo/ lock/ FAILED.
"""
import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

KST = dt.timezone(dt.timedelta(hours=9))
MAIN_LANGS = ("en", "ko")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# the only paths a publish may touch (everything else staged = hard fail)
ALLOWED_PATH = re.compile(
    r"^(content/journal/[a-z0-9-]+\.(en|ko)\.md|journal/.*|ko/journal/.*|index\.html|ko/index\.html|sitemap\.xml|llms\.txt)$")
DEFAULT_REMOTE = "https://github.com/blessu76/tottertop-rest.git"
DEFAULT_LIVE = "https://tottertop.ipe.rest"
DEFAULT_KIT = str(Path.home() / "Developer" / "ipe_web_kit")


class HardFail(Exception):
    """bad manuscript / check red / guard tripped — stop until a human removes FAILED."""


class SoftFail(Exception):
    """network or a non-fast-forward push — retried on the next gate tick from a clean clone."""


# ---------------------------------------------------------------- pure helpers

def split_front(text):
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise HardFail("missing front matter (file must start with ---)")
    end = text.find("\n---", 4)
    if end == -1:
        raise HardFail("front matter is not closed with ---")
    return text[4:end], text[end:]


def front_meta(text):
    head, _ = split_front(text)
    meta = {}
    for line in head.split("\n"):
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        meta[k.strip().lower()] = v
    return meta


def stamp(text, day, hm):
    """slug -> <day>-<slug>; add `published: <day>T<hm>+09:00` as the last front matter line. Nothing else changes."""
    head, rest = split_front(text)
    out, seen_slug = [], False
    for line in head.split("\n"):
        key = line.split(":", 1)[0].strip().lower() if ":" in line and not line.startswith((" ", "#")) else ""
        if key == "published":
            raise HardFail("queued entries must not carry a published: line")
        if key == "slug":
            seen_slug = True
            line = "slug: %s-%s" % (day.isoformat(), line.split(":", 1)[1].strip())
        out.append(line)
    if not seen_slug:
        raise HardFail("front matter has no slug: line")
    out.append("published: %sT%s+09:00" % (day.isoformat(), hm))
    return "---\n" + "\n".join(out) + rest


def queue_items(queue):
    q = Path(queue)
    if not q.is_dir():
        return []
    return sorted(p for p in q.iterdir() if p.is_dir() and not p.name.startswith("."))


def load_item(folder):
    """validate one queue folder -> {'slug','title','en','ko','folder'}. HardFail on anything off."""
    folder = Path(folder)
    texts, metas = {}, {}
    for lang in MAIN_LANGS:
        f = folder / (lang + ".md")
        if not f.is_file():
            raise HardFail("%s: %s.md is missing" % (folder.name, lang))
        texts[lang] = f.read_text(encoding="utf-8")
        metas[lang] = front_meta(texts[lang])
        for k in ("slug", "lang", "title", "description"):
            if not metas[lang].get(k):
                raise HardFail("%s/%s.md: front matter `%s` is missing" % (folder.name, lang, k))
        if metas[lang]["lang"] != lang:
            raise HardFail("%s/%s.md: lang is %r" % (folder.name, lang, metas[lang]["lang"]))
        if "published" in metas[lang]:
            raise HardFail("%s/%s.md: published: is set at publish time, not in the queue" % (folder.name, lang))
    slug = metas["en"]["slug"]
    if metas["ko"]["slug"] != slug:
        raise HardFail("%s: en and ko slugs differ" % folder.name)
    if not SLUG_RE.match(slug) or slug == "feed":
        raise HardFail("%s: bad slug %r" % (folder.name, slug))
    return {"slug": slug, "title": metas["en"]["title"], "en": texts["en"], "ko": texts["ko"], "folder": folder}


def today_posts(repo, day):
    """slugs of posts in the repo whose en `published:` date is `day` (KST)."""
    d = Path(repo) / "content" / "journal"
    out = []
    for f in sorted(d.glob("*.en.md")) if d.is_dir() else []:
        try:
            pub = front_meta(f.read_text(encoding="utf-8")).get("published", "")
        except HardFail:
            continue
        if pub.startswith(day.isoformat()):
            out.append(f.name[:-len(".en.md")])
    return out


def check_staged(name_status, leftovers=""):
    """name_status = `git diff --cached --name-status`. HardFail on a deletion / foreign path / leftovers."""
    dels, bad = [], []
    for line in name_status.splitlines():
        parts = line.split("\t")
        if not parts or not parts[0]:
            continue
        if parts[0].startswith("D"):
            dels.append(parts[-1])
        for p in parts[1:]:
            if not ALLOWED_PATH.match(p):
                bad.append(p)
    if dels:
        raise HardFail("deletions staged (never pushed): " + " ".join(dels))
    if bad:
        raise HardFail("unexpected paths staged: " + " ".join(bad))
    if leftovers.strip():
        raise HardFail("unstaged/untracked leftovers: " + " ".join(leftovers.split())[:200])


# ---------------------------------------------------------------- publisher

class Publisher:
    def __init__(self, base, queue, remote=DEFAULT_REMOTE, live=DEFAULT_LIVE, kit=DEFAULT_KIT, now_fn=None,
                 dry_run=False, verify=True, branch="main", check_cmds=None, log=print):
        self.base, self.queue, self.remote, self.live, self.kit = Path(base), Path(queue), remote, live, kit
        self.clone = self.base / "repo"
        self.now_fn = now_fn or (lambda: dt.datetime.now(KST))
        self.dry, self.verify, self.branch, self.log = dry_run, verify, branch, log
        py = sys.executable or "python3"
        self.build_cmd = [py, "scripts/build_site.py"]
        self.check_cmds = [["bash", "scripts/check.sh"]] if check_cmds is None else check_cmds

    def now(self):
        return self.now_fn().astimezone(KST)

    def say(self, msg):
        self.log("[%s] %s" % (self.now().strftime("%Y-%m-%d %H:%M:%S KST"), msg))

    def run(self, cmd, check=True, timeout=900):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")  # no __pycache__ in the clone (it would trip the leftovers guard)
        r = subprocess.run(cmd, cwd=str(self.clone), capture_output=True, text=True, timeout=timeout, env=env)
        if check and r.returncode != 0:
            raise subprocess.CalledProcessError(r.returncode, cmd, r.stdout, r.stderr)
        return r

    def git(self, *args, check=True):
        return self.run(["git"] + list(args), check=check)

    @staticmethod
    def tail(e):
        return " ".join(((getattr(e, "stderr", "") or "") + (getattr(e, "stdout", "") or "")).split())[-300:]

    def flag(self, name, *lines):
        (self.base / name).write_text("\n".join((self.now().isoformat(),) + lines) + "\n", encoding="utf-8")

    # -- repo
    def sync_clone(self):
        self.base.mkdir(parents=True, exist_ok=True)
        if not (self.clone / ".git").is_dir():
            try:
                subprocess.run(["git", "clone", "--quiet", self.remote, str(self.clone)], check=True, capture_output=True,
                               text=True, timeout=300)
            except subprocess.CalledProcessError as e:
                raise SoftFail("clone failed: " + self.tail(e))
        try:
            self.git("remote", "set-url", "origin", self.remote)
            self.git("fetch", "--quiet", "origin", self.branch)
            self.git("checkout", "--quiet", "-B", self.branch, "origin/" + self.branch)
            self.git("reset", "--hard", "--quiet", "origin/" + self.branch)
            self.git("clean", "-fdq")  # leaves the gitignored vendor/ipe_web_kit alone
        except subprocess.CalledProcessError as e:
            raise SoftFail("git sync failed: " + self.tail(e))

    def reset_clone(self):
        if (self.clone / ".git").is_dir():
            self.run(["git", "reset", "--hard", "--quiet", "origin/" + self.branch], check=False)
            self.run(["git", "clean", "-fdq"], check=False)

    def ensure_kit(self):
        """the private ipe_web_kit is gitignored (vendor/ipe_web_kit): make sure it matches the lock, syncing from a local clone."""
        py = sys.executable or "python3"
        if self.run([py, "scripts/kit_lock.py", "check"], check=False).returncode == 0:
            return
        try:
            self.run([py, "scripts/kit_lock.py", "sync", "--kit", self.kit])
        except subprocess.CalledProcessError as e:
            raise HardFail("ipe_web_kit missing and could not be synced from %s: %s" % (self.kit, self.tail(e)))

    def steps(self, cmds, what):
        for cmd in cmds:
            try:
                self.run(cmd)
            except subprocess.CalledProcessError as e:
                raise HardFail("%s red (%s): %s" % (what, " ".join(cmd[:2]), self.tail(e)))
            except subprocess.TimeoutExpired:
                raise HardFail("%s timed out: %s" % (what, " ".join(cmd)))

    # -- publish
    def move_published(self, folder):
        dest = self.queue / ".published"
        dest.mkdir(parents=True, exist_ok=True)
        target = dest / folder.name
        if target.exists():
            target = dest / ("%s.%d" % (folder.name, int(time.time())))
        shutil.move(str(folder), str(target))

    def commit_and_push(self, slug, day, hm):
        cfg = []
        for k, v in (("user.name", "ipe() tottertop publisher"), ("user.email", "noreply@ipe.rest")):
            if not self.git("config", k, check=False).stdout.strip():
                cfg += ["-c", "%s=%s" % (k, v)]
        msg = "journal: %s (en+ko) — %s auto publish %s KST" % (slug, day.isoformat(), hm)
        body = "Unattended publish (ops/publish_next.py). published = push minute KST; never back-dated."
        self.git(*cfg, "commit", "--quiet", "-m", msg, "-m", body)
        sha = self.git("rev-parse", "--short", "HEAD").stdout.strip()
        if self.dry:
            r = self.git("push", "--dry-run", "origin", "HEAD:" + self.branch, check=False)
            self.say("DRY RUN: would push %s (%s) rc=%d" % (sha, slug, r.returncode))
            if r.returncode != 0:
                raise SoftFail("dry-run push failed: " + self.tail(r))
            self.say("diffstat: " + self.git("diff", "HEAD~1", "--stat").stdout.strip().splitlines()[-1])
            return sha
        try:
            self.git("push", "--quiet", "origin", "HEAD:" + self.branch)
        except subprocess.CalledProcessError as e:
            raise SoftFail("git push failed/rejected: " + self.tail(e))
        self.say("PUSHED %s: %s (%s KST)" % (sha, slug, hm))
        return sha

    def verify_live(self, slug):
        """soft: wait for the Pages deploy, then en+ko post pages answer 200. Never fails the run."""
        ok_all = True
        for lang in MAIN_LANGS:
            url = "%s/%sjournal/%s/" % (self.live.rstrip("/"), "" if lang == "en" else lang + "/", slug)
            ok = False
            for _ in range(24):  # ~12 min
                try:
                    with urllib.request.urlopen(url + "?v=%d" % time.time(), timeout=20) as r:
                        ok = r.status == 200
                except Exception:  # noqa: BLE001
                    ok = False
                if ok:
                    break
                time.sleep(30)
            self.say("live %s: %s" % ("OK" if ok else "NOT 200", url))
            ok_all &= ok
        if not ok_all:
            self.flag("LIVE_CHECK_FAILED", slug)
        else:
            (self.base / "LIVE_CHECK_FAILED").unlink(missing_ok=True)
        return ok_all

    def publish_one(self):
        """-> ('published', slug) | ('already', slug) | ('empty', None). Raises HardFail / SoftFail."""
        try:
            self.sync_clone()
            self.ensure_kit()
            now = self.now()
            day, hm = now.date(), now.strftime("%H:%M")
            done = today_posts(self.clone, day)
            if done:
                self.say("already published today: %s" % ", ".join(done))
                return "already", done[0]
            items = queue_items(self.queue)
            if not items:
                self.say("queue EMPTY — nothing to publish")
                return "empty", None
            item = load_item(items[0])
            slug = "%s-%s" % (day.isoformat(), item["slug"])
            if (self.clone / "content" / "journal" / (slug + ".en.md")).exists():
                raise HardFail("%s already exists in the repo" % slug)
            self.say("publishing %s (%s)" % (slug, item["folder"].name))
            for lang in MAIN_LANGS:
                dest = self.clone / "content" / "journal" / ("%s.%s.md" % (slug, lang))
                dest.write_text(stamp(item[lang], day, hm), encoding="utf-8")
            self.steps([self.build_cmd], "build")
            self.steps(self.check_cmds, "check")
            if self.now().date() != day:
                raise SoftFail("date changed while checking (midnight) — retry next tick")
            self.git("add", "-A")
            names = self.git("diff", "--cached", "--name-status").stdout
            left = "\n".join(l for l in self.git("status", "--porcelain").stdout.splitlines() if not re.match(r"^[AM] ", l))
            check_staged(names, left)
            added = [l.split("\t")[-1] for l in names.splitlines() if l.startswith("A")]
            for lang in MAIN_LANGS:
                if "content/journal/%s.%s.md" % (slug, lang) not in added:
                    raise HardFail("expected new file content/journal/%s.%s.md was not staged" % (slug, lang))
            self.commit_and_push(slug, day, hm)
            if self.dry:
                self.reset_clone()
                return "published", slug
            self.move_published(item["folder"])
            if self.verify:
                self.verify_live(slug)
            return "published", slug
        except (HardFail, SoftFail):
            self.reset_clone()
            raise

    def status(self):
        items = queue_items(self.queue)
        self.say("queue: %d entr%s in %s" % (len(items), "y" if len(items) == 1 else "ies", self.queue))
        for p in items:
            try:
                self.say("  %s -> %s" % (p.name, load_item(p)["slug"]))
            except HardFail as e:
                self.say("  %s -> INVALID: %s" % (p.name, e))
        if (self.clone / ".git").is_dir():
            self.say("today in clone: %s" % (", ".join(today_posts(self.clone, self.now().date())) or "none"))
        for name in ("FAILED", "LIVE_CHECK_FAILED"):
            if (self.base / name).exists():
                self.say("%s: %s" % (name, " | ".join((self.base / name).read_text().strip().splitlines())))
        return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default=os.environ.get("TOTTERTOP_PUBLISH_BASE", str(Path.home() / ".ipe" / "tottertop-publish")))
    ap.add_argument("--queue", default=os.environ.get("TOTTERTOP_PUBLISH_QUEUE", str(Path.home() / ".ipe" / "queue" / "tottertop")))
    ap.add_argument("--remote", default=os.environ.get("TOTTERTOP_PUBLISH_REMOTE", DEFAULT_REMOTE))
    ap.add_argument("--live-base", default=DEFAULT_LIVE)
    ap.add_argument("--kit", default=os.environ.get("TOTTERTOP_KIT", DEFAULT_KIT))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--no-verify", action="store_true", help="skip the live 200 wait after push")
    a = ap.parse_args(argv)
    pub = Publisher(a.base, a.queue, a.remote, a.live_base, a.kit, dry_run=a.dry_run, verify=not a.no_verify)
    if a.status:
        return pub.status()
    try:
        status, slug = pub.publish_one()
    except HardFail as e:
        pub.say("HARD FAIL: %s" % e)
        if not a.dry_run:
            pub.flag("FAILED", str(e))
        return 1
    except SoftFail as e:
        pub.say("soft fail: %s" % e)
        return 1
    pub.say("result: %s %s" % (status, slug or ""))
    return 0 if status != "empty" else 3


if __name__ == "__main__":
    sys.exit(main())
