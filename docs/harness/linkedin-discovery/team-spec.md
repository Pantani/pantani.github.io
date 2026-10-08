# LinkedIn discovery audit

## Goal and architecture

Extend the existing `linkedin-profile-optimization` skill to audit search discovery and qualified remote Go/backend opportunities. Use a single-owner Pipeline: inventory -> evidence -> recommendations -> measurement -> review. The browser and evidence are tightly coupled; permanent specialist agents add coordination without a separate owned outcome. Optional independent read-only evaluation can test the contract. No recursive delegation, provider pins, SDK, build server or runtime adapter is required.

Canonical behavior: [.agents skill](../../../.agents/skills/linkedin-profile-optimization/SKILL.md). This document owns artifact naming and execution boundaries; the skill owns domain rules. Existing `_workspace/00_contract_inventory.md`, `01_linkedin_study.md` and `02_linkedin_changes.md` are historical records and must remain intact.

## Run entry point

Invoke `linkedin-profile-optimization` with a request such as:

> Audit my LinkedIn discovery for remote Go/backend work using current profile data, complete reporting periods and career evidence. Produce prioritized English drafts and measurement records. Do not publish profile changes.

Create `_workspace/linkedin-discovery/YYYY-MM-DD/` using the user's date. If it exists, resume only the same explicitly identified run; otherwise allocate the first unused `-02`, `-03`, etc. Name this path `RUN` below. Keep run outputs local; never stage, publish or upload analytics incidentally. No automatic commit or push. Ordinary definitions/explanations create no run.

## Owner contract

```yaml
role: profile-auditor
responsibility: evidence-based audit, proposals, measurement and final synthesis
skills: [linkedin-profile-optimization]
inputs: [user-scope, profile, analytics-periods, career-evidence, eligible-vacancies]
outputs: [inventory, evidence, recommendations, measurement, validation]
resources:
  reads: [public-primary-sources, authorized-profile, local-career-records]
  writes: [RUN]
  external_mutable: []
ownership:
  requirement: serialized-writer
  enforcement: advisory
workspace:
  preference: shared-existing-checkout
  fallback: local-drafts-with-explicit-missing-capabilities
communication:
  clarification_target: user
  escalation_target: user
permissions:
  shell: scoped-local-inspection-and-artifacts
  write_repo: RUN-only-during-audit
  network: public-sources-and-authorized-profile
  external_write: false
  spawn:
    default: false
    independent_read_only_review: allowed_when_justified
model_policy: inherit
runtime_overrides: {}
completion:
  artifact: RUN/04_validation.md
  states: [complete, partial, blocked]
```

Harness maintenance may update the canonical skill and this contract under its own request. External editing is a separate authorized mode: record the user's field scope, then give the same owner serialized write access only to those fields. A previous session's broad edit scope does not turn a new audit into an edit request. Report applied, failed and read-back-verified separately.

## Durable handoffs

Every output starts with producer, consumer, actual path, schema name, completion state and date. Producer is `profile-auditor` except review; subsequent phase and owner are the consumers. Link sources near claims. Use English in files.

| Phase / path under RUN | Required sections | Completion condition |
| --- | --- | --- |
| `00_contract_inventory.md` | Existing skills/roles, runtime capabilities, drift, scope, domain summary, architecture decision | Existing records preserved and scope stated |
| `01_evidence.md` | Profile snapshot, metric observations, career evidence, vacancy matrix, sources and missing inputs | Provenance/freshness explicit; partial allowed |
| `02_recommendations.md` | Ranked recommendations under the measurement schema, keep decisions, draft text, authorization and change status | Each suggestion tied to evidence or marked needs_evidence |
| `03_measurement.md` | Baseline, intervention ledger, comparable-period table, absolute/percentage changes, qualified outcomes and limitations | Unknowns and comparison eligibility explicit |
| `04_validation.md` | Coverage, factual/scope review, scenario results, path checks, acceptance and follow-up inputs | No unsupported claim of live coverage or measured lift |

## Failure and review policy

- Missing authentication/tool/permission: identify the missing capability, preserve local evidence, produce historical-only or partial outputs. A login form is not an empty profile. Request only the missing access; finish independent work.
- Conflicting snapshots: retain dates and provenance, prioritize verified live state and explicit owner corrections, mark unresolved conflicts. Never silently replace history.
- Missing career or vacancy evidence: mark needs_evidence; do not invent a draft claiming it. Missing analytics block outcome assessment, not the entire harness.
- Resource conflict: serialize; stop concurrent writes before proceeding. Workspace unavailable: return bounded drafts and state unsaved outputs.
- Optional review delegation is permitted only when its independent evaluation value is explicit. Reviewer has no browser, file writes, external writes or further spawn permission. Owner synthesizes results. Spawn/tool/model/communication failure means disclosed self-review; missing review output cannot count as a pass.
- Maximum two targeted review revisions per run; unresolved factual or scope problems remain partial/blocked. No unbounded retry loop.

## Acceptance

Validate the normal audit, partial/transition weeks, zero baseline, missing live access, factual career boundaries and a near-miss explanation. Inspect links and frontmatter. Separate harness validity, audit coverage and career outcomes. A correct manual baseline stays reported as correct; no claim that the skill increased searches without subsequent evidence.
