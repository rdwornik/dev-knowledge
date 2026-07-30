---
class: technical
date: 2026-07-30
slug: night-batch-standing-section-draft
Status: "DRAFT — NOT CANON. Awaiting architect ratification."
producer: claude-code
lane: docs/446-window-step-0-5
anchor_sha: c8490c1d
consumer: the morning verification batch
consumption_path: "branch-only night output -> local gates -> operator merge"
discharges: "U6(a) rider — trigger fired (the 2026-07-30->31 night batch ran)"
---

# Standing night-batch section + ADR-105 activation record — Step 0.5 draft

> **Status: DRAFT — NOT CANON.** This is the U6(a) rider drafted at trigger-fire, not a ratified
> canon insertion. It neither edits a canonical file nor activates a routine. Both deliverables
> below are proposals for the architect's ruling.

## 0. Two premise corrections — read before ruling

Neither is a blocker for the substance, but both should be recorded rather than propagated.

### C-1. The night-batch content is intake #19 **§A**, not §B

Every surface that carries the U6(a) rider cites "intake #19 **§B** standing night-batch
section":

- `docs/audits/2026-07-30-technical-intake18-ratification-record.md:41` (the ratification record —
  immutable per CLAUDE.md §5 rule 3)
- `docs/audits/2026-07-30-technical-v6-spec-sol-draft.md:252`
- `docs/handoffs/2026-07-31-dev-knowledge-architect/PASTE_THIS.md:376` and `RESIDUAL.md:109`

The intake's actual structure disagrees. From
`docs/intake/2026-07-27-func-operator-design-input-night-shift-handoff-reform.md`:

- `:31` — `## SECTION A — night shift`
- `:83` — `## SECTION B — handoff reform`

and the intake's own frontmatter `note:` field states it plainly: *"Section A feeds the
morning-loop wave; section B feeds the intake #18 ratification session."* §B contains **no**
night-batch content; its item (b) is the one-round-trip boot, i.e. `[#446]` itself. The
night-shift design input — HOST, NIGHT-JOB REGISTRY, MORNING RATIFICATION SURFACE, and the
`nothing merges unattended` hard rule — is entirely in **§A**.

**Disposition taken:** this draft is built from **§A**, the section that actually holds the
content. The mis-citation is recorded here, not silently corrected upstream — the ratification
record is immutable, so the correction lands as an amendment marker or a note in the ratifying
arc, at the architect's call.

### C-2. U6(a) is a DEFERRED rider whose trigger fired — not "ratified"

The commissioning brief calls this "the **ratified** intake #19 §B standing night-batch section".
The record says otherwise: `…intake18-ratification-record.md:117` — *"**Rider U6(a) is
unaffected** and stays DEFERRED with its original trigger (the next night-batch request)."*

The trigger has now fired (the 2026-07-30→31 night batch ran, five commits on
`claude/night-2026-07-30-boot-prep`). **Trigger-fire makes the rider actionable; it does not
ratify its content.** That is why this is a draft artifact rather than a canon edit — writing
ratified-sounding text into `protocols/` on a fired trigger would manufacture authority the
record does not grant.

---

## 1. Deliverable A — the standing night-batch section (proposed text)

**Proposed canonical home: `protocols/PLAYBOOK.md`, a new section.** Flagged as needing a ruling
— `ARCHITECTURE.md` Ch3 "Automation axes" is the competing home per `CLAUDE.md` §3's chapter
pointers (cloud/nightly Routine + spec-orchestration + t-shirt model routing already live
there). PLAYBOOK is proposed because this is *working-protocol* material (how a night batch is
run and consumed), not structural-model material. **Do not insert until the home is ruled** —
PLAYBOOK is also freshness-gated and TOC-gated, so the insertion carries a `last_reviewed`
re-stamp and a `toc-freshness-playbook` regen.

### Proposed section text

> ### Night-batch work — the morning-loop wave from the night side
>
> A night batch is not a new project. It is the morning-loop wave seen from the night side, and
> existing doctrine already governs most of it: model routing by stage size (Appendix B),
> unattended-writer branch isolation (ADR-84), propose-never-mutate for Tier-3, and ADR-105's
> rule that a routine may not activate without a named consumer. What night work adds is
> executable, not doctrinal.
>
> **The hard rule: nothing merges unattended.** The night produces proposals and evidence; the
> morning is the operator plus ONE report. A night lane is branch-only — it does not merge, does
> not push, does not edit canon, does not close a row, and does not issue a ruling. Every output
> is UNVERIFIED-UNTIL-LOCAL input until a local gate run confirms it.
>
> **Three organs a night batch needs** (intake #19 §A (a)-(c)):
> 1. a **HOST** — no CI exists, so nightly work runs on the operator's machine or a cloud
>    Routine;
> 2. a **NIGHT-JOB REGISTRY** — each job declares trigger, scope, consumer, consumption path
>    (the ADR-105 six-field shape, which also converts `[#426]` from a 30-item retrofit into one
>    field per job);
> 3. a **MORNING RATIFICATION SURFACE** — the consumer whose absence is the root of `[#419]`.
>
> **Shape of a batch.** Opus orchestrates; Sonnet runs bounded probes; Haiku runs read-only
> fan-out. Every git mutation stays serial in the orchestrating thread — parallel writers on one
> tree corrupt each other. Producer != reviewer holds: a reviewing agent that did not write the
> artifact is less biased toward it.
>
> **Every workstream lands one dated report** carrying a named `consumer` and
> `consumption_path` (ADR-105 discipline), and reports are reports — a night batch does not
> create standing planning artifacts (`[#443]` rent rule).
>
> **Isolation.** Parallel runs sharing one home directory corrupt each other's session state;
> each run needs its own. A night lane names its branch in a sanctioned machine-produced lane
> shape (`claude/<slug>`, CLAUDE.md §4) and is never self-merged.
>
> **Honest-limits requirement.** A night report states what it did NOT check. A batch that
> reports only findings, with no statement of coverage limits, is not a completed batch.

### Empirical basis (this is not inherited from the intake)

The 2026-07-30→31 batch exercised the shape above and is the first witness for it. Four
workstreams, four dated reports, five commits, tree clean, nothing merged. Two behaviors worth
promoting into the text above were *learned* rather than designed, and are already folded in:

- **Report what you did not check.** All four reports carried explicit not-checked sections; W3's
  ruled-out list (CRLF, byte-vs-char, sentinel spoofing) was as decision-useful as its findings.
- **A read-only mandate needs a leftover sweep.** W4 wrote a 12,882-byte working file into the
  repo root despite a read-only brief. It was relocated, not deleted, and the tree ended clean —
  but the mandate alone did not prevent it, which is why the cleanup beat belongs in the section.

---

## 2. Deliverable B — ONE ADR-105 activation record

### The six-field row, per ADR-105 §1

Shape quoted from `docs/decisions/ADR-105-*.md:40-42` — an in-line `·`-delimited clause on the
row, never a continuation line. Proposed record, with the brief's ruled `consumer` and
`consumption_path`:

```
· routine: trigger=operator night-batch request · scope=hub night-batch workstream reports
(branch-only) · consumer=the morning verification batch · consumption_path=branch-only night
output → local gates → operator merge · verified_by=local pytest + audit.py ship-gate at
morning verification · review_date=2026-08-26
```

`review_date=2026-08-26` is proposed, not ruled — it aligns with the existing 2026-08-26 review
cluster (the `.vscode` carrier, the four intake-edge dispositions, the D-queue session) rather
than inventing a date.

### PRE-WRITE CHAR MEASUREMENT — and why the write is BLOCKED

Measured live at `c8490c1d`. Proposed clause: **319 chars**. Cap: **1200** (`validate_doc_rot`
`_BACKLOG_GROSS_CHARS`).

| Candidate host row | Current chars | + clause | Verdict |
|---|---|---|---|
| `[#419]` routines whose output nobody consumes | 1169 | 1488 | **OVER cap** |
| `[#426]` declare consumer + consumption_path for every LIVE routine | 1149 | 1468 | **OVER cap** |
| `[#428]` nightly-triage dead producer | 1194 | 1513 | **OVER cap** |

**All three natural host rows are already within 51 chars of the cap.** Writing the activation
record onto any of them trips `doc_rot` gross-bloat immediately — converting one clean write into
a new WARN plus a new disposition. **No write was made.** This is precisely what the brief's
pre-write measurement requirement exists to catch.

### Options for the architect

| Option | Action | Cost |
|---|---|---|
| **A. Trim the host row first, then add** | condense `[#426]`'s inline history to git-history pointer (the ADR-49/65 pattern), then write the 319-char clause | couples the record to a row trim; `[#426]` is the best semantic fit (it *is* the declare-consumer row) |
| **B. File a new row for the night-batch routine** | new row carries the clause from birth, no cap pressure | triggers `backlog-filing-backpressure` — needs a `kill-candidates:` line; adds a row to a backlog under drain pressure |
| **C. Defer the record to the G0 groom** | the groom is already trimming 5 rows; add `[#426]` as a 6th and land the clause in the same arc | cleanest coupling, but makes the record wait on the G0 ruling |

**Recommendation: C.** The G0 groom (item 2 of this window) is already a trim-and-regen arc over
`tasks/` rows with the disposition-retirement pattern in hand. Adding `[#426]` to that set lands
the trim and the activation record in one coherent move, with one regen and one JOURNAL anchor,
instead of a standalone row-trim whose only purpose is to make room. If G0 is ruled NOT to
proceed, fall back to **A** scoped to `[#426]` alone.

---

## 3. Ride-clean confirmation

Both deliverables ride lane `docs/446-window-step-0-5` (off `main` `c8490c1d`) as **this single
dated artifact**. Confirmed clean:

- **No canonical file touched** — no `protocols/`, no `CLAUDE.md`, no `ARCHITECTURE.md`. The
  §1 section text is quoted *inside* this draft, not inserted.
- **No `tasks/` row touched, no `BACKLOG.md` regen** — the measurement above is why. So no
  char-cap write occurred, and `validate_backlog` / `gen_task_tree --check` are unaffected.
- **No night-lane content merged or cherry-picked.** This lane branches from `main`, not from
  `claude/night-2026-07-30-boot-prep`; that branch is untouched and remains local-only.
- **Gate exposure is one added `docs/audits/` file** — `validate_hermetization` Rule B (name
  grammar: date · `technical` · lowercase-kebab slug) and `audit-index-freshness` (index regen,
  done in the same commit).

**Not done, deliberately:** the routine is **not activated** (ADR-105's gate is at activation, and
activating it requires the row write that the cap blocks); the section is **not inserted** into
PLAYBOOK (home unruled, and the file is freshness- and TOC-gated); the §B→§A mis-citation is
**not** corrected at its four upstream sites (one is an immutable audit).
