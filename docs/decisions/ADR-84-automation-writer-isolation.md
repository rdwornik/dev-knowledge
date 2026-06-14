# ADR-84: Automation-writer outputs are fully isolated from main (Q9)

**Status:** Accepted
**Date:** 2026-06-13
**Number:** 84
**Decides:** Q9 — automation-writer coexistence with the `--no-ff` feature workflow (both Q9a branch policy and Q9b gate exemption)
**Evidence:** AI Council debate `docs/decisions/transcripts/council-out-20260613_225513-pick-council-q9-automation-writers.md`; read-only fact verification (this session)

## Context

Two scheduled, unattended writers commit output into the repo:
- conformance digest — `docs/audits/<date>-conformance-nightly-digest.md`
- fleet-audit baseline — `docs/audits/<date>-ecosystem-audit.md` + `ecosystem/<repo>/history/<date>.md` (written by `scripts/audit.py`, per ADR-80)

They commit directly to `main`, which created four problems: (1) the digest trips `no_ff_merges`, cleared by manual disposition entries; (2) automation commits ride into feature branches cut after them, forcing manual exclusion at integration (the #156/#163 cherry-pick); (3) automation writes to `origin`, so local `main` diverges (behind-N), requiring a reconcile before pushing; (4) an asymmetry — `no_ff_merges` (#153, `_is_automation`) already auto-exempts the baseline writer via its `chore(routine/...)` / `Routine:` marker, but the digest writer carries no marker and still trips the gate (hence disposition `warn-61c5b50`).

An AI Council debate recommended a dedicated automation branch with no gate exemptions, conditional on a fact it could not resolve — whether any consumer requires the outputs on `main`. Read-only verification resolved both open facts:

- **Fact 1 — no hard consumer pins either output to `main`.** The baseline has zero readers (`audit.py` writes but never reads a prior baseline; `docs/audits` is excluded from its checks). The digest has one soft reader — `surface_triage.ps1`'s SessionStart probe queries the default branch and nudges if the digest is absent — which is fail-soft (never gates) and repointable in one line.
- **Fact 2 — outputs are append-only with date-unique filenames.** Each run writes a new dated file; nothing is removed. Because filenames are date-unique and there is a single writer per stream, additive merges never collide, so no merge-cleanup step is needed. The only consequence of append-only is unbounded directory growth (a retention concern, independent of branch policy).

## Decision

**Fully isolate automation output from `main`.**

1. **Branch policy (Q9a):** each writer commits only to its own dedicated branch (`automation/conformance-digest`, `automation/fleet-audit`) — never merged into `main`. Per-stream branches avoid concurrent-push races between the two writers.
2. **Consumer repoint:** repoint `surface_triage.ps1`'s digest probe to read from the digest's automation branch (`?ref=automation/conformance-digest` on the `gh api` call). One line. The baseline has no readers to repoint.
3. **Gate (Q9b):** once the writers no longer land on `main`, **remove** the `_is_automation` marker-exemption from `no_ff_merges` (#153). With no automation on `main`, the exemption is dead code and a spoofable backdoor; removing it restores the gate to one rule — every non-merge commit on `main` is a violation, no exceptions. Retire the digest disposition (`warn-61c5b50`).
4. **Legacy:** automation commits already on `main` are left in place (no history rewrite); the policy is forward-only. `main`'s `docs/audits/` freezes at its current set; live automation accumulates on the branches.
5. **Retention:** unbounded growth of the automation branches is a deferred follow-up (prune/retention policy), not addressed here.

**Sequencing (order matters):** retarget writers to their branches → repoint `surface_triage.ps1` → only then remove the `_is_automation` exemption and retire the disposition. Removing the exemption before the writers retarget would red the gate on the next digest run.

## Consequences

**Positive**
- `no_ff_merges` becomes a single high-signal rule — no exemption, no marker allowlist, no spoofable backdoor. Any non-merge commit on `main` is unambiguously a violation.
- The integration merge-collision (problem 2) is eliminated structurally: feature branches cut from `main` never inherit automation commits — no cherry-pick / rebase / dedupe at merge.
- Local `main` stops diverging from `origin/main` due to automation (problem 3): automation no longer writes to `main` on local or origin.
- The manual disposition register is retired for routine automation (problems 1 and 4).

**Costs**
- One-line repoint of `surface_triage.ps1` (or a daily false "silent-skip" nudge until repointed).
- A small one-time retarget change to each writer (branch target).
- `main`'s `docs/audits/` no longer reflects current automation state; maintainers/readers look at the automation branches for the latest digest/baseline.
- Automation branches grow unbounded until a retention policy is added (deferred).

**Revisit if:** a hard consumer of the outputs on `main` appears (would force a publish-to-main merge cadence instead of isolation); a second maintainer joins (branch protection on the automation branches becomes more important); automation cadence or branch size makes retention urgent.
