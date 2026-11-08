// Home page
const grid = document.getElementById("grid");
const empty = document.getElementById("empty");
const q = document.getElementById("q");
const sort = document.getElementById("sort");
let projects = [];
let kind = "all";

// where the floating icons sit around the hero image (percent of the art box)
const SPOTS = [
  { x: 0, y: 4, r: -10, d: 0 }, { x: 80, y: 0, r: 8, d: -1.5 }, { x: 88, y: 46, r: -6, d: -3 },
  { x: 74, y: 82, r: 10, d: -.8 }, { x: 22, y: 86, r: -8, d: -2.2 }, { x: -4, y: 50, r: 6, d: -4 },
];

function renderHero() {
  const top = [...projects].sort((a, b) => b.downloads - a.downloads).slice(0, SPOTS.length);
  document.getElementById("floaters").innerHTML = top.map((p, i) => {
    const s = SPOTS[i];
    return `<a href="${pageUrl(p)}" title="${esc(p.title)}" tabindex="-1"
      style="left:${s.x}%;top:${s.y}%;transform:rotate(${s.r}deg);animation-delay:${s.d}s">
      <img src="${esc(asset(p.icon_url))}" alt="" width="64" height="64"></a>`;
  }).join("");
  const total = projects.reduce((s, p) => s + p.downloads, 0);
  document.getElementById("s-projects").textContent = projects.length;
  document.getElementById("s-downloads").textContent = short(total);
}

function renderPodium() {
  const top = [...projects].sort((a, b) => b.downloads - a.downloads).slice(0, 3);
  // podium order: #2 left, #1 in the middle (biggest), #3 right
  const placed = [[top[1], 1], [top[0], 0], [top[2], 2]].filter(([p]) => p);
  document.getElementById("podium").innerHTML = placed.map(([p, i]) => `
    <a class="pod pod-${i + 1}" href="${pageUrl(p)}" style="--glow:${glow(p, .45)}">
      <span class="rank">#${i + 1}</span>
      <img src="${esc(asset(p.icon_url))}" alt="" width="128" height="128">
      <h3>${esc(p.title)}</h3>
      <p>${esc(p.description)}</p>
      <span class="num"><b>${nf.format(p.downloads)}</b> downloads</span>
      <span class="more">See the plugin</span>
    </a>`).join("");
}

function renderGrid() {
  const term = q.value.trim().toLowerCase();
  const rows = [...projects, ...Object.values(LOCAL)].filter((p) => {
    if (kind === "mod" && !isMod(p)) return false;
    if (kind === "plugin" && isMod(p)) return false;
    return !term || (p.title + " " + p.description + " " + p.slug).toLowerCase().includes(term);
  });
  const by = sort.dataset.value;
  rows.sort((a, b) =>
    by === "title" ? a.title.localeCompare(b.title)
    : by === "updated" ? new Date(b.updated) - new Date(a.updated)
    : b.downloads - a.downloads);
  grid.innerHTML = rows.map(cardHtml).join("");
  empty.hidden = rows.length > 0;
}

function setKind(k) {
  kind = k;
  document.querySelectorAll(".seg button").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.kind === k)));
  renderGrid();
}

document.querySelectorAll(".seg button").forEach((b) => b.addEventListener("click", () => setKind(b.dataset.kind)));
q.addEventListener("input", renderGrid);
// sort dropdown (custom listbox, works with mouse and keyboard)
(() => {
  const btn = sort.querySelector(".sort-btn");
  const menu = sort.querySelector(".sort-menu");
  const opts = [...menu.querySelectorAll("li")];
  let active = 0;

  const highlight = (i) => {
    active = (i + opts.length) % opts.length;
    opts.forEach((o, j) => o.classList.toggle("active", j === active));
  };
  const open = () => {
    menu.hidden = false; btn.setAttribute("aria-expanded", "true");
    highlight(opts.findIndex((o) => o.getAttribute("aria-selected") === "true"));
    menu.focus();
  };
  const close = (focusBtn = true) => {
    menu.hidden = true; btn.setAttribute("aria-expanded", "false");
    if (focusBtn) btn.focus();
  };
  const choose = (i) => {
    const o = opts[i];
    opts.forEach((x) => x.setAttribute("aria-selected", String(x === o)));
    sort.dataset.value = o.dataset.value;
    const label = o.querySelector("b").textContent;
    sort.querySelector(".sort-label").textContent = label;
    btn.setAttribute("aria-label", `Sort by: ${label}`);
    close();
    renderGrid();
  };

  btn.addEventListener("click", () => (menu.hidden ? open() : close()));
  btn.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); open(); }
  });
  menu.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") { e.preventDefault(); highlight(active + 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); highlight(active - 1); }
    else if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choose(active); }
    else if (e.key === "Escape" || e.key === "Tab") { close(e.key === "Escape"); }
  });
  opts.forEach((o, i) => {
    o.addEventListener("click", () => choose(i));
    o.addEventListener("mousemove", () => highlight(i));
  });
  document.addEventListener("click", (e) => { if (!sort.contains(e.target) && !menu.hidden) close(false); });
})();
document.getElementById("clear").addEventListener("click", () => { q.value = ""; setKind("all"); });

// Draw at once from the data built into data.js, then quietly refresh from Modrinth.
// Only the parts whose numbers changed are redrawn, so nothing jumps or restarts.
const topSlugs = (list, n) => [...list].sort((a, b) => b.downloads - a.downloads).slice(0, n).map((p) => p.slug).join();
const counts = (list) => list.map((p) => p.slug + ":" + p.downloads).sort().join();

function show(list) {
  projects = list;
  renderHero();
  renderPodium();
  renderGrid();
  fillFooter(projects);
}

if (typeof SNAPSHOT !== "undefined" && SNAPSHOT.length) show(SNAPSHOT);

fetch(`${API}/user/${USER}/projects`)
  .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
  .then((fresh) => {
    if (!projects.length) return show(fresh);
    if (counts(fresh) === counts(projects)) return;
    const heroChanged = topSlugs(fresh, SPOTS.length) !== topSlugs(projects, SPOTS.length);
    projects = fresh;
    if (heroChanged) renderHero();
    else {
      const total = projects.reduce((s, p) => s + p.downloads, 0);
      document.getElementById("s-projects").textContent = projects.length;
      document.getElementById("s-downloads").textContent = short(total);
    }
    renderPodium();
    if (!document.querySelector(".sort-menu:not([hidden])")) renderGrid();
    fillFooter(projects);
  })
  .catch(() => { if (!projects.length) show([]); });
