# LANE lane-x-727-fail-closed — deny-and-point fails CLOSED for its matched class, and the row gains the fail-posture clause it never carried

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-727-fail-closed LANE-x-727-fail-closed.md -Effort high -Model sonnet
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #727 · lane-x-727-fail-closed]`. **The model is ON the line, not defaulted** (`[#717]`): it
is rendered from the routing table above, so this lane dispatches at
`sonnet` whatever the surface's own default (`opus`, the
`.dev-knowledge` default per the Ch8 routing matrix) happens to be. A line that
omitted it would silently re-decide the most expensive constant on it.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-727-fail-closed` already exists, so re-running the line is a no-op
rather than a collision.

**`sonnet` here is an OPERATOR RULING, not a lane default, and is not the lane's to re-decide**
(operator, 2026-09-12: "x2-727-fail-closed at `-Model sonnet`"). The Ch8 routing matrix makes
`opus` the default for any arc touching `.dev-knowledge`; this lane is deliberately routed below
that default because its footprint is one module's exception handling plus its trip-tests —
"single-file mechanics carrying no system context", which is the matrix's own `sonnet` row. The
divergence is recorded here so the lane does not escalate it as a fork class, and so a reader
does not mistake it for `[#717]`'s defect (a contract whose model was silently re-decided at
dispatch). The value on the line and the value in the table agree, which is exactly what
`[#717]` closed.

## Worktree pairing

slug `lane-x-727-fail-closed` -> branch `worktree-lane-x-727-fail-closed` -> contract `LANE-x-727-fail-closed.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. **FIRST COMMIT, before any code: `[#727]`'s Done-when is AMENDED to carry the fail-posture
   clause it has never carried.** The amendment text is frozen by the operator (2026-09-12) and
   is transcribed, not paraphrased: *the deny-and-point hook refuses its matched class when it
   cannot evaluate (script missing, interpreter missing, crash, unexpected rc), each refusal
   naming cause and fix, with a RED-first trip-test per failure mode.* **`[#727]` does not close
   until that clause is green.** This rides this lane's first commit — it is NOT a separate lane
   (operator ruling, same message).
2. **`scripts/hooks/deny_and_point.py` fails CLOSED for its matched class** (`Bash`, `PowerShell`,
   `Grep`). The three allow-on-failure paths ARE the target, and they are named here so the lane
   does not have to find them: **L645** (`except Exception`, commented *"allow on ANY failure;
   over-blocking is the costly error"*), **L651** (`except Exception`), and **L660**
   (`except Exception`, commented *"cannot parse -> cannot identify a governed search -> allow"*).
   Line numbers are as of `9136f133` and are a starting point, not an assertion — resolve each
   before editing it.
3. **A RED-first trip-test PER FAILURE MODE**, four at minimum: script missing, interpreter
   missing, crash mid-evaluation, unexpected return code. Each asserts BOTH that the matched call
   is refused AND that the refusal text names **cause and fix**. Each test is proven RED before
   the fix makes it green (ADR-108 §B), and stays RED if the posture is later weakened back to
   permit-on-failure.
4. **The declared `# raw-needed: <reason>` escape STAYS**, and a test proves it still works after
   the flip. A fail-closed guard with no escape wedges the session — that is `[#727]`'s own
   over-match warning, and it is not traded away for fail-closed.
5. **Ordinary non-governed searching is still unaffected**, proven by the existing over-match
   guard test staying green. Fail-CLOSED applies to the **matched class only**; it is not a
   licence to widen what the hook matches.
6. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Why this lane exists — the row would otherwise have closed GREEN against a fail-OPEN organ

`[#727]`'s Done-when as it stands names four things: deny on `Bash`/`Grep`; the pointer naming
the organ; a RED-first trip-test; `floor: MUST`. **All four are already discharged by `11c7c8b1`.**
**Fail-posture appears nowhere in it.** So without clause 1 above, `[#727]` closes green while
the organ it certifies permits every call it cannot evaluate. That is the same defect class the
row itself was filed against — a detector that returns a confident answer over the half of the
input it cannot see.

This is why AX24-5 holds `[#727]` out of the closure set until this lane lands, and why the
Done-when amendment is clause 1 rather than a follow-up.

## Carried rows and clauses (verbatim — AX12-1)

### `AX24-2` — verbatim

> **AX24-2 · `deny_and_point.py` is wired fail-OPEN; it fails CLOSED for its matched class**
> (`Bash|PowerShell|Grep`), exactly as W-2′ ruled for the prompts guard (AX15-1): when the hook
> cannot evaluate — script missing, interpreter missing, crash, unexpected rc — the matched call
> is refused with cause and fix. A permit-on-failure organ is declared enforcement without
> enforcement, and this one was built yesterday. Not a new lane: a clause on `[#727]`, landed
> with a RED-first trip-test per failure mode before `[#727]` closes. The declared
> `# raw-needed: <reason>` escape stays.

### `AX24-5` — verbatim (the clause that gates this row's closure)

> **AX24-5 · Closure set for the operator's word:** `[#684]` `[#716]` `[#717]` `[#718]` `[#692]`
> `[#727]` — each with its proving SHA and named test; `[#727]` closes only after AX24-2 lands.
> `[#689]` `[#664]` `[#735]` `[#736]` explicitly NOT closed.

### Row `[#727]` — current Done-when, verbatim (what clause 1 amends)

> Done when: a `PreToolUse` hook on `Bash` and `Grep` DENIES a raw search (`grep`, `rg`, `find`,
> `Select-String`) over the governed questions AX9-1 enumerates, with exception text naming the
> organ to run instead; a RED-first trip-test sends a raw grep and asserts BOTH the denial and
> the pointer; ordinary non-governed searching is unaffected, proven by a test that a plain
> string search still runs; and the component is declared **floor: MUST**

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

**Not escalation classes here, decided in advance:** the `sonnet` routing (operator ruling,
above); the exact wording of the amended Done-when (frozen in clause 1); and which of the three
`except` sites to change (all of them — clause 2).

## Steps

1. Amend `[#727]`'s Done-when per clause 1, exactly as frozen. **COMMIT** (this is the lane's
   first commit; the row edit precedes the code it governs).
2. Write the four RED-first trip-tests per clause 3 and prove each RED against the current
   fail-open module. **COMMIT** the failing tests before any fix.
3. Flip the three allow-on-failure paths to refuse-with-cause-and-fix for the matched class;
   the four tests go green; the `raw-needed` escape test and the over-match guard test stay
   green. **COMMIT**
4. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items),
   **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
- **Do not widen what the hook matches.** Fail-CLOSED is a posture change on the *existing*
  matched class, not an expansion of it.
- **Do not close `[#727]`.** Closure is the operator's word under AX24-5; this lane makes it
  closable and says so in its end packet.
