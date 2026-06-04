<!-- scope: meta -->
# Runtime Machinery Inventory — 2026-06-05

**Date:** 2026-06-05
**Author:** Claude Code (Opus 4.8 main loop), operator Rob
**Branch:** `docs/machinery-inventory`
**Phase:** C recon
**Nature:** **READ-ONLY recon. Facts only — no judgments, no deletions, no machinery modified.** Every row carries evidence (file mtimes, log traces, JOURNAL/LESSONS references, content staleness, diff output). FLAGS columns record observable signals (stale / orphaned / duplicated / missing), not recommendations.

**Scope surveyed:** `~/.claude/` runtime config (commands, skills, hooks, settings, memory, rules, plans) + the hub repo's own runtime (`.claude/`, `plugins/`, marketplace) + toolchain presence. Evidence-gathering by three parallel read-only Explore subagents; consolidated here.

**Method caveat:** session-log "evidence of use" was **sampled** (grep over a subset of `~/.claude/projects/` transcripts), not exhaustively mined. Hit counts are lower-bounds, not totals.

---

## 1 — Slash commands (`~/.claude/commands/`)

| ITEM | DECLARED ROLE | EVIDENCE OF USE | LAST TOUCHED | FLAGS |
|---|---|---|---|---|
| `boot.md` | Session boot sequence — load memory, verify rules, check trends; "Run at the start of every session" | Sampled transcripts: ~9 references across two recent `.jsonl` session files | 2026-03-29 04:10 | Auto/start command; tied to memory+learned-rules system. No staleness in content. |
| `evolve.md` (3.38 KB) | Evolution audit — review corrections/observations/learned-rules; propose promotions/prunings/graduations; "weekly or every ~10 sessions" | Sampled transcripts: ~8 references | 2026-03-29 16:45 | Depends on the memory `.jsonl` files — **which do not exist** (see §5). Operates on empty inputs. |
| `session-summary.md` (2.96 KB) | Token-efficient summary of THIS session (commits/changes/decisions/pending) for pasting into browser chat | Sampled transcripts: ~3 references | 2026-04-27 23:59 | Explicitly invoked. Contains fallback logic for missing ccusage fields (graceful-degradation present). |
| `codex-review.md` (2.23 KB) | Invoke Codex review against current-branch **code** diff (or full audit); code-extension allowlist + empty-diff guard | Sampled transcripts: ~3 references | 2026-05-19 13:07 | Newest command file; used within ~2 weeks. Declares dependency on `scripts/render-diagrams.ps1`. |

**Note:** the repo-level commands (`/save`, `/handoff`) and the plugin-provided `/review-closures` live elsewhere and are surveyed in §6, not here.

---

## 2 — Skills (`~/.claude/skills/`)

| ITEM | DECLARED ROLE | EVIDENCE OF USE | LAST TOUCHED | FLAGS |
|---|---|---|---|---|
| `gotchas` (gotchas.md 14.98 KB + SKILL.md 0.22 KB) | Auto-loaded. "Universal development gotchas for Python/Claude Code projects. Encoding traps, shell safety, test framework pitfalls." | 16 entries; internal "Last triggered" stamps range 2026-03-25 → **2026-06-04** (today's: Haiku routing, session-deny hot-reload, Dynamic-Workflow subagent write-bypass) | gotchas.md **2026-06-04 12:04** / SKILL.md 2026-03-30 01:50 | **Most recently touched item in the whole survey.** Actively maintained living library. No staleness. |
| `verify` (cross-repo-boundaries.ps1 2.86 KB + SKILL.md 0.16 KB) | Explicitly invoked. "Domain-specific verification scripts for the Corporate OS ecosystem. Run after pytest." Checks corp-monorepo package boundaries (CKE, corp-by-os, corp-os-meta). | No transcript hits in the sampled logs; script header "Last validated: 2026-03-28"; no internal last-triggered stamp | ps1 2026-03-28 16:57 / SKILL.md 2026-03-24 21:51 | **STALE / low-signal** — untouched ~2.5 months; targets a monorepo layout that may have moved; no sampled invocation evidence. |

---

## 3 — Global hooks + settings (`~/.claude/settings.json`, last modified 2026-03-26)

| ITEM | DECLARED ROLE | EVIDENCE OF USE | LAST TOUCHED | FLAGS |
|---|---|---|---|---|
| **PreToolUse** (Bash) → `hooks/block-onedrive.ps1` | Block any Bash command targeting an "OneDrive - Blue Yonder" path (P0 safety, core-invariants §1); exit 2 on match | Enforces the global P0 OneDrive rule; output is inline decision JSON (no log file) | settings 2026-03-26 | **Fail-HARD by design** (exit 2 on violation; pass-through exit 0). Intentional block, not fail-soft. |
| **SessionStart** echo (evolution banner) | Print learned-rules line-count + corrections count; "Run /boot" | Fires every session (visible this session); no persisted log | settings 2026-03-26 | Fail-soft (`2>/dev/null`, always exit 0). Reads `corrections.jsonl` which **does not exist** → reports 0. |
| **SessionStart** → `hooks/surface-closures.ps1` | Read `$CLAUDE_PROJECT_DIR/logs/PROPOSALS-*.md`, count open `- [ ] **#NN**`, nudge if >0 (Tier-1 L0 surfacing) | Self-contained; no plugin-cache dep; stdout only | settings 2026-03-26 | Fail-soft (whole body in try/catch, always exit 0). This is the L0 surfacer CLAUDE.md §9 references. |
| **Stop** → `claude-notify.ps1` | Audible session-end notification (Win32 idle check; chime vs beep) | Audio only; no log | 2026-03-26 | Fail-soft (swallows errors, exit 0). |
| **Stop** echo (evolution reminder) | Remind operator to log corrections/observations + write session scorecard | stdout only | settings 2026-03-26 | Fail-soft. Reminds writing to `.jsonl` files that are never created (see §5). |
| **env block** | `MAX_THINKING_TOKENS=10000`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=40`, `CLAUDE_CODE_SUBAGENT_MODEL=haiku`, `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL=1` | Active settings | n/a | `CLAUDE_CODE_SUBAGENT_MODEL=haiku` corroborates the "Haiku routing regardless of pinned model" gotcha noted in conformance digests. |

Other settings: cleanup period 90 days; default shell PowerShell; effort medium; dangerous-mode + auto-permission prompts skipped.

**Night-agent logs** (`~/.claude/night-agent/logs/`): 9 files, all dated 2026-06-01; latest `run-20260601-203043.log` (0.35 KB). **No runs logged since 2026-06-01** (3+ days dormant at survey time).

---

## 4 — Workflow duplication: global vs in-repo `conformance-hub.js`

| ITEM | DECLARED ROLE | EVIDENCE OF USE | LAST TOUCHED | FLAGS |
|---|---|---|---|---|
| **Global** `~/.claude/workflows/conformance-hub.js` (11,979 B) | Read-only 3-stage hub conformance review (V1 JOURNAL-vs-git, V2 living-doc claims, V3 BACKLOG closures → skeptic → digest) | Local Session fallback path | 2026-06-04 00:12:55 | **STALE** — hardcoded Windows path separators; **lacks** the V1 shallow-history guard. |
| **Repo** `.dev-knowledge/.claude/workflows/conformance-hub.js` (12,452 B) | Same, made Linux/cloud-portable; canonical SPEC for cloud spec-orchestration fallback | Nightly cloud Routine reads it as SPEC; local Session fallback | 2026-06-04 16:21:56 | **CURRENT / canonical** — cwd-relative paths + V1 shallow-history guard (+473 B). |

**Concrete diff (the repo copy is ahead by exactly these changes):**

1. **Path separators** — global uses Windows `REPO + '\\JOURNAL.md'`; repo uses portable `REPO + '/JOURNAL.md'`.
2. **New V1 shallow-history guard** inserted in the repo copy (absent in global), verbatim:
   > `SHALLOW-HISTORY GUARD: before flagging a JOURNAL entry commit SHA as absent, verify that SHA date falls within the available git history (the clone may be SHALLOW -- cloud clones start at the first push). SHAs older than the history boundary are OUT-OF-SCOPE, not findings.`
3. **Rationale (from JOURNAL 2026-06-04):** cloud clones are shallow; stale JOURNAL SHAs fall outside the boundary and were producing false "commit absent" findings. The guard suppresses them.

**State:** global copy is **16h behind** and **missing the guard** — duplicated artifact, repo copy authoritative.

---

## 5 — Memory, rules, plans

### 5a. `~/.claude/memory/`

| ITEM | DECLARED ROLE | EVIDENCE OF USE | LAST TOUCHED | FLAGS |
|---|---|---|---|---|
| `README.md` (1.61 KB, 26 ln) | Protocol spec for the memory harness (corrections/observations/sessions/violations/learned-rules/evolution-log formats + promotion ladder) | Documents the contract | 2026-03-29 16:09 | **STALE** — documents files that do not exist. |
| `learned-rules.md` (0.19 KB, 4 ln) | Graduated rules with `verify:` lines; loaded at /boot | Read by SessionStart echo + /boot | 2026-03-30 01:13 | **UNDERDEVELOPED** — 4 lines, no graduated rules. (SessionStart banner this session reported "6 lines".) |
| `evolution-log.md` (0.16 KB, 4 ln) | Audit trail of /evolve decisions | Header only | 2026-03-29 16:09 | **ORPHANED stub** — no decisions logged. |
| `corrections.jsonl` | Append-only correction log (per README + global CLAUDE.md Self-Evolution Protocol) | Referenced by SessionStart hook | — | **MISSING** — never created; protocol declared, not active. |
| `observations.jsonl` | Verified codebase discoveries | Referenced by README | — | **MISSING.** |
| `sessions.jsonl` | Per-session scorecards | Referenced by Stop hook | — | **MISSING.** |
| `violations.jsonl` | Rule violations caught at /boot | Referenced by README | — | **MISSING.** |

> **Cross-flag:** the global CLAUDE.md "Self-Evolution Protocol" + `/evolve` + both evolution echo-hooks all operate on this memory set; the four `.jsonl` sinks are **never written**, so the loop runs on empty/stub inputs. (Note: this is distinct from the *project auto-memory* at `~/.claude/projects/…/memory/MEMORY.md`, which IS populated — 3 entries + index.)

### 5b. `~/.claude/rules/`

| ITEM | DECLARED ROLE | EVIDENCE OF USE | LAST TOUCHED | FLAGS |
|---|---|---|---|---|
| `core-invariants.md` (1.95 KB) | 4 critical invariants (OneDrive exclusion, test-after-each-step, never-delete-without-asking, clean-tree-at-end); "loads on every context reset" | Invariant #1 directly enforced by the PreToolUse OneDrive hook (§3) | 2026-06-02 02:32 | **ACTIVE** — recently updated; hook-enforced. |

### 5c. `~/.claude/plans/`

| ITEM | DECLARED ROLE | EVIDENCE OF USE | LAST TOUCHED | FLAGS |
|---|---|---|---|---|
| **62 plan files total** | Auto-saved EnterPlanMode artifacts (random-slug names) | Accumulation only; no pruning observed | 2026-03-08 → **2026-06-04 12:36** | **UNMANAGED GROWTH** — no lifecycle/cleanup. |
| Recent cluster (6/3–6/4) | `phase-b-playful-backus.md` (12.23 KB, 6/4 12:36 — newest), `graphify-pilot-88-*`, `pilot-81-v0-*`, `corp-monorepo-baseline-*`, 5× `model-mode-*`, `phase-0-snuggly-penguin.md`, `buzzing-spinning-wombat.md` | Active working set | 2026-06-03 → 2026-06-04 | Current. `pilot-81-v0-*` likely superseded by `phase-b-*`. |
| Mid archive (4/21–5/25) | ~27 files: `cached-*`, `prompt-rollout-*`, `claude-code-prompt-*`, `backlog-md-reconciliation-pass-*` | — | 2026-04-21 → 2026-05-31 | **STALE ARCHIVE** — pre-date the recent series. |
| Oldest (3/8–3/30) | `squishy-sleeping-beaver.md`, `twinkling-rolling-manatee.md`, `elegant-munching-frost.md` | No references in recent repo docs | 2026-03-08 → 2026-03-30 | **ORPHAN CANDIDATES** — 2+ months old, unreferenced. |

---

## 6 — Hub-side runtime (repo `.dev-knowledge/`)

| ITEM | DECLARED ROLE | EVIDENCE OF USE | LAST TOUCHED | FLAGS |
|---|---|---|---|---|
| `.claude/settings.json` — **SessionStart → `scripts/fleet_health.py`** (timeout 60s) | ADR-70 Tier-2: daily-throttled cross-repo audit + `no_sibling_orphans`; prints `[fleet] N/5 repos green` | Fired this session: `[fleet] 1 issue(s) in 5 repos`; commit d0cfe27 made it fail-soft for cloud clones | settings 2026-06-04 10:28 | **ACTIVE, fail-soft** (cloud-clone sibling-absence guarded 2026-06-04). |
| `.claude/settings.json` — Workflow permission | Pre-allow the Workflow tool | `"permissions": { "allow": ["Workflow"] }` | 2026-06-04 10:28 | No Write/Edit deny committed **by design** (deny-beats-allow would break daily work + the routine's own digest write; cloud containment via platform guards instead). |
| `.claude/settings.json` — marketplace + enabled plugin | Register `.dev-knowledge` as `dev-knowledge-methodology`; enable `tier1-lifecycle@dev-knowledge-methodology` | `extraKnownMarketplaces` → Windows-absolute repo path; `enabledPlugins` true | 2026-06-04 10:28 | Marketplace path is **Windows-absolute** → unresolvable on Linux (root cause of cloud-inert plugin, below). |
| `.claude/commands/handoff.md` (12.2 KB) | Handoff generate/complete (HANDOFF_PROCESS v4 two-phase) | Repo command | 2026-05-31 19:41 | Active. |
| `.claude/commands/save.md` (1.13 KB) | Stage + commit with Conventional Commits body | Repo command | 2026-05-17 19:56 | Active. |
| `plugins/tier1-lifecycle/` (scripts: `propose_closures.py` ~15 KB, `review_closures.py` ~12 KB, `validate_backlog.py` ~5.7 KB) | ADR-70 Tier-1: Stop hook writes `logs/PROPOSALS-<date>.md` (detect/propose only); `/review-closures` human-gated close; surfacing via the **global** L0 hook (plugin SessionStart fires too late) | Local: functional (Stop proposes, L0 surfaces). | per repo | **CLOUD-INERT (documented):** JOURNAL 2026-06-04 — *"tier1-lifecycle plugin inert in cloud (local-only marketplace path — harmless)."* Linux clone can't resolve the Windows marketplace path; plugin doesn't load. Harmless because the cloud conformance run is read-only with no closures to propose. |
| `.claude-plugin/marketplace.json` | Declare `dev-knowledge-methodology` marketplace shipping `tier1-lifecycle` (source `./plugins/tier1-lifecycle`) | 1 plugin published; child repos install from here | per repo | Functional locally; cloud unaffected (spec-orchestration path is separate). |

---

## 7 — Toolchain facts (presence only — nothing installed or modified)

| ITEM | DECLARED ROLE | EVIDENCE OF USE | LAST TOUCHED | FLAGS |
|---|---|---|---|---|
| `uv` | (would-be Python pkg/venv manager) | `uv --version` → not recognized | — | **NOT PRESENT.** |
| `pipx` | (would-be isolated CLI installer) | `pipx --version` → not recognized | — | **NOT PRESENT.** |
| Python | Active interpreter | `py --version` → **3.12.10** | — | No Python version pin in `pyproject.toml` (the `required-version` constraint pins **ruff**, not Python). |
| Node | Active runtime (Workflow `.js` execution) | `node --version` → **v25.2.1** | — | No node pin in repo. |
| Ruff | Lint gate (pre-commit, gate mode) | `ruff --version` → **0.15.5**; pin `>=0.15.5` (`pyproject.toml`); `.pre-commit-config.yaml` uses `language: system` | — | **EXACT match to floor — no drift.** `language: system` = no virtualenv mismatch possible. |

---

## ORPHANS / DUPLICATES / STALE

**DUPLICATES**
- **`conformance-hub.js` exists in two places.** Repo copy (`.dev-knowledge/.claude/workflows/`, 12,452 B, 2026-06-04 16:21) is canonical — has the V1 shallow-history guard + portable paths. Global copy (`~/.claude/workflows/`, 11,979 B, 2026-06-04 00:12) is **16h stale and lacks the guard**. (§4)

**ORPHANED / DORMANT**
- `~/.claude/memory/` `.jsonl` sinks (`corrections`, `observations`, `sessions`, `violations`) — **all four missing**; the Self-Evolution Protocol + `/evolve` + both evolution echo-hooks run on empty inputs. `learned-rules.md` (4 ln) and `evolution-log.md` (header-only) are stubs. (§5a)
- `~/.claude/plans/` — 3 files from 2026-03-08…03-30 unreferenced in recent docs; ~27 mid-archive files (4/21–5/25) pre-date the active series. 62 files, no pruning. (§5c)
- `~/.claude/night-agent/logs/` — no runs since **2026-06-01** (9 logs, all that date). (§3)
- `~/.claude/skills/verify` — untouched since 2026-03-28; no sampled invocation; targets a possibly-moved monorepo layout. (§2)

**STALE (content predates dependent state)**
- `~/.claude/memory/README.md` documents a memory protocol whose files don't exist. (§5a)
- Global `conformance-hub.js` (see DUPLICATES). (§4)

**CLOUD-INERT (documented, intentional, harmless)**
- `tier1-lifecycle` plugin — Windows-absolute marketplace path unresolvable on Linux cloud clones; doesn't load there. Local Tier-1 loop unaffected. (§6)

**NOT PRESENT**
- `uv`, `pipx` — neither installed anywhere on PATH. (§7)

---

**End of inventory. No machinery was modified, created (other than this report), or removed.**
