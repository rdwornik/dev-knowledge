# Handoff Methodology — Empirical Failure Evidence 2026-05-25

> **Type:** Research evidence — extracted chat history
> **Purpose:** Document concrete behavioral failures observed during 2026-05-25 handoff attempts, to ground subsequent AI Council debate on handoff methodology
> **Audience:** Claude Code (preparing Council questions); AI Council (consuming questions with evidence base)
> **Scope:** Read-only research artifact. NOT a protocol change. NOT a methodology revision. Evidence summary only.

---

## Context

The 2026-05-23 → 2026-05-25 session arc included substantial governance work (tier-deprecation universalization, self-audit, BACKLOG audit, handoff process residuals). Toward end-of-session, the operator initiated two handoff attempts to transfer state into fresh browser chats. Both produced thin or generic output that did NOT continue work with discipline despite full bundle delivery per current handoff process (ADR-42 v3 / HANDOFF_PROCESS.md v3.3.3).

Concurrently, the OLD sender chat (which had full session context) demonstrated N=7+ verification-miss instances during prompt generation for the very methodology being audited. The failure pattern crossed all three actors (OLD sender, NEW receiver #1, NEW receiver #2).

This evidence file extracts concrete behavioral data points for grounded Council debate.

---

## Sender chat (OLD) — verification-miss pattern N=7

Documented during the 2026-05-25 session, all in single session before handoff attempts:

| # | Instance | Failure mechanism |
|---|---|---|
| 1 | Prompt 9 routing brief claimed "ai-council retains CHANGELOG; ADR-49 specific to .dev-knowledge" — WRONG | Pattern-matched confident claim, no ADR-49 read |
| 2 | Line 2295 PLAYBOOK path tracking — marked pending while already merged | Assumed merge state without verification |
| 3 | Workspace sort regression — assumed preserved without verification | Confidence ahead of grounding |
| 4 | Prompt 11 unauthorized `notes/` folder creation (later deleted) | Generated artifact outside operator-approved scope |
| 5 | CHANGELOG line inserted into proposed user instructions while simultaneously codifying ADR-49 (CHANGELOG retirement) | Modified existing doc without auditing existing content |
| 6 | Prompt 15 v1 (handoff refactor) — **hallucinated file structure** for 11→4 mapping table: referenced files 02_TASK, 03_BOUNDARIES, 10_ROLE, 11_FORMAT_RULES that do not exist in repo. Real 12-file structure is 00_README, 00_first-message, 01_MANIFEST, 01_manifest.json, 02_VISION, 03_PLAYBOOK, 04_ESSENTIALS, 05_GOVERNANCE_ESSENCES, 06_STATE_OF_PLAY, 07_ACTION_PLAN, 08_TREE, 09_EXECUTION_EVIDENCE. Would have silently dropped invariant copies + SHA-256 manifest (materially ADR-45 rolled-back direction). Caught by CC pre-execution verification. | Generated substantive Opus/high prompt without reading actual live template/bundle |
| 7 | Prompt 15 v2 (corrected, audit findings only) — proposed M-6 fix via "add frontmatter" mechanism, but ADR-39 registers templates via Registry, not frontmatter. Caught by CC. | Did not read ADR-39 in full before proposing mechanism |

**Pattern characterization:** confidence itself was the signal to verify, not to skip. Each failure shared structure: pattern-match generated plausible content; live verification absent; correct mechanism existed but uncited.

The N=7 happened in the sender chat that had **maximum context** about the system being modified. Context volume did not prevent verification failure.

---

## NEW chat #1 — .dev-knowledge session-sync handoff

**Bundle delivered:** 11-file self-handoff per current process. Operator pasted `00_first-message.md` into fresh browser chat. Bundle contained full VISION, PLAYBOOK, ESSENTIALS, GOVERNANCE_ESSENCES (ADR-42/45/49/28), STATE_OF_PLAY, ACTION_PLAN.

**Articulation gate (4 items in own words):**

NEW chat #1 produced:
> 1. Role per VISION. .dev-knowledge is the ecosystem's meta-layer — a portable, machine-agnostic methodology framework that authors universal LLM-development conventions, absorbs lessons from child repos, and audits compliance against the universal governance baseline. My role as its architect this session is to drive a load-bearing methodology decision (the bundle consolidation question) and the paired workflow gap (Council-output return), not to execute mechanical refactoring.
> 2. Current phase per state. Post-tier-deprecation stabilization landed cleanly...; the next phase is architectural deliberation on handoff-bundle structural scope (11→N), which is gated on an operator decision and **blocks the P1 cross-repo rollout enablers (scrum-master codification, Council decisions management) behind it**.
> 3. Immediate next action per directive #1. Obtain an operator decision on handoff-bundle consolidation...
> 4. Top 3 Hard Constraints. [accurate transcription]

**Observation:** articulation items 1, 3, 4 — accurate paraphrase. Item 2 contained false claim ("blocks P1 cross-repo rollout enablers behind it") — scrum-master codification is NOT blocked by consolidation; ACTION_PLAN.md Directive 1 explicit path (b) was "shelve consolidation → pivot to scrum-master." This false dependency was constructible from pattern-match ("Directive 1 is gating Directive 2") without close reading of Directive 1 path (b).

**Sender chat reviewer (me) confirmed "role confirmed" without flagging Item 2 drift.** This is itself part of the failure pattern — receiver gates were treated as ACK checkpoints rather than substantive review.

**Receiver synthesis (after role confirmed):**

NEW chat #1 produced full synthesis. Strengths: pinned HEAD verification mechanism, "name model in every Model/Mode/Effort table" specificity, "leaner-bundle = methodology change not template edit" framing.

Drift from Stage 2:
- I-PASS implementation decay evidence (NCBI PMC11968091, healthcare handoff research) cited in Stage 2 as grounding for "ceremony decay is not imagined" → dropped in synthesis, replaced with assertion-only "ceremony decay are not imagined."
- Directive 1+3 coupling explicit in Stage 2 (Council decisions management workflow tested by Council debate on consolidation) → weakened to sequential in synthesis.
- Operator stated phrasing "żeby AI Council wracał, żeby łatwo zarządzać ADR-ami" (return-path concern) → not developed in synthesis "chat-retrievable" framing.

**Critical failure — post-confirmation behavior:**

After "synthesis confirmed" + operator redirect ("priority is corp-monorepo audit + universalization, not bundle consolidation"), NEW chat #1 produced response that:
- Flagged scope contract violation (correct — Layer-2 invariant honored)
- Cited unmerged audit branches as prior-art check (correct)
- Asked operator to choose path

**BUT:** the response was process-about-process. Did NOT reference VISION/standards/ADRs to ground what universalization concretely means. Operator's actual concern was substantive (file structure + naming + workspace pattern + dot-prefix convention + ARCHITECTURE.md + Mermaid diagrams + tier-residue elimination in workspace templates). NEW chat #1 had ADR-38 amendment + ADR-51 amendment + ADR-33 amendment + root hygiene PLAYBOOK section + audit.py + template files **available in bundle** — none invoked in response.

Operator's verbatim assessment: "wydaje się zaskoczony" + "absolutnie nieogarnięte... nie zapoznał się ani z Vision, ani z plikami które przysłałem."

**Behavioral signature:** bundle delivered standards; NEW chat could paraphrase them at articulation gate; could not operationalize them when operator asked for substantive grounding 1 turn later.

---

## NEW chat #2 — corp-monorepo handoff (later same evening)

**Bundle:** generated separately for corp-monorepo universalization work. Less detailed evidence in chat history but pattern matches:
- Operator described concrete universalization concerns (apply .dev-knowledge standards to corp-monorepo: file structure, README removal, ARCHITECTURE diagram, dot-prefix, tier residue, workspace pattern)
- NEW chat #2 produced response operator described as "wydaje się zaskoczony" — surprised by scope it should have known from the bundle
- Specifically: "absolutnie nieogarnięte... ponieważ nie zapoznał się ani z Vision, ani z plikami, które przysłałem"

**Both NEW chats failed at the same juncture:** bundle delivered → articulation passed → substantive work required reference back to bundle content → reference failed.

---

## Cross-actor pattern

Three independent LLM instances (OLD sender, NEW receiver #1, NEW receiver #2), all on Claude (Sonnet/Opus mix), all with substantial context loaded:

- OLD sender: max context, full session history. **Failed verification 7+ times** in single session.
- NEW receiver #1: full bundle, fresh context. **Passed articulation, failed operationalization.**
- NEW receiver #2: full bundle, fresh context. **Failed comprehension visibly to operator.**

**Common failure mode:** plausible-output generation outpaced verified-grounding. Articulation gates that asked "paraphrase X" were satisfiable by pattern-match; substantive work that required "use X to make decision Y" exposed that internalization hadn't happened.

---

## What the sender chat (OLD) attempted as remediation, and why it didn't address root cause

In response to NEW chat failures, sender chat (me) proposed:
1. Forced-retrieval articulation gate (questions requiring file:section references) — addresses fakability but not LLM cognition under context load
2. Multi-round Q&A before substantive work — addresses internalization but expands context window before work begins, contradicting token-optimization concern
3. Conditional bundle composition (skills/gotchas/journal vs PLAYBOOK/ESSENTIALS) — addresses bundle relevance but assumes problem is content not engagement

**Each proposal was an incremental fix to current architecture.** None questioned whether current handoff architecture is right abstraction for session-continuation between LLM chats.

Operator observation: "Ty chcesz go zbyt uprościć, ja uważam, że on w ogóle nawet teraz, jak jest skomplikowany, jest, nie jest dobrze zrobiony."

This is methodology-level concern requiring architectural deliberation, not incremental tuning.

---

## Operator-stated specific concerns (verbatim or near-verbatim from chat)

1. "first message powinno być lepsze... ono w ogóle przeczytaj jeszcze raz te wszystkie pliki. Mam wrażenie, że first message jest za mało takie zmuszające do zadawania sobie pytań."

2. "handoff to jest jednak tak jakbyś uczył dziecko wdrożać nowe rzeczy, czyli musi znać kompleks, historię, wyvision i stan obecny jak najlepszy możliwy sposób, ale jednocześnie musisz zmusić ten czat do tego, żeby on przeczytał te pliki poprzez zadanie mi, zadał nie sobie właściwych pytań."

3. "to nie chodzi o ilość rzeczy, bo na przykład bez playbooka i bez essentials prompty są źle generowane. Czad przestaje generować prompty te one są nie są dokładne nie wiem jaki by playbook i essentials czy to jest odpowiednio ale prompty"

4. "on mówił żeby czytać playbook i essentials a dlaczego miałby czytać playbook i essentials przecież najważniejsze jest to używanie skillsów i używanie żurnalów gotchas wtedy kiedy jest to potrzebne"

5. "jest rozjazd, czat zapomina jak tworzyć promty, nie wiem, jaką algorytm ma dokonywania decyzji, czy te promty są, z jakim modelem"

6. "musimy w tym czacie zakończyć, usprawnić proces hand-offu, tak żebyśmy mogli kontynuować pracę"

---

## Observations about what's NOT broken

To prevent over-correction, what is working:
- 3-stage flow (Stage 1 question → Stage 2 architect response → Stage 3 bundle) — methodologically validated by ICM (Van Clief & McDermott, arXiv:2603.16021); operator confirmed it should not be removed
- Self-Containment Rule (bundle carries full VISION/PLAYBOOK/ESSENTIALS invariant copies) — load-bearing for NEW chat operating without repo access; rolling back via ADR-45 was rejected
- SHA-256 manifest integrity verification — provides drift detection
- HEAD ancestor verification — provides repo-state grounding
- Witnessed/inferred/unknown epistemic markers — provides reasoning hygiene
- Filesystem state tracking (in-progress/ active, flat/ final, archive/ inputs) — operational

What may not be working (subject of Council debate):
- Articulation gate as fakable pattern-match
- Bundle content selection (PLAYBOOK/ESSENTIALS vs skills/gotchas/journal — operator-flagged)
- Single-pass reading discipline (no enforced re-engagement after initial articulation)
- Receiver gate response handling (sender treats as ACK rather than substantive review)
- Prompt-generation discipline within NEW chat (operator: "czat zapomina jak tworzyć promty")

---

## Constraints on Council debate scope

Per current convention:
- ADR-42 v3 + amendments is the live convention
- ADR-45 is frozen design exploration (supersedes nothing); any consolidation re-opens ADR-45 explicitly
- Council debate transcripts return to `.dev-knowledge/docs/decisions/transcripts/`
- Layer-2 invariant: this evidence file, Council questions, transcripts all live in .dev-knowledge or ai-council; no orchestration scripts

---

## Read in conjunction with

- `protocols/HANDOFF_PROCESS.md` (current v3.3.3)
- `docs/decisions/ADR-42-handoff-format-v3.md` (live convention)
- `docs/decisions/ADR-45-handoff-architecture-v4.md` (explored, rolled back, supersession withdrawn 2026-05-25)
- `docs/audits/2026-05-20-handoff-process.md` (prior audit, 6 medium findings resolved 2026-05-25)
- `templates/HANDOFF_QUESTION_TEMPLATE.md`, `templates/HANDOFF_FOLDER_TEMPLATE.md`
- `C:\Users\1028120\Documents\Dev\ai-council\docs\council-question-guide.md` (debate question discipline)
- Recent live bundles in `docs/handoffs/` (concrete examples of current 12-file structure)
