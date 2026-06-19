# Architect strategic supplement — 2026-06-19-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-19

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
A. **ADR-88 ratification path — Council or operator-ratify, and what does it gate?** ADR-88
   (*file-oriented dependency management*) was **authored this window (Proposed)** — the capstone the
   2026-06-18 supplement directed. Its FC4 deterministic trigger (#140 `doc_rot`) already shipped.
   Does ratification go through AI Council, or operator-ratify (the ADR-82/#149 precedent)? And does
   anything (e.g. treating #179–#183 as "doctrine" vs "proposal") wait on it? (RESIDUAL §4 Q1.)
B. **The `ship-gate` RED disposition — A/B/C.** Two 2026-06-19 wrap commits (`3a894ee`, `d0f9ead`)
   landed direct-on-`main` (already pushed; un-FF off the table), so ship-gate is RED. Resolution is a
   *methodology* call: (A) disposition the journal/chore-wrap-direct pattern, (B) operator-accept the
   one-off, or (C) tighten the wrap workflow so even the journal-wrap branches. Which — and does it
   change how strictly core-invariant #5 binds a wrap? (RESIDUAL §1 / §4 Q4.)

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# Handoff supplement — outgoing architect — 2026-06-19

<!-- scope: meta -->

> Old hand to new hand. This is not a task list — it is the *way-of-working* state at the close
> of a long session, so the next architect inherits judgment, not just facts. Written deep, not
> exhaustive. Repo facts (SHAs, line numbers) are in the residual + the committed audit; this is
> the **why**.

---

## The through-line — read this first

Everything this session did was one thing: **grounding ADR-88 (file-oriented dependency management) in reality.** Not a side-cleanup — the central arc.

The session's core engineering was the **Phase-1 seal: three Claude-Code worktrees run in parallel** (this was the most important work):
- **seal-hooks** — fixed the **C1 JOURNAL-gate bug** (the Stop-gate computed its commit arc as the *push* boundary, so under deferred-serial-push a multi-session unpushed arc let one prior SHA-citation "vaccinate" the whole arc → later sessions could ship unjournaled and the gate passed silently). Narrowed to the *session* boundary. Also the #188 hook-completeness audit.
- **seal-dedup** — #187 dedup-on-entry + #186 floor-sync.
- **seal-grooming** — #140 `doc_rot` history-accretion detector.

Those three shipped **ADR-88's deterministic triggers**: FC3 dedup (#187) and FC4 history-accretion (#140). So part of ADR-88 is already mechanically real. The afternoon then authored ADR-88 itself (Proposed) and ran straight into the proof that the *rest* of it is not real: PLAYBOOK + ESSENTIALS were rotting with references to machinery that no longer exists. We audited, groomed the currency, and cleaned the repo — but the structural and lifecycle halves remain unbuilt.

**Where the next session must focus:** make file-oriented dependency management *enforced across the whole repo* before any further methodology deployment (#131). The methodology is not deployed yet. It is closer. It is not there.

---

## What ADR-88 actually is (because you said you don't fully feel it)

Plain model: **markdown files are objects. Their references are edges. The repo is a graph.**

A file references other things — commands (`/boot`), ADRs, sibling sections (`§16`), other files, systems. Each reference is an **edge** from this node to another. In OOP terms: an object holding a pointer to another object. When the target is retired (a method deleted, a command archived, a section removed), the edge becomes a **dangling pointer** — it points at nothing, but it still sits there, read as if live.

The repo has a dangling-edge detector for **one** node type — the BACKLOG task-graph (#156 / #179). It has **none** for prose. So prose docs accrete dangling edges with nothing to catch them. That is the rot you feel. The four failure classes:

- **FC1** — spine-failure (the coherence spine breaks).
- **FC2** — undeclared edges (#179): a real dependency that isn't declared, so nothing tracks it.
- **FC3** — duplication (#187): the same content in two places, drifting apart.
- **FC4** — history-accretion (#140): dead content piles up and is never removed.

"Graphs / whole-repo" = treating every node (file, automation branch, folder) as a graph node that must (a) have all its edges resolve, and (b) prove it still **earns its keep**. That second half is the broadened diagnosis below.

---

## 1. Strategic intent (way-of-working goal)

Turn ADR-88 from *Proposed-and-partially-detected* into an **enforced lifecycle organ** for the whole repo, so the repo becomes self-policing about its own coherence. Concretely, three organs:
1. **Referential-currency detector** — does every edge (command/ADR/section/file reference) still resolve?
2. **Structural linter** — is the graph shape sound? (numbering, header scheme, ToC — the things the architect provably *cannot* eyeball; see Q3.)
3. **"Earns-its-keep" check** — does each node still justify existing? (files, automation, branches, folders — see Off-repo.)

The goal is not to fix today's rot (we did, manually). It is to make manual re-grooming **never necessary again** — so #131 deployment stands on a base that cannot silently rot.

## 2. Tensions weighed, where I landed, why

- **Groom-first vs mechanism-first** → groom-first. The manual currency groom was the *prototype*: doing it by hand is what told us exactly what is mechanical vs judgment, which makes the mechanism design concrete instead of abstract. It also unblocked the handoff (a handoff built on a lying PLAYBOOK carries the rot forward).
- **Where the organ runs** → the same **detect / groom / gate** triad as the rest of the system: detect = nightly conformance digest (ADR-84); groom = human-ratified purge; gate-on-regression = pre-commit + handoff (universal root-7 + a `.dev-knowledge`-local extension for PLAYBOOK/ESSENTIALS). Hard-gating *full* currency would breed `/override` habits, so the gate only blocks *newly-added* dead edges.
- **One problem or three** → three distinct organs. The architect can reliably reason about *references* but **not** *structure* (proven, Q3). So references → detector; structure → linter; lifecycle → earns-its-keep. Don't collapse them.

## 3. Considered + rejected — do NOT relitigate

- **Blanket-purge of every retirement annotation** — REJECTED. Two kinds: dead-refs-in-usable-positions (purge) vs anti-regression context-notes (keep). The ~18 `CHANGELOG retired` notes are load-bearing; a detector that flags all of them is wrong. The **note-vs-usable distinction is settled** and is a load-bearing requirement of the detector.
- **Architect eyeball for structural claims** — REJECTED, *proven wrong this session*. My audit's structural section was 2/2 false: the §18 numbering gap is intentional (documented, "git has it") not rot; the embedded-template H2s sit inside fenced blocks the ToC generator skips, so they don't pollute anything and demoting them would corrupt the templates. A grep over a snapshot cannot see fences, intent-notes, or generator behaviour. **Structural checks must be a live organ. Settled.**
- **Memory-based dead-lists** — REJECTED. Truth derives from live state ∪ the retirement ledger (JOURNAL / archive / ADR), never a hand-kept list. Mechanism-not-memory is ADR-88's own principle.
- **Renumbering the §18 gap; demoting the H2s** — REJECTED (above). Renumbering would have *created* new dangling edges.

## 4. Open questions (unresolved / deferred)

- **The mechanism's exact shape** — you have a debate running in another chat that proposes the solution; that proposal is the next session's primary design input. Open inside it: how does the detector mechanically tell note from usable? How does the linter cope with a two-documents-glued file?
- **The two-docs split** — is PLAYBOOK one document or two (a *reference* doc + a *workflow-recipes* doc)? This is where "I can't see the shape of my infrastructure" lives. Deferred to a deliberate structural decision (Council-class).
- **Lifecycle scope** — see Off-repo: the rot is not only prose edges; automation, branches, folders, ENVIRONMENT.md currency all need the earns-its-keep check. Open: does the organ extend to all node types or start prose-only?
- **ESSENTIALS-as-lens** — reshape ESSENTIALS into a 1:1 projection of PLAYBOOK's chapter list (itself a checkable file-dependency). Deferred, deliberate.
- **Over-annotation condense** — the ~18 / ~10 / ~8 inline retirement notes → canonical-once. Deferred (operator judgment on aggressiveness).
- **Residuals A and B** below.

## 5. Decomposition rationale — what NOT to redo

Locked sequence: **prove the problem** (this session: audit + manual groom = the prototype) → **design the mechanism** (your running debate) → **build + enforce** → **then deploy methodology (#131)**. The groom-as-prototype concretizes the design; the organ must exist before #131 because you cannot deploy onto a base that silently rots.

Do **not** redo: the confirm-live ledger (`/boot`/`/evolve` dead; `/save`/§19 live; all 44 cited ADRs resolve — verified live); the committed audit's findings; the note-vs-usable distinction; the structural-claims-need-a-live-organ lesson (now in LESSONS); the currency groom itself (shipped, merged). **Do not re-audit PLAYBOOK/ESSENTIALS currency by hand** — build the organ so it never needs hand-auditing again.

## 6. Off-repo context

- **Operator state**: deep frustration that `protocols/` rots despite long effort — felt as the methodology not-yet-being-real. The reframe that landed and should hold: it is **one missing organ (lifecycle enforcement)**, not a failed methodology. Everything else worked this session.
- **A debate is running in another chat** proposing the mechanism. Incorporate its output; it is the design authority for the next session.
- **Broadened diagnosis (this-session finding, not yet in an ADR): system-lifecycle-rot, not just doc-rot.** Automation (`automation/fleet-audit`, `automation/conformance-digest`), branches, folders, ENVIRONMENT.md — all accrete with nothing asking "does this still earn its keep / is its output consumed." `fleet-audit` is confirmed live by-design ADR-84 infra (it writes daily; verified, kept) but **its output-consumption is unverified** and it writes local-only (not pushed to origin like its sibling) — a concrete instance of the open lifecycle question.
- **Priority is explicit**: file-oriented dependency management + graphs + whole-repo coherence come **before** further methodology deployment.

---

## A. ADR-88 ratification path — and what it gates

**Lean: ratify via Council (or a Council-equivalent deliberation), not bare operator-ratify — and ratify *before* the mechanism build.** ADR-88 is foundational doctrine — the "files are objects with edges" model the entire lifecycle organ will enforce — not a narrow/procedural decision like the ADR-82/#149 operator-ratify precedent. **But**: your running debate may itself be the deliberation. If it is a genuine multi-agent weighing of the doctrine, its verdict can serve as the ratification basis; otherwise convene. **What it gates**: whether #179–#183 and the shipped detectors are treated as load-bearing *doctrine* vs *proposal*. The mechanism can be *built on* them while Proposed; calling them canonical waits on ratification. Ratify first so the build enforces ratified doctrine, not a draft.

## B. ship-gate RED — disposition

**Lean: (B) for the immediate RED, (C) for the durable rule.** The two wrap commits are already pushed and un-FF — you can't un-ring them, so operator-accept the one-off (B). Going forward, tighten the wrap workflow so even the journal-wrap branches + FFs (C). Reasoning: a wrap commit is still a commit, and "direct-on-`main`" is exactly the discipline-erosion core-invariant #5 exists to prevent — so **#5 should bind a wrap as strictly as anything else.** Reject (A): dispositioning direct-wraps as acceptable is the camel's nose — it converts the invariant into a suggestion. Note the genuine fork: (A) is defensible *if* you judge a journal-only wrap as low-risk-enough to exempt and would rather accept mild gate-noise than mild branch-ceremony. I don't — but it's your call to make, and the way the ship-gate went RED is itself the system correctly flagging the erosion. Honor it by tightening, not by dispositioning it away.

---

*Outgoing-architect supplement, session 2026-06-19. Pairs with the residual and the committed audit `docs/audits/2026-06-19-playbook-essentials-currency-audit.md`. The next session's first move is the mechanism design from the running debate — not a re-audit.*
