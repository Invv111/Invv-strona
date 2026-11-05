# Invv-strona

My site for my Minecraft plugins: https://invv111.github.io/Invv-strona/

The address comes from the repo name (scripts/build.py reads it), so renaming the repo just works.

- `index.html` + `app.js`: the home page. The plugin list loads live from the Modrinth API (user `invv`).
- `plugin.html` + `plugin.js`: one page per plugin, e.g. `plugin.html?p=tpaa` (fallback; built pages live at `/<slug>/`). It pulls the description, gallery, versions and download links from Modrinth.
- `scripts/build.py`: builds a real page for every plugin at `/<slug>/` (Discord previews, Google), plus
  `data.js`, `sitemap.xml` and `404.html`. A GitHub Action runs it every day and on every push.
- `content/local.json` + `content/<name>.md`: plugins that aren't on Modrinth yet (Elevate, Reap, Lounge).
  Once one is on Modrinth, delete it from `local.json`.
- `common.js`: shared helpers.

Local preview: `python -m http.server 8765`, then open http://localhost:8765
