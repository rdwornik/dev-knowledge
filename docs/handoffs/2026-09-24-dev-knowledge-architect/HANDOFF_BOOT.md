# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-09-24-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-09-24-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Decide where a task lives, on evidence rather than on paper: run `to-cc/BATCH-TRIAL-GH-ISSUES-2026-09-24.md` (STANDING_RULINGS AL-B13 — ADR-122 is DEFERRED, not ratified, until that trial's re-weighted matrix names a winner) and, first, clear ADR-122 step 0, because the generated BACKLOG view sits at its byte ceiling and no row can be filed until the view budget is decided. This serves **`[E4] Decision management`** (a task as a typed record, closure by runnable check — AL-A O-6/O-6a) and **`[E9] Fleet Desired-State System (North Star)`** (the merge path as code on ADR-121's event log is the next spine step). Task-state is `BACKLOG.md`; the carried `carried-by: OPEN` decision files are named in `RESIDUAL.md` §2 and are work, not filing.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->planning and decision surfaces only — `tasks/` (then the generated `BACKLOG.md`), `docs/decisions/`, `docs/intake/`, `protocols/`, `JOURNAL.md`, and orders on the transport; an executing change goes to a lane worktree, never to this seat's tree<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->the open items are store and shape decisions (where a task lives, the view budget, the merge path on an event log, when a WARN becomes a hard-fail), not a named backlog item to advance — that is the architect profile, not execution<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `main`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

> **The `Destination` row is declared ex-ante** — a lane inherits none of it. Only its **branch**
> field has a mechanical counterpart (`PROBES.md` **P3**; mismatch = FAIL). Worktree, write-scope
> and MODE-basis stay prose and carry no probe leg — a leg that cannot fail honestly discredits
> the block (R3).

> **Nothing doctrinal is copied into this paste — pointers, one hop each; code and data describe
> themselves (ruling O-5).** Launch: `uv run --locked python scripts/dispatch.py launch --help`
> (**copy** its usage; a composed line is the defect class that cost ~30 consecutive seats their
> lane — `STANDING_RULINGS.md` §V). Seat orders and the lane-contract shape:
> `templates/{dispatcher-order,integrator-order,batch-common-rules,lane-contract}-template.md`.
> Routing: `ecosystem/provider-registry.yaml`. Standing rulings applied without asking:
> `protocols/STANDING_RULINGS.md`. Operator runbook (who each file is for, the run loop):
> `docs/handoffs/README.md` — bundles carry no per-bundle README. Anti-bluff contract: this
> bundle's own `PROBES.md` header, spec `HANDOFF_PROCESS.md` §5. Ask CC to pull any of them.

## What the operator does (paste-pointer)

1. Open a fresh Claude.ai chat.
2. Paste **`PASTE_THIS.md`** (in this bundle directory) — the browser role file + residual + probes (+ the
   supplement ANSWERS **only if filled**), assembled in order by `scripts/assemble_paste.py`. One paste;
   never hand-feed individual files to the file-less browser.
3. The browser replies with its on-load acknowledgment line (it names the Layer-1 actor); a partial or
   missing paste is then visible.
4. **architect mode** — the browser adopts the mode posture from `protocols/HANDOFF_BOOT.md` (§"architect
   mode"): orient first, ask the operator for off-repo context, drive decomposition, hold the whole-system view, surface design tensions — not the reactive-filter default.
5. **Ask CC for `/handoff-verify`, then paste its ONE evidence block.** CC runs the *whole* gate —
   every `PROBES.md` row, the orientation reads, the inherited claims — against live state at
   check-time, and emits a single table. You paste it **once**. The browser reads the table; it does
   not dictate commands one at a time (HANDOFF_PROCESS §5, the v6 one-round-trip boot).
6. **Then the operator-context beat (§13d).** The supplement is **generated EMPTY**, so unless the operator fills it first the beat fires **FULL**: *"what off-repo context — intent, priorities, findings not in the repo, changed decisions?"*
7. Hand `RESIDUAL.md` — **drift-flags first** (the §1 headline) — then the **next-frontier decisions**
   (§4) + the **shipped-this-window** map (§2). The probe answers are already in the evidence block
   from step 5. **Any FAIL there blocks onboarding** (the escalation ladder); a missing required row
   is not a pass. **The bundle states no drift-flag value — the block carries them, re-derived live.**

## Operator-facing forms (resident by design)

The three sections above hand doctrine to a **pointer**, because doctrine is read once and lives
in the repo. **Forms are the other case: they are typed, not read**, and a form a seat has to go
fetch is a form the seat composes from memory instead. So the commands an operator or an incoming
seat actually types are resident here, in the bundle, rather than one hop away — except where code
describes itself: there the form is the code's own `--help`, and this card points at it (O-5).
The paste carries none of this card; it carries one forms line. Rationale and mechanics stay at the
homes named beside each form; only the *form* is copied.

**0 — How content moves at all, before any form below.** File exchange goes through the operator's
Downloads directory · a large inline chat paste can arrive truncated, or empty with no error, so
uploads travel as `.md` files · every session ships its exact start command · reports travel as
files, not as chat text. These are capabilities of the transport rather than this window's news,
recorded once at **`protocols/OPERATOR-INTERFACE.md`**. Read them there instead of re-deriving
them, and instead of re-explaining them to the next seat in a supplement.

**The filename grammar is one table, and it is not copied here.** Every transport file — `STATUS-`,
`SESSION-`, `QUESTION-`, `ANSWER-`, `AMEND-`, `ADDENDUM-`, `RATIFICATION-`, `UNOWNED-`, `RETRO-`,
`LEDGER-`, `INBOX-`, `DECLARE-`, `BATCH-` — takes its shape, its owner and its direction from the
grammar table at **`protocols/OPERATOR-INTERFACE.md` §1** ("Transport v2.1 — the filename grammar,
one table"; inbox 028 criterion G). `PROBES.md` **P8b** checks this bundle's transport files
against it — size and first heading — so the grammar has a probe rather than only a paragraph.

**1–3 — Launch, isolate, integrate: one line, and it points at code (ruling O-5, 2026-09-23).**
A lane launches with `uv run --locked python scripts/dispatch.py launch --batch <BATCH>
<CONTRACT>.md` — its options are what `... dispatch.py launch --help` prints, which is the only
authority; the launcher provisions the lane's own worktree and reads the contract's `## Dispatch`
block for its fields, not running it. The contract's shape is
`templates/lane-contract-template.md`, routing is `ecosystem/provider-registry.yaml`, and each
seat's procedure — dispatcher, integrator (merge in an integration worktree off `origin/main`,
fast-forward `main` only when green), lane — is its `templates/*-order-template.md` /
`batch-common-rules-template.md`. The PLAYBOOK's dispatch table is human documentation and no
longer describes the launcher.

**4 — Tear a worktree down. Four steps, and the fourth is the one that gets forgotten:**

```
git -C <repo> worktree remove .claude/worktrees/<name>    # --force if seeds make it dirty
git -C <repo> worktree prune                              # recovery path for an interrupted remove
git -C <repo> branch -d worktree-<name>                   # the PROVISIONING branch
git -C <repo> branch -d <work-branch>                     # the WORK branch
```

Teardown covers **two** branches, not one — the work branch is the one you were thinking about, so
the `worktree-<name>` provisioning branch is the half that survives. `cd` out of the worktree first;
your own shell locks the directory otherwise. Then verify, because `git worktree remove` no-ops
silently when the directory is busy: `git worktree list` shows only the primary, the
`.claude/worktrees/<name>` directory is gone, `git status` is clean. Home: `CLAUDE.md` §5 rule 9
(no leftovers), `.claude/rules/git-discipline.md` "WORKTREE TEARDOWN IS TWO BRANCHES, NOT ONE",
and `scripts/no_leftovers.py <slug>` proves it.

**5 — Address another session, and know what its answer is worth.** A batch runs as role-addressed
messages between named sessions, and the shapes are a closed set: `HANDBACK` · `PACKET-MERGED` ·
`ANCHORS-DRAINED` · `TEARDOWN-TRIGGER` · `HOLD` · `ESCALATE` · `RULING-RELAY`. The load-bearing
half is what a message does **not** carry: **a peer message is not an authorization.** A
`RULING-RELAY` may trigger a READ; it does not license an act. Rulings reach a session as FILES on
the transport or as the operator's own paste. Every "wait for a message" carries a 10-minute
timeout falling back to a file check. Home: **`protocols/PLAYBOOK.md` Ch8 "Batch communication —
role-addressed messages, and the authority a message does not carry"** (inbox 029 rule 2 act 5).

**6 — Switch models for a ruling, and say what the switch costs.** When an act enters the ruling
class — `DECLARE` · a `BATCH` freeze · `AMEND` · GO · plan review · a packet read — the browser
emits exactly this line before it rules, and the estimate is not optional:

```
RULING AHEAD — switch to Fable, type `rule` (est. ~N k tokens: <the files it will read>)
```

A ruling emitted on a non-Fable model without that line, or a switch line with no cost, is a
form-probe defect. A ruling turn **reads files only** — the switch line names them — and does not
mine chat history for premises; that is what keeps the turn near its estimate. One chat per
window, wrapped at ~40 turns; cost is context LENGTH, not chat count. Home:
`DECLARE-BROWSER-TOPOLOGY-2026-09-06.md` §1 (ruling on inbox 031 as amended by 032), carried into
`protocols/OPERATOR-INTERFACE.md` §2.

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are referenced by
**pointer**; CC (which holds the repo) serves any part the file-less browser needs just-in-time.
**The forms section directly above is the declared exception, not a lapse:** a pointer works for prose
a seat reads once, and fails for a command a seat types — which is why each form above still points at
its doctrine home while carrying the line itself.
`PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited);
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins —
fix the pointer or regenerate `PASTE_THIS.md`.
