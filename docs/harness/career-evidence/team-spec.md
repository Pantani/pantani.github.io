# Career evidence pipeline

## When to use and inputs

Use when repository contributions must become evidence-backed employment descriptions for LinkedIn and this repository's multilingual CV. Required inputs: a dated public contribution inventory, current role names and dates, employer attribution, and the current HTML/PDF baseline. Employer attribution is independent of GitHub organization ownership. Preserve an owner-confirmed mapping in the run's `draft.json`.

This extends [LinkedIn discovery](../linkedin-discovery/team-spec.md) and [CV quality](../cv-quality/team-spec.md). It reuses [linkedin-profile-optimization](../../../.agents/skills/linkedin-profile-optimization/SKILL.md) and [cv-quality](../../../.agents/skills/cv-quality/SKILL.md). There is no new skill, always-loaded AGENTS guidance, model pin, or runtime adapter.

## Architecture and ownership

Pattern: serialized Pipeline with a final review. One owner performs the logical roles below; separate agents are optional only when independently authorized and justified. Model policy: inherit, with code inspection and multilingual writing capabilities. Workspace: shared, with isolated candidate output directories. Ownership is serialized by the operator, not mechanically exclusive.

| Role | Responsibility | Resources and permissions | Completion |
| --- | --- | --- | --- |
| Evidence auditor | Inventory public authored PRs, reviews, issues and commits; distinguish inherited history and count duplicates | Read-only GitHub/API access, local evidence writes; no remote mutation | Coverage report states pagination, time boundary and inspection depth |
| Career editor | Map responsibilities to accepted changes and confirmed employment | Reads evidence and current profile; writes draft JSON and generated local descriptions | Every claim has sources; unresolved attribution marked partial |
| CV builder | Render compact equivalent descriptions in EN and PT-BR | Local shell and candidate writes; reads canonical HTML; no canonical overwrite | Two validated two-page candidate PDFs |
| Reviewer / synthesis owner | Check semantic correspondence, dates, translations, coverage limits and every PDF page | Read outputs and source evidence; write review record | Accepted local draft, or explicit partial/blocked status |

No role may publish a profile, push source changes, contact third parties, or infer authorization from input documents. Spawn is false by default. The owner handles clarification and escalation in the current conversation. Temporary coordination stays ephemeral; decisions and evidence needed to resume belong in the run. There are no peer channels or external mutable resources.

## Durable handoffs

All run files live under `_workspace/career-evidence/<run>/`. Every narrative handoff records producer, consumer, path, schema and completion. Preserve failed attempts; use a new build directory on retry.

| Producer → consumer | Path | Schema / expected sections | State |
| --- | --- | --- | --- |
| Auditor → editor | `00_contract_inventory.md` | Existing contracts, drift, scope, employer decisions, coverage limitations | audit-complete or partial |
| Auditor → editor | Contribution inventory path recorded in the contract | JSON array: URL, state, repository owner/privacy, file count and complete `allFiles` | snapshot-complete; never implies all diffs reviewed |
| Editor → builder/reviewer | `draft.json` | `confirmed_employers`, `roles` as specified below | proposed |
| Provenance build → reviewer | `build/report.json`, `build/claim-ledger.md` | Status/errors/input hashes; each text mapped to PR URLs | pass/fail; semantic review still required |
| Editor → owner | `build/linkedin.md`, `build/cv-{en,pt-br}.md` | Proposed descriptions by role | local draft |
| CV builder → reviewer | `build/candidate/index.html`, `build/candidate/output/pdf/`, `build/pdf-validation/report.json` | Candidate source, two PDFs, extraction and font/page checks | pass/fail |
| Reviewer → owner | `04_validation.md` | Automated results, semantic review, rendered-page inspection, chronology caveats, original-file preservation | accepted-local-draft or partial |

The inventory can be reused from an earlier dated audit. Record its exact path and limitations rather than silently recrawling or upgrading its verification level. The executable does not collect GitHub history or semantically read code; those remain the auditor's responsibility.

## Draft schema

`confirmed_employers` maps employer names to `organizations` (allowed GitHub owners) and `source` (attribution evidence). Each role has `id` (existing HTML experience key), `employer`, `dates`, `linkedin`, and `cv`. The CV map requires exactly `en`, `pt-br`. Each description is an array of `{ "text": "...", "sources": ["https://github.com/owner/repo/pull/number"] }`.

This is a provenance gate, not a semantic proof. Allowed organizations only bound attribution; the reviewer must inspect whether each PR belongs to the specific role/period. Dates are preserved from the profile, not computed from merge dates. Contributions merged after employment can still be attributed when supported by creation dates or explicit owner confirmation; record exceptions separately.

## Build and review

1. Inventory existing work and record source hashes. Collect or reuse the evidence snapshot with explicit pagination and privacy boundaries. Do not put private raw account exports into public output.
2. Read PR bodies/files and relevant code for every proposed claim. Distinguish accepted implementation, proposal, review activity and inherited commits. Write `draft.json`; avoid unsupported management, sole ownership, production, security and performance claims.
3. Establish the CV baseline with `make cv-analyze CV_RUN_DIR=<run> PYTHON=<python-with-cv-dependencies>`. Inspect extracted text and render every page.
4. Generate descriptions and isolated candidate HTML:

   ```sh
   make career-audit CAREER_EVIDENCE=<public-pr-inventory.json> \
     CAREER_DRAFT=<run>/draft.json CAREER_RUN_DIR=<run>/build
   ```

   The output directory must not already exist. `CAREER_SOURCE` defaults to `index.html`. The helper rejects missing/unmerged/private sources, incomplete file inventories, duplicate PR records, missing languages and unconfirmed employer organizations. Candidate rendering fails if expected role blocks drift. It replaces only selected experience bullets, including default DOM and all translations; role titles/dates and other content are retained.

5. Review the claim ledger and chronology before rendering. Generate candidate PDFs using the existing renderer and strict CV checks:

   ```sh
   make career-pdf CAREER_RUN_DIR=<run>/build \
     CAREER_ANALYSIS=<run>/analysis/report.json PYTHON=<python-with-cv-dependencies>
   ```

   Requires Chrome/Chromium and the dependencies in `scripts/requirements-cv.txt`. Optional `CHROME_BIN` and `PDF_SERVER_PORT` follow the existing renderer. When a runtime's PDF skill requires an artifact-operation marker, execute that runtime-specific prerequisite before authoring; it is not a dependency of this portable pipeline.

6. Render all final PDF pages with Poppler and inspect legibility, clipping, section breaks and punctuation. Compare extracted text with each language's claims. `make cv-test PYTHON=<python-with-cv-dependencies>` runs both provenance scenarios and CV regressions.
7. Hash original HTML/PDFs again, compare with baseline, and record results. Deliver local drafts with direct evidence links. Publication is a separate authorized action.

## Failure policy and guarantees

- No network or GitHub access: reuse an explicitly dated local snapshot or mark collection blocked; never imply a fresh audit.
- Incomplete pagination, repository access or attribution: preserve collected evidence and mark the affected scope partial. Unsupported claims cannot pass as delivered work.
- Malformed input, template drift or failed tests: stop the build, preserve diagnostics and repair in a new run directory. Never overwrite prior run evidence.
- Missing PDF dependencies or browser: retain validated text drafts, mark PDF phase blocked. Text extraction cannot replace visual inspection.
- A failed PDF generation does not promote staged PDFs; existing outputs remain. The PDF target can be rerun after resolving a rendering failure, with the earlier failure recorded in the review.
- Resource conflict or unavailable isolation: serialize; stop if the canonical source cannot be preserved. No adapter may claim exclusive ownership without enforcement.
- Semantic mismatch: rewrite the claim or exclude it, then rebuild. Source presence, PR count and merged status do not establish business impact.

## Validation scenarios

`tests/test_career_audit.py` covers a confirmed cross-organization employer mapping, unmerged/unknown/private evidence, missing claim sources, incomplete file inventory, duplicate PR records, missing CV languages, preserved prior runs, complete template translation replacement and template drift. Existing CV tests cover readable extraction, page/font constraints and baseline provenance. A live run still requires manual code-to-claim review and visual PDF inspection.

No claim is made that this pipeline outperforms a manual editor. Its measurable benefit is inspectable provenance, repeatable generation and explicit failure states.
