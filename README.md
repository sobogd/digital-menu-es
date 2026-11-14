# digital-menu (QRgine / Коргин)

Русскоязычный SEO-лендинг: QR-меню + резервации + заказы/KDS. Статика, ноль JS.
Продукт и админка — репо `iq-rest` (база, дашборд, PWA); брендинг QRgine.

## Структура

- `seo/config.py` — бренд, BASE_URL, модули/цены, группы. Смена имени или базы = правка здесь + генерация.
- `seo/templates.py` — шаблоны (head/header/footer/JSON-LD/страницы).
- `seo/gen.py` — генератор: `python3 seo/gen.py`
- `seo/data/**.json` — весь контент: home, ceny, faq, hubs + группы
  `types/` (10), `features/` (10), `cities/` (15), `articles/` (8), `trust/` (4)
- Сгенерированное (коммитится): `index.html`, `<slug>/index.html` × 51, 4 хаба, `sitemap.xml`, `robots.txt`
- `assets/logo.svg` — знак (корги с QR-ушком), `assets/wordmark.svg` — знак + текст

## Генерация

```bash
python3 seo/gen.py   # пересобирает все 54 страницы + sitemap + robots
```

Список страниц — в `sitemap.xml`. Canonical-базу меняют в `seo/config.py:BASE_URL` (сейчас IP:8080, домен появится — одна строка).

## Деплой

Виде прежнего: `bash deploy.sh` (lock → git pull → rsync на VPS → health :8080).
nginx vhost — `nginx/digital-menu-es.conf` (try_files $uri $uri/ — чистые URL без .html).

## Ссылки на продукт

- Sign-up: https://dashboard.iq-rest.com
- Демо-меню: https://love-eatery.iq-rest.com
- Юр. страницы: iq-rest.com/ru/{terms,privacy,cookies}
