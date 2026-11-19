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
      tailNote: (dx, df, lin, tail, share) => `При $\\Delta x = ${dx}$: $\\Delta f = ${df}$, из них линейная часть $${lin}$ и хвост $${tail}$${share != null ? ` (${share} % от $\\Delta f$)` : ""}. Уменьшайте шаг: хвост исчезает быстрее, чем $\\Delta x$, и наклон секущей стремится к $f'(x_0)$.`,
      surf: "Функция", px: "$x_0$", py: "$y_0$", map: "Линии уровня $f(x, y)$", sliceX: "Срез $y = y_0$: функция от $x$", sliceY: "Срез $x = x_0$: функция от $y$",
      fx: "$\\partial f / \\partial x$", fy: "$\\partial f / \\partial y$", fval: "$f(x_0, y_0)$",
      partNote: (fx, fy) => `Заморозили $y$ — осталась функция одной переменной $x$, её наклон в точке $\\partial f / \\partial x = ${fx}$. Заморозили $x$ — наклон по $y$ равен $\\partial f / \\partial y = ${fy}$.`,
      dir: "Направление $\\mathbf{u}$, угол", grad: "$\\nabla f$", uvec: "$\\mathbf{u}$", field: "поле градиентов", gnorm: "$|\\nabla f|$", du: "$D_{\\mathbf{u}} f = \\nabla f\\cdot\\mathbf{u}$",
      gradNote: (g, n, d, ang) => `$\\nabla f = ${g}$, длина $${n}$. Вдоль $\\mathbf{u}$ функция меняется со скоростью $D_{\\mathbf{u}} f = |\\nabla f|\\cos\\varphi = ${d}$, где $\\varphi = ${ang}^{\\circ}$ — угол между $\\mathbf{u}$ и $\\nabla f$. Максимум — когда $\\mathbf{u}$ смотрит вдоль градиента, ноль — вдоль линии уровня.`,
      flat: "В этой точке $\\nabla f = \\mathbf{0}$: функция «плоская» во всех направлениях — это кандидат в минимум, максимум или седло.",
      eta: "Шаг $\\eta$", start: "Старт", go: "Спуск", reset: "Сброс", step: "шаг", path: "путь спуска",
      descNote: (k, p, f, m) => `Шаг ${k}: $\\mathbf{p} = ${p}$, $f = ${f}$. Для этой чаши каждый шаг умножает обе координаты на $1 - 2\\eta = ${m}$.`,
      show: "Показать все решения", hide: "Скрыть все решения",
      same: "Точки совпали: через одну точку проходит бесконечно много прямых, наклон не определён — разведите точки.", ptP: "точка (x, y)", tbl: "Последние шаги спуска", converged: "Точка больше не сдвигается — достигнут минимум.", diverged: "Значения стали огромными — спуск разошёлся.", maxed: "Показаны первые 60 шагов; нажмите «Сброс».",
      thK: "шаг", thP: "$\\mathbf{p}$", thG: "$\\nabla f(\\mathbf{p})$", thF: "$f(\\mathbf{p})$",
    },
    en: {
      ptA: "point A", ptB: "point B", line: "line", run: "run $\\Delta x$", rise: "rise $\\Delta y$", slope: "slope $\\Delta y / \\Delta x$",
      slopeNote: (a, b, dx, dy, k) => `From $A = ${a}$ to $B = ${b}$: we moved right by $\\Delta x = ${dx}$ and rose by $\\Delta y = ${dy}$. Slope $= \\Delta y \\div \\Delta x = ${k}$ — for every step to the right the line changes by $${k}$. Drag the points: a line has the same slope for any pair of its points.`,
      vertical: "The points are on one vertical: $\\Delta x = 0$, and we cannot divide by zero — a vertical line has no slope.",
      x0: "Point $x_0$", dx: "Step $\\Delta x$", shrink: "Δx → 0", fn: "Function",
      exact: "exact $\\Delta f$", linp: "linear part $f'(x_0)\\,\\Delta x$", tailw: "tail", secSlope: "$\\Delta f / \\Delta x$", der: "$f'(x_0)$",
      secant: "secant", tangent: "tangent",
      tailNote: (dx, df, lin, tail, share) => `At $\\Delta x = ${dx}$: $\\Delta f = ${df}$, of which the linear part is $${lin}$ and the tail is $${tail}$${share != null ? ` (${share} % of $\\Delta f$)` : ""}. Make the step smaller: the tail vanishes faster than $\\Delta x$, and the slope of the secant tends to $f'(x_0)$.`,
      surf: "Function", px: "$x_0$", py: "$y_0$", map: "Level curves of $f(x, y)$", sliceX: "Slice $y = y_0$: a function of $x$", sliceY: "Slice $x = x_0$: a function of $y$",
      fx: "$\\partial f / \\partial x$", fy: "$\\partial f / \\partial y$", fval: "$f(x_0, y_0)$",
      partNote: (fx, fy) => `Freeze $y$ — what is left is a function of one variable $x$, and its slope at the point is $\\partial f / \\partial x = ${fx}$. Freeze $x$ — the slope in $y$ is $\\partial f / \\partial y = ${fy}$.`,
      dir: "Direction $\\mathbf{u}$, angle", grad: "$\\nabla f$", uvec: "$\\mathbf{u}$", field: "gradient field", gnorm: "$|\\nabla f|$", du: "$D_{\\mathbf{u}} f = \\nabla f\\cdot\\mathbf{u}$",
      gradNote: (g, n, d, ang) => `$\\nabla f = ${g}$, length $${n}$. Along $\\mathbf{u}$ the function changes at the rate $D_{\\mathbf{u}} f = |\\nabla f|\\cos\\varphi = ${d}$, where $\\varphi = ${ang}^{\\circ}$ is the angle between $\\mathbf{u}$ and $\\nabla f$. The maximum is when $\\mathbf{u}$ points along the gradient, zero along a level curve.`,
      flat: "Here $\\nabla f = \\mathbf{0}$: the function is “flat” in every direction — a candidate for a minimum, a maximum or a saddle.",
      eta: "Step $\\eta$", start: "Start", go: "Descend", reset: "Reset", step: "step", path: "descent path",
      descNote: (k, p, f, m) => `Step ${k}: $\\mathbf{p} = ${p}$, $f = ${f}$. For this bowl every step multiplies both coordinates by $1 - 2\\eta = ${m}$.`,
      show: "Show all solutions", hide: "Hide all solutions",
      same: "The points coincide: infinitely many lines pass through one point, the slope is undefined — move the points apart.", ptP: "point (x, y)", tbl: "The last steps of the descent", converged: "The point no longer moves — the minimum is reached.", diverged: "The values have become huge — the descent has diverged.", maxed: "The first 60 steps are shown; press “Reset”.",
      thK: "step", thP: "$\\mathbf{p}$", thG: "$\\nabla f(\\mathbf{p})$", thF: "$f(\\mathbf{p})$",
    },
    uz: {
      ptA: "A nuqta", ptB: "B nuqta", line: "to‘g‘ri chiziq", run: "o‘ngga $\\Delta x$", rise: "yuqoriga $\\Delta y$", slope: "qiyalik $\\Delta y / \\Delta x$",
      slopeNote: (a, b, dx, dy, k) => `$A = ${a}$ dan $B = ${b}$ ga: o‘ngga $\\Delta x = ${dx}$ yurdik, $\\Delta y = ${dy}$ ga ko‘tarildik. Qiyalik $= \\Delta y \\div \\Delta x = ${k}$ — o‘ngga har bir qadamda to‘g‘ri chiziq $${k}$ ga o‘zgaradi. Nuqtalarni suring: to‘g‘ri chiziqning qiyaligi istalgan ikki nuqtasi uchun bir xil.`,
      vertical: "Nuqtalar bitta vertikalda: $\\Delta x = 0$, nolga bo‘lib bo‘lmaydi — vertikal to‘g‘ri chiziqning qiyaligi yo‘q.",
      x0: "$x_0$ nuqta", dx: "$\\Delta x$ qadam", shrink: "Δx → 0", fn: "Funksiya",
      exact: "aniq $\\Delta f$", linp: "chiziqli qism $f'(x_0)\\,\\Delta x$", tailw: "dum", secSlope: "$\\Delta f / \\Delta x$", der: "$f'(x_0)$",
      secant: "kesuvchi", tangent: "urinma",
      tailNote: (dx, df, lin, tail, share) => `$\\Delta x = ${dx}$ da: $\\Delta f = ${df}$, shundan chiziqli qism $${lin}$ va dum $${tail}$${share != null ? ` ($\\Delta f$ ning ${share} % i)` : ""}. Qadamni kichraytiring: dum $\\Delta x$ dan tezroq yo‘qoladi, kesuvchining qiyaligi esa $f'(x_0)$ ga intiladi.`,
      surf: "Funksiya", px: "$x_0$", py: "$y_0$", map: "$f(x, y)$ ning sath chiziqlari", sliceX: "$y = y_0$ kesim: $x$ ning funksiyasi", sliceY: "$x = x_0$ kesim: $y$ ning funksiyasi",
      fx: "$\\partial f / \\partial x$", fy: "$\\partial f / \\partial y$", fval: "$f(x_0, y_0)$",
      partNote: (fx, fy) => `$y$ ni muzlatdik — bitta $x$ o‘zgaruvchili funksiya qoldi, uning nuqtadagi qiyaligi $\\partial f / \\partial x = ${fx}$. $x$ ni muzlatdik — $y$ bo‘yicha qiyalik $\\partial f / \\partial y = ${fy}$.`,
      dir: "$\\mathbf{u}$ yo‘nalish, burchak", grad: "$\\nabla f$", uvec: "$\\mathbf{u}$", field: "gradiyentlar maydoni", gnorm: "$|\\nabla f|$", du: "$D_{\\mathbf{u}} f = \\nabla f\\cdot\\mathbf{u}$",
      gradNote: (g, n, d, ang) => `$\\nabla f = ${g}$, uzunligi $${n}$. $\\mathbf{u}$ bo‘ylab funksiya $D_{\\mathbf{u}} f = |\\nabla f|\\cos\\varphi = ${d}$ tezlik bilan o‘zgaradi, bu yerda $\\varphi = ${ang}^{\\circ}$ — $\\mathbf{u}$ va $\\nabla f$ orasidagi burchak. Eng kattasi — $\\mathbf{u}$ gradiyent bo‘ylab qaraganda, nol — sath chizig‘i bo‘ylab.`,
      flat: "Bu nuqtada $\\nabla f = \\mathbf{0}$: funksiya barcha yo‘nalishlarda «tekis» — minimum, maksimum yoki egar nuqtasiga nomzod.",
      eta: "$\\eta$ qadam", start: "Start", go: "Tushish", reset: "Qaytarish", step: "qadam", path: "tushish yo‘li",
      descNote: (k, p, f, m) => `${k}-qadam: $\\mathbf{p} = ${p}$, $f = ${f}$. Bu kosa uchun har bir qadam ikkala koordinatani $1 - 2\\eta = ${m}$ ga ko‘paytiradi.`,
      show: "Barcha yechimlarni ko‘rsatish", hide: "Barcha yechimlarni yashirish",
      same: "Nuqtalar ustma-ust tushdi: bitta nuqtadan cheksiz ko‘p to‘g‘ri chiziq o‘tadi, qiyalik aniqlanmagan — nuqtalarni ajrating.", ptP: "(x, y) nuqta", tbl: "Tushishning oxirgi qadamlari", converged: "Nuqta endi siljimaydi — minimumga yetildi.", diverged: "Qiymatlar juda katta bo‘ldi — tushish uzoqlashdi.", maxed: "Dastlabki 60 ta qadam ko‘rsatildi; «Qaytarish»ni bosing.",
      thK: "qadam", thP: "$\\mathbf{p}$", thG: "$\\nabla f(\\mathbf{p})$", thF: "$f(\\mathbf{p})$",
    },
  }[FV.lang] || {};

  const n = (v, d = 3) => FV.num(Math.abs(v) < 1e-9 ? 0 : v, d);
  const tn = (v, d = 3) => n(v, d).replace("−", "-").replace(",", "{,}");
  const SEP = FV.lang === "en" ? ",\\ " : ";\\ ";
  const PSEP = FV.lang === "en" ? ", " : "; ";
  const tv = (a, d = 3) => "(" + a.map((v) => tn(v, d)).join(SEP) + ")";
  const pv = (a, d = 3) => "(" + a.map((v) => n(v, d)).join(PSEP) + ")";
  const reduced = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // The note under a figure is redrawn on every input; screen readers get one calm announcement
  // through a hidden live region, 600 ms after the last change.
  function noter(ui) {
    ui.note.setAttribute("aria-live", "off");
    const live = FV.h("div", { class: "sr-only", "aria-live": "polite" });
    ui.root.append(live);
    let t = 0, last = "", armed = false;
    // announcements start only after the user does something inside the figure (not on load or resize)
    ["pointerdown", "keydown", "input"].forEach((e) => ui.root.addEventListener(e, () => { armed = true; }, { capture: true }));
    return (s) => {
      if (s === last) return;
      ui.note.textContent = ""; ui.note.append(FV.rich(s, "span"));
      last = s; clearTimeout(t);
      if (armed) t = setTimeout(() => { live.textContent = FV.plain(last); }, 600);
    };
  }
  // Play/pause: the label says what a press will do; the glyph is decoration.
  function toggleButton(label, onclick) {
    const b = FV.ui.button({ label: "", primary: true, onclick });
    const set = (on) => {
      b.el.textContent = "";
      b.el.append(FV.h("span", { "aria-hidden": "true", text: on ? "❚❚ " : "▶ " }), FV.rich(on ? FV.t("pause") : label));
    };
    set(false);
    return { el: b.el, set };
  }
  const debounce = (fn) => { let r = 0; return () => { cancelAnimationFrame(r); r = requestAnimationFrame(fn); }; };

  // ---------- 1. the slope of a line ----------
  FV.widget("dr-slope", (el, cfg) => {
    const ui = FV.shell(el), note = noter(ui);
    const plot = new FV.Plot(ui.stage, { x: [-1, 4], y: [-1, 7], aspect: 0.62, maxHeight: 420, xLabel: "x", yLabel: "y", xTicks: [-1, 0, 1, 2, 3, 4], yTicks: [0, 1, 2, 3, 4, 5, 6, 7] });
    const A = (cfg.A || [0, 1]).slice(), B = (cfg.B || [2, 4]).slice();
    const snap = (x, y) => [Math.round(x * 2) / 2, Math.round(y * 2) / 2];
    const ro = FV.ui.readout(ui.readout, [{ key: "dx", label: L.run, c: "blue" }, { key: "dy", label: L.rise, c: "teal" }, { key: "k", label: L.slope, c: "orange" }]);
    const ha = plot.handle(A[0], A[1], { c: "red", label: L.ptA, step: [0.5, 0.5], onDrag: snap, onChange: (x, y) => { A[0] = x; A[1] = y; draw(); } });
    const hb = plot.handle(B[0], B[1], { c: "red", label: L.ptB, step: [0.5, 0.5], onDrag: snap, onChange: (x, y) => { B[0] = x; B[1] = y; draw(); } });
    // a label next to a point, flipped to stay inside the frame
    function letter(P, s) {
      const X = plot.X(P[0]), Y = plot.Y(P[1]), left = X - 16 > plot.x0 + 4, up = Y - 14 > plot.y1 + 10;
      plot.text(P[0], P[1], s, { dx: left ? -16 : 14, dy: up ? -14 : 22, anchor: left ? "end" : "start", c: "red" });
    }
    const num = (v) => n(v).replace("−", "-");
    function eqn(k, b) {
      const kx = Math.abs(k) < 1e-12 ? "" : (k === 1 ? "x" : k === -1 ? "-x" : num(k) + "x");
      const bb = Math.abs(b) < 1e-12 ? "" : (kx ? (b < 0 ? " - " : " + ") + num(Math.abs(b)) : num(b));
      return "y = " + (kx + bb || "0");
    }
    function draw() {
      plot.clear();
      const dx = B[0] - A[0], dy = B[1] - A[1];
      if (Math.abs(dx) < 1e-9) {
        if (Math.abs(dy) > 1e-9) plot.vline(A[0], { c: "ink", w: 2.2, dash: null });
        letter(A, "A"); letter(B, "B");
        plot.legend([{ label: L.line, c: "ink" }]);
        ro.set("dx", "0"); ro.set("dy", n(dy)); ro.set("k", "—");
        note(Math.abs(dy) > 1e-9 ? L.vertical : L.same);
        return;
      }
      const k = dy / dx, b = A[1] - k * A[0];
      plot.line(-1, b - k, 4, b + 4 * k, { c: "ink", w: 2.2 });
      plot.arrow(A[0], A[1], B[0], A[1], { c: "blue", w: 2.4 });
      plot.arrow(B[0], A[1], B[0], B[1], { c: "teal", w: 2.4 });
      const below = plot.Y(A[1]) + 22 < plot.y0 && dy >= 0;
      plot.text((A[0] + B[0]) / 2, A[1], "Δx = " + n(dx), { anchor: "middle", dy: below ? 18 : -8, c: "blue" });
      const right = plot.X(B[0]) + 76 < plot.x1 ? (dx > 0 || plot.X(B[0]) - 76 < plot.x0) : false;
      plot.text(B[0], (A[1] + B[1]) / 2, "Δy = " + n(dy), { dx: right ? 8 : -8, anchor: right ? "start" : "end", c: "teal" });
      letter(A, "A"); letter(B, "B");
      plot.legend([{ label: L.line + " $" + eqn(k, b).replace(/\./g, FV.lang === "en" ? "." : "{,}") + "$", c: "ink" }, { label: L.run, c: "blue" }, { label: L.rise, c: "teal" }]);
      ro.set("dx", n(dx)); ro.set("dy", n(dy)); ro.set("k", n(k));
      note(L.slopeNote(tv(A, 2), tv(B, 2), tn(dx), tn(dy), tn(k)));
    }
    plot.onresize = () => { draw(); ha._place(); hb._place(); };
    draw();
  });

  // ---------- 2. the increment: linear part + tail ----------
  const TF = {
    sq: { tex: "f(x) = x^2", f: (x) => x * x, d: (x) => 2 * x, x: [-1.5, 3.2], y: [-1, 10.6], x0: 1 },
    cube: { tex: "f(x) = x^3", f: (x) => x * x * x, d: (x) => 3 * x * x, x: [-1.8, 2.2], y: [-5, 11], x0: 1 },
    sin: { tex: "f(x) = \\sin x", f: Math.sin, d: Math.cos, x: [-1, 4.2], y: [-1.5, 1.6], x0: 0.6 },
  };
  FV.widget("dr-tail", (el, cfg) => {
    const ui = FV.shell(el), note = noter(ui);
    let P = TF[cfg.preset] || TF.sq, x0 = P.x0, dx = cfg.dx || 1, timer = 0;
    const plot = new FV.Plot(ui.stage, { x: P.x, y: P.y, aspect: 0.56, maxHeight: 420, xLabel: "x", yLabel: "f(x)" });
    const seg = FV.ui.seg({ label: L.fn, value: cfg.preset || "sq", options: Object.keys(TF).map((k) => ({ value: k, label: "$" + TF[k].tex + "$" })), onchange: (k) => { stop(); P = TF[k]; x0 = P.x0; plot.setDomain(P.x, P.y); ranges(); draw(); } });
    const sx = FV.ui.slider({ label: L.x0, min: 0, max: 1, step: 0.01, value: x0, oninput: (v) => { x0 = v; ranges(); draw(); } });
    // Δx on a logarithmic track: from 0.001 to 1.5 every decade gets the same room
    const sd = FV.ui.slider({ label: L.dx, min: -3, max: Math.log10(1.5), step: 0.01, value: Math.log10(dx), map: (v) => Math.pow(10, v), unmap: Math.log10, fmt: (v) => n(v, 3), oninput: (v) => { stop(); dx = v; draw(); } });
    const go = toggleButton(L.shrink, () => (timer ? stop() : start()));
    ui.controls.append(seg.el, sx.el, sd.el, go.el);
    function ranges() {
      sx.input.min = P.x[0] + 0.2; sx.input.max = P.x[1] - 0.3; x0 = FV.clamp(x0, +sx.input.min, +sx.input.max); sx.set(x0);
      const m = Math.max(0.01, Math.min(1.5, P.x[1] - x0 - 0.02)); sd.input.max = Math.log10(m); dx = FV.clamp(dx, 0.001, m); sd.set(dx);
    }
    const ro = FV.ui.readout(ui.readout, [{ key: "df", label: L.exact }, { key: "lin", label: L.linp, c: "blue" }, { key: "t", label: L.tailw, c: "red" }, { key: "q", label: L.secSlope, c: "orange" }, { key: "d", label: L.der, c: "blue" }]);
    function start() {
      if (dx < 0.002) dx = Math.min(1, Math.pow(10, +sd.input.max));
      if (reduced()) { dx = 0.001; sd.set(dx); draw(); return; }
      go.set(true);
      timer = setInterval(() => { dx *= 0.93; if (dx < 0.001) { dx = 0.001; sd.set(dx); draw(); stop(); return; } sd.set(dx); draw(); }, 60);
    }
    function stop() { clearInterval(timer); timer = 0; go.set(false); }
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
      const share = Math.abs(df) > 1e-6 * Math.abs(tail) && Math.abs(df) > 1e-15 ? FV.num(Math.abs(tail / df) * 100, 2) : null;
      note(L.tailNote(tn(dx, 3), tn(df, 4), tn(lin, 4), tn(tail, 4), share));
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
    const ui = FV.shell(el, { cols: true }), note = noter(ui);
    let P = PF[cfg.preset] || PF.bowl, p = P.p.slice();
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const box = () => [-P.R, P.R];
    const lim = () => Math.floor((P.R * 0.9) / 0.05) * 0.05;
    const map = new FV.Plot(c1, { x: box(), y: box(), equal: true, xLabel: "x", yLabel: "y", title: L.map });
    const sl1 = new FV.Plot(c2, { x: box(), y: P.Z, aspect: 0.5, maxHeight: 200, minHeight: 150, xLabel: "x", title: L.sliceX });
    const sl2 = new FV.Plot(c2, { x: box(), y: P.Z, aspect: 0.5, maxHeight: 200, minHeight: 150, xLabel: "y", title: L.sliceY });
    const seg = FV.ui.seg({ label: L.surf, value: cfg.preset || "bowl", options: Object.keys(PF).map((k) => ({ value: k, label: "$" + PF[k].tex + "$" })), onchange: (k) => { P = PF[k]; p = P.p.slice(); map.setDomain(box(), box()); sl1.setDomain(box(), P.Z); sl2.setDomain(box(), P.Z); ranges(); bg = null; draw(); } });
    const sx = FV.ui.slider({ label: L.px, min: -2, max: 2, step: 0.05, value: p[0], oninput: (v) => { p[0] = v; h.set(p[0], p[1]); draw(); } });
    const sy = FV.ui.slider({ label: L.py, min: -2, max: 2, step: 0.05, value: p[1], oninput: (v) => { p[1] = v; h.set(p[0], p[1]); draw(); } });
    // the point can be dragged on the map too; it snaps to the slider grid
    const snap = (v) => FV.clamp(Math.round(v / 0.05) * 0.05, -lim(), lim());
    const h = map.handle(p[0], p[1], { c: "orange", label: L.ptP, step: [0.05, 0.05], onDrag: (x, y) => [snap(x), snap(y)], onChange: (x, y) => { p = [x, y]; sx.set(x); sy.set(y); draw(); } });
    function ranges() { [sx, sy].forEach((s, i) => { s.input.min = -lim(); s.input.max = lim(); s.set(p[i]); p[i] = s.value; }); h.set(p[0], p[1]); }
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
      });
      sl1.clear(); sl1.fn((x) => P.f(x, y0), { c: "blue", w: 2.2 });
      sl1.line(-P.R, z0 + fx * (-P.R - x0), P.R, z0 + fx * (P.R - x0), { c: "orange", w: 1.6, dash: true }); sl1.dot(x0, z0, { c: "orange", r: 5 });
      sl2.clear(); sl2.fn((y) => P.f(x0, y), { c: "teal", w: 2.2 });
      sl2.line(-P.R, z0 + fy * (-P.R - y0), P.R, z0 + fy * (P.R - y0), { c: "orange", w: 1.6, dash: true }); sl2.dot(y0, z0, { c: "orange", r: 5 });
      ro.set("f", n(z0)); ro.set("fx", n(fx)); ro.set("fy", n(fy));
      note(L.partNote(tn(fx), tn(fy)));
    }
    const redraw = debounce(() => { bg = null; draw(); h._place(); });
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
    const ui = FV.shell(el), note = noter(ui);
    ui.stage.classList.add("dr-narrow");
    let P = GF[cfg.preset] || GF.bowl, ang = cfg.angle != null ? cfg.angle : 30;
    const R = 2, M = 2.6, ARR = 0.55; // the point lives in [−R, R]², the frame is [−M, M]², arrows are at most ARR long
    const plot = new FV.Plot(ui.stage, { x: [-M, M], y: [-M, M], equal: true, xLabel: "x", yLabel: "y" });
    const seg = FV.ui.seg({ label: L.surf, value: cfg.preset || "bowl", options: Object.keys(GF).map((k) => ({ value: k, label: "$" + GF[k].tex + "$" })), onchange: (k) => { P = GF[k]; h.set(P.p[0], P.p[1]); bg = null; draw(); } });
    const sa = FV.ui.slider({ label: L.dir, min: 0, max: 360, step: 1, value: ang, fmt: (v) => Math.round(v) + "°", oninput: (v) => { ang = v; draw(); } });
    ui.controls.append(seg.el, sa.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "g", label: L.grad, c: "red" }, { key: "n", label: L.gnorm }, { key: "d", label: L.du, c: "blue" }]);
    const h = plot.handle(P.p[0], P.p[1], { c: "orange", label: L.ptP, step: [0.05, 0.05], onDrag: (x, y) => [FV.clamp(x, -R, R), FV.clamp(y, -R, R)], onChange: () => draw() });
    let bg = null, dyn = null;
    function background() {
      plot.clear();
      plot.heat(P.f, { cmap: "viridis", alpha: 0.28, res: 4 });
      plot.contours(P.f, P.levels, { c: "ink", w: 1, opacity: 0.35 });
      const gs = FV.linspace(-R, R, 9);
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
        if (gn > 1e-9) { const s = Math.min(ARR, 0.25 * gn) / gn; plot.arrow(x, y, x + g[0] * s, y + g[1] * s, { c: "red", w: 2.6 }); }
        plot.arrow(x, y, x + ARR * u[0], y + ARR * u[1], { c: "blue", w: 2.6 });
      } finally { plot.gMain = keep; }
      ro.set("g", pv(g)); ro.set("n", n(gn)); ro.set("d", n(d));
      if (gn < 1e-9) { note(L.flat); return; }
      const phi = Math.acos(FV.clamp(d / gn, -1, 1)) * 180 / Math.PI;
      note(L.gradNote(tv(g), tn(gn), tn(d), tn(phi, 3)));
    }
    plot.onresize = debounce(() => { bg = null; draw(); h._place(); });
    draw();
  });

  // ---------- 5. gradient descent on a bowl ----------
  FV.widget("dr-descent", (el, cfg) => {
    const ui = FV.shell(el), note = noter(ui);
    ui.stage.classList.add("dr-narrow");
    const a = cfg.a || 1, b = cfg.b || 1; // f = a x² + b y²
    const f = (x, y) => a * x * x + b * y * y, g = (x, y) => [2 * a * x, 2 * b * y];
    const MAXSTEPS = 60;
    let eta = cfg.eta || 0.1, p0 = (cfg.p || [3, 4]).slice(), path = [p0.slice()], timer = 0, msg = "";
    const R = 5;
    const plot = new FV.Plot(ui.stage, { x: [-R, R], y: [-R, R], equal: true, xLabel: "x", yLabel: "y" });
    const se = FV.ui.slider({ label: L.eta, min: 0.02, max: 1.1, step: 0.01, value: eta, oninput: (v) => { stop(); eta = v; reset(); } });
    const go = toggleButton(L.go, () => (timer ? stop() : start()));
    const stepB = FV.ui.button({ label: FV.t("step") + " →", onclick: () => { stop(); step(); } });
    const rs = FV.ui.button({ label: "↺ " + L.reset, onclick: () => { stop(); reset(); } });
    ui.controls.append(se.el, go.el, stepB.el, rs.el);
    // the table: the header once, the body is rebuilt
    const tbl = FV.h("div", { class: "table-wrap dr-desc-wrap", role: "region", "aria-label": FV.plain(L.tbl) });
    tbl.innerHTML = `<table class="data"><thead><tr><th class=num scope="col"></th><th class=num scope="col"></th><th class="num dr-g" scope="col"></th><th class=num scope="col"></th></tr></thead><tbody></tbody></table>`;
    const ths = tbl.querySelectorAll("th"), tbody = tbl.querySelector("tbody");
    ths[0].textContent = L.thK;
    [L.thP, L.thG, L.thF].forEach((s, i) => { ths[i + 1].append(FV.rich(s)); ths[i + 1].setAttribute("aria-label", FV.plain(s)); });
    ui.readout.append(tbl);
    const snap = (x, y) => [Math.round(x * 10) / 10, Math.round(y * 10) / 10];
    const h = plot.handle(p0[0], p0[1], { c: "orange", label: L.start, step: [0.1, 0.1], onDrag: snap, onChange: (x, y) => { p0 = [x, y]; stop(); reset(); } });
    let bg = false, dyn = null;
    function background() {
      plot.clear();
      plot.heat(f, { cmap: "viridis", alpha: 0.28, res: 4 });
      plot.contours(f, [1, 2, 4, 8, 12, 16, 25, 36].map((v) => v * Math.min(a, b)), { c: "ink", w: 1, opacity: 0.35 });
      plot.legend([{ label: L.path, c: "red" }]);
      dyn = FV.svg("g", {}, plot.gMain); bg = true;
    }
    function buttons() { const done = !!msg; stepB.el.disabled = done; go.el.disabled = done && !timer; }
    function reset() { path = [p0.slice()]; msg = ""; buttons(); draw(); }
    function step() {
      if (msg) return false;
      const p = path[path.length - 1], gr = g(p[0], p[1]), q = [p[0] - eta * gr[0], p[1] - eta * gr[1]];
      if (Math.hypot(q[0] - p[0], q[1] - p[1]) < 1e-9) { msg = L.converged; buttons(); draw(); return false; }
      path.push(q);
      if (!q.every(Number.isFinite) || Math.hypot(q[0], q[1]) > 1e6) msg = L.diverged;
      else if (path.length > MAXSTEPS) msg = L.maxed;
      buttons(); draw();
      return !msg;
    }
    function start() {
      if (reduced()) { for (let i = 0; i < 10; i++) if (!step()) break; return; }
      go.set(true);
      let k = 0;
      timer = setInterval(() => { if (!step() || ++k >= 30) stop(); }, 350);
    }
    function stop() { if (!timer) return; clearInterval(timer); timer = 0; go.set(false); buttons(); draw(); }
    document.addEventListener("visibilitychange", () => { if (document.hidden && timer) stop(); });
    const fmtV = (v) => "(" + v.map((x) => n(x, 3)).join(PSEP) + ")";
    function draw() {
      if (!bg) background();
      dyn.textContent = "";
      const keep = plot.gMain; plot.gMain = dyn;
      try {
        // points far outside are capped only to keep the SVG numbers sane; the frame clips the rest, so lines stay straight
        const vis = path.map((q) => [FV.clamp(q[0], -1e4, 1e4), FV.clamp(q[1], -1e4, 1e4)]);
        plot.path(vis, { c: "red", w: 2 });
        vis.forEach((q, i) => plot.dot(q[0], q[1], { c: i ? "red" : "orange", r: i ? 3.5 : 5 }));
      } finally { plot.gMain = keep; }
      tbody.innerHTML = path.slice(-8).map((q, i, arr) => { const k = path.length - arr.length + i, gr = g(q[0], q[1]); return `<tr><th class=num scope="row">${k}</th><td class=num>${fmtV(q)}</td><td class="num dr-g">${fmtV(gr)}</td><td class=num>${n(f(q[0], q[1]), 4)}</td></tr>`; }).join("");
      const last = path[path.length - 1];
      note(L.descNote(path.length - 1, tv(last), tn(f(last[0], last[1]), 4), tn(1 - 2 * a * eta, 3)) + (msg ? " " + msg : ""));
    }
    plot.onresize = debounce(() => { bg = false; draw(); h._place(); });
    reset();
  });

  // ---------- 6. the practice: open or close every solution at once ----------
  FV.widget("dr-solutions", (el) => {
    el.classList.add("cr-sol-bar");
    const all = () => Array.from(document.querySelectorAll("details.cr-sol"));
    if (!all().length) { el.textContent = ""; return; }
    const b = FV.ui.button({ label: L.show, onclick: () => { const open = all().some((d) => !d.open); all().forEach((d) => { d.open = open; }); sync(); } });
    function sync() { b.setLabel(all().every((d) => d.open) ? L.hide : L.show); }
    document.addEventListener("toggle", (e) => { if (e.target.matches && e.target.matches("details.cr-sol")) sync(); }, true);
    el.textContent = ""; el.append(b.el);
    sync();
  });
})();
