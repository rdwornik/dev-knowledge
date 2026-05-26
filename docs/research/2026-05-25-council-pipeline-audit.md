---
type: research-audit
scope: AI Council pipeline + .dev-knowledge docs/ taxonomy
date: 2026-05-25
basis: 2026-05-25-council-pipeline-discovery.md
status: analysis (input to proposal)
---

# AI Council Pipeline + docs/ Taxonomy — Audit 2026-05-25

> Analysis layer. Describes the **current state and its friction points**; it does not prescribe a
> structure (that is the proposal). Every finding cites discovery evidence. Findings are grouped A–G,
> each rated High / Medium / Low with rationale.

## How to read severity

- **High** — actively causes wrong action, lost work, or double-work *now*; or a documented invariant
  is at risk.
- **Medium** — causes confusion / friction / drift that will compound; no acute breakage yet.
- **Low** — cosmetic, sparse, or already-tracked; worth noting, low urgency.

---

## A. Folder taxonomy ambiguity

### A1 — `research/` conflates "research-output archive" with "Council-question staging" — **High**
`docs/research/README.md:4-7` and `PLAYBOOK.md:532,1505` define `research/` as an archive of research
*outputs* (research-mode debates, standalone reports, cross-repo decision transcripts). Yet 7 of its 20
files are a `mode: pick` **question-preparation set** (inputs): `2026-05-25-handoff-council-Q1..Q5`,
`-failures-evidence`, `-methodology-council-index`. Per `PLAYBOOK.md:1504`, a `pick`-mode debate's
transcript belongs in `transcripts/`, not `research/`; and the *questions* have no documented home in
`.dev-knowledge` at all. The operator's own working convention ("all output to `research/`") — under which
even this audit lands here — confirms `research/` is the de-facto catch-all. **Why High:** the input/output
semantics are inverted in the same folder, so neither a reader nor an agent can tell from the folder what a
file *is* (a finished artifact vs an in-flight input) — the operator's stated "input vs output vs working vs
archived is ambiguous" frustration, localized to concrete files.

### A2 — No designated home for Stage-0/1 working artifacts — **Medium**
Question drafts, evidence files, and question-set indexes are pipeline *working* artifacts with a lifecycle
(draft → dispatched → superseded-by-transcript). Nothing in the taxonomy names a "working / staging" area,
so they land in `research/` (A1) or wherever convenient. **Why Medium:** drives A1; on its own it is a gap,
not a breakage.

### A3 — `transcripts/` vs `research/` split is documented but bisects one debate's artifacts — **Low**
`PLAYBOOK.md:575,1504-1506` routes `pick` transcripts to `transcripts/` and `research`-mode outputs to
`research/`. For a single decision the *question* (research/) and the *transcript* (transcripts/) and the
*ADR* (decisions/) live in three folders with no shared key linking them except the traceability table in
`decisions/README.md`. **Why Low:** documented and traceable, just dispersed.

---

## B. Pipeline lifecycle fragmentation

### B1 — Pipeline spans 2 repos and ≥4 folders with two manual hops — **Medium**
Lifecycle (discovery Part 4): `research/` (Q draft) → `ai-council/council_inbox/` (manual copy) →
`ai-council/output/` + routed `transcripts/` (auto) → `decisions/` (ADR). Manual hops: **Stage 2**
(copy into inbox + run) and **Stage 6** (author ADR). **Why Medium:** the manual copy is a real cross-repo
action an agent must know to perform; it is documented in the guide but not in a single `.dev-knowledge`
pipeline runbook.

### B2 — No single "pipeline state" view (Q9) — **Medium**
There is no manifest. In-flight vs done is implicit in folder membership (`council_inbox/*` pending,
`council_inbox/archive/*` done, `output/*` transcripts). The `-council-index.md` indexes the *question set*,
not pipeline status. **Why Medium:** for a 5-question batch this is survivable by `ls`; it scales poorly and
gives no completion signal (see B3).

### B3 — No completion signal (Q8); a run can silently stall — **Medium**
Invocation is synchronous with no job-id/notification; completion is inferred from archived inputs + emitted
transcripts + the `_inbox-run-*.log`. Discovery captured the 2026-05-26 run **mid-round-2 with inputs still
unarchived and zero transcripts emitted** — i.e. exactly the state an operator cannot distinguish from
"still running" without reading the log. **Why Medium:** observable, but only by manual log inspection;
no structural signal. (Not diagnosed here — read-only, topic deferred.)

---

## C. Naming convention gaps

### C1 — `research/` filename patterns are heterogeneous and role-blind — **Medium**
`research/` mixes `YYYY-MM-DD-council-NN-slug-REPO.md`, `YYYY-MM-DD-slug.md`, and
`YYYY-MM-DD-handoff-council-QN-slug.md`. The filename does not encode whether a file is an *output* (archive)
or an *input* (question). **Why Medium:** compounds A1 — you cannot sort inputs from outputs by name either.

### C2 — `output/` transcript naming drifted across eras — **Low**
`ai-council/output/` shows `YYYYMMDD_HHMMSS_slug.md`, `council_out_…`, and `council-out-…` variants;
routed copies use the canonical `council-out-YYYYMMDD-HHMMSS-slug.md`. **Why Low:** historical, gitignored,
canonical routed name is consistent; cosmetic.

### C3 — "Section 5 / 5.N" PLAYBOOK references are imprecise — **Low**
`decisions/README.md:103`, `PLAYBOOK.md:529,824,826,843` cite "PLAYBOOK Section 5 / 5.N", but PLAYBOOK
sections are unnumbered `##` headings; the targets resolve by *name* ("Council Debate Archival Protocol"
`:1494`; "When to run Council…" `:1543`). The numbering mismatch was already flagged in
`docs/audits/2026-04-27-deep-cleansing-diagnostic.md:66-68,80`. **Why Low:** resolvable by name; already known.

---

## D. Cross-repo dependencies

### D1 — Stage 2 requires a physical write into ai-council's working tree — **Medium**
An agent working from `.dev-knowledge` must copy `Q*.md` into `ai-council/council_inbox/`. The dir is
gitignored (no tracked-content violation), but it is still a write into the *other* repo, and the prompt for
this very audit forbids writing to ai-council — illustrating how easily that boundary is misread. **Why
Medium:** the read-only-*content* contract holds, but "may I write into ai-council at all?" is genuinely
ambiguous without the gitignore nuance spelled out in a runbook (it currently lives only in the branch-local
mechanism doc, see E3).

### D2 — Routing depends on ai-council `settings.yaml` naming `.dev-knowledge` — **Low**
Transcript routing only fires because `settings.yaml target_projects` contains `.dev-knowledge` and
`dev_root` resolves locally. A rename or relocation of `.dev-knowledge` silently breaks routing (mirror
writes are best-effort — failure only logs a warning). **Why Low:** stable today; single config line; failure
is non-fatal to the canonical write.

---

## E. Documentation vs reality gaps

### E1 — Transcript routing documented as "pending/manual" in `.dev-knowledge`, but it is implemented — **High**
The **central finding.** ADR-43 (2026-05-11) decided cross-project routing, and ai-council implements it
(`ARCHITECTURE.md:136-150`, `README.md:238-288`, `council-question-guide.md:54-83`, `routing.py`
`TargetResolver`, `settings.yaml target_projects:[.dev-knowledge]`). The 5 live Q-files carry
`target-project: .dev-knowledge`. Yet **three** `.dev-knowledge` governance locations still tell the agent
routing does not exist:
- `PLAYBOOK.md:1499` — "Cross-project routing as a CLI feature is pending."
- `PLAYBOOK.md:1526-1541` "Council output convention (current state)" — "emits to `ai-council/output/` only…
  populated by **manual archival**… pending."
- `docs/decisions/README.md:95-104` — "manual archival copies… Cross-project routing… is pending."

**Why High:** an agent following PLAYBOOK/README will *manually copy* transcripts that the CLI already routes
automatically — producing duplicate files or clobbering routed ones, and wasting a documented "~5 min × every
debate" step. It is the single highest-leverage correction in this audit. (Note: ADR-43 sits in the same ADR
index as the stale note — the README contradicts its own index.)

### E2 — BACKLOG `[P2][open]` for routing is effectively done by ADR-43 — **High**
`BACKLOG.md:81-86` carries "AI Council cross-project transcript routing" as **open**, describing the feature
as not-yet-implemented and even noting it was "restored 2026-05-24" because PLAYBOOK §5 referenced it. ADR-43
+ shipped `routing.py` indicate the core capability exists. **Why High:** an open P2 backlog item for shipped
work mis-routes future effort and corroborates E1's staleness; pairs with E1 as the same root divergence.

### E3 — Resolved mechanism knowledge is branch-local, not in `main` — **Medium**
`2026-05-25-council-mechanism-discovery.md` (the doc that resolved Q1–Q7 and the gitignore nuance behind D1)
exists only on `chore/council-debate-execution-2026-05-25-handoff-methodology`. A reader on `main` re-derives
the mechanism from scratch. **Why Medium:** valuable knowledge exists but is invisible on the default branch.

### E4 — Stale transcript counts — **Low**
`PLAYBOOK.md:1533` "12 transcripts", `decisions/README.md:49,101` "12"/"14"; actual `transcripts/` count is
**22**. **Why Low:** cosmetic, but a symptom of the same un-updated blocks as E1.

---

## F. Layer-2 invariant compliance

### F1 — No orchestration scripts in `.dev-knowledge/scripts/` — **compliant (no finding)**
`scripts/` = `audit.py` (ADR-36 read-only auditor), `codemap/` (generator), `migrate_links.py`,
`normalize_headers.py` — validators / local-file utilities operating on `.dev-knowledge`'s own tree. None
drive child-repo state. Consistent with `CLAUDE.md §5 rule 4`. (`audit.py` read-only-ness taken from
ADR-36/CLAUDE.md, not re-read this session — discovery Gap 2.)

### F2 — Pipeline writes cross repo boundaries in both directions — **Low (watch)**
Layer-2→3 push (Stage 2 inbox copy, into gitignored dir) and Layer-3→2 routing (ai-council writes
transcripts into `.dev-knowledge`). Neither makes `.dev-knowledge` *execute*, so the "Layer 2 never executes"
invariant holds; but the bidirectional file flow is worth stating explicitly because it is easy to mistake
for a violation. **Why Low:** invariant intact; documentation clarity only.

---

## G. Friction points (operator-observed, grounded)

The operator reported: folder semantics ambiguous (input vs output vs working vs archived); Council files
scattered; hard to reason about the lifecycle holistically. Grounded against evidence:

| Operator frustration | Grounded in | Severity |
|----------------------|-------------|----------|
| "input vs output vs working vs archived ambiguous" | A1 (research/ holds both inputs and outputs), A2 (no working area), C1 (names don't encode role) | High |
| "Council pipeline files scattered" | B1 (2 repos, ≥4 folders), A3 (one debate split across 3 folders), E3 (mechanism doc branch-local) | Medium |
| "hard to reason about lifecycle holistically" | B2 (no state view), B3 (no completion signal), E1/E2 (docs contradict reality so the mental model is wrong) | High |

The sharpest contributor to "hard to reason holistically" is **E1**: the operator's own governance docs
describe a *manual* pipeline while the tool runs an *automatic* one — so the documented mental model and the
real behavior diverge at the busiest stage.

---

## Severity classification (summary)

| ID | Finding | Category | Severity |
|----|---------|----------|----------|
| E1 | Routing documented "pending/manual" but implemented (3 locations) | Doc vs reality | **High** |
| E2 | BACKLOG P2 routing item open for shipped work | Doc vs reality | **High** |
| A1 | `research/` conflates outputs + question-staging inputs | Taxonomy | **High** |
| G | "Lifecycle hard to reason about" rooted in E1 + B2/B3 | Friction | **High** |
| A2 | No designated working/staging area | Taxonomy | Medium |
| B1 | Pipeline spans 2 repos / ≥4 folders, 2 manual hops | Fragmentation | Medium |
| B2 | No pipeline state manifest | Fragmentation | Medium |
| B3 | No run completion signal | Fragmentation | Medium |
| C1 | `research/` names don't encode input/output role | Naming | Medium |
| D1 | Stage-2 write into ai-council tree (gitignored) is boundary-ambiguous | Cross-repo | Medium |
| E3 | Mechanism doc branch-local, absent from `main` | Doc vs reality | Medium |
| A3 | One debate's artifacts split across 3 folders | Taxonomy | Low |
| C2 | `output/` historical name drift | Naming | Low |
| C3 | "Section 5 / 5.N" references imprecise | Naming | Low |
| D2 | Routing depends on settings.yaml naming | Cross-repo | Low |
| E4 | Stale transcript counts (12/14 vs 22) | Doc vs reality | Low |
| F1 | scripts/ orchestration-free | Layer-2 | compliant |
| F2 | Bidirectional cross-repo file flow | Layer-2 | Low (watch) |

**Distribution:** High ×4, Medium ×7, Low ×6, compliant ×1.

**Root-cause clustering:** the four High findings reduce to two roots — (1) **E1/E2**: ADR-43's
implementation never propagated back into `.dev-knowledge`'s governance docs/backlog (a *staleness* root);
(2) **A1/G**: `research/` has no input/output/working distinction (a *taxonomy* root). The proposal addresses
these two roots first.
