/* Widgets of the formula page "Adam". Built on FV (assets/js/viz.js).
   Optimizer colours, shared with the SGD page: SGD ink, Momentum blue, RMSProp teal, Adam orange, AdamW violet. */
(function () {
  "use strict";
  const L = {
    ru: {
      step: "шаг", t: "Шаг $t$", sigma: "Шум $\\sigma$", b1: "$\\beta_1$", b2: "$\\beta_2$", g: "gₜ", mean: "среднее градиента", mh: "m̂ₜ (с поправкой)", m: "mₜ (без поправки)",
      rms: "±√v̂ₜ", upd: "m̂ₜ / √v̂ₜ (с поправкой)", updRaw: "mₜ / √vₜ (без поправки)", grads: "градиенты и моменты", steps: "шаг Adam в единицах η",
      f1: "1/(1 − β₁ᵗ)", f2: "1/(1 − β₂ᵗ)", ratio: "шаг без поправки / с поправкой", corr: "поправки при t = 1:", rmax: "макс. завышение шага:", at: "при t =", t1: "поправка β₂ < 1% с t =",
      snr: "отношение сигнал/шум μ/σ", snrS: "Сигнал/шум $\\mu/\\sigma$", theory: "теория μ/√(μ² + σ²)", sim: "симуляция Adam (среднее ± ст. откл.)", sgd: "SGD: шаг ∝ μ", stepEta: "средний шаг / η",
      thr: "теория =", simv: "симуляция =", spread: "разброс =",
      scale: "Общий масштаб $k$", eps: "$\\epsilon$", param: "параметр (масштаб градиента)", bars: "длина шага |Δθ|", sgdBar: "SGD (η = 10⁻³)", adamBar: "Adam (η = 10⁻³)",
      sgdR: "SGD: max/min шага =", adamR: "Adam: max/min шага =", effLr: "η/(√v̂ + ε) от", to: "до",
      fn: "Функция", plateau: "плато с ямой", rosen: "Розенброк", start: "старт (тяните)", reach: "до f < 0,01:", now: "шаг t =", top: "вид сверху",
      lam: "Затухание $\\lambda$", theta: "θₜ", adamL2: "Adam + L2", adamw: "AdamW", c0: "градиент 0", c1: "±0,1", c2: "±10", expd: "e^(−ηλt)",
      l2: "Adam+L2, θ₁₀₀₀ при c = 0 / 0,1 / 10:", wv: "AdamW:",
      warm: "Разогрев, шагов", minr: "$\\eta_{\\min}/\\eta_{\\max}$", lr: "темп ηₜ", loss: "потери", constant: "постоянный η", sched: "разогрев + косинус", lossEnd: "потери (ср. за последние 100):", gain: "выигрыш:",
    },
    en: {
      step: "step", t: "Step $t$", sigma: "Noise $\\sigma$", b1: "$\\beta_1$", b2: "$\\beta_2$", g: "gₜ", mean: "gradient mean", mh: "m̂ₜ (corrected)", m: "mₜ (uncorrected)",
      rms: "±√v̂ₜ", upd: "m̂ₜ / √v̂ₜ (corrected)", updRaw: "mₜ / √vₜ (uncorrected)", grads: "gradients and moments", steps: "Adam step in units of η",
      f1: "1/(1 − β₁ᵗ)", f2: "1/(1 − β₂ᵗ)", ratio: "uncorrected / corrected step", corr: "corrections at t = 1:", rmax: "max overshoot of the step:", at: "at t =", t1: "β₂ correction below 1% from t =",
      snr: "signal-to-noise ratio μ/σ", snrS: "Signal/noise $\\mu/\\sigma$", theory: "theory μ/√(μ² + σ²)", sim: "Adam simulation (mean ± std)", sgd: "SGD: step ∝ μ", stepEta: "mean step / η",
      thr: "theory =", simv: "simulation =", spread: "spread =",
      scale: "Overall scale $k$", eps: "$\\epsilon$", param: "parameter (gradient scale)", bars: "step length |Δθ|", sgdBar: "SGD (η = 10⁻³)", adamBar: "Adam (η = 10⁻³)",
      sgdR: "SGD: max/min step =", adamR: "Adam: max/min step =", effLr: "η/(√v̂ + ε) from", to: "to",
      fn: "Function", plateau: "plateau with a pit", rosen: "Rosenbrock", start: "start (drag it)", reach: "to f < 0.01:", now: "step t =", top: "view from above",
      lam: "Decay $\\lambda$", theta: "θₜ", adamL2: "Adam + L2", adamw: "AdamW", c0: "gradient 0", c1: "±0.1", c2: "±10", expd: "e^(−ηλt)",
      l2: "Adam+L2, θ₁₀₀₀ at c = 0 / 0.1 / 10:", wv: "AdamW:",
      warm: "Warmup, steps", minr: "$\\eta_{\\min}/\\eta_{\\max}$", lr: "rate ηₜ", loss: "loss", constant: "constant η", sched: "warmup + cosine", lossEnd: "loss (mean of the last 100):", gain: "gain:",
    },
    uz: {
      step: "qadam", t: "Qadam $t$", sigma: "Shovqin $\\sigma$", b1: "$\\beta_1$", b2: "$\\beta_2$", g: "gₜ", mean: "gradiyent o‘rtachasi", mh: "m̂ₜ (tuzatilgan)", m: "mₜ (tuzatilmagan)",
      rms: "±√v̂ₜ", upd: "m̂ₜ / √v̂ₜ (tuzatilgan)", updRaw: "mₜ / √vₜ (tuzatilmagan)", grads: "gradiyentlar va momentlar", steps: "η birliklarida Adam qadami",
      f1: "1/(1 − β₁ᵗ)", f2: "1/(1 − β₂ᵗ)", ratio: "tuzatishsiz / tuzatishli qadam", corr: "t = 1 dagi tuzatishlar:", rmax: "qadamning eng katta oshishi:", at: "t =", t1: "β₂ tuzatishi 1% dan kichik, t =",
      snr: "signal/shovqin nisbati μ/σ", snrS: "Signal/shovqin $\\mu/\\sigma$", theory: "nazariya μ/√(μ² + σ²)", sim: "Adam simulyatsiyasi (o‘rtacha ± st. chetl.)", sgd: "SGD: qadam ∝ μ", stepEta: "o‘rtacha qadam / η",
      thr: "nazariya =", simv: "simulyatsiya =", spread: "tarqoqlik =",
      scale: "Umumiy masshtab $k$", eps: "$\\epsilon$", param: "parametr (gradiyent masshtabi)", bars: "qadam uzunligi |Δθ|", sgdBar: "SGD (η = 10⁻³)", adamBar: "Adam (η = 10⁻³)",
      sgdR: "SGD: qadam max/min =", adamR: "Adam: qadam max/min =", effLr: "η/(√v̂ + ε):", to: "dan",
      fn: "Funksiya", plateau: "chuqurli plato", rosen: "Rozenbrok", start: "start (torting)", reach: "f < 0,01 gacha:", now: "qadam t =", top: "yuqoridan ko‘rinish",
      lam: "So‘nish $\\lambda$", theta: "θₜ", adamL2: "Adam + L2", adamw: "AdamW", c0: "gradiyent 0", c1: "±0,1", c2: "±10", expd: "e^(−ηλt)",
      l2: "Adam+L2, c = 0 / 0,1 / 10 da θ₁₀₀₀:", wv: "AdamW:",
      warm: "Qizdirish, qadam", minr: "$\\eta_{\\min}/\\eta_{\\max}$", lr: "ηₜ tezlik", loss: "yo‘qotish", constant: "o‘zgarmas η", sched: "qizdirish + kosinus", lossEnd: "yo‘qotish (oxirgi 100 tasi o‘rtachasi):", gain: "yutuq:",
    },
  }[FV.lang] || {};
  const DEC = FV.lang === "en" ? "." : ",";
  const texNum = (s) => String(s).replace(/\./g, FV.lang === "en" ? "." : "{,}");

  // <core> pure functions, no DOM (checked numerically outside the browser)
  // Adam on a scalar gradient stream: all intermediate quantities.
  function adamTrace(gs, b1, b2, eps) {
    let m = 0, v = 0;
    const out = { m: [], v: [], mh: [], vh: [], up: [], raw: [] };
    gs.forEach((g, i) => {
      const t = i + 1;
      m = b1 * m + (1 - b1) * g; v = b2 * v + (1 - b2) * g * g;
      const mh = m / (1 - Math.pow(b1, t)), vh = v / (1 - Math.pow(b2, t));
      out.m.push(m); out.v.push(v); out.mh.push(mh); out.vh.push(vh);
      out.up.push(mh / (Math.sqrt(vh) + eps)); out.raw.push(m / (Math.sqrt(v) + eps));
    });
    return out;
  }
  function noisyStream(n, sigma, seed) { // mean +0.5 for t ≤ 100, −0.5 after
    const r = FV.rng(seed || 4), g = [], mu = [];
    for (let t = 1; t <= n; t++) { const a = t <= 100 ? 0.5 : -0.5; mu.push(a); g.push(a + sigma * r.normal()); }
    return { g, mu };
  }
  // Optimizers on a parameter vector: sgd | momentum | rmsprop | adam | adamw.
  function makeOpt(kind, o) {
    let u = null, m = null, v = null, t = 0;
    return function (th, g) {
      const n = th.length, out = new Array(n);
      if (!u) { u = new Array(n).fill(0); m = new Array(n).fill(0); v = new Array(n).fill(0); }
      t++;
      for (let i = 0; i < n; i++) {
        if (kind === "momentum") { u[i] = o.beta * u[i] + g[i]; out[i] = th[i] - o.eta * u[i]; }
        else if (kind === "rmsprop") { v[i] = o.beta * v[i] + (1 - o.beta) * g[i] * g[i]; out[i] = th[i] - (o.eta * g[i]) / (Math.sqrt(v[i]) + 1e-8); }
        else if (kind === "adam" || kind === "adamw") {
          const gi = kind === "adam" && o.wd ? g[i] + o.wd * th[i] : g[i];
          m[i] = o.b1 * m[i] + (1 - o.b1) * gi; v[i] = o.b2 * v[i] + (1 - o.b2) * gi * gi;
          const mh = m[i] / (1 - Math.pow(o.b1, t)), vh = v[i] / (1 - Math.pow(o.b2, t));
          const x = kind === "adamw" && o.wd ? th[i] - o.eta * o.wd * th[i] : th[i];
          out[i] = x - (o.eta * mh) / (Math.sqrt(vh) + (o.eps != null ? o.eps : 1e-8));
        } else out[i] = th[i] - o.eta * g[i];
      }
      return out;
    };
  }
  function trajectory(kind, o, grad, th0, n) {
    const step = makeOpt(kind, o), pts = [th0.slice()];
    let th = th0.slice();
    for (let t = 0; t < n; t++) {
      th = step(th, grad(th));
      if (!th.every((x) => Number.isFinite(x) && Math.abs(x) < 1e3)) { pts.diverged = t + 1; break; }
      pts.push(th);
    }
    return pts;
  }
  // Two test functions for the race.
  const qP = (x, y) => 0.2 * (x - 1) ** 2 + 1.2 * (y - 0.5) ** 2;
  const FUN = {
    plateau: {
      f: (x, y) => 1 - Math.exp(-qP(x, y)),
      grad: ([x, y]) => { const e = Math.exp(-qP(x, y)); return [e * 0.4 * (x - 1), e * 2.4 * (y - 0.5)]; },
      x: [-3, 3], y: [-2, 2], start: [-2.4, -1.5], n: 300, min: [1, 0.5],
      opt: { sgd: { eta: 0.3 }, momentum: { eta: 0.3, beta: 0.9 }, rmsprop: { eta: 0.05, beta: 0.9 }, adam: { eta: 0.05, b1: 0.9, b2: 0.999 }, adamw: { eta: 0.05, b1: 0.9, b2: 0.999, wd: 0.1 } },
    },
    rosen: {
      f: (x, y) => (1 - x) ** 2 + 100 * (y - x * x) ** 2,
      grad: ([x, y]) => [-2 * (1 - x) - 400 * x * (y - x * x), 200 * (y - x * x)],
      x: [-2, 2], y: [-1, 3], start: [-1.5, 2], n: 2000, min: [1, 1],
      opt: { sgd: { eta: 0.001 }, momentum: { eta: 0.001, beta: 0.9 }, rmsprop: { eta: 0.01, beta: 0.9 }, adam: { eta: 0.05, b1: 0.9, b2: 0.999 }, adamw: { eta: 0.05, b1: 0.9, b2: 0.999, wd: 0.01 } },
    },
  };
  // Mean and spread of Adam's step for a stationary gradient N(μ, 1).
  function snrPoint(mu, b1, b2, T, burn) {
    const r = FV.rng(17);
    let m = 0, v = 0, s = 0, s2 = 0, k = 0;
    for (let t = 1; t <= T; t++) {
      const g = mu + r.normal();
      m = b1 * m + (1 - b1) * g; v = b2 * v + (1 - b2) * g * g;
      if (t > burn) { const u = m / (1 - Math.pow(b1, t)) / (Math.sqrt(v / (1 - Math.pow(b2, t))) + 1e-8); s += u; s2 += u * u; k++; }
    }
    const mean = s / k;
    return { mean, sd: Math.sqrt(Math.max(0, s2 / k - mean * mean)) };
  }
  // Last-step lengths of SGD and Adam for gradients c·k·(1 + 0.5ξ) with one shared noise sequence.
  function scaleSteps(cs, k, eps, eta, T) {
    const r = FV.rng(8), xi = [];
    for (let t = 0; t < T; t++) xi.push(r.normal());
    return cs.map((c) => {
      const gs = xi.map((x) => c * k * (1 + 0.5 * x)), tr = adamTrace(gs, 0.9, 0.999, eps);
      const vh = tr.vh[T - 1];
      return { sgd: eta * Math.abs(gs[T - 1]), adam: eta * Math.abs(tr.up[T - 1]), lr: eta / (Math.sqrt(vh) + eps) };
    });
  }
  // A weight whose data gradient alternates ±c (zero mean) under weight decay λ.
  function decayRun(c, lam, eta, decoupled, T) {
    let th = 1, m = 0, v = 0;
    const out = [1];
    for (let t = 1; t <= T; t++) {
      let g = c * (t % 2 ? 1 : -1);
      if (!decoupled) g += lam * th;
      m = 0.9 * m + 0.1 * g; v = 0.999 * v + 0.001 * g * g;
      const mh = m / (1 - Math.pow(0.9, t)), vh = v / (1 - Math.pow(0.999, t));
      if (decoupled) th -= eta * lam * th;
      th -= (eta * mh) / (Math.sqrt(vh) + 1e-8);
      out.push(th);
    }
    return out;
  }
  // Learning-rate schedule: linear warmup, then cosine decay to minR·ηmax.
  function lrAt(t, T, emax, warm, minR) {
    if (warm > 0 && t <= warm) return (emax * t) / warm;
    const p = (t - warm) / Math.max(1, T - warm);
    return emax * (minR + (1 - minR) * 0.5 * (1 + Math.cos(Math.PI * p)));
  }
  // Adam on a noisy 10-dimensional quadratic with curvatures 10⁻²…1.
  function noisyQuad(T, lrFn) {
    const D = 10, lam = Array.from({ length: D }, (_, i) => Math.pow(10, -2 + (2 * i) / (D - 1)));
    const r = FV.rng(21), th = new Array(D).fill(1), m = new Array(D).fill(0), v = new Array(D).fill(0), out = [];
    const loss = () => th.reduce((s, x, i) => s + 0.5 * lam[i] * x * x, 0);
    out.push(loss());
    for (let t = 1; t <= T; t++) {
      const e = lrFn(t);
      for (let i = 0; i < D; i++) {
        const g = lam[i] * th[i] + 0.05 * r.normal();
        m[i] = 0.9 * m[i] + 0.1 * g; v[i] = 0.999 * v[i] + 0.001 * g * g;
        th[i] -= (e * (m[i] / (1 - Math.pow(0.9, t)))) / (Math.sqrt(v[i] / (1 - Math.pow(0.999, t))) + 1e-8);
      }
      out.push(loss());
    }
    return out;
  }
  const meanLast = (a, n) => a.slice(-n).reduce((s, x) => s + x, 0) / n;
  FV.pageCore = Object.assign(FV.pageCore || {}, { adam: { adamTrace, noisyStream, makeOpt, trajectory, FUN, snrPoint, scaleSteps, decayRun, lrAt, noisyQuad, meanLast } });
  // </core>

  if (!FV.widget) return;
  const COL = { sgd: "ink", momentum: "blue", rmsprop: "teal", adam: "orange", adamw: "violet" };
  const NAME = { sgd: "SGD", momentum: "Momentum", rmsprop: "RMSProp", adam: "Adam", adamw: "AdamW" };
  const KINDS = ["sgd", "momentum", "rmsprop", "adam", "adamw"];
  function lossHeat(p, f, lo, hi) {
    const a = Math.log10(lo), b = Math.log10(hi), span = (b - a) / 0.35;
    p.heat((x, y) => Math.log10(Math.max(f(x, y), lo)), { cmap: "diverging", z: [a - span / 2, a + span / 2], res: 4, alpha: 0.5 });
  }
  const sup = (e) => "10" + String(e).replace("-", "⁻").replace(/\d/g, (d) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[d]);

  // 1. Moments of a noisy gradient: m, v, their bias-corrected versions and the resulting step.
  FV.widget("adam-moments", (el, cfg) => {
    const w = FV.shell(el, {});
    const n = 200;
    const a = new FV.Plot(w.stage, { x: [0, n], y: [-3.5, 3.5], xLabel: L.step + " t", yLabel: "", aspect: 0.36, minHeight: 230, maxHeight: 300, title: L.grads });
    const b = new FV.Plot(w.stage, { x: [0, n], y: [-6, 6], xLabel: L.step + " t", yLabel: "", aspect: 0.3, minHeight: 210, maxHeight: 260, title: L.steps });
    const s1 = FV.ui.slider({ label: L.b1, min: 0, max: 0.99, step: 0.01, value: cfg.b1 != null ? cfg.b1 : 0.9, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const s2 = FV.ui.seg({ label: L.b2, value: cfg.b2 || 0.999, options: [0.9, 0.99, 0.999].map((v) => ({ value: v, label: FV.fmt(v, String(v).length - 2) })), onchange: draw });
    const ss = FV.ui.slider({ label: L.sigma, min: 0, max: 2, step: 0.05, value: cfg.sigma != null ? cfg.sigma : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const st = FV.ui.slider({ label: L.t, min: 1, max: n, step: 1, value: cfg.t || 1, fmt: (v) => String(v), oninput: draw });
    w.controls.append(s1.el, s2.el, ss.el, st.el);
    const ro = FV.ui.readout(w.readout, [{ key: "g", label: "gₜ =" }, { key: "m", label: "mₜ =" }, { key: "mh", label: "m̂ₜ =", c: "orange" }, { key: "vh", label: "√v̂ₜ =", c: "teal" }, { key: "u", label: "m̂ₜ/√v̂ₜ =", c: "orange" }, { key: "r", label: "mₜ/√vₜ =" }]);
    function draw() {
      const S = noisyStream(n, ss.value), tr = adamTrace(S.g, s1.value, s2.value, 1e-8), T = st.value;
      a.clear();
      a.path(S.mu.map((v, i) => [i + 1, v]), { c: "guide", w: 1.4, dash: "5 4" });
      S.g.forEach((g, i) => a.dot(i + 1, FV.clamp(g, -3.5, 3.5), { c: "faint", r: 1.8 }));
      a.path(tr.vh.map((v, i) => [i + 1, Math.sqrt(v)]), { c: "teal", w: 1.8 });
      a.path(tr.vh.map((v, i) => [i + 1, -Math.sqrt(v)]), { c: "teal", w: 1.8 });
      a.path(tr.m.map((v, i) => [i + 1, v]), { c: "orange", w: 1.4, dash: "4 3" });
      a.path(tr.mh.map((v, i) => [i + 1, v]), { c: "orange", w: 2.2 });
      a.vline(T, { c: "ink", opacity: 0.5 });
      a.legend([{ label: L.g, c: "faint", dot: true }, { label: L.mean, c: "guide", dash: true }, { label: L.mh, c: "orange" }, { label: L.m, c: "orange", dash: true }, { label: L.rms, c: "teal" }]);
      b.clear();
      b.hline(1, { c: "guide" }); b.hline(-1, { c: "guide" });
      b.path(tr.raw.map((v, i) => [i + 1, FV.clamp(v, -6, 6)]), { c: "orange", w: 1.4, dash: "4 3" });
      b.path(tr.up.map((v, i) => [i + 1, v]), { c: "orange", w: 2.2 });
      b.vline(T, { c: "ink", opacity: 0.5 });
      b.dot(T, tr.up[T - 1], { c: "orange", r: 4 });
      b.legend([{ label: L.upd, c: "orange" }, { label: L.updRaw, c: "orange", dash: true }]);
      const i = T - 1;
      ro.set("g", FV.fmt(S.g[i], 3)); ro.set("m", FV.fmt(tr.m[i], 3)); ro.set("mh", FV.fmt(tr.mh[i], 3)); ro.set("vh", FV.fmt(Math.sqrt(tr.vh[i]), 3));
      ro.set("u", FV.fmt(tr.up[i], 3)); ro.set("r", FV.fmt(tr.raw[i], 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 2. Bias-correction factors and how much an uncorrected step would overshoot.
  FV.widget("adam-bias", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [1, 1e4], xType: "log", y: [0.5, 3000], yType: "log", xLabel: L.step + " t", yLabel: "", aspect: 0.5 });
    const s1 = FV.ui.slider({ label: L.b1, min: 0.5, max: 0.99, step: 0.01, value: cfg.b1 || 0.9, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const s2 = FV.ui.slider({ label: L.b2, min: -4, max: -1, step: 0.05, value: Math.log10(1 - (cfg.b2 || 0.999)), map: (s) => 1 - Math.pow(10, s), unmap: (v) => Math.log10(1 - v), fmt: (v) => { const d = -Math.log10(1 - v); return FV.fmt(v, Math.abs(d - Math.round(d)) < 1e-6 ? Math.max(2, Math.round(d)) : Math.ceil(d) + 1); }, oninput: draw });
    w.controls.append(s1.el, s2.el);
    const ro = FV.ui.readout(w.readout, [{ key: "c", label: L.corr }, { key: "m", label: L.rmax, c: "ink" }, { key: "t", label: L.t1, c: "teal" }]);
    function draw() {
      const b1 = s1.value, b2 = s2.value;
      const r = (t) => (1 - Math.pow(b1, t)) / Math.sqrt(1 - Math.pow(b2, t));
      p.clear();
      p.hline(1, { c: "guide" });
      p.fn((t) => 1 / (1 - Math.pow(b1, t)), { c: "orange", w: 2.4 });
      p.fn((t) => 1 / (1 - Math.pow(b2, t)), { c: "teal", w: 2.4 });
      p.fn(r, { c: "ink", w: 2, dash: "6 4" });
      let best = 1, bt = 1;
      for (let t = 1; t <= 1e4; t++) { const v = r(t); if (v > best) { best = v; bt = t; } }
      p.dot(bt, best, { c: "ink", r: 4 });
      p.text(bt, best, "×" + FV.fmt(best, 2), { dy: -10, anchor: "middle" });
      p.dot(1, r(1), { c: "ink", r: 3.5, hollow: true });
      p.legend([{ label: "1/(1 − β₁ᵗ)", c: "orange" }, { label: "1/(1 − β₂ᵗ)", c: "teal" }, { label: L.ratio, c: "ink", dash: true }]);
      const t1 = Math.ceil(Math.log(0.01) / Math.log(b2));
      ro.set("c", FV.num(1 / (1 - b1), 3) + " / " + FV.num(1 / (1 - b2), 4));
      ro.set("m", "×" + FV.fmt(best, 2) + " " + L.at + " " + bt + " (t = 1: ×" + FV.fmt(r(1), 2) + ")");
      ro.set("t", String(t1));
    }
    p.onresize = draw; draw();
  });

  // 3. Adam's step as a function of the gradient's signal-to-noise ratio.
  FV.widget("adam-snr", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0.01, 100], xType: "log", y: [0, 1.2], xLabel: L.snr, yLabel: L.stepEta, aspect: 0.48 });
    const s1 = FV.ui.slider({ label: L.b1, min: 0, max: 0.99, step: 0.01, value: cfg.b1 != null ? cfg.b1 : 0.9, fmt: (v) => FV.fmt(v, 2), oninput: () => { cache = null; draw(); } });
    const s2 = FV.ui.seg({ label: L.b2, value: cfg.b2 || 0.999, options: [0.9, 0.99, 0.999].map((v) => ({ value: v, label: FV.fmt(v, String(v).length - 2) })), onchange: () => { cache = null; draw(); } });
    const sx = FV.ui.slider({ label: L.snrS, min: -2, max: 2, value: Math.log10(cfg.snr || 0.3), map: (s) => Math.pow(10, s), unmap: (v) => Math.log10(v), fmt: (v) => FV.num(v, 2), oninput: () => draw() });
    w.controls.append(s1.el, s2.el, sx.el);
    const ro = FV.ui.readout(w.readout, [{ key: "th", label: L.thr }, { key: "m", label: L.simv, c: "orange" }, { key: "s", label: L.spread }]);
    const XS = FV.linspace(-2, 2, 21).map((s) => Math.pow(10, s));
    let cache = null;
    const th = (s) => s / Math.sqrt(1 + s * s);
    function draw() {
      if (!cache) cache = XS.map((s) => snrPoint(s, s1.value, s2.value, 20000, 2000));
      const s = sx.value, cur = snrPoint(s, s1.value, s2.value, 20000, 2000);
      p.clear();
      p.hline(1, { c: "guide" });
      p.fn((x) => x, { c: "ink", w: 1.4, dash: "5 4" });
      p.fn(th, { c: "ink", w: 2.2 });
      XS.forEach((x, i) => { const q = cache[i]; p.line(x, q.mean - q.sd, x, q.mean + q.sd, { c: "orange", w: 1.4, opacity: 0.6 }); p.dot(x, q.mean, { c: "orange", r: 3.5 }); });
      p.vline(s, { c: "ink", opacity: 0.5 });
      p.dot(s, cur.mean, { c: "orange", r: 5 });
      p.legend([{ label: L.theory, c: "ink" }, { label: L.sim, c: "orange", dot: true }, { label: L.sgd, c: "ink", dash: true }]);
      ro.set("th", FV.fmt(th(s), 3)); ro.set("m", FV.fmt(cur.mean, 3)); ro.set("s", "±" + FV.fmt(cur.sd, 3));
    }
    p.onresize = draw; draw();
  });

  // 4. Scale invariance: four parameters whose gradients differ by a factor of 10⁶.
  FV.widget("adam-scale", (el, cfg) => {
    const w = FV.shell(el, {});
    const CS = [1e-3, 1e-1, 1e1, 1e3], eta = 1e-3;
    const p = new FV.Plot(w.stage, { x: [0.4, 4.6], y: [1e-12, 1e3], yType: "log", xLabel: L.param, yLabel: L.bars, aspect: 0.5, xTicks: CS.map((c, i) => ({ v: i + 1, label: "c = " + sup(Math.round(Math.log10(c))) })) });
    const sk = FV.ui.slider({ label: L.scale, min: -6, max: 3, step: 0.5, value: 0, map: (s) => Math.pow(10, s), unmap: (v) => Math.log10(v), fmt: (v) => FV.num(v, 2), oninput: draw });
    const se = FV.ui.slider({ label: L.eps, min: -12, max: -2, step: 0.5, value: Math.log10(cfg.eps || 1e-8), map: (s) => Math.pow(10, s), unmap: (v) => Math.log10(v), fmt: (v) => FV.num(v, 2), oninput: draw });
    w.controls.append(sk.el, se.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.sgdR, c: "ink" }, { key: "a", label: L.adamR, c: "orange" }, { key: "l", label: L.effLr, c: "orange" }]);
    function draw() {
      const k = sk.value, R = scaleSteps(CS, k, se.value, eta, 100);
      p.o.xTicks = CS.map((c, i) => ({ v: i + 1, label: "c = " + FV.num(c * k, 1) }));
      p.clear();
      p.hline(eta, { c: "orange", w: 1, dash: "5 4", opacity: 0.8 });
      p.text(4.58, eta, "η", { anchor: "end", dy: -6, c: "orange" });
      R.forEach((q, i) => {
        p.rect(i + 1 - 0.34, 1e-12, i + 1 - 0.02, Math.max(q.sgd, 1e-12), { c: "ink", opacity: 0.75 });
        p.rect(i + 1 + 0.02, 1e-12, i + 1 + 0.34, Math.max(q.adam, 1e-12), { c: "orange", opacity: 0.9 });
      });
      p.legend([{ label: L.sgdBar, c: "ink", box: true }, { label: L.adamBar, c: "orange", box: true }]);
      const sg = R.map((q) => q.sgd), ad = R.map((q) => q.adam), lr = R.map((q) => q.lr);
      const rf = (r) => (r >= 999 && Math.abs(Math.log10(r) - Math.round(Math.log10(r))) < 0.01 ? sup(Math.round(Math.log10(r))) : FV.num(r, 3));
      ro.set("s", rf(Math.max(...sg) / Math.min(...sg))); ro.set("a", rf(Math.max(...ad) / Math.min(...ad)));
      ro.set("l", FV.num(Math.min(...lr), 2) + " " + L.to + " " + FV.num(Math.max(...lr), 2));
    }
    p.onresize = draw; draw();
  });

  // 5. The race: five optimizers on a 3D surface and on its top view.
  FV.widget("adam-race", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    let F = FUN[cfg.fn || "plateau"], st = F.start.slice(), runs = null, t = F.n;
    const z3 = () => (F === FUN.rosen ? (x, y) => Math.log1p(F.f(x, y)) : F.f);
    const s3 = new FV.Surface(FV.col(w.stage), { f: z3(), x: F.x, y: F.y, n: 40, labels: { x: "x", y: "y", z: "f" }, azimuth: -0.65, elevation: 0.62, aspect: 0.85, cmap: "diverging", cmapT: (q) => 0.5 + 0.36 * q, title: "f(x, y)" });
    const a = new FV.Plot(FV.col(w.stage), { x: F.x, y: F.y, xLabel: "x", yLabel: "y", equal: true, title: L.top });
    const sf = FV.ui.seg({ label: L.fn, value: cfg.fn || "plateau", options: [{ value: "plateau", label: L.plateau }, { value: "rosen", label: L.rosen }], onchange: (v) => {
      F = FUN[v]; st = F.start.slice(); runs = null; t = F.n;
      a.setDomain(F.x, F.y); s3.o.labels.z = v === "rosen" ? "ln(1 + f)" : "f"; s3.setDomain(F.x, F.y); s3.setF(z3()); hd.set(st[0], st[1]); draw(); setNote();
    } });
    const pl = FV.ui.player({ interval: 60, onstep() { t = Math.min(F.n, t + Math.max(1, Math.round(F.n / 150))); draw(); return t < F.n; }, onreset() { t = 0; draw(); } });
    w.controls.append(sf.el, pl.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.now }].concat(KINDS.map((k) => ({ key: k, label: NAME[k] + ":", c: COL[k] }))));
    const hd = a.handle(st[0], st[1], { c: "ink", onDrag: (x, y) => { st = [x, y]; return [x, y]; }, onChange: () => { runs = null; draw(); } });
    function setNote() {
      const o = F.opt, e = (v) => "$\\eta=" + texNum(String(v)) + "$";
      w.note.textContent = "";
      w.note.append(FV.rich("SGD " + e(o.sgd.eta) + " · Momentum " + e(o.momentum.eta) + ", $\\beta=" + texNum("0.9") + "$ · RMSProp " + e(o.rmsprop.eta) + " · Adam " + e(o.adam.eta) + " · AdamW " + e(o.adamw.eta) + ", $\\lambda=" + texNum(String(o.adamw.wd)) + "$."));
    }
    function draw() {
      if (!runs) runs = Object.fromEntries(KINDS.map((k) => [k, trajectory(k, F.opt[k], F.grad, st, F.n)]));
      a.clear();
      lossHeat(a, F.f, F === FUN.rosen ? 0.05 : 0.01, F === FUN.rosen ? 2500 : 1);
      a.contours((x, y) => Math.log10(F.f(x, y) + 1e-12), F === FUN.rosen ? [-1, 0, 0.5, 1, 1.5, 2, 2.5, 3] : [-2, -1.5, -1, -0.5, -0.2, -0.05, -0.01], { c: "ink", w: 1, opacity: 0.25 });
      a.dot(F.min[0], F.min[1], { c: "ink", hollow: true, r: 5 });
      const zf = z3(), paths = [];
      KINDS.forEach((k) => {
        const P = runs[k].slice(0, t + 1);
        a.path(P, { c: COL[k], w: k === "adam" ? 2.6 : 1.8 });
        const e = P[P.length - 1]; a.dot(e[0], e[1], { c: COL[k], r: 4 });
        paths.push({ pts: P.map((q) => [q[0], q[1], zf(q[0], q[1])]), c: COL[k], w: 2.4 });
        const fs = runs[k].map((q) => F.f(q[0], q[1])), hit = fs.findIndex((v) => v < 0.01);
        ro.set(k, "f = " + FV.num(fs[Math.min(t, fs.length - 1)], 2) + " · " + L.reach + " " + (hit < 0 ? "—" : hit));
      });
      hd.set(st[0], st[1]);
      s3.setPoints([{ x: F.min[0], y: F.min[1], z: zf(F.min[0], F.min[1]), c: "ink", r: 4 }]);
      s3.setPaths(paths);
      ro.set("t", String(t));
      a.legend(KINDS.map((k) => ({ label: NAME[k], c: COL[k] })).concat([{ label: L.start, c: "ink", dot: true }]));
    }
    a.onresize = draw; setNote(); draw();
  });

  // 6. AdamW versus L2 inside Adam: three weights with data gradients of different size.
  FV.widget("adam-adamw", (el, cfg) => {
    const w = FV.shell(el, {});
    const T = 1000, eta = 0.01, CS = [0, 0.1, 10], DASH = [null, "7 4", "2 3"];
    const p = new FV.Plot(w.stage, { x: [0, T * 1.04], y: [-0.05, 1.08], xLabel: L.step + " t", yLabel: "θₜ", aspect: 0.48 });
    const sl = FV.ui.slider({ label: L.lam, min: 0, max: 0.5, step: 0.01, value: cfg.lam != null ? cfg.lam : 0.1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sl.el);
    const ro = FV.ui.readout(w.readout, [{ key: "l2", label: L.l2, c: "orange" }, { key: "w", label: L.wv, c: "violet" }]);
    function draw() {
      const lam = sl.value;
      const A = CS.map((c) => decayRun(c, lam, eta, false, T)), W = CS.map((c) => decayRun(c, lam, eta, true, T));
      p.clear();
      p.hline(0, { c: "guide", dash: false });
      p.fn((x) => Math.exp(-eta * lam * x), { c: "guide", w: 1.2, dash: "3 4", to: T });
      W.forEach((s, i) => p.path(s.map((y, x) => [x, y]).filter((d, j) => j % 2 === 0), { c: "violet", w: 2.2, dash: DASH[i] }));
      A.forEach((s, i) => p.path(s.map((y, x) => [x, y]).filter((d, j) => j % 2 === 0), { c: "orange", w: 2.2, dash: DASH[i] }));
      const labs = [L.c0, "c = " + L.c1, "c = " + L.c2].map((s, i) => ({ y: A[i][T], s, c: "orange" })).concat([{ y: W[0][T], s: "AdamW", c: "violet" }]);
      let last = -1;
      labs.sort((u, v) => u.y - v.y).forEach((q) => { const y = Math.max(q.y, last + 0.075); last = y; p.text(T - 8, y, q.s, { anchor: "end", dy: -6, c: q.c }); });
      p.legend([{ label: L.adamL2, c: "orange" }, { label: L.adamw, c: "violet" }, { label: "c = 0", c: "faint" }, { label: "c = " + L.c1, c: "faint", dash: true }, { label: L.expd, c: "guide", dash: true }]);
      ro.set("l2", A.map((s) => FV.fmt(s[T], 4)).join(" / ")); ro.set("w", W.map((s) => FV.fmt(s[T], 4)).join(" / "));
    }
    p.onresize = draw; draw();
  });

  // 7. Warmup + cosine schedule and its effect on a noisy problem.
  FV.widget("adam-schedule", (el, cfg) => {
    const w = FV.shell(el, {});
    const T = 2000, emax = 0.05;
    const a = new FV.Plot(w.stage, { x: [0, T * 1.03], y: [0, 0.058], xLabel: L.step + " t", yLabel: L.lr, aspect: 0.26, minHeight: 190, maxHeight: 240 });
    const b = new FV.Plot(w.stage, { x: [0, T * 1.03], y: [1e-4, 3], yType: "log", xLabel: L.step + " t", yLabel: L.loss, aspect: 0.32, minHeight: 220, maxHeight: 280 });
    const sw = FV.ui.slider({ label: L.warm, min: 0, max: 500, step: 10, value: cfg.warm != null ? cfg.warm : 200, fmt: (v) => String(v), oninput: draw });
    const sm = FV.ui.slider({ label: L.minr, min: 0, max: 0.5, step: 0.01, value: cfg.minr != null ? cfg.minr : 0.1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sw.el, sm.el);
    const ro = FV.ui.readout(w.readout, [{ key: "l", label: L.lossEnd }, { key: "g", label: L.gain, c: "orange" }]);
    const base = noisyQuad(T, () => emax);
    function draw() {
      const warm = sw.value, minR = sm.value, lr = (t) => lrAt(t, T, emax, warm, minR), run = noisyQuad(T, lr);
      a.clear();
      a.line(0, emax, T, emax, { c: "orange", w: 1.4, dash: "5 4", opacity: 0.8 });
      a.fn(lr, { c: "orange", w: 2.4, from: 0, to: T });
      a.legend([{ label: L.constant, c: "orange", dash: true }, { label: L.sched, c: "orange" }]);
      b.clear();
      b.path(base.map((v, i) => [i, v]).filter((d, i) => i % 2 === 0), { c: "orange", w: 1.2, dash: "5 4", opacity: 0.8 });
      b.path(run.map((v, i) => [i, v]).filter((d, i) => i % 2 === 0), { c: "orange", w: 1.8 });
      b.legend([{ label: L.constant, c: "orange", dash: true }, { label: L.sched, c: "orange" }]);
      const l0 = meanLast(base, 100), l1 = meanLast(run, 100);
      ro.set("l", FV.num(l0, 2) + " → " + FV.num(l1, 2)); ro.set("g", "×" + FV.fmt(l0 / l1, 1));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });
})();
