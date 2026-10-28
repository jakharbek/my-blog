"""Formula page: the Huber loss. Format: see README.md (reference page: sigmoid.py)."""

META = dict(
    id="huber",
    date="2026-10-28",
    minutes=35,
    hero=r"L_\delta(r)=\begin{cases}\tfrac12 r^2, & |r|\le\delta\\[1mm] \delta\bigl(|r|-\tfrac12\delta\bigr), & |r|>\delta\end{cases}",
    title={"ru": "Функция потерь Хьюбера: мост между MSE и MAE", "en": "The Huber loss: a bridge between MSE and MAE", "uz": "Huber yo‘qotish funksiyasi: MSE va MAE orasidagi ko‘prik"},
    dek={
        "ru": "Парабола в середине и прямые по краям. Разбираем, почему у стыка совпадают и значения, и наклоны, как порог δ обрезает градиент выбросов, чем оценка Хьюбера лучше среднего и медианы, откуда берётся магическое 1,345σ и где эта потеря работает сегодня — от робастной регрессии до Fast R-CNN и DQN.",
        "en": "A parabola in the middle and straight lines at the edges. We look at why both the values and the slopes agree at the seam, how the threshold δ clips the gradient of outliers, why Huber’s estimate beats both the mean and the median, where the magic 1.345σ comes from, and where this loss works today — from robust regression to Fast R-CNN and DQN.",
        "uz": "O‘rtada parabola, chetlarda to‘g‘ri chiziqlar. Tutashuvda nega qiymatlar ham, qiyaliklar ham mos kelishini, δ chegara chetga chiquvchilar gradiyentini qanday kesishini, Huber bahosi nega o‘rtacha va medianadan yaxshiroq ekanini, sehrli 1,345σ qayerdan kelishini va bu yo‘qotish bugun qayerda ishlashini — robast regressiyadan Fast R-CNN va DQN’gacha — tahlil qilamiz.",
    },
    description={
        "ru": "Потеря Хьюбера подробно: формула по косточкам, гладкость стыка, ограниченный градиент ψ(r), 3D-поверхность L(r, δ), оценка центра, выбор δ = 1,345σ, IRLS, градиентный спуск с выбросами, псевдо-Хьюбер, log-cosh, Smooth L1, код NumPy и PyTorch.",
        "en": "The Huber loss in depth: the formula bone by bone, the smooth seam, the bounded gradient ψ(r), the 3D surface L(r, δ), the location estimate, choosing δ = 1.345σ, IRLS, gradient descent with outliers, pseudo-Huber, log-cosh, Smooth L1, NumPy and PyTorch code.",
        "uz": "Huber yo‘qotishi batafsil: formula mayda detallarigacha, silliq tutashuv, chegaralangan ψ(r) gradiyent, L(r, δ) 3D-sirti, markaz bahosi, δ = 1,345σ tanlovi, IRLS, chetga chiquvchilar bilan gradiyent tushish, psevdo-Huber, log-cosh, Smooth L1, NumPy va PyTorch kodi.",
    },
)

# r, ½r², |r|, L_1(r), ψ_1(r)
TABLE = [("0", "0", "0", "0", "0"), ("0.5", "0.125", "0.5", "0.125", "0.5"), ("1", "0.5", "1", "0.5", "1"), ("2", "2", "2", "1.5", "1"),
         ("3", "4.5", "3", "2.5", "1"), ("5", "12.5", "5", "4.5", "1"), ("10", "50", "10", "9.5", "1")]


def _table(lang):
    dec = "." if lang == "en" else ","
    return [[c.replace(".", dec) for c in row] for row in TABLE]


CODE_NUMPY = '''import numpy as np

def huber(r, delta=1.0):
    """Потеря Хьюбера для остатков r = y − ŷ (поэлементно)."""
    a = np.abs(r)
    return np.where(a <= delta, 0.5 * r**2, delta * (a - 0.5 * delta))

def huber_grad(r, delta=1.0):
    """ψ(r) = dL/dr — остаток, обрезанный до [−δ, δ]. По ŷ — со знаком минус."""
    return np.clip(r, -delta, delta)

def pseudo_huber(r, delta=1.0):
    return delta**2 * (np.sqrt(1.0 + (r / delta)**2) - 1.0)

y     = np.array([3.0, 5.0, 8.0])
y_hat = np.array([2.5, 5.0, 10.0])
r = y - y_hat               # [ 0.5  0.  -2. ]
print(huber(r))             # [0.125 0.    1.5  ]
print(huber(r).mean())      # 0.5416666666666666
print(huber_grad(r))        # [ 0.5  0.  -1. ]'''

CODE_IRLS = '''def huber_regression(X, y, delta=1.345, iters=50):
    """Регрессия Хьюбера методом IRLS: МНК с весами w_i = min(1, δ·s/|r_i|)."""
    X1 = np.column_stack([np.ones(len(X)), X])
    beta = np.linalg.lstsq(X1, y, rcond=None)[0]           # старт — обычный МНК
    for _ in range(iters):
        r = y - X1 @ beta
        s = np.median(np.abs(r - np.median(r))) / 0.6745   # робастный масштаб (MAD)
        w = np.minimum(1.0, delta * s / np.maximum(np.abs(r), 1e-12))
        sw = np.sqrt(w)
        beta = np.linalg.lstsq(X1 * sw[:, None], y * sw, rcond=None)[0]
    return beta

rng = np.random.default_rng(0)
x = np.linspace(0, 10, 30)
y = 1 + 0.5 * x + rng.normal(0, 0.5, 30)
y[-3:] -= 6                                                # три выброса
X1 = np.column_stack([np.ones(30), x])
print(np.linalg.lstsq(X1, y, rcond=None)[0].round(3))      # [1.931 0.182] — МНК
print(huber_regression(x, y).round(3))                     # [1.134 0.442] — Хьюбер'''

CODE_TORCH = '''import torch
import torch.nn as nn

y_hat = torch.tensor([2.5, 5.0, 10.0], requires_grad=True)
y = torch.tensor([3.0, 5.0, 8.0])

loss = nn.HuberLoss(delta=1.0)(y_hat, y)   # среднее: 0.5417
loss.backward()
print(y_hat.grad)       # tensor([-0.1667,  0.0000,  0.3333]) = ψ(ŷ − y) / n

# Smooth L1 из Fast R-CNN — это Хьюбер, делённый на β (β = δ):
huber2 = nn.HuberLoss(delta=2.0)(y_hat, y)        # 0.7083
sl1_2 = nn.SmoothL1Loss(beta=2.0)(y_hat, y)       # 0.3542 = 0.7083 / 2'''


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("Потеря Хьюбера для остатков r = y − ŷ (поэлементно).", "Huber loss for the residuals r = y − ŷ (element-wise)."),
               ("ψ(r) = dL/dr — остаток, обрезанный до [−δ, δ]. По ŷ — со знаком минус.", "ψ(r) = dL/dr: the residual clipped to [−δ, δ]. With respect to ŷ the sign flips."),
               ("Регрессия Хьюбера методом IRLS: МНК с весами w_i = min(1, δ·s/|r_i|).", "Huber regression by IRLS: least squares with weights w_i = min(1, δ·s/|r_i|)."),
               ("старт — обычный МНК", "start from ordinary least squares"), ("робастный масштаб (MAD)", "robust scale (MAD)"),
               ("три выброса", "three outliers"), ("— МНК", "— least squares"), ("— Хьюбер", "— Huber"),
               ("среднее: 0.5417", "mean: 0.5417"),
               ("Smooth L1 из Fast R-CNN — это Хьюбер, делённый на β (β = δ):", "Smooth L1 from Fast R-CNN is Huber divided by β (β = δ):")],
        "uz": [("Потеря Хьюбера для остатков r = y − ŷ (поэлементно).", "r = y − ŷ qoldiqlar uchun Huber yo‘qotishi (elementma-element)."),
               ("ψ(r) = dL/dr — остаток, обрезанный до [−δ, δ]. По ŷ — со знаком минус.", "ψ(r) = dL/dr — [−δ, δ] gacha kesilgan qoldiq. ŷ bo‘yicha — minus ishora bilan."),
               ("Регрессия Хьюбера методом IRLS: МНК с весами w_i = min(1, δ·s/|r_i|).", "IRLS usulidagi Huber regressiyasi: w_i = min(1, δ·s/|r_i|) vaznli EKKU."),
               ("старт — обычный МНК", "boshlanish — oddiy EKKU"), ("робастный масштаб (MAD)", "robast masshtab (MAD)"),
               ("три выброса", "uchta chetga chiquvchi"), ("— МНК", "— EKKU"), ("— Хьюбер", "— Huber"),
               ("среднее: 0.5417", "o‘rtacha: 0.5417"),
               ("Smooth L1 из Fast R-CNN — это Хьюбер, делённый на β (β = δ):", "Fast R-CNN’dagi Smooth L1 — β ga bo‘lingan Huber (β = δ):")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", "Регрессия учится на ошибках $r=y-\\hat y$. Две классические потери отвечают на вопрос «как штрафовать ошибку» по-разному. <a href=\"../mse/\">MSE</a> штрафует квадратом: она гладкая, её градиент пропорционален ошибке и плавно затухает у минимума, но один выброс с ошибкой 10 весит как сто ошибок размером 1. <a href=\"../mae/\">MAE</a> штрафует модулем: выбросы ей почти безразличны, зато в нуле у неё излом, а градиент всегда одного размера — модели трудно «доводить» мелкие ошибки."),
        ("p", "Питер Хьюбер в 1964 году предложил взять лучшее от обеих: <b>парабола для малых ошибок и прямая для больших</b>, с переключением на пороге $\\delta$. Где эта идея работает сегодня:"),
        ("ul", [
            "<b>робастная регрессия</b> — <code>HuberRegressor</code> в scikit-learn, M-оценки в статистике;",
            "<b>детекция объектов</b> — Smooth L1 в Fast R-CNN и его потомках для регрессии координат рамок; это Хьюбер с точностью до множителя;",
            "<b>обучение с подкреплением</b> — в DQN ошибку временной разности обрезают до $[-1;\\,1]$, что равносильно потере Хьюбера с $\\delta=1$;",
            "<b>градиентный бустинг</b> — <code>loss='huber'</code> в scikit-learn, <code>objective='huber'</code> в LightGBM, псевдо-Хьюбер в XGBoost;",
            "<b>любые данные с аномалиями</b> — цены недвижимости, показания датчиков, разметка с опечатками.",
        ]),
        ("callout", "key", "Главное за минуту", "$L_\\delta(r)$ равна $\\tfrac12r^2$ при $|r|\\le\\delta$ и $\\delta(|r|-\\tfrac12\\delta)$ дальше. В точке $|r|=\\delta$ совпадают и значения ($\\tfrac12\\delta^2$), и наклоны ($\\delta$). Производная $\\psi(r)=\\operatorname{clip}(r,-\\delta,\\delta)$ ограничена: выброс тянет модель не сильнее, чем на $\\delta$. Малое $\\delta$ — ближе к MAE, большое — к MSE."),
    ]),
    dict(id="intuition", title="Интуиция: парабола с прямыми хвостами", blocks=[
        ("p", "Представьте пружину, которая тянет прогноз к ответу. Пока ошибка мала, пружина обычная: чем дальше растянута, тем сильнее тянет — это парабола $\\tfrac12r^2$. Но у пружины есть предохранитель: после растяжения $\\delta$ сила перестаёт расти и остаётся равной $\\delta$. Энергия такой пружины дальше растёт уже линейно — это прямые хвосты."),
        ("p", "Потяните точку по графику и подвигайте $\\delta$. Синяя кривая лежит на серой параболе внутри бирюзовой полосы $|r|\\le\\delta$ и на пунктирной прямой $\\delta(|r|-\\delta/2)$ снаружи. Оранжевая касательная проходит стык без излома."),
        ("viz", "huber-explorer", {"delta": 1, "r": 2}, "<b>Рисунок 1.</b> Потеря Хьюбера $L_\\delta(r)$ и её производные. Внизу: оранжевая $\\psi(r)=L'_\\delta(r)$ — наклонная внутри полосы и горизонтальная снаружи; фиолетовая $L''_\\delta$ — ступенька: 1 внутри, 0 снаружи. При $\\delta=1$ и $r=2$: $L=1{,}5$ вместо $\\tfrac12r^2=2$, а наклон равен 1, а не 2."),
        ("callout", "intuition", "Что заметить", "На стыке $|r|=\\delta$ кривая переходит с параболы на прямую плавно: прямая $\\delta(|r|-\\delta/2)$ — это <i>касательная</i> к параболе в точке $r=\\pm\\delta$. Излом есть только у второй производной: кривизна прыгает с 1 до 0."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("eq", r"L_\delta(r)=\begin{cases}\tfrac12 r^2, & |r|\le\delta,\\[1mm] \delta\bigl(|r|-\tfrac12\delta\bigr), & |r|>\delta,\end{cases}\qquad r=y-\hat y"),
        ("symbols", [
            (r"r=y-\hat y", "остаток (residual): насколько ответ $y$ выше прогноза $\\hat y$; потеря зависит только от $|r|$, знак не важен;"),
            (r"\delta>0", "порог: ошибки меньше $\\delta$ считаются «обычным шумом», больше — подозрительными; измеряется в единицах $y$;"),
            (r"\tfrac12 r^2", "квадратичная ветвь — ровно половина квадрата ошибки, как в MSE; множитель $\\tfrac12$ делает производную равной $r$;"),
            (r"\delta|r|", "линейная ветвь — модуль ошибки с весом $\\delta$, как в MAE;"),
            (r"-\tfrac12\delta^2", "сдвиг вниз, который сшивает ветви: без него прямая $\\delta|r|$ при $|r|=\\delta$ давала бы $\\delta^2$, а парабола — $\\tfrac12\\delta^2$."),
        ]),
        ("p", "Проверим сшивку. При $|r|=\\delta$ квадратичная ветвь даёт $\\tfrac12\\delta^2$, линейная — $\\delta(\\delta-\\tfrac12\\delta)=\\tfrac12\\delta^2$: значения равны. Производные: $r=\\delta$ у параболы и $\\delta\\operatorname{sign}r=\\delta$ у прямой — равны и наклоны. Константу $-\\tfrac12\\delta^2$ выбрали именно так, чтобы прямая стала касательной к параболе."),
        ("table", ["$r$", "$\\tfrac12r^2$", "$|r|$", "$L_1(r)$", "$\\psi_1(r)$"], "TABLE", {"num": [0, 1, 2, 3, 4]}),
        ("p", "Таблица для $\\delta=1$ показывает главное: при ошибке 10 квадрат даёт 50, а Хьюбер — 9,5; при этом производная (последний столбец) никогда не превышает 1."),
        ("h3", "Сквозной пример"),
        ("p", "Возьмём пример из шпаргалки: $y=(3;\\,5;\\,8)$, $\\hat y=(2{,}5;\\,5;\\,10)$, ошибки $r=(0{,}5;\\,0;\\,-2)$. При $\\delta=1$ первая ошибка попадает в параболу: $\\tfrac12\\cdot0{,}5^2=0{,}125$; вторая — ноль; третья, $|r|=2&gt;1$, — в прямую: $1\\cdot(2-0{,}5)=1{,}5$. Среднее $(0{,}125+0+1{,}5)/3\\approx0{,}542$."),
        ("p", "Интереснее градиенты. В половине MSE они равны самим ошибкам: $(0{,}5;\\,0;\\,-2)$ — выброс тянет вчетверо сильнее первой точки. У Хьюбера $\\psi=(0{,}5;\\,0;\\,-1)$ — только вдвое: большой промах не может перекричать остальных."),
        ("h3", "Масштаб: одна кривая на все δ"),
        ("p", "Если измерять ошибку в единицах порога, все потери Хьюбера — одна и та же кривая:"),
        ("eq", r"L_\delta(r)=\delta^2\,L_1\!\left(\frac{r}{\delta}\right)"),
        ("p", "Поэтому $\\delta$ нельзя выбрать «вообще»: он зависит от единиц $y$. Ошибка в 1 рубль и в 1 миллион рублей — разные вещи. Обычно $\\delta$ задают в долях типичного разброса шума $\\sigma$ (раздел про выбор $\\delta$)."),
    ]),
    dict(id="properties", title="Свойства", blocks=[
        ("ul", [
            "<b>Неотрицательна и чётна</b>: $L_\\delta(r)\\ge0$, $L_\\delta(-r)=L_\\delta(r)$, минимум $0$ только при $r=0$.",
            "<b>Выпукла</b>: парабола и касательная к ней склеены без «впадины»; значит, у линейной регрессии с потерей Хьюбера нет ложных локальных минимумов.",
            "<b>Гладкость $C^1$, но не $C^2$</b>: первая производная непрерывна, вторая прыгает с 1 на 0 при $|r|=\\delta$.",
            "<b>Зажата между параболой и прямой</b>: $\\delta|r|-\\tfrac12\\delta^2\\le L_\\delta(r)\\le\\tfrac12r^2$; разность с каждой из них равна $\\tfrac12(|r|-\\delta)^2$ там, где кривая с ней не совпадает.",
            "<b>Ограниченная производная</b>: $|L'_\\delta(r)|\\le\\delta$ — главное свойство для робастности.",
            "<b>Пределы</b>: при $\\delta\\to\\infty$ $L_\\delta(r)\\to\\tfrac12r^2$ (MSE), при $\\delta\\to0$ $L_\\delta(r)/\\delta\\to|r|$ (MAE).",
        ]),
        ("deep", "Почему кривая зажата и откуда пределы", [
            ("p", "При $|r|&gt;\\delta$: $\\tfrac12r^2-\\bigl(\\delta|r|-\\tfrac12\\delta^2\\bigr)=\\tfrac12(|r|-\\delta)^2\\ge0$, то есть прямая лежит под параболой. При $|r|\\le\\delta$ то же выражение показывает, что парабола лежит над прямой. Значит, $L_\\delta$ всегда между ними и совпадает с каждой на своём участке."),
            ("p", "Пределы: если $\\delta\\ge|r|$, то $L_\\delta(r)=\\tfrac12r^2$ ровно — достаточно большого порога. Если $\\delta&lt;|r|$, то $L_\\delta(r)/\\delta=|r|-\\tfrac12\\delta\\to|r|$ при $\\delta\\to0$."),
        ]),
        ("deep", "Хьюбер как «смягчённый модуль» (огибающая Моро)", [
            ("p", "Есть изящная эквивалентная запись: потеря Хьюбера — это лучший компромисс, если часть ошибки $z$ разрешено «списать» по цене модуля:"),
            ("eq", r"L_\delta(r)=\min_{z\in\mathbb R}\Bigl(\tfrac12(r-z)^2+\delta|z|\Bigr)"),
            ("p", "Минимум достигается при мягком пороге $z^*=\\operatorname{sign}(r)\\max(|r|-\\delta,\\,0)$. Если $|r|\\le\\delta$, то $z^*=0$ и остаётся $\\tfrac12r^2$. Иначе $z^*=r-\\delta\\operatorname{sign}r$, и получаем $\\tfrac12\\delta^2+\\delta(|r|-\\delta)=\\delta|r|-\\tfrac12\\delta^2$. В выпуклом анализе это называют огибающей Моро функции $\\delta|\\cdot|$: так из негладкого модуля получают гладкую функцию с тем же поведением на бесконечности."),
            ("p", "Модельная интерпретация: $y=\\hat y+\\text{шум}+z$, где $z$ — редкая «аномалия». Потеря Хьюбера сама решает, какую часть ошибки объяснить аномалией, а какую — гауссовым шумом."),
        ]),
    ]),
    dict(id="derivative", title="Производная: обрезанный остаток", blocks=[
        ("p", "Производная по остатку в статистике обозначается $\\psi$ и называется функцией влияния (influence function): она показывает, с какой силой одна точка тянет оценку."),
        ("eq", r"\psi_\delta(r)=L'_\delta(r)=\begin{cases}r, & |r|\le\delta,\\ \delta\operatorname{sign}r, & |r|>\delta\end{cases}=\operatorname{clip}(r,\,-\delta,\,\delta)"),
        ("deep", "Вывод по шагам", [
            ("p", "Внутри полосы $(\\tfrac12r^2)'=r$. Снаружи $|r|$ дифференцируем как $\\operatorname{sign}r$, поэтому $\\bigl(\\delta|r|-\\tfrac12\\delta^2\\bigr)'=\\delta\\operatorname{sign}r$. В точках $r=\\pm\\delta$ левая и правая производные совпадают ($\\pm\\delta$), значит, производная существует и непрерывна."),
            ("p", "По прогнозу — цепное правило: $\\dfrac{\\partial L_\\delta}{\\partial\\hat y}=\\psi_\\delta(r)\\cdot\\dfrac{\\partial r}{\\partial\\hat y}=-\\psi_\\delta(y-\\hat y)$."),
            ("p", "Вторая производная: $L''_\\delta(r)=1$ при $|r|&lt;\\delta$ и $0$ при $|r|&gt;\\delta$; в точках $\\pm\\delta$ её нет — левая и правая не совпадают."),
        ]),
        ("eq", r"\frac{\partial L_\delta}{\partial\hat y}=-\operatorname{clip}\bigl(y-\hat y,\,-\delta,\,\delta\bigr)"),
        ("p", "Сравните три потери. У MSE ($\\tfrac12r^2$) тяга $\\psi=r$ растёт без предела. У MAE тяга постоянна. У Хьюбера она растёт, пока точка «своя», и замирает на уровне $\\delta$, когда точка подозрительна. Вторая полезная картинка — <b>вес</b> точки $w(r)=\\psi(r)/r$: какую долю «голоса» точка получает по сравнению с обычным методом наименьших квадратов (МНК)."),
        ("viz", "huber-influence", {"delta": 1, "r": 4}, "<b>Рисунок 2.</b> Слева — тяга $\\psi(r)$, справа — вес $w(r)=\\psi(r)/r$. Точка с ошибкой $r=4$ при $\\delta=1$ тянет в MSE с силой 4, у Хьюбера — с силой 1, то есть получает вес $0{,}25$. Внутри полосы $|r|\\le\\delta$ вес равен 1: обычные точки Хьюбер не трогает."),
        ("callout", "note", "Почему ψ важнее самой потери", "Оптимум модели определяется уравнением $\\sum_i\\psi(r_i)\\,\\partial\\hat y_i/\\partial\\theta=0$, а не значением потери. Поэтому робастность — это свойство $\\psi$: ограниченная $\\psi$ значит, что никакой одиночный выброс не может сдвинуть решение сколь угодно далеко. У MSE $\\psi$ не ограничена, и один выброс сдвигает среднее куда угодно."),
    ]),
    dict(id="surface", title="Поверхность L(r, δ) в 3D", blocks=[
        ("p", "Посмотрим на потерю как на функцию двух переменных — ошибки $r$ и порога $\\delta$. Это помогает увидеть сразу всё семейство кривых и то, как порог меняет форму."),
        ("viz", "huber-surface", {"delta": 1}, "<b>Рисунок 3.</b> Слева — поверхность $L_\\delta(r)$ (её можно вращать), оранжевые линии — стык $|r|=\\delta$, синяя — срез при выбранном $\\delta$. Справа — вид сверху с линиями уровня. Внутри «клина» $|r|\\le\\delta$ линии вертикальны, снаружи изгибаются. Переключите на псевдо-Хьюбера: стыка больше нет, поверхность гладкая всюду."),
        ("p", "Две вещи видны сразу. Во-первых, под стыком, где $|r|\\le\\delta$, поверхность не зависит от $\\delta$: там всегда $\\tfrac12r^2$, и линии уровня $L=c$ — вертикальные прямые $r=\\pm\\sqrt{2c}$. Во-вторых, снаружи линия уровня $L=c$ — это $|r|=c/\\delta+\\delta/2$: чем меньше порог, тем дальше нужно уйти, чтобы набрать ту же потерю."),
        ("callout", "note", "Многомерный случай", "Когда ответ — вектор (например, четыре координаты рамки в детекции), потерю Хьюбера обычно считают по каждой координате и складывают: $\\sum_jL_\\delta(r_j)$. Линии уровня такой суммы на плоскости $(r_1,r_2)$ — квадраты со скруглёнными углами, а градиент обрезается по каждой координате отдельно. Это не то же самое, что $L_\\delta(\\|r\\|)$, где обрезается длина всего вектора ошибки."),
    ]),
    dict(id="statistics", title="Оценка Хьюбера и выбор δ", blocks=[
        ("p", "Хьюбер придумал свою функцию для простейшей задачи статистики — оценки центра выборки $x_1,\\dots,x_n$. Если минимизировать $\\sum(x_i-\\mu)^2$, получится среднее; если $\\sum|x_i-\\mu|$ — медиана. Оценка Хьюбера $\\hat\\mu$ минимизирует $\\sum L_\\delta(x_i-\\mu)$, то есть решает уравнение"),
        ("eq", r"\sum_{i=1}^{n}\psi_\delta(x_i-\hat\mu)=0"),
        ("p", "Точки внутри зоны $|x_i-\\hat\\mu|\\le\\delta$ участвуют как в среднем, а дальние — только знаком, с силой $\\delta$, как в медиане."),
        ("viz", "huber-location", {"delta": 1}, "<b>Рисунок 4.</b> 13 значений вокруг 5 и два выброса (красные; правый можно тянуть). Высота столбика — вес точки в оценке. При $\\delta=1$: среднее $6{,}079$, медиана $5{,}557$, оценка Хьюбера $5{,}369$ — ближе всех к истинному центру 5. Справа — путь $\\hat\\mu(\\delta)$: при $\\delta\\to0$ оценка стремится к медиане, а при $\\delta\\ge7{,}42$ совпадает со средним."),
        ("p", "Обратите внимание на правый график: путь $\\hat\\mu(\\delta)$ <b>не обязан</b> лежать между медианой и средним — при $\\delta=1$ оценка ниже обоих. Предельные значения точные: при $\\delta\\to0$ получается медиана, а как только $\\delta$ превышает расстояние от среднего до самой дальней точки (здесь $13{,}5-6{,}079\\approx7{,}42$), все точки в квадратичной зоне и $\\hat\\mu$ равна среднему."),
        ("h3", "Сколько стоит робастность: правило 1,345σ"),
        ("p", "Если данные на самом деле нормальные, без выбросов, лучшая оценка — среднее. Насколько Хьюбер хуже? Это измеряют <b>асимптотической эффективностью</b>: отношением дисперсии среднего к дисперсии оценки. Для $\\psi$ с порогом $k$ (в единицах $\\sigma$) при стандартной нормальной $X$:"),
        ("eq", r"\operatorname{Var}\hat\mu\approx\frac{\sigma^2}{n}\cdot\frac{\mathbb E\,\psi_k(X)^2}{\bigl(\mathbb E\,\psi'_k(X)\bigr)^2},\qquad \mathbb E\,\psi'_k=2\Phi(k)-1,\quad \mathbb E\,\psi_k^2=2\Phi(k)-1-2k\varphi(k)+2k^2\bigl(1-\Phi(k)\bigr)"),
        ("p", "Решая «эффективность $=95\\%$», получаем $k\\approx1{,}345$. Отсюда классический выбор $\\delta=1{,}345\\,\\sigma$: всего 5% потерь на чистых данных в обмен на защиту от выбросов. У медианы эффективность $2/\\pi\\approx64\\%$."),
        ("viz", "huber-efficiency", {"k": 1.345, "eps": 0.05}, "<b>Рисунок 5.</b> Дисперсия оценки центра (в единицах $\\sigma^2/n$) для смеси $(1-\\varepsilon)N(0,1)+\\varepsilon N(0,10^2)$. При $k=1{,}345$ эффективность на чистых данных — $95{,}0\\%$. При $\\varepsilon=0{,}05$ дисперсия среднего $5{,}95$, медианы $1{,}722$, Хьюбера с $k=1{,}345$ — $1{,}229$; лучший порог для этой смеси $k\\approx1{,}48$ (полый кружок)."),
        ("callout", "history", "Минимакс Хьюбера", "В статье 1964 года Хьюбер доказал больше: если неизвестно, какие именно выбросы встретятся, а известна лишь их доля $\\varepsilon$, то оценка с $\\psi_k$ минимизирует <i>наихудшую</i> дисперсию. Порог связан с долей уравнением $2\\varphi(k)/k-2\\Phi(-k)=\\varepsilon/(1-\\varepsilon)$: для $\\varepsilon=0{,}05$ это $k\\approx1{,}40$, для $\\varepsilon=0{,}01$ — $k\\approx1{,}95$."),
        ("callout", "warn", "σ тоже нужно оценить робастно", "Правило $\\delta=1{,}345\\sigma$ бесполезно, если $\\sigma$ посчитать обычным стандартным отклонением: выбросы раздуют его. Используют медианное абсолютное отклонение: $\\hat\\sigma=\\operatorname{MAD}/0{,}6745\\approx1{,}4826\\cdot\\operatorname{median}|r_i-\\operatorname{median}(r)|$. В <code>HuberRegressor</code> масштаб оценивается совместно с коэффициентами, а <code>epsilon=1.35</code> по умолчанию — это и есть $k$."),
    ]),
    dict(id="training", title="Хьюбер в обучении", blocks=[
        ("p", "Обучим прямую градиентным спуском двумя способами — на половине MSE и на потере Хьюбера — по одним и тем же данным: 30 точек вокруг $y=1+0{,}5x$ с шумом $\\sigma=0{,}5$ и три выброса внизу справа. Порог $\\delta=0{,}7\\approx1{,}345\\cdot0{,}5$."),
        ("viz", "huber-regression", {"delta": 0.7}, "<b>Рисунок 6.</b> Нажмите «Пуск». Обе модели стартуют с прямой $y=0$ и делают одинаковые шаги ($\\eta=0{,}15$). MSE быстро сходится к наклону $0{,}363$ — выбросы опрокидывают прямую. Хьюбер сначала идёт медленнее (все ошибки большие, и каждая тянет не сильнее $\\delta$), но приходит к наклону $0{,}511$ при истинном $0{,}5$. Перетащите крайний выброс — во время обучения или до него."),
        ("p", "Шаг спуска показывает механизм: каждая точка тянет параметры пропорционально $\\psi(r_i)$. Пока прямая далеко от всех точек, у Хьюбера все тяги равны $\\pm\\delta$ — он движется как MAE, с постоянной скоростью. Когда прямая подходит к основной массе точек, их ошибки попадают в квадратичную зону и спуск становится обычным МНК — уже без выбросов, которые так и остались «на привязи» $\\delta$."),
        ("eq", r"\theta\leftarrow\theta+\eta\,\frac1n\sum_{i=1}^{n}\psi_\delta\bigl(y_i-\hat y_i\bigr)\,\frac{\partial\hat y_i}{\partial\theta}"),
        ("deep", "IRLS: Хьюбер как МНК с весами", [
            ("p", "Для линейной модели $\\hat y_i=x_i^\\top\\beta$ условие оптимума $\\sum_i\\psi(r_i)x_i=0$ можно переписать как $\\sum_iw_ir_ix_i=0$ с весами $w_i=\\psi(r_i)/r_i=\\min(1,\\delta/|r_i|)$. Если веса заморозить, это нормальные уравнения взвешенного МНК, решаемые явно:"),
            ("eq", r"\beta^{(t+1)}=\bigl(X^\top W^{(t)}X\bigr)^{-1}X^\top W^{(t)}y,\qquad W^{(t)}=\operatorname{diag}\bigl(w_i(\beta^{(t)})\bigr)"),
            ("p", "Итерации «посчитать остатки → обновить веса → решить МНК» (iteratively reweighted least squares) сходятся к оценке Хьюбера за десяток шагов. Веса здесь те же, что на рисунке 2 справа."),
        ]),
        ("h3", "Где ещё Хьюбер работает внутри обучения"),
        ("ul", [
            "<b>Градиентный бустинг.</b> Каждое новое дерево учится на антиградиенте потери. Для Хьюбера это $\\psi(r_i)$ — <i>обрезанные</i> остатки, поэтому одно аномальное значение не заставляет дерево тратить лист на выброс. В scikit-learn порог $\\delta$ на каждой итерации берут как $\\alpha$-квантиль $|r_i|$ (по умолчанию $\\alpha=0{,}9$).",
            "<b>DQN.</b> В статье DeepMind (2015) ошибку временной разности обрезали до $[-1;\\,1]$. Обрезанный градиент — это ровно $\\psi_1$, то есть обучение на потере Хьюбера с $\\delta=1$: редкие огромные награды не разрушают сеть.",
            "<b>Fast R-CNN.</b> Для регрессии координат рамки Гиршик (2015) взял Smooth L1: она «менее чувствительна к выбросам, чем L2» и не требует аккуратной настройки темпа обучения, чтобы избежать взрыва градиентов.",
        ]),
    ]),
    dict(id="variants", title="Гладкие родственники: псевдо-Хьюбер, log-cosh, Smooth L1", blocks=[
        ("p", "Скачок второй производной не мешает градиентному спуску, но мешает методам второго порядка. XGBoost и LightGBM делают шаг Ньютона: лист получает значение $-\\sum g_i/\\sum h_i$, где $h_i$ — вторые производные. Истинная вторая производная Хьюбера для всех выбросов равна нулю, и если в лист попали только они, знаменатель обнуляется. Поэтому реализации либо подменяют её константой (так поступает LightGBM в <code>objective='huber'</code>), либо берут гладкий вариант."),
        ("eq", r"\text{псевдо-Хьюбер: }\;\delta^2\Bigl(\sqrt{1+(r/\delta)^2}-1\Bigr),\qquad \text{log-cosh: }\;\delta^2\ln\cosh\frac{r}{\delta},\qquad \text{Smooth L1: }\;\frac{L_\beta(r)}{\beta}"),
        ("viz", "huber-variants", {"variant": "pseudo", "delta": 1, "r": 3}, "<b>Рисунок 7.</b> Хьюбер и его родственники при одинаковом $\\delta$. Псевдо-Хьюбер и log-cosh тоже ведут себя как $\\tfrac12r^2$ у нуля и как $\\delta|r|$ на хвостах, но переход плавный, а вторая производная (галочка внизу) непрерывна. При $\\delta=1$, $r=3$: Хьюбер $2{,}5$, псевдо-Хьюбер $2{,}162$, log-cosh $2{,}309$."),
        ("ul", [
            "<b>Псевдо-Хьюбер</b> (в компьютерном зрении с точностью до множителя $\\delta$ — потеря Шарбоннье $\\sqrt{r^2+\\delta^2}-\\delta$): производная $r/\\sqrt{1+(r/\\delta)^2}$ стремится к $\\pm\\delta$ медленно; вторая производная $(1+(r/\\delta)^2)^{-3/2}$ всюду положительна. В XGBoost — <code>objective='reg:pseudohubererror'</code> с параметром <code>huber_slope</code> ($=\\delta$).",
            "<b>log-cosh</b>: производная $\\delta\\tanh(r/\\delta)$ — гладкое «обрезание»; на хвостах $\\delta^2\\ln\\cosh(r/\\delta)\\approx\\delta|r|-\\delta^2\\ln2$.",
            "<b>Smooth L1</b>: это Хьюбер, делённый на $\\beta$: $\\tfrac{0{,}5r^2}{\\beta}$ при $|r|&lt;\\beta$ и $|r|-\\tfrac12\\beta$ дальше. При $\\beta\\to0$ она стремится к $|r|$ (а Хьюбер — к нулю). В PyTorch: <code>HuberLoss(delta=δ) = δ · SmoothL1Loss(beta=δ)</code>.",
        ]),
    ]),
    dict(id="code", title="В коде", blocks=[
        ("p", "Сама формула — одна строка с <code>np.where</code>. Градиент — <code>np.clip</code>. Ниже — реализация, проверка на сквозном примере и регрессия Хьюбера через IRLS."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_IRLS"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Готовые реализации", "PyTorch: <code>nn.HuberLoss(delta)</code>, <code>nn.SmoothL1Loss(beta)</code>. Keras: <code>keras.losses.Huber(delta)</code>. scikit-learn: <code>HuberRegressor(epsilon=1.35)</code>, <code>GradientBoostingRegressor</code> (<code>loss='huber'</code>, <code>alpha=0.9</code>). LightGBM: <code>objective='huber'</code> (порог — параметр <code>alpha</code>). XGBoost: <code>objective='reg:pseudohubererror'</code>."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>δ без учёта масштаба.</b> $\\delta=1$ для цен в долларах и для цен в миллионах — совершенно разные потери. Нормируйте целевую переменную или задавайте $\\delta$ в единицах робастного разброса.",
            "<b>Путаница Huber и Smooth L1.</b> Они отличаются множителем $1/\\beta$: при одинаковом пороге Smooth L1 даёт в $\\beta$ раз меньшую потерю и градиент. Меняя одну на другую, пересчитайте темп обучения.",
            "<b>Оценка σ обычным std</b> для правила $1{,}345\\sigma$ — выбросы раздувают std, порог получается слишком большим, и защита исчезает. Берите MAD.",
            "<b>Ожидание, что Хьюбер спасёт от выбросов в признаках.</b> Он ограничивает влияние большого остатка $r$, но точка с экстремальным $x$ (высокий рычаг, leverage) всё равно может развернуть прямую. Для этого нужны другие методы (например, веса по $x$).",
            "<b>Хьюбер в бустинге с методом Ньютона</b> без проверки: нулевые вторые производные выбросов делают шаги листьев нестабильными. Используйте псевдо-Хьюбера или реализацию, которая это учитывает.",
            "<b>Сравнение значений потерь при разных δ.</b> Значение $L_\\delta$ растёт с $\\delta$ при прочих равных; сравнивайте модели по внешней метрике (MAE, RMSE на валидации), а не по самой потере.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../mse/\">MSE</a>: при $\\delta\\ge\\max|r_i|$ потеря Хьюбера равна половине квадрата ошибки, а оценка — МНК.",
            "<a href=\"../mae/\">MAE</a>: при $\\delta\\to0$ $L_\\delta/\\delta\\to|r|$; оценка центра стремится к медиане.",
            "<a href=\"../rmse/\">RMSE</a>: метрика, которую чаще всего портят выбросы; Хьюбер позволяет обучаться устойчиво, а отчитываться по RMSE на чистых данных.",
            "<a href=\"../relu/\">ReLU</a> и обрезание: $\\psi_\\delta(r)=\\operatorname{clip}(r,-\\delta,\\delta)$ — та же идея «линейно до порога», что и в ReLU6 и gradient clipping.",
            "<a href=\"../focal/\">Focal Loss</a> — противоположная философия: Хьюбер <i>ослабляет</i> самые большие ошибки (считая их выбросами), а focal loss <i>усиливает</i> вес трудных примеров относительно лёгких.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $L_\\delta(r)$ — парабола $\\tfrac12r^2$ при $|r|\\le\\delta$ и касательная к ней прямая $\\delta(|r|-\\tfrac12\\delta)$ дальше; функция выпукла и принадлежит $C^1$, но не $C^2$. 2) Производная $\\psi=\\operatorname{clip}(r,-\\delta,\\delta)$ ограничена — выброс не тянет сильнее $\\delta$; вес точки $\\min(1,\\delta/|r|)$. 3) $\\delta\\to\\infty$ — MSE и среднее, $\\delta\\to0$ — MAE и медиана. 4) $\\delta=1{,}345\\sigma$ (σ по MAD) даёт 95% эффективности на нормальных данных. 5) Гладкие версии — псевдо-Хьюбер и log-cosh — нужны методам второго порядка; Smooth L1 — тот же Хьюбер, делённый на β."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="Чему равна $L_1(3)$ — потеря Хьюбера с $\\delta=1$ при ошибке 3?", options=["$4{,}5$", "$3$", "$2{,}5$", "$1$"], answer=2,
                 explain="$|r|=3&gt;\\delta$, линейная ветвь: $1\\cdot(3-0{,}5)=2{,}5$. Половина квадрата дала бы $4{,}5$."),
            dict(q="Какое наибольшее значение может принять $|\\partial L_\\delta/\\partial\\hat y|$?", options=["Не ограничено", "$\\delta$", "$\\tfrac12\\delta^2$", "$1$"], answer=1,
                 explain="Производная — обрезанный остаток $\\operatorname{clip}(r,-\\delta,\\delta)$, по модулю не больше $\\delta$."),
            dict(q="Что происходит в точке $|r|=\\delta$?", options=["Разрыв значения", "Излом: прыгает первая производная", "Значение и первая производная непрерывны, прыгает вторая", "Ничего, функция бесконечно гладкая"], answer=2,
                 explain="Ветви сшиты по значению $\\tfrac12\\delta^2$ и по наклону $\\delta$; вторая производная переходит с 1 на 0. Поэтому Хьюбер — $C^1$, но не $C^2$."),
            dict(q="К чему стремится оценка центра Хьюбера при $\\delta\\to0$ и при очень большом $\\delta$?", options=["К среднему и к медиане", "К медиане и к среднему", "К моде и к среднему", "К нулю и к бесконечности"], answer=1,
                 explain="Малый порог оставляет от каждой точки только знак — получается медиана; большой порог делает все точки «своими» — получается среднее."),
            dict(q="Почему порог часто берут равным $1{,}345\\sigma$?", options=["Так оценка становится несмещённой", "Это 95% эффективности на нормальных данных при сохранении робастности", "Так выбрасывается ровно 5% точек", "Это квантиль 0,9 модуля остатков"], answer=1,
                 explain="При $k=1{,}345$ дисперсия оценки Хьюбера на чистой нормальной выборке всего в $1/0{,}95$ раза больше дисперсии среднего; при этом влияние выбросов ограничено. Никакие точки не выбрасываются — дальние просто получают меньший вес."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "Regression learns from its errors $r=y-\\hat y$. Two classic losses answer the question “how to penalise an error” differently. <a href=\"../mse/\">MSE</a> penalises the square: it is smooth, its gradient is proportional to the error and fades gently near the minimum, but one outlier with error 10 weighs as much as a hundred errors of size 1. <a href=\"../mae/\">MAE</a> penalises the absolute value: outliers hardly bother it, but it has a kink at zero and its gradient always has the same size, so the model struggles to polish small errors."),
        ("p", "In 1964 Peter Huber proposed to take the best of both: <b>a parabola for small errors and a straight line for large ones</b>, switching at a threshold $\\delta$. Where the idea works today:"),
        ("ul", [
            "<b>robust regression</b> — <code>HuberRegressor</code> in scikit-learn, M-estimators in statistics;",
            "<b>object detection</b> — Smooth L1 in Fast R-CNN and its descendants for box-coordinate regression; it is Huber up to a factor;",
            "<b>reinforcement learning</b> — DQN clips the temporal-difference error to $[-1,\\,1]$, which is equivalent to the Huber loss with $\\delta=1$;",
            "<b>gradient boosting</b> — <code>loss='huber'</code> in scikit-learn, <code>objective='huber'</code> in LightGBM, pseudo-Huber in XGBoost;",
            "<b>any data with anomalies</b> — property prices, sensor readings, labels with typos.",
        ]),
        ("callout", "key", "The essentials in a minute", "$L_\\delta(r)$ equals $\\tfrac12r^2$ for $|r|\\le\\delta$ and $\\delta(|r|-\\tfrac12\\delta)$ beyond. At $|r|=\\delta$ both the values ($\\tfrac12\\delta^2$) and the slopes ($\\delta$) agree. The derivative $\\psi(r)=\\operatorname{clip}(r,-\\delta,\\delta)$ is bounded: an outlier pulls the model no harder than $\\delta$. Small $\\delta$ is closer to MAE, large $\\delta$ to MSE."),
    ]),
    dict(id="intuition", title="Intuition: a parabola with straight tails", blocks=[
        ("p", "Picture a spring that pulls the prediction towards the answer. While the error is small, it is an ordinary spring: the more it is stretched, the harder it pulls — that is the parabola $\\tfrac12r^2$. But the spring has a safety catch: after a stretch of $\\delta$ the force stops growing and stays equal to $\\delta$. From there on the energy of such a spring grows only linearly — those are the straight tails."),
        ("p", "Drag the point along the plot and move $\\delta$. Inside the teal band $|r|\\le\\delta$ the blue curve lies on the grey parabola, outside it lies on the dashed line $\\delta(|r|-\\delta/2)$. The orange tangent passes the seam without a kink."),
        ("viz", "huber-explorer", {"delta": 1, "r": 2}, "<b>Figure 1.</b> The Huber loss $L_\\delta(r)$ and its derivatives. Below: the orange $\\psi(r)=L'_\\delta(r)$ is sloped inside the band and flat outside; the violet $L''_\\delta$ is a step: 1 inside, 0 outside. With $\\delta=1$ and $r=2$: $L=1.5$ instead of $\\tfrac12r^2=2$, and the slope is 1, not 2."),
        ("callout", "intuition", "What to notice", "At the seam $|r|=\\delta$ the curve passes from the parabola to the line smoothly: the line $\\delta(|r|-\\delta/2)$ is the <i>tangent</i> to the parabola at $r=\\pm\\delta$. Only the second derivative has a jump: the curvature drops from 1 to 0."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("eq", r"L_\delta(r)=\begin{cases}\tfrac12 r^2, & |r|\le\delta,\\[1mm] \delta\bigl(|r|-\tfrac12\delta\bigr), & |r|>\delta,\end{cases}\qquad r=y-\hat y"),
        ("symbols", [
            (r"r=y-\hat y", "the residual: how far the answer $y$ is above the prediction $\\hat y$; the loss depends only on $|r|$, the sign does not matter;"),
            (r"\delta>0", "the threshold: errors below $\\delta$ count as “ordinary noise”, larger ones as suspicious; it is measured in the units of $y$;"),
            (r"\tfrac12 r^2", "the quadratic branch — exactly half the squared error, as in MSE; the factor $\\tfrac12$ makes the derivative equal to $r$;"),
            (r"\delta|r|", "the linear branch — the absolute error weighted by $\\delta$, as in MAE;"),
            (r"-\tfrac12\delta^2", "the downward shift that stitches the branches: without it the line $\\delta|r|$ would give $\\delta^2$ at $|r|=\\delta$, while the parabola gives $\\tfrac12\\delta^2$."),
        ]),
        ("p", "Let us check the stitch. At $|r|=\\delta$ the quadratic branch gives $\\tfrac12\\delta^2$ and the linear one $\\delta(\\delta-\\tfrac12\\delta)=\\tfrac12\\delta^2$: the values agree. The derivatives: $r=\\delta$ for the parabola and $\\delta\\operatorname{sign}r=\\delta$ for the line — the slopes agree too. The constant $-\\tfrac12\\delta^2$ was chosen precisely to make the line tangent to the parabola."),
        ("table", ["$r$", "$\\tfrac12r^2$", "$|r|$", "$L_1(r)$", "$\\psi_1(r)$"], "TABLE", {"num": [0, 1, 2, 3, 4]}),
        ("p", "The table for $\\delta=1$ shows the main point: for an error of 10 the square gives 50 while Huber gives 9.5, and the derivative (last column) never exceeds 1."),
        ("h3", "The running example"),
        ("p", "Take the example from the cheat sheet: $y=(3,\\,5,\\,8)$, $\\hat y=(2.5,\\,5,\\,10)$, errors $r=(0.5,\\,0,\\,-2)$. With $\\delta=1$ the first error falls on the parabola: $\\tfrac12\\cdot0.5^2=0.125$; the second is zero; the third, $|r|=2&gt;1$, falls on the line: $1\\cdot(2-0.5)=1.5$. The mean is $(0.125+0+1.5)/3\\approx0.542$."),
        ("p", "The gradients are more interesting. In half-MSE they equal the errors themselves, $(0.5,\\,0,\\,-2)$: the outlier pulls four times harder than the first point. For Huber $\\psi=(0.5,\\,0,\\,-1)$ — only twice as hard: a big miss cannot shout down the others."),
        ("h3", "Scale: one curve for every δ"),
        ("p", "If the error is measured in units of the threshold, all Huber losses are one and the same curve:"),
        ("eq", r"L_\delta(r)=\delta^2\,L_1\!\left(\frac{r}{\delta}\right)"),
        ("p", "That is why $\\delta$ cannot be chosen “in general”: it depends on the units of $y$. An error of 1 dollar and of 1 million dollars are different things. Usually $\\delta$ is set as a multiple of the typical noise spread $\\sigma$ (see the section on choosing $\\delta$)."),
    ]),
    dict(id="properties", title="Properties", blocks=[
        ("ul", [
            "<b>Non-negative and even</b>: $L_\\delta(r)\\ge0$, $L_\\delta(-r)=L_\\delta(r)$, the minimum $0$ only at $r=0$.",
            "<b>Convex</b>: a parabola and its tangent are glued without a “dip”, so linear regression with the Huber loss has no spurious local minima.",
            "<b>Smoothness $C^1$ but not $C^2$</b>: the first derivative is continuous, the second jumps from 1 to 0 at $|r|=\\delta$.",
            "<b>Squeezed between a parabola and a line</b>: $\\delta|r|-\\tfrac12\\delta^2\\le L_\\delta(r)\\le\\tfrac12r^2$; the gap to each equals $\\tfrac12(|r|-\\delta)^2$ wherever the curve does not coincide with it.",
            "<b>Bounded derivative</b>: $|L'_\\delta(r)|\\le\\delta$ — the key property for robustness.",
            "<b>Limits</b>: as $\\delta\\to\\infty$, $L_\\delta(r)\\to\\tfrac12r^2$ (MSE); as $\\delta\\to0$, $L_\\delta(r)/\\delta\\to|r|$ (MAE).",
        ]),
        ("deep", "Why the curve is squeezed, and where the limits come from", [
            ("p", "For $|r|&gt;\\delta$: $\\tfrac12r^2-\\bigl(\\delta|r|-\\tfrac12\\delta^2\\bigr)=\\tfrac12(|r|-\\delta)^2\\ge0$, i.e. the line lies below the parabola. For $|r|\\le\\delta$ the same expression shows that the parabola lies above the line. So $L_\\delta$ always sits between them and coincides with each on its own piece."),
            ("p", "Limits: if $\\delta\\ge|r|$, then $L_\\delta(r)=\\tfrac12r^2$ exactly — a large enough threshold suffices. If $\\delta&lt;|r|$, then $L_\\delta(r)/\\delta=|r|-\\tfrac12\\delta\\to|r|$ as $\\delta\\to0$."),
        ]),
        ("deep", "Huber as a “softened absolute value” (the Moreau envelope)", [
            ("p", "There is an elegant equivalent form: the Huber loss is the best compromise when part of the error, $z$, may be “written off” at the price of the absolute value:"),
            ("eq", r"L_\delta(r)=\min_{z\in\mathbb R}\Bigl(\tfrac12(r-z)^2+\delta|z|\Bigr)"),
            ("p", "The minimum is attained at the soft threshold $z^*=\\operatorname{sign}(r)\\max(|r|-\\delta,\\,0)$. If $|r|\\le\\delta$, then $z^*=0$ and $\\tfrac12r^2$ remains. Otherwise $z^*=r-\\delta\\operatorname{sign}r$, which gives $\\tfrac12\\delta^2+\\delta(|r|-\\delta)=\\delta|r|-\\tfrac12\\delta^2$. In convex analysis this is the Moreau envelope of $\\delta|\\cdot|$: it turns the non-smooth absolute value into a smooth function with the same behaviour at infinity."),
            ("p", "A modelling reading: $y=\\hat y+\\text{noise}+z$, where $z$ is a rare “anomaly”. The Huber loss decides by itself which part of the error to explain by the anomaly and which by Gaussian noise."),
        ]),
    ]),
    dict(id="derivative", title="The derivative: a clipped residual", blocks=[
        ("p", "In statistics the derivative with respect to the residual is denoted $\\psi$ and called the influence function: it shows how hard a single point pulls the estimate."),
        ("eq", r"\psi_\delta(r)=L'_\delta(r)=\begin{cases}r, & |r|\le\delta,\\ \delta\operatorname{sign}r, & |r|>\delta\end{cases}=\operatorname{clip}(r,\,-\delta,\,\delta)"),
        ("deep", "Step-by-step derivation", [
            ("p", "Inside the band $(\\tfrac12r^2)'=r$. Outside, $|r|$ differentiates to $\\operatorname{sign}r$, so $\\bigl(\\delta|r|-\\tfrac12\\delta^2\\bigr)'=\\delta\\operatorname{sign}r$. At $r=\\pm\\delta$ the left and right derivatives agree ($\\pm\\delta$), so the derivative exists and is continuous."),
            ("p", "With respect to the prediction — the chain rule: $\\dfrac{\\partial L_\\delta}{\\partial\\hat y}=\\psi_\\delta(r)\\cdot\\dfrac{\\partial r}{\\partial\\hat y}=-\\psi_\\delta(y-\\hat y)$."),
            ("p", "The second derivative: $L''_\\delta(r)=1$ for $|r|&lt;\\delta$ and $0$ for $|r|&gt;\\delta$; at $\\pm\\delta$ it does not exist — the left and right ones differ."),
        ]),
        ("eq", r"\frac{\partial L_\delta}{\partial\hat y}=-\operatorname{clip}\bigl(y-\hat y,\,-\delta,\,\delta\bigr)"),
        ("p", "Compare the three losses. For MSE ($\\tfrac12r^2$) the pull $\\psi=r$ grows without limit. For MAE it is constant. For Huber it grows while the point is “one of ours” and freezes at $\\delta$ once the point is suspicious. A second useful picture is the <b>weight</b> of a point, $w(r)=\\psi(r)/r$: what share of a “vote” the point gets compared with ordinary least squares."),
        ("viz", "huber-influence", {"delta": 1, "r": 4}, "<b>Figure 2.</b> Left: the pull $\\psi(r)$; right: the weight $w(r)=\\psi(r)/r$. A point with error $r=4$ at $\\delta=1$ pulls with force 4 under MSE and with force 1 under Huber, i.e. it gets weight $0.25$. Inside the band $|r|\\le\\delta$ the weight is 1: Huber leaves ordinary points alone."),
        ("callout", "note", "Why ψ matters more than the loss itself", "The model’s optimum is defined by the equation $\\sum_i\\psi(r_i)\\,\\partial\\hat y_i/\\partial\\theta=0$, not by the value of the loss. So robustness is a property of $\\psi$: a bounded $\\psi$ means no single outlier can move the solution arbitrarily far. For MSE $\\psi$ is unbounded, and one outlier can drag the mean anywhere."),
    ]),
    dict(id="surface", title="The surface L(r, δ) in 3D", blocks=[
        ("p", "Let us view the loss as a function of two variables — the error $r$ and the threshold $\\delta$. This shows the whole family of curves at once and how the threshold changes the shape."),
        ("viz", "huber-surface", {"delta": 1}, "<b>Figure 3.</b> Left: the surface $L_\\delta(r)$ (you can rotate it); the orange lines are the seam $|r|=\\delta$, the blue one is the slice at the chosen $\\delta$. Right: the view from above with level lines. Inside the “wedge” $|r|\\le\\delta$ the lines are vertical, outside they bend. Switch to pseudo-Huber: the seam disappears and the surface is smooth everywhere."),
        ("p", "Two things are visible at once. First, under the seam, where $|r|\\le\\delta$, the surface does not depend on $\\delta$: it is always $\\tfrac12r^2$ there, and the level lines $L=c$ are the vertical lines $r=\\pm\\sqrt{2c}$. Second, outside, the level line $L=c$ is $|r|=c/\\delta+\\delta/2$: the smaller the threshold, the further you must go to collect the same loss."),
        ("callout", "note", "The multidimensional case", "When the target is a vector (for example, the four coordinates of a box in detection), the Huber loss is usually computed per coordinate and summed: $\\sum_jL_\\delta(r_j)$. The level lines of such a sum in the $(r_1,r_2)$ plane are squares with rounded corners, and the gradient is clipped per coordinate. This is not the same as $L_\\delta(\\|r\\|)$, which clips the length of the whole error vector."),
    ]),
    dict(id="statistics", title="Huber’s estimate and the choice of δ", blocks=[
        ("p", "Huber designed his function for the simplest problem in statistics — estimating the centre of a sample $x_1,\\dots,x_n$. Minimising $\\sum(x_i-\\mu)^2$ gives the mean; minimising $\\sum|x_i-\\mu|$ gives the median. Huber’s estimate $\\hat\\mu$ minimises $\\sum L_\\delta(x_i-\\mu)$, i.e. it solves"),
        ("eq", r"\sum_{i=1}^{n}\psi_\delta(x_i-\hat\mu)=0"),
        ("p", "Points inside the zone $|x_i-\\hat\\mu|\\le\\delta$ take part as in the mean, while far ones contribute only their sign, with force $\\delta$, as in the median."),
        ("viz", "huber-location", {"delta": 1}, "<b>Figure 4.</b> 13 values around 5 and two outliers (red; the right one can be dragged). The height of a bar is the weight of the point in the estimate. At $\\delta=1$: the mean is $6.079$, the median $5.557$, Huber’s estimate $5.369$ — the closest to the true centre 5. On the right, the path $\\hat\\mu(\\delta)$: as $\\delta\\to0$ the estimate tends to the median, and for $\\delta\\ge7.42$ it coincides with the mean."),
        ("p", "Look at the right plot: the path $\\hat\\mu(\\delta)$ <b>need not</b> lie between the median and the mean — at $\\delta=1$ the estimate is below both. The limiting values are exact: as $\\delta\\to0$ we get the median, and as soon as $\\delta$ exceeds the distance from the mean to the farthest point (here $13.5-6.079\\approx7.42$), every point is in the quadratic zone and $\\hat\\mu$ equals the mean."),
        ("h3", "The price of robustness: the 1.345σ rule"),
        ("p", "If the data are actually normal, with no outliers, the best estimate is the mean. How much worse is Huber? This is measured by the <b>asymptotic efficiency</b>: the ratio of the mean’s variance to the estimate’s variance. For $\\psi$ with threshold $k$ (in units of $\\sigma$) and a standard normal $X$:"),
        ("eq", r"\operatorname{Var}\hat\mu\approx\frac{\sigma^2}{n}\cdot\frac{\mathbb E\,\psi_k(X)^2}{\bigl(\mathbb E\,\psi'_k(X)\bigr)^2},\qquad \mathbb E\,\psi'_k=2\Phi(k)-1,\quad \mathbb E\,\psi_k^2=2\Phi(k)-1-2k\varphi(k)+2k^2\bigl(1-\Phi(k)\bigr)"),
        ("p", "Solving “efficiency $=95\\%$” gives $k\\approx1.345$. Hence the classic choice $\\delta=1.345\\,\\sigma$: only a 5% loss on clean data in exchange for protection against outliers. The median’s efficiency is $2/\\pi\\approx64\\%$."),
        ("viz", "huber-efficiency", {"k": 1.345, "eps": 0.05}, "<b>Figure 5.</b> The variance of the location estimate (in units of $\\sigma^2/n$) for the mixture $(1-\\varepsilon)N(0,1)+\\varepsilon N(0,10^2)$. At $k=1.345$ the efficiency on clean data is $95.0\\%$. At $\\varepsilon=0.05$ the variance of the mean is $5.95$, of the median $1.722$, of Huber with $k=1.345$ $1.229$; the best threshold for this mixture is $k\\approx1.48$ (the hollow circle)."),
        ("callout", "history", "Huber’s minimax", "In the 1964 paper Huber proved more: if it is unknown which outliers will appear and only their share $\\varepsilon$ is known, the estimate with $\\psi_k$ minimises the <i>worst-case</i> variance. The threshold is tied to the share by $2\\varphi(k)/k-2\\Phi(-k)=\\varepsilon/(1-\\varepsilon)$: for $\\varepsilon=0.05$ this is $k\\approx1.40$, for $\\varepsilon=0.01$ $k\\approx1.95$."),
        ("callout", "warn", "σ must be estimated robustly too", "The rule $\\delta=1.345\\sigma$ is useless if $\\sigma$ is computed as the ordinary standard deviation: outliers inflate it. Use the median absolute deviation: $\\hat\\sigma=\\operatorname{MAD}/0.6745\\approx1.4826\\cdot\\operatorname{median}|r_i-\\operatorname{median}(r)|$. <code>HuberRegressor</code> estimates the scale jointly with the coefficients, and its default <code>epsilon=1.35</code> is exactly $k$."),
    ]),
    dict(id="training", title="Huber in training", blocks=[
        ("p", "Let us fit a line by gradient descent in two ways — on half-MSE and on the Huber loss — on the same data: 30 points around $y=1+0.5x$ with noise $\\sigma=0.5$ and three outliers at the bottom right. The threshold is $\\delta=0.7\\approx1.345\\cdot0.5$."),
        ("viz", "huber-regression", {"delta": 0.7}, "<b>Figure 6.</b> Press “Play”. Both models start from the line $y=0$ and take identical steps ($\\eta=0.15$). MSE quickly converges to slope $0.363$ — the outliers tip the line over. Huber is slower at first (all errors are large and each pulls no harder than $\\delta$), but arrives at slope $0.511$ against the true $0.5$. Drag the last outlier — during training or before it."),
        ("p", "A descent step shows the mechanism: each point pulls the parameters in proportion to $\\psi(r_i)$. While the line is far from all points, every Huber pull equals $\\pm\\delta$ — it moves like MAE, at a constant speed. Once the line reaches the bulk of the points, their errors enter the quadratic zone and the descent becomes ordinary least squares — now without the outliers, which stay on a $\\delta$ leash."),
        ("eq", r"\theta\leftarrow\theta+\eta\,\frac1n\sum_{i=1}^{n}\psi_\delta\bigl(y_i-\hat y_i\bigr)\,\frac{\partial\hat y_i}{\partial\theta}"),
        ("deep", "IRLS: Huber as weighted least squares", [
            ("p", "For a linear model $\\hat y_i=x_i^\\top\\beta$ the optimality condition $\\sum_i\\psi(r_i)x_i=0$ can be rewritten as $\\sum_iw_ir_ix_i=0$ with weights $w_i=\\psi(r_i)/r_i=\\min(1,\\delta/|r_i|)$. With the weights frozen, these are the normal equations of weighted least squares, solved explicitly:"),
            ("eq", r"\beta^{(t+1)}=\bigl(X^\top W^{(t)}X\bigr)^{-1}X^\top W^{(t)}y,\qquad W^{(t)}=\operatorname{diag}\bigl(w_i(\beta^{(t)})\bigr)"),
            ("p", "The iterations “compute residuals → update weights → solve least squares” (iteratively reweighted least squares) converge to Huber’s estimate in about ten steps. The weights are the same as on the right of Figure 2."),
        ]),
        ("h3", "Where else Huber works inside training"),
        ("ul", [
            "<b>Gradient boosting.</b> Each new tree learns the negative gradient of the loss. For Huber this is $\\psi(r_i)$ — <i>clipped</i> residuals, so a single anomalous value does not make a tree spend a leaf on the outlier. In scikit-learn the threshold $\\delta$ is recomputed at every iteration as the $\\alpha$-quantile of $|r_i|$ (default $\\alpha=0.9$).",
            "<b>DQN.</b> In the DeepMind paper (2015) the temporal-difference error was clipped to $[-1,\\,1]$. The clipped gradient is exactly $\\psi_1$, i.e. training on the Huber loss with $\\delta=1$: rare huge rewards do not wreck the network.",
            "<b>Fast R-CNN.</b> For regressing the box coordinates Girshick (2015) chose Smooth L1: it is “less sensitive to outliers than L2” and does not require careful tuning of the learning rate to avoid exploding gradients.",
        ]),
    ]),
    dict(id="variants", title="Smooth relatives: pseudo-Huber, log-cosh, Smooth L1", blocks=[
        ("p", "The jump in the second derivative does not hurt gradient descent, but it hurts second-order methods. XGBoost and LightGBM take a Newton step: a leaf gets the value $-\\sum g_i/\\sum h_i$, where $h_i$ are second derivatives. The true second derivative of Huber is zero for every outlier, and if a leaf receives only outliers, the denominator vanishes. So implementations either replace it with a constant (LightGBM does this in <code>objective='huber'</code>) or use a smooth variant."),
        ("eq", r"\text{pseudo-Huber: }\;\delta^2\Bigl(\sqrt{1+(r/\delta)^2}-1\Bigr),\qquad \text{log-cosh: }\;\delta^2\ln\cosh\frac{r}{\delta},\qquad \text{Smooth L1: }\;\frac{L_\beta(r)}{\beta}"),
        ("viz", "huber-variants", {"variant": "pseudo", "delta": 1, "r": 3}, "<b>Figure 7.</b> Huber and its relatives at the same $\\delta$. Pseudo-Huber and log-cosh also behave like $\\tfrac12r^2$ near zero and like $\\delta|r|$ on the tails, but the transition is gradual and the second derivative (tick the box) is continuous. At $\\delta=1$, $r=3$: Huber $2.5$, pseudo-Huber $2.162$, log-cosh $2.309$."),
        ("ul", [
            "<b>Pseudo-Huber</b> (in computer vision, up to the factor $\\delta$, the Charbonnier loss $\\sqrt{r^2+\\delta^2}-\\delta$): the derivative $r/\\sqrt{1+(r/\\delta)^2}$ approaches $\\pm\\delta$ slowly; the second derivative $(1+(r/\\delta)^2)^{-3/2}$ is positive everywhere. In XGBoost it is <code>objective='reg:pseudohubererror'</code> with the parameter <code>huber_slope</code> ($=\\delta$).",
            "<b>log-cosh</b>: the derivative $\\delta\\tanh(r/\\delta)$ is a smooth “clip”; on the tails $\\delta^2\\ln\\cosh(r/\\delta)\\approx\\delta|r|-\\delta^2\\ln2$.",
            "<b>Smooth L1</b> is Huber divided by $\\beta$: $\\tfrac{0.5r^2}{\\beta}$ for $|r|&lt;\\beta$ and $|r|-\\tfrac12\\beta$ beyond. As $\\beta\\to0$ it tends to $|r|$ (while Huber tends to zero). In PyTorch: <code>HuberLoss(delta=δ) = δ · SmoothL1Loss(beta=δ)</code>.",
        ]),
    ]),
    dict(id="code", title="In code", blocks=[
        ("p", "The formula itself is one line with <code>np.where</code>. The gradient is <code>np.clip</code>. Below: an implementation, a check on the running example and Huber regression via IRLS."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_IRLS"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Ready-made implementations", "PyTorch: <code>nn.HuberLoss(delta)</code>, <code>nn.SmoothL1Loss(beta)</code>. Keras: <code>keras.losses.Huber(delta)</code>. scikit-learn: <code>HuberRegressor(epsilon=1.35)</code>, <code>GradientBoostingRegressor</code> (<code>loss='huber'</code>, <code>alpha=0.9</code>). LightGBM: <code>objective='huber'</code> (the threshold is the parameter <code>alpha</code>). XGBoost: <code>objective='reg:pseudohubererror'</code>."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>δ without regard to scale.</b> $\\delta=1$ for prices in dollars and for prices in millions are completely different losses. Normalise the target or set $\\delta$ in units of a robust spread.",
            "<b>Confusing Huber and Smooth L1.</b> They differ by the factor $1/\\beta$: at the same threshold Smooth L1 gives a $\\beta$ times smaller loss and gradient. When swapping one for the other, re-tune the learning rate.",
            "<b>Estimating σ with the ordinary std</b> for the $1.345\\sigma$ rule — outliers inflate the std, the threshold becomes too large, and the protection disappears. Use the MAD.",
            "<b>Expecting Huber to protect against outliers in the features.</b> It limits the influence of a large residual $r$, but a point with an extreme $x$ (high leverage) can still swing the line. That needs other methods (for example, weights based on $x$).",
            "<b>Huber in Newton-step boosting</b> without a check: zero second derivatives of the outliers make leaf steps unstable. Use pseudo-Huber or an implementation that accounts for this.",
            "<b>Comparing loss values at different δ.</b> $L_\\delta$ grows with $\\delta$, other things being equal; compare models by an external metric (MAE, RMSE on validation), not by the loss itself.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../mse/\">MSE</a>: for $\\delta\\ge\\max|r_i|$ the Huber loss equals half the squared error, and the estimate is least squares.",
            "<a href=\"../mae/\">MAE</a>: as $\\delta\\to0$, $L_\\delta/\\delta\\to|r|$; the location estimate tends to the median.",
            "<a href=\"../rmse/\">RMSE</a>: the metric most easily spoiled by outliers; Huber lets you train robustly and still report RMSE on clean data.",
            "<a href=\"../relu/\">ReLU</a> and clipping: $\\psi_\\delta(r)=\\operatorname{clip}(r,-\\delta,\\delta)$ is the same “linear up to a threshold” idea as in ReLU6 and gradient clipping.",
            "<a href=\"../focal/\">Focal Loss</a> is the opposite philosophy: Huber <i>weakens</i> the largest errors (treating them as outliers), while focal loss <i>increases</i> the weight of hard examples relative to easy ones.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $L_\\delta(r)$ is the parabola $\\tfrac12r^2$ for $|r|\\le\\delta$ and the line $\\delta(|r|-\\tfrac12\\delta)$, tangent to it, beyond; the function is convex and $C^1$ but not $C^2$. 2) The derivative $\\psi=\\operatorname{clip}(r,-\\delta,\\delta)$ is bounded — an outlier pulls no harder than $\\delta$; the weight of a point is $\\min(1,\\delta/|r|)$. 3) $\\delta\\to\\infty$ gives MSE and the mean, $\\delta\\to0$ gives MAE and the median. 4) $\\delta=1.345\\sigma$ (σ from the MAD) gives 95% efficiency on normal data. 5) Smooth versions — pseudo-Huber and log-cosh — are needed by second-order methods; Smooth L1 is the same Huber divided by β."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="What is $L_1(3)$ — the Huber loss with $\\delta=1$ for an error of 3?", options=["$4.5$", "$3$", "$2.5$", "$1$"], answer=2,
                 explain="$|r|=3&gt;\\delta$, the linear branch: $1\\cdot(3-0.5)=2.5$. Half the square would give $4.5$."),
            dict(q="What is the largest possible value of $|\\partial L_\\delta/\\partial\\hat y|$?", options=["Unbounded", "$\\delta$", "$\\tfrac12\\delta^2$", "$1$"], answer=1,
                 explain="The derivative is the clipped residual $\\operatorname{clip}(r,-\\delta,\\delta)$, at most $\\delta$ in magnitude."),
            dict(q="What happens at $|r|=\\delta$?", options=["The value jumps", "A kink: the first derivative jumps", "The value and the first derivative are continuous, the second jumps", "Nothing, the function is infinitely smooth"], answer=2,
                 explain="The branches are stitched by the value $\\tfrac12\\delta^2$ and the slope $\\delta$; the second derivative goes from 1 to 0. Hence Huber is $C^1$ but not $C^2$."),
            dict(q="What does Huber’s location estimate tend to as $\\delta\\to0$ and for a very large $\\delta$?", options=["The mean and the median", "The median and the mean", "The mode and the mean", "Zero and infinity"], answer=1,
                 explain="A tiny threshold leaves only the sign of each point — that is the median; a huge threshold makes every point “one of ours” — that is the mean."),
            dict(q="Why is the threshold often set to $1.345\\sigma$?", options=["It makes the estimate unbiased", "It gives 95% efficiency on normal data while keeping robustness", "It discards exactly 5% of the points", "It is the 0.9 quantile of the absolute residuals"], answer=1,
                 explain="At $k=1.345$ the variance of Huber’s estimate on a clean normal sample is only $1/0.95$ times that of the mean, while the influence of outliers is bounded. No points are discarded — far ones simply get smaller weights."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "Regressiya o‘z xatolaridan $r=y-\\hat y$ o‘rganadi. Ikki klassik yo‘qotish «xatoni qanday jazolash» savoliga turlicha javob beradi. <a href=\"../mse/\">MSE</a> kvadrat bilan jazolaydi: u silliq, gradiyenti xatoga proporsional va minimum yaqinida ravon so‘nadi, lekin xatosi 10 bo‘lgan bitta chetga chiquvchi qiymat 1 o‘lchamli yuzta xatoga teng keladi. <a href=\"../mae/\">MAE</a> modul bilan jazolaydi: chetga chiquvchilar unga deyarli ta’sir qilmaydi, ammo nolda sinish bor va gradiyent doim bir xil kattalikda — modelga kichik xatolarni «sayqallash» qiyin."),
        ("p", "Piter Huber 1964 yilda ikkalasining eng yaxshisini olishni taklif qildi: <b>kichik xatolar uchun parabola, katta xatolar uchun to‘g‘ri chiziq</b>, $\\delta$ chegarada almashinadi. Bu g‘oya bugun qayerda ishlaydi:"),
        ("ul", [
            "<b>robast regressiya</b> — scikit-learn’dagi <code>HuberRegressor</code>, statistikadagi M-baholar;",
            "<b>obyektlarni aniqlash</b> — Fast R-CNN va uning avlodlarida ramka koordinatalari regressiyasi uchun Smooth L1; bu ko‘paytuvchi aniqligida Huber;",
            "<b>mustahkamlab o‘qitish</b> — DQN’da vaqtli farq xatosi $[-1;\\,1]$ gacha kesiladi, bu $\\delta=1$ dagi Huber yo‘qotishiga teng kuchli;",
            "<b>gradiyentli busting</b> — scikit-learn’da <code>loss='huber'</code>, LightGBM’da <code>objective='huber'</code>, XGBoost’da psevdo-Huber;",
            "<b>anomaliyali har qanday ma’lumot</b> — ko‘chmas mulk narxlari, datchik ko‘rsatkichlari, xatoli belgilash.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "$L_\\delta(r)$ $|r|\\le\\delta$ da $\\tfrac12r^2$ ga, undan tashqarida $\\delta(|r|-\\tfrac12\\delta)$ ga teng. $|r|=\\delta$ nuqtada qiymatlar ($\\tfrac12\\delta^2$) ham, qiyaliklar ($\\delta$) ham mos tushadi. $\\psi(r)=\\operatorname{clip}(r,-\\delta,\\delta)$ hosila chegaralangan: chetga chiquvchi qiymat modelni $\\delta$ dan kuchliroq tortmaydi. Kichik $\\delta$ — MAE’ga yaqinroq, katta $\\delta$ — MSE’ga."),
    ]),
    dict(id="intuition", title="Intuitsiya: to‘g‘ri dumli parabola", blocks=[
        ("p", "Bashoratni javobga tortadigan prujinani tasavvur qiling. Xato kichik ekan, prujina oddiy: qancha cho‘zilsa, shuncha kuchli tortadi — bu $\\tfrac12r^2$ parabola. Lekin prujinada saqlagich bor: $\\delta$ cho‘zilishdan keyin kuch o‘sishdan to‘xtaydi va $\\delta$ ga teng bo‘lib qoladi. Bunday prujinaning energiyasi shundan keyin faqat chiziqli o‘sadi — bular to‘g‘ri dumlar."),
        ("p", "Nuqtani grafik bo‘ylab torting va $\\delta$ ni o‘zgartiring. Firuza $|r|\\le\\delta$ yo‘lak ichida ko‘k egri chiziq kulrang parabolada, tashqarida esa $\\delta(|r|-\\delta/2)$ shtrixli to‘g‘ri chiziqda yotadi. To‘q sariq urinma tutashuvdan sinishsiz o‘tadi."),
        ("viz", "huber-explorer", {"delta": 1, "r": 2}, "<b>1-rasm.</b> $L_\\delta(r)$ Huber yo‘qotishi va uning hosilalari. Pastda: to‘q sariq $\\psi(r)=L'_\\delta(r)$ yo‘lak ichida qiya, tashqarida gorizontal; binafsha $L''_\\delta$ — zinapoya: ichkarida 1, tashqarida 0. $\\delta=1$ va $r=2$ da: $\\tfrac12r^2=2$ o‘rniga $L=1{,}5$, qiyalik esa 2 emas, 1."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "$|r|=\\delta$ tutashuvda egri chiziq paraboladan to‘g‘ri chiziqqa ravon o‘tadi: $\\delta(|r|-\\delta/2)$ to‘g‘ri chiziq $r=\\pm\\delta$ nuqtada parabolaga <i>urinma</i>. Sakrash faqat ikkinchi hosilada bor: egrilik 1 dan 0 ga tushadi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("eq", r"L_\delta(r)=\begin{cases}\tfrac12 r^2, & |r|\le\delta,\\[1mm] \delta\bigl(|r|-\tfrac12\delta\bigr), & |r|>\delta,\end{cases}\qquad r=y-\hat y"),
        ("symbols", [
            (r"r=y-\hat y", "qoldiq (residual): $y$ javob $\\hat y$ bashoratdan qanchalik yuqori; yo‘qotish faqat $|r|$ ga bog‘liq, ishora ahamiyatsiz;"),
            (r"\delta>0", "chegara: $\\delta$ dan kichik xatolar «oddiy shovqin», kattalari shubhali hisoblanadi; $y$ birliklarida o‘lchanadi;"),
            (r"\tfrac12 r^2", "kvadratik tarmoq — MSE’dagi kabi xato kvadratining aynan yarmi; $\\tfrac12$ ko‘paytuvchi hosilani $r$ ga teng qiladi;"),
            (r"\delta|r|", "chiziqli tarmoq — MAE’dagi kabi $\\delta$ vaznli xato moduli;"),
            (r"-\tfrac12\delta^2", "tarmoqlarni tikadigan pastga siljish: usiz $\\delta|r|$ to‘g‘ri chiziq $|r|=\\delta$ da $\\delta^2$ berardi, parabola esa $\\tfrac12\\delta^2$ beradi."),
        ]),
        ("p", "Tikishni tekshiramiz. $|r|=\\delta$ da kvadratik tarmoq $\\tfrac12\\delta^2$, chiziqlisi $\\delta(\\delta-\\tfrac12\\delta)=\\tfrac12\\delta^2$ beradi: qiymatlar teng. Hosilalar: parabolada $r=\\delta$, to‘g‘ri chiziqda $\\delta\\operatorname{sign}r=\\delta$ — qiyaliklar ham teng. $-\\tfrac12\\delta^2$ o‘zgarmas aynan to‘g‘ri chiziq parabolaga urinma bo‘lishi uchun tanlangan."),
        ("table", ["$r$", "$\\tfrac12r^2$", "$|r|$", "$L_1(r)$", "$\\psi_1(r)$"], "TABLE", {"num": [0, 1, 2, 3, 4]}),
        ("p", "$\\delta=1$ uchun jadval asosiy narsani ko‘rsatadi: 10 xatoda kvadrat 50 beradi, Huber esa — 9,5; hosila (oxirgi ustun) esa hech qachon 1 dan oshmaydi."),
        ("h3", "Umumiy misol"),
        ("p", "Qo‘llanmadagi misolni olamiz: $y=(3;\\,5;\\,8)$, $\\hat y=(2{,}5;\\,5;\\,10)$, xatolar $r=(0{,}5;\\,0;\\,-2)$. $\\delta=1$ da birinchi xato parabolaga tushadi: $\\tfrac12\\cdot0{,}5^2=0{,}125$; ikkinchisi — nol; uchinchisi, $|r|=2&gt;1$, — to‘g‘ri chiziqqa: $1\\cdot(2-0{,}5)=1{,}5$. O‘rtacha $(0{,}125+0+1{,}5)/3\\approx0{,}542$."),
        ("p", "Gradiyentlar qiziqroq. MSE yarmida ular xatolarning o‘ziga teng: $(0{,}5;\\,0;\\,-2)$ — chetga chiquvchi birinchi nuqtadan to‘rt marta kuchliroq tortadi. Huber’da $\\psi=(0{,}5;\\,0;\\,-1)$ — faqat ikki marta: katta xato qolganlarini bosib keta olmaydi."),
        ("h3", "Masshtab: barcha δ uchun bitta egri chiziq"),
        ("p", "Agar xatoni chegara birliklarida o‘lchasak, barcha Huber yo‘qotishlari bitta egri chiziqdir:"),
        ("eq", r"L_\delta(r)=\delta^2\,L_1\!\left(\frac{r}{\delta}\right)"),
        ("p", "Shuning uchun $\\delta$ ni «umuman» tanlab bo‘lmaydi: u $y$ birliklariga bog‘liq. 1 so‘mlik va 1 million so‘mlik xato — turli narsalar. Odatda $\\delta$ shovqinning tipik tarqoqligi $\\sigma$ ulushlarida beriladi ($\\delta$ tanlovi bo‘limiga qarang)."),
    ]),
    dict(id="properties", title="Xossalar", blocks=[
        ("ul", [
            "<b>Manfiy emas va juft</b>: $L_\\delta(r)\\ge0$, $L_\\delta(-r)=L_\\delta(r)$, $0$ minimum faqat $r=0$ da.",
            "<b>Qavariq</b>: parabola va uning urinmasi «chuqurliksiz» yopishtirilgan; demak, Huber yo‘qotishli chiziqli regressiyada soxta lokal minimumlar yo‘q.",
            "<b>$C^1$ silliqlik, lekin $C^2$ emas</b>: birinchi hosila uzluksiz, ikkinchisi $|r|=\\delta$ da 1 dan 0 ga sakraydi.",
            "<b>Parabola va to‘g‘ri chiziq orasida qisilgan</b>: $\\delta|r|-\\tfrac12\\delta^2\\le L_\\delta(r)\\le\\tfrac12r^2$; egri chiziq ulardan biri bilan mos kelmagan joyda farq $\\tfrac12(|r|-\\delta)^2$ ga teng.",
            "<b>Chegaralangan hosila</b>: $|L'_\\delta(r)|\\le\\delta$ — robastlik uchun asosiy xossa.",
            "<b>Limitlar</b>: $\\delta\\to\\infty$ da $L_\\delta(r)\\to\\tfrac12r^2$ (MSE), $\\delta\\to0$ da $L_\\delta(r)/\\delta\\to|r|$ (MAE).",
        ]),
        ("deep", "Nega egri chiziq qisilgan va limitlar qayerdan", [
            ("p", "$|r|&gt;\\delta$ da: $\\tfrac12r^2-\\bigl(\\delta|r|-\\tfrac12\\delta^2\\bigr)=\\tfrac12(|r|-\\delta)^2\\ge0$, ya’ni to‘g‘ri chiziq paraboladan pastda yotadi. $|r|\\le\\delta$ da xuddi shu ifoda parabola to‘g‘ri chiziqdan yuqorida ekanini ko‘rsatadi. Demak, $L_\\delta$ doim ular orasida va har biri bilan o‘z qismida mos keladi."),
            ("p", "Limitlar: agar $\\delta\\ge|r|$ bo‘lsa, $L_\\delta(r)=\\tfrac12r^2$ aynan — yetarlicha katta chegara kifoya. Agar $\\delta&lt;|r|$ bo‘lsa, $\\delta\\to0$ da $L_\\delta(r)/\\delta=|r|-\\tfrac12\\delta\\to|r|$."),
        ]),
        ("deep", "Huber «yumshatilgan modul» sifatida (Moro qobig‘i)", [
            ("p", "Nafis ekvivalent yozuv bor: agar xatoning $z$ qismini modul narxida «hisobdan chiqarish» mumkin bo‘lsa, Huber yo‘qotishi eng yaxshi murosadir:"),
            ("eq", r"L_\delta(r)=\min_{z\in\mathbb R}\Bigl(\tfrac12(r-z)^2+\delta|z|\Bigr)"),
            ("p", "Minimumga $z^*=\\operatorname{sign}(r)\\max(|r|-\\delta,\\,0)$ yumshoq chegarada erishiladi. Agar $|r|\\le\\delta$ bo‘lsa, $z^*=0$ va $\\tfrac12r^2$ qoladi. Aks holda $z^*=r-\\delta\\operatorname{sign}r$, va $\\tfrac12\\delta^2+\\delta(|r|-\\delta)=\\delta|r|-\\tfrac12\\delta^2$ hosil bo‘ladi. Qavariq tahlilda bu $\\delta|\\cdot|$ funksiyaning Moro qobig‘i deyiladi: u silliq bo‘lmagan modulni cheksizlikdagi xulqi o‘sha bo‘lgan silliq funksiyaga aylantiradi."),
            ("p", "Modelli talqin: $y=\\hat y+\\text{shovqin}+z$, bu yerda $z$ — kamdan-kam «anomaliya». Huber yo‘qotishi xatoning qaysi qismini anomaliya, qaysi qismini gauss shovqini bilan tushuntirishni o‘zi hal qiladi."),
        ]),
    ]),
    dict(id="derivative", title="Hosila: kesilgan qoldiq", blocks=[
        ("p", "Statistikada qoldiq bo‘yicha hosila $\\psi$ bilan belgilanadi va ta’sir funksiyasi (influence function) deyiladi: u bitta nuqta bahoni qanday kuch bilan tortishini ko‘rsatadi."),
        ("eq", r"\psi_\delta(r)=L'_\delta(r)=\begin{cases}r, & |r|\le\delta,\\ \delta\operatorname{sign}r, & |r|>\delta\end{cases}=\operatorname{clip}(r,\,-\delta,\,\delta)"),
        ("deep", "Qadam-baqadam keltirib chiqarish", [
            ("p", "Yo‘lak ichida $(\\tfrac12r^2)'=r$. Tashqarida $|r|$ ning hosilasi $\\operatorname{sign}r$, shuning uchun $\\bigl(\\delta|r|-\\tfrac12\\delta^2\\bigr)'=\\delta\\operatorname{sign}r$. $r=\\pm\\delta$ nuqtalarda chap va o‘ng hosilalar mos keladi ($\\pm\\delta$), demak, hosila mavjud va uzluksiz."),
            ("p", "Bashorat bo‘yicha — zanjir qoidasi: $\\dfrac{\\partial L_\\delta}{\\partial\\hat y}=\\psi_\\delta(r)\\cdot\\dfrac{\\partial r}{\\partial\\hat y}=-\\psi_\\delta(y-\\hat y)$."),
            ("p", "Ikkinchi hosila: $|r|&lt;\\delta$ da $L''_\\delta(r)=1$, $|r|&gt;\\delta$ da $0$; $\\pm\\delta$ nuqtalarda u yo‘q — chap va o‘ng hosilalar mos kelmaydi."),
        ]),
        ("eq", r"\frac{\partial L_\delta}{\partial\hat y}=-\operatorname{clip}\bigl(y-\hat y,\,-\delta,\,\delta\bigr)"),
        ("p", "Uch yo‘qotishni taqqoslang. MSE’da ($\\tfrac12r^2$) $\\psi=r$ tortish chegarasiz o‘sadi. MAE’da tortish o‘zgarmas. Huber’da u nuqta «o‘zimizniki» ekan o‘sadi va nuqta shubhali bo‘lganda $\\delta$ darajasida to‘xtaydi. Ikkinchi foydali rasm — nuqtaning <b>vazni</b> $w(r)=\\psi(r)/r$: nuqta oddiy eng kichik kvadratlar usuliga (EKKU) nisbatan «ovoz»ning qancha ulushini oladi."),
        ("viz", "huber-influence", {"delta": 1, "r": 4}, "<b>2-rasm.</b> Chapda — $\\psi(r)$ tortish, o‘ngda — $w(r)=\\psi(r)/r$ vazn. $\\delta=1$ da $r=4$ xatoli nuqta MSE’da 4 kuch bilan, Huber’da 1 kuch bilan tortadi, ya’ni $0{,}25$ vazn oladi. $|r|\\le\\delta$ yo‘lak ichida vazn 1 ga teng: Huber oddiy nuqtalarga tegmaydi."),
        ("callout", "note", "Nega ψ yo‘qotishning o‘zidan muhimroq", "Model optimumi yo‘qotish qiymati bilan emas, $\\sum_i\\psi(r_i)\\,\\partial\\hat y_i/\\partial\\theta=0$ tenglama bilan aniqlanadi. Shuning uchun robastlik — $\\psi$ ning xossasi: chegaralangan $\\psi$ hech bir yolg‘iz chetga chiquvchi yechimni istalgancha uzoqqa sura olmasligini bildiradi. MSE’da $\\psi$ chegaralanmagan va bitta chetga chiquvchi o‘rtachani istalgan joyga suradi."),
    ]),
    dict(id="surface", title="L(r, δ) sirti 3D’da", blocks=[
        ("p", "Yo‘qotishni ikki o‘zgaruvchi — $r$ xato va $\\delta$ chegara funksiyasi sifatida ko‘raylik. Bu butun egri chiziqlar oilasini birdaniga va chegara shaklni qanday o‘zgartirishini ko‘rishga yordam beradi."),
        ("viz", "huber-surface", {"delta": 1}, "<b>3-rasm.</b> Chapda — $L_\\delta(r)$ sirti (uni aylantirish mumkin), to‘q sariq chiziqlar — $|r|=\\delta$ tutashuv, ko‘k — tanlangan $\\delta$ dagi kesim. O‘ngda — sath chiziqlari bilan yuqoridan ko‘rinish. $|r|\\le\\delta$ «pona» ichida chiziqlar vertikal, tashqarida egiladi. Psevdo-Huber’ga o‘tkazing: tutashuv yo‘qoladi, sirt hamma joyda silliq."),
        ("p", "Ikki narsa darhol ko‘rinadi. Birinchidan, tutashuv ostida, $|r|\\le\\delta$ da, sirt $\\delta$ ga bog‘liq emas: u yerda doim $\\tfrac12r^2$, va $L=c$ sath chiziqlari — $r=\\pm\\sqrt{2c}$ vertikal to‘g‘ri chiziqlar. Ikkinchidan, tashqarida $L=c$ sath chizig‘i — $|r|=c/\\delta+\\delta/2$: chegara qancha kichik bo‘lsa, o‘sha yo‘qotishni yig‘ish uchun shuncha uzoqqa borish kerak."),
        ("callout", "note", "Ko‘p o‘lchovli holat", "Javob vektor bo‘lganda (masalan, aniqlashda ramkaning to‘rtta koordinatasi), Huber yo‘qotishi odatda har bir koordinata bo‘yicha hisoblanib qo‘shiladi: $\\sum_jL_\\delta(r_j)$. Bunday yig‘indining $(r_1,r_2)$ tekislikdagi sath chiziqlari — burchaklari yumaloqlangan kvadratlar, gradiyent esa har bir koordinata bo‘yicha alohida kesiladi. Bu butun xato vektorining uzunligi kesiladigan $L_\\delta(\\|r\\|)$ bilan bir xil emas."),
    ]),
    dict(id="statistics", title="Huber bahosi va δ tanlovi", blocks=[
        ("p", "Huber o‘z funksiyasini statistikaning eng oddiy masalasi — $x_1,\\dots,x_n$ tanlanma markazini baholash uchun o‘ylab topgan. $\\sum(x_i-\\mu)^2$ ni minimallashtirsak, o‘rtacha; $\\sum|x_i-\\mu|$ ni — mediana chiqadi. Huber bahosi $\\hat\\mu$ $\\sum L_\\delta(x_i-\\mu)$ ni minimallashtiradi, ya’ni quyidagi tenglamani yechadi"),
        ("eq", r"\sum_{i=1}^{n}\psi_\delta(x_i-\hat\mu)=0"),
        ("p", "$|x_i-\\hat\\mu|\\le\\delta$ zona ichidagi nuqtalar o‘rtachadagi kabi qatnashadi, uzoqdagilari esa medianadagi kabi faqat ishorasi bilan, $\\delta$ kuch bilan."),
        ("viz", "huber-location", {"delta": 1}, "<b>4-rasm.</b> 5 atrofidagi 13 qiymat va ikkita chetga chiquvchi (qizil; o‘ngdagisini tortish mumkin). Ustun balandligi — nuqtaning bahodagi vazni. $\\delta=1$ da: o‘rtacha $6{,}079$, mediana $5{,}557$, Huber bahosi $5{,}369$ — haqiqiy markaz 5 ga hammadan yaqin. O‘ngda — $\\hat\\mu(\\delta)$ yo‘li: $\\delta\\to0$ da baho medianaga intiladi, $\\delta\\ge7{,}42$ da esa o‘rtacha bilan mos tushadi."),
        ("p", "O‘ng grafikka e’tibor bering: $\\hat\\mu(\\delta)$ yo‘li mediana va o‘rtacha orasida yotishi <b>shart emas</b> — $\\delta=1$ da baho ikkalasidan ham past. Limit qiymatlar aniq: $\\delta\\to0$ da mediana chiqadi, $\\delta$ o‘rtachadan eng uzoq nuqtagacha masofadan oshishi bilan (bu yerda $13{,}5-6{,}079\\approx7{,}42$) barcha nuqtalar kvadratik zonada va $\\hat\\mu$ o‘rtachaga teng."),
        ("h3", "Robastlik narxi: 1,345σ qoidasi"),
        ("p", "Agar ma’lumotlar haqiqatan normal va chetga chiquvchilarsiz bo‘lsa, eng yaxshi baho — o‘rtacha. Huber qanchalik yomonroq? Buni <b>asimptotik samaradorlik</b> o‘lchaydi: o‘rtacha dispersiyasining baho dispersiyasiga nisbati. $k$ chegarali ($\\sigma$ birliklarida) $\\psi$ uchun standart normal $X$ da:"),
        ("eq", r"\operatorname{Var}\hat\mu\approx\frac{\sigma^2}{n}\cdot\frac{\mathbb E\,\psi_k(X)^2}{\bigl(\mathbb E\,\psi'_k(X)\bigr)^2},\qquad \mathbb E\,\psi'_k=2\Phi(k)-1,\quad \mathbb E\,\psi_k^2=2\Phi(k)-1-2k\varphi(k)+2k^2\bigl(1-\Phi(k)\bigr)"),
        ("p", "«Samaradorlik $=95\\%$» ni yechsak, $k\\approx1{,}345$ chiqadi. Klassik $\\delta=1{,}345\\,\\sigma$ tanlovi shundan: chetga chiquvchilardan himoya evaziga toza ma’lumotlarda atigi 5% yo‘qotish. Medianing samaradorligi $2/\\pi\\approx64\\%$."),
        ("viz", "huber-efficiency", {"k": 1.345, "eps": 0.05}, "<b>5-rasm.</b> $(1-\\varepsilon)N(0,1)+\\varepsilon N(0,10^2)$ aralashma uchun markaz bahosi dispersiyasi ($\\sigma^2/n$ birliklarida). $k=1{,}345$ da toza ma’lumotlardagi samaradorlik — $95{,}0\\%$. $\\varepsilon=0{,}05$ da o‘rtacha dispersiyasi $5{,}95$, mediananiki $1{,}722$, $k=1{,}345$ li Huber’niki $1{,}229$; bu aralashma uchun eng yaxshi chegara $k\\approx1{,}48$ (bo‘sh doiracha)."),
        ("callout", "history", "Huber minimaksi", "1964 yilgi maqolada Huber ko‘proq narsani isbotladi: agar qanday chetga chiquvchilar uchrashi noma’lum bo‘lib, faqat ularning $\\varepsilon$ ulushi ma’lum bo‘lsa, $\\psi_k$ li baho <i>eng yomon holdagi</i> dispersiyani minimallashtiradi. Chegara ulush bilan $2\\varphi(k)/k-2\\Phi(-k)=\\varepsilon/(1-\\varepsilon)$ tenglama orqali bog‘langan: $\\varepsilon=0{,}05$ uchun bu $k\\approx1{,}40$, $\\varepsilon=0{,}01$ uchun $k\\approx1{,}95$."),
        ("callout", "warn", "σ ni ham robast baholash kerak", "Agar $\\sigma$ oddiy standart chetlanish bilan hisoblansa, $\\delta=1{,}345\\sigma$ qoidasi foydasiz: chetga chiquvchilar uni shishiradi. Median absolyut chetlanishdan foydalaning: $\\hat\\sigma=\\operatorname{MAD}/0{,}6745\\approx1{,}4826\\cdot\\operatorname{median}|r_i-\\operatorname{median}(r)|$. <code>HuberRegressor</code>’da masshtab koeffitsiyentlar bilan birga baholanadi, standart <code>epsilon=1.35</code> esa aynan $k$."),
    ]),
    dict(id="training", title="O‘qitishda Huber", blocks=[
        ("p", "To‘g‘ri chiziqni gradiyent tushish bilan ikki usulda — MSE yarmida va Huber yo‘qotishida — bir xil ma’lumotlarda o‘qitamiz: $\\sigma=0{,}5$ shovqinli $y=1+0{,}5x$ atrofidagi 30 nuqta va pastki o‘ngda uchta chetga chiquvchi. Chegara $\\delta=0{,}7\\approx1{,}345\\cdot0{,}5$."),
        ("viz", "huber-regression", {"delta": 0.7}, "<b>6-rasm.</b> «Boshlash»ni bosing. Ikkala model $y=0$ to‘g‘ri chiziqdan boshlaydi va bir xil qadamlar qiladi ($\\eta=0{,}15$). MSE tezda $0{,}363$ qiyalikka yaqinlashadi — chetga chiquvchilar to‘g‘ri chiziqni ag‘daradi. Huber avvaliga sekinroq yuradi (barcha xatolar katta va har biri $\\delta$ dan kuchli tortmaydi), lekin haqiqiy $0{,}5$ ga qarshi $0{,}511$ qiyalikka keladi. Chetdagi chetga chiquvchini torting — o‘qitish paytida yoki undan oldin."),
        ("p", "Tushish qadami mexanizmni ko‘rsatadi: har bir nuqta parametrlarni $\\psi(r_i)$ ga proporsional tortadi. To‘g‘ri chiziq barcha nuqtalardan uzoq ekan, Huber’da barcha tortishlar $\\pm\\delta$ ga teng — u MAE kabi o‘zgarmas tezlikda harakatlanadi. To‘g‘ri chiziq nuqtalarning asosiy qismiga yaqinlashganda ularning xatolari kvadratik zonaga tushadi va tushish oddiy EKKU’ga aylanadi — endi $\\delta$ «arqonida» qolgan chetga chiquvchilarsiz."),
        ("eq", r"\theta\leftarrow\theta+\eta\,\frac1n\sum_{i=1}^{n}\psi_\delta\bigl(y_i-\hat y_i\bigr)\,\frac{\partial\hat y_i}{\partial\theta}"),
        ("deep", "IRLS: Huber vaznli EKKU sifatida", [
            ("p", "$\\hat y_i=x_i^\\top\\beta$ chiziqli model uchun $\\sum_i\\psi(r_i)x_i=0$ optimallik shartini $w_i=\\psi(r_i)/r_i=\\min(1,\\delta/|r_i|)$ vaznlar bilan $\\sum_iw_ir_ix_i=0$ ko‘rinishida qayta yozish mumkin. Vaznlar muzlatilsa, bu vaznli EKKU’ning oshkor yechiladigan normal tenglamalari:"),
            ("eq", r"\beta^{(t+1)}=\bigl(X^\top W^{(t)}X\bigr)^{-1}X^\top W^{(t)}y,\qquad W^{(t)}=\operatorname{diag}\bigl(w_i(\beta^{(t)})\bigr)"),
            ("p", "«Qoldiqlarni hisoblash → vaznlarni yangilash → EKKU’ni yechish» iteratsiyalari (iteratively reweighted least squares) o‘nga yaqin qadamda Huber bahosiga yaqinlashadi. Vaznlar 2-rasmning o‘ng qismidagilarning o‘zi."),
        ]),
        ("h3", "Huber o‘qitish ichida yana qayerda ishlaydi"),
        ("ul", [
            "<b>Gradiyentli busting.</b> Har bir yangi daraxt yo‘qotishning antigradiyentini o‘rganadi. Huber uchun bu $\\psi(r_i)$ — <i>kesilgan</i> qoldiqlar, shuning uchun bitta anomal qiymat daraxtni chetga chiquvchiga barg sarflashga majburlamaydi. scikit-learn’da $\\delta$ chegara har iteratsiyada $|r_i|$ ning $\\alpha$-kvantili sifatida olinadi (standart $\\alpha=0{,}9$).",
            "<b>DQN.</b> DeepMind maqolasida (2015) vaqtli farq xatosi $[-1;\\,1]$ gacha kesilgan. Kesilgan gradiyent — aynan $\\psi_1$, ya’ni $\\delta=1$ dagi Huber yo‘qotishida o‘qitish: kamdan-kam ulkan mukofotlar tarmoqni buzmaydi.",
            "<b>Fast R-CNN.</b> Ramka koordinatalari regressiyasi uchun Girshik (2015) Smooth L1 ni oldi: u «chetga chiquvchilarga L2 dan kamroq sezgir» va gradiyent portlashidan qochish uchun o‘qitish tezligini sinchiklab sozlashni talab qilmaydi.",
        ]),
    ]),
    dict(id="variants", title="Silliq qarindoshlar: psevdo-Huber, log-cosh, Smooth L1", blocks=[
        ("p", "Ikkinchi hosiladagi sakrash gradiyent tushishga xalaqit bermaydi, lekin ikkinchi tartibli usullarga xalaqit beradi. XGBoost va LightGBM Nyuton qadamini qiladi: barg $-\\sum g_i/\\sum h_i$ qiymat oladi, bu yerda $h_i$ — ikkinchi hosilalar. Huber’ning haqiqiy ikkinchi hosilasi barcha chetga chiquvchilar uchun nolga teng, va bargga faqat ular tushsa, maxraj nolga aylanadi. Shuning uchun realizatsiyalar uni yo o‘zgarmas bilan almashtiradi (LightGBM <code>objective='huber'</code> da shunday qiladi), yoki silliq variantni oladi."),
        ("eq", r"\text{psevdo-Huber: }\;\delta^2\Bigl(\sqrt{1+(r/\delta)^2}-1\Bigr),\qquad \text{log-cosh: }\;\delta^2\ln\cosh\frac{r}{\delta},\qquad \text{Smooth L1: }\;\frac{L_\beta(r)}{\beta}"),
        ("viz", "huber-variants", {"variant": "pseudo", "delta": 1, "r": 3}, "<b>7-rasm.</b> Bir xil $\\delta$ da Huber va uning qarindoshlari. Psevdo-Huber va log-cosh ham nol atrofida $\\tfrac12r^2$ kabi, dumlarda $\\delta|r|$ kabi o‘zini tutadi, lekin o‘tish ravon, ikkinchi hosila (pastdagi belgi) esa uzluksiz. $\\delta=1$, $r=3$ da: Huber $2{,}5$, psevdo-Huber $2{,}162$, log-cosh $2{,}309$."),
        ("ul", [
            "<b>Psevdo-Huber</b> (kompyuter ko‘rishida $\\delta$ ko‘paytuvchi aniqligida — Sharbonye yo‘qotishi $\\sqrt{r^2+\\delta^2}-\\delta$): $r/\\sqrt{1+(r/\\delta)^2}$ hosila $\\pm\\delta$ ga sekin intiladi; $(1+(r/\\delta)^2)^{-3/2}$ ikkinchi hosila hamma joyda musbat. XGBoost’da — <code>huber_slope</code> ($=\\delta$) parametrli <code>objective='reg:pseudohubererror'</code>.",
            "<b>log-cosh</b>: $\\delta\\tanh(r/\\delta)$ hosila — silliq «kesish»; dumlarda $\\delta^2\\ln\\cosh(r/\\delta)\\approx\\delta|r|-\\delta^2\\ln2$.",
            "<b>Smooth L1</b> — $\\beta$ ga bo‘lingan Huber: $|r|&lt;\\beta$ da $\\tfrac{0{,}5r^2}{\\beta}$ va undan tashqarida $|r|-\\tfrac12\\beta$. $\\beta\\to0$ da u $|r|$ ga intiladi (Huber esa nolga). PyTorch’da: <code>HuberLoss(delta=δ) = δ · SmoothL1Loss(beta=δ)</code>.",
        ]),
    ]),
    dict(id="code", title="Kodda", blocks=[
        ("p", "Formulaning o‘zi — <code>np.where</code> bilan bitta qator. Gradiyent — <code>np.clip</code>. Quyida — realizatsiya, umumiy misolda tekshirish va IRLS orqali Huber regressiyasi."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_IRLS"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Tayyor realizatsiyalar", "PyTorch: <code>nn.HuberLoss(delta)</code>, <code>nn.SmoothL1Loss(beta)</code>. Keras: <code>keras.losses.Huber(delta)</code>. scikit-learn: <code>HuberRegressor(epsilon=1.35)</code>, <code>GradientBoostingRegressor</code> (<code>loss='huber'</code>, <code>alpha=0.9</code>). LightGBM: <code>objective='huber'</code> (chegara — <code>alpha</code> parametri). XGBoost: <code>objective='reg:pseudohubererror'</code>."),
    ]),
    dict(id="mistakes", title="Keng tarqalgan xatolar", blocks=[
        ("ol", [
            "<b>Masshtabni hisobga olmagan δ.</b> Dollardagi narxlar va milliondagi narxlar uchun $\\delta=1$ — butunlay turli yo‘qotishlar. Maqsadli o‘zgaruvchini normallang yoki $\\delta$ ni robast tarqoqlik birliklarida bering.",
            "<b>Huber va Smooth L1 ni chalkashtirish.</b> Ular $1/\\beta$ ko‘paytuvchiga farq qiladi: bir xil chegarada Smooth L1 $\\beta$ marta kichik yo‘qotish va gradiyent beradi. Birini boshqasiga almashtirganda o‘qitish tezligini qayta sozlang.",
            "<b>$1{,}345\\sigma$ qoidasi uchun σ ni oddiy std bilan baholash</b> — chetga chiquvchilar std ni shishiradi, chegara juda katta bo‘lib qoladi va himoya yo‘qoladi. MAD dan foydalaning.",
            "<b>Huber belgilardagi chetga chiquvchilardan qutqaradi deb kutish.</b> U katta $r$ qoldiqning ta’sirini cheklaydi, lekin ekstremal $x$ li nuqta (yuqori richag, leverage) baribir to‘g‘ri chiziqni burib yuborishi mumkin. Buning uchun boshqa usullar kerak (masalan, $x$ bo‘yicha vaznlar).",
            "<b>Nyuton usulli bustingda Huber</b> tekshiruvsiz: chetga chiquvchilarning nol ikkinchi hosilalari barg qadamlarini beqaror qiladi. Psevdo-Huber’dan yoki buni hisobga oladigan realizatsiyadan foydalaning.",
            "<b>Turli δ dagi yo‘qotish qiymatlarini taqqoslash.</b> Boshqa shartlar teng bo‘lsa, $L_\\delta$ qiymati $\\delta$ bilan o‘sadi; modellarni yo‘qotishning o‘zi bilan emas, tashqi metrika (validatsiyadagi MAE, RMSE) bilan taqqoslang.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘liqlik", blocks=[
        ("ul", [
            "<a href=\"../mse/\">MSE</a>: $\\delta\\ge\\max|r_i|$ da Huber yo‘qotishi xato kvadratining yarmiga, baho esa EKKU’ga teng.",
            "<a href=\"../mae/\">MAE</a>: $\\delta\\to0$ da $L_\\delta/\\delta\\to|r|$; markaz bahosi medianaga intiladi.",
            "<a href=\"../rmse/\">RMSE</a>: chetga chiquvchilar eng oson buzadigan metrika; Huber barqaror o‘qitish va toza ma’lumotlarda RMSE bo‘yicha hisobot berish imkonini beradi.",
            "<a href=\"../relu/\">ReLU</a> va kesish: $\\psi_\\delta(r)=\\operatorname{clip}(r,-\\delta,\\delta)$ — ReLU6 va gradient clipping’dagi «chegaragacha chiziqli» g‘oyaning o‘zi.",
            "<a href=\"../focal/\">Focal Loss</a> — qarama-qarshi falsafa: Huber eng katta xatolarni <i>susaytiradi</i> (ularni chetga chiquvchi deb hisoblab), focal loss esa qiyin misollar vaznini oson misollarga nisbatan <i>oshiradi</i>.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $L_\\delta(r)$ — $|r|\\le\\delta$ da $\\tfrac12r^2$ parabola va undan tashqarida unga urinma $\\delta(|r|-\\tfrac12\\delta)$ to‘g‘ri chiziq; funksiya qavariq va $C^1$, lekin $C^2$ emas. 2) $\\psi=\\operatorname{clip}(r,-\\delta,\\delta)$ hosila chegaralangan — chetga chiquvchi $\\delta$ dan kuchli tortmaydi; nuqta vazni $\\min(1,\\delta/|r|)$. 3) $\\delta\\to\\infty$ — MSE va o‘rtacha, $\\delta\\to0$ — MAE va mediana. 4) $\\delta=1{,}345\\sigma$ (σ MAD bo‘yicha) normal ma’lumotlarda 95% samaradorlik beradi. 5) Silliq versiyalar — psevdo-Huber va log-cosh — ikkinchi tartibli usullarga kerak; Smooth L1 — β ga bo‘lingan o‘sha Huber."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="$L_1(3)$ — $\\delta=1$ li Huber yo‘qotishi 3 xatoda nimaga teng?", options=["$4{,}5$", "$3$", "$2{,}5$", "$1$"], answer=2,
                 explain="$|r|=3&gt;\\delta$, chiziqli tarmoq: $1\\cdot(3-0{,}5)=2{,}5$. Kvadrat yarmi $4{,}5$ berardi."),
            dict(q="$|\\partial L_\\delta/\\partial\\hat y|$ eng katta qanday qiymat qabul qilishi mumkin?", options=["Chegaralanmagan", "$\\delta$", "$\\tfrac12\\delta^2$", "$1$"], answer=1,
                 explain="Hosila — $\\operatorname{clip}(r,-\\delta,\\delta)$ kesilgan qoldiq, moduli $\\delta$ dan oshmaydi."),
            dict(q="$|r|=\\delta$ nuqtada nima bo‘ladi?", options=["Qiymat uziladi", "Sinish: birinchi hosila sakraydi", "Qiymat va birinchi hosila uzluksiz, ikkinchisi sakraydi", "Hech narsa, funksiya cheksiz silliq"], answer=2,
                 explain="Tarmoqlar $\\tfrac12\\delta^2$ qiymat va $\\delta$ qiyalik bo‘yicha tikilgan; ikkinchi hosila 1 dan 0 ga o‘tadi. Shuning uchun Huber — $C^1$, lekin $C^2$ emas."),
            dict(q="$\\delta\\to0$ da va juda katta $\\delta$ da Huber markaz bahosi nimaga intiladi?", options=["O‘rtacha va medianaga", "Mediana va o‘rtachaga", "Moda va o‘rtachaga", "Nol va cheksizlikka"], answer=1,
                 explain="Kichik chegara har bir nuqtadan faqat ishorani qoldiradi — mediana chiqadi; katta chegara barcha nuqtalarni «o‘zimizniki» qiladi — o‘rtacha chiqadi."),
            dict(q="Nega chegara ko‘pincha $1{,}345\\sigma$ ga teng olinadi?", options=["Shunda baho siljimagan bo‘ladi", "Bu robastlikni saqlagan holda normal ma’lumotlarda 95% samaradorlik", "Shunda aynan 5% nuqta tashlab yuboriladi", "Bu qoldiqlar modulining 0,9 kvantili"], answer=1,
                 explain="$k=1{,}345$ da toza normal tanlanmada Huber bahosi dispersiyasi o‘rtacha dispersiyasidan atigi $1/0{,}95$ marta katta; bunda chetga chiquvchilar ta’siri cheklangan. Hech qanday nuqta tashlanmaydi — uzoqdagilari shunchaki kichikroq vazn oladi."),
        ]),
    ]),
],
}

# Fill in the shared pieces (table rows and code listings) per language.
_CODES = {"CODE_NUMPY": CODE_NUMPY, "CODE_IRLS": CODE_IRLS, "CODE_TORCH": CODE_TORCH}
for _lang, _secs in SECTIONS.items():
    for _sec in _secs:
        for _i, _b in enumerate(_sec["blocks"]):
            if _b[0] == "table" and _b[2] == "TABLE":
                _sec["blocks"][_i] = (_b[0], _b[1], _table(_lang), _b[3])
            elif _b[0] == "code" and _b[2] in _CODES:
                _sec["blocks"][_i] = (_b[0], _b[1], _code(_CODES[_b[2]], _lang))
