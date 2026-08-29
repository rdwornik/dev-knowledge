# LANE lane-h-000-codex-universalise — Universalise codex/AGENTS.md into the per-CLI instruction architecture, re-pointing all 21 citing sites, with the global-config carrier deploying byte-identically before and after.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-h-000-codex-universalise LANE-h-000-codex-universalise.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-h-000-codex-universalise · lane-h-000-codex-universalise]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-h-000-codex-universalise` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-h-000-codex-universalise` -> branch `worktree-lane-h-000-codex-universalise` -> contract `LANE-h-000-codex-universalise.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

`codex/**` · `deploy/**` · `tests/**` · `AGENTS.md` · `ARCHITECTURE.md` · `.methodology.yaml` ·
`protocols/PLAYBOOK.md` (its TWO citing lines, not one)

**WIDENED deliberately, on the operator's cut**, because lane-d proved the narrow scope could not
satisfy its own done-contract: 19 of 21 citing sites live outside `codex/**`. The reference map is
`docs/audits/2026-08-29-technical-codex-fate-reference-map.md` — read it first; it is this lane's
starting evidence, not background.

**Disjointness re-verified against the tree AS IT IS NOW** (operator constraint 1), not against the
freeze-time snapshot: lanes a, b and g are merged and torn down, lane f is complete, and lane c is
HELD and undispatched with scope `CLAUDE.md` + `.claude/generated/**` — **EMPTY** overlap with the
above, so c and this lane may later run in parallel.

## Done-contract (immutable)

1. **UNIVERSALISE. Deletion is OFF THE TABLE** — operator's confirmed cut, and
   `protocols/STANDING_RULINGS.md` Z-G5 already said it: *"That directory is **not** free to
   delete"*, *"the lawful discharge is **universalisation into the per-CLI instruction
   architecture**, not deletion"*. `codex/AGENTS.md` is a LIVE CARRIER SOURCE —
   `DEFAULT_SOURCE_REL` in `deploy/carrier_globalconfig.py`, declared in six manifests, read by
   `tests/test_deploy_globalconfig.py`, and the in-repo copy that makes the ADR-115 byte-cap gate
   hermetic. Removing it breaks a live organ.
2. **The universalised home does NOT create another single-file folder** (operator constraint 2).
   Z-G5 is general — *"no single-file folders, ever"* — so a discharge that relocates one file
   into a fresh one-file directory has moved the violation, not resolved it.
3. **The carrier deploys BYTE-IDENTICALLY before and after** (operator constraint 3). Deploy-manifest
   and byte-cap-gate edits are **MECHANISM-PRESERVING MOVES**, and that is proven by RUNNING the
   carrier's own tests plus the ADR-115 byte-cap gate — **not by reading the diff**. Paste both
   results into the packet.
4. **All 21 citing sites across 7 surfaces re-point**, PLAYBOOK's two lines included. Re-derive the
   count from the tree rather than trusting the 21 — the tree has moved since the map was made.
5. **Ratchet read before AND after** via `python -c "import sys;sys.path.insert(0,'scripts');import silent_rule_detector as s;from pathlib import Path;print(s.measure(Path('.')).count)"`,
   both numbers in the packet. Baseline **443 with ZERO
   headroom**, so new `protocols/**` prose is authored token-free (no added `must` / `shall` /
   `never`) or the commit is refused.
4. Docs and code in English; hyphen-only names; logging rather than print;
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

1. Read the reference map and re-derive the citing-site set from the live tree. Where the map and
   the tree disagree, the tree wins and the disagreement is recorded. **COMMIT**
2. Design the universalised home and check it against Z-G5's general rule before building it — a
   home that is itself a single-file folder is not a discharge. **COMMIT**
3. Execute: relocate, re-point all sites, update the deploy manifests and the byte-cap gate as
   mechanism-preserving moves. **COMMIT**
4. **PROVE byte-identity by execution**: run the carrier's own tests and the ADR-115 byte-cap gate,
   paste both outputs. Ratchet before/after. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
