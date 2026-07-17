# Residual — 2026-07-17-ai-council-architect-p6-window-completion — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the ai-council `BACKLOG.md`, §6). Mode: **architect** (§13); the session's WORK is a small **product BUILD** (the D2 parity pair). **Target repo: ai-council** — this bundle is hosted in the hub (ADR-36/42), derived READ-ONLY from `../ai-council`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the ai-council plan-of-record / JOURNAL / git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED** by the outgoing #26-session CC; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"* (not full).

---

## §1 — P4 wave COMPLETE; the ready slack is the D2 parity pair (THE HEADLINE)

**The P4 build wave is done.** `recall`: doctor (**#25**, merge `6e0782e`), CLI seats claude+codex (**#16**, merge `5d601f4`), verdict package (**#26**, merge `3875068`) — all shipped, `main` pushed (**P1 re-derives HEAD live** — it has moved past `3875068`; the #26 close + the session-wrap merge `3862749` sit on top). The sidecar seam rule held: `seats[]` (L-CLI, #16) landed first and defined the `_metrics.json` extension mechanism; the verdict package (#26) consumed `seats[]`/`synthesis` **by reference** via a shared `_seat_payload` serializer (a terra-Critical finding forced the single-serializer design — no parallel seat schema).

**The ready slack is #22/#23 — the ADR-11 D2 parity closure = P6 window completion.** Canonical source: ai-council `docs/intake/2026-07-16-plan-of-record.md` (P6 row) + `protocols/COUNCIL_INVOCATION_CONTRACT.md` §7 (Known deviations). Two deviations remain:

1. **#22** — `--file` parses YAML frontmatter via the same `parse_file()` path as inbox (precedence flag > frontmatter > config default; no frontmatter leaks into the question text). **Likely quick:** the plan-of-record §6 notes the `--file` gap "falls out of" the `cli.py:main` `@click.group` decomposition that **already landed with #25 (A2)** — so the structural basis exists; #22 may be a small wiring + test task.
2. **#23** — research mode honors `--return-dir` (`run_research` gains a return-dir copy; canonical `./output/` always).

**Closing both empties CONTRACT §7 → triggers the DRAFT-INT-2 `1.0` version stamp.** Per L-INT Q7 / DRAFT-INT-2: the CONTRACT stays version-line-less exactly until the D2 deviations empty — a `1.0` shipped with known deviations "would make the first version a lie." So **#22 + #23 → §7 empty → stamp `Contract-Version: 1.0`** and the verdict package's `contract_version` field (currently `null`, shipped by #26) starts echoing `1.0`. **That is P6 window completion.**

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P4), not in trusting these lines.** This bundle states **no** sha, count, armed-state, or phase-table text.

---

## §2 — The #26 residuals + seam constraints still in force (the design context)

**#26 (verdict package) shipped debate-path-only and filed three residuals — do NOT redo, but know they exist:**
- **#33** [P3][S] — **terra pass-3 re-verification, DATE-GATED on/after 2026-07-23.** #26's terra pass-3 was **explicitly waived** (codex credits exhausted mid-gate); pass-1/pass-2 were clean-on-substance after fixes, the two pass-2 fixes are strictly reductive + unit-tested, and the waiver was offset by a fresh live re-witness on the shipping code. #33 runs `codex-review.ps1 -Topic verdict-package-pass3` when credits reset — belt-and-suspenders, not a blocker.
- **#34** [P3][M] — research-path verdict-package parity (R6): `run_research` emits no `council-verdict-*.json` (debate-path only). A Lane A **research** commission gets no transcript-free deliverable until this lands.
- **#35** [P3][S] — broad R4 fail-loud return-dir for transcript/minority (#26 made only the *verdict* raise `OutputRoutingError` on a required-return-dir miss).

**Seam constraints unchanged (design against, never redesign):** the five cross-lane seam contracts are canonical in ai-council `docs/intake/2026-07-06-technical-architect-intake.md` §3. `output.py` remains the highest-contention module (now carries `save_to_file`/`_build_header`/`_build_body` + the verdict package + `seats[]` sidecar via `_seat_payload`) — serialize any work touching it. **Do-not-touch reference module: `healthcheck.py`.**

---

## §3 — Carried residuals (still live from the P4 bundle — NOT re-derivable from the repo alone)

**(a) G3 is OPEN — the operator's blind-scoring mission, un-gates Epic B.** `#24` (EPI-1 archaeology) is **prepped but unscored**. The overnight 40-item blind-scoring pack sits at ai-council `docs/audits/2026-07-17-epi1-archaeology/`. The operator scores 40 historical syntheses blind, un-blinds with the sealed key, tallies per-author pass-rates (gemini vs openai). The flow: operator blind scoring → a **Beat-1 mini-session** → the **#24 single-recommendation report** (Branch A swap / Branch B keep-gemini) + the operator's **ruling**. **That ruling IS the G3 event = Epic B** — un-gates **#18 / #19 / #9** (+ D12/D13 and the v2 crux-resolver ranking, ADR-13). G3 is **pause-independent**; this window-completion chat does NOT do G3 (operator decision authority).

**(b) Hub-feedback ruling still owed — the Codex producer-lane conflict (NEEDS-RULING).** ai-council `docs/intake/2026-07-17-hub-feedback-codex-producer-lane.md` (EPIC-H): a day-session plan tasked Codex as PRODUCER, but `~/.codex/AGENTS.md` is a global read-only reviewer policy + the Windows write-sandbox can't apply patches → Codex-as-producer is unrealizable without editing hub-owned global infra (core-invariant #6). **The hub owes:** either (a) formally adopt "Codex is review-only; CC produces," or (b) define a sanctioned producer-lane exception. **A HUB session's work** — the browser should not re-plan Codex-as-producer.

**(c) Interim Codex-producer fallback — IN FORCE (operator ruling 2026-07-17).** Until the hub reconciles (b): **bounded build tasks run as CC-implements + terra read-only review (`codex exec review`) pre-merge.** This shipped #25/#16/#26 cleanly (terra caught real defects each arc; the #26 pass-3 waiver above is the one gap, date-gated). **Apply to #22/#23:** CC produces; terra reviews read-only; never plan Codex to write. **Note the terra-rate-limit lesson from #26:** codex `exec` can hit its usage cap mid-gate — if it does, the pattern is an **explicit recorded waiver + a filed follow-up** (like #26 pass-3 → #33), never a silent skip.

---

## §4 — Next-frontier (the design "why" that travels)

**Primary — close the ADR-11 D2 parity window (#22 + #23), against the CONTRACT §7 + the plan-of-record P6 row, then stamp DRAFT-INT-2 `1.0` (§1).** The whole-system view the architect must hold: #22 likely falls out of the already-landed A2 `@click.group` decomposition (small); #23 threads `return_dir` through `run_research`; closing both empties §7, which is the sole precondition for the `1.0` stamp — at which point the verdict package's `contract_version` field starts echoing `1.0` instead of `null`. Lane parity is a standing contract obligation (L-INT R6): any behavior added to Lane A states its Lane B disposition.

**Carry-open (do NOT redo / re-decide in this chat):**
- **#33 (terra pass-3)** — date-gated on/after **2026-07-23**; run it then, do not force it early (codex credits).
- **G3 (#24)** is the **operator's** blind-scoring mission (§3a) — its ruling is the Epic B event. This chat does not score or rule.
- **The Codex producer-lane ruling (§3b)** is a **hub** session's — use the interim fallback (§3c).
- **P5 is now RUNNABLE (evidence-gated):** CLI-4 parity (n=12, `#27`, depends-on #16 which **landed**) → the ADR-12 §5 default-flip decision. #27 can start whenever the operator commissions the parity run; #18/#19/#9 only after G3.
- **[S13]/#36–#38 (caller-side commissioning advisor, filed by RIDER 2 this session)** — the front half of the delegation window (authoring → decomposition → verdict→ADR read-back), companion to the council-side surface [S10] delivered. Filing only; build when prioritized. #36 must reconcile with #9 (the ADR-67 quality gate, [E6]-deferred), not duplicate it.
- Any **methodology / hub** question → the hub `.dev-knowledge`.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the ai-council **`BACKLOG.md`** (story-map, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P2) + the frozen **`docs/intake/2026-07-16-plan-of-record.md`** phase→task map (**P6 = #22/#23**; P6 quote re-derived live, `PROBES.md` P4), the live branches (`git branch -v` — P1 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. **New this session:** [S10] gained #33/#34/#35 (#26 residuals); new story **[S13]** carries #36/#37/#38 (RIDER 2 caller-side advisor); wave tasks #16/#25/#26 **struck per ADR-65** (git carries the record). Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **The anti-bluff PROBES manifest (`PROBES.md`, P1–P4) is the load-bearing carrier.**
