<!-- scope: meta -->
# Process / Trigger / Usage Audit — 2026-06-25

**Date:** 2026-06-25
**Author:** Claude Code (Opus 4.8 main loop), operator Rob
**Branch:** `docs/process-trigger-usage-audit` (off `main`)
**Nature:** **STRICTLY READ-ONLY.** Nothing was edited, rewired, retired, or "fixed." The only write is this report. Dead/dormant components are *recorded*, not touched. Every row carries evidence (git SHA / artifact path + mtime / JOURNAL line / a directly-observed system-reminder).
**Audit B** in the multi-prompt audit batch — the process-infrastructure leg (skills · commands · hooks · workflow · agents). Successor to `docs/audits/2026-06-05-machinery-inventory.md` (that one inventoried; this one verdicts *liveness*).

**Method / vantage:**
- Four parallel read-only sub-agents gathered evidence (local+user inventory & wiring · hook-script liveness · git-archaeology usage · cross-repo vantage); the main loop spot-verified every high-stakes "dormant/dead" claim directly before writing.
- **Direct firing evidence this session:** the SessionStart system-reminders observed at boot prove three hooks fired live — `[changelog] claude-code 2.1.190 > last reviewed 2.1.177` (`changelog_sentinel.py`), `[closures] 19 closure(s) proposed` (`surface-closures.ps1`), `[fleet] 2 issue(s) in 5 repos as of 2026-06-25` (`fleet_health.py`). These are PROVEN-firing, not inferred.
- **Vantage:** full read access to sibling repos under `Dev/` (`ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`, `dev-knowledge-138`, `terminal-setup`, `illustrated-book-gen`). `corp-by-os` is **not a separate repo** (see §6).
- **Could not reach (none blocking):** `~/.codex/` runtime sqlite/history internals; ai-council transcript bodies / API telemetry; whether `pre-commit install --hook-type pre-push` ran on this clone (reachability caveat for `block-ff-push`, §3/§5). OneDrive + `automation/fleet-audit` paths deliberately untouched.

---

## 0. Headline — liveness at a glance

**The process infrastructure is genuinely exercised.** Of the operator's five named worries, three are confirmed LIVE and well-used; two are the real concerns:

| Operator worry | Verdict | One-line proof |
|---|---|---|
| **codex-review** "no usage in a long time?" | **DORMANT (~8–9 days)** — but proven heavily-used before | last artifact `docs/audits/2026-06-17-codex-coherence-integration.md`; corp-monorepo last run `6cd225f` 2026-06-16 |
| **check-against-spec** "ever used?" | **BUILT-NEVER-USED** (wired + backed by working code, but **zero invocations**) | defined `89f7140` 2026-06-17; no commit body in all history carries its verdict-checklist signature |
| **lifecycle hooks** "firing?" | **LIVE** | `propose_closures` daily → `PROPOSALS-2026-06-24.md`; `surface-closures` fired THIS session ([closures] 19); Stop-gate + immutability guard armed |
| **the workflow engine** "used?" | **LIVE** (nightly) | conformance digest `72b714e` 2026-06-24 on `automation/conformance-digest`, unbroken 06-15→06-24 — runs via spec-orchestration fallback, not the native launcher |
| **the agents** "used?" | **LIVE** | `artifact-reader` last 2026-06-24 (JOURNAL); ai-council debate panel last run 2026-06-23 (`council-out-20260623_…`) |

**Bucketed (full table in §5):**
- **LIVE (wired + recent/continuous use):** `/ship`, `/save`, `propose_closures` + `surface-closures`, `conformance-hub.js` (nightly), `fleet_health`, `coherence_nudge`, `audit-health`/ship-gate, the pre-commit gates (`ruff`, `validate-backlog`, `codemap`/`toc-freshness`, `normalize-dated-headers`, `backlog-id-on-close`), `session_end_backpressure` (Stop-gate), `block_immutable_edits`, `artifact-reader`, `/session-summary`, `/handoff`, `changelog_sentinel`, `gotchas`, hub-local `verify`, `git-discipline`, `/review-closures`, ai-council.
- **DORMANT (wired, no recent use — some by design):** `codex-review` (~8–9 d), `/changelog-review` (~10 d, push-triggered = idle by design), `/handoff` (~4 d), `/override` (**never used** — escape hatch, *expected* idle).
- **BUILT-NEVER-USED:** `check-against-spec` (the single clearest "built-and-forgotten" finding — though armed, not broken).
- **DEAD / STALE (doc or artifact, not a live component):** CLAUDE.md §8's user-level `verify` skill entry (archived; stale claim); `ecosystem/conformance.md` absent (ADR-86 says not-before-#171 — expected); `dev-knowledge-138/` empty orphan dir (critical-rule-#9 cleanup target).
- **BROKEN:** none found. One unconfirmable reachability caveat: `block-ff-push` fires only if `pre-commit install --hook-type pre-push` was run on this clone (can't verify read-only; `no_ff_merges` audit WARN is the backstop either way).

---

## 1. Inventory — every process component

### 1a. Local `.claude/` (hub-resident)
| Component | Type | Path | Supposed to do | Invoked by |
|---|---|---|---|---|
| `verify` | skill | `.claude/skills/verify/SKILL.md` (+`verify.py`) | pytest + ruff + git-status cadence, 3-line pass/fail; FAIL blocks the step | operator/CC after each numbered step |
| `check-against-spec` | skill | `.claude/skills/check-against-spec/SKILL.md` | reconcile a dependent doc when its spec version bumps: run `coherence_enumerator.py`, verdict each site (`stale\|fine\|not-relevant`), write checklist into the re-stamp commit | operator/CC, manually, on a spec bump |
| `/save` | command | `.claude/commands/save.md` | Conventional-Commits commit workflow w/ required body; never skip hooks | operator (`/save`) |
| `/handoff` | command | `.claude/commands/handoff.md` | generate/complete a handoff per `HANDOFF_PROCESS.md` v5 (ADR-82) | operator (NL triggers) |
| `/changelog-review` | command | `.claude/commands/changelog-review.md` | review claude-code+codex changelogs since `last_reviewed`, classify, write digest, bump state | operator (PUSH only) |
| `/override` | command | `.claude/commands/override.md` | the only escape from the ADR-85 Stop-gate; logs to `logs/OVERRIDES.md`, writes HEAD-bound token | operator, when the gate is wrong |
| `artifact-reader` | agent | `.claude/agents/artifact-reader.md` | read-only subagent (Sonnet; Read/Grep/Glob) summarizing >20k-token artifacts with line-cited quotes | CC via Agent/Task tool |
| `conformance-hub.js` | workflow | `.claude/workflows/conformance-hub.js` | 3-stage read-only conformance review (3 Sonnet verifiers → Opus skeptic → Opus digest), code-owned counts contract | `Workflow` tool locally; nightly cloud Routine |
| `git-discipline.md` | rule | `.claude/rules/git-discipline.md` | commit after every edit; clean tree at session end (`verify:` line) | auto-loaded project rule |

### 1b. User-level `~/.claude/`
| Component | Type | Path | State |
|---|---|---|---|
| `/codex-review` | command | `~/.claude/commands/codex-review.md` (+ `~/.claude/bin/codex-review.ps1`) | LIVE — **no skill form** (the session picker lists the command, not a separate skill) |
| `/session-summary` | command | `~/.claude/commands/session-summary.md` | LIVE |
| `gotchas` | skill | `~/.claude/skills/gotchas/` | LIVE — auto-consulted before edits |
| `verify` | skill | **archived** `~/.claude/archive/2026-06-05-machinery-c3/skills/verify/` | **ARCHIVED** — live `~/.claude/skills/` holds only `gotchas`; the live `verify` is hub-local (1a) |
| `/boot` | command | **archived** `~/.claude/archive/2026-06-05-machinery-c3/commands/boot.md` | ARCHIVED (correctly labeled in CLAUDE.md) |
| `/evolve` | command | **archived** `~/.claude/archive/2026-06-05-machinery-c3/commands/evolve.md` | ARCHIVED (correctly labeled) |

### 1c. Plugin `tier1-lifecycle@dev-knowledge-methodology` (ENABLED)
Layout: `plugins/tier1-lifecycle/{.claude-plugin/plugin.json (v0.1.10), hooks/hooks.json, commands/{review-closures,ship}.md, scripts/{propose_closures,review_closures,validate_backlog}.py, assets/ruff-pre-commit.yaml, INSTALL.md}`. Marketplace: `./.claude-plugin/marketplace.json` (`dev-knowledge-methodology`). Ships: **(1)** a Stop hook → `propose_closures.py`; **(2)** `/review-closures`; **(3)** `/ship`; **(4)** a ruff pre-commit asset. Deliberately **no** SessionStart hook (plugin SessionStart hooks register too late to fire — verified 2026-06-02; surfacing is delegated to the global hook).

### 1d. Hooks
**Pre-commit (`.pre-commit-config.yaml`):** `normalize-dated-headers`, `codemap-freshness`, `toc-freshness`, `toc-freshness-playbook`, `validate-backlog`, `audit-health` (gate), `ruff` (gate), `coherence-nudge` (nudge), `backlog-id-on-close` (commit-msg stage), `block-ff-push` (pre-push stage).
**Project session hooks (`.claude/settings.json`):** `Stop` → `session_end_backpressure.py`; `PreToolUse` (Edit/Write/etc.) → `scripts/hooks/block_immutable_edits.py`; `SessionStart` → `fleet_health.py`, `surface_triage.ps1`, `billing_leak_sentinel.ps1`, `changelog_sentinel.py`.
**Plugin Stop hook:** `${CLAUDE_PLUGIN_ROOT}/scripts/propose_closures.py` (the plugin's own copy; byte-identical carrier of the repo-root source per ADR-78).
**User-level `~/.claude` hooks (merge, don't replace):** `PreToolUse` (Bash/PowerShell) → `block-onedrive.ps1`; `SessionStart` → `surface-closures.ps1` (the closure-surfacing partner to the plugin's detect-only Stop hook — the "5c convergence"); `Stop`/`Notification` → `claude-notify.ps1` (desktop notify, not a governance organ).

### 1e. Cross-repo (detail in §6)
`corp-monorepo` (codex output artifacts; tooling is global `~/.codex/`), `ai-council` (the debate-panel CLI), `corp-by-os` (= the runtime app-name of the engine **inside** corp-monorepo, not a repo).

---

## 2. Wiring check — WIRED vs ORPHANED

**No live, hub-resident component is orphaned.** The central wiring registry is `ARCHITECTURE.md` Ch2 organ map (lines ~196–218); `CLAUDE.md` §7–§9 mirrors it. Cites:

| Component | Wired? | Wiring site |
|---|---|---|
| `verify` (hub) | WIRED | ARCHITECTURE.md organ map; CLAUDE.md §8 |
| `check-against-spec` | WIRED (doc) — **but not gate-fired by design** (v1 scope: "do not wire the ship-gate") | CLAUDE.md §8; backed by `scripts/coherence_enumerator.py` (+ `tests/test_coherence_integration.py`) |
| `/save`, `/handoff`, `/changelog-review`, `/override` | WIRED | CLAUDE.md §7; ARCHITECTURE organ map; `/changelog-review` also nudged by `changelog_sentinel` (settings.json) |
| `artifact-reader` | WIRED | ARCHITECTURE organ map (#97); selectable subagent this session |
| `conformance-hub.js` | WIRED (most-wired) | `settings.json` `//permissions` note; ARCHITECTURE; CONTRIBUTING; PLAYBOOK; consumed by `.github/workflows/nightly-conformance-triage.yml` (parses its counts marker) |
| `git-discipline.md` | WIRED | CLAUDE.md §9 |
| `/codex-review` | WIRED | CLAUDE.md §7; ARCHITECTURE (L0, ADR-54) — **no skill form exists** |
| `/session-summary`, `gotchas` | WIRED | CLAUDE.md §7/§8; global CLAUDE.md "check gotchas before editing" |
| `tier1-lifecycle` + `/review-closures` + `/ship` | WIRED (ENABLED) | `settings.json` `enabledPlugins` + `extraKnownMarketplaces`; CLAUDE.md §7/§8 |
| every hook in 1d | WIRED | `.pre-commit-config.yaml` / `.claude/settings.json` / plugin `hooks.json` / `~/.claude/settings.json` |

**Stale / drift wiring (recorded, not fixed):**
1. **CLAUDE.md §8 lists a user-level `verify` skill** that no longer lives there (archived 2026-06-05; the live one is hub-local). Same §8 line 125 correctly attributes `verify` to `.claude/skills/` — an internal self-contradiction. **Doc drift, not a component failure.**
2. **`check-against-spec` is doc-wired but never gate-wired** (intentional, per its own v1 scope) — so its only trigger is manual, which is why it has never fired (§4).

---

## 3. Trigger-flow map (in sequence)

**On SESSION START** (project hooks fire in listed order; user-level hooks merge):
1. `fleet_health.py` → daily-throttled cross-repo `audit.py run`; writes `logs/FLEET-HEALTH.md` + `ecosystem/<repo>/state.yaml` → prints `[fleet] …` ✅ *fired this session*
2. `surface_triage.ps1` → gh-auth / open nightly-triage issues / failed run / missing digest (fail-soft)
3. `billing_leak_sentinel.ps1` → WARN if `ANTHROPIC_API_KEY` visible (Max→API leak)
4. `changelog_sentinel.py` → compares installed `claude`/`codex` vs `ecosystem/tool-versions.yaml` → prints `[changelog] …` ✅ *fired this session*
5. (user-level) `surface-closures.ps1` → counts unchecked items in `logs/PROPOSALS-*.md` → prints `[closures] N …` ✅ *fired this session (19)*

**On EACH tool use:** `PreToolUse` Edit/Write/etc. → `block_immutable_edits.py` (fail-closed inside `docs/decisions/transcripts/**`, fail-open elsewhere); Bash/PowerShell → user `block-onedrive.ps1`.

**On EACH turn-end (Stop):** (a) `session_end_backpressure.py` — ADR-85 gate: **hard-block** on an un-anchored JOURNAL commit-SHA, advisory on backlog/dirty/cadence legs, fail-soft on its own errors; (b) plugin `propose_closures.py` → writes `logs/PROPOSALS-<today>.md` (detect-only, never mutates BACKLOG, exit 0).

**On COMMIT (`git commit` / `/save`):**
- *pre-commit stage* → `normalize-dated-headers` (auto-format) · `codemap-freshness` (gate) · `toc-freshness` + `toc-freshness-playbook` (gate) · `validate-backlog` (gate) · `audit-health` (**gate** — `audit.py health`, exit 1 on FAIL) · `ruff` (**gate**) · `coherence-nudge` (nudge, always exit 0, appends `logs/coherence-nudge.log`)
- *commit-msg stage* → `backlog-id-on-close` (gate — require `[#id]` when a task is removed)

**On PUSH:** *pre-push stage* → `block-ff-push` (gate — refuses a non-merge commit on main's first-parent spine; fail-soft to 0 on git error). ⚠️ **Only reached if `pre-commit install --hook-type pre-push` ran on this clone** — unverifiable read-only.

**On `/ship` (git-finish):** refuse-in-worktree → refuse-on-main → refuse-dirty → `pytest -x && ruff check` → `audit.py ship-gate` (hub-only) → `--no-ff` merge → push → delete branch. (Push then re-triggers `block-ff-push`, which passes a `--no-ff` merge.)

**Nightly cloud Routine (conformance):** attempt native `Workflow` launcher → **fall back to spec-orchestration** (read `conformance-hub.js` as a spec, run its 3 stages via read-only Explore agents) → commit digest to `automation/conformance-digest` branch → `nightly-conformance-triage.yml` parses the code-owned counts marker, opens/diverts a PR. *(Native launcher is disabled in cloud, so this path is the live one; each run re-probes native first.)*

**No registered hook is unreachable** except the noted `block-ff-push` install caveat. No "expected trigger with no wiring" found.

---

## 4. Usage evidence (per component)

| # | Component | Last used | Citation | Confidence |
|---|---|---|---|---|
| 1 | **codex-review** (.dev-knowledge) | **2026-06-17** | `docs/audits/2026-06-17-codex-coherence-integration.md` (dense Mar→Jun 17, then cold) | PROVEN-invoked; dormant ~8 d |
| 2 | **check-against-spec** | **NEVER** | defined `89f7140` 2026-06-17; grep for its `not-relevant`/`transclusion-candidate` checklist across all history hits only the *defining* commits | PROVEN never-invoked |
| 3 | **conformance-hub.js** | **2026-06-24** | digest `72b714e` on `automation/conformance-digest` (unbroken 06-15→06-24); `nightly-conformance-triage.yml` last edit `99db0e0` 06-14 | PROVEN-active (most consistent automated flow) |
| 4 | **artifact-reader** | **2026-06-24** | JOURNAL (two overnight audits delegated the JOURNAL tail to it); defined `f8bbf1c` 06-06 (#97) | PROVEN-invoked, recent |
| 5 | **propose_closures.py** | **2026-06-24** | `logs/PROPOSALS-2026-06-24.md` (daily unbroken 06-02→06-24); this session surfaced 19 | PROVEN-active (daily) |
| 6 | **/review-closures** | **2026-06-19** | `10c94ae` "close [#187] [#186] [#140] via /review-closures" | PROVEN-invoked (episodic, operator-gated) |
| 7 | **/ship** | **2026-06-24** | multiple `--no-ff` merges (`4a0e6d1`, `8a695b9`, `cf2d858`…); first-parent spine is an unbroken merge wall | PROVEN-active (daily) |
| 8 | **/handoff** | **2026-06-21** | newest bundle `docs/handoffs/2026-06-21-dev-knowledge-architect/` | PROVEN-active; idle ~4 d |
| 9 | **/save** | continuous | every commit follows its Conventional-Commits+body fingerprint | PROVEN (indirect, by design) |
| 10 | **/session-summary** | **2026-06-23** | newest `logs/TOKEN-LOG.md` entry `## 2026-06-23` (`766428a`) | PROVEN-invoked (weekly cadence) |
| 11 | **/changelog-review** | **2026-06-15** | `docs/audits/2026-06-15-changelog-review.md` (`3ddaf6d`); `tool-versions.yaml` bumped same day | PROVEN; idle ~10 d (push-triggered = expected) |
| 12 | **/override** | **NEVER** | `logs/OVERRIDES.md` does not exist in the working tree (gate never escaped) | PROVEN never-used (expected — escape hatch) |
| 13 | **fleet_health.py** | **2026-06-25** | `logs/FLEET-HEALTH.md` `completed_at: 2026-06-25T00:23:15` | PROVEN — ran today |
| 14 | **coherence_nudge.py** | **2026-06-25** | `logs/coherence-nudge.log` last line `2026-06-25T00:22:33 …HANDOFF_PROCESS.md version=5.2` | PROVEN — fired today |
| 15 | **changelog_sentinel.py** | **2026-06-25** | `[changelog] claude-code 2.1.190 > last reviewed 2.1.177` reminder observed at boot | PROVEN — fired this session |
| 16 | **gotchas / verify(hub) / git-discipline / pre-commit gates** | continuous | gotchas auto-consulted; `audit-health`/`ruff`/TOC/backlog gates run on every commit (clean tree = passing) | PROVEN (continuous, by construction) |
| 17 | **session_end_backpressure / block_immutable_edits / block_ff_push** | n/a — pure gates | no artifact trail by design; indirect: clean `--no-ff`-only first-parent spine + no in-place transcript edits are consistent with them working | ASSUMED (correct behavior is silence) |

`ecosystem/conformance.md` **does not exist** (ADR-86's planned location; "the build (#171), not before" — so its absence is per-spec, not a failure).

---

## 5. Liveness verdict (per component) — the headline table

Verdict ∈ LIVE (wired + recent use) · DORMANT (wired, no recent use) · DEAD (not wired / archived) · BROKEN (wired but fails).

| Component | Defined where | Wired? | Last used | Verdict |
|---|---|---|---|---|
| `/ship` (plugin) | `plugins/tier1-lifecycle/commands/ship.md` | YES | 2026-06-24 | **LIVE** |
| `/save` | `.claude/commands/save.md` | YES | continuous | **LIVE** |
| `propose_closures.py` (plugin Stop) | `plugins/tier1-lifecycle/scripts/` | YES | 2026-06-24 | **LIVE** |
| `surface-closures.ps1` (user SessionStart) | `~/.claude/hooks/` | YES | 2026-06-25 (this session) | **LIVE** |
| `conformance-hub.js` (workflow) | `.claude/workflows/conformance-hub.js` | YES | 2026-06-24 | **LIVE** (via spec-orchestration fallback) |
| `fleet_health.py` (SessionStart) | `scripts/fleet_health.py` | YES | 2026-06-25 | **LIVE** |
| `coherence_nudge.py` (pre-commit) | `scripts/coherence_nudge.py` | YES | 2026-06-25 | **LIVE** |
| `changelog_sentinel.py` (SessionStart) | `scripts/changelog_sentinel.py` | YES | 2026-06-25 | **LIVE** |
| `audit-health` / ship-gate (`audit.py`) | `scripts/audit.py` | YES | every commit / ship | **LIVE** |
| `ruff` · `validate-backlog` · `codemap`/`toc-freshness` · `normalize-dated-headers` · `backlog-id-on-close` | `.pre-commit-config.yaml` + `scripts/` | YES | every commit | **LIVE** |
| `session_end_backpressure.py` (Stop-gate) | `scripts/session_end_backpressure.py` | YES | per turn (gate) | **LIVE** (silent gate) |
| `block_immutable_edits.py` (PreToolUse) | `scripts/hooks/block_immutable_edits.py` | YES | per edit (gate) | **LIVE** (silent gate) |
| `artifact-reader` (agent) | `.claude/agents/artifact-reader.md` | YES | 2026-06-24 | **LIVE** |
| `/session-summary` | `~/.claude/commands/session-summary.md` | YES | 2026-06-23 | **LIVE** (weekly) |
| `/review-closures` (plugin) | `plugins/tier1-lifecycle/commands/review-closures.md` | YES | 2026-06-19 | **LIVE** (episodic) |
| `gotchas` (skill) | `~/.claude/skills/gotchas/` | YES | continuous | **LIVE** |
| `verify` (hub skill) | `.claude/skills/verify/` | YES | per numbered step | **LIVE** |
| `git-discipline.md` (rule) | `.claude/rules/git-discipline.md` | YES | continuous | **LIVE** |
| `ai-council` (debate panel) | `Dev/ai-council` (CLI) | YES | 2026-06-23 | **LIVE** (cross-repo, §6) |
| `/handoff` | `.claude/commands/handoff.md` | YES | 2026-06-21 | **DORMANT (~4 d)** — execution arcs, not handoff sessions |
| `codex-review` | `~/.claude/commands/` + `bin/codex-review.ps1` | YES | 2026-06-17 (hub) / 06-16 (corp-monorepo) | **DORMANT (~8–9 d)** |
| `/changelog-review` | `.claude/commands/changelog-review.md` | YES | 2026-06-15 | **DORMANT (~10 d)** — push-triggered, idle by design |
| `/override` | `.claude/commands/override.md` | YES | never | **DORMANT** — escape hatch, idle *expected* |
| `block-ff-push` (pre-push) | `scripts/block_ff_push.py` | YES (config) | unverifiable | **LIVE-if-installed** — reachability caveat (§3) |
| **`check-against-spec`** | `.claude/skills/check-against-spec/SKILL.md` | YES (doc; not gate-fired) | **never** | **BUILT-NEVER-USED** — armed, not broken |
| `verify` (user skill) | archived `~/.claude/archive/2026-06-05-machinery-c3/` | NO | — | **DEAD/ARCHIVED** — but CLAUDE.md §8 still claims it (stale doc) |
| `/boot`, `/evolve` | archived `~/.claude/archive/2026-06-05-machinery-c3/` | NO | — | **DEAD/ARCHIVED** (correctly labeled) |
| `ecosystem/conformance.md` | (planned, ADR-86) | n/a | never built | **NOT-YET-BUILT** (#171; per-spec absence) |
| `dev-knowledge-138/` | `Dev/dev-knowledge-138` (empty dir) | NO | — | **DEAD ORPHAN** — critical-rule-#9 cleanup target |

**No BROKEN component found.** All backing scripts exist, import cleanly (verified `find_violations`/`format_one`/`BASELINE_DATE`/`_git` and `_SPEC_REGISTRY`/`spec_version_numeric`/`SpecSource` all resolve), and ruff is 0.15.5 (meets the `>=0.15.5` floor).

---

## 6. Cross-repo components

I have vantage on the siblings, so these are audited (not deferred), each marked with its repo.

| Component | Repo | What's there | Wired? | Last usage | Verdict |
|---|---|---|---|---|---|
| **codex-review / Codex CLI** | `corp-monorepo` | NO in-repo tooling — only output artifacts in `docs/audits/*codex*.md` (2026-03-30 → 04-21 → 06-03 → **06-16**); reviewer config is **global** `~/.codex/AGENTS.md` (ADR-54), hub source `.dev-knowledge/codex/AGENTS.md` | Not in-repo (external/global by design) | `6cd225f` 2026-06-16 ("4 HIGH, fixed all four") | **LIVE-external** (manual, ~monthly) |
| **agents / debate panel** | `ai-council` | real installed CLI (`council`/`ai-council` → `ai_council.cli:main`); `debate.py` parallel-model + blind-voting (ADR-03); 5 providers; 5-model panel config; `target_projects:[.dev-knowledge]` | YES (standalone CLI, 3 invocation modes) | `council-out-20260623_204026-pick-…` 2026-06-23; 165 transcripts; inbox drained; cross-repo transcript loop confirmed into the hub | **LIVE** (near-daily) |
| **workflow engine** | `corp-by-os` → **resolves to `corp-monorepo`** | **No `corp-by-os` directory exists** under `Dev/`. `corp-by-os` is the runtime *app-name* of the engine inside corp-monorepo (`src/corp/ops/`, `src/corp/overnight/`; runtime DBs `%LOCALAPPDATA%/corp-by-os/*.db`; `task_manager` tags `"source_tool":"corp-by-os"`) | n/a | — | **OUT-OF-VANTAGE as a standalone repo** (none exists); engine itself reachable in corp-monorepo — needs a dedicated corp-monorepo `src/corp/ops` pass if the operator wants its internals audited |

**Sibling process-machinery scan:** `corp-ops` (tier1-lifecycle **installed**, `.claude/`, last commit 2026-06-02) · `corp-sca-time-automation` (tier1-lifecycle **installed**, full pre-commit + CLAUDE-FLOOR + sha256 floor guard, 2026-06-08) · `terminal-setup` (dormant 4 mo, not a machinery node) · `illustrated-book-gen` (not a git repo, out of scope) · **`dev-knowledge-138`** (empty dir, no `.git`, not in `git worktree list` — a stale/abandoned issue-clone shell matching the `.dev-knowledge-*` orphan pattern; recorded, not removed).

**Could / couldn't reach:** reached & confirmed all of the above via git/JOURNAL/filenames. Couldn't reach `~/.codex/` sqlite history internals or ai-council transcript bodies (outside repo scope, not blocking). One initial `grep -r` over all of `Dev/` was correctly blocked by the OneDrive P0 guard and re-scoped to per-repo Grep.

---

## 7. Honest verdict

**The process infrastructure is genuinely exercised — it is not a graveyard of built-and-forgotten machinery.** The automated spine (pre-commit gates, the Stop-gate, the immutability guard, `propose_closures`/`surface-closures`, `fleet_health`, `coherence_nudge`, the nightly conformance workflow) is demonstrably firing — several pieces *today* (2026-06-25), proven by artifact mtimes and the boot system-reminders, not assumed. The human-gated spine (`/ship`, `/save`, `/review-closures`, `/session-summary`, `/handoff`, `artifact-reader`) shows continuous-to-recent use. ai-council's debate panel is near-daily.

**Of the operator's five specific worries:**
- **codex-review — CONFIRMED dormant (~8–9 days), but the framing matters.** It was used *heavily* (≈29 hub artifacts Mar→Jun-17, last corp-monorepo run 06-16). It went quiet as the tail of the 2026-06-17 coherence-spine build arc wound down — a lapsed-since-a-push, not a never-adopted tool. Still LIVE-capable.
- **check-against-spec — CONFIRMED the one true "built-and-forgotten" case.** Defined 2026-06-17 and **never once invoked**; no commit in all of history carries its verdict-checklist signature. Crucially it is *armed, not broken* — it's wired in the docs and its deterministic backing (`coherence_enumerator.py`) exists and is tested; it simply has only a manual trigger and a spec bump hasn't driven a reconciliation through it yet. This is the strongest candidate for the operator's attention: either exercise it on the next spec bump, or decide it was speculative and retire it.
- **lifecycle hooks — CONFIRMED LIVE.** Firing daily/per-session; one fired in this very session's boot.
- **the workflow engine — CONFIRMED LIVE** (nightly digest 06-24), with the honest caveat that it runs via **spec-orchestration**, because the native `Workflow` launcher is disabled in the cloud context; the script's in-process guarantees are inert on that path and the count-contract backstop lives in the GitHub Action parser instead.
- **the agents — CONFIRMED LIVE** (`artifact-reader` 06-24; ai-council 06-23).

**PROVEN vs ASSUMED:** everything with an artifact/SHA/observed-reminder above is PROVEN. The only ASSUMED rows are the three pure gates (`session_end_backpressure`, `block_immutable_edits`, `block_ff_push`) — by nature they leave no trail, so liveness is inferred from the clean `--no-ff`-only spine and the absence of in-place transcript edits; and `block-ff-push` carries an unconfirmable-read-only install caveat.

**Recorded (not fixed, per the read-only contract):**
1. `check-against-spec` — built, wired, never invoked.
2. CLAUDE.md §8 stale user-level `verify`-skill claim (archived; live copy is hub-local) — minor self-contradiction within §8.
3. `dev-knowledge-138/` empty orphan directory (critical-rule-#9 cleanup target).
4. `codex-review` and `/changelog-review` dormancy (the latter is by-design idle).
5. `ecosystem/conformance.md` absent — expected per ADR-86 (#171 unbuilt), noted only because it was a named target.

None of these are breakage; they are a small, legible set of dormant/stale items against a process spine that is otherwise live and well-exercised.

---

*End of audit. Read-only — no component, source, config, hook, command, skill, or existing doc was modified. This report is the only artifact.*
