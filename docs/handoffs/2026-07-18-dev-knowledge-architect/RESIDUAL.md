# Residual — 2026-07-18-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED** with this session's operator rulings (transcribed VERBATIM — RULING-W/S/PY/CF + the `#329` and `#341-R2` inputs + the satellite freeze). Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*. **Read the SUPPLEMENT ANSWERS first** — they are the binding off-repo "why" for ARC 4 that the repo structurally cannot carry.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Every standing WARN this window is pre-dispositioned in `ecosystem/disposition-register.yaml`; the 2026-07-18 serial-integration close-out introduced no NEW undispositioned flag** — `#337` merged ship-gate-GREEN and the one new WARN it surfaced (`#344`) was dispositioned in the same arc. Re-derive the live verdict/count/`[stale]` via P7 — do not trust this framing. The standing families, by reference (all carry register entries):

- **`no_ff_merges`** — three grandfathered direct-on-`main` commits (`warn-no-ff-3a894eeb5` / `-d0f9ead67` / `-533109f`), each dispositioned; historical, pre-date the `block-ff-push` prevent organ. This window's four integration merges were all `--no-ff` — no new direct-on-`main` commit.
- **`doc_rot` (backlog-accretion)** — the long-lived tickets `#262 / #278 / #328 / #332`, **plus NEW-this-window `#344`** (`warn-doc-rot-backlog-344`, `review_date: 2026-08-18` shelf-life — the `#332` A0-seal precedent for a load-bearing NEEDS-RULING task condense-deferred). Trimming is the standing kill-lever, not a gate failure. **Watch:** any edit pushing another task past the 1200-char threshold mints a NEW WARN (the [[backlog-edit-doc-rot-threshold]] class) — keep task edits net-neutral.
- **`undeclared_edges`** — six `*-handoff-process` prose edges (`BACKLOG / VISION / ESSENTIALS / PLAYBOOK / SESSION_SETUP / AI_COUNCIL_PROCESS`), all `warn-undeclared-*` under `#241`; deferred structural work, not fresh drift.
- **`reconciled_versions`** — the `CONTRIBUTING-md-template.md` malformed-stamp WARN under `#335`, dispositioned.
- **`fleet_parity` — CHANGED THIS WINDOW: it is now a BLOCKING `ALL_CHECKS` member (`check_fleet_parity`, `#337`), no longer the informational-only surface the last bundle described.** Its verdict→status map: FAIL on refused/must-absent/tombstone-violated, WARN→RED on warn-undeclared/unavailable/tracked-ephemera; stale-declaration + advisory-rewarn stay advisory-but-visible (a date/corpus advance never REDs). The promotion REDs nothing live today (STOP-condition honored at merge). The one live `warn-undeclared` parity surface remains corp-monorepo `precommit-hub-block` rev-vs-`source_tag` — the `#336` split-state, the sole thing between the fleet and a true zero-WARN steady state. Re-derive the live surface via `python scripts/fleet_parity.py`. **Perf note:** the walk (~8.3s in-process) now runs on every hub pre-commit via `audit.py health`; scoping it to ship-gate-only is the filed `#343` (RIDER-2 follow-up).

**Disposition hygiene:** if the next session CLOSES a task that owns a doc_rot disposition (e.g. `#344` on a ruling, or `#328/#332` on the deploy carrier), remove the register entry in the same arc or P7 prints a `[stale]` line (the [[close-backlog-orphans-disposition]] class).
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map — detail lives in `JOURNAL.md` (2026-07-18 entries) and `BACKLOG.md`; this is pointers only. This was a **serial-integration close-out** (the day's parallel work landed to a quiet primary), not a build session.

- **`#337` CLOSED — fleet_parity promoted to a blocking `ALL_CHECKS` member** (ADR-101 data plane; ADR-102 gate-rev axis). `check_fleet_parity` + the extracted `fleet_parity.walk()` seam; `ALL_CHECKS` 29→30, doc-counts regen (30 checks / final suite **1595 passed / 3 skipped**), ARCHITECTURE status flip + re-stamp. Merge `--no-ff` **`6673904f`**. One codex-terra P1 (bare `import fleet_parity` broke package-mode `python -m scripts.audit`) fixed pre-merge.
- **corp-monorepo architect handoff integrated** — the hand-authored cross-repo bundle (`docs/handoffs/2026-07-18-corp-monorepo-architect/`), merge `--no-ff` **`7ff9b89e`**.
- **ai-council P6-window handoff integrated + `#343`→`#344` cross-session renumber** — the ai-council session's session-close-gate filing collided with main's `#343` (fleet_parity ship-gate scoping); renumbered to `#344`, BACKLOG auto-merged clean (0 dup ids). Merge `--no-ff` **`1eeea5fb`**.
- **`#344` `doc_rot` dispositioned** — load-bearing NEEDS-RULING task, `review_date: 2026-08-18` shelf-life (`#332` A0-seal precedent). Merge `--no-ff` **`54c502fc`**; session-close JOURNAL anchor `3571bd5c`.
- **Filed this window:** `#343` (fleet_parity ship-gate-only perf scoping, RIDER-2) · `#342` (fleet_parity gate-ahead max-fidelity hardening, deferred #336/ADR-102 items). Branch hygiene: every stale/merged branch deleted; **survivors = `main` + `automation/fleet-audit` only**, primary worktree only, no orphan dirs.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The plan-of-record for the next session is ARC 4 — fleet equalization** (the operator-approved prompt file, operator-held off-repo; encoded in `PLAN.md`). Several standing DEFER-pegs converge on one un-happened thing: the hub's methodology actually reaching and equalizing across the consumer repos. **This window landed the operator rulings that unblock it** — they travel **verbatim in `SUPPLEMENT.md` ANSWERS** (RULING-W/S/PY/CF, the `#329` and `#341-R2` inputs, the satellite freeze); read those first, they are the off-repo "why" the repo cannot carry. The open decisions, in rough dependency order:

**1. ARC 4 fleet equalization — and its enabling mechanism (RULING-W).** The equalization work requires the hub to WRITE into consumer trees (methodology/cleanup), which the current ADR-36/41 read-only contract forbids. **RULING-W resolves this: the hub MAY/SHOULD write into consumers via a separate worktree/branch, then report — and the FIRST step of ANY consumer leg is to codify this as the ADR-36/41 amendment (mechanism before act).** So the next session's opening move is not an equalization edit; it is the amendment. **Guardrail preserved:** re-witness consumers live first (their state may have moved), and every consumer write goes worktree/branch → report, never a direct push into a consumer checkout.

**2. `#344` — session-close gate + consumer hub-write guard (NEEDS-RULING).** Ask 1 (a pre-handoff gate refusing bundle generation until session-close criteria hold — audit artifact + doc-currency + operator close-token) and Ask 2 (a consumer-side PreToolUse guard blocking Writes that resolve under a hub/global path). **RULING-W is the doctrinal complement to Ask 2** — it defines the *sanctioned* consumer→hub write path (worktree/branch + report + mechanism-first), so Ask 2's guard should ALLOW exactly that shape and block the unmediated case. The `block-onedrive` guard is the mechanical precedent (`#289`).

**3. `#341` — Codex producer-lane activation. FORK NOW CLOSED by the R2 ruling.** The prior bundle flagged an open fork (per-run codex flag vs repo-local `AGENTS.md` override); **the operator ruled R2: producer-activation = a sanctioned repo-local `AGENTS.md` override (the per-run flag is REJECTED), decided on witnessed precedence evidence.** Remaining `#341` work is implementation, not decision: witness the `AGENTS.md` precedence once, codify the producer guardrails, reconcile PLAYBOOK §16 + the EPIC-H carve-out. Paired reviewer-path drift is `#338`.

**4. Governed-file structure — RULING-S.** Every governed file gets **reader-visible sections** separating methodology-universal from repo-personal content (CLAUDE.md + configs); **machine markers alone are insufficient** — this is the load-bearing constraint on the existing `owner=hub`/`owner=repo` region work (`#312`). The editor-side complement is the **`#329` input**: background decoration of the marked regions via versioned `.vscode` (grey/navy on a dark theme). These are two halves of one "make the hub/repo boundary legible to a human reader" thread.

**5. Standing build queue (execution tickets exist; these are the way-of-working decisions inside them).** `#339` LESSONS legacy-split BUILD leg (threshold + mechanism; still pending the ADR-29 chronological-archival amendment — the ratification landed in the docs, the executed split is the build leg). `#342` fleet_parity gate-ahead max-fidelity hardening (3 items, deferred from #336/ADR-102). `#343` fleet_parity ship-gate-only perf scoping (RIDER-2; the ~8s walk should not tax every pre-commit). `#300` hermetization residual (d.i runbooks / d.ii mode-boot home / d.iii audit-class grammar — DEFER-pegged BEFORE Wave-2). **RULING-PY:** the ruff baseline targets **py311 now** (the corp floor); the standing "always newest Python" direction becomes a filed **fleet-upgrade ticket** (not yet filed — a next-session filing). **RULING-CF:** ai-council adopts the conformance workflow.

**6. The frozen lane — satellite wave.** The 4 satellite onboarding prompts (intake #15) stay **FROZEN until corp + ai-council lessons are extracted** (operator ruling this window). Do not fire the satellite rollout; the Wave-1 consumers (corp, ai-council) are the lesson source ARC 4 harvests first.

**Cross-cutting through-line:** the ecosystem is crossing from **hub-only enforcement to a fleet mesh** (ADR-28 Layer-2 governing all of `Dev/`). RULING-W is the pivot — it converts the read-only hub into a hub that can *equalize* consumers under a mechanism-first discipline. Questions 1, 2, and 4 are all facets of "how the hub reaches and stays in-sync with N consumers, legibly, without unmediated tree-writes." A standing older thread if bandwidth allows: **`#162`/S1** — the "architect" actor-vs-mode vocab collision (the model decision, not just the boot-ack slice).
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
