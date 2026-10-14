# my-blog

Личный блог [javharbek.uz](https://javharbek.uz) на трёх языках: русский, o‘zbekcha, English.

Статический сайт без зависимостей: HTML, CSS и немного JavaScript для интерактивных графиков. Готовые страницы лежат в репозитории, GitHub Pages ничего не собирает.

## Структура

```
index.html                 выбор языка (по языку браузера, затем по сохранённому выбору)
ru/ uz/ en/                главная каждого языка, список записей
ru/<slug>/index.html       запись (аналогично uz/, en/)
assets/css/site.css        единый стиль
assets/js/sigmoid.js       интерактивные графики записи о сигмоиде
assets/js/lang.js          запоминает выбранный язык
tools/build.py             генератор языковых версий из одного шаблона
.github/workflows/pages.yml деплой на GitHub Pages при пуше в main
```

## Новая запись

Тексты всех языков живут в `tools/build.py`. Добавьте запись в словари `SITE` и `ARTICLE`, затем:

```
python3 tools/build.py
```

и закоммитьте результат вместе со скриптом. Можно и без генератора: скопировать любую `*/sigmoid/index.html` и править руками, главное сохранить взаимные `hreflang`.

## Локально

```
python3 -m http.server 8000
```

и откройте http://localhost:8000.
