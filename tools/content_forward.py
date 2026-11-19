"""Article "The forward pass formula" in three languages.

Built by tools/build.py (long_article) from the same blocks as the neuron article; widgets: assets/js/forward.js.
Every number in the text is checked by check_numbers(): python3 tools/content_forward.py
"""

SLUG = "forward-pass"
DATE = "2026-11-18"
MINUTES = 45

HERO = r"\mathbf{a}^{(0)}=\mathbf{x},\qquad \mathbf{z}^{(l)}=W^{(l)}\mathbf{a}^{(l-1)}+\mathbf{b}^{(l)},\qquad \mathbf{a}^{(l)}=f^{(l)}\big(\mathbf{z}^{(l)}\big),\qquad \hat{\mathbf{y}}=\mathbf{a}^{(L)}"

TITLE = {
    "ru": "Формула Forward Pass: как сеть превращает вход в ответ",
    "en": "The forward pass formula: how a network turns an input into an answer",
    "uz": "Forward Pass formulasi: tarmoq kirishni javobga qanday aylantiradi",
}
EXCERPT = {
    "ru": "Прямой проход по косточкам: z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾ и a⁽ˡ⁾ = f(z⁽ˡ⁾) слой за слоем — каждая буква, размерности, геометрия, пакеты, стоимость и код. Анимации, интерактивная сеть и 8 разобранных примеров.",
    "en": "The forward pass bone by bone: z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾ and a⁽ˡ⁾ = f(z⁽ˡ⁾) layer by layer — every symbol, shapes, geometry, batches, cost and code. Animations, an interactive network and 8 worked examples.",
    "uz": "To‘g‘ri o‘tish mayda detallarigacha: z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾ va a⁽ˡ⁾ = f(z⁽ˡ⁾) qatlamma-qatlam — har bir harf, o‘lchamlar, geometriya, paketlar, narx va kod. Animatsiyalar, interaktiv tarmoq va 8 ta yechilgan misol.",
}
DEK = {
    "ru": "Прямой проход — это то, что сеть делает каждый раз, когда отвечает: вход проходит слой за слоем, и в каждом слое повторяются одни и те же два действия — линейное преобразование и активация. Разбираем формулу до последнего индекса, считаем её руками на маленькой сети, смотрим, как слои сгибают пространство, и пишем код.",
    "en": "The forward pass is what a network does every time it answers: the input goes through layer after layer, and every layer repeats the same two actions — a linear map and an activation. We take the formula apart down to the last index, compute it by hand on a small network, watch how layers bend space, and write the code.",
    "uz": "To‘g‘ri o‘tish — tarmoq har safar javob berganda bajaradigan ish: kirish qatlamma-qatlam o‘tadi va har bir qatlamda ikki amal takrorlanadi — chiziqli almashtirish va aktivatsiya. Formulani oxirgi indeksigacha tahlil qilamiz, kichik tarmoqda qo‘lda hisoblaymiz, qatlamlar fazoni qanday egishini ko‘ramiz va kod yozamiz.",
}
DESCRIPTION = {
    "ru": "Формула прямого прохода нейросети z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾, a⁽ˡ⁾ = f(z⁽ˡ⁾) по шагам: обозначения, расчёт на числах, размерности, пакеты, геометрия слоёв, стоимость, код. С интерактивными рисунками.",
    "en": "The neural network forward pass z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾, a⁽ˡ⁾ = f(z⁽ˡ⁾) step by step: notation, worked numbers, shapes, batches, the geometry of layers, cost, code. With interactive figures.",
    "uz": "Neyron tarmoqning to‘g‘ri o‘tishi z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾, a⁽ˡ⁾ = f(z⁽ˡ⁾) qadamma-qadam: belgilar, sonli hisob, o‘lchamlar, paketlar, qatlamlar geometriyasi, narx, kod. Interaktiv rasmlar bilan.",
}
TAGS = {
    "ru": ["Нейросети", "Линейная алгебра", "Основы ML"],
    "en": ["Neural networks", "Linear algebra", "ML basics"],
    "uz": ["Neyron tarmoqlar", "Chiziqli algebra", "ML asoslari"],
}
RELATED = {
    "ru": [("../chain-rule/", "Цепное правило", "Следующая статья"), ("../neuron/", "Формула одного нейрона", "Предыдущая статья"), ("../materials/ml-formulas/", "Шпаргалка формул нейросетей", "Материал")],
    "en": [("../chain-rule/", "The chain rule", "Next article"), ("../neuron/", "The formula of a single neuron", "Previous article"), ("../materials/ml-formulas/", "A cheat sheet of neural network formulas", "Material")],
    "uz": [("../chain-rule/", "Zanjir qoidasi", "Keyingi maqola"), ("../neuron/", "Bitta neyron formulasi", "Oldingi maqola"), ("../materials/ml-formulas/", "Neyron tarmoq formulalari qo‘llanmasi", "Material")],
}

# The running example: a 2–3–2–1 network, ReLU in the hidden layers, the sigmoid at the output.
NET = dict(
    x=[1, 2],
    W=[[[1, -1], [0.5, 1], [-1, 2]], [[1, 0.5, -0.5], [-1, 1, 0.5]], [[2, -0.5]]],
    b=[[0.5, -1, 0], [0, 0.5], [1]],
    f=["relu", "relu", "sigmoid"],
)

VIZ = {
    "flow": dict(net=NET),
    "matvec": dict(net=NET),
    "shapes": dict(sizes=[2, 3, 2, 1], presets=[[2, 3, 2, 1], [784, 128, 64, 10], [3, 3, 1], [2, 100, 1], [2, 10, 10, 10, 1]]),
    "space": dict(preset="fold"),
    "play": dict(net=NET),
}

CODE_NUMPY = {
    "ru": '''import numpy as np

relu = lambda z: np.maximum(0, z)
sigmoid = lambda z: 1 / (1 + np.exp(-z))

# Сеть 2–3–2–1: список слоёв (W, b, f)
layers = [
    (np.array([[1, -1], [0.5, 1], [-1, 2]]),       np.array([0.5, -1, 0]), relu),
    (np.array([[1, 0.5, -0.5], [-1, 1, 0.5]]),     np.array([0.0, 0.5]),   relu),
    (np.array([[2, -0.5]]),                        np.array([1.0]),        sigmoid),
]

def forward(x, layers):
    a = x                                  # a⁽⁰⁾ = x
    cache = []                             # z и a каждого слоя пригодятся обратному проходу
    for W, b, f in layers:
        z = W @ a + b                      # z⁽ˡ⁾ = W⁽ˡ⁾ a⁽ˡ⁻¹⁾ + b⁽ˡ⁾
        a = f(z)                           # a⁽ˡ⁾ = f⁽ˡ⁾(z⁽ˡ⁾)
        cache.append((z, a))
    return a, cache

y_hat, cache = forward(np.array([1.0, 2.0]), layers)
for l, (z, a) in enumerate(cache, 1):
    print(f"слой {l}: z = {z}, a = {np.round(a, 4)}")
# слой 1: z = [-0.5  1.5  3. ], a = [0.  1.5 3. ]
# слой 2: z = [-0.75  3.5 ], a = [0.  3.5]
# слой 3: z = [-0.75], a = [0.3208]

# Пакет: строки X — объекты; та же формула, только X @ W.T
X = np.array([[1, 2], [0, 0], [2, -1]], dtype=float)
A = X
for W, b, f in layers:
    A = f(A @ W.T + b)                     # Z = X Wᵀ + 1bᵀ
print(np.round(A.ravel(), 4))              # [0.3208 0.8808 0.9997]''',
}
CODE_NUMPY["en"] = (CODE_NUMPY["ru"].replace("# Сеть 2–3–2–1: список слоёв (W, b, f)", "# The 2–3–2–1 network: a list of layers (W, b, f)")
                    .replace("# z и a каждого слоя пригодятся обратному проходу", "# z and a of every layer are needed by the backward pass")
                    .replace('print(f"слой {l}:', 'print(f"layer {l}:').replace("# слой ", "# layer ")
                    .replace("# Пакет: строки X — объекты; та же формула, только X @ W.T", "# A batch: the rows of X are objects; the same formula, only X @ W.T"))
CODE_NUMPY["uz"] = (CODE_NUMPY["ru"].replace("# Сеть 2–3–2–1: список слоёв (W, b, f)", "# 2–3–2–1 tarmog‘i: qatlamlar ro‘yxati (W, b, f)")
                    .replace("# z и a каждого слоя пригодятся обратному проходу", "# har bir qatlamning z va a qiymatlari teskari o‘tishga kerak")
                    .replace('print(f"слой {l}:', 'print(f"qatlam {l}:').replace("# слой ", "# qatlam ")
                    .replace("# Пакет: строки X — объекты; та же формула, только X @ W.T", "# Paket: X satrlari — obyektlar; o‘sha formula, faqat X @ W.T"))

CODE_TORCH = {
    "ru": '''import torch
import torch.nn as nn

net = nn.Sequential(
    nn.Linear(2, 3), nn.ReLU(),            # слой 1: W⁽¹⁾ — (3, 2), b⁽¹⁾ — (3,)
    nn.Linear(3, 2), nn.ReLU(),            # слой 2: W⁽²⁾ — (2, 3)
    nn.Linear(2, 1), nn.Sigmoid(),         # слой 3: W⁽³⁾ — (1, 2)
)
with torch.no_grad():                      # те же веса, что в статье
    net[0].weight[:] = torch.tensor([[1., -1.], [0.5, 1.], [-1., 2.]]); net[0].bias[:] = torch.tensor([0.5, -1., 0.])
    net[2].weight[:] = torch.tensor([[1., 0.5, -0.5], [-1., 1., 0.5]]); net[2].bias[:] = torch.tensor([0., 0.5])
    net[4].weight[:] = torch.tensor([[2., -0.5]]);                       net[4].bias[:] = torch.tensor([1.])

X = torch.tensor([[1., 2.], [0., 0.], [2., -1.]])
print(net(X).squeeze())                    # ≈ [0.3208, 0.8808, 0.9997]
print(sum(p.numel() for p in net.parameters()))   # 20''',
}
CODE_TORCH["en"] = (CODE_TORCH["ru"].replace("# слой 1:", "# layer 1:").replace("# слой 2:", "# layer 2:").replace("# слой 3:", "# layer 3:")
                    .replace("# те же веса, что в статье", "# the same weights as in the article"))
CODE_TORCH["uz"] = (CODE_TORCH["ru"].replace("# слой 1:", "# 1-qatlam:").replace("# слой 2:", "# 2-qatlam:").replace("# слой 3:", "# 3-qatlam:")
                    .replace("# те же веса, что в статье", "# maqoladagi vaznlarning o‘zi"))


RU = [
    dict(id="idea", title="Что такое прямой проход", blocks=[
        ("p", r"В <a href='../neuron/'>статье об одном нейроне</a> мы разобрали формулу $a = f(\mathbf{w}^{\top}\mathbf{x} + b)$. Настоящая сеть — это много таких нейронов, сложенных в слои: выходы одного слоя становятся входами следующего. <b>Прямой проход</b> (forward pass) — это вычисление ответа сети: вход идёт слева направо, слой за слоем, до последнего слоя."),
        ("p", r"Вся процедура записывается тремя строками:"),
        ("eq", r"\mathbf{a}^{(0)} = \mathbf{x}"),
        ("eq", r"\mathbf{z}^{(l)} = W^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}, \qquad \mathbf{a}^{(l)} = f^{(l)}\big(\mathbf{z}^{(l)}\big), \qquad l = 1, 2, \dots, L"),
        ("eq", r"\hat{\mathbf{y}} = \mathbf{a}^{(L)}"),
        ("p", r"Прочитаем как инструкцию: положи вход в «нулевой слой»; в каждом слое умножь то, что пришло, на матрицу весов, прибавь смещения и пропусти через функцию активации; то, что вышло из последнего слоя, и есть ответ. Если раскрыть цикл, получится одна длинная вложенная формула:"),
        ("eq", r"\hat{\mathbf{y}} = f^{(L)}\Big(W^{(L)}\,f^{(L-1)}\big(\cdots f^{(1)}\big(W^{(1)}\mathbf{x} + \mathbf{b}^{(1)}\big)\cdots\big) + \mathbf{b}^{(L)}\Big)"),
        ("viz", "fp-flow", VIZ["flow"], r"<b>Рисунок 1.</b> Прямой проход в сети 2–3–2–1. Нажмите «Шаг» или «Пуск»: сигнал проходит слой за слоем, в каждом нейроне сначала появляется $z$, затем $a = f(z)$. Синие связи — положительные веса, красные — отрицательные, толщина — модуль веса. Двигайте ползунки входа: ответ $\hat y$ пересчитывается сразу."),
        ("callout", "intuition", "Аналогия", r"Конвейер на заводе. Сырьё (вход $\mathbf{x}$) проходит через станки (слои). Каждый станок делает одно и то же: смешивает поступившие детали в нужных пропорциях (матрица $W$), добавляет свою добавку (смещение $\mathbf{b}$) и обрабатывает результат (активация $f$). Ни один станок не знает о конечном продукте — он видит только то, что пришло от предыдущего. Продукт на выходе последнего станка — ответ сети."),
        ("callout", "key", "Главное", r"Прямой проход не обучает сеть и не меняет её веса — он только вычисляет ответ при текущих весах. Обучение начинается потом: ответ сравнивают с правильным (функция потерь), и обратный проход вычисляет, как поправить веса."),
    ]),

    dict(id="anatomy", title="Формула по косточкам: каждый символ", blocks=[
        ("p", r"Все обозначения прямого прохода с их размерами. Число нейронов в слое $l$ обозначим $n_l$; $n_0$ — число входов."),
        ("symbols", [
            (r"l", r"<b>номер слоя</b>: $l = 1, \dots, L$; верхний индекс в скобках $^{(l)}$ — «принадлежит слою $l$», а не степень;"),
            (r"L", r"<b>число слоёв с весами</b> (глубина сети); входной «слой» $0$ весов не имеет;"),
            (r"\mathbf{a}^{(l-1)}", r"<b>вход слоя</b> $l$ — выход предыдущего слоя, вектор длины $n_{l-1}$; $\mathbf{a}^{(0)} = \mathbf{x}$;"),
            (r"W^{(l)}", r"<b>матрица весов</b> слоя: $n_l$ строк и $n_{l-1}$ столбцов; строка $j$ — веса нейрона $j$;"),
            (r"W^{(l)}_{jk}", r"<b>один вес</b>: от нейрона $k$ слоя $l-1$ к нейрону $j$ слоя $l$ (сначала «куда», потом «откуда»);"),
            (r"\mathbf{b}^{(l)}", r"<b>вектор смещений</b> длины $n_l$ — по одному на нейрон;"),
            (r"\mathbf{z}^{(l)}", r"<b>предактивации</b> слоя, вектор длины $n_l$: взвешенные суммы всех его нейронов;"),
            (r"f^{(l)}", r"<b>функция активации</b> слоя; применяется к каждой координате отдельно;"),
            (r"\mathbf{a}^{(l)}", r"<b>выход слоя</b> (активации), вектор длины $n_l$;"),
            (r"\hat{\mathbf{y}}", r"<b>ответ сети</b>: выход последнего слоя $\mathbf{a}^{(L)}$."),
        ]),
        ("h3", "Один слой — это много нейронов сразу"),
        ("p", r"Распишем первую строку формулы по координатам. Нейрон $j$ слоя $l$ считает ровно ту же формулу, что и одиночный нейрон: взвешенную сумму входов плюс своё смещение."),
        ("eq", r"z^{(l)}_j = \sum_{k=1}^{n_{l-1}} W^{(l)}_{jk}\,a^{(l-1)}_k + b^{(l)}_j, \qquad a^{(l)}_j = f^{(l)}\big(z^{(l)}_j\big), \qquad j = 1, \dots, n_l"),
        ("p", r"Матричная запись $W^{(l)}\mathbf{a}^{(l-1)}$ — просто способ посчитать все $n_l$ таких сумм одним действием: $j$-я строка матрицы, умноженная на вектор входов, даёт $z_j$. Поэтому формула прямого прохода — это формула одного нейрона, применённая ко всем нейронам слоя и повторённая для всех слоёв."),
        ("h3", "Размеры в нашем примере"),
        ("p", r"Весь дальнейший текст опирается на одну сеть: 2 входа, скрытые слои из 3 и 2 нейронов с ReLU, один выходной нейрон с сигмоидой (сеть 2–3–2–1)."),
        ("table", ["Слой $l$", r"$n_{l-1} \to n_l$", r"$W^{(l)}$", r"$\mathbf{b}^{(l)}$", r"$f^{(l)}$", "Параметров"], [
            ["1", "2 → 3", "3 × 2", "3", "ReLU", "3·2 + 3 = 9"],
            ["2", "3 → 2", "2 × 3", "2", "ReLU", "2·3 + 2 = 8"],
            ["3", "2 → 1", "1 × 2", "1", "сигмоида", "1·2 + 1 = 3"],
            ["<b>всего</b>", "", "", "", "", "<b>20</b>"],
        ], {"num": [0]}),
        ("callout", "key", "Правило подсчёта", r"У слоя $n_{l-1}\to n_l$ ровно $n_l\,(n_{l-1} + 1)$ параметров: $n_l n_{l-1}$ весов и $n_l$ смещений. У всей сети — сумма по слоям."),
    ]),

    dict(id="numbers", title="Прямой проход на числах, шаг за шагом", blocks=[
        ("p", r"Вход $\mathbf{x} = (1;\ 2)$. Веса и смещения:"),
        ("eq", r"W^{(1)} = \begin{pmatrix} 1 & -1\\ 0{,}5 & 1\\ -1 & 2 \end{pmatrix},\ \mathbf{b}^{(1)} = \begin{pmatrix} 0{,}5\\ -1\\ 0 \end{pmatrix};\quad W^{(2)} = \begin{pmatrix} 1 & 0{,}5 & -0{,}5\\ -1 & 1 & 0{,}5 \end{pmatrix},\ \mathbf{b}^{(2)} = \begin{pmatrix} 0\\ 0{,}5 \end{pmatrix};\quad W^{(3)} = \begin{pmatrix} 2 & -0{,}5 \end{pmatrix},\ b^{(3)} = 1"),
        ("h3", "Слой 1: из двух чисел — три"),
        ("eq", r"\mathbf{z}^{(1)} = \begin{pmatrix} 1\cdot1 + (-1)\cdot2 + 0{,}5\\ 0{,}5\cdot1 + 1\cdot2 - 1\\ (-1)\cdot1 + 2\cdot2 + 0 \end{pmatrix} = \begin{pmatrix} -0{,}5\\ 1{,}5\\ 3 \end{pmatrix}, \qquad \mathbf{a}^{(1)} = \mathrm{ReLU}\big(\mathbf{z}^{(1)}\big) = \begin{pmatrix} 0\\ 1{,}5\\ 3 \end{pmatrix}"),
        ("p", r"Первый нейрон получил отрицательную сумму, и ReLU его «выключила»: дальше по сети от него пойдёт ноль."),
        ("h3", "Слой 2: из трёх чисел — два"),
        ("eq", r"\mathbf{z}^{(2)} = \begin{pmatrix} 1\cdot0 + 0{,}5\cdot1{,}5 - 0{,}5\cdot3 + 0\\ -1\cdot0 + 1\cdot1{,}5 + 0{,}5\cdot3 + 0{,}5 \end{pmatrix} = \begin{pmatrix} -0{,}75\\ 3{,}5 \end{pmatrix}, \qquad \mathbf{a}^{(2)} = \begin{pmatrix} 0\\ 3{,}5 \end{pmatrix}"),
        ("h3", "Слой 3: из двух чисел — ответ"),
        ("eq", r"z^{(3)} = 2\cdot0 - 0{,}5\cdot3{,}5 + 1 = -0{,}75, \qquad \hat y = \sigma(-0{,}75) = \frac{1}{1 + e^{0{,}75}} \approx 0{,}3208"),
        ("viz", "fp-matvec", VIZ["matvec"], r"<b>Рисунок 2.</b> Умножение «матрица на вектор» внутри каждого слоя. Выберите слой и нажимайте «Шаг»: подсвечивается строка $W$ (один нейрон), под ней — попарные произведения с входом, их сумма, смещение и активация. Так видно, что $W\mathbf{a} + \mathbf{b}$ — это $n_l$ формул одного нейрона, выполненных одновременно."),
        ("table", ["Слой", r"$\mathbf{z}^{(l)}$", r"$\mathbf{a}^{(l)}$"], [
            ["вход", "—", "(1; 2)"],
            ["1", "(−0,5; 1,5; 3)", "(0; 1,5; 3)"],
            ["2", "(−0,75; 3,5)", "(0; 3,5)"],
            ["3", "−0,75", "0,3208"],
        ], {"num": []}),
        ("callout", "note", "Что сохранить", r"Все $\mathbf{z}^{(l)}$ и $\mathbf{a}^{(l)}$ из этой таблицы при обучении запоминают: обратный проход использует их, чтобы посчитать градиенты, не повторяя прямой проход."),
    ]),

    dict(id="shapes", title="Размерности: проверка, которая ловит половину ошибок", blocks=[
        ("p", r"Каждое действие прямого прохода меняет размер вектора по простому правилу: матрица $n_l \times n_{l-1}$, умноженная на вектор длины $n_{l-1}$, даёт вектор длины $n_l$. Цепочка размеров нашей сети:"),
        ("eq", r"\underbrace{\mathbf{x}}_{2} \xrightarrow{\ W^{(1)}:\,3\times2\ } \underbrace{\mathbf{a}^{(1)}}_{3} \xrightarrow{\ W^{(2)}:\,2\times3\ } \underbrace{\mathbf{a}^{(2)}}_{2} \xrightarrow{\ W^{(3)}:\,1\times2\ } \underbrace{\hat y}_{1}"),
        ("p", r"Число столбцов $W^{(l)}$ обязано совпасть с длиной входа слоя, число строк определяет длину выхода. Если они не совпали, код упадёт с ошибкой формы — и это хорошо: хуже, когда формы случайно совпали, а смысл перепутан (например, $W$ вместо $W^{\top}$ у квадратной матрицы)."),
        ("viz", "fp-shapes", VIZ["shapes"], r"<b>Рисунок 3.</b> Конструктор архитектуры. Задайте размеры слоёв через дефис или выберите готовый вариант: таблица показывает формы $W^{(l)}$, $\mathbf{b}^{(l)}$, число параметров и умножений на один объект, а столбики — где сосредоточены параметры."),
        ("callout", "key", "Стоимость прямого прохода", r"На один объект слой тратит $n_l\cdot n_{l-1}$ умножений со сложением — по одному на каждый вес. Значит, весь прямой проход стоит примерно столько операций, сколько у сети весов: $\sum_l n_l\,n_{l-1}$. Для нашей сети это $6 + 6 + 2 = 14$ умножений."),
    ]),

    dict(id="geometry", title="Геометрия: что слой делает с пространством", blocks=[
        ("p", r"Посмотрим на слой как на преобразование пространства. Линейная часть $W\mathbf{a} + \mathbf{b}$ поворачивает, растягивает, наклоняет и сдвигает пространство: прямые остаются прямыми, параллельные — параллельными, клетки сетки превращаются в одинаковые параллелограммы. Активация затем гнёт его: ReLU складывает всё, что попало в отрицательную область, на оси, сигмоида и tanh сжимают далёкие точки к краям."),
        ("viz", "fp-space", VIZ["space"], r"<b>Рисунок 4.</b> Как слой 2 → 2 изгибает плоскость. Ползунок плавно ведёт сетку через этапы: исходная плоскость → линейная часть $W\mathbf{x} + \mathbf{b}$ → активация. Цветные точки — объекты двух классов: смотрите, как после изгиба их можно разделить прямой, хотя на входе нельзя было. Выбирайте активацию и готовые матрицы."),
        ("p", r"Отсюда главный смысл глубины: каждый слой немного перекраивает пространство, и к последнему слою точки разных классов оказываются по разные стороны простой границы. Последний слой — это обычный линейный классификатор или регрессия, но работающий в пространстве, которое предыдущие слои подготовили для него."),
        ("deep", "Почему без активаций слои схлопываются", [
            ("p", r"Если убрать $f$, два слоя дают $W^{(2)}(W^{(1)}\mathbf{x} + \mathbf{b}^{(1)}) + \mathbf{b}^{(2)} = (W^{(2)}W^{(1)})\mathbf{x} + (W^{(2)}\mathbf{b}^{(1)} + \mathbf{b}^{(2)})$ — снова один линейный слой. Любая глубина без нелинейности равна одному слою: параллелограммы, повёрнутые несколько раз, остаются параллелограммами. Подробно — в <a href='../neuron/#activation'>статье об одном нейроне</a>."),
        ]),
    ]),

    dict(id="batch", title="Пакет объектов: та же формула для многих входов", blocks=[
        ("p", r"На практике сеть считает сразу пакет (batch) из $N$ объектов. Их складывают строками в матрицу $X$ размера $N \times n_0$, и прямой проход переписывается для матриц:"),
        ("eq", r"A^{(0)} = X, \qquad Z^{(l)} = A^{(l-1)}\,W^{(l)\top} + \mathbf{1}\,\mathbf{b}^{(l)\top}, \qquad A^{(l)} = f^{(l)}\big(Z^{(l)}\big)"),
        ("p", r"Строка $k$ матрицы $A^{(l)}$ — это $\mathbf{a}^{(l)}$ для объекта $k$; транспонирование появилось потому, что объекты теперь лежат строками, а не столбцами. Слагаемое $\mathbf{1}\mathbf{b}^{\top}$ прибавляет смещения к каждой строке (в NumPy и PyTorch это делает broadcasting). Пакет из трёх объектов через нашу сеть:"),
        ("table", ["Объект", r"$\mathbf{x}$", r"$\mathbf{z}^{(1)}$", r"$\mathbf{z}^{(2)}$", r"$z^{(3)}$", r"$\hat y$"], [
            ["1", "(1; 2)", "(−0,5; 1,5; 3)", "(−0,75; 3,5)", "−0,75", "0,3208"],
            ["2", "(0; 0)", "(0,5; −1; 0)", "(0,5; 0)", "2", "0,8808"],
            ["3", "(2; −1)", "(3,5; −1; −4)", "(3,5; −3)", "8", "0,9997"],
        ], {"num": [4, 5]}),
        ("p", r"Второй объект — нулевой вход: всё, что сеть ему отвечает, определяют одни смещения. Обратите внимание: ответ $0{,}8808$ — это $\sigma(2)$, то самое число из статьи об одном нейроне."),
        ("callout", "intuition", "Зачем пакеты", r"Одно матричное умножение $N \times n$ на $n \times m$ для процессора и особенно видеокарты гораздо выгоднее, чем $N$ умножений вектора на матрицу: данные читаются из памяти один раз и обрабатываются параллельно. Поэтому и обучение, и вывод идут пакетами."),
    ]),

    dict(id="training", title="Прямой проход в обучении: потери и кэш", blocks=[
        ("p", r"Во время обучения прямой проход заканчивается не на $\hat y$, а на числе потерь $L$, которое сравнивает ответ с правильным $y$. Для нашего объекта с меткой $y = 1$ и бинарной кросс-энтропией:"),
        ("eq", r"L = -\big[y\ln\hat y + (1 - y)\ln(1 - \hat y)\big] = -\ln 0{,}3208 \approx 1{,}1369"),
        ("p", r"Ответ $0{,}32$ при правильном $1$ — плохой, и потеря большая. Чтобы её уменьшить, нужно понять, как каждый вес влияет на $L$. Этим занимается обратный проход: он идёт по сети справа налево и по цепному правилу перемножает производные слоёв. Для этого ему нужны именно те $\mathbf{z}^{(l)}$ и $\mathbf{a}^{(l)}$, которые посчитал прямой проход, — поэтому их кэшируют."),
        ("table", ["Режим", "Что считает прямой проход", "Что хранит"], [
            ["обучение", r"ответ $\hat y$ и потерю $L$", r"все $\mathbf{z}^{(l)}$, $\mathbf{a}^{(l)}$ для обратного прохода"],
            ["вывод (inference)", r"только ответ $\hat y$", "ничего лишнего: промежуточные значения сразу отбрасываются"],
        ], {"num": []}),
        ("callout", "note", None, r"Именно поэтому обучение требует намного больше памяти, чем вывод: на каждом шаге в памяти лежат активации всех слоёв для всего пакета. В PyTorch режим вывода включают через <code>torch.no_grad()</code> или <code>torch.inference_mode()</code>."),
    ]),

    dict(id="playground", title="Песочница: собери прямой проход сам", blocks=[
        ("p", r"Всё вместе в одной интерактивной модели. Слева — сеть со значениями каждого нейрона, справа — карта ответа $\hat y$ для всех входов плоскости: цвет точки $(x_1;\ x_2)$ показывает, что ответит сеть. Меняйте вход, функции активации слоёв и масштаб весов — и смотрите, как меняется и одно число, и вся карта."),
        ("viz", "fp-playground", VIZ["play"], r"<b>Рисунок 5.</b> Песочница прямого прохода. Перетащите точку на карте или двигайте ползунки — значения в сети пересчитываются. Переключайте активации скрытых слоёв: с тождественной функцией граница на карте становится прямой (сеть схлопывается в один линейный слой), с ReLU — ломаной, с tanh и сигмоидой — гладкой. Ползунок «масштаб весов» умножает все веса: большие веса делают переходы резкими."),
    ]),

    dict(id="code", title="Код: прямой проход своими руками и в PyTorch", blocks=[
        ("p", r"Прямой проход — это цикл по слоям. Ниже он целиком, с кэшем для обратного прохода и с версией для пакета."),
        ("code", "python", CODE_NUMPY["ru"]),
        ("p", r"То же самое в PyTorch: <code>nn.Linear</code> хранит $W$ и $\mathbf{b}$ и считает $\mathbf{x}W^{\top} + \mathbf{b}$, а <code>nn.Sequential</code> и есть цикл по слоям."),
        ("code", "python", CODE_TORCH["ru"]),
    ]),

    dict(id="practice", title="Практикум: 8 примеров", blocks=[
        ("p", r"Каждый пример показывает одну грань прямого прохода. Все числа проверены вычислением."),
        ("example", dict(n=1, title="Один слой — это логистическая регрессия", kinds=["расчёт"],
            goal=r"Увидеть, что при $L = 1$ прямой проход вырождается в формулу одного нейрона, и связать новую статью с предыдущей.",
            blocks=[
                ("p", r"Сеть 3–1 с сигмоидой: $W^{(1)} = (0{,}5\ \ -1\ \ 0{,}25)$, $b^{(1)} = -0{,}75$, вход $\mathbf{x} = (2;\ -1;\ 3)$."),
                ("eq", r"\hat y = \sigma\big(W^{(1)}\mathbf{x} + b^{(1)}\big) = \sigma(1 + 1 + 0{,}75 - 0{,}75) = \sigma(2) \approx 0{,}8808"),
            ],
            take=r"Однослойная сеть с сигмоидой — это логистическая регрессия; глубокая сеть — та же формула, повторённая $L$ раз.")),
        ("example", dict(n=2, title="XOR: прямой проход через скрытый слой", kinds=["таблица"],
            goal=r"Пройти прямой проход на четырёх входах и увидеть, как скрытый слой с ReLU делает возможным то, что не умеет один нейрон.",
            blocks=[
                ("p", r"Сеть 2–2–1: $h_1 = \mathrm{ReLU}(x_1 + x_2)$, $h_2 = \mathrm{ReLU}(x_1 + x_2 - 1)$, выход линейный: $\hat y = h_1 - 2h_2$."),
                ("table", [r"$(x_1;\ x_2)$", r"$\mathbf{z}^{(1)}$", r"$\mathbf{a}^{(1)}$", r"$\hat y$", "XOR"], [
                    ["(0; 0)", "(0; −1)", "(0; 0)", "0", "0"],
                    ["(0; 1)", "(1; 0)", "(1; 0)", "1", "1"],
                    ["(1; 0)", "(1; 0)", "(1; 0)", "1", "1"],
                    ["(1; 1)", "(2; 1)", "(2; 1)", "0", "0"],
                ], {"num": [3, 4]}),
            ],
            take=r"Второй нейрон включается только при двух единицах и вычитает лишнее. Без ReLU выход был бы линейным, и XOR не получился бы.")),
        ("example", dict(n=3, title="Формы и параметры сети для MNIST", kinds=["таблица", "расчёт"],
            goal=r"Научиться за минуту посчитать формы всех матриц и число параметров реальной сети.",
            blocks=[
                ("p", r"Картинка 28×28 вытягивается в вектор из 784 чисел; сеть 784–128–64–10 выдаёт 10 чисел — по одному на цифру."),
                ("table", ["Слой", r"$W^{(l)}$", r"$\mathbf{b}^{(l)}$", "Параметров", "Умножений"], [
                    ["1", "128 × 784", "128", "100 480", "100 352"],
                    ["2", "64 × 128", "64", "8 256", "8 192"],
                    ["3", "10 × 64", "10", "650", "640"],
                    ["<b>всего</b>", "", "", "<b>109 386</b>", "<b>109 184</b>"],
                ], {"num": [3, 4]}),
            ],
            take=r"Больше 90% параметров — в первом слое, где много входов. Число умножений на один объект почти равно числу весов.")),
        ("example", dict(n=4, title="Выход из нескольких классов: softmax", kinds=["расчёт"],
            goal=r"Увидеть, как последний слой превращает $n_L$ чисел в распределение вероятностей.",
            blocks=[
                ("p", r"Для $K$ классов последний слой выдаёт $K$ чисел $\mathbf{z}^{(L)}$, а активацией служит softmax: $\hat y_k = e^{z_k} / \sum_j e^{z_j}$. При $\mathbf{z}^{(L)} = (2;\ 1;\ 0{,}1)$:"),
                ("eq", r"e^{\mathbf{z}} \approx (7{,}3891;\ 2{,}7183;\ 1{,}1052), \quad \sum \approx 11{,}2125, \quad \hat{\mathbf{y}} \approx (0{,}6590;\ 0{,}2424;\ 0{,}0986)"),
            ],
            take=r"Softmax — не поэлементная активация: каждый выход зависит от всех $z$. Сумма вероятностей всегда 1.")),
        ("example", dict(n=5, title="Нулевой вход и роль смещений", kinds=["расчёт"],
            goal=r"Понять, что смещения задают ответ сети «по умолчанию».",
            blocks=[
                ("p", r"Подадим в нашу сеть $\mathbf{x} = (0;\ 0)$. Тогда $\mathbf{z}^{(1)} = \mathbf{b}^{(1)} = (0{,}5;\ -1;\ 0)$, $\mathbf{a}^{(1)} = (0{,}5;\ 0;\ 0)$, $\mathbf{z}^{(2)} = (0{,}5;\ 0)$, $\mathbf{a}^{(2)} = (0{,}5;\ 0)$, $z^{(3)} = 2\cdot0{,}5 + 1 = 2$, $\hat y = \sigma(2) \approx 0{,}8808$."),
            ],
            take=r"Без смещений нулевой вход всегда давал бы $\mathbf{z} = \mathbf{0}$ на каждом слое и $\hat y = \sigma(0) = 0{,}5$, что бы сеть ни выучила.")),
        ("example", dict(n=6, title="«Выключенные» нейроны: что ReLU делает с потоком", kinds=["расчёт"],
            goal=r"Увидеть, что нейрон с $a = 0$ полностью отключает свою ветку: его исходящие веса не влияют на ответ.",
            blocks=[
                ("p", r"В нашем примере первый нейрон слоя 2 выдал $a^{(2)}_1 = 0$ ($z = -0{,}75$). Его вес в выходном слое $W^{(3)}_{11} = 2$. Заменим его на $100$ или на $-100$: $z^{(3)} = 100\cdot0 - 0{,}5\cdot3{,}5 + 1 = -0{,}75$ — ответ не изменится."),
            ],
            take=r"При данном входе работает только часть сети. Для другого входа включатся другие нейроны — так ReLU-сеть составляет ответ из кусков, каждый из которых линеен.")),
        ("example", dict(n=7, title="Глубина или ширина", kinds=["таблица"],
            goal=r"Сравнить, во что обходится ширина и во что — глубина.",
            blocks=[
                ("table", ["Сеть", "Слои", "Параметров"], [
                    ["2–100–1", "1 скрытый, широкий", "2·100 + 100 + 100 + 1 = 401"],
                    ["2–10–10–10–1", "3 скрытых, узких", "30 + 110 + 110 + 11 = 261"],
                ], {"num": []}),
            ],
            take=r"Глубокая узкая сеть может стоить меньше широкой мелкой и при этом строить более сложные функции: каждый слой складывает пространство заново, и число «изломов» растёт с глубиной быстрее, чем с шириной.")),
        ("example", dict(n=8, title="Численная устойчивость: где прямой проход ломается", kinds=["расчёт", "код"],
            goal=r"Узнать два классических способа получить NaN на прямом проходе и как их обойти.",
            blocks=[
                ("p", r"Softmax с $\mathbf{z} = (1000;\ 1001;\ 1002)$: $e^{1000}$ не помещается в число с плавающей точкой, получаются $\infty/\infty = $ NaN. Но softmax не меняется, если из всех $z$ вычесть одно и то же число. Вычтем максимум:"),
                ("eq", r"\mathbf{z} - 1002 = (-2;\ -1;\ 0), \quad e^{\mathbf{z} - \max} \approx (0{,}1353;\ 0{,}3679;\ 1), \quad \hat{\mathbf{y}} \approx (0{,}0900;\ 0{,}2447;\ 0{,}6652)"),
                ("p", r"То же с сигмоидой: при $z = -1000$ наивная $1/(1 + e^{1000})$ переполняется. Устойчивая версия считает $e^{z}/(1 + e^{z})$ для отрицательных $z$. И на выходе классификатора в потери отдают логиты $\mathbf{z}^{(L)}$, а не вероятности: <code>BCEWithLogitsLoss</code>, <code>CrossEntropyLoss</code>."),
            ],
            take=r"Математически формула прямого прохода верна для любых чисел, а машинно — нет. Устойчивые версии считают то же самое, но в безопасном порядке.")),
    ]),

    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ul", [
            r"<b>Перепутать порядок индексов.</b> $W^{(l)}_{jk}$ — «в нейрон $j$ из нейрона $k$». Матрица имеет форму $n_l \times n_{l-1}$, в PyTorch — <code>(out_features, in_features)</code>.",
            r"<b>$\mathbf{x}W$ вместо $W\mathbf{x}$.</b> Для одного вектора-столбца — $W\mathbf{x}$; для пакета строками — $XW^{\top}$. Смешение даёт ошибку формы или, хуже, неверный ответ у квадратных матриц.",
            r"<b>Забыть активацию между слоями.</b> Сеть молча схлопывается в один линейный слой.",
            r"<b>Поставить ReLU на выход регрессии</b>, где ответ бывает отрицательным: сеть физически не сможет его выдать. На выходе регрессии — тождественная функция.",
            r"<b>Применить softmax и затем CrossEntropyLoss в PyTorch</b>, которая уже делает log-softmax внутри: вероятности посчитаются дважды.",
            r"<b>Не масштабировать вход.</b> Огромные $\mathbf{x}$ дают огромные $\mathbf{z}$, насыщают сигмоиды и tanh и ломают обучение.",
            r"<b>Считать, что прямой проход учит сеть.</b> Он только вычисляет; веса меняет шаг оптимизатора после обратного прохода.",
        ]),
    ]),

    dict(id="summary", title="Итоги", blocks=[
        ("ul", [
            r"Прямой проход: $\mathbf{a}^{(0)} = \mathbf{x}$; для $l = 1..L$: $\mathbf{z}^{(l)} = W^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}$, $\mathbf{a}^{(l)} = f^{(l)}(\mathbf{z}^{(l)})$; ответ $\hat{\mathbf{y}} = \mathbf{a}^{(L)}$.",
            r"Каждая строка $W^{(l)}$ — один нейрон; слой — это $n_l$ формул одного нейрона сразу.",
            r"$W^{(l)}$ имеет форму $n_l \times n_{l-1}$; у слоя $n_l(n_{l-1} + 1)$ параметров; прямой проход стоит $\sum_l n_l n_{l-1}$ умножений на объект.",
            r"Для пакета: $Z^{(l)} = A^{(l-1)}W^{(l)\top} + \mathbf{1}\mathbf{b}^{(l)\top}$.",
            r"Геометрически линейная часть поворачивает и растягивает пространство, активация его гнёт; без активаций слои схлопываются в один.",
            r"При обучении прямой проход заканчивается потерей и сохраняет все $\mathbf{z}$ и $\mathbf{a}$ для обратного прохода.",
        ]),
    ]),

    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q=r"Какую форму имеет $W^{(l)}$ слоя, где 5 входов и 3 нейрона?", options=[r"$5 \times 3$", r"$3 \times 5$", r"$3 \times 3$", r"$5 \times 5$"], answer=1,
                 explain=r"Строк столько, сколько нейронов ($n_l = 3$), столбцов — сколько входов ($n_{l-1} = 5$)."),
            dict(q=r"Сколько параметров у слоя 4 → 6?", options=["24", "28", "30", "34"], answer=2, explain=r"$6\cdot(4 + 1) = 30$: 24 веса и 6 смещений."),
            dict(q=r"Слой: $W = \begin{pmatrix}1 & 2\end{pmatrix}$, $b = -1$, ReLU, вход $(1;\ -1)$. Выход?", options=["0", "−2", "2", "1"], answer=0,
                 explain=r"$z = 1 - 2 - 1 = -2$, $\mathrm{ReLU}(-2) = 0$."),
            dict(q=r"Что будет, если убрать все активации у сети 2–3–2–1?", options=["Она станет точнее", "Она станет эквивалентна одному линейному слою", "Она перестанет считать", "Ничего не изменится"], answer=1,
                 explain=r"Композиция линейных преобразований линейна: $W^{(3)}W^{(2)}W^{(1)}\mathbf{x} + \dots$"),
            dict(q=r"Как записывается слой для пакета $X$ (объекты строками)?", options=[r"$WX + \mathbf{b}$", r"$XW^{\top} + \mathbf{1}\mathbf{b}^{\top}$", r"$X^{\top}W$", r"$W^{\top}X^{\top}$"], answer=1,
                 explain=r"Каждая строка $X$ — вектор $\mathbf{x}^{\top}$, а $(W\mathbf{x})^{\top} = \mathbf{x}^{\top}W^{\top}$."),
            dict(q=r"Зачем при обучении сохранять $\mathbf{z}^{(l)}$ и $\mathbf{a}^{(l)}$?", options=["Для красоты", "Чтобы обратный проход посчитал градиенты без повторного прямого", "Чтобы уменьшить потерю", "Это нужно только при выводе"], answer=1,
                 explain=r"Производные слоёв выражаются через эти значения, например $f'(\mathbf{z}^{(l)})$ и $\mathbf{a}^{(l-1)}$."),
        ]),
    ]),
]


EN = [
    dict(id="idea", title="What the forward pass is", blocks=[
        ("p", r"In <a href='../neuron/'>the article about a single neuron</a> we took apart the formula $a = f(\mathbf{w}^{\top}\mathbf{x} + b)$. A real network is many such neurons stacked into layers: the outputs of one layer become the inputs of the next. The <b>forward pass</b> is the computation of the network’s answer: the input travels from left to right, layer by layer, all the way to the last layer."),
        ("p", r"The whole procedure is written in three lines:"),
        ("eq", r"\mathbf{a}^{(0)} = \mathbf{x}"),
        ("eq", r"\mathbf{z}^{(l)} = W^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}, \qquad \mathbf{a}^{(l)} = f^{(l)}\big(\mathbf{z}^{(l)}\big), \qquad l = 1, 2, \dots, L"),
        ("eq", r"\hat{\mathbf{y}} = \mathbf{a}^{(L)}"),
        ("p", r"Let us read it as an instruction: put the input into the “zeroth layer”; in every layer, multiply whatever has arrived by the weight matrix, add the biases and pass the result through the activation function; whatever comes out of the last layer is the answer. If we unroll the loop, we get one long nested formula:"),
        ("eq", r"\hat{\mathbf{y}} = f^{(L)}\Big(W^{(L)}\,f^{(L-1)}\big(\cdots f^{(1)}\big(W^{(1)}\mathbf{x} + \mathbf{b}^{(1)}\big)\cdots\big) + \mathbf{b}^{(L)}\Big)"),
        ("viz", "fp-flow", VIZ["flow"], r"<b>Figure 1.</b> The forward pass in a 2–3–2–1 network. Press “Step” or “Play”: the signal travels layer by layer, and in every neuron first $z$ appears, then $a = f(z)$. Blue connections are positive weights, red ones are negative, the thickness is the absolute value of the weight. Move the input sliders: the answer $\hat y$ is recomputed at once."),
        ("callout", "intuition", "An analogy", r"An assembly line in a factory. The raw material (the input $\mathbf{x}$) passes through machines (the layers). Every machine does the same thing: it mixes the incoming parts in the right proportions (the matrix $W$), adds its own additive (the bias $\mathbf{b}$) and processes the result (the activation $f$). No machine knows about the final product: it sees only what came from the previous one. The product leaving the last machine is the network’s answer."),
        ("callout", "key", "The main point", r"The forward pass does not train the network and does not change its weights: it only computes the answer with the current weights. Training comes afterwards: the answer is compared with the correct one (the loss function), and the backward pass computes how to adjust the weights."),
    ]),

    dict(id="anatomy", title="The formula bone by bone: every symbol", blocks=[
        ("p", r"All the notation of the forward pass, with sizes. We denote the number of neurons in layer $l$ by $n_l$; $n_0$ is the number of inputs."),
        ("symbols", [
            (r"l", r"<b>layer number</b>: $l = 1, \dots, L$; the superscript in parentheses $^{(l)}$ means “belongs to layer $l$”, not a power;"),
            (r"L", r"<b>number of layers with weights</b> (the depth of the network); the input “layer” $0$ has no weights;"),
            (r"\mathbf{a}^{(l-1)}", r"<b>input of layer</b> $l$: the output of the previous layer, a vector of length $n_{l-1}$; $\mathbf{a}^{(0)} = \mathbf{x}$;"),
            (r"W^{(l)}", r"<b>weight matrix</b> of the layer: $n_l$ rows and $n_{l-1}$ columns; row $j$ holds the weights of neuron $j$;"),
            (r"W^{(l)}_{jk}", r"<b>a single weight</b>: from neuron $k$ of layer $l-1$ to neuron $j$ of layer $l$ (first “where to”, then “where from”);"),
            (r"\mathbf{b}^{(l)}", r"<b>bias vector</b> of length $n_l$: one bias per neuron;"),
            (r"\mathbf{z}^{(l)}", r"<b>pre-activations</b> of the layer, a vector of length $n_l$: the weighted sums of all its neurons;"),
            (r"f^{(l)}", r"<b>activation function</b> of the layer; applied to each coordinate separately;"),
            (r"\mathbf{a}^{(l)}", r"<b>output of the layer</b> (activations), a vector of length $n_l$;"),
            (r"\hat{\mathbf{y}}", r"<b>the network’s answer</b>: the output of the last layer $\mathbf{a}^{(L)}$."),
        ]),
        ("h3", "One layer is many neurons at once"),
        ("p", r"Let us write the first line of the formula out coordinate by coordinate. Neuron $j$ of layer $l$ computes exactly the same formula as a single neuron: the weighted sum of its inputs plus its own bias."),
        ("eq", r"z^{(l)}_j = \sum_{k=1}^{n_{l-1}} W^{(l)}_{jk}\,a^{(l-1)}_k + b^{(l)}_j, \qquad a^{(l)}_j = f^{(l)}\big(z^{(l)}_j\big), \qquad j = 1, \dots, n_l"),
        ("p", r"The matrix notation $W^{(l)}\mathbf{a}^{(l-1)}$ is simply a way to compute all $n_l$ of these sums in one operation: the $j$-th row of the matrix multiplied by the input vector gives $z_j$. So the forward pass formula is the formula of a single neuron, applied to all the neurons of a layer and repeated for all the layers."),
        ("h3", "The sizes in our example"),
        ("p", r"The rest of the text relies on one network: 2 inputs, hidden layers of 3 and 2 neurons with ReLU, and one output neuron with the sigmoid (a 2–3–2–1 network)."),
        ("table", ["Layer $l$", r"$n_{l-1} \to n_l$", r"$W^{(l)}$", r"$\mathbf{b}^{(l)}$", r"$f^{(l)}$", "Parameters"], [
            ["1", "2 → 3", "3 × 2", "3", "ReLU", "3·2 + 3 = 9"],
            ["2", "3 → 2", "2 × 3", "2", "ReLU", "2·3 + 2 = 8"],
            ["3", "2 → 1", "1 × 2", "1", "sigmoid", "1·2 + 1 = 3"],
            ["<b>total</b>", "", "", "", "", "<b>20</b>"],
        ], {"num": [0]}),
        ("callout", "key", "The counting rule", r"A layer $n_{l-1}\to n_l$ has exactly $n_l\,(n_{l-1} + 1)$ parameters: $n_l n_{l-1}$ weights and $n_l$ biases. The whole network has the sum over its layers."),
    ]),

    dict(id="numbers", title="The forward pass in numbers, step by step", blocks=[
        ("p", r"The input is $\mathbf{x} = (1,\ 2)$. The weights and biases:"),
        ("eq", r"W^{(1)} = \begin{pmatrix} 1 & -1\\ 0.5 & 1\\ -1 & 2 \end{pmatrix},\ \mathbf{b}^{(1)} = \begin{pmatrix} 0.5\\ -1\\ 0 \end{pmatrix};\quad W^{(2)} = \begin{pmatrix} 1 & 0.5 & -0.5\\ -1 & 1 & 0.5 \end{pmatrix},\ \mathbf{b}^{(2)} = \begin{pmatrix} 0\\ 0.5 \end{pmatrix};\quad W^{(3)} = \begin{pmatrix} 2 & -0.5 \end{pmatrix},\ b^{(3)} = 1"),
        ("h3", "Layer 1: from two numbers to three"),
        ("eq", r"\mathbf{z}^{(1)} = \begin{pmatrix} 1\cdot1 + (-1)\cdot2 + 0.5\\ 0.5\cdot1 + 1\cdot2 - 1\\ (-1)\cdot1 + 2\cdot2 + 0 \end{pmatrix} = \begin{pmatrix} -0.5\\ 1.5\\ 3 \end{pmatrix}, \qquad \mathbf{a}^{(1)} = \mathrm{ReLU}\big(\mathbf{z}^{(1)}\big) = \begin{pmatrix} 0\\ 1.5\\ 3 \end{pmatrix}"),
        ("p", r"The first neuron received a negative sum, and ReLU “switched it off”: from here on, only a zero travels down the network from it."),
        ("h3", "Layer 2: from three numbers to two"),
        ("eq", r"\mathbf{z}^{(2)} = \begin{pmatrix} 1\cdot0 + 0.5\cdot1.5 - 0.5\cdot3 + 0\\ -1\cdot0 + 1\cdot1.5 + 0.5\cdot3 + 0.5 \end{pmatrix} = \begin{pmatrix} -0.75\\ 3.5 \end{pmatrix}, \qquad \mathbf{a}^{(2)} = \begin{pmatrix} 0\\ 3.5 \end{pmatrix}"),
        ("h3", "Layer 3: from two numbers to the answer"),
        ("eq", r"z^{(3)} = 2\cdot0 - 0.5\cdot3.5 + 1 = -0.75, \qquad \hat y = \sigma(-0.75) = \frac{1}{1 + e^{0.75}} \approx 0.3208"),
        ("viz", "fp-matvec", VIZ["matvec"], r"<b>Figure 2.</b> The matrix–vector product inside each layer. Choose a layer and press “Step”: a row of $W$ (one neuron) is highlighted, and below it you see the pairwise products with the input, their sum, the bias and the activation. This shows that $W\mathbf{a} + \mathbf{b}$ is $n_l$ single-neuron formulas evaluated at the same time."),
        ("table", ["Layer", r"$\mathbf{z}^{(l)}$", r"$\mathbf{a}^{(l)}$"], [
            ["input", "—", "(1, 2)"],
            ["1", "(−0.5, 1.5, 3)", "(0, 1.5, 3)"],
            ["2", "(−0.75, 3.5)", "(0, 3.5)"],
            ["3", "−0.75", "0.3208"],
        ], {"num": []}),
        ("callout", "note", "What to keep", r"During training, all the $\mathbf{z}^{(l)}$ and $\mathbf{a}^{(l)}$ in this table are stored: the backward pass uses them to compute the gradients without repeating the forward pass."),
    ]),

    dict(id="shapes", title="Shapes: a check that catches half of all bugs", blocks=[
        ("p", r"Every operation of the forward pass changes the size of the vector by a simple rule: an $n_l \times n_{l-1}$ matrix multiplied by a vector of length $n_{l-1}$ gives a vector of length $n_l$. The chain of sizes in our network:"),
        ("eq", r"\underbrace{\mathbf{x}}_{2} \xrightarrow{\ W^{(1)}:\,3\times2\ } \underbrace{\mathbf{a}^{(1)}}_{3} \xrightarrow{\ W^{(2)}:\,2\times3\ } \underbrace{\mathbf{a}^{(2)}}_{2} \xrightarrow{\ W^{(3)}:\,1\times2\ } \underbrace{\hat y}_{1}"),
        ("p", r"The number of columns of $W^{(l)}$ must match the length of the layer’s input; the number of rows determines the length of its output. If they do not match, the code fails with a shape error, and that is a good thing: it is worse when the shapes happen to match but the meaning is mixed up (for example, $W$ instead of $W^{\top}$ for a square matrix)."),
        ("viz", "fp-shapes", VIZ["shapes"], r"<b>Figure 3.</b> An architecture builder. Enter the layer sizes separated by hyphens or pick a ready-made option: the table shows the shapes of $W^{(l)}$ and $\mathbf{b}^{(l)}$, the number of parameters and the number of multiplications per object, and the bars show where the parameters are concentrated."),
        ("callout", "key", "The cost of the forward pass", r"For one object, a layer spends $n_l\cdot n_{l-1}$ multiply-adds, one per weight. So the whole forward pass costs roughly as many operations as the network has weights: $\sum_l n_l\,n_{l-1}$. For our network this is $6 + 6 + 2 = 14$ multiplications."),
    ]),

    dict(id="geometry", title="Geometry: what a layer does to space", blocks=[
        ("p", r"Let us look at a layer as a transformation of space. The linear part $W\mathbf{a} + \mathbf{b}$ rotates, stretches, shears and shifts space: straight lines stay straight, parallel lines stay parallel, and the cells of a grid become identical parallelograms. The activation then bends it: ReLU folds everything that landed in the negative region onto the axes, while the sigmoid and tanh squeeze distant points towards the edges."),
        ("viz", "fp-space", VIZ["space"], r"<b>Figure 4.</b> How a 2 → 2 layer bends the plane. The slider smoothly moves the grid through the stages: the original plane → the linear part $W\mathbf{x} + \mathbf{b}$ → the activation. The coloured dots are objects of two classes: watch how, after the bending, they can be separated by a straight line, although at the input this was impossible. Choose the activation and the preset matrices."),
        ("p", r"This is the main point of depth: each layer reshapes space a little, and by the last layer the points of different classes end up on different sides of a simple boundary. The last layer is an ordinary linear classifier or regression, but one that works in a space the previous layers have prepared for it."),
        ("deep", "Why layers collapse without activations", [
            ("p", r"If we remove $f$, two layers give $W^{(2)}(W^{(1)}\mathbf{x} + \mathbf{b}^{(1)}) + \mathbf{b}^{(2)} = (W^{(2)}W^{(1)})\mathbf{x} + (W^{(2)}\mathbf{b}^{(1)} + \mathbf{b}^{(2)})$, which is again a single linear layer. Any depth without non-linearity equals one layer: parallelograms rotated several times remain parallelograms. For details, see <a href='../neuron/#activation'>the article about a single neuron</a>."),
        ]),
    ]),

    dict(id="batch", title="A batch of objects: the same formula for many inputs", blocks=[
        ("p", r"In practice a network processes a whole batch of $N$ objects at once. They are stacked as rows into a matrix $X$ of size $N \times n_0$, and the forward pass is rewritten for matrices:"),
        ("eq", r"A^{(0)} = X, \qquad Z^{(l)} = A^{(l-1)}\,W^{(l)\top} + \mathbf{1}\,\mathbf{b}^{(l)\top}, \qquad A^{(l)} = f^{(l)}\big(Z^{(l)}\big)"),
        ("p", r"Row $k$ of the matrix $A^{(l)}$ is $\mathbf{a}^{(l)}$ for object $k$; the transpose appears because the objects are now stored as rows rather than columns. The term $\mathbf{1}\mathbf{b}^{\top}$ adds the biases to every row (in NumPy and PyTorch this is done by broadcasting). A batch of three objects through our network:"),
        ("table", ["Object", r"$\mathbf{x}$", r"$\mathbf{z}^{(1)}$", r"$\mathbf{z}^{(2)}$", r"$z^{(3)}$", r"$\hat y$"], [
            ["1", "(1, 2)", "(−0.5, 1.5, 3)", "(−0.75, 3.5)", "−0.75", "0.3208"],
            ["2", "(0, 0)", "(0.5, −1, 0)", "(0.5, 0)", "2", "0.8808"],
            ["3", "(2, −1)", "(3.5, −1, −4)", "(3.5, −3)", "8", "0.9997"],
        ], {"num": [4, 5]}),
        ("p", r"The second object is the zero input: the network’s entire answer to it is determined by the biases alone. Note that the answer $0.8808$ is $\sigma(2)$, the very same number as in the article about a single neuron."),
        ("callout", "intuition", "Why batches", r"A single matrix multiplication of $N \times n$ by $n \times m$ is far more efficient for a CPU, and especially for a GPU, than $N$ vector–matrix multiplications: the data are read from memory once and processed in parallel. That is why both training and inference run in batches."),
    ]),

    dict(id="training", title="The forward pass in training: the loss and the cache", blocks=[
        ("p", r"During training, the forward pass ends not at $\hat y$ but at the loss value $L$, which compares the answer with the correct $y$. For our object with the label $y = 1$ and binary cross-entropy:"),
        ("eq", r"L = -\big[y\ln\hat y + (1 - y)\ln(1 - \hat y)\big] = -\ln 0.3208 \approx 1.1369"),
        ("p", r"An answer of $0.32$ when the correct one is $1$ is bad, and the loss is large. To reduce it, we need to know how each weight affects $L$. This is the job of the backward pass: it goes through the network from right to left and multiplies the derivatives of the layers by the chain rule. For this it needs exactly the $\mathbf{z}^{(l)}$ and $\mathbf{a}^{(l)}$ that the forward pass computed, which is why they are cached."),
        ("table", ["Mode", "What the forward pass computes", "What it stores"], [
            ["training", r"the answer $\hat y$ and the loss $L$", r"all $\mathbf{z}^{(l)}$, $\mathbf{a}^{(l)}$ for the backward pass"],
            ["inference", r"only the answer $\hat y$", "nothing extra: intermediate values are discarded immediately"],
        ], {"num": []}),
        ("callout", "note", None, r"This is exactly why training needs much more memory than inference: at every step, the activations of all layers for the whole batch are held in memory. In PyTorch, inference mode is turned on with <code>torch.no_grad()</code> or <code>torch.inference_mode()</code>."),
    ]),

    dict(id="playground", title="Playground: build the forward pass yourself", blocks=[
        ("p", r"Everything together in one interactive model. On the left is the network with the value of every neuron; on the right is a map of the answer $\hat y$ for all inputs of the plane: the colour of the point $(x_1,\ x_2)$ shows what the network will answer. Change the input, the activation functions of the layers and the weight scale, and watch how both the single number and the whole map change."),
        ("viz", "fp-playground", VIZ["play"], r"<b>Figure 5.</b> The forward pass playground. Drag the point on the map or move the sliders: the values in the network are recomputed. Switch the activations of the hidden layers: with the identity function the boundary on the map becomes a straight line (the network collapses into one linear layer), with ReLU a polyline, with tanh and the sigmoid a smooth curve. The “weight scale” slider multiplies all the weights: large weights make the transitions sharp."),
    ]),

    dict(id="code", title="Code: the forward pass by hand and in PyTorch", blocks=[
        ("p", r"The forward pass is a loop over the layers. Here it is in full, with a cache for the backward pass and with a batch version."),
        ("code", "python", CODE_NUMPY["en"]),
        ("p", r"The same thing in PyTorch: <code>nn.Linear</code> stores $W$ and $\mathbf{b}$ and computes $\mathbf{x}W^{\top} + \mathbf{b}$, and <code>nn.Sequential</code> is exactly the loop over the layers."),
        ("code", "python", CODE_TORCH["en"]),
    ]),

    dict(id="practice", title="Practice: 8 examples", blocks=[
        ("p", r"Each example shows one facet of the forward pass. Every number has been verified by computation."),
        ("example", dict(n=1, title="One layer is logistic regression", kinds=["calculation"],
            goal=r"See that with $L = 1$ the forward pass reduces to the formula of a single neuron, and connect this article with the previous one.",
            blocks=[
                ("p", r"A 3–1 network with the sigmoid: $W^{(1)} = (0.5\ \ -1\ \ 0.25)$, $b^{(1)} = -0.75$, input $\mathbf{x} = (2,\ -1,\ 3)$."),
                ("eq", r"\hat y = \sigma\big(W^{(1)}\mathbf{x} + b^{(1)}\big) = \sigma(1 + 1 + 0.75 - 0.75) = \sigma(2) \approx 0.8808"),
            ],
            take=r"A single-layer network with the sigmoid is logistic regression; a deep network is the same formula repeated $L$ times.")),
        ("example", dict(n=2, title="XOR: a forward pass through a hidden layer", kinds=["table"],
            goal=r"Run the forward pass on four inputs and see how a hidden layer with ReLU makes possible what a single neuron cannot do.",
            blocks=[
                ("p", r"A 2–2–1 network: $h_1 = \mathrm{ReLU}(x_1 + x_2)$, $h_2 = \mathrm{ReLU}(x_1 + x_2 - 1)$, with a linear output: $\hat y = h_1 - 2h_2$."),
                ("table", [r"$(x_1,\ x_2)$", r"$\mathbf{z}^{(1)}$", r"$\mathbf{a}^{(1)}$", r"$\hat y$", "XOR"], [
                    ["(0, 0)", "(0, −1)", "(0, 0)", "0", "0"],
                    ["(0, 1)", "(1, 0)", "(1, 0)", "1", "1"],
                    ["(1, 0)", "(1, 0)", "(1, 0)", "1", "1"],
                    ["(1, 1)", "(2, 1)", "(2, 1)", "0", "0"],
                ], {"num": [3, 4]}),
            ],
            take=r"The second neuron switches on only when both inputs are ones, and it subtracts the excess. Without ReLU the output would be linear, and XOR would be out of reach.")),
        ("example", dict(n=3, title="Shapes and parameters of a network for MNIST", kinds=["table", "calculation"],
            goal=r"Learn to compute the shapes of all the matrices and the number of parameters of a real network in a minute.",
            blocks=[
                ("p", r"A 28×28 image is flattened into a vector of 784 numbers; the 784–128–64–10 network outputs 10 numbers, one per digit."),
                ("table", ["Layer", r"$W^{(l)}$", r"$\mathbf{b}^{(l)}$", "Parameters", "Multiplications"], [
                    ["1", "128 × 784", "128", "100,480", "100,352"],
                    ["2", "64 × 128", "64", "8,256", "8,192"],
                    ["3", "10 × 64", "10", "650", "640"],
                    ["<b>total</b>", "", "", "<b>109,386</b>", "<b>109,184</b>"],
                ], {"num": [3, 4]}),
            ],
            take=r"More than 90% of the parameters are in the first layer, which has many inputs. The number of multiplications per object is almost equal to the number of weights.")),
        ("example", dict(n=4, title="An output with several classes: softmax", kinds=["calculation"],
            goal=r"See how the last layer turns $n_L$ numbers into a probability distribution.",
            blocks=[
                ("p", r"For $K$ classes the last layer outputs $K$ numbers $\mathbf{z}^{(L)}$, and the activation is softmax: $\hat y_k = e^{z_k} / \sum_j e^{z_j}$. For $\mathbf{z}^{(L)} = (2,\ 1,\ 0.1)$:"),
                ("eq", r"e^{\mathbf{z}} \approx (7.3891,\ 2.7183,\ 1.1052), \quad \sum \approx 11.2125, \quad \hat{\mathbf{y}} \approx (0.6590,\ 0.2424,\ 0.0986)"),
            ],
            take=r"Softmax is not an element-wise activation: each output depends on all the $z$. The probabilities always sum to 1.")),
        ("example", dict(n=5, title="The zero input and the role of the biases", kinds=["calculation"],
            goal=r"Understand that the biases set the network’s “default” answer.",
            blocks=[
                ("p", r"Feed $\mathbf{x} = (0,\ 0)$ into our network. Then $\mathbf{z}^{(1)} = \mathbf{b}^{(1)} = (0.5,\ -1,\ 0)$, $\mathbf{a}^{(1)} = (0.5,\ 0,\ 0)$, $\mathbf{z}^{(2)} = (0.5,\ 0)$, $\mathbf{a}^{(2)} = (0.5,\ 0)$, $z^{(3)} = 2\cdot0.5 + 1 = 2$, $\hat y = \sigma(2) \approx 0.8808$."),
            ],
            take=r"Without biases, the zero input would always give $\mathbf{z} = \mathbf{0}$ in every layer and $\hat y = \sigma(0) = 0.5$, no matter what the network has learned.")),
        ("example", dict(n=6, title="“Switched-off” neurons: what ReLU does to the flow", kinds=["calculation"],
            goal=r"See that a neuron with $a = 0$ completely disconnects its branch: its outgoing weights do not affect the answer.",
            blocks=[
                ("p", r"In our example, the first neuron of layer 2 output $a^{(2)}_1 = 0$ ($z = -0.75$). Its weight in the output layer is $W^{(3)}_{11} = 2$. Replace it with $100$ or with $-100$: $z^{(3)} = 100\cdot0 - 0.5\cdot3.5 + 1 = -0.75$, and the answer does not change."),
            ],
            take=r"For a given input, only part of the network is at work. For a different input, other neurons switch on: this is how a ReLU network assembles its answer from pieces, each of which is linear.")),
        ("example", dict(n=7, title="Depth or width", kinds=["table"],
            goal=r"Compare what width costs and what depth costs.",
            blocks=[
                ("table", ["Network", "Layers", "Parameters"], [
                    ["2–100–1", "1 hidden, wide", "2·100 + 100 + 100 + 1 = 401"],
                    ["2–10–10–10–1", "3 hidden, narrow", "30 + 110 + 110 + 11 = 261"],
                ], {"num": []}),
            ],
            take=r"A deep narrow network can cost less than a wide shallow one and still build more complex functions: each layer folds space anew, and the number of “kinks” grows faster with depth than with width.")),
        ("example", dict(n=8, title="Numerical stability: where the forward pass breaks", kinds=["calculation", "code"],
            goal=r"Learn two classic ways to get NaN in the forward pass and how to avoid them.",
            blocks=[
                ("p", r"Softmax with $\mathbf{z} = (1000,\ 1001,\ 1002)$: $e^{1000}$ does not fit into a floating-point number, and we get $\infty/\infty = $ NaN. But softmax does not change if the same number is subtracted from all the $z$. Let us subtract the maximum:"),
                ("eq", r"\mathbf{z} - 1002 = (-2,\ -1,\ 0), \quad e^{\mathbf{z} - \max} \approx (0.1353,\ 0.3679,\ 1), \quad \hat{\mathbf{y}} \approx (0.0900,\ 0.2447,\ 0.6652)"),
                ("p", r"The same goes for the sigmoid: at $z = -1000$ the naive $1/(1 + e^{1000})$ overflows. The stable version computes $e^{z}/(1 + e^{z})$ for negative $z$. And at the output of a classifier, the loss is given the logits $\mathbf{z}^{(L)}$, not the probabilities: <code>BCEWithLogitsLoss</code>, <code>CrossEntropyLoss</code>."),
            ],
            take=r"Mathematically, the forward pass formula holds for any numbers; on a machine it does not. Stable versions compute the same thing, but in a safe order.")),
    ]),

    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ul", [
            r"<b>Mixing up the order of the indices.</b> $W^{(l)}_{jk}$ means “into neuron $j$ from neuron $k$”. The matrix has the shape $n_l \times n_{l-1}$; in PyTorch it is <code>(out_features, in_features)</code>.",
            r"<b>$\mathbf{x}W$ instead of $W\mathbf{x}$.</b> For a single column vector it is $W\mathbf{x}$; for a batch stored as rows it is $XW^{\top}$. Mixing them up gives a shape error or, worse, a wrong answer with square matrices.",
            r"<b>Forgetting the activation between layers.</b> The network silently collapses into a single linear layer.",
            r"<b>Putting ReLU on the output of a regression</b> where the answer can be negative: the network will be physically unable to produce it. The output of a regression uses the identity function.",
            r"<b>Applying softmax and then CrossEntropyLoss in PyTorch</b>, which already performs log-softmax internally: the probabilities are computed twice.",
            r"<b>Not scaling the input.</b> Huge $\mathbf{x}$ give huge $\mathbf{z}$, saturate sigmoids and tanh, and break training.",
            r"<b>Believing that the forward pass trains the network.</b> It only computes; the weights are changed by the optimizer step after the backward pass.",
        ]),
    ]),

    dict(id="summary", title="Summary", blocks=[
        ("ul", [
            r"The forward pass: $\mathbf{a}^{(0)} = \mathbf{x}$; for $l = 1..L$: $\mathbf{z}^{(l)} = W^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}$, $\mathbf{a}^{(l)} = f^{(l)}(\mathbf{z}^{(l)})$; the answer is $\hat{\mathbf{y}} = \mathbf{a}^{(L)}$.",
            r"Each row of $W^{(l)}$ is one neuron; a layer is $n_l$ single-neuron formulas at once.",
            r"$W^{(l)}$ has the shape $n_l \times n_{l-1}$; a layer has $n_l(n_{l-1} + 1)$ parameters; the forward pass costs $\sum_l n_l n_{l-1}$ multiplications per object.",
            r"For a batch: $Z^{(l)} = A^{(l-1)}W^{(l)\top} + \mathbf{1}\mathbf{b}^{(l)\top}$.",
            r"Geometrically, the linear part rotates and stretches space and the activation bends it; without activations, the layers collapse into one.",
            r"In training, the forward pass ends with the loss and stores all $\mathbf{z}$ and $\mathbf{a}$ for the backward pass.",
        ]),
    ]),

    dict(id="quiz", title="Test yourself", blocks=[
        ("quiz", [
            dict(q=r"What is the shape of $W^{(l)}$ for a layer with 5 inputs and 3 neurons?", options=[r"$5 \times 3$", r"$3 \times 5$", r"$3 \times 3$", r"$5 \times 5$"], answer=1,
                 explain=r"There are as many rows as neurons ($n_l = 3$) and as many columns as inputs ($n_{l-1} = 5$)."),
            dict(q=r"How many parameters does a 4 → 6 layer have?", options=["24", "28", "30", "34"], answer=2, explain=r"$6\cdot(4 + 1) = 30$: 24 weights and 6 biases."),
            dict(q=r"A layer: $W = \begin{pmatrix}1 & 2\end{pmatrix}$, $b = -1$, ReLU, input $(1,\ -1)$. What is the output?", options=["0", "−2", "2", "1"], answer=0,
                 explain=r"$z = 1 - 2 - 1 = -2$, $\mathrm{ReLU}(-2) = 0$."),
            dict(q=r"What happens if all the activations are removed from a 2–3–2–1 network?", options=["It becomes more accurate", "It becomes equivalent to a single linear layer", "It stops computing", "Nothing changes"], answer=1,
                 explain=r"A composition of linear maps is linear: $W^{(3)}W^{(2)}W^{(1)}\mathbf{x} + \dots$"),
            dict(q=r"How is a layer written for a batch $X$ (objects as rows)?", options=[r"$WX + \mathbf{b}$", r"$XW^{\top} + \mathbf{1}\mathbf{b}^{\top}$", r"$X^{\top}W$", r"$W^{\top}X^{\top}$"], answer=1,
                 explain=r"Each row of $X$ is a vector $\mathbf{x}^{\top}$, and $(W\mathbf{x})^{\top} = \mathbf{x}^{\top}W^{\top}$."),
            dict(q=r"Why are $\mathbf{z}^{(l)}$ and $\mathbf{a}^{(l)}$ stored during training?", options=["For looks", "So that the backward pass can compute the gradients without a second forward pass", "To reduce the loss", "It is only needed for inference"], answer=1,
                 explain=r"The derivatives of the layers are expressed through these values, for example $f'(\mathbf{z}^{(l)})$ and $\mathbf{a}^{(l-1)}$."),
        ]),
    ]),
]

UZ = [
    dict(id="idea", title="To‘g‘ri o‘tish nima", blocks=[
        ("p", r"<a href='../neuron/'>Bitta neyron haqidagi maqolada</a> biz $a = f(\mathbf{w}^{\top}\mathbf{x} + b)$ formulasini tahlil qildik. Haqiqiy tarmoq — qatlamlarga terilgan ko‘plab shunday neyronlar: bir qatlamning chiqishlari keyingisining kirishlariga aylanadi. <b>To‘g‘ri o‘tish</b> (forward pass) — tarmoq javobini hisoblash: kirish chapdan o‘ngga, qatlamma-qatlam, oxirgi qatlamgacha boradi."),
        ("p", r"Butun jarayon uch satrda yoziladi:"),
        ("eq", r"\mathbf{a}^{(0)} = \mathbf{x}"),
        ("eq", r"\mathbf{z}^{(l)} = W^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}, \qquad \mathbf{a}^{(l)} = f^{(l)}\big(\mathbf{z}^{(l)}\big), \qquad l = 1, 2, \dots, L"),
        ("eq", r"\hat{\mathbf{y}} = \mathbf{a}^{(L)}"),
        ("p", r"Buni yo‘riqnoma sifatida o‘qiymiz: kirishni «nolinchi qatlam»ga joylang; har bir qatlamda kelgan narsani vaznlar matritsasiga ko‘paytiring, siljishlarni qo‘shing va aktivatsiya funksiyasidan o‘tkazing; oxirgi qatlamdan chiqqan narsa — javobning o‘zi. Siklni yoyib yozsak, bitta uzun ichma-ich formula hosil bo‘ladi:"),
        ("eq", r"\hat{\mathbf{y}} = f^{(L)}\Big(W^{(L)}\,f^{(L-1)}\big(\cdots f^{(1)}\big(W^{(1)}\mathbf{x} + \mathbf{b}^{(1)}\big)\cdots\big) + \mathbf{b}^{(L)}\Big)"),
        ("viz", "fp-flow", VIZ["flow"], r"<b>1-rasm.</b> 2–3–2–1 tarmog‘ida to‘g‘ri o‘tish. «Qadam» yoki «Boshlash» tugmasini bosing: signal qatlamma-qatlam o‘tadi, har bir neyronda avval $z$, so‘ng $a = f(z)$ paydo bo‘ladi. Ko‘k bog‘lanishlar — musbat vaznlar, qizillari — manfiy vaznlar, qalinlik — vazn moduli. Kirish slayderlarini suring: $\hat y$ javob darhol qayta hisoblanadi."),
        ("callout", "intuition", "O‘xshatish", r"Zavoddagi konveyer. Xomashyo ($\mathbf{x}$ kirish) dastgohlardan (qatlamlardan) o‘tadi. Har bir dastgoh bir xil ishni bajaradi: kelgan detallarni kerakli nisbatlarda aralashtiradi ($W$ matritsa), o‘z qo‘shimchasini qo‘shadi ($\mathbf{b}$ siljish) va natijaga ishlov beradi ($f$ aktivatsiya). Hech bir dastgoh yakuniy mahsulot haqida bilmaydi — u faqat oldingisidan kelgan narsani ko‘radi. Oxirgi dastgoh chiqishidagi mahsulot — tarmoq javobi."),
        ("callout", "key", "Asosiysi", r"To‘g‘ri o‘tish tarmoqni o‘qitmaydi va uning vaznlarini o‘zgartirmaydi — u faqat joriy vaznlarda javobni hisoblaydi. O‘qitish keyin boshlanadi: javob to‘g‘ri javob bilan solishtiriladi (yo‘qotish funksiyasi), teskari o‘tish esa vaznlarni qanday tuzatish kerakligini hisoblaydi."),
    ]),

    dict(id="anatomy", title="Formula mayda detallarigacha: har bir belgi", blocks=[
        ("p", r"To‘g‘ri o‘tishning barcha belgilari va ularning o‘lchamlari. $l$ qatlamdagi neyronlar sonini $n_l$ bilan belgilaymiz; $n_0$ — kirishlar soni."),
        ("symbols", [
            (r"l", r"<b>qatlam raqami</b>: $l = 1, \dots, L$; qavs ichidagi $^{(l)}$ yuqori indeks daraja emas, balki «$l$ qatlamga tegishli» degani;"),
            (r"L", r"<b>vaznli qatlamlar soni</b> (tarmoq chuqurligi); kirish «qatlami» $0$ ning vaznlari yo‘q;"),
            (r"\mathbf{a}^{(l-1)}", r"$l$ <b>qatlamning kirishi</b> — oldingi qatlamning chiqishi, $n_{l-1}$ uzunlikdagi vektor; $\mathbf{a}^{(0)} = \mathbf{x}$;"),
            (r"W^{(l)}", r"qatlamning <b>vaznlar matritsasi</b>: $n_l$ ta satr va $n_{l-1}$ ta ustun; $j$-satr — $j$-neyronning vaznlari;"),
            (r"W^{(l)}_{jk}", r"<b>bitta vazn</b>: $l-1$ qatlamning $k$ neyronidan $l$ qatlamning $j$ neyroniga (avval «qayerga», keyin «qayerdan»);"),
            (r"\mathbf{b}^{(l)}", r"$n_l$ uzunlikdagi <b>siljishlar vektori</b> — har bir neyronga bittadan;"),
            (r"\mathbf{z}^{(l)}", r"qatlamning <b>predaktivatsiyalari</b>, $n_l$ uzunlikdagi vektor: uning barcha neyronlarining vaznli yig‘indilari;"),
            (r"f^{(l)}", r"qatlamning <b>aktivatsiya funksiyasi</b>; har bir koordinataga alohida qo‘llaniladi;"),
            (r"\mathbf{a}^{(l)}", r"<b>qatlam chiqishi</b> (aktivatsiyalar), $n_l$ uzunlikdagi vektor;"),
            (r"\hat{\mathbf{y}}", r"<b>tarmoq javobi</b>: oxirgi qatlamning chiqishi $\mathbf{a}^{(L)}$."),
        ]),
        ("h3", "Bitta qatlam — bir yo‘la ko‘plab neyronlar"),
        ("p", r"Formulaning birinchi satrini koordinatalar bo‘yicha yozib chiqamiz. $l$ qatlamning $j$ neyroni yakka neyron hisoblaydigan formulaning aynan o‘zini hisoblaydi: kirishlarning vaznli yig‘indisi va o‘z siljishi."),
        ("eq", r"z^{(l)}_j = \sum_{k=1}^{n_{l-1}} W^{(l)}_{jk}\,a^{(l-1)}_k + b^{(l)}_j, \qquad a^{(l)}_j = f^{(l)}\big(z^{(l)}_j\big), \qquad j = 1, \dots, n_l"),
        ("p", r"$W^{(l)}\mathbf{a}^{(l-1)}$ matritsa yozuvi — barcha $n_l$ ta shunday yig‘indini bitta amalda hisoblash usuli, xolos: matritsaning $j$-satri kirishlar vektoriga ko‘paytirilsa, $z_j$ hosil bo‘ladi. Shuning uchun to‘g‘ri o‘tish formulasi — qatlamning barcha neyronlariga qo‘llanilgan va barcha qatlamlar uchun takrorlangan bitta neyron formulasi."),
        ("h3", "Misolimizdagi o‘lchamlar"),
        ("p", r"Bundan keyingi butun matn bitta tarmoqqa tayanadi: 2 ta kirish, ReLU’li 3 va 2 neyronli yashirin qatlamlar, sigmoidali bitta chiqish neyroni (2–3–2–1 tarmog‘i)."),
        ("table", ["$l$ qatlam", r"$n_{l-1} \to n_l$", r"$W^{(l)}$", r"$\mathbf{b}^{(l)}$", r"$f^{(l)}$", "Parametrlar"], [
            ["1", "2 → 3", "3 × 2", "3", "ReLU", "3·2 + 3 = 9"],
            ["2", "3 → 2", "2 × 3", "2", "ReLU", "2·3 + 2 = 8"],
            ["3", "2 → 1", "1 × 2", "1", "sigmoida", "1·2 + 1 = 3"],
            ["<b>jami</b>", "", "", "", "", "<b>20</b>"],
        ], {"num": [0]}),
        ("callout", "key", "Hisoblash qoidasi", r"$n_{l-1}\to n_l$ qatlamda aynan $n_l\,(n_{l-1} + 1)$ ta parametr bor: $n_l n_{l-1}$ ta vazn va $n_l$ ta siljish. Butun tarmoqda — qatlamlar bo‘yicha yig‘indi."),
    ]),

    dict(id="numbers", title="Sonlarda to‘g‘ri o‘tish, qadamma-qadam", blocks=[
        ("p", r"Kirish $\mathbf{x} = (1;\ 2)$. Vaznlar va siljishlar:"),
        ("eq", r"W^{(1)} = \begin{pmatrix} 1 & -1\\ 0{,}5 & 1\\ -1 & 2 \end{pmatrix},\ \mathbf{b}^{(1)} = \begin{pmatrix} 0{,}5\\ -1\\ 0 \end{pmatrix};\quad W^{(2)} = \begin{pmatrix} 1 & 0{,}5 & -0{,}5\\ -1 & 1 & 0{,}5 \end{pmatrix},\ \mathbf{b}^{(2)} = \begin{pmatrix} 0\\ 0{,}5 \end{pmatrix};\quad W^{(3)} = \begin{pmatrix} 2 & -0{,}5 \end{pmatrix},\ b^{(3)} = 1"),
        ("h3", "1-qatlam: ikki sondan — uchta"),
        ("eq", r"\mathbf{z}^{(1)} = \begin{pmatrix} 1\cdot1 + (-1)\cdot2 + 0{,}5\\ 0{,}5\cdot1 + 1\cdot2 - 1\\ (-1)\cdot1 + 2\cdot2 + 0 \end{pmatrix} = \begin{pmatrix} -0{,}5\\ 1{,}5\\ 3 \end{pmatrix}, \qquad \mathbf{a}^{(1)} = \mathrm{ReLU}\big(\mathbf{z}^{(1)}\big) = \begin{pmatrix} 0\\ 1{,}5\\ 3 \end{pmatrix}"),
        ("p", r"Birinchi neyron manfiy yig‘indi oldi va ReLU uni «o‘chirdi»: tarmoq bo‘ylab undan keyin nol boradi."),
        ("h3", "2-qatlam: uch sondan — ikkita"),
        ("eq", r"\mathbf{z}^{(2)} = \begin{pmatrix} 1\cdot0 + 0{,}5\cdot1{,}5 - 0{,}5\cdot3 + 0\\ -1\cdot0 + 1\cdot1{,}5 + 0{,}5\cdot3 + 0{,}5 \end{pmatrix} = \begin{pmatrix} -0{,}75\\ 3{,}5 \end{pmatrix}, \qquad \mathbf{a}^{(2)} = \begin{pmatrix} 0\\ 3{,}5 \end{pmatrix}"),
        ("h3", "3-qatlam: ikki sondan — javob"),
        ("eq", r"z^{(3)} = 2\cdot0 - 0{,}5\cdot3{,}5 + 1 = -0{,}75, \qquad \hat y = \sigma(-0{,}75) = \frac{1}{1 + e^{0{,}75}} \approx 0{,}3208"),
        ("viz", "fp-matvec", VIZ["matvec"], r"<b>2-rasm.</b> Har bir qatlam ichida «matritsani vektorga» ko‘paytirish. Qatlamni tanlang va «Qadam» tugmasini bosing: $W$ ning satri (bitta neyron) ajratib ko‘rsatiladi, uning ostida — kirish bilan juft ko‘paytmalar, ularning yig‘indisi, siljish va aktivatsiya. Shunday qilib, $W\mathbf{a} + \mathbf{b}$ — bir vaqtda bajarilgan $n_l$ ta bitta neyron formulasi ekani ko‘rinadi."),
        ("table", ["Qatlam", r"$\mathbf{z}^{(l)}$", r"$\mathbf{a}^{(l)}$"], [
            ["kirish", "—", "(1; 2)"],
            ["1", "(−0,5; 1,5; 3)", "(0; 1,5; 3)"],
            ["2", "(−0,75; 3,5)", "(0; 3,5)"],
            ["3", "−0,75", "0,3208"],
        ], {"num": []}),
        ("callout", "note", "Nimani saqlash kerak", r"O‘qitishda shu jadvaldagi barcha $\mathbf{z}^{(l)}$ va $\mathbf{a}^{(l)}$ eslab qolinadi: teskari o‘tish ulardan to‘g‘ri o‘tishni takrorlamasdan gradiyentlarni hisoblash uchun foydalanadi."),
    ]),

    dict(id="shapes", title="O‘lchamlar: xatolarning yarmini ushlaydigan tekshiruv", blocks=[
        ("p", r"To‘g‘ri o‘tishning har bir amali vektor o‘lchamini oddiy qoida bo‘yicha o‘zgartiradi: $n_l \times n_{l-1}$ matritsa $n_{l-1}$ uzunlikdagi vektorga ko‘paytirilsa, $n_l$ uzunlikdagi vektor hosil bo‘ladi. Tarmog‘imizning o‘lchamlar zanjiri:"),
        ("eq", r"\underbrace{\mathbf{x}}_{2} \xrightarrow{\ W^{(1)}:\,3\times2\ } \underbrace{\mathbf{a}^{(1)}}_{3} \xrightarrow{\ W^{(2)}:\,2\times3\ } \underbrace{\mathbf{a}^{(2)}}_{2} \xrightarrow{\ W^{(3)}:\,1\times2\ } \underbrace{\hat y}_{1}"),
        ("p", r"$W^{(l)}$ ustunlarining soni qatlam kirishining uzunligiga mos kelishi shart, satrlar soni esa chiqish uzunligini belgilaydi. Agar ular mos kelmasa, kod shakl xatosi bilan to‘xtaydi — va bu yaxshi: shakllar tasodifan mos kelib, ma’no chalkashib ketgani yomonroq (masalan, kvadrat matritsada $W^{\top}$ o‘rniga $W$)."),
        ("viz", "fp-shapes", VIZ["shapes"], r"<b>3-rasm.</b> Arxitektura konstruktori. Qatlamlar o‘lchamlarini chiziqcha orqali kiriting yoki tayyor variantni tanlang: jadval $W^{(l)}$, $\mathbf{b}^{(l)}$ shakllarini, bitta obyekt uchun parametrlar va ko‘paytirishlar sonini, ustunchalar esa parametrlar qayerda to‘planganini ko‘rsatadi."),
        ("callout", "key", "To‘g‘ri o‘tish narxi", r"Bitta obyekt uchun qatlam $n_l\cdot n_{l-1}$ ta qo‘shishli ko‘paytirish sarflaydi — har bir vaznga bittadan. Demak, butun to‘g‘ri o‘tish taxminan tarmoqdagi vaznlar soncha amal talab qiladi: $\sum_l n_l\,n_{l-1}$. Bizning tarmoq uchun bu $6 + 6 + 2 = 14$ ta ko‘paytirish."),
    ]),

    dict(id="geometry", title="Geometriya: qatlam fazo bilan nima qiladi", blocks=[
        ("p", r"Qatlamga fazoni almashtirish sifatida qaraymiz. $W\mathbf{a} + \mathbf{b}$ chiziqli qismi fazoni buradi, cho‘zadi, qiyshaytiradi va suradi: to‘g‘ri chiziqlar to‘g‘riligicha, parallellar parallelligicha qoladi, to‘r kataklari bir xil parallelogrammlarga aylanadi. So‘ng aktivatsiya uni egadi: ReLU manfiy sohaga tushgan hamma narsani o‘qlarga taxlaydi, sigmoida va tanh esa uzoqdagi nuqtalarni chetlarga siqadi."),
        ("viz", "fp-space", VIZ["space"], r"<b>4-rasm.</b> 2 → 2 qatlami tekislikni qanday egadi. Slayder to‘rni bosqichlar bo‘ylab ravon olib o‘tadi: dastlabki tekislik → $W\mathbf{x} + \mathbf{b}$ chiziqli qismi → aktivatsiya. Rangli nuqtalar — ikki sinf obyektlari: egilgandan keyin ularni to‘g‘ri chiziq bilan ajratish mumkin bo‘lib qolishini kuzating, holbuki kirishda buning iloji yo‘q edi. Aktivatsiyani va tayyor matritsalarni tanlang."),
        ("p", r"Chuqurlikning asosiy ma’nosi shundan kelib chiqadi: har bir qatlam fazoni biroz qayta bichadi va oxirgi qatlamga kelib turli sinflarning nuqtalari oddiy chegaraning turli tomonlarida bo‘lib qoladi. Oxirgi qatlam — odatiy chiziqli klassifikator yoki regressiya, lekin u oldingi qatlamlar u uchun tayyorlab bergan fazoda ishlaydi."),
        ("deep", "Nega aktivatsiyalarsiz qatlamlar bittaga qo‘shilib ketadi", [
            ("p", r"Agar $f$ ni olib tashlasak, ikki qatlam $W^{(2)}(W^{(1)}\mathbf{x} + \mathbf{b}^{(1)}) + \mathbf{b}^{(2)} = (W^{(2)}W^{(1)})\mathbf{x} + (W^{(2)}\mathbf{b}^{(1)} + \mathbf{b}^{(2)})$ ni beradi — bu yana bitta chiziqli qatlam. Nochiziqliliksiz har qanday chuqurlik bitta qatlamga teng: bir necha marta burilgan parallelogrammlar parallelogrammligicha qoladi. Batafsil — <a href='../neuron/#activation'>bitta neyron haqidagi maqolada</a>."),
        ]),
    ]),

    dict(id="batch", title="Obyektlar paketi: ko‘p kirishlar uchun o‘sha formula", blocks=[
        ("p", r"Amalda tarmoq birdaniga $N$ ta obyektdan iborat paketni (batch) hisoblaydi. Ular satrlar qilib $N \times n_0$ o‘lchamli $X$ matritsaga yig‘iladi va to‘g‘ri o‘tish matritsalar uchun qayta yoziladi:"),
        ("eq", r"A^{(0)} = X, \qquad Z^{(l)} = A^{(l-1)}\,W^{(l)\top} + \mathbf{1}\,\mathbf{b}^{(l)\top}, \qquad A^{(l)} = f^{(l)}\big(Z^{(l)}\big)"),
        ("p", r"$A^{(l)}$ matritsaning $k$-satri — $k$ obyekt uchun $\mathbf{a}^{(l)}$; transponirlash obyektlar endi ustunlar emas, satrlar bo‘lib joylashgani uchun paydo bo‘ldi. $\mathbf{1}\mathbf{b}^{\top}$ qo‘shiluvchi siljishlarni har bir satrga qo‘shadi (NumPy va PyTorch’da buni broadcasting bajaradi). Tarmog‘imiz orqali o‘tgan uch obyektli paket:"),
        ("table", ["Obyekt", r"$\mathbf{x}$", r"$\mathbf{z}^{(1)}$", r"$\mathbf{z}^{(2)}$", r"$z^{(3)}$", r"$\hat y$"], [
            ["1", "(1; 2)", "(−0,5; 1,5; 3)", "(−0,75; 3,5)", "−0,75", "0,3208"],
            ["2", "(0; 0)", "(0,5; −1; 0)", "(0,5; 0)", "2", "0,8808"],
            ["3", "(2; −1)", "(3,5; −1; −4)", "(3,5; −3)", "8", "0,9997"],
        ], {"num": [4, 5]}),
        ("p", r"Ikkinchi obyekt — nol kirish: tarmoq unga beradigan butun javobni faqat siljishlar belgilaydi. E’tibor bering: $0{,}8808$ javobi — bu $\sigma(2)$, ya’ni bitta neyron haqidagi maqoladagi o‘sha son."),
        ("callout", "intuition", "Paketlar nima uchun kerak", r"Protsessor va ayniqsa videokarta uchun $N \times n$ matritsani $n \times m$ matritsaga bitta ko‘paytirish vektorni matritsaga $N$ marta ko‘paytirishdan ancha foydaliroq: ma’lumotlar xotiradan bir marta o‘qiladi va parallel qayta ishlanadi. Shuning uchun o‘qitish ham, xulosa chiqarish ham paketlar bilan bajariladi."),
    ]),

    dict(id="training", title="O‘qitishdagi to‘g‘ri o‘tish: yo‘qotish va kesh", blocks=[
        ("p", r"O‘qitish paytida to‘g‘ri o‘tish $\hat y$ da emas, balki javobni to‘g‘ri $y$ bilan solishtiradigan $L$ yo‘qotish sonida tugaydi. $y = 1$ belgili obyektimiz va binar kross-entropiya uchun:"),
        ("eq", r"L = -\big[y\ln\hat y + (1 - y)\ln(1 - \hat y)\big] = -\ln 0{,}3208 \approx 1{,}1369"),
        ("p", r"To‘g‘ri javob $1$ bo‘lganda $0{,}32$ javobi — yomon, yo‘qotish esa katta. Uni kamaytirish uchun har bir vazn $L$ ga qanday ta’sir qilishini tushunish kerak. Bu bilan teskari o‘tish shug‘ullanadi: u tarmoq bo‘ylab o‘ngdan chapga yuradi va zanjir qoidasiga ko‘ra qatlamlar hosilalarini ko‘paytiradi. Buning uchun unga to‘g‘ri o‘tish hisoblagan aynan o‘sha $\mathbf{z}^{(l)}$ va $\mathbf{a}^{(l)}$ kerak — shuning uchun ular keshlanadi."),
        ("table", ["Rejim", "To‘g‘ri o‘tish nimani hisoblaydi", "Nimani saqlaydi"], [
            ["o‘qitish", r"$\hat y$ javob va $L$ yo‘qotish", r"teskari o‘tish uchun barcha $\mathbf{z}^{(l)}$, $\mathbf{a}^{(l)}$"],
            ["xulosa chiqarish (inference)", r"faqat $\hat y$ javob", "ortiqcha hech narsa: oraliq qiymatlar darhol tashlab yuboriladi"],
        ], {"num": []}),
        ("callout", "note", None, r"Aynan shuning uchun o‘qitish xulosa chiqarishdan ancha ko‘p xotira talab qiladi: har bir qadamda xotirada butun paket uchun barcha qatlamlarning aktivatsiyalari turadi. PyTorch’da xulosa chiqarish rejimi <code>torch.no_grad()</code> yoki <code>torch.inference_mode()</code> orqali yoqiladi."),
    ]),

    dict(id="playground", title="Sinov maydoni: to‘g‘ri o‘tishni o‘zingiz yig‘ing", blocks=[
        ("p", r"Hammasi birga — bitta interaktiv modelda. Chapda — har bir neyron qiymatlari ko‘rsatilgan tarmoq, o‘ngda — tekislikdagi barcha kirishlar uchun $\hat y$ javob xaritasi: $(x_1;\ x_2)$ nuqtaning rangi tarmoq nima javob berishini ko‘rsatadi. Kirishni, qatlamlarning aktivatsiya funksiyalarini va vaznlar masshtabini o‘zgartiring — bitta son ham, butun xarita ham qanday o‘zgarishini kuzating."),
        ("viz", "fp-playground", VIZ["play"], r"<b>5-rasm.</b> To‘g‘ri o‘tish sinov maydoni. Xaritadagi nuqtani torting yoki slayderlarni suring — tarmoqdagi qiymatlar qayta hisoblanadi. Yashirin qatlamlar aktivatsiyalarini almashtiring: ayniy funksiyada xaritadagi chegara to‘g‘ri chiziqqa aylanadi (tarmoq bitta chiziqli qatlamga qo‘shilib ketadi), ReLU bilan — siniq chiziqqa, tanh va sigmoida bilan — silliq chiziqqa. «Vaznlar masshtabi» slayderi barcha vaznlarni ko‘paytiradi: katta vaznlar o‘tishlarni keskin qiladi."),
    ]),

    dict(id="code", title="Kod: to‘g‘ri o‘tish o‘z qo‘limiz bilan va PyTorch’da", blocks=[
        ("p", r"To‘g‘ri o‘tish — qatlamlar bo‘yicha sikl. Quyida u to‘liq keltirilgan: teskari o‘tish uchun kesh bilan va paket uchun versiya bilan."),
        ("code", "python", CODE_NUMPY["uz"]),
        ("p", r"PyTorch’da ham xuddi shunday: <code>nn.Linear</code> $W$ va $\mathbf{b}$ ni saqlaydi va $\mathbf{x}W^{\top} + \mathbf{b}$ ni hisoblaydi, <code>nn.Sequential</code> esa qatlamlar bo‘yicha siklning o‘zi."),
        ("code", "python", CODE_TORCH["uz"]),
    ]),

    dict(id="practice", title="Amaliyot: 8 ta misol", blocks=[
        ("p", r"Har bir misol to‘g‘ri o‘tishning bitta qirrasini ko‘rsatadi. Barcha sonlar hisoblash orqali tekshirilgan."),
        ("example", dict(n=1, title="Bitta qatlam — bu logistik regressiya", kinds=["hisob"],
            goal=r"$L = 1$ da to‘g‘ri o‘tish bitta neyron formulasiga aylanishini ko‘rish va yangi maqolani oldingisi bilan bog‘lash.",
            blocks=[
                ("p", r"Sigmoidali 3–1 tarmog‘i: $W^{(1)} = (0{,}5\ \ -1\ \ 0{,}25)$, $b^{(1)} = -0{,}75$, kirish $\mathbf{x} = (2;\ -1;\ 3)$."),
                ("eq", r"\hat y = \sigma\big(W^{(1)}\mathbf{x} + b^{(1)}\big) = \sigma(1 + 1 + 0{,}75 - 0{,}75) = \sigma(2) \approx 0{,}8808"),
            ],
            take=r"Sigmoidali bir qatlamli tarmoq — bu logistik regressiya; chuqur tarmoq — $L$ marta takrorlangan o‘sha formula.")),
        ("example", dict(n=2, title="XOR: yashirin qatlam orqali to‘g‘ri o‘tish", kinds=["jadval"],
            goal=r"To‘rtta kirishda to‘g‘ri o‘tishni bajarib, ReLU’li yashirin qatlam bitta neyron uddalay olmaydigan narsani qanday mumkin qilishini ko‘rish.",
            blocks=[
                ("p", r"2–2–1 tarmog‘i: $h_1 = \mathrm{ReLU}(x_1 + x_2)$, $h_2 = \mathrm{ReLU}(x_1 + x_2 - 1)$, chiqish chiziqli: $\hat y = h_1 - 2h_2$."),
                ("table", [r"$(x_1;\ x_2)$", r"$\mathbf{z}^{(1)}$", r"$\mathbf{a}^{(1)}$", r"$\hat y$", "XOR"], [
                    ["(0; 0)", "(0; −1)", "(0; 0)", "0", "0"],
                    ["(0; 1)", "(1; 0)", "(1; 0)", "1", "1"],
                    ["(1; 0)", "(1; 0)", "(1; 0)", "1", "1"],
                    ["(1; 1)", "(2; 1)", "(2; 1)", "0", "0"],
                ], {"num": [3, 4]}),
            ],
            take=r"Ikkinchi neyron faqat ikkala kirish birga teng bo‘lganda yonadi va ortiqchasini ayiradi. ReLU bo‘lmaganda chiqish chiziqli bo‘lardi va XOR hosil bo‘lmasdi.")),
        ("example", dict(n=3, title="MNIST uchun tarmoqning shakllari va parametrlari", kinds=["jadval", "hisob"],
            goal=r"Haqiqiy tarmoqning barcha matritsalari shakllarini va parametrlar sonini bir daqiqada hisoblashni o‘rganish.",
            blocks=[
                ("p", r"28×28 rasm 784 ta sondan iborat vektorga yoyiladi; 784–128–64–10 tarmog‘i 10 ta son chiqaradi — har bir raqamga bittadan."),
                ("table", ["Qatlam", r"$W^{(l)}$", r"$\mathbf{b}^{(l)}$", "Parametrlar", "Ko‘paytirishlar"], [
                    ["1", "128 × 784", "128", "100 480", "100 352"],
                    ["2", "64 × 128", "64", "8 256", "8 192"],
                    ["3", "10 × 64", "10", "650", "640"],
                    ["<b>jami</b>", "", "", "<b>109 386</b>", "<b>109 184</b>"],
                ], {"num": [3, 4]}),
            ],
            take=r"Parametrlarning 90% dan ortig‘i kirishlar ko‘p bo‘lgan birinchi qatlamda joylashgan. Bitta obyektga to‘g‘ri keladigan ko‘paytirishlar soni vaznlar soniga deyarli teng.")),
        ("example", dict(n=4, title="Bir nechta sinfli chiqish: softmax", kinds=["hisob"],
            goal=r"Oxirgi qatlam $n_L$ ta sonni ehtimolliklar taqsimotiga qanday aylantirishini ko‘rish.",
            blocks=[
                ("p", r"$K$ ta sinf uchun oxirgi qatlam $K$ ta $\mathbf{z}^{(L)}$ sonini chiqaradi, aktivatsiya vazifasini esa softmax bajaradi: $\hat y_k = e^{z_k} / \sum_j e^{z_j}$. $\mathbf{z}^{(L)} = (2;\ 1;\ 0{,}1)$ bo‘lganda:"),
                ("eq", r"e^{\mathbf{z}} \approx (7{,}3891;\ 2{,}7183;\ 1{,}1052), \quad \sum \approx 11{,}2125, \quad \hat{\mathbf{y}} \approx (0{,}6590;\ 0{,}2424;\ 0{,}0986)"),
            ],
            take=r"Softmax — elementma-element aktivatsiya emas: har bir chiqish barcha $z$ larga bog‘liq. Ehtimolliklar yig‘indisi doim 1 ga teng.")),
        ("example", dict(n=5, title="Nol kirish va siljishlarning roli", kinds=["hisob"],
            goal=r"Siljishlar tarmoqning «sukut bo‘yicha» javobini belgilashini tushunish.",
            blocks=[
                ("p", r"Tarmog‘imizga $\mathbf{x} = (0;\ 0)$ ni beramiz. U holda $\mathbf{z}^{(1)} = \mathbf{b}^{(1)} = (0{,}5;\ -1;\ 0)$, $\mathbf{a}^{(1)} = (0{,}5;\ 0;\ 0)$, $\mathbf{z}^{(2)} = (0{,}5;\ 0)$, $\mathbf{a}^{(2)} = (0{,}5;\ 0)$, $z^{(3)} = 2\cdot0{,}5 + 1 = 2$, $\hat y = \sigma(2) \approx 0{,}8808$."),
            ],
            take=r"Siljishlar bo‘lmaganda nol kirish har bir qatlamda doim $\mathbf{z} = \mathbf{0}$ va $\hat y = \sigma(0) = 0{,}5$ ni bergan bo‘lardi — tarmoq nimani o‘rganmasin.")),
        ("example", dict(n=6, title="«O‘chirilgan» neyronlar: ReLU oqim bilan nima qiladi", kinds=["hisob"],
            goal=r"$a = 0$ bo‘lgan neyron o‘z shoxobchasini butunlay uzib qo‘yishini ko‘rish: uning chiquvchi vaznlari javobga ta’sir qilmaydi.",
            blocks=[
                ("p", r"Misolimizda 2-qatlamning birinchi neyroni $a^{(2)}_1 = 0$ ni chiqardi ($z = -0{,}75$). Uning chiqish qatlamidagi vazni $W^{(3)}_{11} = 2$. Uni $100$ ga yoki $-100$ ga almashtiramiz: $z^{(3)} = 100\cdot0 - 0{,}5\cdot3{,}5 + 1 = -0{,}75$ — javob o‘zgarmaydi."),
            ],
            take=r"Berilgan kirishda tarmoqning faqat bir qismi ishlaydi. Boshqa kirish uchun boshqa neyronlar yonadi — ReLU tarmog‘i javobni har biri chiziqli bo‘lgan bo‘laklardan shu tarzda tuzadi.")),
        ("example", dict(n=7, title="Chuqurlikmi yoki kenglik", kinds=["jadval"],
            goal=r"Kenglik qanchaga va chuqurlik qanchaga tushishini solishtirish.",
            blocks=[
                ("table", ["Tarmoq", "Qatlamlar", "Parametrlar"], [
                    ["2–100–1", "1 ta yashirin, keng", "2·100 + 100 + 100 + 1 = 401"],
                    ["2–10–10–10–1", "3 ta yashirin, tor", "30 + 110 + 110 + 11 = 261"],
                ], {"num": []}),
            ],
            take=r"Chuqur tor tarmoq keng sayoz tarmoqdan arzonroq bo‘lishi va shu bilan birga murakkabroq funksiyalarni qurishi mumkin: har bir qatlam fazoni qaytadan taxlaydi va «sinish»lar soni kenglikka qaraganda chuqurlik bilan tezroq o‘sadi.")),
        ("example", dict(n=8, title="Sonli barqarorlik: to‘g‘ri o‘tish qayerda buziladi", kinds=["hisob", "kod"],
            goal=r"To‘g‘ri o‘tishda NaN olishning ikkita klassik yo‘lini va ularni qanday chetlab o‘tishni bilib olish.",
            blocks=[
                ("p", r"$\mathbf{z} = (1000;\ 1001;\ 1002)$ bo‘lgan softmax: $e^{1000}$ suzuvchi nuqtali songa sig‘maydi va $\infty/\infty = $ NaN hosil bo‘ladi. Lekin barcha $z$ lardan bir xil son ayirilsa, softmax o‘zgarmaydi. Maksimumni ayiramiz:"),
                ("eq", r"\mathbf{z} - 1002 = (-2;\ -1;\ 0), \quad e^{\mathbf{z} - \max} \approx (0{,}1353;\ 0{,}3679;\ 1), \quad \hat{\mathbf{y}} \approx (0{,}0900;\ 0{,}2447;\ 0{,}6652)"),
                ("p", r"Sigmoida bilan ham shunday: $z = -1000$ da sodda $1/(1 + e^{1000})$ formulasi to‘lib ketadi. Barqaror versiya manfiy $z$ lar uchun $e^{z}/(1 + e^{z})$ ni hisoblaydi. Klassifikator chiqishida esa yo‘qotishga ehtimolliklar emas, $\mathbf{z}^{(L)}$ logitlar beriladi: <code>BCEWithLogitsLoss</code>, <code>CrossEntropyLoss</code>."),
            ],
            take=r"Matematik jihatdan to‘g‘ri o‘tish formulasi istalgan sonlar uchun to‘g‘ri, mashinada esa — yo‘q. Barqaror versiyalar ayni narsani hisoblaydi, lekin xavfsiz tartibda.")),
    ]),

    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ul", [
            r"<b>Indekslar tartibini adashtirish.</b> $W^{(l)}_{jk}$ — «$k$ neyrondan $j$ neyronga». Matritsaning shakli $n_l \times n_{l-1}$, PyTorch’da — <code>(out_features, in_features)</code>.",
            r"<b>$W\mathbf{x}$ o‘rniga $\mathbf{x}W$.</b> Bitta ustun-vektor uchun — $W\mathbf{x}$; satrlar ko‘rinishidagi paket uchun — $XW^{\top}$. Ularni aralashtirish shakl xatosiga yoki, undan ham yomoni, kvadrat matritsalarda noto‘g‘ri javobga olib keladi.",
            r"<b>Qatlamlar orasidagi aktivatsiyani unutish.</b> Tarmoq jimgina bitta chiziqli qatlamga qo‘shilib ketadi.",
            r"<b>Javob manfiy bo‘lishi mumkin bo‘lgan regressiya chiqishiga ReLU qo‘yish</b>: tarmoq bunday javobni jismonan chiqara olmaydi. Regressiya chiqishida — ayniy funksiya.",
            r"<b>PyTorch’da softmax qo‘llab, so‘ng CrossEntropyLoss ishlatish</b> — u log-softmax ni ichida allaqachon bajaradi: ehtimolliklar ikki marta hisoblanadi.",
            r"<b>Kirishni masshtablamaslik.</b> Juda katta $\mathbf{x}$ juda katta $\mathbf{z}$ beradi, sigmoida va tanh ni to‘yintiradi va o‘qitishni buzadi.",
            r"<b>To‘g‘ri o‘tish tarmoqni o‘qitadi deb hisoblash.</b> U faqat hisoblaydi; vaznlarni teskari o‘tishdan keyin optimizator qadami o‘zgartiradi.",
        ]),
    ]),

    dict(id="summary", title="Xulosa", blocks=[
        ("ul", [
            r"To‘g‘ri o‘tish: $\mathbf{a}^{(0)} = \mathbf{x}$; $l = 1..L$ uchun: $\mathbf{z}^{(l)} = W^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}$, $\mathbf{a}^{(l)} = f^{(l)}(\mathbf{z}^{(l)})$; javob $\hat{\mathbf{y}} = \mathbf{a}^{(L)}$.",
            r"$W^{(l)}$ ning har bir satri — bitta neyron; qatlam — bir yo‘la bajariladigan $n_l$ ta bitta neyron formulasi.",
            r"$W^{(l)}$ ning shakli $n_l \times n_{l-1}$; qatlamda $n_l(n_{l-1} + 1)$ ta parametr bor; to‘g‘ri o‘tish har bir obyekt uchun $\sum_l n_l n_{l-1}$ ta ko‘paytirish talab qiladi.",
            r"Paket uchun: $Z^{(l)} = A^{(l-1)}W^{(l)\top} + \mathbf{1}\mathbf{b}^{(l)\top}$.",
            r"Geometrik jihatdan chiziqli qism fazoni buradi va cho‘zadi, aktivatsiya esa uni egadi; aktivatsiyalarsiz qatlamlar bittaga qo‘shilib ketadi.",
            r"O‘qitishda to‘g‘ri o‘tish yo‘qotish bilan tugaydi va teskari o‘tish uchun barcha $\mathbf{z}$ va $\mathbf{a}$ ni saqlaydi.",
        ]),
    ]),

    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q=r"5 ta kirish va 3 ta neyronli qatlamning $W^{(l)}$ matritsasi qanday shaklga ega?", options=[r"$5 \times 3$", r"$3 \times 5$", r"$3 \times 3$", r"$5 \times 5$"], answer=1,
                 explain=r"Satrlar neyronlar soncha ($n_l = 3$), ustunlar esa kirishlar soncha ($n_{l-1} = 5$)."),
            dict(q=r"4 → 6 qatlamida nechta parametr bor?", options=["24", "28", "30", "34"], answer=2, explain=r"$6\cdot(4 + 1) = 30$: 24 ta vazn va 6 ta siljish."),
            dict(q=r"Qatlam: $W = \begin{pmatrix}1 & 2\end{pmatrix}$, $b = -1$, ReLU, kirish $(1;\ -1)$. Chiqish nimaga teng?", options=["0", "−2", "2", "1"], answer=0,
                 explain=r"$z = 1 - 2 - 1 = -2$, $\mathrm{ReLU}(-2) = 0$."),
            dict(q=r"2–3–2–1 tarmog‘idan barcha aktivatsiyalarni olib tashlasak, nima bo‘ladi?", options=["U aniqroq bo‘ladi", "U bitta chiziqli qatlamga ekvivalent bo‘lib qoladi", "U hisoblay olmay qoladi", "Hech narsa o‘zgarmaydi"], answer=1,
                 explain=r"Chiziqli almashtirishlar kompozitsiyasi chiziqli: $W^{(3)}W^{(2)}W^{(1)}\mathbf{x} + \dots$"),
            dict(q=r"$X$ paket (obyektlar satrlarda) uchun qatlam qanday yoziladi?", options=[r"$WX + \mathbf{b}$", r"$XW^{\top} + \mathbf{1}\mathbf{b}^{\top}$", r"$X^{\top}W$", r"$W^{\top}X^{\top}$"], answer=1,
                 explain=r"$X$ ning har bir satri — $\mathbf{x}^{\top}$ vektor, va $(W\mathbf{x})^{\top} = \mathbf{x}^{\top}W^{\top}$."),
            dict(q=r"O‘qitishda $\mathbf{z}^{(l)}$ va $\mathbf{a}^{(l)}$ ni nima uchun saqlash kerak?", options=["Chiroy uchun", "Teskari o‘tish gradiyentlarni to‘g‘ri o‘tishni takrorlamasdan hisoblashi uchun", "Yo‘qotishni kamaytirish uchun", "Bu faqat xulosa chiqarishda kerak"], answer=1,
                 explain=r"Qatlamlar hosilalari shu qiymatlar orqali ifodalanadi, masalan, $f'(\mathbf{z}^{(l)})$ va $\mathbf{a}^{(l-1)}$."),
        ]),
    ]),
]


SECTIONS = {"ru": RU, "en": EN, "uz": UZ}


def check_numbers():
    import math
    sig = lambda z: 1 / (1 + math.exp(-z))
    relu = lambda v: [max(0.0, t) for t in v]
    mv = lambda W, a, b: [sum(w * x for w, x in zip(row, a)) + bb for row, bb in zip(W, b)]
    W, B = NET["W"], NET["b"]
    def fwd(x):
        z1 = mv(W[0], x, B[0]); a1 = relu(z1)
        z2 = mv(W[1], a1, B[1]); a2 = relu(z2)
        z3 = mv(W[2], a2, B[2])[0]
        return z1, a1, z2, a2, z3, sig(z3)
    z1, a1, z2, a2, z3, y = fwd(NET["x"])
    assert z1 == [-0.5, 1.5, 3] and a1 == [0, 1.5, 3] and z2 == [-0.75, 3.5] and a2 == [0, 3.5] and z3 == -0.75
    assert round(y, 4) == 0.3208 and round(-math.log(y), 4) == 1.1369
    assert fwd([0, 0])[0] == [0.5, -1, 0] and fwd([0, 0])[2] == [0.5, 0] and fwd([0, 0])[4] == 2 and round(fwd([0, 0])[5], 4) == 0.8808
    t = fwd([2, -1]); assert t[0] == [3.5, -1, -4] and t[2] == [3.5, -3] and t[4] == 8 and round(t[5], 4) == 0.9997
    params = lambda sizes: sum(o * (i + 1) for i, o in zip(sizes, sizes[1:]))
    macs = lambda sizes: sum(o * i for i, o in zip(sizes, sizes[1:]))
    assert params([2, 3, 2, 1]) == 20 and macs([2, 3, 2, 1]) == 14
    assert params([784, 128, 64, 10]) == 109386 and macs([784, 128, 64, 10]) == 109184
    assert [o * (i + 1) for i, o in zip([784, 128, 64], [128, 64, 10])] == [100480, 8256, 650]
    assert params([2, 100, 1]) == 401 and params([2, 10, 10, 10, 1]) == 261
    assert round(sig(2), 4) == 0.8808 and 0.5 * 2 + (-1) * (-1) + 0.25 * 3 - 0.75 == 2
    xr = lambda p, q: (max(0, p + q), max(0, p + q - 1))
    assert [xr(*p)[0] - 2 * xr(*p)[1] for p in [(0, 0), (0, 1), (1, 0), (1, 1)]] == [0, 1, 1, 0]
    e = [math.exp(v) for v in (2, 1, 0.1)]
    assert [round(v, 4) for v in e] == [7.3891, 2.7183, 1.1052] and round(sum(e), 4) == 11.2125
    assert [round(v / sum(e), 4) for v in e] == [0.659, 0.2424, 0.0986]
    e = [math.exp(v - 1002) for v in (1000, 1001, 1002)]
    assert [round(v, 4) for v in e] == [0.1353, 0.3679, 1] and [round(v / sum(e), 4) for v in e] == [0.09, 0.2447, 0.6652]
    return True


if __name__ == "__main__":
    print("numbers ok" if check_numbers() else "")
