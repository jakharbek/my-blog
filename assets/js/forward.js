/* Widgets of the article "The forward pass formula". Built on FV (assets/js/viz.js).
   a⁽⁰⁾ = x;  z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾;  a⁽ˡ⁾ = f⁽ˡ⁾(z⁽ˡ⁾);  ŷ = a⁽ᴸ⁾ */
(function () {
  "use strict";
  if (typeof FV === "undefined" || !FV.widget) return;

  const L = {
    ru: {
      input: "вход", layer: "слой", out: "выход", x: "Вход", play: "Пуск", stage0: "Вход $\\mathbf{a}^{(0)} = \\mathbf{x}$ подан на сеть. Нажмите «Шаг».",
      layerSel: "Слой", neuron: "нейрон", allLayers: "Все слои подряд", rowHint: "Строка $j$ матрицы — веса нейрона $j$",
      sizes: "Размеры слоёв", sizesPh: "например, 784-128-64-10", presets: "Готовые", bad: "Введите от 2 до 12 целых чисел от 1 до 100 000 через дефис.",
      thL: "Слой", thIO: "$n_{l-1} \\to n_l$", thW: "$W^{(l)}$", thB: "$\\mathbf{b}^{(l)}$", thP: "параметров", thM: "умножений", total: "всего", share: "доля параметров",
      stage: "Этап", sInput: "вход", sLin: "$W\\mathbf{x} + \\mathbf{b}$", sAct: "активация", preset: "Пример", pFold: "сгиб ReLU", pRot: "поворот + tanh", pShear: "сдвиг + сигмоида",
      class0: "класс 0", class1: "класс 1", sepLine: "разделяющая прямая", act1: "Активация слоя 1", act2: "Активация слоя 2", scale: "Масштаб весов",
      identity: "тождественная", sigmoid: "сигмоида", tanh: "tanh", relu: "ReLU", mapTitle: "Ответ $\\hat y$ на всей плоскости входов",
      spaceNote0: "Исходная плоскость входов: точки двух классов нельзя разделить одной прямой.", spaceNote1: "Линейная часть повернула, растянула и сдвинула плоскость: сетка осталась сеткой из параллелограммов.", spaceNote2: "Активация изогнула плоскость; теперь классы разделяет прямая.", spaceNote2b: "Активация изогнула плоскость: далёкие точки прижаты к краям.",
    },
    en: {
      input: "input", layer: "layer", out: "output", x: "Input", play: "Play", stage0: "The input $\\mathbf{a}^{(0)} = \\mathbf{x}$ is fed to the network. Press “Step”.",
      layerSel: "Layer", neuron: "neuron", allLayers: "All layers in a row", rowHint: "Row $j$ of the matrix holds the weights of neuron $j$",
      sizes: "Layer sizes", sizesPh: "e.g. 784-128-64-10", presets: "Presets", bad: "Enter 2 to 12 whole numbers from 1 to 100,000 separated by dashes.",
      thL: "Layer", thIO: "$n_{l-1} \\to n_l$", thW: "$W^{(l)}$", thB: "$\\mathbf{b}^{(l)}$", thP: "parameters", thM: "multiplications", total: "total", share: "share of parameters",
      stage: "Stage", sInput: "input", sLin: "$W\\mathbf{x} + \\mathbf{b}$", sAct: "activation", preset: "Example", pFold: "ReLU fold", pRot: "rotation + tanh", pShear: "shear + sigmoid",
      class0: "class 0", class1: "class 1", sepLine: "separating line", act1: "Activation of layer 1", act2: "Activation of layer 2", scale: "Weight scale",
      identity: "identity", sigmoid: "sigmoid", tanh: "tanh", relu: "ReLU", mapTitle: "The answer $\\hat y$ over the whole input plane",
      spaceNote0: "The original input plane: the two classes cannot be separated by one line.", spaceNote1: "The linear part rotated, stretched and shifted the plane: the grid is still a grid of parallelograms.", spaceNote2: "The activation bent the plane; now a line separates the classes.", spaceNote2b: "The activation bent the plane: distant points are pressed to the edges.",
    },
    uz: {
      input: "kirish", layer: "qatlam", out: "chiqish", x: "Kirish", play: "Boshlash", stage0: "$\\mathbf{a}^{(0)} = \\mathbf{x}$ kirish tarmoqqa berildi. «Qadam»ni bosing.",
      layerSel: "Qatlam", neuron: "neyron", allLayers: "Barcha qatlamlar ketma-ket", rowHint: "Matritsaning $j$-satri — $j$-neyronning vaznlari",
      sizes: "Qatlam o‘lchamlari", sizesPh: "masalan, 784-128-64-10", presets: "Tayyor", bad: "Chiziqcha bilan ajratilgan 1 dan 100 000 gacha bo‘lgan 2–12 ta butun son kiriting.",
      thL: "Qatlam", thIO: "$n_{l-1} \\to n_l$", thW: "$W^{(l)}$", thB: "$\\mathbf{b}^{(l)}$", thP: "parametrlar", thM: "ko‘paytirishlar", total: "jami", share: "parametrlar ulushi",
      stage: "Bosqich", sInput: "kirish", sLin: "$W\\mathbf{x} + \\mathbf{b}$", sAct: "aktivatsiya", preset: "Misol", pFold: "ReLU bukilishi", pRot: "burish + tanh", pShear: "siljitish + sigmoida",
      class0: "0-sinf", class1: "1-sinf", sepLine: "ajratuvchi chiziq", act1: "1-qatlam aktivatsiyasi", act2: "2-qatlam aktivatsiyasi", scale: "Vaznlar masshtabi",
      identity: "ayniy", sigmoid: "sigmoida", tanh: "tanh", relu: "ReLU", mapTitle: "Butun kirish tekisligidagi $\\hat y$ javob",
      spaceNote0: "Dastlabki kirish tekisligi: ikki sinf nuqtalarini bitta to‘g‘ri chiziq bilan ajratib bo‘lmaydi.", spaceNote1: "Chiziqli qism tekislikni burdi, cho‘zdi va surdi: to‘r parallelogrammlar to‘ri bo‘lib qoldi.", spaceNote2: "Aktivatsiya tekislikni egdi; endi sinflarni to‘g‘ri chiziq ajratadi.", spaceNote2b: "Aktivatsiya tekislikni egdi: uzoq nuqtalar chetlarga siqildi.",
    },
  }[FV.lang] || {};

  const sig = FV.sigmoid;
  const ACT = { relu: (z) => Math.max(0, z), sigmoid: sig, tanh: Math.tanh, identity: (z) => z };
  const ACT_TEX = { relu: "\\mathrm{ReLU}", sigmoid: "\\sigma", tanh: "\\tanh", identity: "\\mathrm{id}" };
  const SEP = FV.lang === "en" ? ", " : "; ";
  const TSEP = FV.lang === "en" ? ",\\ " : ";\\ ";
  const SUP = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"];
  const SUB = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"];
  const n4 = (v) => FV.num(Math.abs(v) < 1e-12 ? 0 : v, 4);
  const tn = (v, paren) => { const s = n4(v).replace("−", "-").replace(",", "{,}"); return paren && v < 0 ? `(${s})` : s; };
  const tvec = (a) => "(" + a.map((v) => tn(v)).join(TSEP) + ")";
  const reduced = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // forward pass of a dense network; acts may override the layer activations, k scales every weight and bias
  function forward(net, x, acts, k) {
    k = k == null ? 1 : k;
    let a = x.slice();
    const zs = [], as = [a];
    net.W.forEach((W, l) => {
      const f = ACT[(acts && acts[l]) || net.f[l]];
      const z = W.map((row, j) => row.reduce((s, w, i) => s + k * w * a[i], 0) + k * net.b[l][j]);
      a = z.map(f); zs.push(z); as.push(a);
    });
    return { zs, as };
  }

  // ---------- an SVG drawing of a small dense network ----------
  function NetView(parent, net, o) {
    o = o || {};
    const box = FV.h("div", { class: "fp-net" });
    parent.append(box);
    const svg = FV.svg("svg", { class: "fv-svg fp-svg", role: "img" });
    box.append(svg);
    const gE = FV.svg("g", {}, svg), gN = FV.svg("g", {}, svg);
    const sizes = [net.W[0][0].length].concat(net.W.map((W) => W.length));
    let G = null;
    function layout() {
      const W = Math.max(280, Math.round(box.clientWidth || 600)), nar = W < 520;
      const H = o.height ? o.height(W) : nar ? 300 : 340;
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`); svg.setAttribute("width", W); svg.setAttribute("height", H);
      const padX = nar ? 30 : 56, top = 46, bot = H - 30, R = nar ? 17 : 23;
      const pos = sizes.map((n, l) => Array.from({ length: n }, (_, j) => [padX + ((W - 2 * padX) * l) / (sizes.length - 1), n === 1 ? (top + bot) / 2 : top + ((bot - top) * (j + 0.5)) / n]));
      G = { W, H, nar, R, pos };
    }
    // stage: how many layers already computed (0 = only the input); active: the layer being computed now
    function draw(val, stage, active, k) {
      if (!G) layout();
      k = k == null ? 1 : k;
      const { R, pos, nar, H } = G;
      gE.textContent = ""; gN.textContent = "";
      net.W.forEach((Wl, l) => Wl.forEach((row, j) => row.forEach((w, i) => {
        const A = pos[l][i], B = pos[l + 1][j], d = Math.hypot(B[0] - A[0], B[1] - A[1]);
        const ux = (B[0] - A[0]) / d, uy = (B[1] - A[1]) / d;
        const on = l + 1 === active, done = l + 1 <= stage;
        FV.svg("line", { x1: A[0] + ux * R, y1: A[1] + uy * R, x2: B[0] - ux * R, y2: B[1] - uy * R, class: "fp-edge s-" + (w >= 0 ? "blue" : "red") + (on ? " fp-flow" : ""),
          "stroke-width": (0.8 + 2.4 * Math.min(1, Math.abs(k * w) / 2)) * (on ? 1.3 : 1), opacity: on ? 1 : done ? 0.75 : 0.25 }, gE);
      })));
      sizes.forEach((n, l) => {
        const x0 = pos[l][0][0];
        const t = FV.svg("text", { x: x0, y: 18, "text-anchor": "middle", class: "fp-cap" }, gN);
        t.textContent = l === 0 ? L.input : l === sizes.length - 1 ? L.out : L.layer + " " + l;
        if (l > 0) { const t2 = FV.svg("text", { x: x0, y: 32, "text-anchor": "middle", class: "fp-cap2" }, gN); t2.textContent = "f = " + ({ relu: "ReLU", sigmoid: "σ", tanh: "tanh", identity: "id" }[(o.acts && o.acts()[l - 1]) || net.f[l - 1]]); }
        pos[l].forEach((p, j) => {
          const known = l <= stage, v = known ? val.as[l][j] : null;
          const tone = v == null ? null : v >= 0 ? "blue" : "red";
          const c = FV.svg("circle", { cx: p[0], cy: p[1], r: R, class: "fp-node" + (l === active ? " fp-node-on" : "") + (tone ? " fp-" + tone : "") }, gN);
          if (v != null) c.style.setProperty("--fp-a", Math.min(0.85, Math.abs(l === sizes.length - 1 && net.f[l - 1] === "sigmoid" ? v : v / 3) * 0.85 + 0.08));
          const tv = FV.svg("text", { x: p[0], y: p[1] + 4.5, "text-anchor": "middle", class: "fp-val" }, gN);
          tv.textContent = v == null ? "?" : FV.num(v, nar ? 2 : 3);
          if (l > 0 && known && !nar) {
            const tz = FV.svg("text", { x: p[0], y: p[1] + R + 14, "text-anchor": "middle", class: "fp-z" }, gN);
            tz.textContent = "z = " + FV.num(val.zs[l - 1][j], 3);
          }
          if (l === 0) { const tl = FV.svg("text", { x: p[0] - R - 6, y: p[1] + 4, "text-anchor": "end", class: "fp-z" }, gN); tl.textContent = "x" + SUB[j + 1]; }
        });
      });
      svg.setAttribute("aria-label", (o.aria || "") + " ŷ = " + n4(val.as[val.as.length - 1][0]));
      return H;
    }
    return { box, svg, layout, draw, get G() { return G; } };
  }

  // ======================================================================
  // 1. The forward pass, layer by layer
  // ======================================================================
  FV.widget("fp-flow", (el, cfg) => {
    const net = cfg.net, Ln = net.W.length;
    const w = FV.shell(el, {});
    let x = net.x.slice(), stage = Ln, active = 0;
    const view = NetView(w.stage, net, {});
    const player = FV.ui.player({ interval: 1300, onstep: () => { if (stage >= Ln) stage = -1; stage++; active = stage; draw(); return stage < Ln; }, onreset: () => { stage = 0; active = 0; draw(); } });
    const sx = x.map((v, i) => FV.ui.slider({ label: `$x_${i + 1}$`, min: -3, max: 3, step: 0.25, value: v, fmt: (u) => FV.fmt(u, 2), oninput: (u) => { x[i] = u; draw(); } }));
    w.controls.append(player.el, ...sx.map((s) => s.el));
    const ro = FV.ui.readout(w.readout, [{ key: "y", label: "$\\hat y$ =", c: "orange" }]);
    function draw() {
      const val = forward(net, x);
      view.draw(val, stage, active);
      ro.set("y", stage >= Ln ? n4(val.as[Ln][0]) : "—");
      w.note.textContent = "";
      if (stage === 0) { w.note.append(FV.rich(L.stage0, "p")); return; }
      const l = stage, f = net.f[l - 1];
      w.note.append(FV.tex(`\\mathbf{z}^{(${l})} = W^{(${l})}\\mathbf{a}^{(${l - 1})} + \\mathbf{b}^{(${l})} = ${tvec(val.zs[l - 1])},\\qquad \\mathbf{a}^{(${l})} = ${ACT_TEX[f]}\\big(\\mathbf{z}^{(${l})}\\big) = ${tvec(val.as[l])}`, true));
    }
    if ("ResizeObserver" in window) { let last = 0; new ResizeObserver(() => { const s = view.box.clientWidth; if (Math.abs(s - last) > 1) { last = s; view.layout(); draw(); } }).observe(view.box); }
    view.layout(); draw();
    if (!reduced()) { stage = 0; active = 0; draw(); setTimeout(() => player.start(), 600); }
  });

  // ======================================================================
  // 2. Matrix × vector inside a layer, one neuron (row) at a time
  // ======================================================================
  FV.widget("fp-matvec", (el, cfg) => {
    const net = cfg.net, Ln = net.W.length;
    const w = FV.shell(el, {});
    let l = 0, j = 0;
    const box = FV.h("div", { class: "fp-mv" });
    w.stage.append(box);
    const seg = FV.ui.seg({ label: L.layerSel, value: 0, options: net.W.map((_, i) => ({ value: i, label: String(i + 1) })), onchange: (v) => { player.stop(); l = v; j = -1; draw(); } });
    const player = FV.ui.player({ interval: 1100, onstep: () => step(), onreset: () => { j = -1; draw(); } });
    w.controls.append(seg.el, player.el);
    function step() {
      const n = net.W[l].length;
      if (j < n - 1) j++;
      else if (l < Ln - 1) { l++; j = 0; seg.set(l); }
      else { l = 0; j = -1; seg.set(0); draw(); return false; }
      draw(); return true;
    }
    const cell = (v, cls) => FV.h("td", { class: cls || null, text: n4(v) });
    function draw() {
      const val = forward(net, net.x), Wl = net.W[l], a = val.as[l], z = val.zs[l], aa = val.as[l + 1], b = net.b[l];
      box.textContent = "";
      const tb = FV.h("table", { class: "fp-mvt" });
      const head = FV.h("tr", {}, FV.h("th", {}, FV.rich(`$W^{(${l + 1})}$`)), FV.h("th", {}, ""), FV.h("th", {}, FV.rich(`$\\mathbf{a}^{(${l})}$`)), FV.h("th", {}, ""), FV.h("th", {}, FV.rich(`$\\mathbf{b}^{(${l + 1})}$`)), FV.h("th", {}, ""), FV.h("th", {}, FV.rich(`$\\mathbf{z}^{(${l + 1})}$`)), FV.h("th", {}, FV.rich(`$\\mathbf{a}^{(${l + 1})}$`)));
      tb.append(head);
      const rows = Math.max(Wl.length, a.length);
      for (let r = 0; r < rows; r++) {
        const tr = FV.h("tr", { class: r === j ? "hi" : null });
        const wcell = FV.h("td", { class: "fp-W" });
        if (r < Wl.length) Wl[r].forEach((v, c) => wcell.append(FV.h("span", { class: (v >= 0 ? "pos" : "neg") + (r === j ? " on" : ""), text: n4(v) })));
        tr.append(wcell, FV.h("td", { class: "fp-op", text: r === Math.floor((rows - 1) / 2) ? "×" : "" }));
        tr.append(r < a.length ? cell(a[r], "fp-a" + (j >= 0 ? " on" : "")) : FV.h("td", {}));
        tr.append(FV.h("td", { class: "fp-op", text: r === Math.floor((rows - 1) / 2) ? "+" : "" }));
        tr.append(r < b.length ? cell(b[r], "fp-b" + (r === j ? " on" : "")) : FV.h("td", {}));
        tr.append(FV.h("td", { class: "fp-op", text: r === Math.floor((rows - 1) / 2) ? "=" : "" }));
        tr.append(r < z.length ? cell(r <= j ? z[r] : NaN, "fp-z" + (r === j ? " on" : "")) : FV.h("td", {}));
        tr.append(r < aa.length ? cell(r <= j ? aa[r] : NaN, "fp-aa" + (r === j ? " on" : "")) : FV.h("td", {}));
        tb.append(tr);
      }
      tb.querySelectorAll("td").forEach((c) => { if (c.textContent === "—") c.textContent = "·"; });
      box.append(FV.h("div", { class: "table-wrap" }, tb));
      w.note.textContent = "";
      if (j < 0) { w.note.append(FV.rich(L.rowHint + ".", "p")); return; }
      const f = net.f[l];
      const terms = Wl[j].map((v, c) => `${tn(v, true)}\\cdot${tn(a[c], true)}`).join(" + ");
      w.note.append(FV.tex(`z^{(${l + 1})}_{${j + 1}} = ${terms} + ${tn(b[j], true)} = ${tn(z[j])},\\qquad a^{(${l + 1})}_{${j + 1}} = ${ACT_TEX[f]}(${tn(z[j])}) = ${tn(aa[j])}`, true));
    }
    draw();
  });

  // ======================================================================
  // 3. Shapes, parameters and cost of an architecture
  // ======================================================================
  FV.widget("fp-shapes", (el, cfg) => {
    const w = FV.shell(el, {});
    let sizes = (cfg.sizes || [2, 3, 2, 1]).slice();
    const inp = FV.h("input", { type: "text", class: "fp-in", value: sizes.join("-"), "aria-label": L.sizes, placeholder: L.sizesPh, inputmode: "numeric" });
    const err = FV.h("div", { class: "fp-err", "aria-live": "polite" });
    inp.addEventListener("input", () => {
      const v = inp.value.split(/[^0-9]+/).filter(Boolean).map(Number);
      if (v.length >= 2 && v.length <= 12 && v.every((n) => n >= 1 && n <= 100000)) { sizes = v; err.textContent = ""; draw(); } else err.textContent = L.bad;
    });
    const pres = FV.h("div", { class: "fv-seg" }, FV.h("span", { text: L.presets }), FV.h("div", { class: "fv-seg-btns" },
      (cfg.presets || []).map((p) => FV.h("button", { type: "button", onclick: () => { sizes = p.slice(); inp.value = p.join("-"); err.textContent = ""; draw(); } }, p.join("–")))));
    w.controls.append(FV.h("label", { class: "fp-inl" }, FV.h("span", { text: L.sizes }), inp), pres, err);
    const out = FV.h("div", { class: "fp-shapes" }); w.stage.append(out);
    const fmtI = (n) => n.toLocaleString(FV.lang === "en" ? "en-US" : "ru-RU").replace(/ /g, " ");
    function draw() {
      const rows = sizes.slice(1).map((o, i) => ({ l: i + 1, i: sizes[i], o, p: o * (sizes[i] + 1), m: o * sizes[i] }));
      const P = rows.reduce((s, r) => s + r.p, 0), M = rows.reduce((s, r) => s + r.m, 0);
      out.textContent = "";
      const th = [L.thL, L.thIO, L.thW, L.thB, L.thP, L.thM, L.share].map((t) => FV.h("th", {}, FV.rich(t)));
      const tb = FV.h("table", { class: "data fp-st" }, FV.h("thead", {}, FV.h("tr", {}, th)));
      const body = FV.h("tbody");
      rows.forEach((r) => body.append(FV.h("tr", {}, FV.h("td", { text: String(r.l) }), FV.h("td", { class: "num", text: `${fmtI(r.i)} → ${fmtI(r.o)}` }),
        FV.h("td", { class: "num", text: `${fmtI(r.o)} × ${fmtI(r.i)}` }), FV.h("td", { class: "num", text: fmtI(r.o) }), FV.h("td", { class: "num", text: fmtI(r.p) }), FV.h("td", { class: "num", text: fmtI(r.m) }),
        FV.h("td", {}, FV.h("span", { class: "fp-bar" }, FV.h("i", { style: `width:${Math.max(1, (100 * r.p) / P)}%` })), FV.h("small", { text: " " + FV.fmt((100 * r.p) / P, 1) + "%" })))));
      body.append(FV.h("tr", { class: "tot" }, FV.h("td", { text: L.total }), FV.h("td", { colspan: 3 }), FV.h("td", { class: "num", text: fmtI(P) }), FV.h("td", { class: "num", text: fmtI(M) }), FV.h("td")));
      tb.append(body);
      out.append(FV.h("div", { class: "table-wrap" }, tb));
      w.note.textContent = "";
      w.note.append(FV.tex(sizes.map((n, i) => (i ? `\\ \\xrightarrow{\\ W:\\ ${fmtI(n)}\\times${fmtI(sizes[i - 1])}\\ }\\ ` : "") + `\\mathbf{${fmtI(n)}}`).join(""), true));
    }
    draw();
  });

  // ======================================================================
  // 4. What a 2 → 2 layer does to the plane
  // ======================================================================
  FV.widget("fp-space", (el, cfg) => {
    const w = FV.shell(el, {});
    const PRE = {
      fold: { W: [[1, 0.15], [-1, 0.15]], b: [-0.2, -0.2], f: "relu", line: [1, 1, -0.8] },
      rot: { W: [[1.2, -0.6], [0.6, 1.2]], b: [0.2, -0.1], f: "tanh", line: null },
      shear: { W: [[1.5, 0.8], [0, 1.2]], b: [-0.3, 0.2], f: "sigmoid", line: null },
    };
    let pre = cfg.preset || "fold", t = 0, timer = 0;
    // data: the middle band (class 0) and the two outer bands (class 1) — not separable by one line in the input
    const rng = FV.rng(5), pts = [];
    for (let i = 0; i < 70; i++) { const x2 = -1.5 + 3 * rng(); pts.push({ p: [-0.6 + 1.2 * rng(), x2], c: 0 }); }
    for (let i = 0; i < 70; i++) { const s = rng() < 0.5 ? -1 : 1, x2 = -1.5 + 3 * rng(); pts.push({ p: [s * (1.4 + 0.8 * rng()), x2], c: 1 }); }
    const p = new FV.Plot(w.stage, { x: [-2.6, 2.6], y: [-2, 2], aspect: 0.62, xLabel: "1", yLabel: "2" });
    const st = FV.ui.slider({ label: L.stage, min: 0, max: 2, step: 0.01, value: 0, fmt: (v) => (v < 0.5 ? L.sInput : v < 1.5 ? FV.plain(L.sLin) : L.sAct), oninput: (v) => { stop(); t = v; draw(); }, wide: true });
    const seg = FV.ui.seg({ label: L.preset, value: pre, options: [{ value: "fold", label: L.pFold }, { value: "rot", label: L.pRot }, { value: "shear", label: L.pShear }], onchange: (v) => { pre = v; draw(); } });
    const play = FV.ui.button({ label: "▶ " + L.play, primary: true, onclick: () => (timer ? stop() : startA()) });
    w.controls.append(st.el, seg.el, play.el);
    function startA() { if (t >= 2) t = 0; play.setLabel("❚❚ " + FV.t("pause")); timer = setInterval(() => { t = Math.min(2, t + 0.02); st.set(t); draw(); if (t >= 2) stop(); }, 30); }
    function stop() { clearInterval(timer); timer = 0; play.setLabel("▶ " + L.play); }
    const T = (q) => {
      const P = PRE[pre], lin = [P.W[0][0] * q[0] + P.W[0][1] * q[1] + P.b[0], P.W[1][0] * q[0] + P.W[1][1] * q[1] + P.b[1]];
      if (t <= 1) return [q[0] + (lin[0] - q[0]) * t, q[1] + (lin[1] - q[1]) * t];
      const f = ACT[P.f], u = t - 1, act = lin.map(f);
      return [lin[0] + (act[0] - lin[0]) * u, lin[1] + (act[1] - lin[1]) * u];
    };
    p.onresize = draw;
    function draw() {
      const P = PRE[pre];
      // fit the view to the transformed picture
      const all = pts.map((d) => T(d.p));
      for (let a = -2.5; a <= 2.5; a += 0.5) for (let c = -2; c <= 2; c += 0.5) all.push(T([a, c]));
      const xs = all.map((q) => q[0]), ys = all.map((q) => q[1]);
      const pad = (lo, hi) => { const d = Math.max(0.6, hi - lo); return [lo - d * 0.08, hi + d * 0.08]; };
      p.setDomain(pad(Math.min(...xs), Math.max(...xs)), pad(Math.min(...ys), Math.max(...ys)));
      p.o.xLabel = t < 0.5 ? "x₁" : "h₁"; p.o.yLabel = t < 0.5 ? "x₂" : "h₂";
      p.clear();
      for (let a = -2.5; a <= 2.501; a += 0.5) p.path(FV.linspace(-2, 2, 40).map((c) => T([a, c])), { c: "guide", w: 1, opacity: 0.7 });
      for (let c = -2; c <= 2.001; c += 0.5) p.path(FV.linspace(-2.5, 2.5, 50).map((a) => T([a, c])), { c: "guide", w: 1, opacity: 0.7 });
      pts.forEach((d) => { const q = T(d.p); p.dot(q[0], q[1], { r: 3.6, c: d.c ? "orange" : "blue" }); });
      if (P.line && t > 1.85) {
        const [A, B, Cc] = P.line, D = p.o.x;
        p.line(D[0], -(A * D[0] + Cc) / B, D[1], -(A * D[1] + Cc) / B, { c: "ink", w: 2, opacity: Math.min(1, (t - 1.85) / 0.15) });
      }
      p.legend([{ label: L.class0, c: "blue", dot: true }, { label: L.class1, c: "orange", dot: true }].concat(P.line && t > 1.85 ? [{ label: L.sepLine, c: "ink" }] : []));
      w.note.textContent = "";
      w.note.append(FV.rich(t < 0.5 ? L.spaceNote0 : t < 1.5 ? L.spaceNote1 : P.line ? L.spaceNote2 : L.spaceNote2b, "p"));
      w.note.append(FV.tex(`W = \\begin{pmatrix}${P.W.map((r) => r.map((v) => tn(v)).join("&")).join("\\\\")}\\end{pmatrix},\\ \\mathbf{b} = ${tvec(P.b)},\\ f = ${ACT_TEX[P.f]}`, true));
    }
    draw();
  });

  // ======================================================================
  // 5. Playground: the network and its answer over the whole input plane
  // ======================================================================
  FV.widget("fp-playground", (el, cfg) => {
    const net = cfg.net, Ln = net.W.length;
    const w = FV.shell(el, { cols: true });
    const c1 = FV.col(w.stage), c2 = FV.col(w.stage);
    let x = net.x.slice(), acts = net.f.slice(), k = 1;
    const view = NetView(c1, net, { acts: () => acts, height: (W) => (W < 520 ? 280 : 320) });
    const p = new FV.Plot(c2, { x: [-3, 3], y: [-3, 3], equal: true, xLabel: "x₁", yLabel: "x₂", title: L.mapTitle, maxHeight: 420 });
    const h = p.handle(x[0], x[1], { c: "ink", label: "x", onDrag: (a, b) => { x = [Math.round(a * 4) / 4, Math.round(b * 4) / 4]; return x; }, onChange: () => { sx.forEach((s, i) => s.set(x[i])); draw(); } });
    const sx = x.map((v, i) => FV.ui.slider({ label: `$x_${i + 1}$`, min: -3, max: 3, step: 0.25, value: v, fmt: (u) => FV.fmt(u, 2), oninput: (u) => { x[i] = u; h.set(x[0], x[1]); draw(); } }));
    const actOpts = ["relu", "tanh", "sigmoid", "identity"].map((v) => ({ value: v, label: L[v] }));
    const s1 = FV.ui.seg({ label: L.act1, value: acts[0], options: actOpts, onchange: (v) => { acts[0] = v; draw(true); } });
    const s2 = FV.ui.seg({ label: L.act2, value: acts[1], options: actOpts, onchange: (v) => { acts[1] = v; draw(true); } });
    const sk = FV.ui.slider({ label: L.scale, min: 0.25, max: 3, step: 0.05, value: 1, fmt: (u) => "×" + FV.fmt(u, 2), oninput: (u) => { k = u; draw(true); } });
    w.controls.append(...sx.map((s) => s.el), sk.el, s1.el, s2.el);
    const ro = FV.ui.readout(w.readout, [{ key: "y", label: "$\\hat y$ =", c: "orange" }]);
    let heatKey = "";
    p.onresize = () => { heatKey = ""; draw(); };
    function draw() {
      const val = forward(net, x, acts, k);
      view.draw(val, Ln, 0, k);
      const key = acts.join() + k;
      if (key !== heatKey || !p.gMain.firstChild) {
        heatKey = key;
        p.clear();
        p.heat((a, b) => forward(net, [a, b], acts, k).as[Ln][0], { cmap: "diverging", z: [0, 1], res: 4, alpha: 0.85 });
        p.contours((a, b) => forward(net, [a, b], acts, k).as[Ln][0], [0.5], { c: "ink", w: 2, opacity: 1, n: 80 });
      }
      p.gHover.textContent = "";
      p.hl("dot", x[0], x[1], { r: 6, c: "ink", hollow: true });
      ro.set("y", n4(val.as[Ln][0]));
    }
    if ("ResizeObserver" in window) { let last = 0; new ResizeObserver(() => { const s = view.box.clientWidth; if (Math.abs(s - last) > 1) { last = s; view.layout(); draw(); } }).observe(view.box); }
    view.layout(); draw();
  });
})();
