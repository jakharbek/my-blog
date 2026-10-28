"""Formula page: GELU, the Gaussian error linear unit. Format: see README.md."""

META = dict(
    id="gelu",
    date="2026-10-28",
    minutes=35,
    hero=r"\operatorname{GELU}(x)=x\cdot\Phi(x)=\frac{x}{2}\Bigl(1+\operatorname{erf}\frac{x}{\sqrt2}\Bigr)",
    title={"ru": "GELU: вход, умноженный на вероятность", "en": "GELU: the input times a probability", "uz": "GELU: ehtimollikka ko‘paytirilgan kirish"},
    dek={
        "ru": "Активация BERT, GPT и ViT. Разбираем по косточкам, почему это не просто «сглаженная ReLU»: откуда берётся нормальная функция распределения Φ, как GELU получается усреднением случайной маски, где у неё минимум, чему равна производная Φ(x) + xφ(x) и насколько точны приближения через tanh и сигмоиду.",
        "en": "The activation of BERT, GPT and ViT. We take it apart bone by bone to see why it is more than a “smoothed ReLU”: where the normal distribution function Φ comes from, how GELU arises as the average of a random mask, where its minimum lies, what its derivative Φ(x) + xφ(x) looks like and how accurate the tanh and sigmoid approximations are.",
        "uz": "BERT, GPT va ViT aktivatsiyasi. Nega bu shunchaki «silliqlangan ReLU» emasligini mayda detallarigacha ko‘rib chiqamiz: normal taqsimot funksiyasi Φ qayerdan keladi, GELU tasodifiy niqobni o‘rtachalashdan qanday hosil bo‘ladi, uning minimumi qayerda, Φ(x) + xφ(x) hosila qanday ko‘rinadi va tanh hamda sigmoida orqali yaqinlashishlar qanchalik aniq.",
    },
    description={
        "ru": "GELU подробно: формула x·Φ(x), стохастический смысл, минимум, производная и вторая производная, tanh-приближение, семейство x·Φ(x/s) в 3D, обучение сети, код NumPy и PyTorch.",
        "en": "GELU in depth: the formula x·Φ(x), its stochastic meaning, the minimum, the first and second derivatives, the tanh approximation, the x·Φ(x/s) family in 3D, network training, NumPy and PyTorch code.",
        "uz": "GELU batafsil: x·Φ(x) formulasi, stoxastik ma’nosi, minimum, birinchi va ikkinchi hosilalar, tanh yaqinlashishi, 3D’da x·Φ(x/s) oilasi, tarmoqni o‘qitish, NumPy va PyTorch kodi.",
    },
)

TABLE = [("-3", "0.0013", "-0.0040", "-0.0119", "0"), ("-2", "0.0228", "-0.0455", "-0.0852", "0"), ("-1", "0.1587", "-0.1587", "-0.0833", "0"),
         ("-0.5", "0.3085", "-0.1543", "0.1325", "0"), ("0", "0.5000", "0.0000", "0.5000", "0"), ("0.5", "0.6915", "0.3457", "0.8675", "0.5"),
         ("1", "0.8413", "0.8413", "1.0833", "1"), ("2", "0.9772", "1.9545", "1.0852", "2"), ("3", "0.9987", "2.9960", "1.0119", "3")]


def _table(lang):
    dec = "." if lang == "en" else ","
    m = lambda v: v.replace("-", "−").replace(".", dec)
    return [[m(c) for c in row] for row in TABLE]


CODE_NUMPY = '''import numpy as np
from scipy.special import erfc        # в самой NumPy функции erf нет

SQRT2 = np.sqrt(2.0)

def gelu(x):
    """Точная GELU: x·Φ(x), где Φ(x) = ½·erfc(−x/√2) — без вычитания близких чисел."""
    x = np.asarray(x, dtype=float)
    return x * 0.5 * erfc(-x / SQRT2)

def gelu_grad(x):
    """Производная: Φ(x) + x·φ(x)."""
    x = np.asarray(x, dtype=float)
    cdf = 0.5 * erfc(-x / SQRT2)
    pdf = np.exp(-0.5 * x * x) / np.sqrt(2.0 * np.pi)
    return cdf + x * pdf

def gelu_tanh(x):
    # приближение из исходного кода BERT и GPT-2
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)))

x = np.array([-3.0, -1.0, 0.0, 1.0, 3.0])
print(gelu(x))        # ≈ [-0.00405 -0.15866  0.  0.84134  2.99595]
print(gelu_grad(x))   # ≈ [-0.01195 -0.08332  0.5 1.08332  1.01195]
print(np.abs(gelu_tanh(x) - gelu(x)).max())   # ≈ 4.1e-04 (в точках x = ±3)'''

CODE_TORCH = '''import torch
import torch.nn as nn
import torch.nn.functional as F

x = torch.tensor([-1.0, 0.0, 1.0], requires_grad=True)
y = F.gelu(x)                          # −0.1587, 0.0000, 0.8413
y.sum().backward()
print(x.grad)                          # −0.0833, 0.5000, 1.0833 = Φ(x) + x·φ(x)
print(F.gelu(x, approximate="tanh"))   # −0.1588, 0.0000, 0.8412

# Блок FFN трансформера (как в BERT и GPT): d → 4d → d
class FeedForward(nn.Module):
    def __init__(self, d_model=768, mult=4, p_drop=0.1):
        super().__init__()
        self.fc1 = nn.Linear(d_model, mult * d_model)
        self.act = nn.GELU()           # для весов GPT-2: nn.GELU(approximate="tanh")
        self.fc2 = nn.Linear(mult * d_model, d_model)
        self.drop = nn.Dropout(p_drop)

    def forward(self, h):
        return self.drop(self.fc2(self.act(self.fc1(h))))'''


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("в самой NumPy функции erf нет", "NumPy itself has no erf"),
               ("Точная GELU: x·Φ(x), где Φ(x) = ½·erfc(−x/√2) — без вычитания близких чисел.", "Exact GELU: x·Φ(x) with Φ(x) = ½·erfc(−x/√2) — no subtraction of close numbers."),
               ("Производная: Φ(x) + x·φ(x).", "The derivative: Φ(x) + x·φ(x)."),
               ("приближение из исходного кода BERT и GPT-2", "the approximation from the original BERT and GPT-2 code"),
               ("(в точках x = ±3)", "(at x = ±3)"),
               ("Блок FFN трансформера (как в BERT и GPT): d → 4d → d", "A transformer FFN block (as in BERT and GPT): d → 4d → d"),
               ("для весов GPT-2: nn.GELU(approximate=\"tanh\")", "for GPT-2 weights: nn.GELU(approximate=\"tanh\")")],
        "uz": [("в самой NumPy функции erf нет", "NumPy’ning o‘zida erf funksiyasi yo‘q"),
               ("Точная GELU: x·Φ(x), где Φ(x) = ½·erfc(−x/√2) — без вычитания близких чисел.", "Aniq GELU: x·Φ(x), bunda Φ(x) = ½·erfc(−x/√2) — yaqin sonlarni ayirmasdan."),
               ("Производная: Φ(x) + x·φ(x).", "Hosila: Φ(x) + x·φ(x)."),
               ("приближение из исходного кода BERT и GPT-2", "BERT va GPT-2 ning asl kodidagi yaqinlashish"),
               ("(в точках x = ±3)", "(x = ±3 nuqtalarda)"),
               ("Блок FFN трансформера (как в BERT и GPT): d → 4d → d", "Transformerning FFN bloki (BERT va GPT’dagi kabi): d → 4d → d"),
               ("для весов GPT-2: nn.GELU(approximate=\"tanh\")", "GPT-2 vaznlari uchun: nn.GELU(approximate=\"tanh\")")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", "Функция активации — это нелинейность, которая стоит после каждого линейного слоя. Без неё сколько угодно слоёв схлопываются в одно умножение на матрицу. Долгое время стандартом была <a href=\"../relu/\">ReLU</a>: $\\max(0,x)$ — пропустить положительное, обнулить отрицательное. GELU (Gaussian Error Linear Unit, Хендрикс и Гимпел, 2016) решает ту же задачу мягче: вход не пропускается или режется, а <b>умножается на вероятность</b> того, что его стоит пропустить."),
        ("p", "Где она встречается:"),
        ("ul", [
            "<b>BERT, RoBERTa, GPT, GPT-2, GPT-3</b> — в каждом блоке прямого распространения (feed-forward, FFN) трансформера: $\\operatorname{FFN}(h)=W_2\\,\\operatorname{GELU}(W_1h+b_1)+b_2$;",
            "<b>Vision Transformer (ViT)</b> и многие модели компьютерного зрения после него;",
            "<b>GeGLU</b> — вентильный вариант $\\operatorname{GELU}(xW)\\odot(xV)$, например в Gemma; его родственник SwiGLU с <a href=\"../silu/\">SiLU</a> стоит в LLaMA и Qwen;",
            "<b>везде, где важна гладкость</b>: у GELU есть все производные, нет излома в нуле и нет «мёртвой» зоны с нулевым градиентом, как у ReLU.",
        ]),
        ("callout", "key", "Главное за минуту", "$\\operatorname{GELU}(x)=x\\,\\Phi(x)$, где $\\Phi$ — функция распределения стандартного нормального закона. Большие положительные $x$ проходят почти целиком, большие отрицательные — почти обнуляются, около нуля работает плавный переход. У функции есть минимум $\\approx-0{,}170$ в точке $x\\approx-0{,}752$, производная $\\Phi(x)+x\\varphi(x)$ лежит в пределах от $-0{,}129$ до $1{,}129$, а на практике её часто считают через tanh-приближение с ошибкой не больше $4{,}7\\cdot10^{-4}$."),
    ]),
    dict(id="intuition", title="Интуиция: вход, умноженный на вероятность", blocks=[
        ("p", "Представьте вентиль, который решает, какую долю сигнала $x$ пропустить дальше. У ReLU вентиль жёсткий: при $x&gt;0$ он открыт полностью, при $x&lt;0$ закрыт. У GELU вентиль приоткрыт на $\\Phi(x)$ — на долю от 0 до 1, которая плавно растёт вместе с $x$. Большой положительный сигнал проходит почти целиком, большой отрицательный почти гасится, а около нуля сигнал проходит наполовину: $\\Phi(0)=0{,}5$."),
        ("p", "Потяните точку. Серая полоса — вход $x$ целиком, синяя — та его часть, которая прошла: её длина равна $x\\cdot\\Phi(x)$. Пунктир бирюзового цвета — сама доля $\\Phi(x)$."),
        ("viz", "gelu-explorer", {"x": 1}, "<b>Рисунок 1.</b> GELU, доля $\\Phi(x)$ и производная. При $x=1$ пропускается доля $\\Phi(1)\\approx0{,}841$, поэтому $\\operatorname{GELU}(1)\\approx0{,}841$; при $x=-1$ пропускается только $0{,}159$, и выход равен $-0{,}159$. Кружок отмечает минимум функции."),
        ("callout", "intuition", "Что заметить", "Для отрицательных $x$ выход не равен нулю: он отрицательный и маленький. Сначала, при уменьшении $x$ от нуля, он убывает (вход растёт по модулю быстрее, чем падает доля), а примерно с $x=-0{,}75$ снова поднимается к нулю: доля $\\Phi(x)$ гаснет быстрее, чем растёт $|x|$. Отсюда неглубокая «ямка» — главное отличие формы GELU от ReLU."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", "Вся сложность GELU спрятана в $\\Phi$. Разберём её на части."),
        ("eq", r"\operatorname{GELU}(x)=x\cdot\Phi(x),\qquad \Phi(x)=\int_{-\infty}^{x}\varphi(t)\,dt,\qquad \varphi(t)=\frac{1}{\sqrt{2\pi}}\,e^{-t^{2}/2}"),
        ("symbols", [
            (r"\varphi(t)", "плотность стандартного нормального распределения $N(0,1)$ — колокол Гаусса с максимумом $1/\\sqrt{2\\pi}\\approx0{,}399$ в нуле;"),
            (r"\Phi(x)", "функция распределения: площадь под колоколом левее точки $x$, то есть вероятность $P(\\varepsilon\\le x)$ для $\\varepsilon\\sim N(0,1)$; растёт от 0 до 1, $\\Phi(0)=\\tfrac12$;"),
            (r"x\cdot\Phi(x)", "вход, умноженный на эту вероятность."),
        ]),
        ("p", "Интеграл от гауссианы не выражается через элементарные функции, поэтому для него есть специальное имя — функция ошибок (error function), отсюда «Gaussian <i>Error</i> Linear Unit»:"),
        ("eq", r"\operatorname{erf}(z)=\frac{2}{\sqrt\pi}\int_0^{z}e^{-t^2}\,dt,\qquad \Phi(x)=\frac12\Bigl(1+\operatorname{erf}\frac{x}{\sqrt2}\Bigr)\quad\Longrightarrow\quad\operatorname{GELU}(x)=\frac{x}{2}\Bigl(1+\operatorname{erf}\frac{x}{\sqrt2}\Bigr)"),
        ("p", "Множитель $1/\\sqrt2$ переводит стандартную нормальную величину с плотностью $e^{-t^2/2}$ к ядру $e^{-t^2}$, под которое определена erf. Сама erf нечётная, меняется от $-1$ до $1$, поэтому $\\tfrac12(1+\\operatorname{erf})$ меняется от 0 до 1."),
        ("table", ["$x$", "$\\Phi(x)$", "$\\operatorname{GELU}(x)$", "$\\operatorname{GELU}'(x)$", "$\\operatorname{ReLU}(x)$"], "TABLE", {"num": [0, 1, 2, 3, 4]}),
        ("p", "Таблица показывает три вещи. Справа GELU быстро догоняет ReLU: при $x=3$ разница всего $0{,}004$. Слева выход отрицательный, но маленький: самое глубокое значение в таблице — $-0{,}159$ при $x=-1$. Производная в нуле равна $0{,}5$, а при $x\\ge1$ она больше единицы — функция растёт чуть быстрее прямой $y=x$, догоняя её."),
    ]),
    dict(id="origin", title="Откуда она взялась: шумная маска в среднем", blocks=[
        ("p", "Авторы GELU объединили две идеи. <b>ReLU</b> умножает вход на детерминированную маску: $x\\cdot\\mathbb 1[x&gt;0]$. <b>Dropout</b> умножает вход на случайную маску, которая от входа не зависит. А что если маска случайна, но <i>зависит</i> от входа: чем больше $x$, тем вероятнее, что его пропустят?"),
        ("eq", r"m\sim\operatorname{Bernoulli}\bigl(\Phi(x)\bigr),\qquad \mathbb E\,[\,x\cdot m\,]=x\cdot P(m=1)=x\,\Phi(x)=\operatorname{GELU}(x)"),
        ("p", "Такую маску легко получить: возьмите шум $\\varepsilon\\sim N(0,1)$ и положите $m=1$, если $\\varepsilon\\le x$. Тогда $P(m=1)=\\Phi(x)$ по определению функции распределения. Почему нормальный закон? После нормализаций (BatchNorm, LayerNorm) входы нейронов распределены примерно как $N(0,1)$, и $\\Phi(x)$ отвечает на естественный вопрос: какая доля типичных входов меньше данного $x$."),
        ("viz", "gelu-mask", {"x": 0.5, "seed": 3}, "<b>Рисунок 2.</b> Слева оранжевые точки — среднее $x\\cdot m$ по $n$ случайным маскам в 25 точках от $-3$ до $3$, справа — шум $\\varepsilon$ и доля $\\Phi(x_0)$, при которой маска открыта. Нажмите «Пуск»: при $n=20$ наибольшее отклонение от GELU равно $0{,}146$, при $n=2000$ — уже $0{,}0125$; ошибка среднего убывает как $1/\\sqrt n$. В точке $x_0=0{,}5$ доля открытых масок приближается к $\\Phi(0{,}5)\\approx0{,}691$."),
        ("callout", "note", "GELU сама не случайна", "Шумная маска — только объяснение формы. В сети стоит детерминированное среднее $x\\Phi(x)$: случайности при обучении и выводе нет (если нужен шум, отдельно добавляют dropout)."),
    ]),
    dict(id="properties", title="Свойства и форма", blocks=[
        ("ul", [
            "<b>Область значений</b> — $[-0{,}170;\\,+\\infty)$: снизу функция ограничена, сверху нет.",
            "<b>Гладкость</b>: GELU бесконечно дифференцируема; $\\operatorname{GELU}(0)=0$, $\\operatorname{GELU}'(0)=\\tfrac12$.",
            "<b>Немонотонность</b>: функция убывает на $(-\\infty;\\,-0{,}752)$ и возрастает правее; минимум $\\approx-0{,}170$.",
            "<b>Асимптоты</b>: $\\operatorname{GELU}(x)-x\\to0$ при $x\\to+\\infty$ и $\\operatorname{GELU}(x)\\to0$ при $x\\to-\\infty$, причём слева хвост гаснет как гауссиана: $x\\Phi(x)\\approx-\\varphi(x)$, уже $\\operatorname{GELU}(-4)\\approx-1{,}3\\cdot10^{-4}$.",
            "<b>Тождество</b>: $\\operatorname{GELU}(x)-\\operatorname{GELU}(-x)=x$, потому что $\\Phi(x)+\\Phi(-x)=1$.",
            "<b>Выпуклость</b>: только на отрезке $[-\\sqrt2;\\,\\sqrt2]$; за его пределами функция вогнута (знак второй производной — в следующем разделе).",
        ]),
        ("h3", "GELU = ReLU минус чётная «ямка»"),
        ("p", "Из тождества следует удобная запись. Для $x&gt;0$: $x\\Phi(x)=x-x\\Phi(-x)$; для $x&lt;0$: $x\\Phi(x)=-|x|\\Phi(-|x|)$. В обоих случаях"),
        ("eq", r"\operatorname{GELU}(x)=\operatorname{ReLU}(x)-|x|\,\Phi(-|x|)"),
        ("p", "Поправка $|x|\\Phi(-|x|)$ чётная: она одинакова слева и справа от нуля, достигает максимума $0{,}170$ при $|x|=0{,}752$ и быстро гаснет. Тем же свойством обладает <a href=\"../silu/\">SiLU</a> $x\\,\\sigma(x)$, только её «ямка» шире и глубже: $0{,}278$ при $|x|=1{,}278$."),
        ("viz", "gelu-family", {"x": -1}, "<b>Рисунок 3.</b> Сверху — GELU, SiLU и ReLU, снизу — разности $\\operatorname{ReLU}-f$. Наведите курсор на любой из графиков. При $x=-1$: $\\operatorname{GELU}=-0{,}159$, $\\operatorname{SiLU}=-0{,}269$. Точки на нижнем графике — наибольшие отличия от ReLU: $0{,}170$ у GELU и $0{,}278$ у SiLU; это и глубины их минимумов."),
        ("callout", "note", "Связь с сигмоидой", "Функции распределения нормального и логистического законов очень похожи: $\\Phi(x)\\approx\\sigma(1{,}702\\,x)$ с ошибкой не больше $0{,}0095$. Поэтому GELU почти совпадает с $x\\,\\sigma(1{,}702x)$ — это SiLU с растянутой сигмоидой. Подробнее о самой $\\sigma$ — на странице <a href=\"../sigmoid/\">сигмоиды</a>."),
    ]),
    dict(id="derivative", title="Производная: Φ(x) + x·φ(x)", blocks=[
        ("p", "Производная нужна при обратном распространении ошибки. Выведем её и найдём минимум функции."),
        ("deep", "Вывод первой и второй производной", [
            ("p", "Главный факт: производная функции распределения — плотность, $\\Phi'(x)=\\varphi(x)$ (основная теорема анализа для интеграла с переменным верхним пределом). По правилу производной произведения:"),
            ("eq", r"\operatorname{GELU}'(x)=(x)'\cdot\Phi(x)+x\cdot\Phi'(x)=\Phi(x)+x\,\varphi(x)"),
            ("p", "У гауссианы $\\varphi'(x)=-x\\,\\varphi(x)$. Дифференцируем ещё раз:"),
            ("eq", r"\operatorname{GELU}''(x)=\varphi(x)+\varphi(x)+x\cdot\bigl(-x\,\varphi(x)\bigr)=\varphi(x)\,\bigl(2-x^{2}\bigr)"),
            ("p", "Знак $\\operatorname{GELU}''$ совпадает со знаком $2-x^2$: функция выпукла на $(-\\sqrt2;\\,\\sqrt2)$ и вогнута вне этого отрезка, а производная $\\operatorname{GELU}'$ имеет экстремумы в точках $x=\\pm\\sqrt2$."),
        ]),
        ("eq", r"\operatorname{GELU}'(x)=\underbrace{\Phi(x)}_{\text{доля}}+\underbrace{x\,\varphi(x)}_{\text{изменение доли}}"),
        ("p", "У производной два слагаемых. Первое — сама доля $\\Phi(x)$: так вела бы себя производная, если бы вентиль не зависел от $x$. Второе — поправка от того, что вентиль открывается при росте $x$; она положительна справа от нуля и отрицательна слева. Сравните с ReLU, у которой производная — ступенька 0/1."),
        ("viz", "gelu-derivative", {"x": -0.75}, "<b>Рисунок 4.</b> Производная GELU (оранжевая) и два её слагаемых. Наибольшее значение $\\Phi(\\sqrt2)+\\sqrt2\\,\\varphi(\\sqrt2)\\approx1{,}129$, наименьшее $\\approx-0{,}129$ при $x=-\\sqrt2$ — сумма этих чисел равна 1, ведь $\\operatorname{GELU}'(x)+\\operatorname{GELU}'(-x)=1$. Производная обращается в ноль при $x\\approx-0{,}752$; в начальной точке $x=-0{,}75$ она уже почти нулевая. Включите вторую производную: её нули — в $\\pm\\sqrt2$."),
        ("h3", "Где минимум"),
        ("p", "Минимум — там, где $\\operatorname{GELU}'(x)=0$, то есть $\\Phi(x)=-x\\,\\varphi(x)$. Это уравнение не решается в элементарных функциях; метод Ньютона $x_{k+1}=x_k-\\operatorname{GELU}'(x_k)/\\operatorname{GELU}''(x_k)$ от $x_0=-1$ даёт $-0{,}6557$, $-0{,}7448$, $-0{,}75175$, $-0{,}751792$ — каждая итерация примерно удваивает число верных знаков."),
        ("eq", r"x^{*}\approx-0{,}7518,\qquad \operatorname{GELU}(x^{*})=x^{*}\Phi(x^{*})=-(x^{*})^{2}\varphi(x^{*})\approx-0{,}1700"),
        ("p", "Второе равенство следует из условия минимума $\\Phi(x^*)=-x^*\\varphi(x^*)$. В минимуме пропускается доля $\\Phi(x^*)\\approx0{,}226$."),
        ("callout", "intuition", "Отрицательный градиент слева", "При $x&lt;-0{,}752$ производная отрицательна: если увеличить вход, выход <i>уменьшится</i>. ReLU в этой зоне даёт ровно ноль, а GELU — маленький, но ненулевой сигнал (не меньше $-0{,}129$). Он затухает как гауссиана: $\\operatorname{GELU}'(-3)\\approx-0{,}012$, $\\operatorname{GELU}'(-4)\\approx-0{,}0005$."),
    ]),
    dict(id="approx", title="Быстрые приближения: tanh и сигмоида", blocks=[
        ("p", "В 2016 году функция erf была медленной или вовсе отсутствовала во фреймворках, поэтому авторы предложили два приближения. Первое использует tanh:"),
        ("eq", r"\operatorname{GELU}(x)\approx\frac{x}{2}\Bigl(1+\tanh\Bigl[\sqrt{2/\pi}\,\bigl(x+0{,}044715\,x^{3}\bigr)\Bigr]\Bigr)"),
        ("p", "Именно эта формула записана в исходном коде BERT и GPT-2 (в библиотеке Hugging Face она называется <code>gelu_new</code>, в PyTorch — <code>approximate=\"tanh\"</code>). Наибольшая ошибка — $4{,}7\\cdot10^{-4}$ при $|x|\\approx2{,}70$. Второе приближение — через сигмоиду:"),
        ("eq", r"\operatorname{GELU}(x)\approx x\,\sigma(1{,}702\,x)"),
        ("p", "Оно грубее: ошибка до $0{,}020$ при $|x|\\approx2{,}27$. Обе ошибки — чётные функции, потому что все три формулы удовлетворяют тождеству $f(x)-f(-x)=x$."),
        ("deep", "Откуда берутся √(2/π) и 0,044715", [
            ("p", "Нужно приблизить $\\operatorname{erf}(z)$ функцией $\\tanh(u)$. Разложим обе около нуля: $\\operatorname{erf}(z)=\\frac{2}{\\sqrt\\pi}\\bigl(z-\\frac{z^3}{3}+\\dots\\bigr)$ и $\\tanh u=u-\\frac{u^3}{3}+\\dots$. Возьмём $u=\\frac{2}{\\sqrt\\pi}(z+cz^3)$ и приравняем коэффициенты."),
            ("eq", r"z^{1}:\ \ \frac{2}{\sqrt\pi}=\frac{2}{\sqrt\pi};\qquad z^{3}:\ \ \frac{2c}{\sqrt\pi}-\frac{8}{3\pi\sqrt\pi}=-\frac{2}{3\sqrt\pi}\ \Longrightarrow\ c=\frac{4}{3\pi}-\frac13"),
            ("p", "Подставляя $z=x/\\sqrt2$, получаем $\\sqrt{2/\\pi}\\,(x+c'x^3)$ с $c'=c/2=\\frac{2}{3\\pi}-\\frac16\\approx0{,}0455$. Совпадение рядов даёт точность только около нуля, поэтому авторы подобрали коэффициент численно по всей оси: $0{,}044715$. С тейлоровским $0{,}0455$ максимальная ошибка $7{,}5\\cdot10^{-4}$, с $0{,}044715$ — $4{,}7\\cdot10^{-4}$, а без кубического члена ($c'=0$) — $0{,}034$."),
        ]),
        ("viz", "gelu-approx", {"c": 0.044715, "x": 1}, "<b>Рисунок 5.</b> Сверху — точная GELU и два приближения, снизу — модуль ошибки в логарифмической шкале (провалы — точки, где ошибка меняет знак). Двигайте коэффициент $c$: при $c=0{,}044715$ максимальная ошибка $4{,}7\\cdot10^{-4}$, при $c=0$ — $0{,}034$. При $x=1$: точное значение $0{,}8413$, tanh-приближение $0{,}8412$, сигмоидное $0{,}8458$."),
        ("callout", "warn", "Это разные функции", "Модель, обученная с tanh-приближением, в выводе должна использовать его же. Разница не больше $4{,}7\\cdot10^{-4}$ на нейрон, но в сотнях слоёв и тысячах нейронов она даёт заметное расхождение логитов при конвертации весов и ломает побитовые тесты."),
    ]),
    dict(id="space", title="Семейство x·Φ(x/s) в 3D: от ReLU к прямой", blocks=[
        ("p", "Шум в маске не обязан быть единичным. Если $\\varepsilon\\sim N(0,s^2)$, то $P(\\varepsilon\\le x)=\\Phi(x/s)$, и получается целое семейство функций с «температурой» $s$:"),
        ("eq", r"f(x,s)=x\,\Phi\Bigl(\frac{x}{s}\Bigr)=s\cdot\operatorname{GELU}\Bigl(\frac{x}{s}\Bigr)"),
        ("ul", [
            "$s\\to0$: шума нет, $\\Phi(x/s)$ превращается в ступеньку, и $f\\to\\operatorname{ReLU}(x)$;",
            "$s=1$: обычная GELU;",
            "$s\\to\\infty$: шум заглушает вход, $\\Phi(x/s)\\to\\tfrac12$, и $f\\to x/2$ — прямая, нелинейность исчезает.",
        ]),
        ("p", "Второе равенство показывает, что все члены семейства подобны: минимум находится в точке $x=-0{,}752\\,s$ и равен $-0{,}170\\,s$. На поверхности это прямая бирюзовая линия на дне «оврага»."),
        ("viz", "gelu-surface", {"s": 1}, "<b>Рисунок 6.</b> Поверхность $f(x,s)=x\\,\\Phi(x/s)$ (её можно вращать) и срез при текущем $s$. Оранжевая линия — срез, бирюзовая — линия минимумов. При $s=1$ минимум в $x=-0{,}752$ равен $-0{,}170$. Переключитесь на производную: при малых $s$ она становится ступенькой ReLU, при больших — прижимается к $\\tfrac12$."),
        ("p", "В сети GELU применяется к вектору поэлементно: $h=\\operatorname{GELU}(W_1x+b_1)$. Каждая координата — своя «складка» вдоль гиперплоскости $w_j^\\top x+b_j=0$, но в отличие от ReLU складка гладкая, с небольшим отрицательным провалом перед изломом."),
    ]),
    dict(id="training", title="GELU в обучении и в трансформере", blocks=[
        ("p", "Сеть с одним скрытым слоем строит ответ как сумму «кирпичиков» $w_{2j}\\,f(w_{1j}x+b_{1j})$. У ReLU каждый кирпичик — ломаная с одним изломом, и сумма — тоже ломаная. У GELU кирпичики гладкие, поэтому гладкую зависимость можно описать меньшим их числом."),
        ("viz", "gelu-train", {"h": 4}, "<b>Рисунок 7.</b> Одна и та же сеть из 4 нейронов с одинаковой инициализацией, обучение Adam с шагом $0{,}03$ на 40 точках зашумлённой кривой $\\sin1{,}5x+0{,}3x$. Справа — среднеквадратичная ошибка (MSE) в логарифмической шкале. За 2000 шагов GELU-сеть снижает MSE с $7{,}06$ до $0{,}0042$ — это уже уровень шума в данных ($0{,}0051$), а ReLU-сеть застревает на $0{,}0083$: четырёх изломов не хватает. Кнопка «Нейроны» показывает отдельные кирпичики."),
        ("p", "Обучение использует ту же производную: градиент, приходящий к нейрону, умножается на $\\operatorname{GELU}'(z)=\\Phi(z)+z\\varphi(z)$. В отличие от ReLU, нейрон с отрицательным $z$ продолжает получать сигнал, поэтому GELU-сети реже страдают от «мёртвых» нейронов."),
        ("h3", "Блок прямого распространения трансформера"),
        ("p", "В BERT и GPT после каждого слоя внимания (attention) стоит двухслойный перцептрон, который обрабатывает каждый токен отдельно:"),
        ("eq", r"\operatorname{FFN}(h)=W_2\,\operatorname{GELU}(W_1h+b_1)+b_2,\qquad W_1\in\mathbb R^{4d\times d},\ \ W_2\in\mathbb R^{d\times4d}"),
        ("p", "В BERT-base $d=768$, так что на каждый токен в каждом из 12 слоёв приходится $4d=3072$ вычисления GELU. Перед FFN стоит LayerNorm, поэтому входы $W_1h+b_1$ в начале обучения порядка единицы — ровно та область, где у GELU есть и «ямка», и плавный переход. Поэтому скорость самой активации важна, и вместо точной erf часто берут tanh-приближение."),
        ("callout", "history", "Как GELU стала стандартом", "Хендрикс и Гимпел предложили GELU в 2016 году и показали, что на задачах зрения, речи и текста она не хуже ReLU и ELU. Широкую известность ей принесли GPT (2018) и BERT (2018), затем GPT-2, GPT-3 и Vision Transformer (2020). В 2020 году Шазир показал, что вентильные варианты GeGLU и SwiGLU ещё лучше, и новые LLM чаще используют их."),
    ]),
    dict(id="code", title="В коде: точно, быстро и устойчиво", blocks=[
        ("p", "В NumPy нет функции erf, поэтому её берут из SciPy. Чтобы не терять точность при больших отрицательных $x$, функцию распределения удобно считать через дополнительную функцию ошибок: $\\Phi(x)=\\tfrac12\\operatorname{erfc}(-x/\\sqrt2)$. Формула $\\tfrac12(1+\\operatorname{erf})$ при $x=-10$ вычитает почти равные числа и даёт ровно 0, хотя истинное значение $\\operatorname{GELU}(-10)\\approx-7{,}6\\cdot10^{-23}$; для самой активации это неважно, но та же $\\Phi$ часто нужна и в других формулах."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Правило", "Выбирайте вариант GELU так же, как его выбрали при обучении весов: <code>nn.GELU()</code> — точная, <code>nn.GELU(approximate=\"tanh\")</code> — приближённая. Для новой модели разницы в качестве почти нет; tanh-вариант бывает быстрее на старом железе."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>Считать, что выход GELU неотрицателен</b>, как у ReLU. Он может быть до $-0{,}170$; если дальше идёт логарифм, корень или деление, это нужно учитывать.",
            "<b>Смешивать точную GELU и tanh-приближение</b> между обучением и выводом или при конвертации модели (ONNX, TensorRT, другой фреймворк). Ошибка мала, но накапливается по слоям.",
            "<b>Путать $x\\,\\sigma(1{,}702x)$ с GELU.</b> Это быстрая аппроксимация с ошибкой до $0{,}02$, по сути <a href=\"../silu/\">SiLU</a> с параметром $\\beta=1{,}702$.",
            "<b>Думать, что GELU полностью избавляет от затухающих градиентов.</b> При $x\\to-\\infty$ производная гаснет как гауссиана: уже $\\operatorname{GELU}'(-4)\\approx-0{,}0005$. Нормализация входов по-прежнему нужна.",
            "<b>Писать $\\Phi$ как $\\tfrac12(1+\\operatorname{erf}(x))$, забыв деление на $\\sqrt2$.</b> Получится функция распределения $N(0,\\tfrac12)$, то есть $x\\Phi(\\sqrt2x)$ — другая кривая.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../relu/\">ReLU</a>: предел $x\\,\\Phi(x/s)$ при $s\\to0$ и «скелет» GELU: $\\operatorname{GELU}=\\operatorname{ReLU}-|x|\\Phi(-|x|)$.",
            "<a href=\"../silu/\">SiLU / Swish</a>: та же схема «вход × мягкий вентиль», но с сигмоидой вместо $\\Phi$; $x\\,\\sigma(1{,}702x)\\approx\\operatorname{GELU}(x)$.",
            "<a href=\"../sigmoid/\">Сигмоида</a>: $\\sigma(1{,}702x)$ приближает $\\Phi(x)$ с ошибкой не больше $0{,}0095$ — связь логит- и пробит-моделей.",
            "<a href=\"../tanh/\">tanh</a>: основа самого популярного приближения GELU.",
            "<a href=\"../leaky-relu/\">Leaky ReLU</a>: другой способ пропустить сигнал при $x&lt;0$ — постоянным маленьким наклоном вместо гладкой «ямки».",
            "<a href=\"../adam/\">Adam</a> и <a href=\"../mse/\">MSE</a>: оптимизатор и потеря из симуляции на рисунке 7.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $\\operatorname{GELU}(x)=x\\,\\Phi(x)$: вход, умноженный на вероятность $P(\\varepsilon\\le x)$ для $\\varepsilon\\sim N(0,1)$; это среднее от случайной маски, зависящей от входа. 2) $\\operatorname{GELU}=\\operatorname{ReLU}-|x|\\Phi(-|x|)$: гладкая ReLU с минимумом $-0{,}170$ при $x=-0{,}752$. 3) $\\operatorname{GELU}'=\\Phi+x\\varphi\\in(-0{,}129;\\,1{,}129)$, $\\operatorname{GELU}''=\\varphi\\,(2-x^2)$. 4) tanh-приближение с коэффициентом $0{,}044715$ ошибается не больше чем на $4{,}7\\cdot10^{-4}$, но это другая функция. 5) $x\\,\\Phi(x/s)$ соединяет ReLU ($s\\to0$) и $x/2$ ($s\\to\\infty$). 6) Стоит в FFN-блоках BERT, GPT и ViT."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="Чему примерно равна $\\operatorname{GELU}(-1)$?", options=["$-1$", "$-0{,}159$", "$0$", "$0{,}841$"], answer=1,
                 explain="$\\operatorname{GELU}(-1)=-1\\cdot\\Phi(-1)=-0{,}159$: пропускается только 15,9% отрицательного входа."),
            dict(q="Чему равна производная GELU в нуле?", options=["$0$", "$0{,}25$", "$0{,}5$", "$1$"], answer=2,
                 explain="$\\operatorname{GELU}'(0)=\\Phi(0)+0\\cdot\\varphi(0)=\\tfrac12$."),
            dict(q="Где находится минимум GELU?", options=["В нуле, значение 0", "При $x\\approx-0{,}75$, значение $\\approx-0{,}17$", "При $x=-1$, значение $-0{,}159$", "Минимума нет"], answer=1,
                 explain="Минимум там, где $\\Phi(x)+x\\varphi(x)=0$: $x^*\\approx-0{,}752$, $\\operatorname{GELU}(x^*)\\approx-0{,}170$. Точка $x=-1$ лежит левее, на убывающей ветви."),
            dict(q="Что означает $\\Phi(x)$ в формуле GELU?", options=["Плотность нормального распределения в точке $x$", "Вероятность того, что $\\varepsilon\\sim N(0,1)$ не больше $x$ — доля, в которой вход пропускается", "Сигмоиду от $x$", "Дисперсию входов"], answer=1,
                 explain="$\\Phi$ — функция распределения: $\\Phi(x)=P(\\varepsilon\\le x)$. GELU — среднее $x\\cdot m$ для маски $m=\\mathbb 1[\\varepsilon\\le x]$."),
            dict(q="Чему равна $\\operatorname{GELU}(3)-\\operatorname{GELU}(-3)$?", options=["$0$", "$2{,}996$", "$3$", "$6$"], answer=2,
                 explain="$x\\Phi(x)-(-x)\\Phi(-x)=x\\bigl(\\Phi(x)+\\Phi(-x)\\bigr)=x$, так что разность равна ровно 3."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "An activation function is the nonlinearity placed after every linear layer. Without it, any number of layers collapses into a single matrix multiplication. For a long time the standard was <a href=\"../relu/\">ReLU</a>: $\\max(0,x)$ — let the positive through, zero out the negative. GELU (Gaussian Error Linear Unit, Hendrycks and Gimpel, 2016) solves the same task more gently: the input is not simply passed or cut, it is <b>multiplied by the probability</b> that it should be passed."),
        ("p", "Where it appears:"),
        ("ul", [
            "<b>BERT, RoBERTa, GPT, GPT-2, GPT-3</b> — in every feed-forward (FFN) block of the transformer: $\\operatorname{FFN}(h)=W_2\\,\\operatorname{GELU}(W_1h+b_1)+b_2$;",
            "<b>Vision Transformer (ViT)</b> and many computer-vision models after it;",
            "<b>GeGLU</b> — the gated variant $\\operatorname{GELU}(xW)\\odot(xV)$, used for example in Gemma; its relative SwiGLU with <a href=\"../silu/\">SiLU</a> powers LLaMA and Qwen;",
            "<b>wherever smoothness matters</b>: GELU has derivatives of every order, no kink at zero and no “dead” zone with zero gradient like ReLU.",
        ]),
        ("callout", "key", "The essentials in a minute", "$\\operatorname{GELU}(x)=x\\,\\Phi(x)$, where $\\Phi$ is the cumulative distribution function of the standard normal law. Large positive $x$ pass almost entirely, large negative ones are almost zeroed out, and near zero there is a smooth transition. The function has a minimum of $\\approx-0.170$ at $x\\approx-0.752$, its derivative $\\Phi(x)+x\\varphi(x)$ stays between $-0.129$ and $1.129$, and in practice it is often computed with a tanh approximation whose error never exceeds $4.7\\cdot10^{-4}$."),
    ]),
    dict(id="intuition", title="Intuition: the input times a probability", blocks=[
        ("p", "Imagine a gate that decides what share of the signal $x$ to let through. ReLU’s gate is hard: for $x&gt;0$ it is fully open, for $x&lt;0$ it is shut. GELU’s gate is open by $\\Phi(x)$ — a share between 0 and 1 that grows smoothly with $x$. A large positive signal passes almost entirely, a large negative one is almost extinguished, and near zero half of the signal gets through: $\\Phi(0)=0.5$."),
        ("p", "Drag the point. The grey bar is the whole input $x$, the blue one is the part that got through: its length is $x\\cdot\\Phi(x)$. The teal dashed line is the share $\\Phi(x)$ itself."),
        ("viz", "gelu-explorer", {"x": 1}, "<b>Figure 1.</b> GELU, the share $\\Phi(x)$ and the derivative. At $x=1$ the share $\\Phi(1)\\approx0.841$ passes, so $\\operatorname{GELU}(1)\\approx0.841$; at $x=-1$ only $0.159$ passes, and the output is $-0.159$. The circle marks the minimum of the function."),
        ("callout", "intuition", "What to notice", "For negative $x$ the output is not zero: it is negative and small. As $x$ goes down from zero the output first decreases (the input grows in magnitude faster than the share falls), and from about $x=-0.75$ it rises back towards zero: the share $\\Phi(x)$ dies out faster than $|x|$ grows. Hence a shallow “dip” — the main difference between the shapes of GELU and ReLU."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("p", "All the complexity of GELU is hidden in $\\Phi$. Let us take it apart."),
        ("eq", r"\operatorname{GELU}(x)=x\cdot\Phi(x),\qquad \Phi(x)=\int_{-\infty}^{x}\varphi(t)\,dt,\qquad \varphi(t)=\frac{1}{\sqrt{2\pi}}\,e^{-t^{2}/2}"),
        ("symbols", [
            (r"\varphi(t)", "the density of the standard normal distribution $N(0,1)$ — the Gaussian bell with its maximum $1/\\sqrt{2\\pi}\\approx0.399$ at zero;"),
            (r"\Phi(x)", "the cumulative distribution function: the area under the bell to the left of $x$, i.e. the probability $P(\\varepsilon\\le x)$ for $\\varepsilon\\sim N(0,1)$; it grows from 0 to 1, $\\Phi(0)=\\tfrac12$;"),
            (r"x\cdot\Phi(x)", "the input multiplied by that probability."),
        ]),
        ("p", "The integral of a Gaussian cannot be expressed through elementary functions, so it has a special name — the error function, hence “Gaussian <i>Error</i> Linear Unit”:"),
        ("eq", r"\operatorname{erf}(z)=\frac{2}{\sqrt\pi}\int_0^{z}e^{-t^2}\,dt,\qquad \Phi(x)=\frac12\Bigl(1+\operatorname{erf}\frac{x}{\sqrt2}\Bigr)\quad\Longrightarrow\quad\operatorname{GELU}(x)=\frac{x}{2}\Bigl(1+\operatorname{erf}\frac{x}{\sqrt2}\Bigr)"),
        ("p", "The factor $1/\\sqrt2$ converts the standard normal variable with density $e^{-t^2/2}$ to the kernel $e^{-t^2}$ for which erf is defined. The erf itself is odd and runs from $-1$ to $1$, so $\\tfrac12(1+\\operatorname{erf})$ runs from 0 to 1."),
        ("table", ["$x$", "$\\Phi(x)$", "$\\operatorname{GELU}(x)$", "$\\operatorname{GELU}'(x)$", "$\\operatorname{ReLU}(x)$"], "TABLE", {"num": [0, 1, 2, 3, 4]}),
        ("p", "The table shows three things. On the right GELU quickly catches up with ReLU: at $x=3$ the difference is only $0.004$. On the left the output is negative but small: the deepest value in the table is $-0.159$ at $x=-1$. The derivative at zero is $0.5$, and for $x\\ge1$ it exceeds one — the function grows slightly faster than the line $y=x$ as it catches up with it."),
    ]),
    dict(id="origin", title="Where it came from: a noisy mask on average", blocks=[
        ("p", "The authors of GELU combined two ideas. <b>ReLU</b> multiplies the input by a deterministic mask: $x\\cdot\\mathbb 1[x&gt;0]$. <b>Dropout</b> multiplies the input by a random mask that does not depend on the input. What if the mask is random but <i>does</i> depend on the input: the larger $x$, the more likely it is to be passed?"),
        ("eq", r"m\sim\operatorname{Bernoulli}\bigl(\Phi(x)\bigr),\qquad \mathbb E\,[\,x\cdot m\,]=x\cdot P(m=1)=x\,\Phi(x)=\operatorname{GELU}(x)"),
        ("p", "Such a mask is easy to build: take noise $\\varepsilon\\sim N(0,1)$ and set $m=1$ if $\\varepsilon\\le x$. Then $P(m=1)=\\Phi(x)$ by the definition of the distribution function. Why the normal law? After normalizations (BatchNorm, LayerNorm) neuron inputs are distributed roughly as $N(0,1)$, and $\\Phi(x)$ answers a natural question: what share of typical inputs is smaller than this $x$."),
        ("viz", "gelu-mask", {"x": 0.5, "seed": 3}, "<b>Figure 2.</b> On the left, the orange dots are the mean of $x\\cdot m$ over $n$ random masks at 25 points from $-3$ to $3$; on the right, the noise $\\varepsilon$ and the share $\\Phi(x_0)$ for which the mask is open. Press “Play”: at $n=20$ the largest deviation from GELU is $0.146$, at $n=2000$ it is down to $0.0125$; the error of the mean shrinks as $1/\\sqrt n$. At $x_0=0.5$ the share of open masks approaches $\\Phi(0.5)\\approx0.691$."),
        ("callout", "note", "GELU itself is not random", "The noisy mask only explains the shape. The network uses the deterministic mean $x\\Phi(x)$: there is no randomness in training or inference (if noise is wanted, dropout is added separately)."),
    ]),
    dict(id="properties", title="Properties and shape", blocks=[
        ("ul", [
            "<b>Range</b>: $[-0.170,\\,+\\infty)$ — bounded below, unbounded above.",
            "<b>Smoothness</b>: GELU is infinitely differentiable; $\\operatorname{GELU}(0)=0$, $\\operatorname{GELU}'(0)=\\tfrac12$.",
            "<b>Non-monotonicity</b>: the function decreases on $(-\\infty,\\,-0.752)$ and increases to the right; the minimum is $\\approx-0.170$.",
            "<b>Asymptotes</b>: $\\operatorname{GELU}(x)-x\\to0$ as $x\\to+\\infty$ and $\\operatorname{GELU}(x)\\to0$ as $x\\to-\\infty$, with the left tail dying out like a Gaussian: $x\\Phi(x)\\approx-\\varphi(x)$, already $\\operatorname{GELU}(-4)\\approx-1.3\\cdot10^{-4}$.",
            "<b>Identity</b>: $\\operatorname{GELU}(x)-\\operatorname{GELU}(-x)=x$, because $\\Phi(x)+\\Phi(-x)=1$.",
            "<b>Convexity</b>: only on $[-\\sqrt2,\\,\\sqrt2]$; outside it the function is concave (the sign of the second derivative is in the next section).",
        ]),
        ("h3", "GELU = ReLU minus an even “dip”"),
        ("p", "The identity gives a handy form. For $x&gt;0$: $x\\Phi(x)=x-x\\Phi(-x)$; for $x&lt;0$: $x\\Phi(x)=-|x|\\Phi(-|x|)$. In both cases"),
        ("eq", r"\operatorname{GELU}(x)=\operatorname{ReLU}(x)-|x|\,\Phi(-|x|)"),
        ("p", "The correction $|x|\\Phi(-|x|)$ is even: it is the same on both sides of zero, peaks at $0.170$ at $|x|=0.752$ and fades quickly. <a href=\"../silu/\">SiLU</a> $x\\,\\sigma(x)$ has the same property, only its dip is wider and deeper: $0.278$ at $|x|=1.278$."),
        ("viz", "gelu-family", {"x": -1}, "<b>Figure 3.</b> Top: GELU, SiLU and ReLU; bottom: the differences $\\operatorname{ReLU}-f$. Hover over either plot. At $x=-1$: $\\operatorname{GELU}=-0.159$, $\\operatorname{SiLU}=-0.269$. The dots on the lower plot are the largest gaps from ReLU: $0.170$ for GELU and $0.278$ for SiLU; these are also the depths of their minima."),
        ("callout", "note", "The link with the sigmoid", "The distribution functions of the normal and logistic laws are very close: $\\Phi(x)\\approx\\sigma(1.702\\,x)$ with an error of at most $0.0095$. That is why GELU nearly coincides with $x\\,\\sigma(1.702x)$ — SiLU with a stretched sigmoid. More about $\\sigma$ itself is on the <a href=\"../sigmoid/\">sigmoid</a> page."),
    ]),
    dict(id="derivative", title="The derivative: Φ(x) + x·φ(x)", blocks=[
        ("p", "The derivative is needed for backpropagation. Let us derive it and find the minimum of the function."),
        ("deep", "Deriving the first and second derivatives", [
            ("p", "The key fact: the derivative of a distribution function is the density, $\\Phi'(x)=\\varphi(x)$ (the fundamental theorem of calculus for an integral with a variable upper limit). By the product rule:"),
            ("eq", r"\operatorname{GELU}'(x)=(x)'\cdot\Phi(x)+x\cdot\Phi'(x)=\Phi(x)+x\,\varphi(x)"),
            ("p", "For the Gaussian, $\\varphi'(x)=-x\\,\\varphi(x)$. Differentiating once more:"),
            ("eq", r"\operatorname{GELU}''(x)=\varphi(x)+\varphi(x)+x\cdot\bigl(-x\,\varphi(x)\bigr)=\varphi(x)\,\bigl(2-x^{2}\bigr)"),
            ("p", "The sign of $\\operatorname{GELU}''$ is the sign of $2-x^2$: the function is convex on $(-\\sqrt2,\\,\\sqrt2)$ and concave outside it, and the derivative $\\operatorname{GELU}'$ has its extrema at $x=\\pm\\sqrt2$."),
        ]),
        ("eq", r"\operatorname{GELU}'(x)=\underbrace{\Phi(x)}_{\text{share}}+\underbrace{x\,\varphi(x)}_{\text{change of the share}}"),
        ("p", "The derivative has two terms. The first is the share $\\Phi(x)$ itself: that is how the derivative would look if the gate did not depend on $x$. The second is a correction for the gate opening as $x$ grows; it is positive to the right of zero and negative to the left. Compare with ReLU, whose derivative is a 0/1 step."),
        ("viz", "gelu-derivative", {"x": -0.75}, "<b>Figure 4.</b> The derivative of GELU (orange) and its two terms. The largest value is $\\Phi(\\sqrt2)+\\sqrt2\\,\\varphi(\\sqrt2)\\approx1.129$, the smallest is $\\approx-0.129$ at $x=-\\sqrt2$ — the two add up to 1, since $\\operatorname{GELU}'(x)+\\operatorname{GELU}'(-x)=1$. The derivative vanishes at $x\\approx-0.752$; at the starting point $x=-0.75$ it is already almost zero. Turn on the second derivative: its zeros are at $\\pm\\sqrt2$."),
        ("h3", "Where the minimum is"),
        ("p", "The minimum is where $\\operatorname{GELU}'(x)=0$, i.e. $\\Phi(x)=-x\\,\\varphi(x)$. This equation has no solution in elementary functions; Newton’s method $x_{k+1}=x_k-\\operatorname{GELU}'(x_k)/\\operatorname{GELU}''(x_k)$ from $x_0=-1$ gives $-0.6557$, $-0.7448$, $-0.75175$, $-0.751792$ — every iteration roughly doubles the number of correct digits."),
        ("eq", r"x^{*}\approx-0.7518,\qquad \operatorname{GELU}(x^{*})=x^{*}\Phi(x^{*})=-(x^{*})^{2}\varphi(x^{*})\approx-0.1700"),
        ("p", "The second equality follows from the minimum condition $\\Phi(x^*)=-x^*\\varphi(x^*)$. At the minimum the share $\\Phi(x^*)\\approx0.226$ gets through."),
        ("callout", "intuition", "A negative gradient on the left", "For $x&lt;-0.752$ the derivative is negative: if the input increases, the output <i>decreases</i>. ReLU gives exactly zero in this zone, while GELU gives a small but non-zero signal (no lower than $-0.129$). It fades like a Gaussian: $\\operatorname{GELU}'(-3)\\approx-0.012$, $\\operatorname{GELU}'(-4)\\approx-0.0005$."),
    ]),
    dict(id="approx", title="Fast approximations: tanh and the sigmoid", blocks=[
        ("p", "In 2016 the erf function was slow or simply missing in frameworks, so the authors proposed two approximations. The first one uses tanh:"),
        ("eq", r"\operatorname{GELU}(x)\approx\frac{x}{2}\Bigl(1+\tanh\Bigl[\sqrt{2/\pi}\,\bigl(x+0.044715\,x^{3}\bigr)\Bigr]\Bigr)"),
        ("p", "This is the formula in the original BERT and GPT-2 code (Hugging Face calls it <code>gelu_new</code>, PyTorch — <code>approximate=\"tanh\"</code>). Its largest error is $4.7\\cdot10^{-4}$ at $|x|\\approx2.70$. The second approximation uses the sigmoid:"),
        ("eq", r"\operatorname{GELU}(x)\approx x\,\sigma(1.702\,x)"),
        ("p", "It is coarser: the error reaches $0.020$ at $|x|\\approx2.27$. Both errors are even functions, because all three formulas satisfy the identity $f(x)-f(-x)=x$."),
        ("deep", "Where √(2/π) and 0.044715 come from", [
            ("p", "We need to approximate $\\operatorname{erf}(z)$ with $\\tanh(u)$. Expand both around zero: $\\operatorname{erf}(z)=\\frac{2}{\\sqrt\\pi}\\bigl(z-\\frac{z^3}{3}+\\dots\\bigr)$ and $\\tanh u=u-\\frac{u^3}{3}+\\dots$. Take $u=\\frac{2}{\\sqrt\\pi}(z+cz^3)$ and match the coefficients."),
            ("eq", r"z^{1}:\ \ \frac{2}{\sqrt\pi}=\frac{2}{\sqrt\pi};\qquad z^{3}:\ \ \frac{2c}{\sqrt\pi}-\frac{8}{3\pi\sqrt\pi}=-\frac{2}{3\sqrt\pi}\ \Longrightarrow\ c=\frac{4}{3\pi}-\frac13"),
            ("p", "Substituting $z=x/\\sqrt2$ gives $\\sqrt{2/\\pi}\\,(x+c'x^3)$ with $c'=c/2=\\frac{2}{3\\pi}-\\frac16\\approx0.0455$. Matching the series guarantees accuracy only near zero, so the authors fitted the coefficient numerically over the whole axis: $0.044715$. With the Taylor value $0.0455$ the maximum error is $7.5\\cdot10^{-4}$, with $0.044715$ it is $4.7\\cdot10^{-4}$, and without the cubic term ($c'=0$) it is $0.034$."),
        ]),
        ("viz", "gelu-approx", {"c": 0.044715, "x": 1}, "<b>Figure 5.</b> Top: the exact GELU and the two approximations; bottom: the absolute error on a log scale (the dips are the points where the error changes sign). Move the coefficient $c$: at $c=0.044715$ the maximum error is $4.7\\cdot10^{-4}$, at $c=0$ it is $0.034$. At $x=1$: the exact value is $0.8413$, the tanh approximation $0.8412$, the sigmoid one $0.8458$."),
        ("callout", "warn", "These are different functions", "A model trained with the tanh approximation must use it at inference too. The difference is at most $4.7\\cdot10^{-4}$ per neuron, but over hundreds of layers and thousands of neurons it produces a noticeable mismatch of logits when weights are converted, and it breaks bit-exact tests."),
    ]),
    dict(id="space", title="The x·Φ(x/s) family in 3D: from ReLU to a line", blocks=[
        ("p", "The noise in the mask need not have unit scale. If $\\varepsilon\\sim N(0,s^2)$, then $P(\\varepsilon\\le x)=\\Phi(x/s)$, and we get a whole family of functions with a “temperature” $s$:"),
        ("eq", r"f(x,s)=x\,\Phi\Bigl(\frac{x}{s}\Bigr)=s\cdot\operatorname{GELU}\Bigl(\frac{x}{s}\Bigr)"),
        ("ul", [
            "$s\\to0$: no noise, $\\Phi(x/s)$ becomes a step, and $f\\to\\operatorname{ReLU}(x)$;",
            "$s=1$: the usual GELU;",
            "$s\\to\\infty$: the noise drowns the input, $\\Phi(x/s)\\to\\tfrac12$, and $f\\to x/2$ — a straight line, the nonlinearity disappears.",
        ]),
        ("p", "The second equality shows that all members of the family are similar: the minimum is at $x=-0.752\\,s$ and equals $-0.170\\,s$. On the surface this is the straight teal line along the bottom of the “ravine”."),
        ("viz", "gelu-surface", {"s": 1}, "<b>Figure 6.</b> The surface $f(x,s)=x\\,\\Phi(x/s)$ (you can rotate it) and the slice at the current $s$. The orange line is the slice, the teal one is the line of minima. At $s=1$ the minimum at $x=-0.752$ equals $-0.170$. Switch to the derivative: for small $s$ it becomes ReLU’s step, for large $s$ it flattens towards $\\tfrac12$."),
        ("p", "In a network GELU is applied to a vector element-wise: $h=\\operatorname{GELU}(W_1x+b_1)$. Each coordinate is its own “fold” along the hyperplane $w_j^\\top x+b_j=0$, but unlike ReLU the fold is smooth, with a small negative dip before the bend."),
    ]),
    dict(id="training", title="GELU in training and in the transformer", blocks=[
        ("p", "A network with one hidden layer builds its answer as a sum of “bricks” $w_{2j}\\,f(w_{1j}x+b_{1j})$. With ReLU every brick is a broken line with a single bend, and the sum is a broken line too. With GELU the bricks are smooth, so a smooth dependence can be described with fewer of them."),
        ("viz", "gelu-train", {"h": 4}, "<b>Figure 7.</b> The same network of 4 neurons with identical initialization, trained by Adam with step $0.03$ on 40 points of the noisy curve $\\sin1.5x+0.3x$. On the right, the mean squared error (MSE) on a log scale. In 2000 steps the GELU network brings the MSE from $7.06$ down to $0.0042$ — the noise level of the data ($0.0051$) — while the ReLU network gets stuck at $0.0083$: four bends are not enough. The “Neurons” buttons show the individual bricks."),
        ("p", "Training uses the same derivative: the gradient arriving at a neuron is multiplied by $\\operatorname{GELU}'(z)=\\Phi(z)+z\\varphi(z)$. Unlike ReLU, a neuron with negative $z$ keeps receiving a signal, so GELU networks suffer less from “dead” neurons."),
        ("h3", "The transformer’s feed-forward block"),
        ("p", "In BERT and GPT every attention layer is followed by a two-layer perceptron that processes each token on its own:"),
        ("eq", r"\operatorname{FFN}(h)=W_2\,\operatorname{GELU}(W_1h+b_1)+b_2,\qquad W_1\in\mathbb R^{4d\times d},\ \ W_2\in\mathbb R^{d\times4d}"),
        ("p", "In BERT-base $d=768$, so each token in each of the 12 layers needs $4d=3072$ GELU evaluations. The FFN is preceded by LayerNorm, so at the start of training the inputs $W_1h+b_1$ are of order one — exactly the region where GELU has both the dip and the smooth transition. That is why the speed of the activation itself matters, and the tanh approximation is often used instead of the exact erf."),
        ("callout", "history", "How GELU became the standard", "Hendrycks and Gimpel proposed GELU in 2016 and showed that on vision, speech and text tasks it is no worse than ReLU and ELU. It became widely known through GPT (2018) and BERT (2018), then GPT-2, GPT-3 and the Vision Transformer (2020). In 2020 Shazeer showed that the gated variants GeGLU and SwiGLU are better still, and newer LLMs mostly use those."),
    ]),
    dict(id="code", title="In code: exact, fast and stable", blocks=[
        ("p", "NumPy has no erf function, so it is taken from SciPy. To avoid losing precision at large negative $x$, compute the distribution function through the complementary error function: $\\Phi(x)=\\tfrac12\\operatorname{erfc}(-x/\\sqrt2)$. The formula $\\tfrac12(1+\\operatorname{erf})$ at $x=-10$ subtracts almost equal numbers and gives exactly 0, although the true value is $\\operatorname{GELU}(-10)\\approx-7.6\\cdot10^{-23}$; this does not matter for the activation itself, but the same $\\Phi$ is often needed in other formulas."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "The rule", "Pick the GELU variant the weights were trained with: <code>nn.GELU()</code> is exact, <code>nn.GELU(approximate=\"tanh\")</code> is the approximation. For a new model there is almost no difference in quality; the tanh variant can be faster on older hardware."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>Assuming GELU’s output is non-negative</b>, as with ReLU. It can go down to $-0.170$; if a logarithm, a square root or a division follows, this has to be taken into account.",
            "<b>Mixing the exact GELU and the tanh approximation</b> between training and inference, or when converting a model (ONNX, TensorRT, another framework). The error is small, but it accumulates across layers.",
            "<b>Confusing $x\\,\\sigma(1.702x)$ with GELU.</b> It is a fast approximation with an error of up to $0.02$, essentially <a href=\"../silu/\">SiLU</a> with $\\beta=1.702$.",
            "<b>Believing GELU fully cures vanishing gradients.</b> As $x\\to-\\infty$ the derivative dies out like a Gaussian: already $\\operatorname{GELU}'(-4)\\approx-0.0005$. Normalizing the inputs is still necessary.",
            "<b>Writing $\\Phi$ as $\\tfrac12(1+\\operatorname{erf}(x))$ and forgetting the division by $\\sqrt2$.</b> That is the distribution function of $N(0,\\tfrac12)$, i.e. $x\\Phi(\\sqrt2x)$ — a different curve.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../relu/\">ReLU</a>: the limit of $x\\,\\Phi(x/s)$ as $s\\to0$ and the “skeleton” of GELU: $\\operatorname{GELU}=\\operatorname{ReLU}-|x|\\Phi(-|x|)$.",
            "<a href=\"../silu/\">SiLU / Swish</a>: the same “input × soft gate” scheme with the sigmoid instead of $\\Phi$; $x\\,\\sigma(1.702x)\\approx\\operatorname{GELU}(x)$.",
            "<a href=\"../sigmoid/\">Sigmoid</a>: $\\sigma(1.702x)$ approximates $\\Phi(x)$ with an error of at most $0.0095$ — the link between logit and probit models.",
            "<a href=\"../tanh/\">tanh</a>: the basis of the most popular GELU approximation.",
            "<a href=\"../leaky-relu/\">Leaky ReLU</a>: another way to let a signal through for $x&lt;0$ — a constant small slope instead of a smooth dip.",
            "<a href=\"../adam/\">Adam</a> and <a href=\"../mse/\">MSE</a>: the optimizer and the loss of the simulation in Figure 7.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $\\operatorname{GELU}(x)=x\\,\\Phi(x)$: the input multiplied by the probability $P(\\varepsilon\\le x)$ for $\\varepsilon\\sim N(0,1)$; it is the mean of a random mask that depends on the input. 2) $\\operatorname{GELU}=\\operatorname{ReLU}-|x|\\Phi(-|x|)$: a smooth ReLU with a minimum of $-0.170$ at $x=-0.752$. 3) $\\operatorname{GELU}'=\\Phi+x\\varphi\\in(-0.129,\\,1.129)$, $\\operatorname{GELU}''=\\varphi\\,(2-x^2)$. 4) The tanh approximation with coefficient $0.044715$ is off by at most $4.7\\cdot10^{-4}$, but it is a different function. 5) $x\\,\\Phi(x/s)$ connects ReLU ($s\\to0$) and $x/2$ ($s\\to\\infty$). 6) It sits in the FFN blocks of BERT, GPT and ViT."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="What is $\\operatorname{GELU}(-1)$ approximately?", options=["$-1$", "$-0.159$", "$0$", "$0.841$"], answer=1,
                 explain="$\\operatorname{GELU}(-1)=-1\\cdot\\Phi(-1)=-0.159$: only 15.9% of the negative input gets through."),
            dict(q="What is the derivative of GELU at zero?", options=["$0$", "$0.25$", "$0.5$", "$1$"], answer=2,
                 explain="$\\operatorname{GELU}'(0)=\\Phi(0)+0\\cdot\\varphi(0)=\\tfrac12$."),
            dict(q="Where is the minimum of GELU?", options=["At zero, value 0", "At $x\\approx-0.75$, value $\\approx-0.17$", "At $x=-1$, value $-0.159$", "There is no minimum"], answer=1,
                 explain="The minimum is where $\\Phi(x)+x\\varphi(x)=0$: $x^*\\approx-0.752$, $\\operatorname{GELU}(x^*)\\approx-0.170$. The point $x=-1$ lies further left, on the decreasing branch."),
            dict(q="What does $\\Phi(x)$ mean in the GELU formula?", options=["The normal density at $x$", "The probability that $\\varepsilon\\sim N(0,1)$ is at most $x$ — the share of the input that is passed", "The sigmoid of $x$", "The variance of the inputs"], answer=1,
                 explain="$\\Phi$ is the distribution function: $\\Phi(x)=P(\\varepsilon\\le x)$. GELU is the mean of $x\\cdot m$ for the mask $m=\\mathbb 1[\\varepsilon\\le x]$."),
            dict(q="What is $\\operatorname{GELU}(3)-\\operatorname{GELU}(-3)$?", options=["$0$", "$2.996$", "$3$", "$6$"], answer=2,
                 explain="$x\\Phi(x)-(-x)\\Phi(-x)=x\\bigl(\\Phi(x)+\\Phi(-x)\\bigr)=x$, so the difference is exactly 3."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "Aktivatsiya funksiyasi — har bir chiziqli qatlamdan keyin turadigan nochiziqlilik. Usiz istalgancha qatlam bitta matritsaga ko‘paytirishga aylanib qoladi. Uzoq vaqt standart <a href=\"../relu/\">ReLU</a> edi: $\\max(0,x)$ — musbatni o‘tkazish, manfiyni nolga aylantirish. GELU (Gaussian Error Linear Unit, Xendriks va Gimpel, 2016) xuddi shu vazifani yumshoqroq hal qiladi: kirish shunchaki o‘tkazilmaydi yoki kesilmaydi, balki uni o‘tkazish kerakligi <b>ehtimolligiga ko‘paytiriladi</b>."),
        ("p", "U qayerda uchraydi:"),
        ("ul", [
            "<b>BERT, RoBERTa, GPT, GPT-2, GPT-3</b> — transformerning har bir to‘g‘ri tarqalish (feed-forward, FFN) blokida: $\\operatorname{FFN}(h)=W_2\\,\\operatorname{GELU}(W_1h+b_1)+b_2$;",
            "<b>Vision Transformer (ViT)</b> va undan keyingi ko‘plab kompyuter ko‘rishi modellarida;",
            "<b>GeGLU</b> — ventilli variant $\\operatorname{GELU}(xW)\\odot(xV)$, masalan Gemma’da; uning qarindoshi — <a href=\"../silu/\">SiLU</a>’li SwiGLU — LLaMA va Qwen’da;",
            "<b>silliqlik muhim bo‘lgan har joyda</b>: GELU’ning barcha tartibdagi hosilalari bor, nolda sinish yo‘q va ReLU’dagidek gradiyenti nol bo‘lgan «o‘lik» zona yo‘q.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "$\\operatorname{GELU}(x)=x\\,\\Phi(x)$, bunda $\\Phi$ — standart normal taqsimot funksiyasi. Katta musbat $x$ deyarli to‘liq o‘tadi, katta manfiylari deyarli nolga aylanadi, nol atrofida esa silliq o‘tish ishlaydi. Funksiyaning $x\\approx-0{,}752$ nuqtada $\\approx-0{,}170$ minimumi bor, $\\Phi(x)+x\\varphi(x)$ hosila $-0{,}129$ dan $1{,}129$ gacha oraliqda yotadi, amalda esa uni ko‘pincha xatosi $4{,}7\\cdot10^{-4}$ dan oshmaydigan tanh yaqinlashishi orqali hisoblashadi."),
    ]),
    dict(id="intuition", title="Intuitsiya: ehtimollikka ko‘paytirilgan kirish", blocks=[
        ("p", "$x$ signalning qancha ulushini o‘tkazishni hal qiladigan ventilni tasavvur qiling. ReLU’da ventil qattiq: $x&gt;0$ da to‘liq ochiq, $x&lt;0$ da yopiq. GELU’da ventil $\\Phi(x)$ ga ochiq — 0 dan 1 gacha bo‘lgan, $x$ bilan birga silliq o‘sadigan ulushga. Katta musbat signal deyarli to‘liq o‘tadi, katta manfiysi deyarli so‘nadi, nol atrofida esa signalning yarmi o‘tadi: $\\Phi(0)=0{,}5$."),
        ("p", "Nuqtani torting. Kulrang polosa — butun $x$ kirish, ko‘k polosa — uning o‘tgan qismi: uzunligi $x\\cdot\\Phi(x)$ ga teng. Moviy-yashil punktir — $\\Phi(x)$ ulushning o‘zi."),
        ("viz", "gelu-explorer", {"x": 1}, "<b>1-rasm.</b> GELU, $\\Phi(x)$ ulush va hosila. $x=1$ da $\\Phi(1)\\approx0{,}841$ ulush o‘tadi, shuning uchun $\\operatorname{GELU}(1)\\approx0{,}841$; $x=-1$ da faqat $0{,}159$ o‘tadi va chiqish $-0{,}159$ ga teng. Doiracha funksiya minimumini belgilaydi."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "Manfiy $x$ uchun chiqish nolga teng emas: u manfiy va kichik. $x$ noldan kamayganda chiqish avval kamayadi (kirish moduli ulush kamayishidan tezroq o‘sadi), taxminan $x=-0{,}75$ dan boshlab esa yana nolga ko‘tariladi: $\\Phi(x)$ ulush $|x|$ o‘sishidan tezroq so‘nadi. Shundan sayoz «chuqurcha» paydo bo‘ladi — GELU va ReLU shakllari orasidagi asosiy farq."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", "GELU’ning butun murakkabligi $\\Phi$ ichida yashiringan. Uni qismlarga ajratamiz."),
        ("eq", r"\operatorname{GELU}(x)=x\cdot\Phi(x),\qquad \Phi(x)=\int_{-\infty}^{x}\varphi(t)\,dt,\qquad \varphi(t)=\frac{1}{\sqrt{2\pi}}\,e^{-t^{2}/2}"),
        ("symbols", [
            (r"\varphi(t)", "standart normal taqsimot $N(0,1)$ zichligi — nolda $1/\\sqrt{2\\pi}\\approx0{,}399$ maksimumli Gauss qo‘ng‘irog‘i;"),
            (r"\Phi(x)", "taqsimot funksiyasi: qo‘ng‘iroq ostidagi $x$ nuqtadan chapdagi yuza, ya’ni $\\varepsilon\\sim N(0,1)$ uchun $P(\\varepsilon\\le x)$ ehtimollik; 0 dan 1 gacha o‘sadi, $\\Phi(0)=\\tfrac12$;"),
            (r"x\cdot\Phi(x)", "shu ehtimollikka ko‘paytirilgan kirish."),
        ]),
        ("p", "Gaussiana integrali elementar funksiyalar orqali ifodalanmaydi, shuning uchun uning maxsus nomi bor — xatolar funksiyasi (error function), «Gaussian <i>Error</i> Linear Unit» nomi shundan:"),
        ("eq", r"\operatorname{erf}(z)=\frac{2}{\sqrt\pi}\int_0^{z}e^{-t^2}\,dt,\qquad \Phi(x)=\frac12\Bigl(1+\operatorname{erf}\frac{x}{\sqrt2}\Bigr)\quad\Longrightarrow\quad\operatorname{GELU}(x)=\frac{x}{2}\Bigl(1+\operatorname{erf}\frac{x}{\sqrt2}\Bigr)"),
        ("p", "$1/\\sqrt2$ ko‘paytuvchi zichligi $e^{-t^2/2}$ bo‘lgan standart normal miqdorni erf aniqlangan $e^{-t^2}$ yadroga o‘tkazadi. erf’ning o‘zi toq, $-1$ dan $1$ gacha o‘zgaradi, shuning uchun $\\tfrac12(1+\\operatorname{erf})$ 0 dan 1 gacha o‘zgaradi."),
        ("table", ["$x$", "$\\Phi(x)$", "$\\operatorname{GELU}(x)$", "$\\operatorname{GELU}'(x)$", "$\\operatorname{ReLU}(x)$"], "TABLE", {"num": [0, 1, 2, 3, 4]}),
        ("p", "Jadval uch narsani ko‘rsatadi. O‘ngda GELU ReLU’ga tez yetib oladi: $x=3$ da farq atigi $0{,}004$. Chapda chiqish manfiy, lekin kichik: jadvaldagi eng chuqur qiymat — $x=-1$ da $-0{,}159$. Nolda hosila $0{,}5$ ga teng, $x\\ge1$ da esa birdan katta — funksiya $y=x$ to‘g‘ri chiziqqa yetib olish uchun undan biroz tezroq o‘sadi."),
    ]),
    dict(id="origin", title="U qayerdan kelgan: o‘rtacha shovqinli niqob", blocks=[
        ("p", "GELU mualliflari ikki g‘oyani birlashtirdi. <b>ReLU</b> kirishni deterministik niqobga ko‘paytiradi: $x\\cdot\\mathbb 1[x&gt;0]$. <b>Dropout</b> kirishni undan bog‘liq bo‘lmagan tasodifiy niqobga ko‘paytiradi. Agar niqob tasodifiy bo‘lsa-yu, lekin kirishga <i>bog‘liq</i> bo‘lsa-chi: $x$ qancha katta bo‘lsa, uni o‘tkazish ehtimoli shuncha yuqori?"),
        ("eq", r"m\sim\operatorname{Bernoulli}\bigl(\Phi(x)\bigr),\qquad \mathbb E\,[\,x\cdot m\,]=x\cdot P(m=1)=x\,\Phi(x)=\operatorname{GELU}(x)"),
        ("p", "Bunday niqobni olish oson: $\\varepsilon\\sim N(0,1)$ shovqin oling va $\\varepsilon\\le x$ bo‘lsa, $m=1$ deb oling. U holda taqsimot funksiyasi ta’rifiga ko‘ra $P(m=1)=\\Phi(x)$. Nega normal qonun? Normallashtirishlardan (BatchNorm, LayerNorm) keyin neyron kirishlari taxminan $N(0,1)$ kabi taqsimlangan, $\\Phi(x)$ esa tabiiy savolga javob beradi: odatiy kirishlarning qancha ulushi berilgan $x$ dan kichik."),
        ("viz", "gelu-mask", {"x": 0.5, "seed": 3}, "<b>2-rasm.</b> Chapda to‘q sariq nuqtalar — $-3$ dan $3$ gacha 25 nuqtada $n$ ta tasodifiy niqob bo‘yicha $x\\cdot m$ o‘rtachasi, o‘ngda — $\\varepsilon$ shovqin va niqob ochiq bo‘ladigan $\\Phi(x_0)$ ulush. «Boshlash»ni bosing: $n=20$ da GELU’dan eng katta chetlanish $0{,}146$, $n=2000$ da esa $0{,}0125$; o‘rtacha xatosi $1/\\sqrt n$ kabi kamayadi. $x_0=0{,}5$ nuqtada ochiq niqoblar ulushi $\\Phi(0{,}5)\\approx0{,}691$ ga yaqinlashadi."),
        ("callout", "note", "GELU’ning o‘zi tasodifiy emas", "Shovqinli niqob faqat shaklni tushuntiradi. Tarmoqda deterministik o‘rtacha $x\\Phi(x)$ turadi: o‘qitishda ham, xulosa chiqarishda ham tasodif yo‘q (shovqin kerak bo‘lsa, alohida dropout qo‘shiladi)."),
    ]),
    dict(id="properties", title="Xossalar va shakl", blocks=[
        ("ul", [
            "<b>Qiymatlar sohasi</b> — $[-0{,}170;\\,+\\infty)$: pastdan chegaralangan, yuqoridan yo‘q.",
            "<b>Silliqlik</b>: GELU cheksiz differensiallanuvchi; $\\operatorname{GELU}(0)=0$, $\\operatorname{GELU}'(0)=\\tfrac12$.",
            "<b>Monoton emaslik</b>: funksiya $(-\\infty;\\,-0{,}752)$ da kamayadi, o‘ngda o‘sadi; minimum $\\approx-0{,}170$.",
            "<b>Asimptotalar</b>: $x\\to+\\infty$ da $\\operatorname{GELU}(x)-x\\to0$, $x\\to-\\infty$ da $\\operatorname{GELU}(x)\\to0$, chap dum esa gaussiana kabi so‘nadi: $x\\Phi(x)\\approx-\\varphi(x)$, allaqachon $\\operatorname{GELU}(-4)\\approx-1{,}3\\cdot10^{-4}$.",
            "<b>Ayniyat</b>: $\\operatorname{GELU}(x)-\\operatorname{GELU}(-x)=x$, chunki $\\Phi(x)+\\Phi(-x)=1$.",
            "<b>Qavariqlik</b>: faqat $[-\\sqrt2;\\,\\sqrt2]$ kesmada; undan tashqarida funksiya botiq (ikkinchi hosila ishorasi — keyingi bo‘limda).",
        ]),
        ("h3", "GELU = ReLU minus juft «chuqurcha»"),
        ("p", "Ayniyatdan qulay yozuv kelib chiqadi. $x&gt;0$ uchun: $x\\Phi(x)=x-x\\Phi(-x)$; $x&lt;0$ uchun: $x\\Phi(x)=-|x|\\Phi(-|x|)$. Ikkala holda ham"),
        ("eq", r"\operatorname{GELU}(x)=\operatorname{ReLU}(x)-|x|\,\Phi(-|x|)"),
        ("p", "$|x|\\Phi(-|x|)$ tuzatma juft: noldan chapda ham, o‘ngda ham bir xil, $|x|=0{,}752$ da $0{,}170$ maksimumga erishadi va tez so‘nadi. <a href=\"../silu/\">SiLU</a> $x\\,\\sigma(x)$ ham shu xossaga ega, faqat uning «chuqurchasi» kengroq va chuqurroq: $|x|=1{,}278$ da $0{,}278$."),
        ("viz", "gelu-family", {"x": -1}, "<b>3-rasm.</b> Yuqorida — GELU, SiLU va ReLU, pastda — $\\operatorname{ReLU}-f$ ayirmalar. Kursorni istalgan grafik ustiga olib boring. $x=-1$ da: $\\operatorname{GELU}=-0{,}159$, $\\operatorname{SiLU}=-0{,}269$. Pastki grafikdagi nuqtalar — ReLU’dan eng katta farqlar: GELU’da $0{,}170$, SiLU’da $0{,}278$; bular ularning minimumlari chuqurligi hamdir."),
        ("callout", "note", "Sigmoida bilan bog‘lanish", "Normal va logistik qonunlarning taqsimot funksiyalari juda o‘xshash: $\\Phi(x)\\approx\\sigma(1{,}702\\,x)$, xato $0{,}0095$ dan oshmaydi. Shuning uchun GELU $x\\,\\sigma(1{,}702x)$ bilan deyarli ustma-ust tushadi — bu cho‘zilgan sigmoidali SiLU. $\\sigma$ ning o‘zi haqida — <a href=\"../sigmoid/\">sigmoida</a> sahifasida."),
    ]),
    dict(id="derivative", title="Hosila: Φ(x) + x·φ(x)", blocks=[
        ("p", "Hosila xatoni teskari tarqatishda kerak. Uni keltirib chiqaramiz va funksiya minimumini topamiz."),
        ("deep", "Birinchi va ikkinchi hosilani keltirib chiqarish", [
            ("p", "Asosiy fakt: taqsimot funksiyasining hosilasi — zichlik, $\\Phi'(x)=\\varphi(x)$ (yuqori chegarasi o‘zgaruvchi bo‘lgan integral uchun analizning asosiy teoremasi). Ko‘paytma hosilasi qoidasiga ko‘ra:"),
            ("eq", r"\operatorname{GELU}'(x)=(x)'\cdot\Phi(x)+x\cdot\Phi'(x)=\Phi(x)+x\,\varphi(x)"),
            ("p", "Gaussiana uchun $\\varphi'(x)=-x\\,\\varphi(x)$. Yana bir marta differensiallaymiz:"),
            ("eq", r"\operatorname{GELU}''(x)=\varphi(x)+\varphi(x)+x\cdot\bigl(-x\,\varphi(x)\bigr)=\varphi(x)\,\bigl(2-x^{2}\bigr)"),
            ("p", "$\\operatorname{GELU}''$ ishorasi $2-x^2$ ishorasi bilan bir xil: funksiya $(-\\sqrt2;\\,\\sqrt2)$ da qavariq va undan tashqarida botiq, $\\operatorname{GELU}'$ hosilaning ekstremumlari esa $x=\\pm\\sqrt2$ nuqtalarda."),
        ]),
        ("eq", r"\operatorname{GELU}'(x)=\underbrace{\Phi(x)}_{\text{ulush}}+\underbrace{x\,\varphi(x)}_{\text{ulush o‘zgarishi}}"),
        ("p", "Hosila ikki qo‘shiluvchidan iborat. Birinchisi — $\\Phi(x)$ ulushning o‘zi: ventil $x$ ga bog‘liq bo‘lmaganida hosila shunday bo‘lardi. Ikkinchisi — $x$ o‘sganda ventil ochilishidan keladigan tuzatma; u noldan o‘ngda musbat, chapda manfiy. Hosilasi 0/1 zinapoya bo‘lgan ReLU bilan solishtiring."),
        ("viz", "gelu-derivative", {"x": -0.75}, "<b>4-rasm.</b> GELU hosilasi (to‘q sariq) va uning ikki qo‘shiluvchisi. Eng katta qiymat $\\Phi(\\sqrt2)+\\sqrt2\\,\\varphi(\\sqrt2)\\approx1{,}129$, eng kichigi $x=-\\sqrt2$ da $\\approx-0{,}129$ — bu sonlar yig‘indisi 1 ga teng, chunki $\\operatorname{GELU}'(x)+\\operatorname{GELU}'(-x)=1$. Hosila $x\\approx-0{,}752$ da nolga aylanadi; boshlang‘ich $x=-0{,}75$ nuqtada u allaqachon deyarli nol. Ikkinchi hosilani yoqing: uning nollari $\\pm\\sqrt2$ da."),
        ("h3", "Minimum qayerda"),
        ("p", "Minimum $\\operatorname{GELU}'(x)=0$ bo‘lgan joyda, ya’ni $\\Phi(x)=-x\\,\\varphi(x)$. Bu tenglama elementar funksiyalarda yechilmaydi; $x_0=-1$ dan boshlangan Nyuton usuli $x_{k+1}=x_k-\\operatorname{GELU}'(x_k)/\\operatorname{GELU}''(x_k)$ $-0{,}6557$, $-0{,}7448$, $-0{,}75175$, $-0{,}751792$ ni beradi — har bir iteratsiya to‘g‘ri raqamlar sonini taxminan ikki barobar oshiradi."),
        ("eq", r"x^{*}\approx-0{,}7518,\qquad \operatorname{GELU}(x^{*})=x^{*}\Phi(x^{*})=-(x^{*})^{2}\varphi(x^{*})\approx-0{,}1700"),
        ("p", "Ikkinchi tenglik $\\Phi(x^*)=-x^*\\varphi(x^*)$ minimum shartidan kelib chiqadi. Minimumda $\\Phi(x^*)\\approx0{,}226$ ulush o‘tadi."),
        ("callout", "intuition", "Chapdagi manfiy gradiyent", "$x&lt;-0{,}752$ da hosila manfiy: kirish oshirilsa, chiqish <i>kamayadi</i>. ReLU bu zonada aynan nol beradi, GELU esa kichik, lekin noldan farqli signal beradi ($-0{,}129$ dan kichik emas). U gaussiana kabi so‘nadi: $\\operatorname{GELU}'(-3)\\approx-0{,}012$, $\\operatorname{GELU}'(-4)\\approx-0{,}0005$."),
    ]),
    dict(id="approx", title="Tez yaqinlashishlar: tanh va sigmoida", blocks=[
        ("p", "2016 yilda erf funksiyasi freymvorklarda sekin ishlardi yoki umuman yo‘q edi, shuning uchun mualliflar ikki yaqinlashishni taklif qildi. Birinchisi tanh’dan foydalanadi:"),
        ("eq", r"\operatorname{GELU}(x)\approx\frac{x}{2}\Bigl(1+\tanh\Bigl[\sqrt{2/\pi}\,\bigl(x+0{,}044715\,x^{3}\bigr)\Bigr]\Bigr)"),
        ("p", "BERT va GPT-2 ning asl kodida aynan shu formula yozilgan (Hugging Face kutubxonasida u <code>gelu_new</code>, PyTorch’da — <code>approximate=\"tanh\"</code> deb ataladi). Eng katta xato — $|x|\\approx2{,}70$ da $4{,}7\\cdot10^{-4}$. Ikkinchi yaqinlashish sigmoida orqali:"),
        ("eq", r"\operatorname{GELU}(x)\approx x\,\sigma(1{,}702\,x)"),
        ("p", "U qo‘polroq: $|x|\\approx2{,}27$ da xato $0{,}020$ gacha yetadi. Ikkala xato ham juft funksiyalar, chunki uchala formula ham $f(x)-f(-x)=x$ ayniyatini qanoatlantiradi."),
        ("deep", "√(2/π) va 0,044715 qayerdan keladi", [
            ("p", "$\\operatorname{erf}(z)$ ni $\\tanh(u)$ funksiya bilan yaqinlashtirish kerak. Ikkalasini nol atrofida yoyamiz: $\\operatorname{erf}(z)=\\frac{2}{\\sqrt\\pi}\\bigl(z-\\frac{z^3}{3}+\\dots\\bigr)$ va $\\tanh u=u-\\frac{u^3}{3}+\\dots$. $u=\\frac{2}{\\sqrt\\pi}(z+cz^3)$ ni olamiz va koeffitsiyentlarni tenglashtiramiz."),
            ("eq", r"z^{1}:\ \ \frac{2}{\sqrt\pi}=\frac{2}{\sqrt\pi};\qquad z^{3}:\ \ \frac{2c}{\sqrt\pi}-\frac{8}{3\pi\sqrt\pi}=-\frac{2}{3\sqrt\pi}\ \Longrightarrow\ c=\frac{4}{3\pi}-\frac13"),
            ("p", "$z=x/\\sqrt2$ ni qo‘yib, $c'=c/2=\\frac{2}{3\\pi}-\\frac16\\approx0{,}0455$ bilan $\\sqrt{2/\\pi}\\,(x+c'x^3)$ ni olamiz. Qatorlarning mos kelishi faqat nol atrofida aniqlik beradi, shuning uchun mualliflar koeffitsiyentni butun o‘q bo‘yicha sonli tanladi: $0{,}044715$. Teylor qiymati $0{,}0455$ bilan maksimal xato $7{,}5\\cdot10^{-4}$, $0{,}044715$ bilan — $4{,}7\\cdot10^{-4}$, kub hadsiz ($c'=0$) esa — $0{,}034$."),
        ]),
        ("viz", "gelu-approx", {"c": 0.044715, "x": 1}, "<b>5-rasm.</b> Yuqorida — aniq GELU va ikki yaqinlashish, pastda — logarifmik shkaladagi xato moduli (botiqlar — xato ishorasini o‘zgartiradigan nuqtalar). $c$ koeffitsiyentni suring: $c=0{,}044715$ da maksimal xato $4{,}7\\cdot10^{-4}$, $c=0$ da — $0{,}034$. $x=1$ da: aniq qiymat $0{,}8413$, tanh yaqinlashishi $0{,}8412$, sigmoidali $0{,}8458$."),
        ("callout", "warn", "Bular turli funksiyalar", "tanh yaqinlashishi bilan o‘qitilgan model xulosa chiqarishda ham aynan undan foydalanishi kerak. Farq har bir neyronda $4{,}7\\cdot10^{-4}$ dan oshmaydi, lekin yuzlab qatlam va minglab neyronlarda vaznlarni konvertatsiya qilishda logitlarning sezilarli farqini beradi va bitma-bit testlarni buzadi."),
    ]),
    dict(id="space", title="3D’da x·Φ(x/s) oilasi: ReLU’dan to‘g‘ri chiziqqacha", blocks=[
        ("p", "Niqobdagi shovqin birlik bo‘lishi shart emas. Agar $\\varepsilon\\sim N(0,s^2)$ bo‘lsa, $P(\\varepsilon\\le x)=\\Phi(x/s)$ bo‘ladi va $s$ «harorat»li butun funksiyalar oilasi hosil bo‘ladi:"),
        ("eq", r"f(x,s)=x\,\Phi\Bigl(\frac{x}{s}\Bigr)=s\cdot\operatorname{GELU}\Bigl(\frac{x}{s}\Bigr)"),
        ("ul", [
            "$s\\to0$: shovqin yo‘q, $\\Phi(x/s)$ zinapoyaga aylanadi va $f\\to\\operatorname{ReLU}(x)$;",
            "$s=1$: oddiy GELU;",
            "$s\\to\\infty$: shovqin kirishni bosib ketadi, $\\Phi(x/s)\\to\\tfrac12$ va $f\\to x/2$ — to‘g‘ri chiziq, nochiziqlilik yo‘qoladi.",
        ]),
        ("p", "Ikkinchi tenglik oilaning barcha a’zolari o‘xshash ekanini ko‘rsatadi: minimum $x=-0{,}752\\,s$ nuqtada va $-0{,}170\\,s$ ga teng. Sirtda bu «jarlik» tubi bo‘ylab o‘tgan to‘g‘ri moviy-yashil chiziq."),
        ("viz", "gelu-surface", {"s": 1}, "<b>6-rasm.</b> $f(x,s)=x\\,\\Phi(x/s)$ sirti (uni aylantirish mumkin) va joriy $s$ dagi kesim. To‘q sariq chiziq — kesim, moviy-yashil — minimumlar chizig‘i. $s=1$ da $x=-0{,}752$ dagi minimum $-0{,}170$ ga teng. Hosilaga o‘ting: kichik $s$ da u ReLU zinapoyasiga aylanadi, katta $s$ da $\\tfrac12$ ga yaqinlashadi."),
        ("p", "Tarmoqda GELU vektorga elementma-element qo‘llaniladi: $h=\\operatorname{GELU}(W_1x+b_1)$. Har bir koordinata — $w_j^\\top x+b_j=0$ giperteksislik bo‘ylab o‘z «burmasi», lekin ReLU’dan farqli ravishda burma silliq va sinishdan oldin kichik manfiy botiqqa ega."),
    ]),
    dict(id="training", title="O‘qitishda va transformerda GELU", blocks=[
        ("p", "Bitta yashirin qatlamli tarmoq javobni $w_{2j}\\,f(w_{1j}x+b_{1j})$ «g‘ishtlar» yig‘indisi sifatida quradi. ReLU’da har bir g‘isht — bitta sinishli siniq chiziq, yig‘indi ham siniq chiziq. GELU’da g‘ishtlar silliq, shuning uchun silliq bog‘lanishni ularning kamroq soni bilan tasvirlash mumkin."),
        ("viz", "gelu-train", {"h": 4}, "<b>7-rasm.</b> Bir xil boshlang‘ich qiymatli 4 neyronli o‘sha tarmoq, $\\sin1{,}5x+0{,}3x$ shovqinli egri chiziqning 40 nuqtasida $0{,}03$ qadamli Adam bilan o‘qitiladi. O‘ngda — logarifmik shkaladagi o‘rtacha kvadratik xato (MSE). 2000 qadamda GELU’li tarmoq MSE’ni $7{,}06$ dan $0{,}0042$ gacha tushiradi — bu ma’lumotlardagi shovqin darajasi ($0{,}0051$), ReLU’li tarmoq esa $0{,}0083$ da qotib qoladi: to‘rtta sinish yetmaydi. «Neyronlar» tugmalari alohida g‘ishtlarni ko‘rsatadi."),
        ("p", "O‘qitish o‘sha hosiladan foydalanadi: neyronga kelgan gradiyent $\\operatorname{GELU}'(z)=\\Phi(z)+z\\varphi(z)$ ga ko‘paytiriladi. ReLU’dan farqli ravishda manfiy $z$ li neyron signal olishda davom etadi, shuning uchun GELU’li tarmoqlar «o‘lik» neyronlardan kamroq aziyat chekadi."),
        ("h3", "Transformerning to‘g‘ri tarqalish bloki"),
        ("p", "BERT va GPT’da har bir diqqat (attention) qatlamidan keyin har bir tokenni alohida qayta ishlaydigan ikki qatlamli perseptron turadi:"),
        ("eq", r"\operatorname{FFN}(h)=W_2\,\operatorname{GELU}(W_1h+b_1)+b_2,\qquad W_1\in\mathbb R^{4d\times d},\ \ W_2\in\mathbb R^{d\times4d}"),
        ("p", "BERT-base’da $d=768$, ya’ni 12 qatlamning har birida har bir tokenga $4d=3072$ ta GELU hisoblash to‘g‘ri keladi. FFN oldida LayerNorm turadi, shuning uchun o‘qitish boshida $W_1h+b_1$ kirishlar birlik tartibida — GELU’da ham «chuqurcha», ham silliq o‘tish bo‘lgan aynan o‘sha soha. Shuning uchun aktivatsiyaning o‘z tezligi muhim va aniq erf o‘rniga ko‘pincha tanh yaqinlashishi olinadi."),
        ("callout", "history", "GELU qanday standartga aylandi", "Xendriks va Gimpel GELU’ni 2016 yilda taklif qildi va ko‘rish, nutq hamda matn vazifalarida u ReLU va ELU’dan yomon emasligini ko‘rsatdi. Unga keng shuhrat GPT (2018) va BERT (2018), keyin GPT-2, GPT-3 va Vision Transformer (2020) olib keldi. 2020 yilda Shazir GeGLU va SwiGLU ventilli variantlari yanada yaxshi ekanini ko‘rsatdi va yangi LLM’lar ko‘pincha ulardan foydalanadi."),
    ]),
    dict(id="code", title="Kodda: aniq, tez va barqaror", blocks=[
        ("p", "NumPy’da erf funksiyasi yo‘q, shuning uchun uni SciPy’dan olishadi. Katta manfiy $x$ da aniqlikni yo‘qotmaslik uchun taqsimot funksiyasini qo‘shimcha xatolar funksiyasi orqali hisoblash qulay: $\\Phi(x)=\\tfrac12\\operatorname{erfc}(-x/\\sqrt2)$. $\\tfrac12(1+\\operatorname{erf})$ formulasi $x=-10$ da deyarli teng sonlarni ayiradi va aynan 0 beradi, holbuki haqiqiy qiymat $\\operatorname{GELU}(-10)\\approx-7{,}6\\cdot10^{-23}$; aktivatsiyaning o‘zi uchun bu muhim emas, lekin o‘sha $\\Phi$ boshqa formulalarda ham tez-tez kerak bo‘ladi."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Qoida", "GELU variantini vaznlar o‘qitilgandagidek tanlang: <code>nn.GELU()</code> — aniq, <code>nn.GELU(approximate=\"tanh\")</code> — taqribiy. Yangi model uchun sifatda deyarli farq yo‘q; tanh varianti eski uskunada tezroq bo‘lishi mumkin."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b>GELU chiqishini ReLU’dagidek manfiy emas deb hisoblash.</b> U $-0{,}170$ gacha tushishi mumkin; keyin logarifm, ildiz yoki bo‘lish kelsa, buni hisobga olish kerak.",
            "<b>O‘qitish va xulosa chiqarish orasida yoki modelni konvertatsiya qilishda (ONNX, TensorRT, boshqa freymvork) aniq GELU va tanh yaqinlashishini aralashtirish.</b> Xato kichik, lekin qatlamlar bo‘yicha to‘planadi.",
            "<b>$x\\,\\sigma(1{,}702x)$ ni GELU bilan adashtirish.</b> Bu xatosi $0{,}02$ gacha bo‘lgan tez yaqinlashish, aslida $\\beta=1{,}702$ parametrli <a href=\"../silu/\">SiLU</a>.",
            "<b>GELU gradiyent so‘nishidan to‘liq xalos qiladi deb o‘ylash.</b> $x\\to-\\infty$ da hosila gaussiana kabi so‘nadi: allaqachon $\\operatorname{GELU}'(-4)\\approx-0{,}0005$. Kirishlarni normallashtirish baribir kerak.",
            "<b>$\\Phi$ ni $\\sqrt2$ ga bo‘lishni unutib, $\\tfrac12(1+\\operatorname{erf}(x))$ deb yozish.</b> Bu $N(0,\\tfrac12)$ taqsimot funksiyasi bo‘ladi, ya’ni $x\\Phi(\\sqrt2x)$ — boshqa egri chiziq.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘lanish", blocks=[
        ("ul", [
            "<a href=\"../relu/\">ReLU</a>: $s\\to0$ da $x\\,\\Phi(x/s)$ ning limiti va GELU’ning «skeleti»: $\\operatorname{GELU}=\\operatorname{ReLU}-|x|\\Phi(-|x|)$.",
            "<a href=\"../silu/\">SiLU / Swish</a>: «kirish × yumshoq ventil» sxemasi, faqat $\\Phi$ o‘rnida sigmoida; $x\\,\\sigma(1{,}702x)\\approx\\operatorname{GELU}(x)$.",
            "<a href=\"../sigmoid/\">Sigmoida</a>: $\\sigma(1{,}702x)$ $\\Phi(x)$ ni $0{,}0095$ dan oshmaydigan xato bilan yaqinlashtiradi — logit va probit modellari bog‘lanishi.",
            "<a href=\"../tanh/\">tanh</a>: GELU’ning eng mashhur yaqinlashishi asosi.",
            "<a href=\"../leaky-relu/\">Leaky ReLU</a>: $x&lt;0$ da signalni o‘tkazishning boshqa usuli — silliq «chuqurcha» o‘rniga doimiy kichik qiyalik.",
            "<a href=\"../adam/\">Adam</a> va <a href=\"../mse/\">MSE</a>: 7-rasmdagi simulyatsiyaning optimizatori va yo‘qotishi.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $\\operatorname{GELU}(x)=x\\,\\Phi(x)$: $\\varepsilon\\sim N(0,1)$ uchun $P(\\varepsilon\\le x)$ ehtimollikka ko‘paytirilgan kirish; bu kirishga bog‘liq tasodifiy niqobning o‘rtachasi. 2) $\\operatorname{GELU}=\\operatorname{ReLU}-|x|\\Phi(-|x|)$: $x=-0{,}752$ da $-0{,}170$ minimumli silliq ReLU. 3) $\\operatorname{GELU}'=\\Phi+x\\varphi\\in(-0{,}129;\\,1{,}129)$, $\\operatorname{GELU}''=\\varphi\\,(2-x^2)$. 4) $0{,}044715$ koeffitsiyentli tanh yaqinlashishi ko‘pi bilan $4{,}7\\cdot10^{-4}$ ga xato qiladi, lekin bu boshqa funksiya. 5) $x\\,\\Phi(x/s)$ ReLU ($s\\to0$) va $x/2$ ($s\\to\\infty$) ni bog‘laydi. 6) BERT, GPT va ViT’ning FFN bloklarida turadi."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="$\\operatorname{GELU}(-1)$ taxminan nimaga teng?", options=["$-1$", "$-0{,}159$", "$0$", "$0{,}841$"], answer=1,
                 explain="$\\operatorname{GELU}(-1)=-1\\cdot\\Phi(-1)=-0{,}159$: manfiy kirishning faqat 15,9% i o‘tadi."),
            dict(q="GELU’ning noldagi hosilasi nimaga teng?", options=["$0$", "$0{,}25$", "$0{,}5$", "$1$"], answer=2,
                 explain="$\\operatorname{GELU}'(0)=\\Phi(0)+0\\cdot\\varphi(0)=\\tfrac12$."),
            dict(q="GELU minimumi qayerda?", options=["Nolda, qiymati 0", "$x\\approx-0{,}75$ da, qiymati $\\approx-0{,}17$", "$x=-1$ da, qiymati $-0{,}159$", "Minimum yo‘q"], answer=1,
                 explain="Minimum $\\Phi(x)+x\\varphi(x)=0$ bo‘lgan joyda: $x^*\\approx-0{,}752$, $\\operatorname{GELU}(x^*)\\approx-0{,}170$. $x=-1$ nuqta chaproqda, kamayuvchi tarmoqda yotadi."),
            dict(q="GELU formulasida $\\Phi(x)$ nimani anglatadi?", options=["$x$ nuqtadagi normal zichlik", "$\\varepsilon\\sim N(0,1)$ ning $x$ dan katta bo‘lmaslik ehtimolligi — kirish o‘tkaziladigan ulush", "$x$ ning sigmoidasi", "Kirishlar dispersiyasi"], answer=1,
                 explain="$\\Phi$ — taqsimot funksiyasi: $\\Phi(x)=P(\\varepsilon\\le x)$. GELU — $m=\\mathbb 1[\\varepsilon\\le x]$ niqob uchun $x\\cdot m$ ning o‘rtachasi."),
            dict(q="$\\operatorname{GELU}(3)-\\operatorname{GELU}(-3)$ nimaga teng?", options=["$0$", "$2{,}996$", "$3$", "$6$"], answer=2,
                 explain="$x\\Phi(x)-(-x)\\Phi(-x)=x\\bigl(\\Phi(x)+\\Phi(-x)\\bigr)=x$, shuning uchun ayirma aynan 3 ga teng."),
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
