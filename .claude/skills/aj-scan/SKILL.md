---
name: aj-scan
description: Run the Architekt Jutra delta scan -- lists course files and reference-repo commits newer than the last recorded scan, emits candidate rows, records the new high-water mark. Invoke on a per-wave cadence or when the operator asks for an Architekt Jutra update.
---

Runs `scripts/aj_scan.py scan`, which lists course files and reference-repository commits
newer than `ecosystem/aj-scan-state.yaml`'s recorded high-water mark, emits candidate rows
(carried-forward unfiled findings plus any genuinely new delta), and records a new high-water
mark. Full mechanism and its honest limits: the module docstring in `scripts/aj_scan.py`.

**No operator-disk path lives in this file or in the state file (ruling (a), LANE-5B2-15).**
The course directory is an argument you supply at invocation, never a literal written here.

## Running it

```powershell
uv run --locked python scripts/aj_scan.py scan `
  --course "<course folder path>" `
  --repos Architekt-Jutra/architekt-jutra-code,TheSoftwareHouse/copilot-collections,SkillPanel/maister `
  --since-state ecosystem/aj-scan-state.yaml
```

If the course folder path is not already in context (the operator's message, a prior session's
handoff), ask for it rather than guessing at a path — a wrong path scans nothing and reports it
as "no new candidates" indistinguishably from a real null result. `--repos` defaults to
whatever the last scan's state file already tracks (read `ecosystem/aj-scan-state.yaml`'s
`repos:` keys) if the operator does not name a different set.

## Reading the output

- A markdown table, one row per candidate: `id`, `already in` (the source citation), `what it
  would change`, `cost / time`, `served model` (the CLI that produced the row's description --
  `(carried)` for a row an earlier scan already derived and no lane has filed yet).
- `course delta: N file(s)` and, per repo, `commit(s) since <mark>` -- the mechanical counts
  that drove the row set.

**A candidate row is not a filed backlog row.** This skill only lists what the last scan
already found and what changed since; turning a row into a `tasks/` entry with a runnable
check is a separate, operator-triaged act (ADR-111's four-outcome funnel), same as every other
audit finding in this repo.

## `--dry-run` and `--json`

`--dry-run` prints the table without writing `ecosystem/aj-scan-state.yaml` back — use it to
preview before committing a state change mid-session. `--json` emits the same rows as machine-
readable output for a caller that wants to post-process them (e.g. `lane-rows-owed`-class
filing).

## `--help`

`uv run --locked python scripts/aj_scan.py --help` and `scan --help` document every flag; read
those rather than this file if a flag's exact default or type is in question.
