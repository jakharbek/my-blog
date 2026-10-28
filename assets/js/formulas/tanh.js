/* Widgets of the formula page "Tanh". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      x: "x", tangent: "касательная", asym: "асимптоты ±1", slope: "наклон", cmp: "Сравнить с сигмоидой σ(x)",
      ptx: "Точка $x_0$", step: "Сборка из σ: шаг $t$", sc: "sinh и cosh: tanh — их отношение", fromSig: "Из сигмоиды за три шага",
      target: "цель: tanh x", cur: "текущая кривая", stage: "сейчас",
      order: "Порядок", approx: "приближение", err: "ошибка",
      sigIn: "входы σ(z) ∈ (0; 1)", tanhIn: "входы tanh(z) ∈ (−1; 1)", path: "путь SGD", opt: "оптимум w*", start: "старт", cone: "куда может шагнуть SGD",
      dist: "‖w − w*‖", it: "шаг",
      act: "Активация", gain: "Масштаб весов $g$", layer: "слой", mean: "среднее", std: "ст. откл.", sat: "насыщено", hist: "распределение активаций", lastL: "посл. слой:",
      mode: "Сеть", one: "1 нейрон", two: "2 нейрона", four: "4 + выход", k: "Крутизна $k$", hidden: "скрытых нейронов", surf: "f(x₁, x₂)", top: "вид сверху", lines: "границы скрытых нейронов", zero: "уровень f = 0",
      units: "Нейронов", data: "данные", truth: "истинная функция", model: "сеть", unit: "вклад нейрона", loss: "MSE", lossT: "MSE по шагам",
      wrec: "Рекуррентный вес $w$", state: "состояние hₜ", input: "вход xₜ", grad: "|∂h₃₀/∂hₜ|", gfirst: "|∂h₃₀/∂h₀|", meanh: "среднее |hₜ|", time: "t",
    },
    en: {
      x: "x", tangent: "tangent", asym: "asymptotes ±1", slope: "slope", cmp: "Compare with the sigmoid σ(x)",
      ptx: "Point $x_0$", step: "Building from σ: step $t$", sc: "sinh and cosh: tanh is their ratio", fromSig: "From the sigmoid in three steps",
      target: "target: tanh x", cur: "current curve", stage: "now",
      order: "Order", approx: "approximation", err: "error",
      sigIn: "inputs σ(z) ∈ (0, 1)", tanhIn: "inputs tanh(z) ∈ (−1, 1)", path: "SGD path", opt: "optimum w*", start: "start", cone: "where SGD can step",
      dist: "‖w − w*‖", it: "step",
      act: "Activation", gain: "Weight scale $g$", layer: "layer", mean: "mean", std: "std", sat: "saturated", hist: "distribution of activations", lastL: "last layer:",
      mode: "Network", one: "1 neuron", two: "2 neurons", four: "4 + output", k: "Steepness $k$", hidden: "hidden neurons", surf: "f(x₁, x₂)", top: "view from above", lines: "hidden neuron boundaries", zero: "level f = 0",
      units: "Neurons", data: "data", truth: "true function", model: "network", unit: "one neuron’s share", loss: "MSE", lossT: "MSE over steps",
      wrec: "Recurrent weight $w$", state: "state hₜ", input: "input xₜ", grad: "|∂h₃₀/∂hₜ|", gfirst: "|∂h₃₀/∂h₀|", meanh: "mean |hₜ|", time: "t",
    },
    uz: {
      x: "x", tangent: "urinma", asym: "asimptotalar ±1", slope: "qiyalik", cmp: "Sigmoida σ(x) bilan solishtirish",
      ptx: "Nuqta $x_0$", step: "σ dan yig‘ish: qadam $t$", sc: "sinh va cosh: tanh — ularning nisbati", fromSig: "Sigmoidadan uch qadamda",
      target: "maqsad: tanh x", cur: "joriy egri chiziq", stage: "hozir",
      order: "Tartib", approx: "yaqinlashish", err: "xato",
      sigIn: "kirishlar σ(z) ∈ (0; 1)", tanhIn: "kirishlar tanh(z) ∈ (−1; 1)", path: "SGD yo‘li", opt: "optimum w*", start: "start", cone: "SGD qadam qo‘ya oladigan yo‘nalishlar",
      dist: "‖w − w*‖", it: "qadam",
      act: "Aktivatsiya", gain: "Vaznlar masshtabi $g$", layer: "qatlam", mean: "o‘rtacha", std: "st. og‘ish", sat: "to‘yingan", hist: "aktivatsiyalar taqsimoti", lastL: "oxirgi qatlam:",
      mode: "Tarmoq", one: "1 neyron", two: "2 neyron", four: "4 + chiqish", k: "Tiklik $k$", hidden: "yashirin neyronlar", surf: "f(x₁, x₂)", top: "yuqoridan ko‘rinish", lines: "yashirin neyronlar chegaralari", zero: "f = 0 sathi",
      units: "Neyronlar", data: "ma’lumotlar", truth: "haqiqiy funksiya", model: "tarmoq", unit: "bitta neyron hissasi", loss: "MSE", lossT: "qadamlar bo‘yicha MSE",
      wrec: "Rekurrent vazn $w$", state: "holat hₜ", input: "kirish xₜ", grad: "|∂h₃₀/∂hₜ|", gfirst: "|∂h₃₀/∂h₀|", meanh: "o‘rtacha |hₜ|", time: "t",
    },
  }[FV.lang] || {};
  const EN = FV.lang === "en";
  const dec = (s) => (EN ? s : s.replace(/(\d)\.(\d)/g, "$1,$2"));
  const th = Math.tanh;
  const dth = (x) => { const t = Math.tanh(x); return 1 - t * t; };
  const sig = FV.sigmoid;
  const dsig = (x) => { const s = sig(x); return s * (1 - s); };

  // 1. The curve, its tangent, the derivative below, and the sigmoid for comparison.
  FV.widget("tanh-explorer", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-5, 5], y: [-1.3, 1.3], xLabel: L.x, yLabel: "tanh x", aspect: 0.5 });
    const d = new FV.Plot(w.stage, { x: [-5, 5], y: [-0.06, 1.14], xLabel: L.x, yLabel: "tanh′ x", aspect: 0.28, minHeight: 170, maxHeight: 230 });
    const cmp = FV.ui.check({ label: L.cmp, checked: cfg.compare !== false, onchange: () => draw() });
    w.controls.append(cmp.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "t", label: "tanh x =", c: "blue" }, { key: "d", label: "tanh′ x = 1 − tanh²x =", c: "orange" }, { key: "s", label: "σ′(x) =" }]);
    let x0 = cfg.x != null ? cfg.x : 1;
    const h = p.handle(x0, th(x0), { c: "blue", onDrag: (x) => { x0 = x; return [x, th(x)]; }, onChange: () => draw() });
    function draw() {
      const k = dth(x0), y0 = th(x0);
      p.clear();
      p.hline(1, { c: "blue", dash: false, w: 1.2, opacity: 0.5 }); p.hline(-1, { c: "blue", dash: false, w: 1.2, opacity: 0.5 });
      p.vline(0, {});
      if (cmp.value) p.fn(sig, { c: "guide", w: 1.8, dash: "6 5" });
      p.line(x0 - 2, y0 - 2 * k, x0 + 2, y0 + 2 * k, { c: "orange", w: 1.8 });
      p.fn(th, { c: "ink", w: 2.4 });
      p.line(x0, 0, x0, y0, { c: "guide", w: 1, dash: "3 3" });
      p.dot(0, 0, { hollow: true, r: 4 });
      h.set(x0, y0);
      d.clear();
      d.hline(1, { c: "orange", opacity: 0.6 });
      if (cmp.value) { d.hline(0.25, { c: "guide", opacity: 0.8 }); d.fn(dsig, { c: "guide", w: 1.8, dash: "6 5" }); }
      d.area(dth, null, { c: "orange", fillOpacity: 0.12 });
      d.fn(dth, { c: "orange", w: 2.2 });
      d.line(x0, 0, x0, k, { c: "orange", w: 1, dash: "3 3" });
      d.dot(x0, k, { c: "orange" });
      d.text(0.3, 1.06, dec("max = 1"), { c: "orange" });
      if (cmp.value) d.text(-4.9, 0.31, dec("max σ′ = 0.25"));
      ro.set("x", FV.fmt(x0, 2)); ro.set("t", FV.fmt(y0, 4)); ro.set("d", FV.fmt(k, 4)); ro.set("s", FV.fmt(dsig(x0), 4));
      const lg = [{ label: "tanh x", c: "ink" }, { label: L.tangent + " (" + L.slope + " = tanh′)", c: "orange" }, { label: L.asym, c: "blue" }];
      if (cmp.value) lg.push({ label: "σ(x)", c: "guide", dash: true });
      p.legend(lg);
      d.legend([{ label: "tanh′ x", c: "orange" }].concat(cmp.value ? [{ label: "σ′(x)", c: "guide", dash: true }] : []));
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 2. Two constructions: sinh / cosh, and 2σ(2x) − 1 assembled from the sigmoid.
  FV.widget("tanh-construction", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-2.5, 2.5], y: [-3.2, 3.2], xLabel: L.x, aspect: 0.9, title: L.sc });
    const b = new FV.Plot(FV.col(w.stage), { x: [-4, 4], y: [-1.25, 2.25], xLabel: L.x, aspect: 0.9, title: L.fromSig });
    const sx = FV.ui.slider({ label: L.ptx, min: -2.5, max: 2.5, step: 0.05, value: cfg.x != null ? cfg.x : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const st = FV.ui.slider({ label: L.step, min: 0, max: 3, step: 0.01, value: cfg.t != null ? cfg.t : 3, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const player = FV.ui.player({
      interval: 40,
      onstep() { let t = st.value; if (t >= 3) t = 0; t = Math.min(3, t + 0.03); st.set(t); draw(); return t < 3; },
      onreset() { st.set(0); draw(); },
    });
    w.controls.append(sx.el, st.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: "sinh x₀ =", c: "teal" }, { key: "c", label: "cosh x₀ =", c: "violet" }, { key: "t", label: "tanh x₀ = sinh/cosh =", c: "blue" }, { key: "f", label: L.stage + ":" }]);
    const sh = (x) => (Math.exp(x) - Math.exp(-x)) / 2, ch = (x) => (Math.exp(x) + Math.exp(-x)) / 2;
    function morph(t) {
      if (t <= 1) return { f: (x) => sig((1 + t) * x), s: t < 0.005 ? "σ(x)" : t > 0.995 ? "σ(2x)" : "σ(" + FV.fmt(1 + t, 2) + "x)" };
      if (t <= 2) { const k = t; return { f: (x) => k * sig(2 * x), s: (t > 1.995 ? "2" : FV.fmt(k, 2)) + "·σ(2x)" }; }
      const c = t - 2; return { f: (x) => 2 * sig(2 * x) - c, s: "2σ(2x) − " + (c > 0.995 ? "1 = tanh x" : FV.fmt(c, 2)) };
    }
    function draw() {
      const x0 = sx.value;
      a.clear(); a.vline(0, {});
      a.fn((x) => Math.exp(x) / 2, { c: "faint", w: 1.4, dash: "5 4" });
      a.fn((x) => Math.exp(-x) / 2, { c: "faint", w: 1.4, dash: "5 4" });
      a.fn(ch, { c: "violet", w: 2 }); a.fn(sh, { c: "teal", w: 2 }); a.fn(th, { c: "blue", w: 2.6 });
      a.line(x0, -3.2, x0, 3.2, { c: "guide", w: 1, dash: "3 3" });
      a.dot(x0, sh(x0), { c: "teal", r: 4 }); a.dot(x0, ch(x0), { c: "violet", r: 4 }); a.dot(x0, th(x0), { c: "blue", r: 5 });
      a.legend([{ label: "sinh x", c: "teal" }, { label: "cosh x", c: "violet" }, { label: "tanh x", c: "blue" }, { label: "eˣ/2, e⁻ˣ/2", c: "faint", dash: true }]);
      const m = morph(st.value);
      b.clear(); b.hline(0, {}); b.vline(0, {}); b.hline(1, { c: "guide", dash: false, opacity: 0.6 }); b.hline(-1, { c: "guide", dash: false, opacity: 0.6 });
      b.fn(th, { c: "faint", w: 5, opacity: 0.35 });
      b.fn(sig, { c: "guide", w: 1.6, dash: "6 5" });
      b.fn(m.f, { c: "blue", w: 2.6 });
      b.legend([{ label: L.cur, c: "blue" }, { label: "σ(x)", c: "guide", dash: true }, { label: L.target, c: "faint" }]);
      ro.set("s", FV.fmt(sh(x0), 3)); ro.set("c", FV.fmt(ch(x0), 3)); ro.set("t", FV.fmt(th(x0), 4)); ro.set("f", m.s);
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 3. Taylor polynomials around zero; the series converges only for |x| < π/2.
  FV.widget("tanh-taylor", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-3, 3], y: [-2, 2], xLabel: L.x, yLabel: "y", aspect: 0.5 });
    const terms = [(x) => x, (x) => -(x ** 3) / 3, (x) => (2 * x ** 5) / 15, (x) => (-17 * x ** 7) / 315, (x) => (62 * x ** 9) / 2835];
    const ord = FV.ui.seg({ label: L.order, value: cfg.order || 3, options: [1, 3, 5, 7, 9].map((v) => ({ value: v, label: String(v) })), onchange: draw });
    const sx = FV.ui.slider({ label: "x", min: -3, max: 3, step: 0.05, value: cfg.x != null ? cfg.x : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(ord.el, sx.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: "tanh x =" }, { key: "t", label: L.approx + " =", c: "orange" }, { key: "e", label: L.err + " =" }]);
    function T(x) { let s = 0; for (let i = 0; i < (ord.value + 1) / 2; i++) s += terms[i](x); return s; }
    function draw() {
      const r = Math.PI / 2;
      p.clear(); p.hline(1, { dash: false, c: "guide" }); p.hline(-1, { dash: false, c: "guide" });
      p.rect(-r, -2, r, 2, { c: "teal", opacity: 0.07 });
      p.vline(-r, { c: "teal" }); p.vline(r, { c: "teal" });
      p.text(r, 1.82, "π/2", { c: "teal", dx: 5 }); p.text(-r, 1.82, "−π/2", { c: "teal", dx: -5, anchor: "end" });
      p.fn(th, { c: "ink", w: 2.4 });
      p.fn(T, { c: "orange", w: 2.2 });
      const x = sx.value;
      p.dot(x, th(x), { c: "ink", r: 4 }); if (Math.abs(T(x)) < 2) p.dot(x, T(x), { c: "orange", r: 4 });
      ro.set("s", FV.fmt(th(x), 4)); ro.set("t", FV.fmt(T(x), 4)); ro.set("e", FV.num(Math.abs(T(x) - th(x)), 3));
      p.legend([{ label: "tanh x", c: "ink" }, { label: L.approx + " " + ord.value, c: "orange" }, { label: "|x| < π/2", c: "teal", box: true }]);
    }
    p.onresize = draw; draw();
  });

  // 4. Why zero-centred activations help: SGD on the next layer's weights, sigmoid inputs vs tanh inputs.
  FV.widget("tanh-zigzag", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const dom = [-1.6, 1.6];
    const r = FV.rng(5), Z = [];
    for (let i = 0; i < 100; i++) Z.push([r.normal(), r.normal()]);
    const WS = [1, -1], W0 = [-1, 1], eta = 0.5, MAX = 400;
    function make(f, title) {
      const A = Z.map((z) => [f(z[0]), f(z[1])]);
      const T = A.map((a) => WS[0] * a[0] + WS[1] * a[1]);
      let h11 = 0, h12 = 0, h22 = 0;
      A.forEach((a) => { h11 += a[0] * a[0]; h12 += a[0] * a[1]; h22 += a[1] * a[1]; });
      h11 /= A.length; h12 /= A.length; h22 /= A.length;
      const loss = (u, v) => { const a = u - WS[0], b = v - WS[1]; return 0.5 * (h11 * a * a + 2 * h12 * a * b + h22 * b * b); };
      const plot = new FV.Plot(FV.col(w.stage), { x: dom, y: dom, xLabel: "w₁", yLabel: "w₂", equal: true, title });
      return { A, T, loss, plot, path: [W0.slice()] };
    }
    const S = make(sig, L.sigIn), H = make(th, L.tanhIn);
    let k = 0;
    const K0 = cfg.steps || 0;
    function stepOne(m) {
      const i = k % m.A.length, a = m.A[i], q = m.path[m.path.length - 1];
      const e = q[0] * a[0] + q[1] * a[1] - m.T[i];
      m.path.push([q[0] - eta * e * a[0], q[1] - eta * e * a[1]]);
    }
    const player = FV.ui.player({
      interval: 50,
      onstep() { for (let j = 0; j < 2 && k < MAX; j++) { stepOne(S); stepOne(H); k++; } draw(); return k < MAX; },
      onreset() { k = 0; S.path = [W0.slice()]; H.path = [W0.slice()]; draw(); },
    });
    while (k < K0) { stepOne(S); stepOne(H); k++; }
    w.controls.append(player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "k", label: L.it + " =" }, { key: "s", label: L.dist + " (σ) =", c: "blue" }, { key: "t", label: L.dist + " (tanh) =", c: "blue" }]);
    function panel(m, cone) {
      const p = m.plot, L0 = m.loss(W0[0], W0[1]);
      p.clear();
      p.contours(m.loss, [0.01, 0.04, 0.12, 0.3, 0.6, 1, 1.6].map((v) => v * L0), { c: "ink", w: 1, opacity: 0.35 });
      const q = m.path[m.path.length - 1];
      if (cone) {
        p.rect(q[0], q[1], q[0] + 0.45, q[1] + 0.45, { c: "teal", opacity: 0.16 });
        p.rect(q[0] - 0.45, q[1] - 0.45, q[0], q[1], { c: "teal", opacity: 0.16 });
      }
      p.path(m.path, { c: "blue", w: 1.6 });
      p.dot(W0[0], W0[1], { c: "ink", r: 4, hollow: true });
      p.dot(WS[0], WS[1], { c: "orange", r: 5 });
      p.dot(q[0], q[1], { c: "blue", r: 4.5 });
      const lg = [{ label: L.path, c: "blue" }, { label: L.opt, c: "orange", dot: true }];
      if (cone) lg.push({ label: L.cone, c: "teal", box: true });
      p.legend(lg);
      return Math.hypot(q[0] - WS[0], q[1] - WS[1]);
    }
    function draw() {
      const ds = panel(S, true), dt = panel(H, false);
      ro.set("k", String(k)); ro.set("s", FV.fmt(ds, 3)); ro.set("t", FV.fmt(dt, 3));
    }
    S.plot.onresize = draw; H.plot.onresize = draw; draw();
  });

  // 5. Distribution of activations through the layers of a random deep network.
  FV.widget("tanh-layers", (el, cfg) => {
    const w = FV.shell(el, {});
    const n = 100, B = 20, D = 10;
    const p = new FV.Plot(w.stage, { x: [-1.05, 1.05], y: [0.55, D + 1.4], xLabel: L.hist, yLabel: L.layer, aspect: 0.62, minHeight: 380, maxHeight: 520, yTicks: Array.from({ length: D }, (_, i) => i + 1) });
    const act = FV.ui.seg({ label: L.act, value: cfg.act || "tanh", options: [{ value: "tanh", label: "tanh" }, { value: "sigmoid", label: "sigmoid" }], onchange: draw });
    const gs = FV.ui.seg({ label: L.gain, value: cfg.g || 1, options: [{ value: 0.5, label: dec("0.5") }, { value: 1, label: "1" }, { value: 5 / 3, label: "5/3" }, { value: 3, label: "3" }], onchange: draw });
    w.controls.append(act.el, gs.el);
    const ro = FV.ui.readout(w.readout, [{ key: "l", label: L.lastL }, { key: "m", label: L.mean + " =", c: "orange" }, { key: "s", label: L.std + " =" }, { key: "q", label: L.sat + " =" }]);
    ro.set("l", "");
    // inputs and weights are drawn once, the same for every activation and scale
    const r = FV.rng(3);
    const X = Array.from({ length: B }, () => Array.from({ length: n }, () => r.normal()));
    const Ws = Array.from({ length: D }, () => Array.from({ length: n }, () => Array.from({ length: n }, () => r.normal())));
    const cache = {};
    function run(kind, g) {
      const key = kind + g;
      if (cache[key]) return cache[key];
      const f = kind === "tanh" ? th : sig, c = g / Math.sqrt(n);
      let h = X;
      const out = [];
      for (let l = 0; l < D; l++) {
        const W = Ws[l];
        h = h.map((row) => W.map((wr) => { let s = 0; for (let j = 0; j < n; j++) s += row[j] * wr[j]; return f(s * c); }));
        const all = [].concat(...h);
        const m = all.reduce((s, v) => s + v, 0) / all.length;
        const sd = Math.sqrt(all.reduce((s, v) => s + (v - m) * (v - m), 0) / all.length);
        const sat = all.filter((v) => (kind === "tanh" ? Math.abs(v) > 0.95 : v < 0.025 || v > 0.975)).length / all.length;
        const bins = new Array(42).fill(0);
        all.forEach((v) => { bins[FV.clamp(Math.floor(((v + 1.05) / 2.1) * 42), 0, 41)]++; });
        out.push({ m, sd, sat, bins });
      }
      return (cache[key] = out);
    }
    function draw() {
      const res = run(act.value, gs.value);
      p.clear(); p.vline(0, {});
      if (act.value === "sigmoid") p.vline(0.5, { c: "orange", opacity: 0.5 });
      for (let l = D - 1; l >= 0; l--) {
        const o = res[l], mx = Math.max(...o.bins), base = l + 1, pts = [[-1.05, base]];
        o.bins.forEach((c, i) => { const x0 = -1.05 + (i * 2.1) / 42, x1 = x0 + 2.1 / 42, y = base + (0.92 * c) / mx; pts.push([x0, y], [x1, y]); });
        pts.push([1.05, base]);
        p.path(pts, { c: "blue", fill: true, fillOpacity: 0.28, w: 1.3, close: true });
        p.dot(o.m, base, { c: "orange", r: 3.5 });
      }
      const last = res[D - 1];
      ro.set("m", FV.fmt(last.m, 3)); ro.set("s", FV.fmt(last.sd, 3)); ro.set("q", Math.round(last.sat * 100) + "%");
      p.legend([{ label: L.hist + " (" + act.value + ")", c: "blue", box: true }, { label: L.mean, c: "orange", dot: true }]);
    }
    p.onresize = draw; draw();
  });

  // 6. A tiny tanh network on the plane: one fold, a ridge, a bump.
  FV.widget("tanh-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const P = { mode: cfg.mode || "four", k: cfg.k || 2 };
    const nets = {
      one: { lines: [[0.8, 0.6, 0]], f: (x, y, k) => th(k * (0.8 * x + 0.6 * y)) },
      two: { lines: [[1, 0, 1], [1, 0, -1]], f: (x, y, k) => th(k * (x + 1)) - th(k * (x - 1)) - 1 },
      four: {
        lines: [[1, 0, 1], [1, 0, -1], [0, 1, 1], [0, 1, -1]],
        f: (x, y, k) => th(2 * (th(k * (x + 1)) - th(k * (x - 1)) + th(k * (y + 1)) - th(k * (y - 1)) - 3)),
      },
    };
    const F = (x, y) => FV.clamp(nets[P.mode].f(x, y, P.k), -1, 1);
    const s3 = new FV.Surface(FV.col(w.stage), { f: F, x: [-3, 3], y: [-3, 3], z: [-1, 1], n: 40, labels: { x: "x₁", y: "x₂", z: "f" }, azimuth: -0.12, elevation: 0.5, aspect: 0.85, cmap: "diverging", title: L.surf });
    const h2 = new FV.Plot(FV.col(w.stage), { x: [-3, 3], y: [-3, 3], xLabel: "x₁", yLabel: "x₂", equal: true, title: L.top });
    const mode = FV.ui.seg({ label: L.mode, value: P.mode, options: [{ value: "one", label: L.one }, { value: "two", label: L.two }, { value: "four", label: L.four }], onchange: (v) => { P.mode = v; draw(); } });
    const sk = FV.ui.slider({ label: L.k, min: 0.5, max: 5, step: 0.1, value: P.k, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { P.k = v; draw(); } });
    w.controls.append(mode.el, sk.el);
    const ro = FV.ui.readout(w.readout, [{ key: "n", label: L.hidden + ":" }, { key: "c", label: EN ? "f(0, 0) =" : "f(0; 0) =", c: "blue" }, { key: "o", label: EN ? "f(2.5, 2.5) =" : "f(2,5; 2,5) =" }]);
    function draw() {
      s3.setF(F);
      h2.clear();
      h2.heat(F, { cmap: "diverging", z: [-1, 1], res: 4, alpha: 0.8 });
      nets[P.mode].lines.forEach(([a, b, c]) => {
        if (Math.abs(b) < 1e-9) h2.line(-c / a, -3, -c / a, 3, { c: "ink", w: 1.2, dash: "5 4", opacity: 0.7 });
        else h2.line(-3, (-c + 3 * a) / b, 3, (-c - 3 * a) / b, { c: "ink", w: 1.2, dash: "5 4", opacity: 0.7 });
      });
      h2.contours(F, [0], { c: "ink", w: 2, opacity: 0.9 });
      h2.legend([{ label: L.lines, c: "ink", dash: true }, { label: L.zero, c: "ink" }]);
      ro.set("n", String(nets[P.mode].lines.length)); ro.set("c", FV.fmt(F(0, 0), 3)); ro.set("o", FV.fmt(F(2.5, 2.5), 3));
    }
    h2.onresize = draw; draw();
  });

  // 7. A one-hidden-layer tanh network learns a curve (full-batch Adam).
  FV.widget("tanh-fit", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-3.2, 3.2], y: [-2, 2], xLabel: L.x, yLabel: "y", aspect: 0.5 });
    const q = new FV.Plot(w.stage, { x: [0, 2080], y: [1e-3, 10], yType: "log", xLabel: L.it, yLabel: L.lossT, aspect: 0.26, minHeight: 160, maxHeight: 210 });
    const truth = (x) => 0.8 * Math.sin(2.2 * x) + 0.3 * x;
    const N = 40, rd = FV.rng(4);
    const xs = Array.from({ length: N }, (_, i) => -3 + (6 * i) / (N - 1));
    const ys = xs.map((x) => truth(x) + 0.08 * rd.normal());
    const lr = 0.05, MAX = 2000;
    let H = cfg.h || 5, Pm, M, V, t, hist;
    function init() {
      const r = FV.rng(9);
      const W = Array.from({ length: H }, () => r.normal()), Bb = Array.from({ length: H }, () => r.normal()), Vv = Array.from({ length: H }, () => r.normal() / Math.sqrt(H));
      Pm = W.concat(Bb, Vv, [0]); M = Pm.map(() => 0); V = Pm.map(() => 0); t = 0; hist = [[0, lossAndGrad().L]];
    }
    function net(x) { let s = Pm[3 * H]; for (let k = 0; k < H; k++) s += Pm[2 * H + k] * th(Pm[k] * x + Pm[H + k]); return s; }
    function lossAndGrad() {
      const g = Pm.map(() => 0); let Ls = 0;
      for (let i = 0; i < N; i++) {
        const x = xs[i], a = [], z = [];
        let yh = Pm[3 * H];
        for (let k = 0; k < H; k++) { z[k] = Pm[k] * x + Pm[H + k]; a[k] = th(z[k]); yh += Pm[2 * H + k] * a[k]; }
        const e = yh - ys[i]; Ls += e * e;
        for (let k = 0; k < H; k++) { g[2 * H + k] += (2 * e * a[k]) / N; const dz = (2 * e * Pm[2 * H + k] * (1 - a[k] * a[k])) / N; g[k] += dz * x; g[H + k] += dz; }
        g[3 * H] += (2 * e) / N;
      }
      return { L: Ls / N, g };
    }
    function step() {
      const { g } = lossAndGrad();
      t++;
      for (let i = 0; i < Pm.length; i++) {
        M[i] = 0.9 * M[i] + 0.1 * g[i]; V[i] = 0.999 * V[i] + 0.001 * g[i] * g[i];
        Pm[i] -= (lr * (M[i] / (1 - Math.pow(0.9, t)))) / (Math.sqrt(V[i] / (1 - Math.pow(0.999, t))) + 1e-8);
      }
    }
    const hs = FV.ui.seg({ label: L.units, value: H, options: [3, 5, 8].map((v) => ({ value: v, label: String(v) })), onchange: (v) => { H = v; player.stop(); init(); draw(); } });
    const player = FV.ui.player({
      interval: 50,
      onstep() { for (let j = 0; j < 10 && t < MAX; j++) step(); hist.push([t, lossAndGrad().L]); draw(); return t < MAX; },
      onreset() { init(); draw(); },
    });
    w.controls.append(hs.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.it + " =" }, { key: "l", label: L.loss + " =", c: "blue" }]);
    function draw() {
      p.clear(); p.hline(0, {});
      for (let k = 0; k < H; k++) { const wk = Pm[k], bk = Pm[H + k], vk = Pm[2 * H + k]; p.fn((x) => vk * th(wk * x + bk), { c: "teal", w: 1.3, opacity: 0.75 }); }
      p.fn(truth, { c: "guide", w: 1.6, dash: "6 5" });
      xs.forEach((x, i) => p.dot(x, ys[i], { c: "faint", r: 3.2 }));
      p.fn(net, { c: "blue", w: 2.6 });
      p.legend([{ label: L.model, c: "blue" }, { label: L.unit + " vₖ·tanh(wₖx + bₖ)", c: "teal" }, { label: L.truth, c: "guide", dash: true }, { label: L.data, c: "faint", dot: true }]);
      q.clear(); q.path(hist.map(([s, v]) => [s, Math.max(v, 1e-3)]), { c: "blue", w: 2 });
      const Lc = hist[hist.length - 1][1];
      q.dot(t, Math.max(Lc, 1e-3), { c: "blue", r: 4 });
      ro.set("t", String(t)); ro.set("l", FV.fmt(Lc, 4));
    }
    init();
    p.onresize = draw; q.onresize = draw; draw();
  });

  // 8. A scalar tanh RNN: the state stays bounded, but the gradient through time fades.
  FV.widget("tanh-rnn", (el, cfg) => {
    const w = FV.shell(el, {});
    const T = 30;
    const p = new FV.Plot(w.stage, { x: [-0.5, T + 0.5], y: [-1.15, 1.15], xLabel: L.time, yLabel: "hₜ", aspect: 0.36, minHeight: 200 });
    const sup = (e) => (e === 0 ? "1" : "10" + String(e).replace("-", "⁻").replace(/\d/g, (c) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[c]));
    const q = new FV.Plot(w.stage, { x: [-0.5, T + 0.5], y: [1e-42, 10], yType: "log", xLabel: L.time, yLabel: L.grad, aspect: 0.36, minHeight: 200 });
    const sw = FV.ui.slider({ label: L.wrec, min: 0, max: 4, step: 0.05, value: cfg.w != null ? cfg.w : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sw.el);
    const ro = FV.ui.readout(w.readout, [{ key: "g", label: L.gfirst + " =", c: "orange" }, { key: "m", label: L.meanh + " =", c: "blue" }]);
    const r = FV.rng(2), xs = Array.from({ length: T }, () => 0.2 * r.normal());
    function draw() {
      const wr = sw.value, h = [0];
      for (let t = 0; t < T; t++) h.push(th(wr * h[t] + xs[t]));
      const g = new Array(T + 1); g[T] = 1;
      for (let t = T - 1; t >= 0; t--) g[t] = g[t + 1] * Math.abs(wr * (1 - h[t + 1] * h[t + 1]));
      p.clear(); p.hline(1, { c: "guide", dash: false }); p.hline(-1, { c: "guide", dash: false });
      xs.forEach((v, t) => p.rect(t + 1 - 0.3, 0, t + 1 + 0.3, v, { c: "faint", opacity: 0.45 }));
      p.path(h.map((v, t) => [t, v]), { c: "blue", w: 2 });
      h.forEach((v, t) => p.dot(t, v, { c: "blue", r: 3 }));
      p.legend([{ label: L.state, c: "blue" }, { label: L.input, c: "faint", box: true }]);
      // the vertical range follows the smallest gradient: from 10⁻⁶ down to 10⁻⁴²
      const e0 = FV.clamp(Math.floor(Math.log10(Math.max(Math.min(...g), 1e-300))) - 1, -42, -6);
      const stepE = e0 >= -12 ? 2 : e0 >= -24 ? 5 : 10, ticks = [];
      for (let e = 0; e >= e0; e -= stepE) ticks.unshift({ v: Math.pow(10, e), label: sup(e) });
      q.o.yTicks = ticks; q.setDomain(null, [Math.pow(10, e0), 10]);
      q.clear();
      g.forEach((v, t) => q.rect(t - 0.32, Math.pow(10, e0), t + 0.32, Math.max(v, Math.pow(10, e0)), { c: "orange", opacity: 0.85 }));
      q.legend([{ label: L.grad, c: "orange", box: true }]);
      ro.set("g", FV.num(g[0], 2)); ro.set("m", FV.fmt(h.slice(1).reduce((s, v) => s + Math.abs(v), 0) / T, 3));
    }
    p.onresize = draw; q.onresize = draw; draw();
  });
})();
