"""Formula page: MAPE (mean absolute percentage error). Format: see README.md, reference page: sigmoid.py."""

META = dict(
    id="mape",
    date="2026-10-28",
    minutes=35,
    hero=r"\mathrm{MAPE}=\frac{100\%}{n}\sum_{i=1}^{n}\left|\frac{y_i-\hat{y}_i}{y_i}\right|",
    title={"ru": "MAPE: средняя абсолютная процентная ошибка", "en": "MAPE: the mean absolute percentage error", "uz": "MAPE: o‘rtacha absolyut foiz xatosi"},
    dek={
        "ru": "Метрика, которую понимает любой менеджер: «в среднем ошибаемся на 12%». За простотой прячутся подвохи: деление на факт взрывается возле нуля, недопрогноз и перепрогноз наказываются по-разному, а модель, обученная на MAPE, систематически занижает. Разбираем всё по косточкам — с производной, 3D-поверхностью ошибки, обучением и бизнес-примером.",
        "en": "A metric any manager understands: “on average we are off by 12%”. Behind the simplicity there are traps: dividing by the actual explodes near zero, under- and over-forecasts are punished differently, and a model trained on MAPE systematically forecasts too low. We take it apart bone by bone — with the derivative, a 3D error surface, training and a business example.",
        "uz": "Har qanday menejer tushunadigan metrika: «o‘rtacha 12% ga adashamiz». Soddalik ortida tuzoqlar yashiringan: haqiqiy qiymatga bo‘lish nol atrofida portlaydi, kam va ortiq bashorat har xil jazolanadi, MAPE’da o‘qitilgan model esa sistematik ravishda kamaytirib bashorat qiladi. Hammasini mayda detallarigacha tahlil qilamiz — hosila, xatoning 3D sirti, o‘qitish va biznes misoli bilan.",
    },
    description={
        "ru": "MAPE подробно: формула, асимметрия, поведение возле нуля, производная, оптимальная константа — взвешенная медиана, 3D-поверхность ошибки, обучение с весами 1/y, сравнение с sMAPE, WAPE и MASE, бизнес-пример, код.",
        "en": "MAPE in depth: formula, asymmetry, behaviour near zero, derivative, the optimal constant as a weighted median, a 3D error surface, training with 1/y weights, comparison with sMAPE, WAPE and MASE, a business example, code.",
        "uz": "MAPE batafsil: formula, nosimmetriklik, nol atrofidagi xulq, hosila, optimal konstanta — vaznli mediana, xatoning 3D sirti, 1/y vaznlar bilan o‘qitish, sMAPE, WAPE va MASE bilan taqqoslash, biznes misoli, kod.",
    },
)

# The running example from the cheat sheet: y = (3, 5, 8), ŷ = (2.5, 5, 10).
EXAMPLE = [("1", "3", "2.5", "0.5", "16.7%"), ("2", "5", "5", "0", "0%"), ("3", "8", "10", "2", "25.0%")]
MEAN_ROW = {"ru": "среднее", "en": "mean", "uz": "o‘rtacha"}


def _num(s, lang):
    s = s.replace("-", "−")
    return s if lang == "en" else s.replace(".", ",")


def _table(lang):
    rows = [[_num(c, lang) for c in r] for r in EXAMPLE]
    rows.append([MEAN_ROW[lang], "", "", _num("0.833", lang), _num("13.9%", lang)])
    return rows


ALT = {
    "ru": [["MAPE", "$\\frac{100\\%}{n}\\sum\\frac{|e_i|}{|y_i|}$", "не определена", "доля факта; асимметрична в разах; взрывается возле нуля"],
           ["sMAPE", "$\\frac{100\\%}{n}\\sum\\frac{2|e_i|}{|y_i|+|\\hat y_i|}$", "допустимы, если $\\hat y_i\\ne0$", "ограничена $200\\%$; в штуках строже к недопрогнозу"],
           ["WAPE", "$100\\%\\cdot\\frac{\\sum|e_i|}{\\sum|y_i|}$", "допустимы (нужна ненулевая сумма)", "MAE, делённая на средний факт; крупные объекты весят больше"],
           ["MASE", "$\\frac{\\frac1n\\sum|e_i|}{\\frac{1}{T-1}\\sum_t|y_t-y_{t-1}|}$", "допустимы (ряд не постоянен)", "MAE относительно наивного прогноза «как в прошлый период»; $&lt;1$ — лучше наивного"]],
    "en": [["MAPE", "$\\frac{100\\%}{n}\\sum\\frac{|e_i|}{|y_i|}$", "undefined", "a share of the actual; asymmetric in ratios; explodes near zero"],
           ["sMAPE", "$\\frac{100\\%}{n}\\sum\\frac{2|e_i|}{|y_i|+|\\hat y_i|}$", "allowed if $\\hat y_i\\ne0$", "bounded by $200\\%$; in units, harsher on under-forecasts"],
           ["WAPE", "$100\\%\\cdot\\frac{\\sum|e_i|}{\\sum|y_i|}$", "allowed (a non-zero sum is needed)", "MAE divided by the mean actual; large objects weigh more"],
           ["MASE", "$\\frac{\\frac1n\\sum|e_i|}{\\frac{1}{T-1}\\sum_t|y_t-y_{t-1}|}$", "allowed (the series is not constant)", "MAE relative to the naive “same as last period” forecast; $&lt;1$ — better than naive"]],
    "uz": [["MAPE", "$\\frac{100\\%}{n}\\sum\\frac{|e_i|}{|y_i|}$", "aniqlanmagan", "haqiqiy qiymat ulushi; marta bo‘yicha nosimmetrik; nol atrofida portlaydi"],
           ["sMAPE", "$\\frac{100\\%}{n}\\sum\\frac{2|e_i|}{|y_i|+|\\hat y_i|}$", "$\\hat y_i\\ne0$ bo‘lsa, mumkin", "$200\\%$ bilan chegaralangan; donada kam bashoratga qattiqroq"],
           ["WAPE", "$100\\%\\cdot\\frac{\\sum|e_i|}{\\sum|y_i|}$", "mumkin (yig‘indi nol bo‘lmasin)", "o‘rtacha haqiqiy qiymatga bo‘lingan MAE; katta obyektlar og‘irroq"],
           ["MASE", "$\\frac{\\frac1n\\sum|e_i|}{\\frac{1}{T-1}\\sum_t|y_t-y_{t-1}|}$", "mumkin (qator o‘zgarmas bo‘lmasin)", "«o‘tgan davrdagidek» sodda bashoratga nisbatan MAE; $&lt;1$ — sodda bashoratdan yaxshi"]],
}

CODE_NUMPY = '''import numpy as np

y     = np.array([3.0, 5.0, 8.0])
y_hat = np.array([2.5, 5.0, 10.0])

ape  = np.abs((y - y_hat) / y)      # [0.1667 0.     0.25  ]
mape = 100 * ape.mean()             # 13.89

# То же как взвешенная MAE с весами 1/|y|
w = 1 / np.abs(y)
print(100 * np.mean(w * np.abs(y - y_hat)))   # 13.89

def smape(y, f):
    return 100 * np.mean(2 * np.abs(f - y) / (np.abs(y) + np.abs(f)))

def wape(y, f):
    return 100 * np.sum(np.abs(y - f)) / np.sum(np.abs(y))

print(smape(y, y_hat), wape(y, y_hat))        # ≈13.468 15.625'''

CODE_SKLEARN = '''from sklearn.metrics import mean_absolute_percentage_error
from sklearn.linear_model import LinearRegression, QuantileRegressor

print(mean_absolute_percentage_error(y, y_hat))            # 0.1389 — доля, а не проценты!
print(mean_absolute_percentage_error([0.0, 5.0], [1.0, 5.0]))  # 2.25e+15: деление на eps вместо нуля

# Обучение «на MAPE»: медианная регрессия (MAE) с весами 1/y
rng = np.random.default_rng(0)
x = rng.uniform(1, 10, 400)
t = 10 * x * np.exp(0.35 * rng.standard_normal(400))
X = x[:, None]
ols = LinearRegression(fit_intercept=False).fit(X, t)
fit = QuantileRegressor(quantile=0.5, alpha=0, fit_intercept=False).fit(X, t, sample_weight=1 / t)
print(ols.coef_, fit.coef_)   # ≈[10.58] [8.85] — модель по MAPE занижает сумму на 16%'''

CODE_TORCH = '''import torch

def mape_loss(pred, target, eps=1e-8):
    """MAPE как функция потерь (доля). eps спасает от деления на 0, но не от огромных весов возле нуля."""
    return torch.mean(torch.abs(target - pred) / target.abs().clamp_min(eps))

y     = torch.tensor([3.0, 5.0, 8.0])
y_hat = torch.tensor([2.5, 5.0, 10.0], requires_grad=True)
loss = mape_loss(y_hat, y)
loss.backward()
print(loss.item(), y_hat.grad)   # 0.1389  tensor([-0.1111, -0.0000,  0.0417])'''

_CODE_TR = {
    "en": [("То же как взвешенная MAE с весами 1/|y|", "The same as a weighted MAE with weights 1/|y|"),
           ("доля, а не проценты!", "a fraction, not a percentage!"), ("деление на eps вместо нуля", "division by eps instead of zero"),
           ("Обучение «на MAPE»: медианная регрессия (MAE) с весами 1/y", "Training “on MAPE”: median (MAE) regression with weights 1/y"),
           ("модель по MAPE занижает сумму на 16%", "the MAPE model under-forecasts the total by 16%"),
           ("MAPE как функция потерь (доля). eps спасает от деления на 0, но не от огромных весов возле нуля.", "MAPE as a loss (a fraction). eps prevents division by 0 but not huge weights near zero.")],
    "uz": [("То же как взвешенная MAE с весами 1/|y|", "Xuddi shu, 1/|y| vaznli MAE sifatida"),
           ("доля, а не проценты!", "foiz emas, ulush!"), ("деление на eps вместо нуля", "nol o‘rniga eps ga bo‘lish"),
           ("Обучение «на MAPE»: медианная регрессия (MAE) с весами 1/y", "«MAPE bo‘yicha» o‘qitish: 1/y vaznli mediana regressiyasi (MAE)"),
           ("модель по MAPE занижает сумму на 16%", "MAPE bo‘yicha model yig‘indini 16% ga kamaytiradi"),
           ("MAPE как функция потерь (доля). eps спасает от деления на 0, но не от огромных весов возле нуля.", "Yo‘qotish funksiyasi sifatida MAPE (ulush). eps 0 ga bo‘lishdan saqlaydi, lekin nol atrofidagi ulkan vaznlardan emas.")],
}


def _code(src, lang):
    for a, b in _CODE_TR.get(lang, []):
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", "Отдел продаж спрашивает: «насколько точен прогноз?». Ответ «MAE равна 37 штукам» мало что скажет: для хлеба это отлично, для автомобилей — катастрофа. Ответ «в среднем ошибаемся на 12%» понятен без пояснений и одинаково читается для хлеба и автомобилей. Поэтому MAPE (mean absolute percentage error) — одна из самых популярных метрик в прогнозировании спроса, финансах и энергетике."),
        ("p", "Где она встречается:"),
        ("ul", [
            "<b>прогноз спроса и продаж</b> — розница, логистика, планирование закупок; часто это главный KPI отдела прогнозирования;",
            "<b>финансы и экономика</b> — точность прогнозов выручки, цен, макропоказателей;",
            "<b>энергетика</b> — прогноз нагрузки на сеть, где процент ошибки прямо пересчитывается в стоимость резерва;",
            "<b>сравнение рядов разного масштаба</b> — MAPE безразмерна, поэтому точность можно усреднять по тысячам товаров;",
            "<b>соревнования по прогнозированию</b> — в M-соревнованиях использовали её симметричный вариант sMAPE.",
        ]),
        ("callout", "key", "Главное за минуту", "MAPE — средняя абсолютная ошибка, измеренная в долях факта. Она не зависит от масштаба, но не определена при $y_i=0$ и взрывается возле нуля. Для положительного факта недопрогноз стоит не больше $100\\%$, а перепрогноз — сколько угодно. MAPE — это MAE с весами $1/|y_i|$, поэтому лучшая по MAPE константа — взвешенная медиана, смещённая вниз, а модель, обученная на MAPE, занижает прогнозы."),
    ]),
    dict(id="intuition", title="Интуиция: ошибка в долях от факта", blocks=[
        ("p", "Промахнуться на 1 штуку, когда продано 3, — ошибиться на треть. Промахнуться на ту же штуку, когда продано 100, — почти точное попадание. MAPE измеряет каждую ошибку относительно своего факта и усредняет получившиеся проценты."),
        ("p", "Потяните синие точки — прогнозы. Справа — процентная ошибка каждого объекта (APE, absolute percentage error) и их среднее — MAPE."),
        ("viz", "mape-explorer", {}, "<b>Рисунок 1.</b> Сквозной пример: $y=(3;\\,5;\\,8)$, $\\hat y=(2{,}5;\\,5;\\,10)$. Ошибки $0{,}5$ и $2$ превращаются в $16{,}7\\%$ и $25\\%$, среднее $\\mathrm{MAPE}\\approx13{,}9\\%$. Опустите первый прогноз до 2 — промах на одну штуку будет стоить $33{,}3\\%$; тот же промах на третьем объекте (прогноз 7) стоил бы лишь $12{,}5\\%$."),
        ("callout", "intuition", "Что заметить", "Абсолютная ошибка третьего объекта вчетверо больше, чем первого ($2$ против $0{,}5$), а процентная — лишь в $1{,}5$ раза ($25\\%$ против $16{,}7\\%$): большой факт «прощает» большие ошибки. MAPE равнодушна к масштабу и очень чувствительна к малым фактам."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", "Разберём формулу изнутри наружу."),
        ("eq", r"e_i=y_i-\hat y_i\;\xrightarrow{\;|\cdot|\;}\;|e_i|\;\xrightarrow{\;:\,|y_i|\;}\;\mathrm{APE}_i=\frac{|e_i|}{|y_i|}\;\xrightarrow{\;\frac1n\sum\;}\;\text{доля}\;\xrightarrow{\;\times100\%\;}\;\mathrm{MAPE}"),
        ("symbols", [
            (r"y_i", "факт; должен быть ненулевым;"),
            (r"\hat y_i", "прогноз модели;"),
            (r"|y_i-\hat y_i|", "абсолютная ошибка, как в <a href=\"../mae/\">MAE</a>;"),
            (r"\frac{|y_i-\hat y_i|}{|y_i|}", "относительная ошибка APE — доля факта, на которую мы промахнулись; не зависит от единиц измерения;"),
            (r"\frac{100\%}{n}\sum_{i=1}^n", "среднее по объектам, переведённое в проценты."),
        ]),
        ("p", "Сквозной пример по шагам:"),
        ("table", ["$i$", "$y_i$", "$\\hat y_i$", "$|y_i-\\hat y_i|$", "$\\mathrm{APE}_i$"], "TABLE", {"num": [1, 2, 3, 4]}),
        ("eq", r"\mathrm{MAPE}=\frac{100\%}{3}\Bigl(\frac{0{,}5}{3}+\frac{0}{5}+\frac{2}{8}\Bigr)=\frac{100\%}{3}\,(0{,}1667+0+0{,}25)\approx13{,}9\%"),
        ("p", "Две эквивалентные записи раскрывают устройство метрики:"),
        ("eq", r"\mathrm{MAPE}=\frac{100\%}{n}\sum_{i=1}^{n}\underbrace{\frac{1}{|y_i|}}_{w_i}\,|y_i-\hat y_i|=\frac{100\%}{n}\sum_{i=1}^{n}\Bigl|1-\frac{\hat y_i}{y_i}\Bigr|"),
        ("p", "Первая: MAPE — это <b>взвешенная MAE</b> с весами $w_i=1/|y_i|$; объекты с малым фактом получают огромный вес. Вторая: для положительных фактов APE зависит только от отношения $q_i=\\hat y_i/y_i$, $\\mathrm{APE}_i=|1-q_i|$. Поэтому MAPE не меняется, если умножить все факты и прогнозы на одно и то же число."),
        ("callout", "note", "Проценты или доли", "Библиотеки часто возвращают MAPE долей, без умножения на 100: <code>sklearn.metrics.mean_absolute_percentage_error</code> на сквозном примере даёт $0{,}139$, а не $13{,}9$. Проверяйте, что именно вы сравниваете."),
    ]),
    dict(id="properties", title="Свойства и асимметрия", blocks=[
        ("ul", [
            "<b>Безразмерность</b>: $\\mathrm{MAPE}(c\\,y,\\,c\\,\\hat y)=\\mathrm{MAPE}(y,\\hat y)$ при любом $c\\ne0$. Рубли или тысячи рублей — всё равно.",
            "<b>Нет инвариантности к сдвигу</b>: прибавьте 1000 к фактам и прогнозам — абсолютные ошибки те же, а MAPE упадёт в разы. Поэтому MAPE бессмысленна для температуры в °C и других шкал с условным нулём.",
            "<b>Не определена при $y_i=0$</b> и неограниченно растёт при $y_i\\to0$: прогноз 1 при факте $0{,}01$ — это ошибка $9900\\%$.",
            "<b>Нулевой прогноз стоит ровно $100\\%$</b>: при $\\hat y_i=0$ каждая $\\mathrm{APE}_i=1$. Модель «всегда ноль» имеет $\\mathrm{MAPE}=100\\%$ на любых ненулевых данных.",
            "<b>Асимметрия</b>: для положительного факта и неотрицательного прогноза недопрогноз даёт $\\mathrm{APE}\\le100\\%$, а перепрогноз не ограничен.",
            "<b>Выпуклость</b>: MAPE — сумма модулей линейных функций прогнозов, поэтому она выпукла по прогнозам (и по параметрам линейной модели); равна нулю только при идеальном прогнозе.",
        ]),
        ("h3", "В штуках симметрична, в разах — нет"),
        ("p", "Если считать промах в единицах, MAPE симметрична: прогнозы $y-d$ и $y+d$ стоят одинаково, $d/y$. Но в бизнесе промахи часто меряют в разах: «завысили в полтора раза», «занизили вдвое». Тут MAPE несимметрична: занизить вдвое ($\\hat y=y/2$) стоит $50\\%$, завысить вдвое ($\\hat y=2y$) — $100\\%$. Из двух прогнозов, ошибающихся в одно и то же число раз, MAPE всегда предпочтёт заниженный."),
        ("viz", "mape-asymmetry", {"yhat": 150}, "<b>Рисунок 2.</b> Ошибка одного объекта с фактом $y=100$ как функция прогноза. Оранжевая APE — «галочка» с изломом в $\\hat y=y$: слева она упирается в потолок $100\\%$, справа растёт без ограничений. Прогноз 150 (в $1{,}5$ раза больше факта) стоит $50\\%$, а прогноз $100^2/150\\approx66{,}7$ (в $1{,}5$ раза меньше) — только $33{,}3\\%$. Фиолетовая sMAPE ограничена $200\\%$ и при той же абсолютной ошибке строже к недопрогнозу: $40\\%$ при $\\hat y=150$ и $66{,}7\\%$ при $\\hat y=50$. Внизу — производные: у APE это ступенька $\\pm1\\%$ на единицу прогноза."),
        ("deep", "Почему sMAPE не такая уж симметричная", [
            ("p", "sMAPE делит ошибку на среднее факта и прогноза: $\\mathrm{sAPE}=2|y-\\hat y|/(|y|+|\\hat y|)$. В разах она симметрична: при $\\hat y=k\\,y$ и при $\\hat y=y/k$ (с $k&gt;0$, $y&gt;0$) получается одно и то же:"),
            ("eq", r"\frac{2|k-1|\,y}{y+k\,y}=\frac{2|k-1|}{k+1},\qquad\frac{2|1/k-1|\,y}{y+y/k}=\frac{2|1-k|}{k+1}"),
            ("p", "Но в штуках — нет: при $\\hat y=y\\pm d$ знаменатели $2y-d$ и $2y+d$ различаются, и недопрогноз штрафуется сильнее. Симметрию «в разах» и «в штуках» одновременно не даёт ни одна из этих метрик; строго симметрична в разах логарифмическая ошибка $|\\ln(\\hat y/y)|$."),
        ]),
    ]),
    dict(id="derivative", title="Производная и лучшая константа", blocks=[
        ("p", "Для одного объекта APE — модуль линейной функции прогноза, поэтому её производная — ступенька:"),
        ("eq", r"\frac{\partial\,\mathrm{APE}_i}{\partial\hat y_i}=\frac{\operatorname{sign}(\hat y_i-y_i)}{|y_i|},\qquad\hat y_i\ne y_i"),
        ("deep", "Вывод и градиент по параметрам", [
            ("p", "При $\\hat y_i&gt;y_i$ имеем $\\mathrm{APE}_i=(\\hat y_i-y_i)/|y_i|$ — прямая с наклоном $1/|y_i|$; при $\\hat y_i&lt;y_i$ — прямая $(y_i-\\hat y_i)/|y_i|$ с наклоном $-1/|y_i|$. В точке $\\hat y_i=y_i$ производной нет (излом); субградиент — любое число из $[-1/|y_i|;\\,1/|y_i|]$, библиотеки обычно берут 0. Для параметров модели по цепному правилу:"),
            ("eq", r"\frac{\partial\,\mathrm{MAPE}}{\partial\theta}=\frac{100\%}{n}\sum_{i=1}^{n}\frac{\operatorname{sign}(\hat y_i-y_i)}{|y_i|}\cdot\frac{\partial\hat y_i}{\partial\theta}"),
        ]),
        ("p", "Модуль производной не зависит от размера ошибки — как у <a href=\"../mae/\">MAE</a>, — но умножен на $1/|y_i|$: объект с фактом 1 тянет модель в 100 раз сильнее объекта с фактом 100. В сквозном примере $\\partial\\,\\mathrm{MAPE}/\\partial\\hat y=\\tfrac{100\\%}{3}\\,\\bigl(-\\tfrac13;\\;0;\\;\\tfrac18\\bigr)\\approx(-11{,}1\\%;\\;0;\\;4{,}2\\%)$ на единицу прогноза: первый объект с вчетверо меньшей ошибкой тянет в $2{,}7$ раза сильнее третьего."),
        ("h3", "Лучшая константа — взвешенная медиана, смещённая вниз"),
        ("p", "Какой один прогноз $c$ для всех объектов минимизирует MAPE? Функция $\\mathrm{MAPE}(c)=\\frac{100\\%}{n}\\sum_i|y_i-c|/y_i$ кусочно-линейна и выпукла; между соседними точками данных её наклон равен $\\frac{100\\%}{n}\\bigl(\\sum_{y_i&lt;c}\\tfrac1{y_i}-\\sum_{y_i&gt;c}\\tfrac1{y_i}\\bigr)$. Минимум там, где наклон меняет знак, — где суммарный вес $1/y$ слева сравнивается с весом справа. Это <b>взвешенная медиана</b> с весами $1/y_i$:"),
        ("eq", r"c^*=\operatorname*{arg\,min}_c\sum_{i=1}^{n}\frac{|y_i-c|}{y_i}=\text{взвешенная медиана } y_i \text{ с весами } \frac{1}{y_i}"),
        ("p", "Веса убывают с ростом $y$, поэтому взвешенная медиана не больше обычной: MAPE систематически тянет прогноз вниз. Для логнормального спроса это считается точно: если $\\ln y\\sim N(\\mu,\\sigma^2)$, то $c^*=e^{\\mu-\\sigma^2}$ — медиана $e^{\\mu}$, умноженная на $e^{-\\sigma^2}$."),
        ("deep", "Откуда множитель e^(−σ²)", [
            ("p", "Взвешенная медиана — медиана распределения с плотностью, пропорциональной $f(y)/y$. Для логнормальной плотности $f$, обозначив $t=\\ln y$:"),
            ("eq", r"\frac{f(y)}{y}\propto\frac{1}{y^2}\,e^{-\frac{(t-\mu)^2}{2\sigma^2}}=\frac{1}{y}\,e^{-\frac{(t-\mu)^2+2\sigma^2 t}{2\sigma^2}}\propto\frac{1}{y}\,e^{-\frac{(t-(\mu-\sigma^2))^2}{2\sigma^2}}"),
            ("p", "Это снова логнормальная плотность, но с параметром $\\mu-\\sigma^2$; её медиана $e^{\\mu-\\sigma^2}$. Для сравнения: среднее исходного распределения $e^{\\mu+\\sigma^2/2}$ выше медианы. При $\\sigma=0{,}6$ оптимум MAPE на $1-e^{-0{,}36}\\approx30\\%$ ниже медианы."),
        ]),
        ("viz", "mape-optimal", {"sigma": 0.6, "c": 100}, "<b>Рисунок 3.</b> 60 значений логнормального спроса с медианой около 100 (фиксированное зерно генератора). Чёрная кривая — MAPE константного прогноза $c$, внизу — её наклон, ступенчатая функция. При $\\sigma=0{,}6$ минимум $42{,}5\\%$ достигается в $c^*\\approx71{,}0$, тогда как медиана равна $101{,}0$, а среднее — $119{,}1$: оптимальный по MAPE прогноз на $29{,}7\\%$ ниже медианы (теория $e^{-0{,}36}-1\\approx-30{,}2\\%$). Прогноз, равный медиане, стоит $51{,}5\\%$, равный среднему — $63{,}0\\%$, нулевой — ровно $100\\%$."),
        ("callout", "warn", "Обучение на MAPE даёт недопрогноз", "Модель, обученная минимизировать MAPE, наследует это смещение: её прогнозы систематически ниже фактов. В рознице это означает пустые полки, а потерянные продажи не попадут ни в одну метрику: продано ровно столько, сколько было на складе."),
    ]),
    dict(id="surface", title="Карта ошибки: APE над плоскостью (y, ŷ)", blocks=[
        ("p", "Посмотрим на ошибку одного объекта как на функцию двух переменных — факта $y$ и прогноза $\\hat y$. Линии уровня APE — это <b>лучи из начала координат</b>: условие $|y-\\hat y|/y=a$ равносильно $\\hat y=(1\\pm a)\\,y$. Линии уровня абсолютной ошибки, наоборот, — параллельные прямые $\\hat y=y\\pm e$. Лучи сходятся в нуле, поэтому вблизи $y=0$ любая фиксированная абсолютная ошибка пересекает все уровни APE — отсюда и «взрыв»."),
        ("viz", "mape-surface", {"p": [2, 3]}, "<b>Рисунок 4.</b> Слева — поверхность $\\mathrm{APE}(y,\\hat y)$, обрезанная на $200\\%$ (её можно вращать): долина нулевой ошибки вдоль диагонали $\\hat y=y$ (оранжевая линия) и стена у $y\\to0$. Справа — вид сверху: чёрные лучи — уровни APE, красный пунктир — уровни абсолютной ошибки 1 и 2. Точки $P=(2;\\,3)$ и $Q=(8;\\,9)$ ошибаются на одну и ту же единицу, но $\\mathrm{APE}(P)=50\\%$, а $\\mathrm{APE}(Q)=12{,}5\\%$."),
        ("p", "Для $n$ объектов MAPE — среднее таких функций. В пространстве прогнозов $(\\hat y_1,\\dots,\\hat y_n)$ её линии уровня — многогранники (ромбы в 2D) с центром в $y$ и полуосями, пропорциональными $y_i$: вдоль осей с малыми $y_i$ далеко не отойдёшь без большого штрафа."),
    ]),
    dict(id="training", title="Обучение на MAPE: веса 1/y и недопрогноз", blocks=[
        ("p", "Раз MAPE — это MAE с весами $1/|y_i|$, обучить модель на MAPE можно любым алгоритмом, который минимизирует MAE с весами объектов: передайте <code>sample_weight=1/|y|</code>. В LightGBM есть готовая цель <code>objective=\"mape\"</code>, в PyTorch потеря пишется в одну строку (см. раздел с кодом)."),
        ("p", "Обучим простейшую модель $\\hat y=w\\,x$ на 40 объектах, у которых $y=10\\,x\\cdot e^{0{,}35\\,\\varepsilon}$, $\\varepsilon\\sim N(0,1)$: истинный наклон равен 10, шум мультипликативный — его размер растёт вместе с $y$, как у реальных продаж."),
        ("viz", "mape-training", {}, "<b>Рисунок 5.</b> Слева — данные (размер точки пропорционален весу $1/y$) и две модели, справа — MAPE как функция наклона $w$. Нажмите «Пуск»: субградиентный спуск по MAPE с шагом $8/\\sqrt{t+1}$ из $w=4$ сходится к $w^*\\approx9{,}10$ с $\\mathrm{MAPE}\\approx20{,}28\\%$. Метод наименьших квадратов даёт $w\\approx10{,}74$ и $\\mathrm{MAPE}\\approx22{,}99\\%$, зато его суммарный прогноз почти не смещён ($-0{,}6\\%$), а у модели по MAPE сумма прогнозов примерно на $16\\%$ ниже суммы фактов."),
        ("p", "Почему так: точки с малыми $y$ получают большой вес и тянут прямую вниз. В терминах отношений $q_i=y_i/x_i$ имеем $\\mathrm{MAPE}(w)=\\frac{100\\%}{n}\\sum_i|q_i-w|/q_i$, так что оптимум — взвешенная медиана $q_i$ с весами $1/q_i$. При логнормальном шуме это медиана, умноженная на $e^{-\\sigma^2}=e^{-0{,}1225}\\approx0{,}885$, то есть около $8{,}85$ вместо 10."),
        ("callout", "key", "Как обойти смещение", "1) Обучайте на MAE или MSE от $\\ln y$, а MAPE используйте только для отчёта. 2) Если KPI — именно MAPE, а недопрогноз дорог (дефицит), корректируйте прогнозы множителем, подобранным на валидации, или выберите метрику, отражающую реальные издержки (WAPE, квантильная потеря). 3) Не обучайте на MAPE, если в данных есть нули или почти нули."),
    ]),
    dict(id="alternatives", title="MAPE, sMAPE, WAPE и MASE", blocks=[
        ("p", "Из-за перечисленных проблем у MAPE есть несколько популярных родственников ($e_i=y_i-\\hat y_i$):"),
        ("table", ["Метрика", "Формула", "Нули в $y$", "Особенность"], "ALT", {"num": []}),
        ("p", "В сквозном примере $\\mathrm{MAPE}\\approx13{,}9\\%$, $\\mathrm{sMAPE}\\approx13{,}5\\%$, $\\mathrm{WAPE}=2{,}5/16\\approx15{,}6\\%$, а MASE с масштабом $\\tfrac12\\bigl(|5-3|+|8-5|\\bigr)=2{,}5$ равна $0{,}833/2{,}5\\approx0{,}33$."),
        ("p", "WAPE (её ещё называют MAD/Mean ratio) — это MAE, делённая на средний факт: объекты с большими продажами весят больше, и общий итог не ломается от одного товара с почти нулевым спросом. MASE (Хайндман и Кёлер, 2006) сравнивает MAE модели с MAE наивного прогноза и годится даже для рядов с нулями. На одних и тех же данных WAPE и MASE отличаются лишь постоянным множителем, поэтому у них один и тот же оптимум."),
        ("viz", "mape-metrics", {"k": 1}, "<b>Рисунок 6.</b> 52 недели спроса (точки) и прогноз $k\\cdot$база (синяя линия). Справа — метрики как функции множителя $k$, точки — минимумы. MAPE минимальна при $k\\approx0{,}89$, то есть при прогнозе, заниженном на 11%; sMAPE — при $k\\approx1{,}007$; WAPE (и MASE) — при $k\\approx1{,}012$. Включите провал спроса — одну неделю с $y=3$: MAPE при $k=1$ подскакивает с $24{,}5\\%$ до $68{,}8\\%$, а её минимум уезжает к $k\\approx0{,}78$; WAPE меняется лишь с $23{,}5\\%$ до $25{,}4\\%$."),
    ]),
    dict(id="business", title="Бизнес-пример: ассортимент магазина", blocks=[
        ("p", "Сеть прогнозирует недельные продажи шести товаров. Пять из них продаются десятками и сотнями штук и прогнозируются с ошибкой от $7{,}5\\%$ до $16{,}7\\%$. Шестой, F, — редкий товар: прогноз 10 штук, а продано 4."),
        ("viz", "mape-portfolio", {"f": 4}, "<b>Рисунок 7.</b> Слева — факт и прогноз (логарифмическая шкала), справа — APE каждого товара. Товар F, на который приходится $0{,}15\\%$ продаж, даёт $\\mathrm{APE}=150\\%$ и $72\\%$ суммы всех APE: $\\mathrm{MAPE}=34{,}8\\%$, хотя без него она равна $11{,}7\\%$. WAPE, считающая ошибку в штуках, равна $9{,}4\\%$: 256 штук ошибки на 2714 проданных. Подвигайте продажи F: при одной проданной штуке MAPE почти достигает $160\\%$."),
        ("p", "Что делать на практике:"),
        ("ul", [
            "<b>отчитываться WAPE</b> (или MAPE, взвешенной по выручке), если важна общая точность в штуках или деньгах;",
            "<b>считать MAPE по группам</b> — быстрые и медленные товары отдельно — или исключать позиции с продажами ниже порога, явно указав порог;",
            "<b>для медленных товаров</b> использовать MASE или специальные метрики для прерывистого спроса;",
            "<b>отдельно следить за знаком ошибки</b>: смещение суммы прогнозов (bias) — самостоятельный KPI, MAPE его не показывает.",
        ]),
        ("callout", "history", "Почему MAPE так популярна", "MAPE понятна без статистического образования, поэтому давно стала стандартом отраслевых отчётов. Критика тоже давняя: на смещение в пользу заниженных прогнозов и проблему малых фактов указывали ещё в 1980–1990-х (например, Армстронг и Коллопи, 1992), а Хайндман и Кёлер (2006) предложили MASE как масштабно-независимую альтернативу без этих недостатков."),
    ]),
    dict(id="code", title="В коде", blocks=[
        ("p", "В NumPy MAPE — одна строка; ниже заодно sMAPE, WAPE и проверка формул на сквозном примере."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "scikit-learn возвращает долю и вместо деления на ноль делит на машинный эпсилон. Для обучения «на MAPE» подходит медианная регрессия с весами $1/y$:"),
        ("code", "python", "CODE_SKLEARN"),
        ("p", "В PyTorch MAPE как функция потерь:"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Правило", "Перед тем как считать MAPE, посмотрите на минимум $|y|$ в данных. Если там нули или значения, несопоставимо малые по сравнению с типичными, — отчитывайтесь WAPE или MASE и не используйте MAPE как функцию потерь."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>MAPE на данных с нулями.</b> Деление на ноль даёт бесконечность или NaN, а «защита» через $\\varepsilon$ — астрономические числа: scikit-learn вернёт $2{,}25\\cdot10^{15}$. Фильтруйте нули явно и сообщайте об этом или берите WAPE и MASE.",
            "<b>MAPE для шкал с условным нулём</b> — температуры в °C, индексов, дат. Ошибка в 1° при 2° и при 30° одна и та же, а MAPE различается в 15 раз.",
            "<b>Обучение на MAPE без учёта смещения.</b> Модель систематически занижает прогноз, и в рознице это превращается в дефицит на полках.",
            "<b>Сравнение MAPE между наборами с разной долей малых значений.</b> Одна и та же модель покажет 12% на быстрых товарах и 60% на медленных — дело в данных, а не в качестве.",
            "<b>Путаница долей и процентов</b>: scikit-learn возвращает $0{,}139$, а не $13{,}9$.",
            "<b>«MAPE меньше — значит, план точнее».</b> MAPE не видит знака ошибок: прогноз с меньшей MAPE может в сумме занижать спрос на 16%, как на рисунке 5.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../mae/\">MAE</a>: MAPE — это MAE с весами $1/|y_i|$; модуль градиента тоже не зависит от размера ошибки, но масштабирован на $1/|y_i|$.",
            "<a href=\"../mse/\">MSE</a> и <a href=\"../rmse/\">RMSE</a>: абсолютные квадратичные ошибки; их относительный родственник — RMSLE, RMSE в логарифмической шкале.",
            "<a href=\"../huber/\">Huber</a>: сглаживает излом в нуле; ту же идею можно применить к относительной ошибке.",
            "<a href=\"../sgd/\">SGD</a>: обучение на MAPE — субградиентный спуск, шаг которого нужно уменьшать (на рисунке 5 — как $1/\\sqrt t$).",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $\\mathrm{MAPE}=\\frac{100\\%}{n}\\sum|y_i-\\hat y_i|/|y_i|$ — средняя ошибка в процентах от факта; не зависит от масштаба и понятна бизнесу. 2) Не определена при $y=0$ и взрывается возле нуля; нулевой прогноз стоит ровно $100\\%$. 3) Асимметрична в разах: занизить вдвое — $50\\%$, завысить вдвое — $100\\%$. 4) MAPE — MAE с весами $1/|y|$: производная $\\operatorname{sign}(\\hat y-y)/|y|$, лучшая константа — взвешенная медиана ниже обычной, обучение на MAPE даёт недопрогноз. 5) Для отчётов по ассортименту обычно надёжнее WAPE и MASE."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="Факт 200, прогноз 150. Чему равна APE?", options=["$25\\%$", "$33{,}3\\%$", "$50\\%$", "$12{,}5\\%$"], answer=0,
                 explain="Делим на факт: $50/200=25\\%$. Если по ошибке разделить на прогноз, получится $33{,}3\\%$."),
            dict(q="Факт 100. Какой прогноз даёт большую APE: 50 или 200?", options=["50", "200", "Одинаково", "Зависит от $n$"], answer=1,
                 explain="$|100-50|/100=50\\%$, а $|100-200|/100=100\\%$. Оба промаха — вдвое, но перепрогноз стоит вдвое дороже."),
            dict(q="Модель всегда прогнозирует 0 при положительных продажах. Чему равна её MAPE?", options=["$0\\%$", "$50\\%$", "$100\\%$", "Бесконечности"], answer=2,
                 explain="Каждая $\\mathrm{APE}_i=|y_i-0|/|y_i|=1$, поэтому $\\mathrm{MAPE}=100\\%$ при любых данных."),
            dict(q="Факты: 1, 10 и 100. Какой константный прогноз минимизирует MAPE?", options=["1", "10", "37", "100"], answer=0,
                 explain="Веса $1/y_i$ равны $1$, $0{,}1$ и $0{,}01$; вес первого объекта больше суммы остальных, поэтому взвешенная медиана — 1: $\\mathrm{MAPE}=(0+0{,}9+0{,}99)/3=63\\%$, а при $c=10$ — $330\\%$."),
            dict(q="Почему WAPE устойчивее MAPE на ассортименте с редкими товарами?", options=["WAPE не учитывает ошибки редких товаров", "WAPE делит суммарную ошибку на суммарный факт, и малые факты не получают огромных весов", "WAPE всегда меньше MAPE", "WAPE возводит ошибки в квадрат"], answer=1,
                 explain="В WAPE каждый объект входит своей абсолютной ошибкой в штуках, а деление происходит один раз — на сумму фактов. Ошибка редкого товара в 6 штук остаётся ошибкой в 6 штук."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why it is needed", blocks=[
        ("p", "The sales team asks: “how accurate is the forecast?”. The answer “MAE is 37 units” says little: for bread that is excellent, for cars a disaster. The answer “on average we are off by 12%” needs no explanation and reads the same for bread and for cars. That is why MAPE (mean absolute percentage error) is one of the most popular metrics in demand forecasting, finance and energy."),
        ("p", "Where it shows up:"),
        ("ul", [
            "<b>demand and sales forecasting</b> — retail, logistics, purchase planning; it is often the main KPI of a forecasting team;",
            "<b>finance and economics</b> — the accuracy of revenue, price and macro forecasts;",
            "<b>energy</b> — grid load forecasting, where the percentage error translates directly into the cost of reserves;",
            "<b>comparing series of different scales</b> — MAPE is dimensionless, so accuracy can be averaged over thousands of products;",
            "<b>forecasting competitions</b> — the M competitions used its symmetric variant, sMAPE.",
        ]),
        ("callout", "key", "The gist in a minute", "MAPE is the mean absolute error measured as a share of the actual. It does not depend on scale, but it is undefined at $y_i=0$ and explodes near zero. For a positive actual an under-forecast costs at most $100\\%$, an over-forecast can cost any amount. MAPE is MAE with weights $1/|y_i|$, so the best constant under MAPE is a weighted median shifted downwards, and a model trained on MAPE forecasts too low."),
    ]),
    dict(id="intuition", title="Intuition: the error as a share of the actual", blocks=[
        ("p", "Missing by 1 unit when 3 were sold means being off by a third. Missing by the same unit when 100 were sold is almost a bull’s-eye. MAPE measures each error relative to its own actual and averages the resulting percentages."),
        ("p", "Drag the blue points — the forecasts. On the right, the percentage error of each object (APE, absolute percentage error) and their mean — MAPE."),
        ("viz", "mape-explorer", {}, "<b>Figure 1.</b> The running example: $y=(3,\\,5,\\,8)$, $\\hat y=(2.5,\\,5,\\,10)$. The errors $0.5$ and $2$ become $16.7\\%$ and $25\\%$; the mean is $\\mathrm{MAPE}\\approx13.9\\%$. Lower the first forecast to 2 — a miss of one unit will cost $33.3\\%$; the same miss on the third object (forecast 7) would cost only $12.5\\%$."),
        ("callout", "intuition", "What to notice", "The absolute error of the third object is four times that of the first ($2$ versus $0.5$), but the percentage error is only $1.5$ times larger ($25\\%$ versus $16.7\\%$): a large actual “forgives” large errors. MAPE is indifferent to scale and very sensitive to small actuals."),
    ]),
    dict(id="anatomy", title="The formula bone by bone", blocks=[
        ("p", "Let us take the formula apart from the inside out."),
        ("eq", r"e_i=y_i-\hat y_i\;\xrightarrow{\;|\cdot|\;}\;|e_i|\;\xrightarrow{\;:\,|y_i|\;}\;\mathrm{APE}_i=\frac{|e_i|}{|y_i|}\;\xrightarrow{\;\frac1n\sum\;}\;\text{share}\;\xrightarrow{\;\times100\%\;}\;\mathrm{MAPE}"),
        ("symbols", [
            (r"y_i", "the actual; must be non-zero;"),
            (r"\hat y_i", "the model’s forecast;"),
            (r"|y_i-\hat y_i|", "the absolute error, as in <a href=\"../mae/\">MAE</a>;"),
            (r"\frac{|y_i-\hat y_i|}{|y_i|}", "the relative error APE — the share of the actual by which we missed; independent of the units;"),
            (r"\frac{100\%}{n}\sum_{i=1}^n", "the mean over the objects, converted to per cent."),
        ]),
        ("p", "The running example step by step:"),
        ("table", ["$i$", "$y_i$", "$\\hat y_i$", "$|y_i-\\hat y_i|$", "$\\mathrm{APE}_i$"], "TABLE", {"num": [1, 2, 3, 4]}),
        ("eq", r"\mathrm{MAPE}=\frac{100\%}{3}\Bigl(\frac{0.5}{3}+\frac{0}{5}+\frac{2}{8}\Bigr)=\frac{100\%}{3}\,(0.1667+0+0.25)\approx13.9\%"),
        ("p", "Two equivalent forms reveal how the metric works:"),
        ("eq", r"\mathrm{MAPE}=\frac{100\%}{n}\sum_{i=1}^{n}\underbrace{\frac{1}{|y_i|}}_{w_i}\,|y_i-\hat y_i|=\frac{100\%}{n}\sum_{i=1}^{n}\Bigl|1-\frac{\hat y_i}{y_i}\Bigr|"),
        ("p", "The first: MAPE is a <b>weighted MAE</b> with weights $w_i=1/|y_i|$; objects with a small actual get a huge weight. The second: for positive actuals APE depends only on the ratio $q_i=\\hat y_i/y_i$, $\\mathrm{APE}_i=|1-q_i|$. That is why MAPE does not change when all actuals and forecasts are multiplied by the same number."),
        ("callout", "note", "Per cent or fraction", "Libraries often return MAPE as a fraction, without multiplying by 100: <code>sklearn.metrics.mean_absolute_percentage_error</code> gives $0.139$ on the running example, not $13.9$. Check what exactly you are comparing."),
    ]),
    dict(id="properties", title="Properties and asymmetry", blocks=[
        ("ul", [
            "<b>Dimensionless</b>: $\\mathrm{MAPE}(c\\,y,\\,c\\,\\hat y)=\\mathrm{MAPE}(y,\\hat y)$ for any $c\\ne0$. Dollars or thousands of dollars — it does not matter.",
            "<b>Not shift-invariant</b>: add 1000 to the actuals and the forecasts — the absolute errors are the same, but MAPE drops many times over. So MAPE is meaningless for temperature in °C and other scales with an arbitrary zero.",
            "<b>Undefined at $y_i=0$</b> and unbounded as $y_i\\to0$: a forecast of 1 for an actual of $0.01$ is an error of $9900\\%$.",
            "<b>A zero forecast costs exactly $100\\%$</b>: with $\\hat y_i=0$ every $\\mathrm{APE}_i=1$. The “always zero” model has $\\mathrm{MAPE}=100\\%$ on any non-zero data.",
            "<b>Asymmetry</b>: for a positive actual and a non-negative forecast an under-forecast gives $\\mathrm{APE}\\le100\\%$, while an over-forecast is unbounded.",
            "<b>Convexity</b>: MAPE is a sum of absolute values of linear functions of the forecasts, so it is convex in the forecasts (and in the parameters of a linear model); it is zero only for a perfect forecast.",
        ]),
        ("h3", "Symmetric in units, not in ratios"),
        ("p", "If you count a miss in units, MAPE is symmetric: forecasts $y-d$ and $y+d$ cost the same, $d/y$. But in business misses are often measured in ratios: “over by half again”, “half of what we sold”. Here MAPE is asymmetric: forecasting half ($\\hat y=y/2$) costs $50\\%$, forecasting double ($\\hat y=2y$) costs $100\\%$. Of two forecasts that are off by the same factor, MAPE always prefers the lower one."),
        ("viz", "mape-asymmetry", {"yhat": 150}, "<b>Figure 2.</b> The error of one object with actual $y=100$ as a function of the forecast. The orange APE is a “tick” with a kink at $\\hat y=y$: on the left it hits the $100\\%$ ceiling, on the right it grows without bound. A forecast of 150 ($1.5$ times the actual) costs $50\\%$, while $100^2/150\\approx66.7$ ($1.5$ times less) costs only $33.3\\%$. The violet sMAPE is bounded by $200\\%$ and, for the same absolute error, is harsher on under-forecasts: $40\\%$ at $\\hat y=150$ and $66.7\\%$ at $\\hat y=50$. Bottom: the derivatives; for APE it is a step of $\\pm1\\%$ per unit of forecast."),
        ("deep", "Why sMAPE is not that symmetric", [
            ("p", "sMAPE divides the error by the mean of the actual and the forecast: $\\mathrm{sAPE}=2|y-\\hat y|/(|y|+|\\hat y|)$. In ratios it is symmetric: for $\\hat y=k\\,y$ and for $\\hat y=y/k$ (with $k&gt;0$, $y&gt;0$) we get the same value:"),
            ("eq", r"\frac{2|k-1|\,y}{y+k\,y}=\frac{2|k-1|}{k+1},\qquad\frac{2|1/k-1|\,y}{y+y/k}=\frac{2|1-k|}{k+1}"),
            ("p", "In units it is not: for $\\hat y=y\\pm d$ the denominators $2y-d$ and $2y+d$ differ, and the under-forecast is penalised more. None of these metrics is symmetric both “in ratios” and “in units”; the log error $|\\ln(\\hat y/y)|$ is exactly symmetric in ratios."),
        ]),
    ]),
    dict(id="derivative", title="The derivative and the best constant", blocks=[
        ("p", "For a single object APE is the absolute value of a linear function of the forecast, so its derivative is a step:"),
        ("eq", r"\frac{\partial\,\mathrm{APE}_i}{\partial\hat y_i}=\frac{\operatorname{sign}(\hat y_i-y_i)}{|y_i|},\qquad\hat y_i\ne y_i"),
        ("deep", "Derivation and the gradient in the parameters", [
            ("p", "For $\\hat y_i&gt;y_i$ we have $\\mathrm{APE}_i=(\\hat y_i-y_i)/|y_i|$, a line with slope $1/|y_i|$; for $\\hat y_i&lt;y_i$, the line $(y_i-\\hat y_i)/|y_i|$ with slope $-1/|y_i|$. At $\\hat y_i=y_i$ there is no derivative (a kink); a subgradient is any number in $[-1/|y_i|,\\,1/|y_i|]$, and libraries usually take 0. For model parameters, by the chain rule:"),
            ("eq", r"\frac{\partial\,\mathrm{MAPE}}{\partial\theta}=\frac{100\%}{n}\sum_{i=1}^{n}\frac{\operatorname{sign}(\hat y_i-y_i)}{|y_i|}\cdot\frac{\partial\hat y_i}{\partial\theta}"),
        ]),
        ("p", "The size of the derivative does not depend on the size of the error — as in <a href=\"../mae/\">MAE</a> — but it is multiplied by $1/|y_i|$: an object with actual 1 pulls the model 100 times harder than an object with actual 100. In the running example $\\partial\\,\\mathrm{MAPE}/\\partial\\hat y=\\tfrac{100\\%}{3}\\,\\bigl(-\\tfrac13,\\;0,\\;\\tfrac18\\bigr)\\approx(-11.1\\%,\\;0,\\;4.2\\%)$ per unit of forecast: the first object, with a four times smaller error, pulls $2.7$ times harder than the third."),
        ("h3", "The best constant is a weighted median shifted downwards"),
        ("p", "Which single forecast $c$ for all objects minimises MAPE? The function $\\mathrm{MAPE}(c)=\\frac{100\\%}{n}\\sum_i|y_i-c|/y_i$ is piecewise linear and convex; between neighbouring data points its slope is $\\frac{100\\%}{n}\\bigl(\\sum_{y_i&lt;c}\\tfrac1{y_i}-\\sum_{y_i&gt;c}\\tfrac1{y_i}\\bigr)$. The minimum is where the slope changes sign — where the total weight $1/y$ on the left balances the weight on the right. This is the <b>weighted median</b> with weights $1/y_i$:"),
        ("eq", r"c^*=\operatorname*{arg\,min}_c\sum_{i=1}^{n}\frac{|y_i-c|}{y_i}=\text{the weighted median of } y_i \text{ with weights } \frac{1}{y_i}"),
        ("p", "The weights decrease as $y$ grows, so the weighted median is not larger than the ordinary one: MAPE systematically pulls the forecast down. For lognormal demand this can be computed exactly: if $\\ln y\\sim N(\\mu,\\sigma^2)$, then $c^*=e^{\\mu-\\sigma^2}$ — the median $e^{\\mu}$ multiplied by $e^{-\\sigma^2}$."),
        ("deep", "Where the factor e^(−σ²) comes from", [
            ("p", "The weighted median is the median of the distribution with density proportional to $f(y)/y$. For the lognormal density $f$, writing $t=\\ln y$:"),
            ("eq", r"\frac{f(y)}{y}\propto\frac{1}{y^2}\,e^{-\frac{(t-\mu)^2}{2\sigma^2}}=\frac{1}{y}\,e^{-\frac{(t-\mu)^2+2\sigma^2 t}{2\sigma^2}}\propto\frac{1}{y}\,e^{-\frac{(t-(\mu-\sigma^2))^2}{2\sigma^2}}"),
            ("p", "This is again a lognormal density, but with parameter $\\mu-\\sigma^2$; its median is $e^{\\mu-\\sigma^2}$. For comparison, the mean of the original distribution, $e^{\\mu+\\sigma^2/2}$, is above the median. With $\\sigma=0.6$ the MAPE optimum is $1-e^{-0.36}\\approx30\\%$ below the median."),
        ]),
        ("viz", "mape-optimal", {"sigma": 0.6, "c": 100}, "<b>Figure 3.</b> 60 values of lognormal demand with a median of about 100 (fixed generator seed). The black curve is the MAPE of the constant forecast $c$; below is its slope, a step function. With $\\sigma=0.6$ the minimum $42.5\\%$ is reached at $c^*\\approx71.0$, while the median is $101.0$ and the mean is $119.1$: the MAPE-optimal forecast is $29.7\\%$ below the median (theory $e^{-0.36}-1\\approx-30.2\\%$). A forecast equal to the median costs $51.5\\%$, one equal to the mean $63.0\\%$, and a zero forecast exactly $100\\%$."),
        ("callout", "warn", "Training on MAPE leads to under-forecasting", "A model trained to minimise MAPE inherits this bias: its forecasts are systematically below the actuals. In retail that means empty shelves, and the lost sales never show up in any metric: you sell exactly what was in stock."),
    ]),
    dict(id="surface", title="A map of the error: APE over the (y, ŷ) plane", blocks=[
        ("p", "Look at the error of one object as a function of two variables — the actual $y$ and the forecast $\\hat y$. The level lines of APE are <b>rays from the origin</b>: the condition $|y-\\hat y|/y=a$ is equivalent to $\\hat y=(1\\pm a)\\,y$. The level lines of the absolute error, in contrast, are parallel lines $\\hat y=y\\pm e$. The rays converge at zero, so near $y=0$ any fixed absolute error crosses all levels of APE — hence the “explosion”."),
        ("viz", "mape-surface", {"p": [2, 3]}, "<b>Figure 4.</b> Left: the surface $\\mathrm{APE}(y,\\hat y)$, clipped at $200\\%$ (rotatable): a valley of zero error along the diagonal $\\hat y=y$ (orange line) and a wall as $y\\to0$. Right: the top view; black rays are APE levels, the red dashed lines are absolute-error levels 1 and 2. The points $P=(2,\\,3)$ and $Q=(8,\\,9)$ miss by the same one unit, but $\\mathrm{APE}(P)=50\\%$ while $\\mathrm{APE}(Q)=12.5\\%$."),
        ("p", "For $n$ objects MAPE is the mean of such functions. In the forecast space $(\\hat y_1,\\dots,\\hat y_n)$ its level sets are polytopes (diamonds in 2D) centred at $y$ with semi-axes proportional to $y_i$: along axes with small $y_i$ you cannot move far without a big penalty."),
    ]),
    dict(id="training", title="Training on MAPE: 1/y weights and under-forecasting", blocks=[
        ("p", "Since MAPE is MAE with weights $1/|y_i|$, a model can be trained on MAPE by any algorithm that minimises a weighted MAE: pass <code>sample_weight=1/|y|</code>. LightGBM has a ready-made <code>objective=\"mape\"</code>, and in PyTorch the loss is one line (see the code section)."),
        ("p", "Let us train the simplest model $\\hat y=w\\,x$ on 40 objects with $y=10\\,x\\cdot e^{0.35\\,\\varepsilon}$, $\\varepsilon\\sim N(0,1)$: the true slope is 10, and the noise is multiplicative — its size grows with $y$, as with real sales."),
        ("viz", "mape-training", {}, "<b>Figure 5.</b> Left: the data (dot size is proportional to the weight $1/y$) and two models; right: MAPE as a function of the slope $w$. Press “Play”: subgradient descent on MAPE with step $8/\\sqrt{t+1}$ from $w=4$ converges to $w^*\\approx9.10$ with $\\mathrm{MAPE}\\approx20.28\\%$. Least squares gives $w\\approx10.74$ and $\\mathrm{MAPE}\\approx22.99\\%$, but its total forecast is almost unbiased ($-0.6\\%$), while the MAPE model’s total forecast is about $16\\%$ below the total actual."),
        ("p", "Why: points with small $y$ get a large weight and pull the line down. In terms of the ratios $q_i=y_i/x_i$ we have $\\mathrm{MAPE}(w)=\\frac{100\\%}{n}\\sum_i|q_i-w|/q_i$, so the optimum is the weighted median of $q_i$ with weights $1/q_i$. With lognormal noise this is the median times $e^{-\\sigma^2}=e^{-0.1225}\\approx0.885$, i.e. about $8.85$ instead of 10."),
        ("callout", "key", "How to avoid the bias", "1) Train on MAE or MSE of $\\ln y$ and use MAPE only for reporting. 2) If the KPI really is MAPE but under-forecasts are costly (stock-outs), correct the forecasts with a multiplier tuned on validation data, or choose a metric that reflects the real costs (WAPE, the quantile loss). 3) Do not train on MAPE if the data contain zeros or near-zeros."),
    ]),
    dict(id="alternatives", title="MAPE, sMAPE, WAPE and MASE", blocks=[
        ("p", "Because of these problems MAPE has several popular relatives ($e_i=y_i-\\hat y_i$):"),
        ("table", ["Metric", "Formula", "Zeros in $y$", "Feature"], "ALT", {"num": []}),
        ("p", "In the running example $\\mathrm{MAPE}\\approx13.9\\%$, $\\mathrm{sMAPE}\\approx13.5\\%$, $\\mathrm{WAPE}=2.5/16\\approx15.6\\%$, and MASE with the scale $\\tfrac12\\bigl(|5-3|+|8-5|\\bigr)=2.5$ equals $0.833/2.5\\approx0.33$."),
        ("p", "WAPE (also called the MAD/Mean ratio) is MAE divided by the mean actual: objects with large sales weigh more, and the total is not ruined by a single product with near-zero demand. MASE (Hyndman and Koehler, 2006) compares the model’s MAE with the MAE of the naive forecast and works even for series with zeros. On the same data WAPE and MASE differ only by a constant factor, so they share the same optimum."),
        ("viz", "mape-metrics", {"k": 1}, "<b>Figure 6.</b> 52 weeks of demand (dots) and the forecast $k\\cdot$base (blue line). Right: the metrics as functions of the multiplier $k$; dots mark the minima. MAPE is minimal at $k\\approx0.89$, i.e. for a forecast 11% too low; sMAPE at $k\\approx1.007$; WAPE (and MASE) at $k\\approx1.012$. Turn on the demand dip — one week with $y=3$: MAPE at $k=1$ jumps from $24.5\\%$ to $68.8\\%$ and its minimum moves to $k\\approx0.78$; WAPE only changes from $23.5\\%$ to $25.4\\%$."),
    ]),
    dict(id="business", title="A business example: a store’s assortment", blocks=[
        ("p", "A chain forecasts weekly sales of six products. Five of them sell in tens and hundreds of units and are forecast with errors from $7.5\\%$ to $16.7\\%$. The sixth, F, is a slow mover: the forecast was 10 units and 4 were sold."),
        ("viz", "mape-portfolio", {"f": 4}, "<b>Figure 7.</b> Left: actual and forecast (log scale); right: the APE of each product. Product F, which accounts for $0.15\\%$ of sales, has $\\mathrm{APE}=150\\%$ and $72\\%$ of the sum of all APEs: $\\mathrm{MAPE}=34.8\\%$, whereas without it MAPE is $11.7\\%$. WAPE, which counts the error in units, is $9.4\\%$: 256 units of error over 2714 sold. Move the sales of F: with a single unit sold MAPE almost reaches $160\\%$."),
        ("p", "What to do in practice:"),
        ("ul", [
            "<b>report WAPE</b> (or MAPE weighted by revenue) when the overall accuracy in units or money matters;",
            "<b>compute MAPE by groups</b> — fast and slow movers separately — or exclude items with sales below a threshold, stating the threshold explicitly;",
            "<b>for slow movers</b> use MASE or dedicated metrics for intermittent demand;",
            "<b>track the sign of the error separately</b>: the bias of the total forecast is a KPI of its own, and MAPE does not show it.",
        ]),
        ("callout", "history", "Why MAPE is so popular", "MAPE is understandable without statistical training, so it long ago became the standard of industry reports. The criticism is old too: the bias towards low forecasts and the problem of small actuals were pointed out back in the 1980s–1990s (for example, Armstrong and Collopy, 1992), and Hyndman and Koehler (2006) proposed MASE as a scale-free alternative without these shortcomings."),
    ]),
    dict(id="code", title="In code", blocks=[
        ("p", "In NumPy MAPE is one line; below we also compute sMAPE and WAPE and check the formulas on the running example."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "scikit-learn returns a fraction and divides by the machine epsilon instead of zero. Median regression with weights $1/y$ is a way to train “on MAPE”:"),
        ("code", "python", "CODE_SKLEARN"),
        ("p", "MAPE as a loss in PyTorch:"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Rule of thumb", "Before computing MAPE, look at the minimum of $|y|$ in the data. If there are zeros or values that are tiny compared with typical ones, report WAPE or MASE and do not use MAPE as a loss."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>MAPE on data with zeros.</b> Division by zero gives infinity or NaN, and “protecting” it with $\\varepsilon$ gives astronomical numbers: scikit-learn returns $2.25\\cdot10^{15}$. Filter zeros explicitly and say so, or use WAPE and MASE.",
            "<b>MAPE for scales with an arbitrary zero</b> — temperatures in °C, indices, dates. An error of 1° at 2° and at 30° is the same, but MAPE differs 15 times.",
            "<b>Training on MAPE without accounting for the bias.</b> The model systematically under-forecasts, which in retail turns into stock-outs.",
            "<b>Comparing MAPE across data sets with different shares of small values.</b> The same model will show 12% on fast movers and 60% on slow movers — the data are to blame, not the quality.",
            "<b>Mixing up fractions and per cent</b>: scikit-learn returns $0.139$, not $13.9$.",
            "<b>“Lower MAPE means a more accurate plan”.</b> MAPE does not see the sign of the errors: a forecast with lower MAPE can under-forecast total demand by 16%, as in Figure 5.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../mae/\">MAE</a>: MAPE is MAE with weights $1/|y_i|$; the size of the gradient also does not depend on the size of the error, but it is scaled by $1/|y_i|$.",
            "<a href=\"../mse/\">MSE</a> and <a href=\"../rmse/\">RMSE</a>: absolute squared errors; their relative cousin is RMSLE, the RMSE on a log scale.",
            "<a href=\"../huber/\">Huber</a>: smooths the kink at zero; the same idea can be applied to the relative error.",
            "<a href=\"../sgd/\">SGD</a>: training on MAPE is subgradient descent whose step must shrink (in Figure 5, as $1/\\sqrt t$).",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $\\mathrm{MAPE}=\\frac{100\\%}{n}\\sum|y_i-\\hat y_i|/|y_i|$ is the mean error as a percentage of the actual; scale-free and clear to business. 2) Undefined at $y=0$ and explodes near zero; a zero forecast costs exactly $100\\%$. 3) Asymmetric in ratios: half the actual costs $50\\%$, double costs $100\\%$. 4) MAPE is MAE with weights $1/|y|$: the derivative is $\\operatorname{sign}(\\hat y-y)/|y|$, the best constant is a weighted median below the ordinary one, and training on MAPE leads to under-forecasting. 5) For assortment reports WAPE and MASE are usually more reliable."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="The actual is 200 and the forecast is 150. What is APE?", options=["$25\\%$", "$33.3\\%$", "$50\\%$", "$12.5\\%$"], answer=0,
                 explain="Divide by the actual: $50/200=25\\%$. Dividing by the forecast by mistake would give $33.3\\%$."),
            dict(q="The actual is 100. Which forecast gives the larger APE: 50 or 200?", options=["50", "200", "The same", "It depends on $n$"], answer=1,
                 explain="$|100-50|/100=50\\%$ and $|100-200|/100=100\\%$. Both are off by a factor of two, but the over-forecast costs twice as much."),
            dict(q="A model always forecasts 0 while sales are positive. What is its MAPE?", options=["$0\\%$", "$50\\%$", "$100\\%$", "Infinity"], answer=2,
                 explain="Every $\\mathrm{APE}_i=|y_i-0|/|y_i|=1$, so $\\mathrm{MAPE}=100\\%$ for any data."),
            dict(q="The actuals are 1, 10 and 100. Which constant forecast minimises MAPE?", options=["1", "10", "37", "100"], answer=0,
                 explain="The weights $1/y_i$ are $1$, $0.1$ and $0.01$; the first weight exceeds the sum of the others, so the weighted median is 1: $\\mathrm{MAPE}=(0+0.9+0.99)/3=63\\%$, while at $c=10$ it is $330\\%$."),
            dict(q="Why is WAPE more robust than MAPE on an assortment with slow movers?", options=["WAPE ignores the errors of slow movers", "WAPE divides the total error by the total actual, so small actuals do not get huge weights", "WAPE is always smaller than MAPE", "WAPE squares the errors"], answer=1,
                 explain="In WAPE each object enters with its absolute error in units, and the division happens once — by the sum of the actuals. A slow mover’s error of 6 units stays an error of 6 units."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "Savdo bo‘limi so‘raydi: «bashorat qanchalik aniq?». «MAE 37 dona» degan javob kam narsa aytadi: non uchun bu a’lo, avtomobillar uchun esa falokat. «O‘rtacha 12% ga adashamiz» degan javob izohsiz tushunarli va non uchun ham, avtomobillar uchun ham bir xil o‘qiladi. Shuning uchun MAPE (mean absolute percentage error) talabni bashorat qilish, moliya va energetikadagi eng mashhur metrikalardan biri."),
        ("p", "U qayerda uchraydi:"),
        ("ul", [
            "<b>talab va sotuvlarni bashorat qilish</b> — chakana savdo, logistika, xaridlarni rejalashtirish; ko‘pincha bu bashorat bo‘limining asosiy KPI’i;",
            "<b>moliya va iqtisodiyot</b> — tushum, narxlar, makroko‘rsatkichlar bashoratlarining aniqligi;",
            "<b>energetika</b> — tarmoq yuklamasini bashorat qilish, bunda xato foizi to‘g‘ridan-to‘g‘ri zaxira narxiga aylanadi;",
            "<b>turli masshtabdagi qatorlarni solishtirish</b> — MAPE o‘lchamsiz, shuning uchun aniqlikni minglab tovarlar bo‘yicha o‘rtachalash mumkin;",
            "<b>bashorat musobaqalari</b> — M-musobaqalarda uning simmetrik varianti sMAPE ishlatilgan.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "MAPE — haqiqiy qiymat ulushlarida o‘lchangan o‘rtacha absolyut xato. U masshtabga bog‘liq emas, lekin $y_i=0$ da aniqlanmagan va nol atrofida portlaydi. Musbat haqiqiy qiymat uchun kam bashorat ko‘pi bilan $100\\%$ turadi, ortiq bashorat esa istalgancha. MAPE — $1/|y_i|$ vaznli MAE, shuning uchun MAPE bo‘yicha eng yaxshi konstanta pastga siljigan vaznli mediana, MAPE’da o‘qitilgan model esa bashoratlarni kamaytiradi."),
    ]),
    dict(id="intuition", title="Intuitsiya: haqiqiy qiymat ulushlaridagi xato", blocks=[
        ("p", "3 dona sotilganda 1 donaga adashish — uchdan birga xato qilish. 100 dona sotilganda xuddi shu bir donaga adashish — deyarli aniq tegish. MAPE har bir xatoni o‘z haqiqiy qiymatiga nisbatan o‘lchaydi va hosil bo‘lgan foizlarni o‘rtachalaydi."),
        ("p", "Ko‘k nuqtalarni — bashoratlarni torting. O‘ngda — har bir obyektning foizdagi xatosi (APE, absolute percentage error) va ularning o‘rtachasi — MAPE."),
        ("viz", "mape-explorer", {}, "<b>Rasm 1.</b> Umumiy misol: $y=(3;\\,5;\\,8)$, $\\hat y=(2{,}5;\\,5;\\,10)$. $0{,}5$ va $2$ xatolar $16{,}7\\%$ va $25\\%$ ga aylanadi, o‘rtacha $\\mathrm{MAPE}\\approx13{,}9\\%$. Birinchi bashoratni 2 gacha tushiring — bir donalik xato $33{,}3\\%$ turadi; uchinchi obyektdagi xuddi shunday xato (bashorat 7) atigi $12{,}5\\%$ turar edi."),
        ("callout", "intuition", "Nimaga e’tibor bering", "Uchinchi obyektning absolyut xatosi birinchinikidan to‘rt baravar katta ($2$ va $0{,}5$), foizdagisi esa atigi $1{,}5$ baravar ($25\\%$ va $16{,}7\\%$): katta haqiqiy qiymat katta xatolarni «kechiradi». MAPE masshtabga befarq va kichik haqiqiy qiymatlarga juda sezgir."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", "Formulani ichkaridan tashqariga qarab tahlil qilamiz."),
        ("eq", r"e_i=y_i-\hat y_i\;\xrightarrow{\;|\cdot|\;}\;|e_i|\;\xrightarrow{\;:\,|y_i|\;}\;\mathrm{APE}_i=\frac{|e_i|}{|y_i|}\;\xrightarrow{\;\frac1n\sum\;}\;\text{ulush}\;\xrightarrow{\;\times100\%\;}\;\mathrm{MAPE}"),
        ("symbols", [
            (r"y_i", "haqiqiy qiymat; noldan farqli bo‘lishi shart;"),
            (r"\hat y_i", "model bashorati;"),
            (r"|y_i-\hat y_i|", "absolyut xato, <a href=\"../mae/\">MAE</a>dagi kabi;"),
            (r"\frac{|y_i-\hat y_i|}{|y_i|}", "nisbiy xato APE — haqiqiy qiymatning biz adashgan ulushi; o‘lchov birliklariga bog‘liq emas;"),
            (r"\frac{100\%}{n}\sum_{i=1}^n", "obyektlar bo‘yicha o‘rtacha, foizlarga o‘tkazilgan."),
        ]),
        ("p", "Umumiy misol qadamma-qadam:"),
        ("table", ["$i$", "$y_i$", "$\\hat y_i$", "$|y_i-\\hat y_i|$", "$\\mathrm{APE}_i$"], "TABLE", {"num": [1, 2, 3, 4]}),
        ("eq", r"\mathrm{MAPE}=\frac{100\%}{3}\Bigl(\frac{0{,}5}{3}+\frac{0}{5}+\frac{2}{8}\Bigr)=\frac{100\%}{3}\,(0{,}1667+0+0{,}25)\approx13{,}9\%"),
        ("p", "Ikkita teng kuchli yozuv metrikaning tuzilishini ochib beradi:"),
        ("eq", r"\mathrm{MAPE}=\frac{100\%}{n}\sum_{i=1}^{n}\underbrace{\frac{1}{|y_i|}}_{w_i}\,|y_i-\hat y_i|=\frac{100\%}{n}\sum_{i=1}^{n}\Bigl|1-\frac{\hat y_i}{y_i}\Bigr|"),
        ("p", "Birinchisi: MAPE — $w_i=1/|y_i|$ vaznli <b>vaznli MAE</b>; haqiqiy qiymati kichik obyektlar ulkan vazn oladi. Ikkinchisi: musbat haqiqiy qiymatlar uchun APE faqat $q_i=\\hat y_i/y_i$ nisbatga bog‘liq, $\\mathrm{APE}_i=|1-q_i|$. Shuning uchun barcha haqiqiy qiymatlar va bashoratlar bir xil songa ko‘paytirilsa, MAPE o‘zgarmaydi."),
        ("callout", "note", "Foizmi yoki ulush", "Kutubxonalar ko‘pincha MAPE’ni 100 ga ko‘paytirmasdan, ulush sifatida qaytaradi: <code>sklearn.metrics.mean_absolute_percentage_error</code> umumiy misolda $13{,}9$ emas, $0{,}139$ beradi. Aynan nimani solishtirayotganingizni tekshiring."),
    ]),
    dict(id="properties", title="Xossalar va nosimmetriklik", blocks=[
        ("ul", [
            "<b>O‘lchamsizlik</b>: istalgan $c\\ne0$ da $\\mathrm{MAPE}(c\\,y,\\,c\\,\\hat y)=\\mathrm{MAPE}(y,\\hat y)$. So‘mmi yoki ming so‘mmi — farqi yo‘q.",
            "<b>Siljishga invariant emas</b>: haqiqiy qiymatlar va bashoratlarga 1000 qo‘shing — absolyut xatolar o‘sha, MAPE esa bir necha marta tushib ketadi. Shuning uchun MAPE °C dagi harorat va shartli nolga ega boshqa shkalalar uchun ma’nosiz.",
            "<b>$y_i=0$ da aniqlanmagan</b> va $y_i\\to0$ da cheksiz o‘sadi: haqiqiy qiymat $0{,}01$ bo‘lganda 1 bashorati — $9900\\%$ xato.",
            "<b>Nol bashorat roppa-rosa $100\\%$ turadi</b>: $\\hat y_i=0$ da har bir $\\mathrm{APE}_i=1$. «Doim nol» modeli istalgan nolmas ma’lumotlarda $\\mathrm{MAPE}=100\\%$ ga ega.",
            "<b>Nosimmetriklik</b>: musbat haqiqiy qiymat va manfiy bo‘lmagan bashorat uchun kam bashorat $\\mathrm{APE}\\le100\\%$ beradi, ortiq bashorat esa chegaralanmagan.",
            "<b>Qavariqlik</b>: MAPE — bashoratlarning chiziqli funksiyalari modullari yig‘indisi, shuning uchun u bashoratlar bo‘yicha (va chiziqli model parametrlari bo‘yicha) qavariq; faqat ideal bashoratda nolga teng.",
        ]),
        ("h3", "Donada simmetrik, marta bo‘yicha — yo‘q"),
        ("p", "Agar xatoni birliklarda hisoblasak, MAPE simmetrik: $y-d$ va $y+d$ bashoratlar bir xil, $d/y$ turadi. Lekin biznesda xatolar ko‘pincha marta bilan o‘lchanadi: «bir yarim baravar oshirib yubordik», «ikki baravar kam bashorat qildik». Bu yerda MAPE nosimmetrik: ikki baravar kam ($\\hat y=y/2$) $50\\%$ turadi, ikki baravar ko‘p ($\\hat y=2y$) — $100\\%$. Bir xil marta adashgan ikki bashoratdan MAPE doim kamrog‘ini afzal ko‘radi."),
        ("viz", "mape-asymmetry", {"yhat": 150}, "<b>Rasm 2.</b> Haqiqiy qiymati $y=100$ bo‘lgan bitta obyekt xatosi bashorat funksiyasi sifatida. To‘q sariq APE — $\\hat y=y$ da singan «belgi»: chapda u $100\\%$ shiftga tiraladi, o‘ngda esa cheksiz o‘sadi. 150 bashorati (haqiqiy qiymatdan $1{,}5$ marta katta) $50\\%$ turadi, $100^2/150\\approx66{,}7$ bashorati ($1{,}5$ marta kichik) esa atigi $33{,}3\\%$. Binafsha sMAPE $200\\%$ bilan chegaralangan va xuddi shu absolyut xatoda kam bashoratga qattiqroq: $\\hat y=150$ da $40\\%$ va $\\hat y=50$ da $66{,}7\\%$. Pastda — hosilalar: APE’da bu bashoratning har bir birligiga $\\pm1\\%$ zinapoya."),
        ("deep", "Nega sMAPE unchalik simmetrik emas", [
            ("p", "sMAPE xatoni haqiqiy qiymat va bashoratning o‘rtachasiga bo‘ladi: $\\mathrm{sAPE}=2|y-\\hat y|/(|y|+|\\hat y|)$. Marta bo‘yicha u simmetrik: $\\hat y=k\\,y$ va $\\hat y=y/k$ da ($k&gt;0$, $y&gt;0$) bir xil qiymat chiqadi:"),
            ("eq", r"\frac{2|k-1|\,y}{y+k\,y}=\frac{2|k-1|}{k+1},\qquad\frac{2|1/k-1|\,y}{y+y/k}=\frac{2|1-k|}{k+1}"),
            ("p", "Donada esa yo‘q: $\\hat y=y\\pm d$ da $2y-d$ va $2y+d$ maxrajlar farq qiladi, va kam bashorat qattiqroq jazolanadi. Bu metrikalarning hech biri bir vaqtda ham «marta bo‘yicha», ham «donada» simmetriyani bermaydi; marta bo‘yicha qat’iy simmetrik — logarifmik xato $|\\ln(\\hat y/y)|$."),
        ]),
    ]),
    dict(id="derivative", title="Hosila va eng yaxshi konstanta", blocks=[
        ("p", "Bitta obyekt uchun APE bashoratning chiziqli funksiyasi moduli, shuning uchun uning hosilasi — zinapoya:"),
        ("eq", r"\frac{\partial\,\mathrm{APE}_i}{\partial\hat y_i}=\frac{\operatorname{sign}(\hat y_i-y_i)}{|y_i|},\qquad\hat y_i\ne y_i"),
        ("deep", "Keltirib chiqarish va parametrlar bo‘yicha gradiyent", [
            ("p", "$\\hat y_i&gt;y_i$ da $\\mathrm{APE}_i=(\\hat y_i-y_i)/|y_i|$ — qiyaligi $1/|y_i|$ bo‘lgan to‘g‘ri chiziq; $\\hat y_i&lt;y_i$ da — qiyaligi $-1/|y_i|$ bo‘lgan $(y_i-\\hat y_i)/|y_i|$ to‘g‘ri chiziq. $\\hat y_i=y_i$ nuqtada hosila yo‘q (sinish); subgradiyent — $[-1/|y_i|;\\,1/|y_i|]$ dan istalgan son, kutubxonalar odatda 0 ni oladi. Model parametrlari uchun zanjir qoidasiga ko‘ra:"),
            ("eq", r"\frac{\partial\,\mathrm{MAPE}}{\partial\theta}=\frac{100\%}{n}\sum_{i=1}^{n}\frac{\operatorname{sign}(\hat y_i-y_i)}{|y_i|}\cdot\frac{\partial\hat y_i}{\partial\theta}"),
        ]),
        ("p", "Hosila moduli xato kattaligiga bog‘liq emas — <a href=\"../mae/\">MAE</a>dagi kabi, — lekin $1/|y_i|$ ga ko‘paytirilgan: haqiqiy qiymati 1 bo‘lgan obyekt modelni haqiqiy qiymati 100 bo‘lgan obyektdan 100 marta kuchliroq tortadi. Umumiy misolda bashoratning har bir birligiga $\\partial\\,\\mathrm{MAPE}/\\partial\\hat y=\\tfrac{100\\%}{3}\\,\\bigl(-\\tfrac13;\\;0;\\;\\tfrac18\\bigr)\\approx(-11{,}1\\%;\\;0;\\;4{,}2\\%)$: xatosi to‘rt baravar kichik birinchi obyekt uchinchisidan $2{,}7$ marta kuchliroq tortadi."),
        ("h3", "Eng yaxshi konstanta — pastga siljigan vaznli mediana"),
        ("p", "Barcha obyektlar uchun qaysi yagona $c$ bashorati MAPE’ni minimallashtiradi? $\\mathrm{MAPE}(c)=\\frac{100\\%}{n}\\sum_i|y_i-c|/y_i$ funksiyasi bo‘lakli-chiziqli va qavariq; qo‘shni ma’lumot nuqtalari orasida uning qiyaligi $\\frac{100\\%}{n}\\bigl(\\sum_{y_i&lt;c}\\tfrac1{y_i}-\\sum_{y_i&gt;c}\\tfrac1{y_i}\\bigr)$ ga teng. Minimum qiyalik ishorasini o‘zgartirgan joyda — chapdagi $1/y$ umumiy vazni o‘ngdagisi bilan tenglashgan joyda. Bu $1/y_i$ vaznli <b>vaznli mediana</b>:"),
        ("eq", r"c^*=\operatorname*{arg\,min}_c\sum_{i=1}^{n}\frac{|y_i-c|}{y_i}=\frac{1}{y_i}\text{ vaznli } y_i \text{ larning vaznli medianasi}"),
        ("p", "Vaznlar $y$ o‘sishi bilan kamayadi, shuning uchun vaznli mediana oddiysidan katta emas: MAPE bashoratni sistematik ravishda pastga tortadi. Lognormal talab uchun buni aniq hisoblash mumkin: agar $\\ln y\\sim N(\\mu,\\sigma^2)$ bo‘lsa, $c^*=e^{\\mu-\\sigma^2}$ — $e^{-\\sigma^2}$ ga ko‘paytirilgan $e^{\\mu}$ mediana."),
        ("deep", "e^(−σ²) ko‘paytuvchi qayerdan keladi", [
            ("p", "Vaznli mediana — zichligi $f(y)/y$ ga proporsional bo‘lgan taqsimotning medianasi. Lognormal $f$ zichlik uchun $t=\\ln y$ deb belgilab:"),
            ("eq", r"\frac{f(y)}{y}\propto\frac{1}{y^2}\,e^{-\frac{(t-\mu)^2}{2\sigma^2}}=\frac{1}{y}\,e^{-\frac{(t-\mu)^2+2\sigma^2 t}{2\sigma^2}}\propto\frac{1}{y}\,e^{-\frac{(t-(\mu-\sigma^2))^2}{2\sigma^2}}"),
            ("p", "Bu yana lognormal zichlik, lekin $\\mu-\\sigma^2$ parametr bilan; uning medianasi $e^{\\mu-\\sigma^2}$. Taqqoslash uchun: dastlabki taqsimotning o‘rtachasi $e^{\\mu+\\sigma^2/2}$ medianadan yuqori. $\\sigma=0{,}6$ da MAPE optimumi medianadan $1-e^{-0{,}36}\\approx30\\%$ past."),
        ]),
        ("viz", "mape-optimal", {"sigma": 0.6, "c": 100}, "<b>Rasm 3.</b> Medianasi taxminan 100 bo‘lgan lognormal talabning 60 ta qiymati (generator zerrasi qayd etilgan). Qora egri chiziq — $c$ konstant bashoratning MAPE’si, pastda — uning qiyaligi, zinapoyasimon funksiya. $\\sigma=0{,}6$ da $42{,}5\\%$ minimumga $c^*\\approx71{,}0$ da erishiladi, mediana esa $101{,}0$, o‘rtacha — $119{,}1$: MAPE bo‘yicha optimal bashorat medianadan $29{,}7\\%$ past (nazariya $e^{-0{,}36}-1\\approx-30{,}2\\%$). Medianaga teng bashorat $51{,}5\\%$, o‘rtachaga teng bashorat $63{,}0\\%$, nol bashorat esa roppa-rosa $100\\%$ turadi."),
        ("callout", "warn", "MAPE’da o‘qitish kam bashoratga olib keladi", "MAPE’ni minimallashtirishga o‘qitilgan model bu siljishni meros qilib oladi: uning bashoratlari sistematik ravishda haqiqiy qiymatlardan past. Chakana savdoda bu bo‘sh javonlarni anglatadi, yo‘qotilgan sotuvlar esa hech bir metrikaga tushmaydi: omborda qancha bo‘lsa, roppa-rosa shuncha sotiladi."),
    ]),
    dict(id="surface", title="Xato xaritasi: (y, ŷ) tekisligi ustidagi APE", blocks=[
        ("p", "Bitta obyekt xatosiga ikki o‘zgaruvchining — haqiqiy qiymat $y$ va bashorat $\\hat y$ ning funksiyasi sifatida qaraymiz. APE sath chiziqlari — <b>koordinata boshidan chiqqan nurlar</b>: $|y-\\hat y|/y=a$ sharti $\\hat y=(1\\pm a)\\,y$ ga teng kuchli. Absolyut xatoning sath chiziqlari esa, aksincha, parallel $\\hat y=y\\pm e$ to‘g‘ri chiziqlar. Nurlar nolda tutashadi, shuning uchun $y=0$ yaqinida istalgan qayd etilgan absolyut xato APE’ning barcha sathlarini kesib o‘tadi — «portlash» shundan."),
        ("viz", "mape-surface", {"p": [2, 3]}, "<b>Rasm 4.</b> Chapda — $200\\%$ da kesilgan $\\mathrm{APE}(y,\\hat y)$ sirti (uni aylantirish mumkin): $\\hat y=y$ diagonali (to‘q sariq chiziq) bo‘ylab nol xato vodiysi va $y\\to0$ da devor. O‘ngda — yuqoridan ko‘rinish: qora nurlar — APE sathlari, qizil punktir — 1 va 2 absolyut xato sathlari. $P=(2;\\,3)$ va $Q=(8;\\,9)$ nuqtalar bir xil bir birlikka adashadi, lekin $\\mathrm{APE}(P)=50\\%$, $\\mathrm{APE}(Q)=12{,}5\\%$."),
        ("p", "$n$ ta obyekt uchun MAPE — shunday funksiyalarning o‘rtachasi. $(\\hat y_1,\\dots,\\hat y_n)$ bashoratlar fazosida uning sath chiziqlari — markazi $y$ da, yarim o‘qlari $y_i$ ga proporsional bo‘lgan ko‘pyoqlar (2D’da romblar): kichik $y_i$ o‘qlari bo‘ylab katta jarimasiz uzoqqa ketib bo‘lmaydi."),
    ]),
    dict(id="training", title="MAPE’da o‘qitish: 1/y vaznlar va kam bashorat", blocks=[
        ("p", "MAPE — $1/|y_i|$ vaznli MAE bo‘lgani uchun, modelni MAPE’da obyekt vaznlari bilan MAE’ni minimallashtiradigan istalgan algoritm bilan o‘qitish mumkin: <code>sample_weight=1/|y|</code> ni bering. LightGBM’da tayyor <code>objective=\"mape\"</code> maqsadi bor, PyTorch’da esa yo‘qotish bir qatorda yoziladi (kod bo‘limiga qarang)."),
        ("p", "Eng oddiy $\\hat y=w\\,x$ modelni $y=10\\,x\\cdot e^{0{,}35\\,\\varepsilon}$, $\\varepsilon\\sim N(0,1)$ bo‘lgan 40 ta obyektda o‘qitamiz: haqiqiy qiyalik 10 ga teng, shovqin multiplikativ — uning kattaligi haqiqiy sotuvlardagi kabi $y$ bilan birga o‘sadi."),
        ("viz", "mape-training", {}, "<b>Rasm 5.</b> Chapda — ma’lumotlar (nuqta o‘lchami $1/y$ vazniga proporsional) va ikki model, o‘ngda — $w$ qiyalik funksiyasi sifatida MAPE. «Boshlash»ni bosing: $w=4$ dan $8/\\sqrt{t+1}$ qadam bilan MAPE bo‘yicha subgradiyent tushish $\\mathrm{MAPE}\\approx20{,}28\\%$ bilan $w^*\\approx9{,}10$ ga yaqinlashadi. Eng kichik kvadratlar usuli $w\\approx10{,}74$ va $\\mathrm{MAPE}\\approx22{,}99\\%$ beradi, lekin uning umumiy bashorati deyarli siljimagan ($-0{,}6\\%$), MAPE bo‘yicha modelning bashoratlar yig‘indisi esa haqiqiy qiymatlar yig‘indisidan taxminan $16\\%$ past."),
        ("p", "Nega shunday: kichik $y$ li nuqtalar katta vazn oladi va to‘g‘ri chiziqni pastga tortadi. $q_i=y_i/x_i$ nisbatlar tilida $\\mathrm{MAPE}(w)=\\frac{100\\%}{n}\\sum_i|q_i-w|/q_i$, demak, optimum — $1/q_i$ vaznli $q_i$ larning vaznli medianasi. Lognormal shovqinda bu $e^{-\\sigma^2}=e^{-0{,}1225}\\approx0{,}885$ ga ko‘paytirilgan mediana, ya’ni 10 o‘rniga taxminan $8{,}85$."),
        ("callout", "key", "Siljishni qanday chetlab o‘tish mumkin", "1) $\\ln y$ dan MAE yoki MSE’da o‘qiting, MAPE’ni esa faqat hisobot uchun ishlating. 2) Agar KPI aynan MAPE bo‘lsa-yu, kam bashorat qimmat bo‘lsa (taqchillik), bashoratlarni validatsiyada tanlangan ko‘paytuvchi bilan to‘g‘rilang yoki haqiqiy xarajatlarni aks ettiruvchi metrikani tanlang (WAPE, kvantil yo‘qotish). 3) Ma’lumotlarda nollar yoki nolga yaqin qiymatlar bo‘lsa, MAPE’da o‘qitmang."),
    ]),
    dict(id="alternatives", title="MAPE, sMAPE, WAPE va MASE", blocks=[
        ("p", "Sanab o‘tilgan muammolar tufayli MAPE’ning bir nechta mashhur qarindoshlari bor ($e_i=y_i-\\hat y_i$):"),
        ("table", ["Metrika", "Formula", "$y$ dagi nollar", "Xususiyati"], "ALT", {"num": []}),
        ("p", "Umumiy misolda $\\mathrm{MAPE}\\approx13{,}9\\%$, $\\mathrm{sMAPE}\\approx13{,}5\\%$, $\\mathrm{WAPE}=2{,}5/16\\approx15{,}6\\%$, masshtabi $\\tfrac12\\bigl(|5-3|+|8-5|\\bigr)=2{,}5$ bo‘lgan MASE esa $0{,}833/2{,}5\\approx0{,}33$ ga teng."),
        ("p", "WAPE (uni MAD/Mean ratio deb ham atashadi) — o‘rtacha haqiqiy qiymatga bo‘lingan MAE: sotuvi katta obyektlar og‘irroq, umumiy natija esa talabi nolga yaqin bitta tovar tufayli buzilmaydi. MASE (Xayndman va Kyoler, 2006) model MAE’sini sodda bashorat MAE’si bilan solishtiradi va hatto nollari bor qatorlar uchun ham yaraydi. Bir xil ma’lumotlarda WAPE va MASE faqat o‘zgarmas ko‘paytuvchi bilan farq qiladi, shuning uchun ularning optimumi bitta."),
        ("viz", "mape-metrics", {"k": 1}, "<b>Rasm 6.</b> 52 haftalik talab (nuqtalar) va $k\\cdot$baza bashorati (ko‘k chiziq). O‘ngda — $k$ ko‘paytuvchining funksiyasi sifatida metrikalar, nuqtalar — minimumlar. MAPE $k\\approx0{,}89$ da, ya’ni 11% ga kamaytirilgan bashoratda minimal; sMAPE — $k\\approx1{,}007$ da; WAPE (va MASE) — $k\\approx1{,}012$ da. Talab tushishini yoqing — $y=3$ bo‘lgan bitta hafta: $k=1$ da MAPE $24{,}5\\%$ dan $68{,}8\\%$ gacha sakraydi, uning minimumi esa $k\\approx0{,}78$ ga ko‘chadi; WAPE atigi $23{,}5\\%$ dan $25{,}4\\%$ gacha o‘zgaradi."),
    ]),
    dict(id="business", title="Biznes misoli: do‘kon assortimenti", blocks=[
        ("p", "Tarmoq oltita tovarning haftalik sotuvlarini bashorat qiladi. Ulardan beshtasi o‘nlab va yuzlab dona sotiladi va $7{,}5\\%$ dan $16{,}7\\%$ gacha xato bilan bashorat qilinadi. Oltinchisi, F, — kam sotiladigan tovar: bashorat 10 dona, sotilgani esa 4."),
        ("viz", "mape-portfolio", {"f": 4}, "<b>Rasm 7.</b> Chapda — haqiqiy qiymat va bashorat (logarifmik shkala), o‘ngda — har bir tovarning APE’si. Sotuvlarning $0{,}15\\%$ i to‘g‘ri keladigan F tovari $\\mathrm{APE}=150\\%$ va barcha APE’lar yig‘indisining $72\\%$ ini beradi: $\\mathrm{MAPE}=34{,}8\\%$, holbuki usiz u $11{,}7\\%$ ga teng. Xatoni donada hisoblaydigan WAPE $9{,}4\\%$ ga teng: 2714 ta sotilgan donaga 256 dona xato. F sotuvlarini suring: bitta dona sotilganda MAPE deyarli $160\\%$ ga yetadi."),
        ("p", "Amalda nima qilish kerak:"),
        ("ul", [
            "<b>WAPE bilan hisobot bering</b> (yoki tushum bo‘yicha vaznlangan MAPE bilan), agar donada yoki pulda umumiy aniqlik muhim bo‘lsa;",
            "<b>MAPE’ni guruhlar bo‘yicha hisoblang</b> — tez va sekin sotiladigan tovarlarni alohida — yoki sotuvi chegaradan past pozitsiyalarni chegarani aniq ko‘rsatgan holda chiqarib tashlang;",
            "<b>sekin sotiladigan tovarlar uchun</b> MASE yoki uzilishli talab uchun maxsus metrikalardan foydalaning;",
            "<b>xato ishorasini alohida kuzating</b>: bashoratlar yig‘indisining siljishi (bias) — mustaqil KPI, MAPE uni ko‘rsatmaydi.",
        ]),
        ("callout", "history", "Nega MAPE shunchalik mashhur", "MAPE statistik ma’lumotsiz ham tushunarli, shuning uchun u allaqachon soha hisobotlarining standartiga aylangan. Tanqid ham eski: kam bashoratlar foydasiga siljish va kichik haqiqiy qiymatlar muammosiga 1980–1990-yillardayoq e’tibor qaratilgan (masalan, Armstrong va Kollopi, 1992), Xayndman va Kyoler (2006) esa bu kamchiliklarsiz masshtabga bog‘liq bo‘lmagan muqobil sifatida MASE’ni taklif qilishgan."),
    ]),
    dict(id="code", title="Kodda", blocks=[
        ("p", "NumPy’da MAPE — bitta qator; quyida sMAPE, WAPE va formulalarni umumiy misolda tekshirish ham bor."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "scikit-learn ulush qaytaradi va nolga bo‘lish o‘rniga mashina epsiloniga bo‘ladi. «MAPE bo‘yicha» o‘qitish uchun $1/y$ vaznli mediana regressiyasi mos keladi:"),
        ("code", "python", "CODE_SKLEARN"),
        ("p", "PyTorch’da yo‘qotish funksiyasi sifatida MAPE:"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Qoida", "MAPE’ni hisoblashdan oldin ma’lumotlardagi $|y|$ minimumiga qarang. U yerda nollar yoki odatiy qiymatlarga nisbatan juda kichik qiymatlar bo‘lsa, WAPE yoki MASE bilan hisobot bering va MAPE’ni yo‘qotish funksiyasi sifatida ishlatmang."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b>Nollari bor ma’lumotlarda MAPE.</b> Nolga bo‘lish cheksizlik yoki NaN beradi, $\\varepsilon$ orqali «himoya» esa astronomik sonlar beradi: scikit-learn $2{,}25\\cdot10^{15}$ qaytaradi. Nollarni aniq filtrlang va bu haqda xabar bering yoki WAPE va MASE’ni oling.",
            "<b>Shartli nolli shkalalar uchun MAPE</b> — °C dagi harorat, indekslar, sanalar. 2° da ham, 30° da ham 1° xato bir xil, MAPE esa 15 marta farq qiladi.",
            "<b>Siljishni hisobga olmasdan MAPE’da o‘qitish.</b> Model bashoratni sistematik ravishda kamaytiradi, chakana savdoda bu javonlardagi taqchillikka aylanadi.",
            "<b>Kichik qiymatlar ulushi har xil bo‘lgan to‘plamlar orasida MAPE’ni solishtirish.</b> Bitta model tez sotiladigan tovarlarda 12%, sekin sotiladiganlarda 60% ko‘rsatadi — gap sifatda emas, ma’lumotlarda.",
            "<b>Ulush va foizni chalkashtirish</b>: scikit-learn $13{,}9$ emas, $0{,}139$ qaytaradi.",
            "<b>«MAPE kichikroq — demak, reja aniqroq».</b> MAPE xatolar ishorasini ko‘rmaydi: MAPE’si kichikroq bashorat 5-rasmdagi kabi talabni yig‘indida 16% ga kamaytirishi mumkin.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘lanishlar", blocks=[
        ("ul", [
            "<a href=\"../mae/\">MAE</a>: MAPE — $1/|y_i|$ vaznli MAE; gradiyent moduli ham xato kattaligiga bog‘liq emas, lekin $1/|y_i|$ ga masshtablangan.",
            "<a href=\"../mse/\">MSE</a> va <a href=\"../rmse/\">RMSE</a>: absolyut kvadratik xatolar; ularning nisbiy qarindoshi — RMSLE, logarifmik shkaladagi RMSE.",
            "<a href=\"../huber/\">Huber</a>: noldagi sinishni silliqlaydi; xuddi shu g‘oyani nisbiy xatoga ham qo‘llash mumkin.",
            "<a href=\"../sgd/\">SGD</a>: MAPE’da o‘qitish — qadami kamaytirilishi kerak bo‘lgan subgradiyent tushish (5-rasmda — $1/\\sqrt t$ kabi).",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $\\mathrm{MAPE}=\\frac{100\\%}{n}\\sum|y_i-\\hat y_i|/|y_i|$ — haqiqiy qiymatga nisbatan foizdagi o‘rtacha xato; masshtabga bog‘liq emas va biznesga tushunarli. 2) $y=0$ da aniqlanmagan va nol atrofida portlaydi; nol bashorat roppa-rosa $100\\%$ turadi. 3) Marta bo‘yicha nosimmetrik: ikki baravar kam — $50\\%$, ikki baravar ko‘p — $100\\%$. 4) MAPE — $1/|y|$ vaznli MAE: hosila $\\operatorname{sign}(\\hat y-y)/|y|$, eng yaxshi konstanta — oddiysidan past vaznli mediana, MAPE’da o‘qitish kam bashoratga olib keladi. 5) Assortiment bo‘yicha hisobotlar uchun odatda WAPE va MASE ishonchliroq."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="Haqiqiy qiymat 200, bashorat 150. APE nimaga teng?", options=["$25\\%$", "$33{,}3\\%$", "$50\\%$", "$12{,}5\\%$"], answer=0,
                 explain="Haqiqiy qiymatga bo‘lamiz: $50/200=25\\%$. Xato qilib bashoratga bo‘linsa, $33{,}3\\%$ chiqadi."),
            dict(q="Haqiqiy qiymat 100. Qaysi bashorat kattaroq APE beradi: 50 yoki 200?", options=["50", "200", "Bir xil", "$n$ ga bog‘liq"], answer=1,
                 explain="$|100-50|/100=50\\%$, $|100-200|/100=100\\%$ esa. Ikkalasi ham ikki baravar adashgan, lekin ortiq bashorat ikki baravar qimmat."),
            dict(q="Model musbat sotuvlarda doim 0 bashorat qiladi. Uning MAPE’si nimaga teng?", options=["$0\\%$", "$50\\%$", "$100\\%$", "Cheksizlikka"], answer=2,
                 explain="Har bir $\\mathrm{APE}_i=|y_i-0|/|y_i|=1$, shuning uchun istalgan ma’lumotlarda $\\mathrm{MAPE}=100\\%$."),
            dict(q="Haqiqiy qiymatlar: 1, 10 va 100. Qaysi konstant bashorat MAPE’ni minimallashtiradi?", options=["1", "10", "37", "100"], answer=0,
                 explain="$1/y_i$ vaznlar $1$, $0{,}1$ va $0{,}01$ ga teng; birinchi obyekt vazni qolganlari yig‘indisidan katta, shuning uchun vaznli mediana — 1: $\\mathrm{MAPE}=(0+0{,}9+0{,}99)/3=63\\%$, $c=10$ da esa $330\\%$."),
            dict(q="Nega kam sotiladigan tovarlari bor assortimentda WAPE MAPE’dan barqarorroq?", options=["WAPE kam sotiladigan tovarlar xatolarini hisobga olmaydi", "WAPE umumiy xatoni umumiy haqiqiy qiymatga bo‘ladi, va kichik haqiqiy qiymatlar ulkan vazn olmaydi", "WAPE doim MAPE’dan kichik", "WAPE xatolarni kvadratga oshiradi"], answer=1,
                 explain="WAPE’da har bir obyekt o‘zining donadagi absolyut xatosi bilan kiradi, bo‘lish esa bir marta — haqiqiy qiymatlar yig‘indisiga bajariladi. Kam sotiladigan tovarning 6 donalik xatosi 6 donalik xato bo‘lib qoladi."),
        ]),
    ]),
],
}

# Fill in the shared pieces (tables and code listings) per language.
for _lang, _secs in SECTIONS.items():
    for _sec in _secs:
        for _i, _b in enumerate(_sec["blocks"]):
            if _b[0] == "table" and _b[2] == "TABLE":
                _sec["blocks"][_i] = (_b[0], _b[1], _table(_lang), _b[3])
            elif _b[0] == "table" and _b[2] == "ALT":
                _sec["blocks"][_i] = (_b[0], _b[1], ALT[_lang], _b[3])
            elif _b[0] == "code" and _b[2] in ("CODE_NUMPY", "CODE_SKLEARN", "CODE_TORCH"):
                _sec["blocks"][_i] = (_b[0], _b[1], _code({"CODE_NUMPY": CODE_NUMPY, "CODE_SKLEARN": CODE_SKLEARN, "CODE_TORCH": CODE_TORCH}[_b[2]], _lang))
