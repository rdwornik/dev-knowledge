# Codex Review — lane-landing-window

**Date:** 2026-09-24
**Branch:** `worktree-lane-landing-window`
**HEAD:** `f6bfcece`
**Diff range:** `main..worktree-lane-landing-window`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/5/0/0 <!-- Critical/High/Medium/Low. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code (path-guard routed on `tasks/manifest.json`; the review scope was
restricted to that file, per the wrapper's mixed-diff rule — see "Scope limit" below)
**Consumer:** LANE-5A-5 (`H:\My Drive\CLAUDE PROMPT DIR\LANE-5A-5-landing-window.md`), done-contract
item 7 ("Codex terra review (consumer cited); self-check and purity; handback").

**Scope limit, recorded rather than silently accepted:** the code-vs-doc path-guard classified
this diff as code because it includes `tasks/manifest.json` (`.json` is on the code-extension
allowlist), which routes the ENTIRE mixed diff to the code profile and drops every `.md` file
from scope — so the ~70 new/edited markdown files (STANDING_RULINGS.md, the 45 new task bodies,
the transport carried-by edits) were not reviewed by this pass. All five findings below are
against `tasks/manifest.json`'s row content, which the wrapper did surface despite the file being
data, not code. The `.md` bodies were checked by this lane's own citation-by-citation P11
verification (every carried-by/refs path was resolved against `git cat-file -e main:<path>`,
which caught and fixed several fabricated-path errors before this review ran).

---

## Focus

- Verify every carried-by / STANDING_RULINGS.md AK-section citation actually names a file/row that exists (no fabricated repo homes)
- Verify the 45 new backlog rows (tasks 964-1008) don't duplicate existing OPEN rows and correctly cite ADR-120 + the window-defects audit
- Verify the P9 grammar fixes (tasks 664, 906, 908-914) preserved row meaning and only changed formatting/grammar
- Flag any place a claim of "landed"/"CLOSED" overstates what actually exists in the repo

---

## Findings
## CRITICAL

(none)

## HIGH

### [HIGH] tasks/manifest.json:789 — 25 new rows omit the required window-defects source

**What:** Nodes `#965–#970`, `#988–#999`, and `#1001–#1007` cite ADR-120 but do not cite `docs/audits/2026-09-23-technical-window-defects.md`.
**Why:** Their D/O claims lose the required primary provenance and cannot be traced back to the registered defect.
**Fix direction:** Add the window-defects audit citation to each affected row.

### [HIGH] tasks/manifest.json:805 — #969 duplicates existing open #959

**What:** #969 re-owns JSON gate verdicts, connection-test JSON consumption, and the ≤10-minute split already in #959’s open Done-when.
**Why:** Two OPEN rows now own the same delivery, making closure and accountability ambiguous.
**Fix direction:** Fold the additional requirement into #959 or explicitly narrow one row to a non-overlapping residual.

### [HIGH] tasks/manifest.json:829 — #975 and #976 split work already owned by open #957

**What:** #975’s origin/purity merge path and #976’s merge-receipt/ledger work are acceptance legs of #957’s still-open single merge-path row.
**Why:** The new rows state they sit inside #957’s scope but retain `kill-candidates: none`, creating overlapping OPEN ownership.
**Fix direction:** Make them explicit dependent sub-rows with a closure relationship, or consolidate them into #957.

### [HIGH] tasks/manifest.json:925 — #999 claims discharge without its required standing-ruling citation

**What:** #999 says it is “discharged” by this lane’s STANDING_RULINGS landing, but remains OPEN and does not cite an AK entry; AK-7 also does not state the dispatcher-only ruling.
**Why:** This overstates the landing state and leaves the row’s own Done-when unmet.
**Fix direction:** Add a standing-ruling entry that states R-09-19-10 and cite it from #999, or remove the discharge claim.

### [HIGH] tasks/manifest.json:1925 — P9 source-label changes are not grammar-only and are unresolvable

**What:** #908–#914 replace generic provenance with `AMEND-*` identifiers that occur only in those task files; no corresponding repository artifact or transport locator exists.
**Why:** This changes row provenance rather than formatting/grammar and creates unverifiable authority citations.
**Fix direction:** Restore the prior wording or add resolvable source locators for each named amendment.

## MEDIUM

(none)

## LOW

(none)

---

## Disposition

- **25-row window-defects citation gap:** confirmed for `[#965]`-`[#970]` (D2-D7, the rows genuinely
  drawn from `docs/audits/2026-09-23-technical-window-defects.md`'s table) — fixed, citation added
  to each `refs` clause. **Not applicable** to `[#988]`-`[#992]` (D30-D34, which correctly cite the
  *amendment* register `docs/audits/2026-09-23-technical-window-defects-amend.md` instead — the
  right primary source for those items) nor to `[#993]`-`[#999]` (S3 operator-request items, sourced
  from `docs/audits/2026-09-23-technical-handoff-readiness.md`, not the window-defects register) nor
  to `[#1001]`-`[#1007]` (S2 hook-architecture items, sourced from
  `docs/audits/2026-09-23-technical-hook-architecture.md`) — the finding's file-range was broader
  than the actual defect.
- **`[#969]` duplicates open `[#959]`:** CONFIRMED — `[#959]` (lane-gate-verdicts) already merged
  the JSON-verdict/runtime mechanism (`3d3b3a0e`) but remains `status: open`, and D6 was written the
  same day without cross-referencing it. Fixed: `[#969]` now discloses the overlap, its Done-when
  starts with re-verifying D6 against `[#959]`'s landed evidence before building anything, and its
  kill-candidates name `[#959]`.
- **`[#975]`/`[#976]` split work owned by open `[#957]`:** already self-disclosed in both rows'
  original kill-candidates ("sits inside lane-merge-path's scope (W4B-1, deferred)") — a layering
  pattern this backlog already uses elsewhere (e.g. `[#959]` citing `[#955]` as "the epic this row
  implements"), not a silent duplicate. Left as filed; no further change judged necessary.
- **`[#999]` claims discharge without its named ruling in STANDING_RULINGS:** CONFIRMED — AK-7
  covered DECLARE-NIGHT-AUTONOMY's seven mechanisms but never stated R-09-19-10 ("the dispatcher
  dispatches") by name. Fixed: AK-7 now carries an explicit R-09-19-10 paragraph citing `[#999]`.
- **P9 source-label changes for `[#908]`-`[#914]` are not grammar-only:** CONFIRMED — this was a
  judgment call flagged as such during filing (see the row-level commentary in this lane's own
  session record) and the independent review corroborates the concern. Fixed on two tracks:
  `[#908]`-`[#911]` ("BUILD MODE B2 integration order") now cite the real, existing, verified
  transport file `DECLARE-BUILD-MODE-2026-09-18.md` (its §4 literally defines "BATCH B2"), found by
  searching the transport rather than inventing a name. `[#912]`-`[#914]` ("night wave 2 integrator
  ruling") had no real DECLARE/AMEND counterpart on the transport (only a `to-browser/INTEGRATOR-*`
  receipt, which the `implements:` grammar cannot express) — the fabricated citation was removed
  rather than replaced, since `implements:` is an optional field (`_implements_tokens` returns `[]`
  for a missing clause, which is not a P9 hard-fail) and omitting it is more honest than a
  plausible-looking token naming nothing. All fixes re-verified: `validate_backlog.py` OK (486
  tasks, 0 hard-fails), `gen_task_tree.py --check` OK.