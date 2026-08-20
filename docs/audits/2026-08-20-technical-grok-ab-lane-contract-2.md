# Lane contract of record — Grok 4.6 A/B on the C1 seeded-defect pack (admission trial)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-20 · **Slug:** grok-ab-lane-contract-2
- **Lane:** worktree `ab-grok46-2` · **Branch:** `worktree-ab-grok46-2` · **Base:** `main` at `1def12f6`
- **Status:** dispatch stamp. This file is the frozen contract as dispatched, committed verbatim as
  the lane's first commit per ADR-110. It is an immutable audit artifact; the lane's product is
  `docs/audits/2026-08-20-technical-grok-ab-results-2.md`.
- **`-2` suffix:** the operator's dispatch directs this lane's contract-of-record to carry a `-2`
  suffix because a prior attempt at this lane was aborted. **Checked, not assumed:** `git ls-tree -r
  main --name-only | grep -i grok` at `1def12f6` returns only
  `docs/audits/2026-07-31-technical-382-w2-grok-shadow-ab.md` and
  `tasks/492-grok-review-lane-acceptance-gated-2026-08-07-mea.md` — the aborted attempt committed
  nothing, so there is no collision to avoid and no prior contract file to reconcile against. The
  suffix is carried anyway, as dispatched, and is extended to the results artifact so both of this
  lane's outputs are traceable to one attempt.

---

## Contract as dispatched (verbatim)

# LANE — GROK 4.6 A/B ON THE C1 SEEDED-DEFECT PACK (admission trial)

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**Worktree lane, commit-and-STOP.** ADR-110: commit this prompt first as
`docs/audits/2026-08-2X-technical-grok-ab-lane-contract.md` (today's date).

PRECONDITION P0 (hard): `$env:XAI_API_KEY` must be set by the operator before dispatch — if
absent or the API rejects it, STOP immediately with the exact error; never source a key from
anywhere else. This is the sanctioned auth path for xAI (no subscription-OAuth CLI exists for
Grok; the Google no-API-key ruling does not transfer here — operator-approved).

CONTEXT: pack on main `docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md` (read fully).
Admission bar RULED: `ADMIT iff G1 and G2 and G3`, no partial admission. Operator mandate:
**Grok 4.6 exactly — never 4.5, never any substitute.**

STEPS:
1. **P-item version probe:** call the xAI API (chat completions, model `grok-4.6`,
   reasoning_effort high) with a trivial prompt; assert the RESPONSE's model field reports
   grok-4.6 verbatim. Record request + response fields in the artifact. Any other served model
   = STOP with evidence.
2. Fill §4.2 invocation lines: incumbent fan-out CLI vs `grok-4.6` via direct API calls
   (stdlib/requests one-shot per item; temperature and effort recorded; no retries that could
   mask variance).
3. Run ALL 14 items both sides, raw outputs verbatim per item; score G2/G3 mechanically per
   the pack rubric (trap items C1-R4/C1-R5: fabrication = heavy penalty).
4. Refusal items C1-N1/C1-N2: capture raw outputs VERBATIM, DO NOT score — G1 stays
   ARCHITECT-PENDING.
5. Artifact `docs/audits/2026-08-2X-technical-grok-ab-results.md`: probe evidence, invocation
   lines, per-item table, computed G2/G3, raw N1/N2, token spend total in USD — NO verdict.
FINAL: targeted checks, commit-and-STOP. NOT: no routing-table edits, no verdicts, no
score-improving reruns (first run counts), no key echoed anywhere in the artifact.
