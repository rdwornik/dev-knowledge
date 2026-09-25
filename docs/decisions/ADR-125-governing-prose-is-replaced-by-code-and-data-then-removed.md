# ADR-125: Governing prose is replaced by code and data, file by file, and removed only after every reader is re-pointed

- **Status:** Proposed
- **Date:** 2026-09-25
- **Decision tier:** Architecture (Path A — the architect's technical proposal under ADR-108 §A, drafted by
  `lane-adr-drafts` on `LANE-5B2-11-adr-drafts.md`, batch WAVE5B-N2 row 11). **Stays Proposed until the operator
  ratifies.** Every removal list is his act (plan §7.4); the functional questions are in §Operator decision options.
- **Amends:** none. **Applies** ADR-122's pattern (a record is data, every view a projection) to the rest of the
  governing corpus; **uses** ADR-29's relocation exception (LESSONS.md, byte-identical) and ADR-121's merge
  trailers and events as successors; **keeps** ADR-85's anchor intent while changing what carries it (step 4).
- **Related:** ADR-118 (one graph; organs are views), ADR-120 (the spine), ADR-101 (tree seal), ADR-114
  (README as front door), ADR-115 (AGENTS.md portable layer), ADR-123 (what ships to consumers), ADR-124 (D5).
- **Provenance:** `PLAN-HARNESS-CONSOLIDATE-DEPLOY-2026-09-25` §1 outcome 3 ("what governs is code and data"),
  §2 W3 (replace-then-remove; the boot's `README.md`/`ARCHITECTURE.md` probes go last), §3.5 and §3.6.
  **Intake:** none — born from a batch order.
- **Decommission:** none by this ADR. Each step below names a removal list; nothing leaves the tree without the
  operator's GO on that list.
- **Source (in-repo):** the files inventoried below, at `da11291b`; `ecosystem/harness.yaml` (`manual_until:
  2026-10-05` entries for `batch_janitor.py`, `check_post_merge.py`, `hook_expiry_verdict.py`, `plan_lint.py`);
  `scripts/generated_artifact_freshness.py:148` and `scripts/gen_dashboard.py:79` (the dashboards' only reader and
  their generator); `.pre-commit-config.yaml:19-30` (the hooks kept for data-loss protection: the JOURNAL anchor
  and the two index-freshness hooks); `CLAUDE.md` (the ≤24,576 B boot contract). **Source (transport, in
  addition):** `to-browser/DIGEST-HUB-INVENTORY-2026-09-25.md` (L1, reviewed; readers by `git grep` over tracked
  files, a prose mention never counted) and its `-appendix.md` (per-file tables, unreviewed; two corrections
  recorded in its header); `to-cc/PLAN-HARNESS-CONSOLIDATE-DEPLOY-2026-09-25.md` §3.5-§3.6.

## Context

1. **The hub governs by prose an agent reads as instructions**, much of it large: `JOURNAL.md` 4,213,943 B,
   `protocols/PLAYBOOK.md` 500,379 B, `protocols/STANDING_RULINGS.md` 334,328 B, `LESSONS.md` 323,767 B,
   `protocols/HANDOFF_PROCESS.md` 125,597 B (`wc -c`, this lane).
2. **Every large prose file has code readers**, some of them gates that fail closed: `block_unanchored_push.py`
   (pre-push) reads JOURNAL; the boot reads JOURNAL's last five entries and the handoff probes read
   `ARCHITECTURE.md`. Removing first and fixing readers later breaks the loop (plan §3.5).
3. **The reader census is a floor, not a ceiling.** L1 lists 2-4 readers for JOURNAL and LESSONS; a name grep over
   `scripts/` in this lane finds **20** files naming `JOURNAL.md`, **14** naming `LESSONS.md`, **25** naming
   `ARCHITECTURE.md`. A name is not a reader (a docstring mention is not a read), so the true set lies between;
   step 0 of every removal is an exact census.
4. **Some files have no reader at all**, and some committed generated files are read only by their own freshness
   check — those can go first at no re-pointing cost (L1 closing lists a and b; spot-checked here with `Grep` over
   `scripts/ .github/ .claude/ deploy/ plugins/ tests/ .pre-commit-config.yaml`: zero hits for
   `FUNNEL_LIFECYCLE.md`, `AGENT_FRAMEWORK.md`, `north-star.md`, `HANDOFF_PROCESS_v3.4`, `ARCHITECTURE-template`,
   `scrum-master-cover-letter`; `scripts/gen_north_star.py` does not exist).

## Decision

- **D1 — Successor kind by what the text does.** A sentence that states a rule a program can decide → a **gate**
  (or a `.claude/rules/` line with a `verify:`). A fact a program reads → a **data record** (typed, validated).
  An event in time → a **git trailer** on the `--no-ff` merge or an **ADR-121 event**. A procedure a seat follows
  when a task needs it → an **on-demand skill or command**. A reason → an **ADR**. Anything else is human
  documentation or goes to the archive. **No new prose that instructs** (plan §6).
- **D2 — Replace, then remove, per file.** (0) exact reader census (imports, argv, path literals opened, hook
  entries, `@`-imports, boot reads); (1) successor built RED-first; (2) every reader re-pointed, gates green;
  (3) the file frozen for one batch — a gate refuses additions; (4) the operator's removal list; (5) removal
  through git (history keeps every byte; ADR/audit/handoff immutability is untouched because those files are not
  on any list here). **Two append-only logs are excluded from this generic path.** `LESSONS.md`: its entries leave
  the active file **only** by ADR-29's sanctioned move (amend. 2026-07-17) — a contiguous older block relocated
  byte-identical into a dated `LESSONS-legacy-<span>.md` with a boundary pointer; nothing is deleted or rewritten,
  and D2 applies only to *new* learnings, which go to their successors instead. `JOURNAL.md`: append-only
  (`CLAUDE.md` §5 rule 2) and the carrier of ADR-85's anchor; D2 may freeze it, but removing it needs its own
  decision amending ADR-85 and that rule — this ADR does not authorise it.
- **D3 — Order by reader risk, lowest first** (§Migration): no-reader files → generated files not read at boot →
  instructing prose with script readers → JOURNAL (a fail-closed pre-push gate) → ARCHITECTURE and the handoff
  files (read by the boot probes) last.
- **D4 — What stays prose.** `CLAUDE.md` and `AGENTS.md` (the runtimes require an instruction file; byte-capped);
  `.claude/` commands, skills, rules and agents (already the on-demand form); ADR bodies, audits, handoffs and
  intake docs (immutable records); `README.md` (the front door, ADR-114); templates the assemblers render (they
  are generator input, and shrink as the prose they carry is replaced).

## The inventory (L1, readers named; reviewed digest unless marked)

**(a) No reader found** — step 1 candidates.

| File | Bytes | Readers | Successor |
|---|---|---|---|
| `protocols/FUNNEL_LIFECYCLE.md` | 34,353 | none (spot-checked) | archive (removal list) |
| `protocols/AGENT_FRAMEWORK.md` | 3,747 | none (spot-checked) | archive |
| `protocols/archive/HANDOFF_PROCESS_v3.4.md`, `v4.4.md` | 53,121 / 39,856 | none | removal list (superseded; git keeps them) |
| `ecosystem/north-star.md` | 5,553 | none; names a generator that does not exist | removal list |
| `ecosystem/<repo>/history/` | 80 files, 272,420 | none by name | removal list, or data if a fleet trend needs it |
| `templates/`: `ARCHITECTURE-template.md`, `audit-template.md`, `consumer-onboarding-runbook.md`, `scrum-master-cover-letter.md`, `handoff/epic/*.tmpl`, `handoff/functional/FUNCTIONAL_BOOT.md.tmpl`, `handoff/v5/{README,RESIDUAL,HANDOFF_BOOT}.md.tmpl`, `archive/*-template.md` (4), `workspace-{L,M,S}.code-workspace` | 651-34,857 each (appendix) | none | removal list |
| `docs/archive/*` | 24 files, 595,638 | none per file (`VISION.md` retained by ADR-114/[#614]) | stays until the operator lists it |
| `scripts/billing_leak_sentinel.ps1`, `scripts/surface_triage.ps1` | — | none ("RETIRED 2026-09-25"; `.py` twins live) | removal list |
| `scripts/batch_janitor.py`, `check_post_merge.py`, `hook_expiry_verdict.py`, `plan_lint.py` | — | none wired; `harness.yaml` `manual_until: 2026-10-05` | not prose: wire (lane-organ-wirings) or retire by the expiry |

**(b) Generated and committed.**

| File | Generator | Readers | Successor |
|---|---|---|---|
| `BACKLOG.md` (99,747 B) | `gen_task_tree.py --emit-source` | `validate_backlog.py` (hook), `backlog_source.py` | ADR-122 — a projection, uncommitted after its step 3 |
| `ecosystem/conformance.{md,html}` (25,762 / 36,399 B) | `gen_dashboard.py` | `generated_artifact_freshness.py` only | on-demand skill; stop committing (step 2) |
| `ecosystem/organ-index.md` | `generate_organ_index.py` | freshness hook, `check_organ_truth.py`, `graph_queries.py` | FPG-1 projection (ADR-118); readers re-pointed to the generator |
| `ecosystem/doc-counts.md` | `gen_doc_counts.py` | freshness hook; cited by `CLAUDE.md` in place of typed counts | keep until the count is served by a command |
| `docs/audits/README.md` (146,224 B) | `gen_audit_index.py` | audit-index-freshness and audit-title-gate hooks, `validate_hermetization.py` | projection on demand once the browser's view is delivered (ADR-122 operator question 1) |
| `docs/intake/README.md` Contents block | `gen_intake_index.py` | intake-index-freshness hook | same as above |
| `.claude/generated/recent-adrs.md`, `.claude/methodology-roster.md` | `gen_claude_rosters.py`, `gen_methodology_roster.py` | `@`-imported by `CLAUDE.md` (boot); freshness hooks | **keep** — this is the data-backed form the boot should read |
| `.claude/generated/commands-repo.md`, `.worktreeinclude` | `gen_claude_rosters.py`, `worktree_seed.py` | freshness hook; worktree seeding | keep (data) |
| five self-written baselines (`audit-{consumer,funnel,title}-baseline.json`, `proof-layer-baseline.json`, `silent-rule-baseline.yaml`), `dependency-baseline.yaml`, `doc-code-edge.yaml` | their checkers | their checkers | keep (ratchet data, not prose) |
| `templates/child-methodology-floor.sha256` | `generate_floor.py` | floor-hash-verify hook | moves with ADR-123's artefact |

**(c) Prose an agent reads as instructions.**

| File | Bytes | Readers (L1 floor; name-grep upper bound where measured) | Successor (D1) | Step |
|---|---|---|---|---|
| `JOURNAL.md` | 4,213,943 | `journal_anchor.py`, `block_unanchored_push.py` (pre-push, fails closed); boot reads last 5 entries; 20 script files name it | merge trailers (ADR-121: `Lane`/`Batch`/`Task`/`Event-Id`) + ADR-121 events; boot's "last 5" becomes a `git log --first-parent` projection; the ADR-85 anchor becomes a trailer check | 4 |
| `LESSONS.md` | 323,767 | `logs_retention.py`, `normalize_headers.py`; `git-discipline.md` rule; 14 name it | new learnings → a candidate row with a regression check (WAVE5B-N2 lane 13, learning distiller v0) or a gotcha; existing entries leave only by ADR-29's byte-identical relocation to dated `LESSONS-legacy-<span>.md` with a boundary pointer — never deleted (D2 exclusion) | 3 |
| `protocols/STANDING_RULINGS.md` | 334,328 | `audit.py`, `decision_coverage.py`, `validate_hermetization.py`, +11 | a ruling register as data (id, date, text, provenance, verifier); scripts read ids | 3 |
| `protocols/PLAYBOOK.md` | 500,379 | `audit.py`, `batch_manifest.py`, `gen_lane_contract.py`, +8; toc-freshness hook | per chapter: rules → gates / `.claude/rules`; procedures → skills; rationale → ADRs | 3 |
| `protocols/{AI_COUNCIL_PROCESS, BUILD-LIST, BUILD-MODE, DEFINITION_OF_DONE, ENVIRONMENT, SESSION_SETUP, README}.md` | 3,505-26,409 each | `audit.py`, `canonical_docs.py`, `gen_lane_contract.py`, `.claude/settings.json` (BUILD-MODE), `preflight_contract.py` (README) | per file by D1; checklists → gates, the rest → skills | 3 |
| `protocols/REPO_ONBOARDING.md` | 15,206 | `deploy/release-v1.3.x-contract.md` only (HD) | ADR-123's `harness install` replaces it | 3 |
| `protocols/HANDOFF_PROCESS.md`, `HANDOFF_BOOT.md`, `OPERATOR-INTERFACE.md`; `docs/handoffs/README.md` | 125,597 / 17,683 / 19,135 / 19,028 | `assemble_paste.py`, `gen_handoff.py`, `verify_handoff_probes.py` (+6), `transport.py`; 2 commands; the boot | the boot split into data the probes verify and prose the seat reads (WAVE5B-N2 lane 12, `lane-boot-contract`) | 5 |
| `ARCHITECTURE.md` | 23,849 | `audit.py`, `canonical_docs.py`, `generate_organ_index.py`; codemap-freshness hook; boot probes P1a/P1b; 25 name it | codemap (already generated) + organ map as FPG-1 projection + one human intent page | 5 |
| `CLAUDE.md`, `AGENTS.md` | 23,988 / 5,843 | Claude Code / Codex boot; `canonical_docs.py`; roster hooks | **stay** (D4), byte-capped | — |

## Quality attributes

- **Quality attribute(s):** Modifiability (primary), Usability (a seat's boot).
- **Scenario (six parts):**
  - *Source:* a new Claude Code seat.
  - *Stimulus:* boots on the hub to dispatch a batch.
  - *Environment:* after step 3 of the migration.
  - *Artifact:* the boot surface (`CLAUDE.md`, its `@`-imports, the active handoff).
  - *Response:* the seat reads the boot contract and data projections, not the large prose files.
  - *Response measure:* first correct dispatch in **≤ 5 turns** (plan P3 gate, measured by lane 12's boot measure);
    **0** readers broken per removal; instructing-prose bytes in the working tree reduced by the removed files'
    measured bytes, reported per step.
- **Decision evidence:** the inventory above and the matrix below.

## Decision matrix

**Scoring rule.** Each option is scored 1-5 per criterion (5 best); total = Σ(weight × score), maximum 500.

Criteria (weights sum to 100): **R1** readers never broken; gates stay green (25) · **R2** boot and working-tree
cost reduced (15) · **R3** instructions become checked — a rule becomes a gate or a verifier (25) · **R4** the
operator controls every deletion (10) · **R5** effort per step; batchable into lanes (10) · **R6** history and the
immutability rules preserved (15).

| Option | R1 | R2 | R3 | R4 | R5 | R6 | Total |
|---|---|---|---|---|---|---|---|
| P0 status quo — prose stays and grows | 5 | 1 | 1 | 5 | 5 | 5 | 340 |
| P1 big-bang — convert everything in one arc | 1 | 5 | 4 | 2 | 1 | 3 | 275 |
| **P2 replace-then-remove per file, lowest reader risk first (D1-D3)** | 5 | 4 | 4 | 5 | 4 | 4 | **435** |
| P3 archive only — move prose out, no successors | 2 | 4 | 1 | 4 | 4 | 5 | 290 |
| P4 data becomes source, every prose file kept as a generated projection | 5 | 2 | 4 | 5 | 2 | 4 | 385 |
| P5 summarise prose into on-demand skills (LLM-written) | 3 | 5 | 1 | 4 | 4 | 2 | 285 |

**Reading.** P2 leads P4 by 50 (P4 keeps every file, so boot and tree cost barely move, and needs a generator per
file); P4 remains the right successor *for a single file* where a human view is wanted (ADR-122 is that case).
P0's 340 is all non-breakage: it satisfies R1/R4/R6 by doing nothing. **Sensitivity:** P2 − P0 = 3·(w_R2 + w_R3) −
(w_R5 + w_R6) = 95; P0 overtakes only if R2 and R3 together weigh less than a third of R5 + R6 — i.e. only if checked
instructions and boot cost are not goals, which plan §1 outcome 3 says they are.

## Migration — steps with measurable exit criteria

Each step is one or more lanes; each removal list goes to the operator before anything is deleted.

1. **No-reader files** (table a). **Exit:** the list delivered; after his GO, removed; `audit.py health` and the
   suite outcome-identical to the pre-step baseline.
2. **Generated files not read at boot** — dashboards first (plan §3.6: re-point `generated_artifact_freshness.py`
   to the generator), then `organ-index.md`. **Exit:** each file's readers call the generator; the file is no
   longer committed; 0 readers broken.
3. **Instructing prose with script readers** — STANDING_RULINGS, PLAYBOOK chapter by chapter, the smaller
   `protocols/` files; LESSONS by ADR-29 relocation only (D2 exclusion). **Exit per file:** exact census = successor
   readers; the file frozen one batch with 0 additions; removed on his GO (LESSONS: relocated, never removed).
4. **JOURNAL.md.** The anchor moves to merge trailers and events. **Exit:** `block_unanchored_push.py`'s replacement
   refuses an unanchored push in a RED-first test; the boot's last-five read comes from `git log`; one batch with
   no JOURNAL write. Leaving the tree then needs a separate decision amending ADR-85 and `CLAUDE.md` §5 rule 2
   (D2 exclusion), and his GO.
5. **ARCHITECTURE.md and the handoff files, last** (plan W3). **Exit:** the boot probes P1a/P1b read their data
   successors; a new seat boots in ≤ 5 turns.

## Flip-condition

- **Stop a step and restore the file** if any gate turns red with a cause attributable to a removed file — one
  such incident per step is enough; the census method is then wrong and is fixed before continuing.
- **Keep a file as a generated projection (P4) instead of removing it** if the operator states he reads it himself
  (operator option 2), or if the boot measure rises after its removal.
- **Stop the programme** if a successor data file starts carrying prose clauses that a program parses by regex —
  the failure ADR-122 measured (53 row-marker regexes) would be recreated under a new name.

## Alternatives considered

- **P0 status quo** — breaks nothing; leaves 5.4 MB of instructing prose in the four largest files alone, and every
  rule in it unchecked.
- **P1 big-bang** — fastest on paper; breaks readers it has not found (Context 3: the census is a floor) and puts
  every deletion in one decision.
- **P3 archive only** — reduces bytes without successors: the rules stop being read *and* stop being checked, and
  the gates that read the files break.
- **P4 projections for everything** — safe, but keeps the files; chosen per file where a human view is wanted, not
  as the programme.
- **P5 LLM-summarised skills** — a skill is still prose; the rules stay unchecked, and a summary is a lossy copy of
  a record (ADR-118: LLMs are methods on the structure, never its judge).

## Consequences

- The corpus shrinks by the measured bytes of each removed file, and the number of rules only prose enforces
  falls to the ones D1 routes to skills.
- Each step costs a census and a successor before it removes anything; the order makes the cheap wins first.
- JOURNAL stops growing once the anchor is carried by trailers the merge already writes; whether its
  four-million-byte history then leaves the working tree (never git) is a later decision amending ADR-85, not this one.
- LESSONS keeps ADR-29's invariant: its entries only ever move, byte-identical, into dated legacy files.
- New data surfaces to own (a ruling register, the lesson rows); they must stay typed (Flip-condition, third bullet).

## Operator decision options

These are functional (ADR-108 §A); the technical choice above stands as proposed unless he rules otherwise.

1. **Ratify the approach** — Accept P2 (replace-then-remove, lowest risk first) · Accept, but keep every file as a
   generated projection (P4) · Return.
2. **Which of these does he read himself** (they then keep a human-readable projection): JOURNAL · LESSONS ·
   PLAYBOOK · STANDING_RULINGS · ARCHITECTURE · none.
3. **Step 1 removal list** — GO on the no-reader list (table a) now · GO after this batch closes · hold.
4. **Dashboards** — on demand only (a skill) · also rendered to the transport at each batch close.
5. **Historic records** (`docs/audits/` 22.0 MB, `docs/handoffs/` 11.8 MB; immutable, no per-file reader) — stay in
   the working tree · leave the tree, kept in git history only.
