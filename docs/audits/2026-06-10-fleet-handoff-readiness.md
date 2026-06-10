# Fleet handoff-readiness audit — 2026-06-10

**Type:** read-only fleet inventory · **Scope:** every ecosystem repo's handoff-maturity tier + actual transmission mechanism · **Author:** Claude Code (architect-chat audit)
**Status:** immutable (supersede with a new dated file; never edit in place — CLAUDE.md §5/§4)
**Purpose:** Give the v4.4 fleet-migration rollout a pre-selection basis grounded in *primary fleet state on disk*, not memory or compaction summaries. This audit reads child repos; it modifies none (ADR-41/ADR-36 read-only cross-repo contract). All writes landed only in `.dev-knowledge`.

---

## 1. Readiness matrix

One row per repo. Columns are the Step-2 maturity markers + Step-3 transmission mechanism + Step-4 tier. **State was verified on disk** for every cell — the registry `notes` (last_updated 2026-04-27) were used only to resolve the repo list + paths.

| Repo | CLAUDE.md (ver / last_reviewed) | local `/handoff` cmd | floor wired (@-incl + `CLAUDE-FLOOR.md` + `.sha256`) | `tier1-lifecycle` plugin | `docs/handoffs/` | transmission mechanism | tier |
|---|---|---|---|---|---|---|---|
| `.dev-knowledge` (hub) | v2.16 / 2026-06-07 (191L) | ✅ dispatch → `protocols/HANDOFF_PROCESS.md` v4.4 | n/a — **is** the floor-generator source (`scripts/generate_floor.py`) | 0.1.10 — marketplace **source** + enabled | ✅ 30+ bundles; latest `2026-06-10-dev-knowledge-session` | **hub-source** (canonical origin) | **current** |
| `corp-sca-time-automation` | v2.1 / 2026-06-08 (107L) | ✗ (by design) | ✅ @-include (CLAUDE.md L14) + `CLAUDE-FLOOR.md` + `.sha256` | 0.1.10 (enabled) | ✗ | **hub-pointer + floor** | **current** |
| `corp-monorepo` | v2.2 / 2026-06-02 (153L) | ✗ (by design) | ✗ | 0.1.10 (enabled) | ✗ | **hub-pointer** | **partial** |
| `ai-council` | v2.3 / 2026-06-02 (153L) | ✗ (by design) | ✗ | 0.1.10 (enabled) | ✗ | **hub-pointer** | **partial** |
| `corp-ops` | v2.1 / 2026-06-02 (79L) | ✗ (by design) | ✗ | 0.1.10 (enabled) | ✗ | **hub-pointer** | **partial** |
| `terminal-setup` *(NOT in registry)* | ✗ none | ✗ | ✗ | not present | ✗ | **none** | **cold** (out-of-registry) |

**Tier distribution (5 registered repos):** current = **2** · partial = **3** · cold = **0**.
**Plus** `terminal-setup` = cold, but **out-of-registry** — a live sibling git repo absent from `repos.toml`, so it is *not* counted in the fleet tally (see §4).

---

## 2. Tiering — which repos are cold, partial, current

**Current (2):**
- **`.dev-knowledge` (hub)** — the canonical source. Resident `protocols/HANDOFF_PROCESS.md` v4.4, a `/handoff` dispatch command that defers to it, 30+ self-generated bundles in `docs/handoffs/` (latest 2026-06-10), and the `tier1-lifecycle` marketplace it ships. Special case: it *originates* the process rather than consuming a pointer.
- **`corp-sca-time-automation`** — the only **child** with the full ADR-78 floor stack wired: `CLAUDE.md` L14 `@.claude/CLAUDE-FLOOR.md`, the generated `CLAUDE-FLOOR.md`, and its `.sha256` guard — plus the plugin at hub version and `../.dev-knowledge/protocols/` pointers. It is the ADR-78 pilot, done.

**Partial (3): `corp-monorepo`, `ai-council`, `corp-ops`** — each runs the hub-pointer mechanism correctly (plugin `tier1-lifecycle@0.1.10` enabled + `../.dev-knowledge/protocols/` references in `CLAUDE.md`), so handoff *transmission* works today. What they lack is the **ADR-78 floor wiring** (no `@`-include, no `CLAUDE-FLOOR.md`, no `.sha256`). That single gap is the entire current↔partial discriminator among children.

**Cold (0 registered):** none of the 5 registered repos is cold. `terminal-setup` (unregistered) is cold — no `CLAUDE.md`, no plugin, no handoff machinery; it would be **first-time adoption, not migration**, if inducted.

### By-design, NOT a gap
Children have **no local `/handoff` command** and **no `docs/handoffs/` directory** — and that is *correct*, not a maturity deficiency. Handoffs are centralized at the hub (ADR-42) and children are read-only (ADR-36): a child handoff is generated *at* `.dev-knowledge` (`"Make handoff for <repo>"`) and the bundle is delivered into the child's next session. Presence-based scoring would wrongly flag every child as deficient here; this audit does not.

---

## 3. Pilot candidates for promoting v4.4 beta → stable (§G)

HANDOFF_PROCESS §G / amendment v4.3.1 §B: a version promotes `beta` → `stable` after **one** fresh-eyes review where (1) Stage-1 returns **< 2 critical findings** (sev 4–5) **and** (2) the Stage-3 verdict is **PROMOTE** or **PROMOTE-WITH-CAVEATS**; reviewer judgment overrides the mechanical count. v4.4 currently ships **beta** (the bundle generator stamps `status: beta`; confirmed by the recent "beta correct" commit).

Surfaced candidates — **the rollout ruling is the operator's; this does not decide it:**

1. **`.dev-knowledge` (hub)** — *lowest-risk first pilot.* It already produces v4.4 beta bundles in production daily (latest 2026-06-10). A fresh-eyes Stage-1/Stage-3 review of an **existing** v4.4 bundle could satisfy §G immediately, with no new handoff to manufacture.
2. **`corp-monorepo`** — *strongest stress test.* Richest, most-active business context → exercises v4.4 under the heaviest real conditions; the highest-confidence promotion signal if it passes.
3. **`corp-sca-time-automation`** — *fullest pointer stack.* Only child with the ADR-78 floor wired, so a handoff here validates the complete pointer chain (plugin + protocols + floor) end-to-end.

---

## 4. Verification notes

- **Registry path — CONFIRMED:** `C:\Users\1028120\Documents\Dev\.settings\repos.toml` exists and matches the prompt's expected path. Schema: `[meta]{schema_version, last_updated, maintained_by}` + `[[repo]]{name, path, scale, notes}`. Lists 5 repos. The path uses forward slashes and is accurate.
- **Registry is stale in `notes` / `last_updated`:** `last_updated = 2026-04-27`; the per-repo `notes` reference the retired AGENTS.md and old "violations." The registry was therefore used **only** to resolve the authoritative repo list + paths; every maturity/mechanism cell was re-verified on disk.
- **`terminal-setup` discrepancy:** a live git repo at `Dev\terminal-setup` that is **absent from `repos.toml`**. Flagged here, treated as out-of-registry cold, and **excluded from the fleet tier counts**. Whether it should be inducted into the registry is an operator decision, not part of this audit.
- **PLAYBOOK Mode-enum check — NO mismatch:** PLAYBOOK defines the Mode enum as `auto-accept / plan-then-auto / plan` (≈ PLAYBOOK L1991, L2030–2035). The architect prompt's header "Mode: plan-then-auto" is this task's *chosen* mode, not a competing enum claim — consistent. `HANDOFF_PROCESS.md` defines **no** Mode enum (it governs bundle handoffs, an orthogonal domain) — not a contradiction.
- **v4.4 status is two axes (flag):** `HANDOFF_PROCESS.md` header reads `Status: live` (the process is the active one), while the *version maturity* is `beta` (the bundle generator stamps `v4.4 (status: beta)`; amendment: "ships beta, promotes to stable after one qualifying handoff"). These are different axes — "live" ≠ "stable" — and do not conflict.
- **Ambiguity / judgment call (open for operator re-weighting):** tiering `corp-monorepo` / `ai-council` / `corp-ops` as *partial* rests **solely** on ADR-78 floor absence. If the operator regards the floor as a *separate carrier axis* (methodology baseline) rather than handoff machinery, then all four children are *current* and the split collapses. Surfaced rather than decided.
- **Transmission is two-component (nuance):** for children the *methodology/process* is **hub-pointer** — pulled live via the enabled plugin + `../.dev-knowledge/protocols/` references (+ the floor @-include for corp-sca). The *session-bundle content itself* is hub-**generated** and operator-**pasted** into the child session (snapshot delivery; no upload automation). The Step-3 classification above reflects the methodology axis, which is what the pointer-first migration premise turns on.

### Load-bearing conclusion for the migration runbook
**The hub-pointer mechanism exists today.** All four children enable `tier1-lifecycle@0.1.10` and reference the hub's protocols; `corp-sca-time-automation` additionally @-includes the hub-generated floor under its `.sha256` guard. The premise that a pointer-first migration is mechanically available — and already partly in production — holds.

---

*Sources: `Dev/.settings/repos.toml`; each repo's `CLAUDE.md`, `.claude/settings.json`, `.claude/commands/`, `.claude/CLAUDE-FLOOR.md(.sha256)`, `docs/handoffs/`; hub `protocols/HANDOFF_PROCESS.md` v4.4, `protocols/PLAYBOOK.md`, `ARCHITECTURE.md` Ch2, `plugins/tier1-lifecycle/.claude-plugin/plugin.json`. Discovery via parallel read-only Explore agents; no child repo was written, staged, or committed.*
