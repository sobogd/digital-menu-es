# digital-menu (QRgine / Коргин)

Русскоязычный SEO-лендинг: QR-меню + резервации. Статика, ноль JS.
Продукт: один тариф, всё включено — 7 €/мес (годовая) / 9 €/мес (помесячная), за ресторан.
Вход и демо — заглушки (SIGNUP_URL/DEMO_URL в seo/config.py).

## Структура

- `seo/config.py` — бренд, BASE_URL, тариф (PLAN), группы. Смена имени/базы/цены = правка здесь + генерация.
- `seo/templates.py` — шаблоны (head/header/footer/JSON-LD/страницы).
- `seo/gen.py` — генератор: `python3 seo/gen.py`
- `seo/data/**.json` — весь контент: home, ceny, faq, hubs + группы
  `types/` (10), `features/` (8), `articles/` (8), `trust/` (4)
- Сгенерированное (коммитится): `index.html`, `<slug>/index.html` × 32, 3 хаба, `sitemap.xml`, `robots.txt`
- `assets/logo.svg` — знак (корги с QR-ушком), `assets/wordmark.svg` — знак + текст

## Генерация

```bash
python3 seo/gen.py   # пересобирает все 36 страниц + sitemap + robots
```

Список страниц — в `sitemap.xml`. Canonical-базу меняют в `seo/config.py:BASE_URL`
(сейчас IP:8080; домен qr-gi.com/qrgine.com — решим, одна строка).

## Деплой

`bash deploy.sh` (lock → git pull → rsync на VPS → health :8080).
nginx vhost — `nginx/digital-menu-es.conf` (try_files $uri $uri/ — чистые URL без .html).
