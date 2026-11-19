/* Animated figures of the section "The derivative in motion" (article "The derivative, partial derivatives and the gradient").
   Built on FV (assets/js/viz.js), loaded after assets/js/deriv.js.
   dm-race   — a walker and a car: the same 5 minutes, different distances; speed = slope of the position graph;
   dm-gauge  — average speed over [t, t + Δt] turns into the speedometer reading as Δt → 0;
   dm-tank   — water poured at a constant rate: the level rises faster where the vessel is narrow, dh/dt = Q / A(h);
   dm-zoom   — under a microscope a smooth curve becomes its tangent line; a kink never does;
   dm-build  — the graph of f′ drawn live from the slopes of the tangent;
   dm-ball   — a ball thrown up: height, velocity = h′, acceleration = h″;
   dm-gears  — gears: the ratios multiply — the chain rule. */
(function () {
  "use strict";
  if (typeof FV === "undefined" || !FV.widget) return;

  const L = {
    ru: {
      calc: "Формулы и расчёт", cdef: "По определению", cavg: "Средние скорости", cinc: "Приращение пути", cavg1: "Средняя скорость на отрезке", cinst: "Мгновенная скорость (производная)", cgap: "Разница", cvol: "Объём воды", carea: "Площадь зеркала воды", crate: "Скорость подъёма", csmall: "За малое время", cpoint: "В точке", ctan: "Касательная", cdev: "Отклонение от касательной", cratio: "Доля от ширины окна", ckink: "Излом в нуле", cval: "Значение", cder: "Производная", csign: "Знак", up: "растёт", down: "убывает", flatw: "касательная горизонтальна", ch: "Высота", cv: "Скорость", ca: "Ускорение (вторая производная)", cturn: "Обороты", cchain: "Цепное правило", cm: "см", sec: "с", devh: "отклонение от горизонтали / окно", left: "слева", right: "справа",
      play: "Пуск", pause: "Пауза", restart: "Сначала", time: "Время $t$, мин", work: "работа", home: "дом",
      walker: "пешеход", car: "машина", dist: "путь", speed: "скорость", avg: "средняя", mpm: "м/мин", kmh: "км/ч", m: "м",
      sAxis: "путь s, м", tAxis: "t, мин",
      raceNote: (t, s1, s2, v2, k2) => `$t = ${t}$ мин. Пешеход прошёл $${s1}$ м, его скорость всё время $80$ м/мин — его график — прямая, наклон везде одинаков. Машина проехала $${s2}$ м, её скорость сейчас $${v2}$ м/мин ($${k2}$ км/ч) — это наклон касательной к её графику. Оба доберутся до дома за $5$ минут, но средние скорости разные: $400 \\div 5 = 80$ и $3000 \\div 5 = 600$ м/мин.`,
      t0: "Момент $t_0$, мин", dt: "Отрезок $\\Delta t$, мин", shrink: "Δt → 0", avgSpeed: "средняя $\\Delta s / \\Delta t$", instSpeed: "спидометр $s'(t_0)$",
      gaugeNote: (dt, a, v) => `На отрезке $\\Delta t = ${dt}$ мин средняя скорость $\\frac{\\Delta s}{\\Delta t} = ${a}$ м/мин (оранжевая стрелка, наклон секущей). Спидометр показывает $${v}$ м/мин (синяя стрелка, наклон касательной). Уменьшайте $\\Delta t$ — стрелки сольются: это и есть производная.`,
      shape: "Сосуд", cyl: "цилиндр", cone: "воронка", vase: "ваза", level: "уровень $h$, см", rate: "$dh/dt$, см/с", area: "площадь сечения $A(h)$, см²", hAxis: "h, см", tsAxis: "t, с",
      tankNote: (h, a, r) => `Вода льётся с постоянным расходом $Q$. Уровень $h = ${h}$ см, площадь зеркала воды $A = ${a}$ см², уровень растёт со скоростью $\\frac{dh}{dt} = \\frac{Q}{A} = ${r}$ см/с. Где сосуд узкий — вода поднимается быстро и график круче; где широкий — медленно.`,
      fn: "Функция", pt: "Точка $x_0$", zoom: "Увеличение", win: "ширина окна", dev: "отклонение от касательной / окно",
      zoomNote: (z, d) => `Увеличение $\\times${z}$: в окне кривая отходит от касательной не больше чем на $${d}$ ширины окна. Чем сильнее увеличение, тем прямее кривая — вблизи точки гладкая функция неотличима от прямой с наклоном $f'(x_0)$.`,
      kinkNote: (z) => `Увеличение $\\times${z}$, а излом остаётся изломом: слева наклон $-1$, справа $+1$. Сколько ни увеличивай, $|x|$ в нуле не становится прямой — поэтому производной там нет.`,
      x: "Точка $x$", fGraph: "График $f(x)$ и касательная", dGraph: "График $f'(x)$ — наклоны касательной", slope: "наклон $f'(x)$", zeros: "касательная горизонтальна",
      buildNote: (x, d) => `В точке $x = ${x}$ наклон касательной $f'(x) = ${d}$ — эта точка нарисована на нижнем графике. Где $f$ растёт, $f' > 0$; где убывает, $f' < 0$; на вершинах и во впадинах $f' = 0$.`,
      hgt: "высота $h$, м", vel: "скорость $v = h'$, м/с", acc: "ускорение $a = h''$, м/с²", tsec: "t, с",
      ballNote: (t, h, v) => `$t = ${t}$ с: высота $h = ${h}$ м, скорость $v = h'(t) = 20 - 10t = ${v}$ м/с (стрелка). Скорость — наклон графика высоты, ускорение $a = v'(t) = h''(t) = -10$ м/с² — наклон графика скорости. В верхней точке ($t = 2$ с) касательная горизонтальна: $v = 0$.`,
      k1: "$\\frac{du}{dx}$ — передача первой пары", k2: "$\\frac{dy}{du}$ — передача второй пары", turnsX: "обороты $x$", turnsU: "обороты $u$", turnsY: "обороты $y$",
      gearsNote: (a, b, c) => `За один оборот первой шестерни ($x$) число оборотов второй ($u$) — $${a}$, третьей ($y$) — $${a} \\cdot ${b} = ${c}$. Передаточные числа перемножаются: $\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}$. Это и есть цепное правило; маленькая шестерня крутится быстрее большой.`,
    },
    en: {
      calc: "Formulas and calculation", cdef: "From the definition", cavg: "Average speeds", cinc: "Increment of distance", cavg1: "Average speed over the interval", cinst: "Instantaneous speed (the derivative)", cgap: "Difference", cvol: "Water volume", carea: "Water surface area", crate: "Rate of rise", csmall: "Over a short time", cpoint: "At the point", ctan: "Tangent", cdev: "Deviation from the tangent", cratio: "Share of the window width", ckink: "The kink at zero", cval: "Value", cder: "Derivative", csign: "Sign", up: "increases", down: "decreases", flatw: "horizontal tangent", ch: "Height", cv: "Velocity", ca: "Acceleration (second derivative)", cturn: "Turns", cchain: "The chain rule", cm: "cm", sec: "s", devh: "deviation from the horizontal / window", left: "left", right: "right",
      play: "Play", pause: "Pause", restart: "Restart", time: "Time $t$, min", work: "work", home: "home",
      walker: "walker", car: "car", dist: "distance", speed: "speed", avg: "average", mpm: "m/min", kmh: "km/h", m: "m",
      sAxis: "distance s, m", tAxis: "t, min",
      raceNote: (t, s1, s2, v2, k2) => `$t = ${t}$ min. The walker has covered $${s1}$ m; their speed is always $80$ m/min — their graph is a straight line with the same slope everywhere. The car has covered $${s2}$ m; its speed right now is $${v2}$ m/min ($${k2}$ km/h) — the slope of the tangent to its graph. Both arrive in $5$ minutes, but the average speeds differ: $400 \\div 5 = 80$ and $3000 \\div 5 = 600$ m/min.`,
      t0: "Moment $t_0$, min", dt: "Interval $\\Delta t$, min", shrink: "Δt → 0", avgSpeed: "average $\\Delta s / \\Delta t$", instSpeed: "speedometer $s'(t_0)$",
      gaugeNote: (dt, a, v) => `Over the interval $\\Delta t = ${dt}$ min the average speed is $\\frac{\\Delta s}{\\Delta t} = ${a}$ m/min (the orange needle, the slope of the secant). The speedometer shows $${v}$ m/min (the blue needle, the slope of the tangent). Shrink $\\Delta t$ — the needles merge: that is the derivative.`,
      shape: "Vessel", cyl: "cylinder", cone: "funnel", vase: "vase", level: "level $h$, cm", rate: "$dh/dt$, cm/s", area: "cross-section $A(h)$, cm²", hAxis: "h, cm", tsAxis: "t, s",
      tankNote: (h, a, r) => `Water is poured at a constant rate $Q$. The level is $h = ${h}$ cm, the water surface area is $A = ${a}$ cm², and the level rises at $\\frac{dh}{dt} = \\frac{Q}{A} = ${r}$ cm/s. Where the vessel is narrow the water rises fast and the graph is steep; where it is wide, slowly.`,
      fn: "Function", pt: "Point $x_0$", zoom: "Magnification", win: "window width", dev: "deviation from the tangent / window",
      zoomNote: (z, d) => `Magnification $\\times${z}$: inside the window the curve departs from the tangent by at most $${d}$ of the window width. The stronger the magnification, the straighter the curve — near the point a smooth function is indistinguishable from a line with slope $f'(x_0)$.`,
      kinkNote: (z) => `Magnification $\\times${z}$, and the kink is still a kink: slope $-1$ on the left, $+1$ on the right. However much you zoom in, $|x|$ at zero never becomes a line — that is why there is no derivative there.`,
      x: "Point $x$", fGraph: "The graph of $f(x)$ and the tangent", dGraph: "The graph of $f'(x)$ — slopes of the tangent", slope: "slope $f'(x)$", zeros: "horizontal tangent",
      buildNote: (x, d) => `At $x = ${x}$ the slope of the tangent is $f'(x) = ${d}$ — this point is drawn on the lower graph. Where $f$ increases, $f' > 0$; where it decreases, $f' < 0$; at peaks and troughs $f' = 0$.`,
      hgt: "height $h$, m", vel: "velocity $v = h'$, m/s", acc: "acceleration $a = h''$, m/s²", tsec: "t, s",
      ballNote: (t, h, v) => `$t = ${t}$ s: height $h = ${h}$ m, velocity $v = h'(t) = 20 - 10t = ${v}$ m/s (the arrow). Velocity is the slope of the height graph; acceleration $a = v'(t) = h''(t) = -10$ m/s² is the slope of the velocity graph. At the top ($t = 2$ s) the tangent is horizontal: $v = 0$.`,
      k1: "$\\frac{du}{dx}$ — ratio of the first pair", k2: "$\\frac{dy}{du}$ — ratio of the second pair", turnsX: "turns of $x$", turnsU: "turns of $u$", turnsY: "turns of $y$",
      gearsNote: (a, b, c) => `Per turn of the first gear ($x$), the number of turns of the second ($u$) is $${a}$, of the third ($y$) $${a} \\cdot ${b} = ${c}$. The gear ratios multiply: $\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}$. That is the chain rule; a small gear spins faster than a big one.`,
    },
    uz: {
      calc: "Formulalar va hisob", cdef: "Ta’rif bo‘yicha", cavg: "O‘rtacha tezliklar", cinc: "Yo‘l orttirmasi", cavg1: "Oraliqdagi o‘rtacha tezlik", cinst: "Oniy tezlik (hosila)", cgap: "Farq", cvol: "Suv hajmi", carea: "Suv sirtining yuzi", crate: "Ko‘tarilish tezligi", csmall: "Qisqa vaqt ichida", cpoint: "Nuqtada", ctan: "Urinma", cdev: "Urinmadan og‘ish", cratio: "Oyna kengligidagi ulushi", ckink: "Noldagi sinish", cval: "Qiymat", cder: "Hosila", csign: "Ishora", up: "o‘sadi", down: "kamayadi", flatw: "urinma gorizontal", ch: "Balandlik", cv: "Tezlik", ca: "Tezlanish (ikkinchi hosila)", cturn: "Aylanishlar", cchain: "Zanjir qoidasi", cm: "sm", sec: "s", devh: "gorizontaldan og‘ish / oyna", left: "chapda", right: "o‘ngda",
      play: "Boshlash", pause: "Pauza", restart: "Boshidan", time: "Vaqt $t$, daq", work: "ish", home: "uy",
      walker: "piyoda", car: "mashina", dist: "yo‘l", speed: "tezlik", avg: "o‘rtacha", mpm: "m/daq", kmh: "km/soat", m: "m",
      sAxis: "yo‘l s, m", tAxis: "t, daq",
      raceNote: (t, s1, s2, v2, k2) => `$t = ${t}$ daq. Piyoda $${s1}$ m yurdi, uning tezligi doim $80$ m/daq — grafigi to‘g‘ri chiziq, qiyaligi hamma joyda bir xil. Mashina $${s2}$ m yurdi, hozirgi tezligi $${v2}$ m/daq ($${k2}$ km/soat) — bu uning grafigiga urinmaning qiyaligi. Ikkalasi ham $5$ daqiqada yetib keladi, lekin o‘rtacha tezliklar har xil: $400 \\div 5 = 80$ va $3000 \\div 5 = 600$ m/daq.`,
      t0: "$t_0$ payt, daq", dt: "$\\Delta t$ oraliq, daq", shrink: "Δt → 0", avgSpeed: "o‘rtacha $\\Delta s / \\Delta t$", instSpeed: "spidometr $s'(t_0)$",
      gaugeNote: (dt, a, v) => `$\\Delta t = ${dt}$ daq oraliqda o‘rtacha tezlik $\\frac{\\Delta s}{\\Delta t} = ${a}$ m/daq (to‘q sariq strelka, kesuvchining qiyaligi). Spidometr $${v}$ m/daq ni ko‘rsatadi (ko‘k strelka, urinmaning qiyaligi). $\\Delta t$ ni kichraytiring — strelkalar ustma-ust tushadi: bu hosilaning o‘zi.`,
      shape: "Idish", cyl: "silindr", cone: "voronka", vase: "vaza", level: "sath $h$, sm", rate: "$dh/dt$, sm/s", area: "kesim yuzi $A(h)$, sm²", hAxis: "h, sm", tsAxis: "t, s",
      tankNote: (h, a, r) => `Suv o‘zgarmas $Q$ sarf bilan quyiladi. Sath $h = ${h}$ sm, suv sirtining yuzi $A = ${a}$ sm², sath $\\frac{dh}{dt} = \\frac{Q}{A} = ${r}$ sm/s tezlik bilan ko‘tariladi. Idishning tor joyida suv tez ko‘tariladi va grafik tikroq; keng joyida — sekin.`,
      fn: "Funksiya", pt: "$x_0$ nuqta", zoom: "Kattalashtirish", win: "oyna kengligi", dev: "urinmadan og‘ish / oyna",
      zoomNote: (z, d) => `Kattalashtirish $\\times${z}$: oynada egri chiziq urinmadan oyna kengligining ko‘pi bilan $${d}$ qismiga uzoqlashadi. Kattalashtirish qancha kuchli bo‘lsa, egri chiziq shuncha to‘g‘rilanadi — nuqta yaqinida silliq funksiya $f'(x_0)$ qiyalikli to‘g‘ri chiziqdan farq qilmaydi.`,
      kinkNote: (z) => `Kattalashtirish $\\times${z}$, sinish esa sinishligicha qoladi: chapda qiyalik $-1$, o‘ngda $+1$. Qancha kattalashtirmang, $|x|$ nolda to‘g‘ri chiziqqa aylanmaydi — shuning uchun u yerda hosila yo‘q.`,
      x: "$x$ nuqta", fGraph: "$f(x)$ grafigi va urinma", dGraph: "$f'(x)$ grafigi — urinma qiyaliklari", slope: "qiyalik $f'(x)$", zeros: "urinma gorizontal",
      buildNote: (x, d) => `$x = ${x}$ nuqtada urinmaning qiyaligi $f'(x) = ${d}$ — bu nuqta pastki grafikda chizilgan. $f$ o‘sadigan joyda $f' > 0$; kamayadigan joyda $f' < 0$; cho‘qqi va chuqurliklarda $f' = 0$.`,
      hgt: "balandlik $h$, m", vel: "tezlik $v = h'$, m/s", acc: "tezlanish $a = h''$, m/s²", tsec: "t, s",
      ballNote: (t, h, v) => `$t = ${t}$ s: balandlik $h = ${h}$ m, tezlik $v = h'(t) = 20 - 10t = ${v}$ m/s (strelka). Tezlik — balandlik grafigining qiyaligi, tezlanish $a = v'(t) = h''(t) = -10$ m/s² — tezlik grafigining qiyaligi. Eng yuqori nuqtada ($t = 2$ s) urinma gorizontal: $v = 0$.`,
      k1: "$\\frac{du}{dx}$ — birinchi juft uzatmasi", k2: "$\\frac{dy}{du}$ — ikkinchi juft uzatmasi", turnsX: "$x$ aylanishlari", turnsU: "$u$ aylanishlari", turnsY: "$y$ aylanishlari",
      gearsNote: (a, b, c) => `Birinchi tishli g‘ildirak ($x$) bir marta aylanadi — ikkinchisi ($u$) $${a}$ marta, uchinchisi ($y$) $${a} \\cdot ${b} = ${c}$ marta. Uzatish sonlari ko‘paytiriladi: $\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}$. Bu zanjir qoidasi; kichik g‘ildirak kattasidan tezroq aylanadi.`,
    },
  }[FV.lang] || {};

  const S = FV.svg;
  const n = (v, d = 3) => FV.num(Math.abs(v) < 1e-9 ? 0 : v, d);
  // a number for TeX: a·10ⁿ becomes a\cdot 10^{n}, every decimal comma becomes {,}
  const SUPD = { "⁻": "-", "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9" };
  const tn = (v, d = 3) => {
    let s = n(v, d);
    const m = s.match(/^(.*)·10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)$/);
    if (m) s = m[1] + "\\cdot 10^{" + m[2].replace(/./g, (c) => SUPD[c]) + "}";
    return s.replace(/−/g, "-").replace(/,/g, "{,}");
  };
  const reduced = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Run fn at most every ~120 ms, always with the latest argument (the last call is never lost).
  function throttled(fn, ms = 120) {
    let last = 0, timer = 0, pending;
    return (arg) => {
      pending = arg;
      const now = performance.now();
      if (now - last >= ms) { last = now; clearTimeout(timer); fn(arg); }
      else { clearTimeout(timer); timer = setTimeout(() => { last = performance.now(); fn(pending); }, ms); }
    };
  }
  // The note under a figure follows the motion; screen readers get one short announcement after the user stops changing
  // things (never on load or on resize).
  function noter(ui) {
    ui.note.setAttribute("aria-live", "off");
    const live = FV.h("div", { class: "sr-only", "aria-live": "polite" });
    ui.root.append(live);
    let t = 0, last = "", armed = false;
    const show = throttled((s) => { ui.note.textContent = ""; ui.note.append(FV.rich(s, "span")); });
    const api = (s) => {
      if (s === last) return;
      last = s; show(s);
      if (!armed) return;
      clearTimeout(t); t = setTimeout(() => { live.textContent = FV.plain(last); }, 900);
    };
    // the first user interaction inside the widget arms the announcements
    ["pointerdown", "keydown", "input"].forEach((e) => ui.root.addEventListener(e, () => { armed = true; }, { capture: true }));
    return api;
  }
  // Clocks: requestAnimationFrame; every running clock stops when the tab is hidden or its widget leaves the screen.
  const running = new Set();
  document.addEventListener("visibilitychange", () => { if (document.hidden) running.forEach((c) => c.stop()); });
  function clock(o) {
    let raf = 0, last = 0;
    const btn = FV.ui.button({ label: "", primary: true, onclick: () => (raf ? api.stop() : api.start()) });
    const label = (on) => { btn.el.textContent = ""; btn.el.append(FV.h("span", { "aria-hidden": "true", text: on ? "❚❚ " : "▶ " }), FV.rich(on ? L.pause : o.label || L.play)); };
    label(false);
    function frame(ts) {
      const dt = last ? Math.min(0.1, (ts - last) / 1000) : 0; last = ts;
      if (o.tick(dt) === false) { api.stop(); return; }
      raf = requestAnimationFrame(frame);
    }
    const api = {
      el: btn.el,
      start() {
        if (reduced()) { o.jump && o.jump(); return; }
        if (o.before) o.before();
        last = 0; raf = requestAnimationFrame(frame); label(true); running.add(api);
      },
      stop() { cancelAnimationFrame(raf); raf = 0; label(false); running.delete(api); },
      get running() { return !!raf; },
    };
    if (o.root && "IntersectionObserver" in window) new IntersectionObserver((es) => es.forEach((e) => { if (!e.isIntersecting && raf) api.stop(); })).observe(o.root);
    return api;
  }
  // A plain SVG scene with a fixed coordinate system that scales with the width; its text keeps a readable size
  // on every screen (--dm-fs is the font size in viewBox units that gives ~13 px on screen).
  function scene(parent, w, h, label) {
    const svg = S("svg", { class: "fv-svg dm-scene", viewBox: `0 0 ${w} ${h}`, role: "img", "aria-label": FV.plain(label || "") });
    parent.append(svg);
    svg._fit = () => { const vb = svg.viewBox.baseVal, cw = svg.clientWidth; if (cw) svg.style.setProperty("--dm-fs", ((13 * vb.width) / cw).toFixed(1) + "px"); };
    if ("ResizeObserver" in window) new ResizeObserver(() => svg._fit()).observe(svg);
    requestAnimationFrame(() => svg._fit());
    return svg;
  }
  const el = (tag, attrs, parent, text) => { const e = S(tag, attrs, parent); if (text != null) e.textContent = text; return e; };
  // The "formulas and calculation" panel: display formulas with the current numbers, recomputed with the figure.
  // Numbers carry the colour of their object in the figure (\htmlClass{t-…}), so the eye links the two.
  const KOPT = { displayMode: true, throwOnError: false, strict: false, trust: (c) => c.command === "\\htmlClass" };
  const kx = (src) => { try { return window.katex ? window.katex.renderToString(src, KOPT) : src; } catch (e) { return src; } };
  const C = (cls, v) => `\\htmlClass{t-${cls}}{${v}}`;
  const pm = (v, d = 4) => (v < 0 ? "- " : "+ ") + tn(Math.abs(v), d);
  const P0 = (s) => (s.startsWith("-") ? "(" + s + ")" : s); // a negative number substituted into a formula gets brackets
  const U = (u) => `\\ \\text{${u}}`;
  // Split TeX at top-level separators (outside braces).
  function splitTop(tex, seps) {
    const out = []; let depth = 0, cur = "";
    for (let i = 0; i < tex.length; i++) {
      const ch = tex[i];
      if (ch === "{") depth++; else if (ch === "}") depth--;
      const sep = depth === 0 && seps.find((x) => tex.startsWith(x, i));
      if (sep) { out.push(cur); cur = ""; i += sep.length - 1; } else cur += ch;
    }
    out.push(cur);
    return out;
  }
  // Long chains of equalities go on several lines: "a = b" then "= c = d" …; parallel formulas (",\qquad") each get a line.
  function wrap(tex, narrow) {
    if (tex.includes("\\begin{")) return tex;
    const lines = [];
    splitTop(tex, [",\\qquad ", ",\\quad "]).forEach((seg) => {
      // on a phone every step of the chain gets its own line
      const parts = splitTop(seg, [" = "]), per = narrow ? 1 : 2;
      if (parts.length <= (narrow ? 2 : 3) && !(narrow && parts.length === 2 && parts[0].length > 60)) { lines.push(parts.join(" = ")); return; }
      const head = narrow && parts[0].replace(/\\[a-z]+|[{}\s]/g, "").length > 10 ? 1 : 2; // a short left side stays with the first step
      lines.push(parts.slice(0, head).join(" = "));
      for (let i = head; i < parts.length; i += per) lines.push("= " + parts.slice(i, i + per).join(" = "));
    });
    return lines.length === 1 ? tex : "\\begin{aligned}" + lines.map((l) => "&" + l).join("\\\\[3pt] ") + "\\end{aligned}";
  }
  function calcPanel(ui) {
    const box = FV.h("div", { class: "dm-calc", role: "group", "aria-label": L.calc });
    box.append(FV.h("div", { class: "dm-calc-title", text: L.calc }));
    const body = FV.h("div", { class: "dm-calc-body" });
    box.append(body);
    ui.readout.after(box);
    let narrow = false, rowsLast = null, html = "";
    const render = throttled((rows) => {
      const next = rows.map(([lab, tex]) => `<div class="dm-calc-row"><div class="dm-calc-lab">${lab}</div><div class="dm-calc-eq">${kx(wrap(tex, narrow))}</div></div>`).join("");
      if (next !== html) { html = next; body.innerHTML = next; }
    });
    if ("ResizeObserver" in window) new ResizeObserver(() => { const nw = body.clientWidth > 0 && body.clientWidth < 460; if (nw !== narrow) { narrow = nw; html = ""; if (rowsLast) render(rowsLast); } }).observe(body);
    return (rows) => { const key = JSON.stringify(rows); if (key === rowsLast && html) return; rowsLast = rows; render(rows); };
  }

  // ---------- 1. a walker and a car: the same 5 minutes ----------
  FV.widget("dm-race", (root) => {
    const ui = FV.shell(root), note = noter(ui);
    const T = 5, D1 = 400, D2 = 3000;
    const s1 = (t) => (D1 * t) / T, v1 = () => D1 / T;
    const s2 = (t) => { const u = t / T; return D2 * (3 * u * u - 2 * u * u * u); }, v2 = (t) => { const u = t / T; return (D2 * (6 * u - 6 * u * u)) / T; };
    let t = 2;
    // the road: wide and flat on a desktop, narrower and taller on a phone (text stays readable)
    const road = scene(ui.stage, 720, 156, L.walker + ", " + L.car);
    let W = 720, Y1 = 42, Y2 = 102;
    const X = (s) => 40 + (s / D2) * (W - 80);
    const gR = el("g", {}, road), gM = el("g", {}, road);
    const walker = el("g", { class: "fill-teal s-teal" }, gM);
    el("circle", { cx: 0, cy: -16, r: 4 }, walker); el("path", { d: "M0 -12v10M0 -2l-5 9M0 -2l5 9M-5 -8h10", "stroke-width": 2.2, fill: "none", "stroke-linecap": "round" }, walker);
    const car = el("g", { class: "fill-orange" }, gM);
    el("rect", { x: -16, y: -14, width: 32, height: 10, rx: 3 }, car); el("rect", { x: -9, y: -21, width: 17, height: 8, rx: 3 }, car);
    el("circle", { cx: -9, cy: -3, r: 3.5, class: "dm-wheel" }, car); el("circle", { cx: 9, cy: -3, r: 3.5, class: "dm-wheel" }, car);
    const lab1 = el("text", { class: "fv-text dm-small t-teal", "text-anchor": "middle" }, gM), lab2 = el("text", { class: "fv-text dm-small t-orange", "text-anchor": "middle" }, gM);
    function roadLayout() {
      const narrow = (road.clientWidth || ui.stage.clientWidth || 720) < 600;
      W = narrow ? 380 : 720; Y1 = narrow ? 70 : 42; Y2 = narrow ? 170 : 102;
      const H = narrow ? 230 : 156;
      road.setAttribute("viewBox", `0 0 ${W} ${H}`);
      road.classList.toggle("dm-road-narrow", narrow); road._fit();
      gR.textContent = "";
      [Y1, Y2].forEach((y) => {
        el("line", { x1: X(0), x2: X(D2) + 10, y1: y, y2: y, class: "s-faint", "stroke-width": 1, "stroke-dasharray": "4 5" }, gR);
      });
      const house = (s, y) => { const x = X(s); el("path", { d: `M${x - 9} ${y - 2}h18v-12l-9-8l-9 8z`, class: "fill-faint dm-house" }, gR); el("text", { x, y: y + 20, "text-anchor": "middle", class: "fv-text dm-small" }, gR, L.home); };
      house(D1, Y1); house(D2, Y2);
      el("text", { x: X(0), y: H - 8, "text-anchor": "middle", class: "fv-text dm-small" }, gR, L.work);
      el("line", { x1: X(0), x2: X(0), y1: Y1 - 26, y2: Y2 + 14, class: "s-ink", "stroke-width": 2 }, gR);
    }
    const plot = new FV.Plot(ui.stage, { x: [0, 5], y: [0, 3200], aspect: 0.5, maxHeight: 340, xLabel: L.tAxis, yLabel: L.sAxis });
    const st = FV.ui.slider({ label: L.time, min: 0, max: 5, step: 0.01, value: t, oninput: (v) => { ck.stop(); t = v; draw(); } });
    const ck = clock({ root, before: () => { if (t >= T) t = 0; }, tick: (dt) => { t = Math.min(T, t + dt * 0.7); st.set(t); draw(); return t < T; }, jump: () => { t = t >= T ? 0 : Math.min(T, t + 1); st.set(t); draw(); } });
    ui.controls.append(st.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "s1", label: L.walker + ": " + L.dist, c: "teal" }, { key: "v1", label: L.walker + ": " + L.speed, c: "teal" }, { key: "s2", label: L.car + ": " + L.dist, c: "orange" }, { key: "v2", label: L.car + ": " + L.speed, c: "orange" }]);
    const calc = calcPanel(ui);
    function draw() {
      const a = s1(t), b = s2(t), va = v1(), vb = v2(t);
      walker.setAttribute("transform", `translate(${X(a)} ${Y1})`); car.setAttribute("transform", `translate(${X(b)} ${Y2})`);
      lab1.setAttribute("x", Math.max(W < 500 ? 110 : 90, X(a))); lab1.setAttribute("y", Y1 - 28); lab1.textContent = L.walker + " · " + n(va) + " " + L.mpm;
      lab2.setAttribute("x", FV.clamp(X(b), W < 500 ? 120 : 100, W - (W < 500 ? 120 : 100))); lab2.setAttribute("y", Y2 - 28); lab2.textContent = L.car + " · " + n(vb, 3) + " " + L.mpm;
      plot.clear();
      plot.fn(s1, { c: "teal", w: 2.4, from: 0, to: 5 }); plot.fn(s2, { c: "orange", w: 2.4, from: 0, to: 5 });
      plot.vline(t);
      const w = 0.7;
      plot.line(t - w, a - va * w, t + w, a + va * w, { c: "teal", w: 1.4, dash: true });
      plot.line(t - w, b - vb * w, t + w, b + vb * w, { c: "orange", w: 1.4, dash: true });
      plot.dot(t, a, { c: "teal" }); plot.dot(t, b, { c: "orange" });
      plot.legend([{ label: L.walker + ": $s = 80t$", c: "teal" }, { label: L.car, c: "orange" }]);
      ro.set("s1", n(a) + " " + L.m); ro.set("v1", n(va) + " " + L.mpm); ro.set("s2", n(b, 4) + " " + L.m); ro.set("v2", n(vb, 3) + " " + L.mpm);
      const u = t / T, hstep = t + 0.01 <= T ? 0.01 : -0.01, q = (s2(t + hstep) - b) / hstep;
      calc([
        [L.walker, `s_1(t) = 80t = 80\\cdot ${C("ink", tn(t, 3))} = ${C("teal", tn(a, 4))}${U(L.m)},\\qquad v_1 = s_1'(t) = ${C("teal", "80")}${U(L.mpm)}`],
        [L.car, `u = \\frac{t}{5} = ${tn(u, 4)},\\qquad s_2 = 3000\\,(3u^2 - 2u^3) = 3000\\,(3\\cdot ${tn(u, 4)}^2 - 2\\cdot ${tn(u, 4)}^3) = ${C("orange", tn(b, 5))}${U(L.m)}`],
        [L.cinst, `v_2 = s_2'(t) = 3600\\,(u - u^2) = 3600\\,(${tn(u, 4)} - ${tn(u, 4)}^2) = ${C("orange", tn(vb, 5))}${U(L.mpm)} = ${tn(vb * 0.06, 4)}${U(L.kmh)}`],
        [L.cdef + ", Δt = " + n(hstep, 2), `\\frac{s_2(t + \\Delta t) - s_2(t)}{\\Delta t} = \\frac{${tn(s2(t + hstep), 6)} - ${tn(b, 6)}}{${tn(hstep, 2)}} = ${C("blue", tn(q, 5))} \\approx v_2`],
        [L.cavg, `\\bar v_1 = \\frac{400}{5} = ${C("teal", "80")},\\qquad \\bar v_2 = \\frac{3000}{5} = ${C("orange", "600")}${U(L.mpm)}`],
      ]);
      note(L.raceNote(tn(t, 3), tn(a, 3), tn(b, 4), tn(vb, 3), tn(vb * 0.06, 3)));
    }
    plot.onresize = () => { roadLayout(); draw(); };
    roadLayout(); draw();
  });

  // ---------- 2. average speed → the speedometer ----------
  FV.widget("dm-gauge", (root) => {
    const ui = FV.shell(root, { cols: true }), note = noter(ui);
    const T = 5, D = 3000;
    // the same car as in animation 1: s = 3000(3u² − 2u³), u = t/5, s′ = 3600(u − u²)
    const s = (t) => { const u = t / T; return D * (3 * u * u - 2 * u * u * u); }, v = (t) => { const u = t / T; return 3600 * (u - u * u); };
    let t0 = 1.5, dt = 2;
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const plot = new FV.Plot(c1, { x: [0, 5], y: [-100, 3200], aspect: 0.75, maxHeight: 340, xLabel: L.tAxis, yLabel: L.sAxis });
    const g = scene(c2, 300, 230, L.instSpeed);
    const CX = 150, CY = 150, R = 110, VMAX = 1000, A0 = -210, A1 = 30; // degrees, clockwise from the x axis
    const ang = (val) => ((A0 + (A1 - A0) * FV.clamp(val / VMAX, 0, 1)) * Math.PI) / 180;
    const P = (a, r) => [CX + r * Math.cos(a), CY + r * Math.sin(a)];
    el("path", { d: `M${P(ang(0), R)[0]} ${P(ang(0), R)[1]} A${R} ${R} 0 1 1 ${P(ang(VMAX), R)[0]} ${P(ang(VMAX), R)[1]}`, fill: "none", class: "s-ink", "stroke-width": 3 }, g);
    for (let k = 0; k <= VMAX; k += 50) {
      const a = ang(k), big = k % 250 === 0, p = P(a, R), q = P(a, R - (big ? 14 : 7));
      el("line", { x1: p[0], y1: p[1], x2: q[0], y2: q[1], class: "s-ink", "stroke-width": big ? 2 : 1 }, g);
      if (big) { const r = P(a, R - 28); el("text", { x: r[0], y: r[1] + 4, "text-anchor": "middle", class: "fv-text dm-small" }, g, String(k)); }
    }
    el("text", { x: CX, y: CY + 52, "text-anchor": "middle", class: "fv-text dm-small" }, g, L.mpm);
    const nA = el("line", { x1: CX, y1: CY, class: "s-orange", "stroke-width": 4, "stroke-linecap": "round" }, g);
    const nV = el("line", { x1: CX, y1: CY, class: "s-blue", "stroke-width": 3, "stroke-linecap": "round" }, g);
    el("circle", { cx: CX, cy: CY, r: 7, class: "fill-ink" }, g);
    const st0 = FV.ui.slider({ label: L.t0, min: 0, max: 4.5, step: 0.01, value: t0, oninput: (x) => { ck.stop(); t0 = x; fix(); draw(); } });
    const sdt = FV.ui.slider({ label: L.dt, min: -2.3, max: Math.log10(2.5), step: 0.01, value: Math.log10(dt), map: (x) => Math.pow(10, x), unmap: Math.log10, fmt: (x) => n(x, 3), oninput: (x) => { ck.stop(); dt = x; draw(); } });
    const fix = () => { const m = Math.max(0.005, T - t0); sdt.input.max = Math.log10(Math.min(2.5, m)); dt = Math.min(dt, m); sdt.set(dt); };
    const ck = clock({ root, label: L.shrink, before: () => { if (dt < 0.01) { dt = Math.min(2, T - t0); } }, tick: (d) => { dt *= Math.pow(0.35, d); if (dt < 0.005) { dt = 0.005; sdt.set(dt); draw(); return false; } sdt.set(dt); draw(); return true; }, jump: () => { dt = dt <= 0.0051 ? Math.min(2, T - t0) : 0.005; sdt.set(dt); draw(); } });
    ui.controls.append(st0.el, sdt.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "a", label: L.avgSpeed, c: "orange" }, { key: "v", label: L.instSpeed, c: "blue" }]);
    const calc = calcPanel(ui);
    function needle(line, val, r) { const p = P(ang(val), r); line.setAttribute("x2", p[0]); line.setAttribute("y2", p[1]); }
    function draw() {
      const a = (s(t0 + dt) - s(t0)) / dt, vi = v(t0), y0 = s(t0);
      plot.clear();
      plot.fn(s, { c: "ink", w: 2.2, from: 0, to: 5 });
      plot.line(0, y0 - a * t0, 5, y0 + a * (5 - t0), { c: "orange", w: 1.8 });
      plot.line(0, y0 - vi * t0, 5, y0 + vi * (5 - t0), { c: "blue", w: 1.4, dash: true });
      plot.rect(t0, -100, t0 + dt, -40, { c: "orange", opacity: 0.8 });
      plot.dot(t0, y0, { c: "blue" }); plot.dot(t0 + dt, s(t0 + dt), { c: "orange" });
      plot.legend([{ label: "$s(t)$", c: "ink" }, { label: L.avgSpeed, c: "orange" }, { label: L.instSpeed, c: "blue", dash: true }]);
      needle(nA, a, R - 18); needle(nV, vi, R - 30);
      ro.set("a", n(a, 4) + " " + L.mpm); ro.set("v", n(vi, 4) + " " + L.mpm);
      const s1v = s(t0 + dt), ds = s1v - y0, u0 = t0 / T;
      calc([
        ["s(t)", `s(t) = 3000\\,(3u^2 - 2u^3),\\quad u = \\frac{t}{5}`],
        [L.cinc, `\\Delta s = s(${tn(t0 + dt, 4)}) - s(${tn(t0, 3)}) = ${tn(s1v, 6)} - ${tn(y0, 6)} = ${C("orange", tn(ds, 6))}${U(L.m)}`],
        [L.cavg1, `\\frac{\\Delta s}{\\Delta t} = \\frac{${tn(ds, 6)}}{${tn(dt, 3)}} = ${C("orange", tn(a, 6))}${U(L.mpm)}`],
        [L.cinst, `s'(t_0) = 3600\\,(u_0 - u_0^2) = 3600\\,(${tn(u0, 4)} - ${tn(u0, 4)}^2) = ${C("blue", tn(vi, 6))}${U(L.mpm)}`],
        [L.cgap, `\\Big|\\frac{\\Delta s}{\\Delta t} - s'(t_0)\\Big| = ${C("red", tn(Math.abs(a - vi), 4))}${U(L.mpm)}`],
      ]);
      note(L.gaugeNote(tn(dt, 3), tn(a, 4), tn(vi, 4)));
    }
    plot.onresize = draw;
    fix(); draw();
  });

  // ---------- 3. filling a vessel: dh/dt = Q / A(h) ----------
  const SHAPES = {
    cyl: (h) => 3,
    cone: (h) => 0.7 + 0.45 * h,
    vase: (h) => 1.6 + 2.2 * Math.sin((Math.PI * h) / 10) - 0.5 * Math.sin((2 * Math.PI * h) / 10),
  };
  FV.widget("dm-tank", (root, cfg) => {
    const ui = FV.shell(root, { cols: true }), note = noter(ui);
    const H = 10, TT = 10, N = 500;
    let key = SHAPES[cfg.shape] ? cfg.shape : "vase", t = 4, tab = null;
    function build() { // V(h) by the trapezoid rule
      const r = SHAPES[key], A = (h) => Math.PI * r(h) * r(h), hs = [0], Vs = [0];
      for (let i = 1; i <= N; i++) { const h = (H * i) / N; hs.push(h); Vs.push(Vs[i - 1] + ((A(hs[i - 1]) + A(h)) / 2) * (H / N)); }
      tab = { r, A, hs, Vs, Q: Vs[N] / TT };
    }
    const hAt = (tt) => { const V = Math.min(tab.Vs[N], tab.Q * tt); let lo = 1, hi = N; while (lo < hi) { const m = (lo + hi) >> 1; if (tab.Vs[m] < V) lo = m + 1; else hi = m; } const i = lo; const f = (V - tab.Vs[i - 1]) / (tab.Vs[i] - tab.Vs[i - 1] || 1); return tab.hs[i - 1] + f * (tab.hs[i] - tab.hs[i - 1]); };
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const svg = scene(c1, 300, 300, L.shape);
    const gV = el("g", {}, svg);
    const plot = new FV.Plot(c2, { x: [0, TT], y: [0, H], aspect: 0.9, maxHeight: 320, xLabel: L.tsAxis, yLabel: L.hAxis });
    const seg = FV.ui.seg({ label: L.shape, value: key, options: ["cyl", "cone", "vase"].map((k) => ({ value: k, label: L[k] })), onchange: (k) => { ck.stop(); key = k; build(); t = 0; stt.set(t); draw(); } });
    const stt = FV.ui.slider({ label: L.tsAxis, min: 0, max: TT, step: 0.01, value: t, oninput: (x) => { ck.stop(); t = x; draw(); } });
    const ck = clock({ root, before: () => { if (t >= TT) t = 0; }, tick: (d) => { t = Math.min(TT, t + d * 1.2); stt.set(t); draw(); return t < TT; }, jump: () => { t = t >= TT ? 0 : Math.min(TT, t + 2); stt.set(t); draw(); } });
    ui.controls.append(seg.el, stt.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "h", label: L.level, c: "blue" }, { key: "a", label: L.area }, { key: "r", label: L.rate, c: "orange" }]);
    const SX = 20, BY = 280, SY = 26; // px per cm horizontally, the bottom, px per cm vertically
    const calc = calcPanel(ui);
    function draw() {
      const h = hAt(t), A = tab.A(h), rate = tab.Q / A;
      gV.textContent = "";
      const left = [], right = [], wl = [], wr = [];
      for (let i = 0; i <= 60; i++) { const y = (H * i) / 60, r = tab.r(y); left.push([120 - r * SX, BY - y * SY]); right.push([120 + r * SX, BY - y * SY]); if (y <= h) { wl.push([120 - r * SX, BY - y * SY]); wr.push([120 + r * SX, BY - y * SY]); } }
      const rh = tab.r(h); wl.push([120 - rh * SX, BY - h * SY]); wr.push([120 + rh * SX, BY - h * SY]);
      const poly = (pts) => pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join("");
      el("path", { d: poly(wl.concat(wr.reverse())) + "Z", class: "fill-blue", "fill-opacity": 0.35 }, gV);
      el("line", { x1: 120 - rh * SX, x2: 120 + rh * SX, y1: BY - h * SY, y2: BY - h * SY, class: "s-blue", "stroke-width": 2.5 }, gV);
      el("path", { d: poly(left), fill: "none", class: "s-ink", "stroke-width": 2.5 }, gV);
      el("path", { d: poly(right), fill: "none", class: "s-ink", "stroke-width": 2.5 }, gV);
      el("line", { x1: 120 - tab.r(0) * SX, x2: 120 + tab.r(0) * SX, y1: BY, y2: BY, class: "s-ink", "stroke-width": 2.5 }, gV);
      if (t < TT) el("line", { x1: 120, x2: 120, y1: 4, y2: BY - h * SY, class: "s-blue", "stroke-width": 3, "stroke-dasharray": "2 4", opacity: 0.7 }, gV);
      el("text", { x: 296, y: BY - h * SY + 4, "text-anchor": "end", class: "fv-text dm-small t-blue" }, gV, "h = " + n(h, 3));
      plot.clear();
      plot.fn(hAt, { c: "ink", w: 2.2, from: 0, to: TT, n: 300 });
      plot.line(Math.max(0, t - 1.5), h - rate * Math.min(1.5, t), Math.min(TT, t + 1.5), h + rate * Math.min(1.5, TT - t), { c: "orange", w: 1.8, dash: true });
      plot.dot(t, h, { c: "blue" });
      plot.legend([{ label: "$h(t)$", c: "ink" }, { label: "$dh/dt$", c: "orange", dash: true }]);
      ro.set("h", n(h, 3)); ro.set("a", n(A, 3)); ro.set("r", n(rate, 3));
      const Q = tab.Q, V = Math.min(tab.Vs[N], Q * t), r = tab.r(h), dV = Q * 0.1;
      calc([
        [L.cvol, `V = Q\\,t = ${tn(Q, 4)}\\cdot ${C("ink", tn(t, 3))} = ${tn(V, 5)}${U(L.cm + "^3")}`.replace("\\text{" + L.cm + "^3}", "\\text{" + L.cm + "}^3")],
        [L.carea, `A(h) = \\pi\\,r(h)^2 = \\pi\\cdot ${tn(r, 4)}^2 = ${tn(A, 5)}${U(L.cm)}^2,\\qquad h = ${C("blue", tn(h, 4))}${U(L.cm)}`],
        [L.crate, `\\frac{dh}{dt} = \\frac{Q}{A(h)} = \\frac{${tn(Q, 4)}}{${tn(A, 5)}} = ${C("orange", tn(rate, 4))}${U(L.cm + "/" + L.sec)}`],
        [L.csmall + ", Δt = " + n(0.1), `\\Delta V = Q\\,\\Delta t = ${tn(dV, 4)},\\qquad \\Delta h \\approx \\frac{\\Delta V}{A} = \\frac{${tn(dV, 4)}}{${tn(A, 5)}} = ${tn(dV / A, 4)}${U(L.cm)}`],
      ]);
      note(L.tankNote(tn(h, 3), tn(A, 3), tn(rate, 3)));
    }
    plot.onresize = draw;
    build(); draw();
  });

  // ---------- 4. the microscope: a smooth curve becomes a line ----------
  const ZF = {
    sq: { tex: "f(x) = x^2", f: (x) => x * x, d: (x) => 2 * x, x0: 1, free: true },
    sin: { tex: "f(x) = \\sin x", f: Math.sin, d: Math.cos, x0: 1, free: true },
    abs: { tex: "f(x) = |x|", f: Math.abs, d: null, x0: 0, free: false },
  };
  FV.widget("dm-zoom", (root) => {
    const ui = FV.shell(root), note = noter(ui);
    let P = ZF.sq, x0 = 1, z = 0;
    const plot = new FV.Plot(ui.stage, { x: [-1, 3], y: [-1, 3], equal: true, xLabel: "x", yLabel: "f(x)" });
    const box = FV.h("div", { class: "dm-zoom-box" }); ui.stage.classList.add("dr-narrow");
    const seg = FV.ui.seg({ label: L.fn, value: "sq", options: Object.keys(ZF).map((k) => ({ value: k, label: "$" + ZF[k].tex + "$" })), onchange: (k) => { ck.stop(); const keep = P.free && ZF[k].free; P = ZF[k]; if (!keep) x0 = P.x0; sx.set(x0); sx.input.disabled = !P.free; draw(); } });
    const sx = FV.ui.slider({ label: L.pt, min: -1.5, max: 2, step: 0.01, value: x0, oninput: (v) => { ck.stop(); x0 = v; draw(); } });
    const sz = FV.ui.slider({ label: L.zoom, min: 0, max: 3, step: 0.01, value: z, fmt: (v) => "×" + n(Math.pow(10, v), 3), oninput: (v) => { ck.stop(); z = v; draw(); } });
    const ck = clock({ root, before: () => { if (z >= 3) z = 0; }, tick: (d) => { z = Math.min(3, z + d * 0.45); sz.set(z); draw(); return z < 3; }, jump: () => { z = z >= 3 ? 0 : Math.min(3, z + 1); sz.set(z); draw(); } });
    ui.controls.append(seg.el, sx.el, sz.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "w", label: L.win }, { key: "d", label: L.dev, c: "red" }]);
    const devLabel = ui.readout.querySelectorAll(".fv-ro")[1].firstChild;
    const calc = calcPanel(ui);
    function draw() {
      const w = 2 / Math.pow(10, z), y0 = P.f(x0);
      plot.setDomain([x0 - w, x0 + w], [y0 - w, y0 + w]);
      plot.clear();
      plot.fn(P.f, { c: "ink", w: 2.6, n: 400 });
      let dev = 0;
      if (P.d) {
        const k = P.d(x0);
        plot.line(x0 - w, y0 - k * w, x0 + w, y0 + k * w, { c: "blue", w: 1.6, dash: true });
        for (let i = 0; i <= 100; i++) { const x = x0 - w + (2 * w * i) / 100; dev = Math.max(dev, Math.abs(P.f(x) - y0 - k * (x - x0))); }
        note(L.zoomNote(n(Math.pow(10, z), 3), tn((dev / (2 * w)) * 100, 3) + "\\,\\%"));
      } else {
        plot.line(x0 - w, w, x0, 0, { c: "red", w: 1.4, dash: true }); plot.line(x0, 0, x0 + w, w, { c: "teal", w: 1.4, dash: true });
        dev = w; note(L.kinkNote(n(Math.pow(10, z), 3)));
      }
      plot.dot(x0, y0, { c: "orange" });
      ro.set("w", n(2 * w, 3)); ro.set("d", n((dev / (2 * w)) * 100, 3) + " %");
      devLabel.textContent = P.d ? FV.plain(L.dev) : L.devh;
      if (P.d) {
        const k = P.d(x0), sq = P === ZF.sq;
        calc([
          [L.cpoint, `f(x_0) = ${sq ? P0(tn(x0, 3)) + "^2" : "\\sin " + P0(tn(x0, 3))} = ${tn(y0, 5)},\\qquad f'(x_0) = ${sq ? "2\\cdot " + P0(tn(x0, 3)) : "\\cos " + P0(tn(x0, 3))} = ${C("blue", tn(k, 5))}`],
          [L.ctan, `y = f(x_0) + f'(x_0)\\,(x - x_0) = ${tn(y0, 5)} ${pm(k, 5)}\\,(x ${pm(-x0, 3)})`],
          [L.cdev, sq ? `\\Delta f - f'(x_0)\\,\\Delta x = \\Delta x^2,\\quad \\max_{|\\Delta x| \\le w} \\Delta x^2 = w^2 = ${tn(w, 4)}^2 = ${C("red", tn(w * w, 4))}` : `\\max_{|\\Delta x| \\le w}\\big|\\Delta f - f'(x_0)\\,\\Delta x\\big| = ${C("red", tn(dev, 4))},\\quad w = ${tn(w, 4)}`],
          [L.cratio, `\\frac{${tn(dev, 4)}}{2w} = \\frac{${tn(dev, 4)}}{${tn(2 * w, 4)}} = ${C("red", tn((dev / (2 * w)) * 100, 4))}\\,\\%`],
        ]);
      } else {
        calc([
          [L.ckink, `\\frac{f(0 + \\Delta x) - f(0)}{\\Delta x} = \\frac{|\\Delta x|}{\\Delta x} = \\begin{cases} ${C("teal", "+1")}, & \\Delta x > 0\\\\ ${C("red", "-1")}, & \\Delta x < 0 \\end{cases}`],
          [L.cratio, `w = ${tn(w, 4)}:\\quad \\frac{\\max|f - 0|}{2w} = \\frac{${tn(w, 4)}}{${tn(2 * w, 4)}} = 50\\,\\%`],
        ]);
      }
    }
    plot.onresize = draw;
    draw();
  });

  // ---------- 5. the graph of f′ drawn from the slopes ----------
  const BF = {
    cubic: { tex: "f(x) = x^3 - 3x", f: (x) => x * x * x - 3 * x, d: (x) => 3 * x * x - 3, x: [-2.3, 2.3], y: [-4, 4], dy: [-4, 13] },
    sq: { tex: "f(x) = x^2", f: (x) => x * x, d: (x) => 2 * x, x: [-2.2, 2.2], y: [-0.5, 5], dy: [-5, 5] },
    sin: { tex: "f(x) = \\sin x", f: Math.sin, d: Math.cos, x: [-0.5, 7], y: [-1.4, 1.4], dy: [-1.4, 1.4] },
  };
  FV.widget("dm-build", (root) => {
    const ui = FV.shell(root), note = noter(ui);
    let P = BF.cubic, xc = P.x[0];
    const d = (x) => P.d(x);
    const p1 = new FV.Plot(ui.stage, { x: P.x, y: P.y, aspect: 0.4, maxHeight: 260, minHeight: 170, xLabel: "x", title: L.fGraph });
    const p2 = new FV.Plot(ui.stage, { x: P.x, y: P.dy, aspect: 0.4, maxHeight: 260, minHeight: 170, xLabel: "x", title: L.dGraph });
    p2.svg.setAttribute("aria-hidden", "true");
    const seg = FV.ui.seg({ label: L.fn, value: "cubic", options: Object.keys(BF).map((k) => ({ value: k, label: "$" + BF[k].tex + "$" })), onchange: (k) => { ck.stop(); P = BF[k]; p1.setDomain(P.x, P.y); p2.setDomain(P.x, P.dy); sx.input.min = P.x[0]; sx.input.max = P.x[1]; xc = P.x[0]; sx.set(xc); draw(); } });
    const sx = FV.ui.slider({ label: L.x, min: P.x[0], max: P.x[1], step: 0.01, value: xc, oninput: (v) => { ck.stop(); xc = v; draw(); } });
    const ck = clock({ root, before: () => { if (xc >= P.x[1] - 1e-6) xc = P.x[0]; }, tick: (dt) => { xc = Math.min(P.x[1], xc + dt * (P.x[1] - P.x[0]) / 7); sx.set(xc); draw(); return xc < P.x[1]; }, jump: () => { xc = xc >= P.x[1] - 1e-6 ? P.x[0] : Math.min(P.x[1], xc + (P.x[1] - P.x[0]) / 6); sx.set(xc); draw(); } });
    ui.controls.append(seg.el, sx.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "f", label: "$f(x)$" }, { key: "d", label: L.slope, c: "orange" }]);
    const calc = calcPanel(ui);
    const EXPR = { cubic: ["x^3 - 3x", (x) => `${x}^3 - 3\\cdot ${x}`, "3x^2 - 3", (x) => `3\\cdot ${x}^2 - 3`], sq: ["x^2", (x) => `${x}^2`, "2x", (x) => `2\\cdot ${x}`], sin: ["\\sin x", (x) => `\\sin ${x}`, "\\cos x", (x) => `\\cos ${x}`] };
    const keyOf = () => Object.keys(BF).find((kk) => BF[kk] === P);
    function draw() {
      const y = P.f(xc), k = d(xc), c = k > 1e-6 ? "teal" : k < -1e-6 ? "red" : "orange";
      p1.clear(); p2.clear();
      p1.fn(P.f, { c: "ink", w: 2.2 });
      p2.fn(d, { c: "faint", w: 1.2, dash: "4 4" });
      p2.fn(d, { c: "orange", w: 2.6, from: P.x[0], to: xc });
      const w = (P.x[1] - P.x[0]) * 0.18;
      p1.line(xc - w, y - k * w, xc + w, y + k * w, { c, w: 2.4 });
      // where the tangent was horizontal so far
      const zs = []; for (let i = 0; i < 400; i++) { const a = P.x[0] + ((P.x[1] - P.x[0]) * i) / 400, b = a + (P.x[1] - P.x[0]) / 400; if (b <= xc && d(a) * d(b) <= 0) zs.push((a + b) / 2); }
      zs.forEach((x) => { p1.dot(x, P.f(x), { c: "orange", r: 4, hollow: true }); p2.dot(x, 0, { c: "orange", r: 4, hollow: true }); });
      p1.dot(xc, y, { c }); p2.dot(xc, k, { c });
      p2.vline(xc); p1.vline(xc);
      p1.legend([{ label: "$" + P.tex + "$", c: "ink" }, { label: L.slope + " > 0", c: "teal" }, { label: L.slope + " < 0", c: "red" }]);
      p2.legend([{ label: "$f'(x)$", c: "orange" }, { label: L.zeros, c: "orange", dot: true }]);
      ro.set("f", n(y)); ro.set("d", n(k));
      const E = EXPR[keyOf()], X0 = tn(xc, 3), hs = xc + 0.01 <= P.x[1] ? 0.01 : -0.01, q = (P.f(xc + hs) - y) / hs;
      calc([
        [L.cval, `f(x) = ${E[0]} = ${E[1](X0.startsWith("-") ? "(" + X0 + ")" : X0)} = ${tn(y, 5)}`],
        [L.cdef + ", Δx = " + n(hs, 2), `\\frac{f(x + \\Delta x) - f(x)}{\\Delta x} = \\frac{${tn(P.f(xc + hs), 6)} - ${tn(y, 6)}}{${tn(hs, 2)}} = ${tn(q, 5)}`],
        [L.cder, `f'(x) = ${E[2]} = ${E[3](X0.startsWith("-") ? "(" + X0 + ")" : X0)} = ${C(c, tn(k, 5))}`],
        [L.csign, Math.abs(k) < 1e-6 ? `f'(x) = 0:\\ \\text{${L.flatw}}` : k > 0 ? `${C("teal", "f'(x) > 0")}\\ \\Rightarrow\\ f\\ \\text{${L.up}}` : `${C("red", "f'(x) < 0")}\\ \\Rightarrow\\ f\\ \\text{${L.down}}`],
      ]);
      note(L.buildNote(tn(xc, 3), tn(k, 3)));
    }
    const redraw = () => draw();
    p1.onresize = redraw; p2.onresize = redraw;
    draw();
  });

  // ---------- 6. a ball thrown up: h, h′, h″ ----------
  FV.widget("dm-ball", (root) => {
    const ui = FV.shell(root, { cols: true }), note = noter(ui);
    const h = (t) => 20 * t - 5 * t * t, v = (t) => 20 - 10 * t;
    let t = 0.8;
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    c1.classList.add("dm-ball-col");
    const svg = scene(c1, 160, 320, L.hgt);
    svg.setAttribute("viewBox", "-34 0 194 320");
    const Y = (hh) => 280 - hh * 12.5; // the ball centre; its bottom touches the ground (y = 290) at h = 0
    el("line", { x1: 10, x2: 150, y1: 290, y2: 290, class: "s-ink", "stroke-width": 2.5 }, svg);
    const Yt = (hh) => 290 - hh * 12.5; // the height scale for the ticks (the bottom of the ball)
    for (let k = 0; k <= 20; k += 5) { el("line", { x1: 18, x2: 26, y1: Yt(k), y2: Yt(k), class: "s-ink" }, svg); el("text", { x: 14, y: Yt(k) + 4, "text-anchor": "end", class: "fv-text dm-small" }, svg, String(k)); }
    const trail = el("g", {}, svg), ball = el("circle", { cx: 80, r: 10, class: "fill-orange" }, svg), arrow = el("g", { class: "s-blue fill-blue" }, svg);
    const mk = (y, lab) => new FV.Plot(c2, { x: [0, 4], y, aspect: 0.32, maxHeight: 150, minHeight: 110, xLabel: L.tsec, title: lab });
    const ph = mk([-1, 22], L.hgt), pv = mk([-22, 22], L.vel), pa = mk([-12, 2], L.acc);
    [pv, pa].forEach((pp) => pp.svg.setAttribute("aria-hidden", "true"));
    const stt = FV.ui.slider({ label: L.tsec, min: 0, max: 4, step: 0.01, value: t, oninput: (x) => { ck.stop(); t = x; draw(); } });
    const ck = clock({ root, before: () => { if (t >= 4) t = 0; }, tick: (d) => { t = Math.min(4, t + d * 0.8); stt.set(t); draw(); return t < 4; }, jump: () => { t = t >= 4 ? 0 : Math.min(4, t + 0.5); stt.set(t); draw(); } });
    ui.controls.append(stt.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "h", label: L.hgt, c: "orange" }, { key: "v", label: L.vel, c: "blue" }, { key: "a", label: L.acc, c: "red" }]);
    const calc = calcPanel(ui);
    function draw() {
      const hh = h(t), vv = v(t);
      ball.setAttribute("cy", Y(hh));
      trail.textContent = "";
      for (let s = 0; s < t; s += 0.25) el("circle", { cx: 80, cy: Y(h(s)), r: 2.5, class: "fill-faint" }, trail);
      arrow.textContent = "";
      if (Math.abs(vv) > 0.3) {
        // 2.6 px per m/s, but never through the ground or out of the top
        const y1 = Y(hh), len = FV.clamp(-vv * 2.6, -(y1 - 14), 286 - y1), y2 = y1 + len, dir = Math.sign(len);
        el("line", { x1: 112, x2: 112, y1, y2: y2 - dir * 6, "stroke-width": 3 }, arrow);
        el("path", { d: `M112 ${y2}l-6 ${-dir * 9}h12z` }, arrow);
      }
      [[ph, h, "orange"], [pv, v, "blue"], [pa, () => -10, "red"]].forEach(([p, f, c]) => { p.clear(); p.fn(f, { c, w: 2.2 }); p.vline(t); p.dot(t, f(t), { c }); });
      ph.line(Math.max(0, t - 0.6), hh - vv * Math.min(0.6, t), Math.min(4, t + 0.6), hh + vv * Math.min(0.6, 4 - t), { c: "blue", w: 1.6, dash: true });
      pv.line(Math.max(0, t - 0.6), vv + 10 * Math.min(0.6, t), Math.min(4, t + 0.6), vv - 10 * Math.min(0.6, 4 - t), { c: "red", w: 1.6, dash: true });
      ro.set("h", n(hh, 3)); ro.set("v", n(vv, 3)); ro.set("a", "−10");
      const T3 = tn(t, 3);
      calc([
        [L.ch, `h(t) = 20t - 5t^2 = 20\\cdot ${T3} - 5\\cdot ${T3}^2 = ${C("orange", tn(hh, 5))}${U(L.m)}`],
        [L.cdef + ", Δt = " + n(0.01), `\\frac{h(t + \\Delta t) - h(t)}{\\Delta t} = 20 - 10t - 5\\,\\Delta t = ${tn(20 - 10 * t - 0.05, 5)} \\approx v(t)`],
        [L.cv, `v(t) = h'(t) = 20 - 10t = 20 - 10\\cdot ${T3} = ${C("blue", tn(vv, 5))}${U(L.m + "/" + L.sec)}`],
        [L.ca, `a(t) = v'(t) = h''(t) = \\lim_{\\Delta t \\to 0}\\frac{v(t + \\Delta t) - v(t)}{\\Delta t} = \\lim_{\\Delta t \\to 0}\\frac{-10\\,\\Delta t}{\\Delta t} = ${C("red", "-10")}${U(L.m + "/" + L.sec)}^2`],
      ]);
      note(L.ballNote(tn(t, 3), tn(hh, 3), tn(vv, 3)));
    }
    ph.onresize = pv.onresize = pa.onresize = draw;
    draw();
  });

  // ---------- 7. gears: the chain rule ----------
  // Tooth counts keep the exact ratios (n₂ = n₁/k₁, n₃ = n₂/k₂) with a common tooth size, so the teeth really mesh.
  const gcd = (a, b) => (b ? gcd(b, a % b) : a);
  FV.widget("dm-gears", (root) => {
    const ui = FV.shell(root), note = noter(ui);
    let k1 = 2, k2 = 1.5, th = 0;
    const svg = scene(ui.stage, 720, 290, L.cchain + ": dy/dx = dy/du · du/dx");
    const g = el("g", {}, svg);
    const s1 = FV.ui.slider({ label: L.k1, min: 0.5, max: 3, step: 0.5, value: k1, oninput: (v) => { k1 = v; th = 0; layout(); draw(); } });
    const s2 = FV.ui.slider({ label: L.k2, min: 0.5, max: 3, step: 0.5, value: k2, oninput: (v) => { k2 = v; th = 0; layout(); draw(); } });
    const ck = clock({ root, tick: (d) => { th += d * 0.6; draw(); return true; }, jump: () => { th += 0.25; draw(); } });
    ui.controls.append(s1.el, s2.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "x", label: L.turnsX }, { key: "u", label: L.turnsU, c: "teal" }, { key: "y", label: L.turnsY, c: "orange" }, { key: "k", label: "$\\frac{dy}{dx}$", c: "blue" }]);
    const calc = calcPanel(ui);
    let G = [];
    // a gear with n teeth, a tooth centred on angle 0
    function gearPath(r, nT, depth) {
      let d = "";
      const tw = (Math.PI * 2) / nT;
      for (let i = 0; i < nT; i++) {
        const a = i * tw;
        [[a - tw * 0.3, r + depth], [a + tw * 0.3, r + depth], [a + tw * 0.45, r - depth], [a + tw * 0.55, r - depth]].forEach(([b, rr], j) => { d += (i === 0 && j === 0 ? "M" : "L") + (rr * Math.cos(b)).toFixed(1) + " " + (rr * Math.sin(b)).toFixed(1); });
      }
      return d + "Z";
    }
    function layout() {
      // integer tooth counts in the exact ratios, reduced, then scaled so that the smallest gear has at least 8 teeth
      let n = [144, 144 / k1, 144 / k1 / k2];
      const gg = n.reduce((a, b) => gcd(a, b));
      n = n.map((x) => x / gg);
      const m = Math.ceil(8 / Math.min(...n));
      n = n.map((x) => x * m);
      const pitch0 = 12, r0 = n.map((x) => (x * pitch0) / (2 * Math.PI));
      const total = 2 * (r0[0] + r0[1] + r0[2]) + 20, sc = Math.min(1.6, 690 / total, 220 / (2 * Math.max(...r0) + 10));
      const r = r0.map((x) => x * sc), depth = Math.min(6, (pitch0 * sc) / 4.5);
      const cx1 = 360 - (r[0] + r[1] + r[2]) + r[0], cx2 = cx1 + r[0] + r[1], cx3 = cx2 + r[1] + r[2];
      // the phase: gear 1 has a tooth at the contact point (angle 0); gear 2 a gap at its angle π;
      // gear 3 takes a tooth or a gap at its contact point, opposite to what gear 2 shows there
      const tw = n.map((x) => (2 * Math.PI) / x);
      const ph2 = Math.PI - tw[1] / 2;
      const gapAt2 = n[1] % 2 === 0; // gear 2 shows a gap at its right side when n₂ is even
      const ph3 = gapAt2 ? Math.PI : Math.PI - tw[2] / 2;
      g.textContent = "";
      G = [[cx1, r[0], n[0], "ink", "x", 0], [cx2, r[1], n[1], "teal", "u", ph2], [cx3, r[2], n[2], "orange", "y", ph3]].map(([cx, rr, nT, c, name, ph]) => {
        const grp = el("g", {}, g);
        el("path", { d: gearPath(rr, nT, depth), class: "s-" + c + " fill-" + c, "fill-opacity": 0.25, "stroke-width": 2 }, grp);
        el("line", { x1: 0, y1: 0, x2: Math.max(4, rr - 2 * depth - 2), y2: 0, class: "s-" + c, "stroke-width": 3 }, grp);
        el("circle", { r: 4, class: "fill-" + c }, grp);
        el("text", { x: cx, y: Math.min(284, 140 + rr + depth + 20), "text-anchor": "middle", class: "fv-text dm-small t-" + c }, g, name + " · " + nT);
        return { cx, grp, ph };
      });
    }
    function draw() {
      const angs = [th, -th * k1, th * k1 * k2];
      G.forEach((gg, i) => gg.grp.setAttribute("transform", `translate(${gg.cx} 140) rotate(${(((angs[i] + gg.ph) * 180) / Math.PI).toFixed(2)})`));
      const turns = th / (2 * Math.PI);
      ro.set("x", n(turns, 3)); ro.set("u", n(turns * k1, 3)); ro.set("y", n(turns * k1 * k2, 3)); ro.set("k", n(k1 * k2, 3));
      const Nx = tn(turns, 3), Nu = tn(turns * k1, 3), Ny = tn(turns * k1 * k2, 3);
      calc([
        [L.cturn + ": u", `N_u = \\frac{du}{dx}\\cdot N_x = ${tn(k1, 2)}\\cdot ${Nx} = ${C("teal", Nu)}`],
        [L.cturn + ": y", `N_y = \\frac{dy}{du}\\cdot N_u = ${tn(k2, 2)}\\cdot ${Nu} = ${C("orange", Ny)}`],
        [L.cchain, `\\frac{dy}{dx} = \\frac{dy}{du}\\cdot\\frac{du}{dx} = ${tn(k2, 2)}\\cdot ${tn(k1, 2)} = ${C("blue", tn(k1 * k2, 3))}`],
      ]);
      note(L.gearsNote(tn(k1, 3), tn(k2, 3), tn(k1 * k2, 3)));
    }
    layout(); draw();
  });

  // ---------- 8. a shower with two taps: partial derivatives ----------
  const SH = {
    ru: { hot: "Горячий кран $h$, л/мин", cold: "Холодный кран $c$, л/мин", turn: "Крутим", tHot: "горячий", tCold: "холодный", temp: "температура $T$, °C",
      sliceH: "$T$ при замороженном $c$", sliceC: "$T$ при замороженном $h$", hAx: "h, л/мин", cAx: "c, л/мин", mix: "Температура смеси", dh: "Горячий кран (c заморожен)", dc: "Холодный кран (h заморожен)",
      both: "Крутим оба на 0,1 л/мин", exact: "Точно", grad: "Градиент", note: (T, a, b) => `Сейчас $T = ${T}$ °C. Если повернуть только горячий кран, каждый лишний литр в минуту даёт около $${a}$ °C (наклон верхнего среза $\\partial T / \\partial h$); только холодный — около $${b}$ °C (наклон нижнего среза $\\partial T / \\partial c$). Чтобы понять вклад одного крана, второй «замораживают».` },
    en: { hot: "Hot tap $h$, l/min", cold: "Cold tap $c$, l/min", turn: "Turn", tHot: "hot", tCold: "cold", temp: "temperature $T$, °C",
      sliceH: "$T$ with $c$ frozen", sliceC: "$T$ with $h$ frozen", hAx: "h, l/min", cAx: "c, l/min", mix: "Mixed temperature", dh: "Hot tap (c frozen)", dc: "Cold tap (h frozen)",
      both: "Turn both by 0.1 l/min", exact: "Exactly", grad: "Gradient", note: (T, a, b) => `Now $T = ${T}$ °C. Turning only the hot tap, each extra litre per minute adds about $${a}$ °C (the slope of the upper slice $\\partial T / \\partial h$); only the cold one, about $${b}$ °C (the slope of the lower slice $\\partial T / \\partial c$). To see the effect of one tap, the other one is “frozen”.` },
    uz: { hot: "Issiq jo‘mrak $h$, l/daq", cold: "Sovuq jo‘mrak $c$, l/daq", turn: "Buraymiz", tHot: "issiq", tCold: "sovuq", temp: "harorat $T$, °C",
      sliceH: "$c$ muzlatilganda $T$", sliceC: "$h$ muzlatilganda $T$", hAx: "h, l/daq", cAx: "c, l/daq", mix: "Aralashma harorati", dh: "Issiq jo‘mrak (c muzlatilgan)", dc: "Sovuq jo‘mrak (h muzlatilgan)",
      both: "Ikkalasini 0,1 l/daq ga buraymiz", exact: "Aniq", grad: "Gradiyent", note: (T, a, b) => `Hozir $T = ${T}$ °C. Faqat issiq jo‘mrakni bursak, har bir qo‘shimcha litr/daqiqa taxminan $${a}$ °C beradi (yuqori kesim qiyaligi $\\partial T / \\partial h$); faqat sovuqni — taxminan $${b}$ °C (pastki kesim qiyaligi $\\partial T / \\partial c$). Bitta jo‘mrakning hissasini ko‘rish uchun ikkinchisi «muzlatiladi».` },
  }[FV.lang] || {};
  FV.widget("dm-shower", (root) => {
    const ui = FV.shell(root, { cols: true }), note = noter(ui);
    const T = (h, c) => (60 * h + 10 * c) / (h + c), Th = (h, c) => (50 * c) / ((h + c) * (h + c)), Tc = (h, c) => (-50 * h) / ((h + c) * (h + c));
    let h = 2, c = 3, tap = "hot";
    const c0 = FV.col(ui.stage), c1 = FV.col(ui.stage);
    c0.classList.add("dm-ball-col");
    const svg = scene(c0, 160, 300, SH.mix);
    // the shower: a pipe from both taps, the head and the water coloured by temperature
    el("path", { d: "M30 270V60h100v210", fill: "none", class: "s-ink", "stroke-width": 4 }, svg);
    el("path", { d: "M80 60V30h40", fill: "none", class: "s-ink", "stroke-width": 4 }, svg);
    el("rect", { x: 108, y: 30, width: 34, height: 10, rx: 4, class: "fill-ink" }, svg);
    const tapH = el("circle", { cx: 30, cy: 250, r: 11, class: "fill-red" }, svg), tapC = el("circle", { cx: 130, cy: 250, r: 11, class: "fill-blue" }, svg);
    const water = el("g", {}, svg), thermo = el("text", { x: 80, y: 160, "text-anchor": "middle", class: "fv-text dm-big" }, svg);
    const labH = el("text", { x: 30, y: 292, "text-anchor": "middle", class: "fv-text dm-small t-red" }, svg), labC = el("text", { x: 130, y: 292, "text-anchor": "middle", class: "fv-text dm-small t-blue" }, svg);
    const p1 = new FV.Plot(c1, { x: [0, 6], y: [8, 62], aspect: 0.45, maxHeight: 190, minHeight: 140, xLabel: SH.hAx, title: SH.sliceH });
    const p2 = new FV.Plot(c1, { x: [0, 6], y: [8, 62], aspect: 0.45, maxHeight: 190, minHeight: 140, xLabel: SH.cAx, title: SH.sliceC });
    p1.svg.setAttribute("aria-hidden", "true"); p2.svg.setAttribute("aria-hidden", "true");
    const sh = FV.ui.slider({ label: SH.hot, min: 0.1, max: 6, step: 0.1, value: h, oninput: (v) => { ck.stop(); h = v; draw(); } });
    const sc = FV.ui.slider({ label: SH.cold, min: 0.1, max: 6, step: 0.1, value: c, oninput: (v) => { ck.stop(); c = v; draw(); } });
    const seg = FV.ui.seg({ label: SH.turn, value: tap, options: [{ value: "hot", label: SH.tHot }, { value: "cold", label: SH.tCold }], onchange: (v) => { ck.stop(); tap = v; } });
    const ck = clock({ root, before: () => { if (tap === "hot" && h >= 6) h = 0.1; if (tap === "cold" && c >= 6) c = 0.1; },
      tick: (d) => { if (tap === "hot") { h = Math.min(6, h + d * 1.2); sh.set(h); } else { c = Math.min(6, c + d * 1.2); sc.set(c); } draw(); return (tap === "hot" ? h : c) < 6; },
      jump: () => { if (tap === "hot") { h = h >= 6 ? 0.1 : Math.min(6, h + 1); sh.set(h); } else { c = c >= 6 ? 0.1 : Math.min(6, c + 1); sc.set(c); } draw(); } });
    ui.controls.append(sh.el, sc.el, seg.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "T", label: SH.temp, c: "orange" }, { key: "a", label: "$\\partial T / \\partial h$", c: "red" }, { key: "b", label: "$\\partial T / \\partial c$", c: "blue" }]);
    const calc = calcPanel(ui);
    function draw() {
      const t = T(h, c), a = Th(h, c), b = Tc(h, c);
      // water: colour from blue (10 °C) to red (60 °C), streak count by the flow
      const k = (t - 10) / 50, col = FV.cmap("diverging", FV.clamp(k, 0, 1));
      water.textContent = "";
      const nS = Math.max(2, Math.min(9, Math.round(h + c)));
      for (let i = 0; i < nS; i++) { const x = 112 + (i * 28) / (nS - 1); el("line", { x1: x, x2: x - 6 + i, y1: 44, y2: 230, stroke: FV.rgb(col, 0.8), "stroke-width": 2.4, "stroke-dasharray": "6 6" }, water); }
      thermo.textContent = n(t, 3) + " °C";
      tapH.setAttribute("r", 6 + h * 1.3); tapC.setAttribute("r", 6 + c * 1.3);
      labH.textContent = "h = " + n(h, 2); labC.textContent = "c = " + n(c, 2);
      p1.clear(); p1.fn((x) => T(x, c), { c: "red", w: 2.2, from: 0.05 });
      p1.line(Math.max(0.05, h - 1.2), t - a * Math.min(1.2, h - 0.05), Math.min(6, h + 1.2), t + a * Math.min(1.2, 6 - h), { c: "orange", w: 1.6, dash: true }); p1.dot(h, t, { c: "orange" });
      p2.clear(); p2.fn((x) => T(h, x), { c: "blue", w: 2.2, from: 0.05 });
      p2.line(Math.max(0.05, c - 1.2), t - b * Math.min(1.2, c - 0.05), Math.min(6, c + 1.2), t + b * Math.min(1.2, 6 - c), { c: "orange", w: 1.6, dash: true }); p2.dot(c, t, { c: "orange" });
      ro.set("T", n(t, 4)); ro.set("a", n(a, 4)); ro.set("b", n(b, 4));
      const H = tn(h, 2), Cc = tn(c, 2), S = tn(h + c, 3), d1 = tn(0.1), t2 = T(h + 0.1, c + 0.1);
      const qh = (T(h + 0.01, c) - t) / 0.01;
      calc([
        [SH.mix, `T(h, c) = \\frac{60h + 10c}{h + c} = \\frac{60\\cdot ${C("red", H)} + 10\\cdot ${C("blue", Cc)}}{${S}} = ${C("orange", tn(t, 5))}\\ ^\\circ\\text{C}`],
        [SH.dh, `\\frac{\\partial T}{\\partial h} = \\frac{50c}{(h + c)^2} = \\frac{50\\cdot ${Cc}}{${S}^2} = ${C("red", tn(a, 5))}`],
        [L.cdef + ", Δh = " + n(0.01), `\\frac{T(h + \\Delta h,\\ c) - T(h, c)}{\\Delta h} = \\frac{${tn(T(h + 0.01, c), 6)} - ${tn(t, 6)}}{${tn(0.01)}} = ${tn(qh, 5)}`],
        [SH.dc, `\\frac{\\partial T}{\\partial c} = -\\frac{50h}{(h + c)^2} = -\\frac{50\\cdot ${H}}{${S}^2} = ${C("blue", tn(b, 5))}`],
        [SH.both, `dT \\approx \\frac{\\partial T}{\\partial h}\\,\\Delta h + \\frac{\\partial T}{\\partial c}\\,\\Delta c = ${tn(a, 4)}\\cdot ${d1} ${pm(b, 4)}\\cdot ${d1} = ${C("orange", tn((a + b) * 0.1, 4))}`],
        [SH.exact, `T(h + ${d1},\\ c + ${d1}) - T(h, c) = ${tn(t2, 5)} - ${tn(t, 5)} = ${tn(t2 - t, 4)}`],
        [SH.grad, `\\nabla T = \\Big(\\frac{\\partial T}{\\partial h}${FV.lang === "en" ? ",\\ " : ";\\ "}\\frac{\\partial T}{\\partial c}\\Big) = (${C("red", tn(a, 4))}${FV.lang === "en" ? ",\\ " : ";\\ "}${C("blue", tn(b, 4))})`],
      ]);
      note(SH.note(tn(t, 4), tn(a, 3), tn(b, 3)));
    }
    const redraw = () => draw();
    p1.onresize = p2.onresize = redraw;
    draw();
  });
})();
