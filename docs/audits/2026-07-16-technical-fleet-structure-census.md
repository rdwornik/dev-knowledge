# Fleet Structural Census & Governance-Coverage Report — hub · corp-monorepo · ai-council

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-16
- **Source-session:** operator-dictated OVERNIGHT read-only structural census (CC-primary, auto-mode; model `claude-opus-4-8[1m]`). Pre-arc `main` HEAD `ae6c7592`; working branch `docs/fleet-structure-census`. Evidence basis: 3 parallel read-only tree-walk subagents (one per repo, haiku) + 1 checker-code probe (sonnet) + orchestrator recon of `ecosystem/parity-surfaces.yaml`, all three `.methodology.yaml`, `ADR-101`, `intake #12`, BACKLOG, and the 2026-07-11 fleet-parity register.
- **Status:** PROPOSAL-ONLY — §6 arcs are proposals for operator verb-ruling. **Zero mutations outside this one report**: no declaration added, no parity surface extended, no fix applied, no file moved/renamed/deleted in any of the three repos (core-invariant #3).

---

## 0. Headline — the premise has largely been overtaken by the last five days of work

The operator's standing ask is a **fleet-level structural comparison + a management system for repo structure**, with the working assumption that `.claude` layout, `.github`/`assets`/`config` presence, and root-entry naming are **ungoverned gaps** ("no mechanism sees it today"). That assumption was true when the recurring diff-by-eye lists were written. **It is now substantially false.** Between the 2026-07-11 fleet-parity register and this census (2026-07-16), three mechanisms landed that already *see* almost every surface the operator names:

1. **`ecosystem/parity-surfaces.yaml` v1.0.0** (the #328 versioned parity contract) — a machine-readable manifest of **~45 surfaces × role-tiers × one probe each**, consumed by `scripts/fleet_parity.py`. It already carries rows for `.claude` subtree ownership, `.github`, `assets`, `config`, root config files, the command roster, and an effect-probe for every tool cache.
2. **ADR-101 (Hermetization, Accepted 2026-07-11)** + `scripts/validate_hermetization.py` — a CLOSED sanctioned top-level set, a `docs/<genre>/` seal, a per-class audit-name grammar, and a **prospective pre-commit refusal gate**. This *is* the "root-entry naming/allowlist validator." It is **live and gating — at the hub only.**
3. **The enforcement-transfer mesh (epic S8)** — both consumers now run local twins of `canonical_freshness`, `validate-audit-casing`, `validate-backlog`, `floor-hash-verify`, plus hub-carried `backlog-id-on-close` + `block-ff-push` (pinned `v1.3.1`).

**So the real residual is not blindness — it is teeth and unattended execution.** The parity contract *sees* the fleet but (a) is **WARN-only**, (b) is surfaced **informationally at the ship-gate only** — never a gate input, never wired to a nightly/SessionStart run — and (c) the ADR-101 top-level seal is **hub-only**. The "management system" the operator wants (the intake #12 two-trees model + a nightly manifest walk → verdict sheet → morning prompt) is **designed and half-built, not running unattended.** Everything below is evidence for that one conclusion, plus the three narrow arcs that close it (§6), each mapped to an already-filed ticket so nothing is reinvented.

**One live WARN, one live gap, one unbuilt runtime** is the honest summary:
- **live WARN:** corp `precommit-hub-block` rev `v1.3.1` vs corpus `v1.2.0` split (MUST/non-waivable, undeclarable) — [#336].
- **live gap (unenforced):** consumer top-level tree seal (ADR-101 Rule A is hub-only) — [#306] P6.
- **unbuilt runtime:** the nightly parity walk + verdict sheet — [#324] charter, and the blocking promotion [#337]→gated-on-[#336].

---

## 1. Full root-level tree comparison (presence matrix)

Legend: `✓` tracked-present · `·` absent · `ig` present-on-disk-but-gitignored. "gov" cites the governing `parity-surfaces.yaml` row / ruling.

### 1A. Root files (depth-0 tracked)

| file | hub | corp | ai | gov / note |
|---|---|---|---|---|
| VISION.md · ARCHITECTURE.md · CLAUDE.md · CONTRIBUTING.md · JOURNAL.md · LESSONS.md · BACKLOG.md | ✓ | ✓ | ✓ | 7 canonical docs — `canonical-doc-*` MUST (hub+consumer) |
| INSTALL.md | · | ✓ | ✓ | `install-md` — consumer MUST / **hub INVERSE** (correct: hub absent) |
| .methodology.yaml | ✓ | ✓ | ✓ | `methodology-yaml` MUST (hub added 2026-07-13, ADR-101 §9a amendment) |
| .gitignore · .gitattributes · pyproject.toml | ✓ | ✓ | ✓ | `root-gitignore`/`root-gitattributes`/`root-pyproject` MUST |
| .pre-commit-config.yaml | ✓ | ✓ | ✓ | `root-precommit-config` MUST |
| `<repo>.code-workspace` | ✓ | ✓ | ✓ | `root-code-workspace` MUST (glob `*.code-workspace`) |
| .pre-commit-hooks.yaml | ✓ | · | · | `hub-precommit-hooks-export` — hub-only MUST (hook exporter) |
| .worktreeinclude | ✓ | · | · | hub-LOCAL, declared in hub `.methodology.yaml` |
| package.json · package-lock.json | ✓ | · | · | hub-LOCAL (Pyright oracle node scaffold), declared |
| tach.toml | · | ✓ | · | `tach-toml` — corp SHOULD (monorepo-size) |

**Inverse rules all hold:** hub correctly lacks `INSTALL.md` and `src/`; both consumers correctly lack `docs/handoffs/`. No inverse violation anywhere.

### 1B. Root folders (depth-0)

| folder | hub | corp | ai | gov / note |
|---|---|---|---|---|
| .claude | ✓ | ✓ | ✓ | MUST (+ floor set in consumers) |
| docs | ✓ | ✓ | ✓ | genre folders — `docs-genre-*` MUST |
| scripts · tests · config | ✓ | ✓ | ✓ | `shape-dir-*` MUST (shape only; contents role-dependent) |
| logs | ✓ | ig | ig | `shape-dir-logs` MUST; hub tracks `logs/TOKEN-LOG.md`, consumers ignore whole dir |
| protocols | ✓ | ✓ | ✓ | `protocols-dir` SHOULD — **now carried in all three** (corp gap #314 closed to a genre-shell) |
| src | · | ✓ | ✓ | `src-dir` — hub **INVERSE** / consumer LOCAL |
| .vscode | ✓ | ✓ | ✓ | OPEN ruling e1 — **now declared in all three (2026-07-16 ARC-B)** |
| .github | · | ✓ | · | `github-ci` — corp LOCAL (declared `github-ci-local`) |
| assets | · | · | ✓ | `ai-local-assets` — ai LOCAL (declared) |
| .claude-plugin · codex | ✓ | · | · | hub-LOCAL (marketplace root / Codex config source), declared |
| deploy · ecosystem · plugins · templates | ✓ | · | · | `hub-*-dir` — hub-only MUST (source-role) |
| eval · models | · | ✓ | · | `corp-local-eval`/`corp-local-models` — corp LOCAL (declared_by intake-12) |
| output | · | ✓ | ✓ | `local-output-dir` — corp+ai LOCAL |
| data | · | ✓ | · | `corp-local-data` — corp LOCAL |
| council_inbox | · | · | ✓ | `ai-local-council-inbox` — ai LOCAL |

**docs/ genre folders present:** hub = `archive audits decisions handoffs intake runbooks` (all 6); corp = `archive audits decisions intake`; ai = `archive audits decisions intake`. Both consumers correctly omit `handoffs/` (inverse) and `runbooks/` (hub-only today).

### 1C. `.claude/` internal layout (the operator's named "compare INTERNAL layout")

| `.claude/` subtree | hub | corp | ai | ownership (`claude-subtree-ownership` row) |
|---|---|---|---|---|
| commands/ | ✓ (4) | ✓ (1) | ✓ (1) | **SHARED** — all repos; hub={changelog-review, handoff, override, save}, consumers={override} |
| skills/ | ✓ (check-against-spec, verify) | ✓ (gotchas) | **·** | owned: hub, corp — **ai absent = the #308 half-adoption gap** |
| rules/ | ✓ (git-discipline) | · | ✓ (code-standards, python-env, testing) | owned: hub, ai |
| workflows/ | ✓ (conformance-hub.js) | ✓ (conformance-corp.js) | · | owned: hub, corp |
| agents/ | ✓ (artifact-reader) | · | · | owned: hub |
| generated/ | ✓ (commands-repo, recent-adrs) | · | · | owned: hub |
| hooks/ | · | · | · | owned: hub (declared, none present) |
| CLAUDE-FLOOR.md (+ .sha256, check_floor_hash.py) | · (hub=origin) | ✓ | ✓ | `claude-floor-*` consumer MUST |
| settings.json | ✓ | ✓ | ✓ | hook-block rows (`settings-*`) |
| settings.local.json | ig | ig | · | gitignored per-machine (ai simply hasn't one) |
| methodology-roster.md | ✓ | · | · | hub-only generated |

**Command roster** is closed by `claude-commands-roster` (expected_all `override.md`; expected_repo hub `handoff/save/changelog-review`) — all three conform.

### 1D. `.github` / `.vscode` / `assets` / `config` (the operator's named presence set)

| dir | hub | corp | ai | disposition |
|---|---|---|---|---|
| .github | · | ✓ (workflows: `nightly-conformance-triage.yml`, `tach.yml`) | · | GOVERNED — `github-ci` corp LOCAL, declared `github-ci-local` |
| .vscode | ✓ (settings.json) | ✓ (settings.json) | ✓ (settings.json) | GOVERNED-as-of-today — declared `.vscode` in all three (2026-07-16), OPEN e1 ruling on template-membership |
| assets | · | · | ✓ (`ruff-pre-commit.yaml`) | GOVERNED — `ai-local-assets` LOCAL, declared |
| config | ✓ (requirements-dev.txt) | ✓ (product config tree) | ✓ (python package) | GOVERNED-as-shape — `shape-dir-config` MUST; **contents diverge wildly by role, and the row is `dir_exists` only** |

### 1E. Tool caches — gitignore consistency (NOT presence, per the arc)

**All caches are AT-PARITY: every one is gitignored in all three repos.**

| cache | hub | corp | ai | probe (`ignore-*` Tier-4 row) |
|---|---|---|---|---|
| .venv/ · __pycache__/ · .pytest_cache/ · .ruff_cache/ · .mypy_cache/ | ig | ig | ig | `check_ignore` effect-probe — PASS all |
| .hypothesis/ | ig | ig | ig | `ignore-hypothesis` — **register e2 "hub+ai lack the line" is RESOLVED; all three now carry it** |
| *.egg-info/ | ig | ig | ig | `ignore-egg-info` — PASS all |
| node_modules/ | ig | · (n/a) | · (n/a) | `ignore-node-modules` hub-only tooling (AT-PARITY, register e5) |

This is the cleanest axis in the fleet: the effect-probe (`git check-ignore`, never text-grep — FR-6) returns PASS on every cache × repo.

---

## 2. Divergence classification — (a) GOVERNED · (b) LEGITIMATE-BUT-UNDECLARED · (c) UNGOVERNED GAP

The striking result: **after the 2026-07-16 ARC-A/ARC-B declaration passes, category (b) is nearly empty and category (c) is about teeth/runtime, not blindness.**

### (a) GOVERNED — an existing parity row or a live declaration

Every one of these has a `parity-surfaces.yaml` row **and/or** a `.methodology.yaml` declaration, so it reads as intentional, not drift:

- **Structural presence/absence** — INSTALL.md, src/, docs/handoffs/ (all via inverse rows); .pre-commit-hooks.yaml / deploy / ecosystem / plugins / templates (hub-only MUSTs); tach.toml (corp SHOULD).
- **Hub-local root entries** — .claude-plugin, codex, .worktreeinclude, package.json, package-lock.json — declared in the hub's own `.methodology.yaml` (the §9a "hub is a fleet member" contract).
- **Product-local dirs** — corp `data/eval/models/output/docs-diagrams`, ai `council_inbox/output/assets` — Tier-3 LOCAL `declared_by: intake-12`.
- **Behavioral divergences** — `ruff-gate` (all three run a pinned check-only gate, declared as a tombstone-join divergence in all three); `hub-codemap-hooks` (both consumers, hand-authored codemaps); `hub-toc-hooks` (corp, #326 ToC strip); `audit-casing-r4` corp UPPERCASE 11-name grandfather (declared enumerated skip-set).
- **`.claude` subtree ownership + command roster** — `claude-subtree-ownership` + `claude-commands-roster`.
- **Caches** — Tier-4 `ignore-*` effect-probes, all AT-PARITY.
- **`.vscode`** — as of 2026-07-16 ARC-B, declared in all three (short 2026-08-13 shelf-life to force the e1 revisit).
- **ai-council specifics** — `dep-pytest-xdist` (installed-but-unpinned, declared), `claude-md-section-11-title` (label-accuracy divergence, declared).

### (b) LEGITIMATE-BUT-UNDECLARED — product-specific, would benefit from a declaration or ruling

Almost nothing survives here — the declaration discipline is current. The two residuals are **absence/ruling** shaped, not "an undeclared divergence to record":

- **ai-council has no `.claude/skills/`** while hub and corp do. This is not a divergence to declare — it is the **#308 half-adoption gap** (the universal-`gotchas` + per-project-skill pattern is only half-realized; ai carries no project skill at all). Proposed disposition: rule it under #308 (adopt a minimal ai-council skills/ or accept-absent-with-reason).
- **`.vscode` template-membership** — all three now *track* `.vscode/settings.json`, declared-LOCAL as an interim. The open question "is `.vscode` a **carried fleet template** or a **per-repo local**?" (register e1) is genuinely undecided; the declarations are honest placeholders with a forcing 2026-08-13 shelf-life.

### (c) UNGOVERNED GAP — the honest residual is *unenforced* and *unattended*, not *unseen*

- **(c1) Consumer top-level tree seal is unenforced.** `validate_hermetization` Rule A (the sanctioned-Tier-1-set + `docs/<genre>/` seal) is **HUB-ONLY** by design (a verbatim carry would brick consumer dev under `src/`, `data/`, `council_inbox/`). A consumer session that adds an unsanctioned top-level dir or a mis-cased audit file is caught **only** by the casing branch (`validate-audit-casing`, which both carry) — the **tree-seal branch fires nowhere on a consumer**. `fleet_parity` would emit an *undeclared-deviation WARN* if it ran, but it neither gates nor runs unattended (see c2). → [#306] P6 rollout.
- **(c2) The parity contract has no teeth and no unattended run.** `fleet_parity` is surfaced **informationally at the ship-gate only** (`audit.py::_fleet_parity_surface`, `--no-write --no-events`, fail-open) and is **deliberately not an `ALL_CHECKS` member** (it would RED the gate on any WARN). There is **no `settings.json` SessionStart/Stop wiring and no nightly routine** — the intake #12 "nightly walk → verdict sheet → morning prompt" is unbuilt. So a governed surface is inspected only when a human ships the hub *and* reads the informational line (or remembers to run the `fleet_parity` CLI by hand) — there is **no unattended trigger**. → blocking promotion [#337] (gated on [#336]); nightly runtime [#324] charter.
- **(c3) Per-entry root-file *ownership* classification does not exist.** `parity-surfaces.yaml` encodes role-tiers (MUST/SHOULD/LOCAL/INVERSE) but **not** the `{methodology-generic | project | conditional}` ownership axis the operator's "management system" wants per root entry (the axis the VS Code color layer #329 would render). → [#316] filed, unbuilt.
- **(c4) Consumer canonical-doc *content* governance stops at presence + freshness.** The 7 canonical docs are presence-MUST rows; freshness is now enforced on consumers (local `canonical_freshness_gate.py`); but **no template-conformance or byte-match** governs their content beyond the floor fragment. This is largely by-design (a repo's VISION/ARCHITECTURE are legitimately its own) — the precise governed portion is the floor + CLAUDE.md `owner=hub` Form-A regions (#312), and formalizing that boundary at file-set granularity **is** [#316].

---

## 3. Coverage audit of parity-surfaces v1 — what the root-sweep ACTUALLY sweeps

> *Section 3 was adversarially second-derived against the live code by `codex exec -m gpt-5.6-sol` (2026-07-16, 36-point derivation). Its reconciliations — the generic **root-sweep** as a coverage mechanism, the `.vscode`/`assets` verdict corrections, and the `ruff-gate`-vs-`precommit-hub-block` fidelity split — are folded in below.*

**Mechanism (code-confirmed, `fleet_parity.py` read in full — ~1700 lines).** The checker is a **generic manifest-driven engine with almost no hardcoded surface list** (grep confirms no `PARITY_SURFACES`/`ROOT_FILES`/`SURFACES` table exists). It `load_manifest`s `ecosystem/parity-surfaces.yaml` (`fleet_parity.py:203`), cross-checks the `fleet:` block against `ecosystem/deployed-versions.yaml` (every registry key must appear, both directions — a mismatch is a refusal finding), then for each `surfaces[]` row evaluates its `probe` per repo against the row's `tier` token, applying the intake-#12 nightly decision tree to a verdict. **The manifest is the PRIMARY scope** — most coverage attributes to the *manifest* (507 lines, separately versioned/editable), not the code — **but not the whole of it:** four coverage mechanisms live in the code itself: the generic **root-sweep** (the anti-regress catch-all, `_eval_sweep` `:1249` — see 3A), the 3-stage `hooks-armed` install check (`:837`), the `ruff_config_form` evidence probe (`:543`), and the `dependency-baseline.yaml` leg (`:1278`). The one near-hardcoded content list, `_TIER4_TOP_NAMES` (`:1243`), only *relabels* an already-uncovered entry as `tracked-ephemera` vs generic WARN.

**Declared-divergence mechanism (two layers).** (a) manifest-native — **only** `declared_by: intake-12` directly converts a present LOCAL surface to **AT-PARITY** (the SETTLED template vouches; no live file needed, `:987`). The `declared_divergence` field annotates an *expected* per-repo MUST-difference but **still requires** a live `.methodology.yaml` declaration to pass (else WARN-undeclared, `:946`). (b) a live per-repo allowlist read from each target's own `.methodology.yaml` `sanctioned_divergences` (`ec.read_allowlist`, `:1659`), matched by **EXACT component-id equality** (`_match_declaration`, `:715` — a substring/prefix matches nothing) → **PASS-declared**. Waivers are **shelf-lived, not permanent**: a past `review_date`/`expiry` flips the finding to `advisory-rewarn` rather than clearing it; an allowlist entry matching no live manifest-row/dependency divergence may decorate `stale-declaration`. This is why the 2026-07-16 `.vscode` declarations carry a forcing 2026-08-13 shelf-life.

### 3A. What it sweeps (by probe kind)

| probe kind | what it asserts | surfaces covered |
|---|---|---|
| `path_tracked` / `dir_tracked` / `dir_exists` / `file_exists` / `glob_tracked` | git-tracked (or on-disk) presence of a named path | 7 canonical docs; docs genres; root config files; shape dirs (tests/scripts/logs/config); INSTALL/.methodology; hub-only dirs; Tier-3 LOCAL dirs; floor files |
| `file_contains` (doc-marker) | a required token exists in a file | floor `@import`; CLAUDE.md Form-A `<!-- methodology:start`; BACKLOG `## [E` story-map schema |
| `settings_hook` / `plugin_enabled` / `settings_local_blocks` | a hook block / plugin is present in `settings.json`; local hook commands match an owned allowlist | floor-guard, precommit-arm, stop-backpressure, tier1 plugin, local hook blocks |
| `precommit_remote` — **full fidelity** | the hub block pins the deployed **tag** (rev == source_tag), the tag exists/has ancestry, AND required hook ids are present | `precommit-hub-block` (rev + `backlog-id-on-close` + `block-ff-push`) |
| `precommit_remote` — **URL-only** | matches the first remote whose URL contains the token — **no** rev/ancestry/id check | `ruff-gate` tombstone-join (`ruff-pre-commit` URL presence; removed-status comes from the join, not fidelity) |
| `precommit_hook` | a named local hook id is wired | `validate-backlog`, `validate-audit-casing` (`audit-casing-r4`), `validate-hermetization` (hub Rule A/B) |
| `hooks-armed` (code-side, fleet-wide) | the 3 git-hook stages (pre-commit / commit-msg / pre-push) are installed + armed | the arm-leg of `settings-precommit-arm` |
| `command_present` / `commands_roster` | a command file exists; the roster of **tracked `.md` directly under `.claude/commands/`** has no uncovered file (non-`.md` invisible) | override/handoff/save/changelog-review |
| `claude_subtrees` | each present **tracked first-level** `.claude/` subdir (from tracked paths ≥2 segments deep) is `shared` (commands) or in that repo's `owned` list | `.claude` internal layout **ownership** (tracked, first-level only) |
| `check_ignore` (effect-probe) | `git check-ignore` resolves a cache candidate (never text-grep — FR-6) | every Tier-4 cache + ai `.env` |
| `ruff_config_form` (code-side) | reports each repo's ruff-config **form** as evidence (never verdicts a winner) | `ruff-config-home` (W3-14 open) |
| dependency leg (code-side) | reads `ecosystem/dependency-baseline.yaml`; **each applicable repo's** (hub + consumer) declared/installed dep vs the baseline (WARN on drift) | the #332 leg (e.g. ai `pytest-xdist` installed-but-undeclared) |
| **root-sweep** (code-side — the anti-regress catch-all) | **every TRACKED top-level entry not covered by an applicable row** → AT-PARITY / `declared_by`, `tracked-ephemera` (Tier-4 cache), or **WARN-undeclared** | this is how `.vscode` is governed **despite having no dedicated row** |

**Verdict vocabulary** (report labels, never blocking in v1): AT-PARITY · PASS-declared · WARN-undeclared · MUST-absent · tombstone-violated · advisory-rewarn · stale-declaration · refused · unavailable · skipped-pre-deploy · tracked-ephemera.

### 3B. Where each operator example falls (the coverage claim, tested)

| operator example | swept? | by which row | verdict today |
|---|---|---|---|
| `.claude` INTERNAL layout | **YES** | `claude-subtree-ownership` + `claude-commands-roster` | AT-PARITY (ownership) — see caveat below |
| `.github` presence | **YES** | `github-ci` (corp LOCAL) | PASS-declared (corp `github-ci-local`) |
| `assets` presence | **YES** | `ai-local-assets` (ai LOCAL, `declared_by: intake-12`) | **AT-PARITY** (template-vouched — no allowlist consulted) |
| `config` presence | **YES** | `shape-dir-config` MUST | AT-PARITY (shape only) |
| caches gitignore-consistency | **YES** | Tier-4 `ignore-*` effect-probes | AT-PARITY (all) |
| `.vscode` presence | **YES** | generic **root-sweep** (no *dedicated* row; OPEN e1) | **PASS-declared** in all three (declared 2026-07-16); a dedicated policy row is withheld pending the e1 ruling |

**So the arc's section-6 proposal (a) — "extend parity surfaces to `.claude` layout + `.github`/`assets`/`config` presence" — is substantially realized in v1.0.0** (at ownership/presence grain; see the completeness caveat in 3C). `.vscode`, the one example without a *dedicated* policy row, is still actively swept by the generic root-sweep and reads PASS-declared — the checker abstains only from assigning it a fleet **policy tier**, not from governing its tracked presence.

### 3C. What it does NOT sweep (out of scope BY DESIGN in v1)

- **`.vscode` *dedicated policy row*** — none (OPEN ruling e1; represented only as an "OPEN rulings" comment block). This is **not** "unswept": tracked `.vscode` is verdicted by the generic root-sweep (declared → PASS-declared) — what's absent is a fleet **policy tier** (MUST/SHOULD/LOCAL) for it.
- **Canonical-doc semantic content/quality** — beyond presence **plus two literal content-marker probes** (CLAUDE.md Form-A `<!-- methodology:start` and BACKLOG `## [E`), there is **no** semantic-quality, complete-marker-set, freshness, or byte-match verdict inside `fleet_parity` (freshness is a separate hub gate + consumer local gates).
- **CLAUDE.md per-region fidelity** — explicitly delegated to `boundary_report.py` (#312), never duplicated (FR-12).
- **Audit-class enum + date-grammar on consumers** — hub-local (consumers carry the casing branch only).
- **Root-file `{methodology|project}` ownership axis** — not modelled in v1 (#316).
- **`.claude` subtree *completeness*** — `claude_subtrees` (`_eval_claude_subtrees`, `fleet_parity.py:1152`) validates that a *present* subtree is legitimately `shared`+`owned`; it does **not** require an owned subtree to exist. Hence ai-council's missing `skills/` is invisible to this row (it surfaces only as the #308 gap). **This is the one place the coverage claim in 3B needs an asterisk: `.claude` layout is swept for *ownership*, not for *completeness*.**
- **Sub-folder depth inside a covered top-level dir** — the root-sweep is **single-depth by deliberate design.** `_eval_sweep`'s own docstring (`fleet_parity.py:1249`) states the **GRAIN LIMIT** verbatim: *"the sweep walks TOP-LEVEL entries only … Depth inside a covered top-level dir (e.g. a rogue `docs/` genre) is Rule-A hermetization's job at the hub and a hardening candidate fleet-wide; this v1 does not claim it."* (No `os.walk`/`.rglob` anywhere in the file; `dir_tracked` is a prefix-existence test, `dir_exists` a plain `is_dir()`.) So a rogue `docs/<genre>/` folder added at a **consumer** is caught by nothing — not the top-level sweep, not the hub-only Rule A. This directly compounds gap c1.

### 3D. Invocation & gating (the teeth question)

- **Wired into:** exactly one live caller — `audit.py::cmd_ship_gate` → `_fleet_parity_surface()` (`audit.py:2701`, called at `:2809` **after** the verdict is already computed from `ALL_CHECKS` at `:2771-2790`), printed as `fleet-parity ([#337]; informational — never blocks this gate)`. Fail-open by contract (spawn errors/timeouts → an ASCII note, never raises; a completed run's `[fleet-parity]` stdout lines are surfaced **and the return code is ignored** — so the surface can neither block nor crash the gate).
- **Not wired into:** `ALL_CHECKS` (verified absent from the full list at `audit.py:2125-2156`, so it never contributes to a RED verdict); `.claude/settings.json` (no SessionStart/Stop hook — grep-confirmed); `.pre-commit-config.yaml`; any automated routine. `ARCHITECTURE.md:189` records the trigger as *"operator / nightly leg (manual)"* — i.e. the "nightly" is a manual CLI invocation, not a wired routine.
- **Proven non-blocking by a dedicated teeth-test:** `tests/test_fleet_parity_surface_is_informational` (`tests/test_ship_gate.py:230`) feeds a `2 must-absent` fleet line and asserts the gate still exits GREEN — *"were the surface fed into the verdict, a must-absent line would RED this."* Also tested: `tests/test_fleet_parity.py` + `tests/test_fleet_parity_events.py`.
- **Promotion path:** [#337] makes it a blocking `ALL_CHECKS` member on an undeclared divergence, **gated on** [#336] clearing the one standing WARN (corp split-state) to reach a true zero-WARN steady state — never a date.

**Bottom line for §3: coverage is broad and manifest-driven (plus four code-side mechanisms, the root-sweep chief among them); enforcement is nil; and the only *wired* execution is the informational ship-gate surface — a manual `fleet_parity.py` CLI run exists but nothing triggers it unattended.**

---

## 4. Root-file governance map — template · byte-match · freshness, per repo TODAY

For the eight named docs, "what governs the file" splits cleanly into four columns. **The gap is not presence (fully governed) — it is content-conformance on consumer docs beyond the floor.**

| doc | presence | template (author skeleton) | byte-match / content | freshness |
|---|---|---|---|---|
| CLAUDE.md | MUST all (`canonical-doc-claude`) | hub `templates/CLAUDE-md-template.md` + Form-A owner markers (region-diff via `boundary_report.py` #312) | **floor fragment only** (`@.claude/CLAUDE-FLOOR.md`, hash-guarded) — body not byte-matched | hub `canonical_freshness` (in `_FRESHNESS_FILES`) **+ both consumers' local `canonical_freshness_gate.py`** |
| VISION / ARCHITECTURE / CONTRIBUTING | MUST all | hub templates exist | none (repo-authored) | hub gate + consumer local gates |
| JOURNAL / LESSONS | MUST all | hub templates exist | none (append-only by design) | not freshness-gated (append-only lifecycle) |
| BACKLOG | MUST all | schema, not template | none | `validate-backlog` schema gate — **all three** (hub root validator; consumers carry the ADR-78 plugin twin) |
| INSTALL | consumer MUST / hub INVERSE | **hub-canonical source** `plugins/tier1-lifecycle/INSTALL.md` | source = byte origin; **per-consumer deploy-carry pending [#315]** | none |

### Where consumers have NONE

- **Canonical-doc template-conformance:** consumers author their own VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING bodies; **no template-diff or byte-match check** governs them. Only INSTALL.md has a hub-canonical byte source (carrier landed hub-side; per-consumer roll is [#315]).
- **Canonical-doc byte-match:** none except the floor fragment. The governed-generic portion of CLAUDE.md is exactly its `owner=hub` Form-A regions (§1/§6 + universal §5/§10 spans); the boundary between "generic + governed" and "local + free" is what [#316] would formalize at file-set granularity.
- **What consumers DO now have (mesh-landed, correcting the register):** `canonical_freshness_gate.py`, `session_end_backpressure.py`, `validate-audit-casing`, `validate-backlog` (local twin), `floor-hash-verify`, `backlog-id-on-close`, `block-ff-push`. So the S8 "founding standard is false for every consumer" gap is **materially narrowed** — the residual hub-only organs are `doc_claims` + `git_backlog_drift` (hub-only-by-construction, not a closable consumer gap) and the coherence spine.

---

## 5. RECON-FIRST — existing tickets & rulings on root-structure governance (do NOT re-invent)

This work is **heavily pre-captured.** Every proposal in §6 maps to one of these; none is greenfield.

**Ratified decisions (rulings of record):**
- **ADR-101** (Hermetization, Accepted 2026-07-11) — CLOSED sanctioned Tier-1 set + `docs/<genre>/` seal + per-class audit-name grammar (11-class enum, R3) + all-lowercase-kebab casing (R4) + the refusal gate spec (§3). Amends **ADR-34** (file-naming). Extends **ADR-60** (docs taxonomy), **ADR-98** (intake genre-folder-first).
- **intake #12 — Fleet Ownership Manifest (SETTLED 2026-07-12)** — the operator's **two-trees model** (hub template tree × each repo's implementation tree; the manifest is their join) + the **nightly hygiene decision tree**. §9a: the hub is a fleet member (its own `.methodology.yaml`). *This is the "management system for repo structure" design of record.*
- **intake #14 — SIEM requirements RULED-pack (`docs/intake/2026-07-12-siem-requirements-ruled-pack.md`, RULED)** — the authoritative FR-numbered requirements (`FR-1…FR-15`) that `#328` builds against ("#328 builds against THIS, not against either draft alone"); its two provenance drafts (Fable + Codex `2026-07-13-siem-fleet-management-requirements*.md`) are retained-but-superseded.
- **2026-07-11 fleet-parity register** — the divergence register (§0 master table a1–g2, M) + the §9 `fleet_parity` design. Now realized as v1.0.0 (several rows since superseded by ARC-A/B). ("parity-surfaces v1" is operator shorthand fusing the manifest filename with the "WARN-only v1" maturity label — not a doc title.)
- **satellite-onboarding-rulings.yaml** (2026-07-16) — corp-ops / corp-sca / life-architect / demo-prep all ruled **full** profile (the fleet-wide onboarding target).

**Built (the mechanisms this census confirms live):**
- **[#328]** parity-surfaces manifest + `fleet_parity` check — **BUILT** (`ecosystem/parity-surfaces.yaml` v1.0.0 + `scripts/fleet_parity.py`, WARN-only, informational ship-gate).
- **[#306]** `validate_hermetization.py` refusal gate — **BUILT, hub-only** (Rule A tree-seal + Rule B casing/enum).
- **[#312]** fleet boundary marker + `boundary_report.py` — **BUILT** (Form-A markers + read-only reporter).
- **enforcement mesh S8 (#235–238)** — Informant organ + mesh carrier — **BUILT** (both consumers carry freshness/backpressure/backlog/casing + ff-guard).

**Filed, unbuilt (the residual arcs):**
- **[#316]** Root-files boundary declaration — a `root_files:` manifest classifying each sanctioned root entry `{methodology-generic | project | conditional}` + a reporter diffing declared-vs-actual per repo. *The operator's exact per-entry ask.* Folds #314/#315 file-set shapes.
- **[#337]** Promote `fleet_parity` to a blocking `ALL_CHECKS` member — gated on **[#336]** (corp `precommit-hub-block` v1.3.1-vs-v1.2.0 split reconciliation).
- **[#324]** Codify the night-batch → morning-prompt loop (the nightly parity-walk runtime + verdict-sheet consumer) — charter, deferred.
- **[#329]** VS Code ownership visualization — folder icons/colors **generated from** the #328 manifest + `.methodology.yaml` (depends-on #316's ownership axis).
- **[#308]** verify-skill home + the ai-council-no-skills half-adoption.
- **[#331]** Consumer BACKLOG story-map adoption ruling; **[#334]** ruff→ruff-check id migration; **[#332]** fleet dependency-version parity; **[#280]/[#315]/[#43]** (S17) new-repo scaffold correct-by-default; **[#314]/[#327]** protocols/ genre.

---

## 6. Proposals — 3 arcs closing the true residuals (proposals only; draft Done-whens for operator ruling)

Framed to **execute filed work, not reinvent it.** The census's value-add is the *sequencing* and the evidence that the residual is now exactly this narrow.

### Arc P1 — Give the parity contract teeth + an unattended run (execute [#336] → [#337], build [#324]'s parity leg)

**Why:** the #1 gap is c2 — the contract *sees* the fleet but never gates and never runs unattended. Today parity is inspected only when a human ships the hub and reads one informational line.
- **Step 1 — [#336]:** reconcile the sole standing WARN (corp `precommit-hub-block` rev `v1.3.1` vs corpus `v1.2.0`) — either model enforcement-gate-rev separately from corpus `source_tag` in `parity-surfaces.yaml`, or schedule a real v1.3.1 corp redeploy. This clears the zero-WARN precondition.
- **Step 2 — [#337]:** promote `fleet_parity` to a blocking `ALL_CHECKS` member (undeclared divergence hard-blocks a ship; declared/at-parity passes).
- **Step 3 — [#324]:** wire the read-only parity walk into an unattended surface (a `SessionStart` `fleet_health` digest line and/or the nightly routine) so a new undeclared divergence surfaces the next morning, not just at the next hub ship.
- **Draft Done-when:** the corp split WARN is reconciled (recorded, no corpus over-claim); `fleet_parity` is an `ALL_CHECKS` member REDding a seeded undeclared divergence and passing a declared one, with tests; AND the parity verdict renders in an unattended digest (SessionStart line or nightly report) from live counts.

### Arc P2 — Carry the ADR-101 top-level tree seal to consumers (execute [#306] P6)

**Why:** gap c1 — Rule A (tree-seal) fires nowhere on a consumer; a consumer can add an unsanctioned top-level dir unblocked. The casing branch is already carried; the seal is not.
- **Shape:** carry `validate_hermetization` Rule A to consumers with a **per-repo sanctioned set** — derived from that repo's `parity-surfaces.yaml` LOCAL rows + `.methodology.yaml` (so `src/`, `data/`, `eval/`, `council_inbox/`, `assets/` are sanctioned per their owner), NOT the hub's verbatim set (which would brick dev). The set is data, the gate is generic.
- **Draft Done-when:** a consumer's added unsanctioned top-level dir/file BLOCKS at pre-commit (Rule A carried, keyed to that repo's sanctioned set), witnessed n=1, while a sanctioned add (a new file under `src/`) passes — with tests; the per-repo sanctioned set is derived from the manifest, not hand-listed.

### Arc P3 — Build the [#316] per-entry root-file ownership classification (the "management system" at file-set granularity)

**Why:** gap c3 — the operator's literal ask ("classify every surface methodology-vs-application WITHOUT searching; machine-readable") is a filed-but-unbuilt axis. `parity-surfaces.yaml` has role-tiers but not the `{methodology-generic | project | conditional}` ownership dimension the VS Code viz (#329) needs.
- **Shape:** add a hub-owned `root_files:` ownership map (a block in the manifest or a sibling file) classifying each sanctioned root entry per repo-role; extend the #312 reporter (or a sibling) to diff declared-ownership-set vs actual `ls` per repo. Reuse `parity-surfaces.yaml` as the source of truth for tiers; add only the ownership axis. Unblocks #329.
- **Draft Done-when:** a hub-owned root-entry ownership classification exists (every sanctioned root entry tagged `{methodology-generic | project | conditional}`), a read-only reporter diffs declared-vs-actual per repo (surfacing an unclassified new entry), and #329's viz can render deterministically from it — or #316 decomposes into #314/#315-aligned sub-tickets with a recorded reason.

### (Optional) Arc P4 — Two small rulings that retire live shelf-lives

- **`.vscode` e1 (template-membership):** all three now track `.vscode/settings.json`, declared with a forcing 2026-08-13 shelf-life. Rule it: **carried fleet template** (add a `.vscode` MUST/SHOULD row + a deploy carrier) **or** permanent per-repo LOCAL (keep the declarations, drop the forcing date). **Draft Done-when:** e1 is ruled and the three `.vscode` declarations either retire (template) or convert to durable LOCAL.
- **ai-council `skills/` (#308):** decide adopt-a-minimal-skills-dir vs accept-absent-with-reason, so the universal+per-project skill pattern is either whole or explicitly waived fleet-wide. **Draft Done-when:** ai-council either carries a `.claude/skills/` (n≥1) or the absence is declared in its `.methodology.yaml`.

---

## 7. Anti-pattern check (this report's own discipline)

- **Zero mutations outside this file** — no `.methodology.yaml` edited, no `parity-surfaces.yaml` row added, no gate wired, no consumer touched. All §6 items are proposals with draft Done-whens for operator ruling (core-invariant #3; ADR-70 capture-precedes-construction).
- **No reinvention** — every proposal cites its existing ticket; the census's contribution is evidence + sequencing, not new mechanisms.
- **Faithful to live state** — findings that contradict the 2026-07-11 register (e2 `.hypothesis` resolved; e1 `.vscode` now fleet-tracked+declared; b2 `validate_backlog` now consumer-carried; #302/#309 parity landed) are reported as *the register being overtaken by subsequent arcs*, not as new gaps.

*Read-only sweep: no file in `.dev-knowledge`, `corp-monorepo`, or `ai-council` was moved, renamed, or deleted. Committed on `docs/fleet-structure-census`.*
