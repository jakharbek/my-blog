"""Formula page: the sigmoid (logistic function). Reference page for the format, see README.md."""

META = dict(
    id="sigmoid",
    date="2026-10-28",
    minutes=30,
    hero=r"\sigma(x)=\frac{1}{1+e^{-x}}",
    title={"ru": "Сигмоида: логистическая функция", "en": "The sigmoid: the logistic function", "uz": "Sigmoida: logistik funksiya"},
    dek={
        "ru": "Функция, которая превращает любое число в вероятность. Разбираем её по косточкам: из чего собрана формула, откуда берётся производная σ(1 − σ), как сигмоида строит решающую границу логистической регрессии и почему из-за неё затухают градиенты в глубоких сетях.",
        "en": "The function that turns any number into a probability. We take it apart bone by bone: what the formula is made of, where the derivative σ(1 − σ) comes from, how the sigmoid draws the decision boundary of logistic regression, and why it makes gradients vanish in deep networks.",
        "uz": "Istalgan sonni ehtimollikka aylantiradigan funksiya. Uni mayda detallarigacha tahlil qilamiz: formula nimadan yig‘ilgan, σ(1 − σ) hosila qayerdan keladi, sigmoida logistik regressiyaning qaror chegarasini qanday chizadi va nega chuqur tarmoqlarda gradiyentlarni so‘ndiradi.",
    },
    description={
        "ru": "Сигмоида подробно: формула, свойства, вывод производной, ряд Тейлора, логит и шансы, логистическая регрессия в 3D, насыщение и затухание градиента, устойчивый код.",
        "en": "The sigmoid in depth: formula, properties, derivation of the derivative, Taylor series, logit and odds, logistic regression in 3D, saturation and vanishing gradients, stable code.",
        "uz": "Sigmoida batafsil: formula, xossalar, hosilani keltirib chiqarish, Teylor qatori, logit va imkoniyatlar, 3D’da logistik regressiya, to‘yinish va gradiyent so‘nishi, barqaror kod.",
    },
)

TABLE = [(-6, "0.0025", "0.0025"), (-4, "0.0180", "0.0177"), (-2, "0.1192", "0.1050"), (-1, "0.2689", "0.1966"), (0, "0.5000", "0.2500"),
         (1, "0.7311", "0.1966"), (2, "0.8808", "0.1050"), (4, "0.9820", "0.0177"), (6, "0.9975", "0.0025")]


def _table(lang):
    dec = "." if lang == "en" else ","
    m = lambda v: str(v).replace("-", "−")
    return [[m(x), s.replace(".", dec), d.replace(".", dec)] for x, s, d in TABLE]


CODE_NUMPY = '''import numpy as np

def sigmoid(x):
    """Устойчивая сигмоида: exp никогда не получает большой положительный аргумент."""
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    pos = x >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-x[pos]))
    ex = np.exp(x[~pos])
    out[~pos] = ex / (1.0 + ex)
    return out

def sigmoid_grad(x):
    s = sigmoid(x)
    return s * (1.0 - s)

def log_sigmoid(x):
    # log σ(x) = −softplus(−x) = −log(1 + e^(−x)), без log(0)
    return -np.logaddexp(0.0, -x)

print(sigmoid([-40.0, 0.0, 40.0]))   # [4.248e-18 0.5 1.0]
print(1 - sigmoid(40.0), sigmoid(-40.0))  # 0.0 против 4.248e-18'''

CODE_TORCH = '''import torch
import torch.nn as nn

z = torch.tensor([-2.0, 0.0, 2.0], requires_grad=True)
p = torch.sigmoid(z)            # tensor([0.1192, 0.5000, 0.8808])
p.sum().backward()
print(z.grad)                   # tensor([0.1050, 0.2500, 0.1050]) = σ(1 − σ)

# Для классификации отдавайте в потерю логиты, а не σ(z):
loss_fn = nn.BCEWithLogitsLoss()  # внутри — устойчивый log σ(z)
loss = loss_fn(z, torch.tensor([0.0, 1.0, 1.0]))'''


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("Устойчивая сигмоида: exp никогда не получает большой положительный аргумент.", "Stable sigmoid: exp never gets a large positive argument."),
               ("без log(0)", "without log(0)"), ("0.0 против 4.248e-18", "0.0 versus 4.248e-18"),
               ("Для классификации отдавайте в потерю логиты, а не σ(z):", "For classification pass the logits to the loss, not σ(z):"),
               ("внутри — устойчивый log σ(z)", "a stable log σ(z) inside")],
        "uz": [("Устойчивая сигмоида: exp никогда не получает большой положительный аргумент.", "Barqaror sigmoida: exp hech qachon katta musbat argument olmaydi."),
               ("без log(0)", "log(0) siz"), ("0.0 против 4.248e-18", "0.0 va 4.248e-18"),
               ("Для классификации отдавайте в потерю логиты, а не σ(z):", "Klassifikatsiyada yo‘qotishga σ(z) emas, logitlarni bering:"),
               ("внутри — устойчивый log σ(z)", "ichida — barqaror log σ(z)")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", "Нейросеть, логистическая регрессия, градиентный бустинг — внутри у всех получается просто число: $3{,}7$, $-12$, $0{,}2$. Но вопрос часто звучит иначе: <i>с какой вероятностью</i> письмо — спам, клиент вернёт кредит, на кадре человек. Вероятность обязана лежать между 0 и 1. Сигмоида — самый естественный мост от «любого числа» к «вероятности»."),
        ("p", "Где она встречается:"),
        ("ul", [
            "<b>выход бинарного классификатора</b> — логистическая регрессия, последний нейрон сети, $p=\\sigma(z)$;",
            "<b>вентили (gates) в LSTM и GRU</b> — число от 0 до 1 решает, какую долю информации пропустить, а какую забыть;",
            "<b>градиентный бустинг для классификации</b> — XGBoost, LightGBM и CatBoost складывают деревья в «сырой» счёт, а сигмоида превращает его в вероятность;",
            "<b>современные активации</b> — SiLU (Swish) в LLaMA и Qwen — это $x\\cdot\\sigma(x)$;",
            "<b>статистика</b> — функция распределения логистического закона и связь вероятности с логарифмом шансов (logit).",
        ]),
        ("callout", "key", "Главное за минуту", "$\\sigma$ сжимает всю числовую прямую в интервал $(0;\\,1)$, проходит через $(0;\\,0{,}5)$, симметрична: $\\sigma(-x)=1-\\sigma(x)$. Её производная $\\sigma'=\\sigma(1-\\sigma)$ не больше $0{,}25$ — отсюда и удобство (дешёвый backprop), и беда (затухание градиента)."),
    ]),
    dict(id="intuition", title="Интуиция: сжать бесконечность", blocks=[
        ("p", "Представьте дорогу между полом $y=0$ и потолком $y=1$. Слева дорога почти лежит на полу, справа почти касается потолка, а посередине плавно поднимается. Сколько бы вы ни шли влево или вправо, пол и потолок останутся недостижимы — это <b>асимптоты</b>."),
        ("p", "Потяните точку на графике. Оранжевая прямая — касательная: её наклон и есть производная $\\sigma'(x)$. В центре подъём самый крутой, а на краях дорога почти горизонтальна — производная там близка к нулю."),
        ("viz", "sigmoid-explorer", {"x": 1.5}, "<b>Рисунок 1.</b> Сигмоида, её касательная и производная. Тяните синюю точку или нажимайте стрелки, когда она в фокусе. Максимум производной $0{,}25$ — ровно под центром $x=0$."),
        ("callout", "intuition", "Что заметить", "При $x=4$ сигмоида уже $0{,}982$, а производная — всего $0{,}018$, в 14 раз меньше, чем в центре. Это насыщение (saturation): дальше вход растёт, а выход почти не меняется."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", "Соберём сигмоиду из трёх простых действий и проследим, что каждое делает с числом $x$."),
        ("eq", r"x\;\xrightarrow{\;\cdot(-1)\;}\;-x\;\xrightarrow{\;\exp\;}\;e^{-x}\in(0;\,\infty)\;\xrightarrow{\;+1\;}\;1+e^{-x}\in(1;\,\infty)\;\xrightarrow{\;1/\cdot\;}\;\sigma(x)\in(0;\,1)"),
        ("symbols", [
            (r"e^{-x}", "экспонента всегда положительна: при $x\\to+\\infty$ она стремится к 0, при $x\\to-\\infty$ — к бесконечности;"),
            (r"1+e^{-x}", "знаменатель всегда больше 1 — поэтому дробь всегда меньше 1;"),
            (r"\frac{1}{1+e^{-x}}", "обратная величина положительного числа больше 1 лежит строго между 0 и 1."),
        ]),
        ("p", "Ту же функцию полезно узнавать в других записях:"),
        ("eq", r"\sigma(x)=\frac{1}{1+e^{-x}}=\frac{e^{x}}{1+e^{x}}=\frac{1}{2}\Bigl(1+\tanh\frac{x}{2}\Bigr)"),
        ("p", "Вторая форма получается умножением числителя и знаменателя на $e^x$; она удобна для отрицательных $x$ (см. раздел про код). Третья связывает сигмоиду с гиперболическим тангенсом: tanh — это та же S-кривая, растянутая в два раза по высоте и сдвинутая вниз."),
        ("table", ["$x$", "$\\sigma(x)$", "$\\sigma'(x)$"], "TABLE", {"num": [0, 1, 2]}),
        ("p", "Таблица показывает две симметрии: значения сигмоиды при $\\pm x$ дополняют друг друга до единицы, а производная — чётная функция."),
    ]),
    dict(id="properties", title="Свойства и форма", blocks=[
        ("ul", [
            "<b>Область определения</b> — все действительные числа; <b>область значений</b> — открытый интервал $(0;\\,1)$.",
            "<b>Монотонность</b>: строго возрастает, потому что $\\sigma'(x)&gt;0$ при любом $x$.",
            "<b>Асимптоты</b>: $\\lim_{x\\to-\\infty}\\sigma(x)=0$ и $\\lim_{x\\to+\\infty}\\sigma(x)=1$.",
            "<b>Центральная симметрия</b> относительно точки $(0;\\,0{,}5)$: $\\sigma(-x)=1-\\sigma(x)$.",
            "<b>Точка перегиба</b> — единственная, $x=0$: слева функция выпукла вниз, справа — вверх.",
            "<b>Липшицевость</b>: $|\\sigma(a)-\\sigma(b)|\\le\\tfrac14|a-b|$ — выход меняется не быстрее, чем на четверть изменения входа.",
        ]),
        ("deep", "Почему σ(−x) = 1 − σ(x)", [
            ("eq", r"1-\sigma(x)=1-\frac{1}{1+e^{-x}}=\frac{e^{-x}}{1+e^{-x}}=\frac{1}{e^{x}+1}=\sigma(-x)"),
            ("p", "В предпоследнем шаге числитель и знаменатель умножены на $e^{x}$."),
        ]),
        ("h3", "Вес и сдвиг: как нейрон перестраивает сигмоиду"),
        ("p", "В нейроне сигмоида получает не $x$, а $z=wx+b$. Вес $w$ растягивает кривую по горизонтали, сдвиг $b$ двигает её. Центр, где выход равен $0{,}5$, оказывается в точке $x_0=-b/w$, а наклон в центре равен $w/4$."),
        ("viz", "sigmoid-shape", {"w": 2, "b": -2}, "<b>Рисунок 2.</b> $\\sigma(wx+b)$. При большом $|w|$ кривая превращается почти в ступеньку, при $w&lt;0$ — переворачивается. Бледные кривые — та же функция с весами $w/4$ и $w/2$."),
        ("callout", "note", "Ступенька как предел", "При $w\\to+\\infty$ функция $\\sigma(w x)$ стремится к ступеньке Хевисайда: 0 слева от нуля, 1 справа. Так сигмоида исторически и появилась в нейросетях — как гладкая, дифференцируемая замена пороговому нейрону Маккаллока — Питтса."),
    ]),
    dict(id="derivative", title="Производная: σ′ = σ(1 − σ)", blocks=[
        ("p", "Это главная формула страницы. Выведем её двумя способами — «в лоб» и изящно."),
        ("deep", "Способ 1. Производная частного (по шагам)", [
            ("p", "Запишем $\\sigma(x)=(1+e^{-x})^{-1}$ и применим правило производной сложной функции:"),
            ("eq", r"\sigma'(x)=-(1+e^{-x})^{-2}\cdot\bigl(1+e^{-x}\bigr)'=-(1+e^{-x})^{-2}\cdot(-e^{-x})=\frac{e^{-x}}{(1+e^{-x})^{2}}"),
            ("p", "Разобьём дробь на произведение двух сомножителей:"),
            ("eq", r"\frac{e^{-x}}{(1+e^{-x})^{2}}=\underbrace{\frac{1}{1+e^{-x}}}_{\sigma(x)}\cdot\underbrace{\frac{e^{-x}}{1+e^{-x}}}_{1-\sigma(x)}"),
            ("p", "Второй сомножитель — это $1-\\sigma(x)$, мы доказали это в разделе о свойствах."),
        ]),
        ("deep", "Способ 2. Через логарифм", [
            ("p", "Возьмём логарифм: $\\ln\\sigma(x)=-\\ln(1+e^{-x})$. Продифференцируем обе части:"),
            ("eq", r"\frac{\sigma'(x)}{\sigma(x)}=\frac{e^{-x}}{1+e^{-x}}=1-\sigma(x)\quad\Longrightarrow\quad\sigma'(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)"),
        ]),
        ("eq", r"\sigma'(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)"),
        ("p", "Почему это важно на практике: на прямом проходе сеть уже посчитала $s=\\sigma(z)$. На обратном проходе производная обходится одним умножением $s(1-s)$ — без новой экспоненты."),
        ("h3", "Максимум производной и вторая производная"),
        ("p", "Произведение $s(1-s)$ при $s\\in(0;1)$ — перевёрнутая парабола с вершиной в $s=\\tfrac12$. Значит, $\\max\\sigma'=\\tfrac12\\cdot\\tfrac12=\\tfrac14$, и достигается он при $x=0$. Дифференцируя ещё раз:"),
        ("eq", r"\sigma''(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)\bigl(1-2\sigma(x)\bigr)"),
        ("p", "Вторая производная обращается в ноль при $\\sigma=\\tfrac12$, то есть в точке перегиба $x=0$. Её экстремумы — в точках $x=\\pm\\ln(2+\\sqrt3)\\approx\\pm1{,}317$, где наклон сигмоиды меняется быстрее всего; значение там $\\mp\\sqrt3/18\\approx\\mp0{,}096$."),
        ("h3", "Ряд Тейлора около нуля"),
        ("p", "Из связи с tanh получаем разложение:"),
        ("eq", r"\sigma(x)=\frac12+\frac{x}{4}-\frac{x^{3}}{48}+\frac{x^{5}}{480}-\frac{17x^{7}}{80640}+\dots"),
        ("p", "Около нуля сигмоида почти линейна: $\\sigma(x)\\approx\\tfrac12+\\tfrac{x}{4}$. Именно поэтому при маленьких весах сеть с сигмоидами ведёт себя почти как линейная модель. Ряд сходится только при $|x|&lt;\\pi$: у функции есть особые точки в комплексной плоскости, $x=\\pm i\\pi$."),
        ("viz", "sigmoid-taylor", {}, "<b>Рисунок 3.</b> Многочлены Тейлора порядков 1, 3, 5, 7. Внутри полосы $|x|&lt;\\pi$ точность растёт с порядком, за её пределами многочлены уходят от сигмоиды тем сильнее, чем выше порядок. При $x=2$ приближение третьего порядка даёт $0{,}833$ вместо $0{,}881$."),
    ]),
    dict(id="probability", title="Вероятностный смысл: шансы и логит", blocks=[
        ("p", "Почему выход сигмоиды разумно читать как вероятность? Пусть $p$ — вероятность события. Отношение $p/(1-p)$ называют <b>шансами</b> (odds): при $p=0{,}8$ шансы $4:1$. Логарифм шансов — <b>логит</b>:"),
        ("eq", r"\operatorname{logit}(p)=\ln\frac{p}{1-p}\qquad\Longleftrightarrow\qquad p=\sigma\bigl(\operatorname{logit}(p)\bigr)"),
        ("p", "Логит и сигмоида — взаимно обратные функции. Логит переводит вероятность из $(0;1)$ на всю числовую прямую, где удобно складывать вклады признаков. Логистическая регрессия предполагает ровно это: <b>логарифм шансов линейно зависит от признаков</b>, $\\ln\\frac{p}{1-p}=w^\\top x+b$. Отсюда и сигмоида на выходе."),
        ("viz", "sigmoid-logit", {"p": 0.8}, "<b>Рисунок 4.</b> Слева сигмоида переводит логит $z$ в вероятность $p$, справа логит возвращает обратно. При $p=0{,}8$ шансы равны 4, логит $\\ln4\\approx1{,}386$. Обратите внимание: логит быстро растёт у краях — от $p=0{,}99$ до $p=0{,}999$ он меняется на $2{,}3$."),
        ("callout", "note", "Ещё одна интерпретация", "Сигмоида — функция распределения логистического закона: если шум $\\varepsilon$ имеет логистическое распределение, то $P(\\varepsilon\\le x)=\\sigma(x)$. Похожая модель с нормальным шумом, $\\Phi(x)$, называется пробит-регрессией; её кривая почти совпадает с $\\sigma(1{,}7x)$."),
    ]),
    dict(id="space", title="Сигмоида в многомерном пространстве", blocks=[
        ("p", "У нейрона много входов: $z=w_1x_1+w_2x_2+\\dots+b$. Сигмоида от гиперплоскости — это «складка», которая поднимается от 0 до 1 поперёк границы $w^\\top x+b=0$ и не меняется вдоль неё. Вектор весов $w$ указывает направление самого крутого подъёма, а его длина — крутизну складки."),
        ("viz", "sigmoid-logreg", {"w1": -0.5, "w2": 1.5, "b": 1.5}, "<b>Рисунок 5.</b> Логистическая регрессия на двух признаках. Слева — поверхность вероятности в 3D (её можно вращать), точки стоят на высоте своего класса. Справа — вид сверху: сплошная линия — граница $p=0{,}5$, пунктир — $p=0{,}1$ и $p=0{,}9$, стрелка — направление $w$. Нажмите «Пуск»: градиентный спуск по BCE с шагом $0{,}5$ сам находит веса."),
        ("p", "Обучение использует ту же производную. Для потери BCE градиент по логиту равен $\\sigma(z)-y$ (вывод — на странице <a href=\"../bce/\">BCE</a>), поэтому шаг градиентного спуска по весам:"),
        ("eq", r"w\leftarrow w-\eta\,\frac1n\sum_{i=1}^{n}\bigl(\sigma(w^\top x_i+b)-y_i\bigr)\,x_i"),
        ("callout", "warn", "Линейно разделимые данные", "Если классы можно идеально разделить прямой, BCE продолжает уменьшаться при росте $\\|w\\|$: складка становится всё круче и стремится к ступеньке, веса уходят в бесконечность. На практике это лечат регуляризацией ($L_2$) или ранней остановкой."),
    ]),
    dict(id="training", title="Сигмоида в обучении: насыщение и затухание градиента", blocks=[
        ("p", "Если входы нейрона $z$ велики по модулю, сигмоида работает на плоских хвостах, где $\\sigma'(z)\\approx0$. Градиент через такой нейрон почти не проходит — нейрон <b>насыщен</b>. Насыщение $\\sigma'&lt;0{,}01$ начинается при $|z|&gt;4{,}6$."),
        ("viz", "sigmoid-saturation", {"s": 1}, "<b>Рисунок 6.</b> Синяя область — распределение входов $z\\sim N(\\mu,\\,s^2)$, оранжевая — производная. При $s=1$ средняя производная $0{,}207$ и насыщенных входов почти нет; при $s=4$ средняя производная падает до $0{,}091$, а насыщена уже четверть входов ($25\\%$)."),
        ("p", "Отсюда правило инициализации: веса выбирают так, чтобы дисперсия $z$ была порядка единицы (инициализация Ксавье — Глоро, $\\operatorname{Var}w=1/n_{\\text{in}}$), а данные нормализуют."),
        ("h3", "Затухание градиента в глубокой сети"),
        ("p", "По цепному правилу градиент на слое $l$ — произведение производных всех слоёв выше. У сигмоиды каждая производная не больше $\\tfrac14$, поэтому через 10 слоёв множитель не больше $0{,}25^{10}\\approx9{,}5\\cdot10^{-7}$."),
        ("eq", r"\frac{\partial L}{\partial h_l}=\frac{\partial L}{\partial h_L}\prod_{k=l+1}^{L}W_k^{\top}\operatorname{diag}\bigl(\sigma'(z_k)\bigr)"),
        ("viz", "sigmoid-vanishing", {"depth": 10}, "<b>Рисунок 7.</b> Норма градиента на каждом слое случайной сети ширины 64 (инициализация Ксавье для sigmoid и tanh, Хе для ReLU). Шкала по вертикали логарифмическая. У сигмоиды градиент у входа меньше, чем у выхода, на несколько порядков; у tanh и ReLU он почти не затухает."),
        ("callout", "history", "Почему сигмоида ушла из скрытых слоёв", "До 2010 года глубокие сети с сигмоидами обучались плохо. Гло́ро и Бенжио (2010) показали роль насыщения и предложили инициализацию, а ReLU (Наир и Хинтон, 2010; Глоро и др., 2011) почти сняли проблему. Сегодня сигмоида живёт там, где нужна именно доля от 0 до 1: на выходе бинарного классификатора и в вентилях."),
    ]),
    dict(id="code", title="В коде: устойчиво и без сюрпризов", blocks=[
        ("p", "Наивная формула $1/(1+e^{-x})$ при $x=-1000$ вычисляет $e^{1000}$ — переполнение. Результат всё равно получится 0, но с предупреждением, а в $\\log\\sigma(x)$ уже появится $-\\infty$. Вторая проблема — потеря точности: $1-\\sigma(40)$ в float64 равно ровно 0, хотя истинное значение $\\sigma(-40)\\approx4{,}25\\cdot10^{-18}$."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Правило", "Если дальше идёт логарифм — не считайте $\\sigma$ отдельно. Используйте $\\log\\sigma(x)=-\\operatorname{softplus}(-x)$ или готовые потери на логитах: <code>BCEWithLogitsLoss</code> в PyTorch, <code>from_logits=True</code> в Keras."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>Сигмоида в скрытых слоях глубокой сети</b> — затухание градиента и смещённые (не центрированные) активации. Берите ReLU, GELU, SiLU; сигмоиду — только на выходе или в вентилях.",
            "<b>Сигмоида + softmax на одном выходе.</b> Для $K&gt;2$ взаимоисключающих классов нужен <a href=\"../softmax/\">softmax</a>; сигмоида на каждом выходе — это multi-label, где классы независимы.",
            "<b>Двойная сигмоида</b>: модель уже возвращает вероятность, а потеря применяет σ ещё раз (например, <code>BCEWithLogitsLoss</code> поверх <code>sigmoid</code>). Обучение идёт, но градиенты искажены.",
            "<b>Порог 0,5 «по умолчанию»</b>. Он оптимален только для равных цен ошибок и сбалансированных классов. Порог подбирают по метрике на валидации.",
            "<b>Вывод «σ(z) = 0,9, значит модель уверена на 90%»</b> без калибровки. Сигмоида даёт число в $(0;1)$, но откалиброванность — свойство обучения (BCE способствует ей, переобучение — портит).",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../tanh/\">tanh</a>: $\\tanh x=2\\sigma(2x)-1$ — центрированная сигмоида с максимальным наклоном 1.",
            "<a href=\"../softmax/\">Softmax</a>: для двух классов $\\operatorname{softmax}(z_1,z_2)_1=\\sigma(z_1-z_2)$.",
            "<a href=\"../bce/\">BCE</a>: в паре с сигмоидой даёт градиент $\\hat y-y$ — без множителя $\\sigma'$, а значит без насыщения при ошибке.",
            "<a href=\"../silu/\">SiLU / Swish</a>: $x\\,\\sigma(x)$ — сигмоида как «мягкий вентиль» для самого входа.",
            "<a href=\"../focal/\">Focal Loss</a>: обычно считается от $p_t=\\sigma(z)$ для правильного класса.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $\\sigma(x)=1/(1+e^{-x})$ отображает $\\mathbb R$ в $(0;1)$, проходит через $(0;\\,0{,}5)$ и симметрична: $\\sigma(-x)=1-\\sigma(x)$. 2) $\\sigma'=\\sigma(1-\\sigma)\\le\\tfrac14$: backprop дешёвый, но на хвостах градиент гаснет. 3) Сигмоида обратна логиту: логистическая регрессия моделирует логарифм шансов линейной функцией. 4) В многомерном случае это складка вдоль гиперплоскости $w^\\top x+b=0$. 5) В коде — устойчивые формы и потери на логитах."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="Чему равна $\\sigma(-3)$, если $\\sigma(3)\\approx0{,}953$?", options=["$-0{,}953$", "$0{,}047$", "$0{,}953$", "$1/0{,}953$"], answer=1,
                 explain="По симметрии $\\sigma(-x)=1-\\sigma(x)=1-0{,}953=0{,}047$."),
            dict(q="Какое наибольшее значение принимает производная сигмоиды?", options=["$1$", "$0{,}5$", "$0{,}25$", "Не ограничена"], answer=2,
                 explain="$\\sigma'=s(1-s)$ при $s\\in(0;1)$ максимальна при $s=\\tfrac12$: $\\tfrac14$."),
            dict(q="Нейрон считает $\\sigma(wx+b)$ с $w=2$, $b=-4$. Где выход равен $0{,}5$?", options=["$x=-2$", "$x=0$", "$x=2$", "$x=4$"], answer=2,
                 explain="Центр $x_0=-b/w=4/2=2$."),
            dict(q="Почему в PyTorch для бинарной классификации советуют BCEWithLogitsLoss вместо sigmoid + BCELoss?", options=["Она быстрее обучает", "Она устойчиво считает $\\log\\sigma(z)$ без переполнения и log(0)", "Она не требует меток", "Она добавляет регуляризацию"], answer=1,
                 explain="Функция объединяет сигмоиду и логарифм в одну устойчивую формулу через softplus."),
            dict(q="Какой множитель затухания градиента даёт цепочка из 5 сигмоид в лучшем случае?", options=["$0{,}25^5\\approx0{,}001$", "$0{,}5^5\\approx0{,}03$", "$1$", "$5\\cdot0{,}25$"], answer=0,
                 explain="Каждая производная не больше $\\tfrac14$, поэтому произведение не больше $0{,}25^5\\approx9{,}8\\cdot10^{-4}$."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "A neural network, logistic regression, gradient boosting — inside all of them you end up with a plain number: $3.7$, $-12$, $0.2$. But the question is often different: <i>how likely</i> is the email spam, will the client repay the loan, is there a person in the frame. A probability must lie between 0 and 1. The sigmoid is the most natural bridge from “any number” to “a probability”."),
        ("p", "Where it appears:"),
        ("ul", [
            "<b>the output of a binary classifier</b> — logistic regression, the last neuron of a network, $p=\\sigma(z)$;",
            "<b>gates in LSTM and GRU</b> — a number between 0 and 1 decides what share of the information to let through and what to forget;",
            "<b>gradient boosting for classification</b> — XGBoost, LightGBM and CatBoost add trees into a raw score, and the sigmoid turns it into a probability;",
            "<b>modern activations</b> — SiLU (Swish) in LLaMA and Qwen is $x\\cdot\\sigma(x)$;",
            "<b>statistics</b> — the cumulative distribution function of the logistic law and the link between probability and log-odds (logit).",
        ]),
        ("callout", "key", "The essentials in a minute", "$\\sigma$ squeezes the whole real line into $(0,\\,1)$, passes through $(0,\\,0.5)$ and is symmetric: $\\sigma(-x)=1-\\sigma(x)$. Its derivative $\\sigma'=\\sigma(1-\\sigma)$ never exceeds $0.25$ — the source of both convenience (cheap backprop) and trouble (vanishing gradients)."),
    ]),
    dict(id="intuition", title="Intuition: squeezing infinity", blocks=[
        ("p", "Picture a road between a floor at $y=0$ and a ceiling at $y=1$. On the left the road almost lies on the floor, on the right it almost touches the ceiling, and in the middle it rises smoothly. However far you walk left or right, the floor and the ceiling stay out of reach — they are the <b>asymptotes</b>."),
        ("p", "Drag the point on the plot. The orange line is the tangent: its slope is the derivative $\\sigma'(x)$. The climb is steepest at the centre, while at the edges the road is almost flat — the derivative there is close to zero."),
        ("viz", "sigmoid-explorer", {"x": 1.5}, "<b>Figure 1.</b> The sigmoid, its tangent and its derivative. Drag the blue point, or use the arrow keys when it has focus. The maximum of the derivative, $0.25$, sits exactly under the centre $x=0$."),
        ("callout", "intuition", "What to notice", "At $x=4$ the sigmoid is already $0.982$, while the derivative is only $0.018$, 14 times smaller than at the centre. This is saturation: the input keeps growing, but the output barely changes."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("p", "Let us assemble the sigmoid from three simple steps and follow what each one does to the number $x$."),
        ("eq", r"x\;\xrightarrow{\;\cdot(-1)\;}\;-x\;\xrightarrow{\;\exp\;}\;e^{-x}\in(0,\,\infty)\;\xrightarrow{\;+1\;}\;1+e^{-x}\in(1,\,\infty)\;\xrightarrow{\;1/\cdot\;}\;\sigma(x)\in(0,\,1)"),
        ("symbols", [
            (r"e^{-x}", "the exponential is always positive: as $x\\to+\\infty$ it tends to 0, as $x\\to-\\infty$ to infinity;"),
            (r"1+e^{-x}", "the denominator is always greater than 1 — so the fraction is always less than 1;"),
            (r"\frac{1}{1+e^{-x}}", "the reciprocal of a positive number greater than 1 lies strictly between 0 and 1."),
        ]),
        ("p", "It pays to recognise the same function in other forms:"),
        ("eq", r"\sigma(x)=\frac{1}{1+e^{-x}}=\frac{e^{x}}{1+e^{x}}=\frac{1}{2}\Bigl(1+\tanh\frac{x}{2}\Bigr)"),
        ("p", "The second form comes from multiplying the numerator and the denominator by $e^x$; it is convenient for negative $x$ (see the section on code). The third links the sigmoid to the hyperbolic tangent: tanh is the same S-curve, stretched twice as tall and shifted down."),
        ("table", ["$x$", "$\\sigma(x)$", "$\\sigma'(x)$"], "TABLE", {"num": [0, 1, 2]}),
        ("p", "The table shows two symmetries: the sigmoid values at $\\pm x$ add up to one, and the derivative is an even function."),
    ]),
    dict(id="properties", title="Properties and shape", blocks=[
        ("ul", [
            "<b>Domain</b>: all real numbers; <b>range</b>: the open interval $(0,\\,1)$.",
            "<b>Monotonicity</b>: strictly increasing, since $\\sigma'(x)&gt;0$ for every $x$.",
            "<b>Asymptotes</b>: $\\lim_{x\\to-\\infty}\\sigma(x)=0$ and $\\lim_{x\\to+\\infty}\\sigma(x)=1$.",
            "<b>Point symmetry</b> about $(0,\\,0.5)$: $\\sigma(-x)=1-\\sigma(x)$.",
            "<b>Inflection point</b>: a single one, at $x=0$; the function is convex on the left and concave on the right.",
            "<b>Lipschitz continuity</b>: $|\\sigma(a)-\\sigma(b)|\\le\\tfrac14|a-b|$ — the output changes no faster than a quarter of the change in the input.",
        ]),
        ("deep", "Why σ(−x) = 1 − σ(x)", [
            ("eq", r"1-\sigma(x)=1-\frac{1}{1+e^{-x}}=\frac{e^{-x}}{1+e^{-x}}=\frac{1}{e^{x}+1}=\sigma(-x)"),
            ("p", "In the second-to-last step the numerator and the denominator are multiplied by $e^{x}$."),
        ]),
        ("h3", "Weight and bias: how a neuron reshapes the sigmoid"),
        ("p", "In a neuron the sigmoid receives not $x$ but $z=wx+b$. The weight $w$ stretches the curve horizontally, the bias $b$ shifts it. The centre, where the output equals $0.5$, lands at $x_0=-b/w$, and the slope at the centre is $w/4$."),
        ("viz", "sigmoid-shape", {"w": 2, "b": -2}, "<b>Figure 2.</b> $\\sigma(wx+b)$. For large $|w|$ the curve becomes almost a step; for $w&lt;0$ it flips. The pale curves are the same function with weights $w/4$ and $w/2$."),
        ("callout", "note", "A step as the limit", "As $w\\to+\\infty$, $\\sigma(w x)$ tends to the Heaviside step: 0 to the left of zero, 1 to the right. That is how the sigmoid historically entered neural networks — as a smooth, differentiable replacement for the McCulloch–Pitts threshold neuron."),
    ]),
    dict(id="derivative", title="The derivative: σ′ = σ(1 − σ)", blocks=[
        ("p", "This is the key formula of the page. Let us derive it in two ways — head-on and elegantly."),
        ("deep", "Method 1. The quotient, step by step", [
            ("p", "Write $\\sigma(x)=(1+e^{-x})^{-1}$ and apply the chain rule:"),
            ("eq", r"\sigma'(x)=-(1+e^{-x})^{-2}\cdot\bigl(1+e^{-x}\bigr)'=-(1+e^{-x})^{-2}\cdot(-e^{-x})=\frac{e^{-x}}{(1+e^{-x})^{2}}"),
            ("p", "Split the fraction into a product of two factors:"),
            ("eq", r"\frac{e^{-x}}{(1+e^{-x})^{2}}=\underbrace{\frac{1}{1+e^{-x}}}_{\sigma(x)}\cdot\underbrace{\frac{e^{-x}}{1+e^{-x}}}_{1-\sigma(x)}"),
            ("p", "The second factor is $1-\\sigma(x)$, as shown in the section on properties."),
        ]),
        ("deep", "Method 2. Through the logarithm", [
            ("p", "Take the logarithm: $\\ln\\sigma(x)=-\\ln(1+e^{-x})$. Differentiate both sides:"),
            ("eq", r"\frac{\sigma'(x)}{\sigma(x)}=\frac{e^{-x}}{1+e^{-x}}=1-\sigma(x)\quad\Longrightarrow\quad\sigma'(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)"),
        ]),
        ("eq", r"\sigma'(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)"),
        ("p", "Why this matters in practice: on the forward pass the network has already computed $s=\\sigma(z)$. On the backward pass the derivative costs a single multiplication $s(1-s)$ — no new exponential."),
        ("h3", "The maximum of the derivative and the second derivative"),
        ("p", "The product $s(1-s)$ for $s\\in(0,1)$ is an upside-down parabola with its vertex at $s=\\tfrac12$. Hence $\\max\\sigma'=\\tfrac12\\cdot\\tfrac12=\\tfrac14$, reached at $x=0$. Differentiating once more:"),
        ("eq", r"\sigma''(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)\bigl(1-2\sigma(x)\bigr)"),
        ("p", "The second derivative vanishes at $\\sigma=\\tfrac12$, i.e. at the inflection point $x=0$. Its extrema are at $x=\\pm\\ln(2+\\sqrt3)\\approx\\pm1.317$, where the slope of the sigmoid changes fastest; the value there is $\\mp\\sqrt3/18\\approx\\mp0.096$."),
        ("h3", "The Taylor series around zero"),
        ("p", "From the link with tanh we get the expansion:"),
        ("eq", r"\sigma(x)=\frac12+\frac{x}{4}-\frac{x^{3}}{48}+\frac{x^{5}}{480}-\frac{17x^{7}}{80640}+\dots"),
        ("p", "Near zero the sigmoid is almost linear: $\\sigma(x)\\approx\\tfrac12+\\tfrac{x}{4}$. That is why a network of sigmoids with small weights behaves almost like a linear model. The series converges only for $|x|&lt;\\pi$: the function has singular points in the complex plane at $x=\\pm i\\pi$."),
        ("viz", "sigmoid-taylor", {}, "<b>Figure 3.</b> Taylor polynomials of orders 1, 3, 5 and 7. Inside the band $|x|&lt;\\pi$ accuracy improves with the order; outside it the higher the order, the faster the polynomial leaves the sigmoid. At $x=2$ the third-order approximation gives $0.833$ instead of $0.881$."),
    ]),
    dict(id="probability", title="The probabilistic meaning: odds and the logit", blocks=[
        ("p", "Why is it reasonable to read the sigmoid’s output as a probability? Let $p$ be the probability of an event. The ratio $p/(1-p)$ is called the <b>odds</b>: at $p=0.8$ the odds are $4:1$. The logarithm of the odds is the <b>logit</b>:"),
        ("eq", r"\operatorname{logit}(p)=\ln\frac{p}{1-p}\qquad\Longleftrightarrow\qquad p=\sigma\bigl(\operatorname{logit}(p)\bigr)"),
        ("p", "The logit and the sigmoid are inverses of each other. The logit maps a probability from $(0,1)$ onto the whole real line, where contributions of features are easy to add up. Logistic regression assumes exactly that: <b>the log-odds depend linearly on the features</b>, $\\ln\\frac{p}{1-p}=w^\\top x+b$. Hence the sigmoid at the output."),
        ("viz", "sigmoid-logit", {"p": 0.8}, "<b>Figure 4.</b> On the left the sigmoid maps the logit $z$ to a probability $p$; on the right the logit maps it back. At $p=0.8$ the odds are 4 and the logit is $\\ln4\\approx1.386$. Note how fast the logit grows near the edges — from $p=0.99$ to $p=0.999$ it changes by $2.3$."),
        ("callout", "note", "Another interpretation", "The sigmoid is the cumulative distribution function of the logistic law: if the noise $\\varepsilon$ is logistic, then $P(\\varepsilon\\le x)=\\sigma(x)$. The similar model with normal noise, $\\Phi(x)$, is called probit regression; its curve nearly coincides with $\\sigma(1.7x)$."),
    ]),
    dict(id="space", title="The sigmoid in many dimensions", blocks=[
        ("p", "A neuron has many inputs: $z=w_1x_1+w_2x_2+\\dots+b$. The sigmoid of a hyperplane is a “fold” that rises from 0 to 1 across the boundary $w^\\top x+b=0$ and stays constant along it. The weight vector $w$ points in the direction of the steepest ascent, and its length sets how steep the fold is."),
        ("viz", "sigmoid-logreg", {"w1": -0.5, "w2": 1.5, "b": 1.5}, "<b>Figure 5.</b> Logistic regression on two features. On the left, the probability surface in 3D (you can rotate it); the points sit at the height of their class. On the right, the view from above: the solid line is the boundary $p=0.5$, the dashed lines are $p=0.1$ and $p=0.9$, the arrow is the direction of $w$. Press “Play”: gradient descent on BCE with step $0.5$ finds the weights by itself."),
        ("p", "Training uses the same derivative. For the BCE loss the gradient with respect to the logit is $\\sigma(z)-y$ (derived on the <a href=\"../bce/\">BCE</a> page), so a gradient-descent step on the weights is:"),
        ("eq", r"w\leftarrow w-\eta\,\frac1n\sum_{i=1}^{n}\bigl(\sigma(w^\top x_i+b)-y_i\bigr)\,x_i"),
        ("callout", "warn", "Linearly separable data", "If a line separates the classes perfectly, BCE keeps decreasing as $\\|w\\|$ grows: the fold gets steeper and tends to a step, and the weights run off to infinity. In practice this is cured with regularization ($L_2$) or early stopping."),
    ]),
    dict(id="training", title="The sigmoid in training: saturation and vanishing gradients", blocks=[
        ("p", "If a neuron’s inputs $z$ are large in magnitude, the sigmoid works on its flat tails, where $\\sigma'(z)\\approx0$. Hardly any gradient flows through such a neuron — it is <b>saturated</b>. Saturation, $\\sigma'&lt;0.01$, starts at $|z|&gt;4.6$."),
        ("viz", "sigmoid-saturation", {"s": 1}, "<b>Figure 6.</b> The blue area is the distribution of the inputs $z\\sim N(\\mu,\\,s^2)$, the orange one is the derivative. At $s=1$ the mean derivative is $0.207$ and there are almost no saturated inputs; at $s=4$ the mean derivative drops to $0.091$, and a quarter of the inputs ($25\\%$) are already saturated."),
        ("p", "This gives the initialization rule: weights are chosen so that the variance of $z$ is of order one (Xavier–Glorot initialization, $\\operatorname{Var}w=1/n_{\\text{in}}$), and the data are normalized."),
        ("h3", "Vanishing gradients in a deep network"),
        ("p", "By the chain rule the gradient at layer $l$ is a product of the derivatives of all layers above it. For the sigmoid each derivative is at most $\\tfrac14$, so after 10 layers the factor is at most $0.25^{10}\\approx9.5\\cdot10^{-7}$."),
        ("eq", r"\frac{\partial L}{\partial h_l}=\frac{\partial L}{\partial h_L}\prod_{k=l+1}^{L}W_k^{\top}\operatorname{diag}\bigl(\sigma'(z_k)\bigr)"),
        ("viz", "sigmoid-vanishing", {"depth": 10}, "<b>Figure 7.</b> The gradient norm at every layer of a random network of width 64 (Xavier initialization for sigmoid and tanh, He for ReLU). The vertical scale is logarithmic. With the sigmoid the gradient at the input is several orders of magnitude smaller than at the output; with tanh and ReLU it barely fades."),
        ("callout", "history", "Why the sigmoid left the hidden layers", "Before 2010 deep networks with sigmoids trained poorly. Glorot and Bengio (2010) showed the role of saturation and proposed an initialization, and ReLU (Nair and Hinton, 2010; Glorot et al., 2011) all but removed the problem. Today the sigmoid lives where a share between 0 and 1 is exactly what is needed: at the output of a binary classifier and in gates."),
    ]),
    dict(id="code", title="In code: stable and without surprises", blocks=[
        ("p", "The naive formula $1/(1+e^{-x})$ at $x=-1000$ computes $e^{1000}$ — an overflow. The result still comes out as 0, but with a warning, and $\\log\\sigma(x)$ already yields $-\\infty$. The second problem is loss of precision: $1-\\sigma(40)$ in float64 is exactly 0, while the true value $\\sigma(-40)\\approx4.25\\cdot10^{-18}$."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "The rule", "If a logarithm follows, do not compute $\\sigma$ separately. Use $\\log\\sigma(x)=-\\operatorname{softplus}(-x)$ or ready-made losses on logits: <code>BCEWithLogitsLoss</code> in PyTorch, <code>from_logits=True</code> in Keras."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>Sigmoids in the hidden layers of a deep network</b> — vanishing gradients and shifted (non-centred) activations. Use ReLU, GELU, SiLU; keep the sigmoid for the output or for gates.",
            "<b>Sigmoid instead of softmax on one output.</b> For $K&gt;2$ mutually exclusive classes you need <a href=\"../softmax/\">softmax</a>; a sigmoid on every output means multi-label, where the classes are independent.",
            "<b>A double sigmoid</b>: the model already returns a probability and the loss applies σ again (for example, <code>BCEWithLogitsLoss</code> on top of <code>sigmoid</code>). Training runs, but the gradients are distorted.",
            "<b>The “default” 0.5 threshold.</b> It is optimal only for equal error costs and balanced classes. Tune the threshold for your metric on validation data.",
            "<b>Reading “σ(z) = 0.9 means the model is 90% sure”</b> without calibration. The sigmoid gives a number in $(0,1)$, but calibration is a property of training (BCE encourages it, overfitting spoils it).",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../tanh/\">tanh</a>: $\\tanh x=2\\sigma(2x)-1$ — a centred sigmoid with maximum slope 1.",
            "<a href=\"../softmax/\">Softmax</a>: for two classes $\\operatorname{softmax}(z_1,z_2)_1=\\sigma(z_1-z_2)$.",
            "<a href=\"../bce/\">BCE</a>: paired with the sigmoid it gives the gradient $\\hat y-y$ — without the factor $\\sigma'$, so no saturation while the model is wrong.",
            "<a href=\"../silu/\">SiLU / Swish</a>: $x\\,\\sigma(x)$ — the sigmoid as a “soft gate” for the input itself.",
            "<a href=\"../focal/\">Focal Loss</a>: usually computed from $p_t=\\sigma(z)$ for the correct class.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $\\sigma(x)=1/(1+e^{-x})$ maps $\\mathbb R$ to $(0,1)$, passes through $(0,\\,0.5)$ and is symmetric: $\\sigma(-x)=1-\\sigma(x)$. 2) $\\sigma'=\\sigma(1-\\sigma)\\le\\tfrac14$: backprop is cheap, but the gradient dies on the tails. 3) The sigmoid is the inverse of the logit: logistic regression models the log-odds with a linear function. 4) In many dimensions it is a fold along the hyperplane $w^\\top x+b=0$. 5) In code — stable forms and losses on logits."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="What is $\\sigma(-3)$ if $\\sigma(3)\\approx0.953$?", options=["$-0.953$", "$0.047$", "$0.953$", "$1/0.953$"], answer=1,
                 explain="By symmetry $\\sigma(-x)=1-\\sigma(x)=1-0.953=0.047$."),
            dict(q="What is the largest value of the sigmoid’s derivative?", options=["$1$", "$0.5$", "$0.25$", "It is unbounded"], answer=2,
                 explain="$\\sigma'=s(1-s)$ for $s\\in(0,1)$ is largest at $s=\\tfrac12$: $\\tfrac14$."),
            dict(q="A neuron computes $\\sigma(wx+b)$ with $w=2$, $b=-4$. Where is the output $0.5$?", options=["$x=-2$", "$x=0$", "$x=2$", "$x=4$"], answer=2,
                 explain="The centre is $x_0=-b/w=4/2=2$."),
            dict(q="Why does PyTorch recommend BCEWithLogitsLoss over sigmoid + BCELoss for binary classification?", options=["It trains faster", "It computes $\\log\\sigma(z)$ stably, without overflow and log(0)", "It needs no labels", "It adds regularization"], answer=1,
                 explain="It merges the sigmoid and the logarithm into one stable formula via softplus."),
            dict(q="What is the best-case gradient factor through a chain of 5 sigmoids?", options=["$0.25^5\\approx0.001$", "$0.5^5\\approx0.03$", "$1$", "$5\\cdot0.25$"], answer=0,
                 explain="Each derivative is at most $\\tfrac14$, so the product is at most $0.25^5\\approx9.8\\cdot10^{-4}$."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "Neyron tarmoq, logistik regressiya, gradiyentli busting — barchasining ichida oddiy son hosil bo‘ladi: $3{,}7$, $-12$, $0{,}2$. Lekin savol ko‘pincha boshqacha: xat spam ekanligi, mijoz kreditni qaytarishi, kadrda odam borligi <i>qanday ehtimollik bilan</i>? Ehtimollik 0 va 1 orasida bo‘lishi shart. Sigmoida — «istalgan son»dan «ehtimollik»ka eng tabiiy ko‘prik."),
        ("p", "U qayerda uchraydi:"),
        ("ul", [
            "<b>binar klassifikator chiqishi</b> — logistik regressiya, tarmoqning oxirgi neyroni, $p=\\sigma(z)$;",
            "<b>LSTM va GRU’dagi ventillar (gates)</b> — 0 dan 1 gacha son axborotning qancha qismini o‘tkazish, qanchasini unutishni hal qiladi;",
            "<b>klassifikatsiya uchun gradiyentli busting</b> — XGBoost, LightGBM va CatBoost daraxtlarni «xom» hisobga qo‘shadi, sigmoida esa uni ehtimollikka aylantiradi;",
            "<b>zamonaviy aktivatsiyalar</b> — LLaMA va Qwen’dagi SiLU (Swish) — bu $x\\cdot\\sigma(x)$;",
            "<b>statistika</b> — logistik taqsimot funksiyasi va ehtimollikning imkoniyatlar logarifmi (logit) bilan bog‘lanishi.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "$\\sigma$ butun son o‘qini $(0;\\,1)$ oralig‘iga siqadi, $(0;\\,0{,}5)$ nuqtadan o‘tadi va simmetrik: $\\sigma(-x)=1-\\sigma(x)$. Uning hosilasi $\\sigma'=\\sigma(1-\\sigma)$ $0{,}25$ dan oshmaydi — qulaylik (arzon backprop) ham, muammo (gradiyent so‘nishi) ham shundan."),
    ]),
    dict(id="intuition", title="Intuitsiya: cheksizlikni siqish", blocks=[
        ("p", "$y=0$ dagi pol va $y=1$ dagi shift orasidagi yo‘lni tasavvur qiling. Chapda yo‘l deyarli polda yotadi, o‘ngda deyarli shiftga tegadi, o‘rtada esa silliq ko‘tariladi. Chapga yoki o‘ngga qancha yursangiz ham, pol va shiftga yetib bo‘lmaydi — ular <b>asimptotalar</b>."),
        ("p", "Grafikdagi nuqtani torting. To‘q sariq chiziq — urinma: uning qiyaligi $\\sigma'(x)$ hosilaning o‘zi. Markazda ko‘tarilish eng tik, chekkalarda yo‘l deyarli gorizontal — u yerda hosila nolga yaqin."),
        ("viz", "sigmoid-explorer", {"x": 1.5}, "<b>1-rasm.</b> Sigmoida, uning urinmasi va hosilasi. Ko‘k nuqtani torting yoki u fokusda bo‘lganda strelkalarni bosing. Hosilaning maksimumi $0{,}25$ — aynan $x=0$ markaz ostida."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "$x=4$ da sigmoida allaqachon $0{,}982$, hosila esa atigi $0{,}018$ — markazdagidan 14 marta kichik. Bu to‘yinish (saturation): kirish o‘sishda davom etadi, chiqish esa deyarli o‘zgarmaydi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", "Sigmoidani uchta oddiy amaldan yig‘amiz va har biri $x$ son bilan nima qilishini kuzatamiz."),
        ("eq", r"x\;\xrightarrow{\;\cdot(-1)\;}\;-x\;\xrightarrow{\;\exp\;}\;e^{-x}\in(0;\,\infty)\;\xrightarrow{\;+1\;}\;1+e^{-x}\in(1;\,\infty)\;\xrightarrow{\;1/\cdot\;}\;\sigma(x)\in(0;\,1)"),
        ("symbols", [
            (r"e^{-x}", "eksponenta doim musbat: $x\\to+\\infty$ da u 0 ga, $x\\to-\\infty$ da cheksizlikka intiladi;"),
            (r"1+e^{-x}", "maxraj doim 1 dan katta — shuning uchun kasr doim 1 dan kichik;"),
            (r"\frac{1}{1+e^{-x}}", "1 dan katta musbat sonning teskarisi qat’iy 0 va 1 orasida yotadi."),
        ]),
        ("p", "Shu funksiyani boshqa yozuvlarda ham tanib olish foydali:"),
        ("eq", r"\sigma(x)=\frac{1}{1+e^{-x}}=\frac{e^{x}}{1+e^{x}}=\frac{1}{2}\Bigl(1+\tanh\frac{x}{2}\Bigr)"),
        ("p", "Ikkinchi shakl surat va maxrajni $e^x$ ga ko‘paytirishdan olinadi; u manfiy $x$ uchun qulay (kod bo‘limiga qarang). Uchinchisi sigmoidani giperbolik tangens bilan bog‘laydi: tanh — balandligi ikki marta cho‘zilgan va pastga surilgan o‘sha S-egri chiziq."),
        ("table", ["$x$", "$\\sigma(x)$", "$\\sigma'(x)$"], "TABLE", {"num": [0, 1, 2]}),
        ("p", "Jadval ikki simmetriyani ko‘rsatadi: $\\pm x$ dagi sigmoida qiymatlari bir-birini birgacha to‘ldiradi, hosila esa juft funksiya."),
    ]),
    dict(id="properties", title="Xossalar va shakl", blocks=[
        ("ul", [
            "<b>Aniqlanish sohasi</b> — barcha haqiqiy sonlar; <b>qiymatlar sohasi</b> — ochiq $(0;\\,1)$ oraliq.",
            "<b>Monotonlik</b>: qat’iy o‘suvchi, chunki istalgan $x$ da $\\sigma'(x)&gt;0$.",
            "<b>Asimptotalar</b>: $\\lim_{x\\to-\\infty}\\sigma(x)=0$ va $\\lim_{x\\to+\\infty}\\sigma(x)=1$.",
            "$(0;\\,0{,}5)$ nuqtaga nisbatan <b>markaziy simmetriya</b>: $\\sigma(-x)=1-\\sigma(x)$.",
            "<b>Burilish nuqtasi</b> — yagona, $x=0$: chapda funksiya pastga qavariq, o‘ngda — yuqoriga.",
            "<b>Lipshits sharti</b>: $|\\sigma(a)-\\sigma(b)|\\le\\tfrac14|a-b|$ — chiqish kirish o‘zgarishining choragidan tez o‘zgarmaydi.",
        ]),
        ("deep", "Nega σ(−x) = 1 − σ(x)", [
            ("eq", r"1-\sigma(x)=1-\frac{1}{1+e^{-x}}=\frac{e^{-x}}{1+e^{-x}}=\frac{1}{e^{x}+1}=\sigma(-x)"),
            ("p", "Oxiridan oldingi qadamda surat va maxraj $e^{x}$ ga ko‘paytirilgan."),
        ]),
        ("h3", "Vazn va siljish: neyron sigmoidani qanday o‘zgartiradi"),
        ("p", "Neyronda sigmoida $x$ ni emas, $z=wx+b$ ni oladi. $w$ vazn egri chiziqni gorizontal cho‘zadi, $b$ siljish uni suradi. Chiqish $0{,}5$ ga teng bo‘lgan markaz $x_0=-b/w$ nuqtaga tushadi, markazdagi qiyalik esa $w/4$ ga teng."),
        ("viz", "sigmoid-shape", {"w": 2, "b": -2}, "<b>2-rasm.</b> $\\sigma(wx+b)$. Katta $|w|$ da egri chiziq deyarli zinaga aylanadi, $w&lt;0$ da — ag‘dariladi. Xira chiziqlar — $w/4$ va $w/2$ vaznli o‘sha funksiya."),
        ("callout", "note", "Zina — limit sifatida", "$w\\to+\\infty$ da $\\sigma(w x)$ Xevisayd zinasiga intiladi: noldan chapda 0, o‘ngda 1. Sigmoida neyron tarmoqlarga tarixan aynan shunday kirgan — Makkallok — Pitts chegaraviy neyronining silliq, differensiallanuvchi o‘rinbosari sifatida."),
    ]),
    dict(id="derivative", title="Hosila: σ′ = σ(1 − σ)", blocks=[
        ("p", "Bu sahifaning asosiy formulasi. Uni ikki usulda keltirib chiqaramiz — to‘g‘ridan-to‘g‘ri va nafis usulda."),
        ("deep", "1-usul. Bo‘linma hosilasi (qadamma-qadam)", [
            ("p", "$\\sigma(x)=(1+e^{-x})^{-1}$ deb yozamiz va murakkab funksiya hosilasi qoidasini qo‘llaymiz:"),
            ("eq", r"\sigma'(x)=-(1+e^{-x})^{-2}\cdot\bigl(1+e^{-x}\bigr)'=-(1+e^{-x})^{-2}\cdot(-e^{-x})=\frac{e^{-x}}{(1+e^{-x})^{2}}"),
            ("p", "Kasrni ikki ko‘paytuvchiga ajratamiz:"),
            ("eq", r"\frac{e^{-x}}{(1+e^{-x})^{2}}=\underbrace{\frac{1}{1+e^{-x}}}_{\sigma(x)}\cdot\underbrace{\frac{e^{-x}}{1+e^{-x}}}_{1-\sigma(x)}"),
            ("p", "Ikkinchi ko‘paytuvchi — $1-\\sigma(x)$, buni xossalar bo‘limida isbotladik."),
        ]),
        ("deep", "2-usul. Logarifm orqali", [
            ("p", "Logarifm olamiz: $\\ln\\sigma(x)=-\\ln(1+e^{-x})$. Ikkala tomonni differensiallaymiz:"),
            ("eq", r"\frac{\sigma'(x)}{\sigma(x)}=\frac{e^{-x}}{1+e^{-x}}=1-\sigma(x)\quad\Longrightarrow\quad\sigma'(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)"),
        ]),
        ("eq", r"\sigma'(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)"),
        ("p", "Amalda nega muhim: to‘g‘ri o‘tishda tarmoq $s=\\sigma(z)$ ni allaqachon hisoblagan. Teskari o‘tishda hosila bitta ko‘paytirish $s(1-s)$ ga tushadi — yangi eksponentasiz."),
        ("h3", "Hosila maksimumi va ikkinchi hosila"),
        ("p", "$s\\in(0;1)$ da $s(1-s)$ ko‘paytma — uchi $s=\\tfrac12$ da bo‘lgan ag‘darilgan parabola. Demak, $\\max\\sigma'=\\tfrac12\\cdot\\tfrac12=\\tfrac14$, u $x=0$ da erishiladi. Yana bir marta differensiallaymiz:"),
        ("eq", r"\sigma''(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)\bigl(1-2\sigma(x)\bigr)"),
        ("p", "Ikkinchi hosila $\\sigma=\\tfrac12$ da, ya’ni $x=0$ burilish nuqtasida nolga aylanadi. Uning ekstremumlari $x=\\pm\\ln(2+\\sqrt3)\\approx\\pm1{,}317$ nuqtalarda, u yerda sigmoida qiyaligi eng tez o‘zgaradi; qiymati $\\mp\\sqrt3/18\\approx\\mp0{,}096$."),
        ("h3", "Nol atrofidagi Teylor qatori"),
        ("p", "tanh bilan bog‘lanishdan yoyilmani olamiz:"),
        ("eq", r"\sigma(x)=\frac12+\frac{x}{4}-\frac{x^{3}}{48}+\frac{x^{5}}{480}-\frac{17x^{7}}{80640}+\dots"),
        ("p", "Nol atrofida sigmoida deyarli chiziqli: $\\sigma(x)\\approx\\tfrac12+\\tfrac{x}{4}$. Shuning uchun kichik vaznlarda sigmoidali tarmoq deyarli chiziqli model kabi ishlaydi. Qator faqat $|x|&lt;\\pi$ da yaqinlashadi: funksiyaning kompleks tekislikda $x=\\pm i\\pi$ maxsus nuqtalari bor."),
        ("viz", "sigmoid-taylor", {}, "<b>3-rasm.</b> 1, 3, 5, 7-tartibli Teylor ko‘phadlari. $|x|&lt;\\pi$ yo‘lak ichida aniqlik tartib bilan oshadi, undan tashqarida esa tartib qancha yuqori bo‘lsa, ko‘phad sigmoidadan shuncha tez uzoqlashadi. $x=2$ da uchinchi tartibli yaqinlashish $0{,}881$ o‘rniga $0{,}833$ beradi."),
    ]),
    dict(id="probability", title="Ehtimollik ma’nosi: imkoniyatlar va logit", blocks=[
        ("p", "Nega sigmoida chiqishini ehtimollik deb o‘qish o‘rinli? $p$ — hodisa ehtimolligi bo‘lsin. $p/(1-p)$ nisbat <b>imkoniyatlar</b> (odds) deyiladi: $p=0{,}8$ da imkoniyatlar $4:1$. Imkoniyatlar logarifmi — <b>logit</b>:"),
        ("eq", r"\operatorname{logit}(p)=\ln\frac{p}{1-p}\qquad\Longleftrightarrow\qquad p=\sigma\bigl(\operatorname{logit}(p)\bigr)"),
        ("p", "Logit va sigmoida — o‘zaro teskari funksiyalar. Logit ehtimollikni $(0;1)$ dan butun son o‘qiga o‘tkazadi, u yerda belgilar hissalarini qo‘shish qulay. Logistik regressiya aynan shuni faraz qiladi: <b>imkoniyatlar logarifmi belgilarga chiziqli bog‘liq</b>, $\\ln\\frac{p}{1-p}=w^\\top x+b$. Chiqishdagi sigmoida shundan."),
        ("viz", "sigmoid-logit", {"p": 0.8}, "<b>4-rasm.</b> Chapda sigmoida $z$ logitni $p$ ehtimollikka o‘tkazadi, o‘ngda logit uni qaytaradi. $p=0{,}8$ da imkoniyatlar 4 ga, logit $\\ln4\\approx1{,}386$ ga teng. E’tibor bering: chekkalarda logit tez o‘sadi — $p=0{,}99$ dan $p=0{,}999$ gacha u $2{,}3$ ga o‘zgaradi."),
        ("callout", "note", "Yana bir talqin", "Sigmoida — logistik taqsimot funksiyasi: agar $\\varepsilon$ shovqin logistik taqsimotga ega bo‘lsa, $P(\\varepsilon\\le x)=\\sigma(x)$. Normal shovqinli o‘xshash model, $\\Phi(x)$, probit-regressiya deyiladi; uning egri chizig‘i $\\sigma(1{,}7x)$ bilan deyarli ustma-ust tushadi."),
    ]),
    dict(id="space", title="Ko‘p o‘lchovli fazodagi sigmoida", blocks=[
        ("p", "Neyronning kirishlari ko‘p: $z=w_1x_1+w_2x_2+\\dots+b$. Giperteksislikdan olingan sigmoida — $w^\\top x+b=0$ chegara bo‘ylab ko‘ndalang 0 dan 1 gacha ko‘tariladigan va chegara bo‘ylab o‘zgarmaydigan «burma». $w$ vaznlar vektori eng tik ko‘tarilish yo‘nalishini ko‘rsatadi, uning uzunligi esa burmaning tikligini belgilaydi."),
        ("viz", "sigmoid-logreg", {"w1": -0.5, "w2": 1.5, "b": 1.5}, "<b>5-rasm.</b> Ikki belgili logistik regressiya. Chapda — 3D’dagi ehtimollik sirti (uni aylantirish mumkin), nuqtalar o‘z sinfi balandligida turibdi. O‘ngda — yuqoridan ko‘rinish: yaxlit chiziq — $p=0{,}5$ chegara, punktir — $p=0{,}1$ va $p=0{,}9$, strelka — $w$ yo‘nalishi. «Boshlash»ni bosing: $0{,}5$ qadamli BCE bo‘yicha gradiyent tushish vaznlarni o‘zi topadi."),
        ("p", "O‘qitish o‘sha hosiladan foydalanadi. BCE yo‘qotishi uchun logit bo‘yicha gradiyent $\\sigma(z)-y$ ga teng (keltirib chiqarilishi — <a href=\"../bce/\">BCE</a> sahifasida), shuning uchun vaznlar bo‘yicha gradiyent tushish qadami:"),
        ("eq", r"w\leftarrow w-\eta\,\frac1n\sum_{i=1}^{n}\bigl(\sigma(w^\top x_i+b)-y_i\bigr)\,x_i"),
        ("callout", "warn", "Chiziqli ajraladigan ma’lumotlar", "Agar sinflarni to‘g‘ri chiziq bilan mukammal ajratish mumkin bo‘lsa, $\\|w\\|$ o‘sishi bilan BCE kamayishda davom etadi: burma tobora tiklashadi va zinaga intiladi, vaznlar cheksizlikka ketadi. Amalda bu regulyarizatsiya ($L_2$) yoki erta to‘xtatish bilan davolanadi."),
    ]),
    dict(id="training", title="O‘qitishdagi sigmoida: to‘yinish va gradiyent so‘nishi", blocks=[
        ("p", "Agar neyronning $z$ kirishlari modul bo‘yicha katta bo‘lsa, sigmoida $\\sigma'(z)\\approx0$ bo‘lgan yassi chekkalarda ishlaydi. Bunday neyron orqali gradiyent deyarli o‘tmaydi — neyron <b>to‘yingan</b>. $\\sigma'&lt;0{,}01$ to‘yinish $|z|&gt;4{,}6$ da boshlanadi."),
        ("viz", "sigmoid-saturation", {"s": 1}, "<b>6-rasm.</b> Ko‘k soha — $z\\sim N(\\mu,\\,s^2)$ kirishlar taqsimoti, to‘q sariq — hosila. $s=1$ da o‘rtacha hosila $0{,}207$ va to‘yingan kirishlar deyarli yo‘q; $s=4$ da o‘rtacha hosila $0{,}091$ gacha tushadi, kirishlarning choragi ($25\\%$) esa to‘yingan."),
        ("p", "Initsializatsiya qoidasi shundan kelib chiqadi: vaznlar $z$ dispersiyasi birga yaqin bo‘ladigan qilib tanlanadi (Ksavye — Gloro initsializatsiyasi, $\\operatorname{Var}w=1/n_{\\text{in}}$), ma’lumotlar esa normallashtiriladi."),
        ("h3", "Chuqur tarmoqda gradiyent so‘nishi"),
        ("p", "Zanjir qoidasiga ko‘ra $l$ qatlamdagi gradiyent — yuqoridagi barcha qatlamlar hosilalarining ko‘paytmasi. Sigmoidada har bir hosila $\\tfrac14$ dan oshmaydi, shuning uchun 10 qatlamdan keyin ko‘paytuvchi $0{,}25^{10}\\approx9{,}5\\cdot10^{-7}$ dan oshmaydi."),
        ("eq", r"\frac{\partial L}{\partial h_l}=\frac{\partial L}{\partial h_L}\prod_{k=l+1}^{L}W_k^{\top}\operatorname{diag}\bigl(\sigma'(z_k)\bigr)"),
        ("viz", "sigmoid-vanishing", {"depth": 10}, "<b>7-rasm.</b> Kengligi 64 bo‘lgan tasodifiy tarmoqning har bir qatlamidagi gradiyent normasi (sigmoid va tanh uchun Ksavye, ReLU uchun Xe initsializatsiyasi). Vertikal shkala logarifmik. Sigmoidada kirishdagi gradiyent chiqishdagidan bir necha tartibga kichik; tanh va ReLU’da u deyarli so‘nmaydi."),
        ("callout", "history", "Nega sigmoida yashirin qatlamlardan ketdi", "2010-yilgacha sigmoidali chuqur tarmoqlar yomon o‘qitilardi. Gloro va Benjio (2010) to‘yinish rolini ko‘rsatib, initsializatsiya taklif qildi, ReLU (Nair va Xinton, 2010; Gloro va boshq., 2011) esa muammoni deyarli bartaraf etdi. Bugun sigmoida aynan 0 dan 1 gacha ulush kerak bo‘lgan joyda yashaydi: binar klassifikator chiqishida va ventillarda."),
    ]),
    dict(id="code", title="Kodda: barqaror va kutilmagan holatlarsiz", blocks=[
        ("p", "Sodda $1/(1+e^{-x})$ formula $x=-1000$ da $e^{1000}$ ni hisoblaydi — to‘lib ketish. Natija baribir 0 chiqadi, lekin ogohlantirish bilan, $\\log\\sigma(x)$ da esa $-\\infty$ paydo bo‘ladi. Ikkinchi muammo — aniqlik yo‘qolishi: float64 da $1-\\sigma(40)$ aynan 0 ga teng, haqiqiy qiymat esa $\\sigma(-40)\\approx4{,}25\\cdot10^{-18}$."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Qoida", "Agar keyin logarifm kelsa, $\\sigma$ ni alohida hisoblamang. $\\log\\sigma(x)=-\\operatorname{softplus}(-x)$ yoki logitlardagi tayyor yo‘qotishlardan foydalaning: PyTorch’da <code>BCEWithLogitsLoss</code>, Keras’da <code>from_logits=True</code>."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b>Chuqur tarmoqning yashirin qatlamlarida sigmoida</b> — gradiyent so‘nishi va siljigan (markazlashmagan) aktivatsiyalar. ReLU, GELU, SiLU oling; sigmoidani faqat chiqishda yoki ventillarda qoldiring.",
            "<b>Bitta chiqishda softmax o‘rniga sigmoida.</b> $K&gt;2$ ta o‘zaro istisno sinf uchun <a href=\"../softmax/\">softmax</a> kerak; har bir chiqishdagi sigmoida — sinflar mustaqil bo‘lgan multi-label.",
            "<b>Ikki karra sigmoida</b>: model allaqachon ehtimollik qaytaradi, yo‘qotish esa σ ni yana qo‘llaydi (masalan, <code>sigmoid</code> ustidan <code>BCEWithLogitsLoss</code>). O‘qitish ketadi, lekin gradiyentlar buziladi.",
            "<b>«Standart» 0,5 chegara.</b> U faqat xato narxlari teng va sinflar muvozanatli bo‘lganda optimal. Chegara validatsiyada metrika bo‘yicha tanlanadi.",
            "<b>Kalibrlashsiz «σ(z) = 0,9, demak model 90% ishonchli» xulosasi.</b> Sigmoida $(0;1)$ dagi son beradi, kalibrlanganlik esa o‘qitish xossasi (BCE unga yordam beradi, qayta o‘qitish buzadi).",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘lanishlar", blocks=[
        ("ul", [
            "<a href=\"../tanh/\">tanh</a>: $\\tanh x=2\\sigma(2x)-1$ — maksimal qiyaligi 1 bo‘lgan markazlashgan sigmoida.",
            "<a href=\"../softmax/\">Softmax</a>: ikki sinf uchun $\\operatorname{softmax}(z_1,z_2)_1=\\sigma(z_1-z_2)$.",
            "<a href=\"../bce/\">BCE</a>: sigmoida bilan juftlikda $\\hat y-y$ gradiyent beradi — $\\sigma'$ ko‘paytuvchisiz, demak model xato qilganda to‘yinishsiz.",
            "<a href=\"../silu/\">SiLU / Swish</a>: $x\\,\\sigma(x)$ — kirishning o‘zi uchun «yumshoq ventil» sifatidagi sigmoida.",
            "<a href=\"../focal/\">Focal Loss</a>: odatda to‘g‘ri sinf uchun $p_t=\\sigma(z)$ dan hisoblanadi.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $\\sigma(x)=1/(1+e^{-x})$ $\\mathbb R$ ni $(0;1)$ ga o‘tkazadi, $(0;\\,0{,}5)$ dan o‘tadi va simmetrik: $\\sigma(-x)=1-\\sigma(x)$. 2) $\\sigma'=\\sigma(1-\\sigma)\\le\\tfrac14$: backprop arzon, lekin chekkalarda gradiyent so‘nadi. 3) Sigmoida logitga teskari: logistik regressiya imkoniyatlar logarifmini chiziqli funksiya bilan modellashtiradi. 4) Ko‘p o‘lchovli holatda bu $w^\\top x+b=0$ giperteksislik bo‘ylab burma. 5) Kodda — barqaror shakllar va logitlardagi yo‘qotishlar."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="Agar $\\sigma(3)\\approx0{,}953$ bo‘lsa, $\\sigma(-3)$ nimaga teng?", options=["$-0{,}953$", "$0{,}047$", "$0{,}953$", "$1/0{,}953$"], answer=1,
                 explain="Simmetriya bo‘yicha $\\sigma(-x)=1-\\sigma(x)=1-0{,}953=0{,}047$."),
            dict(q="Sigmoida hosilasi eng katta qanday qiymat qabul qiladi?", options=["$1$", "$0{,}5$", "$0{,}25$", "Chegaralanmagan"], answer=2,
                 explain="$s\\in(0;1)$ da $\\sigma'=s(1-s)$ $s=\\tfrac12$ da maksimal: $\\tfrac14$."),
            dict(q="Neyron $w=2$, $b=-4$ bilan $\\sigma(wx+b)$ ni hisoblaydi. Chiqish qayerda $0{,}5$ ga teng?", options=["$x=-2$", "$x=0$", "$x=2$", "$x=4$"], answer=2,
                 explain="Markaz $x_0=-b/w=4/2=2$."),
            dict(q="Nega PyTorch’da binar klassifikatsiya uchun sigmoid + BCELoss o‘rniga BCEWithLogitsLoss tavsiya qilinadi?", options=["U tezroq o‘qitadi", "U $\\log\\sigma(z)$ ni to‘lib ketishsiz va log(0) siz barqaror hisoblaydi", "Unga belgilar kerak emas", "U regulyarizatsiya qo‘shadi"], answer=1,
                 explain="U sigmoida va logarifmni softplus orqali bitta barqaror formulaga birlashtiradi."),
            dict(q="5 ta sigmoida zanjiri eng yaxshi holatda gradiyentni qanday ko‘paytuvchiga kamaytiradi?", options=["$0{,}25^5\\approx0{,}001$", "$0{,}5^5\\approx0{,}03$", "$1$", "$5\\cdot0{,}25$"], answer=0,
                 explain="Har bir hosila $\\tfrac14$ dan oshmaydi, shuning uchun ko‘paytma $0{,}25^5\\approx9{,}8\\cdot10^{-4}$ dan oshmaydi."),
        ]),
    ]),
],
}

# Fill in the shared pieces (table rows and code listings) per language.
for _lang, _secs in SECTIONS.items():
    for _sec in _secs:
        for _i, _b in enumerate(_sec["blocks"]):
            if _b[0] == "table" and _b[2] == "TABLE":
                _sec["blocks"][_i] = (_b[0], _b[1], _table(_lang), _b[3])
            elif _b[0] == "code" and _b[2] in ("CODE_NUMPY", "CODE_TORCH"):
                _sec["blocks"][_i] = (_b[0], _b[1], _code(CODE_NUMPY if _b[2] == "CODE_NUMPY" else CODE_TORCH, _lang))
