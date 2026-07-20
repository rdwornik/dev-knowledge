# Architect strategic supplement — 2026-07-20-ai-council-architect

Repo: ai-council · Mode: architect · Date: 2026-07-20

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
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================

SUPPLEMENT ANSWERS — outgoing ai-council architect (2026-07-20); CC transcribes VERBATIM

STRATEGIC INTENT (way-of-working level): the failure this repo keeps paying for is "decision
recorded ≠ decision enforced ≠ decision legible." This window converted three silent failures into
mechanisms — a checker per contract, a composed cross-lane witness, two armed pre-commit guards —
so "merged" can no longer be reported as "deployed." The next session finishes the legibility half:
T1 de-bias, deferred for a FOURTH consecutive window with zero code, is the standing debt and must
land plan-AND-build in one session, not another design document. NOTE ON SCOPE: this window shipped
output-contract BEHAVIOUR (27a45d1..eabd962, pushed). It did NOT touch the Python/tooling stack,
assets/, or mypy — that is ARC 5 / hub-side, a different repo. If the live pain is stack config, the
next session is ARC 5, not another ai-council window.

TENSIONS WEIGHED:
(a) Raise-at-source vs record-and-aggregate. Landed: aggregate. Raising inside the writer aborted
    the orchestrator before the minority report and verdict package were written CANONICALLY —
    silent failure traded for data loss. All three debate writers share return_dir (common-mode),
    so the orchestrator raises once after all canonical writes complete.
(b) Merge order A2→A1→C — load-bearing. A1 adds raises in the writer layer; cli.py:799 had NO
    handler on original main, so A1-first turns a silent exit 0 into a raw traceback. A2 first
    closed that window and, per Finding 2, fixed a live pre-existing verdict-package traceback on
    its own.
(c) #66 witness: $0 offline vs billed. Landed: honest GAP, no spend — no first-class codex seat, so
    a live witness bills; CC refused rather than fake a PASS. #66 now gated on #27's ADR-12 §5 flip.
(d) doctor in Contract A: output resolution IN, probe surface OUT (#32's), or a lane drifts into #32.

CONSIDERED + REJECTED (do not relitigate):
- Coupling Contract A to #34's 1.1 bump — rejected: A is a COMPLIANCE fix (ADR-10/R4 already
  promises fail-loud; precedent #39, no §2 entry), forces no bump. #34 keeps 1.1, versions with #76.
- One epic for the silent-failure trio — rejected: split into two contracts on the file surface
  (output-routing vs panel-resolution); a combined acceptance contract stops being checkable.
- #68 as a blanket docs/ ban — rejected: would reject archive/ and both registered corpora. Built
  as a registry check.
- F8 "restrict the scan" fix — rejected: a Risks-only document makes that heading the FIRST match
  too, so narrowing leaves the defect. Dropped the bare "considered" marker instead.

OPEN QUESTIONS / DEFERRED:
- #27 Phase 3 blind scoring: 0/12, untouched. THE highest-leverage item, the one objective function
  of five that missed. Non-delegable, one operator sitting, 60 binary cells. Gates the ADR-12 §5
  flip → #41 → #66.
- Lane B (#69 panel parity + #64 frontmatter robustness): never ran, deferred on cli.py
  serialization. cli.py is now free — cheapest next arc.
- #77 (options_considered extraction contract): CORRUPTED ON MAIN TODAY via F6/F7, latent only
  because nothing consumes the verdict package yet. MUST land before the caller-side advisor
  [S13]/#36–#38 ships.
- #75, #76 (1.1 with #34), #78, #79 filed, out of window.

DECOMPOSITION RATIONALE: split by FILE SURFACE, not ticket. cli.py was contended (A-ii and B → serial);
output.py + guards disjoint → parallel. The lesson that cost a RED main: file-disjointness is NOT
contract-disjointness — A1 changed OutputRoutingError's constructor, A2's fixtures hardcoded the old
signature, zero shared files, real coupling. STANDING RULE: before splitting lanes, list each lane's
changed PUBLIC SIGNATURES and grep the others. DO NOT REDO: the A2→A1→C order, the two-contract
split, the #68 registry-check design, the F8 marker-drop, the 1.0 stamp holding (compliance, not ABI).

OFF-REPO CONTEXT: operator's live frustration is that 8 hours produced no visible STACK/TOOLING
result — root cause is scope: this was the output-contract window, the Python/stack/assets/mypy work
is ARC 5 / hub-side, a different handoff and repo. Educate every close with file-level before→after
the operator can run (git log 27a45d1..eabd962; check.ps1), never ticket names. HUB PACKET for Rob to
route, none actionable from an ai-council chat: (1) Tier-1 /review-closures is structurally stale
(proposals written at session START → same-session deliveries classify WEAK); (2) codex-review.ps1
summary regex misses '### [HIGH]' — CONSOLE-ONLY, no committed audit is wrong, one one-line fix in
operator-owned tooling; (3) provisioner branch-naming vs CLAUDE.md §4; (4) #341 and #344 unruled.
Prove-by-reversion footgun: commit the fix BEFORE reverting, or git checkout -- <file> destroys
uncommitted work.
