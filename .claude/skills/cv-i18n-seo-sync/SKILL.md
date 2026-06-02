---
name: cv-i18n-seo-sync
description: Mechanical correctness for editing Danilo Pantani's single-file HTML CV (index.html) without silently breaking its three languages or its SEO. Use whenever changing any user-visible text, adding a section/chip/tag, or touching title/meta/Open Graph/Twitter/JSON-LD/share-card. Covers the dual-source English rule (HTML default + en dict), the en/pt/es dicts, the &-vs-&amp; gotcha, full translation, and the SEO surfaces that must stay consistent with the canonical role.
---

# cv-i18n-seo-sync — Edit the CV without diverging languages or SEO

The CV is one file, `index.html`. Most user-visible strings exist in up to **4 synchronized places**. Miss one and a language silently diverges (this has caused real bugs).

## The dual-source rule for English

English text lives in TWO places that must always agree:

1. **HTML default** — inline text on an element carrying `data-i18n`, `data-i18n-html`, or `data-i18n-attr*`.
2. **The `en` dict** — a flat `"key": "value"` entry in the JS `translations` object.

When you change any English string, change **both**. (Past drift bugs — Advanced/Fluent, Kubernetes — came from editing only one.)

## The three dicts

`translations` holds three flat key→string maps: `en` (~L2941), `pt` (~L3108), `es` (~L3275). **Always grep the exact key first** — line numbers drift as the file changes. Every translatable string needs an entry in all three dicts **plus** the HTML default. After editing, grep-count the key across the three dicts to confirm 3/3 parity.

```bash
grep -n '"projects.intro"' index.html   # expect: 1 HTML default usage + en + pt + es
```

## The &-entity gotcha (gets people every time)

The same `&` must be escaped differently depending on how the value is applied:

- `data-i18n` → applied via **textContent**. Dict value uses a **plain `&`** (NOT `&amp;`). Writing `&amp;` renders the literal text "&amp;".
- `data-i18n-html` → applied via **innerHTML**. Dict value **must** use HTML entities (`&amp;`) and may contain tags (`<em>`, `<strong>`, `<a>`).
- `data-i18n-attr` + `data-i18n-attr-key` → sets an attribute (aria-label, title) from the keyed value.

Match the value's escaping to the attribute on the element it targets.

## Full translation

No stray English in PT/ES. Translate words, not just sentences ("range" → PT "abrangência", ES "alcance"). **Proper nouns and tech names stay as-is** in every language: Go, Cosmos SDK, IBC, TouchDesigner, MCP, tdmcp, TypeScript.

## Repo chips and tags usually need NO dict entry

A `.repo-chip` or `.tag` whose visible text is a literal token (e.g. `tdmcp`, `MCP`, `ignite/cli`) typically carries no `data-i18n` and needs **no** dict work — it's identical in all languages. Only **prose** (intros, summaries, bullet bodies) needs the 4-place treatment. This keeps additions cheap and low-risk.

## SEO / structured-data surfaces (keep protocol-first)

If the role string, primary keywords, or headline change, update **every** surface so they stay consistent and protocol-first:
`<title>` · `<meta name="description">` · Open Graph (`og:title`, `og:description`, `og:image`) · Twitter card · JSON-LD (WebSite + Person) · hero H1 + eyebrow · the **share card** (`share.cardTitle` in 4 spots: HTML default + en/pt/es) and `og-image.jpg`.

A non-protocol side project (e.g. tdmcp) normally **does not** touch these — adding it must not change the headline. Leave the protocol-first SEO intact.

## Workflow

1. Edit the HTML default (inline text).
2. Edit the `en`, `pt`, `es` dict entries (respect the &-rule per element type).
3. Grep the key across the three dicts → confirm 3/3 parity, no stray English.
4. Only if role/keywords changed: sync the SEO surfaces above.
5. Hand the diff to print-integrity + reviewer verification.
