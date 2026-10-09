"""Render evidence-backed case studies as complete bilingual HTML documents."""

from datetime import date
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from bs4 import BeautifulSoup

from site_metadata import (
    LABELS,
    MODIFIED,
    absolute,
    append_tag,
    article_entities,
    blank_page,
    json_ld,
    metadata,
    route,
)


def load_cases(source):
    items = json.loads(
        (Path(source) / "content/case-studies.json").read_text(encoding="utf-8")
    )
    if not isinstance(items, list):
        raise ValueError("Case studies must be an array")
    for item in items:
        validate_case(item)
    slugs = [item["slug"] for item in items]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Case-study slugs must be unique")
    return items


def validate_case(item):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", item["slug"]):
        raise ValueError("Unsafe case-study slug")
    date.fromisoformat(item["dateModified"])
    for language in ("en", "pt"):
        validate_localized(item[language])


def validate_localized(content):
    for key in ("title", "description", "lead"):
        require_text(content[key])
    for section in content["sections"]:
        require_text(section["title"])
        for text in section["paragraphs"] + section.get("bullets", []):
            require_text(text)
    for source in content["sources"]:
        if urlsplit(source["url"]).scheme not in ("http", "https"):
            raise ValueError("Case-study sources must use HTTP or HTTPS")


def require_text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Case-study text must be a nonempty string")


def fragment(markup):
    return BeautifulSoup(markup, "html.parser").contents


def card(item, language, heading="h3"):
    content = item[language]
    url = route(language, "work/" + item["slug"] + "/")
    return (
        f'<article class="work-card"><{heading}><a href="'
        + url
        + '">'
        + escape(content["title"])
        + f"</a></{heading}><p>"
        + escape(content["description"])
        + "</p></article>"
    )


def cards(items, language, heading="h3"):
    return (
        '<div class="work-grid">'
        + "".join(card(item, language, heading) for item in items)
        + "</div>"
    )


def language_links(language, suffix=""):
    links = []
    for code, label in (("en", "EN"), ("pt", "PT-BR")):
        current = ' aria-current="page"' if code == language else ""
        hreflang = "pt-BR" if code == "pt" else "en"
        links.append(
            f'<a class="lang-button" data-lang="{code}" hreflang="{hreflang}" '
            f'href="{route(code, suffix)}"{current}>{label}</a>'
        )
    return " ".join(links)


def navigation(language, suffix="", with_languages=True):
    labels = LABELS[language]
    languages = ""
    if with_languages:
        languages = (
            f'<span class="language-links">{language_links(language, suffix)}</span>'
        )
    return (
        f'<nav class="site-navigation" aria-label="{labels["home"]}">'
        f'<a href="{route(language)}">{labels["home"]}</a>'
        f'<a href="{route(language, "work/")}">{labels["work"]}</a>'
        f'<a href="mailto:danpantani@gmail.com">{labels["contact"]}</a>'
        f"{languages}</nav>"
    )


def frame(soup, language, suffix, body):
    labels = LABELS[language]
    markup = (
        f'<a class="skip-link" href="#main">{labels["skip"]}</a>'
        f'<header class="site-header"><a class="brand" href="{route(language)}">Danilo Pantani</a>'
        + navigation(language, suffix)
        + "</header>"
        + body
        + f'<footer class="site-footer"><p>© 2026 Danilo Pantani · {labels["updated"]} {MODIFIED}</p>'
        f'<a href="mailto:danpantani@gmail.com">{labels["contact"]}</a></footer>'
    )
    soup.body.extend(fragment(markup))
    append_tag(soup, "link", {"rel": "stylesheet", "href": "/assets/article.css"})
    return soup


def hub(items, language):
    labels = LABELS[language]
    soup = blank_page()
    metadata(
        soup,
        language,
        "work/",
        labels["work"] + " | Danilo Pantani",
        labels["hub_description"],
    )
    json_ld(
        soup,
        {
            "@type": "CollectionPage",
            "@id": absolute(route(language, "work/")) + "#collection",
            "url": absolute(route(language, "work/")),
            "name": labels["work"],
            "inLanguage": soup.html["lang"],
            "dateModified": MODIFIED,
        },
    )
    body = (
        f'<main id="main" class="article-shell"><h1>{labels["work"]}</h1>'
        f'<p class="lead">{labels["hub_description"]}</p>'
        + cards(items, language, heading="h2")
        + "</main>"
    )
    return frame(soup, language, "work/", body)


def section_html(section):
    paragraphs = "".join(
        "<p>" + escape(text) + "</p>" for text in section["paragraphs"]
    )
    bullets = "".join(
        "<li>" + escape(text) + "</li>" for text in section.get("bullets", [])
    )
    listing = "<ul>" + bullets + "</ul>" if bullets else ""
    return (
        "<section><h2>"
        + escape(section["title"])
        + "</h2>"
        + paragraphs
        + listing
        + "</section>"
    )


def sources_html(item, language):
    links = [
        f'<li><a href="{escape(source["url"], quote=True)}">{escape(source["label"])}</a></li>'
        for source in item[language]["sources"]
    ]
    return (
        '<section class="article-sources"><h2>'
        + LABELS[language]["sources"]
        + "</h2><ul>"
        + "".join(links)
        + "</ul></section>"
    )


def article(item, language):
    content = item[language]
    suffix = "work/" + item["slug"] + "/"
    soup = blank_page()
    metadata(
        soup,
        language,
        suffix,
        content["title"] + " | Danilo Pantani",
        content["description"],
        "article",
    )
    article_entities(soup, language, route(language, suffix), item)
    labels = LABELS[language]
    crumb = (
        f'<nav class="breadcrumbs" aria-label="Breadcrumb">'
        f'<a href="{route(language)}">{labels["home"]}</a> / '
        f'<a href="{route(language, "work/")}">{labels["work"]}</a> / '
        f'<span aria-current="page">{escape(content["title"])}</span></nav>'
    )
    sections = "".join(section_html(section) for section in content["sections"])
    body = (
        '<main id="main" class="article-shell">'
        + crumb
        + "<article><h1>"
        + escape(content["title"])
        + '</h1><p class="lead">'
        + escape(content["lead"])
        + "</p>"
        + sections
        + sources_html(item, language)
        + "</article></main>"
    )
    return frame(soup, language, suffix, body)


def not_found():
    soup = blank_page()
    metadata(
        soup,
        "en",
        "404.html",
        "Page not found | Danilo Pantani",
        "This page could not be found.",
        indexable=False,
    )
    return frame(
        soup,
        "en",
        "",
        '<main id="main" class="article-shell"><h1>Page not found</h1>'
        '<p><a href="/">Return to the portfolio</a>.</p></main>',
    )
