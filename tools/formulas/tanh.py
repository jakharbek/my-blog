"""Formula page: tanh, the hyperbolic tangent. Format: see README.md, reference page: sigmoid.py."""

META = dict(
    id="tanh",
    date="2026-10-28",
    minutes=35,
    hero=r"\tanh(x)=\frac{e^{x}-e^{-x}}{e^{x}+e^{-x}}",
    title={"ru": "Tanh: гиперболический тангенс", "en": "Tanh: the hyperbolic tangent", "uz": "Tanh: giperbolik tangens"},
    dek={
        "ru": "S-образная функция, центрированная в нуле. Разбираем её по косточкам: из каких экспонент она собрана, почему это «растянутая сигмоида», откуда производная 1 − tanh², зачем нейрону центрированные выходы и что tanh делает с градиентом в глубоких и рекуррентных сетях.",
        "en": "An S-shaped function centred at zero. We take it apart bone by bone: which exponentials it is built from, why it is a “stretched sigmoid”, where the derivative 1 − tanh² comes from, why a neuron wants zero-centred outputs, and what tanh does to the gradient in deep and recurrent networks.",
        "uz": "Nol atrofida markazlashgan S-shaklli funksiya. Uni mayda detallarigacha tahlil qilamiz: qaysi eksponentalardan yig‘ilgan, nega u «cho‘zilgan sigmoida», 1 − tanh² hosila qayerdan keladi, neyronga nega markazlashgan chiqishlar kerak va tanh chuqur hamda rekurrent tarmoqlarda gradiyentga nima qiladi.",
    },
    description={
        "ru": "Tanh по косточкам: экспоненты, sinh и cosh, связь с сигмоидой, производная 1 − tanh², ряд Тейлора, центрированность, RNN и LSTM, устойчивый код.",
        "en": "Tanh in depth: exponentials, sinh and cosh, the link to the sigmoid, the derivative 1 − tanh², Taylor series, zero-centring, RNN and LSTM, stable code.",
        "uz": "Tanh batafsil: eksponentalar, sinh va cosh, sigmoida bilan bog‘lanish, 1 − tanh² hosila, Teylor qatori, markazlashganlik, RNN va LSTM, barqaror kod.",
    },
)

TABLE = [("-3", "-0.9951", "0.0099", "0.0474"), ("-2", "-0.9640", "0.0707", "0.1192"), ("-1", "-0.7616", "0.4200", "0.2689"),
         ("-0.5", "-0.4621", "0.7864", "0.3775"), ("0", "0.0000", "1.0000", "0.5000"), ("0.5", "0.4621", "0.7864", "0.6225"),
         ("1", "0.7616", "0.4200", "0.7311"), ("2", "0.9640", "0.0707", "0.8808"), ("3", "0.9951", "0.0099", "0.9526")]


def _table(lang):
    dec = "." if lang == "en" else ","
    m = lambda v: v.replace("-", "−").replace(".", dec)
    return [[m(c) for c in row] for row in TABLE]


CODE_NUMPY = '''import numpy as np

def tanh_grad_from_output(t):
    """Производная через уже посчитанный выход t = tanh(x): одно умножение."""
    return 1.0 - t * t

def tanh_grad(x):
    """sech²x = 4e^(−2|x|) / (1 + e^(−2|x|))²:
    без переполнения и без потери точности."""
    e = np.exp(-2.0 * np.abs(x))
    return 4.0 * e / (1.0 + e) ** 2

def naive_tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

print(naive_tanh(1000.0))       # nan: inf / inf (и предупреждение о переполнении)
print(np.tanh(1000.0))          # 1.0 — встроенная функция устойчива
print(1 - np.tanh(20.0) ** 2)   # 0.0: tanh(20) в float64 округляется до 1
print(tanh_grad(20.0))          # 1.6993417021166355e-17 — верное значение'''

CODE_TORCH = '''import torch
import torch.nn as nn

x = torch.tensor([-2.0, 0.0, 2.0], requires_grad=True)
y = torch.tanh(x)               # tensor([-0.9640,  0.0000,  0.9640])
y.sum().backward()
print(x.grad)                   # tensor([0.0707, 1.0000, 0.0707]) = 1 − tanh²

# Инициализация под tanh: усиление 5/3
layer = nn.Linear(256, 256)
nn.init.xavier_uniform_(layer.weight, gain=nn.init.calculate_gain("tanh"))

# Рекуррентная сеть с tanh и обрезка градиента от взрыва
rnn = nn.RNN(input_size=32, hidden_size=64, nonlinearity="tanh", batch_first=True)
out, h = rnn(torch.randn(8, 100, 32))   # 8 последовательностей длины 100
out.pow(2).mean().backward()
nn.utils.clip_grad_norm_(rnn.parameters(), max_norm=1.0)'''


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("Производная через уже посчитанный выход t = tanh(x): одно умножение.", "The derivative from the already computed output t = tanh(x): one multiplication."),
               ("без переполнения и без потери точности.", "no overflow and no loss of precision."),
               ("(и предупреждение о переполнении)", "(plus an overflow warning)"),
               ("встроенная функция устойчива", "the built-in function is stable"),
               ("tanh(20) в float64 округляется до 1", "tanh(20) rounds to 1 in float64"),
               ("верное значение", "the correct value"),
               ("Инициализация под tanh: усиление 5/3", "Initialization for tanh: gain 5/3"),
               ("Рекуррентная сеть с tanh и обрезка градиента от взрыва", "A recurrent network with tanh and gradient clipping against explosions"),
               ("8 последовательностей длины 100", "8 sequences of length 100")],
        "uz": [("Производная через уже посчитанный выход t = tanh(x): одно умножение.", "Hisoblangan chiqish t = tanh(x) orqali hosila: bitta ko‘paytirish."),
               ("без переполнения и без потери точности.", "to‘lib ketishsiz va aniqlik yo‘qotmasdan."),
               ("(и предупреждение о переполнении)", "(va to‘lib ketish haqida ogohlantirish)"),
               ("встроенная функция устойчива", "o‘rnatilgan funksiya barqaror"),
               ("tanh(20) в float64 округляется до 1", "float64 da tanh(20) 1 gacha yaxlitlanadi"),
               ("верное значение", "to‘g‘ri qiymat"),
               ("Инициализация под tanh: усиление 5/3", "tanh uchun initsializatsiya: kuchaytirish 5/3"),
               ("Рекуррентная сеть с tanh и обрезка градиента от взрыва", "tanh’li rekurrent tarmoq va portlashga qarshi gradiyentni kesish"),
               ("8 последовательностей длины 100", "uzunligi 100 bo‘lgan 8 ta ketma-ketlik")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем он нужен", blocks=[
        ("p", r"Сигмоида превращает число в долю от 0 до 1. Но внутри сети нам часто нужна не доля, а <i>сигнал со знаком</i>: «больше обычного» или «меньше обычного», «усилить» или «ослабить». Гиперболический тангенс (hyperbolic tangent) — это та же плавная S-кривая, но с выходом в интервале $(-1;\,1)$ и центром в нуле."),
        ("p", r"Где он встречается:"),
        ("ul", [
            r"<b>рекуррентные сети</b> — в простой RNN $h_t=\tanh(Wh_{t-1}+Ux_t+b)$, в LSTM и GRU tanh формирует кандидата в память, а в LSTM ещё и ограничивает выход ячейки;",
            r"<b>скрытые слои классических сетей</b> — до эпохи ReLU tanh был стандартом и до сих пор хорош в маленьких сетях и физически информированных моделях (PINN), где нужна гладкость;",
            r"<b>выход генератора</b> — если картинки нормированы в $[-1;\,1]$, последний слой генератора GAN (например, DCGAN) берёт tanh;",
            r"<b>ограничение действий и логитов</b> — в обучении с подкреплением (SAC) действие сжимают в $(-1;\,1)$ через tanh, а в Gemma 2 логиты «мягко обрезают»: $c\cdot\tanh(z/c)$;",
            r"<b>внутри других активаций</b> — популярное приближение <a href='../gelu/'>GELU</a> записано через tanh.",
        ]),
        ("callout", "key", "Главное за минуту", r"$\tanh$ сжимает всю числовую прямую в $(-1;\,1)$, проходит через начало координат и нечётна: $\tanh(-x)=-\tanh x$. Это растянутая сигмоида: $\tanh x=2\sigma(2x)-1$. Производная $1-\tanh^2x$ не больше 1 — в 4 раза больше максимума сигмоиды, — но на хвостах tanh так же насыщается, и градиент гаснет."),
    ]),
    dict(id="intuition", title="Интуиция: сигмоида, поставленная на ноль", blocks=[
        ("p", r"Представьте регулятор громкости со знаком: ноль — тишина, вправо — громче, влево — громче в противофазе. Пока вы крутите возле нуля, выход послушно следует за входом: $\tanh x\approx x$. Чем дальше, тем туже ход: выход упирается в $\pm1$ и больше не растёт. Это <b>насыщение</b> (saturation)."),
        ("p", r"Потяните точку. Оранжевая прямая — касательная, её наклон и есть производная. Серый пунктир — сигмоида: та же форма, но сдвинута вверх, вдвое ниже и вчетверо положе."),
        ("viz", "tanh-explorer", {"x": 1}, r"<b>Рисунок 1.</b> tanh, его касательная и производная (снизу). Тяните синюю точку или нажимайте стрелки, когда она в фокусе. Максимум производной — $1$ при $x=0$, у сигмоиды он равен $0{,}25$. При $x=1$: $\tanh 1=0{,}7616$, $\tanh' 1=0{,}4200$."),
        ("callout", "intuition", "Что заметить", r"При $x=2$ tanh уже $0{,}964$, а производная — $0{,}071$, в 14 раз меньше, чем в центре. При $|x|&gt;2{,}99$ производная падает ниже $0{,}01$: дальше вход растёт, а выход почти стоит на месте."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", r"В формуле две экспоненты: растущая $e^{x}$ и убывающая $e^{-x}$. Числитель — их разность, знаменатель — сумма. Половины этих выражений имеют собственные имена — гиперболический синус и косинус:"),
        ("eq", r"\begin{aligned}\sinh x&=\frac{e^{x}-e^{-x}}{2}\\[4pt]\cosh x&=\frac{e^{x}+e^{-x}}{2}\\[4pt]\tanh x&=\frac{\sinh x}{\cosh x}\end{aligned}"),
        ("symbols", [
            (r"e^{x}-e^{-x}", r"разность нечётна: при замене $x\to-x$ меняет знак; при $x&gt;0$ положительна;"),
            (r"e^{x}+e^{-x}", r"сумма всегда положительна и не меньше 2 — знаменатель никогда не обращается в ноль;"),
            (r"|\sinh x|<\cosh x", r"разность по модулю всегда меньше суммы, поэтому $|\tanh x|&lt;1$;"),
            (r"x\to\pm\infty", r"одна из экспонент становится пренебрежимо малой, и дробь стремится к $\pm1$."),
        ]),
        ("p", r"Умножив числитель и знаменатель на $e^{x}$ или на $e^{-x}$, получим формы, удобные для вычислений, а последняя форма связывает tanh с сигмоидой:"),
        ("eq", r"\begin{aligned}\tanh x&=\frac{e^{2x}-1}{e^{2x}+1}=\frac{1-e^{-2x}}{1+e^{-2x}}\\[4pt]&=2\sigma(2x)-1\end{aligned}"),
        ("viz", "tanh-construction", {"x": 1, "t": 3}, r"<b>Рисунок 2.</b> Слева: $\sinh$ и $\cosh$ — полусумма и полуразность экспонент; tanh — их отношение. При $x_0=1$: $\sinh 1=1{,}175$, $\cosh 1=1{,}543$, отношение $0{,}7616=\tanh 1$. Справа: нажмите «Пуск» — сигмоида за три шага превращается в tanh: сжимаем по горизонтали в 2 раза, растягиваем по вертикали в 2 раза, опускаем на 1."),
        ("table", ["$x$", r"$\tanh x$", r"$\tanh' x$", r"$\sigma(x)$"], "TABLE", {"num": [0, 1, 2, 3]}),
        ("p", r"Таблица показывает нечётность: $\tanh(-x)=-\tanh x$, а производная — чётная функция. Рядом для сравнения сигмоида: её значения симметричны не относительно нуля, а относительно $0{,}5$."),
    ]),
    dict(id="properties", title="Свойства и форма", blocks=[
        ("ul", [
            r"<b>Область определения</b> — все действительные числа; <b>область значений</b> — открытый интервал $(-1;\,1)$: значения $\pm1$ не достигаются.",
            r"<b>Нечётность</b>: $\tanh(-x)=-\tanh x$, график симметричен относительно начала координат, $\tanh 0=0$.",
            r"<b>Монотонность</b>: строго возрастает, потому что $\tanh' x=1-\tanh^2x&gt;0$ при любом $x$.",
            r"<b>Асимптоты</b>: $\lim_{x\to\pm\infty}\tanh x=\pm1$.",
            r"<b>Точка перегиба</b> — единственная, $x=0$: при $x&lt;0$ функция выпукла вниз, при $x&gt;0$ — вверх.",
            r"<b>Липшицевость с константой 1</b>: $|\tanh a-\tanh b|\le|a-b|$; в частности, $|\tanh x|\le|x|$, равенство только при $x=0$.",
            r"<b>Почти тождество около нуля</b>: $\tanh x=x-\tfrac{x^3}{3}+\dots$ — при малых весах сеть из tanh ведёт себя почти как линейная.",
        ]),
        ("deep", "Почему tanh x = 2σ(2x) − 1", [
            ("p", r"Подставим определение сигмоиды $\sigma(u)=1/(1+e^{-u})$ при $u=2x$:"),
            ("eq", r"2\sigma(2x)-1=\frac{2}{1+e^{-2x}}-\frac{1+e^{-2x}}{1+e^{-2x}}=\frac{1-e^{-2x}}{1+e^{-2x}}=\frac{e^{x}-e^{-x}}{e^{x}+e^{-x}}=\tanh x"),
            ("p", r"В предпоследнем шаге числитель и знаменатель умножены на $e^{x}$. Обратно: $\sigma(x)=\tfrac12\bigl(1+\tanh\tfrac x2\bigr)$. Значит, сеть со скрытыми tanh можно переписать в сеть со скрытыми сигмоидами той же выразительности — меняются только масштабы весов и сдвиги. Разница — в том, как идёт обучение (раздел о центрированности)."),
        ]),
        ("deep", "Обратная функция и формула сложения", [
            ("p", r"Решим $y=\tanh x$ относительно $x$: из $y=\frac{e^{2x}-1}{e^{2x}+1}$ получаем $e^{2x}=\frac{1+y}{1-y}$, откуда"),
            ("eq", r"\operatorname{artanh}y=\frac12\ln\frac{1+y}{1-y},\qquad -1<y<1"),
            ("p", r"Например, $\operatorname{artanh}0{,}5\approx0{,}549$. Ещё одно полезное тождество — формула сложения:"),
            ("eq", r"\tanh(a+b)=\frac{\tanh a+\tanh b}{1+\tanh a\,\tanh b}"),
            ("p", r"Это ровно релятивистское сложение скоростей (в долях скорости света): $0{,}5c$ и $0{,}5c$ дают не $c$, а $\frac{0{,}5+0{,}5}{1+0{,}25}c=0{,}8c$. Сумма двух чисел из $(-1;\,1)$ «в мире tanh» никогда не выходит за его пределы."),
        ]),
        ("h3", "Мягкий ограничитель: c · tanh(x / c)"),
        ("p", r"Функция $c\tanh(x/c)$ около нуля почти не меняет вход ($\approx x$), а большие значения плавно прижимает к $\pm c$. В отличие от жёсткой обрезки $\operatorname{clip}(x,-c,c)$, у неё нет изломов и производная нигде не обнуляется скачком. Так в Gemma 2 ограничивают логиты внимания ($c=50$) и итоговые логиты ($c=30$), чтобы они не разрастались во время обучения."),
    ]),
    dict(id="derivative", title="Производная: tanh′ = 1 − tanh²", blocks=[
        ("p", r"Главная формула страницы. Выведем её тремя способами — каждый пригодится в другом месте."),
        ("deep", "Способ 1. Производная частного", [
            ("p", r"Пусть $u=e^{x}-e^{-x}$, $v=e^{x}+e^{-x}$. Тогда $u'=v$ и $v'=u$, и по правилу дифференцирования дроби:"),
            ("eq", r"\tanh' x=\frac{u'v-uv'}{v^{2}}=\frac{v^{2}-u^{2}}{v^{2}}=1-\Bigl(\frac{u}{v}\Bigr)^{2}=1-\tanh^{2}x"),
        ]),
        ("deep", "Способ 2. Через основное гиперболическое тождество", [
            ("p", r"Для гиперболических функций $\cosh^2x-\sinh^2x=1$ (проверьте подстановкой экспонент), $\sinh' x=\cosh x$ и $\cosh' x=\sinh x$. Тогда"),
            ("eq", r"\tanh' x=\frac{\cosh x\cdot\cosh x-\sinh x\cdot\sinh x}{\cosh^{2}x}=\frac{1}{\cosh^{2}x}=\operatorname{sech}^{2}x"),
            ("p", r"Деля тождество на $\cosh^2x$, получаем $1-\tanh^2x=\operatorname{sech}^2x$ — та же формула в другой записи. Форма через $\operatorname{sech}^2$ полезна в коде при больших $|x|$."),
        ]),
        ("deep", "Способ 3. Через сигмоиду", [
            ("p", r"Из $\tanh x=2\sigma(2x)-1$ по правилу цепочки:"),
            ("eq", r"\tanh' x=2\cdot\sigma'(2x)\cdot2=4\sigma(2x)\bigl(1-\sigma(2x)\bigr)"),
            ("p", r"Отсюда сразу видно, почему максимум производной равен $4\cdot\tfrac14=1$, а не $\tfrac14$, как у сигмоиды: вдвое больший размах выхода и вдвое более сжатая шкала входа дают множитель 4."),
        ]),
        ("eq", r"\tanh' x=1-\tanh^{2}x"),
        ("p", r"На практике: на прямом проходе сеть уже посчитала $t=\tanh z$. На обратном проходе производная обходится одним умножением $1-t^2$ — без новых экспонент. Именно поэтому фреймворки хранят для обратного прохода выход tanh, а не его вход."),
        ("h3", "Вторая производная и самые крутые изгибы"),
        ("p", r"Дифференцируя ещё раз: $\tanh'' x=-2\tanh x\,(1-\tanh^2x)$. Она равна нулю только при $x=0$ (точка перегиба), а экстремумы достигаются при $\tanh^2x=\tfrac13$, то есть $x=\pm\operatorname{artanh}\tfrac{1}{\sqrt3}\approx\pm0{,}658$; значения там $\mp\tfrac{4}{3\sqrt3}\approx\mp0{,}770$. В этих точках наклон уже $1-\tfrac13=\tfrac23$ и убывает быстрее всего: здесь прямая $y\approx x$ сменяется изгибом к насыщению."),
        ("h3", "Ряд Тейлора около нуля"),
        ("eq", r"\tanh x=x-\frac{x^{3}}{3}+\frac{2x^{5}}{15}-\frac{17x^{7}}{315}+\frac{62x^{9}}{2835}-\dots,\qquad |x|<\frac{\pi}{2}"),
        ("p", r"Ряд сходится только при $|x|&lt;\pi/2\approx1{,}571$: знаменатель $\cosh x$ обращается в ноль в комплексных точках $x=\pm i\pi/2$, и радиус сходимости равен расстоянию до ближайшей из них. Это в два раза меньше, чем у сигмоиды ($\pi$), — ведь tanh «сжат» по горизонтали в 2 раза."),
        ("viz", "tanh-taylor", {"order": 3, "x": 1}, r"<b>Рисунок 3.</b> Многочлены Тейлора порядков 1–9 и полоса сходимости $|x|&lt;\pi/2$. При $x=1$ приближение 3-го порядка даёт $0{,}6667$ вместо $0{,}7616$, а 9-го — $0{,}7679$. При $x=2$, за пределами полосы, многочлены расходятся: 3-й порядок даёт $-0{,}667$, 9-й — уже $7{,}889$."),
    ]),
    dict(id="centered", title="Центрированность: почему tanh учится лучше сигмоиды", blocks=[
        ("p", r"Рассмотрим нейрон следующего слоя: $z=\sum_i w_ia_i+b$, где $a_i$ — выходы предыдущего слоя. Градиент потери по весу равен"),
        ("eq", r"\frac{\partial L}{\partial w_i}=\delta\cdot a_i,\qquad \delta=\frac{\partial L}{\partial z}"),
        ("p", r"Если все $a_i&gt;0$ (выходы сигмоиды), то на одном примере <b>все компоненты градиента имеют один знак</b> — знак $\delta$. Шаг SGD двигает все веса нейрона либо вверх, либо вниз. А если к оптимуму нужно одни веса увеличить, а другие уменьшить, остаётся идти зигзагом."),
        ("p", r"Второй взгляд — через форму поверхности потерь. Для линейного нейрона с квадратичной потерей $\tfrac12(w^\top a-y)^2$ матрица Гессе равна $\mathbb E[aa^\top]=\operatorname{Cov}(a)+\mu\mu^\top$, где $\mu$ — среднее входов. Ненулевое среднее добавляет одно большое собственное значение вдоль $\mu$, и «долина» вытягивается. Для входов $\sigma(z)$ ниже собственные значения $0{,}034$ и $0{,}530$ (число обусловленности 15,5), для $\tanh(z)$ — $0{,}340$ и $0{,}415$ (1,22)."),
        ("viz", "tanh-zigzag", {"steps": 50}, r"<b>Рисунок 4.</b> Обучаем два веса $w=(w_1;\,w_2)$ линейного нейрона по 100 примерам; входы — $\sigma(z)$ слева и $\tanh(z)$ справа от одних и тех же случайных $z$. SGD с шагом $0{,}5$ стартует из $(-1;\,1)$ к $w^*=(1;\,-1)$. Слева каждый шаг направлен «вправо-вверх» или «влево-вниз» (бирюзовые квадранты), путь пилит вытянутую долину; справа путь тоже шумит (SGD берёт по одному примеру), но идёт к оптимуму без систематической «пилы». Через 50 шагов расстояние до оптимума $1{,}252$ против $0{,}000$; точность $0{,}1$ достигается за 194 шага против 21."),
        ("callout", "key", "Вывод", r"Центрированные активации делают поверхность потерь следующего слоя «круглее», и градиентный спуск идёт к минимуму прямее. Это одна из причин, по которым tanh в скрытых слоях обучается быстрее сигмоиды (ЛеКун и др., «Efficient BackProp», 1998). Та же идея лежит в основе нормализации входов и BatchNorm."),
    ]),
    dict(id="space", title="Tanh на плоскости: складки, гребни и холмы", blocks=[
        ("p", r"Нейрон с двумя входами считает $\tanh(w_1x_1+w_2x_2+b)$. На плоскости это <b>складка</b>: поверхность переходит от $-1$ к $+1$ поперёк прямой $w^\top x+b=0$ и не меняется вдоль неё. Сумма двух противоположных складок даёт <b>гребень</b>, а четыре складки и ещё один tanh на выходе — <b>холм</b>, отличный от $-1$ только в квадрате."),
        ("viz", "tanh-surface", {"mode": "four", "k": 2}, r"<b>Рисунок 5.</b> Маленькая сеть из tanh. «1 нейрон» — $\tanh(k(0{,}8x_1+0{,}6x_2))$; «2 нейрона» — $\tanh(k(x_1+1))-\tanh(k(x_1-1))-1$; «4 + выход» — сумма $s$ четырёх таких складок по $x_1$ и $x_2$, затем $\tanh(2(s-3))$. При $k=2$ на вершине холма $f(0;\,0)=0{,}937$, а вдали $f=-1{,}000$. Пунктир — прямые, на которых вход каждого скрытого нейрона равен нулю."),
        ("p", r"Так работает <b>теорема об универсальной аппроксимации</b> (Цыбенко, 1989; Хорник, 1991): сеть с одним скрытым слоем из достаточно большого числа нейронов с tanh приближает любую непрерывную функцию на ограниченном замкнутом множестве с любой точностью. Холмы складываются из складок, а из холмов можно собрать любой рельеф. Наш холм использует второй tanh на выходе ради наглядности, но теореме хватает и одного скрытого слоя с линейным выходом. Она говорит, что такие веса <i>существуют</i>, но не говорит, сколько нужно нейронов и найдёт ли их обучение."),
    ]),
    dict(id="training", title="Tanh в обучении: активации по слоям и подгонка кривой", blocks=[
        ("h3", "Что происходит с сигналом в глубокой сети"),
        ("p", r"Пусть веса слоя выбраны случайно с дисперсией $g^2/n$, где $n$ — число входов нейрона. Если $g$ мал, сигнал затухает от слоя к слою и tanh работает как почти линейная функция. Если $g$ велик, входы нейронов большие, и tanh уходит в насыщение: выходы прилипают к $\pm1$, производные почти нулевые."),
        ("viz", "tanh-layers", {"act": "tanh", "g": 1}, r"<b>Рисунок 6.</b> Случайная сеть из 10 слоёв по 100 нейронов, входы $N(0,1)$; на каждом слое — гистограмма 2000 активаций (20 примеров × 100 нейронов), оранжевая точка — среднее. tanh при $g=1$: среднее последнего слоя $0{,}013$, а разброс постепенно сжимается до $0{,}225$; при $g=0{,}5$ сигнал гаснет: разброс падает до $0{,}001$, при $g=3$ насыщена почти половина нейронов ($48\%$ значений с $|a|&gt;0{,}95$). При $g=5/3$ разброс держится около $0{,}65$, насыщено $10\%$. У сигмоиды среднее на каждом слое около $0{,}5$ ($0{,}516$ на последнем) — выходы не центрированы."),
        ("p", r"Поэтому для tanh берут инициализацию Глоро (Xavier), $\operatorname{Var}w=\frac{2}{n_\text{in}+n_\text{out}}$, а PyTorch советует умножать её на усиление $g=5/3$ (<code>calculate_gain('tanh')</code>): множитель компенсирует то, что tanh сжимает сигнал. Для квадратного слоя это ровно случай $g=5/3$ на рисунке 6."),
        ("h3", "Сеть из tanh подгоняет кривую"),
        ("p", r"Скрытый слой из $H$ нейронов и линейный выход: $\hat y(x)=\sum_{k=1}^{H}v_k\tanh(w_kx+b_k)+c$. Каждое слагаемое — «ступенька» с плавными краями; обучение двигает, растягивает и масштабирует ступеньки так, чтобы их сумма легла на данные."),
        ("viz", "tanh-fit", {"h": 5}, r"<b>Рисунок 7.</b> 40 точек $y=0{,}8\sin(2{,}2x)+0{,}3x$ с шумом ($\sigma=0{,}08$), полный градиент и <a href='../adam/'>Adam</a> с шагом $0{,}05$. Бирюзовые кривые — вклады отдельных нейронов, синяя — их сумма. С 5 нейронами MSE падает с $1{,}059$ до плато около $0{,}05$ (шаги 200–380), затем один из нейронов «находит свою роль»: к шагу 500 ошибка $0{,}006$, к шагу 800 — $0{,}0041$, на уровне шума ($0{,}08^2=0{,}0064$). С 3 нейронами сеть застревает около $0{,}11$ ($0{,}106$ к шагу 2000), с 8 — уже к шагу 400 достигает $0{,}0039$."),
        ("callout", "note", "Плато — это насыщение", r"Длинные плато на кривой потерь часто означают, что часть нейронов работает на плоских хвостах tanh: их производная мала, и градиент почти не сдвигает их параметры. Помогают нормализация входов, аккуратная инициализация и адаптивные оптимизаторы вроде Adam."),
    ]),
    dict(id="rnn", title="Tanh в рекуррентных сетях и LSTM", blocks=[
        ("p", r"Простая рекуррентная сеть обновляет состояние по одной и той же формуле на каждом шаге: $h_t=\tanh(Wh_{t-1}+Ux_t+b)$. Tanh здесь работает как предохранитель: каким бы длинным ни был текст, состояние остаётся в $(-1;\,1)$ и не «взрывается». Но за ограниченность приходится платить градиентом (множители перемножаются от $s=T$ слева до $s=t+1$ справа):"),
        ("eq", r"\frac{\partial h_T}{\partial h_t}=\prod_{s=t+1}^{T}\operatorname{diag}\bigl(1-h_s^{2}\bigr)\,W"),
        ("p", r"Каждый множитель содержит $1-h_s^2\le1$. Если веса малы, произведение затухает экспоненциально. Если веса велики, состояния прижимаются к $\pm1$, $1-h_s^2\to0$ — и градиент тоже гаснет. Выживает он только в узком окне между этими режимами. В многомерной RNN у границы этого окна градиент может и взрываться (Паскану и др., 2013), поэтому вместе с tanh применяют обрезку нормы градиента."),
        ("viz", "tanh-rnn", {"w": 1}, r"<b>Рисунок 8.</b> Скалярная RNN $h_t=\tanh(wh_{t-1}+x_t)$, 30 шагов, входы $x_t\sim N(0;\,0{,}2^2)$ (серые столбики). Снизу — $|\partial h_{30}/\partial h_t|$ в логарифмической шкале. При $w=1$ градиент от первого шага до последнего уменьшается до $3{,}1\cdot10^{-4}$; при $w=0{,}5$ — до $5{,}7\cdot10^{-11}$; при $w=1{,}2$ — $1{,}3\cdot10^{-3}$; а при $w=2$ и $w=3$, когда состояние насыщено, — до $7{,}2\cdot10^{-18}$ и $1{,}6\cdot10^{-38}$."),
        ("p", r"LSTM решает эту проблему отдельной «магистралью» — состоянием ячейки $c_t$, которое обновляется сложением, а не через tanh:"),
        ("eq", r"\begin{aligned}g_t&=\tanh\bigl(W_g[h_{t-1},x_t]+b_g\bigr)\\c_t&=f_t\odot c_{t-1}+i_t\odot g_t\\h_t&=o_t\odot\tanh(c_t)\end{aligned}"),
        ("p", r"Здесь $f_t,i_t,o_t\in(0;\,1)$ — вентили на <a href='../sigmoid/'>сигмоидах</a>, а tanh выполняет две роли: кандидат $g_t\in(-1;\,1)$ может и увеличить, и уменьшить память (сигмоида умела бы только добавлять), а $\tanh(c_t)$ ограничивает выход. Вдоль цепочки $c_{t-1}\to c_t$ градиент умножается на $f_t$ (если не учитывать зависимость вентилей от $h_{t-1}$), без множителя $\tanh'$, поэтому при $f_t\approx1$ он доходит до далёких шагов."),
        ("callout", "history", "Немного истории", r"Ян ЛеКун в 1998 году советовал масштабированный тангенс $1{,}7159\tanh(2x/3)$: он даёт $f(\pm1)=\pm1$ и почти единичную дисперсию выхода. LSTM (Хохрайтер и Шмидхубер, 1997) сделала tanh стандартом рекуррентных сетей на два десятилетия. В свёрточных сетях его вытеснил <a href='../relu/'>ReLU</a>: в статье об AlexNet (2012) четырёхслойная свёрточная сеть с ReLU достигла ошибки 25% на обучающей выборке CIFAR-10 в 6 раз быстрее такой же сети с tanh."),
    ]),
    dict(id="code", title="В коде: устойчиво и без сюрпризов", blocks=[
        ("p", r"Наивная формула через экспоненты при $x=1000$ вычисляет $e^{1000}=\infty$, и получается $\infty/\infty=\text{nan}$. Встроенные <code>np.tanh</code> и <code>torch.tanh</code> устойчивы: при $x\gtrsim19$ они возвращают ровно $1{,}0$ в float64. Но тогда $1-\tanh^2 x$ даёт ровно 0, хотя истинное значение при $x=20$ — около $1{,}7\cdot10^{-17}$. Если нужна производная на далёких хвостах, считайте её через $\operatorname{sech}^2$ в устойчивой форме."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Правило", r"Используйте встроенный tanh и автоматическое дифференцирование; на обратном проходе — формулу $1-t^2$ от сохранённого выхода. Для tanh-сетей — инициализация Глоро (Xavier) с усилением $5/3$, для RNN — обрезка нормы градиента."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            r"<b>tanh на выходе вместо сигмоиды для вероятности.</b> Выход tanh лежит в $(-1;\,1)$ и не является вероятностью. Для бинарной классификации нужна <a href='../sigmoid/'>сигмоида</a> и <a href='../bce/'>BCE</a>; tanh на выходе уместен, если цели нормированы в $[-1;\,1]$.",
            r"<b>Производная по входу вместо выхода.</b> Формула $1-t^2$ применяется к <i>выходу</i> $t=\tanh x$. Частая опечатка — $1-x^2$ от входа: при $x=2$ она даёт $-3$ вместо $0{,}071$.",
            r"<b>Ненормированные входы и крупные веса.</b> Если признаки порядка сотен или веса слишком велики, tanh с первых шагов насыщен и почти не учится. Стандартизируйте данные и берите инициализацию под tanh.",
            r"<b>«tanh решает проблему затухания».</b> Он лучше сигмоиды (производная до 1 и центрированность), но тоже насыщается. Для глубоких сетей — ReLU-семейство, нормализация и остаточные связи; для последовательностей — LSTM/GRU.",
            r"<b>Самописный tanh через exp.</b> Даёт nan при больших $|x|$. Пользуйтесь <code>np.tanh</code>, <code>torch.tanh</code>.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            r"<a href='../sigmoid/'>Сигмоида</a>: $\tanh x=2\sigma(2x)-1$ и $\sigma(x)=\tfrac12(1+\tanh\tfrac x2)$; производные связаны как $\tanh' x=4\sigma'(2x)$.",
            r"<a href='../relu/'>ReLU</a>: не насыщается при $x&gt;0$ и вытеснил tanh из глубоких свёрточных сетей.",
            r"<a href='../gelu/'>GELU</a>: популярное приближение $0{,}5x\bigl(1+\tanh\bigl(\sqrt{2/\pi}\,(x+0{,}044715x^3)\bigr)\bigr)$.",
            r"<a href='../silu/'>SiLU</a>: $x\sigma(x)=\tfrac x2\bigl(1+\tanh\tfrac x2\bigr)$ — та же S-кривая в роли «мягкого вентиля».",
            r"<a href='../mse/'>MSE</a>: естественная пара для выхода tanh при целях в $[-1;\,1]$.",
            r"<a href='../adam/'>Adam</a>: оптимизатор из рисунка 7; адаптивный шаг помогает проходить плато, созданные насыщением.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, r"1) $\tanh x=\frac{e^x-e^{-x}}{e^x+e^{-x}}=\frac{\sinh x}{\cosh x}=2\sigma(2x)-1$ отображает $\mathbb R$ в $(-1;\,1)$, нечётен и проходит через ноль. 2) $\tanh'=1-\tanh^2\le1$, максимум в нуле, на хвостах — насыщение. 3) Ряд Тейлора $x-\frac{x^3}{3}+\dots$ сходится при $|x|&lt;\pi/2$. 4) Центрированные выходы делают обучение следующего слоя быстрее, чем у сигмоиды. 5) Суммы tanh-складок приближают любую непрерывную функцию на компакте; инициализация — Глоро (Xavier) с усилением $5/3$. 6) В RNN tanh держит состояние ограниченным, но градиент через время гаснет — отсюда LSTM."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q=r"Известно, что $\tanh 0{,}5\approx0{,}462$. Чему равен $\tanh(-0{,}5)$?", options=[r"$0{,}538$", r"$-0{,}462$", r"$0{,}462$", r"$-0{,}538$"], answer=1,
                 explain=r"tanh нечётен: $\tanh(-x)=-\tanh x=-0{,}462$. Ответ $0{,}538=1-0{,}462$ — это симметрия сигмоиды, а не тангенса."),
            dict(q=r"Нейрон выдал $t=\tanh z=0{,}8$. Чему равна производная $\tanh' z$?", options=[r"$0{,}2$", r"$0{,}36$", r"$0{,}64$", r"$0{,}16$"], answer=1,
                 explain=r"$\tanh' z=1-t^2=1-0{,}64=0{,}36$. Экспоненту заново считать не нужно."),
            dict(q=r"Какое тождество верно?", options=[r"$\tanh x=\sigma(2x)-1$", r"$\tanh x=2\sigma(x)-1$", r"$\tanh x=2\sigma(2x)-1$", r"$\tanh x=\sigma(x)/2$"], answer=2,
                 explain=r"Сигмоиду сжимают в 2 раза по горизонтали, растягивают в 2 раза по вертикали и опускают на 1: $2\sigma(2x)-1$."),
            dict(q=r"Почему tanh в скрытых слоях обычно обучается быстрее сигмоиды?", options=[r"Он считается быстрее", r"Его выходы центрированы и производная до 1, а не до 0,25", r"Он не насыщается", r"У него нет производной в нуле"], answer=1,
                 explain=r"Центрированность делает поверхность потерь следующего слоя «круглее», а вчетверо больший максимум производной меньше ослабляет градиент. Насыщается tanh так же, как сигмоида."),
            dict(q=r"В RNN с tanh рекуррентный вес сделали очень большим. Что будет с градиентом через много шагов?", options=[r"Взорвётся: множители $|w|&gt;1$", r"Затухнет: состояния насытятся, и $1-h^2\to0$", r"Останется равным 1", r"Станет отрицательным"], answer=1,
                 explain=r"Каждый множитель равен $w(1-h_s^2)$. При большом $w$ состояние прижимается к $\pm1$, и $1-h_s^2$ становится очень мал — на рисунке 8 при $w=3$ градиент падает до $1{,}6\cdot10^{-38}$."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", r"The sigmoid turns a number into a share between 0 and 1. Inside a network, though, we often need not a share but a <i>signed signal</i>: “above normal” or “below normal”, “amplify” or “damp”. The hyperbolic tangent is the same smooth S-curve, but with outputs in $(-1,\,1)$ and its centre at zero."),
        ("p", r"Where it appears:"),
        ("ul", [
            r"<b>recurrent networks</b> — in a plain RNN $h_t=\tanh(Wh_{t-1}+Ux_t+b)$; in LSTM and GRU, tanh produces the candidate for the memory, and in LSTM it also bounds the cell’s output;",
            r"<b>hidden layers of classic networks</b> — before the ReLU era tanh was the standard, and it is still good in small networks and physics-informed models (PINN) where smoothness matters;",
            r"<b>a generator’s output</b> — if images are normalized to $[-1,\,1]$, the last layer of a GAN generator (DCGAN, for example) uses tanh;",
            r"<b>bounding actions and logits</b> — in reinforcement learning (SAC) actions are squashed into $(-1,\,1)$ with tanh, and Gemma 2 “soft-caps” its logits: $c\cdot\tanh(z/c)$;",
            r"<b>inside other activations</b> — the popular approximation of <a href='../gelu/'>GELU</a> is written through tanh.",
        ]),
        ("callout", "key", "The essentials in a minute", r"$\tanh$ squeezes the whole real line into $(-1,\,1)$, passes through the origin and is odd: $\tanh(-x)=-\tanh x$. It is a stretched sigmoid: $\tanh x=2\sigma(2x)-1$. Its derivative $1-\tanh^2x$ never exceeds 1 — four times the sigmoid’s maximum — but on the tails tanh saturates just the same, and the gradient fades."),
    ]),
    dict(id="intuition", title="Intuition: a sigmoid standing on zero", blocks=[
        ("p", r"Picture a volume knob with a sign: zero is silence, turning right makes it louder, turning left makes it louder in antiphase. As long as you stay near zero, the output faithfully follows the input: $\tanh x\approx x$. Further out the knob gets stiffer: the output runs into $\pm1$ and stops growing. This is <b>saturation</b>."),
        ("p", r"Drag the point. The orange line is the tangent; its slope is the derivative. The grey dashed curve is the sigmoid: the same shape, but shifted up, half as tall and four times flatter."),
        ("viz", "tanh-explorer", {"x": 1}, r"<b>Figure 1.</b> tanh, its tangent and its derivative (below). Drag the blue point, or use the arrow keys when it has focus. The maximum of the derivative is $1$ at $x=0$; for the sigmoid it is $0.25$. At $x=1$: $\tanh 1=0.7616$, $\tanh' 1=0.4200$."),
        ("callout", "intuition", "What to notice", r"At $x=2$ tanh is already $0.964$, while the derivative is only $0.071$, 14 times smaller than at the centre. For $|x|&gt;2.99$ the derivative drops below $0.01$: the input keeps growing while the output barely moves."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("p", r"The formula holds two exponentials: the growing $e^{x}$ and the decaying $e^{-x}$. The numerator is their difference, the denominator their sum. Halves of these expressions have names of their own — the hyperbolic sine and cosine:"),
        ("eq", r"\begin{aligned}\sinh x&=\frac{e^{x}-e^{-x}}{2}\\[4pt]\cosh x&=\frac{e^{x}+e^{-x}}{2}\\[4pt]\tanh x&=\frac{\sinh x}{\cosh x}\end{aligned}"),
        ("symbols", [
            (r"e^{x}-e^{-x}", r"the difference is odd: it changes sign under $x\to-x$; for $x&gt;0$ it is positive;"),
            (r"e^{x}+e^{-x}", r"the sum is always positive and at least 2 — the denominator never vanishes;"),
            (r"|\sinh x|<\cosh x", r"the difference is always smaller in absolute value than the sum, hence $|\tanh x|&lt;1$;"),
            (r"x\to\pm\infty", r"one of the exponentials becomes negligible, and the fraction tends to $\pm1$."),
        ]),
        ("p", r"Multiplying the numerator and the denominator by $e^{x}$ or by $e^{-x}$ gives forms convenient for computation, and the last form links tanh to the sigmoid:"),
        ("eq", r"\begin{aligned}\tanh x&=\frac{e^{2x}-1}{e^{2x}+1}=\frac{1-e^{-2x}}{1+e^{-2x}}\\[4pt]&=2\sigma(2x)-1\end{aligned}"),
        ("viz", "tanh-construction", {"x": 1, "t": 3}, r"<b>Figure 2.</b> Left: $\sinh$ and $\cosh$ are the half-difference and the half-sum of the exponentials; tanh is their ratio. At $x_0=1$: $\sinh 1=1.175$, $\cosh 1=1.543$, the ratio is $0.7616=\tanh 1$. Right: press “Play” — the sigmoid turns into tanh in three steps: squeeze it horizontally by 2, stretch it vertically by 2, lower it by 1."),
        ("table", ["$x$", r"$\tanh x$", r"$\tanh' x$", r"$\sigma(x)$"], "TABLE", {"num": [0, 1, 2, 3]}),
        ("p", r"The table shows the oddness, $\tanh(-x)=-\tanh x$, while the derivative is an even function. The sigmoid is listed for comparison: its values are symmetric not about zero but about $0.5$."),
    ]),
    dict(id="properties", title="Properties and shape", blocks=[
        ("ul", [
            r"<b>Domain</b>: all real numbers; <b>range</b>: the open interval $(-1,\,1)$ — the values $\pm1$ are never reached.",
            r"<b>Oddness</b>: $\tanh(-x)=-\tanh x$; the graph is symmetric about the origin, $\tanh 0=0$.",
            r"<b>Monotonicity</b>: strictly increasing, since $\tanh' x=1-\tanh^2x&gt;0$ for every $x$.",
            r"<b>Asymptotes</b>: $\lim_{x\to\pm\infty}\tanh x=\pm1$.",
            r"<b>Inflection point</b>: a single one, at $x=0$; the function is convex for $x&lt;0$ and concave for $x&gt;0$.",
            r"<b>Lipschitz with constant 1</b>: $|\tanh a-\tanh b|\le|a-b|$; in particular $|\tanh x|\le|x|$, with equality only at $x=0$.",
            r"<b>Almost the identity near zero</b>: $\tanh x=x-\tfrac{x^3}{3}+\dots$ — with small weights a tanh network behaves almost linearly.",
        ]),
        ("deep", "Why tanh x = 2σ(2x) − 1", [
            ("p", r"Substitute the definition of the sigmoid $\sigma(u)=1/(1+e^{-u})$ with $u=2x$:"),
            ("eq", r"2\sigma(2x)-1=\frac{2}{1+e^{-2x}}-\frac{1+e^{-2x}}{1+e^{-2x}}=\frac{1-e^{-2x}}{1+e^{-2x}}=\frac{e^{x}-e^{-x}}{e^{x}+e^{-x}}=\tanh x"),
            ("p", r"In the second-to-last step the numerator and the denominator are multiplied by $e^{x}$. Conversely, $\sigma(x)=\tfrac12\bigl(1+\tanh\tfrac x2\bigr)$. So a network with tanh hidden units can be rewritten as one with sigmoid hidden units of the same expressive power — only the weight scales and biases change. The difference lies in how training goes (see the section on centring)."),
        ]),
        ("deep", "The inverse function and the addition formula", [
            ("p", r"Solve $y=\tanh x$ for $x$: from $y=\frac{e^{2x}-1}{e^{2x}+1}$ we get $e^{2x}=\frac{1+y}{1-y}$, hence"),
            ("eq", r"\operatorname{artanh}y=\frac12\ln\frac{1+y}{1-y},\qquad -1<y<1"),
            ("p", r"For example, $\operatorname{artanh}0.5\approx0.549$. Another useful identity is the addition formula:"),
            ("eq", r"\tanh(a+b)=\frac{\tanh a+\tanh b}{1+\tanh a\,\tanh b}"),
            ("p", r"This is exactly the relativistic addition of velocities (as fractions of the speed of light): $0.5c$ and $0.5c$ give not $c$ but $\frac{0.5+0.5}{1+0.25}c=0.8c$. In the “world of tanh” the sum of two numbers from $(-1,\,1)$ never leaves it."),
        ]),
        ("h3", "A soft limiter: c · tanh(x / c)"),
        ("p", r"Near zero the function $c\tanh(x/c)$ barely changes its input ($\approx x$), while large values are smoothly pressed towards $\pm c$. Unlike the hard cut $\operatorname{clip}(x,-c,c)$, it has no kinks, and its derivative never drops to zero abruptly. Gemma 2 bounds its attention logits ($c=50$) and final logits ($c=30$) this way, so that they do not blow up during training."),
    ]),
    dict(id="derivative", title="The derivative: tanh′ = 1 − tanh²", blocks=[
        ("p", r"The key formula of the page. Let us derive it in three ways — each one is useful somewhere else."),
        ("deep", "Method 1. The quotient rule", [
            ("p", r"Let $u=e^{x}-e^{-x}$ and $v=e^{x}+e^{-x}$. Then $u'=v$ and $v'=u$, and by the quotient rule:"),
            ("eq", r"\tanh' x=\frac{u'v-uv'}{v^{2}}=\frac{v^{2}-u^{2}}{v^{2}}=1-\Bigl(\frac{u}{v}\Bigr)^{2}=1-\tanh^{2}x"),
        ]),
        ("deep", "Method 2. Through the fundamental hyperbolic identity", [
            ("p", r"For hyperbolic functions $\cosh^2x-\sinh^2x=1$ (check it by substituting the exponentials), $\sinh' x=\cosh x$ and $\cosh' x=\sinh x$. Then"),
            ("eq", r"\tanh' x=\frac{\cosh x\cdot\cosh x-\sinh x\cdot\sinh x}{\cosh^{2}x}=\frac{1}{\cosh^{2}x}=\operatorname{sech}^{2}x"),
            ("p", r"Dividing the identity by $\cosh^2x$ gives $1-\tanh^2x=\operatorname{sech}^2x$ — the same formula in another notation. The $\operatorname{sech}^2$ form is useful in code for large $|x|$."),
        ]),
        ("deep", "Method 3. Through the sigmoid", [
            ("p", r"From $\tanh x=2\sigma(2x)-1$ by the chain rule:"),
            ("eq", r"\tanh' x=2\cdot\sigma'(2x)\cdot2=4\sigma(2x)\bigl(1-\sigma(2x)\bigr)"),
            ("p", r"This shows at once why the maximum of the derivative is $4\cdot\tfrac14=1$ rather than $\tfrac14$ as for the sigmoid: twice the output range and a twice-compressed input scale give a factor of 4."),
        ]),
        ("eq", r"\tanh' x=1-\tanh^{2}x"),
        ("p", r"In practice: on the forward pass the network has already computed $t=\tanh z$. On the backward pass the derivative costs a single multiplication $1-t^2$ — no new exponentials. That is why frameworks keep the output of tanh, not its input, for the backward pass."),
        ("h3", "The second derivative and the sharpest bends"),
        ("p", r"Differentiating once more: $\tanh'' x=-2\tanh x\,(1-\tanh^2x)$. It vanishes only at $x=0$ (the inflection point), and its extrema are at $\tanh^2x=\tfrac13$, i.e. $x=\pm\operatorname{artanh}\tfrac{1}{\sqrt3}\approx\pm0.658$, with values $\mp\tfrac{4}{3\sqrt3}\approx\mp0.770$. At these points the slope is already $1-\tfrac13=\tfrac23$ and falls fastest: here the line $y\approx x$ gives way to the bend towards saturation."),
        ("h3", "The Taylor series around zero"),
        ("eq", r"\tanh x=x-\frac{x^{3}}{3}+\frac{2x^{5}}{15}-\frac{17x^{7}}{315}+\frac{62x^{9}}{2835}-\dots,\qquad |x|<\frac{\pi}{2}"),
        ("p", r"The series converges only for $|x|&lt;\pi/2\approx1.571$: the denominator $\cosh x$ vanishes at the complex points $x=\pm i\pi/2$, and the radius of convergence equals the distance to the nearest one. That is half the sigmoid’s radius ($\pi$), since tanh is squeezed horizontally by a factor of 2."),
        ("viz", "tanh-taylor", {"order": 3, "x": 1}, r"<b>Figure 3.</b> Taylor polynomials of orders 1–9 and the convergence band $|x|&lt;\pi/2$. At $x=1$ the third-order approximation gives $0.6667$ instead of $0.7616$, and the ninth-order one gives $0.7679$. At $x=2$, outside the band, the polynomials diverge: order 3 gives $-0.667$, order 9 already $7.889$."),
    ]),
    dict(id="centered", title="Zero-centring: why tanh trains better than the sigmoid", blocks=[
        ("p", r"Consider a neuron of the next layer: $z=\sum_i w_ia_i+b$, where $a_i$ are the outputs of the previous layer. The gradient of the loss with respect to a weight is"),
        ("eq", r"\frac{\partial L}{\partial w_i}=\delta\cdot a_i,\qquad \delta=\frac{\partial L}{\partial z}"),
        ("p", r"If all $a_i&gt;0$ (sigmoid outputs), then on a single example <b>all components of the gradient share one sign</b> — the sign of $\delta$. An SGD step moves all the neuron’s weights either up or down. If reaching the optimum requires raising some weights and lowering others, the only way is to zigzag."),
        ("p", r"A second view is through the shape of the loss surface. For a linear neuron with the squared loss $\tfrac12(w^\top a-y)^2$ the Hessian is $\mathbb E[aa^\top]=\operatorname{Cov}(a)+\mu\mu^\top$, where $\mu$ is the mean input. A non-zero mean adds one large eigenvalue along $\mu$, and the “valley” stretches. For the inputs $\sigma(z)$ below the eigenvalues are $0.034$ and $0.530$ (condition number 15.5); for $\tanh(z)$ they are $0.340$ and $0.415$ (1.22)."),
        ("viz", "tanh-zigzag", {"steps": 50}, r"<b>Figure 4.</b> We train the two weights $w=(w_1,\,w_2)$ of a linear neuron on 100 examples; the inputs are $\sigma(z)$ on the left and $\tanh(z)$ on the right, for the same random $z$. SGD with step $0.5$ starts at $(-1,\,1)$ and heads for $w^*=(1,\,-1)$. On the left every step points “up-right” or “down-left” (the teal quadrants), and the path saws across the elongated valley; on the right the path is noisy too (SGD takes one example at a time), but it heads for the optimum without the systematic sawing. After 50 steps the distance to the optimum is $1.252$ versus $0.000$; an accuracy of $0.1$ takes 194 steps versus 21."),
        ("callout", "key", "Takeaway", r"Zero-centred activations make the next layer’s loss surface “rounder”, and gradient descent heads for the minimum more directly. This is one reason tanh in hidden layers trains faster than the sigmoid (LeCun et al., “Efficient BackProp”, 1998). The same idea underlies input normalization and BatchNorm."),
    ]),
    dict(id="space", title="Tanh on the plane: folds, ridges and hills", blocks=[
        ("p", r"A neuron with two inputs computes $\tanh(w_1x_1+w_2x_2+b)$. On the plane this is a <b>fold</b>: the surface goes from $-1$ to $+1$ across the line $w^\top x+b=0$ and stays constant along it. The sum of two opposite folds gives a <b>ridge</b>, and four folds plus one more tanh at the output give a <b>hill</b> that differs from $-1$ only inside a square."),
        ("viz", "tanh-surface", {"mode": "four", "k": 2}, r"<b>Figure 5.</b> A small tanh network. “1 neuron” is $\tanh(k(0.8x_1+0.6x_2))$; “2 neurons” is $\tanh(k(x_1+1))-\tanh(k(x_1-1))-1$; “4 + output” is the sum $s$ of four such folds along $x_1$ and $x_2$, followed by $\tanh(2(s-3))$. At $k=2$ the top of the hill is $f(0,\,0)=0.937$, and far away $f=-1.000$. The dashed lines are where the input of each hidden neuron is zero."),
        ("p", r"This is how the <b>universal approximation theorem</b> works (Cybenko, 1989; Hornik, 1991): a network with one hidden layer of sufficiently many tanh neurons approximates any continuous function on a closed bounded set to any accuracy. Hills are made of folds, and any landscape can be made of hills. Our hill uses a second tanh at the output for clarity, but the theorem needs only one hidden layer with a linear output. It says such weights <i>exist</i>, but not how many neurons are needed or whether training will find them."),
    ]),
    dict(id="training", title="Tanh in training: activations through layers and curve fitting", blocks=[
        ("h3", "What happens to the signal in a deep network"),
        ("p", r"Let the weights of each layer be random with variance $g^2/n$, where $n$ is the number of inputs of a neuron. If $g$ is small, the signal fades from layer to layer and tanh acts almost linearly. If $g$ is large, the neurons’ inputs are large and tanh goes into saturation: outputs stick to $\pm1$ and the derivatives are almost zero."),
        ("viz", "tanh-layers", {"act": "tanh", "g": 1}, r"<b>Figure 6.</b> A random network of 10 layers of 100 neurons with inputs $N(0,1)$; each layer shows a histogram of 2000 activations (20 examples × 100 neurons), the orange point is the mean. tanh with $g=1$: the mean of the last layer is $0.013$, and the spread gradually shrinks to $0.225$; with $g=0.5$ the signal fades: the spread drops to $0.001$; with $g=3$ almost half the neurons are saturated ($48\%$ of values with $|a|&gt;0.95$). With $g=5/3$ the spread stays around $0.65$, with $10\%$ saturated. For the sigmoid the mean on every layer is about $0.5$ ($0.516$ on the last one) — the outputs are not centred."),
        ("p", r"Hence tanh layers use Glorot (Xavier) initialization, $\operatorname{Var}w=\frac{2}{n_\text{in}+n_\text{out}}$, and PyTorch recommends multiplying it by the gain $g=5/3$ (<code>calculate_gain('tanh')</code>): the factor compensates for tanh squeezing the signal. For a square layer this is exactly the case $g=5/3$ in Figure 6."),
        ("h3", "A tanh network fits a curve"),
        ("p", r"A hidden layer of $H$ neurons and a linear output: $\hat y(x)=\sum_{k=1}^{H}v_k\tanh(w_kx+b_k)+c$. Each term is a “step” with smooth edges; training moves, stretches and scales the steps until their sum lies on the data."),
        ("viz", "tanh-fit", {"h": 5}, r"<b>Figure 7.</b> 40 points of $y=0.8\sin(2.2x)+0.3x$ with noise ($\sigma=0.08$), full-batch gradients and <a href='../adam/'>Adam</a> with step $0.05$. The teal curves are the contributions of individual neurons, the blue one is their sum. With 5 neurons the MSE drops from $1.059$ to a plateau of about $0.05$ (steps 200–380); then one neuron “finds its role”: by step 500 the error is $0.006$, by step 800 $0.0041$, at the noise level ($0.08^2=0.0064$). With 3 neurons the network gets stuck at about $0.11$ ($0.106$ by step 2000); with 8 it reaches $0.0039$ by step 400."),
        ("callout", "note", "A plateau means saturation", r"Long plateaus on the loss curve often mean that some neurons work on the flat tails of tanh: their derivative is small, and the gradient barely moves their parameters. Input normalization, careful initialization and adaptive optimizers such as Adam help."),
    ]),
    dict(id="rnn", title="Tanh in recurrent networks and LSTM", blocks=[
        ("p", r"A plain recurrent network updates its state with the same formula at every step: $h_t=\tanh(Wh_{t-1}+Ux_t+b)$. Here tanh works as a fuse: however long the text, the state stays in $(-1,\,1)$ and does not “explode”. But boundedness is paid for with the gradient (the factors are multiplied from $s=T$ on the left to $s=t+1$ on the right):"),
        ("eq", r"\frac{\partial h_T}{\partial h_t}=\prod_{s=t+1}^{T}\operatorname{diag}\bigl(1-h_s^{2}\bigr)\,W"),
        ("p", r"Every factor contains $1-h_s^2\le1$. If the weights are small, the product decays exponentially. If the weights are large, the states are pressed against $\pm1$, $1-h_s^2\to0$ — and the gradient fades too. It survives only in a narrow window between these regimes. In a multidimensional RNN near the edge of this window the gradient can also explode (Pascanu et al., 2013), which is why tanh RNNs are trained with gradient-norm clipping."),
        ("viz", "tanh-rnn", {"w": 1}, r"<b>Figure 8.</b> A scalar RNN $h_t=\tanh(wh_{t-1}+x_t)$, 30 steps, inputs $x_t\sim N(0,\,0.2^2)$ (grey bars). Below: $|\partial h_{30}/\partial h_t|$ on a log scale. With $w=1$ the gradient from the first step to the last shrinks to $3.1\cdot10^{-4}$; with $w=0.5$ to $5.7\cdot10^{-11}$; with $w=1.2$ to $1.3\cdot10^{-3}$; and with $w=2$ and $w=3$, when the state is saturated, to $7.2\cdot10^{-18}$ and $1.6\cdot10^{-38}$."),
        ("p", r"LSTM solves this with a separate “highway” — the cell state $c_t$, which is updated by addition rather than through tanh:"),
        ("eq", r"\begin{aligned}g_t&=\tanh\bigl(W_g[h_{t-1},x_t]+b_g\bigr)\\c_t&=f_t\odot c_{t-1}+i_t\odot g_t\\h_t&=o_t\odot\tanh(c_t)\end{aligned}"),
        ("p", r"Here $f_t,i_t,o_t\in(0,\,1)$ are gates built on <a href='../sigmoid/'>sigmoids</a>, and tanh plays two roles: the candidate $g_t\in(-1,\,1)$ can both increase and decrease the memory (a sigmoid could only add), and $\tanh(c_t)$ bounds the output. Along the chain $c_{t-1}\to c_t$ the gradient is multiplied by $f_t$ (ignoring the dependence of the gates on $h_{t-1}$), with no $\tanh'$ factor, so with $f_t\approx1$ it reaches distant steps."),
        ("callout", "history", "A bit of history", r"In 1998 Yann LeCun recommended the scaled tangent $1.7159\tanh(2x/3)$: it gives $f(\pm1)=\pm1$ and an output variance close to one. LSTM (Hochreiter and Schmidhuber, 1997) made tanh the standard of recurrent networks for two decades. In convolutional networks it was displaced by <a href='../relu/'>ReLU</a>: in the AlexNet paper (2012) a four-layer convolutional network with ReLU reached 25% training error on CIFAR-10 six times faster than the same network with tanh."),
    ]),
    dict(id="code", title="In code: stable and without surprises", blocks=[
        ("p", r"The naive formula through exponentials computes $e^{1000}=\infty$ at $x=1000$, and the result is $\infty/\infty=\text{nan}$. The built-in <code>np.tanh</code> and <code>torch.tanh</code> are stable: for $x\gtrsim19$ they return exactly $1.0$ in float64. But then $1-\tanh^2 x$ gives exactly 0, although the true value at $x=20$ is about $1.7\cdot10^{-17}$. If you need the derivative on the far tails, compute it through $\operatorname{sech}^2$ in a stable form."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "The rule", r"Use the built-in tanh and automatic differentiation; on the backward pass, the formula $1-t^2$ from the stored output. For tanh networks, Glorot (Xavier) initialization with gain $5/3$; for RNNs, gradient-norm clipping."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            r"<b>tanh at the output instead of the sigmoid for a probability.</b> The output of tanh lies in $(-1,\,1)$ and is not a probability. Binary classification needs the <a href='../sigmoid/'>sigmoid</a> and <a href='../bce/'>BCE</a>; tanh at the output is appropriate when the targets are scaled to $[-1,\,1]$.",
            r"<b>The derivative of the input instead of the output.</b> The formula $1-t^2$ applies to the <i>output</i> $t=\tanh x$. A common slip is $1-x^2$ of the input: at $x=2$ it gives $-3$ instead of $0.071$.",
            r"<b>Unnormalized inputs and large weights.</b> If the features are in the hundreds or the weights are too large, tanh is saturated from the first steps and hardly learns. Standardize the data and use an initialization meant for tanh.",
            r"<b>“tanh solves vanishing gradients”.</b> It is better than the sigmoid (a derivative up to 1 and centring), but it saturates too. For deep networks use the ReLU family, normalization and residual connections; for sequences, LSTM/GRU.",
            r"<b>A home-made tanh through exp.</b> It returns nan for large $|x|$. Use <code>np.tanh</code> or <code>torch.tanh</code>.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            r"<a href='../sigmoid/'>Sigmoid</a>: $\tanh x=2\sigma(2x)-1$ and $\sigma(x)=\tfrac12(1+\tanh\tfrac x2)$; the derivatives are related by $\tanh' x=4\sigma'(2x)$.",
            r"<a href='../relu/'>ReLU</a>: does not saturate for $x&gt;0$ and displaced tanh from deep convolutional networks.",
            r"<a href='../gelu/'>GELU</a>: the popular approximation $0.5x\bigl(1+\tanh\bigl(\sqrt{2/\pi}\,(x+0.044715x^3)\bigr)\bigr)$.",
            r"<a href='../silu/'>SiLU</a>: $x\sigma(x)=\tfrac x2\bigl(1+\tanh\tfrac x2\bigr)$ — the same S-curve acting as a “soft gate”.",
            r"<a href='../mse/'>MSE</a>: the natural partner for a tanh output when the targets lie in $[-1,\,1]$.",
            r"<a href='../adam/'>Adam</a>: the optimizer of Figure 7; its adaptive step helps it get through plateaus caused by saturation.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, r"1) $\tanh x=\frac{e^x-e^{-x}}{e^x+e^{-x}}=\frac{\sinh x}{\cosh x}=2\sigma(2x)-1$ maps $\mathbb R$ onto $(-1,\,1)$, is odd and passes through zero. 2) $\tanh'=1-\tanh^2\le1$, with the maximum at zero and saturation on the tails. 3) The Taylor series $x-\frac{x^3}{3}+\dots$ converges for $|x|&lt;\pi/2$. 4) Zero-centred outputs make the next layer train faster than with the sigmoid. 5) Sums of tanh folds approximate any continuous function on a compact set; initialize with Glorot (Xavier) and gain $5/3$. 6) In an RNN tanh keeps the state bounded, but the gradient through time fades — hence LSTM."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q=r"We know that $\tanh 0.5\approx0.462$. What is $\tanh(-0.5)$?", options=[r"$0.538$", r"$-0.462$", r"$0.462$", r"$-0.538$"], answer=1,
                 explain=r"tanh is odd: $\tanh(-x)=-\tanh x=-0.462$. The answer $0.538=1-0.462$ is the symmetry of the sigmoid, not of the tangent."),
            dict(q=r"A neuron output $t=\tanh z=0.8$. What is the derivative $\tanh' z$?", options=[r"$0.2$", r"$0.36$", r"$0.64$", r"$0.16$"], answer=1,
                 explain=r"$\tanh' z=1-t^2=1-0.64=0.36$. No need to recompute an exponential."),
            dict(q=r"Which identity is correct?", options=[r"$\tanh x=\sigma(2x)-1$", r"$\tanh x=2\sigma(x)-1$", r"$\tanh x=2\sigma(2x)-1$", r"$\tanh x=\sigma(x)/2$"], answer=2,
                 explain=r"The sigmoid is squeezed horizontally by 2, stretched vertically by 2 and lowered by 1: $2\sigma(2x)-1$."),
            dict(q=r"Why does tanh in hidden layers usually train faster than the sigmoid?", options=[r"It is faster to compute", r"Its outputs are zero-centred and its derivative reaches 1, not 0.25", r"It does not saturate", r"It has no derivative at zero"], answer=1,
                 explain=r"Centring makes the next layer’s loss surface “rounder”, and a four times larger maximum derivative weakens the gradient less. tanh saturates just like the sigmoid."),
            dict(q=r"In a tanh RNN the recurrent weight was made very large. What happens to the gradient over many steps?", options=[r"It explodes: the factors are $|w|&gt;1$", r"It vanishes: the states saturate and $1-h^2\to0$", r"It stays equal to 1", r"It becomes negative"], answer=1,
                 explain=r"Each factor is $w(1-h_s^2)$. With a large $w$ the state is pressed against $\pm1$ and $1-h_s^2$ becomes tiny — in Figure 8 at $w=3$ the gradient drops to $1.6\cdot10^{-38}$."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", r"Sigmoida sonni 0 dan 1 gacha bo‘lgan ulushga aylantiradi. Lekin tarmoq ichida ko‘pincha ulush emas, <i>ishorali signal</i> kerak bo‘ladi: «odatdagidan ko‘p» yoki «odatdagidan kam», «kuchaytirish» yoki «susaytirish». Giperbolik tangens (hyperbolic tangent) — xuddi shu silliq S-egri chiziq, lekin chiqishi $(-1;\,1)$ oraliqda va markazi nolda."),
        ("p", r"U qayerda uchraydi:"),
        ("ul", [
            r"<b>rekurrent tarmoqlar</b> — oddiy RNN’da $h_t=\tanh(Wh_{t-1}+Ux_t+b)$; LSTM va GRU’da tanh xotira uchun nomzodni hosil qiladi, LSTM’da esa yacheyka chiqishini ham chegaralaydi;",
            r"<b>klassik tarmoqlarning yashirin qatlamlari</b> — ReLU davrigacha tanh standart edi va hozir ham kichik tarmoqlarda hamda silliqlik muhim bo‘lgan fizik modellarda (PINN) yaxshi ishlaydi;",
            r"<b>generator chiqishi</b> — agar rasmlar $[-1;\,1]$ ga normallashtirilgan bo‘lsa, GAN generatorining oxirgi qatlami (masalan, DCGAN) tanh ishlatadi;",
            r"<b>harakatlar va logitlarni chegaralash</b> — mustahkamlab o‘qitishda (SAC) harakat tanh orqali $(-1;\,1)$ ga siqiladi, Gemma 2 esa logitlarni «yumshoq kesadi»: $c\cdot\tanh(z/c)$;",
            r"<b>boshqa aktivatsiyalar ichida</b> — <a href='../gelu/'>GELU</a> ning mashhur yaqinlashuvi tanh orqali yozilgan.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", r"$\tanh$ butun son o‘qini $(-1;\,1)$ ga siqadi, koordinatalar boshidan o‘tadi va toq: $\tanh(-x)=-\tanh x$. Bu cho‘zilgan sigmoida: $\tanh x=2\sigma(2x)-1$. Uning hosilasi $1-\tanh^2x$ 1 dan oshmaydi — sigmoida maksimumidan 4 marta katta, — lekin chekkalarda tanh ham xuddi shunday to‘yinadi va gradiyent so‘nadi."),
    ]),
    dict(id="intuition", title="Intuitsiya: nolga qo‘yilgan sigmoida", blocks=[
        ("p", r"Ishorali ovoz regulyatorini tasavvur qiling: nol — sukunat, o‘ngga — balandroq, chapga — qarama-qarshi fazada balandroq. Nol atrofida burayotganingizda chiqish kirishga itoatkorlik bilan ergashadi: $\tanh x\approx x$. Uzoqlashgan sari burash qiyinlashadi: chiqish $\pm1$ ga tiralib, boshqa o‘smaydi. Bu <b>to‘yinish</b> (saturation)."),
        ("p", r"Nuqtani torting. To‘q sariq chiziq — urinma, uning qiyaligi hosilaga teng. Kulrang punktir — sigmoida: xuddi shu shakl, lekin yuqoriga surilgan, ikki marta past va to‘rt marta yotiqroq."),
        ("viz", "tanh-explorer", {"x": 1}, r"<b>1-rasm.</b> tanh, uning urinmasi va hosilasi (pastda). Ko‘k nuqtani torting yoki u fokusda bo‘lganda strelkalarni bosing. Hosila maksimumi $x=0$ da $1$ ga teng, sigmoidada esa $0{,}25$. $x=1$ da: $\tanh 1=0{,}7616$, $\tanh' 1=0{,}4200$."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", r"$x=2$ da tanh allaqachon $0{,}964$, hosila esa bor-yo‘g‘i $0{,}071$ — markazdagidan 14 marta kichik. $|x|&gt;2{,}99$ da hosila $0{,}01$ dan pastga tushadi: kirish o‘sishda davom etadi, chiqish esa deyarli joyida turadi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", r"Formulada ikkita eksponenta bor: o‘suvchi $e^{x}$ va kamayuvchi $e^{-x}$. Surat — ularning ayirmasi, maxraj — yig‘indisi. Bu ifodalarning yarmilari o‘z nomlariga ega — giperbolik sinus va kosinus:"),
        ("eq", r"\begin{aligned}\sinh x&=\frac{e^{x}-e^{-x}}{2}\\[4pt]\cosh x&=\frac{e^{x}+e^{-x}}{2}\\[4pt]\tanh x&=\frac{\sinh x}{\cosh x}\end{aligned}"),
        ("symbols", [
            (r"e^{x}-e^{-x}", r"ayirma toq: $x\to-x$ almashtirishda ishorasini o‘zgartiradi; $x&gt;0$ da musbat;"),
            (r"e^{x}+e^{-x}", r"yig‘indi doim musbat va 2 dan kichik emas — maxraj hech qachon nolga aylanmaydi;"),
            (r"|\sinh x|<\cosh x", r"ayirma moduli doim yig‘indidan kichik, shuning uchun $|\tanh x|&lt;1$;"),
            (r"x\to\pm\infty", r"eksponentalardan biri e’tiborsiz darajada kichik bo‘lib qoladi va kasr $\pm1$ ga intiladi."),
        ]),
        ("p", r"Surat va maxrajni $e^{x}$ ga yoki $e^{-x}$ ga ko‘paytirib, hisoblash uchun qulay shakllarni olamiz, oxirgi shakl esa tanh’ni sigmoida bilan bog‘laydi:"),
        ("eq", r"\begin{aligned}\tanh x&=\frac{e^{2x}-1}{e^{2x}+1}=\frac{1-e^{-2x}}{1+e^{-2x}}\\[4pt]&=2\sigma(2x)-1\end{aligned}"),
        ("viz", "tanh-construction", {"x": 1, "t": 3}, r"<b>2-rasm.</b> Chapda: $\sinh$ va $\cosh$ — eksponentalarning yarim ayirmasi va yarim yig‘indisi; tanh — ularning nisbati. $x_0=1$ da: $\sinh 1=1{,}175$, $\cosh 1=1{,}543$, nisbat $0{,}7616=\tanh 1$. O‘ngda: «Boshlash»ni bosing — sigmoida uch qadamda tanh’ga aylanadi: gorizontal bo‘yicha 2 marta siqamiz, vertikal bo‘yicha 2 marta cho‘zamiz, 1 ga pastga tushiramiz."),
        ("table", ["$x$", r"$\tanh x$", r"$\tanh' x$", r"$\sigma(x)$"], "TABLE", {"num": [0, 1, 2, 3]}),
        ("p", r"Jadval toqlikni ko‘rsatadi: $\tanh(-x)=-\tanh x$, hosila esa juft funksiya. Taqqoslash uchun yonida sigmoida: uning qiymatlari noldan emas, $0{,}5$ ga nisbatan simmetrik."),
    ]),
    dict(id="properties", title="Xossalar va shakl", blocks=[
        ("ul", [
            r"<b>Aniqlanish sohasi</b> — barcha haqiqiy sonlar; <b>qiymatlar sohasi</b> — ochiq oraliq $(-1;\,1)$: $\pm1$ qiymatlariga erishilmaydi.",
            r"<b>Toqlik</b>: $\tanh(-x)=-\tanh x$, grafik koordinatalar boshiga nisbatan simmetrik, $\tanh 0=0$.",
            r"<b>Monotonlik</b>: qat’iy o‘sadi, chunki istalgan $x$ da $\tanh' x=1-\tanh^2x&gt;0$.",
            r"<b>Asimptotalar</b>: $\lim_{x\to\pm\infty}\tanh x=\pm1$.",
            r"<b>Burilish nuqtasi</b> — yagona, $x=0$: $x&lt;0$ da funksiya pastga qavariq, $x&gt;0$ da — yuqoriga.",
            r"<b>1 konstantali Lipshits sharti</b>: $|\tanh a-\tanh b|\le|a-b|$; xususan, $|\tanh x|\le|x|$, tenglik faqat $x=0$ da.",
            r"<b>Nol atrofida deyarli ayniyat</b>: $\tanh x=x-\tfrac{x^3}{3}+\dots$ — kichik vaznlarda tanh tarmog‘i deyarli chiziqli ishlaydi.",
        ]),
        ("deep", "Nega tanh x = 2σ(2x) − 1", [
            ("p", r"Sigmoida ta’rifi $\sigma(u)=1/(1+e^{-u})$ ga $u=2x$ ni qo‘yamiz:"),
            ("eq", r"2\sigma(2x)-1=\frac{2}{1+e^{-2x}}-\frac{1+e^{-2x}}{1+e^{-2x}}=\frac{1-e^{-2x}}{1+e^{-2x}}=\frac{e^{x}-e^{-x}}{e^{x}+e^{-x}}=\tanh x"),
            ("p", r"Oxiridan oldingi qadamda surat va maxraj $e^{x}$ ga ko‘paytirilgan. Teskarisi: $\sigma(x)=\tfrac12\bigl(1+\tanh\tfrac x2\bigr)$. Demak, yashirin tanh’li tarmoqni xuddi shunday ifoda kuchiga ega yashirin sigmoidali tarmoqqa qayta yozish mumkin — faqat vazn masshtablari va siljishlar o‘zgaradi. Farq o‘qitish qanday borishida (markazlashganlik bo‘limiga qarang)."),
        ]),
        ("deep", "Teskari funksiya va qo‘shish formulasi", [
            ("p", r"$y=\tanh x$ ni $x$ ga nisbatan yechamiz: $y=\frac{e^{2x}-1}{e^{2x}+1}$ dan $e^{2x}=\frac{1+y}{1-y}$, bundan"),
            ("eq", r"\operatorname{artanh}y=\frac12\ln\frac{1+y}{1-y},\qquad -1<y<1"),
            ("p", r"Masalan, $\operatorname{artanh}0{,}5\approx0{,}549$. Yana bir foydali ayniyat — qo‘shish formulasi:"),
            ("eq", r"\tanh(a+b)=\frac{\tanh a+\tanh b}{1+\tanh a\,\tanh b}"),
            ("p", r"Bu aynan tezliklarni relyativistik qo‘shish (yorug‘lik tezligi ulushlarida): $0{,}5c$ va $0{,}5c$ $c$ emas, $\frac{0{,}5+0{,}5}{1+0{,}25}c=0{,}8c$ beradi. «tanh olamida» $(-1;\,1)$ dagi ikki sonning yig‘indisi hech qachon undan chiqmaydi."),
        ]),
        ("h3", "Yumshoq cheklagich: c · tanh(x / c)"),
        ("p", r"$c\tanh(x/c)$ funksiyasi nol atrofida kirishni deyarli o‘zgartirmaydi ($\approx x$), katta qiymatlarni esa silliq ravishda $\pm c$ ga bosadi. Qattiq kesish $\operatorname{clip}(x,-c,c)$ dan farqli, unda sinishlar yo‘q va hosila hech qayerda sakrab nolga tushmaydi. Gemma 2 da diqqat logitlari ($c=50$) va yakuniy logitlar ($c=30$) shunday cheklanadi, toki ular o‘qitish davomida haddan tashqari o‘sib ketmasin."),
    ]),
    dict(id="derivative", title="Hosila: tanh′ = 1 − tanh²", blocks=[
        ("p", r"Sahifaning asosiy formulasi. Uni uch usulda keltirib chiqaramiz — har biri boshqa joyda asqotadi."),
        ("deep", "1-usul. Bo‘linma hosilasi", [
            ("p", r"$u=e^{x}-e^{-x}$, $v=e^{x}+e^{-x}$ bo‘lsin. U holda $u'=v$ va $v'=u$, va kasrni differensiallash qoidasiga ko‘ra:"),
            ("eq", r"\tanh' x=\frac{u'v-uv'}{v^{2}}=\frac{v^{2}-u^{2}}{v^{2}}=1-\Bigl(\frac{u}{v}\Bigr)^{2}=1-\tanh^{2}x"),
        ]),
        ("deep", "2-usul. Asosiy giperbolik ayniyat orqali", [
            ("p", r"Giperbolik funksiyalar uchun $\cosh^2x-\sinh^2x=1$ (eksponentalarni qo‘yib tekshiring), $\sinh' x=\cosh x$ va $\cosh' x=\sinh x$. U holda"),
            ("eq", r"\tanh' x=\frac{\cosh x\cdot\cosh x-\sinh x\cdot\sinh x}{\cosh^{2}x}=\frac{1}{\cosh^{2}x}=\operatorname{sech}^{2}x"),
            ("p", r"Ayniyatni $\cosh^2x$ ga bo‘lib, $1-\tanh^2x=\operatorname{sech}^2x$ ni olamiz — boshqacha yozilgan o‘sha formula. $\operatorname{sech}^2$ shakli katta $|x|$ da kodda foydali."),
        ]),
        ("deep", "3-usul. Sigmoida orqali", [
            ("p", r"$\tanh x=2\sigma(2x)-1$ dan zanjir qoidasiga ko‘ra:"),
            ("eq", r"\tanh' x=2\cdot\sigma'(2x)\cdot2=4\sigma(2x)\bigl(1-\sigma(2x)\bigr)"),
            ("p", r"Bundan darhol ko‘rinadiki, hosila maksimumi sigmoidadagidek $\tfrac14$ emas, $4\cdot\tfrac14=1$: chiqishning ikki baravar katta oralig‘i va kirishning ikki baravar siqilgan shkalasi 4 ko‘paytuvchini beradi."),
        ]),
        ("eq", r"\tanh' x=1-\tanh^{2}x"),
        ("p", r"Amalda: to‘g‘ri o‘tishda tarmoq $t=\tanh z$ ni allaqachon hisoblagan. Teskari o‘tishda hosila bitta ko‘paytirish $1-t^2$ ga tushadi — yangi eksponentalarsiz. Shuning uchun freymvorklar teskari o‘tish uchun tanh’ning kirishini emas, chiqishini saqlaydi."),
        ("h3", "Ikkinchi hosila va eng keskin egilishlar"),
        ("p", r"Yana bir marta differensiallaymiz: $\tanh'' x=-2\tanh x\,(1-\tanh^2x)$. U faqat $x=0$ da (burilish nuqtasi) nolga teng, ekstremumlariga esa $\tanh^2x=\tfrac13$ da, ya’ni $x=\pm\operatorname{artanh}\tfrac{1}{\sqrt3}\approx\pm0{,}658$ da erishadi; u yerdagi qiymatlar $\mp\tfrac{4}{3\sqrt3}\approx\mp0{,}770$. Bu nuqtalarda qiyalik allaqachon $1-\tfrac13=\tfrac23$ va eng tez kamayadi: shu yerda $y\approx x$ to‘g‘ri chiziq to‘yinish tomon egilishga o‘tadi."),
        ("h3", "Nol atrofida Teylor qatori"),
        ("eq", r"\tanh x=x-\frac{x^{3}}{3}+\frac{2x^{5}}{15}-\frac{17x^{7}}{315}+\frac{62x^{9}}{2835}-\dots,\qquad |x|<\frac{\pi}{2}"),
        ("p", r"Qator faqat $|x|&lt;\pi/2\approx1{,}571$ da yaqinlashadi: $\cosh x$ maxraj kompleks nuqtalar $x=\pm i\pi/2$ da nolga aylanadi va yaqinlashish radiusi eng yaqinigacha bo‘lgan masofaga teng. Bu sigmoidanikidan ($\pi$) ikki marta kichik — axir tanh gorizontal bo‘yicha 2 marta siqilgan."),
        ("viz", "tanh-taylor", {"order": 3, "x": 1}, r"<b>3-rasm.</b> 1–9 tartibli Teylor ko‘phadlari va $|x|&lt;\pi/2$ yaqinlashish polosasi. $x=1$ da 3-tartibli yaqinlashish $0{,}7616$ o‘rniga $0{,}6667$, 9-tartibli esa $0{,}7679$ beradi. Polosadan tashqarida, $x=2$ da ko‘phadlar uzoqlashadi: 3-tartib $-0{,}667$, 9-tartib esa allaqachon $7{,}889$ beradi."),
    ]),
    dict(id="centered", title="Markazlashganlik: nega tanh sigmoidadan yaxshiroq o‘qitiladi", blocks=[
        ("p", r"Keyingi qatlam neyronini ko‘raylik: $z=\sum_i w_ia_i+b$, bu yerda $a_i$ — oldingi qatlam chiqishlari. Yo‘qotishning vazn bo‘yicha gradiyenti"),
        ("eq", r"\frac{\partial L}{\partial w_i}=\delta\cdot a_i,\qquad \delta=\frac{\partial L}{\partial z}"),
        ("p", r"Agar barcha $a_i&gt;0$ bo‘lsa (sigmoida chiqishlari), bitta misolda <b>gradiyentning barcha komponentalari bir xil ishorali</b> — $\delta$ ishorasida. SGD qadami neyronning barcha vaznlarini yoki yuqoriga, yoki pastga suradi. Optimumga yetish uchun ba’zi vaznlarni oshirib, boshqalarini kamaytirish kerak bo‘lsa, faqat zigzag bo‘ylab yurish qoladi."),
        ("p", r"Ikkinchi qarash — yo‘qotish sirtining shakli orqali. $\tfrac12(w^\top a-y)^2$ kvadratik yo‘qotishli chiziqli neyron uchun Gesse matritsasi $\mathbb E[aa^\top]=\operatorname{Cov}(a)+\mu\mu^\top$, bu yerda $\mu$ — kirishlar o‘rtachasi. Nolga teng bo‘lmagan o‘rtacha $\mu$ bo‘ylab bitta katta xos qiymat qo‘shadi va «vodiy» cho‘ziladi. Quyidagi $\sigma(z)$ kirishlar uchun xos qiymatlar $0{,}034$ va $0{,}530$ (shartlanganlik soni 15,5), $\tanh(z)$ uchun — $0{,}340$ va $0{,}415$ (1,22)."),
        ("viz", "tanh-zigzag", {"steps": 50}, r"<b>4-rasm.</b> Chiziqli neyronning ikki vazni $w=(w_1;\,w_2)$ ni 100 ta misolda o‘qitamiz; kirishlar bir xil tasodifiy $z$ lardan chapda $\sigma(z)$, o‘ngda $\tanh(z)$. Qadami $0{,}5$ bo‘lgan SGD $(-1;\,1)$ dan $w^*=(1;\,-1)$ ga yo‘l oladi. Chapda har bir qadam «o‘ngga-yuqoriga» yoki «chapga-pastga» yo‘nalgan (firuza kvadrantlar) va yo‘l cho‘zilgan vodiyni arralaydi; o‘ngda yo‘l ham shovqinli (SGD har safar bitta misol oladi), lekin optimumga muntazam «arralash»siz boradi. 50 qadamdan keyin optimumgacha masofa $1{,}252$ va $0{,}000$; $0{,}1$ aniqlikka 194 va 21 qadamda erishiladi."),
        ("callout", "key", "Xulosa", r"Markazlashgan aktivatsiyalar keyingi qatlamning yo‘qotish sirtini «yumaloqroq» qiladi va gradiyent tushish minimumga to‘g‘riroq boradi. Bu tanh yashirin qatlamlarda sigmoidadan tezroq o‘qitilishining sabablaridan biri (LeKun va boshq., «Efficient BackProp», 1998). Kirishlarni normallashtirish va BatchNorm ham shu g‘oyaga asoslangan."),
    ]),
    dict(id="space", title="Tekislikda tanh: burmalar, qirralar va tepaliklar", blocks=[
        ("p", r"Ikki kirishli neyron $\tanh(w_1x_1+w_2x_2+b)$ ni hisoblaydi. Tekislikda bu <b>burma</b>: sirt $w^\top x+b=0$ to‘g‘ri chiziq bo‘ylab $-1$ dan $+1$ ga o‘tadi va u bo‘ylab o‘zgarmaydi. Ikki qarama-qarshi burmaning yig‘indisi <b>qirra</b> beradi, to‘rt burma va chiqishdagi yana bitta tanh esa faqat kvadrat ichida $-1$ dan farq qiladigan <b>tepalik</b> beradi."),
        ("viz", "tanh-surface", {"mode": "four", "k": 2}, r"<b>5-rasm.</b> tanh’dan iborat kichik tarmoq. «1 neyron» — $\tanh(k(0{,}8x_1+0{,}6x_2))$; «2 neyron» — $\tanh(k(x_1+1))-\tanh(k(x_1-1))-1$; «4 + chiqish» — $x_1$ va $x_2$ bo‘yicha to‘rtta shunday burmaning yig‘indisi $s$, so‘ng $\tanh(2(s-3))$. $k=2$ da tepalik cho‘qqisida $f(0;\,0)=0{,}937$, uzoqda esa $f=-1{,}000$. Punktir — har bir yashirin neyron kirishi nolga teng bo‘lgan to‘g‘ri chiziqlar."),
        ("p", r"<b>Universal approksimatsiya teoremasi</b> (Sibenko, 1989; Xornik, 1991) shunday ishlaydi: yetarlicha ko‘p tanh neyronli bitta yashirin qatlamli tarmoq chegaralangan yopiq to‘plamdagi istalgan uzluksiz funksiyani istalgan aniqlikda yaqinlashtiradi. Tepaliklar burmalardan yig‘iladi, tepaliklardan esa istalgan relyefni yig‘ish mumkin. Bizning tepalik ko‘rgazmalilik uchun chiqishda ikkinchi tanh ishlatadi, teoremaga esa chiziqli chiqishli bitta yashirin qatlam yetarli. U bunday vaznlar <i>mavjudligini</i> aytadi, lekin qancha neyron kerakligini va o‘qitish ularni topishini aytmaydi."),
    ]),
    dict(id="training", title="O‘qitishda tanh: qatlamlar bo‘yicha aktivatsiyalar va egri chiziqni moslash", blocks=[
        ("h3", "Chuqur tarmoqda signal bilan nima sodir bo‘ladi"),
        ("p", r"Har bir qatlam vaznlari $g^2/n$ dispersiya bilan tasodifiy tanlangan bo‘lsin, bu yerda $n$ — neyron kirishlari soni. Agar $g$ kichik bo‘lsa, signal qatlamdan qatlamga so‘nadi va tanh deyarli chiziqli funksiya kabi ishlaydi. Agar $g$ katta bo‘lsa, neyron kirishlari katta va tanh to‘yinishga ketadi: chiqishlar $\pm1$ ga yopishadi, hosilalar deyarli nol."),
        ("viz", "tanh-layers", {"act": "tanh", "g": 1}, r"<b>6-rasm.</b> Har biri 100 neyronli 10 qatlamdan iborat tasodifiy tarmoq, kirishlar $N(0,1)$; har bir qatlamda 2000 ta aktivatsiya gistogrammasi (20 misol × 100 neyron), to‘q sariq nuqta — o‘rtacha. $g=1$ da tanh: oxirgi qatlam o‘rtachasi $0{,}013$, tarqoqlik esa asta-sekin $0{,}225$ gacha qisqaradi; $g=0{,}5$ da signal so‘nadi: tarqoqlik $0{,}001$ gacha tushadi, $g=3$ da neyronlarning qariyb yarmi to‘yingan ($|a|&gt;0{,}95$ bo‘lgan qiymatlar $48\%$). $g=5/3$ da tarqoqlik $0{,}65$ atrofida saqlanadi, $10\%$ to‘yingan. Sigmoidada har bir qatlamda o‘rtacha $0{,}5$ atrofida (oxirgisida $0{,}516$) — chiqishlar markazlashmagan."),
        ("p", r"Shuning uchun tanh qatlamlarida Gloro (Xavier) initsializatsiyasi, $\operatorname{Var}w=\frac{2}{n_\text{in}+n_\text{out}}$, olinadi, PyTorch esa uni $g=5/3$ kuchaytirishga ko‘paytirishni tavsiya qiladi (<code>calculate_gain('tanh')</code>): ko‘paytuvchi tanh signalni siqishini qoplaydi. Kvadrat qatlam uchun bu aynan 6-rasmdagi $g=5/3$ holati."),
        ("h3", "tanh tarmog‘i egri chiziqni moslaydi"),
        ("p", r"$H$ neyronli yashirin qatlam va chiziqli chiqish: $\hat y(x)=\sum_{k=1}^{H}v_k\tanh(w_kx+b_k)+c$. Har bir qo‘shiluvchi — chetlari silliq «zina»; o‘qitish zinalarni suradi, cho‘zadi va masshtablaydi, toki ularning yig‘indisi ma’lumotlarga tushsin."),
        ("viz", "tanh-fit", {"h": 5}, r"<b>7-rasm.</b> Shovqinli ($\sigma=0{,}08$) $y=0{,}8\sin(2{,}2x)+0{,}3x$ ning 40 nuqtasi, to‘liq gradiyent va $0{,}05$ qadamli <a href='../adam/'>Adam</a>. Firuza egri chiziqlar — alohida neyronlar hissasi, ko‘k — ularning yig‘indisi. 5 neyron bilan MSE $1{,}059$ dan taxminan $0{,}05$ lik platogacha tushadi (200–380-qadamlar), so‘ng neyronlardan biri «o‘z rolini topadi»: 500-qadamda xato $0{,}006$, 800-qadamda — $0{,}0041$, ya’ni shovqin darajasida ($0{,}08^2=0{,}0064$). 3 neyron bilan tarmoq taxminan $0{,}11$ da tiqilib qoladi (2000-qadamda $0{,}106$), 8 neyron bilan 400-qadamdayoq $0{,}0039$ ga yetadi."),
        ("callout", "note", "Plato — bu to‘yinish", r"Yo‘qotish egri chizig‘idagi uzun platolar ko‘pincha neyronlarning bir qismi tanh’ning yassi chekkalarida ishlayotganini bildiradi: ularning hosilasi kichik va gradiyent parametrlarini deyarli siljitmaydi. Kirishlarni normallashtirish, ehtiyotkor initsializatsiya va Adam kabi adaptiv optimizatorlar yordam beradi."),
    ]),
    dict(id="rnn", title="Rekurrent tarmoqlarda va LSTM’da tanh", blocks=[
        ("p", r"Oddiy rekurrent tarmoq holatni har qadamda bir xil formula bilan yangilaydi: $h_t=\tanh(Wh_{t-1}+Ux_t+b)$. Bu yerda tanh saqlagich vazifasini bajaradi: matn qanchalik uzun bo‘lmasin, holat $(-1;\,1)$ da qoladi va «portlamaydi». Lekin chegaralanganlik uchun gradiyent bilan to‘lashga to‘g‘ri keladi (ko‘paytuvchilar chapda $s=T$ dan o‘ngda $s=t+1$ gacha ko‘paytiriladi):"),
        ("eq", r"\frac{\partial h_T}{\partial h_t}=\prod_{s=t+1}^{T}\operatorname{diag}\bigl(1-h_s^{2}\bigr)\,W"),
        ("p", r"Har bir ko‘paytuvchida $1-h_s^2\le1$ bor. Vaznlar kichik bo‘lsa, ko‘paytma eksponensial so‘nadi. Vaznlar katta bo‘lsa, holatlar $\pm1$ ga bosiladi, $1-h_s^2\to0$ — va gradiyent yana so‘nadi. U faqat shu ikki rejim orasidagi tor oynada omon qoladi. Ko‘p o‘lchovli RNN’da bu oyna chegarasida gradiyent portlashi ham mumkin (Paskanu va boshq., 2013), shuning uchun tanh’li RNN gradiyent normasini kesish bilan o‘qitiladi."),
        ("viz", "tanh-rnn", {"w": 1}, r"<b>8-rasm.</b> Skalyar RNN $h_t=\tanh(wh_{t-1}+x_t)$, 30 qadam, kirishlar $x_t\sim N(0;\,0{,}2^2)$ (kulrang ustunlar). Pastda — logarifmik shkalada $|\partial h_{30}/\partial h_t|$. $w=1$ da birinchi qadamdan oxirgisigacha gradiyent $3{,}1\cdot10^{-4}$ gacha kamayadi; $w=0{,}5$ da — $5{,}7\cdot10^{-11}$ gacha; $w=1{,}2$ da — $1{,}3\cdot10^{-3}$; holat to‘yingan $w=2$ va $w=3$ da esa — $7{,}2\cdot10^{-18}$ va $1{,}6\cdot10^{-38}$ gacha."),
        ("p", r"LSTM bu muammoni alohida «magistral» — tanh orqali emas, qo‘shish orqali yangilanadigan yacheyka holati $c_t$ bilan hal qiladi:"),
        ("eq", r"\begin{aligned}g_t&=\tanh\bigl(W_g[h_{t-1},x_t]+b_g\bigr)\\c_t&=f_t\odot c_{t-1}+i_t\odot g_t\\h_t&=o_t\odot\tanh(c_t)\end{aligned}"),
        ("p", r"Bu yerda $f_t,i_t,o_t\in(0;\,1)$ — <a href='../sigmoid/'>sigmoidalar</a>dagi ventillar, tanh esa ikki vazifani bajaradi: nomzod $g_t\in(-1;\,1)$ xotirani ham oshira, ham kamaytira oladi (sigmoida faqat qo‘sha olardi), $\tanh(c_t)$ esa chiqishni chegaralaydi. $c_{t-1}\to c_t$ zanjiri bo‘ylab gradiyent (ventillarning $h_{t-1}$ ga bog‘liqligini hisobga olmasak) $\tanh'$ ko‘paytuvchisiz $f_t$ ga ko‘payadi, shuning uchun $f_t\approx1$ da u uzoq qadamlargacha yetib boradi."),
        ("callout", "history", "Biroz tarix", r"Yan LeKun 1998 yilda masshtablangan tangens $1{,}7159\tanh(2x/3)$ ni tavsiya qilgan: u $f(\pm1)=\pm1$ va chiqishning deyarli birlik dispersiyasini beradi. LSTM (Xoxrayter va Shmidxuber, 1997) tanh’ni yigirma yil davomida rekurrent tarmoqlar standartiga aylantirdi. O‘ramli tarmoqlarda uni <a href='../relu/'>ReLU</a> siqib chiqardi: AlexNet maqolasida (2012) ReLU’li to‘rt qatlamli o‘ramli tarmoq CIFAR-10 o‘quv to‘plamida 25% xatoga xuddi shunday tanh’li tarmoqdan 6 marta tezroq yetdi."),
    ]),
    dict(id="code", title="Kodda: barqaror va kutilmagan holatlarsiz", blocks=[
        ("p", r"Eksponentalar orqali sodda formula $x=1000$ da $e^{1000}=\infty$ ni hisoblaydi va natijada $\infty/\infty=\text{nan}$ chiqadi. O‘rnatilgan <code>np.tanh</code> va <code>torch.tanh</code> barqaror: $x\gtrsim19$ da ular float64 da aynan $1{,}0$ qaytaradi. Lekin unda $1-\tanh^2 x$ aynan 0 beradi, holbuki $x=20$ da haqiqiy qiymat taxminan $1{,}7\cdot10^{-17}$. Agar uzoq chekkalarda hosila kerak bo‘lsa, uni $\operatorname{sech}^2$ orqali barqaror shaklda hisoblang."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Qoida", r"O‘rnatilgan tanh va avtomatik differensiallashdan foydalaning; teskari o‘tishda — saqlangan chiqishdan $1-t^2$ formulasi. tanh tarmoqlari uchun — $5/3$ kuchaytirishli Gloro (Xavier) initsializatsiyasi, RNN uchun — gradiyent normasini kesish."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            r"<b>Ehtimollik uchun chiqishda sigmoida o‘rniga tanh.</b> tanh chiqishi $(-1;\,1)$ da yotadi va ehtimollik emas. Binar klassifikatsiyaga <a href='../sigmoid/'>sigmoida</a> va <a href='../bce/'>BCE</a> kerak; maqsadlar $[-1;\,1]$ ga normallashtirilgan bo‘lsa, chiqishdagi tanh o‘rinli.",
            r"<b>Chiqish o‘rniga kirish bo‘yicha hosila.</b> $1-t^2$ formulasi <i>chiqish</i> $t=\tanh x$ ga qo‘llaniladi. Ko‘p uchraydigan xato — kirishdan $1-x^2$: $x=2$ da u $0{,}071$ o‘rniga $-3$ beradi.",
            r"<b>Normallashtirilmagan kirishlar va katta vaznlar.</b> Agar belgilar yuzlab tartibda yoki vaznlar juda katta bo‘lsa, tanh birinchi qadamlardanoq to‘yingan va deyarli o‘rganmaydi. Ma’lumotlarni standartlashtiring va tanh uchun mo‘ljallangan initsializatsiyani oling.",
            r"<b>«tanh so‘nish muammosini hal qiladi».</b> U sigmoidadan yaxshiroq (hosila 1 gacha va markazlashganlik), lekin u ham to‘yinadi. Chuqur tarmoqlar uchun — ReLU oilasi, normallashtirish va qoldiq bog‘lanishlar; ketma-ketliklar uchun — LSTM/GRU.",
            r"<b>exp orqali o‘zi yozilgan tanh.</b> Katta $|x|$ da nan beradi. <code>np.tanh</code>, <code>torch.tanh</code> dan foydalaning.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘lanish", blocks=[
        ("ul", [
            r"<a href='../sigmoid/'>Sigmoida</a>: $\tanh x=2\sigma(2x)-1$ va $\sigma(x)=\tfrac12(1+\tanh\tfrac x2)$; hosilalar $\tanh' x=4\sigma'(2x)$ kabi bog‘langan.",
            r"<a href='../relu/'>ReLU</a>: $x&gt;0$ da to‘yinmaydi va tanh’ni chuqur o‘ramli tarmoqlardan siqib chiqardi.",
            r"<a href='../gelu/'>GELU</a>: mashhur yaqinlashuv $0{,}5x\bigl(1+\tanh\bigl(\sqrt{2/\pi}\,(x+0{,}044715x^3)\bigr)\bigr)$.",
            r"<a href='../silu/'>SiLU</a>: $x\sigma(x)=\tfrac x2\bigl(1+\tanh\tfrac x2\bigr)$ — «yumshoq ventil» rolidagi o‘sha S-egri chiziq.",
            r"<a href='../mse/'>MSE</a>: maqsadlar $[-1;\,1]$ da bo‘lganda tanh chiqishi uchun tabiiy juftlik.",
            r"<a href='../adam/'>Adam</a>: 7-rasmdagi optimizator; moslashuvchan qadam unga to‘yinish keltirib chiqargan platolardan o‘tishga yordam beradi.",
        ]),
    ]),
    dict(id="summary", title="Xulosalar", blocks=[
        ("callout", "key", None, r"1) $\tanh x=\frac{e^x-e^{-x}}{e^x+e^{-x}}=\frac{\sinh x}{\cosh x}=2\sigma(2x)-1$ $\mathbb R$ ni $(-1;\,1)$ ga akslantiradi, toq va noldan o‘tadi. 2) $\tanh'=1-\tanh^2\le1$, maksimum nolda, chekkalarda — to‘yinish. 3) Teylor qatori $x-\frac{x^3}{3}+\dots$ $|x|&lt;\pi/2$ da yaqinlashadi. 4) Markazlashgan chiqishlar keyingi qatlamni sigmoidaga qaraganda tezroq o‘qitadi. 5) tanh burmalarining yig‘indilari kompaktdagi istalgan uzluksiz funksiyani yaqinlashtiradi; initsializatsiya — $5/3$ kuchaytirishli Gloro (Xavier). 6) RNN’da tanh holatni chegaralangan saqlaydi, lekin vaqt bo‘yicha gradiyent so‘nadi — LSTM shundan."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q=r"Ma’lumki, $\tanh 0{,}5\approx0{,}462$. $\tanh(-0{,}5)$ nimaga teng?", options=[r"$0{,}538$", r"$-0{,}462$", r"$0{,}462$", r"$-0{,}538$"], answer=1,
                 explain=r"tanh toq: $\tanh(-x)=-\tanh x=-0{,}462$. $0{,}538=1-0{,}462$ javobi — tangensning emas, sigmoidaning simmetriyasi."),
            dict(q=r"Neyron $t=\tanh z=0{,}8$ chiqardi. $\tanh' z$ hosila nimaga teng?", options=[r"$0{,}2$", r"$0{,}36$", r"$0{,}64$", r"$0{,}16$"], answer=1,
                 explain=r"$\tanh' z=1-t^2=1-0{,}64=0{,}36$. Eksponentani qayta hisoblash shart emas."),
            dict(q=r"Qaysi ayniyat to‘g‘ri?", options=[r"$\tanh x=\sigma(2x)-1$", r"$\tanh x=2\sigma(x)-1$", r"$\tanh x=2\sigma(2x)-1$", r"$\tanh x=\sigma(x)/2$"], answer=2,
                 explain=r"Sigmoida gorizontal bo‘yicha 2 marta siqiladi, vertikal bo‘yicha 2 marta cho‘ziladi va 1 ga pastga tushiriladi: $2\sigma(2x)-1$."),
            dict(q=r"Nega yashirin qatlamlarda tanh odatda sigmoidadan tezroq o‘qitiladi?", options=[r"U tezroq hisoblanadi", r"Uning chiqishlari markazlashgan va hosilasi 0,25 gacha emas, 1 gacha", r"U to‘yinmaydi", r"Uning nolda hosilasi yo‘q"], answer=1,
                 explain=r"Markazlashganlik keyingi qatlam yo‘qotish sirtini «yumaloqroq» qiladi, hosila maksimumining to‘rt marta kattaligi esa gradiyentni kamroq susaytiradi. tanh ham xuddi sigmoida kabi to‘yinadi."),
            dict(q=r"tanh’li RNN’da rekurrent vazn juda katta qilindi. Ko‘p qadamlar orqali gradiyent bilan nima bo‘ladi?", options=[r"Portlaydi: ko‘paytuvchilar $|w|&gt;1$", r"So‘nadi: holatlar to‘yinadi va $1-h^2\to0$", r"1 ga teng bo‘lib qoladi", r"Manfiy bo‘lib qoladi"], answer=1,
                 explain=r"Har bir ko‘paytuvchi $w(1-h_s^2)$ ga teng. Katta $w$ da holat $\pm1$ ga bosiladi va $1-h_s^2$ juda kichik bo‘ladi — 8-rasmda $w=3$ da gradiyent $1{,}6\cdot10^{-38}$ gacha tushadi."),
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
