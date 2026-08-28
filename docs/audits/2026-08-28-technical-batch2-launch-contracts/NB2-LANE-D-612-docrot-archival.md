# NB2 · LANE D — [#612] doc-rot row-body archival — M — **EXCLUSIVE `tasks/` OWNER**

**Batch:** night-batch-2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge` (the hub)
**Branch:** `worktree-lane-d-612-docrot-archival` · **Frozen by the Layer-1 architect, 2026-08-28.**
**Architect's lane id in the frozen bundle: N4.**

**Substrate:** local
**Worktree pairing:** slug `lane-d-612-docrot-archival` -> branch `worktree-lane-d-612-docrot-archival`


## Dispatch

```
claude --bg --model opus --effort high --worktree lane-d-612-docrot-archival --permission-mode bypassPermissions "[dev-knowledge . #612 . doc-rot archival] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-LANE-D-612-docrot-archival.md"
```

## LANE CONTRACT (verbatim from the frozen bundle)

> ### N4 — [#612] doc-rot row-body archival — M — EXCLUSIVE tasks/ owner
> Write-scope: `scripts/validate_doc_rot.py` · `tasks/archive/` (destination per D3) · `tasks/*.md`.
> Intent: row annotation is unbounded debt; the fix is RELOCATION, not trimming — a durable
> per-row record takes the narrative load, the row keeps a pointer. This is the operator's
> "widzieć co ubywa" made mechanical.
> Done: (1) `tasks/archive/` exists with a ruled write path; (2) validate_doc_rot re-run shows
> backlog-row-length STRICTLY REDUCED with NO CONTENT DESTROYED — byte-identical relocation,
> provable; (3) P4 discharged: the 77-findings figure re-measured BEFORE and AFTER, both recorded;
> (4) doctrine documented at the doc-rot home; (5) integrator's filing wave lands through this
> lane's mechanism where applicable.
> Anti-patterns: trimming instead of relocating · any non-byte-identical move · deleting a row ·
> touching protocols/.

**D3 (operator, carried in the GO): the archival destination is `tasks/archive/`, APPROVED.**
That is a new directory. `validate-hermetization` Rule C polices the HOME of an added file
against the allowlist derived from the live taxonomy — check it before you commit
(`uv run --locked python scripts/validate_hermetization.py`), and if Rule C refuses
`tasks/archive/`, the operator's approval is the authorization to add that home to the
allowlist **in the same commit**, narrowly, with the ruling cited. Do not `--no-verify`.

## MEASURED AT DISPATCH (your BEFORE number — item 3's first half is already witnessed)

`uv run --locked python scripts/validate_doc_rot.py`, on `main`, 2026-08-28 23:36 local:

```
validate_doc_rot: 77 doc-rot locus(es) past threshold
```

That is the **77** figure P4 asks you to discharge; it is re-measured, not inherited. Re-run the
same command as your last act and report the AFTER number. The ex-ante success criterion the
morning packet reports against is: **77 -> strictly lower, zero content destroyed.**

## THE MECHANISM (this is the load-bearing half — item 5 depends on it)

The integrator will run a **filing wave** through whatever you build, so the mechanism has to be
usable by someone who is not you and did not read your reasoning:

- **Byte-identity is provable or it did not happen.** Emit an md5 (or sha256) per relocated body,
  before and after, into the archive record itself. `Path.write_text` launders LF->CRLF on
  Windows and a `read_text` round-trip cannot detect it — use `write_bytes` / `read_bytes` for
  anything you are claiming is byte-identical. Scripted `tasks/` edits must write **LF**; CRLF
  reads as "foreign" to the generators.
- **`tasks/` is the source of truth; `BACKLOG.md` is a generated one-line VIEW since [#589].**
  After any `tasks/` edit run `uv run --locked python scripts/gen_task_tree.py --emit-source`.
  Never hand-edit `BACKLOG.md`. A body-reading check that reads `BACKLOG.md` instead of
  `backlog_source.canonical_text` passes on an empty set — if you touch any such check, read the
  source, not the view.
- **A relocated row keeps a POINTER.** A bare audit filename inside a row is a doc-rot false
  strip; path-qualify every pointer (`tasks/archive/<name>`, `docs/audits/<name>`).
- **Do not delete a row and do not close one.** Relocation only.

## RESOLVED LOCATORS (verified at dispatch)

- The doc-rot home for item (4)'s doctrine: `scripts/validate_doc_rot.py`'s own module docstring
  is the honest home for a rule the checker enforces; if you judge a doc site is also owed, name
  it as a candidate filing rather than writing into `protocols/` (anti-pattern: touching
  `protocols/`, and lane C holds the batch's only ratchet authorization).
- The 77 findings are dominated by `backlog-row-length` with a declared ceiling of 1320 chars,
  plus a `backlog-accretion` family keyed on `>= 3 dates & >= 30d span & > 700 chars`. The
  accretion family is the one B1 ("trim-vs-disposition", `protocols/STANDING_RULINGS.md` §B1)
  says is drained by **dropping the dated-amendment narration**, not by sentence-level pruning —
  and relocation is exactly that drain performed without destroying the narration. Read B1 before
  you design the record shape.

---

## BOOT (mechanical — do this before touching a file)

You were launched by `dispatch` into your own worktree. `/lane-boot` steps 1–2 are already
done for you (name validated, single-flight claimed, worktree provisioned). Run steps 3–7:

```
Get-Location                                              # confirm you are in the worktree
uv run --locked python scripts/worktree_seed.py --plan .  # prints the seed plan; RUN what it prints
```

Seeding matters: without `ecosystem/*/state.yaml` copied from the primary, `audit-health`
reports `repos registered (none)` -> `health: DEGRADED` and **every commit is blocked**.
Then `uv sync --locked` (the hub's environment) and, once, the import proof:
`uv run --locked python scripts/worktree_import_proof.py --repo .`  (the hub answers
NOT-APPLICABLE / exit 3 — that is expected and is not a PASS).

Every test invocation is `uv run --locked pytest …`. A bare `pytest` inherits `VIRTUAL_ENV`
from the primary tree and reports green about the primary's source (STANDING_RULINGS D4).

## SHARED CLAUSES — every local lane of night-batch-2 (frozen, verbatim)

> A5: generated surfaces (BACKLOG.md, doc-counts.md, doc-code-edge.yaml, indices, ALL_CHECKS
> registrations) resolved by REGENERATION at integration, ONCE on the merged result. N4 is the
> batch's EXCLUSIVE tasks/ writer; every other lane REPORTS candidate filings for the integrator.
> RATCHET: only N3 may move 443; every other lane's protocols/+templates/ delta must be 0,
> verified pre-commit. Decision budget: standing rulings silently; ask only curated-baseline /
> rule-vs-ruling / no-ruling fork / out-of-scope path (P1); everything else per defaults, ONE
> lane packet: per-item MET/NOT-MET, commits, terra tally, candidate filings, budget decisions.

**Ratchet verification is mechanical, not a promise.** Unless you are lane C, run
`uv run --locked python scripts/silent_rule_detector.py` before your first commit and again
before your last. The dispatch-time measurement is **count: 443, files: 61, detector
silent-rule-v5**. A non-zero delta from a lane other than C is a STOP-and-report, not a
baseline bump.

## THE FOUR THINGS THIS LANE DOES NOT DO

1. **No JOURNAL.md entry.** A batch lane never journals — the integrator writes one anchor for
   the whole queue after every lane has STOPped. The session-end Stop hook will demand a JOURNAL
   entry naming your SHAs: **decline it explicitly and say why** (ADR-85 amendment 2026-08-03
   §A5 made that hook advisory in full; the hard leg is `block-unanchored-push` at pre-push, and
   a lane does not push). Do not silently ignore it and do not "fix" it.
2. **No self-merge, and no suggesting one.** Commit-and-STOP. Your branch enters an integrator
   queue whose order is frozen; naming a merge command invites it to happen out of order.
   A hand-back packet ends at `branch + SHAs + gate state + findings`.
3. **No row closures and no `tasks/` writes** (lane D is the batch's exclusive `tasks/` writer).
   Findings are **REPORTED as candidate filings**, never filed. `/review-closures` owns closure.
4. **No generated-surface regeneration** — `BACKLOG.md`, `docs/audits/README.md`,
   `ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, `.claude/generated/*`. The integrator
   regenerates ONCE on the merged result. If a pre-commit gate forces one to keep your own commit
   legal, do it, keep it in its own commit, and **name that commit in your packet**.

## TESTS

Targeted only — the files covering your own diff ([#528]; PLAYBOOK Ch5). The **full suite runs
once, at integration**, and takes ~9–13 min here. Known pre-existing REDs that are **not yours**:
the anchor-gate probe test has been RED on main since 2026-08-22 (`tmp_path` fixture), and a lane
worktree structurally REDs `test_stale_worktrees`. Report a RED you did not cause as inherited,
with the evidence that it is inherited; do not "fix" it inside this lane.

## REVIEWER

Terra pre-merge is required on every LOCAL lane, **tally-in-body**. Run
`codex exec` over your own diff (NOT `/codex-review` — a mixed doc/code diff kills that lane) and
put the tally in your packet. If codex is unreachable, say so in one line with the error and move
on; an unreachable reviewer is a recorded deviation, not a lane failure.

## YOUR PACKET (the last thing you write, in-tree)

Land it at `docs/audits/2026-08-28-technical-nb2-<lane-letter>-packet.md` — never at the repo
root (`validate-hermetization` Rule A refuses a new top-level file class). It carries, in this
order: (1) per-done-item **MET / NOT-MET / PARTIAL** against the contract above, each with a
witness (command output or `file:line`); (2) the commit SHAs on this branch, in order;
(3) the terra tally; (4) candidate filings for the integrator (never filed here); (5) every
decision taken under the budget; (6) deviations, each with an owner. A claim with no witness
is not a claim — this batch's whole point is that the packet is checkable.

Then **STOP**.
