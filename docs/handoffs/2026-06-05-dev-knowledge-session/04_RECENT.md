# 04 · What just happened

A narrative of recent work on `.dev-knowledge`, written so a chat with zero prior context
can pick up the thread. Prose, not a log dump.

## The arc

This was the arc where the methodology **stopped being a project and became
infrastructure**. Four phases (A–D) — A through C all merged and reconciled to git as of
`main @ 6e8c84f`; Phase D (this handoff's job) is **codification only**.

**Phase A — graphify pilot** (`#88`, run on corp-monorepo): verdict **REJECT**. The
adoption process got its first full exercise — pre-registered kill criterion → security
gate *before* install → branch-isolated pilot → measurements → operator ruling → evidence
preserved, zero residue. The security gate paid off twice: it caught that the plan's
premise was false (v0.8.31 has **no** skill-only install path — the documented command
force-bundles a PreToolUse hook and edits the governed root CLAUDE.md) and caught ambient
`GEMINI_API_KEY` auto-detection that would have silently routed the pilot to per-token
billing. Measurements: the symbol graph was *worse* than the hand-curated codemap for
architecture (3003 noisy nodes vs the curated 10/15/4, no layer model); grep was cheaper
2.5–5.6× **and** higher quality 3/3; maintenance clashed with hub governance on three
counts. Kill criterion failed on both clauses. Report: `docs/audits/2026-06-04-graphify-pilot.md`
on **corp-monorepo** `main`.

**Phase B — cloud night.** The hub was pushed to a **private GitHub repo**
(`rdwornik/dev-knowledge`) — a deliberate, recorded reversal of the standing "nothing is
pushed" state, for this repo only (formal ADR still pending under `#86`). The validated
`conformance-hub` workflow now travels **in-repo** (`.claude/workflows/conformance-hub.js`)
— committed byte-identical first, then ported for Linux paths in a separate commit
(provenance preserved). The committed safety envelope is **allow-only** (platform guards:
`claude/`-only branch pushes, PR gate, read-only payload, porcelain tripwire) — a committed
Write/Edit *deny* was explicitly rejected because deny-beats-allow with no carve-outs would
break local daily work. The Step-6 cloud test surfaced the arc's single most important
platform fact: **the native Workflow launcher is NOT enabled in cloud runtimes** ("Workflow
exists but is not enabled in this context" — a capability gate, not permissions).
Resolution: the `.js` is the canonical **specification**; the nightly Routine attempts
native first and falls back to **spec-orchestration** (read-only Explore agents executing
the script's exact stage prompts/schemas), and the digest reports which path ran — so
**every night is a free re-probe** of the platform. The nightly Routine is live (daily
03:00 local, model Sonnet). Its first run-now produced **PR #1** (8 raw → skeptic killed
8 → **0 survivors**), verified and squash-merged. Two same-day hardenings: the V1
shallow-history guard (cloud clones start at the first push, so pre-push SHAs are
out-of-scope, not findings) and a `fleet_health` cloud-clone fail-soft.

**Phase C — machinery review + outcome loop.** A read-only inventory of all runtime
machinery (`docs/audits/2026-06-05-machinery-inventory.md`), then operator-approved
verdicts, then execution. **Retired to archive (never deleted):** the March-era
Self-Evolution system (its four `.jsonl` sinks never existed — the loop ran on empty inputs
for three months; the hub's LESSONS+gotchas+ADRs became the *real* evolution system),
`/boot`, the stale `verify` skill, the global duplicate of `conformance-hub.js`, 16 stale
plan files. The **night-agent finding:** it was NEVER a registered scheduled task — the 9
logs were manual dry-runs; the inventory beat everyone's memory. The arc's best detective
story — **model-routing root cause:** the documented "per-agent routing non-functional"
gotcha was *self-inflicted* — a `CLAUDE_CODE_SUBAGENT_MODEL=haiku` override the operator set
~March for cost control, living in **two** sources (`~/.claude/settings.json` AND
`Documents/.secrets/.env`, dot-sourced into every shell by `$PROFILE` — a covert second
config channel). Clearing only settings.json was necessary but not sufficient. After both
cleared: pins honored distinctly on **both** the Agent-tool and workflow-engine paths
(probed, transcripts read). **P0 hardening:** the `block-onedrive` guard matched only the
Bash tool while sessions run with the PowerShell tool — it now matches both, probe-verified.

**Phase C4 — nightly outcome loop:** the fleet's **first GitHub Action**
(`nightly-conformance-triage.yml`). Diff guard = exactly one ADDED
`docs/audits/*-conformance-nightly-digest.md` or no merge; survivor count parsed from the
digest **body** (the real PR title is free-form — another plan premise refuted by reality),
parse-fails-closed; merge failures loud; untrusted step outputs routed through `env:`
(injection-proofing). Three live synthetic PRs validated all three paths (clean/findings/
anomaly) with full cleanup. Survivors become `nightly-triage` Issues surfaced by a
fail-soft SessionStart line — because the operator does **not** read email; clean nights
are invisible by design.

**Sweeps:** git↔BACKLOG reconciled both directions (the manual run is now `[#90]`'s
reference spec); `#87` withdrawn (premise refuted by the re-probe), `#83`'s note corrected,
`[#89]`/`[#90]` added; the living-doc staleness map authored — and corrected once (see the
Load-bearing table). Parallel detail across these days lives in JOURNAL (2026-06-04 →
2026-06-05) if load-bearing.

## Four-tag discipline (canonical)

The sage tagged every claim using this discipline (canonical per HANDOFF_PROCESS v4.3
Amendment A; supersedes the earlier three-tag body in spec §3.1):

- **witnessed** — sage just verified this OR saw it happen recently AND has no reason to
  think it changed since
- **recall** — sage remembers from earlier in the session; **state may have changed** —
  verify via CC inline if the claim is load-bearing
- **inferred** — reasoning from evidence (not direct knowledge)
- **unknown** — sage doesn't know — flagged explicitly

When you encounter `recall` or `unknown` on a load-bearing claim in this file, verify via
CC before acting on it. This is the "handoff is back-and-forth" rule from PLAYBOOK methodology.

## What the sender chat said (interview)

The sender framed Phase D's mission in one line: **make the books match the building.**
The deployment arc is shipped and reconciled; an entire "night architecture" now exists
that the prose docs don't know about. The sender's recommended entry order [inferred —
sequencing judgment, not a constraint]:

1. **Read the first production nightly PR before writing anything** — it validates (or
   breaks) several assumptions the docs are about to codify. [witnessed: scheduled tonight;
   outcome unknown]
2. **`ARCHITECTURE.md` first** — largest gap (the whole night architecture is absent) and
   the one *actively-misleading* passage: the ADR-68 night-agent section describes a
   never-registered mechanism, superseded in reality by the cloud Routine → needs a
   **supersession note**, deliberately left unfixed (Phase-D scope). [witnessed]
3. **PLAYBOOK adoption section while the three case studies are fresh** — Dynamic Workflows
   **ADOPT**, graphify **REJECT**, GitHub Action **ADOPT** are this week's lived material;
   the rubric (tool-vs-platform / pain-owned-vs-imagined / subscription-economy fit + pilot
   discipline with **pre-registered kill criteria**) writes itself now and won't in a month.
4. **Doctrine pieces** (t-shirt routing, cloud-readiness, maintenance cadences, lessons
   codification) slot in after the two big docs.

The full Phase-D agenda, the living-doc staleness map (ARCHITECTURE/PLAYBOOK **STALE**,
CONTRIBUTING **PARTIAL** — missing the spec-orchestration rationale, CLAUDE
**STALE-by-deferral**, VISION/ESSENTIALS **current-by-scope**), and the reconciliation
baseline ride in the Phase-1 interview's receiver-context block (folded into `05_NOW.md`).

## Load-bearing facts (cross-checked vs repo at Phase 2)

| Claim from sender | Repo fact | Phase-2 verdict | Verification command |
|---|---|---|---|
| HEAD handed off = `6e8c84f` (`main`, clean) | `main` tip = `6e8c84f` | ✅ verified | `git rev-parse main` |
| Branch `docs/handoff-2026-06-05` is 2 commits ahead of main, unmerged | exactly `9a64a22` + `19c2b72` ahead | ✅ verified | `git log --oneline main..HEAD` |
| Hub pushed to private GitHub `rdwornik/dev-knowledge` | `origin` = `github.com/rdwornik/dev-knowledge` | ✅ verified (private flag not git-visible) | `git remote -v` |
| conformance-hub.js / nightly-triage Action / surface_triage.ps1 shipped | all three files present | ✅ verified | `test -f <path>` ×3 |
| `#87` withdrawn; `#83` note corrected; `[#89]`/`[#90]` added | BACKLOG matches; #87 not an active task | ✅ verified | `grep -nE "#(83\|87\|89\|90)" BACKLOG.md` |
| 235 tests green · ruff clean · `validate_backlog` OK 52 tasks | 235 passed · clean · 52 tasks | ✅ verified | `py -m pytest -q` · `py -m ruff check` · `py -m scripts.validate_backlog` |
| PR #1 = 8 raw → 0 survivors, merged | merge `205da14` "0 survivors (#1)" present | ✅ verified | `git log --oneline --grep="0 survivors"` |
| ARCHITECTURE ADR-68 night-agent section misleading + cloud/night content absent (intentionally unfixed) | confirmed by operator grep against live file pre-Phase-2 | ✅ verified (Phase-D target) | `grep -i "cloud\|routine\|spec-orch" ARCHITECTURE.md` |
| `/handoff` **skill** stamps v4.3.1/stable vs live spec v4.3.2 (§E beta) | live spec header `Version: 4.3.2`; §E "ships at status beta" | ⚠️ known skill-staleness, **not** bundle drift — README stamps v4.3.2/beta | `grep -n "Version\|Status" protocols/HANDOFF_PROCESS.md` |
| block-onedrive now matches Bash + PowerShell tools (P0 hardening) | lives in `~/.claude/` (out-of-repo) | ◻️ recall — not re-verified at Phase 2 | (verify in `~/.claude/settings.json` if load-bearing) |

## Decisions & reasoning to carry forward

- **Spec-orchestration over waiting for the platform.** When the native launcher turned
  out cloud-disabled: adapt AND keep investigating for free — attempt-native-first every
  night means the day the platform enables the engine, the digest tells us. Rejected:
  blocking on a research-preview fact we don't control. [witnessed]
- **Platform guards over committed denies.** An enumerated deny of `protocols/`/living docs
  would have protected the cloud but blocked Phase D's own local PLAYBOOK edits (deny beats
  allow, no carve-outs). The night is guarded by structure instead. [witnessed]
- **Remove the model override rather than re-point it.** Evidence showed the env var beats
  explicit pins at *any* value — setting it to "sonnet" would keep routing broken, just
  costlier. Remove it; control cost with explicit per-agent pins (t-shirt doctrine). [witnessed]
- **Deterministic Action over an LLM for outcome management.** Merging a guard-verified
  digest is judgment-free; an LLM belongs where judgment lives (the skeptic, operator
  triage), not where a regex does. [witnessed]
- **Sender's own self-critique (for your calibration):** their contracts repeatedly carried
  *unverified premises* — every one caught by a gate, but the pattern is why `[#89]` exists.
  When you encode a premise into a contract, verify it against state first or mark it an
  assumption-to-check. [witnessed]
