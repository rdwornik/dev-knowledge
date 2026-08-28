# Architect strategic supplement — 2026-08-28-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-28

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
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

**1. Strategic intent.** The next TWO sessions move the hub from self-improvement to
DEPLOYMENT. Way-of-working goal: the methodology proves itself by instantiating in a consumer
repo, not by governing itself better. Concretely: next session = EXECUTION-ONLY against the
seven filed intakes (no new research, no new census, no new measurement — the evidence is
landed and current); the session after opens win-tooling. Operator mandate, verbatim in
priority order: consolidate · universalize · library-first · backlog · methodology hygiene ·
performance/efficiency · deployment to other repos. A window that ships no consumer-visible
value is a failure by the operator's standard — that tolerance is exhausted.

**2. Tensions weighed.**
(a) Subtraction-only vs mechanisms-first: the outgoing seat and operator proposed a
subtraction-only window; I ruled mechanisms first ([#589] view projection, [#590] index
concurrency, [#595] consumer-at-landing) THEN subtraction. Vindicated: the aggregate-view
defect was what made every merge conflict, so subtraction before it would have cost more than
it saved.
(b) Kill vs execute: the census produced 40 kill candidates, every one with a counter-case;
the ex-ante kill algorithm closed ZERO, execution closed EIGHT. Landed rule: at this backlog's
quality, subtraction comes from executing small rows and re-cutting shipped halves — the RE-CUT
column is where the volume is, not the kill column.
(c) Speed vs rigor: adopted tiered gating (targeted-per-merge + one full suite per batch) under
time pressure; it is now doctrine, and NB's per-check tiers cut the commit gate 4.6x (203s ->
44s). Its selector half ([#598] slow-marker) stopped on a measured long-pole verdict (21.42%).
(d) Parallelism vs coordination tax: 11 lanes (previous window) exceeded the useful ratio; 3-5
file-disjoint lanes plus read-only cloud fan-out worked. Cloud recon is nearly free and is
under-used, not over-used.
(e) Role residency vs paste integrity: chose residency (-16,228 B measured), accepting the
sha-pin + standing refusal as the safety. SEE OPEN QUESTION 1 — the residency HOME is unproven.

**3. Considered and rejected — do not relitigate.**
- 52-row active cap: REJECTED as a cap, adopted as a ranking (X2; the census's own arithmetic
  falsifies the cap — it admits same-day rows and excludes older kill candidates).
- A new hub checker for Click / Rich / dataclasses-over-dicts: REJECTED (X3; a hub-hardcoded
  standalone checker lands as `absent` on consumers, measured).
- Rotation justified on performance: REJECTED as a premise (X6; ~0.1s after W2A — its real case
  is context, grep and merge collisions).
- Structural doc diet before the mechanical PLAYBOOK correction: REJECTED as sequencing (X7;
  would silently discard 17 of the 19 [#569] census findings).
- Subtraction-only window: REJECTED in favour of mechanisms-then-subtraction (see 2a).
- Deferring [#267] part (ii) behind a P6 successor that does not exist: REJECTED, cut instead
  (Y-1 — a peg must name a carrier that exists).
- Gemini CLI as a fan-out surface: RETIRED by ruling (UNSUPPORTED_CLIENT, not a tier refusal).
  grok as fan-out: REJECTED — pay-per-call, $0.037 for one trivial test; point-use only.
- A root `prompts/` folder: REVOKED by operator ruling (root is sacred; the docs orphan disease
  is cured by the consumer-at-landing gate, not by a sibling folder). ADR-101's first contraction.

**4. Open questions.**
1. **ROLE RESIDENCY HOME — settle in the first minutes.** D-R1 shipped the PIN, but whether the
   operator's browser has a persistent instructions surface (a Project) is UNPROVEN. If it does
   not, the PIN has nothing to verify and every seat refuses to boot; the correct act is then to
   revert to inlining and record D-R1 as measured-and-reversed. Ask before assuming.
2. G1 — two live birth paths (packet-born `source:` clauses vs register Y restating ADR-111's
   orthodox CANDIDATE -> intake path), with no statement of which applies when.
3. G3 — a CONTRADICTION, not a gap: ruling U(b) makes GitHub compute the default substrate;
   W4, one day later, measured that rung unable to run a single hub gate. One of them must yield.
4. G2 — CLAUDE.md §10's AGENTS.md anti-pattern is provably false since ADR-115 but sits in a
   hub-single-sourced Form-A region; the fix is a fleet-parity act no row authorises ([#577]).
5. G4/G5 — green-by-skip is owned at two layers with the rule still unwritten.
6. R3 measured acceptance for agy / Kimi / GLM / DeepSeek. THE FLEET HAS ZERO WORKING FAN-OUT
   SURFACE. All accounts are now funded (see 6), so this is executable, gated only on seeded-
   defect acceptance vs the incumbent baseline — never on vibes.
7. [#82]'s hub-closability ruling · the 30 unblocked P2s below the ranking cut · whether
   [#548]/[#559]'s multi-edge dependencies imply a manifest-producer row nobody owns.
8. D1 smoke-6 receipt: Codespaces Q4 stays unpriced until `Ok=True AND RemoteExitCode=0` with an
   in-container check-count receipt. Two halves owed: hub image (landed) and the win-tooling
   `gh codespace cp` literal-quote defect (operator-owned).
9. [#611] v7 scope vs what remains of the census deltas (b4 probes-pin is the big one, ~12 KB).

**5. Decomposition rationale — and what NOT to redo.**
Shape: mechanisms (gates) -> measurement (diagnostic, census, recon) -> subtraction (closures,
icebox, re-cuts) -> spec (v6.3.0). Each stage was a precondition of the next, and the order is
the finding, not a preference.
DO NOT REDO, all landed and current: the hub diagnostic (consumption census, 40% orphan
audits) · the backlog quality census incl. its reconstructed age axis (validated 4/5 buckets
exactly) · PERF-RECON's bottleneck map · the four night recons (doc diet, kodeks, rotation,
backlog) · the 874-hit version-surface classification · the provider-surface measurement (8
CLIs) and probe #42's instruction-file precedence · rulings sections U, V, W, X, Y · ADR-115's
criterion (re-test ONLY if agy's AGENTS.md precedence is falsified — it is the load-bearing leg,
not Cursor, which is plan-gated out and unregistered).
DO NOT re-derive dispatch: PLAYBOOK Ch8 is the SOLE literal-command site, one verb per substrate.

**6. Off-repo context — changed intent.**
- Deployment to other repos must START within two sessions. This is the operator's headline
  intent and it outranks further hub polish.
- ALL provider accounts are now funded and verified by the operator (Kimi, GLM, DeepSeek
  confirmed paid; agy authenticated via Google; grok pay-per-call). The chinese-models intake
  is no longer blocked on money — only on R3.
- The night protocol (dispatch -> sentinel -> harvest -> manifest -> morning adjudication) ran
  end-to-end and is now the expected default rhythm, not an experiment. It is owned by [#610].
- Three operator-owned one-liners gate hub work and are outstanding: tag `v1.4.0` (without it
  `deploy` hard-aborts preflight, so win-tooling instantiation cannot start), `git push origin
  automation/fleet-audit` (2 commits behind, ADR-80 record stale), and the win-tooling half:
  `cp`-quote fix plus the two missing verbs `Dispatch-After` and `Harvest-Cloud`.
- L0 finding the hub cannot fix: the global CLAUDE.md Self-Evolution Protocol reads
  `~/.claude/memory/learned-rules.md`, which does not exist.

**7. Ratified-in-chat register — not yet in the repo.**
- **"measure the surface, never enumerate it"** — before any cross-cutting change, grep the repo
  and classify every hit; an enumerated list is a fact carried from memory. Vindicated at 874
  hits (six live false statements found in a file no list named). HOME: PLAYBOOK (versioning
  chapter) + LESSONS.
- **The three version classes** — LIVE-NORMATIVE (update) / STRUCTURAL-LEGAL (a folder name is
  not a version claim) / HISTORICAL-IMMUTABLE (never touched; rewriting a v4.4 citation
  fabricates history). HOME: PLAYBOOK, same chapter.
- **"a transferred fact carries a locator or is derived on site"** — architect errors #18/#19
  were both facts relayed between packets without verification. HOME: LESSONS (partially
  landed; the rule line is owed).
- **Tiered gating cadence** — targeted-per-merge plus ONE full suite per batch, full suite at
  integration only. HOME: PLAYBOOK Ch5 (NB landed the tier mechanism; the cadence paragraph and
  the [#598] selector remain owed).
- **"closures fund births"** — the D3/D5 order: close BEFORE filing, because the cap must be
  known before it is spent; the banked ledger IS the birth budget. Banked at close: 5.
  HOME: PLAYBOOK backlog chapter.
- **Execution beats adjudication for subtraction** (see 2b) — the empirical rule this window
  produced. HOME: LESSONS.

===================== CC VERIFICATION AT FOLD TIME (not an operator answer) =====================
<!-- CC-authored 2026-08-28 at `supplement filled`. The operator's answers above are UNCHANGED.
     Per HANDOFF_PROCESS v6 §B(b) only answers asserting a repo-verifiable FACT are checkable;
     intent, tensions and rejected options are advisory by construction and are NOT checked. -->

Three repo-verifiable facts in **answer 6** were re-derived live at fold time:

- **`v1.4.0` is NOT tagged — CONFIRMED.** Newest tag is `v1.3.1`. The `deploy` preflight abort
  stands, so win-tooling instantiation is still blocked on this one-liner. This is the operator
  one-liner that gates the stated headline intent (deployment within two sessions).
- **`automation/fleet-audit` is NOT 2 commits behind — REFUTED, and the claim is DISCHARGED.**
  Local and `origin/automation/fleet-audit` are both at `1f8b6434`; the push has already happened.
  Recorded here so the next seat does not chase a closed item, and so the `Inherited claims` row
  does not FAIL the boot on a claim that merely went stale between filling and booting.
- **`~/.claude/memory/learned-rules.md` does not exist — CONFIRMED.** It is L0, outside this repo,
  so the hub still cannot fix it; the global CLAUDE.md Self-Evolution Protocol reads a missing file.

**Re-derive rather than trust these three lines** — they are fold-time observations and no P-tier
probe covers them.
