#!/usr/bin/env python3
"""Генератор статичних сторінок famclean.com.ua (укр. + рос.).

Запуск з кореня репозиторію:  python3 _build/build.py
Пише index.html, ru/, сторінки послуг, 404.html, sitemap.xml, robots.txt, site.webmanifest.
CSS, JS і картинки правляться вручну і генератором не чіпаються.
"""
import html
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://famclean.com.ua"
TODAY = "2026-11-11"
VER = "20261111"

PHONE_TEL = "+380669139223"
PHONE_TXT = "066 913 9223"
VIBER = "viber://chat?number=%2B380669139223"
TG = "https://t.me/family_cleaning_plt"
IG = "https://instagram.com/family_cleaning_plt/"
TT = "https://www.tiktok.com/@family_cleaning_plt"
MAP_SRC = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d82721.1626801863!2d34.54504792244252!3d49.615919673461676"
           "!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x40d825e425e6ba6b%3A0xcf3e6bdfb9e4ca82"
           "!2z0J_QvtC70YLQsNCy0LAsINCf0L7Qu9GC0LDQstGB0YzQutCwINC-0LHQu9Cw0YHRgtGMLCAzNjAwMA!5e0!3m2!1suk!2sua"
           "!4v1744300834224!5m2!1suk!2sua")

LANGS = ("uk", "ru")
PAGES = {
    "home": "/",
    "furniture": "/himchistka-mebliv-poltava/",
    "auto": "/himchistka-salonu-avto-poltava/",
    "cleaning": "/klining-poltava/",
}

# ---------------------------------------------------------------- контекст сторінки
LANG = "uk"
CUR = "/"
ABS = False  # true для 404.html: працює на будь-якій глибині URL, тільки на домені


def t(uk, ru):
    return uk if LANG == "uk" else ru


def purl(key, lang=None):
    p = PAGES[key]
    return p if (lang or LANG) == "uk" else "/ru" + p


def _curdir():
    return CUR if CUR.endswith("/") else CUR.rsplit("/", 1)[0] + "/"


def A(name):
    """Шлях до ресурсу (img/css/js) відносно поточної сторінки."""
    if ABS:
        return name  # 404: шляхи від кореня сайту, <base> задається скриптом
    return "../" * (_curdir().count("/") - 1) + name


def H(key, frag="", lang=None):
    """Посилання на сторінку сайту відносно поточної."""
    target = purl(key, lang)
    if ABS:
        r = target.lstrip("/") or "./"
    else:
        r = os.path.relpath(target, _curdir())
        r = "./" if r == "." else r.rstrip("/") + "/"
    return r + ("#" + frag if frag else "")


def ico(name):
    return f'<svg class="ico" aria-hidden="true"><use href="#i-{name}"/></svg>'


SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></symbol>
<symbol id="i-send" viewBox="0 0 24 24"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/></symbol>
<symbol id="i-insta" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/></symbol>
<symbol id="i-music" viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></symbol>
<symbol id="i-camera" viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/></symbol>
<symbol id="i-wallet" viewBox="0 0 24 24"><path d="M20 7H5a2 2 0 0 1 0-4h13v4"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1V8a1 1 0 0 0-1-1"/><path d="M16 14h.01"/></symbol>
<symbol id="i-sofa" viewBox="0 0 24 24"><path d="M6 11V8.5A2.5 2.5 0 0 1 8.5 6h7A2.5 2.5 0 0 1 18 8.5V11"/><path d="M3 14a2 2 0 0 1 4 0v1h10v-1a2 2 0 0 1 4 0v4.5a.5.5 0 0 1-.5.5h-17a.5.5 0 0 1-.5-.5z"/><path d="M6 19v1.5M18 19v1.5"/></symbol>
<symbol id="i-car" viewBox="0 0 24 24"><path d="m3.5 13.5 1.8-4.9a2 2 0 0 1 1.9-1.3h9.6a2 2 0 0 1 1.9 1.3l1.8 4.9"/><path d="M3.5 13.5h17V18a1 1 0 0 1-1 1H18a1 1 0 0 1-1-1v-1.5H7V18a1 1 0 0 1-1 1H4.5a1 1 0 0 1-1-1z"/><path d="M7 15.2h.01M17 15.2h.01"/></symbol>
<symbol id="i-sparkle" viewBox="0 0 24 24"><path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="m19 15 .8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/></symbol>
<symbol id="i-tool" viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></symbol>
<symbol id="i-drop" viewBox="0 0 24 24"><path d="m12 2.69 4.8619 5.66C22.57712 15 18.127128 22.008301 12.005 22.008301 5.8828718 22.008301 1.5 14.921903 7.1480998 8.35z"/></symbol>
<symbol id="i-window" viewBox="0 0 24 24"><rect x="4.5" y="3" width="15" height="18" rx="1.5"/><path d="M12 3v18M4.5 12h15"/></symbol>
<symbol id="i-bug" viewBox="0 0 24 24"><path d="m21.5 12.5h-3m2-7-2.5 2M17.5 17l3 2.5M9.5 6v-1C9.5 3.6932934 10.494907 2.5 12 2.5c1.505093 0 2.5 1.1790416 2.5 2.5v1m-11-.5 2.5 2M18 9.5V14.5c0 3.355263-2.667143 5.982763-6.004534 5.982763-3.337391 0-5.995466-2.6275-5.995466-5.982763V9.5c0-1.7342599 1.181368-3 3-3H15c1.733122 0 3 1.2657401 3 3zM2.5 12.5h3m1 4.5-3 2.5"/></symbol>
</defs></svg>"""

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZP1D5EXPBN"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-ZP1D5EXPBN');</script>"""

# Мова: збережений вибір перенаправляє ще до відмальовування сторінки (без блимання)
LANG_BOOT = ("<script>(function(){var d=document.documentElement;d.classList.add('js');"
             "try{var p=localStorage.getItem('fc_lang'),a=d.getAttribute('data-alt');"
             "if((p==='uk'||p==='ru')&&a&&p!==d.lang){location.replace(new URL(a,location.href).href+location.search+location.hash);}}"
             "catch(e){}})();</script>")


# ---------------------------------------------------------------- структуровані дані
def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def business():
    return {
        "@type": "LocalBusiness",
        "@id": SITE + "/#business",
        "name": "Family Cleaning",
        "alternateName": "FamClean",
        "url": SITE + "/",
        "telephone": PHONE_TEL,
        "image": SITE + "/img/og-cover.jpg",
        "logo": SITE + "/img/android-chrome-512x512.png",
        "description": t("Хімчистка м'яких меблів і салону авто, генеральне прибирання та прибирання після ремонту в Полтаві та Полтавській області.",
                         "Химчистка мягкой мебели и салона авто, генеральная уборка и уборка после ремонта в Полтаве и Полтавской области."),
        "address": {"@type": "PostalAddress", "addressLocality": t("Полтава", "Полтава"),
                    "addressRegion": t("Полтавська область", "Полтавская область"), "addressCountry": "UA"},
        "areaServed": [{"@type": "City", "name": t("Полтава", "Полтава")},
                       {"@type": "AdministrativeArea", "name": t("Полтавська область", "Полтавская область")}],
        "sameAs": [IG, TT],
    }


def provider():
    b = business()
    return {k: b[k] for k in ("@type", "@id", "name", "url", "telephone")}


def offer(name, price, per_m2=False):
    spec = {"@type": "UnitPriceSpecification", "minPrice": price, "priceCurrency": "UAH"}
    if per_m2:
        spec.update({"unitCode": "MTK", "unitText": "м²"})
    return {"@type": "Offer", "itemOffered": {"@type": "Service", "name": name}, "priceSpecification": spec}


def furniture_offers():
    return [
        offer(t("Хімчистка прямого дивана", "Химчистка прямого дивана"), 1000),
        offer(t("Хімчистка кутового дивана", "Химчистка углового дивана"), 1500),
        offer(t("Хімчистка крісла", "Химчистка кресла"), 500),
        offer(t("Хімчистка стільця", "Химчистка стула"), 200),
    ]


def cleaning_offers():
    return [
        offer(t("Вологе прибирання", "Влажная уборка"), 1500),
        offer(t("Генеральне прибирання", "Генеральная уборка"), 70, True),
        offer(t("Прибирання після ремонту", "Уборка после ремонта"), 70, True),
        offer(t("Миття вікон та фасадів", "Мытье окон и фасадов"), 150, True),
    ]


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": LANG,
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def breadcrumb_ld(name, key):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t("Головна", "Главная"), "item": SITE + purl("home")},
                {"@type": "ListItem", "position": 2, "name": name, "item": SITE + purl(key)}]}


def service_ld(name, desc, key, extra=None):
    d = {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
         "description": desc, "url": SITE + purl(key), "inLanguage": LANG,
         "provider": provider(), "areaServed": business()["areaServed"]}
    if extra:
        d.update(extra)
    return d


# ---------------------------------------------------------------- спільні блоки
def head(title, desc, key, schemas=(), noindex=False):
    other = "ru" if LANG == "uk" else "uk"
    if noindex:
        seo = '<meta name="robots" content="noindex">'
        data_alt = ""
    else:
        url = SITE + purl(key)
        alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{purl(key, l)}">' for l in LANGS)
        og_img = "og-cover.jpg" if LANG == "uk" else "og-cover-ru.jpg"
        locale = "uk_UA" if LANG == "uk" else "ru_RU"
        alt_locale = "ru_RU" if LANG == "uk" else "uk_UA"
        seo = f"""<link rel="canonical" href="{url}">
{alts}
<link rel="alternate" hreflang="x-default" href="{SITE}{purl(key, 'uk')}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:locale:alternate" content="{alt_locale}">
<meta property="og:site_name" content="Family Cleaning">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t("Family Cleaning - клінінгові послуги та хімчистка меблів у Полтаві", "Family Cleaning - клининговые услуги и химчистка мебели в Полтаве")}">
<meta name="twitter:card" content="summary_large_image">"""
        data_alt = f' data-alt="{H(key, lang=other)}"'
    ld = "\n".join(jsonld(s) for s in schemas)
    return f"""<!DOCTYPE html>
<html lang="{LANG}"{data_alt}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{LANG_BOOT}
<title>{title}</title>
<meta name="description" content="{desc}">
{seo}
<meta name="theme-color" content="#2b7ba3">
<meta name="google-site-verification" content="99--LuBpgoL34rDlay3CEURhuqWhSlvif_Wz9FNeY6w">
<link rel="icon" href="{A('img/favicon.ico')}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{A('img/favicon-32x32.png')}">
<link rel="icon" type="image/png" sizes="16x16" href="{A('img/favicon-16x16.png')}">
<link rel="apple-touch-icon" sizes="180x180" href="{A('img/apple-touch-icon.png')}">
<link rel="manifest" href="{A('site.webmanifest')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="{A('css/style.css')}?v={VER}">
{ld}
{GTAG}
</head>"""


def lang_switch(key):
    items = []
    for l, label, name in (("uk", "UA", "Українська"), ("ru", "RU", "Русский")):
        cur = ' aria-current="true"' if l == LANG else ""
        items.append(f'<a href="{H(key, lang=l)}" lang="{l}" hreflang="{l}" data-lang-switch="{l}" aria-label="{name}"{cur}>{label}</a>')
    return f'<div class="lang" role="group" aria-label="{t("Мова", "Язык")}">' + "".join(items) + "</div>"


def header(key):
    nav = [("services", t("Послуги", "Услуги")), ("prices", t("Ціни", "Цены")), ("how", t("Як працюємо", "Как работаем")),
           ("faq", t("Питання", "Вопросы")), ("contact", t("Контакти", "Контакты"))]
    links = "\n".join(f'<a href="{H("home", f)}">{n}</a>' for f, n in nav)
    return f"""<body>
<a class="skip-link" href="#main">{t("Перейти до змісту", "Перейти к содержимому")}</a>
{SPRITE}
<header class="site-header">
<div class="container header-inner">
<a class="brand" href="{H("home")}" aria-label="Family Cleaning - {t("на головну", "на главную")}"><img src="{A('img/logo-dark.svg')}" width="120" height="52" alt="Family Cleaning"></a>
<nav class="nav" id="nav" aria-label="{t("Головне меню", "Главное меню")}">
{links}
</nav>
<a class="btn btn--primary btn--sm header-phone" href="tel:{PHONE_TEL}">{ico("phone")} {PHONE_TXT}</a>
{lang_switch(key)}
<button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="{t("Відкрити меню", "Открыть меню")}" data-label-open="{t("Відкрити меню", "Открыть меню")}" data-label-close="{t("Закрити меню", "Закрыть меню")}"><svg class="ico" aria-hidden="true"><use href="#i-menu"/></svg></button>
</div>
</header>"""


def footer():
    return f"""<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div>
<img src="{A('img/logo.svg')}" width="120" height="52" alt="Family Cleaning" loading="lazy">
<p>{t("Хімчистка м'яких меблів і салону авто, клінінг та прибирання в Полтаві й Полтавській області.",
      "Химчистка мягкой мебели и салона авто, клининг и уборка в Полтаве и Полтавской области.")}</p>
</div>
<div>
<h2>{t("Послуги", "Услуги")}</h2>
<ul>
<li><a href="{H("furniture")}">{t("Хімчистка м'яких меблів", "Химчистка мягкой мебели")}</a></li>
<li><a href="{H("auto")}">{t("Хімчистка салону авто", "Химчистка салона авто")}</a></li>
<li><a href="{H("cleaning")}">{t("Клінінг і прибирання", "Клининг и уборка")}</a></li>
<li><a href="{H("home", "prices")}">{t("Ціни", "Цены")}</a></li>
</ul>
</div>
<div>
<h2>{t("Контакти", "Контакты")}</h2>
<ul>
<li><a href="tel:{PHONE_TEL}">{PHONE_TXT}</a></li>
<li><a href="{VIBER}">Viber</a></li>
<li><a href="{TG}" rel="noopener">Telegram</a></li>
<li><a href="{IG}" rel="noopener">Instagram</a></li>
<li><a href="{TT}" rel="noopener">TikTok</a></li>
</ul>
</div>
</div>
<div class="footer-bottom">© 2026 <strong>Family Cleaning</strong> · {t("Полтава", "Полтава")}</div>
</div>
</footer>
<nav class="mobile-bar" aria-label="{t("Швидкий зв'язок", "Быстрая связь")}">
<a class="is-primary" href="tel:{PHONE_TEL}">{ico("phone")}<span>{t("Подзвонити", "Позвонить")}</span></a>
<a href="{VIBER}">{ico("chat")}<span>Viber</span></a>
<a href="{TG}" rel="noopener">{ico("send")}<span>Telegram</span></a>
</nav>
<script src="{A('js/main.js')}?v={VER}" defer></script>
</body>
</html>
"""


def section_head(eyebrow, title, text=None):
    p = f"<p>{text}</p>" if text else ""
    return f'<div class="section-head"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{p}</div>'


def steps(items):
    lis = "\n".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in items)
    return f'<ol class="steps">\n{lis}\n</ol>'


def checklist(items):
    lis = "\n".join(f"<li>{ico('check')}<span>{x}</span></li>" for x in items)
    return f'<ul class="checklist">\n{lis}\n</ul>'


def faq_html(items):
    out = [f'<details><summary>{html.escape(q, quote=False)}</summary><div class="faq-a"><p>{html.escape(a, quote=False)}</p></div></details>'
           for q, a in items]
    return '<div class="faq">\n' + "\n".join(out) + "\n</div>"


def breadcrumbs(current):
    return f"""<nav class="breadcrumbs" aria-label="{t("Навігація", "Навигация")}">
<ol><li><a href="{H("home")}">{t("Головна", "Главная")}</a></li><li><span aria-current="page">{current}</span></li></ol>
</nav>"""


def cta_band(title, text):
    return f"""<section class="section" aria-labelledby="cta-title">
<div class="container">
<div class="cta-band">
<h2 id="cta-title">{title}</h2>
<p>{text}</p>
<div class="btn-row">
<a class="btn btn--light" href="tel:{PHONE_TEL}">{ico("phone")} {PHONE_TXT}</a>
<a class="btn btn--outline-light" href="{VIBER}">{ico("chat")} Viber</a>
<a class="btn btn--outline-light" href="{TG}" rel="noopener">{ico("send")} Telegram</a>
</div>
</div>
</div>
</section>"""


def related(items):
    links = "\n".join(f'<a href="{href}"><span>{a}<small>{b}</small></span>{ico("arrow")}</a>' for href, a, b in items)
    return f"""<section class="section section--alt" aria-labelledby="more-title">
<div class="container">
<h2 id="more-title" class="prose-center">{t("Інші послуги", "Другие услуги")}</h2>
<div class="related">
{links}
</div>
</div>
</section>"""


def contact_section():
    return f"""<section class="section section--alt" id="contact">
<div class="container">
{section_head(t("Контакти", "Контакты"), t("Замовити послугу", "Заказать услугу"),
              t("Замовити послугу, розрахувати вартість по фото або надіслати запит на послугу, якої немає в переліку, ви можете тут. Приймаємо замовлення по всьому місту та області.",
                "Заказать услугу, рассчитать стоимость по фото или отправить запрос на услугу, которой нет в списке, можно здесь. Принимаем заказы по всему городу и области."))}
<div class="contact-grid">
<div class="contact-card">
<h3>{t("Зв'яжіться з нами", "Свяжитесь с нами")}</h3>
<ul class="contact-list">
<li><a href="tel:{PHONE_TEL}"><span class="tile-ico">{ico("phone")}</span><span>{PHONE_TXT}<small>{t("Подзвонити зараз", "Позвонить сейчас")}</small></span></a></li>
<li><a href="{VIBER}"><span class="tile-ico">{ico("chat")}</span><span>Viber<small>{t("Написати або надіслати фото", "Написать или отправить фото")}</small></span></a></li>
<li><a href="{TG}" rel="noopener"><span class="tile-ico">{ico("send")}</span><span>Telegram<small>{t("Написати або надіслати фото", "Написать или отправить фото")}</small></span></a></li>
<li><a href="{IG}" rel="noopener"><span class="tile-ico">{ico("insta")}</span><span>Instagram<small>@family_cleaning_plt</small></span></a></li>
<li><a href="{TT}" rel="noopener"><span class="tile-ico">{ico("music")}</span><span>TikTok<small>{t("Сторінка в TikTok", "Страница в TikTok")}</small></span></a></li>
</ul>
</div>
<div class="map"><iframe src="{MAP_SRC}" title="{t("Карта: Полтава та область", "Карта: Полтава и область")}" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div>
</div>
</section>"""


def small_card(icon, title, text, href=None):
    inner = f'<span class="tile-ico">{ico(icon)}</span>\n<h3>{title}</h3>\n<p>{text}</p>'
    if href:
        return f'<a class="card card--link" href="{href}">\n{inner}\n</a>'
    return f'<article class="card">\n{inner}\n</article>'


def price_card(img, alt, title, price, unit="грн"):
    return f"""<div class="price-card">
<div class="price-thumb"><img src="{A('img/cat/' + img + '.webp')}" alt="{alt}" width="256" height="256" loading="lazy" decoding="async"></div>
<h4>{title}</h4>
<p class="price">{t("від", "от")} <strong>{price}</strong> {unit}</p>
</div>"""


def table_row(thumb, name, price):
    return f'<tr><td><span class="row-item">{thumb}<span>{name}</span></span></td><td>{price}</td></tr>'


def thumb_img(img, alt):
    return f'<img src="{A("img/cat/" + img + ".webp")}" alt="{alt}" width="256" height="256" loading="lazy" decoding="async">'


def thumb_icon(name):
    return f'<span class="tile-ico row-ico">{ico(name)}</span>'


def render(title, desc, key, schemas, main_html):
    return head(title, desc, key, schemas) + "\n" + header(key) + f'\n<main id="main">\n\n{main_html}\n\n</main>\n' + footer()


def hero_page(name, h1, lead, btn2_label, extra_buttons=""):
    return f"""<section class="page-hero">
<div class="container">
{breadcrumbs(name)}
<span class="chip">{ico("pin")} {t("Полтава та Полтавська область", "Полтава и Полтавская область")}</span>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<div class="btn-row">
<a class="btn btn--primary" href="tel:{PHONE_TEL}">{ico("phone")} {PHONE_TXT}</a>
<a class="btn btn--ghost" href="{VIBER}">{ico("camera")} {btn2_label}</a>
</div>
</div>
</section>"""


def p_unit_m2():
    return "грн/м²"


# ================================================================ HOME
def home_faq():
    return [
        (t("Скільки коштує хімчистка дивана в Полтаві?", "Сколько стоит химчистка дивана в Полтаве?"),
         t("Хімчистка прямого дивана - від 1000 грн, кутового - від 1500 грн. Остаточна вартість залежить від розміру, матеріалу оббивки та ступеня забруднення, тому ми розраховуємо її індивідуально - зокрема по фото.",
           "Химчистка прямого дивана - от 1000 грн, углового - от 1500 грн. Окончательная стоимость зависит от размера, материала обивки и степени загрязнения, поэтому мы рассчитываем ее индивидуально - в том числе по фото.")),
        (t("Чи працюєте ви за межами Полтави?", "Работаете ли вы за пределами Полтавы?"),
         t("Так, приймаємо замовлення по всьому місту та області. Напишіть або зателефонуйте - узгодимо деталі.",
           "Да, принимаем заказы по всему городу и области. Напишите или позвоните - согласуем детали.")),
        (t("Як розрахувати вартість по фото?", "Как рассчитать стоимость по фото?"),
         t("Надішліть кілька фото того, що потрібно почистити, у Viber або Telegram і коротко опишіть завдання. Ми розрахуємо вартість і запропонуємо зручний час.",
           "Пришлите несколько фото того, что нужно почистить, в Viber или Telegram и коротко опишите задачу. Мы рассчитаем стоимость и предложим удобное время.")),
        (t("Чи безпечні ваші засоби для алергіків і дітей?", "Безопасны ли ваши средства для аллергиков и детей?"),
         t("Для м'яких меблів ми використовуємо гіпоалергенні засоби. Якщо в сім'ї є алергіки, маленькі діти чи домашні тварини, повідомте нас заздалегідь - врахуємо це під час роботи.",
           "Для мягкой мебели мы используем гипоаллергенные средства. Если в семье есть аллергики, маленькие дети или домашние животные, сообщите нам заранее - учтем это во время работы.")),
        (t("Скільки сохнуть меблі після хімчистки?", "Сколько сохнет мебель после химчистки?"),
         t("Час висихання залежить від тканини, товщини наповнювача та вентиляції в кімнаті - зазвичай від кількох годин до доби. Провітрюйте приміщення й не користуйтеся меблями, доки оббивка повністю не висохне.",
           "Время высыхания зависит от ткани, толщины наполнителя и вентиляции в комнате - обычно от нескольких часов до суток. Проветривайте помещение и не пользуйтесь мебелью, пока обивка полностью не высохнет.")),
        (t("Які ще послуги ви надаєте?", "Какие еще услуги вы оказываете?"),
         t("Окрім хімчистки меблів і салону авто, ми виконуємо генеральне та вологе прибирання, прибирання після ремонту, миття вікон і фасадів, а також дезінсекцію.",
           "Кроме химчистки мебели и салона авто, мы выполняем генеральную и влажную уборку, уборку после ремонта, мытье окон и фасадов, а также дезинсекцию.")),
    ]


def page_home():
    faq = home_faq()
    title = t("Клінінгові послуги та хімчистка меблів у Полтаві - Family Cleaning", "Клининговые услуги и химчистка мебели в Полтаве - Family Cleaning")
    desc = t("Хімчистка диванів, крісел і салону авто, генеральне прибирання та прибирання після ремонту в Полтаві й області. Ціни від 200 грн. Розрахунок по фото.",
             "Химчистка диванов, кресел и салона авто, генеральная уборка и уборка после ремонта в Полтаве и области. Цены от 200 грн. Расчет по фото.")
    b = business()
    site_ld = {"@context": "https://schema.org", **b, "inLanguage": LANG,
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": t("Послуги Family Cleaning", "Услуги Family Cleaning"),
                                   "itemListElement": furniture_offers() + cleaning_offers()}}
    alt = t("Сіре м'яке крісло в інтер'єрі - хімчистка меблів у Полтаві", "Серое мягкое кресло в интерьере - химчистка мебели в Полтаве")
    cl = lambda a: H("cleaning", a)
    main = f"""<section class="hero">
<img class="hero-bg" src="{A('img/hero-1280.webp')}" srcset="{A('img/hero-800.webp')} 800w, {A('img/hero-1280.webp')} 1280w, {A('img/clean-bg.webp')} 1920w" sizes="100vw" width="1920" height="1280" alt="{alt}" fetchpriority="high" decoding="async">
<div class="hero-shade" aria-hidden="true"></div>
<div class="container hero-content">
<div class="hero-copy">
<span class="chip">{ico("pin")} {t("Полтава та Полтавська область", "Полтава и Полтавская область")}</span>
<h1>{t("Клінінгові послуги та хімчистка меблів у Полтаві", "Клининговые услуги и химчистка мебели в Полтаве")}</h1>
<p class="lead">{t("Повертаємо диванам, кріслам і салону авто чистий вигляд, а квартирам і офісам - свіжість.",
                   "Возвращаем диванам, креслам и салону авто чистый вид, а квартирам и офисам - свежесть.")}</p>
<div class="btn-row">
<a class="btn btn--light" href="tel:{PHONE_TEL}">{ico("phone")} {PHONE_TXT}</a>
<a class="btn btn--outline-light" href="{VIBER}">{ico("chat")} {t("Написати у Viber", "Написать в Viber")}</a>
</div>
<ul class="hero-points">
<li>{ico("check")} {t("Гіпоалергенні засоби для м'яких меблів", "Гипоаллергенные средства для мягкой мебели")}</li>
<li>{ico("check")} {t("Ціни без прихованих доплат", "Цены без скрытых доплат")}</li>
<li>{ico("check")} {t("Розрахунок вартості по фото", "Расчет стоимости по фото")}</li>
</ul>
</div>
<div class="hero-badge"><span class="tile-ico">{ico("camera")}</span><span>{t("Надішліть фото - порахуємо вартість", "Пришлите фото - посчитаем стоимость")}</span></div>
</div>
<a class="hero-scroll" href="#services" aria-label="{t("Перейти до послуг", "Перейти к услугам")}"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18"/><path d="m5.5 14.5 6.5 6.5 6.5-6.5"/></svg></a>
</section>

<section class="section" id="services">
<div class="container">
{section_head(t("Що ми робимо", "Что мы делаем"), t("Наші послуги", "Наши услуги"),
              t("Допомагаємо підтримувати порядок там, де це найважливіше - вдома, в авто чи після складних робіт.",
                "Помогаем поддерживать порядок там, где это важнее всего - дома, в авто или после сложных работ."))}
<div class="cards-feature">
<article class="card-feature">
<span class="tile-ico">{ico("sofa")}</span>
<h3>{t("Хімчистка м'яких меблів", "Химчистка мягкой мебели")}</h3>
<p>{t("Видаляємо плями, пил і запахи з диванів, крісел і стільців, відновлюючи їхній вигляд і подовжуючи термін служби.",
     "Удаляем пятна, пыль и запахи с диванов, кресел и стульев, восстанавливая их вид и продлевая срок службы.")}</p>
<span class="price-tag">{t("від 200 грн", "от 200 грн")}</span>
<a class="btn btn--light" href="{H("furniture")}">{t("Ціни та деталі", "Цены и детали")} {ico("arrow")}</a>
</article>
<article class="card-feature">
<span class="tile-ico">{ico("car")}</span>
<h3>{t("Хімчистка салону авто", "Химчистка салона авто")}</h3>
<p>{t("Професійне очищення салону: сидіння, обшивка, стеля. Оновіть інтер'єр для приємної атмосфери в дорозі.",
     "Профессиональная чистка салона: сиденья, обшивка, потолок. Обновите интерьер для приятной атмосферы в дороге.")}</p>
<span class="price-tag">{t("вартість - індивідуально", "стоимость - индивидуально")}</span>
<a class="btn btn--light" href="{H("auto")}">{t("Детальніше", "Подробнее")} {ico("arrow")}</a>
</article>
<article class="card-feature">
<span class="tile-ico">{ico("sparkle")}</span>
<h3>{t("Клінінг і прибирання", "Клининг и уборка")}</h3>
<p>{t("Генеральне та вологе прибирання, прибирання після ремонту, миття вікон і дезінсекція для квартир, будинків і офісів.",
     "Генеральная и влажная уборка, уборка после ремонта, мытье окон и дезинсекция для квартир, домов и офисов.")}</p>
<span class="price-tag">{t("від 70 грн/м²", "от 70 грн/м²")}</span>
<a class="btn btn--light" href="{H("cleaning")}">{t("Ціни та деталі", "Цены и детали")} {ico("arrow")}</a>
</article>
</div>
<div class="cards-grid">
{small_card("drop", t("Вологе прибирання", "Влажная уборка"),
            t("Миття підлог і знепилення створює свіжу атмосферу вдома чи в офісі. Ідеально для регулярної чистоти.",
              "Мытье полов и удаление пыли создают свежую атмосферу дома или в офисе. Идеально для регулярной чистоты."), cl("wet"))}
{small_card("window", t("Миття вікон та фасадів", "Мытье окон и фасадов"),
            t("Повертаємо склу прозорість. Вартість розраховуємо за площею.",
              "Возвращаем стеклу прозрачность. Стоимость рассчитываем по площади."), cl("windows"))}
{small_card("bug", t("Дезінсекція", "Дезинсекция"),
            t("Знищення тарганів, мурах, комарів та інших шкідників. Безпечні методи з тривалим захисним ефектом.",
              "Уничтожение тараканов, муравьев, комаров и других вредителей. Безопасные методы с длительным защитным эффектом."), cl("pest"))}
<article class="card card--cta">
<h3>{t("Потрібна інша послуга?", "Нужна другая услуга?")}</h3>
<p>{t("Напишіть нам - розрахуємо вартість і для того, чого немає в переліку.", "Напишите нам - рассчитаем стоимость и для того, чего нет в списке.")}</p>
<a class="btn btn--primary btn--sm" href="#contact">{t("Написати нам", "Написать нам")}</a>
</article>
</div>
</div>
</section>

<section class="section section--alt" id="prices">
<div class="container">
{section_head(t("Прайс", "Прайс"), t("Ціни на послуги", "Цены на услуги"),
              t("Вказано мінімальну вартість. Точну суму розраховуємо індивідуально - зокрема по фото.",
                "Указана минимальная стоимость. Точную сумму рассчитываем индивидуально - в том числе по фото."))}
<div class="price-block">
<h3>{t("Хімчистка м'яких меблів", "Химчистка мягкой мебели")}</h3>
<div class="price-grid">
{price_card("sofa", t("Хімчистка прямого дивана", "Химчистка прямого дивана"), t("Диван прямий", "Диван прямой"), "1000")}
{price_card("sofa_cor", t("Хімчистка кутового дивана", "Химчистка углового дивана"), t("Диван кутовий", "Диван угловой"), "1500")}
{price_card("armchair", t("Хімчистка крісла", "Химчистка кресла"), t("Крісло", "Кресло"), "500")}
{price_card("chair", t("Хімчистка стільця", "Химчистка стула"), t("Стілець", "Стул"), "200")}
</div>
</div>
<div class="price-block">
<h3>{t("Клінінг", "Клининг")}</h3>
<div class="price-grid">
{price_card("mop", t("Вологе прибирання", "Влажная уборка"), t("Вологе прибирання", "Влажная уборка"), "1500")}
{price_card("gen_clean", t("Генеральне прибирання", "Генеральная уборка"), t("Генеральне прибирання", "Генеральная уборка"), "70", p_unit_m2())}
{price_card("after-repair", t("Прибирання після ремонту", "Уборка после ремонта"), t("Прибирання після ремонту", "Уборка после ремонта"), "70", p_unit_m2())}
{price_card("window", t("Миття вікон та фасадів", "Мытье окон и фасадов"), t("Миття вікон та фасадів", "Мытье окон и фасадов"), "150", p_unit_m2())}
</div>
</div>
<p class="price-note">{t("Вартість хімчистки салону авто та дезінсекції розраховуємо індивідуально - напишіть або зателефонуйте.",
                         "Стоимость химчистки салона авто и дезинсекции рассчитываем индивидуально - напишите или позвоните.")}</p>
<div class="price-cta"><a class="btn btn--primary" href="#contact">{t("Дізнатися точну вартість", "Узнать точную стоимость")}</a></div>
</div>
</section>

<section class="section" id="how">
<div class="container">
{section_head(t("Процес", "Процесс"), t("Як ми працюємо", "Как мы работаем"),
              t("Від першого повідомлення до чистого результату - чотири прості кроки.", "От первого сообщения до чистого результата - четыре простых шага."))}
{steps([
    (t("Звертаєтесь до нас", "Обращаетесь к нам"),
     t("Телефонуйте або пишіть у Viber чи Telegram. Надішліть фото - так розрахунок буде швидшим.",
       "Звоните или пишите в Viber или Telegram. Пришлите фото - так расчет будет быстрее.")),
    (t("Розраховуємо вартість", "Рассчитываем стоимость"),
     t("Називаємо ціну та узгоджуємо зручний для вас час.", "Называем цену и согласуем удобное для вас время.")),
    (t("Виконуємо роботу", "Выполняем работу"),
     t("Приїжджаємо у вказаний час і чистимо професійними засобами.", "Приезжаем в назначенное время и чистим профессиональными средствами.")),
    (t("Ви оцінюєте результат", "Вы оцениваете результат"),
     t("Оглядаєте результат і отримуєте поради, як довше зберегти чистоту.", "Осматриваете результат и получаете советы, как дольше сохранить чистоту.")),
])}
</div>
</section>

<section class="section section--alt" id="about">
<div class="container about-grid">
<div class="about-art"><img src="{A('img/about-img.webp')}" width="800" height="496" alt="{t("Ілюстрація: двоє клінерів зі шваброю, щіткою та відром", "Иллюстрация: двое клинеров со шваброй, щеткой и ведром")}" loading="lazy" decoding="async"></div>
<div>
<span class="eyebrow">{t("Про нас", "О нас")}</span>
<h2>{t("Невелика команда з Полтави, яка любить чистоту", "Небольшая команда из Полтавы, которая любит чистоту")}</h2>
<p>{t("Вітаємо, ми - <strong>Family Cleaning</strong>. Щиро любимо чистоту та дбаємо про комфорт кожного клієнта. Працюємо уважно, акуратно й з повагою до вашого простору. Наше головне завдання - зробити все максимально просто та зручно для вас.",
     "Здравствуйте, мы - <strong>Family Cleaning</strong>. Искренне любим чистоту и заботимся о комфорте каждого клиента. Работаем внимательно, аккуратно и с уважением к вашему пространству. Наша главная задача - сделать все максимально просто и удобно для вас.")}</p>
<ul class="features">
<li><span class="tile-ico">{ico("star")}</span><div><h3>{t("Якісно", "Качественно")}</h3><p>{t("Наша головна перевага. Послуги з прибирання виконуємо на совість, щоб ви залишилися задоволені.", "Наше главное преимущество. Услуги по уборке выполняем на совесть, чтобы вы остались довольны.")}</p></div></li>
<li><span class="tile-ico">{ico("shield")}</span><div><h3>{t("Професійно", "Профессионально")}</h3><p>{t("Миючі засоби німецьких та українських професійних виробників. Гіпоалергенні засоби для м'яких меблів.", "Моющие средства немецких и украинских профессиональных производителей. Гипоаллергенные средства для мягкой мебели.")}</p></div></li>
<li><span class="tile-ico">{ico("wallet")}</span><div><h3>{t("Доступно", "Доступно")}</h3><p>{t("Чесні ціни без прихованих доплат - якісний клінінг у Полтаві, який можна собі дозволити.", "Честные цены без скрытых доплат - качественный клининг в Полтаве, который можно себе позволить.")}</p></div></li>
</ul>
</div>
</div>
</section>

<section class="section" id="info">
<div class="container">
<div class="prose">
<h2>{t("Хімчистка та клінінг у Полтаві й області", "Химчистка и клининг в Полтаве и области")}</h2>
<p>{t(f'<strong>Family Cleaning</strong> - це хімчистка меблів і клінінгові послуги в Полтаві та Полтавській області. Ми чистимо прямі й кутові дивани, крісла та стільці, оновлюємо <a href="{H("auto")}">салони авто</a>, виконуємо <a href="{H("cleaning")}">генеральне й вологе прибирання</a>, а також прибирання після ремонту.',
     f'<strong>Family Cleaning</strong> - это химчистка мебели и клининговые услуги в Полтаве и Полтавской области. Мы чистим прямые и угловые диваны, кресла и стулья, обновляем <a href="{H("auto")}">салоны авто</a>, выполняем <a href="{H("cleaning")}">генеральную и влажную уборку</a>, а также уборку после ремонта.')}</p>
<p>{t(f'<a href="{H("furniture")}">Хімчистка м\'яких меблів</a> допомагає прибрати пил, плями та неприємні запахи, які з часом накопичуються навіть у доглянутому домі. Для м\'яких меблів ми використовуємо гіпоалергенні засоби, а для інших робіт - професійні миючі засоби німецьких та українських виробників.',
     f'<a href="{H("furniture")}">Химчистка мягкой мебели</a> помогает убрать пыль, пятна и неприятные запахи, которые со временем накапливаются даже в ухоженном доме. Для мягкой мебели мы используем гипоаллергенные средства, а для других работ - профессиональные моющие средства немецких и украинских производителей.')}</p>
<p>{t("Вартість залежить від розміру, матеріалу та ступеня забруднення, тому точну суму ми називаємо індивідуально. Щоб дізнатися ціну хімчистки дивана чи прибирання квартири в Полтаві, надішліть фото у Viber або Telegram - ми розрахуємо вартість і узгодимо зручний час.",
     "Стоимость зависит от размера, материала и степени загрязнения, поэтому точную сумму мы называем индивидуально. Чтобы узнать цену химчистки дивана или уборки квартиры в Полтаве, пришлите фото в Viber или Telegram - мы рассчитаем стоимость и согласуем удобное время.")}</p>
</div>
</div>
</section>

<section class="section section--alt" id="faq">
<div class="container">
{section_head(t("Питання й відповіді", "Вопросы и ответы"), t("Часті запитання", "Частые вопросы"))}
{faq_html(faq)}
</div>
</section>

{contact_section()}"""
    return title, desc, [site_ld, faq_ld(faq)], main


# ================================================================ FURNITURE
def furniture_faq():
    return [
        (t("Скільки коштує хімчистка дивана в Полтаві?", "Сколько стоит химчистка дивана в Полтаве?"),
         t("Хімчистка прямого дивана - від 1000 грн, кутового - від 1500 грн. Остаточна вартість залежить від розміру, матеріалу оббивки та ступеня забруднення, тому ми розраховуємо її індивідуально - найшвидше по фото.",
           "Химчистка прямого дивана - от 1000 грн, углового - от 1500 грн. Окончательная стоимость зависит от размера, материала обивки и степени загрязнения, поэтому мы рассчитываем ее индивидуально - быстрее всего по фото.")),
        (t("Скільки коштує хімчистка крісла або стільця?", "Сколько стоит химчистка кресла или стула?"),
         t("Хімчистка крісла - від 500 грн, стільця - від 200 грн. Якщо потрібно почистити кілька предметів, надішліть фото всіх меблів - розрахуємо загальну вартість.",
           "Химчистка кресла - от 500 грн, стула - от 200 грн. Если нужно почистить несколько предметов, пришлите фото всей мебели - рассчитаем общую стоимость.")),
        (t("Скільки сохне диван після хімчистки?", "Сколько сохнет диван после химчистки?"),
         t("Час висихання залежить від тканини, товщини наповнювача та вентиляції в кімнаті - зазвичай від кількох годин до доби. Провітрюйте приміщення й не користуйтеся меблями, доки оббивка повністю не висохне.",
           "Время высыхания зависит от ткани, толщины наполнителя и вентиляции в комнате - обычно от нескольких часов до суток. Проветривайте помещение и не пользуйтесь мебелью, пока обивка полностью не высохнет.")),
        (t("Чи можна вивести старі плями?", "Можно ли вывести старые пятна?"),
         t("Свіжі плями видаляти простіше, а результат зі старими залежить від їхнього походження та матеріалу оббивки. Надішліть фото - ми чесно скажемо, чого очікувати. Гарантувати повне видалення будь-якої плями неможливо.",
           "Свежие пятна удалять проще, а результат со старыми зависит от их происхождения и материала обивки. Пришлите фото - мы честно скажем, чего ожидать. Гарантировать полное удаление любого пятна невозможно.")),
        (t("Чи безпечні ваші засоби для алергіків і дітей?", "Безопасны ли ваши средства для аллергиков и детей?"),
         t("Для м'яких меблів ми використовуємо гіпоалергенні засоби. Якщо в сім'ї є алергіки, маленькі діти чи домашні тварини, повідомте нас заздалегідь - врахуємо це під час роботи.",
           "Для мягкой мебели мы используем гипоаллергенные средства. Если в семье есть аллергики, маленькие дети или домашние животные, сообщите нам заранее - учтем это во время работы.")),
        (t("Чи можна розрахувати вартість по фото?", "Можно ли рассчитать стоимость по фото?"),
         t("Так. Надішліть кілька фото меблів і плям у Viber або Telegram та коротко опишіть завдання. Ми назвемо вартість і запропонуємо зручний час.",
           "Да. Пришлите несколько фото мебели и пятен в Viber или Telegram и коротко опишите задачу. Мы назовем стоимость и предложим удобное время.")),
        (t("Чи працюєте ви за межами Полтави?", "Работаете ли вы за пределами Полтавы?"),
         t("Так, приймаємо замовлення по всьому місту та області. Напишіть або зателефонуйте - узгодимо деталі.",
           "Да, принимаем заказы по всему городу и области. Напишите или позвоните - согласуем детали.")),
        (t("Як замовити хімчистку меблів?", "Как заказать химчистку мебели?"),
         t(f"Зателефонуйте за номером {PHONE_TXT} або напишіть у Viber чи Telegram. Ми розрахуємо вартість і узгодимо зручний для вас час.",
           f"Позвоните по номеру {PHONE_TXT} или напишите в Viber или Telegram. Мы рассчитаем стоимость и согласуем удобное для вас время.")),
    ]


def page_furniture():
    faq = furniture_faq()
    name = t("Хімчистка м'яких меблів", "Химчистка мягкой мебели")
    title = t("Хімчистка диванів і м'яких меблів у Полтаві від 200 грн", "Химчистка диванов и мягкой мебели в Полтаве от 200 грн")
    desc = t("Хімчистка прямих і кутових диванів, крісел та стільців у Полтаві й області. Ціни від 200 грн, гіпоалергенні засоби. Розрахунок вартості по фото.",
             "Химчистка прямых и угловых диванов, кресел и стульев в Полтаве и области. Цены от 200 грн, гипоаллергенные средства. Расчет стоимости по фото.")
    svc = service_ld(name, t("Хімчистка диванів, крісел і стільців: видалення плям, пилу та запахів.",
                             "Химчистка диванов, кресел и стульев: удаление пятен, пыли и запахов."), "furniture",
                     {"hasOfferCatalog": {"@type": "OfferCatalog", "name": t("Ціни на хімчистку м'яких меблів", "Цены на химчистку мягкой мебели"),
                                          "itemListElement": furniture_offers()}})
    fr = t("від", "от")
    rows = "\n".join([
        table_row(thumb_img("sofa", t("Хімчистка прямого дивана", "Химчистка прямого дивана")), t("Диван прямий", "Диван прямой"), f"{fr} 1000 грн"),
        table_row(thumb_img("sofa_cor", t("Хімчистка кутового дивана", "Химчистка углового дивана")), t("Диван кутовий", "Диван угловой"), f"{fr} 1500 грн"),
        table_row(thumb_img("armchair", t("Хімчистка крісла", "Химчистка кресла")), t("Крісло", "Кресло"), f"{fr} 500 грн"),
        table_row(thumb_img("chair", t("Хімчистка стільця", "Химчистка стула")), t("Стілець", "Стул"), f"{fr} 200 грн"),
    ])
    main = f"""{hero_page(name, t("Хімчистка м'яких меблів у Полтаві", "Химчистка мягкой мебели в Полтаве"),
                          t("Видаляємо плями, пил і запахи з диванів, крісел і стільців. Працюємо з гіпоалергенними засобами та називаємо чесну ціну без прихованих доплат.",
                            "Удаляем пятна, пыль и запахи с диванов, кресел и стульев. Работаем с гипоаллергенными средствами и называем честную цену без скрытых доплат."),
                          t("Розрахунок по фото", "Расчет по фото"))}

<section class="section" id="prices">
<div class="container">
{section_head(t("Прайс", "Прайс"), t("Ціни на хімчистку диванів і меблів", "Цены на химчистку диванов и мебели"),
              t("Вказано мінімальну вартість. Остаточна сума залежить від розміру, матеріалу оббивки та ступеня забруднення.",
                "Указана минимальная стоимость. Окончательная сумма зависит от размера, материала обивки и степени загрязнения."))}
<div class="table-wrap">
<table class="price-table">
<caption class="sr-only">{t("Ціни на хімчистку м'яких меблів у Полтаві", "Цены на химчистку мягкой мебели в Полтаве")}</caption>
<thead><tr><th scope="col">{t("Меблі", "Мебель")}</th><th scope="col">{t("Вартість", "Стоимость")}</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
<p class="price-note">{t("Потрібно почистити інші м'які меблі? Надішліть фото - розрахуємо вартість індивідуально.",
                         "Нужно почистить другую мягкую мебель? Пришлите фото - рассчитаем стоимость индивидуально.")}</p>
<div class="price-cta"><a class="btn btn--primary" href="{VIBER}">{ico("camera")} {t("Надіслати фото для розрахунку", "Отправить фото для расчета")}</a></div>
</div>
</section>

<section class="section section--alt">
<div class="container two-col">
<div class="prose">
<h2>{t("Коли варто замовити хімчистку меблів", "Когда стоит заказать химчистку мебели")}</h2>
{checklist([
    t("на оббивці з'явилися плями від їжі, напоїв чи дитячих рук;", "на обивке появились пятна от еды, напитков или детских рук;"),
    t("диван має неприємний запах - від тварин, їжі, вологи чи часу;", "диван имеет неприятный запах - от животных, еды, влаги или времени;"),
    t("тканина потемніла й втратила колір через пил і щоденне використання;", "ткань потемнела и потеряла цвет из-за пыли и ежедневного использования;"),
    t("ви готуєте квартиру до продажу, здачі в оренду або після переїзду;", "вы готовите квартиру к продаже, сдаче в аренду или после переезда;"),
    t("у домі є алергіки, а в оббивці накопичився пил.", "в доме есть аллергики, а в обивке накопилась пыль."),
])}
</div>
<div class="panel">
<h3>{t("Від чого залежить вартість", "От чего зависит стоимость")}</h3>
<ul class="checklist">
<li>{ico("check")}<span>{t("<strong>Розмір і конфігурація.</strong> Прямий диван, кутовий, крісло чи стілець - це різний обсяг роботи.", "<strong>Размер и конфигурация.</strong> Прямой диван, угловой, кресло или стул - разный объем работы.")}</span></li>
<li>{ico("check")}<span>{t("<strong>Матеріал оббивки.</strong> Різні тканини потребують різних засобів і підходів.", "<strong>Материал обивки.</strong> Разные ткани требуют разных средств и подходов.")}</span></li>
<li>{ico("check")}<span>{t("<strong>Складність плям.</strong> Має значення їхня давність і походження: жир, кава, вино, чорнило, сліди тварин.", "<strong>Сложность пятен.</strong> Важны их давность и происхождение: жир, кофе, вино, чернила, следы животных.")}</span></li>
<li>{ico("check")}<span>{t("<strong>Запахи.</strong> Їх усунення може потребувати додаткової обробки.", "<strong>Запахи.</strong> Их устранение может потребовать дополнительной обработки.")}</span></li>
</ul>
<p class="panel-note">{t("Тому точну ціну ми називаємо індивідуально - найшвидше це зробити по фото.", "Поэтому точную цену мы называем индивидуально - быстрее всего это сделать по фото.")}</p>
</div>
</div>
</section>

<section class="section" id="how">
<div class="container">
{section_head(t("Процес", "Процесс"), t("Як проходить хімчистка меблів", "Как проходит химчистка мебели"))}
{steps([
    (t("Розрахунок", "Расчет"), t("Ви надсилаєте фото й розповідаєте про забруднення. Ми називаємо вартість і узгоджуємо час.", "Вы присылаете фото и рассказываете о загрязнении. Мы называем стоимость и согласуем время.")),
    (t("Огляд оббивки", "Осмотр обивки"), t("Оцінюємо матеріал і плями, щоб підібрати підхід, безпечний для тканини.", "Оцениваем материал и пятна, чтобы подобрать подход, безопасный для ткани.")),
    (t("Чистка", "Чистка"), t("Наносимо засоби для м'яких меблів, видаляємо плями, пил і запахи.", "Наносим средства для мягкой мебели, удаляем пятна, пыль и запахи.")),
    (t("Рекомендації", "Рекомендации"), t("Підказуємо, як висушити меблі та доглядати за оббивкою, щоб результат тримався довше.", "Подсказываем, как высушить мебель и ухаживать за обивкой, чтобы результат держался дольше.")),
])}
</div>
</section>

<section class="section section--alt">
<div class="container two-col">
<div class="panel">
<h3>{t("Перед приїздом", "Перед приездом")}</h3>
{checklist([
    t("Приберіть з меблів подушки, пледи та дрібні речі.", "Уберите с мебели подушки, пледы и мелкие вещи."),
    t("Не розтирайте пляму й не заливайте її водою - так вона розповзається й глибше вбирається в тканину.", "Не растирайте пятно и не заливайте его водой - так оно расползается и глубже впитывается в ткань."),
    t("Підготуйте вільний доступ до меблів.", "Подготовьте свободный доступ к мебели."),
])}
</div>
<div class="panel">
<h3>{t("Після хімчистки", "После химчистки")}</h3>
{checklist([
    t("Не сідайте на меблі, поки вони не висохнуть повністю.", "Не садитесь на мебель, пока она не высохнет полностью."),
    t("Провітрюйте кімнату - так оббивка висихає швидше.", "Проветривайте комнату - так обивка сохнет быстрее."),
    t("Не накривайте меблі плівкою чи пледами до повного висихання.", "Не накрывайте мебель пленкой или пледами до полного высыхания."),
])}
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="prose">
<h2>{t("Професійна хімчистка диванів у Полтаві та області", "Профессиональная химчистка диванов в Полтаве и области")}</h2>
<p>{t("<strong>Family Cleaning</strong> - невелика команда з Полтави, яка займається хімчисткою м'яких меблів. Ми чистимо прямі та кутові дивани, крісла й стільці, прибираємо плями, пил і запахи, повертаючи оббивці охайний вигляд.",
     "<strong>Family Cleaning</strong> - небольшая команда из Полтавы, которая занимается химчисткой мягкой мебели. Мы чистим прямые и угловые диваны, кресла и стулья, убираем пятна, пыль и запахи, возвращая обивке аккуратный вид.")}</p>
<p>{t("Для м'яких меблів ми використовуємо гіпоалергенні засоби. Працюємо уважно, акуратно й з повагою до вашого простору. Приймаємо замовлення по всьому місту та області.",
     "Для мягкой мебели мы используем гипоаллергенные средства. Работаем внимательно, аккуратно и с уважением к вашему пространству. Принимаем заказы по всему городу и области.")}</p>
<p>{t("Хочете дізнатися, скільки коштує хімчистка вашого дивана? Надішліть фото у Viber або Telegram - ми розрахуємо вартість і запропонуємо зручний час.",
     "Хотите узнать, сколько стоит химчистка вашего дивана? Пришлите фото в Viber или Telegram - мы рассчитаем стоимость и предложим удобное время.")}</p>
</div>
</div>
</section>

<section class="section section--alt" id="faq">
<div class="container">
{section_head(t("Питання й відповіді", "Вопросы и ответы"), t("Часті запитання про хімчистку меблів", "Частые вопросы о химчистке мебели"))}
{faq_html(faq)}
</div>
</section>

{cta_band(t("Потрібна хімчистка дивана в Полтаві?", "Нужна химчистка дивана в Полтаве?"),
          t("Зателефонуйте або надішліть фото - розрахуємо вартість і узгодимо зручний час.", "Позвоните или пришлите фото - рассчитаем стоимость и согласуем удобное время."))}

{related([
    (H("auto"), t("Хімчистка салону авто", "Химчистка салона авто"), t("Сидіння, обшивка, стеля", "Сиденья, обшивка, потолок")),
    (H("cleaning"), t("Клінінг і прибирання", "Клининг и уборка"), t("Генеральне, після ремонту, вологе, вікна", "Генеральная, после ремонта, влажная, окна")),
])}"""
    return title, desc, [svc, breadcrumb_ld(name, "furniture"), faq_ld(faq)], main


# ================================================================ AUTO
def auto_faq():
    return [
        (t("Скільки коштує хімчистка салону авто в Полтаві?", "Сколько стоит химчистка салона авто в Полтаве?"),
         t("Вартість залежить від розміру автомобіля, матеріалу оббивки, ступеня забруднення та обсягу робіт, тому ми розраховуємо її індивідуально. Надішліть фото салону у Viber або Telegram - назвемо ціну.",
           "Стоимость зависит от размера автомобиля, материала обивки, степени загрязнения и объема работ, поэтому мы рассчитываем ее индивидуально. Пришлите фото салона в Viber или Telegram - назовем цену.")),
        (t("Що входить у хімчистку салону?", "Что входит в химчистку салона?"),
         t("Очищення сидінь, обшивки та стелі. Якщо потрібно почистити щось ще, напишіть нам - обговоримо обсяг робіт.",
           "Чистка сидений, обшивки и потолка. Если нужно почистить что-то еще, напишите нам - обсудим объем работ.")),
        (t("Скільки часу займає хімчистка салону?", "Сколько времени занимает химчистка салона?"),
         t("Час залежить від розміру авто та рівня забруднення. Орієнтовний час скажемо під час розрахунку.",
           "Время зависит от размера авто и уровня загрязнения. Ориентировочное время назовем во время расчета.")),
        (t("Чи можна розрахувати вартість по фото?", "Можно ли рассчитать стоимость по фото?"),
         t("Так. Надішліть кілька фото салону та плям у Viber або Telegram й коротко опишіть завдання. Ми назвемо вартість і запропонуємо зручний час.",
           "Да. Пришлите несколько фото салона и пятен в Viber или Telegram и коротко опишите задачу. Мы назовем стоимость и предложим удобное время.")),
        (t("Чи приймаєте ви замовлення за межами Полтави?", "Принимаете ли вы заказы за пределами Полтавы?"),
         t("Так, приймаємо замовлення по всьому місту та області. Місце й час узгоджуємо індивідуально.",
           "Да, принимаем заказы по всему городу и области. Место и время согласуем индивидуально.")),
        (t("Як замовити хімчистку салону авто?", "Как заказать химчистку салона авто?"),
         t(f"Зателефонуйте за номером {PHONE_TXT} або напишіть у Viber чи Telegram. Ми розрахуємо вартість і узгодимо зручний для вас час.",
           f"Позвоните по номеру {PHONE_TXT} или напишите в Viber или Telegram. Мы рассчитаем стоимость и согласуем удобное для вас время.")),
    ]


def page_auto():
    faq = auto_faq()
    name = t("Хімчистка салону авто", "Химчистка салона авто")
    title = t("Хімчистка салону авто в Полтаві - Family Cleaning", "Химчистка салона авто в Полтаве - Family Cleaning")
    desc = t("Хімчистка салону авто в Полтаві: сидіння, обшивка, стеля. Прибираємо плями, пил і запахи. Вартість - індивідуально, розрахунок по фото.",
             "Химчистка салона авто в Полтаве: сиденья, обшивка, потолок. Убираем пятна, пыль и запахи. Стоимость - индивидуально, расчет по фото.")
    svc = service_ld(name, t("Очищення сидінь, обшивки та стелі салону автомобіля: видалення плям, пилу та запахів.",
                             "Чистка сидений, обшивки и потолка салона автомобиля: удаление пятен, пыли и запахов."), "auto")
    main = f"""{hero_page(name, t("Хімчистка салону авто в Полтаві", "Химчистка салона авто в Полтаве"),
                          t("Професійно очищаємо сидіння, обшивку та стелю, прибираємо плями, пил і запахи - салон знову виглядає охайно й затишно.",
                            "Профессионально чистим сиденья, обшивку и потолок, убираем пятна, пыль и запахи - салон снова выглядит аккуратно и уютно."),
                          t("Розрахунок по фото", "Расчет по фото"))}

<section class="section">
<div class="container">
{section_head(t("Склад робіт", "Состав работ"), t("Що входить у хімчистку салону", "Что входит в химчистку салона"),
              t("Очищаємо основні поверхні салону, які найбільше контактують із пилом, вологою та щоденним використанням.",
                "Чистим основные поверхности салона, которые больше всего контактируют с пылью, влагой и ежедневным использованием."))}
<div class="cards-grid">
{small_card("sofa", t("Сидіння", "Сиденья"), t("Прибираємо плями, пил і забруднення з оббивки сидінь.", "Убираем пятна, пыль и загрязнения с обивки сидений."))}
{small_card("car", t("Обшивка", "Обшивка"), t("Очищаємо обшивку салону від пилу та слідів щоденного користування.", "Чистим обшивку салона от пыли и следов ежедневного использования."))}
{small_card("sparkle", t("Стеля", "Потолок"), t("Очищаємо стелю салону від пилу та плям.", "Чистим потолок салона от пыли и пятен."))}
</div>
<p class="price-note">{t("Потрібно почистити щось інше в салоні? Напишіть нам - обговоримо обсяг робіт.", "Нужно почистить что-то еще в салоне? Напишите нам - обсудим объем работ.")}</p>
</div>
</section>

<section class="section section--alt" id="prices">
<div class="container two-col">
<div class="prose">
<h2>{t("Скільки коштує хімчистка салону авто", "Сколько стоит химчистка салона авто")}</h2>
<p>{t("Вартість залежить від розміру автомобіля, матеріалу оббивки, ступеня забруднення та складу робіт, тому ми розраховуємо її індивідуально.",
     "Стоимость зависит от размера автомобиля, материала обивки, степени загрязнения и состава работ, поэтому мы рассчитываем ее индивидуально.")}</p>
<p>{t("Щоб дізнатися ціну, надішліть кілька фото салону у Viber або Telegram - ми назвемо вартість і запропонуємо зручний час.",
     "Чтобы узнать цену, пришлите несколько фото салона в Viber или Telegram - мы назовем стоимость и предложим удобное время.")}</p>
<div class="btn-row">
<a class="btn btn--primary" href="{VIBER}">{ico("camera")} {t("Надіслати фото", "Отправить фото")}</a>
<a class="btn btn--ghost" href="tel:{PHONE_TEL}">{ico("phone")} {PHONE_TXT}</a>
</div>
</div>
<div class="panel">
<h3>{t("Що впливає на ціну", "Что влияет на цену")}</h3>
{checklist([
    t("<strong>Розмір авто.</strong> Від компактного хетчбека до мінівена - різний обсяг роботи.", "<strong>Размер авто.</strong> От компактного хетчбэка до минивэна - разный объем работы."),
    t("<strong>Матеріал оббивки.</strong> Різні матеріали потребують різних засобів.", "<strong>Материал обивки.</strong> Разные материалы требуют разных средств."),
    t("<strong>Складність плям.</strong> Давність і походження забруднення.", "<strong>Сложность пятен.</strong> Давность и происхождение загрязнения."),
    t("<strong>Запахи.</strong> Їх усунення може потребувати додаткової обробки.", "<strong>Запахи.</strong> Их устранение может потребовать дополнительной обработки."),
    t("<strong>Обсяг робіт.</strong> Лише сидіння чи весь салон.", "<strong>Объем работ.</strong> Только сиденья или весь салон."),
])}
</div>
</div>
</section>

<section class="section">
<div class="container two-col">
<div class="prose">
<h2>{t("Коли варто замовити хімчистку салону", "Когда стоит заказать химчистку салона")}</h2>
{checklist([
    t("на сидіннях з'явилися плями від кави, їжі чи слідів взуття;", "на сиденьях появились пятна от кофе, еды или следов обуви;"),
    t("в салоні неприємний запах - від їжі, тварин, вологи чи тютюну;", "в салоне неприятный запах - от еды, животных, влаги или табака;"),
    t("оббивка потемніла й виглядає запиленою;", "обивка потемнела и выглядит запыленной;"),
    t("ви готуєте авто до продажу;", "вы готовите авто к продаже;"),
    t("салон залишився брудним після поїздок із дітьми чи тваринами.", "салон остался грязным после поездок с детьми или животными."),
])}
</div>
<div class="panel">
<h3>{t("Поради до та після чистки", "Советы до и после чистки")}</h3>
{checklist([
    t("Приберіть із салону особисті речі та сміття.", "Уберите из салона личные вещи и мусор."),
    t("Повідомте про складні плями й запахи - так розрахунок буде точнішим.", "Сообщите о сложных пятнах и запахах - так расчет будет точнее."),
    t("Провітрюйте салон, поки оббивка не висохне.", "Проветривайте салон, пока обивка не высохнет."),
    t("Не чистьте стелю домашніми засобами - вона чутлива до вологи.", "Не чистите потолок домашними средствами - он чувствителен к влаге."),
])}
</div>
</div>
</section>

<section class="section section--alt" id="how">
<div class="container">
{section_head(t("Процес", "Процесс"), t("Як проходить хімчистка салону", "Как проходит химчистка салона"))}
{steps([
    (t("Розрахунок", "Расчет"), t("Надсилаєте фото салону й розповідаєте про забруднення. Ми називаємо вартість.", "Присылаете фото салона и рассказываете о загрязнении. Мы называем стоимость.")),
    (t("Домовленість", "Договоренность"), t("Узгоджуємо зручні для вас час і місце.", "Согласуем удобные для вас время и место.")),
    (t("Чистка", "Чистка"), t("Очищаємо сидіння, обшивку та стелю професійними засобами.", "Чистим сиденья, обшивку и потолок профессиональными средствами.")),
    (t("Результат", "Результат"), t("Ви оглядаєте салон і отримуєте поради щодо догляду за оббивкою.", "Вы осматриваете салон и получаете советы по уходу за обивкой.")),
])}
</div>
</section>

<section class="section">
<div class="container">
<div class="prose">
<h2>{t("Хімчистка авто в Полтаві та області", "Химчистка авто в Полтаве и области")}</h2>
<p>{t(f'<strong>Family Cleaning</strong> - невелика команда з Полтави. Окрім <a href="{H("furniture")}">хімчистки м\'яких меблів</a>, ми виконуємо хімчистку салону авто: очищаємо сидіння, обшивку й стелю, повертаючи інтер\'єру охайний вигляд.',
     f'<strong>Family Cleaning</strong> - небольшая команда из Полтавы. Кроме <a href="{H("furniture")}">химчистки мягкой мебели</a>, мы выполняем химчистку салона авто: чистим сиденья, обшивку и потолок, возвращая интерьеру аккуратный вид.')}</p>
<p>{t("Працюємо з професійними миючими засобами німецьких та українських виробників. Приймаємо замовлення по всьому місту та області - напишіть або зателефонуйте, і ми узгодимо деталі.",
     "Работаем с профессиональными моющими средствами немецких и украинских производителей. Принимаем заказы по всему городу и области - напишите или позвоните, и мы согласуем детали.")}</p>
</div>
</div>
</section>

<section class="section section--alt" id="faq">
<div class="container">
{section_head(t("Питання й відповіді", "Вопросы и ответы"), t("Часті запитання про хімчистку салону авто", "Частые вопросы о химчистке салона авто"))}
{faq_html(faq)}
</div>
</section>

{cta_band(t("Потрібна хімчистка салону авто?", "Нужна химчистка салона авто?"),
          t("Надішліть фото салону - розрахуємо вартість і узгодимо зручний час.", "Пришлите фото салона - рассчитаем стоимость и согласуем удобное время."))}

{related([
    (H("furniture"), t("Хімчистка м'яких меблів", "Химчистка мягкой мебели"), t("Дивани, крісла, стільці - від 200 грн", "Диваны, кресла, стулья - от 200 грн")),
    (H("cleaning"), t("Клінінг і прибирання", "Клининг и уборка"), t("Генеральне, після ремонту, вологе, вікна", "Генеральная, после ремонта, влажная, окна")),
])}"""
    return title, desc, [svc, breadcrumb_ld(name, "auto"), faq_ld(faq)], main


# ================================================================ CLEANING
def cleaning_faq():
    return [
        (t("Скільки коштує генеральне прибирання квартири в Полтаві?", "Сколько стоит генеральная уборка квартиры в Полтаве?"),
         t("Генеральне прибирання коштує від 70 грн за м². Остаточна вартість залежить від площі, стану приміщення та обсягу робіт, тому ми розраховуємо її індивідуально - найшвидше по фото.",
           "Генеральная уборка стоит от 70 грн за м². Окончательная стоимость зависит от площади, состояния помещения и объема работ, поэтому мы рассчитываем ее индивидуально - быстрее всего по фото.")),
        (t("Скільки коштує прибирання після ремонту?", "Сколько стоит уборка после ремонта?"),
         t("Прибирання після ремонту - від 70 грн за м². Остаточна сума залежить від площі та рівня забруднення будівельним пилом і сміттям.",
           "Уборка после ремонта - от 70 грн за м². Окончательная сумма зависит от площади и уровня загрязнения строительной пылью и мусором.")),
        (t("Скільки коштує вологе прибирання?", "Сколько стоит влажная уборка?"),
         t("Вологе прибирання - від 1500 грн. Вартість залежить від площі приміщення та складу робіт.",
           "Влажная уборка - от 1500 грн. Стоимость зависит от площади помещения и состава работ.")),
        (t("Як розраховується вартість миття вікон і фасадів?", "Как рассчитывается стоимость мытья окон и фасадов?"),
         t("За площею, від 150 грн за м². Надішліть фото вікон або фасаду - назвемо точну суму.",
           "По площади, от 150 грн за м². Пришлите фото окон или фасада - назовем точную сумму.")),
        (t("Які засоби ви використовуєте?", "Какие средства вы используете?"),
         t("Професійні миючі засоби німецьких та українських виробників. Якщо вдома є алергіки, діти чи домашні тварини, повідомте нас заздалегідь.",
           "Профессиональные моющие средства немецких и украинских производителей. Если дома есть аллергики, дети или домашние животные, сообщите нам заранее.")),
        (t("Чи можна розрахувати вартість по фото?", "Можно ли рассчитать стоимость по фото?"),
         t("Так. Надішліть кілька фото приміщення у Viber або Telegram й коротко опишіть завдання. Ми назвемо вартість і запропонуємо зручний час.",
           "Да. Пришлите несколько фото помещения в Viber или Telegram и коротко опишите задачу. Мы назовем стоимость и предложим удобное время.")),
        (t("Чи працюєте ви за межами Полтави?", "Работаете ли вы за пределами Полтавы?"),
         t("Так, приймаємо замовлення по всьому місту та області. Напишіть або зателефонуйте - узгодимо деталі.",
           "Да, принимаем заказы по всему городу и области. Напишите или позвоните - согласуем детали.")),
        (t("Як замовити прибирання?", "Как заказать уборку?"),
         t(f"Зателефонуйте за номером {PHONE_TXT} або напишіть у Viber чи Telegram. Ми розрахуємо вартість і узгодимо зручний для вас час.",
           f"Позвоните по номеру {PHONE_TXT} или напишите в Viber или Telegram. Мы рассчитаем стоимость и согласуем удобное для вас время.")),
    ]


def service_block(anchor, h2, paras, when_title, when_items, price_label, alt=False):
    ps = "\n".join(f"<p>{p}</p>" for p in paras)
    cls = "section section--alt" if alt else "section"
    return f"""<section class="{cls}" id="{anchor}">
<div class="container two-col">
<div class="prose">
<h2>{h2}</h2>
{ps}
<p><span class="price-chip">{price_label}</span></p>
<div class="btn-row">
<a class="btn btn--primary" href="tel:{PHONE_TEL}">{ico("phone")} {PHONE_TXT}</a>
<a class="btn btn--ghost" href="{VIBER}">{ico("camera")} {t("Розрахунок по фото", "Расчет по фото")}</a>
</div>
</div>
<div class="panel">
<h3>{when_title}</h3>
{checklist(when_items)}
</div>
</div>
</section>"""


def page_cleaning():
    faq = cleaning_faq()
    name = t("Клінінг і прибирання", "Клининг и уборка")
    title = t("Клінінг і прибирання в Полтаві: генеральне, після ремонту", "Клининг и уборка в Полтаве: генеральная, после ремонта")
    desc = t("Генеральне та вологе прибирання, прибирання після ремонту, миття вікон і фасадів у Полтаві й області. Ціни від 70 грн/м². Розрахунок по фото.",
             "Генеральная и влажная уборка, уборка после ремонта, мытье окон и фасадов в Полтаве и области. Цены от 70 грн/м². Расчет по фото.")
    svc = service_ld(name, t("Генеральне та вологе прибирання, прибирання після ремонту, миття вікон і фасадів, дезінсекція.",
                             "Генеральная и влажная уборка, уборка после ремонта, мытье окон и фасадов, дезинсекция."), "cleaning",
                     {"hasOfferCatalog": {"@type": "OfferCatalog", "name": t("Ціни на клінінг і прибирання", "Цены на клининг и уборку"),
                                          "itemListElement": cleaning_offers()}})
    fr = t("від", "от")
    m2 = "грн/м²"
    rows = "\n".join([
        table_row(thumb_img("mop", t("Вологе прибирання", "Влажная уборка")), t("Вологе прибирання", "Влажная уборка"), f"{fr} 1500 грн"),
        table_row(thumb_img("gen_clean", t("Генеральне прибирання", "Генеральная уборка")), t("Генеральне прибирання", "Генеральная уборка"), f"{fr} 70 {m2}"),
        table_row(thumb_img("after-repair", t("Прибирання після ремонту", "Уборка после ремонта")), t("Прибирання після ремонту", "Уборка после ремонта"), f"{fr} 70 {m2}"),
        table_row(thumb_img("window", t("Миття вікон та фасадів", "Мытье окон и фасадов")), t("Миття вікон та фасадів", "Мытье окон и фасадов"), f"{fr} 150 {m2}"),
        table_row(thumb_img("pest", t("Дезінсекція", "Дезинсекция")), t("Дезінсекція", "Дезинсекция"), t("індивідуально", "индивидуально")),
    ])
    blocks = [
        service_block("general", t("Генеральне прибирання в Полтаві", "Генеральная уборка в Полтаве"),
                      [t("Комплексне очищення всіх зон приміщення від бруду та пилу, включно з важкодоступними місцями. Підходить, коли звичайного прибирання вже недостатньо.",
                         "Комплексная чистка всех зон помещения от грязи и пыли, включая труднодоступные места. Подходит, когда обычной уборки уже недостаточно.")],
                      t("Коли варто замовити", "Когда стоит заказать"),
                      [t("до або після переїзду;", "до или после переезда;"),
                       t("перед здачею житла в оренду чи продажем;", "перед сдачей жилья в аренду или продажей;"),
                       t("перед святами або для сезонного оновлення;", "перед праздниками или для сезонного обновления;"),
                       t("коли давно не було повного прибирання.", "когда давно не было полной уборки.")],
                      t("від 70 грн/м²", "от 70 грн/м²")),
        service_block("after-repair", t("Прибирання після ремонту в Полтаві", "Уборка после ремонта в Полтаве"),
                      [t("Видаляємо залишки будівельного сміття, пилу та матеріалів. Працюємо швидко й дбайливо, не пошкоджуючи поверхні.",
                         "Убираем остатки строительного мусора, пыли и материалов. Работаем быстро и бережно, не повреждая поверхности."),
                       t("Будівельний пил осідає на всіх поверхнях, тому звичайне прибирання з ним зазвичай не справляється.",
                         "Строительная пыль оседает на всех поверхностях, поэтому обычная уборка с ней обычно не справляется.")],
                      t("Коли варто замовити", "Когда стоит заказать"),
                      [t("після косметичного чи капітального ремонту;", "после косметического или капитального ремонта;"),
                       t("перед заселенням у нову квартиру чи будинок;", "перед заселением в новую квартиру или дом;"),
                       t("після оздоблювальних робіт в офісі.", "после отделочных работ в офисе.")],
                      t("від 70 грн/м²", "от 70 грн/м²"), alt=True),
        service_block("wet", t("Вологе прибирання в Полтаві", "Влажная уборка в Полтаве"),
                      [t("Миття підлог і знепилення створює свіжу атмосферу вдома чи в офісі. Ідеально для регулярної чистоти.",
                         "Мытье полов и удаление пыли создают свежую атмосферу дома или в офисе. Идеально для регулярной чистоты.")],
                      t("Коли варто замовити", "Когда стоит заказать"),
                      [t("для регулярної підтримки чистоти вдома чи в офісі;", "для регулярной поддержки чистоты дома или в офисе;"),
                       t("між генеральними прибираннями;", "между генеральными уборками;"),
                       t("коли потрібно швидко освіжити приміщення.", "когда нужно быстро освежить помещение.")],
                      t("від 1500 грн", "от 1500 грн")),
        service_block("windows", t("Миття вікон та фасадів у Полтаві", "Мытье окон и фасадов в Полтаве"),
                      [t("Повертаємо склу прозорість. Вартість розраховуємо за площею - надішліть фото вікон або фасаду, і ми назвемо точну суму.",
                         "Возвращаем стеклу прозрачность. Стоимость рассчитываем по площади - пришлите фото окон или фасада, и мы назовем точную сумму.")],
                      t("Коли варто замовити", "Когда стоит заказать"),
                      [t("скло втратило прозорість;", "стекло потеряло прозрачность;"),
                       t("після ремонту чи зими;", "после ремонта или зимы;"),
                       t("перед святами чи відкриттям приміщення.", "перед праздниками или открытием помещения.")],
                      t("від 150 грн/м²", "от 150 грн/м²"), alt=True),
        service_block("pest", t("Дезінсекція в Полтаві", "Дезинсекция в Полтаве"),
                      [t("Знищення тарганів, мурах, комарів та інших шкідників. Використовуємо безпечні методи з тривалим захисним ефектом.",
                         "Уничтожение тараканов, муравьев, комаров и других вредителей. Используем безопасные методы с длительным защитным эффектом."),
                       t("Вартість розраховуємо індивідуально - напишіть або зателефонуйте, і ми узгодимо деталі.",
                         "Стоимость рассчитываем индивидуально - напишите или позвоните, и мы согласуем детали.")],
                      t("Коли варто замовити", "Когда стоит заказать"),
                      [t("у квартирі чи будинку з'явилися таргани або мурахи;", "в квартире или доме появились тараканы или муравьи;"),
                       t("потрібно позбутися комарів та інших шкідників.", "нужно избавиться от комаров и других вредителей.")],
                      t("вартість - індивідуально", "стоимость - индивидуально")),
    ]
    main = f"""{hero_page(name, t("Клінінг і прибирання в Полтаві", "Клининг и уборка в Полтаве"),
                          t("Генеральне й вологе прибирання, прибирання після ремонту, миття вікон і фасадів, дезінсекція. Професійні засоби та чесні ціни без прихованих доплат.",
                            "Генеральная и влажная уборка, уборка после ремонта, мытье окон и фасадов, дезинсекция. Профессиональные средства и честные цены без скрытых доплат."),
                          t("Розрахунок по фото", "Расчет по фото"))}

<section class="section" id="prices">
<div class="container">
{section_head(t("Прайс", "Прайс"), t("Ціни на клінінг у Полтаві", "Цены на клининг в Полтаве"),
              t("Вказано мінімальну вартість. Остаточна сума залежить від площі, стану приміщення та обсягу робіт.",
                "Указана минимальная стоимость. Окончательная сумма зависит от площади, состояния помещения и объема работ."))}
<div class="table-wrap">
<table class="price-table">
<caption class="sr-only">{t("Ціни на клінінг і прибирання в Полтаві", "Цены на клининг и уборку в Полтаве")}</caption>
<thead><tr><th scope="col">{t("Послуга", "Услуга")}</th><th scope="col">{t("Вартість", "Стоимость")}</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
<p class="price-note">{t("Потрібне прибирання, якого немає в переліку? Напишіть нам - розрахуємо вартість індивідуально.",
                         "Нужна уборка, которой нет в списке? Напишите нам - рассчитаем стоимость индивидуально.")}</p>
<div class="price-cta"><a class="btn btn--primary" href="{VIBER}">{ico("camera")} {t("Надіслати фото для розрахунку", "Отправить фото для расчета")}</a></div>
</div>
</section>

{chr(10).join(blocks)}

<section class="section section--alt">
<div class="container two-col">
<div class="prose">
<h2>{t("Скільки коштує прибирання", "Сколько стоит уборка")}</h2>
<p>{t("Ціна залежить від виду послуги, площі приміщення, його стану та обсягу робіт, тому точну суму ми називаємо індивідуально.",
     "Цена зависит от вида услуги, площади помещения, его состояния и объема работ, поэтому точную сумму мы называем индивидуально.")}</p>
<p>{t("Надішліть кілька фото у Viber або Telegram - ми розрахуємо вартість і запропонуємо зручний час.",
     "Пришлите несколько фото в Viber или Telegram - мы рассчитаем стоимость и предложим удобное время.")}</p>
</div>
<div class="panel">
<h3>{t("Що впливає на ціну", "Что влияет на цену")}</h3>
{checklist([
    t("<strong>Площа приміщення.</strong> Генеральне прибирання, прибирання після ремонту та миття вікон рахуємо за м².", "<strong>Площадь помещения.</strong> Генеральную уборку, уборку после ремонта и мытье окон считаем за м²."),
    t("<strong>Стан приміщення.</strong> Рівень забруднення впливає на обсяг роботи.", "<strong>Состояние помещения.</strong> Уровень загрязнения влияет на объем работы."),
    t("<strong>Вид послуги.</strong> Вологе, генеральне, після ремонту чи миття вікон.", "<strong>Вид услуги.</strong> Влажная, генеральная, после ремонта или мытье окон."),
    t("<strong>Обсяг робіт.</strong> Усе приміщення чи окремі зони.", "<strong>Объем работ.</strong> Все помещение или отдельные зоны."),
])}
</div>
</div>
</section>

<section class="section" id="how">
<div class="container">
{section_head(t("Процес", "Процесс"), t("Як проходить прибирання", "Как проходит уборка"))}
{steps([
    (t("Розрахунок", "Расчет"), t("Телефонуєте або надсилаєте фото приміщення. Ми називаємо вартість.", "Звоните или присылаете фото помещения. Мы называем стоимость.")),
    (t("Домовленість", "Договоренность"), t("Узгоджуємо зручні для вас час і адресу.", "Согласуем удобные для вас время и адрес.")),
    (t("Прибирання", "Уборка"), t("Приїжджаємо у вказаний час і прибираємо професійними засобами.", "Приезжаем в назначенное время и убираем профессиональными средствами.")),
    (t("Результат", "Результат"), t("Ви оглядаєте результат і залишаєтесь із чистим приміщенням.", "Вы осматриваете результат и остаетесь с чистым помещением.")),
])}
</div>
</section>

<section class="section section--alt">
<div class="container">
<div class="prose">
<h2>{t("Клінінгові послуги в Полтаві та області", "Клининговые услуги в Полтаве и области")}</h2>
<p>{t(f'<strong>Family Cleaning</strong> - невелика команда з Полтави, яка щиро любить чистоту. Окрім клінінгу, ми виконуємо <a href="{H("furniture")}">хімчистку м\'яких меблів</a> і <a href="{H("auto")}">хімчистку салону авто</a>.',
     f'<strong>Family Cleaning</strong> - небольшая команда из Полтавы, которая искренне любит чистоту. Кроме клининга, мы выполняем <a href="{H("furniture")}">химчистку мягкой мебели</a> и <a href="{H("auto")}">химчистку салона авто</a>.')}</p>
<p>{t("Працюємо уважно, акуратно й з повагою до вашого простору. Використовуємо професійні миючі засоби німецьких та українських виробників і приймаємо замовлення по всьому місту та області.",
     "Работаем внимательно, аккуратно и с уважением к вашему пространству. Используем профессиональные моющие средства немецких и украинских производителей и принимаем заказы по всему городу и области.")}</p>
</div>
</div>
</section>

<section class="section" id="faq">
<div class="container">
{section_head(t("Питання й відповіді", "Вопросы и ответы"), t("Часті запитання про клінінг і прибирання", "Частые вопросы о клининге и уборке"))}
{faq_html(faq)}
</div>
</section>

{cta_band(t("Потрібне прибирання в Полтаві?", "Нужна уборка в Полтаве?"),
          t("Зателефонуйте або надішліть фото - розрахуємо вартість і узгодимо зручний час.", "Позвоните или пришлите фото - рассчитаем стоимость и согласуем удобное время."))}

{related([
    (H("furniture"), t("Хімчистка м'яких меблів", "Химчистка мягкой мебели"), t("Дивани, крісла, стільці - від 200 грн", "Диваны, кресла, стулья - от 200 грн")),
    (H("auto"), t("Хімчистка салону авто", "Химчистка салона авто"), t("Сидіння, обшивка, стеля", "Сиденья, обшивка, потолок")),
])}"""
    return title, desc, [svc, breadcrumb_ld(name, "cleaning"), faq_ld(faq)], main


# ================================================================ 404 / службові файли
def build_404():
    global LANG, CUR, ABS
    LANG, CUR, ABS = "uk", "/404.html", True
    main = f"""<section class="section">
<div class="container prose prose-center">
<span class="eyebrow">404</span>
<h1>Сторінку не знайдено</h1>
<p>Можливо, посилання застаріло. Перейдіть на головну або зателефонуйте нам - допоможемо із замовленням.</p>
<h2 class="h-ru">Страница не найдена</h2>
<p>Возможно, ссылка устарела. Перейдите на главную или позвоните нам - поможем с заказом.</p>
<div class="btn-row" style="justify-content:center">
<a class="btn btn--primary" href="./">На головну</a>
<a class="btn btn--ghost" href="ru/">На главную (RU)</a>
<a class="btn btn--ghost" href="tel:{PHONE_TEL}">{ico("phone")} {PHONE_TXT}</a>
</div>
</div>
</section>"""
    page = head("Сторінку не знайдено - Family Cleaning", "Такої сторінки не існує. Поверніться на головну Family Cleaning.", "home", noindex=True)
    page = page.replace(' data-alt="/ru/"', "")
    base = ("<script>(function(){var l=location,b='/';if(l.protocol==='file:'){b=l.href.slice(0,l.href.lastIndexOf('/')+1);}"
            "else if(/\\.github\\.io$/.test(l.hostname)){b='/'+(l.pathname.split('/')[1]||'')+'/';}"
            "document.write('<base href=\"'+b+'\">');})();</script>")
    page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + base, 1)
    page += "\n" + header("home") + f'\n<main id="main">\n\n{main}\n\n</main>\n' + footer()
    return page


def write(path, content):
    for ch in ("—", "–"):  # довгі тире: на сайті тільки дефіс
        content = content.replace(" " + ch + " ", " - ").replace(ch, "-")
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def build():
    global LANG, CUR, ABS
    builders = {"home": page_home, "furniture": page_furniture, "auto": page_auto, "cleaning": page_cleaning}
    for lang in LANGS:
        for key, fn in builders.items():
            LANG, CUR, ABS = lang, purl(key, lang), False
            title, desc, schemas, main = fn()
            page = render(title, desc, key, schemas, main)
            out = purl(key, lang).strip("/")
            write((out + "/index.html") if out else "index.html", page)
    write("404.html", build_404())

    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key in PAGES:
        for lang in LANGS:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{purl(key, l)}"/>' for l in LANGS)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{purl(key, "uk")}"/>'
            sm.append(f"  <url><loc>{SITE}{purl(key, lang)}</loc><lastmod>{TODAY}</lastmod>{alts}</url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    manifest = {"name": "Family Cleaning", "short_name": "FamClean", "lang": "uk", "start_url": "/", "display": "standalone",
                "theme_color": "#2b7ba3", "background_color": "#ffffff",
                "icons": [{"src": "/img/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "/img/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}]}
    write("site.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print("built")


if __name__ == "__main__":
    build()
