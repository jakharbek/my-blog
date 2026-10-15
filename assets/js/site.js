/* Shared behaviour: theme toggle, language memory, post search and filter,
   reading progress and TOC highlight. No dependencies. */
(function () {
  "use strict";
  const root = document.documentElement;

  // ----- theme: an explicit choice is stored; otherwise the system decides
  try {
    const saved = localStorage.getItem("theme");
    if (saved === "dark" || saved === "light") root.setAttribute("data-theme", saved);
  } catch (e) {}
  const btn = document.getElementById("theme-toggle");
  if (btn) {
    const isDark = () => root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
    const labels = JSON.parse(btn.getAttribute("data-labels") || "{}");
    const relabel = () => btn.setAttribute("aria-label", isDark() ? (labels.toLight || "Light theme") : (labels.toDark || "Dark theme"));
    relabel();
    btn.addEventListener("click", () => {
      const next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
      relabel();
      document.dispatchEvent(new CustomEvent("themechange"));
    });
  }
  requestAnimationFrame(() => document.body.classList.add("themed"));

  // ----- remember the language for the root redirect
  try { localStorage.setItem("lang", root.lang); } catch (e) {}

  // ----- posts: search + topic filter
  const list = document.getElementById("post-list");
  if (list) {
    const rows = Array.from(list.querySelectorAll(".row"));
    const chips = Array.from(document.querySelectorAll(".chip"));
    const tiles = Array.from(document.querySelectorAll(".tile[data-topic]"));
    const q = document.getElementById("q");
    const found = document.getElementById("found");
    const reset = document.getElementById("reset");
    const empty = document.getElementById("empty");
    const featured = document.getElementById("featured");
    const foundText = found ? found.getAttribute("data-text") : "";
    let topic = "all";

    const matches = (row, t, query) =>
      (t === "all" || row.getAttribute("data-topic") === t) &&
      (!query || row.textContent.toLowerCase().includes(query));

    const apply = () => {
      const query = (q ? q.value : "").trim().toLowerCase();
      let n = 0;
      rows.forEach((row) => { const ok = matches(row, topic, query); row.hidden = !ok; if (ok) n++; });
      chips.forEach((c) => {
        const t = c.getAttribute("data-topic");
        c.setAttribute("aria-pressed", t === topic ? "true" : "false");
        const cnt = rows.filter((r) => matches(r, t, query)).length;
        const s = c.querySelector("small"); if (s) s.textContent = cnt;
      });
      const filtered = topic !== "all" || query.length > 0;
      if (found) found.textContent = foundText + n;
      if (reset) reset.hidden = !filtered;
      if (empty) empty.hidden = n > 0;
      if (featured) featured.hidden = filtered;
    };
    chips.forEach((c) => c.addEventListener("click", () => { topic = c.getAttribute("data-topic"); apply(); }));
    tiles.forEach((t) => t.addEventListener("click", () => {
      topic = t.getAttribute("data-topic"); if (q) q.value = ""; apply();
      document.getElementById("posts").scrollIntoView({ behavior: "smooth", block: "start" });
    }));
    if (q) q.addEventListener("input", apply);
    if (reset) reset.addEventListener("click", () => { topic = "all"; if (q) q.value = ""; apply(); });
    apply();
  }

  // ----- article: reading progress + TOC highlight
  const bar = document.getElementById("progress");
  const article = document.querySelector(".article");
  if (bar && article) {
    const update = () => {
      const r = article.getBoundingClientRect();
      const total = r.height - window.innerHeight;
      const p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
      bar.style.width = (p * 100).toFixed(1) + "%";
    };
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
    const links = Array.from(document.querySelectorAll(".toc a"));
    const heads = links.map((a) => document.getElementById(a.getAttribute("href").slice(1))).filter(Boolean);
    if ("IntersectionObserver" in window && heads.length) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            links.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id));
          }
        });
      }, { rootMargin: "-10% 0px -70% 0px" });
      heads.forEach((h) => io.observe(h));
    }
  }
})();
