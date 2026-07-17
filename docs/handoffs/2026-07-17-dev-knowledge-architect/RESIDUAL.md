# Residual — 2026-07-17-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**All standing WARNs this window are pre-dispositioned in `ecosystem/disposition-register.yaml` — no NEW/undispositioned flag was introduced by the 2026-07-16 close-out.** Re-derive the live verdict/count/`[stale]` via P7 — do not trust this framing. The standing families, by reference (all carry register entries):

- **`no_ff_merges`** — three grandfathered direct-on-`main` commits (two 2026-06-19 journal/transcript, one 2026-06-26 freshness-wrap), each `warn-no-ff-*`-dispositioned; historical, pre-date the `block-ff-push` prevent organ.
- **`doc_rot` (backlog-accretion)** — the long-lived tickets `#262 / #278 / #328 / #332`, each `warn-doc-rot-backlog-*`-dispositioned; trimming is the standing kill-lever, not a gate failure. **Watch:** any edit that pushes another task past the 1200-char threshold mints a NEW WARN (the [[backlog-edit-doc-rot-threshold]] class) — keep task edits net-neutral.
- **`undeclared_edges`** — six `*-handoff-process` prose edges (`BACKLOG / VISION / ESSENTIALS / PLAYBOOK / SESSION_SETUP / AI_COUNCIL_PROCESS`), all `warn-undeclared-*` under `#241`; deferred structural work, not fresh drift.
- **`reconciled_versions`** — the `CONTRIBUTING-md-template.md` malformed-stamp WARN under `#335`, dispositioned.
- **`fleet_parity` (informational only — never a gate input, `#337`)** — its live `warn-undeclared` surface is corp-monorepo `precommit-hub-block` rev-vs-source_tag (the `#336` split-state), surfaced by `cmd_ship_gate` but NOT an `ALL_CHECKS` member. This is the thing standing between the fleet and a true zero-WARN state — hence the `#337` DEFER-peg on `#336`. Re-derive the live surface count via `python scripts/fleet_parity.py`.

**Disposition hygiene:** if the next session CLOSES a task that owns a doc_rot disposition, remove the register entry in the same arc or P7 prints a `[stale]` line (the [[close-backlog-orphans-disposition]] class).
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map — detail lives in `JOURNAL.md` (2026-07-16 entries) and `BACKLOG.md`; this is pointers only.

- **`#328` / `#332` fleet_parity checker + data plane** (ADR-101 in-file amendment) — `scripts/fleet_parity.py` + `ecosystem/{parity-surfaces,dependency-baseline}.yaml` + hub `.methodology.yaml`; both stay **OPEN** (consumer-side deploy carrier unbuilt). Merges `2bc02196` (build) → `3a2086`-era surfacing.
- **`#337` fleet_parity → informational ship-gate surface** — wired into `cmd_ship_gate` as a visible-every-ship, never-a-gate-input line (fail-open widened to `except Exception`); the **promotion-to-blocking** is the filed `#337`, DEFER-pegged on `#336`.
- **`#336` filed** — corp hub-block v1.3.1-vs-v1.2.0 split-state reconciliation (leg-1 deferral, operator-ruled: do not touch the record/pin this arc).
- **Satellite onboarding rulings** — `ecosystem/satellite-onboarding-rulings.yaml` + advisory validator + 4 ready onboarding prompts (`docs/intake/2026-07-16-*`, intake #15); all 4 satellites FULL (life-architect FULL overrides the census floor-only). **Prompts ready but UNFIRED** — operator fires per rollout order.
- **`#333` closed → `#338` filed** — codex-review doc-lane + §16 model re-pin shipped; the 5 residual drift items folded into `#338`.
- **`#339` filed (PROPOSED)** — LESSONS legacy-split ruling recorded in `LESSONS.md`; pending an ADR-29 amendment (chronological archival split ≠ ADR-29's rejected by-topic split).
- **`#254` closed** — fleet-audit data-branch organ (both parts verified; `origin/automation/fleet-audit` pushed, NOT merged — orphan organ stays separate).
- **CLAUDE §1 first-read diet** (v2.41) — PLAYBOOK demoted to on-demand reference; owner=hub region + `templates/claude-regions/first-read.md` in lockstep.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The open way-of-working questions, in rough dependency order. These are **decisions to make**, not tasks to execute — the execution tickets already exist in `BACKLOG.md`.

**1. The shared blocker: sequence the consumer/satellite onboarding wave (E6/S15–S16).** Several DEFER-pegs converge on one un-happened thing — *consumer-side deployment actually running*: `#337` (fleet_parity → blocking) is pegged on a true zero-WARN fleet, `#293` (consumer runbook fan-out) is pegged on Wave-1 onboarding, `#332`'s Done-when includes a deploy carrier. The 4 satellite onboarding prompts (intake #15) are **ready but unfired**, and the operator holds the rollout order (corp-ops → corp-sca → life-architect → demo-prep). **Decision:** does this session's plan fire the wave (unblocking the peg-cluster), or does it advance the hub-side design first? The tension is *breadth-first onboarding* (unblock the mesh) vs *depth-first hub hardening* (get the checker/gate right before it fans out). Note the hard guardrail: CC does not write into consumer trees (ADR-36/41) — the fan-out is per-repo operator-run, not a hub push.

**2. fleet_parity maturation — the split-state modeling call (`#336`, E2/S8).** `#336` is the concrete design decision, and it is the sole thing standing between the fleet and zero-WARN. Two named options: (a) **model enforcement-gate-rev separately from corpus `source_tag`** in `parity-surfaces.yaml` (touches the `#328` checker + the MUST/non-waivable branch — a schema change that recognizes "gate uplifted ahead of a full redeploy" as a legitimate, declarable state), or (b) **schedule a real v1.3.1 corp redeploy** (but full redeploy re-appends the `codemap-freshness` hook corp deliberately removed, #276 unlanded). All three naive fixes (record-stamp / full-redeploy / pin-revert) are ruled wrong — see the `#336` body. **Decision:** (a) vs (b), and whether the answer generalizes into a durable parity-surfaces concept (gate-rev ≠ corpus-rev) rather than a one-off patch.

**3. LESSONS lifecycle — the ADR-29 reconciliation (`#339`, E3/S9).** The ruling (recorded in `LESSONS.md`, 2026-07-16) proposes a **chronological** legacy split (move a contiguous older block byte-unchanged into `LESSONS-legacy-<period>.md`, leave a pointer) — which is **distinct from the by-topic split ADR-29 rejected**, so it stays UNsanctioned until ADR-29 is formally amended/superseded. **Decisions:** (i) the split *threshold* — a hard line/entry count vs the softer navigation-pain trigger; (ii) whether a read-only helper enumerates the split boundary; (iii) draft the ADR-29 amendment that sanctions chronological-but-not-topical archival. This is the append-only-record doctrine (ADR-29/39) meeting a real navigation-scale problem.

**4. codex-review consolidation — the global-infra question (`#338`, E7).** Five folded items; the load-bearing one is **(c): bring `~/.claude/bin/codex-review.ps1` + the `/codex-review` command under version control / a deploy carrier.** This is per-machine, un-versioned global infra → it needs a **core-invariant #6 ruling** (global-infra edits are exception-with-ruling, never unilateral). The meta-question: *how does fleet methodology take ownership of per-machine Claude Code runtime config* — the same class as `#289` (OneDrive-guard should be hub-owned). Also live: (a) config default `sol` vs doctrine `terra` (because the code path passes no `-m`), and (e) the `.ps1` sandbox-halt vs the native `codex exec review --base` path.

**Cross-cutting:** the through-line is the ecosystem crossing from **hub-only enforcement to a fleet/satellite mesh** (ADR-28 Layer-2 governing all of `Dev/`). Questions 1, 2, and 4 are all facets of "how does the hub's methodology reach and stay in-sync with N consumers without the hub reaching into their trees." A standing older thread worth a decision if bandwidth allows: **`#162`/S1** — the "architect" actor-vs-mode vocab collision is still live (the model decision, not just the boot-ack slice).
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
