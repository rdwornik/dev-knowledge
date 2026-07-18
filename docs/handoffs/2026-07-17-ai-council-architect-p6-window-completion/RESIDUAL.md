# Residual — 2026-07-17-ai-council-architect-p6-window-completion — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the ai-council `BACKLOG.md`, §6). Mode: **architect** (§13); the session's WORK is a small **product BUILD** (the D2 parity pair + the night-finding hardening fixes #39–#43). **Target repo: ai-council** — this bundle is hosted in the hub (ADR-36/42), derived READ-ONLY from `../ai-council`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the ai-council plan-of-record / JOURNAL / git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED** by the outgoing session CC (P4-wave close + night batch + morning close); the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"* (not full).

---

## §1 — Prior session CLOSED CLEAN; the P6 completion wave is #22/#23 → #39–#43 → #27 (THE HEADLINE)

**The P4 build wave is done AND the session closed clean.** `recall`: doctor (**#25**), CLI seats claude+codex (**#16**), verdict package (**#26**) all shipped; then the session closed properly — a **pre-authorized unattended night E2E audit** (zero stop conditions fired) + a **supervised morning close** landed four more merges on `main`: night deliverables → a durable **synthesizer swap** (`defaults.synthesizer: gemini → openai`, gated green, terra-waived — codex credits exhausted to 2026-07-23) → doc-currency + BACKLOG hygiene (**#31 struck, #24 closed by operator ruling, #39–#43 filed**) → JOURNAL. **P1 re-derives HEAD live** — it has moved well past the P4 merges; do not trust any sha in prose. The sidecar seam rule held: `seats[]` (#16) defined the `_metrics.json` extension mechanism; the verdict package (#26) consumed `seats[]`/`synthesis` **by reference** via a shared `_seat_payload` serializer.

**The P6 completion wave, in order.** Canonical sources: ai-council `BACKLOG.md` (#22/#23 ready-slack) + `protocols/COUNCIL_INVOCATION_CONTRACT.md` §7 (Known deviations) + the night audit `docs/audits/2026-07-17-night-batch-empirical-e2e-audit.md` §4.2 gap-map (the next-wave menu — POINT at it, do not re-narrate it).

1. **Ready slack — #22 + #23 (the ADR-11 D2 parity pair, both UNBLOCKED).** **#22** — `--file` parses YAML frontmatter via the same `parse_file()` path as inbox (precedence flag > frontmatter > config default; no frontmatter leaks into the question text). **Likely quick:** the `--file` gap "falls out of" the `cli.py:main` `@click.group` decomposition that **already landed with #25 (A2)** — structural basis exists; a small wiring + test task. **#23** — research mode honors `--return-dir` (`run_research` gains a return-dir copy; canonical `./output/` always; re-confirmed empirically open by the night batch). **Closing both empties CONTRACT §7 → triggers the DRAFT-INT-2 `1.0` version stamp** (per L-INT Q7: a `1.0` shipped with known deviations "would make the first version a lie") — at which point the verdict package's `contract_version` field (currently `null`, shipped by #26) starts echoing `1.0`. **That is P6 window completion.**
2. **Night-finding hardening — #39–#43** (all filed from the night E2E audit; harden the artifact surface): **#39** no-persist/scratch output mode + bounded `output/health/` retention (witness runs pollute canonical `output/`); **#40** fix the verdict-package `options_considered` extractor (empty on picks, polluted on ideas); **#41** CLI-seat token-count regexes (codex records 0, claude under-reports input); **#42** research-path double-prefix filename; **#43** first-class `codex` seat name in the provider registry (it rode `deepseek` in the night batch).
3. **Follow-on centerpiece — #27 CLI-4 parity** (n=12 stratified, sealed-key blind, rubric-scored). Prereq #16 landed; the night batch's zero-fallback CLI E2E de-risks it. **Un-gates the ADR-12 §5 default-flip.**

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P4), not in trusting these lines.** This bundle states **no** sha, count, armed-state, or task-line text.

---

## §2 — The #26 residuals + seam constraints still in force (the design context)

**#26 (verdict package) shipped debate-path-only and filed three residuals — do NOT redo, but know they exist:**
- **#33** [P3][S] — **terra pass-3 re-verification, DATE-GATED on/after 2026-07-23.** #26's terra pass-3 was **explicitly waived** (codex credits exhausted mid-gate); pass-1/pass-2 were clean-on-substance after fixes, the two pass-2 fixes are strictly reductive + unit-tested, and the waiver was offset by a fresh live re-witness on the shipping code. #33 runs `codex-review.ps1 -Topic verdict-package-pass3` when credits reset — belt-and-suspenders, not a blocker.
- **#34** [P3][M] — research-path verdict-package parity (R6): `run_research` emits no `council-verdict-*.json` (debate-path only). A Lane A **research** commission gets no transcript-free deliverable until this lands.
- **#35** [P3][S] — broad R4 fail-loud return-dir for transcript/minority (#26 made only the *verdict* raise `OutputRoutingError` on a required-return-dir miss).

**Seam constraints unchanged (design against, never redesign):** the five cross-lane seam contracts are canonical in ai-council `docs/intake/2026-07-06-technical-architect-intake.md` §3. `output.py` remains the highest-contention module (now carries `save_to_file`/`_build_header`/`_build_body` + the verdict package + `seats[]` sidecar via `_seat_payload`) — serialize any work touching it. **Do-not-touch reference module: `healthcheck.py`.**

---

## §3 — Carried residuals (still live — NOT re-derivable from the repo alone)

**(a) G3 / Epic B is RESOLVED — by operator ruling, not by scoring.** `#24` (EPI-1 archaeology) is **CLOSED by operator ruling**. The G3/Epic-B event is the recorded **synthesizer ruling** — ai-council `docs/audits/2026-07-17-synthesizer-ruling-gemini-to-openai.md` (durable `defaults.synthesizer: gemini → openai`, ratified on the night batch's 4/4 empirical corroboration). The EPI-1 40-item pack + sealed key are **RETAINED UNSCORED as the standing reversible instrument** (`docs/audits/2026-07-17-epi1-archaeology/`) — reopen the scoring only if evidence later argues to reverse. **Epic B is formally un-gated:** #2 Branch A (openai) shipped as the durable config default (ADR-01 amendment text pending), and **#18/#19 planning is deferred to a dedicated planning session** on the un-gated baseline — do NOT re-score, re-rule, or start #18/#19 design in this window-completion chat.

**(b) The two consumer→hub NEEDS-RULING intakes — both hub-tracked, ruling pending (do NOT re-plan them here).** Filed locally in ai-council `docs/intake/`, carried across the boundary to the hub (the sanctioned consumer→hub path):
- `2026-07-17-hub-feedback-codex-producer-lane.md` (EPIC-H) — Codex-as-PRODUCER vs the global read-only `~/.codex/AGENTS.md` policy + the Windows write-sandbox. **Hub-tracked as `.dev-knowledge` BACKLOG #341** (per-invocation producer activation without global-infra edits).
- `2026-07-17-hub-feedback-session-close-gate.md` — (Ask 1) the Stop-gate must **mechanically block handoff-bundle generation** until session-close criteria hold (this very bundle was generated mid-session and had to be updated post-close — the exact failure mode); (Ask 2) a **consumer-session guard against hub/global writes**. **Hub-tracked as `.dev-knowledge` BACKLOG #343** (filed this hub session). Both await an operator ruling — a HUB session's work; the browser should not re-plan them.

**(c) Interim Codex-producer fallback — IN FORCE (operator ruling 2026-07-17).** Until the hub reconciles #341: **bounded build tasks run as CC-implements + terra read-only review (`codex exec review`) pre-merge.** This shipped #25/#16/#26 cleanly (terra caught real defects each arc). **Apply to #22/#23 + #39–#43:** CC produces; terra reviews read-only; never plan Codex to write. **Terra-rate-limit lesson:** codex `exec` can hit its usage cap mid-gate (credits exhausted to **2026-07-23**) — if it does, the pattern is an **explicit recorded waiver + a filed follow-up** (like #26 pass-3 → #33), never a silent skip.

**(d) §6.3 scope-boundary fork — still awaiting an explicit ruling.** The plan-of-record / consolidation-brief §6.3 fork (pure-governance vs thinking-aid scope) is implicitly held at "pure governance" but **NOT formally adjudicated** (night audit §4.2) — the one fork worth an explicit ruling. Carry-open; not this window's job unless the operator raises it.

---

## §4 — Next-frontier (the design "why" that travels)

**Primary — close the ADR-11 D2 parity window (#22 + #23) → stamp DRAFT-INT-2 `1.0`, then harden (#39–#43), then #27 parity (§1).** The whole-system view the architect must hold: #22 likely falls out of the already-landed A2 `@click.group` decomposition (small); #23 threads `return_dir` through `run_research`; closing both empties §7, the sole precondition for the `1.0` stamp — at which point the verdict package's `contract_version` field starts echoing `1.0` instead of `null`. #39–#43 harden the artifact surface (output-guard / extractor / token-regexes / naming / seat-identity) — the night E2E audit's concrete findings, sized S each. #27 (CLI-4 parity) is the follow-on centerpiece that un-gates the ADR-12 §5 default-flip. Lane parity is a standing contract obligation (L-INT R6): any behavior added to Lane A states its Lane B disposition (#34 is the one place the verdict package is not yet lane-complete).

**Carry-open (do NOT redo / re-decide in this chat):**
- **#33 (terra pass-3)** — date-gated on/after **2026-07-23**; run it then, do not force it early (codex credits). Any other terra-gated review is likewise blocked until the reset.
- **G3 / Epic B is RESOLVED by ruling (§3a)** — #24 closed, the EPI-1 pack retained as the reversible instrument. Do NOT re-score or re-rule; #18/#19 planning is a **separate** dedicated session on the un-gated baseline.
- **The two hub NEEDS-RULING intakes (§3b)** are hub-tracked (#341 codex-producer, #343 session-close-gate) — a **hub** session's ruling; use the interim fallback (§3c) meanwhile.
- **The §6.3 scope-boundary fork (§3d)** — awaits an explicit ruling; not this window's job unless raised.
- **[S13]/#36–#38 (caller-side commissioning advisor, filed by RIDER 2)** — the front half of the delegation window (authoring → decomposition → verdict→ADR read-back), companion to the council-side surface [S10] delivered. Filing only; build when prioritized. #36 must reconcile with #9 (the ADR-67 quality gate, [E6]-deferred), not duplicate it.
- Any **methodology / hub** question → the hub `.dev-knowledge`.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the ai-council **`BACKLOG.md`** (story-map, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P2; the ready-slack #22/#23 read live, `PROBES.md` P4) + the frozen **`docs/intake/2026-07-16-plan-of-record.md`** phase→task map (**P6 = #22/#23**) and the night audit **`docs/audits/2026-07-17-night-batch-empirical-e2e-audit.md`** §4.2 gap-map (the next-wave menu), the live branches (`git branch -v` — P1 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. **New since the P4 close (morning close of the night batch):** **#31 struck** ([S12] delivered), **#24 CLOSED by operator ruling** (G3/Epic-B = the synthesizer ruling; EPI-1 pack retained as the reversible instrument), **#39–#43 filed** from the night E2E audit; #2 Branch A (openai) shipped as the durable config default (ADR-01 amendment text pending). Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **The anti-bluff PROBES manifest (`PROBES.md`, P1–P4) is the load-bearing carrier.**
