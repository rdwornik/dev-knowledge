# Lane packet — lane N, `[#528]` legs 1+2 (lane-latency)

- **T_start:** 2026-08-15T14:33:31Z
- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-15 · **Slug:** 528-legs12-packet
- **Lane:** `lane-n-528-legs12-latency` · branch `worktree-lane-n-528-legs12-latency` · base
  `d62796ad` (`main`)
- **Contract of record:** `docs/audits/2026-08-15-technical-528-legs12-latency-lane-contract.md`
- **Derived manifest:** `docs/audits/2026-08-15-technical-528-legs12-manifest.md`
- **Legs executed:** (1) and (2). **Leg (3) is not this lane's** — it is owed after `[#529]`
  lands, and `[#528]` therefore does **not** close here.

---

## §1 Manifest as executed

Three files modified, exactly the derived manifest §2, plus the two mandated regen surfaces.

| Path | What changed |
|---|---|
| `.claude/skills/verify/verify.py` | L24 gate-run command takes `-n auto --dist worksteal --max-worker-restart=0`, with the reason for each flag recorded at the site |
| `protocols/PLAYBOOK.md` | new `#### Tiered suite — targeted in-lane, one full suite at integration` in Ch5, after "Per-step test cadence"; one cross-reference clause on Ch8's "Full suite run once on the merged result" bullet |
| `protocols/ESSENTIALS.md` | one pointer bullet in "Parallel sessions"; `last_reviewed` 2026-08-10 → 2026-08-15 |
| `docs/audits/README.md` | audit-index regen (mandated by `audit-index-freshness` for each new audit file) — regen-at-merge surface, excluded from the footprint by the contract's file discipline |
| `docs/audits/2026-08-15-technical-528-legs12-{latency-lane-contract,manifest,packet}.md` | this lane's own three artifacts |

**Nothing outside that list was touched.** `git diff --name-only main...HEAD` at STOP returns
exactly six paths (the three above plus the index and two artifacts; this packet makes seven).
No BACKLOG row, no `tasks/` body, no `[#id]` birthed, no new repo path, no register or
`STANDING_RULINGS` edit.

## §2 Per-step commit SHAs

| Step | SHA | Subject |
|---|---|---|
| 0 (dispatch line) | `ff2066ee` | contract of record committed byte-identical (I-D3) |
| 0b | `1d37e3da` | DERIVED OWNED-FILES manifest, before any edit |
| 1 — leg 1 | `01ee2cb1` | the gate-run pytest call site takes the xdist flags |
| 2 — leg 2 | `d0610add` | the tiered-suite law lands in Ch5, ESSENTIALS points to it |
| 3 — packet | this file | targeted-test evidence + exclusions owed at integration |

Every commit passed the full hook mesh. **Zero `--no-verify`, zero `SKIP=`, zero merges, zero
pushes.** Hooks observed firing across the arc: `normalize-dated-headers`,
`audit-index-freshness`, `validate-hermetization`, `organ-index-freshness`,
`toc-freshness-playbook`, `audit-health`, `ruff`, `backlog-id-on-close`,
`backlog-filing-backpressure`.

## §3 Targeted-test evidence

Derived, not chosen: every tracked test file referencing `skills/verify`, `PLAYBOOK`,
`ESSENTIALS`, `gen_audit_index` or `validate_hermetization` was enumerated by grep, then each was
read at its hit to separate a **live-tree assertion** from an incidental fixture string. Sixteen
files carried a live assertion and were run; five (`test_block_immutable_edits`, `test_gen_handoff`,
`test_merge_serialization`, `test_propose_closures`, plus the `RUN_E2E`-gated
`test_e2e_consumer_lifecycle`) reference the paths only as strings and were not.

All three runs used this lane's own new gate shape — `uv run --locked pytest -n auto
--dist worksteal --max-worker-restart=0 --tb=short -q` — so leg 1's flags are exercised by the
evidence for leg 1 rather than only asserted. `-x` is dropped in these runs so the full outcome
set is visible; the committed call site keeps it.

| Run | Files | Result | Wall |
|---|---|---|---|
| 1 | `test_generate_organ_index`, `test_review_artifact_coverage`, `test_validate_doc_structure`, `test_doc_code_edge`, `test_scan_undeclared_edges`, `test_coherence_integration`, `test_assemble_paste`, `test_gen_audit_index`, `test_validate_hermetization`, `test_toc` | **316 passed** | 80.79 s |
| 2 | `test_audit`, `test_ship_gate` | **1 failed · 212 passed** | 539.18 s |
| 3 | `test_handoff_modes`, `test_validate_landing_predicate`, `test_generator_newlines`, `test_fleet_analytics` | **92 passed** | 23.36 s |

**Totals: 620 passed · 1 failed · ~644 s.** `ruff check` → All checks passed.
`git status --short` → empty. `git stash list` → empty. `audit.py health` → **OK**, zero FAIL and
zero WARN.

`test_toc.py` is a **corpus-tier** file under the doctrine this lane just wrote, and it was run
anyway — PLAYBOOK's TOC is a touched surface, so the oracle/corpus rule's own "plus anything
covering the touched module" clause owes it. Stated because a lane that writes an exclusion rule
and then quietly uses it to skip its own coverage is the failure this packet exists to prevent.
The oracle tier was **not** owed: this lane touches neither `scripts/safe_remove.py` nor
`scripts/reverse_dep_oracle.py`.

### The one RED, proven pre-existing rather than asserted

`tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` — the known
`[#457]` leg (ii) RED. Three independent proofs, not one:

1. **Its inputs are byte-identical to `main`.** `git diff --stat main -- BACKLOG.md tasks/
   scripts/audit.py` is empty; the check parses `BACKLOG.md`, which this lane did not touch.
2. **Its evidence line matches the record.** `check_routine_consumers` on this tree returns
   `2 declared routine row(s) name a consumer and a consumption_path`, which is the string
   `JOURNAL.md` 2026-08-15 (a) already records as the pre-existing state — it used the same
   byte-identity argument to prove the same RED was not the boot-acts arc's.
3. **It is a live-repo BACKLOG assertion**, in the class the night-2 lane-latency audit §1c item
   13 also classified as known-pre-existing.

## §4 Exclusions owed at integration

Enumerated in full in the manifest §4; repeated here as a list the integrator can act on.

1. **`plugins/tier1-lifecycle/commands/ship.md` L37** — already carries `-n auto --dist
   worksteal -x --tb=short`; **lacks `--max-worker-restart=0`**. Out of this lane's candidate
   class (markdown, not a Python call site) and in the deployed plugin corpus, so a change here
   propagates to every consumer. `[#340]` already owns this command's pre-flight shape.
2. **`plugins/tier1-lifecycle/commands/ship.md` L32** — docs-only branch `pytest -m live_repo -q`;
   inherits `-n auto`, no worksteal, no restart cap. Same reasoning.
3. **`.claude/commands/lane-integrate.md` L37, L59** — `uv run --locked pytest -q`. This *is* the
   doctrine's tier B. It inherits `-n auto` and carries neither of the other two flags.
4. **`.github/workflows/report-only-wall.yml` L141** — deliberately **not** a gate
   (`continue-on-error: true`, "Report-only, permanently"); listed so its absence from leg 1 is a
   recorded decision rather than an oversight.
5. **Carrier surfaces** — `templates/child-methodology-floor.md.tmpl` L16,
   `templates/CLAUDE-md-template.md` L52, `templates/claude-regions/session-start-protocol.md`
   L6. Byte-coupled or consumer-shipped; a carrier edit is its own arc.
6. **The two source audits are unmerged drafts.** The doctrine cites `8387ff2a` and `757077f2` by
   SHA with their branches named (`claude/night2-latency-audit-6s1k6p`,
   `claude/night2-research-d30vhu`). If either branch is dropped rather than merged, those
   citations become history-only — reachable, but not via `git ls-tree main`.

**The HARD EXCLUSION cost this lane nothing, and that was checked rather than assumed.**
`.pre-commit-config.yaml` contains no `pytest` invocation and this repo has no `.claude/hooks/`
directory, so lane O (`lane-o-527-block-main`) holds no gate-run call site this lane needed.

## §5 Decisions taken under the V-2 budget

Nothing escalated: no curated-baseline touch, no rule-vs-ruling conflict, no fork class without a
standing ruling arose. Five decisions, each per contract defaults, each reported here.

1. **Doctrine home = PLAYBOOK Ch5, directly after "Per-step test cadence."** The cadence states
   *when* a suite runs and the new subsection states *which*; adjacent, they read as one rule.
   Ch8's batch protocol already carried the integration half ("Full suite run once on the merged
   result"), so putting the tier definitions there would have split one rule across two chapters.
2. **One cross-reference clause added to that Ch8 bullet.** A second site in the same
   manifest-listed file, taken so a seat reading the batch protocol finds the tier definition
   without knowing to look in the testing chapter. The contract says "paragraph(s)", so this is
   inside its grant, but it is a second site and is reported as such.
3. **PLAYBOOK's `Last updated: 2026-08-01` header left standing.** The 2026-08-15 boot-acts arc
   also edited this file and left it; bumping it would assert a whole-document currency this lane
   did not verify. PLAYBOOK is deliberately outside `DEFAULT_FRESHNESS_FILES`, so no gate is
   involved either way. Flagged as an observation, not fixed.
4. **No JOURNAL entry from this lane.** `JOURNAL.md` is not in the derived manifest, and PLAYBOOK
   Ch8 states letters are allocated **at integration by the primary's single writer**. The
   integrator's entry anchors this lane's merge; a lane-written entry would contend for a letter
   it cannot safely derive. If the `Stop` backpressure hook asks for one, the answer is this
   paragraph — the hook is advisory in full since the ADR-85 amendment 2026-08-03 §A5.
5. **The two collect-only / proof call sites left byte-unchanged**, with reasons recorded in
   manifest §3 rather than flags added. `validate_doc_claims.py:137` runs no tests, so a
   distribution policy governs nothing there; `worktree_import_proof.py:416` already drops
   `addopts` and unloads the plugin deliberately, and a `-n` flag added under
   `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` lands in the exit-4 shape `pyproject.toml` L83–91 documents.

## §6 Deviations and findings, self-reported

**Deviations from the contract: none.** Every step landed as written, in order, with the stated
commit shape.

**Three findings the architect should see, none of which this lane acted on.**

1. **A grep-derived targeted set on a DOC diff is not cheap, and it is not tier A.** This lane's
   16-file selection cost **~644 s** — about 70 % of the host's 918.9 s full suite. That does
   **not** falsify the doctrine's 38.7 s tier-A bound, because the two measure different sets:
   tier A is *all* tests minus five excluded files, while this was a *selection* of files
   covering a documentation diff. The two are stated separately in the doctrine text for exactly
   this reason. What it does show is that impacted-test selection over doc surfaces
   (`[#278]`'s territory) lands in a different cost regime than the cost-tier split does.
2. **`test_audit.py` + `test_ship_gate.py` cost 539.18 s on this Windows host** at `-n auto
   --dist worksteal`, for 214 tests. The night-2 audit's cloud profile put `test_audit.py` at
   32.45 s serial. Both files sit **inside tier A**. The cloud→host ratio the audit warns about
   (`INDICATIVE; ratios travel, absolute minutes do not`) therefore bites tier A too, and the
   ~0.9 min tier-A projection is a *cloud* projection. A one-run host measurement of the actual
   tier-A set would settle it; that is a measurement, not this lane's contract.
3. **`--max-worker-restart=0` is now live at one call site and absent at the three markdown
   ones.** Until §4 items 1–3 are taken, the repo's gate-run surfaces disagree about the restart
   cap — which is precisely the "stray workers outside the tuned path" condition `[#528]` leg (1)
   was opened on, narrowed but not closed.

## §7 Constraint verification at STOP

| Constraint | Verdict |
|---|---|
| `silent_rule_ratchet` | **440 ≤ baseline 441**, measured before the edits and again on the staged blobs — unmoved. Zero `must\|shall\|never` tokens in the added prose (counted on the staged diff, case-insensitive). |
| `canonical_freshness` | green. `ESSENTIALS.md` re-stamped 2026-08-15 after a genuine end-to-end re-read of all 181 lines from disk, done before the edit; no defect found in its other sections. |
| `toc-freshness-playbook` | `python -m scripts.toc.cli check protocols/PLAYBOOK.md` → exit 0. The new heading is `####`; PLAYBOOK's TOC covers `##`/`###` only. |
| `audit.py health` | **OK** — zero FAIL, zero WARN, at STOP. |
| `git status --short` | empty. |
| `git stash list` | empty (lane requirement 4 / refuse-to-finish item 5). |
| Env | `uv sync --locked --group analytics` run at boot; every invocation `uv run --locked`. `worktree_import_proof.py` → `NOT-APPLICABLE` (exit 3), which is the hub's correct answer, not a PASS. |

---

**STOPPED.** Branch `worktree-lane-n-528-legs12-latency` is handed back at `d0610add` plus this
packet commit. Not merged, not pushed. `[#528]` stays open — leg (3) is owed after `[#529]`.
