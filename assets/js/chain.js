/* Widgets of the article "The chain rule". Built on FV (assets/js/viz.js).
   cr-limit — the derivative as a limit: the secant through x₀ and x₀ + h turns into the tangent;
   cr-chain — y = f(g(x)): a small step Δx is stretched by g′ and then by f′;
   cr-path  — z = f(x(t), y(t)): dz/dt = f_x·x′ + f_y·y′ along a path over the level lines;
   cr-solutions — the "show all solutions" switch of the practice section. */
(function () {
  "use strict";
  if (typeof FV === "undefined" || !FV.widget) return;

  const L = {
    ru: {
      fn: "Функция", x0: "Точка $x_0$", h: "Шаг $h$", shrink: "h → 0", secant: "секущая", tangent: "касательная",
      dq: "Разностное отношение", der: "Производная $f'(x_0)$", gap: "Разница",
      limNote: (h, q, d) => `При $h = ${h}$ наклон секущей $\\frac{f(x_0 + h) - f(x_0)}{h} = ${q}$; предел при $h \\to 0$ — наклон касательной $f'(x_0) = ${d}$.`,
      preset: "Пример", dx: "Шаг $\\Delta x$", gx: "$u = g(x)$", fu: "$y = f(u)$",
      gp: "$g'(x_0)$", fp: "$f'(u_0)$", prod: "$f'(u_0)\\cdot g'(x_0)$", ratio: "$\\Delta y / \\Delta x$",
      chainNote: (dx, du, dy, gp, fp) => `Шаг $\\Delta x = ${dx}$ внутренняя функция растягивает в $g'(x_0) \\approx ${gp}$ раз: $\\Delta u \\approx ${du}$. Этот шаг внешняя функция растягивает ещё в $f'(u_0) \\approx ${fp}$ раз: $\\Delta y \\approx ${dy}$. Коэффициенты перемножаются.`,
      t: "Параметр $t$", path: "путь $(x(t), y(t))$", grad: "$\\nabla f$", vel: "$(x'(t), y'(t))$", zt: "$z(t) = f(x(t), y(t))$",
      cx: "$f_x \\cdot x'$", cy: "$f_y \\cdot y'$", dzdt: "$dz/dt$", numeric: "численно",
      pathNote: (a, b, s) => `Вклад пути через $x$: $${a}$, через $y$: $${b}$. Сумма $\\frac{dz}{dt} = ${s}$ — это наклон касательной к графику $z(t)$ справа.`,
      zero: " Здесь путь идёт по линии уровня, и вклады взаимно уничтожаются.",
      levels: "линии уровня $f$", plane: "Плоскость $(x, y)$", graph: "График $z(t)$",
      show: "Показать все решения", hide: "Скрыть все решения",
    },
    en: {
      fn: "Function", x0: "Point $x_0$", h: "Step $h$", shrink: "h → 0", secant: "secant", tangent: "tangent",
      dq: "Difference quotient", der: "Derivative $f'(x_0)$", gap: "Difference",
      limNote: (h, q, d) => `At $h = ${h}$ the slope of the secant is $\\frac{f(x_0 + h) - f(x_0)}{h} = ${q}$; its limit as $h \\to 0$ is the slope of the tangent $f'(x_0) = ${d}$.`,
      preset: "Example", dx: "Step $\\Delta x$", gx: "$u = g(x)$", fu: "$y = f(u)$",
      gp: "$g'(x_0)$", fp: "$f'(u_0)$", prod: "$f'(u_0)\\cdot g'(x_0)$", ratio: "$\\Delta y / \\Delta x$",
      chainNote: (dx, du, dy, gp, fp) => `The inner function stretches the step $\\Delta x = ${dx}$ by a factor $g'(x_0) \\approx ${gp}$: $\\Delta u \\approx ${du}$. The outer function stretches that step by another $f'(u_0) \\approx ${fp}$: $\\Delta y \\approx ${dy}$. The factors multiply.`,
      t: "Parameter $t$", path: "path $(x(t), y(t))$", grad: "$\\nabla f$", vel: "$(x'(t), y'(t))$", zt: "$z(t) = f(x(t), y(t))$",
      cx: "$f_x \\cdot x'$", cy: "$f_y \\cdot y'$", dzdt: "$dz/dt$", numeric: "numerically",
      pathNote: (a, b, s) => `The contribution of the path through $x$: $${a}$, through $y$: $${b}$. The sum $\\frac{dz}{dt} = ${s}$ is the slope of the tangent to the graph of $z(t)$ on the right.`,
      zero: " Here the path runs along a level line, and the contributions cancel out.",
      levels: "level lines of $f$", plane: "The $(x, y)$ plane", graph: "The graph of $z(t)$",
      show: "Show all solutions", hide: "Hide all solutions",
    },
    uz: {
      fn: "Funksiya", x0: "$x_0$ nuqta", h: "$h$ qadam", shrink: "h → 0", secant: "kesuvchi", tangent: "urinma",
      dq: "Ayirmali nisbat", der: "$f'(x_0)$ hosila", gap: "Farq",
      limNote: (h, q, d) => `$h = ${h}$ da kesuvchining qiyaligi $\\frac{f(x_0 + h) - f(x_0)}{h} = ${q}$; $h \\to 0$ dagi limiti — urinmaning qiyaligi $f'(x_0) = ${d}$.`,
      preset: "Misol", dx: "$\\Delta x$ qadam", gx: "$u = g(x)$", fu: "$y = f(u)$",
      gp: "$g'(x_0)$", fp: "$f'(u_0)$", prod: "$f'(u_0)\\cdot g'(x_0)$", ratio: "$\\Delta y / \\Delta x$",
      chainNote: (dx, du, dy, gp, fp) => `Ichki funksiya $\\Delta x = ${dx}$ qadamni $g'(x_0) \\approx ${gp}$ marta cho‘zadi: $\\Delta u \\approx ${du}$. Bu qadamni tashqi funksiya yana $f'(u_0) \\approx ${fp}$ marta cho‘zadi: $\\Delta y \\approx ${dy}$. Koeffitsiyentlar ko‘paytiriladi.`,
      t: "$t$ parametr", path: "$(x(t), y(t))$ yo‘l", grad: "$\\nabla f$", vel: "$(x'(t), y'(t))$", zt: "$z(t) = f(x(t), y(t))$",
      cx: "$f_x \\cdot x'$", cy: "$f_y \\cdot y'$", dzdt: "$dz/dt$", numeric: "sonli",
      pathNote: (a, b, s) => `$x$ orqali yo‘l hissasi: $${a}$, $y$ orqali: $${b}$. Yig‘indi $\\frac{dz}{dt} = ${s}$ — o‘ngdagi $z(t)$ grafigiga urinmaning qiyaligi.`,
      zero: " Bu yerda yo‘l sath chizig‘i bo‘ylab boradi va hissalar bir-birini yo‘qotadi.",
      levels: "$f$ ning sath chiziqlari", plane: "$(x, y)$ tekislik", graph: "$z(t)$ grafigi",
      show: "Barcha yechimlarni ko‘rsatish", hide: "Barcha yechimlarni yashirish",
    },
  }[FV.lang] || {};

  const n = (v, d = 3) => FV.num(Math.abs(v) < 1e-12 ? 0 : v, d);
  const tn = (v, d = 3) => n(v, d).replace("−", "-").replace(",", "{,}");
  const reduced = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const tex = (s) => FV.rich(s, "span");
  function setNote(el, s) { el.textContent = ""; el.append(tex(s)); }

  // ---------- 1. secant → tangent ----------
  const LIM = {
    sin2: { tex: "f(x) = \\sin 2x", f: (x) => Math.sin(2 * x), d: (x) => 2 * Math.cos(2 * x), x: [-0.5, 3.5], y: [-1.6, 1.6], x0: 0.4 },
    sqrt: { tex: "f(x) = \\sqrt{2x + 1}", f: (x) => Math.sqrt(2 * x + 1), d: (x) => 1 / Math.sqrt(2 * x + 1), x: [-0.5, 4], y: [-0.4, 3.4], x0: 0.8, min: -0.45 },
    gauss: { tex: "f(x) = e^{-x^2}", f: (x) => Math.exp(-x * x), d: (x) => -2 * x * Math.exp(-x * x), x: [-2.5, 2.5], y: [-0.4, 1.4], x0: -0.7 },
  };
  FV.widget("cr-limit", (el, cfg) => {
    const ui = FV.shell(el);
    let P = LIM[cfg.preset] || LIM.sin2, x0 = P.x0, h = cfg.h || 1, timer = 0;
    const plot = new FV.Plot(ui.stage, { x: P.x, y: P.y, aspect: 0.56, maxHeight: 420, xLabel: "x", yLabel: "f(x)" });
    const seg = FV.ui.seg({ label: L.fn, value: cfg.preset || "sin2", options: Object.keys(LIM).map((k) => ({ value: k, label: "$" + LIM[k].tex + "$" })), onchange: (k) => { P = LIM[k]; x0 = P.x0; range(); sx.set(x0); plot.setDomain(P.x, P.y); draw(); } });
    const sx = FV.ui.slider({ label: L.x0, min: -0.4, max: 3, step: 0.01, value: x0, oninput: (v) => { x0 = v; draw(); } });
    const range = () => { sx.input.min = Math.max(P.x[0], P.min != null ? P.min : -Infinity) + 0.05; sx.input.max = P.x[1] - 0.05; };
    range(); sx.set(x0);
    const sh = FV.ui.slider({ label: L.h, min: -1.5, max: 1.5, step: 0.001, value: h, fmt: (v) => n(v, 4), oninput: (v) => { stop(); h = v; draw(); } });
    const go = FV.ui.button({ label: L.shrink + " ▶", primary: true, onclick: () => (timer ? stop() : start()) });
    ui.controls.append(seg.el, sx.el, sh.el, go.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "q", label: L.dq, c: "orange" }, { key: "d", label: L.der, c: "blue" }, { key: "g", label: L.gap }]);
    function start() {
      if (Math.abs(h) < 0.002) h = 1;
      if (reduced()) { h = 0.001 * Math.sign(h || 1); sh.set(h); draw(); return; }
      go.setLabel("❚❚"); timer = setInterval(() => { h *= 0.93; if (Math.abs(h) < 0.001) { h = 0.001 * Math.sign(h); stop(); } sh.set(h); draw(); }, 60);
    }
    function stop() { clearInterval(timer); timer = 0; go.setLabel(L.shrink + " ▶"); }
    function draw() {
      const lo = Math.max(P.x[0], P.min != null ? P.min : -Infinity);
      x0 = FV.clamp(x0, lo + 0.05, P.x[1] - 0.05);
      let hh = Math.abs(h) < 1e-4 ? 1e-4 : h;
      if (x0 + hh < lo) hh = lo - x0 + 1e-3;
      const f = P.f, y0 = f(x0), y1 = f(x0 + hh), q = (y1 - y0) / hh, d = P.d(x0);
      plot.clear();
      plot.fn(f, { c: "ink", w: 2.2, from: lo });
      plot.line(P.x[0], y0 + d * (P.x[0] - x0), P.x[1], y0 + d * (P.x[1] - x0), { c: "blue", w: 1.6, dash: true });
      plot.line(P.x[0], y0 + q * (P.x[0] - x0), P.x[1], y0 + q * (P.x[1] - x0), { c: "orange", w: 2 });
      plot.line(x0, y0, x0 + hh, y0, { c: "guide", w: 1.2, dash: "3 3" });
      plot.line(x0 + hh, y0, x0 + hh, y1, { c: "guide", w: 1.2, dash: "3 3" });
      plot.text(x0 + hh / 2, y0, "h", { anchor: "middle", dy: y1 >= y0 ? 15 : -7, c: "ink" });
      plot.text(x0 + hh, (y0 + y1) / 2, "Δf", { dx: hh > 0 ? 6 : -6, anchor: hh > 0 ? "start" : "end", c: "ink" });
      plot.dot(x0, y0, { c: "blue", r: 5 }); plot.dot(x0 + hh, y1, { c: "orange", r: 5 });
      plot.legend([{ label: "$" + P.tex + "$", c: "ink" }, { label: L.secant, c: "orange" }, { label: L.tangent, c: "blue", dash: true }]);
      ro.set("q", n(q, 4)); ro.set("d", n(d, 4)); ro.set("g", n(q - d, 4));
      setNote(ui.note, L.limNote(tn(hh, 4), tn(q, 4), tn(d, 4)));
    }
    plot.onresize = draw;
    draw();
  });

  // ---------- 2. two links: x → u = g(x) → y = f(u) ----------
  const CH = {
    sinx2: { g: (x) => x * x, gd: (x) => 2 * x, f: Math.sin, fd: Math.cos, gt: "u = x^2", ft: "y = \\sin u", x: [-0.2, 2.2], u: [-0.3, 4.6], y: [-1.3, 1.3], x0: 0.8 },
    sq: { g: (x) => 3 * x + 1, gd: () => 3, f: (u) => u * u, fd: (u) => 2 * u, gt: "u = 3x + 1", ft: "y = u^2", x: [-1.2, 1.2], u: [-2.8, 4.8], y: [-1, 20], x0: 0.4 },
    expsin: { g: Math.sin, gd: Math.cos, f: Math.exp, fd: Math.exp, gt: "u = \\sin x", ft: "y = e^{u}", x: [-0.3, 3.4], u: [-1.2, 1.2], y: [-0.2, 3.1], x0: 0.6 },
  };
  FV.widget("cr-chain", (el, cfg) => {
    const ui = FV.shell(el, { cols: true });
    let P = CH[cfg.preset] || CH.sinx2, x0 = P.x0, dx = cfg.dx || 0.1;
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const p1 = new FV.Plot(c1, { x: P.x, y: P.u, aspect: 0.8, maxHeight: 330, xLabel: "x", yLabel: "u", title: L.gx });
    const p2 = new FV.Plot(c2, { x: P.u, y: P.y, aspect: 0.8, maxHeight: 330, xLabel: "u", yLabel: "y", title: L.fu });
    const seg = FV.ui.seg({ label: L.preset, value: cfg.preset || "sinx2", options: Object.keys(CH).map((k) => ({ value: k, label: "$" + CH[k].ft + ",\\ " + CH[k].gt + "$" })), onchange: (k) => { P = CH[k]; x0 = P.x0; p1.setDomain(P.x, P.u); p2.setDomain(P.u, P.y); sx.input.min = P.x[0] + 0.1; sx.input.max = P.x[1] - 0.1; sx.set(x0); draw(); } });
    const sx = FV.ui.slider({ label: L.x0, min: P.x[0] + 0.1, max: P.x[1] - 0.1, step: 0.01, value: x0, oninput: (v) => { x0 = v; draw(); } });
    const sd = FV.ui.slider({ label: L.dx, min: 0.01, max: 0.6, step: 0.01, value: dx, oninput: (v) => { dx = v; draw(); } });
    ui.controls.append(seg.el, sx.el, sd.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "g", label: L.gp, c: "teal" }, { key: "f", label: L.fp, c: "violet" }, { key: "p", label: L.prod, c: "blue" }, { key: "r", label: L.ratio, c: "orange" }]);
    function draw() {
      const u0 = P.g(x0), u1 = P.g(x0 + dx), du = u1 - u0, y0 = P.f(u0), y1 = P.f(u1), dy = y1 - y0;
      const gd = P.gd(x0), fd = P.fd(u0);
      p1.clear(); p2.clear();
      p1.fn(P.g, { c: "ink", w: 2.2 });
      p1.line(P.x[0], u0 + gd * (P.x[0] - x0), P.x[1], u0 + gd * (P.x[1] - x0), { c: "teal", w: 1.4, dash: true });
      p1.rect(x0, P.u[0], x0 + dx, P.u[0] + (P.u[1] - P.u[0]) * 0.03, { c: "orange", opacity: 0.9 });
      p1.rect(P.x[0], u0, P.x[0] + (P.x[1] - P.x[0]) * 0.03, u1, { c: "teal", opacity: 0.9 });
      p1.line(x0, P.u[0], x0, u0, { c: "guide", w: 1, dash: "3 3" }); p1.line(x0 + dx, P.u[0], x0 + dx, u1, { c: "guide", w: 1, dash: "3 3" });
      p1.line(P.x[0], u0, x0, u0, { c: "guide", w: 1, dash: "3 3" }); p1.line(P.x[0], u1, x0 + dx, u1, { c: "guide", w: 1, dash: "3 3" });
      p1.dot(x0, u0, { c: "teal" }); p1.dot(x0 + dx, u1, { c: "teal", hollow: true });
      p2.fn(P.f, { c: "ink", w: 2.2 });
      p2.line(P.u[0], y0 + fd * (P.u[0] - u0), P.u[1], y0 + fd * (P.u[1] - u0), { c: "violet", w: 1.4, dash: true });
      p2.rect(u0, P.y[0], u1, P.y[0] + (P.y[1] - P.y[0]) * 0.03, { c: "teal", opacity: 0.9 });
      p2.rect(P.u[0], y0, P.u[0] + (P.u[1] - P.u[0]) * 0.03, y1, { c: "violet", opacity: 0.9 });
      p2.line(u0, P.y[0], u0, y0, { c: "guide", w: 1, dash: "3 3" }); p2.line(u1, P.y[0], u1, y1, { c: "guide", w: 1, dash: "3 3" });
      p2.line(P.u[0], y0, u0, y0, { c: "guide", w: 1, dash: "3 3" }); p2.line(P.u[0], y1, u1, y1, { c: "guide", w: 1, dash: "3 3" });
      p2.dot(u0, y0, { c: "violet" }); p2.dot(u1, y1, { c: "violet", hollow: true });
      p1.legend([{ label: "$\\Delta x$", c: "orange", box: true }, { label: "$\\Delta u$", c: "teal", box: true }]);
      p2.legend([{ label: "$\\Delta u$", c: "teal", box: true }, { label: "$\\Delta y$", c: "violet", box: true }]);
      ro.set("g", n(gd)); ro.set("f", n(fd)); ro.set("p", n(gd * fd)); ro.set("r", n(dy / dx));
      setNote(ui.note, L.chainNote(tn(dx, 2), tn(gd * dx), tn(fd * gd * dx), tn(gd), tn(fd)));
    }
    p1.onresize = draw; p2.onresize = draw;
    draw();
  });

  // ---------- 3. a path over the level lines: dz/dt = f_x x′ + f_y y′ ----------
  const TAU = 2 * Math.PI;
  const PA = {
    x2y: { tex: "z = x^2 y,\\ x = \\cos t,\\ y = \\sin t", f: (x, y) => x * x * y, fx: (x, y) => 2 * x * y, fy: (x) => x * x,
      r: (t) => [Math.cos(t), Math.sin(t)], v: (t) => [-Math.sin(t), Math.cos(t)], t: [0, TAU], t0: 0.9, X: [-1.5, 1.5], Y: [-1.3, 1.3], Z: [-0.5, 0.5], levels: [-0.6, -0.4, -0.25, -0.12, -0.04, 0.04, 0.12, 0.25, 0.4, 0.6] },
    circle: { tex: "z = x^2 + y^2,\\ x = \\cos t,\\ y = \\sin t", f: (x, y) => x * x + y * y, fx: (x) => 2 * x, fy: (x, y) => 2 * y,
      r: (t) => [Math.cos(t), Math.sin(t)], v: (t) => [-Math.sin(t), Math.cos(t)], t: [0, TAU], t0: 0.9, X: [-1.5, 1.5], Y: [-1.3, 1.3], Z: [0, 2], levels: [0.25, 0.5, 1, 1.5, 2, 2.5] },
    xy: { tex: "z = xy,\\ x = t,\\ y = t^2 - 1", f: (x, y) => x * y, fx: (x, y) => y, fy: (x) => x,
      r: (t) => [t, t * t - 1], v: (t) => [1, 2 * t], t: [-1.4, 1.4], t0: -0.8, X: [-1.6, 1.6], Y: [-1.2, 1.2], Z: [-0.6, 1.4], levels: [-1, -0.6, -0.3, -0.1, 0.1, 0.3, 0.6, 1] },
  };
  FV.widget("cr-path", (el, cfg) => {
    const ui = FV.shell(el, { cols: true });
    let P = PA[cfg.preset] || PA.x2y, t0 = P.t0, timer = 0;
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const p1 = new FV.Plot(c1, { x: P.X, y: P.Y, equal: true, xLabel: "x", yLabel: "y", title: L.plane });
    const p2 = new FV.Plot(c2, { x: P.t, y: P.Z, aspect: 0.8, maxHeight: 330, xLabel: "t", yLabel: "z", title: L.graph });
    const seg = FV.ui.seg({ label: L.preset, value: cfg.preset || "x2y", options: Object.keys(PA).map((k) => ({ value: k, label: "$" + PA[k].tex + "$" })), onchange: (k) => { stop(); P = PA[k]; t0 = P.t0; p1.setDomain(P.X, P.Y); p2.setDomain(P.t, P.Z); st.input.min = P.t[0]; st.input.max = P.t[1]; st.set(t0); draw(); } });
    const st = FV.ui.slider({ label: L.t, min: P.t[0], max: P.t[1], step: 0.01, value: t0, oninput: (v) => { stop(); t0 = v; draw(); } });
    const play = FV.ui.button({ label: "▶ " + FV.t("play"), primary: true, onclick: () => (timer ? stop() : start()) });
    ui.controls.append(seg.el, st.el, play.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "a", label: L.cx, c: "red" }, { key: "b", label: L.cy, c: "blue" }, { key: "s", label: L.dzdt, c: "orange" }, { key: "n", label: L.numeric }]);
    function start() {
      if (reduced()) { t0 = FV.clamp(t0 + 0.5, P.t[0], P.t[1]); st.set(t0); draw(); return; }
      play.setLabel("❚❚ " + FV.t("pause"));
      timer = setInterval(() => { t0 += (P.t[1] - P.t[0]) / 240; if (t0 > P.t[1]) t0 = P.t[0]; st.set(t0); draw(); }, 50);
    }
    function stop() { clearInterval(timer); timer = 0; play.setLabel("▶ " + FV.t("play")); }
    let bg = null;
    function draw() {
      const [x, y] = P.r(t0), [vx, vy] = P.v(t0), fx = P.fx(x, y), fy = P.fy(x, y), a = fx * vx, b = fy * vy, s = a + b;
      const z = (t) => { const [u, w] = P.r(t); return P.f(u, w); }, e = 1e-5, num = (z(t0 + e) - z(t0 - e)) / (2 * e);
      p1.clear();
      p1.heat(P.f, { cmap: "diverging", alpha: 0.35, res: 4 });
      p1.contours(P.f, P.levels, { c: "ink", w: 1, opacity: 0.35 });
      const pts = FV.linspace(P.t[0], P.t[1], 240).map(P.r);
      p1.path(pts, { c: "ink", w: 2.2 });
      const g = Math.hypot(fx, fy), kg = g > 0 ? Math.min(0.55, 0.35 * g) / g : 0;
      p1.arrow(x, y, x + fx * kg, y + fy * kg, { c: "red", w: 2.4 });
      const kv = 0.45 / (Math.hypot(vx, vy) || 1);
      p1.arrow(x, y, x + vx * kv, y + vy * kv, { c: "blue", w: 2.4 });
      p1.dot(x, y, { c: "orange", r: 6 });
      p1.legend([{ label: L.path, c: "ink" }, { label: L.grad, c: "red" }, { label: L.vel, c: "blue" }, { label: L.levels, c: "ink", dash: true }]);
      p2.clear();
      p2.fn(z, { c: "ink", w: 2.2 });
      p2.line(P.t[0], z(t0) + s * (P.t[0] - t0), P.t[1], z(t0) + s * (P.t[1] - t0), { c: "orange", w: 1.8, dash: true });
      p2.dot(t0, z(t0), { c: "orange", r: 6 });
      p2.legend([{ label: L.zt, c: "ink" }, { label: L.tangent, c: "orange", dash: true }]);
      ro.set("a", n(a)); ro.set("b", n(b)); ro.set("s", n(s)); ro.set("n", n(num));
      setNote(ui.note, L.pathNote(tn(a), tn(b), tn(s)) + (P === PA.circle ? L.zero : ""));
    }
    p1.onresize = draw; p2.onresize = draw;
    draw();
  });

  // ---------- 4. the practice: open or close every solution at once ----------
  FV.widget("cr-solutions", (el) => {
    el.classList.add("cr-sol-bar");
    let open = false;
    const b = FV.ui.button({ label: L.show, onclick: () => { open = !open; document.querySelectorAll("details.cr-sol").forEach((d) => { d.open = open; }); b.setLabel(open ? L.hide : L.show); } });
    el.textContent = ""; el.append(b.el);
  });
})();
