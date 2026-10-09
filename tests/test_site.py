"""Publication contracts for the bilingual portfolio artifact."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


SOURCE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Old title</title><style>.hero { background:url('portrait.png'); }</style>
<script type="application/ld+json">{"@type":"Person","performerIn":[]}</script>
</head><body><nav><button class="lang-button" data-lang="en">EN</button>
<button class="lang-button" data-lang="pt">PT-BR</button>
<a id="referencesToggle" href="?references=1">With references</a></nav>
<main id="main"><p class="person-name">Danilo Pantani</p>
<h1 data-i18n-html="hero.title"><em>Backend Engineer</em></h1>
<p data-i18n="hero.pitch">Backend services.</p>
<a href="#experience">Experience</a><h2 id="experience">Experience</h2>
<a data-pdf-download href="output/pdf/danilo-pantani-cv-en.pdf">PDF</a>
<img src="portrait.png" alt="Portrait" data-i18n-attr="alt" data-i18n-attr-key="portrait.alt">
<div class="contact-cta">Obsolete blockchain-only offer</div></main>
<script>const translations = {
en:{"hero.title":"<em>Backend Engineer</em>","hero.pitch":"Backend services.",
"portrait.alt":"Portrait","meta.title":"Danilo Pantani | Go Backend",
"meta.description":"Go backend services and distributed systems."},
pt:{"hero.title":"<em>Engenheiro Backend</em>","hero.pitch":"Serviços backend.",
"portrait.alt":"Retrato","meta.title":"Danilo Pantani | Backend Go",
"meta.description":"Serviços backend Go e sistemas distribuídos."}
}; window.unwantedRuntime = true;</script>
<script defer src="assets/references-data.js"></script>
<script defer src="assets/references.js"></script></body></html>"""


def case_studies():
    def localized(label):
        return {
            "title": label,
            "description": f"Details of {label}.",
            "lead": f"Engineering work: {label}.",
            "sections": [
                {
                    "title": "Implementation",
                    "paragraphs": ["Public implementation evidence."],
                    "bullets": ["A bounded engineering contribution."],
                }
            ],
            "sources": [
                {
                    "label": "Pull request",
                    "url": "https://github.com/Pantani/example/pull/1",
                }
            ],
        }

    return [
        {
            "slug": slug,
            "dateModified": "2026-10-09",
            "en": localized(slug),
            "pt": localized(f"Trabalho {slug}"),
        }
        for slug in ("go-indexing", "developer-tooling", "protocol-work")
    ]


class StaticSiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.root.mkdir()
        self.output = Path(self.temporary.name) / "published"
        (self.root / "index.html").write_text(SOURCE, encoding="utf-8")
        (self.root / "content").mkdir()
        (self.root / "content/case-studies.json").write_text(
            json.dumps(case_studies()), encoding="utf-8"
        )
        self.create_assets()

    def create_assets(self):
        (self.root / "assets").mkdir()
        for name in (
            "site.js",
            "references-data.js",
            "references.js",
            "article.css",
            "home-seo.css",
            "fonts.css",
        ):
            (self.root / "assets" / name).write_text(
                "/* public asset */", encoding="utf-8"
            )
        (self.root / "assets/social-card.jpg").write_bytes(b"public image")
        (self.root / "assets/favicon.jpg").write_bytes(b"public image")
        (self.root / "portrait.png").write_bytes(b"public image")
        (self.root / "output/pdf").mkdir(parents=True)
        for language in ("en", "pt-br"):
            (self.root / f"output/pdf/danilo-pantani-cv-{language}.pdf").write_bytes(
                b"public PDF"
            )
        (self.root / "CNAME").write_text("pantani.xyz\n", encoding="utf-8")
        (self.root / "google123.html").write_text(
            "google-site-verification: google123.html", encoding="utf-8"
        )
        (self.root / "private.md").write_text("Private source", encoding="utf-8")
        (self.root / "linkedin-cover.html").write_text(
            "Source-only cover", encoding="utf-8"
        )

    def build(self):
        from build_site import build

        build(self.root, self.output)

    def findings(self):
        from validate_site import validate_directory

        return validate_directory(self.output)

    def soup(self, route="index.html"):
        return BeautifulSoup(
            (self.output / route).read_text(encoding="utf-8"), "html.parser"
        )

    def test_static_portuguese_has_complete_content_without_translation_runtime(self):
        self.build()
        page = self.soup("pt/index.html")
        self.assertEqual(page.html["lang"], "pt-BR")
        self.assertIn("Danilo Pantani", page.h1.get_text(" ", strip=True))
        self.assertIn("Engenheiro Backend", page.h1.get_text())
        self.assertIn("Serviços backend.", page.get_text())
        self.assertEqual(page.img["alt"], "Retrato")
        self.assertEqual(
            page.select_one("[data-pdf-download]")["href"],
            "/output/pdf/danilo-pantani-cv-pt-br.pdf",
        )
        self.assertFalse(page.select("style, [style], .contact-cta"))
        scripts = page.select("script:not([type='application/ld+json'])")
        self.assertEqual(
            [script.get("src") for script in scripts],
            ["/assets/site.js", "/assets/references-data.js", "/assets/references.js"],
        )
        self.assertTrue(all(script.has_attr("defer") for script in scripts))
        self.assertEqual(page.select_one("a[data-lang='pt']")["aria-current"], "page")
        self.assertEqual(page.select_one("a[data-lang='en']")["href"], "/")
        self.assertIn(
            "/portrait.png", (self.output / "assets/portfolio.css").read_text()
        )

    def test_artifact_has_exact_canonical_routes_and_public_assets(self):
        self.build()
        urls = ET.parse(self.output / "sitemap.xml").getroot()
        locations = [url.find("{*}loc").text for url in urls]
        expected = {
            "https://pantani.xyz/",
            "https://pantani.xyz/pt/",
            "https://pantani.xyz/work/",
            "https://pantani.xyz/pt/work/",
        }
        expected.update(
            f"https://pantani.xyz/{prefix}work/{slug}/"
            for prefix in ("", "pt/")
            for slug in ("go-indexing", "developer-tooling", "protocol-work")
        )
        self.assertEqual(set(locations), expected)
        self.assertEqual(len(locations), 10)
        self.assertEqual(self.findings(), [])
        self.assertFalse((self.output / "private.md").exists())
        self.assertFalse((self.output / "linkedin-cover.html").exists())
        self.assertTrue((self.output / "google123.html").exists())
        self.assertIn(
            "/triton-l200-hpe/sitemap.xml", (self.output / "robots.txt").read_text()
        )
        self.assertEqual(
            self.soup("404.html").select_one("meta[name='robots']")["content"],
            "noindex, follow",
        )

    def test_article_schema_uses_verified_modification_date_and_stable_author(self):
        self.build()
        page = self.soup("work/go-indexing/index.html")
        entities = [
            json.loads(script.string)
            for script in page.select("script[type='application/ld+json']")
        ]
        article = next(entity for entity in entities if entity["@type"] == "Article")
        self.assertEqual(article["dateModified"], "2026-10-09")
        self.assertNotIn("datePublished", article)
        self.assertEqual(article["author"]["@id"], "https://pantani.xyz/#person")
        self.assertTrue(any(entity["@type"] == "BreadcrumbList" for entity in entities))
        self.assertEqual(
            page.select_one("link[hreflang='pt-BR']")["href"],
            "https://pantani.xyz/pt/work/go-indexing/",
        )

    def mutate_home(self, old, replacement):
        path = self.output / "index.html"
        path.write_text(path.read_text().replace(old, replacement), encoding="utf-8")

    def test_validator_rejects_canonical_pointing_to_another_page(self):
        self.build()
        page = self.soup()
        page.select_one("link[rel='canonical']")["href"] = "https://pantani.xyz/pt/"
        (self.output / "index.html").write_text(page.decode(), encoding="utf-8")
        self.assertTrue(any("canonical" in issue for issue in self.findings()))

    def test_validator_rejects_broken_link_and_missing_fragment(self):
        self.build()
        self.mutate_home('href="#experience"', 'href="/missing/#absent"')
        self.assertTrue(any("missing" in issue for issue in self.findings()))

    def test_validator_rejects_missing_anchor_on_existing_page(self):
        self.build()
        self.mutate_home('href="#experience"', 'href="/pt/#absent"')
        self.assertTrue(any("fragment" in issue for issue in self.findings()))

    def test_validator_rejects_malformed_structured_data(self):
        self.build()
        self.mutate_home('"@context": "https://schema.org"', '"@context": invalid')
        self.assertTrue(any("JSON" in issue for issue in self.findings()))

    def test_validator_rejects_source_leakage_and_obsolete_spanish_routes(self):
        self.build()
        (self.output / "private.md").write_text("private source")
        self.mutate_home('hreflang="pt-BR"', 'hreflang="es"')
        findings = self.findings()
        self.assertTrue(any("source" in issue for issue in findings))
        self.assertTrue(any("hreflang" in issue for issue in findings))

    def test_build_refuses_source_or_unowned_output_cleanup(self):
        from build_site import build

        with self.assertRaises(ValueError):
            build(self.root, self.root)
        self.output.mkdir()
        (self.output / "important.txt").write_text("preserve")
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual((self.output / "important.txt").read_text(), "preserve")

    def test_validator_rejects_sitemap_modification_date_drift(self):
        self.build()
        path = self.output / "sitemap.xml"
        path.write_text(path.read_text().replace("2026-10-09", "2025-01-01"))
        self.assertTrue(any("lastmod" in issue for issue in self.findings()))

    def test_validator_rejects_incomplete_person_schema_without_crashing(self):
        self.build()
        self.mutate_home('"mainEntity": {', '"mainEntity": null, "removed": {')
        self.assertTrue(any("Person" in issue for issue in self.findings()))

    def test_validator_rejects_empty_head_title(self):
        self.build()
        page = self.soup()
        page.title.clear()
        (self.output / "index.html").write_text(page.decode(), encoding="utf-8")
        self.assertTrue(any("title" in issue for issue in self.findings()))

    def test_new_case_study_extends_routes_without_validator_count_changes(self):
        items = case_studies()
        fourth = json.loads(json.dumps(items[0]))
        fourth["slug"] = "new-work"
        items.append(fourth)
        (self.root / "content/case-studies.json").write_text(json.dumps(items))
        source_before = (self.root / "index.html").read_bytes()
        self.build()
        self.assertEqual(self.findings(), [])
        self.assertEqual((self.root / "index.html").read_bytes(), source_before)
        self.assertTrue((self.output / "pt/work/new-work/index.html").exists())

    def test_hub_cards_follow_page_heading_without_skipping_a_level(self):
        self.build()
        page = self.soup("work/index.html")
        self.assertEqual(len(page.select(".work-card h2")), 3)
        self.assertFalse(page.select(".work-card h3"))


if __name__ == "__main__":
    unittest.main()
