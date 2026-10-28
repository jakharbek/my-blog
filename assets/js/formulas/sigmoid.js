/* Widgets of the formula page "Sigmoid". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      x: "x", sig: "σ(x)", dsig: "σ′(x)", one: "1 − σ(x)", deriv: "Показать производную", tangent: "касательная",
      asym: "асимптоты", slope: "наклон", w: "Вес $w$", b: "Сдвиг $b$", center: "центр $x_0=-b/w$", ref: "σ(x) для сравнения",
      steep: "наклон в центре $w/4$", p: "Вероятность $p$", odds: "шансы $p/(1-p)$", logit: "логит $\\ln\\frac{p}{1-p}$",
      x1: "x₁", x2: "x₂", prob: "p", train: "Обучать", acc: "точность", loss: "BCE", epoch: "шаг",
      depth: "Глубина сети $L$", layer: "слой", grad: "‖∂ℒ/∂h‖", first: "градиент у входа / у выхода",
      spread: "Разброс входов $s$", mean: "Среднее входов $\\mu$", density: "плотность входов", avg: "средняя σ′", dead: "доля входов с σ′ < 0,01",
      order: "Порядок", err: "ошибка в x", approx: "приближение", w1: "$w_1$", w2: "$w_2$", class0: "класс 0", class1: "класс 1", boundary: "граница p = 0,5",
    },
    en: {
      x: "x", sig: "σ(x)", dsig: "σ′(x)", one: "1 − σ(x)", deriv: "Show the derivative", tangent: "tangent",
      asym: "asymptotes", slope: "slope", w: "Weight $w$", b: "Bias $b$", center: "centre $x_0=-b/w$", ref: "σ(x) for reference",
      steep: "slope at the centre $w/4$", p: "Probability $p$", odds: "odds $p/(1-p)$", logit: "logit $\\ln\\frac{p}{1-p}$",
      x1: "x₁", x2: "x₂", prob: "p", train: "Train", acc: "accuracy", loss: "BCE", epoch: "step",
      depth: "Network depth $L$", layer: "layer", grad: "‖∂ℒ/∂h‖", first: "gradient at the input / at the output",
      spread: "Input spread $s$", mean: "Input mean $\\mu$", density: "input density", avg: "mean σ′", dead: "share of inputs with σ′ < 0.01",
      order: "Order", err: "error at x", approx: "approximation", w1: "$w_1$", w2: "$w_2$", class0: "class 0", class1: "class 1", boundary: "boundary p = 0.5",
    },
    uz: {
      x: "x", sig: "σ(x)", dsig: "σ′(x)", one: "1 − σ(x)", deriv: "Hosilani ko‘rsatish", tangent: "urinma",
      asym: "asimptotalar", slope: "qiyalik", w: "Vazn $w$", b: "Siljish $b$", center: "markaz $x_0=-b/w$", ref: "taqqoslash uchun σ(x)",
      steep: "markazdagi qiyalik $w/4$", p: "Ehtimollik $p$", odds: "imkoniyat $p/(1-p)$", logit: "logit $\\ln\\frac{p}{1-p}$",
      x1: "x₁", x2: "x₂", prob: "p", train: "O‘qitish", acc: "aniqlik", loss: "BCE", epoch: "qadam",
      depth: "Tarmoq chuqurligi $L$", layer: "qatlam", grad: "‖∂ℒ/∂h‖", first: "kirishdagi / chiqishdagi gradiyent",
      spread: "Kirishlar tarqoqligi $s$", mean: "Kirishlar o‘rtachasi $\\mu$", density: "kirishlar zichligi", avg: "o‘rtacha σ′", dead: "σ′ < 0,01 bo‘lgan kirishlar ulushi",
      order: "Tartib", err: "x dagi xato", approx: "yaqinlashish", w1: "$w_1$", w2: "$w_2$", class0: "0-sinf", class1: "1-sinf", boundary: "chegara p = 0,5",
    },
  }[FV.lang] || {};
  const sig = FV.sigmoid;
  const dsig = (x) => { const s = sig(x); return s * (1 - s); };

  // 1. The curve, a draggable point, its tangent, and (optionally) the derivative below.
  FV.widget("sigmoid-explorer", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-8, 8], y: [-0.12, 1.12], xLabel: L.x, yLabel: L.sig, aspect: 0.5 });
    const box = FV.h("div"); w.stage.append(box);
    let d = null;
    const show = FV.ui.check({ label: L.deriv, checked: cfg.derivative !== false, onchange: (v) => { box.hidden = !v; draw(); } });
    w.controls.append(show.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "s", label: "σ(x) =", c: "blue" }, { key: "o", label: "1 − σ(x) =" }, { key: "d", label: "σ′(x) =", c: "orange" }]);
    let x0 = cfg.x != null ? cfg.x : 1.5;
    const h = p.handle(x0, sig(x0), { c: "blue", onDrag: (x) => { x0 = x; return [x, sig(x)]; }, onChange: () => draw() });
    function ensureD() {
      if (!d) {
        d = new FV.Plot(box, { x: [-8, 8], y: [-0.02, 0.28], xLabel: L.x, yLabel: L.dsig, aspect: 0.28, minHeight: 160, maxHeight: 220 });
        d.onresize = draw;
      }
    }
    function draw() {
      p.clear();
      p.hline(0, { c: "blue", dash: false, w: 1.2, opacity: 0.55 }); p.hline(1, { c: "blue", dash: false, w: 1.2, opacity: 0.55 });
      p.vline(0, {}); p.hline(0.5, {});
      const k = dsig(x0), y0 = sig(x0);
      p.line(x0 - 3, y0 - 3 * k, x0 + 3, y0 + 3 * k, { c: "orange", w: 1.8 });
      p.fn(sig, { c: "ink", w: 2.4 });
      p.line(x0, 0, x0, y0, { c: "guide", w: 1, dash: "3 3" });
      p.text(7.8, 1.04, "y = 1", { c: "blue", anchor: "end" }); p.text(7.8, 0.04, "y = 0", { c: "blue", anchor: "end" });
      p.dot(0, 0.5, { hollow: true, r: 4 });
      h.set(x0, y0);
      if (show.value) {
        ensureD(); box.hidden = false;
        d.clear(); d.hline(0.25, { c: "orange", opacity: 0.6 });
        d.area(dsig, null, { c: "orange", fillOpacity: 0.12 });
        d.fn(dsig, { c: "orange", w: 2.2 });
        d.line(x0, 0, x0, k, { c: "orange", w: 1, dash: "3 3" });
        d.dot(x0, k, { c: "orange" });
        d.text(0.25, 0.262, "max = 0,25".replace(",", FV.lang === "en" ? "." : ","), { c: "orange" });
      }
      ro.set("x", FV.fmt(x0, 2)); ro.set("s", FV.fmt(y0, 4)); ro.set("o", FV.fmt(1 - y0, 4)); ro.set("d", FV.fmt(k, 4));
      p.legend([{ label: L.sig, c: "ink" }, { label: L.tangent + " (" + L.slope + " = σ′)", c: "orange" }, { label: L.asym, c: "blue" }]);
    }
    p.onresize = draw;
    draw();
  });

  // 2. σ(w·x + b): weight sets the steepness, bias shifts the centre.
  FV.widget("sigmoid-shape", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-6, 6], y: [-0.12, 1.12], xLabel: L.x, yLabel: "σ(wx + b)", aspect: 0.5 });
    const sw = FV.ui.slider({ label: L.w, min: -6, max: 6, step: 0.1, value: cfg.w != null ? cfg.w : 2, oninput: draw });
    const sb = FV.ui.slider({ label: L.b, min: -6, max: 6, step: 0.1, value: cfg.b != null ? cfg.b : -2, oninput: draw });
    w.controls.append(sw.el, sb.el);
    const ro = FV.ui.readout(w.readout, [{ key: "c", label: L.center + " =" }, { key: "k", label: L.steep + " =" }]);
    function draw() {
      const W = sw.value, B = sb.value, f = (x) => sig(W * x + B);
      p.clear(); p.hline(0.5, {}); p.vline(0, {});
      p.fn(sig, { c: "guide", w: 1.6, dash: "5 4" });
      [0.25, 0.5].forEach((t) => p.fn((x) => sig(W * t * x + B * t), { c: "blue", w: 1.2, opacity: 0.25 + t * 0.3 }));
      p.fn(f, { c: "blue", w: 2.6 });
      if (Math.abs(W) > 1e-9) {
        const c = -B / W;
        if (c > -6 && c < 6) {
          p.line(c, -0.12, c, 0.5, { c: "orange", w: 1, dash: "3 3" });
          p.line(c - 0.6, 0.5 - 0.6 * W / 4, c + 0.6, 0.5 + 0.6 * W / 4, { c: "orange", w: 2 });
          p.dot(c, 0.5, { c: "orange" });
        }
        ro.set("c", FV.fmt(c, 2)); ro.set("k", FV.fmt(W / 4, 3));
      } else { ro.set("c", "—"); ro.set("k", FV.fmt(0, 3)); }
      p.legend([{ label: "σ(wx + b)", c: "blue" }, { label: L.ref, c: "guide", dash: true }, { label: L.center, c: "orange", dot: true }]);
    }
    p.onresize = draw; draw();
  });

  // 3. Taylor polynomials around zero versus the sigmoid.
  FV.widget("sigmoid-taylor", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-6, 6], y: [-0.4, 1.4], xLabel: L.x, yLabel: "y", aspect: 0.5 });
    const terms = [(x) => 0.5, (x) => x / 4, (x) => -(x ** 3) / 48, (x) => (x ** 5) / 480, (x) => (-17 * x ** 7) / 80640];
    const ord = FV.ui.seg({ label: L.order, value: 3, options: [{ value: 1, label: "1" }, { value: 3, label: "3" }, { value: 5, label: "5" }, { value: 7, label: "7" }], onchange: draw });
    const sx = FV.ui.slider({ label: "x", min: -6, max: 6, step: 0.05, value: 2, oninput: draw });
    w.controls.append(ord.el, sx.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: "σ(x) =" }, { key: "t", label: L.approx + " =", c: "orange" }, { key: "e", label: L.err + " =" }]);
    function T(x) { const n = { 1: 2, 3: 3, 5: 4, 7: 5 }[ord.value]; let s = 0; for (let i = 0; i < n; i++) s += terms[i](x); return s; }
    function draw() {
      p.clear(); p.hline(0, { dash: false, c: "guide" }); p.hline(1, { dash: false, c: "guide" });
      p.rect(-Math.PI, -0.4, Math.PI, 1.4, { c: "teal", opacity: 0.06 });
      p.vline(-Math.PI, { c: "teal" }); p.vline(Math.PI, { c: "teal" });
      p.text(Math.PI, 1.3, "π", { c: "teal", dx: 4 }); p.text(-Math.PI, 1.3, "−π", { c: "teal", dx: 4 });
      p.fn(sig, { c: "ink", w: 2.4 });
      p.fn(T, { c: "orange", w: 2.2 });
      const x = sx.value;
      p.dot(x, sig(x), { c: "ink", r: 4 }); p.dot(x, T(x), { c: "orange", r: 4 });
      ro.set("s", FV.fmt(sig(x), 4)); ro.set("t", FV.fmt(T(x), 4)); ro.set("e", FV.num(Math.abs(T(x) - sig(x)), 2));
      p.legend([{ label: "σ(x)", c: "ink" }, { label: L.approx + " " + ord.value, c: "orange" }, { label: "|x| < π", c: "teal", box: true }]);
    }
    p.onresize = draw; draw();
  });

  // 4. Probability ↔ odds ↔ log-odds.
  FV.widget("sigmoid-logit", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-6, 6], y: [-0.05, 1.05], xLabel: "z = ln(p / (1 − p))", yLabel: "p = σ(z)", aspect: 0.75, title: "σ: z → p" });
    const b = new FV.Plot(FV.col(w.stage), { x: [0.0025, 0.9975], y: [-6, 6], xLabel: "p", yLabel: "logit(p)", aspect: 0.75, title: "logit = σ⁻¹: p → z" });
    const sp = FV.ui.slider({ label: L.p, min: 0.01, max: 0.99, step: 0.01, value: cfg.p || 0.8, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sp.el);
    const ro = FV.ui.readout(w.readout, [{ key: "p", label: "p =" }, { key: "o", label: L.odds + " =", c: "teal" }, { key: "z", label: L.logit + " =", c: "orange" }]);
    const logit = (q) => Math.log(q / (1 - q));
    function draw() {
      const q = sp.value, z = logit(q);
      a.clear(); a.fn(sig, { c: "ink", w: 2.2 });
      a.line(z, -0.05, z, q, { c: "orange", w: 1.4, dash: "4 3" }); a.line(-6, q, z, q, { c: "blue", w: 1.4, dash: "4 3" });
      a.dot(z, q, { c: "blue" });
      b.clear(); b.fn(logit, { c: "ink", w: 2.2 });
      b.line(q, -6, q, z, { c: "blue", w: 1.4, dash: "4 3" }); b.line(0.0025, z, q, z, { c: "orange", w: 1.4, dash: "4 3" });
      b.dot(q, z, { c: "orange" });
      ro.set("p", FV.fmt(q, 2)); ro.set("o", FV.num(q / (1 - q), 3)); ro.set("z", FV.fmt(z, 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // Two Gaussian clouds for logistic regression (deterministic).
  function cloud() {
    const r = FV.rng(7), pts = [];
    for (let i = 0; i < 40; i++) pts.push({ x: -1.1 + 1.0 * r.normal(), y: -0.8 + 1.0 * r.normal(), c: 0 });
    for (let i = 0; i < 40; i++) pts.push({ x: 1.1 + 1.0 * r.normal(), y: 0.9 + 1.0 * r.normal(), c: 1 });
    return pts;
  }

  // 5. Logistic regression in 2D: a 3D probability surface, a heatmap with the boundary, and live training.
  FV.widget("sigmoid-logreg", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const pts = cloud();
    const P = { w1: cfg.w1 != null ? cfg.w1 : -0.5, w2: cfg.w2 != null ? cfg.w2 : 1.5, b: cfg.b != null ? cfg.b : 1.5 };
    const prob = (x, y) => sig(P.w1 * x + P.w2 * y + P.b);
    const s3 = new FV.Surface(FV.col(w.stage), { f: prob, x: [-4, 4], y: [-4, 4], z: [0, 1], n: 34, labels: { x: L.x1, y: L.x2, z: "p" }, azimuth: -0.6, elevation: 0.55, aspect: 0.85, cmap: "diverging", title: "p = σ(w₁x₁ + w₂x₂ + b)" });
    const h2 = new FV.Plot(FV.col(w.stage), { x: [-4, 4], y: [-4, 4], xLabel: L.x1, yLabel: L.x2, equal: true, title: "p(x₁, x₂)" });
    const s1 = FV.ui.slider({ label: L.w1, min: -4, max: 4, step: 0.05, value: P.w1, oninput: (v) => { P.w1 = v; draw(); } });
    const s2 = FV.ui.slider({ label: L.w2, min: -4, max: 4, step: 0.05, value: P.w2, oninput: (v) => { P.w2 = v; draw(); } });
    const sb = FV.ui.slider({ label: "$b$", min: -4, max: 4, step: 0.05, value: P.b, oninput: (v) => { P.b = v; draw(); } });
    let step = 0;
    const lr = 0.5;
    const player = FV.ui.player({
      interval: 90,
      onstep() {
        let g1 = 0, g2 = 0, gb = 0;
        pts.forEach((q) => { const e = prob(q.x, q.y) - q.c; g1 += e * q.x; g2 += e * q.y; gb += e; });
        const n = pts.length;
        P.w1 -= (lr * g1) / n; P.w2 -= (lr * g2) / n; P.b -= (lr * gb) / n;
        P.w1 = FV.clamp(P.w1, -4, 4); P.w2 = FV.clamp(P.w2, -4, 4); P.b = FV.clamp(P.b, -4, 4);
        s1.set(P.w1); s2.set(P.w2); sb.set(P.b); step++;
        draw();
        return step < 400 && Math.hypot(g1, g2, gb) / n > 1e-3;
      },
      onreset() { P.w1 = cfg.w1 != null ? cfg.w1 : -0.5; P.w2 = cfg.w2 != null ? cfg.w2 : 1.5; P.b = cfg.b != null ? cfg.b : 1.5; s1.set(P.w1); s2.set(P.w2); sb.set(P.b); step = 0; draw(); },
    });
    w.controls.append(s1.el, s2.el, sb.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "a", label: L.acc + " =" }, { key: "l", label: L.loss + " =", c: "orange" }, { key: "s", label: L.epoch + " =" }]);
    function draw() {
      s3.f = prob; s3.sample();
      s3.setPoints(pts.map((q) => ({ x: q.x, y: q.y, z: q.c, c: q.c ? "red" : "blue", r: 4.5 })));
      h2.clear();
      h2.heat(prob, { cmap: "diverging", z: [0, 1], res: 4, alpha: 0.75 });
      h2.contours(prob, [0.1, 0.5, 0.9], { style: (lv) => ({ c: "ink", w: lv === 0.5 ? 2.2 : 1, opacity: lv === 0.5 ? 0.9 : 0.45, dash: lv === 0.5 ? null : "4 4" }) });
      pts.forEach((q) => h2.dot(q.x, q.y, { c: q.c ? "red" : "blue", r: 4 }));
      const a = Math.hypot(P.w1, P.w2);
      if (a > 1e-6) h2.arrow(-P.b * P.w1 / (a * a), -P.b * P.w2 / (a * a), -P.b * P.w1 / (a * a) + P.w1 / a * 1.2, -P.b * P.w2 / (a * a) + P.w2 / a * 1.2, { c: "ink", w: 1.8 });
      let acc = 0, loss = 0;
      pts.forEach((q) => { const z = P.w1 * q.x + P.w2 * q.y + P.b, pr = sig(z); acc += (pr >= 0.5 ? 1 : 0) === q.c ? 1 : 0; loss += Math.max(0, z) - z * q.c + Math.log1p(Math.exp(-Math.abs(z))); });
      ro.set("a", Math.round((100 * acc) / pts.length) + "%"); ro.set("l", FV.fmt(loss / pts.length, 3)); ro.set("s", String(step));
      h2.legend([{ label: L.class0, c: "blue", dot: true }, { label: L.class1, c: "red", dot: true }, { label: L.boundary, c: "ink" }]);
    }
    h2.onresize = draw; draw();
  });

  // 6. Saturation: how much of the input mass lands where σ′ is almost zero.
  FV.widget("sigmoid-saturation", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-12, 12], y: [0, 0.3], xLabel: "z", yLabel: "σ′(z)", aspect: 0.45 });
    const ss = FV.ui.slider({ label: L.spread, min: 0.2, max: 8, step: 0.1, value: cfg.s || 1, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    const sm = FV.ui.slider({ label: L.mean, min: -6, max: 6, step: 0.1, value: 0, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    w.controls.append(ss.el, sm.el);
    const ro = FV.ui.readout(w.readout, [{ key: "a", label: L.avg + " =", c: "orange" }, { key: "d", label: L.dead + " =" }]);
    function draw() {
      const s = ss.value, m = sm.value;
      const dens = (z) => Math.exp(-0.5 * ((z - m) / s) ** 2) / (s * Math.sqrt(2 * Math.PI));
      const peak = dens(m), k = 0.25 / Math.max(peak, 0.25);
      p.clear();
      p.area((z) => dens(z) * k, null, { c: "blue", fillOpacity: 0.16 });
      p.fn((z) => dens(z) * k, { c: "blue", w: 1.4 });
      p.area(dsig, null, { c: "orange", fillOpacity: 0.12 });
      p.fn(dsig, { c: "orange", w: 2.4 });
      p.vline(-4.6, { c: "faint" }); p.vline(4.6, { c: "faint" });
      // expectation by the trapezoid rule over ±8s
      let e = 0, dead = 0; const N = 2000, a = m - 8 * s, b = m + 8 * s, hstep = (b - a) / N;
      for (let i = 0; i <= N; i++) { const z = a + i * hstep, wgt = (i === 0 || i === N ? 0.5 : 1) * hstep * dens(z); e += wgt * dsig(z); if (dsig(z) < 0.01) dead += wgt; }
      ro.set("a", FV.fmt(e, 4)); ro.set("d", Math.round(dead * 100) + "%");
      p.legend([{ label: "σ′(z)", c: "orange" }, { label: L.density + " N(μ, s²)", c: "blue", box: true }, { label: "|z| = 4,6".replace(",", FV.lang === "en" ? "." : ","), c: "faint", dash: true }]);
    }
    p.onresize = draw; draw();
  });

  // 7. Vanishing gradients: gradient size per layer in a deep random network.
  FV.widget("sigmoid-vanishing", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0.3, 20.7], y: [1e-12, 10], yType: "log", xLabel: L.layer, yLabel: L.grad, aspect: 0.45 });
    const act = FV.ui.seg({ value: "sigmoid", options: [{ value: "sigmoid", label: "sigmoid" }, { value: "tanh", label: "tanh" }, { value: "relu", label: "ReLU" }], onchange: draw });
    const sd = FV.ui.slider({ label: L.depth, min: 2, max: 20, step: 1, value: cfg.depth || 10, fmt: (v) => String(v), oninput: draw });
    w.controls.append(act.el, sd.el);
    const ro = FV.ui.readout(w.readout, [{ key: "r", label: L.first + " =", c: "orange" }]);
    const n = 64;
    function run(kind, depth) {
      const r = FV.rng(11);
      const f = { sigmoid: sig, tanh: Math.tanh, relu: (z) => Math.max(0, z) }[kind];
      const df = { sigmoid: dsig, tanh: (z) => 1 - Math.tanh(z) ** 2, relu: (z) => (z > 0 ? 1 : 0) }[kind];
      const std = kind === "relu" ? Math.sqrt(2 / n) : Math.sqrt(1 / n);
      let h = Array.from({ length: n }, () => r.normal());
      const Ws = [], Zs = [];
      for (let l = 0; l < depth; l++) {
        const W = Array.from({ length: n }, () => Array.from({ length: n }, () => r.normal() * std));
        const z = W.map((row) => row.reduce((s, v, j) => s + v * h[j], 0));
        Ws.push(W); Zs.push(z); h = z.map(f);
      }
      let g = Array.from({ length: n }, () => 1 / Math.sqrt(n));
      const norms = new Array(depth);
      for (let l = depth - 1; l >= 0; l--) {
        norms[l] = Math.hypot(...g);
        const gz = g.map((v, i) => v * df(Zs[l][i]));
        g = Array.from({ length: n }, (_, j) => Ws[l].reduce((s, row, i) => s + row[j] * gz[i], 0));
      }
      return norms;
    }
    const cache = {};
    function draw() {
      const depth = sd.value, kind = act.value, key = kind + depth;
      const norms = cache[key] || (cache[key] = run(kind, depth));
      p.setDomain([0.3, depth + 0.7]);
      p.clear();
      norms.forEach((v, i) => p.rect(i + 1 - 0.35, 1e-12, i + 1 + 0.35, Math.max(v, 1e-12), { c: kind === "sigmoid" ? "blue" : kind === "tanh" ? "teal" : "violet", opacity: 0.85 }));
      p.fn((x) => Math.pow(0.25, depth - x) * norms[depth - 1], { c: "orange", w: 1.6, dash: true, from: 1, to: depth });
      ro.set("r", FV.num(norms[0] / norms[depth - 1], 2));
      p.legend([{ label: L.grad + " (" + act.value + ")", c: kind === "sigmoid" ? "blue" : kind === "tanh" ? "teal" : "violet", box: true }, { label: "0,25ᴸ⁻ˡ".replace(",", FV.lang === "en" ? "." : ","), c: "orange", dash: true }]);
    }
    p.onresize = draw; draw();
  });
})();
