/* Widgets of the article "The derivative, partial derivatives and the gradient". Built on FV (assets/js/viz.js).
   dr-slope    — the slope of a line: Δy ÷ Δx between two draggable points;
   dr-tail     — Δf = f′(x)·Δx + tail: the secant turns into the tangent, the tail vanishes faster than Δx;
   dr-partial  — the partial derivatives as slopes of the two slices of a surface through a point;
   dr-grad     — the gradient field over the level curves and the directional derivative ∇f·u;
   dr-descent  — gradient descent p ← p − η∇f on a bowl. */
(function () {
  "use strict";
  if (typeof FV === "undefined" || !FV.widget) return;

  const L = {
    ru: {
      ptA: "точка A", ptB: "точка B", line: "прямая", run: "вправо $\\Delta x$", rise: "вверх $\\Delta y$", slope: "наклон $\\Delta y / \\Delta x$",
      slopeNote: (a, b, dx, dy, k) => `Из $A = ${a}$ в $B = ${b}$: прошли вправо $\\Delta x = ${dx}$, поднялись на $\\Delta y = ${dy}$. Наклон $= \\Delta y \\div \\Delta x = ${k}$ — на каждый шаг вправо прямая меняется на $${k}$. Перетащите точки: у прямой наклон одинаков для любой пары точек.`,
      vertical: "Точки стоят на одной вертикали: $\\Delta x = 0$, делить на ноль нельзя — у вертикальной прямой наклона нет.",
      x0: "Точка $x_0$", dx: "Шаг $\\Delta x$", shrink: "Δx → 0", fn: "Функция",
      exact: "точное $\\Delta f$", linp: "линейная часть $f'(x_0)\\,\\Delta x$", tailw: "хвост", secSlope: "$\\Delta f / \\Delta x$", der: "$f'(x_0)$",
      secant: "секущая", tangent: "касательная",
      tailNote: (dx, df, lin, tail, share) => `При $\\Delta x = ${dx}$: $\\Delta f = ${df}$, из них линейная часть $${lin}$ и хвост $${tail}$ (${share} % от $\\Delta f$). Уменьшайте шаг: хвост исчезает быстрее, чем $\\Delta x$, и наклон секущей стремится к $f'(x_0)$.`,
      surf: "Функция", px: "$x_0$", py: "$y_0$", map: "Линии уровня $f(x, y)$", sliceX: "Срез $y = y_0$: функция от $x$", sliceY: "Срез $x = x_0$: функция от $y$",
      fx: "$\\partial f / \\partial x$", fy: "$\\partial f / \\partial y$", fval: "$f(x_0, y_0)$",
      partNote: (fx, fy) => `Заморозили $y$ — осталась функция одной переменной $x$, её наклон в точке $\\partial f / \\partial x = ${fx}$. Заморозили $x$ — наклон по $y$ равен $\\partial f / \\partial y = ${fy}$.`,
      dir: "Направление $\\mathbf{u}$, угол", grad: "$\\nabla f$", uvec: "$\\mathbf{u}$", field: "поле градиентов", gnorm: "$|\\nabla f|$", du: "$D_{\\mathbf{u}} f = \\nabla f\\cdot\\mathbf{u}$",
      gradNote: (g, n, d, ang) => `$\\nabla f = ${g}$, длина $${n}$. Вдоль $\\mathbf{u}$ функция меняется со скоростью $D_{\\mathbf{u}} f = |\\nabla f|\\cos\\varphi = ${d}$, где $\\varphi = ${ang}^{\\circ}$ — угол между $\\mathbf{u}$ и $\\nabla f$. Максимум — когда $\\mathbf{u}$ смотрит вдоль градиента, ноль — вдоль линии уровня.`,
      flat: "В этой точке $\\nabla f = \\mathbf{0}$: функция «плоская» во всех направлениях — это кандидат в минимум, максимум или седло.",
      eta: "Шаг $\\eta$", start: "Старт", go: "Спуск", reset: "Сброс", step: "шаг", path: "путь спуска",
      descNote: (k, p, f, m) => `Шаг ${k}: $\\mathbf{p} = ${p}$, $f = ${f}$. Для этой чаши каждый шаг умножает $x$ на $${m}$, а $y$ — на свой множитель (см. текст).`,
      show: "Показать все решения", hide: "Скрыть все решения",
      thK: "шаг", thP: "$\\mathbf{p}$", thG: "$\\nabla f(\\mathbf{p})$", thF: "$f(\\mathbf{p})$",
    },
    en: {
      ptA: "point A", ptB: "point B", line: "line", run: "run $\\Delta x$", rise: "rise $\\Delta y$", slope: "slope $\\Delta y / \\Delta x$",
      slopeNote: (a, b, dx, dy, k) => `From $A = ${a}$ to $B = ${b}$: we moved right by $\\Delta x = ${dx}$ and rose by $\\Delta y = ${dy}$. Slope $= \\Delta y \\div \\Delta x = ${k}$ — for every step to the right the line changes by $${k}$. Drag the points: a line has the same slope for any pair of its points.`,
      vertical: "The points are on one vertical: $\\Delta x = 0$, and we cannot divide by zero — a vertical line has no slope.",
      x0: "Point $x_0$", dx: "Step $\\Delta x$", shrink: "Δx → 0", fn: "Function",
      exact: "exact $\\Delta f$", linp: "linear part $f'(x_0)\\,\\Delta x$", tailw: "tail", secSlope: "$\\Delta f / \\Delta x$", der: "$f'(x_0)$",
      secant: "secant", tangent: "tangent",
      tailNote: (dx, df, lin, tail, share) => `At $\\Delta x = ${dx}$: $\\Delta f = ${df}$, of which the linear part is $${lin}$ and the tail is $${tail}$ (${share} % of $\\Delta f$). Make the step smaller: the tail vanishes faster than $\\Delta x$, and the slope of the secant tends to $f'(x_0)$.`,
      surf: "Function", px: "$x_0$", py: "$y_0$", map: "Level curves of $f(x, y)$", sliceX: "Slice $y = y_0$: a function of $x$", sliceY: "Slice $x = x_0$: a function of $y$",
      fx: "$\\partial f / \\partial x$", fy: "$\\partial f / \\partial y$", fval: "$f(x_0, y_0)$",
      partNote: (fx, fy) => `Freeze $y$ — what is left is a function of one variable $x$, and its slope at the point is $\\partial f / \\partial x = ${fx}$. Freeze $x$ — the slope in $y$ is $\\partial f / \\partial y = ${fy}$.`,
      dir: "Direction $\\mathbf{u}$, angle", grad: "$\\nabla f$", uvec: "$\\mathbf{u}$", field: "gradient field", gnorm: "$|\\nabla f|$", du: "$D_{\\mathbf{u}} f = \\nabla f\\cdot\\mathbf{u}$",
      gradNote: (g, n, d, ang) => `$\\nabla f = ${g}$, length $${n}$. Along $\\mathbf{u}$ the function changes at the rate $D_{\\mathbf{u}} f = |\\nabla f|\\cos\\varphi = ${d}$, where $\\varphi = ${ang}^{\\circ}$ is the angle between $\\mathbf{u}$ and $\\nabla f$. The maximum is when $\\mathbf{u}$ points along the gradient, zero along a level curve.`,
      flat: "Here $\\nabla f = \\mathbf{0}$: the function is “flat” in every direction — a candidate for a minimum, a maximum or a saddle.",
      eta: "Step $\\eta$", start: "Start", go: "Descend", reset: "Reset", step: "step", path: "descent path",
      descNote: (k, p, f, m) => `Step ${k}: $\\mathbf{p} = ${p}$, $f = ${f}$. For this bowl every step multiplies $x$ by $${m}$, and $y$ by its own factor (see the text).`,
      show: "Show all solutions", hide: "Hide all solutions",
      thK: "step", thP: "$\\mathbf{p}$", thG: "$\\nabla f(\\mathbf{p})$", thF: "$f(\\mathbf{p})$",
    },
    uz: {
      ptA: "A nuqta", ptB: "B nuqta", line: "to‘g‘ri chiziq", run: "o‘ngga $\\Delta x$", rise: "yuqoriga $\\Delta y$", slope: "qiyalik $\\Delta y / \\Delta x$",
      slopeNote: (a, b, dx, dy, k) => `$A = ${a}$ dan $B = ${b}$ ga: o‘ngga $\\Delta x = ${dx}$ yurdik, $\\Delta y = ${dy}$ ga ko‘tarildik. Qiyalik $= \\Delta y \\div \\Delta x = ${k}$ — o‘ngga har bir qadamda to‘g‘ri chiziq $${k}$ ga o‘zgaradi. Nuqtalarni suring: to‘g‘ri chiziqning qiyaligi istalgan ikki nuqtasi uchun bir xil.`,
      vertical: "Nuqtalar bitta vertikalda: $\\Delta x = 0$, nolga bo‘lib bo‘lmaydi — vertikal to‘g‘ri chiziqning qiyaligi yo‘q.",
      x0: "$x_0$ nuqta", dx: "$\\Delta x$ qadam", shrink: "Δx → 0", fn: "Funksiya",
      exact: "aniq $\\Delta f$", linp: "chiziqli qism $f'(x_0)\\,\\Delta x$", tailw: "dum", secSlope: "$\\Delta f / \\Delta x$", der: "$f'(x_0)$",
      secant: "kesuvchi", tangent: "urinma",
      tailNote: (dx, df, lin, tail, share) => `$\\Delta x = ${dx}$ da: $\\Delta f = ${df}$, shundan chiziqli qism $${lin}$ va dum $${tail}$ ($\\Delta f$ ning ${share} % i). Qadamni kichraytiring: dum $\\Delta x$ dan tezroq yo‘qoladi, kesuvchining qiyaligi esa $f'(x_0)$ ga intiladi.`,
      surf: "Funksiya", px: "$x_0$", py: "$y_0$", map: "$f(x, y)$ ning sath chiziqlari", sliceX: "$y = y_0$ kesim: $x$ ning funksiyasi", sliceY: "$x = x_0$ kesim: $y$ ning funksiyasi",
      fx: "$\\partial f / \\partial x$", fy: "$\\partial f / \\partial y$", fval: "$f(x_0, y_0)$",
      partNote: (fx, fy) => `$y$ ni muzlatdik — bitta $x$ o‘zgaruvchili funksiya qoldi, uning nuqtadagi qiyaligi $\\partial f / \\partial x = ${fx}$. $x$ ni muzlatdik — $y$ bo‘yicha qiyalik $\\partial f / \\partial y = ${fy}$.`,
      dir: "$\\mathbf{u}$ yo‘nalish, burchak", grad: "$\\nabla f$", uvec: "$\\mathbf{u}$", field: "gradiyentlar maydoni", gnorm: "$|\\nabla f|$", du: "$D_{\\mathbf{u}} f = \\nabla f\\cdot\\mathbf{u}$",
      gradNote: (g, n, d, ang) => `$\\nabla f = ${g}$, uzunligi $${n}$. $\\mathbf{u}$ bo‘ylab funksiya $D_{\\mathbf{u}} f = |\\nabla f|\\cos\\varphi = ${d}$ tezlik bilan o‘zgaradi, bu yerda $\\varphi = ${ang}^{\\circ}$ — $\\mathbf{u}$ va $\\nabla f$ orasidagi burchak. Eng kattasi — $\\mathbf{u}$ gradiyent bo‘ylab qaraganda, nol — sath chizig‘i bo‘ylab.`,
      flat: "Bu nuqtada $\\nabla f = \\mathbf{0}$: funksiya barcha yo‘nalishlarda «tekis» — minimum, maksimum yoki egar nuqtasiga nomzod.",
      eta: "$\\eta$ qadam", start: "Start", go: "Tushish", reset: "Qaytarish", step: "qadam", path: "tushish yo‘li",
      descNote: (k, p, f, m) => `${k}-qadam: $\\mathbf{p} = ${p}$, $f = ${f}$. Bu kosa uchun har bir qadam $x$ ni $${m}$ ga, $y$ ni esa o‘z ko‘paytuvchisiga ko‘paytiradi (matnga qarang).`,
      show: "Barcha yechimlarni ko‘rsatish", hide: "Barcha yechimlarni yashirish",
      thK: "qadam", thP: "$\\mathbf{p}$", thG: "$\\nabla f(\\mathbf{p})$", thF: "$f(\\mathbf{p})$",
    },
  }[FV.lang] || {};

  const n = (v, d = 3) => FV.num(Math.abs(v) < 1e-9 ? 0 : v, d);
  const tn = (v, d = 3) => n(v, d).replace("−", "-").replace(",", "{,}");
  const SEP = FV.lang === "en" ? ",\\ " : ";\\ ";
  const tv = (a, d = 3) => "(" + a.map((v) => tn(v, d)).join(SEP) + ")";
  const reduced = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function setNote(el, s) { el.textContent = ""; el.append(FV.rich(s, "span")); }
  function quiet(note, on) { note.setAttribute("aria-live", on ? "off" : "polite"); }
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
  const debounce = (fn) => { let r = 0; return () => { cancelAnimationFrame(r); r = requestAnimationFrame(fn); }; };

  // ---------- 1. the slope of a line ----------
  FV.widget("dr-slope", (el, cfg) => {
    const ui = FV.shell(el);
    const plot = new FV.Plot(ui.stage, { x: [-1, 4], y: [-1, 7], aspect: 0.62, maxHeight: 420, xLabel: "x", yLabel: "y", xTicks: [-1, 0, 1, 2, 3, 4], yTicks: [0, 1, 2, 3, 4, 5, 6, 7] });
    const A = cfg.A || [0, 1], B = cfg.B || [2, 4];
    const snap = (v) => Math.round(v * 2) / 2;
    const ro = FV.ui.readout(ui.readout, [{ key: "dx", label: L.run, c: "blue" }, { key: "dy", label: L.rise, c: "teal" }, { key: "k", label: L.slope, c: "orange" }]);
    const ha = plot.handle(A[0], A[1], { c: "red", label: L.ptA, onDrag: (x, y) => [snap(x), snap(y)], onChange: (x, y) => { A[0] = x; A[1] = y; draw(); } });
    const hb = plot.handle(B[0], B[1], { c: "red", label: L.ptB, onDrag: (x, y) => [snap(x), snap(y)], onChange: (x, y) => { B[0] = x; B[1] = y; draw(); } });
    function draw() {
      plot.clear();
      const dx = B[0] - A[0], dy = B[1] - A[1];
      if (Math.abs(dx) < 1e-9) {
        plot.vline(A[0], { c: "ink", w: 2.2, dash: null });
        ro.set("dx", "0"); ro.set("dy", n(dy)); ro.set("k", "—");
        setNote(ui.note, L.vertical);
        return;
      }
      const k = dy / dx;
      plot.line(-1, A[1] + k * (-1 - A[0]), 4, A[1] + k * (4 - A[0]), { c: "ink", w: 2.2 });
      plot.arrow(A[0], A[1], B[0], A[1], { c: "blue", w: 2.4 });
      plot.arrow(B[0], A[1], B[0], B[1], { c: "teal", w: 2.4 });
      plot.text((A[0] + B[0]) / 2, A[1], "Δx = " + n(dx), { anchor: "middle", dy: dy >= 0 ? 18 : -8, c: "blue", clip: true });
      plot.text(B[0], (A[1] + B[1]) / 2, "Δy = " + n(dy), { dx: dx > 0 ? 8 : -8, anchor: dx > 0 ? "start" : "end", c: "teal", clip: true });
      plot.text(A[0], A[1], "A", { dx: -10, dy: -10, anchor: "end", c: "red", clip: true });
      plot.text(B[0], B[1], "B", { dx: -10, dy: -10, anchor: "end", c: "red", clip: true });
      plot.legend([{ label: L.line + " $y = " + tn(k) + "x " + (A[1] - k * A[0] < 0 ? "- " : "+ ") + tn(Math.abs(A[1] - k * A[0])) + "$", c: "ink" }, { label: L.run, c: "blue" }, { label: L.rise, c: "teal" }]);
      ro.set("dx", n(dx)); ro.set("dy", n(dy)); ro.set("k", n(k));
      setNote(ui.note, L.slopeNote(tv(A, 2), tv(B, 2), tn(dx), tn(dy), tn(k)));
    }
    plot.onresize = () => { draw(); ha._place(); hb._place(); };
    draw();
  });

  // ---------- 2. the increment: linear part + tail ----------
  const TF = {
    sq: { tex: "f(x) = x^2", f: (x) => x * x, d: (x) => 2 * x, x: [-1.5, 3.2], y: [-1, 9], x0: 1 },
    cube: { tex: "f(x) = x^3", f: (x) => x * x * x, d: (x) => 3 * x * x, x: [-1.8, 2.2], y: [-5, 9], x0: 1 },
    sin: { tex: "f(x) = \\sin x", f: Math.sin, d: Math.cos, x: [-1, 4.2], y: [-1.5, 1.6], x0: 0.6 },
  };
  FV.widget("dr-tail", (el, cfg) => {
    const ui = FV.shell(el);
    let P = TF[cfg.preset] || TF.sq, x0 = P.x0, dx = cfg.dx || 1, timer = 0;
    const plot = new FV.Plot(ui.stage, { x: P.x, y: P.y, aspect: 0.56, maxHeight: 420, xLabel: "x", yLabel: "f(x)" });
    const seg = FV.ui.seg({ label: L.fn, value: cfg.preset || "sq", options: Object.keys(TF).map((k) => ({ value: k, label: "$" + TF[k].tex + "$" })), onchange: (k) => { stop(); P = TF[k]; x0 = P.x0; plot.setDomain(P.x, P.y); ranges(); draw(); } });
    const sx = FV.ui.slider({ label: L.x0, min: 0, max: 1, step: 0.01, value: x0, oninput: (v) => { x0 = v; ranges(); draw(); } });
    const sd = FV.ui.slider({ label: L.dx, min: 0.001, max: 1.5, step: 0.001, value: dx, fmt: (v) => n(v, 3), oninput: (v) => { stop(); dx = v; draw(); } });
    const go = toggleButton(L.shrink, () => (timer ? stop() : start()));
    ui.controls.append(seg.el, sx.el, sd.el, go.el);
    function ranges() {
      sx.input.min = P.x[0] + 0.2; sx.input.max = P.x[1] - 0.3; x0 = FV.clamp(x0, +sx.input.min, +sx.input.max); sx.set(x0);
      const m = Math.max(0.01, Math.min(1.5, P.x[1] - x0 - 0.02)); sd.input.max = m; dx = FV.clamp(dx, 0.001, m); sd.set(dx);
    }
    const ro = FV.ui.readout(ui.readout, [{ key: "df", label: L.exact }, { key: "lin", label: L.linp, c: "blue" }, { key: "t", label: L.tailw, c: "red" }, { key: "q", label: L.secSlope, c: "orange" }, { key: "d", label: L.der, c: "blue" }]);
    function start() {
      if (dx < 0.002) dx = Math.min(1, +sd.input.max);
      if (reduced()) { dx = 0.001; sd.set(dx); draw(); return; }
      go.set(true); quiet(ui.note, true);
      timer = setInterval(() => { dx *= 0.93; if (dx < 0.001) { dx = 0.001; stop(); } sd.set(dx); draw(); }, 60);
    }
    function stop() { clearInterval(timer); timer = 0; go.set(false); quiet(ui.note, false); }
    document.addEventListener("visibilitychange", () => { if (document.hidden && timer) stop(); });
    function draw() {
      const f = P.f, y0 = f(x0), y1 = f(x0 + dx), df = y1 - y0, d = P.d(x0), lin = d * dx, tail = df - lin, q = df / dx;
      plot.clear();
      plot.fn(f, { c: "ink", w: 2.2 });
      plot.line(P.x[0], y0 + d * (P.x[0] - x0), P.x[1], y0 + d * (P.x[1] - x0), { c: "blue", w: 1.6, dash: true });
      plot.line(P.x[0], y0 + q * (P.x[0] - x0), P.x[1], y0 + q * (P.x[1] - x0), { c: "orange", w: 1.6, opacity: 0.8 });
      plot.line(x0, y0, x0 + dx, y0, { c: "guide", w: 1.2, dash: "3 3" });
      plot.line(x0 + dx, y0, x0 + dx, y0 + lin, { c: "blue", w: 4 });
      plot.line(x0 + dx, y0 + lin, x0 + dx, y1, { c: "red", w: 4 });
      plot.dot(x0, y0, { c: "blue", r: 5 }); plot.dot(x0 + dx, y1, { c: "orange", r: 5 });
      plot.legend([{ label: "$" + P.tex + "$", c: "ink" }, { label: L.tangent, c: "blue", dash: true }, { label: L.secant, c: "orange" }, { label: L.linp, c: "blue", box: true }, { label: L.tailw, c: "red", box: true }]);
      ro.set("df", n(df, 4)); ro.set("lin", n(lin, 4)); ro.set("t", n(tail, 4)); ro.set("q", n(q, 4)); ro.set("d", n(d, 4));
      const share = Math.abs(df) > 1e-12 ? FV.num(Math.abs(tail / df) * 100, 2) : "0";
      setNote(ui.note, L.tailNote(tn(dx, 3), tn(df, 4), tn(lin, 4), tn(tail, 4), share));
    }
    plot.onresize = draw;
    ranges(); draw();
  });

  // ---------- 3. partial derivatives as slopes of slices ----------
  const PF = {
    bowl: { tex: "f = x^2 + y^2", f: (x, y) => x * x + y * y, fx: (x) => 2 * x, fy: (x, y) => 2 * y, R: 2, Z: [-0.5, 8.5], levels: [0.25, 0.5, 1, 2, 3, 4, 5, 6, 7], p: [1, 1.4] },
    cubic: { tex: "f = x^2 y + y^3", f: (x, y) => x * x * y + y * y * y, fx: (x, y) => 2 * x * y, fy: (x, y) => x * x + 3 * y * y, R: 1.6, Z: [-8.5, 8.5], levels: [-6, -4, -2, -1, -0.3, 0.3, 1, 2, 4, 6], p: [1, 0.5] },
    wave: { tex: "f = \\sin x\\cos y", f: (x, y) => Math.sin(x) * Math.cos(y), fx: (x, y) => Math.cos(x) * Math.cos(y), fy: (x, y) => -Math.sin(x) * Math.sin(y), R: 3.2, Z: [-1.2, 1.2], levels: [-0.8, -0.5, -0.2, 0.2, 0.5, 0.8], p: [0.8, 0.6] },
  };
  FV.widget("dr-partial", (el, cfg) => {
    const ui = FV.shell(el, { cols: true });
    let P = PF[cfg.preset] || PF.bowl, p = P.p.slice();
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const box = () => [-P.R, P.R];
    const map = new FV.Plot(c1, { x: box(), y: box(), equal: true, xLabel: "x", yLabel: "y", title: L.map });
    const sl1 = new FV.Plot(c2, { x: box(), y: P.Z, aspect: 0.5, maxHeight: 200, minHeight: 150, xLabel: "x", title: L.sliceX });
    const sl2 = new FV.Plot(c2, { x: box(), y: P.Z, aspect: 0.5, maxHeight: 200, minHeight: 150, xLabel: "y", title: L.sliceY });
    const seg = FV.ui.seg({ label: L.surf, value: cfg.preset || "bowl", options: Object.keys(PF).map((k) => ({ value: k, label: "$" + PF[k].tex + "$" })), onchange: (k) => { P = PF[k]; p = P.p.slice(); [map].forEach((q) => q.setDomain(box(), box())); sl1.setDomain(box(), P.Z); sl2.setDomain(box(), P.Z); ranges(); bg = null; draw(); } });
    const sx = FV.ui.slider({ label: L.px, min: -2, max: 2, step: 0.05, value: p[0], oninput: (v) => { p[0] = v; draw(); } });
    const sy = FV.ui.slider({ label: L.py, min: -2, max: 2, step: 0.05, value: p[1], oninput: (v) => { p[1] = v; draw(); } });
    function ranges() { [sx, sy].forEach((s, i) => { s.input.min = -P.R * 0.9; s.input.max = P.R * 0.9; s.set(p[i]); }); }
    ui.controls.append(seg.el, sx.el, sy.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "f", label: L.fval }, { key: "fx", label: L.fx, c: "blue" }, { key: "fy", label: L.fy, c: "teal" }]);
    let bg = null, dyn = null;
    const into = (plot, g, fn) => { const keep = plot.gMain; plot.gMain = g; try { fn(); } finally { plot.gMain = keep; } };
    function draw() {
      if (bg !== P) {
        map.clear(); map.heat(P.f, { cmap: "viridis", alpha: 0.32, res: 4 }); map.contours(P.f, P.levels, { c: "ink", w: 1, opacity: 0.35 });
        dyn = FV.svg("g", {}, map.gMain); bg = P;
      }
      const [x0, y0] = p, z0 = P.f(x0, y0), fx = P.fx(x0, y0), fy = P.fy(x0, y0);
      dyn.textContent = "";
      into(map, dyn, () => {
        map.line(-P.R, y0, P.R, y0, { c: "blue", w: 1.6, dash: true });
        map.line(x0, -P.R, x0, P.R, { c: "teal", w: 1.6, dash: true });
        map.dot(x0, y0, { c: "orange", r: 6 });
      });
      sl1.clear(); sl1.fn((x) => P.f(x, y0), { c: "blue", w: 2.2 });
      sl1.line(-P.R, z0 + fx * (-P.R - x0), P.R, z0 + fx * (P.R - x0), { c: "orange", w: 1.6, dash: true }); sl1.dot(x0, z0, { c: "orange", r: 5 });
      sl2.clear(); sl2.fn((y) => P.f(x0, y), { c: "teal", w: 2.2 });
      sl2.line(-P.R, z0 + fy * (-P.R - y0), P.R, z0 + fy * (P.R - y0), { c: "orange", w: 1.6, dash: true }); sl2.dot(y0, z0, { c: "orange", r: 5 });
      ro.set("f", n(z0)); ro.set("fx", n(fx)); ro.set("fy", n(fy));
      setNote(ui.note, L.partNote(tn(fx), tn(fy)));
    }
    const redraw = debounce(() => { bg = null; draw(); });
    map.onresize = sl1.onresize = sl2.onresize = redraw;
    ranges(); draw();
  });

  // ---------- 4. the gradient field and the directional derivative ----------
  const GF = {
    bowl: { tex: "f = x^2 + y^2", f: (x, y) => x * x + y * y, g: (x, y) => [2 * x, 2 * y], levels: [0.25, 0.5, 1, 2, 3, 4], p: [-1, 0.5] },
    saddle: { tex: "f = x^2 - y^2", f: (x, y) => x * x - y * y, g: (x, y) => [2 * x, -2 * y], levels: [-3, -2, -1, -0.4, 0.4, 1, 2, 3], p: [1, 0.5] },
    mix: { tex: "f = x^2 y + \\sin y", f: (x, y) => x * x * y + Math.sin(y), g: (x, y) => [2 * x * y, x * x + Math.cos(y)], levels: [-3, -2, -1, -0.4, 0.4, 1, 2, 3], p: [1, 0] },
  };
  FV.widget("dr-grad", (el, cfg) => {
    const ui = FV.shell(el);
    let P = GF[cfg.preset] || GF.bowl, ang = cfg.angle != null ? cfg.angle : 30;
    const R = 2;
    const plot = new FV.Plot(ui.stage, { x: [-R, R], y: [-R, R], equal: true, maxHeight: 520, xLabel: "x", yLabel: "y" });
    const seg = FV.ui.seg({ label: L.surf, value: cfg.preset || "bowl", options: Object.keys(GF).map((k) => ({ value: k, label: "$" + GF[k].tex + "$" })), onchange: (k) => { P = GF[k]; h.set(P.p[0], P.p[1]); bg = null; draw(); } });
    const sa = FV.ui.slider({ label: L.dir, min: 0, max: 360, step: 1, value: ang, fmt: (v) => Math.round(v) + "°", oninput: (v) => { ang = v; draw(); } });
    ui.controls.append(seg.el, sa.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "g", label: L.grad, c: "red" }, { key: "n", label: L.gnorm }, { key: "d", label: L.du, c: "blue" }]);
    const h = plot.handle(P.p[0], P.p[1], { c: "orange", label: "(x, y)", onChange: () => draw() });
    let bg = null, dyn = null;
    function background() {
      plot.clear();
      plot.heat(P.f, { cmap: "viridis", alpha: 0.28, res: 4 });
      plot.contours(P.f, P.levels, { c: "ink", w: 1, opacity: 0.35 });
      const gs = FV.linspace(-R * 0.85, R * 0.85, 9);
      let mx = 0; gs.forEach((x) => gs.forEach((y) => { const g = P.g(x, y); mx = Math.max(mx, Math.hypot(g[0], g[1])); }));
      gs.forEach((x) => gs.forEach((y) => { const g = P.g(x, y), s = 0.36 / (mx || 1); plot.arrow(x, y, x + g[0] * s, y + g[1] * s, { c: "faint", w: 1.2, head: 5 }); }));
      plot.legend([{ label: L.grad, c: "red" }, { label: L.uvec, c: "blue" }, { label: L.field, c: "faint" }]);
      dyn = FV.svg("g", {}, plot.gMain); bg = P;
    }
    function draw() {
      if (bg !== P) background();
      const x = h.x, y = h.y, g = P.g(x, y), gn = Math.hypot(g[0], g[1]);
      const a = (ang * Math.PI) / 180, u = [Math.cos(a), Math.sin(a)], d = g[0] * u[0] + g[1] * u[1];
      dyn.textContent = "";
      const keep = plot.gMain; plot.gMain = dyn;
      try {
        if (gn > 1e-9) { const s = Math.min(0.9, 0.3 * gn) / gn; plot.arrow(x, y, x + g[0] * s, y + g[1] * s, { c: "red", w: 2.6 }); }
        plot.arrow(x, y, x + 0.7 * u[0], y + 0.7 * u[1], { c: "blue", w: 2.6 });
        plot.dot(x, y, { c: "orange", r: 4 });
      } finally { plot.gMain = keep; }
      ro.set("g", tvPlain(g)); ro.set("n", n(gn)); ro.set("d", n(d));
      if (gn < 1e-9) { setNote(ui.note, L.flat); return; }
      const phi = Math.acos(FV.clamp(d / gn, -1, 1)) * 180 / Math.PI;
      setNote(ui.note, L.gradNote(tv(g), tn(gn), tn(d), FV.num(phi, 3)));
    }
    const tvPlain = (g) => "(" + g.map((v) => n(v)).join(FV.lang === "en" ? ", " : "; ") + ")";
    plot.onresize = debounce(() => { bg = null; draw(); h._place(); });
    draw();
  });

  // ---------- 5. gradient descent on a bowl ----------
  FV.widget("dr-descent", (el, cfg) => {
    const ui = FV.shell(el);
    const a = cfg.a || 1, b = cfg.b || 1; // f = a x² + b y²
    const f = (x, y) => a * x * x + b * y * y, g = (x, y) => [2 * a * x, 2 * b * y];
    let eta = cfg.eta || 0.1, p0 = (cfg.p || [3, 4]).slice(), path = [p0.slice()], timer = 0;
    const R = 5;
    const plot = new FV.Plot(ui.stage, { x: [-R, R], y: [-R, R], equal: true, maxHeight: 460, xLabel: "x", yLabel: "y" });
    const se = FV.ui.slider({ label: L.eta, min: 0.02, max: 1.1, step: 0.01, value: eta, oninput: (v) => { eta = v; reset(); } });
    const go = toggleButton(L.go, () => (timer ? stop() : start()));
    const stepB = FV.ui.button({ label: FV.t("step") + " →", onclick: () => { stop(); step(); } });
    const rs = FV.ui.button({ label: "↺ " + L.reset, onclick: () => { stop(); reset(); } });
    ui.controls.append(se.el, go.el, stepB.el, rs.el);
    const tbl = FV.h("div", { class: "table-wrap dr-desc-wrap", tabindex: "0" });
    ui.readout.append(tbl);
    const h = plot.handle(p0[0], p0[1], { c: "orange", label: L.start, onChange: (x, y) => { p0 = [Math.round(x * 10) / 10, Math.round(y * 10) / 10]; stop(); reset(); } });
    let bg = false, dyn = null;
    function background() {
      plot.clear();
      plot.heat(f, { cmap: "viridis", alpha: 0.28, res: 4 });
      plot.contours(f, [1, 2, 4, 8, 12, 16, 25, 36].map((v) => v * Math.min(a, b)), { c: "ink", w: 1, opacity: 0.35 });
      plot.legend([{ label: L.path, c: "red" }]);
      dyn = FV.svg("g", {}, plot.gMain); bg = true;
    }
    function reset() { path = [p0.slice()]; draw(); }
    function step() {
      const p = path[path.length - 1], gr = g(p[0], p[1]), q = [p[0] - eta * gr[0], p[1] - eta * gr[1]];
      if (!q.every(Number.isFinite) || Math.hypot(q[0], q[1]) > 1e6 || path.length > 60) return false;
      path.push(q); draw(); return true;
    }
    function start() {
      if (reduced()) { for (let i = 0; i < 10; i++) if (!step()) break; return; }
      go.set(true); quiet(ui.note, true);
      let k = 0;
      timer = setInterval(() => { if (!step() || ++k >= 30) stop(); }, 350);
    }
    function stop() { clearInterval(timer); timer = 0; go.set(false); quiet(ui.note, false); }
    document.addEventListener("visibilitychange", () => { if (document.hidden && timer) stop(); });
    function draw() {
      if (!bg) background();
      dyn.textContent = "";
      const keep = plot.gMain; plot.gMain = dyn;
      try {
        const vis = path.map((q) => [FV.clamp(q[0], -R * 1.5, R * 1.5), FV.clamp(q[1], -R * 1.5, R * 1.5)]);
        plot.path(vis, { c: "red", w: 2 });
        vis.forEach((q, i) => plot.dot(q[0], q[1], { c: i ? "red" : "orange", r: i ? 3.5 : 5 }));
      } finally { plot.gMain = keep; }
      const rows = path.slice(-8).map((q, i, arr) => { const k = path.length - arr.length + i, gr = g(q[0], q[1]); return `<tr><td class=num>${k}</td><td class=num>${fmtV(q)}</td><td class=num>${fmtV(gr)}</td><td class=num>${n(f(q[0], q[1]), 4)}</td></tr>`; }).join("");
      tbl.innerHTML = `<table class="data"><thead><tr><th class=num>${L.thK}</th><th class=num></th><th class=num></th><th class=num></th></tr></thead><tbody>${rows}</tbody></table>`;
      const ths = tbl.querySelectorAll("th");
      [L.thP, L.thG, L.thF].forEach((s, i) => { ths[i + 1].append(FV.rich(s)); ths[i + 1].setAttribute("aria-label", FV.plain(s)); });
      const last = path[path.length - 1];
      setNote(ui.note, L.descNote(path.length - 1, tv(last), tn(f(last[0], last[1]), 4), tn(1 - 2 * a * eta, 3)));
    }
    const fmtV = (v) => "(" + v.map((x) => n(x, 3)).join(FV.lang === "en" ? ", " : "; ") + ")";
    plot.onresize = debounce(() => { bg = false; draw(); h._place(); });
    reset();
  });
  // ---------- 6. the practice: open or close every solution at once ----------
  FV.widget("dr-solutions", (el) => {
    el.classList.add("cr-sol-bar");
    const all = () => Array.from(document.querySelectorAll("details.cr-sol"));
    const b = FV.ui.button({ label: L.show, onclick: () => { const open = all().some((d) => !d.open); all().forEach((d) => { d.open = open; }); sync(); } });
    function sync() {
      const open = all().every((d) => d.open);
      b.setLabel(open ? L.hide : L.show);
      b.el.setAttribute("aria-expanded", open ? "true" : "false");
    }
    document.addEventListener("toggle", (e) => { if (e.target.matches && e.target.matches("details.cr-sol")) sync(); }, true);
    el.textContent = ""; el.append(b.el);
    sync();
  });
})();
