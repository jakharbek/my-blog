/* Widgets of the formula page "Triplet Loss". Built on FV (assets/js/viz.js). */
(function () {
  "use strict";
  const L = {
    ru: {
      x1: "z₁", x2: "z₂", m: "Зазор $m$", sq: "Квадраты расстояний $d^2$", anchor: "якорь a", pos: "свой p", neg: "чужой n",
      ringP: "окружность радиуса d(a, p)", ringM: "граница d(a, p) + m", ringMsq: "граница √(d²(a, p) + m)", grad: "−∇L: куда сдвинется точка",
      regime: "режим", easy: "лёгкая", semi: "полутрудная", hard: "трудная", loss: "L =",
      delta: "Δ = d(a, p) − d(a, n)", dlt: "Разность $\\Delta$", hinge: "max(0, Δ + m)", soft: "ln(1 + exp Δ)", dhinge: "производная hinge", dsoft: "σ(Δ)",
      variant: "Вариант", hingeName: "hinge (с зазором)", softName: "soft margin", dL: "∂L/∂Δ",
      dap: "d(a, p)", dan: "d(a, n)", showBatch: "Показать тройки батча (рис. 5)", cnt: "тройки батча: лёгкие / полутрудные / трудные",
      who: "Двигаем", negMode: "чужого n", posMode: "своего p", dist: "Расстояние", plain: "d", sqd: "d²",
      ray: "срез вдоль луча из якоря", r: "расстояние до якоря r", gnorm: "|∇L|", lossLine: "L",
      anc: "Якорь №", strat: "Стратегия", bh: "batch-hard", ba: "batch-all", ident: "личность",
      lbh: "L batch-hard =", lba: "L batch-all =", act: "активных троек =", forA: "у якоря: лёгкие / полутрудные / трудные =",
      hardP: "самый далёкий свой", hardN: "самый близкий чужой", activeN: "чужие, нарушающие зазор",
      input: "входное пространство", emb: "пространство эмбеддингов f(x)", step: "шаг", lossT: "L (batch-hard)", order: "верно упорядоченных троек", actA: "активных якорей",
      lossCurve: "потеря по шагам обучения", nuis: "x₁ — помеха (ракурс, свет)", idf: "x₂ — признак личности",
      ang: "угол", zone: "здесь n нарушал бы зазор", bound: "радиус границы R =", circle: "единичная окружность", dsq: "d² = 2 − 2 cos θ", need: "нужно θ(a, n) ≥", thAP: "θ(a, p) =", thAN: "θ(a, n) =", never: "недостижимо",
    },
    en: {
      x1: "z₁", x2: "z₂", m: "Margin $m$", sq: "Squared distances $d^2$", anchor: "anchor a", pos: "positive p", neg: "negative n",
      ringP: "circle of radius d(a, p)", ringM: "boundary d(a, p) + m", ringMsq: "boundary √(d²(a, p) + m)", grad: "−∇L: where a point will move",
      regime: "regime", easy: "easy", semi: "semi-hard", hard: "hard", loss: "L =",
      delta: "Δ = d(a, p) − d(a, n)", dlt: "Difference $\\Delta$", hinge: "max(0, Δ + m)", soft: "ln(1 + exp Δ)", dhinge: "hinge derivative", dsoft: "σ(Δ)",
      variant: "Variant", hingeName: "hinge (with margin)", softName: "soft margin", dL: "∂L/∂Δ",
      dap: "d(a, p)", dan: "d(a, n)", showBatch: "Show the batch triplets (Fig. 5)", cnt: "batch triplets: easy / semi-hard / hard",
      who: "Move", negMode: "the negative n", posMode: "the positive p", dist: "Distance", plain: "d", sqd: "d²",
      ray: "slice along a ray from the anchor", r: "distance to the anchor r", gnorm: "|∇L|", lossLine: "L",
      anc: "Anchor no.", strat: "Strategy", bh: "batch-hard", ba: "batch-all", ident: "identity",
      lbh: "L batch-hard =", lba: "L batch-all =", act: "active triplets =", forA: "for the anchor: easy / semi-hard / hard =",
      hardP: "farthest positive", hardN: "closest negative", activeN: "negatives violating the margin",
      input: "input space", emb: "embedding space f(x)", step: "step", lossT: "L (batch-hard)", order: "correctly ordered triplets", actA: "active anchors",
      lossCurve: "loss over training steps", nuis: "x₁ — nuisance (pose, light)", idf: "x₂ — identity feature",
      ang: "angle", zone: "n here would violate the margin", bound: "boundary radius R =", circle: "unit circle", dsq: "d² = 2 − 2 cos θ", need: "need θ(a, n) ≥", thAP: "θ(a, p) =", thAN: "θ(a, n) =", never: "unreachable",
    },
    uz: {
      x1: "z₁", x2: "z₂", m: "$m$ oraliq", sq: "Masofalar kvadratlari $d^2$", anchor: "langar a", pos: "o‘ziniki p", neg: "begona n",
      ringP: "radiusi d(a, p) bo‘lgan aylana", ringM: "d(a, p) + m chegara", ringMsq: "√(d²(a, p) + m) chegara", grad: "−∇L: nuqta qayerga siljiydi",
      regime: "rejim", easy: "oson", semi: "yarim qiyin", hard: "qiyin", loss: "L =",
      delta: "Δ = d(a, p) − d(a, n)", dlt: "$\\Delta$ ayirma", hinge: "max(0, Δ + m)", soft: "ln(1 + exp Δ)", dhinge: "hinge hosilasi", dsoft: "σ(Δ)",
      variant: "Variant", hingeName: "hinge (oraliqli)", softName: "soft margin", dL: "∂L/∂Δ",
      dap: "d(a, p)", dan: "d(a, n)", showBatch: "Batch uchliklarini ko‘rsatish (5-rasm)", cnt: "batch uchliklari: oson / yarim qiyin / qiyin",
      who: "Siljitamiz", negMode: "begona n", posMode: "o‘ziniki p", dist: "Masofa", plain: "d", sqd: "d²",
      ray: "langardan chiqqan nur bo‘ylab kesim", r: "langargacha masofa r", gnorm: "|∇L|", lossLine: "L",
      anc: "Langar №", strat: "Strategiya", bh: "batch-hard", ba: "batch-all", ident: "shaxs",
      lbh: "L batch-hard =", lba: "L batch-all =", act: "faol uchliklar =", forA: "langarda: oson / yarim qiyin / qiyin =",
      hardP: "eng uzoq o‘ziniki", hardN: "eng yaqin begona", activeN: "oraliqni buzayotgan begonalar",
      input: "kirish fazosi", emb: "f(x) embedding fazosi", step: "qadam", lossT: "L (batch-hard)", order: "to‘g‘ri tartiblangan uchliklar", actA: "faol langarlar",
      lossCurve: "o‘qitish qadamlari bo‘yicha yo‘qotish", nuis: "x₁ — xalaqit (rakurs, yorug‘lik)", idf: "x₂ — shaxs belgisi",
      ang: "burchak", zone: "bu yerda n oraliqni buzardi", bound: "chegara radiusi R =", circle: "birlik aylana", dsq: "d² = 2 − 2 cos θ", need: "kerak θ(a, n) ≥", thAP: "θ(a, p) =", thAN: "θ(a, n) =", never: "erishib bo‘lmaydi",
    },
  }[FV.lang] || {};
  const dec = (s) => (FV.lang === "en" ? s : s.replace(/(\d)\.(\d)/g, "$1,$2"));
  const ID_C = ["blue", "orange", "teal", "violet"];
  const REG_C = { easy: "teal", semi: "violet", hard: "red" };

  /* sim:begin — pure maths, also used by the numeric checks of the page text */
  const dist = (u, v) => Math.hypot(u[0] - v[0], u[1] - v[1]);
  function regime(dap, dan, m) { return dan >= dap + m ? "easy" : dan > dap ? "semi" : "hard"; }
  // A batch of P identities × K samples in a 2D embedding (fixed).
  function batch() {
    const r = FV.rng(17), pts = [];
    const C = [[-0.9, 0.55], [0.85, 0.75], [0.7, -0.75], [-0.75, -0.7]];
    for (let c = 0; c < 4; c++) for (let k = 0; k < 4; k++) pts.push({ x: C[c][0] + 0.42 * r.normal(), y: C[c][1] + 0.42 * r.normal(), c });
    return pts;
  }
  // All (a, p, n) triplets of a batch: their distances.
  function triplets(pts) {
    const out = [], n = pts.length;
    for (let a = 0; a < n; a++) for (let p = 0; p < n; p++) {
      if (p === a || pts[p].c !== pts[a].c) continue;
      const dap = Math.hypot(pts[a].x - pts[p].x, pts[a].y - pts[p].y);
      for (let q = 0; q < n; q++) if (pts[q].c !== pts[a].c) out.push({ a, p, n: q, dap, dan: Math.hypot(pts[a].x - pts[q].x, pts[a].y - pts[q].y) });
    }
    return out;
  }
  function batchLosses(pts, m) {
    const T = triplets(pts);
    let sa = 0, na = 0;
    T.forEach((t) => { const l = t.dap - t.dan + m; if (l > 0) { sa += l; na++; } });
    let sh = 0;
    for (let a = 0; a < pts.length; a++) {
      let dp = 0, dn = Infinity;
      T.forEach((t) => { if (t.a === a) { dp = Math.max(dp, t.dap); dn = Math.min(dn, t.dan); } });
      sh += Math.max(0, dp - dn + m);
    }
    return { all: na ? sa / na : 0, hard: sh / pts.length, active: na, total: T.length };
  }

  // Training: a 2 → H → 2 tanh network maps inputs to an embedding; batch-hard triplet loss, Adam.
  function trainData() {
    const r = FV.rng(9), pts = [], off = [-1.2, -0.4, 0.4, 1.2];
    for (let c = 0; c < 4; c++) for (let k = 0; k < 12; k++) { const x = -3 + 6 * r(); pts.push({ x, y: off[c] + 0.5 * Math.sin(1.2 * x) + 0.1 * r.normal(), c }); }
    return pts;
  }
  function embedNet(H, seed) {
    const r = FV.rng(seed);
    const M = { H, W1: [], b1: [], W2: [[], []], b2: [0, 0] };
    for (let j = 0; j < H; j++) { M.W1.push([r.normal() * 0.8, r.normal() * 0.8]); M.b1.push(r.normal() * 0.5); }
    for (let o = 0; o < 2; o++) for (let j = 0; j < H; j++) M.W2[o].push(r.normal() / Math.sqrt(H));
    const NP = 5 * H + 2, mom = new Array(NP).fill(0), vel = new Array(NP).fill(0);
    let t = 0;
    M.fwd = (p) => {
      const h = M.W1.map((w, j) => Math.tanh(w[0] * p.x + w[1] * p.y + M.b1[j]));
      return { h, e: [0, 1].map((o) => M.b2[o] + M.W2[o].reduce((s, w, j) => s + w * h[j], 0)) };
    };
    M.embed = (pts) => pts.map((p) => M.fwd(p).e);
    M.step = (pts, m, lr) => {
      const F = pts.map((p) => M.fwd(p)), E = F.map((f) => f.e), n = pts.length;
      const D = (i, j) => Math.hypot(E[i][0] - E[j][0], E[i][1] - E[j][1]);
      const gE = E.map(() => [0, 0]);
      let loss = 0, active = 0;
      for (let a = 0; a < n; a++) {
        let pi = -1, pd = -1, ni = -1, nd = Infinity;
        for (let j = 0; j < n; j++) {
          if (j === a) continue;
          const d = D(a, j);
          if (pts[j].c === pts[a].c) { if (d > pd) { pd = d; pi = j; } } else if (d < nd) { nd = d; ni = j; }
        }
        const l = pd - nd + m;
        if (l > 0) {
          loss += l; active++;
          const ap = [(E[a][0] - E[pi][0]) / (pd + 1e-9), (E[a][1] - E[pi][1]) / (pd + 1e-9)], an = [(E[a][0] - E[ni][0]) / (nd + 1e-9), (E[a][1] - E[ni][1]) / (nd + 1e-9)];
          for (let k = 0; k < 2; k++) { gE[a][k] += (ap[k] - an[k]) / n; gE[pi][k] -= ap[k] / n; gE[ni][k] += an[k] / n; }
        }
      }
      const g = new Array(NP).fill(0);
      for (let i = 0; i < n; i++) {
        const h = F[i].h;
        for (let o = 0; o < 2; o++) { for (let j = 0; j < H; j++) g[3 * H + o * H + j] += gE[i][o] * h[j]; g[5 * H + o] += gE[i][o]; }
        for (let j = 0; j < H; j++) {
          const gh = (gE[i][0] * M.W2[0][j] + gE[i][1] * M.W2[1][j]) * (1 - h[j] * h[j]);
          g[2 * j] += gh * pts[i].x; g[2 * j + 1] += gh * pts[i].y; g[2 * H + j] += gh;
        }
      }
      t++;
      const c1 = 1 - Math.pow(0.9, t), c2 = 1 - Math.pow(0.999, t);
      const th = [...M.W1.flat(), ...M.b1, ...M.W2.flat(), ...M.b2];
      for (let k = 0; k < NP; k++) { mom[k] = 0.9 * mom[k] + 0.1 * g[k]; vel[k] = 0.999 * vel[k] + 0.001 * g[k] * g[k]; th[k] -= (lr * (mom[k] / c1)) / (Math.sqrt(vel[k] / c2) + 1e-8); }
      for (let j = 0; j < H; j++) { M.W1[j][0] = th[2 * j]; M.W1[j][1] = th[2 * j + 1]; M.b1[j] = th[2 * H + j]; M.W2[0][j] = th[3 * H + j]; M.W2[1][j] = th[4 * H + j]; }
      M.b2[0] = th[5 * H]; M.b2[1] = th[5 * H + 1];
      return { loss: loss / n, active };
    };
    return M;
  }
  // Batch-hard loss and the share of correctly ordered triplets for given embeddings.
  function evalEmb(E, pts, m) {
    const n = pts.length, D = (i, j) => Math.hypot(E[i][0] - E[j][0], E[i][1] - E[j][1]);
    let loss = 0, active = 0, ok = 0, tot = 0;
    for (let a = 0; a < n; a++) {
      let pd = 0, nd = Infinity;
      for (let j = 0; j < n; j++) { if (j === a) continue; const d = D(a, j); if (pts[j].c === pts[a].c) pd = Math.max(pd, d); else nd = Math.min(nd, d); }
      const l = pd - nd + m; if (l > 0) { loss += l; active++; }
      for (let p = 0; p < n; p++) {
        if (p === a || pts[p].c !== pts[a].c) continue;
        const dp = D(a, p);
        for (let q = 0; q < n; q++) if (pts[q].c !== pts[a].c) { tot++; if (dp < D(a, q)) ok++; }
      }
    }
    return { loss: loss / n, active, order: ok / tot };
  }
  /* sim:end */

  function circle(p, cx, cy, r, o) { const pts = []; for (let i = 0; i <= 120; i++) { const t = (2 * Math.PI * i) / 120; pts.push([cx + r * Math.cos(t), cy + r * Math.sin(t)]); } return p.path(pts, o); }

  // 1. Drag the anchor, the positive and the negative; rings, loss and gradient arrows.
  FV.widget("triplet-play", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-2, 2], y: [-1.3, 1.3], equal: true, xLabel: L.x1, yLabel: L.x2 });
    const P = { a: (cfg.a || [-0.5, 0]).slice(), p: (cfg.p || [0.4, 0]).slice(), n: (cfg.n || [0.1, 0.8]).slice() };
    const sm = FV.ui.slider({ label: L.m, min: 0, max: 1, step: 0.05, value: cfg.m != null ? cfg.m : 0.2, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sq = FV.ui.check({ label: L.sq, checked: !!cfg.squared, onchange: () => draw() });
    w.controls.append(sm.el, sq.el);
    const ro = FV.ui.readout(w.readout, [{ key: "p", label: "d(a, p) =", c: "blue" }, { key: "n", label: "d(a, n) =", c: "red" }, { key: "l", label: L.loss, c: "orange" }, { key: "r", label: L.regime + ":" }]);
    const mk = (k, c) => p.handle(P[k][0], P[k][1], { c, onDrag: (x, y) => { P[k] = [x, y]; return [x, y]; }, onChange: () => draw() });
    const H = { a: mk("a", "ink"), p: mk("p", "blue"), n: mk("n", "red") };
    function draw() {
      const m = sm.value, s2 = sq.value, a = P.a, pp = P.p, n = P.n;
      const dap = dist(a, pp), dan = dist(a, n);
      const fp = s2 ? dap * dap : dap, fn = s2 ? dan * dan : dan;
      const l = Math.max(0, fp - fn + m), reg = regime(fp, fn, m);
      p.clear();
      const rM = s2 ? Math.sqrt(dap * dap + m) : dap + m;
      const ring = [];
      for (let i = 0; i <= 120; i++) { const t = (2 * Math.PI * i) / 120; ring.push([a[0] + rM * Math.cos(t), a[1] + rM * Math.sin(t)]); }
      for (let i = 120; i >= 0; i--) { const t = (2 * Math.PI * i) / 120; ring.push([a[0] + dap * Math.cos(t), a[1] + dap * Math.sin(t)]); }
      p.path(ring, { fill: true, close: true, fillC: "orange", fillOpacity: 0.1 });
      circle(p, a[0], a[1], dap, { c: "blue", w: 1.3, dash: "5 4" });
      circle(p, a[0], a[1], rM, { c: "orange", w: 1.6 });
      p.line(a[0], a[1], pp[0], pp[1], { c: "blue", w: 2 });
      p.line(a[0], a[1], n[0], n[1], { c: "red", w: 2 });
      if (l > 0) {
        const k = 0.35;
        // −∇L for each point (the direction gradient descent moves it). At a zero distance ‖u − v‖ has no
        // gradient; we take the subgradient 0 (the unit ball contains it), so coincident points get no arrow.
        const unit = (u, v, d) => (d > 1e-9 ? [(u[0] - v[0]) / d, (u[1] - v[1]) / d] : [0, 0]);
        const gp = s2 ? [2 * (a[0] - pp[0]), 2 * (a[1] - pp[1])] : unit(a, pp, dap);
        const gn = s2 ? [2 * (n[0] - a[0]), 2 * (n[1] - a[1])] : unit(n, a, dan);
        const ga = [-(gp[0] + gn[0]), -(gp[1] + gn[1])];
        [[pp, gp], [n, gn], [a, ga]].forEach(([q, g]) => p.arrow(q[0], q[1], q[0] + k * g[0], q[1] + k * g[1], { c: "orange", w: 2 }));
      }
      p.text(a[0], a[1] - 0.22, "a", { anchor: "middle", c: "ink" });
      p.text(pp[0], pp[1] - 0.22, "p", { anchor: "middle", c: "blue" });
      p.text(n[0], n[1] - 0.22, "n", { anchor: "middle", c: "red" });
      H.a.set(a[0], a[1]); H.p.set(pp[0], pp[1]); H.n.set(n[0], n[1]);
      ro.set("p", FV.fmt(fp, 3) + (s2 ? " (d²)" : "")); ro.set("n", FV.fmt(fn, 3) + (s2 ? " (d²)" : "")); ro.set("l", FV.fmt(l, 3)); ro.set("r", L[reg]);
      p.legend([{ label: L.anchor, c: "ink", dot: true }, { label: L.pos, c: "blue", dot: true }, { label: L.neg, c: "red", dot: true }, { label: s2 ? L.ringMsq : L.ringM, c: "orange" }, { label: L.grad, c: "orange", box: true }]);
    }
    p.onresize = draw; draw();
  });

  // 2. The hinge as a function of Δ and its derivative; the soft-margin version for comparison.
  FV.widget("triplet-hinge", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-1.5, 1], y: [-0.1, 1.6], xLabel: L.delta, yLabel: "L", aspect: 0.45 });
    const q = new FV.Plot(w.stage, { x: [-1.5, 1], y: [-0.1, 1.15], xLabel: L.delta, yLabel: L.dL, aspect: 0.25, minHeight: 160, maxHeight: 220 });
    const sm = FV.ui.slider({ label: L.m, min: 0, max: 1, step: 0.05, value: cfg.m != null ? cfg.m : 0.2, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sd = FV.ui.slider({ label: L.dlt, min: -1.5, max: 1, step: 0.01, value: cfg.delta != null ? cfg.delta : -0.1, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sf = FV.ui.check({ label: L.softName + " " + L.soft, checked: cfg.soft !== false, onchange: () => draw() });
    w.controls.append(sm.el, sd.el, sf.el);
    const ro = FV.ui.readout(w.readout, [{ key: "l", label: "max(0, Δ + m) =", c: "blue" }, { key: "g", label: "∂L/∂Δ =", c: "orange" }, { key: "s", label: L.soft + " =", c: "teal" }, { key: "r", label: L.regime + ":" }]);
    const sp = (d) => (d > 0 ? d + Math.log1p(Math.exp(-d)) : Math.log1p(Math.exp(d)));
    const sg = (d) => 1 / (1 + Math.exp(-d));
    function bands(pl, m, y0, y1) {
      pl.rect(-1.5, y0, -m, y1, { c: REG_C.easy, opacity: 0.07 });
      pl.rect(-m, y0, 0, y1, { c: REG_C.semi, opacity: 0.1 });
      pl.rect(0, y0, 1, y1, { c: REG_C.hard, opacity: 0.08 });
    }
    function draw() {
      const m = sm.value, d = sd.value, h = (x) => Math.max(0, x + m);
      p.clear(); bands(p, m, -0.1, 1.6);
      p.text((-1.5 - m) / 2, 1.48, L.easy, { c: "teal", anchor: "middle" });
      if (m >= 0.3) p.text(-m / 2, 1.48, L.semi, { c: "violet", anchor: "middle" });
      p.text(0.5, 1.48, L.hard, { c: "red", anchor: "middle" });
      if (sf.value) p.fn(sp, { c: "teal", w: 1.8, dash: "6 4" });
      p.fn(h, { c: "blue", w: 2.6 });
      p.dot(d, h(d), { c: "blue" });
      p.legend([{ label: L.hinge, c: "blue" }].concat(sf.value ? [{ label: L.soft, c: "teal", dash: true }] : []));
      q.clear(); bands(q, m, -0.1, 1.15);
      if (sf.value) q.fn(sg, { c: "teal", w: 1.8, dash: "6 4" });
      q.line(-1.5, 0, -m, 0, { c: "orange", w: 2.6 }); q.line(-m, 1, 1, 1, { c: "orange", w: 2.6 });
      q.dot(-m, 0, { c: "orange", hollow: true, r: 4 }); q.dot(-m, 1, { c: "orange", r: 4 });
      q.dot(d, d > -m ? 1 : 0, { c: "orange" });
      q.legend([{ label: L.dhinge, c: "orange" }].concat(sf.value ? [{ label: L.dsoft, c: "teal", dash: true }] : []));
      ro.set("l", FV.fmt(h(d), 3)); ro.set("g", d > -m ? "1" : "0"); ro.set("s", FV.fmt(sp(d), 3));
      ro.set("r", L[d <= -m ? "easy" : d < 0 ? "semi" : "hard"]);
    }
    p.onresize = draw; q.onresize = draw; draw();
  });

  // 3. The (d(a,p), d(a,n)) plane: loss heatmap, the three regimes and the batch triplets.
  FV.widget("triplet-regimes", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [0, 2.2], y: [0, 2.2], equal: true, xLabel: L.dap, yLabel: L.dan });
    const T = triplets(batch());
    const sm = FV.ui.slider({ label: L.m, min: 0, max: 1, step: 0.05, value: cfg.m != null ? cfg.m : 0.2, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const sb = FV.ui.check({ label: L.showBatch, checked: cfg.batch !== false, onchange: () => draw() });
    w.controls.append(sm.el, sb.el);
    const ro = FV.ui.readout(w.readout, [{ key: "l", label: L.loss, c: "orange" }, { key: "r", label: L.regime + ":" }, { key: "c", label: L.cnt + " =" }]);
    let pt = (cfg.pt || [0.9, 1.0]).slice();
    const h = p.handle(pt[0], pt[1], { c: "orange", onDrag: (x, y) => { pt = [x, y]; return pt; }, onChange: () => draw() });
    function draw() {
      const m = sm.value, f = (x, y) => Math.max(0, x - y + m);
      p.clear();
      p.heat(f, { cmap: "diverging", z: [-2.4, 2.4], res: 4, alpha: 0.9 });
      p.contours(f, [0.5, 1, 1.5, 2], { c: "ink", w: 1, opacity: 0.25, dash: "3 4" });
      p.line(0, 0, 2.2, 2.2, { c: "red", w: 2 });
      p.line(0, m, 2.2 - m, 2.2, { c: "ink", w: 2 });
      const cnt = { easy: 0, semi: 0, hard: 0 };
      T.forEach((t) => { cnt[regime(t.dap, t.dan, m)]++; });
      if (sb.value) T.forEach((t) => p.dot(t.dap, t.dan, { c: REG_C[regime(t.dap, t.dan, m)], r: 2.2 }));
      p.text(1.05, 2.1, L.easy, { c: "teal" });
      p.text(2.1, 0.15, L.hard, { c: "red", anchor: "end" });
      const sx = 1.65, sy = sx + m / 2;
      if (m >= 0.15) p.text(sx - 0.08, sy, L.semi, { c: "violet", anchor: "end" });
      const l = f(pt[0], pt[1]);
      h.set(pt[0], pt[1]);
      ro.set("l", FV.fmt(l, 3)); ro.set("r", L[regime(pt[0], pt[1], m)]); ro.set("c", cnt.easy + " / " + cnt.semi + " / " + cnt.hard);
      p.legend([{ label: "d(a, n) = d(a, p)", c: "red" }, { label: "d(a, n) = d(a, p) + m", c: "ink" }, { label: L.easy, c: "teal", dot: true }, { label: L.semi, c: "violet", dot: true }, { label: L.hard, c: "red", dot: true }]);
    }
    p.onresize = draw; draw();
  });

  // 4. 3D: the loss as a function of where the negative (or the positive) is.
  FV.widget("triplet-surface", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const A = [0, 0], PF = [0.6, 0], NF = [-1.2, 0];
    let who = cfg.who || "neg", sqr = !!cfg.squared;
    const sm = FV.ui.slider({ label: L.m, min: 0.05, max: 1, step: 0.05, value: cfg.m != null ? cfg.m : 0.4, fmt: (v) => FV.fmt(v, 2), oninput: () => { refresh(); } });
    const lossAt = (x, y) => {
      const m = sm.value, r = Math.hypot(x, y);
      if (who === "neg") { const dp = dist(A, PF); return sqr ? Math.max(0, dp * dp - r * r + m) : Math.max(0, dp - r + m); }
      const dn = dist(A, NF); return sqr ? Math.max(0, r * r - dn * dn + m) : Math.max(0, r - dn + m);
    };
    // z ranges cover the largest loss at m = 1 (corner of the square for the positive), so nothing is clipped
  const zr = () => (who === "neg" ? [0, 1.6] : sqr ? [0, 7.6] : [0, 2.7]);
    const s3 = new FV.Surface(FV.col(w.stage), { f: lossAt, x: [-2, 2], y: [-2, 2], z: zr(), n: 44, labels: { x: "x", y: "y", z: "L" }, azimuth: -0.6, elevation: 0.55, aspect: 0.85, cmap: "viridis", title: "L(x, y)" });
    const p = new FV.Plot(FV.col(w.stage), { x: [0, 2.8], y: [0, 2.6], xLabel: L.r, yLabel: "L, |∇L|", aspect: 0.85, title: L.ray });
    const sw = FV.ui.seg({ label: L.who, value: who, options: [{ value: "neg", label: L.negMode }, { value: "pos", label: L.posMode }], onchange: (v) => { who = v; refresh(); } });
    const sd = FV.ui.seg({ label: L.dist, value: sqr ? "sq" : "d", options: [{ value: "d", label: L.plain }, { value: "sq", label: L.sqd }], onchange: (v) => { sqr = v === "sq"; refresh(); } });
    w.controls.append(sw.el, sd.el, sm.el);
    const ro = FV.ui.readout(w.readout, [{ key: "h", label: "L(a) =" }, { key: "r", label: L.bound, c: "teal" }]);
    function refresh() {
      const m = sm.value;
      s3.setF(lossAt, zr());
      const fixed = who === "neg" ? PF : NF;
      // the circle where the loss turns on / off
      const dp = dist(A, PF), dn = dist(A, NF);
      const R = who === "neg" ? (sqr ? Math.sqrt(dp * dp + m) : dp + m) : sqr ? Math.sqrt(Math.max(0, dn * dn - m)) : Math.max(0, dn - m);
      const ring = FV.linspace(0, 2 * Math.PI, 90).map((t) => [R * Math.cos(t), R * Math.sin(t), 0]);
      s3.setPaths([{ pts: ring, c: "teal", w: 2 }]);
      s3.setPoints([{ x: A[0], y: A[1], z: lossAt(A[0], A[1]), c: "ink", label: "a" }, { x: fixed[0], y: fixed[1], z: lossAt(fixed[0], fixed[1]), c: who === "neg" ? "blue" : "red", label: who === "neg" ? "p" : "n" }]);
      p.setDomain(null, [0, who === "pos" && sqr ? 7.5 : 2.6]);
      p.clear();
      const lr = (r) => lossAt(r, 0), g = (r) => (lossAt(r, 0) > 0 ? (sqr ? 2 * r : 1) : 0);
      p.vline(R, { c: "teal" });
      p.fn(lr, { c: "blue", w: 2.4 });
      p.fn(g, { c: "orange", w: 2.2, jump: 0.05 });
      p.legend([{ label: "L(r)", c: "blue" }, { label: "|∇L|", c: "orange" }, { label: L.bound.replace(" =", ""), c: "teal", dash: true }]);
      ro.set("h", FV.fmt(lossAt(0, 0), 3)); ro.set("r", FV.fmt(R, 3));
    }
    p.onresize = refresh; refresh();
  });

  // 5. Mining inside a batch: batch-hard versus batch-all.
  FV.widget("triplet-mining", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-2.2, 2.2], y: [-1.75, 1.75], equal: true, xLabel: L.x1, yLabel: L.x2 });
    const pts = batch(), T = triplets(pts);
    const sa = FV.ui.slider({ label: L.anc, min: 1, max: pts.length, step: 1, value: cfg.anchor || 1, fmt: (v) => String(v), oninput: draw });
    const sm = FV.ui.slider({ label: L.m, min: 0, max: 1, step: 0.05, value: cfg.m != null ? cfg.m : 0.2, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    const st = FV.ui.seg({ label: L.strat, value: cfg.strategy || "hard", options: [{ value: "hard", label: L.bh }, { value: "all", label: L.ba }], onchange: () => draw() });
    w.controls.append(st.el, sa.el, sm.el);
    const ro = FV.ui.readout(w.readout, [{ key: "c", label: L.forA }, { key: "h", label: L.lbh, c: "orange" }, { key: "a", label: L.lba, c: "orange" }, { key: "n", label: L.act }]);
    function draw() {
      const m = sm.value, ai = sa.value - 1, A = pts[ai];
      const mine = T.filter((t) => t.a === ai);
      let hp = -1, hpd = -1, hn = -1, hnd = Infinity;
      mine.forEach((t) => { if (t.dap > hpd) { hpd = t.dap; hp = t.p; } if (t.dan < hnd) { hnd = t.dan; hn = t.n; } });
      const cnt = { easy: 0, semi: 0, hard: 0 };
      mine.forEach((t) => cnt[regime(t.dap, t.dan, m)]++);
      p.clear();
      if (st.value === "hard") {
        circle(p, A.x, A.y, hpd + m, { c: "orange", w: 1.4, dash: "5 4" });
        p.line(A.x, A.y, pts[hp].x, pts[hp].y, { c: ID_C[A.c], w: 3 });
        p.line(A.x, A.y, pts[hn].x, pts[hn].y, { c: "red", w: 3 });
      } else {
        const act = new Set();
        mine.forEach((t) => { if (t.dap - t.dan + m > 0) act.add(t.n); });
        pts.forEach((q, i) => { if (q.c === A.c && i !== ai) p.line(A.x, A.y, q.x, q.y, { c: ID_C[A.c], w: 2 }); });
        act.forEach((i) => p.line(A.x, A.y, pts[i].x, pts[i].y, { c: "red", w: 1.4, dash: "4 3" }));
      }
      pts.forEach((q, i) => p.dot(q.x, q.y, { c: ID_C[q.c], r: i === ai ? 8 : 5 }));
      p.dot(A.x, A.y, { c: "ink", r: 3 });
      const B = batchLosses(pts, m);
      ro.set("c", cnt.easy + " / " + cnt.semi + " / " + cnt.hard);
      ro.set("h", FV.fmt(B.hard, 3)); ro.set("a", FV.fmt(B.all, 3)); ro.set("n", B.active + " / " + B.total);
      const leg = [1, 2, 3, 4].map((k) => ({ label: L.ident + " " + k, c: ID_C[k - 1], dot: true }));
      p.legend(leg.concat(st.value === "hard" ? [{ label: L.hardP + " / " + L.hardN, c: "red" }, { label: "d_max(a, p) + m", c: "orange", dash: true }] : [{ label: L.activeN, c: "red", dash: true }]));
    }
    p.onresize = draw; draw();
  });

  // 6. Training an embedding network with the batch-hard triplet loss.
  FV.widget("triplet-train", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const a = new FV.Plot(FV.col(w.stage), { x: [-3.2, 3.2], y: [-2.2, 2.2], xLabel: L.nuis, yLabel: "x₂", aspect: 0.8, title: L.input });
    const b = new FV.Plot(FV.col(w.stage), { x: [-3, 3], y: [-3, 3], xLabel: L.x1, yLabel: L.x2, aspect: 0.8, title: L.emb });
    const c = new FV.Plot(FV.col(w.stage), { x: [0, 600], y: [0, 1.4], xLabel: L.step, yLabel: L.lossT, aspect: 0.3, minHeight: 170, maxHeight: 220, title: L.lossCurve });
    c.wrap.parentNode.style.flexBasis = "100%";
    const pts = trainData(), MAXS = 600, PER = 3, m = cfg.m || 0.5, lr = 0.01, H = 12;
    let M, step, hist, E, ev;
    const player = FV.ui.player({
      interval: 60,
      onstep() { for (let k = 0; k < PER && step < MAXS; k++) { M.step(pts, m, lr); step++; } snap(); draw(); return step < MAXS; },
      onreset() { reset(); draw(); },
    });
    w.controls.append(player.el);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.step + " =" }, { key: "l", label: L.lossT + " =", c: "orange" }, { key: "a", label: L.actA + " =" }, { key: "o", label: L.order + " =", c: "blue" }]);
    function snap() { E = M.embed(pts); ev = evalEmb(E, pts, m); hist.push([step, ev.loss]); }
    function reset() { M = embedNet(H, 4); step = 0; hist = []; snap(); }
    function fit(pl, xs, ys) {
      // keep the embedding cloud in view: a square domain that grows with it
      let r = 1;
      xs.forEach((v, i) => { r = Math.max(r, Math.abs(v), Math.abs(ys[i])); });
      r = Math.ceil(r * 1.15 * 2) / 2;
      if (pl.o.x[1] !== r) pl.setDomain([-r, r], [-r, r]);
    }
    function draw() {
      a.clear();
      pts.forEach((q) => a.dot(q.x, q.y, { c: ID_C[q.c], r: 4.5 }));
      fit(b, E.map((e) => e[0]), E.map((e) => e[1]));
      b.clear();
      pts.forEach((q, i) => b.dot(E[i][0], E[i][1], { c: ID_C[q.c], r: 4.5 }));
      c.clear();
      c.path(hist.map((h) => [h[0], h[1]]), { c: "orange", w: 2.2 });
      const last = hist[hist.length - 1];
      c.dot(last[0], last[1], { c: "orange", r: 4 });
      ro.set("s", String(step)); ro.set("l", FV.fmt(ev.loss, 3)); ro.set("a", ev.active + " / " + pts.length); ro.set("o", FV.fmt(100 * ev.order, 1) + "%");
      b.legend([1, 2, 3, 4].map((k) => ({ label: L.ident + " " + k, c: ID_C[k - 1], dot: true })));
    }
    a.onresize = draw; b.onresize = draw; c.onresize = draw;
    reset(); draw();
  });

  // 7. Normalized embeddings: points on the unit circle, d² = 2 − 2 cos θ, FaceNet margin.
  FV.widget("triplet-sphere", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const p = new FV.Plot(FV.col(w.stage), { x: [-1.35, 1.35], y: [-1.35, 1.35], equal: true, xLabel: L.x1, yLabel: L.x2, title: L.circle });
    const q = new FV.Plot(FV.col(w.stage), { x: [0, 180], y: [0, 4.2], xLabel: L.ang + " θ, °", yLabel: "d²", aspect: 0.85, xTicks: [0, 30, 60, 90, 120, 150, 180], title: L.dsq });
    const rad = (d) => (d * Math.PI) / 180, deg = (r) => (r * 180) / Math.PI;
    const ang = { a: rad(cfg.a != null ? cfg.a : 0), p: rad(cfg.p != null ? cfg.p : 40), n: rad(cfg.n != null ? cfg.n : -45) };
    const sm = FV.ui.slider({ label: L.m, min: 0, max: 1, step: 0.05, value: cfg.m != null ? cfg.m : 0.2, fmt: (v) => FV.fmt(v, 2), oninput: draw });
    w.controls.append(sm.el);
    const ro = FV.ui.readout(w.readout, [{ key: "ap", label: L.thAP, c: "blue" }, { key: "an", label: L.thAN, c: "red" }, { key: "d", label: "d²(a, p) / d²(a, n) =" }, { key: "l", label: L.loss, c: "orange" }, { key: "need", label: L.need }]);
    const mk = (k, c) => p.handle(Math.cos(ang[k]), Math.sin(ang[k]), { c, onDrag: (x, y) => { ang[k] = Math.atan2(y, x); return [Math.cos(ang[k]), Math.sin(ang[k])]; }, onChange: () => draw() });
    const H = { a: mk("a", "ink"), p: mk("p", "blue"), n: mk("n", "red") };
    const between = (u, v) => { let d = Math.abs(u - v) % (2 * Math.PI); return d > Math.PI ? 2 * Math.PI - d : d; };
    function draw() {
      const m = sm.value, tp = between(ang.a, ang.p), tn = between(ang.a, ang.n);
      const dp = 2 - 2 * Math.cos(tp), dn = 2 - 2 * Math.cos(tn), l = Math.max(0, dp - dn + m);
      // need = the smallest angle θ(a, n) that satisfies the margin; if cos θ would have to drop below −1, no angle does
      const cosNeed = Math.cos(tp) - m / 2, need = cosNeed < -1 ? NaN : deg(Math.acos(Math.min(1, cosNeed)));
      p.clear();
      circle(p, 0, 0, 1, { c: "guide", w: 1.4 });
      if (!Number.isFinite(need)) circle(p, 0, 0, 1, { c: "orange", w: 6, opacity: 0.35 });   // the whole circle violates
      else {
        const arc = [];
        for (let i = 0; i <= 60; i++) { const t = -rad(need) + (2 * rad(need) * i) / 60; arc.push([Math.cos(ang.a + t), Math.sin(ang.a + t)]); }
        p.path(arc, { c: "orange", w: 6, opacity: 0.35 });
      }
      const A = [Math.cos(ang.a), Math.sin(ang.a)], P = [Math.cos(ang.p), Math.sin(ang.p)], N = [Math.cos(ang.n), Math.sin(ang.n)];
      p.line(A[0], A[1], P[0], P[1], { c: "blue", w: 2 }); p.line(A[0], A[1], N[0], N[1], { c: "red", w: 2 });
      p.line(0, 0, A[0], A[1], { c: "faint", w: 1, dash: "3 3" });
      [["a", A, "ink"], ["p", P, "blue"], ["n", N, "red"]].forEach(([s, v, c]) => p.text(v[0] * 1.2, v[1] * 1.2 - 0.04, s, { anchor: "middle", c }));
      H.a.set(A[0], A[1]); H.p.set(P[0], P[1]); H.n.set(N[0], N[1]);
      p.legend([{ label: L.anchor, c: "ink", dot: true }, { label: L.pos, c: "blue", dot: true }, { label: L.neg, c: "red", dot: true }, { label: L.zone, c: "orange", box: true }]);
      q.clear();
      q.fn((t) => 2 - 2 * Math.cos(rad(t)), { c: "ink", w: 2.2 });
      q.hline(dp + m, { c: "orange", dash: "5 4", w: 1.4 });
      if (Number.isFinite(need)) q.vline(need, { c: "orange" });
      q.line(deg(tp), 0, deg(tp), dp, { c: "blue", w: 1, dash: "3 3" }); q.dot(deg(tp), dp, { c: "blue" });
      q.line(deg(tn), 0, deg(tn), dn, { c: "red", w: 1, dash: "3 3" }); q.dot(deg(tn), dn, { c: "red" });
      q.legend([{ label: "d²(θ)", c: "ink" }, { label: "d²(a, p) + m", c: "orange", dash: true }]);
      ro.set("ap", FV.fmt(deg(tp), 1) + "°"); ro.set("an", FV.fmt(deg(tn), 1) + "°");
      ro.set("d", FV.fmt(dp, 3) + " / " + FV.fmt(dn, 3)); ro.set("l", FV.fmt(l, 3));
      ro.set("need", Number.isFinite(need) ? FV.fmt(need, 1) + "°" : L.never);
    }
    p.onresize = draw; q.onresize = draw; draw();
  });
})();
