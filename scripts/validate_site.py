"""Reject crawlability, metadata, broken links and accidental source publication."""

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

from build_site import MANIFEST, MARKER, PUBLIC_ASSETS, PUBLIC_PDFS, PUBLIC_ROOT
from site_metadata import DOMAIN, IMAGE, absolute, route


def route_for(path, directory):
    relative = path.relative_to(directory).as_posix()
    if relative == "index.html":
        return "/"
    return "/" + relative.removesuffix("index.html")


def public_file(relative):
    path = relative.as_posix()
    fixed = {
        *PUBLIC_ROOT,
        MANIFEST,
        MARKER,
        ".nojekyll",
        "robots.txt",
        "sitemap.xml",
        "404.html",
    }
    if path in fixed or re.fullmatch(r"google[^/]+\.html", path):
        return True
    patterns = (
        r"(?:pt/)?(?:work/(?:[a-z0-9-]+/)?)?index\.html",
        r"assets/(?:"
        + "|".join(re.escape(name) for name in PUBLIC_ASSETS)
        + r"|portfolio\.css)",
        r"assets/fonts/[^/]+(?:\.woff2|OFL\.txt)",
        r"output/pdf/(?:" + "|".join(re.escape(name) for name in PUBLIC_PDFS) + ")",
    )
    return any(re.fullmatch(pattern, path) for pattern in patterns)


def collect_pages(directory, issues):
    pages = {}
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(directory)
        if not public_file(relative):
            issues.append(f"{relative}: source or unapproved file leaked into artifact")
        if path.name in ("index.html", "404.html"):
            pages[route_for(path, directory)] = BeautifulSoup(
                path.read_text(encoding="utf-8"), "html.parser"
            )
    return pages


def value(soup, selector, attribute="content"):
    tags = soup.select(selector)
    if len(tags) != 1:
        return None
    return tags[0].get(attribute)


def expect(actual, expected, label, issues):
    if actual != expected:
        issues.append(f"{label}: expected {expected!r}, got {actual!r}")


def validate_structure(soup, path, issues):
    expect(len(soup.select("h1")), 1, path + " h1 count", issues)
    validate_ids(soup, path, issues)
    if soup.select("style, [style]"):
        issues.append(f"{path}: inline CSS is forbidden")
    validate_head(soup, path, issues)
    validate_scripts(soup, path, issues)


def validate_ids(soup, path, issues):
    counts = Counter(tag["id"] for tag in soup.select("[id]"))
    for identifier, count in counts.items():
        if count > 1:
            issues.append(f"{path}: duplicate ID {identifier}")


def validate_head(soup, path, issues):
    if soup.head is None or soup.body is None:
        issues.append(f"{path}: missing head or body")
        return
    for child in soup.head.find_all(recursive=False):
        if child.name not in ("title", "meta", "link", "script"):
            issues.append(f"{path}: invalid element in head: {child.name}")


def validate_scripts(soup, path, issues):
    scripts = soup.select("script:not([type='application/ld+json'])")
    expected = []
    if path in ("/", "/pt/"):
        expected = [
            "/assets/site.js",
            "/assets/references-data.js",
            "/assets/references.js",
        ]
    expect(
        [script.get("src") for script in scripts],
        expected,
        path + " runtime scripts",
        issues,
    )
    for script in scripts:
        if not script.has_attr("src") or not script.has_attr("defer"):
            issues.append(f"{path}: inline or non-deferred runtime JS")


def equivalent(path):
    suffix = (
        path.removeprefix("/pt/") if path.startswith("/pt/") else path.removeprefix("/")
    )
    return {
        "en": absolute(route("en", suffix)),
        "pt-BR": absolute(route("pt", suffix)),
        "x-default": absolute(route("en", suffix)),
    }


def validate_alternates(soup, path, pages, issues):
    tags = soup.select("link[hreflang]")
    actual = {tag["hreflang"]: tag.get("href") for tag in tags}
    expect(actual, equivalent(path), path + " hreflang", issues)
    expect(len(tags), 3, path + " hreflang count", issues)
    for target in actual.values():
        validate_reciprocal(target, path, pages, issues)


def validate_reciprocal(target, path, pages, issues):
    destination = pages.get(urlsplit(target or "").path)
    if destination is None:
        issues.append(f"{path}: hreflang destination missing: {target}")
        return
    hrefs = {tag.get("href") for tag in destination.select("link[hreflang]")}
    if absolute(path) not in hrefs:
        issues.append(f"{path}: hreflang is not reciprocal: {target}")


def validate_social(soup, path, issues):
    title = soup.title.get_text() if soup.title else ""
    description = value(soup, "meta[name='description']")
    if not all((title.strip(), description)):
        issues.append(f"{path}: missing title or description")
    fields = {
        "og:title": title,
        "og:description": description,
        "og:url": absolute(path),
        "og:image": IMAGE,
        "og:image:width": "1200",
        "og:image:height": "630",
    }
    for key, expected in fields.items():
        expect(
            value(soup, f"meta[property='{key}']"), expected, path + " " + key, issues
        )
    validate_twitter(soup, path, title, description, issues)


def validate_twitter(soup, path, title, description, issues):
    twitter = {
        "title": title,
        "description": description,
        "image": IMAGE,
        "card": "summary_large_image",
    }
    for key, expected in twitter.items():
        expect(
            value(soup, f"meta[name='twitter:{key}']"),
            expected,
            path + " twitter:" + key,
            issues,
        )
    locale = "pt_BR" if path.startswith("/pt/") else "en_US"
    expect(
        value(soup, "meta[property='og:locale']"), locale, path + " og:locale", issues
    )
    if soup.select("[content='es_ES'], [hreflang='es'], [hreflang='es-ES']"):
        issues.append(f"{path}: obsolete Spanish metadata")


def parse_entities(soup, path, issues):
    entities = []
    for script in soup.select("script[type='application/ld+json']"):
        try:
            entity = json.loads(script.get_text())
        except json.JSONDecodeError as error:
            issues.append(f"{path}: invalid JSON-LD: {error.msg}")
            continue
        if not isinstance(entity, dict):
            issues.append(f"{path}: JSON-LD must be an object")
            continue
        if not isinstance(entity.get("@type"), str):
            issues.append(f"{path}: JSON-LD entity type must be a string")
            continue
        expect(
            entity.get("@context"),
            "https://schema.org",
            path + " JSON-LD context",
            issues,
        )
        entities.append(entity)
    return entities


def required_entities(path):
    if path == "/":
        return {"ProfilePage", "WebSite"}
    if path == "/pt/":
        return {"ProfilePage"}
    if path in ("/work/", "/pt/work/"):
        return {"CollectionPage"}
    return {"Article", "BreadcrumbList"}


def validate_entities(soup, path, issues):
    entities = parse_entities(soup, path, issues)
    types = {entity.get("@type") for entity in entities}
    expect(types, required_entities(path), path + " JSON-LD types", issues)
    for entity in entities:
        validate_entity(entity, path, issues)


def validate_entity(entity, path, issues):
    kind = entity.get("@type")
    if "datePublished" in entity:
        issues.append(f"{path}: unverified datePublished is forbidden")
    if "dateModified" in entity:
        validate_date(entity["dateModified"], path + " dateModified", issues)
    if kind == "ProfilePage":
        expect(
            nested_id(entity, "mainEntity"),
            DOMAIN + "/#person",
            path + " Person ID",
            issues,
        )
    if kind == "Article":
        expect(
            nested_id(entity, "author"),
            DOMAIN + "/#person",
            path + " author ID",
            issues,
        )
        expect(entity.get("url"), absolute(path), path + " Article URL", issues)
    if kind in ("ProfilePage", "Article", "CollectionPage"):
        expect(
            entity.get("inLanguage"),
            expected_language(path),
            path + " entity language",
            issues,
        )


def nested_id(entity, key):
    nested = entity.get(key)
    return nested.get("@id") if isinstance(nested, dict) else None


def validate_date(value, label, issues):
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError):
        issues.append(f"{label}: invalid ISO date")


def expected_language(path):
    return "pt-BR" if path.startswith("/pt/") else "en"


def validate_page(soup, path, pages, issues):
    validate_structure(soup, path, issues)
    expect(
        soup.html.get("lang") if soup.html else None,
        expected_language(path),
        path + " language",
        issues,
    )
    robots = value(soup, "meta[name='robots']")
    if path == "/404.html":
        expect(robots, "noindex, follow", path + " robots", issues)
        return
    expect(
        value(soup, "link[rel='canonical']", "href"),
        absolute(path),
        path + " canonical",
        issues,
    )
    expect(robots, "index, follow, max-image-preview:large", path + " robots", issues)
    validate_alternates(soup, path, pages, issues)
    validate_social(soup, path, issues)
    validate_entities(soup, path, issues)


def local_url(value, current):
    target = urlsplit(urljoin(absolute(current), value))
    if (
        target.scheme not in ("http", "https")
        or target.netloc != urlsplit(DOMAIN).netloc
    ):
        return None
    return target


def target_file(directory, path):
    candidate = directory / unquote(path).lstrip("/")
    if path.endswith("/"):
        candidate = candidate / "index.html"
    if not candidate.resolve().is_relative_to(directory.resolve()):
        return None
    return candidate


def validate_url(value, current, directory, pages, issues):
    target = local_url(value, current)
    if target is None:
        return
    candidate = target_file(directory, target.path)
    if candidate is None or not candidate.is_file():
        issues.append(f"{current}: missing local link {value}")
        return
    if target.fragment:
        validate_fragment(target, value, current, pages, issues)


def validate_fragment(target, value, current, pages, issues):
    page = pages.get(target.path)
    if page is None or page.find(id=unquote(target.fragment)) is None:
        issues.append(f"{current}: missing fragment {value}")


def validate_links(soup, current, directory, pages, issues):
    for tag in soup.select("[href], [src]"):
        for attribute in ("href", "src"):
            if tag.has_attr(attribute):
                validate_url(tag[attribute], current, directory, pages, issues)


def validate_styles(directory, pages, issues):
    for stylesheet in directory.rglob("*.css"):
        content = stylesheet.read_text(encoding="utf-8")
        current = "/" + stylesheet.relative_to(directory).as_posix()
        for match in re.finditer(r"url\(([^)]+)\)", content):
            target = match.group(1).strip().strip("\"'")
            validate_url(target, current, directory, pages, issues)


def validate_sitemap(directory, pages, issues):
    try:
        tree = ET.parse(directory / "sitemap.xml").getroot()
    except (OSError, ET.ParseError) as error:
        issues.append(f"sitemap: {error}")
        return
    expected = {absolute(path) for path in pages if path != "/404.html"}
    locations = [element.text for element in tree.findall("{*}url/{*}loc")]
    expect(set(locations), expected, "sitemap exact canonical pages", issues)
    expect(len(locations), len(expected), "sitemap duplicate count", issues)
    for entry in tree.findall("{*}url"):
        validate_sitemap_entry(entry, issues)
    modifications = manifest_pages(directory, issues)
    for entry in tree.findall("{*}url"):
        compare_lastmod(entry, modifications, issues)


def compare_lastmod(entry, modifications, issues):
    location, modified = entry.find("{*}loc"), entry.find("{*}lastmod")
    if location is None or modified is None:
        return
    expected = modifications.get(urlsplit(location.text or "").path)
    expect(
        modified.text, expected, "sitemap lastmod agrees with content manifest", issues
    )


def validate_sitemap_entry(entry, issues):
    url = sitemap_location(entry)
    if any((url.query, url.fragment, not url.path.endswith("/"))):
        issues.append("sitemap: noncanonical URL")
    lastmod = entry.find("{*}lastmod")
    if lastmod is None:
        issues.append("sitemap: missing lastmod")
    else:
        validate_date(lastmod.text, "sitemap lastmod", issues)
    if any(entry.find("{*}" + name) is not None for name in ("priority", "changefreq")):
        issues.append("sitemap: misleading priority or changefreq")


def sitemap_location(entry):
    location = entry.find("{*}loc")
    return urlsplit(location.text or "") if location is not None else urlsplit("")


def validate_robots(directory, issues):
    path = directory / "robots.txt"
    if not path.exists():
        issues.append("robots.txt: missing")
        return
    content = path.read_text(encoding="utf-8")
    for expected in (DOMAIN + "/sitemap.xml", DOMAIN + "/triton-l200-hpe/sitemap.xml"):
        if "Sitemap: " + expected not in content:
            issues.append("robots.txt: missing sitemap " + expected)


def validate_directory(directory):
    directory = Path(directory)
    issues = []
    pages = collect_pages(directory, issues)
    validate_manifest(directory, pages, issues)
    for path, soup in pages.items():
        validate_page(soup, path, pages, issues)
        validate_links(soup, path, directory, pages, issues)
    validate_styles(directory, pages, issues)
    validate_sitemap(directory, pages, issues)
    validate_robots(directory, issues)
    return issues


def validate_manifest(directory, pages, issues):
    paths = set(manifest_pages(directory, issues))
    expect(paths, set(pages) - {"/404.html"}, "manifest exact canonical pages", issues)
    required = {"/", "/pt/", "/work/", "/pt/work/"}
    if not required.issubset(paths):
        issues.append("manifest: mandatory home and work pages missing")
    expect("/404.html" in pages, True, "artifact 404 page", issues)


def manifest_pages(directory, issues):
    try:
        manifest = json.loads((directory / MANIFEST).read_text(encoding="utf-8"))
        modifications = {entry["path"]: entry["lastmod"] for entry in manifest["pages"]}
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        issues.append(f"manifest: invalid or missing artifact manifest: {error}")
        return {}
    expect(
        len(modifications), len(manifest["pages"]), "manifest duplicate pages", issues
    )
    return modifications


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory", type=Path, default=Path(__file__).resolve().parents[1] / "_site"
    )
    arguments = parser.parse_args()
    issues = validate_directory(arguments.directory)
    if issues:
        for issue in issues:
            print(issue)
        parser.exit(1, f"Site validation failed: {len(issues)} finding(s)\n")
    print(
        "Site validation passed: canonical pages, metadata, links and public artifact checked"
    )


if __name__ == "__main__":
    main()
