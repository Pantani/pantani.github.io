---
name: cv-print-integrity
description: Keep Danilo Pantani's HTML CV (index.html) printing to exactly 3 A4 pages in English, Portuguese, and Spanish. Use after any content or CSS change — especially adding Tech Stack tags or Selected Repositories chips — to verify the page count via headless Chrome and protect the deterministic pagination model and the intentional sidebar order.
---

# cv-print-integrity — The CV must stay a clean 3-page A4 PDF in EN/PT/ES

## The invariant

The CV prints to **exactly 3 A4 pages in all three languages**. PT and ES wrap ~10–15% longer than EN, so EN passing does not guarantee PT/ES pass. Verify all three after any content or CSS change.

## Why it's fragile

Page count is driven by `break-inside: avoid` blocks straddling a page boundary, **not** just total height. An avoid-block that can't fit the remaining space jumps **wholesale** to the next page and can push a later section onto a **4th page**. The **Tech Stack tag cloud** and **Selected Repositories chips** are the usual culprits — they grow with exactly the kind of additions this CV gets. Re-verify all three languages whenever you touch them.

## Pagination model (don't fight it)

- **MAIN column** — deterministic via `break-before: page` on `.experience-title` (→ page 2) and `.repos-section` (→ page 3).
- **SIDEBAR** — flows freely down the right column with **no** forced break. (A forced break here once stranded page space and pushed content to a 4th page. Never "fix" a spill by adding a sidebar break.)
- **Cohesion** — `break-inside: avoid` on cards / edu-groups / the Languages panel; `break-after: avoid` on every `.side-panel-head` and `.edu-group h3` so no heading is orphaned.
- **Resulting layout** — P1: Core Expertise + Open Source │ Summary + Languages · P2: Experience │ Highlights + What-I'm-looking-for + Tech Stack + Education · P3: Selected Repositories │ Teaching & Talks.

## Sidebar order is intentional — do not reshuffle

Summary → Languages → Highlights → What I'm looking for → Tech Stack → Education → Teaching & Talks. Languages sits right after Summary specifically so it lands on PDF page 1; Tech Stack sits before Education.

## Verification recipe

Language is selected by `?lang=` (URL param beats localStorage; see `initLang` ~L3394). Serve the file, print each language headless, count pages:

```bash
cd <repo root>
python3 -m http.server 8099 >/dev/null 2>&1 &  SRV=$!; sleep 1
CHROME="$(ls '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' 2>/dev/null || command -v google-chrome chromium chromium-browser 2>/dev/null | head -1)"
for L in en pt es; do
  "$CHROME" --headless=new --disable-gpu \
    --print-to-pdf="/tmp/cv_$L.pdf" "http://localhost:8099/index.html?lang=$L" 2>/dev/null
done
kill $SRV 2>/dev/null
for L in en pt es; do
  printf "%s: " "$L"
  if command -v pdfinfo >/dev/null; then pdfinfo "/tmp/cv_$L.pdf" | awk '/^Pages/{print $2}'
  else mdls -name kMDItemNumberOfPages -raw "/tmp/cv_$L.pdf"; echo; fi
done
```

Expect `3` for each. The recipe is a starting point — adapt the Chrome path/flags and the page-count tool (`pdfinfo` from poppler, or macOS `mdls`) to what's installed.

## If a language prints 4 pages

1. Identify which `break-inside: avoid` block straddles the boundary (usually the Tech Stack cloud after new tags, or the repos block after new chips).
2. Fix at the source: trim copy, drop a marginal tag, or report back to the strategist that the addition doesn't fit the budget.
3. Do **not** add forced page breaks to the sidebar or shrink fonts blindly — that masks the spill and breaks the model.
4. Re-run the recipe until all three read `3`.
