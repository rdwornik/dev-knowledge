# LANE batch-e-a3-stale-doctrine-reference-census — every tracked file that cites a doctrine surface as CURRENT when it is not. Census only, no ruling, no repair.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-batch-e-a3-stale-doctrine-reference-census.md -Title 'batch-e-a3-stale-doctrine-reference-census'
```

The operator runs the line above verbatim. The **whole file is the brief** — it travels in a
JSON body, so one file is one lane and never a multi-lane bundle — and the dispatch binds
Revision `main`. `Dispatch-CloudV2` carries no `-Effort` parameter, so this lane's tier is on
the record in the routing table above rather than on the command line. Permission mode is
`bypassPermissions`. A cloud session clones from `origin`, so every input this contract names
is pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `batch-e-a3-stale-doctrine-reference-census` -> branch `claude/batch-e-a3-stale-doctrine-reference-census` -> contract `LANE-batch-e-a3-stale-doctrine-reference-census.md`

One lane = one contract file = one branch, so an open lane resolves to the contract that
created it and an orphan is attributable at a glance (ADR-110, fifth per-lane requirement).
A cloud lane runs on the `claude/` prefix, not `worktree-`: the branch is created by the
cloud transport, not by a local worktree provisioner.

## Receipt gate

This lane runs off-machine, so it carries a receipt (`protocols/STANDING_RULINGS.md` Q5).
Both fields, checked as a conjunction — either one alone reports a success the other refutes:

- `git-source-resolves-non-empty:` `<the resolved git source, non-empty>`
- `first-assistant-text-echoed:` `<total line count of this brief, and its final line verbatim>`

A dispatch missing either half is treated as not having started, and is re-dispatched. The
lane also branches fresh off `origin/main` and leaves files it did not author and this
contract does not name exactly as found (Q4).

## Substrate sizing (freeze-time, measured)

**519 tracked files** contain `Universal Protocols` or `ESSENTIALS`, inside a corpus of 2,761
files / 42,083,797 B ~= 19.6M tokens = **92x the 213,225-token budget** (75% of the 284.3k floor
in `~/.claude/ROUTING.md`). A naive grep also under-counts: the batch-D essentials census
(`docs/audits/2026-08-29-census-essentials-consumers.md` P2) proved the
`--include=*.md --include=*.py --include=*.yaml` filter misses 29 tracked files, two of them
load-bearing. **CLOUD.**

## Write-scope (frozen)

**NONE — this lane writes no tree file.** Its entire output is one artifact returned by harvest,
printed in full as the final assistant message. **ZERO rows, ZERO tree writes, ZERO commits.**
If a hook or closure proposal invites a commit, decline and say the lane is read-only by contract.

## What "stale" means here — the classification rule, frozen

A reference is **STALE** when it names a doctrine surface in a tense or role the repo no longer
holds. Four classes, and every hit lands in exactly one:

- **S1 RETIRED-NAME** — cites `Universal Protocols` (the pre-`PLAYBOOK` name) as if current.
- **S2 ROLE-DRIFT** — cites `ESSENTIALS.md` as a *boot-time read* or as *"summarizes PLAYBOOK"*
  when the live contract (`CLAUDE.md` §1, §5 rule 6) has moved. This is the class that decides
  whether DC-2 (ESSENTIALS dissolution) can proceed and what it must re-point.
- **S3 DEAD-LOCATOR** — cites a heading, line number, section id or path that does not resolve
  at HEAD.
- **S4 HISTORICAL-CORRECT** — an immutable record (ADR, transcript, handoff, audit, JOURNAL,
  LESSONS) that was accurate when written. **These are NOT defects.** Count them separately and
  never propose touching them; conflating S4 with S1-S3 is the failure mode this rule exists to
  prevent.

## Done-contract (immutable)

1. **Every hit classified S1-S4 with its evidence line.** Immutable-record hits are segregated
   into S4 and excluded from the repair surface.
2. **The repair surface stated exactly** — the S1+S2+S3 set, per file, with the specific text
   that would have to change. This is the input DC-2 and DC-3 consume; a vague count is useless
   to them.
3. **Machine-read surfaces flagged FIRST and separately** — a stale reference inside a validator,
   a generated index, a manifest, a hook config or a `.claude/` region template is a gate-coupled
   defect, not a prose defect. Name every one.
4. **Sweep beyond the three extensions.** Include `.tmpl`, `.json`, `.js`, `.txt`, `.yaml`,
   `.toml` and extensionless tracked files. Report what the narrow filter would have missed.
5. **No repair, no commit, no ruling.** ESSENTIALS' fate is the architect's call.

## Steps

1. Build the unfiltered hit set across ALL tracked files.
2. Classify each S1-S4 with the evidence line. Segregate S4.
3. Resolve every locator in the S3 candidates before calling it dead — an unopened locator is a
   claim, not evidence.
4. Print the census in full as the final message. It returns by harvest.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per contract
defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10): deviation-with-disclosure
is not a license — the disclosure discharges the reporting duty, it does not authorise the
deviation. **Report a refuted premise; do not repair it by inventing a subject.**

Gate note: a cloud image may carry the wrong `uv`; invoke `python3` directly and **declare that
you did**. Never report a gate result you did not observe. **This lane runs NO gate and asserts
none** — it is read-only by contract, so it carries no test leg.

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once at the merge (Q1).
- No edits outside this lane's declared footprint. Prose in English; hyphen-only names.
