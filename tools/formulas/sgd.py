"""Formula page: SGD → Momentum → RMSProp, the groundwork for Adam. Format: see README.md."""

META = dict(
    id="sgd",
    date="2026-10-28",
    minutes=35,
    hero=r"\theta_t=\theta_{t-1}-\eta\,g_t",
    title={"ru": "SGD, Momentum и RMSProp: как веса спускаются по градиенту",
           "en": "SGD, Momentum and RMSProp: how weights go down the loss surface",
           "uz": "SGD, Momentum va RMSProp: vaznlar gradiyent bo‘ylab qanday tushadi"},
    dek={
        "ru": "Три ступени, из которых собран Adam. Разбираем по косточкам стохастический градиентный спуск, инерцию тяжёлого шарика и деление шага на среднеквадратичный градиент: почему шаг ограничен условием ηL &lt; 2, откуда берётся шум мини-батчей, как инерция ускоряет спуск по оврагу и зачем каждому весу свой масштаб шага.",
        "en": "The three steps Adam is built from. We take apart stochastic gradient descent, heavy-ball momentum and dividing the step by the root-mean-square gradient: why the step is limited by ηL &lt; 2, where mini-batch noise comes from, how momentum speeds up descent along a ravine and why every weight needs its own step scale.",
        "uz": "Adam yig‘ilgan uchta pog‘ona. Stoxastik gradiyentli tushish, og‘ir shar inersiyasi va qadamni gradiyentning o‘rta kvadratik qiymatiga bo‘lishni mayda detallarigacha tahlil qilamiz: nega qadam ηL &lt; 2 sharti bilan cheklangan, mini-batch shovqini qayerdan keladi, inersiya jarlik bo‘ylab tushishni qanday tezlashtiradi va nega har bir vaznga o‘z qadam masshtabi kerak.",
    },
    description={
        "ru": "SGD, Momentum и RMSProp по косточкам: устойчивость ηL < 2, число обусловленности, шум мини-батчей, ускорение √κ, Нестеров, траектории в 3D, код.",
        "en": "SGD, Momentum and RMSProp step by step: stability ηL < 2, the condition number, mini-batch noise, the √κ speed-up, Nesterov, 3D trajectories, code.",
        "uz": "SGD, Momentum va RMSProp batafsil: ηL < 2 barqarorlik, shartlanganlik soni, mini-batch shovqini, √κ tezlashuv, Nesterov, 3D traektoriyalar va kod.",
    },
)

CODE_NUMPY = '''import numpy as np

class SGD:
    """SGD с инерцией (momentum) и вариантом Нестерова — как в torch.optim.SGD."""
    def __init__(self, lr=0.01, momentum=0.0, nesterov=False):
        self.lr, self.beta, self.nesterov, self.u = lr, momentum, nesterov, None

    def step(self, theta, g):
        if self.beta == 0:
            return theta - self.lr * g
        self.u = g.copy() if self.u is None else self.beta * self.u + g
        d = g + self.beta * self.u if self.nesterov else self.u
        return theta - self.lr * d

class RMSProp:
    """RMSProp: свой масштаб шага для каждого веса."""
    def __init__(self, lr=0.01, beta=0.99, eps=1e-8):
        self.lr, self.beta, self.eps, self.v = lr, beta, eps, None

    def step(self, theta, g):
        if self.v is None:
            self.v = np.zeros_like(theta)
        self.v = self.beta * self.v + (1 - self.beta) * g * g
        return theta - self.lr * g / (np.sqrt(self.v) + self.eps)

# Вытянутая долина f = (a² + 100·b²)/2, как на рисунке 6
H = np.diag([1.0, 100.0])
f = lambda th: 0.5 * th @ H @ th
grad = lambda th: H @ th

for name, opt in [("SGD", SGD(lr=0.018)),
                  ("Momentum", SGD(lr=0.018, momentum=0.9)),
                  ("Nesterov", SGD(lr=0.018, momentum=0.9, nesterov=True)),
                  ("RMSProp", RMSProp(lr=0.1, beta=0.9))]:
    th = np.array([-3.4, 0.9])
    for t in range(100):
        th = opt.step(th, grad(th))
    print(f"{name:9s} f = {f(th):.2e}")
# SGD       f = 1.53e-01
# Momentum  f = 2.23e-04
# Nesterov  f = 3.14e+57   ← расходится: ηλ_max = 1.8 > 2(1+β)/(1+2β) ≈ 1.36
# RMSProp   f = 2.60e-02'''

CODE_TORCH = '''import torch
import torch.nn.functional as F

model = torch.nn.Linear(10, 1)

# SGD с инерцией и затуханием весов — классика для свёрточных сетей
opt = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9,
                      nesterov=True, weight_decay=1e-4)
# RMSProp: коэффициент сглаживания в PyTorch называется alpha (по умолчанию 0.99)
# opt = torch.optim.RMSprop(model.parameters(), lr=1e-3, alpha=0.99, eps=1e-8)

for x, y in loader:                  # мини-батчи из DataLoader
    opt.zero_grad()                  # градиенты накапливаются — обнуляем
    loss = F.mse_loss(model(x), y)
    loss.backward()                  # g_t в param.grad
    opt.step()                       # θ ← θ − η·(…)'''


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("SGD с инерцией (momentum) и вариантом Нестерова — как в torch.optim.SGD.", "SGD with momentum and the Nesterov variant, as in torch.optim.SGD."),
               ("RMSProp: свой масштаб шага для каждого веса.", "RMSProp: every weight gets its own step scale."),
               ("Вытянутая долина f = (a² + 100·b²)/2, как на рисунке 6", "An elongated valley f = (a² + 100·b²)/2, as in Figure 6"),
               ("← расходится", "← diverges"),
               ("SGD с инерцией и затуханием весов — классика для свёрточных сетей", "SGD with momentum and weight decay, the classic for convolutional networks"),
               ("RMSProp: коэффициент сглаживания в PyTorch называется alpha (по умолчанию 0.99)", "RMSProp: PyTorch calls the smoothing factor alpha (default 0.99)"),
               ("мини-батчи из DataLoader", "mini-batches from a DataLoader"),
               ("градиенты накапливаются — обнуляем", "gradients accumulate, so reset them"),
               ("g_t в param.grad", "g_t lands in param.grad")],
        "uz": [("SGD с инерцией (momentum) и вариантом Нестерова — как в torch.optim.SGD.", "Inersiyali (momentum) va Nesterov variantli SGD — torch.optim.SGD’dagidek."),
               ("RMSProp: свой масштаб шага для каждого веса.", "RMSProp: har bir vaznning o‘z qadam masshtabi."),
               ("Вытянутая долина f = (a² + 100·b²)/2, как на рисунке 6", "Cho‘ziq vodiy f = (a² + 100·b²)/2, 6-rasmdagidek"),
               ("← расходится", "← uzoqlashadi"),
               ("SGD с инерцией и затуханием весов — классика для свёрточных сетей", "Inersiya va vaznlar so‘nishi bilan SGD — o‘ramli tarmoqlar uchun klassika"),
               ("RMSProp: коэффициент сглаживания в PyTorch называется alpha (по умолчанию 0.99)", "RMSProp: PyTorch’da silliqlash koeffitsiyenti alpha deb ataladi (standart 0.99)"),
               ("мини-батчи из DataLoader", "DataLoader’dan mini-batch’lar"),
               ("градиенты накапливаются — обнуляем", "gradiyentlar to‘planadi — nolga tushiramiz"),
               ("g_t в param.grad", "g_t param.grad ichida")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем это нужно", blocks=[
        ("p", "Обучение нейросети — это поиск минимума функции потерь $L(\\theta)$ по миллионам и миллиардам весов $\\theta$. Готовой формулы для минимума нет: потери зависят от весов слишком сложно. Остаётся идти к минимуму шагами, и единственный ориентир на каждом шаге — градиент $\\nabla L$: вектор, указывающий направление самого быстрого роста потерь. Шагаем в обратную сторону."),
        ("p", "Эта страница — о трёх ступенях одного метода:"),
        ("ul", [
            "<b>SGD</b> (stochastic gradient descent, стохастический градиентный спуск) — шаг против градиента, посчитанного на маленькой случайной пачке примеров, мини-батче;",
            "<b>Momentum</b> (инерция, метод тяжёлого шарика) — шаг против накопленной суммы прошлых градиентов: инерция гасит зигзаги и разгоняет спуск вдоль пологих направлений;",
            "<b>RMSProp</b> — шаг, поделённый на среднеквадратичную величину недавних градиентов: у каждого веса свой масштаб шага.",
        ]),
        ("p", "Сложите вторую и третью ступень, добавьте поправку смещения — получится <a href=\"../adam/\">Adam</a>. А SGD с инерцией по-прежнему обучает многие свёрточные сети для изображений и нередко даёт на них лучшее обобщение, чем адаптивные методы."),
        ("callout", "key", "Главное за минуту", "$\\theta_t=\\theta_{t-1}-\\eta g_t$. Шаг устойчив, только если $\\eta L&lt;2$, где $L$ — наибольшая кривизна потерь. Вытянутая долина (большое число обусловленности $\\kappa$) заставляет SGD ползти; инерция $u_t=\\beta u_{t-1}+g_t$ при удачных $\\eta$ и $\\beta$ сокращает путь примерно с $\\kappa$ до $\\sqrt\\kappa$ шагов; RMSProp делит шаг на $\\sqrt{v_t}$ и выравнивает масштабы разных весов."),
    ]),
    dict(id="intuition", title="Интуиция: шаг под гору", blocks=[
        ("p", "Представьте, что вы спускаетесь с холма в густом тумане. Видно только склон под ногами: куда и насколько круто он идёт вниз. Разумная стратегия — шагнуть в сторону самого крутого спуска, осмотреться и повторить. Длина шага задаётся <b>темпом обучения</b> (learning rate) $\\eta$."),
        ("p", "Короткие шаги надёжны, но медленны. Слишком длинный шаг перепрыгивает дно ямы и попадает на противоположный склон — и если там он выше, следующий шаг унесёт ещё дальше. Посмотрите, как это выглядит на простейшей потере $f(\\theta)=L\\theta^2/2$: её градиент $f'(\\theta)=L\\theta$, а кривизна (вторая производная) равна $L$."),
        ("viz", "sgd-parabola", {"eta": 0.3, "L": 2, "x0": 2}, "<b>Рисунок 1.</b> Градиентный спуск на параболе. Вверху — шаги по кривой (стартовую точку $\\theta_0$ можно тянуть), внизу — расстояние до минимума $|\\theta_t|$ в логарифмической шкале. При $L=2$ и $\\eta=0{,}3$ каждый шаг умножает $\\theta$ на $1-\\eta L=0{,}4$, и из $\\theta_0=2$ до $|\\theta|&lt;0{,}01$ нужно 6 шагов. Увеличивайте $\\eta$: при $0{,}5$ минимум достигается за один шаг, при $0{,}6$ точка прыгает через минимум, а при $\\eta&gt;1$ спуск расходится."),
        ("callout", "intuition", "Что заметить", "Всё решает одно число $\\eta L$. При $\\eta L&lt;1$ спуск монотонный, при $1&lt;\\eta L&lt;2$ точка прыгает через минимум, но приближается к нему, при $\\eta L&gt;2$ улетает. Шаг $\\eta=1/L$ попадает в минимум сразу — но только пока кривизна одна во всех направлениях."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("eq", r"\theta_t=\theta_{t-1}-\eta\,g_t,\qquad g_t=\frac1B\sum_{i\in B_t}\nabla_\theta\,\ell(x_i,y_i;\,\theta_{t-1})"),
        ("symbols", [
            (r"\theta_{t-1}", "текущие веса — вектор всех параметров модели;"),
            (r"g_t", "стохастический градиент: среднее градиентов потерь $\\ell$ по мини-батчу $B_t$ из $B$ случайных примеров;"),
            (r"\eta", "темп обучения, положительное число, обычно от $10^{-4}$ до $10^{-1}$;"),
            (r"-\eta\,g_t", "шаг: против градиента, длиной $\\eta\\|g_t\\|$ — тем длиннее, чем круче склон."),
        ]),
        ("p", "Почему это работает. Разложим потери в ряд Тейлора около текущей точки: $L(\\theta-\\eta g)\\approx L(\\theta)-\\eta\\,\\|g\\|^2$. Пока шаг мал, потери уменьшаются примерно на $\\eta\\|g\\|^2$, и это самое быстрое убывание среди шагов той же длины: скалярное произведение $\\langle\\nabla L,\\,d\\rangle$ при фиксированной длине $\\|d\\|$ минимально, когда $d$ направлен против градиента."),
        ("callout", "note", "Пример на числах", "$f(\\theta)=\\theta^2$, $\\theta_0=3$, $\\eta=0{,}1$. Градиент $g_1=2\\cdot3=6$, шаг $-0{,}1\\cdot6=-0{,}6$, новое значение $\\theta_1=2{,}4$, потери падают с $9$ до $5{,}76$. Каждый следующий шаг снова умножает $\\theta$ на $1-2\\eta=0{,}8$."),
        ("deep", "Насколько большим может быть шаг: лемма о спуске", [
            ("p", "Пусть градиент $f$ липшицев с константой $L$: $\\|\\nabla f(a)-\\nabla f(b)\\|\\le L\\|a-b\\|$ (для дважды дифференцируемой $f$ это значит, что собственные значения гессиана по модулю не больше $L$). Тогда $f$ лежит под параболой, касающейся её в текущей точке, и для шага $\\theta-\\eta g$ с $g=\\nabla f(\\theta)$:"),
            ("eq", r"f(\theta-\eta g)\le f(\theta)-\eta\Bigl(1-\frac{L\eta}{2}\Bigr)\|g\|^2"),
            ("p", "Множитель $1-L\\eta/2$ положителен при $\\eta&lt;2/L$ — это та самая граница устойчивости с рисунка 1. Гарантированное убывание максимально при $\\eta=1/L$: тогда $f$ уменьшается хотя бы на $\\|g\\|^2/(2L)$."),
            ("p", "Для квадратичной функции $f=\\tfrac12\\theta^\\top H\\theta$ шаг — линейное отображение $\\theta_t=(I-\\eta H)\\,\\theta_{t-1}$. В собственном базисе $H$ каждая координата умножается на $1-\\eta\\lambda_i$, и спуск сходится тогда и только тогда, когда $|1-\\eta\\lambda_i|&lt;1$ для всех $i$, то есть $0&lt;\\eta&lt;2/\\lambda_{\\max}$ (при положительно определённой $H$)."),
        ]),
        ("h3", "Число обусловленности: почему спуск бывает медленным"),
        ("p", "Если кривизны по разным направлениям различаются, шаг обязан подстроиться под самую крутую: $\\eta&lt;2/\\lambda_{\\max}$. Тогда вдоль самого пологого направления координата за шаг уменьшается лишь на долю $\\eta\\lambda_{\\min}&lt;2/\\kappa$, где $\\kappa=\\lambda_{\\max}/\\lambda_{\\min}$ — <b>число обусловленности</b> (condition number). Даже при лучшем постоянном шаге $\\eta=2/(\\lambda_{\\max}+\\lambda_{\\min})$ ошибка за шаг уменьшается лишь в $(\\kappa-1)/(\\kappa+1)$ раз:"),
        ("eq", r"\|\theta_t-\theta^*\|\le\Bigl(\frac{\kappa-1}{\kappa+1}\Bigr)^{t}\,\|\theta_0-\theta^*\|"),
        ("p", "При $\\kappa=100$ множитель равен $0{,}980$, и чтобы уменьшить ошибку в тысячу раз, нужно около 345 шагов. Грубое правило: SGD тратит порядка $\\kappa$ шагов на каждый порядок точности."),
        ("table", ["Метод", "Шаг", "Что хранит", "Гиперпараметры"], [
            ["SGD", "$\\theta_t=\\theta_{t-1}-\\eta g_t$", "ничего", "$\\eta$"],
            ["Momentum", "$u_t=\\beta u_{t-1}+g_t$,<br>$\\theta_t=\\theta_{t-1}-\\eta u_t$", "$u$: одно число на вес", "$\\eta$, $\\beta\\approx0{,}9$"],
            ["RMSProp", "$v_t=\\beta v_{t-1}+(1-\\beta)g_t^2$,<br>$\\theta_t=\\theta_{t-1}-\\eta\\,\\dfrac{g_t}{\\sqrt{v_t}+\\epsilon}$", "$v$: одно число на вес", "$\\eta$, $\\beta=0{,}9$–$0{,}99$, $\\epsilon$"],
        ], {}),
    ]),
    dict(id="noise", title="Стохастичность: мини-батчи и шум", blocks=[
        ("p", "Полный градиент — среднее по всем $N$ примерам обучающей выборки. При миллионах примеров один такой шаг стоил бы прохода по всем данным. SGD берёт случайный мини-батч из $B$ примеров. Его градиент — <b>несмещённая</b> оценка полного: в среднем совпадает с $\\nabla L$, но каждый раз отклоняется на случайный шум."),
        ("eq", r"\mathbb E\,[g_t]=\nabla L(\theta),\qquad \operatorname{Cov}[g_t]=\frac{\Sigma}{B}\cdot\frac{N-B}{N-1}"),
        ("symbols", [
            (r"\Sigma", "ковариация градиентов отдельных примеров в текущей точке (с делением на $N$);"),
            (r"\frac{N-B}{N-1}", "поправка за выбор без возвращения: при $B=N$ шум исчезает."),
        ]),
        ("p", "Дисперсия шума падает как $1/B$, а цена шага растёт как $B$. Поэтому за одну эпоху (один проход по данным) маленькие батчи делают много неточных шагов, а большие — мало точных. На рисунке — линейная регрессия $y\\approx wx+b$ на 200 точках с потерей $L=\\frac1{2N}\\sum(wx_i+b-y_i)^2$: это квадратичная «миска» над плоскостью весов $(w;\\,b)$."),
        ("viz", "sgd-minibatch", {"B": 10, "eta": 0.05}, "<b>Рисунок 2.</b> Слева — путь SGD по линиям уровня потерь; оранжевые точки — куда попал бы следующий шаг при 40 разных случайных батчах, стрелка — шаг по полному градиенту. Справа — превышение потерь над минимумом $L-L^*$ по эпохам. За 8 эпох с $\\eta=0{,}05$ из начальных $5{,}84$: батч 1 доходит до $1{,}4\\cdot10^{-3}$, батч 10 — до $0{,}044$, батч 50 — до $1{,}06$, а полный градиент (всего 8 шагов) — до $2{,}0$. Нажмите «Пуск» и сравните облака: у $B=1$ оно широкое даже у самого минимума."),
        ("callout", "intuition", "Шум — не только помеха", "У минимума полный градиент равен нулю, а стохастический — нет. При постоянном $\\eta$ SGD не останавливается, а дрожит в облаке, размер которого растёт как $\\sqrt\\eta$; поэтому к концу обучения темп снижают. Зато тот же шум помогает уходить с седловых точек и из узких минимумов; есть наблюдения, что он смещает обучение к более пологим минимумам, которые лучше обобщают."),
        ("deep", "Правило линейного масштабирования батча", [
            ("p", "Если увеличить батч в $k$ раз, дисперсия шума падает в $k$ раз, но шагов за эпоху становится в $k$ раз меньше. Гоял и соавторы (2017) предложили одновременно увеличивать $\\eta$ в $k$ раз: так ResNet-50 обучили на ImageNet с батчем 8192 за час без потери точности. Правило работает до некоторого «критического» размера батча и требует разогрева (warmup) — плавного роста $\\eta$ на первых эпохах."),
        ]),
    ]),
    dict(id="momentum", title="Momentum: инерция тяжёлого шарика", blocks=[
        ("p", "Градиентный спуск — это точка без массы: в каждый момент она идёт ровно туда, куда показывает склон. Б. Т. Поляк (1964) предложил дать ей массу. Тяжёлый шарик катится, накапливая скорость, и не реагирует на каждую кочку. В формуле скорость — вектор $u$:"),
        ("eq", r"u_t=\beta\,u_{t-1}+g_t,\qquad \theta_t=\theta_{t-1}-\eta\,u_t"),
        ("symbols", [
            (r"u_t", "накопленное направление (буфер инерции), $u_0=0$;"),
            (r"\beta", "коэффициент инерции, $0\\le\\beta&lt;1$, обычно $0{,}9$; при $\\beta=0$ — обычный SGD."),
        ]),
        ("p", "Раскроем рекурсию: $u_t=g_t+\\beta g_{t-1}+\\beta^2 g_{t-2}+\\dots$ — взвешенная сумма всех прошлых градиентов с экспоненциально убывающими весами. Если градиенты из шага в шаг указывают в одну сторону, они складываются, и шаг растёт до $\\eta/(1-\\beta)$ — в 10 раз при $\\beta=0{,}9$. Если знак скачет (зигзаг поперёк оврага), слагаемые гасят друг друга."),
        ("viz", "sgd-ema", {"beta": 0.9}, "<b>Рисунок 3.</b> Слева — вес, с которым градиент $k$-шаговой давности входит в $u_t$; яркие столбики — самые свежие градиенты, вместе дающие не меньше половины общего веса. Справа — ответ $u_t$ на постоянный градиент $g=1$: он растёт к $1/(1-\\beta)=10$ и к 22-му шагу набирает $90\\%$ предела. При $\\beta=0{,}9$ половина веса набирается на последних 7 градиентах, при $\\beta=0{,}99$ — на последних 69, а окно памяти — 100 шагов."),
        ("callout", "note", "Две записи одной инерции", "PyTorch пишет $u_t=\\beta u_{t-1}+g_t$, как здесь. Часто встречается и экспоненциальное скользящее среднее (exponential moving average, EMA) $m_t=\\beta m_{t-1}+(1-\\beta)g_t$: оно отличается постоянным множителем $1-\\beta$, который переходит в $\\eta$. Именно EMA стоит в числителе <a href=\"../adam/\">Adam</a>. Переключите форму на рисунке: EMA стартует с $0{,}1$ вместо 1 и лишь постепенно доходит до истинного значения — эта недооценка на первых шагах и есть причина поправки смещения в Adam."),
        ("h3", "Почему инерция ускоряет: теория на квадратичной функции"),
        ("p", "Возьмём одно направление с кривизной $L$ и обозначим $h=\\eta L$. Подставим $g_t=L\\theta_{t-1}$ и исключим $u$ (из второй формулы $\\eta u_{t-1}=\\theta_{t-2}-\\theta_{t-1}$). Получится линейная рекуррентность второго порядка:"),
        ("eq", r"\theta_t=(1+\beta-h)\,\theta_{t-1}-\beta\,\theta_{t-2}"),
        ("p", "Её поведение определяют корни характеристического уравнения $\\lambda^2-(1+\\beta-h)\\lambda+\\beta=0$. Скорость сходимости — наибольший модуль корня $\\rho$: ошибка убывает примерно как $\\rho^t$."),
        ("viz", "sgd-momentum", {"h": 0.04, "beta": 0.9}, "<b>Рисунок 4.</b> Слева — карта скорости $\\rho$ по $\\eta L$ (логарифмическая шкала) и $\\beta$: синее — быстрая сходимость, красное — расходимость, сплошная линия — граница $\\rho=1$, штриховые — критическое затухание. Тяните синюю точку. Справа — $\\theta_t$ для SGD с тем же $\\eta$ и с инерцией. При $\\eta L=0{,}04$ SGD нужно 170 шагов до $|\\theta|&lt;10^{-3}$ ($\\rho=0{,}96$), инерции $\\beta=0{,}9$ — 130 шагов с колебаниями, Нестерову с той же $\\beta$ — 87, а критическое затухание $\\beta=(1-\\sqrt{0{,}04})^2=0{,}64$ даёт 41 шаг ($\\rho=0{,}8$)."),
        ("deep", "Вывод: область устойчивости и оптимальная инерция", [
            ("p", "Корни комплексные, когда $(1+\\beta-h)^2&lt;4\\beta$, то есть при $(1-\\sqrt\\beta)^2&lt;h&lt;(1+\\sqrt\\beta)^2$. Произведение корней равно $\\beta$, поэтому $|\\lambda_1|=|\\lambda_2|=\\sqrt\\beta$: $\\theta_t$ колеблется и затухает в $\\sqrt\\beta$ раз за шаг, независимо от $h$. Вне этой полосы корни вещественные. Вместе оба случая дают точную область устойчивости (условия Шура — Кона для квадратного трёхчлена):"),
            ("eq", r"0<\eta L<2(1+\beta)"),
            ("p", "— инерция почти вдвое расширяет допустимый шаг (у SGD $\\eta L&lt;2$)."),
            ("p", "Пусть кривизны заполняют отрезок $[\\mu;\\,L]$, $\\kappa=L/\\mu$. Подберём $\\eta$ и $\\beta$ так, чтобы оба края попали на границы комплексной полосы: $(1-\\sqrt\\beta)^2=\\eta\\mu$ и $(1+\\sqrt\\beta)^2=\\eta L$. Тогда все направления затухают одинаково быстро:"),
            ("eq", r"\eta=\frac{4}{(\sqrt L+\sqrt\mu)^2},\qquad \beta=\Bigl(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\Bigr)^2,\qquad \rho=\sqrt\beta=\frac{\sqrt\kappa-1}{\sqrt\kappa+1}"),
            ("p", "Сравните с лучшим SGD, $\\rho=(\\kappa-1)/(\\kappa+1)$. При $\\kappa=100$ это $0{,}818$ против $0{,}980$: около 35 шагов вместо 345, чтобы уменьшить ошибку в тысячу раз. Число шагов растёт как $\\sqrt\\kappa$, а не как $\\kappa$ — в этом и состоит ускорение тяжёлого шарика."),
        ]),
        ("h3", "Нестеров: градиент там, куда несёт инерция"),
        ("p", "Ю. Е. Нестеров (1983) предложил считать градиент не в текущей точке, а там, куда шарик всё равно унесёт инерция. В форме PyTorch (<code>nesterov=True</code>) это поправка к шагу:"),
        ("eq", r"u_t=\beta u_{t-1}+g_t,\qquad \theta_t=\theta_{t-1}-\eta\,(g_t+\beta u_t)"),
        ("p", "Характеристическое уравнение становится $\\lambda^2-(1+\\beta)(1-h)\\lambda+\\beta(1-h)=0$. На пологих направлениях колебания затухают быстрее ($\\rho=\\sqrt{\\beta(1-h)}$ вместо $\\sqrt\\beta$), но область устойчивости уже: $\\eta L&lt;2(1+\\beta)/(1+2\\beta)$, при $\\beta=0{,}9$ — всего $1{,}36$. Переключите рисунок 4 на «Нестеров», чтобы увидеть обе особенности."),
    ]),
    dict(id="rmsprop", title="RMSProp: свой шаг для каждого веса", blocks=[
        ("p", "У SGD и Momentum один темп $\\eta$ на все веса. Но градиенты разных весов могут отличаться на порядки: эмбеддинги редких слов получают редкие крупные толчки, смещения последнего слоя — постоянные мелкие. Общий $\\eta$ для одних слишком велик, для других слишком мал. RMSProp (Дж. Хинтон, лекции курса на Coursera, 2012) делит шаг каждого веса на его типичный размер градиента:"),
        ("eq", r"v_t=\beta\,v_{t-1}+(1-\beta)\,g_t^2,\qquad\theta_t=\theta_{t-1}-\eta\,\frac{g_t}{\sqrt{v_t}+\epsilon}"),
        ("symbols", [
            (r"g_t^2", "поэлементный квадрат: у каждого веса свой $v$;"),
            (r"v_t", "экспоненциальное скользящее среднее квадрата градиента — оценка $\\mathbb E[g^2]$ за последние $\\sim1/(1-\\beta)$ шагов, $v_0=0$;"),
            (r"\sqrt{v_t}", "среднеквадратичное значение (root mean square, RMS) градиента — отсюда название;"),
            (r"\epsilon", "маленькая добавка ($10^{-8}$) против деления на ноль."),
        ]),
        ("p", "Деление на $\\sqrt{v_t}$ делает шаг безразмерным: если умножить все градиенты веса на 1000, то и $\\sqrt v$ вырастет в 1000 раз, а шаг не изменится. Типичный шаг становится порядка $\\eta$ — темп теперь задаёт длину шага прямо в единицах весов."),
        ("viz", "sgd-rmsprop", {"beta": 0.9}, "<b>Рисунок 5.</b> Градиент одного веса, масштаб которого меняется: на шаге 100 он вырастает в 10 раз, на шаге 200 падает в 100 раз. Вверху — $|g_t|$ и $\\sqrt{v_t}$, внизу — длина шага. Шаг SGD прыгает вместе с градиентом на два порядка, шаг RMSProp остаётся порядка $\\eta=0{,}01$. Но у адаптации есть запаздывание: после роста шаг кратко подскакивает (при $\\beta=0{,}9$ до $0{,}030$ при границе $0{,}032$), а после падения проваливается — старому большому $v$ нужно около $\\ln10^4/\\ln(1/0{,}9)\\approx87$ шагов, чтобы забыться."),
        ("callout", "key", "Встроенная граница шага", "Из $v_t\\ge(1-\\beta)g_t^2$ следует $|g_t|/\\sqrt{v_t}\\le1/\\sqrt{1-\\beta}$. Шаг RMSProp никогда не превышает $\\eta/\\sqrt{1-\\beta}$: $3{,}16\\,\\eta$ при $\\beta=0{,}9$ и $10\\,\\eta$ при $\\beta=0{,}99$. Это защита от взрыва градиента, которой у SGD нет."),
        ("deep", "Откуда RMSProp: AdaGrad и Rprop", [
            ("p", "Предшественник — AdaGrad (Дучи, Хазан, Сингер, 2011): $v_t=v_{t-1}+g_t^2$, сумма вместо среднего. Для выпуклых задач с редкими признаками он хорош, но в нейросетях $v$ только растёт, и шаг $\\eta/\\sqrt{v_t}$ неизбежно затухает до нуля. RMSProp заменил сумму экспоненциальным средним с конечной памятью."),
            ("p", "Другой корень — Rprop (Ридмиллер и Браун, 1993), который использует только знак градиента. RMSProp можно читать как его вариант для мини-батчей: при $\\beta=0$ получается $v_t=g_t^2$ и шаг $\\eta\\operatorname{sign}(g_t)$."),
            ("p", "Важно: RMSProp масштабирует оси координат, но не поворачивает их. Это <b>диагональное</b> предобусловливание. Если овраг идёт по диагонали между весами, деление на $\\sqrt v$ помогает слабо — это видно на рисунке 6 при повороте на 45°."),
        ]),
    ]),
    dict(id="landscape", title="Траектории в 2D и 3D", blocks=[
        ("p", "Сравним три метода на одной задаче — вытянутой квадратичной долине $f=\\tfrac12(a^2+\\kappa b^2)$, где $a$ и $b$ — координаты вдоль и поперёк оврага: кривизна поперёк в $\\kappa$ раз больше, чем вдоль. Старт — в точке $a=-3{,}4$, $b=0{,}9$, где $f=46{,}3$."),
        ("viz", "sgd-ravine", {"kappa": 100, "eta": 0.018, "beta": 0.9}, "<b>Рисунок 6.</b> Овраг с $\\kappa=100$: вид сверху и поверхность в 3D (её можно вращать). При $\\eta=0{,}018$ SGD прыгает поперёк оврага ($\\eta\\lambda_{\\max}=1{,}8$) и медленно ползёт вдоль него: за 100 шагов $f$ падает лишь до $0{,}15$. Momentum с $\\beta=0{,}9$ доходит до $2{,}2\\cdot10^{-4}$, RMSProp с $\\eta=0{,}1$ — до $0{,}026$: он быстро спускается на дно, но дальше дрожит с шагом порядка $\\eta$. Поверните овраг на 45°: SGD и Momentum разницы не заметят, а RMSProp потеряет преимущество — $0{,}30$ вместо $0{,}026$."),
        ("p", "Вторая классика — функция Розенброка $f=(1-x)^2+100(y-x^2)^2$: узкий изогнутый «банан» с минимумом в $(1;\\,1)$. Кривизна здесь меняется от точки к точке, и никакой постоянный шаг не идеален."),
        ("viz", "sgd-rosenbrock", {}, "<b>Рисунок 7.</b> 3000 шагов из точки $(-1{,}5;\\,2)$ — её можно перетаскивать. SGD с $\\eta=0{,}001$ доходит лишь до $f=0{,}049$. Momentum с тем же $\\eta$ и $\\beta=0{,}9$ проходит банан: $f&lt;10^{-3}$ на 666-м шаге и $3\\cdot10^{-12}$ к концу. RMSProp с $\\eta=0{,}01$ застревает около $f\\approx0{,}02$: его шаг почти не уменьшается у дна. Ползунок $t$ показывает положение всех трёх в любой момент."),
        ("callout", "warn", "Карта — не территория", "Двумерные картинки полезны, но обманчивы: у настоящей сети миллионы измерений, большинство критических точек там — седловые, а не локальные минимумы, и поверхность потерь сама зависит от мини-батча. Используйте рисунки для интуиции о механизмах (зигзаг, инерция, масштаб), а не для выбора оптимизатора."),
    ]),
    dict(id="code", title="В коде: с нуля и в PyTorch", blocks=[
        ("p", "Все три метода помещаются в два маленьких класса. Обратите внимание: состояние ($u$ или $v$) — массив того же размера, что и веса, поэтому Momentum и RMSProp удваивают память под параметры, а Adam — утраивает."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "Числа в комментариях совпадают с рисунком 6, а <code>torch.optim.SGD</code> и <code>torch.optim.RMSprop</code> на той же задаче дают те же значения. Нестеров с тем же $\\eta$ расходится — ровно по условию устойчивости из раздела про инерцию."),
        ("code", "python", "CODE_TORCH"),
        ("callout", "note", "Две формы инерции в библиотеках", "PyTorch хранит сумму сырых градиентов и умножает её на текущий $\\eta$: $\\theta\\leftarrow\\theta-\\eta_t u_t$. Keras и классическая статья Сутскевера и др. (2013) хранят уже умноженную на темп скорость: $v_t=\\beta v_{t-1}-\\eta_t g_t$, $\\theta\\leftarrow\\theta+v_t$. При постоянном $\\eta$ формы эквивалентны, при расписании — нет: в PyTorch новый $\\eta$ сразу применяется ко всему накопленному буферу."),
    ]),
    dict(id="practice", title="Гиперпараметры и практика", blocks=[
        ("table", ["Параметр", "Типичные значения", "Как выбирать"], [
            ["$\\eta$ (SGD с инерцией)", "$0{,}01$–$0{,}1$", "наибольший, при котором потери ещё стабильно падают; ResNet: $0{,}1$ при батче 256"],
            ["$\\beta$ (momentum)", "$0{,}9$, реже $0{,}95$–$0{,}99$", "больше $\\beta$ — длиннее память и сильнее разгон, но выше риск раскачки"],
            ["$\\beta$ RMSProp (alpha)", "$0{,}9$–$0{,}99$", "окно усреднения $1/(1-\\beta)$: от 10 до 100 шагов"],
            ["$\\eta$ (RMSProp)", "$10^{-4}$–$10^{-3}$", "шаг порядка $\\eta$ в единицах весов"],
            ["$B$ (батч)", "32–512", "при росте $B$ в $k$ раз — $\\eta$ в $k$ раз, с разогревом"],
            ["weight decay", "$10^{-4}$–$5\\cdot10^{-4}$", "затухание весов; для SGD совпадает с $L_2$-регуляризацией"],
        ], {}),
        ("ul", [
            "<b>Расписание темпа.</b> Ступенчатое (умножение на $0{,}1$ на 30-й и 60-й эпохах из 90 — классика ResNet), косинусное или «один цикл». Постоянный $\\eta$ оставляет шумовое облако у минимума.",
            "<b>Разогрев (warmup).</b> Первые сотни–тысячи шагов $\\eta$ растёт линейно от малого значения — особенно важно при большом батче.",
            "<b>Обрезка градиента</b> (gradient clipping) по норме защищает от редких огромных градиентов в RNN и трансформерах.",
            "<b>Поиск темпа</b> (LR range test, Л. Смит): короткая прогонка с экспоненциально растущим $\\eta$; берут значение заметно меньше того, где потери начинают расти.",
            "<b>Нормализация</b> входов, батч-нормализация и разумная инициализация уменьшают число обусловленности и позволяют брать больший $\\eta$.",
        ]),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>Забытый <code>zero_grad()</code>.</b> В PyTorch градиенты накапливаются в <code>.grad</code>; без обнуления $g_t$ превращается в сумму всех прошлых градиентов — это не инерция, а ошибка.",
            "<b>Слишком большой темп</b>: потери растут или становятся NaN. По рисунку 1 нужно $\\eta&lt;2/\\lambda_{\\max}$; первым делом уменьшите $\\eta$ в 3–10 раз.",
            "<b>Перенос $\\eta$ между оптимизаторами.</b> С инерцией $\\beta=0{,}9$ установившийся шаг в 10 раз больше, чем у SGD с тем же $\\eta$. У RMSProp и Adam $\\eta$ вообще в других единицах: $10^{-3}$ для них нормально, для SGD обычно мало.",
            "<b>Смена батча без смены темпа.</b> Увеличили $B$ в 8 раз и оставили $\\eta$ — сеть учится медленнее за эпоху; уменьшили $B$ — шум может раскачать обучение.",
            "<b>$\\epsilon=10^{-8}$ в низкой точности.</b> В float16 это число округляется до нуля, и при $v\\approx0$ шаг RMSProp взрывается; в смешанной точности $v$ держат в float32 или берут $\\epsilon$ больше.",
            "<b>Постоянный темп до конца обучения.</b> Без снижения $\\eta$ SGD дрожит у минимума, и последние эпохи почти ничего не дают.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../adam/\">Adam</a>: числитель — EMA-инерция, знаменатель — $\\sqrt{v}$ из RMSProp, плюс поправка смещения.",
            "<a href=\"../mse/\">MSE</a>: её градиент $\\frac2n\\sum_i(\\hat y_i-y_i)\\,x_i$ — с точностью до множителя 2 тот же $g_t$, что в линейной регрессии на рисунке 2 (там потеря — половина MSE).",
            "<a href=\"../bce/\">BCE</a> и <a href=\"../cross-entropy/\">кросс-энтропия</a>: градиент по логитам $\\hat y-y$ — простейший сигнал для спуска.",
            "<a href=\"../sigmoid/\">Сигмоида</a>: насыщение даёт крошечные градиенты — SGD на них почти стоит, а RMSProp растягивает шаг.",
            "<a href=\"../huber/\">Huber</a>: ограничивает градиент выбросов — родственник обрезки градиента.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) SGD: $\\theta_t=\\theta_{t-1}-\\eta g_t$, где $g_t$ — несмещённая оценка градиента по мини-батчу; дисперсия шума падает как $1/B$. 2) Устойчивость: $\\eta&lt;2/\\lambda_{\\max}$; скорость задаёт число обусловленности $\\kappa$ — порядка $\\kappa$ шагов на порядок точности. 3) Momentum $u_t=\\beta u_{t-1}+g_t$ — экспоненциальная память о градиентах с окном $1/(1-\\beta)$; на квадратичных задачах сокращает путь до порядка $\\sqrt\\kappa$ шагов и расширяет устойчивость до $\\eta L&lt;2(1+\\beta)$. 4) RMSProp делит шаг на $\\sqrt{v_t}$: шаг безразмерный, порядка $\\eta$, но адаптация только диагональная. 5) EMA-инерция + RMSProp + поправка смещения = Adam."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="$f(\\theta)=5\\theta^2$. При каких постоянных $\\eta$ градиентный спуск сходится?", options=["$\\eta&lt;0{,}1$", "$\\eta&lt;0{,}2$", "$\\eta&lt;0{,}4$", "$\\eta&lt;2$"], answer=1,
                 explain="Кривизна $f''=10$, условие $\\eta L&lt;2$ даёт $\\eta&lt;0{,}2$. При $\\eta=0{,}1$ минимум достигается за один шаг."),
            dict(q="Каково окно памяти инерции при $\\beta=0{,}95$?", options=["5 шагов", "20 шагов", "95 шагов", "$0{,}05$ шага"], answer=1,
                 explain="$1/(1-\\beta)=1/0{,}05=20$."),
            dict(q="Батч увеличили с 32 до 128 (данных намного больше, чем $B$). Что станет с дисперсией стохастического градиента?", options=["Вырастет в 4 раза", "Упадёт в 2 раза", "Упадёт в 4 раза", "Не изменится"], answer=2,
                 explain="$\\operatorname{Cov}[g]\\approx\\Sigma/B$: батч вырос в 4 раза — дисперсия упала в 4 раза (а стандартное отклонение — в 2)."),
            dict(q="Все градиенты одного веса умножили на 100. Как изменится шаг RMSProp, когда $v$ установится (без учёта $\\epsilon$)?", options=["Вырастет в 100 раз", "Вырастет в 10 раз", "Не изменится", "Уменьшится в 100 раз"], answer=2,
                 explain="$\\sqrt v$ тоже вырастет в 100 раз, и отношение $g/\\sqrt v$ останется прежним."),
            dict(q="Почему инерция ускоряет спуск по вытянутому оврагу?", options=["Вдоль оврага градиенты согласованы и складываются, а поперёк знак чередуется и они гасят друг друга", "Она уменьшает кривизну функции", "Она вычисляет вторые производные", "Она делит шаг на $\\sqrt v$"], answer=0,
                 explain="$u_t$ — сумма прошлых градиентов с весами $\\beta^k$: согласованные компоненты растут до $1/(1-\\beta)$, чередующиеся — сокращаются."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "Training a neural network means searching for the minimum of a loss function $L(\\theta)$ over millions or billions of weights $\\theta$. There is no closed-form formula for the minimum: the loss depends on the weights in too complicated a way. All we can do is walk towards the minimum step by step, and the only guide at every step is the gradient $\\nabla L$, the vector pointing in the direction of the fastest growth of the loss. We step the opposite way."),
        ("p", "This page is about three steps of one method:"),
        ("ul", [
            "<b>SGD</b> (stochastic gradient descent) — a step against the gradient computed on a small random batch of examples, a mini-batch;",
            "<b>Momentum</b> (the heavy-ball method) — a step against the accumulated sum of past gradients: inertia damps zigzags and speeds up descent along gentle directions;",
            "<b>RMSProp</b> — a step divided by the root-mean-square size of recent gradients: every weight gets its own step scale.",
        ]),
        ("p", "Combine the second and third steps, add bias correction, and you get <a href=\"../adam/\">Adam</a>. And SGD with momentum still trains many convolutional networks for images, often generalizing better on them than adaptive methods."),
        ("callout", "key", "The essentials in a minute", "$\\theta_t=\\theta_{t-1}-\\eta g_t$. The step is stable only if $\\eta L&lt;2$, where $L$ is the largest curvature of the loss. An elongated valley (a large condition number $\\kappa$) makes SGD crawl; momentum $u_t=\\beta u_{t-1}+g_t$ with well-chosen $\\eta$ and $\\beta$ cuts the journey from about $\\kappa$ to about $\\sqrt\\kappa$ steps; RMSProp divides the step by $\\sqrt{v_t}$ and evens out the scales of different weights."),
    ]),
    dict(id="intuition", title="Intuition: a step downhill", blocks=[
        ("p", "Imagine walking down a hill in thick fog. All you can see is the slope under your feet: which way and how steeply it goes down. A sensible strategy is to step in the direction of the steepest descent, look around and repeat. The length of the step is set by the <b>learning rate</b> $\\eta$."),
        ("p", "Short steps are safe but slow. A step that is too long jumps over the bottom of the pit onto the opposite slope — and if it lands higher there, the next step throws it even further. See how this looks on the simplest loss $f(\\theta)=L\\theta^2/2$: its gradient is $f'(\\theta)=L\\theta$ and its curvature (second derivative) is $L$."),
        ("viz", "sgd-parabola", {"eta": 0.3, "L": 2, "x0": 2}, "<b>Figure 1.</b> Gradient descent on a parabola. Top: the steps along the curve (you can drag the starting point $\\theta_0$); bottom: the distance to the minimum $|\\theta_t|$ on a log scale. With $L=2$ and $\\eta=0.3$ every step multiplies $\\theta$ by $1-\\eta L=0.4$, and from $\\theta_0=2$ it takes 6 steps to reach $|\\theta|&lt;0.01$. Increase $\\eta$: at $0.5$ the minimum is reached in one step, at $0.6$ the point jumps over the minimum, and for $\\eta&gt;1$ descent diverges."),
        ("callout", "intuition", "What to notice", "One number decides everything: $\\eta L$. For $\\eta L&lt;1$ descent is monotone, for $1&lt;\\eta L&lt;2$ the point jumps over the minimum but still approaches it, for $\\eta L&gt;2$ it flies off. The step $\\eta=1/L$ hits the minimum at once — but only while the curvature is the same in every direction."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("eq", r"\theta_t=\theta_{t-1}-\eta\,g_t,\qquad g_t=\frac1B\sum_{i\in B_t}\nabla_\theta\,\ell(x_i,y_i;\,\theta_{t-1})"),
        ("symbols", [
            (r"\theta_{t-1}", "the current weights, the vector of all model parameters;"),
            (r"g_t", "the stochastic gradient: the mean of the loss gradients $\\ell$ over a mini-batch $B_t$ of $B$ random examples;"),
            (r"\eta", "the learning rate, a positive number, usually between $10^{-4}$ and $10^{-1}$;"),
            (r"-\eta\,g_t", "the step: against the gradient, of length $\\eta\\|g_t\\|$ — the steeper the slope, the longer the step."),
        ]),
        ("p", "Why it works. Expand the loss in a Taylor series around the current point: $L(\\theta-\\eta g)\\approx L(\\theta)-\\eta\\,\\|g\\|^2$. While the step is small the loss drops by about $\\eta\\|g\\|^2$, and this is the fastest decrease among all steps of the same length: the dot product $\\langle\\nabla L,\\,d\\rangle$ for a fixed length $\\|d\\|$ is smallest when $d$ points against the gradient."),
        ("callout", "note", "A worked example", "$f(\\theta)=\\theta^2$, $\\theta_0=3$, $\\eta=0.1$. The gradient is $g_1=2\\cdot3=6$, the step is $-0.1\\cdot6=-0.6$, the new value is $\\theta_1=2.4$, and the loss drops from $9$ to $5.76$. Every further step again multiplies $\\theta$ by $1-2\\eta=0.8$."),
        ("deep", "How large can the step be: the descent lemma", [
            ("p", "Let the gradient of $f$ be Lipschitz with constant $L$: $\\|\\nabla f(a)-\\nabla f(b)\\|\\le L\\|a-b\\|$ (for a twice-differentiable $f$ this means the eigenvalues of the Hessian are at most $L$ in absolute value). Then $f$ lies below the parabola touching it at the current point, and for the step $\\theta-\\eta g$ with $g=\\nabla f(\\theta)$:"),
            ("eq", r"f(\theta-\eta g)\le f(\theta)-\eta\Bigl(1-\frac{L\eta}{2}\Bigr)\|g\|^2"),
            ("p", "The factor $1-L\\eta/2$ is positive for $\\eta&lt;2/L$ — exactly the stability boundary from Figure 1. The guaranteed decrease is largest at $\\eta=1/L$: then $f$ drops by at least $\\|g\\|^2/(2L)$."),
            ("p", "For a quadratic $f=\\tfrac12\\theta^\\top H\\theta$ the step is a linear map $\\theta_t=(I-\\eta H)\\,\\theta_{t-1}$. In the eigenbasis of $H$ every coordinate is multiplied by $1-\\eta\\lambda_i$, and descent converges if and only if $|1-\\eta\\lambda_i|&lt;1$ for all $i$, that is $0&lt;\\eta&lt;2/\\lambda_{\\max}$ (for a positive definite $H$)."),
        ]),
        ("h3", "The condition number: why descent can be slow"),
        ("p", "If the curvatures differ between directions, the step has to adapt to the steepest one: $\\eta&lt;2/\\lambda_{\\max}$. Then along the gentlest direction a coordinate shrinks per step by only the fraction $\\eta\\lambda_{\\min}&lt;2/\\kappa$, where $\\kappa=\\lambda_{\\max}/\\lambda_{\\min}$ is the <b>condition number</b>. Even with the best constant step $\\eta=2/(\\lambda_{\\max}+\\lambda_{\\min})$ the error shrinks per step only by the factor $(\\kappa-1)/(\\kappa+1)$:"),
        ("eq", r"\|\theta_t-\theta^*\|\le\Bigl(\frac{\kappa-1}{\kappa+1}\Bigr)^{t}\,\|\theta_0-\theta^*\|"),
        ("p", "At $\\kappa=100$ the factor is $0.980$, and reducing the error a thousandfold takes about 345 steps. A rough rule: SGD spends on the order of $\\kappa$ steps per digit of accuracy."),
        ("table", ["Method", "Step", "State", "Hyperparameters"], [
            ["SGD", "$\\theta_t=\\theta_{t-1}-\\eta g_t$", "none", "$\\eta$"],
            ["Momentum", "$u_t=\\beta u_{t-1}+g_t$,<br>$\\theta_t=\\theta_{t-1}-\\eta u_t$", "$u$: one number per weight", "$\\eta$, $\\beta\\approx0.9$"],
            ["RMSProp", "$v_t=\\beta v_{t-1}+(1-\\beta)g_t^2$,<br>$\\theta_t=\\theta_{t-1}-\\eta\\,\\dfrac{g_t}{\\sqrt{v_t}+\\epsilon}$", "$v$: one number per weight", "$\\eta$, $\\beta=0.9$–$0.99$, $\\epsilon$"],
        ], {}),
    ]),
    dict(id="noise", title="Stochasticity: mini-batches and noise", blocks=[
        ("p", "The full gradient is the mean over all $N$ examples of the training set. With millions of examples one such step would cost a pass over all the data. SGD takes a random mini-batch of $B$ examples. Its gradient is an <b>unbiased</b> estimate of the full one: it equals $\\nabla L$ on average, but every time it deviates by random noise."),
        ("eq", r"\mathbb E\,[g_t]=\nabla L(\theta),\qquad \operatorname{Cov}[g_t]=\frac{\Sigma}{B}\cdot\frac{N-B}{N-1}"),
        ("symbols", [
            (r"\Sigma", "the covariance of per-example gradients at the current point (normalized by $N$);"),
            (r"\frac{N-B}{N-1}", "the correction for sampling without replacement: at $B=N$ the noise vanishes."),
        ]),
        ("p", "The noise variance falls as $1/B$ while the cost of a step grows as $B$. So within one epoch (one pass over the data) small batches make many imprecise steps and large batches few precise ones. The figure shows linear regression $y\\approx wx+b$ on 200 points with the loss $L=\\frac1{2N}\\sum(wx_i+b-y_i)^2$: a quadratic “bowl” over the plane of the weights $(w,\\,b)$."),
        ("viz", "sgd-minibatch", {"B": 10, "eta": 0.05}, "<b>Figure 2.</b> Left: the SGD path over the loss contours; the orange points show where the next step would land for 40 different random batches, the arrow is the full-gradient step. Right: the excess loss over the minimum $L-L^*$ by epoch. After 8 epochs with $\\eta=0.05$, starting from $5.84$: batch 1 reaches $1.4\\cdot10^{-3}$, batch 10 reaches $0.044$, batch 50 reaches $1.06$, and the full gradient (only 8 steps) reaches $2.0$. Press “Play” and compare the clouds: for $B=1$ it stays wide even at the minimum."),
        ("callout", "intuition", "Noise is not only a nuisance", "At the minimum the full gradient is zero, but the stochastic one is not. With a constant $\\eta$, SGD does not stop but jitters in a cloud whose size grows like $\\sqrt\\eta$; that is why the rate is lowered towards the end of training. On the other hand, the same noise helps escape saddle points and narrow minima; there is evidence that it biases training towards flatter minima that generalize better."),
        ("deep", "The linear scaling rule for the batch size", [
            ("p", "If the batch grows $k$ times, the noise variance drops $k$ times, but there are $k$ times fewer steps per epoch. Goyal et al. (2017) proposed to raise $\\eta$ $k$ times as well: that is how ResNet-50 was trained on ImageNet with a batch of 8192 in one hour without losing accuracy. The rule holds up to some “critical” batch size and requires warmup — a gradual increase of $\\eta$ over the first epochs."),
        ]),
    ]),
    dict(id="momentum", title="Momentum: the inertia of a heavy ball", blocks=[
        ("p", "Gradient descent is a massless point: at every moment it moves exactly where the slope points. Boris Polyak (1964) proposed to give it mass. A heavy ball rolls, builds up speed and does not react to every bump. In the formula the velocity is the vector $u$:"),
        ("eq", r"u_t=\beta\,u_{t-1}+g_t,\qquad \theta_t=\theta_{t-1}-\eta\,u_t"),
        ("symbols", [
            (r"u_t", "the accumulated direction (the momentum buffer), $u_0=0$;"),
            (r"\beta", "the momentum coefficient, $0\\le\\beta&lt;1$, usually $0.9$; at $\\beta=0$ this is plain SGD."),
        ]),
        ("p", "Unroll the recursion: $u_t=g_t+\\beta g_{t-1}+\\beta^2 g_{t-2}+\\dots$ — a weighted sum of all past gradients with exponentially decaying weights. If gradients keep pointing the same way from step to step, they add up and the step grows to $\\eta/(1-\\beta)$, ten times larger at $\\beta=0.9$. If the sign flips (a zigzag across a ravine), the terms cancel each other."),
        ("viz", "sgd-ema", {"beta": 0.9}, "<b>Figure 3.</b> Left: the weight with which a gradient $k$ steps old enters $u_t$; the bright bars are the most recent gradients that together carry at least half of the total weight. Right: the response of $u_t$ to a constant gradient $g=1$: it grows towards $1/(1-\\beta)=10$ and reaches $90\\%$ of the limit by step 22. At $\\beta=0.9$ half of the weight falls on the last 7 gradients, at $\\beta=0.99$ on the last 69, with a memory window of 100 steps."),
        ("callout", "note", "Two ways to write the same momentum", "PyTorch writes $u_t=\\beta u_{t-1}+g_t$, as here. The exponential moving average (EMA) $m_t=\\beta m_{t-1}+(1-\\beta)g_t$ is also common: it differs by the constant factor $1-\\beta$, which moves into $\\eta$. The EMA is exactly what sits in the numerator of <a href=\"../adam/\">Adam</a>. Switch the form in the figure: the EMA starts at $0.1$ instead of 1 and only gradually reaches the true value — this underestimate in the first steps is the reason for bias correction in Adam."),
        ("h3", "Why momentum accelerates: theory on a quadratic"),
        ("p", "Take one direction with curvature $L$ and write $h=\\eta L$. Substitute $g_t=L\\theta_{t-1}$ and eliminate $u$ (from the second formula $\\eta u_{t-1}=\\theta_{t-2}-\\theta_{t-1}$). We get a second-order linear recurrence:"),
        ("eq", r"\theta_t=(1+\beta-h)\,\theta_{t-1}-\beta\,\theta_{t-2}"),
        ("p", "Its behaviour is set by the roots of the characteristic equation $\\lambda^2-(1+\\beta-h)\\lambda+\\beta=0$. The convergence rate is the largest root modulus $\\rho$: the error decays roughly like $\\rho^t$."),
        ("viz", "sgd-momentum", {"h": 0.04, "beta": 0.9}, "<b>Figure 4.</b> Left: a map of the rate $\\rho$ over $\\eta L$ (log scale) and $\\beta$: blue means fast convergence, red means divergence, the solid line is the boundary $\\rho=1$, the dashed lines mark critical damping. Drag the blue point. Right: $\\theta_t$ for SGD with the same $\\eta$ and with momentum. At $\\eta L=0.04$ SGD needs 170 steps to reach $|\\theta|&lt;10^{-3}$ ($\\rho=0.96$), momentum with $\\beta=0.9$ needs 130 steps with oscillations, Nesterov with the same $\\beta$ needs 87, and critical damping $\\beta=(1-\\sqrt{0.04})^2=0.64$ gives 41 steps ($\\rho=0.8$)."),
        ("deep", "Derivation: the stability region and the optimal momentum", [
            ("p", "The roots are complex when $(1+\\beta-h)^2&lt;4\\beta$, i.e. for $(1-\\sqrt\\beta)^2&lt;h&lt;(1+\\sqrt\\beta)^2$. The product of the roots is $\\beta$, so $|\\lambda_1|=|\\lambda_2|=\\sqrt\\beta$: $\\theta_t$ oscillates and decays by the factor $\\sqrt\\beta$ per step regardless of $h$. Outside this band the roots are real. Together the two cases give the exact stability region (the Schur–Cohn conditions for a quadratic):"),
            ("eq", r"0<\eta L<2(1+\beta)"),
            ("p", "— momentum almost doubles the admissible step (for SGD it is $\\eta L&lt;2$)."),
            ("p", "Let the curvatures fill the interval $[\\mu,\\,L]$, $\\kappa=L/\\mu$. Choose $\\eta$ and $\\beta$ so that both ends land on the edges of the complex band: $(1-\\sqrt\\beta)^2=\\eta\\mu$ and $(1+\\sqrt\\beta)^2=\\eta L$. Then all directions decay equally fast:"),
            ("eq", r"\eta=\frac{4}{(\sqrt L+\sqrt\mu)^2},\qquad \beta=\Bigl(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\Bigr)^2,\qquad \rho=\sqrt\beta=\frac{\sqrt\kappa-1}{\sqrt\kappa+1}"),
            ("p", "Compare with the best SGD, $\\rho=(\\kappa-1)/(\\kappa+1)$. At $\\kappa=100$ this is $0.818$ versus $0.980$: about 35 steps instead of 345 to reduce the error a thousandfold. The number of steps grows like $\\sqrt\\kappa$ rather than $\\kappa$ — that is the heavy ball’s acceleration."),
        ]),
        ("h3", "Nesterov: the gradient where momentum is taking you"),
        ("p", "Yurii Nesterov (1983) proposed to compute the gradient not at the current point but where momentum will carry the ball anyway. In PyTorch’s form (<code>nesterov=True</code>) this is a correction to the step:"),
        ("eq", r"u_t=\beta u_{t-1}+g_t,\qquad \theta_t=\theta_{t-1}-\eta\,(g_t+\beta u_t)"),
        ("p", "The characteristic equation becomes $\\lambda^2-(1+\\beta)(1-h)\\lambda+\\beta(1-h)=0$. Along gentle directions oscillations decay faster ($\\rho=\\sqrt{\\beta(1-h)}$ instead of $\\sqrt\\beta$), but the stability region is narrower: $\\eta L&lt;2(1+\\beta)/(1+2\\beta)$, only $1.36$ at $\\beta=0.9$. Switch Figure 4 to “Nesterov” to see both features."),
    ]),
    dict(id="rmsprop", title="RMSProp: a step of its own for every weight", blocks=[
        ("p", "SGD and Momentum use one rate $\\eta$ for all weights. But the gradients of different weights can differ by orders of magnitude: embeddings of rare words get rare large kicks, the biases of the last layer get constant small ones. A shared $\\eta$ is too large for some and too small for others. RMSProp (Geoffrey Hinton, Coursera lectures, 2012) divides the step of each weight by its typical gradient size:"),
        ("eq", r"v_t=\beta\,v_{t-1}+(1-\beta)\,g_t^2,\qquad\theta_t=\theta_{t-1}-\eta\,\frac{g_t}{\sqrt{v_t}+\epsilon}"),
        ("symbols", [
            (r"g_t^2", "an element-wise square: every weight has its own $v$;"),
            (r"v_t", "the exponential moving average of the squared gradient, an estimate of $\\mathbb E[g^2]$ over the last $\\sim1/(1-\\beta)$ steps, $v_0=0$;"),
            (r"\sqrt{v_t}", "the root mean square (RMS) of the gradient — hence the name;"),
            (r"\epsilon", "a small constant ($10^{-8}$) against division by zero."),
        ]),
        ("p", "Dividing by $\\sqrt{v_t}$ makes the step dimensionless: multiply all gradients of a weight by 1000 and $\\sqrt v$ grows 1000 times too, so the step does not change. A typical step becomes of order $\\eta$ — the rate now sets the step length directly in the units of the weights."),
        ("viz", "sgd-rmsprop", {"beta": 0.9}, "<b>Figure 5.</b> The gradient of one weight whose scale changes: at step 100 it grows 10 times, at step 200 it drops 100 times. Top: $|g_t|$ and $\\sqrt{v_t}$; bottom: the step length. The SGD step jumps by two orders of magnitude together with the gradient, the RMSProp step stays of order $\\eta=0.01$. But adaptation lags: after the rise the step briefly spikes (at $\\beta=0.9$ up to $0.030$ against the bound $0.032$), and after the drop it sags — the old large $v$ needs about $\\ln10^4/\\ln(1/0.9)\\approx87$ steps to be forgotten."),
        ("callout", "key", "A built-in step bound", "From $v_t\\ge(1-\\beta)g_t^2$ it follows that $|g_t|/\\sqrt{v_t}\\le1/\\sqrt{1-\\beta}$. The RMSProp step never exceeds $\\eta/\\sqrt{1-\\beta}$: $3.16\\,\\eta$ at $\\beta=0.9$ and $10\\,\\eta$ at $\\beta=0.99$. This is a protection against exploding gradients that SGD does not have."),
        ("deep", "Where RMSProp comes from: AdaGrad and Rprop", [
            ("p", "The predecessor is AdaGrad (Duchi, Hazan, Singer, 2011): $v_t=v_{t-1}+g_t^2$, a sum instead of an average. It is good for convex problems with sparse features, but in neural networks $v$ only grows, and the step $\\eta/\\sqrt{v_t}$ inevitably decays to zero. RMSProp replaced the sum with an exponential average that has finite memory."),
            ("p", "Another root is Rprop (Riedmiller and Braun, 1993), which uses only the sign of the gradient. RMSProp can be read as its mini-batch version: at $\\beta=0$ we get $v_t=g_t^2$ and the step $\\eta\\operatorname{sign}(g_t)$."),
            ("p", "Importantly, RMSProp scales the coordinate axes but does not rotate them. This is <b>diagonal</b> preconditioning. If a ravine runs diagonally between weights, dividing by $\\sqrt v$ helps little — you can see it in Figure 6 with a 45° rotation."),
        ]),
    ]),
    dict(id="landscape", title="Trajectories in 2D and 3D", blocks=[
        ("p", "Let us compare the three methods on one problem — an elongated quadratic valley $f=\\tfrac12(a^2+\\kappa b^2)$, where $a$ and $b$ are the coordinates along and across the ravine: the curvature across is $\\kappa$ times larger than along. The start is at $a=-3.4$, $b=0.9$, where $f=46.3$."),
        ("viz", "sgd-ravine", {"kappa": 100, "eta": 0.018, "beta": 0.9}, "<b>Figure 6.</b> A ravine with $\\kappa=100$: the view from above and the surface in 3D (you can rotate it). With $\\eta=0.018$ SGD jumps across the ravine ($\\eta\\lambda_{\\max}=1.8$) and crawls slowly along it: after 100 steps $f$ only drops to $0.15$. Momentum with $\\beta=0.9$ reaches $2.2\\cdot10^{-4}$, RMSProp with $\\eta=0.1$ reaches $0.026$: it quickly gets down to the floor but then jitters with a step of order $\\eta$. Rotate the ravine by 45°: SGD and Momentum do not notice, but RMSProp loses its advantage — $0.30$ instead of $0.026$."),
        ("p", "The second classic is the Rosenbrock function $f=(1-x)^2+100(y-x^2)^2$: a narrow curved “banana” with its minimum at $(1,\\,1)$. Here the curvature changes from point to point, and no constant step is ideal."),
        ("viz", "sgd-rosenbrock", {}, "<b>Figure 7.</b> 3000 steps from the point $(-1.5,\\,2)$, which you can drag. SGD with $\\eta=0.001$ only gets to $f=0.049$. Momentum with the same $\\eta$ and $\\beta=0.9$ gets through the banana: $f&lt;10^{-3}$ at step 666 and $3\\cdot10^{-12}$ by the end. RMSProp with $\\eta=0.01$ gets stuck around $f\\approx0.02$: its step barely shrinks near the floor. The $t$ slider shows where all three are at any moment."),
        ("callout", "warn", "The map is not the territory", "Two-dimensional pictures are useful but deceptive: a real network has millions of dimensions, most critical points there are saddles rather than local minima, and the loss surface itself depends on the mini-batch. Use the pictures for intuition about mechanisms (zigzag, inertia, scale), not for choosing an optimizer."),
    ]),
    dict(id="code", title="In code: from scratch and in PyTorch", blocks=[
        ("p", "All three methods fit into two small classes. Note that the state ($u$ or $v$) is an array of the same size as the weights, so Momentum and RMSProp double the memory for parameters and Adam triples it."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "The numbers in the comments match Figure 6, and <code>torch.optim.SGD</code> and <code>torch.optim.RMSprop</code> give the same values on the same problem. Nesterov with the same $\\eta$ diverges — exactly as the stability condition from the momentum section predicts."),
        ("code", "python", "CODE_TORCH"),
        ("callout", "note", "Two forms of momentum in libraries", "PyTorch stores the sum of raw gradients and multiplies it by the current $\\eta$: $\\theta\\leftarrow\\theta-\\eta_t u_t$. Keras and the classic paper by Sutskever et al. (2013) store a velocity already multiplied by the rate: $v_t=\\beta v_{t-1}-\\eta_t g_t$, $\\theta\\leftarrow\\theta+v_t$. With a constant $\\eta$ the forms are equivalent, with a schedule they are not: in PyTorch a new $\\eta$ immediately applies to the whole accumulated buffer."),
    ]),
    dict(id="practice", title="Hyperparameters and practice", blocks=[
        ("table", ["Parameter", "Typical values", "How to choose"], [
            ["$\\eta$ (SGD with momentum)", "$0.01$–$0.1$", "the largest value at which the loss still falls steadily; ResNet: $0.1$ at batch 256"],
            ["$\\beta$ (momentum)", "$0.9$, sometimes $0.95$–$0.99$", "a larger $\\beta$ means longer memory and stronger acceleration, but a higher risk of oscillation"],
            ["$\\beta$ of RMSProp (alpha)", "$0.9$–$0.99$", "averaging window $1/(1-\\beta)$: 10 to 100 steps"],
            ["$\\eta$ (RMSProp)", "$10^{-4}$–$10^{-3}$", "a step of order $\\eta$ in the units of the weights"],
            ["$B$ (batch)", "32–512", "when $B$ grows $k$ times, raise $\\eta$ $k$ times, with warmup"],
            ["weight decay", "$10^{-4}$–$5\\cdot10^{-4}$", "shrinks the weights; for SGD it coincides with $L_2$ regularization"],
        ], {}),
        ("ul", [
            "<b>Learning-rate schedule.</b> Step decay (multiply by $0.1$ at epochs 30 and 60 out of 90 — the ResNet classic), cosine or one-cycle. A constant $\\eta$ leaves a noise cloud around the minimum.",
            "<b>Warmup.</b> Over the first hundreds to thousands of steps $\\eta$ grows linearly from a small value — especially important with a large batch.",
            "<b>Gradient clipping</b> by norm protects against rare huge gradients in RNNs and transformers.",
            "<b>Learning-rate search</b> (the LR range test, Leslie Smith): a short run with an exponentially growing $\\eta$; pick a value well below the point where the loss starts to rise.",
            "<b>Normalization</b> of inputs, batch normalization and sensible initialization lower the condition number and allow a larger $\\eta$.",
        ]),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>A forgotten <code>zero_grad()</code>.</b> In PyTorch gradients accumulate in <code>.grad</code>; without resetting, $g_t$ becomes the sum of all past gradients — not momentum, but a bug.",
            "<b>A learning rate that is too large</b>: the loss grows or turns into NaN. By Figure 1 you need $\\eta&lt;2/\\lambda_{\\max}$; first of all reduce $\\eta$ 3–10 times.",
            "<b>Carrying $\\eta$ over between optimizers.</b> With momentum $\\beta=0.9$ the steady-state step is 10 times larger than SGD’s with the same $\\eta$. For RMSProp and Adam $\\eta$ is in different units altogether: $10^{-3}$ is normal for them and usually too small for SGD.",
            "<b>Changing the batch without changing the rate.</b> The batch grew 8 times and $\\eta$ stayed — the network learns more slowly per epoch; the batch shrank — the noise may destabilize training.",
            "<b>$\\epsilon=10^{-8}$ in low precision.</b> In float16 this number rounds to zero, and when $v\\approx0$ the RMSProp step explodes; with mixed precision $v$ is kept in float32 or $\\epsilon$ is made larger.",
            "<b>A constant rate until the end of training.</b> Without lowering $\\eta$, SGD jitters around the minimum and the last epochs achieve almost nothing.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../adam/\">Adam</a>: the numerator is EMA momentum, the denominator is $\\sqrt{v}$ from RMSProp, plus bias correction.",
            "<a href=\"../mse/\">MSE</a>: its gradient $\\frac2n\\sum_i(\\hat y_i-y_i)\\,x_i$ is, up to a factor of 2, the $g_t$ of the linear regression in Figure 2 (the loss there is half the MSE).",
            "<a href=\"../bce/\">BCE</a> and <a href=\"../cross-entropy/\">cross-entropy</a>: the gradient with respect to the logits, $\\hat y-y$, is the simplest descent signal.",
            "<a href=\"../sigmoid/\">The sigmoid</a>: saturation produces tiny gradients — SGD almost stands still on them, while RMSProp stretches the step.",
            "<a href=\"../huber/\">Huber</a>: caps the gradient of outliers — a relative of gradient clipping.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) SGD: $\\theta_t=\\theta_{t-1}-\\eta g_t$, where $g_t$ is an unbiased mini-batch estimate of the gradient; the noise variance falls as $1/B$. 2) Stability: $\\eta&lt;2/\\lambda_{\\max}$; the speed is set by the condition number $\\kappa$ — on the order of $\\kappa$ steps per digit of accuracy. 3) Momentum $u_t=\\beta u_{t-1}+g_t$ is an exponential memory of gradients with window $1/(1-\\beta)$; on quadratics it cuts the journey to the order of $\\sqrt\\kappa$ steps and extends stability to $\\eta L&lt;2(1+\\beta)$. 4) RMSProp divides the step by $\\sqrt{v_t}$: the step is dimensionless, of order $\\eta$, but the adaptation is only diagonal. 5) EMA momentum + RMSProp + bias correction = Adam."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="$f(\\theta)=5\\theta^2$. For which constant $\\eta$ does gradient descent converge?", options=["$\\eta&lt;0.1$", "$\\eta&lt;0.2$", "$\\eta&lt;0.4$", "$\\eta&lt;2$"], answer=1,
                 explain="The curvature is $f''=10$, and $\\eta L&lt;2$ gives $\\eta&lt;0.2$. At $\\eta=0.1$ the minimum is reached in one step."),
            dict(q="What is the memory window of momentum at $\\beta=0.95$?", options=["5 steps", "20 steps", "95 steps", "$0.05$ steps"], answer=1,
                 explain="$1/(1-\\beta)=1/0.05=20$."),
            dict(q="The batch grew from 32 to 128 (there is far more data than $B$). What happens to the variance of the stochastic gradient?", options=["It grows 4 times", "It drops 2 times", "It drops 4 times", "It does not change"], answer=2,
                 explain="$\\operatorname{Cov}[g]\\approx\\Sigma/B$: the batch grew 4 times, so the variance dropped 4 times (and the standard deviation 2 times)."),
            dict(q="All gradients of one weight are multiplied by 100. How does the RMSProp step change once $v$ settles (ignoring $\\epsilon$)?", options=["It grows 100 times", "It grows 10 times", "It does not change", "It shrinks 100 times"], answer=2,
                 explain="$\\sqrt v$ also grows 100 times, and the ratio $g/\\sqrt v$ stays the same."),
            dict(q="Why does momentum speed up descent along an elongated ravine?", options=["Along the ravine the gradients agree and add up, across it the sign alternates and they cancel", "It reduces the curvature of the function", "It computes second derivatives", "It divides the step by $\\sqrt v$"], answer=0,
                 explain="$u_t$ is a sum of past gradients with weights $\\beta^k$: consistent components grow up to $1/(1-\\beta)$, alternating ones cancel."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="Bu nima uchun kerak", blocks=[
        ("p", "Neyron tarmoqni o‘qitish — millionlab va milliardlab $\\theta$ vaznlar bo‘yicha $L(\\theta)$ yo‘qotish funksiyasining minimumini izlash. Minimum uchun tayyor formula yo‘q: yo‘qotish vaznlarga juda murakkab bog‘liq. Minimumga qadam-baqadam borish qoladi, har bir qadamdagi yagona mo‘ljal esa $\\nabla L$ gradiyent: yo‘qotish eng tez o‘sadigan yo‘nalishni ko‘rsatuvchi vektor. Biz teskari tomonga qadam tashlaymiz."),
        ("p", "Bu sahifa bitta usulning uchta pog‘onasi haqida:"),
        ("ul", [
            "<b>SGD</b> (stochastic gradient descent, stoxastik gradiyentli tushish) — kichik tasodifiy misollar to‘plami, mini-batch bo‘yicha hisoblangan gradiyentga qarshi qadam;",
            "<b>Momentum</b> (inersiya, og‘ir shar usuli) — o‘tgan gradiyentlarning to‘plangan yig‘indisiga qarshi qadam: inersiya zigzaglarni so‘ndiradi va qiya yo‘nalishlar bo‘ylab tushishni tezlashtiradi;",
            "<b>RMSProp</b> — yaqindagi gradiyentlarning o‘rta kvadratik kattaligiga bo‘lingan qadam: har bir vaznning o‘z qadam masshtabi bor.",
        ]),
        ("p", "Ikkinchi va uchinchi pog‘onani qo‘shing, siljishni tuzatishni qo‘shing — <a href=\"../adam/\">Adam</a> hosil bo‘ladi. Inersiyali SGD esa hamon tasvirlar uchun ko‘plab o‘ramli tarmoqlarni o‘qitadi va ularda ko‘pincha adaptiv usullardan yaxshiroq umumlashtiradi."),
        ("callout", "key", "Bir daqiqada asosiysi", "$\\theta_t=\\theta_{t-1}-\\eta g_t$. Qadam faqat $\\eta L&lt;2$ bo‘lganda barqaror, bu yerda $L$ — yo‘qotishning eng katta egriligi. Cho‘ziq vodiy (katta $\\kappa$ shartlanganlik soni) SGD’ni sudralishga majbur qiladi; $\\eta$ va $\\beta$ yaxshi tanlanganda $u_t=\\beta u_{t-1}+g_t$ inersiya yo‘lni taxminan $\\kappa$ dan $\\sqrt\\kappa$ qadamgacha qisqartiradi; RMSProp qadamni $\\sqrt{v_t}$ ga bo‘ladi va turli vaznlar masshtablarini tenglashtiradi."),
    ]),
    dict(id="intuition", title="Intuitsiya: pastga qadam", blocks=[
        ("p", "Quyuq tumanda tepalikdan tushayotganingizni tasavvur qiling. Faqat oyoq ostidagi qiyalik ko‘rinadi: u qayerga va qanchalik tik pastga ketyapti. Oqilona strategiya — eng tik tushish tomonga qadam tashlash, atrofga qarash va takrorlash. Qadam uzunligini <b>o‘qitish tezligi</b> (learning rate) $\\eta$ belgilaydi."),
        ("p", "Qisqa qadamlar ishonchli, lekin sekin. Juda uzun qadam chuqurlik tubidan sakrab o‘tib, qarama-qarshi yonbag‘irga tushadi — agar u yerda balandroq bo‘lsa, keyingi qadam yanada uzoqqa otib yuboradi. Buni eng oddiy $f(\\theta)=L\\theta^2/2$ yo‘qotishda ko‘ring: uning gradiyenti $f'(\\theta)=L\\theta$, egriligi (ikkinchi hosilasi) esa $L$ ga teng."),
        ("viz", "sgd-parabola", {"eta": 0.3, "L": 2, "x0": 2}, "<b>1-rasm.</b> Parabolada gradiyentli tushish. Yuqorida — egri chiziq bo‘ylab qadamlar ($\\theta_0$ boshlang‘ich nuqtani tortish mumkin), pastda — minimumgacha masofa $|\\theta_t|$ logarifmik shkalada. $L=2$ va $\\eta=0{,}3$ da har bir qadam $\\theta$ ni $1-\\eta L=0{,}4$ ga ko‘paytiradi va $\\theta_0=2$ dan $|\\theta|&lt;0{,}01$ gacha 6 qadam kerak. $\\eta$ ni oshiring: $0{,}5$ da minimumga bir qadamda yetiladi, $0{,}6$ da nuqta minimum ustidan sakraydi, $\\eta&gt;1$ da esa tushish uzoqlashadi."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "Hammasini bitta son hal qiladi: $\\eta L$. $\\eta L&lt;1$ da tushish monoton, $1&lt;\\eta L&lt;2$ da nuqta minimum ustidan sakraydi, lekin unga yaqinlashadi, $\\eta L&gt;2$ da uchib ketadi. $\\eta=1/L$ qadam minimumga darhol tushadi — lekin faqat egrilik barcha yo‘nalishlarda bir xil bo‘lsa."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("eq", r"\theta_t=\theta_{t-1}-\eta\,g_t,\qquad g_t=\frac1B\sum_{i\in B_t}\nabla_\theta\,\ell(x_i,y_i;\,\theta_{t-1})"),
        ("symbols", [
            (r"\theta_{t-1}", "joriy vaznlar — modelning barcha parametrlari vektori;"),
            (r"g_t", "stoxastik gradiyent: $B$ ta tasodifiy misoldan iborat $B_t$ mini-batch bo‘yicha $\\ell$ yo‘qotish gradiyentlarining o‘rtachasi;"),
            (r"\eta", "o‘qitish tezligi, musbat son, odatda $10^{-4}$ dan $10^{-1}$ gacha;"),
            (r"-\eta\,g_t", "qadam: gradiyentga qarshi, uzunligi $\\eta\\|g_t\\|$ — qiyalik qanchalik tik bo‘lsa, shunchalik uzun."),
        ]),
        ("p", "Nega bu ishlaydi. Yo‘qotishni joriy nuqta atrofida Teylor qatoriga yoyamiz: $L(\\theta-\\eta g)\\approx L(\\theta)-\\eta\\,\\|g\\|^2$. Qadam kichik ekan, yo‘qotish taxminan $\\eta\\|g\\|^2$ ga kamayadi va bu bir xil uzunlikdagi qadamlar orasida eng tez kamayish: $\\|d\\|$ uzunlik qayd etilganda $\\langle\\nabla L,\\,d\\rangle$ skalyar ko‘paytma $d$ gradiyentga qarshi yo‘nalganda eng kichik bo‘ladi."),
        ("callout", "note", "Sonli misol", "$f(\\theta)=\\theta^2$, $\\theta_0=3$, $\\eta=0{,}1$. Gradiyent $g_1=2\\cdot3=6$, qadam $-0{,}1\\cdot6=-0{,}6$, yangi qiymat $\\theta_1=2{,}4$, yo‘qotish $9$ dan $5{,}76$ ga tushadi. Har bir keyingi qadam $\\theta$ ni yana $1-2\\eta=0{,}8$ ga ko‘paytiradi."),
        ("deep", "Qadam qanchalik katta bo‘lishi mumkin: tushish lemmasi", [
            ("p", "$f$ gradiyenti $L$ konstantali Lipshits shartini qanoatlantirsin: $\\|\\nabla f(a)-\\nabla f(b)\\|\\le L\\|a-b\\|$ (ikki marta differensiallanuvchi $f$ uchun bu gessian xos qiymatlari moduli $L$ dan oshmasligini bildiradi). U holda $f$ joriy nuqtada unga urinuvchi parabola ostida yotadi va $g=\\nabla f(\\theta)$ bilan $\\theta-\\eta g$ qadam uchun:"),
            ("eq", r"f(\theta-\eta g)\le f(\theta)-\eta\Bigl(1-\frac{L\eta}{2}\Bigr)\|g\|^2"),
            ("p", "$1-L\\eta/2$ ko‘paytuvchi $\\eta&lt;2/L$ da musbat — bu 1-rasmdagi o‘sha barqarorlik chegarasi. Kafolatlangan kamayish $\\eta=1/L$ da eng katta: u holda $f$ kamida $\\|g\\|^2/(2L)$ ga kamayadi."),
            ("p", "$f=\\tfrac12\\theta^\\top H\\theta$ kvadratik funksiya uchun qadam chiziqli akslantirish: $\\theta_t=(I-\\eta H)\\,\\theta_{t-1}$. $H$ ning xos bazisida har bir koordinata $1-\\eta\\lambda_i$ ga ko‘payadi va tushish barcha $i$ uchun $|1-\\eta\\lambda_i|&lt;1$ bo‘lganda va faqat shundagina yaqinlashadi, ya’ni $0&lt;\\eta&lt;2/\\lambda_{\\max}$ (musbat aniqlangan $H$ uchun)."),
        ]),
        ("h3", "Shartlanganlik soni: nega tushish sekin bo‘lishi mumkin"),
        ("p", "Agar turli yo‘nalishlardagi egriliklar farq qilsa, qadam eng tikiga moslashishi shart: $\\eta&lt;2/\\lambda_{\\max}$. U holda eng qiya yo‘nalish bo‘ylab koordinata bir qadamda faqat $\\eta\\lambda_{\\min}&lt;2/\\kappa$ ulushga kamayadi, bu yerda $\\kappa=\\lambda_{\\max}/\\lambda_{\\min}$ — <b>shartlanganlik soni</b> (condition number). Hatto eng yaxshi o‘zgarmas $\\eta=2/(\\lambda_{\\max}+\\lambda_{\\min})$ qadamda ham xato bir qadamda faqat $(\\kappa-1)/(\\kappa+1)$ marta kamayadi:"),
        ("eq", r"\|\theta_t-\theta^*\|\le\Bigl(\frac{\kappa-1}{\kappa+1}\Bigr)^{t}\,\|\theta_0-\theta^*\|"),
        ("p", "$\\kappa=100$ da ko‘paytuvchi $0{,}980$ ga teng va xatoni ming marta kamaytirish uchun 345 ga yaqin qadam kerak. Taxminiy qoida: SGD aniqlikning har bir tartibiga $\\kappa$ tartibidagi qadam sarflaydi."),
        ("table", ["Usul", "Qadam", "Nimani saqlaydi", "Giperparametrlar"], [
            ["SGD", "$\\theta_t=\\theta_{t-1}-\\eta g_t$", "hech narsa", "$\\eta$"],
            ["Momentum", "$u_t=\\beta u_{t-1}+g_t$,<br>$\\theta_t=\\theta_{t-1}-\\eta u_t$", "$u$: har bir vaznga bitta son", "$\\eta$, $\\beta\\approx0{,}9$"],
            ["RMSProp", "$v_t=\\beta v_{t-1}+(1-\\beta)g_t^2$,<br>$\\theta_t=\\theta_{t-1}-\\eta\\,\\dfrac{g_t}{\\sqrt{v_t}+\\epsilon}$", "$v$: har bir vaznga bitta son", "$\\eta$, $\\beta=0{,}9$–$0{,}99$, $\\epsilon$"],
        ], {}),
    ]),
    dict(id="noise", title="Stoxastiklik: mini-batch’lar va shovqin", blocks=[
        ("p", "To‘liq gradiyent — o‘qitish to‘plamidagi barcha $N$ ta misol bo‘yicha o‘rtacha. Millionlab misollarda bitta shunday qadam barcha ma’lumotlardan bir marta o‘tishga teng bo‘lardi. SGD $B$ ta misoldan iborat tasodifiy mini-batch oladi. Uning gradiyenti to‘liq gradiyentning <b>siljimagan</b> bahosi: o‘rtacha $\\nabla L$ ga teng, lekin har safar tasodifiy shovqinga og‘adi."),
        ("eq", r"\mathbb E\,[g_t]=\nabla L(\theta),\qquad \operatorname{Cov}[g_t]=\frac{\Sigma}{B}\cdot\frac{N-B}{N-1}"),
        ("symbols", [
            (r"\Sigma", "joriy nuqtadagi alohida misollar gradiyentlarining kovariatsiyasi ($N$ ga bo‘lingan);"),
            (r"\frac{N-B}{N-1}", "qaytarmasdan tanlash tuzatmasi: $B=N$ da shovqin yo‘qoladi."),
        ]),
        ("p", "Shovqin dispersiyasi $1/B$ kabi kamayadi, qadam narxi esa $B$ kabi o‘sadi. Shuning uchun bitta davrda (ma’lumotlardan bir marta o‘tishda) kichik batch’lar ko‘p noaniq qadam, kattalari esa kam aniq qadam qiladi. Rasmda — 200 nuqtadagi $y\\approx wx+b$ chiziqli regressiya, yo‘qotish $L=\\frac1{2N}\\sum(wx_i+b-y_i)^2$: $(w;\\,b)$ vaznlar tekisligi ustidagi kvadratik «kosa»."),
        ("viz", "sgd-minibatch", {"B": 10, "eta": 0.05}, "<b>2-rasm.</b> Chapda — yo‘qotish sath chiziqlari bo‘ylab SGD yo‘li; to‘q sariq nuqtalar — 40 xil tasodifiy batch’da keyingi qadam qayerga tushishi, strelka — to‘liq gradiyent bo‘yicha qadam. O‘ngda — yo‘qotishning minimumdan ortig‘i $L-L^*$ davrlar bo‘yicha. $\\eta=0{,}05$ bilan 8 davrda, boshlang‘ich $5{,}84$ dan: 1 o‘lchamli batch $1{,}4\\cdot10^{-3}$ gacha, 10 lik — $0{,}044$ gacha, 50 lik — $1{,}06$ gacha, to‘liq gradiyent (atigi 8 qadam) esa $2{,}0$ gacha yetadi. «Boshlash»ni bosing va bulutlarni solishtiring: $B=1$ da u hatto minimum yonida ham keng."),
        ("callout", "intuition", "Shovqin — faqat xalaqit emas", "Minimumda to‘liq gradiyent nolga teng, stoxastik esa — yo‘q. O‘zgarmas $\\eta$ da SGD to‘xtamaydi, balki o‘lchami $\\sqrt\\eta$ kabi o‘sadigan bulut ichida titraydi; shuning uchun o‘qitish oxirida tezlik pasaytiriladi. Buning evaziga o‘sha shovqin egar nuqtalardan va tor minimumlardan chiqishga yordam beradi; u o‘qitishni yaxshiroq umumlashtiradigan yassiroq minimumlarga siljitishi haqida kuzatishlar bor."),
        ("deep", "Batch o‘lchamini chiziqli masshtablash qoidasi", [
            ("p", "Batch $k$ marta kattalashsa, shovqin dispersiyasi $k$ marta kamayadi, lekin davrdagi qadamlar $k$ marta kamroq bo‘ladi. Goyal va hammualliflar (2017) bir vaqtda $\\eta$ ni ham $k$ marta oshirishni taklif qilishdi: ResNet-50 ImageNet’da 8192 lik batch bilan bir soatda aniqlikni yo‘qotmasdan shunday o‘qitilgan. Qoida qandaydir «kritik» batch o‘lchamigacha ishlaydi va qizdirishni (warmup) — dastlabki davrlarda $\\eta$ ning silliq o‘sishini talab qiladi."),
        ]),
    ]),
    dict(id="momentum", title="Momentum: og‘ir shar inersiyasi", blocks=[
        ("p", "Gradiyentli tushish — massasiz nuqta: har lahzada u aynan qiyalik ko‘rsatgan tomonga boradi. B. T. Polyak (1964) unga massa berishni taklif qildi. Og‘ir shar tezlik to‘plab dumalaydi va har bir do‘nglikka javob bermaydi. Formulada tezlik — $u$ vektor:"),
        ("eq", r"u_t=\beta\,u_{t-1}+g_t,\qquad \theta_t=\theta_{t-1}-\eta\,u_t"),
        ("symbols", [
            (r"u_t", "to‘plangan yo‘nalish (inersiya buferi), $u_0=0$;"),
            (r"\beta", "inersiya koeffitsiyenti, $0\\le\\beta&lt;1$, odatda $0{,}9$; $\\beta=0$ da oddiy SGD."),
        ]),
        ("p", "Rekursiyani ochamiz: $u_t=g_t+\\beta g_{t-1}+\\beta^2 g_{t-2}+\\dots$ — barcha o‘tgan gradiyentlarning eksponensial kamayuvchi vaznli yig‘indisi. Agar gradiyentlar qadamdan qadamga bir tomonni ko‘rsatsa, ular qo‘shiladi va qadam $\\eta/(1-\\beta)$ gacha o‘sadi — $\\beta=0{,}9$ da 10 marta. Agar ishora sakrab tursa (jarlik bo‘ylab zigzag), qo‘shiluvchilar bir-birini so‘ndiradi."),
        ("viz", "sgd-ema", {"beta": 0.9}, "<b>3-rasm.</b> Chapda — $k$ qadam oldingi gradiyent $u_t$ ga qanday vazn bilan kirishi; yorqin ustunlar — birgalikda umumiy vaznning kamida yarmini beradigan eng so‘nggi gradiyentlar. O‘ngda — $u_t$ ning o‘zgarmas $g=1$ gradiyentga javobi: u $1/(1-\\beta)=10$ ga intiladi va 22-qadamda limitning $90\\%$ iga yetadi. $\\beta=0{,}9$ da vaznning yarmi oxirgi 7 ta gradiyentga, $\\beta=0{,}99$ da oxirgi 69 tasiga to‘g‘ri keladi, xotira oynasi esa 100 qadam."),
        ("callout", "note", "Bitta inersiyaning ikki yozuvi", "PyTorch bu yerdagidek $u_t=\\beta u_{t-1}+g_t$ deb yozadi. Eksponensial sirpanuvchi o‘rtacha (exponential moving average, EMA) $m_t=\\beta m_{t-1}+(1-\\beta)g_t$ ham tez-tez uchraydi: u $\\eta$ ga o‘tib ketadigan $1-\\beta$ o‘zgarmas ko‘paytuvchi bilan farq qiladi. Aynan EMA <a href=\"../adam/\">Adam</a> suratida turadi. Rasmda shaklni almashtiring: EMA 1 emas, $0{,}1$ dan boshlanadi va haqiqiy qiymatga asta-sekin yetadi — dastlabki qadamlardagi bu kam baholash Adam’dagi siljishni tuzatishning sababi."),
        ("h3", "Nega inersiya tezlashtiradi: kvadratik funksiyadagi nazariya"),
        ("p", "Egriligi $L$ bo‘lgan bitta yo‘nalishni olamiz va $h=\\eta L$ deb belgilaymiz. $g_t=L\\theta_{t-1}$ ni qo‘yib, $u$ ni yo‘qotamiz (ikkinchi formuladan $\\eta u_{t-1}=\\theta_{t-2}-\\theta_{t-1}$). Ikkinchi tartibli chiziqli rekurrent munosabat hosil bo‘ladi:"),
        ("eq", r"\theta_t=(1+\beta-h)\,\theta_{t-1}-\beta\,\theta_{t-2}"),
        ("p", "Uning xatti-harakatini $\\lambda^2-(1+\\beta-h)\\lambda+\\beta=0$ xarakteristik tenglama ildizlari belgilaydi. Yaqinlashish tezligi — ildizlar modulining eng kattasi $\\rho$: xato taxminan $\\rho^t$ kabi kamayadi."),
        ("viz", "sgd-momentum", {"h": 0.04, "beta": 0.9}, "<b>4-rasm.</b> Chapda — $\\eta L$ (logarifmik shkala) va $\\beta$ bo‘yicha $\\rho$ tezlik xaritasi: ko‘k — tez yaqinlashish, qizil — uzoqlashish, uzluksiz chiziq — $\\rho=1$ chegarasi, shtrixlar — kritik so‘nish. Ko‘k nuqtani torting. O‘ngda — xuddi shu $\\eta$ bilan SGD va inersiya uchun $\\theta_t$. $\\eta L=0{,}04$ da SGD’ga $|\\theta|&lt;10^{-3}$ gacha 170 qadam kerak ($\\rho=0{,}96$), $\\beta=0{,}9$ inersiyaga — tebranishlar bilan 130 qadam, xuddi shu $\\beta$ bilan Nesterovga — 87, kritik so‘nish $\\beta=(1-\\sqrt{0{,}04})^2=0{,}64$ esa 41 qadam beradi ($\\rho=0{,}8$)."),
        ("deep", "Keltirib chiqarish: barqarorlik sohasi va optimal inersiya", [
            ("p", "Ildizlar $(1+\\beta-h)^2&lt;4\\beta$ da, ya’ni $(1-\\sqrt\\beta)^2&lt;h&lt;(1+\\sqrt\\beta)^2$ da kompleks. Ildizlar ko‘paytmasi $\\beta$ ga teng, shuning uchun $|\\lambda_1|=|\\lambda_2|=\\sqrt\\beta$: $\\theta_t$ tebranadi va har qadamda $h$ dan qat’i nazar $\\sqrt\\beta$ marta so‘nadi. Bu polosadan tashqarida ildizlar haqiqiy. Ikkala holat birgalikda aniq barqarorlik sohasini beradi (kvadrat uchhad uchun Shur — Kon shartlari):"),
            ("eq", r"0<\eta L<2(1+\beta)"),
            ("p", "— inersiya ruxsat etilgan qadamni deyarli ikki barobar kengaytiradi (SGD’da $\\eta L&lt;2$)."),
            ("p", "Egriliklar $[\\mu;\\,L]$ kesmani to‘ldirsin, $\\kappa=L/\\mu$. $\\eta$ va $\\beta$ ni ikkala chekka kompleks polosa chegaralariga tushadigan qilib tanlaymiz: $(1-\\sqrt\\beta)^2=\\eta\\mu$ va $(1+\\sqrt\\beta)^2=\\eta L$. U holda barcha yo‘nalishlar bir xil tez so‘nadi:"),
            ("eq", r"\eta=\frac{4}{(\sqrt L+\sqrt\mu)^2},\qquad \beta=\Bigl(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\Bigr)^2,\qquad \rho=\sqrt\beta=\frac{\sqrt\kappa-1}{\sqrt\kappa+1}"),
            ("p", "Eng yaxshi SGD bilan solishtiring: $\\rho=(\\kappa-1)/(\\kappa+1)$. $\\kappa=100$ da bu $0{,}818$ ga qarshi $0{,}980$: xatoni ming marta kamaytirish uchun 345 o‘rniga 35 ga yaqin qadam. Qadamlar soni $\\kappa$ kabi emas, $\\sqrt\\kappa$ kabi o‘sadi — og‘ir sharning tezlashuvi shunda."),
        ]),
        ("h3", "Nesterov: inersiya olib boradigan joydagi gradiyent"),
        ("p", "Yu. E. Nesterov (1983) gradiyentni joriy nuqtada emas, shar baribir inersiya bilan boradigan joyda hisoblashni taklif qildi. PyTorch shaklida (<code>nesterov=True</code>) bu qadamga tuzatma:"),
        ("eq", r"u_t=\beta u_{t-1}+g_t,\qquad \theta_t=\theta_{t-1}-\eta\,(g_t+\beta u_t)"),
        ("p", "Xarakteristik tenglama $\\lambda^2-(1+\\beta)(1-h)\\lambda+\\beta(1-h)=0$ ga aylanadi. Qiya yo‘nalishlarda tebranishlar tezroq so‘nadi ($\\sqrt\\beta$ o‘rniga $\\rho=\\sqrt{\\beta(1-h)}$), lekin barqarorlik sohasi torroq: $\\eta L&lt;2(1+\\beta)/(1+2\\beta)$, $\\beta=0{,}9$ da atigi $1{,}36$. Ikkala xususiyatni ko‘rish uchun 4-rasmni «Nesterov»ga o‘tkazing."),
    ]),
    dict(id="rmsprop", title="RMSProp: har bir vaznga o‘z qadami", blocks=[
        ("p", "SGD va Momentum’da barcha vaznlar uchun bitta $\\eta$ tezlik. Lekin turli vaznlar gradiyentlari tartiblar bilan farq qilishi mumkin: kam uchraydigan so‘zlar embeddinglari kamdan-kam katta turtki oladi, oxirgi qatlam siljishlari — doimiy kichiklarini. Umumiy $\\eta$ birlari uchun juda katta, boshqalari uchun juda kichik. RMSProp (J. Xinton, Coursera’dagi kurs ma’ruzalari, 2012) har bir vazn qadamini uning odatiy gradiyent kattaligiga bo‘ladi:"),
        ("eq", r"v_t=\beta\,v_{t-1}+(1-\beta)\,g_t^2,\qquad\theta_t=\theta_{t-1}-\eta\,\frac{g_t}{\sqrt{v_t}+\epsilon}"),
        ("symbols", [
            (r"g_t^2", "elementma-element kvadrat: har bir vaznning o‘z $v$ si bor;"),
            (r"v_t", "gradiyent kvadratining eksponensial sirpanuvchi o‘rtachasi — oxirgi $\\sim1/(1-\\beta)$ qadamdagi $\\mathbb E[g^2]$ bahosi, $v_0=0$;"),
            (r"\sqrt{v_t}", "gradiyentning o‘rta kvadratik qiymati (root mean square, RMS) — nom shundan;"),
            (r"\epsilon", "nolga bo‘lishdan saqlovchi kichik qo‘shimcha ($10^{-8}$)."),
        ]),
        ("p", "$\\sqrt{v_t}$ ga bo‘lish qadamni o‘lchamsiz qiladi: vaznning barcha gradiyentlarini 1000 ga ko‘paytirsangiz, $\\sqrt v$ ham 1000 marta o‘sadi va qadam o‘zgarmaydi. Odatiy qadam $\\eta$ tartibida bo‘ladi — endi tezlik qadam uzunligini to‘g‘ridan-to‘g‘ri vazn birliklarida belgilaydi."),
        ("viz", "sgd-rmsprop", {"beta": 0.9}, "<b>5-rasm.</b> Masshtabi o‘zgaradigan bitta vazn gradiyenti: 100-qadamda u 10 marta o‘sadi, 200-qadamda 100 marta tushadi. Yuqorida — $|g_t|$ va $\\sqrt{v_t}$, pastda — qadam uzunligi. SGD qadami gradiyent bilan birga ikki tartibga sakraydi, RMSProp qadami esa $\\eta=0{,}01$ tartibida qoladi. Lekin moslashuvda kechikish bor: o‘sishdan keyin qadam qisqa sakraydi ($\\beta=0{,}9$ da $0{,}032$ chegarada $0{,}030$ gacha), tushishdan keyin esa cho‘kadi — eski katta $v$ unutilishi uchun taxminan $\\ln10^4/\\ln(1/0{,}9)\\approx87$ qadam kerak."),
        ("callout", "key", "Ichki qadam chegarasi", "$v_t\\ge(1-\\beta)g_t^2$ dan $|g_t|/\\sqrt{v_t}\\le1/\\sqrt{1-\\beta}$ kelib chiqadi. RMSProp qadami hech qachon $\\eta/\\sqrt{1-\\beta}$ dan oshmaydi: $\\beta=0{,}9$ da $3{,}16\\,\\eta$ va $\\beta=0{,}99$ da $10\\,\\eta$. Bu SGD’da yo‘q bo‘lgan gradiyent portlashidan himoya."),
        ("deep", "RMSProp qayerdan: AdaGrad va Rprop", [
            ("p", "O‘tmishdoshi — AdaGrad (Duchi, Hazan, Singer, 2011): $v_t=v_{t-1}+g_t^2$, o‘rtacha o‘rniga yig‘indi. Siyrak belgili qavariq masalalar uchun u yaxshi, lekin neyron tarmoqlarda $v$ faqat o‘sadi va $\\eta/\\sqrt{v_t}$ qadam muqarrar ravishda nolgacha so‘nadi. RMSProp yig‘indini chekli xotirali eksponensial o‘rtacha bilan almashtirdi."),
            ("p", "Boshqa ildizi — faqat gradiyent ishorasidan foydalanadigan Rprop (Ridmiller va Braun, 1993). RMSProp’ni uning mini-batch’lar uchun varianti deb o‘qish mumkin: $\\beta=0$ da $v_t=g_t^2$ va $\\eta\\operatorname{sign}(g_t)$ qadam hosil bo‘ladi."),
            ("p", "Muhimi: RMSProp koordinata o‘qlarini masshtablaydi, lekin ularni burmaydi. Bu <b>diagonal</b> oldindan shartlash. Agar jarlik vaznlar orasida diagonal bo‘ylab ketsa, $\\sqrt v$ ga bo‘lish kam yordam beradi — bu 6-rasmda 45° burilishda ko‘rinadi."),
        ]),
    ]),
    dict(id="landscape", title="2D va 3D’dagi traektoriyalar", blocks=[
        ("p", "Uchala usulni bitta masalada solishtiramiz — cho‘ziq kvadratik vodiy $f=\\tfrac12(a^2+\\kappa b^2)$, bu yerda $a$ va $b$ — jarlik bo‘ylab va unga ko‘ndalang koordinatalar: ko‘ndalang egrilik bo‘ylamadagidan $\\kappa$ marta katta. Start — $a=-3{,}4$, $b=0{,}9$ nuqtada, u yerda $f=46{,}3$."),
        ("viz", "sgd-ravine", {"kappa": 100, "eta": 0.018, "beta": 0.9}, "<b>6-rasm.</b> $\\kappa=100$ li jarlik: yuqoridan ko‘rinish va 3D sirt (uni aylantirish mumkin). $\\eta=0{,}018$ da SGD jarlik bo‘ylab ko‘ndalang sakraydi ($\\eta\\lambda_{\\max}=1{,}8$) va uning bo‘ylab sekin sudraladi: 100 qadamda $f$ atigi $0{,}15$ gacha tushadi. $\\beta=0{,}9$ li Momentum $2{,}2\\cdot10^{-4}$ gacha, $\\eta=0{,}1$ li RMSProp $0{,}026$ gacha yetadi: u tubga tez tushadi, lekin keyin $\\eta$ tartibidagi qadam bilan titraydi. Jarlikni 45° ga buring: SGD va Momentum farqni sezmaydi, RMSProp esa ustunligini yo‘qotadi — $0{,}026$ o‘rniga $0{,}30$."),
        ("p", "Ikkinchi klassika — Rozenbrok funksiyasi $f=(1-x)^2+100(y-x^2)^2$: minimumi $(1;\\,1)$ da bo‘lgan tor egilgan «banan». Bu yerda egrilik nuqtadan nuqtaga o‘zgaradi va hech qanday o‘zgarmas qadam ideal emas."),
        ("viz", "sgd-rosenbrock", {}, "<b>7-rasm.</b> $(-1{,}5;\\,2)$ nuqtadan 3000 qadam — uni sudrab ko‘chirish mumkin. $\\eta=0{,}001$ li SGD faqat $f=0{,}049$ gacha yetadi. Xuddi shu $\\eta$ va $\\beta=0{,}9$ li Momentum bananni o‘tadi: 666-qadamda $f&lt;10^{-3}$ va oxirida $3\\cdot10^{-12}$. $\\eta=0{,}01$ li RMSProp $f\\approx0{,}02$ atrofida tiqilib qoladi: uning qadami tubda deyarli kamaymaydi. $t$ slayderi uchalasining istalgan paytdagi holatini ko‘rsatadi."),
        ("callout", "warn", "Xarita — hudud emas", "Ikki o‘lchamli rasmlar foydali, lekin aldamchi: haqiqiy tarmoqda millionlab o‘lchov bor, u yerdagi kritik nuqtalarning aksariyati lokal minimumlar emas, egar nuqtalar, yo‘qotish sirtining o‘zi esa mini-batch’ga bog‘liq. Rasmlardan optimizator tanlash uchun emas, mexanizmlar (zigzag, inersiya, masshtab) haqidagi intuitsiya uchun foydalaning."),
    ]),
    dict(id="code", title="Kodda: noldan va PyTorch’da", blocks=[
        ("p", "Uchala usul ikkita kichik sinfga sig‘adi. E’tibor bering: holat ($u$ yoki $v$) vaznlar bilan bir xil o‘lchamli massiv, shuning uchun Momentum va RMSProp parametrlar uchun xotirani ikki barobar, Adam esa uch barobar oshiradi."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "Izohlardagi sonlar 6-rasm bilan mos keladi, <code>torch.optim.SGD</code> va <code>torch.optim.RMSprop</code> esa xuddi shu masalada o‘sha qiymatlarni beradi. Xuddi shu $\\eta$ li Nesterov uzoqlashadi — aynan inersiya bo‘limidagi barqarorlik shartiga ko‘ra."),
        ("code", "python", "CODE_TORCH"),
        ("callout", "note", "Kutubxonalarda inersiyaning ikki shakli", "PyTorch xom gradiyentlar yig‘indisini saqlaydi va uni joriy $\\eta$ ga ko‘paytiradi: $\\theta\\leftarrow\\theta-\\eta_t u_t$. Keras va Sutskever va hammualliflarning (2013) klassik maqolasi esa o‘qitish tezligiga oldindan ko‘paytirilgan «siljish tezligi»ni (velocity) saqlaydi: $v_t=\\beta v_{t-1}-\\eta_t g_t$, $\\theta\\leftarrow\\theta+v_t$. O‘zgarmas $\\eta$ da shakllar teng kuchli, jadvalda esa — yo‘q: PyTorch’da yangi $\\eta$ darhol butun to‘plangan buferga qo‘llanadi."),
    ]),
    dict(id="practice", title="Giperparametrlar va amaliyot", blocks=[
        ("table", ["Parametr", "Odatiy qiymatlar", "Qanday tanlash"], [
            ["$\\eta$ (inersiyali SGD)", "$0{,}01$–$0{,}1$", "yo‘qotish hali barqaror tushadigan eng kattasi; ResNet: 256 lik batch’da $0{,}1$"],
            ["$\\beta$ (momentum)", "$0{,}9$, kamroq $0{,}95$–$0{,}99$", "katta $\\beta$ — uzunroq xotira va kuchliroq tezlashuv, lekin tebranish xavfi yuqoriroq"],
            ["RMSProp’ning $\\beta$ si (alpha)", "$0{,}9$–$0{,}99$", "o‘rtachalash oynasi $1/(1-\\beta)$: 10 dan 100 qadamgacha"],
            ["$\\eta$ (RMSProp)", "$10^{-4}$–$10^{-3}$", "vazn birliklarida $\\eta$ tartibidagi qadam"],
            ["$B$ (batch)", "32–512", "$B$ $k$ marta o‘ssa — $\\eta$ ham $k$ marta, qizdirish bilan"],
            ["weight decay", "$10^{-4}$–$5\\cdot10^{-4}$", "vaznlar so‘nishi; SGD uchun $L_2$-regulyarizatsiya bilan bir xil"],
        ], {}),
        ("ul", [
            "<b>Tezlik jadvali.</b> Pog‘onali (90 davrdan 30- va 60-davrlarda $0{,}1$ ga ko‘paytirish — ResNet klassikasi), kosinusli yoki «bir sikl». O‘zgarmas $\\eta$ minimum atrofida shovqin bulutini qoldiradi.",
            "<b>Qizdirish (warmup).</b> Dastlabki yuzlab–minglab qadamlarda $\\eta$ kichik qiymatdan chiziqli o‘sadi — ayniqsa katta batch’da muhim.",
            "<b>Gradiyentni norma bo‘yicha kesish</b> (gradient clipping) RNN va transformerlarda kamdan-kam uchraydigan ulkan gradiyentlardan himoya qiladi.",
            "<b>Tezlikni qidirish</b> (LR range test, L. Smit): eksponensial o‘suvchi $\\eta$ bilan qisqa yugurish; yo‘qotish o‘sa boshlagan joydan sezilarli kichik qiymat olinadi.",
            "Kirishlarni <b>normallashtirish</b>, batch-normallashtirish va oqilona initsializatsiya shartlanganlik sonini kamaytiradi va kattaroq $\\eta$ olishga imkon beradi.",
        ]),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b>Unutilgan <code>zero_grad()</code>.</b> PyTorch’da gradiyentlar <code>.grad</code> da to‘planadi; nolga tushirilmasa, $g_t$ barcha o‘tgan gradiyentlar yig‘indisiga aylanadi — bu inersiya emas, xato.",
            "<b>Juda katta tezlik</b>: yo‘qotish o‘sadi yoki NaN bo‘ladi. 1-rasmga ko‘ra $\\eta&lt;2/\\lambda_{\\max}$ kerak; avvalo $\\eta$ ni 3–10 marta kamaytiring.",
            "<b>$\\eta$ ni optimizatorlar orasida ko‘chirish.</b> $\\beta=0{,}9$ inersiyada barqaror qadam xuddi shu $\\eta$ li SGD’nikidan 10 marta katta. RMSProp va Adam’da $\\eta$ umuman boshqa birliklarda: ular uchun $10^{-3}$ — normal, SGD uchun odatda kam.",
            "<b>Tezlikni o‘zgartirmasdan batch’ni o‘zgartirish.</b> $B$ 8 marta oshirildi, $\\eta$ esa qoldi — tarmoq davr boshiga sekinroq o‘rganadi; $B$ kamaytirildi — shovqin o‘qitishni tebratib yuborishi mumkin.",
            "<b>Past aniqlikda $\\epsilon=10^{-8}$.</b> float16 da bu son nolgacha yaxlitlanadi va $v\\approx0$ da RMSProp qadami portlaydi; aralash aniqlikda $v$ float32 da saqlanadi yoki $\\epsilon$ kattaroq olinadi.",
            "<b>O‘qitish oxirigacha o‘zgarmas tezlik.</b> $\\eta$ pasaytirilmasa, SGD minimum atrofida titraydi va oxirgi davrlar deyarli hech narsa bermaydi.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘liqlik", blocks=[
        ("ul", [
            "<a href=\"../adam/\">Adam</a>: surat — EMA-inersiya, maxraj — RMSProp’dan $\\sqrt{v}$, ustiga siljishni tuzatish.",
            "<a href=\"../mse/\">MSE</a>: uning gradiyenti $\\frac2n\\sum_i(\\hat y_i-y_i)\\,x_i$ — 2 ko‘paytuvchi aniqligida 2-rasmdagi chiziqli regressiyadagi o‘sha $g_t$ (u yerda yo‘qotish — MSE ning yarmi).",
            "<a href=\"../bce/\">BCE</a> va <a href=\"../cross-entropy/\">kross-entropiya</a>: logitlar bo‘yicha $\\hat y-y$ gradiyent — tushish uchun eng oddiy signal.",
            "<a href=\"../sigmoid/\">Sigmoida</a>: to‘yinish juda kichik gradiyentlar beradi — SGD ularda deyarli turib qoladi, RMSProp esa qadamni cho‘zadi.",
            "<a href=\"../huber/\">Huber</a>: chetga chiqqan qiymatlar gradiyentini cheklaydi — gradiyentni kesishning qarindoshi.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) SGD: $\\theta_t=\\theta_{t-1}-\\eta g_t$, bu yerda $g_t$ — gradiyentning mini-batch bo‘yicha siljimagan bahosi; shovqin dispersiyasi $1/B$ kabi kamayadi. 2) Barqarorlik: $\\eta&lt;2/\\lambda_{\\max}$; tezlikni $\\kappa$ shartlanganlik soni belgilaydi — aniqlikning har bir tartibiga $\\kappa$ tartibidagi qadam. 3) Momentum $u_t=\\beta u_{t-1}+g_t$ — $1/(1-\\beta)$ oynali gradiyentlarning eksponensial xotirasi; kvadratik masalalarda yo‘lni $\\sqrt\\kappa$ tartibidagi qadamgacha qisqartiradi va barqarorlikni $\\eta L&lt;2(1+\\beta)$ gacha kengaytiradi. 4) RMSProp qadamni $\\sqrt{v_t}$ ga bo‘ladi: qadam o‘lchamsiz, $\\eta$ tartibida, lekin moslashuv faqat diagonal. 5) EMA-inersiya + RMSProp + siljishni tuzatish = Adam."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="$f(\\theta)=5\\theta^2$. Qanday o‘zgarmas $\\eta$ larda gradiyentli tushish yaqinlashadi?", options=["$\\eta&lt;0{,}1$", "$\\eta&lt;0{,}2$", "$\\eta&lt;0{,}4$", "$\\eta&lt;2$"], answer=1,
                 explain="Egrilik $f''=10$, $\\eta L&lt;2$ sharti $\\eta&lt;0{,}2$ ni beradi. $\\eta=0{,}1$ da minimumga bir qadamda yetiladi."),
            dict(q="$\\beta=0{,}95$ da inersiyaning xotira oynasi qancha?", options=["5 qadam", "20 qadam", "95 qadam", "$0{,}05$ qadam"], answer=1,
                 explain="$1/(1-\\beta)=1/0{,}05=20$."),
            dict(q="Batch 32 dan 128 ga oshirildi (ma’lumotlar $B$ dan ancha ko‘p). Stoxastik gradiyent dispersiyasi nima bo‘ladi?", options=["4 marta o‘sadi", "2 marta kamayadi", "4 marta kamayadi", "O‘zgarmaydi"], answer=2,
                 explain="$\\operatorname{Cov}[g]\\approx\\Sigma/B$: batch 4 marta o‘sdi — dispersiya 4 marta kamaydi (standart chetlanish esa 2 marta)."),
            dict(q="Bitta vaznning barcha gradiyentlari 100 ga ko‘paytirildi. $v$ barqarorlashgach, RMSProp qadami qanday o‘zgaradi ($\\epsilon$ hisobga olinmaganda)?", options=["100 marta o‘sadi", "10 marta o‘sadi", "O‘zgarmaydi", "100 marta kamayadi"], answer=2,
                 explain="$\\sqrt v$ ham 100 marta o‘sadi va $g/\\sqrt v$ nisbat o‘zgarmaydi."),
            dict(q="Nega inersiya cho‘ziq jarlik bo‘ylab tushishni tezlashtiradi?", options=["Jarlik bo‘ylab gradiyentlar mos va qo‘shiladi, ko‘ndalangiga ishora almashadi va ular bir-birini so‘ndiradi", "U funksiya egriligini kamaytiradi", "U ikkinchi hosilalarni hisoblaydi", "U qadamni $\\sqrt v$ ga bo‘ladi"], answer=0,
                 explain="$u_t$ — $\\beta^k$ vaznli o‘tgan gradiyentlar yig‘indisi: mos komponentlar $1/(1-\\beta)$ gacha o‘sadi, almashinuvchilari qisqaradi."),
        ]),
    ]),
],
}

# Fill in the shared code listings per language.
for _lang, _secs in SECTIONS.items():
    for _sec in _secs:
        for _i, _b in enumerate(_sec["blocks"]):
            if _b[0] == "code" and _b[2] in ("CODE_NUMPY", "CODE_TORCH"):
                _sec["blocks"][_i] = (_b[0], _b[1], _code(CODE_NUMPY if _b[2] == "CODE_NUMPY" else CODE_TORCH, _lang))
