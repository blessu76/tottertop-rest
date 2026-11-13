# tilttower-rest

Intro site for **Tottertop / 기우뚱탑** (F-026). Static site, Python 3.8+ stdlib only, 12 languages.

- Game name / domain / operator live in ONE place: `games.json` (+ root `CNAME` must equal its `domain`).
- Build: `python3 scripts/build_site.py` — writes the generated pages, sitemap.xml, robots.txt, llms.txt.
- Green gate before every commit: `bash scripts/check.sh` (kit lock, sources, tests, build up to date, sitemap).
- Private `ipe_web_kit` is pinned by `vendor/ipe_web_kit.lock`; install with `python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit`.
- Page text: `content/i18n/<lang>.json` and `content/pages/<lang>/{privacy,terms,contact}.md` (non-en/ko pages need `translation_of: en|ko`).

## Daily journal publishing (ops/)
One journal post a day (en+ko), at a random time in 12:00-17:59 KST that is never in yesterday's hour. Nothing here ships in the site.

- Queue (outside the repo): `~/.ipe/queue/tottertop/<NN-name>/{en,ko}.md` (front matter slug/lang/title/description/excerpt, no `published:`). Folders go out in name order and move to `.published/`.
- `ops/publish_next.py` publishes the first entry: dated slug -> build -> `scripts/check.sh` GREEN -> commit -> push -> live 200. Works in its own clone `~/.ipe/tottertop-publish/repo` (hard-reset to origin/main each run).
- `ops/slot_gate.py` keeps `~/.ipe/queue/tottertop/slot.json` (`date`, `time`, `prev_date`, `prev_time`, `published`): new day -> draw a slot, publish once when due, never inside the 10:00-11:00 / 13:00-14:30 push windows (deferred). A queue of 2 or fewer posts logs a warning.
- `ops/rest.ipe.tottertop-publish.plist`: launchd, every 15 min 12:00-18:45 KST. Install: copy to `~/Library/LaunchAgents/`, then `launchctl bootstrap gui/$(id -u) <plist>`. Pause: `launchctl bootout gui/$(id -u)/rest.ipe.tottertop-publish`.
- A hard failure writes `~/.ipe/tottertop-publish/FAILED` and stops the gate until a human deletes it. Logs: `~/.ipe/logs/tottertop-publish.log`.
- Check without publishing: `python3 ops/slot_gate.py --status`, `python3 ops/publish_next.py --dry-run`.

## Hidden pages
privacy/terms are hidden (not built, not linked) until the app exists: see `HIDDEN_PAGES` in `scripts/build_site.py`. Sources stay in `content/pages/`.

## TODO
- Real art (assets/ are brand-neutral placeholders).
- Resolve the `[법무 확인 필요]` markers in privacy §2/§3 and terms §2, then move the slugs back into `PAGE_SLUGS` before the store submission.
