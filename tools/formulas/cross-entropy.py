"""Formula page: categorical cross-entropy. Format: see README.md; widgets in assets/js/formulas/cross-entropy.js."""

META = dict(
    id="cross-entropy",
    date="2026-10-28",
    minutes=35,
    hero=r"\mathrm{CE}=-\sum_{k=1}^{K}y_k\log\hat{y}_k",
    title={"ru": "Категориальная кросс-энтропия", "en": "Categorical cross-entropy", "uz": "Kategorial kross-entropiya"},
    dek={
        "ru": "Главная потеря классификации и языковых моделей. Разбираем её по косточкам: почему штраф — минус логарифм, как кросс-энтропия раскладывается на энтропию и KL-дивергенцию, почему в паре с softmax градиент равен просто s − y, как выглядит ландшафт потерь, зачем сглаживают метки и что такое перплексия.",
        "en": "The main loss of classification and of language models. We take it apart bone by bone: why the penalty is minus a logarithm, how cross-entropy splits into entropy and KL divergence, why together with softmax the gradient is simply s − y, what the loss landscape looks like, why labels are smoothed, and what perplexity is.",
        "uz": "Klassifikatsiya va til modellarining asosiy yo‘qotishi. Uni mayda detallarigacha tahlil qilamiz: nega jarima — minus logarifm, kross-entropiya qanday qilib entropiya va KL-divergensiyaga ajraladi, nega softmax bilan juftlikda gradiyent shunchaki s − y, yo‘qotishlar landshafti qanday ko‘rinadi, belgilar nima uchun silliqlanadi va perpleksiya nima.",
    },
    description={
        "ru": "Кросс-энтропия подробно: −log p, связь с правдоподобием, энтропия и KL-дивергенция, градиент s − y, выпуклость, ландшафт в 3D, сглаживание меток, CE против MSE, перплексия, устойчивый код.",
        "en": "Cross-entropy in depth: −log p, the link to likelihood, entropy and KL divergence, the gradient s − y, convexity, the 3D landscape, label smoothing, CE versus MSE, perplexity, stable code.",
        "uz": "Kross-entropiya batafsil: −log p, haqqoniylik bilan bog‘liqlik, entropiya va KL-divergensiya, s − y gradiyent, qavariqlik, 3D landshaft, belgilarni silliqlash, CE va MSE, perpleksiya, barqaror kod.",
    },
)

# Running example: logits (2, 1, 0), the correct class is the first (checked with numpy).
TABLE = [("1", "2", "0.665", "1", "0.408", "−0.335"), ("2", "1", "0.245", "0", "0", "0.245"),
         ("3", "0", "0.090", "0", "0", "0.090"), ("Σ", "", "1", "1", "0.408", "0")]
HEADS = ["$k$", "$z_k$", "$s_k$", "$y_k$", "$-y_k\\ln s_k$", "$s_k-y_k$"]


def _table(lang):
    dec = "." if lang == "en" else ","
    return [[c.replace(".", dec) for c in row] for row in TABLE]


CODE_NUMPY = '''import numpy as np
np.set_printoptions(precision=3)

def log_softmax(z):
    z = z - z.max(axis=-1, keepdims=True)          # устойчивость: max-трюк
    return z - np.log(np.exp(z).sum(axis=-1, keepdims=True))

def cross_entropy(logits, y):
    """Средняя CE по батчу. logits: (N, K), y: (N,) — номера классов."""
    logp = log_softmax(logits)
    return -logp[np.arange(len(y)), y].mean()

def cross_entropy_grad(logits, y):
    # dCE/dz = (softmax(z) − onehot(y)) / N
    s = np.exp(log_softmax(logits))
    s[np.arange(len(y)), y] -= 1
    return s / len(y)

z = np.array([[2.0, 1.0, 0.0]])
print(cross_entropy(z, np.array([0])))        # ≈ 0.4076
print(cross_entropy(z, np.array([2])))        # ≈ 2.4076 — уверенная ошибка
print(cross_entropy_grad(z, np.array([0])))   # [[-0.335  0.245  0.09 ]]
print(cross_entropy(z + 1000, np.array([0]))) # ≈ 0.4076 — без переполнения'''

CODE_TORCH = '''import torch
import torch.nn.functional as F

logits = torch.tensor([[2.0, 1.0, 0.0]], requires_grad=True)
target = torch.tensor([0])                  # номер класса, а не one-hot
loss = F.cross_entropy(logits, target)      # tensor(0.4076): log_softmax + NLL
loss.backward()
print(logits.grad)                          # tensor([[-0.3348,  0.2447,  0.0900]])

F.cross_entropy(logits, target, label_smoothing=0.1)   # tensor(0.5076)

# Языковая модель: логиты (B, T, V), токены (B, T)
B, T, V = 2, 5, 50000
lm_logits = torch.randn(B, T, V)
tokens = torch.randint(0, V, (B, T))
loss = F.cross_entropy(lm_logits.reshape(-1, V), tokens.reshape(-1))
print(torch.exp(loss))                      # перплексия: порядка V для случайных логитов'''

_REPL = {
    "en": [("устойчивость: max-трюк", "stability: the max trick"),
           ("Средняя CE по батчу. logits: (N, K), y: (N,) — номера классов.", "Mean CE over a batch. logits: (N, K), y: (N,) — class indices."),
           ("— уверенная ошибка", "— a confident mistake"), ("— без переполнения", "— no overflow"),
           ("номер класса, а не one-hot", "a class index, not one-hot"),
           ("Языковая модель: логиты (B, T, V), токены (B, T)", "A language model: logits (B, T, V), tokens (B, T)"),
           ("перплексия: порядка V для случайных логитов", "perplexity: of order V for random logits")],
    "uz": [("устойчивость: max-трюк", "barqarorlik: max-hiyla"),
           ("Средняя CE по батчу. logits: (N, K), y: (N,) — номера классов.", "Batch bo‘yicha o‘rtacha CE. logits: (N, K), y: (N,) — sinf raqamlari."),
           ("— уверенная ошибка", "— ishonchli xato"), ("— без переполнения", "— to‘lib ketishsiz"),
           ("номер класса, а не one-hot", "one-hot emas, sinf raqami"),
           ("Языковая модель: логиты (B, T, V), токены (B, T)", "Til modeli: logitlar (B, T, V), tokenlar (B, T)"),
           ("перплексия: порядка V для случайных логитов", "perpleksiya: tasodifiy logitlarda V tartibida")],
}


def _code(src, lang):
    for a, b in _REPL.get(lang, []):
        src = src.replace(a, b)
    return src


SECTIONS = {
"ru": [
    dict(id="why", title="Зачем она нужна", blocks=[
        ("p", r"Модель выдала вероятности классов — например, $(0{,}665;\,0{,}245;\,0{,}090)$ для «кошка», «собака», «птица», — а на картинке кошка. Насколько это хорошо? Нужно одно число, которое тем меньше, чем больше вероятность правильного ответа, и которое можно минимизировать градиентным спуском. Стандартный ответ — <b>категориальная кросс-энтропия</b> (categorical cross-entropy, CE): здесь $\mathrm{CE}=-\ln0{,}665\approx0{,}408$."),
        ("p", "Где она встречается:"),
        ("ul", [
            r"<b>обучение многоклассовых классификаторов</b> — от логистической регрессии до ResNet и ViT: последний слой выдаёт логиты, <a href='../softmax/'>softmax</a> превращает их в вероятности, CE оценивает ответ;",
            r"<b>языковые модели</b> — предобучение GPT, LLaMA, Qwen — это минимизация CE следующего токена: классы — токены словаря, а $e^{\mathrm{CE}}$ — знаменитая перплексия;",
            r"<b>дистилляция знаний</b> — ученик минимизирует CE до «мягких» вероятностей учителя;",
            r"<b>статистика</b> — минимизация CE равносильна методу максимального правдоподобия для категориального распределения;",
            r"<b>теория информации</b> — CE равна средней длине кода, если кодировать данные по модели $q$, а приходят они из распределения $p$.",
        ]),
        ("callout", "key", "Главное за минуту", r"$\mathrm{CE}=-\sum_k y_k\ln\hat y_k$; для one-hot метки это минус логарифм вероятности правильного класса. Уверенная ошибка стоит дорого: $-\ln0{,}1\approx2{,}303$ против $-\ln0{,}9\approx0{,}105$. В паре с softmax градиент по логитам — просто $s-y$, без насыщения. Кросс-энтропия = энтропия + KL-дивергенция, а $e^{\mathrm{CE}}$ — перплексия."),
    ]),
    dict(id="intuition", title="Интуиция: штраф за удивление", blocks=[
        ("p", r"Пусть модель заранее объявляет вероятности, а потом узнаёт правильный ответ. Если правильному классу она дала вероятность $p$, её «удивление» равно $-\ln p$: при $p=1$ удивления нет, при $p=0{,}5$ оно равно $\ln2\approx0{,}693$, а при $p\to0$ растёт до бесконечности. Кросс-энтропия — среднее удивление модели на данных."),
        ("p", r"Почему именно логарифм? Во-первых, он превращает произведение вероятностей независимых примеров в сумму. Во-вторых, он поощряет честность: среди штрафов, зависящих только от вероятности, которую модель дала случившемуся исходу, при трёх и более исходах лишь логарифмический (с точностью до линейного преобразования) минимален в среднем тогда, когда модель называет свои истинные вероятности."),
        ("viz", "cross-entropy-surprise", {"p": 0.665}, r"<b>Рисунок 1.</b> Сверху — штраф $-\ln p$ (синий) и квадратичная ошибка $(1-p)^2$ для сравнения; снизу — их производные по $p$. Тяните точку. При $p=0{,}665$ потеря $0{,}408$ ната, или $0{,}589$ бита, производная $-1{,}504$. Отмечены уверенный правильный ответ ($p=0{,}9$, штраф $0{,}105$) и уверенная ошибка ($p=0{,}1$, штраф $2{,}303$)."),
        ("callout", "intuition", "Что заметить", r"Уверенная ошибка ($p=0{,}1$) стоит в 22 раза больше уверенного правильного ответа ($p=0{,}9$). При $p=0{,}01$ штраф уже $4{,}605$ и растёт без предела, а квадратичная ошибка $(1-p)^2$ так и остаётся меньше единицы ($0{,}980$). Производная $-1/p$ неограниченно растёт по модулю при $p\to0$: чем хуже ответ, тем сильнее толчок."),
    ]),
    dict(id="anatomy", title="Формула по косточкам", blocks=[
        ("eq", r"\mathrm{CE}(y,\hat y)=-\sum_{k=1}^{K}y_k\ln\hat y_k"),
        ("symbols", [
            (r"y=(y_1,\dots,y_K)", r"истинное распределение; обычно one-hot: $y_c=1$ для правильного класса $c$ и $0$ для остальных;"),
            (r"\hat y_k", r"предсказанная вероятность класса $k$, как правило $\hat y=s=\operatorname{softmax}(z)$;"),
            (r"\ln", r"натуральный логарифм: CE измеряется в натах (nats); с $\log_2$ — в битах, $1$ нат $\approx1{,}443$ бита;"),
            (r"-", "логарифм вероятности отрицателен, минус делает потерю неотрицательной."),
        ]),
        ("p", r"Для one-hot метки в сумме выживает одно слагаемое. Подставив $s=\operatorname{softmax}(z)$, получаем формулу прямо через логиты:"),
        ("eq", r"\mathrm{CE}=-\ln s_c=-z_c+\ln\sum_{j=1}^{K}e^{z_j}=\operatorname{LSE}(z)-z_c"),
        ("p", r"Последняя форма — главная на практике: потеря считается без явного softmax. Для батча из $N$ примеров потери усредняют:"),
        ("eq", r"\mathcal L=-\frac1N\sum_{n=1}^{N}\ln s^{(n)}_{c_n}"),
        ("p", r"Пример шпаргалки — логиты $(2;\,1;\,0)$, правильный класс первый:"),
        ("table", HEADS, "TABLE", {"num": [1, 2, 3, 4, 5]}),
        ("p", r"Итог: $\mathrm{CE}\approx0{,}408$, градиент $s-y\approx(-0{,}335;\,0{,}245;\,0{,}090)$. Если бы правильным был третий класс, потеря была бы $-\ln0{,}090\approx2{,}408$ — модель уверенно ошиблась."),
        ("deep", "CE и максимальное правдоподобие", [
            ("p", r"Пусть модель с параметрами $\theta$ назначает классу $c_n$ вероятность $q_\theta(c_n\mid x_n)$. Правдоподобие выборки — произведение $\prod_n q_\theta(c_n\mid x_n)$. Логарифм превращает произведение в сумму, а смена знака — максимизацию в минимизацию:"),
            ("eq", r"\arg\max_\theta\prod_{n=1}^{N}q_\theta(c_n\mid x_n)=\arg\min_\theta\Bigl(-\frac1N\sum_{n=1}^{N}\ln q_\theta(c_n\mid x_n)\Bigr)=\arg\min_\theta\mathcal L"),
            ("p", r"Минимизировать среднюю CE — то же, что искать оценку максимального правдоподобия для категориального распределения. Поэтому CE — не произвольный выбор, а «родная» потеря вероятностного классификатора."),
        ]),
    ]),
    dict(id="information", title="Энтропия, кросс-энтропия и KL-дивергенция", blocks=[
        ("p", r"Название пришло из теории информации. Пусть события приходят из распределения $p$, а мы кодируем их, исходя из модели $q$. Тогда:"),
        ("eq", r"H(p)=-\sum_k p_k\ln p_k,\qquad H(p,q)=-\sum_k p_k\ln q_k,\qquad\mathrm{KL}(p\,\|\,q)=\sum_k p_k\ln\frac{p_k}{q_k}"),
        ("eq", r"H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)"),
        ("p", r"$H(p)$ — неустранимая неопределённость самих данных (энтропия), $\mathrm{KL}(p\,\|\,q)\ge0$ — штраф за то, что модель $q$ отличается от правды (неравенство Гиббса; равенство только при $q=p$). Поэтому минимум кросс-энтропии по $q$ достигается при $q=p$ и равен $H(p)$. Для one-hot метки $H(y)=0$, и CE совпадает с KL-дивергенцией."),
        ("viz", "cross-entropy-kl", {"p": [0.7, 0.2, 0.1], "q": [0.25, 0.5, 0.25]}, r"<b>Рисунок 2.</b> Цель $p$ (чёрная точка) и прогноз $q$ (красная) в симплексе трёх классов; обе точки можно тянуть. Заливка и линии уровня — $\mathrm{KL}(p\,\|\,q')$ для всех возможных прогнозов $q'$ (уровни $0{,}05$, $0{,}25$, $0{,}75$): светлее всего в самой точке $p$. Справа — разложение $H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)$. При $p=(0{,}7;\,0{,}2;\,0{,}1)$ и $q=(0{,}25;\,0{,}5;\,0{,}25)$: $H(p)\approx0{,}802$, $\mathrm{KL}\approx0{,}446$, $H(p,q)\approx1{,}248$ ната ($1{,}800$ бита). Положите $q$ на $p$ — KL исчезнет; утащите $p$ в вершину — исчезнет $H(p)$."),
        ("deep", "Почему KL ≥ 0", [
            ("p", r"По неравенству Йенсена для вогнутого логарифма (суммы — по $k$ с $p_k&gt;0$):"),
            ("eq", r"-\mathrm{KL}(p\,\|\,q)=\sum_k p_k\ln\frac{q_k}{p_k}\le\ln\sum_k p_k\frac{q_k}{p_k}=\ln\sum_{k:\,p_k>0}q_k\le\ln1=0"),
            ("p", r"Равенство — только когда $q_k=p_k$ для всех $k$."),
        ]),
        ("callout", "note", "Биты или наты", r"С $\log_2$ кросс-энтропия измеряется в битах — это буквально среднее число бит на событие при оптимальном коде, построенном по $q$. В машинном обучении берут натуральный логарифм: производные проще, а минимум тот же. Перевод: $1$ нат $=1/\ln2\approx1{,}443$ бита."),
    ]),
    dict(id="gradient", title="Производная: почему softmax + CE дают s − y", blocks=[
        ("p", r"Посчитаем градиент потери по логитам. Можно идти через матрицу Якоби softmax, но короче — через форму $\mathrm{CE}=\operatorname{LSE}(z)-z_c$: производная LSE — это softmax (см. страницу <a href='../softmax/'>softmax</a>), а производная $z_c$ по $z_k$ равна $y_k$."),
        ("eq", r"\frac{\partial\,\mathrm{CE}}{\partial z_k}=\frac{\partial\operatorname{LSE}(z)}{\partial z_k}-\frac{\partial z_c}{\partial z_k}=s_k-y_k"),
        ("deep", "Вывод через матрицу Якоби (цепное правило)", [
            ("p", r"Производная по вероятностям: $\partial\,\mathrm{CE}/\partial s_i=-y_i/s_i$. Якобиан softmax: $\partial s_i/\partial z_k=s_i(\delta_{ik}-s_k)$. По цепному правилу:"),
            ("eq", r"\frac{\partial\,\mathrm{CE}}{\partial z_k}=\sum_i\Bigl(-\frac{y_i}{s_i}\Bigr)s_i(\delta_{ik}-s_k)=-\sum_i y_i\delta_{ik}+s_k\sum_i y_i=s_k-y_k"),
            ("p", r"На последнем шаге использовано $\sum_i y_i=1$. Множители $s_i$ из якобиана сократились со знаменателями $1/s_i$ из логарифма — вся матрица схлопнулась в разность. Формула верна для любой цели $y$ с суммой 1, не только one-hot (например, при сглаживании меток)."),
        ]),
        ("p", "У этой формулы три важных следствия:"),
        ("ul", [
            r"<b>градиент ограничен</b>: каждая компонента $s_k-y_k$ лежит в $(-1;\,1)$, а их сумма равна 0 — правильный логит тянется вверх ровно настолько, насколько остальные в сумме тянутся вниз;",
            r"<b>нет насыщения на ошибке</b>: если модель уверенно ошибается ($s_c\to0$), градиент по правильному логиту стремится к $-1$, а не к нулю. Сравните с MSE поверх softmax, где множители из якобиана гасят градиент как раз тогда, когда ошибка велика (раздел <a href='#training'>про CE и MSE</a>);",
            r"<b>затухание на успехе</b>: когда $s\to y$, градиент стремится к 0 — хорошо выученные примеры почти не влияют на обучение.",
        ]),
        ("viz", "cross-entropy-gradient", {"z": [2, 1, 0], "k": 0, "eta": 1}, r"<b>Рисунок 3.</b> Один пример с логитами $(2;\,1;\,0)$ и правильным первым классом. Справа столбики — прогноз $s$, чёрные полки — цель $y$, стрелки и числа — $s_k-y_k$. Нажмите «Шаг»: логиты обновляются по правилу $z\leftarrow z-\eta(s-y)$ с $\eta=1$, и потеря падает: $0{,}408\to0{,}258\to0{,}187\to0{,}146$, после 10 шагов $0{,}058$. Сделайте правильным класс 3 — потеря станет $2{,}408$, а градиент $(0{,}665;\,0{,}245;\,-0{,}910)$."),
        ("deep", "Вторая производная: CE выпукла по логитам", [
            ("p", r"Продифференцируем $s_k-y_k$ ещё раз: гессиан CE по логитам равен якобиану softmax, $\nabla^2_z\,\mathrm{CE}=\operatorname{diag}(s)-ss^\top$. Эта матрица неотрицательно определена, поэтому CE — выпуклая функция логитов, а у softmax-регрессии $z=Wx+b$ потеря выпукла по $(W,b)$: плохих локальных минимумов нет. В направлении $\mathbf 1$ матрица вырождена — сдвиг всех логитов не меняет потерю."),
        ]),
    ]),
    dict(id="landscape", title="Ландшафт потерь в 3D", blocks=[
        ("p", r"Зафиксируем третий логит $z_3=0$ и нарисуем потерю как функцию двух других. Для правильного класса 1:"),
        ("eq", r"\mathrm{CE}(z_1,z_2)=\ln\bigl(e^{z_1}+e^{z_2}+1\bigr)-z_1=\ln\bigl(1+e^{z_2-z_1}+e^{-z_1}\bigr)"),
        ("p", r"Где $z_1$ намного больше и $z_2$, и нуля, обе экспоненты под логарифмом малы, и потеря близка к 0. Где первый класс проигрывает, потеря растёт почти линейно — примерно как $\max(z_2,0)-z_1$. Получается выпуклая «долина», которая плавно уходит вниз, но нуля не достигает."),
        ("viz", "cross-entropy-landscape", {"z": [2, 1], "k": 0}, r"<b>Рисунок 4.</b> Слева — поверхность $\mathrm{CE}(z_1,z_2,0)$ для выбранного правильного класса (её можно вращать). Справа — вид сверху: цвет и линии уровня — потеря, стрелки — антиградиент $-(s-y)$ по $z_1$ и $z_2$. Красную точку можно тянуть. «Пуск» запускает градиентный спуск по $z_1$, $z_2$ с шагом $0{,}8$ из точки $(2;\,1)$: потеря $0{,}408\to0{,}132$ за 5 шагов, $0{,}079$ за 10 и $0{,}013$ за 79, а точка всё уходит вправо-вниз — минимум недостижим."),
        ("callout", "warn", "Минимума нет", r"Для one-hot цели нижняя грань CE равна 0, но достигается она только при бесконечном отрыве правильного логита. Если модель может разделить обучающие данные идеально, CE продолжает уменьшаться за счёт роста логитов, и веса уходят в бесконечность. Это лечат регуляризацией весов, ранней остановкой и сглаживанием меток."),
    ]),
    dict(id="smoothing", title="Сглаживание меток", blocks=[
        ("p", r"Сглаживание меток (label smoothing) заменяет one-hot цель смесью с равномерным распределением:"),
        ("eq", r"y^{\mathrm{LS}}_k=(1-\varepsilon)\,y_k+\frac{\varepsilon}{K}"),
        ("p", r"Правильный класс получает $1-\varepsilon+\varepsilon/K$, каждый из остальных — $\varepsilon/K$. Теперь у потери есть настоящий минимум: градиент $s-y^{\mathrm{LS}}$ обнуляется, когда $s=y^{\mathrm{LS}}$. Если все неправильные логиты равны, а правильный опережает их на $m$, оптимальный отрыв конечен:"),
        ("eq", r"s_c=\frac{e^{m}}{e^{m}+K-1}=1-\varepsilon+\frac{\varepsilon}{K}\quad\Longrightarrow\quad m^{*}=\ln\Bigl(1+\frac{K(1-\varepsilon)}{\varepsilon}\Bigr)"),
        ("viz", "cross-entropy-smoothing", {"eps": 0.1, "K": 3}, r"<b>Рисунок 5.</b> Потеря и её производная как функции отрыва $m$ правильного логита (остальные $K-1$ логитов равны). Без сглаживания (пунктир) потеря монотонно убывает и стремится к 0 только при $m\to\infty$, производная всё время отрицательна. Со сглаживанием $\varepsilon=0{,}1$ при $K=3$ появляется минимум: $m^*=\ln28\approx3{,}332$, где вероятность правильного класса равна цели $0{,}9333$, а потеря — энтропии цели $H(y^{\mathrm{LS}})\approx0{,}291$. При $K=10$: $m^*\approx4{,}511$."),
        ("p", r"Сглаживание меток (Сегеди и др., 2016, Inception-v3) ограничивает рост логитов и обычно улучшает калибровку; оно стоит, например, в оригинальном Transformer с $\varepsilon=0{,}1$. Цена — модель больше никогда не уверена на 100%, а информация о сходстве классов в её логитах частично стирается, что может мешать дистилляции (Мюллер и др., 2019)."),
    ]),
    dict(id="training", title="CE против MSE: почему классификаторы учат на кросс-энтропии", blocks=[
        ("p", r"Почему бы не обучать классификатор квадратичной ошибкой $\|s-y\|^2$ между вероятностями и one-hot меткой? Сравним градиенты по логитам:"),
        ("eq", r"\frac{\partial\,\mathrm{CE}}{\partial z}=s-y,\qquad\frac{\partial\,\|s-y\|^2}{\partial z}=J^{\top}\,2(s-y)=2\,s\odot\bigl((s-y)-\langle s-y,\,s\rangle\,\mathbf 1\bigr)"),
        ("p", r"У MSE в градиенте стоит множитель $s$ из матрицы Якоби. Если модель уверенно ошибается — почти вся масса у одного неправильного класса, — градиент почти обнуляется: для маленьких $s_k$ мал множитель $s_k$, а для неправильного класса-фаворита почти нулевой оказывается скобка. Модель «не слышит» собственную грубую ошибку. В градиенте CE такого множителя нет."),
        ("viz", "cross-entropy-train", {}, r"<b>Рисунок 6.</b> Одни и те же данные и один и тот же «уверенно неправильный» старт: веса направлены на центры чужих классов, точность $3{,}3\%$. Две копии softmax-регрессии обучаются параллельно градиентным спуском с шагом $0{,}5$ — одна на CE, другая на MSE. Средняя норма градиента по логитам на старте: $1{,}3$ у CE и $0{,}13$ у MSE. Через 10 шагов точность $85{,}6\%$ против $5{,}6\%$, через 50 — $93{,}3\%$ против $25{,}6\%$; MSE подтягивается только к сотому шагу ($90{,}0\%$), а к двухсотому обе модели дают $95{,}6\%$."),
        ("callout", "note", "Когда квадратичную ошибку всё же используют", r"Квадратичная ошибка между вероятностями и меткой называется оценкой Брайера (Brier score) и полезна как <i>метрика</i> калибровки. Для обучения классификаторов почти всегда берут CE: она выпукла по логитам и не насыщается на ошибках."),
    ]),
    dict(id="llm", title="Языковые модели и перплексия", blocks=[
        ("p", r"Языковая модель на каждой позиции $t$ предсказывает распределение следующего токена по словарю из $V$ токенов (десятки тысяч). Это классификация на $V$ классов, и потеря — средняя кросс-энтропия по позициям:"),
        ("eq", r"\mathcal L=-\frac1T\sum_{t=1}^{T}\ln p_\theta(x_t\mid x_{<t}),\qquad\mathrm{PPL}=e^{\mathcal L}=\Bigl(\prod_{t=1}^{T}\frac{1}{p_\theta(x_t\mid x_{<t})}\Bigr)^{1/T}"),
        ("p", r"<b>Перплексия</b> — экспонента от CE, то есть среднее геометрическое величин $1/p_t$. Её читают как «эффективное число вариантов»: модель, которая всегда равномерно выбирает из $k$ токенов, имеет перплексию ровно $k$. Модель, ничего не знающая о языке (равномерное распределение по словарю), имеет $\mathcal L=\ln V$ и $\mathrm{PPL}=V$."),
        ("viz", "cross-entropy-perplexity", {"lambda": 1}, r"<b>Рисунок 7.</b> Потеря $-\ln p_t$ на каждом токене предложения (учебный пример: вероятности заданы вручную). Оранжевая линия — среднее, то есть CE; пунктир — $\ln V$ для словаря $V=50\,000$. При $\lambda=1$: $\mathrm{CE}\approx1{,}086$, перплексия $\approx2{,}963$ — в среднем модель колеблется между тремя вариантами; дороже всего первое слово ($p=0{,}05$, штраф $3{,}00$). Ползунок $\lambda$ умножает логиты: при $\lambda=0{,}5$ перплексия уже $\approx263{,}5$, при $\lambda=0$ распределение равномерное, $\mathrm{CE}=\ln50\,000\approx10{,}82$ и перплексия $50\,000$."),
        ("callout", "note", "Сравнивайте перплексии осторожно", r"Перплексия зависит от токенизатора: на одном и том же тексте модель с более крупными токенами делает меньше предсказаний, и каждое труднее. Сравнивать можно модели с одинаковым словарём на одних и тех же данных — или переходить к битам на символ или байт."),
    ]),
    dict(id="code", title="В коде", blocks=[
        ("p", r"Главное правило — считать CE по логитам через log-softmax: $\mathrm{CE}=\operatorname{LSE}(z)-z_c$. Путь «softmax, потом логарифм» на уверенных ошибках даёт $\ln0=-\infty$: для логитов $(0;\,800;\,0)$ и правильного первого класса наивный код возвращает <code>inf</code>, а устойчивый — точный ответ $800$."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "Чек-лист PyTorch", r"<code>F.cross_entropy</code> / <code>nn.CrossEntropyLoss</code> принимает <b>логиты</b> (без softmax!) и номера классов типа <code>long</code> — или вероятности той же формы, что и логиты. Полезные параметры: <code>label_smoothing</code>, <code>weight</code> (веса классов при дисбалансе), <code>ignore_index</code> (например, паддинг). Классы должны стоять во втором измерении, поэтому логиты формы $(B,T,V)$ проще всего превратить в $(BT,V)$ через <code>reshape</code>."),
    ]),
    dict(id="mistakes", title="Частые ошибки", blocks=[
        ("ol", [
            r"<b>Softmax перед <code>CrossEntropyLoss</code></b> — двойной softmax: вероятности зажаты, потеря не опускается до нуля, градиенты искажены. Подавайте логиты.",
            r"<b><code>np.log(softmax(z))</code> вместо log-softmax</b> — на уверенной ошибке вероятность округляется до 0, потеря становится <code>inf</code>, градиент — NaN. «Заплатка» <code>clip(p, 1e-7, 1)</code> спасает от бесконечности, но обрезает градиент; правильнее LSE.",
            r"<b>Путаница one-hot и номеров классов</b>. В Keras это разные функции: <code>categorical_crossentropy</code> ждёт one-hot, <code>sparse_categorical_crossentropy</code> — номера. В PyTorch номера должны иметь тип <code>long</code>, а вероятностные цели — ту же форму, что логиты.",
            r"<b>Сумма вместо среднего</b>. С <code>reduction='sum'</code> потеря и градиент растут с размером батча, и подобранный темп обучения перестаёт подходить.",
            r"<b>Дисбаланс классов без внимания</b>. CE усредняет по примерам, поэтому редкий класс почти не влияет на градиент. Помогают веса классов (<code>weight</code>) или <a href='../focal/'>Focal Loss</a>.",
            r"<b>Несопоставимые числа</b>: потери в натах и битах, перплексии моделей с разными токенизаторами.",
        ]),
    ]),
    dict(id="links", title="Связи с другими формулами", blocks=[
        ("ul", [
            r"<a href='../softmax/'>Softmax</a>: даёт вероятности $s$; вместе с CE — градиент $s-y$, а $\mathrm{CE}=\operatorname{LSE}(z)-z_c$.",
            r"<a href='../bce/'>BCE</a>: случай $K=2$ с одним выходом: $-\bigl[y\ln\hat y+(1-y)\ln(1-\hat y)\bigr]$.",
            r"<a href='../sigmoid/'>Сигмоида</a>: для двух классов softmax сводится к сигмоиде, и CE превращается в BCE.",
            r"<a href='../focal/'>Focal Loss</a>: $-(1-p_t)^\gamma\ln p_t$ — кросс-энтропия, ослабленная на лёгких примерах.",
            r"<a href='../mse/'>MSE</a>: поверх softmax насыщается на уверенных ошибках (см. раздел <a href='#training'>о сравнении</a>).",
            r"<a href='../adam/'>Adam</a>: оптимизатор, которым обычно минимизируют CE в глубоких сетях.",
        ]),
    ]),
    dict(id="summary", title="Итоги", blocks=[
        ("callout", "key", None, r"1) Для one-hot метки $\mathrm{CE}=-\ln s_c$ — удивление модели правильным ответом; среднее по данным — минус логарифм правдоподобия, делённый на $N$. 2) $H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)$: минимум по $q$ — при $q=p$. 3) С softmax градиент по логитам равен $s-y$: он ограничен, не насыщается на ошибках и исчезает на успехе; CE выпукла по логитам. 4) На one-hot целях минимум недостижим — логиты растут; сглаживание меток делает оптимум конечным. 5) Считайте CE по логитам через log-sum-exp; $e^{\mathrm{CE}}$ — перплексия."),
    ]),
    dict(id="quiz", title="Проверь себя", blocks=[
        ("quiz", [
            dict(q=r"Правильному классу модель дала вероятность $0{,}25$. Чему равна CE?", options=[r"$0{,}25$", r"$0{,}75$", r"$\approx1{,}386$", r"$\approx0{,}288$"], answer=2,
                 explain=r"$-\ln0{,}25=\ln4\approx1{,}386$ ната (ровно 2 бита)."),
            dict(q="Чему равен градиент CE по логитам, если вероятности получены softmax?", options=[r"$-y/s$", r"$s-y$", r"$\operatorname{diag}(s)-ss^\top$", r"$(s-y)^2$"], answer=1,
                 explain=r"$\mathrm{CE}=\operatorname{LSE}(z)-z_c$, а $\nabla\operatorname{LSE}=s$; $-y/s$ — это градиент по вероятностям, а не по логитам."),
            dict(q="Модель отвечает равномерно на 10 классах. Чему равны CE и перплексия?", options=[r"$0$ и $1$", r"$\ln10\approx2{,}303$ и $10$", r"$0{,}1$ и $10$", r"$1$ и $e$"], answer=1,
                 explain=r"Каждому классу — $0{,}1$, так что $\mathrm{CE}=-\ln0{,}1=\ln10$, а $\mathrm{PPL}=e^{\ln10}=10$."),
            dict(q=r"При каком прогнозе $q$ кросс-энтропия $H(p,q)$ минимальна?", options=[r"$q=p$", r"$q$ — one-hot вектор наиболее вероятного класса $p$", r"$q$ — равномерное распределение", "Минимума нет"], answer=0,
                 explain=r"$H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)$, а KL неотрицательна и равна нулю только при $q=p$."),
            dict(q=r"Сглаживание меток с $\varepsilon=0{,}1$ при $K=3$. К какой вероятности правильного класса стремится обучение?", options=[r"$1$", r"$0{,}9$", r"$\approx0{,}933$", r"$\approx0{,}967$"], answer=2,
                 explain=r"Цель для правильного класса $1-\varepsilon+\varepsilon/K=0{,}9+0{,}0333\approx0{,}933$; в этой точке $s-y=0$."),
        ]),
    ]),
],
"en": [
    dict(id="why", title="Why we need it", blocks=[
        ("p", r"A model has output class probabilities — say $(0.665,\,0.245,\,0.090)$ for “cat”, “dog”, “bird” — and the picture shows a cat. How good is that? We need one number that gets smaller as the probability of the correct answer grows, and that gradient descent can minimize. The standard answer is <b>categorical cross-entropy</b> (CE): here $\mathrm{CE}=-\ln0.665\approx0.408$."),
        ("p", "Where it appears:"),
        ("ul", [
            r"<b>training multi-class classifiers</b> — from logistic regression to ResNet and ViT: the last layer outputs logits, <a href='../softmax/'>softmax</a> turns them into probabilities, CE scores the answer;",
            r"<b>language models</b> — pre-training GPT, LLaMA, Qwen means minimizing the CE of the next token: the classes are vocabulary tokens, and $e^{\mathrm{CE}}$ is the famous perplexity;",
            r"<b>knowledge distillation</b> — the student minimizes CE against the teacher’s “soft” probabilities;",
            r"<b>statistics</b> — minimizing CE is equivalent to maximum likelihood for the categorical distribution;",
            r"<b>information theory</b> — CE is the mean code length when data come from a distribution $p$ but are encoded according to a model $q$.",
        ]),
        ("callout", "key", "The essentials in a minute", r"$\mathrm{CE}=-\sum_k y_k\ln\hat y_k$; for a one-hot label it is minus the log-probability of the correct class. A confident mistake is expensive: $-\ln0.1\approx2.303$ versus $-\ln0.9\approx0.105$. Together with softmax the gradient with respect to the logits is simply $s-y$, with no saturation. Cross-entropy = entropy + KL divergence, and $e^{\mathrm{CE}}$ is perplexity."),
    ]),
    dict(id="intuition", title="Intuition: a penalty for surprise", blocks=[
        ("p", r"Suppose the model announces its probabilities in advance and then learns the correct answer. If it gave the correct class probability $p$, its “surprise” is $-\ln p$: at $p=1$ there is no surprise, at $p=0.5$ it is $\ln2\approx0.693$, and as $p\to0$ it grows to infinity. Cross-entropy is the model’s mean surprise on the data."),
        ("p", r"Why a logarithm? First, it turns the product of probabilities of independent examples into a sum. Second, it rewards honesty: among penalties that depend only on the probability the model assigned to the outcome that happened, with three or more outcomes only the logarithmic one (up to a linear transformation) is minimized on average when the model reports its true probabilities."),
        ("viz", "cross-entropy-surprise", {"p": 0.665}, r"<b>Figure 1.</b> Top: the penalty $-\ln p$ (blue) and the squared error $(1-p)^2$ for comparison; bottom: their derivatives in $p$. Drag the point. At $p=0.665$ the loss is $0.408$ nats, or $0.589$ bits, and the derivative is $-1.504$. Marked are a confident right answer ($p=0.9$, penalty $0.105$) and a confident mistake ($p=0.1$, penalty $2.303$)."),
        ("callout", "intuition", "What to notice", r"A confident mistake ($p=0.1$) costs 22 times more than a confident right answer ($p=0.9$). At $p=0.01$ the penalty is already $4.605$ and grows without bound, while the squared error $(1-p)^2$ stays below one ($0.980$). The derivative $-1/p$ grows without bound in magnitude as $p\to0$: the worse the answer, the harder the push."),
    ]),
    dict(id="anatomy", title="The formula, bone by bone", blocks=[
        ("eq", r"\mathrm{CE}(y,\hat y)=-\sum_{k=1}^{K}y_k\ln\hat y_k"),
        ("symbols", [
            (r"y=(y_1,\dots,y_K)", r"the true distribution; usually one-hot: $y_c=1$ for the correct class $c$ and $0$ for the rest;"),
            (r"\hat y_k", r"the predicted probability of class $k$, usually $\hat y=s=\operatorname{softmax}(z)$;"),
            (r"\ln", r"the natural logarithm: CE is measured in nats; with $\log_2$, in bits, $1$ nat $\approx1.443$ bits;"),
            (r"-", "the log of a probability is negative; the minus makes the loss non-negative."),
        ]),
        ("p", r"For a one-hot label only one term of the sum survives. Substituting $s=\operatorname{softmax}(z)$ gives a formula directly in the logits:"),
        ("eq", r"\mathrm{CE}=-\ln s_c=-z_c+\ln\sum_{j=1}^{K}e^{z_j}=\operatorname{LSE}(z)-z_c"),
        ("p", r"The last form is the one that matters in practice: the loss is computed without an explicit softmax. For a batch of $N$ examples the losses are averaged:"),
        ("eq", r"\mathcal L=-\frac1N\sum_{n=1}^{N}\ln s^{(n)}_{c_n}"),
        ("p", r"The cheat sheet’s example — logits $(2,\,1,\,0)$, the correct class is the first:"),
        ("table", HEADS, "TABLE", {"num": [1, 2, 3, 4, 5]}),
        ("p", r"Result: $\mathrm{CE}\approx0.408$, gradient $s-y\approx(-0.335,\,0.245,\,0.090)$. Had the third class been correct, the loss would be $-\ln0.090\approx2.408$ — a confident mistake."),
        ("deep", "CE and maximum likelihood", [
            ("p", r"Let a model with parameters $\theta$ assign probability $q_\theta(c_n\mid x_n)$ to class $c_n$. The likelihood of the sample is the product $\prod_n q_\theta(c_n\mid x_n)$. The logarithm turns the product into a sum, and flipping the sign turns maximization into minimization:"),
            ("eq", r"\arg\max_\theta\prod_{n=1}^{N}q_\theta(c_n\mid x_n)=\arg\min_\theta\Bigl(-\frac1N\sum_{n=1}^{N}\ln q_\theta(c_n\mid x_n)\Bigr)=\arg\min_\theta\mathcal L"),
            ("p", r"Minimizing the mean CE is the same as finding the maximum-likelihood estimate for the categorical distribution. So CE is not an arbitrary choice but the “native” loss of a probabilistic classifier."),
        ]),
    ]),
    dict(id="information", title="Entropy, cross-entropy and KL divergence", blocks=[
        ("p", r"The name comes from information theory. Let events come from a distribution $p$ while we encode them according to a model $q$. Then:"),
        ("eq", r"H(p)=-\sum_k p_k\ln p_k,\qquad H(p,q)=-\sum_k p_k\ln q_k,\qquad\mathrm{KL}(p\,\|\,q)=\sum_k p_k\ln\frac{p_k}{q_k}"),
        ("eq", r"H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)"),
        ("p", r"$H(p)$ is the irreducible uncertainty of the data themselves (the entropy), and $\mathrm{KL}(p\,\|\,q)\ge0$ is the penalty for the model $q$ differing from the truth (Gibbs’ inequality; equality only when $q=p$). So the minimum of cross-entropy over $q$ is reached at $q=p$ and equals $H(p)$. For a one-hot label $H(y)=0$, and CE coincides with the KL divergence."),
        ("viz", "cross-entropy-kl", {"p": [0.7, 0.2, 0.1], "q": [0.25, 0.5, 0.25]}, r"<b>Figure 2.</b> The target $p$ (black point) and the prediction $q$ (red) in the three-class simplex; both points can be dragged. The shading and level lines show $\mathrm{KL}(p\,\|\,q')$ for every possible prediction $q'$ (levels $0.05$, $0.25$, $0.75$): it is lightest at $p$ itself. On the right, the split $H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)$. With $p=(0.7,\,0.2,\,0.1)$ and $q=(0.25,\,0.5,\,0.25)$: $H(p)\approx0.802$, $\mathrm{KL}\approx0.446$, $H(p,q)\approx1.248$ nats ($1.800$ bits). Put $q$ on $p$ and the KL vanishes; drag $p$ to a vertex and $H(p)$ vanishes."),
        ("deep", "Why KL ≥ 0", [
            ("p", r"By Jensen’s inequality for the concave logarithm (sums over $k$ with $p_k&gt;0$):"),
            ("eq", r"-\mathrm{KL}(p\,\|\,q)=\sum_k p_k\ln\frac{q_k}{p_k}\le\ln\sum_k p_k\frac{q_k}{p_k}=\ln\sum_{k:\,p_k>0}q_k\le\ln1=0"),
            ("p", r"Equality holds only when $q_k=p_k$ for every $k$."),
        ]),
        ("callout", "note", "Bits or nats", r"With $\log_2$ cross-entropy is measured in bits — literally the mean number of bits per event under the optimal code built from $q$. Machine learning uses the natural logarithm: derivatives are simpler and the minimum is the same. Conversion: $1$ nat $=1/\ln2\approx1.443$ bits."),
    ]),
    dict(id="gradient", title="The derivative: why softmax + CE give s − y", blocks=[
        ("p", r"Let us compute the gradient of the loss with respect to the logits. One can go through the softmax Jacobian, but the form $\mathrm{CE}=\operatorname{LSE}(z)-z_c$ is shorter: the derivative of LSE is softmax (see the <a href='../softmax/'>softmax</a> page), and the derivative of $z_c$ with respect to $z_k$ is $y_k$."),
        ("eq", r"\frac{\partial\,\mathrm{CE}}{\partial z_k}=\frac{\partial\operatorname{LSE}(z)}{\partial z_k}-\frac{\partial z_c}{\partial z_k}=s_k-y_k"),
        ("deep", "Derivation through the Jacobian (chain rule)", [
            ("p", r"The derivative with respect to the probabilities: $\partial\,\mathrm{CE}/\partial s_i=-y_i/s_i$. The softmax Jacobian: $\partial s_i/\partial z_k=s_i(\delta_{ik}-s_k)$. By the chain rule:"),
            ("eq", r"\frac{\partial\,\mathrm{CE}}{\partial z_k}=\sum_i\Bigl(-\frac{y_i}{s_i}\Bigr)s_i(\delta_{ik}-s_k)=-\sum_i y_i\delta_{ik}+s_k\sum_i y_i=s_k-y_k"),
            ("p", r"The last step uses $\sum_i y_i=1$. The factors $s_i$ from the Jacobian cancel the denominators $1/s_i$ from the logarithm — the whole matrix collapses into a difference. The formula holds for any target $y$ summing to 1, not only one-hot (for example, with label smoothing)."),
        ]),
        ("p", "This formula has three important consequences:"),
        ("ul", [
            r"<b>the gradient is bounded</b>: every component $s_k-y_k$ lies in $(-1,\,1)$, and they sum to 0 — the correct logit is pulled up exactly as much as the others together are pulled down;",
            r"<b>no saturation on mistakes</b>: if the model is confidently wrong ($s_c\to0$), the gradient on the correct logit tends to $-1$, not to zero. Compare with MSE on top of softmax, where the Jacobian factors kill the gradient precisely when the error is large (see the section <a href='#training'>on CE and MSE</a>);",
            r"<b>fading on success</b>: as $s\to y$ the gradient tends to 0 — well-learned examples barely affect training.",
        ]),
        ("viz", "cross-entropy-gradient", {"z": [2, 1, 0], "k": 0, "eta": 1}, r"<b>Figure 3.</b> One example with logits $(2,\,1,\,0)$ and the first class correct. On the right the bars are the prediction $s$, the black shelves the target $y$, the arrows and numbers $s_k-y_k$. Press “Step”: the logits are updated by $z\leftarrow z-\eta(s-y)$ with $\eta=1$, and the loss falls: $0.408\to0.258\to0.187\to0.146$, and after 10 steps $0.058$. Make class 3 the correct one — the loss becomes $2.408$ and the gradient $(0.665,\,0.245,\,-0.910)$."),
        ("deep", "The second derivative: CE is convex in the logits", [
            ("p", r"Differentiate $s_k-y_k$ once more: the Hessian of CE in the logits equals the softmax Jacobian, $\nabla^2_z\,\mathrm{CE}=\operatorname{diag}(s)-ss^\top$. This matrix is positive semi-definite, so CE is a convex function of the logits, and for softmax regression $z=Wx+b$ the loss is convex in $(W,b)$: there are no bad local minima. In the direction $\mathbf 1$ the matrix is singular — shifting all logits does not change the loss."),
        ]),
    ]),
    dict(id="landscape", title="The loss landscape in 3D", blocks=[
        ("p", r"Fix the third logit $z_3=0$ and draw the loss as a function of the other two. For correct class 1:"),
        ("eq", r"\mathrm{CE}(z_1,z_2)=\ln\bigl(e^{z_1}+e^{z_2}+1\bigr)-z_1=\ln\bigl(1+e^{z_2-z_1}+e^{-z_1}\bigr)"),
        ("p", r"Where $z_1$ is much larger than both $z_2$ and zero, both exponentials under the logarithm are small and the loss is close to 0. Where the first class loses, the loss grows almost linearly — roughly as $\max(z_2,0)-z_1$. The result is a convex “valley” that slopes gently down but never reaches zero."),
        ("viz", "cross-entropy-landscape", {"z": [2, 1], "k": 0}, r"<b>Figure 4.</b> On the left, the surface $\mathrm{CE}(z_1,z_2,0)$ for the chosen correct class (it can be rotated). On the right, the top view: colour and level lines show the loss, the arrows the anti-gradient $-(s-y)$ in $z_1$ and $z_2$. The red point can be dragged. “Play” runs gradient descent on $z_1$, $z_2$ with step $0.8$ from the point $(2,\,1)$: the loss goes $0.408\to0.132$ in 5 steps, $0.079$ in 10 and $0.013$ in 79, while the point keeps moving right and down — the minimum is out of reach."),
        ("callout", "warn", "There is no minimum", r"For a one-hot target the infimum of CE is 0, but it is reached only with an infinite margin of the correct logit. If a model can separate the training data perfectly, CE keeps decreasing as the logits grow, and the weights run off to infinity. The cures are weight regularization, early stopping and label smoothing."),
    ]),
    dict(id="smoothing", title="Label smoothing", blocks=[
        ("p", r"Label smoothing replaces the one-hot target with a mixture with the uniform distribution:"),
        ("eq", r"y^{\mathrm{LS}}_k=(1-\varepsilon)\,y_k+\frac{\varepsilon}{K}"),
        ("p", r"The correct class gets $1-\varepsilon+\varepsilon/K$, each of the others $\varepsilon/K$. Now the loss has a genuine minimum: the gradient $s-y^{\mathrm{LS}}$ vanishes when $s=y^{\mathrm{LS}}$. If all wrong logits are equal and the correct one is ahead of them by $m$, the optimal margin is finite:"),
        ("eq", r"s_c=\frac{e^{m}}{e^{m}+K-1}=1-\varepsilon+\frac{\varepsilon}{K}\quad\Longrightarrow\quad m^{*}=\ln\Bigl(1+\frac{K(1-\varepsilon)}{\varepsilon}\Bigr)"),
        ("viz", "cross-entropy-smoothing", {"eps": 0.1, "K": 3}, r"<b>Figure 5.</b> The loss and its derivative as functions of the margin $m$ of the correct logit (the other $K-1$ logits are equal). Without smoothing (dashed) the loss decreases monotonically and tends to 0 only as $m\to\infty$; the derivative is always negative. With smoothing $\varepsilon=0.1$ and $K=3$ a minimum appears: $m^*=\ln28\approx3.332$, where the probability of the correct class equals the target $0.9333$ and the loss equals the target’s entropy $H(y^{\mathrm{LS}})\approx0.291$. For $K=10$: $m^*\approx4.511$."),
        ("p", r"Label smoothing (Szegedy et al., 2016, Inception-v3) limits the growth of the logits and usually improves calibration; it is used, for example, in the original Transformer with $\varepsilon=0.1$. The price: the model is never 100% sure any more, and the information about class similarity in its logits is partly erased, which can hurt distillation (Müller et al., 2019)."),
    ]),
    dict(id="training", title="CE versus MSE: why classifiers are trained on cross-entropy", blocks=[
        ("p", r"Why not train a classifier with the squared error $\|s-y\|^2$ between the probabilities and the one-hot label? Compare the gradients with respect to the logits:"),
        ("eq", r"\frac{\partial\,\mathrm{CE}}{\partial z}=s-y,\qquad\frac{\partial\,\|s-y\|^2}{\partial z}=J^{\top}\,2(s-y)=2\,s\odot\bigl((s-y)-\langle s-y,\,s\rangle\,\mathbf 1\bigr)"),
        ("p", r"The MSE gradient carries a factor $s$ from the Jacobian. If the model is confidently wrong — almost all the mass sits on one wrong class — the gradient nearly vanishes: for small $s_k$ the factor $s_k$ is small, and for the favourite wrong class the bracket is almost zero. The model does not “hear” its own gross mistake. The CE gradient has no such factor."),
        ("viz", "cross-entropy-train", {}, r"<b>Figure 6.</b> The same data and the same “confidently wrong” start: the weights point at the centres of other classes, accuracy $3.3\%$. Two copies of softmax regression train in parallel with gradient descent, step $0.5$ — one on CE, the other on MSE. The mean gradient norm in the logits at the start: $1.3$ for CE and $0.13$ for MSE. After 10 steps the accuracy is $85.6\%$ versus $5.6\%$, after 50 it is $93.3\%$ versus $25.6\%$; MSE catches up only by step 100 ($90.0\%$), and by step 200 both models reach $95.6\%$."),
        ("callout", "note", "When the squared error is still used", r"The squared error between probabilities and the label is called the Brier score and is useful as a calibration <i>metric</i>. For training classifiers CE is almost always the choice: it is convex in the logits and does not saturate on mistakes."),
    ]),
    dict(id="llm", title="Language models and perplexity", blocks=[
        ("p", r"At every position $t$ a language model predicts the distribution of the next token over a vocabulary of $V$ tokens (tens of thousands). This is classification into $V$ classes, and the loss is the mean cross-entropy over positions:"),
        ("eq", r"\mathcal L=-\frac1T\sum_{t=1}^{T}\ln p_\theta(x_t\mid x_{<t}),\qquad\mathrm{PPL}=e^{\mathcal L}=\Bigl(\prod_{t=1}^{T}\frac{1}{p_\theta(x_t\mid x_{<t})}\Bigr)^{1/T}"),
        ("p", r"<b>Perplexity</b> is the exponential of CE, i.e. the geometric mean of the values $1/p_t$. It reads as an “effective number of choices”: a model that always picks uniformly among $k$ tokens has perplexity exactly $k$. A model that knows nothing about the language (uniform over the vocabulary) has $\mathcal L=\ln V$ and $\mathrm{PPL}=V$."),
        ("viz", "cross-entropy-perplexity", {"lambda": 1}, r"<b>Figure 7.</b> The loss $-\ln p_t$ on every token of a sentence (a teaching example: the probabilities are set by hand). The orange line is the mean, i.e. CE; the dashed line is $\ln V$ for a vocabulary of $V=50{,}000$. At $\lambda=1$: $\mathrm{CE}\approx1.086$, perplexity $\approx2.963$ — on average the model hesitates between three options; the first word costs most ($p=0.05$, penalty $3.00$). The slider $\lambda$ multiplies the logits: at $\lambda=0.5$ the perplexity is already $\approx263.5$, at $\lambda=0$ the distribution is uniform, $\mathrm{CE}=\ln50{,}000\approx10.82$ and the perplexity is $50{,}000$."),
        ("callout", "note", "Compare perplexities with care", r"Perplexity depends on the tokenizer: on the same text a model with larger tokens makes fewer predictions, and each one is harder. Only models with the same vocabulary on the same data can be compared — or switch to bits per character or byte."),
    ]),
    dict(id="code", title="In code", blocks=[
        ("p", r"The main rule is to compute CE from the logits through log-softmax: $\mathrm{CE}=\operatorname{LSE}(z)-z_c$. The route “softmax, then logarithm” gives $\ln0=-\infty$ on confident mistakes: for logits $(0,\,800,\,0)$ and the first class correct, naive code returns <code>inf</code>, while the stable one returns the exact answer $800$."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "A PyTorch checklist", r"<code>F.cross_entropy</code> / <code>nn.CrossEntropyLoss</code> takes <b>logits</b> (no softmax!) and class indices of type <code>long</code> — or probabilities of the same shape as the logits. Useful parameters: <code>label_smoothing</code>, <code>weight</code> (class weights for imbalance), <code>ignore_index</code> (for example, padding). Classes must sit in the second dimension, so logits of shape $(B,T,V)$ are easiest to turn into $(BT,V)$ with <code>reshape</code>."),
    ]),
    dict(id="mistakes", title="Common mistakes", blocks=[
        ("ol", [
            r"<b>A softmax before <code>CrossEntropyLoss</code></b> — a double softmax: the probabilities are squeezed, the loss cannot reach zero, the gradients are distorted. Pass logits.",
            r"<b><code>np.log(softmax(z))</code> instead of log-softmax</b> — on a confident mistake the probability rounds to 0, the loss becomes <code>inf</code> and the gradient NaN. The “patch” <code>clip(p, 1e-7, 1)</code> saves you from infinity but cuts off the gradient; LSE is the right way.",
            r"<b>Mixing up one-hot and class indices</b>. In Keras these are different functions: <code>categorical_crossentropy</code> expects one-hot, <code>sparse_categorical_crossentropy</code> expects indices. In PyTorch indices must be <code>long</code>, and probability targets must have the same shape as the logits.",
            r"<b>Sum instead of mean</b>. With <code>reduction='sum'</code> the loss and gradient grow with the batch size, and a tuned learning rate stops fitting.",
            r"<b>Ignoring class imbalance</b>. CE averages over examples, so a rare class barely affects the gradient. Class weights (<code>weight</code>) or <a href='../focal/'>Focal Loss</a> help.",
            r"<b>Incomparable numbers</b>: losses in nats and in bits, perplexities of models with different tokenizers.",
        ]),
    ]),
    dict(id="links", title="Links to other formulas", blocks=[
        ("ul", [
            r"<a href='../softmax/'>Softmax</a>: gives the probabilities $s$; together with CE, the gradient $s-y$, and $\mathrm{CE}=\operatorname{LSE}(z)-z_c$.",
            r"<a href='../bce/'>BCE</a>: the case $K=2$ with one output: $-\bigl[y\ln\hat y+(1-y)\ln(1-\hat y)\bigr]$.",
            r"<a href='../sigmoid/'>Sigmoid</a>: for two classes softmax reduces to the sigmoid, and CE turns into BCE.",
            r"<a href='../focal/'>Focal Loss</a>: $-(1-p_t)^\gamma\ln p_t$ — cross-entropy damped on easy examples.",
            r"<a href='../mse/'>MSE</a>: on top of softmax it saturates on confident mistakes (see the section <a href='#training'>on the comparison</a>).",
            r"<a href='../adam/'>Adam</a>: the optimizer usually used to minimize CE in deep networks.",
        ]),
    ]),
    dict(id="summary", title="Summary", blocks=[
        ("callout", "key", None, r"1) For a one-hot label $\mathrm{CE}=-\ln s_c$ — the model’s surprise at the correct answer; its mean over the data is minus the log-likelihood divided by $N$. 2) $H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)$: the minimum over $q$ is at $q=p$. 3) With softmax the gradient in the logits is $s-y$: bounded, not saturating on mistakes and vanishing on success; CE is convex in the logits. 4) With one-hot targets the minimum is out of reach — the logits grow; label smoothing makes the optimum finite. 5) Compute CE from the logits via log-sum-exp; $e^{\mathrm{CE}}$ is perplexity."),
    ]),
    dict(id="quiz", title="Check yourself", blocks=[
        ("quiz", [
            dict(q=r"The model gave the correct class probability $0.25$. What is the CE?", options=[r"$0.25$", r"$0.75$", r"$\approx1.386$", r"$\approx0.288$"], answer=2,
                 explain=r"$-\ln0.25=\ln4\approx1.386$ nats (exactly 2 bits)."),
            dict(q="What is the gradient of CE with respect to the logits when the probabilities come from softmax?", options=[r"$-y/s$", r"$s-y$", r"$\operatorname{diag}(s)-ss^\top$", r"$(s-y)^2$"], answer=1,
                 explain=r"$\mathrm{CE}=\operatorname{LSE}(z)-z_c$ and $\nabla\operatorname{LSE}=s$; $-y/s$ is the gradient with respect to the probabilities, not the logits."),
            dict(q="A model answers uniformly over 10 classes. What are its CE and perplexity?", options=[r"$0$ and $1$", r"$\ln10\approx2.303$ and $10$", r"$0.1$ and $10$", r"$1$ and $e$"], answer=1,
                 explain=r"Each class gets $0.1$, so $\mathrm{CE}=-\ln0.1=\ln10$ and $\mathrm{PPL}=e^{\ln10}=10$."),
            dict(q=r"For which prediction $q$ is the cross-entropy $H(p,q)$ smallest?", options=[r"$q=p$", r"$q$ is the one-hot vector of the most likely class of $p$", r"$q$ is uniform", "There is no minimum"], answer=0,
                 explain=r"$H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)$, and KL is non-negative and zero only when $q=p$."),
            dict(q=r"Label smoothing with $\varepsilon=0.1$ and $K=3$. What probability of the correct class does training tend to?", options=[r"$1$", r"$0.9$", r"$\approx0.933$", r"$\approx0.967$"], answer=2,
                 explain=r"The target for the correct class is $1-\varepsilon+\varepsilon/K=0.9+0.0333\approx0.933$; at that point $s-y=0$."),
        ]),
    ]),
],
"uz": [
    dict(id="why", title="U nima uchun kerak", blocks=[
        ("p", r"Model sinflar ehtimolliklarini chiqardi — masalan, «mushuk», «it», «qush» uchun $(0{,}665;\,0{,}245;\,0{,}090)$, — rasmda esa mushuk. Bu qanchalik yaxshi? Bitta son kerak: to‘g‘ri javob ehtimolligi qancha katta bo‘lsa, u shuncha kichik bo‘lsin va uni gradiyentli tushish bilan minimallashtirish mumkin bo‘lsin. Standart javob — <b>kategorial kross-entropiya</b> (categorical cross-entropy, CE): bu yerda $\mathrm{CE}=-\ln0{,}665\approx0{,}408$."),
        ("p", "U qayerda uchraydi:"),
        ("ul", [
            r"<b>ko‘p sinfli klassifikatorlarni o‘qitish</b> — logistik regressiyadan ResNet va ViT’gacha: oxirgi qatlam logitlarni chiqaradi, <a href='../softmax/'>softmax</a> ularni ehtimolliklarga aylantiradi, CE javobni baholaydi;",
            r"<b>til modellari</b> — GPT, LLaMA, Qwen’ni oldindan o‘qitish — keyingi token CE sini minimallashtirish: sinflar — lug‘at tokenlari, $e^{\mathrm{CE}}$ esa mashhur perpleksiya;",
            r"<b>bilimlar distillyatsiyasi</b> — o‘quvchi o‘qituvchining «yumshoq» ehtimolliklarigacha bo‘lgan CE ni minimallashtiradi;",
            r"<b>statistika</b> — CE ni minimallashtirish kategorial taqsimot uchun maksimal haqqoniylik usuliga teng kuchli;",
            r"<b>axborot nazariyasi</b> — ma’lumotlar $p$ taqsimotdan kelib, $q$ model bo‘yicha kodlansa, CE kodning o‘rtacha uzunligiga teng.",
        ]),
        ("callout", "key", "Bir daqiqada asosiysi", r"$\mathrm{CE}=-\sum_k y_k\ln\hat y_k$; one-hot belgi uchun bu to‘g‘ri sinf ehtimolligining minus logarifmi. Ishonchli xato qimmatga tushadi: $-\ln0{,}1\approx2{,}303$, $-\ln0{,}9\approx0{,}105$ ga qarshi. Softmax bilan juftlikda logitlar bo‘yicha gradiyent shunchaki $s-y$, to‘yinishsiz. Kross-entropiya = entropiya + KL-divergensiya, $e^{\mathrm{CE}}$ esa perpleksiya."),
    ]),
    dict(id="intuition", title="Intuitsiya: hayrat uchun jarima", blocks=[
        ("p", r"Model ehtimolliklarni oldindan e’lon qiladi, keyin to‘g‘ri javobni bilib oladi, deylik. Agar u to‘g‘ri sinfga $p$ ehtimollik bergan bo‘lsa, uning «hayrati» $-\ln p$ ga teng: $p=1$ da hayrat yo‘q, $p=0{,}5$ da u $\ln2\approx0{,}693$, $p\to0$ da esa cheksizlikkacha o‘sadi. Kross-entropiya — modelning ma’lumotlardagi o‘rtacha hayrati."),
        ("p", r"Nega aynan logarifm? Birinchidan, u mustaqil misollar ehtimolliklari ko‘paytmasini yig‘indiga aylantiradi. Ikkinchidan, u halollikni rag‘batlantiradi: faqat model sodir bo‘lgan natijaga bergan ehtimollikka bog‘liq jarimalar orasida uch va undan ortiq natijada faqat logarifmik jarima (chiziqli almashtirish aniqligida) model o‘zining haqiqiy ehtimolliklarini aytganda o‘rtacha minimal bo‘ladi."),
        ("viz", "cross-entropy-surprise", {"p": 0.665}, r"<b>Rasm 1.</b> Yuqorida — $-\ln p$ jarima (ko‘k) va taqqoslash uchun $(1-p)^2$ kvadratik xato; pastda — ularning $p$ bo‘yicha hosilalari. Nuqtani torting. $p=0{,}665$ da yo‘qotish $0{,}408$ nat yoki $0{,}589$ bit, hosila $-1{,}504$. Ishonchli to‘g‘ri javob ($p=0{,}9$, jarima $0{,}105$) va ishonchli xato ($p=0{,}1$, jarima $2{,}303$) belgilangan."),
        ("callout", "intuition", "Nimaga e’tibor berish kerak", r"Ishonchli xato ($p=0{,}1$) ishonchli to‘g‘ri javobdan ($p=0{,}9$) 22 marta qimmat. $p=0{,}01$ da jarima allaqachon $4{,}605$ va chegarasiz o‘sadi, $(1-p)^2$ kvadratik xato esa birdan kichikligicha qoladi ($0{,}980$). $-1/p$ hosila $p\to0$ da modul bo‘yicha chegarasiz o‘sadi: javob qancha yomon bo‘lsa, turtki shuncha kuchli."),
    ]),
    dict(id="anatomy", title="Formula mayda detallarigacha", blocks=[
        ("eq", r"\mathrm{CE}(y,\hat y)=-\sum_{k=1}^{K}y_k\ln\hat y_k"),
        ("symbols", [
            (r"y=(y_1,\dots,y_K)", r"haqiqiy taqsimot; odatda one-hot: to‘g‘ri $c$ sinf uchun $y_c=1$, qolganlari uchun $0$;"),
            (r"\hat y_k", r"$k$-sinfning bashorat qilingan ehtimolligi, odatda $\hat y=s=\operatorname{softmax}(z)$;"),
            (r"\ln", r"natural logarifm: CE natlarda (nats) o‘lchanadi; $\log_2$ bilan — bitlarda, $1$ nat $\approx1{,}443$ bit;"),
            (r"-", "ehtimollik logarifmi manfiy, minus yo‘qotishni nomanfiy qiladi."),
        ]),
        ("p", r"One-hot belgida yig‘indidan bitta qo‘shiluvchi qoladi. $s=\operatorname{softmax}(z)$ ni qo‘yib, to‘g‘ridan-to‘g‘ri logitlar orqali formula olamiz:"),
        ("eq", r"\mathrm{CE}=-\ln s_c=-z_c+\ln\sum_{j=1}^{K}e^{z_j}=\operatorname{LSE}(z)-z_c"),
        ("p", r"Oxirgi ko‘rinish amalda asosiysi: yo‘qotish aniq softmax’siz hisoblanadi. $N$ ta misoldan iborat batch uchun yo‘qotishlar o‘rtachalanadi:"),
        ("eq", r"\mathcal L=-\frac1N\sum_{n=1}^{N}\ln s^{(n)}_{c_n}"),
        ("p", r"Qo‘llanmadagi misol — $(2;\,1;\,0)$ logitlar, to‘g‘ri sinf birinchisi:"),
        ("table", HEADS, "TABLE", {"num": [1, 2, 3, 4, 5]}),
        ("p", r"Natija: $\mathrm{CE}\approx0{,}408$, gradiyent $s-y\approx(-0{,}335;\,0{,}245;\,0{,}090)$. Agar uchinchi sinf to‘g‘ri bo‘lganda, yo‘qotish $-\ln0{,}090\approx2{,}408$ bo‘lardi — model ishonch bilan xato qilgan."),
        ("deep", "CE va maksimal haqqoniylik", [
            ("p", r"$\theta$ parametrli model $c_n$ sinfga $q_\theta(c_n\mid x_n)$ ehtimollik bersin. Tanlanma haqqoniyligi — $\prod_n q_\theta(c_n\mid x_n)$ ko‘paytma. Logarifm ko‘paytmani yig‘indiga, ishorani almashtirish esa maksimallashtirishni minimallashtirishga aylantiradi:"),
            ("eq", r"\arg\max_\theta\prod_{n=1}^{N}q_\theta(c_n\mid x_n)=\arg\min_\theta\Bigl(-\frac1N\sum_{n=1}^{N}\ln q_\theta(c_n\mid x_n)\Bigr)=\arg\min_\theta\mathcal L"),
            ("p", r"O‘rtacha CE ni minimallashtirish — kategorial taqsimot uchun maksimal haqqoniylik bahosini izlash bilan bir xil. Shuning uchun CE ixtiyoriy tanlov emas, balki ehtimoliy klassifikatorning «tug‘ma» yo‘qotishi."),
        ]),
    ]),
    dict(id="information", title="Entropiya, kross-entropiya va KL-divergensiya", blocks=[
        ("p", r"Nom axborot nazariyasidan kelgan. Hodisalar $p$ taqsimotdan kelsin, biz esa ularni $q$ modelga asoslanib kodlaylik. U holda:"),
        ("eq", r"H(p)=-\sum_k p_k\ln p_k,\qquad H(p,q)=-\sum_k p_k\ln q_k,\qquad\mathrm{KL}(p\,\|\,q)=\sum_k p_k\ln\frac{p_k}{q_k}"),
        ("eq", r"H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)"),
        ("p", r"$H(p)$ — ma’lumotlarning o‘zidagi yo‘qotib bo‘lmaydigan noaniqlik (entropiya), $\mathrm{KL}(p\,\|\,q)\ge0$ — $q$ modelning haqiqatdan farq qilgani uchun jarima (Gibbs tengsizligi; tenglik faqat $q=p$ da). Shuning uchun kross-entropiyaning $q$ bo‘yicha minimumiga $q=p$ da erishiladi va u $H(p)$ ga teng. One-hot belgi uchun $H(y)=0$ va CE KL-divergensiya bilan ustma-ust tushadi."),
        ("viz", "cross-entropy-kl", {"p": [0.7, 0.2, 0.1], "q": [0.25, 0.5, 0.25]}, r"<b>Rasm 2.</b> Uch sinfli simpleksda maqsad $p$ (qora nuqta) va bashorat $q$ (qizil); ikkala nuqtani ham surish mumkin. Bo‘yoq va sath chiziqlari — barcha mumkin bo‘lgan $q'$ bashoratlar uchun $\mathrm{KL}(p\,\|\,q')$ ($0{,}05$, $0{,}25$, $0{,}75$ sathlar): eng och rang $p$ nuqtaning o‘zida. O‘ngda — $H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)$ yoyilmasi. $p=(0{,}7;\,0{,}2;\,0{,}1)$ va $q=(0{,}25;\,0{,}5;\,0{,}25)$ da: $H(p)\approx0{,}802$, $\mathrm{KL}\approx0{,}446$, $H(p,q)\approx1{,}248$ nat ($1{,}800$ bit). $q$ ni $p$ ustiga qo‘ying — KL yo‘qoladi; $p$ ni uchga suring — $H(p)$ yo‘qoladi."),
        ("deep", "Nega KL ≥ 0", [
            ("p", r"Botiq logarifm uchun Iensen tengsizligi bo‘yicha (yig‘indilar $p_k&gt;0$ bo‘lgan $k$ lar bo‘yicha):"),
            ("eq", r"-\mathrm{KL}(p\,\|\,q)=\sum_k p_k\ln\frac{q_k}{p_k}\le\ln\sum_k p_k\frac{q_k}{p_k}=\ln\sum_{k:\,p_k>0}q_k\le\ln1=0"),
            ("p", r"Tenglik faqat barcha $k$ uchun $q_k=p_k$ bo‘lganda bajariladi."),
        ]),
        ("callout", "note", "Bitlar yoki natlar", r"$\log_2$ bilan kross-entropiya bitlarda o‘lchanadi — bu $q$ bo‘yicha qurilgan optimal kodda har bir hodisaga to‘g‘ri keladigan o‘rtacha bitlar soni. Mashinali o‘qitishda natural logarifm olinadi: hosilalar soddaroq, minimum esa o‘sha. O‘tkazish: $1$ nat $=1/\ln2\approx1{,}443$ bit."),
    ]),
    dict(id="gradient", title="Hosila: nega softmax + CE s − y ni beradi", blocks=[
        ("p", r"Yo‘qotishning logitlar bo‘yicha gradiyentini hisoblaylik. Softmax’ning Yakobi matritsasi orqali borish mumkin, lekin $\mathrm{CE}=\operatorname{LSE}(z)-z_c$ ko‘rinishi orqali qisqaroq: LSE ning hosilasi — softmax (<a href='../softmax/'>softmax</a> sahifasiga qarang), $z_c$ ning $z_k$ bo‘yicha hosilasi esa $y_k$ ga teng."),
        ("eq", r"\frac{\partial\,\mathrm{CE}}{\partial z_k}=\frac{\partial\operatorname{LSE}(z)}{\partial z_k}-\frac{\partial z_c}{\partial z_k}=s_k-y_k"),
        ("deep", "Yakobi matritsasi orqali keltirib chiqarish (zanjir qoidasi)", [
            ("p", r"Ehtimolliklar bo‘yicha hosila: $\partial\,\mathrm{CE}/\partial s_i=-y_i/s_i$. Softmax Yakobi matritsasi: $\partial s_i/\partial z_k=s_i(\delta_{ik}-s_k)$. Zanjir qoidasi bo‘yicha:"),
            ("eq", r"\frac{\partial\,\mathrm{CE}}{\partial z_k}=\sum_i\Bigl(-\frac{y_i}{s_i}\Bigr)s_i(\delta_{ik}-s_k)=-\sum_i y_i\delta_{ik}+s_k\sum_i y_i=s_k-y_k"),
            ("p", r"Oxirgi qadamda $\sum_i y_i=1$ dan foydalanildi. Yakobi matritsasidagi $s_i$ ko‘paytuvchilar logarifmdagi $1/s_i$ maxrajlar bilan qisqardi — butun matritsa ayirmaga aylandi. Formula faqat one-hot uchun emas, yig‘indisi 1 bo‘lgan istalgan $y$ maqsad uchun o‘rinli (masalan, belgilar silliqlanganda)."),
        ]),
        ("p", "Bu formulaning uchta muhim natijasi bor:"),
        ("ul", [
            r"<b>gradiyent chegaralangan</b>: har bir $s_k-y_k$ komponenta $(-1;\,1)$ da yotadi, ularning yig‘indisi esa 0 — to‘g‘ri logit qolganlari birgalikda pastga tortilgancha yuqoriga tortiladi;",
            r"<b>xatoda to‘yinish yo‘q</b>: agar model ishonch bilan xato qilsa ($s_c\to0$), to‘g‘ri logit bo‘yicha gradiyent nolga emas, $-1$ ga intiladi. Softmax ustidagi MSE bilan solishtiring: u yerda Yakobi matritsasidan kelgan ko‘paytuvchilar gradiyentni aynan xato katta bo‘lganda so‘ndiradi (<a href='#training'>CE va MSE haqidagi</a> bo‘lim);",
            r"<b>muvaffaqiyatda so‘nish</b>: $s\to y$ da gradiyent 0 ga intiladi — yaxshi o‘rganilgan misollar o‘qitishga deyarli ta’sir qilmaydi.",
        ]),
        ("viz", "cross-entropy-gradient", {"z": [2, 1, 0], "k": 0, "eta": 1}, r"<b>Rasm 3.</b> $(2;\,1;\,0)$ logitli va birinchi sinfi to‘g‘ri bo‘lgan bitta misol. O‘ngda ustunlar — $s$ bashorat, qora tokchalar — $y$ maqsad, strelkalar va sonlar — $s_k-y_k$. «Qadam» ni bosing: logitlar $\eta=1$ bilan $z\leftarrow z-\eta(s-y)$ qoidasi bo‘yicha yangilanadi va yo‘qotish kamayadi: $0{,}408\to0{,}258\to0{,}187\to0{,}146$, 10 qadamdan keyin $0{,}058$. 3-sinfni to‘g‘ri qiling — yo‘qotish $2{,}408$, gradiyent esa $(0{,}665;\,0{,}245;\,-0{,}910)$ bo‘ladi."),
        ("deep", "Ikkinchi hosila: CE logitlar bo‘yicha qavariq", [
            ("p", r"$s_k-y_k$ ni yana bir marta differensiallaymiz: CE ning logitlar bo‘yicha gessiani softmax Yakobi matritsasiga teng, $\nabla^2_z\,\mathrm{CE}=\operatorname{diag}(s)-ss^\top$. Bu matritsa nomanfiy aniqlangan, shuning uchun CE — logitlarning qavariq funksiyasi, $z=Wx+b$ softmax-regressiyada esa yo‘qotish $(W,b)$ bo‘yicha qavariq: yomon lokal minimumlar yo‘q. $\mathbf 1$ yo‘nalishda matritsa xos — barcha logitlarni siljitish yo‘qotishni o‘zgartirmaydi."),
        ]),
    ]),
    dict(id="landscape", title="3D’da yo‘qotishlar landshafti", blocks=[
        ("p", r"Uchinchi logitni $z_3=0$ da qayd etamiz va yo‘qotishni qolgan ikkitasining funksiyasi sifatida chizamiz. To‘g‘ri sinf 1 uchun:"),
        ("eq", r"\mathrm{CE}(z_1,z_2)=\ln\bigl(e^{z_1}+e^{z_2}+1\bigr)-z_1=\ln\bigl(1+e^{z_2-z_1}+e^{-z_1}\bigr)"),
        ("p", r"$z_1$ ham $z_2$ dan, ham noldan ancha katta bo‘lgan joyda logarifm ostidagi ikkala eksponenta kichik va yo‘qotish 0 ga yaqin. Birinchi sinf yutqazgan joyda yo‘qotish deyarli chiziqli — taxminan $\max(z_2,0)-z_1$ kabi o‘sadi. Asta pastga tushadigan, lekin nolga yetmaydigan qavariq «vodiy» hosil bo‘ladi."),
        ("viz", "cross-entropy-landscape", {"z": [2, 1], "k": 0}, r"<b>Rasm 4.</b> Chapda — tanlangan to‘g‘ri sinf uchun $\mathrm{CE}(z_1,z_2,0)$ sirt (uni aylantirish mumkin). O‘ngda — yuqoridan ko‘rinish: rang va sath chiziqlari — yo‘qotish, strelkalar — $z_1$ va $z_2$ bo‘yicha $-(s-y)$ antigradiyent. Qizil nuqtani surish mumkin. «Boshlash» $(2;\,1)$ nuqtadan $z_1$, $z_2$ bo‘yicha $0{,}8$ qadamli gradiyentli tushishni ishga tushiradi: yo‘qotish 5 qadamda $0{,}408\to0{,}132$, 10 qadamda $0{,}079$, 79 qadamda $0{,}013$, nuqta esa o‘ngga-pastga ketaveradi — minimumga yetib bo‘lmaydi."),
        ("callout", "warn", "Minimum yo‘q", r"One-hot maqsad uchun CE ning quyi chegarasi 0, lekin unga faqat to‘g‘ri logitning cheksiz ustunligida erishiladi. Agar model o‘qitish ma’lumotlarini ideal ajrata olsa, CE logitlar o‘sishi hisobiga kamayishda davom etadi va vaznlar cheksizlikka ketadi. Buni vaznlarni regulyarizatsiya qilish, erta to‘xtatish va belgilarni silliqlash bilan davolaydilar."),
    ]),
    dict(id="smoothing", title="Belgilarni silliqlash", blocks=[
        ("p", r"Belgilarni silliqlash (label smoothing) one-hot maqsadni tekis taqsimot bilan aralashmaga almashtiradi:"),
        ("eq", r"y^{\mathrm{LS}}_k=(1-\varepsilon)\,y_k+\frac{\varepsilon}{K}"),
        ("p", r"To‘g‘ri sinf $1-\varepsilon+\varepsilon/K$, qolganlarining har biri $\varepsilon/K$ oladi. Endi yo‘qotishning haqiqiy minimumi bor: $s=y^{\mathrm{LS}}$ bo‘lganda $s-y^{\mathrm{LS}}$ gradiyent nolga aylanadi. Agar barcha noto‘g‘ri logitlar teng bo‘lib, to‘g‘ri logit ulardan $m$ ga oldinda bo‘lsa, optimal ustunlik chekli:"),
        ("eq", r"s_c=\frac{e^{m}}{e^{m}+K-1}=1-\varepsilon+\frac{\varepsilon}{K}\quad\Longrightarrow\quad m^{*}=\ln\Bigl(1+\frac{K(1-\varepsilon)}{\varepsilon}\Bigr)"),
        ("viz", "cross-entropy-smoothing", {"eps": 0.1, "K": 3}, r"<b>Rasm 5.</b> Yo‘qotish va uning hosilasi to‘g‘ri logitning $m$ ustunligi funksiyalari sifatida (qolgan $K-1$ ta logit teng). Silliqlashsiz (punktir) yo‘qotish monoton kamayadi va faqat $m\to\infty$ da 0 ga intiladi, hosila doim manfiy. $K=3$ da $\varepsilon=0{,}1$ silliqlash bilan minimum paydo bo‘ladi: $m^*=\ln28\approx3{,}332$, bu yerda to‘g‘ri sinf ehtimolligi $0{,}9333$ maqsadga, yo‘qotish esa maqsad entropiyasi $H(y^{\mathrm{LS}})\approx0{,}291$ ga teng. $K=10$ da: $m^*\approx4{,}511$."),
        ("p", r"Belgilarni silliqlash (Segedi va boshq., 2016, Inception-v3) logitlar o‘sishini cheklaydi va odatda kalibrlashni yaxshilaydi; u, masalan, asl Transformer’da $\varepsilon=0{,}1$ bilan ishlatilgan. Bahosi — model endi hech qachon 100% ishonchli emas, logitlaridagi sinflar o‘xshashligi haqidagi axborot qisman o‘chadi, bu esa distillyatsiyaga xalaqit berishi mumkin (Myuller va boshq., 2019)."),
    ]),
    dict(id="training", title="CE va MSE: nega klassifikatorlar kross-entropiyada o‘qitiladi", blocks=[
        ("p", r"Nega klassifikatorni ehtimolliklar va one-hot belgi orasidagi $\|s-y\|^2$ kvadratik xato bilan o‘qitmaslik kerak? Logitlar bo‘yicha gradiyentlarni solishtiramiz:"),
        ("eq", r"\frac{\partial\,\mathrm{CE}}{\partial z}=s-y,\qquad\frac{\partial\,\|s-y\|^2}{\partial z}=J^{\top}\,2(s-y)=2\,s\odot\bigl((s-y)-\langle s-y,\,s\rangle\,\mathbf 1\bigr)"),
        ("p", r"MSE gradiyentida Yakobi matritsasidan kelgan $s$ ko‘paytuvchi turadi. Agar model ishonch bilan xato qilsa — deyarli butun massa bitta noto‘g‘ri sinfda bo‘lsa, — gradiyent deyarli nolga aylanadi: kichik $s_k$ lar uchun $s_k$ ko‘paytuvchi kichik, noto‘g‘ri sevimli sinf uchun esa qavs deyarli nol. Model o‘zining qo‘pol xatosini «eshitmaydi». CE gradiyentida bunday ko‘paytuvchi yo‘q."),
        ("viz", "cross-entropy-train", {}, r"<b>Rasm 6.</b> Bir xil ma’lumotlar va bir xil «ishonchli noto‘g‘ri» boshlanish: vaznlar begona sinflar markazlariga yo‘nalgan, aniqlik $3{,}3\%$. Softmax-regressiyaning ikki nusxasi $0{,}5$ qadamli gradiyentli tushish bilan parallel o‘qitiladi — biri CE da, ikkinchisi MSE da. Boshlanishda logitlar bo‘yicha gradiyentning o‘rtacha normasi: CE da $1{,}3$, MSE da $0{,}13$. 10 qadamdan keyin aniqlik $85{,}6\%$ ga qarshi $5{,}6\%$, 50 qadamdan keyin — $93{,}3\%$ ga qarshi $25{,}6\%$; MSE faqat yuzinchi qadamga kelib yetib oladi ($90{,}0\%$), ikki yuzinchi qadamda esa ikkala model $95{,}6\%$ beradi."),
        ("callout", "note", "Kvadratik xato baribir qachon ishlatiladi", r"Ehtimolliklar va belgi orasidagi kvadratik xato Brayer bahosi (Brier score) deb ataladi va kalibrlash <i>metrikasi</i> sifatida foydali. Klassifikatorlarni o‘qitish uchun deyarli doim CE olinadi: u logitlar bo‘yicha qavariq va xatolarda to‘yinmaydi."),
    ]),
    dict(id="llm", title="Til modellari va perpleksiya", blocks=[
        ("p", r"Til modeli har bir $t$ pozitsiyada keyingi tokenning $V$ ta tokenli (o‘n minglab) lug‘at bo‘yicha taqsimotini bashorat qiladi. Bu $V$ ta sinfga klassifikatsiya, yo‘qotish esa pozitsiyalar bo‘yicha o‘rtacha kross-entropiya:"),
        ("eq", r"\mathcal L=-\frac1T\sum_{t=1}^{T}\ln p_\theta(x_t\mid x_{<t}),\qquad\mathrm{PPL}=e^{\mathcal L}=\Bigl(\prod_{t=1}^{T}\frac{1}{p_\theta(x_t\mid x_{<t})}\Bigr)^{1/T}"),
        ("p", r"<b>Perpleksiya</b> — CE ning eksponentasi, ya’ni $1/p_t$ qiymatlarning o‘rta geometrigi. Uni «variantlarning samarali soni» deb o‘qiydilar: doim $k$ ta token orasidan tekis tanlaydigan modelning perpleksiyasi aynan $k$. Til haqida hech narsa bilmaydigan model (lug‘at bo‘yicha tekis taqsimot) uchun $\mathcal L=\ln V$ va $\mathrm{PPL}=V$."),
        ("viz", "cross-entropy-perplexity", {"lambda": 1}, r"<b>Rasm 7.</b> Gapning har bir tokenidagi $-\ln p_t$ yo‘qotish (o‘quv misoli: ehtimolliklar qo‘lda berilgan). To‘q sariq chiziq — o‘rtacha, ya’ni CE; punktir — $V=50\,000$ lug‘at uchun $\ln V$. $\lambda=1$ da: $\mathrm{CE}\approx1{,}086$, perpleksiya $\approx2{,}963$ — model o‘rtacha uchta variant orasida ikkilanadi; eng qimmati birinchi so‘z ($p=0{,}05$, jarima $3{,}00$). $\lambda$ slayderi logitlarni ko‘paytiradi: $\lambda=0{,}5$ da perpleksiya allaqachon $\approx263{,}5$, $\lambda=0$ da taqsimot tekis, $\mathrm{CE}=\ln50\,000\approx10{,}82$ va perpleksiya $50\,000$."),
        ("callout", "note", "Perpleksiyalarni ehtiyotkorlik bilan solishtiring", r"Perpleksiya tokenizatorga bog‘liq: bir xil matnda yirikroq tokenli model kamroq bashorat qiladi va har biri qiyinroq. Faqat bir xil lug‘atli modellarni bir xil ma’lumotlarda solishtirish mumkin — yoki belgi yoki bayt boshiga bitlarga o‘tish kerak."),
    ]),
    dict(id="code", title="Kodda", blocks=[
        ("p", r"Asosiy qoida — CE ni logitlardan log-softmax orqali hisoblash: $\mathrm{CE}=\operatorname{LSE}(z)-z_c$. «Avval softmax, keyin logarifm» yo‘li ishonchli xatolarda $\ln0=-\infty$ beradi: $(0;\,800;\,0)$ logitlar va to‘g‘ri birinchi sinf uchun sodda kod <code>inf</code> qaytaradi, barqarori esa aniq $800$ javobini."),
        ("code", "python", "CODE_NUMPY"),
        ("code", "python", "CODE_TORCH"),
        ("callout", "key", "PyTorch uchun tekshiruv ro‘yxati", r"<code>F.cross_entropy</code> / <code>nn.CrossEntropyLoss</code> <b>logitlarni</b> (softmax’siz!) va <code>long</code> turidagi sinf raqamlarini — yoki logitlar bilan bir xil shakldagi ehtimolliklarni qabul qiladi. Foydali parametrlar: <code>label_smoothing</code>, <code>weight</code> (nomutanosiblikda sinflar vaznlari), <code>ignore_index</code> (masalan, padding). Sinflar ikkinchi o‘lchovda turishi kerak, shuning uchun $(B,T,V)$ shaklli logitlarni <code>reshape</code> bilan $(BT,V)$ ga aylantirish eng oson."),
    ]),
    dict(id="mistakes", title="Ko‘p uchraydigan xatolar", blocks=[
        ("ol", [
            r"<b><code>CrossEntropyLoss</code> dan oldin softmax</b> — ikki karra softmax: ehtimolliklar siqiladi, yo‘qotish nolgacha tusha olmaydi, gradiyentlar buziladi. Logitlarni bering.",
            r"<b>log-softmax o‘rniga <code>np.log(softmax(z))</code></b> — ishonchli xatoda ehtimollik 0 gacha yaxlitlanadi, yo‘qotish <code>inf</code>, gradiyent NaN bo‘ladi. <code>clip(p, 1e-7, 1)</code> «yamog‘i» cheksizlikdan qutqaradi, lekin gradiyentni kesadi; to‘g‘risi — LSE.",
            r"<b>One-hot va sinf raqamlarini chalkashtirish</b>. Keras’da bular turli funksiyalar: <code>categorical_crossentropy</code> one-hot kutadi, <code>sparse_categorical_crossentropy</code> — raqamlarni. PyTorch’da raqamlar <code>long</code> turida, ehtimoliy maqsadlar esa logitlar bilan bir xil shaklda bo‘lishi kerak.",
            r"<b>O‘rtacha o‘rniga yig‘indi</b>. <code>reduction='sum'</code> bilan yo‘qotish va gradiyent batch o‘lchami bilan o‘sadi va tanlangan o‘qitish tezligi mos kelmay qoladi.",
            r"<b>Sinflar nomutanosibligiga e’tiborsizlik</b>. CE misollar bo‘yicha o‘rtachalaydi, shuning uchun kam uchraydigan sinf gradiyentga deyarli ta’sir qilmaydi. Sinflar vaznlari (<code>weight</code>) yoki <a href='../focal/'>Focal Loss</a> yordam beradi.",
            r"<b>Solishtirib bo‘lmaydigan sonlar</b>: natlar va bitlardagi yo‘qotishlar, turli tokenizatorli modellarning perpleksiyalari.",
        ]),
    ]),
    dict(id="links", title="Boshqa formulalar bilan bog‘liqlik", blocks=[
        ("ul", [
            r"<a href='../softmax/'>Softmax</a>: $s$ ehtimolliklarni beradi; CE bilan birga — $s-y$ gradiyentni, $\mathrm{CE}=\operatorname{LSE}(z)-z_c$.",
            r"<a href='../bce/'>BCE</a>: bitta chiqishli $K=2$ holi: $-\bigl[y\ln\hat y+(1-y)\ln(1-\hat y)\bigr]$.",
            r"<a href='../sigmoid/'>Sigmoida</a>: ikki sinf uchun softmax sigmoidaga keladi va CE BCE ga aylanadi.",
            r"<a href='../focal/'>Focal Loss</a>: $-(1-p_t)^\gamma\ln p_t$ — oson misollarda susaytirilgan kross-entropiya.",
            r"<a href='../mse/'>MSE</a>: softmax ustida ishonchli xatolarda to‘yinadi (<a href='#training'>solishtirish haqidagi</a> bo‘limga qarang).",
            r"<a href='../adam/'>Adam</a>: chuqur tarmoqlarda CE odatda shu optimizator bilan minimallashtiriladi.",
        ]),
    ]),
    dict(id="summary", title="Xulosa", blocks=[
        ("callout", "key", None, r"1) One-hot belgi uchun $\mathrm{CE}=-\ln s_c$ — modelning to‘g‘ri javobdan hayrati; ma’lumotlar bo‘yicha o‘rtachasi — $N$ ga bo‘lingan minus log-haqqoniylik. 2) $H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)$: $q$ bo‘yicha minimum $q=p$ da. 3) Softmax bilan logitlar bo‘yicha gradiyent $s-y$: chegaralangan, xatolarda to‘yinmaydi va muvaffaqiyatda yo‘qoladi; CE logitlar bo‘yicha qavariq. 4) One-hot maqsadlarda minimumga erishib bo‘lmaydi — logitlar o‘sadi; belgilarni silliqlash optimumni chekli qiladi. 5) CE ni logitlardan log-sum-exp orqali hisoblang; $e^{\mathrm{CE}}$ — perpleksiya."),
    ]),
    dict(id="quiz", title="O‘zingizni tekshiring", blocks=[
        ("quiz", [
            dict(q=r"Model to‘g‘ri sinfga $0{,}25$ ehtimollik berdi. CE nimaga teng?", options=[r"$0{,}25$", r"$0{,}75$", r"$\approx1{,}386$", r"$\approx0{,}288$"], answer=2,
                 explain=r"$-\ln0{,}25=\ln4\approx1{,}386$ nat (aynan 2 bit)."),
            dict(q="Ehtimolliklar softmax’dan olingan bo‘lsa, CE ning logitlar bo‘yicha gradiyenti nimaga teng?", options=[r"$-y/s$", r"$s-y$", r"$\operatorname{diag}(s)-ss^\top$", r"$(s-y)^2$"], answer=1,
                 explain=r"$\mathrm{CE}=\operatorname{LSE}(z)-z_c$, $\nabla\operatorname{LSE}=s$ esa; $-y/s$ — logitlar emas, ehtimolliklar bo‘yicha gradiyent."),
            dict(q="Model 10 ta sinfda tekis javob beradi. CE va perpleksiya nimaga teng?", options=[r"$0$ va $1$", r"$\ln10\approx2{,}303$ va $10$", r"$0{,}1$ va $10$", r"$1$ va $e$"], answer=1,
                 explain=r"Har bir sinfga $0{,}1$, demak $\mathrm{CE}=-\ln0{,}1=\ln10$, $\mathrm{PPL}=e^{\ln10}=10$."),
            dict(q=r"Qanday $q$ bashoratda $H(p,q)$ kross-entropiya eng kichik?", options=[r"$q=p$", r"$q$ — $p$ ning eng ehtimolli sinfi one-hot vektori", r"$q$ — tekis taqsimot", "Minimum yo‘q"], answer=0,
                 explain=r"$H(p,q)=H(p)+\mathrm{KL}(p\,\|\,q)$, KL esa nomanfiy va faqat $q=p$ da nolga teng."),
            dict(q=r"$K=3$ da $\varepsilon=0{,}1$ bilan belgilarni silliqlash. O‘qitish to‘g‘ri sinfning qaysi ehtimolligiga intiladi?", options=[r"$1$", r"$0{,}9$", r"$\approx0{,}933$", r"$\approx0{,}967$"], answer=2,
                 explain=r"To‘g‘ri sinf uchun maqsad $1-\varepsilon+\varepsilon/K=0{,}9+0{,}0333\approx0{,}933$; bu nuqtada $s-y=0$."),
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
