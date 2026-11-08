# Invv-strona

My site for my Minecraft plugins: https://invv111.github.io/Invv-strona/

The address comes from the repo name (scripts/build.py reads it), so renaming the repo just works.

- `index.html` + `app.js`: the home page. The plugin list loads live from the Modrinth API (user `invv`).
- `plugin.html` + `plugin.js`: one page per plugin, e.g. `plugin.html?p=tpaa` (fallback; built pages live at `/<slug>/`). It pulls the description, gallery, versions and download links from Modrinth.
- `scripts/build.py`: builds a real page for every plugin at `/<slug>/` (Discord previews, Google), plus
  `data.js`, `sitemap.xml` and `404.html`. A GitHub Action runs it every day and on every push.
- `content/local.json` + `content/<name>.md`: the "Coming next" plugins. The build renders that section
  and a page for each. When one comes out on Modrinth (same slug, the `modrinth` slug in local.json,
  or the same name), the next build moves it out of "Coming next" on its own and its old address
  redirects to the real page. Nothing to delete by hand.
- `common.js`: shared helpers.

Local preview: `python -m http.server 8765`, then open http://localhost:8765

## Adding a plugin to "Coming next"

1. Screenshots: `img/<name>/1-....jpg` (gallery) and one `img/<name>-1.jpg` for the tile, plus `img/<name>-logo.png`.
   Then run `python scripts/images.py`.
2. The description: `content/<name>.md` (the same text as the Modrinth description).
3. An entry in `content/local.json` (copy an existing one): title, description, `modrinth` (the slug it will get),
   `pitch`, `points`, `show` (e.g. `img/<name>-1`), `icon_url`, `loaders`, `game_versions`, `gallery`.
4. Push. The Action builds everything.
