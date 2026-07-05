# EPIC HANDOFF — llm-first-docs · 2026-07-05
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | 2026-07-05-dev-knowledge-epic-llm-first-docs |
| **Mode** | **epic** — one epic end-to-end, inside a root-provisioned worktree (ADR-97; HANDOFF_PROCESS §14a) |
| **Repo** | .dev-knowledge |
| **Date** | 2026-07-05 |
| **Epic branch** | `epic/llm-first-docs` (root-provisioned; bundle generated on `docs/2026-07-05-wave2-prep`) |

## Boot (epic lane)

You are an **EPIC-CHAT lane** (HANDOFF_PROCESS §14a; ADR-97). The root architect owns ADR
acceptance, backlog structure, parallelism rulings, and ALL merges to main. On load reply:
"Epic lane llm-first-docs booted — worktree + boundary acknowledged."

## Worktree + branch

Worktree `epic-llm-first-docs` (root-provisioned — never self-provisioned) · branch
`epic/llm-first-docs`. **RELATIVE PATHS ONLY** (the absolute-path-bypasses-worktree lesson is a
hard rule). Commit-per-story; **commit-and-STOP** — no merges to main.

## Epic scope (the BACKLOG slice)
<!-- FILL-IN:scope START — ROOT authors: epic id · stories in order · done-when per story -->
Epic id **[#259]** (BACKLOG · Canonical-file integrity · "Epic 4 — LLM-first canonical docs"). Stories in order:

1. **S1 — ADR-51 amendment**: canonical root docs are LLM-first; Mermaid leaves canonical docs; visualization is a separate human-facing surface (future Tier-4). Done when: the amendment is authored under `docs/decisions/` (amendment file, per §5 immutability — never edit ADR-51 in place) and internally coherent with S2/S3.
2. **S2 — ARCHITECTURE codemap Mermaid → compact text form**: dependency list + the existing tables; **no information loss** — the graphs are redundant with the tables. Done when: hub `ARCHITECTURE.md` renders zero Mermaid and carries the same dependency facts in text form.
3. **S3 — retire/replace audit check #7** (Mermaid theme) coherently with the amendment. **NARROW GRANT**: check #7 ONLY — no other `audit.py` surface. Done when: no audit check asserts a claim the amendment retired, with tests updated in kind.
4. **S4 — template updated**: `templates/ARCHITECTURE-template.md` reflects the LLM-first form. Done when: a new repo scaffolded from the template carries no Mermaid codemap.
<!-- FILL-IN:scope END -->

## Epic done-contract (ex-ante, immutable to this lane)
<!-- FILL-IN:done-contract START — the hard closure metric for the WHOLE epic -->
Hub `ARCHITECTURE.md` renders **zero Mermaid**, carries the **same dependency facts in text form** (no information loss), audit checks coherent with the amendment, gates green on branch. Closure is claimed on this metric — never on "docs edited" or "committed".
<!-- FILL-IN:done-contract END -->

## FILE-BOUNDARY (hard)
<!-- FILL-IN:boundary START — may-touch / may-NOT-touch; disjoint from every concurrent epic -->
**May touch:** `ARCHITECTURE.md` · `templates/ARCHITECTURE-template.md` · `scripts/audit.py` (**NARROW GRANT: check #7 Mermaid-theme retire/replace ONLY**) · `docs/decisions/` (the new ADR-51 amendment) · own BACKLOG block ([#259] checkboxes only) · `JOURNAL.md` (append).
**May NOT touch:** `protocols/**` · `deploy/**` · `ecosystem/doc-counts.md` (**FORBIDDEN** — the root regenerates it once at integration).
A needed file outside the boundary → STOP, escalate — don't touch. 3 lanes = the ADR-97 cap ceiling — this lane spawns no sub-work outside its worktree.
<!-- FILL-IN:boundary END -->

## Escalation
<!-- FILL-IN:escalation START — epic-specific triggers beyond the standing set -->
Epic-specific: (1) any `audit.py` change beyond check #7 (another check's contract, shared helpers whose edit ripples into other checks) → STOP, return to root; (2) an ARCHITECTURE edit that would drop a dependency FACT (not just its Mermaid rendering) → escalate — the no-information-loss clause is load-bearing; (3) Mermaid found in a canonical doc OUTSIDE the boundary (e.g. protocols/) → list in the EPIC RETURN, do not chase. Standing set (always): ADR-worthy fork · boundary-breach need · cross-epic dependency discovered → STOP, return to the root. Everything intra-epic is the lane's own judgment.
<!-- FILL-IN:escalation END -->

## Refusals (standing — not editable by the lane)

No merge to main · no ADRs · no backlog structure (checkboxes inside this epic's own block
only) · no worktree lifecycle ops · no new top-level folders · no content deletion without
operator ask.

## EPIC RETURN (required before any merge)

Close the lane by filling `EPIC_RETURN.md` in this bundle (§14b): commits + branch state ·
contract-vs-outcome per story · self-adjudications · proposed BACKLOG delta ·
merge-readiness. The root reviews the return against this contract → serial `--no-ff` merge →
applies the backlog delta → declares closure → tears down the worktree.

## Probes

Boot on `PROBES.md` (this bundle) — live-state probes scoped to this epic's boundary
(HANDOFF_PROCESS §5 contract: question + source-locator + command, **never the answer**).

> **Operator note.** Paste THIS file + `PROBES.md` into the fresh epic chat. Epic mode
> assembles no `PASTE_THIS.md` — the v5 paste manifest is architect/execution-shaped
> (requires `RESIDUAL.md`); the EPIC_BOOT scope-contract IS the paste.
