---
intake-id: 70
status: DRAFT
origin: architect inbox 2026-09-05, items 008-A and 009-A; the defect is the operator's finding, recorded 2026-09-05
consumed-by:
---

# Session roles as routing-table rows with a commit-shape carrier

## Problem / motivation

On 2026-09-05 the browser architect assigned two BUILD hotfixes to the integrator session. It spent
roughly 1h48m producing code while six branches waited to be merged. The rule that would have
prevented this — *the integrator merges, never produces* — was real, understood, and agreed. It
simply had no carrier: it lived in the operator's posture and in chat pastes, so no organ knew it
and no organ could refuse it.

That is the class, and the class is what makes this worth an intake rather than a correction:
**a rule that exists only in prose can be violated by the same prose that states it.** The
integrator was not disobeying. It read a paste that told it to build, and nothing in the repo
disagreed. Every role this system runs — lane, reviewer, adversarial, dispatcher, filings, QA — is
in the same position today: named in conversation, carried by nothing.

Left unaddressed it recurs at H0 by construction. At H0 we become a plugin inside a consumer repo,
where the only rules that travel are the ones with carriers. A role that is prose here arrives as
prose there, which is the shape we are trying to stop shipping.

## Scenarios (+1 view)

- As the operator, I hand the integrator session a contract that happens to contain a build step.
  The session's next commit is a one-line `.py` edit; the commit is REFUSED with "integrator builds
  nothing — hand this to a lane", and the work is routed to a lane instead of silently absorbed.
- As the integrator, I merge six branches and regenerate the audits index. Every one of those
  commits passes untouched, because a merge and a regeneration are exactly what my role permits.
- As a consumer repo at H0, I install the methodology floor and receive the roles table and the
  commit-shape hook with it — so my integrator refuses to build for the same reason the hub's does,
  without anyone having explained the rule to me.
- As a reader six months from now, I ask "who is allowed to push?" and the answer is a file I can
  read and a hook I can run, not a person I have to ask.

## Functional requirements

- **Must:** `ecosystem/routing-table.yaml` carries a role row per session role, each with `may`
  and `may_not`. The full set the operator named: integrator, lane, reviewer, adversarial, fan-out,
  read-only/research, dispatcher, filings, QA. Existing rows (reviewer, adversarial, fan_out) are
  extended, not replaced.
- **Must:** the role is knowable at runtime — a session's role is set in its environment
  (`CLAUDE_SESSION_ROLE=integrator|lane|filings|dispatcher|...`) by the command that boots it,
  `/lane-integrate` for the integrator and `/lane-boot` for lanes.
- **Must:** a commit-shape carrier. With `CLAUDE_SESSION_ROLE=integrator`, a commit that is neither
  a merge (>= 2 parents) nor a regeneration touching only generated-allowlist files is refused.
- **Must:** the roles table AND the hook are CARRIED BY THE MANIFEST, not hub-only. A consumer
  receives them with the floor.
- **Should:** each role row names its own carrier, so a role with no carrier is visible as such
  rather than looking identical to a carried one.
- **Could:** roles beyond the integrator gain their own commit-shape predicates once the integrator
  one has run long enough to show its false-positive rate.

## Acceptance criteria (ex-ante)

Written as the tests to run, per the template's instruction. The mechanism detail here is the
architect's and is recorded as acceptance rather than as design.

1. Seeded refusal: a one-line `.py` edit committed by a session with
   `CLAUDE_SESSION_ROLE=integrator` is REFUSED, with refusal text naming the remedy
   ("integrator builds nothing — hand this to a lane").
2. Seeded pass: a `--no-ff` merge commit by the same session passes.
3. Seeded pass: a regeneration commit touching only generated-allowlist files (doc-counts,
   rosters, indexes, JOURNAL anchor lines) by the same session passes.
4. `ecosystem/routing-table.yaml` carries all nine named roles, each with `may`, `may_not` and a
   carrier field.
5. The roles table and the `role-commit-shape` hook appear as payload entries in
   `deploy/manifest-v*.yaml`; a consumer installing the floor receives both. **This criterion is
   the 009-A amendment and is not optional** — without it the fix is hub-local by definition.
6. The refusal is demonstrated on a consumer clone, not only in the hub.

## Non-goals

- Not a permissions system. This constrains the SHAPE of a commit by declared role; it does not
  authenticate who a session is, and a session that lies about its role is out of scope.
- Not a rewrite of the existing routing rows. `reviewer`, `adversarial` and `fan_out` keep their
  meaning; they gain `may`/`may_not` and a carrier.
- Not an attempt to carry every prose rule at once. This carries ROLES. The wider census of
  prose-only behavioural rules is item 008-B's deliverable and is deliberately separate.

## Impact sketch (4+1 lite)

- **Logical:** roles become first-class objects with declared capability, rather than adjectives
  used in conversation.
- **Process:** the integrator stops being able to absorb build work, which is the behaviour change
  the defect asks for; contracts that contain build steps get routed rather than executed.
- **Development:** one new pre-commit hook plus role rows; no new dependency.
- **Physical:** the manifest payload grows by the table and the hook. Consumers receive both at
  their next floor install.

## Open questions

- What exactly belongs in the generated-allowlist for criterion 3? The list must be derived from
  the existing generated surfaces rather than hand-typed here, or it becomes a second roster that
  drifts. Technical-architect question; not answered speculatively.
- Does `filings` need `may_not: [merge]`? This session's whole posture is commit-and-hand-off, so
  the row would carry it — but that is a ruling, not an inference, and it is recorded rather than
  assumed.
- How does a session that legitimately changes role mid-life (an integrator that becomes a lane
  after the queue drains) re-declare? Unresolved; possibly out of scope.

## Reconcile-before-birth

Run before filing, per intake #66's binding rule, rather than asserted:

- `[#241]` undeclared-edge groom — `status: deferred`, E2/S. Different object: it grooms declared
  vs actual EDGES between docs, not session capability. Not a duplicate.
- `[#552]` window-close disposition + archival routine — `status: open`, E2/M. Different object:
  audit/ADR/intake lifecycle at window close. Not a duplicate.
- `[#635]` "SessionStart refuses a non-integrator session on the primary" — **SAME FAMILY, and it
  is the one to fold.** It carries the entry-time half of "who may do what on the primary"; this
  intake carries the commit-time half. One carrier should own both, and 008-A says to fold it in.
  **Locator warning:** `[#635]` is NOT on `main`. It exists only on the unmerged branch
  `worktree-file-candidates` (tip 26d7d743), alongside `[#636]`. Whoever executes this intake must
  re-resolve it after that branch merges; until then the fold is declared here and cannot be
  performed against a row on main.

## Status

DRAFT. Filed 2026-09-05 from architect inbox items 008-A and 009-A, amended by 009-A before filing
rather than after. Not ratified; ADR-111 admits one path — CANDIDATE, then intake, then
ratification — and this is the intake step only.
