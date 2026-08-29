# NB2 · WAVE 2 · LANE K — FM-4: the boot surface — hand-back packet

**Batch:** night-batch-2, wave 2 · **Lane:** K (FM-4) · **Date:** 2026-08-29
**Branch:** `worktree-lane-k-4-fm-boot-surface` · **Substrate:** local
**Contract:** `docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FM-4, dispatched as
`NB2-W2-LANE-K-FM4-boot-surface.md`.

---

## 0. FIRST ACT — the assembler's path, witnessed

The contract deliberately did not name the module. It is **`scripts/gen_handoff.py`**, and the
evidence is read, not assumed:

| Claim | Witness |
|---|---|
| It is the module that assembles a bundle | `scripts/gen_handoff.py:1-5` — *"the v5 handoff bundle generator … Assembles a valid v5 bundle (HANDOFF_BOOT + RESIDUAL + PROBES + SUPPLEMENT, then PASTE_THIS via `scripts/assemble_paste.py`) from COMMITTED repo state"* |
| The assembly entry point | `scripts/gen_handoff.py::generate` (line 1019 at HEAD~2) — resolves the bundle dir, `mkdir`s it, renders each file, seals, then shells out to the paste assembler |
| It writes the bundle, and only the bundle | `scripts/gen_handoff.py:32-33` — *"Layer-2 / read-only w.r.t. tracked spine files: writes ONLY `<bundle>/*`"* |

**The near-miss, named rather than left implicit.** `scripts/assemble_paste.py` is the module
whose *name* says "assembler", and a contract reading of "the handoff assembler module" could
land there. It is **not** the bundle assembler: it is the downstream **paste folder**, invoked as
a subprocess by `generate` (`gen_handoff.py:1160`), and its own manifest is a two-entry required
list (`assemble_paste.py:247-250` — `RESIDUAL.md`, `PROBES.md`). The contract body settles it by
naming `gen_handoff` explicitly. Recording the distinction because "probably right" is the premise
class the contract warned about, and here the obvious candidate was right for a reason that had to
be read to be known.

---

## 1. Per-done-item verdicts

### Contract's Ex-ante line, verbatim

> Ex-ante: the next assembled bundle carries the block; a golden test pins its shape.

### Measured against it

| # | Done-item | Verdict | Witness |
|---|---|---|---|
| 1 | `gen_handoff` emits a generated FUNNEL HEALTH block **in every bundle** | **PARTIAL** | Emitted in `architect`, `execution` and `epic`; **not** in `functional`. Reason is a protocol line, not a preference — see §6 D-1. Tests: `test_assembled_bundle_carries_the_funnel_health_block[architect|execution]`, `test_epic_bundle_carries_the_funnel_health_block`, `test_functional_bundle_stays_one_file` |
| 2 | Five fields: intakes consumed-unarchived / ADRs unexecuted / orphans **both directions** / rows closed this window / value evidence attached | **MET** | `gen_handoff._FUNNEL_FIELDS`; the golden pins the labels **and their order** as literals (`test_funnel_health_block_shape_is_pinned`, `test_golden_literals_and_the_production_constants_agree`). "Both directions" is rendered as two numbers: *orphans forward (object -> consumer)* and *orphans backward (open row -> resolving source)* |
| 3 | Numbers only — **no verdicts, no shas** (anti-bluff intact) | **MET** | `test_funnel_health_block_carries_no_verdict_and_no_sha` refuses `GREEN\|RED\|PASS\|FAIL\|WARN\|healthy\|degraded`, any 7+ hex run, and any `#\d+`, over the whole block. Format is pinned to `<label>: (\d+\|unavailable)` per field |
| 4 | Sourced from **the same derivations FM-2 uses** (one truth) | **MET as written, coupling UNPROVEN** | Nothing is re-implemented here: the entire coupling is four constants (`_FUNNEL_MODULE`, `_FUNNEL_ENTRY`, `_FUNNEL_SOURCE`, `_FUNNEL_FIELDS`) plus `_load_funnel_measure`. FM-2 had not landed — see §1a. The block degrades to `unavailable`, never to an invented number (`test_funnel_health_degrades_honestly_when_fm2_is_absent`) |
| 5 | Ex-ante a: **the next assembled bundle carries the block** | **MET at the level testable tonight; end-to-end MEASUREMENT-OWED** | `generate(..., assemble=True)` writes `<bundle>/FUNNEL_HEALTH.md` for both v5 modes. A cut against the **live** repo is refused — witnessed, see §1b |
| 6 | Ex-ante b: **a golden test pins its shape** | **MET** | `test_funnel_health_block_shape_is_pinned` pins the two delimiters, the heading, the source-line prefix, the six labels, their order and the numbers-only format — as **literals**, not as re-derivations of the production constants (that was terra H2; see §3) |
| 7 | Regenerated, not carried — *a stale block is worse than none* | **MET, with a seeded-violation witness** | `test_funnel_health_is_regenerated_not_carried`. Discrimination proved by seeding the exact violation (an early `if out.exists(): return out` in `write_funnel_health`): the test **FAILED** — `AssertionError: assert 'STALE' not in 'STALE — a previous window\n'` — and the source was restored byte-identically in the same run |

### 1a. FM-2 had not landed — the evidence, and what was done about it

`worktree-lane-i-2-fm-funnel-lifecycle-check` resolved to **`77096131`**, which is `main`'s tip:
the lane carried **zero commits** (`git log --oneline main..worktree-lane-i-2-…` → empty). There
was no module to read. Per the contract's instruction the block is written **against FM-2's
declared module path and says the coupling is unproven until it lands**, and the block says so in
the artifact itself rather than only here:

```
<!-- FUNNEL-HEALTH:BEGIN (generated by gen_handoff — do not edit) -->
## FUNNEL HEALTH (generated — numbers only)

source: scripts/funnel_lifecycle.py::measure (FM-2) — not importable — FM-2 has not landed; this coupling is unproven

intakes consumed-unarchived: unavailable
ADRs unexecuted: unavailable
orphans forward (object -> consumer): unavailable
orphans backward (open row -> resolving source): unavailable
rows closed this window: unavailable
value evidence attached: unavailable
<!-- FUNNEL-HEALTH:END -->
```

That is the block rendered against the **live repo at HEAD**, verbatim.

**The module path is a prediction, and it is named as one.** `funnel_lifecycle.measure(repo_root)`
mirrors the one landed precedent for exactly this shape — `scripts/funnel_coverage.py::measure`,
which `audit.py::check_funnel_coverage` imports at `audit.py:170-172`. The frozen bundle's §FM-2
says only *"new check module + registration (audit.py) + tests"*; it does not name the file. **If
lane I named its module or its fields differently, the four constants at `gen_handoff.py`
`_FUNNEL_MODULE` … `_FUNNEL_FIELDS` are the entire fix** — that is the whole surface area of the
guess, and it is why the guess was concentrated there rather than spread through the renderer.

### 1b. End-to-end assembly — MEASUREMENT-OWED, and the refusal is witnessed

`gen_handoff` refuses to cut while any worktree is live and ships no override. Rather than assert
the hazard from the contract, it was reproduced against the live repo (writing into a throwaway
`bundle_root`, so `docs/handoffs/` was never touched — the guard fires *before* `mkdir`):

```
BoundaryHygieneError: refusing to generate: the tree is not at a clean session boundary —
linked worktree …/lane-h-1-fm-lifecycle-doctrine; …/lane-i-2-fm-funnel-lifecycle-check;
…/lane-j-3-fm-visible-shrinkage; …/lane-k-4-fm-boot-surface; …/lane-l-5-fm-governance-health;
…/lane-m-1-fpg-file-purpose-graph; …/lane-n-1-db-dashboard-successor; …/lane-o-4-agy-acceptance.
```

**Eight** linked worktrees. So the ex-ante's "the next assembled bundle" cannot be produced tonight
by anyone, and the honest state is: **the block is proven at the assembler's own function and
through `generate(assemble=True)` into a temp bundle root; a real cut is MEASUREMENT-OWED until the
lane worktrees are torn down.** The workaround was not taken.

---

## 2. Commit SHAs, in order

| # | SHA | Subject |
|---|---|---|
| 1 | `20d772c6` | `feat(handoff): FM-4 -- gen_handoff emits a generated FUNNEL HEALTH block in every multi-file bundle` |
| 2 | `9b4f6107` | `fix(handoff): FM-4 -- three terra HIGHs closed on the FUNNEL HEALTH block` |
| 3 | *(this packet)* | `docs(audits): FM-4 lane-K hand-back packet` |

Diff footprint: `scripts/gen_handoff.py` + `tests/test_gen_handoff.py` only — the contract's
write-scope, nothing else. **No** generated surface was regenerated, **no** `tasks/` write, **no**
row closed, **no** JOURNAL entry (see §5).

---

## 3. Terra tally — `codex exec` over the working-tree diff

**TALLY: critical=0 high=4 medium=0 low=0** (codex-cli 0.145.0, 58,621 tokens).

| ID | Finding | Disposition |
|---|---|---|
| H1 | *Functional mode is excluded, violating the frozen requirement that every bundle carry FUNNEL HEALTH.* | **DISPUTED with evidence, and reported not buried.** `protocols/HANDOFF_PROCESS.md:949` §16 pins the mode: *"**The boot (one file, generated).**"* — and at :966-972 narrows the answer-free invariant there to *"no counts, SHAs, verdicts, or date-relations enter the boot"*. A counts file in a functional bundle breaks both. Amending §16 is `protocols/`, which this lane's ratchet fixes at delta 0. Architect's call — §6 D-1 |
| H2 | *The "golden" derives delimiters from production constants and uses prefix checks, so shape regressions can pass.* | **ACCEPTED, fixed.** The golden now spells `_GOLDEN_BEGIN` / `_GOLDEN_END` / `_GOLDEN_HEADING` / `_GOLDEN_SOURCE_PREFIX` as literals and asserts first/last line **equality**; `test_golden_literals_and_the_production_constants_agree` keeps the literals bound to what ships |
| H3 | *Trying the bare module name first can load an unrelated `funnel_lifecycle` and emit its numbers while falsely attributing them to FM-2.* | **ACCEPTED, fixed.** `scripts.funnel_lifecycle` is now tried **first** (`scripts.` names this repo or nothing). `test_funnel_source_prefers_the_package_qualified_module` plants two rival modules and asserts ours wins. Carried further than the finding asked: a module that **exists but cannot import** is now reported as *"present, but its import raised …"* rather than as *"has not landed"* — two different facts, and the block must not assert the wrong one |
| H4 | *FUNNEL_HEALTH is overwritten before fallible rendering and sealing, so a failed regeneration can leave a bundle in a mixed state.* | **ACCEPTED, fixed.** The write moved **after** `verify_seal_identity` on both the v5 and the epic path, so a refused cut cannot leave a fresh health block beside stale renders |

---

## 4. Candidate filings — reported, never filed

- **CF-1 · The FM-2 coupling is unverified and nothing detects that.** If lane I ships a different
  module name or field names, the block renders six `unavailable`s and **every gate stays green** —
  a silent degrade. Candidate: at integration, once FM-2 is on `main`, assert
  `gen_handoff._load_funnel_measure()` returns a callable and that no field is `unavailable`
  against the live repo. That test cannot be written tonight without pinning it to a module that
  does not exist. **Owner: integrator.**
- **CF-2 · A1 time-series is NOT taken, and the store is named.** The existing telemetry store is
  `scripts/telemetry_emit.py`, SQLite/WAL at `logs/TELEMETRY.db` (`telemetry_emit.default_db_path()`
  — resolved live, not quoted). It was **found before designing**, per A1. It was **not written
  to**, for three stated reasons: (a) its event-type set is `check_run` / `hook_run` /
  `blocker_fired` — none fits a funnel-health snapshot, so a fourth type would be needed; (b) that
  edit is `scripts/telemetry_emit.py`, outside this lane's write-scope; (c) the module's own
  docstring pins the state of the slice — *"it **wires nothing** … Wiring the call sites is an
  explicitly owed phase-3 step"* ([#529]). Emitting funnel-health as append-only records with a
  derived view is a clean phase-3 call site. **Owner: architect / [#529].**
- **CF-3 · The block is bundle-visible, not browser-visible, and that was a choice.** It is absent
  from `assemble_paste`'s required list, so it never folds into `PASTE_THIS.md`. That keeps the
  §5 answer-free invariant intact where it is actually stated (BOOT / RESIDUAL / PROBES + the
  paste) at the cost of the browser seat not seeing the numbers. If the architect wants the
  browser to see them, that is an `assemble_paste` manifest change **and** an amendment to the
  answer-free invariant — one act, not two silent ones. **Owner: architect.**

---

## 5. Budget decisions

- **RATCHET.** Measured with `scripts/silent_rule_detector.py`, **before first commit** and
  **after last code commit**: `detector: silent-rule-v5 · files: 61 · count: 443` → **443**.
  **Delta 0.** No `protocols/` or `templates/` file was touched. (Measured, not assumed to be 443 —
  it independently reproduced the wave-1 dispatch figure.)
- **Write-scope held to two files.** Everything the contract's five fields need is expressible in
  the assembler; no template token was added, which is why `templates/` delta is 0 without
  argument.
- **New file in the bundle, rather than an append into a rendered file.** Appending the block into
  `HANDOFF_BOOT.md` would have put counts into a browser-visible file and into the paste, breaching
  the answer-free invariant documented at `gen_handoff.py:11-15` and `HANDOFF_PROCESS.md:1008`.
  A dedicated `FUNNEL_HEALTH.md` satisfies "in every bundle" without breaching it. **No existing
  test asserts an exhaustive bundle file-set**, so this adds no collateral RED (verified:
  `test_functional_bundle_is_one_file` and `test_epic_bundle_writes_contract_files_and_no_v5_files`
  both assert *named absences*, not a closed set).
- **No JOURNAL entry.** Declined explicitly, with the reason: the integrator writes one anchor for
  the whole queue after every lane STOPs (contract §"THE FOUR THINGS", ADR-85 amendment
  2026-08-03 §A5 — the Stop hook is advisory in full; the hard leg is `block-unanchored-push`, and
  a lane does not push).
- **No self-merge, no push.** Branch `worktree-lane-k-4-fm-boot-surface` enters the frozen queue.

### Tests

Targeted only, per the contract. `tests/test_gen_handoff.py`, `tests/test_handoff_modes.py`,
`tests/test_assemble_paste.py`, `tests/test_verify_handoff_probes.py`:

- before the terra fixes: **204 passed**, 0 failed
- after the terra fixes: **206 passed**, 0 failed (65s)
- `ruff check` on both changed files: **All checks passed!**

**No inherited RED had to be disproved** — the targeted set is fully green, so neither the
anchor-gate probe test nor `test_stale_worktrees` is in it. The **full suite was not run**; that
is integration's, once.

### RED-first, shown

| Witness | Before | After |
|---|---|---|
| The nine new funnel tests against un-implemented code | **1 failed + 8 errors** — `AttributeError: module 'gen_handoff' has no attribute '_FUNNEL_MODULE'` / `… '_load_funnel_measure'` | 16 passed |
| **Seeded violation**: `write_funnel_health` made to skip when the file exists (the exact "carried block" defect) | `test_funnel_health_is_regenerated_not_carried` **FAILED** — `assert 'STALE' not in 'STALE — a previous window\n'` | restored byte-identically; test green |

The second row is the one that matters: it proves the assertion **discriminates**, not merely that
it runs. `test_functional_bundle_stays_one_file` is disclosed as **green from the start** — it is
a scoping guard, not a RED-first deliverable, and it is not claimed as one.

---

## 6. Deviations, with owners

- **D-1 · `functional` mode carries no block — the one departure from "every bundle."**
  **Owner: Layer-1 architect.** `protocols/HANDOFF_PROCESS.md:949` pins functional at *"The boot
  (one file, generated)"* and :966-972 narrows the answer-free invariant there to *"no counts,
  SHAs, verdicts, or date-relations enter the boot"*. Emitting counts into that mode breaks a
  landed protocol; amending the protocol is outside a lane whose ratchet is delta 0. The contract's
  **executable** ex-ante — *"the next **assembled** bundle carries the block"* — is unaffected:
  functional mode assembles nothing (no `assemble_paste` call). Decision owed: amend §16 to admit
  the block, or ratify the exclusion.
- **D-2 · The five contract fields render as six lines.** *"orphans, both directions"* is one
  contract field carrying two numbers; collapsing them would lose the direction. Named here so the
  golden test's six-line body is not read as scope drift.
- **D-3 · The `source:` line is not a number.** The block is *numbers only* in its **fields**; it
  also carries one `source:` line naming the derivation module and, when a number could not be
  derived, why. That is provenance, not a verdict — and without it a reader cannot tell
  "unavailable" from "zero". Flagged rather than assumed acceptable.
- **D-4 · No end-to-end cut.** §1b. `MEASUREMENT-OWED` until the lane worktrees are gone.

---

**STOP.** Branch `worktree-lane-k-4-fm-boot-surface`, three commits, no push, no merge.
