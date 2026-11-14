# Настройки сайта. Все, что меняется глобально — здесь.
# Смена бренда/базы = поправка здесь + `python3 seo/gen.py`.

BRAND_LATIN = "QRgine"
BRAND_RU = "Коргин"
BRAND_TAGLINE = "Цифровые меню с QR для ресторанов"
BRAND_DESC = ("QRgine (Коргин) — сервис цифровых меню с QR-кодом: гость сканирует код на столе, "
              "открывает меню в браузере на своём языке и заказывает или бронирует стол. "
              "Запуск за 14 дней бесплатно, без карты.")

BASE_URL = "http://46.225.143.221:8080"
YEAR = "2026"
LASTMOD = "2026-11-14"

SIGNUP_URL = "https://dashboard.iq-rest.com"
DEMO_URL = "https://love-eatery.iq-rest.com"
PRODUCT_SITE = "https://iq-rest.com/ru"
LEGAL = {
    "offer": "https://iq-rest.com/ru/terms",
    "privacy": "https://iq-rest.com/ru/privacy",
    "cookies": "https://iq-rest.com/ru/cookies",
}
SUPPORT_URL = "https://iq-rest.com/ru"

GROUPS = {
    "types": {
        "name": "Для кого",
        "path": "dlya-kogo",
        "plural": "заведений",
        "related_h2": "Меню для других заведений",
        "hub_title": "Цифровое меню: для каких заведений",
    },
    "features": {
        "name": "Функции",
        "path": "funktsii",
        "plural": "функций",
        "related_h2": "Другие функции",
        "hub_title": "Функции QRgine: меню, брони, заказы, KDS",
    },
    "cities": {
        "name": "Города",
        "path": "goroda",
        "plural": "городов",
        "related_h2": "Меню в других городах",
        "hub_title": "Цифровое меню в городах России",
    },
    "articles": {
        "name": "Статьи",
        "path": "statyi",
        "plural": "статей",
        "related_h2": "Другие статьи",
        "hub_title": "Гид по цифровым меню для ресторанов",
    },
    "trust": {
        "name": "О сервисе",
        "path": "o-servise",
        "plural": "страниц",
        "related_h2": "Ещё про сервис",
        "hub_title": "О сервисе",
    },
}

# Модули и цены (годовая оплата, EUR, за ресторан в месяц).
MODULES = [
    {"key": "menu", "name": "QR-меню", "price": "9,90",
     "desc": "Меню с фото и аллергенами, AI-перевод на 35 языков, обновления в реальном времени."},
    {"key": "reservations", "name": "+ Бронирование столов", "price": "7,00",
     "desc": "Гости бронируют из того же QR. Агenda, ваши правила, подтверждение автоматически."},
    {"key": "orders", "name": "+ Заказы и кухонный дисплей", "price": "11,00",
     "desc": "Заказ из меню приходит официанту, в WhatsApp или прямо на кухню. KDS-экран."},
    {"key": "domain", "name": "+ Свой домен для меню", "price": "4,00",
     "desc": "Меню открывается на вашем домене, а не на нашем."},
]
