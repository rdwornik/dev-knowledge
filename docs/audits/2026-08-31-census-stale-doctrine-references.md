> **PROVENANCE - harvested cloud artifact, body VERBATIM below this header.**
> Lane `batch-e-a3-stale-doctrine-reference-census` | receipt id `cse_01BxXjpYNAzow4Qj4KDY3mXN` | dispatched 2026-08-31, harvested 2026-08-31 by
> `Save-CloudSessionReport` (the `Harvest-Cloud` alias). Batch E tier (A); the frozen contract is
> `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a3-stale-doctrine-reference-census.md`.
> Selection rule: the LONGEST assistant text, not the last - text #2 of 11 across 6 pages.
> Bytes written unchanged: **31,691**.
> Harvester DEVIATION, recorded not repaired: the report contains no markdown heading at all; bytes UNCHANGED.
> Nothing below this line was edited, reflowed or trimmed.
>
> **Consumed by:** DC-23 (`lane-b-2-essentials-and-claude-md`).
>
> **This lane was READ-ONLY by contract** - zero tree writes, zero commits, zero rows, no gate
> run and none asserted.

---

The census is complete. Read-only throughout: zero tree writes, zero commits, zero rows, no branch, no gate.

```
LANE batch-e-a3-stale-doctrine-reference-census -- stale doctrine-reference census
Repo: .dev-knowledge | HEAD ec8731a9b2fdcc7fffee59bb0743a8b467f65c0b | 2026-08-31

============================================================
0. RECEIPT GATE
============================================================
git-source-resolves-non-empty: https://github.com/rdwornik/dev-knowledge
  (origin fetch+push; HEAD detached at ec8731a, == origin/main;
   `git status --porcelain` empty; 2761 tracked files)

first-assistant-text-echoed:
  "RECEIPT
   - Total line count of brief: 116 lines
   - Final line verbatim: `- No edits outside this lane's declared footprint.
     Prose in English; hyphen-only names.`
   Not truncated. Proceeding to execute."

Contract compliance: ZERO tree writes, ZERO commits, ZERO rows, no branch created.
NO GATE WAS RUN AND NONE IS ASSERTED (read-only by contract; no test leg).
`uv` was never invoked. `python3` (3.11.15) was resolved for version only, never
executed against repo code. One scratch file was written OUTSIDE the repo tree
(/tmp/live53.txt) for a line tally; the tree is byte-identical to HEAD.

============================================================
1. PREMISE CORRECTIONS -- three, REPORTED not ruled (Q10 PAUSE)
============================================================

P1. S1 RETIRED-NAME IS AN EMPTY CLASS. THE PREMISE IS REFUTED.
  The contract defines S1 as citing "`Universal Protocols` (the pre-`PLAYBOOK` name)".
  Measured at HEAD:
    git grep -l "Universal Protocols"          -> 0 files
    git grep -l -iE "universal[ _-]protocols?" -> 26 files
  All 26 hits are the DESCRIPTIVE ROLE PHRASE ("universal protocols", lowercase or
  sentence-case), never a filename. And the name never existed as one:
    git log --all --diff-filter=A --name-only | grep -i universal
  returns 14 paths, none a protocol file; no path matching PROTOCOLS ever existed
  other than the 14 live `protocols/*.md`. `protocols/PLAYBOOK.md` has no rename
  predecessor named "Universal Protocols".
  The phrase is CURRENT doctrine, not retired: CLAUDE.md:29 and its region source
  templates/claude-regions/first-read.md:8 both read "`PLAYBOOK.md` ... is the
  universal-protocols **reference**".
  => S1 = 0 hits. Not repaired, not re-scoped, no subject invented.

P2. S2's TRIGGER CONDITION IS FALSE AS WRITTEN.
  S2 is defined as citing ESSENTIALS as a boot-time read or as "summarizes PLAYBOOK"
  "when the live contract (CLAUDE.md §1, §5 rule 6) HAS MOVED". It has not moved:
    CLAUDE.md §1 item 2  -- ESSENTIALS.md IS boot-time read #2, verbatim.
    CLAUDE.md §5 rule 6  -- "ESSENTIALS summarizes PLAYBOOK, not copies it", verbatim.
  So "ESSENTIALS is a boot read" and "ESSENTIALS summarizes PLAYBOOK" are CORRECT
  statements at HEAD and are NOT defects.
  The clause of the live contract that HAS moved is a different one, added in the same
  §1 line: "hub-pointer, **never copied into a consumer**", plus ADR-79 D2
  (5-file upload -> ONE consolidated bundle) and the v4->v5/v6 flip
  (HANDOFF_PROCESS.md:461: "Methodology extracts copied into `02_METHODOLOGY`"
  -> "methodology referenced by pointer").
  I census S2 against THAT axis -- COPY-vs-POINTER and PER-FILE-UPLOAD-vs-BUNDLE --
  and report it as a re-aimed class, not a silently redefined one.

P3. THE FREEZE-TIME SUBSTRATE SIZING DOES NOT REPRODUCE, AND ONE HALF IS PHANTOM.
  Contract: "519 tracked files contain `Universal Protocols` or `ESSENTIALS`".
  Measured: 519 files contain ESSENTIALS; 0 contain "Universal Protocols". The union
  is 519 because one disjunct contributes nothing. The number is right, its
  composition is not.
  Corpus: 2,761 files -- matches the contract exactly.
  (Cross-check: the batch-D census at 66662c7 measured 514 files / 2,701 tracked.
   +5 hit files, +60 tracked files since. Consistent drift, no anomaly.)

============================================================
2. HEADLINE NUMBERS
============================================================
Tracked files containing "ESSENTIALS"        : 519   (1,871 lines)
  S4 HISTORICAL-CORRECT (immutable/archived) :  466  (1,751 lines)  <- NOT defects
  LIVE / MUTABLE SURFACE                     :   53  (  120 lines)
Files containing "Universal Protocols"       :    0
protocols/ESSENTIALS.md never self-names, so it is absent from all 519.
Subject file at HEAD: 185 lines / 16,308 B / 15 H2 sections /
  last_reviewed 2026-08-23 / status active.

REPAIR SURFACE (S1+S2+S3, live only)         :   11 files,  17 lines
  S1 RETIRED-NAME    :  0 files   (class empty -- see P1)
  S2 ROLE-DRIFT      :  4 files,  10 lines
  S3 DEAD-LOCATOR    :  8 files,  11 lines   (1 file carries both classes)
Gate-coupled / machine-read subset of that   :   4 files,   8 lines  (§3)
Naive-grep noise ratio                       :  97.9 % of files are S4 or clean

============================================================
3. MACHINE-READ SURFACES -- FLAGGED FIRST AND SEPARATELY
   (done-contract item 3: gate-coupled defects, not prose defects)
============================================================

3A. GATE-COUPLED DEFECTS -- 4 files, 8 lines

M1. templates/handoff/02_METHODOLOGY.md.tmpl  -- S2 (5 lines) + S3 (1 of them)
    CLASS: template that EMITS a copy of ESSENTIALS content into a produced artifact.
    :2   "Pulled FROM source (PLAYBOOK + ESSENTIALS) at handoff time"
    :12  "`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md` in `.dev-knowledge`"
    :18  {{PULL: ESSENTIALS#How Claude thinks}}
    :47  {{PULL: ESSENTIALS#Architect routing for technical proposals}}   <- ALSO S3
    :106 {{PULL: ESSENTIALS#Starting a Session}}
    WHY STALE: HANDOFF_PROCESS.md:461 records the v4->v5 supersession verbatim --
      "Methodology extracts copied into `02_METHODOLOGY` | methodology referenced by
      pointer; enforced mechanically". Live process is v6.3.0. The active bundle
      (docs/handoffs/2026-08-31-dev-knowledge-architect/) holds 6 files -- FUNNEL_HEALTH,
      HANDOFF_BOOT, PASTE_THIS, PROBES, RESIDUAL, SUPPLEMENT -- and NO 02_METHODOLOGY.
      scripts/audit_checks/check_handoff_bundle_structure.py docstring: the 8-file
      shape "governs only the HISTORICAL v4 bundles".
      The template also contradicts CLAUDE.md §1's "hub-pointer, never copied".
    S3 LEG (resolved, not claimed): `#Architect routing for technical proposals` matches
      NO heading in ESSENTIALS.md. The 15 H2s are lines 14/33/46/60/71/80/92/103/117/
      124/140/151/158/171/178. The string exists ONLY as a bold BULLET at
      ESSENTIALS.md:54 inside `## Architect disciplines`. The sibling anchors
      `#How Claude thinks` (:14) and `#Starting a Session` (:71) DO resolve to headings,
      so the grammar is heading-shaped and this one anchor is dead.
    HONEST LIMIT: `git grep -ln "PULL:"` outside docs/ returns only
      protocols/archive/HANDOFF_PROCESS_v4.4.md and the 3 templates -- NO CODE RESOLVES
      `{{PULL:`. The directive is hand-executed, so this is dormant-by-construction,
      not a firing gate. It is still the strongest machine-shaped reference and the
      prior census named it load-bearing.
    WHAT WOULD HAVE TO CHANGE: retire the template with the v4 bundle shape, or
      re-point :47 to `ESSENTIALS#Architect disciplines`. Fate is DC-2/DC-3's, not mine.

M2. templates/CLAUDE-md-template.md  -- S2 (1 line) + superseded-doctrine header
    :19  "**For universal rules:** read the hub methodology protocols `ESSENTIALS.md`
          and `PLAYBOOK.md`"
    WHY STALE: this template SEEDS every consumer's CLAUDE.md, and at §1 it imports the
      hub-owned region `first-read` (`<!-- SYNC verbatim from
      templates/claude-regions/first-read.md -- owner=hub -->`). That region's own text
      (first-read.md:8) says PLAYBOOK "is the universal-protocols **reference**, NOT a
      boot-time read". Line 19 sits in the header ABOVE the region markers, so
      region-sync can never reconcile it: the template instructs a boot-time PLAYBOOK
      read that the region it carries forbids.
    ADJACENT, SAME FILE, SAME CLASS (reported, outside the ESSENTIALS subject):
      :17  "Single canonical agent-instruction file (<=200 lines). Per ADR-53."
           -- superseded twice: ADR-115 makes AGENTS.md the portable layer (so CLAUDE.md
           is no longer "the single" file), and the live bound is BYTES (<=24,576 B,
           tests/test_claude_md_byte_cap.py), stated by CLAUDE.md's own preamble.
      :9   `<!-- version: 2.3 -- 2026-07-12 -->` against CLAUDE.md v2.69 (2026-08-29).
    CONSUMERS: scripts/boundary_headers.py, scripts/preflight_contract.py,
      scripts/validate_hermetization.py + 3 tests read the region set.

M3. protocols/PLAYBOOK.md:1114  -- S3, a RESTATED ROSTER that no longer resolves
    TEXT: "The living docs `VISION / ARCHITECTURE / CLAUDE / CONTRIBUTING / ESSENTIALS`
           carry a `last_reviewed` frontmatter date."
    LIVE SET (computed): scripts/audit.py:470
      `_FRESHNESS_FILES = _cfg.DEFAULT_FRESHNESS_FILES + _HUB_ONLY_FRESHNESS_FILES`
      = canonical_docs.py:88-90 FRESHNESS_FILES (VISION, ARCHITECTURE, CLAUDE,
        CONTRIBUTING, docs/handoffs/README.md, protocols/ESSENTIALS.md)
      + audit.py:468-469 (protocols/SESSION_SETUP.md, protocols/AI_COUNCIL_PROCESS.md,
        protocols/DEFINITION_OF_DONE.md)
      = NINE files. PLAYBOOK names FIVE. Four missing.
    WHY IT IS A RULING VIOLATION, not a nit: STANDING_RULINGS.md:2867-2878 (W2,
      operator direction 2026-08-25) rules that PLAYBOOK and ESSENTIALS are human-facing
      functional documentation and "must stop being edited as though they were" competing
      descriptions of the machine layer -- "the same rule `CLAUDE.md` section 4 already
      states as M2 -- never restate a count or roster, cite the surface that computes it".
      CLAUDE.md §4 complies exactly ("computed, not restated here --
      `canonical_docs.py::FRESHNESS_FILES` + `audit.py::_HUB_ONLY_FRESHNESS_FILES`").
      PLAYBOOK:1114 is the same doctrine restated wrong -- an intra-doctrine contradiction
      between two files of the same genre.
    WHAT WOULD HAVE TO CHANGE: replace the five-name list with the citation CLAUDE.md
      already uses.

M4. .claude/commands/changelog-review.md:23  -- S3 (soft)
    TEXT: `ESSENTIALS "Architect routing"`
    RESOLVES TO: a BULLET at ESSENTIALS.md:54, no heading of that name. Same anchor
    class as M1's dead PULL and as ARCHITECTURE.md:323. Command frontmatter is
    machine-enumerated into .claude/generated/commands-repo.md, so the file is
    gate-adjacent even though this line is prose inside it.

3B. MACHINE-READ SURFACES INSPECTED AND FOUND CLEAN -- reported so DC-2 knows the
    full coupling, because none of these is a defect TODAY and every one BREAKS if
    ESSENTIALS is dissolved:

  scripts/canonical_docs.py -- THE REGISTRY; all coupling passes through it
    :61  ESSENTIALS = "ESSENTIALS.md"          :68  ESSENTIALS_PATH = "protocols/ESSENTIALS.md"
    :83  CANONICAL_OPTIONAL (=> CANONICAL_ALL) :92  FRESHNESS_FILES
    :98  SECTION_HISTORY_DOCS                  :105 STRUCTURE_DOCS
    :114 CONFORMANCE_V2_SCAN
  scripts/canonical_freshness_gate.py:50 -- hardcoded consumer-standalone fallback list
  scripts/assemble_paste.py:70 -- warn string "durable home: ADR / PLAYBOOK / ESSENTIALS
    one-liner / carrier?"; asserted by tests/test_assemble_paste.py:532
  .claude/workflows/conformance-hub.js:133 -- V2 scan-list literal; agreement with
    CONFORMANCE_V2_SCAN asserted by check_provider_registry.py seam S11
  tests/test_audit.py:323, :1163, :1165 -- :1165 asserts
    `"protocols/ESSENTIALS.md" in aud._FRESHNESS_FILES`
  tests/test_coherence_integration.py:60 -- fixture prose
  deploy/manifest-v1.1.0/1.2.0/1.3.0/1.3.1/1.4.0 -- `protocols/ESSENTIALS.md:` under
    `doc_shapes:` (v1.4.0:837-839), NOT under `carriers:`. It declares
    `spine: [] / freshness_gated: true` for a consumer that HAS the file. This is
    CONSISTENT with "never copied into a consumer" -- vacuous by construction, not
    contradictory. Explicitly NOT flagged S2.
  ecosystem/disposition-register.yaml:97,131,134 · index.yaml:123 ·
    doc-code-edge.yaml:17 · parity-surfaces.yaml:635 · provider-registry.yaml:40 --
    all live registers naming a path that resolves. Clean.
  templates/claude-regions/{first-read,critical-rules-consistency,antipatterns-universal,
    session-start-protocol,conventions-output-formatting}.md -- the region SOURCES
    that single-source CLAUDE.md §1/§5/§6/§10. All agree with CLAUDE.md at HEAD. Clean.
  templates/child-methodology-floor.md.tmpl:41 -- "The methodology hub (`.dev-knowledge`)
    -- full protocols (PLAYBOOK / ESSENTIALS). Depth only". Pointer, not copy. Clean.
  tasks/manifest.json:1226,:1352 -- generated mirror of tasks/*.md prose. Derived, clean.

============================================================
4. THE REPAIR SURFACE -- S1 + S2 + S3, per file, with the text that must change
============================================================

--- S1 RETIRED-NAME: EMPTY (0 files). See P1. ---

--- S2 ROLE-DRIFT: 4 files, 10 lines ---
  Axis (per P2): cites ESSENTIALS as CONTENT TO COPY or as a PER-FILE BROWSER UPLOAD,
  against CLAUDE.md §1 "hub-pointer, never copied into a consumer", ADR-79 Decision 2
  (one consolidated bundle), and HANDOFF_PROCESS v6 (thin boot + residual + probes).

S2-1. protocols/SESSION_SETUP.md -- 5 lines. THE CONCENTRATION.
      last_reviewed: 2026-08-28 · status: active · reconciled_with: handoff-process@6.3.0
      AND it is freshness-GATED (audit.py:468, _HUB_ONLY_FRESHNESS_FILES).
      :34  "1. **ESSENTIALS.md** -- your working standards and rules"     [functional chat]
      :42  "[upload ESSENTIALS.md + any relevant files]"
      :52  "1. **ESSENTIALS.md** -- your working standards and rules"     [programming chat]
      :58  "[upload ESSENTIALS.md + CLAUDE.md from repo]"
      :76  "[upload ESSENTIALS.md + PLAYBOOK.md]"                         [new project]
      (:65 "PLAYBOOK.md is NOT needed here -- ESSENTIALS covers daily work" is CORRECT
       and is NOT flagged.)
      SELF-CONTRADICTION IN THE SAME FILE: :88-104 states the architect role file
      `protocols/HANDOFF_BOOT.md` is "installed **once** as the browser project's own
      instructions rather than pasted into every session" (operator ruling 2026-08-28 B2),
      and points at the single fleet-wide Project "Dev -- Architect Seat". Step 2 still
      instructs a per-session multi-file paste.
      WHAT WOULD HAVE TO CHANGE: the three fenced `[upload ...]` blocks and the two
      numbered "1. ESSENTIALS.md" items -- replaced by the bundle/ROLE-PIN shape
      OPERATOR-INTERFACE.md §5 and HANDOFF_PROCESS §"Browser-role delivery" already own.
      THIS IS THE STRUCTURAL FINDING: a doc stamped `reconciled_with:
      handoff-process@6.3.0` three days ago still teaches the v4 upload ritual. The
      freshness stamp certifies re-reading; it cannot see doctrine that moved elsewhere.

S2-2. protocols/PLAYBOOK.md:1388-1392 -- 1 line in the hit set, 3-line block.
      `### Session resumption protocol` -> "**Browser chat resumption:**
        1. Upload `ESSENTIALS.md` (always)
        2. Upload most recent `docs/handoffs/*.md` (if any)
        3. Upload PLAYBOOK.md (if doing dev work -- large file...)"
      This is verbatim the multi-file upload ADR-79 Decision 2 collapsed to one
      `BUNDLE.md`, and it names `docs/handoffs/*.md` -- a flat-file shape v5/v6 replaced
      with `docs/handoffs/<slug>/` bundles.
      WHAT WOULD HAVE TO CHANGE: the three numbered upload steps.

S2-3. templates/handoff/02_METHODOLOGY.md.tmpl -- 5 lines. Full detail at M1.

S2-4. templates/CLAUDE-md-template.md:19 -- 1 line. Full detail at M2.

--- S3 DEAD-LOCATOR: 8 files, 11 lines. EVERY ONE RESOLVED BEFORE BEING CALLED DEAD ---

S3-1. protocols/PLAYBOOK.md:654 -- DEAD, and the doctrine is ORPHANED. **ESCALATION (b).**
      TEXT: "- Polish prompts -> Claude Code outputs Polish (per ESSENTIALS line 25,
             prompts are English-only)"
      RESOLVED: `sed -n '25p' protocols/ESSENTIALS.md` -> "**Does NOT:**" -- a bare bold
      label inside `## How Claude thinks`. Not the rule.
      AND THE RULE IS NOWHERE IN ESSENTIALS:
        grep -niE "english|polish|jezyk|language" protocols/ESSENTIALS.md -> ZERO hits.
      COMPANION: PLAYBOOK.md:717 "- [ ] **English only** -- ... prompts are English per
      ESSENTIALS" -- same false attribution, no line number.
      WHY THIS ESCALATES: STANDING_RULINGS.md T-29 (:2514-2519) already dispositioned
      this as "accepted-by-relocation", on the stated basis that "the DOCTRINE is live
      and the LOCATOR has drifted" and that it is "a pointer whose target still exists
      under another name". At HEAD that basis is REFUTED for this item: the target does
      not exist in ESSENTIALS under ANY name. The rule's only surviving homes are the two
      PLAYBOOK lines that cite ESSENTIALS as their source. This is a rule-vs-ruling
      conflict, class (b). REPORTED, NOT REPAIRED, NOT RE-RULED.
      SECOND-ORDER: T-29's own evidence line reads "`protocols/PLAYBOOK.md:649` ...
      **Evidence (verified live at HEAD)**". At this HEAD, PLAYBOOK.md:649 is BLANK; the
      text is at :654. The ruling that accepts locator rot has itself rotted by 5 lines.

S3-2. protocols/AI_COUNCIL_PROCESS.md:325 -- DEAD HEADING.
      TEXT: 'per ESSENTIALS § "Repo artifacts in Claude Code, not browser chat"'
      RESOLVED: no such heading among the 15 H2s. Live equivalent is the bullet
      "**Artifact generation direction:**" at ESSENTIALS.md:56.
      Covered by T-29's accepted-by-relocation disposition.

S3-3. protocols/AI_COUNCIL_PROCESS.md:413 -- DEAD HEADING.
      TEXT: '`protocols/ESSENTIALS.md` § "Repo artifacts".'
      Same resolution and same disposition as S3-2.
      (Ironic context: the very same line-block at :412 already corrects one stale
      pointer -- "The former § 'After a Decision' ref was stale -- no such section
      exists." The file demonstrably knows the failure mode.)

S3-4. protocols/AI_COUNCIL_PROCESS.md:327-329 -- MIS-ATTRIBUTED QUOTE. **NEW, NOT
      COVERED BY T-29.**
      TEXT: 'Per ESSENTIALS: "Council ADR distillation is a mandatory automated step of
             the post-debate protocol -- never a browser-chat hand-off with a placeholder."'
      RESOLVED: `git grep -n "Council ADR distillation" -- protocols/` returns exactly
      two lines -- this one, and protocols/PLAYBOOK.md:4834, which holds the quoted text.
      ESSENTIALS does not contain it. The quote is real; the attribution is wrong.
      T-29 named ONLY the § "Repo artifacts" heading at :325,413 -- this third defect on
      the adjacent line is undispositioned.
      WHAT WOULD HAVE TO CHANGE: "Per ESSENTIALS" -> "Per PLAYBOOK" (or cite
      PLAYBOOK § "Post-debate protocol").
      AGGRAVATOR: this file carries `last_reviewed: 2026-08-29` -- TWO DAYS OLD -- and is
      freshness-GATED via _HUB_ONLY_FRESHNESS_FILES. Three unresolvable ESSENTIALS
      locators survived a two-day-old end-to-end re-read certification. The freshness
      gate checks stamp recency, never locator resolution. That is the mechanism gap
      this census exists to name.

S3-5. protocols/STANDING_RULINGS.md:2617 and :2633 -- DEAD LOCATOR IN A RULING'S OWN
      EVIDENCE LINE. **NEW.**
      TEXT (T-34, `[#356]` RULING-W): ":2617 RULING-W is live prose at
      `protocols/ESSENTIALS.md:86` and `protocols/PLAYBOOK.md:1388`" and
      ":2633 **Evidence:** `protocols/ESSENTIALS.md:86`; `protocols/PLAYBOOK.md:1388`".
      RESOLVED, BOTH HALVES:
        ESSENTIALS.md:86 -> "- **Hub->consumer writes (RULING-W):** the hub **MAY and
          SHOULD** write into a consumer ..."  ** RESOLVES EXACTLY. **
        PLAYBOOK.md:1388 -> inside `### Session resumption protocol` (heading at :1384),
          the browser-upload block. NOT RULING-W. RULING-W is at PLAYBOOK.md:1437,
          "**Hub->consumer writes -- the only sanctioned shape (RULING-W; ADR-36/41
          amendments 2026-07-18).**" Drift: 49 lines, landing in an unrelated section.
      SEVERITY: T-34 has `owner: operator`, `next review: 2026-11-24`, and status
      "CLOSED by this section". A November reviewer following the cited locator lands on
      browser-upload instructions -- which are themselves S2-2. Two defects compound.
      WHAT WOULD HAVE TO CHANGE: `protocols/PLAYBOOK.md:1388` -> `:1437` at both sites,
      or better, cite the heading rather than the line.

S3-6. protocols/PLAYBOOK.md:1114 -- STALE RESTATED ROSTER. Full detail at M3.

S3-7. ARCHITECTURE.md:933 vs protocols/PLAYBOOK.md:1261 -- TWO PROSE ROSTERS THAT
      DISAGREE WITH EACH OTHER.
      ARCHITECTURE:933 "| Living | `README.md`, `VISION` ..., `ARCHITECTURE`, `CLAUDE.md`,
        `AGENTS.md`, `PLAYBOOK`, `ESSENTIALS` |"                        -- 7 names
      PLAYBOOK:1261 "- **Living (in-place updates):** README, CLAUDE.md, PLAYBOOK,
        ESSENTIALS, ENVIRONMENT."                                        -- 5 names
      Neither is a subset of the other: ARCHITECTURE omits ENVIRONMENT; PLAYBOOK omits
      ARCHITECTURE, AGENTS.md and VISION. Both omit CONTRIBUTING, SESSION_SETUP and
      STANDING_RULINGS, which CLAUDE.md §4 lists as living. Same W2 / §4-M2 violation
      as M3.

S3-8. protocols/ENVIRONMENT.md:188 -- STALE RESTATED SIZE + ROSTER.
      TEXT: "  ESSENTIALS.md                 <- Daily cheat sheet (1 page)"
      RESOLVED: ESSENTIALS.md is 185 lines / 16,308 B, and its OWN charter line reads
      "A 1-2-page frame by charter". The enclosing `protocols/` tree block lists 5 files;
      protocols/ holds 14 plus archive/. ENVIRONMENT.md is `Last updated: 2026-07-06`
      and is NOT in _FRESHNESS_FILES, so nothing gates it.
      LOW severity; listed for completeness of the repair surface.

S3-9 (soft). ARCHITECTURE.md:284, ARCHITECTURE.md:323,
      .claude/commands/changelog-review.md:23 -- BULLET-AS-HEADING anchors.
      :284 `ESSENTIALS "Architect -> operator channel-discipline"` -- the bullet at
        ESSENTIALS.md:50 is "Architect -> operator channel-discipline **for execution
        actions**"; the quoted string is a truncation, resolvable by prefix.
      :323 `ESSENTIALS "Architect routing for technical proposals"` -- exact string,
        bullet at :54, no heading.
      changelog-review.md:23 `ESSENTIALS "Architect routing"` -- prefix of the same bullet.
      CLASSIFIED SOFT because ESSENTIALS's own `## Architect disciplines` section names
      these six as "standing rules", so citing one by name is legible even though `§`/
      quote form implies a heading. Named here so DC-2 knows they exist; they do not
      change any count above except changelog-review.md, which is counted once at M4.

--- LOCATORS RESOLVED AND FOUND LIVE (checked, NOT defects) ---
  README.md:109  ESSENTIALS "How Claude thinks"   -> :14   OK
  README.md:111  ESSENTIALS "Governance frame"    -> :60   OK
  VISION.md:46   ESSENTIALS "How Claude thinks"   -> :14   OK
  ARCHITECTURE.md:1018 ESSENTIALS "Feedback Loop" -> :140  OK
  PLAYBOOK.md:4879     ESSENTIALS "Feedback Loop" -> :140  OK
  ENVIRONMENT.md:273   ESSENTIALS "Ending a Session" step 3 -> :124 heading, and step 3
                       IS the two-stage code-review step. Exact.  OK
  DEFINITION_OF_DONE.md:195 ESSENTIALS "Ending a Session" -> :124  OK
  STANDING_RULINGS.md:2617/2633 protocols/ESSENTIALS.md:86 -> RULING-W bullet. Exact.  OK
  protocols/README.md:16 "summarizes PLAYBOOK, does not copy it" -- matches CLAUDE.md
                       §5 rule 6 verbatim.  OK
  templates/handoff/02_METHODOLOGY.md.tmpl:18 -> :14 OK · :106 -> :71 OK
  ESSENTIALS.md:49 "Six standing rules" -> six bullets counted (:50,51,52,54,56,58). OK
  protocols/{AGENT_FRAMEWORK:11, HANDOFF_PROCESS:85,224,828}, PLAYBOOK:{328,543,623,633,
    695,1076,1106,1261-as-genre,3376,4206,4733,4784,4801,4814,4828}, tasks/*.md (11 files),
    .claude/commands/{handoff:80, handoff-verify:95} -- generic co-mentions, no locator
    claim, or correct. Clean.

--- BOOT-PATH NEGATIVE FINDING (checked because §1 makes it live-consumed) ---
  The ACTIVE handoff bundle -- docs/handoffs/2026-08-31-dev-knowledge-architect/,
  resolved by newest git add-date (1788185561), the `audit.py::_select_active_bundle`
  predicate -- contains ZERO ESSENTIALS references. So do docs/handoffs/README.md,
  protocols/HANDOFF_BOOT.md, protocols/OPERATOR-INTERFACE.md and CONTRIBUTING.md.
  THE SESSION-BOOT PATH CARRIES NO STALE ESSENTIALS INSTRUCTION. The rot is all in
  on-demand reference surfaces, which is why nothing has tripped over it.

============================================================
5. S4 HISTORICAL-CORRECT -- 466 files, 1,751 lines. SEGREGATED. NOT DEFECTS.
   NEVER PROPOSE TOUCHING THESE.
============================================================
  docs/handoffs/  (incl. archive/legacy)   259   immutable bundles
  docs/audits/                             166   immutable
  docs/decisions/ (ADRs)                    22   immutable except the status line
  docs/intake/                               6   ADR-98 dated intake records
  docs/archive/                              3   archived
  JOURNAL.md, LESSONS.md, logs/TOKEN-LOG.md  3   append-only
  templates/archive/                         4   archived templates
  protocols/archive/                         2   HANDOFF_PROCESS_v3.4, v4.4
  ecosystem/.dev-knowledge/history/          1   dated history record
  -------------------------------------------------------
  TOTAL                                    466   (89.8 % of all hit files)

  Two S4 sub-populations that LOOK like defects and are not:
   - 12 docs/handoffs/*/03_PLAYBOOK.md carry "| `PLAYBOOK.md` | Universal protocols,
     this file |" at a fixed line. That is a preserved 2026-05 snapshot of the same
     table row that is CURRENT at protocols/PLAYBOOK.md:1077. Accurate then, accurate now.
   - 25 handoff .json/.txt manifests and tree dumps list protocols/ESSENTIALS.md as a
     bundle input. Accurate for the bundle that shipped them.
  CONFLATION RISK THIS RULE PREVENTED: a naive sweep would have reported 466 additional
  "stale references", inflating the repair surface from 11 files to 477 -- 43x.

============================================================
6. SWEEP BEYOND THE THREE EXTENSIONS (done-contract item 4)
============================================================
Extensions swept: .md .py .yaml .tmpl .json .js .txt .toml and extensionless.
  git grep -l "ESSENTIALS" -- '*.md' '*.py' '*.yaml'   ->  490 files
  git grep -l "ESSENTIALS" -- .            (all tracked) ->  519 files
  THE NARROW FILTER MISSES 29 FILES -- reproducing the batch-D P2 finding exactly.

Missed by extension:  json 17 · txt 9 · tmpl 2 · js 1
Missed and LOAD-BEARING (2 of 2 predicted by batch-D, both confirmed here):
  templates/handoff/02_METHODOLOGY.md.tmpl   <- carries 3 machine transclusion
                                                directives, one of them DEAD (M1/S3-1
                                                anchor). The single highest-value hit in
                                                the whole census, and `--include=*.md`
                                                cannot see it: the file ends `.tmpl`.
  templates/child-methodology-floor.md.tmpl  <- the deployed methodology floor. Clean,
                                                but invisible to the narrow filter.
Missed and gate-adjacent:
  .claude/workflows/conformance-hub.js       <- the V2 scan-list literal
  tasks/manifest.json                        <- generated backlog mirror
Missed and S4:  25 historical handoff .json / .txt artifacts.
  .toml: zero hits.  Extensionless tracked files: exactly one (.devcontainer/Dockerfile),
  zero hits.  No binary-file hits (`git grep` with and without -I returns 519 both ways).
NET: the narrow filter's blind spot costs 1 of the 2 S2 template defects and 1 of the
11 S3 lines -- i.e. it hides ~14 % of the repair surface, concentrated in its most
machine-shaped member.

============================================================
7. WHAT DC-2 AND DC-3 CONSUME
============================================================
IF ESSENTIALS IS DISSOLVED, these must be re-pointed (this is the full coupling, and
most of it is NOT in the repair surface because it is currently CORRECT):
  CODE (breaks the build/gates):
    scripts/canonical_docs.py :61,:68 + 5 derived tuples (:83,:92,:98,:105,:114)
    scripts/canonical_freshness_gate.py:50   scripts/assemble_paste.py:70
    .claude/workflows/conformance-hub.js:133 (+ seam S11 agreement check)
    tests/test_audit.py:1165 asserts membership -- WILL FAIL on removal
    tests/test_assemble_paste.py:532 asserts the warn string
  CONTRACT (breaks the boot instruction):
    CLAUDE.md §1 item 2, §5 rule 6, §10 -- via their region sources
    templates/claude-regions/{first-read, critical-rules-consistency,
      antipatterns-universal, session-start-protocol}.md
    templates/CLAUDE-md-template.md:19
  DEPLOY: deploy/manifest-v1.4.0.yaml:837-839 `doc_shapes:` (+4 historical manifests)
  REGISTERS: ecosystem/{disposition-register:97,131,134 · index:123 ·
    doc-code-edge:17 · parity-surfaces:635 · provider-registry:40}.yaml
  PROSE POINTERS (10 live locators listed in §4 "found live") -- each needs a new target.
  BACKLOG: tasks/{354,356,390} name PLAYBOOK/ESSENTIALS edges in their Done-when.

THREE ITEMS DC-2 MUST DECIDE BEFORE IT CAN PROCEED, because a census cannot:
  1. The English-only prompt rule (S3-1) has NO home in ESSENTIALS and only two
     PLAYBOOK lines that cite ESSENTIALS as its source. Dissolving ESSENTIALS does not
     move it -- there is nothing to move. It must be re-homed or declared dead FIRST.
  2. T-29's "accepted-by-relocation" disposition rests on a premise false for one of
     its two items. Re-ruling T-29 is the architect's act.
  3. protocols/SESSION_SETUP.md is freshness-gated, stamped 3 days ago, and teaches the
     retired upload ritual in five places. It is the largest single S2 block and it is
     upstream of any ESSENTIALS decision, not downstream of it.

============================================================
8. DECISION BUDGET -- V-2 DISCHARGE
============================================================
ESCALATED (class b, rule-vs-ruling): ONE.
  S3-1 -- STANDING_RULINGS T-29 dispositions the "ESSENTIALS line 25" pointer as a
  drifted locator over live doctrine. At HEAD the doctrine is absent from ESSENTIALS
  entirely, and T-29's own evidence locator (:649) no longer resolves. Reported with
  full evidence; NOT repaired, NOT re-ruled, no subject invented.
NO class (a) curated-baseline touch arose. NO class (c) fork arose.
DECIDED PER CONTRACT DEFAULT AND REPORTED RATHER THAN ASKED:
  - S1 declared empty rather than re-scoped to a nearest-neighbour subject (P1).
  - S2 re-aimed at the copy-vs-pointer / upload-vs-bundle axis, with the re-aiming
    stated in P2 rather than performed silently.
  - S3 "bullet-as-heading" anchors classified SOFT and excluded from the headline
    count, with the judgment shown at S3-9.
  - docs/intake/ classified S4 (dated ADR-98 records), not live surface.
  - tasks/*.md counted as live but non-doctrine: a backlog row describing open work
    is not a citation of a surface as current.
NOT DONE, BY CONTRACT: no repair, no commit, no ruling, no JOURNAL entry, no index
regeneration, no branch, no push, no gate.
```