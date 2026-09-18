# SDA-1 — a run attempt against its own design, and why it did not start

- **Class:** technical · **Date:** 2026-09-18 · **Lane:** `lane-ac-661-evals` (`[#661]`)
- **Head under test:** `87638c8d` (branch `worktree-lane-ac-661-evals`, off `main`), clean tree
  before and after — no code, harness or pack was written or run by this lane.
- **Design under test:** `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md`
  (SDA-1 §§1–8, plus its own §9 adversarial self-review and §10 verdict).
- **Outcome: SDA-1 DID NOT RUN.** Per `[#661]`'s own contract, "cannot run" is an acceptable and
  useful outcome only if the exact reason and the missing input are named. Both are below,
  evidenced rather than asserted.

---

## 1. Organ check (contract §"Organs and rows")

`ecosystem/organ-index.md` — the generated roster of all 66 organs across 8 classes (agent /
command / skill / workflow / rule / session-hook / git-hook / plugin) — was read in full and
grepped for `sda|eval|benchmark|harness` (case-insensitive). **Zero matches.** No organ answers
"run SDA-1"; none exists to name, and none was skipped. `scripts/preflight_contract.py` and
`tests/test_preflight_freeze_predicates.py` match `SDA-1` textually, but only as an example
string inside preflight's own docstring/tests illustrating an *unopenable-locator* failure mode
— neither is an SDA-1 harness. No new code was written to search for one; this section is a
read-only report of that grep and that read.

## 2. What has actually been run under SDA-1's name, and what has not

SDA-1 (§1) enumerates exactly **four roles**: producer (24 items), reviewer (20 items),
adversarial (12 items), fan-out (15 items, the reused C1 pack). Tracing every artifact this repo
has ever produced against those four packs:

| role | item pack authored as a runnable artifact? | ever dispatched to a live provider under SDA-1's own gates? |
|---|---|---|
| producer (`SDA1-P-*`, 24) | **NO** — §3.2 states counts and classes only | NO |
| reviewer (`SDA1-R-*`, 20) | **NO** — same | NO |
| adversarial (`SDA1-A-*`, 12) | **NO** — same | NO |
| fan-out (`C1-*`, 15, reused) | YES — pre-existing, committed pack | YES, but **before SDA-1 existed**: run 2026-08-20 (Gemini/Grok A/B), 8 days before SDA-1's design landed 2026-08-28. Never re-run under SDA-1's own F0–F2 + G1v2/G2/G3 as such. |

This is not this lane's inference; it is the finding of the one lane that went looking for a
runnable SDA-1 pack to test a harness translation against
(`docs/audits/2026-08-31-technical-dm1-eval-comparison.md` §0, 2026-09-01):

> "SDA-1 … defines four role packs (producer 24, reviewer 20, adversarial 12, fan-out 15). None
> of those has a completed, recorded hand-rolled run small enough to re-run inside this lane's
> budget — **except one**: SDA1-N, the 10-item analysis-role acceptance probe."

SDA1-N is not a discount on that count. Its own freeze document says so explicitly
(`docs/audits/2026-08-29-technical-sda1-analysis-role-freeze.md` §1): "SDA-1 … enumerates four
roles: producer, reviewer, adversarial, fan-out. **There is no `analysis` role in either**
[SDA-1 or `ecosystem/routing-table.yaml`]. This lane's contract asks to staff one, so the role is
defined here." SDA1-N is a different, ad-hoc role, invented for an unrelated lane
(`night-batch-2 wave 2, lane O`), scored against a 10-item probe pack the SDA1-N document itself
calls "one tenth the size SDA-1 designs per provider… sizes an acceptance *probe*, not an
acceptance" (§9 lim.3). It is evidence about a role SDA-1 does not have, not evidence that SDA-1
ran.

Likewise, `docs/audits/2026-08-29-technical-sda1-adversarial-incumbent-baseline.md` is not a run
of the 12-item `SDA1-A-*` adversarial-role pack. It is an adversarial **code-review of the design
document itself** — scoring the design's own §9 critique (C-1…C-15) against the unrelated
SDA1-N packs 2/3 as the only available execution evidence, and it says so in its own second
bullet: "What it is: the incumbent baseline itself, not a verdict… nobody had run this pack as a
baseline."

**Conclusion, evidenced: zero items from SDA-1's producer, reviewer or adversarial packs have
ever been dispatched to any provider, and the fan-out pack's only live run predates SDA-1's own
design and was never re-scored under it.**

## 3. Why it cannot run today — the missing inputs, named

**(a) PRIMARY — the seed corpus does not exist as a runnable artifact for three of four roles.**
SDA-1 §3.1–3.2 states item *counts and defect classes* (`D01`…`D16`, the 24/20/12 split) in
prose. It authors no actual item: no frozen prompt bytes, no ground-truth statement, no
machine-checkable pass predicate, for any `SDA1-P-*`, `SDA1-R-*` or `SDA1-A-*` item. A design
description is not a corpus. There is nothing for a provider to be invoked against for these
three roles, and authoring that corpus now would be **building the benchmark, not running it** —
explicitly out of this lane's scope (`[#661]`'s Done-contract clause 4: "This lane RUNS what is
designed. It does not widen the design").

**(b) The producer role's named guard no longer exists.** SDA-1 §2's precondition table requires,
before any run starts: `Q0 guard armed — scripts/nopack_sandbox.py provisioned once, shared by
all lanes`. That file — and its test, `tests/test_nopack_sandbox.py` — was ratified for deletion
and removed from this repository on 2026-09-13, commit `f7f04c41` (`feat(x-664): retire
nopack_sandbox and trace_writer -- the last two of the ratified six`), as an orphan with zero
consumers: "nopack_sandbox has 0 consumers and 1 outbound import." Even if a producer pack
existed, the sandboxed-write guard the design names by path does not. (Read-only roles —
reviewer, adversarial, fan-out — do not need this guard, per the analysis-role freeze's own
reasoning for why it marked Q0 not-applicable to a non-writing role: `docs/audits/2026-08-29-
technical-sda1-analysis-role-freeze.md` §5.)

**(c) Two of four role incumbents remain unmeasurable under the design's own Rule B0.**
`docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md` §1 flags both at
authoring time: the fan-out incumbent (`claude-haiku-4-5-20251001`) was billing-blocked (HTTP 400
"credit balance too low", `req_011CeKV6v3zFbPmu29SHYnph`, measured 2026-08-23), and no
adversarial-role incumbent (`claude-opus-4-8`) has ever been run. The same billing block was
re-measured 2026-08-29 under a different call (`req_011CeWnLW9y4qixTcbaZuUdG`,
`docs/audits/2026-08-29-technical-sda1-analysis-role-freeze.md` §7). **This lane did not
re-measure it today** — a live provider call is a curated-baseline touch (contract decision
budget class (a)) and is deliberately not spent to produce this artifact; the state above is
reported as last-measured 2026-08-29, not re-verified 2026-09-18, and that gap is named rather
than smoothed over. Per Rule B0, either blocker alone caps its role at absolute-floors-only, not
a full stop — but it compounds with (a): there is no absolute floor to apply without items.

**(a) is the decisive blocker.** (b) and (c) would each independently stop a producer or
fan-out/adversarial run even if a corpus existed; (a) means there is no corpus for three of the
four roles to run into, regardless.

## 4. Deviation record (contract Done-contract clause 2)

- This lane did **not** author a substitute or reduced seed corpus for producer, reviewer or
  adversarial. Doing so would satisfy clause 1 by widening the design, which clause 4 forbids.
- This lane did **not** re-run the fan-out (`C1-*`) pack under SDA-1's own gates using its
  pre-2026-08-28 result, and did not treat that prior result as an SDA-1 run — the design
  postdates that run by 8 days and was never applied to it.
- This lane did **not** issue a live call to re-check either blocked incumbent's billing state
  (§3(c)) — reported as a named gap, not resolved.
- No code was written, no organ was invoked, no pack was built. This artifact is the entire
  footprint of the lane.

## 5. What would unblock a future attempt (informational; not a ruling, not a `tasks/` write)

1. Author the producer/reviewer/adversarial item packs as real files (prompt + ground truth +
   pass predicate) — a build task, distinct from a run task, and not this lane's to start.
2. Either restore a sandboxed-write guard at the path SDA-1 names, or rule that producer-role
   SDA-1 is out of scope until one exists, so the design's own precondition is not silently
   unenforceable.
3. Clear the fan-out incumbent's billing block (or name a replacement incumbent), and run the
   adversarial incumbent once, in-window, per Rule B0.

## 6. What this lane did not touch

No merge, no push to `main`, no branch but its own. No `JOURNAL.md` entry (integrator surface,
`protocols/STANDING_RULINGS.md` P-1). No index regeneration beyond what committing this file into
`docs/audits/` mechanically requires (`audit-index-freshness`, run and committed alongside this
file — the generated `docs/audits/README.md` diff is the row for this file, nothing else). No
`tasks/` write, no row birth, no change to `[#661]`'s status: its Done-when, quoted in this
lane's contract, requires SDA-1 to run; this artifact reports that it did not, and `[#661]` stays
open on that basis rather than being closed by this lane.
