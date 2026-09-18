# Lane ac-694 (insurance leg) — organ calls vs raw scans, AX9-5 (`[#685]`)

**Lane:** `lane-ac-694-insurance-census` · **Branch:** `worktree-lane-ac-694-insurance-census` ·
**Batch:** AC · **Date:** 2026-09-18 · **Scope:** read-only census, no code changes

## 1 · Question

AX9-5 (`[#685]`): count ORGAN CALLS vs RAW SCANS per session across the last two weeks of
transcripts, and list ORGANS UNCALLED IN 30 DAYS by name. Organ call = an invocation of
`FPG-1`, `decision_coverage`, `graph_queries`, the orphan census, or `gen_task_tree`. Raw scan =
`grep`/`rg`/`find`/`Select-String`/`git log`/`git grep` used where an organ would have answered.
Browser-seat activity carries no telemetry and is excluded.

## 2 · Window scanned

Session transcripts (JSONL) at `C:\Users\1028120\.claude\projects\C--Users-1028120-Documents-Dev--dev-knowledge\`:
**140 files** with mtime in the last 14 days (2026-09-04 → 2026-09-18), out of 614 total on disk.

## 3 · Raw-scan counts (measured)

| Pattern | Matches |
|---|---|
| `grep` / `rg` / `find` | 2594 |
| PowerShell `Select-String` | 927 |
| `git log` / `git grep` | 961 |
| **Total raw scans** | **4482** |

## 4 · Organ-call counts — BLOCKED, not zero

**Finding: the measurement is structurally blocked by this repo's own governance.** The repo
runs a `PreToolUse` hook (`scripts/hooks/deny_and_point.py`, matcher `Bash|PowerShell|Grep`,
timeout 10s) — confirmed live in `.claude/settings.json` (restored 2026-09-17, "2% within
bar"). It refuses raw `Bash`/`PowerShell`/`Grep` calls that look like a "governed question" —
one the graph organs already answer — and points the caller at the organ instead. Every attempt
by this census's enumeration agent to `grep` for `file_purpose_graph.py`, `decision_coverage.py`,
`gen_task_tree.py`, or `graph_queries.py` inside the transcript store was itself DENIED by this
guard, for the same reason the guard exists: searching for organ-invocation strings via raw grep
is exactly the pattern class it's built to intercept.

Consequence: **the four core organs cannot be counted by the method AX9-5 prescribes**, inside a
repo that enforces the very discipline AX9-5 is trying to measure. This is not "0 calls" — it is
"0 measurable calls," which is a different and more interesting finding: **the anti-raw-scan
guard and the count-raw-scans-vs-organ-calls audit are in direct tension**, and no one reconciled
that before filing `[#685]`.

Workaround (proxy) searches that the guard did allow:

| Proxy pattern | File-level matches (140-file window) |
|---|---|
| `graph_orphan_census` \| `orphan_census` | 60 |
| `--emit-source` \| `--render` (gen_task_tree proxy) | 322 |
| `uv run.*audit\.py` (audit-orbit proxy) | 322 |

These are **file-level, not per-call** counts (one JSONL may contain many turns) and are proxies,
not the named organs, so they cannot be added to the raw-scan total for a ratio.

## 5 · Organs uncalled in 30 days

**Cannot be verified from transcript data**, for the same reason as §4. `ecosystem/organ-index.md`
lists the canonical organ roster; this census could not confirm invocation (or absence) for
`file_purpose_graph`, `decision_coverage`, or `graph_queries` because the search itself is denied.
Absence-of-evidence claims for any other organ in the index would not be trustworthy without a
second, permitted method (e.g. asking the organs themselves to self-report, or reading hook
receipts rather than grepping for script names) — out of scope for this read-only census.

## 6 · Headline

**Raw scans (4482 matched instances) vastly outnumber organ calls the guard will let anyone
count (0) — but that ratio is an artifact of the measurement being blocked, not evidence that
organs are underused.** The real, actionable finding is structural: AX9-5 as specified cannot be
answered inside this repo without either (a) an explicit, ruled exception letting this kind of
audit search bypass `deny_and_point.py`, or (b) instrumenting the organs themselves to emit
telemetry on invocation (their own log line, a counter file, etc.) so a census doesn't have to
grep for them at all.

## 7 · Caveats

- JSONL transcripts log tool calls (`Bash`, `Grep`, `Read`, …), not the organ's internal
  execution — an organ invoked via `uv run --locked python scripts/audit.py ...` appears as one
  opaque Bash call, not as a discrete "organ fired" event.
- The 4482 raw-scan count is not sampled for false positives (e.g. a `git log` used just to read
  the last commit message, not to answer a structural question); the true "raw scan where an
  organ would have answered" count is smaller than 4482, direction and magnitude unmeasured here.
- Local pre-commit/git-hook organ firings (e.g. `graph-rebuild`, `decision-coverage` as hooks) may
  not appear in cloud-session transcripts at all; this census only saw local Claude Code sessions'
  JSONL, per the 140-file window above.
