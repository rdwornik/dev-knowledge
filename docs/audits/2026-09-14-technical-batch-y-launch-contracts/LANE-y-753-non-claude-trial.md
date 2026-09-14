# LANE lane-y-753-non-claude-trial — Run the supervised daytime non-Claude trial of ten bounded tasks with Grok 4.6 and Copilot Enterprise as stdout-only producers and agy on three read-only scans, CC writing each artifact only after verifying locators, every result through RED-first tests and a review by a model that did not produce it, and record the admission verdict in provider-registry.yaml

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `interactive` — an operator-attended session — integration and seat acts live here.

```
claude
Read <PROMPTS_DIR>\LANE-y-753-non-claude-trial.md and execute it exactly.
```

**Resolved at freeze, so nothing is left to the eye —** the first message is literally:

```
Read H:\My Drive\CLAUDE PROMPT DIR\LANE-y-753-non-claude-trial.md and execute it exactly.
```

**Do NOT launch this lane through the `dispatch` verb.** The verb substitutes exactly one literal,
`$env:CLAUDE_PROMPTS_DIR`, and `<PROMPTS_DIR>` is a different token that it passes through
untouched — a `-DryRun` at freeze rendered `claude Read <PROMPTS_DIR>\LANE-y-753-non-claude-trial.md`,
which as a real launch would hand the session a placeholder it cannot resolve. Use the resolved
line above.

**This lane runs in the PRIMARY checkout, which another seat may be holding.** An interactive
shape has no lane branch, and one checkout is one committing session — the integrator works from
the primary checkout for the whole batch. Before starting, confirm the integrator is not mid-merge,
and take an author-chosen `feat/` branch rather than committing on `main`.

`claude` starts the session; the second line is its **first message**, not a
shell command. `<PROMPTS_DIR>` is the prompts directory
(`$env:CLAUDE_PROMPTS_DIR`, `~\Downloads` by default) — the operator resolves it
by eye here, because a chat message is not a shell and nothing expands the
variable for him. This shape exists for the acts a background lane cannot
perform: integration needs an operator GO per merge, and a `--bg`
session can neither merge to `main` nor ask a question. Tier on the record above
(`opus` / `high`); board label `[.dev-knowledge · #753 · lane-y-753-non-claude-trial]`.

## Worktree pairing

slug `lane-y-753-non-claude-trial` -> contract `LANE-y-753-non-claude-trial.md`

**No lane branch.** An interactive session runs in the primary checkout on an
author-chosen branch, so there is no `worktree-` or `claude/` name for this
contract to declare — and declaring one would be a claim the tree never makes
true. The 1:1 property ADR-110's fifth per-lane requirement asks for still holds
on the pair that exists: one contract file, one session.

## Done-contract (immutable)

1. Ten bounded tasks run with Grok 4.6 and Copilot Enterprise as STDOUT-ONLY producers, plus `agy` on three read-only scans. CC writes every artifact itself, and only after verifying the locators the producer cited. Each result passes this lane's RED-first tests AND a review by a model that did not produce it.
2. An admission verdict -- green on first review, out of ten -- is recorded in `ecosystem/provider-registry.yaml`, per task, with failures NAMED rather than summarised; admission is >= 8/10. THIS LANE IS ATTENDED: it runs in the daytime and reports after each task. It must never be left to run unattended, which is why it is frozen at `shape: interactive` rather than dispatched `--bg`.
3. SEQUENCING, NOT OPTIONAL — this lane is SECOND on `ecosystem/provider-registry.yaml`. Step-0 `file-collision` REFUSED batch Y on that file, claimed by this lane and by `lane-y-751-cost-in-money`; the collision is substantive rather than a checker artifact, because the registry carries no machine-readable rate field at all and `[#751]` must author one. `[#751]` is the sole owner and goes first; this lane does not open the file until `[#751]`'s branch has LANDED on `main`, and it verifies that before its own first write. The two never hold the file at once.
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

1. Provision the trial: confirm each producer CLI answers on this machine, and record the exact invocation for each. REPORT TO THE OPERATOR. **COMMIT**
2. Run the ten bounded tasks ONE AT A TIME -- producer emits to stdout, CC verifies every cited locator, CC writes the artifact, RED-first tests run, a model that did not produce it reviews it. Report after EACH task; never batch them silently. **COMMIT after each**
3. Run `agy` on the three read-only scans, record the admission tally with failures named, and write the verdict into `ecosystem/provider-registry.yaml`; file or amend row `[#753]`. **COMMIT**
4. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
