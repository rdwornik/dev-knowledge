# FUNNEL GROOM — READ-ONLY proposal sheet — CLOUD lane contract (2026-09-05)

**Consumers:** `ADR-111` (the decision funnel — this sheet's bundles are proposals into its
OWNED / DISCHARGED / CANDIDATE / REJECTED triage, and the only path into a row) and the operator's
groom decisions, which execute from this sheet's own commands. Governance home for the arc:
ARCHITECT-INBOX-2026-09-05 item 006.

**Frozen by:** the Layer-1 browser architect, ARCHITECT-INBOX-2026-09-05 item 006-A.
**Dispatched by:** the FILINGS-2 CC session, 2026-09-05. **Repo:** `dev-knowledge`, revision
`main`. **Class:** research, READ-ONLY. Zero rows closed, zero files archived, zero deletions.

| Model | Mode | Effort |
|---|---|---|
| opus | execution | high |

## Substrate — CLOUD, and the routing check that put it there

**Substrate:** `cloud`. The four axes route **read-only = CLOUD**, and Q3 of the Ch8 routing table
agrees: reconnaissance over the repo's own artifacts, own clone, no gate the result depends on.
Every input this arc reads — `scripts/`, `docs/intake/`, `docs/audits/`, `docs/decisions/`,
`tasks/` — is on `origin/main`, which is the CLOUD test (*"CLOUD if all inputs are in the repo on
`origin/main`"*). The cloud token is scoped to `dev-knowledge`, and `dev-knowledge` is the only
repo this arc reads, so the scope constraint that forces a fleet arc LOCAL does not bind here.
**The LOCAL fallback item 006-A names is therefore NOT taken**, and this line is the "say so".

**The Ch8 CLOUD row, quoted — copied, never composed** (PLAYBOOK Ch8, "The dispatch table — the
SOLE literal-command site", row 2):

```
Dispatch-Cloud <FILE.md> -Title '<slug>'
```

For this contract the title is `funnel-groom-2026-09-05`. The **whole file is the brief** — it
travels in a JSON body, so one file is one lane. The dispatch binds Revision `main`.

**Receipt gate (STANDING_RULINGS Q5), checked as a conjunction by the dispatching seat:** the git
source resolves non-empty, **and** the first assistant text is echoed back. A dispatch missing
either half did not run.

## Standing clauses — READ-ONLY, and what that forbids

1. **Proposals only.** Nothing is archived, closed, edited, deleted, retired or renamed by this
   lane. The verb `delete` does not appear in any bundle — `RETIRE` is the word.
2. **The only write is the deliverable** (below) plus its commit. `git status` shows no other
   modified file. Foreign dirty files in the container are left exactly as found (Q4).
3. **Branch: fresh off `origin/main`.** If the harness has already placed you on a `claude/<slug>`
   branch, keep it — that is the ruled cloud lane prefix and it satisfies item 006-A's "a docs
   branch" (the requirement is *not `main`*). Otherwise create `docs/funnel-groom-2026-09-05`.
   Never commit to `main`.
4. **Toolchain honesty.** Run every detector as `uv run --locked python scripts/<name>`. If `uv`
   is absent or its version does not match the repo's exact pin, fall back to
   `python3 scripts/<name>` and **declare in the deliverable that you did**, with the version you
   found. Never report a gate as run when it was not.
5. **Library-first.** Run the detectors that exist; do not write a new one, and do not
   hand-derive a number a detector already computes.
6. **Every locator is resolved before it is used.** A `file:line`, heading, SHA or `[#id]` you
   have not opened is a claim. Row ids resolve against `tasks/`, **not** `BACKLOG.md` — that file
   has been a generated one-line VIEW since `[#589]`, and reading it would let a bad id look fine.
7. **Pin one SHA** at the start (`git rev-parse HEAD`) and print it. Every count and every verbatim
   detector output in the deliverable is pinned to it.

## The work — item 006-A, in reading order

1. **Detectors, verbatim outputs, pinned to the SHA.** `funnel_lifecycle.py` (legs a1 / a2 / b /
   c / d), `validate_git_backlog.py` (rows closed by a SHA but still present),
   `propose_closures.py` (rows whose Done-when is witnessed on `main`), `boot_frontier.py`
   (serialize-group holds), and doc-rot — the module is `validate_doc_rot.py` (name resolved on
   disk 2026-09-05; the frozen text's `doc_rot` is the check). Quote each output rather than
   summarising it.
2. **INTAKES.** ACCEPTED with every named row terminal -> archive candidates; READY past the
   30-day threshold; intakes whose rows were never born (orphans).
3. **AUDITS.** Audits whose arc rows are all closed -> ledger/archive candidates; audits cited by
   nothing (grep witness); audits with unmet `closed_by` targets.
4. **ADRs.** Superseded-in-fact but not marked; ADRs cited by zero live files; ADRs whose measured
   premise moved — **START with ADR-110 section 2** ("no batch above 3 has run") against batch G's
   nine lanes and the `#528` series, then ADR-85 / ADR-84 against the Stop-hook lane behaviour
   seen in batch G.
5. **TASKS.** Rows whose Done-when is already witnessed (close candidates, **with the SHA**); rows
   referencing vanished files/paths; near-duplicates (the `#629`/`#630` shape); rows with no
   theme/story; L rows with no decomposition; batch-G candidates (a)-(t) deduped against existing
   rows **and** against intakes `#68`/`#69`.

## Deliverable — the one write

`docs/audits/2026-09-05-technical-funnel-groom-sheet.md`:

- **Opens with a `Consumers:` line.** A new `docs/audits/**.md` that declares no consumer
  hard-fails `audit-health`'s `consumer_at_landing` and blocks the commit. Cite something that
  resolves — `ADR-111` and the row ids the sheet proposes against are both live.
- **At most 12 decision bundles first**, each one of `CLOSE` / `ARCHIVE` / `MERGE-ROWS` /
  `REWORD` / `AMEND-ADR` / `RETIRE` — **never "delete"** — carrying (a) the witness and (b) the
  exact command that executes it, copy-ready.
- **Per-item appendix** behind the bundles.
- **Counts before -> projected after, per class** (intakes, audits, ADRs, tasks).
- A note on which detectors ran under `uv` and which under the `python3` fallback (clause 4).

## Closure (frozen)

(1) The pinned SHA is printed before any count. (2) Every bundle cites a witness that resolves.
(3) Every bundle carries an executable command. (4) `git status` shows no file changed outside the
deliverable. (5) **Done-clause 0:** the deliverable is a COMMIT on the lane branch, **pushed** — a
receipt reporting success with zero commits is a FAILED run. Commit-and-STOP.

**The `to-browser` copy is NOT yours, and this is the resolution of a conflict in the frozen
text.** Item 006-A asks the lane to copy the sheet into the operator's `to-browser` directory. A
cloud lane has no access to the operator's disk — that directory is on his machine — so the lane
**cannot** discharge it. The lane therefore **pushes its branch** and says so in its final
message; the `to-browser` copy is owed by a **local seat at harvest**, and is recorded as an open
residual by the dispatching session rather than silently dropped. Merging is the primary-checkout
integrator's, as always.

## Decision budget (V-2)

Execution mode. Ask only about: (a) anything that would write outside the deliverable, (b) a
detector that cannot run at all on either toolchain path, (c) a bundle you believe requires a
ruling before it can even be *proposed*. Everything else is decided against these defaults and
reported in the sheet.

## Anti-patterns

No row closed, archived or edited by this lane. No "delete" as a bundle verb. No count without a
reproducible listing. No BACKLOG row born here — ADR-111's only path is CANDIDATE -> intake ->
ratification. No new detector written. No `BACKLOG.md` read as a source of row ids. No locator
cited unopened. No gate reported as run when the toolchain refused it.
