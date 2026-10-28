/* Widgets of the formula page "MSE". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      obj: "объект i", truth: "истинное y", yhat: "прогноз ŷ (тяните)", sqLeg: "квадрат ошибки e²", err: "ошибка e = y − ŷ", sqs: "$e_i^2$ =", sum: "$\\sum e_i^2$ =", mse: "MSE =", share: "доля наибольшего =",
      meanLine: "среднее e² = MSE", absCmp: "|e| для сравнения",
      c: "прогноз-константа c", msec: "MSE(c)", dmsec: "∂MSE/∂c = 2(c − ȳ)", data: "данные yᵢ", mean: "среднее ȳ", median: "медиана", varLine: "Var = минимум", bias2: "(c − ȳ)²",
      out: "Выброс: 16 → 40", cval: "$c$ =", varV: "Var =", b2v: "$(c-\\bar y)^2$ =", meanV: "$\\bar y$ =", medV: "медиана =",
      loss: "потеря", deriv: "производная", e0: "старт e₀ (тяните)", iters: "шаги спуска", eta: "Шаг $\\eta$", factor: "множитель $1-2\\eta$ =", dsq: "2e", sgn: "sign(e) (MAE)", sq: "e²", abs: "|e| (MAE)",
      regime: { mono: "монотонно к нулю", one: "ровно за один шаг", osc: "к нулю с колебаниями", cycle: "вечные колебания ±e₀", div: "расходится" }, mode: "режим:",
      w: "w", b: "b", path: "путь спуска", ols: "МНК-решение", start: "старт", raw: "x как есть", cen: "x − x̄ (центрирован)", feat: "Признак", etaB: "Шаг $\\eta$",
      tv: "$t$ =", mseT: "MSE =", mseS: "MSE* =", exV: "MSE − MSE* =", crit: "$\\eta_{\\text{крит}}=2/\\lambda_{\\max}$ =", excess: "MSE − MSE* (лог. шкала)", iter: "итерация t", top: "вид сверху",
      conv: "сходится", zig: "сходится зигзагом", divg: "расходится", cond: "число обусловленности =",
      deg: "Степень полинома $d$", truthF: "истинная f(x)", fits: "модели на разных выборках", avgFit: "средняя модель", sample: "одна выборка",
      bias2L: "смещение²", varL: "разброс", noise: "шум σ²", total: "ожидаемая MSE на тесте", train: "MSE на обучении", degAx: "степень d",
      b2: "смещение² =", vv: "разброс =", nn: "шум =", tt: "тест MSE =", tr: "обучение MSE =",
      sigma: "Шум $\\sigma$", ww: "$w$", bb: "$b$", bell: "плотность N(ŷᵢ, σ²)", like: "правдоподобие точки", line: "прямая ŷ = wx + b",
      nll: "−ln L", nllV: "$-\\ln L$ =", sBest: "лучшая $\\sigma=\\sqrt{\\mathrm{MSE}}$ =", nllAx: "−ln L при текущей σ", cur: "текущая прямая", best: "МНК-прямая",
      outlier: "выброс (тяните)", points: "данные", lineMSE: "прямая по MSE", lineMAE: "прямая по MAE", infl: "наклон прямой при разной высоте выброса", yo: "высота выброса", slope: "наклон", trueS: "истинный наклон 0,5",
      slMSE: "наклон MSE =", slMAE: "наклон MAE =", shareO: "доля выброса в $\\sum e_i^2$ =",
    },
    en: {
      obj: "object i", truth: "true y", yhat: "prediction ŷ (drag)", sqLeg: "squared error e²", err: "error e = y − ŷ", sqs: "$e_i^2$ =", sum: "$\\sum e_i^2$ =", mse: "MSE =", share: "largest share =",
      meanLine: "mean e² = MSE", absCmp: "|e| for comparison",
      c: "constant prediction c", msec: "MSE(c)", dmsec: "∂MSE/∂c = 2(c − ȳ)", data: "data yᵢ", mean: "mean ȳ", median: "median", varLine: "Var = minimum", bias2: "(c − ȳ)²",
      out: "Outlier: 16 → 40", cval: "$c$ =", varV: "Var =", b2v: "$(c-\\bar y)^2$ =", meanV: "$\\bar y$ =", medV: "median =",
      loss: "loss", deriv: "derivative", e0: "start e₀ (drag)", iters: "descent steps", eta: "Step $\\eta$", factor: "factor $1-2\\eta$ =", dsq: "2e", sgn: "sign(e) (MAE)", sq: "e²", abs: "|e| (MAE)",
      regime: { mono: "monotonically to zero", one: "in exactly one step", osc: "to zero with oscillations", cycle: "endless swings ±e₀", div: "diverges" }, mode: "regime:",
      w: "w", b: "b", path: "descent path", ols: "least-squares solution", start: "start", raw: "x as is", cen: "x − x̄ (centred)", feat: "Feature", etaB: "Step $\\eta$",
      tv: "$t$ =", mseT: "MSE =", mseS: "MSE* =", exV: "MSE − MSE* =", crit: "$\\eta_{\\text{crit}}=2/\\lambda_{\\max}$ =", excess: "MSE − MSE* (log scale)", iter: "iteration t", top: "view from above",
      conv: "converges", zig: "converges in a zigzag", divg: "diverges", cond: "condition number =",
      deg: "Polynomial degree $d$", truthF: "true f(x)", fits: "models on different samples", avgFit: "average model", sample: "one sample",
      bias2L: "bias²", varL: "variance", noise: "noise σ²", total: "expected test MSE", train: "training MSE", degAx: "degree d",
      b2: "bias² =", vv: "variance =", nn: "noise =", tt: "test MSE =", tr: "train MSE =",
      sigma: "Noise $\\sigma$", ww: "$w$", bb: "$b$", bell: "density N(ŷᵢ, σ²)", like: "likelihood of a point", line: "line ŷ = wx + b",
      nll: "−ln L", nllV: "$-\\ln L$ =", sBest: "best $\\sigma=\\sqrt{\\mathrm{MSE}}$ =", nllAx: "−ln L at the current σ", cur: "current line", best: "least-squares line",
      outlier: "outlier (drag)", points: "data", lineMSE: "MSE line", lineMAE: "MAE line", infl: "the slope for different outlier heights", yo: "outlier height", slope: "slope", trueS: "true slope 0.5",
      slMSE: "MSE slope =", slMAE: "MAE slope =", shareO: "outlier’s share of $\\sum e_i^2$ =",
    },
    uz: {
      obj: "obyekt i", truth: "haqiqiy y", yhat: "bashorat ŷ (torting)", sqLeg: "xato kvadrati e²", err: "xato e = y − ŷ", sqs: "$e_i^2$ =", sum: "$\\sum e_i^2$ =", mse: "MSE =", share: "eng kattasining ulushi =",
      meanLine: "o‘rtacha e² = MSE", absCmp: "solishtirish uchun |e|",
      c: "o‘zgarmas bashorat c", msec: "MSE(c)", dmsec: "∂MSE/∂c = 2(c − ȳ)", data: "ma’lumot yᵢ", mean: "o‘rtacha ȳ", median: "mediana", varLine: "Var = minimum", bias2: "(c − ȳ)²",
      out: "Chetga chiquvchi: 16 → 40", cval: "$c$ =", varV: "Var =", b2v: "$(c-\\bar y)^2$ =", meanV: "$\\bar y$ =", medV: "mediana =",
      loss: "yo‘qotish", deriv: "hosila", e0: "start e₀ (torting)", iters: "tushish qadamlari", eta: "Qadam $\\eta$", factor: "ko‘paytuvchi $1-2\\eta$ =", dsq: "2e", sgn: "sign(e) (MAE)", sq: "e²", abs: "|e| (MAE)",
      regime: { mono: "nolga monoton", one: "roppa-rosa bir qadamda", osc: "nolga tebranib", cycle: "abadiy tebranish ±e₀", div: "uzoqlashadi" }, mode: "rejim:",
      w: "w", b: "b", path: "tushish yo‘li", ols: "EKK yechimi", start: "start", raw: "x boricha", cen: "x − x̄ (markazlashgan)", feat: "Belgi", etaB: "Qadam $\\eta$",
      tv: "$t$ =", mseT: "MSE =", mseS: "MSE* =", exV: "MSE − MSE* =", crit: "$\\eta_{\\text{krit}}=2/\\lambda_{\\max}$ =", excess: "MSE − MSE* (log. shkala)", iter: "iteratsiya t", top: "yuqoridan ko‘rinish",
      conv: "yaqinlashadi", zig: "zigzag bilan yaqinlashadi", divg: "uzoqlashadi", cond: "shartlanganlik soni =",
      deg: "Polinom darajasi $d$", truthF: "haqiqiy f(x)", fits: "turli tanlanmalardagi modellar", avgFit: "o‘rtacha model", sample: "bitta tanlanma",
      bias2L: "siljish²", varL: "tarqoqlik", noise: "shovqin σ²", total: "testdagi kutilgan MSE", train: "o‘qitishdagi MSE", degAx: "daraja d",
      b2: "siljish² =", vv: "tarqoqlik =", nn: "shovqin =", tt: "test MSE =", tr: "o‘qitish MSE =",
      sigma: "Shovqin $\\sigma$", ww: "$w$", bb: "$b$", bell: "N(ŷᵢ, σ²) zichligi", like: "nuqta o‘xshashligi", line: "ŷ = wx + b to‘g‘ri chiziq",
      nll: "−ln L", nllV: "$-\\ln L$ =", sBest: "eng yaxshi $\\sigma=\\sqrt{\\mathrm{MSE}}$ =", nllAx: "joriy σ dagi −ln L", cur: "joriy to‘g‘ri chiziq", best: "EKK to‘g‘ri chizig‘i",
      outlier: "chetga chiquvchi nuqta (torting)", points: "ma’lumot", lineMSE: "MSE bo‘yicha to‘g‘ri chiziq", lineMAE: "MAE bo‘yicha to‘g‘ri chiziq", infl: "chetga chiquvchi nuqtaning turli balandligida qiyalik", yo: "chetga chiquvchi nuqta balandligi", slope: "qiyalik", trueS: "haqiqiy qiyalik 0,5",
      slMSE: "MSE qiyaligi =", slMAE: "MAE qiyaligi =", shareO: "chetga chiquvchining $\\sum e_i^2$ dagi ulushi =",
    },
  }[FV.lang] || {};
  const SEP = FV.lang === "en" ? ", " : "; ";
  const trim = (s) => s.replace(/([.,]\d*?)0+$/, "$1").replace(/[.,]$/, "");
  const fx = (v, d) => trim(FV.fmt(v, d));
  const mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;

  function fitOLS(X, Y) {
    const mx = mean(X), my = mean(Y);
    let sxy = 0, sxx = 0;
    for (let i = 0; i < X.length; i++) { sxy += (X[i] - mx) * (Y[i] - my); sxx += (X[i] - mx) ** 2; }
    const w = sxy / sxx;
    return { w, b: my - w * mx };
  }
  // Exact least-absolute-deviations line: the optimum passes through two data points.
  function fitLAD(X, Y) {
    let best = null;
    for (let i = 0; i < X.length; i++) for (let j = i + 1; j < X.length; j++) {
      if (X[i] === X[j]) continue;
      const w = (Y[j] - Y[i]) / (X[j] - X[i]), b = Y[i] - w * X[i];
      let v = 0;
      for (let k = 0; k < X.length; k++) v += Math.abs(Y[k] - w * X[k] - b);
      if (!best || v < best.v - 1e-12) best = { w, b, v };
    }
    return best;
  }

  // 1. The running example with the squares drawn literally on the residuals.
  FV.widget("mse-squares", (el, cfg) => {
    const w = FV.shell(el, {});
    const Y = [3, 5, 8], P = (cfg.yhat || [2.5, 5, 10]).slice(), XS = [2, 7, 12];
    const p = new FV.Plot(w.stage, { x: [0, 16], y: [1, 11], equal: true, xLabel: L.obj, yLabel: "y, ŷ", xTicks: XS.map((v, i) => ({ v, label: "i = " + (i + 1) })) });
    const q = new FV.Plot(w.stage, { x: [-4, 4], y: [0, 16.5], xLabel: L.err, yLabel: "e²", aspect: 0.32, minHeight: 190, maxHeight: 250 });
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.sqs }, { key: "s", label: L.sum }, { key: "m", label: L.mse, c: "orange" }, { key: "h", label: L.share }]);
    const hs = P.map((v, i) => p.handle(XS[i], v, { c: "blue", label: "ŷ" + (i + 1), onDrag: (x, y) => [XS[i], Math.round(y * 10) / 10], onChange: (x, y) => { P[i] = y; draw(); } }));
    function draw() {
      const E = Y.map((y, i) => y - P[i]), S = E.map((e) => e * e), tot = S.reduce((a, b) => a + b, 0), m = tot / 3;
      p.clear();
      const tk = (13 * 16) / (p.x1 - p.x0);
      Y.forEach((y, i) => {
        const x = XS[i], a = Math.abs(E[i]), lo = Math.min(y, P[i]), hi = Math.max(y, P[i]);
        if (a > 0.01) {
          p.rect(x, lo, x + a, hi, { c: "orange", opacity: 0.16 });
          p.path([[x, lo], [x + a, lo], [x + a, hi], [x, hi]], { c: "orange", w: 1.3 });
          p.text(x + a, hi, "e" + "₁₂₃"[i] + "² = " + fx(S[i], 2), { c: "orange", dx: 6, dy: -6 });
        }
        p.line(x, y, x, P[i], { c: "orange", w: 3 });
        p.line(x - tk, y, x + tk, y, { c: "ink", w: 2.5 });
        p.dot(x, y, { c: "ink", r: 4.5 });
      });
      hs.forEach((h, i) => h.set(XS[i], P[i]));
      p.legend([{ label: L.truth, c: "ink", dot: true }, { label: L.yhat, c: "blue", dot: true }, { label: L.sqLeg, c: "orange", box: true }]);
      q.clear();
      q.fn((e) => Math.abs(e), { c: "guide", w: 1.6, dash: "6 4" });
      q.area((e) => e * e, null, { c: "orange", fillOpacity: 0.07 });
      q.fn((e) => e * e, { c: "orange", w: 2.4 });
      q.hline(m, { c: "teal", dash: "5 4", w: 1.6 });
      E.forEach((e, i) => {
        q.line(e, 0, e, S[i], { c: "orange", w: 1, dash: "3 3" });
        q.dot(e, Math.min(S[i], 16.5), { c: "orange", r: 5 });
        q.text(e, Math.min(S[i], 16.5), String(i + 1), { c: "ink", dx: 7, dy: -8 });
      });
      q.legend([{ label: "e²", c: "orange" }, { label: L.meanLine + " = " + FV.fmt(m, 3), c: "teal", dash: true }, { label: L.absCmp, c: "guide", dash: true }]);
      ro.set("e", "(" + S.map((v) => fx(v, 2)).join(SEP) + ")"); ro.set("s", fx(tot, 2)); ro.set("m", FV.fmt(m, 3));
      ro.set("h", tot > 0 ? Math.round((100 * Math.max(...S)) / tot) + "%" : "—");
    }
    p.onresize = draw; q.onresize = draw; draw();
  });

  // 2. The best constant under MSE is the mean; MSE(c) = Var + (c − ȳ)².
  FV.widget("mse-mean", (el, cfg) => {
    const w = FV.shell(el, {});
    const BASE = [2, 3, 5, 9, 16], OUT = [2, 3, 5, 9, 40];
    let D = cfg.outlier ? OUT : BASE, c = cfg.c != null ? cfg.c : 12;
    const dom = () => (D === OUT ? { x: [0, 44], y: [0, 900], d: [-30, 70] } : { x: [0, 18], y: [0, 150], d: [-16, 24] });
    const p = new FV.Plot(w.stage, { x: dom().x, y: dom().y, xLabel: L.c, yLabel: L.msec, aspect: 0.48 });
    const d = new FV.Plot(w.stage, { x: dom().x, y: dom().d, xLabel: L.c, yLabel: L.dmsec, aspect: 0.26, minHeight: 170, maxHeight: 220 });
    const f = (x) => D.reduce((s, y) => s + (y - x) ** 2, 0) / D.length;
    const chk = FV.ui.check({ label: L.out, checked: !!cfg.outlier, onchange: (v) => { D = v ? OUT : BASE; const g = dom(); p.setDomain(g.x, g.y); d.setDomain(g.x, g.d); c = FV.clamp(c, g.x[0], g.x[1]); draw(); } });
    w.controls.append(chk.el);
    const ro = FV.ui.readout(w.readout, [{ key: "c", label: L.cval }, { key: "m", label: L.msec + " =", c: "orange" }, { key: "v", label: L.varV, c: "teal" }, { key: "b", label: L.b2v, c: "blue" }, { key: "a", label: L.meanV }, { key: "md", label: L.medV }]);
    const h = p.handle(c, f(c), { c: "blue", label: "c", onDrag: (x) => { c = Math.round(x * 10) / 10; return [c, f(c)]; }, onChange: () => draw() });
    function draw() {
      const g = dom(), mu = mean(D), v = f(mu), med = D.slice().sort((a, b) => a - b)[2];
      p.clear(); d.clear();
      D.forEach((y) => p.vline(y, { c: "guide", dash: "2 4" }));
      p.hline(v, { c: "teal", dash: "6 4", w: 1.4 });
      p.vline(mu, { c: "teal", dash: false, w: 1.6 });
      p.vline(med, { c: "faint", dash: "6 4", w: 1.3 });
      const yl = g.y[1];
      p.text(mu, yl * 0.8, L.mean, { c: "teal", dx: 5 });
      p.text(med, yl * 0.62, L.median, { c: "faint", anchor: "end", dx: -5 });
      p.fn(f, { c: "orange", w: 2.6 });
      D.forEach((y) => p.dot(y, yl * 0.02, { c: "ink", r: 5 }));
      if (Math.abs(c - mu) > 1e-9) p.line(c, v, c, f(c), { c: "blue", w: 3, opacity: 0.55 });
      h.set(c, f(c));
      p.legend([{ label: L.msec, c: "orange" }, { label: L.data, c: "ink", dot: true }, { label: L.mean, c: "teal" }, { label: L.varLine, c: "teal", dash: true }, { label: L.bias2, c: "blue" }, { label: L.median, c: "faint", dash: true }]);
      d.hline(0, { c: "guide", dash: false });
      d.vline(mu, { c: "teal", dash: false, w: 1.6 });
      d.fn((x) => 2 * (x - mu), { c: "orange", w: 2.4 });
      d.dot(c, 2 * (c - mu), { c: "blue", r: 4.5 });
      ro.set("c", FV.fmt(c, 1)); ro.set("m", FV.fmt(f(c), 2)); ro.set("v", FV.fmt(v, 2)); ro.set("b", FV.fmt((c - mu) ** 2, 2));
      ro.set("a", FV.fmt(mu, 1)); ro.set("md", String(med));
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 3. e², its derivative 2e, and gradient descent on a single error: e ← (1 − 2η)e.
  FV.widget("mse-derivative", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-3.2, 3.2], y: [-0.5, 10.5], xLabel: L.err, yLabel: L.loss, aspect: 0.8, title: "e²" });
    const b = new FV.Plot(FV.col(w.stage), { x: [-3.2, 3.2], y: [-6.6, 6.6], xLabel: L.err, yLabel: L.deriv, aspect: 0.8, title: "∂e²/∂e = 2e" });
    let e0 = cfg.e != null ? cfg.e : 2.5;
    const se = FV.ui.slider({ label: L.eta, min: 0.05, max: 1.1, step: 0.05, value: cfg.eta != null ? cfg.eta : 0.3, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(se.el);
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: "$e_0$ =" }, { key: "f", label: L.factor, c: "orange" }, { key: "s", label: "$e_1, e_2, e_3$ =" }, { key: "r", label: L.mode }]);
    const h = a.handle(e0, e0 * e0, { c: "blue", label: "e₀", onDrag: (x) => { e0 = Math.round(x * 20) / 20; return [e0, e0 * e0]; }, onChange: () => draw() });
    function draw() {
      const eta = Math.round(se.value * 100) / 100, k = 1 - 2 * eta, its = [e0];
      for (let i = 0; i < 6; i++) its.push(its[i] * k);
      a.clear(); b.clear();
      a.hline(0, { c: "guide", dash: false }); b.hline(0, { c: "guide", dash: false });
      a.fn((x) => Math.abs(x), { c: "guide", w: 1.6, dash: "6 4" });
      b.line(-3.2, -1, 0, -1, { c: "guide", w: 1.6, dash: "6 4" }); b.line(0, 1, 3.2, 1, { c: "guide", w: 1.6, dash: "6 4" });
      a.fn((x) => x * x, { c: "orange", w: 2.6 });
      b.fn((x) => 2 * x, { c: "orange", w: 2.6 });
      // tangent at the start point
      a.line(e0 - 1.4, e0 * e0 - 1.4 * 2 * e0, e0 + 1.4, e0 * e0 + 1.4 * 2 * e0, { c: "ink", w: 1.4, dash: "5 4" });
      for (let i = 0; i < 6; i++) {
        const u = its[i], v = its[i + 1];
        if (Math.abs(u) > 4 || Math.abs(v) > 4) break;
        a.arrow(u, u * u, v, v * v, { c: "blue", w: 1.4, head: 7 });
      }
      its.forEach((u, i) => {
        if (Math.abs(u) > 3.3) return;
        a.dot(u, u * u, { c: "blue", r: i ? 3.5 : 5 });
        b.dot(u, 2 * u, { c: "blue", r: i ? 3.5 : 5 });
        if (i < 4) b.line(u, 0, u, 2 * u, { c: "blue", w: 1, opacity: 0.5 });
      });
      h.set(e0, e0 * e0);
      a.legend([{ label: L.sq, c: "orange" }, { label: L.abs, c: "guide", dash: true }, { label: L.iters, c: "blue", dot: true }]);
      b.legend([{ label: L.dsq, c: "orange" }, { label: L.sgn, c: "guide", dash: true }]);
      const R = L.regime;
      const mode = Math.abs(k) < 1e-9 ? R.one : k > 0 ? R.mono : k > -1 + 1e-9 ? R.osc : Math.abs(k + 1) < 1e-9 ? R.cycle : R.div;
      ro.set("e", FV.fmt(e0, 2)); ro.set("f", FV.fmt(k, 2)); ro.set("s", its.slice(1, 4).map((u) => FV.num(u, 3)).join(SEP)); ro.set("r", mode);
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // The line-fit problem shared by the bowl and the likelihood widgets.
  const BX = [1, 2, 3, 4, 5], BY = [1.3, 2.0, 3.1, 4.5, 7.0];
  const ETAS = [0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.45, 0.55];

  // 4. The MSE bowl over (w, b), gradient descent on it, and what centring x does to the bowl.
  FV.widget("mse-bowl", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const T = 150, start = [0, 3];
    const MODES = {
      raw: { X: BX, W: [-0.2, 2.6], B: [-2.4, 4], az: 0.9, el: 0.6 },
      cen: { X: BX.map((x) => x - 3), W: [-0.2, 2.6], B: [0.6, 7], az: -0.6, el: 0.75 },
    };
    let mode = cfg.centered ? "cen" : "raw", t = cfg.t != null ? cfg.t : T, run = null;
    const M = () => MODES[mode];
    const loss = (a, b) => { const X = M().X; let s = 0; for (let i = 0; i < 5; i++) s += (BY[i] - a * X[i] - b) ** 2; return s / 5; };
    const s3 = new FV.Surface(FV.col(w.stage), { f: loss, x: M().W, y: M().B, n: 40, labels: { x: "w", y: "b", z: "MSE" }, azimuth: M().az, elevation: M().el, aspect: 0.95, title: "MSE(w, b)" });
    const right = FV.col(w.stage);
    const c2 = new FV.Plot(right, { x: M().W, y: M().B, xLabel: "w", yLabel: "b", aspect: 0.75, title: L.top });
    const lt = [[-8, "10⁻⁸"], [-6, "10⁻⁶"], [-4, "10⁻⁴"], [-2, "0,01"], [0, "1"], [2, "100"]].map(([e, s]) => ({ v: Math.pow(10, e), label: FV.lang === "en" ? s.replace(",", ".") : s }));
    const lp = new FV.Plot(right, { x: [0, T], y: [1e-8, 1e3], yType: "log", yTicks: lt, xLabel: L.iter, yLabel: "MSE − MSE*", aspect: 0.5, minHeight: 170, maxHeight: 230, title: L.excess });
    const seg = FV.ui.seg({ label: L.feat, value: mode, options: [{ value: "raw", label: L.raw }, { value: "cen", label: L.cen }], onchange: (v) => { mode = v; s3.az = s3.o.azimuth = M().az; s3.el = s3.o.elevation = M().el; s3.setDomain(M().W, M().B); c2.setDomain(M().W, M().B); simulate(); draw(); } });
    const etaIdx = Math.max(0, ETAS.indexOf(cfg.eta != null ? cfg.eta : 0.05));
    const se = FV.ui.slider({ label: L.etaB, min: 0, max: ETAS.length - 1, step: 1, value: etaIdx, map: (i) => ETAS[i], unmap: (v) => ETAS.indexOf(v), fmt: (v) => FV.num(v, 2), oninput: () => { simulate(); draw(); } });
    const player = FV.ui.player({ interval: 40, onstep() { if (t >= T) t = 0; t++; draw(); return t < T; }, onreset() { t = 0; draw(); } });
    w.controls.append(seg.el, se.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.tv }, { key: "m", label: L.mseT, c: "orange" }, { key: "s", label: L.mseS }, { key: "x", label: L.exV }, { key: "c", label: L.crit }, { key: "k", label: L.cond }]);
    function eig() {
      const X = M().X, ex = mean(X), ex2 = mean(X.map((x) => x * x));
      const tr = 2 * (ex2 + 1), det = 4 * (ex2 - ex * ex), r = Math.sqrt(tr * tr / 4 - det);
      return [tr / 2 + r, tr / 2 - r];
    }
    function simulate() {
      const X = M().X, eta = se.value, o = fitOLS(X, BY), best = loss(o.w, o.b);
      let a = start[0], b = start[1];
      const pts = [[a, b]], ex = [loss(a, b) - best];
      for (let k = 0; k < T; k++) {
        let ga = 0, gb = 0;
        for (let i = 0; i < 5; i++) { const r = BY[i] - a * X[i] - b; ga -= (2 * r * X[i]) / 5; gb -= (2 * r) / 5; }
        a -= eta * ga; b -= eta * gb;
        if (!Number.isFinite(a) || Math.abs(a) > 1e6 || Math.abs(b) > 1e6) { a = Math.sign(a) * 1e6; b = Math.sign(b) * 1e6; }
        pts.push([a, b]); ex.push(loss(a, b) - best);
      }
      run = { pts, ex, o, best };
    }
    function draw() {
      const { pts, ex, o, best } = run, W = M().W, B = M().B;
      const inside = (q) => q[0] >= W[0] && q[0] <= W[1] && q[1] >= B[0] && q[1] <= B[1];
      let upto = 0;
      while (upto < t && inside(pts[upto + 1])) upto++;
      const vis = pts.slice(0, upto + 1);
      s3.setPaths([{ pts: vis.map((q) => [q[0], q[1], loss(q[0], q[1])]), c: "orange", w: 2.2 }]);
      s3.points = [{ x: o.w, y: o.b, z: best, c: "red", r: 5 }];
      if (t <= upto) { const q = pts[t]; s3.points.push({ x: q[0], y: q[1], z: loss(q[0], q[1]), c: "blue", r: 5.5 }); }
      s3.draw();
      c2.clear();
      c2.heat(loss, { cmap: "blues", res: 4, alpha: 0.8, transform: Math.sqrt });
      c2.contours(loss, [0.3, 0.5, 1, 2, 3.5, 6, 10, 16], { c: "ink", w: 1, opacity: 0.4 });
      c2.path(vis, { c: "orange", w: 1.8 });
      c2.dot(start[0], start[1], { c: "ink", hollow: true, r: 4.5 });
      c2.dot(o.w, o.b, { c: "red", r: 5.5 });
      if (t <= upto) { const q = pts[t]; c2.dot(q[0], q[1], { c: "blue", r: 5 }); }
      c2.legend([{ label: L.path, c: "orange" }, { label: L.ols, c: "red", dot: true }, { label: L.start, c: "ink", dot: true }]);
      lp.clear();
      const clampE = (v) => (Number.isFinite(v) ? FV.clamp(v, 1e-8, 1e3) : 1e3);
      lp.path(ex.slice(0, t + 1).map((v, i) => [i, clampE(v)]), { c: "orange", w: 2 });
      lp.dot(t, clampE(ex[t]), { c: "blue", r: 4.5 });
      const [l1, l2] = eig(), eta = se.value;
      ro.set("t", String(t)); ro.set("m", Number.isFinite(ex[t]) && ex[t] < 1e6 ? FV.fmt(ex[t] + best, 4) : "∞"); ro.set("s", FV.fmt(best, 4)); ro.set("x", Number.isFinite(ex[t]) && ex[t] < 1e6 ? FV.num(Math.max(ex[t], 0), 2) : "∞");
      ro.set("c", FV.fmt(2 / l1, 4)); ro.set("k", FV.fmt(l1 / l2, 1));
      const fac = [1 - eta * l1, 1 - eta * l2];
      w.note.textContent = (fac.some((v) => Math.abs(v) >= 1) ? L.divg : fac.some((v) => v < 0) ? L.zig : L.conv) + ": 1 − ηλ = " + fac.map((v) => FV.fmt(v, 3)).join(SEP);
    }
    simulate();
    c2.onresize = draw; lp.onresize = draw; draw();
  });

  // Polynomial fits in the Legendre basis (well conditioned on [−1, 1]).
  function legendre(x, d) { const P = [1, x]; for (let k = 1; k < d; k++) P.push(((2 * k + 1) * x * P[k] - k * P[k - 1]) / (k + 1)); return P.slice(0, d + 1); }
  function solve(A, r) {
    const n = r.length; A = A.map((row) => row.slice()); r = r.slice();
    for (let i = 0; i < n; i++) {
      let p = i; for (let k = i + 1; k < n; k++) if (Math.abs(A[k][i]) > Math.abs(A[p][i])) p = k;
      [A[i], A[p]] = [A[p], A[i]]; [r[i], r[p]] = [r[p], r[i]];
      for (let k = i + 1; k < n; k++) { const f = A[k][i] / A[i][i]; for (let c = i; c < n; c++) A[k][c] -= f * A[i][c]; r[k] -= f * r[i]; }
    }
    const x = new Array(n).fill(0);
    for (let i = n - 1; i >= 0; i--) { let s = r[i]; for (let c = i + 1; c < n; c++) s -= A[i][c] * x[c]; x[i] = s / A[i][i]; }
    return x;
  }
  function polyfit(X, Y, d) {
    const p = d + 1, A = Array.from({ length: p }, () => new Array(p).fill(0)), r = new Array(p).fill(0);
    X.forEach((x, i) => { const P = legendre(x, d); for (let a = 0; a < p; a++) { r[a] += P[a] * Y[i]; for (let c = 0; c < p; c++) A[a][c] += P[a] * P[c]; } });
    return solve(A, r);
  }
  const peval = (c, x) => legendre(x, c.length - 1).reduce((s, v, j) => s + v * c[j], 0);

  // 5. Bias–variance: many training sets, polynomial fits of degree d, and the decomposition of the test MSE.
  FV.widget("mse-biasvar", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const N = 15, SIG = 0.3, R = 200, DMAX = 10, f = (x) => Math.sin(Math.PI * x);
    const r = FV.rng(3), X = Array.from({ length: N }, (_, i) => -1 + (2 * (i + 0.5)) / N);
    const sets = Array.from({ length: R }, () => X.map((x) => f(x) + SIG * r.normal()));
    const G = Array.from({ length: 101 }, (_, i) => -1 + i / 50);
    const stats = [];
    for (let d = 0; d <= DMAX; d++) {
      const coefs = sets.map((Y) => polyfit(X, Y, d)), preds = coefs.map((c) => G.map((x) => peval(c, x)));
      let b2 = 0, v = 0;
      const avg = G.map((x, g) => { const m = preds.reduce((s, p) => s + p[g], 0) / R; b2 += (m - f(x)) ** 2; v += preds.reduce((s, p) => s + (p[g] - m) ** 2, 0) / R; return m; });
      b2 /= G.length; v /= G.length;
      let tr = 0;
      sets.forEach((Y, k) => { tr += X.reduce((s, x, i) => s + (Y[i] - peval(coefs[k], x)) ** 2, 0) / N; });
      stats.push({ b2, v, tr: tr / R, total: b2 + v + SIG * SIG, preds, avg });
    }
    const a = new FV.Plot(FV.col(w.stage), { x: [-1, 1], y: [-2, 2], xLabel: "x", yLabel: "y", aspect: 0.85, title: "f̂(x)" });
    const b = new FV.Plot(FV.col(w.stage), { x: [-0.5, DMAX + 0.5], y: [1e-4, 3], yType: "log", xLabel: L.degAx, yLabel: "MSE", aspect: 0.85, title: "MSE = " + L.bias2L + " + " + L.varL + " + σ²" });
    const sd = FV.ui.slider({ label: L.deg, min: 0, max: DMAX, step: 1, value: cfg.d != null ? cfg.d : 3, fmt: (v) => String(v), oninput: draw });
    w.controls.append(sd.el);
    const ro = FV.ui.readout(w.readout, [{ key: "b", label: L.b2, c: "blue" }, { key: "v", label: L.vv, c: "orange" }, { key: "n", label: L.nn }, { key: "t", label: L.tt }, { key: "r", label: L.tr }]);
    function draw() {
      const d = sd.value, s = stats[d];
      a.clear();
      for (let k = 0; k < 25; k++) a.path(G.map((x, g) => [x, s.preds[k][g]]), { c: "blue", w: 1, opacity: 0.22 });
      a.fn(f, { c: "ink", w: 2, dash: "6 4" });
      a.path(G.map((x, g) => [x, s.avg[g]]), { c: "blue", w: 2.6 });
      X.forEach((x, i) => a.dot(x, sets[0][i], { c: "faint", r: 3.5 }));
      a.legend([{ label: L.truthF, c: "ink", dash: true }, { label: L.avgFit, c: "blue" }, { label: L.fits, c: "blue", box: true }, { label: L.sample, c: "faint", dot: true }]);
      b.clear();
      b.rect(d - 0.4, 1e-4, d + 0.4, 3, { c: "guide", opacity: 0.18 });
      b.hline(SIG * SIG, { c: "guide", dash: "6 4", w: 1.4 });
      const line = (k, c, o) => b.path(stats.map((q, i) => [i, Math.max(1e-4, q[k])]), Object.assign({ c, w: 2.2 }, o || {}));
      line("b2", "blue"); line("v", "orange"); line("tr", "ink", { dash: "4 4", w: 1.6 }); line("total", "ink", { w: 2.6 });
      stats.forEach((q, i) => { b.dot(i, Math.max(1e-4, q.total), { c: "ink", r: i === d ? 5 : 3 }); });
      b.legend([{ label: L.bias2L, c: "blue" }, { label: L.varL, c: "orange" }, { label: L.noise, c: "guide", dash: true }, { label: L.total, c: "ink" }, { label: L.train, c: "ink", dash: true }]);
      ro.set("b", FV.fmt(s.b2, 4)); ro.set("v", FV.fmt(s.v, 4)); ro.set("n", FV.fmt(SIG * SIG, 2)); ro.set("t", FV.fmt(s.total, 3)); ro.set("r", FV.fmt(s.tr, 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 6. MSE = Gaussian maximum likelihood: bells around the line, −ln L is an increasing linear function of MSE.
  FV.widget("mse-gauss", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const n = 5, K = 0.55, o = fitOLS(BX, BY);
    const a = new FV.Plot(FV.col(w.stage), { x: [0.3, 6.3], y: [-0.5, 9], xLabel: "x", yLabel: "y", aspect: 0.85, title: L.line });
    const b = new FV.Plot(FV.col(w.stage), { x: [0, 2.5], y: [0, 30], xLabel: "MSE", yLabel: L.nll, aspect: 0.85, title: L.nllAx });
    const sw = FV.ui.slider({ label: L.ww, min: 0, max: 2.5, step: 0.01, value: cfg.w != null ? cfg.w : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sb = FV.ui.slider({ label: L.bb, min: -2, max: 2, step: 0.01, value: cfg.b != null ? cfg.b : 0.5, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const ss = FV.ui.slider({ label: L.sigma, min: 0.3, max: 1.5, step: 0.01, value: cfg.s != null ? cfg.s : 0.6, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sw.el, sb.el, ss.el);
    const ro = FV.ui.readout(w.readout, [{ key: "m", label: "MSE =", c: "orange" }, { key: "l", label: L.nllV, c: "blue" }, { key: "s", label: L.sBest }]);
    const pdf = (z, s) => Math.exp(-0.5 * (z / s) ** 2) / (s * Math.sqrt(2 * Math.PI));
    const nll = (m, s) => (n / 2) * Math.log(2 * Math.PI * s * s) + (n * m) / (2 * s * s);
    function draw() {
      const W = sw.value, B = sb.value, S = ss.value, pred = (x) => W * x + B;
      const m = BX.reduce((acc, x, i) => acc + (BY[i] - pred(x)) ** 2, 0) / n;
      a.clear();
      a.fn(pred, { c: "blue", w: 2.4 });
      BX.forEach((x, i) => {
        const mu = pred(x), ys = FV.linspace(mu - 3.2 * S, mu + 3.2 * S, 60);
        a.path(ys.map((y) => [x + K * pdf(y - mu, S), y]).concat([[x, mu + 3.2 * S], [x, mu - 3.2 * S]]), { c: "blue", fill: true, fillOpacity: 0.1, close: true });
        a.path(ys.map((y) => [x + K * pdf(y - mu, S), y]), { c: "blue", w: 1.2, opacity: 0.7 });
        a.line(x, mu - 3.2 * S, x, mu + 3.2 * S, { c: "blue", w: 1, opacity: 0.35 });
        a.line(x, BY[i], x + K * pdf(BY[i] - mu, S), BY[i], { c: "orange", w: 3 });
        a.dot(x, BY[i], { c: "ink", r: 4.5 });
      });
      a.legend([{ label: L.line, c: "blue" }, { label: L.bell, c: "blue", box: true }, { label: L.like, c: "orange" }, { label: L.points, c: "ink", dot: true }]);
      const top = Math.max(nll(2.5, S), nll(0, S) + 1), bot = Math.min(0, nll(0, S) - 1);
      b.setDomain(null, [bot, top]);
      b.clear();
      b.fn((x) => nll(x, S), { c: "ink", w: 2 });
      const mo = BX.reduce((acc, x, i) => acc + (BY[i] - o.w * x - o.b) ** 2, 0) / n;
      b.line(mo, bot, mo, nll(mo, S), { c: "red", w: 1, dash: "3 3" });
      b.dot(mo, nll(mo, S), { c: "red", r: 5 });
      b.line(m, bot, m, nll(m, S), { c: "blue", w: 1, dash: "3 3" });
      b.dot(m, nll(m, S), { c: "blue", r: 5.5 });
      b.legend([{ label: L.cur, c: "blue", dot: true }, { label: L.best, c: "red", dot: true }]);
      ro.set("m", FV.fmt(m, 3)); ro.set("l", FV.fmt(nll(m, S), 3)); ro.set("s", FV.fmt(Math.sqrt(m), 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 7. Influence of one outlier: the line and its slope as the outlier moves.
  const OX = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5], OY = [1.55, 1.35, 2.45, 3.25, 2.95, 3.85, 3.75, 5.15, 5.05, 6.05];
  FV.widget("mse-outlier", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    let yo = cfg.y != null ? cfg.y : 0;
    const YO = [-5, 13], X = OX.concat([9]);
    const fits = (v) => { const Y = OY.concat([v]); return { o: fitOLS(X, Y), m: fitLAD(X, Y), Y }; };
    const curve = FV.linspace(YO[0], YO[1], 181).map((v) => { const q = fits(v); return [v, q.o.w, q.m.w]; });
    const a = new FV.Plot(FV.col(w.stage), { x: [0, 10], y: YO, xLabel: "x", yLabel: "y", aspect: 0.85, title: L.lineMSE + " / " + L.lineMAE });
    const b = new FV.Plot(FV.col(w.stage), { x: YO, y: [0, 0.9], xLabel: L.yo, yLabel: L.slope, aspect: 0.85, title: L.infl });
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.slMSE, c: "blue" }, { key: "m", label: L.slMAE }, { key: "h", label: L.shareO, c: "orange" }]);
    const h = a.handle(9, yo, { c: "red", label: L.outlier, onDrag: (x, y) => { yo = Math.round(y * 10) / 10; return [9, yo]; }, onChange: () => draw() });
    function draw() {
      const { o, m, Y } = fits(yo);
      a.clear();
      X.forEach((x, i) => a.line(x, Y[i], x, o.w * x + o.b, { c: "orange", w: 1.3, opacity: 0.7 }));
      a.fn((x) => m.w * x + m.b, { c: "guide", w: 2.2, dash: "7 5" });
      a.fn((x) => o.w * x + o.b, { c: "blue", w: 2.6 });
      OX.forEach((x, i) => a.dot(x, OY[i], { c: "ink", r: 4.5 }));
      h.set(9, yo);
      a.legend([{ label: L.points, c: "ink", dot: true }, { label: L.outlier, c: "red", dot: true }, { label: L.lineMSE, c: "blue" }, { label: L.lineMAE, c: "guide", dash: true }]);
      b.clear();
      b.hline(0.5, { c: "faint", dash: "2 4", w: 1.2 });
      b.text(YO[0], 0.5, L.trueS, { c: "faint", dx: 6, dy: -6 });
      b.path(curve.map((q) => [q[0], q[2]]), { c: "guide", w: 2.2, dash: "7 5" });
      b.path(curve.map((q) => [q[0], q[1]]), { c: "blue", w: 2.4 });
      b.vline(yo, { c: "red", w: 1, dash: "3 3" });
      b.dot(yo, m.w, { c: "faint", r: 4.5 }); b.dot(yo, o.w, { c: "blue", r: 5.5 });
      b.legend([{ label: L.lineMSE, c: "blue" }, { label: L.lineMAE, c: "guide", dash: true }]);
      const R = Y.map((y, i) => (y - o.w * X[i] - o.b) ** 2), tot = R.reduce((s, v) => s + v, 0);
      ro.set("s", FV.fmt(o.w, 3)); ro.set("m", FV.fmt(m.w, 3)); ro.set("h", Math.round((100 * R[R.length - 1]) / tot) + "%");
    }
    a.onresize = draw; b.onresize = draw; draw();
  });
})();
