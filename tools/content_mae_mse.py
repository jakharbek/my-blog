"""Материал «MAE и MSE на простых примерах»: 20 задач с подробным разбором (ru / en / uz).

Тексты — здесь; HTML строит tools/build.py (material_mae_mse). Все числа разборов считаются
точными дробями (fractions.Fraction) из условий задач — в тексте нет ни одного числа «на глаз».
Калькулятор на странице (assets/js/practice.js) повторяет те же правила округления.

Правило записи результата деления на n: если частное — конечная десятичная дробь (до 6 знаков),
пишем его точно («= 0,8»); иначе — «≈» и 2 знака после запятой (4 знака, если |x| < 0,1).
"""

from __future__ import annotations

from fractions import Fraction

SLUG = "mae-mse-examples"
DATE = "2026-11-01"
LANGS = ("ru", "en", "uz")

# ----------------------------------------------------------------------------------------------
# Числа
# ----------------------------------------------------------------------------------------------


def F(s: str) -> Fraction:
    return Fraction(str(s).replace(",", "."))


def exact_decimal(x: Fraction, max_digits: int = 6) -> str | None:
    """Точная десятичная запись или None, если дробь бесконечная (или длиннее max_digits знаков)."""
    for d in range(max_digits + 1):
        v = x * 10**d
        if v.denominator == 1:
            s = str(abs(v.numerator)).rjust(d + 1, "0")
            body = s[:-d] + "." + s[-d:] if d else s
            return ("-" if x < 0 else "") + body
    return None


def rounded(x: Fraction) -> str:
    """Округление для «≈»: 2 знака, а если |x| < 0,1 — 4 знака (половина — от нуля)."""
    digits = 2 if abs(x) >= Fraction(1, 10) else 4
    q = Fraction(10) ** digits
    v = abs(x) * q
    n = v.numerator // v.denominator
    if (v - n) * 2 >= 1:
        n += 1
    s = str(n).rjust(digits + 1, "0")
    return ("-" if x < 0 else "") + s[:-digits] + "." + s[-digits:]


def fmt(x: Fraction | str, lang: str, mode: str = "tex") -> str:
    """Число для текста: в ru/uz — десятичная запятая; минус — «−»; в TeX — {,}."""
    s = x if isinstance(x, str) else (exact_decimal(x) or rounded(x))
    if lang != "en":
        s = s.replace(".", "{,}" if mode == "tex" else ",")
    if s.startswith("-"):
        s = ("-" if mode == "tex" else "−") + s[1:]
    return s


def value(x: Fraction, lang: str, mode: str = "tex") -> tuple[str, str]:
    """(знак «=» или «≈», число) для результата деления."""
    ex = exact_decimal(x)
    if ex is not None:
        return "=", fmt(ex, lang, mode)
    return (r"\approx" if mode == "tex" else "≈"), fmt(rounded(x), lang, mode)


def solve(y: list[str], yhat: list[str]) -> dict:
    """Точный разбор: ошибки, модули, квадраты, суммы и средние."""
    ys, ps = [F(v) for v in y], [F(v) for v in yhat]
    assert len(ys) == len(ps) > 0
    e = [a - b for a, b in zip(ys, ps)]
    ab = [abs(v) for v in e]
    sq = [v * v for v in e]
    n = len(ys)
    return dict(y=ys, p=ps, e=e, abs=ab, sq=sq, n=n, sum_abs=sum(ab, Fraction(0)), sum_sq=sum(sq, Fraction(0)),
                mae=sum(ab, Fraction(0)) / n, mse=sum(sq, Fraction(0)) / n, bias=sum(e, Fraction(0)) / n)


# ----------------------------------------------------------------------------------------------
# Тексты страницы
# ----------------------------------------------------------------------------------------------

PAGE = {
    "ru": dict(
        kicker="Практикум · ML / AI",
        title="MAE и MSE на простых примерах",
        dek="20 задач с подробным разбором — от примера с доски до выбросов и выбора модели. Каждый шаг расписан так же, как на уроке: пары $y_i$ и $\\hat y_i$, ошибки, модули и квадраты, сумма, деление на $n$. Числа простые: всё считается в уме или на бумаге.",
        description="MAE и MSE на 20 простых примерах: пошаговые разборы, сравнение метрик, выбросы, медиана и среднее, калькулятор и тест.",
        excerpt="20 простых задач на MAE и MSE с подробным разбором каждого шага — от примера с доски до выбросов и выбора модели. Плюс калькулятор, который расписывает решение для ваших чисел.",
        count="примеров", min="мин", expand="Раскрыть все разборы", collapse="Свернуть",
        example="Пример", solution="Разбор и ответ", try_first="Попробуйте сначала решить сами — потом откройте разбор.",
        task="Найдите MAE и MSE.", answer="Ответ", idea="Что видно из примера", model="Модель",
        step1="Ошибка каждого объекта $e_i = y_i - \\hat y_i$ и её модуль:",
        step2="Сумма модулей:", step3="MAE — делим сумму на $n = {n}$:",
        step4="Квадрат каждой ошибки:", step5="Сумма квадратов:", step6="MSE — делим сумму на $n = {n}$:",
        table_h=["$i$", "$y_i$", "$\\hat y_i$", "$e_i$", "$|e_i|$", "$e_i^2$"],
        sum="Сумма", mean="Среднее",
        compare="Сравнение", stars="сложность {k} из 3",
    ),
    "en": dict(
        kicker="Practice · ML / AI",
        title="MAE and MSE by example",
        dek="20 problems solved step by step, from the example on the board to outliers and choosing a model. Every step is written out as in class: the pairs $y_i$ and $\\hat y_i$, the errors, their absolute values and squares, the sum, the division by $n$. The numbers are simple enough for mental arithmetic or pen and paper.",
        description="MAE and MSE on 20 simple examples: step-by-step solutions, comparing the metrics, outliers, median versus mean, a calculator and a quiz.",
        excerpt="20 simple MAE and MSE problems with every step explained, from the example on the board to outliers and model choice. Plus a calculator that writes out the solution for your own numbers.",
        count="examples", min="min", expand="Expand all solutions", collapse="Collapse",
        example="Example", solution="Solution and answer", try_first="Try to solve it yourself first, then open the solution.",
        task="Find MAE and MSE.", answer="Answer", idea="What the example shows", model="Model",
        step1="The error of each object $e_i = y_i - \\hat y_i$ and its absolute value:",
        step2="Sum of the absolute values:", step3="MAE: divide the sum by $n = {n}$:",
        step4="The square of each error:", step5="Sum of the squares:", step6="MSE: divide the sum by $n = {n}$:",
        table_h=["$i$", "$y_i$", "$\\hat y_i$", "$e_i$", "$|e_i|$", "$e_i^2$"],
        sum="Sum", mean="Mean",
        compare="Comparison", stars="difficulty {k} of 3",
    ),
    "uz": dict(
        kicker="Amaliyot · ML / AI",
        title="MAE va MSE oddiy misollarda",
        dek="Batafsil yechilgan 20 ta masala — doskadagi misoldan chetga chiquvchi qiymatlar va model tanlashgacha. Har bir qadam darsdagidek yozilgan: $y_i$ va $\\hat y_i$ juftlari, xatolar, ularning modullari va kvadratlari, yig‘indi, $n$ ga bo‘lish. Sonlar oddiy: hammasi og‘zaki yoki qog‘ozda hisoblanadi.",
        description="MAE va MSE 20 ta oddiy misolda: qadamma-qadam yechimlar, metrikalarni solishtirish, chetga chiquvchi qiymatlar, mediana va o‘rtacha, kalkulyator va test.",
        excerpt="MAE va MSE bo‘yicha 20 ta oddiy masala, har bir qadami batafsil tushuntirilgan — doskadagi misoldan chetga chiquvchi qiymatlar va model tanlashgacha. Yana o‘z sonlaringiz uchun yechimni yozib beradigan kalkulyator.",
        count="ta misol", min="daq", expand="Barcha yechimlarni ochish", collapse="Yopish",
        example="Misol", solution="Yechim va javob", try_first="Avval o‘zingiz yechib ko‘ring, keyin yechimni oching.",
        task="MAE va MSE ni toping.", answer="Javob", idea="Misol nimani ko‘rsatadi", model="Model",
        step1="Har bir obyektning xatosi $e_i = y_i - \\hat y_i$ va uning moduli:",
        step2="Modullar yig‘indisi:", step3="MAE — yig‘indini $n = {n}$ ga bo‘lamiz:",
        step4="Har bir xatoning kvadrati:", step5="Kvadratlar yig‘indisi:", step6="MSE — yig‘indini $n = {n}$ ga bo‘lamiz:",
        table_h=["$i$", "$y_i$", "$\\hat y_i$", "$e_i$", "$|e_i|$", "$e_i^2$"],
        sum="Yig‘indi", mean="O‘rtacha",
        compare="Solishtirish", stars="qiyinlik {k} / 3",
    ),
}

# ----------------------------------------------------------------------------------------------
# 20 примеров. preds: [(подпись модели или None, ŷ)]; open — разбор раскрыт сразу.
# ----------------------------------------------------------------------------------------------


def T(ru: str, en: str, uz: str) -> dict:
    return {"ru": ru, "en": en, "uz": uz}


EXAMPLES = [
    # --- часть 1: пример с доски
    dict(part="board", stars=1, open=True, y=["3", "5", "8"], preds=[(None, ["2.5", "5", "10"])],
         title=T("Пример с доски", "The example from the board", "Doskadagi misol"),
         idea=T("Две из трёх ошибок небольшие, а одна равна 2. MAE ≈ 0,83 — «в среднем ошибаемся меньше чем на единицу». "
                "MSE ≈ 1,42 больше MAE: квадрат ошибки 2 равен 4 и перетягивает среднее на себя.",
                "Two of the three errors are small and one equals 2. MAE ≈ 0.83: «on average we are off by less than one». "
                "MSE ≈ 1.42 is larger than MAE: the square of the error 2 is 4, and it pulls the average up.",
                "Uchta xatodan ikkitasi kichik, bittasi 2 ga teng. MAE ≈ 0,83 — «o‘rtacha birdan kamroqqa adashamiz». "
                "MSE ≈ 1,42 MAE dan katta: 2 xatoning kvadrati 4 ga teng va o‘rtachani o‘ziga tortadi.")),
    # --- часть 2: разминка
    dict(part="warmup", stars=1, open=True, y=["2", "4", "6"], preds=[(None, ["2", "4", "6"])],
         title=T("Идеальный прогноз", "A perfect prediction", "Mukammal bashorat"),
         idea=T("Все ошибки равны нулю, значит MAE = 0 и MSE = 0. Меньше нуля обе метрики не бывают: модуль и квадрат не отрицательны.",
                "All errors are zero, so MAE = 0 and MSE = 0. Neither metric can go below zero: absolute values and squares are never negative.",
                "Barcha xatolar nolga teng, demak MAE = 0 va MSE = 0. Ikkala metrika ham noldan kichik bo‘lmaydi: modul va kvadrat manfiy emas.")),
    dict(part="warmup", stars=1, y=["1", "2", "3", "4"], preds=[(None, ["1", "2", "3", "6"])],
         title=T("Ошибка только в одной точке", "An error at a single point", "Faqat bitta nuqtadagi xato"),
         idea=T("Ошибка 2 одна на четыре объекта: MAE = 2 / 4 = 0,5. А в MSE она входит как 2² = 4, поэтому MSE = 1 — вдвое больше MAE.",
                "There is one error of 2 among four objects: MAE = 2 / 4 = 0.5. In MSE it enters as 2² = 4, so MSE = 1, twice the MAE.",
                "To‘rtta obyektda bitta 2 xato: MAE = 2 / 4 = 0,5. MSE ga esa u 2² = 4 bo‘lib kiradi, shuning uchun MSE = 1 — MAE dan ikki baravar katta.")),
    dict(part="warmup", stars=1, y=["5", "7", "9"], preds=[(None, ["6", "8", "10"])],
         title=T("Одинаковая ошибка везде", "The same error everywhere", "Hamma joyda bir xil xato"),
         idea=T("Модель везде завышает на 1. Если все |eᵢ| одинаковы и равны a, то MAE = a, а MSE = a². Здесь a = 1, поэтому обе метрики равны 1.",
                "The model overshoots by 1 everywhere. If all |eᵢ| equal the same a, then MAE = a and MSE = a². Here a = 1, so both metrics equal 1.",
                "Model hamma joyda 1 ga oshirib yuboradi. Agar barcha |eᵢ| bir xil va a ga teng bo‘lsa, MAE = a, MSE = a². Bu yerda a = 1, shuning uchun ikkala metrika ham 1 ga teng.")),
    dict(part="warmup", stars=1, y=["10", "20"], preds=[(None, ["12", "18"])],
         title=T("Знак ошибки не важен", "The sign of the error does not matter", "Xatoning ishorasi muhim emas"),
         idea=T("Первая ошибка −2 (модель завысила), вторая +2 (занизила). Модуль и квадрат убирают знак: обе ошибки дают 2 в MAE и 4 в MSE. Промахи вверх и вниз не гасят друг друга.",
                "The first error is −2 (the model overshot), the second +2 (it undershot). The absolute value and the square remove the sign: both errors give 2 in MAE and 4 in MSE. Misses up and down do not cancel out.",
                "Birinchi xato −2 (model oshirib yubordi), ikkinchisi +2 (kam ko‘rsatdi). Modul va kvadrat ishorani olib tashlaydi: ikkala xato ham MAE da 2, MSE da 4 beradi. Yuqoriga va pastga adashishlar bir-birini yo‘qqa chiqarmaydi.")),
    dict(part="warmup", stars=1, y=["1", "1"], preds=[(None, ["1.5", "0.5"])],
         title=T("Ошибки меньше единицы", "Errors smaller than one", "Birdan kichik xatolar"),
         idea=T("Здесь MSE = 0,25 меньше MAE = 0,5: квадрат числа меньше 1 становится ещё меньше (0,5² = 0,25). Поэтому сравнивать MAE и MSE по величине бессмысленно — у них разные единицы и разный характер.",
                "Here MSE = 0.25 is smaller than MAE = 0.5: squaring a number below 1 makes it smaller still (0.5² = 0.25). That is why comparing MAE and MSE by size makes no sense: they have different units and behave differently.",
                "Bu yerda MSE = 0,25 MAE = 0,5 dan kichik: 1 dan kichik sonning kvadrati yanada kichrayadi (0,5² = 0,25). Shuning uchun MAE va MSE ni kattaligi bo‘yicha solishtirish ma’nosiz — ularning birliklari va tabiati har xil.")),
    dict(part="warmup", stars=1, y=["2", "4", "6", "8", "10"], preds=[(None, ["3", "3", "7", "7", "10"])],
         title=T("Пять объектов — делим на 5", "Five objects: divide by 5", "Beshta obyekt — 5 ga bo‘lamiz"),
         idea=T("Делим всегда на число объектов n, а не на число ненулевых ошибок: ошибок четыре, но объектов пять, поэтому MAE = 4 / 5 = 0,8.",
                "Always divide by the number of objects n, not by the number of nonzero errors: there are four errors but five objects, so MAE = 4 / 5 = 0.8.",
                "Har doim obyektlar soni n ga bo‘lamiz, noldan farqli xatolar soniga emas: xato to‘rtta, obyekt esa beshta, shuning uchun MAE = 4 / 5 = 0,8.")),
    # --- часть 3: отрицательные, дроби, n = 1
    dict(part="numbers", stars=2, y=["-2", "0", "3"], preds=[(None, ["1", "-1", "3"])],
         title=T("Отрицательные числа: температура", "Negative numbers: temperature", "Manfiy sonlar: harorat"),
         idea=T("Главное — аккуратно вычитать: 0 − (−1) = 0 + 1 = 1, а (−3)² = 9, не −9. Модуль и квадрат всегда дают неотрицательный результат.",
                "The key is careful subtraction: 0 − (−1) = 0 + 1 = 1, and (−3)² = 9, not −9. Absolute values and squares are never negative.",
                "Asosiysi — ehtiyotkorlik bilan ayirish: 0 − (−1) = 0 + 1 = 1, (−3)² esa 9 ga teng, −9 ga emas. Modul va kvadrat hech qachon manfiy bo‘lmaydi.")),
    dict(part="numbers", stars=2, y=["1.2", "2.5", "3.1"], preds=[(None, ["1", "2.9", "3.1"])],
         title=T("Десятичные дроби", "Decimals", "O‘nli kasrlar"),
         idea=T("С дробями всё то же самое, только аккуратнее с квадратами: 0,2² = 0,04 и 0,4² = 0,16. MSE ≈ 0,0667 намного меньше MAE = 0,2 — все ошибки меньше 1.",
                "Decimals work the same way, just be careful with squares: 0.2² = 0.04 and 0.4² = 0.16. MSE ≈ 0.0667 is much smaller than MAE = 0.2 because all errors are below 1.",
                "Kasrlar bilan ham xuddi shunday, faqat kvadratlarda ehtiyot bo‘ling: 0,2² = 0,04 va 0,4² = 0,16. MSE ≈ 0,0667 MAE = 0,2 dan ancha kichik — barcha xatolar 1 dan kichik.")),
    dict(part="numbers", stars=1, y=["7"], preds=[(None, ["4"])],
         title=T("Один объект, n = 1", "One object, n = 1", "Bitta obyekt, n = 1"),
         idea=T("При n = 1 делить не на что: MAE — это просто модуль ошибки (3), а MSE — её квадрат (9).",
                "With n = 1 there is nothing to average: MAE is just the absolute error (3) and MSE is its square (9).",
                "n = 1 da o‘rtacha olishga hojat yo‘q: MAE — xatoning moduli (3), MSE — uning kvadrati (9).")),
    # --- часть 4: чем отличаются
    dict(part="diff", stars=2, y=["3", "5", "7", "9"], preds=[("A", ["4", "6", "6", "8"]), ("B", ["3", "5", "7", "5"])],
         title=T("Одинаковая MAE — разная MSE", "Same MAE, different MSE", "Bir xil MAE — har xil MSE"),
         idea=T("У обеих моделей MAE = 1. Но A ошибается понемногу везде, а B точна в трёх точках и сильно промахивается в одной. MSE это различает: 1 у A против 4 у B. MSE «наказывает» крупные промахи.",
                "Both models have MAE = 1. But A is slightly off everywhere, while B is exact at three points and misses one badly. MSE tells them apart: 1 for A versus 4 for B. MSE «punishes» large misses.",
                "Ikkala modelda ham MAE = 1. Lekin A hamma joyda ozgina adashadi, B esa uchta nuqtada aniq va bittasida qattiq adashadi. MSE buni farqlaydi: A da 1, B da 4. MSE katta adashishlarni «jazolaydi».")),
    dict(part="diff", stars=2, y=["2", "3", "4", "20"], preds=[(None, ["3", "3", "3", "4"])],
         title=T("Выброс", "An outlier", "Chetga chiquvchi qiymat"),
         idea=T("Одна точка (y = 20) ушла далеко. В MAE её ошибка 16 даёт 16 из 18 в сумме, а в MSE — 256 из 258: почти вся метрика из одной точки. MSE очень чувствительна к выбросам, MAE — заметно спокойнее.",
                "One point (y = 20) is far away. In MAE its error of 16 is 16 out of the sum of 18; in MSE it is 256 out of 258, almost the whole metric from a single point. MSE is very sensitive to outliers; MAE is much calmer.",
                "Bitta nuqta (y = 20) uzoqqa ketgan. MAE da uning 16 xatosi 18 lik yig‘indining 16 tasini beradi, MSE da esa 258 ning 256 tasini — deyarli butun metrika bitta nuqtadan. MSE chetga chiquvchi qiymatlarga juda sezgir, MAE ancha xotirjam.")),
    dict(part="diff", stars=2, y=["1", "2", "3"], preds=[("A", ["2", "3", "4"]), ("B", ["3", "4", "5"])],
         title=T("Ошибки вдвое больше", "Errors twice as large", "Ikki baravar katta xatolar"),
         idea=T("Модель B ошибается вдвое сильнее A (на 2 вместо 1). MAE тоже растёт вдвое (1 → 2), а MSE — вчетверо (1 → 4): квадрат удвоенного числа в 4 раза больше.",
                "Model B errs twice as much as A (by 2 instead of 1). MAE doubles as well (1 → 2), while MSE quadruples (1 → 4): the square of a doubled number is four times larger.",
                "B modeli A dan ikki baravar ko‘p adashadi (1 o‘rniga 2 ga). MAE ham ikki baravar oshadi (1 → 2), MSE esa to‘rt baravar (1 → 4): ikki baravar oshgan sonning kvadrati 4 baravar katta.")),
    dict(part="diff", stars=3, y=["2", "4", "9"], preds=[("A", ["5", "5", "5"]), ("B", ["4", "4", "4"])],
         title=T("Одно число на всех: среднее или медиана?", "One number for everyone: mean or median?", "Hammaga bitta son: o‘rtacha yoki mediana?"),
         idea=T("Модель A всегда отвечает средним (2 + 4 + 9) / 3 = 5, модель B — медианой 4. По MAE лучше медиана (≈ 2,33 против ≈ 2,67), по MSE — среднее (≈ 8,67 против ≈ 9,67). Это общее правило: из всех констант MAE минимизирует медиана, а MSE — среднее.",
                "Model A always answers with the mean (2 + 4 + 9) / 3 = 5, model B with the median 4. By MAE the median wins (≈ 2.33 versus ≈ 2.67), by MSE the mean wins (≈ 8.67 versus ≈ 9.67). This is a general rule: among all constants, the median minimizes MAE and the mean minimizes MSE.",
                "A modeli har doim o‘rtacha (2 + 4 + 9) / 3 = 5 bilan, B modeli esa mediana 4 bilan javob beradi. MAE bo‘yicha mediana yaxshiroq (mediana — ≈ 2,33, o‘rtacha — ≈ 2,67), MSE bo‘yicha — o‘rtacha (o‘rtacha — ≈ 8,67, mediana — ≈ 9,67). Bu umumiy qoida: barcha o‘zgarmaslar orasida MAE ni mediana, MSE ni esa o‘rtacha minimallashtiradi.")),
    dict(part="diff", stars=2, y=["10", "10", "10", "10"], preds=[(None, ["15", "5", "15", "5"])],
         title=T("Средняя ошибка со знаком обманывает", "The signed mean error is misleading", "Ishorali o‘rtacha xato aldaydi"),
         idea=T("Ошибки −5, +5, −5, +5 в сумме дают 0 — «в среднем модель не ошибается»? Нет: каждый прогноз мимо на 5. Поэтому в метриках берут модуль или квадрат: MAE = 5, MSE = 25.",
                "The errors −5, +5, −5, +5 add up to 0. «On average the model is right»? No: every prediction is off by 5. That is why metrics take the absolute value or the square: MAE = 5, MSE = 25.",
                "−5, +5, −5, +5 xatolar yig‘indisi 0 — «o‘rtacha model adashmaydi»mi? Yo‘q: har bir bashorat 5 ga xato. Shuning uchun metrikalarda modul yoki kvadrat olinadi: MAE = 5, MSE = 25.")),
    # --- часть 5: как в жизни
    dict(part="life", stars=2, y=["100", "150", "200"], preds=[(None, ["110", "140", "230"])],
         title=T("Цены в тысячах: единицы измерения", "Prices in thousands: units", "Mingliklardagi narxlar: o‘lchov birliklari"),
         idea=T("Цены в тысячах долларов. MAE ≈ 16,67 — тоже в тысячах: «в среднем ошибаемся на 16,7 тыс.». MSE ≈ 366,67 измеряется в «тысячах в квадрате» — такую величину трудно объяснить заказчику. Поэтому рядом часто считают RMSE = √MSE ≈ 19,15 тыс.",
                "The prices are in thousands of dollars. MAE ≈ 16.67 is in thousands too: «on average we are off by 16.7 thousand». MSE ≈ 366.67 is measured in «thousands squared», which is hard to explain to a client. That is why RMSE = √MSE ≈ 19.15 thousand is often reported next to it.",
                "Narxlar ming dollarda. MAE ≈ 16,67 ham mingda: «o‘rtacha 16,7 mingga adashamiz». MSE ≈ 366,67 esa «mingning kvadrati»da o‘lchanadi — buni buyurtmachiga tushuntirish qiyin. Shuning uchun yonida ko‘pincha RMSE = √MSE ≈ 19,15 ming hisoblanadi.")),
    dict(part="life", stars=2, y=["5", "4", "3", "5", "4", "2"], preds=[(None, ["4", "4", "4", "4", "4", "4"])],
         title=T("Оценки шести учеников", "The grades of six students", "Olti o‘quvchining baholari"),
         idea=T("Модель всем ставит «4». Ошибается на 1 у троих и на 2 у одного: MAE = 5 / 6 ≈ 0,83 балла. В MSE ошибка 2 даёт 4 из 7, поэтому MSE ≈ 1,17 заметно больше MAE.",
                "The model gives everyone a 4. It is off by 1 for three students and by 2 for one: MAE = 5 / 6 ≈ 0.83 points. In MSE the error of 2 contributes 4 out of 7, so MSE ≈ 1.17 is noticeably larger than MAE.",
                "Model hammaga «4» qo‘yadi. Uchtasida 1 ga, bittasida 2 ga adashadi: MAE = 5 / 6 ≈ 0,83 ball. MSE da 2 xato 7 dan 4 ni beradi, shuning uchun MSE ≈ 1,17 MAE dan sezilarli katta.")),
    dict(part="life", stars=2, y=["30", "45", "60"], preds=[(None, ["35", "45", "50"])],
         title=T("Время доставки в минутах", "Delivery time in minutes", "Yetkazib berish vaqti daqiqalarda"),
         idea=T("MAE = 5 минут — понятный ответ для клиента: «в среднем курьер опаздывает или приезжает раньше на 5 минут». MSE ≈ 41,67 «минут в квадрате» удобна для обучения модели, но не для объяснения.",
                "MAE = 5 minutes is a clear answer for a customer: «on average the courier is 5 minutes early or late». MSE ≈ 41.67 «minutes squared» is convenient for training a model but not for explaining it.",
                "MAE = 5 daqiqa — mijoz uchun tushunarli javob: «o‘rtacha kuryer 5 daqiqa kechikadi yoki erta keladi». MSE ≈ 41,67 «daqiqa kvadrati» modelni o‘qitish uchun qulay, lekin tushuntirish uchun emas.")),
    dict(part="life", stars=3, kind="reverse", y=["4", "6"], preds=[(None, ["5", "?"])],
         title=T("Задача наоборот: найдите прогноз", "The reverse problem: find the prediction", "Teskari masala: bashoratni toping"),
         idea=T("Задачу «наоборот» решают тем же рецептом: записать формулу, подставить известное и найти неизвестное. Модуль даёт два ответа — прогноз мог ошибиться вверх или вниз.",
                "A reverse problem is solved with the same recipe: write the formula, plug in what is known and find the unknown. The absolute value gives two answers: the prediction could have missed up or down.",
                "Teskari masala ham xuddi shu retsept bilan yechiladi: formulani yozish, ma’lumni qo‘yish va noma’lumni topish. Modul ikkita javob beradi — bashorat yuqoriga ham, pastga ham adashishi mumkin edi.")),
    dict(part="life", stars=3, y=["10", "20", "30"], preds=[("A", ["12", "18", "33"]), ("B", ["10", "20", "36"])],
         title=T("Какая модель лучше?", "Which model is better?", "Qaysi model yaxshiroq?"),
         idea=T("По MAE лучше B (2 против ≈ 2,33): она точна в двух точках из трёх. По MSE лучше A (≈ 5,67 против 12): у неё нет крупного промаха. Ответ зависит от задачи: если редкие большие ошибки опасны (например, прогноз нагрузки на мост), выбирайте по MSE; если важна типичная ошибка — по MAE.",
                "By MAE, B is better (2 versus ≈ 2.33): it is exact at two points out of three. By MSE, A is better (≈ 5.67 versus 12): it has no large miss. The answer depends on the task: if rare large errors are dangerous (say, forecasting the load on a bridge), choose by MSE; if the typical error matters, choose by MAE.",
                "MAE bo‘yicha B yaxshiroq (B — 2, A — ≈ 2,33): u uchta nuqtadan ikkitasida aniq. MSE bo‘yicha A yaxshiroq (A — ≈ 5,67, B — 12): unda katta adashish yo‘q. Javob masalaga bog‘liq: kamdan-kam katta xatolar xavfli bo‘lsa (masalan, ko‘prikka tushadigan yukni bashorat qilish), MSE bo‘yicha tanlang; odatiy xato muhim bo‘lsa — MAE bo‘yicha.")),
]

assert len(EXAMPLES) == 20

# Задача наоборот (№ 19): y = (4; 6), ŷ₁ = 5, MAE = 1. Найти ŷ₂.
REVERSE = dict(y=["4", "6"], p1="5", mae="1")


def reverse_answers() -> list[Fraction]:
    y1, y2, p1, m = F(REVERSE["y"][0]), F(REVERSE["y"][1]), F(REVERSE["p1"]), F(REVERSE["mae"])
    rest = m * 2 - abs(y1 - p1)  # |y₂ − ŷ₂| = 2·MAE − |y₁ − ŷ₁|
    assert rest >= 0
    return sorted({y2 - rest, y2 + rest})


REVERSE_TEXT = {
    "ru": dict(task="Известно: $y = (4;\\ 6)$, первый прогноз $\\hat y_1 = 5$, а $\\mathrm{MAE} = 1$. Найдите второй прогноз $\\hat y_2$ и MSE.",
               s1="Запишем MAE для $n = 2$ и подставим известное:",
               s2="Умножаем обе части на 2 и переносим известный модуль:",
               s3="Модуль равен 1, значит выражение под ним равно $1$ или $-1$:",
               s4="Проверим MSE для обоих ответов — она одна и та же:",
               ans="$\\hat y_2 = 5$ или $\\hat y_2 = 7$; MSE = 1."),
    "en": dict(task="Given: $y = (4,\\ 6)$, the first prediction $\\hat y_1 = 5$ and $\\mathrm{MAE} = 1$. Find the second prediction $\\hat y_2$ and the MSE.",
               s1="Write MAE for $n = 2$ and plug in what is known:",
               s2="Multiply both sides by 2 and move the known absolute value:",
               s3="The absolute value equals 1, so the expression inside is $1$ or $-1$:",
               s4="Check the MSE for both answers: it is the same:",
               ans="$\\hat y_2 = 5$ or $\\hat y_2 = 7$; MSE = 1."),
    "uz": dict(task="Ma’lum: $y = (4;\\ 6)$, birinchi bashorat $\\hat y_1 = 5$, $\\mathrm{MAE} = 1$. Ikkinchi bashorat $\\hat y_2$ va MSE ni toping.",
               s1="$n = 2$ uchun MAE ni yozamiz va ma’lumlarni qo‘yamiz:",
               s2="Ikkala tomonni 2 ga ko‘paytiramiz va ma’lum modulni o‘tkazamiz:",
               s3="Modul 1 ga teng, demak uning ichidagi ifoda $1$ yoki $-1$:",
               s4="Ikkala javob uchun MSE ni tekshiramiz — u bir xil:",
               ans="$\\hat y_2 = 5$ yoki $\\hat y_2 = 7$; MSE = 1."),
}

PARTS = [
    ("board", T("Пример с доски", "The example from the board", "Doskadagi misol"),
     T("Начнём с примера, разобранного на уроке: три объекта, три прогноза. Каждый шаг ниже — ровно то, что написано на доске, только подробнее.",
       "Let us start with the example solved in class: three objects and three predictions. Each step below is exactly what was written on the board, only in more detail.",
       "Darsda yechilgan misoldan boshlaymiz: uchta obyekt va uchta bashorat. Quyidagi har bir qadam — doskada yozilganining aynan o‘zi, faqat batafsilroq.")),
    ("warmup", T("Разминка", "Warm-up", "Qizish"),
     T("Простые наборы чисел, чтобы рецепт стал привычным. Первая задача раскрыта, остальные попробуйте решить сами.",
       "Simple sets of numbers to make the recipe a habit. The first problem is open; try the rest yourself.",
       "Retsept odatga aylanishi uchun oddiy sonlar to‘plamlari. Birinchi masala ochiq, qolganlarini o‘zingiz yechib ko‘ring.")),
    ("numbers", T("Отрицательные числа, дроби и один объект", "Negative numbers, decimals and a single object", "Manfiy sonlar, kasrlar va bitta obyekt"),
     T("Тот же рецепт, но числа хитрее: минусы, запятые и случай, когда объект всего один.",
       "The same recipe with trickier numbers: minus signs, decimals and the case of a single object.",
       "Xuddi shu retsept, lekin sonlar murakkabroq: minuslar, kasrlar va obyekt bittagina bo‘lgan hol.")),
    ("diff", T("Чем MAE отличается от MSE", "How MAE differs from MSE", "MAE MSE dan nimasi bilan farq qiladi"),
     T("Здесь примеры подобраны так, чтобы метрики «спорили»: одинаковая MAE и разная MSE, выброс, удвоение ошибок, среднее против медианы.",
       "Here the examples are chosen so that the metrics «argue»: the same MAE with different MSE, an outlier, doubled errors, the mean versus the median.",
       "Bu yerda misollar metrikalar «bahslashadigan» qilib tanlangan: bir xil MAE va har xil MSE, chetga chiquvchi qiymat, ikki baravar xatolar, o‘rtacha va mediana.")),
    ("life", T("Как в жизни", "Real-life cases", "Hayotdagidek"),
     T("Единицы измерения, оценки, время доставки, задача «наоборот» и главный практический вопрос — какую модель выбрать.",
       "Units of measurement, grades, delivery times, a reverse problem and the main practical question: which model to choose.",
       "O‘lchov birliklari, baholar, yetkazib berish vaqti, «teskari» masala va asosiy amaliy savol — qaysi modelni tanlash.")),
]

# Вводный раздел, ошибки, итоги, тест — блоки в формате tools/formulas/README.md
INTRO = {
    "ru": [
        ("p", "Обе метрики отвечают на вопрос «насколько модель ошибается?». Есть $n$ объектов; для каждого известен правильный ответ $y_i$ и прогноз модели $\\hat y_i$ (читается «игрек с крышкой»). Разница $e_i = y_i - \\hat y_i$ — ошибка на объекте $i$."),
        ("symbols", [("y_i", "правильный ответ (истина) для объекта $i$"), ("\\hat y_i", "прогноз модели для объекта $i$"),
                     ("e_i = y_i - \\hat y_i", "ошибка: плюс — модель занизила, минус — завысила"),
                     ("n", "число объектов"), ("\\sum_{i=1}^{n}", "сумма по всем объектам от $1$ до $n$")]),
        ("h3", "Рецепт из четырёх шагов"),
        ("ol", ["Выпишите пары $(y_i,\\ \\hat y_i)$ и посчитайте ошибки $e_i = y_i - \\hat y_i$.",
                "Для MAE возьмите модуль каждой ошибки $|e_i|$, для MSE — квадрат $e_i^2$.",
                "Сложите все модули (или все квадраты).",
                "Разделите сумму на $n$ — это и есть MAE (или MSE)."]),
        ("callout", "key", "Как читать ответ", "MAE — средний размер промаха в тех же единицах, что и $y$: «в среднем ошибаемся на 0,83». MSE — средний квадрат промаха, в единицах «в квадрате»; она сильнее реагирует на большие ошибки. Обе метрики: чем меньше, тем лучше, ноль — идеал."),
    ],
    "en": [
        ("p", "Both metrics answer the question «how wrong is the model?». There are $n$ objects; for each we know the correct answer $y_i$ and the model's prediction $\\hat y_i$ (read «y hat»). The difference $e_i = y_i - \\hat y_i$ is the error on object $i$."),
        ("symbols", [("y_i", "the correct answer (ground truth) for object $i$"), ("\\hat y_i", "the model's prediction for object $i$"),
                     ("e_i = y_i - \\hat y_i", "the error: plus means the model undershot, minus means it overshot"),
                     ("n", "the number of objects"), ("\\sum_{i=1}^{n}", "the sum over all objects from $1$ to $n$")]),
        ("h3", "A four-step recipe"),
        ("ol", ["Write out the pairs $(y_i,\\ \\hat y_i)$ and compute the errors $e_i = y_i - \\hat y_i$.",
                "For MAE take the absolute value of each error $|e_i|$; for MSE take the square $e_i^2$.",
                "Add up all the absolute values (or all the squares).",
                "Divide the sum by $n$: that is the MAE (or the MSE)."]),
        ("callout", "key", "How to read the answer", "MAE is the average size of a miss in the same units as $y$: «on average we are off by 0.83». MSE is the average squared miss, in «squared» units; it reacts more strongly to large errors. For both metrics, smaller is better and zero is perfect."),
    ],
    "uz": [
        ("p", "Ikkala metrika ham «model qanchalik adashadi?» degan savolga javob beradi. $n$ ta obyekt bor; har biri uchun to‘g‘ri javob $y_i$ va model bashorati $\\hat y_i$ («igrek qalpoqcha» deb o‘qiladi) ma’lum. $e_i = y_i - \\hat y_i$ ayirma — $i$-obyektdagi xato."),
        ("symbols", [("y_i", "$i$-obyekt uchun to‘g‘ri javob (haqiqat)"), ("\\hat y_i", "$i$-obyekt uchun model bashorati"),
                     ("e_i = y_i - \\hat y_i", "xato: plyus — model kam ko‘rsatdi, minus — oshirib yubordi"),
                     ("n", "obyektlar soni"), ("\\sum_{i=1}^{n}", "$1$ dan $n$ gacha barcha obyektlar bo‘yicha yig‘indi")]),
        ("h3", "To‘rt qadamli retsept"),
        ("ol", ["$(y_i,\\ \\hat y_i)$ juftlarini yozing va $e_i = y_i - \\hat y_i$ xatolarni hisoblang.",
                "MAE uchun har bir xatoning modulini $|e_i|$, MSE uchun kvadratini $e_i^2$ oling.",
                "Barcha modullarni (yoki barcha kvadratlarni) qo‘shing.",
                "Yig‘indini $n$ ga bo‘ling — bu MAE (yoki MSE)."]),
        ("callout", "key", "Javobni qanday o‘qish kerak", "MAE — $y$ bilan bir xil birlikdagi o‘rtacha adashish kattaligi: «o‘rtacha 0,83 ga adashamiz». MSE — adashishning o‘rtacha kvadrati, «kvadrat» birliklarda; u katta xatolarga kuchliroq ta’sir qiladi. Ikkala metrika uchun ham: qancha kichik bo‘lsa, shuncha yaxshi, nol — ideal."),
    ],
}

MISTAKES = {
    "ru": [
        ("ul", ["<b>Забыли модуль.</b> Ошибки −2 и +2 «сократились» в ноль — а модель ошибалась оба раза (примеры 5 и 15).",
                "<b>Возвели в квадрат минус неправильно.</b> $(-3)^2 = 9$, а не $-9$: квадрат любого числа не отрицателен (пример 8).",
                "<b>Разделили не на то $n$.</b> Делим на число объектов, а не на число ненулевых ошибок (пример 7).",
                "<b>Усреднили, а потом возвели в квадрат.</b> MSE — среднее квадратов, а не квадрат среднего: для ошибок −5 и +5 MSE = 25, а «квадрат средней ошибки» был бы 0.",
                "<b>Сравнили MAE с MSE «по величине».</b> У них разные единицы: при ошибках меньше 1 MSE меньше MAE, при больших — больше (примеры 6 и 3).",
                "<b>Перепутали порядок вычитания.</b> Не страшно: $|y - \\hat y| = |\\hat y - y|$ и $(y - \\hat y)^2 = (\\hat y - y)^2$. Но ошибку со знаком принято считать как $y_i - \\hat y_i$."]),
    ],
    "en": [
        ("ul", ["<b>Forgot the absolute value.</b> The errors −2 and +2 «cancel» to zero, yet the model was wrong both times (examples 5 and 15).",
                "<b>Squared a negative number incorrectly.</b> $(-3)^2 = 9$, not $-9$: the square of any number is non-negative (example 8).",
                "<b>Divided by the wrong $n$.</b> Divide by the number of objects, not by the number of nonzero errors (example 7).",
                "<b>Averaged first and squared afterwards.</b> MSE is the mean of the squares, not the square of the mean: for the errors −5 and +5, MSE = 25, while the «square of the mean error» would be 0.",
                "<b>Compared MAE and MSE «by size».</b> They have different units: with errors below 1, MSE is smaller than MAE; with large errors it is larger (examples 6 and 3).",
                "<b>Swapped the order of subtraction.</b> That is harmless: $|y - \\hat y| = |\\hat y - y|$ and $(y - \\hat y)^2 = (\\hat y - y)^2$. Still, the signed error is conventionally $y_i - \\hat y_i$."]),
    ],
    "uz": [
        ("ul", ["<b>Modulni unutish.</b> −2 va +2 xatolar nolga «qisqardi» — lekin model ikkala marta ham adashgan (5- va 15-misollar).",
                "<b>Minusni noto‘g‘ri kvadratga oshirish.</b> $(-3)^2 = 9$, $-9$ emas: istalgan sonning kvadrati manfiy emas (8-misol).",
                "<b>Noto‘g‘ri $n$ ga bo‘lish.</b> Obyektlar soniga bo‘lamiz, noldan farqli xatolar soniga emas (7-misol).",
                "<b>Avval o‘rtacha olib, keyin kvadratga oshirish.</b> MSE — kvadratlarning o‘rtachasi, o‘rtachaning kvadrati emas: −5 va +5 xatolar uchun MSE = 25, «o‘rtacha xatoning kvadrati» esa 0 bo‘lardi.",
                "<b>MAE va MSE ni «kattaligi bo‘yicha» solishtirish.</b> Ularning birliklari har xil: xatolar 1 dan kichik bo‘lsa, MSE MAE dan kichik, katta bo‘lsa — katta (6- va 3-misollar).",
                "<b>Ayirish tartibini almashtirish.</b> Qo‘rqinchli emas: $|y - \\hat y| = |\\hat y - y|$ va $(y - \\hat y)^2 = (\\hat y - y)^2$. Lekin ishorali xato odatda $y_i - \\hat y_i$ deb olinadi."]),
    ],
}

SUMMARY = {
    "ru": dict(
        heads=["", "MAE", "MSE"],
        rows=[["Формула", "$\\tfrac{1}{n}\\sum |e_i|$", "$\\tfrac{1}{n}\\sum e_i^2$"],
              ["Единицы", "те же, что у $y$", "единицы $y$ в квадрате"],
              ["Большие ошибки", "учитывает как есть", "усиливает: ошибка ×2 → вклад ×4"],
              ["Выбросы", "устойчива", "чувствительна"],
              ["Лучшая константа", "медиана", "среднее"],
              ["Когда выбирать", "важна типичная ошибка, есть выбросы", "крупные промахи особенно опасны"]],
        bullets=["Рецепт один: ошибки → модули или квадраты → сумма → деление на $n$.",
                 "Модуль и квадрат убирают знак, поэтому промахи вверх и вниз не гасят друг друга.",
                 "MSE «наказывает» большие ошибки, MAE — нет; одна и та же модель может быть лучше по одной метрике и хуже по другой.",
                 "Подробная теория — на страницах <a class=\"ul\" href=\"../ml-formulas/mae/\">MAE</a>, <a class=\"ul\" href=\"../ml-formulas/mse/\">MSE</a> и <a class=\"ul\" href=\"../ml-formulas/rmse/\">RMSE</a> шпаргалки."]),
    "en": dict(
        heads=["", "MAE", "MSE"],
        rows=[["Formula", "$\\tfrac{1}{n}\\sum |e_i|$", "$\\tfrac{1}{n}\\sum e_i^2$"],
              ["Units", "the same as $y$", "the units of $y$ squared"],
              ["Large errors", "counted proportionally", "amplified: error ×2 → contribution ×4"],
              ["Outliers", "robust", "sensitive"],
              ["Best constant", "the median", "the mean"],
              ["When to choose", "the typical error matters, there are outliers", "large misses are especially dangerous"]],
        bullets=["One recipe: errors → absolute values or squares → sum → divide by $n$.",
                 "The absolute value and the square remove the sign, so misses up and down do not cancel out.",
                 "MSE «punishes» large errors and MAE does not; the same model can be better by one metric and worse by the other.",
                 "The full theory is on the <a class=\"ul\" href=\"../ml-formulas/mae/\">MAE</a>, <a class=\"ul\" href=\"../ml-formulas/mse/\">MSE</a> and <a class=\"ul\" href=\"../ml-formulas/rmse/\">RMSE</a> pages of the cheat sheet."]),
    "uz": dict(
        heads=["", "MAE", "MSE"],
        rows=[["Formula", "$\\tfrac{1}{n}\\sum |e_i|$", "$\\tfrac{1}{n}\\sum e_i^2$"],
              ["Birliklar", "$y$ bilan bir xil", "$y$ birligining kvadrati"],
              ["Katta xatolar", "mutanosib hisobga oladi", "kuchaytiradi: xato ×2 → hissa ×4"],
              ["Chetga chiquvchilar", "bardoshli", "sezgir"],
              ["Eng yaxshi o‘zgarmas", "mediana", "o‘rtacha"],
              ["Qachon tanlash kerak", "odatiy xato muhim, chetga chiquvchilar bor", "katta adashishlar ayniqsa xavfli"]],
        bullets=["Retsept bitta: xatolar → modullar yoki kvadratlar → yig‘indi → $n$ ga bo‘lish.",
                 "Modul va kvadrat ishorani olib tashlaydi, shuning uchun yuqoriga va pastga adashishlar bir-birini yo‘qqa chiqarmaydi.",
                 "MSE katta xatolarni «jazolaydi», MAE — yo‘q; bitta model bir metrika bo‘yicha yaxshiroq, boshqasi bo‘yicha yomonroq bo‘lishi mumkin.",
                 "To‘liq nazariya — qo‘llanmaning <a class=\"ul\" href=\"../ml-formulas/mae/\">MAE</a>, <a class=\"ul\" href=\"../ml-formulas/mse/\">MSE</a> va <a class=\"ul\" href=\"../ml-formulas/rmse/\">RMSE</a> sahifalarida."]),
}

QUIZ = {
    "ru": [
        dict(q="$y = (2;\\ 4)$, $\\hat y = (3;\\ 1)$. Чему равна MAE?", options=["$2$", "$1$", "$4$", "$5$"], answer=0,
             explain="Ошибки $-1$ и $3$, модули $1$ и $3$, сумма $4$, делим на $n = 2$: MAE = 2."),
        dict(q="Для тех же чисел чему равна MSE?", options=["$4$", "$5$", "$10$", "$2$"], answer=1,
             explain="Квадраты ошибок $1$ и $9$, сумма $10$, делим на $2$: MSE = 5."),
        dict(q="Все ошибки увеличили втрое. Во сколько раз вырастет MSE?", options=["в 3 раза", "в 6 раз", "в 9 раз", "не изменится"], answer=2,
             explain="Каждый квадрат растёт в $3^2 = 9$ раз, значит и их среднее — тоже в 9 раз (MAE выросла бы втрое)."),
        dict(q="Какое одно число $c$ минимизирует MAE для данных $(1;\\ 2;\\ 10)$?", options=["$1$", "$2$", "$\\frac{13}{3}$", "$10$"], answer=1,
             explain="MAE минимизирует медиана, а медиана набора $1, 2, 10$ — это $2$. Среднее $\\frac{13}{3}$ минимизировало бы MSE."),
        dict(q="Ошибки модели: $0{,}1;\\ 0{,}2;\\ 0{,}3$. Что больше?", options=["MAE", "MSE", "они равны", "зависит от $n$"], answer=0,
             explain="Все ошибки меньше 1, их квадраты ещё меньше: MAE = 0,2, MSE ≈ 0,0467."),
    ],
    "en": [
        dict(q="$y = (2,\\ 4)$, $\\hat y = (3,\\ 1)$. What is the MAE?", options=["$2$", "$1$", "$4$", "$5$"], answer=0,
             explain="The errors are $-1$ and $3$, the absolute values $1$ and $3$, the sum $4$; divide by $n = 2$: MAE = 2."),
        dict(q="For the same numbers, what is the MSE?", options=["$4$", "$5$", "$10$", "$2$"], answer=1,
             explain="The squared errors are $1$ and $9$, the sum is $10$; divide by $2$: MSE = 5."),
        dict(q="All errors were tripled. How many times larger does the MSE get?", options=["3 times", "6 times", "9 times", "it does not change"], answer=2,
             explain="Every square grows $3^2 = 9$ times, so their mean grows 9 times as well (MAE would triple)."),
        dict(q="Which single number $c$ minimizes the MAE for the data $(1,\\ 2,\\ 10)$?", options=["$1$", "$2$", "$\\frac{13}{3}$", "$10$"], answer=1,
             explain="The median minimizes MAE, and the median of $1, 2, 10$ is $2$. The mean $\\frac{13}{3}$ would minimize the MSE."),
        dict(q="The model's errors are $0.1,\\ 0.2,\\ 0.3$. Which is larger?", options=["MAE", "MSE", "they are equal", "it depends on $n$"], answer=0,
             explain="All errors are below 1, so their squares are even smaller: MAE = 0.2, MSE ≈ 0.0467."),
    ],
    "uz": [
        dict(q="$y = (2;\\ 4)$, $\\hat y = (3;\\ 1)$. MAE nimaga teng?", options=["$2$", "$1$", "$4$", "$5$"], answer=0,
             explain="Xatolar $-1$ va $3$, modullar $1$ va $3$, yig‘indi $4$, $n = 2$ ga bo‘lamiz: MAE = 2."),
        dict(q="Xuddi shu sonlar uchun MSE nimaga teng?", options=["$4$", "$5$", "$10$", "$2$"], answer=1,
             explain="Xatolar kvadratlari $1$ va $9$, yig‘indi $10$, $2$ ga bo‘lamiz: MSE = 5."),
        dict(q="Barcha xatolar uch baravar oshirildi. MSE necha baravar oshadi?", options=["3 baravar", "6 baravar", "9 baravar", "o‘zgarmaydi"], answer=2,
             explain="Har bir kvadrat $3^2 = 9$ baravar oshadi, demak ularning o‘rtachasi ham 9 baravar oshadi (MAE uch baravar oshgan bo‘lardi)."),
        dict(q="$(1;\\ 2;\\ 10)$ ma’lumotlar uchun MAE ni qaysi bitta $c$ soni minimallashtiradi?", options=["$1$", "$2$", "$\\frac{13}{3}$", "$10$"], answer=1,
             explain="MAE ni mediana minimallashtiradi, $1, 2, 10$ to‘plamining medianasi esa $2$. O‘rtacha $\\frac{13}{3}$ MSE ni minimallashtirgan bo‘lardi."),
        dict(q="Model xatolari: $0{,}1;\\ 0{,}2;\\ 0{,}3$. Qaysi biri katta?", options=["MAE", "MSE", "ular teng", "$n$ ga bog‘liq"], answer=0,
             explain="Barcha xatolar 1 dan kichik, ularning kvadratlari yanada kichik: MAE = 0,2, MSE ≈ 0,0467."),
    ],
}

CALC = {
    "ru": dict(title="Посчитайте свой пример", lead="Введите правильные ответы $y$ и прогнозы $\\hat y$ — калькулятор распишет решение по тем же четырём шагам. Числа разделяйте точкой с запятой или пробелом; дробную часть — запятой или точкой.",
               y="Правильные ответы $y$", p="Прогнозы $\\hat y$", go="Посчитать", presets="Подставить:", board="пример с доски", outlier="выброс", decimals="дроби",
               err_count="Количество чисел в $y$ и $\\hat y$ должно совпадать: сейчас {a} и {b}.", err_num="«{t}» — не число. Разделяйте числа точкой с запятой или пробелом: 3; 5; 8.",
               err_empty="Введите хотя бы по одному числу в обе строки.", err_many="Не больше {m} чисел — иначе разбор станет слишком длинным.",
               noscript="Калькулятору нужен JavaScript; все 20 примеров выше работают и без него."),
    "en": dict(title="Compute your own example", lead="Enter the correct answers $y$ and the predictions $\\hat y$, and the calculator will write out the solution in the same four steps. Separate the numbers with commas, spaces or semicolons; use a point for decimals.",
               y="Correct answers $y$", p="Predictions $\\hat y$", go="Compute", presets="Try:", board="the board example", outlier="an outlier", decimals="decimals",
               err_count="$y$ and $\\hat y$ must have the same number of values: now {a} and {b}.", err_num="«{t}» is not a number. Separate the numbers with commas, spaces or semicolons: 3, 5, 8.",
               err_empty="Enter at least one number in both lines.", err_many="At most {m} numbers, otherwise the solution gets too long.",
               noscript="The calculator needs JavaScript; all 20 examples above work without it."),
    "uz": dict(title="O‘z misolingizni hisoblang", lead="To‘g‘ri javoblar $y$ va bashoratlar $\\hat y$ ni kiriting — kalkulyator yechimni xuddi shu to‘rt qadam bo‘yicha yozib beradi. Sonlarni nuqtali vergul yoki bo‘sh joy bilan ajrating; kasr qismini vergul yoki nuqta bilan yozing.",
               y="To‘g‘ri javoblar $y$", p="Bashoratlar $\\hat y$", go="Hisoblash", presets="Qo‘yish:", board="doskadagi misol", outlier="chetga chiquvchi", decimals="kasrlar",
               err_count="$y$ va $\\hat y$ dagi sonlar soni bir xil bo‘lishi kerak: hozir {a} va {b}.", err_num="«{t}» — son emas. Sonlarni nuqtali vergul yoki bo‘sh joy bilan ajrating: 3; 5; 8.",
               err_empty="Ikkala qatorga kamida bittadan son kiriting.", err_many="{m} tadan ko‘p emas — aks holda yechim juda uzun bo‘lib ketadi.",
               noscript="Kalkulyatorga JavaScript kerak; yuqoridagi 20 ta misol usiz ham ishlaydi."),
}

SECTION_TITLES = {
    "ru": dict(intro="Как читать формулы", calc="Посчитайте свой пример", mistakes="Частые ошибки", summary="Итоги", quiz="Проверь себя"),
    "en": dict(intro="How to read the formulas", calc="Compute your own example", mistakes="Common mistakes", summary="Summary", quiz="Check yourself"),
    "uz": dict(intro="Formulalarni qanday o‘qish kerak", calc="O‘z misolingizni hisoblang", mistakes="Tez-tez uchraydigan xatolar", summary="Xulosa", quiz="O‘zingizni tekshiring"),
}

HERO = r"\begin{gathered}\mathrm{MAE}=\frac{1}{n}\sum_{i=1}^{n}\bigl|y_i-\hat{y}_i\bigr|\\[6pt]\mathrm{MSE}=\frac{1}{n}\sum_{i=1}^{n}\bigl(y_i-\hat{y}_i\bigr)^2\end{gathered}"


def count_label(lang: str) -> str:
    return f"{len(EXAMPLES)} {PAGE[lang]['count']}"
