# LANE lane-b-2-handoff-v7 — take HANDOFF_PROCESS to v7.0.0 -- the minimal-bundle package -- before the next handoff is cut against v6.3.0

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

**No-consumer:** a frozen lane contract is consumed by its DISPATCH and by the batch manifest that enumerates its slug, never by a governance-surface citation — and its filename carries no `YYYY-MM-DD` prefix, so neither `consumer_at_landing` token regex could resolve a citation even if one existed. Declared per that check's own escape.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-b-2-handoff-v7 LANE-b-2-handoff-v7.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-b-2-handoff-v7 · lane-b-2-handoff-v7]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-b-2-handoff-v7` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-b-2-handoff-v7` -> branch `worktree-lane-b-2-handoff-v7` -> contract `LANE-b-2-handoff-v7.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

- `protocols/HANDOFF_PROCESS.md`
- `protocols/HANDOFF_BOOT.md`
- `scripts/assemble_paste.py`
- `tests/test_assemble_paste.py`
- `.claude/commands/handoff.md`
- `.claude/commands/handoff-verify.md`

## Done-contract (immutable)

1. **`HANDOFF_PROCESS.md` is at v7.0.0 with every version-bearing surface reconciled**, proven
   by re-running `reconciled_versions`, `silent_rule_ratchet` and `verify_handoff_probes` — not
   by reading the diff.
2. **An assembled paste from a REAL cut measures <=20 KB at >=70% window-specific content**, and
   the measurement is recorded. `HANDOFF_BOOT.md` stays under its 18,000 B budget: it is at
   **17,196 B today, 804 B of headroom**, and the ROLE PIN change spends from it. If v7 cannot
   fit, that is a finding to report, not a budget to quietly raise.
3. **The four stale VISION pointers in this lane's own files are re-pointed to `README.md`'s
   `## Vision`** — `HANDOFF_PROCESS.md:535` and `:960`, `HANDOFF_BOOT.md:116`,
   `.claude/commands/handoff.md:111` and `handoff-verify.md:99`. ADR-114 already made README the
   front door and `templates/handoff/v5/PROBES.md.tmpl` P1a already points there, so these are
   stale TODAY and independent of `[#621]`'s relocation.
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

1. `/preflight` `[#611]`'s Done-when and the b4 probes-pin delta before touching anything.
   **COMMIT**
2. Land v7.0.0 and reconcile every version-bearing surface. Re-point the four stale VISION
   citations in the same pass. **COMMIT**
3. Cut a REAL paste and MEASURE it — size and window-specific ratio, both recorded. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
