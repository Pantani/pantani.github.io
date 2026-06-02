---
name: cv-orchestrator
description: Orchestrates the CV harness for Danilo Pantani's HTML CV (index.html). Use for ANY change to the CV — add or update a project/repo/skill/role, reword copy, fix SEO or i18n, restyle, or do an analytical / end-to-end review. Also triggers on follow-ups: "update the CV", "re-run the review", "add X to my résumé/currículo", "revisar o currículo", "só refazer a parte de Y", "melhorar o resultado", "based on the previous result". Coordinates four specialists (strategist → engineer → layout-guardian + reviewer) so positioning, three-language i18n, SEO, and the 3-page print invariant all stay consistent. Simple factual questions about the CV can be answered directly without the full team.
---

# cv-orchestrator — Run the CV specialist team

Coordinates four agents over one shared file (`index.html`) so no single change breaks positioning, i18n, SEO, or print. The agents are defined in `.claude/agents/`; their domain knowledge is in the sibling skills `cv-positioning`, `cv-i18n-seo-sync`, `cv-print-integrity`.

## Execution mode

**Sub-agent orchestration with file-based handoff.** Spawn each specialist with the `Agent` tool (`subagent_type: "general-purpose"`, **`model: "opus"`**) and a prompt that tells it to first read its definition file in `.claude/agents/` and its skill(s), then do the task. (If a future session exposes the custom types `cv-strategist` etc. as native `subagent_type`s, use those instead — same prompts.) Handoff is via files in `.claude/_workspace/` (git-ignored, never served). Naming: `{phase}_{agent}_{artifact}.md`.

> The team works on one file serially — strategy and implementation must not run in parallel. Verification (layout + review) can run in parallel because both only read.

## Phase 0 — Context check (initial vs follow-up vs partial)

1. Read `git status` and check whether `.claude/_workspace/` already holds artifacts from a prior run.
2. Branch:
   - No `_workspace/` artifacts → **initial run**, start at Phase 1.
   - Artifacts exist + user asks to redo one part ("just the Tech Stack", "re-run the review") → **partial re-run**: re-invoke only the relevant agent(s), reusing prior artifacts as input.
   - Artifacts exist + a genuinely new request → **new run**: move old `_workspace/` to `_workspace_prev/`, start fresh.
3. State which mode you picked in one line before proceeding.

## Phase 1 — Strategy (cv-strategist)

Spawn cv-strategist. It decides exactly where the change belongs (using `cv-positioning`), drafts the English copy, names the precise target sections/keys, and flags anything that risks dilution or the print budget. Output → `.claude/_workspace/01_strategist_positioning.md`. Verify external facts (repo URL, PR counts) are real, not assumed.

## Phase 2 — Implementation (cv-i18n-seo-engineer)

Spawn cv-i18n-seo-engineer with the strategist's artifact. It edits `index.html`: HTML defaults + en/pt/es dicts (respecting the &-rule), repo chips / tags, and only the SEO surfaces that legitimately change. It writes a change log → `.claude/_workspace/02_engineer_changes.md` listing every edited location and the en/pt/es parity check.

## Phase 3 — Verification (parallel: layout-guardian + reviewer)

Spawn both, `run_in_background: true`, both read-only:
- **cv-layout-guardian** (`cv-print-integrity`) renders EN/PT/ES headless and confirms 3 pages each → `03_layout_report.md`.
- **cv-reviewer** does the cross-boundary + analytical audit → `03_review_report.md` (see its definition for the checklist).

## Phase 4 — Remediation

If either report finds a defect: route a focused fix back to cv-i18n-seo-engineer (or cv-strategist if it's a positioning miss), then re-run only the failed verification. One retry per defect; if it still fails, stop and report the defect plainly rather than papering over it.

## Phase 5 — Report + evolve

Summarize to the user (Portuguese — the owner is PT-native): what changed, where, the 3/3 print result, and the review verdict. Then offer the feedback loop: ask if positioning, team shape, or workflow should change. Record any harness change in `CLAUDE.md`'s change-history table.

## Data-passing protocol

- File-based (`.claude/_workspace/`) for artifacts and audit trail.
- Return-value-based for each agent's summary back to the orchestrator.
- Keep `_workspace/` after the run for traceability; only `index.html` (+ assets) is the real output.

## Error handling

- Agent fails → retry once with a sharper prompt; on second failure, proceed without it and note the gap in the report.
- Conflicting facts (e.g. two PR counts) → keep both with sources, never silently pick one.
- Broken/uncertain external link → flag it; do not ship an unverified URL onto a CV.

## Test scenarios

- **Normal:** "Add tdmcp to my CV." → strategist places it in Selected Repositories + 1–2 Tech Stack tags + an AI-native clause; engineer implements across HTML+en/pt/es; guardian confirms 3/3 pages; reviewer confirms still protocol-first, no stray English, no fabricated metrics. PASS.
- **Error:** an addition makes PT print 4 pages → guardian reports `pt: 4`; orchestrator routes a trim back to the engineer; guardian re-runs → `pt: 3`. PASS only after green.
