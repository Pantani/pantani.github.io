# LinkedIn coherence drafts

> **Superseded 2026-11-10.** The live LinkedIn profile now uses "Staff Backend Engineer" (headline, About, Featured CV), and Kafka, RabbitMQ and NATS are on the site under Mercado Bitcoin. The current texts are on LinkedIn and in index.html; this file keeps the earlier drafts for history.

Status: local draft; not published. Prepared on 2026-11-09 by comparing the LinkedIn profile with the CV PDFs and `index.html` at commit `8a36623`.

Assumption: Energi was removed on purpose (commit `530d1e9`). If that is wrong, keep the Energi bullet and restore the role in the CV and site instead.

## 1. About (replace the whole field)

Only change: the Energi bullet is removed.

```text
Senior backend engineer with 10+ years in software engineering, building Go services, distributed systems and blockchain infrastructure for remote teams.

• Trust Wallet / Binance — led Go backend work on the multi-chain blockatlas: chain integrations, transaction indexing, staking and market-data APIs, and the Node.js-to-Go migration (200+ merged PRs).
• All in Bits (2021–2026) — built Go developer tooling for Ignite CLI: AST-based code transformations, Protobuf generation, scaffolding and Cosmos SDK migrations (300+ merged PRs). Implemented protocol work for AtomOne, VaaS and Gno IBC.
• Interchain Foundation — maintained Gaia, the Cosmos Hub application, with E2E coverage for vesting, fee grants and interchain accounts.
• Mercado Bitcoin — tech lead for exchange backend services and a 7-person mobile team.

Stack: Go (Golang), gRPC, Protocol Buffers, REST APIs, SQL/PostgreSQL, Kafka, Docker, Kubernetes, Helm, Terraform, AWS, GCP, Prometheus, Grafana, Cosmos SDK, CometBFT, IBC, Ethereum/EVM.

I'm looking for my next remote Senior Backend / Go Engineer role in distributed systems, infrastructure or blockchain, and I'm open to relocation. Available to start immediately. Brazilian & Italian citizen, UTC−3. If you're hiring for this kind of role, message me directly. I reply to every recruiter. Portfolio and CV: pantani.xyz
```

Owner to confirm:

- Kafka is kept because the Mercado Bitcoin entry on LinkedIn supports it, but it does not appear in the CV or site. Remove it here if it is no longer a skill to highlight.
- "Open to relocation" and "Available to start immediately" appear only on LinkedIn. Keep them only if they are still true.

## 2. Featured: CV item description (replace)

```text
Updated two-page CV for remote Senior Backend Engineer and Senior Software Engineer roles. Go, distributed systems and blockchain infrastructure, plus React Native work at Neon and Ethereum dApp teaching with Angular and React at FIAP. Rust projects are personal study. Updated November 2026.
```

## 3. Education

Delete this duplicate entry. The two other Mackenzie entries already hold the correct details:

- Universidade Presbiteriana Mackenzie — "Computational Science" — "six semesters completed. Electrical Engineering: eight semesters completed. Neither degree completed."

Universidade Metodista de São Paulo (Rádio e TV) appears only on LinkedIn. Keep or remove it at the owner's discretion; the CV selects what it shows.

## 4. Languages (add)

| Language | LinkedIn level |
|---|---|
| Portuguese | Native or bilingual |
| English | Full professional |
| Spanish | Full professional |

The CV says "Advanced" for English and Spanish. LinkedIn has no such level, so "Full professional" is the closest match; use "Professional working" if that describes them better.

## 5. Interchain Foundation (add as the first line of the description)

```text
Held in parallel with my All in Bits role.
```

This matches the CV and site, and explains why two full-time roles overlap from Jun 2022 to Feb 2023.

## 6. Open to Work: job titles (replace)

Matches the roles named on the site, plus the blockchain title used in the headline:

- Senior Backend Engineer
- Senior Software Engineer
- Staff Software Engineer
- Blockchain Engineer
- Blockchain Developer

## 7. Still to check on the profile

- Contact info: confirm the website is `https://pantani.xyz/`.
- The stray "Present" under the self-employed role, probably the title of an attachment.
- Projects: whether tdmcp is listed.
- IBC-Go project: it mentions "core/transfer-path fixes", but only PR #6716 could be confirmed. Narrow the text if there were no others.
