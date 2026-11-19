"""56 worked examples on the chain rule for the article "The chain rule" (tools/content_chain.py).

Each drill is language-neutral data: the formulas (TeX) and the keys of step captions; the captions,
tasks and notes in three languages live in LABELS / TASKS / NOTES. Every answer is verified with SymPy
by verify() — run:  python3 tools/chain_drills.py
"""

# ---- step captions: the explanation of every step, in three languages ----
LABELS = {
    "split": {"ru": "Разбиваем функцию на слои: находим внешнюю функцию $f(u)$ и внутреннюю $u = g(x)$ — то, что стоит «внутри».",
              "en": "Split the function into layers: find the outer function $f(u)$ and the inner one $u = g(x)$ — whatever sits “inside”.",
              "uz": "Funksiyani qatlamlarga ajratamiz: tashqi funksiya $f(u)$ ni va ichki $u = g(x)$ ni topamiz — «ichkarida» turgan narsa."},
    "outer": {"ru": "Дифференцируем внешнюю функцию по её собственному аргументу $u$, как будто $u$ — обычная переменная.",
              "en": "Differentiate the outer function with respect to its own argument $u$, as if $u$ were an ordinary variable.",
              "uz": "Tashqi funksiyani o‘z argumenti $u$ bo‘yicha differensiallaymiz, go‘yo $u$ oddiy o‘zgaruvchi."},
    "inner": {"ru": "Дифференцируем внутреннюю функцию по $x$.",
              "en": "Differentiate the inner function with respect to $x$.",
              "uz": "Ichki funksiyani $x$ bo‘yicha differensiallaymiz."},
    "mult": {"ru": "Перемножаем по цепному правилу $\\frac{dy}{dx} = \\frac{dy}{du}\\cdot\\frac{du}{dx}$ и возвращаем $u = g(x)$.",
             "en": "Multiply by the chain rule $\\frac{dy}{dx} = \\frac{dy}{du}\\cdot\\frac{du}{dx}$ and put back $u = g(x)$.",
             "uz": "Zanjir qoidasi $\\frac{dy}{dx} = \\frac{dy}{du}\\cdot\\frac{du}{dx}$ bo‘yicha ko‘paytiramiz va $u = g(x)$ ni qaytaramiz."},
    "simp": {"ru": "Упрощаем ответ.", "en": "Simplify the answer.", "uz": "Javobni soddalashtiramiz."},
    "chain3": {"ru": "Здесь три слоя. Обозначаем каждый, от внешнего к самому внутреннему.",
               "en": "There are three layers here. Name each of them, from the outermost to the innermost.",
               "uz": "Bu yerda uchta qatlam bor. Har birini tashqisidan eng ichkisigacha belgilaymiz."},
    "each": {"ru": "Дифференцируем каждое звено по его собственному аргументу.",
             "en": "Differentiate every link with respect to its own argument.",
             "uz": "Har bir bo‘g‘inni o‘z argumenti bo‘yicha differensiallaymiz."},
    "mult3": {"ru": "Перемножаем все звенья цепи и подставляем промежуточные переменные обратно.",
              "en": "Multiply all the links of the chain and substitute the intermediate variables back.",
              "uz": "Zanjirning barcha bo‘g‘inlarini ko‘paytiramiz va oraliq o‘zgaruvchilarni qaytarib qo‘yamiz."},
    "def": {"ru": "Записываем определение производной: предел разностного отношения при $h \\to 0$.",
            "en": "Write the definition of the derivative: the limit of the difference quotient as $h \\to 0$.",
            "uz": "Hosila ta’rifini yozamiz: $h \\to 0$ da ayirmali nisbatning limiti."},
    "defsub": {"ru": "Подставляем $f(x + h)$ и $f(x)$ и раскрываем разность в числителе.",
               "en": "Substitute $f(x + h)$ and $f(x)$ and expand the difference in the numerator.",
               "uz": "$f(x + h)$ va $f(x)$ ni qo‘yamiz va suratdagi ayirmani ochamiz."},
    "defcut": {"ru": "Делим на $h$ (при $h \\ne 0$ это законно): $h$ в знаменателе сокращается.",
               "en": "Divide by $h$ (legitimate for $h \\ne 0$): the $h$ in the denominator cancels.",
               "uz": "$h$ ga bo‘lamiz ($h \\ne 0$ da bu qonuniy): maxrajdagi $h$ qisqaradi."},
    "deflim": {"ru": "Переходим к пределу $h \\to 0$: оставшееся выражение непрерывно по $h$, поэтому просто подставляем $h = 0$.",
               "en": "Pass to the limit $h \\to 0$: what remains is continuous in $h$, so we simply substitute $h = 0$.",
               "uz": "$h \\to 0$ limitga o‘tamiz: qolgan ifoda $h$ bo‘yicha uzluksiz, shuning uchun shunchaki $h = 0$ ni qo‘yamiz."},
    "limval": {"ru": "Подставляем найденный предел.", "en": "Substitute the limit we have found.", "uz": "Topilgan limitni qo‘yamiz."},
    "prodsum": {"ru": "Подставляем в $(uv)' = u'v + uv'$ и выносим общий множитель.",
                "en": "Substitute into $(uv)' = u'v + uv'$ and factor out the common factor.",
                "uz": "$(uv)' = u'v + uv'$ ga qo‘yamiz va umumiy ko‘paytuvchini qavsdan chiqaramiz."},
    "pdxprod": {"ru": "Частная производная по $x$: $y$ — константа; $x$ стоит в двух множителях, поэтому применяем правило произведения, а внутри — цепное правило.",
                "en": "The partial derivative with respect to $x$: $y$ is a constant; $x$ appears in both factors, so we apply the product rule, and the chain rule inside it.",
                "uz": "$x$ bo‘yicha xususiy hosila: $y$ — o‘zgarmas; $x$ ikkala ko‘paytuvchida qatnashadi, shuning uchun ko‘paytma qoidasini, ichida esa zanjir qoidasini qo‘llaymiz."},
    "mult3only": {"ru": "Перемножаем звенья цепи.", "en": "Multiply the links of the chain.", "uz": "Zanjir bo‘g‘inlarini ko‘paytiramiz."},
    "conj": {"ru": "Корни в числителе мешают сократить $h$: умножаем числитель и знаменатель на сопряжённое выражение.",
             "en": "The roots in the numerator prevent cancelling $h$: multiply the numerator and the denominator by the conjugate.",
             "uz": "Suratdagi ildizlar $h$ ni qisqartirishga xalaqit beradi: surat va maxrajni qo‘shma ifodaga ko‘paytiramiz."},
    "common": {"ru": "Приводим дроби в числителе к общему знаменателю.",
               "en": "Bring the fractions in the numerator to a common denominator.",
               "uz": "Suratdagi kasrlarni umumiy maxrajga keltiramiz."},
    "known": {"ru": "Используем замечательный предел (его доказывают один раз, отдельно).",
              "en": "Use a standard limit (it is proved once, separately).",
              "uz": "Ajoyib limitdan foydalanamiz (u bir marta, alohida isbotlanadi)."},
    "check": {"ru": "Проверяем цепным правилом: ответ тот же.",
              "en": "Check with the chain rule: the answer is the same.",
              "uz": "Zanjir qoidasi bilan tekshiramiz: javob o‘sha."},
    "pdx": {"ru": "Частная производная по $x$: переменную $y$ считаем постоянным числом и применяем цепное правило по $x$.",
            "en": "The partial derivative with respect to $x$: treat $y$ as a constant number and apply the chain rule in $x$.",
            "uz": "$x$ bo‘yicha xususiy hosila: $y$ ni o‘zgarmas son deb hisoblaymiz va $x$ bo‘yicha zanjir qoidasini qo‘llaymiz."},
    "pdy": {"ru": "Частная производная по $y$: теперь постоянная — $x$.",
            "en": "The partial derivative with respect to $y$: now $x$ is the constant.",
            "uz": "$y$ bo‘yicha xususiy hosila: endi o‘zgarmas — $x$."},
    "pdz": {"ru": "Частная производная по $z$: постоянные — $x$ и $y$.",
            "en": "The partial derivative with respect to $z$: $x$ and $y$ are constants.",
            "uz": "$z$ bo‘yicha xususiy hosila: o‘zgarmaslar — $x$ va $y$."},
    "pdef": {"ru": "Определение частной производной по $x$: даём приращение $h$ только переменной $x$, а $y$ не трогаем.",
             "en": "The definition of the partial derivative in $x$: give the increment $h$ to $x$ only and leave $y$ untouched.",
             "uz": "$x$ bo‘yicha xususiy hosila ta’rifi: $h$ orttirmani faqat $x$ ga beramiz, $y$ ga tegmaymiz."},
    "pdefy": {"ru": "То же по $y$: приращение получает только $y$.",
              "en": "The same in $y$: only $y$ gets the increment.",
              "uz": "$y$ bo‘yicha xuddi shunday: orttirmani faqat $y$ oladi."},
    "tree": {"ru": "Строим дерево зависимостей: от $z$ к переменной дифференцирования ведут несколько путей.",
             "en": "Draw the dependency tree: several paths lead from $z$ to the variable we differentiate by.",
             "uz": "Bog‘liqlik daraxtini chizamiz: $z$ dan differensiallash o‘zgaruvchisigacha bir nechta yo‘l boradi."},
    "pouter": {"ru": "Частные производные внешней функции по промежуточным переменным.",
               "en": "The partial derivatives of the outer function with respect to the intermediate variables.",
               "uz": "Tashqi funksiyaning oraliq o‘zgaruvchilar bo‘yicha xususiy hosilalari."},
    "pinner": {"ru": "Производные промежуточных переменных.",
               "en": "The derivatives of the intermediate variables.",
               "uz": "Oraliq o‘zgaruvchilarning hosilalari."},
    "sum": {"ru": "Многомерное цепное правило: вдоль каждого пути перемножаем производные, вклады всех путей складываем.",
            "en": "The multivariable chain rule: multiply the derivatives along each path and add the contributions of all paths.",
            "uz": "Ko‘p o‘lchovli zanjir qoidasi: har bir yo‘l bo‘ylab hosilalarni ko‘paytiramiz, barcha yo‘llar hissalarini qo‘shamiz."},
    "subs": {"ru": "Подставляем промежуточные переменные через исходные и упрощаем.",
             "en": "Express the intermediate variables through the original ones and simplify.",
             "uz": "Oraliq o‘zgaruvchilarni dastlabki o‘zgaruvchilar orqali ifodalab, soddalashtiramiz."},
    "verify": {"ru": "Проверка: сначала подставляем, потом дифференцируем как функцию одной переменной — ответ совпадает.",
               "en": "Check: substitute first, then differentiate as a function of one variable — the answer matches.",
               "uz": "Tekshiruv: avval qo‘yamiz, so‘ng bir o‘zgaruvchili funksiya kabi differensiallaymiz — javob mos keladi."},
    "total": {"ru": "Полная производная: прямой вклад $x$ плюс вклад через $y = y(x)$.",
              "en": "The total derivative: the direct contribution of $x$ plus the contribution through $y = y(x)$.",
              "uz": "To‘liq hosila: $x$ ning bevosita hissasi va $y = y(x)$ orqali hissa."},
    "impl": {"ru": "Дифференцируем обе части равенства по $x$, помня, что $y = y(x)$: по цепному правилу $(\\varphi(y))' = \\varphi'(y)\\,y'$.",
             "en": "Differentiate both sides of the equation with respect to $x$, remembering that $y = y(x)$: by the chain rule $(\\varphi(y))' = \\varphi'(y)\\,y'$.",
             "uz": "Tenglikning ikkala tomonini $x$ bo‘yicha differensiallaymiz, $y = y(x)$ ekanini yodda tutib: zanjir qoidasiga ko‘ra $(\\varphi(y))' = \\varphi'(y)\\,y'$."},
    "solve": {"ru": "Выражаем $y'$.", "en": "Solve for $y'$.", "uz": "$y'$ ni ifodalaymiz."},
    "point": {"ru": "Подставляем точку.", "en": "Substitute the point.", "uz": "Nuqtani qo‘yamiz."},
    "prod": {"ru": "Здесь произведение: применяем правило произведения $(uv)' = u'v + uv'$, а внутри — цепное правило.",
             "en": "Here we have a product: apply the product rule $(uv)' = u'v + uv'$, and the chain rule inside it.",
             "uz": "Bu yerda ko‘paytma: ko‘paytma qoidasi $(uv)' = u'v + uv'$ ni, ichida esa zanjir qoidasini qo‘llaymiz."},
    "layers": {"ru": "Обозначаем слои сети как цепочку функций.",
               "en": "Write the layers of the model as a chain of functions.",
               "uz": "Model qatlamlarini funksiyalar zanjiri sifatida belgilaymiz."},
}

TASKS = {
    "d": {"ru": "Найдите производную.", "en": "Find the derivative.", "uz": "Hosilani toping."},
    "def": {"ru": "Найдите производную по определению, затем проверьте цепным правилом.", "en": "Find the derivative from the definition, then check it with the chain rule.", "uz": "Hosilani ta’rif bo‘yicha toping, so‘ng zanjir qoidasi bilan tekshiring."},
    "pd": {"ru": "Найдите частные производные.", "en": "Find the partial derivatives.", "uz": "Xususiy hosilalarni toping."},
    "pdef": {"ru": "Найдите частные производные по определению.", "en": "Find the partial derivatives from the definition.", "uz": "Xususiy hosilalarni ta’rif bo‘yicha toping."},
    "dt": {"ru": "Найдите $\\frac{dz}{dt}$ по многомерному цепному правилу.", "en": "Find $\\frac{dz}{dt}$ by the multivariable chain rule.", "uz": "Ko‘p o‘lchovli zanjir qoidasi bilan $\\frac{dz}{dt}$ ni toping."},
    "dst": {"ru": "Найдите $\\frac{\\partial z}{\\partial s}$ и $\\frac{\\partial z}{\\partial t}$.", "en": "Find $\\frac{\\partial z}{\\partial s}$ and $\\frac{\\partial z}{\\partial t}$.", "uz": "$\\frac{\\partial z}{\\partial s}$ va $\\frac{\\partial z}{\\partial t}$ ni toping."},
    "dLt": {"ru": "Найдите $\\frac{dL}{dt}$ по многомерному цепному правилу.", "en": "Find $\\frac{dL}{dt}$ by the multivariable chain rule.", "uz": "Ko‘p o‘lchovli zanjir qoidasi bilan $\\frac{dL}{dt}$ ni toping."},
    "total": {"ru": "Найдите полную производную $\\frac{dz}{dx}$.", "en": "Find the total derivative $\\frac{dz}{dx}$.", "uz": "To‘liq hosila $\\frac{dz}{dx}$ ni toping."},
    "impl": {"ru": "Найдите $y'$ для функции, заданной неявно.", "en": "Find $y'$ for the implicitly defined function.", "uz": "Oshkormas berilgan funksiya uchun $y'$ ni toping."},
    "nn": {"ru": "Найдите градиент потерь по параметрам.", "en": "Find the gradient of the loss with respect to the parameters.", "uz": "Yo‘qotishning parametrlar bo‘yicha gradiyentini toping."},
}

# ---- the drills: (n, level 1–5, task, statement TeX, [(label key, TeX), …], answer TeX, checks) ----
# checks: list of (function (SymPy string), variable, claimed derivative (SymPy string)) — or special tuples, see verify()
D = []
def add(level, task, f, steps, ans, checks):
    D.append(dict(n=len(D) + 1, level=level, task=task, f=f, steps=steps, ans=ans, checks=checks))

# ===== level 1: one link, the basic functions =====
add(1, "d", r"y = (3x + 1)^5", [
    ("split", r"y = u^5,\qquad u = 3x + 1"), ("outer", r"\frac{dy}{du} = 5u^4"), ("inner", r"\frac{du}{dx} = 3"),
    ("mult", r"\frac{dy}{dx} = 5u^4\cdot 3 = 15(3x + 1)^4")], r"y' = 15(3x + 1)^4", [("(3*x+1)**5", "x", "15*(3*x+1)**4")])
add(1, "d", r"y = \sqrt{2x + 1}", [
    ("split", r"y = \sqrt{u} = u^{1/2},\qquad u = 2x + 1"), ("outer", r"\frac{dy}{du} = \tfrac12 u^{-1/2} = \frac{1}{2\sqrt{u}}"), ("inner", r"\frac{du}{dx} = 2"),
    ("mult", r"\frac{dy}{dx} = \frac{1}{2\sqrt{2x + 1}}\cdot 2 = \frac{1}{\sqrt{2x + 1}}")], r"y' = \frac{1}{\sqrt{2x + 1}}", [("sqrt(2*x+1)", "x", "1/sqrt(2*x+1)")])
add(1, "d", r"y = e^{3x}", [
    ("split", r"y = e^u,\qquad u = 3x"), ("outer", r"\frac{dy}{du} = e^u"), ("inner", r"\frac{du}{dx} = 3"),
    ("mult", r"\frac{dy}{dx} = e^{3x}\cdot 3 = 3e^{3x}")], r"y' = 3e^{3x}", [("exp(3*x)", "x", "3*exp(3*x)")])
add(1, "d", r"y = \sin 5x", [
    ("split", r"y = \sin u,\qquad u = 5x"), ("outer", r"\frac{dy}{du} = \cos u"), ("inner", r"\frac{du}{dx} = 5"),
    ("mult", r"\frac{dy}{dx} = 5\cos 5x")], r"y' = 5\cos 5x", [("sin(5*x)", "x", "5*cos(5*x)")])
add(1, "d", r"y = \ln(x^2 + 1)", [
    ("split", r"y = \ln u,\qquad u = x^2 + 1"), ("outer", r"\frac{dy}{du} = \frac{1}{u}"), ("inner", r"\frac{du}{dx} = 2x"),
    ("mult", r"\frac{dy}{dx} = \frac{1}{x^2 + 1}\cdot 2x = \frac{2x}{x^2 + 1}")], r"y' = \frac{2x}{x^2 + 1}", [("log(x**2+1)", "x", "2*x/(x**2+1)")])
add(1, "d", r"y = (x^2 + 1)^3", [
    ("split", r"y = u^3,\qquad u = x^2 + 1"), ("outer", r"\frac{dy}{du} = 3u^2"), ("inner", r"\frac{du}{dx} = 2x"),
    ("mult", r"\frac{dy}{dx} = 3(x^2 + 1)^2\cdot 2x = 6x(x^2 + 1)^2")], r"y' = 6x(x^2 + 1)^2", [("(x**2+1)**3", "x", "6*x*(x**2+1)**2")])
add(1, "d", r"y = \cos(x^2)", [
    ("split", r"y = \cos u,\qquad u = x^2"), ("outer", r"\frac{dy}{du} = -\sin u"), ("inner", r"\frac{du}{dx} = 2x"),
    ("mult", r"\frac{dy}{dx} = -\sin(x^2)\cdot 2x = -2x\sin(x^2)")], r"y' = -2x\sin(x^2)", [("cos(x**2)", "x", "-2*x*sin(x**2)")])
add(1, "d", r"y = e^{-x^2}", [
    ("split", r"y = e^u,\qquad u = -x^2"), ("outer", r"\frac{dy}{du} = e^u"), ("inner", r"\frac{du}{dx} = -2x"),
    ("mult", r"\frac{dy}{dx} = e^{-x^2}\cdot(-2x) = -2x\,e^{-x^2}")], r"y' = -2x\,e^{-x^2}", [("exp(-x**2)", "x", "-2*x*exp(-x**2)")])
add(1, "d", r"y = \frac{1}{(2x - 1)^2}", [
    ("split", r"y = u^{-2},\qquad u = 2x - 1"), ("outer", r"\frac{dy}{du} = -2u^{-3}"), ("inner", r"\frac{du}{dx} = 2"),
    ("mult", r"\frac{dy}{dx} = -2(2x - 1)^{-3}\cdot 2 = -\frac{4}{(2x - 1)^3}")], r"y' = -\frac{4}{(2x - 1)^3}", [("1/(2*x-1)**2", "x", "-4/(2*x-1)**3")])
add(1, "d", r"y = \operatorname{tg} 4x", [
    ("split", r"y = \operatorname{tg} u,\qquad u = 4x"), ("outer", r"\frac{dy}{du} = \frac{1}{\cos^2 u}"), ("inner", r"\frac{du}{dx} = 4"),
    ("mult", r"\frac{dy}{dx} = \frac{4}{\cos^2 4x}")], r"y' = \frac{4}{\cos^2 4x}", [("tan(4*x)", "x", "4/cos(4*x)**2")])

# ===== level 2: a power of a function, a function inside a log or a root =====
add(2, "d", r"y = \sin^2 x", [
    ("split", r"y = u^2,\qquad u = \sin x"), ("outer", r"\frac{dy}{du} = 2u"), ("inner", r"\frac{du}{dx} = \cos x"),
    ("mult", r"\frac{dy}{dx} = 2\sin x\cos x"), ("simp", r"2\sin x\cos x = \sin 2x")], r"y' = \sin 2x", [("sin(x)**2", "x", "sin(2*x)")])
add(2, "d", r"y = \sqrt{1 + \sin x}", [
    ("split", r"y = \sqrt{u},\qquad u = 1 + \sin x"), ("outer", r"\frac{dy}{du} = \frac{1}{2\sqrt{u}}"), ("inner", r"\frac{du}{dx} = \cos x"),
    ("mult", r"\frac{dy}{dx} = \frac{\cos x}{2\sqrt{1 + \sin x}}")], r"y' = \frac{\cos x}{2\sqrt{1 + \sin x}}", [("sqrt(1+sin(x))", "x", "cos(x)/(2*sqrt(1+sin(x)))")])
add(2, "d", r"y = \ln(\cos x),\quad \cos x > 0", [
    ("split", r"y = \ln u,\qquad u = \cos x"), ("outer", r"\frac{dy}{du} = \frac{1}{u}"), ("inner", r"\frac{du}{dx} = -\sin x"),
    ("mult", r"\frac{dy}{dx} = \frac{-\sin x}{\cos x} = -\operatorname{tg} x")], r"y' = -\operatorname{tg} x", [("log(cos(x))", "x", "-tan(x)")])
add(2, "d", r"y = e^{\sin x}", [
    ("split", r"y = e^u,\qquad u = \sin x"), ("outer", r"\frac{dy}{du} = e^u"), ("inner", r"\frac{du}{dx} = \cos x"),
    ("mult", r"\frac{dy}{dx} = e^{\sin x}\cos x")], r"y' = \cos x\,e^{\sin x}", [("exp(sin(x))", "x", "cos(x)*exp(sin(x))")])
add(2, "d", r"y = (x^3 - 2x)^4", [
    ("split", r"y = u^4,\qquad u = x^3 - 2x"), ("outer", r"\frac{dy}{du} = 4u^3"), ("inner", r"\frac{du}{dx} = 3x^2 - 2"),
    ("mult", r"\frac{dy}{dx} = 4(x^3 - 2x)^3(3x^2 - 2)")], r"y' = 4(x^3 - 2x)^3(3x^2 - 2)", [("(x**3-2*x)**4", "x", "4*(x**3-2*x)**3*(3*x**2-2)")])
add(2, "d", r"y = \operatorname{arctg} 2x", [
    ("split", r"y = \operatorname{arctg} u,\qquad u = 2x"), ("outer", r"\frac{dy}{du} = \frac{1}{1 + u^2}"), ("inner", r"\frac{du}{dx} = 2"),
    ("mult", r"\frac{dy}{dx} = \frac{2}{1 + 4x^2}")], r"y' = \frac{2}{1 + 4x^2}", [("atan(2*x)", "x", "2/(1+4*x**2)")])
add(2, "d", r"y = \ln(\ln x),\quad x > 1", [
    ("split", r"y = \ln u,\qquad u = \ln x"), ("outer", r"\frac{dy}{du} = \frac{1}{u}"), ("inner", r"\frac{du}{dx} = \frac{1}{x}"),
    ("mult", r"\frac{dy}{dx} = \frac{1}{\ln x}\cdot\frac{1}{x} = \frac{1}{x\ln x}")], r"y' = \frac{1}{x\ln x}", [("log(log(x))", "x", "1/(x*log(x))")])
add(2, "d", r"y = \sigma(x) = \frac{1}{1 + e^{-x}}", [
    ("split", r"y = u^{-1},\qquad u = 1 + e^{-x}"), ("outer", r"\frac{dy}{du} = -u^{-2}"), ("inner", r"\frac{du}{dx} = -e^{-x}\qquad \big((e^{-x})' = e^{-x}\cdot(-1)\big)"),
    ("mult", r"\frac{dy}{dx} = -\frac{1}{(1 + e^{-x})^2}\cdot(-e^{-x}) = \frac{e^{-x}}{(1 + e^{-x})^2}"),
    ("simp", r"\frac{e^{-x}}{(1 + e^{-x})^2} = \frac{1}{1 + e^{-x}}\cdot\frac{e^{-x}}{1 + e^{-x}} = \sigma(x)\big(1 - \sigma(x)\big)")],
    r"\sigma'(x) = \sigma(x)\big(1 - \sigma(x)\big)", [("1/(1+exp(-x))", "x", "exp(-x)/(1+exp(-x))**2")])
add(2, "d", r"y = \cos^3 2x", [
    ("chain3", r"y = u^3,\quad u = \cos v,\quad v = 2x"), ("each", r"\frac{dy}{du} = 3u^2,\quad \frac{du}{dv} = -\sin v,\quad \frac{dv}{dx} = 2"),
    ("mult3", r"\frac{dy}{dx} = 3\cos^2 2x\cdot(-\sin 2x)\cdot 2 = -6\cos^2 2x\,\sin 2x")], r"y' = -6\cos^2 2x\,\sin 2x", [("cos(2*x)**3", "x", "-6*cos(2*x)**2*sin(2*x)")])
add(2, "d", r"y = \sqrt{x^2 + 9}", [
    ("split", r"y = \sqrt{u},\qquad u = x^2 + 9"), ("outer", r"\frac{dy}{du} = \frac{1}{2\sqrt{u}}"), ("inner", r"\frac{du}{dx} = 2x"),
    ("mult", r"\frac{dy}{dx} = \frac{2x}{2\sqrt{x^2 + 9}} = \frac{x}{\sqrt{x^2 + 9}}")], r"y' = \frac{x}{\sqrt{x^2 + 9}}", [("sqrt(x**2+9)", "x", "x/sqrt(x**2+9)")])

# ===== level 3: three links, products with chains =====
add(3, "d", r"y = \sin^2 3x", [
    ("chain3", r"y = u^2,\quad u = \sin v,\quad v = 3x"), ("each", r"\frac{dy}{du} = 2u,\quad \frac{du}{dv} = \cos v,\quad \frac{dv}{dx} = 3"),
    ("mult3", r"\frac{dy}{dx} = 2\sin 3x\cdot\cos 3x\cdot 3 = 6\sin 3x\cos 3x"), ("simp", r"6\sin 3x\cos 3x = 3\sin 6x")], r"y' = 3\sin 6x", [("sin(3*x)**2", "x", "3*sin(6*x)")])
add(3, "d", r"y = e^{\sqrt{x}}", [
    ("split", r"y = e^u,\qquad u = \sqrt{x}"), ("outer", r"\frac{dy}{du} = e^u"), ("inner", r"\frac{du}{dx} = \frac{1}{2\sqrt{x}}"),
    ("mult", r"\frac{dy}{dx} = \frac{e^{\sqrt{x}}}{2\sqrt{x}}")], r"y' = \frac{e^{\sqrt{x}}}{2\sqrt{x}}", [("exp(sqrt(x))", "x", "exp(sqrt(x))/(2*sqrt(x))")])
add(3, "d", r"y = \sqrt{1 + e^{2x}}", [
    ("chain3", r"y = \sqrt{u},\quad u = 1 + e^{v},\quad v = 2x"), ("each", r"\frac{dy}{du} = \frac{1}{2\sqrt{u}},\quad \frac{du}{dv} = e^{v},\quad \frac{dv}{dx} = 2"),
    ("mult3", r"\frac{dy}{dx} = \frac{1}{2\sqrt{1 + e^{2x}}}\cdot e^{2x}\cdot 2 = \frac{e^{2x}}{\sqrt{1 + e^{2x}}}")], r"y' = \frac{e^{2x}}{\sqrt{1 + e^{2x}}}", [("sqrt(1+exp(2*x))", "x", "exp(2*x)/sqrt(1+exp(2*x))")])
add(3, "d", r"y = \ln\sin(x^2),\quad \sin(x^2) > 0", [
    ("chain3", r"y = \ln u,\quad u = \sin v,\quad v = x^2"), ("each", r"\frac{dy}{du} = \frac{1}{u},\quad \frac{du}{dv} = \cos v,\quad \frac{dv}{dx} = 2x"),
    ("mult3", r"\frac{dy}{dx} = \frac{\cos(x^2)}{\sin(x^2)}\cdot 2x = 2x\operatorname{ctg}(x^2)")], r"y' = 2x\operatorname{ctg}(x^2)", [("log(sin(x**2))", "x", "2*x*cos(x**2)/sin(x**2)")])
add(3, "d", r"y = x^2 e^{3x}", [
    ("prod", r"y = \underbrace{x^2}_{u}\cdot\underbrace{e^{3x}}_{v},\qquad u' = 2x,\quad v' = 3e^{3x}"),
    ("prodsum", r"y' = 2x\,e^{3x} + x^2\cdot 3e^{3x} = x e^{3x}(2 + 3x)")], r"y' = x e^{3x}(3x + 2)", [("x**2*exp(3*x)", "x", "x*exp(3*x)*(3*x+2)")])
add(3, "d", r"y = x\sqrt{1 - x^2},\quad |x| < 1", [
    ("prod", r"\begin{gathered}u = x,\quad u' = 1;\\ v = \sqrt{1 - x^2},\quad v' = \frac{1}{2\sqrt{1 - x^2}}\cdot(-2x) = -\frac{x}{\sqrt{1 - x^2}}\end{gathered}"),
    ("prodsum", r"y' = 1\cdot\sqrt{1 - x^2} + x\cdot\Big(-\frac{x}{\sqrt{1 - x^2}}\Big) = \frac{1 - 2x^2}{\sqrt{1 - x^2}}")], r"y' = \frac{1 - 2x^2}{\sqrt{1 - x^2}}", [("x*sqrt(1-x**2)", "x", "(1-2*x**2)/sqrt(1-x**2)")])
add(3, "d", r"y = e^{\cos^2 x}", [
    ("chain3", r"y = e^u,\quad u = v^2,\quad v = \cos x"), ("each", r"\frac{dy}{du} = e^u,\quad \frac{du}{dv} = 2v,\quad \frac{dv}{dx} = -\sin x"),
    ("mult3", r"\frac{dy}{dx} = e^{\cos^2 x}\cdot 2\cos x\cdot(-\sin x) = -\sin 2x\;e^{\cos^2 x}")], r"y' = -\sin 2x\;e^{\cos^2 x}", [("exp(cos(x)**2)", "x", "-sin(2*x)*exp(cos(x)**2)")])
add(3, "d", r"y = \ln\!\big(x + \sqrt{x^2 + 1}\big)", [
    ("split", r"y = \ln u,\qquad u = x + \sqrt{x^2 + 1}"), ("outer", r"\frac{dy}{du} = \frac{1}{u}"),
    ("inner", r"\frac{du}{dx} = 1 + \frac{2x}{2\sqrt{x^2 + 1}} = \frac{\sqrt{x^2 + 1} + x}{\sqrt{x^2 + 1}}"),
    ("mult", r"\frac{dy}{dx} = \frac{1}{x + \sqrt{x^2 + 1}}\cdot\frac{x + \sqrt{x^2 + 1}}{\sqrt{x^2 + 1}} = \frac{1}{\sqrt{x^2 + 1}}")], r"y' = \frac{1}{\sqrt{x^2 + 1}}", [("log(x+sqrt(x**2+1))", "x", "1/sqrt(x**2+1)")])

# ===== by the definition (the limit of the difference quotient) =====
add(3, "def", r"f(x) = (2x + 1)^2", [
    ("def", r"f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h} = \lim_{h \to 0} \frac{(2x + 2h + 1)^2 - (2x + 1)^2}{h}"),
    ("defsub", r"\begin{aligned}(2x + 1 + 2h)^2 - (2x + 1)^2 &= 2(2x + 1)\cdot 2h + 4h^2\\ &= 4h(2x + 1) + 4h^2\end{aligned}"),
    ("defcut", r"\frac{4h(2x + 1) + 4h^2}{h} = 4(2x + 1) + 4h"), ("deflim", r"f'(x) = \lim_{h \to 0}\big(4(2x + 1) + 4h\big) = 4(2x + 1)"),
    ("check", r"u = 2x + 1:\quad \big(u^2\big)' = 2u\cdot u' = 2(2x + 1)\cdot 2 = 4(2x + 1)")], r"f'(x) = 8x + 4",
    [("(2*x+1)**2", "x", "8*x+4"), ("dq", "(2*x+1)**2", "4*(2*x+1)+4*h")])
add(3, "def", r"f(x) = (x^2 + 1)^2", [
    ("def", r"f'(x) = \lim_{h \to 0} \frac{\big((x + h)^2 + 1\big)^2 - (x^2 + 1)^2}{h}"),
    ("defsub", r"\begin{gathered}A = x^2 + 1,\qquad \Delta = (x + h)^2 + 1 - A = 2xh + h^2;\\ (A + \Delta)^2 - A^2 = 2A\Delta + \Delta^2\end{gathered}"),
    ("defcut", r"\frac{2A\Delta + \Delta^2}{h} = (2A + \Delta)\cdot\frac{\Delta}{h} = (2A + \Delta)(2x + h)"),
    ("deflim", r"h \to 0:\ \Delta \to 0,\ 2x + h \to 2x;\qquad f'(x) = 2A\cdot 2x = 4x(x^2 + 1)"),
    ("check", r"u = x^2 + 1:\quad \big(u^2\big)' = 2u\cdot u' = 2(x^2 + 1)\cdot 2x = 4x(x^2 + 1)")], r"f'(x) = 4x(x^2 + 1)",
    [("(x**2+1)**2", "x", "4*x*(x**2+1)"), ("dq", "(x**2+1)**2", "(2*(x**2+1)+2*x*h+h**2)*(2*x+h)")])
add(3, "def", r"f(x) = \sqrt{3x + 1},\quad x > -\tfrac13", [
    ("def", r"f'(x) = \lim_{h \to 0} \frac{\sqrt{3x + 3h + 1} - \sqrt{3x + 1}}{h}"),
    ("conj", r"\begin{aligned}&\frac{\sqrt{3x + 3h + 1} - \sqrt{3x + 1}}{h}\cdot\frac{\sqrt{3x + 3h + 1} + \sqrt{3x + 1}}{\sqrt{3x + 3h + 1} + \sqrt{3x + 1}}\\ &\qquad= \frac{3h}{h\big(\sqrt{3x + 3h + 1} + \sqrt{3x + 1}\big)}\end{aligned}"),
    ("defcut", r"= \frac{3}{\sqrt{3x + 3h + 1} + \sqrt{3x + 1}}"), ("deflim", r"f'(x) = \lim_{h \to 0}\frac{3}{\sqrt{3x + 3h + 1} + \sqrt{3x + 1}} = \frac{3}{2\sqrt{3x + 1}}"),
    ("check", r"\big(\sqrt{u}\big)' = \frac{u'}{2\sqrt{u}} = \frac{3}{2\sqrt{3x + 1}}")], r"f'(x) = \frac{3}{2\sqrt{3x + 1}}",
    [("sqrt(3*x+1)", "x", "3/(2*sqrt(3*x+1))"), ("dq", "sqrt(3*x+1)", "3/(sqrt(3*x+3*h+1)+sqrt(3*x+1))")])
add(3, "def", r"f(x) = \frac{1}{2x + 3},\quad x \ne -\tfrac32", [
    ("def", r"f'(x) = \lim_{h \to 0} \frac{1}{h}\left(\frac{1}{2x + 2h + 3} - \frac{1}{2x + 3}\right)"),
    ("common", r"\begin{aligned}\frac{1}{2x + 2h + 3} - \frac{1}{2x + 3} &= \frac{(2x + 3) - (2x + 2h + 3)}{(2x + 2h + 3)(2x + 3)}\\ &= \frac{-2h}{(2x + 2h + 3)(2x + 3)}\end{aligned}"),
    ("defcut", r"\frac{1}{h}\cdot\frac{-2h}{(2x + 2h + 3)(2x + 3)} = \frac{-2}{(2x + 2h + 3)(2x + 3)}"), ("deflim", r"f'(x) = \lim_{h \to 0}\frac{-2}{(2x + 2h + 3)(2x + 3)} = -\frac{2}{(2x + 3)^2}"),
    ("check", r"\big(u^{-1}\big)' = -u^{-2}\cdot u' = -\frac{2}{(2x + 3)^2}")], r"f'(x) = -\frac{2}{(2x + 3)^2}",
    [("1/(2*x+3)", "x", "-2/(2*x+3)**2"), ("dq", "1/(2*x+3)", "-2/((2*x+2*h+3)*(2*x+3))")])
add(3, "def", r"f(x) = e^{3x}", [
    ("def", r"f'(x) = \lim_{h \to 0} \frac{e^{3x + 3h} - e^{3x}}{h} = e^{3x}\lim_{h \to 0}\frac{e^{3h} - 1}{h}"),
    ("known", r"\lim_{t \to 0}\frac{e^{t} - 1}{t} = 1 \quad\Rightarrow\quad \frac{e^{3h} - 1}{h} = 3\cdot\frac{e^{3h} - 1}{3h} \to 3"),
    ("limval", r"f'(x) = e^{3x}\cdot\lim_{h \to 0}\frac{e^{3h} - 1}{h} = 3e^{3x}"), ("check", r"\big(e^u\big)' = e^u\cdot u' = e^{3x}\cdot 3")], r"f'(x) = 3e^{3x}",
    [("exp(3*x)", "x", "3*exp(3*x)"), ("lim", "(exp(3*h)-1)/h", "3")])
add(3, "def", r"f(x) = \sin 2x", [
    ("def", r"f'(x) = \lim_{h \to 0} \frac{\sin(2x + 2h) - \sin 2x}{h}"),
    ("defsub", r"\sin(2x + 2h) - \sin 2x = 2\cos(2x + h)\,\sin h"),
    ("known", r"\frac{2\cos(2x + h)\sin h}{h} = 2\cos(2x + h)\cdot\frac{\sin h}{h},\qquad \lim_{h \to 0}\frac{\sin h}{h} = 1"),
    ("limval", r"f'(x) = \lim_{h \to 0} 2\cos(2x + h)\cdot\lim_{h \to 0}\frac{\sin h}{h} = 2\cos 2x\cdot 1 = 2\cos 2x"), ("check", r"\big(\sin u\big)' = \cos u\cdot u' = 2\cos 2x")], r"f'(x) = 2\cos 2x",
    [("sin(2*x)", "x", "2*cos(2*x)"), ("dq", "sin(2*x)", "2*cos(2*x+h)*sin(h)/h")])

# ===== level 4: partial derivatives =====
add(4, "pd", r"z = \sin(xy)", [
    ("pdx", r"\frac{\partial z}{\partial x} = \cos(xy)\cdot\frac{\partial(xy)}{\partial x} = y\cos(xy)"),
    ("pdy", r"\frac{\partial z}{\partial y} = \cos(xy)\cdot x = x\cos(xy)")], r"z_x = y\cos(xy),\quad z_y = x\cos(xy)",
    [("sin(x*y)", "x", "y*cos(x*y)"), ("sin(x*y)", "y", "x*cos(x*y)")])
add(4, "pd", r"z = e^{x^2 y}", [
    ("pdx", r"\frac{\partial z}{\partial x} = e^{x^2 y}\cdot 2xy"), ("pdy", r"\frac{\partial z}{\partial y} = e^{x^2 y}\cdot x^2")],
    r"z_x = 2xy\,e^{x^2 y},\quad z_y = x^2 e^{x^2 y}", [("exp(x**2*y)", "x", "2*x*y*exp(x**2*y)"), ("exp(x**2*y)", "y", "x**2*exp(x**2*y)")])
add(4, "pd", r"z = \ln(x^2 + y^2)", [
    ("pdx", r"\frac{\partial z}{\partial x} = \frac{1}{x^2 + y^2}\cdot 2x"), ("pdy", r"\frac{\partial z}{\partial y} = \frac{1}{x^2 + y^2}\cdot 2y")],
    r"z_x = \frac{2x}{x^2 + y^2},\quad z_y = \frac{2y}{x^2 + y^2}", [("log(x**2+y**2)", "x", "2*x/(x**2+y**2)"), ("log(x**2+y**2)", "y", "2*y/(x**2+y**2)")])
add(4, "pd", r"z = (x + 2y)^3", [
    ("pdx", r"\frac{\partial z}{\partial x} = 3(x + 2y)^2\cdot 1"), ("pdy", r"\frac{\partial z}{\partial y} = 3(x + 2y)^2\cdot 2 = 6(x + 2y)^2")],
    r"z_x = 3(x + 2y)^2,\quad z_y = 6(x + 2y)^2", [("(x+2*y)**3", "x", "3*(x+2*y)**2"), ("(x+2*y)**3", "y", "6*(x+2*y)**2")])
add(4, "pd", r"z = \sqrt{x^2 + y^2}", [
    ("pdx", r"\frac{\partial z}{\partial x} = \frac{1}{2\sqrt{x^2 + y^2}}\cdot 2x = \frac{x}{\sqrt{x^2 + y^2}}"), ("pdy", r"\frac{\partial z}{\partial y} = \frac{y}{\sqrt{x^2 + y^2}}")],
    r"z_x = \frac{x}{\sqrt{x^2 + y^2}},\quad z_y = \frac{y}{\sqrt{x^2 + y^2}}", [("sqrt(x**2+y**2)", "x", "x/sqrt(x**2+y**2)"), ("sqrt(x**2+y**2)", "y", "y/sqrt(x**2+y**2)")])
add(4, "pd", r"z = x\,e^{xy}", [
    ("pdxprod", r"\frac{\partial z}{\partial x} = 1\cdot e^{xy} + x\cdot e^{xy}\cdot y = e^{xy}(1 + xy)"), ("pdy", r"\frac{\partial z}{\partial y} = x\cdot e^{xy}\cdot x = x^2 e^{xy}")],
    r"z_x = e^{xy}(1 + xy),\quad z_y = x^2 e^{xy}", [("x*exp(x*y)", "x", "exp(x*y)*(1+x*y)"), ("x*exp(x*y)", "y", "x**2*exp(x*y)")])
add(4, "pd", r"w = e^{xyz}", [
    ("pdx", r"\frac{\partial w}{\partial x} = yz\,e^{xyz}"), ("pdy", r"\frac{\partial w}{\partial y} = xz\,e^{xyz}"), ("pdz", r"\frac{\partial w}{\partial z} = xy\,e^{xyz}")],
    r"\nabla w = e^{xyz}\,(yz;\ xz;\ xy)", [("exp(x*y*z)", "x", "y*z*exp(x*y*z)"), ("exp(x*y*z)", "y", "x*z*exp(x*y*z)"), ("exp(x*y*z)", "z", "x*y*exp(x*y*z)")])
add(4, "pdef", r"f(x, y) = x^2 y", [
    ("pdef", r"f_x = \lim_{h \to 0}\frac{(x + h)^2 y - x^2 y}{h} = \lim_{h \to 0}\frac{(2xh + h^2)\,y}{h} = \lim_{h \to 0}(2x + h)\,y = 2xy"),
    ("pdefy", r"f_y = \lim_{h \to 0}\frac{x^2(y + h) - x^2 y}{h} = \lim_{h \to 0}\frac{x^2 h}{h} = x^2")], r"f_x = 2xy,\quad f_y = x^2",
    [("x**2*y", "x", "2*x*y"), ("x**2*y", "y", "x**2")])
add(4, "pdef", r"f(x, y) = (x + y)^2", [
    ("pdef", r"\begin{aligned}f_x &= \lim_{h \to 0}\frac{\big((x + h) + y\big)^2 - (x + y)^2}{h} = \lim_{h \to 0}\frac{2(x + y)h + h^2}{h}\\ &= \lim_{h \to 0}\big(2(x + y) + h\big) = 2(x + y)\end{aligned}"),
    ("pdefy", r"\begin{aligned}f_y &= \lim_{h \to 0}\frac{\big(x + (y + h)\big)^2 - (x + y)^2}{h} = \lim_{h \to 0}\frac{2(x + y)h + h^2}{h}\\ &= \lim_{h \to 0}\big(2(x + y) + h\big) = 2(x + y)\end{aligned}")], r"f_x = f_y = 2(x + y)",
    [("(x+y)**2", "x", "2*(x+y)"), ("(x+y)**2", "y", "2*(x+y)")])

# ===== level 5: the multivariable chain rule =====
add(5, "dt", r"z = x^2 y,\quad x = \cos t,\quad y = \sin t", [
    ("tree", r"z \to (x,\ y),\qquad x \to t,\quad y \to t"), ("pouter", r"\frac{\partial z}{\partial x} = 2xy,\qquad \frac{\partial z}{\partial y} = x^2"),
    ("pinner", r"\frac{dx}{dt} = -\sin t,\qquad \frac{dy}{dt} = \cos t"),
    ("sum", r"\frac{dz}{dt} = \frac{\partial z}{\partial x}\frac{dx}{dt} + \frac{\partial z}{\partial y}\frac{dy}{dt} = 2xy(-\sin t) + x^2\cos t"),
    ("subs", r"= -2\cos t\sin^2 t + \cos^3 t"), ("verify", r"z = \cos^2 t\,\sin t;\quad z' = -2\cos t\sin t\cdot\sin t + \cos^2 t\cos t")],
    r"\frac{dz}{dt} = \cos^3 t - 2\cos t\sin^2 t", [("zt", "cos(t)**2*sin(t)", "cos(t)**3-2*cos(t)*sin(t)**2")])
add(5, "dt", r"z = e^{x}\,y,\quad x = t^2,\quad y = 3t", [
    ("pouter", r"\frac{\partial z}{\partial x} = e^{x}y,\qquad \frac{\partial z}{\partial y} = e^{x}"), ("pinner", r"\frac{dx}{dt} = 2t,\qquad \frac{dy}{dt} = 3"),
    ("sum", r"\frac{dz}{dt} = e^{x}y\cdot 2t + e^{x}\cdot 3"), ("subs", r"= e^{t^2}\cdot 3t\cdot 2t + 3e^{t^2} = 3e^{t^2}(2t^2 + 1)")],
    r"\frac{dz}{dt} = 3e^{t^2}(2t^2 + 1)", [("zt", "exp(t**2)*3*t", "3*exp(t**2)*(2*t**2+1)")])
add(5, "dt", r"z = \ln(x + y),\quad x = t^2,\quad y = e^{t}", [
    ("pouter", r"\frac{\partial z}{\partial x} = \frac{\partial z}{\partial y} = \frac{1}{x + y}"), ("pinner", r"\frac{dx}{dt} = 2t,\qquad \frac{dy}{dt} = e^{t}"),
    ("sum", r"\frac{dz}{dt} = \frac{2t}{x + y} + \frac{e^{t}}{x + y} = \frac{2t + e^{t}}{t^2 + e^{t}}")],
    r"\frac{dz}{dt} = \frac{2t + e^{t}}{t^2 + e^{t}}", [("zt", "log(t**2+exp(t))", "(2*t+exp(t))/(t**2+exp(t))")])
add(5, "dt", r"z = \sqrt{x^2 + y^2},\quad x = 3t,\quad y = 4t,\ t > 0", [
    ("pouter", r"\frac{\partial z}{\partial x} = \frac{x}{\sqrt{x^2 + y^2}},\qquad \frac{\partial z}{\partial y} = \frac{y}{\sqrt{x^2 + y^2}}"),
    ("pinner", r"\frac{dx}{dt} = 3,\qquad \frac{dy}{dt} = 4"), ("sum", r"\frac{dz}{dt} = \frac{3x + 4y}{\sqrt{x^2 + y^2}} = \frac{9t + 16t}{5t} = 5")],
    r"\frac{dz}{dt} = 5", [("zt", "sqrt(25*t**2)", "5")])
add(5, "dst", r"z = u^2 + v^2,\quad u = s + t,\quad v = s - t", [
    ("tree", r"z \to (u,\ v),\qquad u \to (s,\ t),\quad v \to (s,\ t)"), ("pouter", r"\frac{\partial z}{\partial u} = 2u,\qquad \frac{\partial z}{\partial v} = 2v"),
    ("pinner", r"\frac{\partial u}{\partial s} = 1,\ \frac{\partial u}{\partial t} = 1;\qquad \frac{\partial v}{\partial s} = 1,\ \frac{\partial v}{\partial t} = -1"),
    ("sum", r"\frac{\partial z}{\partial s} = 2u\cdot 1 + 2v\cdot 1 = 4s,\qquad \frac{\partial z}{\partial t} = 2u\cdot 1 + 2v\cdot(-1) = 4t")],
    r"z_s = 4s,\quad z_t = 4t", [("zst", "(s+t)**2+(s-t)**2", "4*s", "4*t")])
add(5, "dst", r"z = e^{u}\sin v,\quad u = st,\quad v = s + t", [
    ("pouter", r"\frac{\partial z}{\partial u} = e^{u}\sin v,\qquad \frac{\partial z}{\partial v} = e^{u}\cos v"),
    ("pinner", r"u_s = t,\ u_t = s;\qquad v_s = 1,\ v_t = 1"),
    ("sum", r"\begin{gathered}z_s = e^{u}\sin v\cdot t + e^{u}\cos v\cdot 1 = e^{st}\big(t\sin(s + t) + \cos(s + t)\big)\\ z_t = e^{u}\sin v\cdot s + e^{u}\cos v\cdot 1 = e^{st}\big(s\sin(s + t) + \cos(s + t)\big)\end{gathered}")],
    r"\begin{gathered}z_s = e^{st}\big(t\sin(s + t) + \cos(s + t)\big)\\ z_t = e^{st}\big(s\sin(s + t) + \cos(s + t)\big)\end{gathered}", [("zst", "exp(s*t)*sin(s+t)", "exp(s*t)*(t*sin(s+t)+cos(s+t))", "exp(s*t)*(s*sin(s+t)+cos(s+t))")])
add(5, "dst", r"z = \ln(u^2 + v^2),\quad u = s\cos t,\quad v = s\sin t,\quad s > 0", [
    ("pouter", r"\frac{\partial z}{\partial u} = \frac{2u}{u^2 + v^2},\qquad \frac{\partial z}{\partial v} = \frac{2v}{u^2 + v^2},\qquad u^2 + v^2 = s^2"),
    ("pinner", r"u_s = \cos t,\ u_t = -s\sin t;\qquad v_s = \sin t,\ v_t = s\cos t"),
    ("sum", r"\begin{gathered}z_s = \frac{2u}{s^2}\cos t + \frac{2v}{s^2}\sin t = \frac{2s\cos^2 t + 2s\sin^2 t}{s^2} = \frac{2}{s}\\ z_t = \frac{2u}{s^2}(-s\sin t) + \frac{2v}{s^2}\,s\cos t = \frac{-2s^2\cos t\sin t + 2s^2\sin t\cos t}{s^2} = 0\end{gathered}")],
    r"z_s = \frac{2}{s},\quad z_t = 0", [("zst", "log(s**2)", "2/s", "0")])
add(5, "dLt", r"L = (wx + b - y)^2;\quad w = 1 + t,\quad b = 2t,\quad x = 3,\ y = 5", [
    ("pouter", r"\frac{\partial L}{\partial w} = 2(wx + b - y)\,x,\qquad \frac{\partial L}{\partial b} = 2(wx + b - y)"),
    ("pinner", r"\frac{dw}{dt} = 1,\qquad \frac{db}{dt} = 2"),
    ("sum", r"\frac{dL}{dt} = 2(wx + b - y)(x + 2) = 2(3 + 3t + 2t - 5)\cdot 5 = 10(5t - 2)")],
    r"\frac{dL}{dt} = 10(5t - 2)", [("zt", "(3*(1+t)+2*t-5)**2", "10*(5*t-2)")])

# ===== level 5: total derivatives, implicit functions, a neural network =====
add(5, "total", r"z = x^2 + y^2,\quad y = \sin x", [
    ("total", r"\frac{dz}{dx} = \frac{\partial z}{\partial x} + \frac{\partial z}{\partial y}\cdot\frac{dy}{dx} = 2x + 2y\cos x"),
    ("subs", r"= 2x + 2\sin x\cos x = 2x + \sin 2x")], r"\frac{dz}{dx} = 2x + \sin 2x", [("x**2+sin(x)**2", "x", "2*x+sin(2*x)")])
add(5, "total", r"z = x\,e^{y},\quad y = x^2", [
    ("total", r"\frac{dz}{dx} = \underbrace{e^{y}}_{\partial z/\partial x} + \underbrace{x e^{y}}_{\partial z/\partial y}\cdot 2x"),
    ("subs", r"= e^{x^2}(1 + 2x^2)")], r"\frac{dz}{dx} = e^{x^2}(1 + 2x^2)", [("x*exp(x**2)", "x", "exp(x**2)*(1+2*x**2)")])
add(5, "impl", r"x^2 + y^2 = 25", [
    ("impl", r"2x + 2y\,y' = 0"), ("solve", r"y' = -\frac{x}{y}"), ("point", r"(3;\ 4):\quad y' = -\frac34")], r"y' = -\frac{x}{y}\quad (y \ne 0)",
    [("impl", "x**2+y**2-25", "-x/y")])
add(5, "impl", r"e^{y} + xy = e", [
    ("impl", r"e^{y}y' + y + x\,y' = 0"), ("solve", r"y' = -\frac{y}{e^{y} + x}"), ("point", r"(0;\ 1):\quad y' = -\frac{1}{e}")],
    r"y' = -\frac{y}{e^{y} + x}\quad (e^{y} + x \ne 0)", [("impl", "exp(y)+x*y-E", "-y/(exp(y)+x)")])
add(5, "nn", r"\hat y = \sigma(wx + b),\quad L = -\ln\hat y\ \ (y = 1)", [
    ("layers", r"L = -\ln a,\quad a = \sigma(z) = \hat y,\quad z = wx + b"),
    ("each", r"\frac{dL}{da} = -\frac{1}{a},\quad \frac{da}{dz} = a(1 - a),\quad \frac{\partial z}{\partial w} = x,\quad \frac{\partial z}{\partial b} = 1"),
    ("mult3only", r"\frac{\partial L}{\partial w} = -\frac{1}{a}\cdot a(1 - a)\cdot x = (a - 1)\,x = (\hat y - 1)\,x,\qquad \frac{\partial L}{\partial b} = \hat y - 1")],
    r"\frac{\partial L}{\partial w} = (\hat y - 1)\,x,\quad \frac{\partial L}{\partial b} = \hat y - 1",
    [("nnw", "-log(1/(1+exp(-(w*x+b))))", "(1/(1+exp(-(w*x+b)))-1)*x", "1/(1+exp(-(w*x+b)))-1")])

NOTES = {}   # n → {lang: note} for extra explanations


def verify():
    import sympy as sp
    x, y, z, t, s, h, w, b = sp.symbols("x y z t s h w b", real=True)
    V = dict(x=x, y=y, z=z, t=t, s=s, h=h, w=w, b=b, E=sp.E)
    P = lambda e: sp.sympify(e, locals=V)
    zero = lambda e: sp.simplify(sp.expand_trig(sp.simplify(e))) == 0 or abs(complex(e.subs({x: 0.37, y: 0.61, z: 0.53, t: 0.42, s: 1.3, h: 0.0, w: 0.7, b: -0.2}).evalf())) < 1e-9
    assert len(D) >= 50, len(D)
    for d in D:
        for c in d["checks"]:
            kind = c[0]
            if kind == "dq":       # the simplified difference quotient equals (f(x+h) − f(x))/h
                f = P(c[1]); q = (f.subs(x, x + h) - f) / h - P(c[2])
                assert all(abs(complex(q.subs({x: xv, h: hv}).evalf())) < 1e-9 for xv in (0.3, 1.1) for hv in (0.01, 0.2)), (d["n"], c)
            elif kind == "lim":
                assert sp.limit(P(c[1]), h, 0) == P(c[2]), (d["n"], c)
            elif kind == "zt":     # z(t) after substitution, claimed dz/dt
                assert zero(sp.diff(P(c[1]), t) - P(c[2])), (d["n"], c)
            elif kind == "zst":
                g = P(c[1]); assert zero(sp.diff(g, s) - P(c[2])) and zero(sp.diff(g, t) - P(c[3])), (d["n"], c)
            elif kind == "impl":
                F = P(c[1]); assert zero(-sp.diff(F, x) / sp.diff(F, y) - P(c[2])), (d["n"], c)
            elif kind == "nnw":
                g = P(c[1]); assert zero(sp.diff(g, w) - P(c[2])) and zero(sp.diff(g, b) - P(c[3])), (d["n"], c)
            else:
                f, var, claim = c
                assert zero(sp.diff(P(f), V[var]) - P(claim)), (d["n"], c)
    return True


# group headings: the number of the first drill of the group → the heading
GROUPS = {
    1: {"ru": "Одно звено: основные функции", "en": "One link: the basic functions", "uz": "Bitta bo‘g‘in: asosiy funksiyalar"},
    11: {"ru": "Функция в степени, под логарифмом, под корнем", "en": "A function raised to a power, under a logarithm, under a root", "uz": "Darajadagi, logarifm va ildiz ostidagi funksiya"},
    21: {"ru": "Три звена, произведения и вложенные цепочки", "en": "Three links, products and nested chains", "uz": "Uchta bo‘g‘in, ko‘paytmalar va ichma-ich zanjirlar"},
    29: {"ru": "По определению: предел разностного отношения", "en": "From the definition: the limit of the difference quotient", "uz": "Ta’rif bo‘yicha: ayirmali nisbatning limiti"},
    35: {"ru": "Частные производные", "en": "Partial derivatives", "uz": "Xususiy hosilalar"},
    44: {"ru": "Многомерное цепное правило", "en": "The multivariable chain rule", "uz": "Ko‘p o‘lchovli zanjir qoidasi"},
    52: {"ru": "Полная производная, неявная функция, нейрон", "en": "The total derivative, implicit functions, a neuron", "uz": "To‘liq hosila, oshkormas funksiya, neyron"},
}

EN_TEX = [(r"\operatorname{arctg}", r"\arctan"), (r"\operatorname{tg}", r"\tan"), (r"\operatorname{ctg}", r"\cot"), (r";\ ", r",\ ")]


def localize(t, lang):
    """English writes tan, cot, arctan and separates coordinates with a comma."""
    if lang == "en":
        for a, b in EN_TEX:
            t = t.replace(a, b)
    return t


def drill_blocks(lang):
    """The drills as article blocks in one language, with a heading before every group."""
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
