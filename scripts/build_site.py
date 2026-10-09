"""Build an explicit public artifact without changing the canonical CV source."""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

from site_content import (
    article,
    cards,
    fragment,
    hub,
    load_cases,
    not_found,
)
from site_metadata import (
    LABELS,
    LANGUAGES,
    MODIFIED,
    absolute,
    append_tag,
    metadata,
    profile_entities,
    route,
)

ROOT = Path(__file__).resolve().parents[1]
MARKER = ".portfolio-site-build"
MARKER_TEXT = "Portfolio static artifact\n"
MANIFEST = ".site-manifest.json"
PUBLIC_ROOT = (
    "CNAME",
    "favicon.svg",
    "favicon.ico",
    "apple-touch-icon.png",
    "og-image.png",
    "og-image.jpg",
    "user-card-background.png",
    "linkedin-cover.png",
    "portrait.png",
)
PUBLIC_ASSETS = (
    "site.js",
    "references.js",
    "references-data.js",
    "article.css",
    "home-seo.css",
    "fonts.css",
    "social-card.jpg",
    "favicon.jpg",
    "favicon.svg",
)
PUBLIC_PDFS = (
    "danilo-pantani-cv-en.pdf",
    "danilo-pantani-cv-pt-br.pdf",
    "danilo-pantani-cv-en-references.pdf",
    "danilo-pantani-cv-pt-br-references.pdf",
)
NODE_TRANSLATIONS = """
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync(0, 'utf8');
const marker = /const\\s+translations\\s*=\\s*/.exec(source);
if (!marker) throw new Error('Missing source translation dictionary');
const tail = source.slice(marker.index + marker[0].length);
function candidate(end) {
  try { return vm.runInNewContext('(' + tail.slice(0, end + 1) + ')', {}, {timeout: 1000}); }
  catch (error) { if (error instanceof SyntaxError || error.name === 'SyntaxError') return null; throw error; }
}
let dictionary;
for (let end = tail.indexOf('}'); end !== -1; end = tail.indexOf('}', end + 1)) {
  dictionary = candidate(end);
  if (dictionary && dictionary.en && dictionary.pt) break;
}
if (!dictionary || !dictionary.en || !dictionary.pt) throw new Error('Invalid source translation dictionary');
process.stdout.write(JSON.stringify(dictionary));
"""


def translations(source):
    result = subprocess.run(
        ["node", "-e", NODE_TRANSLATIONS],
        input=source,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def guard_output(source, output):
    if output.is_symlink():
        raise ValueError("Output cannot be a symlink")
    source, output = source.resolve(), output.resolve()
    if output == source or output in source.parents:
        raise ValueError("Output cannot overwrite the source or its parent")
    if output.is_relative_to(source):
        relative = output.relative_to(source)
        if relative.parts[0] != "_site":
            raise ValueError("In-repository output must be inside _site")
    return output


def prepare_output(source, output):
    output = guard_output(source, output)
    if output.exists() and any(output.iterdir()):
        marker = output / MARKER
        if not marker.is_file() or marker.read_text(encoding="utf-8") != MARKER_TEXT:
            raise ValueError(
                "Refusing to clean an output directory not owned by this build"
            )
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / MARKER).write_text(MARKER_TEXT, encoding="utf-8")
    (output / ".nojekyll").touch()
    return output


def write(output, path, content):
    destination = output / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def copy_public(source, output, path):
    origin = source / path
    if origin.is_file():
        destination = output / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin, destination)


def copy_assets(source, output):
    for path in PUBLIC_ROOT:
        copy_public(source, output, path)
    for name in PUBLIC_ASSETS:
        copy_public(source, output, "assets/" + name)
    for name in PUBLIC_PDFS:
        copy_public(source, output, "output/pdf/" + name)
    for verification in source.glob("google*.html"):
        copy_public(source, output, verification.name)
    copy_fonts(source, output)


def copy_fonts(source, output):
    for origin in sorted((source / "assets/fonts").glob("*")):
        if origin.suffix == ".woff2" or origin.name.endswith("OFL.txt"):
            copy_public(source, output, origin.relative_to(source))


def root_url(value):
    if value.startswith(("#", "?")) or urlsplit(value).scheme:
        return value
    return urljoin("/", value)


def rewrite_urls(soup):
    for tag in soup.select("[href], [src]"):
        for attribute in ("href", "src"):
            if tag.has_attr(attribute):
                tag[attribute] = root_url(tag[attribute])


def css_urls(css):
    def replace(match):
        value = match.group(1).strip().strip("\"'")
        return 'url("' + root_url(value) + '")'

    return re.sub(r"url\(([^)]+)\)", replace, css)


def replace_html(tag, value):
    tag.clear()
    tag.extend(fragment(value))


def translate(soup, dictionary):
    for tag in soup.select("[data-i18n]"):
        tag.string = dictionary[tag["data-i18n"]]
    for tag in soup.select("[data-i18n-html]"):
        replace_html(tag, dictionary[tag["data-i18n-html"]])
    for tag in soup.select("[data-i18n-attr]"):
        key = tag.get("data-i18n-attr-key", tag.get("data-i18n"))
        tag[tag["data-i18n-attr"]] = dictionary[key]


def extract_inline_styles(soup, rules):
    for tag in soup.select("[style]"):
        rule = tag["style"]
        if rule not in rules:
            rules[rule] = "generated-style-" + str(len(rules) + 1)
        tag["class"] = tag.get("class", []) + [rules[rule]]
        del tag["style"]


def language_controls(soup, language):
    for tag in soup.select(".lang-button[data-lang]"):
        code = tag["data-lang"]
        tag.name = "a"
        tag.attrs.pop("type", None)
        tag.attrs.pop("aria-pressed", None)
        tag.attrs.pop("aria-current", None)
        tag["href"] = route(code)
        tag["hreflang"] = LANGUAGES[code]
        if code == language:
            tag["aria-current"] = "page"


def home_runtime(soup):
    for script in soup.select("script:not([type='application/ld+json'])"):
        script.decompose()
    for path in ("site.js", "references-data.js", "references.js"):
        script = soup.new_tag("script", attrs={"defer": "", "src": "/assets/" + path})
        soup.body.append(script)


def home_details(soup, language):
    heading = soup.h1
    if "Danilo Pantani" not in heading.get_text(" ", strip=True):
        name = soup.new_tag("span", attrs={"class": "sr-only"})
        name.string = "Danilo Pantani — "
        heading.insert(0, name)
    for tag in soup.select("[data-pdf-download]"):
        code = "pt-br" if language == "pt" else "en"
        tag["href"] = "/output/pdf/danilo-pantani-cv-" + code + ".pdf"
        tag["download"] = "Danilo-Pantani-CV-" + code.upper() + ".pdf"
    toggle = soup.select_one("#referencesToggle")
    if toggle is not None:
        toggle.string = "Com referências" if language == "pt" else "With references"
        toggle["href"] = "?references=1"


def home_additions(soup, language, items):
    labels = LABELS[language]
    statement = soup.new_tag(
        "p", attrs={"class": "remote-statement site-only print-hidden"}
    )
    statement.string = labels["remote"]
    hero = soup.select_one(".hero-summary")
    target = hero if hero is not None else soup.h1
    target.insert_after(statement)
    section = (
        f'<section class="case-studies site-only print-hidden" aria-labelledby="case-studies-title">'
        f'<h2 id="case-studies-title">{labels["work"]}</h2>'
        + cards(items, language)
        + "</section>"
    )
    section_node = BeautifulSoup(section, "html.parser").section
    footer = soup.select_one(".resume-footer")
    if footer is not None:
        footer.insert_before(section_node)
    else:
        soup.main.append(section_node)


def relocate_impact(soup):
    impact, column = (
        soup.select_one("#protocol-impact"),
        soup.select_one(".main-column"),
    )
    if impact is not None and column is not None:
        column.insert(0, impact.extract())


def home(source, dictionary, language, items, inline_rules):
    soup = BeautifulSoup(source, "html.parser")
    translate(soup, dictionary[language])
    for obsolete in soup.select(".contact-cta"):
        obsolete.decompose()
    relocate_impact(soup)
    extract_inline_styles(soup, inline_rules)
    metadata(
        soup,
        language,
        "",
        dictionary[language]["meta.title"],
        dictionary[language]["meta.description"],
        "profile",
    )
    profile_entities(
        soup, language, route(language), dictionary[language]["meta.description"]
    )
    append_tag(soup, "link", {"rel": "stylesheet", "href": "/assets/portfolio.css"})
    append_tag(soup, "link", {"rel": "stylesheet", "href": "/assets/home-seo.css"})
    home_runtime(soup)
    language_controls(soup, language)
    home_details(soup, language)
    home_additions(soup, language, items)
    rewrite_urls(soup)
    return soup


def sitemap(output, paths):
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    tree = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
    for path, modified in paths:
        entry = ET.SubElement(tree, "url")
        ET.SubElement(entry, "loc").text = absolute(path)
        ET.SubElement(entry, "lastmod").text = modified
    content = ET.tostring(tree, encoding="unicode", xml_declaration=False)
    write(
        output,
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n' + content + "\n",
    )


def write_page(output, path, soup):
    write(
        output, path.lstrip("/") + "index.html", soup.decode(formatter="minimal") + "\n"
    )


def build_language(source, dictionary, language, items, output, inline_rules):
    write_page(
        output, route(language), home(source, dictionary, language, items, inline_rules)
    )
    write_page(output, route(language, "work/"), hub(items, language))
    pages = [(route(language), MODIFIED), (route(language, "work/"), MODIFIED)]
    for item in items:
        path = route(language, "work/" + item["slug"] + "/")
        write_page(output, path, article(item, language))
        pages.append((path, item["dateModified"]))
    return pages


def build(source, output):
    source = Path(source).resolve()
    raw = (source / "index.html").read_text(encoding="utf-8")
    dictionary, items = translations(raw), load_cases(source)
    output = prepare_output(source, Path(output))
    copy_assets(source, output)
    inline_rules, pages = {}, []
    for language in LANGUAGES:
        pages.extend(
            build_language(raw, dictionary, language, items, output, inline_rules)
        )
    original = BeautifulSoup(raw, "html.parser")
    css = "\n".join(style.get_text() for style in original.select("style"))
    css += "\n" + "\n".join(
        "." + name + " {" + rule + "}" for rule, name in inline_rules.items()
    )
    css = css.replace('[aria-pressed="true"]', '[aria-current="page"]')
    write(output, "assets/portfolio.css", css_urls(css) + "\n")
    finish_artifact(output, pages)
    return output


def finish_artifact(output, pages):
    manifest = {
        "pages": [{"path": path, "lastmod": modified} for path, modified in pages]
    }
    write(output, MANIFEST, json.dumps(manifest, indent=2) + "\n")
    write(output, "404.html", not_found().decode(formatter="minimal") + "\n")
    sitemap(output, pages)
    write(
        output,
        "robots.txt",
        "User-agent: *\nAllow: /\n\nSitemap: https://pantani.xyz/sitemap.xml\n"
        "Sitemap: https://pantani.xyz/triton-l200-hpe/sitemap.xml\n",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    arguments = parser.parse_args()
    try:
        output = build(arguments.source, arguments.output)
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Site build failed: {error}\n")
    print(f"Built public static artifact: {output}")


if __name__ == "__main__":
    main()
