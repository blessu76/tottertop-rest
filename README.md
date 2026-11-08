# tilttower-rest

Intro site for **Tottertop / 기우뚱탑** (F-026). Static site, Python 3.8+ stdlib only, 11 languages.

- Game name / domain / operator live in ONE place: `games.json` (+ root `CNAME` must equal its `domain`).
- Build: `python3 scripts/build_site.py` — writes the generated pages, sitemap.xml, robots.txt, llms.txt.
- Green gate before every commit: `bash scripts/check.sh` (kit lock, sources, tests, build up to date, sitemap).
- Private `ipe_web_kit` is pinned by `vendor/ipe_web_kit.lock`; install with `python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit`.
- Page text: `content/i18n/<lang>.json` and `content/pages/<lang>/{privacy,terms,contact}.md` (non-en/ko pages need `translation_of: en|ko`).

## HOLD
Do not push, create the GitHub repo, or touch DNS until the owner (Davy) says so. The name is final: Tottertop (tottertop.ipe.rest).

## TODO
- Real art (assets/ are brand-neutral placeholders).
- Resolve the `[법무 확인 필요]` markers in privacy §2/§3 and terms §2 before the store submission.
