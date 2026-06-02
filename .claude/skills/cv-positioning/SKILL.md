---
name: cv-positioning
description: How to position content on Danilo Pantani's HTML CV (index.html) — keep it protocol-first (Staff Blockchain Protocol Engineer · Go · Cosmos SDK · IBC) while placing new projects as range/curiosity without diluting the headline. Use when deciding WHERE a project, skill, or claim belongs, when writing or rewording CV copy, when adding a side project, or when reviewing whether the CV still reads protocol-first. Also covers the "no fabricated metrics" rule.
---

# cv-positioning — Protocol-first identity, curiosity on display

## The canonical identity (never dilute)

The role string is **"Staff Blockchain Protocol Engineer · Go · Cosmos SDK · IBC"**. Lead with the rare protocol/Go signal (Cosmos SDK, Ignite, IBC, ADR-004, validator infra). Full-stack (TypeScript/React), DevOps, and AI/creative work are **range** — proof he can own a feature end-to-end — never co-equal with protocol in the H1, title, hero, or Core Expertise protocol bullets.

Why: the site once drifted to a diluted "Senior Backend, Full-Stack & Blockchain" hybrid that buried the rare signal. The owner deliberately sharpened it back. Protect that.

## The analytical lens (read AND place through this persona)

Read the CV as its subject actually is: someone **genuinely curious — drawn to new things, to technology, and to art made with technology** (creative coding, generative / audio-reactive visuals, the MCP-era AI frontier) — **whose center of gravity is unmistakably Go + Web3 / blockchain protocol engineering**.

Two failure modes, both bad:

- **Dilution** — curiosity signals climb into the headline and bury the protocol signal → reads as a generalist, loses the rare differentiator.
- **Flatness** — zero curiosity signal → reads as a narrow backend engineer, hides that he ships on the frontier and even makes art with code.

The win condition: a **protocol-first headline** plus a **visible, tasteful trail of curiosity** that a sharp reader notices and likes. The art/AI work earns its place by being real and frontier, not by shouting.

## Placement framework for any new project or claim

1. **Classify** it: protocol-core (Go/Cosmos/IBC/validator/tooling), range (full-stack/DevOps/AI-native), or curiosity/art-tech.
2. **Map to sections by tier:**
   - protocol-core → hero · Core Expertise · Open Source & Protocol Impact · Highlights · Selected Repositories · Tech Stack
   - range → Summary "range" clause · Tech Stack · Selected Repositories
   - curiosity/art-tech → **Selected Repositories** · **Tech Stack (sparingly)** · at most ONE reinforcing clause in an existing range/AI narrative. **Never** the H1, hero, Core Expertise protocol bullets, the protocol-impact list, or "What I'm looking for".
3. Apply the no-fabricated-metrics rule below.

## tdmcp — worked example

`tdmcp` = the TouchDesigner MCP server. Repo: https://github.com/Pantani/tdmcp (TypeScript). Live: https://pantani.github.io/tdmcp/ . Topics: mcp, model-context-protocol, creative-coding, generative-art, audio-reactive, glsl, vj, claude, cursor. ~102 tools across 3 layers, 629-operator knowledge base, MIDI/OSC/DMX, error self-check + preview loop.

- **Classify:** curiosity/art-tech **and** AI-native proof — he *builds* AI tooling (an MCP server), not just consumes it. This is the single strongest "frontier + art" signal on the CV.
- **Homes:**
  - **Selected Repositories** — add a `tdmcp` chip linking to `https://github.com/Pantani/tdmcp`. The repo intro currently says "across the Cosmos and Web3 ecosystem"; widen it minimally (e.g. add "…plus creative-tech experiments") so a TypeScript/art repo doesn't contradict the intro.
  - **Tech Stack** — add at most 1–2 restrained tags (e.g. `MCP`, and one of `TouchDesigner` / `Creative Coding`). Do not flood the cloud with art tags; that tips into dilution and risks print pagination.
  - **AI-native narrative** — optionally sharpen the existing "AI-native workflows … as a daily multiplier" to note he *authors* MCP tooling. One clause, protocol primacy intact.
- **Keep OUT of:** H1/hero, Core Expertise, Open Source & Protocol Impact, "What I'm looking for".

## No fabricated metrics (hard rule)

Never invent scale numbers — users, volume, downloads, stars, chain counts. tdmcp currently has ~0 stars: describe what it **is and does**, never imply traction or popularity. Verify any GitHub PR/contribution number with `gh search prs 'author:Pantani is:merged ...'` before changing it. Prefer vague-but-true ("maintainer-level contributor") over invented precision.
