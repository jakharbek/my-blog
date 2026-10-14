#!/usr/bin/env python3
"""Generate the three language versions of the site from one set of templates.

Run from the repository root:  python3 tools/build.py
Output is committed, so GitHub Pages needs no build step.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["ru", "uz", "en"]
DATE_ISO = "2026-10-14"

SITE = {
    "ru": dict(
        title="Javharbek — заметки о машинном обучении",
        description="Заметки о машинном обучении, инфраструктуре и математике.",
        nav_blog="Блог", nav_about="Обо мне", nav_sections="Разделы", nav_lang="Язык",
        hero_h1="Машинное обучение, объяснённое до конца",
        hero_p="Заметки инженера о математике под капотом моделей, инфраструктуре и кредитной аналитике.",
        date="14 октября 2026",
        post_title="Анатомия сигмоиды",
        post_blurb="Две горизонтальные асимптоты и одна точка перегиба: что они значат для нейросети и почему 0.5 стал порогом решения. С интерактивными графиками.",
        lang_name="Русский",
    ),
    "uz": dict(
        title="Javharbek — mashinaviy o‘rganish haqida yozuvlar",
        description="Mashinaviy o‘rganish, infratuzilma va matematika haqida yozuvlar.",
        nav_blog="Blog", nav_about="Men haqimda", nav_sections="Bo‘limlar", nav_lang="Til",
        hero_h1="Mashinaviy o‘rganish, oxirigacha tushuntirilgan",
        hero_p="Modellar ostidagi matematika, infratuzilma va kredit tahlili haqida muhandis yozuvlari.",
        date="2026-yil 14-oktabr",
        post_title="Sigmoidaning anatomiyasi",
        post_blurb="Ikki gorizontal asimptota va bitta burilish nuqtasi: ular neyron tarmoq uchun nimani anglatadi va nega 0.5 qaror chegarasiga aylandi. Interaktiv grafiklar bilan.",
        lang_name="O‘zbekcha",
    ),
    "en": dict(
        title="Javharbek — notes on machine learning",
        description="Notes on machine learning, infrastructure and mathematics.",
        nav_blog="Blog", nav_about="About", nav_sections="Sections", nav_lang="Language",
        hero_h1="Machine learning, explained all the way down",
        hero_p="An engineer's notes on the mathematics under the models, infrastructure and credit analytics.",
        date="14 October 2026",
        post_title="Anatomy of the sigmoid",
        post_blurb="Two horizontal asymptotes and a single inflection point: what they mean for a neural network and why 0.5 became the decision threshold. With interactive figures.",
        lang_name="English",
    ),
}

ARTICLE = {
"ru": dict(
    meta_desc="Две горизонтальные асимптоты и единственная точка перегиба: что они значат в контексте сигмоидной функции и нейросетей. С интерактивными графиками.",
    dek="У функции σ(x) = 1 / (1 + e<sup>−x</sup>) две горизонтальные асимптоты и одна точка перегиба. Это не два сухих факта из учебника, а всё, что нужно знать о том, почему она работает в нейросети и где ломается.",
    h_road="Дорога между полом и потолком",
    p_road1="Проще всего думать о сигмоиде как о дороге. Внизу пол на высоте 0, вверху потолок на высоте 1. Дорога идёт слева направо: сначала лежит почти на полу, потом плавно поднимается и ложится почти под потолок.",
    p_road2="Главное слово здесь «почти». Дорога подходит к полу и потолку сколь угодно близко, но никогда их не касается. Линия, к которой кривая бесконечно приближается и которой никогда не достигает, называется асимптотой. У сигмоиды таких линий две, обе горизонтальные: <span class=\"red\">y = 0</span> при x → −∞ и <span class=\"red\">y = 1</span> при x → +∞.",
    fig1_aria="Сигмоида между асимптотами y = 0 и y = 1",
    fig1_label="Диапазон x", fig1_aria_input="Диапазон оси x",
    fig1_cap="Расширяйте диапазон. Кривая всё плотнее прижимается к асимптотам, но щель между ними остаётся при любом x.",
    p_table="Насколько маленькой становится эта щель, видно по числам.",
    p_never="На x = 100 до единицы не хватает числа с сорока тремя нулями после запятой. Но это всё ещё не ноль, и не станет им ни при каком x. Вот это «никогда» и есть содержание слова «асимптота».",
    h_steep="Самое крутое место",
    p_steep1="Теперь пройдём по дороге пешком. Слева она почти плоская. Затем подъём становится всё круче и круче, достигает максимума ровно посередине, в точке x = 0 на высоте 0.5, и дальше снова выравнивается.",
    p_steep2="Место, где «всё круче» сменяется на «всё положе», называется точкой перегиба. Формально там меняется знак второй производной: слева кривая выпукла вниз, справа выпукла вверх. У сигмоиды такое место ровно одно, поэтому вся кривая состоит из одного плавного S-движения без ступенек и плато посередине.",
    fig2_aria="Крутизна сигмоиды и график её производной",
    fig2_label="Положение x", fig2_aria_input="Положение точки на кривой",
    fig2_cap="Чёрный отрезок — касательная в выбранной точке. Внизу — производная σ′(x) = σ(x)(1 − σ(x)); её максимум 0.25 стоит ровно под точкой перегиба.",
    p_deriv="Производная тут удивительно удобна. Она выражается через саму функцию: <span class=\"formula\">σ′ = σ(1 − σ)</span>. Это значит, что при обратном распространении ошибки не нужно заново считать экспоненту, достаточно значения, которое сеть уже вычислила на прямом проходе.",
    h_nn="Что это значит для нейросети",
    p_nn0="Внутри сети нейрон на выходе получает произвольное число: −50, 3, 1000. Для бинарной классификации нужен ответ в виде вероятности от 0 до 1. Сигмоида берёт любое число и укладывает его на дорогу между полом и потолком.",
    p_nn1="<strong>Асимптоты дают ограниченность.</strong> Выход всегда строго между 0 и 1, поэтому его можно читать как вероятность. Это же свойство и главный недостаток: на плоских участках большие входы перестают различаться. σ(10) и σ(100) отличаются в пятом знаке, производная там практически ноль. Если активации уходят в хвосты, градиент через них не проходит, и веса перестают обучаться. Это и есть затухающий градиент, причина, по которой сигмоида ушла из скрытых слоёв глубоких сетей.",
    p_nn2="<strong>Точка перегиба даёт порог.</strong> x = 0 и σ = 0.5 — середина между «нет» и «да». Здесь производная максимальна, а значит, сеть наиболее чувствительна: небольшой сдвиг входа заметно меняет выход. В логистической регрессии граница решения w·x + b = 0 отображается ровно в эту точку. Поэтому 0.5 и стал стандартным порогом.",
    p_nn3="<strong>Единственность перегиба даёт один переход.</strong> Кривая монотонна и не имеет промежуточных полок, поэтому между «нет» и «да» есть ровно одна граница, а не несколько.",
    h_sum="Коротко",
    sum=[
        "Две горизонтальные асимптоты, 0 и 1: выход всегда можно читать как вероятность, но в хвостах функция насыщается и градиент затухает.",
        "Одна точка перегиба в (0, 0.5): максимальная чувствительность, естественный порог решения и единственная граница между классами.",
        "Производная выражается через саму функцию, σ′ = σ(1 − σ), что делает обратное распространение дешёвым.",
        "Для сравнения, у tanh те же свойства, но асимптоты −1 и 1, перегиб в начале координат и наклон 1 вместо 0.25, поэтому в скрытых слоях она обучается быстрее. Сигмоида осталась там, где нужна именно вероятность: на выходе бинарного классификатора.",
    ],
),
"uz": dict(
    meta_desc="Ikki gorizontal asimptota va yagona burilish nuqtasi: ular sigmoida funksiyasi va neyron tarmoqlar kontekstida nimani anglatadi. Interaktiv grafiklar bilan.",
    dek="σ(x) = 1 / (1 + e<sup>−x</sup>) funksiyasining ikkita gorizontal asimptotasi va bitta burilish nuqtasi bor. Bu darslikdagi ikki quruq fakt emas, balki u neyron tarmoqda nega ishlashi va qayerda buzilishi haqida bilish kerak bo‘lgan hamma narsa.",
    h_road="Pol va shift orasidagi yo‘l",
    p_road1="Sigmoidani yo‘l deb tasavvur qilish eng oson. Pastda 0 balandlikdagi pol, tepada 1 balandlikdagi shift. Yo‘l chapdan o‘ngga boradi: avval deyarli polda yotadi, so‘ng silliq ko‘tarilib deyarli shift ostiga yotadi.",
    p_road2="Bu yerda asosiy so‘z «deyarli». Yo‘l polga ham, shiftga ham istalgancha yaqinlashadi, lekin hech qachon ularga tegmaydi. Egri chiziq cheksiz yaqinlashadigan, ammo hech qachon yetib bormaydigan chiziq asimptota deb ataladi. Sigmoidada bunday chiziq ikkita, ikkalasi ham gorizontal: x → −∞ da <span class=\"red\">y = 0</span> va x → +∞ da <span class=\"red\">y = 1</span>.",
    fig1_aria="y = 0 va y = 1 asimptotalar orasidagi sigmoida",
    fig1_label="x oralig‘i", fig1_aria_input="x o‘qi oralig‘i",
    fig1_cap="Oraliqni kengaytiring. Egri chiziq asimptotalarga tobora zichroq yopishadi, lekin ular orasidagi oraliq istalgan x da saqlanib qoladi.",
    p_table="Bu oraliq qanchalik kichik bo‘lishi raqamlarda ko‘rinadi.",
    p_never="x = 100 da birgacha verguldan keyin qirq uchta nol bo‘lgan son yetmaydi. Lekin bu hali ham nol emas va hech qanday x da nol bo‘lmaydi. Ana shu «hech qachon» — «asimptota» so‘zining mazmuni.",
    h_steep="Eng tik joy",
    p_steep1="Endi yo‘l bo‘ylab piyoda yuramiz. Chapda u deyarli tekis. Keyin ko‘tarilish tobora tikroq bo‘lib boradi, aynan o‘rtada, x = 0 nuqtada 0.5 balandlikda maksimumga yetadi va yana tekislanadi.",
    p_steep2="«Tobora tikroq» «tobora yotiqroq»ga almashadigan joy burilish nuqtasi deb ataladi. Rasman u yerda ikkinchi hosilaning ishorasi o‘zgaradi: chapda egri chiziq pastga qavariq, o‘ngda yuqoriga qavariq. Sigmoidada bunday joy aynan bitta, shuning uchun butun egri chiziq zinapoyasiz va o‘rtada tekisliksiz bitta silliq S-harakatdan iborat.",
    fig2_aria="Sigmoidaning tikligi va hosilasining grafigi",
    fig2_label="x holati", fig2_aria_input="Egri chiziqdagi nuqta holati",
    fig2_cap="Qora kesma — tanlangan nuqtadagi urinma. Pastda — σ′(x) = σ(x)(1 − σ(x)) hosilasi; uning maksimumi 0.25 aynan burilish nuqtasi ostida turadi.",
    p_deriv="Bu yerda hosila hayratlanarli darajada qulay. U funksiyaning o‘zi orqali ifodalanadi: <span class=\"formula\">σ′ = σ(1 − σ)</span>. Demak, xatoni teskari tarqatishda eksponentani qayta hisoblash shart emas, tarmoq to‘g‘ri o‘tishda allaqachon hisoblagan qiymat kifoya.",
    h_nn="Bu neyron tarmoq uchun nimani anglatadi",
    p_nn0="Tarmoq ichida chiqishdagi neyron ixtiyoriy sonni oladi: −50, 3, 1000. Binar tasniflash uchun 0 dan 1 gacha ehtimollik ko‘rinishidagi javob kerak. Sigmoida istalgan sonni olib, uni pol va shift orasidagi yo‘lga joylaydi.",
    p_nn1="<strong>Asimptotalar chegaralanganlik beradi.</strong> Chiqish har doim qat’iy 0 va 1 orasida, shuning uchun uni ehtimollik sifatida o‘qish mumkin. Xuddi shu xususiyat asosiy kamchilik hamdir: tekis qismlarda katta kirishlar farqlanmay qoladi. σ(10) va σ(100) beshinchi raqamda farq qiladi, hosila u yerda deyarli nol. Aktivatsiyalar dumlarga ketsa, gradient ulardan o‘tmaydi va vaznlar o‘rganishni to‘xtatadi. Bu so‘nuvchi gradient — sigmoida chuqur tarmoqlarning yashirin qatlamlaridan ketganining sababi.",
    p_nn2="<strong>Burilish nuqtasi chegara beradi.</strong> x = 0 va σ = 0.5 — «yo‘q» va «ha» o‘rtasidagi o‘rta nuqta. Bu yerda hosila maksimal, demak tarmoq eng sezgir: kirishning kichik siljishi chiqishni sezilarli o‘zgartiradi. Logistik regressiyada w·x + b = 0 qaror chegarasi aynan shu nuqtaga tushadi. Shuning uchun 0.5 standart chegaraga aylandi.",
    p_nn3="<strong>Burilishning yagonaligi bitta o‘tish beradi.</strong> Egri chiziq monoton va oraliq tekisliklarsiz, shuning uchun «yo‘q» va «ha» orasida bir nechta emas, aynan bitta chegara bor.",
    h_sum="Qisqacha",
    sum=[
        "Ikki gorizontal asimptota, 0 va 1: chiqishni har doim ehtimollik sifatida o‘qish mumkin, lekin dumlarda funksiya to‘yinadi va gradient so‘nadi.",
        "(0, 0.5) dagi bitta burilish nuqtasi: maksimal sezgirlik, tabiiy qaror chegarasi va sinflar orasidagi yagona chegara.",
        "Hosila funksiyaning o‘zi orqali ifodalanadi, σ′ = σ(1 − σ), bu teskari tarqatishni arzon qiladi.",
        "Taqqoslash uchun, tanh da xuddi shu xususiyatlar, lekin asimptotalar −1 va 1, burilish koordinata boshida va qiyalik 0.25 o‘rniga 1, shuning uchun yashirin qatlamlarda u tezroq o‘rganadi. Sigmoida aynan ehtimollik kerak bo‘lgan joyda qoldi: binar tasniflagich chiqishida.",
    ],
),
"en": dict(
    meta_desc="Two horizontal asymptotes and a single inflection point: what they mean for the sigmoid function and for neural networks. With interactive figures.",
    dek="The function σ(x) = 1 / (1 + e<sup>−x</sup>) has two horizontal asymptotes and one inflection point. These are not two dry textbook facts; they are everything you need to know about why it works inside a neural network and where it breaks.",
    h_road="A road between the floor and the ceiling",
    p_road1="The easiest way to think about the sigmoid is as a road. Below is a floor at height 0, above is a ceiling at height 1. The road runs left to right: it starts almost on the floor, then rises smoothly and settles almost under the ceiling.",
    p_road2="The key word is “almost”. The road comes arbitrarily close to the floor and the ceiling but never touches them. A line that a curve approaches forever without ever reaching is called an asymptote. The sigmoid has two, both horizontal: <span class=\"red\">y = 0</span> as x → −∞ and <span class=\"red\">y = 1</span> as x → +∞.",
    fig1_aria="Sigmoid between the asymptotes y = 0 and y = 1",
    fig1_label="Range of x", fig1_aria_input="Range of the x axis",
    fig1_cap="Widen the range. The curve hugs the asymptotes ever more tightly, but the gap between them remains for every x.",
    p_table="The numbers show just how small that gap becomes.",
    p_never="At x = 100 the distance to one is a number with forty-three zeros after the decimal point. But it is still not zero, and no x will ever make it zero. That “never” is the whole meaning of the word “asymptote”.",
    h_steep="The steepest place",
    p_steep1="Now walk the road. On the left it is almost flat. Then the climb gets steeper and steeper, peaks exactly in the middle, at x = 0 and height 0.5, and levels off again.",
    p_steep2="The place where “getting steeper” turns into “getting flatter” is called the inflection point. Formally, the second derivative changes sign there: the curve is convex on the left and concave on the right. The sigmoid has exactly one such point, so the whole curve is a single smooth S-shaped move with no steps or plateaus in the middle.",
    fig2_aria="Steepness of the sigmoid and the graph of its derivative",
    fig2_label="Position x", fig2_aria_input="Position of the point on the curve",
    fig2_cap="The black segment is the tangent at the chosen point. Below is the derivative σ′(x) = σ(x)(1 − σ(x)); its maximum of 0.25 sits directly under the inflection point.",
    p_deriv="The derivative is remarkably convenient here. It is expressed through the function itself: <span class=\"formula\">σ′ = σ(1 − σ)</span>. So during backpropagation there is no need to recompute the exponential; the value the network already computed on the forward pass is enough.",
    h_nn="What this means for a neural network",
    p_nn0="Inside the network, an output neuron receives an arbitrary number: −50, 3, 1000. Binary classification needs an answer as a probability between 0 and 1. The sigmoid takes any number and lays it onto the road between the floor and the ceiling.",
    p_nn1="<strong>The asymptotes give boundedness.</strong> The output is always strictly between 0 and 1, so it can be read as a probability. The same property is also the main drawback: on the flat parts, large inputs stop being distinguishable. σ(10) and σ(100) differ in the fifth decimal, and the derivative there is practically zero. When activations drift into the tails, no gradient passes through them and the weights stop learning. This is the vanishing gradient, the reason the sigmoid left the hidden layers of deep networks.",
    p_nn2="<strong>The inflection point gives the threshold.</strong> x = 0 and σ = 0.5 is the midpoint between “no” and “yes”. The derivative is largest there, so the network is most sensitive: a small shift in the input visibly changes the output. In logistic regression the decision boundary w·x + b = 0 maps exactly to this point. That is why 0.5 became the standard threshold.",
    p_nn3="<strong>A single inflection gives a single transition.</strong> The curve is monotonic with no intermediate shelves, so there is exactly one boundary between “no” and “yes”, not several.",
    h_sum="In short",
    sum=[
        "Two horizontal asymptotes, 0 and 1: the output can always be read as a probability, but in the tails the function saturates and the gradient vanishes.",
        "One inflection point at (0, 0.5): maximum sensitivity, a natural decision threshold and a single boundary between classes.",
        "The derivative is expressed through the function itself, σ′ = σ(1 − σ), which makes backpropagation cheap.",
        "For comparison, tanh has the same properties but asymptotes at −1 and 1, an inflection at the origin and a slope of 1 instead of 0.25, so it trains faster in hidden layers. The sigmoid stayed where a probability is exactly what is needed: the output of a binary classifier.",
    ],
),
}

TABLE_ROWS = [
    ("2", "0.8808", "0.12"),
    ("5", "0.9933", "6.7 × 10<sup>−3</sup>"),
    ("10", "0.99995", "4.5 × 10<sup>−5</sup>"),
    ("20", "0.999999998", "2.1 × 10<sup>−9</sup>"),
    ("100", "1 − 3.7 × 10<sup>−44</sup>", "3.7 × 10<sup>−44</sup>"),
]

FONTS = (
    '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&display=swap">\n'
)


def hreflang(path_fn):
    out = []
    for l in LANGS:
        out.append(f'  <link rel="alternate" hreflang="{l}" href="{path_fn(l)}">')
    out.append(f'  <link rel="alternate" hreflang="x-default" href="{path_fn("en")}">')
    return "\n".join(out)


def header(lang, rel, page):
    s = SITE[lang]
    items = []
    for l in LANGS:
        cur = ' aria-current="true"' if l == lang else ""
        items.append(f'<a href="{rel}{l}/{page}" lang="{l}" hreflang="{l}"{cur}>{SITE[l]["lang_name"]}</a>')
    return f"""<header class="site-header">
  <a class="wordmark" href="{rel}{lang}/">Javharbek</a>
  <nav class="site-nav" aria-label="{s['nav_sections']}">
    <a href="{rel}{lang}/">{s['nav_blog']}</a>
    <a href="https://javharbek.uz">{s['nav_about']}</a>
    <a href="https://github.com/jakharbek">GitHub</a>
  </nav>
  <nav class="lang-nav" aria-label="{s['nav_lang']}">
    {' '.join(items)}
  </nav>
</header>"""


FOOTER = """<footer class="site-footer">
  <span>© 2026 Javharbek</span>
  <span><a href="https://javharbek.uz">javharbek.uz</a></span>
</footer>"""


def home(lang):
    s = SITE[lang]
    rel = "../"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{s['title']}</title>
  <meta name="description" content="{s['description']}">
  <meta property="og:title" content="Javharbek">
  <meta property="og:description" content="{s['description']}">
  <meta property="og:type" content="website">
{hreflang(lambda l: f"../{l}/")}
  <link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
{FONTS}  <link rel="stylesheet" href="{rel}assets/css/site.css">
</head>
<body>

{header(lang, rel, "")}

<main>
  <section class="hero">
    <h1>{s['hero_h1']}</h1>
    <p>{s['hero_p']}</p>
  </section>

  <ul class="posts">
    <li class="post-row">
      <time datetime="{DATE_ISO}">{s['date']}</time>
      <a href="sigmoid/">
        <h2>{s['post_title']}</h2>
        <p>{s['post_blurb']}</p>
      </a>
    </li>
  </ul>
</main>

{FOOTER}

<script src="{rel}assets/js/lang.js" defer></script>
</body>
</html>
"""


def article(lang):
    s, a = SITE[lang], ARTICLE[lang]
    rel = "../../"
    rows = "\n".join(f"        <tr><td>{x}</td><td>{y}</td><td>{g}</td></tr>" for x, y, g in TABLE_ROWS)
    summary = "\n".join(f"      <li>{li}</li>" for li in a["sum"])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{s['post_title']} — Javharbek</title>
  <meta name="description" content="{a['meta_desc']}">
  <meta property="og:title" content="{s['post_title']}">
  <meta property="og:description" content="{s['post_blurb']}">
  <meta property="og:type" content="article">
{hreflang(lambda l: f"../../{l}/sigmoid/")}
  <link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
{FONTS}  <link rel="stylesheet" href="{rel}assets/css/site.css">
</head>
<body>

{header(lang, rel, "sigmoid/")}

<main class="article">
  <header class="article-head">
    <time datetime="{DATE_ISO}">{s['date']}</time>
    <h1>{s['post_title']}</h1>
    <p class="dek">{a['dek']}</p>
  </header>

  <h2>{a['h_road']}</h2>
  <p>{a['p_road1']}</p>
  <p>{a['p_road2']}</p>

  <figure class="figure">
    <canvas id="fig-asymptotes" width="1600" height="760" aria-label="{a['fig1_aria']}"></canvas>
    <div class="figure-controls">
      <label>{a['fig1_label']}
        <input type="range" id="range" min="4" max="40" step="1" value="6" aria-label="{a['fig1_aria_input']}">
        <output id="range-out" for="range">±6</output>
      </label>
    </div>
    <p class="figcaption">{a['fig1_cap']}</p>
  </figure>

  <p>{a['p_table']}</p>
  <div class="table-wrap">
    <table class="data">
      <thead><tr><th>x</th><th>σ(x)</th><th>1 − σ(x)</th></tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </div>
  <p>{a['p_never']}</p>

  <h2>{a['h_steep']}</h2>
  <p>{a['p_steep1']}</p>
  <p>{a['p_steep2']}</p>

  <figure class="figure">
    <canvas id="fig-slope" width="1600" height="900" aria-label="{a['fig2_aria']}"></canvas>
    <div class="figure-controls">
      <label>{a['fig2_label']}
        <input type="range" id="pos" min="-6" max="6" step="0.1" value="0" aria-label="{a['fig2_aria_input']}">
        <output id="pos-out" for="pos">0.0</output>
      </label>
      <span>σ(x) = <span class="value" id="sig-out">0.5000</span></span>
      <span>σ′(x) = <span class="value" id="slope-out">0.2500</span></span>
    </div>
    <p class="figcaption">{a['fig2_cap']}</p>
  </figure>

  <p>{a['p_deriv']}</p>

  <h2>{a['h_nn']}</h2>
  <p>{a['p_nn0']}</p>
  <p>{a['p_nn1']}</p>
  <p>{a['p_nn2']}</p>
  <p>{a['p_nn3']}</p>

  <section class="takeaway">
    <h2>{a['h_sum']}</h2>
    <ul>
{summary}
    </ul>
  </section>
</main>

{FOOTER}

<script src="{rel}assets/js/sigmoid.js" defer></script>
</body>
</html>
"""


ROOT_INDEX = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Javharbek</title>
  <meta name="robots" content="noindex">
  <link rel="alternate" hreflang="ru" href="ru/">
  <link rel="alternate" hreflang="uz" href="uz/">
  <link rel="alternate" hreflang="en" href="en/">
  <link rel="alternate" hreflang="x-default" href="en/">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <script>
    (function () {
      var supported = ["ru", "uz", "en"], pick = "en";
      try {
        var saved = localStorage.getItem("lang");
        if (supported.indexOf(saved) !== -1) pick = saved;
        else {
          var langs = navigator.languages || [navigator.language || ""];
          for (var i = 0; i < langs.length; i++) {
            var code = String(langs[i]).slice(0, 2).toLowerCase();
            if (supported.indexOf(code) !== -1) { pick = code; break; }
          }
        }
      } catch (e) {}
      location.replace(pick + "/");
    })();
  </script>
  <style>
    body{margin:0;font-family:"Figtree","Helvetica Neue",Helvetica,Arial,sans-serif;background:#fff;color:#000;padding:0 24px;-webkit-font-smoothing:antialiased}
    @media (prefers-color-scheme:dark){body{background:#000;color:#fff}}
    main{max-width:1200px;margin:0 auto;padding:20vh 0;text-align:center}
    h1{font-size:clamp(32px,6vw,56px);font-weight:500;letter-spacing:-.03em;margin:0 0 24px}
    nav{display:flex;gap:32px;justify-content:center;font-size:17px}
    a{color:inherit;text-decoration:none}a:hover{text-decoration:underline;text-underline-offset:.18em}
  </style>
</head>
<body>
<main>
  <h1>Javharbek</h1>
  <nav><a href="ru/" lang="ru">Русский</a><a href="uz/" lang="uz">O‘zbekcha</a><a href="en/" lang="en">English</a></nav>
</main>
</body>
</html>
"""


def main():
    for lang in LANGS:
        (ROOT / lang).mkdir(exist_ok=True)
        (ROOT / lang / "sigmoid").mkdir(exist_ok=True)
        (ROOT / lang / "index.html").write_text(home(lang), encoding="utf-8")
        (ROOT / lang / "sigmoid" / "index.html").write_text(article(lang), encoding="utf-8")
    (ROOT / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
    print("built:", ", ".join(f"{l}/ {l}/sigmoid/" for l in LANGS), "+ index.html")


if __name__ == "__main__":
    main()
