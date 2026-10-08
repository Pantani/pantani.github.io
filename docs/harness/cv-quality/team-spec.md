# CV quality pipeline

Canonical behavior: `.agents/skills/cv-quality/SKILL.md`. Pattern: Pipeline with optional independent review. The coordinator owns synthesis and acceptance; roles may execute sequentially in one context. No runtime adapter or model pin is required.

## Entry points and handoffs

`make cv-analyze` collects machine evidence without editing source or PDFs. `make cv-implement` requires an analysis report, rebuilds PDFs, and validates final files. `PYTHON` selects an environment containing `scripts/requirements-cv.txt`. Use `CV_RUN_DIR` to select a separate run directory; never overwrite a previous run when starting unrelated work.

Default run: `_workspace/cv-quality/`. Every prose handoff declares producer, consumer, path, schema and completion state. Machine reports record source/PDF hashes, tool versions, findings and coverage; local checks are not employer ATS tests.

| Owner | Output under run | Consumer | Required contents |
| --- | --- | --- | --- |
| Coordinator | `00_contract_inventory.md` | Analyst | Existing materials, scope, capabilities, drift, architecture |
| Analyst | `analysis/report.json`, extraction files | Implementer | Baseline hashes, languages, observed checks, missing inputs |
| Analyst | `audit.md` | Implementer | Priorities, evidence, inference, factual gaps, acceptance |
| Coordinator | `plan.md` | Implementer | Files, ordered changes, checks, authorization |
| Implementer | `implementation/report.json` | Reviewer | Final evidence and failed checks |
| Reviewer | `review.md` | Coordinator/user | Finding closure, visual inspection, tests, limits, complete/partial/blocked |

## Role contract

All roles use `cv-quality`, semantic model policy `inherit`, and `runtime_overrides: {}`. Workspace preference is the existing checkout; preserve unrelated untracked files. Ownership is advisory and non-overlapping; serialize when ownership is uncertain. No external mutable resources, publication, network upload, or recursive spawning. Shell/read access is scoped to this repository and required installed tool documentation.

- **Analyst:** reads source, PDFs and existing career evidence; writes run evidence only. Optional editorial worker owns a separate report. May use local rendering and extraction; cannot alter CV facts or files.
- **Implementer:** reads complete analysis/plan; owns `index.html`, README, build/validation scripts, tests and final PDFs. Only one writer per file. Build-script and source work may be delegated with explicit disjoint paths.
- **Reviewer:** reads baseline, final sources, reports, test output and rendered pages; writes review only. Independent review is useful for factual parity and unnoticed omissions. Cannot repair files concurrently with implementer.
- **Coordinator:** owns assignment, decisions and synthesis; receives native messages with durable reports at boundaries. Missing facts escalate to the user only when needed; finish independent work and preserve unknowns meanwhile.

## Failure policy

Missing source/PDF/tool/permission: preserve available evidence and mark coverage incomplete. Missing baseline prevents implementation build. Generation uses staging so a Chrome failure cannot erase existing PDFs. The implementation build also runs strict validation on staging before promotion; generation or quality failure preserves previous outputs and leaves implementation incomplete. Two final renames are serialized but are not a filesystem transaction: an I/O failure during promotion may leave a partial set and must be reported. Visual review is an explicit additional acceptance step.

Worker/model/spawn/communication failure: disclose the missing review, then use serialized owner review if possible. Never count an absent report or branch as a pass. Resource conflict: stop overlapping writes and serialize. Missing workspace: return unsaved drafts and blocked status. Unavailable runtime capabilities lower the guarantee explicitly; no claims of mechanical ownership. Maximum two reviewer correction rounds; remaining factual uncertainty stays needs-evidence, not fabricated closure.

## Scenarios

1. Normal: baseline records old extraction/font defects; final evidence passes for both supported PDFs and every page is visually inspected.
2. Missing PDF: analysis records missing coverage; strict validation fails. Never substitute a file from another language.
3. Generation failure: command exits nonzero and preserves the previously complete PDF set.
4. Unknown client metric: improve wording using existing facts; record missing metric, no invented percentage.
5. Near miss: “What is ATS?” creates no run and modifies no files.

Harness validity, local CV quality, external ATS behavior and hiring outcomes are distinct acceptance categories.
