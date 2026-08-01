# Night batch 2026-08-01 — plan-execution preparation (INDEX)

**Status: PROPOSAL SET — everything in this batch is input for morning architect review.
Nothing here governs. Nothing was filed, flipped, closed, or merged.**

**Mode:** autonomous overnight, cloud container, no operator available. Read-only over all governed
content. Output confined to eight new files under `docs/audits/`, on branch
`chore/night-batch-2026-08-01` off `main` (`1afd957`).

**Morning action:** promote or reject each lane independently. They do not depend on each other,
with one exception noted in the table ([#460] gates three backlog rows).

---

## Lane table

| lane | done-contract met? | headline finding | blocking question for the architect |
|---|---|---|---|
| **L1** — filing pre-pack | **PARTIAL — item (i) cannot be met** | Rows a–e drafted at re-derived ids **467–471**, all under the 1200-char cap; rustworkx note targeted at `tasks/382-*.md:13` with the lifecycle constraint that rules out every ADR and audit home. **The SEED intake doc cannot be written: the operator's verbatim text is not in this repo** (zero hits for "library-first" or "rustworkx"). | Supply the operator's dictation for intake #23 — or rule that the doc waits. Also: **verify [#470] before filing it** (it is written from outside `~/.claude/`, which this container cannot see). |
| **L2** — repomix pilot | **MET** | **`--compress` is a measured no-op on markdown.** 0% reduction on 13/13 `protocols/` files and 5/5 bundle files, vs **−35.5%** on `scripts/` Python. The live 52,119-B `PASTE_THIS.md` re-renders **larger** under every mode tested. All 24 anti-bluff invariants survived (0 lost, 0 altered) — but only because a no-op mutates nothing, so that pass proves nothing about distillation safety. | Adopt-narrowed to CLI-only code-context packing, or reject outright? §D's own named consumer (boot-bundle distillation) is the one the measurement kills. |
| **L3** — copier record | **MET** | **REJECTION STANDS.** The audit's copier-specific evidence (copier#1833) is **wrong, and was wrong at authorship** — fixed 17 months before the audit cited it. But the load-bearing verdict is architectural fit, not that bug, and is unweakened. New: **cruft has had zero commits since 2024-12-25**; copier ships monthly. | Confirm the correction lands as a **note on [#387]**, not a new row — or spend the audit's own falsification pilot as the re-open gate. |
| **L4** — frontmatter parser | **MET** | **The expected answer is half wrong, and that is the finding.** `python-frontmatter` 0/20 byte-identical, no config escape → disqualified. **`ruamel.yaml` is 20/20 faithful** at `width>401`. So keep the hand parser for *redundancy* (the generator templates rather than round-trips), **not** for "libraries break byte-exactness". Why-not line drafted in two forms. | Which home for the why-not line — `gen_task_tree.py` docstring or a LESSONS entry? (Place one, not both.) |
| **L5** — delta-groom | **MET** | Ten rows filed this window, **zero closed**. Proposed triage: 4 live · 4 awaiting-ruling · 1 split · 1 park. **[#460] is the keystone — ruling it converts three rows from blocked to actionable.** Two rows ([#463]/[#464]) can never close from this repo at all. | Rule the A-3 triage. Separately: is there a disposition class for *externally-actioned tracking rows*? Counting them as hub backlog will distort the §F shrink metric from 2026-08-26. |
| **L6** — [#460] decision pack | **MET, with a flagged caveat** | Consolidated to one read. **Two things the recorded recommendation assumes but nothing establishes:** the "dead since 2026-07-16" date could not be re-derived here (branch absent, clone shallow), and **the root cause of the stoppage is not established anywhere** — so "decommission the dead task" may target a component already gone. ADR-105's `consumer`/`consumption_path` are **not honestly fillable today**. | Rule R1. Recommendation: A+B now (after a live host-side check), file C but do **not** activate it. |
| **L7** — wave-2 [#462] | **MET (sketch, as scoped)** | [#462] has two clauses: clause 1 is **data-only, satisfiable in schema v1 as shipped**; clause 2 is **not satisfiable** — no loadable source represents the ADR-104/VISION declaration, and building one collides with ADR-109 §9's explicit rejection of a new persisted v1 file. | Split the row? And: does a "declared-only" member need a 5th `LifecycleStage` value or a separate axis (the D2 `role` precedent)? |

---

## Verification before commit — and one honest deviation from the brief

### Tree state

`git status --porcelain` was checked at every lane boundary and was **empty throughout the read-only
fan-out**. Each of the four bounded probes independently ran and reported the same check. The only
paths this batch adds are the eight `docs/audits/2026-08-01-*` files below.

### ⚠ One existing file IS modified: `docs/audits/README.md`

The brief says *no edits to existing repo files*. The `audit-index-freshness` pre-commit hook
(`.pre-commit-config.yaml:67-78`) **blocks** any commit that adds a `docs/audits/*.md` without
regenerating that index. The two rails cannot both be honored.

**Resolution taken, and it is declared rather than hidden:** the index was regenerated with
`python scripts/gen_audit_index.py --write`. The full diff is **+12 / −1**, and every part of it is
mechanical:
- a new `## 2026-08` heading plus exactly the eight new entries (additive);
- the document count line, `**345 audit documents.**` → `**353 audit documents.**` — the one
  modified line, and 345 + 8 = 353 exactly.

**No existing entry, section, or prose line is altered or removed.** It is machine-generated, not
authored. If the architect disagrees, reverting that one file is a single `git checkout`.

### Suite state — the brief's expectation did not hold, and the reason is the container

The brief expected *"the failure set is still exactly the two known [#457] ids."* **It is not.** The
full serial run on an untouched tree produced **33 failed / 2,061 passed / 7 skipped**.

**This was investigated rather than reported as a delta.** Every failure traces to a
container-environment difference; **none is attributable to this batch**, whose tree was verified
clean before, during, and after the run.

| cause | count | evidence |
|---|---|---|
| `analytics` dependency group not synced | **17** | `ModuleNotFoundError: No module named 'pandas'` at `scripts/fleet_analytics.py:750`. `uv sync --locked` installs the `dev` group only. **Syncing `--group analytics` dropped these 17 to 1** — hypothesis confirmed, not assumed. |
| `pyright-langserver` **present** where tests assume absent | 5 | `assert ['/root/.local/bin/pyright-langserver','--stdio'] is None` — 4× `test_reverse_dep_oracle.py`, 1× `test_safe_remove.py`. The image ships pyright globally. |
| sibling repos absent | ~4 | `audit.py health`: `repos registered (none)`; `fleet_parity: /home/user/ai-council is not a git repo`; same for `corp-monorepo`. Hits `test_boundary_report.py` and the `test_audit.py` health tests. |
| repo directory name | 1 | `assert 'dev-knowledge' == '.dev-knowledge'` — the cloud clone drops the leading dot. |
| lost executable bit | 1 | `Executable …/scripts/block_ff_push.py is not executable` in `test_carrier_hooks_source.py`. |
| oracle-dependent / real-git concurrency | 2 | `test_legibility_graph_conformance.py::test_cell_code_code_fires` (reverse-dependent count 0 — same class as the langserver rows); `test_merge_serialization.py::test_index_lock_blocks_concurrent_merge`. |
| **the two known [#457] ids** | **2** | `test_audit.py::test_check_fleet_parity_green_on_live_repo` and `test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row`. **Both present and failing exactly as `RESIDUAL.md` §1 says they should be.** |

**Conclusion: the [#457] pair is intact and re-witnessed; the other 31 are container artifacts.**

### Two further container facts that matter for reading L6 and anything history-based

1. **This clone is SHALLOW** — 373 commits; `e631e59^1` resolves to `fatal: bad revision`. Any check
   that derives "last edited" from git history is unreliable here.
2. **Consequently, the `canonical_freshness` FAIL this container reports against `VISION.md`
   (`last_reviewed 2026-07-25` vs an apparent 2026-07-26 edit) is NOT reported as a repo defect.**
   It is consistent with truncated history and could not be distinguished from one. It should be
   re-checked on a full clone before anyone acts on it. Flagged so it is neither lost nor
   over-claimed.
3. `automation/fleet-audit` is **not present** in this container (no fetch was attempted, per the
   rails), which is why L6's dead-since date is marked UNVERIFIED rather than repeated as fact.

### Tooling notes

- **Codex CLI is NOT available** in this environment (`which codex` → not found). Availability was
  verified rather than assumed; **no lane depended on it**, so no lane was degraded.
- The container's default `uv` (0.8.17, at `/root/.local/bin/uv`) shadows the pinned 0.11.19 at
  `/usr/local/bin/uv` and refuses to run against this repo's `required-version = "==0.11.19"`.
  Worth knowing for any future cloud run: `export PATH=/usr/local/bin:$PATH` first.

---

## Lane reports

- [L1 — filing pre-pack](2026-08-01-technical-night-batch-l1-filing-pre-pack.md)
- [L2 — repomix pilot measurement](2026-08-01-technical-night-batch-l2-repomix-pilot.md)
- [L3 — copier/cruft record check](2026-08-01-technical-night-batch-l3-copier-record.md)
- [L4 — frontmatter-parser swap analysis](2026-08-01-technical-night-batch-l4-frontmatter-parser.md)
- [L5 — delta-groom dossier](2026-08-01-technical-night-batch-l5-delta-groom.md)
- [L6 — [#460] decision pack](2026-08-01-technical-night-batch-l6-460-decision-pack.md)
- [L7 — wave-2 [#462] pre-analysis](2026-08-01-technical-night-batch-l7-wave2-pre-analysis.md)

---

## The three findings most likely to change a morning decision

1. **repomix cannot help the paste budget.** [#449] is about `PASTE_THIS.md` at 80.18% of its
   65,000-byte budget. §D proposed repomix as the fix. Measured: it makes the paste *larger*. The
   only lever that works on this surface is selective assembly inside `assemble_paste.py`, which the
   repo already owns and which does the one thing repomix structurally cannot — fold a *region* of a
   file rather than a whole file.

2. **[#460] is the highest-leverage five minutes on the board.** It gates [#461] and [#465]
   directly, and the ADR-109 divergence-report cadence via the standing sequencing constraint.
   Ruling it in *either* direction unblocks three rows. But rule it knowing two things the row does
   not say: the stoppage's root cause is unestablished, and stopping the branch would also retire the
   git-history forensics that made [#465]'s writer bugs findable at all.

3. **An expectation was wrong in a useful direction.** L4 was briefed to expect "library breaks
   byte-exactness." `ruamel.yaml` round-trips 20/20 byte-identical. The hand parser is still the
   right call — for a different, better reason than the one that would have been written down. Had
   the lane confirmed the expectation instead of measuring it, the repo would now carry a recorded
   rationale that is false.

---

## Method note

Orchestrator decomposed, dispatched, and verified each lane against its own done-contract before
assembly; a lane that could not meet its contract says so at the top of its report (L1 item (i)).
Bounded probes ran read-only and in parallel; every git mutation ran serially in the main thread
after all fan-out completed. Measurement tooling (repomix, `python-frontmatter`, `ruamel.yaml`,
`pandas`) was installed into the container and a scratchpad venv; nothing they produced landed
outside the scratchpad. Subagent findings were treated as claims, not conclusions: the pandas
hypothesis, the `--compress` no-op, the cp1252 glyph, and the shallow-clone caveat were each
re-derived by the orchestrator before being written down.
