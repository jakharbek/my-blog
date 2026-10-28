/* FV — a small visualization kit for the formula pages of the Materials section.
   No dependencies. SVG for 2D plots, canvas for 3D surfaces and heatmaps.
   Colours come from CSS tokens (--v-*), so a theme change needs no redraw for SVG;
   canvases redraw themselves on the "themechange" event.

   Usage in assets/js/formulas/<id>.js:

     FV.widget("sigmoid-explorer", (el, cfg) => {
       const w = FV.shell(el, { title: cfg.title });
       const p = new FV.Plot(w.stage, { x: [-8, 8], y: [-0.1, 1.1], xLabel: "x", yLabel: "σ(x)" });
       const s = FV.ui.slider({ label: "x", min: -8, max: 8, step: 0.1, value: 0, oninput: draw });
       w.controls.append(s.el);
       function draw() { p.clear(); p.fn(sig, { c: "blue" }); p.dot(s.value, sig(s.value)); }
       p.onresize = draw; draw();
     });

   Series colours (opts.c): ink, blue, orange, teal, red, violet, faint, guide.
*/
(function () {
  "use strict";
  const FV = (window.FV = window.FV || {});
  const doc = document;
  const root = doc.documentElement;
  const LANG = (root.lang || "en").slice(0, 2);
  const DEC = LANG === "en" ? "." : ",";
  const NS = "http://www.w3.org/2000/svg";
  FV.lang = LANG;

  const T = {
    ru: { drag: "Потяните, чтобы повернуть", reset: "Сбросить вид", play: "Пуск", pause: "Пауза", restart: "Сначала", step: "Шаг", error: "Не удалось построить рисунок" },
    en: { drag: "Drag to rotate", reset: "Reset view", play: "Play", pause: "Pause", restart: "Restart", step: "Step", error: "The figure could not be drawn" },
    uz: { drag: "Aylantirish uchun torting", reset: "Ko‘rinishni tiklash", play: "Boshlash", pause: "To‘xtatish", restart: "Boshidan", step: "Qadam", error: "Rasmni chizib bo‘lmadi" },
  };
  FV.t = (k) => (T[LANG] || T.en)[k] || T.en[k];

  // ---------- numbers ----------
  // fmt(0.5, 2) → "0,50" (ru, uz) / "0.50" (en); the minus is a real minus sign.
  FV.fmt = function (v, d = 2) {
    if (v === Infinity) return "∞";
    if (v === -Infinity) return "−∞";
    if (typeof v !== "number" || Number.isNaN(v)) return "—";
    let s = Math.abs(v).toFixed(d);
    if (/^[0.]+$/.test(s)) return s.replace(".", DEC);
    return (v < 0 ? "−" : "") + s.replace(".", DEC);
  };
  // Significant digits; tiny and huge values become a·10ⁿ.
  const SUP = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
  FV.num = function (v, sig = 3) {
    if (!Number.isFinite(v)) return FV.fmt(v);
    if (v === 0) return "0";
    const a = Math.abs(v);
    if (a >= 1e-3 && a < 1e6) {
      const d = Math.max(0, sig - 1 - Math.floor(Math.log10(a)));
      let s = FV.fmt(v, Math.min(d, 8));
      if (s.includes(DEC)) s = s.replace(new RegExp("\\" + DEC + "?0+$"), "");
      return s;
    }
    const e = Math.floor(Math.log10(a));
    const m = v / Math.pow(10, e);
    const ms = FV.fmt(m, sig - 1).replace(new RegExp("\\" + DEC + "?0+$"), "");
    return ms + "·10" + String(e).split("").map((c) => SUP[c]).join("");
  };
  FV.clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  FV.lerp = (a, b, t) => a + (b - a) * t;
  FV.linspace = (a, b, n) => Array.from({ length: n }, (_, i) => a + ((b - a) * i) / (n - 1));

  // Deterministic random numbers (Mulberry32) and a normal sample (Box–Muller).
  FV.rng = function (seed = 1) {
    let a = seed >>> 0;
    const next = () => {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
    next.normal = () => {
      const u = Math.max(next(), 1e-12), v = next();
      return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    };
    return next;
  };

  // Standard math used by many pages.
  FV.sigmoid = (x) => (x >= 0 ? 1 / (1 + Math.exp(-x)) : Math.exp(x) / (1 + Math.exp(x)));
  FV.erf = function (x) {
    // Abramowitz–Stegun 7.1.26, |error| < 1.5e-7
    const s = Math.sign(x), a = Math.abs(x), t = 1 / (1 + 0.3275911 * a);
    const y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-a * a);
    return s * y;
  };
  FV.Phi = (x) => 0.5 * (1 + FV.erf(x / Math.SQRT2));
  FV.phi = (x) => Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI);

  // ---------- DOM ----------
  FV.h = function (tag, attrs, ...kids) {
    const el = doc.createElement(tag);
    for (const k in attrs || {}) {
      const v = attrs[k];
      if (v == null || v === false) continue;
      if (k === "class") el.className = v;
      else if (k === "text") el.textContent = v;
      else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? "" : v);
    }
    kids.flat().forEach((c) => c != null && el.append(c.nodeType ? c : doc.createTextNode(String(c))));
    return el;
  };
  function S(tag, attrs, parent) {
    const el = doc.createElementNS(NS, tag);
    for (const k in attrs || {}) if (attrs[k] != null) el.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(el);
    return el;
  }
  FV.svg = S;

  // Text with $…$ rendered by KaTeX when it is available.
  FV.rich = function (str, tag = "span") {
    const el = doc.createElement(tag);
    const parts = String(str).split(/(\$[^$]+\$)/g);
    parts.forEach((p) => {
      if (p.length > 2 && p[0] === "$" && p[p.length - 1] === "$") {
        const span = doc.createElement("span");
        if (window.katex) {
          try { window.katex.render(p.slice(1, -1), span, { throwOnError: false }); }
          catch (e) { span.textContent = p.slice(1, -1); }
        } else span.textContent = p.slice(1, -1);
        el.append(span);
      } else if (p) el.append(doc.createTextNode(p));
    });
    return el;
  };
  FV.tex = function (src, display = false) {
    const el = doc.createElement(display ? "div" : "span");
    if (window.katex) {
      try { window.katex.render(src, el, { throwOnError: false, displayMode: display }); return el; } catch (e) {}
    }
    el.textContent = src;
    return el;
  };

  FV.css = (name) => getComputedStyle(root).getPropertyValue("--" + name).trim();
  FV.color = (c) => FV.css("v-" + (c || "ink"));

  // ---------- colour maps ----------
  const MAPS = {
    viridis: ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"],
    magma: ["#000004", "#51127c", "#b73779", "#fc8961", "#fcfdbf"],
    blues: ["#f0f4ff", "#c4d3fb", "#7f9ef0", "#3e6ae1", "#1b3a8c"],
  };
  function hex(c) { const n = parseInt(c.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
  const parsed = {};
  FV.cmap = function (name, t) {
    t = FV.clamp(Number.isFinite(t) ? t : 0, 0, 1);
    if (name === "diverging") {
      // blue ↔ neutral ↔ red around t = 0.5, neutral follows the theme
      const bg = hex(FV.css("v-mid") || "#e8e8e8");
      const a = hex(FV.css("v-blue") || "#3e6ae1"), b = hex(FV.css("v-red") || "#c4314b");
      const u = Math.abs(t - 0.5) * 2, c = t < 0.5 ? a : b;
      return bg.map((v, i) => Math.round(v + (c[i] - v) * Math.pow(u, 0.85)));
    }
    const stops = parsed[name] || (parsed[name] = (MAPS[name] || MAPS.viridis).map(hex));
    const x = t * (stops.length - 1), i = Math.min(stops.length - 2, Math.floor(x)), f = x - i;
    return stops[i].map((v, k) => Math.round(v + (stops[i + 1][k] - v) * f));
  };
  FV.rgb = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;

  // ---------- scales and ticks ----------
  function scale(type, d0, d1, r0, r1) {
    if (type === "log") {
      const l0 = Math.log10(d0), l1 = Math.log10(d1);
      return { type, d0, d1, map: (v) => r0 + ((Math.log10(v) - l0) / (l1 - l0)) * (r1 - r0), inv: (p) => Math.pow(10, l0 + ((p - r0) / (r1 - r0)) * (l1 - l0)) };
    }
    return { type, d0, d1, map: (v) => r0 + ((v - d0) / (d1 - d0)) * (r1 - r0), inv: (p) => d0 + ((p - r0) / (r1 - r0)) * (d1 - d0) };
  }
  function decimals(step) {
    for (let d = 0; d < 8; d++) if (Math.abs(Math.round(step * 10 ** d) - step * 10 ** d) < 1e-6) return d;
    return 8;
  }
  FV.ticks = function (a, b, n = 6) {
    const step0 = (b - a) / Math.max(1, n);
    const mag = Math.pow(10, Math.floor(Math.log10(step0)));
    const e = step0 / mag;
    const step = (e >= 7.5 ? 10 : e >= 3.5 ? 5 : e >= 1.5 ? 2 : 1) * mag;
    const out = [];
    for (let v = Math.ceil(a / step - 1e-9) * step; v <= b + step * 1e-9; v += step) out.push(Math.abs(v) < step * 1e-9 ? 0 : v);
    return { values: out, d: decimals(step) };
  };
  function logTicks(a, b) {
    const out = [];
    for (let e = Math.ceil(Math.log10(a) - 1e-9); e <= Math.floor(Math.log10(b) + 1e-9); e++) out.push(Math.pow(10, e));
    return out;
  }
  function tickLabel(v, d, log) {
    if (log) {
      const e = Math.round(Math.log10(v));
      if (e >= 0 && e <= 3) return String(Math.pow(10, e));
      if (e < 0 && e >= -2) return FV.fmt(v, -e);
      return "10" + String(e).split("").map((c) => SUP[c]).join("");
    }
    return FV.fmt(v, d);
  }

  // ---------- 2D plot (SVG) ----------
  const STYLE = (o = {}) => {
    const c = o.c || "ink";
    return {
      class: `s-${c}${o.cls ? " " + o.cls : ""}`,
      "stroke-width": o.w != null ? o.w : 2,
      "stroke-dasharray": o.dash === true ? "6 5" : o.dash || null,
      opacity: o.opacity != null ? o.opacity : null,
    };
  };

  class Plot {
    /* o: { x:[a,b], y:[c,d], xType:'log', yType:'log', aspect: 0.62, maxHeight: 440, minHeight: 220,
            xLabel, yLabel, xTicks:[v|{v,label}], yTicks, grid: true, equal: false, margin:{l,r,t,b}, title } */
    constructor(parent, o = {}) {
      this.o = Object.assign({ x: [-5, 5], y: [-1, 1], aspect: 0.62, maxHeight: 440, minHeight: 220, grid: true }, o);
      this.wrap = FV.h("div", { class: "fv-plot" });
      if (o.title) this.wrap.append(FV.rich(o.title, "div")), (this.wrap.firstChild.className = "fv-plot-title");
      parent.append(this.wrap);
      this.svg = S("svg", { class: "fv-svg", role: "img" }, null);
      if (o.ariaLabel) this.svg.setAttribute("aria-label", o.ariaLabel);
      this.wrap.append(this.svg);
      const id = "fvc" + Math.random().toString(36).slice(2, 9);
      this.clipId = id;
      const defs = S("defs", {}, this.svg);
      this.clipRect = S("rect", {}, S("clipPath", { id }, defs));
      this.gAxes = S("g", { class: "fv-axes" }, this.svg);
      this.gMain = S("g", { "clip-path": `url(#${id})` }, this.svg);
      this.gFree = S("g", {}, this.svg); // not clipped: labels
      this.gHover = S("g", { class: "fv-hover", "clip-path": `url(#${id})` }, this.svg);
      this.overlay = S("rect", { class: "fv-overlay" }, this.svg);
      this.gHandles = S("g", {}, this.svg);
      this.handles = [];
      this.legendEl = null;
      this.onresize = null;
      this.layout();
      if ("ResizeObserver" in window) {
        let last = this.W;
        this.ro = new ResizeObserver(() => {
          const w = Math.round(this.wrap.clientWidth);
          if (w && Math.abs(w - last) > 1) { last = w; this.layout(); this.onresize && this.onresize(); }
        });
        this.ro.observe(this.wrap);
      }
    }
    layout() {
      const o = this.o;
      const W = Math.max(260, Math.round(this.wrap.clientWidth || 640));
      const narrow = W < 480;
      const m = Object.assign({ l: narrow ? 40 : 50, r: narrow ? 10 : 16, t: 12, b: o.xLabel ? (narrow ? 40 : 44) : 28 }, o.margin || {});
      let H = Math.round(W * o.aspect);
      H = FV.clamp(H, o.minHeight, o.maxHeight);
      if (o.equal) {
        const pw = W - m.l - m.r;
        const ratio = (o.y[1] - o.y[0]) / (o.x[1] - o.x[0]);
        H = Math.round(pw * ratio + m.t + m.b);
      }
      this.W = W; this.H = H; this.m = m; this.narrow = narrow;
      this.svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
      this.svg.setAttribute("width", W);
      this.svg.setAttribute("height", H);
      this.x0 = m.l; this.x1 = W - m.r; this.y0 = H - m.b; this.y1 = m.t;
      this.sx = scale(o.xType || "lin", o.x[0], o.x[1], this.x0, this.x1);
      this.sy = scale(o.yType || "lin", o.y[0], o.y[1], this.y0, this.y1);
      Object.assign(this.clipRect.dataset, {});
      ["x", "y", "width", "height"].forEach((k, i) => this.clipRect.setAttribute(k, [this.x0, this.y1, this.x1 - this.x0, this.y0 - this.y1][i]));
      ["x", "y", "width", "height"].forEach((k, i) => this.overlay.setAttribute(k, [this.x0, this.y1, this.x1 - this.x0, this.y0 - this.y1][i]));
      this.handles.forEach((h) => h._place());
    }
    X(x) { return this.sx.map(x); }
    Y(y) { return this.sy.map(y); }
    setDomain(x, y) { if (x) this.o.x = x; if (y) this.o.y = y; this.layout(); }
    clear() {
      this.gMain.textContent = ""; this.gFree.textContent = ""; this.gHover.textContent = "";
      this.drawAxes();
      return this;
    }
    drawAxes() {
      const g = this.gAxes, o = this.o;
      g.textContent = "";
      S("rect", { x: this.x0, y: this.y1, width: this.x1 - this.x0, height: this.y0 - this.y1, class: "fv-frame" }, g);
      const xs = this._ticks("x"), ys = this._ticks("y");
      xs.forEach(({ v, label }) => {
        const px = this.X(v);
        if (o.grid) S("line", { x1: px, x2: px, y1: this.y1, y2: this.y0, class: v === 0 && !o.xTicks ? "fv-zero" : "fv-grid" }, g);
        const t = S("text", { x: px, y: this.y0 + 17, "text-anchor": "middle", class: "fv-tick" }, g);
        t.textContent = label;
      });
      ys.forEach(({ v, label }) => {
        const py = this.Y(v);
        if (o.grid) S("line", { x1: this.x0, x2: this.x1, y1: py, y2: py, class: v === 0 && !o.yTicks ? "fv-zero" : "fv-grid" }, g);
        const t = S("text", { x: this.x0 - 7, y: py + 4, "text-anchor": "end", class: "fv-tick" }, g);
        t.textContent = label;
      });
      if (o.xLabel) {
        const t = S("text", { x: (this.x0 + this.x1) / 2, y: this.H - 6, "text-anchor": "middle", class: "fv-label" }, g);
        t.textContent = o.xLabel;
      }
      if (o.yLabel) {
        const t = S("text", { x: this.x0 + 6, y: this.y1 + 14, "text-anchor": "start", class: "fv-label fv-ylabel" }, g);
        t.textContent = o.yLabel;
      }
    }
    _ticks(axis) {
      const o = this.o, dom = o[axis], type = o[axis + "Type"], given = o[axis + "Ticks"];
      if (given) return given.map((t) => (typeof t === "object" ? { v: t.v, label: t.label } : { v: t, label: FV.num(t) }));
      if (type === "log") return logTicks(dom[0], dom[1]).map((v) => ({ v, label: tickLabel(v, 0, true) }));
      const n = axis === "x" ? (this.narrow ? 4 : 7) : this.narrow ? 4 : 5;
      const t = FV.ticks(dom[0], dom[1], n);
      return t.values.map((v) => ({ v, label: tickLabel(v, t.d, false) }));
    }
    // Function graph; breaks at non-finite values and vertical jumps.
    fn(f, o = {}) {
      const a = o.from != null ? o.from : this.o.x[0], b = o.to != null ? o.to : this.o.x[1];
      const n = o.n || Math.max(200, Math.round(this.x1 - this.x0));
      const span = this.o.y[1] - this.o.y[0], lo = this.o.y[0] - span * 4, hi = this.o.y[1] + span * 4;
      const log = this.o.xType === "log";
      let d = "", pen = false, prev = null;
      for (let i = 0; i <= n; i++) {
        const x = log ? Math.pow(10, Math.log10(a) + ((Math.log10(b) - Math.log10(a)) * i) / n) : a + ((b - a) * i) / n;
        let y = f(x);
        if (this.o.yType === "log" && !(y > 0)) y = NaN;
        if (!Number.isFinite(y)) { pen = false; prev = null; continue; }
        y = FV.clamp(y, lo, hi);
        const px = this.X(x), py = this.Y(y);
        if (prev != null && o.jump && Math.abs(y - prev) > o.jump) pen = false;
        d += (pen ? "L" : "M") + px.toFixed(2) + " " + py.toFixed(2);
        pen = true; prev = y;
      }
      return S("path", Object.assign({ d, fill: "none" }, STYLE(o)), o.free ? this.gFree : this.gMain);
    }
    path(pts, o = {}) {
      let d = "";
      pts.forEach((p, i) => { if (p && Number.isFinite(p[0]) && Number.isFinite(p[1])) d += (i && d ? "L" : "M") + this.X(p[0]).toFixed(2) + " " + this.Y(p[1]).toFixed(2); });
      if (o.close) d += "Z";
      const attrs = Object.assign({ d, fill: "none" }, STYLE(o));
      if (o.fill) { attrs.fill = "currentColor"; attrs.class += " fill-" + (o.fillC || o.c || "ink"); attrs["fill-opacity"] = o.fillOpacity != null ? o.fillOpacity : 0.15; if (o.w == null) attrs["stroke-width"] = 0; }
      return S("path", attrs, o.free ? this.gFree : this.gMain);
    }
    line(x1, y1, x2, y2, o = {}) { return this.path([[x1, y1], [x2, y2]], Object.assign({ w: 1.5 }, o)); }
    vline(x, o = {}) { return this.line(x, this.o.y[0], x, this.o.y[1], Object.assign({ c: "guide", w: 1, dash: "4 4" }, o)); }
    hline(y, o = {}) { return this.line(this.o.x[0], y, this.o.x[1], y, Object.assign({ c: "guide", w: 1, dash: "4 4" }, o)); }
    // Filled region between f and g (g defaults to 0).
    area(f, g, o = {}) {
      const a = o.from != null ? o.from : this.o.x[0], b = o.to != null ? o.to : this.o.x[1], n = o.n || 200;
      const top = [], bot = [];
      for (let i = 0; i <= n; i++) { const x = a + ((b - a) * i) / n; top.push([x, f(x)]); bot.push([x, g ? g(x) : 0]); }
      return this.path(top.concat(bot.reverse()), Object.assign({ fill: true, close: true, fillOpacity: 0.14 }, o));
    }
    rect(x0, y0, x1, y1, o = {}) {
      const X0 = this.X(Math.min(x0, x1)), X1 = this.X(Math.max(x0, x1)), Y0 = this.Y(Math.max(y0, y1)), Y1 = this.Y(Math.min(y0, y1));
      return S("rect", { x: X0, y: Y0, width: Math.max(0, X1 - X0), height: Math.max(0, Y1 - Y0), class: "fill-" + (o.c || "ink"), fill: "currentColor", "fill-opacity": o.opacity != null ? o.opacity : 0.85, rx: o.rx || 0 }, o.free ? this.gFree : this.gMain);
    }
    bar(x, y, o = {}) { const w = (o.width || 0.7) / 2, base = o.base || 0; return this.rect(x - w, base, x + w, y, o); }
    dot(x, y, o = {}) {
      const c = S("circle", { cx: this.X(x), cy: this.Y(y), r: o.r || 5, class: `dot s-${o.c || "ink"} ${o.hollow ? "hollow" : "fill-" + (o.c || "ink")}`, "stroke-width": o.hollow ? 2 : 1.5 }, o.free ? this.gFree : this.gMain);
      return c;
    }
    text(x, y, str, o = {}) {
      const t = S("text", { x: this.X(x) + (o.dx || 0), y: this.Y(y) + (o.dy || 0), "text-anchor": o.anchor || "start", class: "fv-text" + (o.c ? " t-" + o.c : "") + (o.cls ? " " + o.cls : "") }, o.clip ? this.gMain : this.gFree);
      t.textContent = str;
      if (o.size) t.style.fontSize = o.size + "px";
      return t;
    }
    // Arrow from (x0,y0) to (x1,y1) in data coordinates.
    arrow(x0, y0, x1, y1, o = {}) {
      const X0 = this.X(x0), Y0 = this.Y(y0), X1 = this.X(x1), Y1 = this.Y(y1);
      const len = Math.hypot(X1 - X0, Y1 - Y0);
      const g = S("g", { class: `s-${o.c || "ink"} fill-${o.c || "ink"}` }, o.free ? this.gFree : this.gMain);
      if (len < 1) return g;
      const ux = (X1 - X0) / len, uy = (Y1 - Y0) / len, hs = o.head || 8;
      S("line", { x1: X0, y1: Y0, x2: X1 - ux * hs * 0.8, y2: Y1 - uy * hs * 0.8, "stroke-width": o.w || 2, "stroke-dasharray": o.dash ? "5 4" : null }, g);
      S("path", { d: `M${X1} ${Y1}L${X1 - ux * hs - uy * hs * 0.5} ${Y1 - uy * hs + ux * hs * 0.5}L${X1 - ux * hs + uy * hs * 0.5} ${Y1 - uy * hs - ux * hs * 0.5}Z`, fill: "currentColor", stroke: "none" }, g);
      return g;
    }
    // Heatmap of f(x, y) under everything else; cmap: viridis | magma | blues | diverging.
    heat(f, o = {}) {
      const res = o.res || 3, w = Math.max(1, Math.round((this.x1 - this.x0) / res)), h = Math.max(1, Math.round((this.y0 - this.y1) / res));
      const vals = new Float64Array(w * h);
      let lo = Infinity, hi = -Infinity;
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
        const x = this.sx.inv(this.x0 + ((i + 0.5) / w) * (this.x1 - this.x0)), y = this.sy.inv(this.y1 + ((j + 0.5) / h) * (this.y0 - this.y1));
        const v = f(x, y); vals[j * w + i] = v;
        if (Number.isFinite(v)) { if (v < lo) lo = v; if (v > hi) hi = v; }
      }
      const zmin = o.z ? o.z[0] : lo, zmax = o.z ? o.z[1] : hi;
      const tf = o.transform || ((v) => v);
      const a = tf(zmin), b = tf(zmax);
      const cv = doc.createElement("canvas"); cv.width = w; cv.height = h;
      const ctx = cv.getContext("2d"), img = ctx.createImageData(w, h);
      for (let k = 0; k < w * h; k++) {
        const t = (tf(vals[k]) - a) / (b - a || 1);
        const c = FV.cmap(o.cmap || "viridis", t);
        img.data[4 * k] = c[0]; img.data[4 * k + 1] = c[1]; img.data[4 * k + 2] = c[2]; img.data[4 * k + 3] = Number.isFinite(vals[k]) ? Math.round(255 * (o.alpha != null ? o.alpha : 1)) : 0;
      }
      ctx.putImageData(img, 0, 0);
      const im = S("image", { x: this.x0, y: this.y1, width: this.x1 - this.x0, height: this.y0 - this.y1, preserveAspectRatio: "none", href: cv.toDataURL() }, this.gMain);
      im.style.imageRendering = "auto";
      this.gMain.insertBefore(im, this.gMain.firstChild);
      return { min: zmin, max: zmax };
    }
    // Contour lines of f(x, y) at the given levels (marching squares).
    contours(f, levels, o = {}) {
      const n = o.n || 90, m = Math.round(n * (this.y0 - this.y1) / (this.x1 - this.x0)) || n;
      const xs = FV.linspace(this.o.x[0], this.o.x[1], n + 1), ys = FV.linspace(this.o.y[0], this.o.y[1], m + 1);
      const z = ys.map((y) => xs.map((x) => f(x, y)));
      const g = S("g", {}, this.gMain);
      levels.forEach((L, li) => {
        let d = "";
        const P = (i, j, i2, j2) => {
          const a = z[j][i], b = z[j2][i2], t = (L - a) / (b - a);
          return [this.X(xs[i] + (xs[i2] - xs[i]) * t), this.Y(ys[j] + (ys[j2] - ys[j]) * t)];
        };
        for (let j = 0; j < m; j++) for (let i = 0; i < n; i++) {
          const v = [z[j][i], z[j][i + 1], z[j + 1][i + 1], z[j + 1][i]];
          if (!v.every(Number.isFinite)) continue;
          const idx = (v[0] > L ? 1 : 0) | (v[1] > L ? 2 : 0) | (v[2] > L ? 4 : 0) | (v[3] > L ? 8 : 0);
          if (idx === 0 || idx === 15) continue;
          const e = { b: () => P(i, j, i + 1, j), r: () => P(i + 1, j, i + 1, j + 1), t: () => P(i, j + 1, i + 1, j + 1), l: () => P(i, j, i, j + 1) };
          const segs = { 1: ["l", "b"], 2: ["b", "r"], 3: ["l", "r"], 4: ["r", "t"], 5: ["l", "t", "b", "r"], 6: ["b", "t"], 7: ["l", "t"], 8: ["t", "l"], 9: ["t", "b"], 10: ["t", "r", "b", "l"], 11: ["t", "r"], 12: ["r", "l"], 13: ["r", "b"], 14: ["b", "l"] }[idx];
          for (let k = 0; k < segs.length; k += 2) {
            const p = e[segs[k]](), q = e[segs[k + 1]]();
            d += `M${p[0].toFixed(1)} ${p[1].toFixed(1)}L${q[0].toFixed(1)} ${q[1].toFixed(1)}`;
          }
        }
        const st = typeof o.style === "function" ? o.style(L, li) : o;
        S("path", Object.assign({ d, fill: "none" }, STYLE(Object.assign({ c: "ink", w: 1, opacity: 0.45 }, st))), g);
      });
      return g;
    }
    // Pointer tracking inside the plot area: cb(x, y) in data units, cb(null) on leave.
    hover(cb) {
      const ov = this.overlay;
      ov.style.pointerEvents = "all";
      const move = (e) => {
        const r = this.svg.getBoundingClientRect(), k = this.W / r.width;
        const px = (e.clientX - r.left) * k, py = (e.clientY - r.top) * k;
        this.gHover.textContent = "";
        cb(this.sx.inv(px), this.sy.inv(py), e);
      };
      ov.addEventListener("pointermove", move);
      ov.addEventListener("pointerdown", move);
      ov.addEventListener("pointerleave", () => { this.gHover.textContent = ""; cb(null, null); });
    }
    // Hover layer helpers: draw on top, cleared on every pointer move.
    hl(fnName, ...args) {
      const keep = this.gMain; this.gMain = this.gHover; const keepF = this.gFree; this.gFree = this.gHover;
      try { return this[fnName](...args); } finally { this.gMain = keep; this.gFree = keepF; }
    }
    // Draggable point. onDrag(x, y) may return [x, y] to constrain the position.
    handle(x, y, o = {}) {
      const plot = this;
      const g = S("g", { class: "fv-handle s-" + (o.c || "blue"), tabindex: 0, role: "slider", "aria-label": o.label || "" }, this.gHandles);
      const hit = S("circle", { r: 18, class: "hit" }, g);
      const c = S("circle", { r: o.r || 7, class: "knob fill-" + (o.c || "blue") }, g);
      const h = {
        x, y, g,
        _place() { g.setAttribute("transform", `translate(${plot.X(h.x)} ${plot.Y(h.y)})`); },
        set(nx, ny) { h.x = nx; h.y = ny; h._place(); },
      };
      let drag = false;
      const at = (e) => {
        const r = plot.svg.getBoundingClientRect(), k = plot.W / r.width;
        return [plot.sx.inv((e.clientX - r.left) * k), plot.sy.inv((e.clientY - r.top) * k)];
      };
      const apply = (nx, ny) => {
        nx = FV.clamp(nx, Math.min(...plot.o.x), Math.max(...plot.o.x)); ny = FV.clamp(ny, Math.min(...plot.o.y), Math.max(...plot.o.y));
        const r = o.onDrag ? o.onDrag(nx, ny) : null;
        if (Array.isArray(r)) h.set(r[0], r[1]); else h.set(nx, ny);
        o.onChange && o.onChange(h.x, h.y);
      };
      g.addEventListener("pointerdown", (e) => { drag = true; g.setPointerCapture(e.pointerId); g.classList.add("active"); e.preventDefault(); });
      g.addEventListener("pointermove", (e) => { if (drag) apply(...at(e)); });
      const up = () => { drag = false; g.classList.remove("active"); };
      g.addEventListener("pointerup", up); g.addEventListener("pointercancel", up);
      g.addEventListener("keydown", (e) => {
        const sx = (plot.o.x[1] - plot.o.x[0]) / 100, sy = (plot.o.y[1] - plot.o.y[0]) / 100;
        const d = { ArrowLeft: [-sx, 0], ArrowRight: [sx, 0], ArrowUp: [0, sy], ArrowDown: [0, -sy] }[e.key];
        if (d) { e.preventDefault(); apply(h.x + d[0], h.y + d[1]); }
      });
      h._place();
      this.handles.push(h);
      return h;
    }
    legend(items) {
      if (!this.legendEl) { this.legendEl = FV.h("div", { class: "fv-legend" }); this.wrap.append(this.legendEl); }
      this.legendEl.textContent = "";
      items.forEach((it) => {
        const sw = FV.h("i", { class: "sw sw-" + (it.c || "ink") + (it.dash ? " dash" : "") + (it.dot ? " dotted" : "") + (it.box ? " box" : "") });
        this.legendEl.append(FV.h("span", {}, sw, FV.rich(it.label)));
      });
    }
  }
  FV.Plot = Plot;

  // ---------- 3D surface (canvas, painter's algorithm) ----------
  class Surface {
    /* o: { f(x,y), x:[a,b], y:[c,d], z:[lo,hi] (optional, clamps), n: 36, aspect: 0.72, maxHeight: 460,
            labels: {x, y, z}, cmap: 'viridis', azimuth: -0.75, elevation: 0.5, zScale: 0.8, wire: true } */
    constructor(parent, o) {
      this.o = Object.assign({ n: 36, aspect: 0.72, maxHeight: 460, minHeight: 260, cmap: "viridis", azimuth: -0.75, elevation: 0.5, zScale: 0.8, wire: true, labels: {} }, o);
      this.az = this.o.azimuth; this.el = this.o.elevation;
      this.wrap = FV.h("div", { class: "fv-3d" });
      if (o.title) this.wrap.append(FV.rich(o.title, "div")), (this.wrap.firstChild.className = "fv-plot-title");
      this.canvas = FV.h("canvas", { role: "img", "aria-label": o.ariaLabel || "" });
      this.hint = FV.h("div", { class: "fv-3d-hint" }, FV.h("span", { text: "⟲ " + FV.t("drag") }), FV.h("button", { type: "button", class: "fv-link", text: FV.t("reset"), onclick: () => { this.az = this.o.azimuth; this.el = this.o.elevation; this.draw(); } }));
      this.wrap.append(this.canvas, this.hint);
      parent.append(this.wrap);
      this.paths = []; this.points = []; this.planes = [];
      this.f = o.f;
      this.sample();
      this.resize();
      let px = 0, py = 0, on = false, raf = 0;
      this.canvas.addEventListener("pointerdown", (e) => { on = true; px = e.clientX; py = e.clientY; this.canvas.setPointerCapture(e.pointerId); });
      this.canvas.addEventListener("pointermove", (e) => {
        if (!on) return;
        this.az -= (e.clientX - px) * 0.008;
        if (e.pointerType !== "touch") this.el = FV.clamp(this.el + (e.clientY - py) * 0.006, 0.05, 1.5);
        px = e.clientX; py = e.clientY;
        if (!raf) raf = requestAnimationFrame(() => { raf = 0; this.draw(); });
      });
      const up = () => { on = false; };
      this.canvas.addEventListener("pointerup", up); this.canvas.addEventListener("pointercancel", up);
      this.canvas.addEventListener("dblclick", () => { this.az = this.o.azimuth; this.el = this.o.elevation; this.draw(); });
      if ("ResizeObserver" in window) {
        let last = 0;
        new ResizeObserver(() => { const w = this.wrap.clientWidth; if (Math.abs(w - last) > 1) { last = w; this.resize(); } }).observe(this.wrap);
      }
      doc.addEventListener("themechange", () => this.draw());
    }
    setF(f, z) { this.f = f; if (z) this.o.z = z; this.sample(); this.draw(); }
    setDomain(x, y, z) { if (x) this.o.x = x; if (y) this.o.y = y; if (z) this.o.z = z; this.sample(); this.draw(); }
    // Polylines on the surface: [{ pts: [[x,y,z],…], c: 'orange', w: 2.5 }]
    setPaths(p) { this.paths = p || []; this.draw(); }
    // Points: [{ x, y, z, c, label, r }]
    setPoints(p) { this.points = p || []; this.draw(); }
    // Horizontal planes: [{ z, c, opacity }]
    setPlanes(p) { this.planes = p || []; this.draw(); }
    sample() {
      const { n, x, y } = this.o;
      const Z = [];
      let lo = Infinity, hi = -Infinity;
      for (let j = 0; j <= n; j++) {
        const row = [];
        for (let i = 0; i <= n; i++) {
          const v = this.f(x[0] + ((x[1] - x[0]) * i) / n, y[0] + ((y[1] - y[0]) * j) / n);
          row.push(v);
          if (Number.isFinite(v)) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
        }
        Z.push(row);
      }
      this.Z = Z;
      this.zr = this.o.z ? this.o.z.slice() : [lo, hi === lo ? lo + 1 : hi];
    }
    resize() {
      const W = Math.max(260, this.wrap.clientWidth || 640);
      const H = FV.clamp(Math.round(W * this.o.aspect), this.o.minHeight, this.o.maxHeight);
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      this.W = W; this.H = H;
      this.canvas.width = Math.round(W * dpr); this.canvas.height = Math.round(H * dpr);
      this.canvas.style.width = W + "px"; this.canvas.style.height = H + "px";
      this.dpr = dpr;
      this.draw();
    }
    norm(x, y, z) {
      const o = this.o;
      const zc = FV.clamp(z, this.zr[0], this.zr[1]);
      return [((x - o.x[0]) / (o.x[1] - o.x[0])) * 2 - 1, ((y - o.y[0]) / (o.y[1] - o.y[0])) * 2 - 1, (((zc - this.zr[0]) / (this.zr[1] - this.zr[0])) * 2 - 1) * o.zScale];
    }
    proj(nx, ny, nz) {
      const ca = Math.cos(this.az), sa = Math.sin(this.az), ce = Math.cos(this.el), se = Math.sin(this.el);
      const xr = nx * ca - ny * sa, yr = nx * sa + ny * ca;
      const up = nz * ce + yr * se, depth = yr * ce - nz * se;
      return [this.W / 2 + xr * this.s, this.cy - up * this.s, depth];
    }
    P(x, y, z) { const n = this.norm(x, y, z); return this.proj(n[0], n[1], n[2]); }
    draw() {
      if (!this.Z) return;
      const ctx = this.canvas.getContext("2d"), o = this.o, n = o.n;
      // fit the box for any azimuth: horizontal half-extent √2, vertical depends on the elevation
      const halfH = o.zScale * Math.cos(this.el) + Math.SQRT2 * Math.sin(this.el);
      this.s = Math.min((this.W - 2 * 40) / (2 * Math.SQRT2), (this.H - 2 * 30) / (2 * halfH));
      this.cy = this.H / 2;
      ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
      ctx.clearRect(0, 0, this.W, this.H);
      const ink = FV.color("ink"), faint = FV.color("faint"), grid = FV.color("grid");
      ctx.font = `12px ${FV.css("sans") || "sans-serif"}`;
      // floor grid and box
      const zf = -o.zScale;
      ctx.lineWidth = 1;
      ctx.strokeStyle = grid;
      const gl = (a, b) => { const p = this.proj(...a), q = this.proj(...b); ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke(); };
      for (let k = 0; k <= 4; k++) { const t = -1 + k / 2; gl([t, -1, zf], [t, 1, zf]); gl([-1, t, zf], [1, t, zf]); }
      // back vertical edge: the corner farthest from the viewer
      const corners = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
      let back = corners[0], bd = -Infinity;
      corners.forEach((c) => { const d = this.proj(c[0], c[1], 0)[2]; if (d > bd) { bd = d; back = c; } });
      ctx.strokeStyle = faint;
      gl([back[0], back[1], zf], [back[0], back[1], o.zScale]);
      // z ticks on the back edge
      ctx.fillStyle = faint;
      const zt = FV.ticks(this.zr[0], this.zr[1], 4);
      zt.values.forEach((v) => {
        const p = this.proj(back[0], back[1], this.norm(o.x[0], o.y[0], v)[2]);
        ctx.strokeStyle = grid; gl([back[0], back[1], this.norm(0, 0, v)[2]], [back[0] * 0.94, back[1] * 0.94, this.norm(0, 0, v)[2]]);
        ctx.textAlign = "right"; ctx.fillText(tickLabel(v, zt.d), p[0] - 6, p[1] + 4);
      });
      // scene items, sorted far to near
      const items = [];
      const nz = this.Z.map((row, j) => row.map((v, i) => this.norm(o.x[0] + ((o.x[1] - o.x[0]) * i) / n, o.y[0] + ((o.y[1] - o.y[0]) * j) / n, Number.isFinite(v) ? v : this.zr[0])));
      const pj = nz.map((row) => row.map((p) => this.proj(p[0], p[1], p[2])));
      const L = [0.35, -0.45, 0.82];
      for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
        const a = nz[j][i], b = nz[j][i + 1], c = nz[j + 1][i + 1], d = nz[j + 1][i];
        const ux = c[0] - a[0], uy = c[1] - a[1], uz = c[2] - a[2], vx = d[0] - b[0], vy = d[1] - b[1], vz = d[2] - b[2];
        let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nzz = ux * vy - uy * vx;
        const nl = Math.hypot(nx, ny, nzz) || 1; nx /= nl; ny /= nl; nzz /= nl;
        const shade = 0.62 + 0.38 * Math.abs(nx * L[0] + ny * L[1] + nzz * L[2]);
        const zavg = (a[2] + b[2] + c[2] + d[2]) / 4;
        const t = (zavg / o.zScale + 1) / 2;
        const q = [pj[j][i], pj[j][i + 1], pj[j + 1][i + 1], pj[j + 1][i]];
        items.push({ d: (q[0][2] + q[1][2] + q[2][2] + q[3][2]) / 4, k: 0, q, col: FV.cmap(o.cmap, o.cmapT ? o.cmapT(t) : t).map((v) => Math.round(v * shade)) });
      }
      this.planes.forEach((pl) => {
        const z = this.norm(0, 0, pl.z)[2];
        const q = corners.map((c) => this.proj(c[0], c[1], z));
        items.push({ d: (q[0][2] + q[1][2] + q[2][2] + q[3][2]) / 4 + 0.05, k: 3, q, c: pl.c || "faint", a: pl.opacity != null ? pl.opacity : 0.18 });
      });
      this.paths.forEach((p) => {
        for (let k = 1; k < p.pts.length; k++) {
          const A = this.P(...p.pts[k - 1]), B = this.P(...p.pts[k]);
          items.push({ d: (A[2] + B[2]) / 2 - 0.02, k: 1, A, B, c: p.c || "orange", w: p.w || 2.5 });
        }
      });
      this.points.forEach((p) => { const A = this.P(p.x, p.y, p.z); items.push({ d: A[2] - 0.03, k: 2, A, c: p.c || "orange", r: p.r || 5, label: p.label }); });
      items.sort((u, v) => v.d - u.d);
      const bg = FV.css("card") || "#fff";
      items.forEach((it) => {
        if (it.k === 0) {
          ctx.beginPath(); ctx.moveTo(it.q[0][0], it.q[0][1]);
          for (let k = 1; k < 4; k++) ctx.lineTo(it.q[k][0], it.q[k][1]);
          ctx.closePath();
          ctx.fillStyle = FV.rgb(it.col); ctx.fill();
          ctx.strokeStyle = o.wire ? FV.rgb(it.col.map((v) => Math.round(v * 0.78))) : FV.rgb(it.col);
          ctx.lineWidth = 0.6; ctx.stroke();
        } else if (it.k === 3) {
          ctx.beginPath(); ctx.moveTo(it.q[0][0], it.q[0][1]);
          for (let k = 1; k < 4; k++) ctx.lineTo(it.q[k][0], it.q[k][1]);
          ctx.closePath(); ctx.globalAlpha = it.a; ctx.fillStyle = FV.color(it.c); ctx.fill(); ctx.globalAlpha = 1;
        } else if (it.k === 1) {
          ctx.strokeStyle = FV.color(it.c); ctx.lineWidth = it.w; ctx.lineCap = "round";
          ctx.beginPath(); ctx.moveTo(it.A[0], it.A[1]); ctx.lineTo(it.B[0], it.B[1]); ctx.stroke();
        } else {
          ctx.beginPath(); ctx.arc(it.A[0], it.A[1], it.r, 0, Math.PI * 2);
          ctx.lineWidth = 3; ctx.strokeStyle = bg; ctx.stroke(); ctx.fillStyle = FV.color(it.c); ctx.fill();
          if (it.label) { ctx.fillStyle = ink; ctx.textAlign = "left"; ctx.fillText(it.label, it.A[0] + 8, it.A[1] - 8); }
        }
      });
      // axis names and end ticks along the two front floor edges
      ctx.fillStyle = faint; ctx.textAlign = "center";
      const lab = o.labels || {};
      const edge = (a, b, v0, v1, name) => {
        const p = this.proj(a[0], a[1], zf), q = this.proj(b[0], b[1], zf);
        const mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2;
        const cx = this.W / 2, cy = this.cy, dx = mx - cx, dy = my - cy, dl = Math.hypot(dx, dy) || 1;
        ctx.fillStyle = faint;
        ctx.fillText(FV.num(v0), p[0] + (dx / dl) * 14, p[1] + (dy / dl) * 14 + 4);
        ctx.fillText(FV.num(v1), q[0] + (dx / dl) * 14, q[1] + (dy / dl) * 14 + 4);
        if (name) { ctx.fillStyle = ink; ctx.fillText(name, mx + (dx / dl) * 26, my + (dy / dl) * 26 + 4); }
      };
      // pick the x-edge and y-edge nearest the viewer
      const yEdge = this.proj(0, -1, zf)[2] < this.proj(0, 1, zf)[2] ? -1 : 1;
      const xEdge = this.proj(-1, 0, zf)[2] < this.proj(1, 0, zf)[2] ? -1 : 1;
      edge([-1, yEdge], [1, yEdge], o.x[0], o.x[1], lab.x);
      edge([xEdge, -1], [xEdge, 1], o.y[0], o.y[1], lab.y);
      if (lab.z) { const p = this.proj(back[0], back[1], o.zScale); ctx.fillStyle = ink; ctx.textAlign = "center"; ctx.fillText(lab.z, p[0], p[1] - 10); }
    }
  }
  FV.Surface = Surface;

  // ---------- figure shell and controls ----------
  FV.shell = function (el, o = {}) {
    el.textContent = "";
    el.classList.add("fv");
    const head = o.title ? FV.h("div", { class: "fv-head" }, FV.rich(o.title, "div")) : null;
    if (head) head.firstChild.className = "fv-title";
    const stage = FV.h("div", { class: "fv-stage" + (o.cols ? " cols" : "") });
    const controls = FV.h("div", { class: "fv-controls" });
    const readout = FV.h("div", { class: "fv-readout" });
    const note = FV.h("div", { class: "fv-note", "aria-live": "polite" });
    el.append(...[head, stage, controls, readout, note].filter(Boolean));
    return { root: el, stage, controls, readout, note };
  };
  // A sub-column inside a multi-column stage.
  FV.col = (stage) => { const c = FV.h("div", { class: "fv-col" }); stage.append(c); return c; };

  FV.ui = {
    slider(o) {
      const id = "fvs" + Math.random().toString(36).slice(2, 8);
      const out = FV.h("output", { for: id });
      const input = FV.h("input", { type: "range", id, min: o.min, max: o.max, step: o.step || "any", value: o.value });
      const fmt = o.fmt || ((v) => FV.num(v, 3));
      const api = {
        el: FV.h("label", { class: "fv-slider" + (o.wide ? " wide" : "") }, FV.rich(o.label, "span"), input, out),
        get value() { return o.map ? o.map(+input.value) : +input.value; },
        set(v) { input.value = o.unmap ? o.unmap(v) : v; out.textContent = fmt(api.value); },
        input,
      };
      out.textContent = fmt(api.value);
      input.addEventListener("input", () => { out.textContent = fmt(api.value); o.oninput && o.oninput(api.value); });
      return api;
    },
    seg(o) {
      let value = o.value;
      const btns = o.options.map((op) => {
        const b = FV.h("button", { type: "button", "aria-pressed": op.value === value ? "true" : "false" }, FV.rich(op.label));
        b.addEventListener("click", () => { api.set(op.value); o.onchange && o.onchange(value); });
        b._v = op.value;
        return b;
      });
      const api = {
        el: FV.h("div", { class: "fv-seg", role: "group" }, o.label ? FV.rich(o.label, "span") : null, FV.h("div", { class: "fv-seg-btns" }, btns)),
        get value() { return value; },
        set(v) { value = v; btns.forEach((b) => b.setAttribute("aria-pressed", b._v === v ? "true" : "false")); },
      };
      return api;
    },
    check(o) {
      const input = FV.h("input", { type: "checkbox" });
      input.checked = !!o.checked;
      input.addEventListener("change", () => o.onchange && o.onchange(input.checked));
      return { el: FV.h("label", { class: "fv-check" }, input, FV.rich(o.label)), get value() { return input.checked; }, set(v) { input.checked = v; } };
    },
    button(o) {
      const b = FV.h("button", { type: "button", class: "fv-btn" + (o.primary ? " primary" : "") }, FV.rich(o.label));
      b.addEventListener("click", () => o.onclick && o.onclick());
      return { el: b, setLabel(s) { b.textContent = ""; b.append(FV.rich(s)); } };
    },
    // Play / pause / restart. onstep() returns false to stop.
    player(o) {
      let timer = 0;
      const play = FV.ui.button({ label: "▶ " + FV.t("play"), primary: true, onclick: () => (timer ? stop() : start()) });
      const step = FV.ui.button({ label: FV.t("step") + " →", onclick: () => { stop(); o.onstep(); } });
      const reset = FV.ui.button({ label: "↺ " + FV.t("restart"), onclick: () => { stop(); o.onreset && o.onreset(); } });
      function start() {
        play.setLabel("❚❚ " + FV.t("pause"));
        timer = setInterval(() => { if (o.onstep() === false) stop(); }, o.interval || 120);
      }
      function stop() { clearInterval(timer); timer = 0; play.setLabel("▶ " + FV.t("play")); }
      return { el: FV.h("div", { class: "fv-player" }, play.el, step.el, reset.el), start, stop, get running() { return !!timer; } };
    },
    // Read-out values: items [{ key, label }] → set(key, text)
    readout(parent, items) {
      const cells = {};
      items.forEach((it) => {
        const v = FV.h("b", { class: it.c ? "t-" + it.c : null, text: "—" });
        cells[it.key] = v;
        parent.append(FV.h("span", { class: "fv-ro" }, FV.rich(it.label), v));
      });
      return { set(k, t) { if (cells[k]) cells[k].textContent = t; } };
    },
  };

  // ---------- widgets ----------
  const registry = {};
  FV.widget = (name, fn) => { registry[name] = fn; };
  function init(el) {
    if (el._fv) return;
    el._fv = true;
    const name = el.getAttribute("data-viz");
    let cfg = {};
    try { cfg = JSON.parse(el.getAttribute("data-config") || "{}"); } catch (e) { console.error("FV config", name, e); }
    const fn = registry[name];
    if (!fn) { console.error("FV: unknown widget " + name); el.textContent = FV.t("error"); return; }
    try { fn(el, cfg); } catch (e) { console.error("FV " + name, e); el.textContent = FV.t("error"); }
  }
  FV.boot = function () {
    const els = Array.from(doc.querySelectorAll("[data-viz]"));
    if ("IntersectionObserver" in window && !FV.eager) {
      const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { io.unobserve(e.target); init(e.target); } }), { rootMargin: "600px 0px" });
      els.forEach((el) => io.observe(el));
    } else els.forEach(init);
  };
  FV.initAll = () => doc.querySelectorAll("[data-viz]").forEach(init);
  // Widget scripts load after this file (defer), so start only once the document is parsed.
  let booted = false;
  const go = () => { if (!booted) { booted = true; FV.boot(); } };
  doc.addEventListener("DOMContentLoaded", go);
  window.addEventListener("load", go);
  if (doc.readyState === "complete") setTimeout(go);
})();
