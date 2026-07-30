# First live v6 boot — verification report

**Date:** 2026-07-31
**Class:** verification (ADR-101 §2 / R3 closed enum)
**Scope:** the first production use of the HANDOFF_PROCESS v6 one-round-trip boot
**Consumer:** the 2026-07-31 ratification-batch session (this arc) · **consumption_path:** `docs/audits/2026-07-31-verification-first-live-v6-boot-report.md` → ADR-108, the §13(c″) amendment (`64893913`), and rows [#449]–[#452]
**Status:** RECORD ONLY — this report transcribes rulings already made; it makes none.

> **Filename note (ADR-101, mandatory citation).** The commissioning brief named this file
> `docs/audits/2026-07-31-first-live-v6-boot-report.md`. That name carries **no CLOSED-enum
> `<class>` token** after the date, and `validate_hermetization.classify()` refuses it (Rule B,
> prospective-only on staged ADDs). Filed under the conforming grammar
> `<date>-<class>-<slug>.md` with class **`verification`** — evidence *about* state. The
> deviation is the naming grammar only; content and placement are as commissioned.

## 1. The boot ran one round-trip, and the evidence-block mechanism worked as designed

v6's central claim is that **the transport count changes, the proof threshold does not**: one
CC-side command runs the whole live gate and emits **one** evidence block, which the operator
pastes **once**. In its first production use that held — the boot completed on a single
round-trip, and the evidence block was produced and consumed without a second exchange.

**Probe count — a correction, not a transcription.** The commissioning brief records
**"16/16 PASS"**. The repo does not corroborate 16. The live bundle
`docs/handoffs/2026-07-31-dev-knowledge-architect-2/PROBES.md` carries **14** probe rows —
`P0a · P0b · P0c · P1a · P1b · P2 · P3 · P4 · P5 · P6 · P7 · P8 · P9 · P10` — and `audit.py`'s
`handoff_probes` check independently reports **"14 probe(s) bind to live state"** for that
bundle. So the verified figure is **14**, all binding. The "16" is recorded here as an
unreconciled discrepancy rather than silently adopted or silently dropped: it may count legs the
evidence block emitted beyond the manifest rows, which is not checkable from the repo. **What is
verified: 14 probes, all bound. What is not: the 16 figure's provenance.**

## 2. Seam witnessed and ruled — `Destination = main` vs §13(c″)

The bundle's own `Destination` row declared branch **`main`**, which the then-current §13(c″)
described as a value outside "a sanctioned lane shape". The outgoing seat surfaced this in
`RESIDUAL.md` §4 as a **spec question and did not patch it** — recorded verbatim in
`JOURNAL.md`:

> the bundle's own `Destination` branch field reads `main`, which is **not** a sanctioned lane
> shape — P3 will PASS at boot and FAIL once the next seat branches.

That is a real defect in the *reading*, not in the bundle: P3 compares once at boot, so a seat
that boots on `main` and branches per act would satisfy P3 at boot and then diverge from a field
that was never meant to track it.

**Resolved by the architect technical ruling of 2026-07-31** (revertable), landed at `64893913`:
the branch field means **BOOT DESTINATION** — where the seat lands at boot — so **`main` is a
legal value** for a primary-tree architect seat, and **lane branches are declared at delegation**,
not in the boot header. `HANDOFF_PROCESS` moved 6.0 → **6.0.1** with its coupled atomic move
(the `CONTRIBUTING` stamp + all six `reconciled_with` edges).

A second in-spec site — the §13 *Destination contract (intake #18 A4)* paragraph — carried the
same "sanctioned lane shape" wording and was reconciled in the same commit; leaving it would have
made the spec self-contradicting.

## 3. A1 budget scope — VERIFIED, not a defect

The A10/A1 byte budget governs **`protocols/HANDOFF_BOOT.md` only**. Measured this arc:
**16,840 bytes against an 18,000-byte budget** (the gate's LF-blob measurement; the working tree
reads 17,082 bytes because it carries CRLF). `audit.py check_boot_byte_budget` reports OK, and
the budget value is single-sourced from `assemble_paste.HANDOFF_BOOT_BYTE_BUDGET` rather than
duplicated in the checker.

This is recorded as a **verification of intended scope, not a defect**. The budget was never
claimed to cover the assembled paste; that the paste is ungoverned is a separate, deliberate
gap — filed as [#449], not treated as a failure of A1.

## 4. Open questions filed as candidate rows

Filed this arc at `6bfa544f`, each grep-verified as previously unowned:

| Row | Subject | Shape |
|---|---|---|
| [#449] | Assembled-paste byte budget — should `PASTE_THIS.md` gain a hard ceiling? | question, no ruling |
| [#450] | Per-section intake ratification — the doc-level `status:` field | question, no ruling |
| [#451] | CA layer-edge check — port the ai-council precedent | gap; standard already ruled |
| [#452] | `[#433]`→`[#382]` dependency is prose-only — no `depends-on` clause | gap |

[#451] is **not** an open question about whether Clean Architecture applies: the operator ruling
of 2026-07-31 (ADR-108, intake #22 §B) settles that it stays a standing standard **as written**.
The row exists because the **enforcement organ is missing**, with the ai-council layer-edge review
named as the precedent to port.

[#452] was filed as a new row rather than a cross-reference on [#424] after testing the
distinction: [#424] owns `depends-on` clauses that **exist but fail to parse**, and neither
`tasks/433-*` nor `tasks/382-*` carries such a clause at all — so [#424]'s Done-when passes
without ever reaching this pair.

## 5. Honest limits of this report

- It records rulings; it makes none.
- The one-round-trip and evidence-block claims describe a session this report did not observe
  directly. What is repo-verifiable — probe manifest, probe binding, byte budget, the spec text
  and its version — was re-derived live and is cited above. The **16/16** figure is the one load-
  bearing number that could **not** be reproduced, and it is flagged rather than repeated.
- n=1. One successful boot is not a demonstrated success rate.
