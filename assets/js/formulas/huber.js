/* Widgets of the formula page "Huber loss". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      r: "r = y − ŷ", loss: "L(r)", dloss: "производные", delta: "Порог $\\delta$", deriv: "Показать производные",
      huber: "Хьюбер", quad: "½r² (MSE)", lin: "δ(|r| − δ/2)", zone: "|r| ≤ δ", tangent: "касательная",
      psi: "ψ(r) = L′", psi2: "L″", mseD: "r (производная ½r²)", seam: "стык",
      pullTitle: "Тяга точки ψ(r)", weightTitle: "Вес точки w(r) = ψ(r)/r", rOut: "Ошибка точки $r$",
      mse: "MSE", mae: "MAE·δ", pullMse: "тяга MSE =", pullHub: "тяга Хьюбера =", weightHub: "вес Хьюбера =",
      surfTitle: "L(r, δ) в 3D", mapTitle: "Вид сверху: линии уровня, по вертикали $\\delta$", kind: "Функция", hubName: "Хьюбер", pseudoName: "псевдо-Хьюбер",
      slice: "срез δ = ", at2: "L при r = 2:",
      value: "значение x", weight: "вес точки", mean: "среднее", median: "медиана", est: "оценка Хьюбера",
      path: "Оценка $\\hat\\mu$ при разных $\\delta$", quadZone: "± δ", outH: "выброс", inZone: "точек в зоне $|x-\\hat\\mu|\\le\\delta$:",
      x: "x", y: "y", step: "шаг", slope: "наклон", truth: "истинная прямая", trueSlope: "истинный наклон 0,5",
      lineMse: "MSE", lineHub: "Хьюбер", slopeTitle: "Наклон прямой по шагам", outlier: "выбросы (тяните крайний)",
      slopeMse: "наклон MSE =", slopeHub: "наклон Хьюбера =",
      variant: "Сравнить с", pseudo: "псевдо-Хьюбер", logcosh: "log-cosh", sl1: "Smooth L1 (β = δ)",
      second: "Вторая производная", lossT: "Потери", derT: "Производные", rPoint: "Точка $r$",
      hubV: "Хьюбер:", varV: "вариант:", hubD: "ψ Хьюбера:", varD: "ψ варианта:",
      k: "Порог $k=\\delta/\\sigma$", eps: "Доля выбросов $\\varepsilon$", kAxis: "k = δ/σ", vAxis: "дисперсия оценки × n/σ²",
      vHub: "Хьюбер, текущая ε", vClean: "Хьюбер, ε = 0", vMed: "медиана", vMean: "среднее",
      eff: "эффективность при ε = 0:", varNow: "дисперсия при ε:", best: "лучшее k:", meanOff: "среднее: ",
    },
    en: {
      r: "r = y − ŷ", loss: "L(r)", dloss: "derivatives", delta: "Threshold $\\delta$", deriv: "Show the derivatives",
      huber: "Huber", quad: "½r² (MSE)", lin: "δ(|r| − δ/2)", zone: "|r| ≤ δ", tangent: "tangent",
      psi: "ψ(r) = L′", psi2: "L″", mseD: "r (derivative of ½r²)", seam: "seam",
      pullTitle: "Pull of a point ψ(r)", weightTitle: "Weight of a point w(r) = ψ(r)/r", rOut: "Error of the point $r$",
      mse: "MSE", mae: "MAE·δ", pullMse: "MSE pull =", pullHub: "Huber pull =", weightHub: "Huber weight =",
      surfTitle: "L(r, δ) in 3D", mapTitle: "Top view: level lines, $\\delta$ upwards", kind: "Function", hubName: "Huber", pseudoName: "pseudo-Huber",
      slice: "slice δ = ", at2: "L at r = 2:",
      value: "value x", weight: "weight of a point", mean: "mean", median: "median", est: "Huber estimate",
      path: "The estimate $\\hat\\mu$ for different $\\delta$", quadZone: "± δ", outH: "outlier", inZone: "points with $|x-\\hat\\mu|\\le\\delta$:",
      x: "x", y: "y", step: "step", slope: "slope", truth: "true line", trueSlope: "true slope 0.5",
      lineMse: "MSE", lineHub: "Huber", slopeTitle: "Slope of the line, step by step", outlier: "outliers (drag the last one)",
      slopeMse: "MSE slope =", slopeHub: "Huber slope =",
      variant: "Compare with", pseudo: "pseudo-Huber", logcosh: "log-cosh", sl1: "Smooth L1 (β = δ)",
      second: "Second derivative", lossT: "Losses", derT: "Derivatives", rPoint: "Point $r$",
      hubV: "Huber:", varV: "variant:", hubD: "Huber ψ:", varD: "variant ψ:",
      k: "Threshold $k=\\delta/\\sigma$", eps: "Share of outliers $\\varepsilon$", kAxis: "k = δ/σ", vAxis: "variance of the estimate × n/σ²",
      vHub: "Huber, current ε", vClean: "Huber, ε = 0", vMed: "median", vMean: "mean",
      eff: "efficiency at ε = 0:", varNow: "variance at ε:", best: "best k:", meanOff: "mean: ",
    },
    uz: {
      r: "r = y − ŷ", loss: "L(r)", dloss: "hosilalar", delta: "Chegara $\\delta$", deriv: "Hosilalarni ko‘rsatish",
      huber: "Huber", quad: "½r² (MSE)", lin: "δ(|r| − δ/2)", zone: "|r| ≤ δ", tangent: "urinma",
      psi: "ψ(r) = L′", psi2: "L″", mseD: "r (½r² hosilasi)", seam: "tutashuv",
      pullTitle: "Nuqtaning tortishi ψ(r)", weightTitle: "Nuqtaning vazni w(r) = ψ(r)/r", rOut: "Nuqta xatosi $r$",
      mse: "MSE", mae: "MAE·δ", pullMse: "MSE tortishi =", pullHub: "Huber tortishi =", weightHub: "Huber vazni =",
      surfTitle: "L(r, δ) 3D’da", mapTitle: "Yuqoridan ko‘rinish: sath chiziqlari, tik o‘qda $\\delta$", kind: "Funksiya", hubName: "Huber", pseudoName: "psevdo-Huber",
      slice: "kesim δ = ", at2: "r = 2 da L:",
      value: "x qiymat", weight: "nuqta vazni", mean: "o‘rtacha", median: "mediana", est: "Huber bahosi",
      path: "Turli $\\delta$ da $\\hat\\mu$ bahosi", quadZone: "± δ", outH: "chetga chiquvchi", inZone: "$|x-\\hat\\mu|\\le\\delta$ zonadagi nuqtalar:",
      x: "x", y: "y", step: "qadam", slope: "qiyalik", truth: "haqiqiy to‘g‘ri chiziq", trueSlope: "haqiqiy qiyalik 0,5",
      lineMse: "MSE", lineHub: "Huber", slopeTitle: "To‘g‘ri chiziq qiyaligi qadamlar bo‘yicha", outlier: "chetga chiquvchilar (oxirgisini torting)",
      slopeMse: "MSE qiyaligi =", slopeHub: "Huber qiyaligi =",
      variant: "Taqqoslash", pseudo: "psevdo-Huber", logcosh: "log-cosh", sl1: "Smooth L1 (β = δ)",
      second: "Ikkinchi hosila", lossT: "Yo‘qotishlar", derT: "Hosilalar", rPoint: "$r$ nuqta",
      hubV: "Huber:", varV: "variant:", hubD: "Huber ψ:", varD: "variant ψ:",
      k: "Chegara $k=\\delta/\\sigma$", eps: "Chetga chiquvchilar ulushi $\\varepsilon$", kAxis: "k = δ/σ", vAxis: "baho dispersiyasi × n/σ²",
      vHub: "Huber, joriy ε", vClean: "Huber, ε = 0", vMed: "mediana", vMean: "o‘rtacha",
      eff: "ε = 0 dagi samaradorlik:", varNow: "ε dagi dispersiya:", best: "eng yaxshi k:", meanOff: "o‘rtacha: ",
    },
  }[FV.lang] || {};

  const dec = (s) => (FV.lang === "en" ? s : s.replace(/(\d)\.(\d)/g, "$1,$2"));
  // Huber loss, its derivative ψ (the influence function) and the second derivative.
  const H = (r, d) => { const a = Math.abs(r); return a <= d ? 0.5 * r * r : d * (a - 0.5 * d); };
  const psi = (r, d) => Math.max(-d, Math.min(d, r));
  const psi2 = (r, d) => (Math.abs(r) <= d ? 1 : 0);
  const PH = (r, d) => d * d * (Math.sqrt(1 + (r / d) * (r / d)) - 1);
  const logcosh = (x) => { const a = Math.abs(x); return a + Math.log1p(Math.exp(-2 * a)) - Math.LN2; };
  const VARIANTS = {
    pseudo: { f: PH, d: (r, d) => r / Math.sqrt(1 + (r / d) * (r / d)), d2: (r, d) => Math.pow(1 + (r / d) * (r / d), -1.5) },
    logcosh: { f: (r, d) => d * d * logcosh(r / d), d: (r, d) => d * Math.tanh(r / d), d2: (r, d) => 1 / Math.cosh(r / d) ** 2 },
    sl1: { f: (r, d) => H(r, d) / d, d: (r, d) => psi(r, d) / d, d2: (r, d) => psi2(r, d) / d },
  };
  const logSlider = (o) => FV.ui.slider({ label: o.label, min: Math.log10(o.min), max: Math.log10(o.max), step: o.step || 0.01, value: Math.log10(o.value), map: (v) => Math.pow(10, v), unmap: (v) => Math.log10(v), fmt: o.fmt || ((v) => FV.num(v, 3)), oninput: o.oninput });

  // 1. The loss, its two branches, the seam at |r| = δ and (optionally) the first and second derivatives.
  FV.widget("huber-explorer", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-4, 4], y: [-0.25, 4.25], xLabel: L.r, yLabel: L.loss, aspect: 0.5 });
    const box = FV.h("div"); w.stage.append(box);
    let d = null;
    const sd = FV.ui.slider({ label: L.delta, min: 0.1, max: 3, step: 0.05, value: cfg.delta || 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const show = FV.ui.check({ label: L.deriv, checked: cfg.derivative !== false, onchange: (v) => { box.hidden = !v; draw(); } });
    w.controls.append(sd.el, show.el);
    const ro = FV.ui.readout(w.readout, [{ key: "r", label: "r =" }, { key: "l", label: "$L_\\delta(r)$ =", c: "blue" }, { key: "q", label: "½r² =" }, { key: "d", label: "ψ(r) = L′ =", c: "orange" }, { key: "s", label: "L″ =", c: "violet" }]);
    let r0 = cfg.r != null ? cfg.r : 2;
    const h = p.handle(r0, H(r0, sd.value), { c: "blue", onDrag: (x) => { r0 = x; return [x, H(x, sd.value)]; }, onChange: () => draw() });
    function ensureD() {
      if (!d) { d = new FV.Plot(box, { x: [-4, 4], y: [-3.3, 3.3], xLabel: L.r, yLabel: L.dloss, aspect: 0.3, minHeight: 170, maxHeight: 240 }); d.onresize = draw; }
    }
    function draw() {
      const D = sd.value, y0 = H(r0, D), k = psi(r0, D);
      p.clear();
      p.rect(-D, -0.25, D, 4.25, { c: "teal", opacity: 0.07 });
      p.vline(-D, { c: "teal" }); p.vline(D, { c: "teal" });
      p.fn((r) => 0.5 * r * r, { c: "guide", w: 1.8, dash: "6 5" });
      p.fn((r) => D * (Math.abs(r) - 0.5 * D), { c: "faint", w: 1.4, dash: "2 4" });
      p.fn((r) => H(r, D), { c: "blue", w: 2.6 });
      p.line(r0 - 1.6, y0 - 1.6 * k, r0 + 1.6, y0 + 1.6 * k, { c: "orange", w: 1.8 });
      p.dot(-D, 0.5 * D * D, { hollow: true, r: 4, c: "teal" }); p.dot(D, 0.5 * D * D, { hollow: true, r: 4, c: "teal" });
      p.text(D, 4.0, L.zone, { c: "teal", dx: 5 });
      h.set(r0, y0);
      if (show.value) {
        ensureD(); box.hidden = false;
        d.clear();
        d.rect(-D, -3.3, D, 3.3, { c: "teal", opacity: 0.07 });
        d.fn((r) => r, { c: "guide", w: 1.6, dash: "6 5" });
        d.fn((r) => psi2(r, D), { c: "violet", w: 1.8, dash: "5 3", jump: 0.5 });
        d.fn((r) => psi(r, D), { c: "orange", w: 2.4 });
        d.line(r0, 0, r0, k, { c: "orange", w: 1, dash: "3 3" });
        d.dot(r0, k, { c: "orange" });
        d.legend([{ label: L.psi, c: "orange" }, { label: L.psi2, c: "violet", dash: true }, { label: L.mseD, c: "guide", dash: true }]);
      }
      ro.set("r", FV.fmt(r0, 2)); ro.set("l", FV.fmt(y0, 3)); ro.set("q", FV.fmt(0.5 * r0 * r0, 3)); ro.set("d", FV.fmt(k, 3)); ro.set("s", String(psi2(r0, D)));
      p.legend([{ label: L.huber, c: "blue" }, { label: L.quad, c: "guide", dash: true }, { label: L.lin, c: "faint", dash: true }, { label: L.tangent, c: "orange" }, { label: L.zone, c: "teal", box: true }]);
    }
    p.onresize = draw; draw();
  });

  // 2. The pull ψ(r) and the weight ψ(r)/r of a point: MSE, MAE and Huber.
  FV.widget("huber-influence", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-6, 6], y: [-4.5, 4.5], xLabel: "r", yLabel: "ψ(r)", aspect: 0.8, title: L.pullTitle });
    const b = new FV.Plot(FV.col(w.stage), { x: [-6, 6], y: [0, 1.2], xLabel: "r", yLabel: "w(r)", aspect: 0.8, title: L.weightTitle });
    const sd = FV.ui.slider({ label: L.delta, min: 0.2, max: 3, step: 0.05, value: cfg.delta || 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sr = FV.ui.slider({ label: L.rOut, min: 0, max: 6, step: 0.05, value: cfg.r != null ? cfg.r : 4, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sd.el, sr.el);
    const ro = FV.ui.readout(w.readout, [{ key: "m", label: L.pullMse }, { key: "h", label: L.pullHub, c: "orange" }, { key: "w", label: L.weightHub, c: "orange" }]);
    function draw() {
      const D = sd.value, r = sr.value;
      a.clear();
      a.rect(-D, -4.5, D, 4.5, { c: "teal", opacity: 0.07 });
      a.fn((x) => x, { c: "guide", w: 1.8, dash: "6 5" });
      a.fn((x) => (x === 0 ? 0 : D * Math.sign(x)), { c: "teal", w: 1.6, dash: "3 4", jump: D });
      a.fn((x) => psi(x, D), { c: "orange", w: 2.6 });
      a.line(r, 0, r, Math.min(r, 4.5), { c: "guide", w: 1, dash: "3 3" });
      a.dot(r, Math.min(r, 4.5), { c: "guide", r: 4 }); a.dot(r, psi(r, D), { c: "orange" });
      a.legend([{ label: L.hubName, c: "orange" }, { label: L.mse, c: "guide", dash: true }, { label: L.mae, c: "teal", dash: true }]);
      b.clear();
      b.rect(-D, 0, D, 1.2, { c: "teal", opacity: 0.07 });
      b.hline(1, { c: "guide", w: 1.8, dash: "6 5" });
      b.fn((x) => D / Math.abs(x), { c: "teal", w: 1.6, dash: "3 4" });
      b.fn((x) => (Math.abs(x) <= D ? 1 : D / Math.abs(x)), { c: "orange", w: 2.6 });
      const wt = Math.abs(r) <= D ? 1 : D / Math.abs(r);
      b.line(r, 0, r, wt, { c: "orange", w: 1, dash: "3 3" });
      b.dot(r, wt, { c: "orange" });
      b.legend([{ label: L.hubName + ": min(1, δ/|r|)", c: "orange" }, { label: L.mse + ": 1", c: "guide", dash: true }, { label: "MAE·δ: δ/|r|", c: "teal", dash: true }]);
      ro.set("m", FV.fmt(r, 2)); ro.set("h", FV.fmt(psi(r, D), 2)); ro.set("w", FV.fmt(wt, 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 3. The surface L(r, δ) in 3D and its level lines from above.
  FV.widget("huber-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    let kind = "huber";
    const F = (r, d) => (kind === "huber" ? H(r, d) : PH(r, d));
    const s3 = new FV.Surface(FV.col(w.stage), { f: F, x: [-4, 4], y: [0.1, 3], z: [0, 7.5], n: 40, labels: { x: "r", y: "δ", z: "L" }, azimuth: -0.55, elevation: 0.5, aspect: 0.85, title: L.surfTitle });
    const m = new FV.Plot(FV.col(w.stage), { x: [-4, 4], y: [0.1, 3], xLabel: "r", aspect: 0.85, title: L.mapTitle });
    const sd = FV.ui.slider({ label: L.delta, min: 0.1, max: 3, step: 0.05, value: cfg.delta || 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sk = FV.ui.seg({ label: L.kind, value: kind, options: [{ value: "huber", label: L.hubName }, { value: "pseudo", label: L.pseudoName }], onchange: (v) => { kind = v; s3.setF(F); draw(); } });
    w.controls.append(sk.el, sd.el);
    const ro = FV.ui.readout(w.readout, [{ key: "a", label: L.at2, c: "blue" }, { key: "q", label: "½·2² =" }]);
    const ds = FV.linspace(0.1, 3, 60);
    function draw() {
      const D = sd.value;
      const paths = [{ pts: FV.linspace(-4, 4, 81).map((r) => [r, D, F(r, D)]), c: "blue", w: 3 }];
      if (kind === "huber") {
        paths.push({ pts: ds.map((d) => [d, d, 0.5 * d * d]), c: "orange", w: 2.2 });
        paths.push({ pts: ds.map((d) => [-d, d, 0.5 * d * d]), c: "orange", w: 2.2 });
      }
      s3.setPaths(paths);
      m.clear();
      m.heat((r, d) => F(r, d), { cmap: "viridis", z: [0, 7.5], res: 4, alpha: 0.85 });
      m.contours((r, d) => F(r, d), [0.25, 0.5, 1, 2, 3, 4, 5, 6], { style: () => ({ c: "ink", w: 1, opacity: 0.55 }) });
      if (kind === "huber") { m.line(0.1, 0.1, 3, 3, { c: "orange", w: 2.2 }); m.line(-0.1, 0.1, -3, 3, { c: "orange", w: 2.2 }); }
      m.hline(D, { c: "blue", w: 2.2, dash: false });
      m.legend([{ label: L.slice + FV.fmt(D, 2), c: "blue" }].concat(kind === "huber" ? [{ label: L.seam + " |r| = δ", c: "orange" }] : []));
      ro.set("a", FV.fmt(F(2, D), 3)); ro.set("q", "2");
    }
    m.onresize = draw; draw();
  });

  // Location sample: 13 clean values around 5 and two outliers (the last one is draggable).
  function sample() {
    const r = FV.rng(3), xs = [];
    for (let i = 0; i < 13; i++) xs.push(5 + r.normal());
    xs.push(11, 13.5);
    return xs;
  }
  const median = (a) => { const s = a.slice().sort((u, v) => u - v), n = s.length; return n % 2 ? s[(n - 1) / 2] : 0.5 * (s[n / 2 - 1] + s[n / 2]); };
  // Huber M-estimate of location: the root of Σ ψ(x_i − μ) = 0 (the sum is non-increasing in μ), by bisection.
  function huberLoc(xs, d) {
    let lo = Math.min(...xs), hi = Math.max(...xs);
    for (let it = 0; it < 80; it++) {
      const mid = 0.5 * (lo + hi);
      let s = 0; for (const x of xs) s += psi(x - mid, d);
      if (s > 0) lo = mid; else hi = mid;
    }
    return 0.5 * (lo + hi);
  }

  // 4. Huber's estimate of location: between the median (δ → 0) and the mean (δ → ∞).
  FV.widget("huber-location", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const xs = sample();
    const a = new FV.Plot(FV.col(w.stage), { x: [2, 15], y: [0, 1.25], xLabel: L.value, yLabel: L.weight, aspect: 0.62 });
    const b = new FV.Plot(FV.col(w.stage), { x: [0.02, 50], xType: "log", y: [4, 7], xLabel: "δ", aspect: 0.62, title: L.path });
    const sd = logSlider({ label: L.delta, min: 0.02, max: 50, value: cfg.delta || 1, fmt: (v) => FV.num(v, 2), oninput: draw });
    w.controls.append(sd.el);
    const ro = FV.ui.readout(w.readout, [{ key: "m", label: L.mean + " =" }, { key: "md", label: L.median + " =", c: "teal" }, { key: "h", label: "$\\hat\\mu$ =", c: "blue" }, { key: "z", label: L.inZone }]);
    const last = xs.length - 1;
    // the handle sits on the outlier's own weight bar, so the bar is not hidden behind it
    const wOf = (x, mu, D) => (Math.abs(x - mu) <= D ? 1 : D / Math.abs(x - mu));
    const hd = a.handle(xs[last], 0.1, { c: "red", label: L.outH, onDrag: (x) => { xs[last] = x; return [x, wOf(x, huberLoc(xs, sd.value), sd.value)]; }, onChange: () => draw() });
    const grid = FV.linspace(Math.log10(0.02), Math.log10(50), 140).map((v) => Math.pow(10, v));
    function draw() {
      const D = sd.value, mu = huberLoc(xs, D), mean = xs.reduce((s, v) => s + v, 0) / xs.length, med = median(xs);
      a.clear();
      a.rect(mu - D, 0, mu + D, 1.25, { c: "blue", opacity: 0.07 });
      a.vline(mean, { c: "guide", w: 1.4, dash: "6 5" });
      a.vline(med, { c: "teal", w: 1.4, dash: "3 4" });
      a.vline(mu, { c: "blue", w: 1.8, dash: false, opacity: 0.8 });
      let inZone = 0;
      xs.forEach((x, i) => {
        const wt = Math.abs(x - mu) <= D ? 1 : D / Math.abs(x - mu);
        if (Math.abs(x - mu) <= D) inZone++;
        a.line(x, 0, x, wt, { c: i >= 13 ? "red" : "ink", w: 1.4, opacity: 0.7 });
        a.dot(x, wt, { c: i >= 13 ? "red" : "ink", r: 4 });
      });
      hd.set(xs[last], wOf(xs[last], mu, D));
      a.legend([{ label: L.mean, c: "guide", dash: true }, { label: L.median, c: "teal", dash: true }, { label: L.est, c: "blue" }, { label: L.quadZone, c: "blue", box: true }]);
      const path = grid.map((d) => [d, huberLoc(xs, d)]);
      const ys = path.map((q) => q[1]).concat([mean, med]);
      const lo = Math.min(...ys), hi = Math.max(...ys), pad = Math.max(0.25, (hi - lo) * 0.15);
      b.setDomain(null, [lo - pad, hi + pad]);
      b.clear();
      b.hline(mean, { c: "guide", w: 1.6, dash: "6 5" });
      b.hline(med, { c: "teal", w: 1.6, dash: "3 4" });
      b.path(path, { c: "blue", w: 2.4 });
      b.dot(D, mu, { c: "blue" });
      b.text(0.022, mean, L.mean, { c: "faint", dy: -6 }); b.text(0.022, med, L.median, { c: "teal", dy: -6 });
      ro.set("m", FV.fmt(mean, 3)); ro.set("md", FV.fmt(med, 3)); ro.set("h", FV.fmt(mu, 3)); ro.set("z", inZone + " / " + xs.length);
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // Regression data: 30 points on y = 1 + 0.5x with noise 0.5, plus three outliers below the line.
  function regData() {
    const r = FV.rng(5), pts = [];
    for (let i = 0; i < 30; i++) { const x = 0.3 + (9.4 * i) / 29; pts.push({ x, y: 1 + 0.5 * x + 0.5 * r.normal(), out: false }); }
    [[7.6, 0.2], [8.4, 0.6], [9.2, 0.0]].forEach(([x, y]) => pts.push({ x, y, out: true }));
    return pts;
  }

  // 5. Gradient descent on a line: MSE versus Huber, with a draggable outlier.
  FV.widget("huber-regression", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const pts = regData();
    const a = new FV.Plot(FV.col(w.stage), { x: [0, 10], y: [-1.5, 7.5], xLabel: L.x, yLabel: L.y, aspect: 0.75 });
    const MAXS = 300;
    const b = new FV.Plot(FV.col(w.stage), { x: [0, MAXS], y: [-0.05, 0.65], xLabel: L.step, yLabel: L.slope, aspect: 0.75, title: L.slopeTitle });
    const sd = FV.ui.slider({ label: L.delta, min: 0.1, max: 4, step: 0.05, value: cfg.delta || 0.7, fmt: (v) => FV.fmt(v, 2), oninput: () => draw() });
    // the line is y = c + s·u with u = (x − 5)/3, so that both parameters train at a similar pace
    const lr = 0.15;
    let M, Hm, step, hist;
    function init() { M = { c: 0, s: 0 }; Hm = { c: 0, s: 0 }; step = 0; hist = [[0, 0, 0]]; }
    init();
    function gd(m, loss) {
      let gc = 0, gs = 0;
      pts.forEach((q) => { const u = (q.x - 5) / 3, r = q.y - (m.c + m.s * u), g = loss === "mse" ? r : psi(r, sd.value); gc -= g; gs -= g * u; });
      m.c -= (lr * gc) / pts.length; m.s -= (lr * gs) / pts.length;
      return Math.hypot(gc, gs) / pts.length;
    }
    const player = FV.ui.player({
      interval: 50,
      onstep() { const g1 = gd(M, "mse"), g2 = gd(Hm, "huber"); step++; hist.push([step, M.s / 3, Hm.s / 3]); draw(); return step < MAXS && Math.max(g1, g2) > 1e-5; },
      onreset() { const o = regData(); pts.forEach((q, i) => { q.x = o[i].x; q.y = o[i].y; }); init(); draw(); },
    });
    w.controls.append(sd.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.step + " =" }, { key: "m", label: L.slopeMse, c: "violet" }, { key: "h", label: L.slopeHub, c: "blue" }]);
    const last = pts.length - 1;
    const hd = a.handle(pts[last].x, pts[last].y, { c: "red", onDrag: (x, y) => { pts[last].x = x; pts[last].y = y; return [x, y]; }, onChange: () => draw() });
    const lineY = (m, x) => m.c + (m.s * (x - 5)) / 3;
    function draw() {
      a.clear();
      a.line(0, 1, 10, 6, { c: "guide", w: 1.4, dash: "6 5" });
      pts.forEach((q, i) => { if (i !== last) a.dot(q.x, q.y, { c: q.out ? "red" : "faint", r: 4 }); });
      a.line(0, lineY(M, 0), 10, lineY(M, 10), { c: "violet", w: 2.2, dash: "8 5" });
      a.line(0, lineY(Hm, 0), 10, lineY(Hm, 10), { c: "blue", w: 2.6 });
      hd.set(pts[last].x, pts[last].y);
      a.legend([{ label: L.lineHub, c: "blue" }, { label: L.lineMse, c: "violet", dash: true }, { label: L.truth, c: "guide", dash: true }, { label: L.outlier, c: "red", dot: true }]);
      b.clear();
      b.hline(0.5, { c: "guide", w: 1.4, dash: "6 5" });
      b.path(hist.map((h) => [h[0], h[1]]), { c: "violet", w: 2, dash: "8 5" });
      b.path(hist.map((h) => [h[0], h[2]]), { c: "blue", w: 2.4 });
      b.legend([{ label: L.lineHub, c: "blue" }, { label: L.lineMse, c: "violet", dash: true }, { label: L.trueSlope, c: "guide", dash: true }]);
      ro.set("s", String(step)); ro.set("m", FV.fmt(M.s / 3, 3)); ro.set("h", FV.fmt(Hm.s / 3, 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 6. Smooth relatives: pseudo-Huber, log-cosh, Smooth L1.
  FV.widget("huber-variants", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-4, 4], y: [-0.2, 4], xLabel: "r", yLabel: "L(r)", aspect: 0.75, title: L.lossT });
    const b = new FV.Plot(FV.col(w.stage), { x: [-4, 4], y: [-3.3, 3.3], xLabel: "r", yLabel: "L′(r)", aspect: 0.75, title: L.derT });
    let kind = cfg.variant || "pseudo";
    const sv = FV.ui.seg({ label: L.variant, value: kind, options: [{ value: "pseudo", label: L.pseudo }, { value: "logcosh", label: L.logcosh }, { value: "sl1", label: L.sl1 }], onchange: (v) => { kind = v; draw(); } });
    const sd = FV.ui.slider({ label: L.delta, min: 0.2, max: 3, step: 0.05, value: cfg.delta || 1, fmt: (v) => FV.fmt(v, 2), oninput: () => draw() });
    const sr = FV.ui.slider({ label: L.rPoint, min: -4, max: 4, step: 0.05, value: cfg.r != null ? cfg.r : 3, fmt: (v) => FV.fmt(v, 2), oninput: () => draw() });
    const s2 = FV.ui.check({ label: L.second, checked: false, onchange: () => draw() });
    w.controls.append(sv.el, sd.el, sr.el, s2.el);
    const ro = FV.ui.readout(w.readout, [{ key: "h", label: L.hubV, c: "blue" }, { key: "v", label: L.varV, c: "violet" }, { key: "hd", label: L.hubD, c: "orange" }, { key: "vd", label: L.varD, c: "violet" }]);
    function draw() {
      const D = sd.value, r = sr.value, V = VARIANTS[kind];
      a.clear();
      a.fn((x) => 0.5 * x * x, { c: "guide", w: 1.4, dash: "6 5" });
      a.fn((x) => H(x, D), { c: "blue", w: 2.6 });
      a.fn((x) => V.f(x, D), { c: "violet", w: 2.2, dash: "7 4" });
      a.dot(r, H(r, D), { c: "blue", r: 4 }); a.dot(r, V.f(r, D), { c: "violet", r: 4 });
      a.legend([{ label: L.hubName, c: "blue" }, { label: { pseudo: L.pseudo, logcosh: L.logcosh, sl1: L.sl1 }[kind], c: "violet", dash: true }, { label: "½r²", c: "guide", dash: true }]);
      const sec = s2.value;
      b.setDomain(null, sec ? [-0.1, 1.6] : [-3.3, 3.3]);
      b.o.yLabel = sec ? "L″(r)" : "L′(r)";
      b.clear();
      if (sec) {
        b.fn((x) => psi2(x, D), { c: "orange", w: 2.4, jump: 0.5 });
        b.fn((x) => V.d2(x, D), { c: "violet", w: 2.2, dash: "7 4", jump: 0.5 });
      } else {
        b.fn((x) => psi(x, D), { c: "orange", w: 2.4 });
        b.fn((x) => V.d(x, D), { c: "violet", w: 2.2, dash: "7 4" });
        b.dot(r, psi(r, D), { c: "orange", r: 4 }); b.dot(r, V.d(r, D), { c: "violet", r: 4 });
      }
      b.legend([{ label: L.hubName, c: "orange" }, { label: { pseudo: L.pseudo, logcosh: L.logcosh, sl1: L.sl1 }[kind], c: "violet", dash: true }]);
      ro.set("h", FV.fmt(H(r, D), 3)); ro.set("v", FV.fmt(V.f(r, D), 3)); ro.set("hd", FV.fmt(psi(r, D), 3)); ro.set("vd", FV.fmt(V.d(r, D), 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 7. Choosing δ: asymptotic variance of Huber's location estimate under a contaminated normal
  //    (1 − ε)·N(0, 1) + ε·N(0, 10²); k = δ/σ.
  const TAU = 10;
  function Epsi2(k, tau) { const c = k / tau; return tau * tau * (2 * FV.Phi(c) - 1 - 2 * c * FV.phi(c)) + 2 * k * k * (1 - FV.Phi(c)); }
  const Edpsi = (k, tau) => 2 * FV.Phi(k / tau) - 1;
  const varHub = (k, e) => ((1 - e) * Epsi2(k, 1) + e * Epsi2(k, TAU)) / ((1 - e) * Edpsi(k, 1) + e * Edpsi(k, TAU)) ** 2;
  FV.widget("huber-efficiency", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0, 3], y: [0.9, 2.8], xLabel: L.kAxis, yLabel: L.vAxis, aspect: 0.5 });
    const sk = FV.ui.slider({ label: L.k, min: 0.05, max: 3, step: 0.005, value: cfg.k || 1.345, fmt: (v) => FV.fmt(v, 3), oninput: draw });
    const se = FV.ui.slider({ label: L.eps, min: 0, max: 0.25, step: 0.01, value: cfg.eps != null ? cfg.eps : 0.05, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sk.el, se.el);
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.eff, c: "faint" }, { key: "v", label: L.varNow, c: "blue" }, { key: "m", label: L.vMean + " =" }, { key: "md", label: L.vMed + " =", c: "teal" }, { key: "b", label: L.best }]);
    function draw() {
      const k = sk.value, e = se.value;
      const f0 = ((1 - e) + e / TAU) * FV.phi(0), vMed = 1 / (4 * f0 * f0), vMean = 1 - e + e * TAU * TAU;
      let best = 0.05, bv = Infinity;
      for (let i = 0; i <= 590; i++) { const kk = 0.05 + i * 0.005, v = varHub(kk, e); if (v < bv) { bv = v; best = kk; } }
      p.clear();
      p.hline(vMed, { c: "teal", w: 1.6, dash: "3 4" });
      if (vMean <= 2.8) p.hline(vMean, { c: "guide", w: 1.6, dash: "6 5" });
      else p.text(2.95, 2.68, L.meanOff + FV.fmt(vMean, 2) + " ↑", { c: "faint", anchor: "end" });
      p.fn((x) => varHub(Math.max(x, 0.01), 0), { c: "faint", w: 1.4, dash: "2 4", from: 0.05 });
      p.fn((x) => varHub(Math.max(x, 0.01), e), { c: "blue", w: 2.6, from: 0.05 });
      p.vline(k, { c: "ink", opacity: 0.6 });
      p.dot(k, varHub(k, e), { c: "blue" });
      if (best < 2.99) p.dot(best, bv, { c: "ink", hollow: true, r: 5 });
      p.legend([{ label: L.vHub, c: "blue" }, { label: L.vClean, c: "faint", dash: true }, { label: L.vMed, c: "teal", dash: true }, { label: L.vMean, c: "guide", dash: true }]);
      ro.set("e", FV.fmt(100 / varHub(k, 0), 1) + "%"); ro.set("v", FV.fmt(varHub(k, e), 3)); ro.set("m", FV.fmt(vMean, 2)); ro.set("md", FV.fmt(vMed, 3));
      ro.set("b", best < 2.99 ? FV.fmt(best, 2) : "→ ∞");
    }
    p.onresize = draw; draw();
  });
})();
