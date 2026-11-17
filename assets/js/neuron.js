/* Widgets of the article "The formula of a single neuron". Built on FV (assets/js/viz.js).
   a = f(Σ wᵢxᵢ + b) = f(wᵀx + b) */
(function () {
  "use strict";
  if (typeof FV === "undefined" || !FV.widget) return;

  const L = {
    ru: {
      identity: "тождественная", step: "ступенька", sigmoid: "сигмоида", tanh: "tanh", relu: "ReLU",
      inputs: "входы", weights: "веса", sum: "сумма", act: "активация", out: "выход", bias: "смещение",
      anatomyAria: "Схема нейрона: входы, веса, сумматор, функция активации и выход",
      fOf: "Функция $f$",
      steps0: "Нажмите «Шаг» или «Пуск»: вклады будут складываться по одному.",
      stepProd: (i) => `Вклад входа ${i}:`, stepCum: "накопленная сумма", stepBias: "Добавляем смещение:", stepZ: "Взвешенная сумма готова:", stepA: "Активация — сигмоида:",
      other: "Другой пример", ours: "Наш пример", cum: "накопленная сумма",
      dotProj: "проекция $\\mathbf{x}$ на $\\mathbf{w}$", sumForm: "$w_1x_1+w_2x_2$ =", cosForm: "$\\lVert\\mathbf{w}\\rVert\\lVert\\mathbf{x}\\rVert\\cos\\theta$ =", angle: "$\\theta$ =",
      agree: "Угол меньше 90°: вход похож на шаблон весов, вклад положительный.", ortho: "Угол 90°: вход перпендикулярен весам, вклад нулевой.", against: "Угол больше 90°: вход направлен против весов, вклад отрицательный.",
      boundary: "граница $a=0{,}5$", dist: "расстояние", wLen: "$\\lVert\\mathbf{w}\\rVert$ =", b: "Смещение $b$", w1: "Вес $w_1$", w2: "Вес $w_2$", w: "Вес $w$",
      zAt: "$z(\\mathbf{x})$ =", aAt: "$a(\\mathbf{x})$ =", dAt: "$d(\\mathbf{x})$ =", origin: "$|b|/\\lVert\\mathbf{w}\\rVert$ =",
      mode: "Выход", x0: "порог $x_0=-b/w$ =", noBias: "без смещения", withBias: "$f(wx+b)$", a0: "$f(b)$ при $x=0$:", slope: "наклон в $x_0$:",
      zLbl: "Предактивация $z$", deriv: "Показать производную $f'(z)$",
      gate: "Вентиль", train: "Обучение перцептрона", solution: "Готовое решение", epoch: "эпоха", errors: "ошибок сейчас",
      converged: (n) => `Готово: все четыре точки верны после эпохи ${n}.`, noLine: (n) => `После ${n} эпох ошибки остаются: для XOR такой прямой не существует.`,
      noSolution: "Для XOR готового решения нет: одной прямой точки не разделить.", ok: "верно", bad: "ошибка",
      colIn: "входы $x$ (щёлкните)", colW: "веса $w$", colP: "произведения $w_ix_i$", kernel: "Шаблон", vertical: "вертикальная граница", horizontal: "горизонтальная граница", spot: "пятно",
      preset: "Фрагмент", pEdge: "граница", pUniform: "однородный", pH: "гориз. граница", pDot: "точка", pClear: "чёрный",
      fired: "нейрон сработал", silent: "нейрон молчит",
      exam1: "балл по математике", exam2: "балл по языку", target: "Функция", neurons: "Нейронов ReLU", parts: "Показать отдельные нейроны", params: "параметров:", maxErr: "макс. ошибка:", sumRelu: "сумма нейронов", oneRelu: "вклад одного нейрона",
      morph: "Вход → скрытый слой", morph0: "Входное пространство: никакая прямая не отделяет закрашенные точки от пустых. Бирюзовая прямая — граница нейрона OR, фиолетовая — NAND.", morph1: "Скрытое пространство $(h_1;\\ h_2)$: точки $(0;\\ 1)$ и $(1;\\ 0)$ слились в $(1;\\ 1)$, и теперь одна прямая AND их отделяет.", morphMid: "Скрытый слой переносит каждую точку в новые координаты $(h_1;\\ h_2)$.",
      eta: "Шаг обучения $\\eta$", loss: "BCE", acc: "точность", epochN: "шаг", class0: "класс 0", class1: "класс 1", lossTitle: "Потери по шагам",
    },
    en: {
      identity: "identity", step: "step", sigmoid: "sigmoid", tanh: "tanh", relu: "ReLU",
      inputs: "inputs", weights: "weights", sum: "sum", act: "activation", out: "output", bias: "bias",
      anatomyAria: "A neuron diagram: inputs, weights, summation, activation function and output",
      fOf: "Function $f$",
      steps0: "Press “Step” or “Play”: the contributions will be added one by one.",
      stepProd: (i) => `Contribution of input ${i}:`, stepCum: "running sum", stepBias: "Add the bias:", stepZ: "The weighted sum is ready:", stepA: "Activation — the sigmoid:",
      other: "Another example", ours: "Our example", cum: "running sum",
      dotProj: "projection of $\\mathbf{x}$ onto $\\mathbf{w}$", sumForm: "$w_1x_1+w_2x_2$ =", cosForm: "$\\lVert\\mathbf{w}\\rVert\\lVert\\mathbf{x}\\rVert\\cos\\theta$ =", angle: "$\\theta$ =",
      agree: "The angle is below 90°: the input resembles the weight template, the contribution is positive.", ortho: "The angle is 90°: the input is perpendicular to the weights, the contribution is zero.", against: "The angle is above 90°: the input points against the weights, the contribution is negative.",
      boundary: "boundary $a=0.5$", dist: "distance", wLen: "$\\lVert\\mathbf{w}\\rVert$ =", b: "Bias $b$", w1: "Weight $w_1$", w2: "Weight $w_2$", w: "Weight $w$",
      zAt: "$z(\\mathbf{x})$ =", aAt: "$a(\\mathbf{x})$ =", dAt: "$d(\\mathbf{x})$ =", origin: "$|b|/\\lVert\\mathbf{w}\\rVert$ =",
      mode: "Output", x0: "threshold $x_0=-b/w$ =", noBias: "without bias", withBias: "$f(wx+b)$", a0: "$f(b)$ at $x=0$:", slope: "slope at $x_0$:",
      zLbl: "Pre-activation $z$", deriv: "Show the derivative $f'(z)$",
      gate: "Gate", train: "Perceptron learning", solution: "Known solution", epoch: "epoch", errors: "errors now",
      converged: (n) => `Done: all four points are correct after epoch ${n}.`, noLine: (n) => `After ${n} epochs errors remain: no such line exists for XOR.`,
      noSolution: "There is no known solution for XOR: a single line cannot separate the points.", ok: "correct", bad: "error",
      colIn: "inputs $x$ (click)", colW: "weights $w$", colP: "products $w_ix_i$", kernel: "Template", vertical: "vertical edge", horizontal: "horizontal edge", spot: "spot",
      preset: "Patch", pEdge: "edge", pUniform: "uniform", pH: "horiz. edge", pDot: "dot", pClear: "black",
      fired: "the neuron fires", silent: "the neuron is silent",
      exam1: "maths score", exam2: "language score", target: "Function", neurons: "ReLU neurons", parts: "Show individual neurons", params: "parameters:", maxErr: "max error:", sumRelu: "sum of neurons", oneRelu: "one neuron's contribution",
      morph: "Input → hidden layer", morph0: "Input space: no line separates the filled points from the hollow ones. The teal line is the boundary of the OR neuron, the violet one of NAND.", morph1: "Hidden space $(h_1,\\ h_2)$: the points $(0,\\ 1)$ and $(1,\\ 0)$ have merged into $(1,\\ 1)$, and now a single AND line separates them.", morphMid: "The hidden layer moves every point to new coordinates $(h_1,\\ h_2)$.",
      eta: "Learning rate $\\eta$", loss: "BCE", acc: "accuracy", epochN: "step", class0: "class 0", class1: "class 1", lossTitle: "Loss by step",
    },
    uz: {
      identity: "ayniy", step: "zina", sigmoid: "sigmoida", tanh: "tanh", relu: "ReLU",
      inputs: "kirishlar", weights: "vaznlar", sum: "yig‘indi", act: "aktivatsiya", out: "chiqish", bias: "siljish",
      anatomyAria: "Neyron sxemasi: kirishlar, vaznlar, yig‘uvchi, aktivatsiya funksiyasi va chiqish",
      fOf: "$f$ funksiya",
      steps0: "«Qadam» yoki «Boshlash»ni bosing: hissalar birma-bir qo‘shiladi.",
      stepProd: (i) => `${i}-kirishning hissasi:`, stepCum: "jamlangan yig‘indi", stepBias: "Siljishni qo‘shamiz:", stepZ: "Vaznli yig‘indi tayyor:", stepA: "Aktivatsiya — sigmoida:",
      other: "Boshqa misol", ours: "Bizning misol", cum: "jamlangan yig‘indi",
      dotProj: "$\\mathbf{x}$ ning $\\mathbf{w}$ ga proyeksiyasi", sumForm: "$w_1x_1+w_2x_2$ =", cosForm: "$\\lVert\\mathbf{w}\\rVert\\lVert\\mathbf{x}\\rVert\\cos\\theta$ =", angle: "$\\theta$ =",
      agree: "Burchak 90° dan kichik: kirish vaznlar shabloniga o‘xshaydi, hissa musbat.", ortho: "Burchak 90°: kirish vaznlarga perpendikulyar, hissa nolga teng.", against: "Burchak 90° dan katta: kirish vaznlarga qarshi yo‘nalgan, hissa manfiy.",
      boundary: "chegara $a=0{,}5$", dist: "masofa", wLen: "$\\lVert\\mathbf{w}\\rVert$ =", b: "Siljish $b$", w1: "Vazn $w_1$", w2: "Vazn $w_2$", w: "Vazn $w$",
      zAt: "$z(\\mathbf{x})$ =", aAt: "$a(\\mathbf{x})$ =", dAt: "$d(\\mathbf{x})$ =", origin: "$|b|/\\lVert\\mathbf{w}\\rVert$ =",
      mode: "Chiqish", x0: "chegara $x_0=-b/w$ =", noBias: "siljishsiz", withBias: "$f(wx+b)$", a0: "$x=0$ da $f(b)$:", slope: "$x_0$ dagi qiyalik:",
      zLbl: "Preaktivatsiya $z$", deriv: "$f'(z)$ hosilani ko‘rsatish",
      gate: "Ventil", train: "Perseptronni o‘qitish", solution: "Tayyor yechim", epoch: "davr", errors: "hozirgi xatolar",
      converged: (n) => `Tayyor: ${n}-davrdan keyin to‘rtala nuqta ham to‘g‘ri.`, noLine: (n) => `${n} davrdan keyin ham xatolar qolmoqda: XOR uchun bunday to‘g‘ri chiziq yo‘q.`,
      noSolution: "XOR uchun tayyor yechim yo‘q: nuqtalarni bitta to‘g‘ri chiziq bilan ajratib bo‘lmaydi.", ok: "to‘g‘ri", bad: "xato",
      colIn: "kirishlar $x$ (bosing)", colW: "vaznlar $w$", colP: "ko‘paytmalar $w_ix_i$", kernel: "Shablon", vertical: "vertikal chegara", horizontal: "gorizontal chegara", spot: "dog‘",
      preset: "Fragment", pEdge: "chegara", pUniform: "bir xil", pH: "gor. chegara", pDot: "nuqta", pClear: "qora",
      fired: "neyron ishga tushdi", silent: "neyron jim",
      exam1: "matematika bali", exam2: "til bali", target: "Funksiya", neurons: "ReLU neyronlari", parts: "Alohida neyronlarni ko‘rsatish", params: "parametrlar:", maxErr: "maks. xato:", sumRelu: "neyronlar yig‘indisi", oneRelu: "bitta neyron hissasi",
      morph: "Kirish → yashirin qatlam", morph0: "Kirish fazosi: hech bir to‘g‘ri chiziq bo‘yalgan nuqtalarni bo‘sh nuqtalardan ajratmaydi. Firuza chiziq — OR neyronining chegarasi, binafsha — NAND.", morph1: "Yashirin fazo $(h_1;\\ h_2)$: $(0;\\ 1)$ va $(1;\\ 0)$ nuqtalar $(1;\\ 1)$ ga birlashdi, endi ularni bitta AND chizig‘i ajratadi.", morphMid: "Yashirin qatlam har bir nuqtani yangi $(h_1;\\ h_2)$ koordinatalarga ko‘chiradi.",
      eta: "O‘qitish qadami $\\eta$", loss: "BCE", acc: "aniqlik", epochN: "qadam", class0: "0-sinf", class1: "1-sinf", lossTitle: "Qadamlar bo‘yicha yo‘qotish",
    },
  }[FV.lang] || {};

  // ---------- shared math ----------
  const sig = FV.sigmoid;
  const ACT = {
    identity: { f: (z) => z, d: () => 1, sym: "z", c: "violet" },
    step: { f: (z) => (z >= 0 ? 1 : 0), d: () => 0, sym: "H(z)", c: "red" },
    sigmoid: { f: sig, d: (z) => { const s = sig(z); return s * (1 - s); }, sym: "σ(z)", c: "blue" },
    tanh: { f: Math.tanh, d: (z) => 1 - Math.tanh(z) ** 2, sym: "tanh z", c: "teal" },
    relu: { f: (z) => Math.max(0, z), d: (z) => (z > 0 ? 1 : 0), sym: "ReLU(z)", c: "orange" },
  };
  const ACT_IDS = ["identity", "step", "sigmoid", "tanh", "relu"];
  const SEP = FV.lang === "en" ? ", " : "; ";
  const SUB = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"];
  const n4 = (v) => FV.num(Math.abs(v) < 1e-12 ? 0 : v, 4);
  // A number for TeX: decimal comma as {,} in ru/uz, a real minus, negatives in parentheses on demand.
  const tn = (v, paren) => {
    const s = n4(v).replace("−", "-").replace(",", "{,}");
    return paren && v < 0 ? `(${s})` : s;
  };
  const reduced = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const S = FV.svg;

  // Segment of the line a·x + b·y + c = 0 inside the box [x0,x1]×[y0,y1], or null.
  function clipLine(a, b, c, x0, x1, y0, y1) {
    const pts = [];
    if (Math.abs(b) > 1e-9) [x0, x1].forEach((x) => { const y = -(a * x + c) / b; if (y >= y0 - 1e-9 && y <= y1 + 1e-9) pts.push([x, y]); });
    if (Math.abs(a) > 1e-9) [y0, y1].forEach((y) => { const x = -(b * y + c) / a; if (x >= x0 - 1e-9 && x <= x1 + 1e-9) pts.push([x, y]); });
    if (pts.length < 2) return null;
    let best = null, bd = -1;
    for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
      const d = Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]);
      if (d > bd) { bd = d; best = [pts[i], pts[j]]; }
    }
    return bd > 1e-9 ? best : null;
  }
  // The part of the box where a·x + b·y + c ≥ 0 (Sutherland–Hodgman against one half-plane).
  function halfPlane(a, b, c, x0, x1, y0, y1) {
    const poly = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], out = [];
    const v = (p) => a * p[0] + b * p[1] + c;
    for (let i = 0; i < 4; i++) {
      const p = poly[i], q = poly[(i + 1) % 4], vp = v(p), vq = v(q);
      if (vp >= 0) out.push(p);
      if ((vp >= 0) !== (vq >= 0)) { const t = vp / (vp - vq); out.push([p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t]); }
    }
    return out;
  }
  const vec = (arr) => "(" + arr.map(n4).join(SEP) + ")";

  // ======================================================================
  // 1. Anatomy: the animated neuron diagram
  // ======================================================================
  FV.widget("neuron-anatomy", (el, cfg) => {
    const st = { x: (cfg.x || [2, -1, 3]).slice(), w: (cfg.w || [0.5, -1, 0.25]).slice(), b: cfg.b != null ? cfg.b : -0.75, f: cfg.f || "sigmoid" };
    const n = st.x.length;
    const w = FV.shell(el, {});
    const box = FV.h("div", { class: "nr-diagram" });
    w.stage.append(box);
    const svg = S("svg", { class: "fv-svg nr-svg", role: "img", "aria-label": L.anatomyAria });
    box.append(svg);
    const gEdges = S("g", {}, svg), gNodes = S("g", {}, svg), gPulse = S("g", { class: "nr-pulses" }, svg);

    // controls: inputs, weights, bias, activation, play
    const fmt2 = (v) => FV.fmt(v, 2);
    const xs = st.x.map((v, i) => FV.ui.slider({ label: `$x_${i + 1}$`, min: -3, max: 3, step: 0.25, value: v, fmt: fmt2, oninput: (u) => { st.x[i] = u; draw(); } }));
    const ws = st.w.map((v, i) => FV.ui.slider({ label: `$w_${i + 1}$`, min: -2, max: 2, step: 0.05, value: v, fmt: fmt2, oninput: (u) => { st.w[i] = u; draw(); } }));
    const bs = FV.ui.slider({ label: "$b$", min: -3, max: 3, step: 0.05, value: st.b, fmt: fmt2, oninput: (u) => { st.b = u; draw(); } });
    const grid = FV.h("div", { class: "nr-sliders" },
      FV.h("div", { class: "nr-sl-col" }, FV.h("span", { class: "nr-sl-h", text: L.inputs }), xs.map((s) => s.el)),
      FV.h("div", { class: "nr-sl-col" }, FV.h("span", { class: "nr-sl-h", text: L.weights }), ws.map((s) => s.el)),
      FV.h("div", { class: "nr-sl-col" }, FV.h("span", { class: "nr-sl-h", text: L.bias }), bs.el));
    const seg = FV.ui.seg({ label: L.fOf, value: st.f, options: ACT_IDS.map((k) => ({ value: k, label: L[k] })), onchange: (v) => { st.f = v; draw(); } });
    let running = false, visible = true, raf = 0, t0 = 0;
    const play = FV.ui.button({ label: "▶ " + FV.t("play"), primary: true, onclick: () => (running ? stop() : start()) });
    w.controls.append(grid, seg.el, play.el);
    const ro = FV.ui.readout(w.readout, [{ key: "z", label: "$z$ =", c: "blue" }, { key: "a", label: "$a=f(z)$ =", c: "orange" }]);

    let G = null; // geometry of the last layout
    const val = () => {
      const p = st.x.map((x, i) => st.w[i] * x);
      const z = p.reduce((s, v) => s + v, 0) + st.b;
      return { p, z, a: ACT[st.f].f(z) };
    };
    const cls = (v) => (Math.abs(v) < 1e-9 ? "faint" : v > 0 ? "blue" : "red");

    function layout() {
      const W = Math.max(300, Math.round(box.clientWidth || 640));
      const nar = W < 560;
      const H = nar ? 290 : 340;
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`); svg.setAttribute("width", W); svg.setAttribute("height", H);
      const rIn = nar ? 17 : 22, rS = nar ? 21 : 28;
      const xIn = nar ? 26 : 64, yTop = nar ? 52 : 60, yBot = H - (nar ? 34 : 46);
      const ins = st.x.map((_, i) => [xIn, n === 1 ? (yTop + yBot) / 2 : yTop + ((yBot - yTop) * i) / (n - 1)]);
      const cy = (yTop + yBot) / 2 + (nar ? 14 : 18);
      const sum = [W * (nar ? 0.5 : 0.5), cy];
      const bias = [sum[0], nar ? 22 : 26];
      const aw = nar ? 58 : 86, ah = nar ? 46 : 64;
      const act = [W * (nar ? 0.73 : 0.735), cy];
      const out = [W - (nar ? 24 : 52), cy];
      G = { W, H, nar, rIn, rS, ins, sum, bias, act, aw, ah, out };
    }
    const towards = (p, q, r) => { const d = Math.hypot(q[0] - p[0], q[1] - p[1]) || 1; return [p[0] + ((q[0] - p[0]) * r) / d, p[1] + ((q[1] - p[1]) * r) / d]; };
    const txt = (parent, x, y, s, c, anchor = "middle") => { const t = S("text", { x, y, "text-anchor": anchor, class: c }, parent); t.textContent = s; return t; };

    function draw() {
      if (!G) layout();
      const { W, nar, rIn, rS, ins, sum, bias, act, aw, ah, out } = G;
      const v = val();
      gEdges.textContent = ""; gNodes.textContent = "";
      // input → Σ edges
      ins.forEach((p, i) => {
        const a = towards(p, sum, rIn), b = towards(sum, p, rS);
        S("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: "nr-edge s-" + cls(v.p[i]), "stroke-width": 1.2 + 2.6 * Math.abs(st.w[i]) }, gEdges);
        const wl = [a[0] + (b[0] - a[0]) * 0.36, a[1] + (b[1] - a[1]) * 0.36];
        txt(gEdges, wl[0], wl[1] - 8, (nar ? "" : `w${SUB[i + 1]} = `) + n4(st.w[i]), "nr-t nr-w");
        const pl = [a[0] + (b[0] - a[0]) * 0.74, a[1] + (b[1] - a[1]) * 0.74];
        txt(gEdges, pl[0], pl[1] + (i === 0 ? -9 : i === n - 1 ? 17 : -9), (v.p[i] >= 0 ? "+" : "") + n4(v.p[i]), "nr-t nr-p t-" + cls(v.p[i]));
      });
      // bias edge
      { const a = towards(bias, sum, 11), b = towards(sum, bias, rS);
        S("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: "nr-edge s-" + cls(st.b), "stroke-width": 1.2 + 1.2 * Math.abs(st.b), "stroke-dasharray": "5 4" }, gEdges); }
      // Σ → f → a
      S("line", { x1: sum[0] + rS, y1: sum[1], x2: act[0] - aw / 2, y2: act[1], class: "nr-edge s-ink", "stroke-width": 1.6 }, gEdges);
      S("line", { x1: act[0] + aw / 2, y1: act[1], x2: out[0] - rIn, y2: out[1], class: "nr-edge s-ink", "stroke-width": 1.6 }, gEdges);
      txt(gEdges, (sum[0] + rS + act[0] - aw / 2) / 2, sum[1] - 9, "z = " + n4(v.z), "nr-t nr-z");
      txt(gEdges, (act[0] + aw / 2 + out[0] - rIn) / 2, out[1] - 9, nar ? "" : "a", "nr-t nr-w");

      // input nodes
      ins.forEach((p, i) => {
        S("circle", { cx: p[0], cy: p[1], r: rIn, class: "nr-node" }, gNodes);
        txt(gNodes, p[0], p[1] + 4.5, n4(st.x[i]), "nr-v");
        if (!nar) txt(gNodes, p[0] - rIn - 8, p[1] + 4.5, "x" + SUB[i + 1], "nr-t nr-lbl", "end");
        else txt(gNodes, p[0], p[1] - rIn - 5, "x" + SUB[i + 1], "nr-t nr-lbl");
      });
      // bias node
      S("circle", { cx: bias[0], cy: bias[1], r: 11, class: "nr-node nr-bias" }, gNodes);
      txt(gNodes, bias[0], bias[1] + 4, "b", "nr-v nr-small");
      txt(gNodes, bias[0] + 18, bias[1] + 4.5, "= " + n4(st.b), "nr-t", "start");
      // Σ node
      G.sumEl = S("circle", { cx: sum[0], cy: sum[1], r: rS, class: "nr-node nr-sum" }, gNodes);
      txt(gNodes, sum[0], sum[1] + (nar ? 6 : 8), "Σ", "nr-v nr-big");
      if (!nar) txt(gNodes, sum[0], sum[1] + rS + 18, L.sum, "nr-t nr-cap");
      // activation box with a small graph of f
      const bx = act[0] - aw / 2, by = act[1] - ah / 2;
      S("rect", { x: bx, y: by, width: aw, height: ah, rx: 6, class: "nr-node" }, gNodes);
      const F = ACT[st.f];
      const yr = st.f === "identity" ? [-3, 3] : st.f === "relu" ? [-0.6, 3] : st.f === "tanh" ? [-1.25, 1.25] : [-0.2, 1.2];
      const mx = (z) => bx + 6 + ((z + 3) / 6) * (aw - 12), my = (y) => by + ah - 6 - ((FV.clamp(y, yr[0], yr[1]) - yr[0]) / (yr[1] - yr[0])) * (ah - 12);
      let d = "";
      for (let k = 0; k <= 60; k++) { const z = -3 + (6 * k) / 60; d += (k ? "L" : "M") + mx(z).toFixed(1) + " " + my(F.f(z)).toFixed(1); }
      S("path", { d, class: "nr-fcurve s-" + F.c, fill: "none" }, gNodes);
      const zc = FV.clamp(v.z, -3, 3);
      S("circle", { cx: mx(zc), cy: my(F.f(zc)), r: 3.5, class: "fill-orange" }, gNodes);
      txt(gNodes, act[0], by - 8, "f = " + F.sym.replace("(z)", "").replace(" z", ""), "nr-t nr-lbl");
      if (!nar) txt(gNodes, act[0], by + ah + 18, L.act, "nr-t nr-cap");
      // output node
      S("circle", { cx: out[0], cy: out[1], r: rIn, class: "nr-node nr-out" }, gNodes);
      txt(gNodes, out[0], out[1] + 4.5, FV.num(v.a, nar ? 2 : 3), "nr-v");
      if (!nar) txt(gNodes, out[0], out[1] + rIn + 18, L.out, "nr-t nr-cap");

      ro.set("z", n4(v.z)); ro.set("a", n4(v.a));
      const terms = st.x.map((x, i) => `${tn(st.w[i], true)}\\cdot ${tn(x, true)}`).join(" + ");
      w.note.textContent = "";
      w.note.append(FV.tex(`z = ${terms} + ${tn(st.b, true)} = ${tn(v.z)},\\qquad a = ${F.sym.replace("σ", "\\sigma").replace("tanh z", "\\tanh z").replace("ReLU", "\\mathrm{ReLU}").replace("(z)", "(" + tn(v.z) + ")").replace(" z", " " + tn(v.z, true)).replace(/^z$/, tn(v.z, true))} \\approx ${tn(v.a)}`));
      if (!running) pulses(-1);
    }

    // pulses: one dot per input edge, then one along Σ → f, then f → a
    const dots = [];
    function pulses(t) {
      if (!G) return;
      const { ins, sum, act, aw, out, rIn, rS } = G;
      const v = val();
      const need = ins.length + 2;
      while (dots.length < need) dots.push(S("circle", { r: 4, class: "nr-dot" }, gPulse));
      if (t < 0) { dots.forEach((d) => d.setAttribute("opacity", 0)); G.sumEl && G.sumEl.setAttribute("r", rS); return; }
      const maxP = Math.max(0.5, ...v.p.map(Math.abs));
      ins.forEach((p, i) => {
        const d = dots[i], a = towards(p, sum, rIn), b = towards(sum, p, rS), u = FV.clamp(t / 0.42, 0, 1);
        const on = t < 0.44 && Math.abs(v.p[i]) > 1e-9;
        d.setAttribute("cx", a[0] + (b[0] - a[0]) * u); d.setAttribute("cy", a[1] + (b[1] - a[1]) * u);
        d.setAttribute("r", 3 + 4.5 * (Math.abs(v.p[i]) / maxP));
        d.setAttribute("class", "nr-dot fill-" + cls(v.p[i]));
        d.setAttribute("opacity", on ? 0.95 : 0);
      });
      const ds = dots[ins.length], da = dots[ins.length + 1];
      const u1 = FV.clamp((t - 0.5) / 0.2, 0, 1), u2 = FV.clamp((t - 0.74) / 0.2, 0, 1);
      ds.setAttribute("cx", sum[0] + rS + (act[0] - aw / 2 - sum[0] - rS) * u1); ds.setAttribute("cy", sum[1]);
      ds.setAttribute("r", 3 + Math.min(5, Math.abs(v.z) * 1.4)); ds.setAttribute("class", "nr-dot fill-" + cls(v.z));
      ds.setAttribute("opacity", t >= 0.5 && t < 0.71 ? 0.95 : 0);
      da.setAttribute("cx", act[0] + aw / 2 + (out[0] - rIn - act[0] - aw / 2) * u2); da.setAttribute("cy", out[1]);
      da.setAttribute("r", 3 + Math.min(5, Math.abs(v.a) * 3)); da.setAttribute("class", "nr-dot fill-orange");
      da.setAttribute("opacity", t >= 0.74 && t < 0.95 ? 0.95 : 0);
      // Σ swells when the input pulses arrive
      const k = t >= 0.4 && t < 0.56 ? Math.sin(((t - 0.4) / 0.16) * Math.PI) : 0;
      G.sumEl && G.sumEl.setAttribute("r", rS * (1 + 0.16 * k));
    }
    function frame(now) {
      raf = 0;
      if (!running) return;
      if (visible) pulses(((now - t0) % 2600) / 2600);
      raf = requestAnimationFrame(frame);
    }
    function start() { running = true; play.setLabel("❚❚ " + FV.t("pause")); t0 = performance.now(); if (!raf) raf = requestAnimationFrame(frame); }
    function stop() { running = false; play.setLabel("▶ " + FV.t("play")); pulses(-1); }

    if ("ResizeObserver" in window) {
      let last = 0;
      new ResizeObserver(() => { const x = box.clientWidth; if (Math.abs(x - last) > 1) { last = x; layout(); draw(); } }).observe(box);
    }
    if ("IntersectionObserver" in window) new IntersectionObserver((es) => es.forEach((e) => { visible = e.isIntersecting; })).observe(el);
    layout(); draw();
    if (!reduced()) start();
  });

  // ======================================================================
  // 2. Steps: a waterfall of contributions, played step by step
  // ======================================================================
  FV.widget("neuron-steps", (el, cfg) => {
    const base = { x: (cfg.x || [2, -1, 3]).slice(), w: (cfg.w || [0.5, -1, 0.25]).slice(), b: cfg.b != null ? cfg.b : -0.75 };
    let ex = { x: base.x.slice(), w: base.w.slice(), b: base.b };
    const w = FV.shell(el, {});
    const ticks = () => ex.x.map((_, i) => ({ v: i, label: `w${SUB[i + 1]}x${SUB[i + 1]}` })).concat([{ v: ex.x.length, label: "b" }, { v: ex.x.length + 1, label: "z" }]);
    let p = null;
    const KMAX = () => ex.x.length + 3;
    let k = KMAX();
    const rng = FV.rng(11);
    function compute() {
      const prods = ex.x.map((x, i) => ex.w[i] * x);
      const items = prods.concat([ex.b]);
      const cum = [0];
      items.forEach((v) => cum.push(cum[cum.length - 1] + v));
      const z = cum[cum.length - 1];
      return { prods, items, cum, z, a: sig(z) };
    }
    function makePlot() {
      const c = compute();
      const lo = Math.min(0, ...c.cum), hi = Math.max(0, ...c.cum);
      const pad = Math.max(0.4, (hi - lo) * 0.18);
      if (p) { p.wrap.remove(); }
      p = new FV.Plot(w.stage, { x: [-0.6, ex.x.length + 1.6], y: [lo - pad, hi + pad], xTicks: ticks(), aspect: 0.48, minHeight: 240, maxHeight: 360, ariaLabel: L.cum });
      p.onresize = draw;
    }
    const player = FV.ui.player({ interval: 1100, onstep: () => { if (k >= KMAX()) k = 0; k++; draw(); return k < KMAX(); }, onreset: () => { k = 0; draw(); } });
    const other = FV.ui.button({ label: "↻ " + L.other, onclick: () => {
      player.stop();
      const q = () => Math.round((rng() * 6 - 3) * 4) / 4;
      ex = { x: ex.x.map(() => Math.round(rng() * 6 - 3)), w: ex.w.map(() => Math.round((rng() * 3 - 1.5) * 4) / 4), b: q() / 2 };
      k = 0; makePlot(); draw();
    } });
    const ours = FV.ui.button({ label: L.ours, onclick: () => { player.stop(); ex = { x: base.x.slice(), w: base.w.slice(), b: base.b }; k = 0; makePlot(); draw(); } });
    w.controls.append(player.el, other.el, ours.el);
    const ro = FV.ui.readout(w.readout, [{ key: "z", label: "$z$ =", c: "blue" }, { key: "a", label: "$a=\\sigma(z)$ ≈", c: "orange" }]);
    function draw() {
      const c = compute(), n = ex.x.length;
      p.clear();
      p.hline(0, { c: "guide", dash: false, w: 1 });
      const shown = Math.min(k, n + 1);
      for (let i = 0; i < shown; i++) {
        const v = c.items[i], a = c.cum[i], b = c.cum[i + 1];
        p.rect(i - 0.32, a, i + 0.32, b, { c: Math.abs(v) < 1e-9 ? "faint" : v > 0 ? "blue" : "red", opacity: i === k - 1 ? 0.95 : 0.6, rx: 2 });
        p.text(i, Math.max(a, b), (v >= 0 ? "+" : "") + n4(v), { anchor: "middle", dy: -7 });
        if (i < n + 1) p.line(i + 0.32, b, i + 1 - 0.32, b, { c: "faint", w: 1, dash: "3 3" });
      }
      if (k >= n + 2) {
        p.rect(n + 1 - 0.32, 0, n + 1 + 0.32, c.z, { c: "ink", opacity: 0.85, rx: 2 });
        p.text(n + 1, Math.max(0, c.z), "z = " + n4(c.z), { anchor: "middle", dy: -7, cls: "nr-strong" });
      }
      ro.set("z", k >= n + 2 ? n4(c.z) : "—");
      ro.set("a", k >= n + 3 ? n4(c.a) : "—");
      // the running formula
      const parts = [];
      for (let i = 0; i < shown; i++) parts.push(i < n ? `\\underbrace{${tn(ex.w[i], true)}\\cdot${tn(ex.x[i], true)}}_{${tn(c.prods[i])}}` : tn(ex.b, true));
      let line = parts.length ? parts.join(" + ") : "\\;";
      if (k >= n + 2) line = `z = ${line} = ${tn(c.z)}`;
      if (k >= n + 3) line += `,\\quad a = \\sigma(${tn(c.z)}) = \\frac{1}{1+e^{${tn(-c.z)}}} \\approx ${tn(Number(c.a.toFixed(4)))}`;
      let msg;
      if (k === 0) msg = L.steps0;
      else if (k <= n) msg = `${L.stepProd(k)} $w_${k}x_${k} = ${tn(ex.w[k - 1], true)}\\cdot${tn(ex.x[k - 1], true)} = ${tn(c.prods[k - 1])}$; ${L.stepCum} $= ${tn(c.cum[k])}$.`;
      else if (k === n + 1) msg = `${L.stepBias} $${tn(c.cum[n])} + ${tn(ex.b, true)} = ${tn(c.cum[n + 1])}$.`;
      else if (k === n + 2) msg = `${L.stepZ} $z = ${tn(c.z)}$.`;
      else msg = `${L.stepA} $a = \\sigma(${tn(c.z)}) \\approx ${tn(Number(c.a.toFixed(4)))}$.`;
      w.note.textContent = "";
      const eq = FV.tex(line, true); eq.classList.add("nr-eqline");
      w.note.append(eq, FV.rich(msg, "p"));
    }
    makePlot(); draw();
  });

  // ======================================================================
  // 3. The dot product in the plane: two draggable vectors and the projection
  // ======================================================================
  FV.widget("neuron-dot", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-3.2, 3.2], y: [-1.8, 3.2], equal: true, xLabel: "x₁", yLabel: "x₂" });
    let wv = (cfg.w || [2, 1]).slice(), xv = (cfg.x || [1, 2]).slice();
    const snap = (v) => Math.round(v * 10) / 10;
    const hw = p.handle(wv[0], wv[1], { c: "blue", label: "w", onDrag: (a, b) => { const q = [snap(a), snap(b)]; if (Math.hypot(...q) < 0.3) return [wv[0], wv[1]]; wv = q; return q; }, onChange: () => draw() });
    const hx = p.handle(xv[0], xv[1], { c: "teal", label: "x", onDrag: (a, b) => { xv = [snap(a), snap(b)]; return xv; }, onChange: () => draw() });
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.sumForm, c: "blue" }, { key: "c", label: L.cosForm, c: "orange" }, { key: "t", label: L.angle }]);
    p.onresize = draw;
    function draw() {
      p.clear();
      const dot = wv[0] * xv[0] + wv[1] * xv[1], nw = Math.hypot(...wv), nx = Math.hypot(...xv);
      const u = [wv[0] / nw, wv[1] / nw], pr = dot / nw, foot = [u[0] * pr, u[1] * pr];
      p.line(-u[0] * 10, -u[1] * 10, u[0] * 10, u[1] * 10, { c: "guide", w: 1, dash: "2 4" });
      p.line(0, 0, foot[0], foot[1], { c: "orange", w: 5, opacity: 0.85 });
      p.line(xv[0], xv[1], foot[0], foot[1], { c: "faint", w: 1.2, dash: "4 4" });
      // right-angle mark at the foot
      if (nx > 0.2 && Math.abs(pr) > 0.15 && Math.abs(Math.abs(pr) - nx) > 0.05) {
        const s = 0.16, back = [-u[0] * Math.sign(pr) * s, -u[1] * Math.sign(pr) * s];
        const perp = [xv[0] - foot[0], xv[1] - foot[1]], pl = Math.hypot(...perp) || 1, pv = [(perp[0] / pl) * s, (perp[1] / pl) * s];
        p.path([[foot[0] + back[0], foot[1] + back[1]], [foot[0] + back[0] + pv[0], foot[1] + back[1] + pv[1]], [foot[0] + pv[0], foot[1] + pv[1]]], { c: "faint", w: 1 });
      }
      // angle arc
      if (nx > 0.2) {
        const a1 = Math.atan2(wv[1], wv[0]); let a2 = Math.atan2(xv[1], xv[0]);
        let da = a2 - a1; while (da > Math.PI) da -= 2 * Math.PI; while (da < -Math.PI) da += 2 * Math.PI;
        const r = 0.45, pts = [];
        for (let i = 0; i <= 30; i++) { const t = a1 + (da * i) / 30; pts.push([r * Math.cos(t), r * Math.sin(t)]); }
        p.path(pts, { c: "violet", w: 1.5 });
        const tm = a1 + da / 2; p.text(0.72 * Math.cos(tm), 0.72 * Math.sin(tm), "θ", { anchor: "middle", dy: 4, c: "violet" });
      }
      p.arrow(0, 0, wv[0], wv[1], { c: "blue", w: 2.5 });
      p.arrow(0, 0, xv[0], xv[1], { c: "teal", w: 2.5 });
      p.text(wv[0], wv[1], "w", { dx: 16, dy: -12, c: "blue", cls: "nr-strong" });
      p.text(xv[0], xv[1], "x", { dx: 16, dy: -12, c: "teal", cls: "nr-strong" });
      p.dot(0, 0, { r: 3, c: "ink" });
      const cos = nx > 1e-9 ? dot / (nw * nx) : 0, th = (Math.acos(FV.clamp(cos, -1, 1)) * 180) / Math.PI;
      ro.set("s", `${n4(wv[0])}·${n4(xv[0])} + ${n4(wv[1])}·${n4(xv[1])} = ${n4(dot)}`);
      ro.set("c", `${FV.num(nw, 3)}·${FV.num(nx, 3)}·${FV.num(cos, 3)} = ${n4(nw * nx * cos)}`);
      ro.set("t", FV.fmt(th, 1) + "°");
      w.note.textContent = "";
      w.note.append(FV.rich(Math.abs(dot) < 1e-9 ? L.ortho : dot > 0 ? L.agree : L.against));
      hw.set(wv[0], wv[1]); hx.set(xv[0], xv[1]);
    }
    draw();
  });

  // ======================================================================
  // 4. The decision boundary of a 2-input sigmoid neuron
  // ======================================================================
  FV.widget("neuron-plane", (el, cfg) => {
    const w = FV.shell(el, {});
    const D = 3;
    const p = new FV.Plot(w.stage, { x: [-D, D], y: [-D, D], equal: true, xLabel: "x₁", yLabel: "x₂", maxHeight: 560 });
    let wv = (cfg.w || [1.5, 1]).slice(), b = cfg.b != null ? cfg.b : -1, xv = (cfg.x || [1.5, 0.5]).slice();
    const snap = (v) => Math.round(v * 10) / 10;
    const hw = p.handle(wv[0], wv[1], { c: "blue", label: "w", onDrag: (a, c) => { const q = [snap(a), snap(c)]; if (Math.hypot(...q) < 0.2) return [wv[0], wv[1]]; wv = q; return q; }, onChange: () => draw() });
    const hx = p.handle(xv[0], xv[1], { c: "ink", label: "x", onDrag: (a, c) => { xv = [snap(a), snap(c)]; return xv; }, onChange: () => draw() });
    const bs = FV.ui.slider({ label: L.b, min: -4, max: 4, step: 0.1, value: b, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { b = v; draw(); } });
    w.controls.append(bs.el);
    const ro = FV.ui.readout(w.readout, [{ key: "w", label: "$\\mathbf{w}$ =", c: "blue" }, { key: "n", label: L.wLen }, { key: "o", label: L.origin }, { key: "z", label: L.zAt }, { key: "a", label: L.aAt, c: "orange" }, { key: "d", label: L.dAt }]);
    p.onresize = draw;
    function draw() {
      p.clear();
      p.heat((x1, x2) => sig(wv[0] * x1 + wv[1] * x2 + b), { cmap: "diverging", z: [0, 1], res: 4, alpha: 0.8 });
      const nw2 = wv[0] ** 2 + wv[1] ** 2, nw = Math.sqrt(nw2);
      [[-2, "4 5"], [2, "4 5"], [0, null]].forEach(([lev, dash]) => {
        const s = clipLine(wv[0], wv[1], b - lev, -D, D, -D, D);
        if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], { c: "ink", w: lev ? 1.2 : 2.4, dash, opacity: lev ? 0.65 : 1 });
      });
      // perpendicular from the origin to the boundary: length |b|/‖w‖
      const f0 = [(-b * wv[0]) / nw2, (-b * wv[1]) / nw2];
      p.arrow(0, 0, wv[0], wv[1], { c: "blue", w: 2.6 });
      p.line(0, 0, f0[0], f0[1], { c: "violet", w: 4.5, opacity: 0.9 });
      if (Math.hypot(...f0) > 0.35) p.text(f0[0] / 2, f0[1] / 2, "|b|/‖w‖", { dx: -8, dy: -8, anchor: "end", c: "violet", cls: "nr-strong" });
      p.text(wv[0], wv[1], "w", { dx: 16, dy: -12, c: "blue", cls: "nr-strong" });
      p.dot(0, 0, { r: 3, c: "ink" });
      // the point x and its distance to the boundary
      const z = wv[0] * xv[0] + wv[1] * xv[1] + b;
      const proj = [xv[0] - (z * wv[0]) / nw2, xv[1] - (z * wv[1]) / nw2];
      p.line(xv[0], xv[1], proj[0], proj[1], { c: "ink", w: 1.2, dash: "2 3" });
      p.text(xv[0], xv[1], "x", { dx: 16, dy: 20, cls: "nr-strong" });
      const seg = clipLine(wv[0], wv[1], b, -D, D, -D, D);
      if (seg) {
        const m = seg[0][1] > seg[1][1] ? seg[0] : seg[1];
        p.text(m[0], m[1], "a = " + (FV.lang === "en" ? "0.5" : "0,5"), { dx: m[0] > 0 ? -6 : 6, dy: 16, anchor: m[0] > 0 ? "end" : "start", cls: "nr-strong" });
      }
      ro.set("w", vec(wv)); ro.set("n", n4(nw)); ro.set("o", n4(Math.abs(b) / nw));
      ro.set("z", n4(z)); ro.set("a", n4(sig(z))); ro.set("d", n4(z / nw));
      hw.set(wv[0], wv[1]); hx.set(xv[0], xv[1]);
    }
    draw();
  });

  // ======================================================================
  // 5. The output surface over the input plane (3D)
  // ======================================================================
  FV.widget("neuron-surface", (el, cfg) => {
    const w = FV.shell(el, {});
    let wv = (cfg.w || [1.5, 1]).slice(), b = cfg.b != null ? cfg.b : -1, mode = cfg.mode || "sigmoid";
    const D = 3;
    const fOf = () => { const F = mode === "z" ? (z) => z : ACT[mode].f; return (x1, x2) => F(wv[0] * x1 + wv[1] * x2 + b); };
    const range = () => {
      const zs = [[-D, -D], [D, -D], [D, D], [-D, D]].map(([a, c]) => wv[0] * a + wv[1] * c + b);
      const lo = Math.min(...zs), hi = Math.max(...zs);
      if (mode === "sigmoid") return [0, 1];
      if (mode === "relu") return [0, Math.max(1, hi)];
      return [Math.min(-1, lo), Math.max(1, hi)];
    };
    const zLab = () => (mode === "z" ? "z" : mode === "sigmoid" ? "σ(z)" : "ReLU(z)");
    const sf = new FV.Surface(w.stage, { f: fOf(), x: [-D, D], y: [-D, D], z: range(), n: 34, labels: { x: "x₁", y: "x₂", z: zLab() }, cmap: "viridis", azimuth: -0.9, elevation: 0.72 });
    const seg = FV.ui.seg({ label: L.mode, value: mode, options: [{ value: "z", label: "$z$" }, { value: "sigmoid", label: "$\\sigma(z)$" }, { value: "relu", label: "$\\mathrm{ReLU}(z)$" }], onchange: (v) => { mode = v; update(); } });
    const s1 = FV.ui.slider({ label: L.w1, min: -3, max: 3, step: 0.1, value: wv[0], fmt: (v) => FV.fmt(v, 1), oninput: (v) => { wv[0] = v; update(); } });
    const s2 = FV.ui.slider({ label: L.w2, min: -3, max: 3, step: 0.1, value: wv[1], fmt: (v) => FV.fmt(v, 1), oninput: (v) => { wv[1] = v; update(); } });
    const s3 = FV.ui.slider({ label: L.b, min: -4, max: 4, step: 0.1, value: b, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { b = v; update(); } });
    w.controls.append(seg.el, s1.el, s2.el, s3.el);
    let raf = 0;
    function update() {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0;
        sf.o.labels.z = zLab();
        sf.paths = [];
        sf.setF(fOf(), range());
        const s = clipLine(wv[0], wv[1], b, -D, D, -D, D);
        const h = mode === "sigmoid" ? 0.5 : 0;
        if (s) sf.setPaths([{ pts: FV.linspace(0, 1, 24).map((t) => [s[0][0] + (s[1][0] - s[0][0]) * t, s[0][1] + (s[1][1] - s[0][1]) * t, h]), c: "orange", w: 4 }]);
        else sf.setPaths([]);
      });
    }
    update();
  });

  // ======================================================================
  // 6. One input: the weight sets the slope, the bias moves the threshold
  // ======================================================================
  FV.widget("neuron-bias", (el, cfg) => {
    const w = FV.shell(el, {});
    let wt = cfg.w != null ? cfg.w : 2, b = cfg.b != null ? cfg.b : -2, f = cfg.f || "sigmoid";
    const fs = cfg.fs || ["sigmoid", "step", "relu", "identity"];
    const YR = { sigmoid: [-0.15, 1.15], step: [-0.15, 1.15], tanh: [-1.2, 1.2], relu: [-0.6, 6], identity: [-6, 6] };
    const p = new FV.Plot(w.stage, { x: [-5, 5], y: YR[f], xLabel: "x", yLabel: "a", aspect: 0.5 });
    const seg = FV.ui.seg({ label: L.fOf, value: f, options: fs.map((k) => ({ value: k, label: L[k] })), onchange: (v) => { f = v; p.setDomain(null, YR[f]); draw(); } });
    const sw = FV.ui.slider({ label: L.w, min: -4, max: 4, step: 0.1, value: wt, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { wt = v; draw(); } });
    const sb = FV.ui.slider({ label: L.b, min: -6, max: 6, step: 0.1, value: b, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { b = v; draw(); } });
    w.controls.append(seg.el, sw.el, sb.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x0", label: L.x0, c: "violet" }, { key: "a0", label: L.a0 }, { key: "k", label: L.slope }]);
    p.onresize = draw;
    function draw() {
      const F = ACT[f].f;
      p.clear();
      if (f === "sigmoid" || f === "step") p.hline(0.5, {});
      p.fn((x) => F(wt * x), { c: "faint", w: 1.6, dash: "6 5", jump: f === "step" ? 0.5 : null });
      const x0 = Math.abs(wt) > 1e-9 ? -b / wt : NaN;
      if (Number.isFinite(x0) && x0 > -5 && x0 < 5) {
        p.vline(x0, { c: "violet", dash: "5 4", w: 1.4 });
        p.text(x0, YR[f][1], "x₀", { dx: 6, dy: 16, c: "violet", cls: "nr-strong" });
      }
      p.fn((x) => F(wt * x + b), { c: "blue", w: 2.6, jump: f === "step" ? 0.5 : null });
      if (Number.isFinite(x0) && x0 > -5 && x0 < 5) p.dot(x0, F(0), { c: "violet", r: 5 });
      (cfg.marks || []).forEach((m) => {
        const y = F(wt * m + b);
        p.dot(m, y, { c: "orange", r: 4.5 });
        p.text(m, y, n4(y), { dx: 8, dy: 16, anchor: "start", c: "orange", cls: "nr-strong" });
      });
      p.legend([{ label: L.withBias, c: "blue" }, { label: L.noBias, c: "faint", dash: true }]);
      ro.set("x0", Number.isFinite(x0) ? n4(x0) : "—");
      ro.set("a0", n4(F(b)));
      const k = f === "sigmoid" ? wt / 4 : f === "tanh" ? wt : f === "identity" ? wt : f === "relu" ? NaN : NaN;
      ro.set("k", Number.isFinite(k) && Number.isFinite(x0) ? n4(k) : "—");
    }
    draw();
  });

  // ======================================================================
  // 7. Five activations at the same z
  // ======================================================================
  FV.widget("neuron-activations", (el, cfg) => {
    const w = FV.shell(el, {});
    let z = cfg.z != null ? cfg.z : 2, f = cfg.f || "sigmoid", der = false;
    const p = new FV.Plot(w.stage, { x: [-5, 5], y: [-1.5, 3.2], xLabel: "z", yLabel: "f(z)", aspect: 0.55 });
    const seg = FV.ui.seg({ label: L.fOf, value: f, options: ACT_IDS.map((k) => ({ value: k, label: L[k] })), onchange: (v) => { f = v; draw(); } });
    const sz = FV.ui.slider({ label: L.zLbl, min: -5, max: 5, step: 0.05, value: z, fmt: (v) => FV.fmt(v, 2), oninput: (v) => { z = v; draw(); } });
    const ck = FV.ui.check({ label: L.deriv, checked: false, onchange: (v) => { der = v; draw(); } });
    w.controls.append(seg.el, sz.el, ck.el);
    const ro = FV.ui.readout(w.readout, ACT_IDS.map((k) => ({ key: k, label: L[k] + ":", c: ACT[k].c })).concat([{ key: "d", label: "$f'(z)$:" }]));
    p.onresize = draw;
    function draw() {
      p.clear();
      ACT_IDS.forEach((k) => { if (k !== f) p.fn(ACT[k].f, { c: ACT[k].c, w: 1.2, opacity: 0.35, jump: k === "step" ? 0.5 : null }); });
      p.vline(z, {});
      const A = ACT[f];
      if (der) p.fn(A.d, { c: A.c, w: 1.8, dash: "6 4", jump: 0.5 });
      p.fn(A.f, { c: A.c, w: 3, jump: f === "step" ? 0.5 : null });
      p.dot(z, A.f(z), { c: A.c, r: 6 });
      if (der) p.dot(z, A.d(z), { c: A.c, r: 4, hollow: true });
      p.text(z, Math.min(3.0, A.f(z)), "a = " + n4(A.f(z)), { dx: z > 2.5 ? -10 : 10, dy: -10, anchor: z > 2.5 ? "end" : "start", c: A.c, cls: "nr-strong" });
      ACT_IDS.forEach((k) => ro.set(k, n4(ACT[k].f(z))));
      ro.set("d", n4(A.d(z)));
    }
    draw();
  });

  // ======================================================================
  // 8. Logic gates and the perceptron learning rule
  // ======================================================================
  FV.widget("neuron-logic", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const c1 = FV.col(w.stage), c2 = FV.col(w.stage);
    const PTS = [[0, 0], [0, 1], [1, 0], [1, 1]];
    const T = { and: [0, 0, 0, 1], or: [0, 1, 1, 1], nand: [1, 1, 1, 0], xor: [0, 1, 1, 0] };
    const SOL = { and: [1, 1, -1.5], or: [1, 1, -0.5], nand: [-1, -1, 1.5] };
    const START = [-0.4, 0.6, 0.2], ETA = 0.5, MAXE = 30;
    let gate = cfg.gate || "and", th = START.slice(), it = 0, errs = 0, cur = -1, done = "";
    const p = new FV.Plot(c1, { x: [-0.6, 1.6], y: [-0.6, 1.6], equal: true, xLabel: "x₁", yLabel: "x₂", xTicks: [0, 1], yTicks: [0, 1], maxHeight: 420 });
    const seg = FV.ui.seg({ label: L.gate, value: gate, options: ["and", "or", "nand", "xor"].map((g) => ({ value: g, label: g.toUpperCase() })), onchange: (v) => { gate = v; reset(); } });
    const sl = ["w1", "w2", "b"].map((k, i) => FV.ui.slider({ label: i < 2 ? `$w_${i + 1}$` : "$b$", min: -3, max: 3, step: 0.1, value: th[i], fmt: (v) => FV.fmt(v, 2), oninput: (v) => { player.stop(); th[i] = v; done = ""; draw(); } }));
    const player = FV.ui.player({ interval: 420, onstep: () => stepRule(), onreset: () => reset() });
    const sol = FV.ui.button({ label: L.solution, onclick: () => { player.stop(); if (SOL[gate]) { th = SOL[gate].slice(); done = ""; } else done = L.noSolution; cur = -1; sync(); draw(); } });
    w.controls.append(seg.el, ...sl.map((s) => s.el), FV.h("div", { class: "nr-row" }, FV.h("span", { class: "nr-sl-h", text: L.train }), player.el, sol.el));
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.epoch + ":" }, { key: "r", label: L.errors + ":", c: "red" }]);
    p.onresize = draw;
    const H = (z) => (z >= 0 ? 1 : 0);
    const zOf = (q) => th[0] * q[0] + th[1] * q[1] + th[2];
    function sync() { sl.forEach((s, i) => s.set(th[i])); }
    function reset() { player.stop(); th = START.slice(); it = 0; errs = 0; cur = -1; done = ""; sync(); draw(); }
    function stepRule() {
      if (done) return false;
      const i = it % 4, q = PTS[i], y = T[gate][i], e = y - H(zOf(q));
      if (e) { th[0] += ETA * e * q[0]; th[1] += ETA * e * q[1]; th[2] += ETA * e; errs++; }
      th = th.map((v) => Math.round(v * 1000) / 1000);
      cur = i; it++;
      if (it % 4 === 0) {
        const ep = it / 4;
        if (errs === 0) done = L.converged(ep);
        else if (ep >= MAXE) done = L.noLine(ep);
        if (!done) errs = 0;
      }
      sync(); draw();
      return !done;
    }
    function draw() {
      p.clear();
      const poly = halfPlane(th[0], th[1], th[2], -0.6, 1.6, -0.6, 1.6);
      if (poly.length > 2) p.path(poly, { fill: true, close: true, c: "teal", fillOpacity: 0.14 });
      const s = clipLine(th[0], th[1], th[2], -0.6, 1.6, -0.6, 1.6);
      if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], { c: "ink", w: 2.2 });
      let wrong = 0;
      const rows = [];
      PTS.forEach((q, i) => {
        const z = zOf(q), yh = H(z), y = T[gate][i], ok = yh === y;
        if (!ok) wrong++;
        if (i === cur) p.dot(q[0], q[1], { r: 17, c: "orange", hollow: true });
        if (!ok) p.dot(q[0], q[1], { r: 13, c: "red", hollow: true });
        p.dot(q[0], q[1], { r: 8, c: y ? "teal" : "ink", hollow: !y });
        p.text(q[0], q[1], y ? "1" : "0", { dx: 14, dy: -12, cls: "nr-strong" });
        rows.push(`<tr${i === cur ? ' class="cur"' : ""}><td class=num>${q[0]}</td><td class=num>${q[1]}</td><td class=num>${n4(z)}</td><td class=num>${yh}</td><td class=num>${y}</td><td class="${ok ? "ok" : "bad"}">${ok ? "✓" : "✗"}</td></tr>`);
      });
      ro.set("e", it ? String(Math.ceil(it / 4)) : "—");
      ro.set("r", String(wrong));
      c2.innerHTML = `<div class="table-wrap"><table class="data nr-tt"><thead><tr><th class=num>x₁</th><th class=num>x₂</th><th class=num>z</th><th class=num>ŷ</th><th class=num>y</th><th></th></tr></thead><tbody>${rows.join("")}</tbody></table></div>`;
      if (done) c2.append(FV.h("p", { class: "nr-done", text: done }));
    }
    draw();
  });

  // ======================================================================
  // 9. A 3×3 patch: nine inputs, a weight template, ReLU
  // ======================================================================
  FV.widget("neuron-pixels", (el, cfg) => {
    const w = FV.shell(el, {});
    const K = {
      vertical: { w: [-1, 0, 1, -1, 0, 1, -1, 0, 1], b: -1 },
      horizontal: { w: [-1, -1, -1, 0, 0, 0, 1, 1, 1], b: -1 },
      spot: { w: [-1, -1, -1, -1, 8, -1, -1, -1, -1], b: -1 },
    };
    const P = {
      edge: [0, 1, 1, 0, 1, 1, 0, 1, 1], uniform: [1, 1, 1, 1, 1, 1, 1, 1, 1], h: [0, 0, 0, 1, 1, 1, 1, 1, 1], dot: [0, 0, 0, 0, 1, 0, 0, 0, 0], clear: [0, 0, 0, 0, 0, 0, 0, 0, 0],
    };
    let kern = cfg.kernel || "vertical", x = P.edge.slice();
    const mk = (cls) => FV.h("div", { class: "nr-grid " + cls });
    const gIn = mk("in"), gW = mk("w"), gP = mk("p");
    const cellsIn = x.map((_, i) => { const b = FV.h("button", { type: "button", class: "nr-cell", onclick: () => { x[i] = x[i] === 0 ? 0.5 : x[i] === 0.5 ? 1 : 0; draw(); } }); gIn.append(b); return b; });
    const cellsW = x.map(() => { const c = FV.h("span", { class: "nr-cell" }); gW.append(c); return c; });
    const cellsP = x.map(() => { const c = FV.h("span", { class: "nr-cell" }); gP.append(c); return c; });
    const col = (lab, g) => FV.h("div", { class: "nr-gcol" }, FV.rich(lab, "span"), g);
    const out = FV.h("div", { class: "nr-px-out" });
    w.stage.append(FV.h("div", { class: "nr-px" }, col(L.colIn, gIn), FV.h("span", { class: "nr-op", text: "×" }), col(L.colW, gW), FV.h("span", { class: "nr-op", text: "=" }), col(L.colP, gP)), out);
    const sk = FV.ui.seg({ label: L.kernel, value: kern, options: ["vertical", "horizontal", "spot"].map((k) => ({ value: k, label: L[k] })), onchange: (v) => { kern = v; draw(); } });
    const sp = FV.h("div", { class: "fv-seg" }, FV.h("span", { text: L.preset }), FV.h("div", { class: "fv-seg-btns" },
      [["edge", L.pEdge], ["uniform", L.pUniform], ["h", L.pH], ["dot", L.pDot], ["clear", L.pClear]].map(([k, lab]) => FV.h("button", { type: "button", "aria-pressed": "false", onclick: () => { x = P[k].slice(); draw(); } }, lab))));
    w.controls.append(sk.el, sp);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: "$\\sum w_ix_i$ =" }, { key: "b", label: "$b$ =" }, { key: "z", label: "$z$ =", c: "blue" }, { key: "a", label: "$a=\\mathrm{ReLU}(z)$ =", c: "orange" }]);
    const shade = (t) => FV.rgb(FV.cmap("diverging", t));
    function draw() {
      const k = K[kern], m = Math.max(...k.w.map(Math.abs));
      let s = 0;
      x.forEach((v, i) => {
        const g = Math.round(255 * v);
        cellsIn[i].style.background = `rgb(${g},${g},${g})`;
        cellsIn[i].style.color = v > 0.5 ? "#171A20" : "#EDEDED";
        cellsIn[i].textContent = FV.num(v, 2);
        cellsIn[i].setAttribute("aria-label", `x${SUB[i + 1]} = ${FV.num(v, 2)}`);
        cellsW[i].style.background = shade(0.5 - k.w[i] / (2 * m));
        cellsW[i].textContent = n4(k.w[i]);
        const pr = k.w[i] * v; s += pr;
        cellsP[i].style.background = shade(0.5 - pr / (2 * m));
        cellsP[i].textContent = pr === 0 ? "0" : n4(pr);
      });
      const z = s + k.b, a = Math.max(0, z);
      ro.set("s", n4(s)); ro.set("b", n4(k.b)); ro.set("z", n4(z)); ro.set("a", n4(a));
      out.textContent = "";
      const bar = FV.h("span", { class: "nr-meter" }, FV.h("i", { style: `width:${Math.min(100, (a / (kern === "spot" ? 8 : 3)) * 100)}%` }));
      out.append(FV.tex(`z = ${tn(s)} + ${tn(k.b, true)} = ${tn(z)},\\quad a = \\max(0,\\ ${tn(z)}) = ${tn(a)}`), bar, FV.h("b", { class: a > 0 ? "on" : "", text: a > 0 ? L.fired : L.silent }));
    }
    draw();
  });

  // ======================================================================
  // 10. Training a neuron by gradient descent on two classes
  // ======================================================================
  FV.widget("neuron-train", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const c1 = FV.col(w.stage), c2 = FV.col(w.stage);
    const rng = FV.rng(cfg.seed || 7);
    const data = [];
    for (let i = 0; i < 40; i++) data.push({ x: [-1.1 + 0.95 * rng.normal(), -0.8 + 0.95 * rng.normal()], y: 0 });
    for (let i = 0; i < 40; i++) data.push({ x: [1.1 + 0.95 * rng.normal(), 0.9 + 0.95 * rng.normal()], y: 1 });
    const INIT = [-1, 0.6, 1.5], MAX = 200;
    let th = INIT.slice(), eta = cfg.eta || 0.5, hist = [], ep = 0;
    const D = 4;
    const p = new FV.Plot(c1, { x: [-D, D], y: [-D, D], equal: true, xLabel: "x₁", yLabel: "x₂", maxHeight: 460 });
    const lossOf = () => {
      let L0 = 0, acc = 0;
      data.forEach((d) => {
        const z = th[0] * d.x[0] + th[1] * d.x[1] + th[2];
        L0 += Math.max(z, 0) - z * d.y + Math.log1p(Math.exp(-Math.abs(z)));   // stable BCE with logits
        if ((z >= 0 ? 1 : 0) === d.y) acc++;
      });
      return [L0 / data.length, acc / data.length];
    };
    hist.push(lossOf()[0]);
    const lp = new FV.Plot(c2, { x: [0, MAX], y: [0, Math.ceil(hist[0] * 1.15 * 10) / 10], xLabel: L.epochN, yLabel: L.loss, aspect: 0.62, title: L.lossTitle });
    const se = FV.ui.slider({ label: L.eta, min: 0.05, max: 3, step: 0.05, value: eta, fmt: (v) => FV.fmt(v, 2), oninput: (v) => { eta = v; } });
    const player = FV.ui.player({ interval: 60, onstep: () => step(), onreset: () => { th = INIT.slice(); ep = 0; hist = [lossOf()[0]]; draw(); } });
    w.controls.append(player.el, se.el);
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.epochN + ":" }, { key: "w", label: "$\\mathbf{w}$ =", c: "blue" }, { key: "b", label: "$b$ =" }, { key: "l", label: L.loss + ":", c: "orange" }, { key: "a", label: L.acc + ":" }]);
    p.onresize = draw; lp.onresize = draw;
    function step() {
      if (ep >= MAX) return false;
      let g0 = 0, g1 = 0, gb = 0;
      data.forEach((d) => {
        const a = sig(th[0] * d.x[0] + th[1] * d.x[1] + th[2]), dl = a - d.y;   // δ = a − y
        g0 += dl * d.x[0]; g1 += dl * d.x[1]; gb += dl;
      });
      const m = data.length;
      th = [th[0] - (eta * g0) / m, th[1] - (eta * g1) / m, th[2] - (eta * gb) / m];
      ep++; hist.push(lossOf()[0]);
      draw();
      return ep < MAX;
    }
    function draw() {
      p.clear();
      p.heat((a, c) => sig(th[0] * a + th[1] * c + th[2]), { cmap: "diverging", z: [0, 1], res: 5, alpha: 0.5 });
      [[-2, "4 5"], [2, "4 5"], [0, null]].forEach(([lev, dash]) => {
        const s = clipLine(th[0], th[1], th[2] - lev, -D, D, -D, D);
        if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], { c: "ink", w: lev ? 1 : 2.4, dash, opacity: lev ? 0.6 : 1 });
      });
      data.forEach((d) => p.dot(d.x[0], d.x[1], { r: 5, c: d.y ? "red" : "blue" }));
      p.legend([{ label: L.class0, c: "blue", dot: true }, { label: L.class1, c: "red", dot: true }]);
      lp.clear();
      lp.path(hist.map((v, i) => [i, v]), { c: "orange", w: 2.2 });
      lp.dot(ep, hist[hist.length - 1], { c: "orange", r: 4 });
      const [loss, acc] = lossOf();
      ro.set("e", String(ep)); ro.set("w", vec(th.slice(0, 2).map((v) => Math.round(v * 100) / 100)));
      ro.set("b", FV.fmt(th[2], 2)); ro.set("l", FV.fmt(loss, 3)); ro.set("a", Math.round(acc * 100) + "%");
    }
    draw();
  });
  // ======================================================================
  // 11. Labelled points on a plane with its own axes (examples section)
  // ======================================================================
  FV.widget("neuron-points", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const c1 = FV.col(w.stage), c2 = FV.col(w.stage);
    const R = cfg.range || [0, 10];
    let wv = (cfg.w || [1, 0.5]).slice(), b = cfg.b != null ? cfg.b : -9;
    const pts = cfg.pts || [];
    const ax = cfg.axes === "exam" ? [L.exam1, L.exam2] : ["x₁", "x₂"];
    const p = new FV.Plot(c1, { x: R, y: R, equal: true, xLabel: ax[0], yLabel: ax[1], maxHeight: 460 });
    const br = cfg.bRange || [-15, 5];
    const s1 = FV.ui.slider({ label: L.w1, min: -2, max: 2, step: 0.05, value: wv[0], fmt: (v) => FV.fmt(v, 2), oninput: (v) => { wv[0] = v; draw(); } });
    const s2 = FV.ui.slider({ label: L.w2, min: -2, max: 2, step: 0.05, value: wv[1], fmt: (v) => FV.fmt(v, 2), oninput: (v) => { wv[1] = v; draw(); } });
    const s3 = FV.ui.slider({ label: L.b, min: br[0], max: br[1], step: 0.1, value: b, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { b = v; draw(); } });
    const rs = FV.ui.button({ label: "↺ " + FV.t("restart"), onclick: () => { wv = cfg.w.slice(); b = cfg.b; s1.set(wv[0]); s2.set(wv[1]); s3.set(b); draw(); } });
    w.controls.append(s1.el, s2.el, s3.el, rs.el);
    p.onresize = draw;
    function draw() {
      p.clear();
      const nw2 = wv[0] ** 2 + wv[1] ** 2, nw = Math.sqrt(nw2) || 1;
      p.heat((x1, x2) => sig(wv[0] * x1 + wv[1] * x2 + b), { cmap: "diverging", z: [0, 1], res: 4, alpha: 0.6 });
      [[-2, "4 5"], [2, "4 5"], [0, null]].forEach(([lev, dash]) => {
        const s = clipLine(wv[0], wv[1], b - lev, R[0], R[1], R[0], R[1]);
        if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], { c: "ink", w: lev ? 1.1 : 2.4, dash, opacity: lev ? 0.6 : 1 });
      });
      // the normal w, drawn from the boundary point nearest to the centre
      const cx = (R[0] + R[1]) / 2, zc = wv[0] * cx + wv[1] * cx + b;
      const f = [cx - (zc * wv[0]) / nw2, cx - (zc * wv[1]) / nw2], k = (0.14 * (R[1] - R[0])) / nw;
      if (nw2 > 1e-9 && f[0] > R[0] && f[0] < R[1] && f[1] > R[0] && f[1] < R[1]) {
        p.arrow(f[0], f[1], f[0] + wv[0] * k, f[1] + wv[1] * k, { c: "blue", w: 2.4 });
        p.text(f[0] + wv[0] * k, f[1] + wv[1] * k, "w", { dx: 8, dy: -6, c: "blue", cls: "nr-strong" });
      }
      const rows = pts.map((q) => {
        const z = wv[0] * q.x[0] + wv[1] * q.x[1] + b, a = sig(z);
        p.dot(q.x[0], q.x[1], { r: 6, c: a >= 0.5 ? "red" : "blue" });
        p.text(q.x[0], q.x[1], q.l, { dx: 10, dy: -10, cls: "nr-strong" });
        return `<tr><td>${q.l}</td><td class=num>${vec(q.x)}</td><td class=num>${n4(z)}</td><td class=num>${n4(a)}</td><td class=num>${n4(z / nw)}</td></tr>`;
      });
      c2.innerHTML = `<div class="table-wrap"><table class="data nr-tt"><thead><tr><th></th><th class=num>x</th><th class=num>z</th><th class=num>a</th><th class=num>d</th></tr></thead><tbody>${rows.join("")}</tbody></table></div>`;
      const cf = (v) => (Math.abs(Math.abs(v) - 1) < 1e-9 ? "" : tn(Math.abs(v)));
      c2.append(FV.rich(`$z = ${wv[0] < 0 ? "-" : ""}${cf(wv[0])}x_1 ${wv[1] < 0 ? "-" : "+"} ${cf(wv[1])}x_2 ${b < 0 ? "-" : "+"} ${tn(Math.abs(b))}$`, "p"));
    }
    draw();
  });

  // ======================================================================
  // 12. A sum of ReLU neurons builds a broken line (universal approximation)
  // ======================================================================
  FV.widget("neuron-relu-sum", (el, cfg) => {
    const w = FV.shell(el, {});
    const G = { sq: { f: (x) => x * x, y: [-0.6, 4.4], tex: "x^2" }, sin: { f: (x) => Math.sin((Math.PI * x) / 2), y: [-1.4, 1.4], tex: "\\sin\\frac{\\pi x}{2}" } };
    let tg = cfg.target || "sq", K = cfg.k || 4, parts = true;
    const X0 = -2, X1 = 2;
    const p = new FV.Plot(w.stage, { x: [X0, X1], y: G[tg].y, xLabel: "x", yLabel: "y", aspect: 0.55 });
    const seg = FV.ui.seg({ label: L.target, value: tg, options: [{ value: "sq", label: "$x^2$" }, { value: "sin", label: "$\\sin\\frac{\\pi x}{2}$" }], onchange: (v) => { tg = v; p.setDomain(null, G[tg].y); draw(); } });
    const sk = FV.ui.slider({ label: L.neurons, min: 1, max: 16, step: 1, value: K, fmt: (v) => String(v), oninput: (v) => { K = v; draw(); } });
    const ck = FV.ui.check({ label: L.parts, checked: true, onchange: (v) => { parts = v; draw(); } });
    w.controls.append(seg.el, sk.el, ck.el);
    const ro = FV.ui.readout(w.readout, [{ key: "n", label: L.neurons + ":" }, { key: "p", label: L.params }, { key: "e", label: L.maxErr, c: "red" }]);
    p.onresize = draw;
    function build() {
      const g = G[tg].f, xs = FV.linspace(X0, X1, K + 1), sl = [];
      for (let k = 0; k < K; k++) sl.push((g(xs[k + 1]) - g(xs[k])) / (xs[k + 1] - xs[k]));
      // y(x) = g(x₀) + Σ cₖ·ReLU(x − xₖ),  cₖ = sₖ − sₖ₋₁ (s₋₁ = 0): each term is one neuron with w = 1, b = −xₖ
      const c = sl.map((s, k) => s - (k ? sl[k - 1] : 0));
      const y = (x) => g(xs[0]) + c.reduce((acc, ck, k) => acc + ck * Math.max(0, x - xs[k]), 0);
      return { xs, c, y, g };
    }
    function draw() {
      const m = build();
      p.clear();
      p.fn(m.g, { c: "faint", w: 5, opacity: 0.35 });
      if (parts) m.c.forEach((ck, k) => p.fn((x) => ck * Math.max(0, x - m.xs[k]), { c: ck >= 0 ? "blue" : "red", w: 1.2, opacity: 0.55 }));
      p.fn(m.y, { c: "orange", w: 2.6 });
      m.xs.slice(0, -1).forEach((x) => p.dot(x, m.y(x), { r: 3.5, c: "orange" }));
      p.legend([{ label: "$y=" + G[tg].tex + "$", c: "faint" }, { label: L.sumRelu, c: "orange" }].concat(parts ? [{ label: L.oneRelu, c: "blue" }] : []));
      let e = 0;
      FV.linspace(X0, X1, 801).forEach((x) => { e = Math.max(e, Math.abs(m.y(x) - m.g(x))); });
      ro.set("n", String(K)); ro.set("p", String(3 * K + 1)); ro.set("e", FV.num(e, 3));
    }
    draw();
  });

  // ======================================================================
  // 13. XOR: the hidden layer moves the points into a separable position
  // ======================================================================
  FV.widget("neuron-xor-morph", (el, cfg) => {
    const w = FV.shell(el, {});
    const P = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]];
    const H = (z) => (z >= 0 ? 1 : 0);
    const hid = (q) => [H(q[0] + q[1] - 0.5), H(-q[0] - q[1] + 1.5)];
    let t = 0, dir = 1, timer = 0;
    const p = new FV.Plot(w.stage, { x: [-0.45, 1.45], y: [-0.45, 1.45], equal: true, xLabel: "x₁ → h₁", yLabel: "x₂ → h₂", xTicks: [0, 1], yTicks: [0, 1], maxHeight: 420 });
    const st = FV.ui.slider({ label: L.morph, min: 0, max: 1, step: 0.01, value: 0, fmt: (v) => FV.fmt(v, 2), oninput: (v) => { stop(); t = v; draw(); }, wide: true });
    const play = FV.ui.button({ label: "▶ " + FV.t("play"), primary: true, onclick: () => (timer ? stop() : start()) });
    w.controls.append(st.el, play.el);
    function start() { play.setLabel("❚❚ " + FV.t("pause")); timer = setInterval(() => { t += dir * 0.02; if (t >= 1 || t <= 0) { t = FV.clamp(t, 0, 1); dir = -dir; } st.set(t); draw(); }, 40); }
    function stop() { clearInterval(timer); timer = 0; play.setLabel("▶ " + FV.t("play")); }
    p.onresize = draw;
    function draw() {
      p.clear();
      const ln = (a, b, c, o) => { const s = clipLine(a, b, c, -0.45, 1.45, -0.45, 1.45); if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], o); };
      if (t < 1) { ln(1, 1, -0.5, { c: "teal", w: 2, opacity: 1 - t }); ln(-1, -1, 1.5, { c: "violet", w: 2, opacity: 1 - t }); }
      if (t > 0) ln(1, 1, -1.5, { c: "ink", w: 2.4, opacity: t });
      const seen = {};
      P.forEach((q) => {
        const h = hid(q), x = q[0] + (h[0] - q[0]) * t, y = q[1] + (h[1] - q[1]) * t;
        p.dot(x, y, { r: 8, c: q[2] ? "teal" : "ink", hollow: !q[2] });
        const key = Math.round(x * 20) + ":" + Math.round(y * 20), k = (seen[key] = (seen[key] || 0) + 1);
        p.text(x, y, `(${q[0]}${SEP.trim()} ${q[1]})`, { dx: 12, dy: k > 1 ? 14 : -10 });
      });
      p.legend(t < 0.5 ? [{ label: "OR: $x_1+x_2-0{,}5=0$".replace("0{,}5", FV.lang === "en" ? "0.5" : "0{,}5"), c: "teal" }, { label: "NAND: $-x_1-x_2+1{,}5=0$".replace("1{,}5", FV.lang === "en" ? "1.5" : "1{,}5"), c: "violet" }]
        : [{ label: "AND: $h_1+h_2-1{,}5=0$".replace("1{,}5", FV.lang === "en" ? "1.5" : "1{,}5"), c: "ink" }]);
      w.note.textContent = "";
      w.note.append(FV.rich(t < 0.02 ? L.morph0 : t > 0.98 ? L.morph1 : L.morphMid));
    }
    draw();
  });
})();
