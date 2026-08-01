# Architect strategic supplement — 2026-08-01-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-01

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

Q1 STRATEGIC INTENT (way-of-working, not a task). Institutionalize "mechanism over
vigilance". This window's proof: three defects written by the builder were caught by three
different organs (per-step gate, terra review, session-end SHA anchor) and ZERO by re-reading
code. The next session's methodology goal: convert this window's chat-ratified lessons (Q7)
into enforced or recorded form, and treat §F net-negative as a standing property of every
window — closes are first-class deliverables, not exhaust. The enemy pattern this repo now
hunts by name: silent success theater (a push that never recurred, a CRLF that regenerated
zero item nodes, a summary printing "High 0" beside a HIGH).

Q2 TENSIONS WEIGHED. (1) §F shrink vs [E9] build appetite → landed: build waves must carry
their own closes; window ended −3 vs boot 189. (2) Truth vs cheap on fleet membership →
landed: surface the divergence (declared-but-not-deployed = PASS carried as data, ADR-109
§2/§8), never paper it with a hand row or a fabricated deployed-versions entry. (3)
Declaration doctrine vs build speed → landed: module constant provenance-cited to ADR-104:15
with the drift residual NAMED and mapped to [#472]'s Done-when — not a premature source file
(ADR-109 §2/§9) and not a prose parser.

Q3 CONSIDERED + REJECTED (do not relitigate without NEW evidence). Repomix for paste
distillation (measured 0% on markdown; paste grew). Per-intake-file round-trip (inverts the
engine pattern). Intake source-of-truth flip ([#466] closed: split-only TERMINAL). Copier
re-open (rejection STANDS; stale-citation corrected on [#387]). Decommissioning the
fleet-audit writer (L6 reversal: only the manual push ever died). A new persisted
desired-state YAML (ADR-109 §2 :87, §9 :265 — rejected twice). Widening
resolve_fleet_members (a named §2 ruling — [#472]'s scope). Codemap option A for
ecosystem/schema/ (a tool change or §9 reopening wearing a prose leg's clothes — [#459]
ruled B, revisit needs NEW evidence as a NEW row).

Q4 OPEN QUESTIONS (unresolved or deliberately deferred). [#472]: what form the loadable
ADR-104 declaration takes — every candidate has a named cost (regex brittle / doc change /
new file reopens §2). [#449]: needs a non-repomix mechanism; nothing scoped. L3.5 reconcile
cadence: unblocked by [#460] but undesigned (who reads the divergence report, on what
trigger). The 51 fleet-audit commits: pushed but unreviewed (staged night-batch prompt
exists; operator's word pending). ADR-106 system-Python divergence on the fleet-baseline
task: confirmed live, unfixed (L0.5 remainder, ~1 window). Backpressure detector blind to
pure-deletion closures: JOURNAL-recorded, earns a row only if it re-bites.

Q5 DECOMPOSITION RATIONALE. Proof-first shape: discharge §4 generality BEFORE census
([#462]) BEFORE any apply-channel work ([#385]) — each layer's soundness is the next one's
precondition. One-contract-one-deliverable (this window's R-A lesson): never let two
unrelated Done-whens share an acceptance contract. The next session must NOT redo or
re-decide: the wave-1 engine pattern (monolith ↔ per-item + residue carrier), the
membership_agreement verdict model (undeclared member = FAIL; declared-absent = PASS-as-data,
never WARN — an undispositioned WARN REDs the ship-gate), 9-governs (ADR-109 amendment),
[#459] = B, the metrics organ's NOT-COMPUTED semantics (None never renders as 0), and the
canonical count convention (open row = BACKLOG grep ≡ manifest nodes, always quoted with its
SHA; tasks/ file count runs ~11–20 higher by retire-not-delete).

Q6 OFF-REPO CONTEXT. Operator cadence: end-of-day ladder challenges (evidence-or-NOT-DONE);
"go" is his GO shorthand — read it broadly but state your reading back in one line. The
codex wrapper (~/.claude/bin) now pins terra on BOTH lanes and writes LF; a change-record
audit exists — verify `Model used:` on first use, a silent revert is detectable. Codex
severity summary still lies ("High 0" beside a real HIGH, twice this window) — read the
BODY. Cloud containers: shallow clone, uv shadowing, ~33-failure baseline — history-derived
claims from cloud are unverified by definition. The two [#457] REDs are owned and UNMARKED;
the universal step gate is "no NEW failures beyond those two ids". Value that does not land
on main does not exist.

Q7 RATIFIED-IN-CHAT REGISTER (not yet recorded in the repo; verbatim term · definition ·
durable home).
1. "retire-not-delete at story level" · a completed story keeps its heading + COMPLETED
   marker with date and evidence SHAs; map structure is never deleted · home: landed by this
   bundle's Step 1 commit (the precedent) + a PLAYBOOK backlog-map line on the next prose pass.
2. "journal at wrap, not mid-arc" · a JOURNAL entry written mid-arc is stale the moment the
   arc continues; write it at wrap (ADR-85 caught this 3× in one day) · home: LESSONS.
3. "structural-over-enumerated" · a discipline test sweeps the whole class (e.g. every
   ALL_CHECKS member) instead of pinning a hand-built list — the hand list was wrong by one ·
   home: LESSONS / PLAYBOOK test discipline §.
4. "read the body, never the severity summary" (codex reviews) · the wrapper's tally is
   untrustworthy; findings are read from the body · home: LESSONS, [#431]/[#445] family.
"None" does not apply this window — these four are the debt.
