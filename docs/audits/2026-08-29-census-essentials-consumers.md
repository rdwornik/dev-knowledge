The census is complete. Read-only throughout: no file written, no commit, no branch, no gate run.

```
LANE lane-e-000-essentials-census -- ESSENTIALS consumer census
Repo: .dev-knowledge  |  HEAD 66662c7043c18022e6558ad8a8b738fde4dce83d  |  2026-08-29

============================================================
0. RECEIPT GATE
============================================================
git-source-resolves-non-empty: https://github.com/rdwornik/dev-knowledge
  (origin fetch+push; HEAD detached at 66662c7043c18022e6558ad8a8b738fde4dce83d;
   working tree clean, `git status --porcelain` empty; 2701 tracked files)

first-assistant-text-echoed:
  "RECEIPT
   - Total line count of the brief: 101 lines.
   - Final line, verbatim: `- No edits outside this lane's declared footprint.`
   Not truncated. (Ordering slip disclosed: I fired two read-only orientation
   commands before printing this receipt -- the receipt content is unaffected,
   and no write occurred.)
   Proceeding with the brief."

Contract compliance: ZERO tree writes, ZERO commits, ZERO rows. No gate was run and
none is asserted. `python3` (3.11.15) was invoked directly -- twice, read-only: once
to parse ecosystem/index.yaml, once to sha256 the floor template. `uv` was never
invoked. No pytest, no ruff, no audit.py.

============================================================
1. PREMISE CORRECTIONS -- three, reported not ruled
============================================================

P1. THE FREEZE-TIME SIZING DOES NOT REPRODUCE AT HEAD.
  Contract states: 575 files / 50,963,289 B.
  Measured at 66662c7, same command, repo root:
    485 files / 15,375,562 B  (-90 files, -35,587,727 B; the byte figure is 3.3x off)
  The working tree is clean and equals the tracked set, so nothing local inflates it.
  The freeze-time run most plausibly descended a wider root (a sibling-repo parent, or
  a checkout carrying worktrees). Not adjudicated here. The CLOUD routing decision is
  unaffected either way -- 15.4 MB is still ~7x the stated 213,225-token budget.

P2. THE FREEZE-TIME FILTER HAS A BLIND SPOT, AND IT HIDES THE STRONGEST REFERENCE.
  `--include=*.md --include=*.py --include=*.yaml` misses 29 tracked files that
  contain the string. Two of them are load-bearing and neither is a mention:
    templates/child-methodology-floor.md.tmpl   (the deployed methodology floor)
    templates/handoff/02_METHODOLOGY.md.tmpl    (3 machine transclusion directives)
  Plus .claude/workflows/conformance-hub.js, tasks/manifest.json, and 25 historical
  handoff .json/.txt artifacts.
  Unfiltered tracked totals: 514 files / 1,802 reference lines.

P3. "PER FLEET MEMBER" IS NOT DIRECTLY OBSERVABLE FROM THIS CHECKOUT.
  A cloud session clones one repo. Eight of the nine ADR-104 members are not present.
  Every per-member statement in section 5 is therefore derived from hub-held records
  about those members (deployed-versions.yaml, parity-surfaces.yaml, index.yaml,
  ecosystem/<repo>/history/), and each is labelled with its evidence and its date.
  Where the hub holds no record, section 5 says so rather than inferring.

============================================================
2. CLASSIFICATION RULE USED
============================================================
REAL CONSUMER -- behaviour or content depends on protocols/ESSENTIALS.md:
  (a) code that resolves the path, (b) a live instruction requiring it be read or
  uploaded, (c) a gate/contract/register naming it as a governed object, (d) a
  template emitting (a)-(c) into a produced artifact, (e) a test asserting one.
DORMANT -- consumer-shaped, in a surface the live process no longer executes.
MENTION -- names ESSENTIALS with no behaviour depending on it: narrative history,
  a reason-string, a rationale citation, a fixture.

============================================================
3. HEADLINE NUMBERS
============================================================
Tracked files containing the string     : 514   (1,802 lines)
  REAL CONSUMER files                   :  33   (   96 lines)
  DORMANT files                         :   8   (   30 lines)
  MENTION files                         : 473   (1,676 lines)
Naive-grep noise ratio                  : 92.0 % of files are mentions
Live gates that depend on ESSENTIALS
  WITHOUT containing the string         :   6   (section 4.2 -- grep cannot see these)
protocols/ESSENTIALS.md itself contains the string ZERO times (it never self-names),
  so it is absent from all 514.
File under census: 185 lines / 16,308 B, last_reviewed 2026-08-23, 15 H2 sections.

============================================================
4. REAL CONSUMERS -- enumerated with evidence
============================================================

4.1 CODE THAT RESOLVES THE PATH (3 files, 9 lines)

scripts/canonical_docs.py -- THE REGISTRY, and the whole coupling passes through it
  :51  ESSENTIALS = "ESSENTIALS.md"
  :58  ESSENTIALS_PATH = "protocols/ESSENTIALS.md"
  :73  member of CANONICAL_OPTIONAL (and so CANONICAL_ALL) -- casing checked when present
  :82  member of FRESHNESS_FILES
  :88  member of SECTION_HISTORY_DOCS
  :95  member of STRUCTURE_DOCS
  :104 member of CONFORMANCE_V2_SCAN

scripts/canonical_freshness_gate.py -- the deploy-carried pre-commit gate
  :47  DEFAULT_FRESHNESS_FILES = list(_cdocs.FRESHNESS_FILES)   [hub path]
  :49  hardcoded fallback containing "protocols/ESSENTIALS.md"  [consumer standalone copy]
  :124 `if not fpath.exists(): continue` -- so in a consumer that carries no
       ESSENTIALS.md the entry is VACUOUS BY CONSTRUCTION, not an error
  Carried by deploy/carrier_mesh.py (FRESHNESS_GATE_REL), byte-copied to every
  deployed consumer; manifest v1.4.0:771-772 and hook line :209.

.claude/workflows/conformance-hub.js
  :133 scan list literal names protocols/ESSENTIALS.md -- the conformance verifier
       reads the file for verifiable factual claims. Mirrors CONFORMANCE_V2_SCAN;
       agreement asserted by scripts/check_provider_registry.py (docstring :40, seam S11).

4.2 TRANSITIVE CONSUMERS -- 6 live gates, none contains the string
  This is the census's load-bearing structural finding: a grep both over-counts
  (92 % mentions) and under-counts (these six are invisible to it).
    scripts/audit.py:468-470,754  -- _FRESHNESS_FILES = DEFAULT + hub-only extras;
                                     drives audit check #10 canonical_freshness
    scripts/validate_doc_rot.py:164,396        -- section-history accretion scan
    scripts/validate_doc_structure.py:77,318   -- structural-shape scan
    scripts/audit_checks/check_canonical_md_visibility.py:30,43 -- casing check
    deploy/release_lint.py:159-161,412         -- C7 mirror: manifest doc_shapes vs
                                                  DEFAULT_FRESHNESS_FILES, fails loud
    scripts/check_provider_registry.py:40      -- S11 agreement vs CONFORMANCE_V2_SCAN

4.3 TESTS ASSERTING THE BINDING (1 file, 2 lines real)
  tests/test_audit.py:1163-1165 -- asserts "protocols/ESSENTIALS.md" in aud._FRESHNESS_FILES
  tests/test_audit.py:323       -- asserts ESSENTIALS ABSENCE must not fail the ADR-38
                                   baseline (the optional-at-consumer contract)
  tests/test_canonical_docs.py  -- transitive: asserts the gate fallback equals the
                                   registry (contains no ESSENTIALS string)

4.4 DEPLOY CONTRACT (5 files, 5 lines)
  deploy/manifest-v1.4.0.yaml:836 -- doc_shapes: protocols/ESSENTIALS.md
                                     {spine: [], freshness_gated: true}   [CURRENT]
  identical row at v1.3.1:704, v1.3.0:695, v1.2.0:630, v1.1.0:415
  Two of those older rows are STILL LIVE, because two consumers are pinned below head:
     ai-council    -> v1.3.1 (deployed 2026-07-11)
     corp-monorepo -> v1.2.0 (deployed 2026-07-07, held by ADR-102 ruling)
  DECISIVE NEGATIVE, verified: ESSENTIALS.md appears NOWHERE in the manifest
  `carriers:` block (107-386). No carrier copies protocols/ESSENTIALS.md into any
  consumer. It is a governed object of the contract, never a shipped payload.

4.5 LIVE BOOT / SESSION INSTRUCTIONS (10 files, 27 lines)
  CLAUDE.md:14,23,27,102,125,86,211 -- §1 item 2 is the load-bearing line:
    "read at the hub .dev-knowledge/protocols/ set; hub-pointer, never copied
     into a consumer"
  templates/claude-regions/first-read.md:4,8        -- the single-sourced region BODY
    that CLAUDE.md §1 is byte-identical to; the fleet-wide source of that instruction
  templates/claude-regions/session-start-protocol.md:11
  templates/claude-regions/critical-rules-consistency.md:1
  templates/claude-regions/antipatterns-universal.md:5
  templates/claude-regions/conventions-output-formatting.md:1
  templates/CLAUDE-md-template.md:19 -- the onboarding template a new repo is cut from
  templates/child-methodology-floor.md.tmpl:41 -- the METHODOLOGY FLOOR pointer,
    deployed as .claude/CLAUDE-FLOOR.md and hash-guarded. VERIFIED THIS SESSION:
    sha256 of the template == templates/child-methodology-floor.sha256 ==
    4d268f329a7edc8dc95a1c8fded9bdf8244ad8de60be69bf8e250a9b15a8111f == the hash
    recorded in the audit history of all four floor-carrying consumers. Its own
    wording disclaims dependency: "Depth only; this floor is self-sufficient for a
    normal session."
  protocols/SESSION_SETUP.md:34,42,52,58,65,71,76,168 -- the densest live-instruction
    site: three browser-session scale profiles, each opening "upload ESSENTIALS.md",
    plus :65 "PLAYBOOK.md is NOT needed here -- ESSENTIALS covers daily work"
  protocols/PLAYBOOK.md:1389 -- "Upload ESSENTIALS.md (always)" (browser resumption)

4.6 GOVERNANCE BINDINGS -- content-coupled, live (9 files, 44 lines)
  protocols/PLAYBOOK.md (20 lines) -- RECIPROCAL, the strongest doc coupling. CLAUDE.md
    rule 6 binds ESSENTIALS to summarize PLAYBOOK without copying, and PLAYBOOK carries
    five "moved from ESSENTIALS 2026-07-05 [#258] -- ESSENTIALS keeps the pointer"
    markers at :542, :694, :3286, :4116, :4694, plus the roster rows :1075, :1105,
    :1113, :1260, :327
  protocols/STANDING_RULINGS.md (7 lines) -- :2617,:2633 make protocols/ESSENTIALS.md:86
    the EVIDENCE LOCATOR for RULING-W (resolved live this session: line 86 is the
    hub-to-consumer write ruling, present and correct); :2740,:2868 classify ESSENTIALS
    as human-facing functional documentation; :2514-2518 record two stale citations
  protocols/HANDOFF_PROCESS.md:85,224,828 -- v6 can demand an EXACT-LINE QUOTE from a
    named ESSENTIALS section as a proof artifact ("a paraphrase from a summary is not
    byte-identical")
  .claude/commands/handoff-verify.md:95 -- the same requirement in the executed command
  .claude/commands/handoff.md:80 -- bundle carries methodology as pointers to
    PLAYBOOK / ESSENTIALS / CLAUDE.md, never as copies
  .claude/commands/changelog-review.md:23 -- cites ESSENTIALS "Architect routing"
  protocols/DEFINITION_OF_DONE.md:195 -- backstops ESSENTIALS "Ending a Session"
  VISION.md:100-102,186 -- VISION explicitly DEFERS to ESSENTIALS "How Claude thinks"
    for principles, stating "no duplication". A genuine content dependency.
  ARCHITECTURE.md:284,323,925,1007,1010
  protocols/ENVIRONMENT.md:188,273 ; protocols/README.md:16 ; protocols/AGENT_FRAMEWORK.md:11
  protocols/AI_COUNCIL_PROCESS.md:325,327,413 -- makes ESSENTIALS the OWNER rule for
    repo artifacts (a real binding whose anchor is stale -- see 6.1)
  ecosystem/disposition-register.yaml:97,131,134 -- a governed register entry keyed on
    ESSENTIALS: the ADR-88 undeclared-prose-edge "protocols/ESSENTIALS.md ->
    handoff-process", dispositioned rather than removed, with the reason given as
    ESSENTIALS being canonical_freshness-gated

4.7 BOUND OBLIGATIONS -- open work whose done-condition touches ESSENTIALS
  (11 files, 12 lines; a distinct class -- an obligation, not a consumer)
    tasks/231 consumer->hub feedback report
    tasks/241 undeclared-edge groom
    tasks/263 protocols/edge-map reconciliation residuals
    tasks/285 extend hub freshness gating to PLAYBOOK
    tasks/354 ADR-36/41/101 -> PLAYBOOK/ESSENTIALS co-change checker (proposes a
              MECHANICAL edge that does not exist today)
    tasks/356 RULING-W legible in PLAYBOOK/ESSENTIALS but with no mechanism
    tasks/390 records a LIVE CONTRADICTION: ADR-87 item 2 assigns model/effort to CC;
              PLAYBOOK §2 + ESSENTIALS assign effort elsewhere
    tasks/528, tasks/547, tasks/606
    tasks/manifest.json (generated mirror), BACKLOG.md:331,373 (generated)

============================================================
5. GROUPED BY THE NINE ADR-104 FLEET MEMBERS
============================================================
Fleet declaration (ADR-104:15, amended 2026-08-03 with a machine-locatable anchor):
.dev-knowledge, ai-council, corp-monorepo, corp-ops, corp-sca-time-automation,
demo-prep, life-architect, terminal-setup, win-tooling.
Roles from ecosystem/parity-surfaces.yaml:112-159.

--- .dev-knowledge (role: hub) -----------------------------------------------
  Holds the file. Every one of the 33 REAL CONSUMER files in section 4 lives here.
  This is the only member with observable, first-hand evidence.
  Floor: none (floor_integrity n/a -- the hub is the floor SOURCE, not a carrier).
  Deployed corpus version: null (the hub IS the source).
  Verdict: SOLE REAL CONSUMER SURFACE, 33 files / 96 lines.

--- ai-council (role: consumer, corpus v1.3.1, deployed 2026-07-11) -----------
  Real consumption paths, all inherited, none first-hand-verifiable from here:
   1. .claude/CLAUDE-FLOOR.md, sha256 4d268f32... == the hub floor template ->
      carries the ESSENTIALS depth-pointer at floor line 41. VERIFIED by hash match
      (ecosystem/ai-council/history/2026-07-31.md:18).
   2. scripts/canonical_freshness_gate.py (mesh carrier) -> its list names
      protocols/ESSENTIALS.md; the repo carries no ESSENTIALS.md, so the entry is
      vacuous by the :124 exists-check.
   3. manifest v1.3.1:704 doc_shapes row -- freshness_gated: true, same vacuity.
   4. CLAUDE.md present (33,406 chars) and carries Form-A markers (parity row
      claude-md-form-a-markers, MUST fleet-wide) -- so it is CONTRACTED to carry the
      first-read region naming ESSENTIALS. NOT VERIFIED: the probe is presence-only
      (`file_contains "<!-- methodology:start"`), per-region fidelity is owned by
      scripts/boundary_report.py which is Layer-2-scoped to .dev-knowledge paths only.
  Verdict: REAL CONSUMER by inheritance -- 1 verified surface (floor hash),
           3 contracted-but-unverified.

--- corp-monorepo (role: consumer, corpus v1.2.0, deployed 2026-07-07) --------
  Same four paths as ai-council; floor hash matches (history/2026-07-31.md:18).
  Manifest row is v1.2.0:630. CLAUDE.md 22,708 chars.
  Version held at 1.2.0 by ADR-102 / #336 ruling -- not drift.
  Verdict: REAL CONSUMER by inheritance -- 1 verified, 3 contracted-but-unverified.

--- corp-ops (role: pre-deploy) ----------------------------------------------
  No floor (floor_integrity n/a). No corpus deployed (deployed_methodology_version
  null). CLAUDE.md present, 6,818 chars, Form-A markers contracted.
  Verdict: NO REAL CONSUMPTION PATH beyond a contracted-but-unverified CLAUDE.md
           region. The hub holds no evidence that any ESSENTIALS-bearing surface
           reaches this repo.

--- corp-sca-time-automation (role: pre-deploy) ------------------------------
  Floor PRESENT and hash-matching (history/2026-07-31.md:18) despite no corpus
  deploy -- so the ESSENTIALS depth-pointer DOES reach this repo.
  No corpus deployed, so no mesh gate, no doc_shapes row.
  CLAUDE.md 6,920 chars.
  Verdict: REAL CONSUMER by ONE verified surface only (the floor pointer).

--- win-tooling (role: pre-deploy, HELD despite corpus v1.4.0 landed 2026-08-29) --
  The one member whose record moved this month. Floor PRESENT, hash-matching
  (ecosystem/win-tooling/history/2026-08-29.md:23). Corpus v1.4.0 deployed
  (deployed-versions.yaml). CLAUDE.md 6,885 chars.
  Role deliberately HELD at pre-deploy: parity-surfaces.yaml:135-159 records that
  fleet_parity against the deployed tree still reports ELEVEN MUST-absent surfaces.
  Verdict: REAL CONSUMER by inheritance -- floor verified, mesh gate + doc_shapes
           row v1.4.0:836 landed but the parity role is not flipped.

--- demo-prep (role: pre-deploy) ---------------------------------------------
  No ecosystem/ directory, no history file, no deployed-versions.yaml key, never
  audited. NO EVIDENCE EITHER WAY. Not classifiable from this checkout.

--- life-architect (role: pre-deploy) ----------------------------------------
  Same: no ecosystem/ directory, no history, no deployed-versions key.
  NO EVIDENCE EITHER WAY. Not classifiable from this checkout.

--- terminal-setup (role: pre-deploy) ----------------------------------------
  Admitted to deployed-versions.yaml 2026-08-29 ([#604]) with ALL THREE FIELDS NULL --
  the key is a deploy-tool precondition, explicitly not a claim that anything landed.
  The file's own comment records it as methodology-unonboarded: 2 commits, no
  VISION.md, no CLAUDE.md, no deploy record.
  Verdict: NO CONSUMPTION PATH. With no CLAUDE.md there is not even a contracted one.

FLEET ROLL-UP
  Members with a VERIFIED ESSENTIALS-bearing surface (floor hash match): 4
    ai-council, corp-monorepo, corp-sca-time-automation, win-tooling
  Members holding the file itself: 1  (.dev-knowledge)
  Members with a contracted-but-unverifiable CLAUDE.md region: 5
    ai-council, corp-monorepo, corp-ops, corp-sca-time-automation, win-tooling
  Members with NO consumption path: 1  (terminal-setup)
  Members with NO EVIDENCE AT ALL: 2  (demo-prep, life-architect)
  Members receiving a COPY of protocols/ESSENTIALS.md: 0 -- confirmed by the empty
    carriers-block search. The file is hub-resident by design; every consumer path
    is a POINTER or a VACUOUS GATE ENTRY.

============================================================
6. DORMANT -- consumer-shaped, not live (8 files, 30 lines)
============================================================
templates/handoff/02_METHODOLOGY.md.tmpl:18,47,106
  Three machine transclusion directives -- {{PULL: ESSENTIALS#How Claude thinks}},
  {{PULL: ESSENTIALS#Architect routing for technical proposals}},
  {{PULL: ESSENTIALS#Starting a Session}}. Strongest-shaped reference in the tree,
  and NOT EXECUTED:
    - the {{PULL}} grammar is defined ONLY in protocols/archive/HANDOFF_PROCESS_v4.4.md:221
    - HANDOFF_PROCESS v6.3.0 emits from templates/handoff/v5|epic|functional
    - no script implements PULL: `grep -rn PULL scripts/*.py` returns nothing, and
      scripts/gen_handoff.py contains no "templates/handoff" reference
    - one of the three anchors would not resolve anyway: "Architect routing for
      technical proposals" is a bold bullet at ESSENTIALS:54, not a heading
templates/archive/HANDOFF_FOLDER_TEMPLATE.md (12), HANDOFF_QUESTION_TEMPLATE.md (3),
  HANDOFF_TEMPLATE.md (1), AGENTS-md-template.md (1)
protocols/archive/HANDOFF_PROCESS_v4.4.md (2), HANDOFF_PROCESS_v3.4.md (1)
deploy/manifest-v1.1.0.yaml, v1.3.0.yaml -- superseded, no consumer pinned to them
  (v1.2.0 and v1.3.1 are NOT dormant: corp-monorepo and ai-council are pinned there)

6.1 BROKEN LOCATORS FOUND WHILE RESOLVING (each opened, not assumed)
  RESOLVES:  ESSENTIALS:86 (RULING-W) · "Ending a Session" (:124) · "Feedback Loop"
    (:140) · "How Claude thinks" (:14) · "Starting a Session" (:71) ·
    "Architect -> operator channel-discipline" (:51) · "Architect routing for
    technical proposals" (:54)
  STALE:  protocols/PLAYBOOK.md:653 cites "ESSENTIALS line 25" for the English-only
    prompt rule -- line 25 is the string "**Does NOT:**"
  STALE:  protocols/AI_COUNCIL_PROCESS.md:325,413 cite "ESSENTIALS § Repo artifacts"
    -- no such heading exists in the 15-heading set
  Both are already recorded at protocols/STANDING_RULINGS.md:2514-2518 as
  accepted-by-relocation. Reported as verification, not as a new finding.

============================================================
7. MENTIONS -- 473 files, 1,676 lines (92.0 % of files)
============================================================
docs/handoffs   259 files / 719 lines -- immutable session bundles. 37 of the 234 .md
  files carry an instruction-shaped reference ("upload/read/attach ESSENTIALS"), but
  each addresses a session that has ended. The ACTIVE bundle (newest by git add-date,
  docs/handoffs/2026-08-28-dev-knowledge-architect, epoch 1787918140) carries ESSENTIALS
  only twice, both narrative (RESIDUAL.md:127, PASTE_THIS.md:185). There is currently
  ZERO live handoff-bundle instruction to read ESSENTIALS -- under v6 that instruction
  lives in CLAUDE.md §1 instead.
  Includes 25 pre-v4 .json/.txt artifacts the freeze-time filter never saw.
docs/audits     162 files / 619 lines -- immutable findings records; 16 instruction-shaped
JOURNAL.md        1 file  / 218 lines -- the single largest mention concentration in
  the repo; append-only session narration
LESSONS.md        1 file  /  19 lines -- lesson records (2026-03-29 .. 2026-07-28)
docs/decisions   22 files /  48 lines -- ADR rationale. ADR-29/33/35/39/42/43/45/49/51/
  53/57/59/60/62/72/83/87/89/106/115 + README + archived ADR-52. None makes ESSENTIALS
  an executable object; ADR-53 and ADR-115 are the two that shape its instruction role.
docs/intake       6 files /  15 lines ; docs/archive 3 files / 7 lines
ecosystem         5 files /   6 lines -- prose reason/comment strings only:
  doc-code-edge.yaml:17, parity-surfaces.yaml:611, provider-registry.yaml:40,
  index.yaml:123 (generated), .dev-knowledge/history/2026-07-31.md
  (disposition-register.yaml is NOT here -- it is a real binding, section 4.6)
scripts/assemble_paste.py:70 + tests/test_assemble_paste.py:532 -- a triage PROMPT
  STRING listing ESSENTIALS as a durable-home option; no code reads the file
tests/test_coherence_integration.py:60 -- fixture text
logs/TOKEN-LOG.md:1 line -- a reads-list inside one token record
BACKLOG.md:2 lines -- generated from tasks/

============================================================
8. OBSERVATIONS -- flagged, NOT ruled (this is not a ruling lane)
============================================================
O1. AGENTS.md, the ADR-115 portable instruction layer, contains ZERO references to
    ESSENTIALS. So does codex/AGENTS.md. The Claude-runtime boot instruction points
    at ESSENTIALS; the provider-portable one does not. Stated as measured fact.
O2. ecosystem/parity-surfaces.yaml:602-611 tiers protocols/ as SHOULD for a CONSUMER,
    with the reason naming "ESSENTIALS/PLAYBOOK". templates/claude-regions/first-read.md:4
    says ESSENTIALS is "never copied into a consumer". Both are live text.
O3. Every consumer running the mesh freshness gate carries protocols/ESSENTIALS.md in
    its gate list and carries no such file, so the entry passes vacuously
    (canonical_freshness_gate.py:124). The same is true of each doc_shapes row.
O4. ecosystem/index.yaml is stamped 2026-08-05 and covers 6 members; win-tooling's
    2026-08-29 history is newer than anything the index knows. Per-member statements
    in section 5 use the newest per-repo history file, not the index, where they differ.
O5. tasks/354 proposes the ADR -> PLAYBOOK/ESSENTIALS co-change checker; no such
    mechanical edge exists today. The only mechanical bindings ESSENTIALS has are the
    five canonical_docs.py set memberships and the conformance-hub scan list.
O6. The 33/473 split is the answer to the contract's question: of a naive 575 (485
    reproduced, 514 unfiltered), 33 files are real, and 6 more real dependencies are
    invisible to any grep because they reach the file through canonical_docs.py.

ESSENTIALS' fate is the architect's call. This lane makes no recommendation.
```

Three things worth your attention before the architect reads it: the freeze-time sizing does not reproduce at HEAD (485 files / 15.4 MB, not 575 / 50.9 MB), the freeze-time filter missed the two `.tmpl` files that carry the strongest-shaped references, and eight of the nine fleet members are not present in a cloud checkout — every per-member line is hub-held record, labelled with its evidence and date.