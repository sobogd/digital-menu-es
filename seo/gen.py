#!/usr/bin/env python3
# Генератор всего сайта: python3 seo/gen.py
# Данные: seo/data/**.json -> HTML: ./<slug>/index.html, sitemap.xml, robots.txt

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from seo import config as C  # noqa: E402
from seo import templates as T  # noqa: E402


def load_data():
    data = {}
    for group in C.GROUPS:
        d = ROOT / "seo" / "data" / group
        if not d.exists():
            continue
        for f in sorted(d.glob("*.json")):
            doc = json.loads(f.read_text())
            doc["group"] = group
            data[doc["slug"]] = doc
    for name in ("home", "ceny", "faq", "hubs"):
        f = ROOT / "seo" / "data" / f"{name}.json"
        if f.exists():
            data[f"__{name}"] = json.loads(f.read_text())
    return data


def related_for(doc, all_pages):
    if doc.get("related_slugs"):
        out = []
        names = {"ceny": "Цены", "faq": "FAQ",
                 "dlya-kogo": "Для кого", "funktsii": "Функции",
                 "goroda": "Города", "statyi": "Статьи"}
        for s in doc["related_slugs"]:
            p = next((x for x in all_pages if x["slug"] == s), None)
            if p is None:
                p = {"slug": s, "title_short": names[s]} if s in names else None
            if p:
                out.append(p)
        return out
    group = doc["group"]
    return [p for p in all_pages
            if p["group"] == group and p["slug"] != doc["slug"]][:8]


def write(rel, html):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    return rel


def render_home():
    d = DATA["__home"]
    path = ""
    stats = "".join(
        f'<div class="stat"><span class="stat-num">{esc2(s["value"])}</span><span class="stat-label">{esc2(s["label"])}</span></div>'
        for s in d["stats"])
    benefits = "".join(
        f'<div class="benefit-card"><h3>{esc2(b["h3"])}</h3><p>{esc2(b["p"])}</p></div>' for b in d["benefits"])
    reviews = "".join(
        f'<figure class="review"><blockquote>{esc2(r["text"])}</blockquote>'
        f'<figcaption>{esc2(r["name"])} · {esc2(r["role"])}</figcaption></figure>' for r in d["reviews"])
    faq_items = "".join(
        f'<details><summary>{esc2(q["q"])}</summary><p>{esc2(q["a"])}</p></details>' for q in d["faq"])
    menu_items = "".join(
        f'<li><h3>{esc2(x["h3"])}</h3><p>{esc2(x["p"])}</p></li>' for x in d["menu"])
    resa_items = "".join(
        f'<li><h3>{esc2(x["h3"])}</h3><p>{esc2(x["p"])}</p></li>' for x in d["reservations"])
    kds_items = "".join(
        f'<li><h3>{esc2(x["h3"])}</h3><p>{esc2(x["p"])}</p></li>' for x in d["kds"])
    steps = "".join(
        f'<div class="step"><span class="step-num">{i + 1}</span><h3>{esc2(s["h3"])}</h3><p>{esc2(s["p"])}</p></div>'
        for i, s in enumerate(d["steps"]))
    offers = []
    for o in C.MODULES:
        offers.append(f'<div class="module-row"><div class="module-name">{esc2(o["name"])}</div>'
                      f'<div class="module-desc">{esc2(o["desc"])}</div>'
                      f'<div class="module-price">{esc2(o["price"])} €<small>/мес</small></div></div>')
    offers_html = "".join(offers)

    import json as _json
    app_offer = [{"@type": "Offer", "name": o["name"], "price": o["price"].replace(",", "."),
                  "priceCurrency": "EUR", "availability": "https://schema.org/InStock",
                  "url": C.BASE_URL + "/ceny/"} for o in C.MODULES]
    ld = [
        T.org_jsonld(),
        _json.dumps({"@context": "https://schema.org", "@type": "WebSite",
                     "name": C.BRAND_LATIN, "url": C.BASE_URL + "/"}, ensure_ascii=False),
        _json.dumps({"@context": "https://schema.org", "@type": "SoftwareApplication",
                     "name": C.BRAND_LATIN, "alternateName": C.BRAND_RU,
                     "applicationCategory": "BusinessApplication",
                     "operatingSystem": "Web (браузер гостя, без установки)",
                     "url": C.BASE_URL + "/", "offers": app_offer,
                     "publisher": {"@type": "Organization", "name": C.BRAND_LATIN},
                     "featureList": ["QR-меню с фото и аллергенами", "AI-перевод на 35 языков",
                                     "Бронирование столов из QR", "Приём заказов и кухонный дисплей",
                                     "Обновление меню без замены QR"],
                     "description": C.BRAND_DESC}, ensure_ascii=False),
        T.faq_jsonld(d["faq"]),
        T.breadcrumb_jsonld([("", "")]),
    ]
    ld_html = "\n".join(f'<script type="application/ld+json">{x}</script>' for x in ld)

    return f'''<!doctype html>
<html lang="ru">
<head>
  {T.head(d["title"], d["metaDescription"], path)}
  {ld_html}
</head>
<body>
{T.header()}
<main id="main">

  <section class="hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <h1>{esc2(d["h1"])}</h1>
        <p class="lead">{esc2(d["lead"])}</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{C.SIGNUP_URL}">Попробовать бесплатно</a>
          <a class="btn btn-ghost" href="{C.DEMO_URL}">Открыть демо</a>
        </div>
        <p class="hero-note">{esc2(d["hero_note"])}</p>
      </div>
      <div class="hero-device">
        <div class="device phone" role="img" aria-label="Вид цифрового меню в мобильном браузере">
          <div class="screen">
            <div class="m-hero">
              <span class="m-badge">{esc2(C.BRAND_LATIN)}</span>
              <h3>{esc2(d["demo_restaurant"])}</h3>
              <p>Европейская кухня</p>
            </div>
            <div class="m-chips">
              <span class="chip is-active">Блюда</span>
              <span class="chip">Десерты</span>
              <span class="chip">Напитки</span>
            </div>
            <ul class="m-list">
              <li><div class="m-dish-info"><h4>Ризотто с грибами</h4><p>Грибы, сливки, пармезан</p></div><span class="m-price">850 ₽</span></li>
              <li><div class="m-dish-info"><h4>Сырники</h4><p>Творог, сметана, ягоды</p></div><span class="m-price">420 ₽</span></li>
              <li><div class="m-dish-info"><h4>Борщ с говядиной</h4><p>Сметана, пампушка</p></div><span class="m-price">560 ₽</span></li>
            </ul>
            <div class="m-cta"><span>Резервировать стол</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="stats" aria-label="Показатели сервиса">
    <div class="wrap stats-grid">
      {stats}
      <p class="stats-date">Данные на {esc2(d["stats_date"])}</p>
    </div>
  </section>

  <section class="benefits" aria-label="Преимущества">
    <div class="wrap benefits-grid">{benefits}</div>
  </section>

  <section id="menyu" class="feature">
    <div class="wrap feature-grid">
      <div class="feature-copy">
        <h2>{esc2(d["menu_h2"])}</h2>
        <p>{esc2(d["menu_lead"])}</p>
        <ul class="bullet-list">{menu_items}</ul>
        <a class="link-more" href="/funktsii/">Все функции <span aria-hidden="true">→</span></a>
      </div>
      <div class="feature-device">
        <div class="device phone" role="img" aria-label="Карточка блюда с фото и аллергенами">
          <div class="screen">
            <div class="m-hero m-hero--photo"><span class="m-dish-tag">Фото блюда</span><h3>Ризотто с грибами</h3></div>
            <div class="m-detail">
              <p>Грибы, сливки, пармезан. Сметана и пампушка в комплекте.</p>
              <p class="m-allergens">Аллергены: глютен (G), молочные продукты (D)</p>
              <div class="m-price-row"><span class="m-price m-price--big">850 ₽</span><span class="m-add"><span>В заказ</span></span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="rezervy" class="feature feature--flip">
    <div class="wrap feature-grid">
      <div class="feature-copy">
        <h2>{esc2(d["resa_h2"])}</h2>
        <p>{esc2(d["resa_lead"])}</p>
        <ul class="bullet-list">{resa_items}</ul>
        <a class="link-more" href="/rezervy-online-bez-zvonkov/">Подробнее о бронировании <span aria-hidden="true">→</span></a>
      </div>
      <div class="feature-device">
        <div class="device tablet" role="img" aria-label="Экран бронирования столов">
          <div class="screen">
            <div class="r-head"><h3>Резервирование</h3><span>{esc2(d["demo_restaurant"])} · Москва</span></div>
            <div class="r-dates"><span class="chip">14 ноя</span><span class="chip is-active">15 ноя</span><span class="chip">16 ноя</span><span class="chip">17 ноя</span></div>
            <div class="r-slots"><span>13:00</span><span class="is-active">14:00</span><span>15:00</span><span>18:00</span><span class="is-muted">19:00</span><span>20:00</span><span class="is-muted">21:00</span><span>22:00</span></div>
            <div class="r-party"><span>Гостей</span><div class="stepper"><span>−</span><b>2</b><span>+</span></div>
            <div class="r-cta"><span>Подтвердить бронь</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="kds" class="feature">
    <div class="wrap feature-grid">
      <div class="feature-copy">
        <h2>{esc2(d["kds_h2"])}</h2>
        <p>{esc2(d["kds_lead"])}</p>
        <ul class="bullet-list">{kds_items}</ul>
        <a class="link-more" href="/kuhonnyi-displey/">Подробнее о KDS <span aria-hidden="true">→</span></a>
      </div>
      <div class="feature-device">
        <div class="device tablet" role="img" aria-label="Кухонный дисплей с заказами">
          <div class="screen kds-screen">
            <div class="kds-col"><span class="kds-head">Гриль · 3</span><span class="kds-card">12 · Ризотто ×2</span><span class="kds-card is-new">13 · Сырники</span></div>
            <div class="kds-col"><span class="kds-head">Бар · 2</span><span class="kds-card">14 · Мохито</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="ai-band">
    <div class="wrap">
      <h2>{esc2(d["ai_h2"])}</h2>
      <p>{esc2(d["ai_p"])}</p>
    </div>
  </section>

  <section id="pasoi" class="steps">
    <div class="wrap">
      <h2>Как это работает</h2>
      <div class="steps-grid">{steps}</div>
    </div>
  </section>

  <section id="tsenyi" class="pricing">
    <div class="wrap">
      <h2>Цены</h2>
      <p class="pricing-sub">Модульная цена за ресторан, без комиссии с заказов. Годовая оплата.</p>
      <div class="module-table">
        <div class="module-row module-head"><div class="module-name">Модуль</div><div class="module-desc">Что входит</div><div class="module-price">Цена</div></div>
        {offers_html}
      </div>
      <p class="pricing-note">Годовая оплата ≈ −30% к помесячной. Скидки за объём до 50% при 5+ ресторанах. Полный разбор — на странице <a href="/ceny/">«Цены»</a>.</p>
    </div>
  </section>

  <section class="reviews" aria-label="Отзывы">
    <div class="wrap">
      <h2>Что говорят владельцы</h2>
      <div class="reviews-grid">{reviews}</div>
      <p class="reviews-more">Все отзывы — <a href="/otzyvy/">на странице отзывов</a>.</p>
    </div>
  </section>

  <section id="faq" class="faq-section">
    <div class="wrap faq-list">
      <h2>Частые вопросы</h2>
      {faq_items}
      <p class="faq-more">Все вопросы — <a href="/faq/">на странице FAQ</a>.</p>
    </div>
  </section>

  {T.cta_band()}

</main>
{T.footer()}
</body>
</html>'''


def esc2(s):
    return T.esc(s)


def render_ceny():
    d = DATA["__ceny"]
    path = "/ceny"
    rows = []
    for o in C.MODULES:
        rows.append(f'<div class="module-row"><div class="module-name">{T.esc(o["name"])}</div>'
                    f'<div class="module-desc">{T.esc(o["desc"])}</div>'
                    f'<div class="module-price">{T.esc(o["price"])} €<small>/мес</small></div></div>')
    rows_html = "".join(rows)
    import json as _json
    offer = [{"@type": "Offer", "name": o["name"], "price": o["price"].replace(",", "."),
              "priceCurrency": "EUR"} for o in C.MODULES]
    ld = [T.org_jsonld(),
          T.breadcrumb_jsonld([("", ""), ("Цены", "/ceny")]),
          T.webpage_jsonld(d["title"], d["metaDescription"], path),
          T.faq_jsonld(d["faq"]),
          _json.dumps({"@context": "https://schema.org", "@type": "Product",
                       "name": C.BRAND_LATIN + " — модули", "description": d["metaDescription"],
                       "url": C.BASE_URL + "/ceny/", "brand": {"@type": "Brand", "name": C.BRAND_LATIN},
                       "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                                  "lowPrice": "9.90", "highPrice": "31.90",
                                  "offerCount": str(len(offer)), "offers": offer}}, ensure_ascii=False)]
    ld_html = "\n".join(f'<script type="application/ld+json">{x}</script>' for x in ld)
    crumbs_html = T.breadcrumbs([("", ""), ("Цены", "/ceny")])
    intro = "".join(f"<p>{T.esc(p)}</p>" for p in d["intro"])
    sections = T.body_sections(d["sections"])
    return f'''<!doctype html>
<html lang="ru">
<head>
  {T.head(d["title"], d["metaDescription"], path)}
  {ld_html}
</head>
<body>
{T.header()}
<main id="main">
{crumbs_html}
<article class="page-article">
  <div class="wrap prose">
    <h1>{T.esc(d["h1"])}</h1>
    {intro}
    <div class="module-table">
      <div class="module-row module-head"><div class="module-name">Модуль</div><div class="module-desc">Что входит</div><div class="module-price">Цена</div></div>
      {rows_html}
    </div>
    {sections}
  </div>
  {T.faq_block(d["faq"], "Вопросы о ценах")}
  {T.cta_band()}
</article>
</main>
{T.footer()}
</body>
</html>'''


def render_faq():
    d = DATA["__faq"]
    path = "/faq"
    import json as _json
    ld = [T.org_jsonld(),
          T.breadcrumb_jsonld([("", ""), ("FAQ", "/faq")]),
          T.webpage_jsonld(d["title"], d["metaDescription"], path),
          T.faq_jsonld(d["faq"])]
    ld_html = "\n".join(f'<script type="application/ld+json">{x}</script>' for x in ld)
    intro = "".join(f"<p>{T.esc(p)}</p>" for p in d["intro"])
    faq_html = T.faq_block(d["faq"], "Все вопросы")
    return f'''<!doctype html>
<html lang="ru">
<head>
  {T.head(d["title"], d["metaDescription"], path)}
  {ld_html}
</head>
<body>
{T.header()}
<main id="main">
{T.breadcrumbs([("", ""), ("FAQ", "/faq")])}
<article class="page-article">
  <div class="wrap prose">
    <h1>{T.esc(d["h1"])}</h1>
    {intro}
  </div>
  {faq_html}
  {T.cta_band()}
</article>
</main>
{T.footer()}
</body>
</html>'''


def render_hub(group_key, pages):
    g = C.GROUPS[group_key]
    hubs = DATA["__hubs"]
    h = hubs[group_key]
    path = "/" + g["path"]
    import json as _json
    items = [{"@type": "ListItem", "position": i + 1, "name": T.esc(p["title_short"]),
              "url": C.BASE_URL + "/" + p["slug"] + "/"} for i, p in enumerate(pages)]
    ld = [T.org_jsonld(),
          T.breadcrumb_jsonld([("", ""), (g["name"], path)]),
          T.webpage_jsonld(h["title"], h["metaDescription"], path),
          _json.dumps({"@context": "https://schema.org", "@type": "CollectionPage",
                       "name": T.esc(h["title"]), "url": C.BASE_URL + path + "/"}, ensure_ascii=False),
          _json.dumps({"@context": "https://schema.org", "@type": "ItemList",
                       "itemListElement": items}, ensure_ascii=False)]
    ld_html = "\n".join(f'<script type="application/ld+json">{x}</script>' for x in ld)
    intro = "".join(f"<p>{T.esc(p)}</p>" for p in h["intro"])
    cards = "".join(
        f'<a class="related-card" href="/{p["slug"]}/"><span class="related-name">{T.esc(p["title_short"])}</span><span class="related-arrow" aria-hidden="true">→</span></a>'
        for p in pages)
    return f'''<!doctype html>
<html lang="ru">
<head>
  {T.head(h["title"], h["metaDescription"], path)}
  {ld_html}
</head>
<body>
{T.header()}
<main id="main">
{T.breadcrumbs([("", ""), (g["name"], path)])}
<article class="page-article">
  <div class="wrap prose">
    <h1>{T.esc(h["h1"])}</h1>
    {intro}
    <div class="related-grid related-grid--hub">{cards}</div>
  </div>
  {T.cta_band()}
</article>
</main>
{T.footer()}
</body>
</html>'''


def build_sitemap(paths):
    rows = []
    for p, prio in paths:
        loc = C.BASE_URL + ("/" if p == "" else p + "/")
        rows.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{C.LASTMOD}</lastmod>\n    <priority>{prio}</priority>\n  </url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def build_robots():
    return f'User-agent: *\nAllow: /\n\nSitemap: {C.BASE_URL}/sitemap.xml\n'


def main():
    global DATA
    DATA = load_data()
    pages = [p for k, p in DATA.items() if not k.startswith("__")]
    by_group = {}
    for p in pages:
        by_group.setdefault(p["group"], []).append(p)
    for g in by_group:
        by_group[g].sort(key=lambda x: x.get("order", 99))

    written = [write("index.html", render_home()),
               write("ceny/index.html", render_ceny()),
               write("faq/index.html", render_faq())]

    sitemap = [("", "1.0"), ("/ceny", "0.8"), ("/faq", "0.7")]
    for g, pages_g in by_group.items():
        for p in pages_g:
            rel = write(f"{p['slug']}/index.html",
                        T.render_page(p, related_for(p, pages)))
            written.append(rel)
            prio = "0.6" if g in ("types", "features", "cities") else "0.7"
            sitemap.append(("/" + p["slug"], prio))

    for g in ("types", "features", "cities", "articles"):
        hub = write(f"{C.GROUPS[g]['path']}/index.html", render_hub(g, by_group.get(g, [])))
        written.append(hub)
        sitemap.append(("/" + C.GROUPS[g]["path"], "0.8"))

    write("sitemap.xml", build_sitemap(sitemap))
    write("robots.txt", build_robots())
    print(f"Страниц: {len(written)} (+sitemap, robots)")


if __name__ == "__main__":
    main()
