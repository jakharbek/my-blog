/* Widgets of the formula page "Softmax". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      logits: "Логиты $z$", probs: "Вероятности $s=\\mathrm{softmax}(z/T)$", T: "Температура $T$", up: "+1 ко всем логитам", down: "−1 ко всем", reset: "Сбросить",
      sumexp: "Σ e^(z/T) =", uniform: "равномерное 1/K", z2: "$z_2$", z3: "$z_3$", z1: "$z_1$", third: "Есть третий класс", m: "m =",
      s1sig: "s₁ = σ(z₁ − m)", center: "z₁ = m (здесь s₁ = 0,5)", simplex: "Точка s в симплексе", bars: "Те же вероятности столбиками",
      pathT: "путь при изменении T", pathZ: "путь при изменении z₁", ent: "энтропия H(s) =", zc: "логиты z − z̄ =",
      matrix: "Матрица Якоби J = diag(s) − s sᵀ", curves: "Столбец j как функции от zⱼ", col: "Столбец $j$", colsum: "сумма столбца =", trace: "tr J = 1 − Σ s² =", diag: "диагональ sⱼ(1 − sⱼ) =",
      surf: "Поверхность", plane: "Плоскость логитов (z₃ = 0)", regions: "область, где класс k — argmax",
      lseTop: "Гладкий максимум", lseBot: "Его производная — softmax", maxf: "max(x, 0)", bound: "max + T·ln 2", lse: "LSE_T(x, 0) = T·ln(e^(x/T) + 1)", step: "ступенька", deriv: "σ(x/T) = softmax₁",
      gap: "LSE − max =", reg: "Области классов", curve: "Потеря на обучающей выборке", stepN: "шаг", acc: "точность", ce: "CE", cursor: "под курсором s =", class: "класс",
      shiftC: "сдвиг логитов c: z = (2 + c; 1 + c; c)", c: "Сдвиг $c$", stable: "с −max", ok: "верно", nan: "NaN (inf/inf или 0/0)", bad: "неточно (денормализованные числа)",
      r32: "float32, наивно:", r64: "float64, наивно:", rst: "с вычитанием max:", e32: "e^(z₁) во float32 =",
    },
    en: {
      logits: "Logits $z$", probs: "Probabilities $s=\\mathrm{softmax}(z/T)$", T: "Temperature $T$", up: "+1 to every logit", down: "−1 to every logit", reset: "Reset",
      sumexp: "Σ e^(z/T) =", uniform: "uniform 1/K", z2: "$z_2$", z3: "$z_3$", z1: "$z_1$", third: "There is a third class", m: "m =",
      s1sig: "s₁ = σ(z₁ − m)", center: "z₁ = m (here s₁ = 0.5)", simplex: "The point s in the simplex", bars: "The same probabilities as bars",
      pathT: "path as T changes", pathZ: "path as z₁ changes", ent: "entropy H(s) =", zc: "logits z − z̄ =",
      matrix: "Jacobian J = diag(s) − s sᵀ", curves: "Column j as functions of zⱼ", col: "Column $j$", colsum: "column sum =", trace: "tr J = 1 − Σ s² =", diag: "diagonal sⱼ(1 − sⱼ) =",
      surf: "Surface", plane: "The logit plane (z₃ = 0)", regions: "region where class k is the argmax",
      lseTop: "A smooth maximum", lseBot: "Its derivative is softmax", maxf: "max(x, 0)", bound: "max + T·ln 2", lse: "LSE_T(x, 0) = T·ln(e^(x/T) + 1)", step: "step", deriv: "σ(x/T) = softmax₁",
      gap: "LSE − max =", reg: "Class regions", curve: "Loss on the training set", stepN: "step", acc: "accuracy", ce: "CE", cursor: "under the cursor s =", class: "class",
      shiftC: "logit shift c: z = (2 + c, 1 + c, c)", c: "Shift $c$", stable: "with −max", ok: "correct", nan: "NaN (inf/inf or 0/0)", bad: "inaccurate (subnormal numbers)",
      r32: "float32, naive:", r64: "float64, naive:", rst: "max subtracted:", e32: "e^(z₁) in float32 =",
    },
    uz: {
      logits: "Logitlar $z$", probs: "Ehtimolliklar $s=\\mathrm{softmax}(z/T)$", T: "Harorat $T$", up: "Barcha logitlarga +1", down: "Barchasiga −1", reset: "Tiklash",
      sumexp: "Σ e^(z/T) =", uniform: "tekis 1/K", z2: "$z_2$", z3: "$z_3$", z1: "$z_1$", third: "Uchinchi sinf bor", m: "m =",
      s1sig: "s₁ = σ(z₁ − m)", center: "z₁ = m (bu yerda s₁ = 0,5)", simplex: "Simpleksdagi s nuqta", bars: "O‘sha ehtimolliklar ustunlarda",
      pathT: "T o‘zgargandagi yo‘l", pathZ: "z₁ o‘zgargandagi yo‘l", ent: "entropiya H(s) =", zc: "logitlar z − z̄ =",
      matrix: "Yakobi matritsasi J = diag(s) − s sᵀ", curves: "j-ustun zⱼ ning funksiyalari sifatida", col: "Ustun $j$", colsum: "ustun yig‘indisi =", trace: "tr J = 1 − Σ s² =", diag: "diagonal sⱼ(1 − sⱼ) =",
      surf: "Sirt", plane: "Logitlar tekisligi (z₃ = 0)", regions: "k-sinf argmax bo‘lgan soha",
      lseTop: "Silliq maksimum", lseBot: "Uning hosilasi — softmax", maxf: "max(x, 0)", bound: "max + T·ln 2", lse: "LSE_T(x, 0) = T·ln(e^(x/T) + 1)", step: "pog‘ona", deriv: "σ(x/T) = softmax₁",
      gap: "LSE − max =", reg: "Sinflar sohalari", curve: "O‘qitish to‘plamidagi yo‘qotish", stepN: "qadam", acc: "aniqlik", ce: "CE", cursor: "kursor ostida s =", class: "sinf",
      shiftC: "logitlar siljishi c: z = (2 + c; 1 + c; c)", c: "Siljish $c$", stable: "−max bilan", ok: "to‘g‘ri", nan: "NaN (inf/inf yoki 0/0)", bad: "noaniq (subnormal sonlar)",
      r32: "float32, sodda:", r64: "float64, sodda:", rst: "max ayirilgan:", e32: "float32 da e^(z₁) =",
    },
  }[FV.lang] || {};

  const CLS = ["blue", "orange", "teal"];
  const SUB = ["₁", "₂", "₃"];
  const SEP = FV.lang === "en" ? ", " : "; ";
  const sig = FV.sigmoid;
  function softmax(z, T = 1) {
    const m = Math.max(...z), e = z.map((v) => Math.exp((v - m) / T)), s = e.reduce((a, b) => a + b, 0);
    return e.map((v) => v / s);
  }
  function lse(z) { const m = Math.max(...z); return m + Math.log(z.reduce((a, v) => a + Math.exp(v - m), 0)); }
  const argmax = (s) => s.indexOf(Math.max(...s));
  const vec = (s, d = 3) => "(" + s.map((v) => (Number.isNaN(v) ? "NaN" : FV.fmt(v, d))).join(SEP) + ")";
  const entropy = (s) => -s.reduce((a, v) => a + (v > 0 ? v * Math.log(v) : 0), 0);

  // Colours of the series as RGB triples (they follow the theme).
  function rgbOf(name) {
    const c = FV.color(name) || "#888888";
    if (c[0] === "#") { const n = parseInt(c.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
    const m = c.match(/\d+/g) || [136, 136, 136];
    return m.slice(0, 3).map(Number);
  }
  // A raster layer under the plot: f(x, y) → [r, g, b, a] or null (transparent).
  function paint(p, f, res = 3) {
    const w = Math.max(1, Math.round((p.x1 - p.x0) / res)), h = Math.max(1, Math.round((p.y0 - p.y1) / res));
    const cv = document.createElement("canvas"); cv.width = w; cv.height = h;
    const ctx = cv.getContext("2d"), img = ctx.createImageData(w, h);
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const x = p.sx.inv(p.x0 + ((i + 0.5) / w) * (p.x1 - p.x0)), y = p.sy.inv(p.y1 + ((j + 0.5) / h) * (p.y0 - p.y1));
      const c = f(x, y);
      if (!c) continue;
      const k = 4 * (j * w + i);
      img.data[k] = c[0]; img.data[k + 1] = c[1]; img.data[k + 2] = c[2]; img.data[k + 3] = c[3] == null ? 255 : c[3];
    }
    ctx.putImageData(img, 0, 0);
    const im = FV.svg("image", { x: p.x0, y: p.y1, width: p.x1 - p.x0, height: p.y0 - p.y1, preserveAspectRatio: "none", href: cv.toDataURL() });
    p.gMain.insertBefore(im, p.gMain.firstChild);
  }
  // Colour of a point by the winning class; the more confident, the more saturated.
  function regionColour(s, cols, gain = 150) {
    const k = argmax(s), t = Math.max(0, (s[k] - 1 / 3) / (2 / 3));
    const c = cols[k];
    return [c[0], c[1], c[2], Math.round(gain * Math.pow(t, 0.8))];
  }
  const onTheme = (fn) => document.addEventListener("themechange", () => fn());

  // Probability simplex: class 1 at the top, class 2 bottom-left, class 3 bottom-right.
  const H3 = Math.sqrt(3) / 2;
  const VX = [[0.5, H3], [0, 0], [1, 0]];
  const toXY = (s) => [s[0] * VX[0][0] + s[1] * VX[1][0] + s[2] * VX[2][0], s[0] * VX[0][1] + s[1] * VX[1][1] + s[2] * VX[2][1]];
  const toS = (x, y) => { const s1 = y / H3, s3 = x - 0.5 * s1; return [s1, 1 - s1 - s3, s3]; };
  function inside(s, lo) { const t = s.map((v) => Math.max(v, lo)); const k = t.reduce((a, b) => a + b, 0); return t.map((v) => v / k); }
  function simplexFrame(p) {
    p.path([VX[0], VX[1], VX[2]], { c: "ink", w: 1.4, close: true });
    const c = [1 / 3, 1 / 3, 1 / 3], C = toXY(c);
    [[0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]].forEach((m) => { const M = toXY(m); p.line(C[0], C[1], M[0], M[1], { c: "guide", w: 1, dash: "4 4" }); });
    p.dot(C[0], C[1], { hollow: true, r: 3.5, c: "ink" });
    p.text(0.5, H3 + 0.035, "s₁ = 1", { c: "blue", anchor: "middle" });
    p.text(-0.02, -0.075, "s₂ = 1", { c: "orange", anchor: "start" });
    p.text(1.02, -0.075, "s₃ = 1", { c: "teal", anchor: "end" });
  }
  const barTicks = (n) => [1, 2, 3].map((i) => ({ v: i, label: n + SUB[i - 1] }));
  function probBars(b, s, extra) {
    b.clear();
    b.hline(1 / 3, { c: "guide", dash: "4 4" });
    s.forEach((v, i) => { b.rect(i + 1 - 0.28, 0, i + 1 + 0.28, v, { c: CLS[i], opacity: 0.85 }); b.text(i + 1, v, FV.fmt(v, 3), { anchor: "middle", dy: -7 }); });
    if (extra) extra();
  }

  // 1. Logits → probabilities, with temperature and the shift that changes nothing.
  FV.widget("softmax-bars", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const z0 = (cfg.z || [2, 1, 0]).slice(), z = z0.slice();
    const a = new FV.Plot(FV.col(w.stage), { x: [0.4, 3.6], y: [-5, 5], xTicks: barTicks("z"), aspect: 0.9, maxHeight: 340, title: L.logits });
    const b = new FV.Plot(FV.col(w.stage), { x: [0.4, 3.6], y: [0, 1.1], xTicks: barTicks("s"), aspect: 0.9, maxHeight: 340, title: L.probs });
    const sT = FV.ui.slider({ label: L.T, min: -1, max: 1, step: 0.01, value: Math.log10(cfg.T || 1), map: (v) => Math.pow(10, v), unmap: (v) => Math.log10(v), fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const shift = (d) => { if (Math.max(...z) + d > 5.001 || Math.min(...z) + d < -5.001) return; for (let i = 0; i < 3; i++) z[i] = Math.round((z[i] + d) * 100) / 100; draw(); };
    const up = FV.ui.button({ label: L.up, onclick: () => shift(1) });
    const down = FV.ui.button({ label: L.down, onclick: () => shift(-1) });
    const rs = FV.ui.button({ label: L.reset, onclick: () => { z0.forEach((v, i) => (z[i] = v)); sT.set(cfg.T || 1); draw(); } });
    w.controls.append(sT.el, FV.h("div", { class: "fv-player" }, up.el, down.el, rs.el));
    const ro = FV.ui.readout(w.readout, [{ key: "s0", label: "s₁ =", c: "blue" }, { key: "s1", label: "s₂ =", c: "orange" }, { key: "s2", label: "s₃ =", c: "teal" }, { key: "se", label: L.sumexp }]);
    const hs = z.map((v, i) => a.handle(i + 1, v, { c: CLS[i], label: "z" + SUB[i], onDrag: (x, y) => { z[i] = Math.round(y * 20) / 20; return [i + 1, z[i]]; }, onChange: () => draw() }));
    function draw() {
      const T = sT.value, s = softmax(z, T);
      a.clear(); a.hline(0, { c: "guide", dash: false });
      z.forEach((v, i) => {
        a.rect(i + 1 - 0.28, 0, i + 1 + 0.28, v, { c: CLS[i], opacity: 0.8 });
        a.text(i + 1 + 0.2, v, FV.fmt(v, 2), { dx: 6, dy: v >= 0 ? -6 : 14 });
        hs[i].set(i + 1, v);
      });
      probBars(b, s);
      b.legend([{ label: L.uniform, c: "guide", dash: true }]);
      s.forEach((v, i) => ro.set("s" + i, FV.fmt(v, 3)));
      ro.set("se", FV.num(z.reduce((acc, v) => acc + Math.exp(v / T), 0), 4));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 2. One logit against the rest: s₁ is a sigmoid of z₁ − ln Σ e^{z_j}.
  FV.widget("softmax-sigmoid", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-6, 6], y: [-0.05, 1.05], xLabel: "z₁", yLabel: "s", aspect: 0.5 });
    const s2 = FV.ui.slider({ label: L.z2, min: -4, max: 4, step: 0.05, value: cfg.z2 != null ? cfg.z2 : 1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const s3 = FV.ui.slider({ label: L.z3, min: -4, max: 4, step: 0.05, value: cfg.z3 != null ? cfg.z3 : 0, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const third = FV.ui.check({ label: L.third, checked: true, onchange: (v) => { s3.input.disabled = !v; s3.el.style.opacity = v ? "" : "0.45"; draw(); } });
    w.controls.append(s2.el, s3.el, third.el);
    const ro = FV.ui.readout(w.readout, [{ key: "z", label: "z₁ =" }, { key: "m", label: L.m }, { key: "s", label: "s₁ =", c: "blue" }, { key: "q", label: "σ(z₁ − m) =" }]);
    let z1 = cfg.z1 != null ? cfg.z1 : 2;
    const M = () => (third.value ? lse([s2.value, s3.value]) : s2.value);
    const h = p.handle(z1, 0.5, { c: "blue", label: "z₁", onDrag: (x) => { z1 = Math.round(x * 20) / 20; return [z1, sig(z1 - M())]; }, onChange: () => draw() });
    function draw() {
      const m = M(), a = s2.value, c = s3.value, t3 = third.value;
      const den = (x) => Math.exp(x) + Math.exp(a) + (t3 ? Math.exp(c) : 0);
      p.clear(); p.hline(0.5, {});
      p.vline(m, { c: "blue", dash: "5 4", w: 1.2 });
      p.fn((x) => Math.exp(a) / den(x), { c: "orange", w: 2.2 });
      if (t3) p.fn((x) => Math.exp(c) / den(x), { c: "teal", w: 2.2 });
      p.fn((x) => sig(x - m), { c: "blue", w: 2.8 });
      const s = [Math.exp(z1), Math.exp(a), t3 ? Math.exp(c) : 0].map((v, i, arr) => v / (arr[0] + arr[1] + arr[2]));
      p.line(z1, -0.05, z1, s[0], { c: "guide", w: 1, dash: "3 3" });
      p.dot(z1, s[1], { c: "orange", r: 4 }); if (t3) p.dot(z1, s[2], { c: "teal", r: 4 });
      h.set(z1, s[0]);
      ro.set("z", FV.fmt(z1, 2)); ro.set("m", FV.fmt(m, 4)); ro.set("s", FV.fmt(s[0], 4)); ro.set("q", FV.fmt(sig(z1 - m), 4));
      const items = [{ label: L.s1sig, c: "blue" }, { label: "s₂", c: "orange" }];
      if (t3) items.push({ label: "s₃", c: "teal" });
      items.push({ label: L.center, c: "blue", dash: true });
      p.legend(items);
    }
    p.onresize = draw; draw();
  });

  // 3. The probability simplex: every softmax output is a point of the triangle.
  FV.widget("softmax-simplex", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const p = new FV.Plot(FV.col(w.stage), { x: [-0.12, 1.12], y: [-0.13, 0.95], equal: true, grid: false, xTicks: [], yTicks: [], margin: { l: 6, r: 6, t: 6, b: 6 }, title: L.simplex });
    const b = new FV.Plot(FV.col(w.stage), { x: [0.4, 3.6], y: [0, 1.1], xTicks: barTicks("s"), aspect: 0.9, maxHeight: 320, title: L.bars });
    const zc = (z) => { const m = (z[0] + z[1] + z[2]) / 3; return z.map((v) => v - m); };
    let z = zc(cfg.z || [2, 1, 0]);
    const sT = FV.ui.slider({ label: L.T, min: -1, max: 1, step: 0.01, value: 0, map: (v) => Math.pow(10, v), unmap: (v) => Math.log10(v), fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const rs = FV.ui.button({ label: L.reset, onclick: () => { z = zc(cfg.z || [2, 1, 0]); sT.set(1); draw(); } });
    w.controls.append(sT.el, rs.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: "s =" }, { key: "z", label: L.zc }, { key: "h", label: L.ent }]);
    const h = p.handle(0, 0, {
      c: "ink", label: "s",
      onDrag: (x, y) => { const T = sT.value, s = inside(toS(x, y), 0.004); z = zc(s.map((v) => T * Math.log(v))); return toXY(s); },
      onChange: () => draw(),
    });
    let cols = CLS.map(rgbOf);
    function draw() {
      const T = sT.value, s = softmax(z, T);
      p.clear();
      paint(p, (x, y) => { const q = toS(x, y); return Math.min(...q) < -0.003 ? null : regionColour(q, cols, 130); }, 3);
      simplexFrame(p);
      const tp = [], zp = [];
      for (let k = 0; k <= 160; k++) { const tau = Math.pow(10, -1.6 + (3.4 * k) / 160); tp.push(toXY(softmax(z, tau))); }
      for (let k = 0; k <= 160; k++) { const t = -14 + (28 * k) / 160; zp.push(toXY(softmax([z[0] + t, z[1], z[2]], T))); }
      p.path(zp, { c: "blue", w: 1.6, opacity: 0.75 });
      p.path(tp, { c: "ink", w: 1.6, dash: "5 4" });
      const P = toXY(s);
      h.set(P[0], P[1]);
      probBars(b, s);
      ro.set("s", vec(s)); ro.set("z", vec(z, 2)); ro.set("h", FV.fmt(entropy(s), 3));
      p.legend([{ label: L.pathT, c: "ink", dash: true }, { label: L.pathZ, c: "blue" }]);
      b.legend([{ label: L.uniform, c: "guide", dash: true }]);
    }
    onTheme(() => { cols = CLS.map(rgbOf); draw(); });
    p.onresize = draw; b.onresize = draw; draw();
  });

  // 4. The Jacobian: a heatmap of diag(s) − s sᵀ and the derivative curves of one column.
  FV.widget("softmax-jacobian", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const M = new FV.Plot(FV.col(w.stage), {
      x: [0, 3], y: [0, 3], equal: true, grid: false, margin: { l: 30, r: 6, t: 6, b: 26 },
      xTicks: [0.5, 1.5, 2.5].map((v, j) => ({ v, label: "∂/∂z" + SUB[j] })), yTicks: [2.5, 1.5, 0.5].map((v, i) => ({ v, label: "s" + SUB[i] })), title: L.matrix,
    });
    const P = new FV.Plot(FV.col(w.stage), { x: [-6, 6], y: [-0.27, 0.32], xLabel: "zⱼ", yLabel: "∂sᵢ/∂zⱼ", aspect: 0.9, maxHeight: 340, title: L.curves });
    const z = (cfg.z || [2, 1, 0]).slice();
    const sl = [0, 1, 2].map((i) => FV.ui.slider({ label: "$z_" + (i + 1) + "$", min: -4, max: 4, step: 0.05, value: z[i], fmt: (v) => FV.fmt(v, 2), oninput: (v) => { z[i] = v; draw(); } }));
    const col = FV.ui.seg({ label: L.col, value: cfg.j || 0, options: [0, 1, 2].map((j) => ({ value: j, label: "∂/∂z" + SUB[j] })), onchange: draw });
    w.controls.append(...sl.map((s) => s.el), col.el);
    const ro = FV.ui.readout(w.readout, [{ key: "d", label: L.diag }, { key: "c", label: L.colsum }, { key: "t", label: L.trace }]);
    const jac = (s) => s.map((si, i) => s.map((sj, j) => si * ((i === j ? 1 : 0) - sj)));
    function draw() {
      const s = softmax(z), J = jac(s), j = col.value;
      M.clear();
      for (let i = 0; i < 3; i++) for (let k = 0; k < 3; k++) {
        const v = J[i][k], c = FV.cmap("diverging", FV.clamp(0.5 + v / 0.5, 0, 1));
        const x0 = M.X(k), x1 = M.X(k + 1), y0 = M.Y(3 - i), y1 = M.Y(2 - i);
        FV.svg("rect", { x: x0 + 1, y: y0 + 1, width: x1 - x0 - 2, height: y1 - y0 - 2, fill: FV.rgb(c), rx: 3 }, M.gMain);
        const t = M.text(k + 0.5, 2.5 - i, FV.fmt(v, 3), { anchor: "middle", dy: 4 });
        const lum = (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255;
        t.style.stroke = "none"; t.style.fill = lum > 0.55 ? "#171A20" : "#FFFFFF"; t.style.fontWeight = "600";
      }
      M.path([[j, 0], [j + 1, 0], [j + 1, 3], [j, 3]], { c: "ink", w: 2.2, close: true });
      P.clear(); P.hline(0, { c: "guide", dash: false }); P.hline(0.25, { c: "faint", dash: "4 4" });
      for (let i = 0; i < 3; i++) {
        const f = (x) => { const zz = z.slice(); zz[j] = x; const q = softmax(zz); return q[i] * ((i === j ? 1 : 0) - q[j]); };
        P.fn(f, { c: CLS[i], w: i === j ? 2.8 : 2 });
        P.dot(z[j], J[i][j], { c: CLS[i], r: 4.5 });
      }
      P.line(z[j], -0.27, z[j], 0.32, { c: "guide", w: 1, dash: "3 3" });
      P.text(5.9, 0.25, "0" + (FV.lang === "en" ? "." : ",") + "25", { c: "faint", dy: -5, anchor: "end" });
      P.legend([0, 1, 2].map((i) => ({ label: "∂s" + SUB[i] + "/∂z" + SUB[j], c: CLS[i] })));
      ro.set("d", FV.fmt(J[j][j], 4)); ro.set("c", FV.fmt(J[0][j] + J[1][j] + J[2][j] + 0, 4)); ro.set("t", FV.fmt(J[0][0] + J[1][1] + J[2][2], 4));
    }
    onTheme(draw);
    M.onresize = draw; P.onresize = draw; draw();
  });

  // 5. 3D: sₖ(z₁, z₂) with z₃ = 0, and the logit plane split into argmax regions.
  FV.widget("softmax-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const F = {
      s1: { f: (a, b) => softmax([a, b, 0])[0], z: [0, 1], lv: [0.1, 0.5, 0.9], label: "s₁" },
      s2: { f: (a, b) => softmax([a, b, 0])[1], z: [0, 1], lv: [0.1, 0.5, 0.9], label: "s₂" },
      s3: { f: (a, b) => softmax([a, b, 0])[2], z: [0, 1], lv: [0.1, 0.5, 0.9], label: "s₃" },
      d11: { f: (a, b) => { const s = softmax([a, b, 0])[0]; return s * (1 - s); }, z: [0, 0.25], lv: [0.05, 0.15, 0.24], label: "∂s₁/∂z₁" },
    };
    let pt = (cfg.z || [2, 1]).slice(0, 2);
    const kind = FV.ui.seg({ label: L.surf, value: cfg.f || "s1", options: [{ value: "s1", label: "$s_1$" }, { value: "s2", label: "$s_2$" }, { value: "s3", label: "$s_3$" }, { value: "d11", label: "$\\partial s_1/\\partial z_1$" }], onchange: () => { S.o.labels.z = F[kind.value].label; S.setF(F[kind.value].f, F[kind.value].z); draw(); } });
    w.controls.append(kind.el);
    const S = new FV.Surface(FV.col(w.stage), { f: F.s1.f, x: [-6, 6], y: [-6, 6], z: [0, 1], n: 36, labels: { x: "z₁", y: "z₂", z: "s₁" }, azimuth: cfg.az != null ? cfg.az : 0.9, elevation: cfg.el != null ? cfg.el : 0.5, aspect: 0.9, title: "s(z₁, z₂, 0)" });
    const p = new FV.Plot(FV.col(w.stage), { x: [-6, 6], y: [-6, 6], xLabel: "z₁", yLabel: "z₂", equal: true, title: L.plane });
    const ro = FV.ui.readout(w.readout, [{ key: "z", label: "z =" }, { key: "s", label: "s =" }, { key: "v", label: "f =" }]);
    const h = p.handle(pt[0], pt[1], { c: "ink", label: "z", onDrag: (x, y) => { pt = [Math.round(x * 10) / 10, Math.round(y * 10) / 10]; return pt; }, onChange: () => draw() });
    let cols = CLS.map(rgbOf);
    function draw() {
      const G = F[kind.value], s = softmax([pt[0], pt[1], 0]), v = G.f(pt[0], pt[1]);
      S.setPoints([{ x: pt[0], y: pt[1], z: v, c: "ink", r: 5.5 }]);
      p.clear();
      paint(p, (x, y) => regionColour(softmax([x, y, 0]), cols, 140), 4);
      p.contours(G.f, G.lv, { style: (lv) => ({ c: "ink", w: lv === G.lv[1] ? 1.8 : 1, opacity: 0.7, dash: lv === G.lv[1] ? null : "4 4" }) });
      p.line(0, 0, 6, 6, { c: "ink", w: 1.2, opacity: 0.6 }); p.line(0, 0, 0, -6, { c: "ink", w: 1.2, opacity: 0.6 }); p.line(0, 0, -6, 0, { c: "ink", w: 1.2, opacity: 0.6 });
      h.set(pt[0], pt[1]);
      ro.set("z", vec([pt[0], pt[1], 0], 1)); ro.set("s", vec(s)); ro.set("v", FV.fmt(v, 4));
      p.legend([0, 1, 2].map((k) => ({ label: L.class + " " + (k + 1), c: CLS[k], box: true })).concat([{ label: G.label + " = " + G.lv.map((x) => FV.num(x)).join(SEP), c: "ink", dash: true }]));
    }
    onTheme(() => { cols = CLS.map(rgbOf); draw(); });
    p.onresize = draw; draw();
  });

  // 6. Log-sum-exp: a smooth maximum whose gradient is softmax.
  FV.widget("softmax-lse", (el, cfg) => {
    const w = FV.shell(el, {});
    const top = new FV.Plot(w.stage, { x: [-4, 4], y: [-0.5, 4.5], xLabel: "x", yLabel: "y", aspect: 0.45, title: L.lseTop });
    const bot = new FV.Plot(w.stage, { x: [-4, 4], y: [-0.08, 1.08], xLabel: "x", yLabel: "d/dx", aspect: 0.26, minHeight: 170, maxHeight: 230, title: L.lseBot });
    const sT = FV.ui.slider({ label: L.T, min: -1.3, max: 0.5, step: 0.01, value: Math.log10(cfg.T || 1), map: (v) => Math.pow(10, v), unmap: (v) => Math.log10(v), fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sT.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "l", label: "LSE_T =", c: "blue" }, { key: "g", label: L.gap }, { key: "d", label: "σ(x/T) =", c: "orange" }]);
    let x0 = cfg.x != null ? cfg.x : 1;
    const LSE = (x) => { const T = sT.value; return Math.max(x, 0) + T * Math.log1p(Math.exp(-Math.abs(x) / T)); };
    const h = top.handle(x0, LSE(x0), { c: "blue", label: "x", onDrag: (x) => { x0 = Math.round(x * 20) / 20; return [x0, LSE(x0)]; }, onChange: () => draw() });
    function draw() {
      const T = sT.value;
      top.clear();
      top.area(LSE, (x) => Math.max(x, 0), { c: "blue", fillOpacity: 0.12 });
      top.fn((x) => Math.max(x, 0) + T * Math.LN2, { c: "faint", w: 1.4, dash: "5 4" });
      top.fn((x) => Math.max(x, 0), { c: "ink", w: 2 });
      top.fn(LSE, { c: "blue", w: 2.6 });
      top.line(x0, Math.max(x0, 0), x0, LSE(x0), { c: "orange", w: 2 });
      h.set(x0, LSE(x0));
      bot.clear();
      bot.path([[-4, 0], [0, 0], [0, 1], [4, 1]], { c: "guide", w: 1.6, dash: "5 4" });
      bot.fn((x) => sig(x / T), { c: "orange", w: 2.4 });
      bot.dot(x0, sig(x0 / T), { c: "orange" });
      ro.set("x", FV.fmt(x0, 2)); ro.set("l", FV.fmt(LSE(x0), 4)); ro.set("g", FV.fmt(LSE(x0) - Math.max(x0, 0), 4)); ro.set("d", FV.fmt(sig(x0 / T), 4));
      top.legend([{ label: L.lse, c: "blue" }, { label: L.maxf, c: "ink" }, { label: L.bound, c: "faint", dash: true }, { label: L.gap.replace(" =", ""), c: "orange" }]);
      bot.legend([{ label: L.deriv, c: "orange" }, { label: L.step, c: "guide", dash: true }]);
    }
    top.onresize = draw; bot.onresize = draw; draw();
  });

  // Three Gaussian clouds, one per class (deterministic).
  function clouds(seed, n, r, sd) {
    const R = FV.rng(seed), pts = [];
    for (let k = 0; k < 3; k++) {
      const a = Math.PI / 2 + (2 * Math.PI * k) / 3, cx = r * Math.cos(a), cy = r * Math.sin(a);
      for (let i = 0; i < n; i++) { const x = cx + sd * R.normal(), y = cy + sd * R.normal(); pts.push({ x, y, c: k }); }
    }
    return pts;
  }

  // 7. Softmax regression: three linear scores, softmax on top, gradient descent on CE.
  FV.widget("softmax-regression", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const pts = clouds(3, 30, 1.6, 0.85);
    const A = new FV.Plot(FV.col(w.stage), { x: [-4, 4], y: [-4, 4], xLabel: "x₁", yLabel: "x₂", equal: true, title: L.reg });
    const N = cfg.steps || 200, lr = cfg.lr || 0.15;
    const B = new FV.Plot(FV.col(w.stage), { x: [0, N], y: [0, 1.2], xLabel: L.stepN, yLabel: "CE", aspect: 1, maxHeight: 360, title: L.curve });
    let W, b, hist, step;
    const scores = (x, y) => [0, 1, 2].map((k) => W[k][0] * x + W[k][1] * y + b[k]);
    function stats() {
      let loss = 0, acc = 0;
      pts.forEach((q) => { const z = scores(q.x, q.y); loss += lse(z) - z[q.c]; acc += argmax(z) === q.c ? 1 : 0; });
      return [loss / pts.length, acc / pts.length];
    }
    function reset() { W = [[0, 0], [0, 0], [0, 0]]; b = [0, 0, 0]; step = 0; hist = [stats()[0]]; }
    function gd() {
      const gW = [[0, 0], [0, 0], [0, 0]], gb = [0, 0, 0];
      pts.forEach((q) => { const s = softmax(scores(q.x, q.y)); for (let k = 0; k < 3; k++) { const g = s[k] - (k === q.c ? 1 : 0); gW[k][0] += g * q.x; gW[k][1] += g * q.y; gb[k] += g; } });
      const n = pts.length;
      for (let k = 0; k < 3; k++) { W[k][0] -= (lr * gW[k][0]) / n; W[k][1] -= (lr * gW[k][1]) / n; b[k] -= (lr * gb[k]) / n; }
      step++; hist.push(stats()[0]);
    }
    reset();
    const player = FV.ui.player({ interval: 60, onstep() { if (step >= N) return false; gd(); draw(); return step < N; }, onreset() { reset(); draw(); } });
    w.controls.append(player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.stepN + " =" }, { key: "l", label: "CE =", c: "orange" }, { key: "a", label: L.acc + " =" }, { key: "h", label: L.cursor }]);
    let cols = CLS.map(rgbOf);
    A.hover((x, y) => {
      if (x == null) { ro.set("h", "—"); return; }
      A.hl("dot", x, y, { c: "ink", r: 4, hollow: true });
      ro.set("h", vec(softmax(scores(x, y)), 2));
    });
    function draw() {
      A.clear();
      paint(A, (x, y) => regionColour(softmax(scores(x, y)), cols, 150), 4);
      pts.forEach((q) => A.dot(q.x, q.y, { c: CLS[q.c], r: 4 }));
      B.clear();
      B.hline(Math.log(3), { c: "faint", dash: "4 4" });
      B.text(N, Math.log(3), "ln 3", { anchor: "end", dy: -6, c: "faint" });
      B.path(hist.map((v, i) => [i, v]), { c: "orange", w: 2.4 });
      B.dot(step, hist[step], { c: "orange", r: 4.5 });
      const [loss, acc] = stats();
      ro.set("t", String(step)); ro.set("l", FV.fmt(loss, 3)); ro.set("a", FV.fmt(100 * acc, 1) + "%");
      A.legend([0, 1, 2].map((k) => ({ label: L.class + " " + (k + 1), c: CLS[k], dot: true })));
      B.legend([{ label: "CE", c: "orange" }, { label: "ln 3 (s = 1/3)", c: "faint", dash: true }]);
    }
    onTheme(() => { cols = CLS.map(rgbOf); draw(); });
    A.onresize = draw; B.onresize = draw; draw();
  });

  // 8. Overflow: where the naive formula breaks in float32 / float64 and why subtracting the maximum fixes it.
  FV.widget("softmax-overflow", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, {
      x: [-800, 800], y: [-0.6, 2.6], xLabel: L.shiftC, aspect: 0.3, minHeight: 210, maxHeight: 260, grid: true,
      yTicks: [{ v: 2, label: "float32" }, { v: 1, label: "float64" }, { v: 0, label: "z − max z" }], margin: { l: 66 },
    });
    const f32 = Math.fround, id = (v) => v;
    const base = [2, 1, 0], truth = softmax(base);
    function naive(c, R) {
      const e = base.map((v) => R(Math.exp(R(v + c))));
      const s = R(R(e[0] + e[1]) + e[2]);
      return { e, s: e.map((v) => R(v / s)) };
    }
    function stable(c) { const z = base.map((v) => f32(v + c)), m = Math.max(...z); const e = z.map((v) => f32(Math.exp(f32(v - m)))); const s = f32(f32(e[0] + e[1]) + e[2]); return e.map((v) => f32(v / s)); }
    const status = (s) => (s.some(Number.isNaN) ? "nan" : Math.max(...s.map((v, i) => Math.abs(v - truth[i]))) < 1e-3 ? "ok" : "bad");
    const COL = { ok: "teal", nan: "red", bad: "orange" };
    function strip(row, fn) {
      let start = -800, cur = status(fn(-800));
      for (let c = -799; c <= 801; c++) {
        const st = c <= 800 ? status(fn(c)) : null;
        if (st !== cur) { p.rect(start - 0.5, row - 0.28, Math.min(c, 800) - 0.5, row + 0.28, { c: COL[cur], opacity: 0.75 }); start = c; cur = st; }
      }
    }
    const sc = FV.ui.slider({ label: L.c, min: -800, max: 800, step: 1, value: cfg.c || 0, fmt: (v) => FV.fmt(v, 0), oninput: draw });
    w.controls.append(sc.el);
    const ro = FV.ui.readout(w.readout, [{ key: "a", label: L.r32 }, { key: "b", label: L.r64 }, { key: "c", label: L.rst }, { key: "e", label: L.e32 }]);
    function draw() {
      const c = sc.value;
      p.clear();
      strip(2, (x) => naive(x, f32).s); strip(1, (x) => naive(x, id).s); strip(0, stable);
      p.vline(c, { c: "ink", w: 1.6, dash: false });
      const n32 = naive(c, f32), n64 = naive(c, id);
      ro.set("a", vec(n32.s)); ro.set("b", vec(n64.s)); ro.set("c", vec(stable(c))); ro.set("e", FV.num(n32.e[0], 3));
      p.legend([{ label: L.ok, c: "teal", box: true }, { label: L.nan, c: "red", box: true }, { label: L.bad, c: "orange", box: true }]);
    }
    p.onresize = draw; draw();
  });
})();
