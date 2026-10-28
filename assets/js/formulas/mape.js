/* Widgets of the formula page "MAPE". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      obj: "объект i", vals: "y, ŷ", fact: "факт y", pred: "прогноз ŷ (тяните)", err: "ошибка y − ŷ", apeT: "Ошибка в процентах от факта",
      ape: "APE, %", apeI: "APEᵢ = |yᵢ − ŷᵢ| / |yᵢ|",
      yhat: "прогноз ŷ (факт y = 100)", loss: "ошибка, %", dloss: "производная, % на единицу", under: "недопрогноз", over: "перепрогноз",
      cap: "потолок 100%", mirror: "тот же промах в разах: ŷ = y²/ŷ", ratio: "ŷ / y", apeMirror: "APE при y²/ŷ",
      yAx: "факт y", yhAx: "прогноз ŷ", levels: "уровни APE: 10, 25, 50, 100, 200%", absLines: "|y − ŷ| = 1 и 2", top: "Вид сверху: лучи равной APE",
      pP: "точка P (тяните)", pQ: "точка Q = (8; 9)", apeP: "APE в P =", errP: "|y − ŷ| в P =", apeQ: "APE в Q =",
      c: "константный прогноз c", sigma: "Разброс спроса $\\sigma$", median: "медиана", mean: "среднее", copt: "минимум MAPE c*", data: "продажи yᵢ",
      dmape: "наклон MAPE(c)", rel: "c* / медиана − 1 =", theory: "теория e^(−σ²) − 1 =",
      week: "неделя", sales: "спрос", fc: "прогноз k · база", k: "Множитель прогноза $k$", dip: "Провал спроса: неделя 41, y = 3", kAx: "множитель k",
      metric: "метрика, %", best: "минимум",
      x: "x (например, размер магазина)", yv: "продажи y", wAx: "наклон w", mapeModel: "модель по MAPE", olsModel: "модель по MSE (МНК)", truth: "истинная 10·x",
      size: "размер точки ∝ 1/y", mapeW: "MAPE(w)", step: "шаг", bias: "смещение суммы", olsW: "w по МНК =",
      sku: "товар", vol: "продажи (лог. шкала)", actual: "факт", fcst: "прогноз", slowF: "Продажи F (прогноз 10)",
      mapeNoF: "MAPE без F =", shareF: "доля F в сумме APE =",
    },
    en: {
      obj: "object i", vals: "y, ŷ", fact: "actual y", pred: "forecast ŷ (drag)", err: "error y − ŷ", apeT: "Error as a percentage of the actual",
      ape: "APE, %", apeI: "APEᵢ = |yᵢ − ŷᵢ| / |yᵢ|",
      yhat: "forecast ŷ (actual y = 100)", loss: "error, %", dloss: "derivative, % per unit", under: "under-forecast", over: "over-forecast",
      cap: "100% ceiling", mirror: "the same miss as a ratio: ŷ = y²/ŷ", ratio: "ŷ / y", apeMirror: "APE at y²/ŷ",
      yAx: "actual y", yhAx: "forecast ŷ", levels: "APE levels: 10, 25, 50, 100, 200%", absLines: "|y − ŷ| = 1 and 2", top: "Top view: rays of equal APE",
      pP: "point P (drag)", pQ: "point Q = (8, 9)", apeP: "APE at P =", errP: "|y − ŷ| at P =", apeQ: "APE at Q =",
      c: "constant forecast c", sigma: "Demand spread $\\sigma$", median: "median", mean: "mean", copt: "MAPE minimum c*", data: "sales yᵢ",
      dmape: "slope of MAPE(c)", rel: "c* / median − 1 =", theory: "theory e^(−σ²) − 1 =",
      week: "week", sales: "demand", fc: "forecast k · base", k: "Forecast multiplier $k$", dip: "Demand dip: week 41, y = 3", kAx: "multiplier k",
      metric: "metric, %", best: "minimum",
      x: "x (e.g. store size)", yv: "sales y", wAx: "slope w", mapeModel: "MAPE model", olsModel: "MSE model (least squares)", truth: "true 10·x",
      size: "dot size ∝ 1/y", mapeW: "MAPE(w)", step: "step", bias: "bias of the total", olsW: "least-squares w =",
      sku: "product", vol: "sales (log scale)", actual: "actual", fcst: "forecast", slowF: "Sales of F (forecast 10)",
      mapeNoF: "MAPE without F =", shareF: "F’s share of the APE sum =",
    },
    uz: {
      obj: "obyekt i", vals: "y, ŷ", fact: "haqiqiy y", pred: "bashorat ŷ (torting)", err: "xato y − ŷ", apeT: "Haqiqiy qiymatga nisbatan foizdagi xato",
      ape: "APE, %", apeI: "APEᵢ = |yᵢ − ŷᵢ| / |yᵢ|",
      yhat: "bashorat ŷ (haqiqiy y = 100)", loss: "xato, %", dloss: "hosila, birlik uchun %", under: "kam bashorat", over: "ortiq bashorat",
      cap: "100% shift", mirror: "marta bo‘yicha xuddi shu xato: ŷ = y²/ŷ", ratio: "ŷ / y", apeMirror: "y²/ŷ dagi APE",
      yAx: "haqiqiy y", yhAx: "bashorat ŷ", levels: "APE sathlari: 10, 25, 50, 100, 200%", absLines: "|y − ŷ| = 1 va 2", top: "Yuqoridan ko‘rinish: teng APE nurlari",
      pP: "P nuqta (torting)", pQ: "Q = (8; 9) nuqta", apeP: "P dagi APE =", errP: "P dagi |y − ŷ| =", apeQ: "Q dagi APE =",
      c: "konstant bashorat c", sigma: "Talab tarqoqligi $\\sigma$", median: "mediana", mean: "o‘rtacha", copt: "MAPE minimumi c*", data: "sotuvlar yᵢ",
      dmape: "MAPE(c) qiyaligi", rel: "c* / mediana − 1 =", theory: "nazariya e^(−σ²) − 1 =",
      week: "hafta", sales: "talab", fc: "bashorat k · baza", k: "Bashorat ko‘paytuvchisi $k$", dip: "Talab tushishi: 41-hafta, y = 3", kAx: "ko‘paytuvchi k",
      metric: "metrika, %", best: "minimum",
      x: "x (masalan, do‘kon o‘lchami)", yv: "sotuvlar y", wAx: "qiyalik w", mapeModel: "MAPE bo‘yicha model", olsModel: "MSE bo‘yicha model (EKK)", truth: "haqiqiy 10·x",
      size: "nuqta o‘lchami ∝ 1/y", mapeW: "MAPE(w)", step: "qadam", bias: "yig‘indi siljishi", olsW: "EKK bo‘yicha w =",
      sku: "tovar", vol: "sotuvlar (log. shkala)", actual: "haqiqiy", fcst: "bashorat", slowF: "F sotuvlari (bashorat 10)",
      mapeNoF: "F siz MAPE =", shareF: "F ning APE yig‘indisidagi ulushi =",
    },
  }[FV.lang] || {};

  const pct = (v, d = 1) => FV.fmt(v, d) + "%";
  const mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
  const Y = [3, 5, 8], YH = [2.5, 5, 10];

  // 1. The running example: the same absolute miss costs differently.
  FV.widget("mape-explorer", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const yh = (cfg.yhat || YH).slice();
    const a = new FV.Plot(FV.col(w.stage), { x: [0.4, 3.6], y: [0, 12], xTicks: [1, 2, 3], xLabel: L.obj, yLabel: L.vals, aspect: 0.82 });
    const b = new FV.Plot(FV.col(w.stage), { x: [0.4, 3.6], y: [0, 40], xTicks: [1, 2, 3], xLabel: L.obj, yLabel: L.ape, aspect: 0.82, title: L.apeT });
    const ro = FV.ui.readout(w.readout, [{ key: "m", label: "MAPE =", c: "orange" }, { key: "a", label: "MAE =" }]);
    const hs = Y.map((v, i) => a.handle(i + 1, yh[i], { c: "blue", onDrag: (x, y) => { yh[i] = Math.max(0, Math.round(y * 10) / 10); return [i + 1, yh[i]]; }, onChange: () => draw() }));
    function draw() {
      const ape = Y.map((v, i) => (100 * Math.abs(v - yh[i])) / v), m = mean(ape);
      a.clear();
      Y.forEach((v, i) => {
        a.line(i + 1, v, i + 1, yh[i], { c: "orange", w: 2.5 });
        a.dot(i + 1, v, { c: "ink", r: 5.5 });
        a.text(i + 1, (v + yh[i]) / 2, FV.fmt(Math.abs(v - yh[i]), 1) + " / " + v, { dx: 20, dy: 4, c: "orange" });
        hs[i].set(i + 1, yh[i]);
      });
      a.legend([{ label: L.fact, c: "ink", dot: true }, { label: L.pred, c: "blue", dot: true }, { label: L.err, c: "orange" }]);
      const top = Math.max(40, Math.ceil((Math.max(...ape, m) * 1.2) / 10) * 10);
      b.setDomain(null, [0, top]);
      b.clear();
      ape.forEach((v, i) => { b.bar(i + 1, v, { c: "orange", width: 0.5, opacity: 0.8 }); b.text(i + 1, v, pct(v), { anchor: "middle", dy: -6 }); });
      b.hline(m, { c: "ink", w: 1.8, dash: "6 4" });
      b.legend([{ label: L.apeI, c: "orange", box: true }, { label: "MAPE = " + pct(m), c: "ink", dash: true }]);
      ro.set("m", pct(m)); ro.set("a", FV.fmt(mean(Y.map((v, i) => Math.abs(v - yh[i]))), 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 2. Asymmetry: APE(ŷ) for a fixed y, sMAPE for comparison, and the derivatives.
  FV.widget("mape-asymmetry", (el, cfg) => {
    const w = FV.shell(el, {});
    const y = 100;
    const ape = (f) => (100 * Math.abs(f - y)) / y;
    const smape = (f) => (200 * Math.abs(f - y)) / (y + Math.abs(f));
    const dape = (f) => (f < y ? -100 / y : f > y ? 100 / y : NaN);
    const dsm = (f) => (f === y ? NaN : Math.sign(f - y) * (400 * y) / (y + f) ** 2);
    const p = new FV.Plot(w.stage, { x: [0, 300], y: [0, 220], xLabel: L.yhat, yLabel: L.loss, aspect: 0.5 });
    const d = new FV.Plot(w.stage, { x: [0, 300], y: [-4.5, 2.5], xLabel: L.yhat, yLabel: L.dloss, aspect: 0.28, minHeight: 170, maxHeight: 230 });
    let f = cfg.yhat != null ? cfg.yhat : 150;
    const ro = FV.ui.readout(w.readout, [{ key: "f", label: "ŷ =", c: "blue" }, { key: "q", label: L.ratio + " =" }, { key: "a", label: "APE =", c: "orange" }, { key: "s", label: "sMAPE =", c: "violet" }, { key: "m", label: L.apeMirror + " =", c: "teal" }]);
    const h = p.handle(f, ape(f), { c: "blue", onDrag: (x) => { f = FV.clamp(Math.round(x), 0, 300); return [f, ape(f)]; }, onChange: () => draw() });
    function draw() {
      p.clear();
      p.rect(0, 0, y, 220, { c: "teal", opacity: 0.06 });
      p.rect(y, 0, 300, 220, { c: "orange", opacity: 0.04 });
      p.hline(100, { c: "teal", w: 1.2, dash: "4 4" });
      p.text(4, 108, L.cap, { c: "teal" });
      p.text(y / 2, 165, L.under, { anchor: "middle", c: "faint" });
      p.text(y + 100, 165, L.over, { anchor: "middle", c: "faint" });
      p.vline(y, { c: "ink", w: 1, dash: "3 3" });
      p.fn(smape, { c: "violet", w: 2, dash: "6 4" });
      p.fn(ape, { c: "orange", w: 2.6 });
      const fm = f > 0 ? (y * y) / f : Infinity;
      if (fm <= 300) { p.dot(fm, ape(fm), { c: "teal", hollow: true, r: 5 }); p.line(fm, 0, fm, ape(fm), { c: "teal", w: 1, dash: "3 3" }); }
      p.line(f, 0, f, ape(f), { c: "blue", w: 1, dash: "3 3" });
      h.set(f, ape(f));
      p.legend([{ label: "APE = |y − ŷ| / y", c: "orange" }, { label: "sMAPE = 2|y − ŷ| / (|y| + |ŷ|)", c: "violet", dash: true }, { label: L.mirror, c: "teal", dot: true }]);
      d.clear();
      d.hline(0, { c: "guide", dash: false });
      d.line(0, -1, y, -1, { c: "orange", w: 2.4 }); d.line(y, 1, 300, 1, { c: "orange", w: 2.4 });
      d.dot(y, -1, { c: "orange", hollow: true, r: 3.5 }); d.dot(y, 1, { c: "orange", hollow: true, r: 3.5 });
      d.fn(dsm, { c: "violet", w: 2, dash: "6 4", jump: 2 });
      if (f !== y) d.dot(f, dape(f), { c: "orange" });
      d.legend([{ label: "APE′(ŷ) = ±100% / y", c: "orange" }, { label: "sMAPE′(ŷ)", c: "violet", dash: true }]);
      ro.set("f", String(f)); ro.set("q", FV.fmt(f / y, 2)); ro.set("a", pct(ape(f))); ro.set("s", pct(smape(f))); ro.set("m", Number.isFinite(fm) ? pct(ape(fm)) : "—");
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 3. APE over the (y, ŷ) plane: a 3D surface and a top view with rays of equal APE.
  FV.widget("mape-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const ape = (y, f) => (100 * Math.abs(y - f)) / Math.abs(y);
    const s3 = new FV.Surface(FV.col(w.stage), { f: ape, x: [0.25, 10], y: [0, 10], z: [0, 200], n: 60, labels: { x: "y", y: "ŷ", z: "APE, %" }, azimuth: -2.6, elevation: 0.45, aspect: 0.85, cmap: "viridis" });
    const t = new FV.Plot(FV.col(w.stage), { x: [0, 10], y: [0, 10], equal: true, xLabel: L.yAx, yLabel: L.yhAx, title: L.top });
    let P = (cfg.p || [2, 3]).slice();
    const Q = [8, 9];
    const ro = FV.ui.readout(w.readout, [{ key: "p", label: "P = (y; ŷ) =", c: "blue" }, { key: "e", label: L.errP }, { key: "a", label: L.apeP, c: "orange" }, { key: "q", label: L.apeQ }]);
    const h = t.handle(P[0], P[1], { c: "blue", onDrag: (x, y) => { P = [FV.clamp(Math.round(x * 10) / 10, 0.1, 10), Math.round(y * 10) / 10]; return P; }, onChange: () => draw() });
    const LV = [10, 25, 50, 100, 200];
    function draw() {
      t.clear();
      t.heat((x, y) => Math.min(ape(x, y), 400), { cmap: "viridis", z: [0, 200], res: 4, alpha: 0.5 });
      LV.forEach((a) => {
        const k = 1 + a / 100;
        t.line(0, 0, Math.min(10, 10 / k), Math.min(10, 10 / k) * k, { c: "ink", w: 1.2, opacity: 0.7 });
        if (a < 100) t.line(0, 0, 10, 10 * (1 - a / 100), { c: "ink", w: 1.2, opacity: 0.7 });
      });
      LV.forEach((a) => {
        const k = 1 + a / 100;
        if (a > 10) t.text(10 / k, 10, a + "%", { anchor: "middle", dy: -4, size: 11 });
        if (a < 100) t.text(10, 10 * (1 - a / 100), a + "%", { anchor: "end", dx: -4, dy: -4, size: 11 });
      });
      [1, 2].forEach((e) => { t.line(0, e, 10 - e, 10, { c: "red", w: 1.4, dash: "5 4" }); t.line(e, 0, 10, 10 - e, { c: "red", w: 1.4, dash: "5 4" }); });
      t.line(0, 0, 10, 10, { c: "ink", w: 2 });
      t.dot(Q[0], Q[1], { c: "ink", r: 5 }); t.text(Q[0], Q[1], "Q", { dx: 9, dy: 15 });
      t.text(P[0], P[1], "P", { dx: 15, dy: 20 });
      h.set(P[0], P[1]);
      t.legend([{ label: L.levels, c: "ink" }, { label: L.absLines, c: "red", dash: true }, { label: L.pP, c: "blue", dot: true }, { label: L.pQ, c: "ink", dot: true }]);
      s3.points = [{ x: P[0], y: P[1], z: ape(P[0], P[1]), c: "blue", r: 5.5, label: "P" }, { x: Q[0], y: Q[1], z: ape(Q[0], Q[1]), c: "ink", r: 5, label: "Q" }];
      s3.paths = [{ pts: FV.linspace(0.25, 10, 30).map((v) => [v, v, 0]), c: "orange", w: 2.5 }];
      s3.draw();
      ro.set("p", "(" + FV.fmt(P[0], 1) + (FV.lang === "en" ? ", " : "; ") + FV.fmt(P[1], 1) + ")");
      ro.set("e", FV.fmt(Math.abs(P[0] - P[1]), 1)); ro.set("a", pct(ape(P[0], P[1]))); ro.set("q", pct(ape(Q[0], Q[1])));
    }
    t.onresize = draw; draw();
  });

  // 4. The MAPE-optimal constant forecast is a weighted median, biased low.
  FV.widget("mape-optimal", (el, cfg) => {
    const w = FV.shell(el, {});
    const N = 60, r = FV.rng(21), Z = Array.from({ length: N }, () => r.normal());
    const p = new FV.Plot(w.stage, { x: [0, 250], y: [0, 150], xLabel: L.c, yLabel: "MAPE(c), %", aspect: 0.48 });
    const d = new FV.Plot(w.stage, { x: [0, 250], y: [-1.5, 1.5], xLabel: L.c, yLabel: L.dmape, aspect: 0.28, minHeight: 170, maxHeight: 230 });
    const ss = FV.ui.slider({ label: L.sigma, min: 0.1, max: 1.2, step: 0.05, value: cfg.sigma || 0.6, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(ss.el);
    let c = cfg.c != null ? cfg.c : 100;
    const ro = FV.ui.readout(w.readout, [
      { key: "c", label: "c =", c: "blue" }, { key: "m", label: "MAPE(c) =" }, { key: "o", label: "c* =", c: "orange" }, { key: "om", label: "MAPE(c*) =", c: "orange" },
      { key: "md", label: L.median + " =", c: "teal" }, { key: "mn", label: L.mean + " =" }, { key: "r", label: L.rel }, { key: "t", label: L.theory },
    ]);
    let y = [];
    const mape = (cc) => (100 / N) * y.reduce((s, v) => s + Math.abs(v - cc) / v, 0);
    const slope = (cc) => (100 / N) * y.reduce((s, v) => s + Math.sign(cc - v) / v, 0);
    const h = p.handle(c, 0, { c: "blue", onDrag: (x) => { c = FV.clamp(Math.round(x), 0, 250); return [c, Math.min(mape(c), 150)]; }, onChange: () => draw() });
    function draw() {
      const sg = ss.value;
      y = Z.map((z) => 100 * Math.exp(sg * z)).sort((a, b) => a - b);
      const W = y.reduce((s, v) => s + 1 / v, 0);
      let acc = 0, copt = y[0];
      for (const v of y) { acc += 1 / v; if (acc >= W / 2 - 1e-12) { copt = v; break; } }
      const med = (y[N / 2 - 1] + y[N / 2]) / 2, mn = mean(y);
      p.clear();
      p.vline(mn, { c: "guide", w: 1.6, dash: "6 4" });
      p.vline(med, { c: "teal", w: 1.8, dash: "6 4" });
      p.vline(copt, { c: "orange", w: 1.8, dash: false });
      p.hline(100, { c: "faint", w: 1, dash: "2 4" });
      p.fn(mape, { c: "ink", w: 2.4, n: 500 });
      y.forEach((v) => { if (v <= 250) p.line(v, 0, v, 6, { c: "ink", w: 1.2, opacity: 0.6 }); });
      p.dot(copt, mape(copt), { c: "orange", r: 5 });
      h.set(c, Math.min(mape(c), 150));
      p.legend([{ label: "MAPE(c)", c: "ink" }, { label: L.copt, c: "orange" }, { label: L.median, c: "teal", dash: true }, { label: L.mean, c: "guide", dash: true }, { label: L.data, c: "ink", box: true }]);
      const lim = Math.max(1.2, Math.ceil(slope(0) * -1.15 * 2) / 2);
      d.setDomain(null, [-lim, lim]);
      d.clear();
      d.hline(0, { c: "guide", dash: false });
      d.vline(copt, { c: "orange", w: 1.4, dash: "4 3" });
      const pts = [];
      let prev = 0;
      y.concat([250]).forEach((v) => { const s0 = slope((prev + Math.min(v, 250)) / 2); pts.push([prev, s0], [Math.min(v, 250), s0]); prev = Math.min(v, 250); });
      d.path(pts.filter((q) => q[0] <= 250), { c: "orange", w: 2.2 });
      d.dot(c, slope(c), { c: "blue", r: 4.5 });
      d.legend([{ label: "∂MAPE/∂c = (100% / n) · Σ sign(c − yᵢ) / yᵢ", c: "orange" }]);
      ro.set("c", String(c)); ro.set("m", pct(mape(c))); ro.set("o", FV.fmt(copt, 1)); ro.set("om", pct(mape(copt)));
      ro.set("md", FV.fmt(med, 1)); ro.set("mn", FV.fmt(mn, 1)); ro.set("r", pct(100 * (copt / med - 1))); ro.set("t", pct(100 * (Math.exp(-sg * sg) - 1)));
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // Weekly demand (deterministic) for the metric comparison.
  function demand() {
    const r = FV.rng(8), y = [], base = [];
    for (let t = 0; t < 52; t++) { const b = 60 + 30 * Math.sin((2 * Math.PI * t) / 26) + 0.5 * t; base.push(b); y.push(Math.max(1, Math.round(b * Math.exp(0.25 * r.normal())))); }
    return { y, base };
  }

  // 5. MAPE vs sMAPE vs WAPE vs MASE as functions of a forecast multiplier.
  FV.widget("mape-metrics", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const D = demand(), T = 52;
    const a = new FV.Plot(FV.col(w.stage), { x: [0, 53], y: [0, 220], xLabel: L.week, yLabel: L.sales, aspect: 0.75 });
    const b = new FV.Plot(FV.col(w.stage), { x: [0.5, 1.5], y: [0, 80], xLabel: L.kAx, yLabel: L.metric, aspect: 0.75 });
    const sk = FV.ui.slider({ label: L.k, min: 0.5, max: 1.5, step: 0.01, value: cfg.k || 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const dip = FV.ui.check({ label: L.dip, checked: !!cfg.dip, onchange: () => { cache = null; draw(); } });
    w.controls.append(sk.el, dip.el);
    const ro = FV.ui.readout(w.readout, [
      { key: "m", label: "MAPE =", c: "orange" }, { key: "s", label: "sMAPE =", c: "violet" }, { key: "w", label: "WAPE =", c: "teal" }, { key: "x", label: "MASE =" },
      { key: "km", label: "k*(MAPE) =", c: "orange" }, { key: "ks", label: "k*(sMAPE) =", c: "violet" }, { key: "kw", label: "k*(WAPE) =", c: "teal" },
    ]);
    const Ys = () => { const y = D.y.slice(); if (dip.value) y[40] = 3; return y; };
    function metrics(k, y) {
      let ape = 0, sm = 0, ae = 0, sy = 0, sc = 0;
      for (let t = 0; t < T; t++) { const f = k * D.base[t], e = Math.abs(y[t] - f); ape += e / Math.abs(y[t]); sm += (2 * e) / (Math.abs(y[t]) + Math.abs(f)); ae += e; sy += Math.abs(y[t]); }
      for (let t = 1; t < T; t++) sc += Math.abs(y[t] - y[t - 1]);
      return { mape: (100 * ape) / T, smape: (100 * sm) / T, wape: (100 * ae) / sy, mase: ae / T / (sc / (T - 1)) };
    }
    let cache = null;
    function curves() {
      if (cache) return cache;
      const y = Ys(), ks = FV.linspace(0.5, 1.5, 1001), M = ks.map((k) => metrics(k, y));
      const best = {};
      ["mape", "smape", "wape"].forEach((key) => { let j = 0; M.forEach((m, i) => { if (m[key] < M[j][key]) j = i; }); best[key] = [ks[j], M[j][key]]; });
      const top = Math.ceil(Math.max(...M.map((m) => Math.max(m.mape, m.smape, m.wape))) / 10) * 10;
      return (cache = { y, ks, M, best, top });
    }
    function draw() {
      const C = curves(), k = sk.value, y = C.y, m = metrics(k, y);
      a.clear();
      a.path(D.base.map((v, t) => [t + 1, k * v]), { c: "blue", w: 2.4 });
      y.forEach((v, t) => a.dot(t + 1, v, { c: dip.value && t === 40 ? "red" : "ink", r: dip.value && t === 40 ? 5 : 3.5 }));
      a.legend([{ label: L.sales + " y", c: "ink", dot: true }, { label: L.fc, c: "blue" }]);
      b.setDomain(null, [0, Math.min(150, Math.max(60, C.top))]);
      b.clear();
      b.vline(k, { c: "blue", w: 1.4, dash: "4 3" });
      const ser = (key) => C.ks.map((kk, i) => [kk, C.M[i][key]]);
      b.path(ser("wape"), { c: "teal", w: 2.2 });
      b.path(ser("smape"), { c: "violet", w: 2.2, dash: "6 4" });
      b.path(ser("mape"), { c: "orange", w: 2.6 });
      [["mape", "orange"], ["smape", "violet"], ["wape", "teal"]].forEach(([key, c]) => b.dot(C.best[key][0], C.best[key][1], { c, r: 5 }));
      b.legend([{ label: "MAPE", c: "orange" }, { label: "sMAPE", c: "violet", dash: true }, { label: "WAPE", c: "teal" }, { label: L.best, c: "ink", dot: true }]);
      ro.set("m", pct(m.mape)); ro.set("s", pct(m.smape)); ro.set("w", pct(m.wape)); ro.set("x", FV.fmt(m.mase, 3));
      ro.set("km", FV.fmt(C.best.mape[0], 3)); ro.set("ks", FV.fmt(C.best.smape[0], 3)); ro.set("kw", FV.fmt(C.best.wape[0], 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 6. Training a linear model y ≈ w·x by subgradient descent on MAPE.
  FV.widget("mape-training", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const N = 40, r = FV.rng(34), P = [];
    for (let i = 0; i < N; i++) { const x = 1 + 9 * r(); P.push({ x, y: 10 * x * Math.exp(0.35 * r.normal()) }); }
    const mape = (k) => (100 / N) * P.reduce((s, p) => s + Math.abs(p.y - k * p.x) / p.y, 0);
    const bias = (k) => (100 * P.reduce((s, p) => s + (k * p.x - p.y), 0)) / P.reduce((s, p) => s + p.y, 0);
    const ols = P.reduce((s, p) => s + p.x * p.y, 0) / P.reduce((s, p) => s + p.x * p.x, 0);
    const wmax = Math.max(...P.map((p) => 1 / p.y));
    const a = new FV.Plot(FV.col(w.stage), { x: [0, 10.5], y: [0, 180], xLabel: L.x, yLabel: L.yv, aspect: 0.8 });
    const b = new FV.Plot(FV.col(w.stage), { x: [3, 14], y: [0, 70], xLabel: L.wAx, yLabel: "MAPE, %", aspect: 0.8 });
    const W0 = cfg.w0 || 4, ETA = 8, MAXS = 80;
    let k = W0, step = 0, hist = [W0];
    const player = FV.ui.player({
      interval: 90,
      onstep() {
        if (step >= MAXS) return false;
        let g = 0; P.forEach((p) => { g += (Math.sign(k * p.x - p.y) * p.x) / p.y; }); g /= N;
        k -= (ETA * g) / Math.sqrt(step + 1); step++; hist.push(k);
        draw();
        return step < MAXS;
      },
      onreset() { k = W0; step = 0; hist = [W0]; draw(); },
    });
    w.controls.append(player.el);
    const ro = FV.ui.readout(w.readout, [
      { key: "s", label: L.step + " =" }, { key: "w", label: "w =", c: "orange" }, { key: "m", label: "MAPE =", c: "orange" }, { key: "b", label: L.bias + " =", c: "orange" },
      { key: "ow", label: L.olsW, c: "blue" }, { key: "om", label: "MAPE =", c: "blue" }, { key: "ob", label: L.bias + " =", c: "blue" },
    ]);
    function draw() {
      a.clear();
      a.line(0, 0, 10.5, 105, { c: "guide", w: 1.4, dash: "6 5" });
      a.line(0, 0, 10.5, 10.5 * ols, { c: "blue", w: 2.2 });
      a.line(0, 0, 10.5, 10.5 * k, { c: "orange", w: 2.6 });
      P.forEach((p) => a.dot(p.x, p.y, { c: "ink", r: 2.2 + (5 * (1 / p.y)) / wmax }));
      a.legend([{ label: L.mapeModel, c: "orange" }, { label: L.olsModel, c: "blue" }, { label: L.truth, c: "guide", dash: true }, { label: L.size, c: "ink", dot: true }]);
      b.clear();
      b.fn(mape, { c: "ink", w: 2.2, n: 600 });
      b.path(hist.map((v) => [v, mape(v)]), { c: "orange", w: 1.2, opacity: 0.6 });
      b.dot(ols, mape(ols), { c: "blue", r: 5 });
      b.dot(k, mape(k), { c: "orange", r: 5.5 });
      b.legend([{ label: L.mapeW, c: "ink" }, { label: "w (MAPE)", c: "orange", dot: true }, { label: "w (MSE)", c: "blue", dot: true }]);
      ro.set("s", String(step)); ro.set("w", FV.fmt(k, 3)); ro.set("m", pct(mape(k), 2)); ro.set("b", pct(bias(k)));
      ro.set("ow", FV.fmt(ols, 3)); ro.set("om", pct(mape(ols), 2)); ro.set("ob", pct(bias(ols)));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 7. A product portfolio: one slow mover dominates MAPE, WAPE barely notices it.
  FV.widget("mape-portfolio", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const names = ["A", "B", "C", "D", "E", "F"];
    const Ybase = [1200, 800, 450, 200, 60, 4], F = [1100, 860, 400, 230, 50, 10];
    const xt = names.map((n, i) => ({ v: i + 1, label: n }));
    const a = new FV.Plot(FV.col(w.stage), { x: [0.4, 6.6], y: [1, 3000], yType: "log", xTicks: xt, xLabel: L.sku, yLabel: L.vol, aspect: 0.8 });
    const b = new FV.Plot(FV.col(w.stage), { x: [0.4, 6.6], y: [0, 160], xTicks: xt, xLabel: L.sku, yLabel: L.ape, aspect: 0.8 });
    const sf = FV.ui.slider({ label: L.slowF, min: 1, max: 60, step: 1, value: cfg.f || 4, fmt: (v) => String(v), oninput: draw });
    w.controls.append(sf.el);
    const ro = FV.ui.readout(w.readout, [{ key: "m", label: "MAPE =", c: "orange" }, { key: "m5", label: L.mapeNoF }, { key: "w", label: "WAPE =", c: "teal" }, { key: "s", label: L.shareF }]);
    function draw() {
      const y = Ybase.slice(); y[5] = sf.value;
      const ape = y.map((v, i) => (100 * Math.abs(v - F[i])) / v), m = mean(ape);
      const wape = (100 * y.reduce((s, v, i) => s + Math.abs(v - F[i]), 0)) / y.reduce((s, v) => s + v, 0);
      a.clear();
      y.forEach((v, i) => { a.rect(i + 1 - 0.36, 1, i + 1 - 0.02, v, { c: "faint", opacity: 0.5 }); a.rect(i + 1 + 0.02, 1, i + 1 + 0.36, F[i], { c: "blue", opacity: 0.85 }); });
      a.legend([{ label: L.actual, c: "faint", box: true }, { label: L.fcst, c: "blue", box: true }]);
      const top = Math.max(60, Math.ceil((Math.max(...ape) * 1.18) / 20) * 20);
      b.setDomain(null, [0, top]);
      b.clear();
      ape.forEach((v, i) => { b.bar(i + 1, v, { c: "orange", width: 0.55, opacity: 0.8 }); b.text(i + 1, v, FV.fmt(v, v >= 100 ? 0 : 1), { anchor: "middle", dy: -5, size: 11 }); });
      b.hline(m, { c: "ink", w: 1.8, dash: "6 4" });
      b.hline(wape, { c: "teal", w: 1.8, dash: "6 4" });
      b.legend([{ label: "APE", c: "orange", box: true }, { label: "MAPE", c: "ink", dash: true }, { label: "WAPE", c: "teal", dash: true }]);
      ro.set("m", pct(m)); ro.set("m5", pct(mean(ape.slice(0, 5)))); ro.set("w", pct(wape)); ro.set("s", pct((100 * ape[5]) / ape.reduce((s, v) => s + v, 0), 0));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });
})();
