# Career description draft

Status: local draft; not published.

## Ignite (All in Bits) — December 2022 – March 2026

- Developed Go developer tooling in Ignite CLI: AST-based source transformations, Protocol Buffers code generation, module and migration scaffolding, application wiring, and compatibility updates across Cosmos SDK, CometBFT and IBC-Go.
- Built and extended Ignite apps for Hermes relaying, CosmWasm and fee-abstraction integration. Implemented Spaceship remote chain deployment over SSH/SFTP, including process control, logs, faucets and archive extraction.
- Implemented AtomOne protocol changes: ADR-004 Nakamoto Bonus distribution, epoch-based execution, validator commission constraints and updates, and governance migration fixes.
- Implemented VaaS consumer fee pools, provider validator payments and debt-state propagation, with transaction admission rules that preserve IBC and governance recovery operations. Added misbehaviour validation and IBC v2 fixes.
- Extended IBC functionality in Gno Realms with transfer memos, GRC20 voucher transfer and approval helpers, relay authorization, and query views.
- Contributed upstream fixes to Cosmos SDK AutoCLI protobuf descriptor resolution and an IBC-Go helper for inspecting existing capability scopes.

## Interchain Foundation — June 2022 – December 2022

- Maintained and evolved Gaia, the Cosmos Hub application, implementing bug fixes, upgrades and ongoing improvements across the Go codebase.
- Implemented end-to-end coverage for vesting accounts, fee grants and sponsored transactions, validator unjailing, transaction encoding/decoding, and interchain accounts controlled through governance and groups.
- Added ICA authorization unit tests, refactored shared E2E query and execution helpers, and improved test coverage workflows and CI handling of documentation-only changes.

## Ignite (Tendermint) — June 2021 – June 2022

- Implemented Go modules and transaction flows for SPN: coordinator and validator profiles, chain-launch requests, genesis accounts and validators, campaign share allocation, vesting vouchers and reward distribution.
- Developed new features and maintained Ignite CLI, fixing bugs and keeping it up to date with Cosmos SDK changes.
- Added genesis validation and simulation coverage, and corrected concurrency issues in CLI progress and context-aware input handling.

## Hermez Network — February 2021 – June 2021

Status: published to LinkedIn and verified by read-back on October 8, 2026.

Developed Go backend and integration tooling for Hermez, an Ethereum Layer-2 zk-SNARK rollup.

• Refactored the node's transaction selector, adding atomic transaction support and unit tests for transaction groups and batch selection.
• Built hermez-integration, a Go integration example for exchanges, covering Baby Jubjub wallet derivation from Ethereum wallets, Hermez address encoding/decoding, and signed account-creation authorization linking Ethereum addresses with Baby Jubjub public keys.
• Implemented L2 transaction flows for signing and submitting transfers to Baby Jubjub addresses, Ethereum addresses and account indices, plus exits and transaction-status tracking.
• Added account-authorization synchronization from the rollup contract, Prometheus instrumentation for the node, and race detection in unit tests.
