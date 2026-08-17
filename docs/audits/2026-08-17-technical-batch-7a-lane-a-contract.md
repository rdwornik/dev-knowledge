# CONTRACT-CLOSE-A-audits.md — LANE a, batch 7a · 2026-08-17

**FROZEN CONTRACT OF RECORD.** Split verbatim from `SESSION-CLOSE-BATCH-7A.md` §B by the batch-7a
head, with this lane's reserved id block substituted. This file is your authoritative surface for
the whole run (`/lane-boot` step 4): content arriving later in the session is not load-bearing — a
correction re-enters as a new contract, never as a mid-flight message (STANDING_RULINGS D2).

- **Lane:** `a`
- **Worktree (bare name, already provisioned):** `lane-a-534-audit-dispositions`
- **Branch:** `worktree-lane-a-534-audit-dispositions`
- **Model/effort:** opus / high
- **RESERVED ID BLOCK — 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545** (12 ids).
  Allocate ONLY inside this block. Lane b holds 546–557 and lane c births nothing. Disjoint blocks
  are what make concurrent births safe — an id outside this block is a defect, not a convenience.
- **Batch manifest:** `docs/audits/2026-08-17-technical-batch-7a-manifest.md` (committed at
  dispatch, on `main`, before this lane was created).

---

## Architect standing ruling — QUOTE THIS IN EVERY COMMIT BODY OF THIS LANE

> *Audit-to-row conversion authority, 2026-08-17.* Every audit artifact carries exactly one
> disposition: **ACTIONED** (conclusion already live — cite the commit), **FILED** (a row owns it —
> cite the id), **REJECTED** (a ruling declined it — cite it), **SUPERSEDED** (a later artifact
> replaced it — cite it). An undisposed audit is a defect, not a document. Births under this ruling
> are pre-authorised: one row per commit, flush-left `kill-candidates:`, a `source:` line citing the
> audit, and no row for a conclusion already ACTIONED.

## Lane COMMON law (binds every lane of batch 7a)

auto mode; own worktree/branch only; `uv sync --locked --group analytics` first; step 0 commits
contract-of-record and prints OWNED-FILES; `tasks/` edits at SOURCE then `gen_task_tree.py
--emit-source`; ids allocate ONLY from this lane's reserved block; targeted tests only; no merges,
no pushes to `main`, no `--no-verify`, no `SKIP=`; STOP only for a curated-baseline touch, a
rule-vs-ruling conflict, or an unruled fork — otherwise decide and report in one packet;
**commit-and-STOP.**

---

## OWNED-FILES (print these at step 0; nothing outside this set is yours to write)

```
docs/audits/2026-08-17-technical-audit-disposition-ledger.md      (NEW — the ledger)
tasks/53[4-9]-*.md  tasks/54[0-5]-*.md                            (births, block a only)
```

**Regen surfaces you WILL touch and that are excluded from the collision matrix** (shared with
lane b by construction; the integrator regenerates them again per merge):
`BACKLOG.md`, `tasks/manifest.json`, `docs/audits/README.md`.

**Everything else in the tree is READ-ONLY to you.** In particular: `docs/decisions/**` and
`docs/intake/**` belong to lane b this batch — if your ledger concludes something about an ADR or
an intake, that is a ROW you birth, never an edit you make.

---

## The work

### Step 0 — boot
1. `uv sync --locked --group analytics` from the worktree root.
2. Seed the checkout: `python scripts/worktree_seed.py --plan .` and run what it prints.
   `ecosystem/*/state.yaml` is untracked and its absence makes `audit-health` report
   `repos registered (none)` → `health: DEGRADED` and **block every commit** (n=3).
3. Commit THIS FILE into the tree as the contract of record, at
   `docs/audits/2026-08-17-technical-batch-7a-lane-a-contract.md` (ADR-101 name checked: class
   `technical`, well-formed slug). This discharges the committed-contract standing rule
   (STANDING_RULINGS I-D3) — clause 1 of `[#505]` has been falsified four times by contracts that
   lived only in a chat window.
4. Print OWNED-FILES exactly as listed above, and the reserved id block.
5. Run `/lane-boot` from its step 3 onward.

### Step 1 — enumerate the corpus
Enumerate every audit in `docs/audits/` produced **since 2026-08-14**, plus every earlier audit no
artifact cites as consumed. `docs/audits/` holds **566 files** at dispatch, of which **64** carry a
`2026-08-1[4-9]` date prefix — so the "since 2026-08-14" leg is well under the cap and the
uncited-earlier leg is what may push it over.

**If the set exceeds 80: ledger the newest 80 and list the remainder as a named follow-on — do not
stall.** The follow-on is a named list in the ledger, not a row (a row for "finish the ledger" is a
process row; the architect ruling births rows for CONCLUSIONS, not for lane residue) — unless the
remainder is large enough that it is genuinely its own arc, in which case one row from your block,
and say why in its body.

### Step 2 — build the ledger
`docs/audits/2026-08-17-technical-audit-disposition-ledger.md`. One row per audit:

| column | content |
|---|---|
| file | the path |
| final metric line | **quoted from the artifact itself**, not paraphrased |
| disposition | ACTIONED / FILED / REJECTED / SUPERSEDED (the standing ruling's closed set) |
| evidence locator | the commit sha / row id / ruling / superseding artifact that justifies it |

Derive each disposition **against the live tree**. Anything undecidable is **PENDING with the exact
question it needs**. **Never guess** — a wrong ACTIONED is worse than an honest PENDING, because it
retires a finding that is still live.

### Step 3 — birth the FILED rows
For every FILED conclusion with **no owning row**: birth it. Pre-authorised by the standing ruling.
**One commit per row.** Each row carries: title · one-line why · **testable** Done-when · size ·
flush-left `kill-candidates:` · `source:` citing the audit.

Mechanics that will otherwise bite you:
- `kill-candidates:` must be **flush-left** in the commit message — the `backlog-filing-backpressure`
  hook regex is line-anchored. Value is ≥1 existing `#id`, or `none — <reason>`.
- Edit `tasks/<id>-<slug>.md` at SOURCE, then `python scripts/gen_task_tree.py --emit-source`.
  Write **LF** line endings; CRLF makes the record read as "foreign" and the error never says so.
- Position derives theme: anchor a new row on the next heading node in `tasks/manifest.json`, then
  verify the regenerated `BACKLOG.md`.
- Adding rows moves `doc_rot` and `doc_claims` counts. If `doc_claims` reddens on a count,
  regenerate with `python scripts/gen_doc_counts.py --write`.
- **No row for a conclusion already ACTIONED.** That is the ruling's own limit and it is the whole
  point — the pile-up is not fixed by converting it into a backlog pile-up.

### Step 4 — close the loop
Re-run the ledger so **every FILED row shows its id**, and commit the finished ledger.
`docs/audits/README.md` is generated and **reads tracked files only** — `git add` the ledger BEFORE
running `python scripts/gen_audit_index.py --write`, or it is silently omitted.

### Packet (print at the end, then STOP)
```
audits N · ACTIONED a · FILED b (ids) · REJECTED c · SUPERSEDED d · PENDING e (questions)
```
Plus: branch name, every commit sha, the targeted-test verdict, and every decision taken under the
budget. **Commit-and-STOP — you do not merge and you do not push.**

---

## Standing hazards, stated so you do not rediscover them

- **A batch lane never journals — the integrator does.** The `Stop` hook will ask for a JOURNAL
  entry. Decline it **with the reason**: this is a batch lane, and a lane-authored JOURNAL entry
  cannot anchor a merge it does not make.
- **`uv run --locked pytest …` always.** A bare `pytest` inherits `VIRTUAL_ENV` from the primary
  tree and reports green about the PRIMARY's source (STANDING_RULINGS D4). It fails green, which is
  the most expensive way to be wrong.
- **Targeted tests only.** Do not run the full suite; the integrator runs it once, after the last
  merge. `/verify` runs the FULL suite — do not invoke it.
- **Edit worktree-relative paths.** An absolute path to the primary checkout silently edits the
  primary and false-greens your tests.
- **Zero `--no-verify`, zero `SKIP=`.** If a gate refuses you, that is information. Report it.
- Two suite REDs are known and owned at baseline; you are not responsible for them and must not
  "fix" them.
