# DRAFT — Intake process design (functional architect → technical architect → epic chats)

> **STATUS: DRAFT — decision-reserved.** Authored on the unmerged `drafts/2026-07-07-proposals`
> branch by the overnight mission (Block 4) as a decision-ready draft for the morning architect
> session. **Nothing here is ratified.** The operator's explicit undesigned ask (2026-07-06
> SUPPLEMENT/JOURNAL): *"the undesigned functional-architect → technical-architect → epic-chat
> intake process."* Draft boldly, decide nothing — this is the raw material for that decision.

## 1. The problem this designs away

Today a raw operator ask ("I want X") reaches an **architect** (§13) or an **epic lane** (§14a)
with no defined step that turns *intent* into a *decomposed, contracted work-set*. The architect
improvises the decomposition inline. Two gaps:

- **No requirements-capture step.** The "why / for whom / done-looks-like" of a new initiative is
  captured ad-hoc in a prompt, not in a durable intake artifact — so it can't be reviewed,
  re-read, or reconciled against later (the same class the strategic supplement closed for
  *handoffs*, unclosed for *initiatives*).
- **No named hand-off from requirements to structure.** The jump from "here's what I want" to
  "here are the backlog items + ADRs + §14 epic handoffs" is one undifferentiated act. When it
  goes wrong (mis-scoped epic, missing ADR), there's no seam to inspect.

## 2. Proposed shape — a three-role pipeline

A deliberate split of the single "architect" act into three roles (they may be the same browser
chat wearing different hats across turns, or distinct chats — see §5 Open questions):

| Role | Input | Output | Analogue today |
|---|---|---|---|
| **Functional architect** | operator intent (raw) | an **intake doc** — requirements, users, done-looks-like, constraints, non-goals | the strategic supplement's "why", but ex-ante for an initiative |
| **Technical architect** | the intake doc | **BACKLOG items (ADR-66 story-map) + ADRs + §14a epic handoffs** | today's architect decomposition (§13d + Ch8 tree-orchestration) |
| **Epic chats** | one §14a handoff each | executed epic (commit-and-STOP, §14b return) | today's epic lanes (ADR-97) |

The pipeline is **intake doc → decomposition → epic handoffs**, each seam a durable artifact:
the intake doc is the functional/technical seam; the §14a handoff is the technical/epic seam
(already exists). Only the **functional half is green-field.**

## 3. Draft PLAYBOOK section (proposed home: Part II workflow, adjacent to §1 "Starting a New
Project" / §2 "Creating a CC prompt"; or Ch8 tree-orchestration vicinity)

```
### Intake — from operator intent to a decomposed epic set

Before decomposition (§13d / Ch8), a NEW INITIATIVE passes through intake. The functional
architect turns raw operator intent into an INTAKE DOC (templates/intake-template.md):
requirements · users/personas · done-looks-like (the hard acceptance the whole initiative is
measured on) · constraints · explicit non-goals. The operator confirms the intake doc — that
confirmation is the requirements gate (the analogue of "the operator pasting a prompt IS
consent", ADR-28, moved one step earlier).

The technical architect then consumes the CONFIRMED intake doc and produces: BACKLOG items in
the ADR-66 story-map (themes → stories → tasks), any ADRs the initiative forces, and one §14a
EPIC handoff per parallelizable epic (ADR-97 file-boundary discipline). Decomposition doctrine
(§13d, Ch8) is unchanged — intake only adds the requirements-capture step BEFORE it.

Skip intake for a single well-scoped task (that is a §2 CC prompt, not an initiative). Intake
is for MULTI-EPIC initiatives where the requirements themselves need capture + confirmation.
```

## 4. Draft intake template

See `templates/intake-template.md` (drafted alongside this memo on the same unmerged branch).

## 5. Open questions (for the architect to decide — NOT decided here)

1. **One chat or three?** Are functional/technical/epic distinct browser chats (like the
   tree-orchestration root/epic split), or roles one architect chat moves through? Trade-off:
   distinct chats = clean seams + more handoff overhead; one chat = less ceremony, muddier seams.
2. **Where does the intake doc live?** A new `docs/intake/` area (new top-level — needs the ADR-51
   growth-trigger check), or under `docs/` existing, or as a per-initiative artifact in the
   handoff bundle?
3. **Is the intake doc gated?** Should a §14a epic handoff REQUIRE a linked confirmed intake doc
   (a coherence edge), or stay advisory?
4. **Relationship to the strategic supplement.** Intake captures ex-ante initiative requirements;
   the supplement captures ex-post session "why". Do they share a template/mechanism, or stay
   distinct?
5. **Does this need an ADR?** The role-split is process doctrine — likely ADR-class (it changes
   who-does-what in the ADR-28/97 authority model).

## 6. Recommendation (draft — the architect rules)

Adopt the **three-role model as a role-progression within the architect chat** (not three
separate chats) for now — lowest ceremony, and the tree-orchestration split (ADR-97) already
handles the epic-lane fan-out. Make the **intake doc a real artifact** (template below) and
**confirm-gate it** (operator confirmation before decomposition), but leave the intake↔epic
coherence edge **advisory** until a second initiative shows the gate earns its keep (the n=2
discipline). File an ADR if the role-split is adopted. **Decision reserved.**
