# Architect strategic supplement — 2026-07-17-ai-council-architect-p4-build

Repo: ai-council (bundle hosted in the hub .dev-knowledge) · Mode: architect · Date: 2026-07-17

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next session captures off-repo context live via the §13(d) operator-context beat. The empty file is still committed — a record that this session had no transmissible live "why" (the defined cold-handoff disposition, not a defect). **STATUS: FILLED (2026-07-17)** — the outgoing architect chat answered the interview; the ANSWERS region below is folded into `PASTE_THIS.md` and the incoming §13(d) beat narrows to *"anything changed since?"*

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and why?
3. **Considered + rejected** — which options were rejected and why (so the next session does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the repo.

A. **(CC-observed) Build-wave ordering** — is the frozen #25 → #16 → #26 order fixed, or may the operator open a different lane first given the `output.py` contention (verdict package #26 + `seats[]` #16 both touch it)?
B. **(CC-observed) Codex producer-lane** — confirm the interim fallback (CC-implements + terra review) governs the whole P4 wave, and the hub reconciliation (EPIC-H) is deferred to a separate hub session.

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

ANSWERS — outgoing architect (2026-07-17)

1. STRATEGIC INTENT: Shift the way-of-working from generative planning to build-governance.
   CC produces plan-mode proposals per task; the browser-architect reviews each against the
   frozen plan-of-record (docs/intake/2026-07-16-plan-of-record.md) + seam rules; closure is
   the empirical done-contract (real runs witnessed), never tests-pass. The arc's product
   north star: the delegation window — an external repo invokes the council via CLI/contract
   (ADR-11) and gets a transcript-free verdict package back.

2. TENSIONS WEIGHED: (i) build speed vs record discipline -> record first: G2 consolidation
   preceded any build. (ii) evidence purity vs operator time -> EPI-1 prep decoupled from
   operator scoring; G2 reordered ahead of G3 so a human-time dependency never blocks a
   mechanical unblock. (iii) Codex-producer doctrine vs hub-owned global read-only policy ->
   interim fallback (CC-implements-Codex's-design + terra read-only review); reconciliation
   is the hub's. (iv) workspace taxonomy -> output/ is RESERVED for run artifacts (it is
   also the EPI-1 evidence corpus); homes derive from quoted governance, never inference.
   (v) parallel throughput vs unattended risk -> night work ran serial legs with hard stop
   conditions; the stop fired and was correct.

3. CONSIDERED + REJECTED (do not relitigate): overnight P4 build (seam sequencing requires
   architect plan-review); filing a task for P0 (ADR-65 — done-at-merge tasks don't enter);
   stretching E6 to carry governance (charter dilution -> new E7); retaining both #1/#24
   evidence methods (split truth -> #1 absorbed, ruling recorded); editing ~/.codex/AGENTS.md
   from a consumer session (global infra is hub-owned); resurrecting functional-requirements-
   master (superseded by the intake by design).

4. OPEN QUESTIONS / DEFERRED: G3 — operator blind scoring of the 40-item pack, then the
   Beat-1 mini-session (#24 report + ruling = the Epic-B event). The METHOD is settled and
   sealed — only execution is pending; do not redesign it. Seal disposition at finalization
   already ruled: key + judge second-opinion get committed once un-blinding is recorded.
   Hub-side (separate hub session, not this chat): Codex dual-role mechanism (feedback file
   docs/intake/2026-07-17-hub-feedback-codex-producer-lane.md), EPIC-H doc reconciliation.
   DRAFT-GOV-2 deliberately unratified. #20/#21 remain known pre-existing.

5. DECOMPOSITION RATIONALE: gates-before-phases, because the two real blockers were
   decision-shaped (rulings, evidence ruling), not work-shaped. The phase->task map in the
   plan-of-record is 1:1 — navigate by it, do not re-derive. The task-graph shape is
   CONTENTION-driven as much as dependency-driven: cli.py (A2 decompose + doctor + #22) and
   output.py (A4 + B3 + seats[] + verdict package) are the two serialization points. Do NOT
   redo: the RULED register (15 + fork + scope header), ADR-14, the E7 addition, the
   pre-work mapping, the sidecar seam rule.

6. OFF-REPO CONTEXT: Operator's priority = the delegation window (other repos commissioning
   council debates by CLI command) with CLI-subscription token savings as the economic
   driver (ADR-12; parity #27 is the flip evidence). Operator scoring time is the scarce
   resource — keep it off the critical path. Standing sanctions in force: Codex YOLO
   (danger-full-access on this Windows box, operator owns the risk, sandbox-scoped only);
   zero-invented-paths (every path from quoted governance or delegated derivation);
   night/major session reports persist as audits-class artifacts.

A. BUILD-WAVE ORDERING: #25 -> #16 -> #26 is the recommended default (A2 unblocks the
   cli.py surface; doctor's liveness feeds the seats; the first-landing lane defines the
   sidecar extension mechanism), but it is NOT dogma — the operator may open a parallel
   lane where files are disjoint. Specifically, given the operator's window priority:
   #23 (research --return-dir; research/runner.py) qualifies as an early parallel lane;
   #22 (--file frontmatter; cli.py) must WAIT for A2 to land — same-file contention.
   #26 stays last of the wave (output.py contention + consumes seats[] by reference).

B. CODEX PRODUCER-LANE: Confirmed — the interim fallback (CC implements Codex's design +
   terra read-only review) governs the ENTIRE P4 wave. Hub reconciliation (EPIC-H) is a
   separate hub session. The YOLO sanction covers the sandbox only; the global role policy
   stays hub-owned and untouched.
