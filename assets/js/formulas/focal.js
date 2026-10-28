/* Widgets of the formula page "Focal Loss". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      pt: "p_t — вероятность правильного класса", ptShort: "p_t", loss: "потеря", gamma: "Фокусировка $\\gamma$", ptS: "Уверенность $p_t$",
      ce: "CE (γ = 0)", fl: "FL, выбранная γ", family: "γ = 0,5; 1; 2; 5", easyZone: "хорошо классифицированные (p_t > 0,5)",
      ceV: "$\\mathrm{CE}=-\\ln p_t$ =", factor: "$(1-p_t)^\\gamma$ =", flV: "FL =", ratio: "FL меньше CE в",
      times: " раз", factorT: "Модулирующий множитель $(1-p_t)^\\gamma$", logT: "Потери в логарифмической шкале",
      gradT: "|∂L/∂z_t| — сила градиента", gMax: "максимум FL:", gCross: "FL сильнее CE при $p_t<$", gAt: "при $p_t=0{,}9$: FL / CE =",
      flGrad: "FL, выбранная γ", ceGrad: "CE: 1 − p_t", maxDot: "максимум", crossDot: "пересечение с CE",
      surfT: "$\\mathrm{FL}(p_t,\\gamma)$ в 3D", decayT: "FL при росте γ (лог. шкала)", sliceG: "срез по γ", sliceP: "срез по p_t",
      decay: "FL(γ) при выбранном p_t", others: "p_t = 0,1; 0,5; 0,9; 0,99",
      shareT: "Откуда берётся суммарная потеря", binT: "Доля потерь по корзинам $p_t$", posC: "позитивы", hardN: "трудные негативы", easyN: "лёгкие негативы (p_t ≥ 0,9)",
      ratioS: "Негативов на один позитив", easyCnt: "лёгких негативов среди примеров:", easyCE: "их доля потерь: CE", posShare: "доля позитивов: CE", flShort: "FL",
      piS: "Доля позитивов $\\pi$", alphaS: "Вес позитивов $\\alpha$", pAxis: "постоянный прогноз p", jAxis: "средняя потеря / минимум",
      ceOpt: "CE: минимум при p = π", flOpt: "FL с α: минимум", pCe: "p* для CE =", pFl: "p* для FL =", zFl: "логит z* для FL =", bInit: "инициализация b = ln(π/(1−π)) =",
      x1: "x₁", x2: "x₂", ceTitle: "CE", flTitle: "Focal loss", neg: "негативы (400)", pos: "позитивы (20)", bound: "граница p = 0,5",
      step: "шаг", easyG: "доля градиента от лёгких ($p_t>0{,}9$): CE", tp: "найдено позитивов (из 20): CE", fp: "ложных тревог: CE", size: "размер точки ∝ |∂L/∂z|",
    },
    en: {
      pt: "p_t — probability of the correct class", ptShort: "p_t", loss: "loss", gamma: "Focusing $\\gamma$", ptS: "Confidence $p_t$",
      ce: "CE (γ = 0)", fl: "FL, chosen γ", family: "γ = 0.5, 1, 2, 5", easyZone: "well-classified (p_t > 0.5)",
      ceV: "$\\mathrm{CE}=-\\ln p_t$ =", factor: "$(1-p_t)^\\gamma$ =", flV: "FL =", ratio: "FL is smaller than CE by",
      times: "×", factorT: "The modulating factor $(1-p_t)^\\gamma$", logT: "Losses on a log scale",
      gradT: "|∂L/∂z_t| — the gradient strength", gMax: "FL maximum:", gCross: "FL beats CE for $p_t<$", gAt: "at $p_t=0.9$: FL / CE =",
      flGrad: "FL, chosen γ", ceGrad: "CE: 1 − p_t", maxDot: "maximum", crossDot: "crossing with CE",
      surfT: "$\\mathrm{FL}(p_t,\\gamma)$ in 3D", decayT: "FL as γ grows (log scale)", sliceG: "slice along γ", sliceP: "slice along p_t",
      decay: "FL(γ) at the chosen p_t", others: "p_t = 0.1, 0.5, 0.9, 0.99",
      shareT: "Where the total loss comes from", binT: "Share of the loss by $p_t$ bins", posC: "positives", hardN: "hard negatives", easyN: "easy negatives (p_t ≥ 0.9)",
      ratioS: "Negatives per positive", easyCnt: "easy negatives among examples:", easyCE: "their share of the loss: CE", posShare: "share of positives: CE", flShort: "FL",
      piS: "Share of positives $\\pi$", alphaS: "Weight of positives $\\alpha$", pAxis: "constant prediction p", jAxis: "mean loss / minimum",
      ceOpt: "CE: minimum at p = π", flOpt: "FL with α: minimum", pCe: "p* for CE =", pFl: "p* for FL =", zFl: "logit z* for FL =", bInit: "initialization b = ln(π/(1−π)) =",
      x1: "x₁", x2: "x₂", ceTitle: "CE", flTitle: "Focal loss", neg: "negatives (400)", pos: "positives (20)", bound: "boundary p = 0.5",
      step: "step", easyG: "gradient share of easy ones ($p_t>0.9$): CE", tp: "positives found (of 20): CE", fp: "false alarms: CE", size: "dot size ∝ |∂L/∂z|",
    },
    uz: {
      pt: "p_t — to‘g‘ri sinf ehtimolligi", ptShort: "p_t", loss: "yo‘qotish", gamma: "Fokuslash $\\gamma$", ptS: "Ishonch $p_t$",
      ce: "CE (γ = 0)", fl: "FL, tanlangan γ", family: "γ = 0,5; 1; 2; 5", easyZone: "yaxshi klassifikatsiyalangan (p_t > 0,5)",
      ceV: "$\\mathrm{CE}=-\\ln p_t$ =", factor: "$(1-p_t)^\\gamma$ =", flV: "FL =", ratio: "FL CE dan kichik:",
      times: " marta", factorT: "Modulyatsiyalovchi ko‘paytuvchi $(1-p_t)^\\gamma$", logT: "Logarifmik shkaladagi yo‘qotishlar",
      gradT: "|∂L/∂z_t| — gradiyent kuchi", gMax: "FL maksimumi:", gCross: "FL CE dan kuchli, agar $p_t<$", gAt: "$p_t=0{,}9$ da: FL / CE =",
      flGrad: "FL, tanlangan γ", ceGrad: "CE: 1 − p_t", maxDot: "maksimum", crossDot: "CE bilan kesishish",
      surfT: "$\\mathrm{FL}(p_t,\\gamma)$ 3D’da", decayT: "γ o‘sganda FL (log. shkala)", sliceG: "γ bo‘yicha kesim", sliceP: "p_t bo‘yicha kesim",
      decay: "tanlangan p_t da FL(γ)", others: "p_t = 0,1; 0,5; 0,9; 0,99",
      shareT: "Umumiy yo‘qotish qayerdan keladi", binT: "$p_t$ savatlari bo‘yicha yo‘qotish ulushi", posC: "pozitivlar", hardN: "qiyin negativlar", easyN: "oson negativlar (p_t ≥ 0,9)",
      ratioS: "Bitta pozitivga negativlar", easyCnt: "misollar orasida oson negativlar:", easyCE: "ularning yo‘qotish ulushi: CE", posShare: "pozitivlar ulushi: CE", flShort: "FL",
      piS: "Pozitivlar ulushi $\\pi$", alphaS: "Pozitivlar vazni $\\alpha$", pAxis: "o‘zgarmas bashorat p", jAxis: "o‘rtacha yo‘qotish / minimum",
      ceOpt: "CE: minimum p = π da", flOpt: "α li FL: minimum", pCe: "CE uchun p* =", pFl: "FL uchun p* =", zFl: "FL uchun z* logit =", bInit: "boshlang‘ich b = ln(π/(1−π)) =",
      x1: "x₁", x2: "x₂", ceTitle: "CE", flTitle: "Focal loss", neg: "negativlar (400)", pos: "pozitivlar (20)", bound: "chegara p = 0,5",
      step: "qadam", easyG: "osonlar gradiyent ulushi ($p_t>0{,}9$): CE", tp: "topilgan pozitivlar (20 dan): CE", fp: "soxta signallar: CE", size: "nuqta o‘lchami ∝ |∂L/∂z|",
    },
  }[FV.lang] || {};

  const sig = FV.sigmoid;
  const FL = (p, g) => -Math.pow(1 - p, g) * Math.log(p);
  // |∂FL/∂z_t| for the logit z_t of the correct class: (1 − p)^γ (1 − p − γ p ln p)
  const G = (p, g) => Math.pow(1 - p, g) * (1 - p - (g ? g * p * Math.log(p) : 0));
  const pct = (v) => FV.fmt(100 * v, 1) + "%";
  const FAMILY = [0.5, 1, 2, 5];

  // 1. The family FL(p_t) for several γ with a draggable point.
  FV.widget("focal-curves", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0, 1], y: [0, 5], xLabel: L.pt, yLabel: L.loss, aspect: 0.55 });
    const sg = FV.ui.slider({ label: L.gamma, min: 0, max: 5, step: 0.1, value: cfg.gamma != null ? cfg.gamma : 2, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    w.controls.append(sg.el);
    const ro = FV.ui.readout(w.readout, [{ key: "p", label: "$p_t$ =" }, { key: "c", label: L.ceV }, { key: "f", label: L.factor, c: "faint" }, { key: "l", label: L.flV, c: "blue" }, { key: "r", label: L.ratio }]);
    let pt = cfg.pt != null ? cfg.pt : 0.9;
    const h = p.handle(pt, FL(pt, sg.value), { c: "blue", onDrag: (x) => { pt = FV.clamp(x, 0.01, 0.995); return [pt, FL(pt, sg.value)]; }, onChange: () => draw() });
    function draw() {
      const g = sg.value, y0 = FL(pt, g), ce = -Math.log(pt);
      p.clear();
      p.rect(0.5, 0, 1, 5, { c: "teal", opacity: 0.06 });
      p.text(0.99, 4.7, p.narrow ? "p_t > " + FV.fmt(0.5, 1) : L.easyZone, { c: "teal", anchor: "end" });
      FAMILY.forEach((gg) => p.fn((x) => FL(x, gg), { c: "faint", w: 1.2, opacity: 0.75, from: 0.004 }));
      p.fn((x) => -Math.log(x), { c: "guide", w: 1.8, dash: "6 5", from: 0.004 });
      if (!p.narrow) [0].concat(FAMILY).forEach((gg) => { const y = FL(0.22, gg); p.text(0.22, y, gg === 0 ? "γ = 0" : FV.fmt(gg, gg % 1 ? 1 : 0), { c: "faint", dx: 5, dy: -4, size: 11 }); });
      p.fn((x) => FL(x, g), { c: "blue", w: 2.8, from: 0.004 });
      p.line(pt, 0, pt, ce, { c: "guide", w: 1, dash: "3 3" });
      p.dot(pt, ce, { c: "guide", r: 4 });
      h.set(pt, y0);
      ro.set("p", FV.fmt(pt, 2)); ro.set("c", FV.num(ce, 3)); ro.set("f", FV.num(Math.pow(1 - pt, g), 3)); ro.set("l", FV.num(y0, 3));
      ro.set("r", y0 > 0 ? FV.num(ce / y0, 3) + L.times : "∞");
      p.legend([{ label: L.fl, c: "blue" }, { label: L.ce, c: "guide", dash: true }, { label: L.family, c: "faint" }, { label: L.easyZone, c: "teal", box: true }]);
    }
    p.onresize = draw; draw();
  });

  // 2. The modulating factor and both losses on a log scale.
  FV.widget("focal-weight", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [0, 1], y: [0, 1.05], xLabel: "p_t", aspect: 0.8, title: L.factorT });
    const b = new FV.Plot(FV.col(w.stage), { x: [0, 1], y: [1e-6, 100], yType: "log", xLabel: "p_t", yLabel: L.loss, aspect: 0.8, title: L.logT });
    const sg = FV.ui.slider({ label: L.gamma, min: 0, max: 5, step: 0.1, value: cfg.gamma != null ? cfg.gamma : 2, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    const sp = FV.ui.slider({ label: L.ptS, min: 0.01, max: 0.99, step: 0.01, value: cfg.pt != null ? cfg.pt : 0.9, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sg.el, sp.el);
    const ro = FV.ui.readout(w.readout, [{ key: "f", label: L.factor, c: "blue" }, { key: "c", label: "CE =" }, { key: "l", label: L.flV, c: "blue" }]);
    function draw() {
      const g = sg.value, pt = sp.value, f = Math.pow(1 - pt, g), ce = -Math.log(pt), fl = f * ce;
      a.clear();
      a.hline(1, { c: "guide", w: 1.8, dash: "6 5" });
      FAMILY.forEach((gg) => a.fn((x) => Math.pow(1 - x, gg), { c: "faint", w: 1.1, opacity: 0.7 }));
      a.fn((x) => Math.pow(1 - x, g), { c: "blue", w: 2.6 });
      a.line(pt, 0, pt, f, { c: "blue", w: 1, dash: "3 3" }); a.dot(pt, f, { c: "blue" });
      a.legend([{ label: "(1 − p_t)^γ", c: "blue" }, { label: "CE: 1", c: "guide", dash: true }]);
      b.clear();
      b.fn((x) => -Math.log(x), { c: "guide", w: 1.8, dash: "6 5", from: 0.002, to: 0.9995 });
      b.fn((x) => FL(x, g), { c: "blue", w: 2.6, from: 0.002, to: 0.9995 });
      if (fl > 1e-6) b.arrow(pt, ce, pt, fl, { c: "ink", w: 1.4, head: 7 });
      b.dot(pt, ce, { c: "guide", r: 4 });
      if (fl > 1e-6) b.dot(pt, fl, { c: "blue", r: 4 });
      b.legend([{ label: "FL", c: "blue" }, { label: "CE", c: "guide", dash: true }]);
      ro.set("f", FV.num(f, 3)); ro.set("c", FV.num(ce, 3)); ro.set("l", FV.num(fl, 3));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 3. The gradient with respect to the logit: not monotonic in p_t for γ > 0.
  FV.widget("focal-grad", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0, 1], y: [0, 1.5], xLabel: L.pt, yLabel: L.gradT, aspect: 0.5 });
    const sg = FV.ui.slider({ label: L.gamma, min: 0, max: 5, step: 0.1, value: cfg.gamma != null ? cfg.gamma : 2, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    w.controls.append(sg.el);
    const ro = FV.ui.readout(w.readout, [{ key: "m", label: L.gMax, c: "orange" }, { key: "x", label: L.gCross }, { key: "a", label: L.gAt }]);
    function argmax(g) { let bp = 1e-6, bv = -1; for (let i = 1; i < 4000; i++) { const q = i / 4000, v = G(q, g); if (v > bv) { bv = v; bp = q; } } return [bp, bv]; }
    function cross(g) { // root of G(p) − (1 − p) on (0, 1), if any
      if (g === 0) return null;
      let lo = 1e-9, hi = 0.999;
      const f = (q) => G(q, g) - (1 - q);
      if (!(f(lo) > 0) || f(hi) > 0) return null;
      for (let i = 0; i < 80; i++) { const m = 0.5 * (lo + hi); if (f(m) > 0) lo = m; else hi = m; }
      return 0.5 * (lo + hi);
    }
    function draw() {
      const g = sg.value;
      p.clear();
      p.hline(1, { c: "guide", opacity: 0.6 });
      FAMILY.forEach((gg) => p.fn((x) => G(x, gg), { c: "faint", w: 1.1, opacity: 0.7, from: 0.0005 }));
      p.fn((x) => 1 - x, { c: "guide", w: 1.8, dash: "6 5" });
      p.fn((x) => G(x, g), { c: "orange", w: 2.8, from: 0.0005 });
      const [mp, mv] = argmax(g), c = cross(g);
      if (g > 0) { p.dot(mp, mv, { c: "orange" }); p.line(mp, 0, mp, mv, { c: "orange", w: 1, dash: "3 3" }); }
      if (c) p.dot(c, 1 - c, { c: "ink", hollow: true, r: 5 });
      ro.set("m", g > 0 ? FV.fmt(mv, 3) + " (p_t = " + FV.fmt(mp, 3) + ")" : "1 (p_t → 0)");
      ro.set("x", c ? FV.fmt(c, 3) : "—");
      ro.set("a", FV.num(G(0.9, g) / 0.1, 3));
      p.legend([{ label: L.flGrad, c: "orange" }, { label: L.ceGrad, c: "guide", dash: true }, { label: L.family, c: "faint" }, { label: L.maxDot, c: "orange", dot: true }, { label: L.crossDot, c: "ink", dot: true }]);
    }
    p.onresize = draw; draw();
  });

  // 4. The surface FL(p_t, γ) and its exponential decay in γ.
  FV.widget("focal-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const s3 = new FV.Surface(FV.col(w.stage), { f: (p, g) => FL(p, g), x: [0.02, 1], y: [0, 5], z: [0, 4], n: 40, labels: { x: "p_t", y: "γ", z: "FL" }, azimuth: -0.95, elevation: 0.5, aspect: 0.85, title: L.surfT });
    const b = new FV.Plot(FV.col(w.stage), { x: [0, 5], y: [1e-6, 10], yType: "log", xLabel: "γ", yLabel: "FL", aspect: 0.85, title: L.decayT });
    const sg = FV.ui.slider({ label: L.gamma, min: 0, max: 5, step: 0.1, value: cfg.gamma != null ? cfg.gamma : 2, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    const sp = FV.ui.slider({ label: L.ptS, min: 0.02, max: 0.99, step: 0.01, value: cfg.pt != null ? cfg.pt : 0.5, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sg.el, sp.el);
    const ro = FV.ui.readout(w.readout, [{ key: "l", label: "$\\mathrm{FL}(p_t,\\gamma)$ =", c: "blue" }, { key: "k", label: "$\\ln(1-p_t)$ =", c: "teal" }]);
    function draw() {
      const g = sg.value, pt = sp.value;
      s3.setPaths([
        { pts: FV.linspace(0.02, 1, 80).map((x) => [x, g, FL(x, g)]), c: "blue", w: 3 },
        { pts: FV.linspace(0, 5, 60).map((gg) => [pt, gg, FL(pt, gg)]), c: "teal", w: 3 },
      ]);
      s3.setPoints([{ x: pt, y: g, z: FL(pt, g), c: "ink", r: 5 }]);
      b.clear();
      [0.1, 0.5, 0.9, 0.99].forEach((q) => b.fn((gg) => FL(q, gg), { c: "faint", w: 1.1, opacity: 0.7 }));
      [0.1, 0.5, 0.9, 0.99].forEach((q) => { const gx = Math.min(5, Math.log(4e-6 / -Math.log(q)) / Math.log(1 - q)); b.text(gx, FL(q, gx), FV.fmt(q, q === 0.99 ? 2 : 1), { c: "faint", anchor: "end", dx: -4, dy: -5, size: 11 }); });
      b.fn((gg) => FL(pt, gg), { c: "teal", w: 2.6 });
      b.vline(g, { c: "blue" });
      b.dot(g, FL(pt, g), { c: "ink", r: 4 });
      b.legend([{ label: L.decay, c: "teal" }, { label: L.others, c: "faint" }, { label: L.sliceG, c: "blue", dash: true }]);
      ro.set("l", FV.num(FL(pt, g), 3)); ro.set("k", FV.fmt(Math.log(1 - pt), 3));
    }
    b.onresize = draw; draw();
  });

  // 5. Class imbalance: where the total loss comes from under CE and under FL.
  //    Negatives have the logit of the correct class z_t ~ N(4, 1), positives z_t ~ N(0, 1).
  const ZG = FV.linspace(-8, 12, 2001), DZ = ZG[1] - ZG[0];
  function shares(g, ratio) {
    const out = { easy: 0, hard: 0, pos: 0, bins: new Array(20).fill(0), nEasy: 0, nAll: 0 };
    ZG.forEach((z) => {
      const pt = sig(z), l = FL(pt, g), dn = ratio * FV.phi(z - 4) * DZ, dp = FV.phi(z) * DZ;
      const bin = Math.min(19, Math.floor(pt * 20));
      if (pt >= 0.9) { out.easy += dn * l; out.nEasy += dn; } else out.hard += dn * l;
      out.pos += dp * l; out.nAll += dn + dp;
      out.bins[bin] += (dn + dp) * l;
    });
    const T = out.easy + out.hard + out.pos;
    out.easy /= T; out.hard /= T; out.pos /= T; out.bins = out.bins.map((v) => v / T); out.nEasy /= out.nAll;
    return out;
  }
  FV.widget("focal-imbalance", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [0, 1], y: [0, 1], xLabel: "p_t", aspect: 0.8, title: L.binT });
    const b = new FV.Plot(FV.col(w.stage), { x: [0, 2], y: [0, 1], xTicks: [{ v: 0.5, label: "CE" }, { v: 1.5, label: "FL" }], yTicks: [0, 0.25, 0.5, 0.75, 1].map((v) => ({ v, label: (100 * v) + "%" })), aspect: 0.8, title: L.shareT });
    const sg = FV.ui.slider({ label: L.gamma, min: 0, max: 5, step: 0.1, value: cfg.gamma != null ? cfg.gamma : 2, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    const sr = FV.ui.slider({ label: L.ratioS, min: 0, max: 4, step: 0.05, value: Math.log10(cfg.ratio || 1000), map: (v) => Math.round(Math.pow(10, v)), unmap: (v) => Math.log10(v), fmt: (v) => String(v), oninput: draw });
    w.controls.append(sg.el, sr.el);
    const ro = FV.ui.readout(w.readout, [{ key: "n", label: L.easyCnt }, { key: "e", label: L.easyCE }, { key: "e2", label: L.flShort + ":", c: "blue" }, { key: "p", label: L.posShare }, { key: "p2", label: L.flShort + ":", c: "blue" }]);
    function stack(x, s) {
      let y = 0;
      [["easy", "guide"], ["hard", "blue"], ["pos", "red"]].forEach(([k, c]) => {
        const v = s[k];
        b.rect(x - 0.32, y, x + 0.32, y + v, { c, opacity: 0.85 });
        if (v > 0.04) b.text(x + 0.35, y + v / 2, Math.round(100 * v) + "%", { dy: 4, size: 12 });
        y += v;
      });
    }
    function draw() {
      const g = sg.value, ratio = sr.value, ce = shares(0, ratio), fl = shares(g, ratio);
      const top = Math.max(...ce.bins, ...fl.bins);
      a.setDomain(null, [0, Math.max(0.1, Math.ceil(top * 10 + 0.5) / 10)]);
      a.clear();
      a.rect(0.9, 0, 1, a.o.y[1], { c: "faint", opacity: 0.08 });
      ce.bins.forEach((v, i) => a.rect(i / 20 + 0.004, 0, i / 20 + 0.025, v, { c: "guide", opacity: 0.9 }));
      fl.bins.forEach((v, i) => a.rect(i / 20 + 0.025, 0, i / 20 + 0.046, v, { c: "blue", opacity: 0.9 }));
      a.legend([{ label: "CE", c: "guide", box: true }, { label: "FL", c: "blue", box: true }]);
      b.clear(); stack(0.5, ce); stack(1.5, fl);
      b.legend([{ label: L.easyN, c: "guide", box: true }, { label: L.hardN, c: "blue", box: true }, { label: L.posC, c: "red", box: true }]);
      ro.set("n", pct(ce.nEasy)); ro.set("e", pct(ce.easy)); ro.set("e2", pct(fl.easy)); ro.set("p", pct(ce.pos)); ro.set("p2", pct(fl.pos));
    }
    a.onresize = draw; b.onresize = draw; draw();
  });

  // 6. The best constant prediction under CE and under α-balanced FL: FL is not calibrated.
  FV.widget("focal-prior", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [1e-3, 0.95], xType: "log", y: [0.9, 3], xLabel: L.pAxis, aspect: 0.5, title: L.jAxis });
    const logS = (o) => FV.ui.slider({ label: o.label, min: Math.log10(o.min), max: Math.log10(o.max), step: 0.01, value: Math.log10(o.value), map: (v) => Math.pow(10, v), unmap: (v) => Math.log10(v), fmt: (v) => FV.num(v, 2), oninput: draw });
    const sp = logS({ label: L.piS, min: 0.001, max: 0.5, value: cfg.pi || 0.01 });
    const sg = FV.ui.slider({ label: L.gamma, min: 0, max: 5, step: 0.1, value: cfg.gamma != null ? cfg.gamma : 2, fmt: (v) => FV.fmt(v, 1), oninput: draw });
    const sa = FV.ui.slider({ label: L.alphaS, min: 0.05, max: 0.95, step: 0.05, value: cfg.alpha != null ? cfg.alpha : 0.25, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sp.el, sg.el, sa.el);
    const ro = FV.ui.readout(w.readout, [{ key: "c", label: L.pCe }, { key: "f", label: L.pFl, c: "blue" }, { key: "z", label: L.zFl, c: "blue" }, { key: "b", label: L.bInit }]);
    // mean loss of the constant prediction q (as a logit z, for stability)
    const J = (z, pi, g, al) => { const q = sig(z), lq = -Math.log1p(Math.exp(-z)), l1q = -Math.log1p(Math.exp(z)); return -pi * al * Math.pow(1 - q, g) * lq - (1 - pi) * (1 - al) * Math.pow(q, g) * l1q; };
    function argmin(f) { // golden-section search on the logit
      let a = -12, b = 12; const r = (Math.sqrt(5) - 1) / 2;
      let c = b - r * (b - a), d = a + r * (b - a);
      for (let i = 0; i < 120; i++) { if (f(c) < f(d)) b = d; else a = c; c = b - r * (b - a); d = a + r * (b - a); }
      return 0.5 * (a + b);
    }
    const logit = (q) => Math.log(q / (1 - q));
    function draw() {
      const pi = sp.value, g = sg.value, al = sa.value;
      const fce = (z) => J(z, pi, 0, 0.5), ffl = (z) => J(z, pi, g, al);
      const zc = argmin(fce), zf = argmin(ffl), mc = fce(zc), mf = ffl(zf);
      p.clear();
      p.hline(1, { c: "guide", opacity: 0.6 });
      p.fn((q) => fce(logit(q)) / mc, { c: "guide", w: 1.8, dash: "6 5" });
      p.fn((q) => ffl(logit(q)) / mf, { c: "blue", w: 2.6 });
      p.vline(sig(zc), { c: "guide", w: 1.2 }); p.vline(sig(zf), { c: "blue", w: 1.2 });
      p.dot(sig(zc), 1, { c: "guide", r: 4 }); p.dot(sig(zf), 1, { c: "blue" });
      p.legend([{ label: L.flOpt, c: "blue" }, { label: L.ceOpt, c: "guide", dash: true }]);
      ro.set("c", FV.num(sig(zc), 3)); ro.set("f", FV.num(sig(zf), 3)); ro.set("z", FV.fmt(zf, 3)); ro.set("b", FV.fmt(logit(pi), 3));
    }
    p.onresize = draw; draw();
  });

  // Imbalanced 2D data: 400 negatives and 20 positives (deterministic).
  function data() {
    const r = FV.rng(7), pts = [];
    for (let i = 0; i < 400; i++) pts.push({ x: -0.9 + 1.1 * r.normal(), y: -0.7 + 1.1 * r.normal(), c: 0 });
    for (let i = 0; i < 20; i++) pts.push({ x: 1.3 + 0.7 * r.normal(), y: 1.1 + 0.7 * r.normal(), c: 1 });
    return pts;
  }

  // 7. Logistic regression trained with CE and with FL side by side; dot size shows each example's gradient.
  FV.widget("focal-train", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const pts = data();
    const mk = (title) => new FV.Plot(FV.col(w.stage), { x: [-4.5, 4], y: [-4.5, 4], xLabel: L.x1, yLabel: L.x2, equal: true, title });
    const pc = mk(L.ceTitle), pf = mk(L.flTitle);
    const sg = FV.ui.slider({ label: L.gamma + " (FL)", min: 0, max: 5, step: 0.1, value: cfg.gamma != null ? cfg.gamma : 2, fmt: (v) => FV.fmt(v, 1), oninput: () => draw() });
    const pi = 20 / 420, b0 = Math.log(pi / (1 - pi)), lr = 1.5, MAXS = 400;
    let mc, mf, step;
    function init() { mc = { w1: 0, w2: 0, b: b0 }; mf = { w1: 0, w2: 0, b: b0 }; step = 0; }
    init();
    // per-example |∂L/∂z| and the share of it that comes from easy examples (p_t > 0.9)
    function grads(m, g) {
      let g1 = 0, g2 = 0, gb = 0, easy = 0, tot = 0, tp = 0, fp = 0;
      const d = pts.map((q) => {
        const z = m.w1 * q.x + m.w2 * q.y + m.b, pt = sig(q.c ? z : -z), a = G(pt, g), dz = q.c ? -a : a;
        g1 += dz * q.x; g2 += dz * q.y; gb += dz; tot += a; if (pt > 0.9) easy += a;
        if (z >= 0) { if (q.c) tp++; else fp++; }
        return a;
      });
      return { d, g1, g2, gb, easy: easy / tot, tp, fp };
    }
    function upd(m, s) { const n = pts.length; m.w1 -= (lr * s.g1) / n; m.w2 -= (lr * s.g2) / n; m.b -= (lr * s.gb) / n; }
    const player = FV.ui.player({
      interval: 40,
      onstep() { upd(mc, grads(mc, 0)); upd(mf, grads(mf, sg.value)); step++; draw(); return step < MAXS; },
      onreset() { init(); draw(); },
    });
    w.controls.append(sg.el, player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.step + " =" }, { key: "e", label: L.easyG }, { key: "e2", label: "FL:", c: "blue" }, { key: "t", label: L.tp }, { key: "t2", label: "FL:", c: "blue" }, { key: "f", label: L.fp }, { key: "f2", label: "FL:", c: "blue" }]);
    function panel(p, m, s) {
      p.clear();
      const prob = (x, y) => sig(m.w1 * x + m.w2 * y + m.b);
      p.contours(prob, [0.1, 0.9], { style: () => ({ c: "ink", w: 1, opacity: 0.4, dash: "4 4" }) });
      pts.forEach((q, i) => { if (!q.c) p.dot(q.x, q.y, { c: "blue", r: 1.5 + 7 * Math.sqrt(s.d[i]) }); });
      pts.forEach((q, i) => { if (q.c) p.dot(q.x, q.y, { c: "red", r: 1.5 + 7 * Math.sqrt(s.d[i]) }); });
      p.contours(prob, [0.5], { style: () => ({ c: "ink", w: 2.2, opacity: 0.9 }) });
      p.legend([{ label: L.neg, c: "blue", dot: true }, { label: L.pos, c: "red", dot: true }, { label: L.bound, c: "ink" }]);
    }
    function draw() {
      const sc = grads(mc, 0), sf = grads(mf, sg.value);
      panel(pc, mc, sc); panel(pf, mf, sf);
      ro.set("s", String(step)); ro.set("e", pct(sc.easy)); ro.set("e2", pct(sf.easy));
      ro.set("t", String(sc.tp)); ro.set("t2", String(sf.tp)); ro.set("f", String(sc.fp)); ro.set("f2", String(sf.fp));
      w.note.textContent = L.size;
    }
    pc.onresize = draw; pf.onresize = draw; draw();
  });
})();
