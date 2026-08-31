> **PROVENANCE - harvested cloud artifact, body VERBATIM below this header.**
> Lane `batch-e-a2-templates-consumer-census` | receipt id `cse_01NBnDtWhQGwVqFtvcqrwVhG` | dispatched 2026-08-31, harvested 2026-08-31 by
> `Save-CloudSessionReport` (the `Harvest-Cloud` alias). Batch E tier (A); the frozen contract is
> `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a2-templates-consumer-census.md`.
> Selection rule: the LONGEST assistant text, not the last - text #2 of 10 across 4 pages.
> Bytes written unchanged: **27,371**.
> Harvester DEVIATION, recorded not repaired: the report contains no markdown heading at all; bytes UNCHANGED.
> Nothing below this line was edited, reflowed or trimmed.
>
> **Consumed by:** HY-3 (`lane-m-13-templates-disposition`).
>
> **This lane was READ-ONLY by contract** - zero tree writes, zero commits, zero rows, no gate
> run and none asserted.

---

Census complete. Read-only throughout — no tree writes, no commits, no gates run and none asserted.

```
CENSUS — templates/ CONSUMER CENSUS
lane: batch-e-a2-templates-consumer-census
branch: claude/batch-e-a2-templates-consumer-census
contract: LANE-batch-e-a2-templates-consumer-census.md
HEAD measured: ec8731a9b2fdcc7fffee59bb0743a8b467f65c0b
write-scope honored: ZERO rows, ZERO tree writes, ZERO commits

=== RECEIPT ===
git-source-resolves-non-empty: https://github.com/rdwornik/dev-knowledge (origin, fetch+push)
first-assistant-text-echoed: 105 lines; final line verbatim ->
  "- No edits outside this lane's declared footprint. Prose in English; hyphen-only names."

=== STEP 1 — SUBSTRATE RE-MEASURED AT HEAD ===
git ls-files templates/ | wc -l  ->  47
Delta vs the freeze-time figure of 47: ZERO. The brief's substrate number holds.

Shape: 18 at templates/ root · 8 templates/claude-regions/ · 8 templates/handoff/ (flat v4)
       · 3 templates/handoff/epic/ · 1 templates/handoff/functional/
       · 5 templates/handoff/v5/ · 4 templates/archive/.  Sum = 47.

=== METHOD — WHAT COUNTS AS A CONSUMER (stated, because it decides every verdict) ===
A consumer RESOLVES THE FILE BY NAME: a manifest source entry, a generator path constant,
a validator/test that opens it, or a command that instructs an agent to drive it.

EXCLUDED from consumer resolution: glob-scope sweepers that ingest templates/ wholesale.
  scripts/silent_rule_detector.py:137-138  SCOPE_GLOBS = templates/**/*.md, templates/**/*.tmpl
  scripts/preflight_contract.py:926,949    ratchet scope recurses into templates/
  scripts/validate_hermetization.py:223-224 home allowlist: templates, templates/archive,
                                            templates/claude-regions, templates/handoff, .../*
  scripts/funnel_coverage.py:104           baseline enumerates templates/**/*.{md,tmpl}
  scripts/validate_reconciliation.py:182-192 a templates/-prefixed path predicate
  scripts/consumer_at_landing.py:32        templates/ named as a landing root
  scripts/gen_handoff.py:658               fleet_parity edge names templates/ as a directory
These read EVERY template by construction. Counting them makes DEAD STOCK empty by
definition and the census vacuous. They are scope consumers, not purpose consumers.

=== CLASS A — CARRIER (shipped to a consumer by a deploy/manifest-v*.yaml entry) — 3 files ===

A1  templates/child-methodology-floor.md.tmpl
    manifest: deploy/manifest-v1.1.0.yaml:319, v1.2.0:503, v1.3.0:568, v1.3.1:577,
              v1.4.0:709  -> "source: templates/child-methodology-floor.md.tmpl"
    also code-resolved: scripts/generate_floor.py:53 TEMPLATE_PATH = _REPO_ROOT/"templates"/...
                        deploy/release_lint.py:85 FLOOR_TMPL_REL
    .gitattributes:14 pins its eol. Strongest consumer chain in the tree.

A2  templates/child-methodology-floor.sha256
    manifest: v1.1.0:61, v1.2.0:66, v1.3.0:81, v1.3.1:90, v1.4.0:102 — pinned as THE sidecar
              whose bytes the floor hash must equal.
    code: scripts/generate_floor.py:55 HUB_CANONICAL_SHA; deploy/release_lint.py:86
          FLOOR_SIDECAR_REL; tests/test_deploy_floor.py:17;
          plugins/tier1-lifecycle/commands/ship.md:57,61 (consumer-side read at ship time).
    GENRE NOTE: this is a 64-hex hash sidecar, not a template. It lives in templates/ only
    because its subject does. Flagged, not repaired.

A3  templates/intake-template.md
    manifest v1.4.0:375-376 source+path; :405-406 verify block; :409 roster line.
    code: deploy/carrier_docs.py:12,15; tests/test_deploy_docs.py:46,83,91,196-199,217,234,282,293
    doc: .claude/methodology-roster.md:15; protocols/HANDOFF_PROCESS.md:947
    Only manifest entry in templates/ that is genuinely a template.

=== CLASS B — HUB-LOCAL LIVE (a generator, validator, gate or command resolves it) — 21 files ===

B-i  RENDERED BY scripts/gen_handoff.py (path constants at :97-99) — 8 files
  templates/handoff/v5/HANDOFF_BOOT.md.tmpl   gen_handoff.py:1237 _render(...)
                                              tests/test_gen_handoff.py:209,1026;
                                              tests/test_v6_frozen_contract.py:163
  templates/handoff/v5/RESIDUAL.md.tmpl       gen_handoff.py:1238
  templates/handoff/v5/PROBES.md.tmpl         gen_handoff.py:1239;
                                              tests/test_verify_handoff_probes.py:1381;
                                              scripts/verify_handoff_probes.py:136
  templates/handoff/v5/SUPPLEMENT.md.tmpl     gen_handoff.py:1227 _substitute(_TMPL_DIR/...);
                                              tests/test_assemble_paste.py:11,430;
                                              .claude/commands/handoff.md:119
  templates/handoff/epic/EPIC_BOOT.md.tmpl    gen_handoff.py:1199 (tmpl_dir=_TMPL_DIR_EPIC)
  templates/handoff/epic/EPIC_RETURN.md.tmpl  gen_handoff.py:1197
  templates/handoff/epic/PROBES.md.tmpl       gen_handoff.py:1200 (tmpl_dir=_TMPL_DIR_EPIC)
  templates/handoff/functional/FUNCTIONAL_BOOT.md.tmpl
                                              gen_handoff.py:1214-1215 (_TMPL_DIR_FUNCTIONAL)
  Five of these are additionally covered by the FILL-IN drift guard
  tests/test_residual_completeness.py:88 (rglob over templates/handoff/**/*.tmpl):
  FUNCTIONAL_BOOT, v5/RESIDUAL, v5/PROBES, v5/HANDOFF_BOOT, epic/EPIC_BOOT.

B-ii BYTE-MATCH-GATED REGION EXTRACTS — 8 files (templates/claude-regions/)
  antipatterns-universal.md · conventions-commit-branch.md · conventions-output-formatting.md
  · critical-rules-consistency.md · critical-rules-no-leftovers.md · critical-rules-records.md
  · first-read.md · session-start-protocol.md
  Gate: tests/test_boundary_headers.py:279 tpl = _ROOT/"templates"/"claude-regions";
        :285 pytest.fail if an owner=hub region has no extract;
        :287 assert extract bytes == CLAUDE.md region body;
        :291 assert checked == 8  <- the cardinality is asserted, so removing ANY ONE fails
        the suite. Hardest non-manifest consumer in templates/.
  Second site: templates/CLAUDE-md-template.md:24,50,58,65,70,75,83,122 SYNC-verbatim markers.
  Standing licence to move them in lockstep with CLAUDE.md: STANDING_RULINGS.md:3125.

B-iii REGISTERED SPEC — 1 file
  templates/prompt-template.md
    scripts/validate_reconciliation.py:121 — a _SPEC_REGISTRY entry ("prompt-template").
      This makes it a VERSIONED SPEC whose bumps arm coherence-nudge. Not merely a template.
    scripts/dispatch_surface.py:44 AGREEMENT_SITES (one of two provider-agreement sites)
    scripts/gen_lane_contract.py:5,43,96 — the emitted lane contract follows its v1.14 shape
    scripts/gen_handoff.py:655 reconciled_versions edge; scripts/audit.py:2014
    tests/test_dispatch_surface.py:126,140,166
    PLAYBOOK:671,831,1798,1870,2019,2508,2592,2784,2970,3090,3112,4062,4222

B-iv DECLARED LIVE BY A COMMAND, RENDERED BY NOTHING — 8 files (the flat v4 set)
  templates/handoff/01_ROLE.md.tmpl · 02_METHODOLOGY.md.tmpl · 03_PROJECT.md.tmpl
  · 04_RECENT.md.tmpl · 05_NOW.md.tmpl · 06_QUESTIONS.md.tmpl · 07_ASK_BACK.md.tmpl
  · templates/handoff/README.md.tmpl
  Declaration: .claude/commands/handoff.md:73 and :196-197 — "Templates (retained live) ...
    kept for cross-repo v4 per ADR-83"; docs/handoffs/README.md:232 "the v4 templates under
    templates/handoff/ are intentionally retained"; protocols/HANDOFF_PROCESS.md:445
    ("kept templates/handoff/** LIVE"); PLAYBOOK:4223 names 02_METHODOLOGY specifically.
  Mechanical state: gen_handoff.py's _TMPL_DIR is templates/handoff/v5, NOT the flat parent.
    No code path renders these eight. They are agent-driven copy material for a legacy v4
    cross-repo handoff, retained by ADR-83 ruling.
  SUB-CLASS: "declared-live, unexercised". A retention decision exists and is recorded; the
    absence of a mechanical reader is by design, not by neglect.

=== CLASS C — REFERENCE-ONLY (cited by a live doc; no code resolves the path) — 11 files ===

C1  templates/ADR-template.md            PLAYBOOK:4379(b) — the ADR-distillation prompt aligns
                                          drafts to it. Live procedural citation.
C2  templates/ARCHITECTURE-template.md   PLAYBOOK:5685 — the named remedy when a repo lacks
                                          ARCHITECTURE.md or its CODEMAP markers.
C3  templates/CLAUDE-md-template.md      PLAYBOOK:407 — "the canonical 12-section skeleton".
                                          Also the anchor holding the 8 B-ii SYNC markers.
C4  templates/audit-template.md          ADR-101:146 — "author-facing skeleton ... carries the
                                          filename grammar", peer of intake-template. A live
                                          ADR, so this is a ratified citation, not prose drift.
C5  templates/codex-review-config-template.md   PLAYBOOK:3889 — Codex review configuration.
C6  templates/consumer-onboarding-runbook.md    PLAYBOOK:3339 (Stage-4 enforcement-in-effect
                                          worked example) + LESSONS.md:179 (same doctrine).
C7  templates/scrum-master-cover-letter.md      PLAYBOOK:5415 and :5459 — operator copies it,
                                          fills placeholders, pastes to a target-repo architect.
C8  templates/ruff-config-block.toml     pyproject.toml:201 "Canonical: templates/ruff-config-
                                          block.toml" (a COMMENT, not a read);
                                          deploy/release-v1.3.x-contract.md:318 "copy-paste
                                          MATERIAL". scripts/fleet_parity.py:233,754 gates a
                                          ruff_config_form probe — it gates the resulting FORM
                                          in consumers, and never opens this file.
C9-C11 templates/workspace-{S,M,L}.code-workspace   PLAYBOOK:992 + :994 + :997 — see VERDICT.

C-EDGE  templates/CONTRIBUTING-md-template.md
  No live doc cites it. It is nonetheless OPENED by the reconciled_versions check, which is
  a scope sweeper — and the read produces a FALSE WARN, on the record:
    ecosystem/index.yaml:78  "templates/CONTRIBUTING-md-template.md: malformed
                              (reconciled_with not '<spec-id>@<version>')"
  because a template's reconciled_with intentionally carries a fill-in placeholder.
  tests/test_validate_reconciliation.py:173,185 encode exactly that exemption case.
  Open remediation: tasks/335-exempt-templates-from-the-reconciled-versions-ch.md.
  Classified REFERENCE-ONLY: its only reader is a sweeper that should not be reading it.

=== CLASS D — DEAD STOCK (no consumer at all) — 2 files ===

D1  templates/JOURNAL-md-template.md
D2  templates/LESSONS-md-template.md
    Evidence of absence, run at HEAD:
      git grep -n "JOURNAL-md-template\|LESSONS-md-template" -- .
    returns exactly ONE line tree-wide, and it is an immutable audit, not a consumer:
      docs/audits/2026-07-22-technical-hygiene-pre-handoff-inventory.md:14
    No manifest entry. No script, test, hook or command names either file. No protocol, ADR,
    task or living doc cites them. Full-path grep across the whole tracked tree: zero hits.

    PRIOR CLAIM REFUTED. That same audit line asserts:
      "JOURNAL/LESSONS-md-template.md cited by live onboarding intake"
    At HEAD this is false. templates/consumer-onboarding-runbook.md contains exactly one
    occurrence of the word "template" (line 9, about its own proposed home) and cites neither
    file. docs/intake/ cites neither. The 2026-07-22 borderline-kept-with-reason verdict rests
    on a citation that does not exist at HEAD.
    Reported, not repaired — no deletion proposed, per done-contract item 5.

=== CLASS E — ARCHIVED (templates/archive/, handled separately per done-contract item 4) — 4 ===

An archived template is NOT dead stock. Each of the four carries a self-describing in-file
retirement header naming its date and its successor — that header IS the record:

E1  templates/archive/AGENTS-md-template.md
      ":1  <!-- RETIRED 2026-05-19 — superseded by ADR-53. Use templates/CLAUDE-md-template.md
           instead. -->"
E2  templates/archive/HANDOFF_FOLDER_TEMPLATE.md   ":1 ARCHIVED 2026-06-26 ... flat v3.4
      'Stage 3 output structure', superseded by templates/handoff/** (ADR-82)"
E3  templates/archive/HANDOFF_QUESTION_TEMPLATE.md ":1 ARCHIVED 2026-06-26 ... its interview
      function now lives in templates/handoff/v5/SUPPLEMENT.md.tmpl (ADR-82)"
E4  templates/archive/HANDOFF_TEMPLATE.md          ":1 ARCHIVED 2026-06-26 ... flat v2.0/v3.4
      single-file bundle template, superseded by templates/handoff/** (ADR-82)"

TWO OF THE FOUR ARE LOAD-BEARING FOR TESTS — they are fixtures of record, not inert stock:
  tests/test_normalize_headers.py:427 — HANDOFF_QUESTION_TEMPLATE.md is the named real-world
    case of an UNTERMINATED fence; the test cites it to refute a prior assumption.
  tests/test_scan_undeclared_edges.py:319 — HANDOFF_TEMPLATE.md is the named case proving
    templates/archive/ is NOT an immutable prefix and stays edge-eligible.
Deleting either would break the suite. Any retention rule must treat templates/archive/ as
read-protected regardless of citation count.

=== TALLY (47) ===
CARRIER 3 · HUB-LOCAL LIVE 21 (8 rendered + 8 byte-gated + 1 spec + ... see note)
REFERENCE-ONLY 12 · DEAD STOCK 2 · ARCHIVED 4
  Recount, explicit: A=3; B-i=8, B-ii=8, B-iii=1, B-iv=8 -> B=25; C=C1..C11 plus C-EDGE = 12;
  D=2; E=4.  3+25+12+2+4 = 46.  Missing one: templates/handoff/v5/README.md.tmpl — see below,
  it is its own class of one.  3+25+12+2+4+1 = 47.  CONFIRMED.

=== CLASS F — DEFERRED STUB, RETAINED BY RULING — 1 file ===
F1  templates/handoff/v5/README.md.tmpl
    protocols/STANDING_RULINGS.md T-35 (:2638-2657, row CLOSED, expiry open-ended):
      "No script reads the template." The seeder scripts/seed_runbook.py generalizes from the
      already-rendered hub docs/handoffs/README.md.
    protocols/HANDOFF_PROCESS.md:801 — "the render-from-one-template shape is the DEFERRED
      design, not the built one ... it stays a deferred stub until #164 lands".
    Its own line 1 declares "(DEFERRED STUB)".
    NOT dead stock: a ruling exists, names the gap, and retains the file deliberately. This is
    the archetype the retention rule must not eat.

=== DONE-CONTRACT ITEM 2 — THE NAMED RETIREMENT CANDIDATES, LOCATED AND VERDICTED ===

PREMISE PARTIALLY REFUTED — reported, not repaired.

(a) "the workspace templates" — EXIST. Three files, confirmed at HEAD:
      templates/workspace-S.code-workspace, workspace-M, workspace-L.
(b) "the t-shirt-size templates" — DO NOT EXIST AS A SEPARATE SET. Grep for t-shirt/tshirt
    across the tracked tree returns zero template files. In this repo "t-shirt" names two
    OTHER things, neither of which has a template:
      ARCHITECTURE.md:810  model routing (S=Haiku · M=Sonnet · L=Opus)
      PLAYBOOK:805         task-complexity S/M/L sizing, explicitly "bands on a continuum,
                           applied by judgment ... not a tier mandate"
    The brief's "t-shirt-size AND workspace templates" therefore names ONE set of three files
    under two labels, not two sets. No subject is invented to fill the second label.

VERDICT ON THE THREE — RETIREMENT NOT SUPPORTED; CONSOLIDATION IS.
  They are REFERENCE-ONLY and CURRENTLY CITED, with a live bootstrap workflow:
    PLAYBOOK:994  "Templates location: .dev-knowledge/templates/workspace-{S,M,L}.code-workspace"
    PLAYBOOK:997  "1. Copy the template matching repo complexity: cp ... workspace-S..."
  The obvious retirement argument — tier residue, since CLAUDE.md:37 records the repo-tier
  system deprecated 2026-05-23 — HAS ALREADY BEEN DISCHARGED IN PROSE. PLAYBOOK:992 now reads
  "(the S/M/L suffixes are richness levels, not declared tiers)". The deprecation does not
  reach these files.
  What DOES survive is a design objection, operator-raised and still open, recorded at
  docs/audits/2026-05-25-ai-council-universalization-audit-refresh.md (section "workspace
  template tier-residue"): "jeden complex workspace template, scale-adaptive content, NOT
  scale-different templates" — one maximal template with elements selected by complexity.
  That audit routed the item to .dev-knowledge as a standards concern and marked it OUT OF
  SCOPE for that rollout. It has not been picked up since.
  So: three near-duplicate files are a CONSOLIDATION candidate (3 -> 1 + a selection note),
  carrying an operator-stated preference and no ratified decision. It is not a dead-stock
  finding, and this lane rules nothing.

=== DONE-CONTRACT ITEM 3 — RETENTION RULES, ONE PER CLASS (mechanisms, drafted as text) ===

DESIGN CONSTRAINT DISCOVERED, and it kills the obvious rule shape.
  The brief's example mechanism — "a template with no consumer for N days is retired" — is
  UNIMPLEMENTABLE HERE ON AGE. Measured last-commit date for all 47 files: 44 of 47 read
  2026-08-26, with 2026-08-25, -28 and -29 as the only outliers. A tree-wide sweep reset
  every mtime. Age carries no signal in this corpus and any N-days clock reads uniformly
  "fresh" today and uniformly "stale" N days after the next sweep.
  Every rule below therefore keys on CONSUMER RESOLUTION, evaluated at each run, with the
  clock started by the FIRST RUN THAT OBSERVES ZERO CONSUMERS — a fact the organ records —
  never by file mtime.

  Shared machinery all five rules assume (one organ, not five):
    A hub-local validator — working name templates_consumers.py, sibling of the existing
    scripts/funnel_coverage.py and scripts/silent_rule_detector.py, both of which already
    enumerate templates/**/*.{md,tmpl}. It resolves, per tracked file under templates/:
      (1) any deploy/manifest-v*.yaml entry naming it as a source;
      (2) any occurrence of its path or basename under scripts/ tests/ deploy/ .claude/
          plugins/ pyproject.toml .gitattributes, EXCLUDING tests/fixtures/** and EXCLUDING
          the sweeper sites enumerated in the METHOD block above — those are declared,
          by name, in an exclusion constant, so the exclusion is auditable and not implicit;
      (3) any citation from protocols/ docs/decisions/ tasks/ and the root living docs.
    It writes a dated observation row per file: {path, class, consumers, first_seen_zero}.
    first_seen_zero is the ONLY clock any rule below reads.

RULE A — CARRIER
  A file named as a source by ANY deploy/manifest-v*.yaml is NEVER retired by an organ.
  A carrier leaves only by a manifest edit, which is itself a gated change under the release
  contract. Mechanism: the validator FAILS if a manifest source path does not resolve on disk
  — the coupling is enforced in the direction of "the manifest is right, the tree is wrong."
  Retirement path: remove the manifest entry first; the file drops to its next-best class on
  the following run and is governed there. Retiring by hash-orphaning is forbidden — the
  child-methodology-floor pair (A1/A2) is a two-file unit and must move together or not at all.
  Owner: the release gate (deploy/release_lint.py) plus the new validator.

RULE B — HUB-LOCAL LIVE
  Split by HOW the consumer binds, because the two halves fail differently.
  B-mechanical (a generator path constant, or a test that opens the file):
    Never retired by an organ. Deletion is already self-punishing — the suite goes red. The
    validator's job is the INVERSE direction: FAIL when a path constant in scripts/ or a
    template directory rglob resolves to nothing, so a template deleted by hand is caught at
    the gate rather than at the next handoff. Precedent already in the tree:
    tests/test_boundary_headers.py:291 asserts the region count is exactly 8 — cardinality,
    not existence. Generalize that shape: assert the SET, not the count.
  B-declared (a command names the file as material an agent drives, with no code reader —
    the flat v4 eight, B-iv):
    This is the class that rots silently, because nothing goes red. Mechanism: a declared-live
    template carries a REVIEW ANCHOR — the ADR or ruling that retains it (here ADR-83) — and
    the validator FAILS when a file in this class cites no anchor, or cites an anchor whose
    status line has become Superseded. Retirement is then automatic in the only sense that is
    safe: when the retaining ruling dies, the file's retention dies with it and the organ
    surfaces it for triage. No day count. The ruling, not the calendar, is the clock.
  Owner: the new validator, FAIL-class, registered in scripts/audit.py ALL_CHECKS.

RULE C — REFERENCE-ONLY
  The class where a day count is defensible, because the failure mode is a citation quietly
  disappearing from a living doc during an ordinary edit.
  Mechanism, three-stage, and the first stage is the whole point:
    1. On the first run where a REFERENCE-ONLY file resolves ZERO citations, the validator
       WARNs and records first_seen_zero. It does not propose anything. A citation lost to a
       one-commit doc refactor is expected to come back.
    2. If the file still resolves zero citations 90 days after first_seen_zero, the check
       escalates to a CANDIDATE row under the ADR-111 decision funnel — not a deletion, a
       triage obligation, routed to intake per ADR-98. Any new citation resets
       first_seen_zero to null and the clock restarts from scratch.
    3. Retirement, if ratified, is a MOVE to templates/archive/ with a dated in-file header
       naming the date and the superseding surface — the E1-E4 shape, which is already the
       repo's convention. Never a delete.
  Explicit carve-out: a file whose ONLY reader is a sweeper from the METHOD exclusion list
  counts as ZERO consumers, or the C-EDGE case (CONTRIBUTING-md-template, read only by the
  check that [#335] proposes to stop reading it) would be immortalized by its own false WARN.
  Owner: the new validator (WARN-class), escalating into the ADR-111 funnel at day 90.

RULE D — DEAD STOCK
  A file that resolves zero consumers of every kind on its FIRST observation — never cited,
  never carried, never read — has no citation to lose and needs no grace period for one.
  Mechanism: 30 days from first_seen_zero, then straight to a CANDIDATE row under ADR-111,
  with the observation record attached as evidence. The shorter clock is justified by the
  absence of a citation history, not by confidence: the funnel still rules, and the disposal
  is still a MOVE to templates/archive/ under the E1-E4 header convention, never a delete.
  Standing amendment, forced by D1/D2 above: a prose claim in an immutable audit that a file
  "is cited" is NOT a consumer and does not reset the clock. Only a resolved citation at HEAD
  counts. That single provision is what would have caught JOURNAL-md-template.md and
  LESSONS-md-template.md thirteen months earlier.
  Owner: the new validator plus the ADR-111 triage step. The organ proposes; the operator rules.

RULE E — ARCHIVED (templates/archive/)
  NO retirement clock runs in this directory, at any count, for any duration. An archived
  template is the record of a superseded decision; a consumer census that reaches it is
  proposing to delete evidence.
  Mechanism, inverted — the validator PROTECTS rather than proposes:
    1. FAIL if a file under templates/archive/ lacks a first-line RETIRED/ARCHIVED header
       carrying a date and a superseded-by pointer. That header is the artifact's whole value
       and all four current residents already satisfy it.
    2. FAIL if a file under templates/archive/ is DELETED in a diff, with the message naming
       the ADR-83 / ADR-60 archive convention. Note that templates/archive/ is deliberately
       NOT an immutable prefix — tests/test_scan_undeclared_edges.py:319 records that ruling —
       so this rule adds a delete guard only, never an edit guard.
    3. Report, never act on, the fact that E2/E3 are cited by tests as fixtures of record.
       A rule that treated test citations as "activity" would misclassify the other two as
       colder, and coldness is not a retirement criterion in this directory at all.
  Owner: pre-commit, alongside the existing validate-hermetization gate, whose home allowlist
  (scripts/validate_hermetization.py:223) already knows templates/archive/ as a legal home.

RULE F — DEFERRED STUB (class of one today; the class exists because F1 does)
  A template retained by an explicit ruling that ALSO records it has no reader is governed by
  the ruling, not the census. Mechanism: the file must carry a first-line stub marker AND the
  retaining row must be resolvable (STANDING_RULINGS T-35 for F1). Zero consumers is the
  EXPECTED state and raises nothing. The rule fires only on the inverse: if the retaining row
  expires or closes without the stub being either built or archived, the validator raises it
  as a CANDIDATE. Without this class, Rule D would eat templates/handoff/v5/README.md.tmpl on
  its first run, deleting a deliberately-parked design.

=== FINDINGS THE OPERATOR MAY WANT, REPORTED NOT REPAIRED ===
F-1  Two DEAD STOCK files (JOURNAL-md-template.md, LESSONS-md-template.md) were kept in the
     2026-07-22 hygiene inventory on a citation claim that does not resolve at HEAD.
     A borderline-kept-with-reason verdict outlived its reason. This is the single strongest
     argument for Rule D's "prose claim is not a consumer" provision.
F-2  templates/child-methodology-floor.sha256 is a hash sidecar, not a template, living in
     templates/ by adjacency to its subject. Genre anomaly. No action proposed.
F-3  templates/CONTRIBUTING-md-template.md is read by exactly one organ, which produces a
     false WARN on it (ecosystem/index.yaml:78), and an open task [#335] proposes stopping
     that read. Discharging [#335] moves this file to zero consumers and starts Rule C's
     90-day clock — worth knowing BEFORE the exemption lands, not after.
F-4  The 2026-05-25 operator preference "one maximal workspace template, elements selected by
     complexity" was routed to .dev-knowledge as a standards concern, marked out of scope
     there, and never picked up. Three near-duplicate files remain. Consolidation candidate.
F-5  Last-commit dates are uniform at 2026-08-26 across 44 of 47 files. Any future rule,
     organ or audit that reasons about templates/ staleness from mtime will be wrong.

=== CONTRACT COMPLIANCE ===
1. All 47 files classified with per-file evidence.                                  DONE
2. Named candidates located; premise partially refuted and reported, not repaired.  DONE
3. Retention rule per class, drafted as a mechanism (A-F).                          DONE
4. templates/archive/ treated separately, with an inverted protective rule.         DONE
5. No live source deleted. No commit proposed. No ruling made.                      DONE
Escalations under the V-2 budget (a/b/c): NONE. No curated-baseline touch, no
rule-vs-ruling conflict, no fork class without a standing ruling.
Gates: NONE RUN, NONE ASSERTED — read-only by contract, no test leg. python3 was not
invoked; every measurement above is git ls-files, git grep, git log or sed/head.
```