# LANE lane-w-1-wintooling-canonical-restamp — re-read win-tooling's three stale canonical docs END-TO-END and stamp them, unwedging every author's commit gate

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `interactive` — an operator-attended session — integration and seat acts live here.

```
claude
Read <PROMPTS_DIR>\LANE-w-1-wintooling-canonical-restamp.md and execute it exactly.
```

`claude` starts the session; the second line is its **first message**, not a
shell command. `<PROMPTS_DIR>` is the prompts directory
(`$env:CLAUDE_PROMPTS_DIR`, `~\Downloads` by default) — the operator resolves it
by eye here, because a chat message is not a shell and nothing expands the
variable for him. This shape exists for the acts a background lane cannot
perform: integration needs an operator GO per merge, and a `--bg`
session can neither merge to `main` nor ask a question. Tier on the record above
(`opus` / `high`); board label `[.dev-knowledge · lane-w-1-wintooling-canonical-restamp · lane-w-1-wintooling-canonical-restamp]`.

## Worktree pairing

slug `lane-w-1-wintooling-canonical-restamp` -> contract `LANE-w-1-wintooling-canonical-restamp.md`

**No lane branch.** An interactive session runs in the primary checkout on an
author-chosen branch, so there is no `worktree-` or `claude/` name for this
contract to declare — and declaring one would be a claim the tree never makes
true. The 1:1 property ADR-110's fifth per-lane requirement asks for still holds
on the pair that exists: one contract file, one session.

## Why this lane exists (operator ruling 6, 2026-09-01)

`win-tooling`'s `canonical_freshness` gate FAILS on three canonical docs and has since **2026-08-29
at the latest**. It is a blocking gate, so **every author in that repo is wedged**, and the
2026-09-01 window had to declare `SKIP=canonical_freshness` twice — once to merge batch-E's HY-5
and once to push it — with the pre-existence proven each time.

The night seat REFUSED to stamp them, and that refusal is the reason this lane exists rather than
a fix already having happened: a stamp means the doc was re-read, and stamping three unread
canonical docs is exactly the fake stamp the gate's own message forbids. **The honest remedy is
the read, and the read needs an attended seat.**

## Done-contract (immutable)

1. **All three stale docs are RE-READ END-TO-END and stamped with the genuine review date.**
   `win-tooling/VISION.md` (reviewed 2026-07-11, edited 2026-07-12), `ARCHITECTURE.md`
   (edited 2026-08-19) and `CLAUDE.md` (edited 2026-08-29). A stamp means *re-read end-to-end and
   confirmed accurate, or drift filed* — never "touched". **This lane is ATTENDED precisely
   because that is a judgement a background seat cannot honestly make.**
2. **What changed since 2026-08-29 is RECORDED per document** — a short note per file saying what
   the read found, so the next reviewer starts from a diff rather than from zero. A stamp with no
   record of what was reviewed is the fake stamp one level up.
3. **Any drift the read finds is FILED, not fixed in passing.** The lane's product is an honest
   stamp plus a list; repairing content mid-review is how a review becomes an edit nobody reviewed.
4. **The commit gate is UNWEDGED and proven so** — `canonical_freshness` returns clean, and a
   trivial no-op commit in win-tooling succeeds WITHOUT `SKIP=canonical_freshness`. That is the
   whole point: every author in that repo is currently blocked, and two commits during the
   2026-09-01 window had to declare the bypass.
5. Docs in English; hyphen-only names; win-tooling's own suite run, with its **one pre-existing
   environment RED** reported as pre-existing rather than chased or claimed.

## Steps

1. Read `win-tooling/CLAUDE.md`, `ARCHITECTURE.md` and `VISION.md` end to end. Do not skim to the
   stamp.
2. For each, diff against its `last_reviewed` commit to see what actually changed, and write the
   per-document note.
3. Stamp `last_reviewed: <today>` in each, and update any `Last updated:` footer that exists.
4. Run `canonical_freshness_gate.py` and confirm clean; then make a real commit with NO
   `SKIP=`, proving the gate passes.
5. File any drift found as its own row or note. Commit and STOP.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. `<imperative — what is done>` **COMMIT**
2. `<imperative>` **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
