"""Excel-тетрадь «Перекрёстная энтропия на практике» для скачивания: ru / en / uz.

Источник — tools/workbooks/cross_entropy_practice.xlsx: тетрадь автора, выгруженная из Google Таблиц
без изменений. build() пишет assets/files/cross-entropy-practice-<lang>.xlsx:

* ru — та же тетрадь; en и uz — её перевод. Переводятся только тексты: подписи ячеек, строковые
  литералы в формулах (и их сохранённые результаты), заголовки графиков, названия листов
  «Тренировка» и «Ответы». Формулы, числа, оформление и графики остаются как есть.
* Во всех трёх файлах исправлен дефект выгрузки Google Таблиц: у линий графиков белый цвет,
  и в Excel/LibreOffice графики выглядят пустыми. Линиям задаются цвета легенды тетради.
* Сборка детерминирована (фиксированные дата и порядок файлов в zip): повторный запуск
  не меняет файлы, если не менялись источник и переводы.

Проверка: tools/build.py вызывает build(); перевод обязан покрыть каждую строку с кириллицей —
иначе ошибка. Пересчёт в LibreOffice и сверка значений — в описании PR.
"""
import html
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "tools" / "workbooks" / "cross_entropy_practice.xlsx"
OUT_DIR = ROOT / "assets" / "files"
NAME = "cross-entropy-practice-{lang}.xlsx"
LANGS = ["ru", "en", "uz"]

SHEETS = {"Тренировка": {"en": "Practice", "uz": "Mashq"}, "Ответы": {"en": "Answers", "uz": "Javoblar"}}

# (по-русски, по-английски, по-узбекски) — ровно как в ячейках тетради
T = [
    # ---- лист «Тренировка» и «Ответы»
    ("Ответы к тренировке (не подглядывать раньше времени)", "Answers to the practice (no peeking too early)", "Mashq javoblari (oldindan qaramang)"),
    ("Тренировка: посчитайте на калькуляторе и впишите ответ", "Practice: compute on a calculator and enter the answer", "Mashq: kalkulyatorda hisoblang va javobni yozing"),
    ("Задание 1", "Task 1", "1-topshiriq"),
    ("Задание 2", "Task 2", "2-topshiriq"),
    ("Задание 3", "Task 3", "3-topshiriq"),
    ("Допуск ±0.005. Натуральный логарифм ln.", "Tolerance ±0.005. Natural logarithm ln.", "Ruxsat etilgan farq ±0,005. Natural logarifm ln."),
    ("Легенда:", "Legend:", "Belgilar:"),
    ("Легенда", "Legend", "Belgilar"),
    ("жёлтые ячейки с синим текстом — меняйте их", "yellow cells with blue text: change them", "ko‘k matnli sariq kataklar — ularni o‘zgartiring"),
    ("остальное — формулы, пересчитываются сами", "everything else is formulas that recalculate by themselves", "qolgani — formulalar, o‘zi qayta hisoblanadi"),
    ("Задание 1 — BCE (n=3)", "Task 1: BCE (n=3)", "1-topshiriq — BCE (n=3)"),
    ("ваш ответ: слагаемое", "your answer: the term", "javobingiz: qo‘shiluvchi"),
    ("проверка", "check", "tekshiruv"),
    ("пример заполнения: −0.223", "example of an entry: −0.223", "to‘ldirish namunasi: −0,223"),
    ("Задание 2 — Categorical CE (K=3), вероятности уже после softmax", "Task 2: categorical CE (K=3), probabilities already after softmax",
     "2-topshiriq — Categorical CE (K=3), ehtimolliklar softmax’dan keyin"),
    ("ваш ответ: y·ln(ŷ)", "your answer: y·ln(ŷ)", "javobingiz: y·ln(ŷ)"),
    ("Задание 3 — softmax вручную, логиты z = [0, 1, 2], правильный класс k=3", "Task 3: softmax by hand, logits z = [0, 1, 2], correct class k=3",
     "3-topshiriq — softmax qo‘lda, logitlar z = [0, 1, 2], to‘g‘ri sinf k=3"),
    ("ваш ответ: exp(z)", "your answer: exp(z)", "javobingiz: exp(z)"),
    ("ваш ответ: ŷ", "your answer: ŷ", "javobingiz: ŷ"),
    ("проверка ŷ", "check ŷ", "ŷ tekshiruvi"),
    ("✓ верно", "✓ correct", "✓ to‘g‘ri"),
    ("✗ ещё раз", "✗ try again", "✗ yana bir bor"),
    # ---- лист «Categorical CE»
    ("Categorical cross-entropy — шаг за шагом", "Categorical cross-entropy, step by step", "Categorical cross-entropy — qadamma-qadam"),
    ("жёлтое — вводите сами", "yellow: you enter it", "sariq — o‘zingiz kiritasiz"),
    ("голубое — softmax (отдельный шаг, не часть CE)", "light blue: softmax (a separate step, not part of CE)", "havorang — softmax (alohida qadam, CE qismi emas)"),
    ("красное — сама формула CE, светлее = внутри", "red: the CE formula itself, lighter = inside", "qizil — CE formulasining o‘zi, ochrog‘i = ichkarida"),
    ("1. Расчёт: логиты → softmax → CE", "1. Computation: logits → softmax → CE", "1. Hisob: logitlar → softmax → CE"),
    ("шаг 1: вход", "step 1: input", "1-qadam: kirish"),
    ("шаг 2: softmax", "step 2: softmax", "2-qadam: softmax"),
    ("шаг 3: формула CE →", "step 3: the CE formula →", "3-qadam: CE formulasi →"),
    ("y (1 = правильный класс)", "y (1 = correct class)", "y (1 = to‘g‘ri sinf)"),
    ("логит z", "logit z", "logit z"),
    ("← у softmax всегда 1", "← always 1 for softmax", "← softmax’da doim 1"),
    ("проверка: −ln(ŷ правильного)", "check: −ln(ŷ of the correct class)", "tekshiruv: −ln(to‘g‘ri sinf ŷ)"),
    ("В столбце y·ln(ŷ) выживает одно слагаемое — то, где y = 1. Поэтому CE = −ln(вероятности правильного класса).",
     "In the y·ln(ŷ) column only one term survives: the one where y = 1. So CE = −ln(probability of the correct class).",
     "y·ln(ŷ) ustunida bitta qo‘shiluvchi qoladi — y = 1 bo‘lgani. Shuning uchun CE = −ln(to‘g‘ri sinf ehtimolligi)."),
    ("Попробуйте: логит k=2 поставьте 5 → CE почти 0.  Поставьте −2 → CE большой. Сумма ŷ при этом остаётся 1.",
     "Try it: set the logit of k=2 to 5 → CE is almost 0.  Set it to −2 → CE is large. The sum of ŷ stays 1.",
     "Sinab ko‘ring: k=2 logitini 5 qiling → CE deyarli 0.  −2 qiling → CE katta. ŷ yig‘indisi esa 1 bo‘lib qoladi."),
    ("2. Что будет, если подать в CE логиты напрямую (без softmax)", "2. What happens if logits go into CE directly (without softmax)",
     "2. Logitlar CE ga to‘g‘ridan-to‘g‘ri (softmax’siz) berilsa nima bo‘ladi"),
    ("логит z (те же)", "logit z (the same)", "logit z (o‘sha)"),
    ("ln(z) напрямую", "ln(z) directly", "ln(z) to‘g‘ridan-to‘g‘ri"),
    ("что произошло", "what happened", "nima bo‘ldi"),
    ("CE без softmax", "CE without softmax", "softmax’siz CE"),
    ("CE с softmax", "CE with softmax", "softmax bilan CE"),
    ("ссылка на блок 1 — для сравнения", "link to block 1, for comparison", "1-blokka havola — taqqoslash uchun"),
    ("Попробуйте в блоке 1: логит k=2 → 100. Без softmax лосс уйдёт в −4.6, при 1000 → −6.9 и т.д. без дна: сеть будет просто раздувать логит и ничему не учиться. С softmax лосс упрётся в 0.",
     "Try it in block 1: logit of k=2 → 100. Without softmax the loss goes to −4.6, at 1000 → −6.9 and so on with no floor: the network will just inflate the logit and learn nothing. With softmax the loss stops at 0.",
     "1-blokda sinab ko‘ring: k=2 logiti → 100. Softmax’siz loss −4,6 ga tushadi, 1000 da → −6,9 va hokazo, tubi yo‘q: tarmoq shunchaki logitni kattalashtiradi va hech narsa o‘rganmaydi. Softmax bilan loss 0 ga borib taqaladi."),
    ("Попробуйте: логит k=2 → −1. Без softmax — ошибка (ln отрицательного числа не существует). С softmax — всё считается, просто лосс большой.",
     "Try it: logit of k=2 → −1. Without softmax: an error (the ln of a negative number does not exist). With softmax everything is computed; the loss is just large.",
     "Sinab ko‘ring: k=2 logiti → −1. Softmax’siz — xato (manfiy sonning ln i mavjud emas). Softmax bilan — hammasi hisoblanadi, faqat loss katta."),
    ("3. Почему так: функция −ln(x) работает только на отрезке (0, 1]", "3. Why: the function −ln(x) works only on the interval (0, 1]",
     "3. Nega shunday: −ln(x) funksiyasi faqat (0, 1] oralig‘ida ishlaydi"),
    ("x — что подали в ln", "x: what went into ln", "x — ln ga nima berildi"),
    ("зона", "zone", "zona"),
    ("смысл", "meaning", "ma’nosi"),
    ("логарифм не существует → NaN", "the logarithm does not exist → NaN", "logarifm mavjud emas → NaN"),
    ("вероятность", "probability", "ehtimollik"),
    ("почти 0 на правильном классе → огромный штраф", "almost 0 on the correct class → a huge penalty", "to‘g‘ri sinfda deyarli 0 → juda katta jarima"),
    ("плохой ответ → большой штраф", "a bad answer → a large penalty", "yomon javob → katta jarima"),
    ("неуверенный ответ → средний штраф", "an unsure answer → a medium penalty", "ishonchsiz javob → o‘rtacha jarima"),
    ("хороший ответ → маленький штраф", "a good answer → a small penalty", "yaxshi javob → kichik jarima"),
    ("идеальный ответ → штраф 0 (минимум)", "a perfect answer → penalty 0 (the minimum)", "ideal javob → jarima 0 (minimum)"),
    ("лосс < 0 — «лучше идеала», бессмыслица", "loss < 0: “better than perfect”, nonsense", "loss < 0 — «idealdan ham yaxshi», bema’nilik"),
    ("ещё меньше — сеть хочет увеличивать x", "even smaller: the network wants to increase x", "yanada kichik — tarmoq x ni kattalashtirishni xohlaydi"),
    ("дна нет: лосс → −∞, обучение расходится", "no floor: loss → −∞, training diverges", "tubi yo‘q: loss → −∞, o‘qitish uzoqlashadi"),
    ("Зелёное — зона вероятностей, куда softmax всегда попадает. Красное — зона логитов, куда CE напрямую подавать нельзя. Значения x в жёлтых ячейках можно менять.",
     "Green: the zone of probabilities, where softmax always lands. Red: the zone of logits, which must not go into CE directly. The x values in the yellow cells can be changed.",
     "Yashil — ehtimolliklar zonasi, softmax doim shu yerga tushadi. Qizil — logitlar zonasi, ularni CE ga to‘g‘ridan-to‘g‘ri berib bo‘lmaydi. Sariq kataklardagi x qiymatlarini o‘zgartirish mumkin."),
    ("Итог", "Summary", "Xulosa"),
    ("• Формула CE знает только про вероятности: числа от 0 до 1, сумма = 1.", "• The CE formula knows only about probabilities: numbers from 0 to 1 that sum to 1.",
     "• CE formulasi faqat ehtimolliklarni biladi: 0 dan 1 gacha sonlar, yig‘indisi = 1."),
    ("• Логиты — любые числа от −∞ до +∞. Напрямую в CE они дают либо ошибку, либо отрицательный лосс без дна.",
     "• Logits are any numbers from −∞ to +∞. Fed into CE directly, they give either an error or a negative loss with no floor.",
     "• Logitlar — −∞ dan +∞ gacha istalgan sonlar. CE ga to‘g‘ridan-to‘g‘ri berilsa, yo xato, yo tubi yo‘q manfiy loss beradi."),
    ("• Softmax — переводчик: сжимает любые логиты в (0, 1) с суммой 1. Поэтому на карточке написано «CE + softmax».",
     "• Softmax is a translator: it squeezes any logits into (0, 1) with a sum of 1. That is why the card says “CE + softmax”.",
     "• Softmax — tarjimon: istalgan logitlarni yig‘indisi 1 bo‘lgan (0, 1) oralig‘iga siqadi. Shuning uchun kartochkada «CE + softmax» deb yozilgan."),
    ("• В коде смотрите, кто делает softmax: nn.CrossEntropyLoss ждёт логиты (делает сам), nn.NLLLoss ждёт уже лог-вероятности.",
     "• In code, check who applies softmax: nn.CrossEntropyLoss expects logits (applies it itself), nn.NLLLoss expects log-probabilities.",
     "• Kodda softmax’ni kim bajarishini qarang: nn.CrossEntropyLoss logitlarni kutadi (o‘zi bajaradi), nn.NLLLoss esa tayyor log-ehtimolliklarni kutadi."),
    ("z > 1: ln положительный → лосс ОТРИЦАТЕЛЬНЫЙ", "z > 1: ln is positive → the loss is NEGATIVE", "z > 1: ln musbat → loss MANFIY"),
    ("z в (0,1]: случайно сработало", "z in (0,1]: worked by chance", "z (0,1] da: tasodifan ishladi"),
    ("z ≤ 0: логарифма нет → NaN, обучение ломается", "z ≤ 0: no logarithm → NaN, training breaks", "z ≤ 0: logarifm yo‘q → NaN, o‘qitish buziladi"),
    ("меньше нуля — так не бывает у расстояния между распределениями", "below zero: impossible for a distance between distributions",
     "noldan kichik — taqsimotlar orasidagi masofada bunday bo‘lmaydi"),
    ("ноль", "zero", "nol"),
    ("одного логарифма нет → весь лосс NaN", "one logarithm is missing → the whole loss is NaN", "bitta logarifm yo‘q → butun loss NaN"),
    ("ошибка", "error", "xato"),
    ("нет (ln не существует)", "none (ln does not exist)", "yo‘q (ln mavjud emas)"),
    ("нет", "none", "yo‘q"),
    # ---- лист «BCE»
    ("Binary cross-entropy — шаг за шагом", "Binary cross-entropy, step by step", "Binary cross-entropy — qadamma-qadam"),
    ("голубое — sigmoid (отдельный шаг, не часть BCE)", "light blue: sigmoid (a separate step, not part of BCE)", "havorang — sigmoid (alohida qadam, BCE qismi emas)"),
    ("красное — сама формула BCE, светлее = внутри рамки", "red: the BCE formula itself, lighter = inside the bracket", "qizil — BCE formulasining o‘zi, ochrog‘i = qavs ichida"),
    ("1. Расчёт: логит → sigmoid → BCE", "1. Computation: logit → sigmoid → BCE", "1. Hisob: logit → sigmoid → BCE"),
    ("шаг 2: sigmoid", "step 2: sigmoid", "2-qadam: sigmoid"),
    ("шаг 3: формула BCE, рамки изнутри наружу →", "step 3: the BCE formula, brackets from the inside out →", "3-qadam: BCE formulasi, qavslar ichkaridan tashqariga →"),
    ("y (1 = «да», 0 = «нет»)", "y (1 = “yes”, 0 = “no”)", "y (1 = «ha», 0 = «yo‘q»)"),
    ("[ сумма двух ]", "[ sum of the two ]", "[ ikkalasining yig‘indisi ]"),
    ("Σ по всем i", "Σ over all i", "barcha i bo‘yicha Σ"),
    ("проверка: среднее от −ln(p верного)", "check: mean of −ln(p of the right answer)", "tekshiruv: −ln(to‘g‘ri javob p) ning o‘rtachasi"),
    ("В каждой строке живо одно слагаемое: при y=1 остаётся ln(ŷ), при y=0 — ln(1−ŷ). То есть штраф всегда = −ln(вероятности, которую модель дала правильному ответу).",
     "In each row only one term is alive: for y=1, ln(ŷ) remains; for y=0, ln(1−ŷ). So the penalty is always −ln(the probability the model gave to the right answer).",
     "Har bir qatorda bitta qo‘shiluvchi tirik: y=1 da ln(ŷ), y=0 da — ln(1−ŷ) qoladi. Ya’ni jarima doim = −ln(model to‘g‘ri javobga bergan ehtimollik)."),
    ("Попробуйте: строка 1, логит 2.2 → 6 (ŷ→0.998, штраф→0). Строка 1, логит → −3 (ŷ→0.05 при y=1, штраф 3.0 — это одна строка «весит» больше четырёх остальных).",
     "Try it: row 1, logit 2.2 → 6 (ŷ→0.998, penalty→0). Row 1, logit → −3 (ŷ→0.05 with y=1, penalty 3.0: this one row “weighs” more than the other four).",
     "Sinab ko‘ring: 1-qator, logit 2,2 → 6 (ŷ→0,998, jarima→0). 1-qator, logit → −3 (y=1 da ŷ→0,05, jarima 3,0 — bu bitta qator qolgan to‘rttasidan «og‘irroq»)."),
    ("2. Что будет, если подать в BCE логиты напрямую (без sigmoid)", "2. What happens if logits go into BCE directly (without sigmoid)",
     "2. Logitlar BCE ga to‘g‘ridan-to‘g‘ri (sigmoid’siz) berilsa nima bo‘ladi"),
    ("ln(1−z) напрямую", "ln(1−z) directly", "ln(1−z) to‘g‘ridan-to‘g‘ri"),
    ("BCE без sigmoid", "BCE without sigmoid", "sigmoid’siz BCE"),
    ("BCE с sigmoid", "BCE with sigmoid", "sigmoid bilan BCE"),
    ("У BCE две ветви, и обе должны существовать. Логит 2.2 при y=1: ln(2.2) > 0 — уже штраф с обратным знаком, а заодно ln(1−2.2) = ln(−1.2) не существует. Множитель (1−y)=0 не спасает: в вычислениях 0·NaN = NaN.",
     "BCE has two branches, and both must exist. Logit 2.2 with y=1: ln(2.2) > 0 is already a penalty with the opposite sign, and ln(1−2.2) = ln(−1.2) does not exist. The factor (1−y)=0 does not help: in computation 0·NaN = NaN.",
     "BCE ning ikki tarmog‘i bor va ikkalasi ham mavjud bo‘lishi kerak. y=1 da logit 2,2: ln(2,2) > 0 — bu allaqachon teskari ishorali jarima, ustiga ln(1−2,2) = ln(−1,2) mavjud emas. (1−y)=0 ko‘paytuvchi qutqarmaydi: hisoblashda 0·NaN = NaN."),
    ("Достаточно одной такой строки в батче — и весь лосс NaN, градиенты NaN, веса сети после шага оптимизатора тоже NaN. Обучение не «плохое», оно мёртвое.",
     "One such row in a batch is enough: the whole loss is NaN, the gradients are NaN, and after the optimizer step the network weights are NaN too. Training is not “bad”, it is dead.",
     "Batchda bitta shunday qator yetarli — butun loss NaN, gradiyentlar NaN, optimizator qadamidan keyin tarmoq vaznlari ham NaN. O‘qitish «yomon» emas, u o‘lik."),
    ("Sigmoid решает обе проблемы сразу: ŷ ∈ (0,1) и 1−ŷ ∈ (0,1), оба логарифма всегда существуют и всегда ≤ 0.",
     "Sigmoid solves both problems at once: ŷ ∈ (0,1) and 1−ŷ ∈ (0,1), so both logarithms always exist and are always ≤ 0.",
     "Sigmoid ikkala muammoni birdan hal qiladi: ŷ ∈ (0,1) va 1−ŷ ∈ (0,1), ikkala logarifm doim mavjud va doim ≤ 0."),
    ("3. Почему так: обе ветви BCE работают только на отрезке (0, 1)", "3. Why: both branches of BCE work only on the interval (0, 1)",
     "3. Nega shunday: BCE ning ikkala tarmog‘i faqat (0, 1) oralig‘ida ishlaydi"),
    ("x — что подали", "x: what went in", "x — nima berildi"),
    ("штраф при y=1: −ln(x)", "penalty for y=1: −ln(x)", "y=1 dagi jarima: −ln(x)"),
    ("штраф при y=0: −ln(1−x)", "penalty for y=0: −ln(1−x)", "y=0 dagi jarima: −ln(1−x)"),
    ("при y=1 ln(x) не существует → NaN", "for y=1, ln(x) does not exist → NaN", "y=1 da ln(x) mavjud emas → NaN"),
    ("при y=1 ln(0) не существует → NaN", "for y=1, ln(0) does not exist → NaN", "y=1 da ln(0) mavjud emas → NaN"),
    ("y=1: почти 0 на «да» → огромный штраф;  y=0: почти идеально → ~0", "y=1: almost 0 on “yes” → a huge penalty;  y=0: almost perfect → ~0",
     "y=1: «ha» ga deyarli 0 → juda katta jarima;  y=0: deyarli ideal → ~0"),
    ("y=1: плохо;  y=0: хорошо", "y=1: bad;  y=0: good", "y=1: yomon;  y=0: yaxshi"),
    ("неуверенность: штраф 0.693 в обе стороны", "uncertainty: penalty 0.693 either way", "ishonchsizlik: ikkala tomonga jarima 0,693"),
    ("y=1: хорошо;  y=0: плохо", "y=1: good;  y=0: bad", "y=1: yaxshi;  y=0: yomon"),
    ("y=1: почти идеально;  y=0: почти 0 на «нет» → огромный штраф", "y=1: almost perfect;  y=0: almost 0 on “no” → a huge penalty",
     "y=1: deyarli ideal;  y=0: «yo‘q» ga deyarli 0 → juda katta jarima"),
    ("при y=0 ln(0) не существует → NaN", "for y=0, ln(0) does not exist → NaN", "y=0 da ln(0) mavjud emas → NaN"),
    ("y=1: лосс < 0, «лучше идеала»;  y=0: ln(−1) не существует", "y=1: loss < 0, “better than perfect”;  y=0: ln(−1) does not exist",
     "y=1: loss < 0, «idealdan ham yaxshi»;  y=0: ln(−1) mavjud emas"),
    ("y=1: лосс −2.3 и падает без дна", "y=1: loss −2.3 and falling with no floor", "y=1: loss −2,3 va tubsiz pasayadi"),
    ("Зелёное — зона вероятностей, куда sigmoid попадает всегда. Красное — зона логитов. У BCE две ветви и две «стены»: у нуля (для y=1) и у единицы (для y=0). Значения x можно менять.",
     "Green: the zone of probabilities, where sigmoid always lands. Red: the zone of logits. BCE has two branches and two “walls”: at zero (for y=1) and at one (for y=0). The x values can be changed.",
     "Yashil — ehtimolliklar zonasi, sigmoid doim shu yerga tushadi. Qizil — logitlar zonasi. BCE ning ikki tarmog‘i va ikki «devori» bor: nol yonida (y=1 uchun) va bir yonida (y=0 uchun). x qiymatlarini o‘zgartirish mumkin."),
    ("4. Как sigmoid сжимает любой логит в (0, 1)", "4. How sigmoid squeezes any logit into (0, 1)", "4. Sigmoid istalgan logitni (0, 1) ga qanday siqadi"),
    ("комментарий", "comment", "izoh"),
    ("почти 0 — уверенное «нет»", "almost 0: a confident “no”", "deyarli 0 — ishonchli «yo‘q»"),
    ("ровно 0.5 — полная неуверенность", "exactly 0.5: complete uncertainty", "aynan 0,5 — to‘liq ishonchsizlik"),
    ("почти 1 — уверенное «да»", "almost 1: a confident “yes”", "deyarli 1 — ishonchli «ha»"),
    ("Что бы ни подали — хоть −1000, хоть +1000 — ŷ остаётся строго между 0 и 1, и 1−ŷ тоже. Это и есть «+ sigmoid» на карточке: переводчик с языка логитов на язык вероятностей.",
     "Whatever goes in, −1000 or +1000, ŷ stays strictly between 0 and 1, and so does 1−ŷ. That is the “+ sigmoid” on the card: a translator from the language of logits to the language of probabilities.",
     "Nima berilmasin — −1000 mi, +1000 mi — ŷ qat’iy 0 va 1 orasida qoladi, 1−ŷ ham. Kartochkadagi «+ sigmoid» shu: logitlar tilidan ehtimolliklar tiliga tarjimon."),
    ("• BCE — это CE для двух классов, записанная через одно число ŷ: вероятность «да» = ŷ, вероятность «нет» = 1−ŷ.",
     "• BCE is CE for two classes written through a single number ŷ: the probability of “yes” = ŷ, the probability of “no” = 1−ŷ.",
     "• BCE — bu ikki sinf uchun CE, bitta ŷ soni orqali yozilgan: «ha» ehtimolligi = ŷ, «yo‘q» ehtimolligi = 1−ŷ."),
    ("• Формула знает только про ŷ ∈ (0,1). Логиты живут на всей прямой: напрямую они дают NaN или штраф с обратным знаком.",
     "• The formula knows only about ŷ ∈ (0,1). Logits live on the whole line: fed in directly, they give NaN or a penalty with the opposite sign.",
     "• Formula faqat ŷ ∈ (0,1) ni biladi. Logitlar butun to‘g‘ri chiziqda yashaydi: to‘g‘ridan-to‘g‘ri berilsa, NaN yoki teskari ishorali jarima beradi."),
    ("• Sigmoid сжимает любой логит в (0,1). Softmax для K=2 даёт ровно sigmoid — это одна и та же идея.",
     "• Sigmoid squeezes any logit into (0,1). Softmax for K=2 gives exactly a sigmoid: it is one and the same idea.",
     "• Sigmoid istalgan logitni (0,1) ga siqadi. K=2 uchun softmax aynan sigmoid beradi — bu bitta g‘oya."),
    ("• Усреднение на n — просто чтобы лосс не зависел от размера батча; саму форму штрафа задаёт −ln.",
     "• Averaging over n is only there so that the loss does not depend on the batch size; the shape of the penalty comes from −ln.",
     "• n ga o‘rtachalash — faqat loss batch o‘lchamiga bog‘liq bo‘lmasligi uchun; jarima shaklini −ln belgilaydi."),
    ("• В коде: nn.BCEWithLogitsLoss ждёт логиты (делает sigmoid сам и численно устойчивее), nn.BCELoss ждёт уже вероятности.",
     "• In code: nn.BCEWithLogitsLoss expects logits (applies sigmoid itself, and more stably), nn.BCELoss expects probabilities.",
     "• Kodda: nn.BCEWithLogitsLoss logitlarni kutadi (sigmoid’ni o‘zi bajaradi, sonli jihatdan barqarorroq), nn.BCELoss esa tayyor ehtimolliklarni kutadi."),
    ("один из ln не существует → 0·NaN = NaN, строка ломает батч", "one of the ln does not exist → 0·NaN = NaN, the row breaks the batch",
     "ln lardan biri mavjud emas → 0·NaN = NaN, qator batchni buzadi"),
    ("случайно попало в (0,1)", "landed in (0,1) by chance", "tasodifan (0,1) ga tushdi"),
    ("отрицательный лосс — бессмыслица", "a negative loss is nonsense", "manfiy loss — bema’nilik"),
    ("число есть, но это случайность: все z попали в (0,1)", "there is a number, but by chance: all z landed in (0,1)", "son bor, lekin bu tasodif: barcha z (0,1) ga tushgan"),
    ("хотя бы одна строка NaN → весь батч NaN, градиентов нет, веса портятся", "at least one row is NaN → the whole batch is NaN, no gradients, the weights are ruined",
     "kamida bitta qator NaN → butun batch NaN, gradiyentlar yo‘q, vaznlar buziladi"),
    # ---- графики
    ("Две ветви BCE: штраф в зависимости от ŷ", "Two branches of BCE: the penalty as a function of ŷ", "BCE ning ikki tarmog‘i: jarimaning ŷ ga bog‘liqligi"),
    ("ŷ — предсказанная вероятность «да»", "ŷ: the predicted probability of “yes”", "ŷ — «ha» ning bashorat qilingan ehtimolligi"),
    ("штраф", "penalty", "jarima"),
    ("−ln(x) на отрезке (0, 1]: штраф за вероятность правильного класса", "−ln(x) on (0, 1]: the penalty for the probability of the correct class",
     "(0, 1] oralig‘ida −ln(x): to‘g‘ri sinf ehtimolligi uchun jarima"),
    ("ŷ правильного класса", "ŷ of the correct class", "to‘g‘ri sinf ŷ"),
    ("лосс", "loss", "loss"),
]

# Цвета линий графиков (как в легенде тетради): y = 1 — красная ветвь, y = 0 — синяя
CHART_COLORS = {"chart1.xml": ["C0392B", "2E86C1"], "chart2.xml": ["C0392B"]}

_CYR = re.compile("[а-яА-ЯёЁ]")
_FIXED_TIME = (2026, 11, 2, 0, 0, 0)


def table(lang):
    if lang == "ru":
        return {}
    i = LANGS.index(lang)
    out = {}
    for row in T:
        assert len(row) == 3 and row[0] not in out, row[0]
        out[row[0]] = row[i]
    return out


def _sub_text(xml, pattern, tr, seen):
    """Перевести содержимое тегов, подходящих под pattern (группа 1 — открывающий тег, 2 — текст)."""
    def repl(m):
        raw = html.unescape(m.group(2))
        if raw in tr:
            seen.add(raw)
            return m.group(1) + html.escape(tr[raw], quote=False) + m.group(3)
        return m.group(0)
    return re.sub(pattern, repl, xml, flags=re.S)


def _formula(xml, tr, seen):
    """Строковые литералы внутри формул: "…" (в XML — &quot;…&quot;)."""
    def fix(m):
        body = m.group(2)
        def lit(q):
            raw = html.unescape(q.group(1))
            if raw in tr:
                seen.add(raw)
                return "&quot;" + html.escape(tr[raw], quote=False) + "&quot;"
            return q.group(0)
        return m.group(1) + re.sub(r"&quot;(.*?)&quot;", lit, body) + m.group(3)
    return re.sub(r"(<f[^>]*>)(.*?)(</f>)", fix, xml, flags=re.S)


def _chart_colors(xml, colors):
    """У каждой серии <c:ser> — свой цвет линии вместо белого и толщина 2,25 pt."""
    parts = xml.split("<c:ser>")
    for k in range(1, len(parts)):
        c = colors[(k - 1) % len(colors)]
        parts[k] = parts[k].replace('<a:ln cmpd="sng"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:ln>',
                                    f'<a:ln w="28575" cmpd="sng"><a:solidFill><a:srgbClr val="{c}"/></a:solidFill></a:ln>', 1)
    return "<c:ser>".join(parts)


def translate_xml(name, xml, lang, seen):
    tr = table(lang)
    if name.endswith("sharedStrings.xml"):
        xml = _sub_text(xml, r"(<t(?: [^>]*)?>)(.*?)(</t>)", tr, seen)
    elif "/worksheets/sheet" in name:
        xml = _formula(xml, tr, seen)
        # сохранённые результаты строковых формул — чтобы файл и до пересчёта показывал перевод
        xml = re.sub(r'(<c [^>]*t="str"[^>]*>.*?<v>)(.*?)(</v>)',
                     lambda m: m.group(1) + html.escape(tr.get(html.unescape(m.group(2)), html.unescape(m.group(2))), quote=False) + m.group(3), xml, flags=re.S)
    elif "/charts/chart" in name:
        xml = _sub_text(xml, r"(<a:t>)(.*?)(</a:t>)", tr, seen)
        xml = _chart_colors(xml, CHART_COLORS[name.rsplit("/", 1)[1]])
    elif name.endswith("workbook.xml") and lang != "ru":
        for ru, names in SHEETS.items():
            xml = xml.replace(f'name="{ru}"', f'name="{names[lang]}"')
    return xml


def build():
    """Собрать три файла; вернуть их пути. Проверяет, что в en/uz не осталось кириллицы."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    with zipfile.ZipFile(SOURCE) as src:
        items = [(i, src.read(i.filename)) for i in src.infolist()]
    for lang in LANGS:
        seen = set()
        out = OUT_DIR / NAME.format(lang=lang)
        tmp = out.with_suffix(".tmp")
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for info, data in items:
                name = info.filename
                if name.endswith(".xml"):
                    text = translate_xml(name, data.decode("utf-8"), lang, seen)
                    if lang != "ru" and _CYR.search(text):
                        left = sorted(set(re.findall(r">([^<]*[а-яА-ЯёЁ][^<]*)<", text)))[:5]
                        raise ValueError(f"{lang}: нет перевода в {name}: {left}")
                    data = text.encode("utf-8")
                zi = zipfile.ZipInfo(name, _FIXED_TIME)
                zi.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(zi, data)
        if lang != "ru":
            unused = [r[0] for r in T if r[0] not in seen]
            assert not unused, f"{lang}: лишние переводы {unused[:3]}"
        if out.exists() and out.read_bytes() == tmp.read_bytes():
            tmp.unlink()
        else:
            tmp.replace(out)
        paths.append(out)
    return paths


if __name__ == "__main__":
    for p in build():
        print(p.relative_to(ROOT), p.stat().st_size)
