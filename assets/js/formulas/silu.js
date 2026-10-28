/* Widgets of the formula page "SiLU / Swish". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const LANG = (typeof FV !== "undefined" && FV.lang) || "en";
  const L = {
    ru: {
      x: "x", gate: "вентиль σ(x)", signal: "сигнал x", silu: "SiLU(x) = x·σ(x)", relu: "ReLU", min: "минимум", deriv: "Показать вторую производную",
      d1: "SiLU′(x)", d2: "SiLU″(x)", part1: "σ(x)", part2: "x·σ′(x)", sum: "SiLU′ = σ + x·σ′", beta: "Крутизна $\\beta$", half: "x/2 ($\\beta=0$)",
      xmin: "точка минимума", fmin: "значение минимума", slope0: "наклон в нуле", dmax: "макс. производная", view: "Вид", fn: "$f$", fd: "$f'$", fdd: "$f''$",
      noise: "Шум", logistic: "логистический → SiLU", normal: "нормальный → GELU", samples: "выборок на точку", maxdev: "макс. отклонение среднего",
      mean: "среднее x·[ε ≤ x]", pass: "вход прошёл: y = x", block: "вход закрыт: y = 0", gateKind: "Вентиль", a: "a (ветка вентиля)", b: "b (ветка значения)",
      out: "выход", top: "Вид сверху", da: "∂/∂a =", db: "∂/∂b =", fit: "Аппроксимация", loss: "MSE (лог. шкала)", step: "шаг", data: "данные",
      neurons: "Показать нейроны", seed: "Инициализация", lossS: "MSE SiLU", lossR: "MSE ReLU", hover: "Наведите курсор на график", gelu: "GELU",
      bilinear: "без вентиля (a·b)", gateA: "вентиль(a) =",
    },
    en: {
      x: "x", gate: "gate σ(x)", signal: "signal x", silu: "SiLU(x) = x·σ(x)", relu: "ReLU", min: "minimum", deriv: "Show the second derivative",
      d1: "SiLU′(x)", d2: "SiLU″(x)", part1: "σ(x)", part2: "x·σ′(x)", sum: "SiLU′ = σ + x·σ′", beta: "Steepness $\\beta$", half: "x/2 ($\\beta=0$)",
      xmin: "minimum point", fmin: "minimum value", slope0: "slope at zero", dmax: "max derivative", view: "View", fn: "$f$", fd: "$f'$", fdd: "$f''$",
      noise: "Noise", logistic: "logistic → SiLU", normal: "normal → GELU", samples: "samples per point", maxdev: "max deviation of the mean",
      mean: "mean of x·[ε ≤ x]", pass: "input passed: y = x", block: "input blocked: y = 0", gateKind: "Gate", a: "a (gate branch)", b: "b (value branch)",
      out: "output", top: "View from above", da: "∂/∂a =", db: "∂/∂b =", fit: "Approximation", loss: "MSE (log scale)", step: "step", data: "data",
      neurons: "Show the neurons", seed: "Initialization", lossS: "MSE SiLU", lossR: "MSE ReLU", hover: "Hover over the plot", gelu: "GELU",
      bilinear: "no gate (a·b)", gateA: "gate(a) =",
    },
    uz: {
      x: "x", gate: "ventil σ(x)", signal: "signal x", silu: "SiLU(x) = x·σ(x)", relu: "ReLU", min: "minimum", deriv: "Ikkinchi hosilani ko‘rsatish",
      d1: "SiLU′(x)", d2: "SiLU″(x)", part1: "σ(x)", part2: "x·σ′(x)", sum: "SiLU′ = σ + x·σ′", beta: "Tiklik $\\beta$", half: "x/2 ($\\beta=0$)",
      xmin: "minimum nuqtasi", fmin: "minimum qiymati", slope0: "noldagi qiyalik", dmax: "maks. hosila", view: "Ko‘rinish", fn: "$f$", fd: "$f'$", fdd: "$f''$",
      noise: "Shovqin", logistic: "logistik → SiLU", normal: "normal → GELU", samples: "nuqtaga tanlanmalar", maxdev: "o‘rtachaning maks. chetlanishi",
      mean: "x·[ε ≤ x] o‘rtachasi", pass: "kirish o‘tdi: y = x", block: "kirish yopildi: y = 0", gateKind: "Ventil", a: "a (ventil tarmog‘i)", b: "b (qiymat tarmog‘i)",
      out: "chiqish", top: "Yuqoridan ko‘rinish", da: "∂/∂a =", db: "∂/∂b =", fit: "Approksimatsiya", loss: "MSE (log. shkala)", step: "qadam", data: "ma’lumotlar",
      neurons: "Neyronlarni ko‘rsatish", seed: "Initsializatsiya", lossS: "MSE SiLU", lossR: "MSE ReLU", hover: "Kursorni grafikka olib boring", gelu: "GELU",
      bilinear: "ventilsiz (a·b)", gateA: "ventil(a) =",
    },
  }[LANG] || {};

  // ---------- pure math (also used by the numeric checks in node) ----------
  const sig = (x) => (x >= 0 ? 1 / (1 + Math.exp(-x)) : Math.exp(x) / (1 + Math.exp(x)));
  const silu = (x) => x * sig(x);
  const dsilu = (x) => { const s = sig(x); return s * (1 + x * (1 - s)); };
  const d2silu = (x) => { const s = sig(x); return s * (1 - s) * (2 + x * (1 - 2 * s)); };
  const SQ2PI = Math.sqrt(2 * Math.PI);
  const phi = (x) => Math.exp(-0.5 * x * x) / SQ2PI;
  function erf(x) { const s = Math.sign(x), a = Math.abs(x), t = 1 / (1 + 0.3275911 * a); return s * (1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-a * a)); }
  const Phi = (x) => 0.5 * (1 + erf(x / Math.SQRT2));
  const gelu = (x) => x * Phi(x), dgelu = (x) => Phi(x) + x * phi(x), d2gelu = (x) => phi(x) * (2 - x * x);
  const swish = (x, b) => x * sig(b * x);
  const dswish = (x, b) => { const s = sig(b * x); return s + b * x * s * (1 - s); };
  const XMIN = -1.2784645427610738, FMIN = -0.27846454276107374; // x* = −1 − W(1/e), SiLU(x*) = −W(1/e)
  function rng(seed) {
    if (typeof FV !== "undefined" && FV.rng) return FV.rng(seed);
    let s = seed >>> 0;
    const next = () => { s = (s + 0x6d2b79f5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    next.normal = () => { const u = Math.max(next(), 1e-12), v = next(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
    return next;
  }

  // Stochastic gate: y = x·[ε ≤ x]. Logistic ε gives E y = x·σ(x) = SiLU, normal ε gives x·Φ(x) = GELU.
  const NOISE_X = Array.from({ length: 33 }, (_, i) => -4 + i / 4);
  function noiseState(kind) { return { kind, r: rng(kind === "normal" ? 19 : 17), n: 0, sum: NOISE_X.map(() => 0), last: NOISE_X.map(() => 0) }; }
  function noiseStep(S, m) {
    for (let k = 0; k < m; k++) {
      NOISE_X.forEach((x, i) => {
        let e;
        if (S.kind === "normal") e = S.r.normal();
        else { const u = Math.min(Math.max(S.r(), 1e-12), 1 - 1e-12); e = Math.log(u / (1 - u)); }
        const y = e <= x ? x : 0;
        S.sum[i] += y; S.last[i] = y;
      });
      S.n++;
    }
  }
  function noiseDev(S) { const f = S.kind === "normal" ? gelu : silu; return NOISE_X.reduce((m, x, i) => Math.max(m, Math.abs(S.sum[i] / Math.max(S.n, 1) - f(x))), 0); }

  // A 1 → 6 → 1 network fitted with Adam: SiLU and ReLU from the same initialization.
  const TR = (() => { const xs = [], ys = [], n = 40; for (let i = 0; i < n; i++) { const x = -3 + (6 * i) / (n - 1); xs.push(x); ys.push(Math.sin(1.5 * x) + 0.3 * x); } return { xs, ys, n, H: 6, lr: 0.03, T: 2000 }; })();
  const ACT = { silu: { f: silu, d: dsilu }, relu: { f: (x) => (x > 0 ? x : 0), d: (x) => (x > 0 ? 1 : 0) } };
  function trInit(seed) {
    const r = rng(seed), P = { w: [], b: [], v: [], c: 0 };
    for (let k = 0; k < TR.H; k++) { P.w.push(r.normal()); P.b.push(r.normal()); P.v.push(r.normal() / Math.sqrt(TR.H)); }
    const z = () => ({ w: new Array(TR.H).fill(0), b: new Array(TR.H).fill(0), v: new Array(TR.H).fill(0), c: 0 });
    return { P, m: z(), s: z(), t: 0 };
  }
  function trOut(P, act, x) { let o = P.c; for (let k = 0; k < TR.H; k++) o += P.v[k] * act.f(P.w[k] * x + P.b[k]); return o; }
  function trLoss(P, act) { let l = 0; for (let i = 0; i < TR.n; i++) { const e = trOut(P, act, TR.xs[i]) - TR.ys[i]; l += e * e; } return l / TR.n; }
  function trStep(S, act) {
    const P = S.P, H = TR.H, g = { w: new Array(H).fill(0), b: new Array(H).fill(0), v: new Array(H).fill(0), c: 0 };
    for (let i = 0; i < TR.n; i++) {
      const x = TR.xs[i], z = new Array(H), a = new Array(H);
      let o = P.c;
      for (let k = 0; k < H; k++) { z[k] = P.w[k] * x + P.b[k]; a[k] = act.f(z[k]); o += P.v[k] * a[k]; }
      const e = (2 * (o - TR.ys[i])) / TR.n;
      g.c += e;
      for (let k = 0; k < H; k++) { g.v[k] += e * a[k]; const gz = e * P.v[k] * act.d(z[k]); g.w[k] += gz * x; g.b[k] += gz; }
    }
    S.t++;
    const c1 = 1 - Math.pow(0.9, S.t), c2 = 1 - Math.pow(0.999, S.t);
    ["w", "b", "v"].forEach((key) => { for (let k = 0; k < H; k++) { S.m[key][k] = 0.9 * S.m[key][k] + 0.1 * g[key][k]; S.s[key][k] = 0.999 * S.s[key][k] + 0.001 * g[key][k] * g[key][k]; P[key][k] -= (TR.lr * (S.m[key][k] / c1)) / (Math.sqrt(S.s[key][k] / c2) + 1e-8); } });
    S.m.c = 0.9 * S.m.c + 0.1 * g.c; S.s.c = 0.999 * S.s.c + 0.001 * g.c * g.c; P.c -= (TR.lr * (S.m.c / c1)) / (Math.sqrt(S.s.c / c2) + 1e-8);
  }
  function trRun(seed, kind, T) { const S = trInit(seed); for (let t = 0; t < T; t++) trStep(S, ACT[kind]); return trLoss(S.P, ACT[kind]); }

  const GATES = {
    silu: { f: silu, d: dsilu, label: "SwiGLU: SiLU(a)·b" },
    gelu: { f: gelu, d: dgelu, label: "GEGLU: GELU(a)·b" },
    relu: { f: (a) => Math.max(0, a), d: (a) => (a > 0 ? 1 : 0), label: "ReGLU: ReLU(a)·b" },
    sigmoid: { f: sig, d: (a) => sig(a) * (1 - sig(a)), label: "GLU: σ(a)·b" },
    none: { f: (a) => a, d: () => 1, label: "a·b" },
  };

  if (typeof module === "object" && module.exports) module.exports = { sig, silu, dsilu, d2silu, gelu, dgelu, d2gelu, swish, dswish, noiseState, noiseStep, noiseDev, trRun, trInit, trStep, trLoss, ACT, TR, GATES, NOISE_X };
  if (typeof FV === "undefined" || !FV.widget) return;

  // 1. Self-gating: the signal x, the gate σ(x) and their product.
  FV.widget("silu-explorer", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-6, 4], y: [-1, 4], xLabel: L.x, yLabel: "y", aspect: 0.52 });
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "g", label: "σ(x) =", c: "teal" }, { key: "f", label: "x·σ(x) =", c: "blue" }, { key: "r", label: "ReLU(x) =" }]);
    let x0 = cfg.x != null ? cfg.x : -1;
    const h = p.handle(x0, silu(x0), { c: "blue", onDrag: (x) => { x0 = x; return [x, silu(x)]; }, onChange: () => draw() });
    function draw() {
      p.clear();
      p.fn((x) => x, { c: "faint", w: 1.2, dash: "2 4" });
      p.fn((x) => Math.max(0, x), { c: "guide", w: 1.6, dash: "5 4" });
      p.fn(sig, { c: "teal", w: 2 });
      p.fn(silu, { c: "blue", w: 2.8 });
      const g = sig(x0), y0 = silu(x0);
      p.line(x0, 0, x0, g, { c: "teal", w: 1.4, dash: "3 3" });
      p.dot(x0, g, { c: "teal", r: 4 });
      p.dot(XMIN, FMIN, { c: "ink", hollow: true, r: 4 });
      p.text(-5.85, -0.8, (p.narrow ? "" : L.min + " ") + "(" + FV.fmt(XMIN, 3) + (LANG === "en" ? ", " : "; ") + FV.fmt(FMIN, 3) + ")", { c: "ink", anchor: "start", size: 12 });
      p.line(XMIN, FMIN, XMIN, -0.68, { c: "ink", w: 1, dash: "2 2", opacity: 0.6 });
      h.set(x0, y0);
      p.legend([{ label: L.silu, c: "blue" }, { label: L.gate, c: "teal" }, { label: L.signal, c: "faint", dash: true }, { label: L.relu, c: "guide", dash: true }]);
      ro.set("x", FV.fmt(x0, 2)); ro.set("g", FV.fmt(g, 4)); ro.set("f", FV.fmt(y0, 4)); ro.set("r", FV.fmt(Math.max(0, x0), 2));
    }
    p.onresize = draw; draw();
  });

  // 2. The derivative as a sum of two terms (product rule), its overshoot above 1, and the second derivative.
  FV.widget("silu-derivative", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-6, 6], y: [-0.4, 1.4], xLabel: L.x, yLabel: L.d1, aspect: 0.5 });
    const box = FV.h("div"); w.stage.append(box);
    let d = null;
    const show = FV.ui.check({ label: L.deriv, checked: cfg.second !== false, onchange: (v) => { box.hidden = !v; draw(); } });
    w.controls.append(show.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "s", label: "σ(x) =", c: "teal" }, { key: "t", label: "x·σ′(x) =", c: "violet" }, { key: "d", label: "SiLU′(x) =", c: "orange" }, { key: "dd", label: "SiLU″(x) =", c: "red" }]);
    const XM = 2.3993572805154675, DM = 1.0998393201288668;
    let x0 = cfg.x != null ? cfg.x : XM;
    const h = p.handle(x0, dsilu(x0), { c: "orange", onDrag: (x) => { x0 = x; return [x, dsilu(x)]; }, onChange: () => draw() });
    function draw() {
      p.clear();
      p.hline(1, { c: "guide" }); p.hline(0, { c: "guide", dash: false });
      p.fn(sig, { c: "teal", w: 1.6, dash: "5 4" });
      p.fn((x) => x * sig(x) * (1 - sig(x)), { c: "violet", w: 1.6, dash: "5 4" });
      p.fn(dsilu, { c: "orange", w: 2.8 });
      p.dot(XM, DM, { c: "orange", hollow: true, r: 4 }); p.dot(-XM, 1 - DM, { c: "orange", hollow: true, r: 4 });
      p.text(XM + 0.5, DM + 0.13, "max ≈ " + FV.fmt(DM, 4), { c: "orange", anchor: "start", size: 12 });
      p.text(-XM, 1 - DM - 0.17, "min ≈ " + FV.fmt(1 - DM, 4), { c: "orange", anchor: "middle", size: 12 });
      h.set(x0, dsilu(x0));
      p.legend([{ label: L.sum, c: "orange" }, { label: L.part1, c: "teal", dash: true }, { label: L.part2, c: "violet", dash: true }]);
      if (show.value) {
        if (!d) { d = new FV.Plot(box, { x: [-6, 6], y: [-0.15, 0.6], xLabel: L.x, yLabel: L.d2, aspect: 0.28, minHeight: 160, maxHeight: 220 }); d.onresize = draw; }
        box.hidden = false;
        d.clear();
        d.hline(0, { c: "guide", dash: false });
        d.area(d2silu, null, { c: "red", fillOpacity: 0.1 });
        d.fn(d2silu, { c: "red", w: 2.2 });
        d.vline(XM, { c: "faint" }); d.vline(-XM, { c: "faint" });
        d.dot(x0, d2silu(x0), { c: "red", r: 4 });
      }
      ro.set("x", FV.fmt(x0, 3)); ro.set("s", FV.fmt(sig(x0), 4)); ro.set("t", FV.fmt(x0 * sig(x0) * (1 - sig(x0)), 4));
      ro.set("d", FV.fmt(dsilu(x0), 4)); ro.set("dd", FV.fmt(d2silu(x0), 4));
    }
    p.onresize = draw; draw();
  });

  // 3. The Swish family x·σ(βx): from x/2 to ReLU.
  FV.widget("silu-beta", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-5, 4], y: [-1, 4], xLabel: L.x, yLabel: "x·σ(βx)", aspect: 0.5 });
    const box = FV.h("div"); w.stage.append(box);
    const d = new FV.Plot(box, { x: [-5, 4], y: [-0.2, 1.25], xLabel: L.x, yLabel: "∂/∂x", aspect: 0.26, minHeight: 150, maxHeight: 210 });
    const sb = FV.ui.slider({ label: L.beta, min: 0, max: 10, step: 0.05, value: cfg.beta != null ? cfg.beta : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sb.el);
    const ro = FV.ui.readout(w.readout, [{ key: "xm", label: L.xmin + " =" }, { key: "fm", label: L.fmin + " =", c: "blue" }, { key: "s0", label: L.slope0 + " =", c: "orange" }, { key: "dm", label: L.dmax + " =", c: "orange" }]);
    function draw() {
      const b = sb.value, f = (x) => swish(x, b), df = (x) => dswish(x, b);
      p.clear();
      p.fn((x) => Math.max(0, x), { c: "guide", w: 1.6, dash: "5 4" });
      p.fn((x) => x / 2, { c: "faint", w: 1.2, dash: "2 4" });
      p.fn(silu, { c: "ink", w: 1.2, opacity: 0.35 });
      p.fn(f, { c: "blue", w: 2.8 });
      if (b > 1e-9) p.dot(XMIN / b, FMIN / b, { c: "blue", hollow: true, r: 4 });
      p.legend([{ label: "x·σ(βx), β = " + FV.fmt(b, 2), c: "blue" }, { label: "SiLU (β = 1)", c: "ink" }, { label: "ReLU (β → ∞)", c: "guide", dash: true }, { label: "x/2 (β = 0)", c: "faint", dash: true }]);
      d.clear();
      d.hline(1, { c: "guide" }); d.hline(0.5, { c: "faint" });
      d.fn(df, { c: "orange", w: 2.4 });
      ro.set("xm", b > 1e-9 ? FV.fmt(XMIN / b, 3) : "—"); ro.set("fm", b > 1e-9 ? FV.fmt(FMIN / b, 3) : "—");
      ro.set("s0", FV.fmt(0.5, 2)); ro.set("dm", b > 1e-9 ? FV.fmt(1.0998393201288668, 4) : FV.fmt(0.5, 2));
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 4. SiLU, GELU and ReLU side by side: function, first and second derivative.
  FV.widget("silu-compare", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-4, 3], y: [-0.6, 3], xLabel: L.x, yLabel: "f(x)", aspect: 0.5 });
    const view = FV.ui.seg({ label: L.view, value: cfg.view || "f", options: [{ value: "f", label: L.fn }, { value: "d", label: L.fd }, { value: "dd", label: L.fdd }], onchange: draw });
    w.controls.append(view.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "s", label: "SiLU:", c: "blue" }, { key: "g", label: "GELU:", c: "teal" }, { key: "r", label: "ReLU:" }]);
    const FN = {
      f: [silu, gelu, (x) => Math.max(0, x), [-0.6, 3], "f(x)"],
      d: [dsilu, dgelu, (x) => (x > 0 ? 1 : 0), [-0.25, 1.3], "f′(x)"],
      dd: [d2silu, d2gelu, (x) => (x === 0 ? Infinity : 0), [-0.3, 0.95], "f″(x)"],
    };
    let hx = cfg.x != null ? cfg.x : -1;
    p.hover((x) => { if (x != null) { hx = x; mark(); } });
    function mark() {
      const [a, b, c] = FN[view.value];
      p.hl("line", hx, p.o.y[0], hx, p.o.y[1], { c: "guide", w: 1, dash: "3 3" });
      p.hl("dot", hx, a(hx), { c: "blue", r: 4 }); p.hl("dot", hx, b(hx), { c: "teal", r: 4 });
      ro.set("x", FV.fmt(hx, 2)); ro.set("s", FV.fmt(a(hx), 3)); ro.set("g", FV.fmt(b(hx), 3));
      const rv = c(hx); ro.set("r", Number.isFinite(rv) ? FV.fmt(rv, 3) : "∞");
    }
    function draw() {
      const [a, b, c, yr, yl] = FN[view.value];
      p.setDomain(null, yr); p.o.yLabel = yl;
      p.clear();
      if (view.value === "dd") {
        p.line(-4, 0, 3, 0, { c: "guide", w: 1.6, dash: "5 4" });
        p.arrow(0, 0, 0, yr[1] * 0.97, { c: "guide", w: 1.6 });
        p.text(0.08, yr[1] * 0.86, "δ(x)", { c: "faint" });
      } else if (view.value === "d") {
        p.line(-4, 0, 0, 0, { c: "guide", w: 1.6, dash: "5 4" }); p.line(0, 1, 3, 1, { c: "guide", w: 1.6, dash: "5 4" });
      } else p.fn(c, { c: "guide", w: 1.6, dash: "5 4" });
      p.fn(b, { c: "teal", w: 2.2 });
      p.fn(a, { c: "blue", w: 2.6 });
      p.legend([{ label: "SiLU", c: "blue" }, { label: "GELU", c: "teal" }, { label: "ReLU", c: "guide", dash: true }]);
      mark();
    }
    p.onresize = draw; draw();
  });

  // 5. A stochastic gate: the input passes when the noise ε ≤ x. Averaging gives SiLU (logistic ε) or GELU (normal ε).
  FV.widget("silu-noise", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-4.2, 4.2], y: [-1, 4.2], xLabel: L.x, yLabel: "y", aspect: 0.5 });
    const MAX = 2000, PER = 20;
    const kind = FV.ui.seg({ label: L.noise, value: cfg.noise || "logistic", options: [{ value: "logistic", label: L.logistic }, { value: "normal", label: L.normal }], onchange: () => { player.stop(); reset(); } });
    let S;
    const player = FV.ui.player({ interval: 50, onstep() { noiseStep(S, PER); draw(); return S.n < MAX; }, onreset: () => reset() });
    w.controls.append(kind.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "n", label: L.samples + ":" }, { key: "d", label: L.maxdev + ":", c: "blue" }]);
    function reset() { S = noiseState(kind.value); draw(); }
    function draw() {
      const f = kind.value === "normal" ? gelu : silu;
      p.clear();
      p.fn((x) => x, { c: "faint", w: 1.2, dash: "2 4" }); p.hline(0, { c: "faint", dash: "2 4", w: 1.2 });
      p.fn(f, { c: "blue", w: 2.4 });
      if (S.n > 0) NOISE_X.forEach((x, i) => { p.dot(x, S.last[i], { c: "faint", r: 2.5 }); p.dot(x, S.sum[i] / S.n, { c: "orange", r: 4 }); });
      p.legend([{ label: kind.value === "normal" ? "GELU = x·Φ(x)" : "SiLU = x·σ(x)", c: "blue" }, { label: L.mean, c: "orange", dot: true }, { label: L.pass + " / " + L.block, c: "faint", dash: true }]);
      ro.set("n", String(S.n)); ro.set("d", S.n ? FV.fmt(noiseDev(S), 3) : "—");
    }
    p.onresize = draw; reset();
  });

  // 6. SwiGLU in 3D: out = SiLU(a)·b over the plane (a, b), and its relatives.
  FV.widget("silu-swiglu", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const R = 4;
    let G = GATES[cfg.gate || "silu"];
    const P = { a: cfg.a != null ? cfg.a : 1.5, b: cfg.b != null ? cfg.b : 2 };
    const f = (a, b) => G.f(a) * b;
    const zmax = () => { let m = 0; for (let i = 0; i <= 40; i++) m = Math.max(m, Math.abs(G.f(-R + (2 * R * i) / 40)) * R); return m; };
    const s3 = new FV.Surface(FV.col(w.stage), { f, x: [-R, R], y: [-R, R], z: [-zmax(), zmax()], n: 40, labels: { x: "a", y: "b", z: L.out }, azimuth: -0.65, elevation: 0.5, aspect: 0.85, cmap: "diverging", title: G.label });
    const titleEl = s3.wrap.querySelector(".fv-plot-title");
    const top = new FV.Plot(FV.col(w.stage), { x: [-R, R], y: [-R, R], xLabel: "a", equal: true, title: L.top });
    const gs = FV.ui.seg({ label: L.gateKind, value: cfg.gate || "silu", options: [{ value: "silu", label: "SwiGLU" }, { value: "gelu", label: "GEGLU" }, { value: "relu", label: "ReGLU" }, { value: "sigmoid", label: "GLU" }, { value: "none", label: L.bilinear }], onchange: (v) => { G = GATES[v]; s3.o.z = [-zmax(), zmax()]; if (titleEl) { titleEl.textContent = ""; titleEl.append(FV.rich(G.label)); } draw(); } });
    w.controls.append(gs.el);
    const ro = FV.ui.readout(w.readout, [{ key: "a", label: "a =" }, { key: "b", label: "b =" }, { key: "g", label: L.gateA, c: "teal" }, { key: "o", label: L.out + " =", c: "blue" }, { key: "da", label: L.da, c: "orange" }, { key: "db", label: L.db, c: "orange" }]);
    const hd = top.handle(P.a, P.b, { c: "orange", onChange: (x, y) => { P.a = x; P.b = y; draw(); } });
    function draw() {
      const zm = zmax();
      s3.f = f; s3.sample();
      s3.setPoints([{ x: P.a, y: P.b, z: f(P.a, P.b), c: "orange", r: 5 }]);
      top.clear();
      top.heat(f, { cmap: "diverging", res: 4, alpha: 0.85, z: [-zm, zm] });
      const lv = [-0.6, -0.3, 0.3, 0.6].map((t) => t * zm);
      top.contours(f, lv, { style: () => ({ c: "ink", w: 1, opacity: 0.35 }) });
      top.contours(f, [0], { style: () => ({ c: "ink", w: 1.6, opacity: 0.7 }) });
      top.text(-R + 0.15, R - 0.35, "b", { c: "ink" });
      hd.set(P.a, P.b);
      const g = G.f(P.a);
      ro.set("a", FV.fmt(P.a, 2)); ro.set("b", FV.fmt(P.b, 2)); ro.set("g", FV.fmt(g, 3)); ro.set("o", FV.fmt(g * P.b, 3));
      ro.set("da", FV.fmt(G.d(P.a) * P.b, 3)); ro.set("db", FV.fmt(g, 3));
    }
    top.onresize = draw; draw();
  });

  // 7. Training: a 1 → 6 → 1 network with SiLU and with ReLU fits the same curve from the same start.
  FV.widget("silu-train", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const pf = new FV.Plot(FV.col(w.stage), { x: [-3.2, 3.2], y: [-2.2, 2.2], xLabel: L.x, yLabel: "y", aspect: 0.8, title: L.fit });
    const pl = new FV.Plot(FV.col(w.stage), { x: [0, 2080], y: [1e-4, 10], yType: "log", xLabel: L.step, yLabel: "MSE", aspect: 0.8, title: L.loss });
    const PER = 20;
    const seed = FV.ui.seg({ label: L.seed, value: cfg.seed || 1, options: [1, 2, 3, 4].map((v) => ({ value: v, label: "#" + v })), onchange: () => { player.stop(); reset(); } });
    const nn = FV.ui.check({ label: L.neurons, checked: false, onchange: () => draw() });
    let A, B, hA, hB;
    const player = FV.ui.player({
      interval: 50,
      onstep() { for (let k = 0; k < PER && A.t < TR.T; k++) { trStep(A, ACT.silu); trStep(B, ACT.relu); hA.push(trLoss(A.P, ACT.silu)); hB.push(trLoss(B.P, ACT.relu)); } draw(); return A.t < TR.T; },
      onreset: () => reset(),
    });
    w.controls.append(seed.el, nn.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.step + " =" }, { key: "s", label: L.lossS + " =", c: "blue" }, { key: "r", label: L.lossR + " =" }]);
    function reset() { A = trInit(seed.value); B = trInit(seed.value); hA = [trLoss(A.P, ACT.silu)]; hB = [trLoss(B.P, ACT.relu)]; draw(); }
    function draw() {
      pf.clear();
      if (nn.value) {
        for (let k = 0; k < TR.H; k++) {
          pf.fn((x) => A.P.v[k] * silu(A.P.w[k] * x + A.P.b[k]), { c: "blue", w: 1, opacity: 0.35 });
          pf.fn((x) => B.P.v[k] * Math.max(0, B.P.w[k] * x + B.P.b[k]), { c: "ink", w: 1, opacity: 0.3, dash: "3 3" });
        }
      }
      TR.xs.forEach((x, i) => pf.dot(x, TR.ys[i], { c: "faint", r: 3 }));
      pf.fn((x) => trOut(B.P, ACT.relu, x), { c: "ink", w: 2, dash: "6 4" });
      pf.fn((x) => trOut(A.P, ACT.silu, x), { c: "blue", w: 2.6 });
      pf.legend([{ label: L.data, c: "faint", dot: true }, { label: "SiLU", c: "blue" }, { label: "ReLU", c: "ink", dash: true }]);
      pl.clear();
      pl.path(hB.map((v, i) => [i, Math.max(v, 1e-4)]), { c: "ink", w: 2, dash: "6 4" });
      pl.path(hA.map((v, i) => [i, Math.max(v, 1e-4)]), { c: "blue", w: 2.4 });
      pl.legend([{ label: "SiLU", c: "blue" }, { label: "ReLU", c: "ink", dash: true }]);
      ro.set("t", String(A.t)); ro.set("s", FV.num(trLoss(A.P, ACT.silu), 3)); ro.set("r", FV.num(trLoss(B.P, ACT.relu), 3));
    }
    pf.onresize = draw; pl.onresize = draw; reset();
  });
})();
