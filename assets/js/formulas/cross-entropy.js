/* Widgets of the formula page "Categorical cross-entropy". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      p: "Вероятность правильного класса $p$", ce: "−ln p (кросс-энтропия)", sq: "(1 − p)² (квадратичная ошибка)", dce: "−1/p", dsq: "−2(1 − p)",
      loss: "потеря", deriv: "производная по p", bits: "в битах −log₂ p =", nats: "−ln p =", dd: "d/dp =",
      right: "уверен и прав", wrong: "уверен и ошибся",
      logits: "Логиты $z$ (тяните)", sy: "Прогноз $s$ и цель $y$", target: "цель yₖ", push: "−(sₖ − yₖ): куда сдвинется zₖ", cls: "Правильный класс", eta: "Шаг $\\eta$", reset: "Сбросить",
      grad: "s − y =", step: "шаг", stepN: "шаг =",
      simplex: "Цель p и прогноз q в симплексе", decomp: "H(p, q) = H(p) + KL(p‖q), наты", hp: "H(p)", kl: "KL(p‖q)", hpq: "H(p, q)", inbits: "H(p, q) в битах =", level: "линии уровня KL(p‖·)",
      surf: "CE(z₁, z₂, 0)", plane: "Вид сверху: потеря и антиградиент", run: "Спуск по логитам", path: "путь градиентного спуска", anti: "−∇CE",
      eps: "Сглаживание $\\varepsilon$", K: "Классов $K$", m: "отрыв правильного логита m", top: "Потеря от отрыва m", bot: "Производная dCE/dm = s − y", plain: "без сглаживания (ε = 0)", smooth: "со сглаживанием",
      yc: "цель для правильного класса =", mstar: "оптимальный отрыв m* =", hmin: "минимум потери H(y) =",
      model: "Показать модель", mCE: "обучена на CE", mMSE: "обучена на MSE", regions: "Области классов", accT: "Точность на обучающей выборке, %", acc: "точность", gnorm: "|∂L/∂z| в среднем", class: "класс",
      lam: "Уверенность $\\lambda$", tokens: ["Кошка", "сидит", "на", "ковре", "и", "смотрит", "в", "окно"], tokT: "Потеря на каждом токене −ln pₜ, наты", mean: "среднее = CE", unif: "ln V (угадывание из V = 50 000)",
      ppl: "перплексия e^CE =", pfirst: "p(«Кошка») =",
    },
    en: {
      p: "Probability of the correct class $p$", ce: "−ln p (cross-entropy)", sq: "(1 − p)² (squared error)", dce: "−1/p", dsq: "−2(1 − p)",
      loss: "loss", deriv: "derivative in p", bits: "in bits −log₂ p =", nats: "−ln p =", dd: "d/dp =",
      right: "confident and right", wrong: "confident and wrong",
      logits: "Logits $z$ (drag them)", sy: "Prediction $s$ and target $y$", target: "target yₖ", push: "−(sₖ − yₖ): where zₖ moves", cls: "Correct class", eta: "Step $\\eta$", reset: "Reset",
      grad: "s − y =", step: "step", stepN: "step =",
      simplex: "Target p and prediction q in the simplex", decomp: "H(p, q) = H(p) + KL(p‖q), nats", hp: "H(p)", kl: "KL(p‖q)", hpq: "H(p, q)", inbits: "H(p, q) in bits =", level: "level lines of KL(p‖·)",
      surf: "CE(z₁, z₂, 0)", plane: "Top view: loss and anti-gradient", run: "Descent on the logits", path: "gradient-descent path", anti: "−∇CE",
      eps: "Smoothing $\\varepsilon$", K: "Classes $K$", m: "margin of the correct logit m", top: "Loss versus the margin m", bot: "Derivative dCE/dm = s − y", plain: "no smoothing (ε = 0)", smooth: "with smoothing",
      yc: "target for the correct class =", mstar: "optimal margin m* =", hmin: "minimum loss H(y) =",
      model: "Show the model", mCE: "trained on CE", mMSE: "trained on MSE", regions: "Class regions", accT: "Training accuracy, %", acc: "accuracy", gnorm: "mean |∂L/∂z|", class: "class",
      lam: "Confidence $\\lambda$", tokens: ["The", "cat", "sat", "on", "the", "mat", "and", "purred"], tokT: "Loss on every token −ln pₜ, nats", mean: "mean = CE", unif: "ln V (guessing among V = 50,000)",
      ppl: "perplexity e^CE =", pfirst: "p(“The”) =",
    },
    uz: {
      p: "To‘g‘ri sinf ehtimolligi $p$", ce: "−ln p (kross-entropiya)", sq: "(1 − p)² (kvadratik xato)", dce: "−1/p", dsq: "−2(1 − p)",
      loss: "yo‘qotish", deriv: "p bo‘yicha hosila", bits: "bitlarda −log₂ p =", nats: "−ln p =", dd: "d/dp =",
      right: "ishonchli va haq", wrong: "ishonchli, lekin xato",
      logits: "Logitlar $z$ (torting)", sy: "Bashorat $s$ va maqsad $y$", target: "maqsad yₖ", push: "−(sₖ − yₖ): zₖ qayerga siljiydi", cls: "To‘g‘ri sinf", eta: "Qadam $\\eta$", reset: "Tiklash",
      grad: "s − y =", step: "qadam", stepN: "qadam =",
      simplex: "Simpleksda maqsad p va bashorat q", decomp: "H(p, q) = H(p) + KL(p‖q), natlar", hp: "H(p)", kl: "KL(p‖q)", hpq: "H(p, q)", inbits: "bitlarda H(p, q) =", level: "KL(p‖·) sath chiziqlari",
      surf: "CE(z₁, z₂, 0)", plane: "Yuqoridan ko‘rinish: yo‘qotish va antigradiyent", run: "Logitlar bo‘yicha tushish", path: "gradiyentli tushish yo‘li", anti: "−∇CE",
      eps: "Silliqlash $\\varepsilon$", K: "Sinflar $K$", m: "to‘g‘ri logitning ustunligi m", top: "Yo‘qotish m ga qarab", bot: "Hosila dCE/dm = s − y", plain: "silliqlashsiz (ε = 0)", smooth: "silliqlash bilan",
      yc: "to‘g‘ri sinf uchun maqsad =", mstar: "optimal ustunlik m* =", hmin: "yo‘qotish minimumi H(y) =",
      model: "Modelni ko‘rsatish", mCE: "CE bilan o‘qitilgan", mMSE: "MSE bilan o‘qitilgan", regions: "Sinflar sohalari", accT: "O‘qitish to‘plamidagi aniqlik, %", acc: "aniqlik", gnorm: "o‘rtacha |∂L/∂z|", class: "sinf",
      lam: "Ishonch $\\lambda$", tokens: ["Mushuk", "gilamda", "o‘tirib", "derazadan", "tashqariga", "jim", "qarab", "turibdi"], tokT: "Har bir tokendagi yo‘qotish −ln pₜ, natlar", mean: "o‘rtacha = CE", unif: "ln V (V = 50 000 tadan taxmin)",
      ppl: "perpleksiya e^CE =", pfirst: "p(«Mushuk») =",
    },
  }[FV.lang] || {};

  const CLS = ["blue", "orange", "teal"];
  const SUB = ["₁", "₂", "₃"];
  const SEP = FV.lang === "en" ? ", " : "; ";
  const DEC = FV.lang === "en" ? "." : ",";
  function softmax(z) { const m = Math.max(...z), e = z.map((v) => Math.exp(v - m)), s = e.reduce((a, b) => a + b, 0); return e.map((v) => v / s); }
  function lse(z) { const m = Math.max(...z); return m + Math.log(z.reduce((a, v) => a + Math.exp(v - m), 0)); }
  const argmax = (s) => s.indexOf(Math.max(...s));
  const vec = (s, d = 3) => "(" + s.map((v) => FV.fmt(v, d)).join(SEP) + ")";
  const H = (p) => -p.reduce((a, v) => a + (v > 0 ? v * Math.log(v) : 0), 0);
  const Hx = (p, q) => -p.reduce((a, v, i) => a + (v > 0 ? v * Math.log(q[i]) : 0), 0);

  function rgbOf(name) {
    const c = FV.color(name) || "#888888";
    if (c[0] === "#") { const n = parseInt(c.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
    return (c.match(/\d+/g) || [136, 136, 136]).slice(0, 3).map(Number);
  }
  function paint(p, f, res = 3) {
    const w = Math.max(1, Math.round((p.x1 - p.x0) / res)), h = Math.max(1, Math.round((p.y0 - p.y1) / res));
    const cv = document.createElement("canvas"); cv.width = w; cv.height = h;
    const ctx = cv.getContext("2d"), img = ctx.createImageData(w, h);
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const c = f(p.sx.inv(p.x0 + ((i + 0.5) / w) * (p.x1 - p.x0)), p.sy.inv(p.y1 + ((j + 0.5) / h) * (p.y0 - p.y1)));
      if (!c) continue;
      const k = 4 * (j * w + i);
      img.data[k] = c[0]; img.data[k + 1] = c[1]; img.data[k + 2] = c[2]; img.data[k + 3] = c[3] == null ? 255 : c[3];
    }
    ctx.putImageData(img, 0, 0);
    const im = FV.svg("image", { x: p.x0, y: p.y1, width: p.x1 - p.x0, height: p.y0 - p.y1, preserveAspectRatio: "none", href: cv.toDataURL() });
    p.gMain.insertBefore(im, p.gMain.firstChild);
  }
  function regionColour(s, cols, gain = 150) {
    const k = argmax(s), t = Math.max(0, (s[k] - 1 / 3) / (2 / 3)), c = cols[k];
    return [c[0], c[1], c[2], Math.round(gain * Math.pow(t, 0.8))];
  }
  const onTheme = (fn) => document.addEventListener("themechange", () => fn());
  const barTicks = (n) => [1, 2, 3].map((i) => ({ v: i, label: n + SUB[i - 1] }));

  // Probability simplex: class 1 at the top, class 2 bottom-left, class 3 bottom-right.
  const H3 = Math.sqrt(3) / 2;
  const VX = [[0.5, H3], [0, 0], [1, 0]];
  const toXY = (s) => [s[0] * VX[0][0] + s[1] * VX[1][0] + s[2] * VX[2][0], s[0] * VX[0][1] + s[1] * VX[1][1] + s[2] * VX[2][1]];
  const toS = (x, y) => { const s1 = y / H3, s3 = x - 0.5 * s1; return [s1, 1 - s1 - s3, s3]; };
  function inside(s, lo) { const t = s.map((v) => Math.max(v, lo)); const k = t.reduce((a, b) => a + b, 0); return t.map((v) => v / k); }

  // 1. −ln p: the surprise of the correct answer, and its derivative.
  FV.widget("cross-entropy-surprise", (el, cfg) => {
    const w = FV.shell(el, {});
    const top = new FV.Plot(w.stage, { x: [0, 1], y: [0, 5.2], xLabel: "p", yLabel: L.loss, aspect: 0.48 });
    const bot = new FV.Plot(w.stage, { x: [0, 1], y: [-10.5, 0.5], xLabel: "p", yLabel: L.deriv, aspect: 0.26, minHeight: 170, maxHeight: 230 });
    const ro = FV.ui.readout(w.readout, [{ key: "p", label: "p =" }, { key: "n", label: L.nats, c: "blue" }, { key: "b", label: L.bits }, { key: "d", label: L.dd, c: "orange" }]);
    let p0 = cfg.p != null ? cfg.p : 0.665;
    const nl = (p) => -Math.log(p);
    const h = top.handle(p0, nl(p0), { c: "blue", label: "p", onDrag: (x) => { p0 = FV.clamp(Math.round(x * 1000) / 1000, 0.01, 1); return [p0, nl(p0)]; }, onChange: () => draw() });
    function draw() {
      top.clear();
      top.fn((p) => (1 - p) ** 2, { c: "faint", w: 1.8, dash: "6 5", from: 0 });
      top.area(nl, null, { c: "blue", fillOpacity: 0.08, from: 0.006 });
      top.fn(nl, { c: "blue", w: 2.6, from: 0.004 });
      top.dot(0.9, nl(0.9), { c: "ink", hollow: true, r: 4 }); top.dot(0.1, nl(0.1), { c: "ink", hollow: true, r: 4 });
      top.line(0.9, nl(0.9), 0.9, 1.15, { c: "guide", w: 1 });
      top.text(0.99, 1.15, L.right + ": " + FV.fmt(nl(0.9), 3), { anchor: "end", dy: -6 });
      top.text(0.1, nl(0.1), L.wrong + ": " + FV.fmt(nl(0.1), 3), { dx: 10, dy: -4 });
      top.line(p0, 0, p0, nl(p0), { c: "guide", w: 1, dash: "3 3" });
      h.set(p0, nl(p0));
      bot.clear(); bot.hline(0, { c: "guide", dash: false });
      bot.fn((p) => -2 * (1 - p), { c: "faint", w: 1.8, dash: "6 5" });
      bot.fn((p) => -1 / p, { c: "orange", w: 2.4, from: 0.09 });
      bot.dot(p0, Math.max(-1 / p0, -10.5), { c: "orange" });
      ro.set("p", FV.fmt(p0, 3)); ro.set("n", FV.fmt(nl(p0), 4)); ro.set("b", FV.fmt(-Math.log2(p0), 4)); ro.set("d", FV.fmt(-1 / p0, 3));
      top.legend([{ label: L.ce, c: "blue" }, { label: L.sq, c: "faint", dash: true }]);
      bot.legend([{ label: "d/dp (−ln p) = −1/p", c: "orange" }, { label: "d/dp (1 − p)² = −2(1 − p)", c: "faint", dash: true }]);
    }
    top.onresize = draw; bot.onresize = draw; draw();
  });

  // 2. The gradient s − y on one example, and gradient steps on the logits.
  FV.widget("cross-entropy-gradient", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const z0 = (cfg.z || [2, 1, 0]).slice();
    let z = z0.slice(), step = 0;
    const a = new FV.Plot(FV.col(w.stage), { x: [0.4, 3.6], y: [-6, 6], xTicks: barTicks("z"), aspect: 0.9, maxHeight: 340, title: L.logits });
    const b = new FV.Plot(FV.col(w.stage), { x: [0.4, 3.95], y: [0, 1.12], xTicks: barTicks("s"), aspect: 0.9, maxHeight: 340, title: L.sy });
    const k = FV.ui.seg({ label: L.cls, value: cfg.k || 0, options: [0, 1, 2].map((i) => ({ value: i, label: String(i + 1) })), onchange: draw });
    const se = FV.ui.slider({ label: L.eta, min: 0.1, max: 3, step: 0.1, value: cfg.eta || 1, fmt: (v) => FV.fmt(v, 1) });
    const player = FV.ui.player({
      interval: 450,
      onstep() {
        const s = softmax(z), y = [0, 1, 2].map((i) => (i === k.value ? 1 : 0));
        z = z.map((v, i) => FV.clamp(v - se.value * (s[i] - y[i]), -6, 6));
        step++; draw();
        return step < 60;
      },
      onreset() { z = z0.slice(); step = 0; draw(); },
    });
    w.controls.append(k.el, se.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "l", label: "CE =", c: "orange" }, { key: "g", label: L.grad }, { key: "t", label: L.stepN }]);
    const hs = z.map((v, i) => a.handle(i + 1, v, { c: CLS[i], label: "z" + SUB[i], onDrag: (x, yy) => { z[i] = Math.round(yy * 20) / 20; return [i + 1, z[i]]; }, onChange: () => draw() }));
    function draw() {
      const s = softmax(z), y = [0, 1, 2].map((i) => (i === k.value ? 1 : 0));
      a.clear(); a.hline(0, { c: "guide", dash: false });
      z.forEach((v, i) => {
        a.rect(i + 1 - 0.28, 0, i + 1 + 0.28, v, { c: CLS[i], opacity: 0.8 });
        a.text(i + 1 + 0.2, v, FV.fmt(v, 2), { dx: 6, dy: v >= 0 ? -6 : 14 });
        hs[i].set(i + 1, v);
      });
      b.clear();
      s.forEach((v, i) => {
        b.rect(i + 1 - 0.28, 0, i + 1 + 0.28, v, { c: CLS[i], opacity: 0.55 });
        b.line(i + 1 - 0.36, y[i], i + 1 + 0.36, y[i], { c: "ink", w: 2.6 });
        if (Math.abs(v - y[i]) > 0.035) b.arrow(i + 1, v, i + 1, y[i] + (y[i] > v ? -0.012 : 0.012), { c: "ink", w: 1.8, head: 7 });
        b.text(i + 1 + 0.3, (v + y[i]) / 2, (v - y[i] >= 0 ? "+" : "−") + FV.fmt(Math.abs(v - y[i]), 3), { dy: 4, size: 11 });
      });
      ro.set("l", FV.fmt(-Math.log(s[k.value]), 4)); ro.set("g", vec(s.map((v, i) => v - y[i]))); ro.set("t", String(step));
      b.legend([{ label: L.target, c: "ink" }, { label: L.push, c: "ink", dot: false }]);
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 3. Entropy, cross-entropy and KL divergence on the probability simplex.
  FV.widget("cross-entropy-kl", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const p = new FV.Plot(FV.col(w.stage), { x: [-0.12, 1.12], y: [-0.13, 0.95], equal: true, grid: false, xTicks: [], yTicks: [], margin: { l: 6, r: 6, t: 6, b: 6 }, title: L.simplex });
    const b = new FV.Plot(FV.col(w.stage), { x: [0, 2], y: [-0.6, 1.6], yTicks: [{ v: 1, label: "H(p, q)" }, { v: 0, label: "H + KL" }], margin: { l: 64 }, aspect: 0.75, maxHeight: 300, title: L.decomp });
    let P = (cfg.p || [0.7, 0.2, 0.1]).slice(), Q = (cfg.q || [0.25, 0.5, 0.25]).slice();
    const hp = p.handle(0, 0, { c: "ink", label: "p", onDrag: (x, y) => { P = inside(toS(x, y), 0); return toXY(P); }, onChange: () => draw() });
    const hq = p.handle(0, 0, { c: "red", label: "q", onDrag: (x, y) => { Q = inside(toS(x, y), 0.01); return toXY(Q); }, onChange: () => draw() });
    const rs = FV.ui.button({ label: L.reset, onclick: () => { P = (cfg.p || [0.7, 0.2, 0.1]).slice(); Q = (cfg.q || [0.25, 0.5, 0.25]).slice(); draw(); } });
    w.controls.append(rs.el);
    const ro = FV.ui.readout(w.readout, [{ key: "p", label: "p =" }, { key: "q", label: "q =", c: "red" }, { key: "h", label: "H(p) =", c: "violet" }, { key: "k", label: "KL(p‖q) =", c: "orange" }, { key: "x", label: "H(p, q) =" }, { key: "b", label: L.inbits }]);
    function draw() {
      const hP = H(P), hPQ = Hx(P, Q), kl = hPQ - hP;
      p.clear();
      paint(p, (x, y) => {
        const q = toS(x, y);
        if (Math.min(...q) < -0.003) return null;
        const v = Hx(P, q.map((t) => Math.max(t, 1e-9))) - hP, t = FV.clamp(Math.sqrt(Math.max(v, 0) / 3), 0, 1);
        const c = FV.cmap("viridis", 1 - t);
        return [c[0], c[1], c[2], 190];
      }, 3);
      const fq = (x, y) => { const q = toS(x, y); return Math.min(...q) < 0.015 ? NaN : Hx(P, q) - hP; };
      p.contours(fq, [0.05, 0.25, 0.75], { c: "ink", w: 1, opacity: 0.55, n: 110 });
      p.path([VX[0], VX[1], VX[2]], { c: "ink", w: 1.4, close: true });
      p.text(0.5, H3 + 0.035, "1", { c: "blue", anchor: "middle" });
      p.text(-0.02, -0.075, "2", { c: "orange", anchor: "start" });
      p.text(1.02, -0.075, "3", { c: "teal", anchor: "end" });
      const XP = toXY(P), XQ = toXY(Q);
      p.line(XP[0], XP[1], XQ[0], XQ[1], { c: "ink", w: 1.4, dash: "4 3" });
      p.text(XP[0], XP[1], "p", { dx: 12, dy: -10, c: "ink" }); p.text(XQ[0], XQ[1], "q", { dx: 12, dy: -10, c: "red" });
      hp.set(XP[0], XP[1]); hq.set(XQ[0], XQ[1]);
      const xmax = Math.max(1.5, Math.ceil(hPQ * 1.15 * 2) / 2);
      b.setDomain([0, xmax]); b.clear();
      b.rect(0, 0.72, hPQ, 1.28, { c: "ink", opacity: 0.75 });
      b.rect(0, -0.28, hP, 0.28, { c: "violet", opacity: 0.8 });
      b.rect(hP, -0.28, hPQ, 0.28, { c: "orange", opacity: 0.85 });
      b.line(hPQ, -0.5, hPQ, 1.45, { c: "guide", w: 1, dash: "3 3" });
      b.text(hPQ, 1.3, FV.fmt(hPQ, 3), { anchor: hPQ > xmax * 0.8 ? "end" : "start", dx: hPQ > xmax * 0.8 ? -4 : 4, dy: -4 });
      ro.set("p", vec(P, 2)); ro.set("q", vec(Q, 2)); ro.set("h", FV.fmt(hP, 3)); ro.set("k", FV.fmt(kl, 3)); ro.set("x", FV.fmt(hPQ, 3)); ro.set("b", FV.fmt(hPQ / Math.LN2, 3));
      p.legend([{ label: "p", c: "ink", dot: true }, { label: "q", c: "red", dot: true }, { label: L.level, c: "ink" }]);
      b.legend([{ label: L.hpq, c: "ink", box: true }, { label: L.hp, c: "violet", box: true }, { label: L.kl, c: "orange", box: true }]);
    }
    onTheme(draw);
    p.onresize = draw; b.onresize = draw; draw();
  });

  // 4. The loss landscape in the logit plane (z₃ = 0): a 3D surface, the anti-gradient field and gradient descent.
  FV.widget("cross-entropy-landscape", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const R = 5;
    let k = cfg.k || 0;
    const ce = (a, b) => { const z = [a, b, 0]; return lse(z) - z[k]; };
    const S = new FV.Surface(FV.col(w.stage), { f: ce, x: [-R, R], y: [-R, R], n: 34, labels: { x: "z₁", y: "z₂", z: "CE" }, azimuth: cfg.az != null ? cfg.az : -0.6, elevation: 0.5, aspect: 0.9, title: L.surf });
    const p = new FV.Plot(FV.col(w.stage), { x: [-R, R], y: [-R, R], xLabel: "z₁", yLabel: "z₂", equal: true, title: L.plane });
    let pt = (cfg.z || [2, 1]).slice(0, 2), path = [pt.slice()];
    const kseg = FV.ui.seg({ label: L.cls, value: k, options: [0, 1, 2].map((i) => ({ value: i, label: String(i + 1) })), onchange: (v) => { k = v; S.setF(ce); path = [pt.slice()]; draw(); } });
    const player = FV.ui.player({
      interval: 140,
      onstep() {
        const s = softmax([pt[0], pt[1], 0]);
        pt = [FV.clamp(pt[0] - 0.8 * (s[0] - (k === 0 ? 1 : 0)), -R, R), FV.clamp(pt[1] - 0.8 * (s[1] - (k === 1 ? 1 : 0)), -R, R)];
        path.push(pt.slice()); draw();
        return path.length < 80;
      },
      onreset() { pt = (cfg.z || [2, 1]).slice(0, 2); path = [pt.slice()]; draw(); },
    });
    w.controls.append(kseg.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "l", label: "CE =", c: "red" }, { key: "g", label: "∇CE = s − y =" }, { key: "t", label: L.stepN }]);
    const h = p.handle(pt[0], pt[1], { c: "red", label: "z", onDrag: (x, y) => { pt = [Math.round(x * 10) / 10, Math.round(y * 10) / 10]; path = [pt.slice()]; return pt; }, onChange: () => draw() });
    function draw() {
      p.clear();
      p.heat(ce, { cmap: "viridis", res: 4, z: [0, 10.5], transform: (v) => Math.sqrt(Math.max(v, 0)) });
      p.contours(ce, [0.1, 0.5, 1, 2, 4, 7], { c: "ink", w: 1, opacity: 0.5, n: 80 });
      for (let gx = -4; gx <= 4; gx += 2) for (let gy = -4; gy <= 4; gy += 2) {
        const s = softmax([gx, gy, 0]), u = -(s[0] - (k === 0 ? 1 : 0)), v = -(s[1] - (k === 1 ? 1 : 0));
        if (Math.hypot(u, v) > 0.04) p.arrow(gx, gy, gx + 0.9 * u, gy + 0.9 * v, { c: "ink", w: 1.4, head: 6 });
      }
      if (path.length > 1) p.path(path, { c: "red", w: 2.4 });
      h.set(pt[0], pt[1]);
      S.setPaths(path.length > 1 ? [{ pts: path.map((q) => [q[0], q[1], ce(q[0], q[1])]), c: "red", w: 2.5 }] : []);
      S.setPoints([{ x: pt[0], y: pt[1], z: ce(pt[0], pt[1]), c: "red", r: 5.5 }]);
      const s = softmax([pt[0], pt[1], 0]), y = [0, 1, 2].map((i) => (i === k ? 1 : 0));
      ro.set("l", FV.fmt(ce(pt[0], pt[1]), 4)); ro.set("g", vec(s.map((v, i) => v - y[i]))); ro.set("t", String(path.length - 1));
      p.legend([{ label: L.anti, c: "ink" }, { label: L.path, c: "red" }]);
    }
    onTheme(draw);
    p.onresize = draw; draw();
  });

  // 5. Label smoothing: the loss and its derivative as functions of the margin of the correct logit.
  FV.widget("cross-entropy-smoothing", (el, cfg) => {
    const w = FV.shell(el, {});
    const top = new FV.Plot(w.stage, { x: [-2, 10], y: [0, 3.5], xLabel: L.m, yLabel: "CE", aspect: 0.42, title: L.top });
    const bot = new FV.Plot(w.stage, { x: [-2, 10], y: [-1.05, 0.25], xLabel: L.m, yLabel: "dCE/dm", aspect: 0.26, minHeight: 170, maxHeight: 230, title: L.bot });
    const se = FV.ui.slider({ label: L.eps, min: 0, max: 0.3, step: 0.01, value: cfg.eps != null ? cfg.eps : 0.1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sk = FV.ui.seg({ label: L.K, value: cfg.K || 3, options: [3, 10, 100].map((v) => ({ value: v, label: String(v) })), onchange: draw });
    w.controls.append(se.el, sk.el);
    const ro = FV.ui.readout(w.readout, [{ key: "y", label: L.yc }, { key: "m", label: L.mstar, c: "orange" }, { key: "h", label: L.hmin }]);
    function draw() {
      const e = se.value, K = sk.value, yc = 1 - e + e / K;
      const loss = (m, y) => -y * m + Math.max(m, 0) + Math.log(Math.exp(m - Math.max(m, 0)) + (K - 1) * Math.exp(-Math.max(m, 0)));
      const sc = (m) => 1 / (1 + (K - 1) * Math.exp(-m));
      top.setDomain(null, [0, { 3: 3.5, 10: 5, 100: 7.5 }[K]]);
      top.clear(); bot.clear();
      top.fn((m) => loss(m, 1), { c: "faint", w: 2, dash: "6 5" });
      top.fn((m) => loss(m, yc), { c: "blue", w: 2.6 });
      bot.hline(0, { c: "guide", dash: false });
      bot.fn((m) => sc(m) - 1, { c: "faint", w: 2, dash: "6 5" });
      bot.fn((m) => sc(m) - yc, { c: "blue", w: 2.6 });
      const yv = [yc].concat(Array(K - 1).fill(e / K)), hmin = H(yv);
      if (e > 0) {
        const ms = Math.log(1 + (K * (1 - e)) / e);
        if (ms < 10) {
          top.line(ms, 0, ms, loss(ms, yc), { c: "orange", w: 1.2, dash: "4 3" }); top.dot(ms, loss(ms, yc), { c: "orange" });
          bot.line(ms, -1.05, ms, 0, { c: "orange", w: 1.2, dash: "4 3" }); bot.dot(ms, 0, { c: "orange" });
        }
        ro.set("m", FV.fmt(ms, 3));
      } else ro.set("m", "∞");
      ro.set("y", FV.fmt(yc, 4)); ro.set("h", FV.fmt(hmin, 4));
      top.legend([{ label: L.smooth + " (ε = " + FV.fmt(e, 2) + ")", c: "blue" }, { label: L.plain, c: "faint", dash: true }, { label: "m*", c: "orange", dot: true }]);
      bot.legend([{ label: L.smooth, c: "blue" }, { label: L.plain, c: "faint", dash: true }]);
    }
    top.onresize = draw; bot.onresize = draw; draw();
  });

  // Three Gaussian clouds, one per class (deterministic; the same data as on the softmax page).
  function clouds(seed, n, r, sd) {
    const R = FV.rng(seed), pts = [];
    for (let k = 0; k < 3; k++) {
      const a = Math.PI / 2 + (2 * Math.PI * k) / 3, cx = r * Math.cos(a), cy = r * Math.sin(a);
      for (let i = 0; i < n; i++) { const x = cx + sd * R.normal(), y = cy + sd * R.normal(); pts.push({ x, y, c: k }); }
    }
    return pts;
  }

  // 6. CE against MSE on top of softmax, from the same confidently wrong start.
  FV.widget("cross-entropy-train", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const pts = clouds(3, 30, 1.6, 0.85), N = cfg.steps || 200, lr = cfg.lr || 0.5, sc = cfg.scale || 3;
    const A = new FV.Plot(FV.col(w.stage), { x: [-4, 4], y: [-4, 4], xLabel: "x₁", yLabel: "x₂", equal: true, title: L.regions });
    const B = new FV.Plot(FV.col(w.stage), { x: [0, N], y: [0, 100], xLabel: L.step, yLabel: "%", aspect: 1, maxHeight: 360, title: L.accT });
    const ang = [0, 1, 2].map((k) => Math.PI / 2 + (2 * Math.PI * k) / 3);
    function init() { return { W: [0, 1, 2].map((k) => [sc * Math.cos(ang[(k + 1) % 3]), sc * Math.sin(ang[(k + 1) % 3])]), b: [0, 0, 0], acc: [], g: 0 }; }
    let M = { ce: init(), mse: init() }, step = 0;
    const scores = (m, x, y) => [0, 1, 2].map((k) => m.W[k][0] * x + m.W[k][1] * y + m.b[k]);
    function evalm(m) {
      let acc = 0;
      pts.forEach((q) => { acc += argmax(scores(m, q.x, q.y)) === q.c ? 1 : 0; });
      return [acc / pts.length];
    }
    function gd(m, kind) {
      const gW = [[0, 0], [0, 0], [0, 0]], gb = [0, 0, 0];
      pts.forEach((q) => {
        const s = softmax(scores(m, q.x, q.y)), y = [0, 1, 2].map((k) => (k === q.c ? 1 : 0));
        let g;
        if (kind === "ce") g = s.map((v, k) => v - y[k]);
        else { const d = s.map((v, k) => 2 * (v - y[k])), ds = d.reduce((a, v, k) => a + v * s[k], 0); g = s.map((v, k) => v * (d[k] - ds)); }
        for (let k = 0; k < 3; k++) { gW[k][0] += g[k] * q.x; gW[k][1] += g[k] * q.y; gb[k] += g[k]; }
      });
      const n = pts.length;
      for (let k = 0; k < 3; k++) { m.W[k][0] -= (lr * gW[k][0]) / n; m.W[k][1] -= (lr * gW[k][1]) / n; m.b[k] -= (lr * gb[k]) / n; }
    }
    function gradNorm(m, kind) {
      let gn = 0;
      pts.forEach((q) => {
        const s = softmax(scores(m, q.x, q.y)), y = [0, 1, 2].map((k) => (k === q.c ? 1 : 0));
        if (kind === "ce") gn += Math.hypot(...s.map((v, k) => v - y[k]));
        else { const d = s.map((v, k) => 2 * (v - y[k])), ds = d.reduce((a, v, k) => a + v * s[k], 0); gn += Math.hypot(...s.map((v, k) => v * (d[k] - ds))); }
      });
      return gn / pts.length;
    }
    function reset() { M = { ce: init(), mse: init() }; step = 0; ["ce", "mse"].forEach((k) => { M[k].acc = [evalm(M[k])[0]]; M[k].g = gradNorm(M[k], k); }); }
    reset();
    const show = FV.ui.seg({ label: L.model, value: "ce", options: [{ value: "ce", label: L.mCE }, { value: "mse", label: L.mMSE }], onchange: draw });
    const player = FV.ui.player({
      interval: 50,
      onstep() {
        if (step >= N) return false;
        ["ce", "mse"].forEach((k) => { gd(M[k], k); M[k].acc.push(evalm(M[k])[0]); M[k].g = gradNorm(M[k], k); });
        step++; draw();
        return step < N;
      },
      onreset() { reset(); draw(); },
    });
    w.controls.append(show.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.stepN }, { key: "a", label: L.acc + " CE =", c: "ink" }, { key: "b", label: L.acc + " MSE =", c: "violet" }, { key: "g", label: L.gnorm + " CE / MSE =" }]);
    let cols = CLS.map(rgbOf);
    function draw() {
      const m = M[show.value];
      A.clear();
      paint(A, (x, y) => regionColour(softmax(scores(m, x, y)), cols, 150), 4);
      pts.forEach((q) => A.dot(q.x, q.y, { c: CLS[q.c], r: 4 }));
      B.clear();
      B.path(M.mse.acc.map((v, i) => [i, 100 * v]), { c: "violet", w: 2.4 });
      B.path(M.ce.acc.map((v, i) => [i, 100 * v]), { c: "ink", w: 2.4 });
      B.dot(step, 100 * M.mse.acc[step], { c: "violet", r: 4 }); B.dot(step, 100 * M.ce.acc[step], { c: "ink", r: 4 });
      ro.set("t", String(step)); ro.set("a", FV.fmt(100 * M.ce.acc[step], 1) + "%"); ro.set("b", FV.fmt(100 * M.mse.acc[step], 1) + "%");
      ro.set("g", FV.num(M.ce.g, 2) + " / " + FV.num(M.mse.g, 2));
      A.legend([0, 1, 2].map((k) => ({ label: L.class + " " + (k + 1), c: CLS[k], dot: true })));
      B.legend([{ label: L.mCE, c: "ink" }, { label: L.mMSE, c: "violet" }]);
    }
    onTheme(() => { cols = CLS.map(rgbOf); draw(); });
    A.onresize = draw; B.onresize = draw; draw();
  });

  // 7. Language models: per-token loss, its mean (CE) and perplexity e^CE.
  FV.widget("cross-entropy-perplexity", (el, cfg) => {
    const w = FV.shell(el, {});
    const V = 50000, P1 = cfg.p || [0.05, 0.3, 0.85, 0.2, 0.6, 0.25, 0.8, 0.55];
    const margin = P1.map((p) => Math.log((p * (V - 1)) / (1 - p)));
    const n = P1.length, toks = L.tokens || P1.map((_, i) => "t" + (i + 1));
    const p = new FV.Plot(w.stage, {
      x: [0, 11.5], y: [-0.6, n - 0.4], xLabel: "−ln pₜ", aspect: 0.55, maxHeight: 380, margin: { l: 82 },
      yTicks: toks.map((t, i) => ({ v: n - 1 - i, label: t })), title: L.tokT,
    });
    const sl = FV.ui.slider({ label: L.lam, min: 0, max: 1, step: 0.01, value: cfg.lambda != null ? cfg.lambda : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw, wide: true });
    w.controls.append(sl.el);
    const ro = FV.ui.readout(w.readout, [{ key: "c", label: "CE =", c: "orange" }, { key: "p", label: L.ppl }, { key: "f", label: L.pfirst }]);
    function draw() {
      const lam = sl.value;
      const pt = margin.map((m) => 1 / (1 + (V - 1) * Math.exp(-lam * m)));
      const loss = pt.map((v) => -Math.log(v)), ce = loss.reduce((a, b) => a + b, 0) / n;
      p.clear();
      p.vline(Math.log(V), { c: "faint", dash: "5 4", w: 1.4 });
      loss.forEach((v, i) => {
        const y = n - 1 - i;
        p.rect(0, y - 0.32, v, y + 0.32, { c: "blue", opacity: 0.8 });
        const out = v < 8.6;
        p.text(v, y, FV.fmt(v, 2) + "  (p = " + FV.num(pt[i], 2) + ")", { dx: out ? 6 : -6, dy: 4, anchor: out ? "start" : "end", size: 11 });
      });
      p.vline(ce, { c: "orange", dash: false, w: 2.2 });
      ro.set("c", FV.fmt(ce, 3)); ro.set("p", FV.num(Math.exp(ce), 4)); ro.set("f", FV.num(pt[0], 2));
      p.legend([{ label: "−ln pₜ", c: "blue", box: true }, { label: L.mean, c: "orange" }, { label: L.unif, c: "faint", dash: true }]);
    }
    p.onresize = draw; draw();
  });
})();
