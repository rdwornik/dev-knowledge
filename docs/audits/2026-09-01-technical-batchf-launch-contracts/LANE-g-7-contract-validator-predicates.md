# LANE lane-g-7-contract-validator-predicates — build the two ruled freeze predicates -- an amendment cannot subtract an act, and the manifest must agree with the contract

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

**No-consumer:** a frozen lane contract is consumed by its DISPATCH and by the batch manifest that enumerates its slug, never by a governance-surface citation — and its filename carries no `YYYY-MM-DD` prefix, so neither `consumer_at_landing` token regex could resolve a citation even if one existed. Declared per that check's own escape.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-g-7-contract-validator-predicates LANE-g-7-contract-validator-predicates.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-g-7-contract-validator-predicates · lane-g-7-contract-validator-predicates]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-g-7-contract-validator-predicates` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-g-7-contract-validator-predicates` -> branch `worktree-lane-g-7-contract-validator-predicates` -> contract `LANE-g-7-contract-validator-predicates.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

- `scripts/validate_substrate.py`
- `scripts/batch_manifest.py`
- `tests/test_validate_substrate.py`
- `tests/test_batch_manifest.py`

## Done-contract (immutable)

1. **`[#629]` — an amendment cannot SUBTRACT an act.** A new predicate REFUSES a contract whose
   amendment block negates, removes or forbids an act, step or write-scope entry present in its
   own body. Detection is textual and conservative: refusing on a matched negation is cheap, and
   the escape is exactly the reissue the predicate asks for. The refusal text names the REISSUE
   path, not just the defect. It joins the closed `RULE_IDS` set — a rule outside that set
   discharges nothing, which `substrate-unknown-override` already enforces.
2. **`[#630]` — the manifest and the contracts must agree at freeze.** The freeze REFUSES unless
   the set of lane slugs in the manifest's table EQUALS the set of contract slugs in the batch
   directory — set equality BOTH ways, so a manifest naming a phantom lane fails as loudly as a
   contract no manifest names. The refusal names both sides, not a count.
3. **RED-first witnesses, both.** One test dispatches the real DC-3 amendment shape and asserts
   the refusal; one freezes a batch with a renumbered slug (`lane-b-2` in the manifest vs
   `lane-b-3` dispatched — the measured batch-E defect) and asserts the refusal. Both fail before
   the code exists.
4. **Armed at FREEZE, grandfathered at the commit sweep.** Both legs take a `LEG_ARM_DATES` entry
   so they cannot retro-gate an already-executed dispatch, matching how legs 5 and 6 landed.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

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

## Steps

1. Write both RED witnesses first and watch them fail. ADR-108 §B binds this arc: the pass/fail
   criterion is frozen before the build. **COMMIT**
2. Build predicate `[#629]` into `validate_substrate.py` with its `LEG_ARM_DATES` entry.
   **COMMIT**
3. Build `[#630]`'s manifest/contract set-equality check with its own arm date. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
