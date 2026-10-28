/* Widgets of the formula page "SGD → Momentum → RMSProp". Built on FV (assets/js/viz.js).
   Optimizer colours, shared with the Adam page: SGD ink, Momentum blue, RMSProp teal, Adam orange, AdamW violet. */
(function () {
  "use strict";
  const L = {
    ru: {
      step: "шаг", steps: "шагов", eta: "Темп $\\eta$", curv: "Кривизна $L$", etaL: "ηL =", mult: "множитель 1 − ηL =", regime: "режим:", reach: "шагов до |θ| < 0,01:",
      mono: "монотонно сходится", one: "сходится за один шаг", osc: "сходится с колебаниями", edge: "колеблется без затухания", div: "расходится", never: "не сходится",
      sgdPath: "шаги SGD", theory: "|1 − ηL|ᵗ·|θ₀|", parab: "f(θ) = Lθ²/2",
      batch: "Мини-батч $B$", full: "все", epoch: "эпоха", upd: "обновлений за эпоху:", excess: "L − L* =", noise: "разброс шага:", epochs: "эпох:",
      cloud: "куда может попасть шаг", fullStep: "шаг по полному градиенту", fullGD: "полный градиент (B = 200)", otherB: "другие B", selB: "выбранный B",
      beta: "Инерция $\\beta$", form: "Форма", heavy: "$u=\\beta u+g$", ema: "EMA $(1-\\beta)$", weight: "вес градиента $g_{t-k}$", lag: "давность k", half: "половина веса", rest: "остальной вес",
      resp: "ответ на постоянный градиент g = 1", window: "окно 1/(1 − β) =", halfN: "половина веса — в последних", grads: "градиентах", limit: "предел uₜ =",
      polyak: "Поляк", nesterov: "Нестеров", rho: "ρ (скорость сходимости)", hL: "ηL", bAx: "β", xt: "θₜ", gd: "SGD (β = 0)", mom: "Momentum", nes: "Nesterov",
      rhoGD: "ρ SGD =", rhoM: "ρ с инерцией =", nGD: "шагов SGD:", nM: "шагов с инерцией:", over: "без колебаний", fast: "быстрая сходимость", under: "колебания затухают", divg: "расходится", bound: "граница ρ = 1", crit: "критическое затухание",
      kappa: "Вытянутость $\\kappa$", rot: "Поворот", etaSM: "$\\eta$ (SGD, Momentum)", rms: "RMSProp", sgd: "SGD", fAfter: "f после", now: "шаг t =",
      start: "старт (тяните)", tScrub: "Шаг $t$", f: "f(θ)", reach3: "до f < 10⁻³:", fEnd: "f после 3000:",
      gAbs: "|gₜ|", sqrtv: "√vₜ", sgdStep: "|Δθ| SGD", rmsStep: "|Δθ| RMSProp", boundL: "граница η/√(1 − β)", maxStep: "макс. шаг RMSProp после скачка:", scaleJump: "масштаб градиента ×10, затем ×0,01",
    },
    en: {
      step: "step", steps: "steps", eta: "Rate $\\eta$", curv: "Curvature $L$", etaL: "ηL =", mult: "factor 1 − ηL =", regime: "regime:", reach: "steps to |θ| < 0.01:",
      mono: "converges monotonically", one: "converges in one step", osc: "converges with oscillations", edge: "oscillates forever", div: "diverges", never: "does not converge",
      sgdPath: "SGD steps", theory: "|1 − ηL|ᵗ·|θ₀|", parab: "f(θ) = Lθ²/2",
      batch: "Mini-batch $B$", full: "all", epoch: "epoch", upd: "updates per epoch:", excess: "L − L* =", noise: "step spread:", epochs: "epochs:",
      cloud: "where the step may land", fullStep: "full-gradient step", fullGD: "full gradient (B = 200)", otherB: "other B", selB: "chosen B",
      beta: "Momentum $\\beta$", form: "Form", heavy: "$u=\\beta u+g$", ema: "EMA $(1-\\beta)$", weight: "weight of gradient $g_{t-k}$", lag: "age k", half: "half of the weight", rest: "the rest",
      resp: "response to a constant gradient g = 1", window: "window 1/(1 − β) =", halfN: "half of the weight is in the last", grads: "gradients", limit: "limit of uₜ =",
      polyak: "Polyak", nesterov: "Nesterov", rho: "ρ (convergence rate)", hL: "ηL", bAx: "β", xt: "θₜ", gd: "SGD (β = 0)", mom: "Momentum", nes: "Nesterov",
      rhoGD: "ρ SGD =", rhoM: "ρ with momentum =", nGD: "SGD steps:", nM: "steps with momentum:", over: "no oscillations", fast: "fast convergence", under: "damped oscillations", divg: "diverges", bound: "boundary ρ = 1", crit: "critical damping",
      kappa: "Elongation $\\kappa$", rot: "Rotation", etaSM: "$\\eta$ (SGD, Momentum)", rms: "RMSProp", sgd: "SGD", fAfter: "f after", now: "step t =",
      start: "start (drag it)", tScrub: "Step $t$", f: "f(θ)", reach3: "to f < 10⁻³:", fEnd: "f after 3000:",
      gAbs: "|gₜ|", sqrtv: "√vₜ", sgdStep: "|Δθ| SGD", rmsStep: "|Δθ| RMSProp", boundL: "bound η/√(1 − β)", maxStep: "max RMSProp step after the jump:", scaleJump: "gradient scale ×10, then ×0.01",
    },
    uz: {
      step: "qadam", steps: "qadam", eta: "Tezlik $\\eta$", curv: "Egrilik $L$", etaL: "ηL =", mult: "ko‘paytuvchi 1 − ηL =", regime: "rejim:", reach: "|θ| < 0,01 gacha qadamlar:",
      mono: "monoton yaqinlashadi", one: "bir qadamda yaqinlashadi", osc: "tebranib yaqinlashadi", edge: "so‘nmasdan tebranadi", div: "uzoqlashadi", never: "yaqinlashmaydi",
      sgdPath: "SGD qadamlari", theory: "|1 − ηL|ᵗ·|θ₀|", parab: "f(θ) = Lθ²/2",
      batch: "Mini-batch $B$", full: "hammasi", epoch: "davr", upd: "davrdagi yangilanishlar:", excess: "L − L* =", noise: "qadam tarqoqligi:", epochs: "davrlar:",
      cloud: "qadam tushishi mumkin bo‘lgan joy", fullStep: "to‘liq gradiyent qadami", fullGD: "to‘liq gradiyent (B = 200)", otherB: "boshqa B", selB: "tanlangan B",
      beta: "Inersiya $\\beta$", form: "Shakl", heavy: "$u=\\beta u+g$", ema: "EMA $(1-\\beta)$", weight: "$g_{t-k}$ gradiyent vazni", lag: "eskilik k", half: "vaznning yarmi", rest: "qolgan vazn",
      resp: "o‘zgarmas g = 1 gradiyentga javob", window: "oyna 1/(1 − β) =", halfN: "vaznning yarmi oxirgi", grads: "gradiyentda", limit: "uₜ limiti =",
      polyak: "Polyak", nesterov: "Nesterov", rho: "ρ (yaqinlashish tezligi)", hL: "ηL", bAx: "β", xt: "θₜ", gd: "SGD (β = 0)", mom: "Momentum", nes: "Nesterov",
      rhoGD: "ρ SGD =", rhoM: "inersiya bilan ρ =", nGD: "SGD qadamlari:", nM: "inersiya bilan qadamlar:", over: "tebranishsiz", fast: "tez yaqinlashish", under: "tebranishlar so‘nadi", divg: "uzoqlashadi", bound: "ρ = 1 chegarasi", crit: "kritik so‘nish",
      kappa: "Cho‘ziqlik $\\kappa$", rot: "Burilish", etaSM: "$\\eta$ (SGD, Momentum)", rms: "RMSProp", sgd: "SGD", fAfter: "f, qadamdan keyin:", now: "qadam t =",
      start: "start (torting)", tScrub: "Qadam $t$", f: "f(θ)", reach3: "f < 10⁻³ gacha:", fEnd: "3000 dan keyin f:",
      gAbs: "|gₜ|", sqrtv: "√vₜ", sgdStep: "|Δθ| SGD", rmsStep: "|Δθ| RMSProp", boundL: "η/√(1 − β) chegarasi", maxStep: "sakrashdan keyin RMSProp’ning eng katta qadami:", scaleJump: "gradiyent masshtabi ×10, keyin ×0,01",
    },
  }[FV.lang] || {};
  const DEC = FV.lang === "en" ? "." : ",";
  const dn = (s) => String(s).replace(/(\d)\.(\d)/g, "$1" + DEC + "$2");

  // <core> pure functions, no DOM (checked numerically outside the browser)
  // One optimizer step on a parameter vector. kind: sgd | momentum | nesterov | rmsprop.
  function makeOpt(kind, o) {
    let u = null, v = null;
    return function (th, g) {
      const n = th.length, out = new Array(n);
      if (!u) { u = new Array(n).fill(0); v = new Array(n).fill(0); }
      for (let i = 0; i < n; i++) {
        if (kind === "momentum") { u[i] = o.beta * u[i] + g[i]; out[i] = th[i] - o.eta * u[i]; }
        else if (kind === "nesterov") { u[i] = o.beta * u[i] + g[i]; out[i] = th[i] - o.eta * (g[i] + o.beta * u[i]); }
        else if (kind === "rmsprop") { v[i] = o.beta * v[i] + (1 - o.beta) * g[i] * g[i]; out[i] = th[i] - (o.eta * g[i]) / (Math.sqrt(v[i]) + (o.eps != null ? o.eps : 1e-8)); }
        else out[i] = th[i] - o.eta * g[i];
      }
      return out;
    };
  }
  function trajectory(kind, o, grad, th0, n, bound) {
    const step = makeOpt(kind, o), pts = [th0.slice()];
    let th = th0.slice();
    for (let t = 0; t < n; t++) {
      th = step(th, grad(th));
      if (!th.every((v) => Number.isFinite(v) && Math.abs(v) < (bound || 1e6))) { pts.diverged = t + 1; break; }
      pts.push(th);
    }
    return pts;
  }
  // 1D quadratic f = Lθ²/2: θ_t = (1 − ηL)^t θ_0
  function parabola(Lc, eta, x0, n) { const xs = [x0]; for (let t = 0; t < n; t++) xs.push(xs[t] - eta * Lc * xs[t]); return xs; }
  function firstBelow(xs, tol) { for (let i = 0; i < xs.length; i++) if (Math.abs(xs[i]) < tol) return i; return -1; }
  // Heavy ball / Nesterov on f = Lθ²/2 with h = ηL: spectral radius and the sequence θ_t.
  function rhoOf(h, b, nes) {
    const B = nes ? (1 + b) * (1 - h) : 1 + b - h, C = nes ? b * (1 - h) : b, D = B * B - 4 * C;
    if (D < 0) return Math.sqrt(C);
    const s = Math.sqrt(D);
    return Math.max(Math.abs((B + s) / 2), Math.abs((B - s) / 2));
  }
  function momentumSeq(h, b, nes, n) {
    // u_t = βu_{t−1} + g_t, θ_t = θ_{t−1} − η·(u_t | g_t + βu_t); θ in units of θ_0, w = ηu
    let x = 1, w = 0; const xs = [1];
    for (let t = 0; t < n; t++) {
      const g = h * x; w = b * w + g;
      x = x - (nes ? g + b * w : w);
      if (!Number.isFinite(x) || Math.abs(x) > 1e8) break;
      xs.push(x);
    }
    return xs;
  }
  function settle(xs, tol, n) { // first t after which |θ| stays below tol
    let last = -1;
    for (let i = xs.length - 1; i >= 0; i--) if (Math.abs(xs[i]) >= tol) { last = i; break; }
    return xs.length < n + 1 ? -1 : last + 1 < xs.length ? last + 1 : -1;
  }
  // Ill-conditioned quadratic f = (a² + κb²)/2 in coordinates rotated by φ.
  function ravine(kappa, phi) {
    const c = Math.cos(phi), s = Math.sin(phi);
    return {
      f: (x, y) => { const a = c * x + s * y, b = -s * x + c * y; return 0.5 * (a * a + kappa * b * b); },
      grad: ([x, y]) => { const a = c * x + s * y, b = -s * x + c * y, gb = kappa * b; return [c * a - s * gb, s * a + c * gb]; },
      start: [c * -3.4 - s * 0.9, s * -3.4 + c * 0.9],
    };
  }
  const rosen = (x, y) => (1 - x) ** 2 + 100 * (y - x * x) ** 2;
  const rosenGrad = ([x, y]) => [-2 * (1 - x) - 400 * x * (y - x * x), 200 * (y - x * x)];
  // Linear regression data for the mini-batch figure.
  function regData() {
    const r = FV.rng(5), X = [], Y = [];
    for (let i = 0; i < 200; i++) { const x = 1.5 + r.normal(); X.push(x); Y.push(2 * x - 1 + 0.5 * r.normal()); }
    let sx = 0, sxx = 0, sy = 0, sxy = 0, syy = 0;
    for (let i = 0; i < 200; i++) { sx += X[i]; sxx += X[i] * X[i]; sy += Y[i]; sxy += X[i] * Y[i]; syy += Y[i] * Y[i]; }
    const n = 200, det = sxx * n - sx * sx, ws = (sxy * n - sx * sy) / det, bs = (sxx * sy - sx * sxy) / det;
    const loss = (w, b) => 0.5 * (w * w * sxx + 2 * w * b * sx + n * b * b - 2 * w * sxy - 2 * b * sy + syy) / n;
    return { X, Y, n, ws, bs, loss, Lstar: loss(ws, bs) };
  }
  function batchGrad(D, w, b, idx) {
    let gw = 0, gb = 0;
    for (const i of idx) { const e = w * D.X[i] + b - D.Y[i]; gw += e * D.X[i]; gb += e; }
    return [gw / idx.length, gb / idx.length];
  }
  function sgdRun(D, B, eta, epochs, th0) {
    const r = FV.rng(9), perm = D.X.map((_, i) => i), pts = [{ w: th0[0], b: th0[1], e: 0 }];
    let w = th0[0], b = th0[1];
    for (let ep = 0; ep < epochs; ep++) {
      for (let i = perm.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); const t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
      for (let k = 0; k < D.n; k += B) {
        const g = batchGrad(D, w, b, perm.slice(k, k + B));
        w -= eta * g[0]; b -= eta * g[1];
        pts.push({ w, b, e: ep + Math.min(D.n, k + B) / D.n });
      }
    }
    return pts;
  }
  // RMSProp on a scalar gradient stream whose scale jumps: ×1, then ×10 (t ≥ 100), then ×0.1 (t ≥ 200).
  function gradStream(n) {
    const r = FV.rng(3), g = [];
    for (let t = 1; t <= n; t++) { const s = t < 100 ? 1 : t < 200 ? 10 : 0.1; g.push(s * (0.3 + r.normal())); }
    return g;
  }
  function rmsStream(g, beta, eta) {
    let v = 0; const sv = [], st = [];
    g.forEach((x) => { v = beta * v + (1 - beta) * x * x; sv.push(Math.sqrt(v)); st.push((eta * Math.abs(x)) / (Math.sqrt(v) + 1e-8)); });
    return { sv, st };
  }
  FV.pageCore = Object.assign(FV.pageCore || {}, { sgd: { makeOpt, trajectory, parabola, firstBelow, rhoOf, momentumSeq, settle, ravine, rosen, rosenGrad, regData, sgdRun, batchGrad, gradStream, rmsStream } });
  // </core>

  const COL = { sgd: "ink", momentum: "blue", nesterov: "blue", rmsprop: "teal" };
  const NAME = { sgd: "SGD", momentum: "Momentum", nesterov: "Nesterov", rmsprop: "RMSProp" };
  // A loss heat map that keeps the low region neutral (theme colour) and warms up towards high loss.
  function lossHeat(p, f, lo, hi) {
    // log10 f from lo to hi is mapped onto the neutral → warm half of the diverging map, up to 70% of it
    const a = Math.log10(lo), b = Math.log10(hi), span = (b - a) / 0.35;
    p.heat((x, y) => Math.log10(Math.max(f(x, y), lo)), { cmap: "diverging", z: [a - span / 2, a + span / 2], res: 4, alpha: 0.5 });
  }
  const texNum = (s) => String(s).replace(/\./g, FV.lang === "en" ? "." : "{,}");
  const geo = (a, b, n) => Array.from({ length: n }, (_, i) => a * Math.pow(b / a, i / (n - 1)));
  if (!FV.widget) return;

  // 1. Gradient descent on a 1D parabola: convergence, oscillation, divergence.
  FV.widget("sgd-parabola", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-3.2, 3.2], y: [-0.6, 9.6], xLabel: "θ", yLabel: L.parab, aspect: 0.46 });
    const q = new FV.Plot(w.stage, { x: [0, 30], y: [1e-5, 1e3], yType: "log", xLabel: L.step + " t", yLabel: "|θₜ|", aspect: 0.26, minHeight: 190, maxHeight: 250 });
    const se = FV.ui.slider({ label: L.eta, min: 0.01, max: 1.2, step: 0.01, value: cfg.eta != null ? cfg.eta : 0.3, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sl = FV.ui.slider({ label: L.curv, min: 0.5, max: 4, step: 0.1, value: cfg.L != null ? cfg.L : 2, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    w.controls.append(se.el, sl.el);
    const ro = FV.ui.readout(w.readout, [{ key: "h", label: L.etaL }, { key: "q", label: L.mult }, { key: "r", label: L.regime, c: "orange" }, { key: "n", label: L.reach }]);
    const f = (x) => 0.5 * sl.value * x * x;
    let x0 = cfg.x0 != null ? cfg.x0 : 2;
    const hd = p.handle(x0, f(x0), { c: "ink", label: "θ₀", onDrag: (x) => { x0 = x; return [x, f(x)]; }, onChange: () => draw() });
    function draw() {
      const Lc = sl.value, eta = se.value, h = eta * Lc, xs = parabola(Lc, eta, x0, 30);
      p.clear();
      p.vline(0, {});
      p.fn(f, { c: "faint", w: 2.2 });
      for (let t = 0; t < 30; t++) {
        const a = xs[t], b = xs[t + 1];
        if (Math.abs(b) > 3.3 || f(b) > 9.7) { if (Math.abs(a) <= 3.3) p.arrow(a, f(a), FV.clamp(b, -3.3, 3.3), Math.min(f(b), 9.7), { c: "ink", w: 1.4, head: 7 }); break; }
        if (Math.abs(a - b) < 1e-3) break;
        p.arrow(a, f(a), b, f(b), { c: "ink", w: 1.4, head: 7 });
      }
      xs.slice(1, 31).forEach((x) => { if (Math.abs(x) <= 3.2 && f(x) <= 9.6) p.dot(x, f(x), { c: "ink", r: 3 }); });
      ["θ₀", "θ₁", "θ₂"].forEach((s, i) => { const x = xs[i]; if (Math.abs(x) <= 3.1 && f(x) < 9.2 && (i === 0 || Math.abs(x - xs[i - 1]) > 0.25)) p.text(x, f(x), s, { dx: x >= 0 ? 10 : -10, dy: -8, anchor: x >= 0 ? "start" : "end" }); });
      hd.set(x0, f(x0));
      q.clear();
      q.hline(0.01, { c: "guide" });
      q.text(30, 0.01, "0" + DEC + "01", { anchor: "end", dy: -6, c: "faint" });
      if (Math.abs(1 - h) > 1e-9) q.fn((t) => Math.abs(x0) * Math.pow(Math.abs(1 - h), t), { c: "guide", w: 1.4, dash: "5 4" });
      const pts = xs.map((x, t) => [t, Math.abs(x)]).filter((d) => d[1] > 1e-6);
      q.path(pts, { c: "ink", w: 1.6 });
      pts.forEach((d) => q.dot(d[0], d[1], { c: "ink", r: 3 }));
      p.legend([{ label: "f(θ)", c: "faint" }, { label: L.sgdPath, c: "ink" }]);
      q.legend([{ label: "|θₜ|", c: "ink" }, { label: L.theory, c: "guide", dash: true }]);
      const reg = Math.abs(h - 1) < 1e-9 ? L.one : h < 1 ? L.mono : Math.abs(h - 2) < 1e-9 ? L.edge : h < 2 ? L.osc : L.div;
      const nb = Math.abs(x0) < 0.01 ? 0 : h >= 2 - 1e-9 ? -1 : firstBelow(parabola(Lc, eta, x0, 5000), 0.01);
      ro.set("h", FV.fmt(h, 2)); ro.set("q", FV.fmt(1 - h, 2)); ro.set("r", reg); ro.set("n", nb < 0 ? "—" : String(nb));
    }
    p.onresize = draw; q.onresize = draw; draw();
  });

  // 2. Mini-batches: the stochastic gradient is the full gradient plus noise that shrinks with B.
  FV.widget("sgd-minibatch", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const D = regData(), E = 8, th0 = [-1, 2.2];
    const a = new FV.Plot(FV.col(w.stage), { x: [-1.6, 3.4], y: [-3, 3], xLabel: "w", yLabel: "b", aspect: 0.95, title: "L(w, b)" });
    const c = new FV.Plot(FV.col(w.stage), { x: [0, E], y: [1e-5, 30], yType: "log", xLabel: L.epoch, yLabel: "L − L*", aspect: 0.95, title: "L − L*" });
    let eta = cfg.eta || 0.05, tau = E;
    const Bs = [1, 10, 50, 200];
    const sb = FV.ui.seg({ label: L.batch, value: cfg.B || 10, options: Bs.map((b) => ({ value: b, label: b === 200 ? "200 (" + L.full + ")" : String(b) })), onchange: () => { runs = null; draw(); } });
    const se = FV.ui.slider({ label: L.eta, min: 0.005, max: 0.2, step: 0.005, value: eta, fmt: (v) => FV.fmt(v, 3), oninput: (v) => { eta = v; runs = null; draw(); } });
    const pl = FV.ui.player({ interval: 60, onstep() { tau = Math.min(E, +(tau + 0.1).toFixed(4)); draw(); return tau < E; }, onreset() { tau = 0; draw(); } });
    w.controls.append(sb.el, se.el, pl.el);
    const ro = FV.ui.readout(w.readout, [{ key: "u", label: L.upd }, { key: "e", label: L.epochs }, { key: "l", label: L.excess, c: "ink" }, { key: "s", label: L.noise }]);
    let runs = null;
    const lossF = (x, y) => D.loss(x, y) - D.Lstar;
    function draw() {
      if (!runs) runs = Object.fromEntries(Bs.map((b) => [b, sgdRun(D, b, eta, E, th0)]));
      const B = sb.value, run = runs[B], shown = run.filter((d) => d.e <= tau + 1e-9), cur = shown[shown.length - 1];
      a.clear();
      lossHeat(a, lossF, 1e-3, 40);
      a.contours(lossF, geo(0.01, 20, 8), { c: "ink", w: 1, opacity: 0.28 });
      const full = runs[200].filter((d) => d.e <= tau + 1e-9);
      if (B !== 200) { a.path(full.map((d) => [d.w, d.b]), { c: "faint", w: 1.4, dash: "4 4" }); full.forEach((d) => a.dot(d.w, d.b, { c: "faint", r: 2.5 })); }
      a.path(shown.map((d) => [d.w, d.b]), { c: "ink", w: B === 1 ? 1 : 1.6, opacity: B === 1 ? 0.75 : 1 });
      // cloud of possible next steps from the current point
      const r = FV.rng(100 + shown.length), idx = D.X.map((_, i) => i), gF = batchGrad(D, cur.w, cur.b, idx);
      let s2 = 0;
      for (let k = 0; k < 40; k++) {
        for (let i = 0; i < B; i++) { const j = i + Math.floor(r() * (D.n - i)); const t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
        const g = batchGrad(D, cur.w, cur.b, idx.slice(0, B)), px = cur.w - eta * g[0], py = cur.b - eta * g[1];
        s2 += (eta * (g[0] - gF[0])) ** 2 + (eta * (g[1] - gF[1])) ** 2;
        a.dot(px, py, { c: "orange", r: 2.4 });
      }
      a.arrow(cur.w, cur.b, cur.w - eta * gF[0], cur.b - eta * gF[1], { c: "ink", w: 1.6, head: 7 });
      a.dot(cur.w, cur.b, { c: "ink", r: 4.5 });
      a.dot(D.ws, D.bs, { hollow: true, c: "ink", r: 5 });
      a.text(D.ws, D.bs, "θ*", { dx: 9, dy: 14 });
      a.legend([{ label: "SGD, B = " + B, c: "ink" }, { label: L.fullGD, c: "faint", dash: true }, { label: L.cloud, c: "orange", dot: true }]);
      c.clear();
      Bs.forEach((b) => { if (b !== B) c.path(runs[b].filter((d) => d.e <= tau + 1e-9).map((d) => [d.e, Math.max(1e-5, lossF(d.w, d.b))]), { c: "guide", w: 1, opacity: 0.8 }); });
      Bs.forEach((b) => { if (b !== B) { const last = runs[b][runs[b].length - 1]; if (tau >= E - 1e-9) c.text(E, Math.max(1.3e-5, lossF(last.w, last.b)), "B = " + b, { anchor: "end", dy: b === 50 && B !== 200 ? 14 : -5, c: "faint" }); } });
      c.path(shown.map((d) => [d.e, Math.max(1e-5, lossF(d.w, d.b))]), { c: "ink", w: 2 });
      c.legend([{ label: L.selB + " = " + B, c: "ink" }, { label: L.otherB, c: "guide" }]);
      ro.set("u", String(D.n / B)); ro.set("e", FV.fmt(cur.e, 1)); ro.set("l", FV.num(lossF(cur.w, cur.b), 2)); ro.set("s", FV.num(Math.sqrt(s2 / 40), 2));
    }
    a.onresize = draw; c.onresize = draw; draw();
  });

  // 3. Momentum as an exponential memory of past gradients.
  FV.widget("sgd-ema", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-0.8, 39.8], y: [0, 1.05], xLabel: L.lag, yLabel: "", aspect: 0.7, title: L.weight });
    const b = new FV.Plot(FV.col(w.stage), { x: [0, 60], y: [0, 11], xLabel: L.step + " t", yLabel: "uₜ", aspect: 0.7, title: L.resp });
    const sb = FV.ui.slider({ label: L.beta, min: 0, max: 0.99, step: 0.01, value: cfg.beta != null ? cfg.beta : 0.9, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sf = FV.ui.seg({ label: L.form, value: "heavy", options: [{ value: "heavy", label: L.heavy }, { value: "ema", label: L.ema }], onchange: draw });
    w.controls.append(sb.el, sf.el);
    const ro = FV.ui.readout(w.readout, [{ key: "w", label: L.window, c: "blue" }, { key: "h", label: L.halfN }, { key: "l", label: L.limit }]);
    function draw() {
      const be = sb.value, ema = sf.value === "ema", k0 = ema ? 1 - be : 1, lim = ema ? 1 : 1 / (1 - be);
      const nHalf = be > 0 ? Math.ceil(Math.log(0.5) / Math.log(be) - 1e-12) : 1;
      a.setDomain(null, [0, k0 * 1.08]);
      a.clear();
      for (let k = 0; k < 40; k++) a.bar(k, k0 * Math.pow(be, k), { c: "blue", width: 0.72, opacity: k < nHalf ? 0.9 : 0.32 });
      a.legend([{ label: L.half, c: "blue", box: true }, { label: L.rest, c: "blue", box: true }]);
      const lg = a.legendEl && a.legendEl.children[1]; if (lg) lg.firstChild.style.opacity = "0.35";
      b.setDomain(null, [0, ema ? 1.15 : Math.max(1.2, lim * 1.1)]);
      b.clear();
      b.hline(lim, { c: "blue", dash: "5 4", w: 1.2, opacity: 0.7 });
      b.fn((t) => (ema ? 1 - Math.pow(be, t) : (1 - Math.pow(be, t)) / (1 - be)), { c: "blue", w: 2.4, from: 0 });
      for (let t = 1; t <= 60; t += 1) if (t <= 12 || t % 4 === 0) b.dot(t, ema ? 1 - Math.pow(be, t) : (1 - Math.pow(be, t)) / (1 - be), { c: "blue", r: 2.6 });
      b.text(60, lim, (ema ? "1" : "1/(1 − β) = " + FV.num(lim, 3)), { anchor: "end", dy: -7, c: "blue" });
      ro.set("w", FV.num(1 / (1 - be), 3)); ro.set("h", nHalf + " " + L.grads); ro.set("l", FV.num(lim, 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 4. Stability map of heavy-ball / Nesterov momentum on one quadratic direction.
  FV.widget("sgd-momentum", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [0.01, 5], xType: "log", y: [0, 0.99], xLabel: "ηL", yLabel: "β", aspect: 0.85, title: L.rho });
    const b = new FV.Plot(FV.col(w.stage), { x: [0, 120], y: [-1.1, 1.1], xLabel: L.step + " t", yLabel: "θₜ / θ₀", aspect: 0.85, title: "θₜ" });
    let h = cfg.h || 0.04, be = cfg.beta != null ? cfg.beta : 0.9;
    const sm = FV.ui.seg({ value: "polyak", options: [{ value: "polyak", label: L.polyak }, { value: "nesterov", label: L.nesterov }], onchange: draw });
    w.controls.append(sm.el);
    const ro = FV.ui.readout(w.readout, [{ key: "hb", label: "ηL, β =" }, { key: "r0", label: L.rhoGD }, { key: "r1", label: L.rhoM, c: "blue" }, { key: "n0", label: L.nGD }, { key: "n1", label: L.nM, c: "blue" }, { key: "g", label: L.regime }]);
    const hd = a.handle(h, be, { c: "blue", onDrag: (x, y) => { h = FV.clamp(x, 0.01, 5); be = FV.clamp(y, 0, 0.99); return [h, be]; }, onChange: () => draw(false) });
    let heatKey = "";
    function draw(full = true) {
      const nes = sm.value === "nesterov";
      if (full !== false || heatKey !== sm.value) {
        heatKey = sm.value;
        a.clear();
        a.heat((x, y) => { const r = rhoOf(x, y, nes); return r < 1 ? 0.5 - 0.5 * FV.clamp((1 - r) / 0.5, 0, 1) : 0.5 + 0.5 * FV.clamp(r - 1, 0, 1); }, { cmap: "diverging", z: [0, 1], res: 3, alpha: 0.85 });
        a.contours((x, y) => rhoOf(x, y, nes), [0.8, 0.9, 0.95], { c: "ink", w: 1, opacity: 0.35 });
        a.contours((x, y) => rhoOf(x, y, nes), [1], { c: "ink", w: 2, opacity: 0.9 });
        const crit = (sgn) => FV.linspace(0, 0.99, 120).map((y) => { const s = Math.sqrt(y); return nes ? [sgn < 0 ? ((1 - y) / (1 + y)) ** 2 : y > 0 ? 1 : NaN, y] : [(1 + sgn * s) ** 2, y]; }).filter((d) => d[0] >= 0.01 && d[0] <= 5);
        a.path(crit(-1), { c: "guide", w: 1.6, dash: "6 4" }); a.path(crit(1), { c: "guide", w: 1.6, dash: "6 4" });
        a.legend([{ label: L.fast, c: "blue", box: true }, { label: L.divg, c: "red", box: true }, { label: L.bound, c: "ink" }, { label: "ρ = 0" + DEC + "8; 0" + DEC + "9; 0" + DEC + "95", c: "faint" }, { label: L.crit, c: "guide", dash: true }]);
      }
      hd.set(h, be);
      const xs0 = momentumSeq(h, 0, false, 2000), xs1 = momentumSeq(h, be, nes, 2000);
      b.clear();
      b.hline(0, { c: "guide", dash: false });
      b.path(xs0.slice(0, 121).map((x, t) => [t, FV.clamp(x, -5, 5)]), { c: "ink", w: 1.8 });
      b.path(xs1.slice(0, 121).map((x, t) => [t, FV.clamp(x, -5, 5)]), { c: "blue", w: 2.2 });
      b.legend([{ label: L.gd, c: "ink" }, { label: (nes ? L.nes : L.mom) + ", β = " + FV.fmt(be, 2), c: "blue" }]);
      const r0 = rhoOf(h, 0, false), r1 = rhoOf(h, be, nes), n0 = settle(xs0, 1e-3, 2000), n1 = settle(xs1, 1e-3, 2000);
      const B = nes ? (1 + be) * (1 - h) : 1 + be - h, C = nes ? be * (1 - h) : be;
      ro.set("hb", FV.fmt(h, 3) + "; " + FV.fmt(be, 2)); ro.set("r0", FV.fmt(r0, 3)); ro.set("r1", FV.fmt(r1, 3));
      ro.set("n0", n0 < 0 ? "—" : String(n0)); ro.set("n1", n1 < 0 ? "—" : String(n1));
      ro.set("g", r1 >= 1 ? L.divg : B * B - 4 * C < 0 ? L.under : L.over);
    }
    // Nesterov: complex roots for ((1 − β)/(1 + β))² < ηL < 1, real ones outside.
    a.onresize = () => draw(true); b.onresize = () => draw(true); draw(true);
  });

  // 5. An ill-conditioned valley in 2D and 3D: SGD, Momentum, RMSProp.
  FV.widget("sgd-ravine", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const c1 = FV.col(w.stage), c2 = FV.col(w.stage);
    let R = ravine(cfg.kappa || 100, 0);
    const a = new FV.Plot(c1, { x: [-4, 4], y: [-2.5, 2.5], xLabel: "θ₁", yLabel: "θ₂", equal: true, title: L.f });
    const lf = (x, y) => Math.log1p(R.f(x, y));
    const s3 = new FV.Surface(c2, { f: lf, x: [-4, 4], y: [-2.5, 2.5], n: 40, labels: { x: "θ₁", y: "θ₂", z: "ln(1 + f)" }, azimuth: -1.3, elevation: 0.7, aspect: 0.8, cmap: "diverging", cmapT: (t) => 0.5 + 0.36 * t, title: "ln(1 + f)" });
    const sk = FV.ui.slider({ label: L.kappa, min: 1, max: 100, step: 1, value: cfg.kappa || 100, fmt: (v) => String(v), oninput: () => { rebuild(); } });
    const sr = FV.ui.seg({ label: L.rot, value: 0, options: [{ value: 0, label: "0°" }, { value: 45, label: "45°" }], onchange: () => rebuild() });
    const se = FV.ui.slider({ label: L.etaSM, min: 0.002, max: 0.04, step: 0.001, value: cfg.eta || 0.018, fmt: (v) => FV.fmt(v, 3), oninput: () => rebuild(true) });
    const sb = FV.ui.slider({ label: L.beta, min: 0, max: 0.99, step: 0.01, value: cfg.beta != null ? cfg.beta : 0.9, fmt: (v) => FV.fmt(v, 2), oninput: () => rebuild(true) });
    const N = 100, ETA_R = 0.1;
    let t = N, paths = null;
    const pl = FV.ui.player({ interval: 70, onstep() { t = Math.min(N, t + 1); draw(); return t < N; }, onreset() { t = 0; draw(); } });
    w.controls.append(sk.el, sr.el, se.el, sb.el, pl.el);
    const ro = FV.ui.readout(w.readout, [{ key: "t", label: L.now }, { key: "sgd", label: "f SGD =", c: "ink" }, { key: "momentum", label: "f Momentum =", c: "blue" }, { key: "rmsprop", label: "f RMSProp =", c: "teal" }]);
    w.note.append(FV.rich("RMSProp: $\\eta=" + texNum("0.1") + "$, $\\beta=" + texNum("0.9") + "$. " + "SGD, Momentum: $\\eta$ " + (FV.lang === "ru" ? "и" : FV.lang === "uz" ? "va" : "and") + " $\\beta$ " + (FV.lang === "ru" ? "— ползунками." : FV.lang === "uz" ? "— slayderlar bilan." : "from the sliders.")));
    function rebuild(keepF) {
      R = ravine(sk.value, (sr.value * Math.PI) / 180);
      paths = null;
      if (!keepF) s3.setF(lf);
      draw();
    }
    function draw() {
      if (!paths) {
        const eta = se.value, be = sb.value;
        paths = {
          sgd: trajectory("sgd", { eta }, R.grad, R.start, N, 50),
          momentum: trajectory("momentum", { eta, beta: be }, R.grad, R.start, N, 50),
          rmsprop: trajectory("rmsprop", { eta: ETA_R, beta: 0.9 }, R.grad, R.start, N, 50),
        };
      }
      a.clear();
      lossHeat(a, R.f, 0.05, 200);
      a.contours(R.f, geo(0.05, 120, 9), { c: "ink", w: 1, opacity: 0.28 });
      const list = [];
      ["sgd", "momentum", "rmsprop"].forEach((k) => {
        const P = paths[k].slice(0, t + 1);
        a.path(P, { c: COL[k], w: k === "sgd" ? 1.6 : 2 });
        const e = P[P.length - 1]; a.dot(e[0], e[1], { c: COL[k], r: 4 });
        list.push({ pts: P.map((q) => [q[0], q[1], lf(q[0], q[1])]), c: COL[k], w: 2.4 });
        const fv = R.f(e[0], e[1]);
        ro.set(k, paths[k].diverged && t >= paths[k].length - 1 ? L.div : FV.num(fv, 2));
      });
      a.dot(R.start[0], R.start[1], { c: "ink", hollow: true, r: 5 });
      a.dot(0, 0, { c: "ink", r: 3 });
      a.legend([{ label: "SGD", c: "ink" }, { label: "Momentum", c: "blue" }, { label: "RMSProp", c: "teal" }]);
      s3.setPoints([{ x: 0, y: 0, z: 0, c: "ink", r: 4 }]);
      s3.setPaths(list);
      ro.set("t", String(t));
    }
    a.onresize = draw; draw();
  });

  // 6. Rosenbrock's banana valley: whole runs, a draggable start and the loss curves.
  FV.widget("sgd-rosenbrock", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-2, 2], y: [-1, 3], xLabel: "x", yLabel: "y", equal: true, title: "f = (1 − x)² + 100(y − x²)²" });
    const b = new FV.Plot(FV.col(w.stage), { x: [0, 3150], y: [1e-12, 1e4], yType: "log", xLabel: L.step + " t", yLabel: "f", aspect: 0.95, title: L.f });
    const N = 3000, OPT = { sgd: { eta: 0.001 }, momentum: { eta: 0.001, beta: 0.9 }, rmsprop: { eta: 0.01, beta: 0.9 } };
    let st = cfg.start ? cfg.start.slice() : [-1.5, 2], runs = null;
    const sT = FV.ui.slider({ label: L.tScrub, min: 0, max: N, step: 10, value: N, fmt: (v) => String(v), oninput: draw });
    w.controls.append(sT.el);
    const ro = FV.ui.readout(w.readout, [{ key: "sgd", label: "SGD:", c: "ink" }, { key: "momentum", label: "Momentum:", c: "blue" }, { key: "rmsprop", label: "RMSProp:", c: "teal" }]);
    w.note.append(FV.rich("SGD: $\\eta=" + texNum("0.001") + "$ · Momentum: $\\eta=" + texNum("0.001") + "$, $\\beta=" + texNum("0.9") + "$ · RMSProp: $\\eta=" + texNum("0.01") + "$, $\\beta=" + texNum("0.9") + "$. " + (FV.lang === "ru" ? "В строке — f при выбранном t и число шагов до f < 10⁻³." : FV.lang === "uz" ? "Qatorda — tanlangan t dagi f va f < 10⁻³ gacha qadamlar soni." : "The row shows f at the chosen t and the number of steps to f < 10⁻³.")));
    const hd = a.handle(st[0], st[1], { c: "ink", onDrag: (x, y) => { st = [x, y]; return [x, y]; }, onChange: () => { runs = null; draw(); } });
    function draw() {
      if (!runs) runs = Object.fromEntries(Object.keys(OPT).map((k) => [k, trajectory(k, OPT[k], rosenGrad, st, N, 1e3)]));
      const T = sT.value;
      a.clear();
      lossHeat(a, rosen, 0.05, 2500);
      a.contours((x, y) => Math.log10(rosen(x, y) + 1e-9), [-1, 0, 0.5, 1, 1.5, 2, 2.5, 3], { c: "ink", w: 1, opacity: 0.25 });
      a.dot(1, 1, { c: "ink", hollow: true, r: 5 }); a.text(1, 1, "(1" + (FV.lang === "en" ? ", " : "; ") + "1)", { dx: 10, dy: 4 });
      b.clear();
      b.hline(1e-3, { c: "guide" });
      ["rmsprop", "momentum", "sgd"].forEach((k) => {
        const P = runs[k], upto = P.slice(0, T + 1);
        a.path(upto, { c: COL[k], w: k === "rmsprop" ? 3 : k === "momentum" ? 2.2 : 1.6 });
        const e = upto[upto.length - 1]; a.dot(e[0], e[1], { c: COL[k], r: 4 });
        const fs = P.map((q) => rosen(q[0], q[1]));
        b.path(fs.map((v, i) => [i, Math.max(v, 1e-12)]).filter((d, i) => i % 5 === 0 || i === fs.length - 1), { c: COL[k], w: 1.8 });
        const fe = fs[Math.min(T, fs.length - 1)];
        b.dot(Math.min(T, fs.length - 1), Math.max(fe, 1e-12), { c: COL[k], r: 4 });
        const hit = fs.findIndex((v) => v < 1e-3);
        ro.set(k, (P.diverged && T >= P.length - 1 ? L.div : "f = " + FV.num(fe, 2)) + " · " + L.reach3 + " " + (hit < 0 ? "—" : hit));
      });
      b.vline(T, { c: "guide" });
      hd.set(st[0], st[1]);
      a.legend([{ label: "SGD", c: "ink" }, { label: "Momentum", c: "blue" }, { label: "RMSProp", c: "teal" }, { label: L.start, c: "ink", dot: true }]);
      b.legend([{ label: "f = 10⁻³", c: "guide", dash: true }]);
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 7. RMSProp adapts the step to the recent gradient scale.
  FV.widget("sgd-rmsprop", (el, cfg) => {
    const w = FV.shell(el, {});
    const n = 300, eta = 0.01, G = gradStream(n);
    const a = new FV.Plot(w.stage, { x: [0, n], y: [1e-3, 1e2], yType: "log", xLabel: L.step + " t", yLabel: "|gₜ|, √vₜ", aspect: 0.3, minHeight: 210, maxHeight: 280, title: L.scaleJump });
    const b = new FV.Plot(w.stage, { x: [0, n], y: [1e-5, 1], yType: "log", xLabel: L.step + " t", yLabel: "|Δθₜ|", aspect: 0.3, minHeight: 210, maxHeight: 280 });
    const sb = FV.ui.slider({ label: L.beta, min: 0.5, max: 0.999, step: 0.001, value: cfg.beta || 0.9, fmt: (v) => FV.fmt(v, 3), oninput: draw });
    w.controls.append(sb.el);
    const ro = FV.ui.readout(w.readout, [{ key: "w", label: L.window }, { key: "m", label: L.maxStep, c: "teal" }, { key: "b", label: L.boundL + " =" }]);
    function draw() {
      const be = sb.value, R = rmsStream(G, be, eta);
      a.clear(); b.clear();
      [100, 200].forEach((x) => { a.vline(x, {}); b.vline(x, {}); });
      G.forEach((g, i) => a.dot(i + 1, Math.max(Math.abs(g), 1e-3), { c: "faint", r: 1.8 }));
      a.path(R.sv.map((v, i) => [i + 1, v]), { c: "teal", w: 2.4 });
      a.legend([{ label: L.gAbs, c: "faint", dot: true }, { label: L.sqrtv, c: "teal" }]);
      const bound = eta / Math.sqrt(1 - be);
      b.hline(bound, { c: "teal", w: 1.2, dash: "5 4" });
      b.path(G.map((g, i) => [i + 1, Math.max(eta * Math.abs(g), 1e-5)]), { c: "ink", w: 1.2, opacity: 0.75 });
      b.path(R.st.map((s, i) => [i + 1, Math.max(s, 1e-5)]), { c: "teal", w: 1.8 });
      b.legend([{ label: L.sgdStep + " (η = 0" + DEC + "01)", c: "ink" }, { label: L.rmsStep, c: "teal" }, { label: L.boundL, c: "teal", dash: true }]);
      const mx = Math.max(...R.st.slice(99, 110));
      ro.set("w", FV.num(1 / (1 - be), 3)); ro.set("m", FV.num(mx, 3)); ro.set("b", FV.num(bound, 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });
})();
