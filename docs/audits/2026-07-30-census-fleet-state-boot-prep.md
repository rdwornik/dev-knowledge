---
class: census
date: 2026-07-30
slug: fleet-state-boot-prep
Status: "UNVERIFIED-UNTIL-LOCAL — INPUT, NOT AUTHORITY"
producer: claude-code-night-batch
lane: claude/night-2026-07-30-boot-prep
anchor_sha: c8490c1d
consumer: incoming 2026-07-31 dev-knowledge architect boot
consumption_path: "branch -> local re-verification -> architect reads at boot"
scope: "read-only state census of all 6 fleet repos; no git mutations in any repo"
---

> **Status: UNVERIFIED-UNTIL-LOCAL. INPUT, NOT AUTHORITY.** Cloud night-batch lane: no merge,
> no canon edit, no closure, no ruling. Point-in-time snapshot — the hub HEAD advanced during
> the census (see the live-concurrency addendum); re-derive current HEAD on boot.

# Fleet Census — 2026-07-30 (for 2026-07-31 architect boot)

**UNVERIFIED-UNTIL-LOCAL.** This census was produced by a Claude Code session with no
git mutations (read-only `status/log/rev-list/branch --list/remote/diff --stat/show`
only). Per-repo A/B data was gathered by 6 parallel read-only subagents (one per repo);
Section C/D cross-checks and all parity reproduction were done directly by the
orchestrating session against live repo state, cited by exact command/file:line.
Two subagent outputs (win-tooling, corp-ops) were auto-flagged by the harness as
"instruction-shaped" — inspected, contain no embedded directives, treated as plain
findings only.

Reference date for all day-math: **2026-07-30**.

---

## A. HEAD / sync / gates — per repo

| Repo | Branch | HEAD | Subject | Tree | Ahead/Behind @{u} | Unmerged vs main | Pre-commit gate |
|---|---|---|---|---|---|---|---|
| .dev-knowledge | `claude/night-2026-07-30-boot-prep` (unchanged, as instructed) | `c8490c1d` | Merge 'docs/handoff-2026-07-31-architect' — supplement filled and folded | clean | **no upstream configured** (`@{u}` resolution fails: `fatal: no upstream configured for branch 'claude/night-2026-07-30-boot-prep'`) | `automation/fleet-audit` | **ARMED** — `.git/hooks/pre-commit` is a genuine pre-commit shim; `core.hooksPath` unset (default path in effect, not overridden) |
| ai-council | `main` | `be46b30` | Merge 'chore/vscode-e1-redate' | clean | 0 ahead / 0 behind `origin/main` | none (`git branch --no-merged main` empty; only `main` exists locally) | **ARMED** — real shim, `core.hooksPath` unset |
| corp-monorepo | `main` | `c954876` | Merge origin/main (nightly conformance digests) into main | clean | 0 ahead / 0 behind `origin/main` | `docs/327-interface-genre-markers` | **ARMED** — real shim, `core.hooksPath` unset |
| corp-ops | `main` | `d040fcb` | Merge chore/dev-terminals-revert-uppercase-name (lowercase workspace folder name) | clean | **4 ahead / 0 behind** `origin/main` (`git rev-list --left-right --count @{u}...HEAD` → `0  4`) | none | **ABSENT, not silently disarmed** — no `.pre-commit-config.yaml` exists at all; `.git/hooks/` has only stock `*.sample` files; `core.hooksPath` unset (this is "never wired," not the "dead hooksPath" hazard pattern). `.claude/settings.json` declares `tier1-lifecycle` plugin enabled but the gate was never installed. |
| corp-sca-time-automation | **`feature/tenrox-loader`** (NOT main) | `3661b3a` | feat(tenrox): recon method-dump + write-free request tracer | clean | 0 ahead / 0 behind `origin/feature/tenrox-loader` | `feature/tenrox-loader` itself is unmerged into main (it's the checked-out branch) | **ARMED but minimal** — `.pre-commit-config.yaml` contains ONLY `floor-hash-verify` (local hook); no ruff hook exists in this repo at all. `core.hooksPath` unset. |
| win-tooling | `main` | `555adec` | Merge fix/typewhisper-windowless-daemons (background daemons run windowless) | clean | **no remote configured at all** (`git remote -v` empty — fully local-only repo) | none (only `main` exists locally) | **ABSENT, not silently disarmed** — no `.pre-commit-config.yaml` exists anywhere in the repo (confirmed via Glob); only stock `.sample` hooks; `core.hooksPath` unset. Consistent with open `BACKLOG.md:20` `[#1]` (tier1-lifecycle plugin declared in `.claude/settings.json` but Stop-hook closure loop not yet live). |

**Flags:**
- No repo exhibited the "relic hooksPath pointing at a dead path" silent-disarm hazard — every `core.hooksPath` was cleanly unset. The gate-absence in corp-ops/win-tooling/corp-sca-time-automation(ruff) is "never installed," a different (also real) gap.
- corp-sca-time-automation is the only repo checked out on a non-main branch.
- .dev-knowledge has no upstream tracking ref on its current night-batch branch — ahead/behind vs remote genuinely cannot be computed by git; this is expected for an ephemeral Claude-session branch, not necessarily an anomaly.

---

## B. Dated-ledger inventory — sorted oldest-first

Two kinds of dated field are mixed below, distinguished in the **Kind** column:
- **stamp** = `last_reviewed:` (a historical record of when something was reviewed — not itself a deadline; flagged STALE where it exceeds the hub's 30-day freshness cadence, per `CLAUDE.md` §4 "Freshness cadence" doctrine)
- **deadline** = `review_date` / `expires` / `shelf_life` / forcing-date / dated `revisit` (a forward-looking commitment; flagged EXPIRED if past 2026-07-30, DUE SOON if ≤14 days out i.e. on/before 2026-08-13)

| Date | Kind | Repo | File:line | Field | Subject | Days (past=old / until) | Flag |
|---|---|---|---|---|---|---|---|
| 2026-03-12 | stamp | corp-monorepo | `config/rfp/product_profiles/_overrides/wms.yaml:9` | last_reviewed | RFP product-profile override yaml | 140d old | STALE (config data field, not a canonical doc — informational) |
| 2026-05-12 | stamp | .dev-knowledge | `templates/scrum-master-cover-letter.md:4` | last_reviewed | template file (not a canonical living doc) | 79d old | not gated (template) |
| 2026-06-02 | stamp | corp-ops | `ARCHITECTURE.md:2`, `CLAUDE.md:2`, `CONTRIBUTING.md:2`, `VISION.md:4` | last_reviewed | all 4 canonical docs, same date | 58d old | **STALE >30d cadence** |
| 2026-06-02 | stamp | corp-sca-time-automation | `ARCHITECTURE.md:2`, `CLAUDE.md:2`, `CONTRIBUTING.md:2`, `VISION.md:4` | last_reviewed | all 4 canonical docs, same date | 58d old | **STALE >30d cadence**; CLAUDE.md was edited 2026-06-08 (6 days after stamp) without re-review — edited-but-not-re-reviewed drift |
| 2026-06-02 | stamp | corp-monorepo | `VISION.md:5` | last_reviewed | VISION.md | 58d old | **STALE >30d cadence** |
| 2026-06-16 | stamp | corp-monorepo | `docs/archive/2026-06-16-current-state-architecture-audit.md:2` | last_reviewed | archived audit doc | 44d old | not gated (archive) |
| 2026-06-19 | stamp | .dev-knowledge | `protocols/DEFINITION_OF_DONE.md:2` | last_reviewed | DoD protocol | 41d old | **STALE >30d cadence** |
| 2026-07-09 | deadline-ish | .dev-knowledge | `ecosystem/tool-versions.yaml` (claude-code, codex) | reviewed_date | changelog-review state | 21d old | informational (not a deadline field) |
| 2026-07-11 | stamp | win-tooling | `ARCHITECTURE.md:2`, `CLAUDE.md:2`, `CONTRIBUTING.md:2`, `VISION.md:4` | last_reviewed | all 4 canonical docs, same date | 19d old | fresh (<30d), no local enforcement mechanism found |
| 2026-07-12 | stamp | corp-monorepo | `ARCHITECTURE.md:2` | last_reviewed | ARCHITECTURE.md | 18d old | fresh; open nightly-conformance-digest finding (2026-07-21/22) proposes re-stamping due to stale task_manager.py refs — not yet actioned |
| 2026-07-13 | stamp | corp-monorepo | `CLAUDE.md:2` | last_reviewed | CLAUDE.md (v2.8) | 17d old | fresh |
| 2026-07-16 | deadline (ruled, not shelf-life) | .dev-knowledge | `ecosystem/satellite-onboarding-rulings.yaml` | ruled_date | corp-ops/corp-sca-time-automation/life-architect/demo-prep onboarding-profile rulings | 14d old | informational, past ruling not a forward deadline |
| 2026-07-18 | stamp | corp-monorepo | `CONTRIBUTING.md:2` | last_reviewed | CONTRIBUTING.md | 12d old | fresh |
| 2026-07-19 | stamp | ai-council | `docs/audits/2026-07-19-night-consolidation-verification.md:4` | last_reviewed | audit doc (not canonical) | 11d old | not gated |
| 2026-07-23 | stamp | ai-council | `VISION.md:4` | last_reviewed | VISION.md | 7d old | fresh |
| 2026-07-24 | stamp | ai-council | `CONTRIBUTING.md:2` | last_reviewed | CONTRIBUTING.md | 6d old | fresh |
| 2026-07-25 | stamp | .dev-knowledge | `VISION.md:4` | last_reviewed | VISION.md | 5d old | fresh |
| 2026-07-27 | stamp | .dev-knowledge | `CONTRIBUTING.md:2` | last_reviewed | CONTRIBUTING.md | 3d old | fresh |
| 2026-07-27 | stamp | ai-council | `ARCHITECTURE.md:2`, `CLAUDE.md:2` | last_reviewed | ARCHITECTURE.md, CLAUDE.md | 3d old | fresh |
| 2026-07-28 | stamp | .dev-knowledge | `ARCHITECTURE.md:2` | last_reviewed | ARCHITECTURE.md | 2d old | fresh |
| 2026-07-29 | stamp | .dev-knowledge | `protocols/SESSION_SETUP.md:2`, `protocols/AI_COUNCIL_PROCESS.md:2` | last_reviewed | protocols | 1d old | fresh |
| 2026-07-30 | stamp | .dev-knowledge | `CLAUDE.md:2`, `protocols/ESSENTIALS.md:2` | last_reviewed | CLAUDE.md, ESSENTIALS.md | 0d (today) | fresh |
| **2026-08-13** | **deadline** | .dev-knowledge | `ecosystem/disposition-register.yaml` (`warn-doc-rot-backlog-332`) | review_date | doc-rot disposition for BACKLOG #332 | **+14d** | **DUE SOON** (earliest forward deadline found in the whole census) |
| **2026-08-13** | **deadline** | .dev-knowledge | `logs/PROPOSALS-2026-07-30.md` (and prior days back to 07-19) | shelf-life (BACKLOG `[#352]`) | "Versioned `.vscode` region decoration" — revisit/kill if not advanced | **+14d** | **DUE SOON** |
| 2026-08-16 | deadline | ai-council | `.methodology.yaml:85` | review_date | `dep-pytest-xdist` sanctioned-divergence waiver | +17d | not due-soon; **note: this waiver is now STALE-BY-EVIDENCE** — see §D finding 1, pytest-xdist is already pinned in `pyproject.toml:35`, so the divergence the waiver describes no longer exists |
| 2026-08-18 | deadline | .dev-knowledge | `ecosystem/disposition-register.yaml` (`warn-doc-rot-backlog-344`) | review_date | doc-rot disposition BACKLOG #344 | +19d | — |
| 2026-08-26 | deadline | .dev-knowledge | `.methodology.yaml:99` (`.vscode`) | review_date | hub `.vscode` sanctioned divergence, deliberately short shelf-life pending register ruling "e1" | +27d | — |
| 2026-08-26 | deadline | .dev-knowledge | `ecosystem/disposition-register.yaml` (4 entries: `warn-undeclared-intake-v6-proposal`, `-design-input`, `-index`, `-orientation` handoff-process) | review_date | intake-doc undeclared-edge dispositions | +27d | — |
| 2026-08-26 | deadline | .dev-knowledge | `ecosystem/disposition-register.yaml` (`warn-doc-rot-backlog-421`, `-422`) | review_date | doc-rot dispositions | +27d | — |
| 2026-08-26 | deadline | .dev-knowledge | `ecosystem/disposition-register.yaml` (`warn-fleet-parity-ai-council-root-conftest`, ref #430) | review_date | ai-council root conftest.py undeclared-edge tracking | +27d | matches live §D finding 2 below |
| 2026-08-26 | deadline | ai-council | `.methodology.yaml` (`.vscode`) | review_date | ai-council `.vscode` divergence, same "e1" question | +27d | — |
| 2026-08-26 | deadline | corp-monorepo | `.methodology.yaml:100` (`.vscode`) | review_date | corp-monorepo `.vscode` divergence, same "e1" question | +27d | 3-way-linked with the hub + ai-council `.vscode` entries above — all three share the identical 2026-08-26 date, confirming deliberate coordination |
| 2026-10-07 | deadline | corp-monorepo | `.methodology.yaml:22` | review_date | `ruff-gate` sanctioned divergence | +69d | — |
| 2026-10-11 | deadline | corp-monorepo | `.methodology.yaml:36` | review_date | `hub-codemap-hooks` divergence | +73d | — |
| 2026-10-11 | deadline | ai-council | `.methodology.yaml` | review_date | `hub-codemap-hooks` divergence | +73d | — |
| 2026-10-11 | deadline | .dev-knowledge | `.methodology.yaml` | review_date | (hub-codemap-hooks not applicable — hub is source; not present in hub file) | — | n/a, listed for consumer-side symmetry only |
| 2026-10-12 | deadline | .dev-knowledge | `.methodology.yaml` (`ruff-gate`) | review_date | hub ruff-gate divergence | +74d | — |
| 2026-10-12 | deadline | corp-monorepo | `.methodology.yaml` (`audit-casing-r4`, `github-ci-local`) | review_date | 2 divergences | +74d | — |
| 2026-10-12 | deadline | ai-council | `.methodology.yaml` (`ruff-gate`, `hub-hermetization-rule-a`, `hub-hermetization-rule-b-grammar`) | review_date | 3 divergences | +74d | — |
| 2026-10-13 | deadline | .dev-knowledge | `.methodology.yaml` (`hub-hermetization-rule-a`, `-rule-b-grammar`, `token-log`, `command-handoff`, `command-save`, `command-changelog-review`, `.claude-plugin`, `.worktreeinclude`, `codex`, `package.json`, `package-lock.json`) | review_date | 11 divergences, same date | +75d | — |
| 2026-10-13 | deadline | ai-council | `.methodology.yaml` (`claude-md-section-11-title`) | review_date | 1 divergence | +75d | — |
| 2026-10-22 | deadline | corp-monorepo | `.methodology.yaml` (`vscode-boundary-decoration`) | review_date | interim declared-until-mechanism adoption | +84d | — |
| 2026-10-22 | deadline | ai-council | `.methodology.yaml` (`vscode-boundary-decoration`) | review_date | same | +84d | — |
| 2026-10-25 | deadline | .dev-knowledge | `.methodology.yaml` (`adr77-transcript-guard`) | review_date | re-read trigger: keep-armed vs retire decision | +87d | — |
| 2026-10-26 | deadline | ai-council | `.methodology.yaml` (`claude-md-token-log-address`) | review_date | expires-by-reference when hub #427 lands | +88d | — |

**No dated field found anywhere PAST 2026-07-30** (i.e. **zero EXPIRED** deadline-type entries in the whole fleet). **Two entries are DUE SOON** (both land exactly 2026-08-13, 14 days out): `warn-doc-rot-backlog-332` and BACKLOG `[#352]`'s shelf-life.

**Repos with zero dated `review_date`/`expires`/`shelf_life` fields found at all:** corp-ops, corp-sca-time-automation, win-tooling — none of the three carry a `.methodology.yaml` sanctioned-divergence register, so this entire class of ledger is absent for them (consistent with corp-ops/corp-sca-time-automation being pre-deploy and win-tooling being unregistered — see §D).

---

## C. Version / lockstep state

**Hub methodology versions** (`deploy/manifest-v*.yaml`, `.dev-knowledge/deploy/`):
`v1.0.0, v1.1.0, v1.2.0, v1.3.0, v1.3.1, v1.4.0` — **latest = v1.4.0** (matches `.claude/methodology-roster.md` header "manifest v1.4.0").

**`ecosystem/deployed-versions.yaml` vs actual deployed state:**

| Repo | Declared (`deployed-versions.yaml`) | Actual live evidence | Verdict |
|---|---|---|---|
| .dev-knowledge | `null` (hub is the source, not a consumer of its own corpus) | n/a | consistent by definition |
| ai-council | `1.3.1`, deployed 2026-07-11 | `.pre-commit-config.yaml:67-68` pins hub hooks (toc-freshness, toc-generate, backlog-id-on-close, block-ff-push) `@ v1.3.1`; `.claude/CLAUDE-FLOOR.md` + sha256 sidecar present | **CONSISTENT** |
| corp-monorepo | `1.2.0`, deployed 2026-07-07, explicit comment "stays 1.2.0 BY DESIGN — do not fix to 1.3.1" (ADR-102) | `.pre-commit-config.yaml:91` pins `backlog-id-on-close`+`block-ff-push` `@ v1.3.1` (gate uplifted ahead of the 1.2.0 corpus) | **CONSISTENT WITH DECLARED EXCEPTION** — this is exactly the ADR-102 `gate_rev_ahead` case, reproduced in §D finding 3 |
| corp-ops | `null` (pre-deploy) | No `.claude/CLAUDE-FLOOR.md`, no `.pre-commit-config.yaml` anywhere | **CONSISTENT** (genuinely nothing deployed) |
| corp-sca-time-automation | `null` (pre-deploy) | **HAS** `.claude/CLAUDE-FLOOR.md` + sha256 sidecar + a `floor-hash-verify` pre-commit hook (partial floor-only adoption) | **PARTIAL MISMATCH** — the registry says "nothing deployed yet" but the repo already carries the floor mechanism; not captured by the `deployed_methodology_version` field, which is corpus-deploy-only, not floor-adoption-only. Flagging as a real but narrow gap, not a contradiction of doctrine (the file's own header describes this axis as corpus-deploy, and the floor is a separate carrier). |
| win-tooling | **not listed in the file at all** (not even a `null` row) | No floor, no pre-commit, no ruff gate — nothing | Confirmed independently by the hub's own `ecosystem/index.yaml:633` finding: "win-tooling not listed in deployed-versions.yaml (ADR-91)", status `warn` |

**`ecosystem/tool-versions.yaml` vs installed (best-effort, all 6 repos ran the same commands on the same machine — results identical everywhere):**
- `ruff --version` → `ruff 0.15.5` (every repo)
- `python --version` / `py --version` → `Python 3.12.10` (every repo)
- `pre-commit --version` → `pre-commit 4.5.1` (every repo)
- `uv --version` → `uv 0.11.19 (7b2cff1c3 2026-06-03 x86_64-pc-windows-msvc)` (every repo)
- `tool-versions.yaml` itself tracks a **different axis** — last-reviewed-changelog version, not installed version: `claude-code last_reviewed_version: "2.1.204"` (2026-07-09), `codex last_reviewed_version: "0.143.0"` (2026-07-09). Installed claude-code/codex CLI versions were **not independently checked** (out of scope for a git-based repo sweep; would need `claude --version` / `codex --version` run outside this session's own harness to avoid self-referential noise).

**Ruff pre-commit rev per repo, and gate-bearing-repo agreement:**

| Repo | Ruff hook in `.pre-commit-config.yaml`? | Pinned rev |
|---|---|---|
| .dev-knowledge | yes | `v0.15.5` |
| ai-council | yes | `v0.15.5` |
| corp-monorepo | yes | `v0.15.5` |
| corp-ops | **no** (repo has no `.pre-commit-config.yaml`; ships an unactivated *template asset* at `assets/ruff-pre-commit.yaml` pinned `v0.15.5` for other repos to consume — not self-applied) | n/a |
| corp-sca-time-automation | **no** (only `floor-hash-verify` local hook) | n/a |
| win-tooling | **no** (no `.pre-commit-config.yaml` at all) | n/a |

The 3 gate-bearing repos (hub, ai-council, corp-monorepo) **agree exactly** at `v0.15.5`, matching the `pyproject.toml` `[tool.ruff] required-version = ">=0.15.5"` floor and the live installed `ruff 0.15.5` everywhere.

**`HANDOFF_PROCESS.md` Version field and `reconciled_with` stamps:**
- Hub `protocols/HANDOFF_PROCESS.md:4` → **`Version: 5.7`**
- ai-council `CONTRIBUTING.md:3` → `reconciled_with: handoff-process@5.7` — **MATCHES hub exactly**
- corp-monorepo `CONTRIBUTING.md:3` → `reconciled_with: handoff-process@v5` — **STALE AND MALFORMED**: names only a major-ish "v5" (not the `<spec-id>@<version>` grammar, and 2+ point-releases behind the hub's actual 5.7). This is not a subagent artifact — corp-monorepo's own generated audit pointer (`ecosystem/corp-monorepo/state.yaml`, `check_name: reconciled_versions`) independently flags the identical defect: `"CONTRIBUTING.md: malformed (reconciled_with not '<spec-id>@<version>')"`, status `warn`. Verified directly by reading `corp-monorepo/CONTRIBUTING.md:3` on its own `main` branch (repo is currently checked out on `main`, so this is bare-main state with no `git show` indirection needed).
- corp-ops, corp-sca-time-automation, win-tooling: **no `reconciled_with` field found anywhere** — none of the three carry a local `protocols/HANDOFF_PROCESS.md`, so the field is simply absent (their own per-repo audit checks report `n/a`/`no reconciled_with edges declared`), not a defect.

---

## D. Parity findings — reproduced on bare main before listing

**Method:** `python scripts/fleet_parity.py --run-date 2026-07-30 --no-write --no-events` was run from the hub checkout (branch `claude/night-2026-07-30-boot-prep`, per the CRITICAL CAVEAT this is a non-main hub checkout). No `GIT_DIR`/other `GIT_*` env-var overrides were present (`env | grep '^GIT'` showed only `GIT_ASKPASS`/`GIT_EDITOR`, no `GIT_DIR`/`GIT_WORK_TREE`). The walk resolves each **consumer** repo via `ecosystem/<repo>/state.yaml` path pointers to the actual sibling checkouts on disk — per §A, every consumer except corp-sca-time-automation is itself currently sitting on its own `main` at 0/0 with origin, so the walk's consumer-side findings are effectively bare-main reads already; each is independently re-verified below by reading the specific file directly (not trusting the tool's own resolution), which is what "reproduced on bare main" means in practice here. The hub-side findings (root-sweep entries, hooks, ruff-gate) were read from the hub's OWN `.methodology.yaml`/`.pre-commit-config.yaml` on disk — the hub's working tree is clean and these are tracked committed files, so their content is identical on the current branch and on `main` (confirmed no divergence for these specific files via the section-A clean-tree check + no evidence any of them differ from `git show main:<path>` was found or needed, since they are long-committed governance files unrelated to the in-flight branch's diff).

Raw walk output: `183 at-parity, 19 pass-declared, 1 gate-ahead-declared, 1 warn-undeclared, 0 must-absent, 0 tombstone-violated, 0 advisory-rewarn, 1 stale, 0 refused`.

Only the **non-at-parity, non-routine-PASS-declared** findings are listed as findings below (the 19 PASS-declared root-sweep/command/hermetization/token-log entries are hub's own long-declared sanctioned divergences in `.methodology.yaml`, all reproduced trivially by reading that file — not repeated here as "findings").

### Finding 1 — REPRODUCED: ai-council `dep-pytest-xdist` waiver is stale-by-evidence
- **Parity output:** `ai-council dep-pytest-xdist stale-declaration — declaration 'dep-pytest-xdist' matches no live dependency drift (state: at parity)`
- **Reproduction:** `ai-council/.methodology.yaml` (component `dep-pytest-xdist`, review_date 2026-08-16) declares the divergence as "ai-council carries pytest-xdist 3.8.0 in its .venv but does NOT pin it in pyproject". Read directly: `ai-council/pyproject.toml:35` → `"pytest-xdist>=3.8",   # dep-parity: installed 3.8.0 was undeclared (checker rule 10; 2026-07-23 session-close) — declaring, not adding`. The dependency **is now pinned** — the divergence the waiver describes no longer exists (closed 2026-07-23, a week before this waiver's own 2026-08-16 review_date). Repo is on `main`, clean, 0/0 with origin — this is bare-main state.
- **Verdict:** genuine finding — a now-moot `.methodology.yaml` entry that should be retired at (or before) its 2026-08-16 review_date rather than waiting.

### Finding 2 — REPRODUCED: ai-council root `conftest.py` — known, tracked, not yet resolved
- **Parity output:** `ai-council root-sweep WARN-undeclared: top-level entry 'conftest.py'`
- **Reproduction:** `ai-council/conftest.py` confirmed present at repo root (2608 bytes, modified 2026-07-26 14:42, on `main`). Hub's `ecosystem/disposition-register.yaml` (`warn-fleet-parity-ai-council-root-conftest`, ref `#430`, review_date 2026-08-26) already tracks exactly this: "A sibling repo merged a TRACKED root conftest.py ... and the hub's consumer-role root template does not admit it ... [#430] tracked, open."
- **Verdict:** reproduced and already a known, tracked open item (not a new gap) — due for its own review by 2026-08-26.

### Finding 3 — REPRODUCED: corp-monorepo `precommit-hub-block` gate-ahead-declared
- **Parity output:** `corp-monorepo precommit-hub-block gate-ahead-declared — enforcement gate declared ahead of corpus: pin v1.3.1 is a proven descendant of corpus v1.2.0 (ADR-102)`
- **Reproduction:** read directly on corp-monorepo's `main` (clean, 0/0 with origin): `.pre-commit-config.yaml:91-94` → `rev: v1.3.1` / `hooks: - id: backlog-id-on-close` / `- id: block-ff-push`, with an in-file comment at line 78-79 confirming "pinned to the published methodology tag v1.3.1 ... Consumed: the two enforcement gates". Cross-checked against `ecosystem/parity-surfaces.yaml:404-421` (surface `precommit-hub-block`, `gate_rev_ahead.corp-monorepo.gate_tag: v1.3.1`) and `ecosystem/deployed-versions.yaml` (corp-monorepo corpus stays 1.2.0 by design, ADR-102).
- **Verdict:** reproduced exactly; this is a **declared, blessed** state (ADR-102), not an anomaly.

### Finding 4 — REPRODUCED: corp-ops / corp-sca-time-automation `fleet-membership skipped-pre-deploy`
- **Parity output:** both repos report `fleet-membership skipped-pre-deploy — registered, no methodology deployed yet`
- **Reproduction:** `ecosystem/deployed-versions.yaml` lists both with `deployed_methodology_version: null`. Live evidence: corp-ops has no `.claude/CLAUDE-FLOOR.md` and no `.pre-commit-config.yaml` at all (§A); corp-sca-time-automation has a partial floor-only adoption (`.claude/CLAUDE-FLOOR.md` + `floor-hash-verify` hook only, no ruff gate) — consistent with "not yet deployed" for the full corpus sense this field tracks (see §C partial-mismatch note).
- **Verdict:** reproduced.

### Finding 5 — UNREPRODUCED-BY-SCOPE (not a parity-tool finding, but a real gap worth flagging): win-tooling is absent from the fleet_parity manifest entirely
- win-tooling did **not appear anywhere** in the `fleet_parity.py` walk output — not even as `skipped-pre-deploy`. Checked `ecosystem/parity-surfaces.yaml:98-104` `fleet:` mapping directly: only `.dev-knowledge` (hub), `ai-council` (consumer), `corp-monorepo` (consumer), `corp-ops` (pre-deploy), `corp-sca-time-automation` (pre-deploy) are registered — **win-tooling is not a key in this mapping at all**, and is also absent from `ecosystem/satellite-onboarding-rulings.yaml` (which rules `corp-ops`, `corp-sca-time-automation`, `life-architect`, `demo-prep` but never mentions win-tooling). This is why it produced zero parity lines: it is fully out of the parity contract's scope, not silently passing or silently failing.
- This is **not** a `must-absent` finding (nothing is declared MUST for an unregistered repo) and is **not** one of the hub-only-by-construction organs (`doc_claims`/`git_backlog_drift`) — it is a distinct, genuine registration gap: win-tooling is tracked by the broader `audit.py` per-repo check (`ecosystem/win-tooling/state.yaml` exists, `last_audit: 2026-07-30`) but never entered the `#328` fleet-parity manifest or the satellite-onboarding ruling register.
- Listed as **UNREPRODUCED-as-a-parity-finding** per the task's instruction (it never appeared as a parity verdict to reproduce) but flagged because it is a real, evidenced state worth the architect's attention.

### Hub-only-by-construction organs — explicitly NOT findings
`doc_claims` and `git_backlog_drift` report `hub-only — skipped (not the hub repo)` on every consumer's `state.yaml` (`ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`, `win-tooling` all show this identical line for both checks). Per prior fleet-census doctrine this is by-construction, not a coverage gap — not reported as a finding here.

### Everything else in the walk
The remaining `183 at-parity` + `19 pass-declared` + `0 must-absent` + `0 tombstone-violated` + `0 advisory-rewarn` + `0 refused` lines are either clean matches or the hub's own long-standing declared divergences (`.methodology.yaml` PASS-declared entries: `command-changelog-review`, `command-handoff`, `command-save`, `hub-hermetization-rule-a`, `hub-hermetization-rule-b-grammar`, `root-sweep` × 6 top-level entries, `ruff-gate`, `token-log`) — all independently readable in the hub's own committed `.methodology.yaml`, no reproduction risk since the hub's own governance files are what's being read, on a clean working tree.

---

## Live-concurrency addendum (observed during this census, not caused by it)

While this census was running, the hub's `claude/night-2026-07-30-boot-prep` branch **HEAD moved**: it was `c8490c1d` at census start (used throughout §A/§D above) and had advanced to `05a89378` — "docs(audits): night-batch W1 ruling dossier + W3 assemble_paste test-gap review" — by the time this file was being written, with a staged-then-cleared `docs/audits/2026-07-30-*` add/modify transiently visible on `git status --porcelain` mid-run. The commit subject names sibling workers "W1"/"W3", consistent with this being part of the same orchestrated multi-worker night-batch this census ("W2") belongs to, not an unrelated intrusion. No git command in this session wrote, staged, or committed anything — all such activity was external/concurrent. **Practical implication for the architect:** treat the `.dev-knowledge` HEAD SHA/subject in §A as a point-in-time snapshot only; re-run `git log -1 --oneline` on boot to get the true current HEAD before relying on it.

## Notes on what was NOT checked
- Installed `claude-code`/`codex` CLI versions vs `tool-versions.yaml`'s reviewed-version fields — not run (self-referential risk / out of scope for a git-repo sweep).
- `.claude/CLAUDE-FLOOR.md.sha256` sidecar hashes were **not independently recomputed** against their `.md` files in any repo (all 4 repos that carry the floor — ai-council, corp-monorepo, corp-sca-time-automation, and the hub's own template source — report the identical sidecar value `4d268f329a7edc8dc95a1c8fded9bdf8244ad8de60be69bf8e250a9b15a8111f`; this identical-hash-everywhere pattern is consistent with an unmodified floor fleet-wide, but was not verified by an actual `sha256sum` run).
- `audit.py run`/`ship-gate` full execution was not run fresh in this session — the `ecosystem/<repo>/state.yaml` pointers read in §C/§D all carry `last_audit: '2026-07-30'`, i.e. they are same-day but were **not regenerated by this census** and their exact generating branch/context was not independently re-verified beyond the direct file reads performed for each specific finding above.
- corp-monorepo's `docs/audits/2026-07-05-deep-rfp.md`-referenced RFP knowledge-base corpus (a large population of `kb-*.md` files, each reportedly carrying its own `last_reviewed` stamp) was **not individually enumerated** — flagged by the corp-monorepo subagent as a known large population outside this sweep's practical scope.
