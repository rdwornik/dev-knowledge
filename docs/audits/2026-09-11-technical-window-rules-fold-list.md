# WINDOW RULES 2026-09-10/11 — THE FOLD LIST, AND WHAT LANDED

**Lane:** `lane-x-000-window-rules-land` · branch `worktree-lane-x-000-window-rules-land` ·
contract `LANE-x-000-window-rules-land.md` (frozen, batch X).
**Date:** 2026-09-11. **Class:** technical. **Mode:** execute, TEXT-ONLY — this lane built no
mechanism and changed no `scripts/` file.
**Source:** `to-cc/DECLARE-WINDOW-RULES-2026-09-11.md`. **Authority:** the operator's dispatch of
2026-09-11.
**Consumed by:** `protocols/STANDING_RULINGS.md` section AH, which names this file as its fold
list; rows `[#720]` and `[#721]`.

## What changed

| Commit | What |
|---|---|
| `1915f517` | `protocols/STANDING_RULINGS.md` gains section **AH** — ten operator rulings (AH-A1…AH-A10) and four standing architect rulings (AH-B1…AH-B4), one dated section, +229 lines |
| `0a4247aa` | rows `[#720]` and `[#721]` filed under `tasks/`, `tasks/manifest.json` updated, `BACKLOG.md` regenerated |
| this file | the end-of-lane artifact |

Section AH was written **fold-first**: a rule already present in the repo is cited, not restated.
Every locator below was opened and resolved against the live tree before it was written into the
section — a citation that does not resolve converts a landed rule into a dangling pointer, which
is worse than the duplication it avoids.

## The fold list — cited vs. written, with each locator

### Section A — operator rulings (functional, ADR-108 §A)

| Entry | Decision | Locator, resolved |
|---|---|---|
| AH-A1 Decision coverage | **mechanism CITED**, rule written | `[#692]` — `tasks/692-decision-coverage-a-decided-thing-is-never-unscheduled-again.md`. It IS X1-1 `decision_coverage` and carries `AMEND-SESSION-PLAN-009` A9-1..A9-3 verbatim as its Done-when |
| AH-A2 The repo protects itself from the browser | **two halves CITED**, operator judgment written | intake #92 `docs/intake/2026-09-10-tech-harness-is-process.md` §1 (harness = process management) · `[#692]` A9-1 Done-when (a deviation raises an exception that teaches) · `docs/decisions/ADR-108-decision-routing-and-engineering-standards.md` §B closing bullet (expectations the harness enforces) |
| AH-A3 Every rule is written in the repo | **WRITTEN** — deliberately not folded | `protocols/OPERATOR-INTERFACE.md:147` *"Rule 1 (inbox 029) — a browser decision exists only as a file"* binds the TRANSPORT; A3 binds the REPO. Folding A3 into Rule 1 loses the step this lane exists to take |
| AH-A4 Test-driven | **CITED in full** — all three clauses | ADR-108 §B:48 *"RED-first witnesses and failing tests before build code, frozen after freeze"* (build-arc scope, **not** upgraded to a blanket mandate) · `[#278]` + `scripts/impacted_tests.py` + `impacted-tests-guard` at `.pre-commit-config.yaml:450` · `pyproject.toml:211` `addopts = "-n auto"` |
| AH-A5 Value-oriented feedback | **WRITTEN** — no home found | searched `protocols/`, `docs/decisions/` for *gains/losses/never features/value-oriented*: zero hits. `OPERATOR-INTERFACE.md` §4 governs the medium, not the content |
| AH-A6 Every review ends with an action | **WRITTEN** — no home found | searched for *call to action / action point / ends with an action* across `protocols/`, `docs/decisions/`, `.claude/`: zero hits |
| AH-A7 No workarounds | **narrow instance CITED**, general rule written | `AGENTS.md:114`, section *Gates* — *"If a gate fires, fix the cause. Do not reach for `--no-verify`"*. The only in-repo instance, and it binds one surface |
| AH-A8 Concurrent workstreams | **gate corollary CITED**, seat rule written | `[#686]` clause (c) — P11's population over-globs `to-cc/`; the population is the window's files by manifest, not by glob. That row owns the gate; no row states the seat behaviour |
| AH-A9 Session plan | **medium CITED**, the rest written | `protocols/HANDOFF_PROCESS.md:957` *"Transport-medium contract (intake #18 A2)"* — a plan travels as a FILE, never chat-paste. `:937` `PLAN.md` D3 lifecycle is a DIFFERENT artifact and was deliberately not cited as this rule's home |
| AH-A10 Seat routing and CC context | **WRITTEN** — no home found | source `AMEND-BATCH-W-006` AW6-4. `SEAT-BOOT` renders exist under `templates/handoff/seats/`, but `grep -rn "SEAT-BOOT" protocols/ .claude/commands/` returns nothing — no protocol file says where a paste goes |

### Section B — standing architect rulings (technical, ADR-108 §A)

| Entry | Decision | Locator, resolved |
|---|---|---|
| AH-B1 Control surfaces are STATE (AW5-4) | **WRITTEN** — no repo home | live first-match reader verified at `scripts/seat_refusals.py:558`: `line = next((ln for ln in text.splitlines() if "Tally:" in ln), "")` |
| AH-B2 One GO per batch (AW5-1) | **canon CITED**, new clause written | `.claude/commands/lane-integrate.md:46`, §0 *Authorization* — *"One operator **GO** authorizes the whole batch integration"*. The added clause (a render that says otherwise is a generator defect) has no home and is written |
| AH-B3 Review independence is the reviewer model, not the invoker (AW5-2) | **WRITTEN** — no repo home | searched `AW5-2` and *"review independence"* repo-wide: zero hits |
| AH-B4 A decision's carrier must reference it (Q8) | **CITED in full** | `[#686]` clause (a) — P11 checks EXISTENCE where it means REFERENCE; *"existence of the named home is not carriage"*. The row owns both the rule and the repair |

**Tally:** 4 entries cited in full or in mechanism (AH-A1, AH-A4, AH-B2, AH-B4), 4 entries with a
half cited and a half written (AH-A2, AH-A7, AH-A8, AH-A9), 6 entries written out with no home
found (AH-A3, AH-A5, AH-A6, AH-A10, AH-B1, AH-B3).

## The `landed:` blocks, and why there are only four

`check_landing_predicate` resolves a site TRUE only when its `pattern` is found in that path's
current text, and an entry whose sites disagree is a reported propagation gap. Most rules in
section A name a mechanism that does not exist yet, so a `landed` site for them would RED the
tree. Four were declared, each verified with `re.search` against the live file **before** it was
written, and all four resolve uniformly:

```
AH-A2  docs/intake/2026-09-10-tech-harness-is-process.md            -> True
AH-A4  docs/decisions/ADR-108-...-engineering-standards.md          -> True
       .pre-commit-config.yaml                                       -> True
       pyproject.toml                                                -> True
AH-B1  scripts/seat_refusals.py                                      -> True
AH-B2  .claude/commands/lane-integrate.md                            -> True
```

**X1-3 (merge cost) was deliberately given no site.** It is named in AH-A4's prose as a pointer
because it is unbuilt, which is the exact trap the contract named.

## The two rows

| Row | Placement | What it owes |
|---|---|---|
| `[#720]` P3/S | `[E1]` Handoff continuity / `[S1]` | the browser role file gains the thin standing-rulings pointer. **Target resolved to `protocols/HANDOFF_BOOT.md`**, not `templates/handoff/v5/HANDOFF_BOOT.md.tmpl`: section C's own *"(ROLE PIN changes)"* is decisive, since the PIN is computed over the role file alone (`scripts/assemble_paste.py::_role_pin`) and the `.tmpl` is declared ANSWER-FREE and changes no PIN. The rejected reading is recorded in the row body so it is not re-litigated. **The role file was not touched** — section C puts it outside this window's write-scope |
| `[#721]` P2/S | `[E2]` Enforced governance / `[S3]` | `decision_coverage` counts `STANDING_RULINGS.md` entries as decisions. **Filed beside `[#692]` and not inside it:** `[#692]`'s Done-when carries A9-1..A9-3 **verbatim**, and A9-1's three-class decision population cannot gain a fourth class without ceasing to be verbatim. Section AH is the first live witness — six of its fourteen entries have no implementing row |

Both use the literal `Done when:` colon form, written from section C's own words. **No mechanism
was built:** `[#721]` is the clause, not the check.

## Open items, refuted premises and owed acts

1. **`audit-health` was bypassed on both commits, declared in each commit body (Q1).** The FAIL is
   `journal_spine_anchor` on `a3374b70` — *"Merge branch 'worktree-batch-w-aw53-substrate' — the
   AW5-3 substrate change"* — an **integrator merge that landed on `main` during this lane**.
   `audit.py health` was **OK in this tree before it arrived**, which is the evidence it is not
   this lane's. The discriminator was run (`introduced` non-empty, `anchored in this tree` False,
   `anchored at main` **False**) and the tree was synced to main's tip `a3374b70` before
   concluding, so it is a real gap on `main` and not tree lag. It is **not exemptible**:
   `worktree-batch-w-aw53-substrate` does not appear in batch W's manifest lane roster
   (`docs/audits/2026-09-10-technical-batch-w-manifest.md`), so the ADR-110
   declared-integration-arc rule cannot reach it — while three other lane merges ARE exempt and
   were correctly not counted. **Owed to the integrator:** a JOURNAL anchor naming a SHA that
   `a3374b70` introduced. This lane could not write one — the JOURNAL is the integrator's surface
   (`protocols/STANDING_RULINGS.md` P-1) and the frozen contract forbids an entry here.
2. **REFUTED PREMISE (Q10 disclosure) — `canonical_freshness` A2 does not bite this file.** The
   contract warned that `protocols/STANDING_RULINGS.md` carries `last_reviewed: 2026-09-08` and
   that the A2 leg would block the next commit. Measured: A2 gates **8** canonical files
   (`canonical_docs.FRESHNESS_FILES` + `audit.py::_HUB_ONLY_FRESHNESS_FILES`) and
   `STANDING_RULINGS.md` is **not** among them. It appears only in the WARN-class derived leg, and
   that WARN (`declared 2026-09-08 -> derived 2026-09-09`) **pre-dates this edit**. **No stamp was
   invented and no bypass was taken for it.** The `last_reviewed` stamp was deliberately left at
   `2026-09-08`: bumping it asserts the file was re-read end-to-end, which this lane did not do.
3. **REFUTED PREMISE (Q10 disclosure) — AW5-4 is not recorded in the batch W manifest audit.** The
   contract said AW5-4's control-surface ruling *"is also now recorded in
   `docs/audits/2026-09-10-technical-batch-w-manifest.md`; cite that where it helps"*. It is not:
   `grep -n "AW5-4\|control surface\|first-match"` over that file returns nothing, and `AW5-4`
   appears nowhere in the repo. The suggested citation was therefore **not written** — AH-B1 cites
   the live first-match reader instead, which does resolve. This changed nothing about the work:
   AW5-4 was always going to land as text.
4. **Twelve pre-existing test failures, none caused by this lane — measured, not asserted.**
   The impacted-test selector (`scripts/impacted_tests.py select --ref a3374b70`) resolves this
   docs-only diff to `-m live_repo` and zero test files, which is the sanctioned selection.
   `uv run --locked pytest -q -n 4 -m live_repo` gives **12 failed, 123 passed, 1 skipped**. The
   same command on the **same tree with this lane's changes reverted** — `git checkout a3374b70`
   over the three tracked files, both new rows moved out, the artifact moved out — gives
   **12 failed, 123 passed, 1 skipped**, the identical set. `ruff check`: all checks passed.

   The twelve, with the reason each is not this lane's:

   | Test | Class |
   |---|---|
   | `test_normalize_headers.py` ×4, `test_toc.py::test_corpus_fence_fix_never_drops_a_header_from_OUTSIDE_a_code_block` | *"corpus implausibly small (0) — glob is wrong"* — the live-corpus glob resolves empty when the run's cwd is a worktree under `.claude/worktrees/` |
   | `test_consumer_at_landing.py::test_the_live_corpus_measures_and_the_baseline_matches_it` | fails with this lane's artifact **removed** from `docs/audits/`, verified directly; the live-corpus-vs-baseline drift pre-dates it |
   | `test_proof_layer.py::test_the_live_guard_population_is_at_or_below_its_baseline` | the `test_review_artifact_coverage.py` skipif — already a `[~~] proof_layer` WARN in this tree's audit **before any edit** |
   | `test_validate_doc_rot.py::test_citation_regex_strips_only_real_dated_artifact_identifiers` | the known bare-audit-filename false-strip class |
   | `test_canonical_docs.py`, `test_export_backlog_view.py`, `test_handoff_modes.py`, `test_doc_code_edge.py` (one each) | assert against `PLAYBOOK.md`, `scripts/graph_queries.py`, `protocols/HANDOFF_BOOT.md` and the doc-code edge registry — **none of which this lane touched** |

   **"`pytest` green" in the Done-contract is therefore reported honestly as NOT met, and not met
   by this lane's doing:** the selection is green *relative to its base*, which is the only claim
   the evidence supports. Whether the five worktree-corpus failures are a real defect or an
   artifact of running a live-tree suite from inside a worktree is not this lane's question; it is
   recorded here because the next lane will hit the same wall.
5. **Owed integrator act — re-run the generator on the merged tree.** `lane-x-000-batch-x-roster-lands`
   is filing rows concurrently from a block below `719` and also regenerates `BACKLOG.md`. The
   reserved disjoint id blocks removed the id collision; the regeneration overlap resolves at
   merge. This lane's `BACKLOG.md` is correct for its own base and is **not expected to survive
   the second merge untouched** — `uv run --locked python scripts/gen_task_tree.py --emit-source`
   on the merged tree is the integrator's act, recorded here rather than pre-empted.
6. **No third id was minted.** The reserved block `720`–`721` was sufficient; nothing forked.
7. **Forks spent: 0 of 2.** Every fold-vs-write call was decided in-contract and is reported in
   the table above; no class (a)/(b)/(c) escalation arose.

## What this lane did NOT do, by contract

No JOURNAL entry · no merge, no push to `main`, no other lane's branch · no touch of
`protocols/HANDOFF_BOOT.md` or any handoff template · no `decision_coverage` build or any other
mechanism · no `scripts/` change · no edit outside the declared footprint
(`protocols/STANDING_RULINGS.md`, `tasks/`, `tasks/manifest.json`, `BACKLOG.md`, this file).
