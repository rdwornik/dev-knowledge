# Dispatch stamp — NIGHT N3 · intake #35–#39 ratification pack (drafts only)

<!-- scope: meta -->

**Class:** technical · **Date:** 2026-08-19 · **Lane:** night research lane, claude cloud channel
**Branch:** `claude/n3-ratification-pack-35-39-nhqkd3`
**Posture:** read-only + drafts. No status flips, no births, no ADR files, no BACKLOG/tasks
writes, no merge.

This file is the **verbatim dispatch prompt** as received, stamped as the first commit of the
lane per the contract's own instruction. It is the contract of record for
`docs/audits/2026-08-19-technical-n3-ratification-pack.md`; that file is the deliverable.

---

## Prompt as received (verbatim)

```
NIGHT N3 — INTAKE #35–#39 RATIFICATION PACK (drafts only) · cloud, read-only + drafts
Night research lane, claude cloud channel. FIRST COMMIT = dispatch-stamp: this prompt as `docs/audits/2026-08-19-technical-n3-ratification-pack-contract.md` on your `claude/*` branch. DRAFTS ONLY: intake `status:` fields stay DRAFT, no rows are born, no ADR files are created — everything lands inside ONE pack artifact for the seat to execute tomorrow.
CONTEXT: the bundle Purpose owes ratification of DRAFT intakes #35–#39 into ADRs + rows. The seat's anti-orphan rule (ruled, reviewer-approved): each intake, on flip to ACCEPTED, carries either ≥1 carrier row or `disposition: deferred` with a LIVE, DATED trigger — never ACCEPTED-with-zero-carrier (that is the census's L4 FAIL class). Ledger headroom after batch 1: closures 6 / window births 3 → net +3, so up to ~5 births stay lawful tomorrow; draft accordingly and say the arithmetic in the pack.
ITEMS — per intake (#35 agent instruction layers · #36 repo autonomy/policy-as-code · #37 machine-verifiable Done-when · #38 fleet config standardization · #39 off-machine substrate), CLEAR/BLOCKED each:

1. One-paragraph ratification summary: what is being accepted, in force-of-what (ADR vs rows).
2. Draft ADR text (house ADR format) where the intake carries a decision; or "no ADR — rows only" with the reason.
3. Draft carrier row(s) in exact gen_task_tree source form (id left as `#RESERVED`), sized, themed, serialize-grouped — for #38 the kernel carrier row (intake #38 → dev-knowledge-kernel) is MANDATORY in the pack: it is the fleet's oldest ACCEPTED-unfiled debt; if the ledger squeezes it, draft the deferral WITH a dated trigger instead, never silence.
4. Or draft deferral: `disposition: deferred` + the LIVE trigger, dated.
5. Cross-check: for #39, state which content #554 already carries (avoid a duplicate row — #554 stays open on its D1/D2 proof only).

OUTPUT: `docs/audits/2026-08-19-technical-n3-ratification-pack.md` — 5 intake sections + the ledger arithmetic + a suggested execution order for the seat. Commit, push, STOP packet. NOT: no status flips, no births, no ADR files, no BACKLOG/tasks writes, no merge.
```

---

## Scope reading (lane's own, not part of the prompt)

- **Deliverable:** exactly one pack artifact + this stamp. Every draft (ADR text, carrier
  rows, deferrals) lives *inside* the pack as fenced blocks — never as a live file.
- **`#RESERVED`** is the literal id placeholder in every drafted row; the seat allocates
  real ids at execution time.
- **Anti-orphan rule** is the acceptance test for each of the five sections: ACCEPTED must
  carry ≥1 carrier row **or** `disposition: deferred` + a live dated trigger.
- **CLEAR/BLOCKED** verdict is required per intake.
