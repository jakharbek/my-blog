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
      chainNote: (dx, du, dy, gp, fp, real) => `Линейная оценка: внутренняя функция умножает шаг $\\Delta x = ${dx}$ на $g'(x_0) \\approx ${gp}$ — получается $\\Delta u \\approx ${du}$; внешняя умножает этот шаг на $f'(u_0) \\approx ${fp}$ — получается $\\Delta y \\approx ${dy}$ (на самом деле $\\Delta y = ${real}$). Коэффициенты перемножаются; чем меньше $\\Delta x$, тем точнее оценка.`,
      t: "Параметр $t$", path: "путь $(x(t), y(t))$", grad: "$\\nabla f$", vel: "$(x'(t), y'(t))$", zt: "$z(t) = f(x(t), y(t))$",
      cx: "$f_x \\cdot x'$", cy: "$f_y \\cdot y'$", dzdt: "$dz/dt$", numeric: "численно",
      pathNote: (a, b, s) => `Вклад пути через $x$: $${a}$, через $y$: $${b}$. Сумма $\\frac{dz}{dt} = ${s}$ — это наклон касательной к графику $z(t)$.`,
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
      chainNote: (dx, du, dy, gp, fp, real) => `Linear estimate: the inner function multiplies the step $\\Delta x = ${dx}$ by $g'(x_0) \\approx ${gp}$, giving $\\Delta u \\approx ${du}$; the outer function multiplies that step by $f'(u_0) \\approx ${fp}$, giving $\\Delta y \\approx ${dy}$ (the actual $\\Delta y = ${real}$). The factors multiply; the smaller $\\Delta x$, the better the estimate.`,
      t: "Parameter $t$", path: "path $(x(t), y(t))$", grad: "$\\nabla f$", vel: "$(x'(t), y'(t))$", zt: "$z(t) = f(x(t), y(t))$",
      cx: "$f_x \\cdot x'$", cy: "$f_y \\cdot y'$", dzdt: "$dz/dt$", numeric: "numerically",
      pathNote: (a, b, s) => `The contribution of the path through $x$: $${a}$, through $y$: $${b}$. The sum $\\frac{dz}{dt} = ${s}$ is the slope of the tangent to the graph of $z(t)$.`,
      zero: " Here the path runs along a level curve, and the contributions cancel out.",
      levels: "level curves of $f$", plane: "The $(x, y)$ plane", graph: "The graph of $z(t)$",
      show: "Show all solutions", hide: "Hide all solutions",
    },
    uz: {
      fn: "Funksiya", x0: "$x_0$ nuqta", h: "$h$ qadam", shrink: "h → 0", secant: "kesuvchi", tangent: "urinma",
      dq: "Ayirmali nisbat", der: "$f'(x_0)$ hosila", gap: "Farq",
      limNote: (h, q, d) => `$h = ${h}$ da kesuvchining qiyaligi $\\frac{f(x_0 + h) - f(x_0)}{h} = ${q}$; $h \\to 0$ dagi limiti — urinmaning qiyaligi $f'(x_0) = ${d}$.`,
      preset: "Misol", dx: "$\\Delta x$ qadam", gx: "$u = g(x)$", fu: "$y = f(u)$",
      gp: "$g'(x_0)$", fp: "$f'(u_0)$", prod: "$f'(u_0)\\cdot g'(x_0)$", ratio: "$\\Delta y / \\Delta x$",
      chainNote: (dx, du, dy, gp, fp, real) => `Chiziqli baho: ichki funksiya $\\Delta x = ${dx}$ qadamni $g'(x_0) \\approx ${gp}$ ga ko‘paytiradi — $\\Delta u \\approx ${du}$ hosil bo‘ladi; tashqi funksiya bu qadamni $f'(u_0) \\approx ${fp}$ ga ko‘paytiradi — $\\Delta y \\approx ${dy}$ hosil bo‘ladi (aslida $\\Delta y = ${real}$). Koeffitsiyentlar ko‘paytiriladi; $\\Delta x$ qancha kichik bo‘lsa, baho shuncha aniq.`,
      t: "$t$ parametr", path: "$(x(t), y(t))$ yo‘l", grad: "$\\nabla f$", vel: "$(x'(t), y'(t))$", zt: "$z(t) = f(x(t), y(t))$",
      cx: "$f_x \\cdot x'$", cy: "$f_y \\cdot y'$", dzdt: "$dz/dt$", numeric: "sonli",
      pathNote: (a, b, s) => `$x$ orqali yo‘l hissasi: $${a}$, $y$ orqali: $${b}$. Yig‘indi $\\frac{dz}{dt} = ${s}$ — $z(t)$ grafigiga urinmaning qiyaligi.`,
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
  // A play/pause button with a stable accessible name; the glyphs are decoration.
  function toggleButton(label, onclick) {
    const b = FV.ui.button({ label: "", primary: true, onclick });
    const set = (on) => {
      b.el.textContent = "";
      b.el.append(FV.h("span", { "aria-hidden": "true", text: on ? "❚❚ " : "▶ " }), FV.rich(on ? FV.t("pause") : label));
      b.el.setAttribute("aria-pressed", on ? "true" : "false");
    };
    set(false);
    return { el: b.el, set };
  }
  // While an animation runs, the note is rewritten many times a second: keep it out of the live region until it stops.
  function quiet(note, on) { note.setAttribute("aria-live", on ? "off" : "polite"); }
  // Scale an arrow from (x, y) by (dx, dy) so that its tip stays inside the plot frame.
  function fit(P, X, Y, x, y, dx, dy) {
    let k = 1;
    const m = 0.04 * (X[1] - X[0]);
    if (x + dx > X[1] - m) k = Math.min(k, (X[1] - m - x) / dx);
    if (x + dx < X[0] + m) k = Math.min(k, (X[0] + m - x) / dx);
    if (y + dy > Y[1] - m) k = Math.min(k, (Y[1] - m - y) / dy);
    if (y + dy < Y[0] + m) k = Math.min(k, (Y[0] + m - y) / dy);
    return Math.max(0, k);
  }

  // ---------- 1. secant → tangent ----------
  // dom: where f is defined (the curve is drawn there); lo: the smallest x₀ the slider offers.
  const LIM = {
    sin2: { tex: "f(x) = \\sin 2x", f: (x) => Math.sin(2 * x), d: (x) => 2 * Math.cos(2 * x), x: [-0.5, 3.5], y: [-1.6, 1.6], x0: 0.4 },
    sqrt: { tex: "f(x) = \\sqrt{2x + 1}", f: (x) => Math.sqrt(Math.max(0, 2 * x + 1)), d: (x) => 1 / Math.sqrt(2 * x + 1), x: [-0.6, 4], y: [-0.4, 3.4], x0: 0.8, dom: -0.5, lo: -0.45 },
    gauss: { tex: "f(x) = e^{-x^2}", f: (x) => Math.exp(-x * x), d: (x) => -2 * x * Math.exp(-x * x), x: [-2.5, 2.5], y: [-0.4, 1.4], x0: -0.7 },
  };
  FV.widget("cr-limit", (el, cfg) => {
    const ui = FV.shell(el);
    let P = LIM[cfg.preset] || LIM.sin2, x0 = P.x0, h = cfg.h || 1, timer = 0;
    const plot = new FV.Plot(ui.stage, { x: P.x, y: P.y, aspect: 0.56, maxHeight: 420, xLabel: "x", yLabel: "f(x)" });
    const left = () => (P.dom != null ? P.dom : P.x[0]);
    const seg = FV.ui.seg({ label: L.fn, value: cfg.preset || "sin2", options: Object.keys(LIM).map((k) => ({ value: k, label: "$" + LIM[k].tex + "$" })), onchange: (k) => { stop(); P = LIM[k]; x0 = P.x0; plot.setDomain(P.x, P.y); ranges(); draw(); } });
    const sx = FV.ui.slider({ label: L.x0, min: -0.4, max: 3, step: 0.01, value: x0, oninput: (v) => { x0 = v; ranges(); draw(); } });
    const sh = FV.ui.slider({ label: L.h, min: -1.5, max: 1.5, step: 0.001, value: h, fmt: (v) => n(v, 4), oninput: (v) => { stop(); h = v; draw(); } });
    // x₀ stays inside the frame, and x₀ + h inside the domain and the frame: the slider value is always the h that is drawn
    function ranges() {
      sx.input.min = (P.lo != null ? P.lo : P.x[0] + 0.05); sx.input.max = P.x[1] - 0.05;
      x0 = FV.clamp(x0, +sx.input.min, +sx.input.max); sx.set(x0);
      const a = Math.max(-1.5, left() - x0), b = Math.min(1.5, P.x[1] - x0);
      sh.input.min = a; sh.input.max = b;
      h = FV.clamp(h, a, b); sh.set(h);
    }
    const go = toggleButton(L.shrink, () => (timer ? stop() : start()));
    ui.controls.append(seg.el, sx.el, sh.el, go.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "q", label: L.dq, c: "orange" }, { key: "d", label: L.der, c: "blue" }, { key: "g", label: L.gap }]);
    function start() {
      const sg = Math.sign(h) || 1;
      if (Math.abs(h) < 0.002) h = sg * Math.min(1, sg > 0 ? +sh.input.max : -sh.input.min);
      if (reduced()) { h = 0.001 * sg; sh.set(h); draw(); return; }
      go.set(true); quiet(ui.note, true);
      timer = setInterval(() => { h *= 0.93; if (Math.abs(h) < 0.001) { h = 0.001 * sg; stop(); } sh.set(h); draw(); }, 60);
    }
    function stop() { clearInterval(timer); timer = 0; go.set(false); quiet(ui.note, false); }
    document.addEventListener("visibilitychange", () => { if (document.hidden && timer) stop(); });
    function draw() {
      const hh = Math.abs(h) < 1e-4 ? (Math.sign(h) || 1) * 1e-4 : h;
      const f = P.f, y0 = f(x0), y1 = f(x0 + hh), q = (y1 - y0) / hh, d = P.d(x0);
      plot.clear();
      plot.fn(f, { c: "ink", w: 2.2, from: left() });
      plot.line(P.x[0], y0 + d * (P.x[0] - x0), P.x[1], y0 + d * (P.x[1] - x0), { c: "blue", w: 1.6, dash: true });
      plot.line(P.x[0], y0 + q * (P.x[0] - x0), P.x[1], y0 + q * (P.x[1] - x0), { c: "orange", w: 2 });
      plot.line(x0, y0, x0 + hh, y0, { c: "guide", w: 1.2, dash: "3 3" });
      plot.line(x0 + hh, y0, x0 + hh, y1, { c: "guide", w: 1.2, dash: "3 3" });
      // the labels only when the step is wide enough to hold them, and always inside the frame
      if (Math.abs(plot.X(x0 + hh) - plot.X(x0)) > 22) {
        plot.text(x0 + hh / 2, y0, "h", { anchor: "middle", dy: y1 >= y0 ? 15 : -7, c: "ink", clip: true });
        if (Math.abs(plot.Y(y1) - plot.Y(y0)) > 16) plot.text(x0 + hh, (y0 + y1) / 2, "Δf", { dx: hh > 0 ? -6 : 6, anchor: hh > 0 ? "end" : "start", c: "ink", clip: true });
      }
      plot.dot(x0, y0, { c: "blue", r: 5 }); plot.dot(x0 + hh, y1, { c: "orange", r: 5 });
      plot.legend([{ label: "$" + P.tex + "$", c: "ink" }, { label: L.secant, c: "orange" }, { label: L.tangent, c: "blue", dash: true }]);
      ro.set("q", n(q, 4)); ro.set("d", n(d, 4)); ro.set("g", n(q - d, 4));
      setNote(ui.note, L.limNote(tn(hh, 4), tn(q, 4), tn(d, 4)));
    }
    plot.onresize = draw;
    ranges();
    draw();
  });

  // ---------- 2. two links: x → u = g(x) → y = f(u) ----------
  // The plot ranges hold every point the sliders can reach: x₀ + Δx ≤ x[1].
  const CH = {
    sinx2: { g: (x) => x * x, gd: (x) => 2 * x, f: Math.sin, fd: Math.cos, gt: "u = x^2", ft: "y = \\sin u", x: [-0.2, 2.2], u: [-0.3, 5], y: [-1.3, 1.3], x0: 0.8 },
    sq: { g: (x) => 3 * x + 1, gd: () => 3, f: (u) => u * u, fd: (u) => 2 * u, gt: "u = 3x + 1", ft: "y = u^2", x: [-1.2, 1.2], u: [-2.8, 4.8], y: [-1, 22], x0: 0.4 },
    expsin: { g: Math.sin, gd: Math.cos, f: Math.exp, fd: Math.exp, gt: "u = \\sin x", ft: "y = e^{u}", x: [-0.3, 3.4], u: [-1.2, 1.2], y: [-0.2, 3.1], x0: 0.6 },
  };
  FV.widget("cr-chain", (el, cfg) => {
    const ui = FV.shell(el, { cols: true });
    let P = CH[cfg.preset] || CH.sinx2, x0 = P.x0, dx = cfg.dx || 0.1;
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const p1 = new FV.Plot(c1, { x: P.x, y: P.u, aspect: 0.8, maxHeight: 330, xLabel: "x", yLabel: "u", title: L.gx });
    const p2 = new FV.Plot(c2, { x: P.u, y: P.y, aspect: 0.8, maxHeight: 330, xLabel: "u", yLabel: "y", title: L.fu });
    const seg = FV.ui.seg({ label: L.preset, value: cfg.preset || "sinx2", options: Object.keys(CH).map((k) => ({ value: k, label: "$" + CH[k].ft + ",\\ " + CH[k].gt + "$" })), onchange: (k) => { P = CH[k]; x0 = P.x0; p1.setDomain(P.x, P.u); p2.setDomain(P.u, P.y); ranges(); draw(); } });
    const sx = FV.ui.slider({ label: L.x0, min: P.x[0] + 0.1, max: P.x[1] - 0.1, step: 0.01, value: x0, oninput: (v) => { x0 = v; ranges(); draw(); } });
    const sd = FV.ui.slider({ label: L.dx, min: 0.01, max: 0.6, step: 0.01, value: dx, oninput: (v) => { dx = v; draw(); } });
    function ranges() {
      sx.input.min = P.x[0] + 0.1; sx.input.max = P.x[1] - 0.1; x0 = FV.clamp(x0, P.x[0] + 0.1, P.x[1] - 0.1); sx.set(x0);
      const m = Math.max(0.01, Math.min(0.6, Math.floor((P.x[1] - x0) * 100) / 100));
      sd.input.max = m; dx = FV.clamp(dx, 0.01, m); sd.set(dx);
    }
    ui.controls.append(seg.el, sx.el, sd.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "g", label: L.gp, c: "teal" }, { key: "f", label: L.fp, c: "violet" }, { key: "p", label: L.prod, c: "blue" }, { key: "r", label: L.ratio, c: "orange" }]);
    function draw() {
      const u0 = P.g(x0), u1 = P.g(x0 + dx), y0 = P.f(u0), y1 = P.f(u1), dy = y1 - y0;
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
      setNote(ui.note, L.chainNote(tn(dx, 2), tn(gd * dx), tn(fd * gd * dx), tn(gd), tn(fd), tn(dy)));
    }
    let raf = 0;
    p1.onresize = p2.onresize = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); };
    ranges();
    draw();
  });

  // ---------- 3. a path over the level curves: dz/dt = f_x x′ + f_y y′ ----------
  const TAU = 2 * Math.PI;
  const PA = {
    x2y: { tex: "z = x^2 y,\\ x = \\cos t,\\ y = \\sin t", f: (x, y) => x * x * y, fx: (x, y) => 2 * x * y, fy: (x) => x * x,
      r: (t) => [Math.cos(t), Math.sin(t)], v: (t) => [-Math.sin(t), Math.cos(t)], t: [0, TAU], t0: 0.9, X: [-1.5, 1.5], Y: [-1.3, 1.3], Z: [-0.5, 0.5], cmap: "diverging", heatZ: [-1, 1], levels: [-0.6, -0.4, -0.25, -0.12, -0.04, 0.04, 0.12, 0.25, 0.4, 0.6] },
    circle: { tex: "z = x^2 + y^2,\\ x = \\cos t,\\ y = \\sin t", f: (x, y) => x * x + y * y, fx: (x) => 2 * x, fy: (x, y) => 2 * y,
      r: (t) => [Math.cos(t), Math.sin(t)], v: (t) => [-Math.sin(t), Math.cos(t)], t: [0, TAU], t0: 0.9, X: [-1.5, 1.5], Y: [-1.3, 1.3], Z: [0, 2], cmap: "blues", levels: [0.25, 0.5, 1, 1.5, 2, 2.5] },
    xy: { tex: "z = xy,\\ x = t,\\ y = t^2 - 1", f: (x, y) => x * y, fx: (x, y) => y, fy: (x) => x,
      r: (t) => [t, t * t - 1], v: (t) => [1, 2 * t], t: [-1.4, 1.4], t0: -0.8, X: [-1.6, 1.6], Y: [-1.2, 1.2], Z: [-1.5, 1.5], cmap: "diverging", heatZ: [-2, 2], levels: [-1, -0.6, -0.3, -0.1, 0.1, 0.3, 0.6, 1] },
  };
  FV.widget("cr-path", (el, cfg) => {
    const ui = FV.shell(el, { cols: true });
    let P = PA[cfg.preset] || PA.x2y, t0 = P.t0, timer = 0;
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const p1 = new FV.Plot(c1, { x: P.X, y: P.Y, equal: true, xLabel: "x", yLabel: "y", title: L.plane });
    const p2 = new FV.Plot(c2, { x: P.t, y: P.Z, aspect: 0.8, maxHeight: 330, xLabel: "t", yLabel: "z", title: L.graph });
    const seg = FV.ui.seg({ label: L.preset, value: cfg.preset || "x2y", options: Object.keys(PA).map((k) => ({ value: k, label: "$" + PA[k].tex + "$" })), onchange: (k) => { stop(); P = PA[k]; t0 = P.t0; p1.setDomain(P.X, P.Y); p2.setDomain(P.t, P.Z); st.input.min = P.t[0]; st.input.max = P.t[1]; st.set(t0); bg = null; draw(); } });
    const st = FV.ui.slider({ label: L.t, min: P.t[0], max: P.t[1], step: 0.01, value: t0, oninput: (v) => { stop(); t0 = v; draw(); } });
    const play = toggleButton(FV.t("play"), () => (timer ? stop() : start()));
    ui.controls.append(seg.el, st.el, play.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "a", label: L.cx, c: "red" }, { key: "b", label: L.cy, c: "blue" }, { key: "s", label: L.dzdt, c: "orange" }, { key: "n", label: L.numeric }]);
    const wrap = (t) => (t > P.t[1] ? P.t[0] + (t - P.t[1]) : t);
    function start() {
      if (reduced()) { t0 = wrap(t0 + (P.t[1] - P.t[0]) / 12); st.set(t0); draw(); return; }
      play.set(true); quiet(ui.note, true);
      timer = setInterval(() => { t0 = wrap(t0 + (P.t[1] - P.t[0]) / 240); st.set(t0); draw(); }, 50);
    }
    function stop() { clearInterval(timer); timer = 0; play.set(false); quiet(ui.note, false); }
    document.addEventListener("visibilitychange", () => { if (document.hidden && timer) stop(); });
    // The level curves, the heat map and the path depend only on the preset and the size: drawn once, under a layer redrawn every frame.
    let bg = null, dyn1 = null, dyn2 = null;
    const z = (t) => { const [u, w] = P.r(t); return P.f(u, w); };
    function background() {
      p1.clear();
      p1.heat(P.f, { cmap: P.cmap, alpha: 0.35, res: 4, z: P.heatZ });
      p1.contours(P.f, P.levels, { c: "ink", w: 1, opacity: 0.35 });
      p1.path(FV.linspace(P.t[0], P.t[1], 240).map(P.r), { c: "ink", w: 2.2 });
      p1.legend([{ label: L.path, c: "ink" }, { label: L.grad, c: "red" }, { label: L.vel, c: "blue" }, { label: L.levels, c: "ink" }]);
      dyn1 = FV.svg("g", {}, p1.gMain);
      p2.clear();
      p2.fn(z, { c: "ink", w: 2.2 });
      p2.legend([{ label: L.zt, c: "ink" }, { label: L.tangent, c: "orange", dash: true }]);
      dyn2 = FV.svg("g", {}, p2.gMain);
      bg = P;
    }
    const into = (plot, g, fn) => { const keep = plot.gMain; plot.gMain = g; try { fn(); } finally { plot.gMain = keep; } };
    function draw() {
      if (bg !== P) background();
      const [x, y] = P.r(t0), [vx, vy] = P.v(t0), fx = P.fx(x, y), fy = P.fy(x, y), a = fx * vx, b = fy * vy, s = a + b;
      const e = 1e-4, num = (z(t0 + e) - z(t0 - e)) / (2 * e);
      dyn1.textContent = ""; dyn2.textContent = "";
      into(p1, dyn1, () => {
        const g = Math.hypot(fx, fy), kg = g > 0 ? Math.min(0.55, 0.35 * g) / g : 0;
        const k1 = fit(P, P.X, P.Y, x, y, fx * kg, fy * kg);
        p1.arrow(x, y, x + fx * kg * k1, y + fy * kg * k1, { c: "red", w: 2.4 });
        const kv = 0.45 / (Math.hypot(vx, vy) || 1), k2 = fit(P, P.X, P.Y, x, y, vx * kv, vy * kv);
        p1.arrow(x, y, x + vx * kv * k2, y + vy * kv * k2, { c: "blue", w: 2.4 });
        p1.dot(x, y, { c: "orange", r: 6 });
      });
      into(p2, dyn2, () => {
        p2.line(P.t[0], z(t0) + s * (P.t[0] - t0), P.t[1], z(t0) + s * (P.t[1] - t0), { c: "orange", w: 1.8, dash: true });
        p2.dot(t0, z(t0), { c: "orange", r: 6 });
      });
      const r = (v) => (Math.abs(v) < 1e-7 ? 0 : v);
      ro.set("a", n(r(a))); ro.set("b", n(r(b))); ro.set("s", n(r(s))); ro.set("n", n(r(num)));
      setNote(ui.note, L.pathNote(tn(r(a)), tn(r(b)), tn(r(s))) + (P === PA.circle ? L.zero : ""));
    }
    let raf = 0;
    p1.onresize = p2.onresize = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => { bg = null; draw(); }); };
    draw();
  });

  // ---------- 4. the practice: open or close every solution at once ----------
  FV.widget("cr-solutions", (el) => {
    el.classList.add("cr-sol-bar");
    const all = () => Array.from(document.querySelectorAll("details.cr-sol"));
    const b = FV.ui.button({ label: L.show, onclick: () => { const open = all().some((d) => !d.open); all().forEach((d) => { d.open = open; }); sync(); } });
    function sync() {
      const open = all().every((d) => d.open);
      b.setLabel(open ? L.hide : L.show);
      b.el.setAttribute("aria-expanded", open ? "true" : "false");
    }
    // a solution opened or closed by hand keeps the button honest ("toggle" does not bubble: listen in the capture phase)
    document.addEventListener("toggle", (e) => { if (e.target.matches && e.target.matches("details.cr-sol")) sync(); }, true);
    el.textContent = ""; el.append(b.el);
    sync();
  });
})();
