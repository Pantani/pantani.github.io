"""Canonical URLs and localized metadata for the public static artifact."""

import json

from bs4 import BeautifulSoup

DOMAIN = "https://pantani.xyz"
MODIFIED = "2026-10-09"
IMAGE = f"{DOMAIN}/assets/social-card.jpg"
LANGUAGES = {"en": "en", "pt": "pt-BR"}
LABELS = {
    "en": {
        "work": "Engineering case studies",
        "home": "Portfolio",
        "contact": "Contact",
        "skip": "Skip to content",
        "sources": "Public sources",
        "updated": "Updated",
        "hub_description": "Go backend engineering, developer tooling and protocol contributions with public implementation evidence.",
        "remote": "Based in Brazil (UTC−3), seeking remote Go/backend opportunities with employers outside Brazil.",
        "role": "Senior Backend Engineer",
    },
    "pt": {
        "work": "Estudos de caso de engenharia",
        "home": "Portfólio",
        "contact": "Contato",
        "skip": "Ir para o conteúdo",
        "sources": "Fontes públicas",
        "updated": "Atualizado em",
        "hub_description": "Engenharia backend Go, ferramentas para desenvolvedores e contribuições em protocolos com evidências públicas de implementação.",
        "remote": "Resido no Brasil (UTC−3) e busco oportunidades remotas em Go/backend com empregadores de fora do Brasil.",
        "role": "Engenheiro Backend Sênior",
    },
}


def route(language, suffix=""):
    prefix = "/pt/" if language == "pt" else "/"
    return prefix + suffix


def absolute(path):
    return DOMAIN + path


def append_tag(soup, name, attrs, text=None):
    tag = soup.new_tag(name, attrs=attrs)
    if text is not None:
        tag.string = text
    soup.head.append(tag)
    return tag


def json_ld(soup, entity):
    data = {"@context": "https://schema.org", **entity}
    encoded = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    append_tag(soup, "script", {"type": "application/ld+json"}, encoded)


def person(language, description):
    return {
        "@type": "Person",
        "@id": f"{DOMAIN}/#person",
        "name": "Danilo Pantani",
        "url": f"{DOMAIN}/",
        "image": IMAGE,
        "email": "mailto:danpantani@gmail.com",
        "jobTitle": LABELS[language]["role"],
        "description": description,
        "homeLocation": {"@type": "Place", "name": "Brazil"},
        "sameAs": [
            "https://github.com/Pantani",
            "https://www.linkedin.com/in/dpantani/",
        ],
    }


def profile_entities(soup, language, path, description):
    json_ld(
        soup,
        {
            "@type": "ProfilePage",
            "@id": absolute(path) + "#profile",
            "url": absolute(path),
            "inLanguage": LANGUAGES[language],
            "dateModified": MODIFIED,
            "mainEntity": person(language, description),
        },
    )
    if language == "en":
        json_ld(
            soup,
            {
                "@type": "WebSite",
                "@id": f"{DOMAIN}/#website",
                "url": f"{DOMAIN}/",
                "name": "Danilo Pantani",
                "inLanguage": ["en", "pt-BR"],
                "publisher": {"@id": f"{DOMAIN}/#person"},
            },
        )


def breadcrumbs(soup, language, path, title):
    items = [
        (LABELS[language]["home"], route(language)),
        (LABELS[language]["work"], route(language, "work/")),
        (title, path),
    ]
    elements = [
        {"@type": "ListItem", "position": position, "name": name, "item": absolute(url)}
        for position, (name, url) in enumerate(items, start=1)
    ]
    json_ld(
        soup,
        {
            "@type": "BreadcrumbList",
            "@id": absolute(path) + "#breadcrumbs",
            "itemListElement": elements,
        },
    )


def article_entities(soup, language, path, item):
    content = item[language]
    json_ld(
        soup,
        {
            "@type": "Article",
            "@id": absolute(path) + "#article",
            "url": absolute(path),
            "headline": content["title"],
            "description": content["description"],
            "inLanguage": LANGUAGES[language],
            "dateModified": item["dateModified"],
            "image": IMAGE,
            "author": {
                "@type": "Person",
                "@id": f"{DOMAIN}/#person",
                "name": "Danilo Pantani",
            },
            "mainEntityOfPage": absolute(path),
        },
    )
    breadcrumbs(soup, language, path, content["title"])


def social_metadata(soup, language, path, title, description, kind):
    fields = {
        "og:type": kind,
        "og:title": title,
        "og:description": description,
        "og:url": absolute(path),
        "og:site_name": "Danilo Pantani",
        "og:locale": {"en": "en_US", "pt": "pt_BR"}[language],
        "og:locale:alternate": {"en": "pt_BR", "pt": "en_US"}[language],
        "og:image": IMAGE,
        "og:image:type": "image/jpeg",
        "og:image:width": "1200",
        "og:image:height": "630",
        "og:image:alt": title,
    }
    for key, value in fields.items():
        append_tag(soup, "meta", {"property": key, "content": value})
    twitter = {
        "card": "summary_large_image",
        "title": title,
        "description": description,
        "image": IMAGE,
        "image:alt": title,
    }
    for key, value in twitter.items():
        append_tag(soup, "meta", {"name": "twitter:" + key, "content": value})


def metadata(
    soup, language, suffix, title, description, kind="website", indexable=True
):
    soup.html["lang"] = LANGUAGES[language]
    soup.head.clear()
    append_tag(soup, "meta", {"charset": "utf-8"})
    append_tag(
        soup,
        "meta",
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    )
    append_tag(soup, "title", {}, title)
    append_tag(soup, "meta", {"name": "description", "content": description})
    robots = (
        "index, follow, max-image-preview:large" if indexable else "noindex, follow"
    )
    append_tag(soup, "meta", {"name": "robots", "content": robots})
    append_tag(soup, "meta", {"name": "theme-color", "content": "#fbf8f2"})
    append_tag(
        soup,
        "link",
        {"rel": "icon", "type": "image/jpeg", "href": "/assets/favicon.jpg"},
    )
    append_tag(soup, "link", {"rel": "stylesheet", "href": "/assets/fonts.css"})
    if indexable:
        indexable_metadata(soup, language, suffix, title, description, kind)


def indexable_metadata(soup, language, suffix, title, description, kind):
    path = route(language, suffix)
    append_tag(soup, "link", {"rel": "canonical", "href": absolute(path)})
    for code, value in LANGUAGES.items():
        append_tag(
            soup,
            "link",
            {
                "rel": "alternate",
                "hreflang": value,
                "href": absolute(route(code, suffix)),
            },
        )
    append_tag(
        soup,
        "link",
        {
            "rel": "alternate",
            "hreflang": "x-default",
            "href": absolute(route("en", suffix)),
        },
    )
    social_metadata(soup, language, path, title, description, kind)


def blank_page():
    return BeautifulSoup(
        "<!doctype html><html><head></head><body></body></html>", "html.parser"
    )
