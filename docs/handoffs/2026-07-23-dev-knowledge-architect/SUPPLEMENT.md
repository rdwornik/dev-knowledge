# Architect strategic supplement — 2026-07-23-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-23

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

1. STRATEGIC INTENT — the way-of-working goal for the next session

Convert fleet governance from prose-plus-checks to ONE declarative data contract with
mechanisms DERIVED from it — the Terraform MODEL (declare → plan/diff → apply → state
→ reconcile), never the Terraform tool. The operator's vision, restated at handoff:
manage the process (intake→ADR→backlog→execution→archive), the naming, the files, the
dependencies (doc2doc/doc2file, hooks, skills), the methodology deployment and
versioning, with Python libraries (pydantic schema + networkx graph + pandas
divergence report) — never hand-rolled, never hole-patched. This arc PROVED the
delivery loop and codified it (PLAYBOOK §21); the next session does not re-prove it —
it uses it, starting with the one gate: the [#381] polyrepo shape ruling, in its own
fresh chat, before any machinery is built (standing brake, JOURNAL:76).

Newly dictated at handoff, mostly UNFILED — the next session files these as
intake/backlog rows, does not silently absorb them:
(a) UNIVERSAL PYTHON STYLE: one fleet-wide way of producing code — functional-vs-OOP
    stance ruled once, uniform naming for classes/files/objects/variables, a universal
    Python-delivery methodology that is improvable BECAUSE it is universal. The 07-19
    ruff/pytest parity covers tooling only; the paradigm/naming half is unfiled.
(b) AUTO-COUPLED DOC UPDATES: closing a backlog item must PULL the ARCHITECTURE update
    and JOURNAL entry mechanically — wired, not remembered. Evidence this is needed:
    ARCHITECTURE drift was found TWICE this arc, once the day after a genuine re-read
    ([#403] is the mechanism seed — doc_claims extension to machine-derivable claims).
(c) THREE STANDING NIGHT BATCHES: code review · architecture review · creative
    session — produced at night, consumed by day sessions. The pattern ran twice this
    arc (night audit, night integration batch) and worked, including an armed stop
    that correctly held a bad merge; it needs formalizing as routine.
(d) SUBAGENT/WORKFLOW ROUTING: the operator sees systematic underuse of Sonnet
    fan-out, mini-agents, workflows, and wants ONLINE RESEARCH into Anthropic's own
    published commands/skills (code-review, hooks/skills review, etc.) and their
    adoption across the fleet.
(e) COLORS, SEMANTICS CLARIFIED: opening ANY governed markdown must visually show
    what is the global, hub-managed, repeatable part vs the per-repo personalized
    part. Deployed to ai-council as a DECLARED interim (review 2026-10-22); the real
    blocker is the ownership model itself — see open questions.

2. TENSIONS WEIGHED — where we landed and why

- Buy-vs-build → adopt the MODEL, not the tool (three times: Copier→regenerate,
  Terraform→reconcile loop, Splunk→the data frame). The fleet's substrate (markdown-
  heavy, local-disk, divergence-not-merge-replay) kept failing the tools' assumptions
  while their architecture held.
- System-first vs deliver-now → system-first stands, with ONE declared interim: the
  colors deploy (annotated, review-dated, replaced by the carrier when it lands).
  Declared deviations beat silent ones and beat waiting.
- Archival visibility vs strictness → ACCEPTED is a LIVE status (stays in the working
  folder) with a mandatory `disposition: active|deferred(+trigger)` companion — the
  operator must SEE parked-but-alive vs closed; terminal = CONSUMED|SUPERSEDED|
  REJECTED only.
- Enum reality vs aspiration → enums describe what exists on disk (Withdrawn dropped
  at zero uses ever; Proposed/Deprecated recognized). Aspirational categories with no
  queue get deleted, not kept (same ruling shape as the runbooks genre collapse).
- Immutability vs currency → append-only amendment markers on ADRs, live docs
  repointed, historical records left as accurate history (docs/smoke precedent) —
  never rewrite, never stamp around; freshness-gated files get a GENUINE re-read
  before any stamp.
- Meta vs object work → every session's success metric is a consumer-visible,
  operator-witnessed change; merged ≠ done, witnessed = done.

3. CONSIDERED + REJECTED — do not relitigate

Template engines (Copier/cruft: merge-replay fails our divergence profile; hub is
already regenerate-shaped; kept only the per-consumer version-pin scalar) · Renovate ·
SIEM event-stream framing (fleet is nightly cooperative state-diff) · PyDriller
(measured: ~60x slower than git log --numstat; its cyclomatic value-add returns None
on a ~70%-markdown fleet; stdlib+pandas is MORE faithful to the CodeScene model the
spec cites) · CSV analytics output before L5b consumes it · a third status enum
(reconciled the two that existed) · wholesale ADR-43 retirement (re-scoped instead:
hub landing retired, ai-council repo-local production stands) · Withdrawn ADR status ·
one-member genres (runbooks collapsed; SANCTIONED_GENRES shrunk so recreation is
Rule-A-refused — mechanism, not prose) · closing tickets on unmerged branches ·
worktrees for sequential work (worktree = parallel mutation isolation, nothing else) ·
narrowing the ARC-5 rule-fix goal · the 10-20-repo figure (FABRICATED — live
requirements say 5-8+; price the polyrepo ADR at 5-8+).

4. OPEN QUESTIONS — unresolved or deliberately deferred

OPERATOR-OWNED (nobody else can discharge):
- [#381] the polyrepo shape ruling — THE gate. Inputs: intake #16 §4 + the 2026-07-21
  recon. Must price: unfold cost (~4,200 plural-only lines), the employer-data
  compliance boundary (work vs personal repos in one tree — ONE SENTENCE from the
  operator settles it), pre-sales blast radius. Standing recommendation: PARTIAL fold
  along the compliance boundary — fewer repos, not one repo.
- [#386] closes on his witness of merged PLAYBOOK §21.
- ADR-92 amendment (its body still says "four hard-coded carriers"; reality is five —
  the divergence is now LEGIBLE in ARCHITECTURE's Governing-ADR row, marked
  "amendment owed").
- [#403] derivation choice (carrier set / child roster / Governing-ADR completeness).
- docs/archive/ second review — 9 files, per-file proposals ready in the night-batch
  audit; the queue's own contract says default-to-delete, ~8 weeks overdue.
- ADR-77 guard over the deleted transcripts/ zone: stays armed (current) or retires
  (needs an ADR-77 amendment + lockstep hook/test/organ removal).
- Three unreviewed nightly conformance branches (claude/conformance-2026-07-21/22/23,
  0 High total; summarized in JOURNAL).

DESIGN QUESTIONS:
- The ownership model needs a third cell: commands/skills/hooks rosters are
  hub-mandated STRUCTURE with repo-specific CONTENT — neither owner=hub nor
  owner=repo is true ([#400], same gap as [#370] for ~/.claude). This blocks the
  colors semantics the operator actually wants.
- The status-coupled archival VALIDATOR (W3 seed 2; spec in the 2026-07-23
  enum-reconcile audit §4) — enums are now deployed, the mechanism is unbuilt.
- [#401] ai-council routing still armed at the deleted hub zone + a
  declared-unenforced re-creation gap (candidate organs named, none chosen).
- [#391] fleet_analytics nightly wiring · [#392] rename-alias history ·
  [#393]/[#394] rot review + coverage gap · [#397] scripts/ restructure (impact map
  attached, no moves) · [#399] v5 README.tmpl phantom source · [#402] intake naming
  clause (join-key hazard recorded) · [#389]+[#390] prompt-lint + the ADR-87↔PLAYBOOK
  effort-ownership contradiction · [#387] buy-vs-build intake rewrite · [#396]
  gitenv.py extraction · [#242]/[#362] ADR normalization pair · [#368] VISION
  freshness — deliberately honest, discharges ONLY at the #381 session's genuine
  re-read (carries a named checklist item for VISION:110-113).
- The newly dictated items 1(a)-(d) above — all need filing.

5. DECOMPOSITION RATIONALE — why this shape; what NOT to redo

The chain is #381 ruling → #382 desired-state ADR (pydantic/networkx/pandas; its
first deliverable is a CONFORMING technical intake derived from intake #16) → #383
execution waves (per-surface, worktrees singly, wave-done = the pandas report shows
zero undeclared divergence) → #385 L4 tech-currency. Decisions precede machinery —
that ordering IS the lesson of three months (fleet machinery grew under a shape
nobody argued; ~4,200 lines of it may dissolve on the ruling). The hygiene/enum/
doctrine lanes ran FIRST because desired-state migration needs trustworthy statuses
and truthful canon: both enums are now ruled AND deployed, archives exist and are
visible, ARCHITECTURE is current with its claim-drift corrected twice.

Do NOT: re-prove the delivery loop (canon, PLAYBOOK §21) · re-decide the enums or the
companion-field schema (deployed; migration done, zero OTHER bucket) · restructure
ecosystem/ or deploy/ before their gates (#382 replaces the registry sprawl; deploy/
is on the dissolves-on-fold list) · relitigate anything in Q3 · build the desired-
state system before #381 rules · generate handoffs without the operator's explicit
trigger · treat CC's "(Recommended)" as authority — every plan-mode pick is reasoned
per-question on the merits (two picker shapes; closed-set pickers take a note, not
free text).

6. OFF-REPO CONTEXT

- Operator state: long arc, tired at close, but the deadlock is broken — this arc
  SHIPPED (assets/ dissolved+witnessed; loop codified; L5a analytics live and [#384]
  closed through the gate; runbooks collapsed; transcripts/ deleted with ADR-43
  re-scoped; both enums deployed with [#398] closed; hygiene + ARCHITECTURE currency
  landed; colors deployed as declared interim). Do not cite assets/ as an achievement
  — it was only ever a symbol; the SYSTEM is the demand.
- The operator triggers handoffs. Never the architect, never auto.
- Standing communication contract: five architect fields (INTENT · MODE+basis ·
  EFFORT · GOVERNANCE POINTER · CLOSURE+ANTI-PATTERNS), CC self-loads the rest.
  MODE is the field chats keep forgetting — it is not optional. Wrap verification
  runs SHIP-GATE, never health (health is FAIL-only; the WARN class that blocks
  integration is invisible to it — cost us [#401]).
- Worktree algorithm (repeated operator pain, now fixed doctrine): dependency? →
  sequential. No dependency + disjoint files + both mutate the same repo → parallel
  REQUIRES one worktree per lane (index isolation is the only thing a worktree does).
  Different actors/repos/read-only → parallel with no worktree. Propose the priced
  choice unprompted at the moment the second lane is emitted; the operator picks.
- Blue Yonder boundary: corp-monorepo carries employer/pre-sales material; the
  polyrepo ADR must ask the operator the one-sentence compliance question before any
  fold crosses work/personal.
- The architect's recurring failure class this arc, for the next one to guard
  against: asserting unverified load-bearing facts (a fabricated repo count, a
  nonexistent ruling date, a gitignored "path class", an already-installed
  extension). CC caught each. Verify-or-mark-unverified; the discipline works in
  both directions — two of three suspected formatting defects in the final review
  were render artifacts, correctly flagged as verify-first and correctly left
  untouched.
