"""Formula page: softmax. Format: see README.md; widgets in assets/js/formulas/softmax.js."""

META = dict(
    id="softmax",
    date="2026-10-28",
    minutes=35,
    hero=r"\operatorname{softmax}(z)_i=s_i=\frac{e^{z_i}}{\sum_{j=1}^{K}e^{z_j}}",
    title={"ru": "Softmax: от логитов к вероятностям", "en": "Softmax: from logits to probabilities", "uz": "Softmax: logitlardan ehtimolliklarga"},
    dek={
        "ru": "Функция, которая превращает сырые баллы нейросети в распределение вероятностей на K классах. Разбираем её по косточкам: зачем экспонента, почему важны только разности логитов, что делает температура, как устроена матрица Якоби diag(s) − ssᵀ, почему softmax — это градиент гладкого максимума и как не получить NaN в коде.",
        "en": "The function that turns a network’s raw scores into a probability distribution over K classes. We take it apart bone by bone: why the exponential, why only logit differences matter, what temperature does, how the Jacobian diag(s) − ssᵀ is built, why softmax is the gradient of a smooth maximum, and how to avoid NaN in code.",
        "uz": "Neyron tarmoqning xom ballarini K ta sinf bo‘yicha ehtimolliklar taqsimotiga aylantiradigan funksiya. Uni mayda detallarigacha tahlil qilamiz: eksponenta nima uchun kerak, nega faqat logitlar ayirmalari muhim, harorat nima qiladi, diag(s) − ssᵀ Yakobi matritsasi qanday tuzilgan, nega softmax silliq maksimumning gradiyenti va kodda NaN olmaslik uchun nima qilish kerak.",
    },
    description={
        "ru": "Softmax по косточкам: температура, сдвиг логитов, связь с сигмоидой, симплекс, матрица Якоби, log-sum-exp, внимание и устойчивый код без NaN.",
        "en": "Softmax in depth: temperature, shift invariance, the sigmoid link, the simplex, the Jacobian, log-sum-exp, attention and stable code without NaN.",
        "uz": "Softmax batafsil: harorat, siljishga invariantlik, sigmoida bilan bog‘liqlik, simpleks, Yakobi matritsasi, log-sum-exp, attention va barqaror kod.",
    },
)

# Running example z = (2, 1, 0) at three temperatures (checked with numpy).
TABLE = [("1", "2", "7.389", "0.665", "0.867", "0.506"), ("2", "1", "2.718", "0.245", "0.117", "0.307"),
         ("3", "0", "1.000", "0.090", "0.016", "0.186"), ("Σ", "", "11.107", "1", "1", "1")]


def _table(lang):
    dec = "." if lang == "en" else ","
    return [[c.replace(".", dec) for c in row] for row in TABLE]


def _heads(lang):
    h = "0.5" if lang == "en" else "0{,}5"
    return ["$i$", "$z_i$", "$e^{z_i}$", "$s_i,\\ T=1$", f"$s_i,\\ T={h}$", "$s_i,\\ T=2$"]


CODE_NUMPY = '''import numpy as np
np.set_printoptions(precision=3)

def softmax(z, axis=-1, T=1.0):
    """Устойчивый softmax: вычитаем максимум, результат не меняется."""
    z = np.asarray(z, dtype=float) / T
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)

def log_softmax(z, axis=-1):
    # log s_i = z_i − logsumexp(z): без log(0) даже для крошечных вероятностей
    z = np.asarray(z, dtype=float)
    m = z.max(axis=axis, keepdims=True)
    return z - m - np.log(np.exp(z - m).sum(axis=axis, keepdims=True))

def softmax_backward(s, g):
    # J^T g = s * (g − <g, s>): O(K) вместо матрицы K×K
    return s * (g - (g * s).sum(axis=-1, keepdims=True))

z = np.array([2.0, 1.0, 0.0])
print(softmax(z))            # [0.665 0.245 0.09 ]
print(softmax(z + 1000))     # [0.665 0.245 0.09 ] — сдвиг не важен
print(softmax(z, T=0.5))     # [0.867 0.117 0.016] — острее
print(log_softmax([0.0, -800.0]))  # [   0. -800.], а np.log(softmax(...)) даст -inf'''

CODE_TORCH = '''import torch
import torch.nn.functional as F

z = torch.tensor([2.0, 1.0, 0.0], requires_grad=True)
s = F.softmax(z, dim=-1)          # tensor([0.6652, 0.2447, 0.0900])
s[0].backward()                   # первая строка матрицы Якоби
print(z.grad)                     # tensor([ 0.2227, -0.1628, -0.0599])

# Для обучения softmax отдельно не нужен:
logits = torch.randn(4, 3)        # батч: 4 примера, 3 класса
target = torch.tensor([0, 2, 1, 0])
loss = F.cross_entropy(logits, target)   # внутри — log_softmax + NLL
log_p = F.log_softmax(logits, dim=-1)    # если нужны логарифмы вероятностей'''

_REPL = {
    "en": [("Устойчивый softmax: вычитаем максимум, результат не меняется.", "Stable softmax: subtract the maximum, the result does not change."),
           ("без log(0) даже для крошечных вероятностей", "no log(0) even for tiny probabilities"),
           ("O(K) вместо матрицы K×K", "O(K) instead of a K×K matrix"),
           ("— сдвиг не важен", "— the shift does not matter"), ("— острее", "— sharper"),
           ("а np.log(softmax(...)) даст -inf", "while np.log(softmax(...)) gives -inf"),
           ("первая строка матрицы Якоби", "the first row of the Jacobian"),
           ("Для обучения softmax отдельно не нужен:", "For training you do not need a separate softmax:"),
           ("батч: 4 примера, 3 класса", "a batch: 4 examples, 3 classes"),
           ("внутри — log_softmax + NLL", "log_softmax + NLL inside"),
           ("если нужны логарифмы вероятностей", "if you need log-probabilities")],
    "uz": [("Устойчивый softmax: вычитаем максимум, результат не меняется.", "Barqaror softmax: maksimumni ayiramiz, natija o‘zgarmaydi."),
           ("без log(0) даже для крошечных вероятностей", "juda kichik ehtimolliklarda ham log(0) siz"),
           ("O(K) вместо матрицы K×K", "K×K matritsa o‘rniga O(K)"),
           ("— сдвиг не важен", "— siljish muhim emas"), ("— острее", "— keskinroq"),
           ("а np.log(softmax(...)) даст -inf", "np.log(softmax(...)) esa -inf beradi"),
           ("первая строка матрицы Якоби", "Yakobi matritsasining birinchi satri"),
           ("Для обучения softmax отдельно не нужен:", "O‘qitishda alohida softmax kerak emas:"),
           ("батч: 4 примера, 3 класса", "batch: 4 ta misol, 3 ta sinf"),
           ("внутри — log_softmax + NLL", "ichida — log_softmax + NLL"),
           ("если нужны логарифмы вероятностей", "ehtimolliklar logarifmlari kerak bo‘lsa")],
}


def _code(src, lang):
    for a, b in _REPL.get(lang, []):
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем он нужен", blocks=[
        ("p", r"Классификатор на $K$ классов в конце выдаёт $K$ чисел — <b>логитов</b> (logits): например, $(2;\,1;\,0)$ для «кошка», «собака», «птица». Это просто баллы: они бывают отрицательными, не складываются в 1, и по ним не видно, насколько модель уверена. Softmax превращает такой вектор в распределение вероятностей: все числа положительны, в сумме дают 1, а порядок сохраняется — у кого балл больше, у того и вероятность больше."),
        ("p", "Где он встречается:"),
        ("ul", [
            r"<b>выход многоклассового классификатора</b> — от логистической регрессии до ResNet и ViT: $\hat y=\operatorname{softmax}(Wx+b)$;",
            r"<b>языковые модели</b> — на каждом шаге LLM выдаёт логиты для всех токенов словаря (десятки и сотни тысяч), softmax делает из них распределение следующего токена, а температура регулирует «смелость» генерации;",
            r"<b>механизм внимания (attention)</b> в трансформерах — веса $\operatorname{softmax}(QK^\top/\sqrt d)$ решают, на какие токены смотреть;",
            r"<b>смесь экспертов (MoE)</b> — маршрутизатор распределяет токен между экспертами через softmax;",
            r"<b>обучение с подкреплением</b> — больцмановская политика выбирает действие $a$ с вероятностью, пропорциональной $e^{Q(a)/T}$;",
            r"<b>статистическая физика</b> — это распределение Больцмана — Гиббса $p_i\propto e^{-E_i/(kT)}$; отсюда и слово «температура».",
        ]),
        ("callout", "key", "Главное за минуту", r"$s_i=e^{z_i}/\sum_j e^{z_j}$: экспонента делает все числа положительными и превращает разности в отношения, деление на сумму нормирует. Softmax не меняется, если прибавить одну константу ко всем логитам (поэтому в коде вычитают максимум), его производная — матрица $\operatorname{diag}(s)-ss^\top$, а для двух классов он совпадает с <a href='../sigmoid/'>сигмоидой</a> разности логитов."),
    ]),
    dict(id="intuition", title="Интуиция: голосование с усилением", blocks=[
        ("p", r"Представьте, что классы — кандидаты, а логиты — их баллы. Чтобы получить доли «голосов», баллы нужно сделать положительными и нормировать. Просто разделить на сумму нельзя: баллы бывают отрицательными, а сумма — нулевой. Экспонента решает обе проблемы: $e^{z}$ всегда положительна, а разница баллов превращается в <i>отношение</i>: каждая единица преимущества делает долю кандидата в $e\approx2{,}718$ раза больше доли соперника."),
        ("p", "Потяните верхушки столбиков-логитов слева и посмотрите, как меняются вероятности справа. Потом нажмите «+1 ко всем логитам»: столбики слева поднимутся, а справа ничего не изменится."),
        ("viz", "softmax-bars", {"z": [2, 1, 0], "T": 1}, r"<b>Рисунок 1.</b> Логиты и вероятности. Для логитов $(2;\,1;\,0)$ получаем $(0{,}665;\,0{,}245;\,0{,}090)$, сумма экспонент $11{,}11$. Кнопки ±1 сдвигают все логиты — вероятности стоят на месте. Ползунок температуры: при $T=0{,}1$ первому классу достаётся больше $0{,}9999$, при $T=10$ распределение почти равномерное, $(0{,}367;\,0{,}332;\,0{,}301)$. Пунктир — уровень $1/K$."),
        ("callout", "intuition", "Что заметить", r"Логиты $(2;\,1;\,0)$ отличаются на единицу, а вероятности — в $e$ раз: $0{,}665/0{,}245\approx0{,}245/0{,}090\approx2{,}718$. Softmax смотрит только на <i>разности</i> логитов. Температура $T$ делит логиты: при $T&lt;1$ разности растут и распределение заостряется, при $T&gt;1$ — сглаживается."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("eq", r"s_i=\operatorname{softmax}(z)_i=\frac{e^{z_i}}{\sum_{j=1}^{K}e^{z_j}},\qquad i=1,\dots,K"),
        ("symbols", [
            (r"z=(z_1,\dots,z_K)", "вектор логитов — сырые выходы последнего слоя, любые действительные числа;"),
            (r"e^{z_i}", "экспонента: делает число положительным и превращает разности логитов в отношения;"),
            (r"\sum_{j}e^{z_j}", "нормирующая сумма (в физике — статистическая сумма, partition function $Z$);"),
            (r"s_i", r"вероятность $i$-го класса: $s_i\in(0;\,1)$ и $\sum_i s_i=1$."),
        ]),
        ("p", r"Пройдём сквозной пример шпаргалки — логиты $z=(2;\,1;\,0)$:"),
        ("eq", r"\begin{gathered}e^{2}\approx7{,}389,\quad e^{1}\approx2{,}718,\quad e^{0}=1,\quad\textstyle\sum\approx11{,}107\\ \Longrightarrow\;s\approx\Bigl(\frac{7{,}389}{11{,}107};\,\frac{2{,}718}{11{,}107};\,\frac{1}{11{,}107}\Bigr)=(0{,}665;\,0{,}245;\,0{,}090)\end{gathered}"),
        ("h3", "Температура"),
        ("p", r"Часто логиты перед softmax делят на число $T&gt;0$ — <b>температуру</b>:"),
        ("eq", r"s_i(T)=\frac{e^{z_i/T}}{\sum_j e^{z_j/T}}"),
        ("p", r"Таблица показывает, что температура делает с тем же вектором $(2;\,1;\,0)$:"),
        ("table", "HEADS", "TABLE", {"num": [1, 2, 3, 4, 5]}),
        ("p", r"Два предела объясняют название. При $T\to0$ выигрывает только наибольший логит: softmax стремится к one-hot вектору $\operatorname{argmax}$ (если максимум единственный). При $T\to\infty$ разности исчезают, и распределение становится равномерным, $s_i\to1/K$. Softmax — «мягкий» (soft) argmax: промежуточное состояние между жёстким выбором и полным безразличием."),
        ("callout", "note", "О названии", r"Строго говоря, softmax гладко приближает не функцию max, а one-hot вектор argmax. Гладкий максимум — это log-sum-exp, и softmax — его градиент (см. раздел <a href='#lse'>о LSE</a>)."),
    ]),
    dict(id="properties", title="Свойства", blocks=[
        ("ul", [
            r"<b>Распределение</b>: $s_i&gt;0$ и $\sum_i s_i=1$ при любых логитах. Ровно 0 или 1 не получается никогда — только в пределе (а на компьютере — из-за округления).",
            r"<b>Сохраняет порядок</b>: $z_i&gt;z_j\iff s_i&gt;s_j$, поэтому $\operatorname{argmax}s=\operatorname{argmax}z$. Чтобы просто предсказать класс, softmax можно не считать.",
            r"<b>Отношения</b>: $s_i/s_j=e^{z_i-z_j}$ — разность логитов равна логарифму отношения вероятностей. Обратно, $z_i=\ln s_i+C$: логиты восстанавливаются по вероятностям с точностью до общей константы.",
            r"<b>Инвариантность к сдвигу</b>: $\operatorname{softmax}(z+c\mathbf 1)=\operatorname{softmax}(z)$ для любого числа $c$. Из $K$ логитов значимы только $K-1$ разностей.",
            r"<b>Нет инвариантности к масштабу</b>: $\operatorname{softmax}(az)$ при $a&gt;1$ острее, при $0&lt;a&lt;1$ — площе. Это та же температура, $a=1/T$.",
            r"<b>Конкуренция</b>: рост одного логита увеличивает его вероятность и уменьшает все остальные — масса перераспределяется, а не создаётся.",
        ]),
        ("deep", "Почему сдвиг ничего не меняет", [
            ("eq", r"\frac{e^{z_i+c}}{\sum_j e^{z_j+c}}=\frac{e^{c}\,e^{z_i}}{e^{c}\sum_j e^{z_j}}=\frac{e^{z_i}}{\sum_j e^{z_j}}"),
            ("p", r"Множитель $e^c$ сокращается. Именно это позволяет в коде вычесть $\max_j z_j$ из всех логитов: результат тот же, а экспонента больше не переполняется."),
        ]),
        ("h3", "Два класса — это сигмоида"),
        ("eq", r"\operatorname{softmax}(z_1,z_2)_1=\frac{e^{z_1}}{e^{z_1}+e^{z_2}}=\frac{1}{1+e^{-(z_1-z_2)}}=\sigma(z_1-z_2)"),
        ("p", r"Для двух классов softmax — это <a href='../sigmoid/'>сигмоида</a> разности логитов, поэтому бинарному классификатору хватает одного выхода. Похожая формула верна и для $K$ классов, если смотреть на один класс против всех остальных:"),
        ("eq", r"s_i=\sigma\Bigl(z_i-\ln\sum_{j\ne i}e^{z_j}\Bigr)"),
        ("p", r"Каждая вероятность — сигмоида от отрыва своего логита от «гладкого максимума» остальных. Чтобы проверить, разделите числитель и знаменатель $s_i$ на $e^{z_i}$."),
        ("viz", "softmax-sigmoid", {"z1": 2, "z2": 1, "z3": 0}, r"<b>Рисунок 2.</b> $s_1$ как функция $z_1$ при фиксированных $z_2=1$, $z_3=0$. Синяя кривая — сигмоида, сдвинутая в точку $m=\ln(e^{1}+e^{0})\approx1{,}313$: при $z_1=2$ получаем $\sigma(0{,}687)\approx0{,}665$. Оранжевая и бирюзовая кривые — $s_2$ и $s_3$: они убывают, отдавая массу первому классу. Снимите галочку «Есть третий класс» — останется обычная сигмоида $\sigma(z_1-z_2)$."),
    ]),
    dict(id="geometry", title="Геометрия: симплекс вероятностей", blocks=[
        ("p", r"Все распределения на $K$ классах образуют <b>вероятностный симплекс</b>:"),
        ("eq", r"\Delta^{K-1}=\Bigl\{s\in\mathbb R^{K}:\ s_i\ge0,\ \textstyle\sum_i s_i=1\Bigr\}"),
        ("p", r"Для $K=3$ это равносторонний треугольник. Вершины — уверенные ответы $(1;\,0;\,0)$, $(0;\,1;\,0)$, $(0;\,0;\,1)$, центр — равномерное распределение $(\tfrac13;\,\tfrac13;\,\tfrac13)$, а точка внутри — «смесь» вершин с весами $s_i$ (барицентрические координаты)."),
        ("p", r"Softmax отображает всё пространство логитов $\mathbb R^K$ на <i>внутренность</i> симплекса: границы и вершины недостижимы. Все точки прямой $z+c\mathbf 1$ переходят в одну точку, поэтому по сути softmax — взаимно однозначное соответствие между $(K-1)$-мерным пространством разностей логитов и внутренностью симплекса. Обратное отображение — логарифм: $z=\ln s$ с точностью до сдвига."),
        ("viz", "softmax-simplex", {"z": [2, 1, 0]}, r"<b>Рисунок 3.</b> Распределение на трёх классах — точка треугольника; заливка показывает, какой класс побеждает и насколько уверенно. Перетащите чёрную точку: справа те же вероятности столбиками, под рисунком — логиты, которые дают эту точку. Чёрный пунктир — путь при изменении температуры: от вершины-победителя ($T\to0$) к центру ($T\to\infty$). Синяя линия — путь, если менять только $z_1$: от противоположной стороны к вершине 1. При $z=(2;\,1;\,0)$ центрированные логиты равны $(1;\,0;\,-1)$, энтропия $0{,}832$."),
        ("callout", "intuition", "Энтропия — удалённость от вершин", r"Энтропия $H(s)=-\sum_i s_i\ln s_i$ измеряет неуверенность: она стремится к 0 у вершин и максимальна в центре, где равна $\ln K$. Для $(0{,}665;\,0{,}245;\,0{,}090)$ получаем $0{,}832$ при максимуме $\ln3\approx1{,}099$."),
    ]),
    dict(id="derivative", title="Производная: матрица Якоби", blocks=[
        ("p", r"У softmax $K$ входов и $K$ выходов, поэтому его производная — не число, а матрица $K\times K$: элемент $J_{ij}=\partial s_i/\partial z_j$ показывает, как $i$-я вероятность откликается на $j$-й логит."),
        ("deep", "Вывод по правилу частного", [
            ("p", r"Обозначим $S=\sum_k e^{z_k}$; тогда $\partial S/\partial z_j=e^{z_j}$. Для $i=j$:"),
            ("eq", r"\frac{\partial s_i}{\partial z_i}=\frac{e^{z_i}S-e^{z_i}e^{z_i}}{S^{2}}=s_i-s_i^{2}=s_i(1-s_i)"),
            ("p", r"Для $i\ne j$ числитель $e^{z_i}$ от $z_j$ не зависит:"),
            ("eq", r"\frac{\partial s_i}{\partial z_j}=\frac{0\cdot S-e^{z_i}e^{z_j}}{S^{2}}=-s_is_j"),
        ]),
        ("deep", "Вывод через логарифм (короче)", [
            ("p", r"$\ln s_i=z_i-\ln S$. Производная логарифма суммы экспонент — снова softmax: $\partial\ln S/\partial z_j=e^{z_j}/S=s_j$. Значит,"),
            ("eq", r"\frac{\partial\ln s_i}{\partial z_j}=\delta_{ij}-s_j\quad\Longrightarrow\quad\frac{\partial s_i}{\partial z_j}=s_i(\delta_{ij}-s_j)"),
            ("p", r"Здесь $\delta_{ij}$ — символ Кронекера: 1 при $i=j$ и 0 иначе."),
        ]),
        ("eq", r"J=\frac{\partial s}{\partial z}=\operatorname{diag}(s)-s\,s^{\top},\qquad J_{ij}=\begin{cases}s_i(1-s_i),&i=j\\-s_is_j,&i\ne j\end{cases}"),
        ("p", "Свойства этой матрицы:"),
        ("ul", [
            r"<b>диагональ</b> $s_i(1-s_i)$ — ровно производная сигмоиды: не больше $\tfrac14$, максимум при $s_i=\tfrac12$;",
            r"<b>вне диагонали</b> все элементы отрицательны: подняв один логит, мы отнимаем вероятность у остальных;",
            r"<b>симметрична</b>, и каждая строка (и столбец) в сумме даёт 0: $J\mathbf 1=s-s\,(s^\top\mathbf 1)=0$. Это производная равенства $\sum_i s_i=1$, а вектор $\mathbf 1$ — направление сдвига, который ничего не меняет. Поэтому $J$ вырождена;",
            r"<b>неотрицательно определена</b>: $v^\top Jv=\sum_i s_iv_i^2-\bigl(\sum_i s_iv_i\bigr)^2$ — дисперсия величины $v$ при распределении $s$, а дисперсия не бывает отрицательной;",
            r"<b>затухает при уверенности</b>: когда $s$ близок к вершине симплекса, все элементы $J$ близки к нулю — насыщение, как у сигмоиды.",
        ]),
        ("viz", "softmax-jacobian", {"z": [2, 1, 0], "j": 0}, r"<b>Рисунок 4.</b> Слева — матрица Якоби при $z=(2;\,1;\,0)$: диагональ $(0{,}223;\,0{,}185;\,0{,}082)$ положительна (красный), вне диагонали — отрицательные $-0{,}163$, $-0{,}060$, $-0{,}022$ (синий); каждый столбец в сумме даёт 0, след $1-\sum s_i^2\approx0{,}4895$. Справа — элементы выбранного столбца как функции $z_j$: диагональный — колокол $s_j(1-s_j)$ с вершиной $0{,}25$ там, где $s_j=0{,}5$; остальные — отрицательные «ямы»."),
        ("h3", "Обратный проход без матрицы"),
        ("p", r"В backprop нужна не сама $J$, а произведение $J^\top g$, где $g=\partial L/\partial s$ пришёл сверху. Благодаря структуре $\operatorname{diag}(s)-ss^\top$ это стоит $O(K)$ операций вместо $O(K^2)$:"),
        ("eq", r"\frac{\partial L}{\partial z}=J^{\top}g=s\odot\bigl(g-\langle g,s\rangle\,\mathbf 1\bigr)"),
        ("p", r"Для словаря LLM с $K\approx10^5$ токенов это разница между $10^5$ и $10^{10}$ чисел на каждую позицию. А в паре с кросс-энтропией всё ещё проще: $\partial L/\partial z=s-y$ (вывод — на странице <a href='../cross-entropy/'>кросс-энтропии</a>)."),
    ]),
    dict(id="surface", title="3D-картина: softmax над плоскостью логитов", blocks=[
        ("p", r"Зафиксируем $z_3=0$ — это не теряет общности, ведь сдвигом любой логит можно сделать нулём, — и нарисуем $s_1$ как функцию двух переменных $z_1$ и $z_2$. Получается «рампа»: поверхность близка к 1 там, где $z_1$ больше и $z_2$, и нуля, и близка к 0 там, где первый класс проигрывает. Поперёк границы она поднимается по сигмоиде — это формула «один против всех» в действии."),
        ("viz", "softmax-surface", {"z": [2, 1]}, r"<b>Рисунок 5.</b> Слева — $s_k(z_1,z_2,0)$ в 3D (поверхность можно вращать), чёрная точка — $z=(2;\,1;\,0)$ с $s_1\approx0{,}665$. Справа — плоскость логитов: заливка показывает класс-победитель и уверенность, линии — уровни $0{,}1$, $0{,}5$, $0{,}9$ выбранной функции (для производной — $0{,}05$, $0{,}15$, $0{,}24$). Точку можно перетаскивать. Переключитесь на $\partial s_1/\partial z_1$: это гребень высотой $0{,}25$ вдоль линии $s_1=0{,}5$."),
        ("p", r"Вид сверху делит плоскость логитов на три области. Границы — множества равных логитов: луч $z_1=z_2\ge0$ разделяет классы 1 и 2, луч $z_1=0$, $z_2\le0$ — классы 1 и 3, луч $z_2=0$, $z_1\le0$ — классы 2 и 3. Все три луча выходят из начала координат, где $s=(\tfrac13;\,\tfrac13;\,\tfrac13)$."),
        ("callout", "note", "Где течёт градиент", r"Поверхность $\partial s_1/\partial z_1=s_1(1-s_1)$ почти плоская и почти нулевая в глубине «своей» и «чужой» областей. Градиент через softmax течёт только там, где модель сомневается, — вблизи границ."),
    ]),
    dict(id="lse", title="Log-sum-exp: гладкий максимум", blocks=[
        ("p", r"У softmax есть «первообразная» — функция log-sum-exp:"),
        ("eq", r"\operatorname{LSE}(z)=\ln\sum_{j=1}^{K}e^{z_j},\qquad\frac{\partial\operatorname{LSE}}{\partial z_i}=\frac{e^{z_i}}{\sum_j e^{z_j}}=s_i,\qquad\nabla\operatorname{LSE}(z)=\operatorname{softmax}(z)"),
        ("p", r"LSE — гладкий максимум: наибольшая экспонента доминирует в сумме, и логарифм возвращает почти её показатель. Точнее,"),
        ("eq", r"\max_j z_j\;\le\;\operatorname{LSE}(z)\;\le\;\max_j z_j+\ln K"),
        ("p", r"Левое неравенство верно, потому что сумма не меньше своего наибольшего слагаемого, правое — потому что каждое из $K$ слагаемых не больше наибольшего. Для $(2;\,1;\,0)$: $\operatorname{LSE}=\ln11{,}107\approx2{,}408$ — между $2$ и $2+\ln3\approx3{,}099$. С температурой $\operatorname{LSE}_T(z)=T\ln\sum_j e^{z_j/T}$ зазор сжимается до $T\ln K$: при $T\to0$ LSE становится обычным максимумом, а его градиент $\operatorname{softmax}(z/T)$ — one-hot вектором argmax."),
        ("viz", "softmax-lse", {"T": 1, "x": 1}, r"<b>Рисунок 6.</b> Сверху — $\operatorname{LSE}_T(x,0)=T\ln(e^{x/T}+1)$ и $\max(x,0)$; зазор не больше $T\ln2$ и максимален при $x=0$. При $T=1$, $x=1$: $\operatorname{LSE}\approx1{,}3133$, зазор $0{,}3133$. Снизу — производная по $x$: это $\sigma(x/T)$, первая компонента $\operatorname{softmax}(x/T,\,0)$, гладкая ступенька. Уменьшайте $T$ — LSE прижимается к ломаной, а softmax — к ступеньке."),
        ("deep", "Выпуклость LSE и кросс-энтропии", [
            ("p", r"Гессиан LSE — это производная softmax, то есть та же матрица Якоби: $\nabla^2\operatorname{LSE}=\operatorname{diag}(s)-ss^\top$. Она неотрицательно определена, значит LSE — выпуклая функция. Отсюда выпуклость кросс-энтропии по логитам: $-\ln s_y=\operatorname{LSE}(z)-z_y$ — выпуклая функция минус линейная."),
        ]),
        ("callout", "key", "Три формулы, которые стоит связать", r"$\operatorname{softmax}=\nabla\operatorname{LSE}$; $\ln s_i=z_i-\operatorname{LSE}(z)$ (log-softmax); $\mathrm{CE}=\operatorname{LSE}(z)-z_y$. Для примера шпаргалки: $2{,}408-2=0{,}408$. А при $K=2$ и $z=(x;\,0)$ LSE превращается в softplus $\ln(1+e^{x})$ — гладкую версию <a href='../relu/'>ReLU</a>."),
    ]),
    dict(id="training", title="Softmax в обучении", blocks=[
        ("p", r"Простейшая модель с softmax — многоклассовая логистическая (softmax-) регрессия: $K$ линейных функций дают логиты, softmax — вероятности, потеря — <a href='../cross-entropy/'>кросс-энтропия</a>:"),
        ("eq", r"s=\operatorname{softmax}(Wx+b),\qquad L=-\ln s_y,\qquad\frac{\partial L}{\partial W}=(s-y)\,x^{\top},\qquad\frac{\partial L}{\partial b}=s-y"),
        ("p", r"Здесь $y$ — one-hot вектор правильного класса. Вся матрица Якоби в паре с логарифмом сократилась до разности «предсказание − правда»."),
        ("viz", "softmax-regression", {}, r"<b>Рисунок 7.</b> Три класса по 30 точек. Модель начинает с $W=0$, $b=0$: все вероятности равны $\tfrac13$, $\mathrm{CE}=\ln3\approx1{,}099$, точность $33{,}3\%$. Нажмите «Пуск»: градиентный спуск с шагом $0{,}15$ по всей выборке. Уже после первого шага точность $94{,}4\%$, после 200 шагов $\mathrm{CE}\approx0{,}181$ и точность $95{,}6\%$. Яркость заливки — уверенность модели; наведите курсор, чтобы увидеть вероятности в любой точке."),
        ("callout", "note", "Границы — прямые", r"Граница между классами $i$ и $j$ — множество, где $z_i=z_j$, то есть $(w_i-w_j)^\top x+b_i-b_j=0$: прямая (в общем случае гиперплоскость). Softmax не делает модель нелинейной — он только переводит баллы в вероятности. Кривые границы появляются, когда логиты считает нейросеть."),
        ("h3", "Softmax внутри трансформера: внимание"),
        ("eq", r"\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\Bigl(\frac{QK^{\top}}{\sqrt{d}}\Bigr)V"),
        ("p", r"Каждая строка $\operatorname{softmax}(\cdot)$ — распределение внимания одного токена по токенам последовательности (включая его самого), сумма весов 1. Деление на $\sqrt d$ — это температура: скалярное произведение $d$-мерных векторов с независимыми компонентами нулевого среднего и единичной дисперсии имеет дисперсию $d$. Без масштабирования логиты внимания велики, softmax насыщается до почти one-hot, а матрица Якоби — и с ней градиенты — почти обнуляется."),
        ("h3", "Температура при генерации текста"),
        ("p", r"Языковая модель выбирает следующий токен из $\operatorname{softmax}(z/T)$. При $T\to0$ (жадный выбор) берётся самый вероятный токен, при $T&lt;1$ текст предсказуемее, при $T&gt;1$ — разнообразнее и рискованнее. Температура $T&gt;1$ работает и при дистилляции знаний (Хинтон и др., 2015): «мягкие» вероятности учителя несут больше информации, чем one-hot метки."),
        ("callout", "history", "Откуда название", r"Формула пришла из статистической физики: распределение Больцмана — Гиббса $p_i\propto e^{-E_i/(kT)}$ задаёт вероятность состояния с энергией $E_i$ при температуре $T$; логит играет роль энергии со знаком минус. Слово «softmax» предложил Джон Брайдл в 1990 году, описывая вероятностную интерпретацию выходов сети. В эконометрике та же модель называется мультиномиальным логитом."),
    ]),
    dict(id="code", title="В коде: устойчивость, log-softmax и PyTorch", blocks=[
        ("p", r"Наивная формула ломается на больших логитах: $e^{1000}\approx2\cdot10^{434}$ не помещается ни во float32, ни во float64 и превращается в бесконечность, а дальше получается $\infty/\infty=\text{NaN}$. Во float32 (и в bfloat16 с тем же диапазоном порядков) предел ближе: $e^{x}$ переполняется уже при $x&gt;88{,}72$ (наибольшее число float32 $\approx3{,}4\cdot10^{38}$). На очень отрицательных логитах беда обратная: экспоненты обнуляются, и выходит $0/0$."),
        ("viz", "softmax-overflow", {"c": 0}, r"<b>Рисунок 8.</b> Логиты $(2+c;\,1+c;\,c)$ при $c$ от $-800$ до $800$; правильный ответ всегда $(0{,}665;\,0{,}245;\,0{,}090)$. Наивная формула во float32 верна только при $-99\le c\le86$: при $c=87$ число $e^{89}$ не помещается во float32 и получается NaN; при $c\le-106$ все экспоненты равны нулю, $0/0$; а между ними денормализованные числа теряют точность — при $c=-105$ выходит уверенный, но ложный ответ $(1;\,0;\,0)$. Во float64 запас больше ($-741\le c\le707$), но предел тоже есть. С вычитанием максимума ответ верен везде."),
        ("p", r"Лекарство — инвариантность к сдвигу: вычтем $m=\max_j z_j$. Наибольший показатель станет равен 0, $e^0=1$, знаменатель окажется между 1 и $K$ — ни переполнения, ни деления на ноль:"),
        ("eq", r"s_i=\frac{e^{z_i-m}}{\sum_j e^{z_j-m}},\qquad\ln s_i=(z_i-m)-\ln\sum_j e^{z_j-m}"),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Правило", r"Если дальше идёт логарифм, не считайте $\ln(\operatorname{softmax}(z))$ в два шага: маленькая вероятность округлится до 0, и получится $-\infty$. Используйте <code>log_softmax</code> или сразу потерю на логитах: <code>F.cross_entropy</code> / <code>nn.CrossEntropyLoss</code> в PyTorch, <code>from_logits=True</code> в Keras."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            r"<b>Softmax перед <code>nn.CrossEntropyLoss</code></b>. Эта потеря ждёт логиты и сама применяет log-softmax. Двойной softmax зажимает вероятности: для трёх классов второй softmax не даёт больше $e/(e+2)\approx0{,}576$, потеря не опускается ниже $0{,}551$, градиенты искажены.",
            r"<b>Не та ось</b>. Для батча формы $(N,K)$ нормировать нужно по классам (<code>dim=-1</code>), а не по примерам (<code>dim=0</code>). Исключения не будет — модель просто учит бессмыслицу.",
            r"<b>Наивная экспонента</b> без вычитания максимума — NaN на больших логитах, особенно в смешанной точности: во float16 $e^{x}$ переполняется уже при $x&gt;11{,}09$.",
            r"<b>Softmax для multi-label</b>. Если у объекта может быть несколько меток сразу (кот <i>и</i> собака на фото), классы не конкурируют — нужна сигмоида на каждом выходе и <a href='../bce/'>BCE</a>.",
            r"<b>Вероятность softmax как гарантия</b>. $s_{\max}=0{,}99$ не значит «прав в 99% случаев»: глубокие сети часто переуверены. Калибровка — отдельная задача; простейший способ — temperature scaling, подбор одного $T$ на валидации.",
            r"<b>Сравнение логитов разных примеров</b>. Логиты определены с точностью до сдвига, поэтому «логит 5 у одного примера больше, чем 3 у другого» ничего не значит. Сравнивайте вероятности или разности логитов внутри одного примера.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            r"<a href='../sigmoid/'>Сигмоида</a>: $\operatorname{softmax}(z_1,z_2)_1=\sigma(z_1-z_2)$, а диагональ якобиана $s_i(1-s_i)$ — производная сигмоиды.",
            r"<a href='../cross-entropy/'>Кросс-энтропия</a>: естественная пара softmax; вместе дают градиент $s-y$, а $\mathrm{CE}=\operatorname{LSE}(z)-z_y$.",
            r"<a href='../bce/'>BCE</a>: частный случай кросс-энтропии для двух классов, где softmax сводится к сигмоиде.",
            r"<a href='../focal/'>Focal Loss</a>: домножает $-\ln p_t$ на $(1-p_t)^\gamma$, где $p_t$ — softmax-вероятность правильного класса.",
            r"<a href='../relu/'>ReLU</a>: softplus $\ln(1+e^{x})=\operatorname{LSE}(x,0)$ — гладкий вариант $\max(x,0)$.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, r"1) $s_i=e^{z_i}/\sum_je^{z_j}$ превращает любые логиты в распределение на $K$ классах и сохраняет порядок. 2) Важны только разности логитов: $s_i/s_j=e^{z_i-z_j}$, сдвиг ничего не меняет — отсюда устойчивая формула с вычитанием максимума. 3) Температура управляет остротой: $T\to0$ — argmax, $T\to\infty$ — равномерное распределение. 4) Якобиан $\operatorname{diag}(s)-ss^\top$ симметричен, вырожден и затухает при уверенности; обратный проход стоит $O(K)$. 5) Softmax — градиент гладкого максимума LSE, а в паре с кросс-энтропией даёт градиент $s-y$."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q=r"Логиты $(2;\,1;\,0)$ дают $s\approx(0{,}665;\,0{,}245;\,0{,}090)$. Что даст $(102;\,101;\,100)$?", options=[r"$(0{,}665;\,0{,}245;\,0{,}090)$", r"Почти $(1;\,0;\,0)$", r"$(\tfrac13;\,\tfrac13;\,\tfrac13)$", "Ответа нет: переполнение"], answer=0,
                 explain=r"Общая константа $100$ сокращается: softmax зависит только от разностей. (Наивный код во float32 здесь действительно переполнится — поэтому и вычитают максимум.)"),
            dict(q=r"Что происходит с $\operatorname{softmax}(z/T)$ при $T\to0$?", options=["Стремится к равномерному распределению", "Не меняется", "Стремится к one-hot вектору наибольшего логита", "Все вероятности стремятся к 0"], answer=2,
                 explain=r"Разности логитов делятся на малое $T$ и растут, вся масса уходит к максимальному логиту (если он единственный)."),
            dict(q=r"Чему равен $\operatorname{softmax}(z_1,z_2)_1$?", options=[r"$\sigma(z_1)$", r"$\sigma(z_1-z_2)$", r"$\sigma(z_1+z_2)$", r"$z_1/(z_1+z_2)$"], answer=1,
                 explain=r"Разделите числитель и знаменатель $e^{z_1}/(e^{z_1}+e^{z_2})$ на $e^{z_1}$: получится $1/(1+e^{-(z_1-z_2)})$."),
            dict(q="Чему равна сумма элементов любого столбца матрицы Якоби softmax?", options=["1", r"$s_j$", r"$\tfrac14$", "0"], answer=3,
                 explain=r"$\sum_i\partial s_i/\partial z_j=\partial\bigl(\sum_i s_i\bigr)/\partial z_j=\partial1/\partial z_j=0$."),
            dict(q=r"Зачем в устойчивом softmax вычитают $\max_j z_j$?", options=["Чтобы экспонента не переполнялась; результат не меняется", "Чтобы распределение стало острее", "Чтобы сумма стала равна 1", "Чтобы обучение шло быстрее"], answer=0,
                 explain=r"После вычитания наибольший показатель равен 0, знаменатель лежит между 1 и $K$, а по инвариантности к сдвигу ответ тот же."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", r"A classifier with $K$ classes ends with $K$ numbers — <b>logits</b>: for example, $(2,\,1,\,0)$ for “cat”, “dog”, “bird”. They are just scores: they can be negative, they do not add up to 1, and they do not tell how sure the model is. Softmax turns such a vector into a probability distribution: all numbers are positive, they sum to 1, and the order is preserved — a higher score means a higher probability."),
        ("p", "Where it appears:"),
        ("ul", [
            r"<b>the output of a multi-class classifier</b> — from logistic regression to ResNet and ViT: $\hat y=\operatorname{softmax}(Wx+b)$;",
            r"<b>language models</b> — at every step an LLM outputs logits for every token in its vocabulary (tens or hundreds of thousands), softmax turns them into the distribution of the next token, and temperature controls how bold the generation is;",
            r"<b>attention</b> in transformers — the weights $\operatorname{softmax}(QK^\top/\sqrt d)$ decide which tokens to look at;",
            r"<b>mixture of experts (MoE)</b> — the router distributes a token among experts through a softmax;",
            r"<b>reinforcement learning</b> — a Boltzmann policy picks action $a$ with probability proportional to $e^{Q(a)/T}$;",
            r"<b>statistical physics</b> — it is the Boltzmann–Gibbs distribution $p_i\propto e^{-E_i/(kT)}$; hence the word “temperature”.",
        ]),
        ("callout", "key", "The essentials in a minute", r"$s_i=e^{z_i}/\sum_j e^{z_j}$: the exponential makes every number positive and turns differences into ratios, and dividing by the sum normalizes. Softmax does not change when one constant is added to all logits (which is why code subtracts the maximum), its derivative is the matrix $\operatorname{diag}(s)-ss^\top$, and for two classes it coincides with the <a href='../sigmoid/'>sigmoid</a> of the logit difference."),
    ]),
    dict(id="intuition", title="Intuition: a vote with amplification", blocks=[
        ("p", r"Think of the classes as candidates and of the logits as their scores. To get shares of the “vote”, the scores must be made positive and normalized. Simply dividing by the sum does not work: scores can be negative and the sum can be zero. The exponential solves both problems: $e^{z}$ is always positive, and a difference in scores becomes a <i>ratio</i>: every unit of advantage makes a candidate’s share $e\approx2.718$ times its rival’s."),
        ("p", "Drag the tops of the logit bars on the left and watch the probabilities on the right. Then press “+1 to every logit”: the bars on the left rise, while nothing changes on the right."),
        ("viz", "softmax-bars", {"z": [2, 1, 0], "T": 1}, r"<b>Figure 1.</b> Logits and probabilities. The logits $(2,\,1,\,0)$ give $(0.665,\,0.245,\,0.090)$, and the sum of exponentials is $11.11$. The ±1 buttons shift every logit — the probabilities stay put. The temperature slider: at $T=0.1$ the first class gets more than $0.9999$, at $T=10$ the distribution is almost uniform, $(0.367,\,0.332,\,0.301)$. The dashed line is the level $1/K$."),
        ("callout", "intuition", "What to notice", r"The logits $(2,\,1,\,0)$ differ by one, while the probabilities differ by a factor of $e$: $0.665/0.245\approx0.245/0.090\approx2.718$. Softmax only looks at logit <i>differences</i>. The temperature $T$ divides the logits: for $T&lt;1$ the differences grow and the distribution sharpens, for $T&gt;1$ it flattens."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("eq", r"s_i=\operatorname{softmax}(z)_i=\frac{e^{z_i}}{\sum_{j=1}^{K}e^{z_j}},\qquad i=1,\dots,K"),
        ("symbols", [
            (r"z=(z_1,\dots,z_K)", "the vector of logits — raw outputs of the last layer, any real numbers;"),
            (r"e^{z_i}", "the exponential: makes the number positive and turns logit differences into ratios;"),
            (r"\sum_{j}e^{z_j}", "the normalizing sum (in physics, the partition function $Z$);"),
            (r"s_i", r"the probability of class $i$: $s_i\in(0,\,1)$ and $\sum_i s_i=1$."),
        ]),
        ("p", r"Let us walk through the cheat sheet’s running example — the logits $z=(2,\,1,\,0)$:"),
        ("eq", r"\begin{gathered}e^{2}\approx7.389,\quad e^{1}\approx2.718,\quad e^{0}=1,\quad\textstyle\sum\approx11.107\\ \Longrightarrow\;s\approx\Bigl(\frac{7.389}{11.107},\,\frac{2.718}{11.107},\,\frac{1}{11.107}\Bigr)=(0.665,\,0.245,\,0.090)\end{gathered}"),
        ("h3", "Temperature"),
        ("p", r"Logits are often divided by a number $T&gt;0$, the <b>temperature</b>, before the softmax:"),
        ("eq", r"s_i(T)=\frac{e^{z_i/T}}{\sum_j e^{z_j/T}}"),
        ("p", r"The table shows what temperature does to the same vector $(2,\,1,\,0)$:"),
        ("table", "HEADS", "TABLE", {"num": [1, 2, 3, 4, 5]}),
        ("p", r"Two limits explain the name. As $T\to0$ only the largest logit wins: softmax tends to the one-hot vector of the $\operatorname{argmax}$ (if the maximum is unique). As $T\to\infty$ the differences vanish and the distribution becomes uniform, $s_i\to1/K$. Softmax is a “soft” argmax: something between a hard choice and complete indifference."),
        ("callout", "note", "About the name", r"Strictly speaking, softmax smoothly approximates not the max function but the one-hot argmax vector. The smooth maximum is log-sum-exp, and softmax is its gradient (see the section <a href='#lse'>on LSE</a>)."),
    ]),
    dict(id="properties", title="Properties", blocks=[
        ("ul", [
            r"<b>A distribution</b>: $s_i&gt;0$ and $\sum_i s_i=1$ for any logits. Exactly 0 or 1 never happens — only in the limit (and on a computer, through rounding).",
            r"<b>Order-preserving</b>: $z_i&gt;z_j\iff s_i&gt;s_j$, so $\operatorname{argmax}s=\operatorname{argmax}z$. To merely predict the class you can skip the softmax.",
            r"<b>Ratios</b>: $s_i/s_j=e^{z_i-z_j}$ — the logit difference is the logarithm of the probability ratio. Conversely, $z_i=\ln s_i+C$: logits are recovered from probabilities up to a common constant.",
            r"<b>Shift invariance</b>: $\operatorname{softmax}(z+c\mathbf 1)=\operatorname{softmax}(z)$ for any number $c$. Of $K$ logits only $K-1$ differences matter.",
            r"<b>No scale invariance</b>: $\operatorname{softmax}(az)$ is sharper for $a&gt;1$ and flatter for $0&lt;a&lt;1$. This is the same temperature, $a=1/T$.",
            r"<b>Competition</b>: raising one logit increases its probability and decreases all the others — mass is redistributed, not created.",
        ]),
        ("deep", "Why a shift changes nothing", [
            ("eq", r"\frac{e^{z_i+c}}{\sum_j e^{z_j+c}}=\frac{e^{c}\,e^{z_i}}{e^{c}\sum_j e^{z_j}}=\frac{e^{z_i}}{\sum_j e^{z_j}}"),
            ("p", r"The factor $e^c$ cancels. This is exactly what lets code subtract $\max_j z_j$ from every logit: the result is the same, and the exponential no longer overflows."),
        ]),
        ("h3", "Two classes are a sigmoid"),
        ("eq", r"\operatorname{softmax}(z_1,z_2)_1=\frac{e^{z_1}}{e^{z_1}+e^{z_2}}=\frac{1}{1+e^{-(z_1-z_2)}}=\sigma(z_1-z_2)"),
        ("p", r"For two classes softmax is the <a href='../sigmoid/'>sigmoid</a> of the logit difference, which is why a binary classifier needs only one output. A similar formula holds for $K$ classes if we look at one class against all the others:"),
        ("eq", r"s_i=\sigma\Bigl(z_i-\ln\sum_{j\ne i}e^{z_j}\Bigr)"),
        ("p", r"Every probability is a sigmoid of how far its logit is ahead of the “smooth maximum” of the rest. To check it, divide the numerator and the denominator of $s_i$ by $e^{z_i}$."),
        ("viz", "softmax-sigmoid", {"z1": 2, "z2": 1, "z3": 0}, r"<b>Figure 2.</b> $s_1$ as a function of $z_1$ with $z_2=1$, $z_3=0$ fixed. The blue curve is a sigmoid shifted to the point $m=\ln(e^{1}+e^{0})\approx1.313$: at $z_1=2$ we get $\sigma(0.687)\approx0.665$. The orange and teal curves are $s_2$ and $s_3$: they decrease, handing their mass to the first class. Untick “There is a third class” and an ordinary sigmoid $\sigma(z_1-z_2)$ remains."),
    ]),
    dict(id="geometry", title="Geometry: the probability simplex", blocks=[
        ("p", r"All distributions over $K$ classes form the <b>probability simplex</b>:"),
        ("eq", r"\Delta^{K-1}=\Bigl\{s\in\mathbb R^{K}:\ s_i\ge0,\ \textstyle\sum_i s_i=1\Bigr\}"),
        ("p", r"For $K=3$ it is an equilateral triangle. The vertices are confident answers $(1,\,0,\,0)$, $(0,\,1,\,0)$, $(0,\,0,\,1)$, the centre is the uniform distribution $(\tfrac13,\,\tfrac13,\,\tfrac13)$, and a point inside is a “mixture” of the vertices with weights $s_i$ (barycentric coordinates)."),
        ("p", r"Softmax maps the whole logit space $\mathbb R^K$ onto the <i>interior</i> of the simplex: the edges and vertices are out of reach. All points of the line $z+c\mathbf 1$ land on one point, so in essence softmax is a one-to-one correspondence between the $(K-1)$-dimensional space of logit differences and the interior of the simplex. The inverse map is the logarithm: $z=\ln s$ up to a shift."),
        ("viz", "softmax-simplex", {"z": [2, 1, 0]}, r"<b>Figure 3.</b> A distribution over three classes is a point of the triangle; the shading shows which class wins and how confidently. Drag the black point: on the right are the same probabilities as bars, below are the logits that produce this point. The black dashed line is the path as the temperature changes: from the winning vertex ($T\to0$) to the centre ($T\to\infty$). The blue line is the path when only $z_1$ changes: from the opposite edge to vertex 1. At $z=(2,\,1,\,0)$ the centred logits are $(1,\,0,\,-1)$ and the entropy is $0.832$."),
        ("callout", "intuition", "Entropy is the distance from the vertices", r"The entropy $H(s)=-\sum_i s_i\ln s_i$ measures uncertainty: it tends to 0 near the vertices and is largest at the centre, where it equals $\ln K$. For $(0.665,\,0.245,\,0.090)$ it is $0.832$, with a maximum of $\ln3\approx1.099$."),
    ]),
    dict(id="derivative", title="The derivative: the Jacobian matrix", blocks=[
        ("p", r"Softmax has $K$ inputs and $K$ outputs, so its derivative is not a number but a $K\times K$ matrix: the entry $J_{ij}=\partial s_i/\partial z_j$ shows how the $i$-th probability responds to the $j$-th logit."),
        ("deep", "Derivation with the quotient rule", [
            ("p", r"Let $S=\sum_k e^{z_k}$; then $\partial S/\partial z_j=e^{z_j}$. For $i=j$:"),
            ("eq", r"\frac{\partial s_i}{\partial z_i}=\frac{e^{z_i}S-e^{z_i}e^{z_i}}{S^{2}}=s_i-s_i^{2}=s_i(1-s_i)"),
            ("p", r"For $i\ne j$ the numerator $e^{z_i}$ does not depend on $z_j$:"),
            ("eq", r"\frac{\partial s_i}{\partial z_j}=\frac{0\cdot S-e^{z_i}e^{z_j}}{S^{2}}=-s_is_j"),
        ]),
        ("deep", "Derivation through the logarithm (shorter)", [
            ("p", r"$\ln s_i=z_i-\ln S$. The derivative of the log of a sum of exponentials is softmax again: $\partial\ln S/\partial z_j=e^{z_j}/S=s_j$. Hence"),
            ("eq", r"\frac{\partial\ln s_i}{\partial z_j}=\delta_{ij}-s_j\quad\Longrightarrow\quad\frac{\partial s_i}{\partial z_j}=s_i(\delta_{ij}-s_j)"),
            ("p", r"Here $\delta_{ij}$ is the Kronecker delta: 1 if $i=j$ and 0 otherwise."),
        ]),
        ("eq", r"J=\frac{\partial s}{\partial z}=\operatorname{diag}(s)-s\,s^{\top},\qquad J_{ij}=\begin{cases}s_i(1-s_i),&i=j\\-s_is_j,&i\ne j\end{cases}"),
        ("p", "Properties of this matrix:"),
        ("ul", [
            r"<b>the diagonal</b> $s_i(1-s_i)$ is exactly the derivative of the sigmoid: at most $\tfrac14$, largest at $s_i=\tfrac12$;",
            r"<b>off the diagonal</b> every entry is negative: raising one logit takes probability away from the others;",
            r"<b>it is symmetric</b>, and every row (and column) sums to 0: $J\mathbf 1=s-s\,(s^\top\mathbf 1)=0$. This is the derivative of $\sum_i s_i=1$, and the vector $\mathbf 1$ is the shift direction that changes nothing. Hence $J$ is singular;",
            r"<b>it is positive semi-definite</b>: $v^\top Jv=\sum_i s_iv_i^2-\bigl(\sum_i s_iv_i\bigr)^2$ is the variance of $v$ under the distribution $s$, and a variance is never negative;",
            r"<b>it fades with confidence</b>: when $s$ is close to a vertex of the simplex, every entry of $J$ is close to zero — saturation, as with the sigmoid.",
        ]),
        ("viz", "softmax-jacobian", {"z": [2, 1, 0], "j": 0}, r"<b>Figure 4.</b> On the left, the Jacobian at $z=(2,\,1,\,0)$: the diagonal $(0.223,\,0.185,\,0.082)$ is positive (red), the off-diagonal entries $-0.163$, $-0.060$, $-0.022$ are negative (blue); every column sums to 0, and the trace is $1-\sum s_i^2\approx0.4895$. On the right, the entries of the chosen column as functions of $z_j$: the diagonal one is the bell $s_j(1-s_j)$ peaking at $0.25$ where $s_j=0.5$; the others are negative “dips”."),
        ("h3", "A backward pass without the matrix"),
        ("p", r"Backprop needs not $J$ itself but the product $J^\top g$, where $g=\partial L/\partial s$ comes from above. Thanks to the structure $\operatorname{diag}(s)-ss^\top$ it costs $O(K)$ operations instead of $O(K^2)$:"),
        ("eq", r"\frac{\partial L}{\partial z}=J^{\top}g=s\odot\bigl(g-\langle g,s\rangle\,\mathbf 1\bigr)"),
        ("p", r"For an LLM vocabulary of $K\approx10^5$ tokens this is the difference between $10^5$ and $10^{10}$ numbers per position. Paired with cross-entropy it gets simpler still: $\partial L/\partial z=s-y$ (derived on the <a href='../cross-entropy/'>cross-entropy</a> page)."),
    ]),
    dict(id="surface", title="The 3D picture: softmax over the logit plane", blocks=[
        ("p", r"Fix $z_3=0$ — no loss of generality, since a shift can make any logit zero — and draw $s_1$ as a function of the two variables $z_1$ and $z_2$. The result is a “ramp”: the surface is close to 1 where $z_1$ exceeds both $z_2$ and zero, and close to 0 where the first class loses. Across the boundary it rises along a sigmoid — the one-against-all formula in action."),
        ("viz", "softmax-surface", {"z": [2, 1]}, r"<b>Figure 5.</b> On the left, $s_k(z_1,z_2,0)$ in 3D (the surface can be rotated); the black point is $z=(2,\,1,\,0)$ with $s_1\approx0.665$. On the right, the logit plane: the shading shows the winning class and its confidence, the lines are the levels $0.1$, $0.5$, $0.9$ of the chosen function ($0.05$, $0.15$, $0.24$ for the derivative). The point can be dragged. Switch to $\partial s_1/\partial z_1$: it is a ridge of height $0.25$ along the line $s_1=0.5$."),
        ("p", r"The top view splits the logit plane into three regions. The boundaries are the sets of equal logits: the ray $z_1=z_2\ge0$ separates classes 1 and 2, the ray $z_1=0$, $z_2\le0$ separates classes 1 and 3, and the ray $z_2=0$, $z_1\le0$ separates classes 2 and 3. All three rays start at the origin, where $s=(\tfrac13,\,\tfrac13,\,\tfrac13)$."),
        ("callout", "note", "Where the gradient flows", r"The surface $\partial s_1/\partial z_1=s_1(1-s_1)$ is almost flat and almost zero deep inside the class’s “own” and “foreign” regions. Gradient flows through softmax only where the model is in doubt — near the boundaries."),
    ]),
    dict(id="lse", title="Log-sum-exp: a smooth maximum", blocks=[
        ("p", r"Softmax has an “antiderivative” — the log-sum-exp function:"),
        ("eq", r"\operatorname{LSE}(z)=\ln\sum_{j=1}^{K}e^{z_j},\qquad\frac{\partial\operatorname{LSE}}{\partial z_i}=\frac{e^{z_i}}{\sum_j e^{z_j}}=s_i,\qquad\nabla\operatorname{LSE}(z)=\operatorname{softmax}(z)"),
        ("p", r"LSE is a smooth maximum: the largest exponential dominates the sum, and the logarithm returns almost its exponent. More precisely,"),
        ("eq", r"\max_j z_j\;\le\;\operatorname{LSE}(z)\;\le\;\max_j z_j+\ln K"),
        ("p", r"The left inequality holds because a sum is at least its largest term, the right one because each of the $K$ terms is at most the largest. For $(2,\,1,\,0)$: $\operatorname{LSE}=\ln11.107\approx2.408$ — between $2$ and $2+\ln3\approx3.099$. With a temperature, $\operatorname{LSE}_T(z)=T\ln\sum_j e^{z_j/T}$, the gap shrinks to $T\ln K$: as $T\to0$ LSE becomes the ordinary maximum, and its gradient $\operatorname{softmax}(z/T)$ becomes the one-hot argmax vector."),
        ("viz", "softmax-lse", {"T": 1, "x": 1}, r"<b>Figure 6.</b> Top: $\operatorname{LSE}_T(x,0)=T\ln(e^{x/T}+1)$ and $\max(x,0)$; the gap is at most $T\ln2$ and is largest at $x=0$. At $T=1$, $x=1$: $\operatorname{LSE}\approx1.3133$, the gap is $0.3133$. Bottom: the derivative in $x$ — it is $\sigma(x/T)$, the first component of $\operatorname{softmax}(x/T,\,0)$, a smooth step. Decrease $T$ and LSE hugs the broken line while softmax hugs the step."),
        ("deep", "Convexity of LSE and of cross-entropy", [
            ("p", r"The Hessian of LSE is the derivative of softmax, i.e. the same Jacobian: $\nabla^2\operatorname{LSE}=\operatorname{diag}(s)-ss^\top$. It is positive semi-definite, so LSE is a convex function. Hence cross-entropy is convex in the logits: $-\ln s_y=\operatorname{LSE}(z)-z_y$ is a convex function minus a linear one."),
        ]),
        ("callout", "key", "Three formulas worth connecting", r"$\operatorname{softmax}=\nabla\operatorname{LSE}$; $\ln s_i=z_i-\operatorname{LSE}(z)$ (log-softmax); $\mathrm{CE}=\operatorname{LSE}(z)-z_y$. For the cheat sheet’s example: $2.408-2=0.408$. And for $K=2$, $z=(x,\,0)$, LSE becomes softplus $\ln(1+e^{x})$ — a smooth version of <a href='../relu/'>ReLU</a>."),
    ]),
    dict(id="training", title="Softmax in training", blocks=[
        ("p", r"The simplest model with a softmax is multinomial logistic (softmax) regression: $K$ linear functions give the logits, softmax gives the probabilities, and the loss is <a href='../cross-entropy/'>cross-entropy</a>:"),
        ("eq", r"s=\operatorname{softmax}(Wx+b),\qquad L=-\ln s_y,\qquad\frac{\partial L}{\partial W}=(s-y)\,x^{\top},\qquad\frac{\partial L}{\partial b}=s-y"),
        ("p", r"Here $y$ is the one-hot vector of the correct class. The whole Jacobian, paired with the logarithm, has collapsed into the difference “prediction − truth”."),
        ("viz", "softmax-regression", {}, r"<b>Figure 7.</b> Three classes of 30 points each. The model starts at $W=0$, $b=0$: every probability is $\tfrac13$, $\mathrm{CE}=\ln3\approx1.099$, accuracy $33.3\%$. Press “Play”: full-batch gradient descent with step $0.15$. After the very first step the accuracy is $94.4\%$; after 200 steps $\mathrm{CE}\approx0.181$ and the accuracy is $95.6\%$. The brightness of the shading is the model’s confidence; hover to see the probabilities at any point."),
        ("callout", "note", "The boundaries are straight", r"The boundary between classes $i$ and $j$ is the set where $z_i=z_j$, that is $(w_i-w_j)^\top x+b_i-b_j=0$: a line (a hyperplane in general). Softmax does not make the model non-linear — it only turns scores into probabilities. Curved boundaries appear when a neural network computes the logits."),
        ("h3", "Softmax inside the transformer: attention"),
        ("eq", r"\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\Bigl(\frac{QK^{\top}}{\sqrt{d}}\Bigr)V"),
        ("p", r"Each row of $\operatorname{softmax}(\cdot)$ is how one token spreads its attention over the tokens of the sequence (itself included), with weights summing to 1. Dividing by $\sqrt d$ is a temperature: the dot product of $d$-dimensional vectors with independent zero-mean, unit-variance components has variance $d$. Without the scaling the attention logits are large, softmax saturates to nearly one-hot, and the Jacobian — and with it the gradients — nearly vanishes."),
        ("h3", "Temperature in text generation"),
        ("p", r"A language model draws the next token from $\operatorname{softmax}(z/T)$. As $T\to0$ (greedy decoding) the most likely token is taken; with $T&lt;1$ the text is more predictable, with $T&gt;1$ more diverse and riskier. A temperature $T&gt;1$ also appears in knowledge distillation (Hinton et al., 2015): the teacher’s “soft” probabilities carry more information than one-hot labels."),
        ("callout", "history", "Where the name comes from", r"The formula came from statistical physics: the Boltzmann–Gibbs distribution $p_i\propto e^{-E_i/(kT)}$ gives the probability of a state with energy $E_i$ at temperature $T$; a logit plays the role of minus the energy. The word “softmax” was coined by John Bridle in 1990, when describing a probabilistic interpretation of network outputs. In econometrics the same model is called the multinomial logit."),
    ]),
    dict(id="code", title="In code: stability, log-softmax and PyTorch", blocks=[
        ("p", r"The naive formula breaks on large logits: $e^{1000}\approx2\cdot10^{434}$ fits in neither float32 nor float64 and becomes infinity, which then gives $\infty/\infty=\text{NaN}$. In float32 (and in bfloat16, which has the same exponent range) the limit is closer: $e^{x}$ overflows already for $x&gt;88.72$ (the largest float32 is $\approx3.4\cdot10^{38}$). On very negative logits the trouble is the opposite: the exponentials underflow to zero, giving $0/0$."),
        ("viz", "softmax-overflow", {"c": 0}, r"<b>Figure 8.</b> The logits $(2+c,\,1+c,\,c)$ for $c$ from $-800$ to $800$; the correct answer is always $(0.665,\,0.245,\,0.090)$. In float32 the naive formula is right only for $-99\le c\le86$: at $c=87$ the number $e^{89}$ does not fit in float32 and the result is NaN; at $c\le-106$ every exponential is zero, $0/0$; and in between, subnormal numbers lose precision — at $c=-105$ the output is a confident but false $(1,\,0,\,0)$. float64 has more room ($-741\le c\le707$), but a limit as well. With the maximum subtracted the answer is right everywhere."),
        ("p", r"The cure is shift invariance: subtract $m=\max_j z_j$. The largest exponent becomes 0, $e^0=1$, and the denominator lies between 1 and $K$ — no overflow, no division by zero:"),
        ("eq", r"s_i=\frac{e^{z_i-m}}{\sum_j e^{z_j-m}},\qquad\ln s_i=(z_i-m)-\ln\sum_j e^{z_j-m}"),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "The rule", r"If a logarithm follows, do not compute $\ln(\operatorname{softmax}(z))$ in two steps: a small probability rounds to 0 and you get $-\infty$. Use <code>log_softmax</code> or a loss on logits directly: <code>F.cross_entropy</code> / <code>nn.CrossEntropyLoss</code> in PyTorch, <code>from_logits=True</code> in Keras."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            r"<b>A softmax before <code>nn.CrossEntropyLoss</code></b>. This loss expects logits and applies log-softmax itself. A double softmax squeezes the probabilities: for three classes the second softmax never exceeds $e/(e+2)\approx0.576$, the loss cannot drop below $0.551$, and the gradients are distorted.",
            r"<b>The wrong axis</b>. For a batch of shape $(N,K)$ normalize over classes (<code>dim=-1</code>), not over examples (<code>dim=0</code>). No exception is raised — the model simply learns nonsense.",
            r"<b>A naive exponential</b> without subtracting the maximum — NaN on large logits, especially in mixed precision: in float16 $e^{x}$ overflows already for $x&gt;11.09$.",
            r"<b>Softmax for multi-label</b>. If an object can carry several labels at once (a cat <i>and</i> a dog in a photo), the classes do not compete — use a sigmoid on every output and <a href='../bce/'>BCE</a>.",
            r"<b>A softmax probability as a guarantee</b>. $s_{\max}=0.99$ does not mean “right 99% of the time”: deep networks are often overconfident. Calibration is a separate task; the simplest method is temperature scaling, fitting a single $T$ on validation data.",
            r"<b>Comparing logits of different examples</b>. Logits are defined up to a shift, so “a logit of 5 for one example is more than 3 for another” means nothing. Compare probabilities, or logit differences within one example.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            r"<a href='../sigmoid/'>Sigmoid</a>: $\operatorname{softmax}(z_1,z_2)_1=\sigma(z_1-z_2)$, and the Jacobian’s diagonal $s_i(1-s_i)$ is the derivative of the sigmoid.",
            r"<a href='../cross-entropy/'>Cross-entropy</a>: softmax’s natural partner; together they give the gradient $s-y$, and $\mathrm{CE}=\operatorname{LSE}(z)-z_y$.",
            r"<a href='../bce/'>BCE</a>: the two-class special case of cross-entropy, where softmax reduces to the sigmoid.",
            r"<a href='../focal/'>Focal Loss</a>: multiplies $-\ln p_t$ by $(1-p_t)^\gamma$, where $p_t$ is the softmax probability of the correct class.",
            r"<a href='../relu/'>ReLU</a>: softplus $\ln(1+e^{x})=\operatorname{LSE}(x,0)$ is a smooth version of $\max(x,0)$.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, r"1) $s_i=e^{z_i}/\sum_je^{z_j}$ turns any logits into a distribution over $K$ classes and preserves their order. 2) Only logit differences matter: $s_i/s_j=e^{z_i-z_j}$, and a shift changes nothing — hence the stable formula that subtracts the maximum. 3) Temperature controls sharpness: $T\to0$ gives argmax, $T\to\infty$ the uniform distribution. 4) The Jacobian $\operatorname{diag}(s)-ss^\top$ is symmetric, singular and fades with confidence; the backward pass costs $O(K)$. 5) Softmax is the gradient of the smooth maximum LSE, and paired with cross-entropy it gives the gradient $s-y$."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q=r"The logits $(2,\,1,\,0)$ give $s\approx(0.665,\,0.245,\,0.090)$. What do $(102,\,101,\,100)$ give?", options=[r"$(0.665,\,0.245,\,0.090)$", r"Almost $(1,\,0,\,0)$", r"$(\tfrac13,\,\tfrac13,\,\tfrac13)$", "No answer: overflow"], answer=0,
                 explain=r"The common constant $100$ cancels: softmax depends only on differences. (Naive float32 code would indeed overflow here — that is why the maximum is subtracted.)"),
            dict(q=r"What happens to $\operatorname{softmax}(z/T)$ as $T\to0$?", options=["It tends to the uniform distribution", "It does not change", "It tends to the one-hot vector of the largest logit", "All probabilities tend to 0"], answer=2,
                 explain=r"The logit differences are divided by a small $T$ and grow, so all the mass goes to the largest logit (if it is unique)."),
            dict(q=r"What is $\operatorname{softmax}(z_1,z_2)_1$?", options=[r"$\sigma(z_1)$", r"$\sigma(z_1-z_2)$", r"$\sigma(z_1+z_2)$", r"$z_1/(z_1+z_2)$"], answer=1,
                 explain=r"Divide the numerator and the denominator of $e^{z_1}/(e^{z_1}+e^{z_2})$ by $e^{z_1}$: you get $1/(1+e^{-(z_1-z_2)})$."),
            dict(q="What is the sum of the entries of any column of the softmax Jacobian?", options=["1", r"$s_j$", r"$\tfrac14$", "0"], answer=3,
                 explain=r"$\sum_i\partial s_i/\partial z_j=\partial\bigl(\sum_i s_i\bigr)/\partial z_j=\partial1/\partial z_j=0$."),
            dict(q=r"Why does a stable softmax subtract $\max_j z_j$?", options=["So that the exponential does not overflow; the result is unchanged", "To sharpen the distribution", "To make the sum equal 1", "To speed up training"], answer=0,
                 explain=r"After the subtraction the largest exponent is 0, the denominator lies between 1 and $K$, and by shift invariance the answer is the same."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", r"$K$ ta sinfli klassifikator oxirida $K$ ta son chiqaradi — <b>logitlar</b> (logits): masalan, «mushuk», «it», «qush» uchun $(2;\,1;\,0)$. Bular shunchaki ballar: ular manfiy bo‘lishi mumkin, yig‘indisi 1 ga teng emas va ulardan modelning qanchalik ishonchli ekani ko‘rinmaydi. Softmax bunday vektorni ehtimolliklar taqsimotiga aylantiradi: barcha sonlar musbat, yig‘indisi 1, tartib esa saqlanadi — balli katta bo‘lganning ehtimolligi ham katta."),
        ("p", "U qayerda uchraydi:"),
        ("ul", [
            r"<b>ko‘p sinfli klassifikator chiqishi</b> — logistik regressiyadan ResNet va ViT’gacha: $\hat y=\operatorname{softmax}(Wx+b)$;",
            r"<b>til modellari</b> — LLM har qadamda lug‘atdagi barcha tokenlar (o‘n va yuz minglab) uchun logit chiqaradi, softmax ulardan keyingi token taqsimotini yasaydi, harorat esa generatsiyaning «jasoratini» boshqaradi;",
            r"<b>transformerlardagi attention (diqqat) mexanizmi</b> — $\operatorname{softmax}(QK^\top/\sqrt d)$ vaznlari qaysi tokenlarga qarashni hal qiladi;",
            r"<b>ekspertlar aralashmasi (MoE)</b> — marshrutlovchi tokenni ekspertlar orasida softmax orqali taqsimlaydi;",
            r"<b>mustahkamlab o‘qitish</b> — Bolsman siyosati $a$ harakatni $e^{Q(a)/T}$ ga proporsional ehtimollik bilan tanlaydi;",
            r"<b>statistik fizika</b> — bu Bolsman — Gibbs taqsimoti $p_i\propto e^{-E_i/(kT)}$; «harorat» so‘zi ham shu yerdan.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", r"$s_i=e^{z_i}/\sum_j e^{z_j}$: eksponenta barcha sonlarni musbat qiladi va ayirmalarni nisbatlarga aylantiradi, yig‘indiga bo‘lish esa normallaydi. Barcha logitlarga bitta o‘zgarmas qo‘shilsa, softmax o‘zgarmaydi (shuning uchun kodda maksimum ayiriladi), uning hosilasi — $\operatorname{diag}(s)-ss^\top$ matritsa, ikki sinf uchun esa u logitlar ayirmasining <a href='../sigmoid/'>sigmoidasi</a> bilan ustma-ust tushadi."),
    ]),
    dict(id="intuition", title="Intuitsiya: kuchaytirilgan ovoz berish", blocks=[
        ("p", r"Sinflarni nomzodlar, logitlarni esa ularning ballari deb tasavvur qiling. «Ovozlar» ulushini olish uchun ballarni musbat qilish va normallash kerak. Shunchaki yig‘indiga bo‘lib bo‘lmaydi: ballar manfiy, yig‘indi esa nol bo‘lishi mumkin. Eksponenta ikkala muammoni hal qiladi: $e^{z}$ doim musbat, ballar ayirmasi esa <i>nisbatga</i> aylanadi: har bir birlik ustunlik nomzod ulushini raqibnikidan $e\approx2{,}718$ marta katta qiladi."),
        ("p", "Chapdagi logit-ustunlarning uchini torting va o‘ngdagi ehtimolliklar qanday o‘zgarishini kuzating. Keyin «Barcha logitlarga +1» tugmasini bosing: chapdagi ustunlar ko‘tariladi, o‘ngda esa hech narsa o‘zgarmaydi."),
        ("viz", "softmax-bars", {"z": [2, 1, 0], "T": 1}, r"<b>1-rasm.</b> Logitlar va ehtimolliklar. $(2;\,1;\,0)$ logitlar $(0{,}665;\,0{,}245;\,0{,}090)$ ni beradi, eksponentalar yig‘indisi $11{,}11$. ±1 tugmalari barcha logitlarni siljitadi — ehtimolliklar joyida qoladi. Harorat slayderi: $T=0{,}1$ da birinchi sinfga $0{,}9999$ dan ko‘prog‘i tegadi, $T=10$ da taqsimot deyarli tekis, $(0{,}367;\,0{,}332;\,0{,}301)$. Punktir — $1/K$ darajasi."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", r"$(2;\,1;\,0)$ logitlar bittaga farq qiladi, ehtimolliklar esa $e$ marta: $0{,}665/0{,}245\approx0{,}245/0{,}090\approx2{,}718$. Softmax faqat logitlarning <i>ayirmalariga</i> qaraydi. $T$ harorat logitlarni bo‘ladi: $T&lt;1$ da ayirmalar o‘sadi va taqsimot keskinlashadi, $T&gt;1$ da — silliqlashadi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("eq", r"s_i=\operatorname{softmax}(z)_i=\frac{e^{z_i}}{\sum_{j=1}^{K}e^{z_j}},\qquad i=1,\dots,K"),
        ("symbols", [
            (r"z=(z_1,\dots,z_K)", "logitlar vektori — oxirgi qatlamning xom chiqishlari, istalgan haqiqiy sonlar;"),
            (r"e^{z_i}", "eksponenta: sonni musbat qiladi va logitlar ayirmalarini nisbatlarga aylantiradi;"),
            (r"\sum_{j}e^{z_j}", "normallovchi yig‘indi (fizikada — statistik yig‘indi, partition function $Z$);"),
            (r"s_i", r"$i$-sinf ehtimolligi: $s_i\in(0;\,1)$ va $\sum_i s_i=1$."),
        ]),
        ("p", r"Qo‘llanmadagi umumiy misolni ko‘rib chiqamiz — $z=(2;\,1;\,0)$ logitlar:"),
        ("eq", r"\begin{gathered}e^{2}\approx7{,}389,\quad e^{1}\approx2{,}718,\quad e^{0}=1,\quad\textstyle\sum\approx11{,}107\\ \Longrightarrow\;s\approx\Bigl(\frac{7{,}389}{11{,}107};\,\frac{2{,}718}{11{,}107};\,\frac{1}{11{,}107}\Bigr)=(0{,}665;\,0{,}245;\,0{,}090)\end{gathered}"),
        ("h3", "Harorat"),
        ("p", r"Ko‘pincha softmax’dan oldin logitlar $T&gt;0$ songa — <b>haroratga</b> bo‘linadi:"),
        ("eq", r"s_i(T)=\frac{e^{z_i/T}}{\sum_j e^{z_j/T}}"),
        ("p", r"Jadval haroratning o‘sha $(2;\,1;\,0)$ vektor bilan nima qilishini ko‘rsatadi:"),
        ("table", "HEADS", "TABLE", {"num": [1, 2, 3, 4, 5]}),
        ("p", r"Ikki limit nomni tushuntiradi. $T\to0$ da faqat eng katta logit yutadi: softmax $\operatorname{argmax}$ ning one-hot vektoriga intiladi (agar maksimum yagona bo‘lsa). $T\to\infty$ da ayirmalar yo‘qoladi va taqsimot tekis bo‘ladi, $s_i\to1/K$. Softmax — «yumshoq» (soft) argmax: qat’iy tanlov va to‘liq befarqlik orasidagi holat."),
        ("callout", "note", "Nom haqida", r"Aniqroq aytganda, softmax max funksiyasini emas, argmax ning one-hot vektorini silliq yaqinlashtiradi. Silliq maksimum — bu log-sum-exp, softmax esa uning gradiyenti (<a href='#lse'>LSE haqidagi</a> bo‘limga qarang)."),
    ]),
    dict(id="properties", title="Xossalar", blocks=[
        ("ul", [
            r"<b>Taqsimot</b>: istalgan logitlarda $s_i&gt;0$ va $\sum_i s_i=1$. Aynan 0 yoki 1 hech qachon chiqmaydi — faqat limitda (kompyuterda esa yaxlitlash tufayli).",
            r"<b>Tartibni saqlaydi</b>: $z_i&gt;z_j\iff s_i&gt;s_j$, shuning uchun $\operatorname{argmax}s=\operatorname{argmax}z$. Faqat sinfni bashorat qilish uchun softmax’ni hisoblamasa ham bo‘ladi.",
            r"<b>Nisbatlar</b>: $s_i/s_j=e^{z_i-z_j}$ — logitlar ayirmasi ehtimolliklar nisbatining logarifmiga teng. Aksincha, $z_i=\ln s_i+C$: logitlar ehtimolliklardan umumiy o‘zgarmas aniqligida tiklanadi.",
            r"<b>Siljishga invariantlik</b>: istalgan $c$ son uchun $\operatorname{softmax}(z+c\mathbf 1)=\operatorname{softmax}(z)$. $K$ ta logitdan faqat $K-1$ ta ayirma ahamiyatli.",
            r"<b>Masshtabga invariant emas</b>: $\operatorname{softmax}(az)$ $a&gt;1$ da keskinroq, $0&lt;a&lt;1$ da yassiroq. Bu o‘sha harorat, $a=1/T$.",
            r"<b>Raqobat</b>: bitta logitning o‘sishi uning ehtimolligini oshiradi va qolganlarining hammasini kamaytiradi — massa yaratilmaydi, qayta taqsimlanadi.",
        ]),
        ("deep", "Nega siljish hech narsani o‘zgartirmaydi", [
            ("eq", r"\frac{e^{z_i+c}}{\sum_j e^{z_j+c}}=\frac{e^{c}\,e^{z_i}}{e^{c}\sum_j e^{z_j}}=\frac{e^{z_i}}{\sum_j e^{z_j}}"),
            ("p", r"$e^c$ ko‘paytuvchi qisqaradi. Aynan shu xossa kodda barcha logitlardan $\max_j z_j$ ni ayirishga imkon beradi: natija o‘sha, eksponenta esa endi to‘lib ketmaydi."),
        ]),
        ("h3", "Ikki sinf — bu sigmoida"),
        ("eq", r"\operatorname{softmax}(z_1,z_2)_1=\frac{e^{z_1}}{e^{z_1}+e^{z_2}}=\frac{1}{1+e^{-(z_1-z_2)}}=\sigma(z_1-z_2)"),
        ("p", r"Ikki sinf uchun softmax — logitlar ayirmasining <a href='../sigmoid/'>sigmoidasi</a>, shuning uchun binar klassifikatorga bitta chiqish yetarli. Bitta sinfni qolgan hammasiga qarshi qo‘ysak, $K$ ta sinf uchun ham shunga o‘xshash formula o‘rinli:"),
        ("eq", r"s_i=\sigma\Bigl(z_i-\ln\sum_{j\ne i}e^{z_j}\Bigr)"),
        ("p", r"Har bir ehtimollik — o‘z logitining qolganlarning «silliq maksimumidan» ustunligining sigmoidasi. Tekshirish uchun $s_i$ ning surat va maxrajini $e^{z_i}$ ga bo‘ling."),
        ("viz", "softmax-sigmoid", {"z1": 2, "z2": 1, "z3": 0}, r"<b>2-rasm.</b> $z_2=1$, $z_3=0$ qayd etilganda $s_1$ $z_1$ ning funksiyasi sifatida. Ko‘k egri — $m=\ln(e^{1}+e^{0})\approx1{,}313$ nuqtaga siljigan sigmoida: $z_1=2$ da $\sigma(0{,}687)\approx0{,}665$ chiqadi. To‘q sariq va firuza egrilar — $s_2$ va $s_3$: ular kamayib, massasini birinchi sinfga beradi. «Uchinchi sinf bor» belgisini olib tashlang — oddiy $\sigma(z_1-z_2)$ sigmoida qoladi."),
    ]),
    dict(id="geometry", title="Geometriya: ehtimolliklar simpleksi", blocks=[
        ("p", r"$K$ ta sinf bo‘yicha barcha taqsimotlar <b>ehtimolliklar simpleksini</b> tashkil etadi:"),
        ("eq", r"\Delta^{K-1}=\Bigl\{s\in\mathbb R^{K}:\ s_i\ge0,\ \textstyle\sum_i s_i=1\Bigr\}"),
        ("p", r"$K=3$ da bu teng tomonli uchburchak. Uchlari — ishonchli javoblar $(1;\,0;\,0)$, $(0;\,1;\,0)$, $(0;\,0;\,1)$, markazi — tekis taqsimot $(\tfrac13;\,\tfrac13;\,\tfrac13)$, ichidagi nuqta esa uchlarning $s_i$ vaznli «aralashmasi» (barisentrik koordinatalar)."),
        ("p", r"Softmax butun $\mathbb R^K$ logitlar fazosini simpleksning <i>ichki qismiga</i> akslantiradi: tomonlar va uchlarga yetib bo‘lmaydi. $z+c\mathbf 1$ to‘g‘ri chiziqning barcha nuqtalari bitta nuqtaga o‘tadi, shuning uchun mohiyatan softmax $(K-1)$ o‘lchovli logitlar ayirmalari fazosi bilan simpleks ichki qismi orasidagi o‘zaro bir qiymatli moslikdir. Teskari akslantirish — logarifm: siljish aniqligida $z=\ln s$."),
        ("viz", "softmax-simplex", {"z": [2, 1, 0]}, r"<b>3-rasm.</b> Uch sinf bo‘yicha taqsimot — uchburchakning nuqtasi; bo‘yoq qaysi sinf va qanchalik ishonch bilan yutayotganini ko‘rsatadi. Qora nuqtani torting: o‘ngda o‘sha ehtimolliklar ustunlarda, rasm ostida — shu nuqtani beradigan logitlar. Qora punktir — harorat o‘zgargandagi yo‘l: g‘olib uchdan ($T\to0$) markazga ($T\to\infty$). Ko‘k chiziq — faqat $z_1$ o‘zgargandagi yo‘l: qarama-qarshi tomondan 1-uchga. $z=(2;\,1;\,0)$ da markazlashtirilgan logitlar $(1;\,0;\,-1)$, entropiya $0{,}832$."),
        ("callout", "intuition", "Entropiya — uchlardan uzoqlik", r"$H(s)=-\sum_i s_i\ln s_i$ entropiya noaniqlikni o‘lchaydi: u uchlar yonida 0 ga intiladi va markazda eng katta bo‘lib, $\ln K$ ga teng. $(0{,}665;\,0{,}245;\,0{,}090)$ uchun $0{,}832$ chiqadi, maksimum esa $\ln3\approx1{,}099$."),
    ]),
    dict(id="derivative", title="Hosila: Yakobi matritsasi", blocks=[
        ("p", r"Softmax’ning $K$ ta kirishi va $K$ ta chiqishi bor, shuning uchun uning hosilasi son emas, balki $K\times K$ matritsa: $J_{ij}=\partial s_i/\partial z_j$ element $i$-ehtimollik $j$-logitga qanday javob berishini ko‘rsatadi."),
        ("deep", "Bo‘linma qoidasi bilan keltirib chiqarish", [
            ("p", r"$S=\sum_k e^{z_k}$ deb belgilaymiz; u holda $\partial S/\partial z_j=e^{z_j}$. $i=j$ uchun:"),
            ("eq", r"\frac{\partial s_i}{\partial z_i}=\frac{e^{z_i}S-e^{z_i}e^{z_i}}{S^{2}}=s_i-s_i^{2}=s_i(1-s_i)"),
            ("p", r"$i\ne j$ uchun $e^{z_i}$ surat $z_j$ ga bog‘liq emas:"),
            ("eq", r"\frac{\partial s_i}{\partial z_j}=\frac{0\cdot S-e^{z_i}e^{z_j}}{S^{2}}=-s_is_j"),
        ]),
        ("deep", "Logarifm orqali keltirib chiqarish (qisqaroq)", [
            ("p", r"$\ln s_i=z_i-\ln S$. Eksponentalar yig‘indisi logarifmining hosilasi yana softmax: $\partial\ln S/\partial z_j=e^{z_j}/S=s_j$. Demak,"),
            ("eq", r"\frac{\partial\ln s_i}{\partial z_j}=\delta_{ij}-s_j\quad\Longrightarrow\quad\frac{\partial s_i}{\partial z_j}=s_i(\delta_{ij}-s_j)"),
            ("p", r"Bu yerda $\delta_{ij}$ — Kroneker belgisi: $i=j$ da 1, aks holda 0."),
        ]),
        ("eq", r"J=\frac{\partial s}{\partial z}=\operatorname{diag}(s)-s\,s^{\top},\qquad J_{ij}=\begin{cases}s_i(1-s_i),&i=j\\-s_is_j,&i\ne j\end{cases}"),
        ("p", "Bu matritsaning xossalari:"),
        ("ul", [
            r"<b>diagonal</b> $s_i(1-s_i)$ — aynan sigmoidaning hosilasi: $\tfrac14$ dan oshmaydi, $s_i=\tfrac12$ da maksimal;",
            r"<b>diagonaldan tashqaridagi</b> barcha elementlar manfiy: bitta logitni ko‘tarib, qolganlaridan ehtimollik olamiz;",
            r"<b>simmetrik</b> va har bir satr (hamda ustun) yig‘indisi 0: $J\mathbf 1=s-s\,(s^\top\mathbf 1)=0$. Bu $\sum_i s_i=1$ tenglikning hosilasi, $\mathbf 1$ vektor esa hech narsani o‘zgartirmaydigan siljish yo‘nalishi. Shuning uchun $J$ xos (singulyar);",
            r"<b>nomanfiy aniqlangan</b>: $v^\top Jv=\sum_i s_iv_i^2-\bigl(\sum_i s_iv_i\bigr)^2$ — $s$ taqsimotdagi $v$ kattalikning dispersiyasi, dispersiya esa manfiy bo‘lmaydi;",
            r"<b>ishonch oshganda so‘nadi</b>: $s$ simpleks uchiga yaqin bo‘lsa, $J$ ning barcha elementlari nolga yaqin — sigmoidadagi kabi to‘yinish.",
        ]),
        ("viz", "softmax-jacobian", {"z": [2, 1, 0], "j": 0}, r"<b>4-rasm.</b> Chapda — $z=(2;\,1;\,0)$ dagi Yakobi matritsasi: $(0{,}223;\,0{,}185;\,0{,}082)$ diagonal musbat (qizil), diagonaldan tashqarida manfiy $-0{,}163$, $-0{,}060$, $-0{,}022$ (ko‘k); har bir ustun yig‘indisi 0, iz $1-\sum s_i^2\approx0{,}4895$. O‘ngda — tanlangan ustun elementlari $z_j$ ning funksiyalari sifatida: diagonal element — $s_j=0{,}5$ bo‘lgan joyda cho‘qqisi $0{,}25$ bo‘lgan $s_j(1-s_j)$ qo‘ng‘iroq; qolganlari — manfiy «chuqurlar»."),
        ("h3", "Matritsasiz teskari o‘tish"),
        ("p", r"Backprop’da $J$ ning o‘zi emas, $J^\top g$ ko‘paytma kerak, bu yerda $g=\partial L/\partial s$ yuqoridan keladi. $\operatorname{diag}(s)-ss^\top$ tuzilishi tufayli bu $O(K^2)$ o‘rniga $O(K)$ amal turadi:"),
        ("eq", r"\frac{\partial L}{\partial z}=J^{\top}g=s\odot\bigl(g-\langle g,s\rangle\,\mathbf 1\bigr)"),
        ("p", r"$K\approx10^5$ tokenli LLM lug‘ati uchun bu har bir pozitsiyada $10^5$ va $10^{10}$ son orasidagi farq. Kross-entropiya bilan juftlikda esa yanada oddiy: $\partial L/\partial z=s-y$ (keltirib chiqarish — <a href='../cross-entropy/'>kross-entropiya</a> sahifasida)."),
    ]),
    dict(id="surface", title="3D manzara: logitlar tekisligi ustidagi softmax", blocks=[
        ("p", r"$z_3=0$ ni qayd etamiz — bu umumiylikni yo‘qotmaydi, chunki siljish bilan istalgan logitni nolga aylantirish mumkin, — va $s_1$ ni ikki o‘zgaruvchi $z_1$ va $z_2$ ning funksiyasi sifatida chizamiz. «Rampa» hosil bo‘ladi: $z_1$ ham $z_2$ dan, ham noldan katta bo‘lgan joyda sirt 1 ga yaqin, birinchi sinf yutqazgan joyda esa 0 ga yaqin. Chegara bo‘ylab u sigmoida bo‘yicha ko‘tariladi — bu «bittasi hammaga qarshi» formulasining amaldagi ko‘rinishi."),
        ("viz", "softmax-surface", {"z": [2, 1]}, r"<b>5-rasm.</b> Chapda — 3D’da $s_k(z_1,z_2,0)$ (sirtni aylantirish mumkin), qora nuqta — $s_1\approx0{,}665$ bo‘lgan $z=(2;\,1;\,0)$. O‘ngda — logitlar tekisligi: bo‘yoq g‘olib sinf va ishonchni ko‘rsatadi, chiziqlar — tanlangan funksiyaning $0{,}1$, $0{,}5$, $0{,}9$ sathlari (hosila uchun — $0{,}05$, $0{,}15$, $0{,}24$). Nuqtani surish mumkin. $\partial s_1/\partial z_1$ ga o‘ting: bu $s_1=0{,}5$ chiziq bo‘ylab balandligi $0{,}25$ bo‘lgan qir."),
        ("p", r"Yuqoridan ko‘rinish logitlar tekisligini uchta sohaga bo‘ladi. Chegaralar — teng logitlar to‘plamlari: $z_1=z_2\ge0$ nur 1- va 2-sinflarni, $z_1=0$, $z_2\le0$ nur 1- va 3-sinflarni, $z_2=0$, $z_1\le0$ nur 2- va 3-sinflarni ajratadi. Uchala nur ham $s=(\tfrac13;\,\tfrac13;\,\tfrac13)$ bo‘lgan koordinatalar boshidan chiqadi."),
        ("callout", "note", "Gradiyent qayerda oqadi", r"$\partial s_1/\partial z_1=s_1(1-s_1)$ sirt «o‘z» va «begona» sohalar ichkarisida deyarli tekis va deyarli nol. Softmax orqali gradiyent faqat model ikkilanayotgan joyda — chegaralar yaqinida oqadi."),
    ]),
    dict(id="lse", title="Log-sum-exp: silliq maksimum", blocks=[
        ("p", r"Softmax’ning «boshlang‘ich funksiyasi» bor — log-sum-exp funksiyasi:"),
        ("eq", r"\operatorname{LSE}(z)=\ln\sum_{j=1}^{K}e^{z_j},\qquad\frac{\partial\operatorname{LSE}}{\partial z_i}=\frac{e^{z_i}}{\sum_j e^{z_j}}=s_i,\qquad\nabla\operatorname{LSE}(z)=\operatorname{softmax}(z)"),
        ("p", r"LSE — silliq maksimum: eng katta eksponenta yig‘indida ustunlik qiladi va logarifm deyarli uning ko‘rsatkichini qaytaradi. Aniqroq,"),
        ("eq", r"\max_j z_j\;\le\;\operatorname{LSE}(z)\;\le\;\max_j z_j+\ln K"),
        ("p", r"Chap tengsizlik o‘rinli, chunki yig‘indi eng katta qo‘shiluvchisidan kichik emas, o‘ng tengsizlik — chunki $K$ ta qo‘shiluvchining har biri eng kattasidan oshmaydi. $(2;\,1;\,0)$ uchun: $\operatorname{LSE}=\ln11{,}107\approx2{,}408$ — $2$ va $2+\ln3\approx3{,}099$ orasida. Harorat bilan $\operatorname{LSE}_T(z)=T\ln\sum_j e^{z_j/T}$ da oraliq $T\ln K$ gacha qisqaradi: $T\to0$ da LSE oddiy maksimumga, uning gradiyenti $\operatorname{softmax}(z/T)$ esa argmax ning one-hot vektoriga aylanadi."),
        ("viz", "softmax-lse", {"T": 1, "x": 1}, r"<b>6-rasm.</b> Yuqorida — $\operatorname{LSE}_T(x,0)=T\ln(e^{x/T}+1)$ va $\max(x,0)$; oraliq $T\ln2$ dan oshmaydi va $x=0$ da eng katta. $T=1$, $x=1$ da: $\operatorname{LSE}\approx1{,}3133$, oraliq $0{,}3133$. Pastda — $x$ bo‘yicha hosila: bu $\sigma(x/T)$, ya’ni $\operatorname{softmax}(x/T,\,0)$ ning birinchi komponentasi, silliq pog‘ona. $T$ ni kamaytiring — LSE siniq chiziqqa, softmax esa pog‘onaga yopishadi."),
        ("deep", "LSE va kross-entropiyaning qavariqligi", [
            ("p", r"LSE gessiani — softmax’ning hosilasi, ya’ni o‘sha Yakobi matritsasi: $\nabla^2\operatorname{LSE}=\operatorname{diag}(s)-ss^\top$. U nomanfiy aniqlangan, demak LSE — qavariq funksiya. Bundan kross-entropiyaning logitlar bo‘yicha qavariqligi kelib chiqadi: $-\ln s_y=\operatorname{LSE}(z)-z_y$ — qavariq funksiyadan chiziqli funksiya ayirmasi."),
        ]),
        ("callout", "key", "Bog‘lashga arziydigan uchta formula", r"$\operatorname{softmax}=\nabla\operatorname{LSE}$; $\ln s_i=z_i-\operatorname{LSE}(z)$ (log-softmax); $\mathrm{CE}=\operatorname{LSE}(z)-z_y$. Qo‘llanmadagi misol uchun: $2{,}408-2=0{,}408$. $K=2$ va $z=(x;\,0)$ da esa LSE softplus $\ln(1+e^{x})$ ga — <a href='../relu/'>ReLU</a> ning silliq ko‘rinishiga aylanadi."),
    ]),
    dict(id="training", title="O‘qitishda softmax", blocks=[
        ("p", r"Softmax’li eng oddiy model — ko‘p sinfli logistik (softmax-) regressiya: $K$ ta chiziqli funksiya logitlarni, softmax ehtimolliklarni beradi, yo‘qotish esa — <a href='../cross-entropy/'>kross-entropiya</a>:"),
        ("eq", r"s=\operatorname{softmax}(Wx+b),\qquad L=-\ln s_y,\qquad\frac{\partial L}{\partial W}=(s-y)\,x^{\top},\qquad\frac{\partial L}{\partial b}=s-y"),
        ("p", r"Bu yerda $y$ — to‘g‘ri sinfning one-hot vektori. Butun Yakobi matritsasi logarifm bilan juftlikda «bashorat − haqiqat» ayirmasiga qisqardi."),
        ("viz", "softmax-regression", {}, r"<b>7-rasm.</b> Har biri 30 nuqtadan iborat uchta sinf. Model $W=0$, $b=0$ dan boshlaydi: barcha ehtimolliklar $\tfrac13$, $\mathrm{CE}=\ln3\approx1{,}099$, aniqlik $33{,}3\%$. «Boshlash» ni bosing: butun to‘plam bo‘yicha $0{,}15$ qadamli gradiyentli tushish. Birinchi qadamdan keyinoq aniqlik $94{,}4\%$, 200 qadamdan keyin $\mathrm{CE}\approx0{,}181$ va aniqlik $95{,}6\%$. Bo‘yoq yorqinligi — model ishonchi; istalgan nuqtadagi ehtimolliklarni ko‘rish uchun kursorni olib boring."),
        ("callout", "note", "Chegaralar — to‘g‘ri chiziqlar", r"$i$ va $j$ sinflar orasidagi chegara — $z_i=z_j$ bo‘lgan to‘plam, ya’ni $(w_i-w_j)^\top x+b_i-b_j=0$: to‘g‘ri chiziq (umumiy holda gipertekislik). Softmax modelni nochiziqli qilmaydi — u faqat ballarni ehtimolliklarga aylantiradi. Egri chegaralar logitlarni neyron tarmoq hisoblaganda paydo bo‘ladi."),
        ("h3", "Transformer ichidagi softmax: attention"),
        ("eq", r"\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\Bigl(\frac{QK^{\top}}{\sqrt{d}}\Bigr)V"),
        ("p", r"$\operatorname{softmax}(\cdot)$ ning har bir satri — bitta tokenning diqqati ketma-ketlik tokenlari (o‘zi ham) bo‘yicha taqsimoti, vaznlar yig‘indisi 1. $\sqrt d$ ga bo‘lish — bu harorat: komponentalari mustaqil, o‘rtachasi nol va dispersiyasi bir bo‘lgan $d$ o‘lchovli vektorlarning skalyar ko‘paytmasi dispersiyasi $d$ ga teng. Masshtablashsiz attention logitlari katta bo‘ladi, softmax deyarli one-hot gacha to‘yinadi, Yakobi matritsasi — u bilan birga gradiyentlar ham — deyarli nolga aylanadi."),
        ("h3", "Matn generatsiyasidagi harorat"),
        ("p", r"Til modeli keyingi tokenni $\operatorname{softmax}(z/T)$ dan tanlaydi. $T\to0$ da (ochko‘z tanlov) eng ehtimolli token olinadi, $T&lt;1$ da matn oldindan aytib bo‘ladiganroq, $T&gt;1$ da — xilma-xilroq va xavfliroq. $T&gt;1$ harorat bilimlar distillyatsiyasida ham ishlaydi (Xinton va boshq., 2015): o‘qituvchining «yumshoq» ehtimolliklari one-hot belgilardan ko‘ra ko‘proq axborot tashiydi."),
        ("callout", "history", "Nom qayerdan kelgan", r"Formula statistik fizikadan kelgan: Bolsman — Gibbs taqsimoti $p_i\propto e^{-E_i/(kT)}$ $T$ haroratda $E_i$ energiyali holat ehtimolligini beradi; logit minus ishorali energiya rolini o‘ynaydi. «Softmax» so‘zini 1990 yilda Jon Braydl tarmoq chiqishlarining ehtimoliy talqinini tasvirlab taklif qilgan. Ekonometrikada xuddi shu model multinomial logit deb ataladi."),
    ]),
    dict(id="code", title="Kodda: barqarorlik, log-softmax va PyTorch", blocks=[
        ("p", r"Sodda formula katta logitlarda buziladi: $e^{1000}\approx2\cdot10^{434}$ na float32 ga, na float64 ga sig‘adi va cheksizlikka aylanadi, so‘ng $\infty/\infty=\text{NaN}$ chiqadi. float32 da (va daraja diapazoni xuddi shunday bo‘lgan bfloat16 da) chegara yaqinroq: $e^{x}$ allaqachon $x&gt;88{,}72$ da to‘lib ketadi (eng katta float32 soni $\approx3{,}4\cdot10^{38}$). Juda manfiy logitlarda muammo teskari: eksponentalar nolga aylanadi va $0/0$ chiqadi."),
        ("viz", "softmax-overflow", {"c": 0}, r"<b>8-rasm.</b> $c$ $-800$ dan $800$ gacha bo‘lganda $(2+c;\,1+c;\,c)$ logitlar; to‘g‘ri javob doim $(0{,}665;\,0{,}245;\,0{,}090)$. float32 da sodda formula faqat $-99\le c\le86$ da to‘g‘ri: $c=87$ da $e^{89}$ soni float32 ga sig‘maydi va NaN chiqadi; $c\le-106$ da barcha eksponentalar nolga teng, $0/0$; ular orasida esa subnormal sonlar aniqlikni yo‘qotadi — $c=-105$ da ishonchli, lekin yolg‘on $(1;\,0;\,0)$ javob chiqadi. float64 da zaxira kattaroq ($-741\le c\le707$), lekin chegara bor. Maksimum ayirilganda javob hamma joyda to‘g‘ri."),
        ("p", r"Davo — siljishga invariantlik: $m=\max_j z_j$ ni ayiramiz. Eng katta ko‘rsatkich 0 ga, $e^0=1$ ga teng bo‘ladi, maxraj 1 va $K$ orasida yotadi — na to‘lib ketish, na nolga bo‘lish:"),
        ("eq", r"s_i=\frac{e^{z_i-m}}{\sum_j e^{z_j-m}},\qquad\ln s_i=(z_i-m)-\ln\sum_j e^{z_j-m}"),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Qoida", r"Agar keyin logarifm kelsa, $\ln(\operatorname{softmax}(z))$ ni ikki qadamda hisoblamang: kichik ehtimollik 0 ga yaxlitlanadi va $-\infty$ chiqadi. <code>log_softmax</code> dan yoki to‘g‘ridan-to‘g‘ri logitlardagi yo‘qotishdan foydalaning: PyTorch’da <code>F.cross_entropy</code> / <code>nn.CrossEntropyLoss</code>, Keras’da <code>from_logits=True</code>."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            r"<b><code>nn.CrossEntropyLoss</code> dan oldin softmax</b>. Bu yo‘qotish logitlarni kutadi va log-softmax’ni o‘zi qo‘llaydi. Ikki karra softmax ehtimolliklarni siqadi: uch sinf uchun ikkinchi softmax $e/(e+2)\approx0{,}576$ dan ko‘p bermaydi, yo‘qotish $0{,}551$ dan pastga tushmaydi, gradiyentlar buziladi.",
            r"<b>Noto‘g‘ri o‘q</b>. $(N,K)$ shaklli batch uchun misollar bo‘yicha (<code>dim=0</code>) emas, sinflar bo‘yicha (<code>dim=-1</code>) normallash kerak. Istisno chiqmaydi — model shunchaki bema’ni narsani o‘rganadi.",
            r"<b>Sodda eksponenta</b> maksimumni ayirmasdan — katta logitlarda NaN, ayniqsa aralash aniqlikda: float16 da $e^{x}$ allaqachon $x&gt;11{,}09$ da to‘lib ketadi.",
            r"<b>Multi-label uchun softmax</b>. Agar obyektda bir vaqtda bir nechta belgi bo‘lishi mumkin bo‘lsa (rasmda mushuk <i>va</i> it), sinflar raqobatlashmaydi — har bir chiqishda sigmoida va <a href='../bce/'>BCE</a> kerak.",
            r"<b>Softmax ehtimolligini kafolat deb bilish</b>. $s_{\max}=0{,}99$ «99% hollarda haq» degani emas: chuqur tarmoqlar ko‘pincha o‘ziga haddan tashqari ishonadi. Kalibrlash — alohida vazifa; eng oddiy usul — temperature scaling, validatsiyada bitta $T$ ni tanlash.",
            r"<b>Turli misollar logitlarini solishtirish</b>. Logitlar siljish aniqligida aniqlangan, shuning uchun «bir misolda logit 5, boshqasida 3 dan katta» hech narsani anglatmaydi. Ehtimolliklarni yoki bitta misol ichidagi logitlar ayirmalarini solishtiring.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘liqlik", blocks=[
        ("ul", [
            r"<a href='../sigmoid/'>Sigmoida</a>: $\operatorname{softmax}(z_1,z_2)_1=\sigma(z_1-z_2)$, Yakobi matritsasining $s_i(1-s_i)$ diagonali esa sigmoidaning hosilasi.",
            r"<a href='../cross-entropy/'>Kross-entropiya</a>: softmax’ning tabiiy jufti; birgalikda $s-y$ gradiyentni beradi, $\mathrm{CE}=\operatorname{LSE}(z)-z_y$.",
            r"<a href='../bce/'>BCE</a>: ikki sinf uchun kross-entropiyaning xususiy holi, bunda softmax sigmoidaga keladi.",
            r"<a href='../focal/'>Focal Loss</a>: $-\ln p_t$ ni $(1-p_t)^\gamma$ ga ko‘paytiradi, bu yerda $p_t$ — to‘g‘ri sinfning softmax-ehtimolligi.",
            r"<a href='../relu/'>ReLU</a>: softplus $\ln(1+e^{x})=\operatorname{LSE}(x,0)$ — $\max(x,0)$ ning silliq varianti.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, r"1) $s_i=e^{z_i}/\sum_je^{z_j}$ istalgan logitlarni $K$ ta sinf bo‘yicha taqsimotga aylantiradi va tartibni saqlaydi. 2) Faqat logitlar ayirmalari muhim: $s_i/s_j=e^{z_i-z_j}$, siljish hech narsani o‘zgartirmaydi — maksimumni ayiradigan barqaror formula shundan. 3) Harorat keskinlikni boshqaradi: $T\to0$ — argmax, $T\to\infty$ — tekis taqsimot. 4) $\operatorname{diag}(s)-ss^\top$ Yakobi matritsasi simmetrik, xos va ishonch oshganda so‘nadi; teskari o‘tish $O(K)$ turadi. 5) Softmax — LSE silliq maksimumining gradiyenti, kross-entropiya bilan juftlikda esa $s-y$ gradiyentni beradi."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q=r"$(2;\,1;\,0)$ logitlar $s\approx(0{,}665;\,0{,}245;\,0{,}090)$ ni beradi. $(102;\,101;\,100)$ nima beradi?", options=[r"$(0{,}665;\,0{,}245;\,0{,}090)$", r"Deyarli $(1;\,0;\,0)$", r"$(\tfrac13;\,\tfrac13;\,\tfrac13)$", "Javob yo‘q: to‘lib ketish"], answer=0,
                 explain=r"Umumiy $100$ o‘zgarmas qisqaradi: softmax faqat ayirmalarga bog‘liq. (float32 dagi sodda kod bu yerda haqiqatan to‘lib ketadi — shuning uchun maksimum ayiriladi.)"),
            dict(q=r"$T\to0$ da $\operatorname{softmax}(z/T)$ bilan nima bo‘ladi?", options=["Tekis taqsimotga intiladi", "O‘zgarmaydi", "Eng katta logitning one-hot vektoriga intiladi", "Barcha ehtimolliklar 0 ga intiladi"], answer=2,
                 explain=r"Logitlar ayirmalari kichik $T$ ga bo‘linib o‘sadi, butun massa eng katta logitga o‘tadi (agar u yagona bo‘lsa)."),
            dict(q=r"$\operatorname{softmax}(z_1,z_2)_1$ nimaga teng?", options=[r"$\sigma(z_1)$", r"$\sigma(z_1-z_2)$", r"$\sigma(z_1+z_2)$", r"$z_1/(z_1+z_2)$"], answer=1,
                 explain=r"$e^{z_1}/(e^{z_1}+e^{z_2})$ ning surat va maxrajini $e^{z_1}$ ga bo‘ling: $1/(1+e^{-(z_1-z_2)})$ chiqadi."),
            dict(q="Softmax Yakobi matritsasining istalgan ustuni elementlari yig‘indisi nimaga teng?", options=["1", r"$s_j$", r"$\tfrac14$", "0"], answer=3,
                 explain=r"$\sum_i\partial s_i/\partial z_j=\partial\bigl(\sum_i s_i\bigr)/\partial z_j=\partial1/\partial z_j=0$."),
            dict(q=r"Barqaror softmax’da nima uchun $\max_j z_j$ ayiriladi?", options=["Eksponenta to‘lib ketmasligi uchun; natija o‘zgarmaydi", "Taqsimotni keskinroq qilish uchun", "Yig‘indini 1 ga tenglash uchun", "O‘qitishni tezlashtirish uchun"], answer=0,
                 explain=r"Ayirgandan keyin eng katta ko‘rsatkich 0, maxraj 1 va $K$ orasida yotadi, siljishga invariantlik tufayli esa javob o‘sha."),
        ]),
    ]),
],
}

# Fill in the shared pieces (table header and rows, code listings) per language.
for _lang, _secs in SECTIONS.items():
    for _sec in _secs:
        for _i, _b in enumerate(_sec["blocks"]):
            if _b[0] == "table" and _b[2] == "TABLE":
                _sec["blocks"][_i] = (_b[0], _heads(_lang), _table(_lang), _b[3])
            elif _b[0] == "code" and _b[2] in ("CODE_NUMPY", "CODE_TORCH"):
                _sec["blocks"][_i] = (_b[0], _b[1], _code(CODE_NUMPY if _b[2] == "CODE_NUMPY" else CODE_TORCH, _lang))
