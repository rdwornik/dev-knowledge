# Architect strategic supplement — 2026-08-08-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-08

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

SUPPLEMENT ANSWERS — authored by the outgoing architect (browser seat), per the
supplement-authorship rule (HANDOFF_PROCESS 6.1.0). CC: insert unchanged.

A1 · STRATEGIC INTENT. Spend the machinery on the North Star instead of on
itself. This window built and drilled the parallel execution system (Ch8 +
commands + manifest + R-1 + dispatch visibility); the next session's
way-of-working goal is the first FEATURE-MAJORITY batch — wave-2 satellites
under the encoded protocol — with the browser operating purely as architect
(decisions, contracts, model/effort advisory) and zero methodology recalled
from chat. Secondary: make second-seat verification a standing batch citizen
rather than a bespoke arc; it out-caught every author this window.

A2 · TENSIONS WEIGHED. Speed vs verification → second seat institutionalized
(author + author's-test shared a blind spot 4× measured; a different seat
caught every one). Width vs operator saturation → batch-2 closed at 3; width
follows the operator's Needs-input capacity, never machine capacity. Ceremony
vs safety → V-3 tiering stands, but JOURNAL anchoring proved to be a HARD
GATE, not ceremony (an S-trim dropping it cost a reset). Cloud-unattended vs
control → cloud runs own-branch with disclosed structural SKIPs; bundle CUTS
are local-only because a cut binds git state. Prose vs mechanism → every
prose rule that mattered failed at least once where no mechanism stood
(win-tooling merge word; the boot file feeding retired doctrine); landed on
mechanism-first, prose as commentary.

A3 · CONSIDERED + REJECTED (do not relitigate). Vibe Kanban — measured FAIL
(webview UI, blind to dot-prefixed dirs). SARIF for review artifacts — real
standard, wrong size; the live gap is producer discipline (13/122 artifacts
carry a Tally line). Probe-gate parallelization — refuted by measurement (one
probe is 19.47s of 22.58s; cap ≈1.2×). Sonnet for repo-touching arcs —
measured ~3h on a shape-S arc; tier keys on context load. Per-repo
bgIsolation weakening — rejected (F6: guard stays, patch-script route).
History surgery on the win-tooling merge — the reflog proved the defect
didn't exist; verify-before-destroy is now F1. In-place edits of committed
audits/JOURNAL/ADRs — append/amendment only (B6, R-2 precedent). Cutting the
bundle in the cloud — would bind stale git state and break the successor's
P3.

A4 · OPEN QUESTIONS (deliberate). [#502] import convention (sys.path vs
src-layout/pythonpath — shapes and costs in the research memo; architect
decision). [#511] fork — which bought property, if any, to trade; the morning
cut's measured timeline is the decisive input. serialize-group audit-py is 50
ids wide (26% of the open set) — lawful concurrency needs a label ruling.
[#430](b) — deferred WITH direction: subject-scoped severity over pinned
snapshots (ADR input). uv pinning strategy — three organs silenced in one
cloud night, one failing OPEN unbidden; mise (ledger 36) carries the
divergence question. PENDING OPERATOR RATIFICATION: 3.2 (cap evaluated on
dispatched width) · 3.3 ([#505] clause-2 per-seam wording) · win-tooling
remote (14 local-only branches, one disk). v4 template consumer set
unverified. W-wave awaits intake #25 acceptance + births.

A5 · DECOMPOSITION RATIONALE / DO-NOT-REDO. The batch protocol is repo law —
never re-derive it from chat. Batch-2 closed HONESTLY at width 3; wave-2
([#283] [#416] [#393]) is pre-checked and CARRIED — cut it, don't re-plan it,
and mind the serialized pair. [#506] owns whole-set grooming (189/200 since
2026-07-31) — run it as its arc, don't ad-hoc it. STANDING_RULINGS D–F and
intake #27 §B are settled. The successor's boot surface is the prep pack +
staging doc + this bundle — pointers into law, not restatements.

A6 · OFF-REPO CONTEXT. The operator's trust posture is
verification-before-scale: control is exactly as thick as the organs — hub
held everything, win-tooling (no organs) lost its merge word day one;
satellites get organs or [#429]-class guarantees before wide batches. The
Agent View dashboard is the operator's management surface (labels must
survive row titles — truncation observed). The operator saturates before the
machine — design every interaction to Needs-input capacity. Handoff cost is
authoring, not machinery (4.5s vs ~30min) — thinning + staging are the
levers, measured this morning.

A7 · RATIFIED-IN-CHAT, NOT YET IN THE REPO (F5 sweep — each with its durable
home): (a) "cap evaluated on DISPATCHED width, close-delta reported" —
architect-recommended, operator ratification pending → intake #27 amendment +
Ch8. (b) "[#505] clause 2 = two numbers, per-seam and per-batch" — same
status → [#505] row + Ch8. (c) "ADR-87 population boundary: architect states
the session's boot tier; CC routes sub-steps inside it" — RATIFIED; the
descriptive ADR-87 amendment is authorized and unlanded → ADR-87 amendment §.
(d) "immutable bundle with a defective seal retires via an external dated
marker/exclusion, never an edit" — ruled direction; row deferred to the next
batch's first closes → row + register line. (e) win-tooling remote decision —
operator's, pending → win-tooling S-list. Everything else ruled this window
already carries a repo locator (STANDING_RULINGS D–F, ADR-110 amendments,
F5's own [#430a] entry).OPERATOR RATIFIED: 3.2 YES · 3.3 YES · win-tooling: private-remote

