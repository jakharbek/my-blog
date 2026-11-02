/* =====================================================================================
 * ИИ-ассистент блога javharbek.uz — на каждой странице (ru / en / uz).
 *
 * Читатель выделяет фрагмент (слово, формулу, абзац) → рядом кнопка «Спросить ИИ»
 * (или Alt+I, или кнопка в шапке) → панель чата справа. Вопрос уходит на ЛОКАЛЬНЫЙ
 * claude-server (Claude Code на компьютере читателя; OpenAI-совместимый API) вместе с
 * контекстом: страница, раздел, текст раздела и выделенный фрагмент. Ответ приходит потоком.
 *
 * Перенесено из ИИ-ассистента курса «Градиентный бустинг по косточкам»
 * (shared/web/js/ui/assistant.js): лимиты запроса, разбор SSE, скриншот, настройки.
 * Отличия: интерфейс на трёх языках, контекст — из структуры страниц блога, KaTeX
 * подгружается только при открытии панели, у модуля нет зависимостей от кода курса.
 *
 * Безопасность. Ответ модели — недоверенные данные: Markdown разбирается в дерево и
 * собирается через textContent (markdown.js), innerHTML не используется; ссылки — только
 * http/https. Запрос не содержит allow_tools / permission_mode / cwd — модель только отвечает
 * текстом. Настройки и диалоги хранятся только в этом браузере; скриншоты не сохраняются.
 * ===================================================================================== */
(function (root) {
  'use strict';
  const doc = root.document;
  if (!doc) return;
  const GBC = root.GBC || (root.GBC = {});

  /* --------------------------------- настройки ------------------------------------ */
  const DEFAULTS = { url: 'http://127.0.0.1:8137', model: 'sonnet', effort: 'low', token: '' };
  // claude-server.zip собирается при публикации курса; сервер у курсов и блога один и тот же
  const SERVER_ZIP = 'https://jakharbek.github.io/ml_gradient_boosting/claude-server.zip';
  const KATEX = 'https://cdn.jsdelivr.net/npm/katex@0.16.22/dist';
  // claude-server передаёт запрос аргументом командной строки; в Windows она ≈ 32 тыс. символов
  const LIMITS = { selection: 2500, section: 7000, page: 2500, history: 6000, question: 4000, total: 22000, storedTurns: 40 };
  const SHOT_MAX = 1568;

  /* --------------------------------- тексты --------------------------------------- */
  const I18N = {
    ru: {
      quotes: ['«', '»'],
      system: [
        'Ты — ИИ-помощник блога javharbek.uz. Автор блога — Javharbek Abdulatipov, инженер-программист и математик; в блоге — статьи и материалы о машинном обучении, математике и программировании: формулы с разборами, интерактивные рисунки, практикумы. Читатель открыл страницу блога и задаёт вопрос — часто по выделенному фрагменту.',
        '',
        'Правила ответа:',
        '1. Отвечай на языке вопроса (страница — на русском), на «вы», дружелюбно и по существу. Сначала прямой ответ, потом пояснение.',
        '2. Объясняй просто: от интуиции к формуле, каждое новое понятие — простыми словами; английский термин — в скобках при первом упоминании.',
        '3. Опирайся на текст страницы и её обозначения. Не выдумывай чисел и фактов, которых нет на странице; если приводишь свой пример — так и скажи. О самом авторе говори только то, что написано на странице.',
        '4. Будь краток: обычно 80–250 слов. Развёрнуто — только если просят.',
        '5. Формулы — в LaTeX: строчные $…$, выключные $$…$$. Код — в блоках ```python. Разметка — Markdown.',
        '6. Если вопрос не о содержании блога, ответь коротко. Если не уверен — скажи прямо.',
        '7. Отвечай сразу текстом: файлы, команды и другие инструменты не нужны — весь контекст уже в сообщении.',
        '8. Если приложен скриншот — это снимок страницы блога. Сначала коротко скажи, что на нём видно, затем отвечай.',
      ].join('\n'),
      ctxHead: 'Контекст — что читает читатель:',
      page: 'Страница', about: 'Кратко', outline: 'Разделы страницы', addr: 'Адрес',
      quoteHead: 'Выделенный фрагмент страницы', section: 'раздел', reading: 'Читатель сейчас в разделе', sectionText: 'Текст раздела для контекста',
      shotNow: 'К вопросу приложен скриншот страницы.', shotGone: '(К этому вопросу читатель прикладывал скриншот; сейчас он недоступен.)', question: 'Вопрос читателя',
      widget: 'интерактивный рисунок', quiz: 'тест «Проверь себя»', calc: 'калькулятор', start: 'Начало страницы',
      ask: 'Спросить ИИ', askTitle: 'Задать вопрос ИИ-ассистенту по выделенному фрагменту (Alt+I)', toggle: 'ИИ-ассистент (Alt+I)',
      title: 'ИИ-ассистент', newChat: 'Новый диалог', settings: 'Настройки', close: 'Закрыть (Esc)',
      checking: 'проверяю сервер…', online: (m) => 'Claude · ' + m + ' · локально', offlineSt: 'сервер не запущен',
      emptyTitle: 'Спросите о странице', emptyText: 'Выделите любое место — слово, формулу, абзац — и нажмите «Спросить ИИ». Ассистент увидит фрагмент и раздел, в котором он находится. Можно и просто задать вопрос.',
      emptyPage: (t) => 'Открыта страница «' + t + '».',
      placeholder: 'Ваш вопрос…', inputLabel: 'Вопрос ассистенту', send: 'Отправить (Enter)', stop: 'Остановить',
      chipsQuote: ['Объясните проще', 'Приведите пример на числах', 'Зачем это нужно?', 'Как это выглядит в коде?'],
      chipsEmpty: ['Перескажите главную мысль раздела', 'Проверьте меня: задайте 3 вопроса', 'Какие здесь частые ошибки?'],
      fromPage: 'Со страницы', removeQuote: 'Убрать фрагмент', thinking: 'Думаю…', sec: 'с', tokens: 'токенов рассуждений',
      stopped: 'Ответ остановлен.', copy: 'Копировать ответ', copied: 'Ответ скопирован', copyFail: 'Не удалось скопировать', retry: 'Ответить заново',
      noAnswer: 'Не удалось получить ответ.', noLink: 'Нет связи с claude-server. Запустите его и нажмите «Ответить заново».',
      badUrl: 'В настройках указан неверный адрес сервера.', noServer: 'Не удалось связаться с claude-server.', srvErr: (c) => 'Сервер ответил ошибкой ' + c + '.',
      needToken: 'Сервер требует токен: укажите его в настройках ассистента.', empty: 'Модель вернула пустой ответ. Попробуйте ещё раз.', genErr: 'Ошибка генерации.',
      sUrl: 'Адрес claude-server', sUrlHint: 'Локальный сервер на вашем компьютере. Запросы уходят только на этот адрес.', sModel: 'Модель', sEffort: 'Глубина ответа',
      sToken: 'Токен доступа', sTokenHint: 'Нужен, только если сервер запущен с CLAUDE_SERVER_TOKEN.', sTokenPh: 'не требуется', save: 'Сохранить', reset: 'По умолчанию',
      saved: 'Настройки сохранены', urlBad: 'Адрес должен начинаться с http:// или https://',
      models: { sonnet: 'Sonnet — быстро и точно', opus: 'Opus — глубже, медленнее', haiku: 'Haiku — самый быстрый' },
      efforts: { low: 'Быстрый ответ', medium: 'Обдуманный', high: 'Глубокий (дольше)' },
      offTitle: 'ИИ-сервер на вашем компьютере не запущен',
      offText: 'Ассистент работает через Claude Code на вашем компьютере — ключ API не нужен, вопросы никуда, кроме Claude, не уходят. Один раз:',
      step1: ['Установите ', 'Node.js 18+', ' и Claude Code, выполните вход: '],
      step2: 'Скачайте claude-server и распакуйте архив.',
      step3: 'В папке сервера выполните команду:', step4: 'Нажмите «Проверить снова».',
      forbidden: ['Сервер запущен, но отвечает 403: он не разрешает адрес этой страницы ', '. Перезапустите его командой выше — она разрешает этот адрес.'],
      download: 'Скачать claude-server (zip)', check: 'Проверить снова', serverOk: 'Сервер на связи', cmdCopy: 'Копировать', cmdCopied: 'Команда скопирована',
      shotBtn: 'Скриншот страницы к вопросу', shotDefault: 'Объясните, что показано на скриншоте.', shotAlt: 'Скриншот, приложенный к вопросу',
      shotGoneUi: 'скриншот (не сохраняется после перезагрузки)', shotRemove: 'Убрать скриншот', shotWill: 'Скриншот будет отправлен с вопросом',
      shotHint: 'Выделите мышью область для снимка · Enter — всё окно · Esc — отмена', shotArea: 'Выбор области снимка',
      shotFail: 'Не удалось сделать снимок: ', shotType: 'Подойдёт картинка PNG, JPEG, WebP или GIF', shotRead: 'Не удалось прочитать картинку',
      shotOld: 'Запущенный claude-server не принимает картинки — перезапустите его',
      remoteNote: (o) => 'Сервер уже запущен? Если без этой настройки — остановите его (Ctrl+C) и запустите командой выше: она разрешает запросы со страниц ' + o + '.',
      lnaPrompt: 'Браузер спросит, можно ли этому сайту обращаться к устройствам в локальной сети: ответьте «Разрешить» — так страница доберётся до сервера на вашем компьютере.',
      lnaDenied: 'Браузер запретил этому сайту доступ к локальной сети, и страница не видит сервер на вашем компьютере. Разрешите доступ в настройках сайта (значок слева от адреса → «Доступ к локальной сети») и нажмите «Проверить снова».',
      shotPick: 'Приложить картинку', hint: 'Enter — отправить, Shift+Enter — новая строка. Картинку можно вставить из буфера (Ctrl+V). ИИ может ошибаться — сверяйтесь со страницей.',
    },
    en: {
      quotes: ['“', '”'],
      system: [
        'You are the AI assistant of the blog javharbek.uz. The author is Javharbek Abdulatipov, a software engineer and mathematician; the blog has articles and materials on machine learning, mathematics and programming: formulas explained step by step, interactive figures, practice problems. The reader has a blog page open and asks a question, often about a selected fragment.',
        '',
        'Rules:',
        '1. Answer in the language of the question (the page is in English), politely and to the point. Give the direct answer first, then the explanation.',
        '2. Explain simply: from intuition to the formula; explain every new concept in plain words.',
        '3. Rely on the page text and its notation. Do not invent numbers or facts that are not on the page; if you give your own example, say so. About the author, say only what the page says.',
        '4. Be brief: usually 80–250 words. Go into detail only when asked.',
        '5. Formulas in LaTeX: inline $…$, display $$…$$. Code in ```python blocks. Markdown formatting.',
        '6. If the question is not about the blog content, answer briefly. If you are not sure, say so.',
        '7. Answer with text right away: no files, commands or other tools are needed; all context is in the message.',
        '8. If a screenshot is attached, it is a snapshot of a blog page. First say briefly what it shows, then answer.',
      ].join('\n'),
      ctxHead: 'Context, what the reader is reading:',
      page: 'Page', about: 'Summary', outline: 'Page sections', addr: 'Address',
      quoteHead: 'Selected fragment of the page', section: 'section', reading: 'The reader is in the section', sectionText: 'Section text for context',
      shotNow: 'A screenshot of the page is attached.', shotGone: '(The reader attached a screenshot to this question; it is no longer available.)', question: 'Reader’s question',
      widget: 'interactive figure', quiz: 'quiz “Check yourself”', calc: 'calculator', start: 'Top of the page',
      ask: 'Ask AI', askTitle: 'Ask the AI assistant about the selected fragment (Alt+I)', toggle: 'AI assistant (Alt+I)',
      title: 'AI assistant', newChat: 'New chat', settings: 'Settings', close: 'Close (Esc)',
      checking: 'checking the server…', online: (m) => 'Claude · ' + m + ' · local', offlineSt: 'server is not running',
      emptyTitle: 'Ask about the page', emptyText: 'Select any part of the page (a word, a formula, a paragraph) and press “Ask AI”. The assistant sees the fragment and its section. You can also just ask a question.',
      emptyPage: (t) => 'The page “' + t + '” is open.',
      placeholder: 'Your question…', inputLabel: 'Question for the assistant', send: 'Send (Enter)', stop: 'Stop',
      chipsQuote: ['Explain it more simply', 'Give an example with numbers', 'Why is this needed?', 'What does it look like in code?'],
      chipsEmpty: ['Summarize the main idea of this section', 'Quiz me: ask 3 questions', 'What are the common mistakes here?'],
      fromPage: 'From the page', removeQuote: 'Remove the fragment', thinking: 'Thinking…', sec: 's', tokens: 'reasoning tokens',
      stopped: 'The answer was stopped.', copy: 'Copy the answer', copied: 'Answer copied', copyFail: 'Could not copy', retry: 'Answer again',
      noAnswer: 'Could not get an answer.', noLink: 'No connection to claude-server. Start it and press “Answer again”.',
      badUrl: 'The server address in the settings is invalid.', noServer: 'Could not reach claude-server.', srvErr: (c) => 'The server returned error ' + c + '.',
      needToken: 'The server requires a token: enter it in the assistant settings.', empty: 'The model returned an empty answer. Try again.', genErr: 'Generation error.',
      sUrl: 'claude-server address', sUrlHint: 'A local server on your computer. Requests go only to this address.', sModel: 'Model', sEffort: 'Answer depth',
      sToken: 'Access token', sTokenHint: 'Needed only if the server was started with CLAUDE_SERVER_TOKEN.', sTokenPh: 'not required', save: 'Save', reset: 'Defaults',
      saved: 'Settings saved', urlBad: 'The address must start with http:// or https://',
      models: { sonnet: 'Sonnet: fast and accurate', opus: 'Opus: deeper, slower', haiku: 'Haiku: the fastest' },
      efforts: { low: 'Quick answer', medium: 'Considered', high: 'Deep (slower)' },
      offTitle: 'The AI server on your computer is not running',
      offText: 'The assistant works through Claude Code on your computer: no API key is needed, and questions go nowhere except to Claude. Once:',
      step1: ['Install ', 'Node.js 18+', ' and Claude Code, then sign in: '],
      step2: 'Download claude-server and unzip it.',
      step3: 'In the server folder, run:', step4: 'Press “Check again”.',
      forbidden: ['The server is running but answers 403: it does not allow the address of this page ', '. Restart it with the command above, which allows this address.'],
      download: 'Download claude-server (zip)', check: 'Check again', serverOk: 'The server is up', cmdCopy: 'Copy', cmdCopied: 'Command copied',
      shotBtn: 'Attach a screenshot of the page', shotDefault: 'Explain what the screenshot shows.', shotAlt: 'Screenshot attached to the question',
      shotGoneUi: 'screenshot (not kept after reload)', shotRemove: 'Remove the screenshot', shotWill: 'The screenshot will be sent with the question',
      shotHint: 'Drag to select an area · Enter: whole window · Esc: cancel', shotArea: 'Select an area for the screenshot',
      shotFail: 'Could not take the screenshot: ', shotType: 'Use a PNG, JPEG, WebP or GIF image', shotRead: 'Could not read the image',
      shotOld: 'The running claude-server does not accept images; restart it',
      remoteNote: (o) => 'Already running? If it was started without this setting, stop it (Ctrl+C) and start it with the command above, which allows requests from ' + o + '.',
      lnaPrompt: 'The browser will ask whether this site may access devices on your local network: choose “Allow” so the page can reach the server on your computer.',
      lnaDenied: 'The browser has blocked this site from the local network, so the page cannot see the server on your computer. Allow access in the site settings (the icon to the left of the address → “Local network access”) and press “Check again”.',
      shotPick: 'Attach an image', hint: 'Enter to send, Shift+Enter for a new line. You can paste an image from the clipboard (Ctrl+V). AI can make mistakes; check against the page.',
    },
    uz: {
      quotes: ['«', '»'],
      system: [
        'Sen javharbek.uz blogining sun’iy intellekt yordamchisisan. Blog muallifi — Javharbek Abdulatipov, dasturiy ta’minot muhandisi va matematik; blogda mashinali o‘qitish, matematika va dasturlash bo‘yicha maqolalar va materiallar bor: tahlilli formulalar, interaktiv rasmlar, amaliy mashqlar. O‘quvchi blog sahifasini ochgan va savol beradi — ko‘pincha belgilangan parcha bo‘yicha.',
        '',
        'Javob qoidalari:',
        '1. Savol qaysi tilda bo‘lsa, shu tilda javob ber (sahifa — o‘zbek tilida), «siz» deb, samimiy va mazmunli. Avval to‘g‘ridan-to‘g‘ri javob, keyin izoh.',
        '2. Oddiy tushuntir: sezgidan formulaga; har bir yangi tushunchani oddiy so‘zlar bilan; inglizcha atamani birinchi eslatishda qavs ichida ber.',
        '3. Sahifa matni va uning belgilariga tayan. Sahifada yo‘q sonlar va faktlarni to‘qima; o‘z misolingni keltirsang — shuni ayt. Muallif haqida faqat sahifada yozilganini ayt.',
        '4. Qisqa bo‘l: odatda 80–250 so‘z. Batafsil — faqat so‘ralsa.',
        '5. Formulalar — LaTeX da: satr ichida $…$, alohida $$…$$. Kod — ```python bloklarida. Belgilash — Markdown.',
        '6. Savol blog mazmuniga oid bo‘lmasa, qisqa javob ber. Ishonching komil bo‘lmasa — to‘g‘ridan-to‘g‘ri ayt.',
        '7. Darhol matn bilan javob ber: fayllar, buyruqlar va boshqa vositalar kerak emas — butun kontekst xabarda.',
        '8. Skrinshot biriktirilgan bo‘lsa — bu blog sahifasining surati. Avval unda nima ko‘rinayotganini qisqa ayt, keyin javob ber.',
      ].join('\n'),
      ctxHead: 'Kontekst — o‘quvchi nimani o‘qiyapti:',
      page: 'Sahifa', about: 'Qisqacha', outline: 'Sahifa bo‘limlari', addr: 'Manzil',
      quoteHead: 'Sahifadan belgilangan parcha', section: 'bo‘lim', reading: 'O‘quvchi hozir bo‘limda', sectionText: 'Kontekst uchun bo‘lim matni',
      shotNow: 'Savolga sahifa skrinshoti biriktirilgan.', shotGone: '(O‘quvchi bu savolga skrinshot biriktirgan edi; hozir u mavjud emas.)', question: 'O‘quvchining savoli',
      widget: 'interaktiv rasm', quiz: '«O‘zingizni tekshiring» testi', calc: 'kalkulyator', start: 'Sahifa boshi',
      ask: 'AI dan so‘rash', askTitle: 'Belgilangan parcha bo‘yicha AI-yordamchidan so‘rash (Alt+I)', toggle: 'AI-yordamchi (Alt+I)',
      title: 'AI-yordamchi', newChat: 'Yangi suhbat', settings: 'Sozlamalar', close: 'Yopish (Esc)',
      checking: 'server tekshirilmoqda…', online: (m) => 'Claude · ' + m + ' · lokal', offlineSt: 'server ishga tushirilmagan',
      emptyTitle: 'Sahifa haqida so‘rang', emptyText: 'Istalgan joyni — so‘z, formula, xatboshi — belgilang va «AI dan so‘rash» tugmasini bosing. Yordamchi parchani va u turgan bo‘limni ko‘radi. Shunchaki savol berish ham mumkin.',
      emptyPage: (t) => '«' + t + '» sahifasi ochiq.',
      placeholder: 'Savolingiz…', inputLabel: 'Yordamchiga savol', send: 'Yuborish (Enter)', stop: 'To‘xtatish',
      chipsQuote: ['Soddaroq tushuntiring', 'Sonlarda misol keltiring', 'Bu nima uchun kerak?', 'Kodda qanday ko‘rinadi?'],
      chipsEmpty: ['Bo‘limning asosiy fikrini qisqacha ayting', 'Meni tekshiring: 3 ta savol bering', 'Bu yerda qanday xatolar ko‘p uchraydi?'],
      fromPage: 'Sahifadan', removeQuote: 'Parchani olib tashlash', thinking: 'O‘ylayapman…', sec: 's', tokens: 'mulohaza tokenlari',
      stopped: 'Javob to‘xtatildi.', copy: 'Javobni nusxalash', copied: 'Javob nusxalandi', copyFail: 'Nusxalab bo‘lmadi', retry: 'Qaytadan javob berish',
      noAnswer: 'Javob olib bo‘lmadi.', noLink: 'claude-server bilan aloqa yo‘q. Uni ishga tushiring va «Qaytadan javob berish»ni bosing.',
      badUrl: 'Sozlamalarda server manzili noto‘g‘ri.', noServer: 'claude-server bilan bog‘lanib bo‘lmadi.', srvErr: (c) => 'Server ' + c + ' xatosi bilan javob berdi.',
      needToken: 'Server token talab qiladi: uni yordamchi sozlamalarida kiriting.', empty: 'Model bo‘sh javob qaytardi. Yana urinib ko‘ring.', genErr: 'Generatsiya xatosi.',
      sUrl: 'claude-server manzili', sUrlHint: 'Kompyuteringizdagi lokal server. So‘rovlar faqat shu manzilga yuboriladi.', sModel: 'Model', sEffort: 'Javob chuqurligi',
      sToken: 'Kirish tokeni', sTokenHint: 'Faqat server CLAUDE_SERVER_TOKEN bilan ishga tushirilgan bo‘lsa kerak.', sTokenPh: 'talab qilinmaydi', save: 'Saqlash', reset: 'Standart',
      saved: 'Sozlamalar saqlandi', urlBad: 'Manzil http:// yoki https:// bilan boshlanishi kerak',
      models: { sonnet: 'Sonnet — tez va aniq', opus: 'Opus — chuqurroq, sekinroq', haiku: 'Haiku — eng tez' },
      efforts: { low: 'Tez javob', medium: 'O‘ylangan', high: 'Chuqur (uzoqroq)' },
      offTitle: 'Kompyuteringizdagi AI-server ishga tushirilmagan',
      offText: 'Yordamchi kompyuteringizdagi Claude Code orqali ishlaydi — API kaliti kerak emas, savollar Claude dan boshqa hech qayerga ketmaydi. Bir marta:',
      step1: ['', 'Node.js 18+', ' va Claude Code ni o‘rnating, tizimga kiring: '],
      step2: 'claude-server ni yuklab oling va arxivni oching.',
      step3: 'Server papkasida buyruqni bajaring:', step4: '«Qayta tekshirish»ni bosing.',
      forbidden: ['Server ishlayapti, lekin 403 javob beryapti: u bu sahifa manziliga ruxsat bermaydi ', '. Uni yuqoridagi buyruq bilan qayta ishga tushiring — u bu manzilga ruxsat beradi.'],
      download: 'claude-server ni yuklab olish (zip)', check: 'Qayta tekshirish', serverOk: 'Server aloqada', cmdCopy: 'Nusxalash', cmdCopied: 'Buyruq nusxalandi',
      shotBtn: 'Savolga sahifa skrinshotini biriktirish', shotDefault: 'Skrinshotda nima ko‘rsatilganini tushuntiring.', shotAlt: 'Savolga biriktirilgan skrinshot',
      shotGoneUi: 'skrinshot (qayta yuklangandan keyin saqlanmaydi)', shotRemove: 'Skrinshotni olib tashlash', shotWill: 'Skrinshot savol bilan yuboriladi',
      shotHint: 'Sichqoncha bilan sohani belgilang · Enter — butun oyna · Esc — bekor qilish', shotArea: 'Skrinshot sohasini tanlash',
      shotFail: 'Skrinshot olib bo‘lmadi: ', shotType: 'PNG, JPEG, WebP yoki GIF rasm mos keladi', shotRead: 'Rasmni o‘qib bo‘lmadi',
      shotOld: 'Ishlayotgan claude-server rasmlarni qabul qilmaydi — uni qayta ishga tushiring',
      remoteNote: (o) => 'Server allaqachon ishlayaptimi? Agar bu sozlamasiz ishga tushirilgan bo‘lsa — uni to‘xtating (Ctrl+C) va yuqoridagi buyruq bilan ishga tushiring: u ' + o + ' sahifalaridan so‘rovlarga ruxsat beradi.',
      lnaPrompt: 'Brauzer bu saytga lokal tarmoqdagi qurilmalarga murojaat qilishga ruxsat so‘raydi: «Ruxsat berish»ni tanlang — shunda sahifa kompyuteringizdagi serverga yeta oladi.',
      lnaDenied: 'Brauzer bu saytga lokal tarmoqqa kirishni taqiqlagan, sahifa kompyuteringizdagi serverni ko‘rmayapti. Sayt sozlamalarida ruxsat bering (manzil chap tomonidagi belgi → «Lokal tarmoqqa kirish») va «Qayta tekshirish»ni bosing.',
      shotPick: 'Rasm biriktirish', hint: 'Enter — yuborish, Shift+Enter — yangi qator. Rasmni buferdan qo‘yish mumkin (Ctrl+V). AI xato qilishi mumkin — sahifa bilan solishtiring.',
    },
  };
  const LANG = I18N[(doc.documentElement.lang || '').slice(0, 2)] ? (doc.documentElement.lang || '').slice(0, 2) : 'ru';
  const T = I18N[LANG];
  const qt = (s) => T.quotes[0] + s + T.quotes[1];

  /* --------------------------------- мини-хелперы --------------------------------- */
  const SVG_NS = 'http://www.w3.org/2000/svg';
  /** h('div', {class, onclick}, 'текст', child): текст — только через textContent; innerHTML не поддерживается. */
  function build(ns, tag, attrs, children) {
    const el = ns ? doc.createElementNS(ns, tag) : doc.createElement(tag);
    if (attrs) {
      for (const [k, v] of Object.entries(attrs)) {
        if (v === null || v === undefined || v === false) continue;
        if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
        else if (k === 'style' && typeof v === 'object') Object.assign(el.style, v);
        else if (v === true) el.setAttribute(k, '');
        else el.setAttribute(k, String(v));
      }
    }
    for (const c of children.flat(Infinity)) {
      if (c === null || c === undefined || c === false) continue;
      el.appendChild(typeof c === 'object' ? c : doc.createTextNode(String(c)));
    }
    return el;
  }
  const H = (tag, attrs, ...children) => build(null, tag, attrs, children);
  const S = (tag, attrs, ...children) => build(SVG_NS, tag, attrs, children);

  // Иконки — фиксированные фигуры, собранные из элементов SVG (без innerHTML)
  const ICONS = {
    chat: [['path', { d: 'M5 5h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-6.5L8 20.5V17H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z', fill: 'none', 'stroke-width': '1.8', 'stroke-linejoin': 'round' }], ['path', { d: 'M8 10h8M8 13h5', 'stroke-width': '1.8', 'stroke-linecap': 'round' }]],
    close: [['path', { d: 'M6 6l12 12M18 6L6 18', 'stroke-width': '2', 'stroke-linecap': 'round' }]],
    plus: [['path', { d: 'M12 5v14M5 12h14', 'stroke-width': '2', 'stroke-linecap': 'round' }]],
    settings: [['path', { d: 'M4 7h9M17 7h3M4 17h3M11 17h9', 'stroke-width': '1.8', 'stroke-linecap': 'round' }], ['circle', { cx: '15', cy: '7', r: '2', fill: 'none', 'stroke-width': '1.8' }], ['circle', { cx: '9', cy: '17', r: '2', fill: 'none', 'stroke-width': '1.8' }]],
    send: [['path', { d: 'M12 19V6m0 0l-5.5 5.5M12 6l5.5 5.5', fill: 'none', 'stroke-width': '2.2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }]],
    stop: [['rect', { x: '6', y: '6', width: '12', height: '12', rx: '2', fill: 'currentColor', stroke: 'none' }]],
    copy: [['rect', { x: '8', y: '8', width: '12', height: '12', rx: '2', fill: 'none', 'stroke-width': '1.8' }], ['path', { d: 'M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2', fill: 'none', 'stroke-width': '1.8' }]],
    reset: [['path', { d: 'M4 12a8 8 0 1 0 2.3-5.6M4 4v4h4', fill: 'none', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }]],
    alert: [['path', { d: 'M12 4l9 16H3z', fill: 'none', 'stroke-width': '1.8', 'stroke-linejoin': 'round' }], ['path', { d: 'M12 10v4M12 17v.5', 'stroke-width': '2', 'stroke-linecap': 'round' }]],
    download: [['path', { d: 'M12 4v11m0 0l-4-4m4 4l4-4M5 19h14', fill: 'none', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }]],
    camera: [['path', { d: 'M4 8.5A1.5 1.5 0 0 1 5.5 7H8l1.4-2h5.2L16 7h2.5A1.5 1.5 0 0 1 20 8.5v9a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 17.5z', fill: 'none', 'stroke-width': '1.8', 'stroke-linejoin': 'round' }], ['circle', { cx: '12', cy: '13', r: '3.2', fill: 'none', 'stroke-width': '1.8' }]],
    image: [['rect', { x: '3', y: '4', width: '18', height: '16', rx: '2', fill: 'none', 'stroke-width': '1.8' }], ['circle', { cx: '9', cy: '10', r: '2', fill: 'currentColor', stroke: 'none' }], ['path', { d: 'M21 16l-5-5-9 9', fill: 'none', 'stroke-width': '1.8' }]],
  };
  const icon = (name) => S('svg', { viewBox: '0 0 24 24', 'aria-hidden': 'true', fill: 'none', stroke: 'currentColor' }, (ICONS[name] || []).map(([t, a]) => S(t, a)));

  const store = {
    get(key, fallback) {
      try {
        const raw = root.localStorage.getItem('assistant:' + key);
        return raw === null ? fallback : JSON.parse(raw);
      } catch (e) {
        return fallback;
      }
    },
    set(key, value) {
      try {
        root.localStorage.setItem('assistant:' + key, JSON.stringify(value));
      } catch (e) {
        /* приватный режим — без сохранения */
      }
    },
  };
  const settings = () => Object.assign({}, DEFAULTS, store.get('settings', {}) || {});

  let toastTimer = null;
  function toast(text) {
    let t = doc.querySelector('.toast');
    if (!t) {
      t = H('div', { class: 'toast', role: 'status', 'aria-live': 'polite' });
      doc.body.appendChild(t);
    }
    t.textContent = text;
    t.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('show'), 2200);
  }
  async function copyText(text) {
    try {
      await root.navigator.clipboard.writeText(text);
      return true;
    } catch (e) {
      return false;
    }
  }
  function rafThrottle(fn) {
    let queued = false;
    return (...args) => {
      if (queued) return;
      queued = true;
      (root.requestAnimationFrame || ((cb) => setTimeout(cb, 16)))(() => {
        queued = false;
        fn(...args);
      });
    };
  }

  /* --------------------------------- формулы (KaTeX лениво) ----------------------- */
  let katexPromise = null;
  function loadKatex() {
    if (root.katex) return Promise.resolve(true);
    if (katexPromise) return katexPromise;
    katexPromise = new Promise((resolve) => {
      if (!doc.querySelector('link[href*="katex"]')) doc.head.appendChild(H('link', { rel: 'stylesheet', href: KATEX + '/katex.min.css' }));
      const s = H('script', { src: KATEX + '/katex.min.js', defer: true });
      s.onload = () => resolve(true);
      s.onerror = () => resolve(false);
      // страница могла уже подключить KaTeX (материалы) — дождёмся его
      const existing = doc.querySelector('script[src*="katex.min.js"]');
      if (existing) existing.addEventListener('load', () => resolve(true));
      else doc.head.appendChild(s);
      setTimeout(() => resolve(!!root.katex), 8000);
    });
    return katexPromise;
  }
  GBC.h = H; // для markdown.js
  GBC.math = {
    tex(src, display) {
      const span = H('span', { class: display ? 'katex-block' : 'katex-inline' });
      if (root.katex) {
        try {
          root.katex.render(src, span, { displayMode: !!display, throwOnError: false, output: 'htmlAndMathml' });
          return span;
        } catch (e) {
          /* ниже — исходник */
        }
      }
      return H('span', { class: 'no-math' }, display ? '$$' + src + '$$' : '$' + src + '$');
    },
  };

  /* =================================================================================
   * Чистая логика (без DOM): лимиты и сборка запроса — как в курсе
   * ================================================================================= */
  function clip(text, max, around) {
    text = String(text || '');
    if (text.length <= max) return text;
    if (around) {
      const key = around.trim().slice(0, 80);
      const at = key ? text.indexOf(key) : -1;
      if (at >= 0) {
        const start = Math.max(0, Math.min(at - Math.floor(max * 0.4), text.length - max));
        return (start > 0 ? '…' : '') + text.slice(start, start + max).trim() + (start + max < text.length ? '…' : '');
      }
    }
    return text.slice(0, max).trim() + '…';
  }
  const tidy = (text) =>
    String(text || '')
      .replace(/\u00a0/g, ' ')
      .replace(/[ \t]+/g, ' ')
      .replace(/ *\n */g, '\n')
      .replace(/\n{3,}/g, '\n\n')
      .trim();

  function pageBlock(p) {
    if (!p) return '';
    const lines = [T.page + ': ' + qt(p.title) + (p.kicker ? ' (' + p.kicker + ')' : '')];
    if (p.dek) lines.push(T.about + ': ' + p.dek);
    if ((p.outline || []).length) lines.push(T.outline + ': ' + p.outline.join(' → '));
    if (p.url) lines.push(T.addr + ': ' + p.url);
    return clip(lines.join('\n'), LIMITS.page);
  }

  function userContent(turn, full) {
    const parts = [];
    const where = turn.section ? ' (' + T.section + ' ' + qt(turn.section) + ')' : '';
    if (turn.quote) parts.push(T.quoteHead + where + ':\n' + qt(clip(turn.quote, LIMITS.selection)));
    else if (turn.section && full) parts.push(T.reading + ' ' + qt(turn.section) + '.');
    if (full && turn.context) parts.push(T.sectionText + ':\n"""\n' + clip(turn.context, LIMITS.section, turn.quote) + '\n"""');
    if (turn.image && full) parts.push(T.shotNow);
    else if (turn.image || turn.hadImage) parts.push(T.shotGone);
    parts.push(T.question + ': ' + clip(turn.text, LIMITS.question));
    return parts.join('\n\n');
  }

  function buildMessages(page, turns) {
    const system = T.system + '\n\n' + T.ctxHead + '\n' + pageBlock(page);
    const last = turns[turns.length - 1];
    const sizeOf = (list) => list.reduce((s, m) => s + m.content.length + 12, 0);
    let latest = userContent(last, true);
    const history = [];
    let used = 0;
    for (let i = turns.length - 2; i >= 0; i--) {
      const t = turns[i];
      if (t.role === 'assistant' && (t.error || !t.text)) continue;
      const content = t.role === 'user' ? userContent(t, false) : clip(t.text, 2500);
      if (used + content.length > LIMITS.history) break;
      used += content.length;
      history.unshift({ role: t.role, content });
    }
    while (history.length && history[0].role !== 'user') history.shift();
    let messages = [{ role: 'system', content: system }, ...history, { role: 'user', content: latest }];
    while (sizeOf(messages) > LIMITS.total && history.length) {
      history.splice(0, 2);
      messages = [{ role: 'system', content: system }, ...history, { role: 'user', content: latest }];
    }
    if (sizeOf(messages) > LIMITS.total) {
      const over = sizeOf(messages) - LIMITS.total;
      const ctx = clip(last.context || '', Math.max(500, Math.min(LIMITS.section, (last.context || '').length) - over - 50), last.quote);
      latest = userContent(Object.assign({}, last, { context: ctx }), true);
      messages = [{ role: 'system', content: system }, ...history, { role: 'user', content: latest }];
    }
    if (last.image) messages[messages.length - 1].content = [{ type: 'text', text: latest }, { type: 'image_url', image_url: { url: last.image } }];
    return messages;
  }

  function sseParser(onEvent) {
    let buf = '';
    const emit = (block) => {
      const data = block
        .split(/\r?\n/)
        .filter((l) => l.startsWith('data:'))
        .map((l) => l.slice(5).replace(/^ /, ''))
        .join('\n');
      if (!data) return;
      if (data.trim() === '[DONE]') return onEvent('[DONE]');
      try {
        onEvent(JSON.parse(data));
      } catch (e) {
        /* неполная или посторонняя строка */
      }
    };
    return {
      feed(chunk) {
        buf += chunk;
        let m;
        while ((m = /\r?\n\r?\n/.exec(buf))) {
          emit(buf.slice(0, m.index));
          buf = buf.slice(m.index + m[0].length);
        }
      },
      end() {
        if (buf.trim()) emit(buf);
        buf = '';
      },
    };
  }
  function normalizeUrl(url) {
    const s = String(url || '').trim().replace(/\/+$/, '');
    return /^https?:\/\/[^\s/]+(\/[^\s]*)?$/i.test(s) ? s.replace(/\/v1$/i, '') : null;
  }
  function fitSize(w, h, max) {
    const k = Math.min(1, max / Math.max(w, h));
    return { w: Math.max(1, Math.round(w * k)), h: Math.max(1, Math.round(h * k)) };
  }
  function cropRect(rect, view, frame) {
    const sx = frame.w / view.w;
    const sy = frame.h / view.h;
    const x = Math.max(0, Math.min(frame.w - 1, Math.round(rect.x * sx)));
    const y = Math.max(0, Math.min(frame.h - 1, Math.round(rect.y * sy)));
    return { x, y, w: Math.max(1, Math.min(frame.w - x, Math.round(rect.w * sx))), h: Math.max(1, Math.min(frame.h - y, Math.round(rect.h * sy))) };
  }

  /* =================================================================================
   * Страница блога: текст, разделы, выделение
   * ================================================================================= */
  const state = { main: null, turns: [], quote: null, image: null, serverImages: null, serverForbidden: false, busy: false, abort: null, online: null, open: false, capturing: false };
  const el = {};
  const storeKey = () => 'chat:' + root.location.pathname.replace(/index\.html$/, '');
  const saveTurns = () =>
    store.set(
      storeKey(),
      state.turns.slice(-LIMITS.storedTurns).map((t) => ({ role: t.role, text: t.text, quote: t.quote, section: t.section, error: t.error, stopped: t.stopped, hadImage: !!(t.image || t.hadImage) || undefined }))
    );

  const SKIP = 'script, style, noscript, button, svg, input, textarea, select, nav, .toc, .chips, .mat-tools, .mat-btns, .ex-tools, .fv-controls, .fv-readout, .katex-html, .assistant, .assistant-ask, .progress';
  const BLOCK = /^(P|DIV|SECTION|ARTICLE|ASIDE|H[1-6]|LI|UL|OL|DL|DT|DD|TR|TABLE|PRE|BLOCKQUOTE|DETAILS|SUMMARY|HEADER|FOOTER|FIGURE|FIGCAPTION|HR|FIELDSET|LEGEND)$/;

  /** Текст узла так, как его стоит показать модели: формулы — в TeX, рисунки и тесты — пометкой. */
  function textOf(node) {
    let out = '';
    const walk = (n) => {
      if (n.nodeType === 3) {
        out += n.nodeValue;
        return;
      }
      if (n.nodeType !== 1 && n.nodeType !== 11) return;
      if (n.nodeType === 1) {
        if (n.matches(SKIP)) return;
        if (n.classList.contains('katex')) {
          const ann = n.querySelector('annotation');
          const display = n.parentElement && n.parentElement.classList.contains('katex-display');
          if (ann) out += display ? '\n$$' + ann.textContent.trim() + '$$\n' : '$' + ann.textContent.trim() + '$';
          return;
        }
        if (n.classList.contains('katex-mathml')) return;
        if (n.matches('.fv, [data-viz]')) {
          out += '\n[' + T.widget + ']\n';
          return;
        }
        if (n.classList.contains('quiz')) {
          out += '\n[' + T.quiz + ']\n';
          return;
        }
        if (n.classList.contains('calc')) {
          out += '\n[' + T.calc + ']\n';
          return;
        }
        if (n.tagName === 'PRE') {
          out += '\n```\n' + n.textContent.trim() + '\n```\n';
          return;
        }
        if (n.tagName === 'BR') {
          out += '\n';
          return;
        }
        if (n.tagName === 'LI') out += '\n- ';
        else if (n.tagName === 'TD' || n.tagName === 'TH') out += ' | ';
        else if (BLOCK.test(n.tagName)) out += '\n';
      }
      for (const c of n.childNodes) walk(c);
      if (n.nodeType === 1 && BLOCK.test(n.tagName)) out += '\n';
    };
    walk(node);
    return tidy(out);
  }
  const headingText = (h) => (h ? tidy(textOf(h)) : '');

  const fragOf = (nodes) => {
    const frag = doc.createDocumentFragment();
    nodes.forEach((n) => frag.appendChild(n.cloneNode(true)));
    return frag;
  };

  /** В статье разделы «плоские»: h2 и следующие за ним блоки до следующего h2; до первого h2 — вступление. */
  function flatGroup(article, child) {
    const kids = Array.from(article.children);
    let i = kids.indexOf(child);
    if (i < 0) return null;
    while (i >= 0 && kids[i].tagName !== 'H2') i--;
    let j = i + 1;
    const parts = [];
    while (j < kids.length && kids[j].tagName !== 'H2') parts.push(kids[j++]);
    return { title: i >= 0 ? headingText(kids[i]) : T.start, node: fragOf(parts) };
  }

  /** Раздел страницы, к которому относится узел: {title, node}. */
  function sectionOf(node) {
    const start = node && node.nodeType === 3 ? node.parentElement : node;
    if (!start || !start.closest) return { title: '', node: state.main };
    const ex = start.closest('.ex');
    const card = start.closest('.fcard');
    const article = start.closest('.article');
    if (ex) {
      const sec = article ? flatGroup(article, ex.parentElement === article ? ex : ex.closest('.article > *')) : null;
      const name = headingText(ex.querySelector('h3'));
      return { title: (sec && sec.title ? sec.title + ' · ' : '') + name, node: ex };
    }
    if (card) {
      const grp = card.closest('.fgroup');
      const g = grp ? headingText(grp.querySelector('h2')) : '';
      return { title: (g ? g + ' · ' : '') + headingText(card.querySelector('h3')), node: card };
    }
    if (article) {
      let child = start;
      while (child && child.parentElement !== article) child = child.parentElement;
      const sec = child ? flatGroup(article, child) : null;
      if (sec) return sec;
    }
    const sec = start.closest('main section');
    if (sec) {
      const h = sec.querySelector('h1, h2, h3');
      if (!h || h.tagName !== 'H1') return { title: headingText(h), node: sec };
      // шапка страницы (заголовок и подзаголовок) мала — добавим то, что идёт сразу за ней: вступление статьи, список
      const next = sec.nextElementSibling;
      return { title: T.start, node: next && !next.matches(SKIP) ? fragOf([sec, next]) : sec };
    }
    return { title: '', node: state.main };
  }

  /** Раздел, который сейчас на экране (когда чат открыт без выделения). */
  function visibleSection() {
    const top = 100;
    const article = state.main.querySelector('.article');
    if (article) {
      let cur = null;
      for (const h of article.querySelectorAll(':scope > h2')) {
        if (h.getBoundingClientRect().top <= top + 40) cur = h;
        else break;
      }
      if (cur) return flatGroup(article, cur) || { title: '', node: null };
    }
    for (const s of state.main.querySelectorAll('section')) {
      const r = s.getBoundingClientRect();
      if (r.bottom > top + 40 && r.height > 0) return sectionOf(s);
    }
    return { title: '', node: null };
  }

  function pageInfo() {
    const h1 = state.main.querySelector('h1');
    const kicker = state.main.querySelector('.art-head .kicker, .hero .kicker');
    const dek = state.main.querySelector('.art-head .dek, .hero-sub, .dek');
    const outline = Array.from(state.main.querySelectorAll('h2')).map(headingText).filter(Boolean).slice(0, 30);
    return {
      title: h1 ? headingText(h1) : doc.title,
      kicker: kicker ? headingText(kicker) : '',
      dek: dek ? headingText(dek) : '',
      outline,
      url: root.location.origin + root.location.pathname,
    };
  }

  function currentSelection() {
    const sel = root.getSelection && root.getSelection();
    if (!sel || sel.rangeCount === 0 || sel.isCollapsed) return null;
    const range = sel.getRangeAt(0);
    const inMain = (n) => n && state.main.contains(n);
    if (!inMain(sel.anchorNode) || !inMain(sel.focusNode)) return null;
    const host = range.commonAncestorContainer.nodeType === 1 ? range.commonAncestorContainer : range.commonAncestorContainer.parentElement;
    if (host && host.closest('input, textarea, select, [contenteditable="true"], .assistant')) return null;
    const text = textOf(range.cloneContents());
    if (!text.replace(/\s/g, '')) return null;
    return { range, text };
  }
  function quoteFromSelection(s) {
    const sec = sectionOf(s.range.startContainer);
    return { text: clip(s.text, LIMITS.selection), section: sec.title, context: sec.node ? textOf(sec.node) : '' };
  }

  let mouseDown = false;
  let selTimer = null;
  function placeAsk() {
    const s = currentSelection();
    if (!s || mouseDown) return hideAsk();
    const rects = Array.from(s.range.getClientRects()).filter((r) => r.width > 0 && r.height > 0);
    if (!rects.length) return hideAsk();
    const last = rects[rects.length - 1];
    const first = rects[0];
    const vw = doc.documentElement.clientWidth;
    const vh = root.innerHeight;
    el.ask.hidden = false;
    const w = el.ask.offsetWidth;
    const h = el.ask.offsetHeight;
    let top = last.bottom + 8;
    let left = last.right - w / 2;
    if (top + h > vh - 8) top = first.top - h - 8;
    if (top < 8 || last.bottom < 0 || first.top > vh) return hideAsk();
    left = Math.max(8, Math.min(left, vw - w - 8));
    el.ask.style.top = Math.round(top) + 'px';
    el.ask.style.left = Math.round(left) + 'px';
    el.ask.classList.add('show');
  }
  function hideAsk() {
    if (!el.ask) return;
    el.ask.classList.remove('show');
    el.ask.hidden = true;
  }
  function watchSelection() {
    const later = (ms) => {
      clearTimeout(selTimer);
      selTimer = setTimeout(placeAsk, ms);
    };
    doc.addEventListener('mousedown', (e) => {
      if (el.ask.contains(e.target)) return;
      mouseDown = true;
      hideAsk();
    });
    doc.addEventListener('mouseup', () => {
      mouseDown = false;
      later(10);
    });
    doc.addEventListener('keyup', (e) => {
      if (e.shiftKey || e.key === 'Shift' || (e.key === 'a' && (e.ctrlKey || e.metaKey))) later(10);
    });
    doc.addEventListener('touchend', () => later(350), { passive: true });
    doc.addEventListener('selectionchange', () => later(mouseDown ? 100000 : 300));
    const follow = rafThrottle(() => {
      if (!el.ask.hidden) placeAsk();
    });
    root.addEventListener('scroll', follow, { passive: true, capture: true });
    root.addEventListener('resize', follow);
  }

  /* =================================================================================
   * Сервер
   * ================================================================================= */
  function headers() {
    const h = { 'Content-Type': 'application/json' };
    const t = settings().token;
    if (t) h.Authorization = 'Bearer ' + t;
    return h;
  }
  /** Chrome (Local Network Access): сайт из интернета обращается к 127.0.0.1 только с разрешения читателя. */
  async function lnaState() {
    if (!isRemotePage() || !root.navigator.permissions) return null;
    try {
      return (await root.navigator.permissions.query({ name: 'local-network-access' })).state; // granted | prompt | denied
    } catch (e) {
      return null; // браузер не знает такого разрешения — значит, и не спрашивает
    }
  }

  async function checkServer() {
    const url = normalizeUrl(settings().url);
    setStatus(null);
    let ok = false;
    state.serverForbidden = false;
    if (url) {
      const ctl = new AbortController();
      const timer = setTimeout(() => ctl.abort(), 3500);
      try {
        const r = await fetch(url + '/health', { signal: ctl.signal, cache: 'no-store' });
        ok = r.ok;
        state.serverForbidden = r.status === 403;
        state.serverImages = ok ? !!((await r.json().catch(() => ({}))) || {}).images : null;
      } catch (e) {
        ok = false;
      }
      clearTimeout(timer);
      // /health отвечает и чужим адресам; реальное разрешение проверяем пустым preflight-запросом
      if (ok && isRemotePage()) {
        try {
          const r = await fetch(url + '/v1/chat/completions', { method: 'POST', headers: headers(), body: '{}', cache: 'no-store' });
          if (r.status === 403) {
            ok = false;
            state.serverForbidden = true;
          }
        } catch (e) {
          // CORS отказал (старый сервер без этого адреса в списке) — тоже «не разрешено»
          ok = false;
          state.serverForbidden = true;
        }
      }
    }
    if (el.forbidden) el.forbidden.hidden = !state.serverForbidden;
    if (el.lna) {
      const lna = ok ? null : await lnaState();
      el.lna.hidden = !lna || lna === 'granted';
      el.lna.textContent = lna === 'denied' ? T.lnaDenied : T.lnaPrompt;
    }
    setStatus(ok);
    return ok;
  }
  function setStatus(online) {
    state.online = online;
    if (!el.panel) return;
    el.panel.dataset.status = online === null ? 'checking' : online ? 'online' : 'offline';
    el.status.textContent = online === null ? T.checking : online ? T.online(settings().model) : T.offlineSt;
    el.offline.hidden = online !== false;
  }
  async function streamChat(messages, signal, cb) {
    const s = settings();
    const url = normalizeUrl(s.url);
    if (!url) throw Object.assign(new Error(T.badUrl), { kind: 'config' });
    let res;
    try {
      res = await fetch(url + '/v1/chat/completions', {
        method: 'POST',
        headers: headers(),
        body: JSON.stringify({ model: s.model, effort: s.effort, stream: true, messages }),
        signal,
      });
    } catch (e) {
      if (e.name === 'AbortError') throw e;
      throw Object.assign(new Error(T.noServer), { kind: 'offline' });
    }
    if (!res.ok) {
      let msg = T.srvErr(res.status);
      try {
        const j = await res.json();
        if (j && j.error && j.error.message) msg = j.error.message;
      } catch (e) {
        /* тело не JSON */
      }
      if (res.status === 401) msg = T.needToken;
      throw Object.assign(new Error(msg), { kind: res.status === 403 ? 'forbidden' : 'server' });
    }
    let text = '';
    let failed = null;
    const parser = sseParser((ev) => {
      if (ev === '[DONE]') return;
      if (ev.error) {
        failed = ev.error.message || T.genErr;
        return;
      }
      const d = ev.choices && ev.choices[0] && ev.choices[0].delta;
      if (!d) return;
      if (typeof d.reasoning_tokens === 'number') cb.onThinking(d.reasoning_tokens);
      if (d.content) {
        text += d.content;
        cb.onText(text);
      }
    });
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      parser.feed(dec.decode(value, { stream: true }));
    }
    parser.end();
    if (failed) throw Object.assign(new Error(failed), { kind: 'server', partial: text });
    if (!text.trim()) throw Object.assign(new Error(T.empty), { kind: 'server' });
    return text;
  }

  /* =================================================================================
   * Сообщения
   * ================================================================================= */
  const nearBottom = () => el.body.scrollHeight - el.body.scrollTop - el.body.clientHeight < 80;
  const toBottom = () => (el.body.scrollTop = el.body.scrollHeight);

  function withMath(text) {
    const out = [];
    const re = /\$\$([^$]+)\$\$|\$([^$\n]+)\$/g;
    let at = 0;
    let m;
    while ((m = re.exec(text))) {
      if (m.index > at) out.push(text.slice(at, m.index));
      out.push(GBC.math.tex((m[1] || m[2]).trim(), false));
      at = m.index + m[0].length;
    }
    if (at < text.length) out.push(text.slice(at));
    return out;
  }
  const quoteBlock = (q, section) =>
    H('blockquote', { class: 'assistant-cite' }, section ? H('span', { class: 'src' }, T.fromPage + ' · ' + section) : null, H('span', { class: 'txt' }, withMath(clip(q, 600))));

  function renderUser(t) {
    const shot = t.image
      ? H('img', { class: 'assistant-shot', src: t.image, alt: T.shotAlt })
      : t.hadImage
        ? H('span', { class: 'assistant-shot-gone' }, icon('image'), T.shotGoneUi)
        : null;
    return H('div', { class: 'assistant-msg user' }, t.quote ? quoteBlock(t.quote, t.section) : null, shot, H('div', { class: 'bubble' }, t.text));
  }
  function renderBot(t, isLast) {
    const body = H('div', { class: 'assistant-answer' });
    if (t.text) body.appendChild(GBC.md.toElement(t.text));
    if (t.stopped) body.appendChild(H('p', { class: 'assistant-note' }, T.stopped));
    if (t.error) body.appendChild(H('p', { class: 'assistant-error', role: 'alert' }, icon('alert'), H('span', null, t.error)));
    const actions = H('div', { class: 'assistant-actions' });
    if (t.text) {
      const copy = H('button', { type: 'button', class: 'icon-btn', title: T.copy, 'aria-label': T.copy }, icon('copy'));
      copy.addEventListener('click', async () => toast((await copyText(t.text)) ? T.copied : T.copyFail));
      actions.appendChild(copy);
    }
    if (isLast) {
      const retry = H('button', { type: 'button', class: 'icon-btn', title: T.retry, 'aria-label': T.retry }, icon('reset'));
      retry.addEventListener('click', regenerate);
      actions.appendChild(retry);
    }
    return H('div', { class: 'assistant-msg bot' }, body, actions);
  }
  function renderAll() {
    el.log.textContent = '';
    state.turns.forEach((t, i) => el.log.appendChild(t.role === 'user' ? renderUser(t) : renderBot(t, i === state.turns.length - 1 && !state.busy)));
    el.empty.hidden = state.turns.length > 0;
    renderChips();
    toBottom();
  }
  function renderChips() {
    el.chips.textContent = '';
    const list = state.quote ? T.chipsQuote : state.turns.length ? [] : T.chipsEmpty;
    for (const c of list) {
      const b = H('button', { type: 'button', class: 'assistant-chip' }, c);
      b.addEventListener('click', () => send(c));
      el.chips.appendChild(b);
    }
    el.chips.hidden = !list.length || state.busy;
  }
  function renderQuote() {
    el.quote.textContent = '';
    el.quote.hidden = !state.quote;
    if (state.quote) {
      const x = H('button', { type: 'button', class: 'icon-btn', title: T.removeQuote, 'aria-label': T.removeQuote }, icon('close'));
      x.addEventListener('click', () => {
        state.quote = null;
        renderQuote();
        renderChips();
        el.input.focus();
      });
      el.quote.append(quoteBlock(state.quote.text, state.quote.section), x);
    }
  }
  function setBusy(b) {
    state.busy = b;
    el.panel.classList.toggle('busy', b);
    el.log.setAttribute('aria-busy', String(b));
    el.send.replaceChildren(icon(b ? 'stop' : 'send'));
    el.send.title = b ? T.stop : T.send;
    el.send.setAttribute('aria-label', el.send.title);
    updateSend();
    renderChips();
  }
  const updateSend = () => (el.send.disabled = !state.busy && !el.input.value.trim() && !state.image);

  /* --------------------------------- скриншот ------------------------------------- */
  const canCapture = () => !!(root.navigator.mediaDevices && root.navigator.mediaDevices.getDisplayMedia);
  function canvasToDataUrl(canvas) {
    const png = canvas.toDataURL('image/png');
    return png.length < 1500000 ? png : canvas.toDataURL('image/jpeg', 0.9);
  }
  function drawShot(source, frame, crop) {
    const c = crop || { x: 0, y: 0, w: frame.w, h: frame.h };
    const size = fitSize(c.w, c.h, SHOT_MAX);
    const canvas = H('canvas', { width: size.w, height: size.h });
    const ctx = canvas.getContext('2d');
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(source, c.x, c.y, c.w, c.h, 0, 0, size.w, size.h);
    return canvasToDataUrl(canvas);
  }
  function attachImage(dataUrl) {
    state.image = dataUrl;
    renderShot();
    updateSend();
    if (state.serverImages === false) toast(T.shotOld);
  }
  function attachFile(file) {
    if (!file || !/^image\/(png|jpeg|webp|gif)$/.test(file.type)) return toast(T.shotType);
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      attachImage(drawShot(img, { w: img.naturalWidth, h: img.naturalHeight }));
      URL.revokeObjectURL(url);
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      toast(T.shotRead);
    };
    img.src = url;
  }
  function pickRegion(frozen) {
    return new Promise((resolve) => {
      frozen.className = 'assistant-region-frame';
      const box = H('div', { class: 'assistant-region-box', hidden: true });
      const hint = H('div', { class: 'assistant-region-hint' }, T.shotHint);
      const layer = H('div', { class: 'assistant-region', tabindex: '-1', role: 'dialog', 'aria-label': T.shotArea }, frozen, box, hint);
      let start = null;
      const rectOf = (e) => ({ x: Math.min(start.x, e.clientX), y: Math.min(start.y, e.clientY), w: Math.abs(e.clientX - start.x), h: Math.abs(e.clientY - start.y) });
      const finish = (value) => {
        layer.remove();
        doc.removeEventListener('keydown', onKey, true);
        resolve(value);
      };
      const onKey = (e) => {
        if (e.key === 'Escape' || e.key === 'Enter') {
          e.preventDefault();
          e.stopPropagation();
          finish(e.key === 'Enter' ? 'full' : null);
        }
      };
      layer.addEventListener('pointerdown', (e) => {
        start = { x: e.clientX, y: e.clientY };
        layer.setPointerCapture(e.pointerId);
        hint.hidden = true;
      });
      layer.addEventListener('pointermove', (e) => {
        if (!start) return;
        const r = rectOf(e);
        box.hidden = false;
        Object.assign(box.style, { left: r.x + 'px', top: r.y + 'px', width: r.w + 'px', height: r.h + 'px' });
      });
      layer.addEventListener('pointerup', (e) => {
        if (!start) return;
        const r = rectOf(e);
        finish(r.w >= 8 && r.h >= 8 ? r : 'full');
      });
      doc.addEventListener('keydown', onKey, true);
      doc.body.appendChild(layer);
      layer.focus();
    });
  }
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const nextFrame = () => new Promise((r) => (root.requestAnimationFrame || setTimeout)(() => r()));
  /** Один кадр вкладки, затем выбор области на застывшем кадре (как в курсе). */
  async function captureScreenshot() {
    if (state.capturing) return;
    if (!canCapture()) return el.file.click();
    state.capturing = true;
    let stream = null;
    const video = H('video', { class: 'assistant-capture-video', muted: true, playsinline: true });
    try {
      stream = await root.navigator.mediaDevices.getDisplayMedia({ video: { displaySurface: 'browser' }, audio: false, preferCurrentTab: true, selfBrowserSurface: 'include' });
      const track = stream.getVideoTracks()[0];
      const isTab = (track.getSettings ? track.getSettings().displaySurface : 'browser') === 'browser';
      doc.body.classList.add('assistant-shooting');
      doc.body.appendChild(video);
      video.srcObject = stream;
      await video.play();
      await nextFrame();
      await nextFrame();
      await Promise.race([new Promise((r) => (video.requestVideoFrameCallback ? video.requestVideoFrameCallback(() => r()) : r())), sleep(500)]);
      await sleep(250);
      const frame = { w: video.videoWidth, h: video.videoHeight };
      if (!frame.w || !frame.h) throw new Error('empty frame');
      const frozen = H('canvas', { width: frame.w, height: frame.h });
      frozen.getContext('2d').drawImage(video, 0, 0);
      stream.getTracks().forEach((t) => t.stop());
      stream = null;
      const region = isTab ? await pickRegion(frozen) : 'full';
      if (region) attachImage(drawShot(frozen, frame, region === 'full' ? null : cropRect(region, { w: root.innerWidth, h: root.innerHeight }, frame)));
    } catch (e) {
      if (e && e.name !== 'NotAllowedError' && e.name !== 'AbortError') toast(T.shotFail + (e.message || e.name));
    } finally {
      if (stream) stream.getTracks().forEach((t) => t.stop());
      video.remove();
      doc.body.classList.remove('assistant-shooting');
      state.capturing = false;
      if (el.input) el.input.focus({ preventScroll: true });
    }
  }
  function renderShot() {
    el.shot.textContent = '';
    el.shot.hidden = !state.image;
    if (!state.image) return;
    const x = H('button', { type: 'button', class: 'icon-btn', title: T.shotRemove, 'aria-label': T.shotRemove }, icon('close'));
    x.addEventListener('click', () => {
      state.image = null;
      renderShot();
      updateSend();
      el.input.focus();
    });
    el.shot.append(H('img', { src: state.image, alt: T.shotAlt }), H('span', null, T.shotWill), x);
  }

  /* --------------------------------- отправка ------------------------------------- */
  async function send(textArg) {
    if (state.busy) return;
    const text = (textArg || el.input.value).trim() || (state.image ? T.shotDefault : '');
    if (!text) return;
    const q = state.quote;
    const sec = q ? null : visibleSection();
    const turn = { role: 'user', text, quote: q ? q.text : undefined, section: q ? q.section : sec.title || undefined, image: state.image || undefined };
    turn.context = q ? q.context : sec.node ? textOf(sec.node) : '';
    state.turns.push(turn);
    state.quote = null;
    state.image = null;
    renderShot();
    if (!textArg) {
      el.input.value = '';
      autosize();
    }
    renderQuote();
    await answer();
  }
  function regenerate() {
    if (state.busy) return;
    while (state.turns.length && state.turns[state.turns.length - 1].role === 'assistant') state.turns.pop();
    if (state.turns.length) answer();
  }
  async function answer() {
    const bot = { role: 'assistant', text: '' };
    const messages = buildMessages(pageInfo(), state.turns);
    state.turns.push(bot);
    setBusy(true);
    renderAll();
    const node = el.log.lastChild;
    const body = node.querySelector('.assistant-answer');
    const think = H('div', { class: 'assistant-thinking' }, H('span', { class: 'dots', 'aria-hidden': 'true' }, H('i'), H('i'), H('i')), H('span', { class: 'label' }, T.thinking));
    body.replaceChildren(think);
    const t0 = Date.now();
    const tick = setInterval(() => {
      const label = think.querySelector('.label');
      if (label && think.isConnected) label.textContent = T.thinking + ' ' + Math.round((Date.now() - t0) / 1000) + ' ' + T.sec + (think.dataset.tokens ? ' · ≈ ' + think.dataset.tokens + ' ' + T.tokens : '');
    }, 1000);
    const paint = rafThrottle(() => {
      const stick = nearBottom();
      body.replaceChildren(GBC.md.toElement(bot.text), H('span', { class: 'assistant-caret', 'aria-hidden': 'true' }));
      if (stick) toBottom();
    });
    state.abort = new AbortController();
    try {
      bot.text = await streamChat(messages, state.abort.signal, {
        onThinking: (n) => (think.dataset.tokens = String(n)),
        onText: (text) => {
          bot.text = text;
          paint();
        },
      });
      if (state.online !== true) setStatus(true);
    } catch (e) {
      if (e.name === 'AbortError') bot.stopped = true;
      else {
        if (e.partial) bot.text = e.partial;
        bot.error = e.message || T.noAnswer;
        if (e.kind === 'offline' || e.kind === 'forbidden') {
          if (e.kind === 'forbidden') state.serverForbidden = true;
          if (el.forbidden) el.forbidden.hidden = !state.serverForbidden;
          setStatus(false);
          bot.error = T.noLink;
        }
      }
    } finally {
      clearInterval(tick);
      state.abort = null;
      setBusy(false);
      saveTurns();
      const top = el.body.scrollTop;
      const stick = nearBottom();
      renderAll();
      if (!stick) el.body.scrollTop = top;
    }
  }

  /* =================================================================================
   * Панель
   * ================================================================================= */
  function autosize() {
    el.input.style.height = 'auto';
    el.input.style.height = Math.min(160, el.input.scrollHeight) + 'px';
    updateSend();
  }
  const isLocalHost = () => /^(localhost|127\.0\.0\.1|\[::1\])$/i.test(root.location.hostname);
  const isRemotePage = () => /^https?:$/.test(root.location.protocol) && !isLocalHost();
  const isWindows = () => /Win/i.test((root.navigator.userAgentData && root.navigator.userAgentData.platform) || root.navigator.platform || root.navigator.userAgent || '');

  /** Команда запуска сервера: для страницы из интернета — с разрешением её адреса. */
  function serverCommand(os) {
    if (!isRemotePage()) return 'npm start';
    const origin = root.location.origin;
    return os === 'win' ? '$env:CLAUDE_SERVER_ALLOWED_ORIGINS="' + origin + '"; npm start' : 'CLAUDE_SERVER_ALLOWED_ORIGINS=' + origin + ' npm start';
  }

  function buildSettings() {
    const s = settings();
    const field = (label, control, hint) => H('label', { class: 'assistant-field' }, H('span', null, label), control, hint ? H('small', null, hint) : null);
    const url = H('input', { type: 'url', value: s.url, spellcheck: 'false', autocomplete: 'off' });
    const option = (v, label, cur) => H('option', { value: v, selected: v === cur }, label);
    const model = H('select', null, ['sonnet', 'opus', 'haiku'].map((m) => option(m, T.models[m], s.model)));
    const effort = H('select', null, ['low', 'medium', 'high'].map((m) => option(m, T.efforts[m], s.effort)));
    const token = H('input', { type: 'password', value: s.token, autocomplete: 'off', placeholder: T.sTokenPh });
    const save = H('button', { type: 'button', class: 'btn small primary' }, T.save);
    const reset = H('button', { type: 'button', class: 'btn small ghost' }, T.reset);
    save.addEventListener('click', () => {
      const u = normalizeUrl(url.value);
      if (!u) {
        url.setAttribute('aria-invalid', 'true');
        url.focus();
        return toast(T.urlBad);
      }
      store.set('settings', { url: u, model: model.value, effort: effort.value, token: token.value.trim() });
      toggleSettings(false);
      checkServer();
      toast(T.saved);
    });
    reset.addEventListener('click', () => {
      store.set('settings', {});
      el.settings.replaceChildren(...buildSettings());
      checkServer();
    });
    return [field(T.sUrl, url, T.sUrlHint), field(T.sModel, model), field(T.sEffort, effort), field(T.sToken, token, T.sTokenHint), H('div', { class: 'assistant-settings-foot' }, reset, save)];
  }
  function toggleSettings(show) {
    const on = show === undefined ? el.settings.hidden : show;
    if (on) el.settings.replaceChildren(...buildSettings());
    el.settings.hidden = !on;
    el.settingsBtn.setAttribute('aria-expanded', String(on));
  }

  function buildOffline() {
    let os = isWindows() ? 'win' : 'unix';
    const code = H('code', null, serverCommand(os));
    const copyCmd = H('button', { type: 'button', class: 'btn small ghost' }, icon('copy'), T.cmdCopy);
    copyCmd.addEventListener('click', async () => toast((await copyText(code.textContent)) ? T.cmdCopied : T.copyFail));
    let osSwitch = null;
    if (isRemotePage()) {
      const mk = (id, label) => {
        const b = H('button', { type: 'button', 'aria-pressed': String(os === id) }, label);
        b.addEventListener('click', () => {
          os = id;
          code.textContent = serverCommand(os);
          osSwitch.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
        });
        return b;
      };
      osSwitch = H('div', { class: 'os', role: 'group' }, mk('win', 'Windows (PowerShell)'), mk('unix', 'macOS / Linux'));
    }
    const retry = H('button', { type: 'button', class: 'btn small' }, icon('reset'), T.check);
    retry.addEventListener('click', async () => {
      if (await checkServer()) toast(T.serverOk);
    });
    const download = H('a', { class: 'btn small', href: SERVER_ZIP, download: 'claude-server.zip', rel: 'noopener' }, icon('download'), T.download);
    el.forbidden = H('p', { class: 'muted', hidden: true }, H('strong', null, '403 · '), T.forbidden[0], H('code', null, root.location.origin), T.forbidden[1]);
    return H(
      'div',
      { class: 'assistant-offline', hidden: true, role: 'status' },
      H('strong', null, icon('alert'), T.offTitle),
      H('p', null, T.offText),
      H(
        'ol',
        null,
        H('li', null, T.step1[0], H('a', { href: 'https://nodejs.org/', target: '_blank', rel: 'noopener noreferrer' }, T.step1[1]), T.step1[2], H('code', null, 'claude login')),
        H('li', null, T.step2),
        H('li', null, T.step3, osSwitch, H('div', { class: 'cmd' }, code, copyCmd), isRemotePage() ? H('small', { class: 'muted remote-note' }, T.remoteNote(root.location.origin)) : null),
        H('li', null, T.step4)
      ),
      el.forbidden,
      (el.lna = H('p', { class: 'muted lna', hidden: true })),
      H('div', { class: 'actions' }, download, retry)
    );
  }

  function buildPanel() {
    const iconBtn = (name, label, fn) => {
      const b = H('button', { type: 'button', class: 'icon-btn', title: label, 'aria-label': label }, icon(name));
      b.addEventListener('click', fn);
      return b;
    };
    el.status = H('span', { class: 'assistant-status' });
    el.settingsBtn = iconBtn('settings', T.settings, () => toggleSettings());
    el.settingsBtn.setAttribute('aria-expanded', 'false');
    const head = H(
      'header',
      { class: 'assistant-head' },
      H('span', { class: 'assistant-logo' }, icon('chat')),
      H('div', { class: 'assistant-title' }, H('strong', null, T.title), H('span', { class: 'sub' }, H('i', { class: 'dot', 'aria-hidden': 'true' }), el.status)),
      iconBtn('plus', T.newChat, newChat),
      el.settingsBtn,
      iconBtn('close', T.close, () => close())
    );
    el.settings = H('div', { class: 'assistant-settings', hidden: true });
    el.offline = buildOffline();
    const info = pageInfo();
    el.empty = H(
      'div',
      { class: 'assistant-empty' },
      H('span', { class: 'big' }, icon('chat')),
      H('strong', null, T.emptyTitle),
      H('p', null, T.emptyText),
      H('p', { class: 'muted' }, info.title ? T.emptyPage(info.title) : '')
    );
    el.log = H('div', { class: 'assistant-log', role: 'log', 'aria-live': 'polite' });
    el.body = H('div', { class: 'assistant-body' }, el.empty, el.log);
    el.quote = H('div', { class: 'assistant-quote', hidden: true });
    el.chips = H('div', { class: 'assistant-chips' });
    el.shot = H('div', { class: 'assistant-shot-preview', hidden: true });
    el.input = H('textarea', { rows: '1', placeholder: T.placeholder, 'aria-label': T.inputLabel, maxlength: String(LIMITS.question) });
    el.input.addEventListener('input', autosize);
    el.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
        e.preventDefault();
        send();
      }
    });
    el.input.addEventListener('paste', (e) => {
      const file = Array.from((e.clipboardData && e.clipboardData.files) || []).find((f) => f.type.startsWith('image/'));
      if (file) {
        e.preventDefault();
        attachFile(file);
      }
    });
    el.file = H('input', { type: 'file', accept: 'image/png,image/jpeg,image/webp,image/gif', hidden: true, 'aria-hidden': 'true', tabindex: '-1' });
    el.file.addEventListener('change', () => {
      if (el.file.files && el.file.files[0]) attachFile(el.file.files[0]);
      el.file.value = '';
    });
    const shotLabel = canCapture() ? T.shotBtn : T.shotPick;
    const shotBtn = H('button', { type: 'button', class: 'icon-btn assistant-camera', title: shotLabel, 'aria-label': shotLabel }, icon('camera'));
    shotBtn.addEventListener('click', captureScreenshot);
    el.send = H('button', { type: 'button', class: 'assistant-send', title: T.send, 'aria-label': T.send }, icon('send'));
    el.send.addEventListener('click', () => (state.busy ? state.abort && state.abort.abort() : send()));
    const foot = H('footer', { class: 'assistant-foot' }, el.quote, el.shot, el.chips, H('div', { class: 'assistant-input' }, shotBtn, el.input, el.send, el.file), H('p', { class: 'assistant-hint' }, T.hint));
    el.panel = H('aside', { class: 'assistant', 'aria-label': T.title, hidden: true }, head, el.settings, el.offline, el.body, foot);
    el.panel.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        e.stopPropagation();
        if (!el.settings.hidden) toggleSettings(false);
        else close();
      }
    });
    doc.body.appendChild(el.panel);
    updateSend();
  }

  function newChat() {
    if (state.abort) state.abort.abort();
    state.turns = [];
    state.quote = null;
    state.image = null;
    saveTurns();
    renderQuote();
    renderShot();
    renderAll();
    el.input.focus();
  }

  let returnFocus = null;
  function open(quote) {
    if (!el.panel) buildPanel();
    if (quote) state.quote = quote;
    if (!state.open) {
      returnFocus = doc.activeElement;
      state.open = true;
      el.panel.hidden = false;
      doc.body.classList.add('assistant-open');
      el.toggle.setAttribute('aria-pressed', 'true');
      renderAll();
      checkServer();
      // формулы в ответах: KaTeX грузится только сейчас; после загрузки — перерисовать
      if (!root.katex) loadKatex().then((ok) => ok && renderAll());
    }
    renderQuote();
    renderChips();
    hideAsk();
    setTimeout(() => el.input.focus({ preventScroll: true }), 30);
  }
  function close() {
    if (!state.open) return;
    state.open = false;
    el.panel.hidden = true;
    doc.body.classList.remove('assistant-open');
    el.toggle.setAttribute('aria-pressed', 'false');
    if (returnFocus && returnFocus.focus && doc.contains(returnFocus)) returnFocus.focus({ preventScroll: true });
  }

  /* --------------------------------- инициализация -------------------------------- */
  function init() {
    const main = doc.querySelector('main');
    if (!main || el.ask || !GBC.md) return;
    state.main = main;
    state.turns = (store.get(storeKey(), []) || []).filter((t) => t && (t.role === 'user' || t.role === 'assistant') && typeof t.text === 'string');

    el.ask = H('button', { type: 'button', class: 'assistant-ask', hidden: true, title: T.askTitle }, icon('chat'), H('span', null, T.ask));
    el.ask.addEventListener('mousedown', (e) => e.preventDefault());
    el.ask.addEventListener('click', () => {
      const s = currentSelection();
      if (s) open(quoteFromSelection(s));
    });
    doc.body.appendChild(el.ask);
    watchSelection();

    el.toggle = H('button', { type: 'button', class: 'assistant-toggle', 'aria-label': T.toggle, title: T.toggle, 'aria-pressed': 'false' }, icon('chat'));
    el.toggle.addEventListener('click', () => (state.open ? close() : open(null)));
    const theme = doc.getElementById('theme-toggle');
    const tools = doc.querySelector('.site-header .tools');
    if (theme && theme.parentElement) theme.parentElement.insertBefore(el.toggle, theme);
    else if (tools) tools.appendChild(el.toggle);
    else {
      el.toggle.classList.add('floating');
      doc.body.appendChild(el.toggle);
    }

    doc.addEventListener('keydown', (e) => {
      if (e.altKey && !e.ctrlKey && !e.metaKey && (e.code === 'KeyI' || e.key === 'i' || e.key === 'ш')) {
        e.preventDefault();
        const s = currentSelection();
        if (s) open(quoteFromSelection(s));
        else if (state.open) close();
        else open(null);
      } else if (e.key === 'Escape' && el.ask && !el.ask.hidden) hideAsk();
    });
  }

  GBC.assistant = { init, open, close, _pure: { clip, tidy, buildMessages, userContent, pageBlock, sseParser, normalizeUrl, fitSize, cropRect, serverCommand } };
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', init);
  else init();
})(typeof window !== 'undefined' ? window : globalThis);
