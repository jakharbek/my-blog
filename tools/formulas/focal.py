"""Formula page: Focal Loss. Format: see README.md (reference page: sigmoid.py)."""

META = dict(
    id="focal",
    date="2026-10-28",
    minutes=35,
    hero=r"\mathrm{FL}(p_t)=-\alpha_t\,(1-p_t)^{\gamma}\,\log p_t",
    title={"ru": "Focal Loss: потеря, которая смотрит на трудные примеры", "en": "Focal Loss: the loss that looks at the hard examples", "uz": "Focal Loss: qiyin misollarga qaraydigan yo‘qotish"},
    dek={
        "ru": "Кросс-энтропия с одним множителем (1 − p_t)^γ. Разбираем по косточкам, как он в сотни раз гасит лёгкие примеры, почему градиент перестаёт быть монотонным, откуда в RetinaNet γ = 2 и α = 0,25, что происходит с потерей при дисбалансе 1 : 1000 и почему модель, обученная на focal loss, выдаёт некалиброванные вероятности.",
        "en": "Cross-entropy with a single factor (1 − p_t)^γ. We take apart how it damps easy examples by orders of magnitude, why the gradient stops being monotonic, where RetinaNet’s γ = 2 and α = 0.25 come from, what happens to the loss at a 1 : 1000 imbalance, and why a model trained with focal loss outputs uncalibrated probabilities.",
        "uz": "Bitta (1 − p_t)^γ ko‘paytuvchili kross-entropiya. U oson misollarni yuzlab marta qanday so‘ndirishini, nega gradiyent monoton bo‘lmay qolishini, RetinaNet’dagi γ = 2 va α = 0,25 qayerdan kelishini, 1 : 1000 muvozanatsizlikda yo‘qotish bilan nima bo‘lishini va focal loss’da o‘qitilgan model nega kalibrlanmagan ehtimolliklar berishini mayda detallarigacha tahlil qilamiz.",
    },
    description={
        "ru": "Focal loss подробно: p_t и модулирующий множитель, семейство кривых по γ, вывод градиента по логиту, 3D-поверхность FL(p_t, γ), дисбаланс классов, α-балансировка и калибровка, обучение логистической регрессии, код NumPy и PyTorch, RetinaNet.",
        "en": "Focal loss in depth: p_t and the modulating factor, the family of curves in γ, the gradient with respect to the logit, the 3D surface FL(p_t, γ), class imbalance, α-balancing and calibration, training logistic regression, NumPy and PyTorch code, RetinaNet.",
        "uz": "Focal loss batafsil: p_t va modulyatsiyalovchi ko‘paytuvchi, γ bo‘yicha egri chiziqlar oilasi, logit bo‘yicha gradiyent, FL(p_t, γ) 3D-sirti, sinflar muvozanatsizligi, α-muvozanatlash va kalibrlash, logistik regressiyani o‘qitish, NumPy va PyTorch kodi, RetinaNet.",
    },
)

# p_t, CE, (1 − p_t)^2, FL (γ = 2), CE / FL
TABLE = [("0.1", "2.303", "0.81", "1.865", "1.23"), ("0.3", "1.204", "0.49", "0.590", "2.04"), ("0.5", "0.693", "0.25", "0.173", "4"),
         ("0.7", "0.357", "0.09", "0.0321", "11.1"), ("0.9", "0.105", "0.01", "0.00105", "100"), ("0.99", "0.0101", "0.0001", "1.0e-6", "10000")]


def _table(lang):
    dec = "." if lang == "en" else ","
    def cell(c):
        if c == "1.0e-6":
            return f"$1{dec if lang == 'en' else '{,}'}0\\cdot10^{{-6}}$"
        if c == "10000":
            return "10 000" if lang != "en" else "10,000"
        return c.replace(".", dec)
    return [[cell(c) for c in row] for row in TABLE]


CODE_NUMPY = '''import numpy as np

def log_sigmoid(z):
    return -np.logaddexp(0.0, -z)          # log σ(z) без переполнения

def focal_loss(z, y, gamma=2.0, alpha=None):
    """Бинарная focal loss по логитам z и меткам y ∈ {0, 1}, поэлементно."""
    zt = np.where(y == 1, z, -z)           # логит правильного класса: p_t = σ(z_t)
    log_pt = log_sigmoid(zt)
    pt = np.exp(log_pt)
    at = 1.0 if alpha is None else np.where(y == 1, alpha, 1 - alpha)
    return -at * (1 - pt) ** gamma * log_pt

def focal_grad(z, y, gamma=2.0, alpha=None):
    """dFL/dz = ±α_t (1 − p_t)^γ (γ p_t log p_t + p_t − 1)."""
    zt = np.where(y == 1, z, -z)
    log_pt = log_sigmoid(zt)
    pt = np.exp(log_pt)
    at = 1.0 if alpha is None else np.where(y == 1, alpha, 1 - alpha)
    g = at * (1 - pt) ** gamma * (gamma * pt * log_pt + pt - 1)
    return np.where(y == 1, g, -g)

z = np.array([np.log(9.0), np.log(3 / 7), -np.log(9.0)])  # p_t = 0.9, 0.3, 0.9
y = np.array([1, 1, 0])
print(focal_loss(z, y, gamma=0.0).round(4))   # [0.1054 1.204  0.1054]  — это CE
print(focal_loss(z, y).round(5))              # [0.00105 0.58995 0.00105]
print(focal_grad(z, y, gamma=0.0).round(4))   # [-0.1 -0.7  0.1]
print(focal_grad(z, y).round(4))              # [-0.0029 -0.697   0.0029]'''

CODE_TORCH = '''import math
import torch
import torch.nn as nn
from torchvision.ops import sigmoid_focal_loss

# Бинарная (по каждому якорю и классу): α = 0.25, γ = 2 — как в RetinaNet
logits = torch.tensor([math.log(9.0), math.log(3 / 7)])
targets = torch.tensor([1.0, 1.0])
loss = sigmoid_focal_loss(logits, targets, alpha=0.25, gamma=2.0, reduction="none")
# ≈ [0.00026, 0.14749] = 0.25 · [0.00105, 0.58995]

# Многоклассовая версия через log_softmax
def focal_loss_multiclass(logits, target, gamma=2.0):
    logp = torch.log_softmax(logits, dim=-1)
    logp_t = logp.gather(-1, target[:, None]).squeeze(-1)
    return (-(1 - logp_t.exp()) ** gamma * logp_t).mean()

# Инициализация сдвига последнего слоя под редкий класс (π = 0.01)
cls_head = nn.Conv2d(256, 9 * 80, kernel_size=3, padding=1)   # A = 9 якорей × K = 80 классов
nn.init.constant_(cls_head.bias, -math.log((1 - 0.01) / 0.01))   # ≈ −4.595'''


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("log σ(z) без переполнения", "log σ(z) without overflow"),
               ("Бинарная focal loss по логитам z и меткам y ∈ {0, 1}, поэлементно.", "Binary focal loss from logits z and labels y ∈ {0, 1}, element-wise."),
               ("логит правильного класса: p_t = σ(z_t)", "logit of the correct class: p_t = σ(z_t)"),
               ("— это CE", "— this is CE"),
               ("Бинарная (по каждому якорю и классу): α = 0.25, γ = 2 — как в RetinaNet", "Binary (per anchor and class): α = 0.25, γ = 2, as in RetinaNet"),
               ("Многоклассовая версия через log_softmax", "Multi-class version via log_softmax"),
               ("Инициализация сдвига последнего слоя под редкий класс (π = 0.01)", "Initialise the last layer’s bias for a rare class (π = 0.01)"),
               ("A = 9 якорей × K = 80 классов", "A = 9 anchors × K = 80 classes")],
        "uz": [("log σ(z) без переполнения", "to‘lib ketishsiz log σ(z)"),
               ("Бинарная focal loss по логитам z и меткам y ∈ {0, 1}, поэлементно.", "z logitlar va y ∈ {0, 1} belgilar bo‘yicha binar focal loss, elementma-element."),
               ("логит правильного класса: p_t = σ(z_t)", "to‘g‘ri sinf logiti: p_t = σ(z_t)"),
               ("— это CE", "— bu CE"),
               ("Бинарная (по каждому якорю и классу): α = 0.25, γ = 2 — как в RetinaNet", "Binar (har bir anchor va sinf bo‘yicha): α = 0.25, γ = 2 — RetinaNet’dagidek"),
               ("Многоклассовая версия через log_softmax", "log_softmax orqali ko‘p sinfli versiya"),
               ("Инициализация сдвига последнего слоя под редкий класс (π = 0.01)", "Oxirgi qatlam siljishini kamyob sinfga moslab boshlash (π = 0.01)"),
               ("A = 9 якорей × K = 80 классов", "A = 9 anchor × K = 80 sinf")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", "Детектор объектов вроде RetinaNet проверяет на одной картинке около ста тысяч «якорей» — прямоугольников, в каждом из которых может оказаться объект. Объектов на кадре единицы, всё остальное — фон. Большинство фоновых якорей тривиальны: небо, стена, асфальт. Модель быстро учится уверенно называть их фоном, но <a href=\"../cross-entropy/\">кросс-энтропия</a> всё равно начисляет за каждый маленькую потерю. Сто тысяч маленьких потерь складываются в большую — и эта сумма заглушает сигнал от немногих трудных примеров, ради которых всё и затевалось."),
        ("p", "Лин, Гоял, Гиршик, Хе и Доллар (2017) предложили не выбрасывать лёгкие примеры и не пересэмплировать данные, а <b>изменить саму потерю</b>: умножить кросс-энтропию на $(1-p_t)^\\gamma$. Для уверенно распознанного примера множитель почти ноль, для трудного — почти единица. Где это используется:"),
        ("ul", [
            "<b>одностадийные детекторы</b> — RetinaNet, а за ней FCOS, ATSS и другие плотные детекторы;",
            "<b>сегментация</b> — особенно медицинская, где интересующая область занимает доли процента пикселей (часто в паре с Dice);",
            "<b>табличные задачи с редким классом</b> — мошенничество, отток, аномалии; в бустинге focal loss задают как пользовательскую целевую функцию;",
            "<b>классификация с «шумной» уверенностью</b> — focal loss иногда применяют, чтобы сеть не становилась чрезмерно уверенной.",
        ]),
        ("callout", "key", "Главное за минуту", "$p_t$ — вероятность, которую модель дала правильному классу. $\\mathrm{FL}=-(1-p_t)^\\gamma\\log p_t$: при $\\gamma=0$ это обычная кросс-энтропия, при $\\gamma=2$ пример с $p_t=0{,}9$ весит в 100 раз меньше, а с $p_t=0{,}3$ — всего в 2 раза. Множитель $\\alpha_t$ дополнительно задаёт вес классов. Цена — модель перестаёт выдавать откалиброванные вероятности."),
    ]),
    dict(id="intuition", title="Интуиция: громкость для каждого примера", blocks=[
        ("p", "Представьте класс, где учитель отвечает на вопросы учеников. Тысяча учеников задают вопросы, ответ на которые они и так знают, и двадцать — действительно трудные. Если уделять каждому вопросу одинаковое время, на трудные его не останется. Focal loss — это регулятор громкости: чем увереннее модель уже отвечает на пример, тем тише его голос в общей сумме."),
        ("p", "Потяните точку и меняйте $\\gamma$. Серая пунктирная кривая — кросс-энтропия $-\\ln p_t$. Синяя — focal loss: в правой половине, где примеры уже классифицированы верно, она прижимается к нулю гораздо раньше."),
        ("viz", "focal-curves", {"gamma": 2, "pt": 0.9}, "<b>Рисунок 1.</b> Семейство $\\mathrm{FL}(p_t)$ для $\\gamma=0;\\,0{,}5;\\,1;\\,2;\\,5$ (как на рисунке 1 статьи о RetinaNet). При $\\gamma=2$ и $p_t=0{,}9$: $\\mathrm{CE}=0{,}105$, множитель $(1-p_t)^2=0{,}01$, $\\mathrm{FL}=0{,}00105$ — в 100 раз меньше. Слева, где $p_t$ мал, кривые почти совпадают."),
        ("callout", "intuition", "Что заметить", "Focal loss почти не трогает трудные примеры и очень сильно гасит лёгкие. При $p_t\\to0$ множитель $(1-p_t)^\\gamma\\to1$, и $\\mathrm{FL}\\approx\\mathrm{CE}$. При $p_t\\to1$ потеря убывает как $(1-p_t)^{\\gamma+1}$, а не как $1-p_t$ у CE."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("eq", r"\mathrm{FL}(p_t)=-\,\alpha_t\,(1-p_t)^{\gamma}\,\log p_t,\qquad p_t=\begin{cases}p, & y=1,\\ 1-p, & y=0\end{cases}"),
        ("symbols", [
            (r"p=\sigma(z)", "вероятность класса 1, которую модель получила из логита $z$ (через <a href=\"../sigmoid/\">сигмоиду</a>; в многоклассовом случае — через <a href=\"../softmax/\">softmax</a>);"),
            (r"p_t", "вероятность <i>правильного</i> класса: насколько модель права на этом примере; $p_t&gt;0{,}5$ — пример классифицирован верно;"),
            (r"-\log p_t", "обычная кросс-энтропия: ноль при $p_t=1$, бесконечность при $p_t\\to0$;"),
            (r"(1-p_t)^\gamma", "модулирующий множитель (modulating factor): «насколько модель ещё ошибается» в степени $\\gamma$;"),
            (r"\gamma\ge0", "параметр фокусировки (focusing parameter): $\\gamma=0$ — CE, чем больше, тем сильнее гасятся лёгкие примеры; в RetinaNet $\\gamma=2$;"),
            (r"\alpha_t", "вес класса: $\\alpha$ для позитивов и $1-\\alpha$ для негативов; в RetinaNet $\\alpha=0{,}25$."),
        ]),
        ("p", "Запись через $p_t$ — главный приём: вместо двух ветвей бинарной кросс-энтропии $-y\\log p-(1-y)\\log(1-p)$ получается одна, $-\\log p_t$. В терминах логита удобно ввести $z_t=z$ при $y=1$ и $z_t=-z$ при $y=0$; тогда $p_t=\\sigma(z_t)$."),
        ("table", ["$p_t$", "$\\mathrm{CE}$", "$(1-p_t)^2$", "$\\mathrm{FL}_{\\gamma=2}$", "$\\mathrm{CE}/\\mathrm{FL}$"], "TABLE", {"num": [0, 1, 2, 3, 4]}),
        ("p", "Последний столбец — во сколько раз focal loss меньше кросс-энтропии; это ровно $1/(1-p_t)^\\gamma$. Пример из шпаргалки: при $\\gamma=2$ лёгкий пример $p_t=0{,}9$ даёт $0{,}00105$ против $0{,}105$ (в 100 раз меньше), трудный $p_t=0{,}3$ — $0{,}590$ против $1{,}204$ (примерно вдвое)."),
        ("p", "На обычной шкале значения $0{,}001$ и $0{,}000001$ неразличимы, поэтому полезно посмотреть на потери в логарифмической шкале: там множитель превращается в вертикальный сдвиг."),
        ("viz", "focal-weight", {"gamma": 2, "pt": 0.9}, "<b>Рисунок 2.</b> Слева — модулирующий множитель $(1-p_t)^\\gamma$ (бледные кривые — $\\gamma=0{,}5;\\,1;\\,2;\\,5$). Справа — CE и FL в логарифмической шкале; стрелка — разрыв между ними, $\\log$ множителя. При $\\gamma=2$: на $p_t=0{,}9$ разрыв 100 раз, на $p_t=0{,}99$ — 10 000 раз."),
    ]),
    dict(id="properties", title="Свойства", blocks=[
        ("ul", [
            "<b>Обобщает кросс-энтропию</b>: $\\gamma=0$, $\\alpha_t=1$ дают $\\mathrm{CE}=-\\log p_t$.",
            "<b>Не больше CE</b>: $0\\le\\mathrm{FL}\\le\\mathrm{CE}$, потому что $0\\le(1-p_t)^\\gamma\\le1$ при $\\gamma\\ge0$.",
            "<b>Убывает по $p_t$</b>: оба сомножителя $(1-p_t)^\\gamma$ и $-\\log p_t$ неотрицательны и убывают, поэтому чем увереннее верный ответ, тем меньше потеря.",
            "<b>Асимптотика у края</b>: при $p_t\\to1$ $\\mathrm{FL}\\approx(1-p_t)^{\\gamma+1}$, так как $-\\log p_t\\approx1-p_t$.",
            "<b>Не выпукла по логиту</b> при $\\gamma&gt;0$: для очень трудных примеров (при $\\gamma=2$ — для $p_t&lt;0{,}058$, $z_t&lt;-2{,}79$) вторая производная по $z_t$ отрицательна. Кросс-энтропия по логиту выпукла всюду.",
            "<b>Не является строго собственным правилом оценки</b> (proper scoring rule): минимум ожидаемой FL достигается не на истинной вероятности. Поэтому вероятности, выученные на FL, нужно калибровать (раздел про $\\alpha$).",
        ]),
        ("callout", "note", "Сравнение с другими способами борьбы с дисбалансом", "Взвешивание классов ($\\alpha$) меняет вес <i>класса</i> целиком, одинаково для лёгких и трудных примеров. Пересэмплирование и hard negative mining выбрасывают часть примеров по жёсткому правилу. Focal loss меняет вес <i>каждого примера</i> плавно, по тому, насколько модель уже справляется с ним, — и не требует сэмплирования."),
    ]),
    dict(id="derivative", title="Производная: градиент по логиту", blocks=[
        ("p", "Модель учится через градиент по логиту $z$, поэтому именно он показывает, кого «слышит» обучение. Для кросс-энтропии он прост: $\\partial\\,\\mathrm{CE}/\\partial z_t=-(1-p_t)$ — чем сильнее ошибка, тем сильнее градиент, монотонно. У focal loss появляется второй член."),
        ("deep", "Вывод по шагам", [
            ("p", "Шаг 1. Производная по $p_t$ — правило произведения для $-(1-p_t)^\\gamma\\log p_t$:"),
            ("eq", r"\frac{\partial\,\mathrm{FL}}{\partial p_t}=\gamma(1-p_t)^{\gamma-1}\log p_t-\frac{(1-p_t)^{\gamma}}{p_t}"),
            ("p", "Шаг 2. Производная сигмоиды: $\\partial p_t/\\partial z_t=p_t(1-p_t)$ (см. <a href=\"../sigmoid/\">сигмоиду</a>)."),
            ("p", "Шаг 3. Цепное правило и вынесение общего множителя $(1-p_t)^\\gamma$:"),
            ("eq", r"\frac{\partial\,\mathrm{FL}}{\partial z_t}=\gamma p_t(1-p_t)^{\gamma}\log p_t-(1-p_t)^{\gamma+1}=(1-p_t)^{\gamma}\bigl(\gamma p_t\log p_t+p_t-1\bigr)"),
            ("p", "Шаг 4. Для исходного логита $z$: $z_t=\\pm z$, поэтому $\\partial\\,\\mathrm{FL}/\\partial z=\\pm\\,\\partial\\,\\mathrm{FL}/\\partial z_t$ (плюс при $y=1$, минус при $y=0$), а $\\alpha_t$ просто умножает результат. Проверка: при $\\gamma=0$ получаем $p_t-1$, градиент кросс-энтропии."),
        ]),
        ("eq", r"\left|\frac{\partial\,\mathrm{FL}}{\partial z_t}\right|=(1-p_t)^{\gamma}\Bigl[(1-p_t)+\gamma\,p_t\,|\log p_t|\Bigr]"),
        ("p", "В квадратных скобках — градиент CE, $1-p_t$, плюс неотрицательная добавка $\\gamma p_t|\\log p_t|$. Снаружи — тот же множитель $(1-p_t)^\\gamma$. Для лёгких примеров множитель побеждает, а для очень трудных добавка может сделать градиент даже <b>больше</b>, чем у CE."),
        ("viz", "focal-grad", {"gamma": 2}, "<b>Рисунок 3.</b> Сила градиента по логиту правильного класса. Серый пунктир — CE, $1-p_t$. Оранжевая — FL: при $\\gamma=2$ максимум $1{,}129$ достигается при $p_t=0{,}058$, при $p_t&lt;0{,}298$ градиент FL сильнее, чем у CE, а при $p_t=0{,}9$ он составляет лишь $0{,}029$ от градиента CE (в 35 раз меньше)."),
        ("callout", "warn", "Градиент больше не монотонен", "У CE чем хуже пример, тем сильнее он тянет. У FL с $\\gamma&gt;0$ самый сильный градиент — у примеров с $p_t$ около нескольких процентов, а дальше к $p_t\\to0$ он снова падает до 1. Для $\\gamma=1$ граница, где FL тянет сильнее CE, ровно $p_t=1/e\\approx0{,}368$. Если в данных есть ошибочные метки, они как раз попадают в эту зону — focal loss будет усиленно их «учить»."),
    ]),
    dict(id="surface", title="Поверхность FL(p_t, γ) в 3D", blocks=[
        ("p", "Сведём всё семейство кривых в одну поверхность над плоскостью $(p_t,\\gamma)$. Срез при $\\gamma=0$ — кросс-энтропия; при движении по $\\gamma$ поверхность «оседает», причём тем быстрее, чем больше $p_t$."),
        ("viz", "focal-surface", {"gamma": 2, "pt": 0.5}, "<b>Рисунок 4.</b> Слева — $\\mathrm{FL}(p_t,\\gamma)$ (вращайте мышью), синяя линия — срез при выбранном $\\gamma$, бирюзовая — при выбранном $p_t$. Справа — та же бирюзовая кривая в логарифмической шкале: это прямая с наклоном $\\ln(1-p_t)$. При $p_t=0{,}5$ и $\\gamma=2$: $\\mathrm{FL}=0{,}173$, наклон $\\ln0{,}5=-0{,}693$."),
        ("p", "Почему прямая: $\\log\\mathrm{FL}=\\log\\mathrm{CE}+\\gamma\\log(1-p_t)$. По $\\gamma$ потеря затухает экспоненциально, и скорость затухания — $|\\ln(1-p_t)|$: для $p_t=0{,}5$ это $0{,}69$ на единицу $\\gamma$, для $p_t=0{,}9$ — $2{,}30$, для $p_t=0{,}99$ — $4{,}61$. Параметр $\\gamma$ раздвигает лёгкие и трудные примеры по шкале порядков."),
    ]),
    dict(id="imbalance", title="Дисбаланс: откуда берётся потеря", blocks=[
        ("p", "Смоделируем ситуацию одностадийного детектора. На каждый позитив приходится 1000 негативов. Негативы в основном лёгкие: логит правильного класса $z_t\\sim N(4,\\,1)$, то есть типичный $p_t=\\sigma(4)\\approx0{,}98$. Позитивы трудные: $z_t\\sim N(0,\\,1)$, типичный $p_t=0{,}5$. Посчитаем, какая доля суммарной потери приходится на каждую группу."),
        ("viz", "focal-imbalance", {"gamma": 2, "ratio": 1000}, "<b>Рисунок 5.</b> Слева — доля суммарной потери по корзинам $p_t$ шириной $0{,}05$ (серые — CE, синие — FL). Справа — состав суммы. Лёгкие негативы ($p_t\\ge0{,}9$) — это $96{,}3\\%$ примеров. В CE они дают $78{,}1\\%$ потери, а позитивы — только $2{,}7\\%$. В FL с $\\gamma=2$ лёгкие дают $9{,}0\\%$, а позитивы — $58{,}0\\%$."),
        ("p", "Именно это и есть «фокусировка». Градиентный спуск минимизирует сумму, и в CE эта сумма почти целиком состоит из примеров, которые уже решены. Focal loss перераспределяет «бюджет внимания»: потери лёгких примеров гасятся в десятки и сотни раз, и в сумме начинают доминировать трудные негативы и позитивы — те, на которых модель действительно может улучшиться."),
        ("callout", "history", "RetinaNet", "До 2017 года одностадийные детекторы заметно уступали двухстадийным (Faster R-CNN) по точности. Двухстадийные справлялись с дисбалансом за счёт этапа предложений и сэмплирования позитивов и негативов в пропорции 1 : 3. Лин и соавторы показали, что главная причина отставания — именно дисбаланс, и простая замена потери (RetinaNet = ResNet + FPN + focal loss) позволила одностадийному детектору превзойти двухстадийные. Работа получила награду за лучшую студенческую статью на ICCV 2017."),
    ]),
    dict(id="alpha", title="α-балансировка и калибровка", blocks=[
        ("p", "Множитель $\\alpha_t$ — обычное взвешивание классов. Интуиция подсказывает дать редкому классу больший вес: $\\alpha&gt;0{,}5$. Но в RetinaNet лучшим оказалось $\\alpha=0{,}25$ — позитивы весят <i>меньше</i> негативов. Причина в том, что $\\gamma$ уже сделал работу: лёгкие негативы погашены, и теперь перевес скорее у позитивов. $\\alpha$ и $\\gamma$ надо подбирать вместе; авторы советуют $\\gamma=2$, $\\alpha=0{,}25$, но отмечают, что результат устойчив к $\\gamma$ в диапазоне $[0{,}5;\\,5]$."),
        ("p", "Есть и тонкость, о которой забывают. Возьмём самую простую «модель» — одно число $p$, одинаковое для всех примеров. Если доля позитивов $\\pi$, то кросс-энтропия минимальна ровно при $p=\\pi$: CE — собственное правило оценки, оно учит честным вероятностям. С focal loss это уже не так."),
        ("viz", "focal-prior", {"pi": 0.01, "gamma": 2, "alpha": 0.25}, "<b>Рисунок 6.</b> Средняя потеря постоянного прогноза $p$, делённая на свой минимум. Доля позитивов $\\pi=0{,}01$. CE минимальна при $p=0{,}01$. FL с $\\gamma=2$, $\\alpha=0{,}25$ — при $p=0{,}108$ (логит $-2{,}107$), то есть модель в 11 раз переоценивает частоту позитивов. Без $\\alpha$ ($\\alpha=0{,}5$) минимум был бы при $p=0{,}154$."),
        ("p", "Вывод: модуль $(1-p_t)^\\gamma$ тянет предсказания к середине — он «не любит» уверенность, потому что за уверенность перестают платить. Поэтому выход модели, обученной на focal loss, нельзя читать как вероятность: для порогов и ранжирования это нормально, а если нужны вероятности — откалибруйте их на валидации (Platt scaling, изотоническая регрессия, температурное шкалирование)."),
        ("callout", "key", "Инициализация под редкий класс", "В начале обучения сеть выдаёт $p\\approx0{,}5$ для всех якорей, и потери 100 000 негативов взрывают первые шаги. Поэтому сдвиг последнего слоя инициализируют так, чтобы $p=\\pi$: $b=-\\ln\\frac{1-\\pi}{\\pi}$; для $\\pi=0{,}01$ это $b\\approx-4{,}595$. Кроме того, сумму FL по всем якорям делят на число <i>позитивных</i> якорей, а не на число всех."),
    ]),
    dict(id="training", title="Focal loss в обучении", blocks=[
        ("p", "Обучим логистическую регрессию на двумерных данных с дисбалансом 1 : 20 (400 негативов, 20 позитивов) двумя способами — на CE и на FL — с одинаковым стартом (сдвиг инициализирован под долю позитивов, как в RetinaNet) и одинаковым шагом. Размер каждой точки пропорционален её градиенту $|\\partial L/\\partial z|$: так видно, какие примеры «слышит» обучение."),
        ("viz", "focal-train", {"gamma": 2}, "<b>Рисунок 7.</b> Слева — CE, справа — FL с $\\gamma=2$; сплошная линия — граница $p=0{,}5$, пунктир — $p=0{,}1$ и $p=0{,}9$. Нажмите «Пуск». В начале на лёгкие примеры ($p_t&gt;0{,}9$) приходится $50{,}0\\%$ суммарного градиента CE и лишь $0{,}6\\%$ у FL; после 400 шагов — $12{,}8\\%$ и $0{,}7\\%$. Обе модели находят 13 позитивов из 20 при 3 и 4 ложных тревогах соответственно."),
        ("p", "Что видно на рисунке. У CE крупные точки рассеяны по всему облаку негативов: каждый из 400 лёгких примеров добавляет свою небольшую порцию градиента. У FL крупными остаются только точки у границы и позитивы — остальные почти исчезают. Сама граница у двух моделей получается похожей: для линейной модели на таких данных оптимальное направление почти одно и то же. Разница в другом: FL приходит к своей границе за несколько десятков шагов и больше её не двигает, а CE продолжает наращивать веса, делая лёгкие примеры ещё увереннее. В глубокой сети, где параметров миллионы, это различие решающее: градиент, потраченный на «и так понятный» фон, — это ёмкость сети, не потраченная на трудные случаи."),
        ("eq", r"w\leftarrow w-\eta\,\frac1n\sum_{i=1}^{n}\frac{\partial\,\mathrm{FL}_i}{\partial z_i}\,x_i,\qquad \frac{\partial\,\mathrm{FL}_i}{\partial z_i}=\pm(1-p_{t,i})^{\gamma}\bigl(\gamma p_{t,i}\log p_{t,i}+p_{t,i}-1\bigr)"),
        ("callout", "warn", "Честная оговорка", "Focal loss — не волшебное средство от дисбаланса. Если модель простая, а классы хорошо разделимы, она даст почти ту же границу, что и CE, только с менее уверенными вероятностями. Выигрыш появляется там, где лёгких примеров на порядки больше, чем трудных, и они реально отнимают градиент: плотная детекция, сегментация, большие таблицы с редким классом."),
    ]),
    dict(id="code", title="В коде", blocks=[
        ("p", "Считайте focal loss по логитам, а не по вероятностям: $\\log p_t=\\log\\sigma(z_t)=-\\operatorname{softplus}(-z_t)$ — без $\\log0$ и переполнения. Ниже — NumPy-версия с градиентом и проверкой на примере из шпаргалки."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "В PyTorch бинарная версия есть в torchvision; многоклассовую легко написать через <code>log_softmax</code>. Последняя строка — инициализация сдвига под редкий класс."),
        ("code", "python", "CODE_TORCH"),
        ("callout", "note", "Проверка градиента", "Численная производная $\\bigl(\\mathrm{FL}(z+\\varepsilon)-\\mathrm{FL}(z-\\varepsilon)\\bigr)/2\\varepsilon$ при $\\varepsilon=10^{-6}$ совпадает с <code>focal_grad</code> до четырёх знаков: $-0{,}0029$, $-0{,}697$, $0{,}0029$. При $p_t=0{,}3$ градиенты FL и CE почти равны ($0{,}697$ против $0{,}7$): это рядом с точкой пересечения $p_t\\approx0{,}298$ на рисунке 3."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>$\\alpha$ «по частоте» вместе с $\\gamma$.</b> Ставить $\\alpha=0{,}99$ для класса с долей 1% при $\\gamma=2$ — двойная компенсация. Начинайте с $\\gamma=2$, $\\alpha=0{,}25$ и подбирайте их вместе.",
            "<b>Нет инициализации под редкий класс.</b> Со сдвигом 0 первые итерации тонут в потерях фона; в статье RetinaNet обучение с обычной CE без инициализации $\\pi=0{,}01$ расходилось.",
            "<b>Нормировка на число всех примеров.</b> Среднее по 100 000 якорей делает потерю крошечной и зависит от размера картинки; в детекции делят на число позитивов.",
            "<b>Focal loss по вероятностям с <code>clamp</code>.</b> $\\log(\\max(p,\\varepsilon))$ обнуляет градиент для самых трудных примеров. Считайте по логитам.",
            "<b>Чтение выхода как вероятности.</b> FL смещает прогнозы к середине (рисунок 6); для оценки рисков и ставок вероятности нужно калибровать.",
            "<b>Большое $\\gamma$ при шумных метках.</b> Ошибочные метки выглядят как очень трудные примеры, а FL усиливает их относительный вес. При подозрении на шум уменьшайте $\\gamma$ или чистите разметку.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../bce/\">BCE</a> и <a href=\"../cross-entropy/\">кросс-энтропия</a>: FL с $\\gamma=0$, $\\alpha_t=1$ совпадает с ними.",
            "<a href=\"../sigmoid/\">Сигмоида</a>: $p_t=\\sigma(z_t)$, и её производная $p_t(1-p_t)$ входит в градиент FL.",
            "<a href=\"../softmax/\">Softmax</a>: в многоклассовом случае $p_t$ — компонента softmax для правильного класса.",
            "<a href=\"../huber/\">Хьюбер</a> — противоположная философия: Хьюбер <i>ослабляет</i> вклад самых больших ошибок, считая их выбросами, а FL ослабляет самые <i>маленькие</i>, чтобы большие стали заметнее.",
            "<a href=\"../triplet/\">Triplet loss</a> решает родственную задачу в обучении метрик: лёгкие тройки с нулевой потерей не дают градиента, и обучение фокусируется на трудных (hard negative mining).",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $\\mathrm{FL}=-\\alpha_t(1-p_t)^\\gamma\\log p_t$ — кросс-энтропия, умноженная на «степень ошибки» $(1-p_t)^\\gamma$; $\\gamma=0$ — CE. 2) Лёгкие примеры гасятся как $(1-p_t)^{\\gamma+1}$: при $\\gamma=2$ пример с $p_t=0{,}9$ весит в 100 раз меньше. 3) Градиент по логиту $(1-p_t)^\\gamma(\\gamma p_t\\log p_t+p_t-1)$ не монотонен: при $\\gamma=2$ максимум у $p_t\\approx0{,}06$. 4) При дисбалансе 1 : 1000 FL переносит основную часть потерь с лёгких негативов на позитивы и трудные негативы. 5) Практика RetinaNet: $\\gamma=2$, $\\alpha=0{,}25$, инициализация $b=-\\ln\\frac{1-\\pi}{\\pi}$, нормировка на число позитивов; вероятности на выходе нужно калибровать."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="Модель дала правильному классу вероятность $p_t=0{,}8$. Чему равен модулирующий множитель при $\\gamma=2$?", options=["$0{,}64$", "$0{,}2$", "$0{,}04$", "$0{,}8$"], answer=2,
                 explain="$(1-p_t)^\\gamma=0{,}2^2=0{,}04$: потеря этого примера в 25 раз меньше, чем в CE."),
            dict(q="Что получится из focal loss при $\\gamma=0$ и $\\alpha_t=1$?", options=["MSE", "Кросс-энтропия", "Hinge loss", "Ноль"], answer=1,
                 explain="Множитель $(1-p_t)^0=1$, остаётся $-\\log p_t$ — кросс-энтропия."),
            dict(q="Как ведёт себя градиент FL по логиту при $\\gamma=2$ в зависимости от $p_t$?", options=["Монотонно убывает, как у CE", "Растёт с $p_t$", "Сначала растёт, достигает максимума около $p_t\\approx0{,}06$, затем быстро падает", "Постоянен"], answer=2,
                 explain="$|\\partial\\mathrm{FL}/\\partial z_t|=(1-p_t)^\\gamma[(1-p_t)+\\gamma p_t|\\log p_t|]$: при $p_t\\to0$ он равен 1, растёт до $1{,}129$ при $p_t\\approx0{,}058$ и затем убывает."),
            dict(q="Почему в RetinaNet $\\alpha=0{,}25$, а не, скажем, $0{,}99$ для редкого класса объектов?", options=["Это опечатка в статье", "$\\gamma$ уже погасил лёгкие негативы, и сильный перевес позитивов стал бы лишним", "$\\alpha$ не влияет на обучение", "Объекты на самом деле не редки"], answer=1,
                 explain="После модулирующего множителя основная часть потерь и так идёт от позитивов и трудных негативов; $\\alpha$ и $\\gamma$ подбирают вместе, и лучшим оказалось $\\alpha=0{,}25$."),
            dict(q="Модель обучена на focal loss с $\\gamma=2$. Что верно про её выходные вероятности?", options=["Они идеально откалиброваны", "Они смещены к середине и требуют калибровки", "Они всегда равны 0 или 1", "Они совпадают с CE-моделью"], answer=1,
                 explain="FL не является собственным правилом оценки: даже для постоянного прогноза минимум не в $p=\\pi$ (рисунок 6: $0{,}108$ вместо $0{,}01$)."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "An object detector such as RetinaNet checks about a hundred thousand “anchors” per image — boxes, each of which may contain an object. There are only a handful of objects in a frame; everything else is background. Most background anchors are trivial: sky, a wall, asphalt. The model quickly learns to call them background with confidence, but <a href=\"../cross-entropy/\">cross-entropy</a> still charges a small loss for each one. A hundred thousand small losses add up to a large one — and that sum drowns out the signal from the few hard examples the whole thing was for."),
        ("p", "Lin, Goyal, Girshick, He and Dollár (2017) proposed not to discard easy examples and not to resample the data, but to <b>change the loss itself</b>: multiply cross-entropy by $(1-p_t)^\\gamma$. For a confidently recognised example the factor is almost zero, for a hard one almost one. Where it is used:"),
        ("ul", [
            "<b>one-stage detectors</b> — RetinaNet, and after it FCOS, ATSS and other dense detectors;",
            "<b>segmentation</b> — especially medical, where the region of interest covers a fraction of a percent of the pixels (often paired with Dice);",
            "<b>tabular problems with a rare class</b> — fraud, churn, anomalies; in boosting, focal loss is set as a custom objective;",
            "<b>classification with “noisy” confidence</b> — focal loss is sometimes used to keep a network from becoming overconfident.",
        ]),
        ("callout", "key", "The essentials in a minute", "$p_t$ is the probability the model gave to the correct class. $\\mathrm{FL}=-(1-p_t)^\\gamma\\log p_t$: with $\\gamma=0$ it is ordinary cross-entropy; with $\\gamma=2$ an example with $p_t=0.9$ weighs 100 times less, while one with $p_t=0.3$ only about 2 times less. The factor $\\alpha_t$ additionally sets class weights. The price: the model no longer outputs calibrated probabilities."),
    ]),
    dict(id="intuition", title="Intuition: a volume knob for every example", blocks=[
        ("p", "Picture a class where a teacher answers students’ questions. A thousand students ask questions they already know the answer to, and twenty ask really hard ones. If every question gets the same time, none is left for the hard ones. Focal loss is a volume knob: the more confidently the model already answers an example, the quieter its voice in the total."),
        ("p", "Drag the point and change $\\gamma$. The grey dashed curve is cross-entropy, $-\\ln p_t$. The blue one is focal loss: in the right half, where examples are already classified correctly, it hugs zero much earlier."),
        ("viz", "focal-curves", {"gamma": 2, "pt": 0.9}, "<b>Figure 1.</b> The family $\\mathrm{FL}(p_t)$ for $\\gamma=0,\\,0.5,\\,1,\\,2,\\,5$ (as in Figure 1 of the RetinaNet paper). With $\\gamma=2$ and $p_t=0.9$: $\\mathrm{CE}=0.105$, the factor $(1-p_t)^2=0.01$, $\\mathrm{FL}=0.00105$ — 100 times smaller. On the left, where $p_t$ is small, the curves almost coincide."),
        ("callout", "intuition", "What to notice", "Focal loss barely touches hard examples and strongly damps easy ones. As $p_t\\to0$ the factor $(1-p_t)^\\gamma\\to1$ and $\\mathrm{FL}\\approx\\mathrm{CE}$. As $p_t\\to1$ the loss decays like $(1-p_t)^{\\gamma+1}$ rather than $1-p_t$ for CE."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("eq", r"\mathrm{FL}(p_t)=-\,\alpha_t\,(1-p_t)^{\gamma}\,\log p_t,\qquad p_t=\begin{cases}p, & y=1,\\ 1-p, & y=0\end{cases}"),
        ("symbols", [
            (r"p=\sigma(z)", "the probability of class 1 that the model obtained from the logit $z$ (via the <a href=\"../sigmoid/\">sigmoid</a>; in the multi-class case via <a href=\"../softmax/\">softmax</a>);"),
            (r"p_t", "the probability of the <i>correct</i> class: how right the model is on this example; $p_t&gt;0.5$ means it is classified correctly;"),
            (r"-\log p_t", "ordinary cross-entropy: zero at $p_t=1$, infinity as $p_t\\to0$;"),
            (r"(1-p_t)^\gamma", "the modulating factor: “how wrong the model still is”, raised to the power $\\gamma$;"),
            (r"\gamma\ge0", "the focusing parameter: $\\gamma=0$ is CE, and the larger it is, the more easy examples are damped; RetinaNet uses $\\gamma=2$;"),
            (r"\alpha_t", "the class weight: $\\alpha$ for positives and $1-\\alpha$ for negatives; RetinaNet uses $\\alpha=0.25$."),
        ]),
        ("p", "Writing it through $p_t$ is the key trick: instead of the two branches of binary cross-entropy $-y\\log p-(1-y)\\log(1-p)$ there is one, $-\\log p_t$. In terms of the logit it is handy to set $z_t=z$ for $y=1$ and $z_t=-z$ for $y=0$; then $p_t=\\sigma(z_t)$."),
        ("table", ["$p_t$", "$\\mathrm{CE}$", "$(1-p_t)^2$", "$\\mathrm{FL}_{\\gamma=2}$", "$\\mathrm{CE}/\\mathrm{FL}$"], "TABLE", {"num": [0, 1, 2, 3, 4]}),
        ("p", "The last column says how many times focal loss is smaller than cross-entropy; it is exactly $1/(1-p_t)^\\gamma$. The example from the cheat sheet: with $\\gamma=2$ the easy example $p_t=0.9$ gives $0.00105$ versus $0.105$ (100 times less), the hard one $p_t=0.3$ gives $0.590$ versus $1.204$ (about half)."),
        ("p", "On an ordinary scale the values $0.001$ and $0.000001$ are indistinguishable, so it helps to look at the losses on a logarithmic scale, where the factor turns into a vertical shift."),
        ("viz", "focal-weight", {"gamma": 2, "pt": 0.9}, "<b>Figure 2.</b> Left: the modulating factor $(1-p_t)^\\gamma$ (the pale curves are $\\gamma=0.5,\\,1,\\,2,\\,5$). Right: CE and FL on a log scale; the arrow is the gap between them, the log of the factor. With $\\gamma=2$ the gap is 100 times at $p_t=0.9$ and 10,000 times at $p_t=0.99$."),
    ]),
    dict(id="properties", title="Properties", blocks=[
        ("ul", [
            "<b>Generalises cross-entropy</b>: $\\gamma=0$, $\\alpha_t=1$ give $\\mathrm{CE}=-\\log p_t$.",
            "<b>Never exceeds CE</b>: $0\\le\\mathrm{FL}\\le\\mathrm{CE}$, since $0\\le(1-p_t)^\\gamma\\le1$ for $\\gamma\\ge0$.",
            "<b>Decreasing in $p_t$</b>: both factors $(1-p_t)^\\gamma$ and $-\\log p_t$ are non-negative and decreasing, so the more confident the correct answer, the smaller the loss.",
            "<b>Behaviour at the edge</b>: as $p_t\\to1$, $\\mathrm{FL}\\approx(1-p_t)^{\\gamma+1}$, because $-\\log p_t\\approx1-p_t$.",
            "<b>Not convex in the logit</b> for $\\gamma&gt;0$: for very hard examples (with $\\gamma=2$, for $p_t&lt;0.058$, $z_t&lt;-2.79$) the second derivative with respect to $z_t$ is negative. Cross-entropy is convex in the logit everywhere.",
            "<b>Not a strictly proper scoring rule</b>: the minimum of the expected FL is not attained at the true probability. Hence probabilities learned with FL need calibration (see the section on $\\alpha$).",
        ]),
        ("callout", "note", "Compared with other ways to fight imbalance", "Class weighting ($\\alpha$) changes the weight of a whole <i>class</i>, equally for easy and hard examples. Resampling and hard negative mining throw part of the examples away by a hard rule. Focal loss changes the weight of <i>every example</i> smoothly, according to how well the model already handles it — and needs no sampling."),
    ]),
    dict(id="derivative", title="The derivative: the gradient with respect to the logit", blocks=[
        ("p", "The model learns through the gradient with respect to the logit $z$, so that gradient shows whom training “hears”. For cross-entropy it is simple: $\\partial\\,\\mathrm{CE}/\\partial z_t=-(1-p_t)$ — the bigger the error, the stronger the gradient, monotonically. Focal loss adds a second term."),
        ("deep", "Step-by-step derivation", [
            ("p", "Step 1. The derivative with respect to $p_t$ — the product rule for $-(1-p_t)^\\gamma\\log p_t$:"),
            ("eq", r"\frac{\partial\,\mathrm{FL}}{\partial p_t}=\gamma(1-p_t)^{\gamma-1}\log p_t-\frac{(1-p_t)^{\gamma}}{p_t}"),
            ("p", "Step 2. The derivative of the sigmoid: $\\partial p_t/\\partial z_t=p_t(1-p_t)$ (see the <a href=\"../sigmoid/\">sigmoid</a>)."),
            ("p", "Step 3. The chain rule, then factor out $(1-p_t)^\\gamma$:"),
            ("eq", r"\frac{\partial\,\mathrm{FL}}{\partial z_t}=\gamma p_t(1-p_t)^{\gamma}\log p_t-(1-p_t)^{\gamma+1}=(1-p_t)^{\gamma}\bigl(\gamma p_t\log p_t+p_t-1\bigr)"),
            ("p", "Step 4. For the original logit $z$: $z_t=\\pm z$, so $\\partial\\,\\mathrm{FL}/\\partial z=\\pm\\,\\partial\\,\\mathrm{FL}/\\partial z_t$ (plus for $y=1$, minus for $y=0$), and $\\alpha_t$ simply multiplies the result. Check: at $\\gamma=0$ we get $p_t-1$, the gradient of cross-entropy."),
        ]),
        ("eq", r"\left|\frac{\partial\,\mathrm{FL}}{\partial z_t}\right|=(1-p_t)^{\gamma}\Bigl[(1-p_t)+\gamma\,p_t\,|\log p_t|\Bigr]"),
        ("p", "Inside the brackets is the CE gradient, $1-p_t$, plus a non-negative extra term $\\gamma p_t|\\log p_t|$. Outside is the same factor $(1-p_t)^\\gamma$. For easy examples the factor wins, while for very hard ones the extra term can make the gradient even <b>larger</b> than for CE."),
        ("viz", "focal-grad", {"gamma": 2}, "<b>Figure 3.</b> The strength of the gradient with respect to the logit of the correct class. The grey dashed line is CE, $1-p_t$. The orange curve is FL: with $\\gamma=2$ the maximum $1.129$ is reached at $p_t=0.058$; for $p_t&lt;0.298$ the FL gradient is stronger than CE’s, and at $p_t=0.9$ it is only $0.029$ of the CE gradient (35 times smaller)."),
        ("callout", "warn", "The gradient is no longer monotonic", "With CE, the worse an example, the harder it pulls. With FL and $\\gamma&gt;0$ the strongest gradient belongs to examples with $p_t$ around a few per cent, and further towards $p_t\\to0$ it drops back to 1. For $\\gamma=1$ the border where FL pulls harder than CE is exactly $p_t=1/e\\approx0.368$. If the data contain wrong labels, they land precisely in this zone — and focal loss will diligently “learn” them."),
    ]),
    dict(id="surface", title="The surface FL(p_t, γ) in 3D", blocks=[
        ("p", "Let us gather the whole family of curves into one surface over the $(p_t,\\gamma)$ plane. The slice at $\\gamma=0$ is cross-entropy; moving along $\\gamma$, the surface “sinks”, and the larger $p_t$, the faster."),
        ("viz", "focal-surface", {"gamma": 2, "pt": 0.5}, "<b>Figure 4.</b> Left: $\\mathrm{FL}(p_t,\\gamma)$ (rotate it with the mouse); the blue line is the slice at the chosen $\\gamma$, the teal one at the chosen $p_t$. Right: the same teal curve on a log scale — a straight line with slope $\\ln(1-p_t)$. At $p_t=0.5$ and $\\gamma=2$: $\\mathrm{FL}=0.173$, slope $\\ln0.5=-0.693$."),
        ("p", "Why a straight line: $\\log\\mathrm{FL}=\\log\\mathrm{CE}+\\gamma\\log(1-p_t)$. The loss decays exponentially in $\\gamma$, at the rate $|\\ln(1-p_t)|$: $0.69$ per unit of $\\gamma$ for $p_t=0.5$, $2.30$ for $p_t=0.9$, $4.61$ for $p_t=0.99$. The parameter $\\gamma$ spreads easy and hard examples apart on a scale of orders of magnitude."),
    ]),
    dict(id="imbalance", title="Imbalance: where the loss comes from", blocks=[
        ("p", "Let us model a one-stage detector. There are 1000 negatives per positive. The negatives are mostly easy: the logit of the correct class is $z_t\\sim N(4,\\,1)$, so a typical $p_t=\\sigma(4)\\approx0.98$. The positives are hard: $z_t\\sim N(0,\\,1)$, a typical $p_t=0.5$. Let us compute what share of the total loss comes from each group."),
        ("viz", "focal-imbalance", {"gamma": 2, "ratio": 1000}, "<b>Figure 5.</b> Left: the share of the total loss in $p_t$ bins of width $0.05$ (grey — CE, blue — FL). Right: the make-up of the total. Easy negatives ($p_t\\ge0.9$) are $96.3\\%$ of the examples. Under CE they produce $78.1\\%$ of the loss, and the positives only $2.7\\%$. Under FL with $\\gamma=2$ the easy ones produce $9.0\\%$, and the positives $58.0\\%$."),
        ("p", "This is exactly the “focusing”. Gradient descent minimises the sum, and under CE that sum consists almost entirely of examples that are already solved. Focal loss redistributes the “attention budget”: the losses of easy examples are damped tens and hundreds of times, and the sum becomes dominated by hard negatives and positives — the ones on which the model can actually improve."),
        ("callout", "history", "RetinaNet", "Before 2017 one-stage detectors were noticeably less accurate than two-stage ones (Faster R-CNN). Two-stage detectors coped with imbalance thanks to the proposal stage and sampling positives and negatives at a 1 : 3 ratio. Lin and co-authors showed that the main reason for the gap was the imbalance itself, and a simple change of the loss (RetinaNet = ResNet + FPN + focal loss) let a one-stage detector overtake two-stage ones. The paper received the Best Student Paper award at ICCV 2017."),
    ]),
    dict(id="alpha", title="α-balancing and calibration", blocks=[
        ("p", "The factor $\\alpha_t$ is ordinary class weighting. Intuition suggests giving the rare class more weight: $\\alpha&gt;0.5$. Yet in RetinaNet the best value turned out to be $\\alpha=0.25$ — positives weigh <i>less</i> than negatives. The reason is that $\\gamma$ has already done the job: easy negatives are damped, and now the balance tilts towards the positives. $\\alpha$ and $\\gamma$ have to be tuned together; the authors recommend $\\gamma=2$, $\\alpha=0.25$, noting that the result is robust for $\\gamma$ in $[0.5,\\,5]$."),
        ("p", "There is also a subtlety that people forget. Take the simplest “model” — a single number $p$, the same for every example. If the share of positives is $\\pi$, cross-entropy is minimised exactly at $p=\\pi$: CE is a proper scoring rule, it teaches honest probabilities. With focal loss this is no longer true."),
        ("viz", "focal-prior", {"pi": 0.01, "gamma": 2, "alpha": 0.25}, "<b>Figure 6.</b> The mean loss of a constant prediction $p$, divided by its own minimum. The share of positives is $\\pi=0.01$. CE is minimal at $p=0.01$. FL with $\\gamma=2$, $\\alpha=0.25$ is minimal at $p=0.108$ (logit $-2.107$), i.e. the model overestimates the frequency of positives 11 times. Without $\\alpha$ ($\\alpha=0.5$) the minimum would be at $p=0.154$."),
        ("p", "The conclusion: the factor $(1-p_t)^\\gamma$ pulls predictions towards the middle — it “dislikes” confidence, because confidence stops being rewarded. So the output of a model trained with focal loss cannot be read as a probability: for thresholds and ranking that is fine, but if you need probabilities, calibrate them on validation data (Platt scaling, isotonic regression, temperature scaling)."),
        ("callout", "key", "Initialisation for a rare class", "At the start of training the network outputs $p\\approx0.5$ for every anchor, and the losses of 100,000 negatives blow up the first steps. That is why the bias of the last layer is initialised so that $p=\\pi$: $b=-\\ln\\frac{1-\\pi}{\\pi}$; for $\\pi=0.01$ this is $b\\approx-4.595$. In addition, the sum of FL over all anchors is divided by the number of <i>positive</i> anchors, not by the number of all of them."),
    ]),
    dict(id="training", title="Focal loss in training", blocks=[
        ("p", "Let us train logistic regression on two-dimensional data with a 1 : 20 imbalance (400 negatives, 20 positives) in two ways — with CE and with FL — from the same start (the bias initialised to the share of positives, as in RetinaNet) and with the same step. The size of each dot is proportional to its gradient $|\\partial L/\\partial z|$: this shows which examples training “hears”."),
        ("viz", "focal-train", {"gamma": 2}, "<b>Figure 7.</b> Left — CE, right — FL with $\\gamma=2$; the solid line is the boundary $p=0.5$, the dashed ones are $p=0.1$ and $p=0.9$. Press “Play”. At the start easy examples ($p_t&gt;0.9$) account for $50.0\\%$ of the total CE gradient and only $0.6\\%$ for FL; after 400 steps, $12.8\\%$ and $0.7\\%$. Both models find 13 positives of 20, with 3 and 4 false alarms respectively."),
        ("p", "What the figure shows. With CE large dots are scattered over the whole cloud of negatives: each of the 400 easy examples adds its own small portion of gradient. With FL only the dots near the boundary and the positives stay large — the rest almost vanish. The boundary itself comes out similar for the two models: for a linear model on such data the optimal direction is almost the same. The difference lies elsewhere: FL reaches its boundary in a few dozen steps and stops moving it, while CE keeps growing the weights, making easy examples even more confident. In a deep network with millions of parameters this difference is decisive: gradient spent on “obvious” background is network capacity not spent on hard cases."),
        ("eq", r"w\leftarrow w-\eta\,\frac1n\sum_{i=1}^{n}\frac{\partial\,\mathrm{FL}_i}{\partial z_i}\,x_i,\qquad \frac{\partial\,\mathrm{FL}_i}{\partial z_i}=\pm(1-p_{t,i})^{\gamma}\bigl(\gamma p_{t,i}\log p_{t,i}+p_{t,i}-1\bigr)"),
        ("callout", "warn", "An honest caveat", "Focal loss is not a magic cure for imbalance. If the model is simple and the classes are well separated, it gives almost the same boundary as CE, only with less confident probabilities. The gain appears where easy examples outnumber hard ones by orders of magnitude and really take the gradient away: dense detection, segmentation, large tables with a rare class."),
    ]),
    dict(id="code", title="In code", blocks=[
        ("p", "Compute focal loss from logits, not from probabilities: $\\log p_t=\\log\\sigma(z_t)=-\\operatorname{softplus}(-z_t)$ — no $\\log0$ and no overflow. Below is a NumPy version with the gradient and a check on the cheat-sheet example."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "In PyTorch the binary version ships with torchvision; the multi-class one is easy to write with <code>log_softmax</code>. The last line initialises the bias for a rare class."),
        ("code", "python", "CODE_TORCH"),
        ("callout", "note", "Checking the gradient", "The numerical derivative $\\bigl(\\mathrm{FL}(z+\\varepsilon)-\\mathrm{FL}(z-\\varepsilon)\\bigr)/2\\varepsilon$ with $\\varepsilon=10^{-6}$ matches <code>focal_grad</code> to four digits: $-0.0029$, $-0.697$, $0.0029$. At $p_t=0.3$ the FL and CE gradients are almost equal ($0.697$ versus $0.7$): this is close to the crossing point $p_t\\approx0.298$ in Figure 3."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>$\\alpha$ “by frequency” together with $\\gamma$.</b> Setting $\\alpha=0.99$ for a class with a 1% share at $\\gamma=2$ compensates twice. Start from $\\gamma=2$, $\\alpha=0.25$ and tune them together.",
            "<b>No initialisation for the rare class.</b> With a zero bias the first iterations drown in background losses; in the RetinaNet paper, training with plain CE without the $\\pi=0.01$ initialisation diverged.",
            "<b>Normalising by the number of all examples.</b> Averaging over 100,000 anchors makes the loss tiny and dependent on image size; in detection it is divided by the number of positives.",
            "<b>Focal loss on probabilities with a <code>clamp</code>.</b> $\\log(\\max(p,\\varepsilon))$ zeroes the gradient for the hardest examples. Compute from logits.",
            "<b>Reading the output as a probability.</b> FL shifts predictions towards the middle (Figure 6); for risk estimates and pricing, probabilities have to be calibrated.",
            "<b>A large $\\gamma$ with noisy labels.</b> Wrong labels look like very hard examples, and FL increases their relative weight. If you suspect noise, lower $\\gamma$ or clean the labels.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../bce/\">BCE</a> and <a href=\"../cross-entropy/\">cross-entropy</a>: FL with $\\gamma=0$, $\\alpha_t=1$ coincides with them.",
            "<a href=\"../sigmoid/\">The sigmoid</a>: $p_t=\\sigma(z_t)$, and its derivative $p_t(1-p_t)$ enters the FL gradient.",
            "<a href=\"../softmax/\">Softmax</a>: in the multi-class case $p_t$ is the softmax component of the correct class.",
            "<a href=\"../huber/\">Huber</a> is the opposite philosophy: Huber <i>weakens</i> the contribution of the largest errors, treating them as outliers, while FL weakens the <i>smallest</i> ones so that the large ones stand out.",
            "<a href=\"../triplet/\">Triplet loss</a> solves a related problem in metric learning: easy triplets with zero loss give no gradient, and training focuses on the hard ones (hard negative mining).",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $\\mathrm{FL}=-\\alpha_t(1-p_t)^\\gamma\\log p_t$ is cross-entropy multiplied by the “degree of error” $(1-p_t)^\\gamma$; $\\gamma=0$ gives CE. 2) Easy examples are damped like $(1-p_t)^{\\gamma+1}$: with $\\gamma=2$ an example with $p_t=0.9$ weighs 100 times less. 3) The gradient with respect to the logit, $(1-p_t)^\\gamma(\\gamma p_t\\log p_t+p_t-1)$, is not monotonic: with $\\gamma=2$ its maximum is at $p_t\\approx0.06$. 4) At a 1 : 1000 imbalance FL moves most of the loss from easy negatives to positives and hard negatives. 5) RetinaNet practice: $\\gamma=2$, $\\alpha=0.25$, the initialisation $b=-\\ln\\frac{1-\\pi}{\\pi}$, normalisation by the number of positives; the output probabilities need calibration."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="The model gave the correct class a probability $p_t=0.8$. What is the modulating factor at $\\gamma=2$?", options=["$0.64$", "$0.2$", "$0.04$", "$0.8$"], answer=2,
                 explain="$(1-p_t)^\\gamma=0.2^2=0.04$: the loss of this example is 25 times smaller than in CE."),
            dict(q="What does focal loss become with $\\gamma=0$ and $\\alpha_t=1$?", options=["MSE", "Cross-entropy", "Hinge loss", "Zero"], answer=1,
                 explain="The factor $(1-p_t)^0=1$, leaving $-\\log p_t$ — cross-entropy."),
            dict(q="How does the FL gradient with respect to the logit behave at $\\gamma=2$ as a function of $p_t$?", options=["It decreases monotonically, like CE’s", "It grows with $p_t$", "It first grows, peaks around $p_t\\approx0.06$, then falls fast", "It is constant"], answer=2,
                 explain="$|\\partial\\mathrm{FL}/\\partial z_t|=(1-p_t)^\\gamma[(1-p_t)+\\gamma p_t|\\log p_t|]$: it equals 1 as $p_t\\to0$, grows to $1.129$ at $p_t\\approx0.058$ and then decreases."),
            dict(q="Why does RetinaNet use $\\alpha=0.25$ rather than, say, $0.99$ for the rare object class?", options=["It is a typo in the paper", "$\\gamma$ has already damped the easy negatives, and a strong extra tilt towards positives would be too much", "$\\alpha$ does not affect training", "Objects are not actually rare"], answer=1,
                 explain="After the modulating factor most of the loss already comes from positives and hard negatives; $\\alpha$ and $\\gamma$ are tuned together, and $\\alpha=0.25$ turned out best."),
            dict(q="A model is trained with focal loss, $\\gamma=2$. What is true about its output probabilities?", options=["They are perfectly calibrated", "They are pulled towards the middle and need calibration", "They are always 0 or 1", "They coincide with a CE model’s"], answer=1,
                 explain="FL is not a proper scoring rule: even for a constant prediction the minimum is not at $p=\\pi$ (Figure 6: $0.108$ instead of $0.01$)."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "RetinaNet kabi obyekt detektori bitta rasmda yuz mingga yaqin «anchor»ni — har birida obyekt bo‘lishi mumkin bo‘lgan to‘rtburchaklarni tekshiradi. Kadrda obyektlar bir nechta, qolgan hammasi — fon. Ko‘pchilik fon anchorlari arzimas: osmon, devor, asfalt. Model ularni ishonch bilan fon deb atashni tez o‘rganadi, lekin <a href=\"../cross-entropy/\">kross-entropiya</a> baribir har biri uchun kichik yo‘qotish hisoblaydi. Yuz ming kichik yo‘qotish kattasiga qo‘shiladi — va bu yig‘indi hamma narsa aynan ular uchun qilingan bir nechta qiyin misollar signalini bosib ketadi."),
        ("p", "Lin, Goyal, Girshik, Xe va Dollar (2017) oson misollarni tashlab yubormaslikni va ma’lumotlarni qayta tanlamaslikni, balki <b>yo‘qotishning o‘zini o‘zgartirishni</b> taklif qildi: kross-entropiyani $(1-p_t)^\\gamma$ ga ko‘paytirish. Ishonch bilan tanilgan misol uchun ko‘paytuvchi deyarli nol, qiyini uchun deyarli bir. U qayerda qo‘llaniladi:"),
        ("ul", [
            "<b>bir bosqichli detektorlar</b> — RetinaNet, undan keyin FCOS, ATSS va boshqa zich detektorlar;",
            "<b>segmentatsiya</b> — ayniqsa tibbiy, bu yerda qiziqish sohasi piksellarning foiz ulushlarini egallaydi (ko‘pincha Dice bilan juftlikda);",
            "<b>kamyob sinfli jadval masalalari</b> — firibgarlik, mijozlar ketishi, anomaliyalar; bustingda focal loss foydalanuvchi maqsad funksiyasi sifatida beriladi;",
            "<b>«shovqinli» ishonchli klassifikatsiya</b> — focal loss ba’zan tarmoq haddan tashqari ishonchli bo‘lib ketmasligi uchun qo‘llaniladi.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "$p_t$ — model to‘g‘ri sinfga bergan ehtimollik. $\\mathrm{FL}=-(1-p_t)^\\gamma\\log p_t$: $\\gamma=0$ da bu oddiy kross-entropiya, $\\gamma=2$ da $p_t=0{,}9$ li misol 100 marta yengil, $p_t=0{,}3$ lisi esa atigi 2 marta yengil. $\\alpha_t$ ko‘paytuvchi qo‘shimcha ravishda sinflar vaznini beradi. Narxi — model kalibrlangan ehtimolliklar berishni to‘xtatadi."),
    ]),
    dict(id="intuition", title="Intuitsiya: har bir misol uchun ovoz balandligi", blocks=[
        ("p", "O‘qituvchi o‘quvchilar savollariga javob beradigan sinfni tasavvur qiling. Ming o‘quvchi javobini o‘zi biladigan savollarni beradi, yigirmatasi esa haqiqatan qiyinlarini. Agar har bir savolga bir xil vaqt ajratilsa, qiyinlariga vaqt qolmaydi. Focal loss — ovoz balandligi regulyatori: model misolga qanchalik ishonch bilan javob bersa, uning umumiy yig‘indidagi ovozi shunchalik past."),
        ("p", "Nuqtani torting va $\\gamma$ ni o‘zgartiring. Kulrang shtrixli egri chiziq — kross-entropiya $-\\ln p_t$. Ko‘k — focal loss: misollar allaqachon to‘g‘ri klassifikatsiya qilingan o‘ng yarmida u nolga ancha erta yopishadi."),
        ("viz", "focal-curves", {"gamma": 2, "pt": 0.9}, "<b>1-rasm.</b> $\\gamma=0;\\,0{,}5;\\,1;\\,2;\\,5$ uchun $\\mathrm{FL}(p_t)$ oilasi (RetinaNet maqolasining 1-rasmidagi kabi). $\\gamma=2$ va $p_t=0{,}9$ da: $\\mathrm{CE}=0{,}105$, $(1-p_t)^2=0{,}01$ ko‘paytuvchi, $\\mathrm{FL}=0{,}00105$ — 100 marta kichik. Chapda, $p_t$ kichik joyda, egri chiziqlar deyarli mos tushadi."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "Focal loss qiyin misollarga deyarli tegmaydi va oson misollarni juda kuchli so‘ndiradi. $p_t\\to0$ da $(1-p_t)^\\gamma\\to1$ va $\\mathrm{FL}\\approx\\mathrm{CE}$. $p_t\\to1$ da yo‘qotish CE’dagidek $1-p_t$ kabi emas, $(1-p_t)^{\\gamma+1}$ kabi kamayadi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("eq", r"\mathrm{FL}(p_t)=-\,\alpha_t\,(1-p_t)^{\gamma}\,\log p_t,\qquad p_t=\begin{cases}p, & y=1,\\ 1-p, & y=0\end{cases}"),
        ("symbols", [
            (r"p=\sigma(z)", "model $z$ logitdan olgan 1-sinf ehtimolligi (<a href=\"../sigmoid/\">sigmoida</a> orqali; ko‘p sinfli holatda — <a href=\"../softmax/\">softmax</a> orqali);"),
            (r"p_t", "<i>to‘g‘ri</i> sinf ehtimolligi: model bu misolda qanchalik haq; $p_t&gt;0{,}5$ — misol to‘g‘ri klassifikatsiya qilingan;"),
            (r"-\log p_t", "oddiy kross-entropiya: $p_t=1$ da nol, $p_t\\to0$ da cheksizlik;"),
            (r"(1-p_t)^\gamma", "modulyatsiyalovchi ko‘paytuvchi (modulating factor): «model hali qanchalik adashyapti» $\\gamma$ darajasida;"),
            (r"\gamma\ge0", "fokuslash parametri (focusing parameter): $\\gamma=0$ — CE, qancha katta bo‘lsa, oson misollar shuncha kuchli so‘ndiriladi; RetinaNet’da $\\gamma=2$;"),
            (r"\alpha_t", "sinf vazni: pozitivlar uchun $\\alpha$, negativlar uchun $1-\\alpha$; RetinaNet’da $\\alpha=0{,}25$."),
        ]),
        ("p", "$p_t$ orqali yozish — asosiy usul: binar kross-entropiyaning $-y\\log p-(1-y)\\log(1-p)$ ikki tarmog‘i o‘rniga bitta, $-\\log p_t$ hosil bo‘ladi. Logit tilida $y=1$ da $z_t=z$ va $y=0$ da $z_t=-z$ deb kiritish qulay; shunda $p_t=\\sigma(z_t)$."),
        ("table", ["$p_t$", "$\\mathrm{CE}$", "$(1-p_t)^2$", "$\\mathrm{FL}_{\\gamma=2}$", "$\\mathrm{CE}/\\mathrm{FL}$"], "TABLE", {"num": [0, 1, 2, 3, 4]}),
        ("p", "Oxirgi ustun — focal loss kross-entropiyadan necha marta kichik; bu aynan $1/(1-p_t)^\\gamma$. Qo‘llanmadagi misol: $\\gamma=2$ da $p_t=0{,}9$ li oson misol $0{,}105$ ga qarshi $0{,}00105$ beradi (100 marta kam), $p_t=0{,}3$ li qiyini — $1{,}204$ ga qarshi $0{,}590$ (taxminan ikki marta)."),
        ("p", "Oddiy shkalada $0{,}001$ va $0{,}000001$ qiymatlarini farqlab bo‘lmaydi, shuning uchun yo‘qotishlarni logarifmik shkalada ko‘rish foydali: u yerda ko‘paytuvchi vertikal siljishga aylanadi."),
        ("viz", "focal-weight", {"gamma": 2, "pt": 0.9}, "<b>2-rasm.</b> Chapda — $(1-p_t)^\\gamma$ modulyatsiyalovchi ko‘paytuvchi (och egri chiziqlar — $\\gamma=0{,}5;\\,1;\\,2;\\,5$). O‘ngda — logarifmik shkaladagi CE va FL; strelka — ular orasidagi farq, ko‘paytuvchi logarifmi. $\\gamma=2$ da: $p_t=0{,}9$ da farq 100 marta, $p_t=0{,}99$ da — 10 000 marta."),
    ]),
    dict(id="properties", title="Xossalar", blocks=[
        ("ul", [
            "<b>Kross-entropiyani umumlashtiradi</b>: $\\gamma=0$, $\\alpha_t=1$ da $\\mathrm{CE}=-\\log p_t$ chiqadi.",
            "<b>CE dan katta emas</b>: $0\\le\\mathrm{FL}\\le\\mathrm{CE}$, chunki $\\gamma\\ge0$ da $0\\le(1-p_t)^\\gamma\\le1$.",
            "<b>$p_t$ bo‘yicha kamayadi</b>: $(1-p_t)^\\gamma$ va $-\\log p_t$ ko‘paytuvchilarining ikkalasi manfiy emas va kamayuvchi, shuning uchun to‘g‘ri javob qancha ishonchli bo‘lsa, yo‘qotish shuncha kichik.",
            "<b>Chekkadagi xulq</b>: $p_t\\to1$ da $\\mathrm{FL}\\approx(1-p_t)^{\\gamma+1}$, chunki $-\\log p_t\\approx1-p_t$.",
            "<b>Logit bo‘yicha qavariq emas</b> $\\gamma&gt;0$ da: juda qiyin misollar uchun ($\\gamma=2$ da — $p_t&lt;0{,}058$, $z_t&lt;-2{,}79$ uchun) $z_t$ bo‘yicha ikkinchi hosila manfiy. Kross-entropiya logit bo‘yicha hamma joyda qavariq.",
            "<b>Qat’iy xos baholash qoidasi emas</b> (proper scoring rule): kutilgan FL minimumiga haqiqiy ehtimollikda erishilmaydi. Shuning uchun FL da o‘rganilgan ehtimolliklarni kalibrlash kerak ($\\alpha$ bo‘limiga qarang).",
        ]),
        ("callout", "note", "Muvozanatsizlikka qarshi boshqa usullar bilan taqqoslash", "Sinflarni vaznlash ($\\alpha$) butun <i>sinf</i> vaznini oson va qiyin misollar uchun bir xil o‘zgartiradi. Qayta tanlash va hard negative mining misollarning bir qismini qat’iy qoida bo‘yicha tashlab yuboradi. Focal loss <i>har bir misol</i> vaznini model u bilan qanchalik uddalayotganiga qarab ravon o‘zgartiradi — va tanlashni talab qilmaydi."),
    ]),
    dict(id="derivative", title="Hosila: logit bo‘yicha gradiyent", blocks=[
        ("p", "Model $z$ logit bo‘yicha gradiyent orqali o‘rganadi, shuning uchun aynan u o‘qitish kimni «eshitishini» ko‘rsatadi. Kross-entropiya uchun u oddiy: $\\partial\\,\\mathrm{CE}/\\partial z_t=-(1-p_t)$ — xato qancha katta bo‘lsa, gradiyent shuncha kuchli, monoton. Focal loss’da ikkinchi had paydo bo‘ladi."),
        ("deep", "Qadam-baqadam keltirib chiqarish", [
            ("p", "1-qadam. $p_t$ bo‘yicha hosila — $-(1-p_t)^\\gamma\\log p_t$ uchun ko‘paytma qoidasi:"),
            ("eq", r"\frac{\partial\,\mathrm{FL}}{\partial p_t}=\gamma(1-p_t)^{\gamma-1}\log p_t-\frac{(1-p_t)^{\gamma}}{p_t}"),
            ("p", "2-qadam. Sigmoida hosilasi: $\\partial p_t/\\partial z_t=p_t(1-p_t)$ (<a href=\"../sigmoid/\">sigmoida</a>ga qarang)."),
            ("p", "3-qadam. Zanjir qoidasi va umumiy $(1-p_t)^\\gamma$ ko‘paytuvchini qavsdan chiqarish:"),
            ("eq", r"\frac{\partial\,\mathrm{FL}}{\partial z_t}=\gamma p_t(1-p_t)^{\gamma}\log p_t-(1-p_t)^{\gamma+1}=(1-p_t)^{\gamma}\bigl(\gamma p_t\log p_t+p_t-1\bigr)"),
            ("p", "4-qadam. Dastlabki $z$ logit uchun: $z_t=\\pm z$, shuning uchun $\\partial\\,\\mathrm{FL}/\\partial z=\\pm\\,\\partial\\,\\mathrm{FL}/\\partial z_t$ ($y=1$ da plyus, $y=0$ da minus), $\\alpha_t$ esa natijani shunchaki ko‘paytiradi. Tekshiruv: $\\gamma=0$ da $p_t-1$, ya’ni kross-entropiya gradiyenti chiqadi."),
        ]),
        ("eq", r"\left|\frac{\partial\,\mathrm{FL}}{\partial z_t}\right|=(1-p_t)^{\gamma}\Bigl[(1-p_t)+\gamma\,p_t\,|\log p_t|\Bigr]"),
        ("p", "Kvadrat qavs ichida — CE gradiyenti $1-p_t$ va manfiy bo‘lmagan $\\gamma p_t|\\log p_t|$ qo‘shimcha. Tashqarida — o‘sha $(1-p_t)^\\gamma$ ko‘paytuvchi. Oson misollar uchun ko‘paytuvchi g‘olib chiqadi, juda qiyinlari uchun esa qo‘shimcha gradiyentni CE’dagidan hatto <b>kattaroq</b> qilishi mumkin."),
        ("viz", "focal-grad", {"gamma": 2}, "<b>3-rasm.</b> To‘g‘ri sinf logiti bo‘yicha gradiyent kuchi. Kulrang shtrix — CE, $1-p_t$. To‘q sariq — FL: $\\gamma=2$ da $1{,}129$ maksimumga $p_t=0{,}058$ da erishiladi, $p_t&lt;0{,}298$ da FL gradiyenti CE’nikidan kuchli, $p_t=0{,}9$ da esa u CE gradiyentining atigi $0{,}029$ qismini tashkil qiladi (35 marta kichik)."),
        ("callout", "warn", "Gradiyent endi monoton emas", "CE’da misol qancha yomon bo‘lsa, shuncha kuchli tortadi. $\\gamma&gt;0$ li FL’da eng kuchli gradiyent $p_t$ bir necha foiz atrofidagi misollarda, $p_t\\to0$ tomon esa u yana 1 gacha tushadi. $\\gamma=1$ uchun FL CE’dan kuchliroq tortadigan chegara aynan $p_t=1/e\\approx0{,}368$. Agar ma’lumotlarda xato belgilar bo‘lsa, ular aynan shu zonaga tushadi — focal loss ularni zo‘r berib «o‘rganadi»."),
    ]),
    dict(id="surface", title="FL(p_t, γ) sirti 3D’da", blocks=[
        ("p", "Butun egri chiziqlar oilasini $(p_t,\\gamma)$ tekisligi ustidagi bitta sirtga yig‘amiz. $\\gamma=0$ dagi kesim — kross-entropiya; $\\gamma$ bo‘yicha harakatlanganda sirt «cho‘kadi», $p_t$ qancha katta bo‘lsa, shuncha tez."),
        ("viz", "focal-surface", {"gamma": 2, "pt": 0.5}, "<b>4-rasm.</b> Chapda — $\\mathrm{FL}(p_t,\\gamma)$ (sichqoncha bilan aylantiring), ko‘k chiziq — tanlangan $\\gamma$ dagi kesim, firuza — tanlangan $p_t$ dagi kesim. O‘ngda — o‘sha firuza egri chiziq logarifmik shkalada: bu $\\ln(1-p_t)$ qiyalikli to‘g‘ri chiziq. $p_t=0{,}5$ va $\\gamma=2$ da: $\\mathrm{FL}=0{,}173$, qiyalik $\\ln0{,}5=-0{,}693$."),
        ("p", "Nega to‘g‘ri chiziq: $\\log\\mathrm{FL}=\\log\\mathrm{CE}+\\gamma\\log(1-p_t)$. $\\gamma$ bo‘yicha yo‘qotish eksponensial so‘nadi, so‘nish tezligi — $|\\ln(1-p_t)|$: $p_t=0{,}5$ uchun $\\gamma$ birligiga $0{,}69$, $p_t=0{,}9$ uchun — $2{,}30$, $p_t=0{,}99$ uchun — $4{,}61$. $\\gamma$ parametri oson va qiyin misollarni tartiblar shkalasi bo‘yicha bir-biridan uzoqlashtiradi."),
    ]),
    dict(id="imbalance", title="Muvozanatsizlik: yo‘qotish qayerdan keladi", blocks=[
        ("p", "Bir bosqichli detektor holatini modellashtiramiz. Har bir pozitivga 1000 ta negativ to‘g‘ri keladi. Negativlar asosan oson: to‘g‘ri sinf logiti $z_t\\sim N(4,\\,1)$, ya’ni tipik $p_t=\\sigma(4)\\approx0{,}98$. Pozitivlar qiyin: $z_t\\sim N(0,\\,1)$, tipik $p_t=0{,}5$. Umumiy yo‘qotishning qancha ulushi har bir guruhga to‘g‘ri kelishini hisoblaymiz."),
        ("viz", "focal-imbalance", {"gamma": 2, "ratio": 1000}, "<b>5-rasm.</b> Chapda — $0{,}05$ kenglikdagi $p_t$ savatlari bo‘yicha umumiy yo‘qotish ulushi (kulranglar — CE, ko‘klar — FL). O‘ngda — yig‘indi tarkibi. Oson negativlar ($p_t\\ge0{,}9$) — misollarning $96{,}3\\%$ i. CE’da ular yo‘qotishning $78{,}1\\%$ ini beradi, pozitivlar esa atigi $2{,}7\\%$ ini. $\\gamma=2$ li FL’da osonlar $9{,}0\\%$, pozitivlar esa $58{,}0\\%$ beradi."),
        ("p", "Aynan shu «fokuslash». Gradiyent tushish yig‘indini minimallashtiradi, CE’da esa bu yig‘indi deyarli butunlay allaqachon yechilgan misollardan iborat. Focal loss «e’tibor byudjeti»ni qayta taqsimlaydi: oson misollar yo‘qotishlari o‘nlab va yuzlab marta so‘ndiriladi, yig‘indida esa qiyin negativlar va pozitivlar — model haqiqatan yaxshilanishi mumkin bo‘lganlar — ustunlik qila boshlaydi."),
        ("callout", "history", "RetinaNet", "2017 yilgacha bir bosqichli detektorlar aniqlikda ikki bosqichlilardan (Faster R-CNN) sezilarli ortda qolardi. Ikki bosqichlilar muvozanatsizlikni takliflar bosqichi va pozitiv hamda negativlarni 1 : 3 nisbatda tanlash hisobiga yengardi. Lin va hammualliflar ortda qolishning asosiy sababi aynan muvozanatsizlik ekanini ko‘rsatdi, va yo‘qotishni oddiygina almashtirish (RetinaNet = ResNet + FPN + focal loss) bir bosqichli detektorga ikki bosqichlilardan o‘zib ketish imkonini berdi. Ish ICCV 2017 da eng yaxshi talabalik maqolasi mukofotini oldi."),
    ]),
    dict(id="alpha", title="α-muvozanatlash va kalibrlash", blocks=[
        ("p", "$\\alpha_t$ ko‘paytuvchi — oddiy sinflarni vaznlash. Intuitsiya kamyob sinfga kattaroq vazn berishni taklif qiladi: $\\alpha&gt;0{,}5$. Lekin RetinaNet’da eng yaxshisi $\\alpha=0{,}25$ bo‘lib chiqdi — pozitivlar negativlardan <i>yengilroq</i>. Sababi — $\\gamma$ ishni allaqachon qilib bo‘lgan: oson negativlar so‘ndirilgan va endi ustunlik ko‘proq pozitivlarda. $\\alpha$ va $\\gamma$ ni birga tanlash kerak; mualliflar $\\gamma=2$, $\\alpha=0{,}25$ ni tavsiya qiladi va natija $[0{,}5;\\,5]$ oraliqdagi $\\gamma$ ga barqaror ekanini ta’kidlaydi."),
        ("p", "Unutiladigan nozik jihat ham bor. Eng oddiy «model»ni olamiz — barcha misollar uchun bir xil bitta $p$ son. Agar pozitivlar ulushi $\\pi$ bo‘lsa, kross-entropiya aynan $p=\\pi$ da minimal: CE — xos baholash qoidasi, u halol ehtimolliklarga o‘rgatadi. Focal loss bilan bu endi unday emas."),
        ("viz", "focal-prior", {"pi": 0.01, "gamma": 2, "alpha": 0.25}, "<b>6-rasm.</b> O‘zgarmas $p$ bashoratning o‘z minimumiga bo‘lingan o‘rtacha yo‘qotishi. Pozitivlar ulushi $\\pi=0{,}01$. CE $p=0{,}01$ da minimal. $\\gamma=2$, $\\alpha=0{,}25$ li FL — $p=0{,}108$ da (logit $-2{,}107$), ya’ni model pozitivlar chastotasini 11 marta oshirib baholaydi. $\\alpha$ siz ($\\alpha=0{,}5$) minimum $p=0{,}154$ da bo‘lardi."),
        ("p", "Xulosa: $(1-p_t)^\\gamma$ ko‘paytuvchi bashoratlarni o‘rtaga tortadi — u ishonchni «yoqtirmaydi», chunki ishonch uchun to‘lov to‘xtaydi. Shuning uchun focal loss’da o‘qitilgan model chiqishini ehtimollik deb o‘qib bo‘lmaydi: chegaralar va tartiblash uchun bu normal, ehtimolliklar kerak bo‘lsa — ularni validatsiyada kalibrlang (Platt scaling, izotonik regressiya, harorat bilan shkalalash)."),
        ("callout", "key", "Kamyob sinf uchun boshlang‘ich qiymat", "O‘qitish boshida tarmoq barcha anchorlar uchun $p\\approx0{,}5$ beradi, va 100 000 negativ yo‘qotishlari birinchi qadamlarni portlatib yuboradi. Shuning uchun oxirgi qatlam siljishi $p=\\pi$ bo‘ladigan qilib boshlanadi: $b=-\\ln\\frac{1-\\pi}{\\pi}$; $\\pi=0{,}01$ uchun bu $b\\approx-4{,}595$. Bundan tashqari, barcha anchorlar bo‘yicha FL yig‘indisi barcha anchorlar soniga emas, <i>pozitiv</i> anchorlar soniga bo‘linadi."),
    ]),
    dict(id="training", title="O‘qitishda focal loss", blocks=[
        ("p", "Logistik regressiyani 1 : 20 muvozanatsizlikdagi (400 negativ, 20 pozitiv) ikki o‘lchovli ma’lumotlarda ikki usulda — CE va FL bilan — bir xil boshlanish (siljish RetinaNet’dagidek pozitivlar ulushiga moslab boshlangan) va bir xil qadam bilan o‘qitamiz. Har bir nuqta o‘lchami uning $|\\partial L/\\partial z|$ gradiyentiga proporsional: shunda o‘qitish qaysi misollarni «eshitishi» ko‘rinadi."),
        ("viz", "focal-train", {"gamma": 2}, "<b>7-rasm.</b> Chapda — CE, o‘ngda — $\\gamma=2$ li FL; yaxlit chiziq — $p=0{,}5$ chegara, shtrixlar — $p=0{,}1$ va $p=0{,}9$. «Boshlash»ni bosing. Boshida oson misollarga ($p_t&gt;0{,}9$) CE umumiy gradiyentining $50{,}0\\%$ i, FL’da esa atigi $0{,}6\\%$ i to‘g‘ri keladi; 400 qadamdan keyin — $12{,}8\\%$ va $0{,}7\\%$. Ikkala model ham 20 tadan 13 ta pozitivni mos ravishda 3 va 4 ta soxta signal bilan topadi."),
        ("p", "Rasmda nima ko‘rinadi. CE’da yirik nuqtalar butun negativlar buluti bo‘ylab sochilgan: 400 ta oson misolning har biri gradiyentning o‘z kichik ulushini qo‘shadi. FL’da faqat chegaradagi nuqtalar va pozitivlar yirik qoladi — qolganlari deyarli yo‘qoladi. Chegaraning o‘zi ikki modelda o‘xshash chiqadi: bunday ma’lumotlardagi chiziqli model uchun optimal yo‘nalish deyarli bir xil. Farq boshqa joyda: FL o‘z chegarasiga bir necha o‘n qadamda yetib boradi va uni boshqa siljitmaydi, CE esa vaznlarni oshirishda davom etib, oson misollarni yanada ishonchliroq qiladi. Millionlab parametrli chuqur tarmoqda bu farq hal qiluvchi: «baribir tushunarli» fonga sarflangan gradiyent — qiyin holatlarga sarflanmagan tarmoq sig‘imi."),
        ("eq", r"w\leftarrow w-\eta\,\frac1n\sum_{i=1}^{n}\frac{\partial\,\mathrm{FL}_i}{\partial z_i}\,x_i,\qquad \frac{\partial\,\mathrm{FL}_i}{\partial z_i}=\pm(1-p_{t,i})^{\gamma}\bigl(\gamma p_{t,i}\log p_{t,i}+p_{t,i}-1\bigr)"),
        ("callout", "warn", "Halol izoh", "Focal loss muvozanatsizlikka qarshi sehrli vosita emas. Agar model oddiy, sinflar esa yaxshi ajraladigan bo‘lsa, u CE bilan deyarli bir xil chegarani, faqat kamroq ishonchli ehtimolliklar bilan beradi. Yutuq oson misollar qiyinlaridan tartiblarga ko‘p bo‘lgan va gradiyentni haqiqatan tortib oladigan joyda paydo bo‘ladi: zich aniqlash, segmentatsiya, kamyob sinfli katta jadvallar."),
    ]),
    dict(id="code", title="Kodda", blocks=[
        ("p", "Focal loss’ni ehtimolliklar bo‘yicha emas, logitlar bo‘yicha hisoblang: $\\log p_t=\\log\\sigma(z_t)=-\\operatorname{softplus}(-z_t)$ — $\\log0$ va to‘lib ketishsiz. Quyida — gradiyentli va qo‘llanmadagi misolda tekshiriladigan NumPy versiyasi."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "PyTorch’da binar versiya torchvision’da bor; ko‘p sinflisini <code>log_softmax</code> orqali yozish oson. Oxirgi qator — siljishni kamyob sinfga moslab boshlash."),
        ("code", "python", "CODE_TORCH"),
        ("callout", "note", "Gradiyentni tekshirish", "$\\varepsilon=10^{-6}$ dagi $\\bigl(\\mathrm{FL}(z+\\varepsilon)-\\mathrm{FL}(z-\\varepsilon)\\bigr)/2\\varepsilon$ sonli hosila <code>focal_grad</code> bilan to‘rt xonagacha mos keladi: $-0{,}0029$, $-0{,}697$, $0{,}0029$. $p_t=0{,}3$ da FL va CE gradiyentlari deyarli teng ($0{,}7$ ga qarshi $0{,}697$): bu 3-rasmdagi $p_t\\approx0{,}298$ kesishish nuqtasiga yaqin."),
    ]),
    dict(id="mistakes", title="Keng tarqalgan xatolar", blocks=[
        ("ol", [
            "<b>$\\gamma$ bilan birga «chastota bo‘yicha» $\\alpha$.</b> $\\gamma=2$ da ulushi 1% bo‘lgan sinf uchun $\\alpha=0{,}99$ qo‘yish — ikki karra kompensatsiya. $\\gamma=2$, $\\alpha=0{,}25$ dan boshlang va ularni birga tanlang.",
            "<b>Kamyob sinf uchun boshlang‘ich qiymat yo‘q.</b> Siljish 0 bo‘lganda birinchi iteratsiyalar fon yo‘qotishlariga cho‘kadi; RetinaNet maqolasida oddiy CE bilan $\\pi=0{,}01$ boshlang‘ich qiymatsiz o‘qitish uzoqlashib ketgan.",
            "<b>Barcha misollar soniga normallash.</b> 100 000 anchor bo‘yicha o‘rtacha yo‘qotishni juda kichik va rasm o‘lchamiga bog‘liq qiladi; aniqlashda pozitivlar soniga bo‘linadi.",
            "<b><code>clamp</code> bilan ehtimolliklar bo‘yicha focal loss.</b> $\\log(\\max(p,\\varepsilon))$ eng qiyin misollar uchun gradiyentni nolga aylantiradi. Logitlar bo‘yicha hisoblang.",
            "<b>Chiqishni ehtimollik deb o‘qish.</b> FL bashoratlarni o‘rtaga suradi (6-rasm); xavflarni baholash va narxlash uchun ehtimolliklarni kalibrlash kerak.",
            "<b>Shovqinli belgilarda katta $\\gamma$.</b> Xato belgilar juda qiyin misollarga o‘xshaydi, FL esa ularning nisbiy vaznini oshiradi. Shovqin gumoni bo‘lsa, $\\gamma$ ni kamaytiring yoki belgilashni tozalang.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘liqlik", blocks=[
        ("ul", [
            "<a href=\"../bce/\">BCE</a> va <a href=\"../cross-entropy/\">kross-entropiya</a>: $\\gamma=0$, $\\alpha_t=1$ li FL ular bilan mos keladi.",
            "<a href=\"../sigmoid/\">Sigmoida</a>: $p_t=\\sigma(z_t)$, uning $p_t(1-p_t)$ hosilasi esa FL gradiyentiga kiradi.",
            "<a href=\"../softmax/\">Softmax</a>: ko‘p sinfli holatda $p_t$ — to‘g‘ri sinf uchun softmax komponentasi.",
            "<a href=\"../huber/\">Huber</a> — qarama-qarshi falsafa: Huber eng katta xatolarni chetga chiquvchi deb hisoblab ularning hissasini <i>susaytiradi</i>, FL esa kattalari ko‘zga tashlanishi uchun eng <i>kichiklarini</i> susaytiradi.",
            "<a href=\"../triplet/\">Triplet loss</a> metrikani o‘qitishda qarindosh masalani yechadi: nol yo‘qotishli oson uchliklar gradiyent bermaydi va o‘qitish qiyinlariga qaratiladi (hard negative mining).",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $\\mathrm{FL}=-\\alpha_t(1-p_t)^\\gamma\\log p_t$ — «xato darajasi» $(1-p_t)^\\gamma$ ga ko‘paytirilgan kross-entropiya; $\\gamma=0$ — CE. 2) Oson misollar $(1-p_t)^{\\gamma+1}$ kabi so‘ndiriladi: $\\gamma=2$ da $p_t=0{,}9$ li misol 100 marta yengil. 3) Logit bo‘yicha $(1-p_t)^\\gamma(\\gamma p_t\\log p_t+p_t-1)$ gradiyent monoton emas: $\\gamma=2$ da maksimum $p_t\\approx0{,}06$ da. 4) 1 : 1000 muvozanatsizlikda FL yo‘qotishning asosiy qismini oson negativlardan pozitivlar va qiyin negativlarga ko‘chiradi. 5) RetinaNet amaliyoti: $\\gamma=2$, $\\alpha=0{,}25$, $b=-\\ln\\frac{1-\\pi}{\\pi}$ boshlang‘ich qiymat, pozitivlar soniga normallash; chiqishdagi ehtimolliklarni kalibrlash kerak."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="Model to‘g‘ri sinfga $p_t=0{,}8$ ehtimollik berdi. $\\gamma=2$ da modulyatsiyalovchi ko‘paytuvchi nimaga teng?", options=["$0{,}64$", "$0{,}2$", "$0{,}04$", "$0{,}8$"], answer=2,
                 explain="$(1-p_t)^\\gamma=0{,}2^2=0{,}04$: bu misol yo‘qotishi CE’dagidan 25 marta kichik."),
            dict(q="$\\gamma=0$ va $\\alpha_t=1$ da focal loss’dan nima chiqadi?", options=["MSE", "Kross-entropiya", "Hinge loss", "Nol"], answer=1,
                 explain="$(1-p_t)^0=1$ ko‘paytuvchi, $-\\log p_t$ qoladi — kross-entropiya."),
            dict(q="$\\gamma=2$ da logit bo‘yicha FL gradiyenti $p_t$ ga qarab o‘zini qanday tutadi?", options=["CE’dagidek monoton kamayadi", "$p_t$ bilan o‘sadi", "Avval o‘sadi, $p_t\\approx0{,}06$ atrofida maksimumga yetadi, keyin tez tushadi", "O‘zgarmas"], answer=2,
                 explain="$|\\partial\\mathrm{FL}/\\partial z_t|=(1-p_t)^\\gamma[(1-p_t)+\\gamma p_t|\\log p_t|]$: $p_t\\to0$ da u 1 ga teng, $p_t\\approx0{,}058$ da $1{,}129$ gacha o‘sadi, keyin kamayadi."),
            dict(q="Nega RetinaNet’da kamyob obyektlar sinfi uchun, aytaylik, $0{,}99$ emas, $\\alpha=0{,}25$?", options=["Bu maqoladagi xato", "$\\gamma$ oson negativlarni allaqachon so‘ndirgan, pozitivlarga kuchli qo‘shimcha og‘ish ortiqcha bo‘lardi", "$\\alpha$ o‘qitishga ta’sir qilmaydi", "Obyektlar aslida kamyob emas"], answer=1,
                 explain="Modulyatsiyalovchi ko‘paytuvchidan keyin yo‘qotishning asosiy qismi baribir pozitivlar va qiyin negativlardan keladi; $\\alpha$ va $\\gamma$ birga tanlanadi, eng yaxshisi $\\alpha=0{,}25$ bo‘lib chiqdi."),
            dict(q="Model $\\gamma=2$ li focal loss’da o‘qitilgan. Uning chiqish ehtimolliklari haqida nima to‘g‘ri?", options=["Ular ideal kalibrlangan", "Ular o‘rtaga surilgan va kalibrlashni talab qiladi", "Ular doim 0 yoki 1", "Ular CE-model bilan mos tushadi"], answer=1,
                 explain="FL xos baholash qoidasi emas: hatto o‘zgarmas bashorat uchun ham minimum $p=\\pi$ da emas (6-rasm: $0{,}01$ o‘rniga $0{,}108$)."),
        ]),
    ]),
],
}

# Fill in the shared pieces (table rows and code listings) per language.
_CODES = {"CODE_NUMPY": CODE_NUMPY, "CODE_TORCH": CODE_TORCH}
for _lang, _secs in SECTIONS.items():
    for _sec in _secs:
        for _i, _b in enumerate(_sec["blocks"]):
            if _b[0] == "table" and _b[2] == "TABLE":
                _sec["blocks"][_i] = (_b[0], _b[1], _table(_lang), _b[3])
            elif _b[0] == "code" and _b[2] in _CODES:
                _sec["blocks"][_i] = (_b[0], _b[1], _code(_CODES[_b[2]], _lang))
