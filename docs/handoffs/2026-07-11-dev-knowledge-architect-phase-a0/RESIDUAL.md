# Residual — 2026-07-11-dev-knowledge-architect-phase-a0 — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
All drift-flags standing at this wrap are **pre-existing dispositions** carried in `ecosystem/disposition-register.yaml` — the no-ff journal-wrap set, the BACKLOG history-accretion set, and the handoff-process undeclared-edge set. This closure arc introduced **NO new drift**: every gate ran green and every WARN was already dispositioned; nothing was self-induced. Do not trust these words for the live picture — **P4/P6/P7/P9 re-derive** the ship-gate verdict, the WARN count, and any `[stale]`/drifted `#id`; this bundle states none of those values by construction.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
- **Intake pipeline (ADR-98):** intakes **#10/#11** (C4 memo, divergence register), **#12** (ownership manifest — #328 charter), **#13** (plan-of-record, now **v3**) — `docs/intake/`.
- **Fleet-parity register ACCEPTED** (§9a hub `.methodology.yaml` YES; §9b `review_date` advisory-WARN v1) + E6 follow-ups **#327–#331** filed — `BACKLOG.md`, `docs/audits/2026-07-11-technical-fleet-parity-register.md`.
- **#326** ARCHITECTURE→CC-facing (hub leg, closed **#165**); **v1.3.1** cut re-pointing **#318/#319** fixes; both consumer deployed-version rollouts; E-prefix epic ids **E1–E7**.
- **This closure arc:** fleet **structure-comparison** audit; **f1 `temp/`** delete EXECUTED (register amendment); intake #13 → v3; this handoff.
- Detail lives in `JOURNAL.md` (2026-07-11 day-anchor + closure addendum) — this is a map, not a recap.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Immediate — Phase A0 (THIS bundle's job): seven operator rulings, settled by hand across all three repos:**
1. **Audit-filename convention winner** — hub lowercase vs corp `_AUDIT_`/`_BRIEF_` (ADR-101 R4 already leans lowercase); if a rename is ruled, an **ADR-100 referential-currency scan gates every move**.
2. **ONE ruff-config form** — three exist today (hub `.ruff.toml`, corp `.ruff.toml`, ai-council `assets/ruff-pre-commit.yaml`); pick one, declare the rest.
3. **`.vscode`** — carried-template vs local (hub-only today).
4. **Consumer BACKLOG schema (#331)** — apply the E-prefix/S-n story-map to ai-council + corp if ruled.
5. **Command-roster target** — codex-review leftover archived; `/evolve` + `/save` disposition per **#325**.
6. **CLAUDE.md archived-reference cleanup (#330)** — boot/evolve refs → `templates/archive`.
7. **Remaining register rows** — each to parity or a `.methodology.yaml` declaration.
Per-edit **doc2doc / doc2file / doc2code / code2code** hygiene runs through the existing edge validators. **A0 exit promotes intake #12 DRAFT→settled template** (the checker then encodes a fixed target).

**Then — carry-open, in plan-of-record order (intake #13 v3 is the full spec):**
- **#328 = Phase A1** (after A0): ownership manifest + `fleet_parity` WARN-check (hub-included per §9a) + hub `.methodology.yaml`; **the JSONL event schema is born here** — least-commitment (store/viewer deferred to Phase E). First bounded **Codex-producer pilot** candidate, CC-verifies contract.
- **Phase D consumers** — **#329** VS Code ownership colors GENERATED from #328 (never hand-set); **#327** protocols-as-interface genre ruling (+ corp `protocols/`, closing #314); **#330/#331** (A0 executes parts of both).
- **Phase C = manifest v1.4.0** carrier-debt paydown: **#315** durable INSTALL.md carrier · toc-freshness re-scope + hub-toc-hooks waiver retirement · **#325** /save carrier — ONE tag-ancestry-verified release (the v1.3.1 lesson), rolled to both consumers; waiver count should DROP.
- **Phase E = observability, REQUIREMENTS-FIRST:** a functional-requirements pack (adoption-telemetry — are carried hooks/skills/gotchas actually USED per repo; hub-side consumer-log collection at 5–8+ repos; PULL-vs-PUSH hermetization; retention; privacy) → **AI-Council architecture decision-gate if a genuine fork, else the architect rules** (libraries-not-platforms) → only THEN the #322 dashboard.
- **Phase F / EPIC-H** — Opus/Sonnet/Haiku + Codex sol/terra/luna variant-routing doctrine, evidenced by this session + the Phase-A pilot outcome.
- **Cross-repo (adjudicate in the OWNING repo's chat, ADR-41):** corp-monorepo pre-existing branch **`docs/backlog-transcript-mime-fix`** (next corp session decides); ai-council **#21** (stale integration test).
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
