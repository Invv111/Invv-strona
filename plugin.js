// One page per plugin: plugin.html?p=<modrinth slug>
const page = document.getElementById("page");
const slug = new URLSearchParams(location.search).get("p") || "";

function md(text) {
  const html = marked.parse(text || "", { gfm: true, breaks: false });
  return DOMPurify.sanitize(html, { ADD_ATTR: ["align", "target"] });
}

function notFound() {
  document.title = "Not found – Invv";
  page.innerHTML = `<div class="loading">
    <p>There's no plugin called “${esc(slug)}”.</p>
    <p><a class="btn" href="./#all">See all plugins</a></p></div>`;
}

async function getJson(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(r.status);
  return r.json();
}

async function load() {
  if (!slug) return notFound();
  const all = await loadProjects();
  fillFooter(all);

  let p, body, gallery, versions = [];
  try {
    if (LOCAL[slug]) {
      p = LOCAL[slug];
      const [text, extra] = await Promise.all([
        fetch(`content/${slug}.md`).then((r) => r.text()),
        getJson("content/local.json"),
      ]);
      body = text;
      gallery = extra[slug]?.gallery || [];
    } else {
      [p, versions] = await Promise.all([
        getJson(`${API}/project/${encodeURIComponent(slug)}`),
        getJson(`${API}/project/${encodeURIComponent(slug)}/version`).catch(() => []),
      ]);
      body = p.body;
      gallery = [...(p.gallery || [])].sort((a, b) => (b.featured - a.featured) || (a.ordering - b.ordering))
        .map((g) => ({ url: g.url, title: g.title, description: g.description }));
      const fromList = all.find((x) => x.id === p.id);
      if (fromList) p.color ??= fromList.color;
    }
  } catch {
    return notFound();
  }
  render(p, body, gallery, versions, all);
}

function render(p, body, gallery, versions, all) {
  document.title = `${p.title} – Invv`;
  document.querySelector('meta[name="description"]')?.remove();
  document.head.insertAdjacentHTML("beforeend", `<meta name="description" content="${esc(p.description)}">`);

  const latest = versions[0];

  const actions = p.local
    ? `<a class="btn" href="https://discord.gg/E9hpUj3E6G">Get notified on Discord</a>
       <a class="btn btn-ghost" href="./#next">More coming soon</a>`
    : `${latest ? `<a class="btn" href="${modrinthUrl(p)}/version/${encodeURIComponent(latest.id)}">Download ${esc(latest.version_number)}</a>` : ""}
       <a class="btn btn-ghost" href="${modrinthUrl(p)}">Open on Modrinth</a>`;

  const facts = [
    p.local ? `<span class="chip"><b>Coming soon</b></span>` : `<span class="chip"><b>${nf.format(p.downloads)}</b> downloads</span>`,
    !p.local && p.followers ? `<span class="chip"><b>${nf.format(p.followers)}</b> followers</span>` : "",
    `<span class="chip">Minecraft <b>${esc(versionRange(p))}</b></span>`,
    `<span class="chip">${esc(platforms(p))}</span>`,
    !p.local ? `<span class="chip">Updated <b>${ago(p.updated)}</b></span>` : "",
  ].join("");

  const verList = p.local
    ? `<p style="margin:0;color:var(--muted);font-size:15px">Not released yet. Join the Discord to hear when it's out.</p>`
    : versions.length
      ? `<ul class="vers">${versions.slice(0, 6).map((v) => {
          const gv = v.game_versions.filter((x) => /^\d/.test(x));
          const range = gv.length > 1 ? `${gv[0]} – ${gv[gv.length - 1]}` : gv[0] || "";
          return `<li><div><b>${esc(v.version_number)}</b><span>${esc(range)} · ${ago(v.date_published)}</span></div>
            <a href="${modrinthUrl(p)}/version/${encodeURIComponent(v.id)}">Download</a></li>`;
        }).join("")}</ul>
        <p style="margin:14px 0 0;font-size:14px"><a href="${modrinthUrl(p)}/versions" style="color:var(--muted)">All versions on Modrinth</a></p>`
      : `<p style="margin:0;color:var(--muted)">No files yet.</p>`;

  const links = [
    !p.local && [modrinthUrl(p), "Modrinth page"],
    p.source_url && [p.source_url, "Source code"],
    p.issues_url && [p.issues_url, "Issue tracker"],
    p.wiki_url && [p.wiki_url, "Wiki"],
    ["https://discord.gg/E9hpUj3E6G", "Discord, for help and bug reports"],
  ].filter(Boolean).map(([u, t]) => `<li><a href="${esc(u)}">${esc(t)}</a></li>`).join("");

  const others = all.filter((x) => x.slug !== p.slug)
    .sort((a, b) => b.downloads - a.downloads).slice(0, 4);

  const hero = gallery[0]?.url || "";

  page.innerHTML = `
    <section class="p-hero" style="--glow:${glow(p, .35)}">
      ${hero ? `<div class="bgimg" style="background-image:url('${esc(hero)}')"></div>` : ""}
      <div class="p-hero-inner">
        <p class="crumb"><a href="./">Home</a> / <a href="./#all">${typeOf(p)}s</a> / ${esc(p.title)}</p>
        <img class="p-icon" src="${esc(p.icon_url)}" alt="" width="128" height="128">
        <div class="p-title"><h1>${esc(p.title)}</h1><p>${esc(p.description)}</p></div>
        <div class="p-actions">${actions}</div>
        <div class="p-facts">${facts}</div>
      </div>
    </section>

    <div class="p-body">
      <div>
        ${gallery.length ? `<div class="gallery">
          <figure class="g-main" style="margin:0">
            <img id="g-img" src="${esc(gallery[0].url)}" alt="${esc(gallery[0].title || "")}">
            <figcaption class="g-cap" id="g-cap"></figcaption>
          </figure>
          ${gallery.length > 1 ? `<div class="g-thumbs" role="list">${gallery.map((g, i) =>
            `<button type="button" data-i="${i}" aria-current="${i === 0}" aria-label="Show screenshot ${i + 1}${g.title ? ": " + esc(g.title) : ""}">
              <img src="${esc(g.url)}" alt="" loading="lazy"></button>`).join("")}</div>` : ""}
        </div>` : ""}
        <article class="md">${md(body)}</article>
      </div>
      <aside class="side">
        <div class="box"><h2>${p.local ? "Release" : "Latest versions"}</h2>${verList}</div>
        <div class="box"><h2>Links</h2><ul class="links">${links}</ul></div>
      </aside>
    </div>

    <section class="others">
      <div class="block-head center"><h2>More plugins</h2></div>
      <ul class="grid">${others.map(cardHtml).join("")}</ul>
    </section>`;

  // open links in the description in a new tab
  page.querySelectorAll(".md a[href^='http']").forEach((a) => { a.target = "_blank"; a.rel = "noopener"; });

  if (gallery.length) {
    const img = document.getElementById("g-img");
    const cap = document.getElementById("g-cap");
    const show = (i) => {
      const g = gallery[i];
      img.src = g.url; img.alt = g.title || "";
      cap.innerHTML = g.title || g.description ? `${g.title ? `<b>${esc(g.title)}</b>` : ""}${esc(g.description || "")}` : "";
      cap.hidden = !(g.title || g.description);
      page.querySelectorAll(".g-thumbs button").forEach((b) => b.setAttribute("aria-current", String(+b.dataset.i === i)));
    };
    page.querySelectorAll(".g-thumbs button").forEach((b) => b.addEventListener("click", () => show(+b.dataset.i)));
    show(0);
  }
}

load();
