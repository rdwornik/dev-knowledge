---
batch: batch-1-2026-08-28
seq: 2
shape: ADR-110 — ONE plan -> 5 file-disjoint lanes -> ONE integration
dispatched: 2026-08-28
status: open
closed_by: docs/audits/2026-08-28-technical-batch1-end-of-batch-packet.md
substrate: LOCAL
---

# BATCH-1 MANIFEST — 2026-08-28 · SEQ 2

**Frozen contract of record:** `BATCH1-LANE-CONTRACTS-2026-08-28.md` (this directory),
copied verbatim from the operator's prompts dir at dispatch. The contract is the
authoritative surface for every lane; this manifest is the dispatch record.

**Operator GO:** batch-1 GO, 2026-08-28. Two gated points only — GO at dispatch, the
end-of-batch packet at close.

## Substrate — Layer-1 cut, Q1-Q4, per lane

Every lane cuts **Q1 = YES** (each result depends on the pre-commit gate mesh and the
suite), which routes **NOT cloud** by the dispatch table's own first row. Z-G3 makes
**LOCAL** the default until all three W4 defects close, and the 2026-08-26 measurement
adds the container `uv` mismatch (0.8.17 against the repo pin `==0.11.19`), under which
no hub gate can execute on the cloud rung. Q2 is additionally YES for every lane (the
frozen contract lives in the operator's prompts dir). Cut stops at Q2.

**Route for all five lanes: LOCAL.** Q3/Q4 are not reached.

## Launch lines — copied from PLAYBOOK Ch8 "The dispatch table — the SOLE literal-command site"

Row 1, LOCAL background lane, copied rather than composed:

```
dispatch <FILE.md>                  prompts [y/N], then fires
dispatch <FILE.md> -DryRun          prints the resolved line, sends nothing
```

## Lane roster

| lane | worktree / branch slug | row(s) | scale | write-scope (frozen) |
|---|---|---|---|---|
| L1 | `lane-a-577-agents-md-lockstep` | [#577] + [#584] | M | `CLAUDE.md` · root `AGENTS.md` · `templates/claude-regions/*.md` |
| L2 | `lane-b-608-journal-tiling-seam` | [#608] (contract cites [#587] — see defect D2) | S | the tiling seam surfaces |
| L3 | `lane-c-491-fanout-acceptance` | none closed; cites [#491]/[#492] family | M/L | `docs/audits/2026-08-28-*` · fan-out item home |
| L4 | `lane-d-459-architecture-slim` | none closed; executes ruling W2/D5 | M | `ARCHITECTURE.md` only |
| L5 | `lane-e-613-routing-table` | [#613] | S/M | `ecosystem/routing-table.yaml` · check code home |

Branch = `worktree-<slug>`; all five validate against
`scripts/validate_branch_naming.py --lane`. Lanes commit-and-STOP and never self-merge.

## Merge order (frozen)

L2 (spine seam first) -> L1 -> L4 -> L5 -> L3. `--no-ff`, one at a time, ancestor-proven
teardown after each.

## Integrator branch

`docs/batch-1-integration` (ADR-110 gives the integrator no lane prefix; the convention is
an ordinary author-chosen `docs/` branch). >=2 commits: carried edits + packet first,
JOURNAL entry naming that commit second.

## Measured preconditions at dispatch

- `uv --version` = 0.11.19 against `pyproject.toml` `required-version = "==0.11.19"` — MATCH.
  Two uv binaries on PATH (`~/.local/bin`, WinGet); both probed at 0.11.19, shadowing not live.
- `python scripts/gen_task_tree.py --check` -> `check ok`, exit 0. Same under `uv run --locked`.
- `silent_rule_ratchet`: live **443** == baseline **443**, detector `silent-rule-v5`,
  60 files in scope. **Zero headroom.**
- `CLAUDE.md` budget via `validate_doc_rot.scan_file_budget`: **197/200, headroom 3**.

## Contract defects found at dispatch (recorded, not silently repaired)

- **D1 — L5 done-contract item 3 is false.** It asserts "Ratchet untouched (ecosystem/ +
  code are outside its scope roots — verified, not assumed)". `scripts/silent_rule_detector.py`
  `_SCOPE_RULES` carries `("ecosystem", False, (".yaml",))`, so `ecosystem/routing-table.yaml`
  is squarely **in** ratchet scope, against a baseline with zero headroom. Mitigation inside
  the lane's own footprint: author the table with no `must|shall|never` occurrence, holding
  live at 443. Reported rather than treated as authorization to move the baseline.
- **D2 — L2 cites the wrong row.** The contract names `[#587]` for the tiling seam;
  `[#587]` is the anchor-check single-pass inversion, and the tiling seam is `[#608]`
  (X5/C3, "moves zero bytes" — the contract's own words match [#608]'s body verbatim).
  `[#608]` further carries `depends-on: "#587"`, and `[#587]` is **open**. Resolved per
  CLAUDE.md M1 (resolve a locator before acting): the lane executes [#608]'s mechanism and
  the mis-citation plus the unmet dependency are reported here and in the packet.

## Ratchet pre-authorization

**L1: GRANTED** by the operator at GO, bounded to the measured §10-correction delta, with
old->new reported in the packet. Note that `validate_transition` refuses a baseline *raise*
in code regardless of authorization, so the lane's default is a **zero-delta** correction.
