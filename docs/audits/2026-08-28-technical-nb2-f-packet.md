# night-batch-2 · LANE F packet — CANDIDATE C-A: the [#577] byte-cap test

**Batch:** night-batch-2 · **Architect's lane id:** N7 · **Branch:** `worktree-lane-f-577-byte-cap`
**Substrate:** local · **Date:** 2026-08-28 · **Status at hand-back:** committed, unmerged, STOPped.

Intent, restated from the frozen contract: batch-1 landed the root `AGENTS.md` and *measured*
the Codex instruction payload, but reported it **UNGUARDED**. The figures existed; the gate did
not. This lane is that gate.

---

## 1. Per-done-item verdict

### Done-item 1 — "a test asserts the combined payload IN BYTES against the cap" · **MET**

`tests/test_agents_md_byte_cap.py`, one new file, 216 lines, 8 tests, one parametrised helper
`assert_within_cap(*docs, cap=CAP_BYTES)`. Sizes come from `Path.stat().st_size` — bytes on
disk — and never from `len(read_text())`, which would under-report every non-ASCII byte and
every CRLF. Nothing in the module asserts a line count.

Witness:

```
$ uv run --locked pytest tests/test_agents_md_byte_cap.py -n 0 -v -s
tests/test_agents_md_byte_cap.py::test_tracked_payload_is_within_cap
payload 9,430 B = 28.78% of 32,768 B cap
PASSED
tests/test_agents_md_byte_cap.py::test_live_codex_payload_is_within_cap PASSED
tests/test_agents_md_byte_cap.py::test_tracked_stand_in_matches_the_live_global PASSED
tests/test_agents_md_byte_cap.py::test_root_doc_is_not_a_wholesale_claude_md_copy PASSED
tests/test_agents_md_byte_cap.py::test_planted_oversize_pair_is_refused PASSED
tests/test_agents_md_byte_cap.py::test_planted_pair_at_exactly_the_cap_passes PASSED
tests/test_agents_md_byte_cap.py::test_planted_single_oversize_doc_is_refused PASSED
tests/test_agents_md_byte_cap.py::test_missing_doc_is_refused_not_counted_as_zero PASSED
======================== 8 passed ========================
```

No SKIPs: the off-repo global doc is present on this machine, so both the hermetic and the
live halves actually ran. `uv run --locked ruff check tests/test_agents_md_byte_cap.py` — clean.

**THE HARD PART — what "the payload" is. Decision taken, and its cost.** The contract offered
three options; this lane took **(b)**, split across three tests so that neither half is silent:

| test | reads | runs where |
|---|---|---|
| `test_tracked_payload_is_within_cap` | root `AGENTS.md` + **tracked** `codex/AGENTS.md` | everywhere — hermetic, no off-repo dependency |
| `test_live_codex_payload_is_within_cap` | root `AGENTS.md` + **real** `~/.codex/AGENTS.md` | this machine; `skip` (never a vacuous pass) when absent |
| `test_tracked_stand_in_matches_the_live_global` | both global docs, byte-for-byte | guards the substitution itself |

The trade is written into the module docstring, verbatim per the contract's instruction: *"the
hermetic half can go stale relative to the operator's real `~/.codex` state, and the live half
does not run in CI. Neither is complete alone; the third test is what keeps the pair from
drifting apart quietly."*

**The contract's byte-identity claim was verified, not taken on trust — and it understates the
truth.** The contract asserted the tracked stand-in is "byte-identical **in length**". It is
byte-identical in **content**:

```
$ sha256sum codex/AGENTS.md ~/.codex/AGENTS.md
991837cb9ca3bd6f42c1aabf57248528a3b91fdd62c5e00dcf321b7642edbcab *codex/AGENTS.md
991837cb9ca3bd6f42c1aabf57248528a3b91fdd62c5e00dcf321b7642edbcab */c/Users/1028120/.codex/AGENTS.md
$ diff codex/AGENTS.md ~/.codex/AGENTS.md && echo IDENTICAL
IDENTICAL
```

That is why option (b) is honest today, and `test_tracked_stand_in_matches_the_live_global`
is what will say so the day it stops being true.

### Done-item 2 — "fails on a planted oversize fixture" · **MET**

**RED-first, witnessed.** The assertions were written before the helper existed and the module
was run in that state:

```
$ uv run --locked pytest tests/test_agents_md_byte_cap.py -n 0
E   ModuleNotFoundError: No module named 'agents_md_byte_cap'
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

**The planted fixture.** `_plant(tmp, root_size, global_size)` writes a synthetic doc pair of
exact byte sizes; **no real file is ever touched**, which is why `AGENTS.md` and `CLAUDE.md` are
byte-for-byte unmodified on this branch (`git diff main..HEAD --stat` lists one file). Four
failure cases, all proven to fire:

| case | expectation | result |
|---|---|---|
| cap+1 (split across both docs) | refused | `pytest.raises(AssertionError)` — PASSED |
| exactly cap | accepted | PASSED (boundary is inclusive; an off-by-one cannot slip) |
| one doc at cap+1, other empty | refused | PASSED (the cap is on the sum) |
| a doc missing entirely | refused | PASSED — **not counted as zero bytes** |

**Beyond the fixtures — the gate proved to fire on the REAL docs**, by lowering the cap to one
byte under the live payload rather than by inflating a file:

```
$ uv run --locked python -c "... assert_within_cap(ROOT_DOC, LIVE_GLOBAL_DOC, cap=9429)"
Codex instruction payload 9,430 B EXCEEDS the project_doc_max_bytes cap of 9,429 B by 1 B
(lane-f-577-byte-cap/AGENTS.md=5,539 B + .codex/AGENTS.md=3,891 B). Codex truncates SILENTLY past the cap.
```

`xdist` note the contract asked for: **not needed.** No stdlib module is monkeypatched through
an alias, so no worker dies. Every run above used `-n 0` for deterministic ordered output, but
the module has no parallel hazard — the one test whose failure would be load-bearing
(`test_planted_oversize_pair_is_refused`) uses `tempfile.TemporaryDirectory` rather than the
`tmp_path` fixture, deliberately, so it does not share a failure surface with the anchor-gate
probe test that has been RED on `main` since 2026-08-22.

### Done-item 3 — "[#577]'s done-when fully discharged" · **MET (5 of 5 clauses)**

Source: `tasks/577-adopt-agents-md-as-the-portable-instruction-layer.md`, the `· Done when:`
clause, split at its commas. **Verdict on the row as a whole: every clause MET.**

| # | clause | verdict | witness |
|---|---|---|---|
| 1 | a root `AGENTS.md` **≤120 lines** exists carrying the portable layer | **MET** | `wc -l AGENTS.md` → **107** (bound 120) |
| 2 | `CLAUDE.md` carries only the Claude-runtime remainder plus the permitted pointer | **MET** | `CLAUDE.md:42` portable-layer bullet; `CLAUDE.md:44` the thin `@AGENTS.md` importer |
| 3 | the combined global+root payload is asserted **in bytes** against the 32 KiB cap **by a test** | **MET — by this lane, and only by this lane** | done-item 1 above; this was the sole outstanding clause |
| 4 | the scope resolution for the `~/.codex` collision is stated in the `AGENTS.md` header | **MET** | `AGENTS.md:8` `## Precedence — resolved BY SCOPE, not by position`; the three-layer table at `AGENTS.md:19`, including the unpriced third layer `codex/AGENTS.md` |
| 5 | `CLAUDE.md` §10's retired-`AGENTS.md` anti-pattern is corrected **in the same commit** | **MET** | `CLAUDE.md:210` carries the live anti-pattern; `git show --stat 43c18e9f` lists `AGENTS.md` + `CLAUDE.md` + `templates/claude-regions/antipatterns-universal.md` in **one** commit, so the "same commit" qualifier holds literally |

The row's four binding **bounds** are correspondingly satisfied: (1) ≤120 lines — 107;
(2) the pointer relation — an importer, not a symlink; (3) precedence by scope in the header;
(4) **the guard stated in BYTES, not lines** — which is precisely what this lane built.

**Closure candidacy — REPORTED, NOT FILED.** With clause 3 discharged, `[#577]`'s done-when is
fully satisfied and the row is a **strong closure candidate**. It is still `status: open` on
`main`, as is `[#584]`. Whether either closes is `/review-closures`' call and the integrator's
to route — this lane files nothing (contract §3; lane D is the batch's exclusive `tasks/`
writer).

---

## 2. Commits on this branch, in order

| # | SHA | subject |
|---|---|---|
| 1 | `ab6cccd3` | `test(agents-md): [#577] assert the Codex instruction payload in BYTES against the 32 KiB cap` |
| 2 | `4ac3bb69` | `test(agents-md): [#577] terra findings — narrow an overclaiming docstring, add an emptiness floor` |

Diff against `main`: **one file, `tests/test_agents_md_byte_cap.py`, added.** No other path is
touched — no `AGENTS.md`, no `CLAUDE.md`, no `tasks/`, no generated surface. **No generated
surface was regenerated:** no pre-commit gate demanded one, so the contract's carve-out for that
case went unused and there is no third commit to name.

**Gate state.** Both commits passed the full pre-commit set with zero bypasses — no `--no-verify`,
no `SKIP=`. `audit-health`, `validate-hermetization` (the new `tests/` file is inside the
allowlisted home), `provider-registry-agreement`, `ruff`, `backlog-id-on-close` and
`backlog-filing-backpressure` all **Passed**.

---

## 3. Terra tally

Reviewer: `codex exec --model gpt-5.6-terra --full-auto`, scoped to `git show ab6cccd3` — the
lane's own diff. Not `/codex-review` (a mixed doc/code diff kills that lane).

```
TALLY: Critical=0 High=1 Medium=1 Low=0
```

| finding | verdict | disposition |
|---|---|---|
| **HIGH** — the stand-in divergence guard `skip`s exactly where hermetic enforcement is needed (CI), so the tracked stand-in could silently diverge | **PARTIALLY accepted** | The residue is the **disclosed option-(b) trade**, already stated in full in the module docstring — not a silent hole. Terra's proposed remedy (make absence a failure) would RED every CI run to report an off-repo file's absence, which is worse. **What was closable was closed:** a cap assertion only ever fails UPWARDS, so a truncated or blanked stand-in would have made the gate *greener*. An **emptiness floor** now refuses a hollow doc alongside the existing refusal of a missing one — proved to fire on a blanked doc. |
| **MEDIUM** — `test_root_doc_is_not_a_wholesale_claude_md_copy`'s docstring claimed an oversize measurement the test never performs | **ACCEPTED, fixed** | Docstring narrowed to the invariant actually asserted (byte-inequality only), and it now says outright that a near-copy would *not* be caught. The rejected alternative is recorded in place: pinning `CLAUDE.md` against the cap would RED on a legitimate `CLAUDE.md` edit while guarding nothing Codex reads. The remembered "11.50 KiB" constant is **gone** — the figure is measured at run time and reported in the failure message. |

Both fixes landed in `4ac3bb69`; 8/8 green and ruff clean afterwards.

---

## 4. Candidate filings for the integrator — REPORTED, NEVER FILED

**C-F1 · `CLAUDE.md` §2.68's `AGENTS.md` byte and line figures are FALSE.** This is the lane
contract's own D-F1, and this lane **confirms it independently** rather than repeating it:

| surface | measured by this lane | `CLAUDE.md` §2.68 claims |
|---|---|---|
| `~/.codex/AGENTS.md` | 3,891 B | 3,891 B (implied) |
| repo-root `AGENTS.md` | **5,539 B**, **107 lines** | "**103 lines**", "**5,270 B**" |
| combined payload | **9,430 B = 28.78 %** of 32,768 | "9,161 B = 28.0 %" |

Third, independent witness that this is **wrong-at-authoring and not drift**: the landing
commit's own diffstat says `AGENTS.md | 107 +++++`, and `git cat-file -s 43c18e9f:AGENTS.md`
== `5539`, and `43c18e9f` is its only content commit. The file has never been 103 lines or
5,270 B. Correcting §2.68 is a `CLAUDE.md` write — outside this lane's frozen write-scope, and
`CLAUDE.md` sits at **196/200** of its file budget, so the correction needs headroom it does not
have. **This is a fourth instance of the premise class lane G exists to refuse at freeze time.**

**C-F2 · `[#577]` is a strong closure candidate** — all five done-when clauses now MET (§1
above). `/review-closures`' call, not this lane's.

**C-F3 · the ex-ante statement will not match the measured figure.** The morning packet's
ex-ante line reads "byte-cap test green at **9,161 B** payload". The test is green at
**9,430 B**. **Delta: +269 B (+2.9 %).** The gate is correct and the ex-ante constant is the
thing that was wrong — this is C-F1 surfacing where the contract predicted it would.

---

## 5. Decisions taken under the V-2 budget

All four taken **per defaults / standing rulings, silently**. Nothing was escalated: no
curated-baseline, rule-vs-ruling, no-ruling-fork or out-of-scope-path question arose.

| # | decision | basis |
|---|---|---|
| D1 | Payload composition: contract option **(b)** — tracked stand-in as the hermetic gate, real off-repo file as the honest half, plus a third test guarding the substitution | The contract offered the fork explicitly and required only that the trade be **stated**; it is, in the docstring and in §1 above |
| D2 | The helper lives **inside** the test module, not in `scripts/` | Frozen write-scope is `tests/` — **one new file** |
| D3 | `[#577]` referenced in both commit subjects, never `closes` | Closure is `/review-closures`'; a `closes` on a sibling-branch ticket REDs `git_backlog_drift` |
| D4 | Failure-path strings kept **ASCII** (two em-dashes swept in `4ac3bb69`) | They render as `?` on this cp1252 console; a diagnostic that cannot print is a diagnostic that is not there |

---

## 6. Deviations, each with an owner

| # | deviation | owner | note |
|---|---|---|---|
| V1 | **No JOURNAL.md entry, and the session-end Stop hook is DECLINED explicitly** | integrator | Contract §1: a batch lane never journals — the integrator writes one anchor for the whole queue after every lane has STOPped. The hook is **advisory in full** (ADR-85 amendment 2026-08-03 §A5); the hard leg is `block-unanchored-push` at pre-push, and **this lane does not push**. Declined deliberately, not ignored and not "fixed". |
| V2 | **No merge, and none suggested** | integrator | Contract §2. Commit-and-STOP; the queue order is frozen. This packet ends at branch + SHAs + gate state + findings. |
| V3 | **Full suite NOT run** | integrator | Contract "TESTS": targeted only in a lane; the full suite runs **once, at integration** ([#528]; PLAYBOOK Ch5). Targeted set run here: `tests/test_agents_md_byte_cap.py` (8 passed) plus the two count-coupled neighbours `tests/test_gen_doc_counts.py` and `tests/test_validate_doc_claims.py` — **55 passed** total, so adding a test file did **not** trip the doc-counts or doc-claims surfaces and no regeneration is owed on that account. |
| V4 | **No inherited RED encountered** | — | Neither named pre-existing RED (the anchor-gate probe test; `test_stale_worktrees`) is in this lane's targeted set, so neither was run. Reported as *not observed*, **not** as *passing*. |

---

## 7. Ratchet — mechanical, both ends

| when | detector | files | count |
|---|---|---|---|
| dispatch-time baseline (from the contract) | silent-rule-v5 | 61 | **443** |
| before first commit | silent-rule-v5 | 61 | **443** |
| before last commit | silent-rule-v5 | 61 | **443** |

**Delta: ZERO.** This lane is not lane C and touched neither `protocols/` nor `templates/` —
`git diff main..HEAD --stat` is one file under `tests/`.

---

**STOP.** Branch `worktree-lane-f-577-byte-cap` at `4ac3bb69`, two commits, all gates green,
unmerged, awaiting the integrator's frozen queue.
