#!/usr/bin/env python3

from __future__ import annotations

import re
import subprocess
import sys
from html import unescape
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "output" / "pdf"
TEXT_DIR = ROOT / "output" / "text"

VARIANTS = (
    (
        "danilo-pantani-senior-go-engineer",
        "Senior Go Engineer | Backend & Distributed Systems",
    ),
    (
        "danilo-pantani-blockchain-infrastructure-engineer",
        "Senior Blockchain Infrastructure Engineer | Go, Cosmos SDK & IBC",
    ),
    (
        "danilo-pantani-platform-engineer",
        "Senior Platform Engineer | Go, Kubernetes & Distributed Systems",
    ),
)

SECTIONS = (
    "Professional Summary",
    "Core Skills",
    "Professional Experience",
    "Selected Open Source",
    "Education",
    "Languages",
    "Additional Information",
)

EMPLOYERS = (
    "Ignite (All in Bits)",
    "Interchain Foundation",
    "Ignite (formerly Tendermint)",
    "Hermez Network",
    "Energi Core",
    "Trust Wallet",
    "Mercado Bitcoin",
    "Earlier Software Engineering",
)

REQUIRED_URLS = (
    "mailto:danpantani@gmail.com",
    "linkedin.com/in/dpantani",
    "github.com/Pantani",
    "pantani.github.io",
)

FORBIDDEN_PATTERNS = (
    ("verification placeholder", re.compile(r"\[VERIFY", re.IGNORECASE)),
    (
        "ADR-004 authorship claim",
        re.compile(r"\bauthor(?:ed|ship)?\b.{0,80}\bADR[-\s]?004\b", re.IGNORECASE | re.DOTALL),
    ),
    (
        "unsupported 10+ years of production Go/blockchain claim",
        re.compile(
            r"10\+\s+years\s+shipping\s+production\s+(?:Go|blockchain)",
            re.IGNORECASE,
        ),
    ),
    ("unsupported combined Staff/Senior title", re.compile(r"\bStaff\s*/\s*Senior\b", re.IGNORECASE)),
    ("Telegram contact", re.compile(r"\bTelegram\b", re.IGNORECASE)),
    ("unexpanded IBC-Go name", re.compile(r"\bIBCGo\b", re.IGNORECASE)),
    ("compressed market-data wording", re.compile(r"\bmarketdata\b", re.IGNORECASE)),
    ("compressed end-to-end wording", re.compile(r"\bendtoend\b", re.IGNORECASE)),
    ("replacement character", re.compile("�")),
)


def run(*args: str) -> str:
    completed = subprocess.run(
        args,
        check=True,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_forbidden_text(text: str, document: str) -> None:
    for label, pattern in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            fail(f"{document}: forbidden content ({label})")


def validate_target_title(source: str, expected_title: str, document: str) -> None:
    matches = re.findall(
        r'<p\s+class="target-title"\s*>(.*?)</p>',
        source,
        re.DOTALL,
    )
    if len(matches) != 1:
        fail(f"{document}: expected one target-title line")
    target_title = " ".join(
        unescape(re.sub(r"<[^>]+>", " ", matches[0])).split()
    )
    if target_title != expected_title:
        fail(
            f"{document}: target title is {target_title!r}, expected {expected_title!r}"
        )


def section_line_indexes(lines: list[str], document: str) -> list[int]:
    indexes = []
    for section in SECTIONS:
        matches = [
            index
            for index, line in enumerate(lines)
            if line == section or (section == "Selected Open Source" and line.startswith(section))
        ]
        if len(matches) != 1:
            fail(f"{document}: expected one heading for {section!r}, found {len(matches)}")
        indexes.append(matches[0])
    return indexes


def employer_line_indexes(lines: list[str], start: int, end: int, document: str) -> list[int]:
    indexes = []
    for employer in EMPLOYERS:
        matches = [
            index
            for index, line in enumerate(lines[start:end], start=start)
            if line.startswith(employer)
        ]
        if len(matches) != 1:
            fail(f"{document}: expected one experience heading for {employer!r}, found {len(matches)}")
        indexes.append(matches[0])
    return indexes


def validate_html() -> None:
    css = (ROOT / "ats" / "resume.css").read_text(encoding="utf-8")
    if "@page" not in css or "size: A4" not in css:
        fail("ATS print stylesheet must define A4 output")
    if "column-count" in css or "position: absolute" in css:
        fail("ATS print stylesheet contains multi-column or absolute positioning")

    for slug, expected_title in VARIANTS:
        source_name = slug.removeprefix("danilo-pantani-") + ".html"
        source = (ROOT / "ats" / source_name).read_text(encoding="utf-8")
        for forbidden_markup in ("<table", "<img", "<aside"):
            if forbidden_markup in source:
                fail(f"{source_name}: forbidden ATS markup {forbidden_markup}")
        if source.count("<h1>Danilo Pantani</h1>") != 1:
            fail(f"{source_name}: expected one candidate-name heading")
        source_text = unescape(re.sub(r"<[^>]+>", " ", source))
        validate_target_title(source, expected_title, source_name)
        validate_forbidden_text(source_text, source_name)

        markdown_name = f"{slug}.md"
        markdown = (ROOT / "resume-source" / markdown_name).read_text(encoding="utf-8")
        expected_prefix = f"# Danilo Pantani\n\n## {expected_title}\n"
        if not markdown.startswith(expected_prefix):
            fail(f"{markdown_name}: candidate name and title are not the first headings")
        validate_forbidden_text(markdown, markdown_name)


def validate_pdf(slug: str, expected_title: str) -> None:
    pdf_path = PDF_DIR / f"{slug}.pdf"
    text_path = TEXT_DIR / f"{slug}.txt"
    if not pdf_path.is_file():
        fail(f"missing {pdf_path}")

    info = run("pdfinfo", str(pdf_path))
    page_match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    if not page_match:
        fail(f"{pdf_path.name}: page count not found")
    pages = int(page_match.group(1))
    if pages > 2:
        fail(f"{pdf_path.name}: {pages} pages")
    if "A4" not in info:
        fail(f"{pdf_path.name}: page size is not A4")

    run("pdftotext", str(pdf_path), str(text_path))
    text = text_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        fail(f"{pdf_path.name}: insufficient extracted text")
    if lines[0] != "Danilo Pantani":
        fail(f"{pdf_path.name}: first extracted line is {lines[0]!r}")
    if lines[1] != expected_title:
        fail(f"{pdf_path.name}: second extracted line is {lines[1]!r}")

    section_indexes = section_line_indexes(lines, pdf_path.name)
    if section_indexes != sorted(section_indexes):
        fail(f"{pdf_path.name}: incorrect section reading order")
    employer_indexes = employer_line_indexes(
        lines,
        section_indexes[2],
        section_indexes[3],
        pdf_path.name,
    )
    if employer_indexes != sorted(employer_indexes):
        fail(f"{pdf_path.name}: experience is not reverse chronological")
    validate_forbidden_text(text, pdf_path.name)

    urls = run("pdfinfo", "-url", str(pdf_path))
    for required_url in REQUIRED_URLS:
        if required_url not in urls:
            fail(f"{pdf_path.name}: missing clickable link {required_url}")

    print(f"PASS: {pdf_path.name} | pages={pages} | text_order=linear | links=present")


def main() -> None:
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    validate_html()
    for slug, expected_title in VARIANTS:
        validate_pdf(slug, expected_title)
    print("ATS_VALIDATION=PASS")


if __name__ == "__main__":
    main()
