# tilttower-rest

Intro site skeleton for **Tilt Tower / 기우뚱탑** (F-026). Static site, Python 3.8+ stdlib only, 11 languages.

- Game name / domain / operator live in ONE place: `games.json` (+ root `CNAME` must equal its `domain`).
- Build: `python3 scripts/build_site.py` — writes the generated pages, sitemap.xml, robots.txt, llms.txt.
- Green gate before every commit: `bash scripts/check.sh` (kit lock, sources, tests, build up to date, sitemap).
- Private `ipe_web_kit` is pinned by `vendor/ipe_web_kit.lock`; install with `python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit`.
- Page text: `content/i18n/<lang>.json` and `content/pages/<lang>/{privacy,terms,contact}.md` (non-en/ko pages need `translation_of: en|ko`).

## HOLD
Do not push, create the GitHub repo, or touch DNS until the tlt-0001 trademark issue is resolved (decided in room g00).

## TODO
- Real translations for the 9 non-en/ko languages (currently English copies).
- Real art (assets/ are brand-neutral placeholders), privacy §2 and terms §2 `[TODO]`.
