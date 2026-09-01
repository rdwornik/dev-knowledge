# LANE lane-d-4-deploy-waiver-honoring — make the deploy tool READ a consumer's declared divergence allowlist on both legs, unblocking both instantiations

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

**No-consumer:** a frozen lane contract is consumed by its DISPATCH and by the batch manifest that enumerates its slug, never by a governance-surface citation — and its filename carries no `YYYY-MM-DD` prefix, so neither `consumer_at_landing` token regex could resolve a citation even if one existed. Declared per that check's own escape.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-d-4-deploy-waiver-honoring LANE-d-4-deploy-waiver-honoring.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-d-4-deploy-waiver-honoring · lane-d-4-deploy-waiver-honoring]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `sonnet`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-d-4-deploy-waiver-honoring` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-d-4-deploy-waiver-honoring` -> branch `worktree-lane-d-4-deploy-waiver-honoring` -> contract `LANE-d-4-deploy-waiver-honoring.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

- `deploy/carrier_precommit.py`
- `deploy/tool.py`
- `tests/test_carrier_precommit.py`
- `tests/test_deploy_tool.py`

## Done-contract (immutable)

1. **A consumer-declared divergence causes BOTH legs to stand down** — the prune sweep SKIPs
   it with no REFUSE-abort, AND the add/converge leg does NOT re-append it on a
   previously-deployed consumer — with tests for both directions. That is `[#276]`'s Done-when
   verbatim and it is not narrowed here.
2. **The waiver is READ at the measured site.** `deploy/carrier_precommit.py:777`
   `_classify_prune` returns `PRESENT_MODIFIED` (REFUSE) with no waiver input today, and
   `waiver`/`methodology.yaml` appear ZERO times anywhere in `deploy/*.py`. The allowlist is
   consumed there, not duplicated into a second reader.
3. **The two live divergences are the test corpus, not hypotheticals** — ai-council's
   consumer-owned `ruff` id (fleet ruling 2026-07-12) and corp-monorepo's omitted `ruff-format`
   (CRLF/LF under `core.autocrlf=true`). Both are declared and neither is drift
   (`docs/audits/2026-09-01-technical-ruff-gate-divergence-classification.md`).
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

1. `/preflight` `[#276]`'s Done-when and ruling 3's classification before designing anything.
   The row was UN-DEFERRED 2026-09-01 on its own peg; it is on the critical path to the monorepo
   GO. **COMMIT**
2. Teach `_classify_prune` the allowlist, and the add/converge leg the same fact from the same
   reader. RED-first: the two live divergences fail before they pass. **COMMIT**
3. Prove both legs on a previously-deployed consumer shape. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
