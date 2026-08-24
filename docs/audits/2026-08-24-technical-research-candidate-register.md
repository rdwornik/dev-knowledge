# CANDIDATE REGISTER — research distillation, 2026-08-24
Per RESEARCH-TO-REPO-PIPELINE §4 Step 1. Distilled from nine research reports (R-A…R-I) by the
browser architect. **These are candidates, not rulings.** The canonical data is the YAML block;
the prose around it is framing only.

**Field semantics**
- `domain` — which verification lane owns it (V1 governance/agent-context · V2 backlog
  machinery · V3 gates/CI · V4 lifecycle · V5 substrate/models).
- `evidence` — `independent` (peer-reviewed or controlled measurement) · `vendor` (provider
  documentation) · `practitioner` (blog/consensus) · `measured-here` (our own instrumented
  result). **`measured-here` outranks everything else.**
- `changes` — what is different in OUR repo if adopted.
- `cost` — S/M/L implementation size.
- `conflicts` — the ADR/ruling that must be reconciled, or `none`.
- `disposition` — my RECOMMENDATION only: `ADOPT` (ruling + do it) · `INTAKE` (needs evaluation
  through the funnel) · `REJECT` (with reason recorded) · `OPERATOR` (his call, not the
  architect's).
- `carrier` — an EXISTING open row this executes against (no birth), or `NONE` (needs ledger
  headroom), or `intake-N`.

**Two honesty notes.** (1) I do not hold repo files: every `changes` claim is a hypothesis for
the V-lanes to confirm with a locator. (2) I deliberately do **not** cite closed rows as
carriers — `[#563]`, `[#566]`, `[#488]`, `[#529]`, `[#530]`, `[#562]`, `[#565]` were closed in
the last two waves; citing one would reproduce the exact defect class this register exists to
kill. Where the code exists but its row is closed, `carrier: NONE` and the note says so.

```yaml
register_version: 1
date: 2026-08-24
source: nine research reports R-A..R-I (external evidence, zero repo measurement)
ledger_constraint: {open: 212, banked: 0, rule: "no births until closures fund them"}

rows:
# ---------- V1 — governance documents & agent context ----------
- id: C01
  domain: V1
  claim: "One root AGENTS.md (<=120 lines) carrying only non-inferable facts; CLAUDE.md becomes a thin import/symlink of it."
  evidence: independent   # ETH/LogicStar arXiv:2602.11988 — redundant context files cut success, +20% cost
  changes: "Root gains the entry document the operator has asked for three windows; provider files become pointers."
  cost: S
  conflicts: none   # ADR-53 narrow reading already ruled: forbids two content-carrying files, not the name
  disposition: ADOPT
  carrier: "[#577]"

- id: C02
  domain: V1
  claim: "CLAUDE.md is a pointer file (<=200 lines): commands, layout, non-inferable conventions, hard guardrails first, breadcrumbs. Everything procedural leaves."
  evidence: independent   # context rot (Chroma, 18 models); IFScale 68% @500 instructions, primacy bias
  changes: "Ends the recurring 'CLAUDE.md is at its ceiling' crisis structurally instead of by condensing §12 again."
  cost: M
  conflicts: "doc_rot ceiling; CLAUDE.md headroom measured at 2-3 lines"
  disposition: ADOPT
  carrier: NONE

- id: C03
  domain: V1
  claim: "PLAYBOOK splits by chapter type: procedural -> Agent Skills (SKILL.md, on-demand); reference -> machine-readable data; explanation -> ADR. The monolith does not survive."
  evidence: vendor+independent   # Agent Skills 3-level progressive disclosure; minimalism/Diataxis
  changes: "Agents stop being told to 'consult the playbook'; they load one skill when it triggers."
  cost: L
  conflicts: "Ch8 is freshly authored; split must preserve it as a skill, not delete it"
  disposition: INTAKE
  carrier: NONE

- id: C04
  domain: V1
  claim: "Delete prose rules that a linter/hook/gate already enforces; documentation keeps only judgment calls."
  evidence: practitioner   # 'never send an LLM to do a linter's job'
  changes: "Direct reduction of the imperative-token count without losing any enforcement."
  cost: S
  conflicts: none
  disposition: ADOPT
  carrier: NONE

- id: C05
  domain: V1
  claim: "Directory-specific rules move to path-scoped rule files (paths: frontmatter) so they load only when the agent touches matching files."
  evidence: vendor
  changes: "Monorepo packages stop loading irrelevant governance."
  cost: M
  conflicts: "CLAUDE.md §5 rule 7 already records a .claude/rules carve-out — reconcile, do not duplicate"
  disposition: INTAKE
  carrier: NONE

- id: C06
  domain: V1
  claim: "'essentials' is retired unless a consumer census proves a gate or generator reads it."
  evidence: practitioner
  changes: "Removes a document the operator says is never updated and cannot name a purpose for."
  cost: S
  conflicts: none
  disposition: ADOPT
  carrier: NONE

- id: C07
  domain: V1
  claim: "ARCHITECTURE.md keeps only non-derivable content (intent, rejected alternatives, constraints); structural claims are generated (pyreverse/pydeps -> Mermaid) or pointed at."
  evidence: independent   # architectural-drift literature: detection without generation keeps rotting
  changes: "Kills the recurring stale-claims class at its source rather than re-auditing it each window."
  cost: M
  conflicts: "docs-governance lane just re-stamped ARCHITECTURE.md; treat as amendment not rewrite"
  disposition: INTAKE
  carrier: NONE

# ---------- V2 — backlog machinery ----------
- id: C08
  domain: V2
  claim: "Per-item files are the SOLE write surface; the regenerated aggregate with generated_sha256 stops being a write target."
  evidence: independent+practitioner   # every git-native tracker converges on per-item objects
  changes: "Two agents filing one row each stop producing an un-mergeable conflict."
  cost: M
  conflicts: "manifest.json is the membership/ordering authority — must survive the change"
  disposition: ADOPT
  carrier: NONE

- id: C09
  domain: V2
  claim: "Canonical IDs become collision-safe (ULID or content hash); [#NNN] stays as a DISPLAY alias; max+1 scanning is abolished."
  evidence: measured-here   # synthetic [#777] defeated the id scan twice (real ids were 577 / other)
  changes: "Removes a defect that has already bitten twice in one week."
  cost: M
  conflicts: "ADR-107 records the id-derivation rule — amend it, do not bypass"
  disposition: ADOPT
  carrier: NONE

- id: C10
  domain: V2
  claim: "The operator-facing backlog artifact becomes a short committed digest: ledger line, next-5 ready, flow vitals, aging outliers, since-last-window diff. The 212-row dump stops being what anyone reads."
  evidence: practitioner+measured-here   # operator: 'looks the same, huge, huge, huge'
  changes: "The single highest-visibility change available; the view-layer code already exists."
  cost: S
  conflicts: none
  disposition: ADOPT
  carrier: NONE   # export_backlog_view/gen_task_tree --rank are MERGED but their rows are CLOSED

- id: C11
  domain: V2
  claim: "Flow metrics (throughput per window, average age of open rows, aging outliers) become the grooming instrument."
  evidence: independent   # Little's Law; aging-WIP practice
  changes: "This is the missing instrument the closing campaign says it lacks; it also detects ledger gaming."
  cost: S
  conflicts: none
  disposition: ADOPT
  carrier: "[#555] campaign (verify still open)"

- id: C12
  domain: V2
  claim: "Controlled backlog bankruptcy: everything outside the next 2-3 windows moves to an icebox; live set capped ~40-60; one-in-one-out with a bug/discovered-from exemption."
  evidence: practitioner   # Cohn, ProductPlan, Scrum Alliance; OSS stale-bot harm does not apply to a solo operator
  changes: "212 -> a number a human can hold. Git history is the undo."
  cost: M
  conflicts: "[#555] denominator (R2) must define whether an icebox move is a closure or a scope change"
  disposition: OPERATOR
  carrier: NONE

- id: C13
  domain: V2
  claim: "Dependency-aware readiness ('what is unblocked now') outranks value-scoring frameworks (RICE/WSJF/ICE) as the ranking mechanism."
  evidence: independent   # no empirical winner among scoring frameworks; compounding-error critique
  changes: "Ranking becomes computable instead of judgmental."
  cost: M
  conflicts: none
  disposition: INTAKE
  carrier: NONE   # rank command merged, its row closed

- id: C14
  domain: V2
  claim: "The ratchet caps ACTIVE IMPERATIVE RULE IDS, not must/shall/never tokens; every change to the set links an authorizing ruling."
  evidence: measured-here   # 441->445 charged to a session whose files were staged at 441 (commit c559392a)
  changes: "Rewording a rule stops costing headroom; foreign growth stops being charged to whoever commits next."
  cost: M
  conflicts: "the ratchet is itself a standing ruling — amend by ruling"
  disposition: ADOPT
  carrier: NONE

- id: C15
  domain: V2
  claim: "Propose-don't-write is codified: lanes emit generator-ready row specs; only the seat/integrator lands rows."
  evidence: measured-here   # already de facto (lane-rat emitted §6 carrier specs); codify it
  changes: "Makes an existing convention a contract clause and a check."
  cost: S
  conflicts: none
  disposition: ADOPT
  carrier: NONE

# ---------- V3 — gates and CI ----------
- id: C16
  domain: V3
  claim: "Ship-gate/anchor-gate logic is mirrored as GitHub required status checks under a ruleset with an empty bypass list; local pre-commit remains fast feedback only."
  evidence: independent   # only server-side checks are unskippable; client hooks are bypassable by design
  changes: "A rule that must hold stops depending on a correctly-configured local clone."
  cost: L
  conflicts: "Actions minutes budget; measured commit tax already 148s locally"
  disposition: INTAKE
  carrier: NONE

- id: C17
  domain: V3
  claim: "Integration is serialized by MECHANISM (merge queue and/or a primary-checkout lock), not by operator discipline."
  evidence: measured-here   # four primary-checkout contention incidents; the fourth corrupted a MEASUREMENT
  changes: "Turns the most-repeated incident class in this fleet into an impossibility."
  cost: M
  conflicts: none
  disposition: ADOPT
  carrier: "queued Q2-enforcement item (verify filed)"

- id: C18
  domain: V3
  claim: "Every critical gate gets a canary/seeded-failure fixture it must reject; a gate never observed failing is presumed inert."
  evidence: measured-here   # the uv-pin mismatch made the uv run --locked mesh inert in cloud lanes
  changes: "Detects the silent-no-op class that already cost us a whole cloud wave's gate coverage."
  cost: M
  conflicts: none
  disposition: ADOPT
  carrier: NONE

- id: C19
  domain: V3
  claim: "Delivery gate for contracts: a contract file is rejected unless it round-trips through the schema AND carries its exact dispatch command."
  evidence: measured-here   # gen_lane_contract is on a dead path — every contract this window was hand-authored
  changes: "The generator stops being optional; hand-written contracts become un-dispatchable."
  cost: M
  conflicts: "batch-1 contracts of record are grandfathered immutable (already ruled)"
  disposition: ADOPT
  carrier: NONE

- id: C20
  domain: V3
  claim: "Referential-integrity validator: every ruling/disposition reference must resolve to a live id; matchers keyed on measured/mutable values are forbidden by schema."
  evidence: measured-here   # phantom standing-ruling (b); disposition on a CLOSED row; six char-count matchers
  changes: "Kills all three of our real failure classes with one check."
  cost: M
  conflicts: none
  disposition: ADOPT
  carrier: NONE

- id: C21
  domain: V3
  claim: "lychee link/anchor checking runs in CI on the actionable corpus (config only, zero LOC)."
  evidence: independent   # measured zero-error baseline reported by the library-first research
  changes: "Dangling doc references fail loudly instead of aging."
  cost: S
  conflicts: "needs --exclude for our [#id](a) grammar colliding with CommonMark"
  disposition: ADOPT
  carrier: "lychee row filed in part C (resolve its id at landing — do not guess)"

- id: C22
  domain: V3
  claim: "Architecture contracts become executable (import-linter or tach) so layer/cycle rules are CI-enforced rather than described."
  evidence: independent
  changes: "The structural half of ARCHITECTURE.md becomes a check; C07 becomes cheap."
  cost: M
  conflicts: none
  disposition: INTAKE
  carrier: NONE

- id: C23
  domain: V3
  claim: "Python doctrine's enforceable half ships as config: ruff rule families (B/C90/PLR/SIM/RET/ANN/FBT), mypy strict, function/module size limits; the unenforceable half stays a review checklist and is labelled as such."
  evidence: independent+practitioner   # TDD meta-analyses: benefit tracks test granularity, not test-first ordering
  changes: "'Functional, readable Python' stops being taste and becomes a gate."
  cost: M
  conflicts: "intake #34 is BLOCKED on the operator-held source artifact"
  disposition: INTAKE
  carrier: "intake-34"

# ---------- V4 — lifecycle: ADR / intake / audit / registry ----------
- id: C24
  domain: V4
  claim: "Rulings become machine-readable records with stable ids, a status lifecycle (proposed/accepted/superseded/retired), supersession pointers, scope, and a REQUIRED enforced_by field."
  evidence: independent   # MADR/ADR practice + traceability tooling (OpenFastTrace/Doorstop patterns)
  changes: "A ruling with no enforcing check becomes a CI failure instead of a phantom."
  cost: L
  conflicts: "STANDING_RULINGS is prose today; migration must preserve section Q verbatim"
  disposition: ADOPT
  carrier: NONE

- id: C25
  domain: V4
  claim: "Definition-of-done includes the record: a PR touching a governed path fails unless a ruling/ADR is added or an explicit exempt reason is given."
  evidence: practitioner   # ADR-Guard / Danger patterns; no controlled study of efficacy
  changes: "Closes the 'ruled in chat, landed nowhere' leak at the only enforceable point."
  cost: M
  conflicts: none
  disposition: INTAKE
  carrier: NONE

- id: C26
  domain: V4
  claim: "Rule the intake-archival criterion (what makes an intake archivable)."
  evidence: measured-here   # the archival leg ran and returned EMPTY against 34 intakes for want of a criterion
  changes: "Unblocks the operator's most-repeated visible complaint with one ruling."
  cost: S
  conflicts: none
  disposition: ADOPT
  carrier: NONE

- id: C27
  domain: V4
  claim: "Decide ADR-100: keep audits index-only-archived, or amend it to permit physical archival under its §3 preconditions."
  evidence: measured-here   # lane C stopped correctly; PROPOSED-PATH recorded BLOCKED
  changes: "Either the audits tree stops growing unboundedly, or we stop promising archival we cannot lawfully do."
  cost: S
  conflicts: "ADR-100 §1/§3 by definition"
  disposition: OPERATOR
  carrier: NONE

- id: C28
  domain: V4
  claim: "Status-grammar validator plus the ruled marker sweep lands so ADR archival is mechanically possible (four live Status: grammars today)."
  evidence: measured-here   # R4 census: 4 incompatible grammars; 4 superseded-unmarked; 4 archival-eligible blocked
  changes: "ADR archival stops being blocked by an unwritable field."
  cost: M
  conflicts: "ADR-94 permits in-place status edit only on ratification — the narrow restamp exception is already ruled"
  disposition: ADOPT
  carrier: "[#242] + [#362]"

- id: C29
  domain: V4
  claim: "An LLM may PROPOSE rulings from a transcript with verbatim quotes; it may never be the system of record. Human/architect confirmation is mandatory."
  evidence: independent   # decision-detection F1 ~0.35-0.58; dialogue-summary factual inconsistency ~16-27%
  changes: "Prevents automating the exact phantom-ruling failure we already suffered."
  cost: S
  conflicts: none
  disposition: ADOPT
  carrier: NONE

# ---------- V5 — substrate and model routing ----------
- id: C30
  domain: V5
  claim: "A substrate routing table in the repo answers 'where does this run' from declared capability requirements (reviewer_cli, full_history, operator_approval, inputs_on_operator_disk); gen_lane_contract consumes it and emits the verdict plus the exact command."
  evidence: measured-here   # the decision currently lives only in chat; probe measured all four inputs
  changes: "No future seat has to be told which command to type or what runs where."
  cost: M
  conflicts: none
  disposition: ADOPT
  carrier: NONE   # 'M12' as proposed to the incoming architect

- id: C31
  domain: V5
  claim: "Capability enumeration reads BOTH the module exports and PATH-resolvable scripts."
  evidence: measured-here   # 24 module commands + a separate PATH `dispatch` script the operator actually types
  changes: "A generated capability file stops being wrong by construction."
  cost: S
  conflicts: "PLAYBOOK Ch8's 3-alias view is a routing aid, NOT a defect — do not 'fix' it"
  disposition: ADOPT
  carrier: NONE

- id: C32
  domain: V5
  claim: "Reviewer lanes are LOCAL by structural necessity; cloud-eligibility requires BOTH a provisioned binary AND an injectable credential (we hold OAuth tokens, not an API key)."
  evidence: measured-here   # probe: binary absent in provision.sh/Dockerfile, then auth absent
  changes: "Stops anyone 'fixing' this by adding an install line that yields an unauthenticable binary."
  cost: S
  conflicts: none
  disposition: ADOPT
  carrier: NONE

- id: C33
  domain: V5
  claim: "The reviewer must be a DIFFERENT model family from the producer; self-review is not a review."
  evidence: independent   # cross-model review +18.1 points vs ~0 for self-review; self-preference bias literature
  changes: "Formalises what our terra lane already does and forbids the cheap regression to self-review."
  cost: S
  conflicts: none
  disposition: ADOPT
  carrier: NONE

- id: C34
  domain: V5
  claim: "Admission tests use paraphrase sets (>=5 per item), >=20-30 items, held-constant scaffold, and a paired test (McNemar) — a one-item floor measures the prompt, not the model. The Gemini/Grok REFUSALS are re-run under this design before they stand."
  evidence: independent   # prompt-format sensitivity swings measured accuracy by up to 76 points
  changes: "Our admission verdicts become defensible; the promptable-failure finding stops being the whole gate."
  cost: M
  conflicts: "R3's floor reading is a landed ruling — amend by ruling, do not ignore"
  disposition: ADOPT
  carrier: "[#578]"

- id: C35
  domain: V5
  claim: "One model/effort registry with pinned DATED snapshots; floating -latest aliases forbidden in reviewer and adversarial lanes; a drift job diffs provider model lists against the table."
  evidence: independent+vendor   # 58.8% of prompt+model pairs regressed across API updates in one study
  changes: "A provider shipping a new model stops silently changing our results."
  cost: M
  conflicts: "provider registry YAML exists — extend it, do not create a second table"
  disposition: ADOPT
  carrier: NONE

- id: C36
  domain: V5
  claim: "DeepSeek is REJECTED for code-bearing lanes on data-residency/no-enterprise-ZDR grounds; admissible only for non-proprietary fan-out or via a US-hosted endpoint."
  evidence: vendor+independent
  changes: "Answers the operator's DeepSeek ask with a recorded reason rather than a silent omission."
  cost: S
  conflicts: none
  disposition: REJECT
  carrier: NONE

- id: C37
  domain: V5
  claim: "Methodology portability ships as a Copier template + a uv-installable CLI + a skill/plugin pack + org-level CI, with Small/Medium/Large tiers; drift detected by `copier update --check` in CI."
  evidence: vendor+practitioner
  changes: "The apparatus becomes instantiable on ai-council and small projects instead of being hub-bespoke."
  cost: L
  conflicts: none
  disposition: INTAKE
  carrier: NONE
```

## Counts
37 rows — 20 ADOPT · 10 INTAKE · 2 OPERATOR · 1 REJECT · (4 carry an existing carrier).
Of the ADOPTs, **11 rest on `measured-here` evidence** — our own instrumented failures, not
external opinion. Those are the ones to rule first.

## What the V-lanes must return per row
`HAVE <path:line>` · `PARTIAL <what is missing>` · `ABSENT` · `CONFLICTS <ADR/ruling id + quote>`.
Nothing else. The lanes rule nothing; the architect rules over the verified register.
