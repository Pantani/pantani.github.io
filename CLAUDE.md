# pantani.github.io — Danilo Pantani's HTML CV

Single-file CV/portfolio (`index.html`) deployed via GitHub Pages. Trilingual (EN/PT/ES), protocol-first positioning, prints to a clean 3-page A4 PDF.

## Harness: CV maintenance & review

**Goal:** evolve the CV (add/update projects, copy, SEO, i18n) and review it end-to-end without breaking positioning, three-language sync, or the 3-page print invariant.

**Trigger:** for ANY change to the CV — add/update a project, repo, skill, or role; reword copy; fix SEO/i18n; restyle; or run an analytical / end-to-end review — use the `cv-orchestrator` skill. It runs four specialists (strategist → engineer → layout-guardian + reviewer) defined in `.claude/agents/`, backed by skills `cv-positioning`, `cv-i18n-seo-sync`, `cv-print-integrity`. Simple factual questions about the CV can be answered directly.

**Non-negotiables (enforced by the harness):**
- Protocol-first identity: "Staff Blockchain Protocol Engineer · Go · Cosmos SDK · IBC". Full-stack/DevOps/AI/art are *range/curiosity*, never the headline.
- No fabricated metrics; verify numbers/URLs before shipping them onto the CV.
- English lives in two places (HTML default + `en` dict); every string in en/pt/es; mind the `&` vs `&amp;` rule per `data-i18n` vs `data-i18n-html`.
- Must stay exactly 3 A4 pages in EN, PT, and ES.

**Change history:**
| Date | Change | Target | Reason |
|------|--------|--------|--------|
| 2026-05-28 | Initial harness build (4 agents + 4 skills + orchestrator) | whole harness | Add tdmcp to the CV and enable ongoing review |
