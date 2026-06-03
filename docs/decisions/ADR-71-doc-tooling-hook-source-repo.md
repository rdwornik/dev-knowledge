<!-- scope: meta -->

# ADR-71 — Doc-tooling distribution via the pre-commit hook source repo pattern

**Status:** Accepted — 2026-06-03 (operator-confirmed). **Consumption contract VALIDATED** via the corp-monorepo TOC pilot (2026-06-03): consume (`repo:/rev:` from the hub at pinned `69558c7`, relative doc path resolved inside the cloned hook repo), regenerate (`toc-generate`), and gate (`toc-freshness` fails-stale / passes-fresh) all confirmed end-to-end. **Codemap deployment is NOT validated** — gated on the layout finding below (see "Codemap layout finding").
**Records:** the distribution vehicle for fleet-wide codemap + TOC, grounded in `docs/audits/2026-06-03-doc-tooling-inventory.md`.
**Related:** ADR-51 (codemap mandatory for M/L; ARCHITECTURE convention; TOC amendment), ADR-28 (three-layer model — Layer 2 never executes in child repos), ADR-69 (cross-repo read-only contract), ADR-59 (root-hygiene — entry-scripts live in `scripts/`), BACKLOG #9 (cross-repo universalization).

## Context

The 2026-06-03 doc-tooling inventory established the ground truth: the codemap and TOC generators (`scripts/codemap/`, `scripts/toc/`) live in **exactly one repo — the `.dev-knowledge` hub**. The three children that show a codemap (`ai-council`, `corp-monorepo`, `corp-ops`) carry hub-generated mermaid between `<!-- CODEMAP:START/END -->` markers but **no generator and no freshness gate** — frozen, hand-maintained snapshots that silently drift from their source trees; `corp-sca-time-automation` has no codemap at all. There is **no existing distribution** of the generators (no copies to single-source; `repo`-grep across children found no invocation of the hub tooling).

Before any rollout, the tooling must be made **consumable** — installable into a child repo, single-sourced (one canonical generator, not N copies), and version-pinned so the deployed copies cannot drift. The open question was the distribution vehicle.

## Decision

**Distribute doc-tooling fleet-wide via the pre-commit *hook source repo* pattern** — the industry standard for sharing custom hooks across internal repos (e.g. Olist `hulks`).

- **The hub is the hook source.** `.dev-knowledge` ships a root `.pre-commit-hooks.yaml` defining four hooks: `codemap-freshness` (check, default stage), `codemap-generate` (manual stage, writes), `toc-freshness` (check), `toc-generate` (manual stage, writes). Child repos consume them via a `repo: <ref> rev: <tag> hooks: [...]` stanza in their own `.pre-commit-config.yaml` — single-source, version-pinned by `rev`, no copy-drift.
- **`language: script` thin wrappers, not a pip package.** The generators are pure-stdlib (argparse/ast/difflib/re/pathlib), so pre-commit's venv isolation buys nothing. Two thin shims in `scripts/` (`scripts/codemap_hook.py`, `scripts/toc_hook.py`) put the package dir on `sys.path` (relative to `__file__`, so it resolves inside the *cloned* hook repo) and delegate to the real CLI `main()`. This keeps `pyproject.toml` untouched, preserves this Layer-2 repo's "never executes / not a distributable package" identity, and is minimal-diff. Per ADR-59 root-hygiene the wrappers live in `scripts/`, not a new root folder. The wrappers delegate — they do **not** re-implement any check logic, so the check registry stays single-source.
- **Local-path reachability now, URL-swappable later.** The fleet is co-located on one machine, so consumers reference the hub by **local filesystem path**. The same `.pre-commit-hooks.yaml` works unchanged if the hub is later referenced by a git URL — only the consumer's `repo:` value changes.
- **Generation stays local in each repo.** The hook runs *inside the consumer*: it reads the consumer's own source tree and writes the consumer's own `ARCHITECTURE.md` / doc. **The hub never writes a sibling repo** — honoring ADR-28 (Layer 2 never executes/mutates a child) and ADR-69 (read-only cross-repo contract). The hub distributes the *tool*; each repo runs it against itself.

## Consequences

- **Positive:** the generator lives in exactly one place; consumers pin a `rev` so deployed behavior cannot silently drift; a frozen child codemap becomes a live, gated one once the consumer adds the stanza + regenerates; the read-only/Layer-2 invariants stay structurally true (generation is local-to-consumer). No packaging burden, no new root folder.
- **Per-repo prerequisite:** the freshness gate is a *pre-commit* hook, so a consumer needs a `.pre-commit-config.yaml`. `corp-ops` and `corp-sca` have none — the pre-commit framework must be bootstrapped there before the gate can land (sequenced in the rollout).
- **Versioning discipline:** consumers pin `rev` to a hub tag/commit; picking up a tooling change is a deliberate `rev` bump in each consumer (the single-source-after-deploy lever — analogous to the `tier1-lifecycle` plugin's version-keyed cache dance, but git-native here).
- **Windows execution note:** `language: script` execs the `.py` wrapper directly; the wrappers carry a `#!/usr/bin/env python3` shebang. The fleet is single-machine, so `pre-commit try-repo` on that machine is the authoritative cross-platform check.

## Operating / propagation model

The corp-monorepo pilot clarified *how a hub tooling change actually reaches a consumer* — the part most at risk of being lost. Recorded plainly:

- **Propagation is consumer-PULL, not source-push.** pre-commit caches hooks by resolved `rev`; **no** version model gives zero-touch propagation. Whether a consumer pins a `rev` or floats `main`, adopting a hub tooling change is always a *deliberate per-repo action* — a `rev` bump or a `pre-commit autoupdate`. There is no configuration in which editing the hub silently updates a sibling.
- **True central-push is structurally forbidden.** A model where one hub action updates all repos would require the hub to **WRITE into siblings** — which violates the Layer-2 invariant (ADR-28/ADR-69: validators are read-only, the hub never writes a sibling; and generation *must* be local because a codemap is generated from the repo's own source tree). Rejected for that reason.
- **Chosen model: pinned-pull.** Consumers pin `rev` to a stable hub commit/tag; per-repo wiring is a **one-time** setup; ongoing updates are an occasional one-command pull. Floating-ref (loses pinning stability) and a central fleet-writer (breaks Layer-2) were both considered and rejected.

## Codemap layout finding

The pilot's most valuable output — it splits the rollout in two:

- **The hub codemap generator is layout-coupled.** On a single-package-under-`src/` layout it degrades silently. In corp-monorepo (`corp.`-prefixed imports), the edge-matcher keys on the first dotted component `corp`, which ≠ the bare package names, so it finds **0 edges**; the dotted `tach.toml` keys likewise don't match the bare nodes, so it assigns **0 layer colors**. The result is a strictly-worse orphan graph (verified read-only against corp: **13 orphan nodes / 0 edges / 0 layers** vs. the curated **10 / 15 / 4**).
- corp-monorepo therefore **deliberately hand-authors its codemap** per an ADR-51 amendment (carries a `not generator-managed` marker).
- **Conclusion: TOC universalizes cleanly (layout-agnostic); codemap does NOT.** Codemap rollout is gated on:
  - **(a) per-repo grounding** — for each repo, is the "frozen" codemap *hand-authored-deliberate* or *stale generator output*, and is its layout *generator-compatible*?
  - **(b) a generator decision** — fix the generator (handle prefixed imports + dotted keys) vs. a marker-aware freshness gate (respect `not generator-managed` blocks).
- Blanket regeneration would **destroy curated diagrams fleet-wide** — hence the gate. Tracked as BACKLOG #79.

## Alternatives considered

- **Pip package (`language: python`)** — rejected: turns the knowledge-base repo into a distributable package (build-system + `[project]` + console_scripts) for zero benefit, since the tools have no third-party deps; heavier diff; conflicts with the Layer-2 "not a distributable package" posture.
- **Per-repo copy of the generator** — rejected: re-introduces exactly the copy-drift the inventory found (frozen, ungated codemaps) and the drift ADR-69 exists to prevent; duplicates the generator into every child.
- **`tier1-lifecycle`-style CC plugin** — not taken: a CC plugin cannot ship a `.pre-commit-config.yaml` (the ruff gate proves this — it ships as an asset merged by hand), and freshness is fundamentally a pre-commit-stage concern. The hook source repo pattern is the native fit; the plugin remains the right vehicle for the lifecycle/closure hooks it already carries.

## References

- `docs/audits/2026-06-03-doc-tooling-inventory.md` (the grounding: generators live only in the hub; deploy-fresh, not single-source)
- `scripts/codemap/` (`cli.py`, `check.py`, `generator.py`), `scripts/toc/` (the canonical generators), `scripts/codemap_hook.py` + `scripts/toc_hook.py` (the wrappers), `.pre-commit-hooks.yaml` (the four exposed hooks)
- `docs/decisions/ADR-51-*.md` (codemap/TOC convention), `ADR-28-three-layer-architecture.md`, `ADR-69-cross-repo-audit-reach-model.md`, `ADR-59` (root-hygiene)
- BACKLOG #9 (cross-repo universalization), #78 (deferred consolidated docs-refresh pass)
