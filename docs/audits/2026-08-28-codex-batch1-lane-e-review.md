# Terra pre-merge review — batch-1 lane L5 (`lane-e-613-routing-table`)

- **Reviewer:** `gpt-5.6-terra` via `codex exec` (codex-cli 0.145.0)
- **Lane:** L5 — `[#613]`, in-repo routing table + L0 agreement check, under Z-G3 amendment A2
- **Date:** 2026-08-28

## TALLY (as returned by the reviewer)

```
TALLY: critical=0 high=2 medium=0 low=0
```

## Property check the reviewer returned

```
P1  FAILs on divergence, never skips        FAILS (contested — see HIGH-1)
P2  absent L0 is a named report, not a pass HOLDS
P3  a role L0 omits is a divergence         HOLDS
P4  the lane writes nothing to ~/.claude/   HOLDS
P5  ratchet: zero must|shall|never added    HOLDS
```

## Findings, with the lane's disposition

### HIGH-1 — ship-tier registration + `warn` on an absent L0

**Disposition: PARTIALLY REFUTED against the frozen contract; the tier choice DEFENDED and
documented; the live divergence SURFACED rather than left to ship-tier.**

The contract's own wording distinguishes the two cases terra merged into one: *"FAILS (never
skips — Z-G4) when L0 copy **diverges**; degrades to a named report, not a pass, when L0 is
**absent**."* The implementation matches that verbatim — `fail` on divergence, `warn` on
absence. A `warn` is not a skip and not a pass: it blocks `ship-gate` unless explicitly
dispositioned, and the code deliberately refuses `unavailable`, which `_check_outcome`
projects onto `pass`.

On the **tier**, terra's challenge is the right one to ask and deserves a direct answer.
`[#592]` set the evidence bar — *"MEASURED BEFORE ARMING … the check measures 0 findings, so
arming its FAIL leg cannot RED a clean tree"* — and this organ **does not clear it**: the live
L0 diverges **right now**, because the derived copy has never been written and writing it is
the operator's act, which this lane's contract names as an anti-pattern. A COMMIT-tier FAIL
would therefore wedge every commit in the repository on a file the repository may not touch.
Ship tier is the declared, precedented response (`[#597]`), the verdict stays `fail`, and the
reasoning is written into the adapter's docstring rather than left in a review.

**Surfaced, because ship tier should not bury it:** the live scan returns **`diverge` on all
four roles** — `~/.claude/ROUTING.md` exists but does not yet carry the derived rows. That is a
real operator action item, not a latent risk, and it is reported here and in the end-of-batch
packet.

### HIGH-2 — the comparison could produce FALSE AGREEMENT

> *"An L0 document can describe `reviewer: claude-code` while mentioning `codex` under an
> unrelated role, producing false agreement for reviewer."*

**Disposition: VALID. FIXED in this lane.**

Correct, and it is the one outcome this organ may not produce — certifying agreement about
precisely the binding it got wrong. The original `compare()` searched the whole document for
each CLI independently, so any stray mention anywhere corroborated any role.

Comparison is now **region-scoped**: a region starts at a line naming the role and ends at the
next line naming a *different* role, or three lines later. A CLI corroborates a role only if it
appears beside it. Pinned by
`test_a_cli_named_elsewhere_does_not_corroborate_a_role`, which constructs exactly terra's
scenario — `reviewer` bound to the wrong CLI with the right one present under another role —
and asserts divergence.

## Contract defect D1, confirmed by measurement

The frozen contract's L5 done-contract item 3 asserts *"Ratchet untouched (ecosystem/ + code
are outside its scope roots — **verified, not assumed**)"*. It is **false**, and the batch
caught it at dispatch rather than at commit time: `silent_rule_detector._SCOPE_RULES` carries
`("ecosystem", False, (".yaml",))`.

**Measured proof rather than argument:** with the new table staged, the detector's file count
moves **60 → 61** — the file is unambiguously in scope — while the count holds at
**443 = 443, delta 0**, because the table was authored with **zero** `must`/`shall`/`never`
occurrences. Had it been written in ordinary normative prose against a baseline with zero
headroom, it would have RED `audit-health` and blocked the commit.

## Verdict

**MERGE-ELIGIBLE.** No critical findings. HIGH-2 fixed and pinned by a test; HIGH-1 answered
against the contract's own text, the tier defended on the `[#592]` arming bar and documented in
code, and the live L0 divergence surfaced as an operator action item.
