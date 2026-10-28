/* Widgets of the formula page "BCE" (binary cross-entropy). Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      yhat: "ŷ — предсказанная вероятность класса 1", loss: "потеря", label: "Правильный ответ", pc: "вероятность правильного ответа", coin: "монетка ŷ = 0,5: ln 2",
      l1: "y = 1: −ln ŷ", l0: "y = 0: −ln(1 − ŷ)", tangent: "касательная (наклон ∂BCE/∂ŷ)",
      soft: "Мягкая метка $y$", t1: "y·(−ln ŷ)", t0: "(1 − y)·(−ln(1 − ŷ))", ce: "CE = H + KL", ent: "энтропия H(y)", kl: "KL(y ‖ ŷ)", minimum: "минимум при ŷ = y",
      z: "z — логит", eps: "Сглаживание меток $\\varepsilon$", grad: "∂BCE/∂z = ŷ − y", curv: "∂²BCE/∂z² = ŷ(1 − ŷ)", asym: "асимптоты", zstar: "оптимум z*", lossz: "BCE(z)", gz: "производные",
      bce: "BCE", mse: "MSE", gb: "∂BCE/∂z", gm: "∂MSE/∂z", concave: "MSE вогнута", ratio: "BCE / MSE по градиенту",
      lossSel: "Потеря", step: "шаг", grad2: "|∇|", data: "данные", fit: "σ(wx + b) сейчас", best: "оптимум", start: "старт", min: "минимум",
      dataSel: "Данные", over: "перекрываются", sep: "разделимы", acc: "точность", wnorm: "‖w‖", curve: "BCE на обучении", class0: "класс 0", class1: "класс 1", boundary: "граница ŷ = 0,5", size: "размер точки ∝ её потеря",
      prec: "Точность чисел", stable: "устойчиво: softplus(z) − yz", naive: "наивно: −log(1 − σ(z))", naive1: "наивно: −log σ(z)", clip: "обрезка ε = 10⁻⁷", exact: "точно", inf: "∞",
      pw: "pos_weight", thr: "порог x*", recall: "полнота", precision: "точность (precision)", meanp: "среднее ŷ", fitted: "обученная σ(wx + b)", theory: "теория: σ(логит + ln w)", pos: "класс 1 (15)", neg: "класс 0 (150)", x: "x",
      k: "Уверенность модели $k$", kstar: "k*", ece: "ECE", scale: "Температурное шкалирование", pred: "предсказанная вероятность", freq: "доля y = 1", ideal: "идеальная калибровка", bins: "по 10 корзинам", bcek: "BCE(k) на выборке", now: "сейчас",
    },
    en: {
      yhat: "ŷ — predicted probability of class 1", loss: "loss", label: "Correct answer", pc: "probability of the correct answer", coin: "coin ŷ = 0.5: ln 2",
      l1: "y = 1: −ln ŷ", l0: "y = 0: −ln(1 − ŷ)", tangent: "tangent (slope ∂BCE/∂ŷ)",
      soft: "Soft label $y$", t1: "y·(−ln ŷ)", t0: "(1 − y)·(−ln(1 − ŷ))", ce: "CE = H + KL", ent: "entropy H(y)", kl: "KL(y ‖ ŷ)", minimum: "minimum at ŷ = y",
      z: "z — logit", eps: "Label smoothing $\\varepsilon$", grad: "∂BCE/∂z = ŷ − y", curv: "∂²BCE/∂z² = ŷ(1 − ŷ)", asym: "asymptotes", zstar: "optimum z*", lossz: "BCE(z)", gz: "derivatives",
      bce: "BCE", mse: "MSE", gb: "∂BCE/∂z", gm: "∂MSE/∂z", concave: "MSE is concave", ratio: "BCE / MSE gradient",
      lossSel: "Loss", step: "step", grad2: "|∇|", data: "data", fit: "σ(wx + b) now", best: "optimum", start: "start", min: "minimum",
      dataSel: "Data", over: "overlapping", sep: "separable", acc: "accuracy", wnorm: "‖w‖", curve: "training BCE", class0: "class 0", class1: "class 1", boundary: "boundary ŷ = 0.5", size: "dot size ∝ its loss",
      prec: "Precision", stable: "stable: softplus(z) − yz", naive: "naive: −log(1 − σ(z))", naive1: "naive: −log σ(z)", clip: "clipping ε = 10⁻⁷", exact: "exact", inf: "∞",
      pw: "pos_weight", thr: "threshold x*", recall: "recall", precision: "precision", meanp: "mean ŷ", fitted: "trained σ(wx + b)", theory: "theory: σ(logit + ln w)", pos: "class 1 (15)", neg: "class 0 (150)", x: "x",
      k: "Model confidence $k$", kstar: "k*", ece: "ECE", scale: "Temperature scaling", pred: "predicted probability", freq: "share of y = 1", ideal: "perfect calibration", bins: "over 10 bins", bcek: "BCE(k) on the sample", now: "now",
    },
    uz: {
      yhat: "ŷ — 1-sinfning bashorat qilingan ehtimolligi", loss: "yo‘qotish", label: "To‘g‘ri javob", pc: "to‘g‘ri javob ehtimolligi", coin: "tanga ŷ = 0,5: ln 2",
      l1: "y = 1: −ln ŷ", l0: "y = 0: −ln(1 − ŷ)", tangent: "urinma (qiyaligi ∂BCE/∂ŷ)",
      soft: "Yumshoq belgi $y$", t1: "y·(−ln ŷ)", t0: "(1 − y)·(−ln(1 − ŷ))", ce: "CE = H + KL", ent: "entropiya H(y)", kl: "KL(y ‖ ŷ)", minimum: "minimum ŷ = y da",
      z: "z — logit", eps: "Belgilarni silliqlash $\\varepsilon$", grad: "∂BCE/∂z = ŷ − y", curv: "∂²BCE/∂z² = ŷ(1 − ŷ)", asym: "asimptotalar", zstar: "optimum z*", lossz: "BCE(z)", gz: "hosilalar",
      bce: "BCE", mse: "MSE", gb: "∂BCE/∂z", gm: "∂MSE/∂z", concave: "MSE botiq", ratio: "BCE / MSE gradiyenti",
      lossSel: "Yo‘qotish", step: "qadam", grad2: "|∇|", data: "ma’lumotlar", fit: "hozirgi σ(wx + b)", best: "optimum", start: "start", min: "minimum",
      dataSel: "Ma’lumotlar", over: "ustma-ust", sep: "ajraladigan", acc: "aniqlik", wnorm: "‖w‖", curve: "o‘qitishdagi BCE", class0: "0-sinf", class1: "1-sinf", boundary: "chegara ŷ = 0,5", size: "nuqta o‘lchami ∝ uning yo‘qotishi",
      prec: "Sonlar aniqligi", stable: "barqaror: softplus(z) − yz", naive: "sodda: −log(1 − σ(z))", naive1: "sodda: −log σ(z)", clip: "kesish ε = 10⁻⁷", exact: "aniq", inf: "∞",
      pw: "pos_weight", thr: "chegara x*", recall: "to‘liqlik (recall)", precision: "aniqlik (precision)", meanp: "o‘rtacha ŷ", fitted: "o‘qitilgan σ(wx + b)", theory: "nazariya: σ(logit + ln w)", pos: "1-sinf (15)", neg: "0-sinf (150)", x: "x",
      k: "Model ishonchi $k$", kstar: "k*", ece: "ECE", scale: "Harorat bo‘yicha masshtablash", pred: "bashorat qilingan ehtimollik", freq: "y = 1 ulushi", ideal: "ideal kalibrlash", bins: "10 ta savat bo‘yicha", bcek: "tanlanmadagi BCE(k)", now: "hozir",
    },
  }[FV.lang] || {};

  const sig = FV.sigmoid;
  // softplus(z) = ln(1 + e^z) without overflow
  const sp = (z) => Math.max(z, 0) + Math.log1p(Math.exp(-Math.abs(z)));
  // mean BCE from logits: softplus(z) − y·z
  const bceZ = (z, y) => sp(z) - y * z;
  const fx = (v, d) => FV.fmt(v, d);
  const en = FV.lang === "en";
  const dec = (s) => (en ? s : s.replace(/(\d)\.(\d)/g, "$1,$2"));

  // 1. Two branches of the loss: −ln ŷ for y = 1 and −ln(1 − ŷ) for y = 0, with a draggable prediction.
  FV.widget("bce-curves", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0, 1], y: [0, 5], xLabel: L.yhat, yLabel: L.loss, aspect: 0.52 });
    let y = cfg.y != null ? cfg.y : 1, q = cfg.p != null ? cfg.p : 0.9;
    const f1 = (v) => -Math.log(v), f0 = (v) => -Math.log(1 - v);
    const cur = (v) => (y ? f1(v) : f0(v));
    const seg = FV.ui.seg({ label: L.label, value: y, options: [{ value: 1, label: "y = 1" }, { value: 0, label: "y = 0" }], onchange: (v) => { y = v; draw(); } });
    w.controls.append(seg.el);
    const ro = FV.ui.readout(w.readout, [{ key: "q", label: "ŷ =" }, { key: "c", label: L.pc + " =" }, { key: "l", label: "BCE =" }, { key: "d", label: "∂BCE/∂ŷ =", c: "orange" }]);
    const lim = (v) => FV.clamp(v, 0.007, 0.993);
    const h = p.handle(q, cur(q), { c: y ? "red" : "blue", onDrag: (x) => { q = lim(x); return [q, cur(q)]; }, onChange: () => draw() });
    function draw() {
      q = lim(q);
      p.clear();
      p.hline(Math.LN2, { c: "guide", dash: "4 4" });
      p.text(0.985, Math.LN2, dec("ln 2 ≈ 0.693"), { dy: -7, anchor: "end", c: "faint" });
      p.vline(0.5, { c: "guide", dash: "2 4" });
      p.fn(f0, { c: "blue", w: y ? 1.6 : 2.8, opacity: y ? 0.45 : 1, from: 0.0005, to: 0.9999 });
      p.fn(f1, { c: "red", w: y ? 2.8 : 1.6, opacity: y ? 1 : 0.45, from: 0.0001, to: 0.9995 });
      const v = cur(q), k = y ? -1 / q : 1 / (1 - q);
      const dx = 0.16 / Math.sqrt(1 + (k * 0.2) ** 2);
      p.line(q - dx, v - k * dx, q + dx, v + k * dx, { c: "orange", w: 2 });
      p.line(q, 0, q, v, { c: "guide", w: 1, dash: "3 3" });
      const other = y ? f0(q) : f1(q);
      if (other < 5) p.dot(q, other, { c: y ? "blue" : "red", hollow: true, r: 4 });
      h.g.setAttribute("class", "fv-handle s-" + (y ? "red" : "blue"));
      h.g.querySelector(".knob").setAttribute("class", "knob fill-" + (y ? "red" : "blue"));
      h.set(q, v);
      ro.set("q", fx(q, 3)); ro.set("c", fx(y ? q : 1 - q, 3)); ro.set("l", fx(v, 3)); ro.set("d", fx(k, 3));
      p.legend([{ label: L.l1, c: "red" }, { label: L.l0, c: "blue" }, { label: L.tangent, c: "orange" }]);
    }
    p.onresize = draw; draw();
  });

  // 2. Soft label: CE(y, ŷ) = H(y) + KL(y ‖ ŷ); the minimum sits at ŷ = y.
  FV.widget("bce-mix", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0, 1], y: [0, 3], xLabel: L.yhat, yLabel: L.loss, aspect: 0.52 });
    let q = cfg.p != null ? cfg.p : 0.3;
    const sy = FV.ui.slider({ label: L.soft, min: 0, max: 1, step: 0.01, value: cfg.y != null ? cfg.y : 0.8, fmt: (v) => fx(v, 2), oninput: draw });
    w.controls.append(sy.el);
    const ro = FV.ui.readout(w.readout, [{ key: "h", label: "H(y) =", c: "teal" }, { key: "k", label: "KL(y ‖ ŷ) =", c: "orange" }, { key: "c", label: "CE(y, ŷ) =" }]);
    const xlogy = (a, b) => (a === 0 ? 0 : a * Math.log(b));
    const CE = (y, v) => -(xlogy(y, v) + xlogy(1 - y, 1 - v));
    const H = (y) => CE(y, y);
    const lim = (v) => FV.clamp(v, 0.005, 0.995);
    const h = p.handle(q, 1, { c: "ink", onDrag: (x) => { q = lim(x); return [q, Math.min(CE(sy.value, q), 3)]; }, onChange: () => draw() });
    function draw() {
      const y = sy.value; q = lim(q);
      p.clear();
      p.fn((v) => -xlogy(y, v), { c: "red", w: 1.5, opacity: 0.75, from: 0.0005, to: 0.9995 });
      p.fn((v) => -xlogy(1 - y, 1 - v), { c: "blue", w: 1.5, opacity: 0.75, from: 0.0005, to: 0.9995 });
      const Hy = H(y), c = CE(y, q);
      p.hline(Hy, { c: "teal", dash: "6 4", w: 1.4 });
      p.fn((v) => CE(y, v), { c: "ink", w: 2.8, from: 0.0005, to: 0.9995 });
      p.line(q, 0, q, Hy, { c: "teal", w: 5, opacity: 0.55 });
      p.line(q, Hy, q, Math.min(c, 3), { c: "orange", w: 5, opacity: 0.85 });
      p.dot(y, Hy, { c: "teal", r: 5 });
      h.set(q, Math.min(c, 3));
      ro.set("h", fx(Hy, 3)); ro.set("k", fx(c - Hy, 3)); ro.set("c", fx(c, 3));
      p.legend([{ label: L.ce, c: "ink" }, { label: L.t1, c: "red" }, { label: L.t0, c: "blue" }, { label: L.ent, c: "teal", dash: true }, { label: L.minimum, c: "teal", dot: true }, { label: L.kl, c: "orange", box: true }]);
    }
    p.onresize = draw; draw();
  });

  // 3. BCE as a function of the logit: softplus shape, gradient ŷ − y, curvature ŷ(1 − ŷ), label smoothing.
  FV.widget("bce-logit", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-8, 8], y: [-0.2, 8.4], xLabel: L.z, yLabel: L.lossz, aspect: 0.45 });
    const d = new FV.Plot(w.stage, { x: [-8, 8], y: [-1.15, 1.15], xLabel: L.z, yLabel: L.gz, aspect: 0.26, minHeight: 170, maxHeight: 230 });
    let y = cfg.y != null ? cfg.y : 1, z = cfg.z != null ? cfg.z : -2;
    const seg = FV.ui.seg({ label: L.label, value: y, options: [{ value: 1, label: "y = 1" }, { value: 0, label: "y = 0" }], onchange: (v) => { y = v; draw(); } });
    const se = FV.ui.slider({ label: L.eps, min: 0, max: 0.4, step: 0.01, value: cfg.eps || 0, fmt: (v) => fx(v, 2), oninput: draw });
    w.controls.append(seg.el, se.el);
    const ro = FV.ui.readout(w.readout, [{ key: "z", label: "z =" }, { key: "s", label: "ŷ = σ(z) =" }, { key: "l", label: "BCE =" }, { key: "g", label: "∂/∂z =", c: "orange" }, { key: "c", label: "∂²/∂z² =", c: "teal" }, { key: "o", label: "z* =" }]);
    const tgt = () => y * (1 - se.value) + se.value / 2;
    const h = p.handle(z, 1, { c: y ? "red" : "blue", onDrag: (x) => { z = x; return [z, bceZ(z, tgt())]; }, onChange: () => draw() });
    function draw() {
      const t = tgt(), s = sig(z), v = bceZ(z, t), g = s - t;
      p.clear();
      p.line(-8, 8 * t, 0, 0, { c: "faint", w: 1.2, dash: "5 4" });
      p.line(0, 0, 8, 8 * (1 - t), { c: "faint", w: 1.2, dash: "5 4" });
      p.fn((u) => bceZ(u, t), { c: "ink", w: 2.6 });
      p.line(z - 2.2, v - 2.2 * g, z + 2.2, v + 2.2 * g, { c: "orange", w: 1.8 });
      p.line(z, -0.2, z, v, { c: "guide", w: 1, dash: "3 3" });
      const zs = Math.log(t / (1 - t));
      if (Number.isFinite(zs) && Math.abs(zs) < 8) { p.dot(zs, bceZ(zs, t), { c: "teal", r: 4.5 }); p.text(zs, bceZ(zs, t), "z*", { dy: -10, anchor: "middle", c: "teal" }); }
      h.g.setAttribute("class", "fv-handle s-" + (y ? "red" : "blue"));
      h.g.querySelector(".knob").setAttribute("class", "knob fill-" + (y ? "red" : "blue"));
      h.set(z, v);
      p.legend([{ label: "BCE(z) = softplus(z) − y·z", c: "ink" }, { label: L.asym, c: "faint", dash: true }, { label: L.tangent.replace("ŷ", "z"), c: "orange" }]);
      d.clear();
      d.hline(0, { c: "guide", dash: false });
      d.hline(-1, { c: "guide" }); d.hline(1, { c: "guide" });
      d.fn((u) => { const a = sig(u); return a * (1 - a); }, { c: "teal", w: 1.8, dash: "6 4" });
      d.fn((u) => sig(u) - t, { c: "orange", w: 2.4 });
      d.line(z, -1.15, z, 1.15, { c: "guide", w: 1, dash: "3 3" });
      d.dot(z, g, { c: "orange", r: 4.5 });
      if (Number.isFinite(zs) && Math.abs(zs) < 8) d.dot(zs, 0, { c: "teal", r: 4 });
      d.legend([{ label: L.grad, c: "orange" }, { label: L.curv, c: "teal", dash: true }]);
      ro.set("z", fx(z, 2)); ro.set("s", fx(s, 4)); ro.set("l", fx(v, 4)); ro.set("g", fx(g, 4)); ro.set("c", fx(s * (1 - s), 4));
      ro.set("o", Number.isFinite(zs) ? fx(zs, 3) : fx(zs));
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 4. BCE versus MSE, both through a sigmoid, for y = 1: losses and their gradients in the logit.
  FV.widget("bce-vs-mse", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-8, 8], y: [0, 9], xLabel: L.z, yLabel: L.loss + " (y = 1)", aspect: 0.42 });
    const d = new FV.Plot(w.stage, { x: [-8, 8], y: [-1.08, 0.3], xLabel: L.z, yLabel: L.gz, aspect: 0.26, minHeight: 170, maxHeight: 230 });
    let z = cfg.z != null ? cfg.z : -4;
    const ro = FV.ui.readout(w.readout, [{ key: "z", label: "z =" }, { key: "s", label: "ŷ =" }, { key: "b", label: L.gb + " =", c: "orange" }, { key: "m", label: L.gm + " =", c: "violet" }, { key: "r", label: L.ratio + " =" }]);
    const mse = (u) => (1 - sig(u)) ** 2;
    const gm = (u) => { const s = sig(u); return -2 * s * (1 - s) * (1 - s); };
    const h = p.handle(z, sp(-z), { c: "ink", onDrag: (x) => { z = x; return [z, Math.min(sp(-z), 9)]; }, onChange: () => draw() });
    function draw() {
      p.clear();
      const z0 = -Math.LN2;
      p.rect(-8, 0, z0, 9, { c: "violet", opacity: 0.07 });
      p.fn((u) => sp(-u), { c: "ink", w: 2.6 });
      p.fn(mse, { c: "violet", w: 2.6 });
      p.line(z, 0, z, Math.min(sp(-z), 9), { c: "guide", w: 1, dash: "3 3" });
      p.dot(z, mse(z), { c: "violet", r: 4.5 });
      h.set(z, Math.min(sp(-z), 9));
      p.legend([{ label: "BCE = −ln σ(z)", c: "ink" }, { label: "MSE = (1 − σ(z))²", c: "violet" }, { label: L.concave + " (z < −ln 2)", c: "violet", box: true }]);
      d.clear();
      d.hline(0, { c: "guide", dash: false });
      d.hline(-1, { c: "guide" });
      d.fn((u) => sig(u) - 1, { c: "orange", w: 2.6 });
      d.fn(gm, { c: "violet", w: 2.6 });
      d.line(z, -1.08, z, 0.3, { c: "guide", w: 1, dash: "3 3" });
      d.dot(z, sig(z) - 1, { c: "orange", r: 4.5 }); d.dot(z, gm(z), { c: "violet", r: 4.5 });
      d.legend([{ label: L.gb + " = σ(z) − 1", c: "orange" }, { label: L.gm + " = −2σ(1 − σ)²", c: "violet" }]);
      const s = sig(z);
      ro.set("z", fx(z, 2)); ro.set("s", fx(s, 4)); ro.set("b", fx(s - 1, 4)); ro.set("m", fx(gm(z), 4)); ro.set("r", FV.num((s - 1) / gm(z), 3) + "×");
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // One-feature dataset for the loss landscape (deterministic): 12 points per class.
  function line1d() {
    const r = FV.rng(4), X = [], Y = [];
    for (let i = 0; i < 12; i++) { X.push(-1 + r.normal()); Y.push(0); }
    for (let i = 0; i < 12; i++) { X.push(1 + r.normal()); Y.push(1); }
    return { X, Y };
  }

  // 5. The loss surface over (w, b): BCE is a convex bowl, MSE has plateaus. Gradient descent on both.
  FV.widget("bce-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const { X, Y } = line1d(), n = X.length;
    const losses = {
      bce: (a, b) => { let s = 0; for (let i = 0; i < n; i++) s += bceZ(a * X[i] + b, Y[i]); return s / n; },
      mse: (a, b) => { let s = 0; for (let i = 0; i < n; i++) s += (sig(a * X[i] + b) - Y[i]) ** 2; return s / n; },
    };
    const grads = {
      bce: (a, b) => { let ga = 0, gb = 0; for (let i = 0; i < n; i++) { const e = sig(a * X[i] + b) - Y[i]; ga += e * X[i]; gb += e; } return [ga / n, gb / n]; },
      mse: (a, b) => { let ga = 0, gb = 0; for (let i = 0; i < n; i++) { const s = sig(a * X[i] + b), e = 2 * (s - Y[i]) * s * (1 - s); ga += e * X[i]; gb += e; } return [ga / n, gb / n]; },
    };
    const OPT = { bce: [1.4415, 0.1494], mse: [1.3743, 0.3196] };
    const S0 = [cfg.w != null ? cfg.w : -5, cfg.b != null ? cfg.b : 4], lr = cfg.lr || 1;
    let kind = cfg.loss || "bce", P = S0.slice(), path = [S0.slice()], step = 0;
    const f = (a, b) => losses[kind](a, b);
    const s3 = new FV.Surface(FV.col(w.stage), { f, x: [-6, 6], y: [-6, 6], n: 34, labels: { x: "w", y: "b", z: kind.toUpperCase() }, azimuth: -2.35, elevation: 0.5, aspect: 0.85, cmap: "viridis", title: L.lossSel + ": L(w, b)" });
    const hp = new FV.Plot(FV.col(w.stage), { x: [-6, 6], y: [-6, 6], xLabel: "w", yLabel: "b", equal: true, title: "L(w, b) — " + (en ? "view from above" : FV.lang === "uz" ? "yuqoridan ko‘rinish" : "вид сверху") });
    const dp = new FV.Plot(FV.col(w.stage), { x: [-3.2, 3.2], y: [-0.12, 1.12], xLabel: "x", yLabel: "ŷ", aspect: 0.3, minHeight: 170, maxHeight: 220, title: L.data + ": σ(wx + b)" });
    const seg = FV.ui.seg({ label: L.lossSel, value: kind, options: [{ value: "bce", label: "BCE" }, { value: "mse", label: "MSE" }], onchange: (v) => { kind = v; player.stop(); reset(); } });
    const player = FV.ui.player({
      interval: 60,
      onstep() {
        const k = step < 30 ? 1 : step < 150 ? 3 : 10;
        let g = [0, 0];
        for (let i = 0; i < k; i++) { g = grads[kind](P[0], P[1]); P[0] -= lr * g[0]; P[1] -= lr * g[1]; step++; path.push(P.slice()); }
        drawDyn();
        return step < 1500 && Math.hypot(g[0], g[1]) > 1e-4;
      },
      onreset() { reset(); },
    });
    w.controls.append(seg.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.step + " =" }, { key: "w", label: "w =" }, { key: "b", label: "b =" }, { key: "l", label: "L =", c: "orange" }, { key: "g", label: L.grad2 + " =" }]);
    function reset() { P = S0.slice(); path = [S0.slice()]; step = 0; s3.o.labels.z = kind.toUpperCase(); s3.f = f; s3.sample(); drawStatic(); }
    const LEVELS = { bce: [0.5, 0.6, 0.8, 1, 1.5, 2, 3, 4, 5, 6], mse: [0.16, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7] };
    function drawStatic() {
      hp.clear();
      hp.heat(f, { cmap: "viridis", res: 4, alpha: 0.9, transform: kind === "bce" ? Math.log : null });
      hp.contours(f, LEVELS[kind], { c: "ink", w: 1, opacity: 0.35 });
      const o = OPT[kind];
      hp.dot(o[0], o[1], { c: "ink", hollow: true, r: 5 });
      hp.text(o[0], o[1], L.min, { dx: 8, dy: 14, c: "ink" });
      drawDyn();
    }
    function sub(pts) {
      // keep the 3D path on the surface: split long segments
      const out = [];
      for (let i = 0; i < pts.length; i++) {
        if (i) {
          const a = pts[i - 1], b = pts[i], m = Math.min(8, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / 0.25));
          for (let k = 1; k < m; k++) { const u = a[0] + ((b[0] - a[0]) * k) / m, v = a[1] + ((b[1] - a[1]) * k) / m; out.push([u, v, f(u, v)]); }
        }
        out.push([pts[i][0], pts[i][1], f(pts[i][0], pts[i][1])]);
      }
      return out;
    }
    function drawDyn() {
      const pts = path.length > 400 ? path.filter((_, i) => i % Math.ceil(path.length / 400) === 0 || i === path.length - 1) : path;
      s3.paths = [{ pts: sub(pts), c: "orange", w: 2.6 }];
      s3.points = [{ x: S0[0], y: S0[1], z: f(S0[0], S0[1]), c: "faint", r: 4.5 }, { x: P[0], y: P[1], z: f(P[0], P[1]), c: "orange", r: 5.5 }];
      s3.draw();
      hp.gHover.textContent = "";
      hp.hl("path", pts, { c: "orange", w: 2.4 });
      hp.hl("dot", S0[0], S0[1], { c: "faint", r: 4.5 });
      hp.hl("dot", P[0], P[1], { c: "orange", r: 5.5 });
      dp.clear();
      dp.hline(0.5, {});
      const o = OPT[kind];
      dp.fn((x) => sig(o[0] * x + o[1]), { c: "faint", w: 1.6, dash: "5 4" });
      dp.fn((x) => sig(P[0] * x + P[1]), { c: "orange", w: 2.4 });
      for (let i = 0; i < n; i++) dp.dot(X[i], Y[i], { c: Y[i] ? "red" : "blue", r: 4.5 });
      dp.legend([{ label: L.class0, c: "blue", dot: true }, { label: L.class1, c: "red", dot: true }, { label: L.fit, c: "orange" }, { label: L.best + " " + kind.toUpperCase(), c: "faint", dash: true }]);
      const g = grads[kind](P[0], P[1]);
      ro.set("s", String(step)); ro.set("w", fx(P[0], 3)); ro.set("b", fx(P[1], 3)); ro.set("l", fx(f(P[0], P[1]), 4)); ro.set("g", FV.num(Math.hypot(g[0], g[1]), 3));
    }
    hp.onresize = drawStatic; dp.onresize = drawDyn;
    reset();
  });

  // Two Gaussian clouds (deterministic): overlapping or linearly separable.
  function clouds(sep) {
    const r = FV.rng(2), pts = [];
    const m = sep ? [1.6, 1.2] : [1, 0.7], s = sep ? 0.7 : 1;
    for (let i = 0; i < 30; i++) pts.push({ x: -m[0] + s * r.normal(), y: -m[1] + s * r.normal(), c: 0 });
    for (let i = 0; i < 30; i++) pts.push({ x: m[0] + s * r.normal(), y: m[1] + s * r.normal(), c: 1 });
    return pts;
  }

  // 6. Training logistic regression with BCE: per-point losses, the loss curve, separable data.
  FV.widget("bce-train", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    let mode = cfg.data || "over", pts = clouds(mode === "sep");
    const hp = new FV.Plot(FV.col(w.stage), { x: [-4, 4], y: [-4, 4], xLabel: "x₁", yLabel: "x₂", equal: true, title: "ŷ(x₁, x₂)" });
    const lp = new FV.Plot(FV.col(w.stage), { x: [0, 400], y: [0, 0.8], xLabel: L.step, yLabel: "BCE", aspect: 0.9, maxHeight: 400, title: L.curve });
    const lr = cfg.lr || 1;
    let W = [0, 0], B = 0, step = 0, hist = [];
    const seg = FV.ui.seg({ label: L.dataSel, value: mode, options: [{ value: "over", label: L.over }, { value: "sep", label: L.sep }], onchange: (v) => { mode = v; pts = clouds(v === "sep"); player.stop(); reset(); } });
    function stats() {
      let loss = 0, acc = 0;
      pts.forEach((q) => { const z = W[0] * q.x + W[1] * q.y + B; q.l = bceZ(z, q.c); loss += q.l; acc += (z >= 0 ? 1 : 0) === q.c ? 1 : 0; });
      return { loss: loss / pts.length, acc: acc / pts.length };
    }
    function gdStep() {
      let g1 = 0, g2 = 0, gb = 0;
      pts.forEach((q) => { const e = sig(W[0] * q.x + W[1] * q.y + B) - q.c; g1 += e * q.x; g2 += e * q.y; gb += e; });
      const m = pts.length;
      W = [W[0] - (lr * g1) / m, W[1] - (lr * g2) / m]; B -= (lr * gb) / m; step++;
      hist.push([step, stats().loss]);
    }
    const player = FV.ui.player({
      interval: 70,
      onstep() { const k = step < 40 ? 1 : 4; for (let i = 0; i < k && step < 400; i++) gdStep(); draw(); return step < 400; },
      onreset() { reset(); },
    });
    w.controls.append(seg.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.step + " =" }, { key: "l", label: "BCE =", c: "orange" }, { key: "a", label: L.acc + " =" }, { key: "w", label: L.wnorm + " =" }]);
    function reset() { W = [0, 0]; B = 0; step = 0; hist = [[0, stats().loss]]; draw(); }
    function draw() {
      const st = stats();
      const prob = (x, y) => sig(W[0] * x + W[1] * y + B);
      hp.clear();
      hp.heat(prob, { cmap: "diverging", z: [0, 1], res: 4, alpha: 0.7 });
      if (Math.hypot(W[0], W[1]) > 1e-9) hp.contours(prob, [0.5], { c: "ink", w: 2.2, opacity: 0.9 });
      pts.forEach((q) => hp.dot(q.x, q.y, { c: q.c ? "red" : "blue", r: 3 + 2.4 * Math.min(q.l, 2.5) }));
      hp.legend([{ label: L.class0, c: "blue", dot: true }, { label: L.class1, c: "red", dot: true }, { label: L.boundary, c: "ink" }, { label: L.size, c: "faint", dot: true }]);
      lp.clear();
      lp.hline(Math.LN2, { c: "guide" });
      lp.text(396, Math.LN2, "ln 2", { dy: -6, anchor: "end", c: "faint" });
      lp.path(hist, { c: "orange", w: 2.4 });
      lp.dot(step, st.loss, { c: "orange", r: 4.5 });
      ro.set("s", String(step)); ro.set("l", fx(st.loss, 4)); ro.set("a", Math.round(st.acc * 1000) / 10 + "%"); ro.set("w", fx(Math.hypot(W[0], W[1]), 2));
    }
    hp.onresize = draw; lp.onresize = draw;
    reset();
  });

  // 7. Numerical stability: naive log(1 − σ(z)) in float32/float64, clipping, and the stable softplus form.
  FV.widget("bce-stability", (el, cfg) => {
    const w = FV.shell(el, {});
    let y = cfg.y != null ? cfg.y : 0, p32 = cfg.prec !== "64";
    const dom = () => (y ? { x: [-100, 0], y: [0, 120] } : { x: [0, 45], y: [0, 46] });
    const p = new FV.Plot(w.stage, { x: dom().x, y: dom().y, xLabel: L.z, yLabel: "BCE (y = " + y + ")", aspect: 0.5 });
    const r = (v) => (p32 ? Math.fround(v) : v);
    const sgm = (z) => r(1 / r(1 + r(Math.exp(-z))));
    const naive = (z) => (y ? -r(Math.log(sgm(z))) : -r(Math.log(r(1 - sgm(z)))));
    const clip = (z) => { const s = Math.min(Math.max(sgm(z), r(1e-7)), r(1 - 1e-7)); return y ? -r(Math.log(s)) : -r(Math.log(r(1 - s))); };
    const exact = (z) => bceZ(z, y);
    const sz = FV.ui.slider({ label: "z", min: 0, max: 45, step: 0.1, value: cfg.z != null ? cfg.z : 20, fmt: (v) => fx(v, 1), oninput: draw });
    const sy = FV.ui.seg({ label: L.label, value: y, options: [{ value: 0, label: "y = 0" }, { value: 1, label: "y = 1" }], onchange: (v) => {
      y = v; const D = dom(); p.o.yLabel = "BCE (y = " + y + ")"; p.setDomain(D.x, D.y);
      sz.input.min = y ? -100 : 0; sz.input.max = y ? 0 : 45; sz.set(y ? -20 : 20); draw();
    } });
    const sp32 = FV.ui.seg({ label: L.prec, value: p32 ? "32" : "64", options: [{ value: "32", label: "float32" }, { value: "64", label: "float64" }], onchange: (v) => { p32 = v === "32"; draw(); } });
    w.controls.append(sy.el, sp32.el, sz.el);
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.exact + " =" }, { key: "n", label: (en ? "naive" : FV.lang === "uz" ? "sodda" : "наивно") + " =", c: "violet" }, { key: "c", label: (en ? "clipping" : FV.lang === "uz" ? "kesish" : "обрезка") + " =", c: "teal" }]);
    function breakAt() { let lo = 0, hi = y ? -120 : 60; if (Number.isFinite(naive(hi))) return null; for (let i = 0; i < 60; i++) { const m = (lo + hi) / 2; if (Number.isFinite(naive(m))) lo = m; else hi = m; } return lo; }
    function draw() {
      const D = dom(), z = sz.value;
      p.clear();
      p.fn(exact, { c: "ink", w: 2.6 });
      p.fn(clip, { c: "teal", w: 2.2, n: 1600 });
      p.fn(naive, { c: "violet", w: 2.2, dash: "6 4", n: 1600 });
      const zb = breakAt();
      if (zb != null && zb > D.x[0] && zb < D.x[1]) {
        p.line(zb, naive(zb), zb, D.y[1], { c: "violet", w: 1.2, dash: "2 3" });
        p.text(zb, D.y[1], (en ? "→ ∞ from z ≈ " : FV.lang === "uz" ? "→ ∞, z ≈ " : "→ ∞ при z ≈ ") + fx(zb, 2) + (FV.lang === "uz" ? " dan" : ""), { dx: 6, dy: 16, c: "violet" });
      }
      p.line(z, D.y[0], z, D.y[1], { c: "guide", w: 1, dash: "3 3" });
      p.dot(z, exact(z), { c: "ink", r: 4 });
      p.dot(z, clip(z), { c: "teal", r: 4 });
      if (Number.isFinite(naive(z))) p.dot(z, naive(z), { c: "violet", r: 4, hollow: true });
      ro.set("e", fx(exact(z), 3)); ro.set("n", Number.isFinite(naive(z)) ? fx(naive(z), 3) : "∞"); ro.set("c", fx(clip(z), 3));
      p.legend([{ label: L.stable, c: "ink" }, { label: y ? L.naive1 : L.naive, c: "violet", dash: true }, { label: L.clip, c: "teal" }]);
    }
    p.onresize = draw; draw();
  });

  // Imbalanced 1D data: 150 negatives N(0, 1), 15 positives N(2, 1).
  function imb() {
    const r = FV.rng(1), X = [], Y = [], J = [];
    for (let i = 0; i < 150; i++) { X.push(r.normal()); Y.push(0); }
    for (let i = 0; i < 15; i++) { X.push(2 + r.normal()); Y.push(1); }
    const j = FV.rng(99);
    for (let i = 0; i < 165; i++) J.push(j());
    return { X, Y, J };
  }
  // Weighted logistic regression by Newton's method.
  function fitW(X, Y, pw) {
    let a = 0, b = 0;
    for (let it = 0; it < 40; it++) {
      let g0 = 0, g1 = 0, h00 = 1e-9, h01 = 0, h11 = 1e-9;
      for (let i = 0; i < X.length; i++) {
        const s = Y[i] ? pw : 1, q = sig(a * X[i] + b), e = s * (q - Y[i]), hh = s * q * (1 - q);
        g0 += e * X[i]; g1 += e; h00 += hh * X[i] * X[i]; h01 += hh * X[i]; h11 += hh;
      }
      const det = h00 * h11 - h01 * h01, da = (h11 * g0 - h01 * g1) / det, db = (h00 * g1 - h01 * g0) / det;
      a -= da; b -= db;
      if (Math.abs(da) + Math.abs(db) < 1e-12) break;
    }
    return [a, b];
  }

  // 8. pos_weight on imbalanced data: the fitted curve, the threshold, recall and precision.
  FV.widget("bce-imbalance", (el, cfg) => {
    const w = FV.shell(el, {});
    const D = imb();
    const p = new FV.Plot(w.stage, { x: [-3.5, 5.5], y: [-0.12, 1.12], xLabel: L.x, yLabel: "ŷ", aspect: 0.48 });
    const s = FV.ui.slider({ label: "pos_weight $w$", min: 1, max: 30, step: 1, value: cfg.pw || 1, fmt: (v) => String(v), oninput: draw });
    w.controls.append(s.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.thr + " =", c: "orange" }, { key: "r", label: L.recall + " =" }, { key: "p", label: L.precision + " =" }, { key: "m", label: L.meanp + " =" }]);
    const cache = {};
    function draw() {
      const pw = s.value, ab = cache[pw] || (cache[pw] = fitW(D.X, D.Y, pw));
      const t = -ab[1] / ab[0];
      let tp = 0, fp = 0, mp = 0;
      D.X.forEach((x, i) => { const z = ab[0] * x + ab[1]; mp += sig(z); if (z >= 0) { if (D.Y[i]) tp++; else fp++; } });
      p.clear();
      p.rect(t, -0.12, 5.5, 1.12, { c: "orange", opacity: 0.06 });
      p.hline(0.5, {});
      p.fn((x) => sig(Math.log(15 / 150) + 2 * x - 2 + Math.log(pw)), { c: "teal", w: 1.8, dash: "6 4" });
      p.fn((x) => sig(ab[0] * x + ab[1]), { c: "ink", w: 2.6 });
      p.vline(t, { c: "orange", w: 1.6, dash: "5 4" });
      p.text(t, 0.12, "x* = " + fx(t, 2), { dx: 6, c: "orange" });
      D.X.forEach((x, i) => {
        const yy = D.Y[i] ? 1.04 + 0.05 * D.J[i] : -0.09 + 0.05 * D.J[i];
        const c = p.dot(x, yy, { c: D.Y[i] ? "red" : "blue", r: 3.2 });
        if (!D.Y[i]) c.setAttribute("opacity", "0.7");
      });
      p.legend([{ label: L.neg, c: "blue", dot: true }, { label: L.pos, c: "red", dot: true }, { label: L.fitted, c: "ink" }, { label: L.theory, c: "teal", dash: true }, { label: L.thr, c: "orange", dash: true }]);
      ro.set("t", fx(t, 2)); ro.set("r", tp + "/15"); ro.set("p", tp + "/" + (tp + fp)); ro.set("m", fx(mp / D.X.length, 3));
    }
    p.onresize = draw; draw();
  });

  // Calibration data: true logits t ~ N(0, 2²), labels y ~ Bernoulli(σ(t)); the model predicts σ(k·t).
  function calData() {
    const r = FV.rng(7), T = [], Y = [];
    for (let i = 0; i < 4000; i++) { const t = 2 * r.normal(); T.push(t); Y.push(r() < sig(t) ? 1 : 0); }
    return { T, Y };
  }

  // 9. Calibration: reliability diagram and BCE as a function of the model's confidence k.
  FV.widget("bce-calibration", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const D = calData(), n = D.T.length;
    const bk = (k) => { let s = 0; for (let i = 0; i < n; i++) s += bceZ(k * D.T[i], D.Y[i]); return s / n; };
    let a = 0.2, b = 3;
    for (let i = 0; i < 80; i++) { const m1 = a + (b - a) / 3, m2 = b - (b - a) / 3; if (bk(m1) < bk(m2)) b = m2; else a = m1; }
    const kopt = (a + b) / 2;
    const ks = FV.linspace(0.2, 3, 113), curve = ks.map((k) => [k, bk(k)]);
    const rp = new FV.Plot(FV.col(w.stage), { x: [0, 1], y: [0, 1], xLabel: L.pred, yLabel: L.freq, equal: true, title: (en ? "Reliability diagram" : FV.lang === "uz" ? "Ishonchlilik diagrammasi" : "Диаграмма надёжности") });
    const cp = new FV.Plot(FV.col(w.stage), { x: [0.2, 3], y: [0.42, 0.72], xLabel: "k", yLabel: "BCE", aspect: 0.95, maxHeight: 420, title: L.bcek });
    const sk = FV.ui.slider({ label: L.k, min: 0.2, max: 3, step: 0.01, value: cfg.k || 2, fmt: (v) => fx(v, 2), oninput: draw });
    const bt = FV.ui.button({ label: L.scale + " → k*", onclick: () => { sk.set(kopt); draw(); } });
    w.controls.append(sk.el, bt.el);
    const ro = FV.ui.readout(w.readout, [{ key: "k", label: "k =" }, { key: "l", label: "BCE =", c: "orange" }, { key: "e", label: L.ece + " =" }, { key: "o", label: "k* =", c: "teal" }]);
    function draw() {
      const k = sk.value;
      const cnt = new Array(10).fill(0), sp_ = new Array(10).fill(0), sy = new Array(10).fill(0);
      for (let i = 0; i < n; i++) { const q = sig(k * D.T[i]), j = Math.min(9, Math.floor(q * 10)); cnt[j]++; sp_[j] += q; sy[j] += D.Y[i]; }
      let ece = 0;
      rp.clear();
      rp.line(0, 0, 1, 1, { c: "guide", w: 1.4, dash: "5 4" });
      const pts = [];
      for (let j = 0; j < 10; j++) {
        if (!cnt[j]) continue;
        const mp = sp_[j] / cnt[j], fr = sy[j] / cnt[j];
        ece += (cnt[j] / n) * Math.abs(mp - fr);
        rp.rect(j / 10 + 0.008, 0, (j + 1) / 10 - 0.008, fr, { c: "blue", opacity: 0.16 });
        rp.line(mp, mp, mp, fr, { c: "red", w: 2, opacity: 0.8 });
        pts.push([mp, fr]);
      }
      rp.path(pts, { c: "blue", w: 2.2 });
      pts.forEach((q) => rp.dot(q[0], q[1], { c: "blue", r: 4.5 }));
      rp.legend([{ label: L.ideal, c: "guide", dash: true }, { label: L.bins, c: "blue" }, { label: "|ŷ − " + (en ? "share" : FV.lang === "uz" ? "ulush" : "доля") + "|", c: "red" }]);
      cp.clear();
      cp.vline(kopt, { c: "teal", w: 1.4, dash: "5 4" });
      cp.text(kopt, 0.42, "k* = " + fx(kopt, 2), { dx: 6, dy: -8, c: "teal" });
      cp.path(curve, { c: "ink", w: 2.4 });
      cp.dot(k, bk(k), { c: "orange", r: 5.5 });
      cp.legend([{ label: L.bcek, c: "ink" }, { label: L.now, c: "orange", dot: true }, { label: "k*", c: "teal", dash: true }]);
      ro.set("k", fx(k, 2)); ro.set("l", fx(bk(k), 3)); ro.set("e", fx(ece, 3)); ro.set("o", fx(kopt, 3));
    }
    rp.onresize = draw; cp.onresize = draw; draw();
  });
})();
