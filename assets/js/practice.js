/* Практикум «MAE и MSE на простых примерах»: раскрыть/свернуть разборы и калькулятор.
   Калькулятор расписывает решение теми же шагами, что и 20 примеров страницы, и по тем же
   правилам (tools/content_mae_mse.py): арифметика точная — числа хранятся целыми (BigInt)
   в десятичном масштабе; частное пишется точно, если это конечная дробь (до 6 знаков),
   иначе «≈» и 2 знака (4 знака, если |x| < 0,1). Ввод пользователя в HTML не вставляется:
   разбор строится из уже разобранных чисел, сообщения об ошибках — через textContent. */
(function () {
  "use strict";
  const main = document.querySelector("main.practice");
  if (!main) return;

  // ----- раскрыть / свернуть все разборы
  main.querySelectorAll("[data-ex-expand]").forEach((b) => b.addEventListener("click", () => {
    const open = b.getAttribute("data-ex-expand") === "1";
    main.querySelectorAll("details.ex-sol").forEach((d) => { d.open = open; });
  }));
  // ссылка на #ex-7 открывает разбор примера
  const follow = () => {
    const el = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (el && el.matches(".ex")) { const d = el.querySelector("details"); if (d) d.open = true; }
  };
  window.addEventListener("hashchange", follow);
  follow();

  // ----- калькулятор
  const box = main.querySelector(".calc");
  if (!box) return;
  const lang = box.dataset.lang;
  const L = JSON.parse(box.dataset.i18n);
  const inY = box.querySelector("#calc-y"), inP = box.querySelector("#calc-p");
  const out = box.querySelector(".calc-out"), err = box.querySelector(".calc-err");
  const MAX_N = 10, MAX_DEC = 4;

  /** Разбор строки в числа {v: BigInt, d: число знаков после запятой} или ошибка. */
  function parse(text) {
    let tokens = text.trim().split(lang === "en" ? /[;,\s]+/ : /[;\s]+/).filter(Boolean);
    tokens = tokens.map((t) => t.replace(/^,+|,+$/g, "").replace(/−/g, "-")).filter(Boolean);
    const nums = [];
    for (const t of tokens) {
      const m = /^(-?)(\d+)(?:[.,](\d+))?$/.exec(t);
      if (!m || (m[3] || "").length > MAX_DEC) return { error: L.err_num.replace("{t}", t) };
      const d = (m[3] || "").length;
      nums.push({ v: BigInt(m[1] + m[2] + (m[3] || "")), d });
    }
    return { nums };
  }

  const pow10 = (k) => 10n ** BigInt(k);
  const absB = (x) => (x < 0n ? -x : x);

  /** Десятичная строка дроби num / den (как exact_decimal / rounded в Python). */
  function decimal(num, den) {
    if (den < 0n) { num = -num; den = -den; }
    for (let d = 0; d <= 6; d++) {
      const v = num * pow10(d);
      if (v % den === 0n) return { exact: true, s: place(v / den, d) };
    }
    const digits = absB(num) * 10n >= den ? 2 : 4; // |x| ≥ 0,1 → 2 знака
    const q = absB(num) * pow10(digits);
    let n = q / den;
    if ((q % den) * 2n >= den) n += 1n;
    return { exact: false, s: (num < 0n ? "-" : "") + place(n, digits) };
  }
  function place(intVal, d) {
    const neg = intVal < 0n;
    let s = absB(intVal).toString();
    if (d > 0) { s = s.padStart(d + 1, "0"); s = s.slice(0, -d) + "." + s.slice(-d); }
    return (neg ? "-" : "") + s;
  }
  /** Число для TeX: в ru/uz — {,}. */
  const tx = (s) => (lang === "en" ? s : s.replace(".", "{,}"));
  /** Число для текста таблицы: в ru/uz — запятая, минус — «−». */
  const ht = (s) => (lang === "en" ? s : s.replace(".", ",")).replace(/^-/, "−");
  const fx = (v, scale) => decimal(v, pow10(scale)).s; // точное значение v / 10^scale
  const paren = (s) => (s.startsWith("-") ? "(" + tx(s) + ")" : tx(s));

  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function stepP(n, html) { // html — только из наших строк перевода (без ввода пользователя)
    const p = el("p", "ex-step");
    p.appendChild(el("b", null, n + ". "));
    p.appendChild(document.createTextNode(html));
    return p;
  }
  const eqd = (src) => el("div", "eqd", "$$" + src + "$$");

  function compute() {
    err.hidden = true;
    out.textContent = "";
    const a = parse(inY.value), b = parse(inP.value);
    const fail = (msg) => { err.textContent = msg.replace(/\$\\hat y\$/g, "ŷ").replace(/\$y\$/g, "y"); err.hidden = false; };
    if (a.error) return fail(a.error);
    if (b.error) return fail(b.error);
    if (!a.nums.length || !b.nums.length) return fail(L.err_empty);
    if (a.nums.length !== b.nums.length) return fail(L.err_count.replace("{a}", a.nums.length).replace("{b}", b.nums.length));
    if (a.nums.length > MAX_N) return fail(L.err_many.replace("{m}", MAX_N));

    const n = a.nums.length;
    const D = Math.max(...a.nums.map((x) => x.d), ...b.nums.map((x) => x.d));
    const up = (x) => x.v * pow10(D - x.d); // привести к общему масштабу D
    const y = a.nums.map(up), p = b.nums.map(up);
    const e = y.map((v, i) => v - p[i]);
    const ab = e.map(absB), sq = e.map((v) => v * v); // масштаб D и 2D
    const sumAb = ab.reduce((s, v) => s + v, 0n), sumSq = sq.reduce((s, v) => s + v, 0n);
    const N = BigInt(n);
    const mae = decimal(sumAb, N * pow10(D)), mse = decimal(sumSq, N * pow10(2 * D));
    const rel = (r) => (r.exact ? "=" : "\\approx");
    const st = (k) => L[k].replace("{n}", n);

    const absLines = [], sqLines = [];
    for (let i = 0; i < n; i++) {
      const diff = tx(fx(y[i], D)) + "-" + paren(fx(p[i], D));
      const k = "_{" + (i + 1) + "}";
      absLines.push(`\\lvert e${k}\\rvert &= \\lvert ${diff}\\rvert = \\lvert ${tx(fx(e[i], D))}\\rvert = ${tx(fx(ab[i], D))}`);
      sqLines.push(`e${k}^2 &= (${diff})^2 = ${paren(fx(e[i], D))}^2 = ${tx(fx(sq[i], 2 * D))}`);
    }
    const sumLine = (vals, scale, total) => vals.map((v) => tx(fx(v, scale))).join(" + ") + (n > 1 ? " = " + tx(fx(total, scale)) : "");
    const meanLine = (name, total, scale, r) => n === 1
      ? `\\mathrm{${name}} = \\frac{1}{1}\\cdot ${tx(fx(total, scale))} = ${tx(r.s)}`
      : `\\mathrm{${name}} = \\frac{1}{${n}}\\cdot ${tx(fx(total, scale))} = \\frac{${tx(fx(total, scale))}}{${n}} ${rel(r)} ${tx(r.s)}`;
    const aligned = (lines) => "\\begin{aligned}" + lines.join("\\\\") + "\\end{aligned}";

    const frag = document.createDocumentFragment();
    const push = (node) => frag.appendChild(node);
    push(stepP(1, st("step1"))); push(eqd(aligned(absLines)));
    push(stepP(2, st("step2"))); push(eqd(`\\sum_{i=1}^{${n}}\\lvert e_i\\rvert = ` + sumLine(ab, D, sumAb)));
    push(stepP(3, st("step3"))); push(eqd(meanLine("MAE", sumAb, D, mae)));
    push(stepP(4, st("step4"))); push(eqd(aligned(sqLines)));
    push(stepP(5, st("step5"))); push(eqd(`\\sum_{i=1}^{${n}}e_i^2 = ` + sumLine(sq, 2 * D, sumSq)));
    push(stepP(6, st("step6"))); push(eqd(meanLine("MSE", sumSq, 2 * D, mse)));

    // таблица
    const wrap = el("div", "table-wrap"), table = el("table", "data ex-table");
    const thead = el("thead"), hr = el("tr");
    L.table_h.forEach((h) => { const th = el("th", "num", h); hr.appendChild(th); });
    thead.appendChild(hr); table.appendChild(thead);
    const tb = el("tbody");
    for (let i = 0; i < n; i++) {
      const tr = el("tr");
      [String(i + 1), fx(y[i], D), fx(p[i], D), fx(e[i], D), fx(ab[i], D), fx(sq[i], 2 * D)].forEach((v, j) => tr.appendChild(el("td", "num", j ? ht(v) : v)));
      tb.appendChild(tr);
    }
    const tot = (label, c1, c2) => {
      const tr = el("tr", "tot"); const td = el("td", null, label); td.colSpan = 4; tr.appendChild(td);
      tr.appendChild(el("td", "num", c1)); tr.appendChild(el("td", "num", c2)); tb.appendChild(tr);
    };
    tot(L.sum, ht(fx(sumAb, D)), ht(fx(sumSq, 2 * D)));
    tot(L.mean + " (÷ " + n + ")", (mae.exact ? "" : "≈ ") + ht(mae.s), (mse.exact ? "" : "≈ ") + ht(mse.s));
    table.appendChild(tb); wrap.appendChild(table); push(wrap);

    const ans = el("p", "ex-answer");
    ans.appendChild(el("b", null, L.answer + ": "));
    ans.appendChild(document.createTextNode(`$\\mathrm{MAE} ${rel(mae)} ${tx(mae.s)}$,  $\\mathrm{MSE} ${rel(mse)} ${tx(mse.s)}$`));
    push(ans);
    out.appendChild(frag);
    if (window.renderMathInElement) {
      try {
        window.renderMathInElement(out, { delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }], throwOnError: false });
      } catch (e2) { /* без KaTeX остаётся читаемый TeX */ }
    }
  }

  box.querySelector("#calc-go").addEventListener("click", compute);
  [inY, inP].forEach((i) => i.addEventListener("keydown", (ev) => { if (ev.key === "Enter") { ev.preventDefault(); compute(); } }));
  box.querySelectorAll(".chip[data-y]").forEach((c) => c.addEventListener("click", () => {
    inY.value = c.dataset.y; inP.value = c.dataset.p; compute();
  }));
  // первый расчёт — когда KaTeX уже загружен (скрипты с defer идут по порядку, но auto-render может опоздать)
  if (document.readyState === "complete") compute(); else window.addEventListener("load", compute);
})();
