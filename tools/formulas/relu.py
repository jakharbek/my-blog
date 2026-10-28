"""Formula page: ReLU, the rectified linear unit. Format: see README.md, reference page: sigmoid.py."""

META = dict(
    id="relu",
    date="2026-10-28",
    minutes=35,
    hero=r"\operatorname{ReLU}(x)=\max(0,\,x)",
    title={"ru": "ReLU: выпрямленная линейная функция", "en": "ReLU: the rectified linear unit", "uz": "ReLU: to‘g‘rilangan chiziqli funksiya"},
    dek={
        "ru": "Самая простая нелинейность и рабочая лошадка глубокого обучения. Разбираем по косточкам: почему одного излома хватает, чтобы собрать любую ломаную, что такое производная в точке излома, как сеть из ReLU режет пространство на линейные куски, почему нейроны «умирают» и откуда в инициализации Хе двойка.",
        "en": "The simplest nonlinearity and the workhorse of deep learning. We take it apart bone by bone: why a single kink is enough to build any broken line, what the derivative at the kink is, how a ReLU network cuts space into linear pieces, why neurons “die”, and where the 2 in He initialization comes from.",
        "uz": "Eng sodda nochiziqlilik va chuqur o‘qitishning ishchi oti. Mayda detallarigacha tahlil qilamiz: nega istalgan siniq chiziqni yig‘ish uchun bitta sinish yetarli, sinish nuqtasidagi hosila nima, ReLU tarmog‘i fazoni qanday qilib chiziqli bo‘laklarga ajratadi, nega neyronlar «o‘ladi» va He initsializatsiyasidagi ikki qayerdan keladi.",
    },
    description={
        "ru": "ReLU подробно: формула и её записи, сумма изломов, субградиент в нуле, softplus, линейные области сети в 3D, обучение ломаной, умирающие нейроны, инициализация Хе, код на NumPy и PyTorch.",
        "en": "ReLU in depth: the formula and its forms, sums of hinges, the subgradient at zero, softplus, a network’s linear regions in 3D, learning a broken line, dying neurons, He initialization, NumPy and PyTorch code.",
        "uz": "ReLU batafsil: formula va uning yozuvlari, sinishlar yig‘indisi, noldagi subgradiyent, softplus, 3D’da tarmoqning chiziqli sohalari, siniq chiziqni o‘rganish, o‘layotgan neyronlar, He initsializatsiyasi, NumPy va PyTorch kodi.",
    },
)

TABLE = [("-3", "0", "0"), ("-1", "0", "0"), ("-0.5", "0", "0"), ("0", "0", "[0; 1]"), ("0.5", "0.5", "1"), ("1", "1", "1"), ("2.5", "2.5", "1")]


def _table(lang):
    dec = "." if lang == "en" else ","
    m = lambda v: v.replace("-", "−").replace(".", dec)
    rows = [[m(a), m(b), m(c)] for a, b, c in TABLE]
    if lang == "en":
        rows[3][2] = "[0, 1]"
    return rows


CODE_NUMPY = '''import numpy as np

def relu(x):
    return np.maximum(0.0, x)

def relu_grad(x):
    # субградиент: в точке 0 берём 0, как PyTorch и TensorFlow
    return (x > 0).astype(float)

x = np.array([-3.0, 0.0, 2.5])
print(relu(x), relu_grad(x))     # [0.  0.  2.5] [0. 0. 1.]

# «Мёртвые» нейроны: ни одного положительного входа на всём наборе данных
rng = np.random.default_rng(0)
X = rng.normal(size=(1000, 20))
W = rng.normal(size=(20, 64)) * np.sqrt(2 / 20)   # инициализация Хе
for b0 in (0.0, -5.0):
    Z = X @ W + b0
    dead = np.mean((Z > 0).sum(axis=0) == 0)
    print(b0, f"{dead:.0%}")     # 0.0 0%  и  -5.0 66%'''

CODE_TORCH = '''import torch
import torch.nn as nn

x = torch.tensor([-1.0, 0.0, 2.0], requires_grad=True)
torch.relu(x).sum().backward()
print(x.grad)                    # tensor([0., 0., 1.]) — в нуле 0

# Инициализация Хе: Var w = 2 / fan_in
layer = nn.Linear(512, 512)
nn.init.kaiming_normal_(layer.weight, mode="fan_in", nonlinearity="relu")
nn.init.zeros_(layer.bias)

# Блок FFN исходного Transformer: Linear → ReLU → Linear
ffn = nn.Sequential(nn.Linear(512, 2048), nn.ReLU(), nn.Linear(2048, 512))
# nn.ReLU(inplace=True) экономит память, но портит вход, если он ещё нужен'''


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("субградиент: в точке 0 берём 0, как PyTorch и TensorFlow", "subgradient: take 0 at the point 0, like PyTorch and TensorFlow"),
               ("«Мёртвые» нейроны: ни одного положительного входа на всём наборе данных", "“Dead” neurons: not a single positive input on the whole dataset"),
               ("инициализация Хе", "He initialization"), ("0.0 0%  и  -5.0 66%", "0.0 0%  and  -5.0 66%"),
               ("в нуле 0", "0 at zero"), ("Инициализация Хе", "He initialization"),
               ("Блок FFN исходного Transformer", "The FFN block of the original Transformer"),
               ("экономит память, но портит вход, если он ещё нужен", "saves memory but overwrites the input if it is still needed")],
        "uz": [("субградиент: в точке 0 берём 0, как PyTorch и TensorFlow", "subgradiyent: 0 nuqtada PyTorch va TensorFlow kabi 0 olamiz"),
               ("«Мёртвые» нейроны: ни одного положительного входа на всём наборе данных", "«O‘lik» neyronlar: butun ma’lumotlar to‘plamida birorta ham musbat kirish yo‘q"),
               ("инициализация Хе", "He initsializatsiyasi"), ("0.0 0%  и  -5.0 66%", "0.0 0%  va  -5.0 66%"),
               ("в нуле 0", "nolda 0"), ("Инициализация Хе", "He initsializatsiyasi"),
               ("Блок FFN исходного Transformer", "Asl Transformer’ning FFN bloki"),
               ("экономит память, но портит вход, если он ещё нужен", "xotirani tejaydi, lekin kirish hali kerak bo‘lsa, uni buzadi")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем он нужен", blocks=[
        ("p", r"Без нелинейности нейросеть бесполезна: композиция линейных слоёв — снова линейная функция, сколько слоёв ни ставь. Нужна функция, которая «ломает» линейность, но при этом дёшево считается и не душит градиент. ReLU (rectified linear unit, «выпрямленная линейная функция») делает минимально возможное: положительное пропускает как есть, отрицательное заменяет нулём."),
        ("p", r"Где он встречается:"),
        ("ul", [
            r"<b>свёрточные сети</b> — AlexNet, VGG, ResNet: ReLU после каждой свёртки;",
            r"<b>полносвязные сети и табличные модели</b> — выбор по умолчанию для скрытых слоёв;",
            r"<b>исходный Transformer</b> (2017) — блок FFN: $\max(0,\,xW_1+b_1)W_2+b_2$; современные LLM перешли на его гладкие родственники <a href='../gelu/'>GELU</a> и <a href='../silu/'>SiLU</a>;",
            r"<b>мобильные сети</b> — ReLU6 $=\min(\max(0,x),\,6)$ в MobileNet удобна для вычислений с малой разрядностью;",
            r"<b>внутри других формул</b> — $\max(0,\cdot)$ это и hinge-потеря SVM, и <a href='../triplet/'>triplet loss</a>, и положительная часть числа $x^+$.",
        ]),
        ("callout", "key", "Главное за минуту", r"$\operatorname{ReLU}(x)=\max(0,x)$: ноль слева, прямая $y=x$ справа. Производная — ступенька: 0 при $x&lt;0$ и 1 при $x&gt;0$; в нуле производной нет, библиотеки берут 0. Справа градиент проходит без ослабления — поэтому глубокие сети с ReLU учатся быстро. Плата — «мёртвые» нейроны, у которых вход всегда отрицателен."),
    ]),
    dict(id="intuition", title="Интуиция: выпрямитель", blocks=[
        ("p", r"Название пришло из электроники: диод-выпрямитель пропускает ток в одну сторону и не пропускает в другую. Нейрон с ReLU — это датчик: пока признак ниже порога, он молчит; как только порог пройден, отвечает пропорционально тому, насколько сильно."),
        ("p", r"Потяните точку. Справа от нуля касательная совпадает с самой функцией (наклон 1), слева лежит на оси (наклон 0). В нуле единственной касательной нет: любая прямая с наклоном от 0 до 1 касается графика снизу — это <b>опорные прямые</b>."),
        ("viz", "relu-explorer", {"x": 1.5}, r"<b>Рисунок 1.</b> ReLU, касательная и производная (снизу). При $x=1{,}5$: $\operatorname{ReLU}=1{,}5$, $\operatorname{ReLU}'=1$. Подведите точку к нулю: производная не определена, множество наклонов опорных прямых — отрезок $[0;\,1]$ (субдифференциал); PyTorch и TensorFlow берут из него 0."),
        ("callout", "intuition", "Что заметить", r"У ReLU нет насыщения справа: при $x=100$ производная та же 1, что и при $x=0{,}1$. У <a href='../sigmoid/'>сигмоиды</a> и <a href='../tanh/'>tanh</a> при $|x|=5$ производная уже меньше $0{,}01$. Зато слева ReLU «насыщен» полностью: производная ровно 0."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", r"Одну и ту же функцию полезно узнавать в разных записях — каждая подсвечивает своё свойство:"),
        ("eq", r"\operatorname{ReLU}(x)=\max(0,x)=\begin{cases}x, & x>0\\0, & x\le0\end{cases}=\frac{x+|x|}{2}=x\cdot\mathbb 1[x>0]"),
        ("symbols", [
            (r"\max(0,x)", r"сравнение с нулём — одна операция, без экспонент и делений;"),
            (r"\frac{x+|x|}{2}", r"при $x&gt;0$ слагаемые равны и дают $x$, при $x&lt;0$ они взаимно уничтожаются;"),
            (r"x\cdot\mathbb 1[x>0]", r"<b>вентиль</b>: вход умножается на 0 или 1 в зависимости от знака. Для каждого примера сеть с ReLU — это линейная сеть, в которой часть нейронов выключена."),
        ]),
        ("table", ["$x$", r"$\operatorname{ReLU}(x)$", r"$\operatorname{ReLU}'(x)$"], "TABLE", {"num": [0, 1, 2]}),
        ("h3", "Из изломов — любая ломаная"),
        ("p", r"Нейрон $v\cdot\operatorname{ReLU}(x-c)$ — это «шарнир» (hinge): ноль до точки $c$, затем прямая с наклоном $v$. Складывая шарниры с разными $c$, получаем ломаную: в каждой точке $c_k$ наклон меняется ровно на $v_k$. Например, $\operatorname{ReLU}(x+1)-2\operatorname{ReLU}(x)+\operatorname{ReLU}(x-1)$ — «шапочка» высотой 1."),
        ("viz", "relu-hinges", {"v1": 1, "v2": -2, "v3": 1}, r"<b>Рисунок 2.</b> Сумма трёх шарниров с изломами в $-1$, $0$, $1$. При весах $(1;\,-2;\,1)$ получается шапочка: наклоны участков $0,\ 1,\ -1,\ 0$, высота $f(0)=1$. Снизу — производная: ступенчатая функция, которая в точке $c_k$ прыгает ровно на $v_k$."),
        ("p", r"Это и есть главный секрет ReLU-сетей: любая непрерывная кусочно-линейная функция на прямой с $m$ изломами — это линейная функция плюс $m$ шарниров, то есть сеть с одним скрытым слоем из $m$ нейронов (плюс линейная часть, которую тоже можно выразить двумя нейронами: $x=\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)$). А ломаными можно сколь угодно точно приблизить любую непрерывную функцию на отрезке."),
    ]),
    dict(id="properties", title="Свойства", blocks=[
        ("ul", [
            r"<b>Область значений</b> — $[0;\,+\infty)$: сверху не ограничена, в отличие от сигмоиды и tanh.",
            r"<b>Кусочная линейность</b>: два линейных куска, один излом в нуле.",
            r"<b>Непрерывность и липшицевость</b> с константой 1: $|\operatorname{ReLU}(a)-\operatorname{ReLU}(b)|\le|a-b|$.",
            r"<b>Выпуклость</b>: график лежит не выше любой хорды — максимум двух линейных функций всегда выпукл.",
            r"<b>Положительная однородность</b>: $\operatorname{ReLU}(\alpha x)=\alpha\operatorname{ReLU}(x)$ при $\alpha\ge0$. Масштаб можно переносить между слоями: умножив веса слоя на $\alpha&gt;0$, а следующего — на $1/\alpha$, получим ту же сеть.",
            r"<b>Идемпотентность</b>: $\operatorname{ReLU}(\operatorname{ReLU}(x))=\operatorname{ReLU}(x)$.",
            r"<b>Разложение числа</b>: $x=\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)$ и $|x|=\operatorname{ReLU}(x)+\operatorname{ReLU}(-x)$.",
            r"<b>Разреженность</b> (sparsity): если входы нейронов симметричны относительно нуля, примерно половина выходов — точные нули.",
        ]),
        ("deep", "Доказательства: выпуклость и однородность", [
            ("p", r"Выпуклость. Для $t\in[0;1]$ и любых $a,b$: $\max(0,\,ta+(1-t)b)\le\max\bigl(0,\,t\max(0,a)+(1-t)\max(0,b)\bigr)=t\max(0,a)+(1-t)\max(0,b)$, потому что $a\le\max(0,a)$, $b\le\max(0,b)$, а правая часть неотрицательна."),
            ("p", r"Однородность. При $\alpha&gt;0$ знак $\alpha x$ совпадает со знаком $x$, поэтому $\max(0,\alpha x)=\alpha\max(0,x)$; при $\alpha=0$ обе части равны 0. При $\alpha&lt;0$ равенство нарушается: $\operatorname{ReLU}(-x)\ne-\operatorname{ReLU}(x)$ — функция не нечётна."),
        ]),
    ]),
    dict(id="derivative", title="Производная, субградиент и гладкие родственники", blocks=[
        ("eq", r"\operatorname{ReLU}'(x)=\begin{cases}1, & x>0\\0, & x<0\end{cases},\qquad \partial\operatorname{ReLU}(0)=[0,\,1]"),
        ("deep", "Почему в нуле производной нет", [
            ("p", r"Производная — предел разностного отношения. Справа и слева от нуля он разный:"),
            ("eq", r"\lim_{h\to0^+}\frac{\operatorname{ReLU}(h)-0}{h}=\lim_{h\to0^+}\frac{h}{h}=1,\qquad \lim_{h\to0^-}\frac{\operatorname{ReLU}(h)-0}{h}=\lim_{h\to0^-}\frac{0}{h}=0"),
            ("p", r"Односторонние производные не совпадают, значит, обычной производной нет. Для выпуклых функций есть замена — <b>субградиент</b>: число $g$, для которого $f(y)\ge f(x)+g(y-x)$ при всех $y$, то есть прямая с наклоном $g$ лежит под графиком. В нуле так ведут себя все $g\in[0;1]$: это множество называют субдифференциалом $\partial\operatorname{ReLU}(0)$."),
        ]),
        ("p", r"Почему это не мешает обучению: вход нейрона ровно равен нулю с вероятностью 0 для непрерывных данных, а в редких точных нулях подойдёт любое значение из $[0;1]$ — сходимость субградиентных методов это допускает. Библиотеки по соглашению берут 0."),
        ("p", r"Вторая производная равна нулю везде, кроме нуля (в смысле обобщённых функций $\operatorname{ReLU}''=\delta(x)$). Поэтому внутри каждой линейной области сеть из ReLU — аффинная функция входа, а её градиент по входу кусочно-постоянен."),
        ("h3", "Softplus: сглаженный ReLU"),
        ("p", r"Если излом мешает (например, нужна гладкая функция для оптимизации второго порядка или физической модели), его можно скруглить:"),
        ("eq", r"\operatorname{softplus}_\beta(x)=\frac1\beta\ln\bigl(1+e^{\beta x}\bigr),\qquad \operatorname{softplus}_\beta'(x)=\sigma(\beta x)"),
        ("p", r"Разность $\operatorname{softplus}_\beta(x)-\operatorname{ReLU}(x)=\frac1\beta\ln\bigl(1+e^{-\beta|x|}\bigr)$ максимальна в нуле и равна $\frac{\ln2}{\beta}$; при $\beta\to\infty$ softplus стремится к ReLU, а производная-<a href='../sigmoid/'>сигмоида</a> — к ступеньке. В нуле она всегда равна $\sigma(0)=0{,}5$ — середине субдифференциала $[0;1]$."),
        ("viz", "relu-smooth", {"beta": 1}, r"<b>Рисунок 3.</b> Сверху ReLU и $\operatorname{softplus}_\beta$, снизу их производные. При $\beta=1$ наибольший разрыв $\ln2\approx0{,}693$, при $\beta=4$ — $0{,}173$, при $\beta=32$ — $0{,}022$. Производная softplus в нуле всегда $0{,}5$."),
    ]),
    dict(id="space", title="ReLU-сеть в пространстве: линейные области", blocks=[
        ("p", r"Нейрон первого слоя с двумя входами выключен по одну сторону прямой $w^\top x+b=0$ и линеен по другую. Каждая такая прямая — линия сгиба. $H$ нейронов разрезают плоскость на области, и в каждой области набор включённых нейронов (<b>паттерн активаций</b>) постоянен, а значит, сеть — обычная аффинная функция. Поверхность выхода — многогранник, склеенный из плоских граней."),
        ("viz", "relu-surface", {"arch": "n4", "seed": 3}, r"<b>Рисунок 4.</b> Слева — выход сети $f(x_1,x_2)=\sum_k v_k\operatorname{ReLU}(w_k^\top x+b_k)$ в 3D: плоские грани и рёбра-сгибы. Справа — вид сверху: цвет — номер линейной области, пунктир — прямые нейронов, тонкие линии — уровни $f$ (они ломаются на границах). При 4 нейронах в окне 10 областей из возможных 11 ($1+H+\tfrac{H(H-1)}{2}$); при 8 нейронах — 25 из 37. Два слоя по 4 нейрона дают уже 30 областей: границы второго слоя изгибаются на границах первого."),
        ("p", r"$H$ прямых общего положения делят плоскость максимум на $1+H+\binom H2$ частей — число областей одного слоя растёт полиномиально. Глубина работает иначе: каждый следующий слой «складывает» уже разрезанное пространство, и число областей может расти экспоненциально с числом слоёв (Монтуфар и др., 2014). Это одно из объяснений, почему глубокие сети выразительнее широких при том же числе нейронов."),
        ("callout", "note", "Универсальная аппроксимация", r"Сеть с одним скрытым слоем ReLU и достаточным числом нейронов приближает любую непрерывную функцию на ограниченном замкнутом множестве с любой точностью (Лешно и др., 1993: подходит любая непрерывная активация, не являющаяся многочленом). Для ReLU это видно буквально: ломаные — из шарниров, многогранные поверхности — из складок."),
    ]),
    dict(id="training", title="ReLU в обучении: сеть рисует ломаную", blocks=[
        ("p", r"Обучим один скрытый слой $\hat y(x)=\sum_{k=1}^{H}v_k\operatorname{ReLU}(w_kx+b_k)+c$ на точках синусоиды. Каждый нейрон — шарнир с изломом в $x=-b_k/w_k$; градиентный спуск сдвигает изломы туда, где кривая изгибается, и подбирает наклоны."),
        ("eq", r"\frac{\partial\hat y}{\partial b_k}=v_k\,\mathbb 1[w_kx+b_k>0],\qquad \frac{\partial\hat y}{\partial w_k}=v_k\,x\,\mathbb 1[w_kx+b_k>0]"),
        ("p", r"Градиент по параметрам нейрона приходит только от тех точек, где нейрон включён. Если таких точек нет совсем, нейрон перестаёт учиться — это и есть «умирание»."),
        ("viz", "relu-fit", {"h": 6}, r"<b>Рисунок 5.</b> 40 точек $y=\sin(1{,}6x)$ с шумом ($\sigma=0{,}08$), полный градиент и <a href='../adam/'>Adam</a> с шагом $0{,}02$. Бирюзовые линии — шарниры, точки внизу — их изломы, красный пунктир — мёртвые нейроны. С 6 нейронами MSE падает с $3{,}102$ до $0{,}267$ к шагу 100, $0{,}012$ к шагу 300 и $0{,}0090$ к шагу 1500; по дороге один нейрон умирает. С 3 нейронами ломаная слишком грубая — $0{,}265$; с 12 итог $0{,}0101$, но мёртвы уже 4 из 12."),
        ("callout", "note", "Что видно на рисунке", r"Сеть из ReLU не умеет рисовать гладкое — только ломаные. Изломы собираются там, где синусоида сильнее всего изгибается, а на почти прямых участках их нет. Лишние нейроны не обязательно помогают: часть из них умирает или дублирует соседей."),
    ]),
    dict(id="dying", title="Умирающий ReLU", blocks=[
        ("p", r"Нейрон «мёртв», если на всех обучающих примерах $w^\top x+b\le0$. Тогда его выход всегда 0, градиенты по $w$ и $b$ всегда 0 (см. формулу выше), и никакой шаг оптимизатора его не оживит: при обучении на тех же данных он останется выключенным навсегда."),
        ("p", r"Как это происходит: один большой шаг градиентного спуска сильно уменьшает сдвиг $b$ или поворачивает $w$ так, что гиперплоскость нейрона уходит за пределы облака данных. Чем больше шаг обучения, тем чаще это случается."),
        ("viz", "relu-dead", {"lr": 0.3}, r"<b>Рисунок 6.</b> Сеть из 64 нейронов ReLU на 128 точках $y=\sin(3x_1)+x_2$, $x\in[-1;1]^2$, мини-батчи по 16, обычный SGD, 600 шагов, одна и та же инициализация Хе. Справа — нейроны: синие живы (яркость — доля точек, где нейрон включён), красные мертвы. При $\eta=0{,}3$ уже за первые 5 шагов умирает $91\%$ нейронов, к концу — $97\%$, MSE застревает на $0{,}137$. При $\eta=0{,}2$ мертва четверть ($27\%$), MSE $0{,}004$; при $\eta=0{,}1$ и $0{,}03$ мёртвых нет (MSE $0{,}005$ и $0{,}041$ — малый шаг просто медленнее)."),
        ("p", r"Как лечить:"),
        ("ul", [
            r"<b>умеренный шаг обучения</b>, разогрев (warm-up) и обрезка градиента;",
            r"<b>адаптивные оптимизаторы</b> (<a href='../adam/'>Adam</a>) и нормализация (BatchNorm, LayerNorm): они держат входы нейронов около нуля;",
            r"<b>активации с ненулевым наклоном слева</b> — <a href='../leaky-relu/'>Leaky ReLU</a>, PReLU, ELU, <a href='../gelu/'>GELU</a>, <a href='../silu/'>SiLU</a>: градиент слева не равен нулю, и нейрон может вернуться;",
            r"<b>аккуратная инициализация</b>: сдвиги 0 (иногда небольшой положительный), веса по Хе. Сильно отрицательные сдвиги убивают нейроны ещё до обучения.",
        ]),
    ]),
    dict(id="init", title="Инициализация Хе: откуда двойка", blocks=[
        ("p", r"Пусть $z=\sum_{j=1}^{n}w_jh_j$, веса независимы, $\mathbb Ew_j=0$, $\operatorname{Var}w_j=c/n$. Тогда $\operatorname{Var}z=c\cdot q$, где $q=\mathbb E[h^2]$ — средний квадрат входов. Если $z$ симметрична относительно нуля, ReLU обнуляет ровно половину её распределения, и"),
        ("eq", r"q_{l}=\mathbb E\bigl[\operatorname{ReLU}(z)^2\bigr]=\frac12\operatorname{Var}z=\frac c2\,q_{l-1}\qquad\Longrightarrow\qquad q_L=q_0\Bigl(\frac c2\Bigr)^{L}"),
        ("p", r"При $c=1$ (как для tanh) сигнал вдвое слабеет на каждом слое, при $c=3$ — растёт в полтора раза. Сохраняет масштаб только $c=2$: это <b>инициализация Хе</b> (He et al., 2015), $\operatorname{Var}w=2/n_\text{in}$. Обратный проход ведёт себя так же, поэтому градиенты тоже не затухают и не взрываются."),
        ("viz", "relu-depth", {"c": 2}, r"<b>Рисунок 7.</b> Средний квадрат активаций $q_l$ на каждом из 30 слоёв случайной сети ширины 100 (логарифмическая шкала), оранжевый пунктир — теория $q_0(c/2)^l$. При $c=2$ отношение $q_{30}/q_0=2{,}66$; при $c=1$ — $2{,}47\cdot10^{-9}$ (теория $9{,}3\cdot10^{-10}$); при $c=3$ — $5{,}1\cdot10^5$ (теория $1{,}9\cdot10^5$). Множитель $\approx2{,}66$ во всех трёх случаях один и тот же: веса одинаковые, а ReLU положительно однороден, поэтому $c$ лишь умножает весь сигнал на $(c/2)^{L/2}$; отклонение от теории — случайная флуктуация конечной ширины. Активна $51\%$ нейронов последнего слоя."),
        ("callout", "history", "Немного истории", r"Идея выпрямителя давняя: её использовал ещё Фукусима (1969). В глубокое обучение ReLU вошёл в 2010–2011 годах (Наир и Хинтон; Глоро, Борд и Бенжио), а в AlexNet (2012) сеть с ReLU достигла ошибки 25% на обучающей выборке CIFAR-10 в 6 раз быстрее, чем с tanh. В 2015 году Хе и соавторы вывели инициализацию $2/n$ и обучили сети с ReLU-семейством глубиной в десятки слоёв."),
    ]),
    dict(id="code", title="В коде", blocks=[
        ("p", r"ReLU не переполняется и не теряет точность: сравнение с нулём точно в любой арифметике. Внимание стоит уделить другому: соглашению в нуле, мёртвым нейронам и инициализации."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Правило", r"ReLU — плюс инициализация Хе (<code>kaiming_normal_</code> с <code>nonlinearity='relu'</code>), сдвиги 0, разумный шаг обучения. Время от времени проверяйте долю нейронов, которые ни разу не включились на батче: если она растёт, уменьшите шаг или перейдите на Leaky ReLU / GELU."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            r"<b>ReLU на выходе регрессии, где цель может быть отрицательной.</b> Сеть физически не сможет выдать $y&lt;0$. На выходе регрессии — линейный слой; ReLU на выходе уместен только для заведомо неотрицательных величин (и то лучше softplus).",
            r"<b>Инициализация как для tanh.</b> С $\operatorname{Var}w=1/n$ сигнал в глубокой ReLU-сети затухает как $2^{-L}$: через 30 слоёв в $2^{30}\approx10^9$ раз (рисунок 7). Берите инициализацию Хе.",
            r"<b>Слишком большой шаг обучения.</b> Массово убивает нейроны, и восстановить их нельзя (рисунок 6). Симптом — потери застыли, а доля нулевых активаций близка к 100%.",
            r"<b>«Производная ReLU в нуле равна 1/2» или «не определена — значит, ошибка».</b> Математически в нуле есть субдифференциал $[0;1]$, любое его значение допустимо; библиотеки берут 0. На обучение это не влияет.",
            r"<b><code>inplace=True</code> там, где вход нужен дальше.</b> Операция затирает вход; если он используется в остаточной связи или для обратного прохода другой операции, PyTorch выдаст ошибку или результат будет неверным.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            r"<a href='../leaky-relu/'>Leaky ReLU</a>: $\max(\alpha x,x)$ — ненулевой наклон $\alpha$ слева лечит умирание.",
            r"<a href='../gelu/'>GELU</a> и <a href='../silu/'>SiLU</a>: $x\Phi(x)$ и $x\sigma(x)$ — гладкие «вентили» вместо жёсткого $x\cdot\mathbb 1[x&gt;0]$; вдали от нуля ведут себя как ReLU.",
            r"<a href='../sigmoid/'>Сигмоида</a>: производная softplus — это $\sigma(\beta x)$; ReLU вытеснил сигмоиду из скрытых слоёв из-за насыщения.",
            r"<a href='../tanh/'>tanh</a>: насыщается с обеих сторон; для tanh — инициализация Ксавье, для ReLU — Хе.",
            r"<a href='../huber/'>Huber</a> и <a href='../triplet/'>Triplet loss</a>: срезка $\max(0,\cdot)$ встречается и в функциях потерь.",
            r"<a href='../adam/'>Adam</a> и <a href='../sgd/'>SGD</a>: от выбора оптимизатора и шага зависит, сколько нейронов умрёт.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, r"1) $\operatorname{ReLU}(x)=\max(0,x)=\frac{x+|x|}2$ — вентиль: вход умножается на $\mathbb 1[x&gt;0]$. 2) Производная — ступенька 0/1, в нуле субдифференциал $[0;1]$, на практике 0; справа нет насыщения. 3) Сумма шарниров $v_k\operatorname{ReLU}(x-c_k)$ — любая ломаная; на плоскости сеть из ReLU — многогранник из линейных областей, глубина умножает их число. 4) softplus — гладкий ReLU, его производная — сигмоида. 5) Большой шаг обучения убивает нейроны навсегда. 6) Инициализация Хе $\operatorname{Var}w=2/n_\text{in}$ компенсирует то, что ReLU обнуляет половину сигнала."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q=r"Чему равно $\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)$?", options=[r"$|x|$", r"$x$", r"$0$", r"$2\operatorname{ReLU}(x)$"], answer=1,
                 explain=r"При $x&gt;0$ получаем $x-0=x$, при $x&lt;0$ — $0-(-x)=x$. А сумма $\operatorname{ReLU}(x)+\operatorname{ReLU}(-x)=|x|$."),
            dict(q=r"Что вернёт PyTorch как градиент ReLU в точке $x=0$?", options=[r"$1$", r"$0{,}5$", r"$0$", r"nan"], answer=2,
                 explain=r"Математически в нуле субдифференциал $[0;1]$; по соглашению PyTorch и TensorFlow берут 0."),
            dict(q=r"Сеть с одним скрытым слоем из 5 нейронов ReLU и одним входом $x$. Каким может быть её график?", options=[r"Любой гладкой кривой", r"Ломаной не более чем с 5 изломами", r"Только прямой", r"Ступенчатой функцией"], answer=1,
                 explain=r"Каждый нейрон — шарнир с одним изломом в $x=-b_k/w_k$, сумма шарниров — непрерывная ломаная не более чем с 5 изломами."),
            dict(q=r"Почему нейрон ReLU может «умереть» навсегда?", options=[r"Его вес становится бесконечным", r"Если вход отрицателен на всех примерах, градиенты по его весам и сдвигу равны нулю", r"Из-за переполнения экспоненты", r"Потому что производная ReLU не больше 0,25"], answer=1,
                 explain=r"Градиент по параметрам нейрона содержит множитель $\mathbb 1[w^\top x+b&gt;0]$. Если он равен нулю на всех данных, оптимизатор нейрон не сдвинет."),
            dict(q=r"Какую дисперсию весов предлагает инициализация Хе для слоя с $n_\text{in}$ входами?", options=[r"$1/n_\text{in}$", r"$2/n_\text{in}$", r"$2/(n_\text{in}+n_\text{out})$", r"$1$"], answer=1,
                 explain=r"ReLU обнуляет половину симметричного распределения: $\mathbb E[\operatorname{ReLU}(z)^2]=\tfrac12\operatorname{Var}z$. Чтобы средний квадрат не менялся от слоя к слою, нужно $\operatorname{Var}w=2/n_\text{in}$."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", r"Without a nonlinearity a neural network is useless: a composition of linear layers is again a linear function, however many layers you stack. We need a function that “breaks” linearity while being cheap to compute and gentle on the gradient. ReLU (rectified linear unit) does the minimum possible: it passes positive values unchanged and replaces negative ones with zero."),
        ("p", r"Where it appears:"),
        ("ul", [
            r"<b>convolutional networks</b> — AlexNet, VGG, ResNet: a ReLU after every convolution;",
            r"<b>fully connected networks and tabular models</b> — the default choice for hidden layers;",
            r"<b>the original Transformer</b> (2017) — the FFN block: $\max(0,\,xW_1+b_1)W_2+b_2$; modern LLMs moved to its smooth relatives <a href='../gelu/'>GELU</a> and <a href='../silu/'>SiLU</a>;",
            r"<b>mobile networks</b> — ReLU6 $=\min(\max(0,x),\,6)$ in MobileNet suits low-precision arithmetic;",
            r"<b>inside other formulas</b> — $\max(0,\cdot)$ is also the SVM hinge loss, the <a href='../triplet/'>triplet loss</a> and the positive part of a number $x^+$.",
        ]),
        ("callout", "key", "The essentials in a minute", r"$\operatorname{ReLU}(x)=\max(0,x)$: zero on the left, the line $y=x$ on the right. The derivative is a step: 0 for $x&lt;0$ and 1 for $x&gt;0$; at zero there is no derivative, and libraries take 0. On the right the gradient passes without attenuation — that is why deep ReLU networks train fast. The price is “dead” neurons whose input is always negative."),
    ]),
    dict(id="intuition", title="Intuition: a rectifier", blocks=[
        ("p", r"The name comes from electronics: a rectifier diode lets current flow one way and blocks it the other way. A ReLU neuron is a detector: while a feature is below the threshold it stays silent; once the threshold is crossed, it responds in proportion to how far."),
        ("p", r"Drag the point. To the right of zero the tangent coincides with the function itself (slope 1); to the left it lies on the axis (slope 0). At zero there is no single tangent: every line with a slope between 0 and 1 touches the graph from below — these are <b>supporting lines</b>."),
        ("viz", "relu-explorer", {"x": 1.5}, r"<b>Figure 1.</b> ReLU, the tangent and the derivative (below). At $x=1.5$: $\operatorname{ReLU}=1.5$, $\operatorname{ReLU}'=1$. Move the point to zero: the derivative is undefined, and the set of slopes of the supporting lines is the interval $[0,\,1]$ (the subdifferential); PyTorch and TensorFlow take 0 from it."),
        ("callout", "intuition", "What to notice", r"ReLU does not saturate on the right: at $x=100$ the derivative is the same 1 as at $x=0.1$. For the <a href='../sigmoid/'>sigmoid</a> and <a href='../tanh/'>tanh</a> the derivative is already below $0.01$ at $|x|=5$. On the left, however, ReLU is fully “saturated”: the derivative is exactly 0."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("p", r"It pays to recognise the same function in different forms — each one highlights its own property:"),
        ("eq", r"\operatorname{ReLU}(x)=\max(0,x)=\begin{cases}x, & x>0\\0, & x\le0\end{cases}=\frac{x+|x|}{2}=x\cdot\mathbb 1[x>0]"),
        ("symbols", [
            (r"\max(0,x)", r"a comparison with zero — one operation, no exponentials or divisions;"),
            (r"\frac{x+|x|}{2}", r"for $x&gt;0$ the terms are equal and give $x$; for $x&lt;0$ they cancel out;"),
            (r"x\cdot\mathbb 1[x>0]", r"a <b>gate</b>: the input is multiplied by 0 or 1 depending on its sign. For each example a ReLU network is a linear network with some neurons switched off."),
        ]),
        ("table", ["$x$", r"$\operatorname{ReLU}(x)$", r"$\operatorname{ReLU}'(x)$"], "TABLE", {"num": [0, 1, 2]}),
        ("h3", "Kinks make any broken line"),
        ("p", r"A neuron $v\cdot\operatorname{ReLU}(x-c)$ is a “hinge”: zero up to the point $c$, then a line with slope $v$. Adding hinges with different $c$ gives a broken line: at each point $c_k$ the slope changes by exactly $v_k$. For example, $\operatorname{ReLU}(x+1)-2\operatorname{ReLU}(x)+\operatorname{ReLU}(x-1)$ is a “hat” of height 1."),
        ("viz", "relu-hinges", {"v1": 1, "v2": -2, "v3": 1}, r"<b>Figure 2.</b> A sum of three hinges with kinks at $-1$, $0$, $1$. With weights $(1,\,-2,\,1)$ we get a hat: the slopes of the pieces are $0,\ 1,\ -1,\ 0$ and the height is $f(0)=1$. Below is the derivative: a step function that jumps by exactly $v_k$ at the point $c_k$."),
        ("p", r"This is the main secret of ReLU networks: any continuous piecewise linear function on the line with $m$ kinks is a linear function plus $m$ hinges, i.e. a network with one hidden layer of $m$ neurons (plus the linear part, which two neurons can also express: $x=\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)$). And broken lines approximate any continuous function on an interval as closely as we like."),
    ]),
    dict(id="properties", title="Properties", blocks=[
        ("ul", [
            r"<b>Range</b>: $[0,\,+\infty)$ — unbounded above, unlike the sigmoid and tanh.",
            r"<b>Piecewise linearity</b>: two linear pieces, one kink at zero.",
            r"<b>Continuity and the Lipschitz property</b> with constant 1: $|\operatorname{ReLU}(a)-\operatorname{ReLU}(b)|\le|a-b|$.",
            r"<b>Convexity</b>: the graph lies on or below every chord — the maximum of two linear functions is always convex.",
            r"<b>Positive homogeneity</b>: $\operatorname{ReLU}(\alpha x)=\alpha\operatorname{ReLU}(x)$ for $\alpha\ge0$. Scale can be moved between layers: multiplying a layer’s weights by $\alpha&gt;0$ and the next layer’s by $1/\alpha$ gives the same network.",
            r"<b>Idempotence</b>: $\operatorname{ReLU}(\operatorname{ReLU}(x))=\operatorname{ReLU}(x)$.",
            r"<b>Decomposing a number</b>: $x=\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)$ and $|x|=\operatorname{ReLU}(x)+\operatorname{ReLU}(-x)$.",
            r"<b>Sparsity</b>: if the neurons’ inputs are symmetric about zero, about half of the outputs are exact zeros.",
        ]),
        ("deep", "Proofs: convexity and homogeneity", [
            ("p", r"Convexity. For $t\in[0,1]$ and any $a,b$: $\max(0,\,ta+(1-t)b)\le\max\bigl(0,\,t\max(0,a)+(1-t)\max(0,b)\bigr)=t\max(0,a)+(1-t)\max(0,b)$, because $a\le\max(0,a)$, $b\le\max(0,b)$, and the right-hand side is non-negative."),
            ("p", r"Homogeneity. For $\alpha&gt;0$ the sign of $\alpha x$ equals the sign of $x$, so $\max(0,\alpha x)=\alpha\max(0,x)$; for $\alpha=0$ both sides are 0. For $\alpha&lt;0$ the equality fails: $\operatorname{ReLU}(-x)\ne-\operatorname{ReLU}(x)$ — the function is not odd."),
        ]),
    ]),
    dict(id="derivative", title="The derivative, the subgradient and smooth relatives", blocks=[
        ("eq", r"\operatorname{ReLU}'(x)=\begin{cases}1, & x>0\\0, & x<0\end{cases},\qquad \partial\operatorname{ReLU}(0)=[0,\,1]"),
        ("deep", "Why there is no derivative at zero", [
            ("p", r"The derivative is the limit of the difference quotient. To the right and to the left of zero it differs:"),
            ("eq", r"\lim_{h\to0^+}\frac{\operatorname{ReLU}(h)-0}{h}=\lim_{h\to0^+}\frac{h}{h}=1,\qquad \lim_{h\to0^-}\frac{\operatorname{ReLU}(h)-0}{h}=\lim_{h\to0^-}\frac{0}{h}=0"),
            ("p", r"The one-sided derivatives differ, so there is no ordinary derivative. Convex functions have a substitute — the <b>subgradient</b>: a number $g$ such that $f(y)\ge f(x)+g(y-x)$ for all $y$, i.e. the line with slope $g$ lies below the graph. At zero every $g\in[0,1]$ qualifies: this set is called the subdifferential $\partial\operatorname{ReLU}(0)$."),
        ]),
        ("p", r"Why this does not hurt training: for continuous data a neuron’s input is exactly zero with probability 0, and at the rare exact zeros any value in $[0,1]$ will do — convergence of subgradient methods allows it. By convention libraries take 0."),
        ("p", r"The second derivative is zero everywhere except at zero (in the sense of distributions, $\operatorname{ReLU}''=\delta(x)$). Hence inside each linear region a ReLU network is an affine function of its input, and its gradient with respect to the input is piecewise constant."),
        ("h3", "Softplus: a smoothed ReLU"),
        ("p", r"If the kink gets in the way (for example, when second-order optimization or a physical model needs a smooth function), it can be rounded off:"),
        ("eq", r"\operatorname{softplus}_\beta(x)=\frac1\beta\ln\bigl(1+e^{\beta x}\bigr),\qquad \operatorname{softplus}_\beta'(x)=\sigma(\beta x)"),
        ("p", r"The difference $\operatorname{softplus}_\beta(x)-\operatorname{ReLU}(x)=\frac1\beta\ln\bigl(1+e^{-\beta|x|}\bigr)$ is largest at zero, where it equals $\frac{\ln2}{\beta}$; as $\beta\to\infty$ softplus tends to ReLU, and its derivative, the <a href='../sigmoid/'>sigmoid</a>, tends to the step. At zero it always equals $\sigma(0)=0.5$ — the middle of the subdifferential $[0,1]$."),
        ("viz", "relu-smooth", {"beta": 1}, r"<b>Figure 3.</b> Top: ReLU and $\operatorname{softplus}_\beta$; bottom: their derivatives. At $\beta=1$ the largest gap is $\ln2\approx0.693$, at $\beta=4$ it is $0.173$, at $\beta=32$ — $0.022$. The derivative of softplus at zero is always $0.5$."),
    ]),
    dict(id="space", title="A ReLU network in space: linear regions", blocks=[
        ("p", r"A first-layer neuron with two inputs is off on one side of the line $w^\top x+b=0$ and linear on the other. Each such line is a fold line. $H$ neurons cut the plane into regions, and within each region the set of active neurons (the <b>activation pattern</b>) is constant, so the network is an ordinary affine function there. The output surface is a polyhedron glued together from flat facets."),
        ("viz", "relu-surface", {"arch": "n4", "seed": 3}, r"<b>Figure 4.</b> Left: the network output $f(x_1,x_2)=\sum_k v_k\operatorname{ReLU}(w_k^\top x+b_k)$ in 3D — flat facets and fold edges. Right: the view from above; colour is the index of the linear region, dashed lines are the neurons’ lines, thin lines are levels of $f$ (they bend at the boundaries). With 4 neurons the window shows 10 regions out of a possible 11 ($1+H+\tfrac{H(H-1)}{2}$); with 8 neurons, 25 out of 37. Two layers of 4 neurons already give 30 regions: the second layer’s boundaries bend at the first layer’s."),
        ("p", r"$H$ lines in general position divide the plane into at most $1+H+\binom H2$ parts — the number of regions of one layer grows polynomially. Depth works differently: each next layer “folds” the already cut space, and the number of regions can grow exponentially with the number of layers (Montúfar et al., 2014). This is one explanation of why deep networks are more expressive than wide ones with the same number of neurons."),
        ("callout", "note", "Universal approximation", r"A network with one hidden ReLU layer and enough neurons approximates any continuous function on a closed bounded set to any accuracy (Leshno et al., 1993: any continuous activation that is not a polynomial will do). For ReLU this is visible literally: broken lines are made of hinges, polyhedral surfaces of folds."),
    ]),
    dict(id="training", title="ReLU in training: the network draws a broken line", blocks=[
        ("p", r"Let us train one hidden layer $\hat y(x)=\sum_{k=1}^{H}v_k\operatorname{ReLU}(w_kx+b_k)+c$ on points of a sine wave. Each neuron is a hinge with its kink at $x=-b_k/w_k$; gradient descent moves the kinks to where the curve bends and tunes the slopes."),
        ("eq", r"\frac{\partial\hat y}{\partial b_k}=v_k\,\mathbb 1[w_kx+b_k>0],\qquad \frac{\partial\hat y}{\partial w_k}=v_k\,x\,\mathbb 1[w_kx+b_k>0]"),
        ("p", r"The gradient with respect to a neuron’s parameters comes only from the points where the neuron is on. If there are no such points at all, the neuron stops learning — that is what “dying” means."),
        ("viz", "relu-fit", {"h": 6}, r"<b>Figure 5.</b> 40 points of $y=\sin(1.6x)$ with noise ($\sigma=0.08$), full-batch gradients and <a href='../adam/'>Adam</a> with step $0.02$. Teal lines are the hinges, the dots at the bottom are their kinks, red dashes are dead neurons. With 6 neurons the MSE drops from $3.102$ to $0.267$ by step 100, $0.012$ by step 300 and $0.0090$ by step 1500; on the way one neuron dies. With 3 neurons the broken line is too coarse — $0.265$; with 12 the result is $0.0101$, but 4 of the 12 are already dead."),
        ("callout", "note", "What the figure shows", r"A ReLU network cannot draw anything smooth — only broken lines. The kinks gather where the sine bends most, and there are none on nearly straight stretches. Extra neurons do not necessarily help: some of them die or duplicate their neighbours."),
    ]),
    dict(id="dying", title="The dying ReLU", blocks=[
        ("p", r"A neuron is “dead” if $w^\top x+b\le0$ on all training examples. Then its output is always 0, the gradients with respect to $w$ and $b$ are always 0 (see the formula above), and no optimizer step will revive it: when training on the same data it stays switched off for good."),
        ("p", r"How it happens: one large gradient step sharply decreases the bias $b$ or turns $w$ so that the neuron’s hyperplane moves outside the cloud of data. The larger the learning rate, the more often this happens."),
        ("viz", "relu-dead", {"lr": 0.3}, r"<b>Figure 6.</b> A network of 64 ReLU neurons on 128 points $y=\sin(3x_1)+x_2$, $x\in[-1,1]^2$, mini-batches of 16, plain SGD, 600 steps, the same He initialization. Right: the neurons — blue ones are alive (brightness is the share of points where the neuron is on), red ones are dead. With $\eta=0.3$, $91\%$ of the neurons die within the first 5 steps and $97\%$ by the end; the MSE gets stuck at $0.137$. With $\eta=0.2$ a quarter is dead ($27\%$), MSE $0.004$; with $\eta=0.1$ and $0.03$ none die (MSE $0.005$ and $0.041$ — the small step is simply slower)."),
        ("p", r"How to treat it:"),
        ("ul", [
            r"<b>a moderate learning rate</b>, warm-up and gradient clipping;",
            r"<b>adaptive optimizers</b> (<a href='../adam/'>Adam</a>) and normalization (BatchNorm, LayerNorm): they keep the neurons’ inputs near zero;",
            r"<b>activations with a non-zero slope on the left</b> — <a href='../leaky-relu/'>Leaky ReLU</a>, PReLU, ELU, <a href='../gelu/'>GELU</a>, <a href='../silu/'>SiLU</a>: the gradient on the left is not zero, so the neuron can come back;",
            r"<b>careful initialization</b>: zero biases (sometimes slightly positive), He weights. Strongly negative biases kill neurons before training even starts.",
        ]),
    ]),
    dict(id="init", title="He initialization: where the 2 comes from", blocks=[
        ("p", r"Let $z=\sum_{j=1}^{n}w_jh_j$ with independent weights, $\mathbb Ew_j=0$, $\operatorname{Var}w_j=c/n$. Then $\operatorname{Var}z=c\cdot q$, where $q=\mathbb E[h^2]$ is the mean square of the inputs. If $z$ is symmetric about zero, ReLU zeroes out exactly half of its distribution, and"),
        ("eq", r"q_{l}=\mathbb E\bigl[\operatorname{ReLU}(z)^2\bigr]=\frac12\operatorname{Var}z=\frac c2\,q_{l-1}\qquad\Longrightarrow\qquad q_L=q_0\Bigl(\frac c2\Bigr)^{L}"),
        ("p", r"With $c=1$ (as for tanh) the signal halves at every layer; with $c=3$ it grows by half. Only $c=2$ preserves the scale: this is <b>He initialization</b> (He et al., 2015), $\operatorname{Var}w=2/n_\text{in}$. The backward pass behaves the same way, so the gradients neither vanish nor explode either."),
        ("viz", "relu-depth", {"c": 2}, r"<b>Figure 7.</b> The mean square of the activations $q_l$ at each of the 30 layers of a random network of width 100 (log scale); the orange dashed line is the theory $q_0(c/2)^l$. With $c=2$ the ratio $q_{30}/q_0=2.66$; with $c=1$ it is $2.47\cdot10^{-9}$ (theory $9.3\cdot10^{-10}$); with $c=3$, $5.1\cdot10^5$ (theory $1.9\cdot10^5$). The factor $\approx2.66$ is the same in all three cases: the weights are the same and ReLU is positively homogeneous, so $c$ merely multiplies the whole signal by $(c/2)^{L/2}$; the deviation from theory is a random finite-width fluctuation. $51\%$ of the last layer’s neurons are active."),
        ("callout", "history", "A bit of history", r"The rectifier idea is old: Fukushima used it as early as 1969. ReLU entered deep learning in 2010–2011 (Nair and Hinton; Glorot, Bordes and Bengio), and in AlexNet (2012) a ReLU network reached 25% training error on CIFAR-10 six times faster than one with tanh. In 2015 He et al. derived the $2/n$ initialization and trained networks of the ReLU family tens of layers deep."),
    ]),
    dict(id="code", title="In code", blocks=[
        ("p", r"ReLU never overflows and never loses precision: a comparison with zero is exact in any arithmetic. Attention belongs elsewhere: the convention at zero, dead neurons and initialization."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "The rule", r"ReLU plus He initialization (<code>kaiming_normal_</code> with <code>nonlinearity='relu'</code>), zero biases and a reasonable learning rate. Check from time to time the share of neurons that never fired on a batch: if it grows, lower the learning rate or switch to Leaky ReLU / GELU."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            r"<b>ReLU at the output of a regression whose target can be negative.</b> The network physically cannot output $y&lt;0$. A regression output needs a linear layer; ReLU at the output fits only quantities that are non-negative by nature (and even then softplus is better).",
            r"<b>Initialization meant for tanh.</b> With $\operatorname{Var}w=1/n$ the signal in a deep ReLU network decays as $2^{-L}$: after 30 layers by a factor of $2^{30}\approx10^9$ (Figure 7). Use He initialization.",
            r"<b>Too large a learning rate.</b> It kills neurons en masse, and they cannot be restored (Figure 6). The symptom: the loss is frozen and the share of zero activations is close to 100%.",
            r"<b>“The derivative of ReLU at zero is 1/2” or “it is undefined, so it is a bug”.</b> Mathematically, at zero there is the subdifferential $[0,1]$, and any value from it is admissible; libraries take 0. It does not affect training.",
            r"<b><code>inplace=True</code> where the input is needed later.</b> The operation overwrites its input; if that input is used in a residual connection or by another operation’s backward pass, PyTorch raises an error or the result is wrong.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            r"<a href='../leaky-relu/'>Leaky ReLU</a>: $\max(\alpha x,x)$ — a non-zero slope $\alpha$ on the left cures dying.",
            r"<a href='../gelu/'>GELU</a> and <a href='../silu/'>SiLU</a>: $x\Phi(x)$ and $x\sigma(x)$ — smooth “gates” instead of the hard $x\cdot\mathbb 1[x&gt;0]$; far from zero they behave like ReLU.",
            r"<a href='../sigmoid/'>Sigmoid</a>: the derivative of softplus is $\sigma(\beta x)$; ReLU displaced the sigmoid from hidden layers because of saturation.",
            r"<a href='../tanh/'>tanh</a>: saturates on both sides; tanh gets Xavier initialization, ReLU gets He.",
            r"<a href='../huber/'>Huber</a> and <a href='../triplet/'>Triplet loss</a>: the cut-off $\max(0,\cdot)$ appears in loss functions too.",
            r"<a href='../adam/'>Adam</a> and <a href='../sgd/'>SGD</a>: the optimizer and the learning rate decide how many neurons die.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, r"1) $\operatorname{ReLU}(x)=\max(0,x)=\frac{x+|x|}2$ is a gate: the input is multiplied by $\mathbb 1[x&gt;0]$. 2) The derivative is a 0/1 step; at zero the subdifferential is $[0,1]$, in practice 0; no saturation on the right. 3) A sum of hinges $v_k\operatorname{ReLU}(x-c_k)$ is any broken line; on the plane a ReLU network is a polyhedron of linear regions, and depth multiplies their number. 4) Softplus is a smooth ReLU whose derivative is the sigmoid. 5) A large learning rate kills neurons for good. 6) He initialization $\operatorname{Var}w=2/n_\text{in}$ compensates for ReLU zeroing half of the signal."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q=r"What is $\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)$?", options=[r"$|x|$", r"$x$", r"$0$", r"$2\operatorname{ReLU}(x)$"], answer=1,
                 explain=r"For $x&gt;0$ we get $x-0=x$; for $x&lt;0$, $0-(-x)=x$. The sum $\operatorname{ReLU}(x)+\operatorname{ReLU}(-x)$ equals $|x|$."),
            dict(q=r"What does PyTorch return as the gradient of ReLU at $x=0$?", options=[r"$1$", r"$0.5$", r"$0$", r"nan"], answer=2,
                 explain=r"Mathematically, at zero there is the subdifferential $[0,1]$; by convention PyTorch and TensorFlow take 0."),
            dict(q=r"A network with one hidden layer of 5 ReLU neurons and one input $x$. What can its graph be?", options=[r"Any smooth curve", r"A broken line with at most 5 kinks", r"Only a straight line", r"A step function"], answer=1,
                 explain=r"Each neuron is a hinge with one kink at $x=-b_k/w_k$; a sum of hinges is a continuous broken line with at most 5 kinks."),
            dict(q=r"Why can a ReLU neuron “die” for good?", options=[r"Its weight becomes infinite", r"If its input is negative on all examples, the gradients with respect to its weights and bias are zero", r"Because the exponential overflows", r"Because the derivative of ReLU is at most 0.25"], answer=1,
                 explain=r"The gradient with respect to the neuron’s parameters contains the factor $\mathbb 1[w^\top x+b&gt;0]$. If it is zero on all data, the optimizer will not move the neuron."),
            dict(q=r"What weight variance does He initialization suggest for a layer with $n_\text{in}$ inputs?", options=[r"$1/n_\text{in}$", r"$2/n_\text{in}$", r"$2/(n_\text{in}+n_\text{out})$", r"$1$"], answer=1,
                 explain=r"ReLU zeroes half of a symmetric distribution: $\mathbb E[\operatorname{ReLU}(z)^2]=\tfrac12\operatorname{Var}z$. To keep the mean square constant from layer to layer we need $\operatorname{Var}w=2/n_\text{in}$."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", r"Nochiziqliliksiz neyron tarmoq foydasiz: chiziqli qatlamlar kompozitsiyasi qancha qatlam qo‘yilmasin, yana chiziqli funksiya. Chiziqlilikni «sindiradigan», lekin arzon hisoblanadigan va gradiyentni bo‘g‘maydigan funksiya kerak. ReLU (rectified linear unit, «to‘g‘rilangan chiziqli funksiya») eng kam narsani qiladi: musbatni o‘zgarishsiz o‘tkazadi, manfiyni nol bilan almashtiradi."),
        ("p", r"U qayerda uchraydi:"),
        ("ul", [
            r"<b>o‘ramli tarmoqlar</b> — AlexNet, VGG, ResNet: har bir o‘ramdan keyin ReLU;",
            r"<b>to‘liq bog‘langan tarmoqlar va jadval modellari</b> — yashirin qatlamlar uchun standart tanlov;",
            r"<b>asl Transformer</b> (2017) — FFN bloki: $\max(0,\,xW_1+b_1)W_2+b_2$; zamonaviy LLM’lar uning silliq qarindoshlari <a href='../gelu/'>GELU</a> va <a href='../silu/'>SiLU</a> ga o‘tgan;",
            r"<b>mobil tarmoqlar</b> — MobileNet’dagi ReLU6 $=\min(\max(0,x),\,6)$ past razryadli hisoblashlar uchun qulay;",
            r"<b>boshqa formulalar ichida</b> — $\max(0,\cdot)$ bu SVM ning hinge yo‘qotishi ham, <a href='../triplet/'>triplet loss</a> ham, sonning musbat qismi $x^+$ ham.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", r"$\operatorname{ReLU}(x)=\max(0,x)$: chapda nol, o‘ngda $y=x$ to‘g‘ri chiziq. Hosila — zina: $x&lt;0$ da 0 va $x&gt;0$ da 1; nolda hosila yo‘q, kutubxonalar 0 oladi. O‘ngda gradiyent susaymasdan o‘tadi — shuning uchun ReLU li chuqur tarmoqlar tez o‘qitiladi. Buning bahosi — kirishi doim manfiy bo‘lgan «o‘lik» neyronlar."),
    ]),
    dict(id="intuition", title="Intuitsiya: to‘g‘rilagich", blocks=[
        ("p", r"Nom elektronikadan kelgan: to‘g‘rilagich diod tokni bir tomonga o‘tkazadi, ikkinchi tomonga o‘tkazmaydi. ReLU li neyron — datchik: belgi chegaradan past bo‘lsa, u jim; chegaradan o‘tishi bilan qanchalik kuchli o‘tganiga mutanosib javob beradi."),
        ("p", r"Nuqtani torting. Noldan o‘ngda urinma funksiyaning o‘zi bilan ustma-ust tushadi (qiyalik 1), chapda o‘qda yotadi (qiyalik 0). Nolda yagona urinma yo‘q: qiyaligi 0 dan 1 gacha bo‘lgan har qanday to‘g‘ri chiziq grafikka pastdan tegadi — bular <b>tayanch chiziqlar</b>."),
        ("viz", "relu-explorer", {"x": 1.5}, r"<b>Rasm 1.</b> ReLU, urinma va hosila (pastda). $x=1{,}5$ da: $\operatorname{ReLU}=1{,}5$, $\operatorname{ReLU}'=1$. Nuqtani nolga olib boring: hosila aniqlanmagan, tayanch chiziqlar qiyaliklari to‘plami — $[0;\,1]$ kesma (subdifferensial); PyTorch va TensorFlow undan 0 ni oladi."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", r"ReLU o‘ngda to‘yinmaydi: $x=100$ da hosila $x=0{,}1$ dagi kabi 1 ga teng. <a href='../sigmoid/'>Sigmoida</a> va <a href='../tanh/'>tanh</a> da $|x|=5$ da hosila allaqachon $0{,}01$ dan kichik. Buning o‘rniga chapda ReLU to‘liq «to‘yingan»: hosila aynan 0."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", r"Bir xil funksiyani turli yozuvlarda tanib olish foydali — har biri o‘z xossasini yoritadi:"),
        ("eq", r"\operatorname{ReLU}(x)=\max(0,x)=\begin{cases}x, & x>0\\0, & x\le0\end{cases}=\frac{x+|x|}{2}=x\cdot\mathbb 1[x>0]"),
        ("symbols", [
            (r"\max(0,x)", r"nol bilan taqqoslash — eksponenta va bo‘lishsiz bitta amal;"),
            (r"\frac{x+|x|}{2}", r"$x&gt;0$ da qo‘shiluvchilar teng va $x$ beradi, $x&lt;0$ da bir-birini yo‘qotadi;"),
            (r"x\cdot\mathbb 1[x>0]", r"<b>ventil</b>: kirish ishorasiga qarab 0 ga yoki 1 ga ko‘paytiriladi. Har bir misol uchun ReLU tarmog‘i — neyronlarning bir qismi o‘chirilgan chiziqli tarmoq."),
        ]),
        ("table", ["$x$", r"$\operatorname{ReLU}(x)$", r"$\operatorname{ReLU}'(x)$"], "TABLE", {"num": [0, 1, 2]}),
        ("h3", "Sinishlardan — istalgan siniq chiziq"),
        ("p", r"$v\cdot\operatorname{ReLU}(x-c)$ neyroni — «sharnir» (hinge): $c$ nuqtagacha nol, keyin qiyaligi $v$ bo‘lgan to‘g‘ri chiziq. Turli $c$ li sharnirlarni qo‘shib, siniq chiziq olamiz: har bir $c_k$ nuqtada qiyalik aynan $v_k$ ga o‘zgaradi. Masalan, $\operatorname{ReLU}(x+1)-2\operatorname{ReLU}(x)+\operatorname{ReLU}(x-1)$ — balandligi 1 bo‘lgan «qalpoqcha»."),
        ("viz", "relu-hinges", {"v1": 1, "v2": -2, "v3": 1}, r"<b>Rasm 2.</b> Sinishlari $-1$, $0$, $1$ da bo‘lgan uchta sharnir yig‘indisi. $(1;\,-2;\,1)$ vaznlarda qalpoqcha hosil bo‘ladi: bo‘laklar qiyaliklari $0,\ 1,\ -1,\ 0$, balandlik $f(0)=1$. Pastda — hosila: $c_k$ nuqtada aynan $v_k$ ga sakraydigan zinapoya funksiya."),
        ("p", r"ReLU tarmoqlarining asosiy siri shu: to‘g‘ri chiziqdagi $m$ ta sinishli istalgan uzluksiz bo‘lakli-chiziqli funksiya — chiziqli funksiya va $m$ ta sharnir, ya’ni $m$ neyronli bitta yashirin qatlamli tarmoq (chiziqli qismni ham ikki neyron bilan ifodalash mumkin: $x=\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)$). Siniq chiziqlar bilan esa kesmadagi istalgan uzluksiz funksiyani istalgancha aniq yaqinlashtirish mumkin."),
    ]),
    dict(id="properties", title="Xossalar", blocks=[
        ("ul", [
            r"<b>Qiymatlar sohasi</b> — $[0;\,+\infty)$: sigmoida va tanh dan farqli, yuqoridan chegaralanmagan.",
            r"<b>Bo‘lakli chiziqlilik</b>: ikki chiziqli bo‘lak, nolda bitta sinish.",
            r"<b>Uzluksizlik va 1 konstantali Lipshits sharti</b>: $|\operatorname{ReLU}(a)-\operatorname{ReLU}(b)|\le|a-b|$.",
            r"<b>Qavariqlik</b>: grafik istalgan vatardan yuqori emas — ikki chiziqli funksiyaning maksimumi doim qavariq.",
            r"<b>Musbat bir jinslilik</b>: $\alpha\ge0$ da $\operatorname{ReLU}(\alpha x)=\alpha\operatorname{ReLU}(x)$. Masshtabni qatlamlar orasida ko‘chirish mumkin: qatlam vaznlarini $\alpha&gt;0$ ga, keyingisinikini $1/\alpha$ ga ko‘paytirsak, o‘sha tarmoq hosil bo‘ladi.",
            r"<b>Idempotentlik</b>: $\operatorname{ReLU}(\operatorname{ReLU}(x))=\operatorname{ReLU}(x)$.",
            r"<b>Sonni yoyish</b>: $x=\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)$ va $|x|=\operatorname{ReLU}(x)+\operatorname{ReLU}(-x)$.",
            r"<b>Siyraklik</b> (sparsity): neyronlar kirishlari nolga nisbatan simmetrik bo‘lsa, chiqishlarning taxminan yarmi aynan nol.",
        ]),
        ("deep", "Isbotlar: qavariqlik va bir jinslilik", [
            ("p", r"Qavariqlik. $t\in[0;1]$ va istalgan $a,b$ uchun: $\max(0,\,ta+(1-t)b)\le\max\bigl(0,\,t\max(0,a)+(1-t)\max(0,b)\bigr)=t\max(0,a)+(1-t)\max(0,b)$, chunki $a\le\max(0,a)$, $b\le\max(0,b)$, o‘ng tomon esa manfiy emas."),
            ("p", r"Bir jinslilik. $\alpha&gt;0$ da $\alpha x$ ning ishorasi $x$ niki bilan bir xil, shuning uchun $\max(0,\alpha x)=\alpha\max(0,x)$; $\alpha=0$ da ikkala tomon 0 ga teng. $\alpha&lt;0$ da tenglik buziladi: $\operatorname{ReLU}(-x)\ne-\operatorname{ReLU}(x)$ — funksiya toq emas."),
        ]),
    ]),
    dict(id="derivative", title="Hosila, subgradiyent va silliq qarindoshlar", blocks=[
        ("eq", r"\operatorname{ReLU}'(x)=\begin{cases}1, & x>0\\0, & x<0\end{cases},\qquad \partial\operatorname{ReLU}(0)=[0,\,1]"),
        ("deep", "Nega nolda hosila yo‘q", [
            ("p", r"Hosila — ayirmalar nisbatining limiti. Noldan o‘ngda va chapda u turlicha:"),
            ("eq", r"\lim_{h\to0^+}\frac{\operatorname{ReLU}(h)-0}{h}=\lim_{h\to0^+}\frac{h}{h}=1,\qquad \lim_{h\to0^-}\frac{\operatorname{ReLU}(h)-0}{h}=\lim_{h\to0^-}\frac{0}{h}=0"),
            ("p", r"Bir tomonlama hosilalar mos kelmaydi, demak, oddiy hosila yo‘q. Qavariq funksiyalar uchun o‘rinbosar bor — <b>subgradiyent</b>: barcha $y$ da $f(y)\ge f(x)+g(y-x)$ bo‘ladigan $g$ soni, ya’ni qiyaligi $g$ bo‘lgan to‘g‘ri chiziq grafik ostida yotadi. Nolda barcha $g\in[0;1]$ shunday: bu to‘plam subdifferensial $\partial\operatorname{ReLU}(0)$ deb ataladi."),
        ]),
        ("p", r"Nega bu o‘qitishga xalaqit bermaydi: uzluksiz ma’lumotlarda neyron kirishi aynan nolga teng bo‘lish ehtimoli 0, kamdan-kam aniq nollarda esa $[0;1]$ dagi istalgan qiymat yaraydi — subgradiyent usullarining yaqinlashuvi bunga yo‘l qo‘yadi. Kutubxonalar kelishuv bo‘yicha 0 oladi."),
        ("p", r"Ikkinchi hosila noldan boshqa hamma joyda nolga teng (umumlashgan funksiyalar ma’nosida $\operatorname{ReLU}''=\delta(x)$). Shuning uchun har bir chiziqli soha ichida ReLU tarmog‘i kirishning affin funksiyasi, uning kirish bo‘yicha gradiyenti esa bo‘lakli-o‘zgarmas."),
        ("h3", "Softplus: silliqlangan ReLU"),
        ("p", r"Agar sinish xalaqit bersa (masalan, ikkinchi tartibli optimallashtirish yoki fizik model uchun silliq funksiya kerak bo‘lsa), uni yumaloqlash mumkin:"),
        ("eq", r"\operatorname{softplus}_\beta(x)=\frac1\beta\ln\bigl(1+e^{\beta x}\bigr),\qquad \operatorname{softplus}_\beta'(x)=\sigma(\beta x)"),
        ("p", r"$\operatorname{softplus}_\beta(x)-\operatorname{ReLU}(x)=\frac1\beta\ln\bigl(1+e^{-\beta|x|}\bigr)$ ayirma nolda eng katta va $\frac{\ln2}{\beta}$ ga teng; $\beta\to\infty$ da softplus ReLU ga, uning hosilasi — <a href='../sigmoid/'>sigmoida</a> esa zinaga intiladi. Nolda u doim $\sigma(0)=0{,}5$ ga teng — $[0;1]$ subdifferensialning o‘rtasi."),
        ("viz", "relu-smooth", {"beta": 1}, r"<b>Rasm 3.</b> Yuqorida ReLU va $\operatorname{softplus}_\beta$, pastda ularning hosilalari. $\beta=1$ da eng katta farq $\ln2\approx0{,}693$, $\beta=4$ da — $0{,}173$, $\beta=32$ da — $0{,}022$. Softplus ning noldagi hosilasi doim $0{,}5$."),
    ]),
    dict(id="space", title="Fazodagi ReLU tarmog‘i: chiziqli sohalar", blocks=[
        ("p", r"Ikki kirishli birinchi qatlam neyroni $w^\top x+b=0$ to‘g‘ri chiziqning bir tomonida o‘chiq, ikkinchi tomonida chiziqli. Har bir shunday to‘g‘ri chiziq — bukilish chizig‘i. $H$ ta neyron tekislikni sohalarga bo‘ladi va har bir sohada yoniq neyronlar to‘plami (<b>aktivatsiya patterni</b>) o‘zgarmas, demak, tarmoq u yerda oddiy affin funksiya. Chiqish sirti — yassi yoqlardan yopishtirilgan ko‘pyoq."),
        ("viz", "relu-surface", {"arch": "n4", "seed": 3}, r"<b>Rasm 4.</b> Chapda — 3D’da tarmoq chiqishi $f(x_1,x_2)=\sum_k v_k\operatorname{ReLU}(w_k^\top x+b_k)$: yassi yoqlar va bukilish qirralari. O‘ngda — yuqoridan ko‘rinish: rang — chiziqli soha raqami, punktir — neyronlar to‘g‘ri chiziqlari, ingichka chiziqlar — $f$ sathlari (ular chegaralarda sinadi). 4 neyronda oynada mumkin bo‘lgan 11 tadan ($1+H+\tfrac{H(H-1)}{2}$) 10 ta soha bor; 8 neyronda — 37 tadan 25 ta. Har biri 4 neyronli ikki qatlam allaqachon 30 ta soha beradi: ikkinchi qatlam chegaralari birinchisining chegaralarida egiladi."),
        ("p", r"Umumiy holatdagi $H$ ta to‘g‘ri chiziq tekislikni ko‘pi bilan $1+H+\binom H2$ qismga bo‘ladi — bitta qatlam sohalari soni polinomial o‘sadi. Chuqurlik boshqacha ishlaydi: har bir keyingi qatlam allaqachon kesilgan fazoni «buklaydi» va sohalar soni qatlamlar soni bilan eksponensial o‘sishi mumkin (Montufar va boshq., 2014). Bu nega chuqur tarmoqlar bir xil neyronlar sonida keng tarmoqlardan ifodaliroq ekanining tushuntirishlaridan biri."),
        ("callout", "note", "Universal approksimatsiya", r"Bitta yashirin ReLU qatlamli va yetarlicha neyronli tarmoq chegaralangan yopiq to‘plamdagi istalgan uzluksiz funksiyani istalgan aniqlikda yaqinlashtiradi (Leshno va boshq., 1993: ko‘phad bo‘lmagan istalgan uzluksiz aktivatsiya yaraydi). ReLU uchun bu tom ma’noda ko‘rinadi: siniq chiziqlar — sharnirlardan, ko‘pyoqli sirtlar — burmalardan."),
    ]),
    dict(id="training", title="O‘qitishda ReLU: tarmoq siniq chiziq chizadi", blocks=[
        ("p", r"Bitta yashirin qatlam $\hat y(x)=\sum_{k=1}^{H}v_k\operatorname{ReLU}(w_kx+b_k)+c$ ni sinusoida nuqtalarida o‘qitamiz. Har bir neyron — sinishi $x=-b_k/w_k$ da bo‘lgan sharnir; gradiyent tushish sinishlarni egri chiziq egiladigan joyga suradi va qiyaliklarni tanlaydi."),
        ("eq", r"\frac{\partial\hat y}{\partial b_k}=v_k\,\mathbb 1[w_kx+b_k>0],\qquad \frac{\partial\hat y}{\partial w_k}=v_k\,x\,\mathbb 1[w_kx+b_k>0]"),
        ("p", r"Neyron parametrlari bo‘yicha gradiyent faqat neyron yoniq bo‘lgan nuqtalardan keladi. Bunday nuqtalar umuman bo‘lmasa, neyron o‘rganishni to‘xtatadi — «o‘lish» shu."),
        ("viz", "relu-fit", {"h": 6}, r"<b>Rasm 5.</b> Shovqinli ($\sigma=0{,}08$) $y=\sin(1{,}6x)$ ning 40 nuqtasi, to‘liq gradiyent va $0{,}02$ qadamli <a href='../adam/'>Adam</a>. Firuza chiziqlar — sharnirlar, pastdagi nuqtalar — ularning sinishlari, qizil punktir — o‘lik neyronlar. 6 neyron bilan MSE 100-qadamga kelib $3{,}102$ dan $0{,}267$ gacha, 300-qadamga kelib $0{,}012$ gacha va 1500-qadamga kelib $0{,}0090$ gacha tushadi; yo‘lda bitta neyron o‘ladi. 3 neyron bilan siniq chiziq juda qo‘pol — $0{,}265$; 12 neyron bilan natija $0{,}0101$, lekin 12 tadan 4 tasi allaqachon o‘lik."),
        ("callout", "note", "Rasmda nima ko‘rinadi", r"ReLU tarmog‘i silliq narsani chiza olmaydi — faqat siniq chiziqlarni. Sinishlar sinusoida eng ko‘p egiladigan joyda to‘planadi, deyarli to‘g‘ri bo‘laklarda esa ular yo‘q. Ortiqcha neyronlar har doim ham yordam bermaydi: ularning bir qismi o‘ladi yoki qo‘shnilarini takrorlaydi."),
    ]),
    dict(id="dying", title="O‘layotgan ReLU", blocks=[
        ("p", r"Agar barcha o‘quv misollarida $w^\top x+b\le0$ bo‘lsa, neyron «o‘lik». U holda uning chiqishi doim 0, $w$ va $b$ bo‘yicha gradiyentlar doim 0 (yuqoridagi formulaga qarang) va optimizatorning hech bir qadami uni tiriltirmaydi: o‘sha ma’lumotlarda o‘qitishda u butunlay o‘chiq qoladi."),
        ("p", r"Bu qanday sodir bo‘ladi: gradiyent tushishning bitta katta qadami $b$ siljishni keskin kamaytiradi yoki $w$ ni shunday buradiki, neyron giperteksligi ma’lumotlar bulutidan tashqariga chiqib ketadi. O‘qitish qadami qancha katta bo‘lsa, bu shuncha tez-tez yuz beradi."),
        ("viz", "relu-dead", {"lr": 0.3}, r"<b>Rasm 6.</b> 128 ta $y=\sin(3x_1)+x_2$, $x\in[-1;1]^2$ nuqtadagi 64 ta ReLU neyronli tarmoq, 16 talik mini-batchlar, oddiy SGD, 600 qadam, bir xil He initsializatsiyasi. O‘ngda — neyronlar: ko‘klari tirik (yorqinlik — neyron yoniq bo‘lgan nuqtalar ulushi), qizillari o‘lik. $\eta=0{,}3$ da dastlabki 5 qadamdayoq neyronlarning $91\%$ i o‘ladi, oxiriga kelib — $97\%$, MSE $0{,}137$ da tiqilib qoladi. $\eta=0{,}2$ da chorak qismi ($27\%$) o‘lik, MSE $0{,}004$; $\eta=0{,}1$ va $0{,}03$ da o‘liklar yo‘q (MSE $0{,}005$ va $0{,}041$ — kichik qadam shunchaki sekinroq)."),
        ("p", r"Qanday davolash mumkin:"),
        ("ul", [
            r"<b>mo‘tadil o‘qitish qadami</b>, qizdirish (warm-up) va gradiyentni kesish;",
            r"<b>adaptiv optimizatorlar</b> (<a href='../adam/'>Adam</a>) va normallashtirish (BatchNorm, LayerNorm): ular neyronlar kirishlarini nol atrofida ushlab turadi;",
            r"<b>chapda qiyaligi noldan farqli aktivatsiyalar</b> — <a href='../leaky-relu/'>Leaky ReLU</a>, PReLU, ELU, <a href='../gelu/'>GELU</a>, <a href='../silu/'>SiLU</a>: chapda gradiyent nolga teng emas va neyron qaytishi mumkin;",
            r"<b>ehtiyotkor initsializatsiya</b>: siljishlar 0 (ba’zan kichik musbat), vaznlar He bo‘yicha. Kuchli manfiy siljishlar neyronlarni o‘qitishdan oldinoq o‘ldiradi.",
        ]),
    ]),
    dict(id="init", title="He initsializatsiyasi: ikki qayerdan keladi", blocks=[
        ("p", r"$z=\sum_{j=1}^{n}w_jh_j$ bo‘lsin, vaznlar mustaqil, $\mathbb Ew_j=0$, $\operatorname{Var}w_j=c/n$. U holda $\operatorname{Var}z=c\cdot q$, bu yerda $q=\mathbb E[h^2]$ — kirishlarning o‘rtacha kvadrati. Agar $z$ nolga nisbatan simmetrik bo‘lsa, ReLU uning taqsimotining aynan yarmini nolga aylantiradi va"),
        ("eq", r"q_{l}=\mathbb E\bigl[\operatorname{ReLU}(z)^2\bigr]=\frac12\operatorname{Var}z=\frac c2\,q_{l-1}\qquad\Longrightarrow\qquad q_L=q_0\Bigl(\frac c2\Bigr)^{L}"),
        ("p", r"$c=1$ da (tanh dagi kabi) signal har qatlamda ikki marta zaiflashadi, $c=3$ da — bir yarim marta o‘sadi. Masshtabni faqat $c=2$ saqlaydi: bu <b>He initsializatsiyasi</b> (He va boshq., 2015), $\operatorname{Var}w=2/n_\text{in}$. Teskari o‘tish ham xuddi shunday ishlaydi, shuning uchun gradiyentlar ham so‘nmaydi va portlamaydi."),
        ("viz", "relu-depth", {"c": 2}, r"<b>Rasm 7.</b> Kengligi 100 bo‘lgan tasodifiy tarmoqning 30 qatlamining har birida aktivatsiyalarning o‘rtacha kvadrati $q_l$ (logarifmik shkala), to‘q sariq punktir — nazariya $q_0(c/2)^l$. $c=2$ da $q_{30}/q_0=2{,}66$; $c=1$ da — $2{,}47\cdot10^{-9}$ (nazariya $9{,}3\cdot10^{-10}$); $c=3$ da — $5{,}1\cdot10^5$ (nazariya $1{,}9\cdot10^5$). $\approx2{,}66$ ko‘paytuvchi uchala holatda bir xil: vaznlar bir xil, ReLU esa musbat bir jinsli, shuning uchun $c$ butun signalni $(c/2)^{L/2}$ ga ko‘paytiradi xolos; nazariyadan og‘ish — chekli kenglikning tasodifiy tebranishi. Oxirgi qatlam neyronlarining $51\%$ i faol."),
        ("callout", "history", "Biroz tarix", r"To‘g‘rilagich g‘oyasi eski: uni Fukusima 1969 yildayoq ishlatgan. ReLU chuqur o‘qitishga 2010–2011 yillarda kirdi (Nair va Xinton; Gloro, Bord va Benjio), AlexNet’da (2012) esa ReLU li tarmoq CIFAR-10 o‘quv to‘plamida 25% xatoga tanh li tarmoqdan 6 marta tezroq yetdi. 2015 yilda He va hammualliflar $2/n$ initsializatsiyasini keltirib chiqardi va ReLU oilasidagi o‘nlab qatlamli tarmoqlarni o‘qitdi."),
    ]),
    dict(id="code", title="Kodda", blocks=[
        ("p", r"ReLU to‘lib ketmaydi va aniqlikni yo‘qotmaydi: nol bilan taqqoslash istalgan arifmetikada aniq. E’tiborni boshqa narsaga qaratish kerak: noldagi kelishuvga, o‘lik neyronlarga va initsializatsiyaga."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Qoida", r"ReLU va He initsializatsiyasi (<code>nonlinearity='relu'</code> bilan <code>kaiming_normal_</code>), siljishlar 0, oqilona o‘qitish qadami. Vaqti-vaqti bilan batchda bir marta ham yonmagan neyronlar ulushini tekshiring: agar u o‘sayotgan bo‘lsa, qadamni kamaytiring yoki Leaky ReLU / GELU ga o‘ting."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            r"<b>Maqsad manfiy bo‘lishi mumkin bo‘lgan regressiya chiqishida ReLU.</b> Tarmoq jismonan $y&lt;0$ chiqara olmaydi. Regressiya chiqishida — chiziqli qatlam; chiqishdagi ReLU faqat tabiatan manfiy bo‘lmagan kattaliklar uchun o‘rinli (va u holda ham softplus yaxshiroq).",
            r"<b>tanh dagi kabi initsializatsiya.</b> $\operatorname{Var}w=1/n$ da chuqur ReLU tarmog‘ida signal $2^{-L}$ kabi so‘nadi: 30 qatlamdan keyin $2^{30}\approx10^9$ marta (7-rasm). He initsializatsiyasini oling.",
            r"<b>Juda katta o‘qitish qadami.</b> Neyronlarni ommaviy o‘ldiradi va ularni tiklab bo‘lmaydi (6-rasm). Belgisi — yo‘qotish qotib qolgan, nol aktivatsiyalar ulushi esa 100% ga yaqin.",
            r"<b>«ReLU ning noldagi hosilasi 1/2 ga teng» yoki «aniqlanmagan — demak, xato».</b> Matematik jihatdan nolda $[0;1]$ subdifferensial bor, undagi istalgan qiymat joiz; kutubxonalar 0 oladi. Bu o‘qitishga ta’sir qilmaydi.",
            r"<b>Kirish keyin kerak bo‘ladigan joyda <code>inplace=True</code>.</b> Amal kirishni ustidan yozadi; agar u qoldiq bog‘lanishda yoki boshqa amalning teskari o‘tishida ishlatilsa, PyTorch xato beradi yoki natija noto‘g‘ri bo‘ladi.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘lanish", blocks=[
        ("ul", [
            r"<a href='../leaky-relu/'>Leaky ReLU</a>: $\max(\alpha x,x)$ — chapdagi noldan farqli $\alpha$ qiyalik o‘lishni davolaydi.",
            r"<a href='../gelu/'>GELU</a> va <a href='../silu/'>SiLU</a>: $x\Phi(x)$ va $x\sigma(x)$ — qattiq $x\cdot\mathbb 1[x&gt;0]$ o‘rniga silliq «ventillar»; noldan uzoqda ReLU kabi ishlaydi.",
            r"<a href='../sigmoid/'>Sigmoida</a>: softplus ning hosilasi — bu $\sigma(\beta x)$; ReLU to‘yinish tufayli sigmoidani yashirin qatlamlardan siqib chiqardi.",
            r"<a href='../tanh/'>tanh</a>: ikki tomondan to‘yinadi; tanh uchun — Ksavye initsializatsiyasi, ReLU uchun — He.",
            r"<a href='../huber/'>Huber</a> va <a href='../triplet/'>Triplet loss</a>: $\max(0,\cdot)$ kesish yo‘qotish funksiyalarida ham uchraydi.",
            r"<a href='../adam/'>Adam</a> va <a href='../sgd/'>SGD</a>: qancha neyron o‘lishi optimizator va qadam tanloviga bog‘liq.",
        ]),
    ]),
    dict(id="summary", title="Xulosalar", blocks=[
        ("callout", "key", None, r"1) $\operatorname{ReLU}(x)=\max(0,x)=\frac{x+|x|}2$ — ventil: kirish $\mathbb 1[x&gt;0]$ ga ko‘paytiriladi. 2) Hosila — 0/1 zina, nolda subdifferensial $[0;1]$, amalda 0; o‘ngda to‘yinish yo‘q. 3) $v_k\operatorname{ReLU}(x-c_k)$ sharnirlar yig‘indisi — istalgan siniq chiziq; tekislikda ReLU tarmog‘i chiziqli sohalardan iborat ko‘pyoq, chuqurlik ularning sonini ko‘paytiradi. 4) softplus — silliq ReLU, uning hosilasi — sigmoida. 5) Katta o‘qitish qadami neyronlarni butunlay o‘ldiradi. 6) He initsializatsiyasi $\operatorname{Var}w=2/n_\text{in}$ ReLU signalning yarmini nolga aylantirishini qoplaydi."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q=r"$\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)$ nimaga teng?", options=[r"$|x|$", r"$x$", r"$0$", r"$2\operatorname{ReLU}(x)$"], answer=1,
                 explain=r"$x&gt;0$ da $x-0=x$, $x&lt;0$ da $0-(-x)=x$ hosil bo‘ladi. $\operatorname{ReLU}(x)+\operatorname{ReLU}(-x)$ yig‘indi esa $|x|$ ga teng."),
            dict(q=r"PyTorch $x=0$ nuqtada ReLU gradiyenti sifatida nimani qaytaradi?", options=[r"$1$", r"$0{,}5$", r"$0$", r"nan"], answer=2,
                 explain=r"Matematik jihatdan nolda $[0;1]$ subdifferensial; kelishuv bo‘yicha PyTorch va TensorFlow 0 oladi."),
            dict(q=r"5 ta ReLU neyronli bitta yashirin qatlamli va bitta $x$ kirishli tarmoq. Uning grafigi qanday bo‘lishi mumkin?", options=[r"Istalgan silliq egri chiziq", r"Ko‘pi bilan 5 ta sinishli siniq chiziq", r"Faqat to‘g‘ri chiziq", r"Zinapoya funksiya"], answer=1,
                 explain=r"Har bir neyron — $x=-b_k/w_k$ da bitta sinishli sharnir, sharnirlar yig‘indisi — ko‘pi bilan 5 ta sinishli uzluksiz siniq chiziq."),
            dict(q=r"Nega ReLU neyroni butunlay «o‘lishi» mumkin?", options=[r"Uning vazni cheksiz bo‘lib qoladi", r"Agar uning kirishi barcha misollarda manfiy bo‘lsa, vaznlari va siljishi bo‘yicha gradiyentlar nolga teng", r"Eksponenta to‘lib ketgani uchun", r"ReLU hosilasi 0,25 dan oshmagani uchun"], answer=1,
                 explain=r"Neyron parametrlari bo‘yicha gradiyent $\mathbb 1[w^\top x+b&gt;0]$ ko‘paytuvchini o‘z ichiga oladi. U barcha ma’lumotlarda nol bo‘lsa, optimizator neyronni siljitmaydi."),
            dict(q=r"$n_\text{in}$ kirishli qatlam uchun He initsializatsiyasi vaznlarning qanday dispersiyasini taklif qiladi?", options=[r"$1/n_\text{in}$", r"$2/n_\text{in}$", r"$2/(n_\text{in}+n_\text{out})$", r"$1$"], answer=1,
                 explain=r"ReLU simmetrik taqsimotning yarmini nolga aylantiradi: $\mathbb E[\operatorname{ReLU}(z)^2]=\tfrac12\operatorname{Var}z$. O‘rtacha kvadrat qatlamdan qatlamga o‘zgarmasligi uchun $\operatorname{Var}w=2/n_\text{in}$ kerak."),
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
