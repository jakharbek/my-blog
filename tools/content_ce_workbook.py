"""Материал «Перекрёстная энтропия в Excel»: разбор тетради автора (ru / en / uz).

Тетрадь — tools/workbooks/cross_entropy_practice.xlsx (файлы для скачивания собирает
tools/workbook_ce.py). Здесь — тексты страницы и все числа. Числа не пишутся руками: они
считаются из тех же входов, что в тетради (логиты, метки), и форматируются по языку.
Утверждения текста («одна строка весит больше четырёх остальных», «лосс упрётся в 0» …)
проверяются assert-ами при импорте модуля.
"""
import math
import re
from decimal import ROUND_HALF_UP, Decimal

SLUG = "cross-entropy-excel"
DATE = "2026-11-02"
LANGS = ["ru", "en", "uz"]

# ---------------------------------------------------------------- данные тетради
BCE_Y = [1, 0, 1, 0, 1]
BCE_Z = [2.2, -1.4, 0.4, -0.6, 1.4]
ZONE_X = [-1, 0, 0.01, 0.1, 0.5, 0.9, 0.99, 1, 2, 10]          # лист BCE, блок 3
SQUASH_Z = [-10, -3, -1, 0, 1, 3, 10]                          # лист BCE, блок 4
CE_Y = [0, 1, 0]
CE_Z = [1, 2, 0.5]
CE_ZONE_X = [-1, 0, 0.01, 0.1, 0.5, 0.9, 1, 2, 10, 1000]       # лист Categorical CE, блок 3
TASK1 = dict(y=[1, 0, 1], p=[0.8, 0.3, 0.5])
TASK2 = dict(y=[0, 0, 1], p=[0.1, 0.3, 0.6])
TASK3 = dict(z=[0, 1, 2], k=3)
TOL = 0.005

sig = lambda z: 1 / (1 + math.exp(-z))
ln = math.log


def bce_rows(Y, Z):
    rows = []
    for y, z in zip(Y, Z):
        p = sig(z)
        a = y * ln(p)
        b = (1 - y) * ln(1 - p)
        rows.append(dict(y=y, z=z, e=math.exp(-z), p=p, a=a, b=b, s=a + b, right=p if y else 1 - p))
    return rows


R = bce_rows(BCE_Y, BCE_Z)
V = {}
V["sum"] = sum(r["s"] for r in R)
V["bce"] = -V["sum"] / len(R)
V["rest"] = -sum(r["s"] for r in R[1:])
for z1 in (6, -3):
    k = "p6" if z1 == 6 else "pm3"
    V[k] = sig(z1)
    V[k + "_pen"] = -ln(sig(z1))
    V[k + "_bce"] = (V[k + "_pen"] + V["rest"]) / len(R)
assert V["pm3_pen"] > V["rest"]          # «одна строка весит больше четырёх остальных»
assert V["p6_pen"] < 0.005 and V["p6_bce"] < V["bce"]
assert abs(R[1]["right"] - R[4]["right"]) < 1e-12   # σ(−1,4) и σ(1,4): одинаковые штрафы строк 2 и 5

CE_E = [math.exp(z) for z in CE_Z]
V["ce_sum"] = sum(CE_E)
V["ce_lse"] = ln(V["ce_sum"])
CE_P = [e / V["ce_sum"] for e in CE_E]
CE_LN = [ln(p) for p in CE_P]
V["ce"] = -sum(y * l for y, l in zip(CE_Y, CE_LN))
assert abs(V["ce"] - (V["ce_lse"] - CE_Z[1])) < 1e-12
for z2, k in ((5, "ce5"), (-2, "cem2")):
    zz = [CE_Z[0], z2, CE_Z[2]]
    s = sum(math.exp(v) for v in zz)
    V[k + "_p"] = math.exp(z2) / s
    V[k] = -ln(V[k + "_p"])
assert V["ce5"] < 0.05 and V["cem2"] > 3
V["ce_raw"] = -ln(CE_Z[1])                # CE без softmax: −1·ln 2
V["ce_raw100"] = -ln(100)
V["ce_raw1000"] = -ln(1000)
assert V["ce_raw"] < 0 and V["ce_raw1000"] < V["ce_raw100"] < 0

T1 = [y * ln(p) + (1 - y) * ln(1 - p) for y, p in zip(TASK1["y"], TASK1["p"])]
V["t1"] = -sum(T1) / 3
T2 = [y * ln(p) for y, p in zip(TASK2["y"], TASK2["p"])]
V["t2"] = -sum(T2)
T3E = [math.exp(z) for z in TASK3["z"]]
V["t3sum"] = sum(T3E)
T3P = [e / V["t3sum"] for e in T3E]
V["t3"] = -ln(T3P[2])
assert abs(V["t3"] - (ln(V["t3sum"]) - 2)) < 1e-12

V["f64"] = 53 * ln(2)      # σ(z) == 1.0 в float64 при z ≳ 36,74
V["f32"] = 24 * ln(2)      # в float32 при z ≳ 16,64
V["ovf"] = ln(1.7976931348623157e308)   # EXP переполняется при −z > 709,78
assert sig(36.8) == 1.0 and sig(36.7) < 1.0

# Пять «правильных» вероятностей блока 1 — для текста
V.update({f"r{i + 1}": r["right"] for i, r in enumerate(R)})
V.update({f"p{i + 1}": r["p"] for i, r in enumerate(R)})
V.update({f"s{i + 1}": r["s"] for i, r in enumerate(R)})
V.update({f"cp{i + 1}": p for i, p in enumerate(CE_P)})
V.update({f"cl{i + 1}": l for i, l in enumerate(CE_LN)})
V.update({f"ce_e{i + 1}": e for i, e in enumerate(CE_E)})
V.update({f"t1_{i + 1}": v for i, v in enumerate(T1)})
V.update({f"t3e{i + 1}": v for i, v in enumerate(T3E)})
V.update({f"t3p{i + 1}": v for i, v in enumerate(T3P)})
V["ln2"] = ln(2)
V["t2_3"] = T2[2]


# ---------------------------------------------------------------- числа по-русски / по-английски
def num(x, lang, d=3, tex=False):
    """0,299 (ru, uz) / 0.299 (en); минус — «−» в тексте и «-» в TeX; в TeX запятая — {,}."""
    q = Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if q == 0:
        q = abs(q)
    s = f"{abs(q):f}"
    s = s.replace(".", "." if lang == "en" else ("{,}" if tex else ","))
    if q < 0:
        s = ("-" if tex else "−") + s
    return s


def fill(text, lang):
    """{key} или {key:d} → число из V; внутри $…$ — в записи TeX."""
    parts = text.split("$")
    for i, seg in enumerate(parts):
        parts[i] = re.sub(r"\{([a-z][a-z0-9_]*)(?::(\d))?\}",
                          lambda m: num(V[m.group(1)], lang, int(m.group(2) or 3), tex=i % 2 == 1) if m.group(1) in V else m.group(0), seg)
    return "$".join(parts)


def T(ru, en, uz):
    return {"ru": ru, "en": en, "uz": uz}


def pick(d, lang):
    return fill(d[lang], lang) if isinstance(d, dict) else d


# ---------------------------------------------------------------- страница
PAGE = {
    "ru": dict(
        title="Перекрёстная энтропия в Excel: BCE и CE по шагам",
        kicker="Практикум · ML / AI",
        dek="Разбор рабочей тетради: логит → sigmoid или softmax → формула потерь. Что показывает каждый лист и каждая колонка, почему логиты нельзя подавать в формулу напрямую — и тренировка с самопроверкой. Тетрадь можно скачать.",
        description="Разбор Excel-тетради по перекрёстной энтропии: binary cross-entropy и categorical cross-entropy по шагам, логиты без sigmoid и softmax, тренировка с самопроверкой. Файл .xlsx для скачивания.",
        excerpt="Разбор Excel-тетради по бинарной и категориальной перекрёстной энтропии: каждый лист, каждая колонка, все числа — по шагам. Что ломается, если забыть sigmoid или softmax. Тетрадь можно скачать и пересчитать самому.",
        count="листа", charts="графика", tasks="задания", min="мин чтения",
        dl_title="Рабочая тетрадь", dl_btn="Скачать тетрадь (.xlsx)", dl_kb="КБ",
        dl_text="4 листа: BCE, Categorical CE, Тренировка, Ответы. Жёлтые ячейки — входы, их можно менять: всё остальное пересчитается само. Открывается в Excel, LibreOffice Calc и Google Таблицах (Файл → Импорт).",
        dl_other="Другие языки:",
        live="Тетрадь в браузере", live_note="Тот же расчёт, что в листе: меняйте жёлтые ячейки — остальное пересчитается.",
        expand="Раскрыть все разборы", collapse="Свернуть",
    ),
    "en": dict(
        title="Cross-entropy in Excel: BCE and CE step by step",
        kicker="Practice · ML / AI",
        dek="A walk through a workbook: logit → sigmoid or softmax → loss formula. What every sheet and every column shows, why logits must not go into the formula directly, and a practice sheet that checks itself. The workbook can be downloaded.",
        description="A walk through an Excel workbook on cross-entropy: binary and categorical cross-entropy step by step, logits without sigmoid and softmax, self-checking practice. A .xlsx file to download.",
        excerpt="A walk through an Excel workbook on binary and categorical cross-entropy: every sheet, every column, every number step by step. What breaks if you forget sigmoid or softmax. Download the workbook and recompute it yourself.",
        count="sheets", charts="charts", tasks="tasks", min="min read",
        dl_title="The workbook", dl_btn="Download the workbook (.xlsx)", dl_kb="KB",
        dl_text="4 sheets: BCE, Categorical CE, Practice, Answers. Yellow cells are inputs you can change; everything else recalculates by itself. Opens in Excel, LibreOffice Calc and Google Sheets (File → Import).",
        dl_other="Other languages:",
        live="The workbook in the browser", live_note="The same computation as in the sheet: change the yellow cells and the rest recalculates.",
        expand="Expand all solutions", collapse="Collapse",
    ),
    "uz": dict(
        title="Excel’da kross-entropiya: BCE va CE qadamma-qadam",
        kicker="Amaliyot · ML / AI",
        dek="Ishchi daftar tahlili: logit → sigmoid yoki softmax → yo‘qotish formulasi. Har bir varaq va har bir ustun nimani ko‘rsatadi, nega logitlarni formulaga to‘g‘ridan-to‘g‘ri berib bo‘lmaydi — va o‘zini tekshiradigan mashq. Daftarni yuklab olish mumkin.",
        description="Kross-entropiya bo‘yicha Excel-daftar tahlili: binary va categorical cross-entropy qadamma-qadam, sigmoid va softmax’siz logitlar, o‘zini tekshiradigan mashq. Yuklab olish uchun .xlsx fayl.",
        excerpt="Binary va categorical cross-entropy bo‘yicha Excel-daftar tahlili: har bir varaq, har bir ustun, barcha sonlar — qadamma-qadam. Sigmoid yoki softmax unutilsa nima buziladi. Daftarni yuklab olib, o‘zingiz qayta hisoblang.",
        count="varaq", charts="grafik", tasks="topshiriq", min="daq o‘qish",
        dl_title="Ishchi daftar", dl_btn="Daftarni yuklab olish (.xlsx)", dl_kb="KB",
        dl_text="4 varaq: BCE, Categorical CE, Mashq, Javoblar. Sariq kataklar — kirish qiymatlari, ularni o‘zgartirish mumkin: qolgani o‘zi qayta hisoblanadi. Excel, LibreOffice Calc va Google Sheets’da ochiladi (Fayl → Import).",
        dl_other="Boshqa tillar:",
        live="Daftar brauzerda", live_note="Varaqdagi hisobning o‘zi: sariq kataklarni o‘zgartiring — qolgani qayta hisoblanadi.",
        expand="Barcha yechimlarni ochish", collapse="Yig‘ish",
    ),
}
LANG_LABEL = {"ru": "Русский", "en": "English", "uz": "O‘zbekcha"}


def count_label(lang):
    p = PAGE[lang]
    return f"4 {p['count']} · 3 {p['tasks']}"


HERO = r"\begin{gathered}\mathrm{BCE}=-\frac1n\sum_{i=1}^{n}\bigl[y_i\ln\hat y_i+(1-y_i)\ln(1-\hat y_i)\bigr]\\[6pt]\mathrm{CE}=-\sum_{k=1}^{K}y_k\ln\hat y_k\end{gathered}"

# ---------------------------------------------------------------- таблицы листов (общие для языков)
def nums_row(vals, lang, d=3):
    return [num(v, lang, d) for v in vals]


def bce_table(lang):
    h = T(["$i$", "$y$", "логит $z$", r"$\hat y=\sigma(z)$", r"$y\ln\hat y$", r"$(1-y)\ln(1-\hat y)$", "сумма двух"],
          ["$i$", "$y$", "logit $z$", r"$\hat y=\sigma(z)$", r"$y\ln\hat y$", r"$(1-y)\ln(1-\hat y)$", "sum of the two"],
          ["$i$", "$y$", "logit $z$", r"$\hat y=\sigma(z)$", r"$y\ln\hat y$", r"$(1-y)\ln(1-\hat y)$", "ikkalasining yig‘indisi"])[lang]
    rows = [[str(i + 1), str(r["y"]), num(r["z"], lang, 2), *nums_row([r["p"], r["a"], r["b"], r["s"]], lang)] for i, r in enumerate(R)]
    foot = T(["", "", "", "", "", "Σ по всем $i$", num(V["sum"], lang)], ["", "", "", "", "", "Σ over all $i$", num(V["sum"], lang)],
             ["", "", "", "", "", "barcha $i$ bo‘yicha Σ", num(V["sum"], lang)])[lang]
    rows += [foot, ["", "", "", "", "", "$n$", "5"], ["", "", "", "", "", r"<b>BCE = −Σ / n</b>", f"<b>{num(V['bce'], lang)}</b>"]]
    return ("table", h, rows, {"num": [1, 2, 3, 4, 5, 6]})


def ce_table(lang):
    h = T(["$k$", "$y$", "логит $z$", r"$\hat y=\mathrm{softmax}(z)$", r"$\ln\hat y$", r"$y\ln\hat y$"],
          ["$k$", "$y$", "logit $z$", r"$\hat y=\mathrm{softmax}(z)$", r"$\ln\hat y$", r"$y\ln\hat y$"],
          ["$k$", "$y$", "logit $z$", r"$\hat y=\mathrm{softmax}(z)$", r"$\ln\hat y$", r"$y\ln\hat y$"])[lang]
    rows = [[str(k + 1), str(CE_Y[k]), num(CE_Z[k], lang, 1 if CE_Z[k] % 1 else 0), num(CE_P[k], lang), num(CE_LN[k], lang), num(CE_Y[k] * CE_LN[k], lang)] for k in range(3)]
    rows += [["", "", r"$\Sigma\hat y$", num(sum(CE_P), lang), "Σ", num(-V["ce"], lang)],
             ["", "", "", "", "<b>CE = −Σ</b>", f"<b>{num(V['ce'], lang)}</b>"]]
    return ("table", h, rows, {"num": [1, 2, 3, 4, 5]})


ZONE_WORD = {
    "ru": dict(none="нет", prob="вероятность", logit="логит"),
    "en": dict(none="none", prob="probability", logit="logit"),
    "uz": dict(none="yo‘q", prob="ehtimollik", logit="logit"),
}


def zone_table(lang):
    w = ZONE_WORD[lang]
    h = T(["$x$", r"при $y=1$: $-\ln x$", r"при $y=0$: $-\ln(1-x)$", "зона"], ["$x$", r"for $y=1$: $-\ln x$", r"for $y=0$: $-\ln(1-x)$", "zone"],
          ["$x$", r"$y=1$ da: $-\ln x$", r"$y=0$ da: $-\ln(1-x)$", "zona"])[lang]
    rows = []
    for x in ZONE_X:
        a = num(-ln(x), lang) if x > 0 else w["none"]
        b = num(-ln(1 - x), lang) if x < 1 else w["none"]
        zone = w["prob"] if 0 < x < 1 else w["logit"]
        d = 2 if x in (0.01, 0.99) else (1 if x % 1 else 0)
        rows.append([num(x, lang, d), a, b, f'<span class="cew-zone {"ok" if 0 < x < 1 else "bad"}">{zone}</span>'])
    return ("table", h, rows, {"num": [0, 1, 2]})


def ce_zone_table(lang):
    w = ZONE_WORD[lang]
    h = T(["$x$", r"$-\ln x$", "зона"], ["$x$", r"$-\ln x$", "zone"], ["$x$", r"$-\ln x$", "zona"])[lang]
    rows = []
    for x in CE_ZONE_X:
        a = num(-ln(x), lang) if x > 0 else w["none"]
        zone = w["prob"] if 0 < x <= 1 else w["logit"]
        d = 2 if x == 0.01 else (1 if x % 1 else 0)
        rows.append([num(x, lang, d), a, f'<span class="cew-zone {"ok" if 0 < x <= 1 else "bad"}">{zone}</span>'])
    return ("table", h, rows, {"num": [0, 1]})


def squash_table(lang):
    h = ["$z$", r"$e^{-z}$", r"$\hat y=\dfrac{1}{1+e^{-z}}$", r"$1-\hat y$"]
    rows = [[num(z, lang, 0), num(math.exp(-z), lang, 4), num(sig(z), lang, 4), num(1 - sig(z), lang, 4)] for z in SQUASH_Z]
    return ("table", h, rows, {"num": [0, 1, 2, 3]})


def raw_bce_table(lang):
    w = T(dict(none="нет", nan="NaN", by="случайно в $(0;1)$"), dict(none="none", nan="NaN", by="in $(0, 1)$ by chance"),
          dict(none="yo‘q", nan="NaN", by="tasodifan $(0;1)$ da"))[lang]
    h = T(["$i$", "$y$", "$z$", r"$\ln z$", r"$\ln(1-z)$", r"$y\ln z+(1-y)\ln(1-z)$"], ["$i$", "$y$", "$z$", r"$\ln z$", r"$\ln(1-z)$", r"$y\ln z+(1-y)\ln(1-z)$"],
          ["$i$", "$y$", "$z$", r"$\ln z$", r"$\ln(1-z)$", r"$y\ln z+(1-y)\ln(1-z)$"])[lang]
    rows = []
    for i, r in enumerate(R):
        z, y = r["z"], r["y"]
        a = num(ln(z), lang) if z > 0 else w["none"]
        b = num(ln(1 - z), lang) if z < 1 else w["none"]
        res = num(y * ln(z) + (1 - y) * ln(1 - z), lang) + f" ({w['by']})" if 0 < z < 1 else f'<span class="cew-zone bad">{w["nan"]}</span>'
        rows.append([str(i + 1), str(y), num(z, lang, 1), a, b, res])
    return ("table", h, rows, {"num": [1, 2, 3, 4]})


def raw_ce_table(lang):
    h = ["$k$", "$y$", "$z$", r"$\ln z$", r"$y\ln z$"]
    rows = [[str(k + 1), str(CE_Y[k]), num(CE_Z[k], lang, 1 if CE_Z[k] % 1 else 0), num(ln(CE_Z[k]), lang), num(CE_Y[k] * ln(CE_Z[k]), lang)] for k in range(3)]
    rows.append(["", "", "", T("CE без softmax", "CE without softmax", "softmax’siz CE")[lang], f"<b>{num(V['ce_raw'], lang)}</b>"])
    return ("table", h, rows, {"num": [1, 2, 3, 4]})


# ---------------------------------------------------------------- разборы строк (TeX)
def bce_row_steps(lang):
    out = []
    for i, r in enumerate(R):
        n = i + 1
        z, y = r["z"], r["y"]
        zt = num(z, lang, 2, True)
        exp = f"e^{{-({zt})}}" if z < 0 else f"e^{{-{zt}}}"
        l1 = rf"\hat y_{n} = \frac{{1}}{{1+{exp}}} = \frac{{1}}{{1+{num(r['e'], lang, 4, True)}}} = {num(r['p'], lang, 3, True)}"
        if y == 1:
            l2 = (rf"y_{n}\ln\hat y_{n} = 1\cdot\ln {num(r['p'], lang, 3, True)} = {num(r['a'], lang, 3, True)},\quad "
                  rf"(1-y_{n})\ln(1-\hat y_{n}) = 0\cdot\ln {num(1 - r['p'], lang, 3, True)} = 0")
        else:
            l2 = (rf"y_{n}\ln\hat y_{n} = 0\cdot\ln {num(r['p'], lang, 3, True)} = 0,\quad "
                  rf"(1-y_{n})\ln(1-\hat y_{n}) = 1\cdot\ln {num(1 - r['p'], lang, 3, True)} = {num(r['b'], lang, 3, True)}")
        out.append((n, l1, l2))
    return out


# ---------------------------------------------------------------- тексты разделов
TITLES = {
    "ru": dict(map="Что в тетради", bce="Лист BCE: расчёт по шагам", raw="Логиты без sigmoid", zones="Две ветви и две стены",
               squash="Как sigmoid сжимает логит", bce_sum="Итог листа BCE", ce="Лист Categorical CE: расчёт по шагам",
               ce_raw="Логиты без softmax", ce_zone="Почему только $(0;\\,1]$", ce_sum="Итог листа Categorical CE",
               practice="Тренировка с самопроверкой", mistakes="Частые ошибки", summary="Итоги", quiz="Проверь себя"),
    "en": dict(map="What is in the workbook", bce="The BCE sheet: the computation step by step", raw="Logits without sigmoid", zones="Two branches and two walls",
               squash="How sigmoid squeezes a logit", bce_sum="Summary of the BCE sheet", ce="The Categorical CE sheet: the computation step by step",
               ce_raw="Logits without softmax", ce_zone="Why only $(0, 1]$", ce_sum="Summary of the Categorical CE sheet",
               practice="Self-checking practice", mistakes="Common mistakes", summary="Summary", quiz="Check yourself"),
    "uz": dict(map="Daftarda nima bor", bce="BCE varag‘i: hisob qadamma-qadam", raw="Sigmoid’siz logitlar", zones="Ikki tarmoq va ikki devor",
               squash="Sigmoid logitni qanday siqadi", bce_sum="BCE varag‘i xulosasi", ce="Categorical CE varag‘i: hisob qadamma-qadam",
               ce_raw="Softmax’siz logitlar", ce_zone="Nega faqat $(0;\\,1]$", ce_sum="Categorical CE varag‘i xulosasi",
               practice="O‘zini tekshiradigan mashq", mistakes="Ko‘p uchraydigan xatolar", summary="Xulosa", quiz="O‘zingizni tekshiring"),
}

MAP = {
    "ru": [
        ("p", "Тетрадь учит одной цепочке, которая стоит за выходом любого классификатора: сеть выдаёт <b>логит</b> — любое число от $-\\infty$ до $+\\infty$, «переводчик» (sigmoid для двух классов, softmax для $K$ классов) превращает его в вероятность, и только вероятность попадает в формулу потерь. Каждый лист проходит эту цепочку слева направо и показывает, что будет, если пропустить средний шаг."),
        ("table", ["Лист", "Что внутри", "Чему учит"], [
            ["<b>BCE</b>", "4 блока: расчёт для 5 объектов; те же логиты без sigmoid; таблица и график двух ветвей штрафа; как sigmoid сжимает логит", "бинарная перекрёстная энтропия, NaN от логитов, роль sigmoid"],
            ["<b>Categorical CE</b>", "3 блока: расчёт для 3 классов; логиты без softmax; таблица и график $-\\ln x$", "категориальная перекрёстная энтропия, отрицательный лосс без дна, роль softmax"],
            ["<b>Тренировка</b>", "3 задания: BCE для трёх объектов, CE после softmax, softmax вручную", "посчитать самому; рядом с ответом — ✓ или ✗ (допуск ±0,005)"],
            ["<b>Ответы</b>", "эталонные ответы ко всем заданиям — формулами", "сверить ход решения"]]),
        ("p", "Цвета ячеек везде одни и те же:"),
        ("html", '<ul class="cew-legend"><li><i class="cew-sw in"></i><b>жёлтые</b> — входы: метки $y$ и логиты $z$, их можно менять</li>'
                 '<li><i class="cew-sw tr"></i><b>голубые</b> — «переводчик» sigmoid или softmax: отдельный шаг, не часть формулы потерь</li>'
                 '<li><i class="cew-sw fm"></i><b>красные</b> — сама формула потерь; чем светлее, тем глубже внутри скобок</li>'
                 '<li><i class="cew-sw ok"></i><b>зелёные</b> и <i class="cew-sw bad"></i><b>красные зоны</b> в блоках 3 — где логарифмы существуют, а где нет</li></ul>'),
        ("callout", "key", "Как читать этот разбор", "Разделы идут в порядке листов и блоков тетради. Все числа на странице посчитаны из тех же входов, что в файле, и совпадают с ним до третьего знака. Под каждым листом — «Тетрадь в браузере»: тот же расчёт, который можно менять прямо здесь. Логарифм всюду натуральный: $\\ln$."),
    ],
    "en": [
        ("p", "The workbook teaches one chain that stands behind the output of any classifier: the network produces a <b>logit</b>, any number from $-\\infty$ to $+\\infty$; a “translator” (sigmoid for two classes, softmax for $K$ classes) turns it into a probability; and only the probability goes into the loss formula. Each sheet walks this chain from left to right and shows what happens if the middle step is skipped."),
        ("table", ["Sheet", "What is inside", "What it teaches"], [
            ["<b>BCE</b>", "4 blocks: the computation for 5 objects; the same logits without sigmoid; a table and a chart of the two penalty branches; how sigmoid squeezes a logit", "binary cross-entropy, NaN from logits, the role of sigmoid"],
            ["<b>Categorical CE</b>", "3 blocks: the computation for 3 classes; logits without softmax; a table and a chart of $-\\ln x$", "categorical cross-entropy, a negative loss with no floor, the role of softmax"],
            ["<b>Practice</b>", "3 tasks: BCE for three objects, CE after softmax, softmax by hand", "compute it yourself; a ✓ or ✗ appears next to the answer (tolerance ±0.005)"],
            ["<b>Answers</b>", "reference answers to all tasks, as formulas", "check your working"]]),
        ("p", "The cell colours are the same everywhere:"),
        ("html", '<ul class="cew-legend"><li><i class="cew-sw in"></i><b>yellow</b>: inputs, the labels $y$ and the logits $z$; you can change them</li>'
                 '<li><i class="cew-sw tr"></i><b>light blue</b>: the sigmoid or softmax “translator”, a separate step that is not part of the loss formula</li>'
                 '<li><i class="cew-sw fm"></i><b>red</b>: the loss formula itself; the lighter, the deeper inside the brackets</li>'
                 '<li><i class="cew-sw ok"></i><b>green</b> and <i class="cew-sw bad"></i><b>red zones</b> in blocks 3: where the logarithms exist and where they do not</li></ul>'),
        ("callout", "key", "How to read this walk-through", "The sections follow the sheets and blocks of the workbook. Every number on the page is computed from the same inputs as in the file and matches it to three decimals. Under each sheet there is “The workbook in the browser”: the same computation that you can change right here. The logarithm is natural everywhere: $\\ln$."),
    ],
    "uz": [
        ("p", "Daftar istalgan klassifikator chiqishi ortida turgan bitta zanjirni o‘rgatadi: tarmoq <b>logit</b> beradi — $-\\infty$ dan $+\\infty$ gacha istalgan son, «tarjimon» (ikki sinf uchun sigmoid, $K$ sinf uchun softmax) uni ehtimollikka aylantiradi, va faqat ehtimollik yo‘qotish formulasiga tushadi. Har bir varaq bu zanjirni chapdan o‘ngga bosib o‘tadi va o‘rta qadam tashlab ketilsa nima bo‘lishini ko‘rsatadi."),
        ("table", ["Varaq", "Ichida nima bor", "Nimani o‘rgatadi"], [
            ["<b>BCE</b>", "4 blok: 5 ta obyekt uchun hisob; o‘sha logitlar sigmoid’siz; jarimaning ikki tarmog‘i jadvali va grafigi; sigmoid logitni qanday siqadi", "binary cross-entropy, logitlardan NaN, sigmoid’ning roli"],
            ["<b>Categorical CE</b>", "3 blok: 3 ta sinf uchun hisob; softmax’siz logitlar; $-\\ln x$ jadvali va grafigi", "categorical cross-entropy, tubsiz manfiy loss, softmax’ning roli"],
            ["<b>Mashq</b>", "3 topshiriq: uchta obyekt uchun BCE, softmax’dan keyingi CE, softmax qo‘lda", "o‘zingiz hisoblang; javob yonida ✓ yoki ✗ chiqadi (ruxsat etilgan farq ±0,005)"],
            ["<b>Javoblar</b>", "barcha topshiriqlarga namunaviy javoblar — formulalar bilan", "yechim yo‘lini solishtirish"]]),
        ("p", "Kataklar ranglari hamma joyda bir xil:"),
        ("html", '<ul class="cew-legend"><li><i class="cew-sw in"></i><b>sariq</b> — kirish qiymatlari: $y$ belgilar va $z$ logitlar, ularni o‘zgartirish mumkin</li>'
                 '<li><i class="cew-sw tr"></i><b>havorang</b> — sigmoid yoki softmax «tarjimoni»: alohida qadam, yo‘qotish formulasining qismi emas</li>'
                 '<li><i class="cew-sw fm"></i><b>qizil</b> — yo‘qotish formulasining o‘zi; qanchalik och bo‘lsa, qavslar ichida shunchalik chuqur</li>'
                 '<li><i class="cew-sw ok"></i><b>yashil</b> va <i class="cew-sw bad"></i><b>qizil zonalar</b> 3-bloklarda — logarifmlar qayerda mavjud, qayerda yo‘q</li></ul>'),
        ("callout", "key", "Bu tahlilni qanday o‘qish kerak", "Bo‘limlar daftar varaqlari va bloklari tartibida. Sahifadagi barcha sonlar fayldagi o‘sha kirish qiymatlaridan hisoblangan va u bilan uchinchi xonagacha mos keladi. Har bir varaq ostida — «Daftar brauzerda»: o‘sha hisob, uni shu yerning o‘zida o‘zgartirish mumkin. Logarifm hamma joyda natural: $\\ln$."),
    ],
}

BCE_TEXT = {
    "ru": dict(
        intro="Блок 1 листа — пять объектов бинарной задачи: метка $y=1$ («да») или $y=0$ («нет») и логит $z$, который выдала сеть. Расчёт идёт в три шага, как колонки таблицы: вход → sigmoid → формула BCE.",
        legend=[("y_i", "правильный ответ для объекта $i$: 1 или 0"), ("z_i", "логит — «сырой» выход сети, любое число"),
                ("\\hat y_i=\\sigma(z_i)", "предсказанная вероятность ответа «да»"), ("n", "число объектов, здесь $n=5$")],
        steps_title="Разбор каждой строки",
        steps_lead="Шаг 2 (голубая колонка): $\\hat y=1/(1+e^{-z})$. Шаг 3 (красные колонки): два слагаемых и их сумма. В каждой строке одно слагаемое обнуляется множителем $y$ или $1-y$.",
        row="Строка",
        after="Сумма по всем строкам $\\Sigma = {sum}$, объектов $n=5$, поэтому $\\mathrm{BCE}=-\\Sigma/n = -({sum})/5 = {bce}$. Последняя серая строка листа считает то же другим путём — через СУММПРОИЗВ (SUMPRODUCT) обеих ветвей — и тоже даёт ${bce}$.",
        alive_t="В каждой строке живо одно слагаемое",
        alive="При $y=1$ остаётся $\\ln\\hat y$, при $y=0$ — $\\ln(1-\\hat y)$. То есть штраф строки всегда равен $-\\ln$(вероятности, которую модель дала <i>правильному</i> ответу). В блоке 1 эти вероятности равны ${r1}$, ${r2}$, ${r3}$, ${r4}$ и ${r5}$. У строк 2 и 5 штраф одинаковый, ${s5}$: логиты $-1{,}4$ и $1{,}4$ симметричны, а $\\sigma(-z)=1-\\sigma(z)$.",
        try_t="Попробуйте (как предлагает лист)",
        try_=["Логит строки 1: $2{,}2 \\to 6$. Тогда $\\hat y_1 = {p6}$, штраф строки ${p6_pen}$ — почти ноль, а BCE падает с ${bce}$ до ${p6_bce}$.",
              "Логит строки 1: $2{,}2 \\to -3$ при $y=1$. Тогда $\\hat y_1 = {pm3}$, штраф строки ${pm3_pen}$ — больше, чем у четырёх остальных строк вместе (${rest}$). BCE вырастает до ${pm3_bce}$: одна уверенная ошибка весит больше всего остального."],
    ),
    "en": dict(
        intro="Block 1 of the sheet holds five objects of a binary task: the label $y=1$ (“yes”) or $y=0$ (“no”) and the logit $z$ produced by the network. The computation has three steps, like the columns of the table: input → sigmoid → the BCE formula.",
        legend=[("y_i", "the correct answer for object $i$: 1 or 0"), ("z_i", "the logit, the raw output of the network, any number"),
                ("\\hat y_i=\\sigma(z_i)", "the predicted probability of “yes”"), ("n", "the number of objects, here $n=5$")],
        steps_title="Every row, step by step",
        steps_lead="Step 2 (the light blue column): $\\hat y=1/(1+e^{-z})$. Step 3 (the red columns): two terms and their sum. In each row one term is zeroed by the factor $y$ or $1-y$.",
        row="Row",
        after="The sum over all rows is $\\Sigma = {sum}$ and there are $n=5$ objects, so $\\mathrm{BCE}=-\\Sigma/n = -({sum})/5 = {bce}$. The last grey row of the sheet computes the same thing another way, with SUMPRODUCT over both branches, and also gives ${bce}$.",
        alive_t="Only one term is alive in each row",
        alive="For $y=1$, $\\ln\\hat y$ remains; for $y=0$, $\\ln(1-\\hat y)$. So the penalty of a row is always $-\\ln$(the probability the model gave to the <i>right</i> answer). In block 1 these probabilities are ${r1}$, ${r2}$, ${r3}$, ${r4}$ and ${r5}$. Rows 2 and 5 have the same penalty, ${s5}$: the logits $-1.4$ and $1.4$ are symmetric, and $\\sigma(-z)=1-\\sigma(z)$.",
        try_t="Try it (as the sheet suggests)",
        try_=["Logit of row 1: $2.2 \\to 6$. Then $\\hat y_1 = {p6}$, the row penalty is ${p6_pen}$, almost zero, and BCE falls from ${bce}$ to ${p6_bce}$.",
              "Logit of row 1: $2.2 \\to -3$ with $y=1$. Then $\\hat y_1 = {pm3}$ and the row penalty is ${pm3_pen}$: more than the other four rows together (${rest}$). BCE grows to ${pm3_bce}$: one confident mistake outweighs everything else."],
    ),
    "uz": dict(
        intro="Varaqning 1-blokida binary masalaning beshta obyekti bor: $y=1$ («ha») yoki $y=0$ («yo‘q») belgi va tarmoq bergan $z$ logit. Hisob jadval ustunlari kabi uch qadamdan iborat: kirish → sigmoid → BCE formulasi.",
        legend=[("y_i", "$i$ obyekt uchun to‘g‘ri javob: 1 yoki 0"), ("z_i", "logit — tarmoqning «xom» chiqishi, istalgan son"),
                ("\\hat y_i=\\sigma(z_i)", "«ha» javobining bashorat qilingan ehtimolligi"), ("n", "obyektlar soni, bu yerda $n=5$")],
        steps_title="Har bir qator tahlili",
        steps_lead="2-qadam (havorang ustun): $\\hat y=1/(1+e^{-z})$. 3-qadam (qizil ustunlar): ikki qo‘shiluvchi va ularning yig‘indisi. Har bir qatorda bitta qo‘shiluvchi $y$ yoki $1-y$ ko‘paytuvchi bilan nolga aylanadi.",
        row="Qator",
        after="Barcha qatorlar yig‘indisi $\\Sigma = {sum}$, obyektlar $n=5$ ta, shuning uchun $\\mathrm{BCE}=-\\Sigma/n = -({sum})/5 = {bce}$. Varaqning oxirgi kulrang qatori xuddi shuni boshqa yo‘l bilan — ikkala tarmoq bo‘yicha SUMPRODUCT orqali hisoblaydi va u ham ${bce}$ beradi.",
        alive_t="Har bir qatorda bitta qo‘shiluvchi tirik",
        alive="$y=1$ da $\\ln\\hat y$, $y=0$ da — $\\ln(1-\\hat y)$ qoladi. Ya’ni qator jarimasi doim $-\\ln$(model <i>to‘g‘ri</i> javobga bergan ehtimollik) ga teng. 1-blokda bu ehtimolliklar ${r1}$, ${r2}$, ${r3}$, ${r4}$ va ${r5}$. 2- va 5-qatorlarning jarimasi bir xil, ${s5}$: $-1{,}4$ va $1{,}4$ logitlar simmetrik, $\\sigma(-z)=1-\\sigma(z)$ esa.",
        try_t="Sinab ko‘ring (varaq taklif qilganidek)",
        try_=["1-qator logiti: $2{,}2 \\to 6$. U holda $\\hat y_1 = {p6}$, qator jarimasi ${p6_pen}$ — deyarli nol, BCE esa ${bce}$ dan ${p6_bce}$ gacha tushadi.",
              "1-qator logiti: $y=1$ da $2{,}2 \\to -3$. U holda $\\hat y_1 = {pm3}$, qator jarimasi ${pm3_pen}$ — qolgan to‘rtta qatorning birgalikdagi jarimasidan (${rest}$) katta. BCE ${pm3_bce}$ gacha o‘sadi: bitta ishonchli xato qolgan hammasidan og‘irroq."],
    ),
}

RAW_TEXT = {
    "ru": dict(
        intro="Блок 2 берёт те же метки и логиты и подаёт логиты в формулу BCE напрямую — как будто $z$ уже вероятность. У BCE две ветви, $\\ln z$ и $\\ln(1-z)$, и в вычислении существовать должны <b>обе</b>, даже та, что потом умножится на ноль.",
        rows="Что вышло по строкам:",
        items=["Строка 1, $z=2{,}2$: $\\ln 2{,}2 \\approx 0{,}788 > 0$ — «штраф» с обратным знаком, а $\\ln(1-2{,}2)=\\ln(-1{,}2)$ не существует.",
               "Строки 2 и 4, $z<0$: не существует $\\ln z$; строка 5, $z=1{,}4$: не существует $\\ln(1-z)$.",
               "Только строка 3 ($z=0{,}4$) «случайно» попала в $(0;1)$ и дала число $\\ln 0{,}4\\approx-0{,}916$. Но и оно бессмысленно: $0{,}4$ — логит, а не вероятность; настоящая вероятность здесь $\\sigma(0{,}4)={p3}$."],
        nan_t="Почему не спасает нулевой множитель",
        nan="В строке 1 вторая ветвь умножается на $1-y=0$, и кажется, что её можно не считать. Но компьютер сначала вычисляет логарифм, а потом умножает: в числах с плавающей точкой $\\ln(-1{,}2)=\\mathrm{NaN}$, $\\ln 0 = -\\infty$, а $0\\cdot\\mathrm{NaN}=\\mathrm{NaN}$ и $0\\cdot(-\\infty)=\\mathrm{NaN}$. В Excel то же самое выглядит как ошибка #ЧИСЛО! (#NUM!), поэтому лист ловит её через ЕСЛИОШИБКА (IFERROR) и пишет «NaN».",
        dead="Одной такой строки достаточно: среднее с NaN — NaN, градиенты — NaN, после шага оптимизатора веса сети тоже NaN. Обучение не «плохое», оно мёртвое. Итог блока: <b>BCE без sigmoid — NaN, BCE с sigmoid — {bce}</b>.",
        fix="Sigmoid решает обе проблемы сразу: $\\hat y\\in(0;1)$ и $1-\\hat y\\in(0;1)$, поэтому оба логарифма всегда существуют и оба $\\le 0$ — а значит, каждый штраф $\\ge 0$.",
    ),
    "en": dict(
        intro="Block 2 takes the same labels and logits and feeds the logits into the BCE formula directly, as if $z$ were already a probability. BCE has two branches, $\\ln z$ and $\\ln(1-z)$, and <b>both</b> must exist in the computation, even the one that is later multiplied by zero.",
        rows="What came out, row by row:",
        items=["Row 1, $z=2.2$: $\\ln 2.2 \\approx 0.788 > 0$ is a “penalty” with the opposite sign, and $\\ln(1-2.2)=\\ln(-1.2)$ does not exist.",
               "Rows 2 and 4, $z<0$: $\\ln z$ does not exist; row 5, $z=1.4$: $\\ln(1-z)$ does not exist.",
               "Only row 3 ($z=0.4$) landed in $(0, 1)$ “by chance” and gave a number, $\\ln 0.4\\approx-0.916$. Even that is meaningless: $0.4$ is a logit, not a probability; the real probability here is $\\sigma(0.4)={p3}$."],
        nan_t="Why a zero factor does not help",
        nan="In row 1 the second branch is multiplied by $1-y=0$, so it seems it need not be computed. But the computer evaluates the logarithm first and multiplies afterwards: in floating point $\\ln(-1.2)=\\mathrm{NaN}$, $\\ln 0 = -\\infty$, while $0\\cdot\\mathrm{NaN}=\\mathrm{NaN}$ and $0\\cdot(-\\infty)=\\mathrm{NaN}$. In Excel the same thing shows up as a #NUM! error, so the sheet catches it with IFERROR and writes “NaN”.",
        dead="One such row is enough: a mean with a NaN is NaN, the gradients are NaN, and after the optimizer step the network weights are NaN too. Training is not “bad”, it is dead. The result of the block: <b>BCE without sigmoid is NaN, BCE with sigmoid is {bce}</b>.",
        fix="Sigmoid solves both problems at once: $\\hat y\\in(0, 1)$ and $1-\\hat y\\in(0, 1)$, so both logarithms always exist and both are $\\le 0$, which makes every penalty $\\ge 0$.",
    ),
    "uz": dict(
        intro="2-blok o‘sha belgilar va logitlarni olib, logitlarni BCE formulasiga to‘g‘ridan-to‘g‘ri beradi — go‘yo $z$ allaqachon ehtimollik. BCE ning ikki tarmog‘i bor, $\\ln z$ va $\\ln(1-z)$, va hisobda <b>ikkalasi</b> ham mavjud bo‘lishi kerak — keyin nolga ko‘paytiriladigani ham.",
        rows="Qatorlar bo‘yicha nima chiqdi:",
        items=["1-qator, $z=2{,}2$: $\\ln 2{,}2 \\approx 0{,}788 > 0$ — teskari ishorali «jarima», $\\ln(1-2{,}2)=\\ln(-1{,}2)$ esa mavjud emas.",
               "2- va 4-qatorlar, $z<0$: $\\ln z$ mavjud emas; 5-qator, $z=1{,}4$: $\\ln(1-z)$ mavjud emas.",
               "Faqat 3-qator ($z=0{,}4$) «tasodifan» $(0;1)$ ga tushdi va son berdi: $\\ln 0{,}4\\approx-0{,}916$. Lekin u ham ma’nosiz: $0{,}4$ — logit, ehtimollik emas; bu yerdagi haqiqiy ehtimollik $\\sigma(0{,}4)={p3}$."],
        nan_t="Nega nol ko‘paytuvchi qutqarmaydi",
        nan="1-qatorda ikkinchi tarmoq $1-y=0$ ga ko‘paytiriladi va uni hisoblamasa ham bo‘ladigandek tuyuladi. Lekin kompyuter avval logarifmni hisoblaydi, keyin ko‘paytiradi: suzuvchi nuqtali sonlarda $\\ln(-1{,}2)=\\mathrm{NaN}$, $\\ln 0 = -\\infty$, $0\\cdot\\mathrm{NaN}=\\mathrm{NaN}$ va $0\\cdot(-\\infty)=\\mathrm{NaN}$. Excel’da bu #NUM! xatosi bo‘lib ko‘rinadi, shuning uchun varaq uni IFERROR bilan ushlaydi va «NaN» deb yozadi.",
        dead="Bitta shunday qator yetarli: NaN li o‘rtacha — NaN, gradiyentlar — NaN, optimizator qadamidan keyin tarmoq vaznlari ham NaN. O‘qitish «yomon» emas, u o‘lik. Blok natijasi: <b>sigmoid’siz BCE — NaN, sigmoid bilan BCE — {bce}</b>.",
        fix="Sigmoid ikkala muammoni birdan hal qiladi: $\\hat y\\in(0;1)$ va $1-\\hat y\\in(0;1)$, shuning uchun ikkala logarifm doim mavjud va ikkalasi $\\le 0$ — demak, har bir jarima $\\ge 0$.",
    ),
}

ZONES_TEXT = {
    "ru": dict(
        intro="Блок 3 объясняет, почему так: таблица подставляет в обе ветви BCE разные $x$ — и вероятности, и «логитные» значения вне $(0;1)$. Жёлтые $x$ в листе можно менять, а график под таблицей (лист строит его по $\\hat y$ от $0{,}02$ до $0{,}98$) показывает обе ветви целиком.",
        walls="У BCE две «стены». Ветвь $y=1$ — штраф $-\\ln x$ — уходит в бесконечность у нуля: уверенное «нет», когда правильный ответ «да». Ветвь $y=0$ — штраф $-\\ln(1-x)$ — уходит в бесконечность у единицы. Между стенами, в точке $x=0{,}5$, обе ветви дают одинаковый штраф $\\ln 2 \\approx {ln2}$ — цену полной неуверенности.",
        outside="Вне $(0;1)$ всё ломается: при $x\\le0$ нет $\\ln x$, при $x\\ge1$ нет $\\ln(1-x)$, при $x>1$ ветвь $y=1$ даёт отрицательный штраф (при $x=10$ он равен $-\\ln 10\\approx-2{,}303$ и дальше падает без дна), а при $x<0$ так же «ломается» ветвь $y=0$: при $x=-1$ её штраф $-\\ln 2\\approx-0{,}693$. Сеть, которой разрешили отрицательный лосс, будет просто раздувать логит.",
        fig="Потяните точку: зелёная полоса — вероятности, куда попадает sigmoid; красные — область логитов. Переключатель выбирает, какая ветвь считается штрафом.",
    ),
    "en": dict(
        intro="Block 3 explains why: the table plugs different $x$ into both BCE branches, both probabilities and “logit” values outside $(0, 1)$. The yellow $x$ in the sheet can be changed, and the chart under the table (the sheet draws it for $\\hat y$ from $0.02$ to $0.98$) shows both branches in full.",
        walls="BCE has two “walls”. The $y=1$ branch, the penalty $-\\ln x$, goes to infinity near zero: a confident “no” when the right answer is “yes”. The $y=0$ branch, the penalty $-\\ln(1-x)$, goes to infinity near one. Between the walls, at $x=0.5$, both branches give the same penalty $\\ln 2 \\approx {ln2}$: the price of complete uncertainty.",
        outside="Outside $(0, 1)$ everything breaks: for $x\\le0$ there is no $\\ln x$, for $x\\ge1$ there is no $\\ln(1-x)$, for $x>1$ the $y=1$ branch gives a negative penalty (at $x=10$ it is $-\\ln 10\\approx-2.303$ and it keeps falling with no floor), and for $x<0$ the $y=0$ branch breaks the same way: at $x=-1$ its penalty is $-\\ln 2\\approx-0.693$. A network that is allowed a negative loss will simply inflate the logit.",
        fig="Drag the point: the green band holds the probabilities where sigmoid lands; the red bands are the area of logits. The switch chooses which branch counts as the penalty.",
    ),
    "uz": dict(
        intro="3-blok nega shundayligini tushuntiradi: jadval BCE ning ikkala tarmog‘iga turli $x$ larni qo‘yadi — ehtimolliklarni ham, $(0;1)$ dan tashqaridagi «logit» qiymatlarni ham. Varaqdagi sariq $x$ larni o‘zgartirish mumkin, jadval ostidagi grafik (varaq uni $\\hat y$ ning $0{,}02$ dan $0{,}98$ gacha qiymatlari uchun chizadi) ikkala tarmoqni to‘liq ko‘rsatadi.",
        walls="BCE ning ikki «devori» bor. $y=1$ tarmog‘i — $-\\ln x$ jarima — nol yonida cheksizlikka ketadi: to‘g‘ri javob «ha» bo‘lganda ishonchli «yo‘q». $y=0$ tarmog‘i — $-\\ln(1-x)$ jarima — bir yonida cheksizlikka ketadi. Devorlar orasida, $x=0{,}5$ nuqtada, ikkala tarmoq bir xil jarima beradi: $\\ln 2 \\approx {ln2}$ — to‘liq ishonchsizlik bahosi.",
        outside="$(0;1)$ dan tashqarida hammasi buziladi: $x\\le0$ da $\\ln x$ yo‘q, $x\\ge1$ da $\\ln(1-x)$ yo‘q, $x>1$ da $y=1$ tarmog‘i manfiy jarima beradi ($x=10$ da u $-\\ln 10\\approx-2{,}303$ ga teng va tubsiz pasayishda davom etadi), $x<0$ da esa xuddi shunday $y=0$ tarmog‘i «buziladi»: $x=-1$ da uning jarimasi $-\\ln 2\\approx-0{,}693$. Manfiy loss’ga ruxsat berilgan tarmoq shunchaki logitni kattalashtiradi.",
        fig="Nuqtani torting: yashil yo‘lak — sigmoid tushadigan ehtimolliklar; qizil yo‘laklar — logitlar sohasi. Almashtirgich qaysi tarmoq jarima hisoblanishini tanlaydi.",
    ),
}

SQUASH_TEXT = {
    "ru": dict(
        intro="Блок 4 показывает сам «переводчик». Колонки листа — промежуточные шаги формулы $\\hat y = 1/(1+e^{-z})$: сначала $e^{-z}$, потом $\\hat y$, потом $1-\\hat y$.",
        why="Почему результат всегда в $(0;1)$: $e^{-z}>0$ при любом $z$, значит знаменатель $1+e^{-z}>1$ и $0<\\hat y<1$. При $z=0$ ровно $\\hat y=0{,}5$ — полная неуверенность; большие положительные $z$ дают уверенное «да», большие отрицательные — уверенное «нет». Таблица симметрична: $\\sigma(-z)=1-\\sigma(z)$, поэтому строки $z$ и $-z$ меняются колонками $\\hat y$ и $1-\\hat y$.",
        deep_t="Глубже: «хоть −1000, хоть +1000» — в математике, но не в компьютере",
        deep=["Лист пишет, что при любом логите $\\hat y$ остаётся строго между 0 и 1. Математически это так. Но в числах с плавающей точкой при $z \\gtrsim {f64:2}$ (float64; в float32 уже при $z \\gtrsim {f32:2}$) слагаемое $e^{-z}$ теряется рядом с единицей, $\\hat y$ округляется ровно до $1$, а $1-\\hat y$ — ровно до $0$. При $y=0$ штраф $-\\ln(1-\\hat y)$ становится $+\\infty$.",
              "С другой стороны, $e^{-z}$ переполняется при $z<-{ovf:2}$: в самом листе подстановка $z=-1000$ даёт ошибку #ЧИСЛО! (#NUM!) во всей строке, а $z=1000$ — ровно $\\hat y=1$ и $1-\\hat y=0$.",
              "Поэтому библиотеки не считают sigmoid и логарифм по отдельности. Они сразу считают штраф из логита через устойчивую запись $\\max(z,0)-yz+\\ln\\bigl(1+e^{-|z|}\\bigr)$ — так делает nn.BCEWithLogitsLoss. Это ровно то же число, что $-[y\\ln\\sigma(z)+(1-y)\\ln(1-\\sigma(z))]$, но без переполнений."],
        fig="Двигайте логит: кривая — $\\sigma(z)$, внизу — промежуточные значения, как в колонках листа.",
    ),
    "en": dict(
        intro="Block 4 shows the “translator” itself. The columns of the sheet are the intermediate steps of $\\hat y = 1/(1+e^{-z})$: first $e^{-z}$, then $\\hat y$, then $1-\\hat y$.",
        why="Why the result is always in $(0, 1)$: $e^{-z}>0$ for any $z$, so the denominator $1+e^{-z}>1$ and $0<\\hat y<1$. At $z=0$, exactly $\\hat y=0.5$: complete uncertainty; large positive $z$ give a confident “yes”, large negative ones a confident “no”. The table is symmetric: $\\sigma(-z)=1-\\sigma(z)$, so the rows $z$ and $-z$ swap the columns $\\hat y$ and $1-\\hat y$.",
        deep_t="Deeper: “−1000 or +1000” holds in mathematics, not in a computer",
        deep=["The sheet says that for any logit $\\hat y$ stays strictly between 0 and 1. Mathematically, it does. But in floating point, for $z \\gtrsim {f64:2}$ (float64; in float32 already for $z \\gtrsim {f32:2}$) the term $e^{-z}$ is lost next to one, $\\hat y$ rounds to exactly $1$ and $1-\\hat y$ to exactly $0$. With $y=0$ the penalty $-\\ln(1-\\hat y)$ becomes $+\\infty$.",
              "On the other side, $e^{-z}$ overflows for $z<-{ovf:2}$: in the sheet itself, entering $z=-1000$ gives a #NUM! error across the row, while $z=1000$ gives exactly $\\hat y=1$ and $1-\\hat y=0$.",
              "That is why libraries do not compute sigmoid and the logarithm separately. They compute the penalty straight from the logit with the stable form $\\max(z,0)-yz+\\ln\\bigl(1+e^{-|z|}\\bigr)$; this is what nn.BCEWithLogitsLoss does. It is exactly the same number as $-[y\\ln\\sigma(z)+(1-y)\\ln(1-\\sigma(z))]$, without overflows."],
        fig="Move the logit: the curve is $\\sigma(z)$; below are the intermediate values, as in the columns of the sheet.",
    ),
    "uz": dict(
        intro="4-blok «tarjimon»ning o‘zini ko‘rsatadi. Varaq ustunlari $\\hat y = 1/(1+e^{-z})$ formulasining oraliq qadamlari: avval $e^{-z}$, keyin $\\hat y$, keyin $1-\\hat y$.",
        why="Nega natija doim $(0;1)$ da: istalgan $z$ da $e^{-z}>0$, demak maxraj $1+e^{-z}>1$ va $0<\\hat y<1$. $z=0$ da aynan $\\hat y=0{,}5$ — to‘liq ishonchsizlik; katta musbat $z$ lar ishonchli «ha», katta manfiylari — ishonchli «yo‘q» beradi. Jadval simmetrik: $\\sigma(-z)=1-\\sigma(z)$, shuning uchun $z$ va $-z$ qatorlarida $\\hat y$ va $1-\\hat y$ ustunlari o‘rin almashadi.",
        deep_t="Chuqurroq: «−1000 mi, +1000 mi» — matematikada, lekin kompyuterda emas",
        deep=["Varaq istalgan logitda $\\hat y$ qat’iy 0 va 1 orasida qoladi deydi. Matematik jihatdan shunday. Lekin suzuvchi nuqtali sonlarda $z \\gtrsim {f64:2}$ da (float64; float32 da allaqachon $z \\gtrsim {f32:2}$ da) $e^{-z}$ qo‘shiluvchi birning yonida yo‘qoladi, $\\hat y$ aynan $1$ gacha, $1-\\hat y$ esa aynan $0$ gacha yaxlitlanadi. $y=0$ da $-\\ln(1-\\hat y)$ jarima $+\\infty$ ga aylanadi.",
              "Boshqa tomondan, $z<-{ovf:2}$ da $e^{-z}$ to‘lib ketadi: varaqning o‘zida $z=-1000$ qo‘yilsa, butun qatorda #NUM! xatosi chiqadi, $z=1000$ esa aynan $\\hat y=1$ va $1-\\hat y=0$ beradi.",
              "Shuning uchun kutubxonalar sigmoid va logarifmni alohida hisoblamaydi. Ular jarimani darhol logitdan barqaror ko‘rinishda hisoblaydi: $\\max(z,0)-yz+\\ln\\bigl(1+e^{-|z|}\\bigr)$ — nn.BCEWithLogitsLoss shunday qiladi. Bu $-[y\\ln\\sigma(z)+(1-y)\\ln(1-\\sigma(z))]$ bilan aynan bir xil son, faqat to‘lib ketishlarsiz."],
        fig="Logitni suring: egri chiziq — $\\sigma(z)$, pastda — varaq ustunlaridagi kabi oraliq qiymatlar.",
    ),
}

BCE_SUM = {
    "ru": ["BCE — это перекрёстная энтропия для двух классов, записанная через одно число $\\hat y$: вероятность «да» равна $\\hat y$, вероятность «нет» — $1-\\hat y$.",
           "Формула знает только про $\\hat y\\in(0;1)$. Логиты живут на всей прямой: поданные напрямую, они дают NaN или штраф с обратным знаком.",
           "Sigmoid сжимает любой логит в $(0;1)$. Softmax для двух классов даёт ровно sigmoid: $\\mathrm{softmax}(z_1,z_2)_1=\\sigma(z_1-z_2)$ — это одна и та же идея.",
           "Деление на $n$ нужно только для того, чтобы лосс не зависел от размера батча; саму форму штрафа задаёт $-\\ln$.",
           "В коде: <code>nn.BCEWithLogitsLoss</code> ждёт логиты (делает sigmoid сам и численно устойчивее), <code>nn.BCELoss</code> — уже вероятности."],
    "en": ["BCE is cross-entropy for two classes written through a single number $\\hat y$: the probability of “yes” is $\\hat y$, the probability of “no” is $1-\\hat y$.",
           "The formula knows only about $\\hat y\\in(0, 1)$. Logits live on the whole line: fed in directly, they give NaN or a penalty with the opposite sign.",
           "Sigmoid squeezes any logit into $(0, 1)$. Softmax for two classes gives exactly a sigmoid: $\\mathrm{softmax}(z_1,z_2)_1=\\sigma(z_1-z_2)$; it is one and the same idea.",
           "Dividing by $n$ is only there so that the loss does not depend on the batch size; the shape of the penalty comes from $-\\ln$.",
           "In code: <code>nn.BCEWithLogitsLoss</code> expects logits (applies sigmoid itself, and more stably), <code>nn.BCELoss</code> expects probabilities."],
    "uz": ["BCE — bu ikki sinf uchun kross-entropiya, bitta $\\hat y$ soni orqali yozilgan: «ha» ehtimolligi $\\hat y$, «yo‘q» ehtimolligi — $1-\\hat y$.",
           "Formula faqat $\\hat y\\in(0;1)$ ni biladi. Logitlar butun to‘g‘ri chiziqda yashaydi: to‘g‘ridan-to‘g‘ri berilsa, NaN yoki teskari ishorali jarima beradi.",
           "Sigmoid istalgan logitni $(0;1)$ ga siqadi. Ikki sinf uchun softmax aynan sigmoid beradi: $\\mathrm{softmax}(z_1,z_2)_1=\\sigma(z_1-z_2)$ — bu bitta g‘oya.",
           "$n$ ga bo‘lish faqat loss batch o‘lchamiga bog‘liq bo‘lmasligi uchun kerak; jarima shaklini $-\\ln$ belgilaydi.",
           "Kodda: <code>nn.BCEWithLogitsLoss</code> logitlarni kutadi (sigmoid’ni o‘zi bajaradi, sonli jihatdan barqarorroq), <code>nn.BCELoss</code> — tayyor ehtimolliklarni."],
}

CODE_BCE = '''import numpy as np

# метки и логиты из листа BCE
y = np.array([1, 0, 1, 0, 1])
z = np.array([2.2, -1.4, 0.4, -0.6, 1.4])

# шаг 2: sigmoid; шаг 3: формула BCE
p = 1 / (1 + np.exp(-z))
bce = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
print(round(bce, 3))       # 0.299

# то же прямо из логитов, устойчиво (так считает nn.BCEWithLogitsLoss)
s = np.maximum(z, 0) - z * y + np.log1p(np.exp(-np.abs(z)))
print(round(s.mean(), 3))  # 0.299

# PyTorch:
# nn.BCEWithLogitsLoss() ждёт логиты
# nn.BCELoss() ждёт вероятности'''

CODE_CE = '''import numpy as np

# логиты из листа Categorical CE; правильный класс k = 2 (индекс 1)
z = np.array([1.0, 2.0, 0.5])
k = 1

lse = np.log(np.sum(np.exp(z)))   # ln Σ e^z
p = np.exp(z - lse)               # шаг 2: softmax
print(np.round(p, 3), round(p.sum(), 3))
# [0.231 0.629 0.14 ] 1.0
print(round(-np.log(p[k]), 3))    # 0.464
print(round(lse - z[k], 3))       # 0.464: CE = ln Σ e^z − z_k

# PyTorch:
# nn.CrossEntropyLoss() ждёт логиты (softmax внутри)
# nn.NLLLoss() ждёт лог-вероятности (log_softmax)'''


def code(src, lang):
    if lang == "ru":
        return src
    pairs = {
        "en": [("метки и логиты из листа BCE", "labels and logits from the BCE sheet"), ("шаг 2: sigmoid; шаг 3: формула BCE", "step 2: sigmoid; step 3: the BCE formula"),
               ("то же прямо из логитов, устойчиво (так считает nn.BCEWithLogitsLoss)", "the same straight from logits, stably (as nn.BCEWithLogitsLoss does)"),
               ("ждёт логиты (softmax внутри)", "expects logits (softmax inside)"), ("ждёт лог-вероятности", "expects log-probabilities"),
               ("ждёт логиты", "expects logits"), ("ждёт вероятности", "expects probabilities"),
               ("логиты из листа Categorical CE; правильный класс k = 2 (индекс 1)", "logits from the Categorical CE sheet; correct class k = 2 (index 1)"),
               ("шаг 2: softmax", "step 2: softmax")],
        "uz": [("метки и логиты из листа BCE", "BCE varag‘idagi belgilar va logitlar"), ("шаг 2: sigmoid; шаг 3: формула BCE", "2-qadam: sigmoid; 3-qadam: BCE formulasi"),
               ("то же прямо из логитов, устойчиво (так считает nn.BCEWithLogitsLoss)", "xuddi shu logitlardan, barqaror (nn.BCEWithLogitsLoss kabi)"),
               ("ждёт логиты (softmax внутри)", "logitlarni kutadi (softmax ichida)"), ("ждёт лог-вероятности", "log-ehtimolliklarni kutadi"),
               ("ждёт логиты", "logitlarni kutadi"), ("ждёт вероятности", "ehtimolliklarni kutadi"),
               ("логиты из листа Categorical CE; правильный класс k = 2 (индекс 1)", "Categorical CE varag‘idagi logitlar; to‘g‘ri sinf k = 2 (indeks 1)"),
               ("шаг 2: softmax", "2-qadam: softmax")],
    }[lang]
    for a, b in pairs:
        src = src.replace(a, b)
    assert not re.search("[а-яА-ЯёЁ]", src), src
    return src


CE_TEXT = {
    "ru": dict(
        intro="Второй лист — та же цепочка для $K=3$ классов. На входе метки в виде «одного горячего» вектора (one-hot: $y_k=1$ только у правильного класса, здесь $k=2$) и три логита. Переводчик — softmax: он превращает логиты в вероятности, которые в сумме дают 1.",
        legend=[("z_k", "логит класса $k$"), ("\\hat y_k=\\dfrac{e^{z_k}}{\\sum_j e^{z_j}}", "softmax: вероятность класса $k$"),
                ("y_k", "1 у правильного класса, 0 у остальных"), ("K", "число классов, здесь $K=3$")],
        steps="Как получаются числа голубой колонки и колонки $\\ln\\hat y$:",
        s1="Экспоненты логитов и их сумма:",
        s2="Делим каждую экспоненту на сумму — это softmax. Проверка листа $\\Sigma\\hat y = 1$ выполняется всегда, при любых логитах:",
        s3="Логарифмы вероятностей. Удобно заметить, что $\\ln\\hat y_k = z_k - \\ln\\sum_j e^{z_j}$, а $\\ln {ce_sum:3} = {ce_lse}$. Поэтому все три логарифма — это логиты минус одно и то же число:",
        s4="В колонке $y\\ln\\hat y$ выживает одно слагаемое — то, где $y=1$. Значит, CE — это $-\\ln$ вероятности правильного класса (это и проверяет серая строка листа):",
        note="Отсюда видно, что CE зависит только от того, насколько логит правильного класса выделяется на фоне остальных: $\\mathrm{CE}=\\ln\\sum_j e^{z_j}-z_{\\text{правильного}}$.",
        try_t="Попробуйте (как предлагает лист)",
        try_=["Логит класса 2: $2 \\to 5$. Тогда $\\hat y_2={ce5_p}$ и $\\mathrm{CE}={ce5}$ — почти ноль.",
              "Логит класса 2: $2 \\to -2$. Тогда $\\hat y_2={cem2_p}$ и $\\mathrm{CE}={cem2}$ — большой штраф. Сумма $\\hat y$ в обоих случаях остаётся равной 1."],
    ),
    "en": dict(
        intro="The second sheet is the same chain for $K=3$ classes. The input is a one-hot label vector ($y_k=1$ only for the correct class, here $k=2$) and three logits. The translator is softmax: it turns logits into probabilities that sum to 1.",
        legend=[("z_k", "the logit of class $k$"), ("\\hat y_k=\\dfrac{e^{z_k}}{\\sum_j e^{z_j}}", "softmax: the probability of class $k$"),
                ("y_k", "1 for the correct class, 0 for the others"), ("K", "the number of classes, here $K=3$")],
        steps="How the numbers of the light blue column and the $\\ln\\hat y$ column come about:",
        s1="The exponentials of the logits and their sum:",
        s2="Divide each exponential by the sum; that is softmax. The sheet’s check $\\Sigma\\hat y = 1$ always holds, whatever the logits:",
        s3="The logarithms of the probabilities. Note that $\\ln\\hat y_k = z_k - \\ln\\sum_j e^{z_j}$ and $\\ln {ce_sum:3} = {ce_lse}$. So all three logarithms are the logits minus one and the same number:",
        s4="In the $y\\ln\\hat y$ column only one term survives: the one with $y=1$. So CE is $-\\ln$ of the probability of the correct class (which is what the grey row of the sheet checks):",
        note="This also shows that CE depends only on how far the logit of the correct class stands out from the rest: $\\mathrm{CE}=\\ln\\sum_j e^{z_j}-z_{\\text{correct}}$.",
        try_t="Try it (as the sheet suggests)",
        try_=["Logit of class 2: $2 \\to 5$. Then $\\hat y_2={ce5_p}$ and $\\mathrm{CE}={ce5}$, almost zero.",
              "Logit of class 2: $2 \\to -2$. Then $\\hat y_2={cem2_p}$ and $\\mathrm{CE}={cem2}$, a large penalty. In both cases the sum of $\\hat y$ stays equal to 1."],
    ),
    "uz": dict(
        intro="Ikkinchi varaq — $K=3$ sinf uchun o‘sha zanjir. Kirishda belgilar «bitta issiq» vektor ko‘rinishida (one-hot: $y_k=1$ faqat to‘g‘ri sinfda, bu yerda $k=2$) va uchta logit. Tarjimon — softmax: u logitlarni yig‘indisi 1 ga teng ehtimolliklarga aylantiradi.",
        legend=[("z_k", "$k$ sinf logiti"), ("\\hat y_k=\\dfrac{e^{z_k}}{\\sum_j e^{z_j}}", "softmax: $k$ sinf ehtimolligi"),
                ("y_k", "to‘g‘ri sinfda 1, qolganlarida 0"), ("K", "sinflar soni, bu yerda $K=3$")],
        steps="Havorang ustun va $\\ln\\hat y$ ustuni sonlari qanday hosil bo‘ladi:",
        s1="Logitlarning eksponentalari va ularning yig‘indisi:",
        s2="Har bir eksponentani yig‘indiga bo‘lamiz — bu softmax. Varaqdagi $\\Sigma\\hat y = 1$ tekshiruvi istalgan logitlarda doim bajariladi:",
        s3="Ehtimolliklar logarifmlari. $\\ln\\hat y_k = z_k - \\ln\\sum_j e^{z_j}$ ekanini va $\\ln {ce_sum:3} = {ce_lse}$ ni payqash qulay. Demak, uchala logarifm — logitlardan bitta va o‘sha sonni ayirish:",
        s4="$y\\ln\\hat y$ ustunida bitta qo‘shiluvchi qoladi — $y=1$ bo‘lgani. Demak, CE — to‘g‘ri sinf ehtimolligining $-\\ln$ i (varaqning kulrang qatori aynan shuni tekshiradi):",
        note="Bundan CE faqat to‘g‘ri sinf logiti qolganlari fonida qanchalik ajralib turishiga bog‘liqligi ko‘rinadi: $\\mathrm{CE}=\\ln\\sum_j e^{z_j}-z_{\\text{to‘g‘ri}}$.",
        try_t="Sinab ko‘ring (varaq taklif qilganidek)",
        try_=["2-sinf logiti: $2 \\to 5$. U holda $\\hat y_2={ce5_p}$ va $\\mathrm{CE}={ce5}$ — deyarli nol.",
              "2-sinf logiti: $2 \\to -2$. U holda $\\hat y_2={cem2_p}$ va $\\mathrm{CE}={cem2}$ — katta jarima. Ikkala holda ham $\\hat y$ yig‘indisi 1 ga teng qoladi."],
    ),
}


def ce_steps(lang):
    e = [num(v, lang, 3, True) for v in CE_E]
    zt = [num(z, lang, 1 if z % 1 else 0, True) for z in CE_Z]
    S = num(V["ce_sum"], lang, 3, True)
    l1 = rf"e^{{{zt[0]}}}={e[0]},\quad e^{{{zt[1]}}}={e[1]},\quad e^{{{zt[2]}}}={e[2]}\qquad \sum_j e^{{z_j}} = {S}"
    p = [num(v, lang, 3, True) for v in CE_P]
    l2 = rf"\hat y_1=\frac{{{e[0]}}}{{{S}}}={p[0]},\quad \hat y_2=\frac{{{e[1]}}}{{{S}}}={p[1]},\quad \hat y_3=\frac{{{e[2]}}}{{{S}}}={p[2]}"
    L = num(V["ce_lse"], lang, 3, True)
    l3 = rf"\ln\hat y_1={zt[0]}-{L}={num(CE_LN[0], lang, 3, True)},\quad \ln\hat y_2={zt[1]}-{L}={num(CE_LN[1], lang, 3, True)},\quad \ln\hat y_3={zt[2]}-{L}={num(CE_LN[2], lang, 3, True)}"
    l4 = rf"\mathrm{{CE}} = -(0\cdot\ln\hat y_1 + 1\cdot\ln\hat y_2 + 0\cdot\ln\hat y_3) = -\ln {p[1]} = {num(V['ce'], lang, 3, True)}"
    return l1, l2, l3, l4


CE_RAW_TEXT = {
    "ru": dict(
        intro="Блок 2 снова подаёт логиты напрямую — теперь в $\\mathrm{CE}=-\\sum_k y_k\\ln z_k$. Здесь все три логита оказались положительными, поэтому логарифмы существуют, но результат хуже ошибки: <b>CE без softmax $= -\\ln 2 \\approx {ce_raw}$</b> — отрицательный лосс, тогда как с softmax CE $= {ce}$.",
        why="Перекрёстная энтропия настоящих распределений вероятностей не бывает отрицательной: $\\mathrm{CE}(y,\\hat y)=H(y)+\\mathrm{KL}(y\\,\\|\\,\\hat y)\\ge 0$, а для one-hot метки это просто $-\\ln$ вероятности, которая не больше 1. Отрицательное число — верный признак того, что в формулу попали не вероятности.",
        items=["Логит правильного класса $\\to 100$: без softmax лосс $= -\\ln 100 \\approx {ce_raw100}$, при $1000$ — ${ce_raw1000}$, и дальше без дна. Сеть научится только раздувать этот логит. С softmax лосс упирается в 0 снизу.",
               "Логит правильного класса $\\to -1$: без softmax — ошибка, логарифма отрицательного числа нет. С softmax всё считается, просто лосс большой."],
    ),
    "en": dict(
        intro="Block 2 again feeds logits in directly, now into $\\mathrm{CE}=-\\sum_k y_k\\ln z_k$. Here all three logits happen to be positive, so the logarithms exist, but the result is worse than an error: <b>CE without softmax $= -\\ln 2 \\approx {ce_raw}$</b>, a negative loss, whereas with softmax CE $= {ce}$.",
        why="The cross-entropy of real probability distributions is never negative: $\\mathrm{CE}(y,\\hat y)=H(y)+\\mathrm{KL}(y\\,\\|\\,\\hat y)\\ge 0$, and for a one-hot label it is simply $-\\ln$ of a probability that is at most 1. A negative number is a sure sign that something other than probabilities went into the formula.",
        items=["Logit of the correct class $\\to 100$: without softmax the loss is $-\\ln 100 \\approx {ce_raw100}$, at $1000$ it is ${ce_raw1000}$, and so on with no floor. The network will learn only to inflate this logit. With softmax the loss is bounded below by 0.",
               "Logit of the correct class $\\to -1$: without softmax, an error, since a negative number has no logarithm. With softmax everything is computed; the loss is just large."],
    ),
    "uz": dict(
        intro="2-blok yana logitlarni to‘g‘ridan-to‘g‘ri beradi — endi $\\mathrm{CE}=-\\sum_k y_k\\ln z_k$ ga. Bu yerda uchala logit musbat bo‘lib chiqdi, shuning uchun logarifmlar mavjud, lekin natija xatodan ham yomon: <b>softmax’siz CE $= -\\ln 2 \\approx {ce_raw}$</b> — manfiy loss, softmax bilan esa CE $= {ce}$.",
        why="Haqiqiy ehtimollik taqsimotlarining kross-entropiyasi manfiy bo‘lmaydi: $\\mathrm{CE}(y,\\hat y)=H(y)+\\mathrm{KL}(y\\,\\|\\,\\hat y)\\ge 0$, one-hot belgi uchun esa bu shunchaki 1 dan katta bo‘lmagan ehtimollikning $-\\ln$ i. Manfiy son — formulaga ehtimolliklar emas, boshqa narsa tushganining aniq belgisi.",
        items=["To‘g‘ri sinf logiti $\\to 100$: softmax’siz loss $= -\\ln 100 \\approx {ce_raw100}$, $1000$ da — ${ce_raw1000}$, va hokazo, tubi yo‘q. Tarmoq faqat shu logitni kattalashtirishni o‘rganadi. Softmax bilan loss pastdan 0 ga taqaladi.",
               "To‘g‘ri sinf logiti $\\to -1$: softmax’siz — xato, manfiy sonning logarifmi yo‘q. Softmax bilan hammasi hisoblanadi, faqat loss katta."],
    ),
}

CE_ZONE_TEXT = {
    "ru": dict(
        intro="Блок 3 второго листа — та же «карта», что в BCE, но с одной ветвью $-\\ln x$: у CE штрафуется только вероятность правильного класса. Зелёная зона — $(0;1]$: от огромного штрафа у нуля до нулевого при $x=1$. Красные зоны — логиты: при $x\\le 0$ логарифма нет, при $x>1$ штраф отрицательный и падает без дна.",
        fig="Потяните точку: кривая $-\\ln x$ и её зоны. В отличие от BCE стена одна — у нуля.",
    ),
    "en": dict(
        intro="Block 3 of the second sheet is the same “map” as in BCE, but with a single branch $-\\ln x$: CE penalizes only the probability of the correct class. The green zone is $(0, 1]$: from a huge penalty near zero to zero at $x=1$. The red zones are logits: for $x\\le 0$ there is no logarithm, for $x>1$ the penalty is negative and falls with no floor.",
        fig="Drag the point: the curve $-\\ln x$ and its zones. Unlike BCE, there is only one wall, at zero.",
    ),
    "uz": dict(
        intro="Ikkinchi varaqning 3-bloki — BCE dagi o‘sha «xarita», lekin bitta $-\\ln x$ tarmog‘i bilan: CE faqat to‘g‘ri sinf ehtimolligini jarimalaydi. Yashil zona — $(0;1]$: nol yonidagi juda katta jarimadan $x=1$ dagi nol jarimagacha. Qizil zonalar — logitlar: $x\\le 0$ da logarifm yo‘q, $x>1$ da jarima manfiy va tubsiz pasayadi.",
        fig="Nuqtani torting: $-\\ln x$ egri chizig‘i va uning zonalari. BCE dan farqli ravishda devor bitta — nol yonida.",
    ),
}

CE_SUM = {
    "ru": ["Формула CE знает только про вероятности: числа от 0 до 1 с суммой 1.",
           "Логиты — любые числа от $-\\infty$ до $+\\infty$. Поданные в CE напрямую, они дают либо ошибку, либо отрицательный лосс без дна.",
           "Softmax — переводчик: сжимает любые логиты в $(0;1)$ с суммой 1. Поэтому CE и softmax всегда идут парой.",
           "В коде смотрите, кто делает softmax: <code>nn.CrossEntropyLoss</code> ждёт логиты (softmax внутри), <code>nn.NLLLoss</code> — уже лог-вероятности (<code>log_softmax</code>)."],
    "en": ["The CE formula knows only about probabilities: numbers from 0 to 1 that sum to 1.",
           "Logits are any numbers from $-\\infty$ to $+\\infty$. Fed into CE directly, they give either an error or a negative loss with no floor.",
           "Softmax is a translator: it squeezes any logits into $(0, 1)$ with a sum of 1. That is why CE and softmax always come as a pair.",
           "In code, check who applies softmax: <code>nn.CrossEntropyLoss</code> expects logits (softmax inside), <code>nn.NLLLoss</code> expects log-probabilities (<code>log_softmax</code>)."],
    "uz": ["CE formulasi faqat ehtimolliklarni biladi: yig‘indisi 1 ga teng, 0 dan 1 gacha sonlar.",
           "Logitlar — $-\\infty$ dan $+\\infty$ gacha istalgan sonlar. CE ga to‘g‘ridan-to‘g‘ri berilsa, yo xato, yo tubsiz manfiy loss beradi.",
           "Softmax — tarjimon: istalgan logitlarni yig‘indisi 1 bo‘lgan $(0;1)$ ga siqadi. Shuning uchun CE va softmax doim juft bo‘lib yuradi.",
           "Kodda softmax’ni kim bajarishini qarang: <code>nn.CrossEntropyLoss</code> logitlarni kutadi (softmax ichida), <code>nn.NLLLoss</code> — tayyor log-ehtimolliklarni (<code>log_softmax</code>)."],
}

K2_DEEP = {
    "ru": ("Глубже: почему BCE — это CE для двух классов",
           ["Возьмём два класса с логитами $z_1, z_2$. Softmax даёт $\\hat y_1=\\dfrac{e^{z_1}}{e^{z_1}+e^{z_2}}=\\dfrac{1}{1+e^{-(z_1-z_2)}}=\\sigma(z_1-z_2)$ и $\\hat y_2=1-\\hat y_1$.",
            "CE с one-hot меткой $(y,\\,1-y)$ равна $-[y\\ln\\hat y_1+(1-y)\\ln(1-\\hat y_1)]$ — ровно слагаемое BCE. Значит, бинарный классификатор с одним логитом $z$ — это softmax по паре $(z, 0)$, а BCE — частный случай CE."]),
    "en": ("Deeper: why BCE is CE for two classes",
           ["Take two classes with logits $z_1, z_2$. Softmax gives $\\hat y_1=\\dfrac{e^{z_1}}{e^{z_1}+e^{z_2}}=\\dfrac{1}{1+e^{-(z_1-z_2)}}=\\sigma(z_1-z_2)$ and $\\hat y_2=1-\\hat y_1$.",
            "CE with a one-hot label $(y,\\,1-y)$ equals $-[y\\ln\\hat y_1+(1-y)\\ln(1-\\hat y_1)]$, exactly the BCE term. So a binary classifier with a single logit $z$ is softmax over the pair $(z, 0)$, and BCE is a special case of CE."]),
    "uz": ("Chuqurroq: nega BCE — ikki sinf uchun CE",
           ["$z_1, z_2$ logitli ikki sinfni olaylik. Softmax $\\hat y_1=\\dfrac{e^{z_1}}{e^{z_1}+e^{z_2}}=\\dfrac{1}{1+e^{-(z_1-z_2)}}=\\sigma(z_1-z_2)$ va $\\hat y_2=1-\\hat y_1$ beradi.",
            "$(y,\\,1-y)$ one-hot belgili CE $-[y\\ln\\hat y_1+(1-y)\\ln(1-\\hat y_1)]$ ga teng — aynan BCE qo‘shiluvchisi. Demak, bitta $z$ logitli binary klassifikator — $(z, 0)$ juftligi bo‘yicha softmax, BCE esa CE ning xususiy holi."]),
}

PRACTICE_TEXT = {
    "ru": dict(
        intro="Лист «Тренировка» — три задания на калькулятор: впишите ответ в жёлтую ячейку, и рядом появится ✓ или ✗. Допуск — $\\pm 0{,}005$, логарифм натуральный. Ниже — те же задания прямо на странице; числа можно писать через запятую или точку.",
        tips="Чтобы уложиться в допуск, не округляйте промежуточные значения грубее трёх знаков после запятой. Ответ к слагаемому — отрицательное число (логарифм вероятности), а BCE и CE — положительные: в конце стоит минус.",
        answers="Ответы и разбор (лист «Ответы»)",
        a1="Задание 1. Каждое слагаемое — $\\ln$ вероятности правильного ответа: при $y=1$ это $\\ln\\hat y$, при $y=0$ — $\\ln(1-\\hat y)$.",
        a2="Задание 2. Вероятности уже после softmax; выживает только слагаемое правильного класса $k=3$.",
        a3="Задание 3. Softmax вручную для логитов $z=(0;\\,1;\\,2)$, правильный класс $k=3$.",
        a3b="Проверка через логиты: $\\mathrm{CE}=\\ln\\sum_j e^{z_j}-z_3=\\ln {t3sum:3}-2={t3}$.",
    ),
    "en": dict(
        intro="The Practice sheet has three calculator tasks: enter the answer in the yellow cell and a ✓ or ✗ appears next to it. The tolerance is $\\pm 0.005$; the logarithm is natural. Below are the same tasks right on the page; numbers can be written with a comma or a dot.",
        tips="To stay within the tolerance, do not round intermediate values to fewer than three decimals. The answer for a term is negative (the logarithm of a probability), while BCE and CE are positive: there is a minus at the end.",
        answers="Answers and solutions (the Answers sheet)",
        a1="Task 1. Each term is the $\\ln$ of the probability of the right answer: for $y=1$ it is $\\ln\\hat y$, for $y=0$ it is $\\ln(1-\\hat y)$.",
        a2="Task 2. The probabilities are already after softmax; only the term of the correct class $k=3$ survives.",
        a3="Task 3. Softmax by hand for the logits $z=(0, 1, 2)$, correct class $k=3$.",
        a3b="Check through the logits: $\\mathrm{CE}=\\ln\\sum_j e^{z_j}-z_3=\\ln {t3sum:3}-2={t3}$.",
    ),
    "uz": dict(
        intro="«Mashq» varag‘ida kalkulyator uchun uchta topshiriq bor: javobni sariq katakka yozing — yonida ✓ yoki ✗ chiqadi. Ruxsat etilgan farq — $\\pm 0{,}005$, logarifm natural. Quyida o‘sha topshiriqlar sahifaning o‘zida; sonlarni vergul yoki nuqta bilan yozish mumkin.",
        tips="Ruxsat etilgan farqga sig‘ish uchun oraliq qiymatlarni verguldan keyin uch xonadan qo‘polroq yaxlitlamang. Qo‘shiluvchi javobi — manfiy son (ehtimollik logarifmi), BCE va CE esa musbat: oxirida minus turadi.",
        answers="Javoblar va tahlil («Javoblar» varag‘i)",
        a1="1-topshiriq. Har bir qo‘shiluvchi — to‘g‘ri javob ehtimolligining $\\ln$ i: $y=1$ da bu $\\ln\\hat y$, $y=0$ da — $\\ln(1-\\hat y)$.",
        a2="2-topshiriq. Ehtimolliklar allaqachon softmax’dan keyin; faqat to‘g‘ri $k=3$ sinf qo‘shiluvchisi qoladi.",
        a3="3-topshiriq. $z=(0;\\,1;\\,2)$ logitlar uchun softmax qo‘lda, to‘g‘ri sinf $k=3$.",
        a3b="Logitlar orqali tekshiruv: $\\mathrm{CE}=\\ln\\sum_j e^{z_j}-z_3=\\ln {t3sum:3}-2={t3}$.",
    ),
}

TRAIN_UI = {
    "ru": dict(t1="Задание 1 — BCE ($n=3$)", t2="Задание 2 — категориальная CE ($K=3$), вероятности уже после softmax",
               t3="Задание 3 — softmax вручную, логиты $z=(0;\\,1;\\,2)$, правильный класс $k=3$",
               term="ваш ответ: слагаемое", yln="ваш ответ: $y\\ln\\hat y$", ez="ваш ответ: $e^{z}$", yh="ваш ответ: $\\hat y$",
               check="проверка", ok="✓ верно", bad="✗ ещё раз", nan="не число", reset="Очистить", score="Верно: {k} из {n}"),
    "en": dict(t1="Task 1: BCE ($n=3$)", t2="Task 2: categorical CE ($K=3$), probabilities already after softmax",
               t3="Task 3: softmax by hand, logits $z=(0, 1, 2)$, correct class $k=3$",
               term="your answer: the term", yln="your answer: $y\\ln\\hat y$", ez="your answer: $e^{z}$", yh="your answer: $\\hat y$",
               check="check", ok="✓ correct", bad="✗ try again", nan="not a number", reset="Clear", score="Correct: {k} of {n}"),
    "uz": dict(t1="1-topshiriq — BCE ($n=3$)", t2="2-topshiriq — categorical CE ($K=3$), ehtimolliklar softmax’dan keyin",
               t3="3-topshiriq — softmax qo‘lda, logitlar $z=(0;\\,1;\\,2)$, to‘g‘ri sinf $k=3$",
               term="javobingiz: qo‘shiluvchi", yln="javobingiz: $y\\ln\\hat y$", ez="javobingiz: $e^{z}$", yh="javobingiz: $\\hat y$",
               check="tekshiruv", ok="✓ to‘g‘ri", bad="✗ yana bir bor", nan="son emas", reset="Tozalash", score="To‘g‘ri: {k} / {n}"),
}


def train_config(lang):
    """Конфигурация виджета тренировки: значения и эталоны — из тех же данных, что «Ответы»."""
    return dict(tol=TOL, tasks=[
        dict(kind="bce", y=TASK1["y"], p=TASK1["p"], answers=T1, total=V["t1"]),
        dict(kind="ce", y=TASK2["y"], p=TASK2["p"], answers=T2, total=V["t2"]),
        dict(kind="softmax", z=TASK3["z"], k=TASK3["k"], exp=T3E, answers=T3P, total=V["t3"]),
    ])


def practice_answers(lang):
    t1 = [rf"i=1:\ 1\cdot\ln {num(0.8, lang, 1, True)} = {num(T1[0], lang, 3, True)},\quad i=2:\ 1\cdot\ln(1-{num(0.3, lang, 1, True)}) = \ln {num(0.7, lang, 1, True)} = {num(T1[1], lang, 3, True)},\quad i=3:\ \ln {num(0.5, lang, 1, True)} = {num(T1[2], lang, 3, True)}",
          rf"\mathrm{{BCE}} = -\frac{{({num(T1[0], lang, 3, True)}) + ({num(T1[1], lang, 3, True)}) + ({num(T1[2], lang, 3, True)})}}{{3}} = {num(V['t1'], lang, 3, True)}"]
    t2 = [rf"k=1:\ 0\cdot\ln {num(0.1, lang, 1, True)} = 0,\quad k=2:\ 0\cdot\ln {num(0.3, lang, 1, True)} = 0,\quad k=3:\ 1\cdot\ln {num(0.6, lang, 1, True)} = {num(T2[2], lang, 3, True)}",
          rf"\mathrm{{CE}} = -({num(T2[2], lang, 3, True)}) = {num(V['t2'], lang, 3, True)}"]
    e = [num(v, lang, 3, True) for v in T3E]
    S = num(V["t3sum"], lang, 3, True)
    p = [num(v, lang, 3, True) for v in T3P]
    t3 = [rf"e^0={e[0]},\quad e^1={e[1]},\quad e^2={e[2]}\qquad \sum = {S}",
          rf"\hat y = \Bigl(\tfrac{{{e[0]}}}{{{S}}};\ \tfrac{{{e[1]}}}{{{S}}};\ \tfrac{{{e[2]}}}{{{S}}}\Bigr) = ({p[0]};\ {p[1]};\ {p[2]})".replace(";", "," if lang == "en" else ";"),
          rf"\mathrm{{CE}} = -\ln\hat y_3 = -\ln {p[2]} = {num(V['t3'], lang, 3, True)}"]
    return t1, t2, t3


MISTAKES = {
    "ru": ["<b>Логиты в формулу, которая ждёт вероятности.</b> <code>nn.BCELoss</code> или <code>nn.NLLLoss</code> поверх «сырого» выхода сети — это блоки 2 обоих листов: NaN или отрицательный лосс.",
           "<b>Двойной переводчик.</b> Sigmoid перед <code>nn.BCEWithLogitsLoss</code> или softmax перед <code>nn.CrossEntropyLoss</code>: функция применит его второй раз. Ошибки не будет, но вероятности окажутся сжаты к середине, лосс почти перестанет меняться, и обучение забуксует.",
           "<b>Не тот логарифм.</b> В формулах — натуральный $\\ln$. На калькуляторе клавиша log часто означает $\\log_{10}$: $\\log_{10}0{,}8\\approx-0{,}097$ вместо $\\ln 0{,}8\\approx-0{,}223$.",
           "<b>Потерянный минус.</b> Логарифм вероятности отрицателен, поэтому сумма в колонке «сумма двух» отрицательна, а BCE и CE — положительны: $\\mathrm{BCE}=-\\Sigma/n$.",
           "<b>Перепутанная ветвь.</b> При $y=0$ штраф — $-\\ln(1-\\hat y)$, а не $-\\ln\\hat y$: штрафуется вероятность ответа «нет».",
           "<b>Слишком раннее округление.</b> Если округлить $e^{z}$ или $\\hat y$ до одного-двух знаков, ответ выйдет за допуск $\\pm0{,}005$."],
    "en": ["<b>Logits in a formula that expects probabilities.</b> <code>nn.BCELoss</code> or <code>nn.NLLLoss</code> on top of the raw network output: this is blocks 2 of both sheets, NaN or a negative loss.",
           "<b>A double translator.</b> Sigmoid before <code>nn.BCEWithLogitsLoss</code> or softmax before <code>nn.CrossEntropyLoss</code>: the function applies it a second time. There is no error, but the probabilities get squeezed towards the middle, the loss almost stops changing, and training stalls.",
           "<b>The wrong logarithm.</b> The formulas use the natural $\\ln$. On a calculator the log key often means $\\log_{10}$: $\\log_{10}0.8\\approx-0.097$ instead of $\\ln 0.8\\approx-0.223$.",
           "<b>A lost minus.</b> The logarithm of a probability is negative, so the “sum of the two” column is negative, while BCE and CE are positive: $\\mathrm{BCE}=-\\Sigma/n$.",
           "<b>The wrong branch.</b> For $y=0$ the penalty is $-\\ln(1-\\hat y)$, not $-\\ln\\hat y$: it is the probability of “no” that is penalized.",
           "<b>Rounding too early.</b> If you round $e^{z}$ or $\\hat y$ to one or two decimals, the answer falls outside the $\\pm0.005$ tolerance."],
    "uz": ["<b>Ehtimollik kutayotgan formulaga logitlar.</b> Tarmoqning «xom» chiqishi ustidan <code>nn.BCELoss</code> yoki <code>nn.NLLLoss</code> — bu ikkala varaqning 2-bloklari: NaN yoki manfiy loss.",
           "<b>Ikki karra tarjimon.</b> <code>nn.BCEWithLogitsLoss</code> oldidan sigmoid yoki <code>nn.CrossEntropyLoss</code> oldidan softmax: funksiya uni ikkinchi marta qo‘llaydi. Xato chiqmaydi, lekin ehtimolliklar o‘rtaga siqiladi, loss deyarli o‘zgarmay qoladi va o‘qitish to‘xtab qoladi.",
           "<b>Boshqa logarifm.</b> Formulalarda — natural $\\ln$. Kalkulyatorda log tugmasi ko‘pincha $\\log_{10}$ ni bildiradi: $\\ln 0{,}8\\approx-0{,}223$ o‘rniga $\\log_{10}0{,}8\\approx-0{,}097$.",
           "<b>Yo‘qolgan minus.</b> Ehtimollik logarifmi manfiy, shuning uchun «ikkalasining yig‘indisi» ustuni manfiy, BCE va CE esa musbat: $\\mathrm{BCE}=-\\Sigma/n$.",
           "<b>Adashtirilgan tarmoq.</b> $y=0$ da jarima $-\\ln\\hat y$ emas, $-\\ln(1-\\hat y)$: «yo‘q» javobining ehtimolligi jarimalanadi.",
           "<b>Juda erta yaxlitlash.</b> $e^{z}$ yoki $\\hat y$ bir-ikki xonagacha yaxlitlansa, javob $\\pm0{,}005$ farqdan chiqib ketadi."],
}
assert abs(math.log10(0.8) + 0.097) < 0.0005 and abs(ln(0.8) + 0.223) < 0.0005

SUMMARY = {
    "ru": dict(heads=["", "BCE (2 класса)", "Categorical CE ($K$ классов)"], rows=[
        ["выход сети", "один логит $z$", "$K$ логитов $z_1,\\dots,z_K$"],
        ["переводчик", "$\\sigma(z)=1/(1+e^{-z})$", "$\\mathrm{softmax}(z)_k=e^{z_k}/\\sum_j e^{z_j}$"],
        ["штраф объекта", "$-[y\\ln\\hat y+(1-y)\\ln(1-\\hat y)]$", "$-\\sum_k y_k\\ln\\hat y_k=-\\ln\\hat y_{\\text{прав}}$"],
        ["пример тетради", f"$\\mathrm{{BCE}}={num(V['bce'], 'ru', 3, True)}$ (5 объектов)", f"$\\mathrm{{CE}}={num(V['ce'], 'ru', 3, True)}$ (1 объект)"],
        ["без переводчика", "NaN", "$-\\ln 2\\approx" + num(V['ce_raw'], 'ru', 3, True) + "$ и ниже"],
        ["PyTorch", "<code>BCEWithLogitsLoss</code> (логиты)", "<code>CrossEntropyLoss</code> (логиты)"]],
        bullets=["Логит → переводчик → формула: формула потерь понимает только вероятности.",
                 "Штраф объекта — всегда $-\\ln$ вероятности правильного ответа: $0$ при уверенном верном ответе, $\\ln 2\\approx{ln2}$ при полной неуверенности, $+\\infty$ при уверенной ошибке.",
                 "Подробнее о самих функциях — в шпаргалке: <a class=\"ul\" href=\"../ml-formulas/bce/\">BCE</a>, <a class=\"ul\" href=\"../ml-formulas/cross-entropy/\">перекрёстная энтропия</a>, <a class=\"ul\" href=\"../ml-formulas/sigmoid/\">sigmoid</a>, <a class=\"ul\" href=\"../ml-formulas/softmax/\">softmax</a>."]),
    "en": dict(heads=["", "BCE (2 classes)", "Categorical CE ($K$ classes)"], rows=[
        ["network output", "one logit $z$", "$K$ logits $z_1,\\dots,z_K$"],
        ["translator", "$\\sigma(z)=1/(1+e^{-z})$", "$\\mathrm{softmax}(z)_k=e^{z_k}/\\sum_j e^{z_j}$"],
        ["penalty per object", "$-[y\\ln\\hat y+(1-y)\\ln(1-\\hat y)]$", "$-\\sum_k y_k\\ln\\hat y_k=-\\ln\\hat y_{\\text{correct}}$"],
        ["workbook example", f"$\\mathrm{{BCE}}={num(V['bce'], 'en', 3, True)}$ (5 objects)", f"$\\mathrm{{CE}}={num(V['ce'], 'en', 3, True)}$ (1 object)"],
        ["without the translator", "NaN", "$-\\ln 2\\approx" + num(V['ce_raw'], 'en', 3, True) + "$ and below"],
        ["PyTorch", "<code>BCEWithLogitsLoss</code> (logits)", "<code>CrossEntropyLoss</code> (logits)"]],
        bullets=["Logit → translator → formula: the loss formula understands only probabilities.",
                 "The penalty of an object is always $-\\ln$ of the probability of the right answer: $0$ for a confident right answer, $\\ln 2\\approx{ln2}$ for complete uncertainty, $+\\infty$ for a confident mistake.",
                 "More on the functions themselves in the cheat sheet: <a class=\"ul\" href=\"../ml-formulas/bce/\">BCE</a>, <a class=\"ul\" href=\"../ml-formulas/cross-entropy/\">cross-entropy</a>, <a class=\"ul\" href=\"../ml-formulas/sigmoid/\">sigmoid</a>, <a class=\"ul\" href=\"../ml-formulas/softmax/\">softmax</a>."]),
    "uz": dict(heads=["", "BCE (2 sinf)", "Categorical CE ($K$ sinf)"], rows=[
        ["tarmoq chiqishi", "bitta $z$ logit", "$K$ ta logit $z_1,\\dots,z_K$"],
        ["tarjimon", "$\\sigma(z)=1/(1+e^{-z})$", "$\\mathrm{softmax}(z)_k=e^{z_k}/\\sum_j e^{z_j}$"],
        ["obyekt jarimasi", "$-[y\\ln\\hat y+(1-y)\\ln(1-\\hat y)]$", "$-\\sum_k y_k\\ln\\hat y_k=-\\ln\\hat y_{\\text{to‘g‘ri}}$"],
        ["daftardagi misol", f"$\\mathrm{{BCE}}={num(V['bce'], 'uz', 3, True)}$ (5 obyekt)", f"$\\mathrm{{CE}}={num(V['ce'], 'uz', 3, True)}$ (1 obyekt)"],
        ["tarjimonsiz", "NaN", "$-\\ln 2\\approx" + num(V['ce_raw'], 'uz', 3, True) + "$ va undan past"],
        ["PyTorch", "<code>BCEWithLogitsLoss</code> (logitlar)", "<code>CrossEntropyLoss</code> (logitlar)"]],
        bullets=["Logit → tarjimon → formula: yo‘qotish formulasi faqat ehtimolliklarni tushunadi.",
                 "Obyekt jarimasi — doim to‘g‘ri javob ehtimolligining $-\\ln$ i: ishonchli to‘g‘ri javobda $0$, to‘liq ishonchsizlikda $\\ln 2\\approx{ln2}$, ishonchli xatoda $+\\infty$.",
                 "Funksiyalarning o‘zi haqida batafsil — qo‘llanmada: <a class=\"ul\" href=\"../ml-formulas/bce/\">BCE</a>, <a class=\"ul\" href=\"../ml-formulas/cross-entropy/\">kross-entropiya</a>, <a class=\"ul\" href=\"../ml-formulas/sigmoid/\">sigmoid</a>, <a class=\"ul\" href=\"../ml-formulas/softmax/\">softmax</a>."]),
}

QUIZ = {
    "ru": [
        dict(q="Модель дала $\\hat y=0{,}9$, а правильный ответ $y=0$. Чему равно слагаемое строки (колонка «сумма двух»)?",
             options=["$\\ln 0{,}9\\approx-0{,}105$", "$\\ln 0{,}1\\approx-2{,}303$", "$0$", "$-\\ln 0{,}9\\approx0{,}105$"], answer=1,
             explain="При $y=0$ живёт ветвь $(1-y)\\ln(1-\\hat y)=\\ln 0{,}1\\approx-2{,}303$: уверенная ошибка дорого стоит."),
        dict(q="Почему в BCE нельзя подать логит $z=2{,}2$ напрямую?",
             options=["Логарифм получится слишком маленьким", "$\\ln(1-2{,}2)$ не существует, а $0\\cdot\\mathrm{NaN}=\\mathrm{NaN}$ — весь батч станет NaN", "BCE работает только с целыми числами", "Сначала нужно разделить логит на $n$"], answer=1,
             explain="Обе ветви BCE должны существовать; множитель $1-y=0$ не спасает, потому что логарифм считается раньше умножения."),
        dict(q="Логиты $(1;\\,2;\\,0{,}5)$, правильный класс — второй. Чему равна CE?",
             options=["$0{,}629$", "$-0{,}464$", "$0{,}464$", "$1{,}464$"], answer=2,
             explain="$\\hat y_2=0{,}629$, $\\mathrm{CE}=-\\ln 0{,}629\\approx0{,}464$; или сразу $\\ln\\sum_j e^{z_j}-z_2=2{,}464-2$."),
        dict(q="CE без softmax вышла равной $-0{,}693$. О чём это говорит?",
             options=["Модель обучилась лучше идеала", "В формулу попали не вероятности: у настоящих вероятностей CE $\\ge 0$", "Это нормально для трёх классов", "Нужно взять логарифм по основанию 10"], answer=1,
             explain="Для one-hot метки CE $=-\\ln\\hat y_{\\text{прав}}$, а $\\hat y\\le1$, поэтому CE $\\ge0$. Отрицательный лосс — признак логитов вместо вероятностей."),
        dict(q="Что ждёт на вход <code>nn.CrossEntropyLoss</code>?",
             options=["Логиты: softmax она делает сама", "Вероятности после softmax", "Лог-вероятности после log_softmax", "Вероятности после sigmoid"], answer=0,
             explain="CrossEntropyLoss = log_softmax + NLLLoss. Лог-вероятности ждёт NLLLoss."),
        dict(q="Чему равна разность $\\ln\\hat y_2-\\ln\\hat y_1$ для логитов $(1;\\,2;\\,0{,}5)$?",
             options=["$1$ — разности логитов", "$0{,}397$ — разности вероятностей", "$\\ln 2$", "Зависит от суммы экспонент"], answer=0,
             explain="$\\ln\\hat y_k=z_k-\\ln\\sum_j e^{z_j}$, общий член сокращается: $\\ln\\hat y_2-\\ln\\hat y_1=z_2-z_1=1$ (в листе: $-0{,}464-(-1{,}464)$)."),
    ],
    "en": [
        dict(q="The model gave $\\hat y=0.9$ and the right answer is $y=0$. What is the term of the row (the “sum of the two” column)?",
             options=["$\\ln 0.9\\approx-0.105$", "$\\ln 0.1\\approx-2.303$", "$0$", "$-\\ln 0.9\\approx0.105$"], answer=1,
             explain="For $y=0$ the branch $(1-y)\\ln(1-\\hat y)=\\ln 0.1\\approx-2.303$ is alive: a confident mistake costs a lot."),
        dict(q="Why can’t the logit $z=2.2$ go into BCE directly?",
             options=["The logarithm would be too small", "$\\ln(1-2.2)$ does not exist, and $0\\cdot\\mathrm{NaN}=\\mathrm{NaN}$ turns the whole batch into NaN", "BCE works only with integers", "The logit must first be divided by $n$"], answer=1,
             explain="Both BCE branches must exist; the factor $1-y=0$ does not help, because the logarithm is computed before the multiplication."),
        dict(q="Logits $(1, 2, 0.5)$, the correct class is the second. What is CE?",
             options=["$0.629$", "$-0.464$", "$0.464$", "$1.464$"], answer=2,
             explain="$\\hat y_2=0.629$, $\\mathrm{CE}=-\\ln 0.629\\approx0.464$; or directly $\\ln\\sum_j e^{z_j}-z_2=2.464-2$."),
        dict(q="CE without softmax came out as $-0.693$. What does that tell you?",
             options=["The model trained better than perfect", "Something other than probabilities went in: for real probabilities CE $\\ge 0$", "It is normal for three classes", "You need the base-10 logarithm"], answer=1,
             explain="For a one-hot label CE $=-\\ln\\hat y_{\\text{correct}}$ and $\\hat y\\le1$, so CE $\\ge0$. A negative loss is a sign of logits instead of probabilities."),
        dict(q="What does <code>nn.CrossEntropyLoss</code> expect as input?",
             options=["Logits: it applies softmax itself", "Probabilities after softmax", "Log-probabilities after log_softmax", "Probabilities after sigmoid"], answer=0,
             explain="CrossEntropyLoss = log_softmax + NLLLoss. It is NLLLoss that expects log-probabilities."),
        dict(q="What is $\\ln\\hat y_2-\\ln\\hat y_1$ for the logits $(1, 2, 0.5)$?",
             options=["$1$, the difference of the logits", "$0.397$, the difference of the probabilities", "$\\ln 2$", "It depends on the sum of the exponentials"], answer=0,
             explain="$\\ln\\hat y_k=z_k-\\ln\\sum_j e^{z_j}$, the common term cancels: $\\ln\\hat y_2-\\ln\\hat y_1=z_2-z_1=1$ (in the sheet: $-0.464-(-1.464)$)."),
    ],
    "uz": [
        dict(q="Model $\\hat y=0{,}9$ berdi, to‘g‘ri javob esa $y=0$. Qator qo‘shiluvchisi («ikkalasining yig‘indisi» ustuni) nimaga teng?",
             options=["$\\ln 0{,}9\\approx-0{,}105$", "$\\ln 0{,}1\\approx-2{,}303$", "$0$", "$-\\ln 0{,}9\\approx0{,}105$"], answer=1,
             explain="$y=0$ da $(1-y)\\ln(1-\\hat y)=\\ln 0{,}1\\approx-2{,}303$ tarmog‘i tirik: ishonchli xato qimmatga tushadi."),
        dict(q="Nega BCE ga $z=2{,}2$ logitni to‘g‘ridan-to‘g‘ri berib bo‘lmaydi?",
             options=["Logarifm juda kichik chiqadi", "$\\ln(1-2{,}2)$ mavjud emas, $0\\cdot\\mathrm{NaN}=\\mathrm{NaN}$ esa butun batchni NaN qiladi", "BCE faqat butun sonlar bilan ishlaydi", "Avval logitni $n$ ga bo‘lish kerak"], answer=1,
             explain="BCE ning ikkala tarmog‘i mavjud bo‘lishi kerak; $1-y=0$ ko‘paytuvchi qutqarmaydi, chunki logarifm ko‘paytirishdan oldin hisoblanadi."),
        dict(q="Logitlar $(1;\\,2;\\,0{,}5)$, to‘g‘ri sinf — ikkinchisi. CE nimaga teng?",
             options=["$0{,}629$", "$-0{,}464$", "$0{,}464$", "$1{,}464$"], answer=2,
             explain="$\\hat y_2=0{,}629$, $\\mathrm{CE}=-\\ln 0{,}629\\approx0{,}464$; yoki darhol $\\ln\\sum_j e^{z_j}-z_2=2{,}464-2$."),
        dict(q="Softmax’siz CE $-0{,}693$ chiqdi. Bu nimani bildiradi?",
             options=["Model idealdan ham yaxshi o‘qidi", "Formulaga ehtimolliklar tushmagan: haqiqiy ehtimolliklarda CE $\\ge 0$", "Uch sinf uchun bu normal", "10 asosli logarifm olish kerak"], answer=1,
             explain="One-hot belgi uchun CE $=-\\ln\\hat y_{\\text{to‘g‘ri}}$, $\\hat y\\le1$, shuning uchun CE $\\ge0$. Manfiy loss — ehtimolliklar o‘rniga logitlar belgisi."),
        dict(q="<code>nn.CrossEntropyLoss</code> kirishga nimani kutadi?",
             options=["Logitlarni: softmax’ni o‘zi bajaradi", "Softmax’dan keyingi ehtimolliklarni", "log_softmax’dan keyingi log-ehtimolliklarni", "Sigmoid’dan keyingi ehtimolliklarni"], answer=0,
             explain="CrossEntropyLoss = log_softmax + NLLLoss. Log-ehtimolliklarni NLLLoss kutadi."),
        dict(q="$(1;\\,2;\\,0{,}5)$ logitlar uchun $\\ln\\hat y_2-\\ln\\hat y_1$ nimaga teng?",
             options=["$1$ — logitlar ayirmasi", "$0{,}397$ — ehtimolliklar ayirmasi", "$\\ln 2$", "Eksponentalar yig‘indisiga bog‘liq"], answer=0,
             explain="$\\ln\\hat y_k=z_k-\\ln\\sum_j e^{z_j}$, umumiy had qisqaradi: $\\ln\\hat y_2-\\ln\\hat y_1=z_2-z_1=1$ (varaqda: $-0{,}464-(-1{,}464)$)."),
    ],
}
# числа в тесте — проверка
assert num(ln(0.1), "ru") == "−2,303" and num(-ln(0.9), "ru") == "0,105"
assert num(CE_P[1] - CE_P[0], "en") == "0.397" and num(CE_LN[1] - CE_LN[0], "en") == "1.000"

NEWS = {
    "title": T("Новый материал: перекрёстная энтропия в Excel", "New material: cross-entropy in Excel", "Yangi material: Excel’da kross-entropiya"),
}

# Подписи виджетов (в JS числа форматирует FV)
WIDGET = {
    "ru": dict(i="i", y="y", z="логит z", p="ŷ = σ(z)", a="y·ln(ŷ)", b="(1−y)·ln(1−ŷ)", s="сумма двух", sum="Σ по всем i", n="n", bce="BCE = −Σ / n",
               check="проверка: среднее −ln(p верного)", raw="Логиты напрямую (без sigmoid)", lnz="ln z", ln1z="ln(1−z)", res="y·ln z + (1−y)·ln(1−z)", what="что произошло",
               none="нет", nan="NaN", by_chance="случайно попало в (0; 1)", broke="один из ln не существует → строка ломает батч",
               raw_total="BCE без sigmoid", sig_total="BCE с sigmoid", nan_total="NaN: хотя бы одна строка NaN", reset="Как в тетради",
               z6="логит строки 1 → 6", zm3="логит строки 1 → −3", k="k", py="ŷ = softmax(z)", lnp="ln(ŷ)", ylnp="y·ln(ŷ)", sump="Σ ŷ", ce="CE = −Σ",
               ce_check="проверка: −ln(ŷ правильного)", ylnz="y·ln z", ce_raw_total="CE без softmax", ce_total="CE с softmax",
               neg="ln > 0 → лосс отрицательный", lucky="z в (0; 1]: случайно сработало", nolog="z ≤ 0: логарифма нет → NaN",
               err="ошибка", z5="логит класса 2 → 5", zm2="логит класса 2 → −2", z100="логит класса 2 → 100", raw_ce="Логиты напрямую (без softmax)", correct="правильный класс",
               x="x", y1="y = 1: −ln x", y0="y = 0: −ln(1 − x)", pen="штраф", prob="вероятности", logit="логиты", branch="Ветвь", ce_branch="−ln x",
               sz="e^(−z)", yh="ŷ = 1/(1 + e^(−z))", omy="1 − ŷ", input="вход"),
    "en": dict(i="i", y="y", z="logit z", p="ŷ = σ(z)", a="y·ln(ŷ)", b="(1−y)·ln(1−ŷ)", s="sum of the two", sum="Σ over all i", n="n", bce="BCE = −Σ / n",
               check="check: mean −ln(p of the right answer)", raw="Logits directly (without sigmoid)", lnz="ln z", ln1z="ln(1−z)", res="y·ln z + (1−y)·ln(1−z)", what="what happened",
               none="none", nan="NaN", by_chance="landed in (0, 1) by chance", broke="one of the ln does not exist → the row breaks the batch",
               raw_total="BCE without sigmoid", sig_total="BCE with sigmoid", nan_total="NaN: at least one row is NaN", reset="As in the workbook",
               z6="logit of row 1 → 6", zm3="logit of row 1 → −3", k="k", py="ŷ = softmax(z)", lnp="ln(ŷ)", ylnp="y·ln(ŷ)", sump="Σ ŷ", ce="CE = −Σ",
               ce_check="check: −ln(ŷ of the correct class)", ylnz="y·ln z", ce_raw_total="CE without softmax", ce_total="CE with softmax",
               neg="ln > 0 → the loss is negative", lucky="z in (0, 1]: worked by chance", nolog="z ≤ 0: no logarithm → NaN",
               err="error", z5="logit of class 2 → 5", zm2="logit of class 2 → −2", z100="logit of class 2 → 100", raw_ce="Logits directly (without softmax)", correct="correct class",
               x="x", y1="y = 1: −ln x", y0="y = 0: −ln(1 − x)", pen="penalty", prob="probabilities", logit="logits", branch="Branch", ce_branch="−ln x",
               sz="e^(−z)", yh="ŷ = 1/(1 + e^(−z))", omy="1 − ŷ", input="input"),
    "uz": dict(i="i", y="y", z="logit z", p="ŷ = σ(z)", a="y·ln(ŷ)", b="(1−y)·ln(1−ŷ)", s="ikkalasining yig‘indisi", sum="barcha i bo‘yicha Σ", n="n", bce="BCE = −Σ / n",
               check="tekshiruv: −ln(to‘g‘ri javob p) o‘rtachasi", raw="Logitlar to‘g‘ridan-to‘g‘ri (sigmoid’siz)", lnz="ln z", ln1z="ln(1−z)", res="y·ln z + (1−y)·ln(1−z)", what="nima bo‘ldi",
               none="yo‘q", nan="NaN", by_chance="tasodifan (0; 1) ga tushdi", broke="ln lardan biri mavjud emas → qator batchni buzadi",
               raw_total="sigmoid’siz BCE", sig_total="sigmoid bilan BCE", nan_total="NaN: kamida bitta qator NaN", reset="Daftardagidek",
               z6="1-qator logiti → 6", zm3="1-qator logiti → −3", k="k", py="ŷ = softmax(z)", lnp="ln(ŷ)", ylnp="y·ln(ŷ)", sump="Σ ŷ", ce="CE = −Σ",
               ce_check="tekshiruv: −ln(to‘g‘ri sinf ŷ)", ylnz="y·ln z", ce_raw_total="softmax’siz CE", ce_total="softmax bilan CE",
               neg="ln > 0 → loss manfiy", lucky="z (0; 1] da: tasodifan ishladi", nolog="z ≤ 0: logarifm yo‘q → NaN",
               err="xato", z5="2-sinf logiti → 5", zm2="2-sinf logiti → −2", z100="2-sinf logiti → 100", raw_ce="Logitlar to‘g‘ridan-to‘g‘ri (softmax’siz)", correct="to‘g‘ri sinf",
               x="x", y1="y = 1: −ln x", y0="y = 0: −ln(1 − x)", pen="jarima", prob="ehtimolliklar", logit="logitlar", branch="Tarmoq", ce_branch="−ln x",
               sz="e^(−z)", yh="ŷ = 1/(1 + e^(−z))", omy="1 − ŷ", input="kirish"),
}
for _l in LANGS:
    assert set(WIDGET[_l]) == set(WIDGET["ru"]), _l
    assert set(TRAIN_UI[_l]) == set(TRAIN_UI["ru"]), _l
