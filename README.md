# Danilo Pantani

**Senior Backend Engineer**<br>
**Go (Golang) · Distributed Systems · Blockchain Infrastructure**

São Paulo, Brazil · Remote · UTC−3<br>
Brazilian and Italian citizen<br>
[danpantani@gmail.com](mailto:danpantani@gmail.com) · [GitHub](https://github.com/Pantani) · [LinkedIn](https://www.linkedin.com/in/dpantani/?locale=en-US) · [Telegram](https://t.me/dpantani)

[Live visual resume](https://pantani.xyz/) · [HTML source](./index.html)

---

## Professional summary

Senior backend engineer with 10+ years in software engineering, focused on Go backend services, distributed systems, and blockchain infrastructure. Experience includes leading backend work on Trust Wallet's multi-chain blockatlas, building Cosmos developer tooling at Ignite, and implementing AtomOne distribution-module changes.

Seeking remote Senior Backend Engineer and Senior Software Engineer roles focused on Go and distributed systems, including blockchain infrastructure.

## Selected engineering contributions

### AtomOne

- Implemented distribution-module changes for ADR-004 Nakamoto Bonus.
- Delivered governance migrations and validator-commission logic in the AtomOne Cosmos SDK fork.
- Evidence: [`atomone-hub/atomone`](https://github.com/atomone-hub/atomone) · [`atomone-hub/atomone-sdk`](https://github.com/atomone-hub/atomone-sdk)

### Ignite CLI

- Contributed 300+ public merged PRs across two engagements with Ignite CLI; this is a project total, not a count for the latest role.
- Worked on protobuf analysis, AST-based code generation, scaffold migrations, and CLI behavior.
- Evidence: [merged PRs](https://github.com/ignite/cli/pulls?q=is%3Apr+author%3APantani+is%3Amerged) · [`ignite/cli`](https://github.com/ignite/cli)

### Cosmos SDK and IBC-Go

- Fixed protobuf file resolution in Cosmos SDK AutoCLI ([#24330](https://github.com/cosmos/cosmos-sdk/pull/24330)).
- Added an IBC-Go capability-scope inspection helper and tests ([#6716](https://github.com/cosmos/ibc-go/pull/6716)).
- Evidence: [`cosmos/cosmos-sdk`](https://github.com/cosmos/cosmos-sdk) · [`cosmos/ibc-go`](https://github.com/cosmos/ibc-go)

### Trust Wallet blockatlas

- Contributed 200+ public merged PRs.
- Led backend work for multi-chain indexing, integrations, and full-node tooling.
- Contributed to the Node.js-to-Go migration and standardized concurrency patterns in the Go services.
- Evidence: [merged PRs](https://github.com/trustwallet/blockatlas/pulls?q=is%3Apr+author%3APantani+is%3Amerged) · [`trustwallet/blockatlas`](https://github.com/trustwallet/blockatlas)

## Core expertise

| Area | Technologies and focus |
|---|---|
| **Go Backend & Distributed Systems** | Go (Golang), backend engineering, distributed systems, software architecture, system design, HTTP APIs, concurrent processing, goroutines, worker pools, fan-out processing, batching, context cancellation |
| **Blockchain & Protocol Engineering** | Cosmos SDK, CometBFT, Tendermint, IBC, validator infrastructure, AtomOne, Gno, Ethereum, EVM, Bitcoin / UTXO, zk-SNARKs, Layer 2, rollup infrastructure |
| **Platform Engineering, Cloud & DevOps** | Kubernetes, Docker, Helm, Terraform, Pulumi, Ansible, AWS, GCP, GitHub Actions, CI/CD, Prometheus, Grafana, observability, cloud deployments, production operations |
| **Developer Tooling** | Cobra, Viper, protobuf analysis, AST-based code generation, scaffolding, migrations, CLI design, release tooling |
| **Technical Leadership** | Hands-on team leadership, system design, technical decisions, code review, and cross-functional delivery across backend, mobile, and product engineering |
| **Full-Stack, Mobile & IoT** | JavaScript, TypeScript, React; native iOS and Android with Objective-C, Swift, Java, and Kotlin; OpenCV/C++, beacons, Wi-Fi, Arduino, Raspberry Pi |
| **Engineering Workflow** | Repository context, refactoring, and MCP tooling for TouchDesigner through tdmcp |

## Professional experience

### Go Backend Engineer & Blockchain Developer — Danilo Pantani

**Self-employed · Apr 2026–Present · Remote**

Independent work combining blockchain developer tooling with occasional project-based backend engagements.

- Take on occasional backend and Go assignments for external clients.

### Blockchain Engineer, Go — Developer Platform & Distributed Systems — Ignite (All in Bits)

**Full-time · Dec 2022–Mar 2026 · Remote**

- Developed Go developer tooling in Ignite CLI: AST-based source transformations, Protocol Buffers code generation, module and migration scaffolding, application wiring, and compatibility updates across Cosmos SDK, CometBFT and IBC-Go.
- Built and extended Ignite apps for Hermes relaying, CosmWasm and fee-abstraction integration. Implemented Spaceship remote chain deployment over SSH/SFTP, including process control, logs, faucets and archive extraction.
- Implemented AtomOne protocol changes: ADR-004 Nakamoto Bonus distribution, epoch-based execution, validator commission constraints and updates, and governance migration fixes.
- Implemented VaaS consumer fee pools, provider validator payments and debt-state propagation, with transaction admission rules that preserve IBC and governance recovery operations. Added misbehaviour validation and IBC v2 fixes.
- Extended IBC functionality in Gno Realms with transfer memos, GRC20 voucher transfer and approval helpers, relay authorization, and query views.
- Contributed upstream fixes to Cosmos SDK AutoCLI protobuf descriptor resolution and an IBC-Go helper for inspecting existing capability scopes.

### Blockchain Engineer, Go — Cosmos Hub & Interoperability — Interchain Foundation

**Full-time · Jun 2022–Dec 2022 · Remote**

- Maintained and evolved Gaia, the Cosmos Hub application, implementing bug fixes, upgrades and ongoing improvements across the Go codebase.
- Implemented end-to-end coverage for vesting accounts, fee grants and sponsored transactions, validator unjailing, transaction encoding/decoding, and interchain accounts controlled through governance and groups.
- Added ICA authorization unit tests, refactored shared E2E query and execution helpers, and improved test coverage workflows and CI handling of documentation-only changes.

### Senior Blockchain Engineer, Go — Developer Tooling — Ignite (Tendermint)

**Full-time · Jun 2021–Jun 2022 · Remote**

- Implemented Go modules and transaction flows for SPN: coordinator and validator profiles, chain-launch requests, genesis accounts and validators, campaign share allocation, vesting vouchers and reward distribution.
- Developed new features and maintained Ignite CLI, fixing bugs and keeping it up to date with Cosmos SDK changes.
- Added genesis validation and simulation coverage, and corrected concurrency issues in CLI progress and context-aware input handling.

### Blockchain / Layer-2 Engineer, Go — Hermez Network

**Full-time · Feb 2021–Jun 2021 · Remote**

Go backend and integration tooling for an Ethereum Layer-2 zk-SNARK rollup.

- Refactored transaction selection in Go for the Ethereum L2 rollup, adding atomic transaction support and unit tests.
- Integrated Go services with Ethereum smart contracts via ABI to submit zk-SNARK proofs for rollup batches.
- Built Go integration examples for Baby Jubjub wallet derivation, Ethereum account authorization, and L2 transaction signing, submission and tracking.
- Added account-authorization synchronization from the rollup contract, Prometheus instrumentation, and race detection in unit tests.

### Backend Engineer / Architecture — Go, Kubernetes & Observability — Energi Core

**Full-time · Apr 2020–Feb 2021 · Remote**

Designed the overall architecture and built core Go backend services for a cryptocurrency exchange from the ground up, owning application services, infrastructure and operational workflows. Worked alongside an engineer responsible for the matching engine.

- Developed APIs and backend workflows for user accounts, KYC, deposits, withdrawals and transaction tracking, integrating multiple cryptocurrencies and blockchain networks.
- Built custodial-wallet services covering user wallets, private-key custody and blockchain integrations.
- Designed SQL data models and implemented Kafka-based asynchronous processing, including background workers for reconciliation and balance management.
- Designed and deployed infrastructure on AWS and GCP using Kubernetes and Helm charts, with HashiCorp tooling including Vault, Consul and Terraform, plus Ansible for infrastructure automation.
- Built GitHub Actions delivery pipelines for services and full nodes, and implemented production monitoring using Prometheus and Grafana.

### Backend Lead, Go — Trust Wallet — Binance

**Full-time · Aug 2019–Apr 2020 · Remote**

Led backend work on blockatlas, Trust Wallet's multi-chain backend.

- Built and maintained chain integrations, transaction parsing, asset-data routes and indexing workflows in Go.
- Contributed to the migration from Node.js to Go and standardized worker pools, fan-out processing, batching and context cancellation.
- Added HTTP metrics and a metrics endpoint for Prometheus, making request behavior available for monitoring.
- Operated and monitored full nodes supporting the wallet's multi-chain infrastructure.
- Built the Go backend for a Binance crypto gift-card and promotional redemption system, enabling token claims in Trust Wallet via QR codes and single-use links. Implemented redemption-code generation and validation, link expiration and invalidation, and Binance Chain token transfers.
- Evidence: [`redemption` Go backend implementation](https://github.com/prazd/redemption/commit/8a4e8bf3dd686b2ffa2ed4d480c32cc6a9725198).

### Tech Lead — Backend & Mobile — Mercado Bitcoin

**Full-time · Mar 2018–Aug 2019 · São Paulo, Brazil**

Technical leadership across exchange backend services and mobile engineering.

- Built Go and Python services for multi-chain transaction tracking and payload signing.
- Maintained wallet workflows connected to the exchange ledger and matching systems.
- Led a seven-person mobile team and coordinated customer-facing delivery across backend, iOS, Android and web engineering.

### Staff Engineer — XP Inc.

**Full-time · Dec 2017–Mar 2018 · São Paulo, Brazil**

Staff Engineer at XP, working on XDEX, a digital-asset exchange within the group, and a structured-credit product.

- Led the entire 15-person XDEX exchange engineering team as Staff Engineer, combining technical leadership with hands-on work across technical decisions, development and delivery.
- Built and maintained .NET exchange services running on Microsoft Azure.
- Served as technical lead on the structured-credit product.

### Full-Stack Developer — Finchain — Sep 2017–Nov 2017

Developed smart contracts and applications on Ethereum, including ERC-20 wallets, DApps and ICO workflows. Also built native mobile applications and reconciliation systems supporting exchange operations.

### Mobile Developer (Android / iOS) — Neon — Jan 2017–Nov 2017

Developed and maintained native iOS and Android applications, including document-capture and image-recognition workflows using OpenCV and C++.

### Co-Founder / CTO — Miya Solutions — Jan 2016–Jan 2017

Co-founded a real-time people-management platform and led its technical direction, using Wi-Fi signals for presence and location workflows.

### Co-Founder / CTO — Pixon — Jan 2014–Jan 2017

Co-founded the company and led engineering across native mobile applications, automation and micro-location products using beacons and Wi-Fi.

### Mobile Developer (Android / iOS) — Ice Juice Lemon — Jun 2013–Jan 2014

Led the mobile development team while building and maintaining native iOS and Android applications.

### Mobile Developer (Android / iOS) — iai? Instituto de Artes Interativas — Jul 2012–Jun 2013

Developed native iOS and Android applications and delivered practical mobile-development training.

### iOS Developer — Brandish Ad — Nov 2011–Jul 2012

Built and maintained native iOS applications.

### Trainee — Construtora Camargo Corrêa — Jun 2010–Aug 2010

Supported electrical-engineering activities at the Jirau Hydroelectric Power Plant construction site in Porto Velho, Brazil.

## Personal projects

- Build tdmcp, an MCP server for TouchDesigner, and Ableton Mind, an MCP server for Ableton Live, using TypeScript and Python to connect AI assistants with creative applications.
- Rust personal study: Sunscreen for Solana and stellar-forge for Stellar; no professional Rust experience.

## Selected repositories / evidence

- [`ignite/cli`](https://github.com/ignite/cli) — Cosmos SDK tooling, protobuf analysis, AST-based code generation, CLI behavior
- [`ignite/network`](https://github.com/ignite/network) / [`tendermint/spn`](https://github.com/tendermint/spn) — chain-launch tooling and sovereign-chain lifecycle
- [`atomone-hub/atomone`](https://github.com/atomone-hub/atomone) / [`atomone-hub/atomone-sdk`](https://github.com/atomone-hub/atomone-sdk) — AtomOne chain and Cosmos SDK fork
- [`cosmos/cosmos-sdk`](https://github.com/cosmos/cosmos-sdk) — protocol modules and interface registry
- [`cosmos/ibc-go`](https://github.com/cosmos/ibc-go) — interoperability, capability keeper, module composition
- [`cosmos/gaia`](https://github.com/cosmos/gaia) — Cosmos Hub / ATOM chain application
- [`allinbits/vaas`](https://github.com/allinbits/vaas) — validator and consumer-chain lifecycle workflows
- [`hermeznetwork/hermez-node`](https://github.com/hermeznetwork/hermez-node) — Ethereum Layer 2 and zk-SNARK rollup operator services
- [`hermeznetwork/hermez-integration`](https://github.com/hermeznetwork/hermez-integration) — Go wallet authorization and L2 transaction integration examples
- [`trustwallet/blockatlas`](https://github.com/trustwallet/blockatlas) — multi-chain indexing, integrations, and full-node tooling

## Teaching and talks

- **FIAP (Nov 2021–May 2022, part-time):** Taught blockchain fundamentals and Ethereum dApp development in MBA courses, guiding students through Solidity smart contracts for escrow and polling applications.
- **Go Blockchain (Jan 2018–Aug 2019, freelance):** instructor in Ethereum blockchain development and smart contracts for mobile.
- **Let's Code (Sep 2016–Jul 2019, part-time):** taught programming fundamentals and Java.
- **Web3Family 2023, Barcelona:** building Cosmos SDK chains and developer tooling with Ignite.
- **AwesomWasm 2023, Berlin:** workshop on the Ignite stack and roadmap.
- **ETH São Paulo 2021:** zk-SNARKs and Ethereum Layer-2 rollup infrastructure.

## Education, certifications and languages

- **Universidade Presbiteriana Mackenzie:** Computer Science coursework (6 semesters completed) and Electrical Engineering coursework (8 semesters completed); neither degree completed. São Paulo, Brazil.
- **Certifications:** Data Science - Let's Code Academy (2021, 48h); Programming Blockchain - Jimmy Song (2018, 16h); Ethereum Blockchain Developer - Go Blockchain (2017, 16h); Smart Contracts in Ethereum Blockchain - FIAP (2017, 8h); Blockchain Development - Finchain / Blockchain Brazil (2017, 16h).
- **Languages:** Portuguese — native; English — advanced; Spanish — advanced.

## Repository

This repository contains a static, bilingual visual portfolio.

- [`index.html`](./index.html) — English and Brazilian Portuguese CVs
- [`output/pdf/`](./output/pdf/) — generated resume PDFs
- [`og-image.jpg`](./og-image.jpg) — 1200×630 social preview for LinkedIn, WhatsApp, Slack, Discord, Telegram, and X
- [`robots.txt`](./robots.txt) and [`sitemap.xml`](./sitemap.xml) — crawler discovery for the canonical homepage
- [`humans.txt`](./humans.txt) — human-readable contact card

## CV analysis and implementation builds

Install the validation dependencies in a dedicated Python environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-cv.txt
make cv-analyze PYTHON=.venv/bin/python CV_RUN_DIR=_workspace/cv-quality/my-audit
# Apply the audited source/content changes, then regenerate and validate:
make cv-implement PYTHON=.venv/bin/python CV_RUN_DIR=_workspace/cv-quality/my-audit
make cv-test PYTHON=.venv/bin/python
```

Use a new `CV_RUN_DIR` for each new audit. Analysis preserves source hashes, parser versions and extraction evidence; implementation requires that baseline and records an incomplete state before generation. Repeated implementation attempts within the same run retain the original analysis. The workflow is defined in [CV quality](.agents/skills/cv-quality/SKILL.md) and its [team contract](docs/harness/cv-quality/team-spec.md).

Generation requires Chrome/Chromium and a local Python HTTP server. `CHROME_BIN` selects an executable and `PDF_SERVER_PORT` changes the default local port (8765). Both supported PDFs are generated in staging before replacing the existing files. The implementation build validates staging before promotion; generation or quality failure preserves the previous set. Final file moves are serialized, not a filesystem transaction. Run `bash scripts/generate-pdfs.sh` for generation alone, or use the implementation build for mandatory local validation.

The print stylesheet uses static system fonts, neutralizes inherited screen layering, and disables presentation ligatures. Checks require two pages per language, at least 9pt visible text, and the expected section order in two independent readers. Inspect every rendered page as well: automated extraction checks do not prove visual quality or compatibility with an employer's ATS. No job-match score is produced.

The PDF selects two short courses and compact earlier-job records; this README retains the fuller history. Career statements come from the owner's existing record. Missing client metrics or employer-specific technology evidence must never be invented to improve keyword matching.
