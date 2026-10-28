/* Widgets of the formula page "GELU". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      x: "x", gelu: "GELU(x)", phiKeep: "Φ(x) — доля, которую пропускаем", ident: "y = x (вход целиком)", deriv: "Показать производную",
      dgelu: "GELU′(x)", min: "минимум", kept: "пропущено", relu: "ReLU", silu: "SiLU = x·σ(x)",
      samples: "масок на точку", empir: "доля m = 1 при x₀", maxdev: "макс. отклонение", mc: "среднее x·m по маскам", mcTitle: "среднее по n случайным маскам", noise: "шум ε ~ N(0, 1)",
      keepArea: "m = 1, если ε ≤ x₀", x0: "Точка $x_0$", diffRelu: "ReLU − GELU", diffSilu: "ReLU − SiLU", hover: "Наведите на график",
      comp1: "Φ(x)", comp2: "x·φ(x)", stepRelu: "ReLU′(x)", second: "Показать вторую производную", d2: "GELU″(x)",
      exact: "точная x·Φ(x)", tanhA: "tanh-приближение", sigA: "x·σ(1,702x)", err: "|ошибка|", coef: "Коэффициент $c$", maxErr: "макс. ошибка tanh на [−6; 6]",
      s: "Уровень шума $s$", fx: "x·Φ(x/s)", dfx: "∂/∂x", mode: "Поверхность", fn: "функция", der: "производная", slice: "срез при текущем s", minLine: "линия минимумов",
      half: "x/2 (s → ∞)", minAt: "минимум в x =", minVal: "значение минимума", steps: "шаг", lossG: "MSE GELU", lossR: "MSE ReLU", data: "данные",
      fitG: "сеть с GELU", fitR: "сеть с ReLU", units: "Нейроны", none: "скрыть", loss: "MSE (лог. шкала)", step: "шаг обучения",
    },
    en: {
      x: "x", gelu: "GELU(x)", phiKeep: "Φ(x) — the share we let through", ident: "y = x (the whole input)", deriv: "Show the derivative",
      dgelu: "GELU′(x)", min: "minimum", kept: "let through", relu: "ReLU", silu: "SiLU = x·σ(x)",
      samples: "samples per point", empir: "share of m = 1 at x₀", maxdev: "max deviation", mc: "mean of x·m over samples", mcTitle: "mean over n random masks", noise: "noise ε ~ N(0, 1)",
      keepArea: "m = 1 if ε ≤ x₀", x0: "Point $x_0$", diffRelu: "ReLU − GELU", diffSilu: "ReLU − SiLU", hover: "Hover over the plot",
      comp1: "Φ(x)", comp2: "x·φ(x)", stepRelu: "ReLU′(x)", second: "Show the second derivative", d2: "GELU″(x)",
      exact: "exact x·Φ(x)", tanhA: "tanh approximation", sigA: "x·σ(1.702x)", err: "|error|", coef: "Coefficient $c$", maxErr: "max tanh error on [−6, 6]",
      s: "Noise level $s$", fx: "x·Φ(x/s)", dfx: "∂/∂x", mode: "Surface", fn: "function", der: "derivative", slice: "slice at the current s", minLine: "line of minima",
      half: "x/2 (s → ∞)", minAt: "minimum at x =", minVal: "minimum value", steps: "step", lossG: "MSE GELU", lossR: "MSE ReLU", data: "data",
      fitG: "network with GELU", fitR: "network with ReLU", units: "Neurons", none: "hide", loss: "MSE (log scale)", step: "training step",
    },
    uz: {
      x: "x", gelu: "GELU(x)", phiKeep: "Φ(x) — o‘tkaziladigan ulush", ident: "y = x (kirish to‘liq)", deriv: "Hosilani ko‘rsatish",
      dgelu: "GELU′(x)", min: "minimum", kept: "o‘tkazildi", relu: "ReLU", silu: "SiLU = x·σ(x)",
      samples: "har nuqtaga namunalar", empir: "x₀ da m = 1 ulushi", maxdev: "maks. chetlanish", mc: "namunalar bo‘yicha x·m o‘rtachasi", mcTitle: "n ta tasodifiy niqob bo‘yicha o‘rtacha", noise: "shovqin ε ~ N(0, 1)",
      keepArea: "ε ≤ x₀ bo‘lsa, m = 1", x0: "$x_0$ nuqta", diffRelu: "ReLU − GELU", diffSilu: "ReLU − SiLU", hover: "Grafik ustiga olib boring",
      comp1: "Φ(x)", comp2: "x·φ(x)", stepRelu: "ReLU′(x)", second: "Ikkinchi hosilani ko‘rsatish", d2: "GELU″(x)",
      exact: "aniq x·Φ(x)", tanhA: "tanh yaqinlashishi", sigA: "x·σ(1,702x)", err: "|xato|", coef: "$c$ koeffitsiyent", maxErr: "[−6; 6] da tanh maks. xatosi",
      s: "Shovqin darajasi $s$", fx: "x·Φ(x/s)", dfx: "∂/∂x", mode: "Sirt", fn: "funksiya", der: "hosila", slice: "joriy s dagi kesim", minLine: "minimumlar chizig‘i",
      half: "x/2 (s → ∞)", minAt: "minimum x =", minVal: "minimum qiymati", steps: "qadam", lossG: "MSE GELU", lossR: "MSE ReLU", data: "ma’lumotlar",
      fitG: "GELU’li tarmoq", fitR: "ReLU’li tarmoq", units: "Neyronlar", none: "yashirish", loss: "MSE (log. shkala)", step: "o‘qitish qadami",
    },
  }[FV.lang] || {};
  const dec = (s) => (FV.lang === "en" ? s : s.replace(/(\d)\.(\d)/g, "$1,$2"));

  /* sim:begin — pure maths, also used by the numeric checks of the page text */
  // erf to ~1e-15: Maclaurin series for |x| < 2.5, continued fraction for erfc beyond.
  const SQRTPI = Math.sqrt(Math.PI);
  function erf(x) {
    const a = Math.abs(x);
    if (a < 2.5) {
      const x2 = x * x;
      let term = x, s = x;
      for (let n = 1; n <= 80; n++) { term *= -x2 / n; const add = term / (2 * n + 1); s += add; if (Math.abs(add) <= 1e-17 * Math.abs(s)) break; }
      return (2 / SQRTPI) * s;
    }
    let f = a;
    for (let k = 60; k >= 1; k--) f = a + k / 2 / f;
    const c = Math.exp(-a * a) / SQRTPI / f;
    return x < 0 ? c - 1 : 1 - c;
  }
  const Phi = (x) => 0.5 * (1 + erf(x / Math.SQRT2));
  const phi = (x) => Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI);
  const gelu = (x) => x * Phi(x);
  const dgelu = (x) => Phi(x) + x * phi(x);
  const d2gelu = (x) => phi(x) * (2 - x * x);
  const sig = (x) => (x >= 0 ? 1 / (1 + Math.exp(-x)) : Math.exp(x) / (1 + Math.exp(x)));
  const silu = (x) => x * sig(x);
  const relu = (x) => (x > 0 ? x : 0);
  const gTanh = (x, c) => 0.5 * x * (1 + Math.tanh(Math.sqrt(2 / Math.PI) * (x + c * x * x * x)));
  const gSig = (x) => x * sig(1.702 * x);
  const XMIN = -0.7517915246935645, GMIN = -0.16997120747990369;

  // Monte Carlo of the stochastic mask: m = 1 if ε ≤ x, ε ~ N(0, 1).
  function maskSim(seed) {
    const xs = [];
    for (let i = 0; i <= 24; i++) xs.push(-3 + i * 0.25);
    const r = FV.rng(seed), k = new Array(xs.length).fill(0);
    const S = { xs, k, n: 0 };
    S.add = (B) => { for (let i = 0; i < xs.length; i++) for (let b = 0; b < B; b++) if (r.normal() <= xs[i]) k[i]++; S.n += B; };
    S.maxDev = () => xs.reduce((m, x, i) => Math.max(m, Math.abs((x * k[i]) / S.n - gelu(x))), 0);
    return S;
  }

  // A 1 → H → 1 network trained by full-batch Adam on a fixed noisy curve.
  function trainData() {
    const r = FV.rng(5), n = 40, X = [], Y = [];
    for (let i = 0; i < n; i++) { const x = -3 + (6 * i) / (n - 1); X.push(x); Y.push(Math.sin(1.5 * x) + 0.3 * x + 0.08 * r.normal()); }
    return { X, Y };
  }
  const ACT = { gelu: [gelu, dgelu], relu: [relu, (z) => (z > 0 ? 1 : 0)] };
  function mlp(kind, H, lr) {
    const r = FV.rng(21), f = ACT[kind][0], df = ACT[kind][1];
    const P = { w1: [], b1: [], w2: [], b2: 0 };
    for (let j = 0; j < H; j++) { P.w1.push(r.normal() * 1.5); P.b1.push(r.normal() * 1.5); P.w2.push(r.normal() / Math.sqrt(H)); }
    const zeros = () => new Array(H).fill(0);
    const m = { w1: zeros(), b1: zeros(), w2: zeros(), b2: 0 }, v = { w1: zeros(), b1: zeros(), w2: zeros(), b2: 0 };
    let t = 0;
    const unit = (j, x) => P.w2[j] * f(P.w1[j] * x + P.b1[j]);
    const pred = (x) => { let s = P.b2; for (let j = 0; j < H; j++) s += unit(j, x); return s; };
    function step(X, Y) {
      const n = X.length, g = { w1: zeros(), b1: zeros(), w2: zeros(), b2: 0 };
      let loss = 0;
      for (let i = 0; i < n; i++) {
        const z = P.w1.map((w, j) => w * X[i] + P.b1[j]);
        let yh = P.b2;
        for (let j = 0; j < H; j++) yh += P.w2[j] * f(z[j]);
        const e = yh - Y[i];
        loss += e * e;
        const ge = (2 * e) / n;
        g.b2 += ge;
        for (let j = 0; j < H; j++) { g.w2[j] += ge * f(z[j]); const gz = ge * P.w2[j] * df(z[j]); g.w1[j] += gz * X[i]; g.b1[j] += gz; }
      }
      t++;
      const b1 = 0.9, b2 = 0.999, c1 = 1 - Math.pow(b1, t), c2 = 1 - Math.pow(b2, t);
      const up = (k, j) => {
        const gv = j == null ? g[k] : g[k][j];
        const mm = b1 * (j == null ? m[k] : m[k][j]) + (1 - b1) * gv, vv = b2 * (j == null ? v[k] : v[k][j]) + (1 - b2) * gv * gv;
        const d = (lr * (mm / c1)) / (Math.sqrt(vv / c2) + 1e-8);
        if (j == null) { m[k] = mm; v[k] = vv; P[k] -= d; } else { m[k][j] = mm; v[k][j] = vv; P[k][j] -= d; }
      };
      for (const k of ["w1", "b1", "w2"]) for (let j = 0; j < H; j++) up(k, j);
      up("b2");
      return loss / n;
    }
    const mse = (X, Y) => X.reduce((s, x, i) => s + (pred(x) - Y[i]) ** 2, 0) / X.length;
    return { P, H, step, pred, unit, mse };
  }
  /* sim:end */

  // 1. GELU = x · Φ(x): the input times the probability of letting it through.
  FV.widget("gelu-explorer", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-3, 3], y: [-1, 3], xLabel: L.x, yLabel: L.gelu, aspect: 0.55 });
    const box = FV.h("div"); w.stage.append(box);
    let d = null;
    const show = FV.ui.check({ label: L.deriv, checked: cfg.derivative !== false, onchange: () => draw() });
    w.controls.append(show.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "p", label: "Φ(x) =", c: "teal" }, { key: "g", label: "GELU(x) =", c: "blue" }, { key: "d", label: "GELU′(x) =", c: "orange" }]);
    let x0 = cfg.x != null ? cfg.x : 1;
    const h = p.handle(x0, gelu(x0), { c: "blue", onDrag: (x) => { x0 = x; return [x, gelu(x)]; }, onChange: () => draw() });
    function draw() {
      const g = gelu(x0), P = Phi(x0);
      p.clear();
      p.fn((x) => x, { c: "guide", w: 1.4, dash: "5 4" });
      p.fn(Phi, { c: "teal", w: 1.8, dash: "6 4" });
      p.line(x0, 0, x0, x0, { c: "guide", w: 7, opacity: 0.35 });
      p.line(x0, 0, x0, g, { c: "blue", w: 7, opacity: 0.45 });
      p.fn(gelu, { c: "blue", w: 2.6 });
      p.dot(x0, x0, { c: "guide", r: 4 });
      p.dot(XMIN, GMIN, { hollow: true, r: 4, c: "ink" });
      p.text(XMIN, GMIN - 0.22, L.min, { anchor: "middle", c: "faint" });
      const lab = "× Φ = " + FV.fmt(P, 2), right = x0 > 1.6;
      p.text(x0 + (right ? -0.14 : 0.14), x0 > 0 ? g / 2 : Math.max(-0.85, x0 / 2), lab, { anchor: right ? "end" : "start", c: "blue" });
      h.set(x0, g);
      box.hidden = !show.value;
      if (show.value) {
        if (!d) { d = new FV.Plot(box, { x: [-3, 3], y: [-0.3, 1.25], xLabel: L.x, yLabel: L.dgelu, aspect: 0.28, minHeight: 170, maxHeight: 230 }); d.onresize = draw; }
        d.clear();
        d.hline(1, { c: "guide" });
        d.fn(dgelu, { c: "orange", w: 2.2 });
        d.line(x0, 0, x0, dgelu(x0), { c: "orange", w: 1, dash: "3 3" });
        d.dot(x0, dgelu(x0), { c: "orange" });
      }
      ro.set("x", FV.fmt(x0, 2)); ro.set("p", FV.fmt(P, 4)); ro.set("g", FV.fmt(g, 4)); ro.set("d", FV.fmt(dgelu(x0), 4));
      p.legend([{ label: L.gelu, c: "blue" }, { label: L.phiKeep, c: "teal", dash: true }, { label: L.ident, c: "guide", dash: true }]);
    }
    p.onresize = draw; draw();
  });

  // 2. The stochastic view: multiply x by a random mask m ~ Bernoulli(Φ(x)) and average.
  FV.widget("gelu-mask", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-3, 3], y: [-1, 3.2], xLabel: L.x, yLabel: "E[x·m]", aspect: 0.8, title: L.mcTitle });
    const b = new FV.Plot(FV.col(w.stage), { x: [-3.5, 3.5], y: [0, 0.45], xLabel: "ε", yLabel: "φ(ε)", aspect: 0.8, title: L.noise });
    const B = 20, MAX = 2000, seed = cfg.seed || 3;
    let S;
    const sx = FV.ui.slider({ label: L.x0, min: -3, max: 3, step: 0.25, value: cfg.x != null ? cfg.x : 0.5, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const player = FV.ui.player({
      interval: 70,
      onstep() { if (S.n >= MAX) return false; S.add(B); draw(); return S.n < MAX; },
      onreset() { reset(); draw(); },
    });
    w.controls.append(sx.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "n", label: L.samples + " =" }, { key: "e", label: L.empir + " =", c: "orange" }, { key: "p", label: "Φ(x₀) =", c: "teal" }, { key: "m", label: L.maxdev + " =" }]);
    function reset() { S = maskSim(seed); S.add(B); }
    function draw() {
      const x0 = sx.value, i0 = Math.round((x0 + 3) / 0.25);
      a.clear();
      a.fn(relu, { c: "guide", w: 1.4, dash: "5 4" });
      a.fn(gelu, { c: "blue", w: 2.4 });
      S.xs.forEach((x, i) => a.dot(x, (x * S.k[i]) / S.n, { c: "orange", r: i === i0 ? 6 : 4 }));
      a.vline(x0, { c: "faint" });
      a.legend([{ label: L.gelu, c: "blue" }, { label: L.mc, c: "orange", dot: true }, { label: L.relu, c: "guide", dash: true }]);
      b.clear();
      b.area(phi, null, { c: "teal", fillOpacity: 0.28, to: x0 });
      b.fn(phi, { c: "ink", w: 2 });
      b.line(x0, 0, x0, 0.45, { c: "teal", w: 1.6 });
      b.text(x0 + (x0 > 1.5 ? -0.15 : 0.15), 0.42, "x₀", { c: "teal", anchor: x0 > 1.5 ? "end" : "start" });
      b.text(x0 - 0.15, Math.max(0.03, phi(x0) * 0.35), "Φ(x₀) = " + FV.fmt(Phi(x0), 3), { anchor: "end", c: "ink" });
      b.legend([{ label: L.keepArea, c: "teal", box: true }]);
      ro.set("n", String(S.n)); ro.set("e", FV.fmt(S.k[i0] / S.n, 3)); ro.set("p", FV.fmt(Phi(x0), 3)); ro.set("m", FV.fmt(S.maxDev(), 4));
    }
    a.onresize = draw; b.onresize = draw;
    reset(); draw();
  });

  // 3. GELU, SiLU and ReLU; both smooth curves equal ReLU minus an even bump.
  FV.widget("gelu-family", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-4, 4], y: [-0.45, 2.2], xLabel: L.x, yLabel: "f(x)", aspect: 0.5 });
    const q = new FV.Plot(w.stage, { x: [-4, 4], y: [0, 0.33], xLabel: L.x, yLabel: "ReLU − f", aspect: 0.28, minHeight: 170, maxHeight: 230 });
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "g", label: "GELU =", c: "blue" }, { key: "s", label: "SiLU =", c: "teal" }, { key: "r", label: "ReLU =" }]);
    let hx = cfg.x != null ? cfg.x : -1;
    const XS = -1.2784645427610738, SMIN = -0.2784645427610738;
    function draw() {
      p.clear();
      p.fn(relu, { c: "guide", w: 1.6, dash: "5 4" });
      p.fn(silu, { c: "teal", w: 2.2 });
      p.fn(gelu, { c: "blue", w: 2.6 });
      p.vline(hx, { c: "faint" });
      p.dot(hx, gelu(hx), { c: "blue", r: 5 }); p.dot(hx, silu(hx), { c: "teal", r: 5 });
      p.legend([{ label: "GELU = x·Φ(x)", c: "blue" }, { label: L.silu, c: "teal" }, { label: L.relu, c: "guide", dash: true }]);
      q.clear();
      q.fn((x) => relu(x) - silu(x), { c: "teal", w: 2.2 });
      q.fn((x) => relu(x) - gelu(x), { c: "blue", w: 2.4 });
      [-1, 1].forEach((s) => { q.dot(s * -XMIN, -GMIN, { c: "blue", r: 4 }); q.dot(s * -XS, -SMIN, { c: "teal", r: 4 }); });
      q.text(-XMIN + 0.12, -GMIN + 0.02, dec("0.170"), { c: "blue" }); q.text(-XS + 0.12, -SMIN + 0.01, dec("0.278"), { c: "teal" });
      q.vline(hx, { c: "faint" });
      q.legend([{ label: L.diffRelu, c: "blue" }, { label: L.diffSilu, c: "teal" }]);
      ro.set("x", FV.fmt(hx, 2)); ro.set("g", FV.fmt(gelu(hx), 3)); ro.set("s", FV.fmt(silu(hx), 3)); ro.set("r", FV.fmt(relu(hx), 3));
    }
    const mv = (x) => { if (x != null) { hx = FV.clamp(x, -4, 4); draw(); } };
    p.hover(mv); q.hover(mv);
    p.onresize = draw; q.onresize = draw; draw();
  });

  // 4. The derivative Φ(x) + x·φ(x) and its two parts.
  FV.widget("gelu-derivative", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-4, 4], y: [-0.45, 1.35], xLabel: L.x, yLabel: L.dgelu, aspect: 0.5 });
    const box = FV.h("div"); w.stage.append(box);
    let d = null;
    const sx = FV.ui.slider({ label: "x", min: -4, max: 4, step: 0.01, value: cfg.x != null ? cfg.x : -0.75, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sec = FV.ui.check({ label: L.second, checked: !!cfg.second, onchange: () => draw() });
    w.controls.append(sx.el, sec.el);
    const ro = FV.ui.readout(w.readout, [{ key: "a", label: "Φ(x) =", c: "blue" }, { key: "b", label: "x·φ(x) =", c: "teal" }, { key: "d", label: "GELU′(x) =", c: "orange" }, { key: "s", label: "GELU″(x) =" }]);
    const R2 = Math.SQRT2;
    function draw() {
      const x = sx.value;
      p.clear();
      p.hline(1, { c: "guide" });
      p.line(-4, 0, 0, 0, { c: "guide", w: 2, dash: "5 4" }); p.line(0, 1, 4, 1, { c: "guide", w: 2, dash: "5 4" });
      p.fn(Phi, { c: "blue", w: 1.8, dash: "6 4" });
      p.fn((t) => t * phi(t), { c: "teal", w: 1.8, dash: "6 4" });
      p.fn(dgelu, { c: "orange", w: 2.6 });
      p.dot(R2, dgelu(R2), { hollow: true, c: "orange", r: 4 }); p.dot(-R2, dgelu(-R2), { hollow: true, c: "orange", r: 4 });
      p.text(R2, dgelu(R2) + 0.09, dec("1.129"), { anchor: "middle", c: "orange" });
      p.text(-R2 - 0.15, dgelu(-R2) - 0.17, dec("−0.129"), { anchor: "middle", c: "orange" });
      p.dot(XMIN, 0, { hollow: true, c: "ink", r: 4 });
      p.line(x, 0, x, dgelu(x), { c: "orange", w: 1, dash: "3 3" });
      p.dot(x, Phi(x), { c: "blue", r: 4 }); p.dot(x, x * phi(x), { c: "teal", r: 4 }); p.dot(x, dgelu(x), { c: "orange" });
      p.legend([{ label: "GELU′ = Φ + x·φ", c: "orange" }, { label: L.comp1, c: "blue", dash: true }, { label: L.comp2, c: "teal", dash: true }, { label: L.stepRelu, c: "guide", dash: true }]);
      box.hidden = !sec.value;
      if (sec.value) {
        if (!d) { d = new FV.Plot(box, { x: [-4, 4], y: [-0.25, 0.9], xLabel: L.x, yLabel: L.d2, aspect: 0.26, minHeight: 160, maxHeight: 220 }); d.onresize = draw; }
        d.clear();
        d.vline(R2, { c: "faint" }); d.vline(-R2, { c: "faint" });
        d.fn(d2gelu, { c: "violet", w: 2.2 });
        d.dot(x, d2gelu(x), { c: "violet" });
        d.text(R2 + 0.1, 0.75, "√2", { c: "faint" }); d.text(-R2 + 0.1, 0.75, "−√2", { c: "faint" });
      }
      ro.set("a", FV.fmt(Phi(x), 4)); ro.set("b", FV.fmt(x * phi(x), 4)); ro.set("d", FV.fmt(dgelu(x), 4)); ro.set("s", FV.fmt(d2gelu(x), 4));
    }
    p.onresize = draw; draw();
  });

  // 5. The tanh and sigmoid approximations and their errors.
  FV.widget("gelu-approx", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-4, 1.5], y: [-0.25, 1.25], xLabel: L.x, yLabel: "y", aspect: 0.45 });
    const q = new FV.Plot(w.stage, { x: [-6, 6], y: [1e-8, 0.1], yType: "log", xLabel: L.x, yLabel: L.err, aspect: 0.32, minHeight: 190, maxHeight: 260 });
    const sc = FV.ui.slider({ label: L.coef, min: 0, max: 0.1, step: 0.000005, value: cfg.c != null ? cfg.c : 0.044715, fmt: (v) => FV.fmt(v, 6), oninput: draw });
    const sx = FV.ui.slider({ label: "x", min: -4, max: 3, step: 0.01, value: cfg.x != null ? cfg.x : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const dflt = FV.ui.button({ label: "c = " + dec("0.044715"), onclick: () => { sc.set(0.044715); draw(); } });
    w.controls.append(sc.el, sx.el, dflt.el);
    const ro = FV.ui.readout(w.readout, [{ key: "g", label: "x·Φ(x) =" }, { key: "t", label: "tanh =", c: "blue" }, { key: "s", label: "σ =", c: "teal" }, { key: "m", label: L.maxErr + " =", c: "blue" }]);
    function draw() {
      const c = sc.value, x = sx.value, ft = (t) => gTanh(t, c);
      p.clear();
      p.fn(gelu, { c: "ink", w: 3.2, opacity: 0.35 });
      p.fn(gSig, { c: "teal", w: 1.8, dash: "6 4" });
      p.fn(ft, { c: "blue", w: 1.8 });
      p.vline(x, { c: "faint" });
      p.legend([{ label: L.exact, c: "ink" }, { label: L.tanhA, c: "blue" }, { label: L.sigA, c: "teal", dash: true }]);
      q.clear();
      q.fn((t) => Math.abs(gSig(t) - gelu(t)), { c: "teal", w: 1.8, dash: "6 4", n: 900 });
      q.fn((t) => Math.abs(ft(t) - gelu(t)), { c: "blue", w: 2, n: 900 });
      q.vline(x, { c: "faint" });
      let m = 0;
      for (let i = 0; i <= 2400; i++) { const t = -6 + i * 0.005; m = Math.max(m, Math.abs(ft(t) - gelu(t))); }
      q.hline(m, { c: "blue", w: 1, dash: "2 3" });
      ro.set("g", FV.fmt(gelu(x), 4)); ro.set("t", FV.fmt(ft(x), 4)); ro.set("s", FV.fmt(gSig(x), 4)); ro.set("m", FV.num(m, 2));
    }
    p.onresize = draw; q.onresize = draw; draw();
  });

  // 6. x·Φ(x/s) over (x, s): from ReLU (s → 0) to x/2 (s → ∞).
  FV.widget("gelu-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const F = { fn: (x, s) => x * Phi(x / s), der: (x, s) => dgelu(x / s) };
    const Z = { fn: [-0.4, 1.05], der: [-0.25, 1.2] };
    let mode = "fn";
    const s3 = new FV.Surface(FV.col(w.stage), { f: F.fn, x: [-3, 1], y: [0.05, 2], z: Z.fn, n: 40, labels: { x: "x", y: "s", z: "f" }, azimuth: cfg.az != null ? cfg.az : 0.5, elevation: cfg.el != null ? cfg.el : 0.5, aspect: 0.85, cmap: "viridis", title: "f(x, s) = x·Φ(x/s)" });
    const p = new FV.Plot(FV.col(w.stage), { x: [-3, 3], y: [-0.5, 3], xLabel: L.x, yLabel: "f", aspect: 0.85, title: L.slice });
    const ss = FV.ui.slider({ label: L.s, min: 0.05, max: 2, step: 0.01, value: cfg.s != null ? cfg.s : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const md = FV.ui.seg({ label: L.mode, value: "fn", options: [{ value: "fn", label: L.fn }, { value: "der", label: L.der }], onchange: (v) => { mode = v; s3.o.labels.z = v === "fn" ? "f" : "∂f/∂x"; s3.setF(F[v], Z[v]); p.setDomain(null, v === "fn" ? [-0.5, 3] : [-0.2, 1.2]); draw(); } });
    w.controls.append(md.el, ss.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: L.minAt }, { key: "v", label: L.minVal + " =", c: "teal" }]);
    function draw() {
      const s = ss.value, f = (x) => F[mode](x, s);
      const sl = FV.linspace(-3, 1, 81).map((x) => [x, s, f(x)]);
      const ml = FV.linspace(0.05, 2, 60).map((t) => [XMIN * t, t, mode === "fn" ? GMIN * t : 0]);
      s3.setPaths([{ pts: ml, c: "teal", w: 2.2 }, { pts: sl, c: "orange", w: 3 }]);
      p.clear();
      if (mode === "fn") {
        p.fn(relu, { c: "guide", w: 1.5, dash: "5 4" });
        p.fn((x) => x / 2, { c: "faint", w: 1.3, dash: "2 4" });
        p.fn(f, { c: "orange", w: 2.6 });
        p.dot(XMIN * s, GMIN * s, { c: "teal", r: 4.5 });
        p.legend([{ label: "x·Φ(x/s)", c: "orange" }, { label: L.relu + " (s → 0)", c: "guide", dash: true }, { label: L.half, c: "faint", dash: true }]);
      } else {
        p.line(-3, 0, 0, 0, { c: "guide", w: 1.8, dash: "5 4" }); p.line(0, 1, 3, 1, { c: "guide", w: 1.8, dash: "5 4" });
        p.hline(0.5, { c: "faint", dash: "2 4" });
        p.fn(f, { c: "orange", w: 2.6 });
        p.dot(XMIN * s, 0, { c: "teal", r: 4.5 });
        p.legend([{ label: "∂f/∂x", c: "orange" }, { label: "ReLU′ (s → 0)", c: "guide", dash: true }, { label: "1/2 (s → ∞)", c: "faint", dash: true }]);
      }
      ro.set("x", FV.fmt(XMIN * s, 3)); ro.set("v", FV.fmt(GMIN * s, 3));
    }
    p.onresize = draw; draw();
  });

  // 7. Training: the same tiny network (4 neurons) with GELU and with ReLU.
  FV.widget("gelu-train", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-3.2, 3.2], y: [-2.4, 2.4], xLabel: L.x, yLabel: "y", aspect: 0.8 });
    const MAXS = 2000, PER = 10, H = cfg.h || 4, lr = 0.03;
    const b = new FV.Plot(FV.col(w.stage), { x: [0, MAXS], y: [1e-3, 30], yType: "log", xLabel: L.step, yLabel: L.loss, aspect: 0.8 });
    const D = trainData();
    let G, R, step, hist;
    const units = FV.ui.seg({ label: L.units, value: "none", options: [{ value: "none", label: L.none }, { value: "gelu", label: "GELU" }, { value: "relu", label: "ReLU" }], onchange: () => draw() });
    const player = FV.ui.player({
      interval: 60,
      onstep() {
        for (let k = 0; k < PER && step < MAXS; k++) { G.step(D.X, D.Y); R.step(D.X, D.Y); step++; }
        hist.push([step, G.mse(D.X, D.Y), R.mse(D.X, D.Y)]);
        draw();
        return step < MAXS;
      },
      onreset() { reset(); draw(); },
    });
    w.controls.append(player.el, units.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.steps + " =" }, { key: "g", label: L.lossG + " =", c: "blue" }, { key: "r", label: L.lossR + " =", c: "violet" }]);
    function reset() { G = mlp("gelu", H, lr); R = mlp("relu", H, lr); step = 0; hist = [[0, G.mse(D.X, D.Y), R.mse(D.X, D.Y)]]; }
    function draw() {
      a.clear();
      if (units.value !== "none") {
        const N = units.value === "gelu" ? G : R;
        for (let j = 0; j < N.H; j++) a.fn((x) => N.unit(j, x), { c: units.value === "gelu" ? "blue" : "violet", w: 1.2, opacity: 0.5, n: 300 });
      }
      D.X.forEach((x, i) => a.dot(x, D.Y[i], { c: "faint", r: 3.5 }));
      a.fn(R.pred, { c: "violet", w: 2.2, n: 400 });
      a.fn(G.pred, { c: "blue", w: 2.4, n: 400 });
      a.legend([{ label: L.data, c: "faint", dot: true }, { label: L.fitG, c: "blue" }, { label: L.fitR, c: "violet" }]);
      b.clear();
      b.path(hist.map((h) => [h[0], h[2]]), { c: "violet", w: 2 });
      b.path(hist.map((h) => [h[0], h[1]]), { c: "blue", w: 2.2 });
      b.legend([{ label: "GELU", c: "blue" }, { label: "ReLU", c: "violet" }]);
      const last = hist[hist.length - 1];
      b.dot(last[0], last[2], { c: "violet", r: 4 }); b.dot(last[0], last[1], { c: "blue", r: 4 });
      ro.set("s", String(step)); ro.set("g", FV.num(last[1], 3)); ro.set("r", FV.num(last[2], 3));
    }
    a.onresize = draw; b.onresize = draw;
    reset(); draw();
  });
})();
