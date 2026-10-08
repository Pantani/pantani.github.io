"""Validate claim provenance and build local career drafts without publishing."""

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import sys

LANGUAGES = ("en", "pt-br")


def evidence_index(records, errors):
    index = {}
    for record in records:
        url = record["url"]
        if url in index:
            errors.append(f"duplicate evidence: {url}")
        index[url] = record
        if len(record.get("allFiles", [])) != record["files"]["totalCount"]:
            errors.append(f"incomplete file inventory: {url}")
    return index


def source_errors(url, index, organizations):
    record = index.get(url)
    if record is None:
        return [f"unknown source: {url}"]
    errors = []
    if record["state"] != "MERGED":
        errors.append(f"source not merged: {url}")
    if record["repository"].get("isPrivate", True):
        errors.append(f"private source cannot support public draft: {url}")
    owner = record["repository"]["nameWithOwner"].split("/")[0]
    if owner not in organizations:
        errors.append(f"employer attribution missing for {owner}: {url}")
    return errors


def claim_errors(claim, index, organizations):
    errors = []
    if not claim.get("text", "").strip():
        errors.append("claim text is empty")
    if not claim.get("sources"):
        errors.append("claim has no sources")
    for url in claim.get("sources", []):
        errors.extend(source_errors(url, index, organizations))
    return errors


def sections(role):
    yield "linkedin", role.get("linkedin", [])
    for language, claims in role.get("cv", {}).items():
        yield f"cv-{language}", claims


def role_errors(role, employers, index):
    employer = employers.get(role["employer"], {})
    errors = []
    if not employer.get("source"):
        errors.append(f"unconfirmed employer: {role['employer']}")
    if set(role.get("cv", {})) != set(LANGUAGES):
        errors.append(f"CV languages must be {LANGUAGES}: {role['id']}")
    for section, claims in sections(role):
        if not claims:
            errors.append(f"empty section: {role['id']}/{section}")
        for claim in claims:
            errors.extend(claim_errors(claim, index, employer.get("organizations", [])))
    return errors


def validate(records, draft):
    errors = []
    index = evidence_index(records, errors)
    if not draft.get("roles"):
        errors.append("draft has no roles")
    for role in draft.get("roles", []):
        errors.extend(role_errors(role, draft.get("confirmed_employers", {}), index))
    return errors


def render_draft(roles, section):
    lines = ["# Career description draft", "", "Status: local draft; not published.", ""]
    for role in roles:
        claims = dict(sections(role))[section]
        lines.extend([f"## {role['employer']} — {role['dates']}", ""])
        lines.extend(f"- {claim['text']}" for claim in claims)
        lines.append("")
    return "\n".join(lines)


def render_ledger(roles):
    lines = ["# Claim evidence ledger", "", "Merged status verifies acceptance, not production deployment or business impact.",
             "Text-to-code correspondence requires human review; this build validates provenance only.", ""]
    for role in roles:
        for section, claims in sections(role):
            lines.extend([f"## {role['id']} / {section}", ""])
            for claim in claims:
                lines.extend([claim["text"], "", *[f"- {url}" for url in claim["sources"]], ""])
    return "\n".join(lines)


def emit_drafts(output, roles):
    (output / "linkedin.md").write_text(render_draft(roles, "linkedin"))
    for language in LANGUAGES:
        (output / f"cv-{language}.md").write_text(render_draft(roles, f"cv-{language}"))
    (output / "claim-ledger.md").write_text(render_ledger(roles))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_role_dom(source, role):
    key = f"exp.{role['id']}"
    pattern = rf'<ul>\s*<li data-i18n-html="{re.escape(key)}\.b1">.*?</ul>'
    bullets = [f'                  <li data-i18n-html="{key}.b{i}">{html.escape(c["text"])}</li>'
               for i, c in enumerate(role["cv"]["en"], 1)]
    replacement = "<ul>\n" + "\n".join(bullets) + "\n                </ul>"
    result, count = re.subn(pattern, lambda _: replacement, source, flags=re.S)
    if count != 1:
        raise ValueError(f"Template drift: expected one DOM list for {key}, found {count}")
    return result


def replace_role_translations(source, role):
    key = f"exp.{role['id']}"
    pattern = rf'(?:^        "{re.escape(key)}\.b\d+": [^\n]+\n)+'
    matches = list(re.finditer(pattern, source, re.M))
    if len(matches) != len(LANGUAGES):
        raise ValueError(f"Template drift: expected {len(LANGUAGES)} translation blocks for {key}")
    for match, language in reversed(list(zip(matches, LANGUAGES))):
        entries = [f'        "{key}.b{i}": {json.dumps(html.escape(c["text"]), ensure_ascii=False)},\n'
                   for i, c in enumerate(role["cv"][language], 1)]
        source = source[:match.start()] + "".join(entries) + source[match.end():]
    return source


def preview_html(source, roles):
    for role in roles:
        source = replace_role_dom(source, role)
        source = replace_role_translations(source, role)
    return source


def emit_preview(source, roles, output):
    candidate = output / "candidate"
    rendered = preview_html(source.read_text(), roles)
    scripts = candidate / "scripts"
    scripts.mkdir(parents=True)
    (candidate / "index.html").write_text(rendered)
    for name in ("cv_quality.py", "generate-pdfs.sh"):
        shutil.copy2(Path(__file__).parent / name, scripts / name)


def prepare_preview(args, draft, errors):
    if not args.source:
        return
    try:
        emit_preview(args.source, draft["roles"], args.output)
    except (OSError, ValueError) as error:
        errors.append(str(error))


def build(args):
    args.output.mkdir(parents=True, exist_ok=False)
    records = json.loads(args.evidence.read_text())
    draft = json.loads(args.draft.read_text())
    errors = validate(records, draft)
    if not errors:
        prepare_preview(args, draft, errors)
    report = {"status": "fail" if errors else "pass", "errors": errors,
              "evidence_records": len(records), "evidence_sha256": digest(args.evidence),
              "draft_sha256": digest(args.draft), "semantic_review": "required",
              "producer": "career-audit", "consumer": "career-reviewer"}
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    if errors:
        return 1
    emit_drafts(args.output, draft["roles"])
    print(f"Validated provenance; drafts written to {args.output}. Semantic review still required.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", type=Path, help="Prepare an isolated CV HTML preview from this template")
    args = parser.parse_args()
    try:
        return build(args)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Career audit failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
