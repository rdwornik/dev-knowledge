# EPIC RETURN — llm-first-docs · (filled by the lane at close)
<!-- scope: meta -->

Required before any merge (HANDOFF_PROCESS §14b). Fill each section; keep the headers.
Closure is claimed on the epic done-contract's **hard metric**, never on "committed".

## 1. Commits + branch state

_One line per commit (sha + subject), oldest first. Branch state: clean tree? Suite green
ON THE BRANCH (paste the suite tail)._

- `f222941` docs(handoff): persist S2 gate-collision escalation into EPIC_RETURN §3
- `f54c1b2` docs(journal): anchor epic-lane escalation session (ADR-85 gate repair)
- `9f723ba` docs(handoff): record root CONDITIONAL GRANT + notch mirror
- `d29c2e1` docs(adr): ADR-51 amendment — LLM-first canonical docs (S1)
- `baa0db8` feat(codemap): compact-text codemap output + hub ARCHITECTURE zero-Mermaid (S2)
- `f6a8caf` feat(audit): retire check #7 mermaid_theme_directive (S3)
- `8bd952c` docs(template): ARCHITECTURE template to LLM-first compact-text form (S4)
- (+ the lane-close commit carrying this fill + BACKLOG checkboxes + JOURNAL)

Branch state: `epic/llm-first-docs`, clean tree at close. Suite ON THE BRANCH (post-S4):

```
main suite:        1292 passed, 6 skipped in 512.59s (0:08:32)
conformance file:  5 passed, 1 skipped in 1.16s   (run separately — full-suite-in-one-call exceeds the 5-min tool timeout)
total:             1297 passed, 7 skipped, 0 failed
ruff check:        All checks passed
audit health:      exit 0 (doc_code_coverage_drift: all 28 ALL_CHECKS covered)
```

## 2. Contract-vs-outcome per story

_Per story: **met / partial / dropped**, with evidence against its done-when._

- **S1 — MET** (`d29c2e1`). Amendment authored as a NEW file
  `docs/decisions/ADR-51-amendment-2026-07-05-llm-first-canonical-docs.md` (ADR-51 untouched,
  §5 item 3); Status **Proposed** — the lane does not self-accept; coherent with S2 (D2:
  generated compact text, gate retained, hand-authoring refused — the root ruling's frozen
  direction quoted into the decision) and S3 (D4: check #7 retired, no presence-ban).
- **S2 — MET** (`baa0db8`). Hub `ARCHITECTURE.md`: **zero mermaid fences** (`grep -c
  '\`\`\`mermaid'` = 0; 4 remaining "Mermaid" word-hits are prose about the amendment).
  Codemap block REGENERATED through the tool (never hand-written); layer-model flowchart →
  text with all 4 actors/roles + all 6 labelled edges (incl. the dashed prescribes-read-only
  distinction) — **no dependency fact dropped**. The `codemap-freshness` hook itself **Passed
  on the S2 commit** — the gate stayed coherent with the new form, as the ruling required.
- **S3 — MET** (`f6a8caf`). `check_mermaid_theme_directive` removed (function + ALL_CHECKS
  registration, retirement comments left); 5 pinning tests + `mermaid-theme-pass/-fail`
  fixtures removed; a retirement-guard test added. No audit check asserts a claim the
  amendment retired; no presence-ban replacement (amendment D4 rationale). NARROW GRANT held —
  no other check's contract or shared helper touched.
- **S4 — MET** (`8bd952c`). Template: zero mermaid fences; canonical-target example is the
  compact-text block **derived through `text_emit`** (same api/domain/schema facts, layers,
  edges, paths); §4 Diagrams reframed as the separate human-facing visualization surface.
- **Epic done-contract:** hub ARCHITECTURE renders zero Mermaid ✓ · same dependency facts in
  text ✓ · audit checks coherent with the amendment ✓ · gates green on branch: **all
  in-lane gates green** (pre-commit incl. codemap-freshness/toc/audit-health/ruff on every
  commit; full suite 1297/0 fail) — `ship-gate` reports **2 pre-declared integration-owned
  WARNs**, see §3 items (i)/(j); zero lane-caused undispositioned findings beyond them.

## 3. Self-adjudications + ARCHITECT-REVIEW-PENDING

_Every judgment call made inside the lane's discretion, and every item deferred to the root._

**Self-adjudications (lane discretion — root reviews):**

- **(a) `tests/test_doc_code_edge.py` 2-assertion repair** — the file's two
  `len(ALL_CHECKS) == 29` assertions broke solely from check #7's retirement. Adjudicated
  IN-GRANT under the **assertion-scoped** reading of the E4-1 tests notch ("check-#7
  **assertions** ONLY"): these assertions pin check #7's registry membership via its count.
  Changed exactly the two literals 29→28 (+ the adjacent docstring count); nothing else in
  that file touched. If root reads the notch file-scoped instead, this is the one deviation.
- **(b) `mermaid_emit.py` retained unwired** (not deleted, not renamed) as the future
  visualization-surface emitter — smallest diff, keeps `safe_removal` green, coherent with
  amendment D3. `text_emit.py` reuses its `_find_cycles`.
- **(c) `.pre-commit-config.yaml` untouched** — narrower than the lane's original escalation
  proposal: the ruling's format-change direction made the hook self-coherent (proven: hook
  Passed on the S2 commit).
- **(d) Amendment filed as a separate Proposed file** — root ratifies at integration
  (status-line edit per ADR-94); the lane did not self-declare acceptance.
- **(e) Story checkboxes ticked in the [#259] block with story SHAs** — own-block-only per
  the refusals; no other BACKLOG structure touched.

**ARCHITECT-REVIEW-PENDING (out-of-boundary, listed not chased — root at integration):**

- **(f) `CLAUDE.md`** §4 "Persistent diagrams in ARCHITECTURE.md are mermaid (ADR-51/ADR-59)"
  + §9 `codemap-freshness` hook row wording — stale on merge (ungranted; v2.29-precedent).
- **(g) `protocols/PLAYBOOK.md`** — 3 stale loci: §diagram-form algorithm (~L3067–3075,
  "→ Mermaid (ADR-51 theme)"), §Codemap workflow (~L3412, "embedded Mermaid block"), stale
  "ARCHITECTURE C3 Mermaid diagram" cross-ref (~L2404). **`protocols/ESSENTIALS.md`** — 2
  mentions. All protocols/** (FORBIDDEN to this lane).
- **(h) `ecosystem/doc-code-edge.yaml`** — stale `mermaid_theme_directive` exempt entry
  (L110) + comment word (L61); harmless (guard ignores unknown exempt entries — proven by
  `doc_code_coverage_drift` OK at 28) but should be groomed.
- **(i) `ecosystem/doc-counts.md`** — FORBIDDEN to the lane, now stale by design: 29→**28**
  audit checks, 1301→**1304** pytest collected. The pre-declared root regen-once at
  integration; the `doc_claims` WARN at ship-gate is this, not a lane defect.
- **(j) `deployed_methodology_version` WARN** — worktree-dirname artifact
  ("epic-llm-first-docs" not in deployed-versions.yaml); environmental, recorded not
  dispositioned; expected to vanish on primary (Wave-1 Epic-2 precedent).
- **(k) `docs/decisions/README.md`** ADR-index line for the new amendment — not added
  (outside the docs/decisions/ grant parenthetical); add at ratification.
- **(l) `docs/handoffs/README.md`** carries 1 live Mermaid block (living operator runbook,
  outside boundary) — root disposition under amendment "Out of scope".
- **(m) Child-repo migration + consumer carriers** — child ARCHITECTURE Mermaid codemaps are
  legacy-form tolerated (no gate asserts against them post-#7); `.pre-commit-hooks.yaml`
  exported hooks + deploy manifests untouched; consumers pick up the text form at their next
  pinned-rev / corpus-version bump (ADR-91 — root follow-up ticket proposed in §4).

### ESCALATION (blocking — persisted verbatim 2026-07-05 on root order; lane STOPPED at recon, zero story commits)

**STOP — escalating to root before any commit.** The epic's core done-contract collides with an out-of-boundary enforcement organ, and per the boundary contract ("a needed file outside the boundary → STOP, escalate — don't touch") this needs a root ruling before S1–S4 can proceed coherently. No files touched; branch `epic/llm-first-docs` still at `b501f86`, tree clean.

#### Probe gate (all PASS — lane booted, then blocked on recon)

```
E1 PASS  HEAD b501f86 · branch epic/llm-first-docs · tree clean
E2 PASS  live §14 opening quoted from protocols/HANDOFF_PROCESS.md
E3 PASS  main...HEAD diff empty (nothing touched yet)
E4 PASS* ship-gate RED: 10 WARNs dispositioned, 1 undispositioned —
         deployed_methodology_version reads the WORKTREE dirname
         ("epic-llm-first-docs" not in deployed-versions.yaml).
         Pre-existing worktree artifact, zero lane commits; deploy/** is
         forbidden to me. Flagged for root; expected green from primary.
E5 PASS  bundle = EPIC_BOOT + EPIC_RETURN (unfilled 5-section skeleton) + PROBES
```

#### The escalation: S2 cannot ship through the armed gates inside the FILE-BOUNDARY

**The collision.** S2's done-when is "hub `ARCHITECTURE.md` renders zero Mermaid." But the `codemap-freshness` pre-commit hook (`.pre-commit-config.yaml:28-33`) fires on **any** `ARCHITECTURE.md` change and runs `scripts.codemap.cli check`, which regenerates the codemap **as Mermaid** and hard-fails both possible S2 shapes — I verified the code paths in `scripts/codemap/check.py:40-65`:

- text form kept inside the `CODEMAP` markers → drift diff, exit 1 → commit blocked
- markers removed entirely → "markers not found", exit 3 → commit blocked

Both `.pre-commit-config.yaml` and `scripts/codemap/` are outside my may-touch list. The only in-boundary "fix" would be `--no-verify`/`SKIP` bypasses, which I refuse — it would also merge a permanently broken gate onto main (every future ARCHITECTURE.md edit fails the hook).

**Proposed resolution for root (minimal grant, coherent with the amendment's own logic).** The S1 amendment declares visualization a separate human-facing surface (future Tier-4). That lets `scripts/codemap/` **survive unchanged** as that future surface's generator — merely decoupled from canonical-doc gating. Then the extra grant shrinks to:

1. **`.pre-commit-config.yaml`** — remove the `codemap-freshness` hook entry (hub-local gate retire; mirrors what S3 already does to audit check #7 by explicit grant).
2. **`CLAUDE.md`** — two stale lines after S2: §4 "Persistent diagrams in `ARCHITECTURE.md` are mermaid (ADR-51/ADR-59)" and the §9 `codemap-freshness` hook row. Alternatively root reconciles CLAUDE.md itself at integration (v2.29-precedent style) — either works; I just can't leave them uncorrected silently.
3. **No change needed** to `scripts/codemap/`, `tests/test_codemap.py` (tool untouched → its tests stay green), or `safe_removal` (no module removed).

**Deliberately deferred to root / follow-up ticket (not lane work):** the consumer-facing Mermaid surfaces — `.pre-commit-hooks.yaml` exported `codemap-freshness`/`codemap-generate` hooks and the `deploy/manifest-v*.yaml` precommit carriers (deploy/** is FORBIDDEN to this lane; consumer rollout is versioned-corpus territory, ADR-91); plus `ecosystem/*/state.yaml` `mermaid_theme_directive` evidence rows (regenerated artifacts) and child-repo ARCHITECTURE files that check #7 currently scans cross-repo.

**Also noting (escalation item 3 — listed, not chased):** one living doc outside the boundary carries Mermaid: `docs/handoffs/README.md` (the canonical operator runbook). Audits/old bundles are immutable per ADR-39 and correctly out of scope.

#### Why the lane is not doing S1/S3/S4 first

They're in-boundary, but the amendment's text (S1) and check #7's replacement shape (S3) must state what happens to the codemap generator and its freshness gate — that's exactly the thing under ruling. Authoring first risks an amendment the ruling contradicts, and ADRs/amendments are immutable once landed.

**Awaiting root's ruling** (via operator paste-back into this lane): approve the grant extension as proposed — items 1 and 2, or item 1 plus root-side CLAUDE.md reconciliation at integration — or reshape S2. On receipt the lane executes S1→S4 in order, commit-per-story, re-running E3 at each commit.

#### RESOLVED — root ruling received 2026-07-05: CONDITIONAL GRANT (premise verified TRUE, grant active)

Root's conditional: grant applies IF the colliding organ is the codemap generator + its codemap-freshness hook (ARCHITECTURE's block generator-managed). **Premise re-verified live: TRUE** (`ARCHITECTURE.md:85` "generated by codemap tool" marker stamp · `.pre-commit-config.yaml:28-33` hook entry · `scripts/codemap/check.py:40-65` regen-and-diff).

**The notch (mirrored verbatim from the ruling):** boundary widens by exactly **the codemap generator script + the codemap-freshness hook script + their pinning tests, ONLY as required for S2/S3 coherence**. Direction FROZEN: the compact-text codemap remains **GENERATED** — change the generator's OUTPUT FORMAT (Mermaid → compact text: dependency list + module/layer tables), regenerate ARCHITECTURE's block through it, keep the freshness gate coherent with the new form. **Hand-authoring the text block is REFUSED** (derive-don't-maintain).

Consequences vs the lane's original proposal: `.pre-commit-config.yaml` needs **no change** (the hook entry stays; its check now regenerates in the new form) — narrower than proposed item 1; the CLAUDE.md §4/§9 stale lines (proposed item 2) remain UNGRANTED → left for root at integration, listed under §3. Lane resumed S1→S4 under this grant.

## 4. Proposed BACKLOG delta

_Structural changes for the ROOT to apply at integration (new stories, re-scoping,
closures) — the lane never applies these itself (BACKLOG single-writer for structure,
ADR-97)._

- **Close [#259]** at integration (`closes [#259]` on the root's merge/queue commit) —
  evidence: `d29c2e1`/`baa0db8`/`f6a8caf`/`8bd952c` + the zero-Mermaid hard metric in §2.
- **New task (root files): child-repo codemap migration to compact-text form** — per-repo
  `codemap generate --write` regen (ai-council, corp-monorepo, corp-ops,
  corp-sca-time-automation carry legacy Mermaid codemaps); pairs with the consumer
  corpus-version bump for the updated codemap tooling (ADR-91; `.pre-commit-hooks.yaml`
  pinned-rev consumers).
- **New task or fold-in (root's call): protocols/CLAUDE.md Mermaid-doctrine reconciliation**
  — §3 items (f)/(g) (+ (l) disposition); the amendment is the anchor ref.
- ADR-51-amendment ratification (status line → Accepted, ADR-94 path) + `docs/decisions/README.md`
  index line — §3 items (d)/(k).

## 5. Merge-readiness checklist

- [x] Diff touches ONLY the declared FILE-BOUNDARY as widened by the root CONDITIONAL GRANT
  (`git diff --name-only main...HEAD` audited at every story commit and at close: ARCHITECTURE.md ·
  templates/ARCHITECTURE-template.md · scripts/audit.py · scripts/codemap/* · tests/test_codemap.py +
  codemap fixtures · tests/test_audit.py · tests/fixtures/mermaid-theme-* (deleted) ·
  tests/test_doc_code_edge.py (§3a, 2 assertions) · docs/decisions/ (amendment) · BACKLOG [#259]
  checkboxes · JOURNAL.md · this bundle)
- [x] No merges to main performed from this lane
- [x] JOURNAL entry on the branch names this lane's session SHAs
- [x] Working tree clean; suite green on the branch (1297 passed / 7 skipped / 0 failed; §1 tail)
