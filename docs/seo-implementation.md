# Portfolio SEO implementation — 2026-10-09

The public portfolio is built from the existing CV source into an explicit static artifact. English and Brazilian Portuguese have independent crawlable URLs. This avoids depending on JavaScript translation or a visitor's previous language selection for initial content.

## Implemented

- Ten canonical pages: two portfolio pages, two article indexes and six localized case studies.
- Self-referencing canonical URLs and reciprocal `en`, `pt-BR`, and `x-default` alternates.
- Localized titles, descriptions, Open Graph and Twitter metadata; current social card and raster favicon.
- ProfilePage/Person, WebSite, CollectionPage, Article and BreadcrumbList structured data with stable identity URLs and accurate modification dates.
- Internal links to substantive articles about Go backend work, developer tooling and upstream fixes. Public implementation evidence supports each article; limitations and provenance are recorded separately.
- Shared stylesheets, locally hosted licensed font subsets and deferred enhancement scripts. Locale content is present in the initial HTML.
- Generated sitemap, crawlable robots rules, noindex 404 and an explicit publication allowlist. The cover editor and repository/workspace files are excluded.
- Legacy language URLs preserve query parameters and anchors. References remain optional and the existing English/PT PDF URLs remain stable.
- CI runs source tests, metadata/link validation and complexity checks before publishing `_site/`. Only `main` deploys.

## Verified locally

40 Python tests, four JavaScript runtime tests and six reference-view browser checks passed. ESLint, Ruff and complexipy passed with cyclomatic limit 6 and cognitive limit 10. The generated artifact passed canonical, reciprocal-language, structured-data, local-link, sitemap and publication checks. English/PT home, article index and article layouts were inspected in the browser, including a 390px mobile viewport. After integrating the latest public evidence update, reference navigation preserved 124 links, language, query and anchor.

Existing PDFs were preserved, inspected visually and passed strict extraction checks in pypdf and pdfplumber: two pages each, minimum visible font 9pt, no reported findings. This is a local readability check, not an ATS vendor score.

The source HTML is 179,036 bytes and generated English HTML is 49,491 bytes after integrating the latest public evidence update. Styles, scripts and fonts remain separate downloads; the HTML reduction is not a measured loading-time improvement.

## Measurement still requires external access

Search Console opened the unauthenticated landing page in this session. Property access is needed to submit the generated sitemap, inspect URLs and measure impressions, clicks and queries. PageSpeed API requests during the audit returned HTTP 429; no Lighthouse score or field Core Web Vitals result is claimed. Search ranking changes must be measured after indexing, rather than inferred from implementation.

Do not add fabricated Search Console verification files, analytics identifiers, career metrics or continuously renewed sitemap dates. Keep the separately published L200 project and its sitemap independent.
