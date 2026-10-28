/* Widgets of the formula page "MAE". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      obj: "объект i", y: "y", truth: "истинное y", yhat: "прогноз ŷ (тяните)", err: "ошибка e = y − ŷ", abs: "|e|",
      errs: "$|e_i|$ =", sum: "$\\sum|e_i|$ =", mae: "MAE =", meanLine: "среднее |e| = MAE",
      c: "прогноз-константа c", maec: "MAE(c)", dmaec: "∂MAE/∂c", median: "медиана", medians: "медианы", mean: "среднее", data: "данные yᵢ",
      sample: "Выборка", cval: "$c$ =", slope: "наклон =", med: "медиана =", avg: "среднее =", sub: "субградиент", zeroIn: "0 ∈ ∂MAE",
      flat: "Любое $c$ из отрезка $[5;\\,9]$ даёт один и тот же минимум MAE = 4,5: при чётном $n$ медиана не единственна.",
      e: "e", loss: "потеря", deriv: "производная", tangent: "касательная", fan: "субградиенты в 0", cmp: "Сравнить с MSE ($e^2$ и $2e$)",
      eVal: "$e$ =", absVal: "$|e|$ =", dAbs: "$\\partial|e|/\\partial e$ =", sq: "$e^2$ =", dsq: "$2e$ =", subdiff: "∂|e|(0) = [−1; 1]", sqName: "e² (MSE)", dsqName: "2e (MSE)",
      x: "x", lineMAE: "прямая по MAE", lineMSE: "прямая по MSE", outlier: "выброс (тяните)", points: "данные", resid: "Показать остатки",
      slMAE: "наклон MAE =", slMSE: "наклон MSE =", gMAE: "вклад выброса в $|\\partial/\\partial b|$: MAE", gMSE: "MSE",
      w: "w", b: "b", which: "Потеря", surfMAE: "MAE(w, b)", surfMSE: "MSE(w, b)", top: "вид сверху", line: "текущая прямая", best: "оптимум", crease: "сгибы yᵢ = w·xᵢ + b",
      wv: "$w$ =", bv: "$b$ =", val: "значение =", min: "минимум =",
      eta: "Шаг $\\eta$", iter: "итерация t", constS: "постоянный шаг η", decS: "убывающий шаг η/√(t+1)", opt: "MAE* (оптимум)",
      tv: "$t$ =", mc: "MAE, постоянный =", md: "MAE, убывающий =", ms: "MAE* =", path: "траектории", excess: "превышение над оптимумом (лог. шкала)", startP: "старт",
      tau: "Квантиль $\\tau$", pin: "ρτ(e)", half: "½|e| (τ = 0,5)", ql: "прямая τ-квантиля", qref: "τ = 0,1 · 0,5 · 0,9", below: "ниже прямой =", under: "точки ниже прямой", on: "на прямой =",
      qloss: "пинбол-потеря", slopeR: "наклон τ", slopeL: "наклон τ − 1",
    },
    en: {
      obj: "object i", y: "y", truth: "true y", yhat: "prediction ŷ (drag)", err: "error e = y − ŷ", abs: "|e|",
      errs: "$|e_i|$ =", sum: "$\\sum|e_i|$ =", mae: "MAE =", meanLine: "mean |e| = MAE",
      c: "constant prediction c", maec: "MAE(c)", dmaec: "∂MAE/∂c", median: "median", medians: "medians", mean: "mean", data: "data yᵢ",
      sample: "Sample", cval: "$c$ =", slope: "slope =", med: "median =", avg: "mean =", sub: "subgradient", zeroIn: "0 ∈ ∂MAE",
      flat: "Any $c$ in $[5,\\,9]$ gives the same minimum MAE = 4.5: for even $n$ the median is not unique.",
      e: "e", loss: "loss", deriv: "derivative", tangent: "tangent", fan: "subgradients at 0", cmp: "Compare with MSE ($e^2$ and $2e$)",
      eVal: "$e$ =", absVal: "$|e|$ =", dAbs: "$\\partial|e|/\\partial e$ =", sq: "$e^2$ =", dsq: "$2e$ =", subdiff: "∂|e|(0) = [−1, 1]", sqName: "e² (MSE)", dsqName: "2e (MSE)",
      x: "x", lineMAE: "MAE line", lineMSE: "MSE line", outlier: "outlier (drag)", points: "data", resid: "Show residuals",
      slMAE: "MAE slope =", slMSE: "MSE slope =", gMAE: "outlier’s share of $|\\partial/\\partial b|$: MAE", gMSE: "MSE",
      w: "w", b: "b", which: "Loss", surfMAE: "MAE(w, b)", surfMSE: "MSE(w, b)", top: "view from above", line: "current line", best: "optimum", crease: "creases yᵢ = w·xᵢ + b",
      wv: "$w$ =", bv: "$b$ =", val: "value =", min: "minimum =",
      eta: "Step $\\eta$", iter: "iteration t", constS: "constant step η", decS: "decaying step η/√(t+1)", opt: "MAE* (optimum)",
      tv: "$t$ =", mc: "MAE, constant =", md: "MAE, decaying =", ms: "MAE* =", path: "trajectories", excess: "excess over the optimum (log scale)", startP: "start",
      tau: "Quantile $\\tau$", pin: "ρτ(e)", half: "½|e| (τ = 0.5)", ql: "τ-quantile line", qref: "τ = 0.1 · 0.5 · 0.9", below: "below the line =", under: "points below the line", on: "on the line =",
      qloss: "pinball loss", slopeR: "slope τ", slopeL: "slope τ − 1",
    },
    uz: {
      obj: "obyekt i", y: "y", truth: "haqiqiy y", yhat: "bashorat ŷ (torting)", err: "xato e = y − ŷ", abs: "|e|",
      errs: "$|e_i|$ =", sum: "$\\sum|e_i|$ =", mae: "MAE =", meanLine: "o‘rtacha |e| = MAE",
      c: "o‘zgarmas bashorat c", maec: "MAE(c)", dmaec: "∂MAE/∂c", median: "mediana", medians: "medianalar", mean: "o‘rtacha", data: "ma’lumot yᵢ",
      sample: "Tanlanma", cval: "$c$ =", slope: "qiyalik =", med: "mediana =", avg: "o‘rtacha =", sub: "subgradiyent", zeroIn: "0 ∈ ∂MAE",
      flat: "$[5;\\,9]$ kesmadagi istalgan $c$ bir xil minimum MAE = 4,5 ni beradi: juft $n$ da mediana yagona emas.",
      e: "e", loss: "yo‘qotish", deriv: "hosila", tangent: "urinma", fan: "0 dagi subgradiyentlar", cmp: "MSE bilan solishtirish ($e^2$ va $2e$)",
      eVal: "$e$ =", absVal: "$|e|$ =", dAbs: "$\\partial|e|/\\partial e$ =", sq: "$e^2$ =", dsq: "$2e$ =", subdiff: "∂|e|(0) = [−1; 1]", sqName: "e² (MSE)", dsqName: "2e (MSE)",
      x: "x", lineMAE: "MAE bo‘yicha to‘g‘ri chiziq", lineMSE: "MSE bo‘yicha to‘g‘ri chiziq", outlier: "chetga chiquvchi nuqta (torting)", points: "ma’lumot", resid: "Qoldiqlarni ko‘rsatish",
      slMAE: "MAE qiyaligi =", slMSE: "MSE qiyaligi =", gMAE: "chetga chiquvchi nuqtaning $|\\partial/\\partial b|$ dagi hissasi: MAE", gMSE: "MSE",
      w: "w", b: "b", which: "Yo‘qotish", surfMAE: "MAE(w, b)", surfMSE: "MSE(w, b)", top: "yuqoridan ko‘rinish", line: "joriy to‘g‘ri chiziq", best: "optimum", crease: "bukilishlar yᵢ = w·xᵢ + b",
      wv: "$w$ =", bv: "$b$ =", val: "qiymat =", min: "minimum =",
      eta: "Qadam $\\eta$", iter: "iteratsiya t", constS: "o‘zgarmas qadam η", decS: "kamayuvchi qadam η/√(t+1)", opt: "MAE* (optimum)",
      tv: "$t$ =", mc: "MAE, o‘zgarmas =", md: "MAE, kamayuvchi =", ms: "MAE* =", path: "trayektoriyalar", excess: "optimumdan ortiqcha (log. shkala)", startP: "start",
      tau: "Kvantil $\\tau$", pin: "ρτ(e)", half: "½|e| (τ = 0,5)", ql: "τ-kvantil to‘g‘ri chizig‘i", qref: "τ = 0,1 · 0,5 · 0,9", below: "chiziqdan pastda =", under: "chiziqdan pastdagi nuqtalar", on: "chiziq ustida =",
      qloss: "pinbol yo‘qotish", slopeR: "qiyalik τ", slopeL: "qiyalik τ − 1",
    },
  }[FV.lang] || {};
  const SEP = FV.lang === "en" ? ", " : "; ";
  const f1 = (v) => FV.fmt(v, 1).replace(/[.,]0$/, "");
  const sgn = (v) => (v > 0 ? 1 : v < 0 ? -1 : 0);

  // Best line under the pinball loss (τ = 0.5 gives MAE). The LP optimum passes through two data points,
  // so trying every pair is exact; ties keep the first pair met.
  function fitPin(X, Y, tau) {
    const n = X.length;
    let best = null;
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      if (X[i] === X[j]) continue;
      const w = (Y[j] - Y[i]) / (X[j] - X[i]), b = Y[i] - w * X[i];
      let v = 0;
      for (let k = 0; k < n; k++) { const r = Y[k] - w * X[k] - b; v += r >= 0 ? tau * r : (tau - 1) * r; }
      if (!best || v < best.v - 1e-12) best = { w, b, v };
    }
    best.v /= n;
    return best;
  }
  function fitOLS(X, Y) {
    const n = X.length, mx = X.reduce((s, v) => s + v, 0) / n, my = Y.reduce((s, v) => s + v, 0) / n;
    let sxy = 0, sxx = 0;
    for (let i = 0; i < n; i++) { sxy += (X[i] - mx) * (Y[i] - my); sxx += (X[i] - mx) ** 2; }
    const w = sxy / sxx;
    return { w, b: my - w * mx };
  }
  const maeOf = (X, Y, w, b) => X.reduce((s, x, i) => s + Math.abs(Y[i] - w * x - b), 0) / X.length;
  const mseOf = (X, Y, w, b) => X.reduce((s, x, i) => s + (Y[i] - w * x - b) ** 2, 0) / X.length;

  // 1. The running example: drag the predictions, watch the error segments and the V of |e|.
  FV.widget("mae-errors", (el, cfg) => {
    const w = FV.shell(el, {});
    const Y = [3, 5, 8], P = (cfg.yhat || [2.5, 5, 10]).slice();
    const p = new FV.Plot(w.stage, { x: [0.4, 3.6], y: [0, 12], xLabel: L.obj, yLabel: "y, ŷ", aspect: 0.5, xTicks: [1, 2, 3].map((v) => ({ v, label: "i = " + v })) });
    const q = new FV.Plot(w.stage, { x: [-6, 6], y: [0, 6.5], xLabel: L.err, yLabel: L.abs, aspect: 0.32, minHeight: 190, maxHeight: 250 });
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.errs }, { key: "s", label: L.sum }, { key: "m", label: L.mae, c: "orange" }]);
    const hs = P.map((v, i) => p.handle(i + 1, v, { c: "blue", label: "ŷ" + (i + 1), onDrag: (x, y) => [i + 1, Math.round(y * 10) / 10], onChange: (x, y) => { P[i] = y; draw(); } }));
    function draw() {
      const E = Y.map((y, i) => y - P[i]), A = E.map(Math.abs), m = A.reduce((s, v) => s + v, 0) / 3;
      p.clear();
      Y.forEach((y, i) => {
        const x = i + 1;
        p.line(x, y, x, P[i], { c: "orange", w: 3.2 });
        if (A[i] > 0.05) p.text(x, (y + P[i]) / 2, "|e" + "₁₂₃"[i] + "| = " + f1(A[i]), { c: "orange", dx: 18, dy: 4 });
        const tk = (13 * 3.2) / (p.x1 - p.x0);
        p.line(x - tk, y, x + tk, y, { c: "ink", w: 2.5 });
        p.dot(x, y, { c: "ink", r: 4.5 });
      });
      hs.forEach((h, i) => h.set(i + 1, P[i]));
      p.legend([{ label: L.truth, c: "ink", dot: true }, { label: L.yhat, c: "blue", dot: true }, { label: "|e| = |y − ŷ|", c: "orange" }]);
      q.clear();
      q.area((e) => Math.abs(e), null, { c: "orange", fillOpacity: 0.07 });
      q.fn((e) => Math.abs(e), { c: "orange", w: 2.4 });
      q.hline(m, { c: "teal", dash: "5 4", w: 1.6 });
      E.forEach((e, i) => {
        q.line(e, 0, e, A[i], { c: "orange", w: 1, dash: "3 3" });
        q.dot(e, A[i], { c: "orange", r: 5 });
        q.text(e, A[i], String(i + 1), { c: "ink", dx: 7, dy: -8 });
      });
      q.legend([{ label: "|e|", c: "orange" }, { label: L.meanLine + " = " + FV.fmt(m, 3), c: "teal", dash: true }]);
      ro.set("e", "(" + A.map(f1).join(SEP) + ")");
      ro.set("s", f1(A.reduce((s, v) => s + v, 0)));
      ro.set("m", FV.fmt(m, 3));
    }
    p.onresize = draw; q.onresize = draw; draw();
  });

  // 2. The best constant under MAE is the median: MAE(c) is piecewise linear with kinks at the data.
  FV.widget("mae-median", (el, cfg) => {
    const w = FV.shell(el, {});
    const SETS = { 5: [2, 3, 5, 9, 16], 6: [2, 3, 5, 9, 12, 16] };
    let D = SETS[cfg.n || 5], c = cfg.c != null ? cfg.c : 10;
    const f = (x) => D.reduce((s, y) => s + Math.abs(y - x), 0) / D.length;
    const g = (x) => D.reduce((s, y) => s + (y < x ? 1 : y > x ? -1 : 0), 0) / D.length;
    const p = new FV.Plot(w.stage, { x: [0, 18], y: [0, 12], xLabel: L.c, yLabel: L.maec, aspect: 0.48 });
    const d = new FV.Plot(w.stage, { x: [0, 18], y: [-1.25, 1.25], xLabel: L.c, yLabel: L.dmaec, aspect: 0.26, minHeight: 170, maxHeight: 220, yTicks: [-1, -0.5, 0, 0.5, 1].map((v) => ({ v, label: FV.fmt(v, v % 1 ? 1 : 0) })) });
    const seg = FV.ui.seg({ label: L.sample, value: cfg.n || 5, options: [{ value: 5, label: "n = 5" }, { value: 6, label: "n = 6" }], onchange: (v) => { D = SETS[v]; draw(); } });
    w.controls.append(seg.el);
    const ro = FV.ui.readout(w.readout, [{ key: "c", label: L.cval }, { key: "m", label: L.maec + " =", c: "orange" }, { key: "s", label: L.slope }, { key: "md", label: L.med, c: "teal" }, { key: "a", label: L.avg }]);
    const h = p.handle(c, f(c), { c: "blue", label: "c", onDrag: (x) => { c = Math.round(x * 20) / 20; return [c, f(c)]; }, onChange: () => draw() });
    function draw() {
      const n = D.length, s = D.slice().sort((a, b) => a - b);
      const lo = s[(n - 1) >> 1], hi = s[n >> 1], mean = D.reduce((a, b) => a + b, 0) / n;
      p.clear(); d.clear();
      D.forEach((y) => { p.vline(y, { c: "guide", dash: "2 4" }); d.vline(y, { c: "guide", dash: "2 4" }); });
      if (hi > lo) { p.rect(lo, 0, hi, 12, { c: "teal", opacity: 0.1 }); d.rect(lo, -1.25, hi, 1.25, { c: "teal", opacity: 0.1 }); }
      else { p.vline(lo, { c: "teal", dash: false, w: 1.6 }); }
      p.vline(mean, { c: "faint", dash: "6 4", w: 1.4 });
      p.text(lo, 9.6, hi > lo ? L.medians : L.median, { c: "teal", anchor: "end", dx: -5 });
      p.text(mean, 8.5, L.mean, { c: "faint", dx: 5 });
      p.fn(f, { c: "orange", w: 2.6 });
      D.forEach((y) => p.dot(y, 0.25, { c: "ink", r: 5 }));
      p.line(c, 0, c, f(c), { c: "blue", w: 1, dash: "3 3" });
      h.set(c, f(c));
      p.legend([{ label: L.maec, c: "orange" }, { label: L.data, c: "ink", dot: true }, { label: hi > lo ? L.medians : L.median, c: "teal", box: hi > lo }, { label: L.mean, c: "faint", dash: true }]);
      // the subgradient: a step function, a whole interval at each data point
      d.hline(0, { c: "guide", dash: false });
      for (let k = 0; k <= n; k++) {
        const a = k === 0 ? 0 : s[k - 1], b = k === n ? 18 : s[k], v = (2 * k - n) / n;
        d.line(a, v, b, v, { c: "orange", w: 2.4 });
        if (k < n) { d.line(s[k], v, s[k], (2 * k + 2 - n) / n, { c: "orange", w: 1.2, opacity: 0.6 }); }
      }
      if (hi === lo) d.line(lo, -1 / n, lo, 1 / n, { c: "teal", w: 4 });
      d.dot(c, g(c), { c: "blue", r: 4.5 });
      const onKink = D.some((y) => Math.abs(y - c) < 1e-9);
      ro.set("c", FV.fmt(c, 2)); ro.set("m", FV.fmt(f(c), 3));
      if (onKink) {
        const k = s.filter((y) => y < c).length, e = s.filter((y) => y === c).length;
        ro.set("s", "[" + FV.fmt((2 * k - n) / n, 2) + SEP + FV.fmt((2 * (k + e) - n) / n, 2) + "]");
      } else ro.set("s", FV.fmt(g(c), 2));
      ro.set("md", hi > lo ? "[" + FV.fmt(lo, 0) + SEP + FV.fmt(hi, 0) + "]" : FV.fmt(lo, 0)); ro.set("a", FV.fmt(mean, 2));
      w.note.textContent = "";
      if (hi > lo) w.note.append(FV.rich(L.flat));
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 3. |e| and its (sub)derivative sign(e), compared with e² and 2e.
  FV.widget("mae-derivative", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-3, 3], y: [-0.6, 3.4], xLabel: L.err, yLabel: L.loss, aspect: 0.8, title: "|e|" });
    const b = new FV.Plot(FV.col(w.stage), { x: [-3, 3], y: [-3.4, 3.4], xLabel: L.err, yLabel: L.deriv, aspect: 0.8, title: "∂|e|/∂e = sign(e)" });
    let e = cfg.e != null ? cfg.e : 1.5;
    const cmp = FV.ui.check({ label: L.cmp, checked: !!cfg.compare, onchange: draw });
    w.controls.append(cmp.el);
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.eVal }, { key: "a", label: L.absVal, c: "orange" }, { key: "d", label: L.dAbs, c: "orange" }, { key: "s", label: L.sq }, { key: "ds", label: L.dsq }]);
    const h = a.handle(e, Math.abs(e), { c: "blue", label: "e", onDrag: (x) => { e = Math.abs(x) < 0.08 ? 0 : Math.round(x * 100) / 100; return [e, Math.abs(e)]; }, onChange: () => draw() });
    function draw() {
      a.clear(); b.clear();
      a.hline(0, { c: "guide", dash: false }); b.hline(0, { c: "guide", dash: false });
      if (cmp.value) { a.fn((x) => x * x, { c: "guide", w: 1.8, dash: "6 4" }); b.fn((x) => 2 * x, { c: "guide", w: 1.8, dash: "6 4" }); }
      a.fn((x) => Math.abs(x), { c: "orange", w: 2.6 });
      if (e === 0) {
        [-1, -0.5, 0, 0.5, 1].forEach((k) => a.line(-2, -2 * k, 2, 2 * k, { c: "ink", w: 1.2, opacity: 0.45 }));
      } else {
        const k = sgn(e);
        a.line(e - 4, Math.abs(e) - 4 * k, e + 4, Math.abs(e) + 4 * k, { c: "ink", w: 1.5, dash: "5 4" });
      }
      h.set(e, Math.abs(e));
      a.legend([{ label: "|e|", c: "orange" }, { label: e === 0 ? L.fan : L.tangent, c: "ink", dash: e !== 0 }].concat(cmp.value ? [{ label: L.sqName, c: "guide", dash: true }] : []));
      // derivative: −1 on the left, +1 on the right, the whole segment [−1, 1] at zero
      b.line(-3, -1, 0, -1, { c: "orange", w: 2.6 }); b.line(0, 1, 3, 1, { c: "orange", w: 2.6 });
      b.line(0, -1, 0, 1, { c: "orange", w: 5, opacity: 0.35 });
      b.dot(0, -1, { c: "orange", hollow: true, r: 4.5 }); b.dot(0, 1, { c: "orange", hollow: true, r: 4.5 });
      b.text(0.18, 0.45, L.subdiff, { c: "orange" });
      if (e !== 0) b.dot(e, sgn(e), { c: "blue", r: 5.5 });
      else b.dot(0, 0, { c: "blue", r: 5.5 });
      b.legend([{ label: "sign(e)", c: "orange" }].concat(cmp.value ? [{ label: L.dsqName, c: "guide", dash: true }] : []));
      ro.set("e", FV.fmt(e, 2)); ro.set("a", FV.fmt(Math.abs(e), 2));
      ro.set("d", e === 0 ? "[−1" + SEP + "1]" : FV.fmt(sgn(e), 0)); ro.set("s", FV.fmt(e * e, 2)); ro.set("ds", FV.fmt(2 * e, 2));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 4. One draggable outlier against a MAE line and a MSE line.
  const OX = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5], OY = [1.55, 1.35, 2.45, 3.25, 2.95, 3.85, 3.75, 5.15, 5.05, 6.05];
  FV.widget("mae-outlier", (el, cfg) => {
    const w = FV.shell(el, {});
    let yo = cfg.y != null ? cfg.y : 0;
    const p = new FV.Plot(w.stage, { x: [0, 10], y: [-5, 13], xLabel: L.x, yLabel: "y", aspect: 0.55 });
    const res = FV.ui.check({ label: L.resid, checked: cfg.residuals !== false, onchange: draw });
    w.controls.append(res.el);
    const ro = FV.ui.readout(w.readout, [{ key: "a", label: L.slMAE, c: "blue" }, { key: "s", label: L.slMSE }, { key: "ga", label: L.gMAE }, { key: "gs", label: L.gMSE }]);
    const h = p.handle(9, yo, { c: "red", label: L.outlier, onDrag: (x, y) => { yo = Math.round(y * 10) / 10; return [9, yo]; }, onChange: () => draw() });
    function draw() {
      const X = OX.concat([9]), Y = OY.concat([yo]), n = X.length;
      const m = fitPin(X, Y, 0.5), o = fitOLS(X, Y);
      p.clear();
      if (res.value) X.forEach((x, i) => p.line(x, Y[i], x, m.w * x + m.b, { c: "orange", w: 1.4, opacity: 0.75 }));
      p.fn((x) => o.w * x + o.b, { c: "guide", w: 2.2, dash: "7 5" });
      p.fn((x) => m.w * x + m.b, { c: "blue", w: 2.6 });
      OX.forEach((x, i) => p.dot(x, OY[i], { c: "ink", r: 4.5 }));
      h.set(9, yo);
      p.legend([{ label: L.points, c: "ink", dot: true }, { label: L.outlier, c: "red", dot: true }, { label: L.lineMAE, c: "blue" }, { label: L.lineMSE, c: "guide", dash: true }].concat(res.value ? [{ label: "|e|", c: "orange" }] : []));
      ro.set("a", FV.fmt(m.w, 3)); ro.set("s", FV.fmt(o.w, 3));
      const r = yo - (o.w * 9 + o.b);
      ro.set("ga", FV.fmt(Math.abs(yo - (m.w * 9 + m.b)) < 1e-9 ? 0 : 1 / n, 3)); ro.set("gs", FV.fmt((2 * Math.abs(r)) / n, 3));
    }
    p.onresize = draw; draw();
  });

  // The small line-fit problem used by the surface and the descent: centred x.
  const SX = [-2, -1, 0, 1, 2], SY = [1.3, 2.0, 3.1, 4.5, 7.0];
  const lossMAE = (w, b) => maeOf(SX, SY, w, b), lossMSE = (w, b) => mseOf(SX, SY, w, b);

  // 5. The MAE surface over (w, b): a polyhedron with creases, versus the smooth MSE bowl.
  FV.widget("mae-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const W = [-1, 3.5], B = [0.5, 6];
    let kind = cfg.loss || "mae", P = { w: cfg.w != null ? cfg.w : 0.4, b: cfg.b != null ? cfg.b : 1.8 };
    const F = () => (kind === "mae" ? lossMAE : lossMSE);
    const lad = fitPin(SX, SY, 0.5), ols = fitOLS(SX, SY);
    const s3 = new FV.Surface(FV.col(w.stage), { f: F(), x: W, y: B, n: 44, labels: { x: "w", y: "b", z: "MAE" }, azimuth: -0.55, elevation: 0.5, aspect: 0.95, title: L.surfMAE });
    const right = FV.col(w.stage);
    const c2 = new FV.Plot(right, { x: W, y: B, xLabel: "w", yLabel: "b", aspect: 0.78, title: L.top });
    const dp = new FV.Plot(right, { x: [-2.6, 2.6], y: [0, 8.5], xLabel: "x", yLabel: "y", aspect: 0.5, minHeight: 170, maxHeight: 230, title: L.line });
    const seg = FV.ui.seg({ label: L.which, value: kind, options: [{ value: "mae", label: "MAE" }, { value: "mse", label: "MSE" }], onchange: (v) => { kind = v; s3.o.labels.z = v.toUpperCase(); s3.wrap.firstChild.textContent = v === "mae" ? L.surfMAE : L.surfMSE; s3.setF(F()); draw(); } });
    w.controls.append(seg.el);
    const ro = FV.ui.readout(w.readout, [{ key: "w", label: L.wv }, { key: "b", label: L.bv }, { key: "v", label: L.val, c: "blue" }, { key: "m", label: L.min, c: "red" }]);
    const h = c2.handle(P.w, P.b, { c: "blue", label: "(w, b)", onChange: (x, y) => { P.w = x; P.b = y; draw(); } });
    const LV = { mae: [0.45, 0.6, 0.8, 1.05, 1.35, 1.7, 2.1, 2.6, 3.2], mse: [0.3, 0.6, 1.2, 2.2, 3.6, 5.5, 8, 11, 15] };
    function draw() {
      const f = F(), best = kind === "mae" ? { w: lad.w, b: lad.b } : ols, fb = f(best.w, best.b);
      c2.clear();
      c2.heat(f, { cmap: "blues", res: 4, alpha: 0.8, transform: Math.sqrt });
      c2.contours(f, LV[kind], { c: "ink", w: 1, opacity: 0.4 });
      if (kind === "mae") SX.forEach((x, i) => c2.line(W[0], SY[i] - x * W[0], W[1], SY[i] - x * W[1], { c: "orange", w: 1.3, dash: "5 4", opacity: 0.9 }));
      c2.dot(best.w, best.b, { c: "red", r: 5.5 });
      h.set(P.w, P.b);
      c2.legend([{ label: L.best, c: "red", dot: true }, { label: "(w, b)", c: "blue", dot: true }].concat(kind === "mae" ? [{ label: L.crease, c: "orange", dash: true }] : []));
      s3.setPoints([{ x: best.w, y: best.b, z: fb, c: "red", r: 5 }, { x: P.w, y: P.b, z: f(P.w, P.b), c: "blue", r: 6 }]);
      dp.clear();
      dp.fn((x) => best.w * x + best.b, { c: "red", w: 1.6, dash: "6 4" });
      SX.forEach((x, i) => dp.line(x, SY[i], x, P.w * x + P.b, { c: "orange", w: 1.3, opacity: 0.8 }));
      dp.fn((x) => P.w * x + P.b, { c: "blue", w: 2.4 });
      SX.forEach((x, i) => dp.dot(x, SY[i], { c: "ink", r: 4.5 }));
      ro.set("w", FV.fmt(P.w, 2)); ro.set("b", FV.fmt(P.b, 2)); ro.set("v", FV.fmt(f(P.w, P.b), 3)); ro.set("m", FV.fmt(fb, 3));
    }
    c2.onresize = draw; dp.onresize = draw; draw();
  });

  // 6. Subgradient descent on MAE(w, b): a constant step keeps bouncing, a decaying step settles.
  FV.widget("mae-descent", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const W = [-0.8, 2.2], B = [0.2, 4.2], T = 200, start = [-0.5, 0.5], FLOOR = 1e-4;
    const lad = fitPin(SX, SY, 0.5);
    const c2 = new FV.Plot(FV.col(w.stage), { x: W, y: B, xLabel: "w", yLabel: "b", aspect: 0.95, title: L.path });
    const lp = new FV.Plot(FV.col(w.stage), { x: [0, T], y: [FLOOR, 10], yType: "log", xLabel: L.iter, yLabel: "MAE − MAE*", aspect: 0.95, title: L.excess });
    const se = FV.ui.slider({ label: L.eta, min: 0.05, max: 0.8, step: 0.05, value: cfg.eta || 0.2, fmt: (v) => FV.fmt(v, 2), oninput: () => { run(); draw(); } });
    let t = cfg.t != null ? cfg.t : T, runs = null;
    const player = FV.ui.player({ interval: 45, onstep() { if (t >= T) t = 0; t = Math.min(T, t + 1); draw(); return t < T; }, onreset() { t = 0; draw(); } });
    w.controls.append(se.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.tv }, { key: "c", label: L.mc, c: "orange" }, { key: "d", label: L.md, c: "teal" }, { key: "m", label: L.ms }]);
    function run() {
      const eta = se.value;
      runs = [false, true].map((decay) => {
        let a = start[0], b = start[1];
        const pts = [[a, b]], vals = [lossMAE(a, b)];
        for (let k = 0; k < T; k++) {
          let gw = 0, gb = 0;
          SX.forEach((x, i) => { const s = sgn(SY[i] - a * x - b); gw -= s * x; gb -= s; });
          gw /= SX.length; gb /= SX.length;
          const st = decay ? eta / Math.sqrt(k + 1) : eta;
          a -= st * gw; b -= st * gb;
          pts.push([a, b]); vals.push(lossMAE(a, b));
        }
        return { pts, vals };
      });
    }
    function draw() {
      c2.clear();
      c2.heat(lossMAE, { cmap: "blues", res: 4, alpha: 0.8, transform: Math.sqrt });
      c2.contours(lossMAE, [0.45, 0.6, 0.8, 1.05, 1.35, 1.7, 2.1, 2.6], { c: "ink", w: 1, opacity: 0.4 });
      const cols = ["orange", "teal"];
      [1, 0].forEach((k) => {
        const r = runs[k];
        c2.path(r.pts.slice(0, t + 1), { c: cols[k], w: k ? 2.2 : 1.6 });
        const q = r.pts[t]; c2.dot(q[0], q[1], { c: cols[k], r: 5 });
      });
      c2.dot(start[0], start[1], { c: "ink", hollow: true, r: 4.5 });
      c2.dot(lad.w, lad.b, { c: "red", r: 5 });
      c2.legend([{ label: L.best, c: "red", dot: true }, { label: L.startP, c: "ink", dot: true }]);
      lp.clear();
      const ex = (v) => Math.max(FLOOR, v - 2 * lad.v);
      [1, 0].forEach((k) => {
        const r = runs[k];
        lp.path(r.vals.slice(0, t + 1).map((v, i) => [i, ex(v)]), { c: cols[k], w: k ? 2.2 : 1.4 });
        lp.dot(t, ex(r.vals[t]), { c: cols[k], r: 4.5 });
      });
      lp.legend([{ label: L.constS, c: "orange" }, { label: L.decS, c: "teal" }]);
      ro.set("t", String(t)); ro.set("c", FV.fmt(runs[0].vals[t], 3)); ro.set("d", FV.fmt(runs[1].vals[t], 3)); ro.set("m", FV.fmt(2 * lad.v, 3));
    }
    run();
    c2.onresize = draw; lp.onresize = draw; draw();
  });

  // Heteroscedastic data for the quantile fit (deterministic).
  function qdata() {
    const r = FV.rng(5), X = [], Y = [];
    for (let i = 0; i < 60; i++) { const x = 10 * r(); X.push(x); Y.push(2 + 0.5 * x + (0.3 + 0.2 * x) * r.normal()); }
    return { X, Y };
  }

  // 7. Pinball (quantile) loss: MAE is its τ = 0.5 case; the fitted line splits the data in the ratio τ : (1 − τ).
  FV.widget("mae-quantile", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const { X, Y } = qdata(), cache = {};
    const fit = (tau) => cache[tau] || (cache[tau] = fitPin(X, Y, tau));
    const a = new FV.Plot(FV.col(w.stage), { x: [-3, 3], y: [0, 2.9], xLabel: L.err, yLabel: L.qloss, aspect: 0.85, title: "ρτ(e) = max(τe, (τ − 1)e)" });
    const b = new FV.Plot(FV.col(w.stage), { x: [0, 10], y: [0, 11.5], xLabel: "x", yLabel: "y", aspect: 0.85, title: L.ql });
    const st = FV.ui.slider({ label: L.tau, min: 0.05, max: 0.95, step: 0.05, value: cfg.tau || 0.9, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(st.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: "τ =" }, { key: "u", label: L.below, c: "blue" }, { key: "o", label: L.on }, { key: "w", label: L.wv }, { key: "b", label: L.bv }]);
    function draw() {
      const tau = Math.round(st.value * 100) / 100, rho = (e) => Math.max(tau * e, (tau - 1) * e);
      a.clear();
      a.fn((e) => Math.abs(e) / 2, { c: "guide", w: 1.8, dash: "6 4" });
      a.fn(rho, { c: "orange", w: 2.6 });
      a.text(2.9, rho(2.9), L.slopeR, { c: "orange", anchor: "end", dy: -10 });
      a.text(-2.9, rho(-2.9), L.slopeL, { c: "orange", anchor: "start", dy: -10 });
      a.legend([{ label: L.pin, c: "orange" }, { label: L.half, c: "guide", dash: true }]);
      const m = fit(tau);
      b.clear();
      [0.1, 0.5, 0.9].forEach((t) => { if (Math.abs(t - tau) > 1e-9) { const q = fit(t); b.fn((x) => q.w * x + q.b, { c: "guide", w: 1.4, dash: "6 4" }); } });
      let below = 0, on = 0;
      X.forEach((x, i) => {
        const r = Y[i] - (m.w * x + m.b);
        if (Math.abs(r) < 1e-9) on++; else if (r < 0) below++;
        b.dot(x, Y[i], Math.abs(r) < 1e-9 ? { c: "blue", r: 4.5 } : r < 0 ? { c: "ink", r: 3.6 } : { c: "faint", r: 3.6, hollow: true });
      });
      b.fn((x) => m.w * x + m.b, { c: "blue", w: 2.6 });
      b.legend([{ label: L.ql, c: "blue" }, { label: L.qref, c: "guide", dash: true }, { label: L.under, c: "ink", dot: true }]);
      ro.set("t", FV.fmt(tau, 2)); ro.set("u", below + " / " + X.length + " = " + Math.round((100 * below) / X.length) + "%");
      ro.set("o", String(on)); ro.set("w", FV.fmt(m.w, 3)); ro.set("b", FV.fmt(m.b, 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });
})();
