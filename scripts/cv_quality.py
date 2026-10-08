#!/usr/bin/env python3
"""Audit local CV PDFs; this is a readability contract, not an ATS score."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import pdfplumber
from pypdf import PdfReader

LANGUAGES = ("en", "pt-br")
SECTION_ANCHORS = {
    "en": ("Professional Summary", "Technical Skills & Core Expertise",
           "Professional Experience", "Trust Wallet / Binance", "Mercado Bitcoin",
           "Earlier Roles", "Selected Repositories / Evidence", "Teaching & Talks",
           "Languages", "Education & Certifications"),
    "pt-br": ("Resumo Profissional", "Competências Técnicas e Áreas de Especialização",
              "Experiência Profissional", "Trust Wallet / Binance", "Mercado Bitcoin",
              "Atuações Anteriores", "Repositórios Selecionados / Evidências",
              "Docência e Palestras", "Idiomas", "Formação e Certificações"),
}
CONTACT = "danpantani@gmail.com"
LIGATURES = re.compile("[\ufb00-\ufb06]")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_reference(path):
    return {"path": str(path), "sha256": sha256(path)}


def normalized(text):
    """Normalize layout whitespace, preserving meaningful Unicode characters."""
    return " ".join(text.casefold().split())


def finding(code, detail, extractor=None):
    return {"code": code, "detail": detail, "extractor": extractor}


def anchor_findings(text, language, extractor):
    content = normalized(text)
    previous = -1
    findings = []
    for anchor in (CONTACT, *SECTION_ANCHORS[language]):
        position = content.find(normalized(anchor), max(previous, 0))
        if position < 0:
            findings.append(finding("missing_anchor", f"Missing or out of order: {anchor}", extractor))
            continue
        previous = position + len(normalized(anchor))
    return findings


def text_findings(text, language, extractor):
    findings = anchor_findings(text, language, extractor)
    if not text.strip():
        findings.append(finding("empty_text", "No extractable text", extractor))
    ligatures = sorted(set(LIGATURES.findall(text)))
    if ligatures:
        findings.append(finding("unicode_ligatures", f"Ligatures: {ligatures}", extractor))
    return findings


def extract_pdf(path):
    reader = PdfReader(path)
    if reader.is_encrypted:
        raise ValueError("Encrypted PDFs are not accepted")
    plain = "\n\f\n".join(page.extract_text() for page in reader.pages)
    layout, minimum_size = extract_layout(path)
    return len(reader.pages), minimum_size, {"pypdf": plain, "pdfplumber": layout}


def page_font_sizes(page):
    return [float(char["size"]) for char in page.chars if char["text"].strip()]


def extract_layout(path):
    with pdfplumber.open(path, unicode_norm=None) as pdf:
        layout = "\n\f\n".join(page.extract_text() or "" for page in pdf.pages)
        sizes = [size for page in pdf.pages for size in page_font_sizes(page)]
    return layout, min(sizes, default=0.0)


def document_metrics(pages, minimum_size):
    findings = []
    if pages != 2:
        findings.append(finding("page_count", f"Expected 2 pages; found {pages}"))
    if minimum_size < 8.95:
        findings.append(finding("minimum_font", f"Expected >=9pt (0.05pt tolerance); found {minimum_size:.3f}pt"))
    return findings


def save_extractions(texts, language, output):
    evidence = {}
    for extractor, text in texts.items():
        path = output / f"{language}.{extractor}.txt"
        path.write_text(text, encoding="utf-8")
        evidence[extractor] = {"file": path.name, "sha256": sha256(path)}
    return evidence


def inspect_document(path, language, output):
    document = {"language": language, "path": str(path), "findings": []}
    try:
        document["sha256"] = sha256(path)
        pages, size, texts = extract_pdf(path)
        document.update(pages=pages, minimum_font_pt=round(size, 4), encrypted=False)
        document["evidence"] = save_extractions(texts, language, output)
        document["findings"] = document_metrics(pages, size)
        for extractor, text in texts.items():
            document["findings"].extend(text_findings(text, language, extractor))
    except Exception as error:
        document["findings"].append(finding("input_error", f"{type(error).__name__}: {error}"))
    return document


def report_status(documents):
    codes = {item["code"] for doc in documents for item in doc["findings"]}
    if "input_error" in codes:
        return "incomplete"
    return "needs_changes" if codes else "pass"


def collect_report(args):
    source = file_reference(args.source)
    if not args.strict:
        snapshot = args.output / "source.html"
        snapshot.write_bytes(args.source.read_bytes())
        source["evidence"] = snapshot.name
    documents = [inspect_document(args.pdf_dir / f"danilo-pantani-cv-{lang}.pdf", lang, args.output)
                 for lang in LANGUAGES]
    report = {
        "schema_version": 1,
        "phase": "implementation" if args.strict else "analysis",
        "status": report_status(documents),
        "source": source,
        "tools": {"pypdf": __import__("pypdf").__version__, "pdfplumber": pdfplumber.__version__},
        "contract": {"pages": 2, "minimum_font_pt": 9, "font_tolerance_pt": 0.05,
                     "extractors": ["pypdf plain", "pdfplumber default"],
                     "scope": "Local PDF readability only; no ATS vendor score or job matching"},
        "documents": documents,
    }
    if args.analysis_report:
        report["analysis"] = file_reference(args.analysis_report)
    return report


def verify_analysis_documents(report, path, pdf_dir, retries):
    documents = report["documents"]
    if {doc["language"] for doc in documents} != set(LANGUAGES):
        raise ValueError("Analysis must cover all supported languages")
    for doc in documents:
        current = pdf_dir / f"danilo-pantani-cv-{doc['language']}.pdf"
        accepted = {doc["sha256"], retries.get(doc["language"])}
        if sha256(current) not in accepted:
            raise ValueError(f"PDF changed outside this analysis/build: {current.name}; use a new CV_RUN_DIR")
        verify_evidence(doc, path.parent)


def verify_evidence(document, directory):
    if set(document["evidence"]) != {"pypdf", "pdfplumber"}:
        raise ValueError("Both extraction evidence files are required")
    for evidence in document["evidence"].values():
        if sha256(directory / evidence["file"]) != evidence["sha256"]:
            raise ValueError("Analysis extraction evidence changed; run cv-analyze again")


def retry_hashes(previous, baseline):
    if not previous.is_file():
        return {}
    report = json.loads(previous.read_text(encoding="utf-8"))
    identity = (report.get("phase"), report.get("analysis", {}).get("sha256"))
    if identity != ("implementation", sha256(baseline)):
        return {}
    if "documents" in report:
        return {doc["language"]: doc.get("sha256") for doc in report["documents"]}
    return report.get("input_pdf_hashes", {})


def require_analysis(path, pdf_dir, previous):
    report = json.loads(path.read_text(encoding="utf-8"))
    expected = (report["schema_version"], report["phase"], report["status"])
    if expected not in ((1, "analysis", "pass"), (1, "analysis", "needs_changes")):
        raise ValueError("A complete analysis report is required before implementation")
    source = report["source"]
    if sha256(path.parent / source["evidence"]) != source["sha256"]:
        raise ValueError("Analysis source snapshot changed")
    verify_analysis_documents(report, path, pdf_dir, retry_hashes(previous, path))


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("index.html"))
    parser.add_argument("--pdf-dir", type=Path, default=Path("output/pdf"))
    parser.add_argument("--output", type=Path, default=Path("_workspace/cv-quality/analysis"))
    parser.add_argument("--strict", action="store_true", help="Fail on quality findings")
    parser.add_argument("--require-analysis", type=Path, help="Only verify the analysis gate; do not generate PDFs")
    parser.add_argument("--prepare-implementation", action="store_true", help="Record a pending build after the analysis gate")
    parser.add_argument("--analysis-report", type=Path, help="Record the baseline report hash in the final audit")
    args = parser.parse_args()
    if args.prepare_implementation and args.require_analysis is None:
        parser.error("--prepare-implementation requires --require-analysis")
    return args


def write_report(report, output):
    output.mkdir(parents=True, exist_ok=True)
    destination = output / "report.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CV validation: {report['status']} ({destination})")


def prepare_implementation(args):
    input_hashes = {lang: sha256(args.pdf_dir / f"danilo-pantani-cv-{lang}.pdf") for lang in LANGUAGES}
    report = {"schema_version": 1, "phase": "implementation", "status": "incomplete",
              "stage": "generation_pending", "source": file_reference(args.source),
              "analysis": file_reference(args.require_analysis), "input_pdf_hashes": input_hashes}
    write_report(report, args.output)


def run_audit(args):
    if not args.strict and (args.output / "report.json").exists():
        print("Analysis already exists; select a new CV_RUN_DIR or --output to preserve history", file=sys.stderr)
        return 2
    args.output.mkdir(parents=True, exist_ok=True)
    try:
        report = collect_report(args)
    except OSError as error:
        report = {"schema_version": 1, "status": "incomplete", "error": str(error)}
    write_report(report, args.output)
    if report["status"] == "incomplete":
        return 2
    return int(args.strict and report["status"] != "pass")


def main():
    args = arguments()
    if args.require_analysis is None:
        return run_audit(args)
    try:
        require_analysis(args.require_analysis, args.pdf_dir, args.output / "report.json")
        if args.prepare_implementation:
            prepare_implementation(args)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Analysis gate failed: {error}", file=sys.stderr)
        return 2
    print(f"Analysis gate passed: {args.require_analysis}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
