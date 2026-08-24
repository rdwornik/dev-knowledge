# REGISTER ADDENDUM — architect corrections against the 2026-08-24 landed state

Companion to `CANDIDATE-REGISTER-2026-08-24.md`. **The register is accepted as the working
document.** It was distilled without sight of what merged to `main` on 2026-08-24 (68 commits,
pushed), so the corrections below supersede the named fields. The V-lanes read BOTH files; where
they disagree, this addendum governs. The register file itself is not edited — it is the evidence
of what the distillation said.

Authored by the sitting architect. Corrections keyed by row id.

---

## C01 — the `conflicts: none` claim is refuted, and by measurement, not opinion

The register's comment — *"ADR-53 narrow reading already ruled: forbids two content-carrying files,
not the name"* — **is the exact claim the ruling-provenance audit disproved on 2026-08-23/24**:

- The phrase "two content-carrying files" appears **nowhere** in ADR-53. Decision 2 names the file
  and retires it, and **stands un-superseded, Status `Accepted`, today.**
- The shape R-1 admits is materially the alternative ADR-53 **rejected** at `:47`.
- `validate_hermetization.classify('AGENTS.md')` **refuses the file** — verified in a cloud
  container and re-executed on the operator's Windows checkout. Two machines, two interpreters.

**Corrections:** `conflicts: ADR-53 Decision 2 (Accepted, un-superseded) + register ruling R-1 +
intake #42 (filed 2026-08-24, fork: supersede ADR-53 D2 vs retire R-1; architect lean: retire R-1)`.
`disposition: ADOPT → BLOCKED-ON-ADR` — nothing lawful can create the file until the fork is ruled.
`carrier: [#577]` stands but **its Done-when is ruled unexecutable as written** and awaits rewrite.
The *content* claim of C01 (≤120 lines, non-inferable facts only, thin importer) is untouched and
good — it becomes the spec **for whichever surface the ADR fork admits**. Note: the discoverability
need R-1 served is already met — a provider section landed in a sanctioned Tier-1 file on
2026-08-24.

## C14 — partially landed today; reconcile, do not re-derive

R12 (landed as code + test, 2026-08-24): `protocols/STANDING_RULINGS.md` is excluded from the
silent-rule detector's scope. R13 (ruled): the detector's definition is *does the rule have a
normative home elsewhere* — yes → description, drain; no → imperative, count. C14's proposal
(active-rule-ID counting, authorizing ruling per change) is the **next step beyond** R12/R13, not a
fresh start. `conflicts:` add `R12 (landed), R13 (ruled)`. Disposition ADOPT stands, scoped to the
delta.

## C19 — the premise is stale; the deliverable already has a carrier

*"gen_lane_contract is on a dead path"* was **half-refuted by LANE-L7 on 2026-08-24**: a live
`lane-contract-check` hook parses contracts, and the generator's unconditional `Dispatch-Lane`
emission would have made that hook refuse a correct cloud command. L7 rebuilt emission
shape-selective (SHAPE_ENUM local/cloud/interactive, wrong shape refused in all three, merged).
The delivery-gate half of C19 is **legs 2–4 of the contract-integrity intake filed 2026-08-24**.
`carrier: NONE → intake-5 (contract-integrity gate)`. Disposition ADOPT stands.

## C23 — the blocker is false, verified

*"intake #34 is BLOCKED on the operator-held source artifact"* — **refuted in Phase 0**: the
artifact has been in-repo at `docs/archive/2026-08-09-research-code-style-doctrine-wf-8a83eb70.md`
since **2026-08-10**, six days before the intake claiming to be blocked on it. #34's provenance
correction is already appended in-repo. **C23 is executable now.** `conflicts:` replace with
`none — prior blocker disproven, see #34 provenance note`.

## C26 / C27 — likely already decided this window; verify before adopting

M4 closed CLEAN on 2026-08-24: the intake-archival premise was retired and **ADR-100 was reaffirmed
index-only, with the reason recorded**. The V4 lane's first act on these two rows is to locate that
ruling; expected verdict `HAVE <locator>` for C27 and at least PARTIAL for C26. **Neither is
adopted as new work if the locator exists** — that would re-decide a decided thing.

## C28 — half landed today

The status-grammar validator **merged 2026-08-24** (`ALL_CHECKS` 43 → 44, ~147 tests). The marker
sweep exists as **47 proposed corrections, deliberately unexecuted** (ADR-94 discipline). Expected
V4 verdict: `PARTIAL — validator HAVE, sweep proposed-unexecuted`. Disposition ADOPT stands for the
sweep half only, via the ruled ADR-94 path.

## C30 — this is M12; the intake exists and two amendments are already ruled

`carrier: NONE → intake-4 (substrate router, filed 2026-08-24)`. Ruled amendments that bind the
adoption: **(A1)** the table carries THREE off-machine-relevant substrates — `local`,
`cloud-session` (measured: unpinned `uv`, no `click`, no armed hooks, shallow clone — **never
routes gate-dependent work**), `devcontainer` — not a single `CLOUD` cell; **(A3)** docs point at
the table and never restate its numbers; every number carries its measurement date and producing
command.

## C31 — a THIRD capability source, and it is the one nobody has been using

The row reads module exports + PATH scripts. **Measured 2026-08-24 (operator's `git ls-files`): a
third surface exists — `.claude/commands/` (8 commands: `changelog-review`, `handoff-verify`,
`handoff`, `lane-boot`, `lane-integrate`, `override`, `preflight`, `save`) and `.claude/skills/`
(2 skills: `check-against-spec`, `verify` + `verify.py`).** The sitting architect authored an
entire window of lane and integrator contracts in prose without invoking one of them — not by
choice but by ignorance: no bundle names this surface. `changes:` therefore widens: capability
enumeration reads **three** sources, and the generated bundle carries the command/skill list with
one-line triggers so no seat has to remember it.

**V1 addition (read-only, fits its domain):** enumerate all 11 files, return per file its one-line
purpose and trigger, and **flag any procedure inside that conflicts with the 2026-08-24 rulings**
(sentinel-on-tip verification, regenerate-never-pick on generated files, measure-once-at-the-end
for N-dependent values, P-1 lanes-never-journal). A skill that contradicts a landed ruling is a
CONFLICTS verdict with the quote, exactly like any register row.

## C36 — consistent with M1 only if configuration survives the rejection

M1's landed reading: **admission verdicts govern role eligibility only and never block
configuration.** C36's REJECT is a role-eligibility verdict for code-bearing lanes — lawful — but
the provider remains **configured** in the registry with its verdict recorded. The V5 lane should
confirm the registry entry exists rather than treating REJECT as "omit".

## Sequencing note for the operator (not a row correction)

This register + addendum **land on `main` only after L2 and L4 seal** — a `main` advance while two
pinned worktrees are mid-commit is the contention class that has already struck four times, the
fourth corrupting a measurement. Then: commit both files to
`docs/audits/` (exact home derived at landing against the audit-naming convention, not guessed),
push, and dispatch **V1–V5 as five read-only cloud lanes** — read-only verification needs no gate
results, so `cloud-session` is lawful for it under the routing table.

## The verification protocol stands as written

`HAVE <path:line>` · `PARTIAL <missing>` · `ABSENT` · `CONFLICTS <id + quote>` — nothing else, the
lanes rule nothing. One addition: **for every `measured-here` evidence tag, the lane returns the
locator of the measurement artifact too** — a `measured-here` claim without a findable measurement
is downgraded to `practitioner` before it reaches ruling.
