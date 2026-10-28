"""Formula page: Leaky ReLU (and PReLU / RReLU). Format: see README.md, reference page: sigmoid.py."""

META = dict(
    id="leaky-relu",
    date="2026-10-28",
    minutes=30,
    hero=r"\operatorname{LReLU}(x)=\max(\alpha x,\,x)=\begin{cases}x, & x>0\\ \alpha x, & x\le 0\end{cases}",
    title={"ru": "Leaky ReLU: «протекающий» ReLU", "en": "Leaky ReLU: the “leaky” ReLU", "uz": "Leaky ReLU: «oqadigan» ReLU"},
    dek={
        "ru": "ReLU с крошечной поправкой: слева от нуля функция не обнуляет сигнал, а умножает его на маленький α. Разбираем по косточкам, почему этого хватает, чтобы нейроны не умирали, откуда берётся инициализация Хе с множителем 1 + α², как сеть из таких нейронов режет пространство на плоские куски и как PReLU учит α сам.",
        "en": "ReLU with a tiny fix: to the left of zero the function does not zero the signal, it multiplies it by a small α. We take it apart bone by bone: why that is enough to keep neurons alive, where the He initialization with the factor 1 + α² comes from, how a network of such neurons cuts space into flat pieces, and how PReLU learns α by itself.",
        "uz": "Kichik tuzatishli ReLU: noldan chapda funksiya signalni nolga aylantirmaydi, uni kichik α ga ko‘paytiradi. Mayda detallarigacha tahlil qilamiz: nega shu neyronlar o‘lmasligi uchun yetarli, 1 + α² ko‘paytuvchili He initsializatsiyasi qayerdan keladi, bunday neyronlardan iborat tarmoq fazoni qanday tekis bo‘laklarga kesadi va PReLU α ni o‘zi qanday o‘rganadi.",
    },
    description={
        "ru": "Leaky ReLU подробно: формула в трёх записях, производная и субградиент, умирающий ReLU и оживление нейрона, кусочно-линейная сеть в 3D, инициализация Хе для α, PReLU, RReLU, ELU и SELU, код на NumPy и PyTorch.",
        "en": "Leaky ReLU in depth: the formula in three forms, the derivative and subgradient, the dying ReLU and neuron revival, a piecewise-linear network in 3D, He initialization for α, PReLU, RReLU, ELU and SELU, code in NumPy and PyTorch.",
        "uz": "Leaky ReLU batafsil: formulaning uch yozuvi, hosila va subgradiyent, o‘layotgan ReLU va neyronning jonlanishi, 3D’da bo‘lak-chiziqli tarmoq, α uchun He initsializatsiyasi, PReLU, RReLU, ELU va SELU, NumPy va PyTorch’da kod.",
    },
)

# x, LReLU at α = 0.01, LReLU at α = 0.2, derivative
TABLE = [("-5", "-0.05", "-1", "α"), ("-2", "-0.02", "-0.4", "α"), ("-0.5", "-0.005", "-0.1", "α"),
         ("0.5", "0.5", "0.5", "1"), ("2", "2", "2", "1"), ("5", "5", "5", "1")]


def _table(lang):
    dec = "." if lang == "en" else ","
    m = lambda v: v.replace("-", "−").replace(".", dec)
    return [[m(x), m(a), m(b), f"${d}$".replace("α", "\\alpha")] for x, a, b, d in TABLE]


FAMILY = {
    "ru": [["ReLU", "$0$", "$0$", "нулевой градиент, «мёртвые» нейроны"],
           ["Leaky ReLU", "$\\alpha x$", "$\\alpha$", "фиксированный наклон, обычно $0{,}01$–$0{,}3$"],
           ["PReLU", "$\\alpha x$, $\\alpha$ обучается", "$\\alpha$", "+1 параметр на слой или канал"],
           ["RReLU", "$\\alpha x$, $\\alpha\\sim U(\\tfrac18;\\,\\tfrac13)$", "$\\alpha$", "шум как регуляризация"],
           ["ELU", "$\\alpha(e^{x}-1)$", "$\\alpha e^{x}$", "гладкая при $\\alpha=1$, насыщение на $-\\alpha$"],
           ["SELU", "$\\lambda\\alpha(e^{x}-1)$", "$\\lambda\\alpha e^{x}$", "самонормализация, $\\lambda\\approx1{,}0507$"]],
    "en": [["ReLU", "$0$", "$0$", "zero gradient, “dead” neurons"],
           ["Leaky ReLU", "$\\alpha x$", "$\\alpha$", "fixed slope, usually $0.01$–$0.3$"],
           ["PReLU", "$\\alpha x$, $\\alpha$ is learned", "$\\alpha$", "+1 parameter per layer or channel"],
           ["RReLU", "$\\alpha x$, $\\alpha\\sim U(\\tfrac18,\\,\\tfrac13)$", "$\\alpha$", "noise as regularization"],
           ["ELU", "$\\alpha(e^{x}-1)$", "$\\alpha e^{x}$", "smooth for $\\alpha=1$, saturates at $-\\alpha$"],
           ["SELU", "$\\lambda\\alpha(e^{x}-1)$", "$\\lambda\\alpha e^{x}$", "self-normalizing, $\\lambda\\approx1.0507$"]],
    "uz": [["ReLU", "$0$", "$0$", "nol gradiyent, «o‘lik» neyronlar"],
           ["Leaky ReLU", "$\\alpha x$", "$\\alpha$", "qat’iy qiyalik, odatda $0{,}01$–$0{,}3$"],
           ["PReLU", "$\\alpha x$, $\\alpha$ o‘rganiladi", "$\\alpha$", "qatlam yoki kanalga +1 parametr"],
           ["RReLU", "$\\alpha x$, $\\alpha\\sim U(\\tfrac18;\\,\\tfrac13)$", "$\\alpha$", "regulyarizatsiya sifatida shovqin"],
           ["ELU", "$\\alpha(e^{x}-1)$", "$\\alpha e^{x}$", "$\\alpha=1$ da silliq, $-\\alpha$ da to‘yinadi"],
           ["SELU", "$\\lambda\\alpha(e^{x}-1)$", "$\\lambda\\alpha e^{x}$", "o‘z-o‘zini normallashtirish, $\\lambda\\approx1{,}0507$"]],
}

CODE_NUMPY = '''import numpy as np

def leaky_relu(x, alpha=0.01):
    # where, а не maximum(alpha * x, x): эта запись верна при любом alpha
    return np.where(x > 0, x, alpha * x)

def leaky_relu_grad(x, alpha=0.01):
    return np.where(x > 0, 1.0, alpha)      # в нуле берём alpha, как PyTorch

def he_std(n_in, alpha=0.01):
    # инициализация Хе для Leaky ReLU: Var w = 2 / ((1 + alpha²) · n_in)
    return np.sqrt(2.0 / ((1.0 + alpha**2) * n_in))

x = np.array([-3.0, -0.5, 0.0, 2.0])
print(leaky_relu(x))        # [-0.03  -0.005  0.     2.   ]
print(leaky_relu_grad(x))   # [0.01 0.01 0.01 1.  ]
print(he_std(256, 0.2))     # 0.08667...'''

CODE_TORCH = '''import torch
import torch.nn as nn

act = nn.LeakyReLU(negative_slope=0.01)   # 0.01 — значение по умолчанию
x = torch.tensor([-3.0, 0.0, 2.0], requires_grad=True)
act(x).sum().backward()
print(x.grad)                    # tensor([0.0100, 0.0100, 1.0000]) — в нуле α

prelu = nn.PReLU(num_parameters=1, init=0.25)   # α — обучаемый параметр
print(prelu(torch.tensor([-2.0, 3.0])))         # tensor([-0.5000, 3.0000])

lin = nn.Linear(256, 256)
# std = √(2 / ((1 + a²) · 256)); по умолчанию a=0, то есть «как для ReLU»
nn.init.kaiming_normal_(lin.weight, a=0.2, nonlinearity="leaky_relu")
print(nn.init.calculate_gain("leaky_relu", 0.2))  # 1.3867504905630728'''

_CODE_TR = {
    "en": [("where, а не maximum(alpha * x, x): эта запись верна при любом alpha", "where, not maximum(alpha * x, x): this form is correct for any alpha"),
           ("в нуле берём alpha, как PyTorch", "alpha at zero, as in PyTorch"),
           ("инициализация Хе для Leaky ReLU", "He initialization for Leaky ReLU"),
           ("0.01 — значение по умолчанию", "0.01 is the default"), ("— в нуле α", "— α at zero"),
           ("α — обучаемый параметр", "α is a learnable parameter"),
           ("по умолчанию a=0, то есть «как для ReLU»", "the default a=0 means “as for ReLU”")],
    "uz": [("where, а не maximum(alpha * x, x): эта запись верна при любом alpha", "maximum(alpha * x, x) emas, where: bu yozuv istalgan alpha da to‘g‘ri"),
           ("в нуле берём alpha, как PyTorch", "nolda alpha olinadi, PyTorch’dagidek"),
           ("инициализация Хе для Leaky ReLU", "Leaky ReLU uchun He initsializatsiyasi"),
           ("0.01 — значение по умолчанию", "0.01 — standart qiymat"), ("— в нуле α", "— nolda α"),
           ("α — обучаемый параметр", "α — o‘rganiladigan parametr"),
           ("по умолчанию a=0, то есть «как для ReLU»", "standart a=0, ya’ni «ReLU uchun»")],
}


def _code(src, lang):
    for a, b in _CODE_TR.get(lang, []):
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем он нужен", blocks=[
        ("p", "<a href=\"../relu/\">ReLU</a> — самая популярная активация глубокого обучения: $\\max(0,x)$ считается мгновенно, а справа от нуля градиент не затухает. Но у него есть слабое место. Слева от нуля ReLU не приглушает сигнал, а <b>обнуляет</b> его — и вместе с ним градиент. Нейрон, у которого вход отрицателен на всех примерах, выдаёт 0, получает нулевой градиент и больше никогда не учится. Это «умирающий ReLU» (dying ReLU)."),
        ("p", "Leaky ReLU — минимальная поправка: слева от нуля график не горизонтален, а слегка наклонён, $\\alpha x$ с маленьким $\\alpha$ (обычно от $0{,}01$ до $0{,}3$). Сигнал «протекает» сквозь закрытую дверь — отсюда и название (leaky — «протекающий»)."),
        ("p", "Где он встречается:"),
        ("ul", [
            "<b>дискриминаторы GAN</b> — в DCGAN (Рэдфорд и др., 2015) все слои дискриминатора используют Leaky ReLU с $\\alpha=0{,}2$;",
            "<b>детекторы YOLO</b> — сеть Darknet в YOLOv2 и YOLOv3 построена на Leaky ReLU с $\\alpha=0{,}1$;",
            "<b>графовые сети</b> — коэффициенты внимания в GAT считаются через Leaky ReLU с $\\alpha=0{,}2$;",
            "<b>свёрточные сети с PReLU</b> — вариант с обучаемым $\\alpha$ (Хе и др., 2015) помог впервые опустить ошибку top-5 на ImageNet ниже человеческой;",
            "<b>любая сеть, где ReLU «умирает»</b> — замена занимает одну строку и почти ничего не стоит.",
        ]),
        ("callout", "key", "Главное за минуту", "$\\operatorname{LReLU}(x)=x$ при $x&gt;0$ и $\\alpha x$ при $x\\le0$. Производная — ступенька: $1$ справа и $\\alpha$ слева, поэтому градиент никогда не обнуляется целиком. Функция остаётся кусочно-линейной, монотонной и почти такой же дешёвой, как ReLU. При $\\alpha=0$ это ReLU, при $\\alpha=1$ — тождественная функция, при обучаемом $\\alpha$ — PReLU."),
    ]),
    dict(id="intuition", title="Интуиция: дверь, которая не закрывается до конца", blocks=[
        ("p", "ReLU похож на дверь: положительный сигнал проходит целиком, отрицательный упирается в закрытую створку. Leaky ReLU оставляет щель — отрицательный сигнал проходит, но ослабленным в $1/\\alpha$ раз. При $\\alpha=0{,}1$ вход $-2$ превращается в $-0{,}2$."),
        ("p", "Потяните точку по графику. Оранжевый «треугольник наклона» показывает производную: шаг на 1 вдоль оси $x$ меняет значение на $\\alpha$ слева от нуля и на 1 справа. Ниже — сама производная: две горизонтальные ступеньки с разрывом в нуле. Подвигайте ползунок $\\alpha$: от ReLU ($\\alpha=0$) через «протекающий» вариант к прямой $y=x$ ($\\alpha=1$)."),
        ("viz", "leaky-relu-explorer", {"alpha": 0.1, "x": -2}, "<b>Рисунок 1.</b> Leaky ReLU и его производная при $\\alpha=0{,}1$. В точке $x=-2$ значение равно $-0{,}2$, производная — $0{,}1$. Серый пунктир — ReLU, точечная линия — $y=x$. В нуле производная не определена: слева она равна $\\alpha$, справа — 1."),
        ("callout", "intuition", "Что заметить", "Слева график не плоский, но очень пологий: при $\\alpha=0{,}01$ вход $-100$ даёт всего $-1$. Вся нелинейность Leaky ReLU сосредоточена в одной точке — изломе в нуле, где наклон меняется с $\\alpha$ на 1. Выразительная сила сети из таких нейронов берётся именно из этих изломов."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", "Одну и ту же функцию полезно уметь записывать тремя способами — каждый пригодится в своём месте."),
        ("h3", "1. По случаям"),
        ("eq", r"\operatorname{LReLU}_\alpha(x)=\begin{cases}x, & x>0,\\ \alpha x, & x\le 0.\end{cases}"),
        ("symbols", [
            (r"x", "вход нейрона — обычно пре-активация $z=w^\\top h+b$;"),
            (r"\alpha", "наклон отрицательной части, гиперпараметр; обычно $0&lt;\\alpha&lt;1$;"),
            (r"\alpha x", "«протечка»: отрицательный вход не обнуляется, а сжимается в $1/\\alpha$ раз."),
        ]),
        ("p", "В точке $x=0$ обе ветки дают ноль, поэтому неважно, к какой из них отнести ноль: функция непрерывна."),
        ("h3", "2. Через максимум"),
        ("eq", r"\operatorname{LReLU}_\alpha(x)=\max(\alpha x,\;x)\qquad(\alpha\le 1)"),
        ("p", "При $x&gt;0$ и $\\alpha\\le1$ выполняется $x\\ge\\alpha x$, а при $x&lt;0$ — наоборот, $\\alpha x\\ge x$. Значит, максимум сам выбирает нужную ветку. Но только при $\\alpha\\le1$: при $\\alpha=2$ справа победит $2x$, и получится другая функция. Запись удобна в коде (<code>np.maximum(alpha * x, x)</code>), но про условие легко забыть."),
        ("h3", "3. Линейная часть плюс модуль"),
        ("eq", r"\operatorname{LReLU}_\alpha(x)=\frac{1+\alpha}{2}\,x+\frac{1-\alpha}{2}\,|x|"),
        ("p", "Проверка: при $x&gt;0$ получаем $\\frac{1+\\alpha}{2}x+\\frac{1-\\alpha}{2}x=x$, при $x&lt;0$ — $\\frac{1+\\alpha}{2}x-\\frac{1-\\alpha}{2}x=\\alpha x$. Эта форма верна при любом $\\alpha$ и объясняет главное: Leaky ReLU — это линейная функция плюс «немного модуля». Вся нелинейность сидит во втором слагаемом, и её доля $\\frac{1-\\alpha}{2}$ уменьшается с ростом $\\alpha$. При $\\alpha=1$ нелинейность исчезает полностью."),
        ("viz", "leaky-relu-parts", {"alpha": 0.2}, "<b>Рисунок 2.</b> Слева — Leaky ReLU как верхняя огибающая двух прямых $y=x$ и $y=\\alpha x$. Сдвиньте $\\alpha$ выше 1: огибающая (чёрный пунктир) отрывается от настоящего Leaky ReLU (синяя линия). Справа — разложение на линейную часть и модуль; при $\\alpha=0{,}2$ коэффициенты равны $0{,}6$ и $0{,}4$."),
        ("table", ["$x$", "$\\alpha=0{,}01$", "$\\alpha=0{,}2$", "$\\operatorname{LReLU}'(x)$"], "TABLE", {"num": [0, 1, 2, 3]}),
        ("p", "Справа от нуля все варианты совпадают с ReLU; они различаются только тем, сколько отрицательного сигнала «протекает»."),
    ]),
    dict(id="properties", title="Свойства", blocks=[
        ("ul", [
            "<b>Область определения и значений</b> — вся числовая прямая $\\mathbb R$ (при $\\alpha&gt;0$). У ReLU значения только $[0;\\,+\\infty)$.",
            "<b>Непрерывность и кусочная линейность</b>: две прямые, склеенные в нуле. Функция дифференцируема везде, кроме $x=0$.",
            "<b>Строгая монотонность</b> при $\\alpha&gt;0$: больший вход даёт больший выход. Поэтому функция обратима: $\\operatorname{LReLU}_\\alpha^{-1}(y)=y$ при $y&gt;0$ и $y/\\alpha$ при $y\\le0$, то есть $\\operatorname{LReLU}_{1/\\alpha}$. У ReLU обратной нет: все отрицательные входы склеены в ноль.",
            "<b>Положительная однородность</b>: $\\operatorname{LReLU}(cx)=c\\,\\operatorname{LReLU}(x)$ при $c\\ge0$. Масштаб входа просто переносится на выход — отсюда простые формулы инициализации.",
            "<b>Липшицевость</b> с константой $\\max(1,\\alpha)$, то есть 1 при $\\alpha\\le1$: $|\\operatorname{LReLU}(a)-\\operatorname{LReLU}(b)|\\le|a-b|$.",
            "<b>Неограниченность</b> сверху и снизу, но вниз функция растёт в $1/\\alpha$ раз медленнее.",
            "<b>Частные случаи</b>: $\\alpha=0$ — ReLU, $\\alpha=1$ — тождественная функция, $\\alpha=-1$ — модуль $|x|$ (уже не монотонный).",
        ]),
        ("h3", "Среднее и разброс выхода"),
        ("p", "Пусть вход нейрона $z\\sim N(0,1)$. Тогда"),
        ("eq", r"\mathbb E\bigl[\operatorname{LReLU}(z)\bigr]=\frac{1-\alpha}{\sqrt{2\pi}},\qquad \mathbb E\bigl[\operatorname{LReLU}(z)^2\bigr]=\frac{1+\alpha^2}{2}"),
        ("p", "При $\\alpha=0{,}01$ среднее равно $0{,}395$ (у ReLU — $0{,}399$), при $\\alpha=0{,}2$ — $0{,}319$. Чем больше $\\alpha$, тем ближе выходы к нулевому среднему; это немного облегчает обучение следующего слоя. Второй момент $\\frac{1+\\alpha^2}{2}$ понадобится в разделе об инициализации."),
        ("deep", "Откуда эти формулы", [
            ("p", "Для $z\\sim N(0,1)$ известно, что $\\mathbb E[z\\,\\mathbf 1_{z&gt;0}]=\\varphi(0)=1/\\sqrt{2\\pi}$, а по симметрии $\\mathbb E[z\\,\\mathbf 1_{z&lt;0}]=-1/\\sqrt{2\\pi}$. Поэтому"),
            ("eq", r"\mathbb E[\operatorname{LReLU}(z)]=\mathbb E[z\mathbf 1_{z>0}]+\alpha\,\mathbb E[z\mathbf 1_{z<0}]=\frac{1}{\sqrt{2\pi}}-\frac{\alpha}{\sqrt{2\pi}}"),
            ("p", "Аналогично $\\mathbb E[z^2\\mathbf 1_{z&gt;0}]=\\mathbb E[z^2\\mathbf 1_{z&lt;0}]=\\tfrac12$, откуда $\\mathbb E[\\operatorname{LReLU}(z)^2]=\\tfrac12+\\tfrac{\\alpha^2}{2}$. Вторая формула верна для любого симметричного распределения с единичной дисперсией, первая — только для нормального."),
        ]),
    ]),
    dict(id="derivative", title="Производная: ступенька вместо обрыва", blocks=[
        ("p", "На каждой ветке функция линейна, поэтому производная — просто наклон ветки:"),
        ("eq", r"\operatorname{LReLU}'_\alpha(x)=\begin{cases}1, & x>0,\\ \alpha, & x<0.\end{cases}"),
        ("deep", "Вывод по определению", [
            ("p", "При $x&gt;0$ для достаточно малых $h$ точка $x+h$ тоже положительна, и $\\frac{\\operatorname{LReLU}(x+h)-\\operatorname{LReLU}(x)}{h}=\\frac{(x+h)-x}{h}=1$. При $x&lt;0$ так же получаем $\\frac{\\alpha(x+h)-\\alpha x}{h}=\\alpha$."),
            ("p", "В нуле односторонние пределы разные:"),
            ("eq", r"\lim_{h\to0^+}\frac{\operatorname{LReLU}(h)-0}{h}=1,\qquad \lim_{h\to0^-}\frac{\alpha h-0}{h}=\alpha"),
            ("p", "При $\\alpha\\ne1$ они не совпадают, поэтому производной в нуле нет — это точка излома."),
        ]),
        ("p", "Что делать с нулём на практике? В точке излома есть <b>субградиент</b> (subgradient): при $0\\le\\alpha\\le1$ любое число $g\\in[\\alpha;\\,1]$ задаёт прямую $y=gx$, которая лежит не выше графика. Библиотеки выбирают одно значение по соглашению — в PyTorch при $x=0$ берётся $\\alpha$. Точно в ноль вход попадает редко, так что выбор почти ни на что не влияет."),
        ("h3", "Почему ступенька лучше обрыва"),
        ("p", "По цепному правилу градиент по весу $w_j$ нейрона $a=\\operatorname{LReLU}(z)$, $z=\\sum_j w_jx_j+b$, равен"),
        ("eq", r"\frac{\partial L}{\partial w_j}=\frac{\partial L}{\partial a}\cdot\operatorname{LReLU}'(z)\cdot x_j"),
        ("p", "У ReLU средний множитель равен 0 при $z&lt;0$, у Leaky ReLU — $\\alpha$. Слева градиент в $1/\\alpha$ раз слабее, но не равен нулю: нейрон, «застрявший» в отрицательной зоне, продолжает получать сигнал об ошибке."),
        ("h3", "Производная по α: шаг к PReLU"),
        ("p", "Если сделать $\\alpha$ обучаемым параметром, понадобится производная по нему. Она тоже простая:"),
        ("eq", r"\frac{\partial\operatorname{LReLU}_\alpha(x)}{\partial\alpha}=\begin{cases}0, & x>0,\\ x, & x\le 0\end{cases}\;=\;\min(0,\,x)"),
        ("p", "Наклон $\\alpha$ учится только на примерах, попавших в левую ветку, — так устроен PReLU (раздел 9). Вторая производная по $x$ равна нулю везде, кроме нуля: вся кривизна сосредоточена в изломе, и в смысле обобщённых функций $\\operatorname{LReLU}''(x)=(1-\\alpha)\\,\\delta(x)$."),
    ]),
    dict(id="dying", title="Умирающий ReLU и как Leaky его лечит", blocks=[
        ("p", "Как умирает нейрон. Пусть после неудачного большого шага (слишком большой темп обучения, выброс в данных, неудачная инициализация) сдвиг $b$ нейрона стал сильно отрицательным. Тогда $z=w^\\top x+b&lt;0$ на всех примерах, ReLU выдаёт 0, производная $\\operatorname{ReLU}'(z)=0$ — и градиенты по $w$, $b$ и по выходному весу $v$ обнуляются одновременно. Градиентный спуск больше никогда не сдвинет этот нейрон: он мёртв. В конспектах курса CS231n отмечают, что при слишком большом темпе обучения мёртвой может оказаться до 40% сети."),
        ("p", "Ниже — самый чистый эксперимент. Один нейрон $f(x)=v\\cdot\\operatorname{act}(wx+b)$ должен выучить «шарнир» $y=1{,}5\\max(0,\\,x-1)$ по 41 точке отрезка $[-3;\\,3]$. Старт: $w=1$, $b=-4$, $v=1$ — излом в точке $x=4$, за пределами данных, поэтому на всех примерах $z&lt;0$. Обучение — градиентный спуск по MSE с шагом $0{,}1$."),
        ("viz", "leaky-relu-revive", {"alpha": 0.1}, "<b>Рисунок 3.</b> Нажмите «Пуск». Нейрон ReLU (чёрный пунктир) заморожен: все его градиенты равны нулю, и ошибка навсегда остаётся $1{,}09$. Нейрон Leaky ReLU с $\\alpha=0{,}1$ получает слабый градиент, его прямая наклоняется и сдвигается, и на 24-м шаге излом входит в область данных. Через 1500 шагов ошибка равна $0{,}0549$. При $\\alpha=0{,}01$ оживление занимает 135 шагов, зато итоговая ошибка — $0{,}00082$."),
        ("p", "Обратите внимание на компромисс. Большой $\\alpha$ быстро возвращает нейрон к жизни, но левая ветка остаётся наклонной: при $\\alpha=0{,}1$ итоговая модель слева имеет наклон $\\alpha v w\\approx0{,}116$ вместо нуля, отсюда остаточная ошибка. Маленький $\\alpha$ почти не искажает форму функции, но оживляет медленнее."),
        ("callout", "warn", "Leaky — не гарантия", "Ненулевой градиент не означает, что нейрон обязательно вернётся: он может так и остаться на левой ветке, работая как линейная функция $\\alpha(w^\\top x+b)$. Leaky ReLU гарантирует другое — нейрон никогда не замерзает намертво и продолжает учиться. Против самой причины гибели помогают умеренный темп обучения, разогрев (warmup), нормализация и правильная инициализация."),
    ]),
    dict(id="space", title="Сеть из Leaky ReLU: кусочно-линейный рельеф", blocks=[
        ("p", "В сети с двумя входами каждый нейрон $\\operatorname{LReLU}(w_k^\\top x+b_k)$ «сгибает» плоскость вдоль прямой $w_k^\\top x+b_k=0$: по одну сторону от неё наклон в $1/\\alpha$ раз меньше, чем по другую. Сумма нейронов $f(x)=\\sum_k v_k\\operatorname{LReLU}(w_k^\\top x+b_k)$ — многогранная поверхность: внутри каждой области, где набор включённых нейронов не меняется, она плоская, а на прямых-изломах меняет наклон."),
        ("viz", "leaky-relu-surface", {"alpha": 0.1}, "<b>Рисунок 4.</b> Сеть из шести нейронов Leaky ReLU. Слева — поверхность $f(x_1,x_2)$ в 3D (её можно вращать), справа — вид сверху с шестью прямыми изломов. Они делят квадрат $[-3;\\,3]^2$ на 19 линейных областей. Тяните оранжевую точку: в центре, в точке $(0{,}2;\\,-0{,}3)$, выключены все шесть нейронов, но градиент не нулевой: $|\\nabla f|=0{,}100$. Поставьте $\\alpha=0$: центральная область станет плоской — это 5% квадрата, где у сети из ReLU градиент по входу равен нулю. При $\\alpha=1$ вся сеть превращается в одну плоскость."),
        ("p", "Число областей не зависит от $\\alpha$ (пока $\\alpha\\ne1$): его задают только прямые изломов. Зато от $\\alpha$ зависит, что происходит там, где все нейроны выключены. У ReLU там плато с нулевым градиентом, и примеры, попавшие на него, ничего не сообщают сети. У Leaky ReLU плато наклонено, и градиент там, как правило, не нулевой."),
        ("callout", "note", "Сколько областей может быть", "$n$ прямых общего положения делят плоскость не более чем на $1+n+\\binom n2$ частей: для $n=6$ это 22. В квадрате на рисунке видно 19 из них. У глубоких сетей число линейных областей может расти с глубиной экспоненциально — это одно из объяснений их выразительной силы."),
    ]),
    dict(id="depth", title="Глубокие сети: инициализация Хе для Leaky ReLU", blocks=[
        ("p", "В глубокой сети сигнал проходит через десятки слоёв $z_{l+1}=W_{l+1}\\operatorname{LReLU}(z_l)$. Если на каждом слое дисперсия умножается на число, хоть немного отличное от 1, через 50 слоёв это превратится во взрыв или исчезновение сигнала. Посчитаем этот множитель."),
        ("deep", "Вывод множителя", [
            ("p", "Пусть веса $W_{ij}$ независимы, $\\mathbb E W_{ij}=0$, $\\operatorname{Var}W_{ij}=s^2$, а входы $z_l$ симметричны относительно нуля. Для одного выхода $z_{l+1,i}=\\sum_{j=1}^{n}W_{ij}h_j$, где $h_j=\\operatorname{LReLU}(z_{l,j})$:"),
            ("eq", r"\operatorname{Var}z_{l+1}=n\,s^2\,\mathbb E[h^2]=n\,s^2\,\frac{1+\alpha^2}{2}\operatorname{Var}z_l"),
            ("p", "Последнее равенство — второй момент из раздела о свойствах: половина $z_l^2$ приходит с положительной ветки целиком, половина — с отрицательной, умноженная на $\\alpha^2$. Чтобы дисперсия сохранялась, множитель должен быть равен 1:"),
            ("eq", r"s^2=\frac{2}{(1+\alpha^2)\,n_{\text{in}}}\qquad\Longleftrightarrow\qquad g=\sqrt n\,s=\sqrt{\frac{2}{1+\alpha^2}}"),
            ("p", "На обратном проходе градиент умножается на $W^\\top$ и на $\\operatorname{LReLU}'(z)$, а $\\mathbb E[\\operatorname{LReLU}'(z)^2]=\\frac{1+\\alpha^2}{2}$ — тот же множитель. Поэтому одна и та же инициализация сохраняет и прямой сигнал, и градиенты."),
        ]),
        ("eq", r"\operatorname{Var}z_{l+1}=\frac{g^2(1+\alpha^2)}{2}\,\operatorname{Var}z_l,\qquad g_{\text{He}}=\sqrt{\frac{2}{1+\alpha^2}}"),
        ("p", "При $\\alpha=0$ получается знаменитое $g=\\sqrt2$ инициализации Хе (Kaiming) для ReLU. Для Leaky ReLU коэффициент чуть меньше: $1{,}414$ при $\\alpha=0{,}01$, $1{,}387$ при $\\alpha=0{,}2$, $1{,}355$ при $\\alpha=0{,}3$."),
        ("viz", "leaky-relu-init", {"alpha": 0.3, "depth": 50}, "<b>Рисунок 5.</b> RMS пре-активаций на каждом слое случайной сети ширины 256 (вертикальная шкала логарифмическая). По умолчанию $\\alpha=0{,}3$, а веса инициализированы «как для ReLU», $g=\\sqrt2$: множитель дисперсии равен $1{,}09$ за слой, и к 50-му слою RMS вырастает до $11{,}6$ (теория — $11{,}7$). С правильным $g=\\sqrt{2/(1+\\alpha^2)}$ множитель равен 1, и на 50-м слое RMS равен $1{,}34$ (теория — $1{,}35$). При $g=1$ множитель $0{,}545$, и сигнал гаснет до $3{,}45\\cdot10^{-7}$."),
        ("callout", "note", "В PyTorch", "Ровно это делает <code>nn.init.kaiming_normal_(w, a=alpha, nonlinearity='leaky_relu')</code>: стандартное отклонение $\\sqrt{2/((1+a^2)\\,n_{\\text{in}})}$. По умолчанию там <code>a=0</code>, то есть инициализация для обычного ReLU, — для Leaky ReLU параметр <code>a</code> нужно передать явно."),
    ]),
    dict(id="family", title="PReLU, RReLU и вся семья", blocks=[
        ("p", "Как выбрать $\\alpha$? Есть три ответа."),
        ("ul", [
            "<b>Фиксированный $\\alpha$</b> — классический Leaky ReLU (Маас, Ханнун, Ын, 2013, $\\alpha=0{,}01$). Сегодня часто берут $0{,}1$–$0{,}3$: в сравнении Сюй и др. (2015) «сильно протекающий» вариант с $\\alpha=1/5{,}5\\approx0{,}18$ работал лучше, чем $0{,}01$.",
            "<b>Обучаемый $\\alpha$</b> — PReLU (Parametric ReLU, Хе и др., 2015). $\\alpha$ становится параметром — один на слой или по одному на канал — и учится градиентным спуском вместе с весами. Начальное значение в PyTorch — $0{,}25$.",
            "<b>Случайный $\\alpha$</b> — RReLU (Randomized ReLU): при обучении $\\alpha$ для каждого примера берётся из равномерного распределения $U(1/8;\\,1/3)$ (границы по умолчанию в PyTorch), при выводе — среднее $\\frac{1/8+1/3}{2}=\\frac{11}{48}\\approx0{,}229$. Шум действует как регуляризация.",
        ]),
        ("p", "У PReLU градиент по $\\alpha$ — это $\\min(0,\\,z)$ из раздела о производной: наклон учится только на отрицательных входах. Посмотрим, как градиентный спуск находит сразу и вес, и наклон."),
        ("viz", "leaky-relu-prelu", {"w": 0.5, "a": 1.3}, "<b>Рисунок 6.</b> Модель $\\operatorname{PReLU}_\\alpha(wx)$ с двумя параметрами учится на 31 точке, сгенерированной «учителем» $w^*=1{,}5$, $\\alpha^*=0{,}2$ с шумом. Справа — поверхность ошибки $L(w,\\alpha)$ (чем светлее, тем меньше). Из старта $(0{,}5;\\,1{,}3)$ градиентный спуск с шагом $0{,}05$ за 87 шагов приходит в $w=1{,}521$, $\\alpha=0{,}209$ с ошибкой $0{,}0158$ — это минимум для этих зашумлённых данных (у самого учителя ошибка $0{,}0170$). Перетащите старт в другое место."),
        ("p", "PReLU добавляет всего по одному параметру на канал, но в работе Хе и др. он вместе с новой инициализацией позволил обучить очень глубокие свёрточные сети и получить ошибку top-5 $4{,}94\\%$ на ImageNet — ниже оценки человеческой ошибки $5{,}1\\%$. Авторы отмечают, что к $\\alpha$ не стоит применять затухание весов (weight decay): оно тянет $\\alpha$ к нулю, то есть обратно к ReLU."),
        ("h3", "Гладкие родственники"),
        ("p", "Излом в нуле можно сгладить. ELU заменяет левую прямую экспонентой $\\alpha(e^x-1)$, которая насыщается на уровне $-\\alpha$. SELU добавляет масштаб: $\\lambda\\approx1{,}0507$ и $\\alpha\\approx1{,}6733$ подобраны так, чтобы активации сами поддерживали нулевое среднее и единичную дисперсию. <a href=\"../gelu/\">GELU</a> и <a href=\"../silu/\">SiLU</a> — гладкие и даже немонотонные функции, которые сегодня стоят в трансформерах."),
        ("viz", "leaky-relu-zoo", {"cmp": "elu", "x": -2}, "<b>Рисунок 7.</b> Leaky ReLU с $\\alpha=0{,}1$ рядом с родственниками. Наведите курсор: при $x=-2$ Leaky ReLU даёт $-0{,}2$, ELU — $-0{,}865$, SELU — $-1{,}520$, GELU — $-0{,}046$, SiLU — $-0{,}238$. Переключитесь на производные: у Leaky ReLU и SELU это ступенька с разрывом в нуле (у SELU слева $\\lambda\\alpha\\approx1{,}758$, справа $\\lambda\\approx1{,}051$), у ELU, GELU и SiLU — непрерывная кривая."),
        ("table", ["Функция", "При $x\\le0$", "Производная слева", "Особенность"], "FAMILY", {}),
    ]),
    dict(id="code", title="В коде", blocks=[
        ("p", "В NumPy Leaky ReLU — одна строка. Надёжнее писать <code>np.where</code>, чем <code>np.maximum(alpha * x, x)</code>: вторая запись тихо ломается при $\\alpha&gt;1$."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Значения по умолчанию в библиотеках разные", "PyTorch <code>nn.LeakyReLU</code>: <code>negative_slope=0.01</code>. TensorFlow <code>tf.nn.leaky_relu</code>: <code>alpha=0.2</code>. Keras <code>layers.LeakyReLU</code>: $0{,}3$. Одна и та же «Leaky ReLU» в трёх фреймворках — три разные функции. При переносе модели указывайте $\\alpha$ явно."),
        ("p", "С численной точки зрения Leaky ReLU безопасен: ни экспонент, ни деления, ни переполнений. Единственная тонкость — <code>inplace=True</code> в PyTorch: он экономит память, но перезаписывает вход, который может понадобиться другим операциям графа."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>Запись <code>max(alpha * x, x)</code> при $\\alpha&gt;1$.</b> Формула верна только при $\\alpha\\le1$; при больших $\\alpha$ получается другая функция. Безопасная запись — <code>where(x &gt; 0, x, alpha * x)</code>.",
            "<b>Слишком большой $\\alpha$.</b> При $\\alpha\\to1$ доля нелинейности $\\frac{1-\\alpha}{2}$ стремится к нулю, функция становится почти линейной, и глубокая сеть теряет выразительность. Разумный диапазон — от $0{,}01$ до $0{,}3$.",
            "<b>Инициализация «как для ReLU» без поправки на $\\alpha$.</b> Множитель дисперсии $1+\\alpha^2$ за слой: при $\\alpha=0{,}3$ за 50 слоёв сигнал вырастает примерно в 8 раз (рисунок 5). Передавайте $\\alpha$ в <code>kaiming_normal_(..., a=alpha)</code>.",
            "<b>Надежда, что Leaky ReLU сам вылечит нестабильное обучение.</b> Он убирает нулевой градиент, но не причину: слишком большой темп обучения по-прежнему опасен.",
            "<b>Затухание весов на $\\alpha$ у PReLU.</b> Оно тянет $\\alpha$ к нулю, и PReLU превращается в ReLU. Исключайте $\\alpha$ из группы параметров с weight decay.",
            "<b>Разные значения по умолчанию</b> в PyTorch ($0{,}01$), TensorFlow ($0{,}2$) и Keras ($0{,}3$): при переносе модели между фреймворками результат молча меняется.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../relu/\">ReLU</a>: частный случай $\\alpha=0$; там же — подробнее об «умирающем ReLU».",
            "<a href=\"../silu/\">SiLU / Swish</a> и <a href=\"../gelu/\">GELU</a>: гладкие активации, у которых слева тоже проходит небольшой отрицательный сигнал, но затем он гаснет.",
            "<a href=\"../sigmoid/\">Сигмоида</a> и <a href=\"../tanh/\">tanh</a>: насыщающиеся активации; у Leaky ReLU насыщения нет вовсе, а значит, нет и затухания градиента из-за насыщения.",
            "<a href=\"../mse/\">MSE</a>: функция потерь в экспериментах на рисунках 3 и 6.",
            "<a href=\"../sgd/\">SGD</a> и <a href=\"../adam/\">Adam</a>: слишком большой шаг оптимизатора — главная причина гибели ReLU-нейронов.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $\\operatorname{LReLU}_\\alpha(x)=x$ при $x&gt;0$ и $\\alpha x$ при $x\\le0$; это $\\max(\\alpha x,x)$ при $\\alpha\\le1$ и $\\frac{1+\\alpha}{2}x+\\frac{1-\\alpha}{2}|x|$ при любом $\\alpha$. 2) Производная — ступенька из $\\alpha$ и $1$: градиент не обнуляется, нейрон не замерзает. 3) Компромисс: больший $\\alpha$ быстрее оживляет нейроны, но приближает функцию к линейной. 4) Сеть из Leaky ReLU — кусочно-линейная функция без плоских «мёртвых» плато. 5) Инициализация: $\\operatorname{Var}w=\\frac{2}{(1+\\alpha^2)\\,n_{\\text{in}}}$. 6) PReLU учит $\\alpha$ по градиенту $\\min(0,z)$."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="Чему равно $\\operatorname{LReLU}(-5)$ при $\\alpha=0{,}2$?", options=["$0$", "$-1$", "$-5$", "$1$"], answer=1,
                 explain="Вход отрицательный, поэтому работает ветка $\\alpha x=0{,}2\\cdot(-5)=-1$."),
            dict(q="Чему равна производная Leaky ReLU при $x&lt;0$?", options=["$0$", "$1$", "$\\alpha$", "$\\alpha x$"], answer=2,
                 explain="Слева функция — прямая $\\alpha x$, её наклон равен $\\alpha$. Поэтому градиент не обнуляется."),
            dict(q="При каких $\\alpha$ верно $\\operatorname{LReLU}_\\alpha(x)=\\max(\\alpha x,x)$?", options=["При любом $\\alpha$", "Только при $\\alpha\\le1$", "Только при $\\alpha&gt;1$", "Только при $\\alpha=0{,}01$"], answer=1,
                 explain="При $\\alpha\\le1$ справа $x\\ge\\alpha x$, слева $\\alpha x\\ge x$. При $\\alpha&gt;1$ справа максимум выберет $\\alpha x$ — получится другая функция."),
            dict(q="Сеть с Leaky ReLU ($\\alpha=0{,}3$) инициализирована «как для ReLU», $g=\\sqrt2$. Каков множитель дисперсии за слой?", options=["$1$", "$1{,}09$", "$0{,}545$", "$2$"], answer=1,
                 explain="$g^2(1+\\alpha^2)/2=2\\cdot1{,}09/2=1{,}09$. За 50 слоёв RMS вырастает примерно в $1{,}09^{24{,}5}\\approx8{,}3$ раза."),
            dict(q="Нейрон ReLU получает $z&lt;0$ на всех примерах. Что верно?", options=["Градиенты по его параметрам равны нулю, и градиентный спуск его больше не изменит", "Градиент маленький, но не нулевой", "Нейрон выдаёт отрицательные значения", "Достаточно уменьшить темп обучения, и он оживёт"], answer=0,
                 explain="$\\operatorname{ReLU}'(z)=0$ при $z&lt;0$, поэтому все градиенты обнуляются — это мёртвый нейрон. Уменьшение шага тут не поможет: шаг, умноженный на ноль, остаётся нулём."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "<a href=\"../relu/\">ReLU</a> is the most popular activation in deep learning: $\\max(0,x)$ is instant to compute, and to the right of zero the gradient does not vanish. But it has a weak spot. To the left of zero ReLU does not dampen the signal, it <b>zeroes</b> it — and the gradient with it. A neuron whose input is negative on every example outputs 0, receives a zero gradient and never learns again. This is the “dying ReLU”."),
        ("p", "Leaky ReLU is the minimal fix: to the left of zero the graph is not horizontal but slightly tilted, $\\alpha x$ with a small $\\alpha$ (usually from $0.01$ to $0.3$). The signal “leaks” through the closed door — hence the name."),
        ("p", "Where it appears:"),
        ("ul", [
            "<b>GAN discriminators</b> — in DCGAN (Radford et al., 2015) every discriminator layer uses Leaky ReLU with $\\alpha=0.2$;",
            "<b>YOLO detectors</b> — the Darknet network of YOLOv2 and YOLOv3 is built on Leaky ReLU with $\\alpha=0.1$;",
            "<b>graph networks</b> — the attention coefficients in GAT are computed through Leaky ReLU with $\\alpha=0.2$;",
            "<b>convolutional networks with PReLU</b> — the variant with a learnable $\\alpha$ (He et al., 2015) helped push the ImageNet top-5 error below the human level for the first time;",
            "<b>any network where ReLU “dies”</b> — the swap is one line and costs almost nothing.",
        ]),
        ("callout", "key", "The essentials in a minute", "$\\operatorname{LReLU}(x)=x$ for $x&gt;0$ and $\\alpha x$ for $x\\le0$. The derivative is a step: $1$ on the right and $\\alpha$ on the left, so the gradient never vanishes completely. The function stays piecewise linear, monotonic and almost as cheap as ReLU. With $\\alpha=0$ it is ReLU, with $\\alpha=1$ the identity, with a learnable $\\alpha$ it is PReLU."),
    ]),
    dict(id="intuition", title="Intuition: a door that never closes completely", blocks=[
        ("p", "ReLU is like a door: a positive signal passes through in full, a negative one hits the closed leaf. Leaky ReLU leaves a gap — the negative signal gets through, but weakened $1/\\alpha$ times. With $\\alpha=0.1$ the input $-2$ becomes $-0.2$."),
        ("p", "Drag the point along the graph. The orange “slope triangle” shows the derivative: one step of 1 along $x$ changes the value by $\\alpha$ to the left of zero and by 1 to the right. Below is the derivative itself: two horizontal steps with a jump at zero. Move the $\\alpha$ slider: from ReLU ($\\alpha=0$) through the leaky variant to the line $y=x$ ($\\alpha=1$)."),
        ("viz", "leaky-relu-explorer", {"alpha": 0.1, "x": -2}, "<b>Figure 1.</b> Leaky ReLU and its derivative at $\\alpha=0.1$. At $x=-2$ the value is $-0.2$ and the derivative is $0.1$. The grey dashed line is ReLU, the dotted line is $y=x$. At zero the derivative is undefined: it equals $\\alpha$ on the left and 1 on the right."),
        ("callout", "intuition", "What to notice", "On the left the graph is not flat, just very shallow: with $\\alpha=0.01$ the input $-100$ gives only $-1$. All the nonlinearity of Leaky ReLU sits at one point — the kink at zero, where the slope switches from $\\alpha$ to 1. The expressive power of a network of such neurons comes precisely from these kinks."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("p", "It pays to be able to write the same function in three ways — each one is useful in its own place."),
        ("h3", "1. By cases"),
        ("eq", r"\operatorname{LReLU}_\alpha(x)=\begin{cases}x, & x>0,\\ \alpha x, & x\le 0.\end{cases}"),
        ("symbols", [
            (r"x", "the neuron’s input — usually the pre-activation $z=w^\\top h+b$;"),
            (r"\alpha", "the slope of the negative part, a hyperparameter; usually $0&lt;\\alpha&lt;1$;"),
            (r"\alpha x", "the “leak”: a negative input is not zeroed but shrunk $1/\\alpha$ times."),
        ]),
        ("p", "At $x=0$ both branches give zero, so it does not matter which branch zero belongs to: the function is continuous."),
        ("h3", "2. Through the maximum"),
        ("eq", r"\operatorname{LReLU}_\alpha(x)=\max(\alpha x,\;x)\qquad(\alpha\le 1)"),
        ("p", "For $x&gt;0$ and $\\alpha\\le1$ we have $x\\ge\\alpha x$, and for $x&lt;0$ the opposite, $\\alpha x\\ge x$. So the maximum picks the right branch by itself. But only when $\\alpha\\le1$: with $\\alpha=2$ the term $2x$ wins on the right, and you get a different function. This form is handy in code (<code>np.maximum(alpha * x, x)</code>), but the condition is easy to forget."),
        ("h3", "3. A linear part plus the absolute value"),
        ("eq", r"\operatorname{LReLU}_\alpha(x)=\frac{1+\alpha}{2}\,x+\frac{1-\alpha}{2}\,|x|"),
        ("p", "Check: for $x&gt;0$ we get $\\frac{1+\\alpha}{2}x+\\frac{1-\\alpha}{2}x=x$, for $x&lt;0$ — $\\frac{1+\\alpha}{2}x-\\frac{1-\\alpha}{2}x=\\alpha x$. This form holds for any $\\alpha$ and explains the main point: Leaky ReLU is a linear function plus “a bit of absolute value”. All the nonlinearity lives in the second term, and its share $\\frac{1-\\alpha}{2}$ shrinks as $\\alpha$ grows. At $\\alpha=1$ the nonlinearity disappears completely."),
        ("viz", "leaky-relu-parts", {"alpha": 0.2}, "<b>Figure 2.</b> On the left, Leaky ReLU as the upper envelope of the two lines $y=x$ and $y=\\alpha x$. Move $\\alpha$ above 1: the envelope (black dashes) breaks away from the real Leaky ReLU (blue line). On the right, the split into a linear part and the absolute value; at $\\alpha=0.2$ the coefficients are $0.6$ and $0.4$."),
        ("table", ["$x$", "$\\alpha=0.01$", "$\\alpha=0.2$", "$\\operatorname{LReLU}'(x)$"], "TABLE", {"num": [0, 1, 2, 3]}),
        ("p", "To the right of zero all variants coincide with ReLU; they differ only in how much negative signal “leaks” through."),
    ]),
    dict(id="properties", title="Properties", blocks=[
        ("ul", [
            "<b>Domain and range</b>: the whole real line $\\mathbb R$ (for $\\alpha&gt;0$). ReLU only takes values in $[0,\\,+\\infty)$.",
            "<b>Continuity and piecewise linearity</b>: two lines glued at zero. The function is differentiable everywhere except $x=0$.",
            "<b>Strict monotonicity</b> for $\\alpha&gt;0$: a larger input gives a larger output. Hence the function is invertible: $\\operatorname{LReLU}_\\alpha^{-1}(y)=y$ for $y&gt;0$ and $y/\\alpha$ for $y\\le0$, i.e. $\\operatorname{LReLU}_{1/\\alpha}$. ReLU has no inverse: all negative inputs are glued into zero.",
            "<b>Positive homogeneity</b>: $\\operatorname{LReLU}(cx)=c\\,\\operatorname{LReLU}(x)$ for $c\\ge0$. The scale of the input carries over to the output — hence the simple initialization formulas.",
            "<b>Lipschitz continuity</b> with constant $\\max(1,\\alpha)$, i.e. 1 for $\\alpha\\le1$: $|\\operatorname{LReLU}(a)-\\operatorname{LReLU}(b)|\\le|a-b|$.",
            "<b>Unboundedness</b> above and below, though downwards the function grows $1/\\alpha$ times more slowly.",
            "<b>Special cases</b>: $\\alpha=0$ is ReLU, $\\alpha=1$ the identity, $\\alpha=-1$ the absolute value $|x|$ (no longer monotonic).",
        ]),
        ("h3", "Mean and spread of the output"),
        ("p", "Let the neuron’s input be $z\\sim N(0,1)$. Then"),
        ("eq", r"\mathbb E\bigl[\operatorname{LReLU}(z)\bigr]=\frac{1-\alpha}{\sqrt{2\pi}},\qquad \mathbb E\bigl[\operatorname{LReLU}(z)^2\bigr]=\frac{1+\alpha^2}{2}"),
        ("p", "At $\\alpha=0.01$ the mean is $0.395$ (ReLU: $0.399$), at $\\alpha=0.2$ it is $0.319$. The larger $\\alpha$, the closer the outputs are to zero mean, which makes the next layer slightly easier to train. The second moment $\\frac{1+\\alpha^2}{2}$ will be needed in the section on initialization."),
        ("deep", "Where these formulas come from", [
            ("p", "For $z\\sim N(0,1)$ we know that $\\mathbb E[z\\,\\mathbf 1_{z&gt;0}]=\\varphi(0)=1/\\sqrt{2\\pi}$, and by symmetry $\\mathbb E[z\\,\\mathbf 1_{z&lt;0}]=-1/\\sqrt{2\\pi}$. Therefore"),
            ("eq", r"\mathbb E[\operatorname{LReLU}(z)]=\mathbb E[z\mathbf 1_{z>0}]+\alpha\,\mathbb E[z\mathbf 1_{z<0}]=\frac{1}{\sqrt{2\pi}}-\frac{\alpha}{\sqrt{2\pi}}"),
            ("p", "Likewise $\\mathbb E[z^2\\mathbf 1_{z&gt;0}]=\\mathbb E[z^2\\mathbf 1_{z&lt;0}]=\\tfrac12$, so $\\mathbb E[\\operatorname{LReLU}(z)^2]=\\tfrac12+\\tfrac{\\alpha^2}{2}$. The second formula holds for any symmetric distribution with unit variance, the first only for the normal one."),
        ]),
    ]),
    dict(id="derivative", title="The derivative: a step instead of a cliff", blocks=[
        ("p", "On each branch the function is linear, so the derivative is simply the slope of the branch:"),
        ("eq", r"\operatorname{LReLU}'_\alpha(x)=\begin{cases}1, & x>0,\\ \alpha, & x<0.\end{cases}"),
        ("deep", "Derivation from the definition", [
            ("p", "For $x&gt;0$ and small enough $h$ the point $x+h$ is positive too, and $\\frac{\\operatorname{LReLU}(x+h)-\\operatorname{LReLU}(x)}{h}=\\frac{(x+h)-x}{h}=1$. For $x&lt;0$ we likewise get $\\frac{\\alpha(x+h)-\\alpha x}{h}=\\alpha$."),
            ("p", "At zero the one-sided limits differ:"),
            ("eq", r"\lim_{h\to0^+}\frac{\operatorname{LReLU}(h)-0}{h}=1,\qquad \lim_{h\to0^-}\frac{\alpha h-0}{h}=\alpha"),
            ("p", "For $\\alpha\\ne1$ they do not match, so there is no derivative at zero — it is a kink."),
        ]),
        ("p", "What to do about zero in practice? At the kink there is a <b>subgradient</b>: for $0\\le\\alpha\\le1$ any number $g\\in[\\alpha,\\,1]$ defines a line $y=gx$ that lies nowhere above the graph. Libraries pick one value by convention — PyTorch takes $\\alpha$ at $x=0$. An input rarely lands exactly on zero, so the choice hardly matters."),
        ("h3", "Why a step is better than a cliff"),
        ("p", "By the chain rule the gradient with respect to the weight $w_j$ of a neuron $a=\\operatorname{LReLU}(z)$, $z=\\sum_j w_jx_j+b$, is"),
        ("eq", r"\frac{\partial L}{\partial w_j}=\frac{\partial L}{\partial a}\cdot\operatorname{LReLU}'(z)\cdot x_j"),
        ("p", "For ReLU the middle factor is 0 when $z&lt;0$; for Leaky ReLU it is $\\alpha$. On the left the gradient is $1/\\alpha$ times weaker, but not zero: a neuron “stuck” in the negative zone still receives an error signal."),
        ("h3", "The derivative with respect to α: a step towards PReLU"),
        ("p", "If $\\alpha$ becomes a learnable parameter, we need the derivative with respect to it. It is simple too:"),
        ("eq", r"\frac{\partial\operatorname{LReLU}_\alpha(x)}{\partial\alpha}=\begin{cases}0, & x>0,\\ x, & x\le 0\end{cases}\;=\;\min(0,\,x)"),
        ("p", "The slope $\\alpha$ learns only from examples that land on the left branch — this is how PReLU works (section 9). The second derivative in $x$ is zero everywhere except at zero: all the curvature is concentrated in the kink, and in the sense of generalized functions $\\operatorname{LReLU}''(x)=(1-\\alpha)\\,\\delta(x)$."),
    ]),
    dict(id="dying", title="The dying ReLU and how Leaky cures it", blocks=[
        ("p", "How a neuron dies. Suppose that after an unlucky large step (too high a learning rate, an outlier in the data, a bad initialization) the neuron’s bias $b$ has become strongly negative. Then $z=w^\\top x+b&lt;0$ on every example, ReLU outputs 0, the derivative $\\operatorname{ReLU}'(z)=0$ — and the gradients with respect to $w$, $b$ and the output weight $v$ vanish all at once. Gradient descent will never move this neuron again: it is dead. The CS231n course notes mention that with too high a learning rate as much as 40% of a network can end up dead."),
        ("p", "Below is the cleanest possible experiment. A single neuron $f(x)=v\\cdot\\operatorname{act}(wx+b)$ has to learn the “hinge” $y=1.5\\max(0,\\,x-1)$ from 41 points on $[-3,\\,3]$. Start: $w=1$, $b=-4$, $v=1$ — the kink is at $x=4$, outside the data, so $z&lt;0$ on every example. Training is gradient descent on MSE with step $0.1$."),
        ("viz", "leaky-relu-revive", {"alpha": 0.1}, "<b>Figure 3.</b> Press “Play”. The ReLU neuron (black dashes) is frozen: all its gradients are zero, and the error stays at $1.09$ forever. The Leaky ReLU neuron with $\\alpha=0.1$ receives a weak gradient, its line tilts and shifts, and at step 24 the kink enters the data range. After 1500 steps the error is $0.0549$. With $\\alpha=0.01$ the revival takes 135 steps, but the final error is $0.00082$."),
        ("p", "Note the trade-off. A large $\\alpha$ brings the neuron back to life quickly, but the left branch stays tilted: with $\\alpha=0.1$ the final model has slope $\\alpha v w\\approx0.116$ on the left instead of zero, hence the residual error. A small $\\alpha$ barely distorts the shape of the function, but revives more slowly."),
        ("callout", "warn", "Leaky is not a guarantee", "A non-zero gradient does not mean the neuron must come back: it may stay on the left branch, working as the linear function $\\alpha(w^\\top x+b)$. What Leaky ReLU guarantees is different — the neuron never freezes solid and keeps learning. Against the cause of death itself, use a moderate learning rate, warmup, normalization and proper initialization."),
    ]),
    dict(id="space", title="A network of Leaky ReLUs: a piecewise-linear landscape", blocks=[
        ("p", "In a network with two inputs every neuron $\\operatorname{LReLU}(w_k^\\top x+b_k)$ “folds” the plane along the line $w_k^\\top x+b_k=0$: on one side of it the slope is $1/\\alpha$ times smaller than on the other. The sum of neurons $f(x)=\\sum_k v_k\\operatorname{LReLU}(w_k^\\top x+b_k)$ is a polyhedral surface: inside every region where the set of active neurons does not change it is flat, and on the kink lines it changes slope."),
        ("viz", "leaky-relu-surface", {"alpha": 0.1}, "<b>Figure 4.</b> A network of six Leaky ReLU neurons. On the left, the surface $f(x_1,x_2)$ in 3D (you can rotate it); on the right, the view from above with the six kink lines. They cut the square $[-3,\\,3]^2$ into 19 linear regions. Drag the orange point: at the centre, at $(0.2,\\,-0.3)$, all six neurons are off, yet the gradient is not zero: $|\\nabla f|=0.100$. Set $\\alpha=0$: the central region becomes flat — that is 5% of the square where a ReLU network has a zero gradient with respect to the input. At $\\alpha=1$ the whole network turns into a single plane."),
        ("p", "The number of regions does not depend on $\\alpha$ (as long as $\\alpha\\ne1$): only the kink lines set it. What does depend on $\\alpha$ is what happens where all neurons are off. With ReLU there is a plateau with zero gradient, and examples that land on it tell the network nothing. With Leaky ReLU the plateau is tilted, and the gradient there is generally non-zero."),
        ("callout", "note", "How many regions there can be", "$n$ lines in general position cut the plane into at most $1+n+\\binom n2$ pieces: for $n=6$ that is 22. In the square of the figure 19 of them are visible. In deep networks the number of linear regions can grow exponentially with depth — one explanation of their expressive power."),
    ]),
    dict(id="depth", title="Deep networks: He initialization for Leaky ReLU", blocks=[
        ("p", "In a deep network the signal passes through dozens of layers $z_{l+1}=W_{l+1}\\operatorname{LReLU}(z_l)$. If at every layer the variance is multiplied by a number even slightly different from 1, after 50 layers this becomes an explosion or a disappearance of the signal. Let us compute that factor."),
        ("deep", "Deriving the factor", [
            ("p", "Let the weights $W_{ij}$ be independent, $\\mathbb E W_{ij}=0$, $\\operatorname{Var}W_{ij}=s^2$, and the inputs $z_l$ symmetric around zero. For one output $z_{l+1,i}=\\sum_{j=1}^{n}W_{ij}h_j$ with $h_j=\\operatorname{LReLU}(z_{l,j})$:"),
            ("eq", r"\operatorname{Var}z_{l+1}=n\,s^2\,\mathbb E[h^2]=n\,s^2\,\frac{1+\alpha^2}{2}\operatorname{Var}z_l"),
            ("p", "The last equality is the second moment from the section on properties: half of $z_l^2$ comes from the positive branch in full, half from the negative one, multiplied by $\\alpha^2$. For the variance to be preserved, the factor must equal 1:"),
            ("eq", r"s^2=\frac{2}{(1+\alpha^2)\,n_{\text{in}}}\qquad\Longleftrightarrow\qquad g=\sqrt n\,s=\sqrt{\frac{2}{1+\alpha^2}}"),
            ("p", "On the backward pass the gradient is multiplied by $W^\\top$ and by $\\operatorname{LReLU}'(z)$, and $\\mathbb E[\\operatorname{LReLU}'(z)^2]=\\frac{1+\\alpha^2}{2}$ — the same factor. So one and the same initialization preserves both the forward signal and the gradients."),
        ]),
        ("eq", r"\operatorname{Var}z_{l+1}=\frac{g^2(1+\alpha^2)}{2}\,\operatorname{Var}z_l,\qquad g_{\text{He}}=\sqrt{\frac{2}{1+\alpha^2}}"),
        ("p", "With $\\alpha=0$ we get the famous $g=\\sqrt2$ of He (Kaiming) initialization for ReLU. For Leaky ReLU the coefficient is slightly smaller: $1.414$ at $\\alpha=0.01$, $1.387$ at $\\alpha=0.2$, $1.355$ at $\\alpha=0.3$."),
        ("viz", "leaky-relu-init", {"alpha": 0.3, "depth": 50}, "<b>Figure 5.</b> The RMS of the pre-activations at every layer of a random network of width 256 (the vertical scale is logarithmic). By default $\\alpha=0.3$ and the weights are initialized “as for ReLU”, $g=\\sqrt2$: the variance factor is $1.09$ per layer, and by layer 50 the RMS grows to $11.6$ (theory: $11.7$). With the correct $g=\\sqrt{2/(1+\\alpha^2)}$ the factor is 1, and at layer 50 the RMS is $1.34$ (theory: $1.35$). With $g=1$ the factor is $0.545$, and the signal fades to $3.45\\cdot10^{-7}$."),
        ("callout", "note", "In PyTorch", "This is exactly what <code>nn.init.kaiming_normal_(w, a=alpha, nonlinearity='leaky_relu')</code> does: the standard deviation is $\\sqrt{2/((1+a^2)\\,n_{\\text{in}})}$. The default there is <code>a=0</code>, i.e. the initialization for plain ReLU — for Leaky ReLU the parameter <code>a</code> has to be passed explicitly."),
    ]),
    dict(id="family", title="PReLU, RReLU and the whole family", blocks=[
        ("p", "How to choose $\\alpha$? There are three answers."),
        ("ul", [
            "<b>A fixed $\\alpha$</b> — the classic Leaky ReLU (Maas, Hannun, Ng, 2013, $\\alpha=0.01$). Today $0.1$–$0.3$ is common: in the comparison by Xu et al. (2015) a “very leaky” variant with $\\alpha=1/5.5\\approx0.18$ worked better than $0.01$.",
            "<b>A learnable $\\alpha$</b> — PReLU (Parametric ReLU, He et al., 2015). $\\alpha$ becomes a parameter — one per layer or one per channel — and is learned by gradient descent together with the weights. The initial value in PyTorch is $0.25$.",
            "<b>A random $\\alpha$</b> — RReLU (Randomized ReLU): during training $\\alpha$ is drawn for each example from the uniform distribution $U(1/8,\\,1/3)$ (PyTorch’s default bounds); at inference the mean $\\frac{1/8+1/3}{2}=\\frac{11}{48}\\approx0.229$ is used. The noise acts as regularization.",
        ]),
        ("p", "For PReLU the gradient with respect to $\\alpha$ is $\\min(0,\\,z)$ from the section on the derivative: the slope learns only from negative inputs. Let us watch gradient descent find both the weight and the slope."),
        ("viz", "leaky-relu-prelu", {"w": 0.5, "a": 1.3}, "<b>Figure 6.</b> The two-parameter model $\\operatorname{PReLU}_\\alpha(wx)$ learns from 31 points generated by the “teacher” $w^*=1.5$, $\\alpha^*=0.2$ with noise. On the right, the error surface $L(w,\\alpha)$ (lighter means smaller). From the start $(0.5,\\,1.3)$ gradient descent with step $0.05$ arrives in 87 steps at $w=1.521$, $\\alpha=0.209$ with error $0.0158$ — the minimum for these noisy data (the teacher itself has error $0.0170$). Drag the start somewhere else."),
        ("p", "PReLU adds only one parameter per channel, yet in the work of He et al., together with a new initialization, it made it possible to train very deep convolutional networks and reach a top-5 error of $4.94\\%$ on ImageNet — below the estimated human error of $5.1\\%$. The authors note that weight decay should not be applied to $\\alpha$: it pulls $\\alpha$ towards zero, that is, back to ReLU."),
        ("h3", "Smooth relatives"),
        ("p", "The kink at zero can be smoothed. ELU replaces the left line with the exponential $\\alpha(e^x-1)$, which saturates at $-\\alpha$. SELU adds a scale: $\\lambda\\approx1.0507$ and $\\alpha\\approx1.6733$ are chosen so that the activations keep zero mean and unit variance by themselves. <a href=\"../gelu/\">GELU</a> and <a href=\"../silu/\">SiLU</a> are smooth and even non-monotonic functions used in today’s transformers."),
        ("viz", "leaky-relu-zoo", {"cmp": "elu", "x": -2}, "<b>Figure 7.</b> Leaky ReLU with $\\alpha=0.1$ next to its relatives. Hover the cursor: at $x=-2$ Leaky ReLU gives $-0.2$, ELU $-0.865$, SELU $-1.520$, GELU $-0.046$, SiLU $-0.238$. Switch to the derivatives: for Leaky ReLU and SELU it is a step with a jump at zero (for SELU $\\lambda\\alpha\\approx1.758$ on the left and $\\lambda\\approx1.051$ on the right), for ELU, GELU and SiLU a continuous curve."),
        ("table", ["Function", "For $x\\le0$", "Derivative on the left", "Feature"], "FAMILY", {}),
    ]),
    dict(id="code", title="In code", blocks=[
        ("p", "In NumPy Leaky ReLU is one line. It is safer to write <code>np.where</code> than <code>np.maximum(alpha * x, x)</code>: the latter silently breaks for $\\alpha&gt;1$."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Library defaults differ", "PyTorch <code>nn.LeakyReLU</code>: <code>negative_slope=0.01</code>. TensorFlow <code>tf.nn.leaky_relu</code>: <code>alpha=0.2</code>. Keras <code>layers.LeakyReLU</code>: $0.3$. The same “Leaky ReLU” in three frameworks is three different functions. When porting a model, set $\\alpha$ explicitly."),
        ("p", "Numerically Leaky ReLU is safe: no exponentials, no division, no overflow. The only subtlety is <code>inplace=True</code> in PyTorch: it saves memory but overwrites the input, which other operations of the graph may still need."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>Writing <code>max(alpha * x, x)</code> with $\\alpha&gt;1$.</b> The formula holds only for $\\alpha\\le1$; for larger $\\alpha$ you get a different function. The safe form is <code>where(x &gt; 0, x, alpha * x)</code>.",
            "<b>Too large an $\\alpha$.</b> As $\\alpha\\to1$ the share of nonlinearity $\\frac{1-\\alpha}{2}$ goes to zero, the function becomes almost linear, and a deep network loses expressiveness. A sensible range is from $0.01$ to $0.3$.",
            "<b>Initializing “as for ReLU” without correcting for $\\alpha$.</b> The variance factor is $1+\\alpha^2$ per layer: at $\\alpha=0.3$ the signal grows about 8 times over 50 layers (figure 5). Pass $\\alpha$ to <code>kaiming_normal_(..., a=alpha)</code>.",
            "<b>Hoping that Leaky ReLU alone will cure unstable training.</b> It removes the zero gradient, but not the cause: too high a learning rate is still dangerous.",
            "<b>Weight decay on the $\\alpha$ of PReLU.</b> It pulls $\\alpha$ towards zero, and PReLU turns into ReLU. Exclude $\\alpha$ from the parameter group with weight decay.",
            "<b>Different defaults</b> in PyTorch ($0.01$), TensorFlow ($0.2$) and Keras ($0.3$): when a model moves between frameworks, the result silently changes.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../relu/\">ReLU</a>: the special case $\\alpha=0$; more on the dying ReLU there.",
            "<a href=\"../silu/\">SiLU / Swish</a> and <a href=\"../gelu/\">GELU</a>: smooth activations that also let a small negative signal through on the left, but then fade it out.",
            "<a href=\"../sigmoid/\">Sigmoid</a> and <a href=\"../tanh/\">tanh</a>: saturating activations; Leaky ReLU has no saturation at all, and hence no vanishing gradient caused by saturation.",
            "<a href=\"../mse/\">MSE</a>: the loss function in the experiments of figures 3 and 6.",
            "<a href=\"../sgd/\">SGD</a> and <a href=\"../adam/\">Adam</a>: too large an optimizer step is the main cause of death for ReLU neurons.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $\\operatorname{LReLU}_\\alpha(x)=x$ for $x&gt;0$ and $\\alpha x$ for $x\\le0$; it equals $\\max(\\alpha x,x)$ for $\\alpha\\le1$ and $\\frac{1+\\alpha}{2}x+\\frac{1-\\alpha}{2}|x|$ for any $\\alpha$. 2) The derivative is a step made of $\\alpha$ and $1$: the gradient does not vanish, the neuron does not freeze. 3) The trade-off: a larger $\\alpha$ revives neurons faster but brings the function closer to linear. 4) A network of Leaky ReLUs is a piecewise-linear function without flat “dead” plateaus. 5) Initialization: $\\operatorname{Var}w=\\frac{2}{(1+\\alpha^2)\\,n_{\\text{in}}}$. 6) PReLU learns $\\alpha$ through the gradient $\\min(0,z)$."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="What is $\\operatorname{LReLU}(-5)$ with $\\alpha=0.2$?", options=["$0$", "$-1$", "$-5$", "$1$"], answer=1,
                 explain="The input is negative, so the branch $\\alpha x=0.2\\cdot(-5)=-1$ applies."),
            dict(q="What is the derivative of Leaky ReLU for $x&lt;0$?", options=["$0$", "$1$", "$\\alpha$", "$\\alpha x$"], answer=2,
                 explain="On the left the function is the line $\\alpha x$, whose slope is $\\alpha$. So the gradient does not vanish."),
            dict(q="For which $\\alpha$ does $\\operatorname{LReLU}_\\alpha(x)=\\max(\\alpha x,x)$ hold?", options=["For any $\\alpha$", "Only for $\\alpha\\le1$", "Only for $\\alpha&gt;1$", "Only for $\\alpha=0.01$"], answer=1,
                 explain="For $\\alpha\\le1$, on the right $x\\ge\\alpha x$ and on the left $\\alpha x\\ge x$. For $\\alpha&gt;1$ the maximum picks $\\alpha x$ on the right — a different function."),
            dict(q="A network with Leaky ReLU ($\\alpha=0.3$) is initialized “as for ReLU”, $g=\\sqrt2$. What is the variance factor per layer?", options=["$1$", "$1.09$", "$0.545$", "$2$"], answer=1,
                 explain="$g^2(1+\\alpha^2)/2=2\\cdot1.09/2=1.09$. Over 50 layers the RMS grows by about $1.09^{24.5}\\approx8.3$ times."),
            dict(q="A ReLU neuron gets $z&lt;0$ on every example. What is true?", options=["The gradients with respect to its parameters are zero, and gradient descent will never change it again", "The gradient is small but not zero", "The neuron outputs negative values", "Lowering the learning rate is enough to revive it"], answer=0,
                 explain="$\\operatorname{ReLU}'(z)=0$ for $z&lt;0$, so all gradients vanish — the neuron is dead. A smaller step will not help: a step multiplied by zero is still zero."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "<a href=\"../relu/\">ReLU</a> — chuqur o‘qitishdagi eng mashhur aktivatsiya: $\\max(0,x)$ bir zumda hisoblanadi, noldan o‘ngda esa gradiyent so‘nmaydi. Lekin uning zaif joyi bor. Noldan chapda ReLU signalni susaytirmaydi, balki uni <b>nolga aylantiradi</b> — u bilan birga gradiyentni ham. Kirishi barcha misollarda manfiy bo‘lgan neyron 0 chiqaradi, nol gradiyent oladi va boshqa hech qachon o‘rganmaydi. Bu «o‘layotgan ReLU» (dying ReLU)."),
        ("p", "Leaky ReLU — eng kichik tuzatish: noldan chapda grafik gorizontal emas, biroz qiya — kichik $\\alpha$ bilan $\\alpha x$ (odatda $0{,}01$ dan $0{,}3$ gacha). Signal yopiq eshikdan «sizib o‘tadi» — nomi shundan (leaky — «oqadigan»)."),
        ("p", "U qayerda uchraydi:"),
        ("ul", [
            "<b>GAN diskriminatorlari</b> — DCGAN’da (Redford va boshq., 2015) diskriminatorning barcha qatlamlari $\\alpha=0{,}2$ li Leaky ReLU’dan foydalanadi;",
            "<b>YOLO detektorlari</b> — YOLOv2 va YOLOv3 dagi Darknet tarmog‘i $\\alpha=0{,}1$ li Leaky ReLU asosida qurilgan;",
            "<b>graf tarmoqlari</b> — GAT’dagi e’tibor koeffitsiyentlari $\\alpha=0{,}2$ li Leaky ReLU orqali hisoblanadi;",
            "<b>PReLU’li konvolyutsion tarmoqlar</b> — o‘rganiladigan $\\alpha$ li variant (Xe va boshq., 2015) ImageNet’da top-5 xatoni ilk bor inson darajasidan pastga tushirishga yordam berdi;",
            "<b>ReLU «o‘ladigan» istalgan tarmoq</b> — almashtirish bitta qator va deyarli hech narsaga tushmaydi.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "$x&gt;0$ da $\\operatorname{LReLU}(x)=x$, $x\\le0$ da $\\alpha x$. Hosila — zina: o‘ngda $1$, chapda $\\alpha$, shuning uchun gradiyent hech qachon butunlay nolga aylanmaydi. Funksiya bo‘lak-chiziqli, monoton va deyarli ReLU kabi arzon bo‘lib qoladi. $\\alpha=0$ da bu ReLU, $\\alpha=1$ da ayniy funksiya, o‘rganiladigan $\\alpha$ da — PReLU."),
    ]),
    dict(id="intuition", title="Intuitsiya: oxirigacha yopilmaydigan eshik", blocks=[
        ("p", "ReLU eshikka o‘xshaydi: musbat signal to‘liq o‘tadi, manfiysi yopiq tabaqaga uriladi. Leaky ReLU tirqish qoldiradi — manfiy signal o‘tadi, lekin $1/\\alpha$ marta susaygan holda. $\\alpha=0{,}1$ da $-2$ kirish $-0{,}2$ ga aylanadi."),
        ("p", "Nuqtani grafik bo‘ylab torting. To‘q sariq «qiyalik uchburchagi» hosilani ko‘rsatadi: $x$ o‘qi bo‘ylab 1 ga qadam qiymatni noldan chapda $\\alpha$ ga, o‘ngda 1 ga o‘zgartiradi. Pastda — hosilaning o‘zi: nolda uzilishga ega ikki gorizontal zina. $\\alpha$ surgichini suring: ReLU’dan ($\\alpha=0$) «oqadigan» variant orqali $y=x$ to‘g‘ri chiziqqacha ($\\alpha=1$)."),
        ("viz", "leaky-relu-explorer", {"alpha": 0.1, "x": -2}, "<b>1-rasm.</b> $\\alpha=0{,}1$ dagi Leaky ReLU va uning hosilasi. $x=-2$ nuqtada qiymat $-0{,}2$, hosila $0{,}1$. Kulrang punktir — ReLU, nuqtali chiziq — $y=x$. Nolda hosila aniqlanmagan: chapda u $\\alpha$ ga, o‘ngda 1 ga teng."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "Chapda grafik yassi emas, lekin juda qiya emas: $\\alpha=0{,}01$ da $-100$ kirish atigi $-1$ beradi. Leaky ReLU’ning butun nochiziqliligi bitta nuqtada — qiyalik $\\alpha$ dan 1 ga o‘zgaradigan noldagi sinishda jamlangan. Bunday neyronlardan iborat tarmoqning ifodalash kuchi aynan shu sinishlardan keladi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", "Bitta funksiyani uch xil yozishni bilish foydali — har biri o‘z joyida kerak bo‘ladi."),
        ("h3", "1. Hollar bo‘yicha"),
        ("eq", r"\operatorname{LReLU}_\alpha(x)=\begin{cases}x, & x>0,\\ \alpha x, & x\le 0.\end{cases}"),
        ("symbols", [
            (r"x", "neyron kirishi — odatda $z=w^\\top h+b$ pre-aktivatsiya;"),
            (r"\alpha", "manfiy qismning qiyaligi, giperparametr; odatda $0&lt;\\alpha&lt;1$;"),
            (r"\alpha x", "«sizish»: manfiy kirish nolga aylanmaydi, $1/\\alpha$ marta siqiladi."),
        ]),
        ("p", "$x=0$ nuqtada ikkala tarmoq ham nol beradi, shuning uchun nolni qaysi tarmoqqa qo‘shish muhim emas: funksiya uzluksiz."),
        ("h3", "2. Maksimum orqali"),
        ("eq", r"\operatorname{LReLU}_\alpha(x)=\max(\alpha x,\;x)\qquad(\alpha\le 1)"),
        ("p", "$x&gt;0$ va $\\alpha\\le1$ da $x\\ge\\alpha x$, $x&lt;0$ da esa aksincha, $\\alpha x\\ge x$. Demak, maksimum kerakli tarmoqni o‘zi tanlaydi. Lekin faqat $\\alpha\\le1$ da: $\\alpha=2$ da o‘ngda $2x$ yutadi va boshqa funksiya hosil bo‘ladi. Bu yozuv kodda qulay (<code>np.maximum(alpha * x, x)</code>), lekin shartni unutish oson."),
        ("h3", "3. Chiziqli qism plyus modul"),
        ("eq", r"\operatorname{LReLU}_\alpha(x)=\frac{1+\alpha}{2}\,x+\frac{1-\alpha}{2}\,|x|"),
        ("p", "Tekshiruv: $x&gt;0$ da $\\frac{1+\\alpha}{2}x+\\frac{1-\\alpha}{2}x=x$, $x&lt;0$ da — $\\frac{1+\\alpha}{2}x-\\frac{1-\\alpha}{2}x=\\alpha x$. Bu shakl istalgan $\\alpha$ da to‘g‘ri va asosiysini tushuntiradi: Leaky ReLU — chiziqli funksiya plyus «ozgina modul». Butun nochiziqlilik ikkinchi qo‘shiluvchida, uning ulushi $\\frac{1-\\alpha}{2}$ esa $\\alpha$ o‘sishi bilan kamayadi. $\\alpha=1$ da nochiziqlilik butunlay yo‘qoladi."),
        ("viz", "leaky-relu-parts", {"alpha": 0.2}, "<b>2-rasm.</b> Chapda — $y=x$ va $y=\\alpha x$ ikki to‘g‘ri chiziqning yuqori o‘ramasi sifatidagi Leaky ReLU. $\\alpha$ ni 1 dan yuqoriga suring: o‘rama (qora punktir) haqiqiy Leaky ReLU’dan (ko‘k chiziq) ajralib ketadi. O‘ngda — chiziqli qism va modulga ajratish; $\\alpha=0{,}2$ da koeffitsiyentlar $0{,}6$ va $0{,}4$."),
        ("table", ["$x$", "$\\alpha=0{,}01$", "$\\alpha=0{,}2$", "$\\operatorname{LReLU}'(x)$"], "TABLE", {"num": [0, 1, 2, 3]}),
        ("p", "Noldan o‘ngda barcha variantlar ReLU bilan ustma-ust tushadi; ular faqat qancha manfiy signal «sizib o‘tishi» bilan farqlanadi."),
    ]),
    dict(id="properties", title="Xossalar", blocks=[
        ("ul", [
            "<b>Aniqlanish va qiymatlar sohasi</b> — butun son o‘qi $\\mathbb R$ ($\\alpha&gt;0$ da). ReLU’ning qiymatlari faqat $[0;\\,+\\infty)$.",
            "<b>Uzluksizlik va bo‘lak-chiziqlilik</b>: nolda yopishtirilgan ikki to‘g‘ri chiziq. Funksiya $x=0$ dan boshqa hamma joyda differensiallanuvchi.",
            "<b>Qat’iy monotonlik</b> $\\alpha&gt;0$ da: katta kirish katta chiqish beradi. Shuning uchun funksiya teskarilanuvchi: $y&gt;0$ da $\\operatorname{LReLU}_\\alpha^{-1}(y)=y$, $y\\le0$ da $y/\\alpha$, ya’ni $\\operatorname{LReLU}_{1/\\alpha}$. ReLU’ning teskarisi yo‘q: barcha manfiy kirishlar nolga yopishtirilgan.",
            "<b>Musbat bir jinslilik</b>: $c\\ge0$ da $\\operatorname{LReLU}(cx)=c\\,\\operatorname{LReLU}(x)$. Kirish masshtabi shunchaki chiqishga o‘tadi — initsializatsiyaning sodda formulalari shundan.",
            "<b>Lipshits sharti</b> $\\max(1,\\alpha)$ konstanta bilan, ya’ni $\\alpha\\le1$ da 1: $|\\operatorname{LReLU}(a)-\\operatorname{LReLU}(b)|\\le|a-b|$.",
            "<b>Chegaralanmaganlik</b> yuqoridan ham, pastdan ham, lekin pastga funksiya $1/\\alpha$ marta sekinroq o‘sadi.",
            "<b>Xususiy hollar</b>: $\\alpha=0$ — ReLU, $\\alpha=1$ — ayniy funksiya, $\\alpha=-1$ — $|x|$ modul (endi monoton emas).",
        ]),
        ("h3", "Chiqishning o‘rtachasi va tarqoqligi"),
        ("p", "Neyron kirishi $z\\sim N(0,1)$ bo‘lsin. U holda"),
        ("eq", r"\mathbb E\bigl[\operatorname{LReLU}(z)\bigr]=\frac{1-\alpha}{\sqrt{2\pi}},\qquad \mathbb E\bigl[\operatorname{LReLU}(z)^2\bigr]=\frac{1+\alpha^2}{2}"),
        ("p", "$\\alpha=0{,}01$ da o‘rtacha $0{,}395$ ga teng (ReLU’da — $0{,}399$), $\\alpha=0{,}2$ da — $0{,}319$. $\\alpha$ qancha katta bo‘lsa, chiqishlar nol o‘rtachaga shuncha yaqin; bu keyingi qatlamni o‘qitishni biroz yengillashtiradi. $\\frac{1+\\alpha^2}{2}$ ikkinchi moment initsializatsiya bo‘limida kerak bo‘ladi."),
        ("deep", "Bu formulalar qayerdan keladi", [
            ("p", "$z\\sim N(0,1)$ uchun $\\mathbb E[z\\,\\mathbf 1_{z&gt;0}]=\\varphi(0)=1/\\sqrt{2\\pi}$ ekani ma’lum, simmetriya bo‘yicha esa $\\mathbb E[z\\,\\mathbf 1_{z&lt;0}]=-1/\\sqrt{2\\pi}$. Shuning uchun"),
            ("eq", r"\mathbb E[\operatorname{LReLU}(z)]=\mathbb E[z\mathbf 1_{z>0}]+\alpha\,\mathbb E[z\mathbf 1_{z<0}]=\frac{1}{\sqrt{2\pi}}-\frac{\alpha}{\sqrt{2\pi}}"),
            ("p", "Xuddi shunday $\\mathbb E[z^2\\mathbf 1_{z&gt;0}]=\\mathbb E[z^2\\mathbf 1_{z&lt;0}]=\\tfrac12$, bundan $\\mathbb E[\\operatorname{LReLU}(z)^2]=\\tfrac12+\\tfrac{\\alpha^2}{2}$. Ikkinchi formula birlik dispersiyali istalgan simmetrik taqsimot uchun to‘g‘ri, birinchisi — faqat normal taqsimot uchun."),
        ]),
    ]),
    dict(id="derivative", title="Hosila: jarlik o‘rniga zina", blocks=[
        ("p", "Har bir tarmoqda funksiya chiziqli, shuning uchun hosila — shunchaki tarmoq qiyaligi:"),
        ("eq", r"\operatorname{LReLU}'_\alpha(x)=\begin{cases}1, & x>0,\\ \alpha, & x<0.\end{cases}"),
        ("deep", "Ta’rif bo‘yicha keltirib chiqarish", [
            ("p", "$x&gt;0$ da yetarlicha kichik $h$ uchun $x+h$ nuqta ham musbat, va $\\frac{\\operatorname{LReLU}(x+h)-\\operatorname{LReLU}(x)}{h}=\\frac{(x+h)-x}{h}=1$. $x&lt;0$ da xuddi shunday $\\frac{\\alpha(x+h)-\\alpha x}{h}=\\alpha$ ni olamiz."),
            ("p", "Nolda bir tomonlama limitlar har xil:"),
            ("eq", r"\lim_{h\to0^+}\frac{\operatorname{LReLU}(h)-0}{h}=1,\qquad \lim_{h\to0^-}\frac{\alpha h-0}{h}=\alpha"),
            ("p", "$\\alpha\\ne1$ da ular mos kelmaydi, shuning uchun nolda hosila yo‘q — bu sinish nuqtasi."),
        ]),
        ("p", "Amalda nol bilan nima qilish kerak? Sinish nuqtasida <b>subgradiyent</b> (subgradient) bor: $0\\le\\alpha\\le1$ da istalgan $g\\in[\\alpha;\\,1]$ son grafikdan yuqorida yotmaydigan $y=gx$ to‘g‘ri chiziqni beradi. Kutubxonalar kelishuv bo‘yicha bitta qiymatni tanlaydi — PyTorch’da $x=0$ da $\\alpha$ olinadi. Kirish aynan nolga kamdan-kam tushadi, shuning uchun tanlov deyarli hech narsaga ta’sir qilmaydi."),
        ("h3", "Nega zina jarlikdan yaxshi"),
        ("p", "Zanjir qoidasiga ko‘ra $a=\\operatorname{LReLU}(z)$, $z=\\sum_j w_jx_j+b$ neyronning $w_j$ vazni bo‘yicha gradiyent"),
        ("eq", r"\frac{\partial L}{\partial w_j}=\frac{\partial L}{\partial a}\cdot\operatorname{LReLU}'(z)\cdot x_j"),
        ("p", "ReLU’da $z&lt;0$ da o‘rta ko‘paytuvchi 0 ga teng, Leaky ReLU’da — $\\alpha$ ga. Chapda gradiyent $1/\\alpha$ marta kuchsizroq, lekin nolga teng emas: manfiy zonada «qolib ketgan» neyron xato haqidagi signalni olishda davom etadi."),
        ("h3", "α bo‘yicha hosila: PReLU sari qadam"),
        ("p", "Agar $\\alpha$ ni o‘rganiladigan parametrga aylantirsak, u bo‘yicha hosila kerak bo‘ladi. U ham sodda:"),
        ("eq", r"\frac{\partial\operatorname{LReLU}_\alpha(x)}{\partial\alpha}=\begin{cases}0, & x>0,\\ x, & x\le 0\end{cases}\;=\;\min(0,\,x)"),
        ("p", "$\\alpha$ qiyalik faqat chap tarmoqqa tushgan misollardan o‘rganadi — PReLU shunday tuzilgan (9-bo‘lim). $x$ bo‘yicha ikkinchi hosila noldan boshqa hamma joyda nolga teng: butun egrilik sinishda jamlangan, umumlashgan funksiyalar ma’nosida $\\operatorname{LReLU}''(x)=(1-\\alpha)\\,\\delta(x)$."),
    ]),
    dict(id="dying", title="O‘layotgan ReLU va Leaky uni qanday davolaydi", blocks=[
        ("p", "Neyron qanday o‘ladi. Muvaffaqiyatsiz katta qadamdan keyin (juda katta o‘qitish tezligi, ma’lumotlardagi chetga chiqish, yomon initsializatsiya) neyronning $b$ siljishi kuchli manfiy bo‘lib qolgan bo‘lsin. U holda barcha misollarda $z=w^\\top x+b&lt;0$, ReLU 0 chiqaradi, $\\operatorname{ReLU}'(z)=0$ — va $w$, $b$ hamda chiqish vazni $v$ bo‘yicha gradiyentlar birdaniga nolga aylanadi. Gradiyent tushish bu neyronni boshqa hech qachon siljitmaydi: u o‘lik. CS231n kursi konspektlarida o‘qitish tezligi juda katta bo‘lsa, tarmoqning 40% gachasi o‘lik bo‘lib qolishi mumkinligi qayd etilgan."),
        ("p", "Quyida eng toza tajriba. Bitta $f(x)=v\\cdot\\operatorname{act}(wx+b)$ neyron $[-3;\\,3]$ kesmadagi 41 nuqta bo‘yicha $y=1{,}5\\max(0,\\,x-1)$ «sharnir»ni o‘rganishi kerak. Start: $w=1$, $b=-4$, $v=1$ — sinish $x=4$ nuqtada, ma’lumotlardan tashqarida, shuning uchun barcha misollarda $z&lt;0$. O‘qitish — $0{,}1$ qadamli MSE bo‘yicha gradiyent tushish."),
        ("viz", "leaky-relu-revive", {"alpha": 0.1}, "<b>3-rasm.</b> «Boshlash»ni bosing. ReLU neyron (qora punktir) muzlagan: uning barcha gradiyentlari nolga teng va xato abadiy $1{,}09$ bo‘lib qoladi. $\\alpha=0{,}1$ li Leaky ReLU neyron kuchsiz gradiyent oladi, uning to‘g‘ri chizig‘i qiyshayadi va suriladi, 24-qadamda sinish ma’lumotlar sohasiga kiradi. 1500 qadamdan keyin xato $0{,}0549$ ga teng. $\\alpha=0{,}01$ da jonlanish 135 qadam oladi, lekin yakuniy xato — $0{,}00082$."),
        ("p", "Murosaga e’tibor bering. Katta $\\alpha$ neyronni tez hayotga qaytaradi, lekin chap tarmoq qiya bo‘lib qoladi: $\\alpha=0{,}1$ da yakuniy model chapda nol o‘rniga $\\alpha v w\\approx0{,}116$ qiyalikka ega, qoldiq xato shundan. Kichik $\\alpha$ funksiya shaklini deyarli buzmaydi, lekin sekinroq jonlantiradi."),
        ("callout", "warn", "Leaky — kafolat emas", "Nol bo‘lmagan gradiyent neyron albatta qaytadi degani emas: u chap tarmoqda $\\alpha(w^\\top x+b)$ chiziqli funksiya sifatida ishlab qolishi mumkin. Leaky ReLU boshqa narsani kafolatlaydi — neyron hech qachon butunlay muzlamaydi va o‘rganishda davom etadi. O‘limning o‘z sababiga qarshi mo‘tadil o‘qitish tezligi, qizdirish (warmup), normallashtirish va to‘g‘ri initsializatsiya yordam beradi."),
    ]),
    dict(id="space", title="Leaky ReLU’lardan iborat tarmoq: bo‘lak-chiziqli relyef", blocks=[
        ("p", "Ikki kirishli tarmoqda har bir $\\operatorname{LReLU}(w_k^\\top x+b_k)$ neyron tekislikni $w_k^\\top x+b_k=0$ to‘g‘ri chiziq bo‘ylab «bukadi»: uning bir tomonida qiyalik ikkinchisidagidan $1/\\alpha$ marta kichik. $f(x)=\\sum_k v_k\\operatorname{LReLU}(w_k^\\top x+b_k)$ neyronlar yig‘indisi — ko‘p yoqli sirt: faol neyronlar to‘plami o‘zgarmaydigan har bir soha ichida u tekis, sinish chiziqlarida esa qiyaligini o‘zgartiradi."),
        ("viz", "leaky-relu-surface", {"alpha": 0.1}, "<b>4-rasm.</b> Oltita Leaky ReLU neyrondan iborat tarmoq. Chapda — 3D’dagi $f(x_1,x_2)$ sirt (uni aylantirish mumkin), o‘ngda — oltita sinish chizig‘i bilan yuqoridan ko‘rinish. Ular $[-3;\\,3]^2$ kvadratni 19 ta chiziqli sohaga bo‘ladi. To‘q sariq nuqtani torting: markazda, $(0{,}2;\\,-0{,}3)$ nuqtada oltala neyron ham o‘chgan, lekin gradiyent nol emas: $|\\nabla f|=0{,}100$. $\\alpha=0$ qiling: markaziy soha tekis bo‘lib qoladi — bu kvadratning 5% i, u yerda ReLU tarmog‘ining kirish bo‘yicha gradiyenti nolga teng. $\\alpha=1$ da butun tarmoq bitta tekislikka aylanadi."),
        ("p", "Sohalar soni $\\alpha$ ga bog‘liq emas ($\\alpha\\ne1$ ekan): uni faqat sinish chiziqlari belgilaydi. Lekin barcha neyronlar o‘chgan joyda nima bo‘lishi $\\alpha$ ga bog‘liq. ReLU’da u yerda nol gradiyentli plato bo‘ladi va unga tushgan misollar tarmoqqa hech narsa bildirmaydi. Leaky ReLU’da plato qiya va u yerda gradiyent, odatda, nolga teng emas."),
        ("callout", "note", "Sohalar nechta bo‘lishi mumkin", "Umumiy vaziyatdagi $n$ ta to‘g‘ri chiziq tekislikni ko‘pi bilan $1+n+\\binom n2$ qismga bo‘ladi: $n=6$ uchun bu 22. Rasmdagi kvadratda ulardan 19 tasi ko‘rinadi. Chuqur tarmoqlarda chiziqli sohalar soni chuqurlik bilan eksponensial o‘sishi mumkin — bu ularning ifodalash kuchining tushuntirishlaridan biri."),
    ]),
    dict(id="depth", title="Chuqur tarmoqlar: Leaky ReLU uchun He initsializatsiyasi", blocks=[
        ("p", "Chuqur tarmoqda signal o‘nlab $z_{l+1}=W_{l+1}\\operatorname{LReLU}(z_l)$ qatlamlardan o‘tadi. Agar har bir qatlamda dispersiya 1 dan ozgina bo‘lsa ham farq qiladigan songa ko‘paytirilsa, 50 qatlamdan keyin bu signalning portlashi yoki yo‘qolishiga aylanadi. Shu ko‘paytuvchini hisoblaymiz."),
        ("deep", "Ko‘paytuvchini keltirib chiqarish", [
            ("p", "$W_{ij}$ vaznlar mustaqil, $\\mathbb E W_{ij}=0$, $\\operatorname{Var}W_{ij}=s^2$, $z_l$ kirishlar esa nolga nisbatan simmetrik bo‘lsin. $h_j=\\operatorname{LReLU}(z_{l,j})$ bo‘lgan bitta $z_{l+1,i}=\\sum_{j=1}^{n}W_{ij}h_j$ chiqish uchun:"),
            ("eq", r"\operatorname{Var}z_{l+1}=n\,s^2\,\mathbb E[h^2]=n\,s^2\,\frac{1+\alpha^2}{2}\operatorname{Var}z_l"),
            ("p", "Oxirgi tenglik — xossalar bo‘limidagi ikkinchi moment: $z_l^2$ ning yarmi musbat tarmoqdan to‘liq keladi, yarmi — manfiy tarmoqdan $\\alpha^2$ ga ko‘paytirilgan holda. Dispersiya saqlanishi uchun ko‘paytuvchi 1 ga teng bo‘lishi kerak:"),
            ("eq", r"s^2=\frac{2}{(1+\alpha^2)\,n_{\text{in}}}\qquad\Longleftrightarrow\qquad g=\sqrt n\,s=\sqrt{\frac{2}{1+\alpha^2}}"),
            ("p", "Teskari o‘tishda gradiyent $W^\\top$ ga va $\\operatorname{LReLU}'(z)$ ga ko‘paytiriladi, $\\mathbb E[\\operatorname{LReLU}'(z)^2]=\\frac{1+\\alpha^2}{2}$ esa — o‘sha ko‘paytuvchi. Shuning uchun bitta initsializatsiya ham to‘g‘ri signalni, ham gradiyentlarni saqlaydi."),
        ]),
        ("eq", r"\operatorname{Var}z_{l+1}=\frac{g^2(1+\alpha^2)}{2}\,\operatorname{Var}z_l,\qquad g_{\text{He}}=\sqrt{\frac{2}{1+\alpha^2}}"),
        ("p", "$\\alpha=0$ da ReLU uchun mashhur He (Kaiming) initsializatsiyasining $g=\\sqrt2$ qiymati chiqadi. Leaky ReLU uchun koeffitsiyent biroz kichikroq: $\\alpha=0{,}01$ da $1{,}414$, $\\alpha=0{,}2$ da $1{,}387$, $\\alpha=0{,}3$ da $1{,}355$."),
        ("viz", "leaky-relu-init", {"alpha": 0.3, "depth": 50}, "<b>5-rasm.</b> Kengligi 256 bo‘lgan tasodifiy tarmoqning har bir qatlamidagi pre-aktivatsiyalar RMS qiymati (vertikal shkala logarifmik). Standart holatda $\\alpha=0{,}3$, vaznlar esa «ReLU uchun» initsializatsiya qilingan, $g=\\sqrt2$: dispersiya ko‘paytuvchisi har qatlamda $1{,}09$, 50-qatlamgacha RMS $11{,}6$ gacha o‘sadi (nazariya — $11{,}7$). To‘g‘ri $g=\\sqrt{2/(1+\\alpha^2)}$ bilan ko‘paytuvchi 1 ga teng va 50-qatlamda RMS $1{,}34$ (nazariya — $1{,}35$). $g=1$ da ko‘paytuvchi $0{,}545$, signal esa $3{,}45\\cdot10^{-7}$ gacha so‘nadi."),
        ("callout", "note", "PyTorch’da", "Aynan shuni <code>nn.init.kaiming_normal_(w, a=alpha, nonlinearity='leaky_relu')</code> bajaradi: standart chetlanish $\\sqrt{2/((1+a^2)\\,n_{\\text{in}})}$. U yerda standart qiymat <code>a=0</code>, ya’ni oddiy ReLU uchun initsializatsiya — Leaky ReLU uchun <code>a</code> parametrini aniq berish kerak."),
    ]),
    dict(id="family", title="PReLU, RReLU va butun oila", blocks=[
        ("p", "$\\alpha$ ni qanday tanlash kerak? Uchta javob bor."),
        ("ul", [
            "<b>Qat’iy $\\alpha$</b> — klassik Leaky ReLU (Maas, Hannun, In, 2013, $\\alpha=0{,}01$). Bugun ko‘pincha $0{,}1$–$0{,}3$ olinadi: Syuy va boshq. (2015) taqqoslashida $\\alpha=1/5{,}5\\approx0{,}18$ li «kuchli oqadigan» variant $0{,}01$ dan yaxshiroq ishlagan.",
            "<b>O‘rganiladigan $\\alpha$</b> — PReLU (Parametric ReLU, Xe va boshq., 2015). $\\alpha$ parametrga aylanadi — qatlamga bitta yoki har kanalga bittadan — va vaznlar bilan birga gradiyent tushish orqali o‘rganiladi. PyTorch’da boshlang‘ich qiymat — $0{,}25$.",
            "<b>Tasodifiy $\\alpha$</b> — RReLU (Randomized ReLU): o‘qitishda $\\alpha$ har bir misol uchun $U(1/8;\\,1/3)$ tekis taqsimotdan olinadi (PyTorch’dagi standart chegaralar), xulosa chiqarishda — o‘rtacha $\\frac{1/8+1/3}{2}=\\frac{11}{48}\\approx0{,}229$. Shovqin regulyarizatsiya vazifasini bajaradi.",
        ]),
        ("p", "PReLU’da $\\alpha$ bo‘yicha gradiyent — hosila bo‘limidagi $\\min(0,\\,z)$: qiyalik faqat manfiy kirishlardan o‘rganadi. Gradiyent tushish vaznni ham, qiyalikni ham birdaniga qanday topishini ko‘raylik."),
        ("viz", "leaky-relu-prelu", {"w": 0.5, "a": 1.3}, "<b>6-rasm.</b> Ikki parametrli $\\operatorname{PReLU}_\\alpha(wx)$ model $w^*=1{,}5$, $\\alpha^*=0{,}2$ «o‘qituvchi» shovqin bilan yaratgan 31 nuqtadan o‘rganadi. O‘ngda — $L(w,\\alpha)$ xato sirti (qancha och bo‘lsa, shuncha kichik). $(0{,}5;\\,1{,}3)$ startdan $0{,}05$ qadamli gradiyent tushish 87 qadamda $w=1{,}521$, $\\alpha=0{,}209$ ga $0{,}0158$ xato bilan yetib keladi — bu shovqinli ma’lumotlar uchun minimum (o‘qituvchining o‘z xatosi $0{,}0170$). Startni boshqa joyga torting."),
        ("p", "PReLU har bir kanalga atigi bitta parametr qo‘shadi, lekin Xe va boshqalarning ishida yangi initsializatsiya bilan birga u juda chuqur konvolyutsion tarmoqlarni o‘qitish va ImageNet’da $4{,}94\\%$ top-5 xatoga erishish imkonini berdi — bu insonning taxminiy $5{,}1\\%$ xatosidan past. Mualliflar $\\alpha$ ga vaznlar so‘nishini (weight decay) qo‘llamaslikni ta’kidlaydi: u $\\alpha$ ni nolga, ya’ni ReLU’ga qaytaradi."),
        ("h3", "Silliq qarindoshlar"),
        ("p", "Noldagi sinishni silliqlash mumkin. ELU chap to‘g‘ri chiziqni $-\\alpha$ darajasida to‘yinadigan $\\alpha(e^x-1)$ eksponenta bilan almashtiradi. SELU masshtab qo‘shadi: $\\lambda\\approx1{,}0507$ va $\\alpha\\approx1{,}6733$ aktivatsiyalar nol o‘rtacha va birlik dispersiyani o‘zi saqlaydigan qilib tanlangan. <a href=\"../gelu/\">GELU</a> va <a href=\"../silu/\">SiLU</a> — bugungi transformerlarda turadigan silliq va hatto nomonoton funksiyalar."),
        ("viz", "leaky-relu-zoo", {"cmp": "elu", "x": -2}, "<b>7-rasm.</b> $\\alpha=0{,}1$ li Leaky ReLU qarindoshlari yonida. Kursorni olib boring: $x=-2$ da Leaky ReLU $-0{,}2$, ELU — $-0{,}865$, SELU — $-1{,}520$, GELU — $-0{,}046$, SiLU — $-0{,}238$ beradi. Hosilalarga o‘ting: Leaky ReLU va SELU’da bu nolda uzilishli zina (SELU’da chapda $\\lambda\\alpha\\approx1{,}758$, o‘ngda $\\lambda\\approx1{,}051$), ELU, GELU va SiLU’da — uzluksiz egri chiziq."),
        ("table", ["Funksiya", "$x\\le0$ da", "Chapdagi hosila", "Xususiyati"], "FAMILY", {}),
    ]),
    dict(id="code", title="Kodda", blocks=[
        ("p", "NumPy’da Leaky ReLU — bitta qator. <code>np.maximum(alpha * x, x)</code> dan ko‘ra <code>np.where</code> yozish ishonchliroq: ikkinchi yozuv $\\alpha&gt;1$ da jimgina buziladi."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Kutubxonalardagi standart qiymatlar har xil", "PyTorch <code>nn.LeakyReLU</code>: <code>negative_slope=0.01</code>. TensorFlow <code>tf.nn.leaky_relu</code>: <code>alpha=0.2</code>. Keras <code>layers.LeakyReLU</code>: $0{,}3$. Uchta freymvorkdagi bitta «Leaky ReLU» — uchta har xil funksiya. Modelni ko‘chirishda $\\alpha$ ni aniq ko‘rsating."),
        ("p", "Hisoblash nuqtai nazaridan Leaky ReLU xavfsiz: eksponenta ham, bo‘lish ham, to‘lib ketish ham yo‘q. Yagona nozik joy — PyTorch’dagi <code>inplace=True</code>: u xotirani tejaydi, lekin grafning boshqa amallariga kerak bo‘lishi mumkin bo‘lgan kirishni qayta yozadi."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b>$\\alpha&gt;1$ da <code>max(alpha * x, x)</code> yozuvi.</b> Formula faqat $\\alpha\\le1$ da to‘g‘ri; katta $\\alpha$ larda boshqa funksiya chiqadi. Xavfsiz yozuv — <code>where(x &gt; 0, x, alpha * x)</code>.",
            "<b>Juda katta $\\alpha$.</b> $\\alpha\\to1$ da nochiziqlilik ulushi $\\frac{1-\\alpha}{2}$ nolga intiladi, funksiya deyarli chiziqli bo‘lib qoladi va chuqur tarmoq ifodalash kuchini yo‘qotadi. Oqilona oraliq — $0{,}01$ dan $0{,}3$ gacha.",
            "<b>$\\alpha$ ga tuzatishsiz «ReLU uchun» initsializatsiya.</b> Har qatlamda dispersiya ko‘paytuvchisi $1+\\alpha^2$: $\\alpha=0{,}3$ da 50 qatlamda signal taxminan 8 marta o‘sadi (5-rasm). $\\alpha$ ni <code>kaiming_normal_(..., a=alpha)</code> ga bering.",
            "<b>Leaky ReLU beqaror o‘qitishni o‘zi davolaydi degan umid.</b> U nol gradiyentni yo‘qotadi, lekin sababini emas: juda katta o‘qitish tezligi baribir xavfli.",
            "<b>PReLU’ning $\\alpha$ siga vaznlar so‘nishi.</b> U $\\alpha$ ni nolga tortadi va PReLU ReLU’ga aylanadi. $\\alpha$ ni weight decay qo‘llanadigan parametrlar guruhidan chiqaring.",
            "<b>Har xil standart qiymatlar</b> PyTorch ($0{,}01$), TensorFlow ($0{,}2$) va Keras’da ($0{,}3$): modelni freymvorklar o‘rtasida ko‘chirganda natija jimgina o‘zgaradi.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘lanishlar", blocks=[
        ("ul", [
            "<a href=\"../relu/\">ReLU</a>: $\\alpha=0$ xususiy hol; «o‘layotgan ReLU» haqida batafsil — o‘sha yerda.",
            "<a href=\"../silu/\">SiLU / Swish</a> va <a href=\"../gelu/\">GELU</a>: chapda ham kichik manfiy signalni o‘tkazadigan, lekin keyin uni so‘ndiradigan silliq aktivatsiyalar.",
            "<a href=\"../sigmoid/\">Sigmoida</a> va <a href=\"../tanh/\">tanh</a>: to‘yinadigan aktivatsiyalar; Leaky ReLU’da to‘yinish umuman yo‘q, demak, to‘yinish tufayli gradiyent so‘nishi ham yo‘q.",
            "<a href=\"../mse/\">MSE</a>: 3 va 6-rasmlardagi tajribalarning yo‘qotish funksiyasi.",
            "<a href=\"../sgd/\">SGD</a> va <a href=\"../adam/\">Adam</a>: optimizatorning juda katta qadami — ReLU neyronlari o‘limining asosiy sababi.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $x&gt;0$ da $\\operatorname{LReLU}_\\alpha(x)=x$, $x\\le0$ da $\\alpha x$; bu $\\alpha\\le1$ da $\\max(\\alpha x,x)$ ga va istalgan $\\alpha$ da $\\frac{1+\\alpha}{2}x+\\frac{1-\\alpha}{2}|x|$ ga teng. 2) Hosila — $\\alpha$ va $1$ dan iborat zina: gradiyent nolga aylanmaydi, neyron muzlamaydi. 3) Murosa: katta $\\alpha$ neyronlarni tezroq jonlantiradi, lekin funksiyani chiziqliga yaqinlashtiradi. 4) Leaky ReLU tarmog‘i — tekis «o‘lik» platolarsiz bo‘lak-chiziqli funksiya. 5) Initsializatsiya: $\\operatorname{Var}w=\\frac{2}{(1+\\alpha^2)\\,n_{\\text{in}}}$. 6) PReLU $\\alpha$ ni $\\min(0,z)$ gradiyent orqali o‘rganadi."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="$\\alpha=0{,}2$ da $\\operatorname{LReLU}(-5)$ nimaga teng?", options=["$0$", "$-1$", "$-5$", "$1$"], answer=1,
                 explain="Kirish manfiy, shuning uchun $\\alpha x=0{,}2\\cdot(-5)=-1$ tarmog‘i ishlaydi."),
            dict(q="$x&lt;0$ da Leaky ReLU hosilasi nimaga teng?", options=["$0$", "$1$", "$\\alpha$", "$\\alpha x$"], answer=2,
                 explain="Chapda funksiya — $\\alpha x$ to‘g‘ri chiziq, uning qiyaligi $\\alpha$. Shuning uchun gradiyent nolga aylanmaydi."),
            dict(q="Qaysi $\\alpha$ larda $\\operatorname{LReLU}_\\alpha(x)=\\max(\\alpha x,x)$ to‘g‘ri?", options=["Istalgan $\\alpha$ da", "Faqat $\\alpha\\le1$ da", "Faqat $\\alpha&gt;1$ da", "Faqat $\\alpha=0{,}01$ da"], answer=1,
                 explain="$\\alpha\\le1$ da o‘ngda $x\\ge\\alpha x$, chapda $\\alpha x\\ge x$. $\\alpha&gt;1$ da o‘ngda maksimum $\\alpha x$ ni tanlaydi — boshqa funksiya chiqadi."),
            dict(q="Leaky ReLU’li ($\\alpha=0{,}3$) tarmoq «ReLU uchun», $g=\\sqrt2$ bilan initsializatsiya qilingan. Har qatlamdagi dispersiya ko‘paytuvchisi qancha?", options=["$1$", "$1{,}09$", "$0{,}545$", "$2$"], answer=1,
                 explain="$g^2(1+\\alpha^2)/2=2\\cdot1{,}09/2=1{,}09$. 50 qatlamda RMS taxminan $1{,}09^{24{,}5}\\approx8{,}3$ marta o‘sadi."),
            dict(q="ReLU neyron barcha misollarda $z&lt;0$ oladi. Qaysi biri to‘g‘ri?", options=["Uning parametrlari bo‘yicha gradiyentlar nolga teng va gradiyent tushish uni boshqa o‘zgartirmaydi", "Gradiyent kichik, lekin nol emas", "Neyron manfiy qiymatlar chiqaradi", "O‘qitish tezligini kamaytirish kifoya, u jonlanadi"], answer=0,
                 explain="$z&lt;0$ da $\\operatorname{ReLU}'(z)=0$, shuning uchun barcha gradiyentlar nolga aylanadi — bu o‘lik neyron. Qadamni kamaytirish yordam bermaydi: nolga ko‘paytirilgan qadam nolligicha qoladi."),
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
            elif _b[0] == "table" and _b[2] == "FAMILY":
                _sec["blocks"][_i] = (_b[0], _b[1], FAMILY[_lang], _b[3])
            elif _b[0] == "code" and _b[2] in ("CODE_NUMPY", "CODE_TORCH"):
                _sec["blocks"][_i] = (_b[0], _b[1], _code(CODE_NUMPY if _b[2] == "CODE_NUMPY" else CODE_TORCH, _lang))
