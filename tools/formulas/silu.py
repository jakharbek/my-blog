"""Formula page: SiLU / Swish (x·σ(x)) and SwiGLU. Format: see README.md, reference page: sigmoid.py."""

META = dict(
    id="silu",
    date="2026-10-28",
    minutes=35,
    hero=r"\operatorname{SiLU}(x)=x\cdot\sigma(x)=\frac{x}{1+e^{-x}}",
    title={"ru": "SiLU / Swish: вход, который сам себя пропускает", "en": "SiLU / Swish: an input that gates itself", "uz": "SiLU / Swish: o‘zini o‘zi o‘tkazadigan kirish"},
    dek={
        "ru": "Активация современных языковых моделей: вход умножается на сигмоиду от самого себя. Разбираем по косточкам, почему у неё есть минимум −0,278 и производная больше единицы, как она связана с ReLU и GELU, откуда берётся семейство Swish-β и как SiLU работает внутри блока SwiGLU в LLaMA и Qwen.",
        "en": "The activation of modern language models: the input is multiplied by the sigmoid of itself. We take it apart bone by bone: why it has a minimum of −0.278 and a derivative above one, how it relates to ReLU and GELU, where the Swish-β family comes from, and how SiLU works inside the SwiGLU block of LLaMA and Qwen.",
        "uz": "Zamonaviy til modellarining aktivatsiyasi: kirish o‘zining sigmoidasiga ko‘paytiriladi. Mayda detallarigacha tahlil qilamiz: nega uning −0,278 minimumi va birdan katta hosilasi bor, u ReLU va GELU bilan qanday bog‘liq, Swish-β oilasi qayerdan keladi va SiLU LLaMA va Qwen’dagi SwiGLU bloki ichida qanday ishlaydi.",
    },
    description={
        "ru": "SiLU (Swish) подробно: самовентиль x·σ(x), минимум через W-функцию Ламберта, производная и её выброс выше 1, Swish-β, сравнение с ReLU и GELU, вероятностный смысл, SwiGLU в 3D, обучение, код на NumPy и PyTorch.",
        "en": "SiLU (Swish) in depth: the self-gate x·σ(x), the minimum via the Lambert W function, the derivative and its overshoot above 1, Swish-β, comparison with ReLU and GELU, the probabilistic meaning, SwiGLU in 3D, training, code in NumPy and PyTorch.",
        "uz": "SiLU (Swish) batafsil: x·σ(x) o‘z-o‘zini ventillash, Lambert W funksiyasi orqali minimum, hosila va uning 1 dan yuqori chiqishi, Swish-β, ReLU va GELU bilan taqqoslash, ehtimollik ma’nosi, 3D’da SwiGLU, o‘qitish, NumPy va PyTorch’da kod.",
    },
)

# x, σ(x), SiLU(x), SiLU'(x)
TABLE = [("-5", "0.0067", "-0.0335", "-0.0265"), ("-3", "0.0474", "-0.1423", "-0.0881"), ("-1.2785", "0.2178", "-0.2785", "0.0000"),
         ("-1", "0.2689", "-0.2689", "0.0723"), ("0", "0.5000", "0.0000", "0.5000"), ("1", "0.7311", "0.7311", "0.9277"),
         ("2", "0.8808", "1.7616", "1.0908"), ("3", "0.9526", "2.8577", "1.0881"), ("5", "0.9933", "4.9665", "1.0265")]


def _table(lang):
    dec = "." if lang == "en" else ","
    m = lambda v: v.replace("-", "−").replace(".", dec)
    return [[m(c) for c in row] for row in TABLE]


CODE_NUMPY = '''import numpy as np

def sigmoid(x):
    # σ(x) = (1 + tanh(x/2)) / 2 — без переполнения при любом x
    return 0.5 * (1.0 + np.tanh(0.5 * x))

def silu(x):
    return x * sigmoid(x)

def silu_grad(x):
    s = sigmoid(x)
    return s * (1.0 + x * (1.0 - s))      # = SiLU(x) + σ(x)·(1 − SiLU(x))

def swish(x, beta=1.0):
    return x * sigmoid(beta * x)

x = np.array([-1000.0, -1.0, 0.0, 1.0, 2.3994])
print(silu(x))        # [-0.     -0.2689  0.      0.7311  2.1997]
print(silu_grad(x))   # [-0.      0.0723  0.5     0.9277  1.0998]'''

CODE_TORCH = '''import torch
import torch.nn as nn
import torch.nn.functional as F

z = torch.tensor([-2.0, 0.0, 2.0], requires_grad=True)
y = F.silu(z)                    # tensor([-0.2384, 0.0000, 1.7616])
y.sum().backward()
print(z.grad)                    # tensor([-0.0908, 0.5000, 1.0908])

class SwiGLU(nn.Module):
    """FFN-блок LLaMA и Qwen: W2 · (SiLU(W1 x) ⊙ W3 x)."""
    def __init__(self, d, hidden):
        super().__init__()
        self.w1 = nn.Linear(d, hidden, bias=False)   # ветка вентиля
        self.w3 = nn.Linear(d, hidden, bias=False)   # ветка значения
        self.w2 = nn.Linear(hidden, d, bias=False)   # обратно в размер d
    def forward(self, x):
        return self.w2(F.silu(self.w1(x)) * self.w3(x))

ffn = SwiGLU(4096, 11008)                          # размеры LLaMA-7B
print(sum(p.numel() for p in ffn.parameters()))   # 135266304'''

_CODE_TR = {
    "en": [("без переполнения при любом x", "no overflow for any x"), ("FFN-блок LLaMA и Qwen", "The FFN block of LLaMA and Qwen"),
           ("ветка вентиля", "gate branch"), ("ветка значения", "value branch"), ("обратно в размер d", "back to size d"),
           ("размеры LLaMA-7B", "the sizes of LLaMA-7B")],
    "uz": [("без переполнения при любом x", "istalgan x da to‘lib ketishsiz"), ("FFN-блок LLaMA и Qwen", "LLaMA va Qwen’ning FFN bloki"),
           ("ветка вентиля", "ventil tarmog‘i"), ("ветка значения", "qiymat tarmog‘i"), ("обратно в размер d", "d o‘lchamga qaytarish"),
           ("размеры LLaMA-7B", "LLaMA-7B o‘lchamlari")],
}


def _code(src, lang):
    for a, b in _CODE_TR.get(lang, []):
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", "У <a href=\"../relu/\">ReLU</a> два недостатка: в нуле у неё излом, а слева она выбрасывает весь сигнал вместе с градиентом. SiLU (Sigmoid Linear Unit) устроена иначе: вход $x$ умножается на <a href=\"../sigmoid/\">сигмоиду</a> от самого себя. Большой положительный вход проходит почти целиком, большой отрицательный почти полностью гасится, а около нуля пропускается «частично» — плавно, без изломов."),
        ("p", "Ту же функцию с параметром, $x\\,\\sigma(\\beta x)$, называют Swish. При $\\beta=1$ это ровно SiLU; в PyTorch и других библиотеках так и пишут: <code>nn.SiLU</code>."),
        ("p", "Где она встречается:"),
        ("ul", [
            "<b>большие языковые модели</b> — LLaMA, Qwen, Mistral и PaLM используют SiLU внутри блока SwiGLU (раздел 7); в конфигурациях моделей это строка <code>hidden_act = \"silu\"</code>;",
            "<b>компьютерное зрение</b> — EfficientNet (2019) построен на Swish, детекторы семейства YOLO начиная с YOLOv5 — на SiLU;",
            "<b>мобильные сети</b> — MobileNetV3 использует «жёсткий» Swish, дешёвое кусочно-полиномиальное приближение $x\\cdot\\operatorname{ReLU6}(x+3)/6$;",
            "<b>обучение с подкреплением</b> — Элфвинг, Утибе и Дойя (2017) применили её для аппроксимации функций ценности под именем SiLU.",
        ]),
        ("callout", "key", "Главное за минуту", "$\\operatorname{SiLU}(x)=x\\,\\sigma(x)$. Далеко справа она почти равна $x$, далеко слева — почти 0, как ReLU, но гладкая. Она немонотонна: минимум $\\approx-0{,}278$ в точке $x\\approx-1{,}278$. Производная $\\sigma(x)\\bigl(1+x(1-\\sigma(x))\\bigr)$ равна $0{,}5$ в нуле и превышает 1 при $x&gt;1{,}278$ (максимум $\\approx1{,}100$). В LLM SiLU работает вентилем в SwiGLU: $\\operatorname{SiLU}(W_1x)\\odot W_3x$."),
    ]),
    dict(id="intuition", title="Интуиция: вход сам решает, сколько себя пропустить", blocks=[
        ("p", "Представьте кран, ручку которого крутит сам поток. Сигмоида $\\sigma(x)$ — это степень открытия крана, от 0 до 1. Если вход большой и положительный, кран открыт почти полностью ($\\sigma\\approx1$) и выход почти равен входу. Если вход сильно отрицательный, кран почти закрыт, и выход близок к нулю. Такой механизм называют <b>самовентилем</b> (self-gating): вход одновременно и сигнал, и решение о том, сколько сигнала пропустить."),
        ("p", "Потяните синюю точку. Бирюзовая кривая — вентиль $\\sigma(x)$, синяя — произведение $x\\cdot\\sigma(x)$. Обратите внимание на область около $x=-1$: вентиль уже прикрыт, но не до конца, а вход отрицательный — и выход проваливается ниже нуля."),
        ("viz", "silu-explorer", {"x": -1}, "<b>Рисунок 1.</b> SiLU как произведение сигнала и вентиля. При $x=-1$ вентиль открыт на $\\sigma(-1)=0{,}2689$, и выход равен $-1\\cdot0{,}2689=-0{,}2689$. Кружок отмечает минимум $(-1{,}278;\\,-0{,}278)$. Серый пунктир — ReLU, точечная линия — $y=x$."),
        ("callout", "intuition", "Что заметить", "Справа синяя кривая прижимается к прямой $y=x$, слева — к нулю: в этих областях SiLU почти не отличается от ReLU. Вся разница сосредоточена в полосе примерно $-5&lt;x&lt;5$, где вентиль открыт частично. Именно там ReLU делает резкий излом, а SiLU — плавный изгиб с небольшой «ямкой» слева."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", "Соберём SiLU из двух знакомых деталей и посмотрим на неё в нескольких записях."),
        ("eq", r"\operatorname{SiLU}(x)=\underbrace{x}_{\text{сигнал}}\cdot\underbrace{\sigma(x)}_{\text{вентиль}}=\frac{x}{1+e^{-x}}"),
        ("symbols", [
            (r"x", "вход нейрона (пре-активация); он же — сигнал, который нужно пропустить;"),
            (r"\sigma(x)=\frac{1}{1+e^{-x}}", "<a href=\"../sigmoid/\">сигмоида</a>, число из $(0;\\,1)$ — доля сигнала, которая пройдёт;"),
            (r"x\cdot\sigma(x)", "результат: при $\\sigma\\approx1$ выход $\\approx x$, при $\\sigma\\approx0$ выход $\\approx0$."),
        ]),
        ("p", "Через гиперболический тангенс ($\\sigma(x)=\\tfrac12(1+\\tanh\\tfrac x2)$) получается запись, которая многое объясняет:"),
        ("eq", r"\operatorname{SiLU}(x)=\frac{x}{2}\Bigl(1+\tanh\frac{x}{2}\Bigr)=\underbrace{\frac{x}{2}}_{\text{нечётная часть}}+\underbrace{\frac{x}{2}\tanh\frac{x}{2}}_{\text{чётная часть}}"),
        ("p", "Сравните с ReLU: $\\operatorname{ReLU}(x)=\\frac{x}{2}+\\frac{|x|}{2}$. Нечётные части у них одинаковые, а чётная часть SiLU, $\\frac x2\\tanh\\frac x2$, — это <b>сглаженный модуль</b> $\\frac{|x|}{2}$: при больших $|x|$ тангенс равен $\\pm1$, и они совпадают, а около нуля вместо угла получается парабола $\\approx\\frac{x^2}{4}$."),
        ("table", ["$x$", "$\\sigma(x)$", "$\\operatorname{SiLU}(x)$", "$\\operatorname{SiLU}'(x)$"], "TABLE", {"num": [0, 1, 2, 3]}),
        ("p", "В таблице видны три особенности: отрицательные значения слева (самое глубокое — $-0{,}2785$), производная $0{,}5$ в нуле и производная больше 1 при $x=2$ и $x=3$."),
    ]),
    dict(id="properties", title="Свойства", blocks=[
        ("ul", [
            "<b>Гладкость</b>: SiLU бесконечно дифференцируема — нет ни одного излома.",
            "<b>Асимптоты</b>: $\\operatorname{SiLU}(x)-x\\to0$ при $x\\to+\\infty$ и $\\operatorname{SiLU}(x)\\to0$ при $x\\to-\\infty$, причём в обоих случаях экспоненциально быстро.",
            "<b>Немонотонность</b>: функция убывает на $(-\\infty;\\,x^*)$ и возрастает на $(x^*;\\,+\\infty)$, где $x^*\\approx-1{,}2785$.",
            "<b>Ограниченность снизу</b>: область значений $[-0{,}2785;\\,+\\infty)$. Сверху не ограничена.",
            "<b>Связь с ReLU</b>: $\\operatorname{ReLU}(x)-\\operatorname{SiLU}(x)=|x|\\,\\sigma(-|x|)$ — чётная функция от 0 до $0{,}2785$. SiLU всегда лежит ниже ReLU, но не дальше чем на $0{,}2785$.",
            "<b>Антисимметрия разности</b>: $\\operatorname{SiLU}(x)-\\operatorname{SiLU}(-x)=x$, потому что $\\sigma(x)+\\sigma(-x)=1$.",
            "<b>Выпуклость</b>: функция выпукла на $(-2{,}3994;\\,2{,}3994)$ и вогнута вне этого отрезка; это точки перегиба.",
        ]),
        ("h3", "Минимум: где и почему −0,278"),
        ("p", "Минимум находится там, где производная равна нулю. Результат удобно записать через W-функцию Ламберта — решение уравнения $We^{W}=c$:"),
        ("eq", r"x^*=-1-W\!\left(e^{-1}\right)\approx-1{,}2785,\qquad \operatorname{SiLU}(x^*)=x^*+1=-W\!\left(e^{-1}\right)\approx-0{,}2785"),
        ("deep", "Вывод через W-функцию Ламберта", [
            ("p", "Производная (раздел 5) равна $\\sigma(x)\\bigl(1+x(1-\\sigma(x))\\bigr)$. Сигмоида положительна, поэтому ноль даёт только скобка: $1+x(1-\\sigma)=0$, то есть $1-\\sigma(x)=-1/x$."),
            ("p", "Сразу получаем значение минимума: $\\sigma(x^*)=1+1/x^*$, и $\\operatorname{SiLU}(x^*)=x^*\\sigma(x^*)=x^*+1$."),
            ("p", "Теперь найдём $x^*$. Так как $1-\\sigma(x)=\\sigma(-x)=\\frac{1}{1+e^{x}}$, уравнение принимает вид $1+e^{x}=-x$. Положим $u=-x-1$; тогда $x=-u-1$ и"),
            ("eq", r"1+e^{-u-1}=u+1\;\Longleftrightarrow\;e^{-u}e^{-1}=u\;\Longleftrightarrow\;u\,e^{u}=e^{-1}\;\Longleftrightarrow\;u=W(e^{-1})\approx0{,}2785"),
            ("p", "Отсюда $x^*=-1-W(e^{-1})\\approx-1{,}2785$ и $\\operatorname{SiLU}(x^*)=x^*+1=-W(e^{-1})\\approx-0{,}2785$. Красивое совпадение: глубина ямы и её расстояние от точки $x=-1$ — одно и то же число."),
        ]),
        ("h3", "Семейство Swish-β"),
        ("p", "Если добавить в вентиль крутизну $\\beta$, получится семейство Swish:"),
        ("eq", r"\operatorname{Swish}_\beta(x)=x\,\sigma(\beta x),\qquad \lim_{\beta\to\infty}\operatorname{Swish}_\beta(x)=\operatorname{ReLU}(x),\qquad \operatorname{Swish}_0(x)=\frac{x}{2}"),
        ("p", "При $\\beta=0$ вентиль всегда открыт наполовину, и функция линейна. При $\\beta\\to\\infty$ сигмоида превращается в ступеньку, и получается ReLU. Swish-β — это мост между линейной функцией и ReLU, а SiLU — точка $\\beta=1$ на этом мосту. Замена $u=\\beta x$ показывает, что все члены семейства — один и тот же график в другом масштабе: $\\operatorname{Swish}_\\beta(x)=\\frac{1}{\\beta}\\operatorname{SiLU}(\\beta x)$."),
        ("viz", "silu-beta", {"beta": 1}, "<b>Рисунок 2.</b> $x\\,\\sigma(\\beta x)$ и её производная. При $\\beta=1$ минимум $(-1{,}278;\\,-0{,}278)$, наклон в нуле $0{,}5$, максимум производной $1{,}0998$. Подвигайте $\\beta$: минимум перемещается в $(-1{,}278/\\beta;\\,-0{,}278/\\beta)$, а наклон в нуле и максимум производной не меняются. При $\\beta=1{,}702$ функция почти совпадает с GELU."),
        ("p", "Рамачандран, Зоф и Ле (2017) нашли $x\\,\\sigma(\\beta x)$ автоматическим поиском среди тысяч формул-кандидатов и назвали Swish; обучаемое $\\beta$ почти ничего не добавило, и на практике закрепилось $\\beta=1$."),
    ]),
    dict(id="derivative", title="Производная: больше единицы и меньше нуля", blocks=[
        ("p", "По правилу произведения производная SiLU складывается из двух частей: вентиля и того, как быстро вентиль открывается."),
        ("eq", r"\operatorname{SiLU}'(x)=\underbrace{\sigma(x)}_{\text{вентиль}}+\underbrace{x\,\sigma'(x)}_{\text{открытие вентиля}}=\sigma(x)\bigl(1+x\,(1-\sigma(x))\bigr)"),
        ("deep", "Вывод по шагам", [
            ("p", "Правило произведения: $(x\\cdot\\sigma(x))'=1\\cdot\\sigma(x)+x\\cdot\\sigma'(x)$."),
            ("p", "Производная сигмоиды известна: $\\sigma'(x)=\\sigma(x)(1-\\sigma(x))$ (вывод — на странице <a href=\"../sigmoid/\">сигмоиды</a>). Подставляем и выносим $\\sigma(x)$:"),
            ("eq", r"\operatorname{SiLU}'(x)=\sigma(x)+x\,\sigma(x)\bigl(1-\sigma(x)\bigr)=\sigma(x)\bigl(1+x(1-\sigma(x))\bigr)"),
            ("p", "Ещё одна полезная форма — через значение самой функции $f=\\operatorname{SiLU}(x)$: раскрыв скобки, получим $\\sigma+x\\sigma-x\\sigma^2=f+\\sigma(1-f)$. Её используют реализации: на обратном проходе нужны только уже посчитанные $f$ и $\\sigma$."),
        ]),
        ("eq", r"\operatorname{SiLU}'(x)=\operatorname{SiLU}(x)+\sigma(x)\bigl(1-\operatorname{SiLU}(x)\bigr)"),
        ("p", "Свойства производной:"),
        ("ul", [
            "$\\operatorname{SiLU}'(0)=\\sigma(0)=\\tfrac12$ — в нуле наклон ровно половина;",
            "$\\operatorname{SiLU}'(x)+\\operatorname{SiLU}'(-x)=1$ — это производная тождества $\\operatorname{SiLU}(x)-\\operatorname{SiLU}(-x)=x$;",
            "производная <b>отрицательна</b> при $x&lt;-1{,}2785$ (левее минимума) с наименьшим значением $\\approx-0{,}0998$ при $x\\approx-2{,}3994$;",
            "производная <b>больше 1</b> при $x&gt;1{,}2785$ — по симметрии из предыдущего пункта — с максимумом $\\approx1{,}0998$ при $x\\approx2{,}3994$; затем она стремится к 1 сверху.",
        ]),
        ("p", "Точки $\\pm2{,}3994$ — корни уравнения $x\\tanh\\frac{x}{2}=2$: там обращается в ноль вторая производная"),
        ("eq", r"\operatorname{SiLU}''(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)\Bigl(2-x\tanh\frac{x}{2}\Bigr),\qquad \operatorname{SiLU}''(0)=\frac12"),
        ("viz", "silu-derivative", {"x": 2.3994}, "<b>Рисунок 3.</b> Производная SiLU (оранжевая) — сумма вентиля $\\sigma(x)$ и слагаемого $x\\sigma'(x)$. В точке $x=2{,}399$ вентиль даёт $0{,}9168$, второе слагаемое — $0{,}1831$, вместе $1{,}0998$; это максимум, и вторая производная (нижний график) здесь равна нулю. Слева производная опускается до $-0{,}0998$."),
        ("callout", "note", "Почему производная больше 1 — это нормально", "Наклон больше 1 значит, что на участке $x&gt;1{,}28$ SiLU «догоняет» прямую $y=x$, от которой отстала около нуля. Выход SiLU никогда не превышает вход при $x&gt;0$ ($\\sigma&lt;1$), так что взрыва нет: наклон лишь ненамного больше 1 и быстро возвращается к 1."),
    ]),
    dict(id="compare", title="Гладкость и родственники: ReLU и GELU", blocks=[
        ("p", "Три функции на одном графике: ReLU, SiLU и <a href=\"../gelu/\">GELU</a> $=x\\,\\Phi(x)$, где $\\Phi$ — функция распределения стандартного нормального закона. Посмотрите не только на сами функции, но и на первую и вторую производные: именно там видна разница в гладкости."),
        ("viz", "silu-compare", {"view": "f", "x": -1}, "<b>Рисунок 4.</b> ReLU, SiLU и GELU: функции, первые и вторые производные. При $x=-1$: SiLU $=-0{,}269$, GELU $=-0{,}159$; первые производные $0{,}072$ и $-0{,}083$ (GELU в этой точке ещё убывает, её минимум $-0{,}170$ при $x\\approx-0{,}752$); вторые производные $0{,}302$ и $0{,}242$. Вторая производная ReLU — дельта-функция в нуле: вся кривизна собрана в одной точке."),
        ("ul", [
            "<b>ReLU</b>: первая производная — ступенька, вторая — дельта-функция. Для оптимизатора поверхность ошибки состоит из плоских кусков с резкими рёбрами.",
            "<b>SiLU и GELU</b>: производные непрерывны, вторые производные — гладкие «горбы» с максимумом в нуле ($0{,}5$ у SiLU, $2\\varphi(0)\\approx0{,}798$ у GELU). Ландшафт ошибки становится гладким, и градиент меняется постепенно.",
            "<b>GELU ≈ Swish с $\\beta=1{,}702$</b>: $x\\,\\Phi(x)\\approx x\\,\\sigma(1{,}702x)$ с наибольшей ошибкой около $0{,}02$. GELU — чуть более «крутой» SiLU: минимум мельче ($-0{,}170$ против $-0{,}278$), максимум производной выше ($1{,}129$ против $1{,}100$).",
        ]),
        ("h3", "Вероятностный смысл: случайный вентиль"),
        ("p", "У SiLU и GELU есть общее объяснение. Пусть нейрон пропускает вход целиком, если вход больше случайного шума $\\varepsilon$, и полностью блокирует, если меньше: $y=x\\cdot[\\varepsilon\\le x]$. Тогда среднее значение выхода"),
        ("eq", r"\mathbb E[y]=x\cdot P(\varepsilon\le x)=x\cdot F_\varepsilon(x)=\begin{cases}x\,\sigma(x)=\operatorname{SiLU}(x), & \varepsilon\sim\text{Logistic}(0,1),\\ x\,\Phi(x)=\operatorname{GELU}(x), & \varepsilon\sim N(0,1).\end{cases}"),
        ("p", "Сигмоида — функция распределения логистического закона, $\\Phi$ — нормального. Значит, SiLU — это «усреднённый ReLU со случайным порогом»: вместо того чтобы резать ровно в нуле, нейрон режет в случайной точке около нуля, а в среднем получается гладкая кривая."),
        ("viz", "silu-noise", {"noise": "logistic"}, "<b>Рисунок 5.</b> Нажмите «Пуск». Для 33 значений $x$ разыгрывается логистический шум $\\varepsilon$, и выход равен либо $x$, либо 0 (серые точки на пунктирах). Оранжевые точки — средние выходы; через 2000 розыгрышей на точку они отходят от кривой SiLU не больше чем на $0{,}031$. Переключите шум на нормальный: средние соберутся на кривой GELU (отклонение $0{,}015$)."),
    ]),
    dict(id="swiglu", title="SwiGLU: SiLU в больших языковых моделях", blocks=[
        ("p", "В трансформере после блока внимания стоит полносвязный блок (feed-forward network, FFN). Классический вариант — $W_2\\,\\operatorname{ReLU}(W_1x)$ (или GELU вместо ReLU). Шазир (2020) предложил заменить его на <b>вентильный</b> блок (gated linear unit), где одна ветка решает, сколько пропустить из другой:"),
        ("eq", r"\operatorname{FFN}_{\text{SwiGLU}}(x)=W_2\bigl(\operatorname{SiLU}(W_1x)\odot W_3x\bigr)"),
        ("symbols", [
            (r"x\in\mathbb R^{d}", "вектор токена размерности $d$ (у LLaMA-7B $d=4096$);"),
            (r"W_1x", "ветка вентиля: через SiLU решает, какие компоненты пропускать и насколько;"),
            (r"W_3x", "ветка значения: линейная, без активации — то, что пропускается;"),
            (r"\odot", "поэлементное произведение двух векторов размерности $h$ (скрытый размер);"),
            (r"W_2", "проекция обратно в размерность $d$."),
        ]),
        ("p", "Для одной компоненты это функция двух чисел: $g(a,b)=\\operatorname{SiLU}(a)\\cdot b$, где $a$ — компонента ветки вентиля, $b$ — ветки значения. Её и стоит увидеть в 3D."),
        ("viz", "silu-swiglu", {"gate": "silu", "a": 1.5, "b": 2}, "<b>Рисунок 6.</b> Поверхность $\\operatorname{SiLU}(a)\\cdot b$ (её можно вращать) и вид сверху. При $a&lt;0$ вентиль почти закрыт, и поверхность почти плоская при любом $b$; при $a&gt;0$ она становится «седлом» $\\approx a\\cdot b$. В точке $(1{,}5;\\,2)$: вентиль $\\operatorname{SiLU}(1{,}5)=1{,}226$, выход $2{,}453$, $\\partial/\\partial a=\\operatorname{SiLU}'(1{,}5)\\cdot b=2{,}083$, $\\partial/\\partial b=1{,}226$. Переключите вентиль на ReLU, GELU, сигмоиду или уберите его совсем."),
        ("p", "Градиенты здесь простые и поучительные: $\\frac{\\partial g}{\\partial b}=\\operatorname{SiLU}(a)$ — ветка значения учится пропорционально тому, насколько открыт вентиль; $\\frac{\\partial g}{\\partial a}=\\operatorname{SiLU}'(a)\\cdot b$ — вентиль учится, только если через него есть что пропускать."),
        ("h3", "Почему скрытый размер 8/3·d"),
        ("p", "В SwiGLU три матрицы вместо двух. Чтобы число параметров осталось как у обычного FFN с $h=4d$ ($2\\cdot d\\cdot4d=8d^2$), скрытый размер уменьшают до $h=\\frac{2}{3}\\cdot4d=\\frac83 d$: тогда $3\\cdot d\\cdot\\frac83d=8d^2$. У LLaMA-7B $\\frac83\\cdot4096\\approx10923$ округлено вверх до кратного 256: $h=11008$. Получается $3\\cdot4096\\cdot11008=135\\,266\\,304$ параметра на блок против $134\\,217\\,728$ у FFN с $h=4d$ — всего на $0{,}8\\%$ больше."),
        ("callout", "history", "Откуда это пришло", "Вентильные линейные блоки (GLU, $\\sigma(W_1x)\\odot W_3x$) предложили Дофин и др. (2017) для свёрточных языковых моделей. Шазир (2020) сравнил варианты с разными вентилями — ReGLU, GEGLU, SwiGLU — и все они обошли обычный FFN. SwiGLU выбрали для PaLM (2022), затем для LLaMA (2023), и с тех пор он стал стандартом открытых LLM: Qwen, Mistral и многие другие."),
    ]),
    dict(id="training", title="SiLU в обучении", blocks=[
        ("p", "Чем гладкая активация помогает на практике? Сеть из нейронов ReLU собирает функцию из отрезков прямых, сеть из SiLU — из гладких «изгибов». Если целевая зависимость гладкая, SiLU-нейронам проще её повторить. Кроме того, у SiLU нет точного нуля градиента: при отрицательном входе производная маленькая, но не нулевая, и нейрон не «умирает»."),
        ("p", "Эксперимент: сеть $1\\to6\\to1$ приближает кривую $y=\\sin1{,}5x+0{,}3x$ по 40 точкам. Две сети стартуют с одинаковых весов, отличаются только активацией; обучение — Adam с шагом $0{,}03$, 2000 шагов."),
        ("viz", "silu-train", {"seed": 1}, "<b>Рисунок 7.</b> Нажмите «Пуск». Синяя кривая — сеть с SiLU, чёрный пунктир — с ReLU. При инициализации №1 через 2000 шагов ошибка SiLU $0{,}00139$, ReLU — $0{,}00406$, почти втрое больше. Включите «Показать нейроны»: у ReLU каждый нейрон — «уголок», у SiLU — гладкий изгиб. Редкие всплески на графике ошибки — обычные колебания Adam с постоянным шагом."),
        ("p", "Чтобы не делать выводов по одному запуску, мы повторили опыт для восьми разных инициализаций. SiLU оказалась точнее во всех восьми, с выигрышем от $1{,}4$ до $5{,}2$ раза. Но это свойство гладкой цели: на кусочно-линейной зависимости ReLU может оказаться не хуже. Поэтому выбор активации — эмпирический вопрос, и в больших моделях его решают экспериментом."),
        ("callout", "warn", "Цена гладкости", "SiLU дороже ReLU: нужна экспонента (или tanh), а для обратного прохода приходится хранить вход. На GPU это обычно незаметно на фоне матричных умножений, но на мобильных устройствах используют «жёсткий» Swish $x\\cdot\\operatorname{ReLU6}(x+3)/6$ — кусочно-полиномиальное приближение без экспонент."),
    ]),
    dict(id="code", title="В коде", blocks=[
        ("p", "Наивная запись <code>x / (1 + np.exp(-x))</code> при $x=-1000$ вычисляет $e^{1000}$ и выдаёт предупреждение о переполнении (результат всё равно $-0$). Аккуратнее считать сигмоиду через $\\tanh$: $\\sigma(x)=\\tfrac12(1+\\tanh\\tfrac x2)$ — тангенс никогда не переполняется."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Имена в библиотеках", "PyTorch: <code>nn.SiLU</code>, <code>F.silu</code>. TensorFlow/Keras: <code>tf.nn.silu</code>, <code>activation=\"swish\"</code> (это та же функция с $\\beta=1$). В конфигурациях Hugging Face: <code>hidden_act=\"silu\"</code>. Встроенная функция инициализации <code>nn.init.calculate_gain</code> не знает SiLU: обычно берут инициализацию по умолчанию или как для ReLU."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>«SiLU неотрицательна, как ReLU».</b> Нет: при $x&lt;0$ она отрицательна, минимум $-0{,}278$. Если дальше идёт что-то, что требует неотрицательного входа (например, логарифм или корень), это важно.",
            "<b>«SiLU монотонна».</b> Нет: левее $x\\approx-1{,}278$ она убывает, и её производная там отрицательна. Обратной функции на всей прямой нет.",
            "<b>Путаница SiLU и GELU.</b> Это разные функции: $x\\sigma(x)$ и $x\\Phi(x)$. Подменять одну другой в предобученной модели нельзя — веса подобраны под конкретную активацию.",
            "<b>Активация на обеих ветках SwiGLU.</b> SiLU стоит только на ветке вентиля $W_1x$; ветка значения $W_3x$ линейна. Лишняя активация меняет модель.",
            "<b>Скрытый размер $4d$ в SwiGLU.</b> С тремя матрицами это даёт в $1{,}5$ раза больше параметров, чем у обычного FFN. Для честного сравнения берут $h\\approx\\frac83d$.",
            "<b>Наивная формула с <code>exp(-x)</code></b> в самописных ядрах: переполнение при больших отрицательных $x$ и потеря точности в половинной точности. Пользуйтесь <code>F.silu</code> или формой через tanh.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../sigmoid/\">Сигмоида</a>: вентиль SiLU; производная $\\sigma'=\\sigma(1-\\sigma)$ входит в $\\operatorname{SiLU}'$.",
            "<a href=\"../relu/\">ReLU</a>: предел $x\\sigma(\\beta x)$ при $\\beta\\to\\infty$; $\\operatorname{ReLU}-\\operatorname{SiLU}=|x|\\sigma(-|x|)\\le0{,}2785$.",
            "<a href=\"../gelu/\">GELU</a>: $x\\Phi(x)\\approx x\\sigma(1{,}702x)$ — тот же самовентиль с нормальным шумом вместо логистического.",
            "<a href=\"../leaky-relu/\">Leaky ReLU</a>: другой способ не обнулять отрицательную часть — прямая $\\alpha x$ вместо гладкой «ямки».",
            "<a href=\"../tanh/\">tanh</a>: $\\operatorname{SiLU}(x)=\\frac x2\\bigl(1+\\tanh\\frac x2\\bigr)$.",
            "<a href=\"../softmax/\">Softmax</a> и <a href=\"../adam/\">Adam</a>: соседи SwiGLU в трансформере — механизм внимания и оптимизатор, которым такие модели обучают.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $\\operatorname{SiLU}(x)=x\\,\\sigma(x)=\\frac x2\\bigl(1+\\tanh\\frac x2\\bigr)$ — самовентиль: вход решает, какую долю себя пропустить. 2) Гладкая, немонотонная, минимум $-W(e^{-1})\\approx-0{,}278$ в точке $\\approx-1{,}278$; всегда ниже ReLU не более чем на $0{,}278$. 3) $\\operatorname{SiLU}'=\\sigma(1+x(1-\\sigma))$: $0{,}5$ в нуле, больше 1 при $x&gt;1{,}278$, максимум $\\approx1{,}100$. 4) Swish-β связывает линейную функцию ($\\beta=0$) и ReLU ($\\beta\\to\\infty$); GELU $\\approx$ Swish-1,702. 5) Вероятностно — ReLU со случайным логистическим порогом, усреднённый. 6) В LLM — вентиль SwiGLU: $W_2(\\operatorname{SiLU}(W_1x)\\odot W_3x)$ со скрытым размером $\\approx\\frac83d$."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="Чему примерно равно $\\operatorname{SiLU}(-1)$?", options=["$0$", "$-0{,}269$", "$0{,}269$", "$-1$"], answer=1,
                 explain="$\\operatorname{SiLU}(-1)=-1\\cdot\\sigma(-1)=-0{,}2689$: вентиль открыт примерно на четверть."),
            dict(q="Какое наименьшее значение принимает SiLU?", options=["$0$", "$\\approx-0{,}278$", "$-1$", "Не ограничена снизу"], answer=1,
                 explain="Минимум в точке $x^*\\approx-1{,}278$, значение $x^*+1=-W(e^{-1})\\approx-0{,}278$."),
            dict(q="Чему равна производная SiLU в нуле?", options=["$0$", "$0{,}25$", "$0{,}5$", "$1$"], answer=2,
                 explain="$\\operatorname{SiLU}'(0)=\\sigma(0)\\bigl(1+0\\bigr)=\\tfrac12$."),
            dict(q="В блоке SwiGLU $W_2\\bigl(\\operatorname{SiLU}(W_1x)\\odot W_3x\\bigr)$ сколько весовых матриц и какая активация на ветке $W_3x$?", options=["2 матрицы, SiLU", "3 матрицы, никакой (линейная ветка)", "3 матрицы, сигмоида", "4 матрицы, ReLU"], answer=1,
                 explain="Матрицы $W_1$, $W_2$, $W_3$; ветка значения $W_3x$ линейна, SiLU стоит только на ветке вентиля."),
            dict(q="Во что превращается $x\\,\\sigma(\\beta x)$ при $\\beta=0$?", options=["В ReLU", "В $x/2$", "В 0", "В SiLU"], answer=1,
                 explain="$\\sigma(0)=\\tfrac12$, поэтому $x\\,\\sigma(0)=x/2$. При $\\beta\\to\\infty$, наоборот, получается ReLU."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "<a href=\"../relu/\">ReLU</a> has two drawbacks: it has a kink at zero, and on the left it throws away the whole signal together with the gradient. SiLU (Sigmoid Linear Unit) works differently: the input $x$ is multiplied by the <a href=\"../sigmoid/\">sigmoid</a> of itself. A large positive input passes almost in full, a large negative one is almost completely suppressed, and near zero the input passes “partially” — smoothly, without kinks."),
        ("p", "The same function with a parameter, $x\\,\\sigma(\\beta x)$, is called Swish. With $\\beta=1$ it is exactly SiLU; PyTorch and other libraries call it just that: <code>nn.SiLU</code>."),
        ("p", "Where it appears:"),
        ("ul", [
            "<b>large language models</b> — LLaMA, Qwen, Mistral and PaLM use SiLU inside the SwiGLU block (section 7); in model configs it is the line <code>hidden_act = \"silu\"</code>;",
            "<b>computer vision</b> — EfficientNet (2019) is built on Swish, and the YOLO family of detectors uses SiLU starting with YOLOv5;",
            "<b>mobile networks</b> — MobileNetV3 uses the “hard” Swish, a cheap piecewise-polynomial approximation $x\\cdot\\operatorname{ReLU6}(x+3)/6$;",
            "<b>reinforcement learning</b> — Elfwing, Uchibe and Doya (2017) used it to approximate value functions under the name SiLU.",
        ]),
        ("callout", "key", "The essentials in a minute", "$\\operatorname{SiLU}(x)=x\\,\\sigma(x)$. Far to the right it is almost $x$, far to the left almost 0, like ReLU, but smooth. It is non-monotonic: the minimum is $\\approx-0.278$ at $x\\approx-1.278$. The derivative $\\sigma(x)\\bigl(1+x(1-\\sigma(x))\\bigr)$ equals $0.5$ at zero and exceeds 1 for $x&gt;1.278$ (maximum $\\approx1.100$). In LLMs SiLU acts as the gate in SwiGLU: $\\operatorname{SiLU}(W_1x)\\odot W_3x$."),
    ]),
    dict(id="intuition", title="Intuition: the input decides how much of itself to let through", blocks=[
        ("p", "Picture a tap whose handle is turned by the flow itself. The sigmoid $\\sigma(x)$ is how far the tap is open, from 0 to 1. If the input is large and positive, the tap is almost fully open ($\\sigma\\approx1$) and the output almost equals the input. If the input is strongly negative, the tap is almost closed and the output is close to zero. This mechanism is called <b>self-gating</b>: the input is both the signal and the decision about how much of the signal to pass."),
        ("p", "Drag the blue point. The teal curve is the gate $\\sigma(x)$, the blue one is the product $x\\cdot\\sigma(x)$. Look at the area around $x=-1$: the gate is already partly closed, but not fully, while the input is negative — and the output dips below zero."),
        ("viz", "silu-explorer", {"x": -1}, "<b>Figure 1.</b> SiLU as the product of the signal and the gate. At $x=-1$ the gate is open by $\\sigma(-1)=0.2689$, and the output is $-1\\cdot0.2689=-0.2689$. The circle marks the minimum $(-1.278,\\,-0.278)$. The grey dashed line is ReLU, the dotted line is $y=x$."),
        ("callout", "intuition", "What to notice", "On the right the blue curve hugs the line $y=x$, on the left it hugs zero: in those areas SiLU hardly differs from ReLU. The whole difference sits in the band of roughly $-5&lt;x&lt;5$, where the gate is partly open. That is where ReLU makes a sharp kink, while SiLU makes a smooth bend with a small “dip” on the left."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("p", "Let us build SiLU from two familiar parts and look at it in several forms."),
        ("eq", r"\operatorname{SiLU}(x)=\underbrace{x}_{\text{signal}}\cdot\underbrace{\sigma(x)}_{\text{gate}}=\frac{x}{1+e^{-x}}"),
        ("symbols", [
            (r"x", "the neuron’s input (pre-activation); it is also the signal to be let through;"),
            (r"\sigma(x)=\frac{1}{1+e^{-x}}", "the <a href=\"../sigmoid/\">sigmoid</a>, a number in $(0,\\,1)$ — the share of the signal that will pass;"),
            (r"x\cdot\sigma(x)", "the result: with $\\sigma\\approx1$ the output is $\\approx x$, with $\\sigma\\approx0$ it is $\\approx0$."),
        ]),
        ("p", "Through the hyperbolic tangent ($\\sigma(x)=\\tfrac12(1+\\tanh\\tfrac x2)$) we get a form that explains a lot:"),
        ("eq", r"\operatorname{SiLU}(x)=\frac{x}{2}\Bigl(1+\tanh\frac{x}{2}\Bigr)=\underbrace{\frac{x}{2}}_{\text{odd part}}+\underbrace{\frac{x}{2}\tanh\frac{x}{2}}_{\text{even part}}"),
        ("p", "Compare with ReLU: $\\operatorname{ReLU}(x)=\\frac{x}{2}+\\frac{|x|}{2}$. Their odd parts are identical, and the even part of SiLU, $\\frac x2\\tanh\\frac x2$, is a <b>smoothed absolute value</b> $\\frac{|x|}{2}$: for large $|x|$ the tangent is $\\pm1$ and they coincide, while near zero the corner is replaced by the parabola $\\approx\\frac{x^2}{4}$."),
        ("table", ["$x$", "$\\sigma(x)$", "$\\operatorname{SiLU}(x)$", "$\\operatorname{SiLU}'(x)$"], "TABLE", {"num": [0, 1, 2, 3]}),
        ("p", "The table shows three features: negative values on the left (the deepest is $-0.2785$), a derivative of $0.5$ at zero, and a derivative above 1 at $x=2$ and $x=3$."),
    ]),
    dict(id="properties", title="Properties", blocks=[
        ("ul", [
            "<b>Smoothness</b>: SiLU is infinitely differentiable — there is not a single kink.",
            "<b>Asymptotes</b>: $\\operatorname{SiLU}(x)-x\\to0$ as $x\\to+\\infty$ and $\\operatorname{SiLU}(x)\\to0$ as $x\\to-\\infty$, exponentially fast in both cases.",
            "<b>Non-monotonicity</b>: the function decreases on $(-\\infty,\\,x^*)$ and increases on $(x^*,\\,+\\infty)$, where $x^*\\approx-1.2785$.",
            "<b>Bounded below</b>: the range is $[-0.2785,\\,+\\infty)$. It is unbounded above.",
            "<b>Link with ReLU</b>: $\\operatorname{ReLU}(x)-\\operatorname{SiLU}(x)=|x|\\,\\sigma(-|x|)$ — an even function between 0 and $0.2785$. SiLU always lies below ReLU, but never more than $0.2785$ below.",
            "<b>Antisymmetry of the difference</b>: $\\operatorname{SiLU}(x)-\\operatorname{SiLU}(-x)=x$, because $\\sigma(x)+\\sigma(-x)=1$.",
            "<b>Convexity</b>: the function is convex on $(-2.3994,\\,2.3994)$ and concave outside it; these are the inflection points.",
        ]),
        ("h3", "The minimum: where and why −0.278"),
        ("p", "The minimum is where the derivative is zero. The result is neatly written through the Lambert W function — the solution of $We^{W}=c$:"),
        ("eq", r"x^*=-1-W\!\left(e^{-1}\right)\approx-1.2785,\qquad \operatorname{SiLU}(x^*)=x^*+1=-W\!\left(e^{-1}\right)\approx-0.2785"),
        ("deep", "Derivation through the Lambert W function", [
            ("p", "The derivative (section 5) is $\\sigma(x)\\bigl(1+x(1-\\sigma(x))\\bigr)$. The sigmoid is positive, so only the bracket can vanish: $1+x(1-\\sigma)=0$, i.e. $1-\\sigma(x)=-1/x$."),
            ("p", "This immediately gives the value of the minimum: $\\sigma(x^*)=1+1/x^*$, and $\\operatorname{SiLU}(x^*)=x^*\\sigma(x^*)=x^*+1$."),
            ("p", "Now find $x^*$. Since $1-\\sigma(x)=\\sigma(-x)=\\frac{1}{1+e^{x}}$, the equation becomes $1+e^{x}=-x$. Put $u=-x-1$; then $x=-u-1$ and"),
            ("eq", r"1+e^{-u-1}=u+1\;\Longleftrightarrow\;e^{-u}e^{-1}=u\;\Longleftrightarrow\;u\,e^{u}=e^{-1}\;\Longleftrightarrow\;u=W(e^{-1})\approx0.2785"),
            ("p", "Hence $x^*=-1-W(e^{-1})\\approx-1.2785$ and $\\operatorname{SiLU}(x^*)=x^*+1=-W(e^{-1})\\approx-0.2785$. A pretty coincidence: the depth of the dip and its distance from the point $x=-1$ are the same number."),
        ]),
        ("h3", "The Swish-β family"),
        ("p", "Adding a steepness $\\beta$ to the gate gives the Swish family:"),
        ("eq", r"\operatorname{Swish}_\beta(x)=x\,\sigma(\beta x),\qquad \lim_{\beta\to\infty}\operatorname{Swish}_\beta(x)=\operatorname{ReLU}(x),\qquad \operatorname{Swish}_0(x)=\frac{x}{2}"),
        ("p", "With $\\beta=0$ the gate is always half open, and the function is linear. As $\\beta\\to\\infty$ the sigmoid turns into a step, and we get ReLU. Swish-β is a bridge between a linear function and ReLU, and SiLU is the point $\\beta=1$ on that bridge. The substitution $u=\\beta x$ shows that all members of the family are one and the same graph at a different scale: $\\operatorname{Swish}_\\beta(x)=\\frac{1}{\\beta}\\operatorname{SiLU}(\\beta x)$."),
        ("viz", "silu-beta", {"beta": 1}, "<b>Figure 2.</b> $x\\,\\sigma(\\beta x)$ and its derivative. At $\\beta=1$ the minimum is $(-1.278,\\,-0.278)$, the slope at zero is $0.5$, and the maximum of the derivative is $1.0998$. Move $\\beta$: the minimum shifts to $(-1.278/\\beta,\\,-0.278/\\beta)$, while the slope at zero and the maximum of the derivative stay the same. At $\\beta=1.702$ the function nearly coincides with GELU."),
        ("p", "Ramachandran, Zoph and Le (2017) found $x\\,\\sigma(\\beta x)$ by an automated search among thousands of candidate formulas and called it Swish; a learnable $\\beta$ added almost nothing, and in practice $\\beta=1$ stuck."),
    ]),
    dict(id="derivative", title="The derivative: above one and below zero", blocks=[
        ("p", "By the product rule the derivative of SiLU is made of two parts: the gate and how fast the gate opens."),
        ("eq", r"\operatorname{SiLU}'(x)=\underbrace{\sigma(x)}_{\text{gate}}+\underbrace{x\,\sigma'(x)}_{\text{gate opening}}=\sigma(x)\bigl(1+x\,(1-\sigma(x))\bigr)"),
        ("deep", "Step-by-step derivation", [
            ("p", "The product rule: $(x\\cdot\\sigma(x))'=1\\cdot\\sigma(x)+x\\cdot\\sigma'(x)$."),
            ("p", "The derivative of the sigmoid is known: $\\sigma'(x)=\\sigma(x)(1-\\sigma(x))$ (derived on the <a href=\"../sigmoid/\">sigmoid</a> page). Substitute and factor out $\\sigma(x)$:"),
            ("eq", r"\operatorname{SiLU}'(x)=\sigma(x)+x\,\sigma(x)\bigl(1-\sigma(x)\bigr)=\sigma(x)\bigl(1+x(1-\sigma(x))\bigr)"),
            ("p", "One more useful form uses the value of the function itself, $f=\\operatorname{SiLU}(x)$: expanding the brackets gives $\\sigma+x\\sigma-x\\sigma^2=f+\\sigma(1-f)$. Implementations use it: the backward pass needs only the already computed $f$ and $\\sigma$."),
        ]),
        ("eq", r"\operatorname{SiLU}'(x)=\operatorname{SiLU}(x)+\sigma(x)\bigl(1-\operatorname{SiLU}(x)\bigr)"),
        ("p", "Properties of the derivative:"),
        ("ul", [
            "$\\operatorname{SiLU}'(0)=\\sigma(0)=\\tfrac12$ — at zero the slope is exactly one half;",
            "$\\operatorname{SiLU}'(x)+\\operatorname{SiLU}'(-x)=1$ — the derivative of the identity $\\operatorname{SiLU}(x)-\\operatorname{SiLU}(-x)=x$;",
            "the derivative is <b>negative</b> for $x&lt;-1.2785$ (left of the minimum), with the smallest value $\\approx-0.0998$ at $x\\approx-2.3994$;",
            "the derivative is <b>above 1</b> for $x&gt;1.2785$ — by the symmetry of the previous item — with a maximum of $\\approx1.0998$ at $x\\approx2.3994$; then it tends to 1 from above.",
        ]),
        ("p", "The points $\\pm2.3994$ are the roots of $x\\tanh\\frac{x}{2}=2$: that is where the second derivative vanishes"),
        ("eq", r"\operatorname{SiLU}''(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)\Bigl(2-x\tanh\frac{x}{2}\Bigr),\qquad \operatorname{SiLU}''(0)=\frac12"),
        ("viz", "silu-derivative", {"x": 2.3994}, "<b>Figure 3.</b> The derivative of SiLU (orange) is the sum of the gate $\\sigma(x)$ and the term $x\\sigma'(x)$. At $x=2.399$ the gate gives $0.9168$, the second term $0.1831$, together $1.0998$; this is the maximum, and the second derivative (lower plot) is zero here. On the left the derivative drops to $-0.0998$."),
        ("callout", "note", "Why a derivative above 1 is fine", "A slope above 1 means that for $x&gt;1.28$ SiLU is “catching up” with the line $y=x$, from which it fell behind near zero. For $x&gt;0$ the output of SiLU never exceeds the input ($\\sigma&lt;1$), so nothing explodes: the slope is only slightly above 1 and quickly returns to 1."),
    ]),
    dict(id="compare", title="Smoothness and relatives: ReLU and GELU", blocks=[
        ("p", "Three functions on one plot: ReLU, SiLU and <a href=\"../gelu/\">GELU</a> $=x\\,\\Phi(x)$, where $\\Phi$ is the cumulative distribution function of the standard normal. Look not only at the functions but also at the first and second derivatives: that is where the difference in smoothness shows."),
        ("viz", "silu-compare", {"view": "f", "x": -1}, "<b>Figure 4.</b> ReLU, SiLU and GELU: the functions, the first and the second derivatives. At $x=-1$: SiLU $=-0.269$, GELU $=-0.159$; the first derivatives are $0.072$ and $-0.083$ (GELU is still decreasing there, its minimum is $-0.170$ at $x\\approx-0.752$); the second derivatives are $0.302$ and $0.242$. The second derivative of ReLU is a delta function at zero: all the curvature is gathered at one point."),
        ("ul", [
            "<b>ReLU</b>: the first derivative is a step, the second a delta function. For the optimizer the loss surface is made of flat pieces with sharp edges.",
            "<b>SiLU and GELU</b>: the derivatives are continuous, the second derivatives are smooth “humps” peaking at zero ($0.5$ for SiLU, $2\\varphi(0)\\approx0.798$ for GELU). The loss landscape becomes smooth, and the gradient changes gradually.",
            "<b>GELU ≈ Swish with $\\beta=1.702$</b>: $x\\,\\Phi(x)\\approx x\\,\\sigma(1.702x)$ with a largest error of about $0.02$. GELU is a slightly “steeper” SiLU: its dip is shallower ($-0.170$ versus $-0.278$), and its maximum derivative is higher ($1.129$ versus $1.100$).",
        ]),
        ("h3", "The probabilistic meaning: a random gate"),
        ("p", "SiLU and GELU share an explanation. Let a neuron pass the input in full if the input is larger than a random noise $\\varepsilon$, and block it completely otherwise: $y=x\\cdot[\\varepsilon\\le x]$. Then the mean output is"),
        ("eq", r"\mathbb E[y]=x\cdot P(\varepsilon\le x)=x\cdot F_\varepsilon(x)=\begin{cases}x\,\sigma(x)=\operatorname{SiLU}(x), & \varepsilon\sim\text{Logistic}(0,1),\\ x\,\Phi(x)=\operatorname{GELU}(x), & \varepsilon\sim N(0,1).\end{cases}"),
        ("p", "The sigmoid is the distribution function of the logistic law, $\\Phi$ that of the normal one. So SiLU is an “averaged ReLU with a random threshold”: instead of cutting exactly at zero, the neuron cuts at a random point near zero, and on average the result is a smooth curve."),
        ("viz", "silu-noise", {"noise": "logistic"}, "<b>Figure 5.</b> Press “Play”. For 33 values of $x$ a logistic noise $\\varepsilon$ is drawn, and the output is either $x$ or 0 (grey dots on the dashed lines). The orange dots are the mean outputs; after 2000 draws per point they deviate from the SiLU curve by at most $0.031$. Switch the noise to normal: the means gather on the GELU curve (deviation $0.015$)."),
    ]),
    dict(id="swiglu", title="SwiGLU: SiLU in large language models", blocks=[
        ("p", "In a transformer the attention block is followed by a fully connected block (feed-forward network, FFN). The classic version is $W_2\\,\\operatorname{ReLU}(W_1x)$ (or GELU instead of ReLU). Shazeer (2020) proposed replacing it with a <b>gated</b> block (gated linear unit), where one branch decides how much of the other to let through:"),
        ("eq", r"\operatorname{FFN}_{\text{SwiGLU}}(x)=W_2\bigl(\operatorname{SiLU}(W_1x)\odot W_3x\bigr)"),
        ("symbols", [
            (r"x\in\mathbb R^{d}", "the token vector of dimension $d$ (for LLaMA-7B $d=4096$);"),
            (r"W_1x", "the gate branch: through SiLU it decides which components to pass and how much;"),
            (r"W_3x", "the value branch: linear, with no activation — what gets passed;"),
            (r"\odot", "the element-wise product of two vectors of dimension $h$ (the hidden size);"),
            (r"W_2", "the projection back to dimension $d$."),
        ]),
        ("p", "For a single component this is a function of two numbers: $g(a,b)=\\operatorname{SiLU}(a)\\cdot b$, where $a$ is a component of the gate branch and $b$ of the value branch. It is worth seeing in 3D."),
        ("viz", "silu-swiglu", {"gate": "silu", "a": 1.5, "b": 2}, "<b>Figure 6.</b> The surface $\\operatorname{SiLU}(a)\\cdot b$ (you can rotate it) and the view from above. For $a&lt;0$ the gate is almost closed, and the surface is almost flat for any $b$; for $a&gt;0$ it becomes the “saddle” $\\approx a\\cdot b$. At the point $(1.5,\\,2)$: the gate $\\operatorname{SiLU}(1.5)=1.226$, the output $2.453$, $\\partial/\\partial a=\\operatorname{SiLU}'(1.5)\\cdot b=2.083$, $\\partial/\\partial b=1.226$. Switch the gate to ReLU, GELU, the sigmoid, or remove it altogether."),
        ("p", "The gradients here are simple and instructive: $\\frac{\\partial g}{\\partial b}=\\operatorname{SiLU}(a)$ — the value branch learns in proportion to how far the gate is open; $\\frac{\\partial g}{\\partial a}=\\operatorname{SiLU}'(a)\\cdot b$ — the gate learns only if there is something to pass through it."),
        ("h3", "Why the hidden size is 8/3·d"),
        ("p", "SwiGLU has three matrices instead of two. To keep the parameter count of an ordinary FFN with $h=4d$ ($2\\cdot d\\cdot4d=8d^2$), the hidden size is reduced to $h=\\frac{2}{3}\\cdot4d=\\frac83 d$: then $3\\cdot d\\cdot\\frac83d=8d^2$. For LLaMA-7B $\\frac83\\cdot4096\\approx10923$ is rounded up to a multiple of 256: $h=11008$. That gives $3\\cdot4096\\cdot11008=135{,}266{,}304$ parameters per block versus $134{,}217{,}728$ for an FFN with $h=4d$ — only $0.8\\%$ more."),
        ("callout", "history", "Where it came from", "Gated linear units (GLU, $\\sigma(W_1x)\\odot W_3x$) were proposed by Dauphin et al. (2017) for convolutional language models. Shazeer (2020) compared variants with different gates — ReGLU, GEGLU, SwiGLU — and all of them beat the ordinary FFN. SwiGLU was chosen for PaLM (2022), then for LLaMA (2023), and since then it has been the standard of open LLMs: Qwen, Mistral and many others."),
    ]),
    dict(id="training", title="SiLU in training", blocks=[
        ("p", "How does a smooth activation help in practice? A network of ReLU neurons assembles a function from line segments, a network of SiLUs from smooth “bends”. If the target dependence is smooth, SiLU neurons find it easier to reproduce. Besides, SiLU has no exact zero gradient: for a negative input the derivative is small but not zero, and the neuron does not “die”."),
        ("p", "The experiment: a $1\\to6\\to1$ network approximates the curve $y=\\sin1.5x+0.3x$ from 40 points. Both networks start from the same weights and differ only in the activation; training is Adam with step $0.03$ for 2000 steps."),
        ("viz", "silu-train", {"seed": 1}, "<b>Figure 7.</b> Press “Play”. The blue curve is the network with SiLU, the black dashes the one with ReLU. With initialization #1, after 2000 steps the SiLU error is $0.00139$ and the ReLU error $0.00406$, almost three times larger. Turn on “Show the neurons”: in ReLU every neuron is a “corner”, in SiLU a smooth bend. The rare spikes in the error curve are the usual oscillations of Adam with a constant step."),
        ("p", "To avoid conclusions from a single run, we repeated the experiment for eight different initializations. SiLU was more accurate in all eight, by a factor of $1.4$ to $5.2$. But this is a property of a smooth target: on a piecewise-linear dependence ReLU may do no worse. So the choice of activation is an empirical question, and in large models it is settled by experiment."),
        ("callout", "warn", "The price of smoothness", "SiLU is more expensive than ReLU: it needs an exponential (or tanh), and the backward pass has to keep the input. On a GPU this is usually invisible next to the matrix multiplications, but on mobile devices people use the “hard” Swish $x\\cdot\\operatorname{ReLU6}(x+3)/6$ — a piecewise-polynomial approximation without exponentials."),
    ]),
    dict(id="code", title="In code", blocks=[
        ("p", "The naive form <code>x / (1 + np.exp(-x))</code> at $x=-1000$ computes $e^{1000}$ and emits an overflow warning (the result is still $-0$). It is cleaner to compute the sigmoid through $\\tanh$: $\\sigma(x)=\\tfrac12(1+\\tanh\\tfrac x2)$ — the tangent never overflows."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Names in libraries", "PyTorch: <code>nn.SiLU</code>, <code>F.silu</code>. TensorFlow/Keras: <code>tf.nn.silu</code>, <code>activation=\"swish\"</code> (the same function with $\\beta=1$). In Hugging Face configs: <code>hidden_act=\"silu\"</code>. The built-in <code>nn.init.calculate_gain</code> does not know SiLU: people usually take the default initialization or the one for ReLU."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>“SiLU is non-negative, like ReLU.”</b> No: for $x&lt;0$ it is negative, with a minimum of $-0.278$. If something that needs a non-negative input follows (a logarithm or a square root, say), this matters.",
            "<b>“SiLU is monotonic.”</b> No: to the left of $x\\approx-1.278$ it decreases, and its derivative is negative there. It has no inverse on the whole line.",
            "<b>Confusing SiLU and GELU.</b> They are different functions: $x\\sigma(x)$ and $x\\Phi(x)$. You cannot swap one for the other in a pretrained model — the weights are tuned to a specific activation.",
            "<b>An activation on both branches of SwiGLU.</b> SiLU sits only on the gate branch $W_1x$; the value branch $W_3x$ is linear. An extra activation changes the model.",
            "<b>A hidden size of $4d$ in SwiGLU.</b> With three matrices this gives $1.5$ times more parameters than an ordinary FFN. For a fair comparison take $h\\approx\\frac83d$.",
            "<b>The naive formula with <code>exp(-x)</code></b> in hand-written kernels: overflow for large negative $x$ and loss of precision in half precision. Use <code>F.silu</code> or the tanh form.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../sigmoid/\">Sigmoid</a>: the gate of SiLU; the derivative $\\sigma'=\\sigma(1-\\sigma)$ enters $\\operatorname{SiLU}'$.",
            "<a href=\"../relu/\">ReLU</a>: the limit of $x\\sigma(\\beta x)$ as $\\beta\\to\\infty$; $\\operatorname{ReLU}-\\operatorname{SiLU}=|x|\\sigma(-|x|)\\le0.2785$.",
            "<a href=\"../gelu/\">GELU</a>: $x\\Phi(x)\\approx x\\sigma(1.702x)$ — the same self-gate with normal noise instead of logistic.",
            "<a href=\"../leaky-relu/\">Leaky ReLU</a>: another way not to zero the negative part — the line $\\alpha x$ instead of a smooth dip.",
            "<a href=\"../tanh/\">tanh</a>: $\\operatorname{SiLU}(x)=\\frac x2\\bigl(1+\\tanh\\frac x2\\bigr)$.",
            "<a href=\"../softmax/\">Softmax</a> and <a href=\"../adam/\">Adam</a>: SwiGLU’s neighbours in a transformer — the attention mechanism and the optimizer such models are trained with.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $\\operatorname{SiLU}(x)=x\\,\\sigma(x)=\\frac x2\\bigl(1+\\tanh\\frac x2\\bigr)$ is a self-gate: the input decides what share of itself to pass. 2) Smooth, non-monotonic, with a minimum of $-W(e^{-1})\\approx-0.278$ at $\\approx-1.278$; always below ReLU by at most $0.278$. 3) $\\operatorname{SiLU}'=\\sigma(1+x(1-\\sigma))$: $0.5$ at zero, above 1 for $x&gt;1.278$, maximum $\\approx1.100$. 4) Swish-β links the linear function ($\\beta=0$) and ReLU ($\\beta\\to\\infty$); GELU $\\approx$ Swish-1.702. 5) Probabilistically, it is ReLU with a random logistic threshold, averaged. 6) In LLMs it is the gate of SwiGLU: $W_2(\\operatorname{SiLU}(W_1x)\\odot W_3x)$ with a hidden size of $\\approx\\frac83d$."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="What is $\\operatorname{SiLU}(-1)$ approximately?", options=["$0$", "$-0.269$", "$0.269$", "$-1$"], answer=1,
                 explain="$\\operatorname{SiLU}(-1)=-1\\cdot\\sigma(-1)=-0.2689$: the gate is about a quarter open."),
            dict(q="What is the smallest value SiLU takes?", options=["$0$", "$\\approx-0.278$", "$-1$", "It is unbounded below"], answer=1,
                 explain="The minimum is at $x^*\\approx-1.278$, with the value $x^*+1=-W(e^{-1})\\approx-0.278$."),
            dict(q="What is the derivative of SiLU at zero?", options=["$0$", "$0.25$", "$0.5$", "$1$"], answer=2,
                 explain="$\\operatorname{SiLU}'(0)=\\sigma(0)\\bigl(1+0\\bigr)=\\tfrac12$."),
            dict(q="In the SwiGLU block $W_2\\bigl(\\operatorname{SiLU}(W_1x)\\odot W_3x\\bigr)$, how many weight matrices are there and what activation is on the $W_3x$ branch?", options=["2 matrices, SiLU", "3 matrices, none (a linear branch)", "3 matrices, the sigmoid", "4 matrices, ReLU"], answer=1,
                 explain="The matrices are $W_1$, $W_2$, $W_3$; the value branch $W_3x$ is linear, and SiLU sits only on the gate branch."),
            dict(q="What does $x\\,\\sigma(\\beta x)$ become at $\\beta=0$?", options=["ReLU", "$x/2$", "0", "SiLU"], answer=1,
                 explain="$\\sigma(0)=\\tfrac12$, so $x\\,\\sigma(0)=x/2$. As $\\beta\\to\\infty$, on the contrary, we get ReLU."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "<a href=\"../relu/\">ReLU</a>’ning ikki kamchiligi bor: nolda u sinadi, chapda esa butun signalni gradiyent bilan birga tashlab yuboradi. SiLU (Sigmoid Linear Unit) boshqacha tuzilgan: $x$ kirish o‘zining <a href=\"../sigmoid/\">sigmoidasiga</a> ko‘paytiriladi. Katta musbat kirish deyarli to‘liq o‘tadi, katta manfiy kirish deyarli butunlay so‘ndiriladi, nol atrofida esa kirish «qisman» — silliq, sinishsiz o‘tadi."),
        ("p", "Parametrli o‘sha funksiya, $x\\,\\sigma(\\beta x)$, Swish deb ataladi. $\\beta=1$ da bu aynan SiLU; PyTorch va boshqa kutubxonalarda uni shunday yozishadi: <code>nn.SiLU</code>."),
        ("p", "U qayerda uchraydi:"),
        ("ul", [
            "<b>katta til modellari</b> — LLaMA, Qwen, Mistral va PaLM SiLU’ni SwiGLU bloki ichida ishlatadi (7-bo‘lim); model konfiguratsiyalarida bu <code>hidden_act = \"silu\"</code> qatori;",
            "<b>kompyuter ko‘rishi</b> — EfficientNet (2019) Swish asosida qurilgan, YOLO oilasidagi detektorlar YOLOv5 dan boshlab SiLU’dan foydalanadi;",
            "<b>mobil tarmoqlar</b> — MobileNetV3 «qattiq» Swish’dan, arzon bo‘lak-polinomial $x\\cdot\\operatorname{ReLU6}(x+3)/6$ yaqinlashishdan foydalanadi;",
            "<b>mustahkamlab o‘qitish</b> — Elfving, Utibe va Doya (2017) uni SiLU nomi bilan qiymat funksiyalarini approksimatsiya qilish uchun qo‘llagan.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "$\\operatorname{SiLU}(x)=x\\,\\sigma(x)$. O‘ngda uzoqda u deyarli $x$ ga, chapda uzoqda deyarli 0 ga teng — ReLU kabi, lekin silliq. U nomonoton: minimum $x\\approx-1{,}278$ nuqtada $\\approx-0{,}278$. $\\sigma(x)\\bigl(1+x(1-\\sigma(x))\\bigr)$ hosila nolda $0{,}5$ ga teng va $x&gt;1{,}278$ da 1 dan oshadi (maksimum $\\approx1{,}100$). LLM’larda SiLU SwiGLU’da ventil vazifasini bajaradi: $\\operatorname{SiLU}(W_1x)\\odot W_3x$."),
    ]),
    dict(id="intuition", title="Intuitsiya: kirish o‘zidan qanchasini o‘tkazishni o‘zi hal qiladi", blocks=[
        ("p", "Dastasini oqimning o‘zi buraydigan jo‘mrakni tasavvur qiling. $\\sigma(x)$ sigmoida — jo‘mrakning ochiqlik darajasi, 0 dan 1 gacha. Agar kirish katta va musbat bo‘lsa, jo‘mrak deyarli to‘liq ochiq ($\\sigma\\approx1$) va chiqish deyarli kirishga teng. Agar kirish kuchli manfiy bo‘lsa, jo‘mrak deyarli yopiq va chiqish nolga yaqin. Bunday mexanizm <b>o‘z-o‘zini ventillash</b> (self-gating) deyiladi: kirish bir vaqtning o‘zida ham signal, ham signalning qancha qismini o‘tkazish haqidagi qaror."),
        ("p", "Ko‘k nuqtani torting. Firuza egri chiziq — $\\sigma(x)$ ventil, ko‘k — $x\\cdot\\sigma(x)$ ko‘paytma. $x=-1$ atrofiga qarang: ventil allaqachon qisman yopilgan, lekin to‘liq emas, kirish esa manfiy — va chiqish noldan pastga tushadi."),
        ("viz", "silu-explorer", {"x": -1}, "<b>1-rasm.</b> Signal va ventil ko‘paytmasi sifatidagi SiLU. $x=-1$ da ventil $\\sigma(-1)=0{,}2689$ ga ochiq va chiqish $-1\\cdot0{,}2689=-0{,}2689$ ga teng. Doiracha $(-1{,}278;\\,-0{,}278)$ minimumni belgilaydi. Kulrang punktir — ReLU, nuqtali chiziq — $y=x$."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "O‘ngda ko‘k egri chiziq $y=x$ to‘g‘ri chiziqqa, chapda esa nolga yopishadi: bu sohalarda SiLU ReLU’dan deyarli farq qilmaydi. Butun farq taxminan $-5&lt;x&lt;5$ yo‘lakda, ventil qisman ochiq joyda jamlangan. Aynan u yerda ReLU keskin sinadi, SiLU esa chapda kichik «chuqurcha» bilan silliq egiladi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", "SiLU’ni ikki tanish qismdan yig‘amiz va unga bir necha yozuvda qaraymiz."),
        ("eq", r"\operatorname{SiLU}(x)=\underbrace{x}_{\text{signal}}\cdot\underbrace{\sigma(x)}_{\text{ventil}}=\frac{x}{1+e^{-x}}"),
        ("symbols", [
            (r"x", "neyron kirishi (pre-aktivatsiya); u o‘tkazilishi kerak bo‘lgan signal ham;"),
            (r"\sigma(x)=\frac{1}{1+e^{-x}}", "<a href=\"../sigmoid/\">sigmoida</a>, $(0;\\,1)$ dagi son — signalning o‘tadigan ulushi;"),
            (r"x\cdot\sigma(x)", "natija: $\\sigma\\approx1$ da chiqish $\\approx x$, $\\sigma\\approx0$ da chiqish $\\approx0$."),
        ]),
        ("p", "Giperbolik tangens orqali ($\\sigma(x)=\\tfrac12(1+\\tanh\\tfrac x2)$) ko‘p narsani tushuntiradigan yozuv hosil bo‘ladi:"),
        ("eq", r"\operatorname{SiLU}(x)=\frac{x}{2}\Bigl(1+\tanh\frac{x}{2}\Bigr)=\underbrace{\frac{x}{2}}_{\text{toq qism}}+\underbrace{\frac{x}{2}\tanh\frac{x}{2}}_{\text{juft qism}}"),
        ("p", "ReLU bilan solishtiring: $\\operatorname{ReLU}(x)=\\frac{x}{2}+\\frac{|x|}{2}$. Ularning toq qismlari bir xil, SiLU’ning juft qismi $\\frac x2\\tanh\\frac x2$ esa — <b>silliqlangan modul</b> $\\frac{|x|}{2}$: katta $|x|$ larda tangens $\\pm1$ ga teng va ular ustma-ust tushadi, nol atrofida esa burchak o‘rniga $\\approx\\frac{x^2}{4}$ parabola hosil bo‘ladi."),
        ("table", ["$x$", "$\\sigma(x)$", "$\\operatorname{SiLU}(x)$", "$\\operatorname{SiLU}'(x)$"], "TABLE", {"num": [0, 1, 2, 3]}),
        ("p", "Jadvalda uchta xususiyat ko‘rinadi: chapdagi manfiy qiymatlar (eng chuquri — $-0{,}2785$), nolda $0{,}5$ hosila va $x=2$ hamda $x=3$ da 1 dan katta hosila."),
    ]),
    dict(id="properties", title="Xossalar", blocks=[
        ("ul", [
            "<b>Silliqlik</b>: SiLU cheksiz differensiallanuvchi — birorta ham sinish yo‘q.",
            "<b>Asimptotalar</b>: $x\\to+\\infty$ da $\\operatorname{SiLU}(x)-x\\to0$ va $x\\to-\\infty$ da $\\operatorname{SiLU}(x)\\to0$, ikkala holda ham eksponensial tez.",
            "<b>Nomonotonlik</b>: funksiya $(-\\infty;\\,x^*)$ da kamayadi va $(x^*;\\,+\\infty)$ da o‘sadi, bu yerda $x^*\\approx-1{,}2785$.",
            "<b>Quyidan chegaralanganlik</b>: qiymatlar sohasi $[-0{,}2785;\\,+\\infty)$. Yuqoridan chegaralanmagan.",
            "<b>ReLU bilan bog‘liqlik</b>: $\\operatorname{ReLU}(x)-\\operatorname{SiLU}(x)=|x|\\,\\sigma(-|x|)$ — 0 dan $0{,}2785$ gacha juft funksiya. SiLU doim ReLU’dan pastda yotadi, lekin $0{,}2785$ dan uzoq emas.",
            "<b>Ayirmaning antisimmetriyasi</b>: $\\operatorname{SiLU}(x)-\\operatorname{SiLU}(-x)=x$, chunki $\\sigma(x)+\\sigma(-x)=1$.",
            "<b>Qavariqlik</b>: funksiya $(-2{,}3994;\\,2{,}3994)$ da qavariq va bu kesmadan tashqarida botiq; bular burilish nuqtalari.",
        ]),
        ("h3", "Minimum: qayerda va nega −0,278"),
        ("p", "Minimum hosila nolga teng bo‘lgan joyda. Natijani Lambert W-funksiyasi — $We^{W}=c$ tenglama yechimi orqali yozish qulay:"),
        ("eq", r"x^*=-1-W\!\left(e^{-1}\right)\approx-1{,}2785,\qquad \operatorname{SiLU}(x^*)=x^*+1=-W\!\left(e^{-1}\right)\approx-0{,}2785"),
        ("deep", "Lambert W-funksiyasi orqali keltirib chiqarish", [
            ("p", "Hosila (5-bo‘lim) $\\sigma(x)\\bigl(1+x(1-\\sigma(x))\\bigr)$ ga teng. Sigmoida musbat, shuning uchun nolni faqat qavs beradi: $1+x(1-\\sigma)=0$, ya’ni $1-\\sigma(x)=-1/x$."),
            ("p", "Darhol minimum qiymatini olamiz: $\\sigma(x^*)=1+1/x^*$ va $\\operatorname{SiLU}(x^*)=x^*\\sigma(x^*)=x^*+1$."),
            ("p", "Endi $x^*$ ni topamiz. $1-\\sigma(x)=\\sigma(-x)=\\frac{1}{1+e^{x}}$ bo‘lgani uchun tenglama $1+e^{x}=-x$ ko‘rinishini oladi. $u=-x-1$ deylik; u holda $x=-u-1$ va"),
            ("eq", r"1+e^{-u-1}=u+1\;\Longleftrightarrow\;e^{-u}e^{-1}=u\;\Longleftrightarrow\;u\,e^{u}=e^{-1}\;\Longleftrightarrow\;u=W(e^{-1})\approx0{,}2785"),
            ("p", "Bundan $x^*=-1-W(e^{-1})\\approx-1{,}2785$ va $\\operatorname{SiLU}(x^*)=x^*+1=-W(e^{-1})\\approx-0{,}2785$. Chiroyli moslik: chuqurchaning chuqurligi va uning $x=-1$ nuqtadan masofasi — bir xil son."),
        ]),
        ("h3", "Swish-β oilasi"),
        ("p", "Ventilga $\\beta$ tiklik qo‘shsak, Swish oilasi hosil bo‘ladi:"),
        ("eq", r"\operatorname{Swish}_\beta(x)=x\,\sigma(\beta x),\qquad \lim_{\beta\to\infty}\operatorname{Swish}_\beta(x)=\operatorname{ReLU}(x),\qquad \operatorname{Swish}_0(x)=\frac{x}{2}"),
        ("p", "$\\beta=0$ da ventil doim yarim ochiq va funksiya chiziqli. $\\beta\\to\\infty$ da sigmoida zinaga aylanadi va ReLU hosil bo‘ladi. Swish-β — chiziqli funksiya va ReLU orasidagi ko‘prik, SiLU esa bu ko‘prikdagi $\\beta=1$ nuqta. $u=\\beta x$ almashtirish oilaning barcha a’zolari boshqa masshtabdagi bitta grafik ekanini ko‘rsatadi: $\\operatorname{Swish}_\\beta(x)=\\frac{1}{\\beta}\\operatorname{SiLU}(\\beta x)$."),
        ("viz", "silu-beta", {"beta": 1}, "<b>2-rasm.</b> $x\\,\\sigma(\\beta x)$ va uning hosilasi. $\\beta=1$ da minimum $(-1{,}278;\\,-0{,}278)$, noldagi qiyalik $0{,}5$, hosila maksimumi $1{,}0998$. $\\beta$ ni suring: minimum $(-1{,}278/\\beta;\\,-0{,}278/\\beta)$ ga ko‘chadi, noldagi qiyalik va hosila maksimumi esa o‘zgarmaydi. $\\beta=1{,}702$ da funksiya GELU bilan deyarli ustma-ust tushadi."),
        ("p", "Ramachandran, Zof va Le (2017) $x\\,\\sigma(\\beta x)$ ni minglab nomzod formulalar orasidan avtomatik qidiruv bilan topib, Swish deb atashgan; o‘rganiladigan $\\beta$ deyarli hech narsa qo‘shmagan va amalda $\\beta=1$ qaror topgan."),
    ]),
    dict(id="derivative", title="Hosila: birdan katta va noldan kichik", blocks=[
        ("p", "Ko‘paytma qoidasiga ko‘ra SiLU hosilasi ikki qismdan iborat: ventil va ventil qanchalik tez ochilishi."),
        ("eq", r"\operatorname{SiLU}'(x)=\underbrace{\sigma(x)}_{\text{ventil}}+\underbrace{x\,\sigma'(x)}_{\text{ventil ochilishi}}=\sigma(x)\bigl(1+x\,(1-\sigma(x))\bigr)"),
        ("deep", "Qadamma-qadam keltirib chiqarish", [
            ("p", "Ko‘paytma qoidasi: $(x\\cdot\\sigma(x))'=1\\cdot\\sigma(x)+x\\cdot\\sigma'(x)$."),
            ("p", "Sigmoida hosilasi ma’lum: $\\sigma'(x)=\\sigma(x)(1-\\sigma(x))$ (keltirib chiqarilishi — <a href=\"../sigmoid/\">sigmoida</a> sahifasida). O‘rniga qo‘yamiz va $\\sigma(x)$ ni qavsdan chiqaramiz:"),
            ("eq", r"\operatorname{SiLU}'(x)=\sigma(x)+x\,\sigma(x)\bigl(1-\sigma(x)\bigr)=\sigma(x)\bigl(1+x(1-\sigma(x))\bigr)"),
            ("p", "Yana bir foydali shakl funksiyaning o‘z qiymati $f=\\operatorname{SiLU}(x)$ orqali: qavslarni ochsak, $\\sigma+x\\sigma-x\\sigma^2=f+\\sigma(1-f)$ hosil bo‘ladi. Uni amalga oshirishlar ishlatadi: teskari o‘tishda faqat allaqachon hisoblangan $f$ va $\\sigma$ kerak."),
        ]),
        ("eq", r"\operatorname{SiLU}'(x)=\operatorname{SiLU}(x)+\sigma(x)\bigl(1-\operatorname{SiLU}(x)\bigr)"),
        ("p", "Hosila xossalari:"),
        ("ul", [
            "$\\operatorname{SiLU}'(0)=\\sigma(0)=\\tfrac12$ — nolda qiyalik aynan yarim;",
            "$\\operatorname{SiLU}'(x)+\\operatorname{SiLU}'(-x)=1$ — bu $\\operatorname{SiLU}(x)-\\operatorname{SiLU}(-x)=x$ ayniyatning hosilasi;",
            "hosila $x&lt;-1{,}2785$ da (minimumdan chapda) <b>manfiy</b>, eng kichik qiymati $x\\approx-2{,}3994$ da $\\approx-0{,}0998$;",
            "hosila $x&gt;1{,}2785$ da <b>1 dan katta</b> — oldingi banddagi simmetriya bo‘yicha — maksimumi $x\\approx2{,}3994$ da $\\approx1{,}0998$; keyin u 1 ga yuqoridan intiladi.",
        ]),
        ("p", "$\\pm2{,}3994$ nuqtalar $x\\tanh\\frac{x}{2}=2$ tenglamaning ildizlari: u yerda ikkinchi hosila nolga aylanadi"),
        ("eq", r"\operatorname{SiLU}''(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)\Bigl(2-x\tanh\frac{x}{2}\Bigr),\qquad \operatorname{SiLU}''(0)=\frac12"),
        ("viz", "silu-derivative", {"x": 2.3994}, "<b>3-rasm.</b> SiLU hosilasi (to‘q sariq) — $\\sigma(x)$ ventil va $x\\sigma'(x)$ qo‘shiluvchi yig‘indisi. $x=2{,}399$ nuqtada ventil $0{,}9168$, ikkinchi qo‘shiluvchi $0{,}1831$ beradi, birgalikda $1{,}0998$; bu maksimum va bu yerda ikkinchi hosila (pastki grafik) nolga teng. Chapda hosila $-0{,}0998$ gacha tushadi."),
        ("callout", "note", "Nega 1 dan katta hosila — normal holat", "1 dan katta qiyalik $x&gt;1{,}28$ da SiLU nol atrofida ortda qolgan $y=x$ to‘g‘ri chiziqni «quvib yetayotganini» bildiradi. $x&gt;0$ da SiLU chiqishi hech qachon kirishdan oshmaydi ($\\sigma&lt;1$), shuning uchun portlash yo‘q: qiyalik 1 dan biroz katta va tezda 1 ga qaytadi."),
    ]),
    dict(id="compare", title="Silliqlik va qarindoshlar: ReLU va GELU", blocks=[
        ("p", "Bitta grafikda uchta funksiya: ReLU, SiLU va <a href=\"../gelu/\">GELU</a> $=x\\,\\Phi(x)$, bu yerda $\\Phi$ — standart normal taqsimot funksiyasi. Faqat funksiyalarning o‘ziga emas, birinchi va ikkinchi hosilalarga ham qarang: silliqlikdagi farq aynan o‘sha yerda ko‘rinadi."),
        ("viz", "silu-compare", {"view": "f", "x": -1}, "<b>4-rasm.</b> ReLU, SiLU va GELU: funksiyalar, birinchi va ikkinchi hosilalar. $x=-1$ da: SiLU $=-0{,}269$, GELU $=-0{,}159$; birinchi hosilalar $0{,}072$ va $-0{,}083$ (GELU bu nuqtada hali kamayadi, uning minimumi $x\\approx-0{,}752$ da $-0{,}170$); ikkinchi hosilalar $0{,}302$ va $0{,}242$. ReLU’ning ikkinchi hosilasi nolda delta-funksiya: butun egrilik bitta nuqtada to‘plangan."),
        ("ul", [
            "<b>ReLU</b>: birinchi hosila — zina, ikkinchisi — delta-funksiya. Optimizator uchun xato sirti keskin qirrali tekis bo‘laklardan iborat.",
            "<b>SiLU va GELU</b>: hosilalar uzluksiz, ikkinchi hosilalar — maksimumi nolda bo‘lgan silliq «do‘ngliklar» (SiLU’da $0{,}5$, GELU’da $2\\varphi(0)\\approx0{,}798$). Xato landshafti silliq bo‘ladi va gradiyent asta-sekin o‘zgaradi.",
            "<b>GELU ≈ $\\beta=1{,}702$ li Swish</b>: $x\\,\\Phi(x)\\approx x\\,\\sigma(1{,}702x)$, eng katta xato taxminan $0{,}02$. GELU — biroz «tikroq» SiLU: chuqurchasi sayozroq ($-0{,}170$, SiLU’da esa $-0{,}278$), hosila maksimumi yuqoriroq ($1{,}129$, SiLU’da esa $1{,}100$).",
        ]),
        ("h3", "Ehtimollik ma’nosi: tasodifiy ventil"),
        ("p", "SiLU va GELU’ning umumiy tushuntirishi bor. Neyron kirish tasodifiy $\\varepsilon$ shovqindan katta bo‘lsa, uni to‘liq o‘tkazsin, kichik bo‘lsa — butunlay to‘sib qo‘ysin: $y=x\\cdot[\\varepsilon\\le x]$. U holda chiqishning o‘rtacha qiymati"),
        ("eq", r"\mathbb E[y]=x\cdot P(\varepsilon\le x)=x\cdot F_\varepsilon(x)=\begin{cases}x\,\sigma(x)=\operatorname{SiLU}(x), & \varepsilon\sim\text{Logistic}(0,1),\\ x\,\Phi(x)=\operatorname{GELU}(x), & \varepsilon\sim N(0,1).\end{cases}"),
        ("p", "Sigmoida — logistik taqsimot funksiyasi, $\\Phi$ — normal taqsimotniki. Demak, SiLU — «tasodifiy chegarali, o‘rtachalangan ReLU»: neyron aynan nolda kesish o‘rniga nol atrofidagi tasodifiy nuqtada kesadi, o‘rtacha esa silliq egri chiziq hosil bo‘ladi."),
        ("viz", "silu-noise", {"noise": "logistic"}, "<b>5-rasm.</b> «Boshlash»ni bosing. $x$ ning 33 ta qiymati uchun logistik $\\varepsilon$ shovqin tanlanadi va chiqish yo $x$ ga, yo 0 ga teng (punktirlardagi kulrang nuqtalar). To‘q sariq nuqtalar — o‘rtacha chiqishlar; har nuqtada 2000 ta tanlovdan keyin ular SiLU egri chizig‘idan ko‘pi bilan $0{,}031$ ga chetlashadi. Shovqinni normalga almashtiring: o‘rtachalar GELU egri chizig‘ida to‘planadi (chetlanish $0{,}015$)."),
    ]),
    dict(id="swiglu", title="SwiGLU: katta til modellaridagi SiLU", blocks=[
        ("p", "Transformerda e’tibor blokidan keyin to‘liq bog‘langan blok (feed-forward network, FFN) turadi. Klassik varianti — $W_2\\,\\operatorname{ReLU}(W_1x)$ (yoki ReLU o‘rniga GELU). Shazir (2020) uni bir tarmoq ikkinchisidan qanchasini o‘tkazishni hal qiladigan <b>ventilli</b> blok (gated linear unit) bilan almashtirishni taklif qilgan:"),
        ("eq", r"\operatorname{FFN}_{\text{SwiGLU}}(x)=W_2\bigl(\operatorname{SiLU}(W_1x)\odot W_3x\bigr)"),
        ("symbols", [
            (r"x\in\mathbb R^{d}", "$d$ o‘lchamli token vektori (LLaMA-7B da $d=4096$);"),
            (r"W_1x", "ventil tarmog‘i: SiLU orqali qaysi komponentlarni va qanchalik o‘tkazishni hal qiladi;"),
            (r"W_3x", "qiymat tarmog‘i: chiziqli, aktivatsiyasiz — o‘tkaziladigan narsa;"),
            (r"\odot", "$h$ o‘lchamli (yashirin o‘lcham) ikki vektorning elementma-element ko‘paytmasi;"),
            (r"W_2", "$d$ o‘lchamga qaytarish proyeksiyasi."),
        ]),
        ("p", "Bitta komponent uchun bu ikki sonning funksiyasi: $g(a,b)=\\operatorname{SiLU}(a)\\cdot b$, bu yerda $a$ — ventil tarmog‘ining, $b$ — qiymat tarmog‘ining komponenti. Uni 3D’da ko‘rish arziydi."),
        ("viz", "silu-swiglu", {"gate": "silu", "a": 1.5, "b": 2}, "<b>6-rasm.</b> $\\operatorname{SiLU}(a)\\cdot b$ sirti (uni aylantirish mumkin) va yuqoridan ko‘rinish. $a&lt;0$ da ventil deyarli yopiq va sirt istalgan $b$ da deyarli tekis; $a&gt;0$ da u $\\approx a\\cdot b$ «egar»ga aylanadi. $(1{,}5;\\,2)$ nuqtada: ventil $\\operatorname{SiLU}(1{,}5)=1{,}226$, chiqish $2{,}453$, $\\partial/\\partial a=\\operatorname{SiLU}'(1{,}5)\\cdot b=2{,}083$, $\\partial/\\partial b=1{,}226$. Ventilni ReLU, GELU, sigmoidaga almashtiring yoki uni butunlay olib tashlang."),
        ("p", "Bu yerdagi gradiyentlar sodda va ibratli: $\\frac{\\partial g}{\\partial b}=\\operatorname{SiLU}(a)$ — qiymat tarmog‘i ventil qanchalik ochiq bo‘lsa, shunga mutanosib o‘rganadi; $\\frac{\\partial g}{\\partial a}=\\operatorname{SiLU}'(a)\\cdot b$ — ventil faqat u orqali o‘tkazadigan narsa bo‘lsagina o‘rganadi."),
        ("h3", "Nega yashirin o‘lcham 8/3·d"),
        ("p", "SwiGLU’da ikkita o‘rniga uchta matritsa bor. Parametrlar soni $h=4d$ li oddiy FFN’dagidek ($2\\cdot d\\cdot4d=8d^2$) qolishi uchun yashirin o‘lcham $h=\\frac{2}{3}\\cdot4d=\\frac83 d$ gacha kamaytiriladi: u holda $3\\cdot d\\cdot\\frac83d=8d^2$. LLaMA-7B da $\\frac83\\cdot4096\\approx10923$ 256 ga karrali songacha yuqoriga yaxlitlanadi: $h=11008$. Natijada blokka $3\\cdot4096\\cdot11008=135\\,266\\,304$ parametr to‘g‘ri keladi, $h=4d$ li FFN’da esa $134\\,217\\,728$ — atigi $0{,}8\\%$ ko‘p."),
        ("callout", "history", "Bu qayerdan kelgan", "Ventilli chiziqli bloklarni (GLU, $\\sigma(W_1x)\\odot W_3x$) Dofin va boshq. (2017) konvolyutsion til modellari uchun taklif qilgan. Shazir (2020) turli ventilli variantlarni — ReGLU, GEGLU, SwiGLU — taqqoslagan va ularning barchasi oddiy FFN’dan o‘zib ketgan. SwiGLU PaLM (2022), keyin LLaMA (2023) uchun tanlangan va shundan beri ochiq LLM’lar standartiga aylangan: Qwen, Mistral va boshqa ko‘plari."),
    ]),
    dict(id="training", title="O‘qitishdagi SiLU", blocks=[
        ("p", "Silliq aktivatsiya amalda nima bilan yordam beradi? ReLU neyronlaridan iborat tarmoq funksiyani to‘g‘ri chiziq kesmalaridan, SiLU tarmog‘i esa silliq «egilishlar»dan yig‘adi. Agar maqsadli bog‘liqlik silliq bo‘lsa, SiLU neyronlariga uni takrorlash osonroq. Bundan tashqari, SiLU’da gradiyent aynan nolga teng bo‘lmaydi: manfiy kirishda hosila kichik, lekin nol emas va neyron «o‘lmaydi»."),
        ("p", "Tajriba: $1\\to6\\to1$ tarmoq 40 nuqta bo‘yicha $y=\\sin1{,}5x+0{,}3x$ egri chiziqni yaqinlashtiradi. Ikkala tarmoq bir xil vaznlardan boshlaydi va faqat aktivatsiya bilan farqlanadi; o‘qitish — $0{,}03$ qadamli Adam, 2000 qadam."),
        ("viz", "silu-train", {"seed": 1}, "<b>7-rasm.</b> «Boshlash»ni bosing. Ko‘k egri chiziq — SiLU’li tarmoq, qora punktir — ReLU’li. 1-initsializatsiyada 2000 qadamdan keyin SiLU xatosi $0{,}00139$, ReLU’niki — $0{,}00406$, deyarli uch barobar ko‘p. «Neyronlarni ko‘rsatish»ni yoqing: ReLU’da har bir neyron — «burchak», SiLU’da — silliq egilish. Xato grafigidagi kamdan-kam sakrashlar — doimiy qadamli Adam’ning odatiy tebranishlari."),
        ("p", "Bitta ishga tushirish bo‘yicha xulosa chiqarmaslik uchun tajribani sakkizta turli initsializatsiya uchun takrorladik. SiLU sakkiztasining hammasida aniqroq chiqdi, yutuq $1{,}4$ dan $5{,}2$ martagacha. Lekin bu silliq maqsadning xossasi: bo‘lak-chiziqli bog‘liqlikda ReLU yomonroq bo‘lmasligi mumkin. Shuning uchun aktivatsiyani tanlash — empirik masala, katta modellarda u tajriba bilan hal qilinadi."),
        ("callout", "warn", "Silliqlik narxi", "SiLU ReLU’dan qimmatroq: eksponenta (yoki tanh) kerak, teskari o‘tish uchun esa kirishni saqlash kerak. GPU’da bu odatda matritsa ko‘paytirishlari fonida sezilmaydi, lekin mobil qurilmalarda «qattiq» Swish $x\\cdot\\operatorname{ReLU6}(x+3)/6$ — eksponentasiz bo‘lak-polinomial yaqinlashish ishlatiladi."),
    ]),
    dict(id="code", title="Kodda", blocks=[
        ("p", "Sodda <code>x / (1 + np.exp(-x))</code> yozuvi $x=-1000$ da $e^{1000}$ ni hisoblaydi va to‘lib ketish haqida ogohlantiradi (natija baribir $-0$). Sigmoidani $\\tanh$ orqali hisoblash tozaroq: $\\sigma(x)=\\tfrac12(1+\\tanh\\tfrac x2)$ — tangens hech qachon to‘lib ketmaydi."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Kutubxonalardagi nomlar", "PyTorch: <code>nn.SiLU</code>, <code>F.silu</code>. TensorFlow/Keras: <code>tf.nn.silu</code>, <code>activation=\"swish\"</code> ($\\beta=1$ li o‘sha funksiya). Hugging Face konfiguratsiyalarida: <code>hidden_act=\"silu\"</code>. O‘rnatilgan <code>nn.init.calculate_gain</code> SiLU’ni bilmaydi: odatda standart initsializatsiya yoki ReLU uchun initsializatsiya olinadi."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b>«SiLU ReLU kabi manfiy emas».</b> Yo‘q: $x&lt;0$ da u manfiy, minimumi $-0{,}278$. Agar keyin manfiy bo‘lmagan kirish talab qiladigan narsa kelsa (masalan, logarifm yoki ildiz), bu muhim.",
            "<b>«SiLU monoton».</b> Yo‘q: $x\\approx-1{,}278$ dan chapda u kamayadi va hosilasi u yerda manfiy. Butun to‘g‘ri chiziqda teskari funksiyasi yo‘q.",
            "<b>SiLU va GELU’ni chalkashtirish.</b> Bular har xil funksiyalar: $x\\sigma(x)$ va $x\\Phi(x)$. Oldindan o‘qitilgan modelda birini ikkinchisi bilan almashtirib bo‘lmaydi — vaznlar aniq aktivatsiyaga moslangan.",
            "<b>SwiGLU’ning ikkala tarmog‘ida aktivatsiya.</b> SiLU faqat $W_1x$ ventil tarmog‘ida turadi; $W_3x$ qiymat tarmog‘i chiziqli. Ortiqcha aktivatsiya modelni o‘zgartiradi.",
            "<b>SwiGLU’da $4d$ yashirin o‘lcham.</b> Uchta matritsa bilan bu oddiy FFN’dan $1{,}5$ marta ko‘p parametr beradi. Halol taqqoslash uchun $h\\approx\\frac83d$ olinadi.",
            "<b>O‘zi yozilgan yadrolarda <code>exp(-x)</code> li sodda formula</b>: katta manfiy $x$ larda to‘lib ketish va yarim aniqlikda aniqlik yo‘qolishi. <code>F.silu</code> yoki tanh orqali shakldan foydalaning.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘lanishlar", blocks=[
        ("ul", [
            "<a href=\"../sigmoid/\">Sigmoida</a>: SiLU ventili; $\\sigma'=\\sigma(1-\\sigma)$ hosila $\\operatorname{SiLU}'$ ga kiradi.",
            "<a href=\"../relu/\">ReLU</a>: $\\beta\\to\\infty$ da $x\\sigma(\\beta x)$ ning limiti; $\\operatorname{ReLU}-\\operatorname{SiLU}=|x|\\sigma(-|x|)\\le0{,}2785$.",
            "<a href=\"../gelu/\">GELU</a>: $x\\Phi(x)\\approx x\\sigma(1{,}702x)$ — logistik o‘rniga normal shovqinli o‘sha o‘z-o‘zini ventillash.",
            "<a href=\"../leaky-relu/\">Leaky ReLU</a>: manfiy qismni nolga aylantirmaslikning boshqa usuli — silliq chuqurcha o‘rniga $\\alpha x$ to‘g‘ri chiziq.",
            "<a href=\"../tanh/\">tanh</a>: $\\operatorname{SiLU}(x)=\\frac x2\\bigl(1+\\tanh\\frac x2\\bigr)$.",
            "<a href=\"../softmax/\">Softmax</a> va <a href=\"../adam/\">Adam</a>: transformerda SwiGLU’ning qo‘shnilari — e’tibor mexanizmi va bunday modellar o‘qitiladigan optimizator.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $\\operatorname{SiLU}(x)=x\\,\\sigma(x)=\\frac x2\\bigl(1+\\tanh\\frac x2\\bigr)$ — o‘z-o‘zini ventillash: kirish o‘zining qancha ulushini o‘tkazishni hal qiladi. 2) Silliq, nomonoton, minimumi $\\approx-1{,}278$ nuqtada $-W(e^{-1})\\approx-0{,}278$; doim ReLU’dan ko‘pi bilan $0{,}278$ ga pastda. 3) $\\operatorname{SiLU}'=\\sigma(1+x(1-\\sigma))$: nolda $0{,}5$, $x&gt;1{,}278$ da 1 dan katta, maksimumi $\\approx1{,}100$. 4) Swish-β chiziqli funksiya ($\\beta=0$) va ReLU’ni ($\\beta\\to\\infty$) bog‘laydi; GELU $\\approx$ Swish-1,702. 5) Ehtimollik nuqtai nazaridan — tasodifiy logistik chegarali, o‘rtachalangan ReLU. 6) LLM’larda — SwiGLU ventili: $W_2(\\operatorname{SiLU}(W_1x)\\odot W_3x)$, yashirin o‘lcham $\\approx\\frac83d$."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="$\\operatorname{SiLU}(-1)$ taxminan nimaga teng?", options=["$0$", "$-0{,}269$", "$0{,}269$", "$-1$"], answer=1,
                 explain="$\\operatorname{SiLU}(-1)=-1\\cdot\\sigma(-1)=-0{,}2689$: ventil taxminan chorakka ochiq."),
            dict(q="SiLU eng kichik qanday qiymat qabul qiladi?", options=["$0$", "$\\approx-0{,}278$", "$-1$", "Quyidan chegaralanmagan"], answer=1,
                 explain="Minimum $x^*\\approx-1{,}278$ nuqtada, qiymati $x^*+1=-W(e^{-1})\\approx-0{,}278$."),
            dict(q="SiLU’ning noldagi hosilasi nimaga teng?", options=["$0$", "$0{,}25$", "$0{,}5$", "$1$"], answer=2,
                 explain="$\\operatorname{SiLU}'(0)=\\sigma(0)\\bigl(1+0\\bigr)=\\tfrac12$."),
            dict(q="$W_2\\bigl(\\operatorname{SiLU}(W_1x)\\odot W_3x\\bigr)$ SwiGLU blokida nechta vazn matritsasi bor va $W_3x$ tarmog‘ida qanday aktivatsiya?", options=["2 ta matritsa, SiLU", "3 ta matritsa, hech qanday (chiziqli tarmoq)", "3 ta matritsa, sigmoida", "4 ta matritsa, ReLU"], answer=1,
                 explain="Matritsalar $W_1$, $W_2$, $W_3$; $W_3x$ qiymat tarmog‘i chiziqli, SiLU faqat ventil tarmog‘ida turadi."),
            dict(q="$\\beta=0$ da $x\\,\\sigma(\\beta x)$ nimaga aylanadi?", options=["ReLU’ga", "$x/2$ ga", "0 ga", "SiLU’ga"], answer=1,
                 explain="$\\sigma(0)=\\tfrac12$, shuning uchun $x\\,\\sigma(0)=x/2$. $\\beta\\to\\infty$ da esa, aksincha, ReLU hosil bo‘ladi."),
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
