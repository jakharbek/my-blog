/* Widgets of the formula page "RMSE". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      obj: "объект i", vals: "y, ŷ", fact: "факт y", pred: "прогноз ŷ (тяните)", err: "ошибка r = y − ŷ",
      sq: "квадраты ошибок r²ᵢ", sqTitle: "Квадраты ошибок, вложенные в угол", rmseSq: "квадрат со стороной RMSE", maeSq: "квадрат со стороной MAE",
      dist: "Распределение", normal: "нормальное", laplace: "Лаплас", uniform: "равномерное", eps: "Доля выбросов (×10) $\\varepsilon$",
      errs: "ошибки r", dens: "плотность", outside: "за рамкой", ratio: "RMSE / MAE", theory: "теория",
      r1: "r₁", r2: "r₂", plane: "Две ошибки: плоскость (r₁; r₂)", diamond: "MAE = const (ромб)", circle: "RMSE через точку",
      bounds: "RMSE = MAE и RMSE = √2·MAE", diag: "|r₁| = |r₂|", nObj: "Объектов $n$", kObj: "Ошибка в $k$ объектах",
      kAxis: "k — сколько объектов несут ошибку", conc: "Отношение RMSE/MAE = √(n/k)",
      axis: "i = ", y: "факт y", yhat: "прогноз ŷ", const: "лучшая константа ȳ·1", diagL: "константные прогнозы", sphere: "Показать сферу RMSE = const",
      setConst: "ŷ = ȳ·1", setEx: "ŷ из примера", norm: "‖y − ŷ‖ =", rmseConst: "RMSE константы =",
      c: "константный прогноз c", loss: "потеря", dloss: "производная", tangent: "касательная", asym: "асимптоты |c − ȳ|", data: "данные yᵢ",
      bias: "Смещение $\\bar r$", sd: "Разброс $\\sigma_r$", idx: "объект i", resid: "остаток rᵢ", mean: "среднее r̄", band: "r̄ ± σ",
      tri: "RMSE² = r̄² + σ²", legBias: "|r̄|", legSd: "σ",
      w: "вес w", b: "сдвиг b", surf: "Поверхность", eta: "Шаг $\\eta$", gdMse: "спуск по MSE", gdRmse: "спуск по RMSE", start: "старт (тяните)",
      opt: "минимум", step: "шаг", curve: "RMSE по шагам", top: "Вид сверху: линии уровня RMSE",
      yTrue: "Факт $y$", yhatL: "прогноз ŷ", sle: "(ln(1+ŷ) − ln(1+y))²", mirror: "зеркально: тот же промах вверх", dsle: "производная по ŷ",
      ratioW: "во сколько раз больше",
    },
    en: {
      obj: "object i", vals: "y, ŷ", fact: "actual y", pred: "forecast ŷ (drag)", err: "error r = y − ŷ",
      sq: "squared errors r²ᵢ", sqTitle: "Squared errors nested in a corner", rmseSq: "square with side RMSE", maeSq: "square with side MAE",
      dist: "Distribution", normal: "normal", laplace: "Laplace", uniform: "uniform", eps: "Outlier share (×10) $\\varepsilon$",
      errs: "errors r", dens: "density", outside: "outside", ratio: "RMSE / MAE", theory: "theory",
      r1: "r₁", r2: "r₂", plane: "Two errors: the (r₁, r₂) plane", diamond: "MAE = const (diamond)", circle: "RMSE through the point",
      bounds: "RMSE = MAE and RMSE = √2·MAE", diag: "|r₁| = |r₂|", nObj: "Objects $n$", kObj: "Error in $k$ objects",
      kAxis: "k — how many objects carry the error", conc: "Ratio RMSE/MAE = √(n/k)",
      axis: "i = ", y: "actual y", yhat: "forecast ŷ", const: "best constant ȳ·1", diagL: "constant forecasts", sphere: "Show the sphere RMSE = const",
      setConst: "ŷ = ȳ·1", setEx: "ŷ from the example", norm: "‖y − ŷ‖ =", rmseConst: "RMSE of the constant =",
      c: "constant forecast c", loss: "loss", dloss: "derivative", tangent: "tangent", asym: "asymptotes |c − ȳ|", data: "data yᵢ",
      bias: "Bias $\\bar r$", sd: "Spread $\\sigma_r$", idx: "object i", resid: "residual rᵢ", mean: "mean r̄", band: "r̄ ± σ",
      tri: "RMSE² = r̄² + σ²", legBias: "|r̄|", legSd: "σ",
      w: "weight w", b: "bias b", surf: "Surface", eta: "Step $\\eta$", gdMse: "descent on MSE", gdRmse: "descent on RMSE", start: "start (drag)",
      opt: "minimum", step: "step", curve: "RMSE by step", top: "Top view: RMSE level lines",
      yTrue: "Actual $y$", yhatL: "forecast ŷ", sle: "(ln(1+ŷ) − ln(1+y))²", mirror: "mirror: the same miss upwards", dsle: "derivative in ŷ",
      ratioW: "times larger",
    },
    uz: {
      obj: "obyekt i", vals: "y, ŷ", fact: "haqiqiy y", pred: "bashorat ŷ (torting)", err: "xato r = y − ŷ",
      sq: "xatolar kvadratlari r²ᵢ", sqTitle: "Burchakka joylangan xato kvadratlari", rmseSq: "tomoni RMSE bo‘lgan kvadrat", maeSq: "tomoni MAE bo‘lgan kvadrat",
      dist: "Taqsimot", normal: "normal", laplace: "Laplas", uniform: "tekis", eps: "Chetlanishlar ulushi (×10) $\\varepsilon$",
      errs: "xatolar r", dens: "zichlik", outside: "ramkadan tashqarida", ratio: "RMSE / MAE", theory: "nazariya",
      r1: "r₁", r2: "r₂", plane: "Ikki xato: (r₁; r₂) tekisligi", diamond: "MAE = const (romb)", circle: "nuqtadan o‘tuvchi RMSE",
      bounds: "RMSE = MAE va RMSE = √2·MAE", diag: "|r₁| = |r₂|", nObj: "Obyektlar $n$", kObj: "Xato $k$ ta obyektda",
      kAxis: "k — xatoni nechta obyekt ko‘taradi", conc: "RMSE/MAE nisbati = √(n/k)",
      axis: "i = ", y: "haqiqiy y", yhat: "bashorat ŷ", const: "eng yaxshi konstanta ȳ·1", diagL: "konstant bashoratlar", sphere: "RMSE = const sferasini ko‘rsatish",
      setConst: "ŷ = ȳ·1", setEx: "misoldagi ŷ", norm: "‖y − ŷ‖ =", rmseConst: "konstanta RMSE’i =",
      c: "konstant bashorat c", loss: "yo‘qotish", dloss: "hosila", tangent: "urinma", asym: "asimptotalar |c − ȳ|", data: "ma’lumotlar yᵢ",
      bias: "Siljish $\\bar r$", sd: "Tarqoqlik $\\sigma_r$", idx: "obyekt i", resid: "qoldiq rᵢ", mean: "o‘rtacha r̄", band: "r̄ ± σ",
      tri: "RMSE² = r̄² + σ²", legBias: "|r̄|", legSd: "σ",
      w: "vazn w", b: "siljish b", surf: "Sirt", eta: "Qadam $\\eta$", gdMse: "MSE bo‘yicha tushish", gdRmse: "RMSE bo‘yicha tushish", start: "start (torting)",
      opt: "minimum", step: "qadam", curve: "qadamlar bo‘yicha RMSE", top: "Yuqoridan ko‘rinish: RMSE sath chiziqlari",
      yTrue: "Haqiqiy $y$", yhatL: "bashorat ŷ", sle: "(ln(1+ŷ) − ln(1+y))²", mirror: "ko‘zgu: xuddi shu xato yuqoriga", dsle: "ŷ bo‘yicha hosila",
      ratioW: "necha marta katta",
    },
  }[FV.lang] || {};

  const Y = [3, 5, 8], YH = [2.5, 5, 10];
  const mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
  const stats = (r) => {
    const mae = mean(r.map(Math.abs)), mse = mean(r.map((v) => v * v));
    return { mae, mse, rmse: Math.sqrt(mse) };
  };

  // 1. Squares of the errors: RMSE is the side of the square whose area is the mean area.
  FV.widget("rmse-squares", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const yh = (cfg.yhat || YH).slice();
    const a = new FV.Plot(FV.col(w.stage), { x: [0.4, 3.6], y: [0, 12], xTicks: [1, 2, 3], xLabel: L.obj, yLabel: L.vals, aspect: 0.82 });
    const bcol = FV.col(w.stage);
    const b = new FV.Plot(bcol, { x: [0, 2.5], y: [0, 2.5], equal: true, xLabel: "|r|", title: L.sqTitle });
    const ro = FV.ui.readout(w.readout, [{ key: "mae", label: "MAE =", c: "teal" }, { key: "mse", label: "MSE =" }, { key: "rmse", label: "RMSE =", c: "blue" }, { key: "k", label: L.ratio + " =" }]);
    const hs = Y.map((v, i) => a.handle(i + 1, yh[i], { c: "blue", label: "ŷ" + (i + 1), onDrag: (x, y) => { yh[i] = Math.round(y * 10) / 10; return [i + 1, yh[i]]; }, onChange: () => draw() }));
    function draw() {
      const r = Y.map((v, i) => v - yh[i]), s = stats(r);
      a.clear();
      Y.forEach((v, i) => {
        a.line(i + 1, v, i + 1, yh[i], { c: "orange", w: 2.5 });
        a.dot(i + 1, v, { c: "ink", r: 5.5 });
        a.text(i + 1, v, FV.fmt(r[i], 1), { dx: 20, dy: 4, c: "orange" });
        hs[i].set(i + 1, yh[i]);
      });
      a.legend([{ label: L.fact, c: "ink", dot: true }, { label: L.pred, c: "blue", dot: true }, { label: L.err, c: "orange" }]);
      const D = Math.max(2.5, Math.ceil(Math.max(...r.map(Math.abs)) * 1.15 * 2) / 2);
      b.setDomain([0, D], [0, D]);
      b.clear();
      r.map(Math.abs).sort((p, q) => q - p).forEach((v) => { if (v > 0) b.path([[0, 0], [v, 0], [v, v], [0, v]], { close: true, fill: true, c: "orange", fillOpacity: 0.1, w: 1.6 }); });
      b.path([[0, 0], [s.mae, 0], [s.mae, s.mae], [0, s.mae]], { close: true, c: "teal", w: 1.8, dash: "5 4" });
      b.path([[0, 0], [s.rmse, 0], [s.rmse, s.rmse], [0, s.rmse]], { close: true, c: "blue", w: 2.6 });
      b.legend([{ label: L.sq, c: "orange", box: true }, { label: L.rmseSq, c: "blue" }, { label: L.maeSq, c: "teal", dash: true }]);
      ro.set("mae", FV.fmt(s.mae, 3)); ro.set("mse", FV.fmt(s.mse, 3)); ro.set("rmse", FV.fmt(s.rmse, 3)); ro.set("k", s.mae > 0 ? FV.fmt(s.rmse / s.mae, 3) : "—");
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 2. RMSE versus MAE for different error distributions and outliers.
  FV.widget("rmse-vs-mae", (el, cfg) => {
    const w = FV.shell(el, {});
    const N = 2000, BW = 0.25;
    const p = new FV.Plot(w.stage, { x: [-6, 6], y: [0, 0.8], xLabel: L.errs, yLabel: L.dens, aspect: 0.45 });
    const MAE0 = { normal: Math.sqrt(2 / Math.PI), laplace: 1 / Math.SQRT2, uniform: Math.sqrt(3) / 2 };
    const cache = {};
    function sample(kind) {
      if (cache[kind]) return cache[kind];
      const r = FV.rng(5), out = [];
      for (let i = 0; i < N; i++) {
        const u = r();
        let e;
        if (kind === "normal") e = r.normal();
        else if (kind === "laplace") { const v = Math.min(r(), 1 - 1e-12) - 0.5; e = (-Math.sign(v) * Math.log(1 - 2 * Math.abs(v))) / Math.SQRT2; }
        else e = (2 * r() - 1) * Math.sqrt(3);
        out.push({ u, e });
      }
      return (cache[kind] = out);
    }
    const dist = FV.ui.seg({ label: L.dist, value: cfg.dist || "normal", options: [{ value: "normal", label: L.normal }, { value: "laplace", label: L.laplace }, { value: "uniform", label: L.uniform }], onchange: draw });
    const se = FV.ui.slider({ label: L.eps, min: 0, max: 0.2, step: 0.01, value: cfg.eps || 0, fmt: (v) => Math.round(v * 100) + "%", oninput: draw });
    w.controls.append(dist.el, se.el);
    const ro = FV.ui.readout(w.readout, [{ key: "mae", label: "MAE =", c: "teal" }, { key: "rmse", label: "RMSE =", c: "orange" }, { key: "k", label: L.ratio + " =" }, { key: "t", label: L.theory + " =" }]);
    function draw() {
      const kind = dist.value, eps = se.value, s = sample(kind);
      const bins = new Array(48).fill(0);
      let a = 0, q = 0, out = 0;
      s.forEach(({ u, e }) => {
        const x = u < eps ? 10 * e : e;
        a += Math.abs(x); q += x * x;
        if (Math.abs(x) >= 6) out++; else bins[Math.floor((x + 6) / BW)]++;
      });
      const mae = a / N, rmse = Math.sqrt(q / N);
      p.clear();
      bins.forEach((c, i) => { if (c) p.rect(-6 + i * BW + 0.02, 0, -6 + (i + 1) * BW - 0.02, c / (N * BW), { c: "faint", opacity: 0.35 }); });
      [-1, 1].forEach((sg) => {
        p.vline(sg * mae, { c: "teal", w: 2, dash: "6 4" });
        p.vline(sg * rmse, { c: "orange", w: 2.4, dash: false });
      });
      if (out) p.text(5.9, 0.76, L.outside + ": " + out, { anchor: "end", c: "faint" });
      p.legend([{ label: L.errs, c: "faint", box: true }, { label: "± MAE", c: "teal", dash: true }, { label: "± RMSE", c: "orange" }]);
      const th = Math.sqrt(1 + 99 * eps) / ((1 + 9 * eps) * MAE0[kind]);
      ro.set("mae", FV.fmt(mae, 3)); ro.set("rmse", FV.fmt(rmse, 3)); ro.set("k", FV.fmt(rmse / mae, 3)); ro.set("t", FV.fmt(th, 3));
    }
    p.onresize = draw; draw();
  });

  // 3. MAE ≤ RMSE ≤ √n·MAE: the diamond and the circle; the ratio √(n/k).
  FV.widget("rmse-bounds", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-3, 3], y: [-3, 3], equal: true, xLabel: L.r1, yLabel: L.r2, title: L.plane });
    const b = new FV.Plot(FV.col(w.stage), { x: [0.5, 10.5], y: [0, 4], xLabel: L.kAxis, yLabel: "RMSE / MAE", aspect: 0.9, title: L.conc });
    let P = cfg.r || [0.5, -2];
    const sn = FV.ui.slider({ label: L.nObj, min: 2, max: 30, step: 1, value: cfg.n || 10, fmt: (v) => String(v), oninput: () => { sk.input.max = sn.value; if (sk.value > sn.value) sk.set(sn.value); draw(); } });
    const sk = FV.ui.slider({ label: L.kObj, min: 1, max: cfg.n || 10, step: 1, value: cfg.k || 1, fmt: (v) => String(v), oninput: draw });
    w.controls.append(sn.el, sk.el);
    const ro = FV.ui.readout(w.readout, [{ key: "mae", label: "MAE =", c: "teal" }, { key: "rmse", label: "RMSE =", c: "orange" }, { key: "k", label: L.ratio + " =" }, { key: "c", label: "√(n/k) =", c: "blue" }]);
    const h = a.handle(P[0], P[1], { c: "blue", onDrag: (x, y) => { P = [Math.round(x * 20) / 20, Math.round(y * 20) / 20]; return P; }, onChange: () => draw() });
    const circ = (R) => FV.linspace(0, 2 * Math.PI, 121).map((t) => [R * Math.cos(t), R * Math.sin(t)]);
    function draw() {
      const mae = (Math.abs(P[0]) + Math.abs(P[1])) / 2, rmse = Math.sqrt((P[0] ** 2 + P[1] ** 2) / 2);
      a.clear();
      a.line(-3, -3, 3, 3, { c: "guide", w: 1, dash: "3 4" }); a.line(-3, 3, 3, -3, { c: "guide", w: 1, dash: "3 4" });
      if (mae > 0) {
        const m = 2 * mae;
        a.path(circ(Math.SQRT2 * mae), { c: "faint", w: 1, opacity: 0.8 });
        a.path(circ(m), { c: "faint", w: 1, opacity: 0.8 });
        a.path([[m, 0], [0, m], [-m, 0], [0, -m]], { close: true, c: "teal", w: 2, dash: "6 4", fill: true, fillOpacity: 0.06 });
        a.path(circ(Math.SQRT2 * rmse), { c: "orange", w: 2.4 });
      }
      a.line(0, 0, P[0], P[1], { c: "blue", w: 1.4, dash: "3 3" });
      h.set(P[0], P[1]);
      a.legend([{ label: L.diamond, c: "teal", dash: true }, { label: L.circle, c: "orange" }, { label: L.bounds, c: "faint" }, { label: L.diag, c: "guide", dash: true }]);
      const n = sn.value, k = Math.min(sk.value, n);
      b.setDomain([0.5, n + 0.5], [0, Math.ceil(Math.sqrt(n) * 1.15 * 2) / 2]);
      b.clear();
      b.hline(1, { c: "teal", w: 1.4, dash: "6 4" });
      b.fn((x) => Math.sqrt(n / x), { c: "guide", w: 1.2, from: 1, to: n });
      for (let j = 1; j <= n; j++) b.dot(j, Math.sqrt(n / j), { c: j === k ? "blue" : "faint", r: j === k ? 6 : n > 15 ? 2.5 : 3.5 });
      b.text(1, Math.sqrt(n), "√n = " + FV.fmt(Math.sqrt(n), 2), { dx: 10, dy: 4 });
      b.legend([{ label: "√(n/k)", c: "faint", dot: true }, { label: "RMSE = MAE", c: "teal", dash: true }]);
      ro.set("mae", FV.fmt(mae, 3)); ro.set("rmse", FV.fmt(rmse, 3)); ro.set("k", mae > 0 ? FV.fmt(rmse / mae, 3) : "—"); ro.set("c", FV.fmt(Math.sqrt(n / k), 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // A small rotatable 3D scene (points and segments) for the vector picture; FV.Surface draws only graphs z = f(x, y).
  function Scene3D(parent, o) {
    const S = { az: o.azimuth != null ? o.azimuth : -0.9, el: o.elevation != null ? o.elevation : 0.42, items: () => [] };
    const wrap = FV.h("div", { class: "fv-3d" });
    if (o.title) { const t = FV.rich(o.title, "div"); t.className = "fv-plot-title"; wrap.append(t); }
    const canvas = FV.h("canvas", { role: "img", "aria-label": o.ariaLabel || "" });
    const reset = () => { S.az = o.azimuth != null ? o.azimuth : -0.9; S.el = o.elevation != null ? o.elevation : 0.42; S.draw(); };
    wrap.append(canvas, FV.h("div", { class: "fv-3d-hint" }, FV.h("span", { text: "⟲ " + FV.t("drag") }), FV.h("button", { type: "button", class: "fv-link", text: FV.t("reset"), onclick: reset })));
    parent.append(wrap);
    const lo = o.range[0], hi = o.range[1];
    let W = 600, H = 400, dpr = 1, sc = 100, cy = 200;
    const nrm = (v) => v.map((c) => ((c - lo) / (hi - lo)) * 2 - 1);
    const proj = (n) => {
      const ca = Math.cos(S.az), sa = Math.sin(S.az), ce = Math.cos(S.el), se = Math.sin(S.el);
      const xr = n[0] * ca - n[1] * sa, yr = n[0] * sa + n[1] * ca;
      return [W / 2 + xr * sc, cy - (n[2] * ce + yr * se) * sc, yr * ce - n[2] * se];
    };
    const P = (v) => proj(nrm(v));
    S.resize = () => {
      W = Math.max(260, wrap.clientWidth || 600);
      H = FV.clamp(Math.round(W * (o.aspect || 0.75)), 260, 480);
      dpr = Math.min(2, window.devicePixelRatio || 1);
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      canvas.style.width = W + "px"; canvas.style.height = H + "px";
      S.draw();
    };
    S.draw = () => {
      const ctx = canvas.getContext("2d");
      const halfH = Math.cos(S.el) + Math.SQRT2 * Math.sin(S.el);
      sc = Math.min((W - 2 * 44) / (2 * Math.SQRT2), (H - 2 * 30) / (2 * halfH)); cy = H / 2;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
      ctx.font = `12px ${FV.css("sans") || "sans-serif"}`;
      const seg = (A, B, col, lw, dash, alpha) => {
        ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.setLineDash(dash || []); ctx.globalAlpha = alpha == null ? 1 : alpha; ctx.lineCap = "round";
        ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.stroke(); ctx.restore();
      };
      const grid = FV.color("grid"), faint = FV.color("faint"), ink = FV.color("ink");
      for (let k = 0; k <= 4; k++) { const t = -1 + k / 2; seg(proj([t, -1, -1]), proj([t, 1, -1]), grid, 1); seg(proj([-1, t, -1]), proj([1, t, -1]), grid, 1); }
      const C = [-1, 1];
      C.forEach((x) => C.forEach((y) => seg(proj([x, y, -1]), proj([x, y, 1]), faint, 0.8, [2, 4], 0.5)));
      C.forEach((z) => { if (z > 0) { seg(proj([-1, -1, z]), proj([1, -1, z]), faint, 0.8, [2, 4], 0.5); seg(proj([-1, 1, z]), proj([1, 1, z]), faint, 0.8, [2, 4], 0.5); seg(proj([-1, -1, z]), proj([-1, 1, z]), faint, 0.8, [2, 4], 0.5); seg(proj([1, -1, z]), proj([1, 1, z]), faint, 0.8, [2, 4], 0.5); } });
      // axis names along the front floor edges, the z axis on the back edge
      const corners = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
      let back = corners[0], bd = -Infinity;
      corners.forEach((c) => { const d = proj([c[0], c[1], 0])[2]; if (d > bd) { bd = d; back = c; } });
      const edge = (a, b, name) => {
        const p = proj([a[0], a[1], -1]), q = proj([b[0], b[1], -1]);
        const mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2, dx = mx - W / 2, dy = my - cy, dl = Math.hypot(dx, dy) || 1;
        ctx.fillStyle = faint; ctx.textAlign = "center";
        ctx.fillText(FV.num(lo), p[0] + (dx / dl) * 14, p[1] + (dy / dl) * 14 + 4);
        ctx.fillText(FV.num(hi), q[0] + (dx / dl) * 14, q[1] + (dy / dl) * 14 + 4);
        ctx.fillStyle = ink; ctx.fillText(name, mx + (dx / dl) * 24, my + (dy / dl) * 24 + 4);
      };
      const yEdge = proj([0, -1, -1])[2] < proj([0, 1, -1])[2] ? -1 : 1;
      const xEdge = proj([-1, 0, -1])[2] < proj([1, 0, -1])[2] ? -1 : 1;
      edge([-1, yEdge], [1, yEdge], o.labels[0]);
      edge([xEdge, -1], [xEdge, 1], o.labels[1]);
      const zt = proj([back[0], back[1], 1]), zb = proj([back[0], back[1], -1]);
      ctx.fillStyle = faint; ctx.textAlign = "right";
      ctx.fillText(FV.num(hi), zt[0] - 6, zt[1] + 4); ctx.fillText(FV.num(lo), zb[0] - 6, zb[1] + 4);
      ctx.fillStyle = ink; ctx.textAlign = "center"; ctx.fillText(o.labels[2], zt[0], zt[1] - 12);
      // scene items sorted far to near
      const list = [];
      S.items().forEach((it) => {
        if (it.pts) for (let k = 1; k < it.pts.length; k++) { const A = P(it.pts[k - 1]), B = P(it.pts[k]); list.push({ d: (A[2] + B[2]) / 2, A, B, it }); }
        else { const A = P(it.p); list.push({ d: A[2] - 0.02, A, it }); }
      });
      list.sort((u, v) => v.d - u.d);
      const bg = FV.css("card") || "#fff";
      const labels = [];
      list.forEach(({ A, B, it }) => {
        if (B) seg(A, B, FV.color(it.c), it.w || 2, it.dash, it.alpha);
        else {
          ctx.beginPath(); ctx.arc(A[0], A[1], it.r || 5.5, 0, Math.PI * 2);
          ctx.lineWidth = 3; ctx.strokeStyle = bg; ctx.stroke(); ctx.fillStyle = FV.color(it.c); ctx.fill();
          if (it.label) labels.push([A, it]);
        }
      });
      labels.forEach(([A, it]) => {
        ctx.font = `600 12px ${FV.css("sans") || "sans-serif"}`; ctx.textAlign = it.left ? "right" : "left";
        ctx.lineWidth = 3; ctx.strokeStyle = bg; ctx.lineJoin = "round";
        const x = A[0] + (it.left ? -9 : 9), y = A[1] - 8;
        ctx.strokeText(it.label, x, y); ctx.fillStyle = FV.color(it.c); ctx.fillText(it.label, x, y);
      });
    };
    let px = 0, py = 0, on = false, raf = 0;
    canvas.addEventListener("pointerdown", (e) => { on = true; px = e.clientX; py = e.clientY; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener("pointermove", (e) => {
      if (!on) return;
      S.az -= (e.clientX - px) * 0.008;
      if (e.pointerType !== "touch") S.el = FV.clamp(S.el + (e.clientY - py) * 0.006, 0.05, 1.5);
      px = e.clientX; py = e.clientY;
      if (!raf) raf = requestAnimationFrame(() => { raf = 0; S.draw(); });
    });
    const up = () => { on = false; };
    canvas.addEventListener("pointerup", up); canvas.addEventListener("pointercancel", up);
    canvas.addEventListener("dblclick", reset);
    if ("ResizeObserver" in window) { let last = 0; new ResizeObserver(() => { const ww = wrap.clientWidth; if (Math.abs(ww - last) > 1) { last = ww; S.resize(); } }).observe(wrap); }
    document.addEventListener("themechange", () => S.draw());
    S.resize();
    return S;
  }

  // 4. Vectors in R³: RMSE = Euclidean distance between y and ŷ divided by √n.
  FV.widget("rmse-vectors", (el, cfg) => {
    const w = FV.shell(el, {});
    let yh = (cfg.yhat || YH).slice();
    const sc = Scene3D(w.stage, { range: [0, 10], labels: [L.axis + "1", L.axis + "2", L.axis + "3"], aspect: 0.72 });
    const sl = [0, 1, 2].map((i) => FV.ui.slider({ label: "$\\hat y_" + (i + 1) + "$", min: 0, max: 10, step: 0.1, value: yh[i], fmt: (v) => FV.fmt(v, 1), oninput: (v) => { yh[i] = v; draw(); } }));
    const sph = FV.ui.check({ label: L.sphere, checked: cfg.sphere !== false, onchange: draw });
    const bc = FV.ui.button({ label: L.setConst, onclick: () => { const m = mean(Y); yh = [m, m, m]; sl.forEach((s) => s.set(m)); draw(); } });
    const be = FV.ui.button({ label: L.setEx, onclick: () => { yh = YH.slice(); sl.forEach((s, i) => s.set(YH[i])); draw(); } });
    w.controls.append(...sl.map((s) => s.el), sph.el, FV.h("div", { class: "fv-player" }, bc.el, be.el));
    const ro = FV.ui.readout(w.readout, [{ key: "d", label: L.norm, c: "orange" }, { key: "r", label: "RMSE = ‖y − ŷ‖/√3 =", c: "blue" }, { key: "c", label: L.rmseConst, c: "teal" }]);
    const m = mean(Y), s0 = Math.sqrt(mean(Y.map((v) => (v - m) ** 2)));
    function draw() {
      const d = Math.hypot(Y[0] - yh[0], Y[1] - yh[1], Y[2] - yh[2]);
      sc.items = () => {
        const it = [];
        it.push({ pts: [[0, 0, 0], [10, 10, 10]], c: "guide", w: 1.5, dash: [6, 5] });
        if (sph.value && d > 1e-9) {
          const circle = (u, v) => FV.linspace(0, 2 * Math.PI, 61).map((t) => Y.map((c, k) => c + d * (Math.cos(t) * u[k] + Math.sin(t) * v[k])));
          const e = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
          [[0, 1], [0, 2], [1, 2]].forEach(([i, j]) => it.push({ pts: circle(e[i], e[j]), c: "faint", w: 1, alpha: 0.55 }));
          [-0.6, 0.6].forEach((h) => { const rr = Math.sqrt(1 - h * h); it.push({ pts: FV.linspace(0, 2 * Math.PI, 61).map((t) => [Y[0] + d * rr * Math.cos(t), Y[1] + d * rr * Math.sin(t), Y[2] + d * h]), c: "faint", w: 1, alpha: 0.4 }); });
        }
        it.push({ pts: [Y, [Y[0], Y[1], 0]], c: "ink", w: 1, dash: [2, 3], alpha: 0.6 });
        it.push({ pts: [yh, [yh[0], yh[1], 0]], c: "blue", w: 1, dash: [2, 3], alpha: 0.6 });
        it.push({ pts: [Y, [m, m, m]], c: "teal", w: 1.4, dash: [4, 3] });
        it.push({ pts: [Y, yh], c: "orange", w: 3 });
        it.push({ p: [m, m, m], c: "teal", r: 5, label: "ȳ·1", left: true });
        it.push({ p: Y, c: "ink", r: 6, label: "y" });
        it.push({ p: yh, c: "blue", r: 6, label: "ŷ" });
        return it;
      };
      sc.draw();
      ro.set("d", FV.fmt(d, 3)); ro.set("r", FV.fmt(d / Math.sqrt(3), 3)); ro.set("c", FV.fmt(s0, 3));
    }
    draw();
    const lg = FV.h("div", { class: "fv-legend" });
    [[L.y, "ink", "dotted"], [L.yhat, "blue", "dotted"], ["y − ŷ", "orange", ""], [L.const, "teal", "dotted"], [L.diagL, "guide", "dash"]].forEach(([t, c, k]) => lg.append(FV.h("span", {}, FV.h("i", { class: "sw sw-" + c + (k ? " " + k : "") }), FV.rich(t))));
    w.stage.append(lg);
  });

  // 5. Constant forecast: RMSE(c) is a hyperbola, its derivative is bounded by 1.
  FV.widget("rmse-derivative", (el, cfg) => {
    const w = FV.shell(el, {});
    const m = mean(Y), s2 = mean(Y.map((v) => (v - m) ** 2));
    const R = (c) => Math.sqrt((c - m) ** 2 + s2), MSE = (c) => (c - m) ** 2 + s2, MAE = (c) => mean(Y.map((v) => Math.abs(v - c)));
    const dR = (c) => (c - m) / R(c), dM = (c) => 2 * (c - m);
    const p = new FV.Plot(w.stage, { x: [-1, 12], y: [0, 8], xLabel: L.c, yLabel: L.loss, aspect: 0.5 });
    const d = new FV.Plot(w.stage, { x: [-1, 12], y: [-2.2, 2.2], xLabel: L.c, yLabel: L.dloss, aspect: 0.3, minHeight: 170, maxHeight: 240 });
    let c = cfg.c != null ? cfg.c : 8;
    const ro = FV.ui.readout(w.readout, [{ key: "c", label: "c =", c: "blue" }, { key: "r", label: "RMSE(c) =" }, { key: "dr", label: "RMSE′(c) =", c: "orange" }, { key: "dm", label: "MSE′(c) =" }, { key: "k", label: "MSE′ / RMSE′ = 2·RMSE =" }]);
    const h = p.handle(c, R(c), { c: "blue", onDrag: (x) => { c = Math.round(x * 20) / 20; return [c, R(c)]; }, onChange: () => draw() });
    function draw() {
      p.clear();
      p.fn((x) => Math.abs(x - m), { c: "faint", w: 1, dash: "3 4" });
      p.fn(MSE, { c: "guide", w: 1.8, dash: "6 5" });
      p.fn(MAE, { c: "teal", w: 1.8, dash: "5 4" });
      const k = dR(c), r0 = R(c);
      p.line(c - 3, r0 - 3 * k, c + 3, r0 + 3 * k, { c: "orange", w: 1.8 });
      p.fn(R, { c: "ink", w: 2.6 });
      Y.forEach((v) => p.dot(v, 0, { c: "ink", r: 4.5 }));
      p.line(m, 0, m, Math.sqrt(s2), { c: "guide", w: 1, dash: "3 3" });
      p.text(m, Math.sqrt(s2), "ȳ", { dx: -4, dy: -10, anchor: "middle", c: "faint" });
      h.set(c, r0);
      p.legend([{ label: "RMSE(c)", c: "ink" }, { label: "MSE(c)", c: "guide", dash: true }, { label: "MAE(c)", c: "teal", dash: true }, { label: L.tangent, c: "orange" }, { label: L.asym, c: "faint", dash: true }]);
      d.clear();
      d.hline(1, { c: "faint" }); d.hline(-1, { c: "faint" });
      d.fn(dM, { c: "guide", w: 1.6, dash: "6 5" });
      d.fn(dR, { c: "orange", w: 2.4 });
      d.line(c, 0, c, k, { c: "orange", w: 1, dash: "3 3" });
      d.dot(c, k, { c: "orange" });
      d.legend([{ label: "RMSE′(c) = (c − ȳ)/RMSE(c)", c: "orange" }, { label: "MSE′(c) = 2(c − ȳ)", c: "guide", dash: true }]);
      ro.set("c", FV.fmt(c, 2)); ro.set("r", FV.fmt(r0, 3)); ro.set("dr", FV.fmt(k, 3)); ro.set("dm", FV.fmt(dM(c), 3)); ro.set("k", FV.fmt(2 * r0, 3));
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 6. RMSE² = bias² + variance: a right triangle.
  FV.widget("rmse-pythagoras", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const n = 40, r = FV.rng(9);
    let z = Array.from({ length: n }, () => r.normal());
    const zm = mean(z); z = z.map((v) => v - zm);
    const zs = Math.sqrt(mean(z.map((v) => v * v))); z = z.map((v) => v / zs);
    const a = new FV.Plot(FV.col(w.stage), { x: [0, n + 1], y: [-6, 6], xLabel: L.idx, yLabel: L.resid, aspect: 0.75 });
    const t = new FV.Plot(FV.col(w.stage), { x: [-1.9, 4.4], y: [-0.5, 3.4], equal: true, title: L.tri, grid: false, xTicks: [0, 1, 2, 3, 4], yTicks: [0, 1, 2, 3] });
    const sb = FV.ui.slider({ label: L.bias, min: -3, max: 3, step: 0.1, value: cfg.bias != null ? cfg.bias : 1, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    const ss = FV.ui.slider({ label: L.sd, min: 0, max: 3, step: 0.1, value: cfg.sd != null ? cfg.sd : 1.5, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    w.controls.append(sb.el, ss.el);
    const ro = FV.ui.readout(w.readout, [{ key: "b", label: "r̄ =", c: "orange" }, { key: "s", label: "σ =", c: "teal" }, { key: "r", label: "RMSE =" }, { key: "m", label: "MAE =" }]);
    function draw() {
      const B = sb.value, Sd = ss.value, res = z.map((v) => B + Sd * v), st = stats(res);
      const lim = Math.max(4, Math.ceil(Math.abs(B) + 3 * Sd));
      a.setDomain(null, [-lim, lim]);
      a.clear();
      a.rect(0, B - Sd, n + 1, B + Sd, { c: "teal", opacity: 0.1 });
      a.hline(0, { c: "guide", dash: false, w: 1.2 });
      a.hline(B, { c: "orange", dash: false, w: 2.2 });
      res.forEach((v, i) => { a.line(i + 1, 0, i + 1, v, { c: "faint", w: 1, opacity: 0.5 }); a.dot(i + 1, v, { c: "ink", r: 3.5 }); });
      a.legend([{ label: L.resid, c: "ink", dot: true }, { label: L.mean, c: "orange" }, { label: L.band, c: "teal", box: true }]);
      t.clear();
      const ab = Math.abs(B), R = Math.hypot(B, Sd);
      if (ab > 1e-9 && Sd > 1e-9) { const q = Math.min(0.22, ab / 3, Sd / 3); t.path([[ab - q, 0], [ab - q, q], [ab, q]], { c: "faint", w: 1 }); }
      t.line(0, 0, ab, 0, { c: "orange", w: 3.5 });
      t.line(ab, 0, ab, Sd, { c: "teal", w: 3.5 });
      t.line(0, 0, ab, Sd, { c: "ink", w: 3 });
      t.dot(0, 0, { c: "ink", r: 3.5 });
      t.text(ab / 2, 0, L.legBias + " = " + FV.fmt(ab, 1), { anchor: "middle", dy: 18, c: "orange" });
      t.text(ab, Sd / 2, L.legSd + " = " + FV.fmt(Sd, 1), { dx: 8, dy: 4, c: "teal" });
      if (R > 1e-9) {
        const px = t.X(ab) - t.X(0), py = t.Y(Sd) - t.Y(0), pl = Math.hypot(px, py) || 1;
        t.text(ab / 2, Sd / 2, "RMSE = " + FV.fmt(R, 2), { anchor: "end", dx: (py / pl) * 22, dy: (-px / pl) * 22 + 4 });
      }
      ro.set("b", FV.fmt(mean(res), 2)); ro.set("s", FV.fmt(Math.sqrt(mean(res.map((v) => (v - mean(res)) ** 2))), 2)); ro.set("r", FV.fmt(st.rmse, 3)); ro.set("m", FV.fmt(st.mae, 3));
    }
    a.onresize = draw; t.onresize = draw; draw();
  });

  // Data for the regression landscape (deterministic).
  function regData() {
    const r = FV.rng(3), pts = [];
    for (let i = 0; i < 14; i++) { const x = 4 * r(); pts.push({ x, y: 1.5 * x + 1 + 0.8 * r.normal() }); }
    return pts;
  }

  // 7. RMSE(w, b) versus MSE(w, b) and gradient descent on each.
  FV.widget("rmse-landscape", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const pts = regData(), n = pts.length;
    const mse = (a, b) => { let s = 0; pts.forEach((p) => { s += (p.y - a * p.x - b) ** 2; }); return s / n; };
    const rmse = (a, b) => Math.sqrt(mse(a, b));
    const grad = (a, b) => { let ga = 0, gb = 0; pts.forEach((p) => { const e = a * p.x + b - p.y; ga += (2 * e * p.x) / n; gb += (2 * e) / n; }); return [ga, gb]; };
    const mx = mean(pts.map((p) => p.x)), my = mean(pts.map((p) => p.y));
    let sxy = 0, sxx = 0; pts.forEach((p) => { sxy += (p.x - mx) * (p.y - my); sxx += (p.x - mx) ** 2; });
    const W0 = sxy / sxx, B0 = my - W0 * mx, Rmin = rmse(W0, B0);
    const XD = [-1, 3.5], YD = [-2.5, 4.5], MAXS = 200;
    let mode = cfg.mode || "rmse";
    const fz = () => (mode === "rmse" ? rmse : mse);
    const s3 = new FV.Surface(FV.col(w.stage), { f: fz(), x: XD, y: YD, n: 34, labels: { x: "w", y: "b", z: mode.toUpperCase() }, azimuth: -0.55, elevation: 0.55, aspect: 0.85, cmap: "viridis" });
    const top = new FV.Plot(FV.col(w.stage), { x: XD, y: YD, xLabel: L.w, yLabel: L.b, aspect: 0.85, title: L.top });
    const lc = new FV.Plot(FV.col(w.stage), { x: [0, MAXS], y: [0.8, 3], xLabel: L.step, aspect: 0.3, minHeight: 170, maxHeight: 230, title: L.curve });
    const seg = FV.ui.seg({ label: L.surf, value: mode, options: [{ value: "rmse", label: "RMSE(w, b)" }, { value: "mse", label: "MSE(w, b)" }], onchange: (v) => { mode = v; s3.o.labels.z = v.toUpperCase(); s3.o.z = null; s3.f = fz(); s3.sample(); draw(); } });
    const se = FV.ui.slider({ label: L.eta, min: 0.02, max: 0.16, step: 0.01, value: cfg.eta || 0.1, fmt: (v) => FV.fmt(v, 2), oninput: () => { player.stop(); reset(); } });
    let S0 = (cfg.start || [0, 3]).slice();
    let PA, PC, HA, HC;
    function reset() { PA = [S0.slice()]; PC = [S0.slice()]; HA = [rmse(...S0)]; HC = [rmse(...S0)]; lc.setDomain(null, [0.8, Math.max(3, Math.ceil(HA[0] * 2) / 2)]); draw(); }
    const finite = (P) => P.map((v) => (Number.isFinite(v) ? FV.clamp(v, -1e6, 1e6) : 1e6));
    const player = FV.ui.player({
      interval: 50,
      onstep() {
        if (PA.length > MAXS) return false;
        const eta = se.value, A = PA[PA.length - 1], C = PC[PC.length - 1];
        const ga = grad(...A), gc = grad(...C), rc = rmse(...C);
        const A2 = finite([A[0] - eta * ga[0], A[1] - eta * ga[1]]);
        const C2 = finite([C[0] - (eta * gc[0]) / (2 * rc), C[1] - (eta * gc[1]) / (2 * rc)]);
        PA.push(A2); PC.push(C2); HA.push(rmse(...A2)); HC.push(rmse(...C2));
        draw();
        return PA.length <= MAXS;
      },
      onreset: reset,
    });
    w.controls.append(seg.el, se.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.step + " =" }, { key: "a", label: "RMSE (" + L.gdMse + ") =", c: "blue" }, { key: "c", label: "RMSE (" + L.gdRmse + ") =", c: "orange" }, { key: "m", label: "min RMSE =", c: "teal" }]);
    const h = top.handle(S0[0], S0[1], { c: "ink", r: 6, onDrag: (x, y) => { S0 = [Math.round(x * 20) / 20, Math.round(y * 20) / 20]; return S0; }, onChange: () => { player.stop(); reset(); } });
    const inD = (p) => p[0] >= XD[0] && p[0] <= XD[1] && p[1] >= YD[0] && p[1] <= YD[1];
    // keep the visible part of a path: points until it first leaves the domain
    const visible = (P) => { const out = []; for (const p of P) { if (!inD(p)) break; out.push(p); } return out; };
    function draw() {
      const f = fz(), A = PA[PA.length - 1], C = PC[PC.length - 1];
      const lift = (P) => visible(P).map((p) => [p[0], p[1], f(p[0], p[1])]);
      s3.paths = [{ pts: lift(PA), c: "blue", w: 2.5 }, { pts: lift(PC), c: "orange", w: 2.5 }];
      s3.points = [{ x: W0, y: B0, z: f(W0, B0), c: "teal", r: 5 }, { x: S0[0], y: S0[1], z: f(S0[0], S0[1]), c: "ink", r: 4.5 }];
      if (PA.length > 1 && inD(A)) s3.points.push({ x: A[0], y: A[1], z: f(A[0], A[1]), c: "blue", r: 4 });
      if (PC.length > 1 && inD(C)) s3.points.push({ x: C[0], y: C[1], z: f(C[0], C[1]), c: "orange", r: 4 });
      s3.draw();
      top.clear();
      top.heat(rmse, { cmap: "viridis", res: 4, alpha: 0.5, transform: Math.log });
      top.contours(rmse, [1, 1.25, 1.5, 2, 3, 4, 5, 6], { c: "ink", w: 1, opacity: 0.45 });
      top.path(visible(PA), { c: "blue", w: 2.4 });
      top.path(visible(PC), { c: "orange", w: 2.4, dash: "6 4" });
      if (PA.length === 1) {
        const eta = se.value, g = grad(...S0), r = rmse(...S0);
        top.arrow(S0[0], S0[1], S0[0] - eta * g[0], S0[1] - eta * g[1], { c: "blue", w: 2 });
        top.arrow(S0[0], S0[1], S0[0] - (eta * g[0]) / (2 * r), S0[1] - (eta * g[1]) / (2 * r), { c: "orange", w: 2.6 });
      } else {
        if (inD(A)) top.dot(A[0], A[1], { c: "blue", r: 4.5 });
        if (inD(C)) top.dot(C[0], C[1], { c: "orange", r: 4.5 });
      }
      top.dot(W0, B0, { c: "teal", r: 5 });
      h.set(S0[0], S0[1]);
      top.legend([{ label: L.gdMse, c: "blue" }, { label: L.gdRmse, c: "orange", dash: true }, { label: L.opt, c: "teal", dot: true }, { label: L.start, c: "ink", dot: true }]);
      lc.clear();
      lc.hline(Rmin, { c: "teal", w: 1.2, dash: false });
      lc.path(HA.map((v, i) => [i, Math.min(v, 1e3)]), { c: "blue", w: 2.2 });
      lc.path(HC.map((v, i) => [i, v]), { c: "orange", w: 2.2, dash: "6 4" });
      const la = HA[HA.length - 1];
      ro.set("s", String(PA.length - 1)); ro.set("a", la > 999 || !Number.isFinite(la) ? "> 999" : FV.fmt(la, 3)); ro.set("c", FV.fmt(HC[HC.length - 1], 3)); ro.set("m", FV.fmt(Rmin, 3));
    }
    top.onresize = draw; lc.onresize = draw;
    reset();
  });

  // 8. RMSLE: the squared log error is asymmetric in absolute units.
  FV.widget("rmse-rmsle", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0, 40], y: [0, 2], xLabel: L.yhatL, yLabel: L.loss, aspect: 0.45 });
    const d = new FV.Plot(w.stage, { x: [0, 40], y: [-1.2, 0.4], xLabel: L.yhatL, yLabel: L.dsle, aspect: 0.28, minHeight: 160, maxHeight: 220 });
    const sy = FV.ui.slider({ label: L.yTrue, min: 2, max: 20, step: 1, value: cfg.y || 10, fmt: (v) => String(v), oninput: () => { yh = Math.min(yh, 2 * sy.value); draw(); } });
    w.controls.append(sy.el);
    let yh = cfg.yhat != null ? cfg.yhat : 5;
    const ro = FV.ui.readout(w.readout, [{ key: "a", label: "ℓ(ŷ) =", c: "orange" }, { key: "b", label: "ℓ(2y − ŷ) =" }, { key: "k", label: L.ratioW + " =" }]);
    const ell = (y) => (x) => (Math.log1p(x) - Math.log1p(y)) ** 2;
    const dell = (y) => (x) => (2 * (Math.log1p(x) - Math.log1p(y))) / (1 + x);
    const h = p.handle(yh, 0, { c: "blue", onDrag: (x) => { yh = FV.clamp(Math.round(x * 2) / 2, 0, 2 * sy.value); return [yh, ell(sy.value)(yh)]; }, onChange: () => draw() });
    function draw() {
      const y = sy.value, f = ell(y), g = dell(y), mir = 2 * y - yh;
      p.clear();
      p.vline(y, { c: "ink", w: 1.2, dash: "3 3" });
      p.text(y, 1.9, "y = " + y, { dx: 6, c: "ink" });
      p.fn((x) => f(2 * y - x), { c: "guide", w: 1.8, dash: "6 5", from: 0, to: 2 * y });
      p.fn((x) => ((x - y) / (1 + y)) ** 2, { c: "faint", w: 1.2, dash: "2 4" });
      p.fn(f, { c: "orange", w: 2.6 });
      p.line(yh, 0, yh, f(yh), { c: "blue", w: 1, dash: "3 3" });
      p.line(mir, 0, mir, f(mir), { c: "guide", w: 1, dash: "3 3" });
      p.dot(mir, f(mir), { c: "guide", r: 4.5 });
      h.set(yh, f(yh));
      p.legend([{ label: "ℓ(ŷ) = " + L.sle, c: "orange" }, { label: L.mirror, c: "guide", dash: true }, { label: "((ŷ − y)/(1 + y))²", c: "faint", dash: true }]);
      d.clear();
      d.vline(y, { c: "ink", w: 1.2, dash: "3 3" });
      d.fn(g, { c: "orange", w: 2.4 });
      d.dot(yh, g(yh), { c: "orange" });
      ro.set("a", FV.fmt(f(yh), 3)); ro.set("b", FV.fmt(f(mir), 3)); ro.set("k", f(mir) > 1e-12 ? FV.fmt(f(yh) / f(mir), 2) : "—");
    }
    p.onresize = draw; d.onresize = draw; draw();
  });
})();
