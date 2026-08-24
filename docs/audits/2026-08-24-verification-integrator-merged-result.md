# Integrator verification of the merged result — 2026-08-24 nine-branch batch

**Seat:** integrator, local, primary checkout · **Base:** `aeec0fd1` · **Merged head:** `4a476e89`
**Mode:** one full-suite run on the MERGED result, not per lane (contract Step 8).

---

## 1. `pytest` — full suite, unpiped, once on the merged result

Run once against merged `main`, redirected to a file rather than piped (a pipe reports the
pipe's exit code and hides the real one).

```
7 failed, 3819 passed, 4 skipped, 1 xfailed in 2048.54s (0:34:08)
```

Collected count moved **3573 → 3831** (+258) — L3's new `validate_adr_status` suite plus L1's
provider-registry schema suite. `ecosystem/doc-counts.md` regenerated to match; `validate_doc_claims`
confirms `pytest_collected` doc **3831** / actual **3831**.

### Every survivor RED, named and attributed

| # | Test | Verdict | Evidence |
|---|---|---|---|
| 1 | `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` | **PRE-EXISTING** | Re-run at bare `main` `aeec0fd1` — FAILS there too |
| 2 | `test_audit.py::test_health_ok_with_registered_repo` | **PRE-EXISTING** | Re-run at bare `main` — FAILS there too |
| 3 | `test_audit.py::test_health_stays_ok_with_na_status` | **PRE-EXISTING** | Re-run at bare `main` — FAILS there too |
| 4 | `test_reverse_dep_oracle.py::test_main_finding_json_exit_zero` | **MEASUREMENT ARTIFACT** | see §1.2 |
| 5 | `test_doc_code_edge.py::test_edge_check_registered_and_resolves_starter_set` | **MINE — FIXED** | `15 doc` → `16 doc`; `4a476e89` |
| 6 | `test_silent_rule_ratchet.py::test_target_state_on_live_repo_is_a_known_state` | **MINE — FIXED** | latent 5th state; `4a476e89` |
| 7 | `test_silent_rule_ratchet.py::test_check_registered_and_green_on_live_repo` | **MINE — FIXED** | migration also presents as `mixed`; `4a476e89` |

**Pre-existence proved, not asserted.** Rows 1–3 were re-run individually at bare `main`
`aeec0fd1` (`3 failed, 2 passed in 494.86s`). The contract's stated baseline was *"1 failed
(`test_anchor_gate_probe…`)"* — **that baseline was incomplete**: two `test_audit.py` health
tests fail at bare `main` as well and are not this batch's doing.

### 1.2 Row 4 is a measurement artifact, and the discriminator is recorded doctrine

`assert 3 >= 50` — the reverse-dep oracle drives pyright on a 40 s wall-clock timeout and returns
a **partial** corpus under CPU contention, which reads exactly like a code regression. Three
independent checks:

- **Its sibling passed.** `test_finding_headline_resolves_with_provenance` asserts the *same*
  `>= 50` floor via `run_oracle(timeout=40)` and passed in this run. When only the
  `main(--json)` variant fails, it is timing, not truth.
- **The arc cannot regress it.** Both oracle tests count reverse-dependents of a *Python* symbol.
  This batch's cloud/doc lanes touch zero `.py` files; L5's diff is markdown-only.
- **Re-measured quietly.** At L5's tip, where both oracle tests failed under load, they
  **both passed in 9.74 s** on a quiet re-run of the identical tree.

### 1.3 The three that were mine

All three are count/state pins my own Step 4–5 changes moved, fixed at their cause in `4a476e89`
and verified by targeted re-run (`100 passed`, `tests/test_silent_rule_ratchet.py` +
`tests/test_doc_code_edge.py`). The full suite was run **once**, per the contract; these three
are therefore reported as measured-then-fixed rather than re-measured by a second 34-minute run.

---

## 2. `audit.py ship-gate` — git-bash, unpiped

PowerShell false-REDs `handoff_probes`; run in git-bash as the contract requires.

```
ship-gate: RED — not shipped-ready (1 hard-fail organ(s); 25 new/undispositioned WARN(s))
```

### Against the Phase 0 baseline

| Metric | Phase 0 | Now | Δ |
|---|---|---|---|
| findings | 95 | **93** | −2 |
| WARN | 52 | **52** | 0 |
| dispositioned | 27 | **27** | 0 |
| undispositioned | 25 | **25** | 0 |
| `[stale]` | 3 | **3** | 0 |
| FAIL | 0 | **1** | **+1** |

Four of six metrics land **exactly** on the Phase 0 baseline after nine merges.

### The single FAIL is transient and only the operator can clear it

```
[!!] silent_rule_ratchet: integration refs (origin/main, main) carry baselines from
     DIFFERENT detectors — no common scale to compare against (live 443, committed 443)
```

**The numbers agree** — `live 443, committed 443`. What disagrees is the two integration refs:
`origin/main` still carries `silent-rule-v4 / 441`, `main` carries `silent-rule-v5 / 443`,
because **pushing `main` is the operator's act** and the contract reserves it.

**Precedented in the baseline file's own provenance**, for the previous raise: *"Until that arc
merges, the branch-side check reads raise-rejected vs origin/main (428) — expected, self-healing
at merge."* Every baseline change presents this way until the integration ref catches up. It
clears on the push.

---

## 3. The four validators, each in full

| Validator | Result |
|---|---|
| `validate_doc_claims` | **OK** — 4 claims, no prose drift. `precommit_hook_count` 21/21; `precommit_hook_roster` match (21 ids); `pytest_collected` **3831/3831**; `audit_check_count` skipped (ground truth unavailable) |
| `validate_backlog` | **OK** — 9 themes, 26 stories, **212 tasks**, 1 warning |
| `validate_git_backlog` | **OK** — no closed-but-present drift (direction (a) STRONG, full history) |
| `gen_task_tree --check` | **check ok** |

**The one `validate_backlog` warning, reported not fixed** (contract Step 7): *"user story with
no tasks — `[S24]`"* at `BACKLOG.md:459`. **Cause identified:** `[S24]` is marked **COMPLETED
2026-08-01**; its tasks correctly left the backlog per ADR-65 (done tasks leave `BACKLOG.md`). The
validator warns on a completed story that has properly shed its rows — the WARN is real, the
story is not defective.

---

## 4. Honest limits of this verification

- The full suite ran **once**, on the merged result, per the contract. The three REDs fixed in
  `4a476e89` were verified by **targeted** re-run, not by a second full pass.
- `audit_check_count` is **skipped** by `validate_doc_claims` (*ground truth unavailable*), so the
  44-check claim in `ecosystem/doc-counts.md` is asserted by regeneration and by
  `test_writer_integrity`/`test_audit`/`test_doc_code_edge` pins, **not** by that validator.
- The ship-gate verdict is **RED** and stays RED until the operator pushes. Nothing in this
  window can turn it GREEN, and no attempt was made to.
