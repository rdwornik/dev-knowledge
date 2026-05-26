---
type: research-proposal
scope: AI Council pipeline + .dev-knowledge docs/ taxonomy
date: 2026-05-25
basis: 2026-05-25-council-pipeline-audit.md
status: proposal (operator decides)
---

# AI Council Pipeline + docs/ Taxonomy — Proposal 2026-05-25

> Prescription layer. Recommends a direction grounded in the audit's findings; **nothing here is
> applied.** No files move, no folders are created, no ADRs are amended by this document. The operator
> chooses an option (or none) and any change runs as a separate prompt/branch.
>
> Out of scope per the operator: the handoff process, methodology rewrites, workspace aliases, and
> executing any ADR amendment. Where an ADR *may be warranted* this proposal only flags it for the
> operator — it does not draft or amend one.

## Design principles (derived from the audit)

1. **Documentation must match reality first.** The two High findings about routing (E1/E2) are pure
   staleness; correcting them is zero-risk and unblocks correct agent behavior regardless of any
   taxonomy decision. Truth-up precedes restructure.
2. **A file's folder should tell you what it is** — input vs output vs working vs archived. This is the
   root of A1/G and the operator's primary frustration.
3. **Proportional governance.** The pipeline is a low-volume solo workflow (22 transcripts over ~5 weeks,
   5-question batches). Per ADR-48 (trim to structural enforcement) and the "governance proportionality"
   posture, prefer the smallest change that fixes the root; avoid machinery that costs more than the
   friction it removes.
4. **Preserve the Layer-2 invariant and the read-only-content contract** with ai-council. No proposal may
   make `.dev-knowledge` execute or write tracked content into ai-council.
5. **One holistic view of the lifecycle** should exist in `.dev-knowledge` (a runbook + a state convention),
   so the pipeline can be reasoned about without reading ai-council source.

---

## Proposed structure

### Option A — Minimal change (truth-up, no moves)

Fix only the documentation-vs-reality gaps; leave the taxonomy as-is.

- Correct the three "routing is pending/manual" blocks (`PLAYBOOK.md:1499`, `:1526-1541`;
  `decisions/README.md:95-104`) to state that ADR-43 routing is **implemented**, transcripts auto-land in
  `transcripts/` via `target-project:`, and manual archival is the fallback only.
- Reconcile `BACKLOG.md:81-86` `[P2]` (close or re-scope to "verify end-to-end + delete manual-archival
  language").
- Refresh stale counts (12/14 → actual).
- Add a short "what `research/` actually holds today" note to `research/README.md` acknowledging the
  question-staging usage (documents A1 rather than fixing it).

**Pros:** kills all four doc-vs-reality findings (E1–E4); near-zero risk; hours of effort; no link churn.
**Cons:** leaves A1/A2/G (the taxonomy root, also High) unaddressed — `research/` stays a catch-all; the
"input vs output ambiguous" frustration persists.
**Effort:** ~1 short session, edits only.

### Option B — Moderate reorganization (truth-up + input/output separation) — *recommended*

Everything in A, plus a minimal taxonomy change that separates pipeline **inputs/working** files from
research **outputs**, and one holistic runbook.

- **Designate a staging home for Council question drafts + evidence + set-indexes** (Stage 0/1 working
  artifacts) — separate from `research/` outputs. Exact location is an open question below (a new
  `docs/council-questions/` vs a `research/questions/` subfolder vs a naming-prefix convention).
- **Reclassify the 2026-05-25 Q-set** (`Q1..Q5`, evidence, index) into that staging home; leave finished
  research outputs in `research/`. Update `research/README.md` to describe only outputs.
- **Add one pipeline runbook** in `.dev-knowledge` (e.g. a PLAYBOOK subsection or a single
  `docs/decisions/` reference) covering the full Stage 0→7 lifecycle, the `council --inbox` step, the
  gitignored-inbox nuance (resolves D1), and the routing-is-automatic truth (folds in A's truth-up).
- **Promote the branch-local mechanism doc** (E3) into `main` (or supersede it with the runbook) so the
  resolved mechanism is visible on the default branch.

**Pros:** addresses **both** High roots (staleness + taxonomy); folder now signals input vs output;
single lifecycle view; still small.
**Cons:** touches the file taxonomy (arguably ADR-worthy — see open questions); a handful of files move, so
existing links/traceability references must be updated; one operator decision required (staging location).
**Migration considerations:** the moved Q-set is referenced by the branch-local mechanism doc and the
`-council-index.md`; update those references. Transcripts/ADR traceability table in `decisions/README` is
unaffected (no transcripts move). No ai-council change.
**Backward compatibility:** `research/` outputs and their inbound links are untouched; only the 7 input
files relocate.
**Effort:** ~1 focused session after the staging-location decision.

### Option C — Substantial restructure (explicit pipeline-stage taxonomy)

Everything in B, plus encode the pipeline lifecycle directly in folder structure and add tracking.

- Introduce stage-named folders or a role-encoding naming convention across the whole pipeline (e.g.
  `questions/` → `transcripts/` → `decisions/`), and a lightweight **pipeline manifest** (resolves B2/B3):
  a single index of question-set → dispatched → transcript → ADR status.
- Optionally define a *documented, still-manual* Stage-2 helper convention (a checklist or a read-only
  validator that flags un-dispatched/un-archived debates) — **without** automating cross-repo writes
  (Layer-2 preserved).

**Pros:** lifecycle is legible from structure alone; manifest gives the holistic view and a completion
signal; strongest answer to "reason about it holistically."
**Cons:** highest churn and highest risk of over-engineering a low-volume solo pipeline (principle 3);
a manifest is a new living artifact that can itself drift; renames ripple through ADR traceability and
PLAYBOOK references. Disproportionate to current volume.
**Effort:** multi-session; new conventions to maintain.

---

## Recommendation

**Option B**, sequenced so A's truth-up is phase 1.

Reasoning, grounded in the audit (not preference):
- The audit found **four High findings across two roots**. Option A fixes only the staleness root
  (E1/E2/E4) and explicitly leaves A1/G (also High) unaddressed — so A is insufficient on its own.
- Option C resolves everything but adds stage-folders, a manifest, and Stage-2 tooling. The pipeline's
  measured volume (22 transcripts/~5 weeks; 5-question batches) and the repo's own proportionality posture
  (ADR-48; governance-proportionality) make C's standing machinery cost exceed the friction it removes —
  the manifest (B2/B3, both Medium) is a *Medium* problem and does not justify a *new permanent artifact*.
- Option B fixes both High roots with documentation plus one input/output distinction and a single runbook,
  and keeps the change proportional. It is the smallest option that does not leave a High finding open.

Sequencing matters: **phase 1 = A's truth-up** (zero-risk, do regardless), **phase 2 = B's taxonomy split**
(after the operator answers the staging-location question). If the operator wants to stop after phase 1,
the most dangerous findings (E1/E2 — agents double-copying transcripts) are already gone.

---

## Implementation plan (if operator chooses — NOT executed here)

Each phase = its own prompt + branch + commit + verify gate. No phase runs in this audit.

1. **Phase 1 — Truth-up (Option A core).** Edit the three routing-stale blocks + BACKLOG P2 + counts;
   verify routing end-to-end against one real completed debate before deleting "manual archival" language.
   Lowest risk; highest value.
2. **Phase 2 — Staging split (Option B).** After the staging-location decision: relocate the 2026-05-25
   Q-set + evidence + index; update `research/README.md` and inbound references; add the lifecycle runbook;
   promote/supersede the branch-local mechanism doc into `main`.
3. **Phase 3 (optional) — only if volume grows.** Revisit C's manifest/stage-folders if batch frequency or
   transcript volume materially increases. Explicit trigger, not now.

If the operator deems the Phase-2 taxonomy change ADR-worthy (it touches file-taxonomy + the ADR-43 area),
that ADR is authored in its own prompt — this proposal does not draft it.

---

## Open questions for operator

1. **Staging location for question drafts/evidence/indexes** — new top-level `docs/council-questions/`, a
   `docs/research/questions/` subfolder, or a filename-prefix convention inside `research/`? (Drives B/C.)
2. **Is `docs/tech-radar/` actively maintained or dormant?** Only `2026-Q2.md` exists. If dormant, decide
   keep-as-is vs fold its charter into `research/`. (Low-severity; affects scope of any taxonomy pass.)
3. **Stage-2 (inbox copy):** keep it a documented manual step, or add a read-only validator that flags
   un-dispatched/un-archived debates? (No automated cross-repo writes either way — Layer-2.)
4. **Reclassify history or only new artifacts?** Should the 2026-05-25 Q-set and *this audit's* files move
   into a staging area once it exists, or stay where they are as historical record?
5. **ADR for the taxonomy change?** Per the PLAYBOOK Council gate, a folder-semantics change touching the
   file taxonomy may qualify for an ADR (and possibly a small Council/conversational decision). Operator to
   decide whether to formalize or treat as living-doc edits.
6. **Confirm ADR-43 routing actually fires end-to-end** by inspecting one completed debate's routed
   transcript before phase 1 deletes the "manual archival" language. (The 2026-05-26 run was incomplete at
   discovery; verify on the next completed run.)
