# CONTRACT-CLOSE-B-currency.md — LANE b, batch 7a · 2026-08-17

**FROZEN CONTRACT OF RECORD.** Split verbatim from `SESSION-CLOSE-BATCH-7A.md` §B by the batch-7a
head, with this lane's reserved id block substituted. This file is your authoritative surface for
the whole run (`/lane-boot` step 4): content arriving later in the session is not load-bearing — a
correction re-enters as a new contract, never as a mid-flight message (STANDING_RULINGS D2).

- **Lane:** `b`
- **Worktree (bare name, already provisioned):** `lane-b-546-currency-archival`
- **Branch:** `worktree-lane-b-546-currency-archival`
- **Model/effort:** opus / medium
- **RESERVED ID BLOCK — 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557** (12 ids).
  Allocate ONLY inside this block. Lane a holds 534–545 and lane c births nothing. Disjoint blocks
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
docs/decisions/**          (86 ADRs at `docs/decisions/*.md` + `docs/decisions/archive/`)
docs/intake/**             (intakes + `docs/intake/archive/` + both indexes)
tasks/54[6-9]-*.md  tasks/55[0-7]-*.md                            (births, block b only)
```

**Regen surfaces you WILL touch and that are excluded from the collision matrix** (shared with
lane a by construction; the integrator regenerates them again per merge):
`BACKLOG.md`, `tasks/manifest.json`, `docs/audits/README.md`.

**Two more generated surfaces are yours to regenerate because only you move their inputs** —
`.claude/generated/recent-adrs.md` (gated by the `claude-rosters-freshness` pre-commit hook; regen
`python scripts/gen_claude_rosters.py --write`) and `docs/intake/README.md` + the intake residue
carrier (gated by `intake-index-freshness`; **an intake change needs TWO generators** —
`python scripts/gen_intake_index.py --write` AND `python scripts/gen_intake_tree.py --write`, and
the second is NOT hook-gated, so forgetting it FAILs the `intake_tree_coherence` audit check).

**Everything else in the tree is READ-ONLY to you.** In particular `docs/audits/**` belongs to
lanes a and c this batch.

---

## The work

### Step 0 — boot
1. `uv sync --locked --group analytics` from the worktree root.
2. Seed the checkout: `python scripts/worktree_seed.py --plan .` and run what it prints.
   `ecosystem/*/state.yaml` is untracked and its absence makes `audit-health` report
   `repos registered (none)` → `health: DEGRADED` and **block every commit** (n=3).
3. Commit THIS FILE into the tree as the contract of record, at
   `docs/audits/2026-08-17-technical-batch-7a-lane-b-contract.md` (ADR-101 name checked: class
   `technical`, well-formed slug). This discharges the committed-contract standing rule
   (STANDING_RULINGS I-D3).
4. Print OWNED-FILES exactly as listed above, and the reserved id block.
5. Run `/lane-boot` from its step 3 onward.

### Step 1 — ADR currency sweep
Classify **every** ADR (86 live at `docs/decisions/*.md`, plus `docs/decisions/archive/`) into
exactly one of:

- **CURRENT** — the tree still matches what it decided.
- **STALE** — the tree has diverged. **Quote the divergence with a locator.**
- **SUPERSEDED-BY** — name the successor ADR.
- **TERMINAL-UNARCHIVED** — its decision is spent and it still sits in the live directory.

**Execute the archival moves for TERMINAL-UNARCHIVED per the existing rule** (ADR-60 + its
2026-05-27 amendment; `archive/` is the triage zone, and **Rule 5 — append-only/immutable records
are NOT rewritten on move**: an ADR is point-in-time history, so you move the file and update only
living docs and the moved file's own cross-refs). Regen the indexes afterwards.

> **NEVER REWRITE A STALE ADR.** File **one row per stale ADR**, with the divergence in the row
> body. ADRs are immutable (CLAUDE.md §5 rule 3); the only in-place edit sanctioned anywhere is the
> ADR-94 **status-line-only** exception on ratification, and "the tree diverged" is not a
> ratification. An amendment, if one is ever right, is an APPENDED in-file marker — and that is a
> decision for the architect, not for this lane.

### Step 2 — intake sweep, same shape
Terminal-status intakes move to `docs/intake/archive/`. Then the class the operator keeps
complaining about: **every ACCEPTED intake whose content never became a row or an ADR gets a row**
— the **DECIDED-UNFILED** class. That is the standing complaint, and a row is the answer to it.

Frontmatter hazard, since you are editing `status:` values: **a quoted value breaks the status
parse.** The file still counts but vanishes from its status group in the generated index, and both
generators still report success. Write `status: archived`, never `status: "archived"`.

### Step 3 — ONE row for the audit-corpus change
File **one** row proposing the **smallest honest** audit-corpus change consistent with **ADR-100**
(*files never move*): a `status:` frontmatter field — **LIVE / CONSUMED / SUPERSEDED** — written by
lane a's disposition ledger, so the index can hide consumed artifacts.

**Row only. No implementation.** Cross-reference lane a's ledger by path
(`docs/audits/2026-08-17-technical-audit-disposition-ledger.md`); it lands in the same batch and
merges before you.

### Step 4 — BIRTH the recurring routine row
This is the mechanism that stops the pile-up recurring, and it is the most load-bearing birth in
this lane. **ADR-105 form** — the row must name a **consumer** and a **consumption_path**, because
`audit.py::check_routine_consumers` reads exactly those two fields and a routine row that names
neither is a routine nobody runs.

The routine: *at every window close, every new audit gets a disposition and every terminal
ADR/intake is archived.*

### Step 5 — packet
```
ADRs current/stale/superseded/archived · intakes archived/filed · rows born (ids)
```
Plus: branch name, every commit sha, the targeted-test verdict, and every decision taken under the
budget. **Commit-and-STOP — you do not merge and you do not push.**

---

## Standing hazards, stated so you do not rediscover them

- **A batch lane never journals — the integrator does.** The `Stop` hook will ask for a JOURNAL
  entry. Decline it **with the reason**.
- **`uv run --locked pytest …` always.** A bare `pytest` inherits `VIRTUAL_ENV` from the primary
  tree and reports green about the PRIMARY's source (STANDING_RULINGS D4). It fails green.
- **Targeted tests only.** The integrator runs the full suite once, after the last merge. Do not
  invoke `/verify` — it runs the FULL suite.
- **Edit worktree-relative paths.** An absolute path to the primary checkout silently edits the
  primary and false-greens your tests.
- **`git mv` for archival moves**, so the move stays a rename in history rather than a
  delete-plus-add.
- **`kill-candidates:` must be flush-left** in the commit message — the hook regex is line-anchored.
- **Write LF line endings** into `tasks/`; CRLF makes the record read as "foreign" and the error
  never says so.
- **`docs/handoffs/README.md` and the living docs are freshness-gated** — do not touch a
  `last_reviewed`-stamped file without a genuine end-to-end re-read. Nothing in this contract asks
  you to.
- **Zero `--no-verify`, zero `SKIP=`.** If a gate refuses you, that is information. Report it.
- Two suite REDs are known and owned at baseline; you are not responsible for them and must not
  "fix" them.
