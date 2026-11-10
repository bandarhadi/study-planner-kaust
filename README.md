# STUDY PLANNER. (PWA)

A small offline-capable web app version of the Notion "STUDY PLANNER." page.

- **Live app:** https://bandarhadi.github.io/study-planner-kaust/
- **Content source:** `content-backup/content.json`. This is the hash-verified Notion backup; the audit is in `content-backup/AUDIT.md`.
- **App data:** `data.js` is generated from that file by `tools/make_assets.py`. Do not edit it by hand.
- **Saved progress:** stored in the browser's localStorage under the key `study-planner:v1`.
- Interface in Arabic (default) and English; the original Notion content is never translated.
- Arabic font: IBM Plex Sans Arabic, bundled in `fonts/` under the SIL Open Font License.
- No backend, no accounts, no external requests.

When you change any file, bump `VERSION` in `sw.js` so installed copies pick up the update.
