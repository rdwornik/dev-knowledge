# Architect strategic supplement — 2026-09-08-dev-knowledge-architect-2

Repo: .dev-knowledge · Mode: architect · Date: 2026-09-08

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
6. **Off-repo context — changed INTENT only.** Intent, priorities and decisions that moved
   this window and are not in the repo. **Not** the operator's interface mechanics — file
   exchange through Downloads, `.md` uploads because a large inline paste arrives empty,
   shipping the exact start command, reports travelling as files. Those are constants, they
   live at `protocols/OPERATOR-INTERFACE.md`, and the incoming bundle's forms card already
   carries them; one of them being wrong is a defect report about that file, not an answer
   here.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo, **and interface BEHAVIORS you relied on that
   are not yet named in `protocols/OPERATOR-INTERFACE.md`** — e.g. a copy-ready block
   substituting for a described action, a paste arriving as a `.md` upload rather than inline
   text, reliance on the `PASTE_THIS.md` END sentinel to detect a truncated paste, or a
   Downloads-directory fallback for file exchange. For either kind: the verbatim term/behavior ·
   a one-line definition (or what relying on it looked like) · its intended durable home
   (BACKLOG id / ADR / LESSONS / PLAYBOOK §, or `OPERATOR-INTERFACE.md` for an interface
   behavior). "None" is a valid answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

_Answers transcribed VERBATIM from `to-cc/SUPPLEMENT-ANSWERS-2026-09-07.md`; the seven `Files:` lines appended VERBATIM from `to-cc/SUPPLEMENT-ANSWERS-CITATIONS-2026-09-08.md` (browser-authored). No answer text was edited, reflowed or re-cited._

# SUPPLEMENT — ANSWERS from the browser architect (window 2026-09-06 → 2026-09-07) — authored by the browser; the handoff seat transcribes VERBATIM
<!-- reads: DECLARE-SITTING, DECLARE-F, DECLARE-F-2, DECLARE-GRAPH, DECLARE-REVIEWS, AMEND-NIGHT-2-001, INBOX 033–036, REVIEW-*-redteam headlines, integrator-N3 report 21:58 · SHA-cited where witnessed; OPINION marked -->

## Q1 · Strategic intent for the next session (way of working)
Stop adding organs; make the existing ones one system. Three moves, in order: (1) the repo graph (FPG-1) becomes the single source for corpus-structure edges and `orphan_census` is its first query; (2) every rule that failed in batches T/U becomes a REFUSAL in a seat template or a launcher (sleeping poll, lane ceiling 4–6, `reads: path@sha` + PLAN/INFORMATION head, reviewer model in the tally, receipt = commit), so no seat can repeat this window's failures; (3) batch size ≤ 6, one sitting per browser window, decisions only as files. Measure by: substantive-commit share (was ≈ 10 %), human points on the critical path (was 14), orphans (count), tokens per window (browser ≤ 10 Fable turns).

Q1 — Files: to-cc/INBOX-dev-knowledge-2026-09-07-036.md · to-cc/DECLARE-REVIEWS-2026-09-07.md §C · docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md

## Q2 · Tensions weighed — where I landed
- Speed vs ceiling: I ran 15 and 19 lanes; merges cost 9–28 s but every coordination failure scaled with lane count (dispatcher turn-end on wait, superseded integrator, reaped sessions, destroyed handback). Landed: ≤ 6, mechanisms first.
- Graph as engine vs graph as view: the architecture review proved two-tree gates cannot be views and that Z-C3 stands. Landed: FPG-1 for corpus edges only; state gates stay gates; graph computed by the hub over consumer trees read-only (not shipped as a pull component — a consumer of identical shape yields an empty graph).
- Push vs pull carrier (ADR-117): landed on the divergence discriminator; flip-condition recorded ([#616]).
- Browser: two chats vs one: landed one chat, model per act, tags on every reply, ≤ 40 turns.
- LLM in the data structure: landed as METHODS with recorded outputs (`describe()`, `evaluate()` on the grey zone), never as the judge on a gate's hot path.
- Pre-handoff hygiene: landed as preflight ROWS (mechanism), not a checklist the operator invents each time — see Q7.

Q2 — Files: to-cc/DECLARE-REVIEWS-2026-09-07.md §A · to-cc/DECLARE-GRAPH-2026-09-07.md · docs/decisions/ADR-117*.md · to-cc/DECLARE-BROWSER-TOPOLOGY-2026-09-06.md · to-cc/INBOX-dev-knowledge-2026-09-07-035.md

## Q3 · Considered + rejected (do not relitigate)
Second browser chat (synchronisation cost, no token gain) · URL-management engine (identity = id, layout identical → resolver is a dictionary) · an LLM instance in every node · hub-only graph · graph shipped as a pull component · Rust/C# for gates (measured) · multiplayer/ADE · reminder hooks that re-argue rules · HTML companions per artifact · judged score beside mechanical (deferred) · ruling 336 seal waivers by hand (fix the two hub-local rules first) · codespace as producer substrate until receipt = commit · pasting CC transcripts into the browser.

Q3 — Files: to-cc/DECLARE-F-2-2026-09-07.md §C · to-cc/DECLARE-REVIEWS-2026-09-07.md §A.4 · to-cc/INBOX-dev-knowledge-2026-09-06-032.md · docs/audits/2026-09-05-technical-research-python-quality-speed.md

## Q4 · Open questions (deferred deliberately)
ADR-85 amendment (spine anchor from merge commit, WARN at commit) — operator ruling · the 2026-08-29 deploy freeze — never ruled, blocks H0 step 4 · which of the 24 hooks / 56 checks retire (S-10 census supplies zero-true-finding organs) · #75 offload admission (Enterprise) · #76 one-chat topology · MEMORY.md drop list · the two seal-rule fixes before any consumer ruling · what the interface review §5 says about the browser's cost (unread in full).

Q4 — Files: to-browser/RATIFICATION-2026-09-08.md · to-browser/QUESTION-handoff-cut-2026-09-08.md §3 · to-browser/REVIEW-2026-09-07-architecture-redteam.md (R-1) · to-browser/REVIEW-2026-09-07-plan-redteam.md (deploy freeze)

## Q5 · Decomposition rationale — do not redo
Batches T and U are CLOSED on the hard metric (packet on main after integrator-N3 lands it). Do not re-run: NC1 clearing, freshness stamps, README, PLAYBOOK re-read, seal report (fleet), shape spec, ADR-117, deploy-tool override, plugin drift, ADR template (Flip-condition + Alternatives REQUIRED), handoff v7.1 build, 13 censuses. The 5 human decisions stay human (GO, ratification, tag, destructive acts on live seats, seat release); everything else in 036 wave 2 is mechanism work.

Q5 — Files: docs/audits/2026-09-07-technical-batch-u-close-packet.md · docs/audits/2026-09-06-technical-batch-t-close-packet.md · to-cc/DECLARE-SITTING-2026-09-06.md · to-cc/INBOX-dev-knowledge-2026-09-07-036.md §Operator's five

## Q6 · Off-repo context — changed INTENT only
Operator's word this window: identical layout everywhere (shape, not content) — waivers are exceptions with a reason, not a way of life; universalization by mechanism; think-before-act as the browser's fixed order (033); "cook and clean" — every batch carries hygiene; the fleet is "a new programming paradigm": classic data structures and patterns are the skeleton, models complement them; he wants Enterprise tokens used ($90, product unidentified) and Gemini used as a reader; he leaves at night and wants ≥ 12-lane unattended batches — now bounded by the 4–6 ceiling per batch, so "unattended" means several small batches chained by files, not one large one.

Q6 — Files: to-cc/INBOX-dev-knowledge-2026-09-05-023.md · to-cc/INBOX-dev-knowledge-2026-09-07-033.md · to-cc/DECLARE-GO-2026-09-06.md · to-cc/INBOX-dev-knowledge-2026-09-07-035.md (paradigm) · docs/intake/…offload (#75)

## Q7 · Ratified-in-chat register (not yet in the repo unless noted)
- THINK-BEFORE-ACT order (033) → OPERATOR-INTERFACE §2 + floor item 7 (filed; not landed).
- Model tag on every browser reply (ROUTINE / RULING AHEAD with cost) → same (DECLARE-BROWSER-TOPOLOGY; not landed).
- Decisions are files with a `carried-by:` line; P11 probe → v7.1 (W1-9 landed P11; `carried-by:` fill owed by filings).
- Lane ceiling 4–6 enforced at dispatcher step 0 → PLAYBOOK Ch8 (not landed).
- No seat ends a turn on a peer wait; file is the only coordination primitive → PLAYBOOK Ch8 "Batch communication" (section landed via 30c6e587; the poll-as-code not landed).
- Reviewer model name in the tally; mismatch = review=NONE → PLAYBOOK Ch8 (not landed).
- "A cited SHA is checked, not inherited"; "a clean tree is not a stop signal"; "destroyed, not withheld" (a reaper destroying a handback channel) → LESSONS (JOURNAL (r) landed).
- Pre-handoff hygiene = preflight rows: ship-gate 0/0 or dispositioned · LEDGER refreshed · RATIFICATION current · STATUS ≤ 5 KB archived · living docs stamped · JOURNAL anchored · QUESTION files answered or carried · MEMORY.md within cap · no worktree without a live owner → `/handoff` preflight (CLOSE batch lane).
- Interface behaviours relied on: `.md` uploads for anything > a screen; the END sentinel; Drive connector for browser writes (rename-then-create to overwrite); the daemon's env block as the real source of `CLAUDE_PROMPTS_DIR` (E-29) → OPERATOR-INTERFACE §1.

Q7 — Files: as already cited in the answer (OPERATOR-INTERFACE §1/§2 · protocols/HANDOFF_BOOT.md floor · PLAYBOOK Ch8 "Batch communication" · JOURNAL.md (r) · .claude/commands/handoff.md preflight)

=== END OF SUPPLEMENT ANSWERS ===
