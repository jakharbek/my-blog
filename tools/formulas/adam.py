"""Formula page: Adam (and AdamW). Format: see README.md."""

META = dict(
    id="adam",
    date="2026-10-28",
    minutes=40,
    hero=r"\theta_t=\theta_{t-1}-\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}",
    title={"ru": "Adam: инерция, масштаб и поправка смещения",
           "en": "Adam: momentum, scale and bias correction",
           "uz": "Adam: inersiya, masshtab va siljishni tuzatish"},
    dek={
        "ru": "Оптимизатор по умолчанию для нейросетей и основа AdamW, которым обучают языковые модели. Разбираем по косточкам оба момента, выводим поправку смещения, смотрим, почему шаг Adam не зависит от масштаба градиента и сам уменьшается в шуме, гоняем пять оптимизаторов по поверхностям в 3D и разбираемся, чем AdamW лучше L2-регуляризации.",
        "en": "The default optimizer for neural networks and the basis of AdamW, which trains language models. We take apart both moments, derive bias correction, see why Adam’s step does not depend on the gradient’s scale and shrinks by itself in noise, race five optimizers over 3D surfaces and work out why AdamW beats L2 regularization.",
        "uz": "Neyron tarmoqlar uchun standart optimizator va til modellari o‘qitiladigan AdamW’ning asosi. Ikkala momentni mayda detallarigacha tahlil qilamiz, siljishni tuzatishni keltirib chiqaramiz, nega Adam qadami gradiyent masshtabiga bog‘liq emasligi va shovqinda o‘zi kichrayishini ko‘ramiz, beshta optimizatorni 3D sirtlarda poygaga qo‘yamiz va AdamW nima uchun L2-regulyarizatsiyadan yaxshiroq ekanini aniqlaymiz.",
    },
    description={
        "ru": "Adam подробно: моменты m и v, вывод поправки смещения, масштабная инвариантность, шаг и отношение сигнал/шум, гонка оптимизаторов в 3D, AdamW против L2, разогрев и косинусное расписание, код на NumPy и PyTorch.",
        "en": "Adam in depth: the moments m and v, the derivation of bias correction, scale invariance, the step and the signal-to-noise ratio, an optimizer race in 3D, AdamW versus L2, warmup and cosine schedules, NumPy and PyTorch code.",
        "uz": "Adam batafsil: m va v momentlar, siljishni tuzatishni keltirib chiqarish, masshtab invariantligi, qadam va signal/shovqin nisbati, 3D’da optimizatorlar poygasi, AdamW va L2, qizdirish va kosinusli jadval, NumPy va PyTorch kodi.",
    },
)

# Three Adam steps for g = 0.5, −0.2, 0.4 with β1 = 0.9, β2 = 0.999 (checked numerically).
STEPS = [("1", "0.5", "0.05", "0.00025", "0.5", "0.5", "1.000", "3.162"),
         ("2", "−0.2", "0.025", "0.00029", "0.1316", "0.3807", "0.346", "1.469"),
         ("3", "0.4", "0.0625", "0.00045", "0.2306", "0.3873", "0.596", "2.948")]


def _steps(lang):
    dec = "." if lang == "en" else ","
    return [[c.replace(".", dec) for c in row] for row in STEPS]


CODE_NUMPY = '''import numpy as np

class Adam:
    """Adam; при weight_decay > 0 и decoupled=True — AdamW. Как в torch.optim."""
    def __init__(self, lr=1e-3, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0, decoupled=True):
        self.lr, (self.b1, self.b2), self.eps = lr, betas, eps
        self.wd, self.decoupled = weight_decay, decoupled
        self.m = self.v = None
        self.t = 0

    def step(self, theta, g):
        if self.m is None:
            self.m, self.v = np.zeros_like(theta), np.zeros_like(theta)
        if self.wd and not self.decoupled:
            g = g + self.wd * theta                        # L2 внутри градиента (Adam)
        self.t += 1
        self.m = self.b1 * self.m + (1 - self.b1) * g      # инерция
        self.v = self.b2 * self.v + (1 - self.b2) * g * g  # масштаб
        m_hat = self.m / (1 - self.b1 ** self.t)           # поправка смещения
        v_hat = self.v / (1 - self.b2 ** self.t)
        if self.wd and self.decoupled:
            theta = theta - self.lr * self.wd * theta      # AdamW: затухание отдельно
        return theta - self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

# Три шага из таблицы: g = 0.5, −0.2, 0.4 (lr = 1, чтобы шаг был в единицах η)
opt, th = Adam(lr=1.0), np.zeros(1)
for g in [0.5, -0.2, 0.4]:
    new = opt.step(th, np.array([g]))
    print(f"t={opt.t}: m̂={opt.m[0] / (1 - 0.9 ** opt.t):.4f}  шаг/η={th[0] - new[0]:.4f}")
    th = new
# t=1: m̂=0.5000  шаг/η=1.0000
# t=2: m̂=0.1316  шаг/η=0.3456
# t=3: m̂=0.2306  шаг/η=0.5955

# Масштабная инвариантность: градиенты ×1000 дают те же шаги
rng = np.random.default_rng(0)
a, b, x, y = Adam(lr=0.01), Adam(lr=0.01), np.zeros(1), np.zeros(1)
for t in range(100):
    g = rng.normal(1.0, 0.5, size=1)
    x, y = a.step(x, g), b.step(y, 1000 * g)
print(x, y, abs(x - y))   # [-0.95081564] [-0.95081565] [8.6e-09] — разница только из-за ε'''

CODE_TORCH = '''import math
import torch
import torch.nn.functional as F

decay = [p for p in model.parameters() if p.ndim >= 2]     # матрицы весов
no_decay = [p for p in model.parameters() if p.ndim < 2]   # смещения и нормализации
opt = torch.optim.AdamW([{"params": decay, "weight_decay": 0.1},
                         {"params": no_decay, "weight_decay": 0.0}],
                        lr=3e-4, betas=(0.9, 0.95), eps=1e-8)

total, warmup = 10_000, 500
def lr_factor(step):                       # множитель к lr: разогрев, затем косинус до 10%
    if step < warmup:
        return (step + 1) / warmup
    p = (step - warmup) / (total - warmup)
    return 0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * p))
sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_factor)

for step, (x, y) in zip(range(total), loader):
    loss = F.mse_loss(model(x), y)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # обрезка градиента
    opt.step()
    sched.step()                          # расписание — после каждого шага'''


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("Adam; при weight_decay > 0 и decoupled=True — AdamW. Как в torch.optim.", "Adam; with weight_decay > 0 and decoupled=True it is AdamW. As in torch.optim."),
               ("L2 внутри градиента (Adam)", "L2 inside the gradient (Adam)"), ("# инерция", "# momentum"), ("# масштаб", "# scale"),
               ("поправка смещения", "bias correction"), ("AdamW: затухание отдельно", "AdamW: decay applied separately"),
               ("Три шага из таблицы: g = 0.5, −0.2, 0.4 (lr = 1, чтобы шаг был в единицах η)", "The three steps from the table: g = 0.5, −0.2, 0.4 (lr = 1, so the step is in units of η)"),
               ("шаг/η", "step/η"), ("Масштабная инвариантность: градиенты ×1000 дают те же шаги", "Scale invariance: gradients ×1000 give the same steps"),
               ("разница только из-за ε", "the difference comes from ε alone"),
               ("матрицы весов", "weight matrices"), ("смещения и нормализации", "biases and normalization layers"),
               ("множитель к lr: разогрев, затем косинус до 10%", "lr multiplier: warmup, then cosine down to 10%"),
               ("обрезка градиента", "gradient clipping"), ("расписание — после каждого шага", "the schedule steps after every update")],
        "uz": [("Adam; при weight_decay > 0 и decoupled=True — AdamW. Как в torch.optim.", "Adam; weight_decay > 0 va decoupled=True bo‘lsa — AdamW. torch.optim’dagidek."),
               ("L2 внутри градиента (Adam)", "gradiyent ichidagi L2 (Adam)"), ("# инерция", "# inersiya"), ("# масштаб", "# masshtab"),
               ("поправка смещения", "siljishni tuzatish"), ("AdamW: затухание отдельно", "AdamW: so‘nish alohida"),
               ("Три шага из таблицы: g = 0.5, −0.2, 0.4 (lr = 1, чтобы шаг был в единицах η)", "Jadvaldagi uchta qadam: g = 0.5, −0.2, 0.4 (qadam η birliklarida bo‘lishi uchun lr = 1)"),
               ("шаг/η", "qadam/η"), ("Масштабная инвариантность: градиенты ×1000 дают те же шаги", "Masshtab invariantligi: ×1000 gradiyentlar o‘sha qadamlarni beradi"),
               ("разница только из-за ε", "farq faqat ε tufayli"),
               ("матрицы весов", "vazn matritsalari"), ("смещения и нормализации", "siljishlar va normallashtirishlar"),
               ("множитель к lr: разогрев, затем косинус до 10%", "lr ko‘paytuvchisi: qizdirish, keyin 10% gacha kosinus"),
               ("обрезка градиента", "gradiyentni kesish"), ("расписание — после каждого шага", "jadval — har bir qadamdan keyin")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем нужен Adam", blocks=[
        ("p", "У нейросети миллионы весов, и их градиенты живут в очень разных масштабах: у эмбеддингов редких токенов — редкие крупные толчки, у последних слоёв — постоянные мелкие, у слоёв нормализации — третьи. Обычный <a href=\"../sgd/\">SGD</a> делает шаг $\\eta g$, и один темп $\\eta$ для всех одновременно слишком велик для одних весов и слишком мал для других. К тому же мини-батчевый градиент шумит, а поверхность потерь полна вытянутых оврагов и плато."),
        ("p", "Adam (adaptive moment estimation, Кингма и Ба, 2014) решает обе задачи одной формулой:"),
        ("ul", [
            "<b>первый момент</b> $m_t$ — экспоненциальное среднее градиентов: инерция, которая гасит шум и зигзаги (как <a href=\"../sgd/\">Momentum</a>);",
            "<b>второй момент</b> $v_t$ — экспоненциальное среднее квадратов градиента: типичный размер градиента каждого веса, на который делится шаг (как RMSProp);",
            "<b>поправка смещения</b> — деление на $1-\\beta^t$, которое убирает систематическую недооценку моментов на первых шагах.",
        ]),
        ("p", "Результат: шаг каждого веса порядка $\\eta$ независимо от масштаба его градиента, без ручной подстройки под каждый слой. Поэтому Adam — оптимизатор по умолчанию в большинстве задач, а его вариант AdamW обучает трансформеры и большие языковые модели."),
        ("callout", "key", "Главное за минуту", "$m_t$ — куда идти (сглаженный градиент), $\\sqrt{v_t}$ — насколько крупно шагать (среднеквадратичный градиент), $1-\\beta^t$ — поправка за старт с нуля. Шаг $\\eta\\,\\hat m_t/(\\sqrt{\\hat v_t}+\\epsilon)$ безразмерен: умножьте градиенты на 1000 — шаги не изменятся. При чистом сигнале шаг $\\approx\\eta$, в шуме — меньше. AdamW выносит затухание весов из градиента."),
    ]),
    dict(id="intuition", title="Интуиция: компас и спидометр", blocks=[
        ("p", "Представьте, что вы ведёте машину по бездорожью по показаниям дрожащего компаса. Глупо поворачивать руль при каждом его рывке — разумнее следить за усреднённым направлением. Это $m_t$. А скорость стоит выбирать по тому, насколько обычно сильны рывки: на ровной дороге можно ехать уверенно, на ухабах — осторожно. Это $\\sqrt{v_t}$: шаг Adam — направление, делённое на типичную силу толчков."),
        ("p", "На рисунке — поток градиентов одного веса: среднее $+0{,}5$ до шага 100 и $-0{,}5$ после, плюс шум. Оранжевая линия — сглаженный градиент $\\hat m_t$, бирюзовые — коридор $\\pm\\sqrt{\\hat v_t}$, внизу — итоговый шаг в единицах $\\eta$."),
        ("viz", "adam-moments", {"b1": 0.9, "b2": 0.999, "sigma": 1, "t": 1}, "<b>Рисунок 1.</b> Моменты Adam на шумном градиенте ($\\sigma=1$). Ползунок $t$ выбирает шаг для таблицы под рисунком. На первом шаге $\\hat m_1/\\sqrt{\\hat v_1}=1$ ровно — шаг равен $\\eta$ в сторону, противоположную $g_1$, каким бы ни был $g_1$; без поправки отношение было бы $3{,}16$. После смены знака среднего $\\hat m_t$ становится отрицательным навсегда с шага 109, а $\\sqrt{\\hat v_t}$ почти не меняется ($\\approx1{,}1$): величина шага определяется отношением сигнала к шуму, $0{,}5/\\sqrt{1{,}25}\\approx0{,}45$. Даже на шаге 200 шаг без поправки (штрих) в $2{,}35$ раза больше правильного."),
        ("callout", "intuition", "Что заметить", "Уберите шум ($\\sigma=0$): шаг сразу становится ровно $\\pm1$ — Adam при чистом сигнале ходит шагами $\\eta$, как знаковый метод. Увеличьте шум — шаг сжимается. Уменьшите $\\beta_1$ до нуля — $\\hat m_t$ превращается в сам градиент, и шаг скачет между $\\pm1$."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("eq", r"\begin{aligned}g_t&=\nabla_\theta L(\theta_{t-1})\\ m_t&=\beta_1 m_{t-1}+(1-\beta_1)\,g_t\\ v_t&=\beta_2 v_{t-1}+(1-\beta_2)\,g_t^2\\ \hat m_t&=\frac{m_t}{1-\beta_1^{\,t}},\qquad \hat v_t=\frac{v_t}{1-\beta_2^{\,t}}\\ \theta_t&=\theta_{t-1}-\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}\end{aligned}"),
        ("symbols", [
            (r"g_t", "градиент на мини-батче шага $t$ (шаги нумеруются с 1);"),
            (r"m_t", "первый момент: экспоненциальное скользящее среднее (EMA) градиента, $m_0=0$;"),
            (r"v_t", "второй момент: EMA поэлементного квадрата градиента, $v_0=0$; у каждого веса свои $m$ и $v$;"),
            (r"\beta_1,\ \beta_2", "коэффициенты затухания, по умолчанию $0{,}9$ и $0{,}999$: память примерно $1/(1-\\beta)$ шагов — 10 и 1000;"),
            (r"1-\beta^t", "поправка смещения: компенсирует старт моментов с нуля;"),
            (r"\eta", "темп обучения (learning rate), по умолчанию $10^{-3}$; здесь он задаёт типичную длину шага в единицах весов;"),
            (r"\epsilon", "маленькая добавка ($10^{-8}$) против деления на ноль."),
        ]),
        ("p", "Пройдём три шага руками для градиентов $0{,}5$, $-0{,}2$, $0{,}4$ при стандартных $\\beta_1=0{,}9$, $\\beta_2=0{,}999$. Последний столбец — каким был бы шаг без поправки смещения."),
        ("table", ["$t$", "$g_t$", "$m_t$", "$v_t$", "$\\hat m_t$", "$\\sqrt{\\hat v_t}$", "шаг $/\\eta$", "без поправки"], "STEPS", {"num": [0, 1, 2, 3, 4, 5, 6, 7]}),
        ("callout", "note", "Первый шаг в деталях", "$g_1=0{,}5$: $m_1=0{,}1\\cdot0{,}5=0{,}05$ и $v_1=0{,}001\\cdot0{,}25=0{,}00025$ — оба момента занижены, в 10 и в 1000 раз. Поправка возвращает $\\hat m_1=0{,}5$ и $\\hat v_1=0{,}25$, отношение $\\hat m_1/\\sqrt{\\hat v_1}=1$: вес сдвигается ровно на $\\eta$. Без поправки было бы $m_1/\\sqrt{v_1}=0{,}05/0{,}0158\\approx3{,}16$ — шаг завышен в $3{,}16$ раза, потому что $\\sqrt{v_1}$ занижен сильнее ($\\sqrt{1000}\\approx31{,}6$ раза), чем $m_1$ (10 раз). Если бы поправили только $m$, шаг вырос бы в $31{,}6$ раза; только $v$ — уменьшился бы в 10."),
        ("p", "Обратите внимание на третий шаг: градиенты меняли знак, поэтому $\\hat m_3=0{,}23$ заметно меньше типичного размера градиента $\\sqrt{\\hat v_3}=0{,}39$, и Adam шагает лишь на $0{,}6\\eta$. Чем согласованнее градиенты, тем ближе шаг к $\\eta$."),
    ]),
    dict(id="bias", title="Поправка смещения: откуда 1 − βᵗ", blocks=[
        ("p", "Моменты стартуют с нуля и первые шаги «помнят» этот ноль. Раскроем рекурсию для $m_t$:"),
        ("eq", r"m_t=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{\,t-i}\,g_i"),
        ("p", "Это взвешенная сумма градиентов, но сумма весов равна не 1, а $(1-\\beta_1)(1+\\beta_1+\\dots+\\beta_1^{t-1})=1-\\beta_1^t$. Недостающая доля $\\beta_1^t$ досталась начальному нулю. Отсюда и поправка."),
        ("deep", "Вывод: несмещённость $\\hat m_t$ и $\\hat v_t$", [
            ("p", "Пусть градиенты стационарны: $\\mathbb E[g_i]=\\mu$, $\\mathbb E[g_i^2]=s$ для всех $i$. Тогда по линейности ожидания"),
            ("eq", r"\mathbb E[m_t]=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{\,t-i}\mu=\mu\,(1-\beta_1^{\,t}),\qquad \mathbb E[v_t]=s\,(1-\beta_2^{\,t})"),
            ("p", "Деление на $1-\\beta^t$ даёт $\\mathbb E[\\hat m_t]=\\mu$ и $\\mathbb E[\\hat v_t]=s$ — оценки несмещённые с первого шага. Если градиенты нестационарны, остаётся смещение порядка изменения $\\mu$ за окно памяти; Кингма и Ба отмечают, что его можно держать малым, потому что веса далёкого прошлого экспоненциально малы."),
            ("p", "Поправка нужна только в начале: $\\beta_1^t&lt;0{,}01$ уже при $t\\ge44$, а вот $\\beta_2^t&lt;0{,}01$ — лишь при $t\\ge4603$. Поэтому важнее всего она для второго момента."),
        ]),
        ("viz", "adam-bias", {"b1": 0.9, "b2": 0.999}, "<b>Рисунок 2.</b> Множители поправки $1/(1-\\beta_1^t)$ и $1/(1-\\beta_2^t)$ (обе оси логарифмические) и отношение шага без поправки к шагу с поправкой при постоянном градиенте, $(1-\\beta_1^t)/\\sqrt{1-\\beta_2^t}$. При стандартных $\\beta$ первые множители — 10 и 1000; шаг без поправки завышен в $3{,}16$ раза на первом шаге, сильнее всего — в $6{,}57$ раза — на 12-м, всё ещё в $2{,}35$ раза на 200-м и в $1{,}26$ раза на 1000-м. При $\\beta_2=0{,}99$ первые шаги совпадают ($0{,}1/\\sqrt{0{,}01}=1$), но к 13-му шагу завышение достигает $2{,}13$."),
        ("callout", "warn", "Зачем это важно на практике", "Без поправки ранние шаги Adam в несколько раз длиннее задуманного — ровно тогда, когда веса только что инициализированы и потери максимальны. Это одна из причин, по которой трансформеры без разогрева темпа (warmup) расходятся на первых сотнях шагов; сама поправка этот риск убирает лишь частично, потому что $\\hat v_t$ на первых шагах оценён всего по нескольким градиентам."),
    ]),
    dict(id="properties", title="Свойства шага", blocks=[
        ("h3", "Масштабная инвариантность"),
        ("p", "Умножим все градиенты веса на $c&gt;0$. Тогда $m_t$ умножится на $c$, $v_t$ — на $c^2$, $\\sqrt{v_t}$ — на $c$, и отношение $\\hat m_t/\\sqrt{\\hat v_t}$ не изменится. Шаг Adam — однородная функция нулевой степени от градиентов (пока $\\sqrt{\\hat v_t}\\gg\\epsilon$). Эффективный темп каждого веса $\\eta/(\\sqrt{\\hat v_t}+\\epsilon)$ подстраивается сам: большой у весов с мелкими градиентами, маленький — у весов с крупными."),
        ("viz", "adam-scale", {"eps": 1e-8}, "<b>Рисунок 3.</b> Четыре параметра с одинаковым шумным градиентом $c\\,(1+0{,}5\\xi_t)$, но масштабами $c$ от $10^{-3}$ до $10^{3}$; столбики — длина шага на сотом шаге (шкала логарифмическая). Шаги SGD различаются в $10^6$ раз, шаги Adam одинаковы: $8{,}8\\cdot10^{-4}=0{,}88\\,\\eta$, а эффективный темп $\\eta/(\\sqrt{\\hat v}+\\epsilon)$ меняется от $8{,}8\\cdot10^{-7}$ до $0{,}88$. Уменьшите общий масштаб $k$ до $10^{-6}$: градиент порядка $10^{-9}$ становится меньше $\\epsilon=10^{-8}$, и его шаг падает в 10 раз — так $\\epsilon$ отключает адаптацию для совсем малых градиентов."),
        ("h3", "Шаг и отношение сигнал/шум"),
        ("p", "Пусть градиент веса стационарен со средним $\\mu$ и стандартным отклонением $\\sigma$. Тогда $\\hat m_t\\approx\\mu$, $\\hat v_t\\approx\\mu^2+\\sigma^2$ (второй момент — это квадрат среднего плюс дисперсия), и средний шаг"),
        ("eq", r"\frac{|\Delta\theta|}{\eta}\approx\frac{|\mu|}{\sqrt{\mu^2+\sigma^2}}=\frac{\mathrm{SNR}}{\sqrt{1+\mathrm{SNR}^2}},\qquad \mathrm{SNR}=\frac{|\mu|}{\sigma}"),
        ("p", "При чистом сигнале ($\\sigma\\ll|\\mu|$) шаг $\\approx\\eta$, в сильном шуме ($\\sigma\\gg|\\mu|$) он пропорционален отношению сигнал/шум. Это автоматическое «торможение»: у минимума средний градиент стремится к нулю, а шум остаётся — и Adam сам укорачивает шаги."),
        ("viz", "adam-snr", {"b1": 0.9, "b2": 0.999, "snr": 0.3}, "<b>Рисунок 4.</b> Средний шаг Adam (в единицах $\\eta$) в зависимости от отношения сигнал/шум $\\mu/\\sigma$: сплошная — формула выше, точки — симуляция 20 000 шагов с разбросом $\\pm$ одно стандартное отклонение, штрих — шаг SGD, растущий пропорционально $\\mu$. При $\\mu/\\sigma=0{,}3$ формула даёт $0{,}287$, симуляция — $0{,}298$ с разбросом $\\pm0{,}216$. Разброс при слабом сигнале близок к $\\sqrt{(1-\\beta_1)/(1+\\beta_1)}\\approx0{,}23$: уменьшите $\\beta_1$ — шаги станут хаотичнее."),
        ("deep", "Насколько большим бывает шаг", [
            ("p", "Обычно $|\\hat m_t|\\le\\sqrt{\\hat v_t}$ и шаг не больше $\\eta$, но это не теорема. Если градиент был нулём и вдруг стал $g$, то при больших $t$ получаем $m_t=(1-\\beta_1)g$, $v_t=(1-\\beta_2)g^2$, и шаг равен $\\eta(1-\\beta_1)/\\sqrt{1-\\beta_2}\\approx3{,}16\\,\\eta$ — этот случай разбирают Кингма и Ба. Точная верхняя граница следует из неравенства Коши — Буняковского для взвешенных сумм:"),
            ("eq", r"\frac{|m_t|}{\sqrt{v_t}}\le\frac{1-\beta_1}{\sqrt{(1-\beta_2)\,(1-\beta_1^2/\beta_2)}}\approx7{,}27"),
            ("p", "(при $\\beta_1^2&lt;\\beta_2$). Она достигается, когда градиент растёт в $\\beta_2/\\beta_1\\approx1{,}11$ раза за шаг. Значит, шаг Adam ограничен величиной порядка $\\eta$ при любых градиентах — встроенная защита от их взрыва."),
        ]),
        ("h3", "Особые случаи"),
        ("ul", [
            "$\\beta_1=\\beta_2=0$: $\\hat m_t=g_t$, $\\sqrt{\\hat v_t}=|g_t|$, шаг $\\eta\\operatorname{sign}(g_t)$ — знаковый градиентный спуск (signSGD).",
            "$\\beta_1=0$: RMSProp с поправкой смещения.",
            "$\\epsilon\\gg\\sqrt{\\hat v_t}$: шаг $\\approx(\\eta/\\epsilon)\\,\\hat m_t$ — SGD с инерцией и темпом $\\eta/\\epsilon$.",
            "Adam — <b>диагональный</b> предобусловливатель: он масштабирует каждую координату отдельно и не умеет поворачивать оси (см. рисунок 6 на странице <a href=\"../sgd/\">SGD</a>).",
        ]),
    ]),
    dict(id="math", title="Математика за формулой", blocks=[
        ("p", "Соберём вместе то, что прячется за четырьмя строками."),
        ("ul", [
            "<b>EMA как взвешенное среднее.</b> $\\hat m_t=\\sum_i w_i g_i$ с весами $w_i=(1-\\beta_1)\\beta_1^{t-i}/(1-\\beta_1^t)$, которые положительны и в сумме дают 1. Вес убывает вдвое примерно каждые $\\ln2/(1-\\beta)$ шагов: 7 для $\\beta_1=0{,}9$ и 693 для $\\beta_2=0{,}999$.",
            "<b>Эффективное окно</b> $1/(1-\\beta)$: $m$ усредняет примерно 10 последних градиентов, $v$ — примерно 1000. Направление реагирует быстро, масштаб — медленно и потому устойчиво.",
            "<b>Второй момент — не дисперсия.</b> $v$ оценивает $\\mathbb E[g^2]=\\mu^2+\\sigma^2$, то есть «нецентрированный» размер градиента. Поэтому при чистом сигнале шаг $\\approx\\eta$, а не бесконечен.",
            "<b>Связь с методом Ньютона.</b> Иногда говорят, что $\\sqrt v$ аппроксимирует кривизну. Это верно лишь отчасти: $v$ — оценка диагонали эмпирической матрицы Фишера (по градиентам мини-батчей), которая для некоторых потерь у минимума близка к гессиану, но Adam берёт из неё квадратный корень. Надёжнее понимать Adam как нормировку шага, а не как приближение Ньютона.",
        ]),
        ("deep", "Сходимость: контрпример и AMSGrad", [
            ("p", "Исходное доказательство сходимости Adam для выпуклых задач содержало ошибку. Редди, Кейл и Кумар (2018) построили простую выпуклую задачу, на которой Adam сходится к худшей точке: редкий, но большой градиент быстро «забывается» в $v_t$, потому что $\\beta_2$-память конечна, и эффективный темп $\\eta/\\sqrt{\\hat v_t}$ может расти."),
            ("p", "Их исправление, AMSGrad, использует $\\hat v_t=\\max(\\hat v_{t-1},v_t)$ — эффективный темп больше не растёт, и сходимость в выпуклом случае доказывается. На практике AMSGrad редко заметно лучше Adam (в PyTorch — флаг <code>amsgrad=True</code>). Для невыпуклых задач гарантии получены при убывающем темпе и достаточно большом $\\beta_2$."),
        ]),
    ]),
    dict(id="landscape", title="Гонка оптимизаторов в 3D", blocks=[
        ("p", "Сравним пять методов на двух поверхностях. Первая — плато с ямой: $f=1-e^{-q(x,y)}$, $q=0{,}2(x-1)^2+1{,}2(y-0{,}5)^2$. Вдали от ямы $f\\approx1$, градиент крошечный, а сама яма вытянута. Вторая — банан Розенброка."),
        ("viz", "adam-race", {"fn": "plateau"}, "<b>Рисунок 5.</b> Слева поверхность в 3D (её можно вращать), справа вид сверху; старт можно перетаскивать, «Пуск» проигрывает гонку. В точке старта $(-2{,}4;\\,-1{,}5)$ градиент порядка $4\\cdot10^{-3}$: SGD с $\\eta=0{,}3$ ползёт по плато и достигает $f&lt;0{,}01$ лишь за 246 шагов, Momentum — за 61, RMSProp — за 44, Adam — за 58, AdamW — за 53. Но AdamW останавливается не в минимуме $(1;\\,0{,}5)$, а в $(0{,}979;\\,0{,}498)$, где $f=9\\cdot10^{-5}$: затухание весов тянет к нулю. На Розенброке за 2000 шагов: Momentum — 416 шагов, Adam — 717, AdamW — 818, а SGD и RMSProp не доходят до $f&lt;0{,}01$."),
        ("callout", "intuition", "Чему учит гонка", "Адаптивные методы выигрывают там, где градиенты плохо масштабированы: на плато их шаг остаётся порядка $\\eta$, пока у SGD он пропорционален крошечному градиенту. Но хорошо настроенная инерция может их обогнать (Розенброк), а затухание весов сдвигает решение — это не баг, а регуляризация. Универсального победителя нет."),
    ]),
    dict(id="adamw", title="AdamW: правильное затухание весов", blocks=[
        ("p", "Классическая $L_2$-регуляризация добавляет к потерям $\\tfrac\\lambda2\\|\\theta\\|^2$, то есть к градиенту — $\\lambda\\theta$. Для SGD это то же самое, что на каждом шаге умножать веса на $1-\\eta\\lambda$ (затухание весов, weight decay). Для Adam — нет: слагаемое $\\lambda\\theta$ попадает в $m$ и $v$ и делится на $\\sqrt{\\hat v_t}$. Лошчилов и Хаттер (2017) предложили отделить затухание от градиента:"),
        ("eq", r"\text{Adam}+L_2:\quad \begin{aligned}g_t&=\nabla L(\theta_{t-1})+\lambda\,\theta_{t-1}\\ \theta_t&=\theta_{t-1}-\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}\end{aligned}"),
        ("eq", r"\text{AdamW}:\quad \theta_t=\theta_{t-1}-\eta\Bigl(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}+\lambda\,\theta_{t-1}\Bigr)"),
        ("p", "В AdamW моменты считаются по градиенту одних лишь потерь, а все веса затухают с одной и той же скоростью $\\eta\\lambda$ за шаг. В Adam с $L_2$ затухание каждого веса делится на его $\\sqrt{\\hat v_t}$: веса с крупными градиентами почти не регуляризуются, а веса без градиента потерь сжимаются с постоянной скоростью $\\approx\\eta$ за шаг, независимо от $\\lambda$."),
        ("viz", "adam-adamw", {"lam": 0.1}, "<b>Рисунок 6.</b> Три веса, стартующие с $\\theta=1$; градиент данных у них знакопеременный, $\\pm c$ (в среднем ноль), с $c=0$, $0{,}1$ и $10$. Темп $\\eta=0{,}01$, $\\lambda=0{,}1$, 1000 шагов. AdamW (фиолетовые) уменьшает все три одинаково, до $0{,}37\\approx e^{-\\eta\\lambda t}=e^{-1}$. Adam с $L_2$ (оранжевые) обнуляет вес без градиента (ниже $0{,}01$ уже к шагу 213), сжимает вес с $c=0{,}1$ до $0{,}0003$ и почти не трогает вес с $c=10$ — у того остаётся $0{,}889$."),
        ("callout", "key", "Вывод", "В Adam регуляризация $L_2$ и затухание весов — разные вещи. Если вы хотите затухание, используйте <code>AdamW</code>; в PyTorch <code>torch.optim.Adam(weight_decay=…)</code> реализует именно $L_2$ внутри градиента. По умолчанию у <code>AdamW</code> $\\lambda=0{,}01$; языковые модели обычно обучают с $\\lambda=0{,}1$ и не применяют затухание к смещениям и весам нормализаций."),
    ]),
    dict(id="training", title="Adam в обучении: разогрев и расписание", blocks=[
        ("p", "Даже адаптивному методу нужен график темпа. Самая распространённая схема для трансформеров — <b>линейный разогрев</b> (warmup) от нуля до $\\eta_{\\max}$ за первые сотни или тысячи шагов, затем <b>косинусное снижение</b> до $\\eta_{\\min}$:"),
        ("eq", r"\eta_t=\eta_{\max}\,\frac{t}{T_w}\qquad(t\le T_w)"),
        ("eq", r"\eta_t=\eta_{\min}+\tfrac12(\eta_{\max}-\eta_{\min})\bigl(1+\cos\pi p\bigr),\quad p=\frac{t-T_w}{T-T_w}"),
        ("viz", "adam-schedule", {"warm": 200, "minr": 0.1}, "<b>Рисунок 7.</b> Adam на шумной квадратичной задаче (10 параметров с кривизнами от $0{,}01$ до 1, шум градиента $0{,}05$), $\\eta_{\\max}=0{,}05$, 2000 шагов. Вверху — темп, внизу — потери (логарифмическая шкала). С постоянным $\\eta$ потери застревают на шумовом уровне $5{,}6\\cdot10^{-3}$ (среднее за последние 100 шагов); с разогревом на 200 шагов и косинусом до $0{,}1\\,\\eta_{\\max}$ — $7{,}1\\cdot10^{-4}$, в $7{,}9$ раза ниже. Разогрев здесь лишь немного задерживает старт; его польза проявляется в глубоких сетях."),
        ("p", "Почему снижение помогает: из раздела о свойствах шаг Adam у минимума пропорционален $\\eta$, умноженному на отношение сигнал/шум. Чем меньше $\\eta$, тем меньше облако, в котором веса дрожат вокруг минимума."),
        ("p", "Почему разогрев нужен: на первых шагах $\\hat v_t$ оценён по нескольким градиентам и сильно шумит, а веса только что инициализированы, и градиенты особенно велики. Лю и соавторы (RAdam, 2019) показали, что дисперсия эффективного темпа $\\eta/\\sqrt{\\hat v_t}$ в начале обучения велика, и предложили выпрямлять её аналитически; разогрев решает ту же проблему проще."),
        ("callout", "note", "Типичный рецепт для языковых моделей", "AdamW с $\\beta_1=0{,}9$, $\\beta_2=0{,}95$, $\\lambda=0{,}1$, обрезка градиента по норме 1, разогрев на ~2000 шагов и косинус до 10% от $\\eta_{\\max}$ — так, например, описано обучение LLaMA. Меньшее $\\beta_2$ (окно 20 шагов вместо 1000) быстрее реагирует на всплески градиента и делает обучение больших моделей устойчивее."),
    ]),
    dict(id="code", title="В коде: с нуля и в PyTorch", blocks=[
        ("p", "Реализация с нуля — двадцать строк. Флаг <code>decoupled</code> переключает затухание весов между AdamW и $L_2$ внутри градиента."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "Выход совпадает с таблицей из раздела «Формула по косточкам», а <code>torch.optim.Adam</code> на том же первом шаге сдвигает вес ровно на $\\eta$. Типичный цикл обучения с AdamW, раздельными группами затухания, разогревом и косинусом:"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "warn", "Память", "Adam хранит $m$ и $v$ — два числа на каждый параметр. Для модели на 7 млрд параметров это $2\\cdot7\\cdot10^9\\cdot4$ байта $=56$ ГБ в float32 только под состояние оптимизатора. Отсюда 8-битные оптимизаторы, шардирование состояния (ZeRO) и экономные варианты вроде Adafactor."),
    ]),
    dict(id="practice", title="Гиперпараметры и практика", blocks=[
        ("table", ["Параметр", "По умолчанию", "Типичный диапазон и смысл"], [
            ["$\\eta$", "$10^{-3}$", "$10^{-4}$–$3\\cdot10^{-3}$; трансформеры — около $3\\cdot10^{-4}$ и меньше с ростом модели; дообучение — $10^{-5}$–$5\\cdot10^{-5}$"],
            ["$\\beta_1$", "$0{,}9$", "почти никогда не меняют; окно направления 10 шагов"],
            ["$\\beta_2$", "$0{,}999$", "$0{,}95$–$0{,}98$ для больших трансформеров: быстрее реагирует на всплески"],
            ["$\\epsilon$", "$10^{-8}$", "больше ($10^{-6}$ и выше) — при низкой точности или нестабильности; слишком большой $\\epsilon$ превращает Adam в SGD с инерцией"],
            ["$\\lambda$ (AdamW)", "$0{,}01$", "$0{,}01$–$0{,}1$; не применять к смещениям и нормализациям"],
            ["разогрев", "—", "от сотен до нескольких тысяч шагов, 1–5% обучения"],
        ], {}),
        ("ul", [
            "<b>Начните с умолчаний.</b> $\\eta=10^{-3}$ (или $3\\cdot10^{-4}$ для трансформеров), $\\beta=(0{,}9;\\,0{,}999)$, AdamW с $\\lambda=0{,}01$. Подбирать в первую очередь стоит $\\eta$, затем $\\lambda$ и расписание.",
            "<b>Обрезка градиента</b> по норме ($1{,}0$) почти бесплатна и спасает от редких выбросов.",
            "<b>Сохраняйте состояние оптимизатора</b> (<code>opt.state_dict()</code>) вместе с весами: при продолжении обучения с нулевыми $m$ и $v$ первые шаги снова будут «холодными».",
            "<b>Когда SGD лучше.</b> На задачах компьютерного зрения хорошо настроенный SGD с инерцией часто даёт лучшее обобщение (Уилсон и др., 2017). Для трансформеров, рекомендательных систем с эмбеддингами и задач с разреженными градиентами выигрывает Adam.",
        ]),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b><code>Adam(weight_decay=…)</code> вместо <code>AdamW</code>.</b> Это $L_2$ внутри градиента: затухание делится на $\\sqrt{\\hat v_t}$ и работает неравномерно (рисунок 6).",
            "<b>Темп от SGD.</b> $\\eta=0{,}1$ хорош для SGD с инерцией, но для Adam это шаг около $0{,}1$ в единицах весов на каждом шаге — обучение почти наверняка разойдётся.",
            "<b>Затухание для всех параметров.</b> Смещения и веса LayerNorm/BatchNorm обычно исключают из weight decay: их сжатие к нулю вредит, а не регуляризует.",
            "<b>Неудачный $\\epsilon$.</b> Слишком маленький в float16 округляется до нуля, слишком большой ($\\gtrsim\\sqrt{\\hat v}$) молча отключает адаптацию — шаг становится $(\\eta/\\epsilon)\\hat m$.",
            "<b>Без разогрева на трансформере.</b> Большой $\\eta$ с первых шагов при шумной оценке $\\hat v_t$ часто приводит к взрыву потерь в начале обучения.",
            "<b>Расписание не на том шаге.</b> <code>scheduler.step()</code> раз за эпоху там, где расписание рассчитано на шаги (или наоборот), растягивает разогрев в сотни раз.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            "<a href=\"../sgd/\">SGD, Momentum и RMSProp</a>: числитель Adam — EMA-инерция, знаменатель — $\\sqrt v$ из RMSProp; там же условие устойчивости и число обусловленности.",
            "<a href=\"../cross-entropy/\">Кросс-энтропия</a> и <a href=\"../softmax/\">softmax</a>: потеря, которую AdamW минимизирует в языковых моделях; её градиент по логитам $s-y$ и есть $g_t$ последнего слоя.",
            "<a href=\"../mse/\">MSE</a> и <a href=\"../huber/\">Huber</a>: от масштаба целевой переменной зависит масштаб градиента — Adam к нему нечувствителен, SGD — нет.",
            "<a href=\"../gelu/\">GELU</a> и <a href=\"../silu/\">SiLU</a>: активации трансформеров, которые обучаются AdamW.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) Adam хранит два экспоненциальных средних: $m_t$ градиента (направление, окно ~10 шагов) и $v_t$ его квадрата (масштаб, окно ~1000 шагов). 2) Оба стартуют с нуля и занижены в $1-\\beta^t$ раз; поправка делает их несмещёнными, без неё ранние шаги завышены — в $3{,}16$ раза на первом шаге. 3) Шаг $\\eta\\,\\hat m_t/(\\sqrt{\\hat v_t}+\\epsilon)$ не зависит от масштаба градиента, порядка $\\eta$ при чистом сигнале и пропорционален отношению сигнал/шум в шуме. 4) AdamW отделяет затухание весов от градиента — все веса затухают равномерно. 5) На практике: AdamW, разогрев, косинус, обрезка градиента; $\\eta$ — главный гиперпараметр."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="Первый шаг Adam с поправкой смещения, $g_1=-3$. Как изменится вес?", options=["Уменьшится на $3\\eta$", "Увеличится на $\\eta$", "Уменьшится на $\\eta$", "Увеличится на $3\\eta$"], answer=1,
                 explain="$\\hat m_1=g_1=-3$, $\\sqrt{\\hat v_1}=|g_1|=3$, шаг $-\\eta\\cdot(-3)/3=+\\eta$: вес растёт на $\\eta$, каким бы ни был $|g_1|$."),
            dict(q="Сколько последних шагов примерно «помнит» $v_t$ при $\\beta_2=0{,}999$?", options=["10", "100", "1000", "10 000"], answer=2,
                 explain="Эффективное окно $1/(1-\\beta_2)=1000$ шагов."),
            dict(q="Все градиенты модели умножили на 100 (например, потерю умножили на 100). Что станет с шагами Adam?", options=["Вырастут в 100 раз", "Вырастут в 10 раз", "Почти не изменятся", "Уменьшатся в 100 раз"], answer=2,
                 explain="$\\hat m$ и $\\sqrt{\\hat v}$ вырастут в 100 раз, их отношение не изменится (пока $\\epsilon$ пренебрежимо мал)."),
            dict(q="Чем AdamW отличается от Adam с $L_2$-регуляризацией?", options=["Ничем, это синонимы", "Затухание весов не проходит через $m$ и $v$ и не делится на $\\sqrt{\\hat v}$", "AdamW не использует поправку смещения", "AdamW использует знак градиента"], answer=1,
                 explain="В AdamW веса умножаются на $1-\\eta\\lambda$ отдельно от адаптивного шага, поэтому затухание одинаково для всех весов."),
            dict(q="Во сколько раз завышен первый шаг Adam без поправки смещения при $\\beta_1=0{,}9$, $\\beta_2=0{,}999$?", options=["В $0{,}1$ раза (занижен в 10)", "Не завышен", "В $3{,}16$ раза", "В 1000 раз"], answer=2,
                 explain="$m_1/\\sqrt{v_1}=(1-\\beta_1)g/(\\sqrt{1-\\beta_2}\\,|g|)=0{,}1/0{,}0316\\approx3{,}16$."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need Adam", blocks=[
        ("p", "A neural network has millions of weights, and their gradients live on very different scales: embeddings of rare tokens get rare large kicks, the last layers get constant small ones, normalization layers yet others. Plain <a href=\"../sgd/\">SGD</a> takes the step $\\eta g$, and a single rate $\\eta$ is at once too large for some weights and too small for others. On top of that, the mini-batch gradient is noisy, and the loss surface is full of elongated ravines and plateaus."),
        ("p", "Adam (adaptive moment estimation, Kingma and Ba, 2014) tackles both problems with one formula:"),
        ("ul", [
            "<b>the first moment</b> $m_t$ — an exponential average of gradients: inertia that damps noise and zigzags (like <a href=\"../sgd/\">Momentum</a>);",
            "<b>the second moment</b> $v_t$ — an exponential average of squared gradients: the typical gradient size of each weight, by which the step is divided (like RMSProp);",
            "<b>bias correction</b> — division by $1-\\beta^t$, which removes the systematic underestimate of the moments in the first steps.",
        ]),
        ("p", "The result: every weight’s step is of order $\\eta$ regardless of its gradient’s scale, with no manual tuning per layer. That is why Adam is the default optimizer for most tasks, and its variant AdamW trains transformers and large language models."),
        ("callout", "key", "The essentials in a minute", "$m_t$ says where to go (a smoothed gradient), $\\sqrt{v_t}$ how big a step to take (the root-mean-square gradient), $1-\\beta^t$ corrects for starting from zero. The step $\\eta\\,\\hat m_t/(\\sqrt{\\hat v_t}+\\epsilon)$ is dimensionless: multiply the gradients by 1000 and the steps do not change. With a clean signal the step is $\\approx\\eta$, in noise it is smaller. AdamW takes weight decay out of the gradient."),
    ]),
    dict(id="intuition", title="Intuition: a compass and a speedometer", blocks=[
        ("p", "Imagine driving off-road by a jittery compass. Turning the wheel at every twitch would be silly — it is wiser to follow the averaged direction. That is $m_t$. And the speed should depend on how strong the twitches usually are: on a smooth road you can drive confidently, on bumps carefully. That is $\\sqrt{v_t}$: Adam’s step is the direction divided by the typical strength of the jolts."),
        ("p", "The figure shows the gradient stream of one weight: mean $+0.5$ until step 100 and $-0.5$ after, plus noise. The orange line is the smoothed gradient $\\hat m_t$, the teal lines are the corridor $\\pm\\sqrt{\\hat v_t}$, and below is the resulting step in units of $\\eta$."),
        ("viz", "adam-moments", {"b1": 0.9, "b2": 0.999, "sigma": 1, "t": 1}, "<b>Figure 1.</b> Adam’s moments on a noisy gradient ($\\sigma=1$). The $t$ slider picks the step for the table below the figure. At the first step $\\hat m_1/\\sqrt{\\hat v_1}=1$ exactly — the step is $\\eta$ against $g_1$, whatever $g_1$ is; without correction the ratio would be $3.16$. After the mean changes sign, $\\hat m_t$ turns negative for good from step 109, while $\\sqrt{\\hat v_t}$ hardly changes ($\\approx1.1$): the step size is set by the signal-to-noise ratio, $0.5/\\sqrt{1.25}\\approx0.45$. Even at step 200 the uncorrected step (dashed) is $2.35$ times the correct one."),
        ("callout", "intuition", "What to notice", "Remove the noise ($\\sigma=0$): the step immediately becomes exactly $\\pm1$ — with a clean signal Adam takes steps of $\\eta$, like a sign method. Increase the noise and the step shrinks. Lower $\\beta_1$ to zero and $\\hat m_t$ turns into the gradient itself, so the step jumps between $\\pm1$."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("eq", r"\begin{aligned}g_t&=\nabla_\theta L(\theta_{t-1})\\ m_t&=\beta_1 m_{t-1}+(1-\beta_1)\,g_t\\ v_t&=\beta_2 v_{t-1}+(1-\beta_2)\,g_t^2\\ \hat m_t&=\frac{m_t}{1-\beta_1^{\,t}},\qquad \hat v_t=\frac{v_t}{1-\beta_2^{\,t}}\\ \theta_t&=\theta_{t-1}-\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}\end{aligned}"),
        ("symbols", [
            (r"g_t", "the mini-batch gradient at step $t$ (steps are numbered from 1);"),
            (r"m_t", "the first moment: an exponential moving average (EMA) of the gradient, $m_0=0$;"),
            (r"v_t", "the second moment: an EMA of the element-wise squared gradient, $v_0=0$; every weight has its own $m$ and $v$;"),
            (r"\beta_1,\ \beta_2", "decay rates, $0.9$ and $0.999$ by default: memory of about $1/(1-\\beta)$ steps — 10 and 1000;"),
            (r"1-\beta^t", "bias correction: compensates for the moments starting at zero;"),
            (r"\eta", "the learning rate, $10^{-3}$ by default; here it sets the typical step length in the units of the weights;"),
            (r"\epsilon", "a small constant ($10^{-8}$) against division by zero."),
        ]),
        ("p", "Let us run three steps by hand for the gradients $0.5$, $-0.2$, $0.4$ with the standard $\\beta_1=0.9$, $\\beta_2=0.999$. The last column shows what the step would be without bias correction."),
        ("table", ["$t$", "$g_t$", "$m_t$", "$v_t$", "$\\hat m_t$", "$\\sqrt{\\hat v_t}$", "step $/\\eta$", "uncorrected"], "STEPS", {"num": [0, 1, 2, 3, 4, 5, 6, 7]}),
        ("callout", "note", "The first step in detail", "$g_1=0.5$: $m_1=0.1\\cdot0.5=0.05$ and $v_1=0.001\\cdot0.25=0.00025$ — both moments are understated, by factors of 10 and 1000. The correction restores $\\hat m_1=0.5$ and $\\hat v_1=0.25$, and the ratio $\\hat m_1/\\sqrt{\\hat v_1}=1$: the weight moves by exactly $\\eta$. Without correction it would be $m_1/\\sqrt{v_1}=0.05/0.0158\\approx3.16$ — the step is $3.16$ times too large, because $\\sqrt{v_1}$ is understated more ($\\sqrt{1000}\\approx31.6$ times) than $m_1$ (10 times). Correcting only $m$ would make the step $31.6$ times too large; correcting only $v$ would make it 10 times too small."),
        ("p", "Note the third step: the gradients changed sign, so $\\hat m_3=0.23$ is noticeably smaller than the typical gradient size $\\sqrt{\\hat v_3}=0.39$, and Adam steps only $0.6\\eta$. The more consistent the gradients, the closer the step is to $\\eta$."),
    ]),
    dict(id="bias", title="Bias correction: where 1 − βᵗ comes from", blocks=[
        ("p", "The moments start at zero, and the first steps “remember” that zero. Unroll the recursion for $m_t$:"),
        ("eq", r"m_t=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{\,t-i}\,g_i"),
        ("p", "This is a weighted sum of gradients, but the weights add up not to 1 but to $(1-\\beta_1)(1+\\beta_1+\\dots+\\beta_1^{t-1})=1-\\beta_1^t$. The missing share $\\beta_1^t$ went to the initial zero. Hence the correction."),
        ("deep", "Derivation: $\\hat m_t$ and $\\hat v_t$ are unbiased", [
            ("p", "Let the gradients be stationary: $\\mathbb E[g_i]=\\mu$, $\\mathbb E[g_i^2]=s$ for all $i$. Then by linearity of expectation"),
            ("eq", r"\mathbb E[m_t]=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{\,t-i}\mu=\mu\,(1-\beta_1^{\,t}),\qquad \mathbb E[v_t]=s\,(1-\beta_2^{\,t})"),
            ("p", "Dividing by $1-\\beta^t$ gives $\\mathbb E[\\hat m_t]=\\mu$ and $\\mathbb E[\\hat v_t]=s$ — the estimates are unbiased from the very first step. If the gradients are non-stationary, a bias of the order of the change of $\\mu$ over the memory window remains; Kingma and Ba note that it can be kept small because the weights of the distant past are exponentially small."),
            ("p", "The correction matters only at the start: $\\beta_1^t&lt;0.01$ already for $t\\ge44$, but $\\beta_2^t&lt;0.01$ only for $t\\ge4603$. That is why it matters most for the second moment."),
        ]),
        ("viz", "adam-bias", {"b1": 0.9, "b2": 0.999}, "<b>Figure 2.</b> The correction factors $1/(1-\\beta_1^t)$ and $1/(1-\\beta_2^t)$ (both axes logarithmic) and the ratio of the uncorrected step to the corrected one for a constant gradient, $(1-\\beta_1^t)/\\sqrt{1-\\beta_2^t}$. With the standard $\\beta$ the first factors are 10 and 1000; the uncorrected step is $3.16$ times too large at the first step, most of all — $6.57$ times — at step 12, still $2.35$ times at step 200 and $1.26$ times at step 1000. With $\\beta_2=0.99$ the first steps coincide ($0.1/\\sqrt{0.01}=1$), but by step 13 the overshoot reaches $2.13$."),
        ("callout", "warn", "Why this matters in practice", "Without correction Adam’s early steps are several times longer than intended — exactly when the weights have just been initialized and the loss is at its largest. This is one of the reasons transformers without learning-rate warmup diverge in the first hundreds of steps; the correction itself removes this risk only partly, because in the first steps $\\hat v_t$ is estimated from just a few gradients."),
    ]),
    dict(id="properties", title="Properties of the step", blocks=[
        ("h3", "Scale invariance"),
        ("p", "Multiply all gradients of a weight by $c&gt;0$. Then $m_t$ is multiplied by $c$, $v_t$ by $c^2$, $\\sqrt{v_t}$ by $c$, and the ratio $\\hat m_t/\\sqrt{\\hat v_t}$ does not change. Adam’s step is a homogeneous function of degree zero in the gradients (as long as $\\sqrt{\\hat v_t}\\gg\\epsilon$). Each weight’s effective rate $\\eta/(\\sqrt{\\hat v_t}+\\epsilon)$ adapts by itself: large for weights with small gradients, small for weights with large ones."),
        ("viz", "adam-scale", {"eps": 1e-8}, "<b>Figure 3.</b> Four parameters with the same noisy gradient $c\\,(1+0.5\\xi_t)$ but scales $c$ from $10^{-3}$ to $10^{3}$; the bars are the step length at step 100 (log scale). SGD’s steps differ by a factor of $10^6$, Adam’s steps are identical: $8.8\\cdot10^{-4}=0.88\\,\\eta$, while the effective rate $\\eta/(\\sqrt{\\hat v}+\\epsilon)$ ranges from $8.8\\cdot10^{-7}$ to $0.88$. Lower the overall scale $k$ to $10^{-6}$: a gradient of order $10^{-9}$ becomes smaller than $\\epsilon=10^{-8}$, and its step drops 10 times — this is how $\\epsilon$ switches off adaptation for very small gradients."),
        ("h3", "The step and the signal-to-noise ratio"),
        ("p", "Let a weight’s gradient be stationary with mean $\\mu$ and standard deviation $\\sigma$. Then $\\hat m_t\\approx\\mu$, $\\hat v_t\\approx\\mu^2+\\sigma^2$ (the second moment is the squared mean plus the variance), and the mean step is"),
        ("eq", r"\frac{|\Delta\theta|}{\eta}\approx\frac{|\mu|}{\sqrt{\mu^2+\sigma^2}}=\frac{\mathrm{SNR}}{\sqrt{1+\mathrm{SNR}^2}},\qquad \mathrm{SNR}=\frac{|\mu|}{\sigma}"),
        ("p", "With a clean signal ($\\sigma\\ll|\\mu|$) the step is $\\approx\\eta$; in strong noise ($\\sigma\\gg|\\mu|$) it is proportional to the signal-to-noise ratio. This is automatic “braking”: near the minimum the mean gradient tends to zero while the noise remains — and Adam shortens its steps by itself."),
        ("viz", "adam-snr", {"b1": 0.9, "b2": 0.999, "snr": 0.3}, "<b>Figure 4.</b> Adam’s mean step (in units of $\\eta$) against the signal-to-noise ratio $\\mu/\\sigma$: the solid line is the formula above, the points are a 20,000-step simulation with a spread of $\\pm$ one standard deviation, the dashed line is SGD’s step, which grows in proportion to $\\mu$. At $\\mu/\\sigma=0.3$ the formula gives $0.287$, the simulation $0.298$ with a spread of $\\pm0.216$. With a weak signal the spread is close to $\\sqrt{(1-\\beta_1)/(1+\\beta_1)}\\approx0.23$: lower $\\beta_1$ and the steps become more erratic."),
        ("deep", "How large can the step get", [
            ("p", "Usually $|\\hat m_t|\\le\\sqrt{\\hat v_t}$ and the step does not exceed $\\eta$, but this is not a theorem. If the gradient was zero and suddenly became $g$, then for large $t$ we get $m_t=(1-\\beta_1)g$, $v_t=(1-\\beta_2)g^2$, and the step equals $\\eta(1-\\beta_1)/\\sqrt{1-\\beta_2}\\approx3.16\\,\\eta$ — the case discussed by Kingma and Ba. The exact upper bound follows from the Cauchy–Schwarz inequality for weighted sums:"),
            ("eq", r"\frac{|m_t|}{\sqrt{v_t}}\le\frac{1-\beta_1}{\sqrt{(1-\beta_2)\,(1-\beta_1^2/\beta_2)}}\approx7.27"),
            ("p", "(for $\\beta_1^2&lt;\\beta_2$). It is attained when the gradient grows by a factor of $\\beta_2/\\beta_1\\approx1.11$ per step. So Adam’s step is bounded by something of order $\\eta$ for any gradients — a built-in protection against their explosion."),
        ]),
        ("h3", "Special cases"),
        ("ul", [
            "$\\beta_1=\\beta_2=0$: $\\hat m_t=g_t$, $\\sqrt{\\hat v_t}=|g_t|$, the step is $\\eta\\operatorname{sign}(g_t)$ — sign gradient descent (signSGD).",
            "$\\beta_1=0$: RMSProp with bias correction.",
            "$\\epsilon\\gg\\sqrt{\\hat v_t}$: the step is $\\approx(\\eta/\\epsilon)\\,\\hat m_t$ — SGD with momentum and rate $\\eta/\\epsilon$.",
            "Adam is a <b>diagonal</b> preconditioner: it scales each coordinate separately and cannot rotate the axes (see Figure 6 on the <a href=\"../sgd/\">SGD</a> page).",
        ]),
    ]),
    dict(id="math", title="The mathematics behind the formula", blocks=[
        ("p", "Let us collect what hides behind the four lines."),
        ("ul", [
            "<b>EMA as a weighted average.</b> $\\hat m_t=\\sum_i w_i g_i$ with weights $w_i=(1-\\beta_1)\\beta_1^{t-i}/(1-\\beta_1^t)$, which are positive and sum to 1. The weight halves roughly every $\\ln2/(1-\\beta)$ steps: 7 for $\\beta_1=0.9$ and 693 for $\\beta_2=0.999$.",
            "<b>The effective window</b> $1/(1-\\beta)$: $m$ averages about the last 10 gradients, $v$ about the last 1000. The direction reacts fast, the scale slowly and therefore stably.",
            "<b>The second moment is not the variance.</b> $v$ estimates $\\mathbb E[g^2]=\\mu^2+\\sigma^2$, the “uncentred” size of the gradient. That is why with a clean signal the step is $\\approx\\eta$ rather than infinite.",
            "<b>The link to Newton’s method.</b> It is sometimes said that $\\sqrt v$ approximates the curvature. That is only partly true: $v$ estimates the diagonal of the empirical Fisher matrix (from mini-batch gradients), which for some losses is close to the Hessian near the minimum, but Adam takes its square root. It is safer to see Adam as step normalization rather than as an approximation to Newton.",
        ]),
        ("deep", "Convergence: a counterexample and AMSGrad", [
            ("p", "The original proof of Adam’s convergence for convex problems contained an error. Reddi, Kale and Kumar (2018) built a simple convex problem on which Adam converges to a worse point: a rare but large gradient is quickly “forgotten” in $v_t$, because the $\\beta_2$ memory is finite, and the effective rate $\\eta/\\sqrt{\\hat v_t}$ can grow."),
            ("p", "Their fix, AMSGrad, uses $\\hat v_t=\\max(\\hat v_{t-1},v_t)$ — the effective rate no longer grows, and convergence in the convex case can be proved. In practice AMSGrad is rarely noticeably better than Adam (in PyTorch it is the flag <code>amsgrad=True</code>). For non-convex problems guarantees exist for a decaying rate and a large enough $\\beta_2$."),
        ]),
    ]),
    dict(id="landscape", title="An optimizer race in 3D", blocks=[
        ("p", "Let us compare five methods on two surfaces. The first is a plateau with a pit: $f=1-e^{-q(x,y)}$, $q=0.2(x-1)^2+1.2(y-0.5)^2$. Far from the pit $f\\approx1$ and the gradient is tiny, while the pit itself is elongated. The second is the Rosenbrock banana."),
        ("viz", "adam-race", {"fn": "plateau"}, "<b>Figure 5.</b> On the left the surface in 3D (you can rotate it), on the right the view from above; the start can be dragged, and “Play” replays the race. At the start $(-2.4,\\,-1.5)$ the gradient is of order $4\\cdot10^{-3}$: SGD with $\\eta=0.3$ crawls across the plateau and reaches $f&lt;0.01$ only after 246 steps, Momentum after 61, RMSProp after 44, Adam after 58, AdamW after 53. But AdamW stops not at the minimum $(1,\\,0.5)$ but at $(0.979,\\,0.498)$, where $f=9\\cdot10^{-5}$: weight decay pulls towards zero. On Rosenbrock, within 2000 steps: Momentum takes 416 steps, Adam 717, AdamW 818, while SGD and RMSProp never reach $f&lt;0.01$."),
        ("callout", "intuition", "What the race teaches", "Adaptive methods win where gradients are badly scaled: on a plateau their step stays of order $\\eta$, while SGD’s is proportional to the tiny gradient. But well-tuned momentum can beat them (Rosenbrock), and weight decay shifts the solution — that is not a bug but regularization. There is no universal winner."),
    ]),
    dict(id="adamw", title="AdamW: weight decay done right", blocks=[
        ("p", "Classic $L_2$ regularization adds $\\tfrac\\lambda2\\|\\theta\\|^2$ to the loss, i.e. $\\lambda\\theta$ to the gradient. For SGD this is the same as multiplying the weights by $1-\\eta\\lambda$ at every step (weight decay). For Adam it is not: the term $\\lambda\\theta$ enters $m$ and $v$ and gets divided by $\\sqrt{\\hat v_t}$. Loshchilov and Hutter (2017) proposed to decouple decay from the gradient:"),
        ("eq", r"\text{Adam}+L_2:\quad \begin{aligned}g_t&=\nabla L(\theta_{t-1})+\lambda\,\theta_{t-1}\\ \theta_t&=\theta_{t-1}-\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}\end{aligned}"),
        ("eq", r"\text{AdamW}:\quad \theta_t=\theta_{t-1}-\eta\Bigl(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}+\lambda\,\theta_{t-1}\Bigr)"),
        ("p", "In AdamW the moments are computed from the loss gradient alone, and all weights decay at the same rate $\\eta\\lambda$ per step. In Adam with $L_2$ each weight’s decay is divided by its $\\sqrt{\\hat v_t}$: weights with large gradients are barely regularized, while weights with no loss gradient shrink at a constant speed of $\\approx\\eta$ per step, regardless of $\\lambda$."),
        ("viz", "adam-adamw", {"lam": 0.1}, "<b>Figure 6.</b> Three weights starting at $\\theta=1$; their data gradient alternates in sign, $\\pm c$ (zero on average), with $c=0$, $0.1$ and $10$. Rate $\\eta=0.01$, $\\lambda=0.1$, 1000 steps. AdamW (violet) shrinks all three equally, to $0.37\\approx e^{-\\eta\\lambda t}=e^{-1}$. Adam with $L_2$ (orange) wipes out the weight with no gradient (below $0.01$ already by step 213), shrinks the weight with $c=0.1$ to $0.0003$ and barely touches the weight with $c=10$, which keeps $0.889$."),
        ("callout", "key", "Takeaway", "In Adam, $L_2$ regularization and weight decay are different things. If you want decay, use <code>AdamW</code>; in PyTorch <code>torch.optim.Adam(weight_decay=…)</code> implements exactly $L_2$ inside the gradient. The default for <code>AdamW</code> is $\\lambda=0.01$; language models are usually trained with $\\lambda=0.1$ and without decay on biases and normalization weights."),
    ]),
    dict(id="training", title="Adam in training: warmup and schedules", blocks=[
        ("p", "Even an adaptive method needs a rate schedule. The most common scheme for transformers is a <b>linear warmup</b> from zero to $\\eta_{\\max}$ over the first hundreds or thousands of steps, followed by a <b>cosine decay</b> to $\\eta_{\\min}$:"),
        ("eq", r"\eta_t=\eta_{\max}\,\frac{t}{T_w}\qquad(t\le T_w)"),
        ("eq", r"\eta_t=\eta_{\min}+\tfrac12(\eta_{\max}-\eta_{\min})\bigl(1+\cos\pi p\bigr),\quad p=\frac{t-T_w}{T-T_w}"),
        ("viz", "adam-schedule", {"warm": 200, "minr": 0.1}, "<b>Figure 7.</b> Adam on a noisy quadratic problem (10 parameters with curvatures from $0.01$ to 1, gradient noise $0.05$), $\\eta_{\\max}=0.05$, 2000 steps. Top: the rate; bottom: the loss (log scale). With a constant $\\eta$ the loss gets stuck at the noise level $5.6\\cdot10^{-3}$ (mean of the last 100 steps); with a 200-step warmup and cosine down to $0.1\\,\\eta_{\\max}$ it reaches $7.1\\cdot10^{-4}$, $7.9$ times lower. Warmup only slightly delays the start here; its benefit shows in deep networks."),
        ("p", "Why decay helps: from the section on properties, Adam’s step near the minimum is proportional to $\\eta$ times the signal-to-noise ratio. The smaller $\\eta$, the smaller the cloud in which the weights jitter around the minimum."),
        ("p", "Why warmup is needed: in the first steps $\\hat v_t$ is estimated from a few gradients and is very noisy, while the weights have just been initialized and the gradients are especially large. Liu et al. (RAdam, 2019) showed that the variance of the effective rate $\\eta/\\sqrt{\\hat v_t}$ is large early in training and proposed to rectify it analytically; warmup solves the same problem more simply."),
        ("callout", "note", "A typical recipe for language models", "AdamW with $\\beta_1=0.9$, $\\beta_2=0.95$, $\\lambda=0.1$, gradient clipping at norm 1, warmup over ~2000 steps and a cosine down to 10% of $\\eta_{\\max}$ — this is, for example, how the training of LLaMA is described. A smaller $\\beta_2$ (a window of 20 steps instead of 1000) reacts faster to gradient spikes and makes training of large models more stable."),
    ]),
    dict(id="code", title="In code: from scratch and in PyTorch", blocks=[
        ("p", "A from-scratch implementation takes twenty lines. The <code>decoupled</code> flag switches weight decay between AdamW and $L_2$ inside the gradient."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "The output matches the table from “The formula, bone by bone”, and <code>torch.optim.Adam</code> moves the weight by exactly $\\eta$ on the same first step. A typical training loop with AdamW, separate decay groups, warmup and cosine:"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "warn", "Memory", "Adam stores $m$ and $v$ — two numbers per parameter. For a 7-billion-parameter model that is $2\\cdot7\\cdot10^9\\cdot4$ bytes $=56$ GB in float32 for the optimizer state alone. Hence 8-bit optimizers, state sharding (ZeRO) and frugal variants such as Adafactor."),
    ]),
    dict(id="practice", title="Hyperparameters and practice", blocks=[
        ("table", ["Parameter", "Default", "Typical range and meaning"], [
            ["$\\eta$", "$10^{-3}$", "$10^{-4}$–$3\\cdot10^{-3}$; transformers — about $3\\cdot10^{-4}$ and lower as models grow; fine-tuning — $10^{-5}$–$5\\cdot10^{-5}$"],
            ["$\\beta_1$", "$0.9$", "almost never changed; a direction window of 10 steps"],
            ["$\\beta_2$", "$0.999$", "$0.95$–$0.98$ for large transformers: reacts faster to spikes"],
            ["$\\epsilon$", "$10^{-8}$", "larger ($10^{-6}$ and up) in low precision or when unstable; a too large $\\epsilon$ turns Adam into SGD with momentum"],
            ["$\\lambda$ (AdamW)", "$0.01$", "$0.01$–$0.1$; do not apply to biases and normalization layers"],
            ["warmup", "—", "from hundreds to a few thousand steps, 1–5% of training"],
        ], {}),
        ("ul", [
            "<b>Start with the defaults.</b> $\\eta=10^{-3}$ (or $3\\cdot10^{-4}$ for transformers), $\\beta=(0.9,\\,0.999)$, AdamW with $\\lambda=0.01$. Tune $\\eta$ first, then $\\lambda$ and the schedule.",
            "<b>Gradient clipping</b> by norm ($1.0$) is almost free and saves you from rare outliers.",
            "<b>Save the optimizer state</b> (<code>opt.state_dict()</code>) together with the weights: when resuming with zero $m$ and $v$ the first steps will be “cold” again.",
            "<b>When SGD is better.</b> On computer-vision tasks a well-tuned SGD with momentum often generalizes better (Wilson et al., 2017). For transformers, recommender systems with embeddings and problems with sparse gradients Adam wins.",
        ]),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b><code>Adam(weight_decay=…)</code> instead of <code>AdamW</code>.</b> That is $L_2$ inside the gradient: the decay is divided by $\\sqrt{\\hat v_t}$ and acts unevenly (Figure 6).",
            "<b>A rate taken from SGD.</b> $\\eta=0.1$ is fine for SGD with momentum, but for Adam it means a step of about $0.1$ in weight units at every step — training will almost surely diverge.",
            "<b>Decay on all parameters.</b> Biases and LayerNorm/BatchNorm weights are usually excluded from weight decay: shrinking them towards zero hurts rather than regularizes.",
            "<b>A poor $\\epsilon$.</b> A too small one rounds to zero in float16; a too large one ($\\gtrsim\\sqrt{\\hat v}$) silently switches adaptation off — the step becomes $(\\eta/\\epsilon)\\hat m$.",
            "<b>No warmup on a transformer.</b> A large $\\eta$ from the first steps, with a noisy estimate $\\hat v_t$, often makes the loss explode early in training.",
            "<b>The schedule on the wrong step.</b> <code>scheduler.step()</code> once per epoch where the schedule is defined in steps (or vice versa) stretches warmup hundreds of times.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            "<a href=\"../sgd/\">SGD, Momentum and RMSProp</a>: Adam’s numerator is EMA momentum, its denominator is $\\sqrt v$ from RMSProp; that page also covers the stability condition and the condition number.",
            "<a href=\"../cross-entropy/\">Cross-entropy</a> and <a href=\"../softmax/\">softmax</a>: the loss AdamW minimizes in language models; its gradient with respect to the logits, $s-y$, is the $g_t$ of the last layer.",
            "<a href=\"../mse/\">MSE</a> and <a href=\"../huber/\">Huber</a>: the scale of the target sets the scale of the gradient — Adam is insensitive to it, SGD is not.",
            "<a href=\"../gelu/\">GELU</a> and <a href=\"../silu/\">SiLU</a>: the activations of transformers trained with AdamW.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) Adam keeps two exponential averages: $m_t$ of the gradient (direction, a window of ~10 steps) and $v_t$ of its square (scale, a window of ~1000 steps). 2) Both start at zero and are understated by a factor of $1-\\beta^t$; the correction makes them unbiased, and without it early steps overshoot — by $3.16$ times at the first step. 3) The step $\\eta\\,\\hat m_t/(\\sqrt{\\hat v_t}+\\epsilon)$ does not depend on the gradient’s scale, is of order $\\eta$ with a clean signal and proportional to the signal-to-noise ratio in noise. 4) AdamW decouples weight decay from the gradient — all weights decay evenly. 5) In practice: AdamW, warmup, cosine, gradient clipping; $\\eta$ is the main hyperparameter."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="Adam’s first step with bias correction, $g_1=-3$. How does the weight change?", options=["It decreases by $3\\eta$", "It increases by $\\eta$", "It decreases by $\\eta$", "It increases by $3\\eta$"], answer=1,
                 explain="$\\hat m_1=g_1=-3$, $\\sqrt{\\hat v_1}=|g_1|=3$, the step is $-\\eta\\cdot(-3)/3=+\\eta$: the weight grows by $\\eta$, whatever $|g_1|$ is."),
            dict(q="Roughly how many recent steps does $v_t$ “remember” at $\\beta_2=0.999$?", options=["10", "100", "1000", "10 000"], answer=2,
                 explain="The effective window is $1/(1-\\beta_2)=1000$ steps."),
            dict(q="All gradients of a model are multiplied by 100 (for example, the loss is multiplied by 100). What happens to Adam’s steps?", options=["They grow 100 times", "They grow 10 times", "They hardly change", "They shrink 100 times"], answer=2,
                 explain="$\\hat m$ and $\\sqrt{\\hat v}$ grow 100 times, and their ratio stays the same (as long as $\\epsilon$ is negligible)."),
            dict(q="How does AdamW differ from Adam with $L_2$ regularization?", options=["It does not, they are synonyms", "Weight decay does not go through $m$ and $v$ and is not divided by $\\sqrt{\\hat v}$", "AdamW does not use bias correction", "AdamW uses the sign of the gradient"], answer=1,
                 explain="In AdamW the weights are multiplied by $1-\\eta\\lambda$ separately from the adaptive step, so the decay is the same for all weights."),
            dict(q="By how much is Adam’s first step too large without bias correction at $\\beta_1=0.9$, $\\beta_2=0.999$?", options=["$0.1$ times (10 times too small)", "It is not too large", "$3.16$ times", "1000 times"], answer=2,
                 explain="$m_1/\\sqrt{v_1}=(1-\\beta_1)g/(\\sqrt{1-\\beta_2}\\,|g|)=0.1/0.0316\\approx3.16$."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="Adam nima uchun kerak", blocks=[
        ("p", "Neyron tarmoqda millionlab vazn bor va ularning gradiyentlari juda turli masshtablarda yashaydi: kam uchraydigan tokenlar embeddinglari kamdan-kam katta turtki oladi, oxirgi qatlamlar — doimiy kichiklarini, normallashtirish qatlamlari — yana boshqacha. Oddiy <a href=\"../sgd/\">SGD</a> $\\eta g$ qadam tashlaydi va barcha uchun bitta $\\eta$ tezlik bir vaqtda ba’zi vaznlar uchun juda katta, boshqalari uchun juda kichik. Bundan tashqari, mini-batch gradiyenti shovqinli, yo‘qotish sirti esa cho‘ziq jarliklar va platolarga to‘la."),
        ("p", "Adam (adaptive moment estimation, Kingma va Ba, 2014) ikkala masalani bitta formula bilan hal qiladi:"),
        ("ul", [
            "<b>birinchi moment</b> $m_t$ — gradiyentlarning eksponensial o‘rtachasi: shovqin va zigzaglarni so‘ndiradigan inersiya (<a href=\"../sgd/\">Momentum</a> kabi);",
            "<b>ikkinchi moment</b> $v_t$ — gradiyent kvadratlarining eksponensial o‘rtachasi: har bir vazn gradiyentining odatiy kattaligi, qadam unga bo‘linadi (RMSProp kabi);",
            "<b>siljishni tuzatish</b> — $1-\\beta^t$ ga bo‘lish, u dastlabki qadamlarda momentlarning tizimli kam baholanishini yo‘qotadi.",
        ]),
        ("p", "Natija: har bir vazn qadami gradiyent masshtabidan qat’i nazar $\\eta$ tartibida, har bir qatlam uchun qo‘lda sozlashsiz. Shuning uchun Adam ko‘pchilik masalalarda standart optimizator, uning AdamW varianti esa transformerlar va katta til modellarini o‘qitadi."),
        ("callout", "key", "Bir daqiqada asosiysi", "$m_t$ — qayerga borish (silliqlangan gradiyent), $\\sqrt{v_t}$ — qanchalik katta qadam tashlash (o‘rta kvadratik gradiyent), $1-\\beta^t$ — noldan boshlanganlik uchun tuzatish. $\\eta\\,\\hat m_t/(\\sqrt{\\hat v_t}+\\epsilon)$ qadam o‘lchamsiz: gradiyentlarni 1000 ga ko‘paytiring — qadamlar o‘zgarmaydi. Toza signalda qadam $\\approx\\eta$, shovqinda — kichikroq. AdamW vaznlar so‘nishini gradiyentdan chiqaradi."),
    ]),
    dict(id="intuition", title="Intuitsiya: kompas va spidometr", blocks=[
        ("p", "Yo‘lsiz joyda titrab turgan kompas ko‘rsatkichi bo‘yicha mashina haydayotganingizni tasavvur qiling. Uning har bir siltanishida rulni burish ahmoqlik — o‘rtachalangan yo‘nalishni kuzatish oqilonaroq. Bu $m_t$. Tezlikni esa siltanishlar odatda qanchalik kuchli ekaniga qarab tanlash kerak: tekis yo‘lda ishonch bilan, o‘nqir-cho‘nqirda ehtiyotkorlik bilan. Bu $\\sqrt{v_t}$: Adam qadami — turtkilar odatiy kuchiga bo‘lingan yo‘nalish."),
        ("p", "Rasmda — bitta vazn gradiyentlari oqimi: 100-qadamgacha o‘rtacha $+0{,}5$, keyin $-0{,}5$, ustiga shovqin. To‘q sariq chiziq — silliqlangan gradiyent $\\hat m_t$, firuza rangdagilar — $\\pm\\sqrt{\\hat v_t}$ yo‘lak, pastda — $\\eta$ birliklarida yakuniy qadam."),
        ("viz", "adam-moments", {"b1": 0.9, "b2": 0.999, "sigma": 1, "t": 1}, "<b>1-rasm.</b> Shovqinli gradiyentda ($\\sigma=1$) Adam momentlari. $t$ slayderi rasm ostidagi jadval uchun qadamni tanlaydi. Birinchi qadamda aynan $\\hat m_1/\\sqrt{\\hat v_1}=1$ — $g_1$ qanday bo‘lmasin, qadam $g_1$ ga qarshi tomonga $\\eta$ ga teng; tuzatishsiz nisbat $3{,}16$ bo‘lardi. O‘rtacha ishorasi almashgach, $\\hat m_t$ 109-qadamdan boshlab butunlay manfiy bo‘ladi, $\\sqrt{\\hat v_t}$ esa deyarli o‘zgarmaydi ($\\approx1{,}1$): qadam kattaligini signal/shovqin nisbati belgilaydi, $0{,}5/\\sqrt{1{,}25}\\approx0{,}45$. Hatto 200-qadamda ham tuzatishsiz qadam (shtrix) to‘g‘risidan $2{,}35$ marta katta."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "Shovqinni olib tashlang ($\\sigma=0$): qadam darhol aynan $\\pm1$ bo‘ladi — toza signalda Adam ishora usuli kabi $\\eta$ qadamlar bilan yuradi. Shovqinni oshiring — qadam qisqaradi. $\\beta_1$ ni nolgacha kamaytiring — $\\hat m_t$ gradiyentning o‘ziga aylanadi va qadam $\\pm1$ orasida sakraydi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("eq", r"\begin{aligned}g_t&=\nabla_\theta L(\theta_{t-1})\\ m_t&=\beta_1 m_{t-1}+(1-\beta_1)\,g_t\\ v_t&=\beta_2 v_{t-1}+(1-\beta_2)\,g_t^2\\ \hat m_t&=\frac{m_t}{1-\beta_1^{\,t}},\qquad \hat v_t=\frac{v_t}{1-\beta_2^{\,t}}\\ \theta_t&=\theta_{t-1}-\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}\end{aligned}"),
        ("symbols", [
            (r"g_t", "$t$-qadamdagi mini-batch gradiyenti (qadamlar 1 dan raqamlanadi);"),
            (r"m_t", "birinchi moment: gradiyentning eksponensial sirpanuvchi o‘rtachasi (EMA), $m_0=0$;"),
            (r"v_t", "ikkinchi moment: gradiyent elementma-element kvadratining EMA’si, $v_0=0$; har bir vaznning o‘z $m$ va $v$ si bor;"),
            (r"\beta_1,\ \beta_2", "so‘nish koeffitsiyentlari, standart $0{,}9$ va $0{,}999$: xotira taxminan $1/(1-\\beta)$ qadam — 10 va 1000;"),
            (r"1-\beta^t", "siljishni tuzatish: momentlarning noldan boshlanishini qoplaydi;"),
            (r"\eta", "o‘qitish tezligi (learning rate), standart $10^{-3}$; bu yerda u vazn birliklarida odatiy qadam uzunligini belgilaydi;"),
            (r"\epsilon", "nolga bo‘lishdan saqlovchi kichik qo‘shimcha ($10^{-8}$)."),
        ]),
        ("p", "Standart $\\beta_1=0{,}9$, $\\beta_2=0{,}999$ da $0{,}5$, $-0{,}2$, $0{,}4$ gradiyentlar uchun uchta qadamni qo‘lda bajaramiz. Oxirgi ustun — siljishni tuzatishsiz qadam qanday bo‘lardi."),
        ("table", ["$t$", "$g_t$", "$m_t$", "$v_t$", "$\\hat m_t$", "$\\sqrt{\\hat v_t}$", "qadam $/\\eta$", "tuzatishsiz"], "STEPS", {"num": [0, 1, 2, 3, 4, 5, 6, 7]}),
        ("callout", "note", "Birinchi qadam batafsil", "$g_1=0{,}5$: $m_1=0{,}1\\cdot0{,}5=0{,}05$ va $v_1=0{,}001\\cdot0{,}25=0{,}00025$ — ikkala moment ham kam baholangan, 10 va 1000 marta. Tuzatish $\\hat m_1=0{,}5$ va $\\hat v_1=0{,}25$ ni qaytaradi, nisbat $\\hat m_1/\\sqrt{\\hat v_1}=1$: vazn aynan $\\eta$ ga siljiydi. Tuzatishsiz $m_1/\\sqrt{v_1}=0{,}05/0{,}0158\\approx3{,}16$ bo‘lardi — qadam $3{,}16$ marta oshib ketadi, chunki $\\sqrt{v_1}$ $m_1$ dan (10 marta) kuchliroq ($\\sqrt{1000}\\approx31{,}6$ marta) kam baholangan. Faqat $m$ tuzatilsa, qadam $31{,}6$ marta o‘sardi; faqat $v$ — 10 marta kamayardi."),
        ("p", "Uchinchi qadamga e’tibor bering: gradiyentlar ishorasini almashtirdi, shuning uchun $\\hat m_3=0{,}23$ gradiyentning odatiy kattaligi $\\sqrt{\\hat v_3}=0{,}39$ dan sezilarli kichik va Adam atigi $0{,}6\\eta$ qadam tashlaydi. Gradiyentlar qanchalik mos bo‘lsa, qadam $\\eta$ ga shunchalik yaqin."),
    ]),
    dict(id="bias", title="Siljishni tuzatish: 1 − βᵗ qayerdan", blocks=[
        ("p", "Momentlar noldan boshlanadi va dastlabki qadamlar shu nolni «eslab qoladi». $m_t$ uchun rekursiyani ochamiz:"),
        ("eq", r"m_t=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{\,t-i}\,g_i"),
        ("p", "Bu gradiyentlarning vaznli yig‘indisi, lekin vaznlar yig‘indisi 1 emas, $(1-\\beta_1)(1+\\beta_1+\\dots+\\beta_1^{t-1})=1-\\beta_1^t$ ga teng. Yetishmayotgan $\\beta_1^t$ ulush boshlang‘ich nolga tegdi. Tuzatish shundan."),
        ("deep", "Keltirib chiqarish: $\\hat m_t$ va $\\hat v_t$ ning siljimaganligi", [
            ("p", "Gradiyentlar statsionar bo‘lsin: barcha $i$ uchun $\\mathbb E[g_i]=\\mu$, $\\mathbb E[g_i^2]=s$. U holda matematik kutilmaning chiziqliligiga ko‘ra"),
            ("eq", r"\mathbb E[m_t]=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{\,t-i}\mu=\mu\,(1-\beta_1^{\,t}),\qquad \mathbb E[v_t]=s\,(1-\beta_2^{\,t})"),
            ("p", "$1-\\beta^t$ ga bo‘lish $\\mathbb E[\\hat m_t]=\\mu$ va $\\mathbb E[\\hat v_t]=s$ ni beradi — baholar birinchi qadamdanoq siljimagan. Agar gradiyentlar nostatsionar bo‘lsa, xotira oynasi davomida $\\mu$ ning o‘zgarishi tartibidagi siljish qoladi; Kingma va Ba uni kichik ushlab turish mumkinligini ta’kidlaydi, chunki uzoq o‘tmish vaznlari eksponensial kichik."),
            ("p", "Tuzatish faqat boshida kerak: $\\beta_1^t&lt;0{,}01$ allaqachon $t\\ge44$ da, $\\beta_2^t&lt;0{,}01$ esa faqat $t\\ge4603$ da. Shuning uchun u ikkinchi moment uchun eng muhim."),
        ]),
        ("viz", "adam-bias", {"b1": 0.9, "b2": 0.999}, "<b>2-rasm.</b> $1/(1-\\beta_1^t)$ va $1/(1-\\beta_2^t)$ tuzatish ko‘paytuvchilari (ikkala o‘q ham logarifmik) va o‘zgarmas gradiyentda tuzatishsiz qadamning tuzatishliga nisbati, $(1-\\beta_1^t)/\\sqrt{1-\\beta_2^t}$. Standart $\\beta$ larda birinchi ko‘paytuvchilar — 10 va 1000; tuzatishsiz qadam birinchi qadamda $3{,}16$ marta, eng ko‘p — $6{,}57$ marta — 12-qadamda, 200-qadamda hali $2{,}35$ marta va 1000-qadamda $1{,}26$ marta oshib ketgan. $\\beta_2=0{,}99$ da birinchi qadamlar mos keladi ($0{,}1/\\sqrt{0{,}01}=1$), lekin 13-qadamga kelib oshish $2{,}13$ ga yetadi."),
        ("callout", "warn", "Amaliyotda nega bu muhim", "Tuzatishsiz Adam’ning dastlabki qadamlari mo‘ljallanganidan bir necha marta uzun — aynan vaznlar endigina initsializatsiya qilingan va yo‘qotish eng katta bo‘lgan paytda. Bu qizdirishsiz (warmup) transformerlar dastlabki yuzlab qadamlarda uzoqlashib ketishining sabablaridan biri; tuzatishning o‘zi bu xavfni qisman yo‘qotadi, chunki dastlabki qadamlarda $\\hat v_t$ atigi bir nechta gradiyent bo‘yicha baholangan."),
    ]),
    dict(id="properties", title="Qadam xossalari", blocks=[
        ("h3", "Masshtab invariantligi"),
        ("p", "Vaznning barcha gradiyentlarini $c&gt;0$ ga ko‘paytiramiz. U holda $m_t$ $c$ ga, $v_t$ $c^2$ ga, $\\sqrt{v_t}$ $c$ ga ko‘payadi va $\\hat m_t/\\sqrt{\\hat v_t}$ nisbat o‘zgarmaydi. Adam qadami gradiyentlarning nolinchi darajali bir jinsli funksiyasi ($\\sqrt{\\hat v_t}\\gg\\epsilon$ ekan). Har bir vaznning samarali tezligi $\\eta/(\\sqrt{\\hat v_t}+\\epsilon)$ o‘zi moslashadi: kichik gradiyentli vaznlarda katta, katta gradiyentlilarda kichik."),
        ("viz", "adam-scale", {"eps": 1e-8}, "<b>3-rasm.</b> Bir xil shovqinli $c\\,(1+0{,}5\\xi_t)$ gradiyentli, lekin $c$ masshtablari $10^{-3}$ dan $10^{3}$ gacha bo‘lgan to‘rtta parametr; ustunlar — yuzinchi qadamdagi qadam uzunligi (logarifmik shkala). SGD qadamlari $10^6$ marta farq qiladi, Adam qadamlari bir xil: $8{,}8\\cdot10^{-4}=0{,}88\\,\\eta$, samarali tezlik $\\eta/(\\sqrt{\\hat v}+\\epsilon)$ esa $8{,}8\\cdot10^{-7}$ dan $0{,}88$ gacha o‘zgaradi. Umumiy $k$ masshtabni $10^{-6}$ gacha kamaytiring: $10^{-9}$ tartibidagi gradiyent $\\epsilon=10^{-8}$ dan kichik bo‘lib qoladi va uning qadami 10 marta tushadi — $\\epsilon$ juda kichik gradiyentlar uchun moslashuvni shunday o‘chiradi."),
        ("h3", "Qadam va signal/shovqin nisbati"),
        ("p", "Vazn gradiyenti $\\mu$ o‘rtacha va $\\sigma$ standart chetlanish bilan statsionar bo‘lsin. U holda $\\hat m_t\\approx\\mu$, $\\hat v_t\\approx\\mu^2+\\sigma^2$ (ikkinchi moment — o‘rtacha kvadrati plyus dispersiya) va o‘rtacha qadam"),
        ("eq", r"\frac{|\Delta\theta|}{\eta}\approx\frac{|\mu|}{\sqrt{\mu^2+\sigma^2}}=\frac{\mathrm{SNR}}{\sqrt{1+\mathrm{SNR}^2}},\qquad \mathrm{SNR}=\frac{|\mu|}{\sigma}"),
        ("p", "Toza signalda ($\\sigma\\ll|\\mu|$) qadam $\\approx\\eta$, kuchli shovqinda ($\\sigma\\gg|\\mu|$) u signal/shovqin nisbatiga proporsional. Bu avtomatik «tormoz»: minimum yonida o‘rtacha gradiyent nolga intiladi, shovqin esa qoladi — va Adam qadamlarni o‘zi qisqartiradi."),
        ("viz", "adam-snr", {"b1": 0.9, "b2": 0.999, "snr": 0.3}, "<b>4-rasm.</b> Adam’ning o‘rtacha qadami ($\\eta$ birliklarida) $\\mu/\\sigma$ signal/shovqin nisbatiga bog‘liq holda: uzluksiz chiziq — yuqoridagi formula, nuqtalar — $\\pm$ bitta standart chetlanish tarqoqligi bilan 20 000 qadamli simulyatsiya, shtrix — $\\mu$ ga proporsional o‘suvchi SGD qadami. $\\mu/\\sigma=0{,}3$ da formula $0{,}287$, simulyatsiya — $\\pm0{,}216$ tarqoqlik bilan $0{,}298$ beradi. Kuchsiz signalda tarqoqlik $\\sqrt{(1-\\beta_1)/(1+\\beta_1)}\\approx0{,}23$ ga yaqin: $\\beta_1$ ni kamaytiring — qadamlar tartibsizroq bo‘ladi."),
        ("deep", "Qadam qanchalik katta bo‘lishi mumkin", [
            ("p", "Odatda $|\\hat m_t|\\le\\sqrt{\\hat v_t}$ va qadam $\\eta$ dan oshmaydi, lekin bu teorema emas. Agar gradiyent nol bo‘lib, birdan $g$ ga aylansa, katta $t$ larda $m_t=(1-\\beta_1)g$, $v_t=(1-\\beta_2)g^2$ va qadam $\\eta(1-\\beta_1)/\\sqrt{1-\\beta_2}\\approx3{,}16\\,\\eta$ ga teng — bu holatni Kingma va Ba ko‘rib chiqadi. Aniq yuqori chegara vaznli yig‘indilar uchun Koshi — Bunyakovskiy tengsizligidan kelib chiqadi:"),
            ("eq", r"\frac{|m_t|}{\sqrt{v_t}}\le\frac{1-\beta_1}{\sqrt{(1-\beta_2)\,(1-\beta_1^2/\beta_2)}}\approx7{,}27"),
            ("p", "($\\beta_1^2&lt;\\beta_2$ da). Unga gradiyent har qadamda $\\beta_2/\\beta_1\\approx1{,}11$ marta o‘sganda erishiladi. Demak, Adam qadami har qanday gradiyentlarda $\\eta$ tartibidagi kattalik bilan chegaralangan — ularning portlashidan ichki himoya."),
        ]),
        ("h3", "Xususiy holatlar"),
        ("ul", [
            "$\\beta_1=\\beta_2=0$: $\\hat m_t=g_t$, $\\sqrt{\\hat v_t}=|g_t|$, qadam $\\eta\\operatorname{sign}(g_t)$ — ishorali gradiyentli tushish (signSGD).",
            "$\\beta_1=0$: siljishni tuzatishli RMSProp.",
            "$\\epsilon\\gg\\sqrt{\\hat v_t}$: qadam $\\approx(\\eta/\\epsilon)\\,\\hat m_t$ — $\\eta/\\epsilon$ tezlikli inersiyali SGD.",
            "Adam — <b>diagonal</b> oldindan shartlovchi: u har bir koordinatani alohida masshtablaydi va o‘qlarni bura olmaydi (<a href=\"../sgd/\">SGD</a> sahifasidagi 6-rasmga qarang).",
        ]),
    ]),
    dict(id="math", title="Formula ortidagi matematika", blocks=[
        ("p", "To‘rt qator ortida yashiringan narsalarni jamlaymiz."),
        ("ul", [
            "<b>Vaznli o‘rtacha sifatida EMA.</b> $\\hat m_t=\\sum_i w_i g_i$, vaznlar $w_i=(1-\\beta_1)\\beta_1^{t-i}/(1-\\beta_1^t)$ musbat va yig‘indisi 1 ga teng. Vazn taxminan har $\\ln2/(1-\\beta)$ qadamda ikki marta kamayadi: $\\beta_1=0{,}9$ uchun 7 va $\\beta_2=0{,}999$ uchun 693.",
            "<b>Samarali oyna</b> $1/(1-\\beta)$: $m$ taxminan oxirgi 10 ta gradiyentni, $v$ — taxminan 1000 tasini o‘rtachalaydi. Yo‘nalish tez, masshtab esa sekin va shuning uchun barqaror javob beradi.",
            "<b>Ikkinchi moment — dispersiya emas.</b> $v$ $\\mathbb E[g^2]=\\mu^2+\\sigma^2$ ni, ya’ni gradiyentning «markazlashtirilmagan» kattaligini baholaydi. Shuning uchun toza signalda qadam cheksiz emas, $\\approx\\eta$.",
            "<b>Nyuton usuli bilan bog‘liqlik.</b> Ba’zan $\\sqrt v$ egrilikni yaqinlashtiradi deyishadi. Bu faqat qisman to‘g‘ri: $v$ — empirik Fisher matritsasi diagonalining bahosi (mini-batch gradiyentlari bo‘yicha), ba’zi yo‘qotishlar uchun u minimum yonida gessianga yaqin, lekin Adam undan kvadrat ildiz oladi. Adam’ni Nyuton yaqinlashuvi emas, qadamni normallashtirish deb tushunish ishonchliroq.",
        ]),
        ("deep", "Yaqinlashish: qarshi misol va AMSGrad", [
            ("p", "Qavariq masalalar uchun Adam yaqinlashishining dastlabki isbotida xato bor edi. Reddi, Keyl va Kumar (2018) Adam yomonroq nuqtaga yaqinlashadigan oddiy qavariq masala tuzishdi: kamdan-kam, lekin katta gradiyent $v_t$ da tez «unutiladi», chunki $\\beta_2$-xotira chekli, va samarali tezlik $\\eta/\\sqrt{\\hat v_t}$ o‘sishi mumkin."),
            ("p", "Ularning tuzatmasi AMSGrad $\\hat v_t=\\max(\\hat v_{t-1},v_t)$ dan foydalanadi — samarali tezlik endi o‘smaydi va qavariq holatda yaqinlashish isbotlanadi. Amaliyotda AMSGrad kamdan-kam hollarda Adam’dan sezilarli yaxshiroq (PyTorch’da — <code>amsgrad=True</code> bayrog‘i). Qavariq bo‘lmagan masalalar uchun kafolatlar kamayuvchi tezlik va yetarlicha katta $\\beta_2$ da olingan."),
        ]),
    ]),
    dict(id="landscape", title="3D’da optimizatorlar poygasi", blocks=[
        ("p", "Beshta usulni ikkita sirtda solishtiramiz. Birinchisi — chuqurli plato: $f=1-e^{-q(x,y)}$, $q=0{,}2(x-1)^2+1{,}2(y-0{,}5)^2$. Chuqurlikdan uzoqda $f\\approx1$, gradiyent juda kichik, chuqurlikning o‘zi esa cho‘ziq. Ikkinchisi — Rozenbrok banani."),
        ("viz", "adam-race", {"fn": "plateau"}, "<b>5-rasm.</b> Chapda 3D sirt (uni aylantirish mumkin), o‘ngda yuqoridan ko‘rinish; startni sudrab ko‘chirish mumkin, «Boshlash» poygani qayta ko‘rsatadi. $(-2{,}4;\\,-1{,}5)$ start nuqtasida gradiyent $4\\cdot10^{-3}$ tartibida: $\\eta=0{,}3$ li SGD plato bo‘ylab sudraladi va $f&lt;0{,}01$ ga faqat 246 qadamda yetadi, Momentum — 61 da, RMSProp — 44 da, Adam — 58 da, AdamW — 53 da. Lekin AdamW $(1;\\,0{,}5)$ minimumda emas, $f=9\\cdot10^{-5}$ bo‘lgan $(0{,}979;\\,0{,}498)$ da to‘xtaydi: vaznlar so‘nishi nolga tortadi. Rozenbrokda 2000 qadam ichida: Momentum — 416 qadam, Adam — 717, AdamW — 818, SGD va RMSProp esa $f&lt;0{,}01$ ga yetmaydi."),
        ("callout", "intuition", "Poyga nimani o‘rgatadi", "Adaptiv usullar gradiyentlar yomon masshtablangan joyda yutadi: platoda ularning qadami $\\eta$ tartibida qoladi, SGD’niki esa juda kichik gradiyentga proporsional. Lekin yaxshi sozlangan inersiya ulardan o‘zib ketishi mumkin (Rozenbrok), vaznlar so‘nishi esa yechimni siljitadi — bu xato emas, regulyarizatsiya. Universal g‘olib yo‘q."),
    ]),
    dict(id="adamw", title="AdamW: vaznlarning to‘g‘ri so‘nishi", blocks=[
        ("p", "Klassik $L_2$-regulyarizatsiya yo‘qotishga $\\tfrac\\lambda2\\|\\theta\\|^2$, ya’ni gradiyentga $\\lambda\\theta$ qo‘shadi. SGD uchun bu har qadamda vaznlarni $1-\\eta\\lambda$ ga ko‘paytirish bilan bir xil (vaznlar so‘nishi, weight decay). Adam uchun — yo‘q: $\\lambda\\theta$ qo‘shiluvchi $m$ va $v$ ga tushadi va $\\sqrt{\\hat v_t}$ ga bo‘linadi. Loshchilov va Xatter (2017) so‘nishni gradiyentdan ajratishni taklif qilishdi:"),
        ("eq", r"\text{Adam}+L_2:\quad \begin{aligned}g_t&=\nabla L(\theta_{t-1})+\lambda\,\theta_{t-1}\\ \theta_t&=\theta_{t-1}-\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}\end{aligned}"),
        ("eq", r"\text{AdamW}:\quad \theta_t=\theta_{t-1}-\eta\Bigl(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}+\lambda\,\theta_{t-1}\Bigr)"),
        ("p", "AdamW’da momentlar faqat yo‘qotish gradiyenti bo‘yicha hisoblanadi, barcha vaznlar esa qadam boshiga bir xil $\\eta\\lambda$ tezlikda so‘nadi. $L_2$ li Adam’da har bir vazn so‘nishi uning $\\sqrt{\\hat v_t}$ siga bo‘linadi: katta gradiyentli vaznlar deyarli regulyarizatsiya qilinmaydi, yo‘qotish gradiyenti yo‘q vaznlar esa $\\lambda$ dan qat’i nazar qadam boshiga $\\approx\\eta$ o‘zgarmas tezlikda qisqaradi."),
        ("viz", "adam-adamw", {"lam": 0.1}, "<b>6-rasm.</b> $\\theta=1$ dan boshlanadigan uchta vazn; ularning ma’lumot gradiyenti ishorasini almashtiradi, $\\pm c$ (o‘rtacha nol), $c=0$, $0{,}1$ va $10$. Tezlik $\\eta=0{,}01$, $\\lambda=0{,}1$, 1000 qadam. AdamW (binafsha) uchalasini bir xil, $0{,}37\\approx e^{-\\eta\\lambda t}=e^{-1}$ gacha kamaytiradi. $L_2$ li Adam (to‘q sariq) gradiyentsiz vaznni nolga tushiradi (213-qadamdayoq $0{,}01$ dan past), $c=0{,}1$ li vaznni $0{,}0003$ gacha qisqartiradi va $c=10$ li vaznga deyarli tegmaydi — unda $0{,}889$ qoladi."),
        ("callout", "key", "Xulosa", "Adam’da $L_2$-regulyarizatsiya va vaznlar so‘nishi — turli narsalar. So‘nish kerak bo‘lsa, <code>AdamW</code> dan foydalaning; PyTorch’da <code>torch.optim.Adam(weight_decay=…)</code> aynan gradiyent ichidagi $L_2$ ni amalga oshiradi. <code>AdamW</code> da standart $\\lambda=0{,}01$; til modellari odatda $\\lambda=0{,}1$ bilan va siljishlar hamda normallashtirish vaznlariga so‘nish qo‘llamasdan o‘qitiladi."),
    ]),
    dict(id="training", title="O‘qitishda Adam: qizdirish va jadval", blocks=[
        ("p", "Hatto adaptiv usulga ham tezlik jadvali kerak. Transformerlar uchun eng keng tarqalgan sxema — dastlabki yuzlab yoki minglab qadamlarda noldan $\\eta_{\\max}$ gacha <b>chiziqli qizdirish</b> (warmup), keyin $\\eta_{\\min}$ gacha <b>kosinusli pasaytirish</b>:"),
        ("eq", r"\eta_t=\eta_{\max}\,\frac{t}{T_w}\qquad(t\le T_w)"),
        ("eq", r"\eta_t=\eta_{\min}+\tfrac12(\eta_{\max}-\eta_{\min})\bigl(1+\cos\pi p\bigr),\quad p=\frac{t-T_w}{T-T_w}"),
        ("viz", "adam-schedule", {"warm": 200, "minr": 0.1}, "<b>7-rasm.</b> Shovqinli kvadratik masalada Adam (egriliklari $0{,}01$ dan 1 gacha bo‘lgan 10 parametr, gradiyent shovqini $0{,}05$), $\\eta_{\\max}=0{,}05$, 2000 qadam. Yuqorida — tezlik, pastda — yo‘qotish (logarifmik shkala). O‘zgarmas $\\eta$ bilan yo‘qotish $5{,}6\\cdot10^{-3}$ shovqin darajasida tiqilib qoladi (oxirgi 100 qadam o‘rtachasi); 200 qadamli qizdirish va $0{,}1\\,\\eta_{\\max}$ gacha kosinus bilan — $7{,}1\\cdot10^{-4}$, $7{,}9$ marta past. Bu yerda qizdirish startni biroz kechiktiradi xolos; uning foydasi chuqur tarmoqlarda namoyon bo‘ladi."),
        ("p", "Nega pasaytirish yordam beradi: xossalar bo‘limidan ma’lumki, minimum yonida Adam qadami signal/shovqin nisbatiga ko‘paytirilgan $\\eta$ ga proporsional. $\\eta$ qanchalik kichik bo‘lsa, vaznlar minimum atrofida titraydigan bulut shunchalik kichik."),
        ("p", "Nega qizdirish kerak: dastlabki qadamlarda $\\hat v_t$ bir nechta gradiyent bo‘yicha baholangan va kuchli shovqinli, vaznlar esa endigina initsializatsiya qilingan va gradiyentlar ayniqsa katta. Lyu va hammualliflar (RAdam, 2019) o‘qitish boshida $\\eta/\\sqrt{\\hat v_t}$ samarali tezlik dispersiyasi katta ekanini ko‘rsatishdi va uni analitik to‘g‘rilashni taklif qilishdi; qizdirish o‘sha muammoni soddaroq hal qiladi."),
        ("callout", "note", "Til modellari uchun odatiy retsept", "$\\beta_1=0{,}9$, $\\beta_2=0{,}95$, $\\lambda=0{,}1$ li AdamW, gradiyentni 1 norma bo‘yicha kesish, ~2000 qadam qizdirish va $\\eta_{\\max}$ ning 10% igacha kosinus — masalan, LLaMA o‘qitilishi shunday tasvirlangan. Kichikroq $\\beta_2$ (1000 o‘rniga 20 qadamlik oyna) gradiyent sakrashlariga tezroq javob beradi va katta modellarni o‘qitishni barqarorroq qiladi."),
    ]),
    dict(id="code", title="Kodda: noldan va PyTorch’da", blocks=[
        ("p", "Noldan amalga oshirish — yigirma qator. <code>decoupled</code> bayrog‘i vaznlar so‘nishini AdamW va gradiyent ichidagi $L_2$ orasida almashtiradi."),
        ("code", "python", "CODE_NUMPY"),
        ("p", "Natija «Formula mayda detallarigacha» bo‘limidagi jadval bilan mos keladi, <code>torch.optim.Adam</code> esa o‘sha birinchi qadamda vaznni aynan $\\eta$ ga siljitadi. AdamW, alohida so‘nish guruhlari, qizdirish va kosinus bilan odatiy o‘qitish sikli:"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "warn", "Xotira", "Adam $m$ va $v$ ni saqlaydi — har bir parametrga ikkita son. 7 mlrd parametrli model uchun bu faqat optimizator holati uchun float32 da $2\\cdot7\\cdot10^9\\cdot4$ bayt $=56$ GB. 8-bitli optimizatorlar, holatni sharding qilish (ZeRO) va Adafactor kabi tejamkor variantlar shundan kelib chiqqan."),
    ]),
    dict(id="practice", title="Giperparametrlar va amaliyot", blocks=[
        ("table", ["Parametr", "Standart", "Odatiy diapazon va ma’nosi"], [
            ["$\\eta$", "$10^{-3}$", "$10^{-4}$–$3\\cdot10^{-3}$; transformerlar — taxminan $3\\cdot10^{-4}$ va model o‘sishi bilan kamroq; qo‘shimcha o‘qitish — $10^{-5}$–$5\\cdot10^{-5}$"],
            ["$\\beta_1$", "$0{,}9$", "deyarli hech qachon o‘zgartirilmaydi; yo‘nalish oynasi 10 qadam"],
            ["$\\beta_2$", "$0{,}999$", "katta transformerlar uchun $0{,}95$–$0{,}98$: sakrashlarga tezroq javob beradi"],
            ["$\\epsilon$", "$10^{-8}$", "past aniqlikda yoki beqarorlikda kattaroq ($10^{-6}$ va undan yuqori); juda katta $\\epsilon$ Adam’ni inersiyali SGD’ga aylantiradi"],
            ["$\\lambda$ (AdamW)", "$0{,}01$", "$0{,}01$–$0{,}1$; siljishlar va normallashtirishlarga qo‘llanmaydi"],
            ["qizdirish", "—", "yuzlab qadamdan bir necha ming qadamgacha, o‘qitishning 1–5% i"],
        ], {}),
        ("ul", [
            "<b>Standart qiymatlardan boshlang.</b> $\\eta=10^{-3}$ (transformerlar uchun $3\\cdot10^{-4}$), $\\beta=(0{,}9;\\,0{,}999)$, $\\lambda=0{,}01$ li AdamW. Avval $\\eta$, keyin $\\lambda$ va jadvalni tanlash kerak.",
            "Norma bo‘yicha ($1{,}0$) <b>gradiyentni kesish</b> deyarli tekin va kamdan-kam chetga chiqishlardan qutqaradi.",
            "Vaznlar bilan birga <b>optimizator holatini saqlang</b> (<code>opt.state_dict()</code>): nol $m$ va $v$ bilan o‘qitishni davom ettirganda dastlabki qadamlar yana «sovuq» bo‘ladi.",
            "<b>SGD qachon yaxshiroq.</b> Kompyuter ko‘rishi masalalarida yaxshi sozlangan inersiyali SGD ko‘pincha yaxshiroq umumlashtiradi (Uilson va boshq., 2017). Transformerlar, embeddingli tavsiya tizimlari va siyrak gradiyentli masalalarda Adam yutadi.",
        ]),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b><code>AdamW</code> o‘rniga <code>Adam(weight_decay=…)</code>.</b> Bu gradiyent ichidagi $L_2$: so‘nish $\\sqrt{\\hat v_t}$ ga bo‘linadi va notekis ishlaydi (6-rasm).",
            "<b>SGD’dan olingan tezlik.</b> $\\eta=0{,}1$ inersiyali SGD uchun yaxshi, lekin Adam uchun bu har qadamda vazn birliklarida taxminan $0{,}1$ qadam — o‘qitish deyarli albatta uzoqlashadi.",
            "<b>Barcha parametrlarga so‘nish.</b> Siljishlar va LayerNorm/BatchNorm vaznlari odatda weight decay’dan chiqariladi: ularni nolga qisish regulyarizatsiya qilmaydi, zarar keltiradi.",
            "<b>Noto‘g‘ri $\\epsilon$.</b> Juda kichigi float16 da nolgacha yaxlitlanadi, juda kattasi ($\\gtrsim\\sqrt{\\hat v}$) moslashuvni jimgina o‘chiradi — qadam $(\\eta/\\epsilon)\\hat m$ ga aylanadi.",
            "<b>Transformerda qizdirishsiz.</b> Shovqinli $\\hat v_t$ bahosi bilan birinchi qadamlardanoq katta $\\eta$ ko‘pincha o‘qitish boshida yo‘qotish portlashiga olib keladi.",
            "<b>Jadval noto‘g‘ri qadamda.</b> Jadval qadamlar uchun mo‘ljallangan joyda <code>scheduler.step()</code> ni davrda bir marta chaqirish (yoki aksincha) qizdirishni yuzlab marta cho‘zadi.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘liqlik", blocks=[
        ("ul", [
            "<a href=\"../sgd/\">SGD, Momentum va RMSProp</a>: Adam surati — EMA-inersiya, maxraji — RMSProp’dan $\\sqrt v$; o‘sha yerda barqarorlik sharti va shartlanganlik soni.",
            "<a href=\"../cross-entropy/\">Kross-entropiya</a> va <a href=\"../softmax/\">softmax</a>: til modellarida AdamW minimallashtiradigan yo‘qotish; uning logitlar bo‘yicha $s-y$ gradiyenti oxirgi qatlamning $g_t$ sidir.",
            "<a href=\"../mse/\">MSE</a> va <a href=\"../huber/\">Huber</a>: maqsad o‘zgaruvchi masshtabi gradiyent masshtabini belgilaydi — Adam unga befarq, SGD esa yo‘q.",
            "<a href=\"../gelu/\">GELU</a> va <a href=\"../silu/\">SiLU</a>: AdamW bilan o‘qitiladigan transformerlar aktivatsiyalari.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) Adam ikkita eksponensial o‘rtachani saqlaydi: gradiyentning $m_t$ si (yo‘nalish, ~10 qadamlik oyna) va uning kvadratining $v_t$ si (masshtab, ~1000 qadamlik oyna). 2) Ikkalasi noldan boshlanadi va $1-\\beta^t$ marta kam baholangan; tuzatish ularni siljimagan qiladi, usiz dastlabki qadamlar oshib ketadi — birinchi qadamda $3{,}16$ marta. 3) $\\eta\\,\\hat m_t/(\\sqrt{\\hat v_t}+\\epsilon)$ qadam gradiyent masshtabiga bog‘liq emas, toza signalda $\\eta$ tartibida va shovqinda signal/shovqin nisbatiga proporsional. 4) AdamW vaznlar so‘nishini gradiyentdan ajratadi — barcha vaznlar bir tekis so‘nadi. 5) Amaliyotda: AdamW, qizdirish, kosinus, gradiyentni kesish; $\\eta$ — asosiy giperparametr."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="Siljishni tuzatishli Adam’ning birinchi qadami, $g_1=-3$. Vazn qanday o‘zgaradi?", options=["$3\\eta$ ga kamayadi", "$\\eta$ ga oshadi", "$\\eta$ ga kamayadi", "$3\\eta$ ga oshadi"], answer=1,
                 explain="$\\hat m_1=g_1=-3$, $\\sqrt{\\hat v_1}=|g_1|=3$, qadam $-\\eta\\cdot(-3)/3=+\\eta$: $|g_1|$ qanday bo‘lmasin, vazn $\\eta$ ga o‘sadi."),
            dict(q="$\\beta_2=0{,}999$ da $v_t$ taxminan nechta oxirgi qadamni «eslaydi»?", options=["10", "100", "1000", "10 000"], answer=2,
                 explain="Samarali oyna $1/(1-\\beta_2)=1000$ qadam."),
            dict(q="Modelning barcha gradiyentlari 100 ga ko‘paytirildi (masalan, yo‘qotish 100 ga ko‘paytirildi). Adam qadamlari nima bo‘ladi?", options=["100 marta o‘sadi", "10 marta o‘sadi", "Deyarli o‘zgarmaydi", "100 marta kamayadi"], answer=2,
                 explain="$\\hat m$ va $\\sqrt{\\hat v}$ 100 marta o‘sadi, ularning nisbati o‘zgarmaydi ($\\epsilon$ juda kichik ekan)."),
            dict(q="AdamW $L_2$-regulyarizatsiyali Adam’dan nimasi bilan farq qiladi?", options=["Hech narsasi bilan, ular sinonim", "Vaznlar so‘nishi $m$ va $v$ orqali o‘tmaydi va $\\sqrt{\\hat v}$ ga bo‘linmaydi", "AdamW siljishni tuzatishdan foydalanmaydi", "AdamW gradiyent ishorasidan foydalanadi"], answer=1,
                 explain="AdamW’da vaznlar adaptiv qadamdan alohida $1-\\eta\\lambda$ ga ko‘paytiriladi, shuning uchun so‘nish barcha vaznlar uchun bir xil."),
            dict(q="$\\beta_1=0{,}9$, $\\beta_2=0{,}999$ da siljishni tuzatishsiz Adam’ning birinchi qadami necha marta oshib ketgan?", options=["$0{,}1$ marta (10 marta kam)", "Oshmagan", "$3{,}16$ marta", "1000 marta"], answer=2,
                 explain="$m_1/\\sqrt{v_1}=(1-\\beta_1)g/(\\sqrt{1-\\beta_2}\\,|g|)=0{,}1/0{,}0316\\approx3{,}16$."),
        ]),
    ]),
],
}

# Fill in the shared pieces (table rows and code listings) per language.
for _lang, _secs in SECTIONS.items():
    for _sec in _secs:
        for _i, _b in enumerate(_sec["blocks"]):
            if _b[0] == "table" and _b[2] == "STEPS":
                _sec["blocks"][_i] = (_b[0], _b[1], _steps(_lang), _b[3])
            elif _b[0] == "code" and _b[2] in ("CODE_NUMPY", "CODE_TORCH"):
                _sec["blocks"][_i] = (_b[0], _b[1], _code(CODE_NUMPY if _b[2] == "CODE_NUMPY" else CODE_TORCH, _lang))
