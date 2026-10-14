/* Interactive figures for "Анатомия сигмоиды".
   Plain canvas, no dependencies. Colors come from CSS custom properties
   so the figures follow light/dark mode. */
(function () {
  "use strict";

  const sig = (x) => 1 / (1 + Math.exp(-x));
  const dsig = (x) => { const s = sig(x); return s * (1 - s); };
  const token = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const FONT = '"Figtree", "Helvetica Neue", Helvetica, Arial, sans-serif';
  const fmtSmall = (v) => (v < 1e-3 ? v.toExponential(1).replace("e-", " × 10⁻") : v.toFixed(4));

  function setupCanvas(el) {
    // Render at device pixel ratio for crisp lines; CSS keeps it responsive.
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = el.width, h = el.height;
    el.width = w * dpr; el.height = h * dpr;
    el.style.aspectRatio = `${w} / ${h}`;
    const ctx = el.getContext("2d");
    ctx.scale(dpr, dpr);
    return { ctx, W: w, H: h };
  }

  /* ---------- Figure 1: the two asymptotes ---------- */
  const fig1 = document.getElementById("fig-asymptotes");
  const rangeInput = document.getElementById("range");
  const rangeOut = document.getElementById("range-out");

  function drawAsymptotes() {
    if (!fig1) return;
    const { ctx, W, H } = fig1._c || (fig1._c = setupCanvas(fig1));
    const R = Number(rangeInput.value);
    rangeOut.value = "±" + R;

    const fg = token("--fg"), fg2 = token("--fg-2"), rule = token("--rule"), accent = token("--accent"), bg = token("--bg");
    const L = 110, RR = 40, T = 80, B = 96;
    const px = (x) => L + ((x + R) / (2 * R)) * (W - L - RR);
    const py = (y) => H - B - y * (H - T - B);

    ctx.clearRect(0, 0, W, H);

    // quiet grid
    ctx.strokeStyle = rule; ctx.lineWidth = 1;
    [0.25, 0.5, 0.75].forEach((v) => { ctx.beginPath(); ctx.moveTo(L, py(v)); ctx.lineTo(W - RR, py(v)); ctx.stroke(); });

    ctx.fillStyle = fg2; ctx.font = `400 28px ${FONT}`; ctx.textAlign = "right"; ctx.textBaseline = "middle";
    [0.25, 0.5, 0.75].forEach((v) => ctx.fillText(v.toFixed(2), L - 22, py(v)));
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    const step = R <= 8 ? 2 : R <= 20 ? 5 : 10;
    for (let x = -R; x <= R; x += step) ctx.fillText(String(x), px(x), H - B + 22);

    // asymptotes: the only red on the page
    ctx.strokeStyle = accent; ctx.lineWidth = 2;
    [0, 1].forEach((v) => { ctx.beginPath(); ctx.moveTo(L, py(v)); ctx.lineTo(W - RR, py(v)); ctx.stroke(); });
    ctx.fillStyle = accent; ctx.font = `500 28px ${FONT}`; ctx.textAlign = "left";
    ctx.textBaseline = "bottom"; ctx.fillText("y = 1", L, py(1) - 10);
    ctx.textBaseline = "top"; ctx.fillText("y = 0", L, py(0) + 10);
    ctx.textAlign = "right"; ctx.textBaseline = "middle";
    ctx.fillText("1", L - 22, py(1)); ctx.fillText("0", L - 22, py(0));

    // the curve
    ctx.strokeStyle = fg; ctx.lineWidth = 4; ctx.lineJoin = "round"; ctx.beginPath();
    const N = 600;
    for (let i = 0; i <= N; i++) {
      const x = -R + (2 * R * i) / N;
      const X = px(x), Y = py(sig(x));
      i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y);
    }
    ctx.stroke();

    // gap markers at the edges
    const xr = R * 0.9, xl = -R * 0.9;
    const gapR = 1 - sig(xr), gapL = sig(xl);
    ctx.strokeStyle = fg2; ctx.lineWidth = 1; ctx.setLineDash([3, 4]);
    ctx.beginPath(); ctx.moveTo(px(xr), py(1)); ctx.lineTo(px(xr), py(sig(xr))); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(px(xl), py(0)); ctx.lineTo(px(xl), py(sig(xl))); ctx.stroke();
    ctx.setLineDash([]);

    const label = (text, x, y, align) => {
      ctx.font = `400 26px ${FONT}`; ctx.textAlign = align; ctx.textBaseline = "middle";
      const w = ctx.measureText(text).width + 20;
      const bx = align === "right" ? x - w : x;
      ctx.fillStyle = bg; ctx.fillRect(bx, y - 18, w, 36);
      ctx.fillStyle = fg2; ctx.fillText(text, align === "right" ? x - 6 : x + 6, y);
    };
    label("щель " + fmtSmall(gapR), px(xr) - 8, py(1) + Math.max(40, (py(sig(xr)) - py(1)) / 2), "right");
    label("щель " + fmtSmall(gapL), px(xl) + 8, py(0) - Math.max(40, (py(0) - py(sig(xl))) / 2), "left");
  }

  /* ---------- Figure 2: slope and the inflection point ---------- */
  const fig2 = document.getElementById("fig-slope");
  const posInput = document.getElementById("pos");
  const posOut = document.getElementById("pos-out");
  const sigOut = document.getElementById("sig-out");
  const slopeOut = document.getElementById("slope-out");

  function drawSlope() {
    if (!fig2) return;
    const { ctx, W, H } = fig2._c || (fig2._c = setupCanvas(fig2));
    const x = Number(posInput.value), s = sig(x), d = dsig(x);
    posOut.value = x.toFixed(1);
    sigOut.textContent = s.toFixed(4);
    slopeOut.textContent = d.toFixed(4);

    const fg = token("--fg"), fg2 = token("--fg-2"), rule = token("--rule"), accent = token("--accent"), soft = token("--chart-soft"), bg = token("--bg");
    const R = 6, L = 110, RR = 40;
    const top = { y0: 48, y1: 520 }, bot = { y0: 600, y1: 840 };
    const px = (v) => L + ((v + R) / (2 * R)) * (W - L - RR);
    const pyT = (y) => top.y1 - y * (top.y1 - top.y0);
    const pyB = (v) => bot.y1 - (v / 0.25) * (bot.y1 - bot.y0);

    ctx.clearRect(0, 0, W, H);

    // top panel: asymptotes, thin
    ctx.strokeStyle = accent; ctx.lineWidth = 1.5;
    [0, 1].forEach((v) => { ctx.beginPath(); ctx.moveTo(L, pyT(v)); ctx.lineTo(W - RR, pyT(v)); ctx.stroke(); });
    ctx.strokeStyle = rule; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(L, pyT(0.5)); ctx.lineTo(W - RR, pyT(0.5)); ctx.stroke();

    ctx.fillStyle = fg2; ctx.font = `400 28px ${FONT}`; ctx.textAlign = "right"; ctx.textBaseline = "middle";
    ctx.fillText("1", L - 22, pyT(1)); ctx.fillText("0.5", L - 22, pyT(0.5)); ctx.fillText("0", L - 22, pyT(0));
    ctx.fillText("0.25", L - 22, pyB(0.25)); ctx.fillText("0", L - 22, pyB(0));
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    for (let v = -R; v <= R; v += 1) ctx.fillText(String(v), px(v), bot.y1 + 22);

    // convexity regions, barely there
    ctx.fillStyle = fg; ctx.globalAlpha = 0.035;
    ctx.fillRect(px(0), top.y0, W - RR - px(0), top.y1 - top.y0);
    ctx.globalAlpha = 1;
    ctx.fillStyle = fg2; ctx.font = `400 26px ${FONT}`; ctx.textAlign = "center"; ctx.textBaseline = "top";
    ctx.fillText("выпукла вниз", (L + px(0)) / 2, top.y0 + 4);
    ctx.fillText("выпукла вверх", (px(0) + W - RR) / 2, top.y0 + 4);

    // bottom panel: derivative as area + line
    ctx.beginPath();
    const N = 400;
    for (let i = 0; i <= N; i++) {
      const v = -R + (2 * R * i) / N;
      const X = px(v), Y = pyB(dsig(v));
      i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y);
    }
    ctx.lineTo(px(R), bot.y1); ctx.lineTo(px(-R), bot.y1); ctx.closePath();
    ctx.fillStyle = soft; ctx.globalAlpha = 0.45; ctx.fill(); ctx.globalAlpha = 1;
    ctx.strokeStyle = fg2; ctx.lineWidth = 1.5; ctx.beginPath();
    for (let i = 0; i <= N; i++) {
      const v = -R + (2 * R * i) / N;
      const X = px(v), Y = pyB(dsig(v));
      i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y);
    }
    ctx.stroke();
    ctx.fillStyle = fg2; ctx.font = `500 28px ${FONT}`; ctx.textAlign = "left"; ctx.textBaseline = "bottom";
    ctx.fillText("σ′(x)", L, bot.y0 - 8);
    ctx.fillText("σ(x)", L, top.y0 - 8);

    // main curve
    ctx.strokeStyle = fg; ctx.lineWidth = 4; ctx.lineJoin = "round"; ctx.beginPath();
    for (let i = 0; i <= N; i++) {
      const v = -R + (2 * R * i) / N;
      const X = px(v), Y = pyT(sig(v));
      i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y);
    }
    ctx.stroke();

    // inflection point: dashed vertical through both panels, hollow dot
    ctx.strokeStyle = fg2; ctx.lineWidth = 1; ctx.setLineDash([3, 5]);
    ctx.beginPath(); ctx.moveTo(px(0), top.y0); ctx.lineTo(px(0), bot.y1); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = bg; ctx.strokeStyle = fg; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.arc(px(0), pyT(0.5), 8, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    ctx.fillStyle = fg; ctx.font = `400 26px ${FONT}`; ctx.textAlign = "left"; ctx.textBaseline = "middle";
    ctx.fillText("точка перегиба (0, 0.5)", px(0) + 26, pyT(0.5) + 44);

    // tangent at the chosen point
    const span = 1.5;
    ctx.strokeStyle = fg; ctx.lineWidth = 1.5; ctx.beginPath();
    ctx.moveTo(px(x - span), pyT(s - d * span)); ctx.lineTo(px(x + span), pyT(s + d * span)); ctx.stroke();

    // link to derivative panel + dots
    ctx.strokeStyle = fg2; ctx.lineWidth = 1; ctx.setLineDash([2, 4]);
    ctx.beginPath(); ctx.moveTo(px(x), pyT(s)); ctx.lineTo(px(x), pyB(d)); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = fg;
    ctx.beginPath(); ctx.arc(px(x), pyT(s), 7, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(px(x), pyB(d), 5, 0, Math.PI * 2); ctx.fill();
  }

  /* ---------- wiring ---------- */
  const drawAll = () => { drawAsymptotes(); drawSlope(); };
  rangeInput && rangeInput.addEventListener("input", drawAsymptotes);
  posInput && posInput.addEventListener("input", drawSlope);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(drawAll);
  const mq = window.matchMedia("(prefers-color-scheme: dark)");
  mq.addEventListener ? mq.addEventListener("change", drawAll) : mq.addListener(drawAll);
  new MutationObserver(drawAll).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  drawAll();
})();
