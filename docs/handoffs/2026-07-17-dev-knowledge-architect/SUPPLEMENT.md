# Architect strategic supplement — 2026-07-17-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-17

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

ANSWERS — outgoing browser architect (authored by the browser architect;
CC transcribes verbatim). 2026-07-17.

1. STRATEGIC INTENT — Move fleet structural governance from SEEN to
EXPLAINED → ENFORCED → UNATTENDED → REPLICABLE, working ON the census
document of record (docs/audits/2026-07-16-technical-fleet-structure-
census.md), never around it. Operator doctrine, binding: a PASS verdict
without a recorded WHY is not governance — every root-level divergence
(.claude layout, .github, assets, config, каждая) must carry a machine-
readable reason; the consolidated model must then deploy automatically onto
a new repo (correct-by-default scaffold), run unattended nightly, and only
then be optimized. Each repo stays hermetized in its own way of working —
uniformity is never the goal; explained, declared, enforced divergence is.

2. TENSIONS WEIGHED — (a) uniformity vs product-local hermetization: held
DECLARED-WITH-REASON; census category (b) is nearly empty — the discipline
is current. (b) teeth-now vs teeth-after-zero: promotion (#337) stays
pegged on #336, never a date. (c) #336 split-state: mechanism over stamp —
record-stamp rejected as over-claim; schema remodel is the path.
(d) verdict-labels vs operator's WHY-ask: verdicts alone ruled
insufficient; the ownership+reason axis (#316) is elevated to the cycle's
centerpiece. (e) canonical-doc content: stays repo-authored except floor +
Form-A regions (#312); the boundary formalization is #316's file-set grain.
(f) tool caches: on-disk presence is runtime noise (local test runs);
the governed surface is gitignore effect — AT-PARITY fleet-wide; do not
re-open as structural drift.

3. CONSIDERED + REJECTED — record-stamp / full-redeploy / pin-revert for
#336 (over-claims corpus / re-appends the #276-removed hook / discards
#318-#319 uplift) → ticketed remodel instead. Verbatim hub Rule-A carry to
consumers (would brick dev under src/, data/, council_inbox/) → per-repo
sanctioned set DERIVED from the manifest (P2 shape). Ultracode auto-
orchestration for night batches → self-orchestrated Task fan-out per our
own doctrine (explicit shape, haiku walkers / sonnet probes / opus
orchestrator). A dedicated .vscode policy row before the e1 ruling →
generic root-sweep + declared LOCAL with forcing shelf-life. Any greenfield
mechanism → barred; every arc maps to a filed ticket (#306/#316/#324/#336/
#337). Codex --yolo: operator-ruled IN for overnight legs, review/
derivation ONLY, never edit authority — accepted-risk posture, do not
relitigate.

4. OPEN QUESTIONS (operator) — P4a .vscode e1: durable LOCAL vs fleet
template (architect rec: LOCAL; shelf-life 2026-08-13 forces it). P4b
ai-council .claude/skills/ (#308): adopt minimal vs waive (rec: adopt —
FULL-profile consistency). #336 schema shape (separate enforcement-gate-rev
axis) — the design fork inside P1's first arc. Extend #316's Done-when
with a per-entry reason: field (the operator's "answers for everything,
tracked" — recommended: fold it in). Satellite prompts (intake #15) ready,
UNFIRED — operator fires per rollout order. #338/#339 scheduling; W3-13
operator-present. BACKLOG grooming probe: operator wants every open item
verified live / dead / awaiting-ruling at next boot.

5. DECOMPOSITION RATIONALE — serialize around the manifest (both #336 and
#316 touch parity-surfaces.yaml): (1) #336 schema remodel → clears the sole
WARN; (2) #337 promotion to blocking ALL_CHECKS; (3) #316 ownership+REASON
axis (unblocks #329 viz) — the operator's management-system centerpiece;
(4) #306 consumer tree-seal (sanctioned set derived from the enriched
manifest, so it follows #316); (5) #324 nightly runtime LAST — it consumes
everything above into the walk → verdict sheet → morning prompt. P4
rulings slot anywhere. NOT redo / NOT re-decide: the census's divergence
classifications and coverage audit (sol-derived, terra-reviewed); ARC-A/B
declarations + shelf-lives; satellite tier rulings (all FULL); W3-16
no-op closures (fleet is LF — proven); merge/push execution delegation
(PLAYBOOK Ch8); TARGET-REPO guard; ADR-65 grooming discipline (done tasks
leave — the operator has re-confirmed this expectation).

6. OFF-REPO CONTEXT — Operator's strategic ladder, verbatim intent:
explain → consolidate → document → deploy automatically onto other repos →
manage → optimize; the census is the working document for it. Codex
registry healthy (sol 36-point derivation + terra doc-lane both clean on
the census); native codex exec is the working path, .ps1 wrapper halt is
#338(e). Corp product-architect browser chat: payload printed by corp CC,
NOT yet booted — operator's move. CC effort settings persist across
sessions (operator reminded to reset after high-effort night runs).
Operator hard rule (new, 2026-07-16): zero invented filesystem paths —
every emitted path must come from a quoted governance source or be
delegated to CC to derive from primary sources; hyphen-only naming.
