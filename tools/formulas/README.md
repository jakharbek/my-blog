# Страницы формул

Каждая формула шпаргалки (`tools/content_formulas.py`) может иметь подробную страницу
`/<lang>/materials/ml-formulas/<id>/`. Страница состоит из двух файлов:

```
tools/formulas/<id>.py          тексты на трёх языках: META и SECTIONS
assets/js/formulas/<id>.js      интерактивные рисунки этой страницы (на FV из assets/js/viz.js)
```

`<id>` совпадает с `id` карточки в `content_formulas.py`. Образец — `sigmoid.py` и `assets/js/formulas/sigmoid.js`.

```
python3 tools/build.py --only <id>   # собрать одну страницу (ru, en, uz)
python3 tools/build.py               # собрать весь сайт; на карточках шпаргалки появятся ссылки «Полный разбор →»
```

## META

```python
META = dict(
    id="sigmoid", date="2026-10-28", minutes=30,
    hero=r"\sigma(x)=\frac{1}{1+e^{-x}}",           # главная формула, TeX
    title={"ru": …, "en": …, "uz": …},               # заголовок h1
    dek={…},                                          # подзаголовок, 2–3 предложения
    description={…},                                  # meta description, одна фраза
)
```

## SECTIONS

`SECTIONS = {"ru": [section, …], "en": […], "uz": […]}` — у всех языков одинаковая структура.
`section = dict(id="why", title="…", blocks=[…])`; разделы попадают в оглавление с номерами.

Блоки (кортежи):

| Блок | Что даёт |
|---|---|
| `("p", html)` | абзац; формулы в тексте — `$…$` (KaTeX), `<b>`, `<i>`, `<a href="../tanh/">` |
| `("h3", text)` | подзаголовок внутри раздела |
| `("eq", tex)` | выключная формула |
| `("symbols", [(tex, html), …])` | расшифровка обозначений |
| `("viz", "имя-виджета", {config}, caption_html)` | интерактивный рисунок; подпись начинается с `<b>Рисунок N.</b>` |
| `("callout", kind, title или None, html)` | выноска: `key`, `intuition`, `warn`, `note`, `history` |
| `("code", "python", src)` | листинг (экранируется автоматически) |
| `("table", [заголовки], [[ячейки], …], {"num": [индексы числовых столбцов]})` | таблица |
| `("ul", [html, …])`, `("ol", […])` | списки |
| `("deep", summary, [блоки])` | сворачиваемый блок «глубже» (выводы, доказательства) |
| `("quiz", [dict(q, options, answer, explain), …])` | тест «Проверь себя»; `answer` — индекс верного варианта |

Правила текста:
* русский — основной; английский и узбекский (латиница, `o‘`, `g‘`, `’`) — полноценные переводы, не сокращения;
* в ru и uz десятичная запятая в TeX пишется `0{,}5`, в en — `0.5`; координаты в ru/uz — `(1;\,2)`;
* в HTML-тексте (`p`, списки, подписи, выноски, тест) вместо `<` и `>` пишите `&lt;` и `&gt;`, в том числе внутри `$…$`;
  а в чистом TeX (`eq`, `symbols`, `META["hero"]`) — обычные `<` и `>`: генератор экранирует их сам;
* каждое число в тексте и подписях проверено вычислением и совпадает с тем, что показывает рисунок.

Рекомендуемые разделы: зачем нужна → интуиция (первый рисунок) → формула по косточкам → свойства →
производная (вывод в `deep`) → многомерная / 3D-картина → как работает в обучении (симуляция) →
код (NumPy, PyTorch, устойчивость) → частые ошибки → связи с другими формулами → итоги → проверь себя.

## Виджеты (FV)

```js
(function () {
  const L = { ru: {…}, en: {…}, uz: {…} }[FV.lang];      // подписи внутри рисунка — на трёх языках
  FV.widget("tanh-explorer", (el, cfg) => {
    const w = FV.shell(el, {});                          // { stage, controls, readout, note }
    const p = new FV.Plot(w.stage, { x: [-4, 4], y: [-1.2, 1.2], xLabel: "x", yLabel: "tanh x" });
    const s = FV.ui.slider({ label: "$x$", min: -4, max: 4, step: 0.05, value: 1, oninput: draw });
    w.controls.append(s.el);
    const ro = FV.ui.readout(w.readout, [{ key: "y", label: "tanh x =", c: "blue" }]);
    function draw() { p.clear(); p.fn(Math.tanh, { c: "blue" }); p.dot(s.value, Math.tanh(s.value)); ro.set("y", FV.fmt(Math.tanh(s.value), 4)); }
    p.onresize = draw; draw();
  });
})();
```

* `FV.Plot(parent, {x, y, xType/yType: "log", xLabel, yLabel, aspect, equal, xTicks, yTicks, title})`:
  `clear, fn, path, line, vline, hline, area, rect, bar, dot, text, arrow, heat (тепловая карта), contours,
  hover(cb), hl(…) (рисовать в слое наведения), handle(x, y, {onDrag, onChange}) (перетаскиваемая точка),
  legend([{label, c, dash, dot, box}]), setDomain`. После `clear()` перерисовывайте всё; `p.onresize = draw`.
* `FV.Surface(parent, {f, x, y, z, n, labels:{x,y,z}, cmap, azimuth, elevation, title})` — 3D-поверхность
  с вращением мышью/пальцем: `setF, setDomain, setPaths([{pts:[[x,y,z],…], c}]), setPoints([{x,y,z,c,label}]), setPlanes`.
* Колонки: `FV.shell(el, {cols: true})` и `FV.col(w.stage)`.
* Контролы: `FV.ui.slider, seg, check, button, player({onstep, onreset, interval}), readout`.
* Цвета серий `c`: `ink, blue, orange, teal, red, violet, faint, guide`; карты цветов: `viridis, magma, blues, diverging`.
* Числа: `FV.fmt(v, d)` (запятая в ru/uz), `FV.num(v, sig)`; детерминированный ГПСЧ `FV.rng(seed)` (`.normal()`);
  `FV.sigmoid, FV.erf, FV.Phi, FV.phi`.
* Подписи с формулами: `FV.rich("Вес $w$")`, `FV.tex(src)`.
