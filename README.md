# digital-menu (qrgi)

Русскоязычный SEO-лендинг: QR-меню + резервации. Статика, ноль JS.
Продукт: три тарифа за ресторан — 0 € до 120 сканов в месяц, 5 € до 1000, 9 € безлимит;
все функции в каждом, разница только в сканах.
Вход — заглушка (SIGNUP_URL в seo/config.py), CTA-кнопка «Взять» ведёт на /ceny/.

## Структура

- `seo/config.py` — бренд, BASE_URL (qr-gi.com), CTA, тарифы (PLANS), группы.
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

Список страниц — в `sitemap.xml`. Canonical-база — в `seo/config.py:BASE_URL` (qr-gi.com).

## Деплой

`bash deploy.sh` (lock → git pull → rsync на VPS → health :8080).
nginx vhost — `nginx/digital-menu-es.conf` (try_files $uri $uri/ — чистые URL без .html).
