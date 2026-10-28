"""Formula page: MAE, the mean absolute error. Format: see README.md (reference page: sigmoid.py)."""

META = dict(
    id="mae",
    date="2026-10-28",
    minutes=32,
    hero=r"\mathrm{MAE}=\frac{1}{n}\sum_{i=1}^{n}\bigl|y_i-\hat{y}_i\bigr|",
    title={"ru": "MAE: средняя абсолютная ошибка", "en": "MAE: the mean absolute error", "uz": "MAE: o‘rtacha absolyut xato"},
    dek={
        "ru": "Самая понятная метрика регрессии: на сколько в среднем ошибается модель. Разбираем MAE по косточкам: почему её минимизирует медиана, что такое субградиент и почему с постоянным шагом спуск «дрожит» у оптимума, как выглядит её поверхность-многогранник и почему она так спокойно переносит выбросы.",
        "en": "The most readable regression metric: how far off the model is on average. We take MAE apart bone by bone: why the median minimizes it, what a subgradient is and why descent with a constant step jitters near the optimum, what its polyhedral loss surface looks like, and why it shrugs off outliers.",
        "uz": "Regressiyaning eng tushunarli metrikasi: model o‘rtacha qanchaga adashadi. MAE’ni mayda detallarigacha tahlil qilamiz: nega uni mediana minimallashtiradi, subgradiyent nima va nega o‘zgarmas qadamli tushish optimum yonida «titraydi», uning ko‘pyoqli sirti qanday ko‘rinadi va nega u chetga chiquvchi qiymatlarga bunchalik bardoshli.",
    },
    description={
        "ru": "MAE подробно: формула, свойства, медиана как оптимальная константа, субградиент, поверхность потерь в 3D, устойчивость к выбросам, субградиентный спуск, квантильная потеря, код на NumPy, PyTorch и scikit-learn.",
        "en": "MAE in depth: formula, properties, the median as the optimal constant, the subgradient, the loss surface in 3D, robustness to outliers, subgradient descent, the quantile loss, code in NumPy, PyTorch and scikit-learn.",
        "uz": "MAE batafsil: formula, xossalar, optimal o‘zgarmas sifatida mediana, subgradiyent, 3D’da yo‘qotish sirti, chetga chiquvchi qiymatlarga bardoshlilik, subgradiyent tushish, kvantil yo‘qotish, NumPy, PyTorch va scikit-learn’da kod.",
    },
)

# The running example from the cheat sheet: y = (3, 5, 8), ŷ = (2.5, 5, 10).
TABLE = [("1", "3", "2.5", "0.5", "0.5", "0.25"), ("2", "5", "5", "0", "0", "0"), ("3", "8", "10", "-2", "2", "4")]
TOTAL = {"ru": ("Сумма", "2.5", "4.25"), "en": ("Sum", "2.5", "4.25"), "uz": ("Yig‘indi", "2.5", "4.25")}
MEAN = {"ru": ("Среднее", "0.833", "1.417"), "en": ("Mean", "0.833", "1.417"), "uz": ("O‘rtacha", "0.833", "1.417")}


def _table(lang):
    dec = "." if lang == "en" else ","
    m = lambda v: v.replace("-", "−").replace(".", dec)
    rows = [[m(c) for c in r] for r in TABLE]
    for t in (TOTAL[lang], MEAN[lang]):
        rows.append([f"<b>{t[0]}</b>", "", "", "", f"<b>{m(t[1])}</b>", f"<b>{m(t[2])}</b>"])
    return rows


CODE_NUMPY = '''import numpy as np

y     = np.array([3.0, 5.0, 8.0])
y_hat = np.array([2.5, 5.0, 10.0])

def mae(y, y_hat):
    return np.mean(np.abs(y - y_hat))

def mae_grad(y, y_hat):
    # субградиент по прогнозам: sign(ŷ − y) / n, в нуле берём 0
    return np.sign(y_hat - y) / y.size

print(mae(y, y_hat))        # 0.8333333333333334
print(mae_grad(y, y_hat))   # [-0.33333333  0.          0.33333333]

# лучшая константа по MAE — медиана, а не среднее
data = np.array([2.0, 3.0, 5.0, 9.0, 16.0])
print(np.median(data), mae(data, np.median(data)))   # 5.0 4.0
print(data.mean(), mae(data, data.mean()))           # 7.0 4.4'''

CODE_TORCH = '''import torch
import torch.nn as nn

y     = torch.tensor([3.0, 5.0, 8.0])
y_hat = torch.tensor([2.5, 5.0, 10.0], requires_grad=True)

loss = nn.L1Loss()(y_hat, y)     # то же, что (y_hat - y).abs().mean()
loss.backward()
print(loss.item())               # 0.8333333134651184
print(y_hat.grad)                # tensor([-0.3333,  0.0000,  0.3333])

# линейная модель по MAE: шаг убывает как 1/√t
x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
t = torch.tensor([1.3, 2.0, 3.1, 4.5, 7.0])
w = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
opt = torch.optim.SGD([w, b], lr=0.5)
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda k: 1 / (k + 1) ** 0.5)
for step in range(3000):
    opt.zero_grad()
    nn.functional.l1_loss(w * x + b, t).backward()
    opt.step(); sched.step()
print(round(w.item(), 2), round(b.item(), 2))   # 1.25 3.25 — прямая через 2 точки'''

CODE_SKLEARN = '''import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import QuantileRegressor
from sklearn.ensemble import HistGradientBoostingRegressor

print(mean_absolute_error([3, 5, 8], [2.5, 5, 10]))   # 0.8333333333333334

# линейная регрессия по MAE — это квантильная регрессия с τ = 0,5
X = np.array([[-2.0], [-1.0], [0.0], [1.0], [2.0]])
y = np.array([1.3, 2.0, 3.1, 4.5, 7.0])
lad = QuantileRegressor(quantile=0.5, alpha=0.0).fit(X, y)   # alpha=0 — без L1-штрафа
print(lad.coef_, lad.intercept_)                             # [1.25] 3.25

# бустинг на MAE: значения в листьях — медианы остатков
gbr = HistGradientBoostingRegressor(loss="absolute_error")'''

CODES = {"CODE_NUMPY": CODE_NUMPY, "CODE_TORCH": CODE_TORCH, "CODE_SKLEARN": CODE_SKLEARN}


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("субградиент по прогнозам: sign(ŷ − y) / n, в нуле берём 0", "subgradient w.r.t. the predictions: sign(ŷ − y) / n, 0 at zero"),
               ("лучшая константа по MAE — медиана, а не среднее", "the best constant under MAE is the median, not the mean"),
               ("то же, что (y_hat - y).abs().mean()", "same as (y_hat - y).abs().mean()"),
               ("линейная модель по MAE: шаг убывает как 1/√t", "a linear model under MAE: the step decays as 1/√t"),
               ("— прямая через 2 точки", "— a line through 2 points"),
               ("линейная регрессия по MAE — это квантильная регрессия с τ = 0,5", "linear regression under MAE is quantile regression with τ = 0.5"),
               ("alpha=0 — без L1-штрафа", "alpha=0: no L1 penalty"),
               ("бустинг на MAE: значения в листьях — медианы остатков", "boosting on MAE: leaf values are medians of the residuals")],
        "uz": [("субградиент по прогнозам: sign(ŷ − y) / n, в нуле берём 0", "bashoratlar bo‘yicha subgradiyent: sign(ŷ − y) / n, nolda 0 olamiz"),
               ("лучшая константа по MAE — медиана, а не среднее", "MAE bo‘yicha eng yaxshi o‘zgarmas — o‘rtacha emas, mediana"),
               ("то же, что (y_hat - y).abs().mean()", "(y_hat - y).abs().mean() bilan bir xil"),
               ("линейная модель по MAE: шаг убывает как 1/√t", "MAE bo‘yicha chiziqli model: qadam 1/√t kabi kamayadi"),
               ("— прямая через 2 точки", "— 2 nuqtadan o‘tuvchi to‘g‘ri chiziq"),
               ("линейная регрессия по MAE — это квантильная регрессия с τ = 0,5", "MAE bo‘yicha chiziqli regressiya — τ = 0,5 bo‘lgan kvantil regressiya"),
               ("alpha=0 — без L1-штрафа", "alpha=0 — L1-jarimasiz"),
               ("бустинг на MAE: значения в листьях — медианы остатков", "MAE’dagi busting: barglardagi qiymatlar — qoldiqlar medianalari")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", "Модель предсказывает цену квартиры, время доставки, спрос на товар. Первый вопрос заказчика: «На сколько она ошибается?» Ответ «в среднем на 4 минуты» или «на 120 тысяч» — это и есть MAE (mean absolute error), <b>средняя абсолютная ошибка</b>. Её понимает любой человек без статистического образования, потому что она измеряется в тех же единицах, что и сама величина."),
        ("p", "Где она встречается:"),
        ("ul", [
            "<b>метрика качества регрессии</b> — прогноз спроса, времени в пути, цен, нагрузки на серверы; в отчётах её ставят рядом с <a href=\"../rmse/\">RMSE</a>;",
            "<b>функция потерь</b> — <code>L1Loss</code> в PyTorch; её берут, когда в данных есть выбросы или нужен прогноз медианы, а не среднего;",
            "<b>компьютерное зрение</b> — L1 по пикселям в pix2pix и в задачах сверхразрешения (EDSR), L1 по координатам рамок в детекторе DETR;",
            "<b>градиентный бустинг</b> — <code>loss=\"absolute_error\"</code> в scikit-learn, <code>objective=\"l1\"</code> в LightGBM: значения в листьях — медианы остатков;",
            "<b>робастная статистика</b> — регрессия наименьших модулей (least absolute deviations, LAD), квантильная регрессия, медиана как оценка «типичного» значения.",
        ]),
        ("callout", "key", "Главное за минуту", "MAE — среднее расстояние от прогноза до правды: $\\frac1n\\sum|y_i-\\hat y_i|$. Каждая ошибка входит <i>линейно</i>: промах на 2 весит как четыре промаха по $0{,}5$. Поэтому MAE устойчива к выбросам, а лучшая константа для неё — <b>медиана</b>. Цена за это — излом в нуле: производная есть везде, кроме точки, где ошибка равна нулю, и её модуль не уменьшается у минимума."),
    ]),
    dict(id="intuition", title="Интуиция: средняя длина промаха", blocks=[
        ("p", "Нарисуем правду $y_i$ точками, прогнозы $\\hat y_i$ — синими маркерами, а ошибку — вертикальным отрезком между ними. MAE — это <b>средняя длина оранжевых отрезков</b>. Направление не важно: недолёт и перелёт на одно и то же расстояние стоят одинаково."),
        ("p", "Ниже — сквозной пример шпаргалки: $y=(3;\\,5;\\,8)$, $\\hat y=(2{,}5;\\,5;\\,10)$. Тяните синие маркеры. На нижнем графике каждая ошибка $e_i=y_i-\\hat y_i$ стоит на «галочке» $|e|$; MAE — средняя высота этих точек (бирюзовая линия)."),
        ("viz", "mae-errors", {"yhat": [2.5, 5, 10]}, "<b>Рисунок 1.</b> Ошибки сквозного примера. Длины отрезков $0{,}5$, $0$ и $2$, их сумма $2{,}5$, среднее $\\mathrm{MAE}=2{,}5/3\\approx0{,}833$. Поставьте третий прогноз на $8$ — MAE упадёт до $0{,}5/3\\approx0{,}167$."),
        ("callout", "intuition", "Что заметить", "Самая большая ошибка, $2$, даёт $80\\%$ суммы модулей ($2$ из $2{,}5$). В <a href=\"../mse/\">MSE</a> та же ошибка дала бы $94\\%$ суммы квадратов ($4$ из $4{,}25$). MAE «демократичнее»: она не позволяет одному большому промаху заслонить остальные."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", "Разберём формулу на четыре действия и посмотрим, что делает каждое."),
        ("eq", r"\underbrace{y_i-\hat y_i}_{\text{ошибка }e_i}\;\longrightarrow\;\underbrace{|e_i|}_{\text{длина}}\;\longrightarrow\;\underbrace{\sum_{i=1}^{n}|e_i|}_{\text{общий промах}}\;\longrightarrow\;\underbrace{\frac1n\sum_{i=1}^{n}|e_i|}_{\text{средний промах}}"),
        ("symbols", [
            (r"y_i", "истинное значение для объекта $i$ (цена, время, спрос);"),
            (r"\hat y_i", "прогноз модели для того же объекта;"),
            (r"e_i=y_i-\hat y_i", "ошибка (остаток, residual): положительная — модель недооценила, отрицательная — переоценила;"),
            (r"|e_i|", "модуль убирает знак, чтобы недолёт и перелёт не гасили друг друга; $|e|=\\sqrt{e^2}$ — расстояние на числовой прямой;"),
            (r"\frac1n\sum", "усреднение делает метрику независимой от размера выборки: MAE на 100 и на 10 000 объектах можно сравнивать."),
        ]),
        ("p", "Почему нельзя обойтись без модуля? Средняя ошибка без него, $\\frac1n\\sum e_i$, на нашем примере равна $(0{,}5+0-2)/3=-0{,}5$, и её можно сделать нулевой при сколь угодно плохой модели: ошибки $+100$ и $-100$ в среднем дают ноль. Эта величина называется <b>смещением</b> (bias) — полезная, но другая метрика."),
        ("table", ["$i$", "$y_i$", "$\\hat y_i$", "$e_i$", "$|e_i|$", "$e_i^2$"], "TABLE", {"num": [0, 1, 2, 3, 4, 5]}),
        ("p", "Столбец $e_i^2$ добавлен для сравнения с <a href=\"../mse/\">MSE</a>. В векторной записи MAE — это норма $L_1$ вектора ошибок, делённая на $n$:"),
        ("eq", r"\mathrm{MAE}(y,\hat y)=\frac{1}{n}\,\bigl\|y-\hat y\bigr\|_1,\qquad \|v\|_1=\sum_{i=1}^{n}|v_i|"),
        ("p", "Отсюда второе имя функции потерь — <b>L1-потеря</b> (L1 loss). Расстояние $\\|y-\\hat y\\|_1$ называют манхэттенским: так ходит такси по сетке кварталов — сумма смещений по каждой оси."),
    ]),
    dict(id="properties", title="Свойства и лучшая константа", blocks=[
        ("ul", [
            "<b>Неотрицательность</b>: $\\mathrm{MAE}\\ge0$, и $\\mathrm{MAE}=0$ только если все прогнозы точные.",
            "<b>Единицы</b> — те же, что у $y$. Масштаб переносится напрямую: если перевести рубли в тысячи рублей, MAE уменьшится ровно в 1000 раз.",
            "<b>Линейный вклад ошибок</b>: удвоение одной ошибки удваивает её вклад, а не учетверяет, как в MSE.",
            "<b>Выпуклость</b>: модуль выпуклый, сумма выпуклых функций выпукла, поэтому у MAE нет «ложных» локальных минимумов — ни по прогнозам, ни по параметрам линейной модели. Но выпуклость <i>нестрогая</i>: минимум может быть не единственным.",
            "<b>Кусочная линейность</b>: как функция прогнозов MAE состоит из плоских кусков, склеенных по изломам там, где какая-то ошибка равна нулю. В изломах производной нет.",
            "<b>Связь с RMSE</b>: $\\mathrm{MAE}\\le\\mathrm{RMSE}\\le\\sqrt n\\,\\mathrm{MAE}$. В примере: $0{,}833\\le1{,}190\\le1{,}443$. Чем больше отношение RMSE/MAE, тем «тяжелее хвосты» ошибок.",
        ]),
        ("h3", "Лучшая константа — медиана"),
        ("p", "Пусть модель совсем простая: для всех объектов она отвечает одним и тем же числом $c$. Какое $c$ лучшее по MAE? Функция $\\mathrm{MAE}(c)=\\frac1n\\sum|y_i-c|$ — сумма «галочек» с вершинами в точках данных. Её наклон в любой точке между данными равен"),
        ("eq", r"\frac{d\,\mathrm{MAE}}{dc}=\frac{\#\{i:\,y_i<c\}-\#\{i:\,y_i>c\}}{n}"),
        ("p", "Пока слева от $c$ меньше половины точек, наклон отрицательный, и $c$ выгодно двигать вправо; когда слева больше половины — наклон положительный. Минимум там, где точки делятся пополам, то есть в <b>медиане</b>."),
        ("viz", "mae-median", {"n": 5, "c": 10}, "<b>Рисунок 2.</b> $\\mathrm{MAE}(c)$ для выборки $(2;\\,3;\\,5;\\,9;\\,16)$ и её субградиент. При $c=10$ слева четыре точки, справа одна: наклон $(4-1)/5=0{,}6$, $\\mathrm{MAE}(10)=5{,}4$. Минимум $4$ — в медиане $5$; в среднем $7$ MAE больше: $4{,}4$. Переключите на $n=6$ (добавлена точка $12$): дно становится плоским на всём отрезке $[5;\\,9]$."),
        ("deep", "Доказательство: минимум MAE(c) достигается ровно на медианах", [
            ("p", "Упорядочим данные: $y_{(1)}\\le\\dots\\le y_{(n)}$. Функция $f(c)=\\sum|y_i-c|$ выпукла и кусочно линейна. В точке $c$, не совпадающей с данными, её производная равна $L(c)-R(c)$, где $L$ и $R$ — число точек слева и справа. В точке данных $c=y_{(k)}$ (пусть она встречается один раз) субдифференциал — отрезок $[L-R-1;\\;L-R+1]$."),
            ("p", "Для выпуклой функции $c^*$ — точка минимума тогда и только тогда, когда $0\\in\\partial f(c^*)$. При нечётном $n=2m+1$ это выполняется только в $c^*=y_{(m+1)}$: там $L=R=m$, и $0\\in[-1;\\,1]$. Левее медианы $L-R\\le-1$ и производная отрицательна, правее — положительна. Значит, минимум единственный."),
            ("p", "При чётном $n=2m$ для любого $c$ строго между $y_{(m)}$ и $y_{(m+1)}$ имеем $L=R=m$: производная равна нулю, и вся эта полоса — минимумы. Обычная договорённость «медиана $=(y_{(m)}+y_{(m+1)})/2$» — лишь один из равноправных ответов."),
        ]),
        ("callout", "note", "Почему это важно", "Медиана почти не реагирует на крайние значения: если $16$ заменить на $1600$, медиана останется $5$, а среднее улетит к $323{,}8$. Модель, обученная на MAE, ведёт себя так же: она предсказывает <i>условную медиану</i> $y$ при данных признаках, а не условное среднее."),
    ]),
    dict(id="derivative", title="Производная: знак ошибки и субградиент", blocks=[
        ("p", "Производная модуля — это знак: $|e|'=\\operatorname{sign}(e)$ при $e\\ne0$. В нуле у «галочки» излом, и обычной производной нет. Выпуклый анализ предлагает замену — <b>субградиент</b>."),
        ("deep", "Вывод: производная MAE по прогнозам и по параметрам", [
            ("p", "Запишем $|e|=\\sqrt{e^2}$ и продифференцируем при $e\\ne0$:"),
            ("eq", r"\frac{d|e|}{de}=\frac{1}{2\sqrt{e^2}}\cdot2e=\frac{e}{|e|}=\operatorname{sign}(e)"),
            ("p", "Ошибка зависит от прогноза так: $e_i=y_i-\\hat y_i$, поэтому $\\partial e_i/\\partial\\hat y_i=-1$. По цепному правилу:"),
            ("eq", r"\frac{\partial\,\mathrm{MAE}}{\partial\hat y_i}=\frac1n\operatorname{sign}(e_i)\cdot(-1)=-\frac{1}{n}\operatorname{sign}\bigl(y_i-\hat y_i\bigr)"),
            ("p", "Если прогноз даёт линейная модель $\\hat y_i=wx_i+b$, то $\\partial\\hat y_i/\\partial w=x_i$, $\\partial\\hat y_i/\\partial b=1$, и"),
            ("eq", r"\frac{\partial\,\mathrm{MAE}}{\partial w}=-\frac1n\sum_{i=1}^{n}\operatorname{sign}(e_i)\,x_i,\qquad \frac{\partial\,\mathrm{MAE}}{\partial b}=-\frac1n\sum_{i=1}^{n}\operatorname{sign}(e_i)"),
            ("p", "В градиент входит только <i>знак</i> каждой ошибки, а не её размер. Объект с ошибкой $0{,}1$ и объект с ошибкой $100$ тянут параметры с одинаковой силой $1/n$."),
        ]),
        ("eq", r"\frac{\partial\,\mathrm{MAE}}{\partial\hat y_i}=-\frac{1}{n}\operatorname{sign}\bigl(y_i-\hat y_i\bigr),\qquad \partial|e|\,\big|_{e=0}=[-1;\,1]"),
        ("p", "<b>Субградиент</b> выпуклой функции $f$ в точке $x$ — любое число $g$, для которого прямая $f(x)+g\\,(z-x)$ нигде не поднимается выше графика: $f(z)\\ge f(x)+g\\,(z-x)$ для всех $z$. Для $|e|$ в нуле это все $g$ с $|g|\\le1$: любую прямую через начало координат с наклоном от $-1$ до $1$ можно «подложить» под галочку. Множество субградиентов называется <b>субдифференциалом</b>."),
        ("viz", "mae-derivative", {"e": 1.5}, "<b>Рисунок 3.</b> Слева — потеря $|e|$ и касательная, справа — производная $\\operatorname{sign}(e)$. Подведите точку к нулю: касательная распадается на веер прямых с наклонами от $-1$ до $1$, а справа этому соответствует весь отрезок $[-1;\\,1]$. Включите сравнение: производная $e^2$ равна $2e$ и плавно уменьшается к нулю, а у $|e|$ она остаётся $\\pm1$ вплоть до самого минимума."),
        ("callout", "warn", "На практике в нуле берут 0", "Фреймворки не хранят множество субградиентов: PyTorch, TensorFlow и NumPy считают $\\operatorname{sign}(0)=0$. Это законный выбор — $0\\in[-1;\\,1]$. Вторая производная модуля равна нулю везде, кроме излома, поэтому методы, которым нужен гессиан (метод Ньютона, листья XGBoost по формуле $-G/H$), с MAE напрямую не работают: в бустинге значения листьев для MAE пересчитывают как медианы остатков."),
    ]),
    dict(id="robust", title="Устойчивость к выбросам", blocks=[
        ("p", "Выброс (outlier) — объект с аномальным $y$: опечатка, сбой датчика, редкое событие. Для потери важно, <b>с какой силой</b> такой объект тянет модель. У MSE сила пропорциональна ошибке ($2e/n$), у MAE она ограничена: $1/n$, как бы далеко ни лежала точка."),
        ("viz", "mae-outlier", {"y": 0, "residuals": True}, "<b>Рисунок 4.</b> Десять точек вокруг прямой $y=1+0{,}5x$ и один выброс в $x=9$ (тяните красную точку). Без выброса наклоны близки к истинному: $0{,}467$ у MAE и $0{,}499$ у MSE. С выбросом в $y=0$ прямая MSE заваливается до наклона $0{,}291$, а прямая MAE — лишь до $0{,}438$. Вклад выброса в градиент по $b$: у MAE $1/11\\approx0{,}091$, у MSE $0{,}778$."),
        ("p", "Обратите внимание на поведение синей прямой: пока выброс ниже неё, его можно тащить вниз сколько угодно — прямая не сдвинется вообще. Знак его ошибки не меняется, а MAE реагирует только на знаки. Прямая MSE, наоборот, ползёт за выбросом без ограничений."),
        ("callout", "note", "Точка излома (breakdown point)", "В робастной статистике устойчивость измеряют долей испорченных данных, которая может увести оценку сколь угодно далеко. У среднего она нулевая: одной точки достаточно. У медианы — $50\\%$: пока испорчено меньше половины выборки, медиана остаётся в пределах «чистых» данных. Регрессия по MAE устойчива к выбросам по $y$, но <i>не</i> к точкам с аномальным $x$ (высоким рычагом, leverage) — такая точка всё ещё может развернуть прямую."),
    ]),
    dict(id="space", title="MAE в пространстве параметров: многогранник", blocks=[
        ("p", "Пусть модель — прямая $\\hat y=wx+b$, данные — пять точек с $x=(-2;\\,-1;\\,0;\\,1;\\,2)$ и $y=(1{,}3;\\,2;\\,3{,}1;\\,4{,}5;\\,7)$. Каждой паре $(w;\\,b)$ соответствует своя прямая и своя MAE. Получаем поверхность над плоскостью параметров."),
        ("p", "Каждое слагаемое $|y_i-wx_i-b|$ — это «двускатная крыша» с коньком вдоль прямой $b=y_i-wx_i$, где $i$-я ошибка равна нулю. Сумма пяти крыш — <b>многогранник</b>: плоские грани, острые рёбра, вершины. Минимум всегда достигается в вершине, где пересекаются два ребра, то есть прямая проходит ровно через две точки данных."),
        ("viz", "mae-surface", {"w": 0.4, "b": 1.8, "loss": "mae"}, "<b>Рисунок 5.</b> Слева — поверхность $\\mathrm{MAE}(w,b)$, её можно вращать. Справа вверху — вид сверху: оранжевый пунктир — рёбра (сгибы) $y_i=wx_i+b$, красная точка — минимум $\\mathrm{MAE}=0{,}39$ в $(1{,}25;\\,3{,}25)$. Тяните синюю точку: внизу видна соответствующая прямая. В исходной точке $(0{,}4;\\,1{,}8)$ $\\mathrm{MAE}=1{,}78$. Переключитесь на MSE: вместо кристалла — гладкая чаша с минимумом $0{,}229$ в $(1{,}39;\\,3{,}58)$."),
        ("p", "Две поверхности дают разные ответы: прямая MAE проходит через точки $x=-1$ и $x=1$ и почти не замечает «оттопыренную» последнюю точку $y=7$; прямая MSE наклонена круче, чтобы уменьшить её квадрат. Каждая лучше по своей мере: у прямой MSE $\\mathrm{MAE}=0{,}456&gt;0{,}39$, у прямой MAE $\\mathrm{MSE}=0{,}378&gt;0{,}229$."),
        ("deep", "Почему оптимум проходит через две точки", [
            ("p", "Задачу $\\min_{w,b}\\sum|y_i-wx_i-b|$ можно записать как линейную программу: введём $u_i\\ge0$, $v_i\\ge0$ с $y_i-wx_i-b=u_i-v_i$ и будем минимизировать $\\sum(u_i+v_i)$. Оптимум линейной программы, если он существует, достигается в вершине допустимого множества. В вершине активны как минимум столько ограничений, сколько свободных параметров у прямой, — два: значит, хотя бы две ошибки равны нулю."),
            ("p", "Отсюда же — возможная неединственность: если грань многогранника горизонтальна, минимумом будет целое ребро или грань, как плоское дно $\\mathrm{MAE}(c)$ при чётном $n$. Для пяти точек нашего примера минимум единственный: следующая по качеству вершина даёт $0{,}427$."),
        ]),
    ]),
    dict(id="training", title="MAE в обучении: субградиентный спуск", blocks=[
        ("p", "Градиентный спуск делает шаг против градиента: $\\theta\\leftarrow\\theta-\\eta\\,g$. С MAE возникает особенность: у минимума градиент <b>не уменьшается</b>. Он скачет между векторами, составленными из $\\pm1/n$, и с постоянным шагом $\\eta$ параметры всё время перепрыгивают через дно."),
        ("eq", r"\theta_{t+1}=\theta_t-\eta_t\,g_t,\qquad g_t\in\partial\,\mathrm{MAE}(\theta_t),\qquad \eta_t=\frac{\eta}{\sqrt{t+1}}"),
        ("viz", "mae-descent", {"eta": 0.2}, "<b>Рисунок 6.</b> Субградиентный спуск по $\\mathrm{MAE}(w,b)$ из точки $(-0{,}5;\\,0{,}5)$, где $\\mathrm{MAE}=3{,}16$, при $\\eta=0{,}2$. Постоянный шаг (оранжевый) уже к $t=20$ даёт $0{,}424$, но дальше скачет вокруг минимума: при $t\\ge100$ MAE колеблется между $0{,}392$ и $0{,}408$ и до $0{,}390$ не доходит. Убывающий шаг (бирюзовый) стартует медленнее — $1{,}085$ при $t=50$ и $0{,}481$ при $t=100$, — но к $t=200$ приходит к оптимуму $0{,}390$. Справа — превышение над оптимумом $\\mathrm{MAE}-\\mathrm{MAE}^*$ в логарифмическом масштабе: у постоянного шага оно застревает между $0{,}002$ и $0{,}018$, у убывающего к $t=200$ падает до $3{,}5\\cdot10^{-4}$."),
        ("p", "Для выпуклых функций теория даёт точный рецепт: при шаге $\\eta_t\\propto1/\\sqrt t$ лучшее найденное значение сходится к минимуму со скоростью $O(1/\\sqrt t)$. С постоянным шагом гарантирован лишь выход в окрестность оптимума шириной порядка $\\eta$. Поэтому на практике MAE обучают с расписанием шага (learning rate schedule), с оптимизатором <a href=\"../adam/\">Adam</a> или заменяют на гладкую <a href=\"../huber/\">функцию Хьюбера</a>."),
        ("callout", "intuition", "Сравните с MSE", "У MSE градиент пропорционален ошибке, поэтому шаги сами укорачиваются по мере приближения к минимуму — постоянного $\\eta$ хватает для точной сходимости. У MAE «тормозов» нет: о близости к оптимуму говорит только то, что знаки ошибок начинают делиться поровну."),
    ]),
    dict(id="quantile", title="Обобщение: квантили и вероятностный смысл", blocks=[
        ("p", "Медиана — это квантиль уровня $0{,}5$. Если наклонить «галочку», сделав правую ветвь круче левой, минимум сдвинется к другому квантилю. Получается <b>пинбол-потеря</b> (pinball loss), или квантильная потеря:"),
        ("eq", r"\rho_\tau(e)=\max\bigl(\tau e,\;(\tau-1)\,e\bigr)=\begin{cases}\tau\,e, & e\ge0,\\ (\tau-1)\,e, & e<0,\end{cases}\qquad \mathrm{MAE}=\frac{2}{n}\sum_{i=1}^{n}\rho_{0{,}5}(e_i)"),
        ("p", "При $\\tau=0{,}9$ недооценка ($e&gt;0$) штрафуется в девять раз сильнее переоценки, и оптимальная константа — $90\\%$-й квантиль. Так строят прогнозные интервалы: модель для $\\tau=0{,}1$ и модель для $\\tau=0{,}9$ дают коридор, в который должно попадать около $80\\%$ наблюдений."),
        ("viz", "mae-quantile", {"tau": 0.9}, "<b>Рисунок 7.</b> Слева — пинбол-потеря и для сравнения $\\tfrac12|e|$ (это $\\tau=0{,}5$). Справа — 60 точек с разбросом, растущим вместе с $x$, и лучшая прямая для выбранного $\\tau$. При $\\tau=0{,}9$ ниже прямой $53$ точки из $60$ ($88\\%$), ещё $2$ лежат на ней; при $\\tau=0{,}5$ ниже $29$, на прямой $2$. Пунктир — прямые для $\\tau=0{,}1$, $0{,}5$ и $0{,}9$: из-за растущего разброса они расходятся веером."),
        ("p", "Для оптимальной прямой доля точек ниже неё не больше $\\tau$, а доля точек ниже или на ней — не меньше $\\tau$: $53/60\\le0{,}9\\le55/60$. Это прямое следствие условия $0\\in\\partial$ — того же, что дало медиану."),
        ("h3", "MAE как метод максимального правдоподобия"),
        ("p", "Пусть $y_i=\\hat y_i+\\varepsilon_i$, где шум $\\varepsilon$ имеет распределение Лапласа с плотностью $p(\\varepsilon)=\\frac{1}{2s}e^{-|\\varepsilon|/s}$. Тогда отрицательный логарифм правдоподобия"),
        ("eq", r"-\ln L=n\ln(2s)+\frac{1}{s}\sum_{i=1}^{n}|y_i-\hat y_i|=n\ln(2s)+\frac{n}{s}\,\mathrm{MAE}"),
        ("p", "При фиксированном $s$ минимизировать правдоподобие — то же, что минимизировать MAE, а оценка масштаба шума — сама MAE: $\\hat s=\\mathrm{MAE}$. Выбирая MAE, мы неявно предполагаем шум с «тяжёлыми» (по сравнению с гауссовским) хвостами. Для MSE та же логика приводит к нормальному шуму — см. <a href=\"../mse/\">MSE</a>."),
    ]),
    dict(id="code", title="В коде", blocks=[
        ("p", "MAE считается в одну строку. Интереснее — субградиент и обучение. В NumPy:"),
        ("code", "python", "CODE_NUMPY"),
        ("p", "В PyTorch потеря называется <code>L1Loss</code>. Обратите внимание на градиент: у второго объекта ошибка ровно ноль, и фреймворк берёт субградиент $0$. Вторая часть листинга обучает прямую рисунков 5–6 с убывающим шагом:"),
        ("code", "python", "CODE_TORCH"),
        ("p", "В scikit-learn есть метрика, точная линейная регрессия по MAE (через линейную программу) и бустинг с MAE:"),
        ("code", "python", "CODE_SKLEARN"),
        ("callout", "key", "Правило", "Если нужна MAE как <i>метрика</i> — считайте её как есть. Если как <i>потеря</i> для градиентного спуска — уменьшайте шаг по расписанию или берите <a href=\"../huber/\">Хьюбера</a> с малым $\\delta$: та же устойчивость к выбросам, но гладкий минимум."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>Забыть модуль</b>: <code>np.mean(y - y_hat)</code> — это смещение, а не MAE. Ошибки разных знаков гасят друг друга, и плохая модель может получить ноль.",
            "<b>Сравнивать MAE разных задач</b>. MAE $=5$ для цен в тысячах и для температуры в градусах — несравнимые числа. Для сравнения между масштабами есть <a href=\"../mape/\">MAPE</a> или MAE, делённая на MAE простой базовой модели.",
            "<b>Учить на MSE, а отчитываться MAE</b> (или наоборот). MSE ведёт модель к условному среднему, MAE — к медиане. На скошенных данных (цены, доходы, время ожидания) это разные числа, и модель, лучшая по одной метрике, проиграет по другой.",
            "<b>Постоянный шаг с MAE-потерей</b>. Параметры будут дрожать у минимума с амплитудой порядка $\\eta$. Нужно расписание шага или сглаженная потеря.",
            "<b>Ждать единственного решения</b>. Минимум MAE может быть целым отрезком (чётное число точек) или ребром многогранника. Разные решатели вернут разные, но одинаково хорошие ответы.",
            "<b>Считать MAE «типичной ошибкой» без оглядки на хвост</b>. MAE $=1$ может скрывать редкие промахи на 50. Смотрите на распределение ошибок, квантили и RMSE рядом с MAE.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../mse/\">MSE</a>: квадрат вместо модуля — гладкость и среднее вместо медианы, но чувствительность к выбросам.",
            "<a href=\"../rmse/\">RMSE</a>: $\\mathrm{RMSE}\\ge\\mathrm{MAE}$. Для нормальных ошибок $\\mathrm{RMSE}/\\mathrm{MAE}=\\sqrt{\\pi/2}\\approx1{,}253$, для лапласовских $\\sqrt2\\approx1{,}414$; в сквозном примере $1{,}428$.",
            "<a href=\"../huber/\">Huber</a>: квадрат около нуля и модуль вдали — гладкий минимум и устойчивость к выбросам одновременно.",
            "<a href=\"../mape/\">MAPE</a>: та же MAE, но от относительных ошибок $|e_i|/|y_i|$.",
            "<a href=\"../sgd/\">SGD</a> и <a href=\"../adam/\">Adam</a>: оптимизаторы, которым с MAE нужен убывающий шаг.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $\\mathrm{MAE}=\\frac1n\\sum|y_i-\\hat y_i|$ — средняя длина промаха в единицах $y$; в сквозном примере $0{,}833$. 2) Ошибки входят линейно, поэтому MAE устойчива к выбросам, а лучшая константа — медиана (при чётном $n$ — любая точка между двумя средними). 3) Производная — $-\\operatorname{sign}(e_i)/n$; в нуле субдифференциал $[-1;\\,1]$, на практике берут $0$. 4) Поверхность MAE по параметрам — многогранник; минимум в вершине, прямая проходит через две точки. 5) Градиент не убывает у минимума: учите с убывающим шагом или берите Хьюбера. 6) Наклонная «галочка» — пинбол-потеря — даёт квантили; MAE соответствует шуму Лапласа."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="$y=(1;\\,4;\\,6)$, $\\hat y=(2;\\,4;\\,3)$. Чему равна MAE?", options=["$1{,}333$", "$3{,}333$", "$1{,}826$", "$0{,}667$"], answer=0,
                 explain="Ошибки $(-1;\\,0;\\,3)$, модули $(1;\\,0;\\,3)$, $\\mathrm{MAE}=4/3\\approx1{,}333$. $3{,}333$ — это MSE, $1{,}826$ — RMSE, $0{,}667$ — средняя ошибка без модуля."),
            dict(q="Какая константа минимизирует MAE для выборки $(1;\\,2;\\,3;\\,10;\\,50)$?", options=["$13{,}2$", "$3$", "$10$", "$2{,}5$"], answer=1,
                 explain="Оптимальная константа — медиана, $3$. Среднее $13{,}2$ минимизирует MSE, а не MAE."),
            dict(q="Каков субдифференциал функции $|e|$ в точке $e=0$?", options=["Только $\\{0\\}$", "Отрезок $[-1;\\,1]$", "$\\{-1;\\,1\\}$", "Пустое множество"], answer=1,
                 explain="Любая прямая $g\\cdot e$ с $|g|\\le1$ лежит под графиком $|e|$, поэтому $\\partial|e|(0)=[-1;\\,1]$."),
            dict(q="Почему градиентный спуск по MAE с постоянным шагом не сходится точно?", options=["MAE невыпукла", "Модуль градиента не уменьшается у минимума — шаги не укорачиваются", "У MAE нет минимума", "Градиент MAE всегда равен нулю"], answer=1,
                 explain="Каждый объект даёт вклад $\\pm1/n$ независимо от размера ошибки, поэтому шаг $\\eta g$ остаётся крупным и параметры перескакивают через дно. Помогает убывающий шаг $\\eta_t\\propto1/\\sqrt t$."),
            dict(q="Что оценивает константа, минимизирующая пинбол-потерю с $\\tau=0{,}9$?", options=["Среднее", "Медиану", "$90\\%$-й квантиль", "$10\\%$-й квантиль"], answer=2,
                 explain="Недооценка штрафуется с весом $0{,}9$, переоценка — с весом $0{,}1$; равновесие наступает, когда ниже константы $90\\%$ данных."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "A model predicts a flat’s price, a delivery time, demand for a product. The client’s first question is: “How far off is it?” The answer “4 minutes on average” or “120 thousand” is exactly MAE, the <b>mean absolute error</b>. Anyone understands it without a background in statistics, because it is measured in the same units as the quantity itself."),
        ("p", "Where it appears:"),
        ("ul", [
            "<b>a regression quality metric</b> — forecasting demand, travel time, prices, server load; reports put it next to <a href=\"../rmse/\">RMSE</a>;",
            "<b>a loss function</b> — <code>L1Loss</code> in PyTorch; it is chosen when the data contain outliers or when the target is the median rather than the mean;",
            "<b>computer vision</b> — L1 over pixels in pix2pix and in super-resolution (EDSR), L1 over box coordinates in the DETR detector;",
            "<b>gradient boosting</b> — <code>loss=\"absolute_error\"</code> in scikit-learn, <code>objective=\"l1\"</code> in LightGBM: leaf values are medians of the residuals;",
            "<b>robust statistics</b> — least absolute deviations (LAD) regression, quantile regression, the median as an estimate of a “typical” value.",
        ]),
        ("callout", "key", "The essentials in a minute", "MAE is the average distance from the prediction to the truth: $\\frac1n\\sum|y_i-\\hat y_i|$. Every error enters <i>linearly</i>: a miss of 2 weighs as much as four misses of $0.5$. That is why MAE is robust to outliers and its best constant is the <b>median</b>. The price is a kink at zero: the derivative exists everywhere except where an error equals zero, and its size does not shrink near the minimum."),
    ]),
    dict(id="intuition", title="Intuition: the average length of a miss", blocks=[
        ("p", "Draw the truth $y_i$ as points, the predictions $\\hat y_i$ as blue markers and the error as a vertical segment between them. MAE is the <b>average length of the orange segments</b>. Direction does not matter: undershooting and overshooting by the same distance cost the same."),
        ("p", "Below is the cheat sheet’s running example: $y=(3,\\,5,\\,8)$, $\\hat y=(2.5,\\,5,\\,10)$. Drag the blue markers. On the lower plot every error $e_i=y_i-\\hat y_i$ sits on the “V” of $|e|$; MAE is the average height of these points (the teal line)."),
        ("viz", "mae-errors", {"yhat": [2.5, 5, 10]}, "<b>Figure 1.</b> The errors of the running example. The segments have lengths $0.5$, $0$ and $2$; their sum is $2.5$ and their mean is $\\mathrm{MAE}=2.5/3\\approx0.833$. Move the third prediction to $8$ and MAE drops to $0.5/3\\approx0.167$."),
        ("callout", "intuition", "What to notice", "The largest error, $2$, makes up $80\\%$ of the sum of absolute values ($2$ out of $2.5$). In <a href=\"../mse/\">MSE</a> the same error would make up $94\\%$ of the sum of squares ($4$ out of $4.25$). MAE is “more democratic”: it does not let one big miss overshadow the rest."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("p", "Let us split the formula into four steps and see what each one does."),
        ("eq", r"\underbrace{y_i-\hat y_i}_{\text{error }e_i}\;\longrightarrow\;\underbrace{|e_i|}_{\text{length}}\;\longrightarrow\;\underbrace{\sum_{i=1}^{n}|e_i|}_{\text{total miss}}\;\longrightarrow\;\underbrace{\frac1n\sum_{i=1}^{n}|e_i|}_{\text{average miss}}"),
        ("symbols", [
            (r"y_i", "the true value for object $i$ (a price, a time, demand);"),
            (r"\hat y_i", "the model’s prediction for the same object;"),
            (r"e_i=y_i-\hat y_i", "the error (residual): positive means the model underestimated, negative means it overestimated;"),
            (r"|e_i|", "the absolute value drops the sign so that undershoots and overshoots do not cancel out; $|e|=\\sqrt{e^2}$ is a distance on the number line;"),
            (r"\frac1n\sum", "averaging makes the metric independent of the sample size: MAE on 100 and on 10,000 objects can be compared."),
        ]),
        ("p", "Why can we not do without the absolute value? The mean error without it, $\\frac1n\\sum e_i$, equals $(0.5+0-2)/3=-0.5$ in our example, and it can be zero for an arbitrarily bad model: errors of $+100$ and $-100$ average to zero. This quantity is called the <b>bias</b> — useful, but a different metric."),
        ("table", ["$i$", "$y_i$", "$\\hat y_i$", "$e_i$", "$|e_i|$", "$e_i^2$"], "TABLE", {"num": [0, 1, 2, 3, 4, 5]}),
        ("p", "The $e_i^2$ column is there for comparison with <a href=\"../mse/\">MSE</a>. In vector form MAE is the $L_1$ norm of the error vector divided by $n$:"),
        ("eq", r"\mathrm{MAE}(y,\hat y)=\frac{1}{n}\,\bigl\|y-\hat y\bigr\|_1,\qquad \|v\|_1=\sum_{i=1}^{n}|v_i|"),
        ("p", "Hence the second name of the loss, <b>L1 loss</b>. The distance $\\|y-\\hat y\\|_1$ is called the Manhattan distance: it is how a taxi moves on a grid of blocks — the sum of the shifts along each axis."),
    ]),
    dict(id="properties", title="Properties and the best constant", blocks=[
        ("ul", [
            "<b>Non-negativity</b>: $\\mathrm{MAE}\\ge0$, and $\\mathrm{MAE}=0$ only if every prediction is exact.",
            "<b>Units</b> are those of $y$. Scale carries over directly: convert roubles to thousands of roubles and MAE shrinks exactly 1000 times.",
            "<b>Linear contribution of errors</b>: doubling one error doubles its contribution instead of quadrupling it as in MSE.",
            "<b>Convexity</b>: the absolute value is convex and a sum of convex functions is convex, so MAE has no “false” local minima — neither in the predictions nor in the parameters of a linear model. But the convexity is <i>not strict</i>: the minimum may be non-unique.",
            "<b>Piecewise linearity</b>: as a function of the predictions MAE consists of flat pieces glued along kinks where some error is zero. There is no derivative at the kinks.",
            "<b>Link with RMSE</b>: $\\mathrm{MAE}\\le\\mathrm{RMSE}\\le\\sqrt n\\,\\mathrm{MAE}$. In the example: $0.833\\le1.190\\le1.443$. The larger the ratio RMSE/MAE, the “heavier the tails” of the errors.",
        ]),
        ("h3", "The best constant is the median"),
        ("p", "Let the model be as simple as possible: it answers the same number $c$ for every object. Which $c$ is best under MAE? The function $\\mathrm{MAE}(c)=\\frac1n\\sum|y_i-c|$ is a sum of “V”s with their tips at the data points. Its slope anywhere between the data points is"),
        ("eq", r"\frac{d\,\mathrm{MAE}}{dc}=\frac{\#\{i:\,y_i<c\}-\#\{i:\,y_i>c\}}{n}"),
        ("p", "While fewer than half the points lie to the left of $c$, the slope is negative and it pays to move $c$ to the right; once more than half lie to the left, the slope is positive. The minimum is where the points split in half, that is, at the <b>median</b>."),
        ("viz", "mae-median", {"n": 5, "c": 10}, "<b>Figure 2.</b> $\\mathrm{MAE}(c)$ for the sample $(2,\\,3,\\,5,\\,9,\\,16)$ and its subgradient. At $c=10$ four points lie to the left and one to the right: the slope is $(4-1)/5=0.6$ and $\\mathrm{MAE}(10)=5.4$. The minimum, $4$, is at the median $5$; at the mean $7$ MAE is larger: $4.4$. Switch to $n=6$ (the point $12$ is added): the bottom becomes flat over the whole interval $[5,\\,9]$."),
        ("deep", "Proof: the minimum of MAE(c) is attained exactly at the medians", [
            ("p", "Sort the data: $y_{(1)}\\le\\dots\\le y_{(n)}$. The function $f(c)=\\sum|y_i-c|$ is convex and piecewise linear. At a point $c$ that is not a data point its derivative is $L(c)-R(c)$, where $L$ and $R$ count the points to the left and to the right. At a data point $c=y_{(k)}$ (say it occurs once) the subdifferential is the interval $[L-R-1,\\;L-R+1]$."),
            ("p", "For a convex function, $c^*$ is a minimizer if and only if $0\\in\\partial f(c^*)$. For odd $n=2m+1$ this holds only at $c^*=y_{(m+1)}$: there $L=R=m$ and $0\\in[-1,\\,1]$. Left of the median $L-R\\le-1$ and the derivative is negative; right of it, positive. So the minimum is unique."),
            ("p", "For even $n=2m$, every $c$ strictly between $y_{(m)}$ and $y_{(m+1)}$ has $L=R=m$: the derivative is zero, and the whole band consists of minimizers. The usual convention “median $=(y_{(m)}+y_{(m+1)})/2$” is just one of equally valid answers."),
        ]),
        ("callout", "note", "Why it matters", "The median barely reacts to extreme values: replace $16$ with $1600$ and the median stays $5$, while the mean flies off to $323.8$. A model trained on MAE behaves the same way: it predicts the <i>conditional median</i> of $y$ given the features, not the conditional mean."),
    ]),
    dict(id="derivative", title="The derivative: the sign of the error and the subgradient", blocks=[
        ("p", "The derivative of the absolute value is the sign: $|e|'=\\operatorname{sign}(e)$ for $e\\ne0$. At zero the “V” has a kink and there is no ordinary derivative. Convex analysis offers a substitute — the <b>subgradient</b>."),
        ("deep", "Derivation: the derivative of MAE with respect to the predictions and the parameters", [
            ("p", "Write $|e|=\\sqrt{e^2}$ and differentiate for $e\\ne0$:"),
            ("eq", r"\frac{d|e|}{de}=\frac{1}{2\sqrt{e^2}}\cdot2e=\frac{e}{|e|}=\operatorname{sign}(e)"),
            ("p", "The error depends on the prediction as $e_i=y_i-\\hat y_i$, so $\\partial e_i/\\partial\\hat y_i=-1$. By the chain rule:"),
            ("eq", r"\frac{\partial\,\mathrm{MAE}}{\partial\hat y_i}=\frac1n\operatorname{sign}(e_i)\cdot(-1)=-\frac{1}{n}\operatorname{sign}\bigl(y_i-\hat y_i\bigr)"),
            ("p", "If the prediction comes from a linear model $\\hat y_i=wx_i+b$, then $\\partial\\hat y_i/\\partial w=x_i$, $\\partial\\hat y_i/\\partial b=1$, and"),
            ("eq", r"\frac{\partial\,\mathrm{MAE}}{\partial w}=-\frac1n\sum_{i=1}^{n}\operatorname{sign}(e_i)\,x_i,\qquad \frac{\partial\,\mathrm{MAE}}{\partial b}=-\frac1n\sum_{i=1}^{n}\operatorname{sign}(e_i)"),
            ("p", "Only the <i>sign</i> of each error enters the gradient, not its size. An object with an error of $0.1$ and an object with an error of $100$ pull the parameters with the same force $1/n$."),
        ]),
        ("eq", r"\frac{\partial\,\mathrm{MAE}}{\partial\hat y_i}=-\frac{1}{n}\operatorname{sign}\bigl(y_i-\hat y_i\bigr),\qquad \partial|e|\,\big|_{e=0}=[-1,\,1]"),
        ("p", "A <b>subgradient</b> of a convex function $f$ at a point $x$ is any number $g$ such that the line $f(x)+g\\,(z-x)$ never rises above the graph: $f(z)\\ge f(x)+g\\,(z-x)$ for all $z$. For $|e|$ at zero these are all $g$ with $|g|\\le1$: any line through the origin with slope between $-1$ and $1$ can be slid under the “V”. The set of subgradients is called the <b>subdifferential</b>."),
        ("viz", "mae-derivative", {"e": 1.5}, "<b>Figure 3.</b> On the left, the loss $|e|$ and its tangent; on the right, the derivative $\\operatorname{sign}(e)$. Bring the point to zero: the tangent falls apart into a fan of lines with slopes from $-1$ to $1$, which on the right corresponds to the whole segment $[-1,\\,1]$. Turn on the comparison: the derivative of $e^2$ is $2e$ and shrinks smoothly towards zero, whereas for $|e|$ it stays $\\pm1$ right up to the minimum."),
        ("callout", "warn", "In practice, 0 is taken at zero", "Frameworks do not store a set of subgradients: PyTorch, TensorFlow and NumPy use $\\operatorname{sign}(0)=0$. That is a legitimate choice, since $0\\in[-1,\\,1]$. The second derivative of the absolute value is zero everywhere except at the kink, so methods that need a Hessian (Newton’s method, XGBoost leaves via $-G/H$) do not work with MAE directly: in boosting the leaf values for MAE are recomputed as medians of the residuals."),
    ]),
    dict(id="robust", title="Robustness to outliers", blocks=[
        ("p", "An outlier is an object with an anomalous $y$: a typo, a sensor glitch, a rare event. What matters for a loss is <b>how hard</b> such an object pulls the model. For MSE the pull is proportional to the error ($2e/n$); for MAE it is bounded: $1/n$, however far away the point lies."),
        ("viz", "mae-outlier", {"y": 0, "residuals": True}, "<b>Figure 4.</b> Ten points around the line $y=1+0.5x$ and one outlier at $x=9$ (drag the red point). Without the outlier both slopes are close to the true one: $0.467$ for MAE and $0.499$ for MSE. With the outlier at $y=0$ the MSE line tilts down to a slope of $0.291$, while the MAE line only goes to $0.438$. The outlier’s contribution to the gradient with respect to $b$: $1/11\\approx0.091$ for MAE, $0.778$ for MSE."),
        ("p", "Watch the blue line: while the outlier is below it, you can drag it down as far as you like — the line does not move at all. The sign of its error does not change, and MAE reacts only to signs. The MSE line, on the contrary, follows the outlier without limit."),
        ("callout", "note", "The breakdown point", "Robust statistics measures robustness by the share of corrupted data that can drive an estimate arbitrarily far. For the mean it is zero: one point is enough. For the median it is $50\\%$: as long as less than half the sample is corrupted, the median stays within the range of the “clean” data. MAE regression is robust to outliers in $y$ but <i>not</i> to points with an anomalous $x$ (high leverage) — such a point can still swing the line."),
    ]),
    dict(id="space", title="MAE in parameter space: a polyhedron", blocks=[
        ("p", "Let the model be a line $\\hat y=wx+b$ and the data five points with $x=(-2,\\,-1,\\,0,\\,1,\\,2)$ and $y=(1.3,\\,2,\\,3.1,\\,4.5,\\,7)$. Each pair $(w,\\,b)$ gives its own line and its own MAE, so we get a surface over the parameter plane."),
        ("p", "Each term $|y_i-wx_i-b|$ is a “gable roof” with its ridge along the line $b=y_i-wx_i$, where the $i$-th error is zero. The sum of five roofs is a <b>polyhedron</b>: flat faces, sharp edges, vertices. The minimum is always attained at a vertex where two edges cross, i.e. the line passes exactly through two data points."),
        ("viz", "mae-surface", {"w": 0.4, "b": 1.8, "loss": "mae"}, "<b>Figure 5.</b> On the left, the surface $\\mathrm{MAE}(w,b)$; you can rotate it. Top right, the view from above: the dashed orange lines are the edges (creases) $y_i=wx_i+b$, the red point is the minimum $\\mathrm{MAE}=0.39$ at $(1.25,\\,3.25)$. Drag the blue point: the corresponding line is shown below. At the starting point $(0.4,\\,1.8)$, $\\mathrm{MAE}=1.78$. Switch to MSE: instead of a crystal there is a smooth bowl with its minimum $0.229$ at $(1.39,\\,3.58)$."),
        ("p", "The two surfaces give different answers: the MAE line passes through the points at $x=-1$ and $x=1$ and almost ignores the “sticking-out” last point $y=7$; the MSE line is steeper to reduce that point’s square. Each is better by its own measure: the MSE line has $\\mathrm{MAE}=0.456&gt;0.39$, the MAE line has $\\mathrm{MSE}=0.378&gt;0.229$."),
        ("deep", "Why the optimum passes through two points", [
            ("p", "The problem $\\min_{w,b}\\sum|y_i-wx_i-b|$ can be written as a linear program: introduce $u_i\\ge0$, $v_i\\ge0$ with $y_i-wx_i-b=u_i-v_i$ and minimize $\\sum(u_i+v_i)$. The optimum of a linear program, if it exists, is attained at a vertex of the feasible set. At a vertex at least as many constraints are active as the line has free parameters — two: so at least two errors are zero."),
            ("p", "This also explains the possible non-uniqueness: if a face of the polyhedron is horizontal, a whole edge or face is optimal, like the flat bottom of $\\mathrm{MAE}(c)$ for even $n$. For the five points of our example the minimum is unique: the next best vertex gives $0.427$."),
        ]),
    ]),
    dict(id="training", title="MAE in training: subgradient descent", blocks=[
        ("p", "Gradient descent steps against the gradient: $\\theta\\leftarrow\\theta-\\eta\\,g$. MAE has a peculiarity: near the minimum the gradient <b>does not shrink</b>. It jumps between vectors built from $\\pm1/n$, and with a constant step $\\eta$ the parameters keep leaping over the bottom."),
        ("eq", r"\theta_{t+1}=\theta_t-\eta_t\,g_t,\qquad g_t\in\partial\,\mathrm{MAE}(\theta_t),\qquad \eta_t=\frac{\eta}{\sqrt{t+1}}"),
        ("viz", "mae-descent", {"eta": 0.2}, "<b>Figure 6.</b> Subgradient descent on $\\mathrm{MAE}(w,b)$ from the point $(-0.5,\\,0.5)$, where $\\mathrm{MAE}=3.16$, with $\\eta=0.2$. The constant step (orange) reaches $0.424$ by $t=20$, but then keeps jumping around the minimum: for $t\\ge100$ MAE oscillates between $0.392$ and $0.408$ and never gets to $0.390$. The decaying step (teal) starts more slowly — $1.085$ at $t=50$ and $0.481$ at $t=100$ — but by $t=200$ it arrives at the optimum $0.390$. On the right, the excess over the optimum $\\mathrm{MAE}-\\mathrm{MAE}^*$ on a log scale: for the constant step it gets stuck between $0.002$ and $0.018$, for the decaying step it falls to $3.5\\cdot10^{-4}$ by $t=200$."),
        ("p", "For convex functions theory gives an exact recipe: with a step $\\eta_t\\propto1/\\sqrt t$ the best value found converges to the minimum at the rate $O(1/\\sqrt t)$. With a constant step only an approach to a neighbourhood of the optimum of width of order $\\eta$ is guaranteed. That is why in practice MAE is trained with a learning rate schedule, with the <a href=\"../adam/\">Adam</a> optimizer, or replaced by the smooth <a href=\"../huber/\">Huber loss</a>."),
        ("callout", "intuition", "Compare with MSE", "For MSE the gradient is proportional to the error, so the steps shorten by themselves as the minimum gets closer — a constant $\\eta$ is enough for exact convergence. MAE has no “brakes”: the only sign of being near the optimum is that the error signs start to split evenly."),
    ]),
    dict(id="quantile", title="Generalization: quantiles and the probabilistic meaning", blocks=[
        ("p", "The median is the quantile of level $0.5$. Tilt the “V” so that the right branch is steeper than the left one, and the minimum moves to another quantile. This is the <b>pinball loss</b>, or quantile loss:"),
        ("eq", r"\rho_\tau(e)=\max\bigl(\tau e,\;(\tau-1)\,e\bigr)=\begin{cases}\tau\,e, & e\ge0,\\ (\tau-1)\,e, & e<0,\end{cases}\qquad \mathrm{MAE}=\frac{2}{n}\sum_{i=1}^{n}\rho_{0.5}(e_i)"),
        ("p", "With $\\tau=0.9$ underestimation ($e&gt;0$) is penalized nine times harder than overestimation, and the optimal constant is the $90\\%$ quantile. This is how prediction intervals are built: a model for $\\tau=0.1$ and a model for $\\tau=0.9$ give a band that should contain about $80\\%$ of the observations."),
        ("viz", "mae-quantile", {"tau": 0.9}, "<b>Figure 7.</b> On the left, the pinball loss and, for comparison, $\\tfrac12|e|$ (that is $\\tau=0.5$). On the right, 60 points whose spread grows with $x$, and the best line for the chosen $\\tau$. At $\\tau=0.9$, $53$ of the $60$ points lie below the line ($88\\%$) and $2$ more lie on it; at $\\tau=0.5$, $29$ lie below and $2$ on the line. The dashed lines are the fits for $\\tau=0.1$, $0.5$ and $0.9$: because the spread grows, they fan out."),
        ("p", "For the optimal line the share of points below it is at most $\\tau$, and the share of points below or on it is at least $\\tau$: $53/60\\le0.9\\le55/60$. This follows directly from the condition $0\\in\\partial$ — the same one that gave the median."),
        ("h3", "MAE as maximum likelihood"),
        ("p", "Let $y_i=\\hat y_i+\\varepsilon_i$, where the noise $\\varepsilon$ follows the Laplace distribution with density $p(\\varepsilon)=\\frac{1}{2s}e^{-|\\varepsilon|/s}$. Then the negative log-likelihood is"),
        ("eq", r"-\ln L=n\ln(2s)+\frac{1}{s}\sum_{i=1}^{n}|y_i-\hat y_i|=n\ln(2s)+\frac{n}{s}\,\mathrm{MAE}"),
        ("p", "For a fixed $s$, maximizing the likelihood is the same as minimizing MAE, and the estimate of the noise scale is MAE itself: $\\hat s=\\mathrm{MAE}$. By choosing MAE we implicitly assume noise with heavier tails than the Gaussian. For MSE the same reasoning leads to normal noise — see <a href=\"../mse/\">MSE</a>."),
    ]),
    dict(id="code", title="In code", blocks=[
        ("p", "MAE takes one line. The subgradient and training are more interesting. In NumPy:"),
        ("code", "python", "CODE_NUMPY"),
        ("p", "In PyTorch the loss is called <code>L1Loss</code>. Look at the gradient: the second object’s error is exactly zero and the framework takes the subgradient $0$. The second part of the listing trains the line of Figures 5–6 with a decaying step:"),
        ("code", "python", "CODE_TORCH"),
        ("p", "scikit-learn has the metric, exact linear regression under MAE (via a linear program) and boosting with MAE:"),
        ("code", "python", "CODE_SKLEARN"),
        ("callout", "key", "The rule", "If you need MAE as a <i>metric</i>, compute it as is. If you need it as a <i>loss</i> for gradient descent, decay the step on a schedule or use <a href=\"../huber/\">Huber</a> with a small $\\delta$: the same robustness to outliers, but a smooth minimum."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>Forgetting the absolute value</b>: <code>np.mean(y - y_hat)</code> is the bias, not MAE. Errors of opposite sign cancel, and a bad model can score zero.",
            "<b>Comparing MAE across tasks</b>. MAE $=5$ for prices in thousands and for temperature in degrees are incomparable numbers. For comparisons across scales there is <a href=\"../mape/\">MAPE</a>, or MAE divided by the MAE of a simple baseline.",
            "<b>Training on MSE and reporting MAE</b> (or the other way round). MSE drives the model to the conditional mean, MAE to the median. On skewed data (prices, incomes, waiting times) these are different numbers, and the model that wins on one metric will lose on the other.",
            "<b>A constant step with an MAE loss</b>. The parameters will jitter around the minimum with an amplitude of order $\\eta$. You need a step schedule or a smoothed loss.",
            "<b>Expecting a unique solution</b>. The minimum of MAE can be a whole interval (an even number of points) or an edge of the polyhedron. Different solvers will return different but equally good answers.",
            "<b>Reading MAE as the “typical error” without looking at the tail</b>. MAE $=1$ can hide rare misses of 50. Look at the error distribution, its quantiles and RMSE next to MAE.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../mse/\">MSE</a>: a square instead of the absolute value — smoothness and the mean instead of the median, but sensitivity to outliers.",
            "<a href=\"../rmse/\">RMSE</a>: $\\mathrm{RMSE}\\ge\\mathrm{MAE}$. For normal errors $\\mathrm{RMSE}/\\mathrm{MAE}=\\sqrt{\\pi/2}\\approx1.253$, for Laplace errors $\\sqrt2\\approx1.414$; in the running example $1.428$.",
            "<a href=\"../huber/\">Huber</a>: a square near zero and the absolute value far away — a smooth minimum and robustness to outliers at the same time.",
            "<a href=\"../mape/\">MAPE</a>: the same MAE, but of the relative errors $|e_i|/|y_i|$.",
            "<a href=\"../sgd/\">SGD</a> and <a href=\"../adam/\">Adam</a>: optimizers that need a decaying step with MAE.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $\\mathrm{MAE}=\\frac1n\\sum|y_i-\\hat y_i|$ is the average length of a miss in the units of $y$; $0.833$ in the running example. 2) Errors enter linearly, so MAE is robust to outliers and its best constant is the median (for even $n$, any point between the two middle ones). 3) The derivative is $-\\operatorname{sign}(e_i)/n$; at zero the subdifferential is $[-1,\\,1]$, and $0$ is used in practice. 4) The MAE surface over the parameters is a polyhedron; the minimum is at a vertex, and the line passes through two points. 5) The gradient does not shrink near the minimum: train with a decaying step or use Huber. 6) A tilted “V”, the pinball loss, gives quantiles; MAE corresponds to Laplace noise."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="$y=(1,\\,4,\\,6)$, $\\hat y=(2,\\,4,\\,3)$. What is MAE?", options=["$1.333$", "$3.333$", "$1.826$", "$0.667$"], answer=0,
                 explain="The errors are $(-1,\\,0,\\,3)$, their absolute values $(1,\\,0,\\,3)$, $\\mathrm{MAE}=4/3\\approx1.333$. $3.333$ is MSE, $1.826$ is RMSE, $0.667$ is the mean error without the absolute value."),
            dict(q="Which constant minimizes MAE for the sample $(1,\\,2,\\,3,\\,10,\\,50)$?", options=["$13.2$", "$3$", "$10$", "$2.5$"], answer=1,
                 explain="The optimal constant is the median, $3$. The mean $13.2$ minimizes MSE, not MAE."),
            dict(q="What is the subdifferential of $|e|$ at $e=0$?", options=["Only $\\{0\\}$", "The interval $[-1,\\,1]$", "$\\{-1,\\,1\\}$", "The empty set"], answer=1,
                 explain="Every line $g\\cdot e$ with $|g|\\le1$ lies below the graph of $|e|$, so $\\partial|e|(0)=[-1,\\,1]$."),
            dict(q="Why does gradient descent on MAE with a constant step not converge exactly?", options=["MAE is not convex", "The size of the gradient does not shrink near the minimum, so the steps do not get shorter", "MAE has no minimum", "The gradient of MAE is always zero"], answer=1,
                 explain="Each object contributes $\\pm1/n$ regardless of the size of its error, so the step $\\eta g$ stays large and the parameters jump over the bottom. A decaying step $\\eta_t\\propto1/\\sqrt t$ helps."),
            dict(q="What does the constant that minimizes the pinball loss with $\\tau=0.9$ estimate?", options=["The mean", "The median", "The $90\\%$ quantile", "The $10\\%$ quantile"], answer=2,
                 explain="Underestimation is penalized with weight $0.9$, overestimation with weight $0.1$; the balance is reached when $90\\%$ of the data lie below the constant."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "Model kvartira narxini, yetkazib berish vaqtini, mahsulotga talabni bashorat qiladi. Buyurtmachining birinchi savoli: «U qanchaga adashadi?» «O‘rtacha 4 daqiqaga» yoki «120 mingga» degan javob — aynan MAE (mean absolute error), <b>o‘rtacha absolyut xato</b>. Uni statistik ma’lumoti bo‘lmagan har qanday odam tushunadi, chunki u miqdorning o‘zi bilan bir xil birliklarda o‘lchanadi."),
        ("p", "U qayerda uchraydi:"),
        ("ul", [
            "<b>regressiya sifati metrikasi</b> — talab, yo‘l vaqti, narxlar, serverlar yuklamasini bashorat qilish; hisobotlarda uni <a href=\"../rmse/\">RMSE</a> yoniga qo‘yishadi;",
            "<b>yo‘qotish funksiyasi</b> — PyTorch’dagi <code>L1Loss</code>; ma’lumotlarda chetga chiquvchi qiymatlar bo‘lsa yoki o‘rtacha emas, mediana bashorati kerak bo‘lsa olinadi;",
            "<b>kompyuter ko‘rishi</b> — pix2pix’da va o‘ta ruxsat (super-resolution, EDSR) masalalarida piksellar bo‘yicha L1, DETR detektorida ramka koordinatalari bo‘yicha L1;",
            "<b>gradiyent busting</b> — scikit-learn’da <code>loss=\"absolute_error\"</code>, LightGBM’da <code>objective=\"l1\"</code>: barglardagi qiymatlar — qoldiqlar medianalari;",
            "<b>robast statistika</b> — eng kichik modullar regressiyasi (least absolute deviations, LAD), kvantil regressiya, «tipik» qiymat bahosi sifatida mediana.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "MAE — bashoratdan haqiqatgacha o‘rtacha masofa: $\\frac1n\\sum|y_i-\\hat y_i|$. Har bir xato <i>chiziqli</i> kiradi: 2 ga adashish $0{,}5$ ga to‘rt marta adashish bilan teng vaznga ega. Shuning uchun MAE chetga chiquvchi qiymatlarga bardoshli, uning uchun eng yaxshi o‘zgarmas esa — <b>mediana</b>. Buning bahosi — noldagi sinish: hosila xato nolga teng bo‘lgan nuqtadan boshqa hamma joyda bor va uning moduli minimum yonida kamaymaydi."),
    ]),
    dict(id="intuition", title="Intuitsiya: adashishning o‘rtacha uzunligi", blocks=[
        ("p", "Haqiqiy $y_i$ qiymatlarni nuqtalar, bashoratlar $\\hat y_i$ ni ko‘k markerlar, xatoni esa ular orasidagi vertikal kesma bilan chizamiz. MAE — <b>to‘q sariq kesmalarning o‘rtacha uzunligi</b>. Yo‘nalish muhim emas: bir xil masofaga kam yoki ortiq baholash bir xil turadi."),
        ("p", "Quyida qo‘llanmaning umumiy misoli: $y=(3;\\,5;\\,8)$, $\\hat y=(2{,}5;\\,5;\\,10)$. Ko‘k markerlarni torting. Pastki grafikda har bir xato $e_i=y_i-\\hat y_i$ $|e|$ «belgisi» ustida turadi; MAE — bu nuqtalarning o‘rtacha balandligi (feruza chiziq)."),
        ("viz", "mae-errors", {"yhat": [2.5, 5, 10]}, "<b>1-rasm.</b> Umumiy misol xatolari. Kesmalar uzunligi $0{,}5$, $0$ va $2$, ularning yig‘indisi $2{,}5$, o‘rtachasi $\\mathrm{MAE}=2{,}5/3\\approx0{,}833$. Uchinchi bashoratni $8$ ga qo‘ying — MAE $0{,}5/3\\approx0{,}167$ gacha tushadi."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "Eng katta xato, $2$, modullar yig‘indisining $80\\%$ ini beradi ($2{,}5$ dan $2$). <a href=\"../mse/\">MSE</a>’da xuddi shu xato kvadratlar yig‘indisining $94\\%$ ini berardi ($4{,}25$ dan $4$). MAE «demokratikroq»: u bitta katta adashish qolganlarini to‘sib qo‘yishiga yo‘l qo‘ymaydi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", "Formulani to‘rtta amalga ajratamiz va har biri nima qilishini ko‘ramiz."),
        ("eq", r"\underbrace{y_i-\hat y_i}_{\text{xato }e_i}\;\longrightarrow\;\underbrace{|e_i|}_{\text{uzunlik}}\;\longrightarrow\;\underbrace{\sum_{i=1}^{n}|e_i|}_{\text{umumiy xato}}\;\longrightarrow\;\underbrace{\frac1n\sum_{i=1}^{n}|e_i|}_{\text{o‘rtacha xato}}"),
        ("symbols", [
            (r"y_i", "$i$-obyekt uchun haqiqiy qiymat (narx, vaqt, talab);"),
            (r"\hat y_i", "xuddi shu obyekt uchun model bashorati;"),
            (r"e_i=y_i-\hat y_i", "xato (qoldiq, residual): musbat — model kam baholagan, manfiy — ortiq baholagan;"),
            (r"|e_i|", "modul ishorani olib tashlaydi, toki kam va ortiq baholashlar bir-birini yo‘qotmasin; $|e|=\\sqrt{e^2}$ — son o‘qidagi masofa;"),
            (r"\frac1n\sum", "o‘rtachalash metrikani tanlanma hajmiga bog‘liq bo‘lmagan qiladi: 100 va 10 000 obyektdagi MAE’ni solishtirish mumkin."),
        ]),
        ("p", "Nega modulsiz bo‘lmaydi? Modulsiz o‘rtacha xato $\\frac1n\\sum e_i$ bizning misolda $(0{,}5+0-2)/3=-0{,}5$ ga teng va uni istalgancha yomon model uchun ham nolga tenglashtirish mumkin: $+100$ va $-100$ xatolar o‘rtachada nol beradi. Bu kattalik <b>siljish</b> (bias) deyiladi — foydali, lekin boshqa metrika."),
        ("table", ["$i$", "$y_i$", "$\\hat y_i$", "$e_i$", "$|e_i|$", "$e_i^2$"], "TABLE", {"num": [0, 1, 2, 3, 4, 5]}),
        ("p", "$e_i^2$ ustuni <a href=\"../mse/\">MSE</a> bilan solishtirish uchun qo‘shilgan. Vektor ko‘rinishida MAE — xatolar vektorining $n$ ga bo‘lingan $L_1$ normasi:"),
        ("eq", r"\mathrm{MAE}(y,\hat y)=\frac{1}{n}\,\bigl\|y-\hat y\bigr\|_1,\qquad \|v\|_1=\sum_{i=1}^{n}|v_i|"),
        ("p", "Yo‘qotish funksiyasining ikkinchi nomi shundan — <b>L1-yo‘qotish</b> (L1 loss). $\\|y-\\hat y\\|_1$ masofa Manxetten masofasi deyiladi: kvartallar to‘ri bo‘ylab taksi shunday yuradi — har bir o‘q bo‘yicha siljishlar yig‘indisi."),
    ]),
    dict(id="properties", title="Xossalar va eng yaxshi o‘zgarmas", blocks=[
        ("ul", [
            "<b>Manfiy emaslik</b>: $\\mathrm{MAE}\\ge0$, va $\\mathrm{MAE}=0$ faqat barcha bashoratlar aniq bo‘lsa.",
            "<b>Birliklar</b> — $y$ niki bilan bir xil. Masshtab to‘g‘ridan-to‘g‘ri o‘tadi: so‘mni ming so‘mga o‘tkazsak, MAE roppa-rosa 1000 marta kamayadi.",
            "<b>Xatolarning chiziqli hissasi</b>: bitta xatoni ikki marta oshirish uning hissasini MSE’dagidek to‘rt emas, ikki marta oshiradi.",
            "<b>Qavariqlik</b>: modul qavariq, qavariq funksiyalar yig‘indisi qavariq, shuning uchun MAE’da «soxta» lokal minimumlar yo‘q — na bashoratlar, na chiziqli model parametrlari bo‘yicha. Lekin qavariqlik <i>qat’iy emas</i>: minimum yagona bo‘lmasligi mumkin.",
            "<b>Bo‘lakli chiziqlilik</b>: bashoratlar funksiyasi sifatida MAE biror xato nolga teng bo‘lgan sinishlar bo‘ylab yopishtirilgan tekis bo‘laklardan iborat. Sinishlarda hosila yo‘q.",
            "<b>RMSE bilan bog‘liqlik</b>: $\\mathrm{MAE}\\le\\mathrm{RMSE}\\le\\sqrt n\\,\\mathrm{MAE}$. Misolda: $0{,}833\\le1{,}190\\le1{,}443$. RMSE/MAE nisbati qancha katta bo‘lsa, xatolarning «dumlari» shuncha «og‘ir».",
        ]),
        ("h3", "Eng yaxshi o‘zgarmas — mediana"),
        ("p", "Model juda oddiy bo‘lsin: barcha obyektlar uchun u bitta $c$ son bilan javob beradi. MAE bo‘yicha qaysi $c$ eng yaxshi? $\\mathrm{MAE}(c)=\\frac1n\\sum|y_i-c|$ funksiyasi — uchlari ma’lumot nuqtalarida bo‘lgan «belgilar» yig‘indisi. Ma’lumotlar orasidagi istalgan nuqtada uning qiyaligi"),
        ("eq", r"\frac{d\,\mathrm{MAE}}{dc}=\frac{\#\{i:\,y_i<c\}-\#\{i:\,y_i>c\}}{n}"),
        ("p", "$c$ dan chapda nuqtalarning yarmidan kami bo‘lsa, qiyalik manfiy va $c$ ni o‘ngga surish foydali; chapda yarmidan ko‘pi bo‘lsa — qiyalik musbat. Minimum nuqtalar teng ikkiga bo‘linadigan joyda, ya’ni <b>medianada</b>."),
        ("viz", "mae-median", {"n": 5, "c": 10}, "<b>2-rasm.</b> $(2;\\,3;\\,5;\\,9;\\,16)$ tanlanma uchun $\\mathrm{MAE}(c)$ va uning subgradiyenti. $c=10$ da chapda to‘rtta, o‘ngda bitta nuqta: qiyalik $(4-1)/5=0{,}6$, $\\mathrm{MAE}(10)=5{,}4$. Minimum $4$ — mediana $5$ da; o‘rtacha $7$ da MAE kattaroq: $4{,}4$. $n=6$ ga o‘ting ($12$ nuqtasi qo‘shilgan): tub butun $[5;\\,9]$ kesmada tekis bo‘lib qoladi."),
        ("deep", "Isbot: MAE(c) minimumiga aynan medianalarda erishiladi", [
            ("p", "Ma’lumotlarni tartiblaymiz: $y_{(1)}\\le\\dots\\le y_{(n)}$. $f(c)=\\sum|y_i-c|$ funksiyasi qavariq va bo‘lakli chiziqli. Ma’lumotlarga to‘g‘ri kelmaydigan $c$ nuqtada uning hosilasi $L(c)-R(c)$ ga teng, bu yerda $L$ va $R$ — chapdagi va o‘ngdagi nuqtalar soni. $c=y_{(k)}$ ma’lumot nuqtasida (u bir marta uchrasin) subdifferensial — $[L-R-1;\\;L-R+1]$ kesma."),
            ("p", "Qavariq funksiya uchun $c^*$ minimum nuqtasi bo‘ladi faqat va faqat $0\\in\\partial f(c^*)$ bo‘lsa. Toq $n=2m+1$ da bu faqat $c^*=y_{(m+1)}$ da bajariladi: u yerda $L=R=m$ va $0\\in[-1;\\,1]$. Medianadan chapda $L-R\\le-1$ va hosila manfiy, o‘ngda — musbat. Demak, minimum yagona."),
            ("p", "Juft $n=2m$ da $y_{(m)}$ va $y_{(m+1)}$ orasidagi istalgan $c$ uchun $L=R=m$: hosila nolga teng va bu butun yo‘lak — minimumlar. Odatiy kelishuv «mediana $=(y_{(m)}+y_{(m+1)})/2$» — teng huquqli javoblardan faqat bittasi."),
        ]),
        ("callout", "note", "Nega bu muhim", "Mediana chekka qiymatlarga deyarli javob bermaydi: $16$ ni $1600$ ga almashtirsak, mediana $5$ bo‘lib qoladi, o‘rtacha esa $323{,}8$ gacha uchib ketadi. MAE’da o‘qitilgan model ham xuddi shunday: u berilgan belgilar uchun $y$ ning <i>shartli o‘rtachasini</i> emas, <i>shartli medianasini</i> bashorat qiladi."),
    ]),
    dict(id="derivative", title="Hosila: xato ishorasi va subgradiyent", blocks=[
        ("p", "Modul hosilasi — ishora: $e\\ne0$ da $|e|'=\\operatorname{sign}(e)$. Nolda «belgi» sinadi va oddiy hosila yo‘q. Qavariq tahlil uning o‘rniga <b>subgradiyent</b>ni taklif qiladi."),
        ("deep", "Keltirib chiqarish: MAE’ning bashoratlar va parametrlar bo‘yicha hosilasi", [
            ("p", "$|e|=\\sqrt{e^2}$ deb yozamiz va $e\\ne0$ da differensiallaymiz:"),
            ("eq", r"\frac{d|e|}{de}=\frac{1}{2\sqrt{e^2}}\cdot2e=\frac{e}{|e|}=\operatorname{sign}(e)"),
            ("p", "Xato bashoratga $e_i=y_i-\\hat y_i$ kabi bog‘liq, shuning uchun $\\partial e_i/\\partial\\hat y_i=-1$. Zanjir qoidasi bo‘yicha:"),
            ("eq", r"\frac{\partial\,\mathrm{MAE}}{\partial\hat y_i}=\frac1n\operatorname{sign}(e_i)\cdot(-1)=-\frac{1}{n}\operatorname{sign}\bigl(y_i-\hat y_i\bigr)"),
            ("p", "Agar bashoratni $\\hat y_i=wx_i+b$ chiziqli model bersa, $\\partial\\hat y_i/\\partial w=x_i$, $\\partial\\hat y_i/\\partial b=1$ va"),
            ("eq", r"\frac{\partial\,\mathrm{MAE}}{\partial w}=-\frac1n\sum_{i=1}^{n}\operatorname{sign}(e_i)\,x_i,\qquad \frac{\partial\,\mathrm{MAE}}{\partial b}=-\frac1n\sum_{i=1}^{n}\operatorname{sign}(e_i)"),
            ("p", "Gradiyentga har bir xatoning kattaligi emas, faqat <i>ishorasi</i> kiradi. Xatosi $0{,}1$ bo‘lgan obyekt ham, xatosi $100$ bo‘lgan obyekt ham parametrlarni bir xil $1/n$ kuch bilan tortadi."),
        ]),
        ("eq", r"\frac{\partial\,\mathrm{MAE}}{\partial\hat y_i}=-\frac{1}{n}\operatorname{sign}\bigl(y_i-\hat y_i\bigr),\qquad \partial|e|\,\big|_{e=0}=[-1;\,1]"),
        ("p", "Qavariq $f$ funksiyaning $x$ nuqtadagi <b>subgradiyenti</b> — $f(x)+g\\,(z-x)$ to‘g‘ri chiziq hech qayerda grafikdan yuqoriga chiqmaydigan har qanday $g$ son: barcha $z$ uchun $f(z)\\ge f(x)+g\\,(z-x)$. $|e|$ uchun nolda bular $|g|\\le1$ bo‘lgan barcha $g$: koordinata boshidan o‘tuvchi qiyaligi $-1$ dan $1$ gacha bo‘lgan istalgan to‘g‘ri chiziqni «belgi» ostiga qo‘yish mumkin. Subgradiyentlar to‘plami <b>subdifferensial</b> deyiladi."),
        ("viz", "mae-derivative", {"e": 1.5}, "<b>3-rasm.</b> Chapda — $|e|$ yo‘qotish va urinma, o‘ngda — $\\operatorname{sign}(e)$ hosila. Nuqtani nolga olib boring: urinma qiyaliklari $-1$ dan $1$ gacha bo‘lgan to‘g‘ri chiziqlar yelpig‘ichiga ajraladi, o‘ngda esa bunga butun $[-1;\\,1]$ kesma mos keladi. Solishtirishni yoqing: $e^2$ ning hosilasi $2e$ ga teng va nolga qarab silliq kamayadi, $|e|$ da esa u minimumning o‘zigacha $\\pm1$ bo‘lib qoladi."),
        ("callout", "warn", "Amalda nolda 0 olinadi", "Freymvorklar subgradiyentlar to‘plamini saqlamaydi: PyTorch, TensorFlow va NumPy $\\operatorname{sign}(0)=0$ deb hisoblaydi. Bu qonuniy tanlov — $0\\in[-1;\\,1]$. Modulning ikkinchi hosilasi sinishdan boshqa hamma joyda nolga teng, shuning uchun gessian kerak bo‘lgan usullar (Nyuton usuli, $-G/H$ formulasi bo‘yicha XGBoost barglari) MAE bilan to‘g‘ridan-to‘g‘ri ishlamaydi: bustingda MAE uchun barg qiymatlari qoldiqlar medianalari sifatida qayta hisoblanadi."),
    ]),
    dict(id="robust", title="Chetga chiquvchi qiymatlarga bardoshlilik", blocks=[
        ("p", "Chetga chiquvchi qiymat (outlier) — anomal $y$ li obyekt: xato yozuv, datchik nosozligi, kamdan-kam hodisa. Yo‘qotish uchun bunday obyekt modelni <b>qanday kuch bilan</b> tortishi muhim. MSE’da kuch xatoga proporsional ($2e/n$), MAE’da u chegaralangan: nuqta qanchalik uzoqda yotmasin, $1/n$."),
        ("viz", "mae-outlier", {"y": 0, "residuals": True}, "<b>4-rasm.</b> $y=1+0{,}5x$ to‘g‘ri chiziq atrofidagi o‘nta nuqta va $x=9$ dagi bitta chetga chiquvchi nuqta (qizil nuqtani torting). Usiz qiyaliklar haqiqiysiga yaqin: MAE’da $0{,}467$, MSE’da $0{,}499$. Chetga chiquvchi nuqta $y=0$ da bo‘lganda MSE chizig‘i $0{,}291$ qiyalikkacha qulaydi, MAE chizig‘i esa faqat $0{,}438$ gacha. Chetga chiquvchi nuqtaning $b$ bo‘yicha gradiyentdagi hissasi: MAE’da $1/11\\approx0{,}091$, MSE’da $0{,}778$."),
        ("p", "Ko‘k chiziqqa e’tibor bering: chetga chiquvchi nuqta undan pastda ekan, uni istalgancha pastga tortish mumkin — chiziq umuman siljimaydi. Uning xatosi ishorasi o‘zgarmaydi, MAE esa faqat ishoralarga javob beradi. MSE chizig‘i, aksincha, chetga chiquvchi nuqta ortidan cheksiz sudraladi."),
        ("callout", "note", "Sinish nuqtasi (breakdown point)", "Robast statistikada bardoshlilik bahoni istalgancha uzoqqa olib keta oladigan buzilgan ma’lumotlar ulushi bilan o‘lchanadi. O‘rtachada u nolga teng: bitta nuqta yetarli. Medianada — $50\\%$: tanlanmaning yarmidan kami buzilgan ekan, mediana «toza» ma’lumotlar chegarasida qoladi. MAE bo‘yicha regressiya $y$ bo‘yicha chetga chiquvchilarga bardoshli, lekin anomal $x$ li nuqtalarga (yuqori richag, leverage) <i>bardoshli emas</i> — bunday nuqta baribir to‘g‘ri chiziqni burib yuborishi mumkin."),
    ]),
    dict(id="space", title="Parametrlar fazosida MAE: ko‘pyoq", blocks=[
        ("p", "Model — $\\hat y=wx+b$ to‘g‘ri chiziq, ma’lumotlar — $x=(-2;\\,-1;\\,0;\\,1;\\,2)$ va $y=(1{,}3;\\,2;\\,3{,}1;\\,4{,}5;\\,7)$ bo‘lgan beshta nuqta bo‘lsin. Har bir $(w;\\,b)$ juftligiga o‘z to‘g‘ri chizig‘i va o‘z MAE’si mos keladi. Parametrlar tekisligi ustida sirt hosil bo‘ladi."),
        ("p", "Har bir $|y_i-wx_i-b|$ qo‘shiluvchi — $i$-xato nolga teng bo‘lgan $b=y_i-wx_i$ to‘g‘ri chiziq bo‘ylab qirrali «ikki nishabli tom». Beshta tom yig‘indisi — <b>ko‘pyoq</b>: tekis yoqlar, o‘tkir qirralar, uchlar. Minimumga har doim ikki qirra kesishadigan uchda erishiladi, ya’ni to‘g‘ri chiziq roppa-rosa ikkita ma’lumot nuqtasidan o‘tadi."),
        ("viz", "mae-surface", {"w": 0.4, "b": 1.8, "loss": "mae"}, "<b>5-rasm.</b> Chapda — $\\mathrm{MAE}(w,b)$ sirti, uni aylantirish mumkin. O‘ngda yuqorida — yuqoridan ko‘rinish: to‘q sariq punktir — $y_i=wx_i+b$ qirralar (bukilishlar), qizil nuqta — $(1{,}25;\\,3{,}25)$ dagi $\\mathrm{MAE}=0{,}39$ minimum. Ko‘k nuqtani torting: pastda mos to‘g‘ri chiziq ko‘rinadi. Boshlang‘ich $(0{,}4;\\,1{,}8)$ nuqtada $\\mathrm{MAE}=1{,}78$. MSE’ga o‘ting: kristall o‘rniga $(1{,}39;\\,3{,}58)$ da $0{,}229$ minimumli silliq kosa."),
        ("p", "Ikki sirt turli javob beradi: MAE chizig‘i $x=-1$ va $x=1$ nuqtalaridan o‘tadi va «turtib chiqqan» oxirgi $y=7$ nuqtani deyarli sezmaydi; MSE chizig‘i uning kvadratini kamaytirish uchun tikroq og‘gan. Har biri o‘z o‘lchovi bo‘yicha yaxshiroq: MSE chizig‘ida $\\mathrm{MAE}=0{,}456&gt;0{,}39$, MAE chizig‘ida $\\mathrm{MSE}=0{,}378&gt;0{,}229$."),
        ("deep", "Nega optimum ikki nuqtadan o‘tadi", [
            ("p", "$\\min_{w,b}\\sum|y_i-wx_i-b|$ masalasini chiziqli dasturlash masalasi sifatida yozish mumkin: $y_i-wx_i-b=u_i-v_i$ bo‘lgan $u_i\\ge0$, $v_i\\ge0$ kiritamiz va $\\sum(u_i+v_i)$ ni minimallashtiramiz. Chiziqli dastur optimumi, agar mavjud bo‘lsa, joiz to‘plamning uchida erishiladi. Uchda to‘g‘ri chiziqning erkin parametrlari soncha — ikkita — cheklov faol bo‘ladi: demak, kamida ikkita xato nolga teng."),
            ("p", "Yagonalik bo‘lmasligi ham shundan: ko‘pyoqning yog‘i gorizontal bo‘lsa, butun qirra yoki yoq minimum bo‘ladi — juft $n$ dagi $\\mathrm{MAE}(c)$ ning tekis tubi kabi. Misolimizdagi beshta nuqta uchun minimum yagona: sifat bo‘yicha keyingi uch $0{,}427$ beradi."),
        ]),
    ]),
    dict(id="training", title="O‘qitishda MAE: subgradiyent tushish", blocks=[
        ("p", "Gradiyent tushish gradiyentga qarshi qadam tashlaydi: $\\theta\\leftarrow\\theta-\\eta\\,g$. MAE’da o‘ziga xoslik bor: minimum yonida gradiyent <b>kamaymaydi</b>. U $\\pm1/n$ lardan tuzilgan vektorlar orasida sakraydi va o‘zgarmas $\\eta$ qadamda parametrlar tub ustidan doimo sakrab o‘tadi."),
        ("eq", r"\theta_{t+1}=\theta_t-\eta_t\,g_t,\qquad g_t\in\partial\,\mathrm{MAE}(\theta_t),\qquad \eta_t=\frac{\eta}{\sqrt{t+1}}"),
        ("viz", "mae-descent", {"eta": 0.2}, "<b>6-rasm.</b> $\\mathrm{MAE}=3{,}16$ bo‘lgan $(-0{,}5;\\,0{,}5)$ nuqtadan $\\eta=0{,}2$ bilan $\\mathrm{MAE}(w,b)$ bo‘yicha subgradiyent tushish. O‘zgarmas qadam (to‘q sariq) $t=20$ dayoq $0{,}424$ beradi, lekin keyin minimum atrofida sakraydi: $t\\ge100$ da MAE $0{,}392$ va $0{,}408$ orasida tebranadi va $0{,}390$ gacha yetmaydi. Kamayuvchi qadam (feruza) sekinroq boshlanadi — $t=50$ da $1{,}085$ va $t=100$ da $0{,}481$, — lekin $t=200$ ga kelib $0{,}390$ optimumga yetadi. O‘ngda — optimumdan ortiqcha $\\mathrm{MAE}-\\mathrm{MAE}^*$ logarifmik shkalada: o‘zgarmas qadamda u $0{,}002$ va $0{,}018$ orasida qotib qoladi, kamayuvchida $t=200$ ga kelib $3{,}5\\cdot10^{-4}$ gacha tushadi."),
        ("p", "Qavariq funksiyalar uchun nazariya aniq retsept beradi: $\\eta_t\\propto1/\\sqrt t$ qadamda topilgan eng yaxshi qiymat minimumga $O(1/\\sqrt t)$ tezlikda yaqinlashadi. O‘zgarmas qadamda faqat optimumning $\\eta$ tartibidagi kenglikdagi atrofiga chiqish kafolatlanadi. Shuning uchun amalda MAE qadam jadvali (learning rate schedule) bilan, <a href=\"../adam/\">Adam</a> optimizatori bilan o‘qitiladi yoki silliq <a href=\"../huber/\">Xyuber funksiyasi</a> bilan almashtiriladi."),
        ("callout", "intuition", "MSE bilan solishtiring", "MSE’da gradiyent xatoga proporsional, shuning uchun minimumga yaqinlashgan sari qadamlar o‘z-o‘zidan qisqaradi — aniq yaqinlashish uchun o‘zgarmas $\\eta$ yetarli. MAE’da «tormoz» yo‘q: optimumga yaqinlikni faqat xatolar ishoralarining teng bo‘linishi boshlangani ko‘rsatadi."),
    ]),
    dict(id="quantile", title="Umumlashma: kvantillar va ehtimoliy ma’no", blocks=[
        ("p", "Mediana — $0{,}5$ darajali kvantil. Agar «belgi»ni o‘ng tarmog‘i chapidan tikroq qilib og‘dirsak, minimum boshqa kvantilga siljiydi. <b>Pinbol yo‘qotish</b> (pinball loss), ya’ni kvantil yo‘qotish hosil bo‘ladi:"),
        ("eq", r"\rho_\tau(e)=\max\bigl(\tau e,\;(\tau-1)\,e\bigr)=\begin{cases}\tau\,e, & e\ge0,\\ (\tau-1)\,e, & e<0,\end{cases}\qquad \mathrm{MAE}=\frac{2}{n}\sum_{i=1}^{n}\rho_{0{,}5}(e_i)"),
        ("p", "$\\tau=0{,}9$ da kam baholash ($e&gt;0$) ortiq baholashdan to‘qqiz marta qattiqroq jazolanadi va optimal o‘zgarmas — $90\\%$-kvantil. Bashorat intervallari shunday quriladi: $\\tau=0{,}1$ uchun model va $\\tau=0{,}9$ uchun model kuzatuvlarning taxminan $80\\%$ i tushishi kerak bo‘lgan yo‘lakni beradi."),
        ("viz", "mae-quantile", {"tau": 0.9}, "<b>7-rasm.</b> Chapda — pinbol yo‘qotish va solishtirish uchun $\\tfrac12|e|$ (bu $\\tau=0{,}5$). O‘ngda — tarqoqligi $x$ bilan birga o‘sadigan 60 nuqta va tanlangan $\\tau$ uchun eng yaxshi to‘g‘ri chiziq. $\\tau=0{,}9$ da chiziqdan pastda $60$ tadan $53$ nuqta ($88\\%$), yana $2$ tasi uning ustida; $\\tau=0{,}5$ da pastda $29$ ta, chiziq ustida $2$ ta. Punktir — $\\tau=0{,}1$, $0{,}5$ va $0{,}9$ uchun to‘g‘ri chiziqlar: tarqoqlik o‘sgani uchun ular yelpig‘ichdek tarqaladi."),
        ("p", "Optimal chiziq uchun undan pastdagi nuqtalar ulushi $\\tau$ dan oshmaydi, pastdagi yoki ustidagi nuqtalar ulushi esa $\\tau$ dan kam emas: $53/60\\le0{,}9\\le55/60$. Bu medianani bergan o‘sha $0\\in\\partial$ shartining bevosita natijasi."),
        ("h3", "MAE haqiqatga maksimal o‘xshashlik usuli sifatida"),
        ("p", "$y_i=\\hat y_i+\\varepsilon_i$ bo‘lsin, bu yerda $\\varepsilon$ shovqin zichligi $p(\\varepsilon)=\\frac{1}{2s}e^{-|\\varepsilon|/s}$ bo‘lgan Laplas taqsimotiga ega. U holda o‘xshashlikning manfiy logarifmi"),
        ("eq", r"-\ln L=n\ln(2s)+\frac{1}{s}\sum_{i=1}^{n}|y_i-\hat y_i|=n\ln(2s)+\frac{n}{s}\,\mathrm{MAE}"),
        ("p", "Belgilangan $s$ da o‘xshashlikni maksimallashtirish MAE’ni minimallashtirish bilan bir xil, shovqin masshtabi bahosi esa MAE’ning o‘zi: $\\hat s=\\mathrm{MAE}$. MAE’ni tanlab, biz yashirincha gausnikiga nisbatan «og‘ir» dumli shovqinni faraz qilamiz. MSE uchun xuddi shu mantiq normal shovqinga olib keladi — <a href=\"../mse/\">MSE</a> ga qarang."),
    ]),
    dict(id="code", title="Kodda", blocks=[
        ("p", "MAE bir qatorda hisoblanadi. Subgradiyent va o‘qitish qiziqroq. NumPy’da:"),
        ("code", "python", "CODE_NUMPY"),
        ("p", "PyTorch’da yo‘qotish <code>L1Loss</code> deb ataladi. Gradiyentga e’tibor bering: ikkinchi obyektning xatosi roppa-rosa nol va freymvork $0$ subgradiyentni oladi. Listingning ikkinchi qismi 5–6-rasmlardagi to‘g‘ri chiziqni kamayuvchi qadam bilan o‘qitadi:"),
        ("code", "python", "CODE_TORCH"),
        ("p", "scikit-learn’da metrika, MAE bo‘yicha aniq chiziqli regressiya (chiziqli dastur orqali) va MAE bilan busting bor:"),
        ("code", "python", "CODE_SKLEARN"),
        ("callout", "key", "Qoida", "MAE <i>metrika</i> sifatida kerak bo‘lsa — uni boricha hisoblang. Gradiyent tushish uchun <i>yo‘qotish</i> sifatida kerak bo‘lsa — qadamni jadval bo‘yicha kamaytiring yoki kichik $\\delta$ li <a href=\"../huber/\">Xyuber</a>ni oling: chetga chiquvchilarga xuddi shunday bardoshlilik, lekin silliq minimum."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b>Modulni unutish</b>: <code>np.mean(y - y_hat)</code> — bu MAE emas, siljish. Turli ishorali xatolar bir-birini yo‘qotadi va yomon model nol olishi mumkin.",
            "<b>Turli masalalarning MAE’sini solishtirish</b>. Minglardagi narxlar uchun va graduslardagi harorat uchun MAE $=5$ — solishtirib bo‘lmaydigan sonlar. Masshtablar orasida solishtirish uchun <a href=\"../mape/\">MAPE</a> yoki oddiy bazaviy model MAE’siga bo‘lingan MAE bor.",
            "<b>MSE’da o‘qitib, MAE bilan hisobot berish</b> (yoki aksincha). MSE modelni shartli o‘rtachaga, MAE — medianaga olib boradi. Qiyshiq ma’lumotlarda (narxlar, daromadlar, kutish vaqti) bular turli sonlar va bir metrika bo‘yicha eng yaxshi model ikkinchisida yutqazadi.",
            "<b>MAE-yo‘qotish bilan o‘zgarmas qadam</b>. Parametrlar minimum yonida $\\eta$ tartibidagi amplituda bilan titraydi. Qadam jadvali yoki silliqlangan yo‘qotish kerak.",
            "<b>Yagona yechim kutish</b>. MAE minimumi butun kesma (nuqtalar soni juft bo‘lsa) yoki ko‘pyoq qirrasi bo‘lishi mumkin. Turli yechuvchilar turli, lekin bir xil yaxshi javoblar qaytaradi.",
            "<b>Dumga qaramay MAE’ni «tipik xato» deb hisoblash</b>. MAE $=1$ kamdan-kam 50 ga adashishlarni yashirishi mumkin. MAE yonida xatolar taqsimotiga, kvantillarga va RMSE’ga qarang.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘liqlik", blocks=[
        ("ul", [
            "<a href=\"../mse/\">MSE</a>: modul o‘rniga kvadrat — silliqlik va mediana o‘rniga o‘rtacha, lekin chetga chiquvchilarga sezgirlik.",
            "<a href=\"../rmse/\">RMSE</a>: $\\mathrm{RMSE}\\ge\\mathrm{MAE}$. Normal xatolar uchun $\\mathrm{RMSE}/\\mathrm{MAE}=\\sqrt{\\pi/2}\\approx1{,}253$, Laplas xatolari uchun $\\sqrt2\\approx1{,}414$; umumiy misolda $1{,}428$.",
            "<a href=\"../huber/\">Huber</a>: nol yonida kvadrat, uzoqda modul — bir vaqtda silliq minimum va chetga chiquvchilarga bardoshlilik.",
            "<a href=\"../mape/\">MAPE</a>: o‘sha MAE, lekin nisbiy xatolar $|e_i|/|y_i|$ dan.",
            "<a href=\"../sgd/\">SGD</a> va <a href=\"../adam/\">Adam</a>: MAE bilan kamayuvchi qadam kerak bo‘ladigan optimizatorlar.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $\\mathrm{MAE}=\\frac1n\\sum|y_i-\\hat y_i|$ — $y$ birliklaridagi adashishning o‘rtacha uzunligi; umumiy misolda $0{,}833$. 2) Xatolar chiziqli kiradi, shuning uchun MAE chetga chiquvchilarga bardoshli, eng yaxshi o‘zgarmas esa — mediana (juft $n$ da — ikki o‘rtadagi nuqta orasidagi istalgan nuqta). 3) Hosila — $-\\operatorname{sign}(e_i)/n$; nolda subdifferensial $[-1;\\,1]$, amalda $0$ olinadi. 4) Parametrlar bo‘yicha MAE sirti — ko‘pyoq; minimum uchda, to‘g‘ri chiziq ikki nuqtadan o‘tadi. 5) Minimum yonida gradiyent kamaymaydi: kamayuvchi qadam bilan o‘qiting yoki Xyuberni oling. 6) Og‘ma «belgi» — pinbol yo‘qotish — kvantillarni beradi; MAE Laplas shovqiniga mos keladi."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="$y=(1;\\,4;\\,6)$, $\\hat y=(2;\\,4;\\,3)$. MAE nimaga teng?", options=["$1{,}333$", "$3{,}333$", "$1{,}826$", "$0{,}667$"], answer=0,
                 explain="Xatolar $(-1;\\,0;\\,3)$, modullar $(1;\\,0;\\,3)$, $\\mathrm{MAE}=4/3\\approx1{,}333$. $3{,}333$ — bu MSE, $1{,}826$ — RMSE, $0{,}667$ — modulsiz o‘rtacha xato."),
            dict(q="$(1;\\,2;\\,3;\\,10;\\,50)$ tanlanma uchun qaysi o‘zgarmas MAE’ni minimallashtiradi?", options=["$13{,}2$", "$3$", "$10$", "$2{,}5$"], answer=1,
                 explain="Optimal o‘zgarmas — mediana, $3$. O‘rtacha $13{,}2$ MAE’ni emas, MSE’ni minimallashtiradi."),
            dict(q="$|e|$ funksiyaning $e=0$ nuqtadagi subdifferensiali qanday?", options=["Faqat $\\{0\\}$", "$[-1;\\,1]$ kesma", "$\\{-1;\\,1\\}$", "Bo‘sh to‘plam"], answer=1,
                 explain="$|g|\\le1$ bo‘lgan har qanday $g\\cdot e$ to‘g‘ri chiziq $|e|$ grafigi ostida yotadi, shuning uchun $\\partial|e|(0)=[-1;\\,1]$."),
            dict(q="Nega MAE bo‘yicha o‘zgarmas qadamli gradiyent tushish aniq yaqinlashmaydi?", options=["MAE qavariq emas", "Gradiyent moduli minimum yonida kamaymaydi — qadamlar qisqarmaydi", "MAE’ning minimumi yo‘q", "MAE gradiyenti doim nolga teng"], answer=1,
                 explain="Har bir obyekt xato kattaligidan qat’i nazar $\\pm1/n$ hissa qo‘shadi, shuning uchun $\\eta g$ qadam katta bo‘lib qoladi va parametrlar tub ustidan sakraydi. Kamayuvchi $\\eta_t\\propto1/\\sqrt t$ qadam yordam beradi."),
            dict(q="$\\tau=0{,}9$ bo‘lgan pinbol yo‘qotishni minimallashtiruvchi o‘zgarmas nimani baholaydi?", options=["O‘rtachani", "Medianani", "$90\\%$-kvantilni", "$10\\%$-kvantilni"], answer=2,
                 explain="Kam baholash $0{,}9$ vazn bilan, ortiq baholash $0{,}1$ vazn bilan jazolanadi; muvozanat ma’lumotlarning $90\\%$ i o‘zgarmasdan pastda bo‘lganda keladi."),
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
            elif _b[0] == "code" and _b[2] in CODES:
                _sec["blocks"][_i] = (_b[0], _b[1], _code(CODES[_b[2]], _lang))
