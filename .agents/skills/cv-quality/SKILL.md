---
name: cv-quality
description: Use when auditing or improving this repository's multilingual CV PDFs, their print generation, factual consistency, or repeatable analysis and implementation builds.
---

# CV Quality

## When to use

Use for repository CV analysis, authorized CV edits, or PDF-generation regressions. A general explanation of ATS needs a direct answer, not this workflow. LinkedIn profile edits belong to the LinkedIn skill.

## Required inputs

Read `index.html`, `README.md`, `scripts/generate-pdfs.sh`, and all three files in `output/pdf/`. Read `docs/harness/cv-quality/team-spec.md` for phase paths and ownership. Establish whether the request authorizes analysis only or implementation too. A target vacancy is optional: without it, report general Go/backend positioning and no match score.

## Analysis build

1. Inspect existing changes and preserve unrelated work. Capture originals before implementation.
2. Run `make cv-analyze`. Set `PYTHON` when dependencies are in a dedicated environment. Preserve analysis evidence before rebuilding; use a new run directory for a separate future audit.
3. Inspect every rendered page with Poppler and an image viewer. Compare pypdf's default extraction with pdfplumber's positional extraction. A successful extraction alone does not prove correct section association.
4. Audit facts, career chronology, language parity, current work, technical evidence and readability. Record source-backed facts, editorial inference and unverified claims separately in `audit.md`.
5. Map every accepted finding to a concrete change and acceptance check in `plan.md`. Missing facts produce a needs-evidence entry, not invented metrics or employment claims.

## Implementation build

1. Consume the audit and plan. If absent or incomplete, finish analysis first. User authorization to audit alone does not authorize implementation.
2. Edit the canonical HTML and all affected dictionaries/default English DOM together. Keep README factual wording aligned. Preserve dates, citizenship, remote preference, language levels and incomplete-degree disclosures. Personal Rust study stays explicitly personal.
3. Improve reading order at the source; avoid reordering extracted text to conceal a malformed PDF. Prefer already demonstrated skills over invented employment associations. A compact earlier-job record still names its actual employer, role and full dates.
4. Run `make cv-implement`, which requires analysis, generates staged PDFs and runs strict local checks. A failed build is incomplete and must not be described as ATS-ready.
5. Render and inspect every final page. Review source changes and claims; record finding-by-finding outcomes in `review.md`. Resolve reproducible local defects before completion.

## Outputs and validation

Analysis: `_workspace/cv-quality/analysis/` contains machine evidence; the run root contains inventory, audit and plan. Implementation evidence lives in `implementation/`; final files remain `output/pdf/`.

Normal acceptance: three languages, correct extraction sequence in both readers, no presentation ligatures, readable fonts, complete roles and factual boundaries, reviewed rendering. Tests cover missing inputs and a failed generation. Build success is local PDF validation, never a proprietary ATS score or interview guarantee.

## Common mistakes

- Counting a positional extraction pass as proof that raw extraction also passed.
- Adding plausible client achievements, metrics or employer-specific tools without evidence.
- Removing the Rust qualification while leaving Rust among professional claims.
- Treating a successful command as visual review or a partial language set as complete.
- Publishing private audit evidence with the public CV.

Example: “Audit the three CV PDFs for remote Go/backend roles, then apply the accepted fixes locally.” Run analysis, preserve its baseline, implement the plan, then return final PDFs and explicit unverified items. No upload, commit or publication is implied.
