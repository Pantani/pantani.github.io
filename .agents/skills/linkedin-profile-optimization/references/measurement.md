# Measurement and recommendation contract

This is an observational audit, not a controlled experiment or a ranking predictor.

## Evidence schema

Every metric observation records:

- `metric`, `ui_label`, `definition`, `value` (number or `unknown`), `unit`.
- `source`, `observed_at`, `reporting_start`, `reporting_end`, `timezone`.
- `period_complete` (true/false/unknown), `duration_days`, `coverage` (live/historical/user-reported).
- `intervention_dates`, `concurrent_activity`, `limitations`.

Record the displayed reporting interval exactly. Do not manufacture a rolling week or infer a missing year/date from the host clock. Preserve historical notes and use the user's timezone for new observations. If unavailable, use `unknown`, not zero. A historical note verified as a local file is not a newly verified live metric.

## Metrics

| Metric | Use | Limitation |
| --- | --- | --- |
| Search appearances | Primary discovery count per displayed period | Not unique recruiters, profile views, messages or interviews |
| All appearances | Context for overall exposure | Includes other surfaces; never substitute for searches |
| Search share | `100 * search / all`, when the two values have compatible scope and all > 0 | Descriptive, not a target; rounded UI share may differ |
| Searcher titles and companies | Audience context using exact UI labels | Not the jobs searched for or proof of hiring intent |
| Job titles found for | Query/role relevance when UI exposes it | Keep separate from searcher occupations; unknown if unavailable |
| Profile views | Secondary interest signal with its own period | No search-to-view conversion unless attribution and denominator are supported |
| Qualified inbound | Owner-confirmed unique opportunity threads compatible with Go/backend, remote work and location eligibility | Do not read messages without scope; unknown unless supplied/authorized |
| Interviews from inbound | Owner-confirmed interviews associated with those opportunities | No division by search appearances as a conversion claim |

Qualify an opportunity by role, real Go/backend responsibilities, remote arrangement and ability to hire in the owner's location. Compensation is an additional filter only when the owner supplies one. Deduplicate follow-ups within the same opportunity. Record unknown eligibility separately. Do not persist names, message bodies or private contacts when aggregate counts suffice.

## Comparison eligibility

Compare only the same definitions, complete periods of equal duration, non-overlapping dates and consistent filters. An incomplete period, changed metric definition or missing boundary produces `comparable: false` with a reason. A period crossing a profile intervention is `transition`; it cannot be a clean post-change observation. After-change periods must start after the recorded change, but this does not imply that indexing has completed.

For eligible periods, report absolute change `current - baseline`. Percentage change is `100 * (current - baseline) / baseline` only when baseline > 0. For baseline = 0, report `percentage_change: unknown`, `reason: zero_baseline` and the absolute change. No infinity or fabricated percentage. If data are missing, neither change is computed.

Example: 0 to 20 across complete comparable weeks means +20 and percentage undefined. A 130-count complete week and a 100-count partial week are not a measured decline.

Use four subsequent complete reporting periods as a practical observation proposal, not a platform SLA or a statistical-significance guarantee. No automatic scheduling. Record posts, comments, connections, applications, profile edits and seasonality as possible confounders. Outcome wording is observational: "increased after changes; causation not established." Do not attribute the batch to one field or promise interviews.

## Market evidence and recommendation schema

When fresh vacancies can be inspected, select 5–10 distinct eligible employer postings as a manageable qualitative sample, not a market estimate. Record employer URL, access date, role, remote/location restrictions, required versus preferred terms, and evidence of eligibility. Exclude duplicates/closed postings; report actual coverage if fewer qualify. Platform job-title choices must be verified in the UI before proposing them as selectable values.

Build `term -> vacancy IDs -> career evidence -> existing profile section -> supported gap`. Frequency is descriptive only. Do not infer ranking weight from occurrence count, invent synonyms as past job titles, or add unsupported experience.

Every recommendation includes `id`, `priority`, `field`, `current_text`, `current_verified_at`, `proposed_text`, `evidence`, `claim_status`, `rationale`, `rejected_alternative`, `expected_metric`, `risk`, `authorization`, `state`. Use `keep`, `proposed`, `needs_evidence`, `authorized`, `applied`, `verified`, `failed` or `blocked` as state. An unobserved current field stays unknown; do not write a fictitious before/after diff. Expected search effects are hypotheses, not percentages.

Separate P1 documented discoverability/eligibility gaps, P2 evidence-backed clarity improvements and P3 presentation preferences. These are triage categories, not a score awarded by LinkedIn. Never generate an invented "profile SEO score". If no supported gap exists, keep the field.
