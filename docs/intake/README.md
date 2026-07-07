# docs/intake/ — the requirements spine

<!-- scope: meta -->

`docs/intake/` holds **intake documents** — the requirements-capture artifact ratified by
ADR-98 (Accepted 2026-07-07) and built by BACKLOG **#268** (Arc 2, "the intake scene").
This README defines the format, the frontmatter schema, and the lifecycle; the
fill-in skeleton is `templates/intake-template.md`.

## 1. What this folder is

An intake doc is **WHAT/WHY**, captured from the operator's own conversation (fluid
voice or chat, the `--mode functional` boot) and structured by CC into the template
below. **0..1 intake doc per initiative** — it is the requirements spine an initiative
hangs off, not a running log.

ADR-98 §3 draws the genre line hard, and it is the single fact worth memorizing about
this folder:

- **Intake doc = WHAT/WHY** — problem, scenarios, requirements, ex-ante acceptance
  criteria. Lives here.
- **ADR = the DECISION at a genuine fork** — authored only when a reasonable person
  could choose otherwise *and* reversal is costly. **0..n per intake** (an intake may
  force zero ADRs, or several). Lives in `docs/decisions/`.
- **Backlog epic = the WORK** — **1..n per accepted intake**; each epic entry cites
  its intake-id **and** the ADR-id(s) it rests on. Lives in `BACKLOG.md`.

The seam that makes this useful: **acceptance criteria copy VERBATIM** from the
intake doc into the epic's UAT — no re-derivation between capture and build. If the
UAT reads differently from the intake doc's acceptance-criteria section, one of them
is wrong.

## 2. Doc format

Fill in `templates/intake-template.md` — do not hand-roll the shape. Eight sections,
framed on the operator's own 4+1 thesis method (the "+1" scenarios view drives the
rest):

- **Problem / motivation** — why now, one paragraph.
- **Scenarios (+1 view)** — concrete walkthroughs: "as the operator I … and then …".
  **The load-bearing section** — a requirement with no scenario behind it is suspect;
  push back on it rather than encode it.
- **Functional requirements** — must / should / could.
- **Acceptance criteria (ex-ante)** — measurable, written before build starts. These
  become the epic's UAT **verbatim** at EPIC RETURN (§1 above).
- **Non-goals** — what this explicitly does not cover; as load-bearing as the
  requirements themselves for keeping an epic's scope honest.
- **Impact sketch (4+1 lite)** — one line per view: logical / process / development /
  physical. Which views does this actually touch? Keeps the thesis framing honest
  without ceremony.
- **Open questions** — everything the functional chat refused to guess. A functional
  boot has no live-state probes (that's the technical architect's lane); a
  technical-factual question that comes up mid-conversation gets recorded here, not
  answered speculatively.
- **Status** — see §5 Lifecycle below.

## 3. Frontmatter schema

Every intake doc opens with:

```yaml
---
intake-id: <N>       # stable integer, next free across all history (closed ids are not reused — same discipline as BACKLOG ids)
status: <see §5>
origin: <one line: who / where / when — e.g. "operator voice session, 2026-07-06">
consumed-by: <ADR/backlog ids — populate only when status: CONSUMED>
---
```

`intake-id` is permanent once assigned — it is the join key the accepting ADR and the
resulting epic(s) cite back (§1). Don't renumber on rejection or on folder growth.

## 4. Naming

Going-forward: `YYYY-MM-DD-{func|tech}-slug.md` — the repo's standard dated-artifact
convention (CLAUDE.md §4) plus a genre infix:

- **`func`** — an elicitation-born requirement (a functional-architect conversation; the
  WHAT/WHY the operator surfaced).
- **`tech`** — a technical follow-up (a requirement raised by the technical architect's
  triage, or a technical-factual item spun out of a `func` doc).

The date is the **origin** date (when the conversation happened / the SEED landed), not
the date the doc was formatted or triaged.

**Genre is folder-first, infix-second.** The hard split is the *folder*: `docs/audits/` =
evidence (what a read-only census/audit found), `docs/intake/` = requests (what someone
wants built). The `{func|tech}` infix subdivides *within* intake; it never crosses the
folder line.

Ratified 2026-07-08. **No mass-rename** — existing intake docs keep their current
`YYYY-MM-DD-slug.md` names; the infix applies only to docs created from here on.

## 5. Lifecycle

```
SEED → DRAFT → READY-FOR-TECHNICAL → CONSUMED (ADR/backlog ids)
                                    → REJECTED (one-line why, kept)
```

- **SEED** — a pre-intake candidate dropped by a feed (§8), not yet worked by a
  functional-architect conversation. SEED docs live in **this one folder** — ADR-98's
  source ruling rejected a separate `proposals/` folder (folder proliferation is its
  own rot class; the fleet-audit lesson applies to folders same as routines).
- **DRAFT** — a functional conversation is structuring it; not yet operator-approved.
- **READY-FOR-TECHNICAL** — operator-approved (§6), waiting on the technical
  architect's triage.
- **CONSUMED (ids)** — the technical architect accepted it; the doc records which
  ADR(s) and/or backlog epic(s) it produced (§3 `consumed-by`).
- **REJECTED (why, kept)** — the technical architect declined it. The one-line reason
  is recorded in the doc's Status section and the doc **stays** — rejections are
  knowledge, not garbage; do not delete a rejected intake doc.

## 6. The confirm-gate

An intake doc is a **confirm-gated artifact**, not an advisory note (ADR-98 §4): the
**operator approves the draft before it lands here**. This is ADR-28's "operator
consent" moved one step earlier in the pipeline — consent now attaches to the
confirmed intake doc, before decomposition even starts, rather than to the eventual
ADR or epic.

Conversion path for a fluid session: voice/chat ramble → CC converts the transcript
or the functional-architect synthesis into the template shape → **operator approves
the draft** → it lands in `docs/intake/` at DRAFT or READY-FOR-TECHNICAL. A doc that
hasn't cleared that approval step does not belong in this folder yet (it's still a
transcript, not an intake doc).

## 7. Rent rule (ex-ante)

Every routine — including this one — names its **consumer + a survival metric**
before it's allowed to run (the fleet-audit lesson: a routine with no consumer is a
rot generator, not permanent infrastructure). For the intake scene:

- **Consumer:** the technical-architect triage — accept (→ ADR and/or backlog
  epic(s), doc goes CONSUMED with ids), defer (parked, stays visible in this folder's
  index), or reject (recorded, doc goes REJECTED).
- **Survival metric:** intake docs sitting unconsumed after **~1 month of operation**
  trigger a review of the scene for removal (ADR-98 §6). A folder that only
  accumulates SEED/DRAFT docs nobody triages has failed the same test a routine
  fails.

## 8. Feeds

Two mechanisms drop SEED docs into this folder without going through a functional
conversation first:

- **`/changelog-review`** (ADR-98 §7, live) — ADOPT and OBSOLETES-WORKAROUND findings
  from a changelog-review run land here as **one batched SEED doc per review**,
  named `YYYY-MM-DD-changelog-review-seeds.md`. This is the review's actual
  consumer now — ADOPT items no longer dead-end on "the operator routes from the
  digest" (see `.claude/commands/changelog-review.md`).
- **The nightly proposal loop** (NOT yet live — gated on the load-gauge landing
  first, per standing operator ruling; see BACKLOG) — will land functional feature
  ideas the same way, one SEED doc per run, same naming pattern.

Both feeds write **status: SEED only** — a feed proposes, it never decomposes and
never mutates the backlog directly (the same never-mutate boundary the nightly loop
carries generally).

Beyond these two automated feeds, an **audit** (evidence, `docs/audits/`) feeds intake by
hand when a finding turns out **requirement-shaped** — it crosses the folder line as a SEED
and runs the full spine (**audit → SEED → triage → ADR → backlog → build → UAT**), evidence
becoming a request.

## 9. Advisory edge note

A backlog epic (or a §14a-style epic handoff) that cites a confirmed intake doc forms
a coherence edge between `docs/intake/` and the epic surface. Per ADR-98 §5 that edge
stays **advisory** — nothing gates on it — **until two intake docs have been consumed
end-to-end**. Only at that n=2 point does hardening (a required-linked-intake gate on
new epics) get decided. Don't build or propose that gate before the evidence exists.
