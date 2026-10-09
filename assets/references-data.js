// Public, authored contributions. Curated mapping; not an exhaustive PR inventory.
const CV_REFERENCES = {
  "checkedOn": "2026-10-09",
  "claims": {
    "exp.ignite.b1": {
      "sources": [
        {
          "url": "https://github.com/ignite/cli/pull/3553",
          "title": "feat: change app.go to v2 and add AppWiring feature",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/3659",
          "title": "feat: cosmos-sdk `v0.50.x`",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/4004",
          "title": "feat: remove all import placeholders using the `xast` pkg",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/4877",
          "title": "feat: remove app config and ibc add route placeholders",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/4884",
          "title": "feat: remove autocli placeholders",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/4090",
          "title": "feat: remove `protoc` pkg and also nodetime helpers `ts-proto` and `sta`",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/4133",
          "title": "feat: improve buf rate limit",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/4902",
          "title": "feat: scaffold migrations",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/ibc-go/pull/6716",
          "title": "feat: add a method to check if the scope module already exists in the capability keeper",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/cosmos-sdk/pull/24330",
          "title": "fix: use the gogoproto merge registry as a file resolver instead of the interface registry",
          "kind": "pr"
        }
      ]
    },
    "exp.ignite.b2": {
      "sources": [
        {
          "url": "https://github.com/ignite/apps/pull/3",
          "title": "feat: add hermes relayer plugin",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/apps/pull/60",
          "title": "feat: cosmwasm official app",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/apps/pull/130",
          "title": "feat: add fee abstraction app",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/apps/pull/103",
          "title": "feat: spaceship",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/apps/pull/144",
          "title": "feat: spaceship faucet",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/apps/pull/251",
          "title": "refactor(spaceship): make tarball extraction safe",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/apps/pull/124",
          "title": "feat: add real time logs for spaceship",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/apps/pull/145",
          "title": "feat(spaceship): improve logs",
          "kind": "pr"
        }
      ]
    },
    "exp.ignite.b3": {
      "sources": [
        {
          "url": "https://github.com/atomone-hub/atomone-sdk/pull/10",
          "title": "feat: ADR-004 (Nakamoto Bonus)",
          "kind": "pr"
        },
        {
          "url": "https://github.com/atomone-hub/atomone-sdk/pull/19",
          "title": "feat: fixed commission rate and max rate parameter",
          "kind": "pr"
        },
        {
          "url": "https://github.com/atomone-hub/atomone-sdk/pull/33",
          "title": "feat: add `x/epochs` module",
          "kind": "pr"
        },
        {
          "url": "https://github.com/atomone-hub/atomone-sdk/pull/44",
          "title": "feat: use epoch time to the nakamoto bonus period",
          "kind": "pr"
        },
        {
          "url": "https://github.com/atomone-hub/atomone-sdk/pull/69",
          "title": "fix(x/gov): fix migration clearing deprecated (A-31)",
          "kind": "pr"
        },
        {
          "url": "https://github.com/atomone-hub/atomone-sdk/pull/83",
          "title": "fix(x/staking): update existing validator commissions when commission params change",
          "kind": "pr"
        }
      ]
    },
    "exp.ignite.b4": {
      "sources": [
        {
          "url": "https://github.com/allinbits/vaas/pull/10",
          "title": "feat(x/provider): withdraw funds from consumer pool address at each block",
          "kind": "pr"
        },
        {
          "url": "https://github.com/allinbits/vaas/pull/16",
          "title": "feat: harden misbehaviour/double-vote validation and remove infraction_parameters from APIs",
          "kind": "pr"
        },
        {
          "url": "https://github.com/allinbits/vaas/pull/26",
          "title": "fix(ibc): address provider v2 review feedback and restore isolated devdeps",
          "kind": "pr"
        }
      ]
    },
    "exp.ignite.b5": {
      "sources": [
        {
          "url": "https://github.com/allinbits/gno-realms/pull/29",
          "title": "feat: add a memo argument to transfer functions",
          "kind": "pr"
        },
        {
          "url": "https://github.com/allinbits/gno-realms/pull/31",
          "title": "feat: add home render content for IBC core and transfer realms",
          "kind": "pr"
        },
        {
          "url": "https://github.com/allinbits/gno-realms/pull/34",
          "title": "feat(transfer): add MsgCall helpers for IBC voucher tokens",
          "kind": "pr"
        },
        {
          "url": "https://github.com/allinbits/gno-realms/pull/35",
          "title": "feat(core): restrict relayed IBC operations",
          "kind": "pr"
        }
      ]
    },
    "exp.interchain.b1": {
      "sources": [
        {
          "url": "https://github.com/cosmos/gaia/pull/1728",
          "title": "bug(app config): fix the wrong `bypass-min-fee-msg-types` key parse from the app config file",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1800",
          "title": "fix(export-genesis): fix export genesis command for missing values",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1881",
          "title": "fix(chore): fix gosec issues",
          "kind": "pr"
        }
      ],
      "note": {
        "en": "These PRs document fixes and maintenance. Broader upgrade responsibilities are owner-confirmed.",
        "pt": "Estes PRs documentam correções e manutenção. As responsabilidades mais amplas com upgrades foram confirmadas pelo autor."
      }
    },
    "exp.interchain.b2": {
      "sources": [
        {
          "url": "https://github.com/cosmos/gaia/pull/1738",
          "title": "feat(e2e): add e2e tests for the vesting module",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1775",
          "title": "feat(e2e): add e2e tests for the feegrant module",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1764",
          "title": "feat(e2e): add e2e tests for the slashing module",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1843",
          "title": "feat(e2e): manage ica from gov module",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1895",
          "title": "feat(e2e): manage ica from group module ",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1897",
          "title": "feat(x/ica): add tests for icamauth module",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1780",
          "title": "chore(e2e): remove queries as `IntegrationTestSuite` object",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1903",
          "title": "fix(CI): fix code coverage",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1789",
          "title": "feat(e2e): add encode and decode tests",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1749",
          "title": "refactor(e2e): small improvements to the e2e tests",
          "kind": "pr"
        },
        {
          "url": "https://github.com/cosmos/gaia/pull/1907",
          "title": "feat(CI): skip run the go CI test for markdown/docs files",
          "kind": "pr"
        }
      ]
    },
    "exp.ignite2.b1": {
      "sources": [
        {
          "url": "https://github.com/tendermint/spn/pull/169",
          "title": "feat(account): initialize the coordinator struct",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/235",
          "title": "feat(launch): allow to settle requests",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/304",
          "title": "feat(campaign): allows to allocate shares for mainnet accounts",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/330",
          "title": "feat(campaign): allows to redeem vouchers",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/488",
          "title": "feat(reward): Implement `DistributeRewards` method",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/190",
          "title": "feat(profile): init the validator structure",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/216",
          "title": "feat(launch): request to remove a genesis validator",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/222",
          "title": "feat(launch): request a vested account",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/224",
          "title": "feat(launch): filter accounts and validator list by chain ID flag",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/298",
          "title": "feat(campaign): initialize mainnet account",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/324",
          "title": "feat(launch): prevent account request if the chain is a mainnet",
          "kind": "pr"
        }
      ]
    },
    "exp.ignite2.b2": {
      "sources": [
        {
          "url": "https://github.com/ignite/cli/pull/1343",
          "title": "feat(module): bandchain oracle support",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/1731",
          "title": "feat(template): scaffold simulation testing templates with `simapp`",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/1774",
          "title": "feat(network): add `network join` command",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/1868",
          "title": "feat(network): add chain launch command",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/1899",
          "title": "feat(simapp): add `chain simulate` command",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/2401",
          "title": "feat(cmd/network): implement `client create` cmd",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/2263",
          "title": "feat(network): update SPN and SDK version",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/1495",
          "title": "feat(component): provide custom type for field ",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/1716",
          "title": "feat(module): scaffold parameters for a module",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/1288",
          "title": "fix: solve the race condition for the clispinner",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/1368",
          "title": "fix(pkg/ctxreader): Fix the data race after the context timeout",
          "kind": "pr"
        }
      ]
    },
    "exp.hermez.b1": {
      "sources": [
        {
          "url": "https://github.com/hermeznetwork/hermez-node/pull/799",
          "title": "TxSelector Refactor",
          "kind": "pr"
        }
      ]
    },
    "exp.hermez.b2": {
      "sources": [
        {
          "url": "https://github.com/hermeznetwork/hermez-integration/pull/1",
          "title": "first implementation",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-integration/pull/2",
          "title": "fix bjj endianness",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-integration/pull/3",
          "title": "add other transfers type",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-integration/pull/5",
          "title": "fix eth address generation",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-integration/pull/7",
          "title": "adding more examples",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-integration/pull/10",
          "title": "create wallet authentication signature",
          "kind": "pr"
        }
      ]
    },
    "exp.hermez.b3": {
      "sources": [],
      "note": {
        "en": "Owner-confirmed work; no specific public PR identified for this statement.",
        "pt": "Trabalho confirmado pelo autor; nenhum PR público específico identificado para este item."
      }
    },
    "exp.trustwallet.b1": {
      "sources": [
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/803",
          "title": "Add vechain stake api",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/801",
          "title": "Add ontology stake api",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/797",
          "title": "[Tezos] Fix delegation and add delegations tx history",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/787",
          "title": "[BNB] Multiple Addresses Tx",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/742",
          "title": "add coin info for markets",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/698",
          "title": "fix BTC Blockbook parser",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/636",
          "title": "Fix cosmos transaction history ",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/607",
          "title": "fix bnb block parser",
          "kind": "pr"
        }
      ],
      "note": {
        "en": "These PRs document implementation work; they do not establish the leadership scope.",
        "pt": "Estes PRs documentam a implementação; não comprovam o escopo de liderança."
      }
    },
    "exp.trustwallet.b2": {
      "sources": [
        {
          "url": "https://github.com/prazd/redemption/commit/8a4e8bf3dd686b2ffa2ed4d480c32cc6a9725198",
          "title": "Go Backend (#3)",
          "kind": "commit"
        }
      ]
    },
    "exp.trustwallet.b3": {
      "sources": [
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/891",
          "title": "Add support for rpc batch call",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/892",
          "title": "Add rpc batch call for zilliqa block",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/372",
          "title": "Send http metrics to Prometheus",
          "kind": "pr"
        }
      ],
      "note": {
        "en": "References cover RPC batching and metrics. Full-node operations are owner-confirmed.",
        "pt": "As referências cobrem RPC em lote e métricas. A operação de full nodes foi confirmada pelo autor."
      }
    },
    "exp.trustwallet.b5": {
      "sources": [
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/283",
          "title": "Add transaction webhook support for xpub addresses",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/426",
          "title": "Create cache middleware",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/451",
          "title": "Change Redis to Postgres",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/518",
          "title": "market/rates worker",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/641",
          "title": "fix btc block memory leak",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/771",
          "title": "fix cosmos race condition",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/795",
          "title": "fix observer race condition",
          "kind": "pr"
        },
        {
          "url": "https://github.com/trustwallet/blockatlas/pull/883",
          "title": "fix Zilliqa block request and data race",
          "kind": "pr"
        }
      ]
    },
    "exp.ignite.b6": {
      "sources": [
        {
          "url": "https://github.com/ignite/cli/pull/4091",
          "title": "fix: race conditions in the plugin logic",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/4889",
          "title": "fix: plugin data race",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/4910",
          "title": "fix(protoanalysis): resolve qualified and nested RPC request messages",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/cli/pull/4869",
          "title": "feat(pkg/httpstatuschecker): allow custom `http.Client`",
          "kind": "pr"
        }
      ]
    },
    "exp.hermez.b4": {
      "sources": [
        {
          "url": "https://github.com/hermeznetwork/hermez-node/pull/611",
          "title": "Synchronize the AccountCreationAuths from L1CoordinatorTxs",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-node/pull/636",
          "title": "instrumenting the application",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-node/pull/653",
          "title": "Generating automatically releases with Goreleaser",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-node/pull/708",
          "title": "fix the setType method to avoid invalid tx in the tx pool",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-node/pull/713",
          "title": "add race condition detector to the unit tests",
          "kind": "pr"
        },
        {
          "url": "https://github.com/hermeznetwork/hermez-node/pull/723",
          "title": "Automatically fetch the smart contract addresses from the Rollup contract",
          "kind": "pr"
        }
      ]
    },
    "opensource.defillama": {
      "sources": [
        {
          "url": "https://github.com/DefiLlama/DefiLlama-Adapters/pull/21478",
          "title": "Replace SuperRare subgraph with on-chain Rarity Pool balances",
          "kind": "pr"
        },
        {
          "url": "https://github.com/DefiLlama/DefiLlama-Adapters/pull/21479",
          "title": "Fix Rumpel Fluid position discovery to avoid full-factory scans",
          "kind": "pr"
        }
      ]
    },
    "exp.ignite.b7": {
      "sources": [
        {
          "url": "https://github.com/ignite/modules/pull/77",
          "title": "feat: airdrop start",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/modules/pull/81",
          "title": "feat: register staking and gov hooks",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/modules/pull/82",
          "title": "feat: add claim record mission invariant",
          "kind": "pr"
        },
        {
          "url": "https://github.com/ignite/modules/pull/87",
          "title": "feat(sim): add sim tests",
          "kind": "pr"
        }
      ]
    },
    "exp.ignite2.b3": {
      "sources": [
        {
          "url": "https://github.com/tendermint/spn/pull/248",
          "title": "feat(x/launch/keeper): verify and validate all request contents",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/315",
          "title": "feat(invariants): add module invariants",
          "kind": "pr"
        },
        {
          "url": "https://github.com/tendermint/spn/pull/332",
          "title": "feat(campaign): add shares invariant",
          "kind": "pr"
        }
      ]
    },
    "personal.mcp": {
      "sources": [
        {
          "url": "https://github.com/Pantani/tdmcp/pull/100",
          "title": "feat(rag): cross-RAG ranking via Reciprocal Rank Fusion (opt-in)",
          "kind": "pr"
        },
        {
          "url": "https://github.com/Pantani/tdmcp/pull/143",
          "title": "fix: enforce raw-off across code-bearing routes",
          "kind": "pr"
        },
        {
          "url": "https://github.com/Pantani/tdmcp/pull/150",
          "title": "fix: expose operator snapshot provenance",
          "kind": "pr"
        },
        {
          "url": "https://github.com/Pantani/ableton-mind/pull/11",
          "title": "Handle Glama startup without a local Ableton bridge",
          "kind": "pr"
        }
      ]
    },
    "personal.go": {
      "sources": [
        {
          "url": "https://github.com/Pantani/healthcheck/pull/1",
          "title": "feat: modernize healthcheck runtime",
          "kind": "pr"
        },
        {
          "url": "https://github.com/Pantani/chainops/pull/1",
          "title": "Refine safety checks and add coverage across core pipelines",
          "kind": "pr"
        },
        {
          "url": "https://github.com/Pantani/chainops/pull/2",
          "title": "Harden registry, validation, and path handling across the project",
          "kind": "pr"
        }
      ]
    },
    "personal.blockchain": {
      "sources": [
        {
          "url": "https://github.com/Pantani/cartographer/pull/2",
          "title": "Add local XCM Chopsticks orchestration",
          "kind": "pr"
        },
        {
          "url": "https://github.com/Pantani/cartographer/pull/3",
          "title": "feat: implement Cartographer next steps",
          "kind": "pr"
        },
        {
          "url": "https://github.com/Pantani/pool-party/pull/1",
          "title": "feat: modernize crypto derivation and CI",
          "kind": "pr"
        },
        {
          "url": "https://github.com/Pantani/pool-party/pull/2",
          "title": "Deprecate legacy BIP32 and harden BIP39 wordlists",
          "kind": "pr"
        }
      ]
    }
  }
};
