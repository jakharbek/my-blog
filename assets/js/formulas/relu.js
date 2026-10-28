/* Widgets of the formula page "ReLU". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      x: "x", relu: "ReLU(x)", drelu: "ReLU′(x)", tangent: "касательная", ident: "y = x", fan: "опорные прямые в нуле: наклон ∈ [0; 1]",
      sub: "субдифференциал в нуле [0; 1]", conv: "соглашение: ReLU′(0) = 0",
      v: "Вес", sum: "сумма f(x)", hinge: "изломы vₖ·ReLU(x − cₖ)", slopes: "наклоны по участкам:", df: "f′(x): ступеньки", kink: "изломы",
      beta: "Резкость $\\beta$", sp: "softplus_β(x)", dsp: "σ(βx) — производная softplus", gap: "max разрыв ln 2/β", d0: "производная в 0",
      arch: "Сеть", n4: "4 нейрона", n8: "8 нейронов", deep: "2 слоя × 4", reseed: "Другая сеть", surf: "f(x₁, x₂)", top: "линейные области (вид сверху)",
      regions: "линейных областей в окне", maxr: "максимум для прямых", lines: "границы нейронов 1-го слоя", levels: "линии уровня f",
      units: "Нейронов", data: "данные", truth: "истинная функция", model: "сеть", unit: "вклад нейрона", deadU: "мёртвый нейрон", loss: "MSE", lossT: "MSE по шагам", it: "шаг", dead: "мёртвых",
      lr: "Шаг обучения $\\eta$", deadPct: "мёртвых нейронов, %", alive: "живой (яркость — доля точек, где активен)", deadN: "мёртвый: 0 на всех данных",
      init: "Инициализация", layer: "слой", q: "средний квадрат активаций", theory: "теория q₀(c/2)ˡ", ratio: "q₃₀ / q₀", active: "активных на посл. слое",
    },
    en: {
      x: "x", relu: "ReLU(x)", drelu: "ReLU′(x)", tangent: "tangent", ident: "y = x", fan: "supporting lines at zero: slope ∈ [0, 1]",
      sub: "subdifferential at zero [0, 1]", conv: "convention: ReLU′(0) = 0",
      v: "Weight", sum: "sum f(x)", hinge: "hinges vₖ·ReLU(x − cₖ)", slopes: "slopes of the pieces:", df: "f′(x): steps", kink: "kinks",
      beta: "Sharpness $\\beta$", sp: "softplus_β(x)", dsp: "σ(βx), the derivative of softplus", gap: "max gap ln 2/β", d0: "derivative at 0",
      arch: "Network", n4: "4 neurons", n8: "8 neurons", deep: "2 layers × 4", reseed: "Another network", surf: "f(x₁, x₂)", top: "linear regions (view from above)",
      regions: "linear regions in the window", maxr: "maximum for lines", lines: "boundaries of layer-1 neurons", levels: "level lines of f",
      units: "Neurons", data: "data", truth: "true function", model: "network", unit: "one neuron’s share", deadU: "dead neuron", loss: "MSE", lossT: "MSE over steps", it: "step", dead: "dead",
      lr: "Learning rate $\\eta$", deadPct: "dead neurons, %", alive: "alive (brightness = share of points where active)", deadN: "dead: 0 on all data",
      init: "Initialization", layer: "layer", q: "mean square of activations", theory: "theory q₀(c/2)ˡ", ratio: "q₃₀ / q₀", active: "active in the last layer",
    },
    uz: {
      x: "x", relu: "ReLU(x)", drelu: "ReLU′(x)", tangent: "urinma", ident: "y = x", fan: "noldagi tayanch chiziqlar: qiyalik ∈ [0; 1]",
      sub: "noldagi subdifferensial [0; 1]", conv: "kelishuv: ReLU′(0) = 0",
      v: "Vazn", sum: "yig‘indi f(x)", hinge: "sinishlar vₖ·ReLU(x − cₖ)", slopes: "bo‘laklar qiyaliklari:", df: "f′(x): zinalar", kink: "sinishlar",
      beta: "Keskinlik $\\beta$", sp: "softplus_β(x)", dsp: "σ(βx) — softplus hosilasi", gap: "maks. farq ln 2/β", d0: "0 dagi hosila",
      arch: "Tarmoq", n4: "4 neyron", n8: "8 neyron", deep: "2 qatlam × 4", reseed: "Boshqa tarmoq", surf: "f(x₁, x₂)", top: "chiziqli sohalar (yuqoridan)",
      regions: "oynadagi chiziqli sohalar", maxr: "to‘g‘ri chiziqlar uchun maksimum", lines: "1-qatlam neyronlari chegaralari", levels: "f ning sath chiziqlari",
      units: "Neyronlar", data: "ma’lumotlar", truth: "haqiqiy funksiya", model: "tarmoq", unit: "bitta neyron hissasi", deadU: "o‘lik neyron", loss: "MSE", lossT: "qadamlar bo‘yicha MSE", it: "qadam", dead: "o‘lik",
      lr: "O‘qitish qadami $\\eta$", deadPct: "o‘lik neyronlar, %", alive: "tirik (yorqinlik — faol bo‘lgan nuqtalar ulushi)", deadN: "o‘lik: barcha ma’lumotlarda 0",
      init: "Initsializatsiya", layer: "qatlam", q: "aktivatsiyalarning o‘rtacha kvadrati", theory: "nazariya q₀(c/2)ˡ", ratio: "q₃₀ / q₀", active: "oxirgi qatlamda faollar",
    },
  }[FV.lang] || {};
  const EN = FV.lang === "en";
  const dec = (s) => (EN ? s : s.replace(/(\d)\.(\d)/g, "$1,$2"));
  const relu = (x) => (x > 0 ? x : 0);
  const sup = (e) => (e === 0 ? "1" : "10" + String(e).replace("-", "⁻").replace(/\d/g, (c) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[c]));

  // 1. The kink: ReLU, its tangent, the step derivative and the subdifferential at zero.
  FV.widget("relu-explorer", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-4, 4], y: [-1.5, 4], xLabel: L.x, yLabel: L.relu, aspect: 0.5 });
    const d = new FV.Plot(w.stage, { x: [-4, 4], y: [-0.25, 1.3], xLabel: L.x, yLabel: L.drelu, aspect: 0.26, minHeight: 160, maxHeight: 210 });
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "r", label: "ReLU(x) =", c: "blue" }, { key: "d", label: "ReLU′(x) =", c: "orange" }]);
    let x0 = cfg.x != null ? cfg.x : 1.5;
    const h = p.handle(x0, relu(x0), { c: "blue", onDrag: (x) => { x0 = Math.abs(x) < 0.06 ? 0 : x; return [x0, relu(x0)]; }, onChange: () => draw() });
    function draw() {
      p.clear(); p.vline(0, {});
      p.fn((x) => x, { c: "guide", w: 1.4, dash: "5 4" });
      [0.25, 0.5, 0.75].forEach((k) => p.line(-1.6, -1.6 * k, 4, 4 * k, { c: "orange", w: 1.2, opacity: 0.5, dash: "4 4" }));
      if (x0 === 0) p.line(-1.6, -0.8, 4, 2, { c: "orange", w: 2 });
      else { const k = x0 > 0 ? 1 : 0; p.line(x0 - 1.5, relu(x0) - 1.5 * k, x0 + 1.5, relu(x0) + 1.5 * k, { c: "orange", w: 2 }); }
      p.fn(relu, { c: "ink", w: 2.6 });
      if (x0 > 0) p.line(x0 - 1.5, x0 - 1.5, x0 + 1.5, x0 + 1.5, { c: "orange", w: 2.2 });
      else if (x0 < 0) p.line(x0 - 1.5, 0, x0 + 1.5, 0, { c: "orange", w: 2.2 });
      h.set(x0, relu(x0));
      d.clear(); d.hline(0, { c: "guide", dash: false, opacity: 0.6 }); d.hline(1, { c: "guide", opacity: 0.6 });
      d.line(-4, 0, 0, 0, { c: "orange", w: 2.4 }); d.line(0, 1, 4, 1, { c: "orange", w: 2.4 });
      d.line(0, 0, 0, 1, { c: "orange", w: 4, opacity: 0.35 });
      d.dot(0, 1, { c: "orange", hollow: true, r: 4.5 }); d.dot(0, 0, { c: "orange", r: 4.5 });
      const dv = x0 > 0 ? 1 : 0;
      if (x0 !== 0) d.dot(x0, dv, { c: "blue", r: 4.5 });
      d.text(0.15, 0.5, dec(L.sub), { c: "orange" });
      ro.set("x", FV.fmt(x0, 2)); ro.set("r", FV.fmt(relu(x0), 2));
      ro.set("d", x0 === 0 ? (EN ? "∂ = [0, 1]; PyTorch: 0" : "∂ = [0; 1]; PyTorch: 0") : String(dv));
      p.legend([{ label: L.relu, c: "ink" }, { label: L.tangent, c: "orange" }, { label: L.fan, c: "orange", dash: true }, { label: L.ident, c: "guide", dash: true }]);
      d.legend([{ label: L.drelu, c: "orange" }, { label: L.conv, c: "orange", dot: true }]);
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 2. A sum of three hinges: any broken line; the derivative is a staircase with jumps vₖ.
  FV.widget("relu-hinges", (el, cfg) => {
    const w = FV.shell(el, {});
    const C = [-1, 0, 1];
    const p = new FV.Plot(w.stage, { x: [-3, 3], y: [-2.5, 2.5], xLabel: L.x, yLabel: "f(x)", aspect: 0.5 });
    const d = new FV.Plot(w.stage, { x: [-3, 3], y: [-3, 3], xLabel: L.x, yLabel: "f′(x)", aspect: 0.26, minHeight: 160, maxHeight: 210 });
    const V = [cfg.v1 != null ? cfg.v1 : 1, cfg.v2 != null ? cfg.v2 : -2, cfg.v3 != null ? cfg.v3 : 1];
    const sl = V.map((v, i) => FV.ui.slider({ label: L.v + " $v_" + (i + 1) + "$ (c = " + (C[i] < 0 ? "−1" : C[i]) + ")", min: -3, max: 3, step: 0.1, value: v, fmt: (u) => FV.fmt(u, 1), oninput: (u) => { V[i] = u; draw(); } }));
    sl.forEach((s) => w.controls.append(s.el));
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.slopes, c: "orange" }, { key: "m", label: "f(0) =", c: "blue" }]);
    const f = (x) => V.reduce((s, v, i) => s + v * relu(x - C[i]), 0);
    function draw() {
      const S = [0, V[0], V[0] + V[1], V[0] + V[1] + V[2]];
      p.clear(); p.hline(0, {});
      V.forEach((v, i) => p.fn((x) => v * relu(x - C[i]), { c: "guide", w: 1.4, dash: "5 4" }));
      p.fn(f, { c: "blue", w: 2.8 });
      C.forEach((c) => p.dot(c, f(c), { c: "blue", r: 4.5, hollow: true }));
      const lo = Math.min(-1.5, ...S) - 0.6, hi = Math.max(1.5, ...S) + 0.6;
      d.setDomain(null, [lo, hi]);
      d.clear(); d.hline(0, { c: "guide", dash: false });
      const xs = [-3, -1, 0, 1, 3];
      for (let i = 0; i < 4; i++) d.line(xs[i], S[i], xs[i + 1], S[i], { c: "orange", w: 2.4 });
      for (let i = 0; i < 3; i++) {
        d.line(C[i], S[i], C[i], S[i + 1], { c: "orange", w: 1, dash: "3 3" });
        if (Math.abs(V[i]) > 0.05) d.text(C[i], (S[i] + S[i + 1]) / 2, (V[i] > 0 ? "+" : "−") + FV.fmt(Math.abs(V[i]), 1), { dx: 6, size: 12 });
      }
      ro.set("s", S.map((v) => FV.fmt(v, 1)).join("  |  ")); ro.set("m", FV.fmt(f(0), 2));
      p.legend([{ label: L.sum, c: "blue" }, { label: L.hinge, c: "guide", dash: true }, { label: L.kink + " c = −1, 0, 1", c: "blue", dot: true }]);
      d.legend([{ label: L.df, c: "orange" }]);
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 3. Softplus as a smooth ReLU; its derivative σ(βx) tends to the step.
  FV.widget("relu-smooth", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-3, 3], y: [-0.4, 3], xLabel: L.x, yLabel: "y", aspect: 0.45 });
    const d = new FV.Plot(w.stage, { x: [-3, 3], y: [-0.1, 1.15], xLabel: L.x, yLabel: "y′", aspect: 0.26, minHeight: 160, maxHeight: 210 });
    const sb = FV.ui.slider({ label: L.beta, min: -1, max: 5, step: 0.05, value: Math.log2(cfg.beta || 1), map: (v) => Math.pow(2, v), unmap: (v) => Math.log2(v), fmt: (v) => FV.num(v, 3), oninput: draw });
    w.controls.append(sb.el);
    const ro = FV.ui.readout(w.readout, [{ key: "b", label: "β =" }, { key: "g", label: L.gap + " =", c: "blue" }, { key: "d", label: L.d0 + " σ(0) =", c: "orange" }]);
    function draw() {
      const b = sb.value;
      const sp = (x) => (Math.max(b * x, 0) + Math.log1p(Math.exp(-Math.abs(b * x)))) / b;
      p.clear(); p.vline(0, {});
      p.fn(relu, { c: "ink", w: 2.2 });
      p.fn(sp, { c: "blue", w: 2.6 });
      p.line(0, 0, 0, Math.log(2) / b, { c: "blue", w: 1.2, dash: "3 3" });
      p.dot(0, Math.log(2) / b, { c: "blue", r: 4 });
      d.clear(); d.hline(0, { c: "guide", dash: false }); d.hline(1, { c: "guide" }); d.hline(0.5, { c: "guide", opacity: 0.6 });
      d.line(-3, 0, 0, 0, { c: "ink", w: 2 }); d.line(0, 1, 3, 1, { c: "ink", w: 2 });
      d.fn((x) => FV.sigmoid(b * x), { c: "orange", w: 2.4 });
      d.dot(0, 0.5, { c: "orange", r: 4 });
      ro.set("b", FV.num(b, 3)); ro.set("g", FV.fmt(Math.log(2) / b, 3)); ro.set("d", FV.fmt(0.5, 1));
      p.legend([{ label: "ReLU(x)", c: "ink" }, { label: "softplus_β(x) = ln(1 + e^{βx}) / β".replace("^{βx}", "ᵝˣ"), c: "blue" }]);
      d.legend([{ label: "ReLU′(x)", c: "ink" }, { label: L.dsp, c: "orange" }]);
    }
    p.onresize = draw; d.onresize = draw; draw();
  });

  // 4. A ReLU network on the plane is piecewise linear: creases, flat facets, linear regions.
  FV.widget("relu-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const P = { arch: cfg.arch || "n4", seed: cfg.seed || 3 };
    let net = null;
    function build() {
      const r = FV.rng(P.seed);
      const H = P.arch === "n8" ? 8 : 4;
      const W1 = [], B1 = [];
      for (let k = 0; k < H; k++) { const t = 2 * Math.PI * r(); W1.push([Math.cos(t), Math.sin(t)]); B1.push((r() * 2 - 1) * 2); }
      let W2 = null, B2 = null;
      if (P.arch === "deep") {
        W2 = []; B2 = [];
        for (let k = 0; k < 4; k++) { W2.push(Array.from({ length: H }, () => r.normal() * Math.SQRT1_2)); B2.push((r() * 2 - 1) * 0.5); }
      }
      const V = Array.from({ length: P.arch === "deep" ? 4 : H }, () => r.normal());
      net = { H, W1, B1, W2, B2, V };
    }
    function forward(x, y, key) {
      const n = net, h1 = [];
      let code = "";
      for (let k = 0; k < n.H; k++) { const z = n.W1[k][0] * x + n.W1[k][1] * y + n.B1[k]; h1.push(z > 0 ? z : 0); code += z > 0 ? "1" : "0"; }
      let h = h1;
      if (n.W2) {
        h = [];
        for (let k = 0; k < 4; k++) { let z = n.B2[k]; for (let j = 0; j < n.H; j++) z += n.W2[k][j] * h1[j]; h.push(z > 0 ? z : 0); code += z > 0 ? "1" : "0"; }
      }
      if (key) return code;
      return h.reduce((s, v, k) => s + n.V[k] * v, 0);
    }
    const F = (x, y) => forward(x, y, false);
    build();
    const s3 = new FV.Surface(FV.col(w.stage), { f: F, x: [-3, 3], y: [-3, 3], n: 60, labels: { x: "x₁", y: "x₂", z: "f" }, azimuth: -0.5, elevation: 0.55, aspect: 0.85, cmap: "viridis", wire: false, title: L.surf });
    const h2 = new FV.Plot(FV.col(w.stage), { x: [-3, 3], y: [-3, 3], xLabel: "x₁", yLabel: "x₂", equal: true, title: L.top });
    const arch = FV.ui.seg({ label: L.arch, value: P.arch, options: [{ value: "n4", label: L.n4 }, { value: "n8", label: L.n8 }, { value: "deep", label: L.deep }], onchange: (v) => { P.arch = v; build(); draw(); } });
    const again = FV.ui.button({ label: "↻ " + L.reseed, onclick: () => { P.seed++; build(); draw(); } });
    w.controls.append(arch.el, again.el);
    const ro = FV.ui.readout(w.readout, [{ key: "r", label: L.regions + ":", c: "blue" }, { key: "m", label: L.maxr + " 1 + H + H(H − 1)/2:" }]);
    function draw() {
      s3.setF(F);
      // count activation patterns on a fine grid; each pattern is one linear piece
      const ids = new Map(), G = 300;
      for (let j = 0; j < G; j++) for (let i = 0; i < G; i++) {
        const k = forward(-3 + (6 * (i + 0.5)) / G, -3 + (6 * (j + 0.5)) / G, true);
        if (!ids.has(k)) ids.set(k, ids.size);
      }
      h2.clear();
      h2.heat((x, y) => { const k = forward(x, y, true); if (!ids.has(k)) ids.set(k, ids.size); return (ids.get(k) * 0.618034) % 1; }, { cmap: "viridis", z: [0, 1], res: 2, alpha: 0.55 });
      let lo = Infinity, hi = -Infinity;
      for (let j = 0; j <= 30; j++) for (let i = 0; i <= 30; i++) { const v = F(-3 + i / 5, -3 + j / 5); lo = Math.min(lo, v); hi = Math.max(hi, v); }
      const lv = FV.linspace(lo, hi, 11).slice(1, -1);
      h2.contours(F, lv, { c: "ink", w: 1, opacity: 0.5 });
      if (!net.W2) net.W1.forEach(([a, b], k) => {
        const c = net.B1[k];
        if (Math.abs(b) > Math.abs(a)) h2.line(-3, (-c + 3 * a) / b, 3, (-c - 3 * a) / b, { c: "ink", w: 1.6, dash: "6 4", opacity: 0.85 });
        else h2.line((-c + 3 * b) / a, -3, (-c - 3 * b) / a, 3, { c: "ink", w: 1.6, dash: "6 4", opacity: 0.85 });
      });
      const H = net.H;
      ro.set("r", String(ids.size)); ro.set("m", net.W2 ? "—" : String(1 + H + (H * (H - 1)) / 2));
      h2.legend(net.W2 ? [{ label: L.levels, c: "ink" }] : [{ label: L.lines, c: "ink", dash: true }, { label: L.levels, c: "ink" }]);
    }
    h2.onresize = draw; draw();
  });

  // 5. A one-hidden-layer ReLU network learns a curve as a broken line (full-batch Adam).
  FV.widget("relu-fit", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-3.2, 3.2], y: [-2, 2], xLabel: L.x, yLabel: "y", aspect: 0.5 });
    const q = new FV.Plot(w.stage, { x: [0, 1560], y: [1e-3, 10], yType: "log", xLabel: L.it, yLabel: L.lossT, aspect: 0.26, minHeight: 160, maxHeight: 210 });
    const truth = (x) => Math.sin(1.6 * x);
    const N = 40, rd = FV.rng(4);
    const xs = Array.from({ length: N }, (_, i) => -3 + (6 * i) / (N - 1));
    const ys = xs.map((x) => truth(x) + 0.08 * rd.normal());
    const lr = 0.02, MAX = 1500;
    let H = cfg.h || 6, Pm, M, V, t, hist;
    function init() {
      const r = FV.rng(9);
      const W = Array.from({ length: H }, () => r.normal() * Math.SQRT2), Bb = Array.from({ length: H }, () => (r() * 2 - 1) * 2.5), Vv = Array.from({ length: H }, () => r.normal() / Math.sqrt(H));
      Pm = W.concat(Bb, Vv, [0]); M = Pm.map(() => 0); V = Pm.map(() => 0); t = 0; hist = [[0, lossAndGrad().L]];
    }
    function net(x) { let s = Pm[3 * H]; for (let k = 0; k < H; k++) s += Pm[2 * H + k] * relu(Pm[k] * x + Pm[H + k]); return s; }
    function isDead(k) { return xs.every((x) => Pm[k] * x + Pm[H + k] <= 0); }
    function lossAndGrad() {
      const g = Pm.map(() => 0); let Ls = 0;
      for (let i = 0; i < N; i++) {
        const x = xs[i], z = [];
        let yh = Pm[3 * H];
        for (let k = 0; k < H; k++) { z[k] = Pm[k] * x + Pm[H + k]; yh += Pm[2 * H + k] * relu(z[k]); }
        const e = yh - ys[i]; Ls += e * e;
        for (let k = 0; k < H; k++) { g[2 * H + k] += (2 * e * relu(z[k])) / N; if (z[k] > 0) { const dz = (2 * e * Pm[2 * H + k]) / N; g[k] += dz * x; g[H + k] += dz; } }
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
    const hs = FV.ui.seg({ label: L.units, value: H, options: [3, 6, 12].map((v) => ({ value: v, label: String(v) })), onchange: (v) => { H = v; player.stop(); init(); draw(); } });
    const player = FV.ui.player({
      interval: 50,
      onstep() { for (let j = 0; j < 5 && t < MAX; j++) step(); hist.push([t, lossAndGrad().L]); draw(); return t < MAX; },
      onreset() { init(); draw(); },
    });
    w.controls.append(hs.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.it + " =" }, { key: "l", label: L.loss + " =", c: "blue" }, { key: "d", label: L.dead + " =", c: "red" }]);
    function draw() {
      p.clear(); p.hline(0, {});
      let dead = 0;
      for (let k = 0; k < H; k++) {
        const wk = Pm[k], bk = Pm[H + k], vk = Pm[2 * H + k], dk = isDead(k);
        if (dk) dead++;
        p.fn((x) => vk * relu(wk * x + bk), { c: dk ? "red" : "teal", w: 1.3, opacity: dk ? 0.6 : 0.8, dash: dk ? "4 4" : null });
        const c = -bk / wk;
        if (Math.abs(wk) > 1e-9 && c > -3.2 && c < 3.2) p.dot(c, -1.85, { c: dk ? "red" : "teal", r: 3.5 });
      }
      p.fn(truth, { c: "guide", w: 1.6, dash: "6 5" });
      xs.forEach((x, i) => p.dot(x, ys[i], { c: "faint", r: 3.2 }));
      p.fn(net, { c: "blue", w: 2.6 });
      p.legend([{ label: L.model, c: "blue" }, { label: L.unit + " vₖ·ReLU(wₖx + bₖ)", c: "teal" }, { label: L.deadU, c: "red", dash: true }, { label: L.truth, c: "guide", dash: true }, { label: L.data, c: "faint", dot: true }]);
      q.clear(); q.path(hist.map(([s, v]) => [s, Math.max(v, 1e-3)]), { c: "blue", w: 2 });
      const Lc = hist[hist.length - 1][1];
      q.dot(t, Math.max(Lc, 1e-3), { c: "blue", r: 4 });
      ro.set("t", String(t)); ro.set("l", FV.fmt(Lc, 4)); ro.set("d", dead + " / " + H);
    }
    init();
    p.onresize = draw; q.onresize = draw; draw();
  });

  // 6. Dying ReLU: with a too-large learning rate most neurons switch off for good.
  FV.widget("relu-dead", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const H = 64, N = 128, BS = 16, T = 600, LRS = [0.03, 0.1, 0.2, 0.3];
    const rd = FV.rng(12), X = [], Y = [];
    for (let i = 0; i < N; i++) { const a = rd() * 2 - 1, b = rd() * 2 - 1; X.push([a, b]); Y.push(Math.sin(3 * a) + b); }
    function run(lr) {
      const r = FV.rng(21);
      const W = Array.from({ length: H }, () => [r.normal(), r.normal()]), B = new Array(H).fill(0);
      const V = Array.from({ length: H }, () => r.normal() / Math.sqrt(H));
      let c = 0;
      const dead = [], loss = [], act = [];
      for (let t = 0; t <= T; t++) {
        const cnt = new Array(H).fill(0); let Ls = 0;
        for (let i = 0; i < N; i++) {
          let yh = c;
          for (let k = 0; k < H; k++) { const z = W[k][0] * X[i][0] + W[k][1] * X[i][1] + B[k]; if (z > 0) { cnt[k]++; yh += V[k] * z; } }
          Ls += (yh - Y[i]) ** 2;
        }
        dead.push(cnt.filter((v) => v === 0).length / H); loss.push(Ls / N); act.push(cnt.map((v) => v / N));
        if (t === T) break;
        const gW = W.map(() => [0, 0]), gB = new Array(H).fill(0), gV = new Array(H).fill(0); let gc = 0;
        for (let j = 0; j < BS; j++) {
          const i = (t * BS + j) % N, z = [];
          let yh = c;
          for (let k = 0; k < H; k++) { z[k] = W[k][0] * X[i][0] + W[k][1] * X[i][1] + B[k]; if (z[k] > 0) yh += V[k] * z[k]; }
          const e = (2 * (yh - Y[i])) / BS;
          gc += e;
          for (let k = 0; k < H; k++) if (z[k] > 0) { gV[k] += e * z[k]; const dz = e * V[k]; gW[k][0] += dz * X[i][0]; gW[k][1] += dz * X[i][1]; gB[k] += dz; }
        }
        for (let k = 0; k < H; k++) { W[k][0] -= lr * gW[k][0]; W[k][1] -= lr * gW[k][1]; B[k] -= lr * gB[k]; V[k] -= lr * gV[k]; }
        c -= lr * gc;
      }
      return { dead, loss, act };
    }
    const runs = LRS.map(run);
    const p = new FV.Plot(FV.col(w.stage), { x: [0, T * 1.04], y: [-3, 118], yTicks: [0, 20, 40, 60, 80, 100], xLabel: L.it, yLabel: L.deadPct, aspect: 0.75 });
    const g = new FV.Plot(FV.col(w.stage), { x: [0, 8], y: [0, 8], equal: true, grid: false, xTicks: [], yTicks: [], margin: { l: 10, r: 10, t: 10, b: 10 } });
    let sel = LRS.indexOf(cfg.lr != null ? cfg.lr : 0.3); if (sel < 0) sel = 3;
    let t = cfg.t != null ? cfg.t : T;
    const seg = FV.ui.seg({ label: L.lr, value: LRS[sel], options: LRS.map((v) => ({ value: v, label: dec(String(v)) })), onchange: (v) => { sel = LRS.indexOf(v); draw(); } });
    const player = FV.ui.player({
      interval: 60,
      onstep() { if (t >= T) t = 0; t = Math.min(T, t + 5); draw(); return t < T; },
      onreset() { t = 0; draw(); },
    });
    w.controls.append(seg.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.it + " =" }, { key: "d", label: L.deadPct.replace(", %", "") + " =", c: "red" }, { key: "l", label: L.loss + " =", c: "blue" }]);
    function draw() {
      p.clear();
      const ends = {};
      runs.forEach((R, i) => {
        if (i === sel) return;
        p.path(R.dead.map((v, s) => [s, 100 * v]), { c: "guide", w: 1.4, dash: "5 4" });
        const e = Math.round(100 * R.dead[T]);
        (ends[e] = ends[e] || []).push(dec(String(LRS[i])));
      });
      Object.keys(ends).forEach((e) => p.text(T - 6, +e + (e > 90 ? -6 : 5), "η = " + ends[e].join(EN ? ", " : "; "), { anchor: "end", size: 11 }));
      const R = runs[sel];
      p.path(R.dead.slice(0, t + 1).map((v, s) => [s, 100 * v]), { c: "red", w: 2.6 });
      p.vline(t, { c: "ink", opacity: 0.5 });
      p.dot(t, 100 * R.dead[t], { c: "red", r: 4.5 });
      p.legend([{ label: "η = " + dec(String(LRS[sel])), c: "red" }, { label: dec("η = 0.03, 0.1, 0.2, 0.3"), c: "guide", dash: true }]);
      g.clear();
      R.act[t].forEach((a, k) => {
        const cx = k % 8, cy = 7 - Math.floor(k / 8);
        if (a === 0) g.rect(cx + 0.08, cy + 0.08, cx + 0.92, cy + 0.92, { c: "red", opacity: 0.7, rx: 3 });
        else g.rect(cx + 0.08, cy + 0.08, cx + 0.92, cy + 0.92, { c: "blue", opacity: 0.2 + 0.75 * a, rx: 3 });
      });
      g.legend([{ label: L.alive, c: "blue", box: true }, { label: L.deadN, c: "red", box: true }]);
      ro.set("t", String(t)); ro.set("d", Math.round(100 * R.dead[t]) + "%"); ro.set("l", FV.fmt(R.loss[t], 3));
    }
    p.onresize = draw; g.onresize = draw; draw();
  });

  // 7. He initialization: the mean square of activations through 30 ReLU layers.
  FV.widget("relu-depth", (el, cfg) => {
    const w = FV.shell(el, {});
    const n = 100, B = 20, D = 30;
    const yt = [-10, -5, 0, 5].map((e) => ({ v: Math.pow(10, e), label: sup(e) }));
    const p = new FV.Plot(w.stage, { x: [-0.7, D + 0.7], y: [1e-11, 1e7], yType: "log", yTicks: yt, xLabel: L.layer, yLabel: L.q, aspect: 0.45 });
    const init = FV.ui.seg({ label: L.init, value: cfg.c || 2, options: [{ value: 1, label: dec("1/n (LeCun)") }, { value: 2, label: "2/n (He)" }, { value: 3, label: "3/n" }], onchange: draw });
    w.controls.append(init.el);
    const ro = FV.ui.readout(w.readout, [{ key: "r", label: L.ratio + " =", c: "blue" }, { key: "t", label: L.theory.split(" ")[0] + " (c/2)³⁰ =", c: "orange" }, { key: "a", label: L.active + " =" }]);
    const r = FV.rng(5);
    const X = Array.from({ length: B }, () => Array.from({ length: n }, () => r.normal()));
    const Ws = Array.from({ length: D }, () => Array.from({ length: n }, () => Array.from({ length: n }, () => r.normal())));
    const cache = {};
    function run(c) {
      if (cache[c]) return cache[c];
      const s = Math.sqrt(c / n), q = [], all = (h) => h.reduce((a, row) => a + row.reduce((b, v) => b + v * v, 0), 0) / (B * n);
      let h = X, act = 0;
      q.push(all(h));
      for (let l = 0; l < D; l++) {
        const W = Ws[l];
        let on = 0;
        h = h.map((row) => W.map((wr) => { let z = 0; for (let j = 0; j < n; j++) z += row[j] * wr[j]; z *= s; if (z > 0) { on++; return z; } return 0; }));
        q.push(all(h)); act = on / (B * n);
      }
      return (cache[c] = { q, act });
    }
    function draw() {
      const c = init.value, R = run(c);
      p.clear(); p.hline(1, { c: "guide", dash: false });
      R.q.forEach((v, l) => p.rect(l - 0.32, 1e-11, l + 0.32, FV.clamp(v, 1e-11, 1e7), { c: "blue", opacity: 0.8 }));
      p.fn((l) => R.q[0] * Math.pow(c / 2, l), { c: "orange", w: 2, dash: true, from: 0, to: D });
      ro.set("r", FV.num(R.q[D] / R.q[0], 3)); ro.set("t", FV.num(Math.pow(c / 2, D), 3)); ro.set("a", Math.round(100 * R.act) + "%");
      p.legend([{ label: L.q + " qₗ", c: "blue", box: true }, { label: L.theory, c: "orange", dash: true }]);
    }
    p.onresize = draw; draw();
  });
})();
