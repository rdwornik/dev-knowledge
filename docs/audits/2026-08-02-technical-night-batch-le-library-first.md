# Night batch 2026-08-02 · lane L-E — library-first sweep

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-02 · **Slug:** night-batch-le-library-first
- **Status:** PROPOSAL — **no swaps tonight.** No repo file was touched; every experiment ran in a
  scratchpad venv importing the repo's own unmodified functions read-only.
- **Doctrine (intake #23, quoted):** *"Library-first is doctrine: research libraries BEFORE
  implementing anything from scratch."*

---

## 1. The controlling rule, restated before any recommendation

Lane L4 of the 2026-08-01 batch measured `python-frontmatter` against this repo's byte-exactness
contract: **0/20** round-trips. `ruamel.yaml` passed **20/20** — and was *still* the wrong answer,
because the generator templates rather than round-trips, so the contract it would have to survive
was never the one being measured.

**The rule that follows, and that this lane is bound by: a verdict must be MEASURED against the
specific contract at the specific site. A library that breaks a contract is disqualified; a
library that passes a contract the site does not have is irrelevant.**

Accordingly: **3 of 5 candidates below were fully measured with real experiments; 2 are marked
MEASURE-FIRST and are not recommended for anything.** The network was never a limiter — pip,
the PyPI JSON API and the GitHub API all resolved directly, so nothing was downgraded to
MEASURE-FIRST for lack of access.

---

## 2. Ranked shortlist

| Site | Library | Measured verdict | Recommendation |
|---|---|---|---|
| 6× dotted-version parse/compare (`audit.py`, `changelog_sentinel.py`, `enforcement_coverage.py`, `validate_reconciliation.py`, `fleet_parity.py`, `gen_methodology_roster.py`) | `packaging` — **already in the tree** (transitively via pytest) | **SURVIVES** — matched every real version pair tested; **2 real defects found in the hand-rolled code** | **SWAP** |
| 4× hand-rolled DFS cycle detection (`codemap/generator.py`, `codemap/mermaid_emit.py`, `validate_backlog.py`, + a verbatim-mirrored plugin-floor twin) | `networkx` — doctrine-precleared (intake #16 §2, #23 P3), not yet installed | **SURVIVES** — 12/12 and 6/6 matched, including self-loops and disjoint multi-cycles | **SWAP**, riding along with [#383]'s dependency-add |
| TOC anchor slug + dedup (`toc/generator.py`) | `github-slugger` | **SURVIVES fidelity** — 1029/1030 real headers — but the library is **abandoned** (last release v0.0.3, 2022-12-12) | **KEEP** — and write the why-not line into the code |
| 2× fenced-code-block detectors (`coherence_enumerator.py`, `toc/generator.py`) | `markdown-it-py` — already in the tree (via `rich`) | not measured — time budget | **MEASURE-FIRST** |
| ~13× hand-rolled `_git()` subprocess wrappers | GitPython / pygit2 | not measured — sites have *deliberately different* fail-postures and no demonstrated bug class | **MEASURE-FIRST**, leaning KEEP or internal dedup |

---

## 3. The finding that matters most — two real defects in version comparison

This is not a tidiness proposal. The hand-rolled comparator is **wrong**, and the swap is the fix.

`scripts/fleet_parity.py:821` `_version_tuple()` builds a tuple by stripping non-digits from each
dot-separated token. **Verified live by this orchestrator** (read-only, in-memory):

```
'0.15.5'      -> (0, 15, 5)
'0.15.5rc1'   -> (0, 15, 51)      <-- WRONG
'0.15.5-beta' -> (0, 15, 5)       <-- WRONG (different direction)
```

**Correction to the in-lane description, stated rather than absorbed.** The lane reported the
prerelease suffix as "silently dropped". It is not dropped — for a suffix *containing digits* it
is **absorbed into the preceding component**, so `0.15.5rc1` parses as **0.15.51** and compares
*greater* than the release it precedes. A suffix with **no** digits (`-beta`, `-alpha`) is dropped
and compares *equal* to the release. **Two defects, failing in opposite directions**, which is
strictly worse than the single truncation the lane described.

**Live blast radius.** `_satisfies()` and `_declared_ok()` gate the fleet's dependency-parity
reporting. The repo pins `ruff` at exactly `v0.15.5` in both `.pre-commit-config.yaml` and the
`pyproject.toml` required-version floor — so the defect is **dormant today** precisely because no
prerelease is in play. It is dormant, not absent: a `>=`-style floor is exactly where an `rc`
build shows up, and the reporter would silently accept one as a *newer* release.

The second defect the lane found — **compound specifiers silently mangled** — is dormant for the
same reason: `_DECLARED_VERSION_RE` accepts only a single leading operator, so a compound
specifier such as `>=1.0,<2.0` is not parsed as a range.

**Cost of the swap is near zero.** `packaging` is **already resolved** in the environment as a
pytest dependency, so the swap adds no new distribution to the locked gate environment — it
replaces ~10 lines of arithmetic with `packaging.version.Version` and `SpecifierSet`, both of
which implement PEP 440 including prerelease ordering.

**One standing decision found and reconsidered, not silently overridden.**
`scripts/fleet_parity.py:832` documents the choice in its own docstring: *"Tiny dotted-int
comparator (**no packaging dep**)"*. That premise was true when written and is **now stale** —
packaging is transitively free. This lane flags the staleness for the architect; it does **not**
overrule the standing choice, and the swap is a proposal, not a correction already made.

---

## 4. Notes on the other candidates

**networkx (SWAP, with sequencing).** 4 sites hand-roll DFS cycle detection, one of them a
**verbatim mirror** in the plugin floor — so a fix must land twice or the mirror drifts. networkx
is already doctrine-precleared as the intended graph library (intake #16 §2), and ADR-105 gates
its arrival on a **named consumer**, which [#383] supplies. **Recommendation: do not add networkx
for this alone** — ride it along with [#383]'s dependency-add, then collapse the four DFS sites.
Adding it early would install a library ahead of its ruled consumer, which is the exact shape
ADR-105 exists to prevent.

**github-slugger (KEEP).** Fidelity is not the problem — 1029/1030 real headers matched. The
problem is maintenance: last release **v0.0.3, 2022-12-12**. Adopting an abandoned dependency to
delete working code trades a maintained ~20 lines for an unmaintained supply-chain edge.
**Recommendation: keep the hand-rolled slugger and record the why-not in the code**, so the next
sweep does not re-derive this from scratch. That note is the deliverable, not a swap.

**markdown-it-py and GitPython (MEASURE-FIRST).** Neither is recommended, because neither was
measured. Named so the next sweep starts here rather than rediscovering them:
- *markdown-it-py* — free (already present via `rich`); the experiment is whether its fence
  tokenizer agrees with both hand-rolled detectors on the repo's real corpus, including nested and
  unterminated fences.
- *GitPython/pygit2* — the ~13 `_git()` wrappers have **deliberately different failure postures**
  per site (fail-soft in reporters, fail-closed in gates). A library that unifies them would
  flatten a distinction the repo chose on purpose. The likely right answer is an **internal**
  helper that preserves per-site posture, not an external dependency.

## 5. Surveyed and confirmed already correct — not re-proposed

Recorded so a future sweep does not re-open settled ground: `pydantic` already used correctly for
the ADR-109 schema · `pandas` already declared for `fleet_analytics` · `argparse` used properly
repo-wide · `difflib` used correctly in both regen-and-diff gates · frontmatter settled by the
L4 lane. **Table-rendering libraries were correctly never reached for** — CLAUDE.md §4 forbids
column-padded tables, so their absence is a doctrine match, not a gap.

## 6. Blocking questions for the architect

| # | Question | Decision shape |
|---|---|---|
| E-1 | Swap the 6 version-compare sites to `packaging`? It is a **defect fix**, not tidiness, and costs no new dependency. | swap-now / file-a-row / keep |
| E-2 | The two version defects are dormant today. Fix now, or file and wait for a prerelease to bite? | fix-now / file / accept-with-reason |
| E-3 | Collapse the 4 DFS sites onto networkx **as part of** [#383]'s dependency-add, or keep them hand-rolled? | ride-along / keep / separate-row |
| E-4 | Spend a future lane measuring markdown-it-py and the `_git()` wrappers, or close them as KEEP now? | measure / close-as-keep |

---

*Read-only night batch. No swap was performed, no dependency added, no repo file modified. Every
experiment ran in an isolated scratchpad venv against unmodified repo functions.*
