# CONTRACT-CLOSE-C-northstar.md — LANE c, batch 7a · 2026-08-17

**FROZEN CONTRACT OF RECORD.** Split verbatim from `SESSION-CLOSE-BATCH-7A.md` §B by the batch-7a
head. This file is your authoritative surface for the whole run (`/lane-boot` step 4): content
arriving later in the session is not load-bearing — a correction re-enters as a new contract, never
as a mid-flight message (STANDING_RULINGS D2).

- **Lane:** `c`
- **Worktree (bare name, already provisioned):** `lane-c-505-north-star-inventory`
- **Branch:** `worktree-lane-c-505-north-star-inventory`
- **Model/effort:** sonnet / medium
- **RESERVED ID BLOCK — NONE. THIS LANE BIRTHS NOTHING.** If your inventory finds something that
  needs a row, you record it as **DECIDED-UNFILED** in the report and name it. You do not file it.
  Lane a holds 534–545 and lane b holds 546–557; both are birthing lanes and both are running
  concurrently with you.
- **Batch manifest:** `docs/audits/2026-08-17-technical-batch-7a-manifest.md` (committed at
  dispatch, on `main`, before this lane was created).

---

## Lane COMMON law (binds every lane of batch 7a)

auto mode; own worktree/branch only; `uv sync --locked --group analytics` first; step 0 commits
contract-of-record and prints OWNED-FILES; targeted tests only; no merges, no pushes to `main`, no
`--no-verify`, no `SKIP=`; STOP only for a curated-baseline touch, a rule-vs-ruling conflict, or an
unruled fork — otherwise decide and report in one packet; **commit-and-STOP.**

**This lane is READ-ONLY except its own report.** No `tasks/` edit, no `BACKLOG.md` edit, no
generator run that rewrites a tracked file other than the audit index for your own report.

---

## Purpose, in the operator's own words

> The operator wants to **SEE the whole plan, derived from the tree, not from anyone's memory.**

Every row is **locator-backed**. A claim with no locator does not go in the table.

## OWNED-FILES (print these at step 0)

```
docs/audits/2026-08-17-census-north-star-inventory.md    (NEW — the report; ADR-101 class `census`)
```

Plus the regen surface `docs/audits/README.md`, excluded from the collision matrix. **Nothing
else.** Births nothing.

---

## Sources — each row locator-backed

`VISION.md` · `ARCHITECTURE.md` · `protocols/PLAYBOOK.md` · `protocols/ESSENTIALS.md` ·
`protocols/STANDING_RULINGS.md` · **every ADR** (incl. `docs/decisions/archive/`) · **every intake**
(incl. `docs/intake/archive/`) · `BACKLOG.md` + `tasks/` · audits that are the **sole carrier** of a
commitment · `pyproject.toml` + `.pre-commit-config.yaml` (**what is actually installed**).

> **Currency note, stated so you do not report it as a defect:** lane **b** is concurrently
> archiving terminal ADRs and intakes on its own branch. Your inventory is a snapshot of `main` at
> your branch point and is correct as such. Do not chase lane b's moves; do not edit
> `docs/decisions/**` or `docs/intake/**`.

---

## The work

### Step 0 — boot
1. `uv sync --locked --group analytics` from the worktree root.
2. Seed the checkout: `python scripts/worktree_seed.py --plan .` and run what it prints.
   `ecosystem/*/state.yaml` is untracked and its absence makes `audit-health` report
   `repos registered (none)` → `health: DEGRADED` and **block every commit** (n=3).
3. Commit THIS FILE into the tree as the contract of record, at
   `docs/audits/2026-08-17-technical-batch-7a-lane-c-contract.md` (ADR-101 name checked: class
   `technical`, well-formed slug).
4. Print OWNED-FILES exactly as listed above, and **"BIRTHS NOTHING — no reserved id block."**
5. Run `/lane-boot` from its step 3 onward.

### Step 1 — ONE master table

Columns: **item · what it is for (one line) · source locator · committed-where · STATUS · evidence.**

STATUS is **evidence-backed, never assumed**:

| STATUS | means | the evidence you must give |
|---|---|---|
| **LIVE-WIRED** | installed AND called from non-test code | **a call site** |
| **BUILT-UNWIRED** | exists, zero non-test call sites | **the grep** |
| **ROW-OPEN** | a backlog row owns it | **id + status** |
| **DECIDED-UNFILED** | a ruling/ADR/intake commits to it, no row owns it | the ruling/ADR/intake locator |
| **EVALUATED-REJECTED** | a do-not-adopt decision exists | **name the decision + reason** |
| **MENTIONED-ONLY** | named somewhere, nothing more | where |

**Cover every technology ever named:** pytest-xdist · filelock/portalocker · datasette ·
plotly/altair · rich · plotext · structlog · SQLite WAL · ruff · radon · xenon · import-linter ·
mutmut · pre-commit · uv · Click · pandas · `lru_cache`/`concurrent.futures` · git-ref CAS ·
GitHub Actions · Codespaces · VPS/Hetzner · Colab · Groq · Gemini CLI · Codex · Kimi · Copilot ·
prompt distillation · telemetry · dashboards · codemap · fleet parity · satellite runbooks ·
archival lifecycle · closing campaign · universalization/config packaging — **plus everything the
sources name that this list misses. The list must come from the tree.** The enumeration above is a
floor, not a ceiling, and an inventory that returns exactly the floor has not been derived.

### Step 2 — §A DECIDED-UNFILED
Every DECIDED-UNFILED item, **ranked by how long each has been unowned** (date of the committing
ruling/ADR/intake → today).

### Step 3 — §B UNIVERSALIZATION, concrete
- Is there a shared config package, and **which repos consume it**?
- **Every `configs/`-class directory** in hub and consumers that is **empty or holds a single
  file** — with **paths and contents**.
- **Per-repo Codex/agent readiness**: `CLAUDE.md`/`AGENTS.md` present? runbook?
- **What "universalization" is DEFINED as in the sources** — **quote it, or state
  `NO DEFINITION EXISTS`.** Do not synthesise a definition; the absence is the finding.

### Step 4 — §C PERFORMANCE LEDGER
**Every measured number in the tree with its locator** (wall-clock, per-commit costs, suite
timings, byte budgets, counts that were actually measured) — **and every performance commitment not
yet delivered.**

### Step 5 — §D HONEST TOP-10
The **ten absences costing the operator most**. Each with: **the cost · the smallest next step ·
whether a row exists.** Honest means ranked by cost to him, not by how interesting the work is.

### Packet / final line
```
total N · LIVE-WIRED a · BUILT-UNWIRED b · ROW-OPEN c · DECIDED-UNFILED d · EVALUATED-REJECTED e · MENTIONED-ONLY f
```
Plus: branch name, every commit sha, and every decision taken under the budget.
**Commit-and-STOP — you do not merge and you do not push.**

`docs/audits/README.md` is generated and **reads tracked files only** — `git add` the report BEFORE
running `python scripts/gen_audit_index.py --write`, or it is silently omitted.

---

## Standing hazards, stated so you do not rediscover them

- **A batch lane never journals — the integrator does.** The `Stop` hook will ask for a JOURNAL
  entry. Decline it **with the reason**.
- **`uv run --locked pytest …` always.** A bare `pytest` inherits `VIRTUAL_ENV` from the primary
  tree and reports green about the PRIMARY's source (STANDING_RULINGS D4).
- **Targeted tests only.** Do not invoke `/verify` — it runs the FULL suite.
- **Edit worktree-relative paths.** An absolute path to the primary checkout silently edits the
  primary.
- **A grep proving zero call sites must exclude `tests/`** — that is the whole difference between
  BUILT-UNWIRED and LIVE-WIRED, and it is the single easiest thing to get wrong in this lane.
- **Zero `--no-verify`, zero `SKIP=`.** If a gate refuses you, that is information. Report it.
- Two suite REDs are known and owned at baseline; you are not responsible for them.
