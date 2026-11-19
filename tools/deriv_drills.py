"""Practice drills for the article "The derivative, partial derivatives and the gradient" (tools/content_deriv.py).

Every drill is solved FROM THE DEFINITION (the limit of the ratio of increments). The drills are language-neutral
data — formulas in TeX and keys of step captions; the captions and tasks in three languages live in LABELS / TASKS.
Every intermediate quotient and every answer is verified with SymPy by verify() — run:  python3 tools/deriv_drills.py
"""

LABELS = {
    "def": {"ru": "Записываем определение: предел отношения приращения функции к приращению аргумента.",
            "en": "Write the definition: the limit of the ratio of the increment of the function to the increment of the argument.",
            "uz": "Ta’rifni yozamiz: funksiya orttirmasining argument orttirmasiga nisbati limiti."},
    "inc": {"ru": "Находим приращение функции $\\Delta f = f(x + \\Delta x) - f(x)$: подставляем $x + \\Delta x$ вместо $x$ и раскрываем скобки.",
            "en": "Find the increment of the function $\\Delta f = f(x + \\Delta x) - f(x)$: substitute $x + \\Delta x$ for $x$ and expand the brackets.",
            "uz": "Funksiya orttirmasini topamiz $\\Delta f = f(x + \\Delta x) - f(x)$: $x$ o‘rniga $x + \\Delta x$ ni qo‘yamiz va qavslarni ochamiz."},
    "cut": {"ru": "Делим на $\\Delta x$ (по определению предела $\\Delta x \\ne 0$, поэтому это законно) и сокращаем.",
            "en": "Divide by $\\Delta x$ (in the definition of the limit $\\Delta x \\ne 0$, so this is legitimate) and cancel.",
            "uz": "$\\Delta x$ ga bo‘lamiz (limit ta’rifida $\\Delta x \\ne 0$, shuning uchun bu qonuniy) va qisqartiramiz."},
    "lim": {"ru": "Переходим к пределу $\\Delta x \\to 0$: оставшееся выражение непрерывно по $\\Delta x$, поэтому подставляем $\\Delta x = 0$.",
            "en": "Pass to the limit $\\Delta x \\to 0$: what remains is continuous in $\\Delta x$, so we substitute $\\Delta x = 0$.",
            "uz": "$\\Delta x \\to 0$ limitga o‘tamiz: qolgan ifoda $\\Delta x$ bo‘yicha uzluksiz, shuning uchun $\\Delta x = 0$ ni qo‘yamiz."},
    "point": {"ru": "Подставляем точку в определение: приращение даём аргументу именно в этой точке.",
              "en": "Substitute the point into the definition: the argument gets its increment exactly at this point.",
              "uz": "Nuqtani ta’rifga qo‘yamiz: argument aynan shu nuqtada orttirma oladi."},
    "conj": {"ru": "Корни в числителе мешают сократить $\\Delta x$: умножаем числитель и знаменатель на сопряжённое выражение — получается разность квадратов.",
             "en": "The roots in the numerator prevent cancelling $\\Delta x$: multiply the numerator and the denominator by the conjugate — a difference of squares appears.",
             "uz": "Suratdagi ildizlar $\\Delta x$ ni qisqartirishga xalaqit beradi: surat va maxrajni qo‘shma ifodaga ko‘paytiramiz — kvadratlar ayirmasi hosil bo‘ladi."},
    "common": {"ru": "Приводим дроби в приращении к общему знаменателю.",
               "en": "Bring the fractions in the increment to a common denominator.",
               "uz": "Orttirmadagi kasrlarni umumiy maxrajga keltiramiz."},
    "factor": {"ru": "Выносим общий множитель: в приращении остаётся выражение, предел которого известен.",
               "en": "Factor out the common factor: what remains in the increment has a known limit.",
               "uz": "Umumiy ko‘paytuvchini chiqaramiz: orttirmada limiti ma’lum ifoda qoladi."},
    "trig": {"ru": "Превращаем разность тригонометрических функций в произведение (формулы разности синусов и косинусов).",
             "en": "Turn the difference of trigonometric functions into a product (the difference-of-sines and difference-of-cosines formulas).",
             "uz": "Trigonometrik funksiyalar ayirmasini ko‘paytmaga aylantiramiz (sinuslar va kosinuslar ayirmasi formulalari)."},
    "known": {"ru": "Используем замечательный предел — его доказывают один раз, отдельно, а потом применяют как готовый факт.",
              "en": "Use a fundamental limit — it is proved once, separately, and then used as a ready fact.",
              "uz": "Ajoyib limitdan foydalanamiz — u bir marta, alohida isbotlanadi, keyin tayyor fakt sifatida qo‘llanadi."},
    "check": {"ru": "Проверяем по таблице производных: ответ совпадает.",
              "en": "Check with the table of derivatives: the answer is the same.",
              "uz": "Hosilalar jadvali bilan tekshiramiz: javob mos keladi."},
    "right": {"ru": "Предел справа ($\\Delta x \\to 0^{+}$, шаг положительный).",
              "en": "The limit from the right ($\\Delta x \\to 0^{+}$, a positive step).",
              "uz": "O‘ngdan limit ($\\Delta x \\to 0^{+}$, qadam musbat)."},
    "left": {"ru": "Предел слева ($\\Delta x \\to 0^{-}$, шаг отрицательный).",
             "en": "The limit from the left ($\\Delta x \\to 0^{-}$, a negative step).",
             "uz": "Chapdan limit ($\\Delta x \\to 0^{-}$, qadam manfiy)."},
    "nolim": {"ru": "Односторонние пределы различны — общего предела нет, значит, производной в этой точке не существует.",
              "en": "The one-sided limits differ — there is no common limit, so the derivative does not exist at this point.",
              "uz": "Bir tomonlama limitlar har xil — umumiy limit yo‘q, demak, bu nuqtada hosila mavjud emas."},
    "squeeze": {"ru": "Ограниченный множитель умножается на бесконечно малый — произведение стремится к нулю (теорема о двух милиционерах).",
                "en": "A bounded factor times a vanishing one — the product tends to zero (the squeeze theorem).",
                "uz": "Chegaralangan ko‘paytuvchi cheksiz kichikka ko‘paytiriladi — ko‘paytma nolga intiladi (ikki militsioner teoremasi)."},
    "infinite": {"ru": "Отношение неограниченно растёт: конечного предела нет, касательная вертикальна.",
                 "en": "The ratio grows without bound: there is no finite limit, the tangent is vertical.",
                 "uz": "Nisbat cheksiz o‘sadi: chekli limit yo‘q, urinma vertikal."},
    "incx": {"ru": "Частное приращение по $x$: приращение $\\Delta x$ получает только $x$, а $y$ остаётся прежним (ведёт себя как число).",
             "en": "The partial increment in $x$: only $x$ gets the increment $\\Delta x$, while $y$ stays the same (behaves as a number).",
             "uz": "$x$ bo‘yicha xususiy orttirma: $\\Delta x$ orttirmani faqat $x$ oladi, $y$ esa o‘zgarmaydi (son kabi)."},
    "incy": {"ru": "Частное приращение по $y$: приращение $\\Delta y$ получает только $y$, а $x$ заморожен.",
             "en": "The partial increment in $y$: only $y$ gets the increment $\\Delta y$, while $x$ is frozen.",
             "uz": "$y$ bo‘yicha xususiy orttirma: $\\Delta y$ orttirmani faqat $y$ oladi, $x$ esa muzlatilgan."},
    "incz": {"ru": "Частное приращение по $z$: меняется только $z$.",
             "en": "The partial increment in $z$: only $z$ changes.",
             "uz": "$z$ bo‘yicha xususiy orttirma: faqat $z$ o‘zgaradi."},
    "limx": {"ru": "Делим на $\\Delta x$ и переходим к пределу $\\Delta x \\to 0$.",
             "en": "Divide by $\\Delta x$ and pass to the limit $\\Delta x \\to 0$.",
             "uz": "$\\Delta x$ ga bo‘lamiz va $\\Delta x \\to 0$ limitga o‘tamiz."},
    "limy": {"ru": "Делим на $\\Delta y$ и переходим к пределу $\\Delta y \\to 0$.",
             "en": "Divide by $\\Delta y$ and pass to the limit $\\Delta y \\to 0$.",
             "uz": "$\\Delta y$ ga bo‘lamiz va $\\Delta y \\to 0$ limitga o‘tamiz."},
    "limz": {"ru": "Делим на $\\Delta z$ и переходим к пределу $\\Delta z \\to 0$.",
             "en": "Divide by $\\Delta z$ and pass to the limit $\\Delta z \\to 0$.",
             "uz": "$\\Delta z$ ga bo‘lamiz va $\\Delta z \\to 0$ limitga o‘tamiz."},
    "grad": {"ru": "Собираем частные производные в один вектор — градиент.",
             "en": "Collect the partial derivatives into one vector — the gradient.",
             "uz": "Xususiy hosilalarni bitta vektorga yig‘amiz — gradiyent."},
    "grad1": {"ru": "У функции одной переменной градиент — вектор из одной компоненты, и она совпадает с обычной производной.",
              "en": "For a function of one variable the gradient is a vector with one component, and it equals the ordinary derivative.",
              "uz": "Bir o‘zgaruvchili funksiyada gradiyent — bitta komponentli vektor va u oddiy hosilaga teng."},
    "unit": {"ru": "Направление должно быть единичным: делим вектор на его длину.",
             "en": "The direction must be a unit vector: divide the vector by its length.",
             "uz": "Yo‘nalish birlik vektor bo‘lishi kerak: vektorni uning uzunligiga bo‘lamiz."},
    "dirdef": {"ru": "Определение производной по направлению: сдвигаемся из точки на $t$ вдоль единичного вектора $\\mathbf{u}$ и делим приращение на $t$.",
               "en": "The definition of the directional derivative: move from the point by $t$ along the unit vector $\\mathbf{u}$ and divide the increment by $t$.",
               "uz": "Yo‘nalish bo‘yicha hosila ta’rifi: nuqtadan $\\mathbf{u}$ birlik vektor bo‘ylab $t$ ga siljiymiz va orttirmani $t$ ga bo‘lamiz."},
    "dirinc": {"ru": "Считаем приращение функции вдоль направления и делим на $t$.",
               "en": "Compute the increment of the function along the direction and divide by $t$.",
               "uz": "Yo‘nalish bo‘ylab funksiya orttirmasini hisoblaymiz va $t$ ga bo‘lamiz."},
    "dirlim": {"ru": "Переходим к пределу $t \\to 0$.", "en": "Pass to the limit $t \\to 0$.", "uz": "$t \\to 0$ limitga o‘tamiz."},
    "dircheck": {"ru": "Проверка через градиент: $D_{\\mathbf{u}} f = \\nabla f\\cdot\\mathbf{u}$ — тот же ответ.",
                 "en": "Check through the gradient: $D_{\\mathbf{u}} f = \\nabla f\\cdot\\mathbf{u}$ — the same answer.",
                 "uz": "Gradiyent orqali tekshiruv: $D_{\\mathbf{u}} f = \\nabla f\\cdot\\mathbf{u}$ — javob o‘sha-o‘sha."},
    "gradpt": {"ru": "Частные производные (найдены по определению выше) в данной точке.",
               "en": "The partial derivatives (found from the definition above) at the given point.",
               "uz": "Berilgan nuqtadagi xususiy hosilalar (yuqorida ta’rif bo‘yicha topilgan)."},
    "lin": {"ru": "Полный дифференциал — линейная часть приращения: $df = f_x\\,\\Delta x + f_y\\,\\Delta y$.",
            "en": "The total differential is the linear part of the increment: $df = f_x\\,\\Delta x + f_y\\,\\Delta y$.",
            "uz": "To‘liq differensial — orttirmaning chiziqli qismi: $df = f_x\\,\\Delta x + f_y\\,\\Delta y$."},
    "exact": {"ru": "Точное приращение для сравнения; разница — «хвост» второго порядка малости.",
              "en": "The exact increment for comparison; the difference is a second-order “tail”.",
              "uz": "Taqqoslash uchun aniq orttirma; farq — ikkinchi tartibli «dum»."},
    "step": {"ru": "Шаг градиентного спуска: $\\mathbf{p} \\leftarrow \\mathbf{p} - \\eta\\,\\nabla f(\\mathbf{p})$.",
             "en": "A gradient descent step: $\\mathbf{p} \\leftarrow \\mathbf{p} - \\eta\\,\\nabla f(\\mathbf{p})$.",
             "uz": "Gradiyent tushish qadami: $\\mathbf{p} \\leftarrow \\mathbf{p} - \\eta\\,\\nabla f(\\mathbf{p})$."},
    "value": {"ru": "Значение функции до и после шага: оно уменьшилось.",
              "en": "The value of the function before and after the step: it has decreased.",
              "uz": "Qadamdan oldin va keyin funksiya qiymati: u kamaydi."},
}

TASKS = {
    "d": {"ru": "Найдите производную по определению.", "en": "Find the derivative from the definition.", "uz": "Hosilani ta’rif bo‘yicha toping."},
    "dp": {"ru": "Найдите производную в точке по определению.", "en": "Find the derivative at the point from the definition.", "uz": "Nuqtadagi hosilani ta’rif bo‘yicha toping."},
    "ex": {"ru": "Существует ли производная в точке $x = 0$? Ответьте по определению.", "en": "Does the derivative exist at $x = 0$? Answer from the definition.", "uz": "$x = 0$ nuqtada hosila mavjudmi? Ta’rif bo‘yicha javob bering."},
    "pd": {"ru": "Найдите частные производные по определению.", "en": "Find the partial derivatives from the definition.", "uz": "Xususiy hosilalarni ta’rif bo‘yicha toping."},
    "pdp": {"ru": "Найдите частные производные в точке по определению.", "en": "Find the partial derivatives at the point from the definition.", "uz": "Nuqtadagi xususiy hosilalarni ta’rif bo‘yicha toping."},
    "gr": {"ru": "Найдите градиент по определению.", "en": "Find the gradient from the definition.", "uz": "Gradiyentni ta’rif bo‘yicha toping."},
    "dir": {"ru": "Найдите производную по направлению по определению и проверьте через градиент.", "en": "Find the directional derivative from the definition and check it through the gradient.", "uz": "Yo‘nalish bo‘yicha hosilani ta’rif bo‘yicha toping va gradiyent orqali tekshiring."},
    "lin": {"ru": "Оцените приращение функции полным дифференциалом и сравните с точным.", "en": "Estimate the increment of the function with the total differential and compare it with the exact one.", "uz": "Funksiya orttirmasini to‘liq differensial bilan baholang va aniq qiymat bilan solishtiring."},
    "gd": {"ru": "Сделайте шаг градиентного спуска (градиент — по определению).", "en": "Make a gradient descent step (the gradient from the definition).", "uz": "Gradiyent tushishning bir qadamini bajaring (gradiyent — ta’rif bo‘yicha)."},
}

GROUPS = {
    1: {"ru": "Многочлены: приращение, деление, предел", "en": "Polynomials: increment, division, limit", "uz": "Ko‘phadlar: orttirma, bo‘lish, limit"},
    11: {"ru": "Дроби и корни", "en": "Fractions and roots", "uz": "Kasrlar va ildizlar"},
    18: {"ru": "Экспонента, логарифм, синус и косинус", "en": "The exponential, the logarithm, sine and cosine", "uz": "Eksponenta, logarifm, sinus va kosinus"},
    25: {"ru": "Существует ли производная?", "en": "Does the derivative exist?", "uz": "Hosila mavjudmi?"},
    29: {"ru": "Частные производные по определению", "en": "Partial derivatives from the definition", "uz": "Ta’rif bo‘yicha xususiy hosilalar"},
    38: {"ru": "Градиент по определению", "en": "The gradient from the definition", "uz": "Ta’rif bo‘yicha gradiyent"},
    42: {"ru": "Производная по направлению, дифференциал, спуск", "en": "The directional derivative, the differential, descent", "uz": "Yo‘nalish bo‘yicha hosila, differensial, tushish"},
}

D = []


def add(level, task, f, steps, ans, checks):
    D.append(dict(n=len(D) + 1, level=level, task=task, f=f, steps=steps, ans=ans, checks=checks))


DEF = r"f'(x) = \lim_{\Delta x \to 0}\frac{\Delta f}{\Delta x} = \lim_{\Delta x \to 0}\frac{f(x + \Delta x) - f(x)}{\Delta x}"
# checks: ("q", f, var, quotient-after-cancelling, limit) — the quotient equals (f(var + Δ) − f)/Δ and tends to the limit;
#         point drills: ("qp", f, var, x0, quotient, limit); partials: ("q2", f, var, quotient, limit) with other variables free.

# ===== 1–10: polynomials =====
add(1, "d", r"f(x) = 5", [
    ("def", DEF), ("inc", r"\Delta f = f(x + \Delta x) - f(x) = 5 - 5 = 0"), ("cut", r"\frac{\Delta f}{\Delta x} = \frac{0}{\Delta x} = 0"),
    ("lim", r"f'(x) = \lim_{\Delta x \to 0} 0 = 0")], r"(5)' = 0", [("q", "5", "x", "0", "0")])
add(1, "d", r"f(x) = 3x - 2", [
    ("def", DEF), ("inc", r"\Delta f = \big(3(x + \Delta x) - 2\big) - (3x - 2) = 3\Delta x"), ("cut", r"\frac{\Delta f}{\Delta x} = \frac{3\Delta x}{\Delta x} = 3"),
    ("lim", r"f'(x) = \lim_{\Delta x \to 0} 3 = 3")], r"(3x - 2)' = 3", [("q", "3*x-2", "x", "3", "3")])
add(1, "d", r"f(x) = x^2", [
    ("def", DEF), ("inc", r"\Delta f = (x + \Delta x)^2 - x^2 = x^2 + 2x\,\Delta x + \Delta x^2 - x^2 = 2x\,\Delta x + \Delta x^2"),
    ("cut", r"\frac{\Delta f}{\Delta x} = \frac{\Delta x\,(2x + \Delta x)}{\Delta x} = 2x + \Delta x"), ("lim", r"f'(x) = \lim_{\Delta x \to 0}(2x + \Delta x) = 2x")],
    r"(x^2)' = 2x", [("q", "x**2", "x", "2*x+D", "2*x")])
add(1, "dp", r"f(x) = x^2,\quad x_0 = 3", [
    ("point", r"f'(3) = \lim_{\Delta x \to 0}\frac{f(3 + \Delta x) - f(3)}{\Delta x}"), ("inc", r"\Delta f = (3 + \Delta x)^2 - 9 = 9 + 6\Delta x + \Delta x^2 - 9 = 6\Delta x + \Delta x^2"),
    ("cut", r"\frac{\Delta f}{\Delta x} = 6 + \Delta x"), ("lim", r"f'(3) = \lim_{\Delta x \to 0}(6 + \Delta x) = 6"), ("check", r"f'(x) = 2x,\quad f'(3) = 2\cdot 3 = 6")],
    r"f'(3) = 6", [("qp", "x**2", "x", "3", "6+D", "6")])
add(2, "d", r"f(x) = 2x^2 - 3x + 1", [
    ("def", DEF), ("inc", r"\Delta f = 2(x + \Delta x)^2 - 3(x + \Delta x) + 1 - (2x^2 - 3x + 1) = 4x\,\Delta x + 2\Delta x^2 - 3\Delta x"),
    ("cut", r"\frac{\Delta f}{\Delta x} = 4x - 3 + 2\Delta x"), ("lim", r"f'(x) = 4x - 3")], r"(2x^2 - 3x + 1)' = 4x - 3",
    [("q", "2*x**2-3*x+1", "x", "4*x-3+2*D", "4*x-3")])
add(2, "d", r"f(x) = x^3", [
    ("def", DEF), ("inc", r"\Delta f = (x + \Delta x)^3 - x^3 = 3x^2\Delta x + 3x\,\Delta x^2 + \Delta x^3"),
    ("cut", r"\frac{\Delta f}{\Delta x} = 3x^2 + 3x\,\Delta x + \Delta x^2"), ("lim", r"f'(x) = 3x^2")], r"(x^3)' = 3x^2",
    [("q", "x**3", "x", "3*x**2+3*x*D+D**2", "3*x**2")])
add(2, "d", r"f(x) = (x + 1)^2", [
    ("def", DEF), ("inc", r"\Delta f = (x + 1 + \Delta x)^2 - (x + 1)^2 = 2(x + 1)\Delta x + \Delta x^2"),
    ("cut", r"\frac{\Delta f}{\Delta x} = 2(x + 1) + \Delta x"), ("lim", r"f'(x) = 2(x + 1) = 2x + 2")], r"\big((x + 1)^2\big)' = 2x + 2",
    [("q", "(x+1)**2", "x", "2*(x+1)+D", "2*x+2")])
add(2, "d", r"f(x) = 4x - x^2", [
    ("def", DEF), ("inc", r"\Delta f = 4(x + \Delta x) - (x + \Delta x)^2 - 4x + x^2 = 4\Delta x - 2x\,\Delta x - \Delta x^2"),
    ("cut", r"\frac{\Delta f}{\Delta x} = 4 - 2x - \Delta x"), ("lim", r"f'(x) = 4 - 2x")], r"(4x - x^2)' = 4 - 2x",
    [("q", "4*x-x**2", "x", "4-2*x-D", "4-2*x")])
add(2, "d", r"f(x) = x^4", [
    ("def", DEF), ("inc", r"\Delta f = (x + \Delta x)^4 - x^4 = 4x^3\Delta x + 6x^2\Delta x^2 + 4x\,\Delta x^3 + \Delta x^4"),
    ("cut", r"\frac{\Delta f}{\Delta x} = 4x^3 + 6x^2\Delta x + 4x\,\Delta x^2 + \Delta x^3"), ("lim", r"f'(x) = 4x^3")], r"(x^4)' = 4x^3",
    [("q", "x**4", "x", "4*x**3+6*x**2*D+4*x*D**2+D**3", "4*x**3")])
add(2, "dp", r"f(x) = x^3,\quad x_0 = -1", [
    ("point", r"f'(-1) = \lim_{\Delta x \to 0}\frac{f(-1 + \Delta x) - f(-1)}{\Delta x}"),
    ("inc", r"\Delta f = (-1 + \Delta x)^3 - (-1) = -1 + 3\Delta x - 3\Delta x^2 + \Delta x^3 + 1 = 3\Delta x - 3\Delta x^2 + \Delta x^3"),
    ("cut", r"\frac{\Delta f}{\Delta x} = 3 - 3\Delta x + \Delta x^2"), ("lim", r"f'(-1) = 3"), ("check", r"f'(x) = 3x^2,\quad f'(-1) = 3\cdot(-1)^2 = 3")],
    r"f'(-1) = 3", [("qp", "x**3", "x", "-1", "3-3*D+D**2", "3")])

# ===== 11–17: fractions and roots =====
add(2, "d", r"f(x) = \frac{1}{x},\quad x \ne 0", [
    ("def", DEF), ("common", r"\Delta f = \frac{1}{x + \Delta x} - \frac{1}{x} = \frac{x - (x + \Delta x)}{x(x + \Delta x)} = \frac{-\Delta x}{x(x + \Delta x)}"),
    ("cut", r"\frac{\Delta f}{\Delta x} = -\frac{1}{x(x + \Delta x)}"), ("lim", r"f'(x) = -\frac{1}{x\cdot x} = -\frac{1}{x^2}")], r"\Big(\frac1x\Big)' = -\frac{1}{x^2}",
    [("q", "1/x", "x", "-1/(x*(x+D))", "-1/x**2")])
add(3, "d", r"f(x) = \frac{1}{x + 1},\quad x \ne -1", [
    ("def", DEF), ("common", r"\Delta f = \frac{1}{x + 1 + \Delta x} - \frac{1}{x + 1} = \frac{-\Delta x}{(x + 1 + \Delta x)(x + 1)}"),
    ("cut", r"\frac{\Delta f}{\Delta x} = -\frac{1}{(x + 1 + \Delta x)(x + 1)}"), ("lim", r"f'(x) = -\frac{1}{(x + 1)^2}")], r"f'(x) = -\frac{1}{(x + 1)^2}",
    [("q", "1/(x+1)", "x", "-1/((x+1+D)*(x+1))", "-1/(x+1)**2")])
add(3, "d", r"f(x) = \frac{1}{x^2},\quad x \ne 0", [
    ("def", DEF), ("common", r"\Delta f = \frac{1}{(x + \Delta x)^2} - \frac{1}{x^2} = \frac{x^2 - (x + \Delta x)^2}{x^2(x + \Delta x)^2} = \frac{-\Delta x\,(2x + \Delta x)}{x^2(x + \Delta x)^2}"),
    ("cut", r"\frac{\Delta f}{\Delta x} = -\frac{2x + \Delta x}{x^2(x + \Delta x)^2}"), ("lim", r"f'(x) = -\frac{2x}{x^2\cdot x^2} = -\frac{2}{x^3}")], r"\Big(\frac{1}{x^2}\Big)' = -\frac{2}{x^3}",
    [("q", "1/x**2", "x", "-(2*x+D)/(x**2*(x+D)**2)", "-2/x**3")])
add(3, "d", r"f(x) = \sqrt{x},\quad x > 0", [
    ("def", DEF), ("conj", r"\frac{\sqrt{x + \Delta x} - \sqrt{x}}{\Delta x}\cdot\frac{\sqrt{x + \Delta x} + \sqrt{x}}{\sqrt{x + \Delta x} + \sqrt{x}} = \frac{(x + \Delta x) - x}{\Delta x\big(\sqrt{x + \Delta x} + \sqrt{x}\big)}"),
    ("cut", r"\frac{\Delta f}{\Delta x} = \frac{1}{\sqrt{x + \Delta x} + \sqrt{x}}"), ("lim", r"f'(x) = \frac{1}{\sqrt{x} + \sqrt{x}} = \frac{1}{2\sqrt{x}}")],
    r"(\sqrt{x})' = \frac{1}{2\sqrt{x}}", [("q", "sqrt(x)", "x", "1/(sqrt(x+D)+sqrt(x))", "1/(2*sqrt(x))")])
add(3, "d", r"f(x) = \sqrt{x + 4},\quad x > -4", [
    ("def", DEF), ("conj", r"\frac{\sqrt{x + 4 + \Delta x} - \sqrt{x + 4}}{\Delta x} = \frac{(x + 4 + \Delta x) - (x + 4)}{\Delta x\big(\sqrt{x + 4 + \Delta x} + \sqrt{x + 4}\big)}"),
    ("cut", r"\frac{\Delta f}{\Delta x} = \frac{1}{\sqrt{x + 4 + \Delta x} + \sqrt{x + 4}}"), ("lim", r"f'(x) = \frac{1}{2\sqrt{x + 4}}")], r"f'(x) = \frac{1}{2\sqrt{x + 4}}",
    [("q", "sqrt(x+4)", "x", "1/(sqrt(x+4+D)+sqrt(x+4))", "1/(2*sqrt(x+4))")])
add(3, "d", r"f(x) = \frac{x}{x + 1},\quad x \ne -1", [
    ("def", DEF), ("common", r"\Delta f = \frac{x + \Delta x}{x + 1 + \Delta x} - \frac{x}{x + 1} = \frac{(x + \Delta x)(x + 1) - x(x + 1 + \Delta x)}{(x + 1 + \Delta x)(x + 1)} = \frac{\Delta x}{(x + 1 + \Delta x)(x + 1)}"),
    ("cut", r"\frac{\Delta f}{\Delta x} = \frac{1}{(x + 1 + \Delta x)(x + 1)}"), ("lim", r"f'(x) = \frac{1}{(x + 1)^2}")], r"f'(x) = \frac{1}{(x + 1)^2}",
    [("q", "x/(x+1)", "x", "1/((x+1+D)*(x+1))", "1/(x+1)**2")])
add(3, "dp", r"f(x) = \sqrt{x},\quad x_0 = 4", [
    ("point", r"f'(4) = \lim_{\Delta x \to 0}\frac{\sqrt{4 + \Delta x} - 2}{\Delta x}"),
    ("conj", r"\frac{\sqrt{4 + \Delta x} - 2}{\Delta x}\cdot\frac{\sqrt{4 + \Delta x} + 2}{\sqrt{4 + \Delta x} + 2} = \frac{\Delta x}{\Delta x\big(\sqrt{4 + \Delta x} + 2\big)} = \frac{1}{\sqrt{4 + \Delta x} + 2}"),
    ("lim", r"f'(4) = \frac{1}{2 + 2} = \frac14"), ("check", r"f'(x) = \frac{1}{2\sqrt{x}},\quad f'(4) = \frac{1}{2\cdot 2} = \frac14")], r"f'(4) = \frac14",
    [("qp", "sqrt(x)", "x", "4", "1/(sqrt(4+D)+2)", "1/4")])

# ===== 18–24: the exponential, the logarithm, sine and cosine =====
add(3, "d", r"f(x) = e^{x}", [
    ("def", DEF), ("factor", r"\Delta f = e^{x + \Delta x} - e^{x} = e^{x}\big(e^{\Delta x} - 1\big),\qquad \frac{\Delta f}{\Delta x} = e^{x}\cdot\frac{e^{\Delta x} - 1}{\Delta x}"),
    ("known", r"\lim_{t \to 0}\frac{e^{t} - 1}{t} = 1"), ("lim", r"f'(x) = e^{x}\cdot 1 = e^{x}")], r"(e^{x})' = e^{x}",
    [("q", "exp(x)", "x", "exp(x)*(exp(D)-1)/D", "exp(x)")])
add(3, "d", r"f(x) = e^{2x}", [
    ("def", DEF), ("factor", r"\frac{\Delta f}{\Delta x} = \frac{e^{2x + 2\Delta x} - e^{2x}}{\Delta x} = e^{2x}\cdot\frac{e^{2\Delta x} - 1}{\Delta x} = 2e^{2x}\cdot\frac{e^{2\Delta x} - 1}{2\Delta x}"),
    ("known", r"t = 2\Delta x \to 0:\qquad \frac{e^{t} - 1}{t} \to 1"), ("lim", r"f'(x) = 2e^{2x}")], r"(e^{2x})' = 2e^{2x}",
    [("q", "exp(2*x)", "x", "2*exp(2*x)*(exp(2*D)-1)/(2*D)", "2*exp(2*x)")])
add(3, "d", r"f(x) = \sin x", [
    ("def", DEF), ("trig", r"\Delta f = \sin(x + \Delta x) - \sin x = 2\cos\!\Big(x + \frac{\Delta x}{2}\Big)\sin\frac{\Delta x}{2}"),
    ("cut", r"\frac{\Delta f}{\Delta x} = \cos\!\Big(x + \frac{\Delta x}{2}\Big)\cdot\frac{\sin(\Delta x/2)}{\Delta x/2}"),
    ("known", r"\lim_{t \to 0}\frac{\sin t}{t} = 1"), ("lim", r"f'(x) = \cos x\cdot 1 = \cos x")], r"(\sin x)' = \cos x",
    [("q", "sin(x)", "x", "cos(x+D/2)*sin(D/2)/(D/2)", "cos(x)")])
add(3, "d", r"f(x) = \cos x", [
    ("def", DEF), ("trig", r"\Delta f = \cos(x + \Delta x) - \cos x = -2\sin\!\Big(x + \frac{\Delta x}{2}\Big)\sin\frac{\Delta x}{2}"),
    ("cut", r"\frac{\Delta f}{\Delta x} = -\sin\!\Big(x + \frac{\Delta x}{2}\Big)\cdot\frac{\sin(\Delta x/2)}{\Delta x/2}"),
    ("known", r"\lim_{t \to 0}\frac{\sin t}{t} = 1"), ("lim", r"f'(x) = -\sin x")], r"(\cos x)' = -\sin x",
    [("q", "cos(x)", "x", "-sin(x+D/2)*sin(D/2)/(D/2)", "-sin(x)")])
add(4, "d", r"f(x) = \ln x,\quad x > 0", [
    ("def", DEF), ("factor", r"\Delta f = \ln(x + \Delta x) - \ln x = \ln\Big(1 + \frac{\Delta x}{x}\Big),\qquad \frac{\Delta f}{\Delta x} = \frac1x\cdot\frac{\ln(1 + \Delta x/x)}{\Delta x/x}"),
    ("known", r"\lim_{t \to 0}\frac{\ln(1 + t)}{t} = 1"), ("lim", r"f'(x) = \frac1x\cdot 1 = \frac1x")], r"(\ln x)' = \frac1x",
    [("q", "log(x)", "x", "(1/x)*log(1+D/x)/(D/x)", "1/x")])
add(4, "d", r"f(x) = \sin 3x", [
    ("def", DEF), ("trig", r"\Delta f = \sin(3x + 3\Delta x) - \sin 3x = 2\cos\!\Big(3x + \frac{3\Delta x}{2}\Big)\sin\frac{3\Delta x}{2}"),
    ("cut", r"\frac{\Delta f}{\Delta x} = 3\cos\!\Big(3x + \frac{3\Delta x}{2}\Big)\cdot\frac{\sin(3\Delta x/2)}{3\Delta x/2}"),
    ("lim", r"f'(x) = 3\cos 3x\cdot 1 = 3\cos 3x")], r"(\sin 3x)' = 3\cos 3x",
    [("q", "sin(3*x)", "x", "3*cos(3*x+3*D/2)*sin(3*D/2)/(3*D/2)", "3*cos(3*x)")])
add(4, "d", r"f(x) = 2^{x}", [
    ("def", DEF), ("factor", r"\frac{\Delta f}{\Delta x} = \frac{2^{x + \Delta x} - 2^{x}}{\Delta x} = 2^{x}\cdot\frac{2^{\Delta x} - 1}{\Delta x}"),
    ("known", r"\lim_{t \to 0}\frac{a^{t} - 1}{t} = \ln a\qquad\big(a^{t} = e^{t\ln a}\big)"), ("lim", r"f'(x) = 2^{x}\ln 2")], r"(2^{x})' = 2^{x}\ln 2",
    [("q", "2**x", "x", "2**x*(2**D-1)/D", "2**x*log(2)")])

# ===== 25–28: does the derivative exist? =====
add(4, "ex", r"f(x) = |x|", [
    ("point", r"\frac{f(0 + \Delta x) - f(0)}{\Delta x} = \frac{|\Delta x|}{\Delta x}"),
    ("right", r"\Delta x > 0:\quad \frac{\Delta x}{\Delta x} = 1\ \to\ 1"), ("left", r"\Delta x < 0:\quad \frac{-\Delta x}{\Delta x} = -1\ \to\ -1"),
    ("nolim", r"1 \ne -1")], r"f'(0)\ \text{—}", [("side", "Abs(D)/D", "1", "-1")])
add(4, "ex", r"f(x) = x\,|x|", [
    ("point", r"\frac{f(\Delta x) - f(0)}{\Delta x} = \frac{\Delta x\,|\Delta x|}{\Delta x} = |\Delta x|"),
    ("lim", r"f'(0) = \lim_{\Delta x \to 0}|\Delta x| = 0")], r"f'(0) = 0", [("side", "D*Abs(D)/D", "0", "0")])
add(5, "ex", r"f(x) = \sqrt[3]{x}", [
    ("point", r"\frac{f(\Delta x) - f(0)}{\Delta x} = \frac{\sqrt[3]{\Delta x}}{\Delta x} = \frac{1}{\sqrt[3]{\Delta x^2}}"),
    ("infinite", r"\Delta x \to 0:\quad \frac{1}{\sqrt[3]{\Delta x^2}} \to +\infty")], r"f'(0)\ \text{—}\ (+\infty)", [("side", "1/Abs(D)**(2/S(3))", "oo", "oo")])
add(5, "ex", r"f(x) = \begin{cases} x^2\sin\frac1x, & x \ne 0\\ 0, & x = 0\end{cases}", [
    ("point", r"\frac{f(\Delta x) - f(0)}{\Delta x} = \frac{\Delta x^2\sin(1/\Delta x)}{\Delta x} = \Delta x\,\sin\frac{1}{\Delta x}"),
    ("squeeze", r"-|\Delta x| \le \Delta x\,\sin\frac{1}{\Delta x} \le |\Delta x|,\qquad |\Delta x| \to 0"), ("lim", r"f'(0) = 0")], r"f'(0) = 0",
    [("side", "D*sin(1/D)", "0", "0")])

# ===== 29–37: partial derivatives =====
PX = r"\frac{\partial f}{\partial x} = \lim_{\Delta x \to 0}\frac{f(x + \Delta x,\ y) - f(x,\ y)}{\Delta x}"
PY = r"\frac{\partial f}{\partial y} = \lim_{\Delta y \to 0}\frac{f(x,\ y + \Delta y) - f(x,\ y)}{\Delta y}"
add(3, "pd", r"f(x, y) = x^2 y", [
    ("incx", r"\Delta_x f = (x + \Delta x)^2 y - x^2 y = (2x\,\Delta x + \Delta x^2)\,y"), ("limx", r"\frac{\partial f}{\partial x} = \lim_{\Delta x \to 0}(2x + \Delta x)\,y = 2xy"),
    ("incy", r"\Delta_y f = x^2(y + \Delta y) - x^2 y = x^2\Delta y"), ("limy", r"\frac{\partial f}{\partial y} = \lim_{\Delta y \to 0}x^2 = x^2")],
    r"f_x = 2xy,\quad f_y = x^2", [("q2", "x**2*y", "x", "(2*x+D)*y", "2*x*y"), ("q2", "x**2*y", "y", "x**2", "x**2")])
add(3, "pd", r"f(x, y) = x^2 + 3xy", [
    ("incx", r"\Delta_x f = (x + \Delta x)^2 + 3(x + \Delta x)y - x^2 - 3xy = 2x\,\Delta x + \Delta x^2 + 3y\,\Delta x"), ("limx", r"\frac{\partial f}{\partial x} = \lim_{\Delta x \to 0}(2x + 3y + \Delta x) = 2x + 3y"),
    ("incy", r"\Delta_y f = x^2 + 3x(y + \Delta y) - x^2 - 3xy = 3x\,\Delta y"), ("limy", r"\frac{\partial f}{\partial y} = 3x")],
    r"f_x = 2x + 3y,\quad f_y = 3x", [("q2", "x**2+3*x*y", "x", "2*x+3*y+D", "2*x+3*y"), ("q2", "x**2+3*x*y", "y", "3*x", "3*x")])
add(3, "pd", r"f(x, y) = x^2 y + y^3", [
    ("incx", r"\Delta_x f = (x + \Delta x)^2 y + y^3 - x^2 y - y^3 = (2x\,\Delta x + \Delta x^2)\,y"), ("limx", r"\frac{\partial f}{\partial x} = \lim_{\Delta x \to 0}(2x + \Delta x)\,y = 2xy"),
    ("incy", r"\Delta_y f = x^2\Delta y + (y + \Delta y)^3 - y^3 = x^2\Delta y + 3y^2\Delta y + 3y\,\Delta y^2 + \Delta y^3"),
    ("limy", r"\frac{\partial f}{\partial y} = \lim_{\Delta y \to 0}\big(x^2 + 3y^2 + 3y\,\Delta y + \Delta y^2\big) = x^2 + 3y^2")],
    r"f_x = 2xy,\quad f_y = x^2 + 3y^2", [("q2", "x**2*y+y**3", "x", "(2*x+D)*y", "2*x*y"), ("q2", "x**2*y+y**3", "y", "x**2+3*y**2+3*y*D+D**2", "x**2+3*y**2")])
add(3, "pd", r"f(x, y) = x^3 + y^3", [
    ("incx", r"\Delta_x f = (x + \Delta x)^3 - x^3 = 3x^2\Delta x + 3x\,\Delta x^2 + \Delta x^3"), ("limx", r"\frac{\partial f}{\partial x} = 3x^2"),
    ("incy", r"\Delta_y f = (y + \Delta y)^3 - y^3 = 3y^2\Delta y + 3y\,\Delta y^2 + \Delta y^3"), ("limy", r"\frac{\partial f}{\partial y} = 3y^2")],
    r"f_x = 3x^2,\quad f_y = 3y^2", [("q2", "x**3+y**3", "x", "3*x**2+3*x*D+D**2", "3*x**2"), ("q2", "x**3+y**3", "y", "3*y**2+3*y*D+D**2", "3*y**2")])
add(3, "pd", r"f(x, y) = xy^2 + y", [
    ("incx", r"\Delta_x f = (x + \Delta x)y^2 + y - xy^2 - y = y^2\Delta x"), ("limx", r"\frac{\partial f}{\partial x} = y^2"),
    ("incy", r"\Delta_y f = x(y + \Delta y)^2 + (y + \Delta y) - xy^2 - y = x(2y\,\Delta y + \Delta y^2) + \Delta y"), ("limy", r"\frac{\partial f}{\partial y} = \lim_{\Delta y \to 0}(2xy + x\,\Delta y + 1) = 2xy + 1")],
    r"f_x = y^2,\quad f_y = 2xy + 1", [("q2", "x*y**2+y", "x", "y**2", "y**2"), ("q2", "x*y**2+y", "y", "2*x*y+x*D+1", "2*x*y+1")])
add(4, "pd", r"f(x, y) = \frac{x}{y},\quad y \ne 0", [
    ("incx", r"\Delta_x f = \frac{x + \Delta x}{y} - \frac{x}{y} = \frac{\Delta x}{y}"), ("limx", r"\frac{\partial f}{\partial x} = \frac1y"),
    ("incy", r"\Delta_y f = \frac{x}{y + \Delta y} - \frac{x}{y} = \frac{-x\,\Delta y}{y\,(y + \Delta y)}"), ("limy", r"\frac{\partial f}{\partial y} = \lim_{\Delta y \to 0}\frac{-x}{y\,(y + \Delta y)} = -\frac{x}{y^2}")],
    r"f_x = \frac1y,\quad f_y = -\frac{x}{y^2}", [("q2", "x/y", "x", "1/y", "1/y"), ("q2", "x/y", "y", "-x/(y*(y+D))", "-x/y**2")])
add(4, "pd", r"f(x, y) = e^{x + y}", [
    ("incx", r"\Delta_x f = e^{x + \Delta x + y} - e^{x + y} = e^{x + y}\big(e^{\Delta x} - 1\big)"), ("limx", r"\frac{\partial f}{\partial x} = e^{x + y}\lim_{\Delta x \to 0}\frac{e^{\Delta x} - 1}{\Delta x} = e^{x + y}"),
    ("incy", r"\Delta_y f = e^{x + y}\big(e^{\Delta y} - 1\big)"), ("limy", r"\frac{\partial f}{\partial y} = e^{x + y}")],
    r"f_x = f_y = e^{x + y}", [("q2", "exp(x+y)", "x", "exp(x+y)*(exp(D)-1)/D", "exp(x+y)"), ("q2", "exp(x+y)", "y", "exp(x+y)*(exp(D)-1)/D", "exp(x+y)")])
add(4, "pd", r"f(x, y, z) = xyz", [
    ("incx", r"\Delta_x f = (x + \Delta x)yz - xyz = yz\,\Delta x\ \Rightarrow\ \frac{\partial f}{\partial x} = yz"),
    ("incy", r"\Delta_y f = x(y + \Delta y)z - xyz = xz\,\Delta y\ \Rightarrow\ \frac{\partial f}{\partial y} = xz"),
    ("incz", r"\Delta_z f = xy(z + \Delta z) - xyz = xy\,\Delta z\ \Rightarrow\ \frac{\partial f}{\partial z} = xy")],
    r"f_x = yz,\quad f_y = xz,\quad f_z = xy", [("q2", "x*y*z", "x", "y*z", "y*z"), ("q2", "x*y*z", "y", "x*z", "x*z"), ("q2", "x*y*z", "z", "x*y", "x*y")])
add(3, "pdp", r"f(x, y) = x^2 + y^2,\quad (1;\ 2)", [
    ("incx", r"\frac{f(1 + \Delta x,\ 2) - f(1,\ 2)}{\Delta x} = \frac{(1 + \Delta x)^2 + 4 - 5}{\Delta x} = \frac{2\Delta x + \Delta x^2}{\Delta x} = 2 + \Delta x\ \to\ 2"),
    ("incy", r"\frac{f(1,\ 2 + \Delta y) - f(1,\ 2)}{\Delta y} = \frac{1 + (2 + \Delta y)^2 - 5}{\Delta y} = \frac{4\Delta y + \Delta y^2}{\Delta y} = 4 + \Delta y\ \to\ 4")],
    r"f_x(1;\ 2) = 2,\quad f_y(1;\ 2) = 4", [("qp2", "x**2+y**2", "x", {"x": 1, "y": 2}, "2+D", "2"), ("qp2", "x**2+y**2", "y", {"x": 1, "y": 2}, "4+D", "4")])

# ===== 38–41: the gradient =====
add(3, "gr", r"f(x, y) = x^2 + y^2,\quad (3;\ 4)", [
    ("incx", r"\frac{f(3 + \Delta x,\ 4) - f(3,\ 4)}{\Delta x} = \frac{(3 + \Delta x)^2 - 9}{\Delta x} = 6 + \Delta x\ \to\ 6"),
    ("incy", r"\frac{f(3,\ 4 + \Delta y) - f(3,\ 4)}{\Delta y} = \frac{(4 + \Delta y)^2 - 16}{\Delta y} = 8 + \Delta y\ \to\ 8"),
    ("grad", r"\nabla f(3;\ 4) = (6;\ 8),\qquad |\nabla f| = \sqrt{36 + 64} = 10")], r"\nabla f(3;\ 4) = (6;\ 8)",
    [("qp2", "x**2+y**2", "x", {"x": 3, "y": 4}, "6+D", "6"), ("qp2", "x**2+y**2", "y", {"x": 3, "y": 4}, "8+D", "8")])
add(4, "gr", r"f(x, y) = x^2 - xy,\quad (2;\ 1)", [
    ("incx", r"\Delta_x f = (x + \Delta x)^2 - (x + \Delta x)y - x^2 + xy = (2x - y)\Delta x + \Delta x^2\ \Rightarrow\ f_x = 2x - y"),
    ("incy", r"\Delta_y f = x^2 - x(y + \Delta y) - x^2 + xy = -x\,\Delta y\ \Rightarrow\ f_y = -x"),
    ("grad", r"\nabla f = (2x - y;\ -x),\qquad \nabla f(2;\ 1) = (3;\ -2)")], r"\nabla f(2;\ 1) = (3;\ -2)",
    [("q2", "x**2-x*y", "x", "2*x-y+D", "2*x-y"), ("q2", "x**2-x*y", "y", "-x", "-x")])
add(4, "gr", r"f(x, y, z) = x^2 + y^2 + z^2", [
    ("incx", r"\Delta_x f = (x + \Delta x)^2 - x^2 = 2x\,\Delta x + \Delta x^2\ \Rightarrow\ f_x = 2x"),
    ("incy", r"\Delta_y f = 2y\,\Delta y + \Delta y^2\ \Rightarrow\ f_y = 2y"), ("incz", r"\Delta_z f = 2z\,\Delta z + \Delta z^2\ \Rightarrow\ f_z = 2z"),
    ("grad", r"\nabla f = (2x;\ 2y;\ 2z) = 2\,(x;\ y;\ z)")], r"\nabla f = (2x;\ 2y;\ 2z)",
    [("q2", "x**2+y**2+z**2", "x", "2*x+D", "2*x"), ("q2", "x**2+y**2+z**2", "y", "2*y+D", "2*y"), ("q2", "x**2+y**2+z**2", "z", "2*z+D", "2*z")])
add(2, "gr", r"f(x) = x^3", [
    ("def", DEF), ("cut", r"\frac{(x + \Delta x)^3 - x^3}{\Delta x} = 3x^2 + 3x\,\Delta x + \Delta x^2\ \to\ 3x^2"),
    ("grad1", r"\nabla f(x) = \Big(\frac{df}{dx}\Big) = (3x^2) = f'(x)")], r"\nabla f = (3x^2) = f'(x)", [("q", "x**3", "x", "3*x**2+3*x*D+D**2", "3*x**2")])

# ===== 42–46: the directional derivative, the differential, descent =====
add(4, "dir", r"f(x, y) = x^2 + y^2,\quad (1;\ 1),\quad \mathbf{u} = \big(\tfrac35;\ \tfrac45\big)", [
    ("dirdef", r"D_{\mathbf{u}} f(1;\ 1) = \lim_{t \to 0}\frac{f\big(1 + \frac35 t,\ 1 + \frac45 t\big) - f(1,\ 1)}{t}"),
    ("dirinc", r"\frac{\big(1 + \frac35 t\big)^2 + \big(1 + \frac45 t\big)^2 - 2}{t} = \frac{\frac{14}{5}t + t^2}{t} = \frac{14}{5} + t"),
    ("dirlim", r"D_{\mathbf{u}} f = \frac{14}{5}"), ("dircheck", r"\nabla f(1;\ 1) = (2;\ 2),\qquad (2;\ 2)\cdot\big(\tfrac35;\ \tfrac45\big) = \frac65 + \frac85 = \frac{14}{5}")],
    r"D_{\mathbf{u}} f = \frac{14}{5}", [("dir", "x**2+y**2", {"x": 1, "y": 1}, ("3/5", "4/5"), "14/5+t", "14/5")])
add(4, "dir", r"f(x, y) = xy,\quad (1;\ 2),\quad \mathbf{v} = (1;\ 1)", [
    ("unit", r"|\mathbf{v}| = \sqrt2,\qquad \mathbf{u} = \Big(\frac{1}{\sqrt2};\ \frac{1}{\sqrt2}\Big)"),
    ("dirinc", r"a = \frac{t}{\sqrt2}:\quad \frac{(1 + a)(2 + a) - 2}{t} = \frac{3a + a^2}{t} = \frac{3}{\sqrt2} + \frac{t}{2}"),
    ("dirlim", r"D_{\mathbf{u}} f = \frac{3}{\sqrt2}"), ("dircheck", r"\nabla f = (y;\ x) = (2;\ 1),\qquad (2;\ 1)\cdot\Big(\frac{1}{\sqrt2};\ \frac{1}{\sqrt2}\Big) = \frac{3}{\sqrt2}")],
    r"D_{\mathbf{u}} f = \frac{3}{\sqrt2} \approx 2{,}121", [("dir", "x*y", {"x": 1, "y": 2}, ("1/sqrt(2)", "1/sqrt(2)"), "3/sqrt(2)+t/2", "3/sqrt(2)")])
add(4, "lin", r"f(x, y) = x^2 + y^2,\quad (3;\ 4),\quad \Delta x = 0{,}1,\ \Delta y = -0{,}2", [
    ("gradpt", r"f_x = 2x = 6,\qquad f_y = 2y = 8"), ("lin", r"df = 6\cdot 0{,}1 + 8\cdot(-0{,}2) = 0{,}6 - 1{,}6 = -1"),
    ("exact", r"\Delta f = f(3{,}1;\ 3{,}8) - f(3;\ 4) = 9{,}61 + 14{,}44 - 25 = -0{,}95;\qquad \Delta f - df = \Delta x^2 + \Delta y^2 = 0{,}05")],
    r"df = -1,\quad \Delta f = -0{,}95", [("num", "x**2+y**2", {"x": 3, "y": 4}, (0.1, -0.2), -1, -0.95)])
add(5, "gd", r"f(x, y) = x^2 + y^2,\quad \mathbf{p} = (3;\ 4),\quad \eta = 0{,}1", [
    ("gradpt", r"\nabla f(3;\ 4) = (6;\ 8)"), ("step", r"\mathbf{p} \leftarrow (3;\ 4) - 0{,}1\cdot(6;\ 8) = (2{,}4;\ 3{,}2)"),
    ("value", r"f(3;\ 4) = 25\ \longrightarrow\ f(2{,}4;\ 3{,}2) = 5{,}76 + 10{,}24 = 16")], r"\mathbf{p} = (2{,}4;\ 3{,}2),\quad f: 25 \to 16",
    [("gd", "x**2+y**2", (3, 4), 0.1, (2.4, 3.2), 25, 16)])
add(5, "gd", r"f(x, y) = (x - 1)^2 + 2y^2,\quad \mathbf{p} = (3;\ 1),\quad \eta = 0{,}25", [
    ("gradpt", r"f_x = 2(x - 1) = 4,\qquad f_y = 4y = 4,\qquad \nabla f(3;\ 1) = (4;\ 4)"),
    ("step", r"\mathbf{p} \leftarrow (3;\ 1) - 0{,}25\cdot(4;\ 4) = (2;\ 0)"), ("value", r"f(3;\ 1) = 4 + 2 = 6\ \longrightarrow\ f(2;\ 0) = 1")],
    r"\mathbf{p} = (2;\ 0),\quad f: 6 \to 1", [("gd", "(x-1)**2+2*y**2", (3, 1), 0.25, (2, 0), 6, 1)])

NOTES = {}


def verify():
    import sympy as sp
    x, y, z, t, Dl = sp.symbols("x y z t D", real=True)
    V = dict(x=x, y=y, z=z, t=t, D=Dl, S=sp.S, oo=sp.oo)
    P = lambda e: sp.sympify(e, locals=V)
    pts = [{x: 0.7, y: 1.3, z: -0.4}, {x: 2.1, y: -0.6, z: 1.7}]

    def same(a, b, subs_list):
        return all(abs(complex((a - b).subs(s).evalf())) < 1e-9 for s in subs_list)
    assert len(D) >= 40, len(D)
    for d in D:
        for c in d["checks"]:
            k = c[0]
            if k in ("q", "q2"):
                f, var, q, lim = P(c[1]), V[c[2]], P(c[3]), P(c[4])
                quot = (f.subs(var, var + Dl) - f) / Dl
                subs = [{**p, Dl: dv} for p in pts for dv in (0.013, -0.21)]
                assert same(quot, q, subs), (d["n"], c)
                assert sp.simplify(sp.limit(q, Dl, 0) - lim) == 0, (d["n"], c, sp.limit(q, Dl, 0))
                assert sp.simplify(sp.diff(f, var) - lim) == 0, (d["n"], c)
            elif k == "qp":
                f, var, x0, q, lim = P(c[1]), V[c[2]], P(c[3]), P(c[4]), P(c[5])
                quot = (f.subs(var, x0 + Dl) - f.subs(var, x0)) / Dl
                assert same(quot, q, [{Dl: 0.013}, {Dl: -0.21}]), (d["n"], c)
                assert sp.limit(q, Dl, 0) == lim and sp.simplify(sp.diff(f, var).subs(var, x0) - lim) == 0, (d["n"], c)
            elif k == "qp2":
                f, var, pt, q, lim = P(c[1]), V[c[2]], {V[a]: b for a, b in c[3].items()}, P(c[4]), P(c[5])
                quot = (f.subs(var, var + Dl).subs(pt) - f.subs(pt)) / Dl
                assert same(quot, q, [{Dl: 0.013}, {Dl: -0.21}]), (d["n"], c)
                assert sp.limit(q, Dl, 0) == lim and sp.diff(f, var).subs(pt) == lim, (d["n"], c)
            elif k == "side":
                q, r, l = P(c[1]), P(c[2]), P(c[3])
                assert sp.limit(q, Dl, 0, "+") == r and sp.limit(q, Dl, 0, "-") == l, (d["n"], c)
            elif k == "dir":
                f, pt, (ux, uy), q, lim = P(c[1]), {V[a]: b for a, b in c[2].items()}, c[3], P(c[4]), P(c[5])
                ux, uy = P(ux), P(uy)
                assert sp.simplify(ux ** 2 + uy ** 2 - 1) == 0
                x0, y0 = pt[x], pt[y]
                quot = (f.subs({x: x0 + ux * t, y: y0 + uy * t}) - f.subs(pt)) / t
                assert sp.simplify(quot - q) == 0, (d["n"], c)
                assert sp.simplify(sp.limit(q, t, 0) - lim) == 0
                assert sp.simplify(sp.diff(f, x).subs(pt) * ux + sp.diff(f, y).subs(pt) * uy - lim) == 0, (d["n"], c)
            elif k == "num":
                f, pt, (dx, dy), dfv, Dfv = P(c[1]), {V[a]: b for a, b in c[2].items()}, c[3], c[4], c[5]
                df = float(sp.diff(f, x).subs(pt) * dx + sp.diff(f, y).subs(pt) * dy)
                Df = float(f.subs({x: pt[x] + dx, y: pt[y] + dy}) - f.subs(pt))
                assert abs(df - dfv) < 1e-12 and abs(Df - Dfv) < 1e-12, (d["n"], df, Df)
            elif k == "gd":
                f, (px, py), eta, new, f0, f1 = P(c[1]), c[2], c[3], c[4], c[5], c[6]
                gx, gy = (float(sp.diff(f, v).subs({x: px, y: py})) for v in (x, y))
                nx, ny = px - eta * gx, py - eta * gy
                assert abs(nx - new[0]) < 1e-12 and abs(ny - new[1]) < 1e-12, (d["n"], nx, ny)
                assert abs(float(f.subs({x: px, y: py})) - f0) < 1e-12 and abs(float(f.subs({x: nx, y: ny})) - f1) < 1e-9, (d["n"],)
            else:
                raise ValueError(k)
    return True


EN_TEX = [(r";\ ", r",\ "), ("{,}", ".")]


def localize(t, lang):
    """English writes a decimal point and separates coordinates with a comma."""
    if lang == "en":
        for a, b in EN_TEX:
            t = t.replace(a, b)
    return t


def drill_blocks(lang):
    out = []
    for d in D:
        if d["n"] in GROUPS:
            out.append(("h3", GROUPS[d["n"]][lang]))
        out.append(("drill", dict(n=d["n"], level=d["level"], task=localize(TASKS[d["task"]][lang], lang), f=localize(d["f"], lang),
                                  steps=[(localize(LABELS[k][lang], lang), localize(tex, lang)) for k, tex in d["steps"]],
                                  ans=localize(d["ans"], lang), note=NOTES.get(d["n"], {}).get(lang))))
    return out


if __name__ == "__main__":
    print("drills ok:", len(D)) if verify() else None
