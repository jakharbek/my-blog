/* Widgets of the formula page "Leaky ReLU". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const LANG = (typeof FV !== "undefined" && FV.lang) || "en";
  const L = {
    ru: {
      x: "x", f: "LReLU(x)", df: "LReLU′(x)", alpha: "Наклон слева $\\alpha$", tangent: "наклон = производная", relu: "ReLU ($\\alpha=0$)", lin: "линейная ($\\alpha=1$)",
      deriv: "Показать производную", undef: "в нуле не определена", maxTitle: "max(αx, x)", sumTitle: "линейная часть + модуль",
      same: "max(αx, x) = LReLU?", yes: "да", no: "нет: при α > 1 max берёт αx справа", lineX: "y = x", lineAx: "y = αx", cases: "LReLU по определению", maxEnv: "max(αx, x)",
      linPart: "(1 + α)/2 · x", absPart: "(1 − α)/2 · |x|", sum: "сумма = LReLU", view: "Вид", fun: "функция", der: "производная",
      cmp: "Сравнить с", hoverX: "x =", data: "данные", leaky: "нейрон Leaky", reluN: "нейрон ReLU", kink: "излом −b/w", loss: "MSE", step: "шаг",
      lossL: "MSE Leaky", lossR: "MSE ReLU", active: "точек с z > 0 (Leaky)", revived: "ожил на шаге", dataZone: "область данных", lossTitle: "Ошибка (лог. шкала)",
      fitTitle: "Данные и нейроны", never: "никогда", x1: "x₁", x2: "x₂", top: "Вид сверху: линии изломов", regions: "линейных областей", activeU: "активных нейронов",
      grad: "|∇f|", flat: "доля плоскости с ∇f = 0", layer: "слой", rms: "RMS(z)", gain: "Инициализация", depth: "Глубина $L$", measured: "измерено",
      theory: "теория", perLayer: "множитель дисперсии за слой", last: "RMS на последнем слое", xavier: "$g=1$", heRelu: "$g=\\sqrt2$ (Хе для ReLU)", heLeaky: "$g=\\sqrt{2/(1+\\alpha^2)}$",
      w: "w", a: "α", landscape: "Ошибка L(w, α), лог. шкала", path: "путь градиентного спуска", start: "старт (тяните)", teacher: "истина (1,5; 0,2)", fit: "модель",
      dragHint: "Тяните оранжевую точку старта на правом рисунке",
    },
    en: {
      x: "x", f: "LReLU(x)", df: "LReLU′(x)", alpha: "Left slope $\\alpha$", tangent: "slope = derivative", relu: "ReLU ($\\alpha=0$)", lin: "linear ($\\alpha=1$)",
      deriv: "Show the derivative", undef: "undefined at zero", maxTitle: "max(αx, x)", sumTitle: "linear part + absolute value",
      same: "max(αx, x) = LReLU?", yes: "yes", no: "no: for α > 1 the max takes αx on the right", lineX: "y = x", lineAx: "y = αx", cases: "LReLU by definition", maxEnv: "max(αx, x)",
      linPart: "(1 + α)/2 · x", absPart: "(1 − α)/2 · |x|", sum: "sum = LReLU", view: "View", fun: "function", der: "derivative",
      cmp: "Compare with", hoverX: "x =", data: "data", leaky: "Leaky neuron", reluN: "ReLU neuron", kink: "kink −b/w", loss: "MSE", step: "step",
      lossL: "MSE Leaky", lossR: "MSE ReLU", active: "points with z > 0 (Leaky)", revived: "revived at step", dataZone: "data range", lossTitle: "Error (log scale)",
      fitTitle: "Data and neurons", never: "never", x1: "x₁", x2: "x₂", top: "View from above: kink lines", regions: "linear regions", activeU: "active neurons",
      grad: "|∇f|", flat: "share of the plane with ∇f = 0", layer: "layer", rms: "RMS(z)", gain: "Initialization", depth: "Depth $L$", measured: "measured",
      theory: "theory", perLayer: "variance factor per layer", last: "RMS at the last layer", xavier: "$g=1$", heRelu: "$g=\\sqrt2$ (He for ReLU)", heLeaky: "$g=\\sqrt{2/(1+\\alpha^2)}$",
      w: "w", a: "α", landscape: "Error L(w, α), log scale", path: "gradient-descent path", start: "start (drag)", teacher: "truth (1.5, 0.2)", fit: "model",
      dragHint: "Drag the orange start point on the right plot",
    },
    uz: {
      x: "x", f: "LReLU(x)", df: "LReLU′(x)", alpha: "Chapdagi qiyalik $\\alpha$", tangent: "qiyalik = hosila", relu: "ReLU ($\\alpha=0$)", lin: "chiziqli ($\\alpha=1$)",
      deriv: "Hosilani ko‘rsatish", undef: "nolda aniqlanmagan", maxTitle: "max(αx, x)", sumTitle: "chiziqli qism + modul",
      same: "max(αx, x) = LReLU?", yes: "ha", no: "yo‘q: α > 1 da max o‘ngda αx ni oladi", lineX: "y = x", lineAx: "y = αx", cases: "ta’rif bo‘yicha LReLU", maxEnv: "max(αx, x)",
      linPart: "(1 + α)/2 · x", absPart: "(1 − α)/2 · |x|", sum: "yig‘indi = LReLU", view: "Ko‘rinish", fun: "funksiya", der: "hosila",
      cmp: "Taqqoslash", hoverX: "x =", data: "ma’lumotlar", leaky: "Leaky neyron", reluN: "ReLU neyron", kink: "sinish −b/w", loss: "MSE", step: "qadam",
      lossL: "MSE Leaky", lossR: "MSE ReLU", active: "z > 0 bo‘lgan nuqtalar (Leaky)", revived: "jonlandi, qadam", dataZone: "ma’lumotlar sohasi", lossTitle: "Xato (log. shkala)",
      fitTitle: "Ma’lumotlar va neyronlar", never: "hech qachon", x1: "x₁", x2: "x₂", top: "Yuqoridan ko‘rinish: sinish chiziqlari", regions: "chiziqli sohalar", activeU: "faol neyronlar",
      grad: "|∇f|", flat: "∇f = 0 bo‘lgan tekislik ulushi", layer: "qatlam", rms: "RMS(z)", gain: "Initsializatsiya", depth: "Chuqurlik $L$", measured: "o‘lchangan",
      theory: "nazariya", perLayer: "qatlamdagi dispersiya ko‘paytuvchisi", last: "oxirgi qatlamdagi RMS", xavier: "$g=1$", heRelu: "$g=\\sqrt2$ (ReLU uchun He)", heLeaky: "$g=\\sqrt{2/(1+\\alpha^2)}$",
      w: "w", a: "α", landscape: "L(w, α) xato, log. shkala", path: "gradiyent tushish yo‘li", start: "start (torting)", teacher: "haqiqat (1,5; 0,2)", fit: "model",
      dragHint: "O‘ngdagi rasmda to‘q sariq start nuqtasini torting",
    },
  }[LANG] || {};

  // ---------- pure math (also used by the numeric checks in node) ----------
  const lrelu = (x, a) => (x > 0 ? x : a * x);
  const dlrelu = (x, a) => (x > 0 ? 1 : a);
  function rng(seed) {
    if (typeof FV !== "undefined" && FV.rng) return FV.rng(seed);
    let s = seed >>> 0;
    const next = () => { s = (s + 0x6d2b79f5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    next.normal = () => { const u = Math.max(next(), 1e-12), v = next(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
    return next;
  }

  // Revival of a dead neuron: f(x) = v·act(w x + b), target 1.5·max(0, x − 1) on 41 points of [−3, 3].
  const REV = { n: 41, xs: [], ys: [], lr: 0.1 };
  for (let i = 0; i < REV.n; i++) { const x = -3 + (6 * i) / (REV.n - 1); REV.xs.push(x); REV.ys.push(1.5 * Math.max(0, x - 1)); }
  const revInit = () => ({ w: 1, b: -4, v: 1 });
  function revLoss(s, a) { let l = 0; for (let i = 0; i < REV.n; i++) { const e = s.v * lrelu(s.w * REV.xs[i] + s.b, a) - REV.ys[i]; l += e * e; } return l / REV.n; }
  function revStep(s, a) {
    let gw = 0, gb = 0, gv = 0;
    for (let i = 0; i < REV.n; i++) {
      const z = s.w * REV.xs[i] + s.b, act = lrelu(z, a), g = (2 * (s.v * act - REV.ys[i])) / REV.n, gz = g * s.v * dlrelu(z, a);
      gv += g * act; gw += gz * REV.xs[i]; gb += gz;
    }
    s.w -= REV.lr * gw; s.b -= REV.lr * gb; s.v -= REV.lr * gv;
  }
  const revActive = (s) => REV.xs.reduce((c, x) => c + (s.w * x + s.b > 0 ? 1 : 0), 0);
  function revRun(a, T) {
    const s = revInit(); let revived = -1;
    for (let t = 1; t <= T; t++) { revStep(s, a); if (revived < 0 && revActive(s) > 0) revived = t; }
    return { s, revived, loss: revLoss(s, a), kink: -s.b / s.w, active: revActive(s) };
  }

  // A small fixed network 2 → 6 → 1 for the 3D picture.
  const NET = (() => {
    const th = [0.35, 1.4, 2.45, 3.5, 4.55, 5.6], b = [-0.8, -0.5, -1.0, -0.6, -0.9, -0.7], v = [1.0, -0.8, 0.6, 0.9, -0.7, -0.5];
    return th.map((t, k) => ({ w1: Math.cos(t), w2: Math.sin(t), b: b[k], v: v[k] }));
  })();
  function netF(x1, x2, a) { let s = 0; NET.forEach((u) => { s += u.v * lrelu(u.w1 * x1 + u.w2 * x2 + u.b, a); }); return s; }
  function netGrad(x1, x2, a) { let g1 = 0, g2 = 0, on = 0; NET.forEach((u) => { const z = u.w1 * x1 + u.w2 * x2 + u.b, d = dlrelu(z, a); if (z > 0) on++; g1 += u.v * d * u.w1; g2 += u.v * d * u.w2; }); return { g: Math.hypot(g1, g2), on }; }
  function netStats(a, R) {
    // distinct activation patterns and the share of the square [−R, R]² where the gradient is exactly zero
    const n = 160, pats = new Set(); let flat = 0;
    for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
      const x1 = -R + (2 * R * (i + 0.5)) / n, x2 = -R + (2 * R * (j + 0.5)) / n;
      let p = 0; NET.forEach((u, k) => { if (u.w1 * x1 + u.w2 * x2 + u.b > 0) p |= 1 << k; });
      pats.add(p); if (netGrad(x1, x2, a).g < 1e-12) flat++;
    }
    return { regions: Math.abs(a - 1) < 1e-9 ? 1 : pats.size, flat: flat / (n * n) };
  }

  // Signal propagation: pre-activation RMS per layer in a random network of width 256.
  function initRun(a, g, depth) {
    const n = 256, r = rng(22), std = g / Math.sqrt(n);
    let h = Array.from({ length: n }, () => r.normal());
    const out = [];
    for (let l = 0; l < depth; l++) {
      const z = new Array(n);
      for (let i = 0; i < n; i++) { let s = 0; for (let j = 0; j < n; j++) s += r.normal() * std * h[j]; z[i] = s; }
      out.push(Math.sqrt(z.reduce((s, v) => s + v * v, 0) / n));
      h = z.map((v) => lrelu(v, a));
    }
    return out;
  }

  // PReLU: learn w and α of f(x) = PReLU_α(w x) on data from the teacher w* = 1.5, α* = 0.2.
  const PR = (() => {
    const r = rng(5), xs = [], ys = [], n = 31;
    for (let i = 0; i < n; i++) { const x = -3 + (6 * i) / (n - 1); xs.push(x); ys.push(lrelu(1.5 * x, 0.2) + 0.15 * r.normal()); }
    return { xs, ys, n, lr: 0.05 };
  })();
  function prLoss(w, a) { let l = 0; for (let i = 0; i < PR.n; i++) { const e = lrelu(w * PR.xs[i], a) - PR.ys[i]; l += e * e; } return l / PR.n; }
  function prStep(p) {
    let gw = 0, ga = 0;
    for (let i = 0; i < PR.n; i++) {
      const x = PR.xs[i], z = p.w * x, e = (2 * (lrelu(z, p.a) - PR.ys[i])) / PR.n;
      gw += e * x * dlrelu(z, p.a); ga += e * Math.min(0, z);
    }
    p.w -= PR.lr * gw; p.a -= PR.lr * ga;
    return Math.hypot(gw, ga);
  }
  function prRun(w, a, T) { const p = { w, a }; let t = 0; for (; t < T; t++) if (prStep(p) < 1e-6) break; return { w: p.w, a: p.a, loss: prLoss(p.w, p.a), steps: t + 1 }; }

  // Activation zoo
  const SELU_L = 1.0507009873554805, SELU_A = 1.6732632423543772;
  const ZOO = {
    elu: { f: (x) => (x > 0 ? x : Math.expm1(x)), d: (x) => (x > 0 ? 1 : Math.exp(x)), label: "ELU", jump: false },
    selu: { f: (x) => SELU_L * (x > 0 ? x : SELU_A * Math.expm1(x)), d: (x) => (x > 0 ? SELU_L : SELU_L * SELU_A * Math.exp(x)), label: "SELU", jump: true },
    gelu: { f: (x) => x * phiC(x), d: (x) => phiC(x) + x * Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI), label: "GELU" },
    silu: { f: (x) => x * sigm(x), d: (x) => { const s = sigm(x); return s * (1 + x * (1 - s)); }, label: "SiLU" },
  };
  function sigm(x) { return x >= 0 ? 1 / (1 + Math.exp(-x)) : Math.exp(x) / (1 + Math.exp(x)); }
  function phiC(x) { return typeof FV !== "undefined" && FV.Phi ? FV.Phi(x) : 0.5 * (1 + erf(x / Math.SQRT2)); }
  function erf(x) { const s = Math.sign(x), a = Math.abs(x), t = 1 / (1 + 0.3275911 * a); return s * (1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-a * a)); }

  if (typeof module === "object" && module.exports) module.exports = { revRun, revLoss, revInit, netStats, netF, netGrad, initRun, prRun, prLoss, PR, REV, ZOO };
  if (typeof FV === "undefined" || !FV.widget) return;

  const dec = (s) => (LANG === "en" ? s : s.replace(/(\d)\.(\d)/g, "$1,$2"));

  // 1. The function, the draggable point with its tangent, and the derivative with its jump.
  FV.widget("leaky-relu-explorer", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-4, 4], y: [-2, 4], xLabel: L.x, yLabel: L.f, aspect: 0.52 });
    const box = FV.h("div"); w.stage.append(box);
    let d = null;
    const sa = FV.ui.slider({ label: L.alpha, min: 0, max: 1, step: 0.01, value: cfg.alpha != null ? cfg.alpha : 0.1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const show = FV.ui.check({ label: L.deriv, checked: true, onchange: (v) => { box.hidden = !v; draw(); } });
    w.controls.append(sa.el, show.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "f", label: "LReLU(x) =", c: "blue" }, { key: "d", label: "LReLU′(x) =", c: "orange" }]);
    let x0 = cfg.x != null ? cfg.x : -2;
    const h = p.handle(x0, lrelu(x0, sa.value), { c: "blue", onDrag: (x) => { x0 = x; return [x, lrelu(x, sa.value)]; }, onChange: () => draw() });
    function draw() {
      const a = sa.value, f = (x) => lrelu(x, a);
      p.clear();
      p.fn((x) => Math.max(0, x), { c: "guide", w: 1.6, dash: "5 4" });
      p.fn((x) => x, { c: "faint", w: 1.2, dash: "2 4" });
      const k = Math.abs(x0) < 1e-9 ? NaN : dlrelu(x0, a), y0 = f(x0);
      p.fn(f, { c: "blue", w: 2.6 });
      if (Number.isFinite(k)) {
        // slope triangle: one step to the right, the rise equals the derivative
        const dx = x0 < 0 ? -1 : 1, xa = x0 + dx;
        p.line(Math.min(x0, xa), x0 < 0 ? f(xa) : y0, Math.max(x0, xa), x0 < 0 ? f(xa) : y0, { c: "orange", w: 1.6, dash: "3 3" });
        p.line(x0 < 0 ? x0 : xa, x0 < 0 ? f(xa) : y0, x0 < 0 ? x0 : xa, x0 < 0 ? y0 : f(xa), { c: "orange", w: 2.4 });
        p.text(x0 < 0 ? x0 + 0.08 : xa + 0.08, (f(xa) + y0) / 2 + 0.05, (x0 < 0 ? "α" : "1"), { c: "orange" });
        p.text((x0 + xa) / 2, (x0 < 0 ? f(xa) : y0) - 0.22, "1", { c: "orange", anchor: "middle" });
      }
      p.line(x0, 0, x0, y0, { c: "guide", w: 1, dash: "3 3" });
      p.dot(0, 0, { hollow: true, r: 4 });
      h.set(x0, y0);
      p.legend([{ label: "LReLU, α = " + FV.fmt(a, 2), c: "blue" }, { label: L.tangent, c: "orange" }, { label: "ReLU", c: "guide", dash: true }, { label: "y = x", c: "faint", dash: true }]);
      if (show.value) {
        if (!d) { d = new FV.Plot(box, { x: [-4, 4], y: [-0.12, 1.18], xLabel: L.x, yLabel: L.df, aspect: 0.26, minHeight: 150, maxHeight: 210 }); d.onresize = draw; }
        box.hidden = false;
        d.clear();
        d.rect(-4, 0, 0, a, { c: "orange", opacity: 0.1 }); d.rect(0, 0, 4, 1, { c: "orange", opacity: 0.1 });
        d.line(-4, a, 0, a, { c: "orange", w: 2.4 }); d.line(0, 1, 4, 1, { c: "orange", w: 2.4 });
        d.line(0, a, 0, 1, { c: "orange", w: 1, dash: "3 3" });
        d.dot(0, a, { c: "orange", hollow: true, r: 4 }); d.dot(0, 1, { c: "orange", hollow: true, r: 4 });
        if (Number.isFinite(k)) d.dot(x0, k, { c: "orange" });
        d.text(-3.9, a + 0.07, "α = " + FV.fmt(a, 2), { c: "orange" });
        d.text(3.9, 0.8, "1", { c: "orange", anchor: "end" });
        d.text(0.12, 0.5 * (a + 1), L.undef, { c: "faint", size: 12 });
      }
      ro.set("x", FV.fmt(x0, 2)); ro.set("f", FV.fmt(y0, 3)); ro.set("d", Number.isFinite(k) ? FV.fmt(k, 2) : "—");
    }
    p.onresize = draw; draw();
  });

  // 2. Two ways to build the same function: the upper envelope of two lines and "linear + |x|".
  FV.widget("leaky-relu-parts", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const opt = { x: [-3, 3], y: [-3, 3], xLabel: L.x, aspect: 0.8 };
    const p1 = new FV.Plot(FV.col(w.stage), Object.assign({ title: L.maxTitle }, opt));
    const p2 = new FV.Plot(FV.col(w.stage), Object.assign({ title: L.sumTitle }, opt));
    const sa = FV.ui.slider({ label: L.alpha, min: 0, max: 2, step: 0.01, value: cfg.alpha != null ? cfg.alpha : 0.2, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sa.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.same }, { key: "c", label: "(1 + α)/2 =", c: "teal" }, { key: "k", label: "(1 − α)/2 =", c: "violet" }]);
    function draw() {
      const a = sa.value;
      p1.clear();
      p1.fn((x) => x, { c: "teal", w: 1.4, dash: "5 4" }); p1.fn((x) => a * x, { c: "violet", w: 1.4, dash: "5 4" });
      p1.fn((x) => lrelu(x, a), { c: "blue", w: 3 });
      p1.fn((x) => Math.max(a * x, x), { c: "ink", w: 1.8, dash: "2 3" });
      p1.legend([{ label: L.lineX, c: "teal", dash: true }, { label: L.lineAx, c: "violet", dash: true }, { label: L.cases, c: "blue" }, { label: L.maxEnv, c: "ink", dash: true }]);
      p2.clear();
      p2.fn((x) => ((1 + a) / 2) * x, { c: "teal", w: 1.6, dash: "5 4" }); p2.fn((x) => ((1 - a) / 2) * Math.abs(x), { c: "violet", w: 1.6, dash: "5 4" });
      p2.fn((x) => lrelu(x, a), { c: "blue", w: 3 });
      p2.legend([{ label: L.linPart, c: "teal", dash: true }, { label: L.absPart, c: "violet", dash: true }, { label: L.sum, c: "blue" }]);
      ro.set("s", a <= 1 ? L.yes : L.no); ro.set("c", FV.fmt((1 + a) / 2, 3)); ro.set("k", FV.fmt((1 - a) / 2, 3));
    }
    p1.onresize = draw; p2.onresize = draw; draw();
  });

  // 3. A dead neuron: ReLU stays frozen, Leaky ReLU returns to the data thanks to the gradient α.
  FV.widget("leaky-relu-revive", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const T = 1500, PER = 10;
    const pf = new FV.Plot(FV.col(w.stage), { x: [-3.5, 5.5], y: [-1.2, 3.8], xLabel: L.x, yLabel: "y", aspect: 0.75, title: L.fitTitle });
    const pl = new FV.Plot(FV.col(w.stage), { x: [0, 1560], y: [1e-4, 10], yType: "log", xLabel: L.step, yLabel: L.loss, aspect: 0.75, title: L.lossTitle });
    const sa = FV.ui.seg({ label: "$\\alpha$", value: cfg.alpha != null ? cfg.alpha : 0.1, options: [0.01, 0.03, 0.1].map((v) => ({ value: v, label: FV.fmt(v, 2) })), onchange: () => reset() });
    let S, R, t, histL, histR, revived;
    const player = FV.ui.player({
      interval: 60,
      onstep() {
        for (let k = 0; k < PER && t < T; k++) {
          revStep(S, sa.value); revStep(R, 0); t++;
          if (revived < 0 && revActive(S) > 0) revived = t;
          histL.push(revLoss(S, sa.value)); histR.push(revLoss(R, 0));
        }
        draw();
        return t < T;
      },
      onreset: () => reset(),
    });
    w.controls.append(sa.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.step + " =" }, { key: "k", label: L.kink + " =", c: "blue" }, { key: "a", label: L.active + ":", c: "blue" },
      { key: "r", label: L.revived + ":" }, { key: "lr", label: L.lossR + " =" }, { key: "ll", label: L.lossL + " =", c: "blue" }]);
    function reset() { S = revInit(); R = revInit(); t = 0; revived = -1; histL = [revLoss(S, sa.value)]; histR = [revLoss(R, 0)]; draw(); }
    function draw() {
      const a = sa.value;
      pf.clear();
      pf.rect(-3, -1.2, 3, 3.8, { c: "teal", opacity: 0.06 });
      pf.text(2.9, -0.95, L.dataZone, { c: "teal", size: 12, anchor: "end" });
      REV.xs.forEach((x, i) => pf.dot(x, REV.ys[i], { c: "faint", r: 3 }));
      pf.fn((x) => R.v * lrelu(R.w * x + R.b, 0), { c: "ink", w: 2, dash: "6 4" });
      pf.fn((x) => S.v * lrelu(S.w * x + S.b, a), { c: "blue", w: 2.6 });
      const kr = -R.b / R.w, kl = -S.b / S.w;
      pf.dot(kr, 0, { c: "ink", hollow: true, r: 4 });
      if (kl > -3.5 && kl < 5.5) pf.dot(kl, 0, { c: "blue", hollow: true, r: 5 });
      pf.legend([{ label: L.data, c: "faint", dot: true }, { label: L.reluN, c: "ink", dash: true }, { label: L.leaky + ", α = " + FV.fmt(a, 2), c: "blue" }]);
      pl.clear();
      const pts = (hst) => hst.map((v, i) => [i, Math.max(v, 1e-4)]);
      if (revived > 0) { pl.vline(revived, { c: "teal" }); }
      pl.path(pts(histR), { c: "ink", w: 2, dash: "6 4" });
      pl.path(pts(histL), { c: "blue", w: 2.4 });
      pl.legend([{ label: L.reluN, c: "ink", dash: true }, { label: L.leaky, c: "blue" }, { label: L.revived, c: "teal", dash: true }]);
      ro.set("t", String(t)); ro.set("k", FV.fmt(kl, 2)); ro.set("a", revActive(S) + " / " + REV.n);
      ro.set("r", revived > 0 ? String(revived) : "—"); ro.set("lr", FV.num(revLoss(R, 0), 3)); ro.set("ll", FV.num(revLoss(S, a), 3));
    }
    pf.onresize = draw; pl.onresize = draw; reset();
  });

  // 4. A small Leaky network in 2D: a piecewise-linear surface and its kink lines.
  FV.widget("leaky-relu-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const RNG = 3;
    let a = cfg.alpha != null ? cfg.alpha : 0.1;
    const P = { x: cfg.x1 != null ? cfg.x1 : 0.2, y: cfg.x2 != null ? cfg.x2 : -0.3 };
    const f = (x1, x2) => netF(x1, x2, a);
    const s3 = new FV.Surface(FV.col(w.stage), { f, x: [-RNG, RNG], y: [-RNG, RNG], n: 48, labels: { x: L.x1, y: L.x2, z: "f" }, azimuth: -0.9, elevation: 0.62, aspect: 0.85, cmap: "viridis", title: "f = Σ vₖ·LReLU(wₖ·x + bₖ)" });
    const top = new FV.Plot(FV.col(w.stage), { x: [-RNG, RNG], y: [-RNG, RNG], xLabel: L.x1, yLabel: L.x2, equal: true, title: L.top });
    const sa = FV.ui.slider({ label: L.alpha, min: 0, max: 1, step: 0.01, value: a, fmt: (v) => FV.fmt(v, 2), oninput: (v) => { a = v; stats = netStats(a, RNG); draw(); } });
    w.controls.append(sa.el);
    const ro = FV.ui.readout(w.readout, [{ key: "f", label: "f =", c: "blue" }, { key: "g", label: L.grad + " =", c: "orange" }, { key: "on", label: L.activeU + ":" },
      { key: "r", label: L.regions + ":" }, { key: "z", label: L.flat + ":" }]);
    let stats = netStats(a, RNG);
    const hd = top.handle(P.x, P.y, { c: "orange", onChange: (x, y) => { P.x = x; P.y = y; draw(); } });
    function draw() {
      s3.f = f; s3.sample();
      s3.setPoints([{ x: P.x, y: P.y, z: f(P.x, P.y), c: "orange", r: 5 }]);
      top.clear();
      top.heat(f, { cmap: "viridis", res: 4, alpha: 0.85, z: [s3.zr[0], s3.zr[1]] });
      NET.forEach((u) => {
        // the line w1·x1 + w2·x2 + b = 0, drawn across the square
        if (Math.abs(u.w2) > Math.abs(u.w1)) top.line(-RNG, (-u.b + u.w1 * RNG) / u.w2, RNG, (-u.b - u.w1 * RNG) / u.w2, { c: "ink", w: 1.3, opacity: 0.75 });
        else top.line((-u.b + u.w2 * RNG) / u.w1, -RNG, (-u.b - u.w2 * RNG) / u.w1, RNG, { c: "ink", w: 1.3, opacity: 0.75 });
      });
      top.text(-RNG + 0.1, RNG - 0.25, L.x2, { c: "ink" });
      hd.set(P.x, P.y);
      const g = netGrad(P.x, P.y, a);
      ro.set("f", FV.fmt(f(P.x, P.y), 3)); ro.set("g", FV.fmt(g.g, 3)); ro.set("on", g.on + " / " + NET.length);
      ro.set("r", String(stats.regions)); ro.set("z", Math.round(stats.flat * 100) + "%");
    }
    top.onresize = draw; draw();
  });

  // 5. Signal propagation through depth: the variance factor g²(1 + α²)/2 per layer.
  FV.widget("leaky-relu-init", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0.3, 50.7], y: [1e-6, 1e6], yType: "log", xLabel: L.layer, yLabel: L.rms, aspect: 0.45 });
    const sa = FV.ui.slider({ label: L.alpha, min: 0, max: 1, step: 0.05, value: cfg.alpha != null ? cfg.alpha : 0.3, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sd = FV.ui.slider({ label: L.depth, min: 5, max: 50, step: 1, value: cfg.depth || 50, fmt: (v) => String(v), oninput: draw });
    const gs = FV.ui.seg({ label: L.gain, value: cfg.gain || "relu", options: [{ value: "one", label: L.xavier }, { value: "relu", label: L.heRelu }, { value: "leaky", label: L.heLeaky }], onchange: draw });
    w.controls.append(gs.el, sa.el, sd.el);
    const ro = FV.ui.readout(w.readout, [{ key: "g", label: "g =" }, { key: "f", label: L.perLayer + " =", c: "orange" }, { key: "t", label: L.last + ", " + L.theory + " =" }, { key: "m", label: L.measured + " =", c: "blue" }]);
    const cache = {};
    function gain(a) { return gs.value === "one" ? 1 : gs.value === "relu" ? Math.SQRT2 : Math.sqrt(2 / (1 + a * a)); }
    function draw() {
      const a = sa.value, L_ = sd.value, g = gain(a), key = a.toFixed(2) + gs.value;
      const rms = cache[key] || (cache[key] = initRun(a, g, 50));
      const fac = (g * g * (1 + a * a)) / 2, th = (l) => g * Math.pow(fac, (l - 1) / 2);
      p.setDomain([0.3, L_ + 0.7]);
      p.clear();
      p.hline(1, { c: "guide" });
      for (let l = 1; l <= L_; l++) p.rect(l - 0.35, 1e-6, l + 0.35, FV.clamp(rms[l - 1], 1e-6, 1e6), { c: "blue", opacity: 0.8 });
      p.fn(th, { c: "orange", w: 2, dash: true, from: 1, to: L_ });
      p.legend([{ label: L.rms + ", " + L.measured, c: "blue", box: true }, { label: L.theory, c: "orange", dash: true }]);
      ro.set("g", FV.fmt(g, 3)); ro.set("f", FV.fmt(fac, 3)); ro.set("t", FV.num(th(L_), 3)); ro.set("m", FV.num(rms[L_ - 1], 3));
    }
    p.onresize = draw; draw();
  });

  // 6. PReLU: α is a weight too. Gradient descent on (w, α) over the error landscape.
  FV.widget("leaky-relu-prelu", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const pf = new FV.Plot(FV.col(w.stage), { x: [-3.2, 3.2], y: [-2.5, 5], xLabel: L.x, yLabel: "y", aspect: 0.8, title: "PReLU_α(w·x)" });
    const pm = new FV.Plot(FV.col(w.stage), { x: [-1, 3], y: [-0.6, 1.6], xLabel: L.w, aspect: 0.8, title: L.landscape });
    const start = { w: cfg.w != null ? cfg.w : 0.5, a: cfg.a != null ? cfg.a : 1.3 };
    let P, path, t;
    const player = FV.ui.player({
      interval: 50,
      onstep() { let g = 1; for (let k = 0; k < 3; k++) { g = prStep(P); t++; path.push([P.w, P.a]); } draw(); return t < 600 && g > 1e-5; },
      onreset: () => reset(),
    });
    w.controls.append(player.el);
    w.note.append(FV.rich(L.dragHint));
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.step + " =" }, { key: "w", label: "w =", c: "blue" }, { key: "a", label: "α =", c: "blue" }, { key: "l", label: "L =", c: "orange" }]);
    const hd = pm.handle(start.w, start.a, { c: "orange", onChange: (x, y) => { start.w = x; start.a = y; player.stop(); reset(); } });
    function reset() { P = { w: start.w, a: start.a }; path = [[P.w, P.a]]; t = 0; draw(); }
    const lg = (x, y) => Math.log10(prLoss(x, y));
    function draw() {
      pf.clear();
      PR.xs.forEach((x, i) => pf.dot(x, PR.ys[i], { c: "faint", r: 3.5 }));
      pf.fn((x) => lrelu(1.5 * x, 0.2), { c: "teal", w: 1.4, dash: "5 4" });
      pf.fn((x) => lrelu(P.w * x, P.a), { c: "blue", w: 2.6 });
      pf.legend([{ label: L.data, c: "faint", dot: true }, { label: L.teacher, c: "teal", dash: true }, { label: L.fit, c: "blue" }]);
      pm.clear();
      pm.heat(lg, { cmap: "blues", res: 4, alpha: 0.9, transform: (v) => -v });
      pm.contours(lg, [-1.5, -1, -0.5, 0, 0.5, 1], { style: () => ({ c: "ink", w: 1, opacity: 0.35 }) });
      pm.text(-0.93, 1.47, "α", { c: "ink" });
      pm.path(path, { c: "ink", w: 2 });
      pm.dot(1.5, 0.2, { c: "teal", hollow: true, r: 6 });
      pm.dot(P.w, P.a, { c: "blue", r: 5 });
      hd.set(start.w, start.a);
      pm.legend([{ label: L.path, c: "ink" }, { label: L.start, c: "orange", dot: true }, { label: L.teacher, c: "teal", dot: true }]);
      ro.set("t", String(t)); ro.set("w", FV.fmt(P.w, 3)); ro.set("a", FV.fmt(P.a, 3)); ro.set("l", FV.fmt(prLoss(P.w, P.a), 4));
    }
    pf.onresize = draw; pm.onresize = draw; reset();
  });

  // 7. The family: Leaky ReLU next to ELU, SELU, GELU and SiLU, as functions and as derivatives.
  FV.widget("leaky-relu-zoo", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-4, 3], y: [-2, 3], xLabel: L.x, yLabel: "f(x)", aspect: 0.52 });
    const view = FV.ui.seg({ label: L.view, value: cfg.view || "f", options: [{ value: "f", label: L.fun }, { value: "d", label: L.der }], onchange: draw });
    const cmp = FV.ui.seg({ label: L.cmp, value: cfg.cmp || "elu", options: Object.keys(ZOO).map((k) => ({ value: k, label: ZOO[k].label })), onchange: draw });
    const a = cfg.alpha != null ? cfg.alpha : 0.1;
    w.controls.append(view.el, cmp.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "l", label: "Leaky:", c: "blue" }, { key: "c", label: "ELU:", c: "teal" }, { key: "r", label: "ReLU:" }]);
    let hx = cfg.x != null ? cfg.x : -2;
    p.hover((x) => { if (x != null) { hx = x; mark(); } });
    function vals(x) {
      const z = ZOO[cmp.value], d = view.value === "d";
      return { l: d ? dlrelu(x, a) : lrelu(x, a), c: d ? z.d(x) : z.f(x), r: d ? (x > 0 ? 1 : 0) : Math.max(0, x) };
    }
    function mark() {
      const v = vals(hx);
      p.hl("line", hx, p.o.y[0], hx, p.o.y[1], { c: "guide", w: 1, dash: "3 3" });
      p.hl("dot", hx, v.l, { c: view.value === "d" ? "orange" : "blue", r: 4 }); p.hl("dot", hx, v.c, { c: "teal", r: 4 });
      ro.set("x", FV.fmt(hx, 2)); ro.set("l", FV.fmt(v.l, 3)); ro.set("c", FV.fmt(v.c, 3)); ro.set("r", FV.fmt(v.r, 3));
    }
    function draw() {
      const z = ZOO[cmp.value], d = view.value === "d";
      p.setDomain(null, d ? [-0.25, 1.95] : [-2, 3]);
      p.o.yLabel = d ? "f′(x)" : "f(x)";
      p.clear();
      const main = d ? "orange" : "blue";
      if (d) {
        p.line(-4, 0, 0, 0, { c: "guide", w: 1.6, dash: "5 4" }); p.line(0, 1, 3, 1, { c: "guide", w: 1.6, dash: "5 4" });
        p.fn(z.d, { c: "teal", w: 2.2, jump: 0.3 });
        p.line(-4, a, 0, a, { c: main, w: 2.6 }); p.line(0, 1, 3, 1, { c: main, w: 2.6 });
        p.dot(0, a, { c: main, hollow: true, r: 4 }); p.dot(0, 1, { c: main, hollow: true, r: 4 });
      } else {
        p.fn((x) => Math.max(0, x), { c: "guide", w: 1.6, dash: "5 4" });
        p.fn(z.f, { c: "teal", w: 2.2 });
        p.fn((x) => lrelu(x, a), { c: main, w: 2.6 });
      }
      p.legend([{ label: "Leaky ReLU, α = " + FV.fmt(a, 2), c: main }, { label: z.label, c: "teal" }, { label: "ReLU", c: "guide", dash: true }]);
      // relabel the comparison read-out
      const lab = w.readout.querySelectorAll(".fv-ro")[2];
      if (lab && lab.firstChild) lab.firstChild.textContent = z.label + ":";
      mark();
    }
    p.onresize = draw; draw();
  });
})();
