# my-blog

Личный блог [javharbek.uz](https://javharbek.uz): заметки о машинном обучении, инфраструктуре и математике.

Статический сайт без сборки и зависимостей: HTML, CSS и немного JavaScript для интерактивных графиков.

## Структура

```
index.html                 главная, список записей
posts/<slug>/index.html    запись
posts/<slug>/*.js          интерактив конкретной записи
assets/css/site.css        единый стиль
assets/favicon.svg
.github/workflows/pages.yml деплой на GitHub Pages при пуше в main
```

## Новая запись

1. Скопируйте `posts/sigmoid/index.html` в `posts/<slug>/index.html`, замените текст.
2. Добавьте строку в список `.posts` в `index.html`.
3. Запушьте в `main`; GitHub Pages обновится автоматически.

## Локально

```
python3 -m http.server 8000
```

и откройте http://localhost:8000.
