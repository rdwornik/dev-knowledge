# QA-role incident evidence — reporting-truthfulness + maintenance-commit (2026-07-08)

<!-- scope: meta -->

> **Genre:** evidence (`docs/audits/`, per `docs/intake/README.md` §4 genre-folder-first:
> `docs/audits/` = what a read-only pass found; `docs/intake/` = what someone wants built).
> **Feeds:** the `qa-engineer-role` functional intake (not yet authored) — two real
> session-discipline incidents that motivate a QA / verification role. Evidence, not a
> build request; the intake doc, when authored, may lift these as ex-ante scenarios.
> **Routing:** filed per the operator's 2026-07-08 direction — F-A and F-B as QA-intake
> **evidence**, F-B as evidence **+ a pointer** to the machine-memory rule (not a duplicate
> standalone backlog item).

## Incident context

An interrupted session left `.dev-knowledge` mid-merge (`chore/qa-bundle-ephemeral-fix-0708`
→ `main`, uncommitted). A maintenance session then accidentally finalized + reverted that
pending merge. **No commits were lost**; `main` was re-derived from live git and the branch
re-integrated cleanly on 2026-07-08 (merge `408a9f8`). Two findings surfaced — recorded here
as evidence for the QA role, whose whole job is to catch exactly this class before it ships.

## F-A — premature closure (success reported ahead of live state)

**What happened:** a session reported "merged `<sha>`, ship-gate GREEN" while the working
tree still held an **uncommitted `MERGE_HEAD`** — the success claim preceded the post-hoc
live read that would have confirmed it.

**Rule candidate (QA-role acceptance posture):** report SHAs and gate verdicts **only from
post-hoc live reads** (`git log -1`, a re-run gate) — never from intended / expected state.
A "done" claim is unverified until a read *after the fact* confirms it. The verifier trusts
the mechanism's output, not the actor's narration. (This arc applied the rule: every SHA and
every ship-gate verdict below was read back from live `git` / a fresh gate run.)

## F-B — maintenance session committed in a live checkout

**What happened:** a maintenance / OS session ran `git commit` in the **live repo checkout**
and finalized a foreign pending merge it did not own.

**Rule (already captured — pointer, not a restatement):** system-verification / maintenance
commits happen in **disposable temp repos only**, never in the live checkout (which may be
mid-merge even when the boot snapshot shows clean); integration goes via the primary
session's `/ship`, never a raw merge from a maintenance session.

**Pointer:** this rule already lives in machine memory —
`memory/system-maintenance-never-commits-in-live-checkout.md` (MEMORY.md-indexed). Per the
operator's 2026-07-08 direction it is filed here as **evidence + pointer only**; it is **not**
duplicated as a second standalone backlog item.

## Disposition

Evidence recorded for the `qa-engineer-role` intake. **No backlog item** filed for either
finding: F-B's rule is memory-resident (pointer above); F-A rides this same evidence record
as a QA-role acceptance-criterion candidate. When the functional QA intake is authored, both
findings are available as ex-ante scenarios / acceptance criteria.
