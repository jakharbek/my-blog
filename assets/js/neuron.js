/* Widgets of the article "The formula of a single neuron". Built on FV (assets/js/viz.js).
   a = f(Σ wᵢxᵢ + b) = f(wᵀx + b) */
(function () {
  "use strict";
  if (typeof FV === "undefined" || !FV.widget) return;

  const L = {
    ru: {
      identity: "тождественная", step: "ступенька", sigmoid: "сигмоида", tanh: "tanh", relu: "ReLU",
      inputs: "входы", weights: "веса", sum: "сумма", act: "активация", out: "выход", bias: "смещение",
      anatomyAria: "Схема нейрона: входы, веса, сумматор, функция активации и выход",
      fOf: "Функция $f$",
      steps0: "Нажмите «Шаг» или «Пуск»: вклады будут складываться по одному.",
      stepProd: (i) => `Вклад входа ${i}:`, stepCum: "накопленная сумма", stepBias: "Добавляем смещение:", stepZ: "Взвешенная сумма готова:", stepA: "Активация — сигмоида:",
      other: "Другой пример", ours: "Наш пример", cum: "накопленная сумма",
      dotProj: "проекция $\\mathbf{x}$ на $\\mathbf{w}$", sumForm: "$w_1x_1+w_2x_2$ =", cosForm: "$\\lVert\\mathbf{w}\\rVert\\lVert\\mathbf{x}\\rVert\\cos\\theta$ =", angle: "$\\theta$ =",
      agree: "Угол меньше 90°: вход похож на шаблон весов, вклад положительный.", ortho: "Угол 90°: вход перпендикулярен весам, вклад нулевой.", against: "Угол больше 90°: вход направлен против весов, вклад отрицательный.",
      boundary: "граница $a=0{,}5$", dist: "расстояние", wLen: "$\\lVert\\mathbf{w}\\rVert$ =", b: "Смещение $b$", w1: "Вес $w_1$", w2: "Вес $w_2$", w: "Вес $w$",
      zAt: "$z(\\mathbf{x})$ =", aAt: "$a(\\mathbf{x})$ =", dAt: "$d(\\mathbf{x})$ =", origin: "$|b|/\\lVert\\mathbf{w}\\rVert$ =",
      mode: "Выход", x0: "порог $x_0=-b/w$ =", noBias: "без смещения", withBias: "$f(wx+b)$", a0: "$f(b)$ при $x=0$:", slope: "наклон в $x_0$:",
      zLbl: "Предактивация $z$", deriv: "Показать производную $f'(z)$",
      gate: "Вентиль", train: "Обучение перцептрона", solution: "Готовое решение", epoch: "эпоха", errors: "ошибок сейчас",
      converged: (n) => `Готово: все четыре точки верны после эпохи ${n}.`, noLine: (n) => `После ${n} эпох ошибки остаются: для XOR такой прямой не существует.`,
      noSolution: "Для XOR готового решения нет: одной прямой точки не разделить.", ok: "верно", bad: "ошибка",
      colIn: "входы $x$ (щёлкните)", colW: "веса $w$", colP: "произведения $w_ix_i$", kernel: "Шаблон", vertical: "вертикальная граница", horizontal: "горизонтальная граница", spot: "пятно",
      preset: "Фрагмент", pEdge: "граница", pUniform: "однородный", pH: "гориз. граница", pDot: "точка", pClear: "чёрный",
      fired: "нейрон сработал", silent: "нейрон молчит",
      exam1: "балл по математике", exam2: "балл по языку", target: "Функция", neurons: "Нейронов ReLU", parts: "Показать отдельные нейроны", params: "параметров:", maxErr: "макс. ошибка:", sumRelu: "сумма нейронов", oneRelu: "вклад одного нейрона",
      morph: "Вход → скрытый слой", morph0: "Входное пространство: никакая прямая не отделяет закрашенные точки от пустых. Бирюзовая прямая — граница нейрона OR, фиолетовая — NAND.", morph1: "Скрытое пространство $(h_1;\\ h_2)$: точки $(0;\\ 1)$ и $(1;\\ 0)$ слились в $(1;\\ 1)$, и теперь одна прямая AND их отделяет.", morphMid: "Скрытый слой переносит каждую точку в новые координаты $(h_1;\\ h_2)$.",
      netAria: "Трёхмерная модель нейросети 3–3–1: входы, скрытый слой, выход", netMode: "Проход", netFwd: "прямой", netBwd: "обратный", netNeuron: "Нейрон", netPlay: "Пустить сигнал",
      netSpin: "Вращать", netBias: "Смещения как вход «1»", netFull: "На весь экран", netExit: "Выйти", netTarget: "Верный ответ", netLoss: "Потери:", netParams: "параметров:",
      netIn: "входной слой", netHidden: "скрытый слой", netOut: "выходной слой", netOurs: "наш нейрон", netW1: "Скрытый слой: $W^{(1)}$ | $\\mathbf{b}^{(1)}$", netW2: "Выход: $\\mathbf{w}^{(2)\\top}$ | $b^{(2)}$",
      netInText: "Вход {i} — это не нейрон, а число из данных. Он ничего не считает, а раздаёт своё значение всем трём нейронам скрытого слоя.",
      netHidText: "Нейрон скрытого слоя считает ту же формулу $a = f(\\mathbf{w}^{\\top}\\mathbf{x} + b)$; его веса — одна строка матрицы $W^{(1)}$ на соседней панели.",
      netHidNext: "Его выход становится одним из входов выходного нейрона, с весом {w}.", netOutText: "Выходной нейрон — та же формула, но его входы — выходы скрытого слоя $h_1, h_2, h_3$.",
      netEnter: "Войти в нейрон", netLeave: "Выйти из нейрона", netCrumb: "Сеть", netCrumbAria: "Где вы находитесь", netClickIn: "щёлкните, чтобы войти внутрь",
      netHintNet: "Щёлкните по нейрону, чтобы войти внутрь · тяните — вращать, правой кнопкой — перемещать · Ctrl + колёсико — масштаб", netHintIn: "Щёлкните по входу или выходу, чтобы перейти в соседний нейрон · Esc — выйти", netHintFan: "Щёлкните по нейрону справа, чтобы войти в него · Esc — выйти",
      netEntered: "Вы внутри нейрона {n}", netLeft: "Вы вернулись к сети целиком",
      inFan: "Вход не вычисляет: он раздаёт одно и то же число всем нейронам слоя, каждый умножает его на свой вес", inFanBwd: "Ошибки трёх нейронов возвращаются ко входу и складываются: ∂L/∂x = Σ δⱼ·wⱼ",
      inMembrane: "нейрон", inAnswer: "ответ сети", inCol: "вход", inVal: "значение", inW: "вес $w$", inProd: "вклад $w\\cdot a$", inGrad: "$\\partial L/\\partial w = \\delta\\cdot a$", inTable: "Внутри {n}: входы, веса и вклады",
      fsHelpBtn: "Подсказка по управлению", fsZoomIn: "Приблизить", fsZoomOut: "Отдалить", fsFit: "Вписать", fsControls: "Управление", fsPanel: "Панель", fsBar: "Инструменты полноэкранного режима",
      fsHelp: "Колёсико — масштаб к курсору · левая кнопка — вращать · правая кнопка или Shift — перемещать · двойной щелчок — приблизить · щелчок по нейрону — войти · Backspace — выйти из нейрона · W A S D — сдвиг, 0 — сброс",
      fsHelpTouch: "Щипок — масштаб · два пальца — перемещать · один палец — вращать · касание нейрона — войти",
      netAct: "Функция активации", netActFor: "Активация нейрона {n}:", netActNone: "{n} — вход, у него нет активации", netActLayer: "для всего слоя", netActReset: "все — сигмоида",
      netActSet: "Активация {n}: {f}", netActAll: "Все нейроны снова с сигмоидой", netMse: "Выход не сигмоида: ответ уже не вероятность, поэтому потери — MSE ½(ŷ − y)², а δ = (ŷ − y)·f′(z).",
      netKeys: "Клавиши: стрелки — вращать; Shift + стрелки или W A S D — перемещать; + и − — масштаб; 0 — сброс; Enter — войти в выбранный нейрон; Esc или Backspace — выйти из нейрона.", fsZoomNow: "Масштаб {p}%: нажмите, чтобы вписать",
      eta: "Шаг обучения $\\eta$", loss: "BCE", acc: "точность", epochN: "шаг", class0: "класс 0", class1: "класс 1", lossTitle: "Потери по шагам",
    },
    en: {
      identity: "identity", step: "step", sigmoid: "sigmoid", tanh: "tanh", relu: "ReLU",
      inputs: "inputs", weights: "weights", sum: "sum", act: "activation", out: "output", bias: "bias",
      anatomyAria: "A neuron diagram: inputs, weights, summation, activation function and output",
      fOf: "Function $f$",
      steps0: "Press “Step” or “Play”: the contributions will be added one by one.",
      stepProd: (i) => `Contribution of input ${i}:`, stepCum: "running sum", stepBias: "Add the bias:", stepZ: "The weighted sum is ready:", stepA: "Activation — the sigmoid:",
      other: "Another example", ours: "Our example", cum: "running sum",
      dotProj: "projection of $\\mathbf{x}$ onto $\\mathbf{w}$", sumForm: "$w_1x_1+w_2x_2$ =", cosForm: "$\\lVert\\mathbf{w}\\rVert\\lVert\\mathbf{x}\\rVert\\cos\\theta$ =", angle: "$\\theta$ =",
      agree: "The angle is below 90°: the input resembles the weight template, the contribution is positive.", ortho: "The angle is 90°: the input is perpendicular to the weights, the contribution is zero.", against: "The angle is above 90°: the input points against the weights, the contribution is negative.",
      boundary: "boundary $a=0.5$", dist: "distance", wLen: "$\\lVert\\mathbf{w}\\rVert$ =", b: "Bias $b$", w1: "Weight $w_1$", w2: "Weight $w_2$", w: "Weight $w$",
      zAt: "$z(\\mathbf{x})$ =", aAt: "$a(\\mathbf{x})$ =", dAt: "$d(\\mathbf{x})$ =", origin: "$|b|/\\lVert\\mathbf{w}\\rVert$ =",
      mode: "Output", x0: "threshold $x_0=-b/w$ =", noBias: "without bias", withBias: "$f(wx+b)$", a0: "$f(b)$ at $x=0$:", slope: "slope at $x_0$:",
      zLbl: "Pre-activation $z$", deriv: "Show the derivative $f'(z)$",
      gate: "Gate", train: "Perceptron learning", solution: "Known solution", epoch: "epoch", errors: "errors now",
      converged: (n) => `Done: all four points are correct after epoch ${n}.`, noLine: (n) => `After ${n} epochs errors remain: no such line exists for XOR.`,
      noSolution: "There is no known solution for XOR: a single line cannot separate the points.", ok: "correct", bad: "error",
      colIn: "inputs $x$ (click)", colW: "weights $w$", colP: "products $w_ix_i$", kernel: "Template", vertical: "vertical edge", horizontal: "horizontal edge", spot: "spot",
      preset: "Patch", pEdge: "edge", pUniform: "uniform", pH: "horiz. edge", pDot: "dot", pClear: "black",
      fired: "the neuron fires", silent: "the neuron is silent",
      exam1: "maths score", exam2: "language score", target: "Function", neurons: "ReLU neurons", parts: "Show individual neurons", params: "parameters:", maxErr: "max error:", sumRelu: "sum of neurons", oneRelu: "one neuron's contribution",
      morph: "Input → hidden layer", morph0: "Input space: no line separates the filled points from the hollow ones. The teal line is the boundary of the OR neuron, the violet one of NAND.", morph1: "Hidden space $(h_1,\\ h_2)$: the points $(0,\\ 1)$ and $(1,\\ 0)$ have merged into $(1,\\ 1)$, and now a single AND line separates them.", morphMid: "The hidden layer moves every point to new coordinates $(h_1,\\ h_2)$.",
      netAria: "A 3D model of the 3–3–1 network: inputs, hidden layer, output", netMode: "Pass", netFwd: "forward", netBwd: "backward", netNeuron: "Neuron", netPlay: "Send a signal",
      netSpin: "Rotate", netBias: "Biases as input “1”", netFull: "Full screen", netExit: "Exit", netTarget: "Correct answer", netLoss: "Loss:", netParams: "parameters:",
      netIn: "input layer", netHidden: "hidden layer", netOut: "output layer", netOurs: "our neuron", netW1: "Hidden layer: $W^{(1)}$ | $\\mathbf{b}^{(1)}$", netW2: "Output: $\\mathbf{w}^{(2)\\top}$ | $b^{(2)}$",
      netInText: "Input {i} is not a neuron but a number from the data. It computes nothing; it hands its value to all three neurons of the hidden layer.",
      netHidText: "A hidden neuron computes the same formula $a = f(\\mathbf{w}^{\\top}\\mathbf{x} + b)$; its weights are one row of the matrix $W^{(1)}$ in the neighbouring panel.",
      netHidNext: "Its output becomes one of the inputs of the output neuron, with weight {w}.", netOutText: "The output neuron is the same formula, but its inputs are the outputs of the hidden layer $h_1, h_2, h_3$.",
      netEnter: "Enter the neuron", netLeave: "Leave the neuron", netCrumb: "Network", netCrumbAria: "Where you are", netClickIn: "click to go inside",
      netHintNet: "Click a neuron to go inside · drag to rotate, right-drag to pan · Ctrl + wheel to zoom", netHintIn: "Click an input or the output to move to the neighbouring neuron · Esc to leave", netHintFan: "Click a neuron on the right to enter it · Esc to leave",
      netEntered: "You are inside neuron {n}", netLeft: "You are back to the whole network",
      inFan: "An input computes nothing: it hands the same number to every neuron of the layer, and each multiplies it by its own weight", inFanBwd: "The errors of the three neurons come back to the input and add up: ∂L/∂x = Σ δⱼ·wⱼ",
      inMembrane: "neuron", inAnswer: "network answer", inCol: "input", inVal: "value", inW: "weight $w$", inProd: "contribution $w\\cdot a$", inGrad: "$\\partial L/\\partial w = \\delta\\cdot a$", inTable: "Inside {n}: inputs, weights and contributions",
      fsHelpBtn: "Controls help", fsZoomIn: "Zoom in", fsZoomOut: "Zoom out", fsFit: "Fit", fsControls: "Controls", fsPanel: "Panel", fsBar: "Full-screen tools",
      fsHelp: "Wheel — zoom to the cursor · left button — rotate · right button or Shift — pan · double click — zoom in · click a neuron — go inside · Backspace — leave the neuron · W A S D — pan, 0 — reset",
      fsHelpTouch: "Pinch — zoom · two fingers — pan · one finger — rotate · tap a neuron — go inside",
      netAct: "Activation function", netActFor: "Activation of neuron {n}:", netActNone: "{n} is an input, it has no activation", netActLayer: "for the whole layer", netActReset: "all sigmoid",
      netActSet: "Activation of {n}: {f}", netActAll: "All neurons use the sigmoid again", netMse: "The output is not a sigmoid: the answer is no longer a probability, so the loss is MSE ½(ŷ − y)² and δ = (ŷ − y)·f′(z).",
      netKeys: "Keys: arrows rotate; Shift + arrows or W A S D pan; + and − zoom; 0 resets; Enter enters the selected neuron; Esc or Backspace leaves the neuron.", fsZoomNow: "Zoom {p}%: press to fit",
      eta: "Learning rate $\\eta$", loss: "BCE", acc: "accuracy", epochN: "step", class0: "class 0", class1: "class 1", lossTitle: "Loss by step",
    },
    uz: {
      identity: "ayniy", step: "zina", sigmoid: "sigmoida", tanh: "tanh", relu: "ReLU",
      inputs: "kirishlar", weights: "vaznlar", sum: "yig‘indi", act: "aktivatsiya", out: "chiqish", bias: "siljish",
      anatomyAria: "Neyron sxemasi: kirishlar, vaznlar, yig‘uvchi, aktivatsiya funksiyasi va chiqish",
      fOf: "$f$ funksiya",
      steps0: "«Qadam» yoki «Boshlash»ni bosing: hissalar birma-bir qo‘shiladi.",
      stepProd: (i) => `${i}-kirishning hissasi:`, stepCum: "jamlangan yig‘indi", stepBias: "Siljishni qo‘shamiz:", stepZ: "Vaznli yig‘indi tayyor:", stepA: "Aktivatsiya — sigmoida:",
      other: "Boshqa misol", ours: "Bizning misol", cum: "jamlangan yig‘indi",
      dotProj: "$\\mathbf{x}$ ning $\\mathbf{w}$ ga proyeksiyasi", sumForm: "$w_1x_1+w_2x_2$ =", cosForm: "$\\lVert\\mathbf{w}\\rVert\\lVert\\mathbf{x}\\rVert\\cos\\theta$ =", angle: "$\\theta$ =",
      agree: "Burchak 90° dan kichik: kirish vaznlar shabloniga o‘xshaydi, hissa musbat.", ortho: "Burchak 90°: kirish vaznlarga perpendikulyar, hissa nolga teng.", against: "Burchak 90° dan katta: kirish vaznlarga qarshi yo‘nalgan, hissa manfiy.",
      boundary: "chegara $a=0{,}5$", dist: "masofa", wLen: "$\\lVert\\mathbf{w}\\rVert$ =", b: "Siljish $b$", w1: "Vazn $w_1$", w2: "Vazn $w_2$", w: "Vazn $w$",
      zAt: "$z(\\mathbf{x})$ =", aAt: "$a(\\mathbf{x})$ =", dAt: "$d(\\mathbf{x})$ =", origin: "$|b|/\\lVert\\mathbf{w}\\rVert$ =",
      mode: "Chiqish", x0: "chegara $x_0=-b/w$ =", noBias: "siljishsiz", withBias: "$f(wx+b)$", a0: "$x=0$ da $f(b)$:", slope: "$x_0$ dagi qiyalik:",
      zLbl: "Preaktivatsiya $z$", deriv: "$f'(z)$ hosilani ko‘rsatish",
      gate: "Ventil", train: "Perseptronni o‘qitish", solution: "Tayyor yechim", epoch: "epoxa", errors: "hozirgi xatolar",
      converged: (n) => `Tayyor: ${n}-epoxadan keyin to‘rtala nuqta ham to‘g‘ri.`, noLine: (n) => `${n} epoxadan keyin ham xatolar qolmoqda: XOR uchun bunday to‘g‘ri chiziq yo‘q.`,
      noSolution: "XOR uchun tayyor yechim yo‘q: nuqtalarni bitta to‘g‘ri chiziq bilan ajratib bo‘lmaydi.", ok: "to‘g‘ri", bad: "xato",
      colIn: "kirishlar $x$ (bosing)", colW: "vaznlar $w$", colP: "ko‘paytmalar $w_ix_i$", kernel: "Shablon", vertical: "vertikal chegara", horizontal: "gorizontal chegara", spot: "dog‘",
      preset: "Fragment", pEdge: "chegara", pUniform: "bir xil", pH: "gor. chegara", pDot: "nuqta", pClear: "qora",
      fired: "neyron ishga tushdi", silent: "neyron jim",
      exam1: "matematika bali", exam2: "til bali", target: "Funksiya", neurons: "ReLU neyronlari", parts: "Alohida neyronlarni ko‘rsatish", params: "parametrlar:", maxErr: "maks. xato:", sumRelu: "neyronlar yig‘indisi", oneRelu: "bitta neyron hissasi",
      morph: "Kirish → yashirin qatlam", morph0: "Kirish fazosi: hech bir to‘g‘ri chiziq bo‘yalgan nuqtalarni bo‘sh nuqtalardan ajratmaydi. Firuza chiziq — OR neyronining chegarasi, binafsha — NAND.", morph1: "Yashirin fazo $(h_1;\\ h_2)$: $(0;\\ 1)$ va $(1;\\ 0)$ nuqtalar $(1;\\ 1)$ ga birlashdi, endi ularni bitta AND chizig‘i ajratadi.", morphMid: "Yashirin qatlam har bir nuqtani yangi $(h_1;\\ h_2)$ koordinatalarga ko‘chiradi.",
      netAria: "3–3–1 tarmog‘ining uch o‘lchamli modeli: kirishlar, yashirin qatlam, chiqish", netMode: "O‘tish", netFwd: "to‘g‘ri", netBwd: "teskari", netNeuron: "Neyron", netPlay: "Signal yuborish",
      netSpin: "Aylantirish", netBias: "Siljishlar «1» kirish sifatida", netFull: "To‘liq ekran", netExit: "Chiqish", netTarget: "To‘g‘ri javob", netLoss: "Yo‘qotish:", netParams: "parametrlar:",
      netIn: "kirish qatlami", netHidden: "yashirin qatlam", netOut: "chiqish qatlami", netOurs: "bizning neyron", netW1: "Yashirin qatlam: $W^{(1)}$ | $\\mathbf{b}^{(1)}$", netW2: "Chiqish: $\\mathbf{w}^{(2)\\top}$ | $b^{(2)}$",
      netInText: "{i}-kirish neyron emas, ma’lumotlardagi son. U hech narsa hisoblamaydi, o‘z qiymatini yashirin qatlamning uchala neyroniga tarqatadi.",
      netHidText: "Yashirin qatlam neyroni xuddi shu $a = f(\\mathbf{w}^{\\top}\\mathbf{x} + b)$ formulani hisoblaydi; uning vaznlari — qo‘shni paneldagi $W^{(1)}$ matritsasining bitta satri.",
      netHidNext: "Uning chiqishi chiqish neyronining kirishlaridan biriga aylanadi, vazni {w}.", netOutText: "Chiqish neyroni — o‘sha formula, faqat uning kirishlari yashirin qatlam chiqishlari $h_1, h_2, h_3$.",
      netEnter: "Neyron ichiga kirish", netLeave: "Neyrondan chiqish", netCrumb: "Tarmoq", netCrumbAria: "Siz qayerdasiz", netClickIn: "ichiga kirish uchun bosing",
      netHintNet: "Ichiga kirish uchun neyronni bosing · aylantirish uchun torting, o‘ng tugma bilan — surish · Ctrl + g‘ildirak — masshtab", netHintIn: "Qo‘shni neyronga o‘tish uchun kirish yoki chiqishni bosing · Esc — chiqish", netHintFan: "Kirish uchun o‘ngdagi neyronni bosing · Esc — chiqish",
      netEntered: "Siz {n} neyronining ichidasiz", netLeft: "Siz butun tarmoqqa qaytdingiz",
      inFan: "Kirish hisoblamaydi: u bir xil sonni qatlamning barcha neyronlariga tarqatadi, har biri uni o‘z vazniga ko‘paytiradi", inFanBwd: "Uchta neyronning xatolari kirishga qaytib, qo‘shiladi: ∂L/∂x = Σ δⱼ·wⱼ",
      inMembrane: "neyron", inAnswer: "tarmoq javobi", inCol: "kirish", inVal: "qiymat", inW: "vazn $w$", inProd: "hissa $w\\cdot a$", inGrad: "$\\partial L/\\partial w = \\delta\\cdot a$", inTable: "{n} ichida: kirishlar, vaznlar va hissalar",
      fsHelpBtn: "Boshqaruv bo‘yicha yordam", fsZoomIn: "Yaqinlashtirish", fsZoomOut: "Uzoqlashtirish", fsFit: "Sig‘dirish", fsControls: "Boshqaruv", fsPanel: "Panel", fsBar: "To‘liq ekran asboblari",
      fsHelp: "G‘ildirak — kursorga masshtab · chap tugma — aylantirish · o‘ng tugma yoki Shift — surish · ikki marta bosish — yaqinlashtirish · neyronni bosish — ichiga kirish · Backspace — neyrondan chiqish · W A S D — surish, 0 — tiklash",
      fsHelpTouch: "Chimchilash — masshtab · ikki barmoq — surish · bitta barmoq — aylantirish · neyronga tegish — ichiga kirish",
      netAct: "Aktivatsiya funksiyasi", netActFor: "{n} neyronining aktivatsiyasi:", netActNone: "{n} — kirish, uning aktivatsiyasi yo‘q", netActLayer: "butun qatlam uchun", netActReset: "hammasi — sigmoida",
      netActSet: "{n} aktivatsiyasi: {f}", netActAll: "Barcha neyronlar yana sigmoida bilan", netMse: "Chiqish sigmoida emas: javob endi ehtimollik emas, shuning uchun yo‘qotish — MSE ½(ŷ − y)², δ = (ŷ − y)·f′(z).",
      netKeys: "Tugmalar: strelkalar — aylantirish; Shift + strelkalar yoki W A S D — surish; + va − — masshtab; 0 — tiklash; Enter — tanlangan neyronga kirish; Esc yoki Backspace — neyrondan chiqish.", fsZoomNow: "Masshtab {p}%: sig‘dirish uchun bosing",
      eta: "O‘qitish qadami $\\eta$", loss: "BCE", acc: "aniqlik", epochN: "qadam", class0: "0-sinf", class1: "1-sinf", lossTitle: "Qadamlar bo‘yicha yo‘qotish",
    },
  }[FV.lang] || {};

  // ---------- shared math ----------
  const sig = FV.sigmoid;
  const ACT = {
    identity: { f: (z) => z, d: () => 1, sym: "z", c: "violet" },
    step: { f: (z) => (z >= 0 ? 1 : 0), d: () => 0, sym: "H(z)", c: "red" },
    sigmoid: { f: sig, d: (z) => { const s = sig(z); return s * (1 - s); }, sym: "σ(z)", c: "blue" },
    tanh: { f: Math.tanh, d: (z) => 1 - Math.tanh(z) ** 2, sym: "tanh z", c: "teal" },
    relu: { f: (z) => Math.max(0, z), d: (z) => (z > 0 ? 1 : 0), sym: "ReLU(z)", c: "orange" },
  };
  const ACT_IDS = ["identity", "step", "sigmoid", "tanh", "relu"];
  const SEP = FV.lang === "en" ? ", " : "; ";
  const SUB = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"];
  const n4 = (v) => FV.num(Math.abs(v) < 1e-12 ? 0 : v, 4);
  // A number for TeX: decimal comma as {,} in ru/uz, a real minus, negatives in parentheses on demand.
  const tn = (v, paren) => {
    const s = n4(v).replace("−", "-").replace(",", "{,}");
    return paren && v < 0 ? `(${s})` : s;
  };
  const reduced = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const S = FV.svg;

  // Segment of the line a·x + b·y + c = 0 inside the box [x0,x1]×[y0,y1], or null.
  function clipLine(a, b, c, x0, x1, y0, y1) {
    const pts = [];
    if (Math.abs(b) > 1e-9) [x0, x1].forEach((x) => { const y = -(a * x + c) / b; if (y >= y0 - 1e-9 && y <= y1 + 1e-9) pts.push([x, y]); });
    if (Math.abs(a) > 1e-9) [y0, y1].forEach((y) => { const x = -(b * y + c) / a; if (x >= x0 - 1e-9 && x <= x1 + 1e-9) pts.push([x, y]); });
    if (pts.length < 2) return null;
    let best = null, bd = -1;
    for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
      const d = Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]);
      if (d > bd) { bd = d; best = [pts[i], pts[j]]; }
    }
    return bd > 1e-9 ? best : null;
  }
  // The part of the box where a·x + b·y + c ≥ 0 (Sutherland–Hodgman against one half-plane).
  function halfPlane(a, b, c, x0, x1, y0, y1) {
    const poly = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], out = [];
    const v = (p) => a * p[0] + b * p[1] + c;
    for (let i = 0; i < 4; i++) {
      const p = poly[i], q = poly[(i + 1) % 4], vp = v(p), vq = v(q);
      if (vp >= 0) out.push(p);
      if ((vp >= 0) !== (vq >= 0)) { const t = vp / (vp - vq); out.push([p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t]); }
    }
    return out;
  }
  const vec = (arr) => "(" + arr.map(n4).join(SEP) + ")";

  // ======================================================================
  // 1. Anatomy: the animated neuron diagram
  // ======================================================================
  FV.widget("neuron-anatomy", (el, cfg) => {
    const st = { x: (cfg.x || [2, -1, 3]).slice(), w: (cfg.w || [0.5, -1, 0.25]).slice(), b: cfg.b != null ? cfg.b : -0.75, f: cfg.f || "sigmoid" };
    const n = st.x.length;
    const w = FV.shell(el, {});
    const box = FV.h("div", { class: "nr-diagram" });
    w.stage.append(box);
    const svg = S("svg", { class: "fv-svg nr-svg", role: "img", "aria-label": L.anatomyAria });
    box.append(svg);
    const gEdges = S("g", {}, svg), gNodes = S("g", {}, svg), gPulse = S("g", { class: "nr-pulses" }, svg);

    // controls: inputs, weights, bias, activation, play
    const fmt2 = (v) => FV.fmt(v, 2);
    const xs = st.x.map((v, i) => FV.ui.slider({ label: `$x_${i + 1}$`, min: -3, max: 3, step: 0.25, value: v, fmt: fmt2, oninput: (u) => { st.x[i] = u; draw(); } }));
    const ws = st.w.map((v, i) => FV.ui.slider({ label: `$w_${i + 1}$`, min: -2, max: 2, step: 0.05, value: v, fmt: fmt2, oninput: (u) => { st.w[i] = u; draw(); } }));
    const bs = FV.ui.slider({ label: "$b$", min: -3, max: 3, step: 0.05, value: st.b, fmt: fmt2, oninput: (u) => { st.b = u; draw(); } });
    const grid = FV.h("div", { class: "nr-sliders" },
      FV.h("div", { class: "nr-sl-col" }, FV.h("span", { class: "nr-sl-h", text: L.inputs }), xs.map((s) => s.el)),
      FV.h("div", { class: "nr-sl-col" }, FV.h("span", { class: "nr-sl-h", text: L.weights }), ws.map((s) => s.el)),
      FV.h("div", { class: "nr-sl-col" }, FV.h("span", { class: "nr-sl-h", text: L.bias }), bs.el));
    const seg = FV.ui.seg({ label: L.fOf, value: st.f, options: ACT_IDS.map((k) => ({ value: k, label: L[k] })), onchange: (v) => { st.f = v; draw(); } });
    let running = false, visible = true, raf = 0, t0 = 0;
    const play = FV.ui.button({ label: "▶ " + FV.t("play"), primary: true, onclick: () => (running ? stop() : start()) });
    w.controls.append(grid, seg.el, play.el);
    const ro = FV.ui.readout(w.readout, [{ key: "z", label: "$z$ =", c: "blue" }, { key: "a", label: "$a=f(z)$ =", c: "orange" }]);

    let G = null; // geometry of the last layout
    const val = () => {
      const p = st.x.map((x, i) => st.w[i] * x);
      const z = p.reduce((s, v) => s + v, 0) + st.b;
      return { p, z, a: ACT[st.f].f(z) };
    };
    const cls = (v) => (Math.abs(v) < 1e-9 ? "faint" : v > 0 ? "blue" : "red");

    function layout() {
      const W = Math.max(300, Math.round(box.clientWidth || 640));
      const nar = W < 560;
      const H = nar ? 290 : 340;
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`); svg.setAttribute("width", W); svg.setAttribute("height", H);
      const rIn = nar ? 17 : 22, rS = nar ? 21 : 28;
      const xIn = nar ? 26 : 64, yTop = nar ? 52 : 60, yBot = H - (nar ? 34 : 46);
      const ins = st.x.map((_, i) => [xIn, n === 1 ? (yTop + yBot) / 2 : yTop + ((yBot - yTop) * i) / (n - 1)]);
      const cy = (yTop + yBot) / 2 + (nar ? 14 : 18);
      const sum = [W * (nar ? 0.5 : 0.5), cy];
      const bias = [sum[0], nar ? 22 : 26];
      const aw = nar ? 58 : 86, ah = nar ? 46 : 64;
      const act = [W * (nar ? 0.73 : 0.735), cy];
      const out = [W - (nar ? 24 : 52), cy];
      G = { W, H, nar, rIn, rS, ins, sum, bias, act, aw, ah, out };
    }
    const towards = (p, q, r) => { const d = Math.hypot(q[0] - p[0], q[1] - p[1]) || 1; return [p[0] + ((q[0] - p[0]) * r) / d, p[1] + ((q[1] - p[1]) * r) / d]; };
    const txt = (parent, x, y, s, c, anchor = "middle") => { const t = S("text", { x, y, "text-anchor": anchor, class: c }, parent); t.textContent = s; return t; };

    function draw() {
      if (!G) layout();
      const { W, nar, rIn, rS, ins, sum, bias, act, aw, ah, out } = G;
      const v = val();
      gEdges.textContent = ""; gNodes.textContent = "";
      // input → Σ edges
      ins.forEach((p, i) => {
        const a = towards(p, sum, rIn), b = towards(sum, p, rS);
        S("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: "nr-edge s-" + cls(v.p[i]), "stroke-width": 1.2 + 2.6 * Math.abs(st.w[i]) }, gEdges);
        const wl = [a[0] + (b[0] - a[0]) * 0.36, a[1] + (b[1] - a[1]) * 0.36];
        txt(gEdges, wl[0], wl[1] - 8, (nar ? "" : `w${SUB[i + 1]} = `) + n4(st.w[i]), "nr-t nr-w");
        const pl = [a[0] + (b[0] - a[0]) * 0.74, a[1] + (b[1] - a[1]) * 0.74];
        txt(gEdges, pl[0], pl[1] + (i === 0 ? -9 : i === n - 1 ? 17 : -9), (v.p[i] >= 0 ? "+" : "") + n4(v.p[i]), "nr-t nr-p t-" + cls(v.p[i]));
      });
      // bias edge
      { const a = towards(bias, sum, 11), b = towards(sum, bias, rS);
        S("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: "nr-edge s-" + cls(st.b), "stroke-width": 1.2 + 1.2 * Math.abs(st.b), "stroke-dasharray": "5 4" }, gEdges); }
      // Σ → f → a
      S("line", { x1: sum[0] + rS, y1: sum[1], x2: act[0] - aw / 2, y2: act[1], class: "nr-edge s-ink", "stroke-width": 1.6 }, gEdges);
      S("line", { x1: act[0] + aw / 2, y1: act[1], x2: out[0] - rIn, y2: out[1], class: "nr-edge s-ink", "stroke-width": 1.6 }, gEdges);
      txt(gEdges, (sum[0] + rS + act[0] - aw / 2) / 2, sum[1] - 9, "z = " + n4(v.z), "nr-t nr-z");
      txt(gEdges, (act[0] + aw / 2 + out[0] - rIn) / 2, out[1] - 9, nar ? "" : "a", "nr-t nr-w");

      // input nodes
      ins.forEach((p, i) => {
        S("circle", { cx: p[0], cy: p[1], r: rIn, class: "nr-node" }, gNodes);
        txt(gNodes, p[0], p[1] + 4.5, n4(st.x[i]), "nr-v");
        if (!nar) txt(gNodes, p[0] - rIn - 8, p[1] + 4.5, "x" + SUB[i + 1], "nr-t nr-lbl", "end");
        else txt(gNodes, p[0], p[1] - rIn - 5, "x" + SUB[i + 1], "nr-t nr-lbl");
      });
      // bias node
      S("circle", { cx: bias[0], cy: bias[1], r: 11, class: "nr-node nr-bias" }, gNodes);
      txt(gNodes, bias[0], bias[1] + 4, "b", "nr-v nr-small");
      txt(gNodes, bias[0] + 18, bias[1] + 4.5, "= " + n4(st.b), "nr-t", "start");
      // Σ node
      G.sumEl = S("circle", { cx: sum[0], cy: sum[1], r: rS, class: "nr-node nr-sum" }, gNodes);
      txt(gNodes, sum[0], sum[1] + (nar ? 6 : 8), "Σ", "nr-v nr-big");
      if (!nar) txt(gNodes, sum[0], sum[1] + rS + 18, L.sum, "nr-t nr-cap");
      // activation box with a small graph of f
      const bx = act[0] - aw / 2, by = act[1] - ah / 2;
      S("rect", { x: bx, y: by, width: aw, height: ah, rx: 6, class: "nr-node" }, gNodes);
      const F = ACT[st.f];
      const yr = st.f === "identity" ? [-3, 3] : st.f === "relu" ? [-0.6, 3] : st.f === "tanh" ? [-1.25, 1.25] : [-0.2, 1.2];
      const mx = (z) => bx + 6 + ((z + 3) / 6) * (aw - 12), my = (y) => by + ah - 6 - ((FV.clamp(y, yr[0], yr[1]) - yr[0]) / (yr[1] - yr[0])) * (ah - 12);
      let d = "";
      for (let k = 0; k <= 60; k++) { const z = -3 + (6 * k) / 60; d += (k ? "L" : "M") + mx(z).toFixed(1) + " " + my(F.f(z)).toFixed(1); }
      S("path", { d, class: "nr-fcurve s-" + F.c, fill: "none" }, gNodes);
      const zc = FV.clamp(v.z, -3, 3);
      S("circle", { cx: mx(zc), cy: my(F.f(zc)), r: 3.5, class: "fill-orange" }, gNodes);
      txt(gNodes, act[0], by - 8, "f = " + F.sym.replace("(z)", "").replace(" z", ""), "nr-t nr-lbl");
      if (!nar) txt(gNodes, act[0], by + ah + 18, L.act, "nr-t nr-cap");
      // output node
      S("circle", { cx: out[0], cy: out[1], r: rIn, class: "nr-node nr-out" }, gNodes);
      txt(gNodes, out[0], out[1] + 4.5, FV.num(v.a, nar ? 2 : 3), "nr-v");
      if (!nar) txt(gNodes, out[0], out[1] + rIn + 18, L.out, "nr-t nr-cap");

      ro.set("z", n4(v.z)); ro.set("a", n4(v.a));
      const terms = st.x.map((x, i) => `${tn(st.w[i], true)}\\cdot ${tn(x, true)}`).join(" + ");
      w.note.textContent = "";
      w.note.append(FV.tex(`z = ${terms} + ${tn(st.b, true)} = ${tn(v.z)},\\qquad a = ${F.sym.replace("σ", "\\sigma").replace("tanh z", "\\tanh z").replace("ReLU", "\\mathrm{ReLU}").replace("(z)", "(" + tn(v.z) + ")").replace(" z", " " + tn(v.z, true)).replace(/^z$/, tn(v.z, true))} \\approx ${tn(v.a)}`));
      if (!running) pulses(-1);
    }

    // pulses: one dot per input edge, then one along Σ → f, then f → a
    const dots = [];
    function pulses(t) {
      if (!G) return;
      const { ins, sum, act, aw, out, rIn, rS } = G;
      const v = val();
      const need = ins.length + 2;
      while (dots.length < need) dots.push(S("circle", { r: 4, class: "nr-dot" }, gPulse));
      if (t < 0) { dots.forEach((d) => d.setAttribute("opacity", 0)); G.sumEl && G.sumEl.setAttribute("r", rS); return; }
      const maxP = Math.max(0.5, ...v.p.map(Math.abs));
      ins.forEach((p, i) => {
        const d = dots[i], a = towards(p, sum, rIn), b = towards(sum, p, rS), u = FV.clamp(t / 0.42, 0, 1);
        const on = t < 0.44 && Math.abs(v.p[i]) > 1e-9;
        d.setAttribute("cx", a[0] + (b[0] - a[0]) * u); d.setAttribute("cy", a[1] + (b[1] - a[1]) * u);
        d.setAttribute("r", 3 + 4.5 * (Math.abs(v.p[i]) / maxP));
        d.setAttribute("class", "nr-dot fill-" + cls(v.p[i]));
        d.setAttribute("opacity", on ? 0.95 : 0);
      });
      const ds = dots[ins.length], da = dots[ins.length + 1];
      const u1 = FV.clamp((t - 0.5) / 0.2, 0, 1), u2 = FV.clamp((t - 0.74) / 0.2, 0, 1);
      ds.setAttribute("cx", sum[0] + rS + (act[0] - aw / 2 - sum[0] - rS) * u1); ds.setAttribute("cy", sum[1]);
      ds.setAttribute("r", 3 + Math.min(5, Math.abs(v.z) * 1.4)); ds.setAttribute("class", "nr-dot fill-" + cls(v.z));
      ds.setAttribute("opacity", t >= 0.5 && t < 0.71 ? 0.95 : 0);
      da.setAttribute("cx", act[0] + aw / 2 + (out[0] - rIn - act[0] - aw / 2) * u2); da.setAttribute("cy", out[1]);
      da.setAttribute("r", 3 + Math.min(5, Math.abs(v.a) * 3)); da.setAttribute("class", "nr-dot fill-orange");
      da.setAttribute("opacity", t >= 0.74 && t < 0.95 ? 0.95 : 0);
      // Σ swells when the input pulses arrive
      const k = t >= 0.4 && t < 0.56 ? Math.sin(((t - 0.4) / 0.16) * Math.PI) : 0;
      G.sumEl && G.sumEl.setAttribute("r", rS * (1 + 0.16 * k));
    }
    function frame(now) {
      raf = 0;
      if (!running || !visible) return;          // off screen the loop sleeps; the observer wakes it up
      pulses(((now - t0) % 2600) / 2600);
      raf = requestAnimationFrame(frame);
    }
    function start() { running = true; play.setLabel("❚❚ " + FV.t("pause")); t0 = performance.now(); if (!raf) raf = requestAnimationFrame(frame); }
    function stop() { running = false; play.setLabel("▶ " + FV.t("play")); pulses(-1); }

    if ("ResizeObserver" in window) {
      let last = 0;
      new ResizeObserver(() => { const x = box.clientWidth; if (Math.abs(x - last) > 1) { last = x; layout(); draw(); } }).observe(box);
    }
    if ("IntersectionObserver" in window) new IntersectionObserver((es) => es.forEach((e) => { visible = e.isIntersecting; if (visible && running && !raf) raf = requestAnimationFrame(frame); })).observe(el);
    layout(); draw();
    if (!reduced()) start();
  });

  // ======================================================================
  // 2. Steps: a waterfall of contributions, played step by step
  // ======================================================================
  FV.widget("neuron-steps", (el, cfg) => {
    const base = { x: (cfg.x || [2, -1, 3]).slice(), w: (cfg.w || [0.5, -1, 0.25]).slice(), b: cfg.b != null ? cfg.b : -0.75 };
    let ex = { x: base.x.slice(), w: base.w.slice(), b: base.b };
    const w = FV.shell(el, {});
    const ticks = () => ex.x.map((_, i) => ({ v: i, label: `w${SUB[i + 1]}x${SUB[i + 1]}` })).concat([{ v: ex.x.length, label: "b" }, { v: ex.x.length + 1, label: "z" }]);
    let p = null;
    const KMAX = () => ex.x.length + 3;
    let k = KMAX();
    const rng = FV.rng(11);
    function compute() {
      const prods = ex.x.map((x, i) => ex.w[i] * x);
      const items = prods.concat([ex.b]);
      const cum = [0];
      items.forEach((v) => cum.push(cum[cum.length - 1] + v));
      const z = cum[cum.length - 1];
      return { prods, items, cum, z, a: sig(z) };
    }
    function makePlot() {
      const c = compute();
      const lo = Math.min(0, ...c.cum), hi = Math.max(0, ...c.cum);
      const pad = Math.max(0.4, (hi - lo) * 0.18);
      if (p) { p.ro && p.ro.disconnect(); p.wrap.remove(); }
      p = new FV.Plot(w.stage, { x: [-0.6, ex.x.length + 1.6], y: [lo - pad, hi + pad], xTicks: ticks(), aspect: 0.48, minHeight: 240, maxHeight: 360, ariaLabel: L.cum });
      p.onresize = draw;
    }
    const player = FV.ui.player({ interval: 1100, onstep: () => { if (k >= KMAX()) k = 0; k++; draw(); return k < KMAX(); }, onreset: () => { k = 0; draw(); } });
    const other = FV.ui.button({ label: "↻ " + L.other, onclick: () => {
      player.stop();
      const q = () => Math.round((rng() * 6 - 3) * 4) / 4;
      ex = { x: ex.x.map(() => Math.round(rng() * 6 - 3)), w: ex.w.map(() => Math.round((rng() * 3 - 1.5) * 4) / 4), b: q() / 2 };
      k = 0; makePlot(); draw();
    } });
    const ours = FV.ui.button({ label: L.ours, onclick: () => { player.stop(); ex = { x: base.x.slice(), w: base.w.slice(), b: base.b }; k = 0; makePlot(); draw(); } });
    w.controls.append(player.el, other.el, ours.el);
    const ro = FV.ui.readout(w.readout, [{ key: "z", label: "$z$ =", c: "blue" }, { key: "a", label: "$a=\\sigma(z)$ ≈", c: "orange" }]);
    function draw() {
      const c = compute(), n = ex.x.length;
      p.clear();
      p.hline(0, { c: "guide", dash: false, w: 1 });
      const shown = Math.min(k, n + 1);
      for (let i = 0; i < shown; i++) {
        const v = c.items[i], a = c.cum[i], b = c.cum[i + 1];
        p.rect(i - 0.32, a, i + 0.32, b, { c: Math.abs(v) < 1e-9 ? "faint" : v > 0 ? "blue" : "red", opacity: i === k - 1 ? 0.95 : 0.6, rx: 2 });
        p.text(i, Math.max(a, b), (v >= 0 ? "+" : "") + n4(v), { anchor: "middle", dy: -7 });
        if (i < n + 1) p.line(i + 0.32, b, i + 1 - 0.32, b, { c: "faint", w: 1, dash: "3 3" });
      }
      if (k >= n + 2) {
        p.rect(n + 1 - 0.32, 0, n + 1 + 0.32, c.z, { c: "ink", opacity: 0.85, rx: 2 });
        p.text(n + 1, Math.max(0, c.z), "z = " + n4(c.z), { anchor: "middle", dy: -7, cls: "nr-strong" });
      }
      ro.set("z", k >= n + 2 ? n4(c.z) : "—");
      ro.set("a", k >= n + 3 ? n4(c.a) : "—");
      // the running formula
      const parts = [];
      for (let i = 0; i < shown; i++) parts.push(i < n ? `\\underbrace{${tn(ex.w[i], true)}\\cdot${tn(ex.x[i], true)}}_{${tn(c.prods[i])}}` : tn(ex.b, true));
      let line = parts.length ? parts.join(" + ") : "\\;";
      if (k >= n + 2) line = `z = ${line} = ${tn(c.z)}`;
      if (k >= n + 3) line += `,\\quad a = \\sigma(${tn(c.z)}) = \\frac{1}{1+e^{${tn(-c.z)}}} \\approx ${tn(Number(c.a.toFixed(4)))}`;
      let msg;
      if (k === 0) msg = L.steps0;
      else if (k <= n) msg = `${L.stepProd(k)} $w_${k}x_${k} = ${tn(ex.w[k - 1], true)}\\cdot${tn(ex.x[k - 1], true)} = ${tn(c.prods[k - 1])}$; ${L.stepCum} $= ${tn(c.cum[k])}$.`;
      else if (k === n + 1) msg = `${L.stepBias} $${tn(c.cum[n])} + ${tn(ex.b, true)} = ${tn(c.cum[n + 1])}$.`;
      else if (k === n + 2) msg = `${L.stepZ} $z = ${tn(c.z)}$.`;
      else msg = `${L.stepA} $a = \\sigma(${tn(c.z)}) \\approx ${tn(Number(c.a.toFixed(4)))}$.`;
      w.note.textContent = "";
      const eq = FV.tex(line, true); eq.classList.add("nr-eqline");
      w.note.append(eq, FV.rich(msg, "p"));
    }
    makePlot(); draw();
  });

  // ======================================================================
  // 3. The dot product in the plane: two draggable vectors and the projection
  // ======================================================================
  FV.widget("neuron-dot", (el, cfg) => {
    const w = FV.shell(el, {});
    const p = new FV.Plot(w.stage, { x: [-3.2, 3.2], y: [-1.8, 3.2], equal: true, xLabel: "x₁", yLabel: "x₂" });
    let wv = (cfg.w || [2, 1]).slice(), xv = (cfg.x || [1, 2]).slice();
    const snap = (v) => Math.round(v * 10) / 10;
    const hw = p.handle(wv[0], wv[1], { c: "blue", label: "w", onDrag: (a, b) => { const q = [snap(a), snap(b)]; if (Math.hypot(...q) < 0.3) return [wv[0], wv[1]]; wv = q; return q; }, onChange: () => draw() });
    const hx = p.handle(xv[0], xv[1], { c: "teal", label: "x", onDrag: (a, b) => { xv = [snap(a), snap(b)]; return xv; }, onChange: () => draw() });
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: L.sumForm, c: "blue" }, { key: "c", label: L.cosForm, c: "orange" }, { key: "t", label: L.angle }]);
    p.onresize = draw;
    function draw() {
      p.clear();
      const dot = wv[0] * xv[0] + wv[1] * xv[1], nw = Math.hypot(...wv), nx = Math.hypot(...xv);
      const u = [wv[0] / nw, wv[1] / nw], pr = dot / nw, foot = [u[0] * pr, u[1] * pr];
      p.line(-u[0] * 10, -u[1] * 10, u[0] * 10, u[1] * 10, { c: "guide", w: 1, dash: "2 4" });
      p.line(0, 0, foot[0], foot[1], { c: "orange", w: 5, opacity: 0.85 });
      p.line(xv[0], xv[1], foot[0], foot[1], { c: "faint", w: 1.2, dash: "4 4" });
      // right-angle mark at the foot
      if (nx > 0.2 && Math.abs(pr) > 0.15 && Math.abs(Math.abs(pr) - nx) > 0.05) {
        const s = 0.16, back = [-u[0] * Math.sign(pr) * s, -u[1] * Math.sign(pr) * s];
        const perp = [xv[0] - foot[0], xv[1] - foot[1]], pl = Math.hypot(...perp) || 1, pv = [(perp[0] / pl) * s, (perp[1] / pl) * s];
        p.path([[foot[0] + back[0], foot[1] + back[1]], [foot[0] + back[0] + pv[0], foot[1] + back[1] + pv[1]], [foot[0] + pv[0], foot[1] + pv[1]]], { c: "faint", w: 1 });
      }
      // angle arc
      if (nx > 0.2) {
        const a1 = Math.atan2(wv[1], wv[0]); let a2 = Math.atan2(xv[1], xv[0]);
        let da = a2 - a1; while (da > Math.PI) da -= 2 * Math.PI; while (da < -Math.PI) da += 2 * Math.PI;
        const r = 0.45, pts = [];
        for (let i = 0; i <= 30; i++) { const t = a1 + (da * i) / 30; pts.push([r * Math.cos(t), r * Math.sin(t)]); }
        p.path(pts, { c: "violet", w: 1.5 });
        const tm = a1 + da / 2; p.text(0.72 * Math.cos(tm), 0.72 * Math.sin(tm), "θ", { anchor: "middle", dy: 4, c: "violet" });
      }
      p.arrow(0, 0, wv[0], wv[1], { c: "blue", w: 2.5 });
      p.arrow(0, 0, xv[0], xv[1], { c: "teal", w: 2.5 });
      p.text(wv[0], wv[1], "w", { dx: 16, dy: -12, c: "blue", cls: "nr-strong" });
      p.text(xv[0], xv[1], "x", { dx: 16, dy: -12, c: "teal", cls: "nr-strong" });
      p.dot(0, 0, { r: 3, c: "ink" });
      const cos = nx > 1e-9 ? dot / (nw * nx) : 0, th = (Math.acos(FV.clamp(cos, -1, 1)) * 180) / Math.PI;
      ro.set("s", `${n4(wv[0])}·${n4(xv[0])} + ${n4(wv[1])}·${n4(xv[1])} = ${n4(dot)}`);
      ro.set("c", `${FV.num(nw, 3)}·${FV.num(nx, 3)}·${FV.num(cos, 3)} = ${n4(nw * nx * cos)}`);
      ro.set("t", FV.fmt(th, 1) + "°");
      w.note.textContent = "";
      w.note.append(FV.rich(Math.abs(dot) < 1e-9 ? L.ortho : dot > 0 ? L.agree : L.against));
      hw.set(wv[0], wv[1]); hx.set(xv[0], xv[1]);
    }
    draw();
  });

  // ======================================================================
  // 4. The decision boundary of a 2-input sigmoid neuron
  // ======================================================================
  FV.widget("neuron-plane", (el, cfg) => {
    const w = FV.shell(el, {});
    const D = 3;
    const p = new FV.Plot(w.stage, { x: [-D, D], y: [-D, D], equal: true, xLabel: "x₁", yLabel: "x₂", maxHeight: 560 });
    let wv = (cfg.w || [1.5, 1]).slice(), b = cfg.b != null ? cfg.b : -1, xv = (cfg.x || [1.5, 0.5]).slice();
    const snap = (v) => Math.round(v * 10) / 10;
    const hw = p.handle(wv[0], wv[1], { c: "blue", label: "w", onDrag: (a, c) => { const q = [snap(a), snap(c)]; if (Math.hypot(...q) < 0.2) return [wv[0], wv[1]]; wv = q; return q; }, onChange: () => draw() });
    const hx = p.handle(xv[0], xv[1], { c: "ink", label: "x", onDrag: (a, c) => { xv = [snap(a), snap(c)]; return xv; }, onChange: () => draw() });
    const bs = FV.ui.slider({ label: L.b, min: -4, max: 4, step: 0.1, value: b, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { b = v; draw(); } });
    w.controls.append(bs.el);
    const ro = FV.ui.readout(w.readout, [{ key: "w", label: "$\\mathbf{w}$ =", c: "blue" }, { key: "n", label: L.wLen }, { key: "o", label: L.origin }, { key: "z", label: L.zAt }, { key: "a", label: L.aAt, c: "orange" }, { key: "d", label: L.dAt }]);
    p.onresize = draw;
    function draw() {
      p.clear();
      p.heat((x1, x2) => sig(wv[0] * x1 + wv[1] * x2 + b), { cmap: "diverging", z: [0, 1], res: 4, alpha: 0.8 });
      const nw2 = wv[0] ** 2 + wv[1] ** 2, nw = Math.sqrt(nw2);
      [[-2, "4 5"], [2, "4 5"], [0, null]].forEach(([lev, dash]) => {
        const s = clipLine(wv[0], wv[1], b - lev, -D, D, -D, D);
        if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], { c: "ink", w: lev ? 1.2 : 2.4, dash, opacity: lev ? 0.65 : 1 });
      });
      // perpendicular from the origin to the boundary: length |b|/‖w‖
      const f0 = [(-b * wv[0]) / nw2, (-b * wv[1]) / nw2];
      p.arrow(0, 0, wv[0], wv[1], { c: "blue", w: 2.6 });
      p.line(0, 0, f0[0], f0[1], { c: "violet", w: 4.5, opacity: 0.9 });
      if (Math.hypot(...f0) > 0.35) p.text(f0[0] / 2, f0[1] / 2, "|b|/‖w‖", { dx: -8, dy: -8, anchor: "end", c: "violet", cls: "nr-strong" });
      p.text(wv[0], wv[1], "w", { dx: 16, dy: -12, c: "blue", cls: "nr-strong" });
      p.dot(0, 0, { r: 3, c: "ink" });
      // the point x and its distance to the boundary
      const z = wv[0] * xv[0] + wv[1] * xv[1] + b;
      const proj = [xv[0] - (z * wv[0]) / nw2, xv[1] - (z * wv[1]) / nw2];
      p.line(xv[0], xv[1], proj[0], proj[1], { c: "ink", w: 1.2, dash: "2 3" });
      p.text(xv[0], xv[1], "x", { dx: 16, dy: 20, cls: "nr-strong" });
      const seg = clipLine(wv[0], wv[1], b, -D, D, -D, D);
      if (seg) {
        const m = seg[0][1] > seg[1][1] ? seg[0] : seg[1];
        p.text(m[0], m[1], "a = " + (FV.lang === "en" ? "0.5" : "0,5"), { dx: m[0] > 0 ? -6 : 6, dy: 16, anchor: m[0] > 0 ? "end" : "start", cls: "nr-strong" });
      }
      ro.set("w", vec(wv)); ro.set("n", n4(nw)); ro.set("o", n4(Math.abs(b) / nw));
      ro.set("z", n4(z)); ro.set("a", n4(sig(z))); ro.set("d", n4(z / nw));
      hw.set(wv[0], wv[1]); hx.set(xv[0], xv[1]);
    }
    draw();
  });

  // ======================================================================
  // 5. The output surface over the input plane (3D)
  // ======================================================================
  FV.widget("neuron-surface", (el, cfg) => {
    const w = FV.shell(el, {});
    let wv = (cfg.w || [1.5, 1]).slice(), b = cfg.b != null ? cfg.b : -1, mode = cfg.mode || "sigmoid";
    const D = 3;
    const fOf = () => { const F = mode === "z" ? (z) => z : ACT[mode].f; return (x1, x2) => F(wv[0] * x1 + wv[1] * x2 + b); };
    const range = () => {
      const zs = [[-D, -D], [D, -D], [D, D], [-D, D]].map(([a, c]) => wv[0] * a + wv[1] * c + b);
      const lo = Math.min(...zs), hi = Math.max(...zs);
      if (mode === "sigmoid") return [0, 1];
      if (mode === "relu") return [0, Math.max(1, hi)];
      return [Math.min(-1, lo), Math.max(1, hi)];
    };
    const zLab = () => (mode === "z" ? "z" : mode === "sigmoid" ? "σ(z)" : "ReLU(z)");
    const sf = new FV.Surface(w.stage, { f: fOf(), x: [-D, D], y: [-D, D], z: range(), n: 34, labels: { x: "x₁", y: "x₂", z: zLab() }, cmap: "viridis", azimuth: -0.9, elevation: 0.72 });
    const seg = FV.ui.seg({ label: L.mode, value: mode, options: [{ value: "z", label: "$z$" }, { value: "sigmoid", label: "$\\sigma(z)$" }, { value: "relu", label: "$\\mathrm{ReLU}(z)$" }], onchange: (v) => { mode = v; update(); } });
    const s1 = FV.ui.slider({ label: L.w1, min: -3, max: 3, step: 0.1, value: wv[0], fmt: (v) => FV.fmt(v, 1), oninput: (v) => { wv[0] = v; update(); } });
    const s2 = FV.ui.slider({ label: L.w2, min: -3, max: 3, step: 0.1, value: wv[1], fmt: (v) => FV.fmt(v, 1), oninput: (v) => { wv[1] = v; update(); } });
    const s3 = FV.ui.slider({ label: L.b, min: -4, max: 4, step: 0.1, value: b, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { b = v; update(); } });
    w.controls.append(seg.el, s1.el, s2.el, s3.el);
    let raf = 0;
    function update() {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0;
        sf.o.labels.z = zLab();
        sf.paths = [];
        sf.setF(fOf(), range());
        const s = clipLine(wv[0], wv[1], b, -D, D, -D, D);
        const h = mode === "sigmoid" ? 0.5 : 0;
        if (s) sf.setPaths([{ pts: FV.linspace(0, 1, 24).map((t) => [s[0][0] + (s[1][0] - s[0][0]) * t, s[0][1] + (s[1][1] - s[0][1]) * t, h]), c: "orange", w: 4 }]);
        else sf.setPaths([]);
      });
    }
    update();
  });

  // ======================================================================
  // 6. One input: the weight sets the slope, the bias moves the threshold
  // ======================================================================
  FV.widget("neuron-bias", (el, cfg) => {
    const w = FV.shell(el, {});
    let wt = cfg.w != null ? cfg.w : 2, b = cfg.b != null ? cfg.b : -2, f = cfg.f || "sigmoid";
    const fs = cfg.fs || ["sigmoid", "step", "relu", "identity"];
    const YR = { sigmoid: [-0.15, 1.15], step: [-0.15, 1.15], tanh: [-1.2, 1.2], relu: [-0.6, 6], identity: [-6, 6] };
    const p = new FV.Plot(w.stage, { x: [-5, 5], y: YR[f], xLabel: "x", yLabel: "a", aspect: 0.5 });
    const seg = FV.ui.seg({ label: L.fOf, value: f, options: fs.map((k) => ({ value: k, label: L[k] })), onchange: (v) => { f = v; p.setDomain(null, YR[f]); draw(); } });
    const sw = FV.ui.slider({ label: L.w, min: -4, max: 4, step: 0.1, value: wt, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { wt = v; draw(); } });
    const sb = FV.ui.slider({ label: L.b, min: -6, max: 6, step: 0.1, value: b, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { b = v; draw(); } });
    w.controls.append(seg.el, sw.el, sb.el);
    const ro = FV.ui.readout(w.readout, [{ key: "x0", label: L.x0, c: "violet" }, { key: "a0", label: L.a0 }, { key: "k", label: L.slope }]);
    p.onresize = draw;
    function draw() {
      const F = ACT[f].f;
      p.clear();
      if (f === "sigmoid" || f === "step") p.hline(0.5, {});
      p.fn((x) => F(wt * x), { c: "faint", w: 1.6, dash: "6 5", jump: f === "step" ? 0.5 : null });
      const x0 = Math.abs(wt) > 1e-9 ? -b / wt : NaN;
      if (Number.isFinite(x0) && x0 > -5 && x0 < 5) {
        p.vline(x0, { c: "violet", dash: "5 4", w: 1.4 });
        p.text(x0, YR[f][1], "x₀", { dx: 6, dy: 16, c: "violet", cls: "nr-strong" });
      }
      p.fn((x) => F(wt * x + b), { c: "blue", w: 2.6, jump: f === "step" ? 0.5 : null });
      if (Number.isFinite(x0) && x0 > -5 && x0 < 5) p.dot(x0, F(0), { c: "violet", r: 5 });
      (cfg.marks || []).forEach((m) => {
        const y = F(wt * m + b);
        p.dot(m, y, { c: "orange", r: 4.5 });
        p.text(m, y, n4(y), { dx: 8, dy: 16, anchor: "start", c: "orange", cls: "nr-strong" });
      });
      p.legend([{ label: L.withBias, c: "blue" }, { label: L.noBias, c: "faint", dash: true }]);
      ro.set("x0", Number.isFinite(x0) ? n4(x0) : "—");
      ro.set("a0", n4(F(b)));
      const k = f === "sigmoid" ? wt / 4 : f === "tanh" ? wt : f === "identity" ? wt : f === "relu" ? NaN : NaN;
      ro.set("k", Number.isFinite(k) && Number.isFinite(x0) ? n4(k) : "—");
    }
    draw();
  });

  // ======================================================================
  // 7. Five activations at the same z
  // ======================================================================
  FV.widget("neuron-activations", (el, cfg) => {
    const w = FV.shell(el, {});
    let z = cfg.z != null ? cfg.z : 2, f = cfg.f || "sigmoid", der = false;
    const p = new FV.Plot(w.stage, { x: [-5, 5], y: [-1.5, 3.2], xLabel: "z", yLabel: "f(z)", aspect: 0.55 });
    const seg = FV.ui.seg({ label: L.fOf, value: f, options: ACT_IDS.map((k) => ({ value: k, label: L[k] })), onchange: (v) => { f = v; draw(); } });
    const sz = FV.ui.slider({ label: L.zLbl, min: -5, max: 5, step: 0.05, value: z, fmt: (v) => FV.fmt(v, 2), oninput: (v) => { z = v; draw(); } });
    const ck = FV.ui.check({ label: L.deriv, checked: false, onchange: (v) => { der = v; draw(); } });
    w.controls.append(seg.el, sz.el, ck.el);
    const ro = FV.ui.readout(w.readout, ACT_IDS.map((k) => ({ key: k, label: L[k] + ":", c: ACT[k].c })).concat([{ key: "d", label: "$f'(z)$:" }]));
    p.onresize = draw;
    function draw() {
      p.clear();
      ACT_IDS.forEach((k) => { if (k !== f) p.fn(ACT[k].f, { c: ACT[k].c, w: 1.2, opacity: 0.35, jump: k === "step" ? 0.5 : null }); });
      p.vline(z, {});
      const A = ACT[f];
      if (der) p.fn(A.d, { c: A.c, w: 1.8, dash: "6 4", jump: 0.5 });
      p.fn(A.f, { c: A.c, w: 3, jump: f === "step" ? 0.5 : null });
      p.dot(z, A.f(z), { c: A.c, r: 6 });
      if (der) p.dot(z, A.d(z), { c: A.c, r: 4, hollow: true });
      p.text(z, Math.min(3.0, A.f(z)), "a = " + n4(A.f(z)), { dx: z > 2.5 ? -10 : 10, dy: -10, anchor: z > 2.5 ? "end" : "start", c: A.c, cls: "nr-strong" });
      ACT_IDS.forEach((k) => ro.set(k, n4(ACT[k].f(z))));
      ro.set("d", n4(A.d(z)));
    }
    draw();
  });

  // ======================================================================
  // 8. Logic gates and the perceptron learning rule
  // ======================================================================
  FV.widget("neuron-logic", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const c1 = FV.col(w.stage), c2 = FV.col(w.stage);
    const PTS = [[0, 0], [0, 1], [1, 0], [1, 1]];
    const T = { and: [0, 0, 0, 1], or: [0, 1, 1, 1], nand: [1, 1, 1, 0], xor: [0, 1, 1, 0] };
    const SOL = { and: [1, 1, -1.5], or: [1, 1, -0.5], nand: [-1, -1, 1.5] };
    const START = [-0.4, 0.6, 0.2], ETA = 0.5, MAXE = 30;
    let gate = cfg.gate || "and", th = START.slice(), it = 0, errs = 0, cur = -1, done = "";
    const p = new FV.Plot(c1, { x: [-0.6, 1.6], y: [-0.6, 1.6], equal: true, xLabel: "x₁", yLabel: "x₂", xTicks: [0, 1], yTicks: [0, 1], maxHeight: 420 });
    const seg = FV.ui.seg({ label: L.gate, value: gate, options: ["and", "or", "nand", "xor"].map((g) => ({ value: g, label: g.toUpperCase() })), onchange: (v) => { gate = v; reset(); } });
    const sl = ["w1", "w2", "b"].map((k, i) => FV.ui.slider({ label: i < 2 ? `$w_${i + 1}$` : "$b$", min: -3, max: 3, step: 0.1, value: th[i], fmt: (v) => FV.fmt(v, 2), oninput: (v) => { player.stop(); th[i] = v; done = ""; draw(); } }));
    const player = FV.ui.player({ interval: 420, onstep: () => stepRule(), onreset: () => reset() });
    const sol = FV.ui.button({ label: L.solution, onclick: () => { player.stop(); if (SOL[gate]) { th = SOL[gate].slice(); done = ""; } else done = L.noSolution; cur = -1; sync(); draw(); } });
    w.controls.append(seg.el, ...sl.map((s) => s.el), FV.h("div", { class: "nr-row" }, FV.h("span", { class: "nr-sl-h", text: L.train }), player.el, sol.el));
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.epoch + ":" }, { key: "r", label: L.errors + ":", c: "red" }]);
    p.onresize = draw;
    const H = (z) => (z >= 0 ? 1 : 0);
    const zOf = (q) => th[0] * q[0] + th[1] * q[1] + th[2];
    function sync() { sl.forEach((s, i) => s.set(th[i])); }
    function reset() { player.stop(); th = START.slice(); it = 0; errs = 0; cur = -1; done = ""; sync(); draw(); }
    function stepRule() {
      if (done) return false;
      const i = it % 4, q = PTS[i], y = T[gate][i], e = y - H(zOf(q));
      if (e) { th[0] += ETA * e * q[0]; th[1] += ETA * e * q[1]; th[2] += ETA * e; errs++; }
      th = th.map((v) => Math.round(v * 1000) / 1000);
      cur = i; it++;
      if (it % 4 === 0) {
        const ep = it / 4;
        if (errs === 0) done = L.converged(ep);
        else if (ep >= MAXE) done = L.noLine(ep);
        if (!done) errs = 0;
      }
      sync(); draw();
      return !done;
    }
    function draw() {
      p.clear();
      const poly = halfPlane(th[0], th[1], th[2], -0.6, 1.6, -0.6, 1.6);
      if (poly.length > 2) p.path(poly, { fill: true, close: true, c: "teal", fillOpacity: 0.14 });
      const s = clipLine(th[0], th[1], th[2], -0.6, 1.6, -0.6, 1.6);
      if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], { c: "ink", w: 2.2 });
      let wrong = 0;
      const rows = [];
      PTS.forEach((q, i) => {
        const z = zOf(q), yh = H(z), y = T[gate][i], ok = yh === y;
        if (!ok) wrong++;
        if (i === cur) p.dot(q[0], q[1], { r: 17, c: "orange", hollow: true });
        if (!ok) p.dot(q[0], q[1], { r: 13, c: "red", hollow: true });
        p.dot(q[0], q[1], { r: 8, c: y ? "teal" : "ink", hollow: !y });
        p.text(q[0], q[1], y ? "1" : "0", { dx: 14, dy: -12, cls: "nr-strong" });
        rows.push(`<tr${i === cur ? ' class="cur"' : ""}><td class=num>${q[0]}</td><td class=num>${q[1]}</td><td class=num>${n4(z)}</td><td class=num>${yh}</td><td class=num>${y}</td><td class="${ok ? "ok" : "bad"}">${ok ? "✓" : "✗"}</td></tr>`);
      });
      ro.set("e", it ? String(Math.ceil(it / 4)) : "—");
      ro.set("r", String(wrong));
      c2.innerHTML = `<div class="table-wrap"><table class="data nr-tt"><thead><tr><th class=num>x₁</th><th class=num>x₂</th><th class=num>z</th><th class=num>ŷ</th><th class=num>y</th><th></th></tr></thead><tbody>${rows.join("")}</tbody></table></div>`;
      if (done) c2.append(FV.h("p", { class: "nr-done", text: done }));
    }
    draw();
  });

  // ======================================================================
  // 9. A 3×3 patch: nine inputs, a weight template, ReLU
  // ======================================================================
  FV.widget("neuron-pixels", (el, cfg) => {
    const w = FV.shell(el, {});
    const K = {
      vertical: { w: [-1, 0, 1, -1, 0, 1, -1, 0, 1], b: -1 },
      horizontal: { w: [-1, -1, -1, 0, 0, 0, 1, 1, 1], b: -1 },
      spot: { w: [-1, -1, -1, -1, 8, -1, -1, -1, -1], b: -1 },
    };
    const P = {
      edge: [0, 1, 1, 0, 1, 1, 0, 1, 1], uniform: [1, 1, 1, 1, 1, 1, 1, 1, 1], h: [0, 0, 0, 1, 1, 1, 1, 1, 1], dot: [0, 0, 0, 0, 1, 0, 0, 0, 0], clear: [0, 0, 0, 0, 0, 0, 0, 0, 0],
    };
    let kern = cfg.kernel || "vertical", x = P.edge.slice();
    const mk = (cls) => FV.h("div", { class: "nr-grid " + cls });
    const gIn = mk("in"), gW = mk("w"), gP = mk("p");
    const cellsIn = x.map((_, i) => { const b = FV.h("button", { type: "button", class: "nr-cell", onclick: () => { x[i] = x[i] === 0 ? 0.5 : x[i] === 0.5 ? 1 : 0; draw(); } }); gIn.append(b); return b; });
    const cellsW = x.map(() => { const c = FV.h("span", { class: "nr-cell" }); gW.append(c); return c; });
    const cellsP = x.map(() => { const c = FV.h("span", { class: "nr-cell" }); gP.append(c); return c; });
    const col = (lab, g) => FV.h("div", { class: "nr-gcol" }, FV.rich(lab, "span"), g);
    const out = FV.h("div", { class: "nr-px-out" });
    w.stage.append(FV.h("div", { class: "nr-px" }, col(L.colIn, gIn), FV.h("span", { class: "nr-op", text: "×" }), col(L.colW, gW), FV.h("span", { class: "nr-op", text: "=" }), col(L.colP, gP)), out);
    const sk = FV.ui.seg({ label: L.kernel, value: kern, options: ["vertical", "horizontal", "spot"].map((k) => ({ value: k, label: L[k] })), onchange: (v) => { kern = v; draw(); } });
    const sp = FV.h("div", { class: "fv-seg" }, FV.h("span", { text: L.preset }), FV.h("div", { class: "fv-seg-btns" },
      [["edge", L.pEdge], ["uniform", L.pUniform], ["h", L.pH], ["dot", L.pDot], ["clear", L.pClear]].map(([k, lab]) => FV.h("button", { type: "button", onclick: () => { x = P[k].slice(); draw(); } }, lab))));
    w.controls.append(sk.el, sp);
    const ro = FV.ui.readout(w.readout, [{ key: "s", label: "$\\sum w_ix_i$ =" }, { key: "b", label: "$b$ =" }, { key: "z", label: "$z$ =", c: "blue" }, { key: "a", label: "$a=\\mathrm{ReLU}(z)$ =", c: "orange" }]);
    const shade = (t) => FV.rgb(FV.cmap("diverging", t));
    // white or near-black digits, whichever is more readable on the cell's colour (WCAG relative luminance)
    const ink = (t) => { const c = FV.cmap("diverging", t).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
      const Lc = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; return 1.05 / (Lc + 0.05) > (Lc + 0.05) / 0.0595 ? "#FFFFFF" : "#171A20"; };
    function draw() {
      const k = K[kern], m = Math.max(...k.w.map(Math.abs));
      let s = 0;
      x.forEach((v, i) => {
        const g = Math.round(255 * v);
        cellsIn[i].style.background = `rgb(${g},${g},${g})`;
        cellsIn[i].style.color = v > 0.5 ? "#171A20" : "#EDEDED";
        cellsIn[i].textContent = FV.num(v, 2);
        cellsIn[i].setAttribute("aria-label", `x${SUB[i + 1]} = ${FV.num(v, 2)}`);
        cellsW[i].style.background = shade(0.5 - k.w[i] / (2 * m));
        cellsW[i].style.color = ink(0.5 - k.w[i] / (2 * m));
        cellsW[i].textContent = n4(k.w[i]);
        const pr = k.w[i] * v; s += pr;
        cellsP[i].style.background = shade(0.5 - pr / (2 * m));
        cellsP[i].style.color = ink(0.5 - pr / (2 * m));
        cellsP[i].textContent = pr === 0 ? "0" : n4(pr);
      });
      const z = s + k.b, a = Math.max(0, z);
      ro.set("s", n4(s)); ro.set("b", n4(k.b)); ro.set("z", n4(z)); ro.set("a", n4(a));
      out.textContent = "";
      const bar = FV.h("span", { class: "nr-meter" }, FV.h("i", { style: `width:${Math.min(100, (a / (kern === "spot" ? 8 : 3)) * 100)}%` }));
      out.append(FV.tex(`z = ${tn(s)} + ${tn(k.b, true)} = ${tn(z)},\\quad a = \\max(0,\\ ${tn(z)}) = ${tn(a)}`), bar, FV.h("b", { class: a > 0 ? "on" : "", text: a > 0 ? L.fired : L.silent }));
    }
    draw();
  });

  // ======================================================================
  // 10. Training a neuron by gradient descent on two classes
  // ======================================================================
  FV.widget("neuron-train", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const c1 = FV.col(w.stage), c2 = FV.col(w.stage);
    const rng = FV.rng(cfg.seed || 7);
    const data = [];
    for (let i = 0; i < 40; i++) data.push({ x: [-1.1 + 0.95 * rng.normal(), -0.8 + 0.95 * rng.normal()], y: 0 });
    for (let i = 0; i < 40; i++) data.push({ x: [1.1 + 0.95 * rng.normal(), 0.9 + 0.95 * rng.normal()], y: 1 });
    const INIT = [-1, 0.6, 1.5], MAX = 200;
    let th = INIT.slice(), eta = cfg.eta || 0.5, hist = [], ep = 0;
    const D = 4;
    const p = new FV.Plot(c1, { x: [-D, D], y: [-D, D], equal: true, xLabel: "x₁", yLabel: "x₂", maxHeight: 460 });
    const lossOf = () => {
      let L0 = 0, acc = 0;
      data.forEach((d) => {
        const z = th[0] * d.x[0] + th[1] * d.x[1] + th[2];
        L0 += Math.max(z, 0) - z * d.y + Math.log1p(Math.exp(-Math.abs(z)));   // stable BCE with logits
        if ((z >= 0 ? 1 : 0) === d.y) acc++;
      });
      return [L0 / data.length, acc / data.length];
    };
    hist.push(lossOf()[0]);
    const lp = new FV.Plot(c2, { x: [0, MAX], y: [0, Math.ceil(hist[0] * 1.15 * 10) / 10], xLabel: L.epochN, yLabel: L.loss, aspect: 0.62, title: L.lossTitle });
    const se = FV.ui.slider({ label: L.eta, min: 0.05, max: 3, step: 0.05, value: eta, fmt: (v) => FV.fmt(v, 2), oninput: (v) => { eta = v; } });
    const player = FV.ui.player({ interval: 60, onstep: () => step(), onreset: () => { th = INIT.slice(); ep = 0; hist = [lossOf()[0]]; draw(); } });
    w.controls.append(player.el, se.el);
    const ro = FV.ui.readout(w.readout, [{ key: "e", label: L.epochN + ":" }, { key: "w", label: "$\\mathbf{w}$ =", c: "blue" }, { key: "b", label: "$b$ =" }, { key: "l", label: L.loss + ":", c: "orange" }, { key: "a", label: L.acc + ":" }]);
    p.onresize = draw; lp.onresize = draw;
    function step() {
      if (ep >= MAX) return false;
      let g0 = 0, g1 = 0, gb = 0;
      data.forEach((d) => {
        const a = sig(th[0] * d.x[0] + th[1] * d.x[1] + th[2]), dl = a - d.y;   // δ = a − y
        g0 += dl * d.x[0]; g1 += dl * d.x[1]; gb += dl;
      });
      const m = data.length;
      th = [th[0] - (eta * g0) / m, th[1] - (eta * g1) / m, th[2] - (eta * gb) / m];
      ep++; hist.push(lossOf()[0]);
      draw();
      return ep < MAX;
    }
    function draw() {
      p.clear();
      p.heat((a, c) => sig(th[0] * a + th[1] * c + th[2]), { cmap: "diverging", z: [0, 1], res: 5, alpha: 0.5 });
      [[-2, "4 5"], [2, "4 5"], [0, null]].forEach(([lev, dash]) => {
        const s = clipLine(th[0], th[1], th[2] - lev, -D, D, -D, D);
        if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], { c: "ink", w: lev ? 1 : 2.4, dash, opacity: lev ? 0.6 : 1 });
      });
      data.forEach((d) => p.dot(d.x[0], d.x[1], { r: 5, c: d.y ? "red" : "blue" }));
      p.legend([{ label: L.class0, c: "blue", dot: true }, { label: L.class1, c: "red", dot: true }]);
      lp.clear();
      lp.path(hist.map((v, i) => [i, v]), { c: "orange", w: 2.2 });
      lp.dot(ep, hist[hist.length - 1], { c: "orange", r: 4 });
      const [loss, acc] = lossOf();
      ro.set("e", String(ep)); ro.set("w", vec(th.slice(0, 2).map((v) => Math.round(v * 100) / 100)));
      ro.set("b", FV.fmt(th[2], 2)); ro.set("l", FV.fmt(loss, 3)); ro.set("a", Math.round(acc * 100) + "%");
    }
    draw();
  });
  // ======================================================================
  // 11. Labelled points on a plane with its own axes (examples section)
  // ======================================================================
  FV.widget("neuron-points", (el, cfg) => {
    const w = FV.shell(el, { cols: true });
    const c1 = FV.col(w.stage), c2 = FV.col(w.stage);
    const R = cfg.range || [0, 10];
    let wv = (cfg.w || [1, 0.5]).slice(), b = cfg.b != null ? cfg.b : -9;
    const pts = cfg.pts || [];
    const ax = cfg.axes === "exam" ? [L.exam1, L.exam2] : ["x₁", "x₂"];
    const p = new FV.Plot(c1, { x: R, y: R, equal: true, xLabel: ax[0], yLabel: ax[1], maxHeight: 460 });
    const br = cfg.bRange || [-15, 5];
    const s1 = FV.ui.slider({ label: L.w1, min: -2, max: 2, step: 0.05, value: wv[0], fmt: (v) => FV.fmt(v, 2), oninput: (v) => { wv[0] = v; draw(); } });
    const s2 = FV.ui.slider({ label: L.w2, min: -2, max: 2, step: 0.05, value: wv[1], fmt: (v) => FV.fmt(v, 2), oninput: (v) => { wv[1] = v; draw(); } });
    const s3 = FV.ui.slider({ label: L.b, min: br[0], max: br[1], step: 0.1, value: b, fmt: (v) => FV.fmt(v, 1), oninput: (v) => { b = v; draw(); } });
    const rs = FV.ui.button({ label: "↺ " + FV.t("restart"), onclick: () => { wv = cfg.w.slice(); b = cfg.b; s1.set(wv[0]); s2.set(wv[1]); s3.set(b); draw(); } });
    w.controls.append(s1.el, s2.el, s3.el, rs.el);
    p.onresize = draw;
    function draw() {
      p.clear();
      const nw2 = wv[0] ** 2 + wv[1] ** 2, nw = Math.sqrt(nw2) || 1;
      p.heat((x1, x2) => sig(wv[0] * x1 + wv[1] * x2 + b), { cmap: "diverging", z: [0, 1], res: 4, alpha: 0.6 });
      [[-2, "4 5"], [2, "4 5"], [0, null]].forEach(([lev, dash]) => {
        const s = clipLine(wv[0], wv[1], b - lev, R[0], R[1], R[0], R[1]);
        if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], { c: "ink", w: lev ? 1.1 : 2.4, dash, opacity: lev ? 0.6 : 1 });
      });
      // the normal w, drawn from the boundary point nearest to the centre
      const cx = (R[0] + R[1]) / 2, zc = wv[0] * cx + wv[1] * cx + b;
      const f = [cx - (zc * wv[0]) / nw2, cx - (zc * wv[1]) / nw2], k = (0.14 * (R[1] - R[0])) / nw;
      if (nw2 > 1e-9 && f[0] > R[0] && f[0] < R[1] && f[1] > R[0] && f[1] < R[1]) {
        p.arrow(f[0], f[1], f[0] + wv[0] * k, f[1] + wv[1] * k, { c: "blue", w: 2.4 });
        p.text(f[0] + wv[0] * k, f[1] + wv[1] * k, "w", { dx: 8, dy: -6, c: "blue", cls: "nr-strong" });
      }
      const rows = pts.map((q) => {
        const z = wv[0] * q.x[0] + wv[1] * q.x[1] + b, a = sig(z);
        p.dot(q.x[0], q.x[1], { r: 6, c: a >= 0.5 ? "red" : "blue" });
        p.text(q.x[0], q.x[1], q.l, { dx: 10, dy: -10, cls: "nr-strong" });
        return `<tr><td>${q.l}</td><td class=num>${vec(q.x)}</td><td class=num>${n4(z)}</td><td class=num>${n4(a)}</td><td class=num>${n4(z / nw)}</td></tr>`;
      });
      c2.innerHTML = `<div class="table-wrap"><table class="data nr-tt"><thead><tr><th></th><th class=num>x</th><th class=num>z</th><th class=num>a</th><th class=num>d</th></tr></thead><tbody>${rows.join("")}</tbody></table></div>`;
      const cf = (v) => (Math.abs(Math.abs(v) - 1) < 1e-9 ? "" : tn(Math.abs(v)));
      c2.append(FV.rich(`$z = ${wv[0] < 0 ? "-" : ""}${cf(wv[0])}x_1 ${wv[1] < 0 ? "-" : "+"} ${cf(wv[1])}x_2 ${b < 0 ? "-" : "+"} ${tn(Math.abs(b))}$`, "p"));
    }
    draw();
  });

  // ======================================================================
  // 12. A sum of ReLU neurons builds a broken line (universal approximation)
  // ======================================================================
  FV.widget("neuron-relu-sum", (el, cfg) => {
    const w = FV.shell(el, {});
    const G = { sq: { f: (x) => x * x, y: [-0.6, 4.4], tex: "x^2" }, sin: { f: (x) => Math.sin((Math.PI * x) / 2), y: [-1.4, 1.4], tex: "\\sin\\frac{\\pi x}{2}" } };
    let tg = cfg.target || "sq", K = cfg.k || 4, parts = true;
    const X0 = -2, X1 = 2;
    const p = new FV.Plot(w.stage, { x: [X0, X1], y: G[tg].y, xLabel: "x", yLabel: "y", aspect: 0.55 });
    const seg = FV.ui.seg({ label: L.target, value: tg, options: [{ value: "sq", label: "$x^2$" }, { value: "sin", label: "$\\sin\\frac{\\pi x}{2}$" }], onchange: (v) => { tg = v; p.setDomain(null, G[tg].y); draw(); } });
    const sk = FV.ui.slider({ label: L.neurons, min: 1, max: 16, step: 1, value: K, fmt: (v) => String(v), oninput: (v) => { K = v; draw(); } });
    const ck = FV.ui.check({ label: L.parts, checked: true, onchange: (v) => { parts = v; draw(); } });
    w.controls.append(seg.el, sk.el, ck.el);
    const ro = FV.ui.readout(w.readout, [{ key: "n", label: L.neurons + ":" }, { key: "p", label: L.params }, { key: "e", label: L.maxErr, c: "red" }]);
    p.onresize = draw;
    function build() {
      const g = G[tg].f, xs = FV.linspace(X0, X1, K + 1), sl = [];
      for (let k = 0; k < K; k++) sl.push((g(xs[k + 1]) - g(xs[k])) / (xs[k + 1] - xs[k]));
      // y(x) = g(x₀) + Σ cₖ·ReLU(x − xₖ),  cₖ = sₖ − sₖ₋₁ (s₋₁ = 0): each term is one neuron with w = 1, b = −xₖ
      const c = sl.map((s, k) => s - (k ? sl[k - 1] : 0));
      const y = (x) => g(xs[0]) + c.reduce((acc, ck, k) => acc + ck * Math.max(0, x - xs[k]), 0);
      return { xs, c, y, g };
    }
    function draw() {
      const m = build();
      p.clear();
      p.fn(m.g, { c: "faint", w: 5, opacity: 0.35 });
      if (parts) m.c.forEach((ck, k) => p.fn((x) => ck * Math.max(0, x - m.xs[k]), { c: ck >= 0 ? "blue" : "red", w: 1.2, opacity: 0.55 }));
      p.fn(m.y, { c: "orange", w: 2.6 });
      m.xs.slice(0, -1).forEach((x) => p.dot(x, m.y(x), { r: 3.5, c: "orange" }));
      p.legend([{ label: "$y=" + G[tg].tex + "$", c: "faint" }, { label: L.sumRelu, c: "orange" }].concat(parts ? [{ label: L.oneRelu, c: "blue" }] : []));
      let e = 0;
      FV.linspace(X0, X1, 801).forEach((x) => { e = Math.max(e, Math.abs(m.y(x) - m.g(x))); });
      ro.set("n", String(K)); ro.set("p", String(3 * K + 1)); ro.set("e", FV.num(e, 3));
    }
    draw();
  });

  // ======================================================================
  // 13. XOR: the hidden layer moves the points into a separable position
  // ======================================================================
  FV.widget("neuron-xor-morph", (el, cfg) => {
    const w = FV.shell(el, {});
    const P = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]];
    const H = (z) => (z >= 0 ? 1 : 0);
    const hid = (q) => [H(q[0] + q[1] - 0.5), H(-q[0] - q[1] + 1.5)];
    let t = 0, dir = 1, timer = 0;
    const p = new FV.Plot(w.stage, { x: [-0.45, 1.45], y: [-0.45, 1.45], equal: true, xLabel: "x₁ → h₁", yLabel: "x₂ → h₂", xTicks: [0, 1], yTicks: [0, 1], maxHeight: 420 });
    const st = FV.ui.slider({ label: L.morph, min: 0, max: 1, step: 0.01, value: 0, fmt: (v) => FV.fmt(v, 2), oninput: (v) => { stop(); t = v; draw(); }, wide: true });
    const play = FV.ui.button({ label: "▶ " + FV.t("play"), primary: true, onclick: () => (timer ? stop() : start()) });
    w.controls.append(st.el, play.el);
    let seen = true;
    if ("IntersectionObserver" in window) new IntersectionObserver((es) => es.forEach((e) => { seen = e.isIntersecting; })).observe(el);
    function start() { play.setLabel("❚❚ " + FV.t("pause")); timer = setInterval(() => { if (!seen) return; t += dir * 0.02; if (t >= 1 || t <= 0) { t = FV.clamp(t, 0, 1); dir = -dir; } st.set(t); draw(); }, 40); }
    function stop() { clearInterval(timer); timer = 0; play.setLabel("▶ " + FV.t("play")); }
    p.onresize = draw;
    function draw() {
      p.clear();
      const ln = (a, b, c, o) => { const s = clipLine(a, b, c, -0.45, 1.45, -0.45, 1.45); if (s) p.line(s[0][0], s[0][1], s[1][0], s[1][1], o); };
      if (t < 1) { ln(1, 1, -0.5, { c: "teal", w: 2, opacity: 1 - t }); ln(-1, -1, 1.5, { c: "violet", w: 2, opacity: 1 - t }); }
      if (t > 0) ln(1, 1, -1.5, { c: "ink", w: 2.4, opacity: t });
      const seen = {};
      P.forEach((q) => {
        const h = hid(q), x = q[0] + (h[0] - q[0]) * t, y = q[1] + (h[1] - q[1]) * t;
        p.dot(x, y, { r: 8, c: q[2] ? "teal" : "ink", hollow: !q[2] });
        const key = Math.round(x * 20) + ":" + Math.round(y * 20), k = (seen[key] = (seen[key] || 0) + 1);
        p.text(x, y, `(${q[0]}${SEP.trim()} ${q[1]})`, { dx: 12, dy: k > 1 ? 14 : -10 });
      });
      p.legend(t < 0.5 ? [{ label: "OR: $x_1+x_2-0{,}5=0$".replace("0{,}5", FV.lang === "en" ? "0.5" : "0{,}5"), c: "teal" }, { label: "NAND: $-x_1-x_2+1{,}5=0$".replace("1{,}5", FV.lang === "en" ? "1.5" : "1{,}5"), c: "violet" }]
        : [{ label: "AND: $h_1+h_2-1{,}5=0$".replace("1{,}5", FV.lang === "en" ? "1.5" : "1{,}5"), c: "ink" }]);
      w.note.textContent = "";
      w.note.append(FV.rich(t < 0.02 ? L.morph0 : t > 0.98 ? L.morph1 : L.morphMid));
    }
    draw();
  });

  // ======================================================================
  // 14. The neuron inside a tiny network 3–3–1, in 3D: forward and backward pass,
  //     and a flight inside any neuron to see its parts (inputs, weights, Σ, b, f, output)
  // ======================================================================
  FV.widget("neuron-network3d", (el, cfg) => {
    const w = FV.shell(el, {});
    w.root.classList.add("nr-net");
    // ----- the network: our neuron is h₁
    let X = (cfg.x || [2, -1, 3]).slice(), target = cfg.y != null ? cfg.y : 1;
    const W1 = cfg.W1 || [[0.5, -1, 0.25], [-1, 0.5, 1], [0.3, 0.8, -0.5]], B1 = cfg.b1 || [-0.75, 0.5, 0.2];
    const W2 = cfg.w2 || [1.5, -1, 2], B2 = cfg.b2 != null ? cfg.b2 : -0.5;
    // standard activations with their derivatives; every neuron can have its own
    const NACT = {
      sigmoid: { f: sig, d: (z) => { const s = sig(z); return s * (1 - s); }, tex: "\\sigma", name: "σ", label: L.sigmoid + " σ" },
      tanh: { f: Math.tanh, d: (z) => 1 - Math.tanh(z) ** 2, tex: "\\tanh", name: "tanh", label: "tanh" },
      relu: { f: (z) => Math.max(0, z), d: (z) => (z > 0 ? 1 : 0), tex: "\\mathrm{ReLU}", name: "ReLU", label: "ReLU" },
      leaky: { f: (z) => (z > 0 ? z : 0.1 * z), d: (z) => (z > 0 ? 1 : 0.1), tex: "\\mathrm{LReLU}", name: "LReLU", label: "Leaky ReLU (α = " + FV.fmt(0.1, 1) + ")" },
      elu: { f: (z) => (z > 0 ? z : Math.expm1(z)), d: (z) => (z > 0 ? 1 : Math.exp(z)), tex: "\\mathrm{ELU}", name: "ELU", label: "ELU (α = 1)" },
      gelu: { f: (z) => z * FV.Phi(z), d: (z) => FV.Phi(z) + z * FV.phi(z), tex: "\\mathrm{GELU}", name: "GELU", label: "GELU" },
      silu: { f: (z) => z * sig(z), d: (z) => { const s = sig(z); return s * (1 + z * (1 - s)); }, tex: "\\mathrm{SiLU}", name: "SiLU", label: "SiLU / Swish" },
      softplus: { f: (z) => Math.max(z, 0) + Math.log1p(Math.exp(-Math.abs(z))), d: sig, tex: "\\mathrm{softplus}", name: "softplus", label: "Softplus" },
      identity: { f: (z) => z, d: () => 1, tex: "\\mathrm{id}", name: "id", label: L.identity + " (id)" },
      step: { f: (z) => (z >= 0 ? 1 : 0), d: () => 0, tex: "H", name: "H", label: L.step + " H" },
    };
    const ACT_ORDER = ["sigmoid", "tanh", "relu", "leaky", "elu", "gelu", "silu", "softplus", "identity", "step"];
    const acts = Object.assign({ h0: "sigmoid", h1: "sigmoid", h2: "sigmoid", y: "sigmoid" }, cfg.acts || {});
    const Af = (id) => NACT[acts[id]] || NACT.sigmoid;
    function run() {
      const z1 = W1.map((row, j) => row.reduce((s, v, i) => s + v * X[i], 0) + B1[j]), h = z1.map((z, j) => Af("h" + j).f(z));
      const AY = Af("y"), z2 = W2.reduce((s, v, j) => s + v * h[j], 0) + B2, y = AY.f(z2);
      // with a sigmoid output the loss is BCE and δ = ŷ − y; any other output cannot be a probability, so MSE
      const bce = acts.y === "sigmoid";
      const loss = bce ? -Math.log(Math.max(1e-12, target ? y : 1 - y)) : 0.5 * (y - target) ** 2;
      const d2 = bce ? y - target : (y - target) * AY.d(z2), d1 = h.map((a, j) => Af("h" + j).d(z1[j]) * W2[j] * d2);
      const dx = X.map((_, i) => W1.reduce((s, row, j) => s + row[i] * d1[j], 0));
      return { z1, h, z2, y, loss, d2, d1, dx, bce };
    }
    // ----- scene of the network: layers along x, the neurons of a layer on a ring in the y–z plane
    const ring = (x, k, R, ph) => { const t = ph + (2 * Math.PI * k) / 3; return [x, R * Math.sin(t) - 0.12, R * Math.cos(t)]; };
    const N = [];
    for (let i = 0; i < 3; i++) N.push({ id: "x" + i, layer: 0, i, name: "x" + SUB[i + 1], pos: ring(-1.75, i, 0.95, Math.PI / 2) });
    for (let j = 0; j < 3; j++) N.push({ id: "h" + j, layer: 1, i: j, name: "h" + SUB[j + 1], pos: ring(0, j, 1.1, Math.PI / 6) });
    N.push({ id: "y", layer: 2, i: 0, name: "ŷ", pos: [1.75, -0.12, 0] });
    const BN = [{ id: "b1", layer: 0.5, name: "1", pos: [-0.9, -1.45, 0], bias: true }, { id: "b2", layer: 1.5, name: "1", pos: [0.9, -1.45, 0], bias: true }];
    const byId = {}; N.concat(BN).forEach((n) => (byId[n.id] = n));
    const E = [];
    for (let j = 0; j < 3; j++) for (let i = 0; i < 3; i++) E.push({ a: "x" + i, b: "h" + j, w: () => W1[j][i], stage: 0 });
    for (let j = 0; j < 3; j++) E.push({ a: "h" + j, b: "y", w: () => W2[j], stage: 1 });
    for (let j = 0; j < 3; j++) E.push({ a: "b1", b: "h" + j, w: () => B1[j], stage: 0, bias: true });
    E.push({ a: "b2", b: "y", w: () => B2, stage: 1, bias: true });
    const nameOf = (id) => byId[id].name + (id === "h0" ? " · " + L.netOurs : "") + (byId[id].layer > 0 && acts[id] !== "sigmoid" ? " · " + Af(id).name : "");

    // ----- state
    let sel = cfg.select || "h0", mode = "fwd", showBias = false, spin = !reduced(), playing = false;
    let az = -0.62, elv = 0.22, t = -1, t0 = 0, raf = 0, visible = true, lastSpin = 0, panelKey = "";
    let focus = 0, inside = null, anim = null;     // focus: 0 = the whole network, 1 = inside the neuron `inside`
    let hot = [];                                  // clickable / hoverable spots of the current frame
    // free camera: zoom `uz` follows `uzT` smoothly towards the cursor; pan in pixels; rotation keeps some inertia
    let uz = 1, uzT = 1, zAnchor = null, panX = 0, panY = 0, vAz = 0, vEl = 0, camTw = null, isFs = false;

    // ----- DOM
    const keysId = "nrk" + Math.random().toString(36).slice(2, 8);
    const keysDesc = FV.h("p", { class: "nr-sr", id: keysId, text: L.netKeys });
    const cv = FV.h("canvas", { class: "nr-net-canvas", role: "img", "aria-label": L.netAria, "aria-describedby": keysId, tabindex: 0 });
    const tip = FV.h("div", { class: "nr-net-tip", hidden: true });
    const crumbCur = FV.h("span", { class: "nr-crumb-cur" });
    const crumb = FV.h("nav", { class: "nr-net-crumb", "aria-label": L.netCrumbAria },
      FV.h("button", { type: "button", class: "nr-crumb-link", onclick: () => exitN() }, L.netCrumb), FV.h("span", { class: "nr-crumb-sep", text: "›" }), crumbCur);
    const exitBtn = FV.h("button", { type: "button", class: "nr-net-exit", "aria-label": L.netLeave, title: L.netLeave, onclick: () => exitN() }, "← " + L.netLeave);
    const hint = FV.h("div", { class: "nr-net-hint" });
    const fsBtn = (cls, title, text, onclick) => FV.h("button", { type: "button", class: "nr-fs-btn " + cls, title, "aria-label": title, onclick }, text);
    const zoomLbl = fsBtn("nr-fs-zoom", L.fsFit, "100%", () => fitView());
    // on narrow screens the two floating windows take turns, so they never cover each other
    const toggleWin = (cls, other) => { const on = el.classList.toggle(cls) === false; if (on && window.innerWidth < 1040) el.classList.add(other); syncFsBar(); };
    const dockB = fsBtn("nr-fs-tg", L.fsControls, "", () => toggleWin("nr-dock-off", "nr-info-off"));
    const infoB = fsBtn("nr-fs-tg", L.fsPanel, "", () => toggleWin("nr-info-off", "nr-dock-off"));
    dockB.append(FV.h("span", { class: "i", text: "⚙" }), FV.h("span", { class: "t", text: L.fsControls }));
    infoB.append(FV.h("span", { class: "i", text: "ℹ" }), FV.h("span", { class: "t", text: L.fsPanel }));
    let helpTimer = 0;
    const showHelp = (on) => { clearTimeout(helpTimer); el.classList.toggle("nr-help-on", on); helpB.setAttribute("aria-pressed", on ? "true" : "false"); if (on) helpTimer = setTimeout(() => showHelp(false), 9000); };
    const helpB = fsBtn("nr-fs-tg nr-fs-q", L.fsHelpBtn, "?", () => showHelp(!el.classList.contains("nr-help-on")));
    const fitB = fsBtn("", L.fsFit, "", () => fitView(true)); fitB.append(FV.h("span", { class: "i", text: "⤢" }), FV.h("span", { class: "t", text: L.fsFit }));
    const fsClose = fsBtn("nr-fs-close", L.netExit, "", () => toggleFs()); fsClose.append(FV.h("span", { class: "i", text: "✕" }), FV.h("span", { class: "t", text: L.netExit }));
    const fsBar = FV.h("div", { class: "nr-fs-bar", role: "toolbar", "aria-label": L.fsBar },
      fsBtn("nr-fs-z", L.fsZoomOut, "−", () => zoomBy(1 / 1.4)), zoomLbl, fsBtn("nr-fs-z", L.fsZoomIn, "+", () => zoomBy(1.4)),
      FV.h("span", { class: "nr-fs-sep" }), fitB, dockB, infoB, helpB, FV.h("span", { class: "nr-fs-sep" }), fsClose);
    const fsHelp = FV.h("div", { class: "nr-fs-help" });
    const stageBox = FV.h("div", { class: "nr-net-stage" }, cv, tip, crumb, exitBtn, hint, fsBar, fsHelp);
    const live = FV.h("div", { class: "nr-sr", "aria-live": "polite" });
    const panel = FV.h("div", { class: "nr-net-panel" });
    const pL = FV.h("div", { class: "nr-net-sel" }), pR = FV.h("div", { class: "nr-net-mat" });
    panel.append(pL, pR);
    w.stage.append(stageBox, live, keysDesc, panel);
    const segMode = FV.ui.seg({ label: L.netMode, value: mode, options: [{ value: "fwd", label: L.netFwd }, { value: "bwd", label: L.netBwd }], onchange: (v) => { mode = v; start(); } });
    const segSel = FV.ui.seg({ label: L.netNeuron, value: sel, options: N.map((n) => ({ value: n.id, label: n.name })), onchange: (v) => { if (focus > 0.5 || anim) enterN(v); else { sel = v; draw(); } } });
    const play = FV.ui.button({ label: "▶ " + L.netPlay, primary: true, onclick: () => (playing ? stopPlay() : start()) });
    const go = FV.ui.button({ label: "⤵ " + L.netEnter, onclick: () => (focus > 0.5 ? exitN() : enterN(sel)) });
    const ckSpin = FV.ui.check({ label: L.netSpin, checked: spin, onchange: (v) => { spin = v; kick(); } });
    const ckBias = FV.ui.check({ label: L.netBias, checked: false, onchange: (v) => { showBias = v; draw(); } });
    const full = FV.ui.button({ label: "⛶ " + L.netFull, onclick: () => toggleFs() });
    const resetV = FV.ui.button({ label: "↺ " + FV.t("reset"), onclick: () => fitView(true) });
    const actSel = FV.h("select", { class: "nr-act-sel", "aria-label": L.netAct, onchange: () => setAct(actSel.value) }, ACT_ORDER.map((k) => FV.h("option", { value: k, text: NACT[k].label })));
    const actLbl = FV.h("span", { class: "nr-act-lbl" });
    const ckLayer = FV.ui.check({ label: L.netActLayer, checked: false });
    const actReset = FV.h("button", { type: "button", class: "fv-btn", onclick: () => { Object.keys(acts).forEach((k) => (acts[k] = "sigmoid")); live.textContent = L.netActAll; draw(); } }, "↺ " + L.netActReset);
    const actNote = FV.h("div", { class: "nr-act-note", "aria-live": "polite" });
    function setAct(k) {
      const n = byId[sel];
      if (!n || n.layer === 0) return;
      const ids = ckLayer.value ? (n.layer === 1 ? ["h0", "h1", "h2"] : ["y"]) : [sel];
      ids.forEach((id) => (acts[id] = k));
      live.textContent = L.netActSet.replace("{n}", ids.map((id) => byId[id].name).join(", ")).replace("{f}", NACT[k].label);
      draw();
    }
    const xs = X.map((v, i) => FV.ui.slider({ label: `$x_${i + 1}$`, min: -3, max: 3, step: 0.25, value: v, fmt: (u) => FV.fmt(u, 2), oninput: (u) => { X[i] = u; draw(); } }));
    const segY = FV.ui.seg({ label: L.netTarget, value: target, options: [{ value: 0, label: "$y=0$" }, { value: 1, label: "$y=1$" }], onchange: (v) => { target = v; draw(); } });
    w.controls.append(
      FV.h("div", { class: "nr-row" }, play.el, go.el, segMode.el, segY.el),
      FV.h("div", { class: "nr-row" }, segSel.el),
      FV.h("div", { class: "nr-row nr-act" }, actLbl, actSel, ckLayer.el, actReset, actNote),
      FV.h("div", { class: "nr-sliders" }, xs.map((s) => s.el)),
      FV.h("div", { class: "nr-row" }, ckSpin.el, ckBias.el, resetV.el, full.el));
    const ro = FV.ui.readout(w.readout, [{ key: "y", label: "$\\hat y$ =", c: "orange" }, { key: "l", label: L.netLoss }, { key: "p", label: L.netParams }]);

    // ----- projection; `zoom` flies the camera to the node `zt` of the network
    let Wd = 640, Hd = 420, dpr = 1, F = 600;
    const CAM = 6.5;
    function resize() {
      Wd = Math.max(280, isFs ? window.innerWidth : stageBox.clientWidth || 640);
      Hd = isFs ? Math.max(300, window.innerHeight) : Wd < 520 ? Math.round(Wd * 0.95) : FV.clamp(Math.round(Wd * 0.62), 300, 580);
      dpr = Math.min(2, window.devicePixelRatio || 1);
      cv.width = Math.round(Wd * dpr); cv.height = Math.round(Hd * dpr);
      cv.style.width = Wd + "px"; cv.style.height = Hd + "px";
      F = CAM * Math.min((0.47 * Wd) / (Wd < 520 ? 1.95 : 2.05), ((isFs ? 0.32 : 0.42) * Hd) / 1.3);
      exitBtn.textContent = Wd < 520 ? "✕" : "← " + L.netLeave;
      draw();
    }
    function proj(p) {
      const ca = Math.cos(az), sa = Math.sin(az), ce = Math.cos(elv), se = Math.sin(elv);
      const x1 = p[0] * ca + p[2] * sa, z1 = -p[0] * sa + p[2] * ca;
      const y2 = p[1] * ce - z1 * se, z2 = p[1] * se + z1 * ce;
      const dd = CAM - z2, k = dd > 0.35 ? (F / dd) * uz : NaN;
      return { X: Wd / 2 + panX + x1 * k, Y: Hd / 2 + panY - y2 * k, d: z2, k, ok: dd > 0.35 };
    }
    const unit = () => F / CAM;   // pixels per scene unit at the centre
    const mixC = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
    const hex = (c) => { c = (c || "#888").trim(); if (c[0] !== "#") return [128, 128, 128]; const n = parseInt(c.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
    const ease = (u) => (u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2);
    const smooth = (a, b, x) => { const u = FV.clamp((x - a) / (b - a), 0, 1); return u * u * (3 - 2 * u); };

    // value shown in a network node and its colour
    function nodeVal(n, r) {
      if (n.bias) return { v: 1, t: 0 };
      if (mode === "fwd") {
        const v = n.layer === 0 ? X[n.i] : n.layer === 1 ? r.h[n.i] : r.y;
        return { v, t: n.layer === 0 ? FV.clamp(v / 3, -1, 1) : FV.clamp(v, -1, 1) };
      }
      const v = n.layer === 0 ? r.dx[n.i] : n.layer === 1 ? r.d1[n.i] : r.d2;
      return { v, t: FV.clamp(v / 0.4, -1, 1) };
    }
    const related = (e) => e.a === sel || e.b === sel;
    // text with a halo, so it stays readable over lines
    function label(ctx, s, x, y, col, C, size = 12, align = "center", weight = 600) {
      ctx.font = `${weight} ${size}px ${FV.css("sans") || "sans-serif"}`; ctx.textAlign = align; ctx.textBaseline = "middle"; ctx.lineJoin = "round";
      ctx.lineWidth = 4; ctx.strokeStyle = FV.rgb(C.card); ctx.strokeText(s, x, y);
      ctx.fillStyle = col; ctx.fillText(s, x, y);
    }
    function sphere(ctx, x, y, R, fill, C, ring, ringW) {
      const g = ctx.createRadialGradient(x - R * 0.35, y - R * 0.4, R * 0.1, x, y, R);
      g.addColorStop(0, FV.rgb(mixC(fill, [255, 255, 255], 0.55))); g.addColorStop(1, FV.rgb(fill));
      ctx.beginPath(); ctx.arc(x, y, R, 0, Math.PI * 2); ctx.fillStyle = g; ctx.fill();
      ctx.lineWidth = ringW || 1.4; ctx.strokeStyle = ring || FV.rgb(C.ink, 0.75); ctx.stroke();
    }
    const valueFill = (tt, C) => { const tone = mode === "fwd" ? (tt >= 0 ? C.blue : C.red) : (tt >= 0 ? C.red : C.blue); return mixC(C.card, tone, Math.min(0.85, Math.abs(tt) * 0.85)); };

    // ======================= the network view =======================
    function drawNet(ctx, r, C, zoom, alpha) {
      const tgt = byId[inside || sel].pos, s = 1 + 5.5 * zoom;
      const P = {};
      N.concat(BN).forEach((n) => { P[n.id] = proj([(n.pos[0] - tgt[0] * zoom) * s, (n.pos[1] - tgt[1] * zoom) * s, (n.pos[2] - tgt[2] * zoom) * s]); });
      ctx.save(); ctx.globalAlpha = alpha;
      if (zoom < 0.05) [[-1.75, L.netIn], [0, L.netHidden], [1.75, L.netOut]].forEach(([x, s0]) => {
        const q = proj([x, 1.32, 0]);
        ctx.font = `600 ${Math.round((Wd < 520 ? 10 : 12) * FV.clamp(q.k / unit(), 0.8, 1.2))}px ${FV.css("sans") || "sans-serif"}`;
        const hw = ctx.measureText(s0).width / 2 + 6;
        ctx.fillStyle = C.faint; ctx.textAlign = "center"; ctx.textBaseline = "alphabetic"; ctx.fillText(s0, FV.clamp(q.X, hw, Wd - hw), Math.max(14, q.Y));
      });
      const edges = E.filter((e) => showBias || !e.bias).map((e) => ({ e, A: P[e.a], B: P[e.b], d: (P[e.a].d + P[e.b].d) / 2 })).filter((o) => o.A.ok && o.B.ok).sort((u, v) => u.d - v.d);
      edges.forEach(({ e, A, B }) => {
        const wv = e.w(), hl = related(e);
        ctx.strokeStyle = FV.rgb(wv >= 0 ? C.blue : C.red, hl ? 0.95 : 0.22);
        ctx.lineWidth = Math.min(14, (0.6 + 2.4 * Math.min(1, Math.abs(wv) / 1.5)) * ((A.k + B.k) / 2) / unit() * (hl ? 1.25 : 1));
        ctx.setLineDash(e.bias ? [5, 4] : []);
        ctx.beginPath(); ctx.moveTo(A.X, A.Y); ctx.lineTo(B.X, B.Y); ctx.stroke();
      });
      ctx.setLineDash([]);
      if (t >= 0 && zoom < 0.05) edges.forEach(({ e, A, B }) => {
        const st = mode === "fwd" ? e.stage : 1 - e.stage;
        if (t < st * 0.5 || t > st * 0.5 + 0.45) return;
        const u = FV.clamp((t - st * 0.5) / 0.42, 0, 1);
        let mag;
        if (mode === "fwd") { const src = e.bias ? 1 : e.stage === 0 ? X[byId[e.a].i] : r.h[byId[e.a].i]; mag = Math.abs(e.w() * src); }
        else { const dst = byId[e.b]; mag = Math.abs(e.w() * (dst.layer === 2 ? r.d2 : r.d1[dst.i])) * 4; }
        const f = mode === "fwd" ? u : 1 - u;
        ctx.beginPath(); ctx.arc(A.X + (B.X - A.X) * f, A.Y + (B.Y - A.Y) * f, 2.5 + Math.min(6, mag * 2.2), 0, Math.PI * 2);
        ctx.fillStyle = FV.rgb(mode === "fwd" ? (e.w() >= 0 ? C.blue : C.red) : C.orange, related(e) ? 1 : 0.55); ctx.fill();
      });
      if (zoom < 0.05) edges.filter(({ e }) => related(e)).forEach(({ e, A, B }) => label(ctx, (e.bias ? "b=" : "") + n4(e.w()), A.X + (B.X - A.X) * 0.42, A.Y + (B.Y - A.Y) * 0.42, FV.rgb(e.w() >= 0 ? C.blue : C.red), C));
      const flash = (layer) => { if (t < 0) return 0; const at = mode === "fwd" ? layer * 0.5 : (2 - layer) * 0.5; return Math.max(0, 1 - Math.abs(t - at) / 0.08); };
      N.concat(showBias ? BN : []).map((n) => ({ n, q: P[n.id] })).filter((o) => o.q.ok).sort((a, b) => a.q.d - b.q.d).forEach(({ n, q }) => {
        const R = Math.min(Wd, (n.bias ? 0.11 : n.layer === 2 ? 0.25 : 0.21) * q.k * (1 + 0.25 * flash(n.layer)));
        const { v, t: tt } = nodeVal(n, r);
        const fill = n.bias ? C.card : valueFill(tt, C);
        sphere(ctx, q.X, q.Y, R, fill, C, n.id === sel ? FV.rgb(C.orange) : null, n.id === sel ? 3.5 : 1.4);
        if (n.id === "h0") { ctx.setLineDash([3, 3]); ctx.lineWidth = 1.2; ctx.strokeStyle = FV.rgb(C.orange); ctx.beginPath(); ctx.arc(q.X, q.Y, R + 6, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]); }
        if (zoom < 0.4) {
          const dark = (fill[0] * 0.3 + fill[1] * 0.59 + fill[2] * 0.11) < 120;
          ctx.fillStyle = dark ? "#fff" : "#171A20"; ctx.font = `600 ${Math.round(FV.clamp(R * 0.62, 9, 15))}px ${FV.css("sans") || "sans-serif"}`; ctx.textAlign = "center"; ctx.textBaseline = "middle";
          ctx.fillText(n.bias ? "1" : (mode === "bwd" && n.layer > 0 ? FV.num(v, 2) : FV.fmt(v, 2)), q.X, q.Y + 1);
          if (!n.bias) label(ctx, nameOf(n.id), q.X, q.Y + R + 12, n.id === "h0" ? FV.rgb(C.orange) : FV.rgb(C.ink), C);
        }
        if (!n.bias && zoom < 0.05) hot.push({ x: q.X, y: q.Y, r: R + 6, id: n.id, tip: () => `${n.name}: ${mode === "fwd" ? (n.layer ? "a" : "x") : (n.layer ? "δ" : "∂L/∂x")} = ${n4(nodeVal(n, run()).v)} · ${L.netClickIn}` });
      });
      ctx.restore();
    }

    // ======================= the inside of one neuron =======================
    // Its parts, in the neuron's own coordinates: inputs on the left (dendrites), synapses with weights on
    // the membrane, the summation core Σ with the bias, the activation f, and the output (axon) on the right.
    function interior(id, r) {
      const n = byId[id];
      if (n.layer === 0) return { n, fan: true, val: X[n.i], grad: r.dx[n.i],
        outs: W1.map((row, j) => ({ id: "h" + j, name: "h" + SUB[j + 1], w: row[n.i], v: r.h[j], d: r.d1[j] })) };
      const hidden = n.layer === 1, j = n.i;
      const ins = hidden ? X.map((v, i) => ({ id: "x" + i, name: "x" + SUB[i + 1], v, w: W1[j][i] })) : r.h.map((v, k) => ({ id: "h" + k, name: "h" + SUB[k + 1], v, w: W2[k] }));
      const A = Af(id), b = hidden ? B1[j] : B2, z = hidden ? r.z1[j] : r.z2, a = A.f(z), delta = hidden ? r.d1[j] : r.d2;
      return { n, A, ins, b, z, a, delta, sum: z - b, out: hidden ? { id: "y", name: "ŷ", w: W2[j] } : null };
    }
    const RM = 1.2;                                     // membrane radius
    const CORE = [-0.32, 0, 0];
    const GX0 = 0.08, GX1 = 0.86, GY = 0.4;            // the activation graph: a panel inside the cell
    const srcPos = (k, m) => { const t = Math.PI / 2 + (2 * Math.PI * k) / m; return [-2.45, 1.3 * Math.sin(t), 1.3 * Math.cos(t)]; };
    const onMembrane = (p) => { const l = Math.hypot(...p); return p.map((v) => (v / l) * RM); };
    function drawInside(ctx, r, C, alpha, scl) {
      const I = interior(inside, r);
      const P3 = (p) => proj([p[0] * scl, p[1] * scl, p[2] * scl]);
      ctx.save(); ctx.globalAlpha = alpha;
      const sans = FV.css("sans") || "sans-serif";
      const fg = FV.rgb(C.ink), faint = C.faint;
      const signC = (v) => FV.rgb(v >= 0 ? C.blue : C.red);
      const line = (a, b, col, wdt, dash) => { const A = P3(a), B = P3(b); if (!A.ok || !B.ok) return; ctx.strokeStyle = col; ctx.lineWidth = Math.min(16, wdt * ((A.k + B.k) / 2) / unit()); ctx.setLineDash(dash || []); ctx.beginPath(); ctx.moveTo(A.X, A.Y); ctx.lineTo(B.X, B.Y); ctx.stroke(); ctx.setLineDash([]); };
      const along = (pts, u) => { // a point at fraction u of a polyline
        const L0 = []; let tot = 0;
        for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1], pts[i][2] - pts[i - 1][2]); L0.push(d); tot += d; }
        let s = u * tot;
        for (let i = 1; i < pts.length; i++) { if (s <= L0[i - 1] || i === pts.length - 1) { const f = L0[i - 1] ? Math.min(1, s / L0[i - 1]) : 0; return pts[i - 1].map((v, k) => v + (pts[i][k] - v) * f); } s -= L0[i - 1]; }
        return pts[pts.length - 1];
      };
      const pulse = (p, rad, col) => { const q = P3(p); if (!q.ok) return; ctx.beginPath(); ctx.arc(q.X, q.Y, rad * q.k / unit(), 0, Math.PI * 2); ctx.fillStyle = col; ctx.fill(); };
      const ringPath = (fn, col, wdt, dash) => { ctx.beginPath(); for (let i = 0; i <= 64; i++) { const q = P3(fn((2 * Math.PI * i) / 64)); i ? ctx.lineTo(q.X, q.Y) : ctx.moveTo(q.X, q.Y); } ctx.strokeStyle = col; ctx.lineWidth = wdt; ctx.setLineDash(dash || []); ctx.stroke(); ctx.setLineDash([]); };

      if (I.fan) {
        // an input: one number handed to three neurons
        const c = [-1.1, 0, 0], q = P3(c);
        const outs = I.outs.map((o, j) => ({ ...o, p: [1.75, 1.35 * Math.sin(Math.PI / 2 + (2 * Math.PI * j) / 3), 1.35 * Math.cos(Math.PI / 2 + (2 * Math.PI * j) / 3)] }));
        outs.forEach((o) => line(c, o.p, FV.rgb(o.w >= 0 ? C.blue : C.red, 0.9), 1 + 2.6 * Math.min(1, Math.abs(o.w) / 1.5)));
        if (t >= 0) outs.forEach((o) => { const u = mode === "fwd" ? FV.clamp(t / 0.8, 0, 1) : 1 - FV.clamp(t / 0.8, 0, 1); pulse(along([c, o.p], u), 5 + 4 * Math.min(1, Math.abs(o.w * I.val) / 2), FV.rgb(mode === "fwd" ? (o.w * I.val >= 0 ? C.blue : C.red) : C.orange)); });
        outs.slice().sort((a, b) => P3(a.p).d - P3(b.p).d).forEach((o) => {
          const qo = P3(o.p), R = 0.26 * qo.k;
          sphere(ctx, qo.X, qo.Y, R, valueFill(mode === "fwd" ? o.v : FV.clamp(o.d / 0.4, -1, 1), C), C);
          label(ctx, o.name, qo.X, qo.Y + R + 12, fg, C);
          hot.push({ x: qo.X, y: qo.Y, r: R + 6, id: o.id, tip: () => `${o.name} · ${L.netClickIn}` });
          const m = P3(along([c, o.p], 0.62));
          label(ctx, mode === "fwd" ? `w = ${n4(o.w)} · ${n4(I.val)} = ${n4(o.w * I.val)}` : `δ(${o.name})·w = ${n4(o.d * o.w)}`, m.X, m.Y - 12, signC(mode === "fwd" ? o.w * I.val : -o.d * o.w), C);
        });
        const R = 0.42 * q.k;
        sphere(ctx, q.X, q.Y, R, valueFill(mode === "fwd" ? FV.clamp(I.val / 3, -1, 1) : FV.clamp(I.grad / 0.4, -1, 1), C), FV.rgb(C.orange), 3);
        ctx.fillStyle = fg; ctx.font = `600 ${Math.round(FV.clamp(R * 0.45, 11, 20))}px ${sans}`; ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(mode === "fwd" ? FV.fmt(I.val, 2) : FV.num(I.grad, 3), q.X, q.Y);
        label(ctx, I.n.name, q.X, q.Y + R + 14, FV.rgb(C.orange), C, 14);
        ctx.restore();
        return;
      }

      const m = I.ins.length;
      const src = I.ins.map((_, k) => srcPos(k, m)), syn = src.map(onMembrane);
      const bSrc = [CORE[0], -1.85, 0], bSyn = onMembrane([CORE[0], -1, 0.0001]);
      const fz = (zv) => FV.clamp(zv, -4, 4);
      // the panel shows f in the forward pass and its derivative f′ in the backward pass
      const Gf = mode === "bwd" ? I.A.d : I.A.f, gv = Gf(I.z);
      let lo = 0, hi = 0;
      for (let i = 0; i <= 80; i++) { const v = Gf(-4 + (8 * i) / 80); lo = Math.min(lo, v); hi = Math.max(hi, v); }
      if (hi - lo < 1e-6) hi = lo + 1;
      const gx = (zv) => GX0 + ((fz(zv) + 4) / 8) * (GX1 - GX0), gy = (av) => ((FV.clamp(av, lo, hi) - lo) / (hi - lo) - 0.5) * 2 * (GY * 0.85);
      const gPt = [gx(I.z), gy(gv), 0];
      const axonA = [GX1, gy(gv), 0], axonB = [RM, 0, 0], dest = [2.55, 0, 0];

      // membrane: a translucent sphere with three great circles
      const cq = P3([0, 0, 0]), Rp = RM * scl * cq.k;
      const g = ctx.createRadialGradient(cq.X - Rp * 0.3, cq.Y - Rp * 0.35, Rp * 0.1, cq.X, cq.Y, Rp);
      g.addColorStop(0, FV.rgb(mixC(C.card, C.blue, 0.06), 0.9)); g.addColorStop(1, FV.rgb(mixC(C.card, C.blue, 0.22), 0.9));
      ctx.beginPath(); ctx.arc(cq.X, cq.Y, Rp, 0, Math.PI * 2); ctx.fillStyle = g; ctx.fill();
      ctx.lineWidth = 1.6; ctx.strokeStyle = FV.rgb(C.blue, 0.55); ctx.stroke();
      ringPath((a) => [RM * Math.cos(a), 0, RM * Math.sin(a)], FV.rgb(C.blue, 0.28), 1, [3, 4]);
      ringPath((a) => [RM * Math.cos(a), RM * Math.sin(a), 0], FV.rgb(C.blue, 0.28), 1, [3, 4]);
      ringPath((a) => [0, RM * Math.cos(a), RM * Math.sin(a)], FV.rgb(C.blue, 0.2), 1, [3, 4]);

      // dendrites (outside: the weight, inside: the product w·a), the bias, core → f → axon
      I.ins.forEach((it, k) => {
        line(src[k], syn[k], FV.rgb(it.w >= 0 ? C.blue : C.red, 0.95), 1 + 2.8 * Math.min(1, Math.abs(it.w) / 1.5));
        line(syn[k], CORE, FV.rgb(it.w * it.v >= 0 ? C.blue : C.red, 0.75), 0.8 + 2.2 * Math.min(1, Math.abs(it.w * it.v) / 2));
      });
      line(bSrc, bSyn, FV.rgb(I.b >= 0 ? C.blue : C.red, 0.9), 1.6, [5, 4]);
      line(bSyn, CORE, FV.rgb(I.b >= 0 ? C.blue : C.red, 0.7), 1.2, [5, 4]);
      line(CORE, [GX0, 0, 0], fg, 1.4);
      // the activation panel, standing inside the cell
      const corners = [[GX0, -GY, 0], [GX1, -GY, 0], [GX1, GY, 0], [GX0, GY, 0]].map(P3);
      ctx.beginPath(); corners.forEach((q, i) => (i ? ctx.lineTo(q.X, q.Y) : ctx.moveTo(q.X, q.Y))); ctx.closePath();
      ctx.fillStyle = FV.rgb(C.card, 0.92); ctx.fill(); ctx.lineWidth = 1; ctx.strokeStyle = FV.rgb(C.ink, 0.35); ctx.stroke();
      line([GX0, gy(0), 0], [GX1, gy(0), 0], FV.rgb(C.ink, 0.25), 0.8, [2, 3]);
      line([gx(0), -GY, 0], [gx(0), GY, 0], FV.rgb(C.ink, 0.2), 0.8, [2, 3]);
      ctx.beginPath();
      for (let i = 0; i <= 80; i++) { const zv = -4 + (8 * i) / 80, q = P3([gx(zv), gy(Gf(zv)), 0]); i ? ctx.lineTo(q.X, q.Y) : ctx.moveTo(q.X, q.Y); }
      ctx.strokeStyle = FV.rgb(mode === "bwd" ? C.orange : C.blue); ctx.lineWidth = 2.2; ctx.stroke();
      line([gx(I.z), gy(lo), 0], gPt, FV.rgb(C.orange, 0.6), 1, [2, 3]);
      line(axonA, axonB, FV.rgb(C.orange, 0.95), 2.4);
      line(axonB, dest, FV.rgb(I.out ? (I.out.w >= 0 ? C.blue : C.red) : C.orange, 0.95), I.out ? 1 + 2.8 * Math.min(1, Math.abs(I.out.w) / 1.5) : 2.4);

      // pulses: forward — inputs → Σ → f → output; backward — the same path in reverse, carrying δ
      if (t >= 0) {
        const fw = mode === "fwd", T = fw ? t : 1 - t, col = (v) => (fw ? FV.rgb(v >= 0 ? C.blue : C.red) : FV.rgb(C.orange));
        if (T < 0.42) {
          const u = T / 0.42;
          I.ins.forEach((it, k) => pulse(along([src[k], syn[k], CORE], u), 4 + 4 * Math.min(1, Math.abs(it.w * it.v) / 2), col(it.w * it.v)));
          pulse(along([bSrc, bSyn, CORE], u), 4, col(I.b));
        } else if (T < 0.62) pulse(along([CORE, [GX0, 0, 0], gPt], (T - 0.42) / 0.2), 6, col(I.z));
        else if (T < 0.96) pulse(along([gPt, axonA, axonB, dest], (T - 0.62) / 0.34), 6, fw ? FV.rgb(C.orange) : FV.rgb(C.orange));
      }
      const flashCore = t >= 0 ? Math.max(0, 1 - Math.abs((mode === "fwd" ? t : 1 - t) - 0.44) / 0.07) : 0;

      // nodes: sources, core, the point on f, destination
      const things = [];
      I.ins.forEach((it, k) => things.push({ p: src[k], draw: (q) => {
        const R = 0.24 * q.k; sphere(ctx, q.X, q.Y, R, valueFill(mode === "fwd" ? (it.id[0] === "x" ? FV.clamp(it.v / 3, -1, 1) : it.v) : 0, C), C);
        ctx.fillStyle = "#171A20"; ctx.font = `600 ${Math.round(FV.clamp(R * 0.6, 9, 14))}px ${sans}`; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(FV.fmt(it.v, 2), q.X, q.Y + 1);
        label(ctx, it.name, q.X, q.Y + R + 12, fg, C);
        hot.push({ x: q.X, y: q.Y, r: R + 6, id: it.id, tip: () => `${it.name} = ${n4(it.v)} · ${L.netClickIn}` });
      } }));
      things.push({ p: bSrc, draw: (q) => { const R = 0.13 * q.k; sphere(ctx, q.X, q.Y, R, C.card, C); ctx.fillStyle = fg; ctx.font = `600 11px ${sans}`; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("1", q.X, q.Y + 1); } });
      things.push({ p: CORE, draw: (q) => { const R = 0.2 * q.k * (1 + 0.3 * flashCore); sphere(ctx, q.X, q.Y, R, mixC(C.card, C.orange, 0.55), C, FV.rgb(C.orange), 2.4); ctx.fillStyle = "#171A20"; ctx.font = `600 ${Math.round(FV.clamp(R * 0.9, 12, 22))}px ${sans}`; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("Σ", q.X, q.Y + 1);
        hot.push({ x: q.X, y: q.Y, r: R + 6, id: null, tip: () => `Σ wᵢaᵢ = ${n4(I.sum)}, z = ${n4(I.z)}` }); } });
      things.push({ p: gPt, draw: (q) => { ctx.beginPath(); ctx.arc(q.X, q.Y, 5, 0, Math.PI * 2); ctx.fillStyle = FV.rgb(C.orange); ctx.fill(); } });
      things.push({ p: dest, draw: (q) => {
        const R = 0.27 * q.k;
        if (I.out) { const tt = mode === "fwd" ? r.y : FV.clamp(r.d2 / 0.4, -1, 1); sphere(ctx, q.X, q.Y, R, valueFill(tt, C), C); ctx.fillStyle = "#171A20"; ctx.font = `600 ${Math.round(FV.clamp(R * 0.6, 9, 14))}px ${sans}`; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(FV.fmt(mode === "fwd" ? r.y : r.d2, 2), q.X, q.Y + 1);
          label(ctx, I.out.name, q.X, q.Y + R + 12, fg, C); hot.push({ x: q.X, y: q.Y, r: R + 6, id: "y", tip: () => `ŷ = ${n4(r.y)} · ${L.netClickIn}` }); }
        else { ctx.beginPath(); ctx.rect(q.X - R, q.Y - R * 0.75, 2 * R, 1.5 * R); ctx.fillStyle = FV.rgb(mixC(C.card, C.orange, 0.25)); ctx.fill(); ctx.strokeStyle = FV.rgb(C.orange); ctx.lineWidth = 2; ctx.stroke();
          ctx.fillStyle = fg; let fsz = Math.round(FV.clamp(R * 0.42, 9, 13)); ctx.font = `600 ${fsz}px ${sans}`;
          while (fsz > 7 && ctx.measureText(L.inAnswer).width > 1.8 * R) { fsz--; ctx.font = `600 ${fsz}px ${sans}`; }
          ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(L.inAnswer, q.X, q.Y); }
      } });
      things.map((o) => ({ o, q: P3(o.p) })).filter((o) => o.q.ok).sort((a, b) => a.q.d - b.q.d).forEach(({ o, q }) => o.draw(q));

      // labels: the parts of the formula where they live
      const at = (p) => P3(p);
      I.ins.forEach((it, k) => {
        const s = at(syn[k]), wl = at(along([src[k], syn[k]], 0.5));
        if (mode === "fwd") {
          label(ctx, `w${SUB[k + 1]} = ${n4(it.w)}`, wl.X, wl.Y - 13, signC(it.w), C, 13);
          if (Wd >= 520) label(ctx, `w${SUB[k + 1]}·${it.name} = ${n4(it.w * it.v)}`, wl.X, wl.Y + 13, signC(it.w * it.v), C, 11, "center", 500);
        } else label(ctx, `∂L/∂w${SUB[k + 1]} = δ·${it.name} = ${n4(I.delta * it.v)}`, wl.X, wl.Y - 13, FV.rgb(C.orange), C, 12);
        hot.push({ x: s.X, y: s.Y, r: 14, id: null, tip: () => `w${SUB[k + 1]} = ${n4(it.w)}, ${it.name} = ${n4(it.v)}, w·${it.name} = ${n4(it.w * it.v)}, ∂L/∂w = ${n4(I.delta * it.v)}` });
      });
      const bq = at(bSyn);
      label(ctx, mode === "fwd" ? `b = ${n4(I.b)}` : `∂L/∂b = δ = ${n4(I.delta)}`, bq.X + 10, bq.Y + 16, mode === "fwd" ? signC(I.b) : FV.rgb(C.orange), C, 12, "left");
      const cq2 = at(CORE);
      if (mode === "fwd") label(ctx, `Σ = ${n4(I.sum)}`, cq2.X, cq2.Y - 0.2 * cq2.k - 22, fg, C, 12);
      label(ctx, mode === "fwd" ? `z = Σ + b = ${n4(I.z)}` : `δ = ${n4(I.delta)}`, cq2.X, cq2.Y - 0.2 * cq2.k - 8, mode === "fwd" ? FV.rgb(C.orange) : FV.rgb(C.orange), C, 13);
      const gq = at([(GX0 + GX1) / 2, -GY, 0]);
      label(ctx, mode === "fwd" ? `f = ${I.A.name}:  a = ${I.A.name}(${n4(I.z)}) = ${n4(I.a)}` : `f′(z) = ${I.A.name}′(${n4(I.z)}) = ${n4(I.A.d(I.z))}`, gq.X, gq.Y + 14, fg, C, 12);
      const aq = at(along([axonB, dest], 0.45));
      label(ctx, I.out ? (mode === "fwd" ? `a = ${n4(I.a)} → ŷ,  w = ${n4(I.out.w)}` : `δ(ŷ)·w = ${n4(r.d2 * I.out.w)}`) : (mode === "fwd" ? `ŷ = ${n4(I.a)}` : r.bce ? `δ = ŷ − y = ${n4(r.d2)}` : `δ = (ŷ − y)·f′(z) = ${n4(r.d2)}`), aq.X, aq.Y - 14, FV.rgb(C.orange), C, 12);
      // caption of the parts, small, near the membrane
      const mq = at([0, RM, 0]);
      label(ctx, L.inMembrane, mq.X, mq.Y - 10, faint, C, 11, "center", 500);
      ctx.restore();
    }

    function draw() {
      if (!cv.width) return;
      const ctx = cv.getContext("2d"), r = run();
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, Wd, Hd);
      hot = [];
      const C = { card: hex(FV.css("card")), blue: hex(FV.color("blue")), red: hex(FV.color("red")), orange: hex(FV.color("orange")), ink: hex(FV.color("ink")), faint: FV.color("faint") };
      const zoom = ease(FV.clamp(focus / 0.7, 0, 1)), netA = 1 - smooth(0.4, 0.8, focus), inA = smooth(0.45, 0.9, focus);
      if (netA > 0.01) drawNet(ctx, r, C, zoom, netA);
      if (inA > 0.01 && inside) drawInside(ctx, r, C, inA, (Wd < 520 ? 0.62 : 0.7) * (0.6 + 0.4 * smooth(0.45, 1, focus)));
      // overlay: breadcrumb, exit, hint
      const isIn = focus > 0.5 && inside;
      stageBox.classList.toggle("is-in", !!isIn);
      crumbCur.textContent = inside ? nameOf(inside) : "";
      hint.textContent = isIn ? (byId[inside].layer === 0 ? (mode === "fwd" ? L.inFan : L.inFanBwd) + ". " + L.netHintFan : L.netHintIn) : L.netHintNet;
      go.setLabel(isIn ? "⤴ " + L.netLeave : "⤵ " + L.netEnter);
      zoomLbl.textContent = Math.round(uz * 100) + "%";
      zoomLbl.setAttribute("aria-label", L.fsZoomNow.replace("{p}", Math.round(uz * 100)));
      const sn = byId[sel], noAct = sn.layer === 0;
      actLbl.textContent = noAct ? L.netActNone.replace("{n}", sn.name) : L.netActFor.replace("{n}", sn.name);
      actSel.disabled = noAct; if (!noAct && actSel.value !== acts[sel]) actSel.value = acts[sel];
      actNote.textContent = r.bce ? "" : L.netMse;
      ro.set("y", n4(r.y)); ro.set("l", n4(r.loss) + (r.bce ? " (BCE)" : " (MSE)")); ro.set("p", "3·(3+1) + 1·(3+1) = 16");
      segSel.set(sel);
      // the panel (KaTeX) changes only with the data, not with the rotation or the pulses
      const key = [sel, mode, target, X.join(","), isIn ? inside : "", ACT_ORDER.indexOf(acts.h0), ACT_ORDER.indexOf(acts.h1), ACT_ORDER.indexOf(acts.h2), ACT_ORDER.indexOf(acts.y)].join("|");
      if (key !== panelKey) { panelKey = key; renderPanel(r, isIn); }
    }

    function renderPanel(r, isIn) {
      const n = byId[sel];
      pL.textContent = ""; pR.textContent = "";
      const head = FV.h("div", { class: "nr-net-h" }, FV.h("b", { text: n.name + (sel === "h0" ? " — " + L.netOurs : "") }), FV.h("span", { text: [L.netIn, L.netHidden, L.netOut][n.layer] }));
      pL.append(head);
      const add = (src, disp = true) => { const e = FV.tex(src, disp); e.classList.add("nr-net-eq"); pL.append(e); };
      const txt = (s) => pL.append(FV.rich(s, "p"));
      if (n.layer === 0) {
        txt(L.netInText.replace("{i}", n.i + 1));
        add(`x_${n.i + 1} = ${tn(X[n.i])}`);
        if (mode === "bwd") add(`\\frac{\\partial L}{\\partial x_${n.i + 1}} = \\sum_j W_{j${n.i + 1}}\\,\\delta_{h_j} \\approx ${tn(Number(r.dx[n.i].toFixed(4)))}`);
      } else if (n.layer === 1) {
        const j = n.i, row = W1[j];
        txt(L.netHidText);
        add(`z_${j + 1} = ${row.map((v, i) => `${tn(v, true)}\\cdot${tn(X[i], true)}`).join(" + ")} + ${tn(B1[j], true)} = ${tn(Number(r.z1[j].toFixed(4)))}`);
        const AJ = Af("h" + j);
        add(`h_${j + 1} = ${AJ.tex}(z_${j + 1}) \\approx ${tn(Number(r.h[j].toFixed(4)))}`);
        if (mode === "fwd") txt(L.netHidNext.replace("{w}", n4(W2[j])));
        else {
          add(`\\begin{aligned}\\delta_{h_${j + 1}} &= ${AJ.tex}'(z_${j + 1})\\cdot w^{(2)}_${j + 1}\\cdot\\delta_{\\hat y}\\\\ &\\approx ${tn(Number(AJ.d(r.z1[j]).toFixed(4)))}\\cdot${tn(W2[j], true)}\\cdot${tn(Number(r.d2.toFixed(4)), true)} \\approx ${tn(Number(r.d1[j].toFixed(4)))}\\end{aligned}`);
          add(`\\nabla_{\\mathbf{w}_${j + 1}}L = \\delta_{h_${j + 1}}\\,\\mathbf{x} \\approx (${X.map((x) => tn(Number((r.d1[j] * x).toFixed(4)))).join(FV.lang === "en" ? ",\\ " : ";\\ ")})`);
        }
      } else {
        txt(L.netOutText);
        add(`z = ${W2.map((v, j) => `${tn(v, true)}\\cdot${tn(Number(r.h[j].toFixed(4)))}`).join(" + ")} + ${tn(B2, true)} \\approx ${tn(Number(r.z2.toFixed(4)))}`);
        const AO = Af("y");
        add(`\\hat y = ${AO.tex}(z) \\approx ${tn(Number(r.y.toFixed(4)))}`);
        if (mode === "bwd") {
          if (r.bce) add(`\\delta_{\\hat y} = \\hat y - y \\approx ${tn(Number(r.y.toFixed(4)))} - ${target} = ${tn(Number(r.d2.toFixed(4)))}`);
          else add(`\\delta_{\\hat y} = (\\hat y - y)\\cdot ${AO.tex}'(z) \\approx ${tn(Number((r.y - target).toFixed(4)), true)}\\cdot ${tn(Number(AO.d(r.z2).toFixed(4)), true)} = ${tn(Number(r.d2.toFixed(4)))}`);
        }
      }
      if (isIn && n.layer > 0) {
        // inside a neuron: its own table of inputs, weights and contributions (or gradients)
        const I = interior(sel, r);
        const tb = FV.h("table", { class: "nr-mat nr-in-tab" });
        const th = mode === "fwd" ? [L.inCol, L.inVal, L.inW, L.inProd] : [L.inCol, L.inVal, L.inW, L.inGrad];
        tb.append(FV.h("tr", {}, th.map((s) => FV.h("th", {}, FV.rich(s)))));
        I.ins.forEach((it) => {
          const v4 = mode === "fwd" ? it.w * it.v : I.delta * it.v;
          tb.append(FV.h("tr", { onclick: () => enterN(it.id) }, FV.h("th", { text: it.name }), FV.h("td", { text: n4(it.v) }), FV.h("td", { class: it.w >= 0 ? "pos" : "neg", text: n4(it.w) }), FV.h("td", { class: v4 >= 0 ? "pos" : "neg", text: n4(v4) })));
        });
        tb.append(FV.h("tr", {}, FV.h("th", { text: "b" }), FV.h("td", { text: "1" }), FV.h("td", { class: I.b >= 0 ? "pos" : "neg", text: n4(I.b) }), FV.h("td", { class: "b", text: n4(mode === "fwd" ? I.b : I.delta) })));
        const foot = mode === "fwd" ? `$z = ${tn(Number(I.z.toFixed(4)))}$, $a = ${I.A.tex}(z) \\approx ${tn(Number(I.a.toFixed(4)))}$` : `$\\delta \\approx ${tn(Number(I.delta.toFixed(4)))}$`;
        pR.append(FV.h("div", { class: "nr-mat-box" }, FV.rich(L.inTable.replace("{n}", n.name), "span"), tb, FV.rich(foot, "span")));
        return;
      }
      const mat = (title, rows, bias, hiRow, names) => {
        const tb = FV.h("table", { class: "nr-mat" });
        rows.forEach((rw, j) => {
          const tr = FV.h("tr", { class: hiRow === j ? "hi" : null, onclick: () => { sel = names[j]; if (focus > 0.5) enterN(sel); else draw(); } });
          tr.append(FV.h("th", { text: byId[names[j]].name }));
          rw.forEach((v) => tr.append(FV.h("td", { class: v >= 0 ? "pos" : "neg", text: n4(v) })));
          tr.append(FV.h("td", { class: "b " + (bias[j] >= 0 ? "pos" : "neg"), text: n4(bias[j]) }));
          tb.append(tr);
        });
        return FV.h("div", { class: "nr-mat-box" }, FV.rich(title, "span"), tb);
      };
      pR.append(mat(L.netW1, W1, B1, n.layer === 1 ? n.i : -1, ["h0", "h1", "h2"]), mat(L.netW2, [W2], [B2], n.layer === 2 ? 0 : -1, ["y"]));
    }

    // ----- entering and leaving a neuron
    function animateTo(to, dur, done, view) { anim = { from: focus, to, start: performance.now(), dur, done, az0: az, el0: elv, view }; kick(); }
    function enterN(id) {
      sel = id; tip.hidden = true;
      live.textContent = L.netEntered.replace("{n}", byId[id].name);
      if (reduced()) { if (!inside) { az = -0.62; elv = 0.3; } inside = id; focus = 1; anim = null; camTw = null; uz = uzT = 1; panX = panY = 0; draw(); return; }
      camTo(1, 0, 0, 600);
      if (inside && inside !== id && focus > 0.3) animateTo(0.3, 360, () => { inside = id; animateTo(1, 620); });
      else { inside = id; animateTo(1, 950, null, [-0.62, 0.3]); }
    }
    function exitN() {
      if (!inside) return;
      tip.hidden = true; live.textContent = L.netLeft;
      if (reduced()) { focus = 0; inside = null; anim = null; camTw = null; uz = uzT = 1; panX = panY = 0; draw(); return; }
      camTo(1, 0, 0, 600);
      animateTo(0, 750, () => { inside = null; draw(); });
    }

    // ----- the free camera: zoom to a point, pan, fit; full screen
    function zoomBy(f, ax, ay) { if (camTw) { camTw = null; uzT = uz; } uzT = FV.clamp(uzT * f, 0.35, 8); zAnchor = [ax != null ? ax : Wd / 2, ay != null ? ay : Hd / 2]; kick(); }
    function zoomNow(r, ax, ay) {   // immediate zoom by the ratio r around the screen point (ax, ay)
      const nu = FV.clamp(uz * r, 0.35, 8); r = nu / uz;
      const cx = ax - Wd / 2, cy = ay - Hd / 2;
      panX = cx - (cx - panX) * r; panY = cy - (cy - panY) * r; uz = uzT = nu;
    }
    function camTo(u1, x1, y1, dur) { camTw = { u0: uz, x0: panX, y0: panY, u1, x1, y1, start: performance.now(), dur }; kick(); }
    function fitView(rot) { if (rot) { vAz = vEl = 0; if (!inside) { az = -0.62; elv = 0.22; } } camTo(1, 0, 0, 450); }
    function toggleFs() {
      if (document.fullscreenElement === el) { document.exitFullscreen && document.exitFullscreen(); return; }
      if (isFs) { setFs(false); return; }
      if (el.requestFullscreen && document.fullscreenEnabled !== false) el.requestFullscreen().catch(() => setFs(true, true));
      else setFs(true, true);
    }
    let fakeScroll = null;
    function setFs(on, fake) {
      if (on === isFs && !fake) return;
      isFs = on; if (on) visible = true;
      if (on && fake) fakeScroll = window.scrollY;
      const wasFake = el.classList.contains("nr-fs-fake");
      el.classList.toggle("nr-fs", on); el.classList.toggle("nr-fs-fake", !!(on && fake));
      document.documentElement.classList.toggle("nr-noscroll", !!(on && fake));
      // In full screen the wheel is heard on the document. Headless Chromium delivered no wheel events to the
      // full-screen element until some passive wheel listener existed on the window, so one is kept for the
      // duration (a passive listener never blocks scrolling).
      if (on) { document.addEventListener("wheel", onWheel, { passive: false, capture: true }); window.addEventListener("wheel", noop, { passive: true }); }
      else { document.removeEventListener("wheel", onWheel, { capture: true }); window.removeEventListener("wheel", noop); }
      if (on) { const wide = window.innerWidth >= 1040; el.classList.toggle("nr-dock-off", !wide); el.classList.toggle("nr-info-off", !wide); }
      full.setLabel((on ? "✕ " : "⛶ ") + (on ? L.netExit : L.netFull));
      fsHelp.textContent = window.matchMedia && window.matchMedia("(pointer: coarse)").matches ? L.fsHelpTouch : L.fsHelp;
      syncFsBar();
      camTo(1, 0, 0, 1);
      resize();
      showHelp(on);
      if (on) cv.focus({ preventScroll: true });
      else {
        if (wasFake && fakeScroll != null) window.scrollTo(0, fakeScroll);
        fakeScroll = null;
        el.scrollIntoView({ block: "nearest" });
        full.el.focus({ preventScroll: true });
      }
    }
    function syncFsBar() {
      dockB.setAttribute("aria-pressed", el.classList.contains("nr-dock-off") ? "false" : "true");
      infoB.setAttribute("aria-pressed", el.classList.contains("nr-info-off") ? "false" : "true");
    }

    // ----- animation loop: the flight, the pulses and the slow spin
    function frame(now) {
      raf = 0;
      if (!visible && !isFs) return;   // in full screen the element is always visible, whatever the observer says
      let again = false;
      if (anim) {
        const u = FV.clamp((now - anim.start) / anim.dur, 0, 1);
        focus = anim.from + (anim.to - anim.from) * ease(u);
        if (anim.view) { az = anim.az0 + (anim.view[0] - anim.az0) * ease(u); elv = anim.el0 + (anim.view[1] - anim.el0) * ease(u); }
        if (u >= 1) { const d = anim.done; anim = null; d && d(); }
        again = true;
      }
      if (camTw) {
        const u = FV.clamp((now - camTw.start) / camTw.dur, 0, 1), e = ease(u);
        uz = camTw.u0 + (camTw.u1 - camTw.u0) * e; panX = camTw.x0 + (camTw.x1 - camTw.x0) * e; panY = camTw.y0 + (camTw.y1 - camTw.y0) * e;
        if (u >= 1) { camTw = null; uzT = uz; }
        again = true;
      } else if (Math.abs(uzT - uz) > 1e-4) {
        const a = zAnchor || [Wd / 2, Hd / 2];
        const tg = uzT; zoomNow((uz + (uzT - uz) * 0.22) / uz, a[0], a[1]); uzT = tg; again = true;
        if (Math.abs(uzT - uz) <= 1e-4) uz = uzT;
      }
      if (!down && (Math.abs(vAz) > 1e-4 || Math.abs(vEl) > 1e-4)) {
        az += vAz; elv = FV.clamp(elv + vEl, -0.9, 1.2); vAz *= 0.92; vEl *= 0.92; again = true;
      }
      if (spin) { if (lastSpin) az -= Math.min(50, now - lastSpin) * (focus > 0.5 ? 0.00012 : 0.00018); lastSpin = now; again = true; } else lastSpin = 0;
      if (playing) { t = ((now - t0) % 2600) / 2600; again = true; }
      draw();
      if (again || anim) { raf = requestAnimationFrame(frame); rafAt = now; }
    }
    // a frame that was requested but never delivered (a hidden tab, a screenshot) must not stall the loop
    let rafAt = 0;
    const kick = () => {
      const now = performance.now();
      if (raf && now - rafAt < 250) return;
      if (raf) cancelAnimationFrame(raf);
      raf = requestAnimationFrame(frame); rafAt = now;
    };
    function start() { playing = true; t0 = performance.now(); play.setLabel("❚❚ " + FV.t("pause")); kick(); }
    function stopPlay() { playing = false; t = -1; play.setLabel("▶ " + L.netPlay); draw(); }

    // ----- pointer: left drag rotates (with inertia), right / middle / Shift drag pans, the wheel zooms to the cursor
    //       (always in full screen, with Ctrl elsewhere), two fingers pinch and pan; a click on a neuron flies inside it
    const pts = new Map();
    let down = null, moved = 0, dragMode = "rot", pinch = null, lastMove = 0;
    const at = (e) => { const b = cv.getBoundingClientRect(); return [e.clientX - b.left, e.clientY - b.top]; };
    const hit = (px, py) => { let best = null, bd = 1e9; hot.forEach((h) => { const d = Math.hypot(h.x - px, h.y - py); if (d < h.r && d < bd) { bd = d; best = h; } }); return best; };
    const two = () => { const [a, b] = [...pts.values()]; const r = cv.getBoundingClientRect(); return { d: Math.hypot(a[0] - b[0], a[1] - b[1]), m: [(a[0] + b[0]) / 2 - r.left, (a[1] + b[1]) / 2 - r.top] }; };
    cv.addEventListener("contextmenu", (e) => e.preventDefault());
    cv.addEventListener("pointerdown", (e) => {
      pts.set(e.pointerId, [e.clientX, e.clientY]);
      cv.setPointerCapture(e.pointerId);
      if (isFs && el.classList.contains("nr-help-on")) showHelp(false);
      tip.hidden = true;
      if (pts.size === 2 && (isFs || e.pointerType === "touch")) { pinch = two(); down = null; camTw = null; return; }
      if (e.button === 1) e.preventDefault();
      down = [e.clientX, e.clientY]; moved = 0; vAz = vEl = 0; camTw = null;
      dragMode = e.button === 2 || e.button === 1 || e.shiftKey ? "pan" : "rot";
      cv.classList.toggle("is-panning", dragMode === "pan");
    });
    cv.addEventListener("pointermove", (e) => {
      if (pts.has(e.pointerId)) pts.set(e.pointerId, [e.clientX, e.clientY]);
      if (pinch && pts.size === 2) {
        const q = two();
        zoomNow(q.d / (pinch.d || 1), q.m[0], q.m[1]);
        panX += q.m[0] - pinch.m[0]; panY += q.m[1] - pinch.m[1];
        pinch = q; moved += 10;
        if (!raf) draw();
        return;
      }
      if (down) {
        const dx = e.clientX - down[0], dy = e.clientY - down[1]; moved += Math.abs(dx) + Math.abs(dy);
        if (dragMode === "pan") { panX += dx; panY += dy; uzT = uz; }
        else {
          const ra = dx * 0.009; az += ra; vAz = ra;
          if (e.pointerType !== "touch" || isFs) { const re = dy * 0.006; elv = FV.clamp(elv + re, -0.9, 1.2); vEl = re; }
        }
        down = [e.clientX, e.clientY]; lastMove = performance.now();
        if (!raf) draw();
        return;
      }
      const [px, py] = at(e), h = hit(px, py);
      cv.style.cursor = h && h.id ? "pointer" : "";
      if (h) { tip.hidden = false; tip.textContent = h.tip(); tip.style.left = Math.min(px + 12, Wd - 200) + "px"; tip.style.top = py + 14 + "px"; }
      else tip.hidden = true;
    });
    const release = (e, click) => {
      pts.delete(e.pointerId);
      if (pinch) { if (pts.size < 2) pinch = null; down = null; vAz = vEl = 0; return; }
      if (click && down && moved < 6 && dragMode === "rot") { const [px, py] = at(e), h = hit(px, py); if (h && h.id) enterN(h.id); }
      if (dragMode !== "rot" || performance.now() - lastMove > 90) vAz = vEl = 0;
      down = null; cv.classList.remove("is-panning");
      if (Math.abs(vAz) > 1e-4 || Math.abs(vEl) > 1e-4) kick();
    };
    cv.addEventListener("pointerup", (e) => release(e, true));
    cv.addEventListener("pointercancel", (e) => release(e, false));
    cv.addEventListener("pointerleave", () => { tip.hidden = true; });
    // The wheel zooms to the cursor. On the page it needs Ctrl (or a trackpad pinch), so the page keeps scrolling.
    // In full screen it is heard on the document: right after the switch Chromium may not route the wheel to a
    // listener on the canvas or on the element itself, and the page cannot scroll there anyway.
    const noop = () => {};
    function onWheel(e) {
      if (e._nr || (e.target !== cv)) return;
      if (!isFs && !e.ctrlKey && !e.metaKey) return;
      e._nr = true; e.preventDefault();
      const [px, py] = at(e), dy = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaMode === 2 ? e.deltaY * 400 : e.deltaY;
      zoomBy(Math.exp(-FV.clamp(dy, -240, 240) * 0.0018), px, py);
    }
    el.addEventListener("wheel", onWheel, { passive: false });
    cv.addEventListener("dblclick", (e) => { if (!hit(...at(e))) { const [px, py] = at(e); zoomBy(1.8, px, py); } });
    el.addEventListener("keydown", (e) => {
      if (!isFs) return;
      if (e.key === "Tab") {   // the page behind a full-screen widget is not reachable, so focus cycles inside it
        const f = [...el.querySelectorAll('button, input, select, canvas[tabindex], [tabindex="0"]')].filter((x) => !x.disabled && x.offsetParent !== null && getComputedStyle(x).visibility !== "hidden");
        if (!f.length) return;
        const i = f.indexOf(document.activeElement), n = e.shiftKey ? (i <= 0 ? f.length - 1 : i - 1) : (i === f.length - 1 ? 0 : i + 1);
        e.preventDefault(); f[n].focus();
        return;
      }
      if (e.key === "Escape" && e.target !== cv) { e.preventDefault(); if (inside) exitN(); else toggleFs(); }
    });
    cv.addEventListener("keydown", (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;   // Ctrl/⌘ shortcuts (page zoom, save…) belong to the browser
      if (e.key === "Enter") { e.preventDefault(); enterN(sel); return; }
      if ((e.key === "Escape" || e.key === "Backspace") && inside) { e.preventDefault(); e.stopPropagation(); exitN(); return; }
      if (e.key === "Escape" && isFs) { e.preventDefault(); e.stopPropagation(); toggleFs(); return; }
      if (e.key === "+" || e.key === "=") { e.preventDefault(); zoomBy(1.25); return; }
      if (e.key === "-" || e.key === "_") { e.preventDefault(); zoomBy(0.8); return; }
      if (e.key === "0") { e.preventDefault(); fitView(true); return; }
      const pan = { w: [0, 40], s: [0, -40], a: [40, 0], d: [-40, 0], W: [0, 40], S: [0, -40], A: [40, 0], D: [-40, 0], "ц": [0, 40], "ы": [0, -40], "ф": [40, 0], "в": [-40, 0] }[e.key];
      if (pan) { e.preventDefault(); camTw = null; panX += pan[0]; panY += pan[1]; draw(); return; }
      const k = { ArrowLeft: [0.12, 0], ArrowRight: [-0.12, 0], ArrowUp: [0, -0.08], ArrowDown: [0, 0.08] }[e.key];
      if (k && e.shiftKey) { e.preventDefault(); camTw = null; panX += k[0] * 330; panY += k[1] * -500; draw(); return; }
      if (k) { e.preventDefault(); az += k[0]; elv = FV.clamp(elv + k[1], -0.9, 1.2); draw(); }
    });
    window.addEventListener("resize", () => { if (isFs) resize(); });
    if ("ResizeObserver" in window) { let last = 0; new ResizeObserver(() => { const x = stageBox.clientWidth; if (Math.abs(x - last) > 1) { last = x; resize(); } }).observe(stageBox); }
    if ("IntersectionObserver" in window) new IntersectionObserver((es) => es.forEach((e) => { visible = e.isIntersecting; if (visible) kick(); })).observe(el);
    document.addEventListener("fullscreenchange", () => setFs(document.fullscreenElement === el, false));
    const redraw = () => { panelKey = ""; draw(); };
    document.addEventListener("themechange", () => setTimeout(redraw, 320));
    new MutationObserver(redraw).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    if (cfg.enter) { inside = cfg.enter; sel = cfg.enter; focus = 1; }
    resize();
    kick();
  });
})();
