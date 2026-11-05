# invv111.github.io

My site for my Minecraft plugins: https://invv111.github.io/Invv-strona/

The address comes from the repo name (scripts/build.py reads it), so renaming the repo just works.

- `index.html` + `app.js`: the home page. The plugin list loads live from the Modrinth API (user `invv`).
- `plugin.html` + `plugin.js`: one page per plugin, e.g. `plugin.html?p=tpaa` (fallback; built pages live at `/<slug>/`). It pulls the description, gallery, versions and download links from Modrinth.
- `common.js`: shared helpers and `LOCAL`, the plugins that aren't on Modrinth yet (Elevate, Reap, Lounge).
  Their pages are built from `content/<name>.md` and `content/local.json`. Once one is on Modrinth, delete it from `LOCAL`.
- `projects.json`: a fallback snapshot in case the API doesn't respond.

Local preview: `python -m http.server 8765`, then open http://localhost:8765
