# Morning packet — 2026-08-06 night batch

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-06
- **Source-session:** unattended night batch, Claude Code on the web (cloud sandbox); base HEAD `8e2be6a1`
- **Status:** complete — all four parts delivered; two library items NOT delivered and named
- **Model:** claude-opus-5 orchestrating; Sonnet-class read-only probe and web lanes

**Gate posture, stated plainly:** these commits are **gate-unverified by construction**. A fresh
cloud clone is ungated — `pre-commit` was never installed. `main` was never touched, nothing was
merged, nothing was force-pushed. Re-run the hooks and the suite locally before any merge.

## 1. What is on the night branch

```
branch : claude/night-batch-2026-08-06-p59kml   (pushed; tree clean)
base   : 8e2be6a1

9803270  docs(audits): night-batch adversarial review of the 2026-08-05 window
81cf13b  docs(audits): night-batch prep packs, library research, and the [#408] design

files (1777 insertions, 1 deletion):
  docs/audits/2026-08-06-technical-night-window-review.md              545  Part 1
  docs/audits/2026-08-06-technical-night-prep-packs.md                 500  Part 2
  docs/audits/2026-08-06-technical-night-library-research.md           318  Part 3
  docs/audits/2026-08-06-technical-night-408-coupling-manifest-design.md 409  Part 4
  docs/audits/README.md                                                  6  regenerated
```

Nothing else was touched. No `scripts/`, `protocols/`, `templates/`, `tasks/`, `ecosystem/` edits.
No rows born, no closes, no dispositions. The one generated-file write the contract sanctioned
(`gen_audit_index.py --write`) was run; the intake generators were not, because no intake file
was added.

## 2. Top findings, worst first

**1 — The FR-7 window violated a landed PLAYBOOK rule, and that is why v1.6 now contradicts
three live doctrine passages.** `PLAYBOOK.md:2665-2675` requires that any change to prompt
`mode` criteria update *both* PLAYBOOK and the point-of-use card, and calls divergence "a process
bug" by name. FR-7 touched only `JOURNAL.md`, `STANDING_RULINGS.md` and `prompt-template.md`.
Result — three hard contradictions now live:
- default mode: template `:14` "default lane mode is execution" vs `PLAYBOOK.md:2508`
  "plan-then-auto … is the default for most multi-step prompts";
- Scale L: template `:10`/`:18-19` vs **three** passages stating L-sized epic stories default
  plan-first (`PLAYBOOK.md:659`, `:1647-1650`, `HANDOFF_PROCESS.md:704-708`) — and v1.5's
  "plan-mode usually preferred" was *deleted*, not replaced;
- lane ceiling: template `:25-27` "~10 parallel lanes" vs `PLAYBOOK.md:1643` "**The cap: 2–3
  concurrent epic lanes.**"

Precedence between the card and PLAYBOOK for a live disagreement is **undeclared**. And the
template's backing pointer does not hold: `STANDING_RULINGS.md` carries the V-2 decision budget
verbatim but **not** V-3's ceremony tiers and **not** the lane-count ruling — those three exist
only in a commit message. One mitigating nuance on the lane cap: PLAYBOOK is scoped to ADR-97
*epic lanes*, the template to footprint-disjoint *work lanes* — plausibly different objects, but
neither text says so, so the ambiguity is itself the defect.

**2 — `audit.py health` is not shallow-clone-safe, and it fails in the FAIL direction.** Proven
here: `canonical_freshness` emitted **5 false FAILs**, `no_ff_merges` a false WARN on a genuine
2-parent merge, and `journal_spine_anchor` a FAIL-class `AnchorError`. Mechanism: graft roots
(`.git/shallow`) look like commits that create whole files — `git show --numstat 27c82d4 --
CONTRIBUTING.md` → `219 0`. **This is a hard requirement for B1** (`fetch-depth: 0`) and it is
the finding most likely to have burned the day lane. I initially read those 5 FAILs as a live
commit-blocking emergency; that was wrong and is retracted in the artifact.

**3 — A new, unfiled code defect: `CLOSES_RE` matches a non-word and misses the real one.**
`scripts/propose_closures.py:51` — `fixes?` parses as `fixe` + optional `s`. Executed against
the live object: `fixe [#5]` **matches**, `fix [#5]` **misses**. Almost certainly meant
`fix(?:es)?`. Two-file fix by construction (twin-pinned at
`tests/test_propose_closures_twin_parity.py:31`).

**4 — The A2 register defect is real and it is a *double* mislocation.** Both legs confirmed:
the PERMANENT entry is in `ecosystem/doc-code-edge.yaml:120-127`, not the disposition register
(which has **zero** `PERMANENT` hits); and the correct RESIDUAL locator is unnumbered §1 prose at
`:39-42`, not frontier item 6 — which is about `[#499]`'s cadence and is cited *correctly* for
that by B4 two sections later. The disposition row A2 names does conform. Wrong file, wrong line,
right tension. Everything else in the register verified CONFIRMED.

**5 — P3's issue-per-finding shape is refuted on measured platform limits.** `GITHUB_TOKEN` is
**1,000 requests/hour per repository** (not the 5,000 personal limit), and secondary limits cap
content creation at **80/minute and 500/hour**. A documented real case hit a 403 content-creation
block after roughly **100–150** issue creations with the primary quota barely touched. `[#487]`'s
parked set is **149**. Batch into one Issue per run; do not emit one per finding.

**6 — The suite is not green on a CI-shaped environment, for a *test* reason.**
`ARCHITECTURE.md:477-479` models two env shapes (Pyright vendored → 8/8; unprovisioned → 7/8).
A runner with `pyright-langserver` on PATH and no `node_modules/pyright` is an unmodelled third
shape and produces 7 failures — including `tests/test_reverse_dep_oracle.py:130`, which asserts
on ambient PATH contents (`# no node_modules, nothing on PATH`). B1 must vendor Pyright, declare
these expected, or the tests need an env-shape guard.

**7 — Three smaller finds.** `.claude/settings.json` pins the plugin marketplace to a hardcoded
Windows path (`C:\Users\1028120\...`), so the Tier-1 Stop hook's liveness is
environment-dependent. `CONTRIBUTING.md` has a **sixth** stale claim (`:128-156`, the deleted
Action in present tense) — B4's scope is ×6, not ×5. And `protocols/DEFINITION_OF_DONE.md` is
**not in the freshness-gated set** at all (`canonical_freshness_gate.py:32-33` + `audit.py:266`),
so its `last_reviewed: 2026-06-19` stamp is read by nothing.

## 3. GO / NO-GO board for the day lane

```
A2 register fix        READY. Both legs verified; exact replacement locators in hand:
                       ecosystem/doc-code-edge.yaml:120-127 and RESIDUAL.md:39-42.
                       One edit to STANDING_RULINGS.md:67-71. Serial job, unblocked.

B1 workflow YAML       READY, PENDING PATH WORD. Full draft YAML is in the prep packs,
                       carrying six requirements earned empirically (on: push /
                       fetch-depth: 0 / uv==0.11.19 / --group analytics / record-not-judge
                       / the Pyright decision). Needs .github/workflows/ approval only.
                       NOTE: also owes ARCHITECTURE.md Ch2+Ch6 rows in the same commit.

B4 doc-currency        READY. Scope corrected to CONTRIBUTING x6 + DoD:141-149 +
                       override.md. Eight sites, each with a live locator.

B5 block_ff_push:39    READY, code-impact -> terra review owed. Fold in ARCHITECTURE.md:327
                       (U-1, same class, currently unfiled by [#497]). Do NOT "fix"
                       :153/:169 -- those fail-soft descriptions are correct.

B2 mutation eval       BLOCKED on the missing library verdict (items 1-2 not delivered).
                       Everything else in the brief is complete, incl. the verified
                       vacuous-test calibration case.

B3 vale eval           BLOCKED on the same gap. Its decisive question is untested: can vale
                       express a CORPUS-WIDE ceiling (441 across 57 files) or only per-file?

[#487] re-scope        NOT for the first batch (L). Three premise corrections change the
                       spec -- see below.

first V-1 batch        Lane A: B1 (.github/workflows/ + ARCHITECTURE rows)   BLOCKED
                       Lane B: B4 (CONTRIBUTING, DoD, override.md)           READY
                       Lane C: B5 (block_ff_push.py, tests, ARCHITECTURE:327) READY
                       Lane D: B2 (pyproject.toml, test_fleet_analytics)      BLOCKED
                       Lane E: B3 (.pre-commit-config.yaml, .vale.ini)        BLOCKED
                       COLLISION: A and C both touch ARCHITECTURE.md -> run C first,
                       A after; never concurrently on that file.
                       B1 is the sole owner of .github/workflows/ (4 candidates converge
                       there; only report-only is authorized-shaped today).
```

**Library verdicts that change a birth's shape:**

```
[#408]  BUILD-thin, with a design change: replace the raw-SHA trigger with a normalized
        fingerprint. Fiberplane drift (MIT, active) stores an AST fingerprint, not a SHA,
        precisely because "any commit after X" false-positives on reformats. Recommend
        building v1 raw but STORING the sig field from day one, so adding the comparison
        later is not a schema migration. drift is not adoptable: 1-file-per-edge, whole-doc
        anchor -- the two dimensions [#408] needs.
P6      commit-convention engines: LEAVE. commitlint's rule API cannot see the diff (both
        rules need it); gitlint can, but last release 2023-03-10, last commit 2023-09-02,
        with an unshipped "0.20.0 Unreleased" in its own changelog. Keep the two bespoke
        Python hooks.
P6      lychee: ADOPT-candidate, and better than expected -- --include-fragments checks
        LOCAL markdown heading anchors (GitHub-style kebab-case), which is the repo's real
        rot class. Cannot do file.py:123; that stays /preflight's job.
P2      dead-man's switch: BUILD-thin, and one part is honestly unsolvable. workflow_run
        does NOT fire on absence (confirmed). The watchdog shares the scheduler's failure
        mode -- with a documented Jan-2026 case where a private repo's cron silently
        stopped and GitHub staff confirmed a rolled-back change. Also: the 60-day
        auto-disable is documented for PUBLIC repos only; private applicability is
        genuinely unresolved, and it matters for [#493].
P3      gh: ADOPT-candidate for mechanics; the issue-per-finding shape is refuted (finding 5).
```

**Rulings the red-team genuinely dented** — steelman plus my honest read; the browser re-rules:

```
R-A  DENTED ON REASONING, NOT ON VERDICT.
     The premise "mesh unchanged" is false on the repo's own text. Ch2 admits "every
     enforcement/AWARENESS organ" (:183-184); non-gate reporters are already members
     (boundary_report.py :245, fleet_analytics.py :247); and the Layer enum (:193-196) plus
     Ch6's mesh table (:720-726) contain NO server-side value -- so B1 adds a LAYER, not a
     row, which is the plainest reading of R-5's "changes the mesh model" trigger.
     Sharpest evidence: .github/ is not virgin ground. It existed and was deleted under
     [#255] "because a PR-triggered organ under a local-merge workflow was vacuous -- it
     never fired." So the live risk is a third ARMED-but-tells-you-nothing organ, not
     enforcement creep.
     My read: the CONCLUSION survives (no ADR to arm nothing -- NC-A5 already exempts the
     report-only deliverable). The REASONING does not, and fixing it changes the
     deliverable: B1 owes ARCHITECTURE rows in the same commit, and whether a new Layer
     value is ADR-shaped is a real fork R-A forecloses by assumption. Re-rule the narrow
     point only.

R-B  VERDICT SURVIVES; THE SPEC'S FIRST ASK SHOULD CHANGE.
     Three premise corrections from live code:
     (i) "frozen since_commit" is the wrong diagnosis. resolve_window() is a deliberate
         fail-safe that re-covers from the EARLIEST pending file (:348-353). The real
         defect is that ONE ancient unresolved WEAK id pins the baseline for everything,
         including STRONG detection -- so the repair is SEPARATING the STRONG and WEAK
         baselines, not "unfreezing". Unfreezing would discard unreviewed candidates.
     (ii) the confirm action is not merely unexercised -- NOTHING in the codebase writes a
         checked "- [x]" row. render() emits "- [ ]" unconditionally. The checkbox is a
         convention with no implementation; the only real confirm is BACKLOG-row removal.
     (iii) the addendum's line-anchoring premise does not apply: proposal evidence is
         already content-anchored (SHA + subject, or path + SHA + subject). The [#359]
         rot mode is real in the repo but not in this pipeline.
     My read: R-B is right that this is a broken pipeline, and the forensics strengthened
     it -- the regex bug (finding 3) bites regardless of anyone's review cadence.

R-C  SURVIVES, CONDITIONALLY -- two things belong on the record first.
     Steelman: (iv) institutionalizes the mechanism that caused the problem. The cause is a
     threshold (validate_doc_rot.py:56-58, WARN-only, confirmed three ways); (iv) leaves it
     alone and builds a sanctioned overflow channel beside it, into a directory already at
     397 files that ADR-100 keeps unbounded -- while NOTHING re-validates a pointer
     (preflight_contract.py self-describes as "wired into NO gate").
     The cheaper alternative -- exempt a delimited diagnosis region from the char count --
     is a constants change in one file and is not on the record as considered. Note the
     disposition route is NOT available: STANDING_RULINGS B1 reserves dispositions for
     genuine rule-vs-ruling conflict, so it is ceiling-change vs (iv).
     My read: the addendum's pointer-validation leg already patches (iv)'s worst flaw,
     which is the tell that the flaw is real. Make that leg load-bearing and gated, not
     advisory, and record an explicit rejection of the ceiling-change option.
```

## 4. Judgment calls made under the zero-questions budget

```
1  BRANCH. Worked on claude/night-batch-2026-08-06-p59kml, not the contract's
   night/2026-08-06-prep. Reason: "night/" is not in CLAUDE.md §4's branch-prefix enum
   (feat/ fix/ docs/ chore/ + worktree-<name> + epic/<slug> + claude/<slug>), while
   claude/<slug> is exactly the sanctioned cloud-session lane -- and it is the
   harness-designated branch. Creating night/ would have invented a lane prefix.

2  FILENAMES. Contract asked for docs/audits/2026-08-06-night-*.md. Those would be BLOCKED
   by validate-hermetization Rule B -- "night" is not in the CLOSED 11-class enum. Proven,
   not assumed: ran the validator's own check() over both forms.
     BLOCK  2026-08-06-night-window-review.md      (no CLOSED-enum <class>)
     PASS   2026-08-06-technical-night-window-review.md
   Used the -technical- form, matching the 2026-08-05-technical-night-batch-morning-report
   precedent. Slugs keep the contract's "night-" intent.

3  PART 4 DESTINATION. Contract asked for docs/intake/...  status: DRAFT. Routed to
   docs/audits/ instead. Reason: all 12 live intake docs carry an operator-assigned
   intake-id, and gen_intake_index.py:136-139 renders a missing one as a loud MISSING-ID
   schema break (zero such hits today). [#408] is a BACKLOG row, not an intake number, and
   inventing an intake id is a filing act this contract forbids. The cited night-draft
   precedent (2026-08-05-tech-currency-wave-1.md) carries intake-id: 24 -- already
   assigned. docs/intake/README.md:247-250 documents audit -> SEED as the promotion path;
   the exact promotion command is in the design doc. One operator move, no rework.

4  TOOLCHAIN. The container shipped uv 0.8.17; pyproject.toml:25 pins ==0.11.19 (ADR-106),
   and every hook entry is `uv run --locked`, so nothing could execute. `uv self update
   0.11.19` failed. Installed uv==0.11.19 from PyPI into a scratchpad venv OUTSIDE the repo
   tree and used that. Conforms to the repo's pin; changed no repo file; no leftovers in tree.

5  OPTIONAL DEPS. First suite run showed 32 failures. Installed the declared-but-optional
   analytics group (pandas) and re-ran only the failing files: that file went 22 -> 1. So 21
   of the 32 were my own setup omission, and I say so rather than reporting them as repo red.

6  GENERATED FILES. Ran gen_audit_index.py --write (sanctioned). Did NOT run
   gen_intake_index.py / gen_intake_tree.py -- correct, because no intake file was added.
   Had Part 4 gone to docs/intake/, BOTH would have been required or the commit would fail
   intake-index-freshness; that is a second reason call 3 went the way it did.

7  I OVERRULED MYSELF, ON A LANE'S EVIDENCE. Mid-batch I warned the probe lanes that the
   register's SHAs were unverifiable in a shallow clone. A lane re-derived them directly and
   overruled me: all of them are dated 2026-08-05 and all resolve. The shallow limit is real
   but narrower than I claimed -- it hits only pre-2026-08-01 SHAs (82227f08, 57ae83a6,
   3c5e476ba). The corrected position is what the artifacts carry.

8  COMMIT SHAPE. Two commits rather than one, so each artifact's rationale lives in its own
   message. No JOURNAL entry was written -- JOURNAL is the operator's spine and a night
   branch that is never self-merged should not prepend to it.
```

## 5. Coverage statement

**Delivered in full:** Part 1 (every register locator resolved; v1.6 checked against five docs
with negatives verified; all three rulings steelmanned and rebutted; live `audit.py health` and a
completed, fully-classified suite run). Part 2 (six briefs, footprints verified live, B1's YAML
written). Part 4 (design, granularity table for all 11 addressable sections, three-layer spec,
pointer-validation leg, subsume-or-peg analysis). Part 3 for items 3–7.

**Not delivered, named rather than smoothed:**

```
1  RESEARCH ITEMS 1 AND 2 ARE MISSING -- mutation testing (B2) and vale (B3). The lane did
   not return within the window. This is the batch's one real hole. Consequence: B2 and B3
   are the two BLOCKED-on-verdict lanes on the board. Both briefs are otherwise complete and
   carry "LIBRARY VERDICT: NOT DELIVERED" with the specific unanswered questions listed, so
   nothing inherits a false green. The decisive unknowns: can mutmut/cosmic-ray scope a run
   to named modules with cached re-runs (a 2228-test suite makes an unscoped run
   impractical); and can vale express a CORPUS-WIDE numeric ceiling rather than per-file
   counts.

2  [#487]'s VOLUMETRICS ARE UNVERIFIABLE HERE. logs/PROPOSALS-*.md does not exist in this
   container (ls logs/ -> TOKEN-LOG.md only; gitignored; the repo itself says the
   accumulation lives only on the operator's machine). So 149/62/3c5e476ba are neither
   confirmed nor disproved. Corroborated instead from git-tracked sources: #277
   (BACKLOG.md:68) "proposed 49 items, 0 valid"; the 2026-07-29 triage, 132 WEAK / 0
   closable; #487's own row, 139 parked / 0 verdicts. Direction and magnitude hold; exact
   figures do not.

3  PRE-2026-08-01 SHAs ARE UNRESOLVABLE (shallow clone, 203 commits, earliest 2026-08-01).
   The .github/ retirement narrative rests on ARCHITECTURE.md's own live text, not on the
   commits.

4  SECTION C OF THE REGISTER IS UNVERIFIABLE IN PRINCIPLE from this repo -- its source is
   off-repo by design and the label NC-A5 appears nowhere in-repo. Worth naming because R-A
   leans on that brake.

5  THE SUITE RAN ON A CONTAINER, NOT A PROVISIONED HOST. 32 failures, all accounted for,
   exactly 1 genuine: the [#457] leg-(ii) RED, now located and named --
   tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row,
   asserting "1 declared routine row" against a live "2 declared routine row(s)". Untouched
   per contract. The 10 environment-shape failures carry named causes; the Pyright cluster
   is a test-portability defect that will recur anywhere PATH has pyright-langserver
   without a vendored copy.

6  ONE INTER-LANE DISAGREEMENT, REPORTED NOT RESOLVED. The [#483] pointer's facts are agreed
   (no BACKLOG row, no manifest node, retired task file, ruling doc present); a lane read it
   as resolving cleanly rather than orphaned. The design consequence is unaffected because
   nothing re-validates it either way -- and two careful readers disagreeing is itself the
   argument for the pointer-validation leg.

7  OPERATIONAL FINDING ABOUT THIS BATCH'S OWN METHOD -- relevant to the V-1 model.
   Mid-flight correction messages from the orchestrator reached the probe lanes in a shape
   indistinguishable from a prompt injection. Two lanes flagged them as probable injections
   and re-derived every claim before folding anything in. That was correct behaviour and it
   caught a genuine error of mine (item 7 in section 4). But it means a multi-lane batch
   CANNOT rely on mid-flight corrections landing as trusted input -- anything load-bearing
   belongs in the lane's original contract.

8  NOT ATTEMPTED, BY CONTRACT: no fix to [#457], the A2 register line, or block_ff_push.py;
   no births, closes or dispositions; no scripts/protocols/templates/tasks/ecosystem edits;
   no new folders or top-level files; main untouched, nothing merged.
```
