"""
Builds a real HTML page for every plugin, so Discord link previews and Google see the content.

  python scripts/build.py

Writes:
  <slug>/index.html   one page per plugin (Modrinth + content/local.json)
  data.js             LOCAL plugins + a snapshot of the Modrinth list, used by the JS
  sitemap.xml
Needs: pip install markdown-it-py
"""
import html
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

from markdown_it import MarkdownIt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def site_address():
    """Where GitHub Pages serves this repo: owner.github.io/ for a repo named owner.github.io,
    owner.github.io/<repo>/ for any other name. Read from the repo, so a rename just works."""
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT, capture_output=True, text=True).stdout
        m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?\s*$", url)
        repo = f"{m.group(1)}/{m.group(2)}" if m else "Invv111/Invv111.github.io"
    owner, name = repo.split("/")
    base = "/" if name.lower() == f"{owner.lower()}.github.io" else f"/{name}/"
    return f"https://{owner.lower()}.github.io{base}".rstrip("/"), base


SITE, BASE = site_address()
USER = "invv"
API = "https://api.modrinth.com/v2"
DISCORD = "https://discord.gg/E9hpUj3E6G"
UA = "Invv111/invv111.github.io (site build)"

MOD_LOADERS = {"fabric", "quilt", "neoforge", "forge"}
NICE = {"paper": "Paper", "folia": "Folia", "spigot": "Spigot", "purpur": "Purpur", "bukkit": "Bukkit",
        "fabric": "Fabric", "quilt": "Quilt", "neoforge": "NeoForge", "forge": "Forge"}

md = MarkdownIt("commonmark", {"html": True, "linkify": False}).enable(["table", "strikethrough"])
e = lambda s: html.escape(str(s if s is not None else ""), quote=True)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def is_mod(p):
    return bool(MOD_LOADERS & set(p["loaders"]))


def type_of(p):
    return "Fabric mod" if is_mod(p) else "Server plugin"


def modrinth_url(p):
    return f"https://modrinth.com/{'mod' if is_mod(p) else 'plugin'}/{p['slug']}"


def version_range(p):
    v = [x for x in p.get("game_versions", []) if re.match(r"^\d", x)]
    if not v:
        return ""
    return v[0] if len(v) == 1 else f"{v[0]} – {v[-1]}"


def platforms(p):
    order = ["paper", "folia", "spigot", "purpur", "bukkit", "fabric", "quilt", "neoforge", "forge"]
    ls = [l for l in order if l in p["loaders"]]
    if "spigot" in ls and "bukkit" in ls:
        ls.remove("bukkit")
    return ", ".join(NICE[l] for l in ls)


def hex_color(p):
    c = p.get("color") if isinstance(p.get("color"), int) else 0xF3A53A
    return f"#{c:06x}"


def glow(p, a=0.35):
    c = p.get("color") if isinstance(p.get("color"), int) else 0xF3A53A
    return f"rgba({(c >> 16) & 255}, {(c >> 8) & 255}, {c & 255}, {a})"


def ago(iso):
    days = (datetime.now(timezone.utc) - datetime.fromisoformat(iso.replace("Z", "+00:00"))).days
    if days < 1:
        return "today"
    if days < 31:
        return f"{days} day{'s' if days != 1 else ''} ago"
    m = days // 30
    if m < 12:
        return f"{m} month{'s' if m != 1 else ''} ago"
    y = m // 12
    return f"{y} year{'s' if y != 1 else ''} ago"


def absolute(url):
    return url if url.startswith("http") else SITE + "/" + url.lstrip("/")


def rootrel(url):
    """'img/x.png' -> '/img/x.png' in the templates; to_relative() later turns '/' into '../'"""
    return url if url.startswith("http") else "/" + url.lstrip("/")


def to_relative(page_html):
    """the generated pages live one folder down, so every root path becomes ../"""
    return re.sub(r'(href|src)="/(?!/)', r'\g<1>="../', page_html).replace("url('/", "url('../")


def plain(text, n=200):
    """first n chars of a description, for meta tags"""
    t = re.sub(r"\s+", " ", text or "").strip()
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0] + "…"


def card(p):
    meta = ("<span>Coming soon</span>" if p.get("local")
            else f"<span><b>{p['downloads']:,}</b> downloads</span>")
    return f"""<li class="card"><a href="/{e(p['slug'])}/" style="--glow:{glow(p, .32)}">
    <img class="icon" src="{e(rootrel(p['icon_url']))}" alt="" width="64" height="64" loading="lazy">
    <span class="head"><h3>{e(p['title'])}</h3><span class="type">{type_of(p)}</span></span>
    <p>{e(p['description'])}</p>
    <span class="meta">{meta}<span>{e(version_range(p))}</span></span>
  </a></li>"""


HEADER = f"""<header class="top">
  <a class="me" href="/">
    <img src="/img/logo.svg" alt="" width="34" height="34">
    Invv
  </a>
  <nav id="nav" aria-label="Main">
    <a href="/#popular">Popular</a>
    <a href="/#next">Coming next</a>
    <a href="/#all">All plugins</a>
    <a href="https://modrinth.com/user/{USER}">Modrinth</a>
  </nav>
  <a class="btn btn-small" href="{DISCORD}">Discord</a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span></button>
</header>"""


def footer(projects):
    top = sorted(projects, key=lambda p: -p["downloads"])
    li = lambda p: f'<li><a href="/{e(p["slug"])}/">{e(p["title"])}</a></li>'
    plugins = "".join(li(p) for p in [p for p in top if not is_mod(p)][:6])
    mods = "".join(li(p) for p in [p for p in top if is_mod(p)][:6])
    return f"""<footer class="foot">
  <div class="foot-inner">
    <div class="foot-about">
      <a class="me" href="/"><img src="/img/logo.svg" alt="" width="34" height="34">Invv</a>
      <p>Found a bug or want a feature? Tell me on Discord, I read everything.</p>
      <a class="btn btn-small" href="{DISCORD}">Join the Discord</a>
    </div>
    <div><h4>Server plugins</h4><ul id="foot-plugins">{plugins}</ul></div>
    <div><h4>Fabric mods</h4><ul id="foot-mods">{mods}</ul></div>
    <div>
      <h4>Links</h4>
      <ul>
        <li><a href="https://modrinth.com/user/{USER}">Modrinth profile</a></li>
        <li><a href="{DISCORD}">Discord</a></li>
        <li><a href="https://github.com/Invv111">GitHub</a></li>
      </ul>
    </div>
  </div>
  <p class="fine">Descriptions and download counts come from Modrinth. Not affiliated with Mojang or Microsoft.</p>
</footer>"""


def page(p, body_md, gallery, versions, projects):
    slug = p["slug"]
    url = f"{SITE}/{slug}/"
    title = f"{p['title']} – {type_of(p)} for Minecraft {version_range(p)}"
    desc = plain(p["description"])
    # link previews get the JPG (every app shows it); the page itself loads WebP
    image = absolute(gallery[0].get("og") or gallery[0]["url"]) if gallery else absolute(p["icon_url"])
    big = bool(gallery)
    latest = versions[0] if versions else None

    if p.get("local"):
        actions = f"""<a class="btn" href="{DISCORD}">Get notified on Discord</a>
        <a class="btn btn-ghost" href="/#next">More coming soon</a>"""
        facts = '<span class="chip"><b>Coming soon</b></span>'
    else:
        dl = (f'<a class="btn" href="{modrinth_url(p)}/version/{e(latest["id"])}">Download {e(latest["version_number"])}</a>'
              if latest else "")
        actions = f"""{dl}
        <a class="btn btn-ghost" href="{modrinth_url(p)}">Open on Modrinth</a>"""
        facts = f'<span class="chip"><b data-live="downloads">{p["downloads"]:,}</b> downloads</span>'
        if p.get("followers"):
            facts += f'<span class="chip"><b data-live="followers">{p["followers"]:,}</b> followers</span>'
    facts += f'<span class="chip">Minecraft <b>{e(version_range(p))}</b></span>'
    facts += f'<span class="chip">{e(platforms(p))}</span>'
    if not p.get("local"):
        facts += f'<span class="chip">Updated <b>{ago(p["updated"])}</b></span>'

    if p.get("local"):
        ver_box = '<p class="box-note">Not released yet. Join the Discord to hear when it\'s out.</p>'
    elif versions:
        rows = []
        for v in versions[:6]:
            gv = [x for x in v["game_versions"] if re.match(r"^\d", x)]
            rng = f"{gv[0]} – {gv[-1]}" if len(gv) > 1 else (gv[0] if gv else "")
            rows.append(f'<li><div><b>{e(v["version_number"])}</b><span>{e(rng)} · {ago(v["date_published"])}</span></div>'
                        f'<a href="{modrinth_url(p)}/version/{e(v["id"])}">Download</a></li>')
        ver_box = (f'<ul class="vers">{"".join(rows)}</ul>'
                   f'<p class="box-more"><a href="{modrinth_url(p)}/versions">All versions on Modrinth</a></p>')
    else:
        ver_box = '<p class="box-note">No files yet.</p>'

    links = [] if p.get("local") else [(modrinth_url(p), "Modrinth page")]
    for key, label in (("source_url", "Source code"), ("issues_url", "Issue tracker"), ("wiki_url", "Wiki")):
        if p.get(key):
            links.append((p[key], label))
    links.append((DISCORD, "Discord, for help and bug reports"))
    links_html = "".join(f'<li><a href="{e(u)}">{e(t)}</a></li>' for u, t in links)

    gal_html = ""
    if gallery:
        g0 = gallery[0]
        thumbs = ""
        if len(gallery) > 1:
            thumbs = '<div class="g-thumbs" role="list">' + "".join(
                f'<button type="button" data-i="{i}" aria-current="{str(i == 0).lower()}" '
                f'aria-label="Show screenshot {i + 1}{": " + e(g.get("title")) if g.get("title") else ""}">'
                f'<img src="{e(rootrel(g.get("thumb") or g["url"]))}" alt="" width="160" height="90" loading="lazy" decoding="async"></button>'
                for i, g in enumerate(gallery)) + "</div>"
        cap = ""
        if g0.get("title") or g0.get("description"):
            cap = (f'{"<b>" + e(g0["title"]) + "</b>" if g0.get("title") else ""}{e(g0.get("description") or "")}')
        gal_html = f"""<div class="gallery">
          <figure class="g-main" style="margin:0">
            <img id="g-img" src="{e(rootrel(g0['url']))}" alt="{e(g0.get('title') or p['title'])}" width="1400" height="788" decoding="async">
            <figcaption class="g-cap" id="g-cap"{'' if cap else ' hidden'}>{cap}</figcaption>
          </figure>
          {thumbs}
        </div>"""

    others = [x for x in sorted(projects, key=lambda x: -x["downloads"]) if x["slug"] != slug][:4]

    ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": p["title"],
        "description": p["description"],
        "url": url,
        "image": image,
        "applicationCategory": "GameApplication",
        "applicationSubCategory": type_of(p),
        "operatingSystem": f"Minecraft {version_range(p)} ({platforms(p)})",
        "author": {"@type": "Person", "name": "Invv", "url": f"https://modrinth.com/user/{USER}"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }
    if not p.get("local"):
        ld["downloadUrl"] = modrinth_url(p)
        ld["interactionStatistic"] = {"@type": "InteractionCounter",
                                      "interactionType": "https://schema.org/DownloadAction",
                                      "userInteractionCount": p["downloads"]}
        if latest:
            ld["softwareVersion"] = latest["version_number"]
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    data_json = json.dumps({"slug": slug, "local": bool(p.get("local")), "gallery": gallery},
                           ensure_ascii=False).replace("</", "<\\/")

    hero_bg = ""
    if gallery:
        bg = e(rootrel(gallery[0].get("thumb") or gallery[0]["url"]))
        hero_bg = "<div class=\"bgimg\" style=\"background-image:url(" + "'" + bg + "'" + ")\"></div>"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="{hex_color(p)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Invv – Minecraft plugins">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(p['title'])} – {type_of(p)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{e(image)}">
<meta name="twitter:card" content="{'summary_large_image' if big else 'summary'}">
<meta name="twitter:title" content="{e(p['title'])} – {type_of(p)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{e(image)}">
<link rel="icon" href="/img/logo.svg" type="image/svg+xml">
<link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preload" href="/fonts/bricolage-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">{ld_json}</script>
</head>
<body>

{HEADER}

<main id="page" data-static>
  <section class="p-hero" style="--glow:{glow(p)}">
    {hero_bg}
    <div class="p-hero-inner">
      <p class="crumb"><a href="/">Home</a> / <a href="/#all">{type_of(p)}s</a> / {e(p['title'])}</p>
      <img class="p-icon" src="{e(rootrel(p['icon_url']))}" alt="" width="128" height="128">
      <div class="p-title"><h1>{e(p['title'])}</h1><p>{e(p['description'])}</p></div>
      <div class="p-actions">{actions}</div>
      <div class="p-facts">{facts}</div>
    </div>
  </section>

  <div class="p-body">
    <div>
      {gal_html}
      <article class="md"><!--@BODY@--></article>
    </div>
    <aside class="side">
      <div class="box"><h2>{'Release' if p.get('local') else 'Latest versions'}</h2>{ver_box}</div>
      <div class="box"><h2>Links</h2><ul class="links">{links_html}</ul></div>
    </aside>
  </div>

  <section class="others">
    <div class="block-head center"><h2>More plugins</h2></div>
    <ul class="grid">{''.join(card(x) for x in others)}</ul>
  </section>
</main>

{footer(projects)}

<script id="page-data" type="application/json">{data_json}</script>
<script src="/data.js" defer></script>
<script src="/common.js" defer></script>
<script src="/plugin.js" defer></script>
</body>
</html>
"""


def render_page(p, body_md, gallery, versions, projects):
    out = to_relative(page(p, body_md, gallery, versions, projects))
    return out.replace("<!--@BODY@-->", md.render(body_md or ""))


def main():
    local = json.load(open(os.path.join(ROOT, "content", "local.json"), encoding="utf-8"))
    projects = get(f"{API}/user/{USER}/projects")
    if not projects:
        sys.exit("Modrinth returned no projects, not touching anything")
    print(f"{len(projects)} projects on Modrinth, {len(local)} local")

    # the snapshot keeps only what the list needs
    keep = ["id", "slug", "title", "description", "downloads", "followers", "icon_url", "color",
            "game_versions", "loaders", "published", "updated", "categories"]
    snapshot = [{k: p.get(k) for k in keep} for p in projects]
    for s in snapshot:
        gv = [x for x in s["game_versions"] if re.match(r"^\d", x)]
        s["game_versions"] = [gv[0], gv[-1]] if len(gv) > 1 else gv

    everything = projects + list(local.values())
    built = []

    for p in projects:
        full = get(f"{API}/project/{p['slug']}")
        try:
            versions = get(f"{API}/project/{p['slug']}/version")
        except Exception:
            versions = []
        versions.sort(key=lambda v: v["date_published"], reverse=True)
        gallery = sorted(full.get("gallery") or [], key=lambda g: (not g.get("featured"), g.get("ordering", 0)))
        gallery = [{"url": g["url"], "title": g.get("title"), "description": g.get("description")} for g in gallery]
        full["color"] = full.get("color") if full.get("color") is not None else p.get("color")
        write_page(full, full.get("body", ""), gallery, versions, everything)
        built.append((p["slug"], p["updated"]))

    for slug, p in local.items():
        body = open(os.path.join(ROOT, "content", f"{slug}.md"), encoding="utf-8").read()
        write_page(p, body, p["gallery"], [], everything)
        built.append((slug, p["updated"]))

    local_js = {k: {kk: vv for kk, vv in v.items() if kk != "gallery"} for k, v in local.items()}
    with open(os.path.join(ROOT, "data.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("// Generated by scripts/build.py. Edit content/local.json instead.\n")
        f.write(f"const LOCAL = {json.dumps(local_js, ensure_ascii=False, indent=1)};\n")
        f.write(f"const SNAPSHOT = {json.dumps(snapshot, ensure_ascii=False)};\n")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [f"  <url><loc>{SITE}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>"]
    urls += [f"  <url><loc>{SITE}/{e(s)}/</loc><lastmod>{u[:10]}</lastmod></url>" for s, u in built]
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write("\n".join(urls) + "\n</urlset>\n")

    patch_index()
    write_404()

    # drop pages of projects that no longer exist
    names = {s for s, _ in built}
    for d in os.listdir(ROOT):
        path = os.path.join(ROOT, d, "index.html")
        if d not in names and os.path.isfile(path) and os.path.isfile(os.path.join(ROOT, d, ".generated")):
            os.remove(path)
            os.remove(os.path.join(ROOT, d, ".generated"))
            os.rmdir(os.path.join(ROOT, d))
            print("removed", d)
    print(f"built {len(built)} pages")


def write_page(p, body, gallery, versions, everything):
    d = os.path.join(ROOT, p["slug"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(render_page(p, body, gallery, versions, everything))
    open(os.path.join(d, ".generated"), "w").close()


def patch_index():
    """put the real site address into the home page's link-preview tags"""
    path = os.path.join(ROOT, "index.html")
    s = open(path, encoding="utf-8").read()
    tags = f"""<!-- og: filled in by scripts/build.py with the site address -->
<link rel="canonical" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Invv – Minecraft plugins">
<meta property="og:url" content="{SITE}/">
<meta property="og:title" content="Invv – Minecraft plugins">
<meta property="og:description" content="Teleports, graves, an anti-xray, nametags, elevators and more. One jar for Paper, Folia, Spigot and Purpur, no dependencies.">
<meta property="og:image" content="{SITE}/img/elevate-1.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/img/elevate-1.jpg">
<!-- /og -->"""
    s = re.sub(r"<!-- og:.*?<!-- /og -->", lambda _: tags, s, flags=re.S)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def write_404():
    """GitHub Pages shows 404.html at any depth, so it uses full paths from BASE.
    An unknown /<slug>/ is sent to plugin.html, which renders a plugin published after the last build."""
    b = BASE
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found – Invv</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#f3a53a">
<link rel="icon" href="{b}img/logo.svg" type="image/svg+xml">
<link rel="icon" href="{b}img/favicon-32.png" sizes="32x32" type="image/png">
<script>
  (function () {{
    var base = {json.dumps(b)};
    var rest = location.pathname.indexOf(base) === 0 ? location.pathname.slice(base.length) : "";
    var parts = rest.split("/").filter(Boolean);
    var p = parts[0] || "";
    var isFile = /\\.(html?|png|jpe?g|gif|svg|webp|ico|js|css|json|xml|txt|md)$/i.test(p);
    if (parts.length === 1 && /^[\\w.-]+$/.test(p) && !isFile) {{
      location.replace(base + "plugin.html?p=" + encodeURIComponent(p) + "&from404=1");
    }}
  }})();
</script>
<link rel="preload" href="{b}fonts/bricolage-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{b}style.css">
</head>
<body>
<header class="top">
  <a class="me" href="{b}"><img src="{b}img/logo.svg" alt="" width="34" height="34">Invv</a>
  <a class="btn btn-small" href="{DISCORD}">Discord</a>
</header>
<main>
  <div class="loading">
    <p style="font-size:64px;font-weight:800;margin:0;color:var(--ink)">404</p>
    <p>This page doesn't exist. Maybe it was renamed, or the link has a typo.</p>
    <p><a class="btn" href="{b}#all">See all plugins</a></p>
  </div>
</main>
</body>
</html>
""")


if __name__ == "__main__":
    main()
