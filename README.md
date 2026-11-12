# tilttower-rest

Intro site for **Tottertop / 기우뚱탑** (F-026). Static site, Python 3.8+ stdlib only, 12 languages.

- Game name / domain / operator live in ONE place: `games.json` (+ root `CNAME` must equal its `domain`).
- Build: `python3 scripts/build_site.py` — writes the generated pages, sitemap.xml, robots.txt, llms.txt.
- Green gate before every commit: `bash scripts/check.sh` (kit lock, sources, tests, build up to date, sitemap).
- Private `ipe_web_kit` is pinned by `vendor/ipe_web_kit.lock`; install with `python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit`.
- Page text: `content/i18n/<lang>.json` and `content/pages/<lang>/{privacy,terms,contact}.md` (non-en/ko pages need `translation_of: en|ko`).

## Hidden pages
privacy/terms are hidden (not built, not linked) until the app exists: see `HIDDEN_PAGES` in `scripts/build_site.py`. Sources stay in `content/pages/`.

## TODO
- Real art (assets/ are brand-neutral placeholders).
- Resolve the `[법무 확인 필요]` markers in privacy §2/§3 and terms §2, then move the slugs back into `PAGE_SLUGS` before the store submission.
