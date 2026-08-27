# lane-h-handoff-mech — lane report

<!-- scope: meta -->

**Lane:** `worktree-lane-h-handoff-mech` · **Base:** `d8211b03` · **Substrate:** LOCAL worktree,
gates armed · **Contract:** `lane-h-handoff-mech.md` (frozen; operator prompts dir)
**Evidence read:** `docs/audits/2026-08-26-technical-handoff-census.md` — the FROZEN repo path,
landed by sibling lane-g2. Not yet on this branch's base at execution time, so it was read from
`CLOUD-HANDOFF-CENSUS-RESULT.md` in the operator's Downloads directory per the contract's own
instruction, and cited by the frozen repo path regardless.
**Rows:** census items R2–R6, born by lane-g2. Cited here by census item id; the integrator
reconciles row ids at merge.

---

## 1. What shipped

| Step | Census item | Landed | Commit |
|---|---|---|---|
| 1 | R3 — bounded probes | P10 out of the shipped manifest; a boundedness rung in `verify_handoff_probes.py`, era-gated | `b14306bc` |
| 2 | R4 — `supplement_folded` | New FAIL-class ALL_CHECKS member; the one live instance dispositioned immutable-and-lost | `b043b9e1` |
| 3 | R2 — generated Standing-vs-NEW | Three generated lists above the driftflags FILL-IN; the hand region narrowed to one judgment | `b75cff19` |
| 4 | R5 — the ruled dispatch verb | Forms card renders the verb FROM Ch8; new agreement gate over the two point-of-use sites | `43d940cc` |
| 5 | R6 — operator-interface capability file | `protocols/OPERATOR-INTERFACE.md`; forms card points at it; SUPPLEMENT Q6 narrowed | `d75acb03` |
| 6 | (contract step 6) | One attributed Ch8 Q1 note — container uv pinned-but-wrong, routing unchanged | `026be720` |
| 7 | (contract step 7) | Terra review, 6 passes, 9 findings fixed | `3d80436f` |

19 files, +1612 / −23. Two new ALL_CHECKS members (46 → 48). Two new script modules
(`scripts/dispatch_surface.py`, and `supplement_folded` inline in `audit.py`). One new protocols
file. Four of the five v5 templates edited.

---

## 2. The two decisions the contract left open, and how each was answered

**R4's either/or — regenerate the 2026-08-23 paste, or disposition it.** DISPOSITIONED as
**immutable-and-lost**, not regenerated. Three reasons, in order of weight:

1. `assemble_paste.py` writes `PASTE_THIS.md` **and** calls `reflow_framing`, which edits
   `HANDOFF_BOOT.md` / `RESIDUAL.md` / `PROBES.md` in place. Re-running it on a sealed bundle
   edits four immutable artifacts, not one (Critical Rule #3).
2. It would not un-lose anything. The seat that needed those 87 answer lines booted on 2026-08-25
   without them; rewriting the paste now falsifies what was actually delivered rather than
   delivering it.
3. The disposition register was never available for this even if repair had been the answer:
   `cmd_ship_gate` dispositions WARNs only, and the contract requires this check to be FAIL-class.

So the record lives in the check itself. `_SUPPLEMENT_FOLD_ERA = "2026-08-26"` gates the ADAPTER
only; a pre-era violation is NAMED in the pass evidence (`pre-era, immutable-and-lost (recorded,
not repaired): 2026-08-23-dev-knowledge-architect`) — permanently visible, never suppressed. The
PREDICATE is era-blind, so the contract's "must reproduce RED against that bundle" is satisfied
and reproducible: `tests/test_supplement_folded.py::test_predicate_reds_against_the_real_2026_08_23_bundle`
runs against the real tree, not a fixture.

**Measured, not assumed:** 63 bundles carry both a filled SUPPLEMENT ANSWERS region and an
assembled paste; 62 folded; exactly one did not. A second name appearing in that set fails the
suite (`test_predicate_finds_only_that_one_instance_in_the_live_corpus`).

**R3's era clause.** The contract said "historical bundles judged by their own era", which is
`HANDOFF_PROCESS` §5's own phrase for the `expected:` rung's ROW-SCOPING. Row-scoping alone was
not enough here, and the difference is worth recording: the `expected:` rung landed while the
ACTIVE bundle was already clean, whereas the 35 P10-bearing bundles are immutable and the NEWEST
of them is what `check_handoff_probes` reads on every commit. An ungated rung REDs audit-health
against an artifact nobody can fix. Hence a date, and hence the same date-predicate is now shared
with R4 rather than written twice.

---

## 3. Terra review — the loop

Run ad-hoc via `codex exec review -m gpt-5.6-terra` with a focus prompt, NOT `/codex-review`: the
wrapper's path guard routes a mixed `.py` + `.md` diff to the code profile and filters the prose
out entirely. Scope was stated inside the prompt (`git diff d8211b03...HEAD` plus staged changes,
with the six in-scope SHAs named), because `--base` and a custom PROMPT are mutually exclusive and
`main` moves under a lane.

| Pass | Findings | Verdict |
|---|---|---|
| 1 | 1 (P2) | era gate compared the whole dir name lexicographically |
| 2 | 1 (P1) | unreadable bundle file dropped from the result set → clean pass |
| 3 | 1 (P1) | same hole one level up: `is_file()` swallows a stat failure |
| 4 | 4 (2×P1, 2×P2) | same hole at the bundle dir and at `docs/handoffs/`; unbounded LOCAL-row search; a test that never reached the branch it claimed |
| 5 | 2 (P1) | non-calendar date prefix compared as pre-era; unreadable PLAYBOOK reported n/a |
| 6 | **0 — CLEAN** | "No actionable defects or answer-value leaks were found" |

**Tally: 9 findings — 9 fixed (2× P2 severity, 6× P1, 1× P2 test-quality), 0 refuted, 0 recorded
as accepted limits.** Every finding was ≥ medium and every one was fixed, so the contract's
"fix ≥ medium" condition is discharged with nothing deferred. Every one was a real defect in code this lane introduced.

**Seven of the nine are ONE class, found one level at a time**, and naming it is the point:
*a stdlib predicate that swallows OSError turns "I could not look" into "there is nothing here"*.
`Path.is_file()` and `Path.is_dir()` both return False on any OSError, and these checks treat
"nothing here" as a legitimate skip — so a Windows share lock or ACL change on a bundle file, a
bundle directory, `docs/handoffs/` itself, or `protocols/PLAYBOOK.md` would each have produced a
clean `pass` about evidence never opened, inside FAIL-class gates whose whole purpose is to refuse
that. The fix converged on one helper (`audit._path_state` → `'file' | 'dir' | 'absent' |
'unreadable'`) rather than seven patches. This is the [#438] thesis with fresh evidence: the suite
structurally could not catch it, because every test goes through the same entry point and the same
posture assumption the defect lives in.

The other two: an unbounded `find` in `dispatch_surface.ruled_form` (the row leaving the table
would have rendered a wrong fence confidently — the exact drift the reader exists to detect), and
one of this lane's own tests asserting less than it appeared to.

---

## 4. Accepted limits — stated, not covered

Each is written into the code it belongs to, so it survives this artifact.

- **The boundedness rung detects a SHAPE, not unboundedness in general.** It matches P10's own two
  quantifiers. A row asking for unbounded judgment in different words still passes it; rationale
  quality stays the manual gate (`HANDOFF_PROCESS` §5). Measured false-positive rate at authoring
  time: ZERO across 115 bundles and both live templates — the 36 matching files are all the
  P10/P7 grooming row itself.
- **`supplement_folded` asserts a SUPPLEMENT section exists, not that it is current.** A
  supplement edited after a fold still reads as folded. The measured failure class — a fold that
  never happened at all — is the one it refuses.
- **The dispatch gate is HALF of the organ §V describes, and says so.** The other half — every
  literal command in Ch8 resolving via `Get-Command` on the operator's machine — probes an L0
  surface in `win-tooling` and needs executing, which Layer 2 does not do. A verb that agrees
  everywhere and resolves nowhere passes this gate.
- **The R2 drift-organ binding manifest is curated**, with a reason per row, because no
  auto-enumerable organ→corpus map exists. Its scope is stated inside the rendered block so it
  cannot read as exhaustive, and a test asserts every key is a live registry name.
- **Rivals are refused inside a FENCED block only.** Both point-of-use files RECORD the §V
  correction in prose; a gate refusing the mention would force them to delete the history that
  explains why they changed.

---

## 5. Deviations and cross-lane notes — flagged, not buried

**1. `ecosystem/doc-code-edge.yaml` was edited, and the contract reserved `ecosystem/` to
lane-g2.** Two lines plus their reasons, appended at the END of `exempt:` so they conflict
cleanly. Structural rather than chosen: `check_doc_code_coverage_drift` is FAIL-class and names
any ALL_CHECKS member that is neither `# rule:`-annotated nor exempt, so neither R4 nor R5 could
enter the registry without an entry. `supplement_folded` is declared TEMPORARY (its rule is census
delta D4 against `HANDOFF_PROCESS` §13 and is not yet written); `dispatch_verb_agreement` is
declared PERMANENT (its rule IS written, at `STANDING_RULINGS` §V, but a ruling register is not a
living doc a `# rule:` marker can bind).

**2. `HANDOFF_PROCESS.md` was NOT edited, and two spec-side items are owed.** The contract's steps
did not ask for it and the file is large enough that a `last_reviewed` bump would be a claim this
lane cannot honestly make. Left for whoever takes the spec pass:
  - §5 "Structural enforcement" lists the answer-hint rung as the machine-held half of item 2's
    contract. It should list the boundedness rung beside it — the spec now describes one of two.
  - §13 owes the D4 rule the R4 exemption is waiting on. Writing it converts that exempt row to
    `coverage_scope`.
  Census delta D1's spec half was verified as a NO-OP rather than skipped: P10 is not in §5's
  manifest table; it appears only as the named ORIGIN of condition 4, which the removal upholds.

**3. Four commits carry a declared `SKIP=audit-health`, with the ownership proof in each body.**
`journal_spine_anchor` FAILs on `08b0d192` "Merge branch
'chore/workspace-provider-roots-2026-08-26'" (rdwornik, 2026-08-26 23:02:57 +0200), landed on main
by another session mid-lane. Diagnosed before acting, per the recorded procedure:
`git merge-base --is-ancestor 08b0d192 HEAD` exits 1 (not this lane's), and
`journal_anchor.unanchored_on_spine` returns the same single sha against this tree's `JOURNAL.md`
AND against `main:JOURNAL.md` — the "gap in BOTH" case, so a real unanchored merge on main rather
than lane-lag, and a sync-merge of main would buy nothing. Left un-discharged and reported: a
batch lane does not write the JOURNAL entry for another session's merge. Never `--no-verify`. A
full `audit.py health` run at each step showed that ONE `[!!]` and no other, so nothing this lane
wrote rode the bypass.

**4. Pre-existing RED, reported not absorbed.** Running `tests/test_gen_handoff.py` before
`tests/test_residual_completeness.py` in one process REDs three residual-completeness tests
(`module 'audit' has no attribute '_vrc'`): `gen_handoff.collect_hints` inserts the STUB repo's
`scripts/` at `sys.path[0]` and imports `audit` from there, so `sys.modules["audit"]` becomes a
one-line stub. Proved pre-existing by stashing this lane's entire diff and re-running the
identical pair — 3 failed, same three names. The same pollution silently defeated one of this
lane's own tests (it read an empty `ALL_CHECKS` and passed vacuously); that test now reads
`audit_checks.registry.CHECK_ORDER` instead, and its docstring records why.

**5. R1 (role-file residency) was NOT implemented** — the contract names it an OPERATOR decision.

---

## 6. Verification

- **Targeted, per step:** each step's own suites green before its commit.
- **Full suite:** run once at the end of the lane, per the per-step-targeted /
  full-at-integration cadence. **4004 passed · 24 failed · 11 skipped · 1 xfailed (20m08s).**
  **+63 tests added by this lane** (3977 → 4040 collected), and `ecosystem/doc-counts.md`
  regenerated for both drifts it caused (46 → 48 checks, 3977 → 4040 tests).

**Every one of the 24 failures attributed, and none is this lane's:**

| n | Test(s) | Cause | How it was proved |
|---|---|---|---|
| 17 | `test_fleet_analytics.py` | `ModuleNotFoundError: No module named 'pandas'` | Environmental — the lane venv lacks the `analytics` dependency group. Import-time failure in a module this lane never touched. |
| 2 | `test_audit.py::test_health_ok_with_registered_repo`, `::test_health_stays_ok_with_na_status` | `audit.py health` is DEGRADED | Directly observed at every step of this lane: a full `health` run prints exactly ONE `[!!]`, `journal_spine_anchor` on the foreign merge `08b0d192`, and nothing from either new check. |
| 1 | `test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement` | 44 undispositioned `docs/audits/` artifacts | Re-run with THIS lane's artifact removed from the tree — still RED, and not one of the 44 names is this lane's. |
| 1 | `test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings` | `BACKLOG#348` — 4 history dates spanning 32d | Re-run with this lane's artifact removed — still RED. This lane touched no BACKLOG file at all (see the diffstat). |
| 1 | `test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` | The reader sees the live lane worktree | Structural: running the full suite FROM a worktree is what produces it. |
| 1 | `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` | Anchor-gate probe | Pre-existing on `main` since 2026-08-22. |
| 1 | `test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export` | `ecosystem/conformance.htm…` reads the export | This lane touched no `ecosystem/` HTML and no export path. |

The honest limit on this attribution: five of the seven rows are argued from evidence gathered
inside this tree rather than from a clean re-run at the merge base. The two that could plausibly
have been this lane's — the new `docs/audits/` artifact tripping `funnel_coverage`, and `doc_rot`
— were the two settled by actually re-running with the artifact removed.
- **`ruff check`:** clean across `scripts/` and `tests/` at every commit.
- **`audit.py health`:** one `[!!]`, the foreign unanchored merge above, at every step.
- **Silent-rule ratchet:** main sits at its baseline with ZERO headroom, so every edited file in
  `protocols/*.md`, `templates/**` and `ecosystem/*.yaml` was measured before and after.
  `protocols/OPERATOR-INTERFACE.md` is a NEW protocols file and is **token-free (0)**; every other
  in-scope file is net-zero. No ratchet RED at any commit.

**Funnel note for the integrator:** this artifact is a new `docs/audits/` file and will surface as
an undispositioned `funnel_coverage` WARN until the batch's ledger dispositions it. That is the
organ working, not a defect.
