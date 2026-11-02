/* Widgets of the material "Cross-entropy in Excel": the sheets of the workbook, live in the browser.
   Built on FV (assets/js/viz.js). Labels come from data-config (cfg.L), numbers are formatted by FV.fmt
   (decimal comma for ru/uz, real minus sign). The formulas repeat the workbook cell by cell:
   BCE  — D = 1/(1+EXP(−C)), E = B·LN(D), F = (1−B)·LN(1−D), G = E+F, BCE = −ΣG / n;
   CE   — D = EXP(C)/ΣEXP(C), E = LN(D), F = B·E, CE = −ΣF;
   practice — ✓ when |answer − key| < 0.005, as in the sheet. */
(function () {
  "use strict";
  const h = FV.h;
  const f3 = (v) => FV.fmt(v, 3);
  const f4 = (v) => FV.fmt(v, 4);
  const sig = (z) => 1 / (1 + Math.exp(-z)); // the workbook formula as written (overflow → NaN, like #NUM!)

  // "−0,223", "-0.223", " 2,2 " → number; anything else → NaN
  function parse(s) {
    const t = String(s).trim().replace(/[−–]/g, "-").replace(",", ".");
    if (!/^[-+]?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?$/i.test(t)) return NaN;
    return parseFloat(t);
  }
  const lnOrNaN = (x) => (x > 0 ? Math.log(x) : NaN);
  const cell = (cls, content) => h("td", { class: cls }, content);
  const num = (v) => (Number.isFinite(v) ? f3(v) : null);

  // a logit as the workbook shows it: 2,2 · −1,4 · 0,5 · 2
  const zText = (v) => FV.fmt(v, Number.isInteger(v) ? 0 : 1);
  function input(value, onchange, label) {
    const el = h("input", { type: "text", inputmode: "decimal", value: zText(value), "aria-label": label, autocomplete: "off", spellcheck: "false" });
    el.addEventListener("input", () => { el.setAttribute("aria-invalid", Number.isNaN(parse(el.value)) ? "true" : "false"); onchange(); });
    return el;
  }
  function table(heads, cls) {
    const tbody = h("tbody");
    const t = h("table", { class: "cew-sheet " + (cls || "") }, h("thead", {}, h("tr", {}, heads.map((x) => h("th", { class: x[1] || "" }, x[0])))), tbody);
    return { el: h("div", { class: "table-wrap" }, t), tbody };
  }
  function presets(list) {
    const bar = h("div", { class: "cew-presets" });
    list.forEach((p) => { const b = FV.ui.button({ label: p.label, onclick: p.run }); bar.append(b.el); });
    return bar;
  }
  const setTxt = (td, v, bad) => { td.textContent = v == null ? bad : v; td.classList.toggle("cew-err", v == null); };

  // ---------------------------------------------------------------- BCE sheet, blocks 1 and 2
  FV.widget("cew-bce-sheet", (el, cfg) => {
    const L = cfg.L;
    const w = FV.shell(el, {});
    const t1 = table([[L.i], [L.y, "in"], [L.z, "in"], [L.p, "tr"], [L.a, "fm"], [L.b, "fm"], [L.s, "fm2"]], "bce");
    const t2 = table([[L.i], [L.z], [L.lnz], [L.ln1z], [L.res], [L.what]], "raw");
    const rows = cfg.y.map((y0, i) => {
      const r = { y: y0 };
      r.yBtn = h("button", { type: "button", class: "cew-y", "aria-label": L.y + " " + (i + 1) }, String(y0));
      r.yBtn.addEventListener("click", () => { r.y = 1 - r.y; r.yBtn.textContent = String(r.y); draw(); });
      r.zIn = input(cfg.z[i], draw, L.z + " " + (i + 1));
      r.c = [cell("tr num"), cell("fm num"), cell("fm num"), cell("fm2 num")];
      t1.tbody.append(h("tr", {}, cell("idx", String(i + 1)), cell("in", r.yBtn), cell("in", r.zIn), ...r.c));
      r.d = [cell("num"), cell("num"), cell("num"), cell("num"), cell("what")];
      t2.tbody.append(h("tr", {}, cell("idx", String(i + 1)), ...r.d));
      return r;
    });
    const tot = {};
    const foot = (tb, span, label, key, cls, withNote) => {
      tot[key] = cell((cls || "") + " num");
      const tr = h("tr", { class: "cew-foot" }, h("td", { colspan: span, class: "lab" }, label), tot[key]);
      if (withNote) tr.append((tot[key + "_m"] = cell("what")));
      tb.append(tr);
    };
    foot(t1.tbody, 6, L.sum, "sum", "tot1"); foot(t1.tbody, 6, L.n, "n"); foot(t1.tbody, 6, L.bce, "bce", "tot2"); foot(t1.tbody, 6, L.check, "chk", "muted");
    foot(t2.tbody, 4, L.raw_total, "raw", "tot2", true); foot(t2.tbody, 4, L.sig_total, "sig", "tot1", true);
    const title2 = h("p", { class: "cew-sub" }, L.raw);
    const reset = () => rows.forEach((r, i) => { r.y = cfg.y[i]; r.yBtn.textContent = String(r.y); r.zIn.value = zText(cfg.z[i]); r.zIn.removeAttribute("aria-invalid"); });
    const setZ1 = (v) => { reset(); rows[0].zIn.value = zText(v); draw(); };
    w.stage.append(t1.el, title2, t2.el);
    w.controls.append(presets([{ label: L.reset, run: () => { reset(); draw(); } }, { label: L.z6, run: () => setZ1(6) }, { label: L.zm3, run: () => setZ1(-3) }]));

    function draw() {
      let sum = 0, n = 0, rawSum = 0, rawOk = true, chk = 0;
      rows.forEach((r) => {
        const z = parse(r.zIn.value), y = r.y;
        const p = sig(z);
        const a = y * Math.log(p), b = (1 - y) * Math.log(1 - p), s = a + b;
        [p, a, b, s].forEach((v, k) => setTxt(r.c[k], num(v), "#NUM!"));
        if (Number.isFinite(z)) n++;
        sum += s; chk += -(y * Math.log(p)) - (1 - y) * Math.log(1 - p);
        // block 2: the same logits straight into the formula
        const lz = lnOrNaN(z), l1z = lnOrNaN(1 - z);
        setTxt(r.d[0], Number.isFinite(z) ? zText(z) : null, "—");
        setTxt(r.d[1], num(lz), L.none);
        setTxt(r.d[2], num(l1z), L.none);
        const ok = Number.isFinite(lz) && Number.isFinite(l1z);
        setTxt(r.d[3], ok ? num(y * lz + (1 - y) * l1z) : null, L.err);
        r.d[4].textContent = !Number.isFinite(z) ? "" : ok ? L.by_chance : L.broke;
        r.d[4].classList.toggle("cew-err", Number.isFinite(z) && !ok);
        if (ok) rawSum += y * lz + (1 - y) * l1z; else rawOk = false;
      });
      setTxt(tot.sum, num(sum), "#NUM!");
      tot.n.textContent = String(n);
      const bce = -sum / n;
      setTxt(tot.bce, num(bce), "#NUM!");
      setTxt(tot.chk, num(chk / n), "#NUM!");
      const raw = rawOk ? -rawSum / n : NaN;
      setTxt(tot.raw, rawOk ? num(raw) : null, L.nan);
      tot.raw_m.textContent = rawOk ? (raw < 0 ? L.neg : L.by_chance) : L.nan_total;
      tot.raw_m.classList.toggle("cew-err", !rawOk || raw < 0);
      setTxt(tot.sig, num(bce), "#NUM!");
      tot.sig_m.textContent = "";
    }
    draw();
  });

  // ---------------------------------------------------------------- Categorical CE sheet, blocks 1 and 2
  FV.widget("cew-ce-sheet", (el, cfg) => {
    const L = cfg.L;
    const w = FV.shell(el, {});
    const K = cfg.z.length;
    let right = cfg.y.indexOf(1);
    const t1 = table([[L.k], [L.y, "in"], [L.z, "in"], [L.py, "tr"], [L.lnp], [L.ylnp, "fm"]], "ce");
    const t2 = table([[L.k], [L.z], [L.lnz], [L.ylnz], [L.what]], "raw");
    const rows = cfg.z.map((z0, k) => {
      const r = {};
      r.yBtn = h("button", { type: "button", class: "cew-y", "aria-label": L.correct + " " + (k + 1) });
      r.yBtn.addEventListener("click", () => { right = k; draw(); });
      r.zIn = input(z0, draw, L.z + " " + (k + 1));
      r.c = [cell("tr num"), cell("num"), cell("fm num")];
      t1.tbody.append(h("tr", {}, cell("idx", String(k + 1)), cell("in", r.yBtn), cell("in", r.zIn), ...r.c));
      r.d = [cell("num"), cell("num"), cell("num"), cell("what")];
      t2.tbody.append(h("tr", {}, cell("idx", String(k + 1)), ...r.d));
      return r;
    });
    const tot = {};
    const mk = (tb, span, label, key, cls, withNote) => {
      tot[key] = cell((cls || "") + " num");
      const tr = h("tr", { class: "cew-foot" }, h("td", { colspan: span, class: "lab" }, label), tot[key]);
      if (withNote) tr.append((tot[key + "_m"] = cell("what")));
      tb.append(tr);
    };
    mk(t1.tbody, 3, L.sump, "sp", "tr"); t1.tbody.lastChild.append(h("td", { colspan: 2 }));
    mk(t1.tbody, 5, "Σ", "sum", "tot1"); mk(t1.tbody, 5, L.ce, "ce", "tot2"); mk(t1.tbody, 5, L.ce_check, "chk", "muted");
    mk(t2.tbody, 3, L.ce_raw_total, "raw", "tot2", true); mk(t2.tbody, 3, L.ce_total, "cet", "tot1", true);
    const reset = () => { right = cfg.y.indexOf(1); rows.forEach((r, k) => { r.zIn.value = zText(cfg.z[k]); r.zIn.removeAttribute("aria-invalid"); }); };
    const setZ = (v) => { reset(); rows[right].zIn.value = zText(v); draw(); };
    w.stage.append(t1.el, h("p", { class: "cew-sub" }, L.raw_ce), t2.el);
    w.controls.append(presets([{ label: L.reset, run: () => { reset(); draw(); } }, { label: L.z5, run: () => setZ(5) }, { label: L.zm2, run: () => setZ(-2) },
      { label: L.z100, run: () => setZ(100) }]));

    function draw() {
      const z = rows.map((r) => parse(r.zIn.value));
      const e = z.map(Math.exp), S = e.reduce((a, b) => a + b, 0);
      const p = e.map((v) => v / S);
      let sum = 0, rawOk = true, raw = 0;
      rows.forEach((r, k) => {
        const y = k === right ? 1 : 0;
        r.yBtn.textContent = String(y);
        r.yBtn.setAttribute("aria-pressed", y ? "true" : "false");
        const lp = Math.log(p[k]);
        setTxt(r.c[0], num(p[k]), "#NUM!");
        setTxt(r.c[1], num(lp), "#NUM!");
        setTxt(r.c[2], num(y * lp), "#NUM!");
        sum += y * lp;
        const lz = lnOrNaN(z[k]);
        setTxt(r.d[0], Number.isFinite(z[k]) ? zText(z[k]) : null, "—");
        setTxt(r.d[1], num(lz), L.none);
        setTxt(r.d[2], Number.isFinite(lz) ? num(y * lz) : null, L.err);
        r.d[3].textContent = !Number.isFinite(z[k]) ? "" : z[k] <= 0 ? L.nolog : z[k] > 1 ? L.neg : L.lucky;
        r.d[3].classList.toggle("cew-err", z[k] <= 0 || z[k] > 1);
        if (Number.isFinite(lz)) raw += y * lz; else rawOk = false;
      });
      setTxt(tot.sp, num(p.reduce((a, b) => a + b, 0)), "#NUM!");
      setTxt(tot.sum, num(sum), "#NUM!");
      setTxt(tot.ce, num(-sum), "#NUM!");
      setTxt(tot.chk, num(-Math.log(p[right])), "#NUM!");
      setTxt(tot.raw, rawOk ? num(-raw) : null, L.err);
      tot.raw_m.textContent = !rawOk ? L.nolog : -raw < 0 ? L.neg : "";
      tot.raw_m.classList.toggle("cew-err", !rawOk || -raw < 0);
      setTxt(tot.cet, num(-sum), "#NUM!");
      tot.cet_m.textContent = "";
    }
    draw();
  });

  // ---------------------------------------------------------------- zones of the logarithm (BCE: two branches, CE: one)
  FV.widget("cew-zones", (el, cfg) => {
    const L = cfg.L, ce = cfg.mode === "ce";
    const w = FV.shell(el, {});
    const X = [-0.6, 2.4], Y = [-1.6, 5];
    const p = new FV.Plot(w.stage, { x: X, y: Y, xLabel: L.x, yLabel: L.pen, aspect: 0.56 });
    let branch = 1, x = ce ? 0.3 : 0.8;
    const f1 = (v) => (v > 0 ? -Math.log(v) : NaN), f0 = (v) => (v < 1 ? -Math.log(1 - v) : NaN);
    const cur = (v) => (ce || branch === 1 ? f1(v) : f0(v));
    if (!ce) {
      const seg = FV.ui.seg({ label: L.branch, value: 1, options: [{ value: 1, label: L.y1 }, { value: 0, label: L.y0 }], onchange: (v) => { branch = v; place(); draw(); } });
      w.controls.append(seg.el);
    }
    const ro = FV.ui.readout(w.readout, [{ key: "x", label: "x =" }, { key: "v", label: L.pen + " =" }, { key: "z", label: "" }]);
    const clampY = (v) => FV.clamp(v, Y[0] + 0.05, Y[1] - 0.05);
    const hd = p.handle(x, clampY(cur(x)), { c: "red", onDrag: (nx) => { x = FV.clamp(nx, X[0] + 0.01, X[1] - 0.01); return [x, clampY(Number.isFinite(cur(x)) ? cur(x) : 0)]; }, onChange: () => draw() });
    function place() { hd.set(x, clampY(Number.isFinite(cur(x)) ? cur(x) : 0)); }
    function draw() {
      p.clear();
      const okTo = 1;
      p.rect(X[0], Y[0], 0, Y[1], { c: "red", opacity: 0.08 });
      p.rect(0, Y[0], okTo, Y[1], { c: "teal", opacity: 0.08 });
      p.rect(okTo, Y[0], X[1], Y[1], { c: "red", opacity: 0.08 });
      // zone names along the bottom: the curves and the axis label stay clear
      p.text(0.5, Y[0] + 0.25, L.prob, { anchor: "middle", c: "teal", clip: true });
      p.text(-0.3, Y[0] + 0.25, L.logit, { anchor: "middle", c: "red", clip: true });
      p.text(1.95, Y[0] + 0.25, L.logit, { anchor: "middle", c: "red", clip: true });
      p.hline(0, { c: "guide", dash: null, w: 1 });
      p.fn(f1, { c: "red", w: ce || branch === 1 ? 2.6 : 1.4, opacity: ce || branch === 1 ? 1 : 0.45, from: 0.002, to: X[1] });
      if (!ce) p.fn(f0, { c: "blue", w: branch === 0 ? 2.6 : 1.4, opacity: branch === 0 ? 1 : 0.45, from: X[0], to: 0.998 });
      if (!ce) p.legend([{ c: "red", label: L.y1 }, { c: "blue", label: L.y0 }]);
      else p.legend([{ c: "red", label: L.ce_branch }]);
      const v = cur(x);
      ro.set("x", FV.fmt(x, 2));
      ro.set("v", Number.isFinite(v) ? f3(v) : L.none);
      const inside = ce ? x > 0 && x <= 1 : x > 0 && x < 1;
      ro.set("z", inside ? L.prob : L.logit);
      hd.g.setAttribute("class", "fv-handle s-" + (ce || branch === 1 ? "red" : "blue") + (Number.isFinite(v) ? "" : " cew-off"));
      hd.g.querySelector(".knob").setAttribute("class", "knob fill-" + (ce || branch === 1 ? "red" : "blue"));
    }
    p.onresize = () => { place(); draw(); };
    place(); draw();
  });

  // ---------------------------------------------------------------- sigmoid squeezes the logit (BCE sheet, block 4)
  FV.widget("cew-sigmoid", (el, cfg) => {
    const L = cfg.L;
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-10, 10], y: [-0.05, 1.05], xLabel: L.z, yLabel: "σ(z)", aspect: 0.5 });
    const sl = FV.ui.slider({ label: L.z, min: -10, max: 10, step: 0.1, value: 2.2, fmt: (v) => FV.fmt(v, 1), oninput: draw, wide: true });
    w.controls.append(sl.el);
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.sz + " =" }, { key: "p", label: L.yh + " =", c: "blue" }, { key: "q", label: L.omy + " =" }]);
    function draw() {
      const z = sl.value, e = Math.exp(-z), y = sig(z);
      p.clear();
      p.hline(0.5, { c: "guide", dash: "4 4" });
      p.hline(0, { c: "guide", dash: null }); p.hline(1, { c: "guide", dash: null });
      p.fn((v) => 1 - sig(v), { c: "faint", w: 1.4, dash: "5 4" });
      p.fn(sig, { c: "blue", w: 2.6 });
      p.line(z, 0, z, y, { c: "guide", w: 1, dash: "3 3" });
      p.dot(z, y, { c: "blue" });
      p.legend([{ c: "blue", label: L.yh }, { c: "faint", label: L.omy, dash: true }]);
      ro.set("e", Math.abs(e) >= 1e4 || e < 1e-3 ? FV.num(e, 4) : f4(e));
      ro.set("p", f4(y));
      ro.set("q", f4(1 - y));
    }
    p.onresize = draw;
    draw();
  });

  // ---------------------------------------------------------------- practice with self-check (the Practice sheet)
  FV.widget("cew-train", (el, cfg) => {
    const L = cfg.L, tol = cfg.tol;
    el.textContent = "";
    el.classList.add("fv", "cew-train");
    const checks = [];
    function answerCell(key, label) {
      const inp = h("input", { type: "text", inputmode: "decimal", autocomplete: "off", spellcheck: "false", "aria-label": label });
      const mark = h("td", { class: "mark", "aria-live": "polite" });
      const run = () => {
        const s = inp.value.trim();
        if (!s) { mark.textContent = ""; mark.className = "mark"; inp.removeAttribute("aria-invalid"); return null; }
        const v = parse(s);
        if (Number.isNaN(v)) { mark.textContent = L.nan; mark.className = "mark bad"; inp.setAttribute("aria-invalid", "true"); return false; }
        const ok = Math.abs(v - key) < tol;
        mark.textContent = ok ? L.ok : L.bad; mark.className = "mark " + (ok ? "ok" : "bad");
        inp.setAttribute("aria-invalid", ok ? "false" : "true");
        return ok;
      };
      inp.addEventListener("input", () => { run(); score(); });
      checks.push({ run, inp });
      return [h("td", { class: "in" }, inp), mark];
    }
    const score = () => {
      const res = checks.map((c) => c.run());
      const done = res.filter((r) => r !== null).length;
      total.textContent = done ? L.score.replace("{k}", res.filter((r) => r === true).length).replace("{n}", checks.length) : "";
    };
    const blocks = [];
    cfg.tasks.forEach((t, ti) => {
      const title = h("p", { class: "cew-sub" }, FV.rich(L["t" + (ti + 1)]));
      let tb;
      if (t.kind === "softmax") {
        tb = table([["k"], ["z"], [FV.rich(L.ez), "in"], [""], [FV.rich(L.yh), "in"], [L.check]], "train");
        t.z.forEach((z, k) => tb.tbody.append(h("tr", {}, cell("idx", String(k + 1)), cell("num", FV.fmt(z, 0)), ...answerCell(t.exp[k], "e^z " + (k + 1)), ...answerCell(t.answers[k], "ŷ " + (k + 1)))));
        tb.tbody.append(h("tr", { class: "cew-foot" }, h("td", { colspan: 4, class: "lab" }, "CE ="), ...answerCell(t.total, "CE")));
      } else {
        const lab = t.kind === "bce" ? L.term : L.yln;
        tb = table([[t.kind === "bce" ? "i" : "k"], ["y"], ["ŷ"], [FV.rich(lab), "in"], [L.check]], "train");
        t.y.forEach((y, i) => tb.tbody.append(h("tr", {}, cell("idx", String(i + 1)), cell("num", String(y)), cell("num", FV.fmt(t.p[i], 1)), ...answerCell(t.answers[i], lab + " " + (i + 1)))));
        tb.tbody.append(h("tr", { class: "cew-foot" }, h("td", { colspan: 3, class: "lab" }, t.kind === "bce" ? "BCE =" : "CE ="), ...answerCell(t.total, t.kind.toUpperCase())));
      }
      blocks.push(title, tb.el);
    });
    const total = h("span", { class: "cew-score", "aria-live": "polite" });
    const clear = FV.ui.button({ label: L.reset, onclick: () => { checks.forEach((c) => { c.inp.value = ""; }); score(); } });
    el.append(...blocks, h("div", { class: "cew-train-foot" }, clear.el, total));
  });
})();
