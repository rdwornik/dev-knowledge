# Night-3 landed review — the seven phase-1 arcs, verified against the merged tree

- **Class:** verification (ADR-101 enum) · **Date:** 2026-08-15 · **Slug:** night3-landed-review
- **Status:** **DRAFT. This document binds nothing.** It closes no row, disposes of no WARN,
  overturns no ruling, and grants no authorization. Every "proposed" below is a proposal to the
  operator, and every verdict is a measurement offered for adjudication, not an adjudication.
- **Scope:** the 7 arcs merged in batch 5 (S, Q, R, N, M, P, O), per
  `docs/audits/2026-08-15-technical-batch-phase1-packet.md`.
- **Posture:** read-only. Nothing was deleted, renamed, closed, or pushed to `main`. The single
  write this session performs is this file plus its owed `docs/audits/README.md` regeneration.

---

## §0. The measurement caveat that governs every number below

**In this checkout the ref `main` does NOT contain batch 5.** `main` and `origin/main` both sit at
`7bbb0674`; the batch-5 queue and the two integration arcs are reachable only from this session's
branch tip `65dc3183`. The first-parent walk makes it plain:

```
65dc3183  Merge branch 'docs/night2-land-unique-holds'      <- HEAD (reviewed tree)
6a80f98…  Merge branch 'docs/phase1-integration-wrap'
60eefbb…  O   50daad0…  P   4ad2025…  M   7d1f6ce…  N
8c9163e…  R   dce393e…  Q   bce5838…  S
faad5f4…  Merge branch 'docs/phase1-batch-manifest'
d62796a…  merge boot-acts 2026-08-15                        <- the batch's declared base
7bbb0674  Merge branch 'docs/handoff-cut-2026-08-14-correction'  <- `main` HERE
```

This matters mechanically, not just bookkeeping-wise: **`audit.py` resolves several checks from the
bare ref `main`** (`scripts/audit.py:4227` → `journal_anchor.spine_entries(root, "main")`;
`scripts/audit.py:3911` → `f"{floor}..main"`). Run in this clone they report on the **pre-batch**
spine and say nothing about the seven merges. Demonstrated:

- `check_review_artifact_coverage(.)` here returns *"1 code-impact merge(s) since 2026-08-05 carry
  no linked review artifact: `387b794a` integrator/513-repin-close"* — a **pre-batch** merge. The
  packet §3 reports the batch's own four. **Both are correct**; they walked different spines.

So this review does **not** quote any `main`-walking gate output as evidence about batch 5. Where
such evidence is needed (§6), the check's logic is replicated read-only against `HEAD`. Anyone
re-running `audit.py health` in a fresh clone should fast-forward `main` first, or read its output
as describing `7bbb0674`.

**Two further environment facts, disclosed rather than left to be inferred:**

1. **No git hooks are armed in this checkout.** `.git/hooks/{pre-commit,commit-msg,pre-push}` are all
   absent — a fresh clone that never ran `pre-commit install`. The commit landing this file therefore
   **did not pass the hook mesh**; there was no gate to pass and nothing was bypassed (no
   `--no-verify`, no `SKIP=`). The two gates this file's addition would owe were run **by hand** and
   are green: `validate_hermetization.classify()` → ADMIT, and `gen_audit_index.py --check` → clean
   after regeneration. This is also a live instance of exactly what `check_hooks_armed` exists to
   catch (`scripts/audit.py:1625`).
2. **`uv run --locked` does not work here.** This environment ships `uv 0.8.17` against the repo's
   `required-version = "==0.11.19"` pin (`pyproject.toml:25`), so every `uv run` invocation refuses —
   which is the pin behaving correctly, not a defect. Tests and scripts were run on a side venv built
   outside the repo tree. **Nothing in the repo was modified to make anything run.**

---

## §1. Per-arc Done-when verification, clause by clause

Verdict key: **MET** · **PARTIAL** (what remains named) · **NOT-MET** · **N/A** (arc owns no row).

### Arc O — `[#527]` anti-direct-to-main mechanism · merge `60eefbb7`

Row: `tasks/527-anti-direct-to-main-mechanism.md:12`. Done-when has **three** clauses.

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| 1 | "a seeded direct commit attempt on `main` is refused by a pre-commit hook" | **MET** | `tests/test_block_commit_on_main.py:157` `test_e1_…` installs the script as the repo's **real** `.git/hooks/pre-commit` (`_arm`, `:106-126`), stages a file on `main`, runs `git commit`, and asserts non-zero exit, the `REFUSED` string, **and that `HEAD` did not move**. Refusal path: `scripts/block_commit_on_main.py:144-154` |
| 2 | "with a test" | **MET** | 13 tests. Acceptance matrix E1–E5 + W1 (`:157-278`), unit legs for the branch reader, the detached-HEAD hole, the per-worktree `MERGE_HEAD` carve-out, cherry-pick non-carve-out, and fail-closed exit 2 (`:280-355`) |
| 3 | "the hook is armed via the existing `arm_hooks.py`/`check_hooks_armed` mechanism" | **MET** | `.pre-commit-config.yaml:22-46` — a `local` hook at `stages: [pre-commit]`, `always_run: true`, `pass_filenames: false`. `pre-commit` is in `default_install_hook_types` (`:8`), so the SessionStart `arm_hooks.py` self-arm installs it and `audit.py::check_hooks_armed` (`scripts/audit.py:1625`) asserts the stage stays armed. **No new arming mechanism was added**, which is what the clause asks. Pinned by `test_the_hook_is_wired_and_therefore_armed` (`:361`) |

**All 13 tests pass on the reviewed tree** (§7 for the runner used). **Verdict: MET on all three
clauses.** Closure evidence sheet at §2.

### Arc P — `[#530]` single-flight dispatch guard · merge `50daad05`

Row: `tasks/530-single-flight-dispatch-guard-one-contract-execut.md:13`. **Four** clauses.

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| 1 | "the guard claims and releases a lock ref" | **MET** | `scripts/single_flight.py:219` `claim` / `:265` `release`; `tests/test_single_flight.py` T1/T5. Real-`origin` transcript P1–P9 at `docs/audits/2026-08-15-technical-530-single-flight-lane-packet.md:105-129` |
| 2 | "a second clone that never fetched the ref is refused" | **MET** | T2. The lease is evaluated by the receiving repo, so the racer needs no knowledge of the ref — `scripts/single_flight.py:14-17` |
| 3 | "a same-commit racer is refused rather than passing" | **MET** | T4, the trap the design exists for. Verdict is read from the `--porcelain` **status flag**, not the exit code (`:244-248`, `_push_status` `:186`); `=` `[up to date]` is refused despite exit 0. Live transcript line 113/116 shows the `=` arriving at exit 0, line 122 shows the refusal |
| 4 | "those T2/T4 properties are demonstrated against the real `origin`, not a local bare remote" | **MET** | Lane packet `:19` names `https://github.com/rdwornik/dev-knowledge.git`; P4–P9 are the transcript. `refs/locks/*` confirmed accepted by GitHub (`:132`) and the probe ref confirmed deleted afterwards (`:129`, `ls-remote` → 0 lines) |

**Verdict: MET on all four clauses** — which is precisely what the row already says
(*"merged `50daad05`, Done-when met, NOT closed"*). The two R2 open legs are **re-verified as real**
at their cited lines, and neither is a Done-when clause:

- **(a) ABA race in `release`** — `scripts/single_flight.py:279` `push = _git(repo, "push", remote, f":{ref}")`.
  **Confirmed real.** The remote delete is unconditional: no `--force-with-lease`, no old-value
  guard. The local leg one line above *does* guard (`update-ref -d ref held`, `:273`), so the two
  halves of one function disagree about whether a delete needs a witness. Since racers share HEAD,
  a value-based lease would not discriminate either — the row's "needs a generation-unique token"
  is the right shape.
- **(b) `rev-parse` conflation** — `scripts/single_flight.py:206-208` `_local_holder` maps **any**
  non-zero to `""`, i.e. "not held". **Confirmed real.** `--verify --quiet` exits 1 for "absent"
  and can exit non-zero for a corrupt/unreadable repo; both read as FREE.

### Arc M — `[#529]` telemetry v1 EMIT · merge `4ad2025d`

Row: `tasks/529-telemetry-v1-emit-stage-1-events-from-the-gate-m.md:13`. Done-when decomposes into
**four** clauses.

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| 1 | "the three stage-1 events emit **from live gate runs**" | **NOT-MET** | Zero call sites. `scripts/telemetry_emit.py:12-15` states this as the slice's own scope line. A repo-wide grep for `telemetry_emit` outside the module and its test returns nothing. This is phase-3 work and the row says so |
| 2 | "into a WAL-mode SQLite store **via structlog**" | **PARTIAL** | WAL store: **MET** — `WAL_PRAGMAS` (`:140-144`) applies the memo's three pragmas; `connect()` (`:278`) ensures schema. structlog: **NOT-MET** — measured live on this tree, `telemetry_emit.logger_backend()` → **`stdlib-logging`**. structlog is absent from `pyproject.toml [dependency-groups]` and `uv.lock`. The fallback is deliberate and documented (`:32-40`), but the clause names structlog |
| 3 | "with a test per event type, each constraint carries a test" | **MET** | 27 tests. Per event type: `check_run` / `hook_run` / `blocker_fired`. Per constraint: shallow-refusal `:212`, `:247`, `:262`; coverage-unknown `:273`, `:292`, `:299`, `:307`; capability-vector `:320`, `:327`, `:338`, `:346`, `:353` |
| 4 | "a recorded gate run reads back without re-measurement" | **NOT-MET** | Requires clause 1. No gate run exists to read back |

**Verdict: PARTIAL.** Remaining: call-site wiring (1), the structlog decision (2), and the read-back
record (4). Leg-status map at §3. **One correction owed to the row's leg 2** — see §4.2.

### Arc N — `[#528]` lane-latency legs 1+2 · merge `7d1f6ce0`

Row scopes this arc to **legs 1 and 2 only**; leg 3 is explicitly owed after `[#529]`.

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| 1 | "gate-run call sites use `-n auto --dist worksteal` (**or a recorded reason one does not**)" | **MET** | `.claude/skills/verify/verify.py:37` now runs `uv run --locked pytest -n auto --dist worksteal --max-worker-restart=0 -x --tb=short`, with the reason for each flag recorded at the site (`:24-36`). The five non-adopting sites each carry a recorded reason: `ship.md` L37/L32 → `[#340]`; `lane-integrate.md` L37/L59 → leg 3; `report-only-wall.yml` L141 → never a gate; carrier surfaces → own arc. Enumerated at `docs/audits/2026-08-15-technical-528-legs12-packet.md:93-110`. The clause's escape hatch is exercised honestly, not used to excuse silence |
| 2 | "the tiered-suite rule is written in PLAYBOOK/ESSENTIALS" | **MET** | `protocols/ESSENTIALS.md:86` (summary + pointer) and `protocols/PLAYBOOK.md:827` (the section). Both present on the reviewed tree |
| 3 | "`test_run` duration events land via the telemetry leg" | **NOT-MET, and out of this arc's scope** | Depends on `[#529]` phase-3 wiring |

**Verdict: MET for the arc as scoped (legs 1+2); the ROW is PARTIAL on leg 3.**

**W2 residual re-verified as still live:** `protocols/PLAYBOOK.md:843-844` and `:865-866` still
describe both night-2 audits as *"a draft on the unmerged branch"*. Both are now on the reviewed
tree (landed inside merge `7d1f6ce0` — `docs/audits/2026-08-14-technical-night2-latency.md`,
`…-night2-research.md`), so the prose is **factually false on the current tree**. This is the
packet's W2, unchanged.

### Arc Q — `[#293]` consumer runbook fan-out · merge `dce393ec`

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| 1 | "each onboarded consumer carries the seeded runbook (per-repo tracked, **n≥1 recorded**)" | **NOT-MET** | 0 of 8. The merge landed a contract and a packet and **no consumer write** — `git show --stat dce393ec` is two `docs/audits/` files plus the index. This is correct, not a shortfall: the guardrail bars a hub write into a consumer tree and R6 keeps seeding operator-gated. The row states the advance is **zero by design** |

**Verdict: NOT-MET, by ruled design.** R6's denominator correction (6 → 8) **is** applied at source:
`tasks/293-consumer-runbook-fan-out.md` carries it and the BACKLOG row renders it.

### Arc R — gate-close drain · merge `8c9163e0` · **N/A (owns no row)**

Manifest bucket: finish-line. Drains `#344 #423 #430 #415 #487 #428`, holds `#523 #514`.
**Drain ≠ closure**, and the tree agrees: all eight task files are present with `status: open`.
`git show --stat 8c9163e0` is `BACKLOG.md` (12 lines), six one-line task-body edits, `manifest.json`,
the contract, and the index — i.e. prose condensation, exactly as the packet describes. **No
Done-when clause is claimed or met by this arc, and none is claimed to be.**

### Arc S — W2-0 conversion-draft landing · merge `bce5838a` · **N/A (owns no row)**

Manifest: *"none (W2-0 conversion drafts)"*. Landed
`docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md` (360 lines) + its contract.
Verified as the **enabling condition** for the packet §4 teardown verdict on
`claude/night2-wave2-drafts-fmbwa4`: the blob is on the reviewed tree, so the branch is genuinely
superseded. **No Done-when to verify.**

---

## §2. Closure evidence sheet — `[#527]` (packet W4, "proposed closeable")

Offered for `/review-closures`. **This sheet does not close the row.**

| Field | Value |
|---|---|
| Row | `[#527]` [P2][S] Anti-direct-to-main mechanism — a commit-time local hook, not vigilance |
| Source | `tasks/527-anti-direct-to-main-mechanism.md` (`status: open`) |
| Merge | `60eefbb7` (`worktree-lane-o-527-block-main`), merge #7 of 7, R4-ruled last |
| Done-when clause 1 | **MET** — `tests/test_block_commit_on_main.py:157`, real git hook, HEAD asserted unmoved |
| Done-when clause 2 | **MET** — 13 tests, acceptance matrix E1–E5 + W1 + 7 unit legs |
| Done-when clause 3 | **MET** — `.pre-commit-config.yaml:22-46`; no new arming mechanism |
| Artifacts | `scripts/block_commit_on_main.py`, `tests/test_block_commit_on_main.py`, `.pre-commit-config.yaml` §1 entry, `CLAUDE.md` §9 roster row (landed separately at `a84f069d`) |
| Suite | 13/13 pass on the reviewed tree |
| Doc debt | **None outstanding.** The §9 roster row was the one owed item and it landed at `a84f069d`; `CLAUDE.md` v2.60 records it and states the gate's honest limit |
| Known limits (documented, not defects) | detached HEAD passes; only `MERGE_HEAD` carves out; client-side hooks are bypassable; `current_branch()` fails **open** on a git error while sibling `merge_in_progress()` **raises** — the module answers the same question two ways |
| **Blocking objection** | **None found.** |
| **Non-blocking finding raised by this review** | The config's ordering rationale (`.pre-commit-config.yaml:29-31`) claims a benefit the tool does not deliver without `fail_fast` — §7.2. This is a **config comment** defect, not a gate defect: the gate refuses correctly. It does not block closure |
| **Proposed** | **CLOSEABLE** |

---

## §3. Leg-status maps

### `[#528]` — 3 legs

| Leg | Status | Where it stands |
|---|---|---|
| 1 — gate-run call sites take `-n auto --dist worksteal` | **MET** | `.claude/skills/verify/verify.py:37` adopts; 5 sites decline with recorded reasons (packet `:93-110`) |
| 2 — tiered-suite law written in PLAYBOOK/ESSENTIALS | **MET** | `protocols/ESSENTIALS.md:86`, `protocols/PLAYBOOK.md:827` |
| 3 — `test_run` duration events land via the telemetry leg | **OPEN, blocked on `[#529]`** | No telemetry call sites exist |
| — residual W2 | **OPEN** | `protocols/PLAYBOOK.md:843-844`, `:865-866` still say "unmerged branch"; both audits are on the tree |

**Row verdict: PARTIAL — 2 of 3 legs met, leg 3 blocked, one prose residual.** Not closeable.

### `[#529]` stage-1 — 4 legs

| Leg | Status | Where it stands |
|---|---|---|
| 1 — wire the call sites (phase 3) | **OPEN** | Zero call sites, by declared scope |
| 2 — `.gitignore logs/TELEMETRY.db` | **OPEN — and the leg as written is INSUFFICIENT** | See §4.2. Measured: the literal wording leaves two files untracked |
| 3 — decide `structlog` | **OPEN** | `logger_backend()` measured → `stdlib-logging` |
| 4 — last two Done-when legs are phase-3 | **OPEN** | Clauses 1 and 4 of §1 |
| — terra P1: `default_db_path()` worktree resolution | **OPEN, confirmed real** | `scripts/telemetry_emit.py:110` sets `_REPO_ROOT = Path(__file__).resolve().parent.parent`; in a linked worktree `scripts/` resolves inside the **worktree**, so parallel lanes write *separate* stores. The cited fix pattern is live and correct: `scripts/fleet_analytics.py:1075` `_git_common_dir()` — worktrees of one repo share the git common dir |

**Row verdict: PARTIAL, stage-1 library only.** Not closeable.

---

## §4. Code-quality pass — the three new modules

### §4.1 `scripts/block_commit_on_main.py` (159 lines)

**No correctness defect found in the refusal logic.** The design is careful in the places that
matter: the branch check precedes the `MERGE_HEAD` probe (`:119-121`) so a feature branch can never
be refused by the probe's error; `MERGE_HEAD` is resolved via `git rev-parse --git-path` rather than
a literal `.git/MERGE_HEAD`, which is the only form that works in a linked worktree (`:102`); and
the broad `except Exception` fails **closed** at exit 2 (`:139-143`).

Two observations, neither blocking:

1. **The two failure sites answer the same question opposite ways — documented, and worth keeping
   documented.** `current_branch()` returns `None` on any non-zero exit (`:83-84`) → a git failure
   **allows** the commit. `merge_in_progress()` **raises** on any non-zero exit (`:103-106`) → a git
   failure **refuses**. Both are deliberate and both docstrings say so. The asymmetry is defensible
   (the first copies upstream's predicate verbatim, which is the stated point), but it means the
   module's fail-closed posture has one fail-open door. `CLAUDE.md` §9 already names this.
2. **`_git` is a member of the strict-decode class** (`:68`, `text=True` with no `errors=`) — see
   §5. Here it degrades **safely**: a decode error propagates into `main()`'s `except Exception` and
   exits 2. Worth noting only because the packet's W8 scoped that class to `test_single_flight.py`,
   and lane O's own new module is in it too.

**A property worth recording as correct-by-accident-or-design:** a `git merge --squash` on `main`
leaves no `MERGE_HEAD`, so the resulting commit is **refused**. That is the right answer — a squash
merge produces exactly the non-merge spine entry core-invariant #5 forbids — but it is not stated
anywhere and is not pinned by a test.

### §4.2 `scripts/telemetry_emit.py` (473 lines)

The refusal design is strong: the three binding constraints are enforced at the **raw-context door**
as well as through named parameters (`:380-390`), so a wiring site that hand-spells `coverage` or
`skipped` is refused rather than silently bypassing the normalizer. `safe_emit` deliberately does
**not** swallow `TelemetryError`/`ShallowRepositoryRefusal` (`:459-472`) — correct, since swallowing
either would ship a gate that silently records nothing.

**Finding T-1 — the `.gitignore` leg as written on the row is insufficient. Measured, not argued.**
WAL creates two sidecars. They are removed on a clean close, but **survive a crash**:

```
after a normal emit (clean close)   -> TELEMETRY.db
while any connection is OPEN        -> TELEMETRY.db  TELEMETRY.db-shm  TELEMETRY.db-wal
after SIGKILL mid-write             -> TELEMETRY.db  TELEMETRY.db-shm  TELEMETRY.db-wal
```

Against a real git repo, with `.gitignore` containing exactly the row's wording:

```
.gitignore = "logs/TELEMETRY.db"     -> ?? logs/TELEMETRY.db-shm
                                        ?? logs/TELEMETRY.db-wal      <- STILL untracked
.gitignore = "logs/TELEMETRY.db*"    -> (clean)
```

Leg 2 exists to stop the first live emit dirtying `git status` and tripping session-end
backpressure. The literal wording does not achieve that on any crash, and the module's whole premise
is concurrent writers (`:26-30`). **Proposed: the leg should read `logs/TELEMETRY.db*`.** One
character. Also note `logs/` is not wholesale ignored here — `.gitignore` lists each artifact
individually — so the glob is the idiom-consistent fix, not a shortcut.

**Finding T-2 — the WAL cold-start conversion can lose its race.** See §7.1; it is a test-visible
defect, so it is reported there with its measurement.

**Finding T-3 (minor) — `gitenv.py` is executed at import.** `:118-121` runs
`spec.loader.exec_module` at module import. If `scripts/gitenv.py` is absent or raises, importing
`telemetry_emit` fails with a bare `FileNotFoundError` rather than a diagnosable message. The
by-path load is well-argued (`:112-117`) and should stay; only the failure surface is bare.

### §4.3 `scripts/single_flight.py` (340 lines)

The core insight is right and hard-won: **the verdict is the `--porcelain` status flag, not the exit
code** (`:32-37`, `:244-248`). The module's own docstring records that the design sketch's
`if r.returncode == 0: return 0` would have greenlit the same-HEAD race it was written against. The
`_git` helper encodes stdin as bytes to dodge the `TextIOWrapper` CRLF rewrite that breaks
`git update-ref --stdin` on Windows (`:145-158`), and decodes with `errors="replace"` — correct.

Beyond the two known R2 legs (§1, both re-confirmed), one new observation:

**Finding S-1 — `scripts/single_flight.py:120` is itself in the W8 strict-decode class**, and the
packet's W8 note did not reach it. `_local_env_names()` runs `git rev-parse --local-env-vars` with
`text=True, encoding="utf-8"` and **no `errors=`**, three lines above a helper whose entire docstring
is about decoding carefully. The output is git's own ASCII variable names, so the practical risk is
near zero — but W8 named the *test* file's `_git` while the production module carries the same
shape. Same one-line fix.

**Finding S-2 (design, not defect) — `release` is idempotent by intent and that is what makes the
ABA race reachable.** `:267-268` documents idempotency as a safety property for re-runs after a
partial failure. It is also exactly why an unconditional remote delete looked acceptable. Recording
the tension because a generation-token fix (R2 leg (a)) will have to trade some of that idempotency
away, and that trade should be a decision rather than a surprise.

---

## §5. The W8 latent strict-decode class — full repo-wide enumeration

**Method.** AST enumeration (not grep) of every `subprocess.run/check_output/Popen/call/check_call`
that decodes to text (`text=True` / `universal_newlines=True` / `encoding=…`) and passes **no**
`errors=`. Cross-checked against the 56 sites that *do* pass `errors=`.

**Result: 181 decoding call sites repo-wide — 56 safe, 125 in the class.**

| Area | In class |
|---|---|
| `scripts/` | 36 |
| `tests/` | 85 |
| `deploy/` | 2 |
| `plugins/` | 2 |

**The 125 are not one class, and treating them as one would misprice the fix.** Split by what the
child process actually emits:

### Sub-class 1 — strict UTF-8 over a NON-git child · **6 sites** · this is the exact R2 defect

The child is Python or PowerShell writing this repo's own prose; on Windows its stdout is the console
codepage, and an em dash (cp1252 `0x97`) is not valid UTF-8. **These are the true W8 twins.**

```
scripts/validate_doc_claims.py:136                    child=python(sys.executable)  encoding='utf-8'
tests/test_block_immutable_edits.py:161               child=python(sys.executable)  encoding='utf-8'
tests/test_block_immutable_edits.py:191               child=python(sys.executable)  encoding='utf-8'
tests/test_validate_hermetization.py:244              child=python(sys.executable)  encoding='utf-8'
tests/test_surface_triage.py:75                       child=powershell              encoding='utf-8'
plugins/tier1-lifecycle/tests/test_plugin_paths.py:92 child=python                  encoding='utf-8'
```

`scripts/validate_doc_claims.py:136` is the **only production organ** among them, and it is wired
into a gate. Highest-value single fix in the class.

### Sub-class 2 — strict UTF-8 over a `git` child · **45 sites** · lowest risk

git emits UTF-8 bytes, so `encoding='utf-8'` is *correct by default*; it raises only on genuinely
non-UTF-8 repo content (a Latin-1 filename, a non-default `i18n.commitEncoding`). **The packet's
named W8 site lives here** — `tests/test_single_flight.py:50` — as does §4.3's new
`scripts/single_flight.py:120`. Production members: `scripts/audit.py:909,941,1094`,
`canonical_freshness_gate.py:79`, `check_backlog_commit_msg.py:43`, `check_backlog_filing.py:93`,
`coherence_nudge.py:77`, `gen_audit_index.py:66`, `generate_organ_index.py:241`,
`single_flight.py:120`, `validate_branch_naming.py:147,232`, `validate_hermetization.py:317`,
`worktree_import_proof.py:196`, `worktree_seed.py:195`.

### Sub-class 3 — locale decode (`text=True`, no encoding) over a `git` child · **62 sites** · silent corruption

This one is **not latent on the hub's actual host.** `text=True` decodes with the locale encoding; on
a cp1252 Windows console git's UTF-8 output does not raise — it **mojibakes silently** (and the five
undefined cp1252 bytes `81 8D 8F 90 9D` *do* raise). Measured on the reviewed tree:

```
first-parent commit subjects carrying non-ASCII, last 200:  43
sample: 781bd4f Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, …
grep -rn PYTHONUTF8 (toml|yaml|cfg|ini|py):                  0 matches
```

**43 of the last 200 spine subjects contain an em dash, and the repo pins `PYTHONUTF8` nowhere**, so
decoding behaviour is a property of whichever shell the operator happens to open. Production members
include `scripts/audit.py` ×12 (`:1651, 3042, 4652, 4671, 4768, 4792, 4801, 4809, 4817, 4828, 4841, 4850`),
`gen_handoff.py:202,220`, `validate_residual_completeness.py:133`, `boundary_headers.py:225`,
`boundary_report.py:275`, `arm_hooks.py:38`, and **`block_commit_on_main.py:68`** (§4.1).

Most of these read `git status --porcelain` paths (ASCII here). The ones that read **commit message
text** are where silent corruption actually lands; the commit-message readers in the class are
`scripts/canonical_freshness_gate.py:79`, `scripts/coherence_nudge.py:77`,
`scripts/validate_branch_naming.py:232`, and `tests/test_review_closures.py:228`.

### Proposed disposition (proposal only)

1. **Sub-class 1 (6 sites)** — apply the R2 one-liner. Reproducible failure, one already witnessed.
2. **Sub-class 3, commit-message readers (4 sites)** — set `encoding="utf-8", errors="replace"`
   explicitly. git emits UTF-8; inheriting the locale is the bug.
3. **Sub-class 2 (45) and the remaining sub-class 3 (58)** — carry as a recorded residual. Adding
   `errors="replace"` is harmless everywhere and could be a mechanical sweep, but it is 103 sites of
   churn against a low measured risk, and that is an operator call.
4. **Consider the class-level fix instead**: a shared `_git()` in one module (the repo already has
   `scripts/gitenv.py` as the leaf precedent) would make this uniform rather than per-site. Sizing
   that is out of scope here.

---

## §6. W9 — the canonical in-repo codex-review artifact shape

### §6.1 The shape is fully derivable from the check; no new convention is needed

`check_review_artifact_coverage` (`scripts/audit.py:4131`) recognises an artifact by four
mechanical properties, all pinned by regex at `scripts/audit.py:4108-4123`:

| # | Requirement | Regex / rule | Why it exists |
|---|---|---|---|
| 1 | File lives in `docs/audits/*.md` | glob at `:4200` | scan root |
| 2 | Title line `# Codex Review` | `_REVIEW_TITLE_RE` `^# Codex Review\b` | **The title is what makes a doc a review artifact.** Measured: 13 tracked non-review audits carry a `**Branch:**` field, 0 carry this title — field presence alone would let a memo satisfy coverage |
| 3 | Linkage — `**Branch:** \`<branch>\`` **or** `**HEAD:** <sha≥7>` | `_REVIEW_BRANCH_RE` / `_REVIEW_HEAD_RE` | Branch leg matches the `Merge branch '<x>'` subject; HEAD leg matches a commit the merge *introduced*. Either satisfies |
| 4 | `**Tally:** C/H/M/L` | `_REVIEW_TALLY_RE` `^\*\*Tally:\*\*[ \t]*(\d+)/(\d+)/(\d+)/(\d+)\b` | Tracked separately as `untallied`; an artifact without it still links but reads as untallied |

Filename must satisfy ADR-101 R3/R4. **`codex` is already in `AUDIT_CLASS_ENUM`**
(`scripts/validate_hermetization.py:104-115`), so `docs/audits/<YYYY-MM-DD>-codex-<slug>.md` admits.
Verified live against `validate_hermetization.classify()`.

**Proposed canonical template** — this is not a new invention; it is
`docs/audits/2026-08-14-codex-524-check-extensions.md` generalised, which is the one in-repo
precedent that already satisfies all four properties:

```
# Codex Review — <slug>

**Date:** <YYYY-MM-DD>
**Branch:** `<lane-branch-exactly-as-the-merge-subject-names-it>`
**HEAD:** `<lane tip sha>`
**Diff range:** `main..<branch>`
**Codex version:** <cli version>
**Mode:** diff-review
**Tally:** C/H/M/L <!-- Critical/High/Medium/Low -->

**Model used:** `<model>`
**Review profile:** code

---

## Focus
<what was asked>

---

## Findings
## CRITICAL
## HIGH
## MEDIUM
## LOW

---

## ADJUDICATION OF RECORD
<accept / reject per finding, with the ruling that decided it>
```

The final section is the one addition to the precedent, and it is not decorative: R3's rejection of
terra's Layer-2 claim on lane P currently lives only in the off-repo Downloads file. If the artifact
of record moves in-repo, the adjudication has to travel with it or the rejection is lost.

### §6.2 Exactly what re-landing the existing terra review would take

Measured read-only against `HEAD` (§0 — the `main`-walking check cannot see these):

```
lane  merge sha   code_impact  linked_artifact
S     bce5838a    False        NONE      <- not code-impact; owes nothing
Q     dce393ec    False        NONE      <- not code-impact; owes nothing
R     8c9163e0    False        NONE      <- not code-impact; owes nothing
N     7d1f6ce0    True         NONE      <- owed
M     4ad2025d    True         NONE      <- owed
P     50daad05    True         NONE      <- owed
O     60eefbb7    True         NONE      <- owed
```

This confirms the packet §3 attribution exactly: **4 code-impact merges, 0 linked artifacts.**

**Cost: four files, not one.** An artifact carries a single `**Branch:**` and a single `**HEAD:**`,
and each lane tip is introduced only by its own merge, so linkage is strictly 1:1. One combined file
would clear exactly one of the four.

| # | File | `**Branch:**` | `**HEAD:**` |
|---|---|---|---|
| 1 | `docs/audits/2026-08-15-codex-lane-n-528-legs12.md` | `worktree-lane-n-528-legs12-latency` | `03814f6c` |
| 2 | `docs/audits/2026-08-15-codex-lane-m-529-telemetry.md` | `worktree-lane-m-529-telemetry-emit` | `d45fdb9e` |
| 3 | `docs/audits/2026-08-15-codex-lane-p-530-single-flight.md` | `worktree-lane-p-530-single-flight` | `11b0cbdb` |
| 4 | `docs/audits/2026-08-15-codex-lane-o-527-block-main.md` | `worktree-lane-o-527-block-main` | `9732daea` |

Content source is the existing off-repo harvest `~/Downloads/PHASE1-TERRA-RAW-2026-08-15.md`, split
per lane. Each needs a `**Tally:**` line or it links but reads as untallied. Also owed with any such
addition: `python scripts/gen_audit_index.py --write` (the `audit-index-freshness` gate).

**Two things this review will not decide, because they are decisions and not hygiene:**

- **Which file is the review of record.** R3 names the Downloads file. Landing these four moves that,
  and the packet's W9 says so. Note lane P's tip in the table is `11b0cbdb` (post-R2-fixup), while
  the terra review ran at `73da833c` — so P's artifact would record a review of a *superseded* tip
  unless it is re-run or the delta is stated in the file.
- **Whether a 1:1-per-merge artifact convention is wanted at all**, given it produces four files per
  batch. The alternative — relaxing the check to accept a multi-branch artifact — is a change to
  `[#480]`'s organ, which `[#499]` owns.

---

## §7. Regressions the single full suite could not see

The packet §2 records one full-suite run: `1 failed, 2955 passed, 3 skipped, 1 xfailed`, the failure
proved pre-existing three ways. That is a sound result and this section does not dispute it. It
reports what **one** run of a suite structurally cannot observe.

**Runner note.** This environment ships `uv 0.8.17` against the repo's `required-version = "==0.11.19"`
pin (`pyproject.toml:25`), so `uv run --locked` refuses here. Tests were run on a side venv
(pytest 9.1.1) built outside the repo tree; the repo's own `addopts = "-n auto"` was honoured.
**Nothing in the repo was modified to make tests run.**

### §7.1 A load-sensitive concurrency failure in the telemetry WAL store — **1 occurrence in 29 runs**

First run of the three new suites together produced:

```
FAILED tests/test_telemetry_emit.py::test_wal_concurrency_smoke_real_processes
  assert [0, 1, 0, 0] == [0, 0, 0, 0]     (a writer process failed)
  sqlite3.OperationalError: database is locked
    telemetry_emit.py:290  conn.execute(f"PRAGMA {pragma}={value}")
```

**Reproduction, measured rather than assumed:**

| Condition | Runs | Failures |
|---|---|---|
| three suites together, `-n auto` (the original) | 1 + 8 | **1** |
| that test alone, `-n 0` (serial) | 10 | 0 |
| `test_telemetry_emit.py` alone, `-n auto` | 10 | 0 |
| 12 processes × 25 events, direct | 6 | 0 |

**A correction to my own first measurement, recorded because it nearly became a false finding.** An
initial "10/10 fail" run used `-p no:xdist`, which unloads the `-n` option that `addopts` supplies →
pytest usage error, not a test failure. `pyproject.toml:83-90` documents exactly this trap. The
honest figure is **1 failure in 29 observed runs (~3%)**.

**Root cause, isolated to the statement:**

```
holder takes BEGIN EXCLUSIVE, then a second connection runs telemetry_emit's pragmas:

  store ALREADY in WAL   PRAGMA journal_mode=WAL  -> OK in 0.00s   (no-op read, no contention)
  store NOT yet in WAL   PRAGMA journal_mode=WAL  -> OperationalError: database is locked after 5.01s
  (contrast) INSERT                               -> OperationalError: database is locked after 5.01s
```

So it is **not** steady-state WAL contention, and `busy_timeout` **is** honoured (both failures wait
the full 5.01s). It is the **cold-start conversion**: converting a store from the default journal
mode to WAL needs an exclusive lock, and on a brand-new store *every* concurrent writer races for
that same conversion simultaneously. Under enough CPU pressure the holder does not finish inside the
5s budget and the losers raise.

**Why this matters beyond a flaky test.** The window is "first concurrent emits into a not-yet-WAL
store" — which is the state of **every fresh clone, CI runner, and newly provisioned worktree**, and
the module's stated deployment premise is that pre-commit hooks, pre-push hooks and parallel agent
lanes write it at once (`scripts/telemetry_emit.py:26-30`). Phase-3 wiring would put this on a gate's
critical path. `safe_emit()` swallows `sqlite3.Error` and would absorb it — but only wiring sites
that use `safe_emit` are covered, and the event is then silently lost.

**Nothing is proposed as a fix here** beyond naming the shape: the conversion is a once-per-store
operation and could be tolerated (re-read the mode and proceed if another process already converted)
rather than treated as fatal. That is `[#529]`'s call, and it interacts with leg 1.

**This is the class the task asked about**: a single full-suite run cannot distinguish a ~3%
load-sensitive race from a pass. It passed in the batch run and it is still there.

### §7.2 Hook interaction — the ordering rationale claims something `pre-commit` does not do

`.pre-commit-config.yaml:29-31` states:

> *FIRST in the list on purpose: a commit that will not be allowed should not first pay for the
> codemap / audit / index checks below, and normalize-dated-headers should not rewrite files for it.*

**`fail_fast` is set nowhere in the file** (checked: no top-level key, none on any hook), and
pre-commit's default is `fail_fast: false` — every hook runs regardless of an earlier failure.
Ordering therefore controls output order only. Proved on a scratch repo mirroring the shape:

```
A - refuses (stands in for block-commit-on-main, FIRST) ......... Failed
B - rewrites a file (stands in for normalize-dated-headers) ..... Failed  (files were modified by this hook)
C - expensive check (stands in for codemap/audit/index) ......... Passed

note.md after the refused commit:  "REWRITTEN BY HOOK B"
EXPENSIVE_RAN marker:              PRESENT  -> hook C ran

... and with `fail_fast: true` added:
A - refuses ..................................................... Failed
note.md:  "original content"     EXPENSIVE_RAN: absent  -> claim now holds
```

**What is and is not affected.** The gate itself is fine — `block-commit-on-main` refuses the commit
correctly, and core-invariant #5 is enforced. What is false is the stated cost/side-effect benefit,
and the side effect is real: a refused direct-commit-on-main **still** gets its markdown rewritten by
`normalize-dated-headers`, leaving the working tree modified after a commit that did not happen.
With 18 pre-commit hooks in the list, it also still pays for all of them.

**Proposed (proposal only):** either add `fail_fast: true` to the `block-commit-on-main` entry — the
narrow fix, which short-circuits only when this gate refuses — or correct the comment. The comment
should not be left asserting behaviour the config does not produce.

### §7.3 Import cycles — none, and structurally none possible

All three new modules import **stdlib only**:

```
telemetry_emit      importlib.util json logging os shutil sqlite3 subprocess + typing/pathlib/datetime
single_flight       argparse os subprocess sys pathlib
block_commit_on_main subprocess sys pathlib
```

`telemetry_emit`'s one in-repo dependency (`scripts/gitenv.py`) is loaded **by path** via
`importlib.util.spec_from_file_location` (`:118-121`), not by module name — so it creates no import
edge and cannot participate in a cycle. `gitenv.py` is a documented leaf. **Zero new import edges,
zero cycle risk.** (`tach.toml` is referenced by the `codemap-freshness` hook's `files:` regex but
does not exist in the tree; harmless, the alternation simply never matches.)

### §7.4 What this section did NOT examine

- The pre-existing full-suite RED (`test_routine_consumers_…`) — the packet proves it pre-existing
  on a leg that predates the batch, and that proof was checked and is sound. Not re-litigated.
- Cross-suite ordering coupling beyond the three new files. A `-n 0` full serial sweep is the
  instrument for that (`pyproject.toml:141-146`); it was not run here.
- Any behaviour on Windows. Every measurement above is Linux. Sub-class 3 in §5 is precisely the
  class whose *worst* behaviour is Windows-only, so those 62 sites remain **unmeasured**, not clean.

---

## §8. Final verdict table

| Arc | Merge | Owning row | Done-when verdict | Remaining |
|---|---|---|---|---|
| **S** | `bce5838a` | none (W2-0 drafts) | **N/A** | — |
| **Q** | `dce393ec` | `[#293]` | **NOT-MET** (0 of 8, by ruled design) | consumer seeding, operator-gated |
| **R** | `8c9163e0` | none (drains 6, holds 2) | **N/A** | all 8 drained rows remain open |
| **N** | `7d1f6ce0` | `[#528]` legs 1+2 | **MET as scoped** · row **PARTIAL** | leg 3 (blocked on `[#529]`); W2 PLAYBOOK prose `:843-844`, `:865-866` |
| **M** | `4ad2025d` | `[#529]` | **PARTIAL** (2 of 4 clauses) | call sites; structlog; read-back; `.gitignore` glob; worktree path |
| **P** | `50daad05` | `[#530]` | **MET** (4 of 4 clauses) | 2 open legs (ABA release; `rev-parse` conflation) — not Done-when |
| **O** | `60eefbb7` | `[#527]` | **MET** (3 of 3 clauses) | none |

**Proposed closeable: 1 — `[#527]` only.**
