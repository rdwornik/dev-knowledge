# HY-3 — templates/ disposition: universalize, relocate or retire, one verdict per censused item

- **Class:** technical · **Date:** 2026-08-31
- **Source-session:** `lane-m-13-templates-disposition` (batch E, HY-3), contract
  `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-m-13-templates-disposition.md`
- **Status:** complete
- **Model:** opus, execute, high (per contract)
- **Inherited-vs-measured:** every per-file classification and consumer-resolution fact below
  is INHERITED verbatim from the two tier-(A) censuses this lane consumes —
  `docs/audits/2026-08-31-census-templates-consumers.md` (A2, the 47-file templates/ census)
  and `docs/audits/2026-08-31-census-single-file-folders.md` (A1, item #17 only — the one
  single-file folder under `templates/`). Nothing here re-measures a consumer. What is
  MEASURED in this run: (1) that no `templates/` drift occurred between A2's HEAD
  (`ec8731a9`) and this lane's HEAD (`git log ec8731a9..HEAD -- templates/` returns empty,
  file count still 47 pre-move); (2) an independent re-run of A2's zero-consumer grep for the
  two retired files, confirmed identical; (3) the two archive moves executed by this lane.

```
## Executive so-what

47 templates/ items, one disposition each. 44 UNIVERSALIZE (confirmed live, no action taken).
2 RETIRE — EXECUTED this lane: templates/JOURNAL-md-template.md and
templates/LESSONS-md-template.md moved to templates/archive/ with dated retirement headers,
in the E1-E4 convention. 1 class of 3 files RELOCATE — FLAGGED, NOT EXECUTED: the
workspace-{S,M,L} consolidation candidate, which A2 itself declined to rule on and which this
lane's decision budget does not cover (content authorship, not a mechanical move).
templates/archive/ (4 pre-existing + 2 newly retired = 6) is tracked SEPARATELY per
done-contract item 3 — not dead stock, not re-dispositioned. The one Z-G5 exception living
under templates/ is named per done-contract item 4. No live source was deleted. No merge, no
JOURNAL entry, no index regeneration, no row births.

## Disposition vocabulary (stated once, applied below)

UNIVERSALIZE  — the item is (or remains) genuinely load-bearing shared material with a
                resolved consumer at HEAD; current placement and packaging are correct;
                disposition confirms status quo. No tree action.
RELOCATE      — evidence supports a location or packaging change (move, merge, consolidate).
                Executed here only when mechanical and uncontested; otherwise reported as a
                flagged candidate pending ratification, per reconcile-before-birth.
RETIRE        — zero resolved consumers at HEAD. Disposition is retirement via relocation into
                templates/archive/ plus a dated retention header — never an rm (done-contract
                item 2). Executed here where the census evidence is airtight and re-verified.

## Findings

=== CLASS A — CARRIER (3 files) — disposition: UNIVERSALIZE (all 3) ===
Shipped identically to every consumer via deploy/manifest-v*.yaml. This class IS the literal
definition of "universal" in this corpus; no action needed or taken.

  templates/child-methodology-floor.md.tmpl   A2 A1 (manifest v1.1.0-v1.4.0; .gitattributes:14)
  templates/child-methodology-floor.sha256    A2 A2 (manifest sidecar pin; GENRE NOTE: a hash
                                               sidecar living in templates/ by adjacency to its
                                               subject, not a template — flagged by A2 as F-2,
                                               "no action proposed." UNIVERSALIZE stands; the
                                               genre anomaly is noted, not acted on.)
  templates/intake-template.md                A2 A3 (manifest v1.4.0:375-376,405-406,409)

=== CLASS B — HUB-LOCAL LIVE (21 files) — disposition: UNIVERSALIZE (all 21) ===
Each has a mechanical consumer (a generator path constant, a byte-match gate, a registered
spec, or an explicit retention ruling). None is dead, none needs relocation.

  B-i   RENDERED BY gen_handoff.py (8) — universalize, mechanical render sources:
        templates/handoff/v5/HANDOFF_BOOT.md.tmpl · v5/RESIDUAL.md.tmpl · v5/PROBES.md.tmpl
        · v5/SUPPLEMENT.md.tmpl · epic/EPIC_BOOT.md.tmpl · epic/EPIC_RETURN.md.tmpl
        · epic/PROBES.md.tmpl · functional/FUNCTIONAL_BOOT.md.tmpl
        Evidence: A2 B-i (gen_handoff.py:97-99,1197-1239; five also drift-guarded by
        test_residual_completeness.py:88).
        NOTE: functional/FUNCTIONAL_BOOT.md.tmpl's parent directory
        templates/handoff/functional/ is ALSO the done-contract item 4 Z-G5 exception — see
        below. The file's own disposition is UNIVERSALIZE regardless of its directory's
        single-file shape.

  B-ii  BYTE-MATCH-GATED CLAUDE.md REGION EXTRACTS (8) — universalize, cardinality-asserted:
        templates/claude-regions/{antipatterns-universal,conventions-commit-branch,
        conventions-output-formatting,critical-rules-consistency,critical-rules-no-leftovers,
        critical-rules-records,first-read,session-start-protocol}.md
        Evidence: A2 B-ii (test_boundary_headers.py:279-291 asserts checked == 8 — removing
        any one fails the suite; second site templates/CLAUDE-md-template.md SYNC markers,
        licensed by STANDING_RULINGS.md:3125).

  B-iii REGISTERED SPEC (1) — universalize:
        templates/prompt-template.md
        Evidence: A2 B-iii (_SPEC_REGISTRY entry; AGREEMENT_SITES; gen_lane_contract.py v1.14
        shape; 13 PLAYBOOK citations).

  B-iv  DECLARED-LIVE, UNEXERCISED — flat v4 cross-repo handoff set (8) — universalize:
        templates/handoff/{01_ROLE,02_METHODOLOGY,03_PROJECT,04_RECENT,05_NOW,06_QUESTIONS,
        07_ASK_BACK,README}.md.tmpl
        Evidence: A2 B-iv (.claude/commands/handoff.md:73,196-197; docs/handoffs/README.md:232;
        HANDOFF_PROCESS.md:445; PLAYBOOK:4223 — retained LIVE for cross-repo v4 by ADR-83
        ruling). No code path renders these; the absence of a mechanical reader is BY DESIGN,
        not neglect, per A2's own sub-classification. UNIVERSALIZE, not RETIRE: these already
        serve the fleet-wide (cross-repo) purpose that "universalize" names — they are simply
        not manifest-carried. A ruling (ADR-83), not a citation count, is what would change
        this disposition; none exists.

=== CLASS C — REFERENCE-ONLY, CITED (8 of 11) — disposition: UNIVERSALIZE ===
Each is opened by no code, but cited by a live doc as procedural or bootstrap material, with a
resolved reader at HEAD.

  templates/ADR-template.md                    A2 C1 (PLAYBOOK:4379(b))
  templates/ARCHITECTURE-template.md            A2 C2 (PLAYBOOK:5685)
  templates/CLAUDE-md-template.md               A2 C3 (PLAYBOOK:407; anchors the 8 B-ii markers)
  templates/audit-template.md                   A2 C4 (ADR-101:146, ratified citation)
  templates/codex-review-config-template.md     A2 C5 (PLAYBOOK:3889)
  templates/consumer-onboarding-runbook.md      A2 C6 (PLAYBOOK:3339; LESSONS.md:179)
  templates/scrum-master-cover-letter.md        A2 C7 (PLAYBOOK:5415,5459)
  templates/ruff-config-block.toml              A2 C8 (pyproject.toml:201 comment;
                                                 deploy/release-v1.3.x-contract.md:318;
                                                 fleet_parity.py:233,754 gates the resulting
                                                 FORM, never opens the file — genre note only)

=== CLASS C-EDGE — REFERENCE-ONLY, FALSE-WARN READER (1) — disposition: UNIVERSALIZE ===
  templates/CONTRIBUTING-md-template.md
  No live doc cites it; its only reader is the reconciled_versions sweeper, which produces a
  FALSE WARN on it (ecosystem/index.yaml:78) because a template's reconciled_with intentionally
  carries a fill-in placeholder. Evidence: A2 C-EDGE (test_validate_reconciliation.py:173,185
  encode the exemption case; open remediation tasks/335-exempt-templates-from-the-
  reconciled-versions-ch.md). UNIVERSALIZE stands: the file is not dead, its only "consumer" is
  a sweeper that should not be reading it, and [#335] already owns the fix. Not this lane's
  finding to re-file — reconcile-before-birth: the row already exists.

=== CLASS C — CONSOLIDATION CANDIDATE (3 files, C9-C11) — disposition: RELOCATE, FLAGGED NOT
    EXECUTED ===
  templates/workspace-S.code-workspace
  templates/workspace-M.code-workspace
  templates/workspace-L.code-workspace
  Evidence: A2's own "DONE-CONTRACT ITEM 2" verdict — live, cited (PLAYBOOK:992,994,997,
  bootstrap "cp templates/workspace-S..." workflow), retirement NOT supported. What survives
  is a design objection recorded at docs/audits/2026-05-25-ai-council-universalization-audit-
  refresh.md ("one maximal complex workspace template, scale-adaptive content, NOT
  scale-different templates"), routed to .dev-knowledge as a standards concern, marked OUT OF
  SCOPE there, and never picked up. A2's verdict verbatim: "an operator-stated preference and
  no ratified decision. It is not a dead-stock finding, and this lane rules nothing."
  THIS LANE ALSO RULES NOTHING ON THE MERGE ITSELF. Disposition is RELOCATE in the sense that
  the evidence supports consolidating 3 -> 1 + a selection note — but executing a 3-into-1
  content merge is authorship, not a mechanical move, and no ratifying decision exists for
  which content survives the merge. That is outside a lane's decision budget under contract
  defaults (it is not curated-baseline, not a rule-vs-ruling conflict, and not a fork class —
  it is simply unruled), so it is reported here as the actionable finding for the operator,
  not performed. All three files are UNCHANGED.

=== CLASS D — DEAD STOCK (2 files) — disposition: RETIRE, EXECUTED ===
  templates/JOURNAL-md-template.md   -> templates/archive/JOURNAL-md-template.md
  templates/LESSONS-md-template.md   -> templates/archive/LESSONS-md-template.md
  Evidence: A2 Class D (git grep -n "JOURNAL-md-template\|LESSONS-md-template" -- . returns
  exactly one tree-wide hit pre-move, an immutable audit line at
  docs/audits/2026-07-22-technical-hygiene-pre-handoff-inventory.md:14 — not a consumer. No
  manifest entry, no script/test/hook/command name, no protocol/ADR/task citation.
  RE-VERIFIED INDEPENDENTLY by this lane at its own HEAD (e96638da), post-A2: identical
  result, zero drift in templates/ since A2's ec8731a9.
  The 2026-07-22 hygiene inventory's "cited by live onboarding intake" claim does NOT resolve
  at HEAD (consumer-onboarding-runbook.md contains one occurrence of the word "template," about
  its own proposed home, and cites neither file) — A2's F-1 finding, a borderline-kept-with-
  reason verdict that outlived its reason.
  ACTION TAKEN: both files git-mv'd into templates/archive/, each carrying a first-line
  RETIRED header (2026-08-31, reason, census pointer, this audit's pointer) in the E1-E4
  convention — a relocation plus a retention rule, never an rm, per done-contract item 2.
  This is NOT the future templates_consumers.py organ's 30-day/ADR-111 automated clock (A2's
  drafted Rule D) — that mechanism does not exist yet; it is this lane's own one-time,
  contract-authorized disposition act, applied to evidence that is thirteen months stale and
  re-verified twice.

## templates/archive/ — treated SEPARATELY (done-contract item 3), not re-dispositioned

An already-archived template is not dead stock; conflating the two proposes deleting the
record. Six files after this lane's two additions — none of the six is assigned a
universalize/relocate/retire verdict; they are the RECORD that a retirement already happened.

  templates/archive/AGENTS-md-template.md            RETIRED 2026-05-19 (pre-existing, A1)
  templates/archive/HANDOFF_FOLDER_TEMPLATE.md       ARCHIVED 2026-06-26 (pre-existing, A2 E2)
  templates/archive/HANDOFF_QUESTION_TEMPLATE.md     ARCHIVED 2026-06-26 (pre-existing, A2 E3)
  templates/archive/HANDOFF_TEMPLATE.md              ARCHIVED 2026-06-26 (pre-existing, A2 E4)
  templates/archive/JOURNAL-md-template.md           RETIRED 2026-08-31 (new, this lane)
  templates/archive/LESSONS-md-template.md           RETIRED 2026-08-31 (new, this lane)

Two of the four pre-existing residents remain load-bearing test fixtures of record (A2 Class
E note): tests/test_normalize_headers.py:427 (HANDOFF_QUESTION_TEMPLATE.md, the named
unterminated-fence case) and tests/test_scan_undeclared_edges.py:319 (HANDOFF_TEMPLATE.md, the
named case proving templates/archive/ is NOT an immutable prefix). Unchanged by this lane.

## Class F — deferred stub (1 file) — disposition: UNIVERSALIZE (deferred)

  templates/handoff/v5/README.md.tmpl
  Retained by an explicit ruling that ALSO records it has no reader — STANDING_RULINGS T-35
  (row CLOSED, expiry open-ended): "No script reads the template," the seeder generalizes from
  the already-rendered docs/handoffs/README.md; HANDOFF_PROCESS.md:801 names the render-from-
  one-template shape "the DEFERRED design, not the built one ... it stays a deferred stub until
  #164 lands." Zero consumers is the EXPECTED state here, not a Class-D signal — A2's own Rule
  F exists specifically so a naive sweep does not eat this file. UNIVERSALIZE (deferred): it is
  the seed of a future fleet-facing render, governed by ruling T-35, not by this census. No
  action taken.

## Done-contract item 4 — the Z-G5 exception living under templates/

Z-G5 ("no single-file folders, ever," STANDING_RULINGS.md:3213) reaches exactly ONE directory
inside templates/'s footprint, per A1's tree-wide 23-directory census (predicate A):

  A1 item #17 — templates/handoff/functional/
    holds exactly one file: FUNCTIONAL_BOOT.md.tmpl (3,667 B)
    single since 5617fe17, 2026-07-06 ("feat(handoff): --mode functional ... [#268]")
    consumer: gen_handoff.py:99 _TMPL_DIR_FUNCTIONAL, a hard-coded module constant
              (also validate_hermetization.py:196 templates/handoff/* allowlist row)
    A1's own verdict: "BITES: MARGINALLY — the census's clearest 'file wearing a directory's
    clothes' that is not protected by an external convention ... the honest candidate if the
    operator ever wants Z-G5 to actually cost something."

  Granted IMPLICITLY, per A1 done-contract item 4: admitted by the WILDCARD row
  `templates/handoff/*` in scripts/validate_hermetization.py::_HOME_PATTERNS (Rule C home
  allowlist, operator ruling A of 2026-08-11, register K-1) — eighteen days before Z-G5 was
  ruled. Sibling shape: templates/handoff/ holds 8 flat .tmpl files plus three mode
  directories — epic/ (3 files), v5/ (5 files), functional/ (1 file) — so the single-file
  state is taxonomy symmetry with its siblings, not an isolated anomaly.
  This lane takes no action on it: its file disposition (above, Class B-i) is UNIVERSALIZE, and
  Z-G5's tension with the pre-existing Rule C allowlist is a repo-wide finding A1 already
  reported (not a templates/-scoped one, and not this lane's write-scope to resolve).

## Recommendations / routing

1. Workspace-{S,M,L} consolidation (RELOCATE, flagged): route the 2026-05-25 operator
   preference to intake (ADR-98) if the operator wants it acted on. Not filed here —
   reconcile-before-birth; no new row is born by this audit.
2. templates/child-methodology-floor.sha256's genre anomaly (A2 F-2) and
   templates/CONTRIBUTING-md-template.md's false-WARN reader (A2 F-3, task [#335] already open)
   — both reported for completeness, neither actioned; both already carried forward from A2,
   not new findings of this lane.
3. The dangling `codex` allowlist row and the two stale `.github/workflows/
   nightly-conformance-triage.yml` citations (A1's "actionable defect" and companion staleness)
   are OUTSIDE templates/ and outside this lane's write-scope — reported by A1, not re-filed
   here.

## Scope / method

Read-then-disposition only; A1 and A2 were not re-measured, per contract step 1. One
independent re-verification was performed (git log for templates/ drift since A2's HEAD; a
repeat of A2's zero-consumer grep for the two retired files) before executing the two archive
moves, per P0 "don't guess on irreversible changes." `conflict/` is confirmed to have no
subject in this repo (contract's own refutation, corroborated by A1 P1) — no conflict/ item is
dispositioned. Write-scope honored: templates/ (two git-mv's plus two header edits) and this
audit file only. No merge, no push, no JOURNAL entry, no index regeneration, no row births.
Escalations under the V-2 budget (a/b/c): NONE triggered — no curated-baseline touch, no
rule-vs-ruling conflict (A2's drafted Rule A-F is a proposal, not an operative rule, so no
conflict exists to escalate), no fork class without a standing ruling.
```
