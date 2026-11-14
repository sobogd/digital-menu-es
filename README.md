# digital-menu-es

Лендинг нового продукта: QR-меню + резервации. Только HTML + CSS, **ноль JS**, один язык — испанский. Один файл `index.html`, весь дизайн (мок-апы телефона/планшета, формы FAQ, мобильное меню) — чистый CSS.

## Файлы

- `index.html` — вся страница
- `css/style.css` — все стили
- `nginx/digital-menu-es.conf` — nginx vhost для VPS (`listen 8080`), ставится один раз
- `deploy.sh` — деплой на VPS (паттерн `iq-translate/deploy.sh`)

## Деплой

Разовая подготовка на VPS:

```bash
ssh deployer@46.225.143.221
sudo mkdir -p /home/deploy/apps/digital-menu-es
# скопировать nginx/digital-menu-es.conf в sites-available + symlink в sites-enabled
sudo nginx -t && sudo systemctl reload nginx
```

Дальше с Mac:

```bash
bash deploy.sh
```

Смотреть: http://46.225.143.221:8080/

`deploy.sh`: lock → git pull → dirty-guard (FORCE=1) → rsync на VPS → health-check `:8080` → state-файл `~/Library/Logs/digital-menu-es.applied`.

## Статус

Каркас: hero, 4 benefit-карточки, секции Menú / Reservas с CSS-мок-апами, «como funciona», Precios (2 плана), FAQ (`<details>`), final CTA, footer. Тексты — placeholder. Лид-форма и живое демо пока не делаются.
