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
      play: "Пуск", pause: "Пауза", restart: "Сначала", time: "Время $t$, мин", work: "работа", home: "дом",
      walker: "пешеход", car: "машина", dist: "путь", speed: "скорость", avg: "средняя", mpm: "м/мин", kmh: "км/ч", m: "м",
      sAxis: "путь s, м", tAxis: "t, мин",
      raceNote: (t, s1, s2, v2, k2) => `$t = ${t}$ мин. Пешеход прошёл $${s1}$ м, его скорость всё время $80$ м/мин — его график прямая, наклон везде одинаков. Машина проехала $${s2}$ м, её скорость сейчас $${v2}$ м/мин ($${k2}$ км/ч) — это наклон касательной к её графику. Оба добрались за $5$ минут, но средние скорости разные: $400 \\div 5 = 80$ и $3000 \\div 5 = 600$ м/мин.`,
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
      gearsNote: (a, b, c) => `Первая шестерня ($x$) делает оборот — вторая ($u$) делает $${a}$ оборота, третья ($y$) — $${a} \\cdot ${b} = ${c}$. Передаточные числа перемножаются: $\\frac{dy}{dx} = \\frac{dy}{du}\\cdot\\frac{du}{dx}$. Это и есть цепное правило; маленькая шестерня крутится быстрее большой.`,
    },
    en: {
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
      gearsNote: (a, b, c) => `The first gear ($x$) makes one turn — the second ($u$) makes $${a}$ turns, the third ($y$) $${a} \\cdot ${b} = ${c}$. The gear ratios multiply: $\\frac{dy}{dx} = \\frac{dy}{du}\\cdot\\frac{du}{dx}$. That is the chain rule; a small gear spins faster than a big one.`,
    },
    uz: {
      play: "Boshlash", pause: "Pauza", restart: "Boshidan", time: "Vaqt $t$, daq", work: "ish", home: "uy",
      walker: "piyoda", car: "mashina", dist: "yo‘l", speed: "tezlik", avg: "o‘rtacha", mpm: "m/daq", kmh: "km/soat", m: "m",
      sAxis: "yo‘l s, m", tAxis: "t, daq",
      raceNote: (t, s1, s2, v2, k2) => `$t = ${t}$ daq. Piyoda $${s1}$ m yurdi, uning tezligi doim $80$ m/daq — grafigi to‘g‘ri chiziq, qiyaligi hamma joyda bir xil. Mashina $${s2}$ m yurdi, hozirgi tezligi $${v2}$ m/daq ($${k2}$ km/soat) — bu uning grafigiga urinmaning qiyaligi. Ikkalasi ham $5$ daqiqada yetib keldi, lekin o‘rtacha tezliklar har xil: $400 \\div 5 = 80$ va $3000 \\div 5 = 600$ m/daq.`,
      t0: "$t_0$ payt, daq", dt: "$\\Delta t$ oraliq, daq", shrink: "Δt → 0", avgSpeed: "o‘rtacha $\\Delta s / \\Delta t$", instSpeed: "spidometr $s'(t_0)$",
      gaugeNote: (dt, a, v) => `$\\Delta t = ${dt}$ daq oraliqda o‘rtacha tezlik $\\frac{\\Delta s}{\\Delta t} = ${a}$ m/daq (to‘q sariq strelka, kesuvchining qiyaligi). Spidometr $${v}$ m/daq ni ko‘rsatadi (ko‘k strelka, urinmaning qiyaligi). $\\Delta t$ ni kichraytiring — strelkalar ustma-ust tushadi: bu hosilaning o‘zi.`,
      shape: "Idish", cyl: "silindr", cone: "voronka", vase: "vaza", level: "sath $h$, sm", rate: "$dh/dt$, sm/s", area: "kesim yuzi $A(h)$, sm²", hAxis: "h, sm", tsAxis: "t, s",
      tankNote: (h, a, r) => `Suv o‘zgarmas $Q$ sarf bilan quyiladi. Sath $h = ${h}$ sm, suv sirtining yuzi $A = ${a}$ sm², sath $\\frac{dh}{dt} = \\frac{Q}{A} = ${r}$ sm/s tezlik bilan ko‘tariladi. Idish tor joyda suv tez ko‘tariladi va grafik tikroq; keng joyda — sekin.`,
      fn: "Funksiya", pt: "$x_0$ nuqta", zoom: "Kattalashtirish", win: "oyna kengligi", dev: "urinmadan og‘ish / oyna",
      zoomNote: (z, d) => `Kattalashtirish $\\times${z}$: oynada egri chiziq urinmadan oyna kengligining ko‘pi bilan $${d}$ qismiga uzoqlashadi. Kattalashtirish qancha kuchli bo‘lsa, egri chiziq shuncha to‘g‘rilanadi — nuqta yaqinida silliq funksiya $f'(x_0)$ qiyalikli to‘g‘ri chiziqdan farq qilmaydi.`,
      kinkNote: (z) => `Kattalashtirish $\\times${z}$, sinish esa sinishligicha qoladi: chapda qiyalik $-1$, o‘ngda $+1$. Qancha kattalashtirmang, $|x|$ nolda to‘g‘ri chiziqqa aylanmaydi — shuning uchun u yerda hosila yo‘q.`,
      x: "$x$ nuqta", fGraph: "$f(x)$ grafigi va urinma", dGraph: "$f'(x)$ grafigi — urinma qiyaliklari", slope: "qiyalik $f'(x)$", zeros: "urinma gorizontal",
      buildNote: (x, d) => `$x = ${x}$ nuqtada urinmaning qiyaligi $f'(x) = ${d}$ — bu nuqta pastki grafikda chizilgan. $f$ o‘sadigan joyda $f' > 0$; kamayadigan joyda $f' < 0$; cho‘qqi va chuqurliklarda $f' = 0$.`,
      hgt: "balandlik $h$, m", vel: "tezlik $v = h'$, m/s", acc: "tezlanish $a = h''$, m/s²", tsec: "t, s",
      ballNote: (t, h, v) => `$t = ${t}$ s: balandlik $h = ${h}$ m, tezlik $v = h'(t) = 20 - 10t = ${v}$ m/s (strelka). Tezlik — balandlik grafigining qiyaligi, tezlanish $a = v'(t) = h''(t) = -10$ m/s² — tezlik grafigining qiyaligi. Eng yuqori nuqtada ($t = 2$ s) urinma gorizontal: $v = 0$.`,
      k1: "$\\frac{du}{dx}$ — birinchi juft uzatmasi", k2: "$\\frac{dy}{du}$ — ikkinchi juft uzatmasi", turnsX: "$x$ aylanishlari", turnsU: "$u$ aylanishlari", turnsY: "$y$ aylanishlari",
      gearsNote: (a, b, c) => `Birinchi tishli g‘ildirak ($x$) bir marta aylanadi — ikkinchisi ($u$) $${a}$ marta, uchinchisi ($y$) $${a} \\cdot ${b} = ${c}$ marta. Uzatish sonlari ko‘paytiriladi: $\\frac{dy}{dx} = \\frac{dy}{du}\\cdot\\frac{du}{dx}$. Bu zanjir qoidasi; kichik g‘ildirak kattasidan tezroq aylanadi.`,
    },
  }[FV.lang] || {};

  const S = FV.svg;
  const n = (v, d = 3) => FV.num(Math.abs(v) < 1e-9 ? 0 : v, d);
  const tn = (v, d = 3) => n(v, d).replace("−", "-").replace(",", "{,}");
  const reduced = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // the note is redrawn every frame; a hidden live region announces it calmly after the motion stops
  function noter(ui) {
    ui.note.setAttribute("aria-live", "off");
    const live = FV.h("div", { class: "sr-only", "aria-live": "polite" });
    ui.root.append(live);
    let t = 0, last = "";
    return (s) => { ui.note.textContent = ""; ui.note.append(FV.rich(s, "span")); last = s; clearTimeout(t); t = setTimeout(() => { live.textContent = FV.plain(last); }, 700); };
  }
  // A clock driving an animation: value v runs from a to b in `secs` seconds; requestAnimationFrame, stops on hidden tab.
  function clock(o) {
    let raf = 0, last = 0;
    const btn = FV.ui.button({ label: "", primary: true, onclick: () => (raf ? stop() : start()) });
    const label = (on) => { btn.el.textContent = ""; btn.el.append(FV.h("span", { "aria-hidden": "true", text: on ? "❚❚ " : "▶ " }), FV.rich(on ? L.pause : o.label || L.play)); };
    label(false);
    function frame(ts) {
      const dt = last ? Math.min(0.1, (ts - last) / 1000) : 0; last = ts;
      if (o.tick(dt) === false) { stop(); return; }
      raf = requestAnimationFrame(frame);
    }
    function start() {
      if (reduced()) { o.jump && o.jump(); return; }
      if (o.before) o.before();
      last = 0; raf = requestAnimationFrame(frame); label(true);
    }
    function stop() { cancelAnimationFrame(raf); raf = 0; label(false); }
    document.addEventListener("visibilitychange", () => { if (document.hidden && raf) stop(); });
    return { el: btn.el, start, stop, get running() { return !!raf; } };
  }
  // A plain SVG scene with a fixed coordinate system that scales with the width.
  function scene(parent, w, h, label) {
    const svg = S("svg", { class: "fv-svg dm-scene", viewBox: `0 0 ${w} ${h}`, role: "img", "aria-label": label || "" });
    parent.append(svg);
    return svg;
  }
  const el = (tag, attrs, parent, text) => { const e = S(tag, attrs, parent); if (text != null) e.textContent = text; return e; };

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
    el("circle", { cx: -9, cy: -3, r: 3.5, class: "fill-ink" }, car); el("circle", { cx: 9, cy: -3, r: 3.5, class: "fill-ink" }, car);
    const lab1 = el("text", { class: "fv-text dm-small t-teal", "text-anchor": "middle" }, gM), lab2 = el("text", { class: "fv-text dm-small t-orange", "text-anchor": "middle" }, gM);
    function roadLayout() {
      const narrow = (road.clientWidth || ui.stage.clientWidth || 720) < 520;
      W = narrow ? 380 : 720; Y1 = narrow ? 70 : 42; Y2 = narrow ? 170 : 102;
      const H = narrow ? 230 : 156;
      road.setAttribute("viewBox", `0 0 ${W} ${H}`);
      road.classList.toggle("dm-road-narrow", narrow);
      gR.textContent = "";
      [Y1, Y2].forEach((y) => {
        el("line", { x1: X(0), x2: X(D2) + 10, y1: y, y2: y, class: "s-guide", "stroke-width": 1, "stroke-dasharray": "4 5" }, gR);
      });
      const house = (s, y) => { const x = X(s); el("path", { d: `M${x - 9} ${y - 2}h18v-12l-9-8l-9 8z`, class: "fill-guide dm-house" }, gR); el("text", { x, y: y + 20, "text-anchor": "middle", class: "fv-text dm-small" }, gR, L.home); };
      house(D1, Y1); house(D2, Y2);
      el("text", { x: X(0), y: H - 8, "text-anchor": "middle", class: "fv-text dm-small" }, gR, L.work);
      el("line", { x1: X(0), x2: X(0), y1: Y1 - 26, y2: Y2 + 14, class: "s-ink", "stroke-width": 2 }, gR);
    }
    const plot = new FV.Plot(ui.stage, { x: [0, 5], y: [0, 3200], aspect: 0.5, maxHeight: 340, xLabel: L.tAxis, yLabel: L.sAxis });
    const st = FV.ui.slider({ label: L.time, min: 0, max: 5, step: 0.01, value: t, oninput: (v) => { ck.stop(); t = v; draw(); } });
    const ck = clock({ before: () => { if (t >= T) t = 0; }, tick: (dt) => { t = Math.min(T, t + dt * 0.7); st.set(t); draw(); return t < T; }, jump: () => { t = t >= T ? 0 : Math.min(T, t + 1); st.set(t); draw(); } });
    ui.controls.append(st.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "s1", label: L.walker + ": " + L.dist, c: "teal" }, { key: "v1", label: L.speed, c: "teal" }, { key: "s2", label: L.car + ": " + L.dist, c: "orange" }, { key: "v2", label: L.speed, c: "orange" }]);
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
      note(L.raceNote(tn(t, 3), tn(a, 3), tn(b, 4), tn(vb, 3), tn(vb * 0.06, 3)));
    }
    plot.onresize = () => { roadLayout(); draw(); };
    roadLayout(); draw();
  });

  // ---------- 2. average speed → the speedometer ----------
  FV.widget("dm-gauge", (root) => {
    const ui = FV.shell(root, { cols: true }), note = noter(ui);
    const T = 5, D = 3000;
    const s = (t) => D * (t / T - Math.sin((2 * Math.PI * t) / T) / (2 * Math.PI)), v = (t) => (D / T) * (1 - Math.cos((2 * Math.PI * t) / T));
    let t0 = 1.5, dt = 2;
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const plot = new FV.Plot(c1, { x: [0, 5], y: [-100, 3200], aspect: 0.75, maxHeight: 340, xLabel: L.tAxis, yLabel: L.sAxis });
    const g = scene(c2, 300, 230, L.instSpeed);
    const CX = 150, CY = 150, R = 110, VMAX = 1400, A0 = -210, A1 = 30; // degrees, clockwise from the x axis
    const ang = (val) => ((A0 + (A1 - A0) * FV.clamp(val / VMAX, 0, 1)) * Math.PI) / 180;
    const P = (a, r) => [CX + r * Math.cos(a), CY + r * Math.sin(a)];
    el("path", { d: `M${P(ang(0), R)[0]} ${P(ang(0), R)[1]} A${R} ${R} 0 1 1 ${P(ang(VMAX), R)[0]} ${P(ang(VMAX), R)[1]}`, fill: "none", class: "s-ink", "stroke-width": 3 }, g);
    for (let k = 0; k <= VMAX; k += 100) {
      const a = ang(k), big = k % 500 === 0, p = P(a, R), q = P(a, R - (big ? 14 : 7));
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
    const ck = clock({ label: L.shrink, before: () => { if (dt < 0.01) { dt = Math.min(2, T - t0); } }, tick: (d) => { dt *= Math.pow(0.35, d); if (dt < 0.005) { dt = 0.005; sdt.set(dt); draw(); return false; } sdt.set(dt); draw(); return true; }, jump: () => { dt = 0.005; sdt.set(dt); draw(); } });
    ui.controls.append(st0.el, sdt.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "a", label: L.avgSpeed, c: "orange" }, { key: "v", label: L.instSpeed, c: "blue" }]);
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
    let key = cfg.shape || "vase", t = 4, tab = null;
    function build() { // V(h) by the trapezoid rule
      const r = SHAPES[key], A = (h) => Math.PI * r(h) * r(h), hs = [0], Vs = [0];
      for (let i = 1; i <= N; i++) { const h = (H * i) / N; hs.push(h); Vs.push(Vs[i - 1] + ((A(hs[i - 1]) + A(h)) / 2) * (H / N)); }
      tab = { r, A, hs, Vs, Q: Vs[N] / TT };
    }
    const hAt = (tt) => { const V = Math.min(tab.Vs[N], tab.Q * tt); let i = 1; while (i < N && tab.Vs[i] < V) i++; const f = (V - tab.Vs[i - 1]) / (tab.Vs[i] - tab.Vs[i - 1] || 1); return tab.hs[i - 1] + f * (tab.hs[i] - tab.hs[i - 1]); };
    const c1 = FV.col(ui.stage), c2 = FV.col(ui.stage);
    const svg = scene(c1, 300, 300, L.shape);
    const gV = el("g", {}, svg);
    const plot = new FV.Plot(c2, { x: [0, TT], y: [0, H], aspect: 0.9, maxHeight: 320, xLabel: L.tsAxis, yLabel: L.hAxis });
    const seg = FV.ui.seg({ label: L.shape, value: key, options: ["cyl", "cone", "vase"].map((k) => ({ value: k, label: L[k] })), onchange: (k) => { ck.stop(); key = k; build(); t = 0; stt.set(t); draw(); } });
    const stt = FV.ui.slider({ label: L.tsAxis, min: 0, max: TT, step: 0.01, value: t, oninput: (x) => { ck.stop(); t = x; draw(); } });
    const ck = clock({ before: () => { if (t >= TT) t = 0; }, tick: (d) => { t = Math.min(TT, t + d * 1.2); stt.set(t); draw(); return t < TT; }, jump: () => { t = t >= TT ? 0 : Math.min(TT, t + 2); stt.set(t); draw(); } });
    ui.controls.append(seg.el, stt.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "h", label: L.level, c: "blue" }, { key: "a", label: L.area }, { key: "r", label: L.rate, c: "orange" }]);
    const SX = 20, BY = 280, SY = 26; // px per cm horizontally, the bottom, px per cm vertically
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
    const seg = FV.ui.seg({ label: L.fn, value: "sq", options: Object.keys(ZF).map((k) => ({ value: k, label: "$" + ZF[k].tex + "$" })), onchange: (k) => { ck.stop(); P = ZF[k]; x0 = P.x0; sx.set(x0); sx.input.disabled = !P.free; draw(); } });
    const sx = FV.ui.slider({ label: L.pt, min: -1.5, max: 2, step: 0.01, value: x0, oninput: (v) => { x0 = v; draw(); } });
    const sz = FV.ui.slider({ label: L.zoom, min: 0, max: 3, step: 0.01, value: z, fmt: (v) => "×" + n(Math.pow(10, v), 3), oninput: (v) => { ck.stop(); z = v; draw(); } });
    const ck = clock({ before: () => { if (z >= 3) z = 0; }, tick: (d) => { z = Math.min(3, z + d * 0.45); sz.set(z); draw(); return z < 3; }, jump: () => { z = z >= 3 ? 0 : Math.min(3, z + 1); sz.set(z); draw(); } });
    ui.controls.append(seg.el, sx.el, sz.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "w", label: L.win }, { key: "d", label: L.dev, c: "red" }]);
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
    }
    plot.onresize = draw;
    draw();
  });

  // ---------- 5. the graph of f′ drawn from the slopes ----------
  const BF = {
    cubic: { tex: "f(x) = x^3 - 3x", f: (x) => x * x * x - 3 * x, x: [-2.3, 2.3], y: [-4, 4], dy: [-4, 13] },
    sq: { tex: "f(x) = x^2", f: (x) => x * x, x: [-2.2, 2.2], y: [-0.5, 5], dy: [-5, 5] },
    sin: { tex: "f(x) = \\sin x", f: Math.sin, x: [-0.5, 7], y: [-1.4, 1.4], dy: [-1.4, 1.4] },
  };
  FV.widget("dm-build", (root) => {
    const ui = FV.shell(root), note = noter(ui);
    let P = BF.cubic, xc = P.x[0];
    const d = (x) => (P.f(x + 1e-4) - P.f(x - 1e-4)) / 2e-4;
    const p1 = new FV.Plot(ui.stage, { x: P.x, y: P.y, aspect: 0.4, maxHeight: 260, minHeight: 170, xLabel: "x", title: L.fGraph });
    const p2 = new FV.Plot(ui.stage, { x: P.x, y: P.dy, aspect: 0.4, maxHeight: 260, minHeight: 170, xLabel: "x", title: L.dGraph });
    const seg = FV.ui.seg({ label: L.fn, value: "cubic", options: Object.keys(BF).map((k) => ({ value: k, label: "$" + BF[k].tex + "$" })), onchange: (k) => { ck.stop(); P = BF[k]; p1.setDomain(P.x, P.y); p2.setDomain(P.x, P.dy); sx.input.min = P.x[0]; sx.input.max = P.x[1]; xc = P.x[0]; sx.set(xc); draw(); } });
    const sx = FV.ui.slider({ label: L.x, min: P.x[0], max: P.x[1], step: 0.01, value: xc, oninput: (v) => { ck.stop(); xc = v; draw(); } });
    const ck = clock({ before: () => { if (xc >= P.x[1] - 1e-6) xc = P.x[0]; }, tick: (dt) => { xc = Math.min(P.x[1], xc + dt * (P.x[1] - P.x[0]) / 7); sx.set(xc); draw(); return xc < P.x[1]; }, jump: () => { xc = Math.min(P.x[1], xc + (P.x[1] - P.x[0]) / 6); sx.set(xc); draw(); } });
    ui.controls.append(seg.el, sx.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "f", label: "$f(x)$" }, { key: "d", label: L.slope, c: "orange" }]);
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
    const Y = (hh) => 290 - hh * 12.5;
    el("line", { x1: 10, x2: 150, y1: 290, y2: 290, class: "s-ink", "stroke-width": 2.5 }, svg);
    for (let k = 0; k <= 20; k += 5) { el("line", { x1: 18, x2: 26, y1: Y(k), y2: Y(k), class: "s-ink" }, svg); el("text", { x: 14, y: Y(k) + 4, "text-anchor": "end", class: "fv-text dm-small" }, svg, String(k)); }
    const trail = el("g", {}, svg), ball = el("circle", { cx: 80, r: 10, class: "fill-orange" }, svg), arrow = el("g", { class: "s-blue fill-blue" }, svg);
    const mk = (y, lab) => new FV.Plot(c2, { x: [0, 4], y, aspect: 0.32, maxHeight: 150, minHeight: 110, xLabel: L.tsec, title: lab });
    const ph = mk([-1, 22], L.hgt), pv = mk([-22, 22], L.vel), pa = mk([-12, 2], L.acc);
    const stt = FV.ui.slider({ label: L.tsec, min: 0, max: 4, step: 0.01, value: t, oninput: (x) => { ck.stop(); t = x; draw(); } });
    const ck = clock({ before: () => { if (t >= 4) t = 0; }, tick: (d) => { t = Math.min(4, t + d * 0.8); stt.set(t); draw(); return t < 4; }, jump: () => { t = t >= 4 ? 0 : Math.min(4, t + 0.5); stt.set(t); draw(); } });
    ui.controls.append(stt.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "h", label: L.hgt, c: "orange" }, { key: "v", label: L.vel, c: "blue" }, { key: "a", label: L.acc, c: "red" }]);
    function draw() {
      const hh = h(t), vv = v(t);
      ball.setAttribute("cy", Y(hh));
      trail.textContent = "";
      for (let s = 0; s < t; s += 0.25) el("circle", { cx: 80, cy: Y(h(s)), r: 2.5, class: "fill-faint" }, trail);
      arrow.textContent = "";
      if (Math.abs(vv) > 0.3) {
        const y1 = Y(hh), y2 = y1 - vv * 3.2, dir = Math.sign(y2 - y1);
        el("line", { x1: 112, x2: 112, y1, y2: y2 - dir * 6, "stroke-width": 3 }, arrow);
        el("path", { d: `M112 ${y2}l-6 ${-dir * 9}h12z` }, arrow);
      }
      [[ph, h, "orange"], [pv, v, "blue"], [pa, () => -10, "red"]].forEach(([p, f, c]) => { p.clear(); p.fn(f, { c, w: 2.2 }); p.vline(t); p.dot(t, f(t), { c }); });
      ph.line(Math.max(0, t - 0.6), hh - vv * Math.min(0.6, t), Math.min(4, t + 0.6), hh + vv * Math.min(0.6, 4 - t), { c: "blue", w: 1.6, dash: true });
      pv.line(Math.max(0, t - 0.6), vv + 10 * Math.min(0.6, t), Math.min(4, t + 0.6), vv - 10 * Math.min(0.6, 4 - t), { c: "red", w: 1.6, dash: true });
      ro.set("h", n(hh, 3)); ro.set("v", n(vv, 3)); ro.set("a", "−10");
      note(L.ballNote(tn(t, 3), tn(hh, 3), tn(vv, 3)));
    }
    ph.onresize = pv.onresize = pa.onresize = draw;
    draw();
  });

  // ---------- 7. gears: the chain rule ----------
  FV.widget("dm-gears", (root) => {
    const ui = FV.shell(root), note = noter(ui);
    let k1 = 2, k2 = 1.5, th = 0;
    const svg = scene(ui.stage, 720, 280, "x → u → y");
    const g = el("g", {}, svg);
    const s1 = FV.ui.slider({ label: L.k1, min: 0.5, max: 3, step: 0.5, value: k1, oninput: (v) => { k1 = v; th = 0; layout(); draw(); } });
    const s2 = FV.ui.slider({ label: L.k2, min: 0.5, max: 3, step: 0.5, value: k2, oninput: (v) => { k2 = v; th = 0; layout(); draw(); } });
    const ck = clock({ tick: (d) => { th += d * 0.6; draw(); return true; }, jump: () => { th += 0.25; draw(); } });
    ui.controls.append(s1.el, s2.el, ck.el);
    const ro = FV.ui.readout(ui.readout, [{ key: "x", label: L.turnsX }, { key: "u", label: L.turnsU, c: "teal" }, { key: "y", label: L.turnsY, c: "orange" }, { key: "k", label: "$\\frac{dy}{dx}$", c: "blue" }]);
    let G = [];
    function gearPath(r, teeth) {
      let d = "";
      const tw = (Math.PI * 2) / teeth;
      for (let i = 0; i < teeth; i++) {
        const a = i * tw;
        [[a, r - 6], [a + tw * 0.15, r + 6], [a + tw * 0.45, r + 6], [a + tw * 0.6, r - 6]].forEach(([b, rr], j) => { d += (i === 0 && j === 0 ? "M" : "L") + (rr * Math.cos(b)).toFixed(1) + " " + (rr * Math.sin(b)).toFixed(1); });
      }
      return d + "Z";
    }
    function layout() {
      let r1 = 80, r2 = r1 / k1, r3 = r2 / k2;
      const total = 2 * (r1 + r2 + r3) + 24, sc = Math.min(1, 680 / total, 230 / (2 * Math.max(r1, r2, r3) + 12));
      r1 *= sc; r2 *= sc; r3 *= sc;
      const x1 = 360 - (r1 + r2 + r3 + 6) + r1, x2 = x1 + r1 + r2 + 3, x3 = x2 + r2 + r3 + 3;
      G = [[x1, r1, "ink", "x"], [x2, r2, "teal", "u"], [x3, r3, "orange", "y"]].map(([cx, r, c, name]) => ({ cx, r, c, name, teeth: Math.max(6, Math.round(r / 5)) }));
    }
    function draw() {
      g.textContent = "";
      const angs = [th, -th * k1, th * k1 * k2];
      G.forEach((gg, i) => {
        const grp = el("g", { transform: `translate(${gg.cx} 140) rotate(${(angs[i] * 180) / Math.PI + (i === 1 ? 180 / gg.teeth : 0)})` }, g);
        el("path", { d: gearPath(gg.r, gg.teeth), class: "fill-" + gg.c, "fill-opacity": 0.25, stroke: "currentColor", "stroke-width": 2 }, grp).setAttribute("class", "s-" + gg.c + " fill-" + gg.c);
        el("line", { x1: 0, y1: 0, x2: gg.r - 10, y2: 0, class: "s-" + gg.c, "stroke-width": 3 }, grp);
        el("circle", { r: 5, class: "fill-" + gg.c }, grp);
        el("text", { x: gg.cx, y: 140 + gg.r + 26, "text-anchor": "middle", class: "fv-text t-" + gg.c }, g, gg.name);
      });
      const turns = th / (2 * Math.PI);
      ro.set("x", n(turns, 3)); ro.set("u", n(turns * k1, 3)); ro.set("y", n(turns * k1 * k2, 3)); ro.set("k", n(k1 * k2, 3));
      note(L.gearsNote(tn(k1, 3), tn(k2, 3), tn(k1 * k2, 3)));
    }
    layout(); draw();
  });
})();
