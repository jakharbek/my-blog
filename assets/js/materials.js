/* Materials page: formulas (KaTeX, if it loaded), group filter,
   expand / collapse all, and opening the card a link points to. */
(function () {
  "use strict";
  const main = document.querySelector("main.material");
  if (!main) return;

  // ----- formulas: without KaTeX the TeX source stays as text
  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(main, {
        delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }],
        throwOnError: false,
      });
    } catch (e) {}
  }

  // ----- group filter
  const chips = Array.from(main.querySelectorAll(".chip[data-group]"));
  const groups = Array.from(main.querySelectorAll(".fgroup"));
  let current = "all";
  const show = (g) => {
    current = g;
    chips.forEach((c) => c.setAttribute("aria-pressed", c.getAttribute("data-group") === g ? "true" : "false"));
    groups.forEach((s) => { s.hidden = g !== "all" && s.getAttribute("data-group") !== g; });
  };
  chips.forEach((c) => c.addEventListener("click", () => show(c.getAttribute("data-group"))));

  // ----- expand / collapse the visible cards
  main.querySelectorAll("[data-expand]").forEach((b) => b.addEventListener("click", () => {
    const open = b.getAttribute("data-expand") === "1";
    groups.forEach((s) => { if (!s.hidden) s.querySelectorAll(".fcard details").forEach((d) => { d.open = open; }); });
  }));

  // ----- quizzes on formula pages: one answer per question, then the explanation
  main.querySelectorAll(".quiz").forEach((quiz) => {
    quiz.querySelectorAll(".q").forEach((q) => {
      const btns = Array.from(q.querySelectorAll(".opts button"));
      const ex = q.querySelector(".explain");
      btns.forEach((b) => b.addEventListener("click", () => {
        const ok = b.getAttribute("data-ok") === "1";
        btns.forEach((x) => { x.disabled = true; if (x.getAttribute("data-ok") === "1") x.classList.add("right"); });
        if (!ok) b.classList.add("wrong");
        if (ex) {
          const verdict = document.createElement("b");
          verdict.textContent = (ok ? quiz.dataset.right : quiz.dataset.wrong) + " ";
          ex.prepend(verdict);
          ex.hidden = false;
        }
      }));
    });
  });

  // ----- a link to #card opens that card
  const follow = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const el = id && document.getElementById(id);
    if (!el || !main.contains(el)) return;
    if (current !== "all" && el.closest(".fgroup") && el.closest(".fgroup").hidden) show("all");
    const d = el.matches(".fcard") ? el.querySelector("details") : null;
    if (d) d.open = true;
    el.scrollIntoView({ block: "start" });
  };
  window.addEventListener("hashchange", follow);
  follow();
})();
