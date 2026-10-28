"""Formula page: MSE, the mean squared error. Format: see README.md (reference page: sigmoid.py)."""

META = dict(
    id="mse",
    date="2026-10-28",
    minutes=35,
    hero=r"\mathrm{MSE}=\frac{1}{n}\sum_{i=1}^{n}\bigl(y_i-\hat{y}_i\bigr)^2",
    title={"ru": "MSE: среднеквадратичная ошибка", "en": "MSE: the mean squared error", "uz": "MSE: o‘rtacha kvadratik xato"},
    dek={
        "ru": "Главная функция потерь регрессии и основа метода наименьших квадратов. Разбираем MSE по косточкам: буквальные квадраты на ошибках, почему её минимизирует среднее, производная 2e и чаша над параметрами модели, критический шаг градиентного спуска, разложение на смещение и разброс, связь с нормальным шумом и чувствительность к выбросам.",
        "en": "The main loss of regression and the foundation of least squares. We take MSE apart bone by bone: literal squares on the errors, why the mean minimizes it, the derivative 2e and the bowl over the model’s parameters, the critical step of gradient descent, the bias–variance decomposition, the link with Gaussian noise and the sensitivity to outliers.",
        "uz": "Regressiyaning asosiy yo‘qotish funksiyasi va eng kichik kvadratlar usulining poydevori. MSE’ni mayda detallarigacha tahlil qilamiz: xatolar ustidagi tom ma’nodagi kvadratlar, nega uni o‘rtacha minimallashtiradi, 2e hosila va model parametrlari ustidagi kosa, gradiyent tushishning kritik qadami, siljish va tarqoqlikka yoyilma, normal shovqin bilan bog‘liqlik va chetga chiquvchi qiymatlarga sezgirlik.",
    },
    description={
        "ru": "MSE по косточкам: формула, среднее как лучшая константа, производная, МНК и чаша потерь, шаг градиентного спуска, смещение и разброс, выбросы и код.",
        "en": "MSE explained: the formula, the mean as the best constant, the gradient, least squares, the gradient-descent step limit, bias–variance, outliers and code.",
        "uz": "MSE batafsil: formula, eng yaxshi o‘zgarmas — o‘rtacha, hosila, EKK va yo‘qotish kosasi, gradiyent tushish qadami, siljish va tarqoqlik, kod.",
    },
)

# The running example from the cheat sheet: y = (3, 5, 8), ŷ = (2.5, 5, 10).
TABLE = [("1", "3", "2.5", "0.5", "0.25", "5.9%"), ("2", "5", "5", "0", "0", "0%"), ("3", "8", "10", "-2", "4", "94.1%")]
TOTAL = {"ru": ("Сумма", "4.25", "100%"), "en": ("Sum", "4.25", "100%"), "uz": ("Yig‘indi", "4.25", "100%")}
MEAN = {"ru": ("Среднее (MSE)", "1.417", ""), "en": ("Mean (MSE)", "1.417", ""), "uz": ("O‘rtacha (MSE)", "1.417", "")}


def _table(lang):
    dec = "." if lang == "en" else ","
    m = lambda v: v.replace("-", "−").replace(".", dec)
    rows = [[m(c) for c in r] for r in TABLE]
    for t in (TOTAL[lang], MEAN[lang]):
        rows.append([f"<b>{t[0]}</b>", "", "", "", f"<b>{m(t[1])}</b>", m(t[2])])
    return rows


CODE_NUMPY = '''import numpy as np

y     = np.array([3.0, 5.0, 8.0])
y_hat = np.array([2.5, 5.0, 10.0])

def mse(y, y_hat):
    return np.mean((y - y_hat) ** 2)

def mse_grad(y, y_hat):
    # градиент по прогнозам: 2(ŷ − y) / n
    return 2 * (y_hat - y) / y.size

print(mse(y, y_hat))        # 1.4166666666666667
print(mse_grad(y, y_hat))   # [-0.33333333  0.          1.33333333]

# прямая по МНК: точное решение нормальных уравнений
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
t = np.array([1.3, 2.0, 3.1, 4.5, 7.0])
A = np.column_stack([x, np.ones_like(x)])
w, b = np.linalg.lstsq(A, t, rcond=None)[0]
print(round(w, 4), round(b, 4), round(mse(t, A @ [w, b]), 4))   # 1.39 -0.59 0.2294

# лучшая константа по MSE — среднее; MSE(c) = Var + (c − ȳ)²
data = np.array([2.0, 3.0, 5.0, 9.0, 16.0])
print(data.mean(), mse(data, data.mean()), mse(data, 12.0))   # 7.0 26.0 51.0'''

CODE_TORCH = '''import torch
import torch.nn as nn

y     = torch.tensor([3.0, 5.0, 8.0])
y_hat = torch.tensor([2.5, 5.0, 10.0], requires_grad=True)

loss = nn.MSELoss()(y_hat, y)    # то же, что ((y_hat - y) ** 2).mean()
loss.backward()
print(loss.item())               # 1.4166666269302368
print(y_hat.grad)                # tensor([-0.3333,  0.0000,  1.3333])

# градиентный спуск по прямой: при η > 2/λ_max ≈ 0.0845 он разойдётся
x = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
t = torch.tensor([1.3, 2.0, 3.1, 4.5, 7.0])
w = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
opt = torch.optim.SGD([w, b], lr=0.05)
for step in range(2000):
    opt.zero_grad()
    nn.functional.mse_loss(w * x + b, t).backward()
    opt.step()
print(round(w.item(), 2), round(b.item(), 2))   # 1.39 -0.59'''

CODE_SKLEARN = '''import numpy as np
from sklearn.metrics import mean_squared_error, root_mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor

print(mean_squared_error([3, 5, 8], [2.5, 5, 10]))        # 1.4166666666666667
print(root_mean_squared_error([3, 5, 8], [2.5, 5, 10]))   # 1.1902380714238083

X = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
y = np.array([1.3, 2.0, 3.1, 4.5, 7.0])
lr = LinearRegression().fit(X, y)                    # минимизирует MSE точно
print(lr.coef_.round(4), round(lr.intercept_, 4))    # [1.39] -0.59

# бустинг на MSE: каждое дерево подгоняется к остаткам y − F(x)
gbr = HistGradientBoostingRegressor(loss="squared_error")'''

CODES = {"CODE_NUMPY": CODE_NUMPY, "CODE_TORCH": CODE_TORCH, "CODE_SKLEARN": CODE_SKLEARN}


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("градиент по прогнозам: 2(ŷ − y) / n", "gradient w.r.t. the predictions: 2(ŷ − y) / n"),
               ("прямая по МНК: точное решение нормальных уравнений", "the least-squares line: the exact solution of the normal equations"),
               ("лучшая константа по MSE — среднее; MSE(c) = Var + (c − ȳ)²", "the best constant under MSE is the mean; MSE(c) = Var + (c − ȳ)²"),
               ("то же, что ((y_hat - y) ** 2).mean()", "same as ((y_hat - y) ** 2).mean()"),
               ("градиентный спуск по прямой: при η > 2/λ_max ≈ 0.0845 он разойдётся", "gradient descent for a line: with η > 2/λ_max ≈ 0.0845 it diverges"),
               ("минимизирует MSE точно", "minimizes MSE exactly"),
               ("бустинг на MSE: каждое дерево подгоняется к остаткам y − F(x)", "boosting on MSE: each tree is fitted to the residuals y − F(x)")],
        "uz": [("градиент по прогнозам: 2(ŷ − y) / n", "bashoratlar bo‘yicha gradiyent: 2(ŷ − y) / n"),
               ("прямая по МНК: точное решение нормальных уравнений", "EKK to‘g‘ri chizig‘i: normal tenglamalarning aniq yechimi"),
               ("лучшая константа по MSE — среднее; MSE(c) = Var + (c − ȳ)²", "MSE bo‘yicha eng yaxshi o‘zgarmas — o‘rtacha; MSE(c) = Var + (c − ȳ)²"),
               ("то же, что ((y_hat - y) ** 2).mean()", "((y_hat - y) ** 2).mean() bilan bir xil"),
               ("градиентный спуск по прямой: при η > 2/λ_max ≈ 0.0845 он разойдётся", "to‘g‘ri chiziq uchun gradiyent tushish: η > 2/λ_max ≈ 0.0845 da u uzoqlashadi"),
               ("минимизирует MSE точно", "MSE’ni aniq minimallashtiradi"),
               ("бустинг на MSE: каждое дерево подгоняется к остаткам y − F(x)", "MSE’dagi busting: har bir daraxt y − F(x) qoldiqlarga moslashtiriladi")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", "Если модель предсказывает число, почти наверняка её учили, уменьшая MSE (mean squared error) — <b>средний квадрат ошибки</b>. Это потеря «по умолчанию» для регрессии: у неё есть точное решение для линейных моделей, гладкий градиент для нейросетей и ясный статистический смысл. Метод наименьших квадратов, который Лежандр опубликовал в 1805 году, а Гаусс в 1809-м связал с нормальным законом ошибок, — это и есть минимизация MSE."),
        ("p", "Где она встречается:"),
        ("ul", [
            "<b>линейная регрессия</b> — метод наименьших квадратов (МНК, ordinary least squares) с решением в одну формулу;",
            "<b>нейросети для регрессии</b> — <code>MSELoss</code> в PyTorch, <code>\"mse\"</code> в Keras; автоэнкодеры, восстанавливающие вход;",
            "<b>диффузионные модели</b> — сеть учится предсказывать добавленный шум, и потеря — MSE между настоящим и предсказанным шумом;",
            "<b>обучение с подкреплением</b> — функцию ценности часто обучают на квадрате TD-ошибки;",
            "<b>градиентный бустинг</b> — <code>loss=\"squared_error\"</code>: антиградиент MSE равен остатку, поэтому каждое дерево подгоняется к остаткам;",
            "<b>обработка сигналов и изображений</b> — PSNR вычисляется через MSE, фильтр Калмана минимизирует ожидаемый квадрат ошибки.",
        ]),
        ("callout", "key", "Главное за минуту", "MSE — среднее квадратов ошибок: $\\frac1n\\sum(y_i-\\hat y_i)^2$. Квадрат делает потерю гладкой чашей с единственным дном, её градиент $-\\frac2n(y_i-\\hat y_i)$ пропорционален ошибке, а лучшая константа — <b>среднее</b>. Обратная сторона — квадрат раздувает большие промахи: одна ошибка в 10 весит как сто ошибок в 1, поэтому MSE чувствительна к выбросам и измеряется в квадратных единицах."),
    ]),
    dict(id="intuition", title="Интуиция: площадь квадратов", blocks=[
        ("p", "Слово «квадрат» здесь можно понимать буквально. Нарисуем на каждой ошибке квадрат со стороной $|e_i|$. Его площадь — $e_i^2$, а MSE — <b>средняя площадь квадратов</b>. Сравните с MAE, где усредняются длины отрезков: площадь растёт как квадрат стороны, поэтому большие ошибки занимают несоразмерно много места."),
        ("p", "Ниже — сквозной пример шпаргалки: $y=(3;\\,5;\\,8)$, $\\hat y=(2{,}5;\\,5;\\,10)$. Тяните синие прогнозы. На нижнем графике ошибки стоят на параболе $e^2$; MSE — средняя высота этих точек."),
        ("viz", "mse-squares", {"yhat": [2.5, 5, 10]}, "<b>Рисунок 1.</b> Квадраты ошибок сквозного примера. Площади $0{,}25$, $0$ и $4$, сумма $4{,}25$, $\\mathrm{MSE}=4{,}25/3\\approx1{,}417$. Третий квадрат — $94\\%$ всей площади. Поставьте третий прогноз на $8$ — MSE упадёт до $0{,}25/3\\approx0{,}083$."),
        ("callout", "intuition", "Что заметить", "Ошибка $2$ больше ошибки $0{,}5$ в 4 раза, а её квадрат больше в 16 раз. Модель, обученная на MSE, поэтому «боится» крупных промахов и охотно разменивает несколько мелких ошибок на устранение одной большой. Это и достоинство (большие ошибки обычно дороже), и уязвимость (выброс в данных тоже кажется «большой ошибкой»)."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", "Те же четыре действия, что у MAE, только вместо модуля — квадрат."),
        ("eq", r"\underbrace{y_i-\hat y_i}_{\text{ошибка }e_i}\;\longrightarrow\;\underbrace{e_i^2}_{\text{площадь}}\;\longrightarrow\;\underbrace{\sum_{i=1}^{n}e_i^2}_{\text{SSE}}\;\longrightarrow\;\underbrace{\frac1n\sum_{i=1}^{n}e_i^2}_{\text{MSE}}"),
        ("symbols", [
            (r"y_i", "истинное значение для объекта $i$;"),
            (r"\hat y_i", "прогноз модели;"),
            (r"e_i=y_i-\hat y_i", "ошибка (остаток); её знак после возведения в квадрат исчезает;"),
            (r"e_i^2", "квадрат: неотрицателен, гладок и растёт тем быстрее, чем больше ошибка;"),
            (r"\sum e_i^2", "сумма квадратов остатков — SSE (sum of squared errors), или RSS (residual sum of squares);"),
            (r"\frac1n", "усреднение: MSE не зависит от размера выборки."),
        ]),
        ("p", "Почему квадрат, а не модуль? Причин три. <b>Гладкость</b>: у $e^2$ производная $2e$ есть везде, в том числе в нуле. <b>Алгебра</b>: сумма квадратов — квадратичная форма, её минимум находится решением линейной системы (нормальных уравнений). <b>Геометрия</b>: $\\sum e_i^2$ — квадрат евклидова расстояния, и наилучший прогноз — ортогональная проекция, как в теореме Пифагора."),
        ("table", ["$i$", "$y_i$", "$\\hat y_i$", "$e_i$", "$e_i^2$", "доля в сумме"], "TABLE", {"num": [0, 1, 2, 3, 4, 5]}),
        ("p", "В векторной записи MSE — квадрат евклидовой нормы вектора ошибок, делённый на $n$:"),
        ("eq", r"\mathrm{MSE}(y,\hat y)=\frac{1}{n}\,\bigl\|y-\hat y\bigr\|_2^2,\qquad \mathrm{RMSE}=\sqrt{\mathrm{MSE}}"),
        ("p", "Отсюда второе название — <b>L2-потеря</b>. Единицы MSE — квадрат единиц $y$: рубли², минуты². Чтобы вернуться к исходным единицам, извлекают корень и получают <a href=\"../rmse/\">RMSE</a>; в примере $\\sqrt{1{,}417}\\approx1{,}190$."),
    ]),
    dict(id="properties", title="Свойства и лучшая константа", blocks=[
        ("ul", [
            "<b>Неотрицательность</b>: $\\mathrm{MSE}\\ge0$, равенство — только при точных прогнозах.",
            "<b>Квадратичный масштаб</b>: если $y$ и $\\hat y$ умножить на $k$, MSE умножится на $k^2$. Перевод рублей в тысячи рублей уменьшает MSE в миллион раз.",
            "<b>Гладкость и выпуклость</b>: MSE — квадратичная функция прогнозов; для линейной модели — квадратичная функция параметров. Если столбцы матрицы признаков (вместе со столбцом единиц для сдвига) линейно независимы, она строго выпукла, и минимум единственный.",
            "<b>Разложение ошибок</b>: $\\mathrm{MSE}=\\bar e^{\\,2}+\\operatorname{Var}(e)$ — квадрат среднего смещения плюс разброс ошибок. В примере $\\bar e=-0{,}5$: $1{,}417=0{,}25+1{,}167$.",
            "<b>Сравнение с MAE</b>: $\\mathrm{MSE}\\ge\\mathrm{MAE}^2$ (неравенство между средним квадратов и квадратом среднего). В примере: $1{,}417\\ge0{,}833^2\\approx0{,}694$.",
        ]),
        ("h3", "Лучшая константа — среднее"),
        ("p", "Если модель отвечает одним числом $c$, MSE как функция $c$ — парабола. Раскроем скобки, прибавив и вычтя среднее $\\bar y$:"),
        ("eq", r"\mathrm{MSE}(c)=\frac1n\sum_{i=1}^{n}(y_i-c)^2=\underbrace{\frac1n\sum_{i=1}^{n}(y_i-\bar y)^2}_{\operatorname{Var}(y)}+\;(c-\bar y)^2"),
        ("p", "Первое слагаемое от $c$ не зависит, второе неотрицательно и обращается в ноль только при $c=\\bar y$. Значит, минимум MSE единственный и достигается в <b>среднем</b>, а его значение — дисперсия данных. Производная $2(c-\\bar y)$ — прямая, пропорциональная расстоянию до среднего."),
        ("viz", "mse-mean", {"c": 12}, "<b>Рисунок 2.</b> $\\mathrm{MSE}(c)$ для выборки $(2;\\,3;\\,5;\\,9;\\,16)$ и её производная. Среднее $\\bar y=7$, минимум $\\operatorname{Var}=26$. При $c=12$: $\\mathrm{MSE}=26+(12-7)^2=51$, производная $2\\cdot5=10$. Медиана $5$ даёт $30$ — для MSE она хуже среднего. Включите выброс ($16\\to40$): среднее уезжает в $11{,}8$, дисперсия вырастает до $204{,}56$, а медиана остаётся $5$."),
        ("deep", "Доказательство разложения MSE(c) = Var + (c − ȳ)²", [
            ("p", "Запишем $y_i-c=(y_i-\\bar y)+(\\bar y-c)$ и возведём в квадрат:"),
            ("eq", r"\sum_{i=1}^{n}(y_i-c)^2=\sum_{i=1}^{n}(y_i-\bar y)^2+2(\bar y-c)\sum_{i=1}^{n}(y_i-\bar y)+n(\bar y-c)^2"),
            ("p", "Среднее слагаемое равно нулю, потому что отклонения от среднего в сумме дают ноль: $\\sum(y_i-\\bar y)=n\\bar y-n\\bar y=0$. Делим на $n$ и получаем разложение. Та же алгебра даёт формулу $\\mathrm{MSE}=\\bar e^{\\,2}+\\operatorname{Var}(e)$ и, в вероятностной версии, разложение на смещение и разброс."),
        ]),
        ("callout", "note", "Сравните с MAE", "Для MAE лучшая константа — медиана, и она не замечает выброс. Для MSE — среднее, которое выброс тянет за собой: одна точка, сдвинутая на $\\Delta$, сдвигает среднее на $\\Delta/n$, сколько бы ни было $\\Delta$. На <a href=\"../mae/\">странице MAE</a> — тот же опыт для медианы."),
    ]),
    dict(id="derivative", title="Производная: сила, пропорциональная ошибке", blocks=[
        ("p", "Производная квадрата — $2e$. Чем дальше прогноз от правды, тем сильнее градиент тянет его обратно, а у самого минимума сила плавно исчезает. Именно это делает MSE такой удобной для градиентного спуска."),
        ("deep", "Вывод: производная MSE по прогнозам и по параметрам", [
            ("p", "Для одного объекта $\\ell=(y_i-\\hat y_i)^2$. По цепному правилу, с $\\partial e_i/\\partial\\hat y_i=-1$:"),
            ("eq", r"\frac{\partial\,\mathrm{MSE}}{\partial\hat y_i}=\frac1n\cdot2e_i\cdot(-1)=-\frac{2}{n}\bigl(y_i-\hat y_i\bigr)"),
            ("p", "Для линейной модели $\\hat y_i=wx_i+b$:"),
            ("eq", r"\frac{\partial\,\mathrm{MSE}}{\partial w}=-\frac2n\sum_{i=1}^{n}e_i\,x_i,\qquad \frac{\partial\,\mathrm{MSE}}{\partial b}=-\frac2n\sum_{i=1}^{n}e_i"),
            ("p", "В матричной форме, $\\hat y=X\\theta$: $\\nabla_\\theta\\,\\mathrm{MSE}=\\frac2nX^\\top(X\\theta-y)$, а гессиан $\\frac2nX^\\top X$ от $\\theta$ не зависит — кривизна чаши везде одинакова."),
            ("p", "Вторая производная по каждому прогнозу постоянна: $\\partial^2\\mathrm{MSE}/\\partial\\hat y_i^2=2/n$. Поэтому в градиентном бустинге на MSE шаг Ньютона просто равен среднему остатку в листе, а каждое новое дерево обучается на остатках $y_i-F(x_i)$."),
        ]),
        ("eq", r"\frac{\partial\,\mathrm{MSE}}{\partial\hat y_i}=-\frac{2}{n}\bigl(y_i-\hat y_i\bigr)"),
        ("p", "Посмотрим на градиентный спуск для одной ошибки. Шаг $\\hat y\\leftarrow\\hat y-\\eta\\,\\partial e^2/\\partial\\hat y=\\hat y+2\\eta e$ превращает ошибку в $e\\leftarrow(1-2\\eta)\\,e$. Каждый шаг умножает ошибку на одно и то же число — получается геометрическая прогрессия."),
        ("viz", "mse-derivative", {"e": 2.5, "eta": 0.3}, "<b>Рисунок 3.</b> Слева — парабола $e^2$, касательная в стартовой точке и шаги спуска; справа — производная $2e$: длины синих отрезков, то есть градиенты, убывают вместе с ошибкой. При $e_0=2{,}5$ и $\\eta=0{,}3$ множитель $1-2\\eta=0{,}4$: ошибки $1$, $0{,}4$, $0{,}16$. Меняйте шаг: при $\\eta&lt;0{,}5$ ошибка убывает монотонно, при $\\eta=0{,}5$ исчезает за один шаг, при $0{,}5&lt;\\eta&lt;1$ — с колебаниями, при $\\eta=1$ качается вечно, при $\\eta&gt;1$ растёт."),
        ("callout", "intuition", "Сравните с MAE", "У $|e|$ производная $\\pm1$ не зависит от размера ошибки, поэтому шаги с постоянным $\\eta$ не укорачиваются, и спуск дрожит у минимума (см. <a href=\"../mae/\">MAE</a>). У $e^2$ «тормоза» встроены: градиент сам уменьшается у дна, и постоянного шага достаточно для точной сходимости."),
    ]),
    dict(id="space", title="Чаша над параметрами: МНК и градиентный спуск", blocks=[
        ("p", "Возьмём прямую $\\hat y=wx+b$ и пять точек: $x=(1;\\,2;\\,3;\\,4;\\,5)$, $y=(1{,}3;\\,2;\\,3{,}1;\\,4{,}5;\\,7)$. MSE как функция $(w;\\,b)$ — квадратичная форма, её график — <b>эллиптическая чаша</b> (параболоид) с единственным дном."),
        ("h3", "Точное решение: нормальные уравнения"),
        ("p", "Приравняв градиент к нулю, получаем линейную систему — нормальные уравнения — и решение метода наименьших квадратов:"),
        ("eq", r"X^\top X\,\theta=X^\top y\quad\Longrightarrow\quad\theta^*=(X^\top X)^{-1}X^\top y;\qquad w^*=\frac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)},\quad b^*=\bar y-w^*\bar x"),
        ("p", "Для наших точек $w^*=1{,}39$, $b^*=-0{,}59$, $\\mathrm{MSE}^*=0{,}2294$. На практике обратную матрицу не вычисляют: используют QR- или SVD-разложение (<code>np.linalg.lstsq</code>), а на больших данных — градиентный спуск."),
        ("h3", "Градиентный спуск и форма чаши"),
        ("p", "Скорость спуска определяет форма чаши — собственные числа гессиана $H=\\frac2nX^\\top X$. Вдоль крутого направления ($\\lambda_{\\max}$) слишком большой шаг перебрасывает через дно, вдоль пологого ($\\lambda_{\\min}$) спуск ползёт. Для наших данных $\\lambda_{\\max}=23{,}66$, $\\lambda_{\\min}=0{,}338$, их отношение — число обусловленности — около $70$: чаша вытянута в узкий овраг, и шаг больше $\\eta_{\\text{крит}}=2/\\lambda_{\\max}\\approx0{,}0845$ ведёт к расходимости."),
        ("viz", "mse-bowl", {"eta": 0.05}, "<b>Рисунок 4.</b> Слева — чаша $\\mathrm{MSE}(w,b)$ (её можно вращать), справа — вид сверху и превышение над минимумом в логарифмическом масштабе. Старт — прямая $y=3$, $\\eta=0{,}05$. За 150 шагов спуск проходит овраг лишь до превышения $1{,}5\\cdot10^{-2}$; при $\\eta=0{,}09$ он разлетается. Переключитесь на центрированный признак $x-\\bar x$: гессиан становится диагональным ($\\lambda=4$ и $2$), число обусловленности падает до $2$, допустимый шаг растёт до $0{,}5$, и при том же $\\eta=0{,}05$ превышение меньше $10^{-6}$ уже на 61-м шаге, а при $\\eta=0{,}2$ — на 13-м."),
        ("deep", "Почему условие сходимости — η < 2/λ_max", [
            ("p", "Для квадратичной функции градиент линеен: $\\nabla\\mathrm{MSE}(\\theta)=H(\\theta-\\theta^*)$. Шаг спуска даёт"),
            ("eq", r"\theta_{t+1}-\theta^*=(I-\eta H)(\theta_t-\theta^*)\quad\Longrightarrow\quad\theta_t-\theta^*=(I-\eta H)^t(\theta_0-\theta^*)"),
            ("p", "В базисе собственных векторов $H$ каждая координата умножается на $1-\\eta\\lambda_k$ на каждом шаге. Спуск сходится, если $|1-\\eta\\lambda_k|&lt;1$ для всех $k$, то есть $0&lt;\\eta&lt;2/\\lambda_{\\max}$. При $1/\\lambda_{\\max}&lt;\\eta&lt;2/\\lambda_{\\max}$ множитель отрицателен — отсюда зигзаг поперёк оврага. Медленнее всего сходится направление $\\lambda_{\\min}$: даже при лучшем постоянном шаге $\\eta=2/(\\lambda_{\\max}+\\lambda_{\\min})$ ошибка убывает в $(\\kappa-1)/(\\kappa+1)$ раз за шаг, где $\\kappa=\\lambda_{\\max}/\\lambda_{\\min}$. При $\\kappa=70$ это $0{,}97$ — сотни шагов; при $\\kappa=2$ — $1/3$."),
        ]),
        ("callout", "key", "Практический вывод", "Стандартизируйте признаки (вычесть среднее, поделить на стандартное отклонение) — это округляет чашу и позволяет брать больший шаг. Адаптивные оптимизаторы (<a href=\"../adam/\">Adam</a>, RMSProp) делают похожее масштабирование автоматически, но только по каждой координате отдельно: овраг, повёрнутый относительно осей, как у нас, они выпрямляют лишь частично."),
    ]),
    dict(id="biasvar", title="Смещение и разброс", blocks=[
        ("p", "MSE на новых данных складывается из трёх частей, и это, пожалуй, самая важная формула о переобучении. Пусть $y=f(x)+\\varepsilon$, шум имеет среднее $0$ и дисперсию $\\sigma^2$, а модель $\\hat f$ обучена на случайной выборке. Тогда ожидаемая ошибка в точке $x$:"),
        ("eq", r"\mathbb E\bigl[(y-\hat f(x))^2\bigr]=\underbrace{\bigl(f(x)-\mathbb E\hat f(x)\bigr)^2}_{\text{смещение}^2}+\underbrace{\mathbb E\bigl[(\hat f(x)-\mathbb E\hat f(x))^2\bigr]}_{\text{разброс}}+\underbrace{\sigma^2}_{\text{шум}}"),
        ("symbols", [
            (r"\mathbb E\hat f(x)", "средний прогноз по всем возможным обучающим выборкам;"),
            (r"\text{смещение}^2", "насколько средняя модель промахивается мимо истины — плата за слишком простую модель;"),
            (r"\text{разброс}", "насколько модель меняется от выборки к выборке — плата за слишком гибкую модель;"),
            (r"\sigma^2", "неустранимый шум: его не уберёт никакая модель."),
        ]),
        ("viz", "mse-biasvar", {"d": 3}, "<b>Рисунок 5.</b> Истина $f(x)=\\sin\\pi x$, 15 точек с шумом $\\sigma=0{,}3$, 200 разных обучающих выборок, полиномы степени $d$. Прямая ($d=1$) смещена: $0{,}204+0{,}012+0{,}09=0{,}306$. При $d=3$ — минимум ожидаемой ошибки: $0{,}005+0{,}025+0{,}09=0{,}120$. При $d=10$ смещение почти не меняется ($0{,}005$), но разброс взлетает до $0{,}777$, и тестовая MSE — $0{,}872$, хотя MSE на обучении всего $0{,}022$ — меньше самого шума $\\sigma^2=0{,}09$: модель запоминает шум."),
        ("deep", "Вывод разложения", [
            ("p", "Обозначим $\\bar f=\\mathbb E\\hat f(x)$. Шум $\\varepsilon$ в новой точке не зависит от обучающей выборки, поэтому"),
            ("eq", r"\mathbb E(y-\hat f)^2=\mathbb E(f+\varepsilon-\hat f)^2=\sigma^2+\mathbb E(f-\hat f)^2"),
            ("p", "Затем повторим приём из раздела о константе: $f-\\hat f=(f-\\bar f)+(\\bar f-\\hat f)$, и перекрёстное слагаемое исчезает, потому что $\\mathbb E(\\bar f-\\hat f)=0$:"),
            ("eq", r"\mathbb E(f-\hat f)^2=(f-\bar f)^2+\mathbb E(\hat f-\bar f)^2"),
            ("p", "На рисунке те же величины усреднены по равномерной сетке $x\\in[-1;\\,1]$. Чётные степени для нечётной функции $\\sin\\pi x$ почти ничего не добавляют: смещение при $d=1$ и $d=2$ одинаковое."),
        ]),
        ("callout", "note", "Смещённая оценка может быть лучше", "Минимизировать нужно сумму, а не одно смещение. Регуляризация (гребневая регрессия, ранняя остановка, усреднение моделей) сознательно вносит смещение, чтобы сильнее уменьшить разброс, и часто снижает тестовую MSE."),
    ]),
    dict(id="probability", title="Вероятностный смысл: нормальный шум", blocks=[
        ("p", "Почему именно квадрат? Классический ответ дал Гаусс (1809). Пусть $y_i=\\hat y_i+\\varepsilon_i$, где шум $\\varepsilon_i$ независим и распределён нормально, $N(0,\\sigma^2)$. Плотность одного наблюдения — колокол вокруг прогноза, а правдоподобие выборки — произведение высот колоколов в точках данных. Отрицательный логарифм правдоподобия:"),
        ("eq", r"-\ln L=\frac n2\ln(2\pi\sigma^2)+\frac{1}{2\sigma^2}\sum_{i=1}^{n}\bigl(y_i-\hat y_i\bigr)^2=\frac n2\ln(2\pi\sigma^2)+\frac{n}{2\sigma^2}\,\mathrm{MSE}"),
        ("p", "При любом фиксированном $\\sigma$ это возрастающая линейная функция MSE. Значит, <b>минимизация MSE — это метод максимального правдоподобия при нормальном шуме</b>. Минимум по $\\sigma$ даёт ещё одну связь: $\\hat\\sigma^2=\\mathrm{MSE}$. Позже (1821–1823) Гаусс дал и второе обоснование, уже без нормальности: если ошибки несмещены, некоррелированы и имеют одинаковую дисперсию, МНК-оценка имеет наименьшую дисперсию среди всех линейных несмещённых оценок (теорема Гаусса — Маркова)."),
        ("viz", "mse-gauss", {"w": 1, "b": 0.5, "s": 0.6}, "<b>Рисунок 6.</b> Слева — прямая и нормальные колокола $N(\\hat y_i,\\sigma^2)$ вокруг неё; оранжевые отрезки — высоты колоколов в точках данных, то есть вклад каждой точки в правдоподобие. Справа — $-\\ln L$ как функция MSE при текущем $\\sigma$: это прямая. Для $w=1$, $b=0{,}5$, $\\sigma=0{,}6$: $\\mathrm{MSE}=0{,}540$, $-\\ln L=5{,}791$; МНК-прямая (красная точка) с $\\mathrm{MSE}=0{,}229$ даёт $-\\ln L=3{,}634$. Лучшая $\\sigma$ для текущей прямой — $\\sqrt{0{,}54}\\approx0{,}735$."),
        ("p", "Ещё одна формулировка того же факта: среди всех функций $g(x)$ ожидаемый квадрат ошибки $\\mathbb E(y-g(x))^2$ минимален при $g(x)=\\mathbb E[y\\mid x]$. Модель, обученная на MSE, оценивает <b>условное среднее</b>. Если шум несимметричен или с тяжёлыми хвостами, условное среднее может плохо описывать «типичный» исход — тогда смотрят на медиану (<a href=\"../mae/\">MAE</a>) или квантили."),
    ]),
    dict(id="outliers", title="Выбросы: неограниченное влияние", blocks=[
        ("p", "Обратная сторона квадрата — чувствительность к аномальным точкам. Градиент от объекта пропорционален его ошибке, поэтому далёкий выброс тянет модель тем сильнее, чем он дальше. В робастной статистике говорят, что у МНК <b>неограниченная функция влияния</b> и нулевая пороговая точка (breakdown point): одной точки достаточно, чтобы увести прямую сколь угодно далеко."),
        ("viz", "mse-outlier", {"y": 0}, "<b>Рисунок 7.</b> Десять точек вокруг $y=1+0{,}5x$ и выброс в $x=9$. При выбросе в $y=0$ наклон прямой MSE падает до $0{,}291$, а сам выброс даёт $74\\%$ суммы квадратов. Справа — наклон как функция высоты выброса: у MSE это прямая (каждая единица высоты меняет наклон на $0{,}0375$, от $0{,}104$ при $y=-5$ до $0{,}779$ при $y=13$), у MAE наклон остаётся между $0{,}438$ и $0{,}514$."),
        ("p", "Что делать с выбросами, если MSE нужна:"),
        ("ul", [
            "заменить потерю на <a href=\"../huber/\">Хьюбера</a>: квадрат для малых ошибок и модуль для больших — гладкость MSE и ограниченное влияние MAE;",
            "преобразовать целевую переменную ($\\log y$ для цен и доходов) — но тогда модель оценивает среднее логарифма, а не среднее $y$;",
            "найти и проверить выбросы по остаткам: точки с огромным $e_i^2$ видны сразу;",
            "использовать робастные алгоритмы подбора (RANSAC, Theil–Sen), которые обучаются на подмножествах данных.",
        ]),
    ]),
    dict(id="code", title="В коде", blocks=[
        ("p", "MSE и её градиент в NumPy, точное решение МНК и проверка того, что лучшая константа — среднее:"),
        ("code", "python", "CODE_NUMPY"),
        ("p", "В PyTorch — <code>MSELoss</code>. Градиент по прогнозам — $2(\\hat y-y)/n$; спуск с шагом $0{,}05$ по сырому признаку из рисунка 4 приходит к тому же решению МНК, но медленно: до двух знаков — примерно за 300 шагов (в листинге их 2000 с запасом):"),
        ("code", "python", "CODE_TORCH"),
        ("p", "В scikit-learn есть метрики MSE и RMSE (метод <code>score</code> регрессоров при этом возвращает $R^2$), <code>LinearRegression</code> минимизирует MSE точно, а бустинг использует её как потерю по умолчанию:"),
        ("code", "python", "CODE_SKLEARN"),
        ("callout", "key", "Правило", "Учите на MSE, а в отчётах показывайте <a href=\"../rmse/\">RMSE</a> (те же единицы, что у $y$) рядом с <a href=\"../mae/\">MAE</a>. Большой разрыв между ними — сигнал, что в ошибках есть тяжёлый хвост или выбросы."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>Читать MSE как «среднюю ошибку»</b>. MSE $=1{,}417$ в примере — это квадратные единицы; средняя ошибка порядка $\\sqrt{1{,}417}\\approx1{,}19$ (RMSE) или $0{,}833$ (MAE).",
            "<b>MSE на данных с выбросами</b>. Несколько аномалий утащат модель за собой (рисунок 7). Чистите данные, берите <a href=\"../huber/\">Хьюбера</a> или MAE.",
            "<b>Неотмасштабированные признаки</b>. Вытянутая чаша — медленный спуск и маленький допустимый шаг (рисунок 4). Стандартизируйте признаки.",
            "<b>Слишком большой шаг</b>. При $\\eta&gt;2/\\lambda_{\\max}$ потеря растёт экспоненциально и быстро превращается в <code>inf</code> и <code>nan</code>.",
            "<b>MSE для классификации поверх сигмоиды</b>. Градиент $2(p-y)\\,p(1-p)$ гаснет, когда модель уверенно ошибается ($p\\approx0$ при $y=1$). Для вероятностей используйте <a href=\"../bce/\">BCE</a> или <a href=\"../cross-entropy/\">кросс-энтропию</a>.",
            "<b>Судить о модели по MSE на обучении</b>. Низкая MSE на обучающих данных может означать запоминание шума (рисунок 5, $d=10$). Смотрите на валидацию.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../mae/\">MAE</a>: модуль вместо квадрата — медиана вместо среднего, устойчивость к выбросам, но излом в нуле.",
            "<a href=\"../rmse/\">RMSE</a>: $\\sqrt{\\mathrm{MSE}}$ — та же оптимальная модель, но ошибка в единицах $y$.",
            "<a href=\"../huber/\">Функция Хьюбера</a>: MSE около нуля и MAE на хвостах.",
            "<a href=\"../bce/\">BCE</a>: аналог MSE для вероятностей — тоже метод максимального правдоподобия, но для распределения Бернулли.",
            "<a href=\"../sgd/\">SGD</a> и <a href=\"../adam/\">Adam</a>: на MSE хорошо видно, как шаг и обусловленность задачи определяют сходимость.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $\\mathrm{MSE}=\\frac1n\\sum(y_i-\\hat y_i)^2$ — средняя площадь квадратов на ошибках; в примере $1{,}417$, и $94\\%$ даёт одна ошибка. 2) Лучшая константа — среднее, и $\\mathrm{MSE}(c)=\\operatorname{Var}+(c-\\bar y)^2$. 3) Градиент $-\\frac2n(y_i-\\hat y_i)$ пропорционален ошибке и сам гаснет у минимума. 4) Для линейной модели MSE — чаша с точным решением $(X^\\top X)^{-1}X^\\top y$; градиентный спуск сходится при $\\eta&lt;2/\\lambda_{\\max}$, скорость задаёт число обусловленности. 5) Тестовая MSE = смещение² + разброс + шум. 6) MSE — правдоподобие при нормальном шуме; модель оценивает условное среднее. 7) Цена — неограниченное влияние выбросов."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="$y=(1;\\,4;\\,6)$, $\\hat y=(2;\\,4;\\,3)$. Чему равна MSE?", options=["$3{,}333$", "$1{,}333$", "$1{,}826$", "$10$"], answer=0,
                 explain="Ошибки $(-1;\\,0;\\,3)$, квадраты $(1;\\,0;\\,9)$, $\\mathrm{MSE}=10/3\\approx3{,}333$. $1{,}333$ — это MAE, $1{,}826$ — RMSE, $10$ — сумма квадратов без деления на $n$."),
            dict(q="Какая константа минимизирует MSE для выборки $(1;\\,2;\\,3;\\,10;\\,50)$?", options=["$3$", "$13{,}2$", "$10$", "$50$"], answer=1,
                 explain="Минимум MSE — в среднем: $(1+2+3+10+50)/5=13{,}2$. Медиана $3$ минимизирует MAE."),
            dict(q="Чему равна $\\partial\\,\\mathrm{MSE}/\\partial\\hat y_i$?", options=["$-\\frac2n(y_i-\\hat y_i)$", "$-\\frac1n\\operatorname{sign}(y_i-\\hat y_i)$", "$(y_i-\\hat y_i)^2$", "$\\frac2n$"], answer=0,
                 explain="$\\frac{\\partial}{\\partial\\hat y_i}\\frac1n(y_i-\\hat y_i)^2=\\frac1n\\cdot2(y_i-\\hat y_i)\\cdot(-1)$. Вариант со знаком — производная MAE, $\\frac2n$ — вторая производная."),
            dict(q="Собственные числа гессиана MSE равны $4$ и $2$. При каких постоянных шагах $\\eta&gt;0$ градиентный спуск сходится?", options=["$\\eta&lt;0{,}25$", "$\\eta&lt;0{,}5$", "$\\eta&lt;1$", "$\\eta&lt;2$"], answer=1,
                 explain="Условие $|1-\\eta\\lambda|&lt;1$ для всех собственных чисел даёт $\\eta&lt;2/\\lambda_{\\max}=2/4=0{,}5$. Это как раз центрированный случай рисунка 4."),
            dict(q="Минимизация MSE совпадает с методом максимального правдоподобия, если шум распределён…", options=["по Лапласу", "нормально", "равномерно", "по Пуассону"], answer=1,
                 explain="При нормальном шуме $-\\ln L=\\frac n2\\ln(2\\pi\\sigma^2)+\\frac{n}{2\\sigma^2}\\mathrm{MSE}$ — возрастающая функция MSE. Шум Лапласа соответствует MAE."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "If a model predicts a number, it was almost certainly trained by reducing MSE, the <b>mean squared error</b>. It is the “default” loss for regression: it has an exact solution for linear models, a smooth gradient for neural networks and a clear statistical meaning. The method of least squares, published by Legendre in 1805 and tied to the normal law of errors by Gauss in 1809, is exactly the minimization of MSE."),
        ("p", "Where it appears:"),
        ("ul", [
            "<b>linear regression</b> — ordinary least squares (OLS) with a one-formula solution;",
            "<b>neural networks for regression</b> — <code>MSELoss</code> in PyTorch, <code>\"mse\"</code> in Keras; autoencoders that reconstruct their input;",
            "<b>diffusion models</b> — the network learns to predict the added noise, and the loss is the MSE between the true and the predicted noise;",
            "<b>reinforcement learning</b> — the value function is often trained on the squared TD error;",
            "<b>gradient boosting</b> — <code>loss=\"squared_error\"</code>: the negative gradient of MSE is the residual, so every tree is fitted to the residuals;",
            "<b>signal and image processing</b> — PSNR is computed from MSE, and the Kalman filter minimizes the expected squared error.",
        ]),
        ("callout", "key", "The essentials in a minute", "MSE is the mean of the squared errors: $\\frac1n\\sum(y_i-\\hat y_i)^2$. The square turns the loss into a smooth bowl with a single bottom, its gradient $-\\frac2n(y_i-\\hat y_i)$ is proportional to the error, and the best constant is the <b>mean</b>. The flip side is that the square inflates big misses: one error of 10 weighs as much as a hundred errors of 1, so MSE is sensitive to outliers and is measured in squared units."),
    ]),
    dict(id="intuition", title="Intuition: the area of the squares", blocks=[
        ("p", "The word “squared” can be taken literally here. Draw a square with side $|e_i|$ on each error. Its area is $e_i^2$, and MSE is the <b>average area of the squares</b>. Compare with MAE, where lengths of segments are averaged: area grows as the square of the side, so big errors take up a disproportionate amount of space."),
        ("p", "Below is the cheat sheet’s running example: $y=(3,\\,5,\\,8)$, $\\hat y=(2.5,\\,5,\\,10)$. Drag the blue predictions. On the lower plot the errors sit on the parabola $e^2$; MSE is the average height of these points."),
        ("viz", "mse-squares", {"yhat": [2.5, 5, 10]}, "<b>Figure 1.</b> The squared errors of the running example. The areas are $0.25$, $0$ and $4$; the sum is $4.25$ and $\\mathrm{MSE}=4.25/3\\approx1.417$. The third square is $94\\%$ of the total area. Move the third prediction to $8$ and MSE drops to $0.25/3\\approx0.083$."),
        ("callout", "intuition", "What to notice", "The error $2$ is 4 times the error $0.5$, but its square is 16 times larger. A model trained on MSE is therefore “afraid” of big misses and readily trades several small errors for removing one large one. That is both a virtue (big errors are usually more costly) and a weakness (an outlier in the data also looks like a “big error”)."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("p", "The same four steps as in MAE, only with a square instead of the absolute value."),
        ("eq", r"\underbrace{y_i-\hat y_i}_{\text{error }e_i}\;\longrightarrow\;\underbrace{e_i^2}_{\text{area}}\;\longrightarrow\;\underbrace{\sum_{i=1}^{n}e_i^2}_{\text{SSE}}\;\longrightarrow\;\underbrace{\frac1n\sum_{i=1}^{n}e_i^2}_{\text{MSE}}"),
        ("symbols", [
            (r"y_i", "the true value for object $i$;"),
            (r"\hat y_i", "the model’s prediction;"),
            (r"e_i=y_i-\hat y_i", "the error (residual); its sign disappears after squaring;"),
            (r"e_i^2", "the square: non-negative, smooth, and growing faster the larger the error;"),
            (r"\sum e_i^2", "the sum of squared residuals — SSE (sum of squared errors), or RSS (residual sum of squares);"),
            (r"\frac1n", "averaging: MSE does not depend on the sample size."),
        ]),
        ("p", "Why a square and not the absolute value? There are three reasons. <b>Smoothness</b>: $e^2$ has the derivative $2e$ everywhere, including at zero. <b>Algebra</b>: a sum of squares is a quadratic form, and its minimum is found by solving a linear system (the normal equations). <b>Geometry</b>: $\\sum e_i^2$ is a squared Euclidean distance, and the best prediction is an orthogonal projection, as in Pythagoras’ theorem."),
        ("table", ["$i$", "$y_i$", "$\\hat y_i$", "$e_i$", "$e_i^2$", "share of the sum"], "TABLE", {"num": [0, 1, 2, 3, 4, 5]}),
        ("p", "In vector form MSE is the squared Euclidean norm of the error vector divided by $n$:"),
        ("eq", r"\mathrm{MSE}(y,\hat y)=\frac{1}{n}\,\bigl\|y-\hat y\bigr\|_2^2,\qquad \mathrm{RMSE}=\sqrt{\mathrm{MSE}}"),
        ("p", "Hence its second name, the <b>L2 loss</b>. The units of MSE are the units of $y$ squared: roubles², minutes². To get back to the original units, take the square root and you get <a href=\"../rmse/\">RMSE</a>; in the example $\\sqrt{1.417}\\approx1.190$."),
    ]),
    dict(id="properties", title="Properties and the best constant", blocks=[
        ("ul", [
            "<b>Non-negativity</b>: $\\mathrm{MSE}\\ge0$, with equality only for exact predictions.",
            "<b>Quadratic scaling</b>: multiply $y$ and $\\hat y$ by $k$ and MSE is multiplied by $k^2$. Converting roubles to thousands of roubles shrinks MSE a million times.",
            "<b>Smoothness and convexity</b>: MSE is a quadratic function of the predictions; for a linear model, a quadratic function of the parameters. If the columns of the feature matrix (together with the column of ones for the intercept) are linearly independent, it is strictly convex and the minimum is unique.",
            "<b>Error decomposition</b>: $\\mathrm{MSE}=\\bar e^{\\,2}+\\operatorname{Var}(e)$ — the squared mean bias plus the spread of the errors. In the example $\\bar e=-0.5$: $1.417=0.25+1.167$.",
            "<b>Comparison with MAE</b>: $\\mathrm{MSE}\\ge\\mathrm{MAE}^2$ (the mean of squares is at least the square of the mean). In the example: $1.417\\ge0.833^2\\approx0.694$.",
        ]),
        ("h3", "The best constant is the mean"),
        ("p", "If the model answers with a single number $c$, MSE as a function of $c$ is a parabola. Expand it by adding and subtracting the mean $\\bar y$:"),
        ("eq", r"\mathrm{MSE}(c)=\frac1n\sum_{i=1}^{n}(y_i-c)^2=\underbrace{\frac1n\sum_{i=1}^{n}(y_i-\bar y)^2}_{\operatorname{Var}(y)}+\;(c-\bar y)^2"),
        ("p", "The first term does not depend on $c$; the second is non-negative and vanishes only at $c=\\bar y$. So the minimum of MSE is unique and is attained at the <b>mean</b>, and its value is the variance of the data. The derivative $2(c-\\bar y)$ is a straight line proportional to the distance from the mean."),
        ("viz", "mse-mean", {"c": 12}, "<b>Figure 2.</b> $\\mathrm{MSE}(c)$ for the sample $(2,\\,3,\\,5,\\,9,\\,16)$ and its derivative. The mean is $\\bar y=7$ and the minimum is $\\operatorname{Var}=26$. At $c=12$: $\\mathrm{MSE}=26+(12-7)^2=51$, and the derivative is $2\\cdot5=10$. The median $5$ gives $30$ — under MSE it is worse than the mean. Turn on the outlier ($16\\to40$): the mean moves to $11.8$, the variance grows to $204.56$, while the median stays at $5$."),
        ("deep", "Proof of the decomposition MSE(c) = Var + (c − ȳ)²", [
            ("p", "Write $y_i-c=(y_i-\\bar y)+(\\bar y-c)$ and square it:"),
            ("eq", r"\sum_{i=1}^{n}(y_i-c)^2=\sum_{i=1}^{n}(y_i-\bar y)^2+2(\bar y-c)\sum_{i=1}^{n}(y_i-\bar y)+n(\bar y-c)^2"),
            ("p", "The middle term is zero because deviations from the mean sum to zero: $\\sum(y_i-\\bar y)=n\\bar y-n\\bar y=0$. Divide by $n$ to get the decomposition. The same algebra gives the formula $\\mathrm{MSE}=\\bar e^{\\,2}+\\operatorname{Var}(e)$ and, in its probabilistic version, the bias–variance decomposition."),
        ]),
        ("callout", "note", "Compare with MAE", "For MAE the best constant is the median, which ignores the outlier. For MSE it is the mean, which the outlier drags along: one point moved by $\\Delta$ moves the mean by $\\Delta/n$, however large $\\Delta$ is. The <a href=\"../mae/\">MAE page</a> runs the same experiment for the median."),
    ]),
    dict(id="derivative", title="The derivative: a force proportional to the error", blocks=[
        ("p", "The derivative of the square is $2e$. The further the prediction is from the truth, the harder the gradient pulls it back, and at the minimum itself the force fades out smoothly. This is exactly what makes MSE so convenient for gradient descent."),
        ("deep", "Derivation: the derivative of MSE with respect to the predictions and the parameters", [
            ("p", "For one object $\\ell=(y_i-\\hat y_i)^2$. By the chain rule, with $\\partial e_i/\\partial\\hat y_i=-1$:"),
            ("eq", r"\frac{\partial\,\mathrm{MSE}}{\partial\hat y_i}=\frac1n\cdot2e_i\cdot(-1)=-\frac{2}{n}\bigl(y_i-\hat y_i\bigr)"),
            ("p", "For a linear model $\\hat y_i=wx_i+b$:"),
            ("eq", r"\frac{\partial\,\mathrm{MSE}}{\partial w}=-\frac2n\sum_{i=1}^{n}e_i\,x_i,\qquad \frac{\partial\,\mathrm{MSE}}{\partial b}=-\frac2n\sum_{i=1}^{n}e_i"),
            ("p", "In matrix form, with $\\hat y=X\\theta$: $\\nabla_\\theta\\,\\mathrm{MSE}=\\frac2nX^\\top(X\\theta-y)$, and the Hessian $\\frac2nX^\\top X$ does not depend on $\\theta$ — the curvature of the bowl is the same everywhere."),
            ("p", "The second derivative with respect to each prediction is constant: $\\partial^2\\mathrm{MSE}/\\partial\\hat y_i^2=2/n$. That is why in gradient boosting on MSE the Newton step is simply the mean residual in a leaf, and each new tree is trained on the residuals $y_i-F(x_i)$."),
        ]),
        ("eq", r"\frac{\partial\,\mathrm{MSE}}{\partial\hat y_i}=-\frac{2}{n}\bigl(y_i-\hat y_i\bigr)"),
        ("p", "Look at gradient descent on a single error. The step $\\hat y\\leftarrow\\hat y-\\eta\\,\\partial e^2/\\partial\\hat y=\\hat y+2\\eta e$ turns the error into $e\\leftarrow(1-2\\eta)\\,e$. Each step multiplies the error by the same number — a geometric progression."),
        ("viz", "mse-derivative", {"e": 2.5, "eta": 0.3}, "<b>Figure 3.</b> On the left, the parabola $e^2$, the tangent at the starting point and the descent steps; on the right, the derivative $2e$: the lengths of the blue segments, i.e. the gradients, shrink together with the error. With $e_0=2.5$ and $\\eta=0.3$ the factor is $1-2\\eta=0.4$: the errors are $1$, $0.4$, $0.16$. Change the step: for $\\eta&lt;0.5$ the error decreases monotonically, at $\\eta=0.5$ it vanishes in one step, for $0.5&lt;\\eta&lt;1$ it decreases with oscillations, at $\\eta=1$ it swings forever, and for $\\eta&gt;1$ it grows."),
        ("callout", "intuition", "Compare with MAE", "For $|e|$ the derivative $\\pm1$ does not depend on the size of the error, so steps with a constant $\\eta$ do not get shorter and the descent jitters around the minimum (see <a href=\"../mae/\">MAE</a>). For $e^2$ the “brakes” are built in: the gradient shrinks by itself near the bottom, and a constant step is enough for exact convergence."),
    ]),
    dict(id="space", title="The bowl over the parameters: least squares and gradient descent", blocks=[
        ("p", "Take the line $\\hat y=wx+b$ and five points: $x=(1,\\,2,\\,3,\\,4,\\,5)$, $y=(1.3,\\,2,\\,3.1,\\,4.5,\\,7)$. MSE as a function of $(w,\\,b)$ is a quadratic form, and its graph is an <b>elliptic bowl</b> (a paraboloid) with a single bottom."),
        ("h3", "The exact solution: the normal equations"),
        ("p", "Setting the gradient to zero gives a linear system — the normal equations — and the least-squares solution:"),
        ("eq", r"X^\top X\,\theta=X^\top y\quad\Longrightarrow\quad\theta^*=(X^\top X)^{-1}X^\top y;\qquad w^*=\frac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)},\quad b^*=\bar y-w^*\bar x"),
        ("p", "For our points $w^*=1.39$, $b^*=-0.59$, $\\mathrm{MSE}^*=0.2294$. In practice the inverse matrix is not computed: QR or SVD decompositions are used (<code>np.linalg.lstsq</code>), and on large data, gradient descent."),
        ("h3", "Gradient descent and the shape of the bowl"),
        ("p", "The speed of descent is set by the shape of the bowl — the eigenvalues of the Hessian $H=\\frac2nX^\\top X$. Along the steep direction ($\\lambda_{\\max}$) too large a step throws you over the bottom; along the flat one ($\\lambda_{\\min}$) the descent crawls. For our data $\\lambda_{\\max}=23.66$ and $\\lambda_{\\min}=0.338$; their ratio, the condition number, is about $70$: the bowl is stretched into a narrow ravine, and any step above $\\eta_{\\text{crit}}=2/\\lambda_{\\max}\\approx0.0845$ diverges."),
        ("viz", "mse-bowl", {"eta": 0.05}, "<b>Figure 4.</b> On the left, the bowl $\\mathrm{MSE}(w,b)$ (you can rotate it); on the right, the view from above and the excess over the minimum on a log scale. The start is the line $y=3$, $\\eta=0.05$. In 150 steps the descent gets down the ravine only to an excess of $1.5\\cdot10^{-2}$; at $\\eta=0.09$ it blows up. Switch to the centred feature $x-\\bar x$: the Hessian becomes diagonal ($\\lambda=4$ and $2$), the condition number drops to $2$, the admissible step grows to $0.5$, and with the same $\\eta=0.05$ the excess is below $10^{-6}$ already at step 61, and at $\\eta=0.2$ at step 13."),
        ("deep", "Why the convergence condition is η < 2/λ_max", [
            ("p", "For a quadratic function the gradient is linear: $\\nabla\\mathrm{MSE}(\\theta)=H(\\theta-\\theta^*)$. A descent step gives"),
            ("eq", r"\theta_{t+1}-\theta^*=(I-\eta H)(\theta_t-\theta^*)\quad\Longrightarrow\quad\theta_t-\theta^*=(I-\eta H)^t(\theta_0-\theta^*)"),
            ("p", "In the eigenbasis of $H$ each coordinate is multiplied by $1-\\eta\\lambda_k$ at every step. The descent converges if $|1-\\eta\\lambda_k|&lt;1$ for all $k$, i.e. $0&lt;\\eta&lt;2/\\lambda_{\\max}$. For $1/\\lambda_{\\max}&lt;\\eta&lt;2/\\lambda_{\\max}$ the factor is negative — hence the zigzag across the ravine. The slowest direction is $\\lambda_{\\min}$: even with the best constant step $\\eta=2/(\\lambda_{\\max}+\\lambda_{\\min})$ the error shrinks by a factor $(\\kappa-1)/(\\kappa+1)$ per step, where $\\kappa=\\lambda_{\\max}/\\lambda_{\\min}$. At $\\kappa=70$ that is $0.97$ — hundreds of steps; at $\\kappa=2$ it is $1/3$."),
        ]),
        ("callout", "key", "The practical takeaway", "Standardize the features (subtract the mean, divide by the standard deviation): this rounds the bowl and allows a larger step. Adaptive optimizers (<a href=\"../adam/\">Adam</a>, RMSProp) do a similar rescaling automatically, but only coordinate by coordinate: a ravine tilted relative to the axes, like ours, is straightened only partly."),
    ]),
    dict(id="biasvar", title="Bias and variance", blocks=[
        ("p", "MSE on new data splits into three parts, and this is perhaps the most important formula about overfitting. Let $y=f(x)+\\varepsilon$, where the noise has mean $0$ and variance $\\sigma^2$, and let the model $\\hat f$ be trained on a random sample. Then the expected error at a point $x$ is:"),
        ("eq", r"\mathbb E\bigl[(y-\hat f(x))^2\bigr]=\underbrace{\bigl(f(x)-\mathbb E\hat f(x)\bigr)^2}_{\text{bias}^2}+\underbrace{\mathbb E\bigl[(\hat f(x)-\mathbb E\hat f(x))^2\bigr]}_{\text{variance}}+\underbrace{\sigma^2}_{\text{noise}}"),
        ("symbols", [
            (r"\mathbb E\hat f(x)", "the average prediction over all possible training samples;"),
            (r"\text{bias}^2", "how far the average model misses the truth — the price of a too simple model;"),
            (r"\text{variance}", "how much the model changes from sample to sample — the price of a too flexible model;"),
            (r"\sigma^2", "irreducible noise: no model can remove it."),
        ]),
        ("viz", "mse-biasvar", {"d": 3}, "<b>Figure 5.</b> The truth $f(x)=\\sin\\pi x$, 15 points with noise $\\sigma=0.3$, 200 different training samples, polynomials of degree $d$. A line ($d=1$) is biased: $0.204+0.012+0.09=0.306$. At $d=3$ the expected error is minimal: $0.005+0.025+0.09=0.120$. At $d=10$ the bias barely changes ($0.005$), but the variance shoots up to $0.777$ and the test MSE is $0.872$, even though the training MSE is only $0.022$ — less than the noise itself, $\\sigma^2=0.09$: the model memorizes the noise."),
        ("deep", "Deriving the decomposition", [
            ("p", "Denote $\\bar f=\\mathbb E\\hat f(x)$. The noise $\\varepsilon$ at a new point does not depend on the training sample, so"),
            ("eq", r"\mathbb E(y-\hat f)^2=\mathbb E(f+\varepsilon-\hat f)^2=\sigma^2+\mathbb E(f-\hat f)^2"),
            ("p", "Then repeat the trick from the section on the constant: $f-\\hat f=(f-\\bar f)+(\\bar f-\\hat f)$, and the cross term vanishes because $\\mathbb E(\\bar f-\\hat f)=0$:"),
            ("eq", r"\mathbb E(f-\hat f)^2=(f-\bar f)^2+\mathbb E(\hat f-\bar f)^2"),
            ("p", "In the figure the same quantities are averaged over a uniform grid $x\\in[-1,\\,1]$. Even degrees add almost nothing for the odd function $\\sin\\pi x$: the bias at $d=1$ and $d=2$ is the same."),
        ]),
        ("callout", "note", "A biased estimate can be better", "What has to be minimized is the sum, not the bias alone. Regularization (ridge regression, early stopping, model averaging) deliberately introduces bias to reduce variance even more, and often lowers the test MSE."),
    ]),
    dict(id="probability", title="The probabilistic meaning: Gaussian noise", blocks=[
        ("p", "Why the square of all things? The classical answer was given by Gauss (1809). Let $y_i=\\hat y_i+\\varepsilon_i$, where the noise $\\varepsilon_i$ is independent and normally distributed, $N(0,\\sigma^2)$. The density of one observation is a bell around the prediction, and the likelihood of the sample is the product of the heights of the bells at the data points. The negative log-likelihood is:"),
        ("eq", r"-\ln L=\frac n2\ln(2\pi\sigma^2)+\frac{1}{2\sigma^2}\sum_{i=1}^{n}\bigl(y_i-\hat y_i\bigr)^2=\frac n2\ln(2\pi\sigma^2)+\frac{n}{2\sigma^2}\,\mathrm{MSE}"),
        ("p", "For any fixed $\\sigma$ this is an increasing linear function of MSE. Hence <b>minimizing MSE is maximum likelihood under Gaussian noise</b>. Minimizing over $\\sigma$ gives one more link: $\\hat\\sigma^2=\\mathrm{MSE}$. Later (1821–1823) Gauss gave a second justification that needs no normality: if the errors are unbiased, uncorrelated and have equal variance, the least-squares estimate has the smallest variance among all linear unbiased estimates (the Gauss–Markov theorem)."),
        ("viz", "mse-gauss", {"w": 1, "b": 0.5, "s": 0.6}, "<b>Figure 6.</b> On the left, a line and the normal bells $N(\\hat y_i,\\sigma^2)$ around it; the orange segments are the heights of the bells at the data points, i.e. each point’s contribution to the likelihood. On the right, $-\\ln L$ as a function of MSE at the current $\\sigma$: a straight line. For $w=1$, $b=0.5$, $\\sigma=0.6$: $\\mathrm{MSE}=0.540$ and $-\\ln L=5.791$; the least-squares line (red point) with $\\mathrm{MSE}=0.229$ gives $-\\ln L=3.634$. The best $\\sigma$ for the current line is $\\sqrt{0.54}\\approx0.735$."),
        ("p", "One more statement of the same fact: among all functions $g(x)$ the expected squared error $\\mathbb E(y-g(x))^2$ is smallest for $g(x)=\\mathbb E[y\\mid x]$. A model trained on MSE estimates the <b>conditional mean</b>. If the noise is asymmetric or heavy-tailed, the conditional mean can describe the “typical” outcome poorly — then one looks at the median (<a href=\"../mae/\">MAE</a>) or at quantiles."),
    ]),
    dict(id="outliers", title="Outliers: unbounded influence", blocks=[
        ("p", "The flip side of the square is sensitivity to anomalous points. The gradient from an object is proportional to its error, so a distant outlier pulls the model harder the further away it is. Robust statistics says that least squares has an <b>unbounded influence function</b> and a breakdown point of zero: a single point is enough to drive the line arbitrarily far."),
        ("viz", "mse-outlier", {"y": 0}, "<b>Figure 7.</b> Ten points around $y=1+0.5x$ and an outlier at $x=9$. With the outlier at $y=0$ the slope of the MSE line drops to $0.291$, and the outlier alone accounts for $74\\%$ of the sum of squares. On the right, the slope as a function of the outlier’s height: for MSE it is a straight line (each unit of height changes the slope by $0.0375$, from $0.104$ at $y=-5$ to $0.779$ at $y=13$), while for MAE the slope stays between $0.438$ and $0.514$."),
        ("p", "What to do about outliers if you need MSE:"),
        ("ul", [
            "replace the loss with <a href=\"../huber/\">Huber</a>: a square for small errors and the absolute value for large ones — the smoothness of MSE and the bounded influence of MAE;",
            "transform the target ($\\log y$ for prices and incomes) — but then the model estimates the mean of the logarithm, not the mean of $y$;",
            "find and inspect outliers by their residuals: points with a huge $e_i^2$ stand out immediately;",
            "use robust fitting algorithms (RANSAC, Theil–Sen) that learn from subsets of the data.",
        ]),
    ]),
    dict(id="code", title="In code", blocks=[
        ("p", "MSE and its gradient in NumPy, the exact least-squares solution, and a check that the best constant is the mean:"),
        ("code", "python", "CODE_NUMPY"),
        ("p", "In PyTorch it is <code>MSELoss</code>. The gradient with respect to the predictions is $2(\\hat y-y)/n$; descent with step $0.05$ on the raw feature from Figure 4 reaches the same least-squares solution, but slowly: to two decimals it takes about 300 steps (the listing runs 2000 to be safe):"),
        ("code", "python", "CODE_TORCH"),
        ("p", "scikit-learn has MSE and RMSE metrics (the regressors’ <code>score</code> method returns $R^2$, though), <code>LinearRegression</code> minimizes MSE exactly, and boosting uses it as the default loss:"),
        ("code", "python", "CODE_SKLEARN"),
        ("callout", "key", "The rule", "Train on MSE, but in reports show <a href=\"../rmse/\">RMSE</a> (same units as $y$) next to <a href=\"../mae/\">MAE</a>. A large gap between them signals a heavy tail or outliers in the errors."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>Reading MSE as the “average error”</b>. MSE $=1.417$ in the example is in squared units; the average error is of order $\\sqrt{1.417}\\approx1.19$ (RMSE) or $0.833$ (MAE).",
            "<b>MSE on data with outliers</b>. A few anomalies will drag the model along (Figure 7). Clean the data, or use <a href=\"../huber/\">Huber</a> or MAE.",
            "<b>Unscaled features</b>. A stretched bowl means slow descent and a small admissible step (Figure 4). Standardize the features.",
            "<b>Too large a step</b>. With $\\eta&gt;2/\\lambda_{\\max}$ the loss grows exponentially and quickly turns into <code>inf</code> and <code>nan</code>.",
            "<b>MSE for classification on top of a sigmoid</b>. The gradient $2(p-y)\\,p(1-p)$ vanishes when the model is confidently wrong ($p\\approx0$ for $y=1$). For probabilities use <a href=\"../bce/\">BCE</a> or <a href=\"../cross-entropy/\">cross-entropy</a>.",
            "<b>Judging a model by its training MSE</b>. A low MSE on the training data can mean memorized noise (Figure 5, $d=10$). Look at validation.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../mae/\">MAE</a>: the absolute value instead of the square — the median instead of the mean, robustness to outliers, but a kink at zero.",
            "<a href=\"../rmse/\">RMSE</a>: $\\sqrt{\\mathrm{MSE}}$ — the same optimal model, but the error in the units of $y$.",
            "<a href=\"../huber/\">Huber</a>: MSE near zero and MAE in the tails.",
            "<a href=\"../bce/\">BCE</a>: the analogue of MSE for probabilities — also maximum likelihood, but for the Bernoulli distribution.",
            "<a href=\"../sgd/\">SGD</a> and <a href=\"../adam/\">Adam</a>: MSE shows clearly how the step and the conditioning of the problem determine convergence.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $\\mathrm{MSE}=\\frac1n\\sum(y_i-\\hat y_i)^2$ is the average area of the squares on the errors; $1.417$ in the example, with $94\\%$ coming from a single error. 2) The best constant is the mean, and $\\mathrm{MSE}(c)=\\operatorname{Var}+(c-\\bar y)^2$. 3) The gradient $-\\frac2n(y_i-\\hat y_i)$ is proportional to the error and fades by itself near the minimum. 4) For a linear model MSE is a bowl with the exact solution $(X^\\top X)^{-1}X^\\top y$; gradient descent converges for $\\eta&lt;2/\\lambda_{\\max}$, and its speed is set by the condition number. 5) Test MSE = bias² + variance + noise. 6) MSE is the likelihood under Gaussian noise; the model estimates the conditional mean. 7) The price is the unbounded influence of outliers."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="$y=(1,\\,4,\\,6)$, $\\hat y=(2,\\,4,\\,3)$. What is MSE?", options=["$3.333$", "$1.333$", "$1.826$", "$10$"], answer=0,
                 explain="The errors are $(-1,\\,0,\\,3)$, the squares $(1,\\,0,\\,9)$, $\\mathrm{MSE}=10/3\\approx3.333$. $1.333$ is MAE, $1.826$ is RMSE, $10$ is the sum of squares without dividing by $n$."),
            dict(q="Which constant minimizes MSE for the sample $(1,\\,2,\\,3,\\,10,\\,50)$?", options=["$3$", "$13.2$", "$10$", "$50$"], answer=1,
                 explain="The minimum of MSE is at the mean: $(1+2+3+10+50)/5=13.2$. The median $3$ minimizes MAE."),
            dict(q="What is $\\partial\\,\\mathrm{MSE}/\\partial\\hat y_i$?", options=["$-\\frac2n(y_i-\\hat y_i)$", "$-\\frac1n\\operatorname{sign}(y_i-\\hat y_i)$", "$(y_i-\\hat y_i)^2$", "$\\frac2n$"], answer=0,
                 explain="$\\frac{\\partial}{\\partial\\hat y_i}\\frac1n(y_i-\\hat y_i)^2=\\frac1n\\cdot2(y_i-\\hat y_i)\\cdot(-1)$. The option with the sign is the derivative of MAE, and $\\frac2n$ is the second derivative."),
            dict(q="The eigenvalues of the MSE Hessian are $4$ and $2$. For which constant steps $\\eta&gt;0$ does gradient descent converge?", options=["$\\eta&lt;0.25$", "$\\eta&lt;0.5$", "$\\eta&lt;1$", "$\\eta&lt;2$"], answer=1,
                 explain="The condition $|1-\\eta\\lambda|&lt;1$ for all eigenvalues gives $\\eta&lt;2/\\lambda_{\\max}=2/4=0.5$. That is exactly the centred case of Figure 4."),
            dict(q="Minimizing MSE coincides with maximum likelihood if the noise is…", options=["Laplace", "normal", "uniform", "Poisson"], answer=1,
                 explain="With normal noise $-\\ln L=\\frac n2\\ln(2\\pi\\sigma^2)+\\frac{n}{2\\sigma^2}\\mathrm{MSE}$, an increasing function of MSE. Laplace noise corresponds to MAE."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "Agar model son bashorat qilsa, deyarli aniq uni MSE (mean squared error) — <b>xatoning o‘rtacha kvadratini</b> kamaytirib o‘qitishgan. Bu regressiya uchun «standart» yo‘qotish: chiziqli modellar uchun uning aniq yechimi, neyron tarmoqlar uchun silliq gradiyenti va aniq statistik ma’nosi bor. Lejandr 1805 yilda e’lon qilgan, Gauss esa 1809 yilda xatolarning normal qonuni bilan bog‘lagan eng kichik kvadratlar usuli — aynan MSE’ni minimallashtirishdir."),
        ("p", "U qayerda uchraydi:"),
        ("ul", [
            "<b>chiziqli regressiya</b> — bitta formulali yechimga ega eng kichik kvadratlar usuli (EKK, ordinary least squares);",
            "<b>regressiya uchun neyron tarmoqlar</b> — PyTorch’da <code>MSELoss</code>, Keras’da <code>\"mse\"</code>; kirishni tiklaydigan avtoenkoderlar;",
            "<b>diffuziya modellari</b> — tarmoq qo‘shilgan shovqinni bashorat qilishni o‘rganadi va yo‘qotish — haqiqiy va bashorat qilingan shovqin orasidagi MSE;",
            "<b>mustahkamlab o‘qitish</b> — qiymat funksiyasi ko‘pincha TD-xato kvadratida o‘qitiladi;",
            "<b>gradiyent busting</b> — <code>loss=\"squared_error\"</code>: MSE antigradiyenti qoldiqqa teng, shuning uchun har bir daraxt qoldiqlarga moslashtiriladi;",
            "<b>signal va tasvirlarga ishlov berish</b> — PSNR MSE orqali hisoblanadi, Kalman filtri xato kvadratining kutilmasini minimallashtiradi.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "MSE — xatolar kvadratlarining o‘rtachasi: $\\frac1n\\sum(y_i-\\hat y_i)^2$. Kvadrat yo‘qotishni yagona tubli silliq kosaga aylantiradi, uning gradiyenti $-\\frac2n(y_i-\\hat y_i)$ xatoga proporsional, eng yaxshi o‘zgarmas esa — <b>o‘rtacha</b>. Teskari tomoni — kvadrat katta adashishlarni bo‘rttiradi: 10 ga teng bitta xato 1 ga teng yuzta xato bilan teng vaznga ega, shuning uchun MSE chetga chiquvchi qiymatlarga sezgir va kvadrat birliklarda o‘lchanadi."),
    ]),
    dict(id="intuition", title="Intuitsiya: kvadratlar yuzi", blocks=[
        ("p", "Bu yerda «kvadrat» so‘zini tom ma’noda tushunish mumkin. Har bir xato ustiga tomoni $|e_i|$ bo‘lgan kvadrat chizamiz. Uning yuzi — $e_i^2$, MSE esa — <b>kvadratlarning o‘rtacha yuzi</b>. Kesmalar uzunligi o‘rtachalanadigan MAE bilan solishtiring: yuz tomonning kvadrati kabi o‘sadi, shuning uchun katta xatolar nomutanosib ko‘p joy egallaydi."),
        ("p", "Quyida qo‘llanmaning umumiy misoli: $y=(3;\\,5;\\,8)$, $\\hat y=(2{,}5;\\,5;\\,10)$. Ko‘k bashoratlarni torting. Pastki grafikda xatolar $e^2$ parabolasi ustida turadi; MSE — bu nuqtalarning o‘rtacha balandligi."),
        ("viz", "mse-squares", {"yhat": [2.5, 5, 10]}, "<b>1-rasm.</b> Umumiy misol xatolarining kvadratlari. Yuzlar $0{,}25$, $0$ va $4$, yig‘indi $4{,}25$, $\\mathrm{MSE}=4{,}25/3\\approx1{,}417$. Uchinchi kvadrat — butun yuzning $94\\%$ i. Uchinchi bashoratni $8$ ga qo‘ying — MSE $0{,}25/3\\approx0{,}083$ gacha tushadi."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "$2$ xato $0{,}5$ xatodan 4 marta katta, uning kvadrati esa 16 marta katta. Shuning uchun MSE’da o‘qitilgan model katta adashishlardan «qo‘rqadi» va bitta kattasini yo‘qotish uchun bir nechta mayda xatolarga bajonidil rozi bo‘ladi. Bu ham afzallik (katta xatolar odatda qimmatroq), ham zaiflik (ma’lumotlardagi chetga chiquvchi qiymat ham «katta xato» bo‘lib ko‘rinadi)."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", "MAE’dagi o‘sha to‘rtta amal, faqat modul o‘rniga — kvadrat."),
        ("eq", r"\underbrace{y_i-\hat y_i}_{\text{xato }e_i}\;\longrightarrow\;\underbrace{e_i^2}_{\text{yuz}}\;\longrightarrow\;\underbrace{\sum_{i=1}^{n}e_i^2}_{\text{SSE}}\;\longrightarrow\;\underbrace{\frac1n\sum_{i=1}^{n}e_i^2}_{\text{MSE}}"),
        ("symbols", [
            (r"y_i", "$i$-obyekt uchun haqiqiy qiymat;"),
            (r"\hat y_i", "model bashorati;"),
            (r"e_i=y_i-\hat y_i", "xato (qoldiq); kvadratga oshirilgandan keyin uning ishorasi yo‘qoladi;"),
            (r"e_i^2", "kvadrat: manfiy emas, silliq va xato qancha katta bo‘lsa, shuncha tez o‘sadi;"),
            (r"\sum e_i^2", "qoldiqlar kvadratlari yig‘indisi — SSE (sum of squared errors) yoki RSS (residual sum of squares);"),
            (r"\frac1n", "o‘rtachalash: MSE tanlanma hajmiga bog‘liq emas."),
        ]),
        ("p", "Nega modul emas, kvadrat? Uchta sabab bor. <b>Silliqlik</b>: $e^2$ ning $2e$ hosilasi hamma joyda, jumladan nolda ham bor. <b>Algebra</b>: kvadratlar yig‘indisi — kvadratik forma, uning minimumi chiziqli sistemani (normal tenglamalarni) yechib topiladi. <b>Geometriya</b>: $\\sum e_i^2$ — Yevklid masofasining kvadrati, eng yaxshi bashorat esa Pifagor teoremasidagidek ortogonal proyeksiya."),
        ("table", ["$i$", "$y_i$", "$\\hat y_i$", "$e_i$", "$e_i^2$", "yig‘indidagi ulush"], "TABLE", {"num": [0, 1, 2, 3, 4, 5]}),
        ("p", "Vektor ko‘rinishida MSE — xatolar vektori Yevklid normasining $n$ ga bo‘lingan kvadrati:"),
        ("eq", r"\mathrm{MSE}(y,\hat y)=\frac{1}{n}\,\bigl\|y-\hat y\bigr\|_2^2,\qquad \mathrm{RMSE}=\sqrt{\mathrm{MSE}}"),
        ("p", "Ikkinchi nomi shundan — <b>L2-yo‘qotish</b>. MSE birliklari — $y$ birliklarining kvadrati: so‘m², daqiqa². Dastlabki birliklarga qaytish uchun ildiz olinadi va <a href=\"../rmse/\">RMSE</a> hosil bo‘ladi; misolda $\\sqrt{1{,}417}\\approx1{,}190$."),
    ]),
    dict(id="properties", title="Xossalar va eng yaxshi o‘zgarmas", blocks=[
        ("ul", [
            "<b>Manfiy emaslik</b>: $\\mathrm{MSE}\\ge0$, tenglik — faqat aniq bashoratlarda.",
            "<b>Kvadratik masshtab</b>: $y$ va $\\hat y$ ni $k$ ga ko‘paytirsak, MSE $k^2$ ga ko‘payadi. So‘mni ming so‘mga o‘tkazish MSE’ni million marta kamaytiradi.",
            "<b>Silliqlik va qavariqlik</b>: MSE — bashoratlarning kvadratik funksiyasi; chiziqli model uchun — parametrlarning kvadratik funksiyasi. Belgilar matritsasining ustunlari (siljish uchun birlar ustuni bilan birga) chiziqli erkli bo‘lsa, u qat’iy qavariq va minimum yagona.",
            "<b>Xatolar yoyilmasi</b>: $\\mathrm{MSE}=\\bar e^{\\,2}+\\operatorname{Var}(e)$ — o‘rtacha siljish kvadrati plyus xatolar tarqoqligi. Misolda $\\bar e=-0{,}5$: $1{,}417=0{,}25+1{,}167$.",
            "<b>MAE bilan solishtirish</b>: $\\mathrm{MSE}\\ge\\mathrm{MAE}^2$ (kvadratlar o‘rtachasi o‘rtachaning kvadratidan kam emas). Misolda: $1{,}417\\ge0{,}833^2\\approx0{,}694$.",
        ]),
        ("h3", "Eng yaxshi o‘zgarmas — o‘rtacha"),
        ("p", "Agar model bitta $c$ son bilan javob bersa, $c$ ning funksiyasi sifatida MSE — parabola. $\\bar y$ o‘rtachani qo‘shib va ayirib qavslarni ochamiz:"),
        ("eq", r"\mathrm{MSE}(c)=\frac1n\sum_{i=1}^{n}(y_i-c)^2=\underbrace{\frac1n\sum_{i=1}^{n}(y_i-\bar y)^2}_{\operatorname{Var}(y)}+\;(c-\bar y)^2"),
        ("p", "Birinchi qo‘shiluvchi $c$ ga bog‘liq emas, ikkinchisi manfiy emas va faqat $c=\\bar y$ da nolga aylanadi. Demak, MSE minimumi yagona va <b>o‘rtachada</b> erishiladi, uning qiymati esa — ma’lumotlar dispersiyasi. $2(c-\\bar y)$ hosila — o‘rtachagacha bo‘lgan masofaga proporsional to‘g‘ri chiziq."),
        ("viz", "mse-mean", {"c": 12}, "<b>2-rasm.</b> $(2;\\,3;\\,5;\\,9;\\,16)$ tanlanma uchun $\\mathrm{MSE}(c)$ va uning hosilasi. O‘rtacha $\\bar y=7$, minimum $\\operatorname{Var}=26$. $c=12$ da: $\\mathrm{MSE}=26+(12-7)^2=51$, hosila $2\\cdot5=10$. Mediana $5$ esa $30$ beradi — MSE uchun u o‘rtachadan yomonroq. Chetga chiquvchi qiymatni yoqing ($16\\to40$): o‘rtacha $11{,}8$ ga ketadi, dispersiya $204{,}56$ gacha o‘sadi, mediana esa $5$ bo‘lib qoladi."),
        ("deep", "MSE(c) = Var + (c − ȳ)² yoyilmasining isboti", [
            ("p", "$y_i-c=(y_i-\\bar y)+(\\bar y-c)$ deb yozamiz va kvadratga oshiramiz:"),
            ("eq", r"\sum_{i=1}^{n}(y_i-c)^2=\sum_{i=1}^{n}(y_i-\bar y)^2+2(\bar y-c)\sum_{i=1}^{n}(y_i-\bar y)+n(\bar y-c)^2"),
            ("p", "O‘rtadagi qo‘shiluvchi nolga teng, chunki o‘rtachadan chetlanishlar yig‘indisi nol: $\\sum(y_i-\\bar y)=n\\bar y-n\\bar y=0$. $n$ ga bo‘lib yoyilmani olamiz. Xuddi shu algebra $\\mathrm{MSE}=\\bar e^{\\,2}+\\operatorname{Var}(e)$ formulasini va ehtimoliy shaklda siljish va tarqoqlikka yoyilmani beradi."),
        ]),
        ("callout", "note", "MAE bilan solishtiring", "MAE uchun eng yaxshi o‘zgarmas — mediana va u chetga chiquvchi qiymatni sezmaydi. MSE uchun — o‘rtacha, uni chetga chiquvchi qiymat o‘zi bilan sudraydi: $\\Delta$ ga surilgan bitta nuqta $\\Delta$ qancha bo‘lmasin, o‘rtachani $\\Delta/n$ ga suradi. <a href=\"../mae/\">MAE sahifasida</a> — mediana uchun xuddi shu tajriba."),
    ]),
    dict(id="derivative", title="Hosila: xatoga proporsional kuch", blocks=[
        ("p", "Kvadratning hosilasi — $2e$. Bashorat haqiqatdan qancha uzoq bo‘lsa, gradiyent uni shuncha kuchli orqaga tortadi, minimumning o‘zida esa kuch silliq yo‘qoladi. Aynan shu MSE’ni gradiyent tushish uchun shunchalik qulay qiladi."),
        ("deep", "Keltirib chiqarish: MSE’ning bashoratlar va parametrlar bo‘yicha hosilasi", [
            ("p", "Bitta obyekt uchun $\\ell=(y_i-\\hat y_i)^2$. Zanjir qoidasi bo‘yicha, $\\partial e_i/\\partial\\hat y_i=-1$ bilan:"),
            ("eq", r"\frac{\partial\,\mathrm{MSE}}{\partial\hat y_i}=\frac1n\cdot2e_i\cdot(-1)=-\frac{2}{n}\bigl(y_i-\hat y_i\bigr)"),
            ("p", "$\\hat y_i=wx_i+b$ chiziqli model uchun:"),
            ("eq", r"\frac{\partial\,\mathrm{MSE}}{\partial w}=-\frac2n\sum_{i=1}^{n}e_i\,x_i,\qquad \frac{\partial\,\mathrm{MSE}}{\partial b}=-\frac2n\sum_{i=1}^{n}e_i"),
            ("p", "Matritsa shaklida, $\\hat y=X\\theta$: $\\nabla_\\theta\\,\\mathrm{MSE}=\\frac2nX^\\top(X\\theta-y)$, $\\frac2nX^\\top X$ gessian esa $\\theta$ ga bog‘liq emas — kosaning egriligi hamma joyda bir xil."),
            ("p", "Har bir bashorat bo‘yicha ikkinchi hosila o‘zgarmas: $\\partial^2\\mathrm{MSE}/\\partial\\hat y_i^2=2/n$. Shuning uchun MSE’dagi gradiyent bustingda Nyuton qadami shunchaki bargdagi o‘rtacha qoldiqqa teng va har bir yangi daraxt $y_i-F(x_i)$ qoldiqlarda o‘qitiladi."),
        ]),
        ("eq", r"\frac{\partial\,\mathrm{MSE}}{\partial\hat y_i}=-\frac{2}{n}\bigl(y_i-\hat y_i\bigr)"),
        ("p", "Bitta xato uchun gradiyent tushishni ko‘raylik. $\\hat y\\leftarrow\\hat y-\\eta\\,\\partial e^2/\\partial\\hat y=\\hat y+2\\eta e$ qadami xatoni $e\\leftarrow(1-2\\eta)\\,e$ ga aylantiradi. Har bir qadam xatoni bir xil songa ko‘paytiradi — geometrik progressiya hosil bo‘ladi."),
        ("viz", "mse-derivative", {"e": 2.5, "eta": 0.3}, "<b>3-rasm.</b> Chapda — $e^2$ parabola, boshlang‘ich nuqtadagi urinma va tushish qadamlari; o‘ngda — $2e$ hosila: ko‘k kesmalar uzunligi, ya’ni gradiyentlar xato bilan birga kamayadi. $e_0=2{,}5$ va $\\eta=0{,}3$ da ko‘paytuvchi $1-2\\eta=0{,}4$: xatolar $1$, $0{,}4$, $0{,}16$. Qadamni o‘zgartiring: $\\eta&lt;0{,}5$ da xato monoton kamayadi, $\\eta=0{,}5$ da bir qadamda yo‘qoladi, $0{,}5&lt;\\eta&lt;1$ da — tebranib, $\\eta=1$ da abadiy tebranadi, $\\eta&gt;1$ da o‘sadi."),
        ("callout", "intuition", "MAE bilan solishtiring", "$|e|$ da $\\pm1$ hosila xato kattaligiga bog‘liq emas, shuning uchun o‘zgarmas $\\eta$ li qadamlar qisqarmaydi va tushish minimum yonida titraydi (<a href=\"../mae/\">MAE</a> ga qarang). $e^2$ da «tormoz» ichiga o‘rnatilgan: gradiyent tub yonida o‘z-o‘zidan kamayadi va aniq yaqinlashish uchun o‘zgarmas qadam yetarli."),
    ]),
    dict(id="space", title="Parametrlar ustidagi kosa: EKK va gradiyent tushish", blocks=[
        ("p", "$\\hat y=wx+b$ to‘g‘ri chiziqni va beshta nuqtani olamiz: $x=(1;\\,2;\\,3;\\,4;\\,5)$, $y=(1{,}3;\\,2;\\,3{,}1;\\,4{,}5;\\,7)$. $(w;\\,b)$ funksiyasi sifatida MSE — kvadratik forma, uning grafigi — yagona tubli <b>elliptik kosa</b> (paraboloid)."),
        ("h3", "Aniq yechim: normal tenglamalar"),
        ("p", "Gradiyentni nolga tenglab, chiziqli sistema — normal tenglamalar — va eng kichik kvadratlar usuli yechimini olamiz:"),
        ("eq", r"X^\top X\,\theta=X^\top y\quad\Longrightarrow\quad\theta^*=(X^\top X)^{-1}X^\top y;\qquad w^*=\frac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)},\quad b^*=\bar y-w^*\bar x"),
        ("p", "Bizning nuqtalar uchun $w^*=1{,}39$, $b^*=-0{,}59$, $\\mathrm{MSE}^*=0{,}2294$. Amalda teskari matritsa hisoblanmaydi: QR yoki SVD yoyilmasi (<code>np.linalg.lstsq</code>), katta ma’lumotlarda esa gradiyent tushish ishlatiladi."),
        ("h3", "Gradiyent tushish va kosa shakli"),
        ("p", "Tushish tezligini kosa shakli — $H=\\frac2nX^\\top X$ gessianning xos sonlari belgilaydi. Tik yo‘nalish ($\\lambda_{\\max}$) bo‘ylab juda katta qadam tub ustidan oshirib yuboradi, yotiq yo‘nalish ($\\lambda_{\\min}$) bo‘ylab tushish sudraladi. Bizning ma’lumotlar uchun $\\lambda_{\\max}=23{,}66$, $\\lambda_{\\min}=0{,}338$, ularning nisbati — shartlanganlik soni — taxminan $70$: kosa tor jarlikka cho‘zilgan va $\\eta_{\\text{krit}}=2/\\lambda_{\\max}\\approx0{,}0845$ dan katta qadam uzoqlashishga olib keladi."),
        ("viz", "mse-bowl", {"eta": 0.05}, "<b>4-rasm.</b> Chapda — $\\mathrm{MSE}(w,b)$ kosasi (uni aylantirish mumkin), o‘ngda — yuqoridan ko‘rinish va minimumdan ortiqcha logarifmik shkalada. Start — $y=3$ to‘g‘ri chiziq, $\\eta=0{,}05$. 150 qadamda tushish jarlik bo‘ylab faqat $1{,}5\\cdot10^{-2}$ ortiqchagacha yetadi; $\\eta=0{,}09$ da u sochilib ketadi. Markazlashgan $x-\\bar x$ belgiga o‘ting: gessian diagonal bo‘ladi ($\\lambda=4$ va $2$), shartlanganlik soni $2$ gacha tushadi, joiz qadam $0{,}5$ gacha o‘sadi va o‘sha $\\eta=0{,}05$ da ortiqcha 61-qadamdayoq $10^{-6}$ dan kichik, $\\eta=0{,}2$ da esa 13-qadamda."),
        ("deep", "Nega yaqinlashish sharti — η < 2/λ_max", [
            ("p", "Kvadratik funksiya uchun gradiyent chiziqli: $\\nabla\\mathrm{MSE}(\\theta)=H(\\theta-\\theta^*)$. Tushish qadami beradi"),
            ("eq", r"\theta_{t+1}-\theta^*=(I-\eta H)(\theta_t-\theta^*)\quad\Longrightarrow\quad\theta_t-\theta^*=(I-\eta H)^t(\theta_0-\theta^*)"),
            ("p", "$H$ ning xos vektorlari bazisida har bir koordinata har qadamda $1-\\eta\\lambda_k$ ga ko‘payadi. Barcha $k$ uchun $|1-\\eta\\lambda_k|&lt;1$ bo‘lsa, ya’ni $0&lt;\\eta&lt;2/\\lambda_{\\max}$ da tushish yaqinlashadi. $1/\\lambda_{\\max}&lt;\\eta&lt;2/\\lambda_{\\max}$ da ko‘paytuvchi manfiy — jarlik bo‘ylab zigzag shundan. Eng sekin $\\lambda_{\\min}$ yo‘nalishi yaqinlashadi: hatto eng yaxshi o‘zgarmas $\\eta=2/(\\lambda_{\\max}+\\lambda_{\\min})$ qadamda ham xato har qadamda $(\\kappa-1)/(\\kappa+1)$ marta kamayadi, bu yerda $\\kappa=\\lambda_{\\max}/\\lambda_{\\min}$. $\\kappa=70$ da bu $0{,}97$ — yuzlab qadamlar; $\\kappa=2$ da — $1/3$."),
        ]),
        ("callout", "key", "Amaliy xulosa", "Belgilarni standartlashtiring (o‘rtachani ayiring, standart chetlanishga bo‘ling) — bu kosani yumaloqlaydi va kattaroq qadam olishga imkon beradi. Moslashuvchan optimizatorlar (<a href=\"../adam/\">Adam</a>, RMSProp) shunga o‘xshash masshtablashni avtomatik bajaradi, lekin faqat har bir koordinata bo‘yicha alohida: biznikidek o‘qlarga nisbatan burilgan jarlikni ular faqat qisman to‘g‘rilaydi."),
    ]),
    dict(id="biasvar", title="Siljish va tarqoqlik", blocks=[
        ("p", "Yangi ma’lumotlardagi MSE uch qismdan iborat va bu, ehtimol, ortiqcha moslashish (overfitting) haqidagi eng muhim formula. $y=f(x)+\\varepsilon$ bo‘lsin, shovqinning o‘rtachasi $0$ va dispersiyasi $\\sigma^2$, $\\hat f$ model esa tasodifiy tanlanmada o‘qitilgan. U holda $x$ nuqtadagi kutilgan xato:"),
        ("eq", r"\mathbb E\bigl[(y-\hat f(x))^2\bigr]=\underbrace{\bigl(f(x)-\mathbb E\hat f(x)\bigr)^2}_{\text{siljish}^2}+\underbrace{\mathbb E\bigl[(\hat f(x)-\mathbb E\hat f(x))^2\bigr]}_{\text{tarqoqlik}}+\underbrace{\sigma^2}_{\text{shovqin}}"),
        ("symbols", [
            (r"\mathbb E\hat f(x)", "barcha mumkin bo‘lgan o‘qitish tanlanmalari bo‘yicha o‘rtacha bashorat;"),
            (r"\text{siljish}^2", "o‘rtacha model haqiqatdan qanchalik adashadi — juda oddiy model uchun to‘lov;"),
            (r"\text{tarqoqlik}", "model tanlanmadan tanlanmaga qanchalik o‘zgaradi — juda moslashuvchan model uchun to‘lov;"),
            (r"\sigma^2", "yo‘qotib bo‘lmaydigan shovqin: uni hech qanday model olib tashlamaydi."),
        ]),
        ("viz", "mse-biasvar", {"d": 3}, "<b>5-rasm.</b> Haqiqat $f(x)=\\sin\\pi x$, $\\sigma=0{,}3$ shovqinli 15 nuqta, 200 ta turli o‘qitish tanlanmasi, $d$ darajali polinomlar. To‘g‘ri chiziq ($d=1$) siljigan: $0{,}204+0{,}012+0{,}09=0{,}306$. $d=3$ da kutilgan xato minimal: $0{,}005+0{,}025+0{,}09=0{,}120$. $d=10$ da siljish deyarli o‘zgarmaydi ($0{,}005$), lekin tarqoqlik $0{,}777$ gacha sakraydi va test MSE — $0{,}872$, garchi o‘qitishdagi MSE atigi $0{,}022$ bo‘lsa ham — shovqinning o‘zidan, $\\sigma^2=0{,}09$ dan kichik: model shovqinni yodlab oladi."),
        ("deep", "Yoyilmani keltirib chiqarish", [
            ("p", "$\\bar f=\\mathbb E\\hat f(x)$ deb belgilaymiz. Yangi nuqtadagi $\\varepsilon$ shovqin o‘qitish tanlanmasiga bog‘liq emas, shuning uchun"),
            ("eq", r"\mathbb E(y-\hat f)^2=\mathbb E(f+\varepsilon-\hat f)^2=\sigma^2+\mathbb E(f-\hat f)^2"),
            ("p", "So‘ng o‘zgarmas haqidagi bo‘limdagi usulni takrorlaymiz: $f-\\hat f=(f-\\bar f)+(\\bar f-\\hat f)$, va kesishgan qo‘shiluvchi yo‘qoladi, chunki $\\mathbb E(\\bar f-\\hat f)=0$:"),
            ("eq", r"\mathbb E(f-\hat f)^2=(f-\bar f)^2+\mathbb E(\hat f-\bar f)^2"),
            ("p", "Rasmda xuddi shu kattaliklar $x\\in[-1;\\,1]$ tekis to‘r bo‘yicha o‘rtachalangan. Toq $\\sin\\pi x$ funksiya uchun juft darajalar deyarli hech narsa qo‘shmaydi: $d=1$ va $d=2$ da siljish bir xil."),
        ]),
        ("callout", "note", "Siljigan baho yaxshiroq bo‘lishi mumkin", "Faqat siljishni emas, yig‘indini minimallashtirish kerak. Regulyarizatsiya (ridge regressiya, erta to‘xtatish, modellarni o‘rtachalash) tarqoqlikni ko‘proq kamaytirish uchun ataylab siljish kiritadi va ko‘pincha test MSE’ni pasaytiradi."),
    ]),
    dict(id="probability", title="Ehtimoliy ma’no: normal shovqin", blocks=[
        ("p", "Nega aynan kvadrat? Klassik javobni Gauss (1809) bergan. $y_i=\\hat y_i+\\varepsilon_i$ bo‘lsin, bu yerda $\\varepsilon_i$ shovqin erkli va normal taqsimlangan, $N(0,\\sigma^2)$. Bitta kuzatuv zichligi — bashorat atrofidagi qo‘ng‘iroq, tanlanma o‘xshashligi esa — ma’lumot nuqtalaridagi qo‘ng‘iroqlar balandliklarining ko‘paytmasi. O‘xshashlikning manfiy logarifmi:"),
        ("eq", r"-\ln L=\frac n2\ln(2\pi\sigma^2)+\frac{1}{2\sigma^2}\sum_{i=1}^{n}\bigl(y_i-\hat y_i\bigr)^2=\frac n2\ln(2\pi\sigma^2)+\frac{n}{2\sigma^2}\,\mathrm{MSE}"),
        ("p", "Istalgan belgilangan $\\sigma$ da bu MSE’ning o‘suvchi chiziqli funksiyasi. Demak, <b>MSE’ni minimallashtirish — normal shovqindagi maksimal o‘xshashlik usuli</b>. $\\sigma$ bo‘yicha minimum yana bir bog‘liqlikni beradi: $\\hat\\sigma^2=\\mathrm{MSE}$. Keyinroq (1821–1823) Gauss normallikni talab qilmaydigan ikkinchi asosni ham bergan: agar xatolar siljimagan, korrelyatsiyalanmagan va bir xil dispersiyali bo‘lsa, EKK bahosi barcha chiziqli siljimagan baholar orasida eng kichik dispersiyaga ega (Gauss — Markov teoremasi)."),
        ("viz", "mse-gauss", {"w": 1, "b": 0.5, "s": 0.6}, "<b>6-rasm.</b> Chapda — to‘g‘ri chiziq va uning atrofidagi $N(\\hat y_i,\\sigma^2)$ normal qo‘ng‘iroqlar; to‘q sariq kesmalar — ma’lumot nuqtalaridagi qo‘ng‘iroqlar balandligi, ya’ni har bir nuqtaning o‘xshashlikka hissasi. O‘ngda — joriy $\\sigma$ da MSE funksiyasi sifatida $-\\ln L$: bu to‘g‘ri chiziq. $w=1$, $b=0{,}5$, $\\sigma=0{,}6$ uchun: $\\mathrm{MSE}=0{,}540$, $-\\ln L=5{,}791$; $\\mathrm{MSE}=0{,}229$ bo‘lgan EKK chizig‘i (qizil nuqta) $-\\ln L=3{,}634$ beradi. Joriy chiziq uchun eng yaxshi $\\sigma$ — $\\sqrt{0{,}54}\\approx0{,}735$."),
        ("p", "Xuddi shu faktning yana bir ifodasi: barcha $g(x)$ funksiyalar orasida $\\mathbb E(y-g(x))^2$ kutilgan xato kvadrati $g(x)=\\mathbb E[y\\mid x]$ da minimal. MSE’da o‘qitilgan model <b>shartli o‘rtachani</b> baholaydi. Agar shovqin nosimmetrik yoki og‘ir dumli bo‘lsa, shartli o‘rtacha «tipik» natijani yomon tasvirlashi mumkin — u holda medianaga (<a href=\"../mae/\">MAE</a>) yoki kvantillarga qarashadi."),
    ]),
    dict(id="outliers", title="Chetga chiquvchi qiymatlar: cheklanmagan ta’sir", blocks=[
        ("p", "Kvadratning teskari tomoni — anomal nuqtalarga sezgirlik. Obyektdan keladigan gradiyent uning xatosiga proporsional, shuning uchun uzoqdagi chetga chiquvchi nuqta qancha uzoq bo‘lsa, modelni shuncha kuchli tortadi. Robast statistikada EKK’ning <b>ta’sir funksiyasi cheklanmagan</b> va buzilish nuqtasi (breakdown point) nolga teng deyiladi: to‘g‘ri chiziqni istalgancha uzoqqa olib ketish uchun bitta nuqta yetarli."),
        ("viz", "mse-outlier", {"y": 0}, "<b>7-rasm.</b> $y=1+0{,}5x$ atrofidagi o‘nta nuqta va $x=9$ dagi chetga chiquvchi nuqta. U $y=0$ da bo‘lganda MSE chizig‘ining qiyaligi $0{,}291$ gacha tushadi, chetga chiquvchi nuqtaning o‘zi esa kvadratlar yig‘indisining $74\\%$ ini beradi. O‘ngda — chetga chiquvchi nuqta balandligi funksiyasi sifatida qiyalik: MSE’da bu to‘g‘ri chiziq (balandlikning har bir birligi qiyalikni $0{,}0375$ ga o‘zgartiradi, $y=-5$ da $0{,}104$ dan $y=13$ da $0{,}779$ gacha), MAE’da qiyalik $0{,}438$ va $0{,}514$ orasida qoladi."),
        ("p", "MSE kerak bo‘lsa, chetga chiquvchi qiymatlar bilan nima qilish kerak:"),
        ("ul", [
            "yo‘qotishni <a href=\"../huber/\">Xyuber</a> bilan almashtirish: kichik xatolar uchun kvadrat va kattalar uchun modul — MSE silliqligi va MAE’ning cheklangan ta’siri;",
            "maqsadli o‘zgaruvchini o‘zgartirish (narxlar va daromadlar uchun $\\log y$) — lekin u holda model $y$ ning emas, logarifmning o‘rtachasini baholaydi;",
            "chetga chiquvchilarni qoldiqlar bo‘yicha topish va tekshirish: juda katta $e_i^2$ li nuqtalar darhol ko‘rinadi;",
            "ma’lumotlar qism-to‘plamlarida o‘qitiladigan robast moslashtirish algoritmlaridan (RANSAC, Theil–Sen) foydalanish.",
        ]),
    ]),
    dict(id="code", title="Kodda", blocks=[
        ("p", "NumPy’da MSE va uning gradiyenti, EKK’ning aniq yechimi va eng yaxshi o‘zgarmas o‘rtacha ekanini tekshirish:"),
        ("code", "python", "CODE_NUMPY"),
        ("p", "PyTorch’da — <code>MSELoss</code>. Bashoratlar bo‘yicha gradiyent — $2(\\hat y-y)/n$; 4-rasmdagi xom belgi bo‘yicha $0{,}05$ qadamli tushish o‘sha EKK yechimiga keladi, lekin sekin: ikki xona aniqlikkacha taxminan 300 qadamda (listingda zaxira bilan 2000 qadam):"),
        ("code", "python", "CODE_TORCH"),
        ("p", "scikit-learn’da MSE va RMSE metrikalari bor (regressorlarning <code>score</code> metodi esa $R^2$ qaytaradi), <code>LinearRegression</code> MSE’ni aniq minimallashtiradi, busting esa undan standart yo‘qotish sifatida foydalanadi:"),
        ("code", "python", "CODE_SKLEARN"),
        ("callout", "key", "Qoida", "MSE’da o‘qiting, hisobotlarda esa <a href=\"../mae/\">MAE</a> yonida <a href=\"../rmse/\">RMSE</a>’ni ($y$ bilan bir xil birliklarda) ko‘rsating. Ular orasidagi katta farq — xatolarda og‘ir dum yoki chetga chiquvchilar borligi haqida signal."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b>MSE’ni «o‘rtacha xato» deb o‘qish</b>. Misoldagi MSE $=1{,}417$ — kvadrat birliklarda; o‘rtacha xato $\\sqrt{1{,}417}\\approx1{,}19$ (RMSE) yoki $0{,}833$ (MAE) tartibida.",
            "<b>Chetga chiquvchilari bor ma’lumotlarda MSE</b>. Bir nechta anomaliya modelni o‘zi bilan sudrab ketadi (7-rasm). Ma’lumotlarni tozalang, <a href=\"../huber/\">Xyuber</a> yoki MAE’ni oling.",
            "<b>Masshtablanmagan belgilar</b>. Cho‘zilgan kosa — sekin tushish va kichik joiz qadam (4-rasm). Belgilarni standartlashtiring.",
            "<b>Juda katta qadam</b>. $\\eta&gt;2/\\lambda_{\\max}$ da yo‘qotish eksponensial o‘sadi va tezda <code>inf</code> va <code>nan</code> ga aylanadi.",
            "<b>Sigmoida ustidan klassifikatsiya uchun MSE</b>. Model ishonch bilan adashganda ($y=1$ da $p\\approx0$) $2(p-y)\\,p(1-p)$ gradiyent so‘nadi. Ehtimolliklar uchun <a href=\"../bce/\">BCE</a> yoki <a href=\"../cross-entropy/\">kross-entropiya</a>dan foydalaning.",
            "<b>Modelni o‘qitishdagi MSE bo‘yicha baholash</b>. O‘qitish ma’lumotlaridagi past MSE shovqinni yodlashni anglatishi mumkin (5-rasm, $d=10$). Validatsiyaga qarang.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘liqlik", blocks=[
        ("ul", [
            "<a href=\"../mae/\">MAE</a>: kvadrat o‘rniga modul — o‘rtacha o‘rniga mediana, chetga chiquvchilarga bardoshlilik, lekin nolda sinish.",
            "<a href=\"../rmse/\">RMSE</a>: $\\sqrt{\\mathrm{MSE}}$ — o‘sha optimal model, lekin xato $y$ birliklarida.",
            "<a href=\"../huber/\">Xyuber funksiyasi</a>: nol yonida MSE va dumlarda MAE.",
            "<a href=\"../bce/\">BCE</a>: ehtimolliklar uchun MSE analogi — u ham maksimal o‘xshashlik usuli, lekin Bernulli taqsimoti uchun.",
            "<a href=\"../sgd/\">SGD</a> va <a href=\"../adam/\">Adam</a>: MSE’da qadam va masalaning shartlanganligi yaqinlashishni qanday belgilashi yaxshi ko‘rinadi.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $\\mathrm{MSE}=\\frac1n\\sum(y_i-\\hat y_i)^2$ — xatolar ustidagi kvadratlarning o‘rtacha yuzi; misolda $1{,}417$ va $94\\%$ ini bitta xato beradi. 2) Eng yaxshi o‘zgarmas — o‘rtacha va $\\mathrm{MSE}(c)=\\operatorname{Var}+(c-\\bar y)^2$. 3) $-\\frac2n(y_i-\\hat y_i)$ gradiyent xatoga proporsional va minimum yonida o‘z-o‘zidan so‘nadi. 4) Chiziqli model uchun MSE — $(X^\\top X)^{-1}X^\\top y$ aniq yechimli kosa; gradiyent tushish $\\eta&lt;2/\\lambda_{\\max}$ da yaqinlashadi, tezlikni shartlanganlik soni belgilaydi. 5) Test MSE = siljish² + tarqoqlik + shovqin. 6) MSE — normal shovqindagi o‘xshashlik; model shartli o‘rtachani baholaydi. 7) Bahosi — chetga chiquvchilarning cheklanmagan ta’siri."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="$y=(1;\\,4;\\,6)$, $\\hat y=(2;\\,4;\\,3)$. MSE nimaga teng?", options=["$3{,}333$", "$1{,}333$", "$1{,}826$", "$10$"], answer=0,
                 explain="Xatolar $(-1;\\,0;\\,3)$, kvadratlar $(1;\\,0;\\,9)$, $\\mathrm{MSE}=10/3\\approx3{,}333$. $1{,}333$ — bu MAE, $1{,}826$ — RMSE, $10$ — $n$ ga bo‘linmagan kvadratlar yig‘indisi."),
            dict(q="$(1;\\,2;\\,3;\\,10;\\,50)$ tanlanma uchun qaysi o‘zgarmas MSE’ni minimallashtiradi?", options=["$3$", "$13{,}2$", "$10$", "$50$"], answer=1,
                 explain="MSE minimumi o‘rtachada: $(1+2+3+10+50)/5=13{,}2$. Mediana $3$ MAE’ni minimallashtiradi."),
            dict(q="$\\partial\\,\\mathrm{MSE}/\\partial\\hat y_i$ nimaga teng?", options=["$-\\frac2n(y_i-\\hat y_i)$", "$-\\frac1n\\operatorname{sign}(y_i-\\hat y_i)$", "$(y_i-\\hat y_i)^2$", "$\\frac2n$"], answer=0,
                 explain="$\\frac{\\partial}{\\partial\\hat y_i}\\frac1n(y_i-\\hat y_i)^2=\\frac1n\\cdot2(y_i-\\hat y_i)\\cdot(-1)$. Ishorali variant — MAE hosilasi, $\\frac2n$ — ikkinchi hosila."),
            dict(q="MSE gessianining xos sonlari $4$ va $2$. Qanday o‘zgarmas $\\eta&gt;0$ qadamlarda gradiyent tushish yaqinlashadi?", options=["$\\eta&lt;0{,}25$", "$\\eta&lt;0{,}5$", "$\\eta&lt;1$", "$\\eta&lt;2$"], answer=1,
                 explain="Barcha xos sonlar uchun $|1-\\eta\\lambda|&lt;1$ sharti $\\eta&lt;2/\\lambda_{\\max}=2/4=0{,}5$ ni beradi. Bu aynan 4-rasmdagi markazlashgan holat."),
            dict(q="Agar shovqin … taqsimlangan bo‘lsa, MSE’ni minimallashtirish maksimal o‘xshashlik usuli bilan mos keladi", options=["Laplas bo‘yicha", "normal", "tekis", "Puasson bo‘yicha"], answer=1,
                 explain="Normal shovqinda $-\\ln L=\\frac n2\\ln(2\\pi\\sigma^2)+\\frac{n}{2\\sigma^2}\\mathrm{MSE}$ — MSE’ning o‘suvchi funksiyasi. Laplas shovqini MAE’ga mos keladi."),
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
