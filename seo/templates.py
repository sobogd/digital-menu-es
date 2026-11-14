# HTML-шаблоны. Без JS. Весь контент — в HTML.

from . import config as C


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def logo_svg(size=32):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 512 512" aria-hidden="true" class="logo-mark">
  <rect width="512" height="512" rx="112" fill="#1b4332"/>
  <path d="M118 214 166 84c4-11 19-13 26-4l86 108H118Z" fill="#e8944a"/>
  <path d="M146 196 178 106l58 80H146Z" fill="#b4622f"/>
  <g fill="#f7efe3">
    <rect x="292" y="96" width="44" height="44" rx="8"/>
    <rect x="348" y="96" width="44" height="44" rx="8"/>
    <rect x="292" y="152" width="44" height="44" rx="8"/>
    <rect x="348" y="152" width="44" height="44" rx="8" fill="#1b4332"/>
    <rect x="292" y="208" width="44" height="44" rx="8" fill="#1b4332"/>
    <rect x="348" y="208" width="44" height="44" rx="8"/>
  </g>
  <path d="M256 158c104 0 172 66 172 148 0 92-74 148-172 148S84 398 84 306c0-82 68-148 172-148Z" fill="#f0b26a"/>
  <path d="M256 210c64 0 112 38 112 90 0 60-52 96-112 96s-112-36-112-96c0-52 48-90 112-90Z" fill="#f7efe3"/>
  <circle cx="204" cy="286" r="17" fill="#2a1e14"/>
  <circle cx="308" cy="286" r="17" fill="#2a1e14"/>
  <path d="M256 318c-14 0-24 10-24 22 0 14 12 24 24 24s24-10 24-24c0-12-10-22-24-22Z" fill="#2a1e14"/>
  <path d="M256 364v26m0 0c-10 14-26 16-38 8m38-8c10 14 26 16 38 8" stroke="#2a1e14" stroke-width="12" stroke-linecap="round" fill="none"/>
</svg>'''


def wordmark():
    return f'<span class="wordmark"><b>QR</b>{esc(C.BRAND_LATIN[2:])}</span>'


def head(title, description, path, og_type="website"):
    url = C.BASE_URL + path
    return f'''<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{url}/">
  <link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{esc(C.BRAND_LATIN)}">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{url}/">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/css/style.css">'''


def org_jsonld():
    return '''{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "%s",
  "alternateName": "%s",
  "url": "%s/",
  "logo": "%s/assets/logo.svg",
  "description": "%s",
  "sameAs": ["%s"]
}''' % (C.BRAND_LATIN, C.BRAND_RU, C.BASE_URL, C.BASE_URL, esc(C.BRAND_DESC).replace('"', "'"), C.PRODUCT_SITE)


def breadcrumb_items(items):
    out = [{"@type": "ListItem", "position": i + 1, "name": esc(n),
            "item": C.BASE_URL + ("/" if p == "" else p + "/")}
           for i, (n, p) in enumerate(items)]
    return out


def breadcrumb_jsonld(items):
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": breadcrumb_items(items)}, ensure_ascii=False)


def faq_jsonld(faqs):
    import json
    q = [{"@type": "Question", "name": esc(f["q"]),
          "acceptedAnswer": {"@type": "Answer", "text": esc(f["a"])}} for f in faqs]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": q},
                      ensure_ascii=False)


def webpage_jsonld(title, description, path):
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                       "name": esc(title), "description": esc(description),
                       "url": C.BASE_URL + path + "/"}, ensure_ascii=False)


def article_jsonld(title, description, path, body_text):
    import json
    return json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": esc(title), "description": esc(description),
        "url": C.BASE_URL + path + "/", "inLanguage": "ru",
        "datePublished": C.LASTMOD, "dateModified": C.LASTMOD,
        "author": {"@type": "Organization", "name": C.BRAND_LATIN},
        "publisher": {"@type": "Organization", "name": C.BRAND_LATIN,
                      "logo": {"@type": "ImageObject", "url": C.BASE_URL + "/assets/logo.svg"}},
        "articleBody": esc(body_text[:5000])}, ensure_ascii=False)


def header():
    nav = '''<nav class="nav-desktop" aria-label="Основная навигация">
      <a href="/funktsii/">Функции</a>
      <a href="/dlya-kogo/">Для кого</a>
      <a href="/goroda/">Города</a>
      <a href="/statyi/">Статьи</a>
      <a href="/ceny/">Цены</a>
      <a href="/faq/">FAQ</a>
    </nav>'''
    drop = '''<nav class="nav-drop" aria-label="Основная навигация">
      <a href="/funktsii/">Функции</a>
      <a href="/dlya-kogo/">Для кого</a>
      <a href="/goroda/">Города</a>
      <a href="/statyi/">Статьи</a>
      <a href="/ceny/">Цены</a>
      <a href="/faq/">FAQ</a>
      <a class="btn btn-primary btn-sm" href="{signup}">Попробовать бесплатно</a>
    </nav>'''.format(signup=C.SIGNUP_URL)
    return f'''<a class="skip" href="#main">К содержанию</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="{esc(C.BRAND_LATIN)} — на главную">{logo_svg(34)}{wordmark()}</a>
    <details class="nav-toggle">
      <summary aria-label="Открыть меню"><span class="burger" aria-hidden="true"></span></summary>
      {drop}
    </details>
    {nav}
    <a class="btn btn-primary btn-sm header-cta" href="{C.SIGNUP_URL}">Попробовать бесплатно</a>
  </div>
</header>'''


def footer():
    legal = "".join(
        f'<a href="{u}" rel="noopener">{label}</a>'
        for label, u in [("Оферта", C.LEGAL["offer"]), ("Конфиденциальность", C.LEGAL["privacy"]),
                         ("Cookies", C.LEGAL["cookies"])]
    )
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      {logo_svg(40)}{wordmark()}
      <p>{esc(C.BRAND_TAGLINE)}. Запуск за 14 дней бесплатно, без карты.</p>
      <p class="footer-contacts">Продукт: <a href="{C.PRODUCT_SITE}">{esc(C.BRAND_LATIN)} · iq-rest.com</a></p>
    </div>
    <nav class="footer-col" aria-label="Функции">
      <h3>Функции</h3>
      <a href="/rezervy-online-bez-zvonkov/">Бронирование онлайн</a>
      <a href="/mnogoiazychnoe-menyu/">Мультиязычное меню</a>
      <a href="/alergeny-v-menyu/">Аллергены в меню</a>
      <a href="/kuhonnyi-displey/">Кухонный дисплей</a>
      <a href="/zakazy-iz-menyu/">Заказы из меню</a>
      <a href="/ceny/">Цены</a>
    </nav>
    <nav class="footer-col" aria-label="Для кого">
      <h3>Для кого</h3>
      <a href="/menyu-digital-dlya-pitseryi/">Пиццерия</a>
      <a href="/menyu-digital-dlya-sushi-bar/">Суши-бар</a>
      <a href="/menyu-digital-dlya-bara/">Бар</a>
      <a href="/menyu-digital-dlya-otelya/">Отель</a>
      <a href="/dlya-kogo/">Все заведения <span aria-hidden="true">→</span></a>
    </nav>
    <nav class="footer-col" aria-label="Города">
      <h3>Города</h3>
      <a href="/menyu-digital-v-moskve/">Москва</a>
      <a href="/menyu-digital-v-s-peterburge/">Санкт-Петербург</a>
      <a href="/menyu-digital-v-kazani/">Казань</a>
      <a href="/menyu-digital-v-novosibirske/">Новосибирск</a>
      <a href="/goroda/">Все города <span aria-hidden="true">→</span></a>
    </nav>
    <nav class="footer-col" aria-label="Статьи и помощь">
      <h3>Статьи и помощь</h3>
      <a href="/statyi/">Все статьи <span aria-hidden="true">→</span></a>
      <a href="/skolko-stoit-menyu-digitalnoe/">Сколько стоит меню</a>
      <a href="/faq/">FAQ</a>
      <a href="/otzyvy/">Отзывы</a>
      <a href="/bezopasnost-dannykh/">Безопасность данных</a>
    </nav>
  </div>
  <div class="wrap footer-bottom">
    <p>© {C.YEAR} {esc(C.BRAND_LATIN)} · {esc(C.BRAND_RU)}</p>
    <nav class="footer-legal" aria-label="Юридическое">{legal}</nav>
  </div>
</footer>'''


def breadcrumbs(items):
    links = " ".join(
        f'<a href="{p}/">{esc(n)}</a>' for n, p in items[1:-1] if p
    )
    last = esc(items[-1][0])
    if links:
        inner = f'{links} <span>/</span> <span class="bc-current">{last}</span>'
    else:
        inner = f'<span class="bc-current">{last}</span>'
    return f'''<nav class="breadcrumbs" aria-label="Хлебные крошки">
  <div class="wrap"><a href="/">Главная</a>{" <span>/</span> " if links else ""}{inner}</div>
</nav>'''


def faq_block(faqs, h2="Частые вопросы"):
    items = "".join(
        f'<details><summary>{esc(q["q"])}</summary><p>{esc(q["a"])}</p></details>' for q in faqs
    )
    return f'<section class="faq-section"><div class="wrap faq-list"><h2>{esc(h2)}</h2>{items}</div></section>'


def related_block(pages, h2):
    if not pages:
        return ""
    cards = "".join(
        f'<a class="related-card" href="/{p["slug"]}/"><span class="related-name">{esc(p["title_short"])}</span><span class="related-arrow" aria-hidden="true">→</span></a>'
        for p in pages[:8]
    )
    return f'<section class="related"><div class="wrap"><h2>{esc(h2)}</h2><div class="related-grid">{cards}</div></div></section>'


def cta_band():
    return f'''<section class="final-cta">
  <div class="wrap">
    <h2>Запустите меню за 14 дней бесплатно</h2>
    <p>Карта не нужна. Для старта — только email. Демо: <a href="{C.DEMO_URL}">открыть меню-демо</a>.</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="{C.SIGNUP_URL}">Попробовать бесплатно</a>
      <a class="btn btn-ghost" href="{C.DEMO_URL}">Открыть демо</a>
    </div>
  </div>
</section>'''


def body_sections(sections):
    out = []
    for s in sections:
        html = f'<h2>{esc(s["h2"])}</h2>'
        for p in s.get("body", []):
            html += f"<p>{esc(p)}</p>"
        if s.get("list"):
            html += "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in s["list"]) + "</ul>"
        out.append(f'<div class="article-block">{html}</div>')
    return "\n".join(out)


def reviews_block(reviews):
    if not reviews:
        return ""
    cards = "".join(
        f'<figure class="review"><blockquote>{esc(r["text"])}</blockquote>'
        f'<figcaption>{esc(r["name"])} · {esc(r["role"])}</figcaption></figure>' for r in reviews)
    return f'<section class="reviews" aria-label="Отзывы"><div class="wrap"><div class="reviews-grid">{cards}</div></div></section>'


def render_page(data, related):
    """Программная страница или статья."""
    path = "/" + data["slug"]
    group = C.GROUPS[data["group"]]
    if data["kind"] == "article":
        crumbs = [("", ""), (group["name"], "/" + group["path"]), (data["h1"], path)]
        ld = [org_jsonld(), breadcrumb_jsonld(crumbs), article_jsonld(
            data["title"], data["metaDescription"], path, " ".join(
                p for s in data["sections"] for p in s.get("body", []))), faq_jsonld(data["faq"])]
    else:
        crumbs = [("", ""), (group["name"], "/" + group["path"]), (data["h1"], path)]
        ld = [org_jsonld(), breadcrumb_jsonld(crumbs), webpage_jsonld(
            data["title"], data["metaDescription"], path)]
    if data.get("faq"):
        if data["kind"] != "article":
            ld.append(faq_jsonld(data["faq"]))
    ld_html = "\n".join(f'<script type="application/ld+json">{x}</script>' for x in ld)
    intro = f'<p class="lead">{esc(data["intro"][0])}</p>'
    if len(data["intro"]) > 1:
        intro += "".join(f"<p>{esc(p)}</p>" for p in data["intro"][1:])
    faq = data.get("faq", [])
    faq_html = faq_block(faq) if faq else ""
    return f'''<!doctype html>
<html lang="ru">
<head>
  {head(data["title"], data["metaDescription"], path)}
  {ld_html}
</head>
<body>
{header()}
<main id="main">
{breadcrumbs(crumbs)}
<article class="page-article">
  <div class="wrap prose">
    <h1>{esc(data["h1"])}</h1>
    {intro}
    {body_sections(data.get("sections", []))}
  </div>
  {reviews_block(data.get("reviews"))}
  {faq_html}
  {related_block(related, group["related_h2"])}
  {cta_band()}
</article>
</main>
{footer()}
</body>
</html>'''
