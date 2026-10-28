#!/usr/bin/env python3
"""Generate the site: three languages × (home, article, about, materials).

Run from the repository root:  python3 tools/build.py
The output is committed, so GitHub Pages needs no build step.
Article texts live in tools/content_sigmoid.py, materials in tools/content_formulas.py.
"""
import html
import importlib.util
import json
import sys
from pathlib import Path

import content_formulas as formulas
from content_sigmoid import ARTICLE, TABLE_ROWS

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["ru", "en", "uz"]
DATE_ISO = "2026-10-14"
ATTRACTOR = (ROOT / "tools" / "attractor.txt").read_text().strip()

FONTS = (
    '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600&family=STIX+Two+Text:ital,wght@0,400;1,400&family=JetBrains+Mono:wght@400&display=swap">\n'
)
THEME_BOOT = (
    '  <script>try{var t=localStorage.getItem("theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>\n'
)
LANG_NAME = {"ru": "RU", "en": "EN", "uz": "UZ"}

SITE = {
    "ru": dict(
        brand="Абдулатипов Ж.", title="Абдулатипов Ж. — программирование, математика, машинное обучение",
        description="Блог Жавхарбека Абдулатипова: математика под капотом моделей, машинное обучение, компьютерное зрение, инженерия систем.",
        navLabel="Основная навигация", langLabel="Язык", footLabel="Ссылки в подвале", filterLabel="Фильтр по разделу",
        toDark="Тёмная тема", toLight="Светлая тема",
        navPosts="Статьи", navFields="Разделы", navResearch="Исследования", navAbout="Обо мне", allArticles="Все статьи",
        hero1="Мыслить строго.", hero2="Строить красиво.",
        heroSub="Программирование · Математика · Физика · Машинное обучение · Инженерия", ctaRead="Читать статьи",
        featKicker="Избранное · Машинное обучение", min="мин", read="Читать",
        fieldsSub="Шесть направлений, которые пересекаются чаще, чем кажется.",
        postsTitle="Записи", searchLabel="Поиск по статьям", searchPh="Например, сигмоида", all="Все",
        found="Найдено записей: ", reset="Сбросить фильтры", empty="Ничего не найдено. Попробуйте другой запрос или раздел.",
        formulaKicker="Формула недели",
        formulaText="Производная сигмоиды выражается через саму сигмоиду. Поэтому при обратном распространении ошибки экспоненту не считают заново: достаточно значения, уже вычисленного на прямом проходе.",
        derive="Разобрать вывод", researchTitle="Исследования и проекты",
        aboutKicker="Об авторе", aboutMore="Подробнее обо мне",
        about1="Здравствуйте. Меня зовут Жавхарбек Абдулатипов, я заместитель директора Департамента программных технологий Xalq Banki. Занимаюсь машинным обучением, компьютерным зрением и разработкой банковских систем.",
        news="Новость", openSite="Открыть сайт ↗", openMaterial="Открыть материал →",
        navMaterials="Материалы", materialsDek="Шпаргалки и справочники, которые я собираю по ходу работы: формулы, производные, примеры на числах и код. Здесь они хранятся целиком и дополняются.",
    ),
    "en": dict(
        brand="Abdulatipov J.", title="Abdulatipov J. — programming, mathematics, machine learning",
        description="Javharbek Abdulatipov's blog: the mathematics under the models, machine learning, computer vision, systems engineering.",
        navLabel="Main navigation", langLabel="Language", footLabel="Footer links", filterLabel="Filter by topic",
        toDark="Dark theme", toLight="Light theme",
        navPosts="Articles", navFields="Topics", navResearch="Research", navAbout="About me", allArticles="All articles",
        hero1="Think rigorously.", hero2="Build beautifully.",
        heroSub="Programming · Mathematics · Physics · Machine Learning · Engineering", ctaRead="Read articles",
        featKicker="Featured · Machine Learning", min="min", read="Read",
        fieldsSub="Six fields that overlap more often than you might think.",
        postsTitle="Posts", searchLabel="Search articles", searchPh="e.g. sigmoid", all="All",
        found="Posts found: ", reset="Reset filters", empty="Nothing found. Try another query or topic.",
        formulaKicker="Formula of the week",
        formulaText="The derivative of the sigmoid is expressed through the sigmoid itself. So backpropagation never recomputes the exponential: the value already obtained on the forward pass is enough.",
        derive="See the derivation", researchTitle="Research and projects",
        aboutKicker="About the author", aboutMore="More about me",
        about1="Hello. My name is Javharbek Abdulatipov, and I am Deputy Director of the Software Technologies Department at Xalq Banki. I work on machine learning, computer vision and banking systems development.",
        news="News", openSite="Open the site ↗", openMaterial="Open the material →",
        navMaterials="Materials", materialsDek="Cheat sheets and references I put together along the way: formulas, derivatives, worked numeric examples and code. They are kept here in full and keep growing.",
    ),
    "uz": dict(
        brand="Abdulatipov J.", title="Abdulatipov J. — dasturlash, matematika, mashinaviy o‘qitish",
        description="Javharbek Abdulatipov blogi: modellar ostidagi matematika, mashinaviy o‘qitish, kompyuter ko‘rishi, tizimlar muhandisligi.",
        navLabel="Asosiy navigatsiya", langLabel="Til", footLabel="Pastki havolalar", filterLabel="Bo‘lim bo‘yicha saralash",
        toDark="Qorong‘i mavzu", toLight="Yorug‘ mavzu",
        navPosts="Maqolalar", navFields="Bo‘limlar", navResearch="Tadqiqotlar", navAbout="Men haqimda", allArticles="Barcha maqolalar",
        hero1="Qat’iy fikrlash.", hero2="Go‘zal yaratish.",
        heroSub="Dasturlash · Matematika · Fizika · Mashinaviy o‘qitish · Muhandislik", ctaRead="Maqolalarni o‘qish",
        featKicker="Tanlangan · Mashinaviy o‘qitish", min="daq", read="O‘qish",
        fieldsSub="Oltita yo‘nalish — ular o‘ylaganingizdan ko‘ra tez-tez kesishadi.",
        postsTitle="Yozuvlar", searchLabel="Maqolalardan qidirish", searchPh="Masalan, sigmoida", all="Barchasi",
        found="Topilgan yozuvlar: ", reset="Filtrlarni tozalash", empty="Hech narsa topilmadi. Boshqa so‘rov yoki bo‘limni sinab ko‘ring.",
        formulaKicker="Hafta formulasi",
        formulaText="Sigmoidaning hosilasi sigmoidaning o‘zi orqali ifodalanadi. Shuning uchun teskari tarqatishda eksponenta qayta hisoblanmaydi: to‘g‘ri o‘tishda olingan qiymat kifoya.",
        derive="Isbotini ko‘rish", researchTitle="Tadqiqotlar va loyihalar",
        aboutKicker="Muallif haqida", aboutMore="Men haqimda batafsil",
        about1="Assalomu alaykum. Mening ismim Javharbek Abdulatipov, Xalq Banki Dasturiy texnologiyalar departamenti direktori o‘rinbosariman. Mashinaviy o‘qitish, kompyuter ko‘rishi va bank tizimlarini ishlab chiqish bilan shug‘ullanaman.",
        news="Yangilik", openSite="Saytni ochish ↗", openMaterial="Materialni ochish →",
        navMaterials="Materiallar", materialsDek="Ish jarayonida yig‘ib boradigan qo‘llanma va ma’lumotnomalarim: formulalar, hosilalar, sonli misollar va kod. Ular bu yerda to‘liq saqlanadi va to‘ldirib boriladi.",
    ),
}

TOPICS = [
    ("code", "{ }", False, {"ru": ["Программирование", "PHP, Java, Python, алгоритмы и структуры данных"], "en": ["Programming", "PHP, Java, Python, algorithms and data structures"], "uz": ["Dasturlash", "PHP, Java, Python, algoritmlar va ma’lumotlar tuzilmalari"]}),
    ("ml", "∇", False, {"ru": ["ML / AI", "Бустинг, нейросети, LLM, скоринг"], "en": ["ML / AI", "Boosting, neural networks, LLMs, scoring"], "uz": ["ML / AI", "Busting, neyron tarmoqlar, LLM, skoring"]}),
    ("math", "∑", False, {"ru": ["Математика", "Анализ, линейная алгебра, вероятность"], "en": ["Mathematics", "Analysis, linear algebra, probability"], "uz": ["Matematika", "Analiz, chiziqli algebra, ehtimollar"]}),
    ("phys", "ℏ", True, {"ru": ["Физика", "Механика, поля, квантовый мир"], "en": ["Physics", "Mechanics, fields, the quantum world"], "uz": ["Fizika", "Mexanika, maydonlar, kvant olami"]}),
    ("cv", "◎", False, {"ru": ["Компьютерное зрение", "Детекция, лица, Re-ID"], "en": ["Computer Vision", "Detection, faces, Re-ID"], "uz": ["Kompyuter ko‘rishi", "Aniqlash, yuzlar, Re-ID"]}),
    ("sys", "⇄", False, {"ru": ["Инженерия систем", "Архитектура, Linux, Docker"], "en": ["Systems Engineering", "Architecture, Linux, Docker"], "uz": ["Tizimlar muhandisligi", "Arxitektura, Linux, Docker"]}),
]

MONTHS = {
    "ru": ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "uz": ["yanvar", "fevral", "mart", "aprel", "may", "iyun", "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"],
}


def fmt_date(iso, lang):
    y, m, d = (int(x) for x in iso.split("-"))
    if lang == "uz":
        return f"{y}-yil {d}-{MONTHS[lang][m - 1]}"
    return f"{d} {MONTHS[lang][m - 1]} {y}"


# Posts. Add new ones here; the list on the home page is sorted newest first.
# A post with "url" is a news item: the row links to that page instead of an article.
# An absolute url opens another site; a relative one opens a page of this blog (a material).
FEATURED = "sigmoid"
COURSE_URL = "https://jakharbek.github.io/ml_gradient_boosting/"
POSTS = [
    dict(slug="sigmoid", topic="ml", date=DATE_ISO, mins=9,
         title={"ru": "Анатомия сигмоиды", "en": "Anatomy of the sigmoid", "uz": "Sigmoidaning anatomiyasi"},
         excerpt={"ru": "Две горизонтальные асимптоты и одна точка перегиба: что они значат для нейросети и почему 0.5 стал порогом решения.",
                  "en": "Two horizontal asymptotes and a single inflection point: what they mean for a neural network and why 0.5 became the decision threshold.",
                  "uz": "Ikki gorizontal asimptota va bitta burilish nuqtasi: ular neyron tarmoq uchun nimani anglatadi va nega 0.5 qaror chegarasiga aylandi."},
         figAria={"ru": "Сигмоида между асимптотами 0 и 1", "en": "The sigmoid between the asymptotes 0 and 1", "uz": "0 va 1 asimptotalar orasidagi sigmoida"}),
    dict(slug="gradient-boosting-course", topic="ml", date="2026-10-26",
         url=COURSE_URL,
         title={"ru": "Открыт курс «Градиентный бустинг по косточкам»",
                "en": "Course launched: «Gradient boosting, bone by bone»",
                "uz": "«Gradiyentli busting: mayda detallarigacha» kursi ochildi"},
         excerpt={"ru": "Интерактивный курс на русском: от первого дерева решений до XGBoost, LightGBM и CatBoost. Параметры меняются прямо на странице, код запускается на Python в браузере и повторяется в Jupyter.",
                  "en": "An interactive course in Russian: from the first decision tree to XGBoost, LightGBM and CatBoost. Change parameters right on the page, run the code in Python in the browser and repeat it in Jupyter.",
                  "uz": "Rus tilidagi interaktiv kurs: birinchi qaror daraxtidan XGBoost, LightGBM va CatBoost’gacha. Parametrlar sahifaning o‘zida o‘zgaradi, kod brauzerda Python’da ishlaydi va Jupyter’da takrorlanadi."}),
    dict(slug="ml-formulas-news", topic="ml", date="2026-10-28",
         url="materials/ml-formulas/",
         title={"ru": "Новый материал: шпаргалка формул нейросетей",
                "en": "New material: a cheat sheet of neural network formulas",
                "uz": "Yangi material: neyron tarmoq formulalari qo‘llanmasi"},
         excerpt={l: formulas.PAGE[l]["excerpt"] for l in LANGS}),
]
POST = {p["slug"]: p for p in POSTS}

# Materials: long-lived reference pages under <lang>/materials/<slug>/, newest first.
MATERIALS = [
    dict(slug="ml-formulas", topic="ml", date="2026-10-28", module=formulas),
]

# Research cards: [kicker, title, text] and an optional link as a fourth item.
RESEARCH = {
    "ru": [["ML · Курс", "Градиентный бустинг по косточкам", "Интерактивный курс от первого дерева решений до XGBoost, LightGBM и CatBoost: живые графики, Python в браузере и Jupyter-ноутбуки.", COURSE_URL],
           ["Метод · № 010556", "Модель «Шаршара»", "Научный математический метод, зарегистрированный в Центре интеллектуальной собственности при Министерстве юстиции Узбекистана."],
           ["CV · Реальное время", "Периметр, который видит", "Детекция людей, распознавание лиц и повторная идентификация между камерами."],
           ["Бизнес · Финансовый сектор", "Корпоративные системы", "Документооборот (DMS), управление кадрами (HRMS), создание и управление бизнес-процессами (BPMS), учёт и скоринг клиентов (CRM), корпоративные сайты и другие системы."]],
    "en": [["ML · Course", "Gradient boosting, bone by bone", "An interactive course in Russian, from the first decision tree to XGBoost, LightGBM and CatBoost: live charts, Python in the browser and Jupyter notebooks.", COURSE_URL],
           ["Method · No. 010556", "The «Sharshara» model", "A scientific mathematical method registered with the Intellectual Property Center under the Ministry of Justice of Uzbekistan."],
           ["CV · Real time", "A perimeter that sees", "Person detection, face recognition and re-identification across cameras."],
           ["Business · Financial sector", "Enterprise systems", "Document management (DMS), human resources (HRMS), business process design and management (BPMS), customer records and scoring (CRM), corporate websites and other systems."]],
    "uz": [["ML · Kurs", "Gradiyentli busting: mayda detallarigacha", "Rus tilidagi interaktiv kurs, birinchi qaror daraxtidan XGBoost, LightGBM va CatBoost’gacha: jonli grafiklar, brauzerda Python va Jupyter-daftarlar.", COURSE_URL],
           ["Usul · № 010556", "«Sharshara» modeli", "O‘zbekiston Adliya vazirligi huzuridagi Intellektual mulk markazida ro‘yxatdan o‘tgan ilmiy matematik usul."],
           ["CV · Real vaqt", "Ko‘ra oladigan perimetr", "Odamlarni aniqlash, yuzni tanish va kameralar orasida qayta identifikatsiya."],
           ["Biznes · Moliya sektori", "Korporativ tizimlar", "Hujjat aylanmasi (DMS), kadrlar boshqaruvi (HRMS), biznes-jarayonlarni yaratish va boshqarish (BPMS), mijozlarni hisobga olish va skoring (CRM), korporativ saytlar va boshqa tizimlar."]],
}

ABOUT = {
    "ru": dict(
        kicker="Обо мне", loc="Xalq Banki · Ташкент, Узбекистан",
        about2="По образованию программист-математик. В этом блоге записываю то, в чём разбираюсь сам: формулы, код и заметки по ходу работы.",
        experience="Опыт", education="Образование", degree="Бакалавр", fac1="Физико-математический факультет (Физмат)", fac2="Высшая школа точных наук",
        programme="Направление «Математика и информатика»", uni="Национальный педагогический университет Узбекистана им. Низами",
        stackTitle="Стек", contacts="Связаться со мной", write="Написать", now="н.в.",
        dep="Заместитель директора, Департамент программных технологий", xq="Внутренние системы банка, проектирование ПО и баз данных, высоконагруженные сервисы, код-ревью",
        oks="CRM, CMS и высоконагруженные сайты", fl="Фриланс", others=" и другие",
        stats=[["2-е место", "Евразийская олимпиада по информатике, 2022"], ["1-е место", "Best Soft Challenge, 2017 · Минцифры РУз"], ["13+ лет", "в разработке программного обеспечения"]],
        keys=["Языки", "Бэкенд", "Фронтенд", "Базы данных", "Очереди и интеграции", "Инфраструктура и DevOps", "Архитектура", "ML и анализ данных", "Компьютерное зрение", "LLM и NLP"],
        db="Реляционные (OLTP): PostgreSQL, MySQL, Oracle Database\nАналитические (OLAP): ClickHouse\nНереляционные (NoSQL): Redis, Memcached, MongoDB\nПоисковые: Elasticsearch\nВекторные: pgvector, Qdrant",
        arch="Микросервисы, CQRS, Event-driven, DDD, MVC, ООП, SOLID, паттерны проектирования",
        ml="CatBoost, scikit-learn, pandas, NumPy, PyTorch, кредитный скоринг",
        cv="OpenCV, YOLO, распознавание лиц, Re-ID, видеоаналитика в реальном времени",
        llm="LLM-инфраструктура, RAG, эмбеддинги, векторный поиск, инференс на своих серверах",
    ),
    "en": dict(
        kicker="About me", loc="Xalq Banki · Tashkent, Uzbekistan",
        about2="By education, I am a programmer-mathematician. In this blog I write about what I work through myself: formulas, code and notes along the way.",
        experience="Experience", education="Education", degree="Bachelor’s degree", fac1="Faculty of Physics and Mathematics", fac2="Higher School of Exact Sciences",
        programme="Programme: Mathematics and Computer Science", uni="Nizami National Pedagogical University of Uzbekistan",
        stackTitle="Stack", contacts="Get in touch", write="Email me", now="present",
        dep="Deputy Director, Software Technologies Department", xq="Internal banking systems, software and database design, high-load services, code review",
        oks="CRM, CMS and high-load websites", fl="Freelance", others=" and others",
        stats=[["2nd place", "Eurasian Olympiad in Informatics, 2022"], ["1st place", "Best Soft Challenge, 2017 · Ministry of Digital Technologies"], ["13+ years", "in software development"]],
        keys=["Languages", "Backend", "Frontend", "Databases", "Messaging & integration", "Infrastructure & DevOps", "Architecture", "ML & data analysis", "Computer vision", "LLM & NLP"],
        db="Relational (OLTP): PostgreSQL, MySQL, Oracle Database\nAnalytical (OLAP): ClickHouse\nNon-relational (NoSQL): Redis, Memcached, MongoDB\nSearch: Elasticsearch\nVector: pgvector, Qdrant",
        arch="Microservices, CQRS, event-driven, DDD, MVC, OOP, SOLID, design patterns",
        ml="CatBoost, scikit-learn, pandas, NumPy, PyTorch, credit scoring",
        cv="OpenCV, YOLO, face recognition, Re-ID, real-time video analytics",
        llm="LLM infrastructure, RAG, embeddings, vector search, self-hosted inference",
    ),
    "uz": dict(
        kicker="Men haqimda", loc="Xalq Banki · Toshkent, O‘zbekiston",
        about2="Ma’lumotim bo‘yicha dasturchi-matematikman. Ushbu blogda o‘zim o‘rganayotgan narsalarni yozib boraman: formulalar, kod va ish jarayonidagi qaydlar.",
        experience="Tajriba", education="Ta’lim", degree="Bakalavr", fac1="Fizika-matematika fakulteti", fac2="Aniq fanlar oliy maktabi",
        programme="Yo‘nalish: «Matematika va informatika»", uni="Nizomiy nomidagi O‘zbekiston milliy pedagogika universiteti",
        stackTitle="Stek", contacts="Men bilan bog‘lanish", write="Yozish", now="h.v.",
        dep="Direktor o‘rinbosari, Dasturiy texnologiyalar departamenti", xq="Bankning ichki tizimlari, dasturiy ta’minot va ma’lumotlar bazalarini loyihalash, yuqori yuklamali servislar, kod-review",
        oks="CRM, CMS va yuqori yuklamali saytlar", fl="Frilans", others=" va boshqalar",
        stats=[["2-o‘rin", "Informatika bo‘yicha Yevroosiyo olimpiadasi, 2022"], ["1-o‘rin", "Best Soft Challenge, 2017 · Raqamli texnologiyalar vazirligi"], ["13+ yil", "dasturiy ta’minot ishlab chiqishda"]],
        keys=["Tillar", "Backend", "Frontend", "Ma’lumotlar bazalari", "Navbatlar va integratsiya", "Infratuzilma va DevOps", "Arxitektura", "ML va ma’lumotlar tahlili", "Kompyuter ko‘rishi", "LLM va NLP"],
        db="Relyatsion (OLTP): PostgreSQL, MySQL, Oracle Database\nAnalitik (OLAP): ClickHouse\nNorelyatsion (NoSQL): Redis, Memcached, MongoDB\nQidiruv: Elasticsearch\nVektor: pgvector, Qdrant",
        arch="Mikroservislar, CQRS, Event-driven, DDD, MVC, OOP, SOLID, loyihalash patternlari",
        ml="CatBoost, scikit-learn, pandas, NumPy, PyTorch, kredit skoringi",
        cv="OpenCV, YOLO, yuzni tanish, Re-ID, real vaqtda videoanalitika",
        llm="LLM-infratuzilma, RAG, embeddinglar, vektor qidiruv, o‘z serverlarida inferens",
    ),
}

STACK_VALUES = [
    "PHP, Java, Python, JavaScript, TypeScript, C#, SQL, Bash",
    "Laravel, Symfony, Yii, CodeIgniter, Doctrine, Spring Boot, Spring Framework, Hibernate, FastAPI, .NET",
    "React",
    "{db}",
    "Apache Kafka, RabbitMQ, REST, gRPC, WebSocket",
    "Linux, Docker, Docker Compose, Kubernetes, Helm, Nginx, HAProxy, Git, GitLab CI, GitHub Actions, Jenkins, Ansible, Terraform, Bash, CI/CD, Prometheus, Grafana, ELK Stack, Zabbix, self-hosted",
    "{arch}", "{ml}", "{cv}", "{llm}",
]

SOCIAL = [("LinkedIn", "https://www.linkedin.com/in/javharbek-abdulatipov"), ("GitHub", "https://github.com/jakharbek"), ("Telegram", "https://t.me/javharbek16")]
EMAIL = "javhar_work@mail.ru"
PHONE = "+998 90 929-44-63"


def hreflang(path_fn):
    out = [f'  <link rel="alternate" hreflang="{l}" href="{path_fn(l)}">' for l in LANGS]
    out.append(f'  <link rel="alternate" hreflang="x-default" href="{path_fn("en")}">')
    return "\n".join(out)


def head(lang, title, desc, rel, page, og_type="website", extra=""):
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:image" content="{rel}assets/img/javharbek.png">
{hreflang(lambda l: f"{rel}{l}/{page}")}
  <link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
{THEME_BOOT}{FONTS}  <link rel="stylesheet" href="{rel}assets/css/site.css">
{extra}</head>
<body>
"""


def header(lang, rel, page, nav_items):
    s = SITE[lang]
    langs = " ".join(
        f'<a href="{rel}{l}/{page}" lang="{l}" hreflang="{l}"{" aria-current=\"true\"" if l == lang else ""}>{LANG_NAME[l]}</a>'
        for l in LANGS
    )
    nav = "\n    ".join(f'<a href="{href}"{" aria-current=\"page\"" if cur else ""}>{label}</a>' for label, href, cur in nav_items)
    labels = json.dumps({"toDark": s["toDark"], "toLight": s["toLight"]}, ensure_ascii=False).replace('"', "&quot;")
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{rel}{lang}/">{s['brand']}</a>
    <nav class="nav" aria-label="{s['navLabel']}">
    {nav}
    </nav>
    <div class="tools">
      <nav class="langs" aria-label="{s['langLabel']}">{langs}</nav>
      <button id="theme-toggle" class="theme-btn ghost" type="button" data-labels="{labels}" aria-label="{s['toDark']}">
        <svg class="sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="4.5"></circle><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path></svg>
        <svg class="moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"></path></svg>
      </button>
    </div>
  </div>
</header>
"""


def footer(lang, rel):
    s = SITE[lang]
    links = "\n    ".join(f'<a href="{u}">{n}</a>' for n, u in SOCIAL)
    return f"""<footer class="site-footer">
  <nav aria-label="{s['footLabel']}">
    <span>Javharbek Abdulatipov © 2026</span>
    <a href="{rel}{lang}/#posts">{s['navPosts']}</a>
    <a href="{rel}{lang}/materials/">{s['navMaterials']}</a>
    <a href="{rel}{lang}/about/">{s['navAbout']}</a>
    {links}
  </nav>
</footer>

<script src="{rel}assets/js/site.js" defer></script>
"""


def sigmoid_svg(aria):
    # The sigmoid itself, drawn as the featured figure: asymptotes in the accent, curve in the foreground.
    pts = []
    import math
    for i in range(0, 481, 8):
        x = -7 + 14 * i / 480
        y = 1 / (1 + math.exp(-x))
        pts.append(f"{i} {round(250 - 220 * y, 1)}")
    curve = "M" + " L".join(pts)
    return f"""<svg viewBox="0 0 480 280" role="img" aria-label="{aria}">
<line x1="0" y1="30" x2="480" y2="30" stroke="var(--accent)" stroke-width="1.5"></line>
<line x1="0" y1="250" x2="480" y2="250" stroke="var(--accent)" stroke-width="1.5"></line>
<line x1="240" y1="30" x2="240" y2="250" stroke="var(--curve)" stroke-dasharray="4 4"></line>
<path d="{curve}" fill="none" stroke="var(--fg)" stroke-width="2"></path>
<circle cx="240" cy="140" r="4" fill="var(--bg)" stroke="var(--fg)" stroke-width="2"></circle>
</svg>"""


def home(lang):
    s = SITE[lang]
    rel = "../"
    nav = [(s["navPosts"], "#posts", False), (s["navFields"], "#fields", False), (s["navMaterials"], "materials/", False), (s["navResearch"], "#research", False), (s["navAbout"], "about/", False)]
    feat = POST[FEATURED]
    chips = [f'<button type="button" class="chip" data-topic="all" aria-pressed="true"><span>{s["all"]}</span><small>{len(POSTS)}</small></button>']
    for tid, _, _, names in TOPICS:
        chips.append(f'<button type="button" class="chip" data-topic="{tid}" aria-pressed="false"><span>{names[lang][0]}</span><small>{sum(1 for p in POSTS if p["topic"] == tid)}</small></button>')
    topic_name = {tid: names[lang][0] for tid, _, _, names in TOPICS}
    def cta(p):
        if "url" not in p:
            return f"{p['mins']} {s['min']}"
        return s["openSite"] if p["url"].startswith("http") else s["openMaterial"]
    rows = "\n".join(
        f"""      <a class="row" href="{p.get('url') or p['slug'] + '/'}" data-topic="{p['topic']}">
        <span class="l"><span class="kicker">{s['news'] + ' · ' if 'url' in p else ''}{topic_name[p['topic']]}</span><span class="rt">{p['title'][lang]}</span><span class="ex">{p['excerpt'][lang]}</span></span>
        <span class="r"><time datetime="{p['date']}">{fmt_date(p['date'], lang)}</time><span>{cta(p)}</span></span>
      </a>""" for p in sorted(POSTS, key=lambda p: p["date"], reverse=True))
    tiles = "\n".join(
        f"""      <button type="button" class="tile" data-topic="{tid}"><span class="glyph math{' it' if it else ''}">{glyph}</span><span class="nm"><b>{names[lang][0]}</b><span>{names[lang][1]}</span></span><span class="cnt">{sum(1 for p in POSTS if p['topic'] == tid)}</span></button>"""
        for tid, glyph, it, names in TOPICS)
    link = lambda u: f'<a href="{u[0]}" class="ul">{s["openSite"]}</a>' if u else ""
    research = "\n".join(f'      <article><span class="kicker">{k}</span><h3>{t}</h3><p>{x}</p>{link(u)}</article>' for k, t, x, *u in RESEARCH[lang])
    return head(lang, s["title"], s["description"], rel, "") + header(lang, rel, "", nav) + f"""
<main>
<section id="top" class="hero">
  <svg class="bg" viewBox="0 0 520 560" aria-hidden="true"><path class="attractor" d="{ATTRACTOR}" fill="none" stroke="var(--curve)" stroke-width=".7" stroke-linejoin="round" stroke-linecap="round"></path></svg>
  <div class="hero-text rise">
    <h1><span>{s['hero1']}</span><span>{s['hero2']}</span></h1>
    <p class="hero-sub">{s['heroSub']}</p>
  </div>
  <div class="hero-cta rise">
    <a href="#posts" class="b1">{s['ctaRead']}</a>
    <a href="about/" class="b2">{s['navAbout']}</a>
  </div>
</section>

<section id="posts" class="posts">
  <div class="wrap-s">
    <div class="posts-head">
      <h2 class="sec">{s['postsTitle']}</h2>
      <div class="search">
        <label for="q">{s['searchLabel']}</label>
        <div class="field">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>
          <input id="q" type="search" placeholder="{s['searchPh']}" autocomplete="off">
        </div>
      </div>
    </div>
    <div class="chips" role="group" aria-label="{s['filterLabel']}">
      {''.join(chips)}
    </div>

    <a id="featured" class="featured" href="{feat['slug']}/">
      <span class="txt">
        <span class="kicker">{s['featKicker']}</span>
        <span class="ttl">{feat['title'][lang]}</span>
        <span class="sum">{feat['excerpt'][lang]}</span>
        <span class="meta"><time datetime="{feat['date']}">{fmt_date(feat['date'], lang)}</time><span>{feat['mins']} {s['min']}</span><span class="ul">{s['read']} →</span></span>
      </span>
      <span class="fig">
        {sigmoid_svg(feat['figAria'][lang])}
        <span class="formula math">σ(x) = 1 / (1 + e<sup>−x</sup>)</span>
      </span>
    </a>

    <div class="found">
      <span id="found" aria-live="polite" data-text="{s['found']}">{s['found']}{len(POSTS)}</span>
      <button id="reset" type="button" class="ul" hidden>{s['reset']}</button>
    </div>
    <div id="post-list" class="list">
{rows}
      <p id="empty" class="empty" hidden>{s['empty']}</p>
    </div>
  </div>
</section>

<section id="fields" class="fields">
  <div class="wrap-m">
    <div class="fields-head">
      <h2 class="sec">{s['navFields']}</h2>
      <p>{s['fieldsSub']}</p>
    </div>
    <div class="tiles">
{tiles}
    </div>
  </div>
</section>

<section class="formula-sec">
  <div class="wrap-xs">
    <span class="kicker">{s['formulaKicker']}</span>
    <div class="bigmath math" role="img" aria-label="σ′(x) = σ(x)(1 − σ(x))">
      <span>σ′(x)</span><span class="n">=</span><span>σ(x)</span><span class="n">(1 −</span><span>σ(x)</span><span class="n">)</span>
    </div>
    <p>{s['formulaText']}</p>
    <a href="sigmoid/#s3" class="ul">{s['derive']}</a>
  </div>
</section>

<section id="research" class="research">
  <div class="wrap-m">
    <h2 class="sec">{s['researchTitle']}</h2>
    <div class="cards">
{research}
    </div>
  </div>
</section>

<section id="about" class="about-teaser on-bg2">
  <div class="wrap-s">
    <img src="{rel}assets/img/javharbek.png" alt="Javharbek Abdulatipov" width="200" height="200">
    <div class="txt">
      <span class="kicker">{s['aboutKicker']}</span>
      <h2>Javharbek Abdulatipov</h2>
      <p>{s['about1']}</p>
      <div class="btns">
        <a href="about/" class="b1">{s['aboutMore']}</a>
        <a href="https://t.me/javharbek16" class="b2">Telegram</a>
      </div>
    </div>
  </div>
</section>
</main>

""" + footer(lang, rel) + "</body>\n</html>\n"


def article(lang):
    s, a, p = SITE[lang], ARTICLE[lang], POST["sigmoid"]
    rel = "../../"
    nav = [(s["allArticles"], f"{rel}{lang}/#posts", False), (s["navMaterials"], f"{rel}{lang}/materials/", False), (s["navAbout"], f"{rel}{lang}/about/", False)]
    rows = "\n".join(f"        <tr><td>{x}</td><td>{y}</td><td>{g}</td></tr>" for x, y, g in TABLE_ROWS)
    summary = "\n".join(f"      <li>{li}</li>" for li in a["sum"])
    toc = "\n".join(f'      <a href="#s{i+1}">{h}</a>' for i, h in enumerate(a["toc"]))
    tags = "".join(f'<a href="{rel}{lang}/#posts">{t}</a>' for t in a["tags"])
    return head(lang, f"{p['title'][lang]} — {s['brand']}", a["meta_desc"], rel, "sigmoid/", "article") + header(lang, rel, "sigmoid/", nav) + f"""<div class="progress" aria-hidden="true"><div id="progress"></div></div>

<main>
<section class="art-head wrap-xs">
  <span class="kicker">{a['kicker']}</span>
  <h1>{p['title'][lang]}</h1>
  <p class="dek">{a['dek']}</p>
  <div class="author">
    <img src="{rel}assets/img/javharbek.png" alt="" width="44" height="44">
    <span class="who"><b>Javharbek Abdulatipov</b><span><time datetime="{p['date']}">{fmt_date(p['date'], lang)}</time> · {p['mins']} {s['min']}</span></span>
  </div>
</section>

<div class="art-body wrap-m">
  <aside class="toc" aria-label="{a['tocTitle']}">
    <span>{a['tocTitle']}</span>
    <nav>
{toc}
    </nav>
  </aside>

  <article class="article">
    <h2 id="s1">{a['h_road']}</h2>
    <p>{a['p_road1']}</p>
    <p>{a['p_road2']}</p>

    <div class="eq"><div class="math">
      <span>σ(x)</span><span class="n">=</span>
      <span class="frac"><span class="n">1</span><span><span class="n">1 + </span>e<sup>−x</sup></span></span>
    </div><span class="num">(1)</span></div>

    <figure class="figure">
      <canvas id="fig-asymptotes" width="1600" height="760" aria-label="{a['fig1_aria']}"></canvas>
      <div class="figure-controls">
        <label>{a['fig1_label']}
          <input type="range" id="range" min="4" max="40" step="1" value="6" aria-label="{a['fig1_aria_input']}">
          <output id="range-out" for="range">±6</output>
        </label>
      </div>
      <figcaption class="figcaption">{a['fig1_cap']}</figcaption>
    </figure>

    <p>{a['p_table']}</p>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>x</th><th>σ(x)</th><th>1 − σ(x)</th></tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>
    <p>{a['p_never']}</p>

    <h2 id="s2">{a['h_steep']}</h2>
    <p>{a['p_steep1']}</p>
    <p>{a['p_steep2']}</p>

    <figure class="figure">
      <canvas id="fig-slope" width="1600" height="900" aria-label="{a['fig2_aria']}"></canvas>
      <div class="figure-controls">
        <label>{a['fig2_label']}
          <input type="range" id="pos" min="-6" max="6" step="0.1" value="0" aria-label="{a['fig2_aria_input']}">
          <output id="pos-out" for="pos">0.0</output>
        </label>
        <span>σ(x) = <span class="value" id="sig-out">0.5000</span></span>
        <span>σ′(x) = <span class="value" id="slope-out">0.2500</span></span>
      </div>
      <figcaption class="figcaption">{a['fig2_cap']}</figcaption>
    </figure>

    <h2 id="s3">{a['h_deriv']}</h2>
    <p>{a['p_deriv']}</p>
    <div class="eq"><div class="math">
      <span>σ′(x)</span><span class="n">=</span><span>σ(x)</span><span class="n">(1 −</span><span>σ(x)</span><span class="n">)</span>
    </div><span class="num">(2)</span></div>
    <p>{a['p_deriv2']}</p>

    <h2 id="s4">{a['h_nn']}</h2>
    <p>{a['p_nn0']}</p>
    <p>{a['p_nn1']}</p>
    <p>{a['p_nn2']}</p>
    <p>{a['p_nn3']}</p>

    <section class="takeaway" id="s5">
      <h2>{a['h_sum']}</h2>
      <ul>
{summary}
      </ul>
    </section>

    <div class="tags">{tags}</div>
  </article>
</div>
</main>

""" + footer(lang, rel) + f'<script src="{rel}assets/js/sigmoid.js" defer></script>\n</body>\n</html>\n'


def about(lang):
    s, a = SITE[lang], ABOUT[lang]
    rel = "../../"
    nav = [(s["allArticles"], f"{rel}{lang}/#posts", False), (s["navMaterials"], f"{rel}{lang}/materials/", False), (s["navAbout"], "./", True)]
    stats = "\n".join(f"      <div><b>{b}</b><span>{t}</span></div>" for b, t in a["stats"])
    jobs = [
        ("2026 — " + a["now"], a["dep"], "Xalq Banki", ""),
        ("2020 — 2026", "Software Engineer, Team Lead", "Xalq Banki · PHP + Java", a["xq"]),
        ("2018 — 2020", "Software Engineer, Team Lead", "OKS Technologies", a["oks"]),
        ("2017 — 2018", "Software Engineer, Team Lead", "Phoenix Systems", ""),
        ("2016", "Software Engineer", "Sirdaryo Soft", ""),
        ("2013 — 2015", "Software Engineer", a["fl"], ""),
    ]
    jobs_html = "\n".join(
        f'      <div class="job"><span class="y">{y}</span><span class="d"><b>{r}</b><span>{o}</span>{f"<small>{d}</small>" if d else ""}</span></div>'
        for y, r, o, d in jobs)
    vals = [v.format(**a) for v in STACK_VALUES]
    stack = "\n".join(f'        <div class="k"><span>{k}</span><span>{v}{a["others"]}</span></div>' for k, v in zip(a["keys"], vals))
    social = "".join(f'<a href="{u}" class="b2">{n}</a>' for n, u in SOCIAL if n != "Telegram")
    return head(lang, f"{s['navAbout']} — {s['brand']}", s["about1"], rel, "about/", "profile") + header(lang, rel, "about/", nav) + f"""
<main>
<section class="about-hero wrap-m">
  <img src="{rel}assets/img/javharbek.png" alt="Javharbek Abdulatipov" width="300" height="300">
  <div class="txt">
    <span class="kicker">{a['kicker']}</span>
    <h1>Javharbek Abdulatipov</h1>
    <div class="roles"><span>Deputy Director</span><i aria-hidden="true">|</i><span>Senior AI/ML Engineer</span><i aria-hidden="true">|</i><span>Senior Software Engineer</span></div>
    <span class="loc">{a['loc']}</span>
    <div class="bio"><p>{s['about1']}</p><p>{a['about2']}</p></div>
  </div>
</section>

<section class="wrap-m">
  <div class="stats">
{stats}
  </div>
</section>

<section class="about-grid wrap-m">
  <div>
    <h2>{a['experience']}</h2>
{jobs_html}
  </div>
  <div class="right-col">
    <div class="edu">
      <h2>{a['education']}</h2>
      <b>{a['degree']}</b>
      <span>{a['fac1']} → {a['fac2']}</span>
      <span>{a['programme']}</span>
      <span class="uni">{a['uni']}</span>
    </div>
    <div class="stack">
      <h2>{a['stackTitle']}</h2>
{stack}
    </div>
  </div>
</section>

<section class="contacts on-bg2">
  <div class="wrap-s">
    <h2>{a['contacts']}</h2>
    <div class="btns">
      <a href="https://t.me/javharbek16" class="b1">Telegram</a>
      <a href="mailto:{EMAIL}" class="b2">{a['write']}</a>
      <a href="tel:{PHONE.replace(' ', '').replace('-', '')}" class="b2">{PHONE}</a>
      {social}
    </div>
  </div>
</section>
</main>

""" + footer(lang, rel) + "</body>\n</html>\n"


KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.22/dist"


def tr(v, lang):
    """A text that differs by language is a dict; anything else is shared."""
    return v[lang] if isinstance(v, dict) else v


def tex(src, display=True):
    # KaTeX renders it in the browser; without KaTeX the TeX source stays readable.
    d = "$$" if display else "$"
    return f"{d}{html.escape(src, quote=False)}{d}"


def materials_nav(lang, rel, current):
    s = SITE[lang]
    return [(s["allArticles"], f"{rel}{lang}/#posts", False), (s["navMaterials"], f"{rel}{lang}/materials/", current), (s["navAbout"], f"{rel}{lang}/about/", False)]


def materials_index(lang):
    s = SITE[lang]
    rel = "../../"
    topic_name = {tid: names[lang][0] for tid, _, _, names in TOPICS}
    rows = "\n".join(
        f"""      <a class="row" href="{m['slug']}/">
        <span class="l"><span class="kicker">{topic_name[m['topic']]}</span><span class="rt">{m['module'].PAGE[lang]['title']}</span><span class="ex">{m['module'].PAGE[lang]['excerpt']}</span></span>
        <span class="r"><time datetime="{m['date']}">{fmt_date(m['date'], lang)}</time><span>{sum(1 for g in m['module'].GROUPS for c in g['cards'] if c['tex'])} {m['module'].PAGE[lang]['count']}</span></span>
      </a>""" for m in sorted(MATERIALS, key=lambda m: m["date"], reverse=True))
    return head(lang, f"{s['navMaterials']} — {s['brand']}", s["materialsDek"], rel, "materials/") + header(lang, rel, "materials/", materials_nav(lang, rel, True)) + f"""
<main>
<section class="art-head wrap-xs">
  <span class="kicker">{s['brand']}</span>
  <h1>{s['navMaterials']}</h1>
  <p class="dek">{s['materialsDek']}</p>
</section>

<section class="wrap-s mat-list">
  <div class="list">
{rows}
  </div>
</section>
</main>

""" + footer(lang, rel) + "</body>\n</html>\n"


def formula_card(c, lang):
    f = formulas
    rows = []
    for kind, label, body in c["rows"]:
        lab = f'<span class="lab">{f.LABEL[label][lang]}</span>'
        if kind == "fx":
            rows.append(f'<div class="fc-row">{lab}<div class="fx">{tex(body)}</div></div>')
        elif kind == "code":
            rows.append(f'<div class="fc-row">{lab}<pre><code>{html.escape(body)}</code></pre></div>')
        else:
            rows.append(f'<div class="fc-row">{lab}<p>{body[lang]}</p></div>')
    rows.append(f'<div class="fc-key">{c["key"][lang]}</div>')
    body = "\n          ".join(rows)
    shown = f'<div class="fc-formula">{tex(c["tex"])}</div>' if c["tex"] else f'<p class="fc-lead">{c["lead"][lang]}</p>'
    if c["id"] in FORMULA_IDS:
        shown += f'\n        <a class="ul fc-full" href="{c["id"]}/">{f.PAGE[lang]["full"]}</a>'
    return f"""      <article class="fcard" id="{c['id']}">
        <div class="fc-top"><h3><span>{tr(c['name'], lang)}</span><small>{c['alt'][lang]}</small></h3><span class="fc-tag mono">{tr(c['tag'], lang)}</span></div>
        {shown}
        <details>
          <summary>{f.PAGE[lang]['more']}</summary>
          <div class="fc-body">
          {body}
          </div>
        </details>
      </article>"""


def material_formulas(lang):
    s, f = SITE[lang], formulas
    pg = f.PAGE[lang]
    m = next(x for x in MATERIALS if x["slug"] == "ml-formulas")
    rel = "../../../"
    page = "materials/ml-formulas/"
    kinds = {"act": {"silu", "gelu"}, "loss": {"triplet", "focal"}, "opt": {"sgd"}}
    ids = {g["id"]: [c["id"] for c in g["cards"]] for g in f.GROUPS}
    counts = [sum(1 for g in f.GROUPS for c in g["cards"] if c["tex"]),
              len(ids["act"]) + len(kinds["act"]), len(ids["reg"]) + len(ids["cls"]) + len(kinds["loss"]), len(ids["opt"]) + len(kinds["opt"])]
    stats = "".join(f"<span><b>{n}</b> {t}</span>" for n, t in zip(counts, pg["stats"]))
    chips = [f'<button type="button" class="chip" data-group="all" aria-pressed="true"><span>{pg["all"]}</span></button>']
    chips += [f'<button type="button" class="chip" data-group="{g["id"]}" aria-pressed="false"><span>{g["title"][lang]}</span><small>{len(g["cards"])}</small></button>' for g in f.GROUPS]
    groups = []
    for g in f.GROUPS:
        cards = "\n".join(formula_card(c, lang) for c in g["cards"])
        route = f'\n    <p class="fc-route">{g["route"][lang]}</p>' if "route" in g else ""
        groups.append(f"""  <section class="fgroup{' upcoming' if g.get('upcoming') else ''}" id="{g['id']}" data-group="{g['id']}">
    <div class="fg-head"><span class="glyph math" aria-hidden="true">{g['glyph']}</span><h2>{g['title'][lang]}</h2><p>{g['note'][lang]}</p></div>
    <div class="fgrid">
{cards}
    </div>{route}
  </section>""")
    links = "\n".join(f"      <li>{li}</li>" for li in pg["links"])
    extra = (f'  <link rel="stylesheet" href="{KATEX}/katex.min.css">\n'
             f'  <script defer src="{KATEX}/katex.min.js"></script>\n'
             f'  <script defer src="{KATEX}/contrib/auto-render.min.js"></script>\n')
    return head(lang, f"{pg['title']} — {s['brand']}", pg["meta_desc"], rel, page, "article", extra) + header(lang, rel, page, materials_nav(lang, rel, False)) + f"""
<main class="material">
<section class="art-head wrap-xs">
  <span class="kicker">{pg['kicker']}</span>
  <h1>{pg['title']}</h1>
  <p class="dek">{pg['dek']}</p>
  <div class="author">
    <img src="{rel}assets/img/javharbek.png" alt="" width="44" height="44">
    <span class="who"><b>Javharbek Abdulatipov</b><span><time datetime="{m['date']}">{fmt_date(m['date'], lang)}</time></span></span>
  </div>
  <div class="mat-stats">{stats}</div>
</section>

<div class="wrap-s">
  <div class="mat-tools">
    <div class="chips" role="group" aria-label="{pg['filter']}">{''.join(chips)}</div>
    <div class="mat-btns"><button type="button" class="b2" data-expand="1">{pg['expand']}</button><button type="button" class="b2" data-expand="0">{pg['collapse']}</button></div>
  </div>

{chr(10).join(groups)}

  <section class="takeaway mat-links">
    <h2>{pg['links_h']}</h2>
    <ul>
{links}
    </ul>
  </section>

  <p class="mat-back"><a class="ul" href="../">← {pg['back']}</a></p>
</div>
</main>

""" + footer(lang, rel) + f'<script src="{rel}assets/js/materials.js" defer></script>\n</body>\n</html>\n'



# ---------- formula pages: materials/ml-formulas/<id>/ ----------
# Each page is a module tools/formulas/<id>.py with META and SECTIONS (see tools/formulas/README.md).
FORMULA_DIR = ROOT / "tools" / "formulas"
FORMULA_IDS = sorted(p.stem for p in FORMULA_DIR.glob("*.py") if not p.stem.startswith("_"))
CARD_ORDER = [c["id"] for g in formulas.GROUPS for c in g["cards"]]
CARD = {c["id"]: (g, c) for g in formulas.GROUPS for c in g["cards"]}

FX_UI = {
    "ru": dict(sheet="Шпаргалка", prev="← Предыдущая формула", next="Следующая формула →", toc="Содержание", min="мин чтения", quiz_right="Верно.", quiz_wrong="Не совсем."),
    "en": dict(sheet="Cheat sheet", prev="← Previous formula", next="Next formula →", toc="Contents", min="min read", quiz_right="Correct.", quiz_wrong="Not quite."),
    "uz": dict(sheet="Qo‘llanma", prev="← Oldingi formula", next="Keyingi formula →", toc="Mundarija", min="daq o‘qish", quiz_right="To‘g‘ri.", quiz_wrong="Unchalik emas."),
}


def load_formula(fid):
    spec = importlib.util.spec_from_file_location(f"formula_{fid.replace('-', '_')}", FORMULA_DIR / f"{fid}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def attr_json(data):
    return html.escape(json.dumps(data, ensure_ascii=False), quote=True)


def render_blocks(blocks, lang, ind="    "):
    out = []
    for b in blocks:
        kind = b[0]
        if kind == "p":
            out.append(f"<p>{b[1]}</p>")
        elif kind == "h3":
            out.append(f"<h3>{b[1]}</h3>")
        elif kind == "eq":
            out.append(f'<div class="eqd">{tex(b[1])}</div>')
        elif kind == "symbols":
            rows = "".join(f"<dt>{tex(t, False)}</dt><dd>{d}</dd>" for t, d in b[1])
            out.append(f'<dl class="symbols">{rows}</dl>')
        elif kind == "viz":
            name, cfg, cap = b[1], b[2], b[3] if len(b) > 3 else ""
            capt = f"<figcaption>{cap}</figcaption>" if cap else ""
            out.append(f'<figure class="viz"><div class="fv" data-viz="{name}" data-config="{attr_json(cfg)}"></div>{capt}</figure>')
        elif kind == "callout":
            k, title, body = b[1], b[2], b[3]
            out.append(f'<div class="callout {k}">{f"<b>{title}</b>" if title else ""}<p>{body}</p></div>')
        elif kind == "code":
            out.append(f'<pre class="code"><span class="lang">{b[1]}</span><code>{html.escape(b[2])}</code></pre>')
        elif kind == "table":
            heads, rows = b[1], b[2]
            num = set((b[3] or {}).get("num", [])) if len(b) > 3 else set()
            th = "".join(f'<th{" class=num" if i in num else ""}>{h}</th>' for i, h in enumerate(heads))
            trs = "".join("<tr>" + "".join(f'<td{" class=num" if i in num else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
            out.append(f'<div class="table-wrap"><table class="data"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>')
        elif kind in ("ul", "ol"):
            out.append(f'<{kind} class="flist">' + "".join(f"<li>{i}</li>" for i in b[1]) + f"</{kind}>")
        elif kind == "deep":
            out.append(f'<details class="deep"><summary>{b[1]}</summary><div class="deep-body">\n' + render_blocks(b[2], lang, ind + "  ") + f"\n{ind}</div></details>")
        elif kind == "quiz":
            qs = []
            for i, q in enumerate(b[1]):
                ans = q["answer"]
                opts = "".join(f'<button type="button" data-ok="{1 if j == ans else 0}">{o}</button>' for j, o in enumerate(q["options"]))
                qs.append(f'<fieldset class="q"><legend>{i + 1}. {q["q"]}</legend><div class="opts">{opts}</div><div class="explain" hidden>{q["explain"]}</div></fieldset>')
            ui = FX_UI[lang]
            out.append(f'<div class="quiz" data-right="{ui["quiz_right"]}" data-wrong="{ui["quiz_wrong"]}">' + "".join(qs) + "</div>")
        else:
            raise ValueError(f"unknown block {kind!r}")
    return "\n".join(ind + x for x in out)


def formula_page(lang, fid, mod):
    s, ui, pg = SITE[lang], FX_UI[lang], formulas.PAGE[lang]
    meta, sections = mod.META, mod.SECTIONS[lang]
    group, card = CARD[fid]
    rel = "../../../../"
    page = f"materials/ml-formulas/{fid}/"
    nav = [(s["allArticles"], f"{rel}{lang}/#posts", False), (s["navMaterials"], f"{rel}{lang}/materials/", False), (ui["sheet"], "../", False), (s["navAbout"], f"{rel}{lang}/about/", False)]
    toc = "\n".join(f'      <a href="#{sec["id"]}"><span class="n">{i + 1}</span>{sec["title"]}</a>' for i, sec in enumerate(sections))
    body = "\n\n".join(f'    <h2 id="{sec["id"]}">{sec["title"]}</h2>\n' + render_blocks(sec["blocks"], lang) for sec in sections)
    order = [x for x in CARD_ORDER if x in FORMULA_IDS]
    i = order.index(fid)
    def nav_card(other, cls, label):
        _, c = CARD[other]
        return f'<a class="{cls}" href="../{other}/"><span class="kicker">{label}</span><span class="big">{tr(c["name"], lang)}</span><span class="kicker">{c["alt"][lang]}</span></a>'
    links = []
    if i > 0:
        links.append(nav_card(order[i - 1], "prev", ui["prev"]))
    if i + 1 < len(order):
        links.append(nav_card(order[i + 1], "next", ui["next"]))
    extra = (f'  <link rel="stylesheet" href="{KATEX}/katex.min.css">\n'
             f'  <script defer src="{KATEX}/katex.min.js"></script>\n'
             f'  <script defer src="{KATEX}/contrib/auto-render.min.js"></script>\n'
             f'  <script defer src="{rel}assets/js/viz.js"></script>\n'
             f'  <script defer src="{rel}assets/js/formulas/{fid}.js"></script>\n'
             f'  <script defer src="{rel}assets/js/materials.js"></script>\n')
    title = meta["title"][lang]
    return head(lang, f"{title} — {pg['title']} — {s['brand']}", html.escape(meta["description"][lang], quote=True), rel, page, "article", extra) + header(lang, rel, page, nav) + f"""<div class="progress" aria-hidden="true"><div id="progress"></div></div>

<main class="material fx-page">
<section class="art-head wrap-xs">
  <span class="kicker"><a class="ul" href="../">{pg['title']}</a> · {group['title'][lang]}</span>
  <h1>{title}</h1>
  <p class="dek">{meta['dek'][lang]}</p>
  <div class="author">
    <img src="{rel}assets/img/javharbek.png" alt="" width="44" height="44">
    <span class="who"><b>Javharbek Abdulatipov</b><span><time datetime="{meta['date']}">{fmt_date(meta['date'], lang)}</time> · {meta['minutes']} {ui['min']}</span></span>
  </div>
</section>

<div class="art-body wrap-m">
  <aside class="toc" aria-label="{ui['toc']}">
    <span>{ui['toc']}</span>
    <nav>
{toc}
    </nav>
  </aside>

  <article class="article">
    <div class="fx-hero">{tex(meta['hero'])}</div>

{body}
  </article>
</div>

<nav class="fx-nav" aria-label="{ui['sheet']}">
  <div class="wrap-m">
    {chr(10).join(links)}
  </div>
</nav>
</main>

""" + footer(lang, rel) + "</body>\n</html>\n"


def build_formula(fid):
    mod = load_formula(fid)
    assert fid in CARD, f"{fid}: no card with this id in content_formulas.py"
    for lang in LANGS:
        d = ROOT / lang / "materials" / "ml-formulas" / fid
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(formula_page(lang, fid, mod), encoding="utf-8")

ROOT_INDEX = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Javharbek Abdulatipov</title>
  <meta name="robots" content="noindex">
  <link rel="alternate" hreflang="ru" href="ru/">
  <link rel="alternate" hreflang="en" href="en/">
  <link rel="alternate" hreflang="uz" href="uz/">
  <link rel="alternate" hreflang="x-default" href="en/">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <script>
    (function () {
      var supported = ["ru", "en", "uz"], pick = "en";
      try {
        var saved = localStorage.getItem("lang");
        if (supported.indexOf(saved) !== -1) pick = saved;
        else {
          var langs = navigator.languages || [navigator.language || ""];
          for (var i = 0; i < langs.length; i++) {
            var code = String(langs[i]).slice(0, 2).toLowerCase();
            if (supported.indexOf(code) !== -1) { pick = code; break; }
          }
        }
      } catch (e) {}
      location.replace(pick + "/");
    })();
  </script>
  <style>
    body{margin:0;font-family:"Manrope",system-ui,sans-serif;background:#fff;color:#171A20;padding:0 24px}
    @media (prefers-color-scheme:dark){body{background:#0F1012;color:#EDEDED}}
    main{max-width:1200px;margin:0 auto;padding:20vh 0;text-align:center}
    h1{font-size:clamp(32px,6vw,56px);font-weight:500;letter-spacing:-.01em;margin:0 0 24px}
    nav{display:flex;gap:32px;justify-content:center;font-size:16px;font-weight:500}
    a{color:inherit;text-decoration:none}a:hover{text-decoration:underline;text-underline-offset:.18em}
  </style>
</head>
<body>
<main>
  <h1>Javharbek Abdulatipov</h1>
  <nav><a href="ru/" lang="ru">Русский</a><a href="en/" lang="en">English</a><a href="uz/" lang="uz">O‘zbekcha</a></nav>
</main>
</body>
</html>
"""


def main():
    # python3 tools/build.py --only <id>  builds just one formula page (all three languages)
    if "--only" in sys.argv:
        fid = sys.argv[sys.argv.index("--only") + 1]
        build_formula(fid)
        print(f"built: {fid} in", ", ".join(f"{l}/materials/ml-formulas/{fid}/" for l in LANGS))
        return
    for fid in FORMULA_IDS:
        build_formula(fid)
    for lang in LANGS:
        pages = {"": home, "sigmoid": article, "about": about, "materials": materials_index, "materials/ml-formulas": material_formulas}
        for sub, render in pages.items():
            (ROOT / lang / sub).mkdir(parents=True, exist_ok=True)
            (ROOT / lang / sub / "index.html").write_text(render(lang), encoding="utf-8")
    (ROOT / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
    print("built:", ", ".join(f"{l}/" + "{" + ", ".join(pages) + "}" for l in LANGS), "+ index.html,", len(FORMULA_IDS), "formula pages")


if __name__ == "__main__":
    main()
