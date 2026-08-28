# NB2 · CLOUD C1 — the 11-CANDIDATE triage sheet (READ-ONLY)

**Batch:** night-batch-2 · repo `dev-knowledge`, revision `main`. One artifact. Zero writes.

**Substrate:** cloud

## BRIEF (verbatim from the frozen bundle)

> **C1 — 11-CANDIDATE triage sheet.** Input: the batch-1 packet's candidate set, exactly 11
> (2 standing: ratchet zero-headroom; cloud uv · 5 from L3: producer-pack prereqs, corpus
> rotation, served-id, transport-health preflight, locate/re-verify · 4 discovered: byte-cap
> [scheduled as N7 — mark it], Shape-ambiguity [fixed by N8 — mark it], tile manifest, the 664+
> anchored-by-mention WARNs). One row per candidate: proposed ADR-111 disposition — OWNED (name
> the open row) / DISCHARGED (resolving locator) / CANDIDATE (draft one-liner) / REJECTED
> (reason) — each with evidence. A pass routing most items to CANDIDATE has not triaged; say so
> about your own output if it happens.

## WHERE THE INPUT LIVES

`docs/audits/2026-08-28-technical-batch1-end-of-batch-packet.md` — the batch-1 close packet.
Its candidate set is the input; find it and quote each candidate's own words before dispositioning
it. Two of the eleven are already scheduled in tonight's batch and **must be marked as such**:
the **byte-cap** candidate is running as lane F (the architect's N7) and the **`**Shape:**`
ambiguity** is running as lane G (N8). Marking them is not the same as calling them DISCHARGED —
a lane in flight has discharged nothing; say "OWNED, in flight tonight as lane F/G".

## THE FUNNEL RULES THAT BIND YOUR DISPOSITIONS (ADR-111, read it: `docs/decisions/ADR-111-*.md`)

Exactly one of four, per finding: **OWNED** (an open row already covers it — name the row id and
quote the clause that covers it) / **DISCHARGED** (already done or ruled — give a locator that
RESOLVES, and check that it does) / **CANDIDATE** (needs a decision — draft the intake one-liner)
/ **REJECTED** (reason recorded, not relitigated). Row ids resolve against `tasks/`, **not**
`BACKLOG.md` (a generated one-line view since [#589] — reading it would let a bad id look fine).

## SELF-AUDIT

ADR-111's own words: *"a triage pass that routes most items to (c) has not triaged"*. Count your
own dispositions and print the four-way tally. If CANDIDATE is the plurality, say so in the report
under a heading that the operator cannot miss, and say why each one genuinely needed a decision.

---

## STANDING CLAUSES FOR EVERY CLOUD LANE OF NIGHT-BATCH-2 (frozen)

> Shared: zero writes, zero deletions, zero commits; no gate runs (uv mismatch); gate-dependent
> claims = MEASUREMENT-OWED-LOCAL. Each ends with EXACTLY ONE self-contained artifact.

**You are READ-ONLY.** Do not create, edit, delete, stage, commit, branch, push or tag anything.
Your entire output is ONE report, written as your final assistant message.

**You cannot run this repo's gates.** The container's `uv` is 0.8.17 against the repo's pinned
`required-version = "==0.11.19"`, so `uv run --locked …` cannot start. Read files, use `git log`
/ `git show` / `grep` / `python3` directly. **Any claim that would need a gate, a hook, the
pytest suite or `scripts/audit.py` to establish is written as `MEASUREMENT-OWED-LOCAL`, never
estimated and never asserted.** That marker is a first-class, correct outcome here.

**Every claim carries a resolving locator** — `path`, `path:line`, a heading, or a SHA. A claim
without one is not a claim. Do not restate a count you did not compute; compute it and show the
command.

**Output shape.** ONE self-contained artifact as your final message. Begin with the report's own
`#` heading as byte 0 — no preamble line, no wrapping code fence around the whole report. (Two of
the four 2026-08-26 cloud reports wrapped themselves in a fence behind one line of prose; the
harvester kept the bytes and recorded the deviation, which is more expensive than getting it
right.) Inside the report, fence code and tables that the operator will copy.

**Self-audit clause.** Each brief below states a way its own output can fail while looking
complete. Apply it to yourself and **say so in the report** if it happens.

**Repo facts you can rely on (measured on the operator's disk, 2026-08-28 23:36 local):**
`docs/intake/*.md` = 56 · `docs/decisions/*.md` (top level) = 89 · `docs/audits/*.md` (top level)
= 769 · `tasks/**/*.md` = 344 · `BACKLOG.md` = 67,883 B (a generated one-line VIEW since [#589];
the SOURCE OF TRUTH is `tasks/`). If your own count of the clone disagrees, **report both** — the
clone is `origin/main` and the disk may be ahead.
