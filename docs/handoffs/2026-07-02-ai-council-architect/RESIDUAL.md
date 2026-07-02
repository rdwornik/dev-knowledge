# Residual — 2026-07-02 ai-council architect handoff (cross-repo; the part the repo does not already encode)

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole ai-council `BACKLOG.md` + the two live audits, and the open architecture
> questions travel as residual so the next session **resumes** the design rather than rediscovering it.
>
> **Cross-repo (ADR-36/41).** The **target is `ai-council`**; the next architect session works ON
> ai-council. This bundle lives in the `.dev-knowledge` hub (`docs/handoffs/`) but every pointer,
> anchor, and probe below binds to **ai-council's own state** — ai-council has **no** `audit.py` /
> `ship-gate`, so the teeth probes (`PROBES.md`) are ai-council-native (its git, its pytest, its
> JOURNAL, its floor-guard). Run every probe **from the ai-council checkout**
> (`C:\Users\1028120\Documents\Dev\ai-council`).
>
> **Generated LIVE by hub CC (read-only on ai-council).** The repo-side facts in §1–§3 were
> re-derived live this generation (**witnessed**); the audit *contents* in §4 are **inferred/recall**
> from a full read of the two ai-council audit artifacts — re-derive the load-bearing ones via
> `PROBES.md`. `unknown` is stated as such.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the audits / git window, may have moved (re-checkable via `PROBES.md`);
> `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

ai-council has no `ship-gate`; these are computed directly from live git ∩ files (**witnessed** this
generation). **Re-derive each at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ⚠️ HEADLINE — the narrative record (JOURNAL / LESSONS) lags git by ~4 weeks

- **`JOURNAL.md`'s newest entry is dated `2026-06-03`** (ADR-71 TOC rollout), but **four significant
  merges landed after it** and are **unjournaled**: the council-vs-research audit (`a01358a`,
  2026-06-16), **deploy run #1** (methodology v1.0.0 pre-commit gate, `cba43a2`, 2026-06-30),
  **deploy run #2** (floor-arming, `2675394`, 2026-07-01), and today's methodology-adoption audit
  (`2026-07-02`, uncommitted-or-just-landed). **witnessed** (`PROBES.md` P4 recomputes the two dates).
  - *Caveat (do not overclaim):* deploy #1/#2 were **hub-driven** (the `.dev-knowledge` deploy
    orchestrator applied them TO ai-council), so their absence from ai-council's own JOURNAL is
    partly expected. The **genuinely-owed** entry is the **council-vs-research audit** (substantial
    in-repo architect work). The architect should confirm the journaling convention, not assume drift.
- **`LESSONS.md`'s newest entry is dated `2026-05-12`.** Two months of provider/deploy work carries
  no new lesson — likely a real capture gap, not a convention. **witnessed / inferred.**

### The straggler branch — merged, not deleted

- **`feat/floor-arming` (`7fb9650`) is merged into `main` (`2675394`) but not deleted** — a
  cleanup item (operator-gated `git branch -d`). **witnessed** (`PROBES.md` P6).

### ADR index omits an existing ADR (minor)

- **`docs/decisions/ADR-08-research-degradation-alarm.md` exists on disk, but the index
  `docs/decisions/README.md` table lists only ADR-01…ADR-07** — ADR-08 is missing from the index.
  Minor coherence gap, worth a one-line fix. **witnessed** (`PROBES.md` P7).

### What is NOT drift (surfaced so the architect does not chase it)

- **Methodology adoption is COMPLETE and clean** — the 2026-07-02 methodology-adoption audit
  read-live-verified: floor **ARMED & INTACT** (all six parts present, hash-guard exits 0, the
  CRLF/sha256 "mismatch" was a false alarm), the `tier1-lifecycle` plugin installed+enabled,
  `CLAUDE.md` ADR-53-conformant with the `@`-include on line 1, docs correctly split (PLAYBOOK/
  ESSENTIALS/handoffs deferred to the hub by design). **This is NOT the frontier** — only hygiene
  follow-ups remain (see §4). **inferred** from the audit.

---

## §2 — Shipped this window (2026-06-03 → 2026-07-02) — the map, not the narration

Pointer-first (`git log --first-parent`, the two audit files, `LESSONS.md`, ADR index). **recall/inferred**
from the window; re-derive load-bearing facts via `PROBES.md`.

- **Council-vs-research audit** (`a01358a`, 2026-06-16) — `docs/audits/2026-06-16-council-architecture-vs-research-audit.md`.
  A council-vs-MAD (multi-agent-debate) research audit: current-state inventory, correlation matrix,
  gap analysis (G1–G7), invention bank (clusters A–F), tension map (8 axes). **Explicitly an
  ADR seed — converged on nothing.** This is the substantive architect input (see §4).
- **Deploy run #1** (`cba43a2`, 2026-06-30) — adopted methodology **v1.0.0** pre-commit gate
  (ruff v0.15.5 Tier-1 + hub-hooks rev-pin `v1.0.0`); ai-council ratified as the first real deploy.
- **Deploy run #2** (`2675394`, 2026-07-01) — **floor-arming**: `.claude/CLAUDE-FLOOR.md` +
  `.sha256` sidecar + `check_floor_hash.py` guard + the `floor-hash-verify` pre-commit hook +
  the `@.claude/CLAUDE-FLOOR.md` include in `CLAUDE.md` line 7. ai-council is now **armed**, not
  merely configured (the arm-first chain the hub's 2026-07-01 architect handoff sequenced).
- **Methodology-adoption audit** (2026-07-02) — `docs/audits/2026-07-02-methodology-adoption-audit.md`.
  Read-live inventory confirming adoption is genuinely complete; surfaces four hygiene items (§4).

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `ai-council/BACKLOG.md`** (ADR-66 story-map; **4 themes**, **11 tasks** `#1–#11`,
  all open at generation). The spec; items are tickets. **Do not re-narrate — open it.** **witnessed.**
  - The most decision-relevant open items: **#1/#2/#3** (decide the synthesizer on real data, then
    codify ADR-01) and **#9** (ADR-67 gated `/council-question` loop — **DEFERRED**, do NOT build
    before the canonical-baseline settles). The research-audit frontier (§4) is **not yet a BACKLOG
    item** — filing it is part of the next session's job.
- **Live branches:** `git branch -v` in ai-council. At generation: `main` (`2675394`, integrated,
  in sync with `origin/main`) + the straggler `feat/floor-arming` (§1).
- **No durable task-graph schema** — ai-council's `BACKLOG.md` uses the ADR-66 story-map but did
  **not** adopt the hub's `depends-on` / `serialize-group` clauses (#156 is hub-only). Precedence
  is prose (`BLOCKED on #1`, `conditional on #2`). So the task-graph is **residual prose**, not a
  schema fact — do not claim otherwise.

---

## §4 — The next frontier (open architecture decisions — this is a DECISION session)

Methodology adoption is **done**; the deploy machinery is **armed**. The center of gravity is the
**research-driven evolution of the council itself** — the 2026-06-16 audit is a **converged-nothing
ADR seed**, and the architect's job is to **decide what (if anything) to build and in what order.**
**recall/inferred** from the audit — the architect resumes the design here.

**The load-bearing frame (from the audit).** ai-council strongly implements the *"diversity + blind +
quality-weighted-judge half"* of the MAD research but **largely lacks the *measurement + control
half"* — baseline comparison, calibration, debate-gating, influence-gating, retrieval-for-debate,
context-budget enforcement. The seven gaps:

- **G1** per-regime refeed policy + diversity instrumentation (full refeed is a trade-off, not a defect).
- **G2** no score-based aggregation (single-judge fragility at full-transcript token cost).
- **G3** no debate-gating (full panel always runs; debate can override a correct single answer).
- **G4** no calibration / cross-session memory (confidence exists in judge mode only).
- **G5** **no baseline comparison — "the load-bearing gap."** Cannot show the council is net-positive
  over a self-consistency baseline at matched compute. **Gates the credibility of every other
  verifiable-regime improvement.**
- **G6** no retrieval for the debate panel (empirical cruxes settled by the most persuasive assertion).
- **G7** minority report is not a first-class output (dissent buried in the synthesis narrative).

**The audit's named first move (the architect's likely starting decision):** run **Open Question #1 —
the baseline experiment (closes G5)** — *"On verifiable sub-questions, is the council net-positive
over a self-consistency baseline at matched compute?"* Until measured, every verifiable-regime
invention (the audit's Clusters B/C, reputation, Self-MoA) is **a bet, not a settled win.**

**The unresolved decision axes (the tension map — the architect must pick a stance, not relitigate
each option):**
- Is the unit of change a **global redesign** or a **regime-aware policy** (refeed / gating / judging
  that branches on verifiable-vs-subjective)? — the audit frames this as *the* framing question.
- **Anonymization vs. reputation is a direct conflict** (blind-voting ADR-03 vs. earned calibration):
  can calibration be carried **after** the blind rounds, at synthesis only, without re-introducing
  identity-driven sycophancy?
- Which single invention has the **best effort-to-value ratio** for a first experiment? The audit's
  candidate (not conclusion): **recursive crux-zooming + tool adjudication** (Cluster C) — the only
  proposal with **no structural conflict** that **reuses the existing research pool**.

**Candidate ADR framing (the audit's, no number assigned):** *"Regime-aware council policy: when to
debate, how to refeed, how to adjudicate."* Numbering + the decision-to-record are the operator's.
The natural process move is a **Council debate seeded by this audit** — ai-council debating its own
architecture (dogfood). Whether to run that debate now, or run the G5 baseline experiment first, is
the **top sequencing call** for the incoming architect.

**Adjacent / smaller (do NOT let these crowd out the frontier):**
- **Hygiene follow-ups from the 2026-07-02 audit** (ranked): (1) `settings.local.json` is stale — its
  permission allowlist pins a **path that no longer exists** (`…/Documents/Scripts/ai-council`);
  cheapest high-value fix. (2) **`INSTALL.md` ownership** — keep-local vs. relocate-to-hub is an
  **architect call**. (3) prune duplicate `*.egg-info` + a spurious plugin-install record. (4)
  **confirm `.env` holds no API keys** (repo rule: keys live in `Documents/.secrets/.env`) — an
  **operator verify**, not a CC inspect. These are **hygiene, not architecture** — none touch Council runtime.
- **BACKLOG #1/#2/#3** (synthesizer-on-real-data → ADR-01 amendment) is a real, self-contained
  decision stream independent of the research frontier; **#9** (ADR-67 loop) stays **DEFERRED**.
- **JOURNAL/LESSONS catch-up** (§1) — a capture-hygiene decision (does ai-council journal hub-driven
  deploys? file the owed council-vs-research entry?).

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient (forced-read via `PROBES.md` P1):** `ai-council/VISION.md` `## Vision`,
  `ai-council/ARCHITECTURE.md` `## Purpose [CORE]`.
- **The frontier's "why":** `ai-council/docs/audits/2026-06-16-council-architecture-vs-research-audit.md`
  (the ADR seed — gaps, invention bank, tension map, open questions §"Open questions"/"next-step") and
  `ai-council/docs/audits/2026-07-02-methodology-adoption-audit.md` (adoption-complete + hygiene).
- **The council's design canon:** `ai-council/docs/decisions/ADR-01…ADR-08`, `VISION.md` Values,
  `docs/synthesis-quality-rubric.md`, `docs/council-question-guide.md`.
- **The end-to-end process this tool implements:** `.dev-knowledge/protocols/AI_COUNCIL_PROCESS.md`
  (hub; referenced by pointer, never re-narrated).
- **Recent design "why" in-repo:** `ai-council/LESSONS.md` (newest 2026-05-12 — see §1 staleness),
  the JOURNAL arc (newest 2026-06-03 — see §1).
- **Gate the design against live state:** run `PROBES.md` P1–P7 **from the ai-council checkout**.
  Any FAIL blocks onboarding.
