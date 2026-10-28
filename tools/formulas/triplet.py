"""Formula page: Triplet Loss (metric learning). Format: see README.md."""

META = dict(
    id="triplet",
    date="2026-10-28",
    minutes=35,
    hero=r"L(a,p,n)=\max\bigl(0,\;d(a,p)-d(a,n)+m\bigr)",
    title={"ru": "Triplet Loss: свой ближе чужого", "en": "Triplet Loss: the positive closer than the negative", "uz": "Triplet Loss: o‘ziniki begonadan yaqinroq"},
    dek={
        "ru": "Функция потерь, которая учит не классы, а расстояния: якорь должен быть ближе к «своему», чем к «чужому», хотя бы на зазор m. Разбираем по косточкам формулу, три режима троек, градиенты, майнинг batch-hard, нормализацию на сфере и то, как на этой математике держатся FaceNet и повторная идентификация людей (Re-ID).",
        "en": "A loss that learns distances rather than classes: the anchor must be closer to its positive than to the negative by at least a margin m. We take apart the formula, the three regimes of triplets, the gradients, batch-hard mining, normalization on the sphere, and how FaceNet and person re-identification (Re-ID) rest on this mathematics.",
        "uz": "Sinflarni emas, masofalarni o‘rgatadigan yo‘qotish funksiyasi: langar «o‘ziniki»ga «begona»dan kamida m oraliqqa yaqinroq bo‘lishi kerak. Formulani, uchliklarning uch rejimini, gradiyentlarni, batch-hard maynigni, sferada normallashtirishni va FaceNet hamda odamlarni qayta identifikatsiya qilish (Re-ID) shu matematikaga qanday tayanishini mayda detallarigacha ko‘rib chiqamiz.",
    },
    description={
        "ru": "Triplet Loss подробно: формула и зазор, лёгкие, полутрудные и трудные тройки, градиенты и 3D-поверхность потерь, batch-hard и batch-all, обучение эмбеддингов, нормализация, FaceNet и Re-ID, код NumPy и PyTorch.",
        "en": "Triplet Loss in depth: the formula and the margin, easy, semi-hard and hard triplets, gradients and the 3D loss surface, batch-hard and batch-all, embedding training, normalization, FaceNet and Re-ID, NumPy and PyTorch code.",
        "uz": "Triplet Loss batafsil: formula va oraliq, oson, yarim qiyin va qiyin uchliklar, gradiyentlar va 3D yo‘qotish sirti, batch-hard va batch-all, embeddinglarni o‘qitish, normallashtirish, FaceNet va Re-ID, NumPy va PyTorch kodi.",
    },
)

CODE_NUMPY = '''import numpy as np

def pairwise_dist(E, eps=1e-12):
    """Матрица евклидовых расстояний между строками E (n × d)."""
    sq = (E * E).sum(1)
    d2 = sq[:, None] - 2.0 * E @ E.T + sq[None, :]
    return np.sqrt(np.maximum(d2, eps))     # max: защита от −1e-16 и корня из нуля

def batch_hard_triplet(E, labels, margin=0.3):
    D = pairwise_dist(E)
    same = labels[:, None] == labels[None, :]
    hardest_pos = np.where(same, D, 0.0).max(1)       # самый далёкий «свой»
    hardest_neg = np.where(same, np.inf, D).min(1)    # самый близкий «чужой»
    return np.maximum(hardest_pos - hardest_neg + margin, 0.0).mean()

E = np.array([[0.0, 0.0], [0.9, 0.0], [0.6, 0.8]])   # якорь, свой, чужой
labels = np.array([0, 0, 1])
print(batch_hard_triplet(E, labels, margin=0.2))      # ≈ 0.1152 = (0.1 + 0.2456 + 0) / 3'''

CODE_TORCH = '''import torch
import torch.nn as nn
import torch.nn.functional as F

# 1) Тройки собраны заранее: готовая потеря
loss_fn = nn.TripletMarginLoss(margin=0.2, p=2)
a = torch.tensor([[0.0, 0.0]], requires_grad=True)
p = torch.tensor([[0.9, 0.0]], requires_grad=True)
n = torch.tensor([[0.6, 0.8]], requires_grad=True)
loss = loss_fn(a, p, n)            # max(0, 0.9 − 1.0 + 0.2) ≈ 0.1
loss.backward()
print(p.grad, n.grad)              # ≈ [1, 0] и [−0.6, −0.8]: единичные векторы

# 2) Майнинг внутри батча P × K (batch-hard)
def batch_hard(emb, labels, margin=0.3, normalize=True):
    if normalize:
        emb = F.normalize(emb, dim=1)          # точки на единичной сфере
    D = torch.cdist(emb, emb)                  # n × n евклидовых расстояний
    same = labels[:, None] == labels[None, :]
    pos = (D * same).max(1).values             # самый далёкий «свой»
    neg = D.masked_fill(same, float("inf")).min(1).values   # самый близкий «чужой»
    return F.relu(pos - neg + margin).mean()'''


def _code(src, lang):
    if lang == "ru":
        return src
    repl = {
        "en": [("Матрица евклидовых расстояний между строками E (n × d).", "Matrix of Euclidean distances between the rows of E (n × d)."),
               ("max: защита от −1e-16 и корня из нуля", "max: guards against −1e-16 and the root of zero"),
               ("самый далёкий «свой»", "the farthest positive"), ("самый близкий «чужой»", "the closest negative"),
               ("якорь, свой, чужой", "anchor, positive, negative"),
               ("Тройки собраны заранее: готовая потеря", "Triplets prepared in advance: the built-in loss"),
               ("≈ [1, 0] и [−0.6, −0.8]: единичные векторы", "≈ [1, 0] and [−0.6, −0.8]: unit vectors"),
               ("Майнинг внутри батча P × K (batch-hard)", "Mining inside a P × K batch (batch-hard)"),
               ("точки на единичной сфере", "points on the unit sphere"), ("n × n евклидовых расстояний", "n × n Euclidean distances")],
        "uz": [("Матрица евклидовых расстояний между строками E (n × d).", "E (n × d) satrlari orasidagi Evklid masofalari matritsasi."),
               ("max: защита от −1e-16 и корня из нуля", "max: −1e-16 va noldan ildizdan himoya"),
               ("самый далёкий «свой»", "eng uzoq o‘ziniki"), ("самый близкий «чужой»", "eng yaqin begona"),
               ("якорь, свой, чужой", "langar, o‘ziniki, begona"),
               ("Тройки собраны заранее: готовая потеря", "Uchliklar oldindan yig‘ilgan: tayyor yo‘qotish"),
               ("≈ [1, 0] и [−0.6, −0.8]: единичные векторы", "≈ [1, 0] va [−0.6, −0.8]: birlik vektorlar"),
               ("Майнинг внутри батча P × K (batch-hard)", "P × K batch ichida mayning (batch-hard)"),
               ("точки на единичной сфере", "birlik sferadagi nuqtalar"), ("n × n евклидовых расстояний", "n × n Evklid masofalari")],
    }[lang]
    for a, b in repl:
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", "Обычный классификатор знает фиксированный список классов. Но система распознавания лиц должна узнавать людей, которых не было в обучающей выборке, а система повторной идентификации (re-identification, Re-ID) — находить того же человека на записи другой камеры, в другом ракурсе и при другом свете. Переобучать сеть ради каждого нового человека невозможно."),
        ("p", "Выход — учить не классы, а <b>метрику</b> (metric learning). Сеть $f$ превращает изображение в вектор-эмбеддинг (embedding) $f(x)\\in\\mathbb R^d$ так, чтобы снимки одного человека оказывались рядом, а разных — далеко. Тогда «кто это?» сводится к поиску ближайших соседей по расстоянию, и новый человек добавляется одним эмбеддингом в базу."),
        ("p", "Triplet Loss задаёт это требование напрямую. Берём тройку: <b>якорь</b> $a$ (anchor), <b>свой</b> $p$ (positive, тот же человек) и <b>чужой</b> $n$ (negative, другой человек). Требуем, чтобы свой был ближе чужого хотя бы на зазор $m$ (margin)."),
        ("ul", [
            "<b>распознавание лиц</b> — FaceNet (Google, 2015): 128-мерные эмбеддинги, зазор $0{,}2$, точность $99{,}63\\%$ на наборе LFW;",
            "<b>повторная идентификация людей между камерами</b> — batch-hard triplet loss (Херманс и др., 2017) и библиотека torchreid, где он дополняет кросс-энтропию при обучении OSNet;",
            "<b>поиск похожих изображений, товаров, голосов</b> и вообще любой поиск по смыслу, где вопрос звучит «что ближе к этому образцу?».",
        ]),
        ("callout", "key", "Главное за минуту", "$L=\\max\\bigl(0,\\,d(a,p)-d(a,n)+m\\bigr)$. Если чужой дальше своего больше чем на $m$, потеря равна нулю и тройка ничему не учит. Иначе градиент тянет своего к якорю и отталкивает чужого. Почти все случайные тройки лёгкие, поэтому главное искусство — выбирать трудные (майнинг), например самого далёкого своего и самого близкого чужого в батче (batch-hard)."),
    ]),
    dict(id="intuition", title="Интуиция: свой ближе чужого", blocks=[
        ("p", "Нарисуем эмбеддинги на плоскости. Вокруг якоря $a$ проведём окружность через своего $p$ — её радиус $d(a,p)$. Добавим вторую, шире на зазор: радиус $d(a,p)+m$. Требование формулы простое: <b>чужой должен лежать за внешней окружностью</b>. Попал в оранжевое кольцо или внутрь — потеря положительна."),
        ("viz", "triplet-play", {"a": [-0.5, 0], "p": [0.4, 0], "n": [0.1, 0.8], "m": 0.2}, "<b>Рисунок 1.</b> Тяните якорь, своего и чужого. Оранжевые стрелки — направления, в которых градиентный спуск сдвинет каждую точку. В начальном положении $d(a,p)=0{,}9$, $d(a,n)=1{,}0$, $m=0{,}2$: чужой внутри кольца, $L=0{,}9-1{,}0+0{,}2=0{,}1$. Вытащите его за кольцо — стрелки исчезнут."),
        ("callout", "intuition", "Что заметить", "Стрелки у своего и чужого всегда направлены вдоль линий к якорю, а их длины в обычной (не квадратной) метрике одинаковы и равны 1: важна не величина ошибки, а сам факт нарушения. Включите квадраты расстояний — длины стрелок станут пропорциональны расстояниям."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("p", "Запишем потерю полностью — с сетью, расстояниями и усреднением по тройкам:"),
        ("eq", r"\mathcal L=\frac{1}{|T|}\sum_{(a,p,n)\in T}\max\Bigl(0,\;\bigl\|f(x_a)-f(x_p)\bigr\|-\bigl\|f(x_a)-f(x_n)\bigr\|+m\Bigr)"),
        ("symbols", [
            (r"f(x)", "эмбеддинг: выход сети для изображения $x$, вектор из $\\mathbb R^d$ (в FaceNet $d=128$), часто нормированный на единичную длину;"),
            (r"d(a,p)", "расстояние до своего, $\\|f(x_a)-f(x_p)\\|$; его хотим уменьшить;"),
            (r"d(a,n)", "расстояние до чужого, $\\|f(x_a)-f(x_n)\\|$; его хотим увеличить;"),
            (r"m>0", "зазор: чужой должен быть дальше своего не просто, а с запасом $m$;"),
            (r"\max(0,\cdot)", "шарнир (hinge): выполненное требование не штрафуется и не даёт градиента;"),
            (r"T", "множество троек, по которому усредняем, — обычно тройки внутри батча (см. раздел о майнинге)."),
        ]),
        ("p", "Удобно ввести одну переменную — разность расстояний $\\Delta=d(a,p)-d(a,n)$. Тогда $L=\\max(0,\\Delta+m)$: это <a href=\"../relu/\">ReLU</a>, сдвинутая на $m$. Отрицательная $\\Delta$ значит, что свой уже ближе; но пока $\\Delta&gt;-m$, запаса не хватает."),
        ("p", "Примеры при $m=0{,}2$: $d(a,p)=0{,}4$, $d(a,n)=1{,}1$ дают $\\Delta=-0{,}7$ и $L=\\max(0;\\,-0{,}5)=0$ — тройка уже разделена. $d(a,p)=0{,}9$, $d(a,n)=1{,}0$ дают $\\Delta=-0{,}1$ и $L=0{,}1$: свой ближе, но зазора мало."),
        ("viz", "triplet-hinge", {"m": 0.2, "delta": -0.1}, "<b>Рисунок 2.</b> Потеря как функция $\\Delta$ (сверху) и её производная (снизу). Производная — ступенька: 0 для выполненных троек и 1 для нарушенных, без промежуточных значений. Пунктир — «мягкий зазор» (soft margin) $\\ln(1+e^{\\Delta})$ из работы Херманса и др.: он никогда не обнуляется, а его производная — <a href=\"../sigmoid/\">сигмоида</a> $\\sigma(\\Delta)$. При $\\Delta=-0{,}1$: hinge даёт $0{,}1$, мягкий вариант — $0{,}644$."),
        ("callout", "note", "Зазор — относительный", "Triplet Loss не требует, чтобы свои были ближе какого-то фиксированного порога, — только ближе чужих. Поэтому у разных людей кластеры могут иметь разный размер. Порог для ответа «это тот же человек» подбирают потом, на валидации."),
    ]),
    dict(id="regimes", title="Три режима: лёгкие, полутрудные, трудные", blocks=[
        ("p", "Каждая тройка попадает в один из трёх режимов в зависимости от $d(a,p)$ и $d(a,n)$:"),
        ("table", ["Режим", "Условие", "$L$", "Градиент"], [
            ["лёгкая (easy)", "$d(a,n)\\ge d(a,p)+m$", "$0$", "нет"],
            ["полутрудная (semi-hard)", "$d(a,p)&lt;d(a,n)&lt;d(a,p)+m$", "от $0$ до $m$", "есть"],
            ["трудная (hard)", "$d(a,n)\\le d(a,p)$", "не меньше $m$", "есть"],
        ], {}),
        ("p", "На плоскости $(d(a,p),\\,d(a,n))$ границы режимов — две параллельные прямые: $d(a,n)=d(a,p)$ и $d(a,n)=d(a,p)+m$. Потеря — плоскость, наклонённая под углом к этим прямым, обрезанная нулём выше верхней из них."),
        ("viz", "triplet-regimes", {"m": 0.2, "pt": [0.9, 1.0]}, "<b>Рисунок 3.</b> Потеря на плоскости $(d(a,p),\\,d(a,n))$: чем насыщеннее красный, тем она больше. Точки — все 576 троек батча из рисунка 5 (4 человека по 4 снимка). При $m=0{,}2$ из них 510 лёгких, 31 полутрудная и 35 трудных: только 66 троек из 576 дают градиент. Увеличьте зазор — полоса полутрудных расширится."),
        ("callout", "warn", "Почему случайные тройки бесполезны", "Как только сеть немного обучилась, подавляющее большинство случайных троек становится лёгкими: их потеря и градиент равны нулю. Усреднение по ним разбавляет полезный сигнал, и обучение почти останавливается. Отсюда майнинг — целенаправленный выбор трудных и полутрудных троек."),
    ]),
    dict(id="gradients", title="Градиенты: куда тянет каждую точку", blocks=[
        ("p", "Для активной тройки ($L&gt;0$) потеря равна $d(a,p)-d(a,n)+m$, и всё сводится к градиенту расстояния. Для евклидовой нормы $\\nabla_u\\|u-v\\|=\\frac{u-v}{\\|u-v\\|}$ — единичный вектор от $v$ к $u$."),
        ("deep", "Вывод градиентов по трём точкам", [
            ("p", "Обозначим $a,p,n$ эмбеддинги и $d_{ap}=\\|a-p\\|$, $d_{an}=\\|a-n\\|$. Дифференцируем $d_{ap}=\\sqrt{(a-p)^\\top(a-p)}$ по правилу цепочки:"),
            ("eq", r"\nabla_a d_{ap}=\frac{1}{2d_{ap}}\cdot2(a-p)=\frac{a-p}{d_{ap}},\qquad \nabla_p d_{ap}=\frac{p-a}{d_{ap}}"),
            ("p", "Аналогично для $d_{an}$. Подставляем в $L=d_{ap}-d_{an}+m$:"),
            ("eq", r"\nabla_p L=\frac{p-a}{d_{ap}},\qquad \nabla_n L=-\frac{n-a}{d_{an}},\qquad \nabla_a L=\frac{a-p}{d_{ap}}-\frac{a-n}{d_{an}}"),
            ("p", "Сумма трёх градиентов равна нулю: сдвиг всех трёх точек на один вектор не меняет расстояний, значит, и потеря не меняется. Для квадратов расстояний $L=d_{ap}^2-d_{an}^2+m$ получаем $\\nabla_pL=2(p-a)$, $\\nabla_nL=-2(n-a)$ и $\\nabla_aL=2(n-p)$ — у якоря градиент вообще не зависит от его положения."),
        ]),
        ("p", "Шаг градиентного спуска идёт против градиента: свой $p$ сдвигается <b>к якорю</b>, чужой $n$ — <b>от якоря</b>, а якорь — к своему и от чужого. В обычной метрике длины этих сдвигов равны 1 при любых расстояниях; в квадратной — пропорциональны расстояниям."),
        ("p", "Это видно на 3D-поверхности. Закрепим якорь в начале координат и своего на расстоянии $0{,}6$; как зависит потеря от положения чужого $n=(x,y)$? Получается перевёрнутый конус: в центре $L=0{,}6+m$, к краю круга радиуса $0{,}6+m$ — ноль. Склон конуса везде одинаковый, $|\\nabla L|=1$."),
        ("viz", "triplet-surface", {"m": 0.4, "who": "neg"}, "<b>Рисунок 4.</b> Потеря как функция положения чужого (или своего) при закреплённом якоре; поверхность можно вращать. Справа — срез вдоль луча из якоря: сама потеря и норма градиента. При $m=0{,}4$ и обычном расстоянии конус имеет высоту $1{,}0$ и радиус $1{,}0$. Переключитесь на $d^2$: поверхность станет параболоидом высотой $0{,}76$ и радиусом $0{,}872$, а градиент у самого якоря обнулится. Для своего (чужой на расстоянии $1{,}2$) — воронка: потеря растёт за окружностью радиуса $0{,}8$."),
        ("callout", "warn", "Квадрат расстояния и трудные чужие", "С квадратами расстояний сила отталкивания $2\\,d(a,n)$ тем слабее, чем ближе чужой к якорю — то есть именно для самых опасных ошибок. В обычной метрике она постоянна. Поэтому в Re-ID (Херманс и др., 2017) рекомендуют обычное евклидово расстояние; FaceNet использует квадраты, но на нормированных векторах и с полутрудными тройками."),
    ]),
    dict(id="mining", title="Майнинг: какие тройки брать", blocks=[
        ("p", "В наборе из $N$ изображений троек порядка $N^3$ — перебрать их все нельзя, да и почти все лёгкие. Тройки выбирают <b>онлайн</b>, внутри батча. Батч строят по схеме $P\\times K$: $P$ человек, по $K$ снимков каждого. Внутри такого батча"),
        ("eq", r"|T|=\underbrace{PK}_{\text{якорей}}\cdot\underbrace{(K-1)}_{\text{своих}}\cdot\underbrace{(P-1)K}_{\text{чужих}}"),
        ("p", "При $P=4$, $K=4$ это 576 троек, при $P=18$, $K=4$ (батч Херманса и др. для набора Market-1501) — уже 14 688. Основные стратегии:"),
        ("ul", [
            "<b>batch-all</b> — берём все тройки батча и усредняем потерю только по активным ($L&gt;0$), чтобы лёгкие не разбавляли сигнал;",
            "<b>batch-hard</b> — для каждого якоря одна тройка: <i>самый далёкий свой</i> и <i>самый близкий чужой</i>; $PK$ троек, самые информативные;",
            "<b>semi-hard</b> (FaceNet) — для пары $(a,p)$ берут чужого, который дальше своего, но внутри зазора; так обучение мягче на старте.",
        ]),
        ("eq", r"\mathcal L_{\text{BH}}=\frac{1}{PK}\sum_{a}\max\Bigl(0,\;\max_{p:\,y_p=y_a}d(a,p)-\min_{n:\,y_n\ne y_a}d(a,n)+m\Bigr)"),
        ("viz", "triplet-mining", {"anchor": 1, "m": 0.2, "strategy": "hard"}, "<b>Рисунок 5.</b> Батч $P=4$, $K=4$ в пространстве эмбеддингов. Выберите якорь и стратегию. В режиме batch-hard жирные линии ведут к самому далёкому своему и самому близкому чужому, пунктирная окружность — радиус $d_{\\max}(a,p)+m$. При $m=0{,}2$ batch-hard даёт $L=0{,}353$, batch-all — $0{,}306$ по 66 активным тройкам из 576. У первого якоря из 36 троек 34 лёгкие и 2 полутрудные."),
        ("callout", "warn", "Опасность самых трудных", "Самые трудные тройки часто оказываются ошибками разметки или почти неразличимыми снимками. В начале обучения, когда эмбеддинги случайны, погоня за ними может «схлопнуть» модель: все $f(x)$ стягиваются в одну точку, где $L=m$ для любой тройки. Помогают полутрудные тройки на старте, нормировка эмбеддингов, мягкий зазор и комбинация с кросс-энтропией."),
    ]),
    dict(id="training", title="Как это работает в обучении", blocks=[
        ("p", "Соберём всё вместе. Пусть у каждого снимка два признака: $x_1$ — помеха (ракурс, освещение), которая сильно меняется у одного и того же человека, и $x_2$ — признак личности, слегка искривлённый помехой. Во входном пространстве два снимка одного человека могут быть дальше друг от друга, чем снимки разных людей: верно упорядочены только $62{,}7\\%$ троек."),
        ("p", "Маленькая сеть $f:\\mathbb R^2\\to\\mathbb R^2$ (12 нейронов tanh) учится с batch-hard triplet loss при $m=0{,}5$ и оптимизатором <a href=\"../adam/\">Adam</a>. Ей не говорят, где какой человек должен оказаться, — только что свои ближе чужих."),
        ("viz", "triplet-train", {"m": 0.5}, "<b>Рисунок 6.</b> Слева — входы 4 человек по 12 снимков, справа — их эмбеддинги, внизу — потеря. Нажмите «Пуск». В начале $L=1{,}266$, все 48 якорей активны, верно упорядочено $64{,}9\\%$ троек. К шагу 60 упорядочены все $100\\%$, но зазора ещё не хватает 42 якорям; к шагу 300 активных остаётся 4, к шагу 600 потеря равна нулю. Сеть «выпрямила» полосы: помеха $x_1$ больше не влияет на расстояния."),
        ("p", "Так же устроена Re-ID: запрос (query) — снимок человека с одной камеры, галерея (gallery) — снимки со всех остальных. Эмбеддинги галереи сортируют по расстоянию до запроса и смотрят, на каком месте первый верный ответ. Метрики — Rank-1 (верный ответ на первом месте) и mAP (средняя точность по всем верным)."),
        ("callout", "history", "Откуда это пошло", "Идея зазора между своими и чужими — из метода ближайших соседей с большим зазором (LMNN, Вайнбергер и Сол, 2005). Пары своих и чужих с зазором ввели в контрастной потере (Хадселл, Чопра и Лекун, 2006). Шрофф, Калениченко и Филбин сделали тройки основой FaceNet (2015), а Херманс, Байер и Лейбе в работе «In Defense of the Triplet Loss for Person Re-Identification» (2017) показали, что с batch-hard майнингом тройки хорошо работают и в Re-ID."),
    ]),
    dict(id="sphere", title="Нормализация на сфере и выбор зазора", blocks=[
        ("p", "Без ограничений сеть может увеличивать все расстояния, просто растягивая пространство: в обычной метрике зазор $m$ теряет смысл, если масштаб не фиксирован. Поэтому эмбеддинги часто нормируют: $\\hat f=f/\\|f\\|$, все точки лежат на единичной сфере. Для единичных векторов"),
        ("eq", r"\|u-v\|^{2}=\|u\|^2+\|v\|^2-2\,u^\top v=2-2\cos\theta"),
        ("p", "где $\\theta$ — угол между векторами. Квадрат расстояния меняется от 0 (совпадают) до 4 (противоположны), и зазор $m=0{,}2$ в FaceNet — это $5\\%$ всего диапазона. Требование $d^2(a,n)\\ge d^2(a,p)+m$ превращается в требование к углам: $\\cos\\theta_{an}\\le\\cos\\theta_{ap}-m/2$."),
        ("viz", "triplet-sphere", {"a": 0, "p": 40, "n": -45, "m": 0.2}, "<b>Рисунок 7.</b> Нормированные эмбеддинги на единичной окружности (тяните точки по ней) и квадрат расстояния как функция угла. Оранжевая дуга — зона, где чужой нарушал бы зазор. При $\\theta_{ap}=40^\\circ$ и $m=0{,}2$ чужой должен быть не ближе $48{,}2^\\circ$ от якоря; в начальном положении он на $45^\\circ$: $d^2(a,p)=0{,}468$, $d^2(a,n)=0{,}586$, $L=0{,}082$."),
        ("callout", "note", "Как выбрать зазор", "Зазор измеряется в единицах расстояния, поэтому зависит от нормировки и от того, квадрат расстояния или нет. Для нормированных эмбеддингов типичны $0{,}2$ (FaceNet, $d^2$) и $0{,}3$ (torchreid, $d$). Слишком маленький зазор почти не требует разделения, слишком большой может быть недостижим и держит все тройки активными."),
    ]),
    dict(id="code", title="В коде: батч-майнинг и устойчивость", blocks=[
        ("p", "Ключ к эффективности — матрица всех попарных расстояний батча, из которой майнинг берётся масками без циклов. Численная тонкость: $\\|u-v\\|$ не дифференцируема при $u=v$ (производная корня в нуле бесконечна), а через формулу $\\|u\\|^2-2u^\\top v+\\|v\\|^2$ из-за округления может получиться крошечное отрицательное число. Поэтому под корень ставят $\\max(\\cdot,\\varepsilon)$, а <code>nn.TripletMarginLoss</code> добавляет $\\varepsilon=10^{-6}$ к разности векторов."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Практика", "Батч $P\\times K$ (например, $P=16$, $K=4$) нужен обязательно: без нескольких снимков одного человека в батче не будет своих. Triplet loss обычно комбинируют с кросс-энтропией по личностям — так обучение быстрее и устойчивее."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            "<b>Случайные батчи вместо $P\\times K$.</b> В случайном батче у многих якорей нет ни одного своего, и тройки не собираются.",
            "<b>Обучение только на случайных тройках.</b> Почти все они лёгкие, градиент нулевой, и потеря «застывает» на маленьком значении, хотя модель плохая.",
            "<b>Самые трудные тройки с первого шага</b> без нормировки и разогрева — риск схлопывания всех эмбеддингов в точку.",
            "<b>Зазор без учёта масштаба.</b> Без нормировки сеть растягивает пространство; на сфере $m$ нужно соотносить с максимумом расстояния (2 для $d$, 4 для $d^2$).",
            "<b>Корень из нуля.</b> Расстояние точки до самой себя на диагонали матрицы даёт NaN в градиенте, если не добавить $\\varepsilon$ или не маскировать диагональ.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("p", "Ближайший родственник — <b>контрастная потеря</b> (contrastive loss): она работает с парами и абсолютными порогами, а не с относительным сравнением. Для пары с меткой $y=1$ (свои) и $y=0$ (чужие):"),
        ("eq", r"L_{\text{contr}}=y\,d^{2}+(1-y)\,\max(0,\;m-d)^{2}"),
        ("ul", [
            "<a href=\"../relu/\">ReLU</a>: шарнир $\\max(0,\\Delta+m)$ — это ReLU от сдвинутой разности расстояний; его производная — ступенька.",
            "<a href=\"../sigmoid/\">Сигмоида</a>: производная мягкого зазора $\\ln(1+e^\\Delta)$ равна $\\sigma(\\Delta)$.",
            "<a href=\"../softmax/\">Softmax</a> и <a href=\"../cross-entropy/\">кросс-энтропия</a>: N-pair loss и InfoNCE обобщают тройку на одного своего против многих чужих через softmax по сходствам; ArcFace переносит зазор в угол внутри softmax.",
            "<a href=\"../mse/\">MSE</a>: квадрат евклидова расстояния — та же сумма квадратов разностей.",
            "<a href=\"../focal/\">Focal Loss</a>: та же идея «учиться на трудных», только через вес примера, а не через выбор троек.",
            "<a href=\"../adam/\">Adam</a>: оптимизатор симуляции на рисунке 6.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, "1) $L=\\max(0,\\,d(a,p)-d(a,n)+m)$: свой должен быть ближе чужого с запасом $m$; это ReLU от $\\Delta+m$. 2) Режимы: лёгкие ($L=0$, нет градиента), полутрудные ($0&lt;L&lt;m$), трудные ($L\\ge m$). 3) Градиенты — единичные векторы вдоль линий к якорю (для $d^2$ — пропорциональные расстояниям), их сумма равна нулю. 4) Тройки выбирают в батче $P\\times K$: batch-all, batch-hard, semi-hard. 5) Нормировка на сфере даёт $d^2=2-2\\cos\\theta$ и осмысленный зазор. 6) На этом держатся FaceNet и Re-ID: эмбеддинг плюс поиск ближайших соседей."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q="$m=0{,}2$, $d(a,p)=0{,}9$, $d(a,n)=1{,}0$. Чему равна потеря?", options=["$0$", "$0{,}1$", "$0{,}2$", "$0{,}3$"], answer=1,
                 explain="$\\max(0;\\,0{,}9-1{,}0+0{,}2)=0{,}1$: свой ближе, но запас $0{,}1$ меньше зазора $0{,}2$."),
            dict(q="Тройка с $d(a,p)=0{,}5$, $d(a,n)=0{,}4$ при $m=0{,}2$ — это…", options=["лёгкая", "полутрудная", "трудная", "невозможная"], answer=2,
                 explain="Чужой ближе своего: $d(a,n)\\le d(a,p)$, это трудная тройка; $L=0{,}3\\ge m$."),
            dict(q="Куда направлен шаг градиентного спуска для чужого $n$ в активной тройке (обычная метрика)?", options=["К якорю, длина $d(a,n)$", "От якоря, единичной длины", "К своему $p$", "Шага нет"], answer=1,
                 explain="$\\nabla_nL=-(n-a)/d(a,n)$, шаг идёт против градиента: $+(n-a)/d(a,n)$ — единичный вектор от якоря."),
            dict(q="Что выбирает batch-hard для каждого якоря?", options=["Случайного своего и случайного чужого", "Самого близкого своего и самого далёкого чужого", "Самого далёкого своего и самого близкого чужого", "Все тройки с $L&gt;0$"], answer=2,
                 explain="Худший случай для якоря: $\\max d(a,p)$ и $\\min d(a,n)$ — самая информативная тройка."),
            dict(q="Для единичных векторов под углом $90^\\circ$ квадрат расстояния равен…", options=["$0$", "$1$", "$2$", "$4$"], answer=2,
                 explain="$d^2=2-2\\cos90^\\circ=2$."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", "An ordinary classifier knows a fixed list of classes. But a face recognition system must recognize people who were not in the training set, and a re-identification (Re-ID) system must find the same person in another camera’s footage, from another angle and under different light. Retraining the network for every new person is impossible."),
        ("p", "The way out is to learn not classes but a <b>metric</b> (metric learning). The network $f$ turns an image into an embedding vector $f(x)\\in\\mathbb R^d$ so that pictures of the same person end up close together and pictures of different people far apart. Then “who is this?” becomes a nearest-neighbour search by distance, and a new person is added as a single embedding in the database."),
        ("p", "Triplet Loss states this requirement directly. Take a triplet: an <b>anchor</b> $a$, a <b>positive</b> $p$ (the same person) and a <b>negative</b> $n$ (a different person). Require the positive to be closer than the negative by at least a margin $m$."),
        ("ul", [
            "<b>face recognition</b> — FaceNet (Google, 2015): 128-dimensional embeddings, margin $0.2$, accuracy $99.63\\%$ on the LFW benchmark;",
            "<b>re-identifying people across cameras</b> — the batch-hard triplet loss (Hermans et al., 2017) and the torchreid library, where it complements cross-entropy when training OSNet;",
            "<b>searching for similar images, products, voices</b> and any search by meaning where the question is “what is closest to this sample?”.",
        ]),
        ("callout", "key", "The essentials in a minute", "$L=\\max\\bigl(0,\\,d(a,p)-d(a,n)+m\\bigr)$. If the negative is farther than the positive by more than $m$, the loss is zero and the triplet teaches nothing. Otherwise the gradient pulls the positive towards the anchor and pushes the negative away. Almost all random triplets are easy, so the main skill is choosing hard ones (mining), for example the farthest positive and the closest negative in the batch (batch-hard)."),
    ]),
    dict(id="intuition", title="Intuition: the positive closer than the negative", blocks=[
        ("p", "Draw the embeddings on a plane. Around the anchor $a$ draw a circle through the positive $p$ — its radius is $d(a,p)$. Add a second one, wider by the margin: radius $d(a,p)+m$. The formula’s requirement is simple: <b>the negative must lie outside the outer circle</b>. If it falls into the orange ring or inside it, the loss is positive."),
        ("viz", "triplet-play", {"a": [-0.5, 0], "p": [0.4, 0], "n": [0.1, 0.8], "m": 0.2}, "<b>Figure 1.</b> Drag the anchor, the positive and the negative. The orange arrows show where gradient descent will move each point. In the starting position $d(a,p)=0.9$, $d(a,n)=1.0$, $m=0.2$: the negative is inside the ring, $L=0.9-1.0+0.2=0.1$. Pull it out of the ring and the arrows disappear."),
        ("callout", "intuition", "What to notice", "The arrows at the positive and the negative always point along the lines to the anchor, and in the ordinary (non-squared) metric their lengths are equal to 1: what matters is not the size of the violation but the fact of it. Turn on squared distances and the arrow lengths become proportional to the distances."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("p", "Let us write the loss in full — with the network, the distances and the average over triplets:"),
        ("eq", r"\mathcal L=\frac{1}{|T|}\sum_{(a,p,n)\in T}\max\Bigl(0,\;\bigl\|f(x_a)-f(x_p)\bigr\|-\bigl\|f(x_a)-f(x_n)\bigr\|+m\Bigr)"),
        ("symbols", [
            (r"f(x)", "the embedding: the network output for an image $x$, a vector in $\\mathbb R^d$ ($d=128$ in FaceNet), often normalized to unit length;"),
            (r"d(a,p)", "the distance to the positive, $\\|f(x_a)-f(x_p)\\|$; we want to decrease it;"),
            (r"d(a,n)", "the distance to the negative, $\\|f(x_a)-f(x_n)\\|$; we want to increase it;"),
            (r"m>0", "the margin: the negative must be farther than the positive not just barely, but with a reserve $m$;"),
            (r"\max(0,\cdot)", "the hinge: a satisfied requirement is not penalized and gives no gradient;"),
            (r"T", "the set of triplets we average over — usually triplets inside a batch (see the section on mining)."),
        ]),
        ("p", "It is convenient to introduce a single variable — the difference of distances $\\Delta=d(a,p)-d(a,n)$. Then $L=\\max(0,\\Delta+m)$: a <a href=\"../relu/\">ReLU</a> shifted by $m$. A negative $\\Delta$ means the positive is already closer; but as long as $\\Delta&gt;-m$, the reserve is not enough."),
        ("p", "Examples with $m=0.2$: $d(a,p)=0.4$, $d(a,n)=1.1$ give $\\Delta=-0.7$ and $L=\\max(0,\\,-0.5)=0$ — the triplet is already separated. $d(a,p)=0.9$, $d(a,n)=1.0$ give $\\Delta=-0.1$ and $L=0.1$: the positive is closer, but the margin is too small."),
        ("viz", "triplet-hinge", {"m": 0.2, "delta": -0.1}, "<b>Figure 2.</b> The loss as a function of $\\Delta$ (top) and its derivative (bottom). The derivative is a step: 0 for satisfied triplets and 1 for violated ones, with nothing in between. The dashed line is the soft margin $\\ln(1+e^{\\Delta})$ from Hermans et al.: it never becomes zero, and its derivative is the <a href=\"../sigmoid/\">sigmoid</a> $\\sigma(\\Delta)$. At $\\Delta=-0.1$ the hinge gives $0.1$, the soft version $0.644$."),
        ("callout", "note", "The margin is relative", "Triplet Loss does not require positives to be closer than some fixed threshold — only closer than the negatives. So clusters of different people may have different sizes. The threshold for answering “this is the same person” is tuned later, on validation data."),
    ]),
    dict(id="regimes", title="Three regimes: easy, semi-hard, hard", blocks=[
        ("p", "Every triplet falls into one of three regimes depending on $d(a,p)$ and $d(a,n)$:"),
        ("table", ["Regime", "Condition", "$L$", "Gradient"], [
            ["easy", "$d(a,n)\\ge d(a,p)+m$", "$0$", "none"],
            ["semi-hard", "$d(a,p)&lt;d(a,n)&lt;d(a,p)+m$", "from $0$ to $m$", "yes"],
            ["hard", "$d(a,n)\\le d(a,p)$", "at least $m$", "yes"],
        ], {}),
        ("p", "In the $(d(a,p),\\,d(a,n))$ plane the regime boundaries are two parallel lines: $d(a,n)=d(a,p)$ and $d(a,n)=d(a,p)+m$. The loss is a tilted plane cut off at zero above the upper of them."),
        ("viz", "triplet-regimes", {"m": 0.2, "pt": [0.9, 1.0]}, "<b>Figure 3.</b> The loss on the $(d(a,p),\\,d(a,n))$ plane: the deeper the red, the larger it is. The dots are all 576 triplets of the batch from Figure 5 (4 people with 4 pictures each). At $m=0.2$, 510 of them are easy, 31 semi-hard and 35 hard: only 66 triplets out of 576 give a gradient. Increase the margin and the semi-hard band widens."),
        ("callout", "warn", "Why random triplets are useless", "As soon as the network has learned a little, the vast majority of random triplets become easy: their loss and gradient are zero. Averaging over them dilutes the useful signal, and training almost stalls. Hence mining — deliberately choosing hard and semi-hard triplets."),
    ]),
    dict(id="gradients", title="Gradients: where each point is pulled", blocks=[
        ("p", "For an active triplet ($L&gt;0$) the loss equals $d(a,p)-d(a,n)+m$, and everything reduces to the gradient of a distance. For the Euclidean norm $\\nabla_u\\|u-v\\|=\\frac{u-v}{\\|u-v\\|}$ — the unit vector from $v$ to $u$."),
        ("deep", "Deriving the gradients for the three points", [
            ("p", "Denote the embeddings $a,p,n$ and $d_{ap}=\\|a-p\\|$, $d_{an}=\\|a-n\\|$. Differentiate $d_{ap}=\\sqrt{(a-p)^\\top(a-p)}$ by the chain rule:"),
            ("eq", r"\nabla_a d_{ap}=\frac{1}{2d_{ap}}\cdot2(a-p)=\frac{a-p}{d_{ap}},\qquad \nabla_p d_{ap}=\frac{p-a}{d_{ap}}"),
            ("p", "The same holds for $d_{an}$. Substitute into $L=d_{ap}-d_{an}+m$:"),
            ("eq", r"\nabla_p L=\frac{p-a}{d_{ap}},\qquad \nabla_n L=-\frac{n-a}{d_{an}},\qquad \nabla_a L=\frac{a-p}{d_{ap}}-\frac{a-n}{d_{an}}"),
            ("p", "The three gradients add up to zero: shifting all three points by the same vector does not change the distances, so the loss does not change either. For squared distances $L=d_{ap}^2-d_{an}^2+m$ we get $\\nabla_pL=2(p-a)$, $\\nabla_nL=-2(n-a)$ and $\\nabla_aL=2(n-p)$ — the anchor’s gradient does not even depend on its position."),
        ]),
        ("p", "A gradient-descent step goes against the gradient: the positive $p$ moves <b>towards the anchor</b>, the negative $n$ <b>away from the anchor</b>, and the anchor moves towards the positive and away from the negative. In the ordinary metric the lengths of these moves equal 1 at any distance; in the squared one they are proportional to the distances."),
        ("p", "This is visible on a 3D surface. Fix the anchor at the origin and the positive at distance $0.6$; how does the loss depend on the position of the negative $n=(x,y)$? We get an upside-down cone: $L=0.6+m$ in the centre, falling to zero at the edge of a disc of radius $0.6+m$. The slope of the cone is the same everywhere, $|\\nabla L|=1$."),
        ("viz", "triplet-surface", {"m": 0.4, "who": "neg"}, "<b>Figure 4.</b> The loss as a function of the position of the negative (or the positive) with the anchor fixed; the surface can be rotated. On the right, a slice along a ray from the anchor: the loss itself and the gradient norm. At $m=0.4$ and the ordinary distance the cone has height $1.0$ and radius $1.0$. Switch to $d^2$: the surface becomes a paraboloid of height $0.76$ and radius $0.872$, and the gradient vanishes right at the anchor. For the positive (with the negative at distance $1.2$) it is a funnel: the loss grows outside the circle of radius $0.8$."),
        ("callout", "warn", "Squared distance and hard negatives", "With squared distances the repelling force $2\\,d(a,n)$ is the weaker the closer the negative is to the anchor — that is, exactly for the most dangerous mistakes. In the ordinary metric it is constant. That is why in Re-ID (Hermans et al., 2017) the plain Euclidean distance is recommended; FaceNet uses squares, but on normalized vectors and with semi-hard triplets."),
    ]),
    dict(id="mining", title="Mining: which triplets to take", blocks=[
        ("p", "A set of $N$ images contains on the order of $N^3$ triplets — they cannot all be enumerated, and almost all of them are easy anyway. Triplets are chosen <b>online</b>, inside a batch. The batch is built as $P\\times K$: $P$ people with $K$ pictures each. Inside such a batch"),
        ("eq", r"|T|=\underbrace{PK}_{\text{anchors}}\cdot\underbrace{(K-1)}_{\text{positives}}\cdot\underbrace{(P-1)K}_{\text{negatives}}"),
        ("p", "With $P=4$, $K=4$ this is 576 triplets; with $P=18$, $K=4$ (the batch of Hermans et al. for the Market-1501 dataset) it is already 14,688. The main strategies:"),
        ("ul", [
            "<b>batch-all</b> — take all triplets of the batch and average the loss over the active ones ($L&gt;0$) only, so that the easy ones do not dilute the signal;",
            "<b>batch-hard</b> — one triplet per anchor: <i>the farthest positive</i> and <i>the closest negative</i>; $PK$ triplets, the most informative ones;",
            "<b>semi-hard</b> (FaceNet) — for a pair $(a,p)$ take a negative that is farther than the positive but inside the margin; this makes training gentler at the start.",
        ]),
        ("eq", r"\mathcal L_{\text{BH}}=\frac{1}{PK}\sum_{a}\max\Bigl(0,\;\max_{p:\,y_p=y_a}d(a,p)-\min_{n:\,y_n\ne y_a}d(a,n)+m\Bigr)"),
        ("viz", "triplet-mining", {"anchor": 1, "m": 0.2, "strategy": "hard"}, "<b>Figure 5.</b> A batch with $P=4$, $K=4$ in the embedding space. Choose an anchor and a strategy. In batch-hard mode the thick lines lead to the farthest positive and the closest negative, the dashed circle has radius $d_{\\max}(a,p)+m$. At $m=0.2$ batch-hard gives $L=0.353$, batch-all $0.306$ over 66 active triplets out of 576. For the first anchor 34 of its 36 triplets are easy and 2 are semi-hard."),
        ("callout", "warn", "The danger of the hardest ones", "The very hardest triplets are often labelling errors or nearly indistinguishable pictures. Early in training, when the embeddings are random, chasing them can “collapse” the model: all $f(x)$ shrink to one point where $L=m$ for every triplet. Semi-hard triplets at the start, normalized embeddings, a soft margin and combining with cross-entropy all help."),
    ]),
    dict(id="training", title="How it works in training", blocks=[
        ("p", "Let us put everything together. Suppose every picture has two features: $x_1$ is a nuisance (pose, lighting) that varies a lot for the same person, and $x_2$ is an identity feature slightly bent by the nuisance. In the input space two pictures of the same person can be farther apart than pictures of different people: only $62.7\\%$ of the triplets are correctly ordered."),
        ("p", "A small network $f:\\mathbb R^2\\to\\mathbb R^2$ (12 tanh neurons) is trained with the batch-hard triplet loss at $m=0.5$ and the <a href=\"../adam/\">Adam</a> optimizer. It is not told where each person should end up — only that positives must be closer than negatives."),
        ("viz", "triplet-train", {"m": 0.5}, "<b>Figure 6.</b> Left: the inputs of 4 people with 12 pictures each; right: their embeddings; bottom: the loss. Press “Play”. At the start $L=1.266$, all 48 anchors are active, $64.9\\%$ of the triplets are correctly ordered. By step 60 all $100\\%$ are ordered, but 42 anchors still lack the margin; by step 300 only 4 are active, and by step 600 the loss is zero. The network has “straightened” the bands: the nuisance $x_1$ no longer affects the distances."),
        ("p", "Re-ID works the same way: the query is a picture of a person from one camera, the gallery holds pictures from all the others. The gallery embeddings are sorted by distance to the query, and one looks at the position of the first correct match. The metrics are Rank-1 (the correct match comes first) and mAP (mean average precision over all correct matches)."),
        ("callout", "history", "Where it came from", "The idea of a margin between positives and negatives comes from large margin nearest neighbour (LMNN, Weinberger and Saul, 2005). Pairs of positives and negatives with a margin were introduced in the contrastive loss (Hadsell, Chopra and LeCun, 2006). Schroff, Kalenichenko and Philbin made triplets the basis of FaceNet (2015), and Hermans, Beyer and Leibe in “In Defense of the Triplet Loss for Person Re-Identification” (2017) showed that with batch-hard mining triplets work well in Re-ID too."),
    ]),
    dict(id="sphere", title="Normalization on the sphere and choosing the margin", blocks=[
        ("p", "Without constraints the network can increase all distances by simply stretching the space: in the ordinary metric the margin $m$ loses its meaning if the scale is not fixed. That is why embeddings are often normalized: $\\hat f=f/\\|f\\|$, and all points lie on the unit sphere. For unit vectors"),
        ("eq", r"\|u-v\|^{2}=\|u\|^2+\|v\|^2-2\,u^\top v=2-2\cos\theta"),
        ("p", "where $\\theta$ is the angle between the vectors. The squared distance ranges from 0 (identical) to 4 (opposite), and FaceNet’s margin $m=0.2$ is $5\\%$ of the whole range. The requirement $d^2(a,n)\\ge d^2(a,p)+m$ becomes a requirement on angles: $\\cos\\theta_{an}\\le\\cos\\theta_{ap}-m/2$."),
        ("viz", "triplet-sphere", {"a": 0, "p": 40, "n": -45, "m": 0.2}, "<b>Figure 7.</b> Normalized embeddings on the unit circle (drag the points along it) and the squared distance as a function of the angle. The orange arc is the zone where the negative would violate the margin. With $\\theta_{ap}=40^\\circ$ and $m=0.2$ the negative must be at least $48.2^\\circ$ from the anchor; in the starting position it is at $45^\\circ$: $d^2(a,p)=0.468$, $d^2(a,n)=0.586$, $L=0.082$."),
        ("callout", "note", "How to choose the margin", "The margin is measured in units of distance, so it depends on the normalization and on whether the distance is squared. For normalized embeddings typical values are $0.2$ (FaceNet, $d^2$) and $0.3$ (torchreid, $d$). A margin that is too small hardly demands any separation; one that is too large may be unreachable and keeps all triplets active."),
    ]),
    dict(id="code", title="In code: batch mining and stability", blocks=[
        ("p", "The key to efficiency is the matrix of all pairwise distances in the batch, from which mining is done with masks and no loops. A numerical subtlety: $\\|u-v\\|$ is not differentiable at $u=v$ (the derivative of the square root at zero is infinite), and the formula $\\|u\\|^2-2u^\\top v+\\|v\\|^2$ may produce a tiny negative number due to rounding. So $\\max(\\cdot,\\varepsilon)$ is put under the root, and <code>nn.TripletMarginLoss</code> adds $\\varepsilon=10^{-6}$ to the difference of vectors."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "In practice", "A $P\\times K$ batch (for example $P=16$, $K=4$) is a must: without several pictures of the same person in the batch there are no positives. The triplet loss is usually combined with cross-entropy over identities — training is then faster and more stable."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            "<b>Random batches instead of $P\\times K$.</b> In a random batch many anchors have no positive at all, and no triplets can be formed.",
            "<b>Training on random triplets only.</b> Almost all of them are easy, the gradient is zero, and the loss “freezes” at a small value although the model is poor.",
            "<b>The hardest triplets from the very first step</b> without normalization or warm-up — a risk of all embeddings collapsing to a point.",
            "<b>A margin that ignores the scale.</b> Without normalization the network stretches the space; on the sphere $m$ has to be related to the maximum distance (2 for $d$, 4 for $d^2$).",
            "<b>The square root of zero.</b> The distance of a point to itself on the diagonal of the matrix gives a NaN gradient unless $\\varepsilon$ is added or the diagonal is masked.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("p", "The closest relative is the <b>contrastive loss</b>: it works with pairs and absolute thresholds rather than a relative comparison. For a pair labelled $y=1$ (same) or $y=0$ (different):"),
        ("eq", r"L_{\text{contr}}=y\,d^{2}+(1-y)\,\max(0,\;m-d)^{2}"),
        ("ul", [
            "<a href=\"../relu/\">ReLU</a>: the hinge $\\max(0,\\Delta+m)$ is a ReLU of the shifted difference of distances; its derivative is a step.",
            "<a href=\"../sigmoid/\">Sigmoid</a>: the derivative of the soft margin $\\ln(1+e^\\Delta)$ is $\\sigma(\\Delta)$.",
            "<a href=\"../softmax/\">Softmax</a> and <a href=\"../cross-entropy/\">cross-entropy</a>: the N-pair loss and InfoNCE generalize the triplet to one positive against many negatives via a softmax over similarities; ArcFace moves the margin into an angle inside the softmax.",
            "<a href=\"../mse/\">MSE</a>: the squared Euclidean distance is the same sum of squared differences.",
            "<a href=\"../focal/\">Focal Loss</a>: the same idea of “learning from the hard ones”, through a per-example weight rather than triplet selection.",
            "<a href=\"../adam/\">Adam</a>: the optimizer of the simulation in Figure 6.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, "1) $L=\\max(0,\\,d(a,p)-d(a,n)+m)$: the positive must be closer than the negative with a reserve $m$; it is a ReLU of $\\Delta+m$. 2) Regimes: easy ($L=0$, no gradient), semi-hard ($0&lt;L&lt;m$), hard ($L\\ge m$). 3) The gradients are unit vectors along the lines to the anchor (proportional to the distances for $d^2$), and they add up to zero. 4) Triplets are chosen inside a $P\\times K$ batch: batch-all, batch-hard, semi-hard. 5) Normalization on the sphere gives $d^2=2-2\\cos\\theta$ and a meaningful margin. 6) FaceNet and Re-ID rest on this: an embedding plus nearest-neighbour search."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q="$m=0.2$, $d(a,p)=0.9$, $d(a,n)=1.0$. What is the loss?", options=["$0$", "$0.1$", "$0.2$", "$0.3$"], answer=1,
                 explain="$\\max(0,\\,0.9-1.0+0.2)=0.1$: the positive is closer, but the reserve $0.1$ is smaller than the margin $0.2$."),
            dict(q="A triplet with $d(a,p)=0.5$, $d(a,n)=0.4$ at $m=0.2$ is…", options=["easy", "semi-hard", "hard", "impossible"], answer=2,
                 explain="The negative is closer than the positive: $d(a,n)\\le d(a,p)$, a hard triplet; $L=0.3\\ge m$."),
            dict(q="Where does the gradient-descent step for the negative $n$ of an active triplet point (ordinary metric)?", options=["Towards the anchor, length $d(a,n)$", "Away from the anchor, unit length", "Towards the positive $p$", "There is no step"], answer=1,
                 explain="$\\nabla_nL=-(n-a)/d(a,n)$; the step goes against the gradient: $+(n-a)/d(a,n)$ — a unit vector away from the anchor."),
            dict(q="What does batch-hard pick for each anchor?", options=["A random positive and a random negative", "The closest positive and the farthest negative", "The farthest positive and the closest negative", "All triplets with $L&gt;0$"], answer=2,
                 explain="The worst case for the anchor: $\\max d(a,p)$ and $\\min d(a,n)$ — the most informative triplet."),
            dict(q="For unit vectors at an angle of $90^\\circ$ the squared distance is…", options=["$0$", "$1$", "$2$", "$4$"], answer=2,
                 explain="$d^2=2-2\\cos90^\\circ=2$."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", "Oddiy klassifikator sinflarning qat’iy ro‘yxatini biladi. Lekin yuzni tanish tizimi o‘quv to‘plamida bo‘lmagan odamlarni ham tanishi, qayta identifikatsiya (re-identification, Re-ID) tizimi esa o‘sha odamni boshqa kamera yozuvida, boshqa rakursda va boshqa yorug‘likda topishi kerak. Har bir yangi odam uchun tarmoqni qayta o‘qitib bo‘lmaydi."),
        ("p", "Yechim — sinflarni emas, <b>metrikani</b> o‘rgatish (metric learning). $f$ tarmoq tasvirni $f(x)\\in\\mathbb R^d$ embedding vektoriga shunday aylantiradiki, bir odamning suratlari yonma-yon, turli odamlarniki esa uzoqda bo‘ladi. Shunda «bu kim?» savoli masofa bo‘yicha eng yaqin qo‘shnilarni qidirishga keltiriladi, yangi odam esa bazaga bitta embedding bilan qo‘shiladi."),
        ("p", "Triplet Loss bu talabni to‘g‘ridan-to‘g‘ri qo‘yadi. Uchlik olamiz: <b>langar</b> $a$ (anchor), <b>o‘ziniki</b> $p$ (positive, o‘sha odam) va <b>begona</b> $n$ (negative, boshqa odam). O‘ziniki begonadan kamida $m$ oraliqqa (margin) yaqinroq bo‘lishini talab qilamiz."),
        ("ul", [
            "<b>yuzni tanish</b> — FaceNet (Google, 2015): 128 o‘lchovli embeddinglar, $0{,}2$ oraliq, LFW to‘plamida $99{,}63\\%$ aniqlik;",
            "<b>odamlarni kameralar orasida qayta identifikatsiya qilish</b> — batch-hard triplet loss (Xermans va boshq., 2017) va torchreid kutubxonasi, unda u OSNet’ni o‘qitishda kross-entropiyani to‘ldiradi;",
            "<b>o‘xshash tasvirlar, tovarlar, ovozlarni qidirish</b> va umuman savol «bu namunaga nima yaqinroq?» bo‘lgan har qanday ma’no bo‘yicha qidiruv.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", "$L=\\max\\bigl(0,\\,d(a,p)-d(a,n)+m\\bigr)$. Agar begona o‘zinikidan $m$ dan ko‘proq uzoq bo‘lsa, yo‘qotish nolga teng va uchlik hech narsa o‘rgatmaydi. Aks holda gradiyent o‘zinikini langarga tortadi va begonani itaradi. Tasodifiy uchliklarning deyarli hammasi oson, shuning uchun asosiy mahorat — qiyinlarini tanlash (mayning), masalan batch ichidagi eng uzoq o‘ziniki va eng yaqin begonani (batch-hard)."),
    ]),
    dict(id="intuition", title="Intuitsiya: o‘ziniki begonadan yaqinroq", blocks=[
        ("p", "Embeddinglarni tekislikda chizamiz. $a$ langar atrofida o‘ziniki $p$ orqali aylana o‘tkazamiz — uning radiusi $d(a,p)$. Ikkinchisini oraliq qadar kengroq qo‘shamiz: radiusi $d(a,p)+m$. Formula talabi oddiy: <b>begona tashqi aylanadan tashqarida yotishi kerak</b>. To‘q sariq halqaga yoki ichkariga tushsa — yo‘qotish musbat."),
        ("viz", "triplet-play", {"a": [-0.5, 0], "p": [0.4, 0], "n": [0.1, 0.8], "m": 0.2}, "<b>1-rasm.</b> Langar, o‘ziniki va begonani torting. To‘q sariq strelkalar — gradiyent tushish har bir nuqtani siljitadigan yo‘nalishlar. Boshlang‘ich holatda $d(a,p)=0{,}9$, $d(a,n)=1{,}0$, $m=0{,}2$: begona halqa ichida, $L=0{,}9-1{,}0+0{,}2=0{,}1$. Uni halqadan tashqariga chiqaring — strelkalar yo‘qoladi."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", "O‘ziniki va begonadagi strelkalar doim langarga boruvchi chiziqlar bo‘ylab yo‘nalgan, oddiy (kvadratsiz) metrikada esa ularning uzunliklari bir xil va 1 ga teng: buzilish kattaligi emas, uning faktining o‘zi muhim. Masofalar kvadratlarini yoqing — strelkalar uzunligi masofalarga proporsional bo‘lib qoladi."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("p", "Yo‘qotishni to‘liq yozamiz — tarmoq, masofalar va uchliklar bo‘yicha o‘rtachalash bilan:"),
        ("eq", r"\mathcal L=\frac{1}{|T|}\sum_{(a,p,n)\in T}\max\Bigl(0,\;\bigl\|f(x_a)-f(x_p)\bigr\|-\bigl\|f(x_a)-f(x_n)\bigr\|+m\Bigr)"),
        ("symbols", [
            (r"f(x)", "embedding: $x$ tasvir uchun tarmoq chiqishi, $\\mathbb R^d$ dagi vektor (FaceNet’da $d=128$), ko‘pincha birlik uzunlikka normallashtirilgan;"),
            (r"d(a,p)", "o‘zinikigacha masofa, $\\|f(x_a)-f(x_p)\\|$; uni kamaytirmoqchimiz;"),
            (r"d(a,n)", "begonagacha masofa, $\\|f(x_a)-f(x_n)\\|$; uni oshirmoqchimiz;"),
            (r"m>0", "oraliq: begona o‘zinikidan shunchaki emas, $m$ zaxira bilan uzoqroq bo‘lishi kerak;"),
            (r"\max(0,\cdot)", "sharnir (hinge): bajarilgan talab jarimalanmaydi va gradiyent bermaydi;"),
            (r"T", "o‘rtachalanadigan uchliklar to‘plami — odatda batch ichidagi uchliklar (mayning bo‘limiga qarang)."),
        ]),
        ("p", "Bitta o‘zgaruvchi — masofalar ayirmasi $\\Delta=d(a,p)-d(a,n)$ ni kiritish qulay. U holda $L=\\max(0,\\Delta+m)$: bu $m$ ga surilgan <a href=\"../relu/\">ReLU</a>. Manfiy $\\Delta$ o‘ziniki allaqachon yaqinroq ekanini bildiradi; lekin $\\Delta&gt;-m$ ekan, zaxira yetmaydi."),
        ("p", "$m=0{,}2$ dagi misollar: $d(a,p)=0{,}4$, $d(a,n)=1{,}1$ $\\Delta=-0{,}7$ va $L=\\max(0;\\,-0{,}5)=0$ beradi — uchlik allaqachon ajratilgan. $d(a,p)=0{,}9$, $d(a,n)=1{,}0$ $\\Delta=-0{,}1$ va $L=0{,}1$ beradi: o‘ziniki yaqinroq, lekin oraliq kam."),
        ("viz", "triplet-hinge", {"m": 0.2, "delta": -0.1}, "<b>2-rasm.</b> $\\Delta$ funksiyasi sifatidagi yo‘qotish (yuqorida) va uning hosilasi (pastda). Hosila — zinapoya: bajarilgan uchliklar uchun 0, buzilganlari uchun 1, oraliq qiymatlarsiz. Punktir — Xermans va boshqalar ishidagi «yumshoq oraliq» (soft margin) $\\ln(1+e^{\\Delta})$: u hech qachon nolga aylanmaydi, hosilasi esa <a href=\"../sigmoid/\">sigmoida</a> $\\sigma(\\Delta)$. $\\Delta=-0{,}1$ da: hinge $0{,}1$, yumshoq variant $0{,}644$ beradi."),
        ("callout", "note", "Oraliq — nisbiy", "Triplet Loss o‘zinikilar qandaydir qat’iy chegaradan yaqinroq bo‘lishini talab qilmaydi — faqat begonalardan yaqinroq bo‘lishini. Shuning uchun turli odamlarning klasterlari turli o‘lchamda bo‘lishi mumkin. «Bu o‘sha odam» javobi uchun chegara keyin, validatsiyada tanlanadi."),
    ]),
    dict(id="regimes", title="Uch rejim: oson, yarim qiyin, qiyin", blocks=[
        ("p", "Har bir uchlik $d(a,p)$ va $d(a,n)$ ga qarab uch rejimdan biriga tushadi:"),
        ("table", ["Rejim", "Shart", "$L$", "Gradiyent"], [
            ["oson (easy)", "$d(a,n)\\ge d(a,p)+m$", "$0$", "yo‘q"],
            ["yarim qiyin (semi-hard)", "$d(a,p)&lt;d(a,n)&lt;d(a,p)+m$", "$0$ dan $m$ gacha", "bor"],
            ["qiyin (hard)", "$d(a,n)\\le d(a,p)$", "$m$ dan kam emas", "bor"],
        ], {}),
        ("p", "$(d(a,p),\\,d(a,n))$ tekisligida rejimlar chegaralari — ikkita parallel to‘g‘ri chiziq: $d(a,n)=d(a,p)$ va $d(a,n)=d(a,p)+m$. Yo‘qotish — ulardan yuqoridagisidan tepada nol bilan kesilgan qiya tekislik."),
        ("viz", "triplet-regimes", {"m": 0.2, "pt": [0.9, 1.0]}, "<b>3-rasm.</b> $(d(a,p),\\,d(a,n))$ tekisligidagi yo‘qotish: qizil rang qancha to‘q bo‘lsa, u shuncha katta. Nuqtalar — 5-rasmdagi batchning barcha 576 uchligi (4 kishi, har biri 4 suratdan). $m=0{,}2$ da ulardan 510 tasi oson, 31 tasi yarim qiyin va 35 tasi qiyin: 576 tadan faqat 66 uchlik gradiyent beradi. Oraliqni oshiring — yarim qiyinlar polosasi kengayadi."),
        ("callout", "warn", "Nega tasodifiy uchliklar foydasiz", "Tarmoq ozgina o‘rgangan zahoti tasodifiy uchliklarning aksariyati oson bo‘lib qoladi: ularning yo‘qotishi va gradiyenti nolga teng. Ular bo‘yicha o‘rtachalash foydali signalni suyultiradi va o‘qitish deyarli to‘xtaydi. Mayning shundan kelib chiqadi — qiyin va yarim qiyin uchliklarni maqsadli tanlash."),
    ]),
    dict(id="gradients", title="Gradiyentlar: har bir nuqta qayerga tortiladi", blocks=[
        ("p", "Faol uchlik ($L&gt;0$) uchun yo‘qotish $d(a,p)-d(a,n)+m$ ga teng va hammasi masofa gradiyentiga keltiriladi. Evklid normasi uchun $\\nabla_u\\|u-v\\|=\\frac{u-v}{\\|u-v\\|}$ — $v$ dan $u$ ga yo‘nalgan birlik vektor."),
        ("deep", "Uch nuqta bo‘yicha gradiyentlarni keltirib chiqarish", [
            ("p", "Embeddinglarni $a,p,n$ va $d_{ap}=\\|a-p\\|$, $d_{an}=\\|a-n\\|$ deb belgilaymiz. $d_{ap}=\\sqrt{(a-p)^\\top(a-p)}$ ni zanjir qoidasi bo‘yicha differensiallaymiz:"),
            ("eq", r"\nabla_a d_{ap}=\frac{1}{2d_{ap}}\cdot2(a-p)=\frac{a-p}{d_{ap}},\qquad \nabla_p d_{ap}=\frac{p-a}{d_{ap}}"),
            ("p", "$d_{an}$ uchun ham xuddi shunday. $L=d_{ap}-d_{an}+m$ ga qo‘yamiz:"),
            ("eq", r"\nabla_p L=\frac{p-a}{d_{ap}},\qquad \nabla_n L=-\frac{n-a}{d_{an}},\qquad \nabla_a L=\frac{a-p}{d_{ap}}-\frac{a-n}{d_{an}}"),
            ("p", "Uch gradiyent yig‘indisi nolga teng: uchala nuqtani bir xil vektorga surish masofalarni o‘zgartirmaydi, demak, yo‘qotish ham o‘zgarmaydi. Masofalar kvadratlari uchun $L=d_{ap}^2-d_{an}^2+m$ dan $\\nabla_pL=2(p-a)$, $\\nabla_nL=-2(n-a)$ va $\\nabla_aL=2(n-p)$ ni olamiz — langarning gradiyenti umuman uning holatiga bog‘liq emas."),
        ]),
        ("p", "Gradiyent tushish qadami gradiyentga qarshi yo‘naladi: o‘ziniki $p$ <b>langarga qarab</b>, begona $n$ <b>langardan uzoqqa</b> siljiydi, langar esa o‘zinikiga qarab va begonadan uzoqlashadi. Oddiy metrikada bu siljishlar uzunligi istalgan masofada 1 ga teng; kvadratli metrikada — masofalarga proporsional."),
        ("p", "Buni 3D sirtda ko‘rish mumkin. Langarni koordinata boshida, o‘zinikini esa $0{,}6$ masofada mahkamlaymiz; yo‘qotish begonaning $n=(x,y)$ holatiga qanday bog‘liq? To‘ntarilgan konus hosil bo‘ladi: markazda $L=0{,}6+m$, radiusi $0{,}6+m$ bo‘lgan doira chetida — nol. Konus qiyaligi hamma joyda bir xil, $|\\nabla L|=1$."),
        ("viz", "triplet-surface", {"m": 0.4, "who": "neg"}, "<b>4-rasm.</b> Langar mahkamlanganda begona (yoki o‘ziniki) holatining funksiyasi sifatidagi yo‘qotish; sirtni aylantirish mumkin. O‘ngda — langardan chiqqan nur bo‘ylab kesim: yo‘qotishning o‘zi va gradiyent normasi. $m=0{,}4$ va oddiy masofada konus balandligi $1{,}0$ va radiusi $1{,}0$. $d^2$ ga o‘ting: sirt balandligi $0{,}76$ va radiusi $0{,}872$ bo‘lgan paraboloidga aylanadi, langarning o‘zida esa gradiyent nolga aylanadi. O‘ziniki uchun (begona $1{,}2$ masofada) — voronka: yo‘qotish radiusi $0{,}8$ bo‘lgan aylanadan tashqarida o‘sadi."),
        ("callout", "warn", "Masofa kvadrati va qiyin begonalar", "Masofalar kvadratlarida itarish kuchi $2\\,d(a,n)$ begona langarga qancha yaqin bo‘lsa, shuncha zaif — ya’ni aynan eng xavfli xatolar uchun. Oddiy metrikada u doimiy. Shuning uchun Re-ID’da (Xermans va boshq., 2017) oddiy Evklid masofasi tavsiya etiladi; FaceNet kvadratlardan foydalanadi, lekin normallashtirilgan vektorlarda va yarim qiyin uchliklar bilan."),
    ]),
    dict(id="mining", title="Mayning: qaysi uchliklarni olish kerak", blocks=[
        ("p", "$N$ ta tasvir to‘plamida $N^3$ tartibidagi uchlik bor — hammasini sanab chiqib bo‘lmaydi, ularning deyarli barchasi oson ham. Uchliklar batch ichida <b>onlayn</b> tanlanadi. Batch $P\\times K$ sxemasida quriladi: $P$ kishi, har biridan $K$ surat. Bunday batch ichida"),
        ("eq", r"|T|=\underbrace{PK}_{\text{langarlar}}\cdot\underbrace{(K-1)}_{\text{o‘zinikilar}}\cdot\underbrace{(P-1)K}_{\text{begonalar}}"),
        ("p", "$P=4$, $K=4$ da bu 576 uchlik, $P=18$, $K=4$ da (Xermans va boshqalarning Market-1501 to‘plami uchun batchi) — allaqachon 14 688. Asosiy strategiyalar:"),
        ("ul", [
            "<b>batch-all</b> — batchning barcha uchliklarini olamiz va osonlari signalni suyultirmasligi uchun yo‘qotishni faqat faollari ($L&gt;0$) bo‘yicha o‘rtachalaymiz;",
            "<b>batch-hard</b> — har bir langar uchun bitta uchlik: <i>eng uzoq o‘ziniki</i> va <i>eng yaqin begona</i>; $PK$ ta eng informativ uchlik;",
            "<b>semi-hard</b> (FaceNet) — $(a,p)$ juftligi uchun o‘zinikidan uzoqroq, lekin oraliq ichidagi begona olinadi; shunda boshida o‘qitish yumshoqroq bo‘ladi.",
        ]),
        ("eq", r"\mathcal L_{\text{BH}}=\frac{1}{PK}\sum_{a}\max\Bigl(0,\;\max_{p:\,y_p=y_a}d(a,p)-\min_{n:\,y_n\ne y_a}d(a,n)+m\Bigr)"),
        ("viz", "triplet-mining", {"anchor": 1, "m": 0.2, "strategy": "hard"}, "<b>5-rasm.</b> Embedding fazosidagi $P=4$, $K=4$ batch. Langar va strategiyani tanlang. batch-hard rejimida qalin chiziqlar eng uzoq o‘ziniki va eng yaqin begonaga olib boradi, punktir aylana — $d_{\\max}(a,p)+m$ radius. $m=0{,}2$ da batch-hard $L=0{,}353$, batch-all esa 576 tadan 66 faol uchlik bo‘yicha $0{,}306$ beradi. Birinchi langarning 36 uchligidan 34 tasi oson va 2 tasi yarim qiyin."),
        ("callout", "warn", "Eng qiyinlarining xavfi", "Eng qiyin uchliklar ko‘pincha belgilashdagi xatolar yoki deyarli farqlanmaydigan suratlar bo‘lib chiqadi. O‘qitish boshida, embeddinglar tasodifiy bo‘lganda, ularning ortidan quvish modelni «yopishtirib» qo‘yishi mumkin: barcha $f(x)$ bitta nuqtaga tortiladi, u yerda istalgan uchlik uchun $L=m$. Boshida yarim qiyin uchliklar, embeddinglarni normallashtirish, yumshoq oraliq va kross-entropiya bilan birlashtirish yordam beradi."),
    ]),
    dict(id="training", title="O‘qitishda bu qanday ishlaydi", blocks=[
        ("p", "Hammasini birlashtiramiz. Har bir suratning ikki belgisi bo‘lsin: $x_1$ — bir odamning o‘zida kuchli o‘zgaradigan xalaqit (rakurs, yoritilish), $x_2$ esa — xalaqit ozgina egib yuborgan shaxs belgisi. Kirish fazosida bir odamning ikki surati turli odamlarning suratlaridan uzoqroq bo‘lishi mumkin: uchliklarning faqat $62{,}7\\%$ i to‘g‘ri tartiblangan."),
        ("p", "Kichik $f:\\mathbb R^2\\to\\mathbb R^2$ tarmoq (12 ta tanh neyron) $m=0{,}5$ dagi batch-hard triplet loss va <a href=\"../adam/\">Adam</a> optimizatori bilan o‘qitiladi. Unga qaysi odam qayerda bo‘lishi kerakligi aytilmaydi — faqat o‘zinikilar begonalardan yaqinroq bo‘lishi kerakligi."),
        ("viz", "triplet-train", {"m": 0.5}, "<b>6-rasm.</b> Chapda — har biri 12 suratli 4 kishining kirishlari, o‘ngda — ularning embeddinglari, pastda — yo‘qotish. «Boshlash»ni bosing. Boshida $L=1{,}266$, barcha 48 langar faol, uchliklarning $64{,}9\\%$ i to‘g‘ri tartiblangan. 60-qadamga kelib $100\\%$ i tartiblangan, lekin 42 langarga hali oraliq yetmaydi; 300-qadamga kelib 4 tasi faol qoladi, 600-qadamda yo‘qotish nolga teng. Tarmoq polosalarni «to‘g‘riladi»: $x_1$ xalaqit endi masofalarga ta’sir qilmaydi."),
        ("p", "Re-ID ham xuddi shunday ishlaydi: so‘rov (query) — bir kameradagi odam surati, galereya (gallery) — qolgan barcha kameralardagi suratlar. Galereya embeddinglari so‘rovgacha bo‘lgan masofa bo‘yicha saralanadi va birinchi to‘g‘ri javob nechanchi o‘rinda ekaniga qaraladi. Metrikalar — Rank-1 (to‘g‘ri javob birinchi o‘rinda) va mAP (barcha to‘g‘rilar bo‘yicha o‘rtacha aniqlik)."),
        ("callout", "history", "Bu qayerdan boshlangan", "O‘zinikilar va begonalar orasidagi oraliq g‘oyasi — katta oraliqli eng yaqin qo‘shnilar usulidan (LMNN, Vaynberger va Sol, 2005). Oraliqli o‘ziniki va begona juftliklarini kontrastiv yo‘qotish kiritgan (Xadsell, Chopra va LeKun, 2006). Shroff, Kalenichenko va Filbin uchliklarni FaceNet asosiga aylantirdi (2015), Xermans, Bayer va Leybe esa «In Defense of the Triplet Loss for Person Re-Identification» (2017) ishida batch-hard mayning bilan uchliklar Re-ID’da ham yaxshi ishlashini ko‘rsatdi."),
    ]),
    dict(id="sphere", title="Sferada normallashtirish va oraliqni tanlash", blocks=[
        ("p", "Cheklovlarsiz tarmoq fazoni shunchaki cho‘zib, barcha masofalarni oshirishi mumkin: oddiy metrikada masshtab qat’iy bo‘lmasa, $m$ oraliq ma’nosini yo‘qotadi. Shuning uchun embeddinglar ko‘pincha normallashtiriladi: $\\hat f=f/\\|f\\|$, barcha nuqtalar birlik sferada yotadi. Birlik vektorlar uchun"),
        ("eq", r"\|u-v\|^{2}=\|u\|^2+\|v\|^2-2\,u^\top v=2-2\cos\theta"),
        ("p", "bunda $\\theta$ — vektorlar orasidagi burchak. Masofa kvadrati 0 dan (ustma-ust) 4 gacha (qarama-qarshi) o‘zgaradi va FaceNet’dagi $m=0{,}2$ oraliq butun diapazonning $5\\%$ i. $d^2(a,n)\\ge d^2(a,p)+m$ talabi burchaklarga qo‘yilgan talabga aylanadi: $\\cos\\theta_{an}\\le\\cos\\theta_{ap}-m/2$."),
        ("viz", "triplet-sphere", {"a": 0, "p": 40, "n": -45, "m": 0.2}, "<b>7-rasm.</b> Birlik aylanadagi normallashtirilgan embeddinglar (nuqtalarni aylana bo‘ylab torting) va burchak funksiyasi sifatidagi masofa kvadrati. To‘q sariq yoy — begona oraliqni buzadigan zona. $\\theta_{ap}=40^\\circ$ va $m=0{,}2$ da begona langardan kamida $48{,}2^\\circ$ uzoqda bo‘lishi kerak; boshlang‘ich holatda u $45^\\circ$ da: $d^2(a,p)=0{,}468$, $d^2(a,n)=0{,}586$, $L=0{,}082$."),
        ("callout", "note", "Oraliqni qanday tanlash kerak", "Oraliq masofa birliklarida o‘lchanadi, shuning uchun normallashtirishga va masofa kvadratmi yoki yo‘qligiga bog‘liq. Normallashtirilgan embeddinglar uchun odatiy qiymatlar $0{,}2$ (FaceNet, $d^2$) va $0{,}3$ (torchreid, $d$). Juda kichik oraliq deyarli ajratishni talab qilmaydi, juda kattasiga esa erishib bo‘lmasligi mumkin va u barcha uchliklarni faol ushlab turadi."),
    ]),
    dict(id="code", title="Kodda: batch ichida mayning va barqarorlik", blocks=[
        ("p", "Samaradorlik kaliti — batchdagi barcha juft masofalar matritsasi, undan mayning sikllarsiz, niqoblar bilan olinadi. Sonli nozik jihat: $\\|u-v\\|$ $u=v$ da differensiallanmaydi (ildizning noldagi hosilasi cheksiz), $\\|u\\|^2-2u^\\top v+\\|v\\|^2$ formulasi esa yaxlitlash tufayli juda kichik manfiy son berishi mumkin. Shuning uchun ildiz ostiga $\\max(\\cdot,\\varepsilon)$ qo‘yiladi, <code>nn.TripletMarginLoss</code> esa vektorlar ayirmasiga $\\varepsilon=10^{-6}$ qo‘shadi."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Amaliyot", "$P\\times K$ batch (masalan, $P=16$, $K=4$) albatta kerak: batchda bir odamning bir nechta surati bo‘lmasa, o‘zinikilar bo‘lmaydi. Triplet loss odatda shaxslar bo‘yicha kross-entropiya bilan birlashtiriladi — shunda o‘qitish tezroq va barqarorroq."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            "<b>$P\\times K$ o‘rniga tasodifiy batchlar.</b> Tasodifiy batchda ko‘p langarlarning birorta ham o‘zinikisi yo‘q va uchliklar yig‘ilmaydi.",
            "<b>Faqat tasodifiy uchliklarda o‘qitish.</b> Ularning deyarli hammasi oson, gradiyent nol va model yomon bo‘lsa ham yo‘qotish kichik qiymatda «qotib qoladi».",
            "<b>Birinchi qadamdan eng qiyin uchliklar</b> normallashtirish va qizdirishsiz — barcha embeddinglarning bitta nuqtaga yopishib qolish xavfi.",
            "<b>Masshtabni hisobga olmagan oraliq.</b> Normallashtirishsiz tarmoq fazoni cho‘zadi; sferada $m$ ni masofa maksimumiga ($d$ uchun 2, $d^2$ uchun 4) solishtirish kerak.",
            "<b>Noldan ildiz.</b> Matritsa diagonalidagi nuqtaning o‘zigacha masofasi, agar $\\varepsilon$ qo‘shilmasa yoki diagonal niqoblanmasa, gradiyentda NaN beradi.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘lanish", blocks=[
        ("p", "Eng yaqin qarindoshi — <b>kontrastiv yo‘qotish</b> (contrastive loss): u nisbiy taqqoslash bilan emas, juftliklar va mutlaq chegaralar bilan ishlaydi. $y=1$ (o‘zinikilar) va $y=0$ (begonalar) belgili juftlik uchun:"),
        ("eq", r"L_{\text{contr}}=y\,d^{2}+(1-y)\,\max(0,\;m-d)^{2}"),
        ("ul", [
            "<a href=\"../relu/\">ReLU</a>: $\\max(0,\\Delta+m)$ sharnir — masofalarning surilgan ayirmasidan olingan ReLU; uning hosilasi — zinapoya.",
            "<a href=\"../sigmoid/\">Sigmoida</a>: $\\ln(1+e^\\Delta)$ yumshoq oraliq hosilasi $\\sigma(\\Delta)$ ga teng.",
            "<a href=\"../softmax/\">Softmax</a> va <a href=\"../cross-entropy/\">kross-entropiya</a>: N-pair loss va InfoNCE uchlikni o‘xshashliklar bo‘yicha softmax orqali bitta o‘ziniki va ko‘plab begonalarga umumlashtiradi; ArcFace oraliqni softmax ichidagi burchakka ko‘chiradi.",
            "<a href=\"../mse/\">MSE</a>: Evklid masofasi kvadrati — ayirmalar kvadratlarining o‘sha yig‘indisi.",
            "<a href=\"../focal/\">Focal Loss</a>: «qiyinlardan o‘rganish» g‘oyasining o‘zi, faqat uchliklarni tanlash orqali emas, misol vazni orqali.",
            "<a href=\"../adam/\">Adam</a>: 6-rasmdagi simulyatsiya optimizatori.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, "1) $L=\\max(0,\\,d(a,p)-d(a,n)+m)$: o‘ziniki begonadan $m$ zaxira bilan yaqinroq bo‘lishi kerak; bu $\\Delta+m$ dan olingan ReLU. 2) Rejimlar: oson ($L=0$, gradiyent yo‘q), yarim qiyin ($0&lt;L&lt;m$), qiyin ($L\\ge m$). 3) Gradiyentlar — langarga boruvchi chiziqlar bo‘ylab birlik vektorlar ($d^2$ uchun masofalarga proporsional), yig‘indisi nolga teng. 4) Uchliklar $P\\times K$ batch ichida tanlanadi: batch-all, batch-hard, semi-hard. 5) Sferada normallashtirish $d^2=2-2\\cos\\theta$ va ma’noli oraliq beradi. 6) FaceNet va Re-ID shunga tayanadi: embedding va eng yaqin qo‘shnilarni qidirish."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q="$m=0{,}2$, $d(a,p)=0{,}9$, $d(a,n)=1{,}0$. Yo‘qotish nimaga teng?", options=["$0$", "$0{,}1$", "$0{,}2$", "$0{,}3$"], answer=1,
                 explain="$\\max(0;\\,0{,}9-1{,}0+0{,}2)=0{,}1$: o‘ziniki yaqinroq, lekin $0{,}1$ zaxira $0{,}2$ oraliqdan kichik."),
            dict(q="$m=0{,}2$ da $d(a,p)=0{,}5$, $d(a,n)=0{,}4$ bo‘lgan uchlik —…", options=["oson", "yarim qiyin", "qiyin", "mumkin emas"], answer=2,
                 explain="Begona o‘zinikidan yaqinroq: $d(a,n)\\le d(a,p)$, bu qiyin uchlik; $L=0{,}3\\ge m$."),
            dict(q="Faol uchlikdagi begona $n$ uchun gradiyent tushish qadami qayerga yo‘nalgan (oddiy metrika)?", options=["Langarga, uzunligi $d(a,n)$", "Langardan, birlik uzunlikda", "O‘ziniki $p$ ga", "Qadam yo‘q"], answer=1,
                 explain="$\\nabla_nL=-(n-a)/d(a,n)$, qadam gradiyentga qarshi: $+(n-a)/d(a,n)$ — langardan yo‘nalgan birlik vektor."),
            dict(q="batch-hard har bir langar uchun nimani tanlaydi?", options=["Tasodifiy o‘ziniki va tasodifiy begonani", "Eng yaqin o‘ziniki va eng uzoq begonani", "Eng uzoq o‘ziniki va eng yaqin begonani", "$L&gt;0$ bo‘lgan barcha uchliklarni"], answer=2,
                 explain="Langar uchun eng yomon holat: $\\max d(a,p)$ va $\\min d(a,n)$ — eng informativ uchlik."),
            dict(q="$90^\\circ$ burchak ostidagi birlik vektorlar uchun masofa kvadrati…", options=["$0$", "$1$", "$2$", "$4$"], answer=2,
                 explain="$d^2=2-2\\cos90^\\circ=2$."),
        ]),
    ]),
],
}

# Fill in the code listings per language.
for _lang, _secs in SECTIONS.items():
    for _sec in _secs:
        for _i, _b in enumerate(_sec["blocks"]):
            if _b[0] == "code" and _b[2] in ("CODE_NUMPY", "CODE_TORCH"):
                _sec["blocks"][_i] = (_b[0], _b[1], _code(CODE_NUMPY if _b[2] == "CODE_NUMPY" else CODE_TORCH, _lang))
