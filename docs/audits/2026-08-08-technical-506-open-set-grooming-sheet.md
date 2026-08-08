# SHEET-506 — whole-open-set grooming evidence sheet

<!-- scope: meta -->

**This sheet carries EVIDENCE ONLY. It issues no verdict.** No row here says live, dead,
closeable, or stale, and none is a disposition. Per `[#506]`, the read-only evidence half is
separable from the per-id verdict, which is architect adjudication and serializes. Nothing in
`BACKLOG.md`, `tasks/`, or any generator was modified — the sheet is the arc's only new file.

| Field | Value |
|---|---|
| **Generated at** | `2026-08-08T15:01:24+02:00` (HEAD committer clock) |
| **HEAD** | `3ed60c4c5358ca4b07be995e0e3ad0fb69ad41e3` on `worktree-lane-506-groom-sheet` |
| **Live open-count** | **202** |
| **Rows in this sheet** | **202** |
| **Pending closure-proposals** | **153** distinct open ids |
| **Proposal-store locator** | `logs/PROPOSALS-*.md` in the PRIMARY checkout (65 files, `PROPOSALS-2026-06-02.md` .. `PROPOSALS-2026-08-08.md`) — gitignored, therefore per-working-tree and **absent from this lane worktree** |
| **Evidence-completeness** | `complete` **165** · `gap:*` **37** |

## How each column was derived

Every column is mechanical. Where a value could not be determined it reads `unknown` or
`none` — never a guess.

- **id · title** — verbatim from `tasks/*.md` frontmatter. Titles are reproduced as-is,
  including any drift; correcting them is a row edit and out of scope.
- **last-touch** — newest commit touching that row's `tasks/*.md`, over full history.
- **candidate closing merge** — every `--first-parent main` **merge** whose **subject** cites
  the id. Per the contract this is deliberately broader than a `closes` token: a subject
  citation is a *candidate* for the architect to check, not a closure claim. Up to 3 shown,
  bracketed citations first. **A `~` prefix marks a bare-`#N` citation** — see the precision
  limit below; unmarked entries cite the id in the gate-enforced `[#N]` form.
- **open branch refs** — branches (local + remote, excluding `main`) whose **name** cites the
  id, or which carry a commit citing it in `main..<branch>`.
- **serialize-group** — parsed from `scripts/validate_backlog.py`'s own output, not re-derived.
- **linked closure-proposal** — the most recent `logs/PROPOSALS-*.md` where the id is
  **unchecked and still open** (the `#98` pending predicate, via
  `propose_closures._proposals_meta`).
- **evidence-completeness flag** — **mechanical, not a verdict.** `complete` = the row carries
  at least one unambiguous signal to adjudicate against (a bracketed candidate merge, a
  pending proposal, or a branch ref). `gap:no-closure-signal` = none of the three.
  `gap:bare-citation-only` = the sole signal is a `~` bare-`#N` subject citation, which the
  precision limit below makes unsafe to count without reading the subject.
  `gap:*` says nothing about whether a row is live or dead — it describes this sheet's
  evidence, not the row's condition.

## Two measurement caveats that change how the table reads

**1. `last-touch` is dominated by one mechanical sweep.** Commit `5c8a9d6d` (2026-07-28,
"ADR-107 strangler STEP 3 — flip tasks/ to the source of truth") is the newest touch for
**136 of 202** rows, because it created the `tasks/` tree wholesale. Those rows are
marked **ᴮ**. For them, `last-touch` dates the migration, not any consideration of the row —
reading it as row activity would overstate freshness across two thirds of the set.

**2. Ids are cited in two forms, and the bare form is ambiguous.** Today's gates require the
bracketed `[#N]`; older commits use a bare `#N`. Both are matched, because a bracket-only scan
reports long-worked rows as never-cited — witnessed on `#340` and `#266`, which carry only
bare-`#N` merge commits. But the bare form has **no namespace**: `intake #19` and
`consult #1` are different registries, and a subject that enumerates rulings as
`#1 … #2 … #3 … #4` collides with low backlog ids (witnessed on `a0f5aac2`, where `#4` is
ruling 4 while the same subject cites real ids as `BACKLOG #241/#242/#243`).

Two mitigations, and one residue the architect must carry:
- `intake #N` and `consult #N` are stripped before scanning — they are known distinct registries.
- Every bare-form citation is rendered with a **`~` prefix**, so a marked row is one where
  the subject must be read before the citation counts.
- **Residue:** an unkeyworded enumerator (`; #4 ADR-95 …`) is still indistinguishable from a
  bare id by shape alone. Marked entries on **low ids are the ones to distrust**; the subject
  is printed on the row precisely so this is checkable without leaving the sheet.

**A third fact the architect should have before reading row `[#505]`:** its candidate-merge
evidence includes `25ff8ec3`, whose subject is *"…3 rows filed, 0 closed [#505] [#430]"*. That
subject already trips `CLOSES_RE` on `closed [#505]` while explicitly declaring zero closures;
the repo dispositioned it as false-positive-by-construction and `[#505]` stayed open. It is
listed because the column is defined on subject citation, and suppressing it would hide the
one row where the mechanism is known to misread.

## The sheet

One row per live open id. Row-count **202** = live open-count **202**.

| id | title | last-touch | candidate closing merge | open branch refs | serialize-group | linked closure-proposal | evidence |
|---|---|---|---|---|---|---|---|
| [#4] | Build lessons-index.json + SessionStart retrieval + CLI query | 2026-07-28 `5c8a9d6d` ᴮ | `a0f5aac2` ~Merge feat/consult1-disposition — disposition the 4 Fable consult #1 rulings: #1 ADR-81  | none | none | none | `gap:bare-citation-only` |
| [#19] | Complete the ADR-39 register | 2026-07-28 `5c8a9d6d` ᴮ | `1ee48e68` ~Merge chore/backlog-groom-134 — #134 n=1 backlog groom: 78->67 tasks. closes [#81] close | none | none | none | `gap:bare-citation-only` |
| [#23] | Validate ADR frontmatter relation-fields | 2026-07-28 `5c8a9d6d` ᴮ | `ee61dff9` ~Merge docs/handoff-ai-council-p6-window — ai-council P6 window-completion handoff bundle | none | none | none | `gap:bare-citation-only` |
| [#43] | Decide + | 2026-07-28 `5c8a9d6d` ᴮ | `29054cf6` ~Merge docs/2026-07-08-intake-seed-block -- intake SEED block: 4 func intake docs (ids 6- | none | none | `logs/PROPOSALS-2026-08-08.md` _(+30 earlier)_ | `complete` |
| [#71] | Reconcile ENVIRONMENT.md's `~/.claude/` directory tree with live contents | 2026-07-28 `5c8a9d6d` ᴮ | `1ee48e68` ~Merge chore/backlog-groom-134 — #134 n=1 backlog groom: 78->67 tasks. closes [#81] close | none | environment | none | `gap:bare-citation-only` |
| [#82] | Define per-repository agentic-review profiles | 2026-07-28 `5c8a9d6d` ᴮ | `a4d081bd` ~Merge docs/backlog-capture-sota — SOTA gap analysis: #102-#111 + annotations #17/#82/#96<br>`d4399691` ~Merge docs/backlog-agentic-arc -- frame agentic arc: #80 DW research, #81 methodology wo | none | none | none | `gap:bare-citation-only` |
| [#99] | FLEET-HEALTH digest names the failing check per red repo | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#102] | Machine-readable repo index for agent consumption | 2026-07-28 `5c8a9d6d` ᴮ | `a4d081bd` ~Merge docs/backlog-capture-sota — SOTA gap analysis: #102-#111 + annotations #17/#82/#96 | none | none | none | `gap:bare-citation-only` |
| [#112] | adr_amend helper + ADR immutable-zone extension | 2026-07-28 `5c8a9d6d` ᴮ | none | none | claude-md | none | `gap:no-closure-signal` |
| [#116] | Hooks hygiene | 2026-07-28 `5c8a9d6d` ᴮ | none | none | settings-json | none | `gap:no-closure-signal` |
| [#117] | Evaluate prompt/agent-based hooks | 2026-07-28 `5c8a9d6d` ᴮ | none | none | settings-json | none | `gap:no-closure-signal` |
| [#122] | Retire the PATH shim | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#123] | Routine observability convention + value review | 2026-07-28 `5c8a9d6d` ᴮ | `08c5ef81` ~Merge docs/backlog-routine-observability — add #123 routine observability convention + v | none | none | none | `gap:bare-citation-only` |
| [#126] | Backpressure-loop pattern evaluation | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#127] | verify skill failure-output contract | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#130] | Memory-hygiene review | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#132] | Organ-index generator | 2026-07-28 `5c8a9d6d` ᴮ | none | none | pre-commit-config | `logs/PROPOSALS-2026-08-08.md` _(+59 earlier)_ | `complete` |
| [#139] | merged-arc→record verifier | 2026-07-28 `5c8a9d6d` ᴮ | `e9797305` ~Merge chore/consolidation-audit-2026-06-10 -- consolidation audit: recent arc verified a<br>`b6a89203` ~Merge feat/git-backlog-verifier — #90 git↔backlog drift verifier (direction (a) STRONG)  | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+39 earlier)_ | `complete` |
| [#144] | Feature DoD = end-to-end / user-flow test | 2026-07-28 `5c8a9d6d` ᴮ | `57dd61a2` ~Merge docs/a2-acceptance-contract --no-ff -- A2: test-first acceptance contract generali<br>`97ffbb5b` ~Merge feat/worktree-workflow-codification — Close worktree TRANSMISSION gap: make the PL | none | none | none | `gap:bare-citation-only` |
| [#145] | Codification-completeness pass | 2026-07-28 `5c8a9d6d` ᴮ | `8f5694b8` ~Merge docs/a4-contract-essence-completion --no-ff -- A4: Architect Operating Contract es<br>`97ffbb5b` ~Merge feat/worktree-workflow-codification — Close worktree TRANSMISSION gap: make the PL | none | none | none | `gap:bare-citation-only` |
| [#146] | De-hardcode-first doctrine + sweep | 2026-08-06 `576fded9` | `afe1bd8a` ~Merge docs/backlog-146-dehardcode — file #146 de-hardcode-first doctrine + sweep (ADR-81 | none | playbook | none | `gap:bare-citation-only` |
| [#153] | Enforcement-completeness pass | 2026-07-28 `5c8a9d6d` ᴮ | `dec77264` ~Merge chore/153-trim --no-ff -- keep #153 under the doc_rot threshold (ship-gate GREEN)<br>`bf538ee0` ~Merge chore/153-text-currency --no-ff -- #153 text reflects the shipped+activated block-<br>`744af365` ~Merge docs/journal-153-ff-block --no-ff -- author the owed #153 block-ff-push JOURNAL en<br>_(+2 more)_ | none | audit-py | `logs/PROPOSALS-2026-06-17.md` _(+6 earlier)_ | `complete` |
| [#162] | Vocab decision | 2026-07-28 `5c8a9d6d` ᴮ | none | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+55 earlier)_ | `complete` |
| [#166] | doctrine_enforcement_coherence check | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | none | `gap:no-closure-signal` |
| [#169] | Ungated-doc staleness detection | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+50 earlier)_ | `complete` |
| [#170] | Design + land the traceability-spine ADR | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+50 earlier)_ | `complete` |
| [#171] | Build the conformance dashboard at `ecosystem/conformance.md` | 2026-07-28 `5c8a9d6d` ᴮ | `adf0cbe2` ~Merge feat/coherence-integration -- coherence spine v1 integration: wire checker-enumera | none | none | `logs/PROPOSALS-2026-08-08.md` _(+50 earlier)_ | `complete` |
| [#181] | Coherence v2 nudge-response | 2026-07-28 `5c8a9d6d` ᴮ | none | none | coherence | `logs/PROPOSALS-2026-08-08.md` _(+27 earlier)_ | `complete` |
| [#185] | GAP-2 deterministic gotcha-injection guard | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#188] | Deny-rule + hook completeness audit | 2026-07-28 `5c8a9d6d` ᴮ | `de7d0405` ~Merge chore/file-191-onedrive-filepath-guard --no-ff -- file #191 (file_path PreToolUse <br>`442c9944` ~Merge worktree-seal-hooks --no-ff -- Phase-1 seal Track A: #188 hook-completeness audit <br>`62763d73` ~Merge chore/backlog-groom-2026-06-18 -- apply approved 2026-06-18 groom: close [#138] (d | none | none | none | `gap:bare-citation-only` |
| [#189] | Execute in ~/.claude | 2026-07-28 `5c8a9d6d` ᴮ | `62763d73` ~Merge chore/backlog-groom-2026-06-18 -- apply approved 2026-06-18 groom: close [#138] (d | none | none | none | `gap:bare-citation-only` |
| [#190] | General intra-file duplication detector | 2026-07-28 `5c8a9d6d` ᴮ | `e48da286` ~Merge grooming-amended --no-ff -- Phase-1 seal Track C: #140 doc_rot grooming-gate (ADR- | none | audit-py | none | `gap:bare-citation-only` |
| [#210] | Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule | 2026-07-28 `5c8a9d6d` ᴮ | `984ad66e` Merge chore/ratify-533109f-disposition -- ratify 3rd journal-wrap no-ff disposition + fi | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+40 earlier)_ | `complete` |
| [#213] | PLAYBOOK rule/history condensation | 2026-07-28 `5c8a9d6d` ᴮ | `d35e61f6` Merge docs/journal-seal1a-integration — SEAL-1a integration JOURNAL wrap [#213]<br>`9ab191f5` Merge docs/playbook-condensation -- SEAL-1a PLAYBOOK rule/history condensation [#213] | none | playbook | `logs/PROPOSALS-2026-08-08.md` _(+40 earlier)_ | `complete` |
| [#215] | Onboard + verify methodology in a new repo | 2026-07-28 `5c8a9d6d` ᴮ | `32db7eb7` Merge feat/wave1-prep -- repo-onboarding runbook + v1.3.x release contract + all-three-h<br>`7cc4b6a6` Merge docs/handoff-capture — pre-handoff capture: #226(a) floor-provisioning DECIDED (mo<br>`0e2af58d` Merge docs/pre-handoff-hygiene — pre-handoff capture ([#219] loop cross-ref + #131/#215 <br>_(+2 more)_ | none | none | `logs/PROPOSALS-2026-08-08.md` _(+14 earlier)_ | `complete` |
| [#218] | Safe-removal gate M2+M3 boundary | 2026-08-05 `23518240` | `232dbe8c` Merge docs/file-195-successor — file [#218] safe-removal gate M2+M3 boundary (#195's def | none | code-edge | `logs/PROPOSALS-2026-08-08.md` _(+40 earlier)_ | `complete` |
| [#220] | MODIFY / semantic-drift axis | 2026-07-28 `5c8a9d6d` ᴮ | `fbf4a2d0` Merge docs/backlog-reconcile — file audit-surfaced BACKLOG items #220–#229 (deploy-arc r | none | coherence | none | `complete` |
| [#227] | Relocate AGENT_FRAMEWORK.md out of protocols/ | 2026-07-28 `5c8a9d6d` ᴮ | `fbf4a2d0` Merge docs/backlog-reconcile — file audit-surfaced BACKLOG items #220–#229 (deploy-arc r | none | none | none | `complete` |
| [#231] | Consumer → hub feedback report | 2026-07-28 `5c8a9d6d` ᴮ | `7cc4b6a6` Merge docs/handoff-capture — pre-handoff capture: #226(a) floor-provisioning DECIDED (mo | none | none | `logs/PROPOSALS-2026-08-08.md` _(+36 earlier)_ | `complete` |
| [#234] | Cross-repo probe validator | 2026-07-28 `5c8a9d6d` ᴮ | `fef026ed` Merge docs/2026-07-02-ai-council-architect-handoff — v5 cross-repo architect handoff for | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+35 earlier)_ | `complete` |
| [#239] | Follow-up | 2026-07-28 `5c8a9d6d` ᴮ | `bd4fa973` ~Merge feat/informant-organ — Informant Organ (Stage-2 enforcement-transfer): read-only e | none | none | `logs/PROPOSALS-2026-08-08.md` _(+34 earlier)_ | `complete` |
| [#240] | Follow-up | 2026-07-28 `5c8a9d6d` ᴮ | `bd4fa973` ~Merge feat/informant-organ — Informant Organ (Stage-2 enforcement-transfer): read-only e | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+34 earlier)_ | `complete` |
| [#241] | Undeclared-edge groom | 2026-07-28 `5c8a9d6d` ᴮ | `a0f5aac2` ~Merge feat/consult1-disposition — disposition the 4 Fable consult #1 rulings: #1 ADR-81  | none | coherence | `logs/PROPOSALS-2026-08-08.md` _(+34 earlier)_ | `complete` |
| [#242] | ADR status-flip coherence check | 2026-08-04 `43eced57` | `a0f5aac2` ~Merge feat/consult1-disposition — disposition the 4 Fable consult #1 rulings: #1 ADR-81  | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+34 earlier)_ | `complete` |
| [#244] | Essence-spec lifecycle epic | 2026-07-28 `5c8a9d6d` ᴮ | `25b104ed` Merge feat/244-p4-sync-surfacing — [#244] P4 sync surfacing SHIPPED: Informant Tier-3 dr<br>`a7504565` Merge feat/roster-gen-p3 — [#244] P3 generated methodology roster SHIPPED (n=1 hub; mani<br>`2c869518` Merge feat/prune-remove-leg-p2 — [#244] P2 remove leg (deploy engine gains PRUNE)<br>_(+1 more)_ | none | none | `logs/PROPOSALS-2026-08-08.md` _(+34 earlier)_ | `complete` |
| [#245] | Add-path status-awareness | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+33 earlier)_ | `complete` |
| [#263] | Protocols/edge-map reconciliation residuals | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+32 earlier)_ | `complete` |
| [#266] | Codify the test-scoped-grant language lesson | 2026-07-28 `5c8a9d6d` ᴮ | `c3ce72d6` ~Merge docs/2026-07-05-wave2-root-integration-queue — Wave-2 root integration: ratify ADR | none | none | `logs/PROPOSALS-2026-08-08.md` _(+32 earlier)_ | `complete` |
| [#267] | Scope-exercising arc extension | 2026-07-28 `5c8a9d6d` ᴮ | `ffe4d875` Merge feat/267-scope-exercising-arc — #267 half-b (engages scope condition + observer te<br>`fb112667` Merge fix/g7-mirror-codex-highs -- Wave-3 close adjudication 4: G7 Codex 0 CRIT / 2 HIGH<br>`8e1dd571` Merge docs/2026-07-06-wave3-closure-declaration -- Wave-3 close: root declaration + 5 ad<br>_(+1 more)_ | none | none | `logs/PROPOSALS-2026-08-08.md` _(+31 earlier)_ | `complete` |
| [#269] | Audit-index count-tiered shape + freshness hook | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+31 earlier)_ | `complete` |
| [#270] | Operator-load gauge | 2026-07-28 `5c8a9d6d` ᴮ | `d8b564bc` ~Merge docs/handoff-2026-07-11-supplement-fill -- fold the operator's filled architect SU<br>`086aa13d` ~Merge docs/handoff-2026-07-11-architect -- cut the 2026-07-11 architect handoff bundle;  | none | none | `logs/PROPOSALS-2026-08-08.md` _(+31 earlier)_ | `complete` |
| [#271] | Nightly proposal loop | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+31 earlier)_ | `complete` |
| [#273] | Changelog-review staleness escalation | 2026-07-28 `5c8a9d6d` ᴮ | `02389890` Merge worktree-arc5-platform-triage -- Arc-5 platform buy-vs-build triage epic landed: i | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+30 earlier)_ | `complete` |
| [#274] | Dogfood-signal prior in the /changelog-review ADOPT rubric | 2026-07-28 `5c8a9d6d` ᴮ | `02389890` Merge worktree-arc5-platform-triage -- Arc-5 platform buy-vs-build triage epic landed: i | none | none | `logs/PROPOSALS-2026-08-08.md` _(+30 earlier)_ | `complete` |
| [#276] | D2 per-consumer waiver-honoring | 2026-07-28 `5c8a9d6d` ᴮ | `b82dd054` ~Merge chore/post-v131-backlog-state-wrap — post-v1.3.1 rollout: ai-council deployed-vers<br>`d5e7223d` ~Merge fix/deploy-greenfield-prune-skip -- Arc-4 Phase 1: greenfield remove-leg skip (ADR | none | none | `logs/PROPOSALS-2026-08-08.md` _(+31 earlier)_ | `complete` |
| [#277] | propose_closures signal repair | 2026-07-28 `5c8a9d6d` ᴮ | `57ae83a6` ~Merge chore/session-close-0709 -- session-close arc: 39/39 WEAK proposals rejected at ar<br>`a8effba0` ~Merge docs/2026-07-07-post-triage-rulings -- file #277/#278/#279, consume intake #3, ADR | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+11 earlier)_ | `complete` |
| [#278] | Test-suite hygiene epic | 2026-07-30 `27ec8bc5` | `a8effba0` ~Merge docs/2026-07-07-post-triage-rulings -- file #277/#278/#279, consume intake #3, ADR | none | none | `logs/PROPOSALS-2026-08-08.md` _(+30 earlier)_ | `complete` |
| [#280] | Propagate the intake area to greenfield consumers via the deploy manifest | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+30 earlier)_ | `complete` |
| [#281] | Re-peg the ai-council ADR-66 story-map convergence | 2026-07-28 `5c8a9d6d` ᴮ | `5dd29072` ~Merge feat/286-story-ids -- [#286] stable [S<n>] story ids: assigned S1-S20 to every sto<br>`6fef4666` ~Merge docs/2026-07-08-census-triage-rulings -- Wave 0: census-triage rulings (REGISTRY,  | none | none | `logs/PROPOSALS-2026-08-08.md` _(+30 earlier)_ | `complete` |
| [#282] | Fleet `.gitattributes` EOL-normalization parity | 2026-07-28 `5c8a9d6d` ᴮ | none | `worktree-lane-d-282-eol` | none | `logs/PROPOSALS-2026-08-08.md` _(+30 earlier)_ | `complete` |
| [#283] | corp-monorepo `hybrid_classifier.json` 1.08MB duplication | 2026-07-28 `5c8a9d6d` ᴮ | none | `worktree-lane-a-283-dedup` | none | `logs/PROPOSALS-2026-08-08.md` _(+30 earlier)_ | `complete` |
| [#285] | Extend hub freshness gating to PLAYBOOK | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+30 earlier)_ | `complete` |
| [#288] | Model-identity guard for unattended runs | 2026-07-28 `5c8a9d6d` ᴮ | `29054cf6` ~Merge docs/2026-07-08-intake-seed-block -- intake SEED block: 4 func intake docs (ids 6- | none | none | none | `gap:bare-citation-only` |
| [#289] | Hub-own the OneDrive-Blue-Yonder guard | 2026-07-28 `5c8a9d6d` ᴮ | none | none | settings-json | none | `gap:no-closure-signal` |
| [#290] | Floor-carrier verify-teeth + self-heal | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+29 earlier)_ | `complete` |
| [#293] | Consumer runbook fan-out | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+29 earlier)_ | `complete` |
| [#294] | `validate_backlog` deploy-carrier + `--path` de-hardcode | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+29 earlier)_ | `complete` |
| [#296] | `audit.py repo <name> --repo-path` prints a report path that isn't there | 2026-08-06 `e4545b27` | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+29 earlier)_ | `complete` |
| [#297] | Lightweight/dry `observe-arc` coverage mode | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+29 earlier)_ | `complete` |
| [#298] | Handoff-generator polish | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+29 earlier)_ | `complete` |
| [#300] | Hermetization residual d.ii | 2026-07-28 `5c8a9d6d` ᴮ | `e490275c` Merge docs/runbooks-collapse — genre collapse (docs/runbooks -> protocols/) + ADR-101 d.<br>`47f31b5c` Merge ship/lane-b-300 — #300 EPIC-I: ADR-101 hermetization draft (d.i/d.ii/d.iii), PROPO<br>`1545c0d4` Merge chore/remediation-completion-0708 -- incident recovery + remediation completeness  | none | none | `logs/PROPOSALS-2026-08-08.md` _(+29 earlier)_ | `complete` |
| [#301] | Session-plan artifact class | 2026-07-28 `5c8a9d6d` ᴮ | `cb317a58` ~Merge docs/session-wrap-2026-07-11 — intake #13 plan-of-record (#301 iv baseline) + day-<br>`b94a2322` ~Merge docs/morning-triage-filings — night-triage follow-ups #318-#321 + plan-continuity <br>`5fdd0740` ~Merge chore/night-filings-0709 -- Phase-1 night filings: #301 session-plan artifact clas | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+28 earlier)_ | `complete` |
| [#303] | Make seed_runbook.py child-class-aware | 2026-07-28 `5c8a9d6d` ᴮ | none | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+27 earlier)_ | `complete` |
| [#305] | Add a verify-only / already-onboarded re-run mode to the onboarding runbook | 2026-07-28 `5c8a9d6d` ᴮ | `e490275c` Merge docs/runbooks-collapse — genre collapse (docs/runbooks -> protocols/) + ADR-101 d. | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+27 earlier)_ | `complete` |
| [#308] | Decide the `verify` skill's canonical home | 2026-07-28 `5c8a9d6d` ᴮ | none | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+27 earlier)_ | `complete` |
| [#310] | Define the cold-bundle annotation surface + annotate the 2026-07-05 architect bundle as-cold | 2026-07-28 `5c8a9d6d` ᴮ | `b791e419` ~Merge chore/m15-filing-doctor-sweep — post-batch residue sweep: file #310 (cold-bundle a | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+27 earlier)_ | `complete` |
| [#315] | `INSTALL.md` uniform fleet-wide, hub-owned, deploy-carried | 2026-07-28 `5c8a9d6d` ᴮ | `b82dd054` ~Merge chore/post-v131-backlog-state-wrap — post-v1.3.1 rollout: ai-council deployed-vers<br>`e47a2b78` ~Merge docs/file-boundary-matrix-rulings -- file operator-ruled fleet-boundary-matrix fol | none | none | `logs/PROPOSALS-2026-08-08.md` _(+27 earlier)_ | `complete` |
| [#317] | Default-parallel test invocation | 2026-08-06 `6510427a` | `7c1b94fc` Merge docs/lane-cd-integration-journal — record LANE-C + LANE-D integration session [#30<br>`b1f7d618` Merge chore/trim-317-doc-rot — trim #317 to <1200 chars, clear doc_rot WARN [#317]<br>`c7d45921` Merge docs/317-parallel-test-invocation — file [#317] parallel test invocation + slow-ti | none | none | `logs/PROPOSALS-2026-08-08.md` _(+12 earlier)_ | `complete` |
| [#322] | Fleet dashboard | 2026-07-28 `5c8a9d6d` ᴮ | `63a4439a` ~Merge docs/2026-07-11-architect-handoff — #322 fleet dashboard + next architect bundle ( | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+26 earlier)_ | `complete` |
| [#323] | Design question | 2026-07-28 `5c8a9d6d` ᴮ | `617e17a5` ~Merge docs/2026-07-11-319-wrap — #319 integration wrap (close [#319], file #323/#324) | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+26 earlier)_ | `complete` |
| [#324] | Phase-6 axis-2 carrier | 2026-07-28 `5c8a9d6d` ᴮ | `65c9827e` Merge docs/audit-corpus-verb-list — #324 leg-c audit-corpus verb list [#324]<br>`598b9cba` ~Merge docs/2026-07-11-324-v131-wrap — session wrap: #324 integration + v1.3.1 cut record<br>`617e17a5` ~Merge docs/2026-07-11-319-wrap — #319 integration wrap (close [#319], file #323/#324) | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+26 earlier)_ | `complete` |
| [#325] | Carry `/save` to consumers via a manifest command-artifact carrier | 2026-07-28 `5c8a9d6d` ᴮ | `b82dd054` ~Merge chore/post-v131-backlog-state-wrap — post-v1.3.1 rollout: ai-council deployed-vers | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+26 earlier)_ | `complete` |
| [#327] | Protocols-as-interface genre ruling | 2026-07-28 `5c8a9d6d` ᴮ | `b4b1997f` ~Merge docs/e6-fleet-parity-followups — 5 E6 follow-ups from the accepted fleet-parity re | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+26 earlier)_ | `complete` |
| [#329] | VS Code ownership visualization | 2026-07-28 `5c8a9d6d` ᴮ | none | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+26 earlier)_ | `complete` |
| [#331] | Consumer BACKLOG schema adoption ruling | 2026-07-28 `5c8a9d6d` ᴮ | `b4b1997f` ~Merge docs/e6-fleet-parity-followups — 5 E6 follow-ups from the accepted fleet-parity re | none | none | `logs/PROPOSALS-2026-08-08.md` _(+26 earlier)_ | `complete` |
| [#332] | Fleet dependency-version parity | 2026-07-30 `27ec8bc5` | `2bc02196` merge: #328 fleet_parity checker + parity manifest + hub §9a declarations [#328] [#332]<br>`ff2118b2` Merge docs/journal-332 — anchor bde6b55/105cabc (JOURNAL entry for [#332])<br>`105cabc9` Merge docs/backlog-332-dep-version-parity — file [#332] fleet dependency-version parity <br>_(+1 more)_ | none | audit-py | none | `complete` |
| [#334] | Fleet-wide ruff hook id migration `ruff` → `ruff-check` | 2026-07-28 `5c8a9d6d` ᴮ | `97cf58e0` merge: file [#334] fleet-wide ruff id migration ruff -> ruff-check under [S15] | none | pre-commit-config | `logs/PROPOSALS-2026-08-08.md` _(+25 earlier)_ | `complete` |
| [#335] | Exempt `templates/` from the `reconciled_versions` check | 2026-07-28 `5c8a9d6d` ᴮ | `1c11f261` ~merge: A0 seal arc — intake #12 settled + #14 SIEM ruled pack + lessons/PLAYBOOK codific | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+24 earlier)_ | `complete` |
| [#338] | codex-review drift consolidation | 2026-08-06 `6510427a` | `a620d63e` merge: close [#333] doc-lane + file [#338] codex-review drift consolidation | none | codex-review | none | `complete` |
| [#340] | /ship pre-flight validator honors the consumer repo's canonical test gate | 2026-07-28 `5c8a9d6d` ᴮ | `ccd7afab` ~merge: docs/backlog-340-trim — trim #340 under the doc_rot 1200-char threshold (ship-gat<br>`ae6c7592` ~merge: chore/backlog-ship-marker-gap — file #340 (/ship pre-flight honors consumer canon | none | none | `logs/PROPOSALS-2026-08-08.md` _(+23 earlier)_ | `complete` |
| [#341] | Codex producer-lane activation mechanism | 2026-07-28 `5c8a9d6d` ᴮ | `91b36fbe` ~merge: docs/codex-role-governance — Codex role-governance R1/R4/R5 doctrine + #341 produ | none | codex-review | none | `gap:bare-citation-only` |
| [#342] | fleet_parity gate-ahead max-fidelity hardening | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+22 earlier)_ | `complete` |
| [#343] | fleet_parity ship-gate-only scoping | 2026-07-28 `5c8a9d6d` ᴮ | `3571bd5c` ~Merge docs/session-close-2026-07-18 --no-ff — session-close JOURNAL close-out anchor for<br>`54c502fc` ~Merge chore/disposition-backlog-344 --no-ff — disposition doc_rot BACKLOG#344 (ai-counci<br>`1eeea5fb` ~Merge worktree-ai-council-handoff --no-ff — ai-council P6-window-completion handoff bund | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+21 earlier)_ | `complete` |
| [#344] | Session-close gate for handoff generation + consumer hub-write guard | 2026-07-31 `15d2b569` | `7ef40567` Merge branch 'feat/382-desired-state-schema' — [#382] W1: ADR-109 accepted (fleet desire<br>`3571bd5c` ~Merge docs/session-close-2026-07-18 --no-ff — session-close JOURNAL close-out anchor for<br>`1eeea5fb` ~Merge worktree-ai-council-handoff --no-ff — ai-council P6-window-completion handoff bund | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+21 earlier)_ | `complete` |
| [#345] | Externalize the ADR-101 frozensets → machine-readable path-pattern registry + generalize `valida | 2026-07-28 `5c8a9d6d` ᴮ | none | none | pre-commit-config | `logs/PROPOSALS-2026-08-08.md` _(+21 earlier)_ | `complete` |
| [#346] | Persist the two-tier new-path executor rule into `~/.claude` | 2026-07-28 `5c8a9d6d` ᴮ | none | none | claude-md | none | `gap:no-closure-signal` |
| [#347] | Formalize the engineering loop/harness end-to-end + sanctioned safe-deletion pattern | 2026-07-28 `5c8a9d6d` ᴮ | none | none | playbook | none | `gap:no-closure-signal` |
| [#348] | Backlog grooming as a standing routine, not ad-hoc | 2026-07-28 `5c8a9d6d` ᴮ | `05450245` Merge branch 'docs/457-routine-pin-census' — [#457] leg (ii) census discharged: the two  | none | settings-json | none | `complete` |
| [#349] | Mechanize session-discipline inheritance | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+21 earlier)_ | `complete` |
| [#350] | Handoff-process refinements | 2026-07-28 `5c8a9d6d` ᴮ | none | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+21 earlier)_ | `complete` |
| [#351] | Fleet-Python-upgrade ticket | 2026-07-28 `5c8a9d6d` ᴮ | none | none | pre-commit-config | `logs/PROPOSALS-2026-08-08.md` _(+11 earlier)_ | `complete` |
| [#352] | Versioned `.vscode` region decoration | 2026-07-28 `5c8a9d6d` ᴮ | `3fc9458d` Merge docs/352-render-diagnostic — [#352] (f) render-gap diagnostic + [#370] [#371] file<br>`21ec4653` Merge feat/visible-boundary — W1 reader-visible ownership headers + .vscode decoration [ | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+21 earlier)_ | `complete` |
| [#353] | Session-boot contract hardening | 2026-07-28 `5c8a9d6d` ᴮ | `6077c428` ~Merge feat/arc4-leg1-ruff-equalization — ARC-4 leg-1 hub-side: ruff shape + pytest floor | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#354] | W6 seed-1 recurrence half | 2026-07-28 `5c8a9d6d` ᴮ | none | none | playbook | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#356] | RULING-W and the merge-delegation composite are LEGIBLE but have neither a mechanism nor a decla | 2026-07-28 `5c8a9d6d` ᴮ | `9a3fb86b` Merge docs/arc5-census-filing — census declaration test + baseline into [E8], 6 tickets, | none | playbook | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#357] | Silent-rule census run 2 | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#358] | `ecosystem/parity-surfaces.yaml` misdescribes its own enforcement posture at HEAD | 2026-07-28 `5c8a9d6d` ᴮ | none | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#359] | PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md:517-518` claims a mechanism that does not ex | 2026-07-28 `5c8a9d6d` ᴮ | none | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#360] | `protocols/DEFINITION_OF_DONE.md:106-109` expired in place | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#361] | ADR-immutability's real coverage is declared only in code, never in the protocol | 2026-07-31 `c5353d03` | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#362] | #242 carries a SUBSTANTIVE guard loss, not status hygiene | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | none | `gap:no-closure-signal` |
| [#364] | `doc_rot`'s length cap blocks [#353] from doing its job | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#365] | Promote `residual_completeness` from `exempt:` to `coverage_scope` | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#366] | `residual_completeness` scans the WORKING TREE, not the staged blob | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+20 earlier)_ | `complete` |
| [#369] | Wire `boundary_headers.py --check` into pre-commit | 2026-07-28 `5c8a9d6d` ᴮ | `0e5d015b` Merge docs/session-close-arc5 — session-close record, [#368] [#369], [#355] evidence @ 1 | none | pre-commit-config | `logs/PROPOSALS-2026-08-08.md` _(+19 earlier)_ | `complete` |
| [#371] | Consumer editor-config write-through — declared at v1.4.0, never built, never ticketed | 2026-07-28 `5c8a9d6d` ᴮ | `3fc9458d` Merge docs/352-render-diagnostic — [#352] (f) render-gap diagnostic + [#370] [#371] file | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+19 earlier)_ | `complete` |
| [#383] | Execution waves per surface | 2026-08-04 `4e70a0aa` | `42ff1323` Merge branch 'docs/383-ratify-caches-wave' — ARC 0: [#383] ratified, caches wave named, <br>`1afd9579` Merge branch 'feat/intake-split-generality-discharge' — [#383] wave 1: ADR-109 §4 DISCHA | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+18 earlier)_ | `complete` |
| [#385] | L4 tech-currency lane | 2026-07-28 `5c8a9d6d` ᴮ | none | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+18 earlier)_ | `complete` |
| [#387] | Rewrite the buy-vs-build intake BEFORE anything ingests it | 2026-08-01 `3aab4d28` | none | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+18 earlier)_ | `complete` |
| [#388] | The \"10–20 repo\" fleet-scale target is FABRICATED — correct it to the live 5–8+ wherever it is | 2026-07-28 `ae55ff8b` | none | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+18 earlier)_ | `complete` |
| [#389] | Prompt-lint — gate the five architect fields before a lane runs | 2026-07-28 `5c8a9d6d` ᴮ | `db878f4c` Merge docs/playbook-delivery-loop — [#386] delivery loop codified into PLAYBOOK (§21 spi | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+17 earlier)_ | `complete` |
| [#390] | Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template | 2026-07-28 `5c8a9d6d` ᴮ | `db878f4c` Merge docs/playbook-delivery-loop — [#386] delivery loop codified into PLAYBOOK (§21 spi | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+17 earlier)_ | `complete` |
| [#391] | Wire fleet_analytics into a nightly lane, or narrow #384 to a manual reporter | 2026-07-28 `5c8a9d6d` ᴮ | `423a372e` Merge docs/night-batch-close — night-batch integration close: evidence relocated to docs | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+17 earlier)_ | `complete` |
| [#392] | fleet_analytics rename-alias loses history on path-reuse | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+17 earlier)_ | `complete` |
| [#393] | corp-sca rot review — confirm-live-or-retire 3 candidates | 2026-07-28 `5c8a9d6d` ᴮ | none | `worktree-lane-c-393-rot` | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+17 earlier)_ | `complete` |
| [#396] | Extract `scripts/gitenv.py` — the GIT_* env-scrub is in 3 places | 2026-07-28 `5c8a9d6d` ᴮ | `423a372e` Merge docs/night-batch-close — night-batch integration close: evidence relocated to docs | `worktree-lane-e-gitenv-scrub` | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+17 earlier)_ | `complete` |
| [#397] | scripts/ target structure — rule on the mapped grouping, then (maybe) move | 2026-07-28 `5c8a9d6d` ᴮ | `f1c9911d` ~Merge chore/hygiene-pre-handoff — hygiene lane: first intake/decisions archivals + logs  | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+17 earlier)_ | `complete` |
| [#399] | `templates/handoff/v5/README.md.tmpl` — phantom source claim (the [#359] class) | 2026-07-28 `5c8a9d6d` ᴮ | `f1c9911d` ~Merge chore/hygiene-pre-handoff — hygiene lane: first intake/decisions archivals + logs  | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+17 earlier)_ | `complete` |
| [#400] | Ownership-model: the hub-mandated-STRUCTURE / repo-owned-CONTENT cell (rosters) — same ruling fa | 2026-07-28 `9ce96be8` | `624b0485` Merge docs/night-batch-audit-0722 — NIGHT BATCH: transcripts/ deletion (operator ruling, | none | claude-md | `logs/PROPOSALS-2026-08-08.md` _(+16 earlier)_ | `complete` |
| [#401] | ai-council routing still ARMED at the deleted hub landing zone | 2026-07-28 `5c8a9d6d` ᴮ | `19cf25dc` Merge docs/401b-anchor — JOURNAL merge-SHA anchor for the [#401] clause (b) ruling c5f65<br>`c5f65165` Merge docs/401b-ruling — [#401] clause (b) ruled: routing.py PATH-REFUSAL (refs #401, do<br>`2802e401` Merge chore/consolidation-reconcile — BACKLOG next-free pointer [#403] + [#401] doc_rot <br>_(+1 more)_ | none | architecture | none | `complete` |
| [#402] | Intake naming clause — DEPLOY the `YYYY-MM-DD-<class>-<slug>` half of the enum ruling | 2026-07-28 `5c8a9d6d` ᴮ | `fb868199` Merge worktree-enum-reconcile — [#398] ruled intake status-enum deployed (README S3/S5 + | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+16 earlier)_ | `complete` |
| [#403] | Extend `doc_claims` to ARCHITECTURE's machine-derivable claims | 2026-07-28 `5c8a9d6d` ᴮ | `44e47b48` Merge docs/architecture-currency — ARCHITECTURE claim-drift verify-then-fix: carrier cou<br>`2802e401` Merge chore/consolidation-reconcile — BACKLOG next-free pointer [#403] + [#401] doc_rot  | none | audit-py | `logs/PROPOSALS-2026-07-25.md` _(+2 earlier)_ | `complete` |
| [#404] | gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row) | 2026-07-28 `5c8a9d6d` ᴮ | `de402b1c` Merge docs/handoff-execution — execution handoff bundle 2026-07-23 (hand-corrected to §1<br>`2134abef` ~Merge docs/handoff-architect — architect handoff bundle 2026-07-23 (supersedes same-day  | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+16 earlier)_ | `complete` |
| [#405] | Session-end leftover check — nothing verifies \"no leftovers\ | 2026-07-28 `5c8a9d6d` ᴮ | `f3ead30b` Merge chore/trim-405 — [#405] doc_rot trim (self-induced WARN cleared) [refs #405]<br>`21a21e81` Merge chore/leftover-check-filing — [#405] session-end leftover check filed (organ uncho | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+16 earlier)_ | `complete` |
| [#406] | Commit-time doc_rot surfacing — an over-threshold BACKLOG task commits clean, reds only the NEXT | 2026-07-31 `c5353d03` | `023520f0` Merge docs/lane-c-filings — Lane C filings [#406]-[#414] + self-acting-on-main incident  | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+15 earlier)_ | `complete` |
| [#407] | Universal fleet Python style — functional-vs-OOP stance + uniform naming (the paradigm/naming ha | 2026-07-31 `c5353d03` | none | none | playbook | none | `gap:no-closure-signal` |
| [#408] | Auto-coupled doc updates — closing a backlog item must mechanically PULL its ARCHITECTURE + JOUR | 2026-08-06 `a45559f8` | `b8957c98` Merge branch 'docs/supplement-fold-2026-08-06' — supplement folded, [#408] pointer filed | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+15 earlier)_ | `complete` |
| [#409] | Standing night batch — CODE review (formalize as routine) | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#410] | Standing night batch — ARCHITECTURE review (formalize as routine) | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#411] | Standing night batch — creative session, and the recurring Q&A cadence | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#412] | Subagent / workflow routing + configured fan-out + online research into Anthropic's published co | 2026-07-28 `5c8a9d6d` ᴮ | none | none | none | none | `gap:no-closure-signal` |
| [#413] | Colors semantics — visually distinguish global/hub-managed vs per-repo content in governed markd | 2026-07-28 `9ce96be8` | none | none | claude-md | `logs/PROPOSALS-2026-08-08.md` _(+15 earlier)_ | `complete` |
| [#414] | Self-acting-on-main incident family — a session changed `main` with no operator GO and no anchor | 2026-07-31 `c5353d03` | `023520f0` Merge docs/lane-c-filings — Lane C filings [#406]-[#414] + self-acting-on-main incident  | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+15 earlier)_ | `complete` |
| [#415] | Tests must bind fixtures, not live mutable repo content (heuristic-behaviour tests) | 2026-07-28 `5c8a9d6d` ᴮ | `8e2ecc80` Merge docs/fix-live-backlog-test — dedup-specificity guard re-pointed to a fixture (fixe | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+14 earlier)_ | `complete` |
| [#416] | ai-council `ARCHITECTURE.md` codemap drift at L23/L109 | 2026-07-28 `5c8a9d6d` ᴮ | none | `worktree-lane-b-416-codemap` | architecture | `logs/PROPOSALS-2026-08-08.md` _(+14 earlier)_ | `complete` |
| [#417] | `check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non-work | 2026-07-28 `5c8a9d6d` ᴮ | none | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+14 earlier)_ | `complete` |
| [#418] | `automation/fleet-audit` records 0–10 baselines a day, not one | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+14 earlier)_ | `complete` |
| [#419] | We run routines whose output nobody consumes | 2026-07-28 `5c8a9d6d` ᴮ | `371daefd` Merge docs/close-out-folds — fold the [#419] branch-count and [#429] id-invisibility cor<br>`903638c5` Merge docs/0726-brake-discharge — [E9] brake discharged, ADR-105 activation gate, [#419] | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+14 earlier)_ | `complete` |
| [#420] | Does a TOP-LEVEL `docs/archive/` still make sense? | 2026-07-28 `5c8a9d6d` ᴮ | none | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+14 earlier)_ | `complete` |
| [#422] | `reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-contradic | 2026-07-30 `27ec8bc5` | `c74f918c` Merge docs/disposition-421-422 — dispositions for [#421]/[#422]/fleet_parity, [#430], an<br>`d5ef97d0` Merge docs/hub-defects-handoff-tooling — recover intake #17 + [#421] [#422] from the mis | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+13 earlier)_ | `complete` |
| [#423] | The integration sequence runs on prose every time, never mechanized | 2026-07-28 `5c8a9d6d` ᴮ | `ac798945` Merge docs/0726-cleanup — clear the orphaned #262 disposition; file [#423] | none | none | `logs/PROPOSALS-2026-08-08.md` _(+14 earlier)_ | `complete` |
| [#424] | Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is written bar | 2026-08-03 `808ef911` | `42ff1323` Merge branch 'docs/383-ratify-caches-wave' — ARC 0: [#383] ratified, caches wave named,  | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+13 earlier)_ | `complete` |
| [#425] | The suite is green on a format the file does not use | 2026-07-28 `5c8a9d6d` ᴮ | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+13 earlier)_ | `complete` |
| [#426] | Declare `consumer` + `consumption_path` for every LIVE routine | 2026-07-30 `27ec8bc5` | `05450245` Merge branch 'docs/457-routine-pin-census' — [#457] leg (ii) census discharged: the two <br>`57c81fd5` Merge branch 'docs/446-window-step-0-5' — [#446] Step 0.5 window recon + arc 0731-g0-gro | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+13 earlier)_ | `complete` |
| [#427] | Region templates carry a repo-POSITION-DEPENDENT path | 2026-07-28 `5c8a9d6d` ᴮ | `863cb804` Merge docs/427-position-dependent-template — file [#427] position-dependent region-templ | none | claude-md | `logs/PROPOSALS-2026-08-08.md` _(+13 earlier)_ | `complete` |
| [#428] | `nightly-triage` reports a dead producer to every session start | 2026-07-28 `5c8a9d6d` ᴮ | `495b8a22` Merge docs/handoff-review-closing-batch — [#435] filed, [#434] fork RULED, [#428] narrow<br>`e631e59d` Merge docs/428-dead-producer-nag — file [#428] dead-producer session-start nag [#428] | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+13 earlier)_ | `complete` |
| [#430] | Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on state outside  | 2026-08-07 `63b7b6a9` | `25ff8ec3` Merge branch 'docs/consolidate-batch2-lessons' — batch-2 lessons become mechanisms; 3 ro<br>`8bef876e` Merge branch 'docs/batch-2-integration' — batch 2 closed at width 3; 3 rows closed, pack<br>`47bd4f52` Merge branch 'worktree-lane-a-490-parity-manifest' — [#490] parity 9/9 + [#430](a) root <br>_(+1 more)_ | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+13 earlier)_ | `complete` |
| [#431] | `codex-review` silently drops the doc lane on any mixed diff | 2026-07-28 `5c8a9d6d` ᴮ | `feb95e18` Merge docs/recording-batch-433-431-lessons — [#433] engine/viewer ruling, [#431] second <br>`d584ff4a` Merge docs/micro-window-currency — intake #17 §5 MICRO-WINDOW: ARCHITECTURE currency + h | none | codex-review | `logs/PROPOSALS-2026-08-08.md` _(+13 earlier)_ | `complete` |
| [#438] | Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs | 2026-07-28 `5c8a9d6d` ᴮ | `c0b40d37` Merge docs/recording-batch-2026-07-28 — recording batch: [E8] clause (b) AMENDED (D1), 7 | none | playbook | `logs/PROPOSALS-2026-08-08.md` _(+11 earlier)_ | `complete` |
| [#440] | Make the `tasks/` id ledger tamper-evident — a deleted retired record is undetectable | 2026-07-28 `104a04f6` | none | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+11 earlier)_ | `complete` |
| [#441] | Way-of-working: the DEFAULT is one strong self-contained prompt on primary; worktrees are the ex | 2026-07-29 `540acb37` | `14bcb1c4` Merge claude/night-2026-07-28-prep-5my46t — night-batch prep: intake #18 ratification do<br>`952c10ad` Merge docs/recording-batch-r — 2026-07-28 recording batch: owner=user ruled, [#441]/[#44 | none | playbook | none | `complete` |
| [#442] | Plugin command-cache staleness — cached command text can silently outlive a workflow change | 2026-07-28 `9ce96be8` | `952c10ad` Merge docs/recording-batch-r — 2026-07-28 recording batch: owner=user ruled, [#441]/[#44 | none | settings-json | `logs/PROPOSALS-2026-08-08.md` _(+11 earlier)_ | `complete` |
| [#443] | Planning artifacts outside the three enforced classes carry no rent rule | 2026-07-28 `ae55ff8b` | `31fe0e01` Merge docs/intake-20-ratification — intake #20 ratified, #16 ACCEPTED/deferred, [#443] f | none | playbook | `logs/PROPOSALS-2026-08-08.md` _(+11 earlier)_ | `complete` |
| [#445] | `codex-review` wrapper path-guard reports SUCCESS having reviewed nothing | 2026-07-29 `99aceb54` | none | none | codex-review | `logs/PROPOSALS-2026-08-08.md` _(+10 earlier)_ | `complete` |
| [#447] | Self-referential gate family — the committing act cannot satisfy the gate's own precondition | 2026-07-30 `645822ba` | `ebda157e` Merge branch 'chore/447-row-trim' — [#447] row under the doc_rot cap + the 2nd instance  | none | gates | `logs/PROPOSALS-2026-08-08.md` _(+10 earlier)_ | `complete` |
| [#448] | A11 staged-diff guard — cover EVERY candidate bundle, not just the active one | 2026-07-30 `6ae2acb0` | `3f4a1819` Merge branch 'chore/446-seal' — [#446] window seal: closures, [#448], A6 record, LESSONS | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+9 earlier)_ | `complete` |
| [#449] | Assembled-paste byte budget — should `PASTE_THIS.md` gain a hard ceiling? | 2026-07-30 `6bfa544f` | `65a549bf` Merge branch 'docs/2026-07-31-ratification-batch' — intake #22 §A+§B ratified (ADR-108)  | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+9 earlier)_ | `complete` |
| [#450] | Per-section intake ratification — the `status:` field is doc-level, so partial ratification need | 2026-07-30 `6bfa544f` | none | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+9 earlier)_ | `complete` |
| [#451] | CA layer-edge check — port the ai-council layer-edge review as the missing Layer-2 organ | 2026-07-30 `6bfa544f` | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+9 earlier)_ | `complete` |
| [#452] | `[#433]`→`[#382]` pilot-precedes-contract dependency is prose-only — no `depends-on` clause exis | 2026-07-30 `6bfa544f` | `65a549bf` Merge branch 'docs/2026-07-31-ratification-batch' — intake #22 §A+§B ratified (ADR-108)  | none | audit-py | none | `complete` |
| [#453] | Cloud night-run runbook — the container gaps that silently degrade an unattended session | 2026-07-31 `584ab835` | none | none | environment | `logs/PROPOSALS-2026-08-08.md` _(+8 earlier)_ | `complete` |
| [#454] | `closure_ids` negation defect — the parser reads a negated closure mention as a closure | 2026-07-31 `584ab835` | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+8 earlier)_ | `complete` |
| [#456] | Ruling-blocked cohort sweep — re-route the remaining Done-when clauses per ADR-108 §A | 2026-07-31 `584ab835` | none | none | none | none | `gap:no-closure-signal` |
| [#457] | Two live-repo tests fail on main against green gates — test-vs-organ mismatch | 2026-08-05 `7a70f54c` | `05450245` Merge branch 'docs/457-routine-pin-census' — [#457] leg (ii) census discharged: the two <br>`0c64a76a` Merge branch 'docs/file-night-batch-defect-rows' — night-batch defect rows [#477]-[#480]<br>`356841a9` Merge branch 'docs/457-inherited-test-failures-row' — file [#457] inherited test-failure | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+8 earlier)_ | `complete` |
| [#463] | win-tooling onboarding debt — 2 FAILs + 2 WARNs unchanged since admission | 2026-08-01 `3aab4d28` | `13b98f22` Merge branch 'docs/fleet-audit-deep-review' — [#463][#464][#465] filed, [#460] recommend | none | environment | none | `complete` |
| [#464] | corp-*/ai-council governance drift — five findings live 15–46 days, surfaced daily, zero consump | 2026-08-01 `3aab4d28` | `13b98f22` Merge branch 'docs/fleet-audit-deep-review' — [#463][#464][#465] filed, [#460] recommend | none | environment | none | `complete` |
| [#470] | `audit.py checks` crashes mid-listing on a cp1252 console — one U+2192 glyph | 2026-08-01 `3aab4d28` | `b0af8e92` Merge branch 'docs/filing-batch-2026-08-01' — conformance absorbed, intake #23 filed, [# | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+7 earlier)_ | `complete` |
| [#477] | `deployed_methodology_version` keys the registry by repo-root BASENAME — a clone named `dev-know | 2026-08-03 `d2ba06ca` | `0c64a76a` Merge branch 'docs/file-night-batch-defect-rows' — night-batch defect rows [#477]-[#480] | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+5 earlier)_ | `complete` |
| [#478] | `changelog_sentinel` drops PEP 440 suffixes — a prerelease as the reviewed value silences the se | 2026-08-03 `d2ba06ca` | none | none | none | none | `gap:no-closure-signal` |
| [#484] | ADR-106 system-Python divergence — named deferral, not an open build | 2026-08-04 `aad1a235` | none | none | environment | `logs/PROPOSALS-2026-08-08.md` _(+4 earlier)_ | `complete` |
| [#485] | A shared LF-enforcing write helper — the mechanism that replaces the CRLF gotcha | 2026-08-04 `aad1a235` | none | none | audit-py | `logs/PROPOSALS-2026-08-08.md` _(+4 earlier)_ | `complete` |
| [#486] | `desired_state_report.py` dies on a cp1252 console — U+21C4 in its own HONEST LIMITS text | 2026-08-05 `4ca1ca23` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#487] | Closure-proposal consumption arc — repair the pipeline first | 2026-08-06 `4cdf2a4b` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#488] | Priority axis — the backlog has no ranking function beyond a hand-set [P1..P3] | 2026-08-05 `4ca1ca23` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#491] | Gemini scanning lane — ruling R-G plus an acceptance contract | 2026-08-05 `4ca1ca23` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#492] | Grok review-lane acceptance — gated ≥ 2026-08-07, measured against terra on the same diffs | 2026-08-05 `4ca1ca23` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#493] | B-2 investigation — the scheduled fleet-baseline task has been silent 10+ days | 2026-08-05 `4ca1ca23` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#494] | Ladder ratification — L0–L5 promote-vs-leave is unruled, and prose already cites it as authority | 2026-08-05 `4ca1ca23` | none | none | none | none | `gap:no-closure-signal` |
| [#495] | Tech-currency cadence — give [#385] a recurring lane instead of a one-off | 2026-08-05 `4ca1ca23` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#496] | `_ORGAN_TO_COMPONENT` attributes the pre-push organ to a component that does not carry it — the  | 2026-08-05 `4ca1ca23` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#497] | Two stale claims on carrier/hook declarations | 2026-08-05 `23518240` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#499] | Promote the review-artifact coverage leg to a hard pre-push gate | 2026-08-05 `23518240` | `05450245` Merge branch 'docs/457-routine-pin-census' — [#457] leg (ii) census discharged: the two <br>`e676cd3f` Merge branch 'feat/480-review-artifact-organ' — review-artifact coverage made checkable  | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#500] | The Stop hook's BACKLOG advisory reads a correctly-closed task as \"nothing closed\ | 2026-08-05 `23518240` | `05450245` Merge branch 'docs/457-routine-pin-census' — [#457] leg (ii) census discharged: the two <br>`e676cd3f` Merge branch 'feat/480-review-artifact-organ' — review-artifact coverage made checkable  | none | none | `logs/PROPOSALS-2026-08-08.md` _(+3 earlier)_ | `complete` |
| [#502] | mutmut 3.7.0 mutation-testing evaluation — CI-hosted | 2026-08-06 `e7c0b70e` | `3234abb3` Merge branch 'fix/502-mutmut-sandbox-markers' — the [#502] chain's third blocker [#502]<br>`945598f9` Merge branch 'feat/pre2-batch2-preconditions' — batch-2 preconditions cleared [#505] [#5<br>`2f2edd2b` Merge branch 'docs/morning-consolidation' — integrate the night audit, close F4, land R-<br>_(+2 more)_ | none | environment | none | `complete` |
| [#505] | Batch-protocol encoding — the parallel-execution way-of-working as versioned repo artifacts | 2026-08-08 `af1fd03b` | `8c438220` Merge branch 'chore/pre-cut-gate-hygiene' — five inherited WARNs, honestly resolved: thr<br>`b669bd8f` Merge branch 'docs/handoff-engine-thinning' — the bundle carries pointers, the repo carr<br>`25ff8ec3` Merge branch 'docs/consolidate-batch2-lessons' — batch-2 lessons become mechanisms; 3 ro<br>_(+8 more)_ | none | playbook | `logs/PROPOSALS-2026-08-08.md` _(+2 earlier)_ | `complete` |
| [#506] | Whole-set P10 grooming arc — the open set is unreconciled | 2026-08-06 `92db7d9d` | `461fa233` Merge branch 'docs/arc1-intake26-adr-doctrine' — ARC-1: intake #26 filed, ADR-110 cut, S | `worktree-lane-506-groom-sheet` | none | none | `complete` |
| [#507] | Report-only wall — decide the fourth recorded leg (`pre-commit run --all-files`) | 2026-08-07 `876cc463` | `945598f9` Merge branch 'feat/pre2-batch2-preconditions' — batch-2 preconditions cleared [#505] [#5 | none | architecture | `logs/PROPOSALS-2026-08-08.md` _(+1 earlier)_ | `complete` |
| [#508] | Couple the lane-prefix enum's cardinality to its prose, or record it deliberately-unmechanized | 2026-08-07 `876cc463` | `945598f9` Merge branch 'feat/pre2-batch2-preconditions' — batch-2 preconditions cleared [#505] [#5 | none | gates | `logs/PROPOSALS-2026-08-08.md` _(+1 earlier)_ | `complete` |
| [#509] | `Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR` | 2026-08-07 `e351b685` | none | none | none | `logs/PROPOSALS-2026-08-08.md` _(+1 earlier)_ | `complete` |
| [#510] | Scope the R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming t | 2026-08-07 `e351b685` | none | none | gates | `logs/PROPOSALS-2026-08-08.md` _(+1 earlier)_ | `complete` |
| [#511] | The 30-minute handoff cut is ~99.8% session authoring, not machinery | 2026-08-07 `e351b685` | `8c438220` Merge branch 'chore/pre-cut-gate-hygiene' — five inherited WARNs, honestly resolved: thr<br>`b669bd8f` Merge branch 'docs/handoff-engine-thinning' — the bundle carries pointers, the repo carr | none | handoff | `logs/PROPOSALS-2026-08-08.md` _(+1 earlier)_ | `complete` |
| [#512] | `gen_handoff.py`'s open-batch refusal doesn't scrub `GIT_DIR` | 2026-08-07 `e351b685` | `8c438220` Merge branch 'chore/pre-cut-gate-hygiene' — five inherited WARNs, honestly resolved: thr | `worktree-lane-e-gitenv-scrub` | gates | `logs/PROPOSALS-2026-08-08.md` _(+1 earlier)_ | `complete` |

**ᴮ** = last-touch is the `5c8a9d6d` bulk `tasks/` migration, not row-specific activity.

## Gap census

- `no-closure-signal` — **22** rows
- `bare-citation-only` — **15** rows

A `gap:no-closure-signal` row is one the Phase-3.5 wave cannot adjudicate from this sheet
alone. Naming that count is the point: it is the honest size of the archaeology the evidence
half could not remove.
