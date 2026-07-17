# ADR-103: Parity-surfaces ownership axis — per-entry `{value, reason, provenance}` classification adopting the ADR-102 grammar

**Status:** Accepted
**Date:** 2026-07-17
**Decision tier:** Architecture (Path A — direct operator/architect ruling in-thread; drafted plan-first under architect review, 2026-07-17; the lane never self-accepts, ADR-94)
**Related:** ADR-102 (the reusable `value/reason/provenance` declaration grammar this axis adopts verbatim — grammar defined there, ownership enum deferred to #316), ADR-28/36 (Layer-2 read-only, WARN-only posture the checker keeps), ADR-101 (hermetization — governs tree structure/naming, deliberately NOT the parity-schema semantics this extends), #316 (this decision's backlog task — root-files boundary declaration), #328 (the parity mechanism this enriches, designed in `docs/audits/2026-07-11-technical-fleet-parity-register.md §9`), #329 (VS Code ownership viz — a downstream VIEW mapping FROM these tokens), #337 (blocking-promotion, sequenced AFTER this enriched schema lands), the 2026-07-16 fleet structural census (`docs/audits/2026-07-16-technical-fleet-structure-census.md` — the classification source consumed, never redone)

## Context

`ecosystem/parity-surfaces.yaml` (the #328 fleet parity contract) records, per surface row, *what* the surface is (`kind`), *how* it is probed, and *what tier* it holds per repo. It does **not** record **why a surface is classified the way it is** — there is no machine-readable owner or rationale per entry. That is the exact residual #316 (the operator's "answers for everything, tracked" doctrine) exists to close: give every governed divergence its WHY.

ADR-102 anticipated this. It defined a **reusable declaration grammar** — `value` (mandatory, axis-specific scalar) · `reason` (mandatory, non-blank) · `provenance` (mandatory, non-empty list of `{kind, repo, ref}`) — used first by the `gate_rev_ahead` axis, and **explicitly stopped at the grammar**, deferring the ownership category enumeration to #316 (ADR-102 Decision 5; manifest header L73-74). This ADR is that enumeration.

## Decision

**Add a per-entry `ownership` axis to `ecosystem/parity-surfaces.yaml`, adopting the ADR-102 declaration grammar verbatim, classifying every surface row as `{methodology-generic | project | conditional}` with a mandatory reason and mandatory structured provenance.** The checker consumes it read-only/WARN-only.

1. **Grammar — adopted verbatim from ADR-102, no fork.** Every `ownership` block is the ADR-102 wrapper: `value` (mandatory scalar) · `reason` (mandatory, non-blank) · `provenance` (mandatory, non-empty list; each item `{kind, repo, ref}`, all three non-blank strings). Both axes route their reason+provenance validation through **one shared predicate** in `scripts/fleet_parity.py` (`_declaration_bad`, itself built on `_nonblank`) — the grammar is structurally incapable of forking, and a test asserts byte-compatibility across the two axes.

2. **Shape — a single per-row wrapper, not a repo-id-keyed map.** Ownership is a property of the *entry itself*: it is **hub-authoritative** and does not vary by consumer repo (contrast `gate_rev_ahead`, which is repo-id-keyed because a gate can be legitimately ahead in one consumer and not another). So `ownership` is one block per surface row, keyed by nothing.

3. **Category enum — `{methodology-generic | project | conditional}`, reconciled explicitly.** Three phrasings existed across sources: the #316 body and the 2026-07-16 census say `{methodology-generic | project | conditional}`; ADR-102's Decision-5 grammar-aside wrote a bare `{methodology | project | conditional}`; #329 renders `{methodology | repo-local | ignored}`. **The two named contract sources (#316 + census) govern.** ADR-102's bare `methodology` was a grammar-only illustration — ADR-102 was deliberately scope-guarded to grammar and could not decide the vocabulary, so it is **non-normative** for the enum. #329's set is a downstream **VIEW** that maps FROM these tokens (its concern, out of this axis's scope). Semantics:
   - **`methodology-generic`** — the methodology corpus every fleet repo carries; ownership is hub-authoritative (canonical living docs, floor, protocols, hub methodology dirs, hooks/commands/rosters, hermetization rules, methodology-shipped root config).
   - **`project`** — repo-local product/domain surfaces the methodology never owns (a consumer's data/eval/model/output/inbox/transcript/asset trees).
   - **`conditional`** — present-if-applicable / toolchain-derived surfaces whose presence depends on a repo's stack rather than a methodology mandate (cache-ignore effects, optional tooling configs, conditional source layouts).

4. **`value` is an enum-constrained axis-specific scalar — this is not a grammar fork.** ADR-102's grammar specifies `value` as an "axis-specific scalar"; the ownership axis's scalar domain is the closed three-token enum (the loader refuses a `value` outside it). `gate_rev_ahead`'s scalar was a free-form `gate_tag`. Same wrapper grammar, different value domain — exactly ADR-102's "shared grammar, separate axes."

5. **Provenance `kind` vocabulary.** The doctrinal-source kinds are **`backlog | audit | adr`** (an ownership classification rests on a charter ticket, a census/design audit, and this ADR). The `git-tag`/`git-commit` kinds ADR-102 introduced remain valid where an entry genuinely rests on a git object. `kind` stays an **open enum in code** — the loader validates `_nonblank` only, never a hardcoded set (per ADR-102; a closed kind-enum is not decision-worthy here).

6. **Mandatory on every surface row.** Unlike the optional `gate_rev_ahead` (present only on `precommit_remote` MUST rows), `ownership` is **required on every row**: the loader REFUSES a row with a missing or malformed `ownership` block (row skipped — refused, never guessed). This realizes the doctrine's "every governed entry carries a machine-readable reason." Consequence: the manifest may never be partially classified on `main` — the enrichment lands atomically, zero refusals.

7. **Posture — read-only, WARN-only; blocking-promotion is #337, sequenced after.** The checker keeps its ADR-28/36 Layer-2 posture: a completed run always exits 0, this axis adds no blocking gate. Refusals and any future ownership findings are REPORT labels. Promoting `fleet_parity` to a blocking `ALL_CHECKS` member is #337's job, explicitly sequenced to land **after** this enriched schema (architect re-sequence 2026-07-17), on top of a zero-WARN steady state.

8. **#329 consumption surface.** #329 (the VS Code ownership viz) reads the `fleet_parity` **summary / ownership-tally line** — the management surface ADR-102 Decision 3 already named for #316/#329 — not the raw YAML. This ADR adds an ownership tally to that surface (`ownership: N methodology-generic, N project, N conditional`). #329 maps those tokens to its own render enum; that mapping is #329's concern.

## Why a successor ADR (not an ADR-102 amendment)

ADR-102 is Accepted and immutable (CLAUDE.md §5 item 3; the `block_immutable_edits` PreToolUse guard). More to the point, ADR-102 established the governing precedent for exactly this schema family: *"a durable schema concept that #316 will build on is decision-worthy in its own right → a successor ADR, not an [in-file] amendment."* The ownership enum is that durable concept. It gets its own ADR, adopting ADR-102's grammar by reference.

## Consequences

- Every parity surface now carries a hub-authoritative, provenance-cited ownership classification — the "answers for everything, tracked" residual for the root/file-set boundary closes with a machine-readable reason per entry.
- The mandatory-classification invariant means adding a future surface row requires classifying it (or the loader refuses it) — ownership can no longer silently drift in.
- The checker stays Layer-2 read-only, WARN-only (exit 0 always; exit 2 only on an unusable manifest / bad `--run-date`); this axis adds no blocking gate. #337 carries the blocking promotion.
- The shared `_declaration_bad` predicate makes the ADR-102 ↔ ADR-103 grammar provably non-forking (a regression that diverged one axis's grammar would fail the cross-axis test).

## Ratification

Landed **Accepted in-arc** (skipping the Proposed interim) per architect ruling 2026-07-17: all recorded decisions (posture, scope, doc-home, enum) were operator/architect-ruled in the authoring thread, and the terra `/codex-review` lane reviews the diff pre-merge. Index row added to `docs/decisions/README.md` with no `**Proposed** —` prefix.
