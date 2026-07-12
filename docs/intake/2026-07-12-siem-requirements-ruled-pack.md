---
intake-id: 14
status: RULED
origin: "consolidation of the two independent #14 derivations (Fable + Codex sol), ruled 2026-07-12 (A0 seal)"
consumed-by: "#328 build (charter requirements)"
note: "ONE ruled pack unioning the two independent #14 SIEM/observability derivations. The two source drafts (2026-07-13-siem-fleet-management-requirements.md = Fable · -codex.md = Codex sol) are RETAINED as provenance, not deleted; this pack is the authority #328 builds against."
---

# SIEM / fleet-observability requirements — RULED consolidation pack (#14)

> **What this is.** The two independent #14 derivations — Fable (`2026-07-13-siem-fleet-management-requirements.md`) and Codex sol (`…-codex.md`) — were commissioned as a parallel-derivation check. They CONVERGED. This pack unions them into the settled requirement set, **ratifies PULL**, records the **W1/S1 reclassification**, and adds **two requirements neither draft carried**. Phase A / **#328 builds against THIS**, not against either draft alone. The two source drafts stay in-folder as provenance (§1 join-key discipline — same intake-id 14).

## 1. Consolidation method — union of requirements

The two derivations agree on the floor; the union takes the **stronger/more-specific** form of each shared requirement and preserves what only one carried.

**ADOPT from Codex (sol) — the more-specific mechanics:**
- **Five distinct mechanism states** (Codex FR-02): `desired` → `detected/carried` → `armed` → `synthetic-fire-proven` → `operationally-observed`, plus `retired | not-applicable | unavailable | unknown | stale`. **No later state inferred from an earlier one; synthetic never counts as adoption.** (Supersedes Fable's coarser present/fired split — Fable FR-9's "CAN-fire vs DID-fire" is the two endpoints of this five-state spine.)
- **Opportunity-denominator telemetry** (Codex FR-08): every eligible action emits `opportunity` → `organ-fired` → terminal `passed | blocked | failed-soft | errored | skipped`, correlated to one invocation. **A missing fire is `silent` ONLY when an eligible opportunity AND fresh collection are both proven; else `inactive | unknown | collection-gap`.** This is the load-bearing adoption of the whole pack (see the §3 correction).
- **Collector self-health** (Codex FR-09/FR-12): watermarks, per-repo lag, records accepted/rejected/duplicated, partial-line counts, rotation/truncation detection, schema-versions-seen, rebuild status. **"No findings" with a stale collector renders `unavailable`, never green.**
- **Idempotency** (Codex FR-07/FR-09): duplicate `event_id` ingestion is idempotent; collection is incremental, restartable, checkpoint-per-segment; recovery yields exactly one normalized row per `event_id`; locked Windows files degrade to a visible retry state, never loss or false-empty.

**KEEP from Fable — the framing and scale case:**
- **Volumes arithmetic** (Fable Annex A): ≤1 MB/day, tens of MB/month before rotation at 8 repos — **three-plus orders of magnitude below any log-platform threshold**; the ELK/Grafana/Loki rejection is terminal on arithmetic, independent of the standing doctrinal rejection.
- **Scenarios S1–S6** (Fable): the six witnessed walkthroughs remain the acceptance narrative (silent Stop hook · silently-serial suite · resurrected prune · carry-that-didn't-take · three-name organ · the morning read).
- **Register-faithful output grammar** (Fable FR-14): the machine emits the human registers' own verdict vocabulary (**FIX-NOW / DECLARE-LOCAL / TICKET / AT-PARITY**) so registers regenerate from runs instead of drifting from them.

**Convergent in BOTH (carried forward unchanged):** one versioned role-aware contract (Fable FR-1 / Codex FR-01, incl. the hub-as-role §9a fix — see §4/step-2 reconciliation); canonical organ identity distinct from name/path/byte-shape (Fable FR-2 / Codex FR-04); semantic parity with byte evidence, not byte-equality-as-policy (Fable FR-1/FR-2 / Codex FR-03); dependency-version parity leg (#332; Fable FR-7 / Codex FR-05); deterministic two-direction conformance walk, WARN-only v1 (Fable FR-3 / Codex FR-06); extend-don't-duplicate the existing organs + registers (Fable FR-12 / Codex FR-10); effect-probes over text-probes (Fable FR-6 / Codex FR-09 `git check-ignore`); privacy metadata-only (Fable FR-11 / Codex FR-12); hermetic consumer-local spool, no egress coupling (Fable FR-10 / Codex FR-09).

## 2. Ratified decision — PULL

Both derivations independently **RECOMMEND PULL** (Fable Annex C; Codex §(c)). The fork is **not genuinely contested**: every standing doctrine — hermetization, fail-open organs, Windows shared-write-lock avoidance, the incumbent read-only fleet organs (fleet_health / enforcement_coverage / boundary_report), single-operator nightly cadence — lands on PULL; PUSH's only edge (real-time freshness) has no consumer at n=1 operator, 3→8 locally-reachable repos.

**RATIFIED: PULL** — consumer-local gitignored JSONL spools + a hub-owned incremental read-only collector; transport-neutral event schema so delivery can change without touching producers or history. **Default is ratify** (this pack settles it). The operator MAY still route it to AI Council; per the standing ceremony rule, a lopsided question is manufactured ceremony, so Council is not the default here. **Reopen tripwires (any one revives the fork → Council):** the fleet spans machines / no shared local disk; a near-real-time consumer appears (cross-repo gating mid-session); a repo joins the hub may not read (privacy inversion); collection retries/lag exceed the survival metric.

## 3. CORRECTION — W1/S1 stop-hook evidence reclassified (2026-07-12 diagnosis)

Fable's **S1 / W1** ("the silent Stop hook") framed ai-council's Stop-organ silence as a candidate **organ failure** — the organ went quiet where corp's fired. **The 2026-07-12 diagnosis reclassifies this evidence:** the ai-council Stop-hook silence was a **REPO-STATE-designed no-op** — the organ did exactly what it should given the repo state (nothing to close/propose), NOT a failure to fire. The defect is that **healthy silence (nothing to do) and broken silence (organ failed) are INDISTINGUISHABLE from the outside** — an **OBSERVABILITY gap**, not an organ failure.

**Consequence (this STRENGTHENS the layer, does not weaken the requirement):** the correct evidence for the whole pack is that presence/fire checks cannot tell designed-quiet from broken-quiet — which is *exactly* why the **opportunity-denominator** (§1, Codex FR-08) is load-bearing: only an `opportunity` event proves there was something to fire on, so a no-`opportunity` window reads `inactive`, not `silent`. W1 stays a witnessed motivator; its **class changes from `organ-execution-failure` to `observability-gap`**, and the S1 acceptance criterion (Fable AC-3) is restated: *with telemetry live, an eligible-opportunity-with-no-fire surfaces `silent` within one cycle, while a no-opportunity window surfaces `inactive` — never a bare "last seen".*

## 4. Added requirements — neither draft carried

**FR-A — Sanctioned-lanes queryability (worktree lanes as first-class state).** Parallel-session **worktree lanes** are a sanctioned, transient, methodology-legitimate repo state (the provision→cleanup round-trip; core-invariant "no leftovers"). The layer MUST represent an active/known sanctioned lane as **first-class queryable state**, exactly as deliberate-absence is first-class (Fable FR-5 / Codex FR-02 `retired`): a lane's presence, its owning session, and its expected teardown are queryable, so a lane-in-flight reads as **`sanctioned-lane`**, never as undeclared drift, an orphan, or a dirty-tree anomaly. Without this, the conformance walk mis-classifies a legitimate worktree as an UNDECLARED deviation (the false-positive class), and a lane that outlived its session (a real leftover) is indistinguishable from one still working. Rationale continuous with S3's "deliberate absence is queryable" — sanctioned transient PRESENCE deserves the same first-class treatment as sanctioned ABSENCE.

**FR-4 — Ruling-addressability (operator rulings must be citable).** An operator ruling MUST be **machine-addressable/citable** — it has a durable home (prompt/plan/doc + a stable reference) so a later session can *find and cite the settled ruling* instead of re-litigating it. **Witnessed:** a corp session **re-asked a fork the operator had already settled**, because the ruling lived only in a dialog turn with no addressable home (the dialog died with the session). This is the observability-of-decisions leg: the layer/registers MUST let "was this fork already ruled, and where?" be answered by reference, not by memory or re-ask. Continuous with the LESSONS entry "operator rulings live in prompts/plans, not dialog turns" and the §3 observability principle (a decision with no addressable evidence is indistinguishable from an unmade one).

## 5. Non-goals (union — binding, do not relitigate)

Both drafts' non-goals stand, unioned: **no Grafana/Loki/ELK-class stack or hosted service (permanently rejected)**; no resident daemons/agents/services/queues/brokers; no cloud/SaaS destination; **no auto-remediation / no consumer mutation** (detect-and-propose; ADR-96 refusal semantics); **WARN-only v1, zero new blocking gates** (§9b, ADR-85 hardening pattern); no dashboards-as-service (viewer = local HTML, intake #9; architecture-viz deferred, intake #10); **out of collection scope:** application logs, transcripts, client/product content, OneDrive-zone paths (all tiers), anything beyond methodology-organ metadata. **Platform tripwire** (operationalizing libraries-not-platforms): a candidate is a PLATFORM and out if it runs resident, owns state not regenerable from git + JSONL, carries its own upgrade/ops lifecycle, or introduces a rule DSL to learn.

## 6. Acceptance criteria

The Fable AC set (1–8) and the Codex AC set (1–10) both hold; the union is the build's UAT, with two adjustments: **AC-3 restated** per §3 (opportunity-vs-silence, not bare last-seen); **two added** — (FR-A) a hermetic fixture with an active sanctioned worktree lane reads `sanctioned-lane`, not UNDECLARED, and a lane that outlived its owning session reads as a distinct leftover; (FR-4) a fork the operator already ruled is answerable "already-ruled @ <reference>" by citation, and an unaddressable re-ask is itself surfaced.

## 7. Status

**RULED** — this pack is the settled requirement set; **consumed-by #328 build** (charter). PULL ratified (§2, operator may still route to Council); W1/S1 reclassified (§3); FR-A + FR-4 added (§4). The two source derivations remain in-folder as provenance (same intake-id 14). Least-commitment stands: schema finalization, store/viewer class (SQLite vs DuckDB), and emitter-wiring locus are Phase A build decisions, not settled here.
