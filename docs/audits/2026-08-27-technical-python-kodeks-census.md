# CLOUD-NIGHT-C2 — Python-standards kodeks: the hub measured against its own North Star

**Substrate.** `.dev-knowledge` @ `d8211b0` (detached HEAD on origin/main), read-only, zero writes to the tree.
**Instrument.** `ruff 0.15.8` (system binary; satisfies the repo's own `required-version = ">=0.15.5"` floor). **`uv run --locked` was unavailable** — the container ships uv 0.8.17, `pyproject.toml:25` pins `==0.11.19`, so uv refused. Every count below is standalone-ruff or AST/grep over the tracked tree. Nothing is inferred.

**Denominator correction.** The brief says 287 `.py`. Live: **289 git-tracked** — **135 non-test**, **154 under `tests/`** (29 of those `tests/fixtures/`). The standard is about production code, so the non-test denominator is **135**, not 287, and most tables below use it.

**Where the standard actually lives.** `protocols/PLAYBOOK.md:3551-3557`, inside a *"CLAUDE.md template (minimum viable)"* copy-paste block — advice the hub hands a **new consumer project** to paste into its own CLAUDE.md. It is not in `CONTRIBUTING.md`, not in `ENVIRONMENT.md`, not in the hub's own `CLAUDE.md`, and not in any parity surface. **The hub authored the standard for others and never adopted it.** That is the single structural fact this report rests on.

---

## 1. Enforcement inventory

**What is on, per `file:line`:**

- `pyproject.toml:170-177` `[tool.ruff]` — `required-version = ">=0.15.5"`, `target-version = "py311"`, `line-length = 120`
- `pyproject.toml:181-182` `[tool.ruff.lint]` → **`extend-select = []`** ← the whole finding in one line. Ruff's **default rule set only**: `E4`, `E7`, `E9`, `F`. No style, no bugbear, no print ban, no annotations, no complexity.
- `pyproject.toml:184-185` per-file-ignores, `tests/fixtures/**` → `F401,F811,E402`
- `.pre-commit-config.yaml:298-308` — `astral-sh/ruff-pre-commit` @ `v0.15.5`, `args: []` (gate mode, no `--fix`); rev == the pyproject floor
- `pyproject.toml:115-117` `[tool.pytest.ini_options] minversion = "9.0"`
- `ecosystem/parity-surfaces.yaml:661-691` — four **MUST-uniform, non-waivable** fleet surfaces: `ruff-target-version`, `ruff-line-length`, `ruff-required-version`, `pytest-minversion`
- `templates/ruff-config-block.toml:34-40` — the fleet carrier, which **explicitly declares `select`/`ignore`/`per-file-ignores` REPO-PERSONAL** and lists the hub's posture verbatim as `extend-select = []`

**Baseline: `ruff check .` returns 0 violations tree-wide.** The gate is green because it asks almost nothing.

**Grep for `select` in `ecosystem/parity-surfaces.yaml`: zero hits.** The fleet gates ruff's *version, target and line width* — never its *rule set*. Nine of the eleven standard items have no enforcement anywhere in the repo.

### The gap table

```
STANDARD ITEM (PLAYBOOK:3552-3557)  ENFORCED BY                      VIOLATIONS (non-test/135)   SMALLEST MECHANISM
Python 3.11+                         pyproject.toml:176 target-version   0                        (already on)
  ...type hints                      NOTHING                            302  ANN                  select ANN001,ANN201
                                                                        (ANN001 156, ANN201 55,
                                                                         ANN401 46, ANN202 40)
pyproject.toml for deps              parity-surfaces.yaml:257 (MUST)      0                        (already on)
                                     + ADR-106 uv.lock
ruff for linting                     .pre-commit-config.yaml:298-308      0 — BY CONSTRUCTION      widen extend-select
                                     (rule set = ruff DEFAULT)                                     (pyproject.toml:182)
pytest                               pyproject.toml:117 minversion,       1 unittest importer      select PT
                                     parity-surfaces MUST-uniform         (tests/test_fleet_health.py)
                                                                          PT: 349 tree / 1 non-test
Click for CLI                        NOTHING                            65 of 78 CLI files        NO RUFF RULE EXISTS
                                                                        (click 13 / argparse 31   -> needs a check, or
                                                                         / neither 34)             amend the standard
Rich for output                      NOTHING                            134 of 135 files          NO RUFF RULE EXISTS
                                                                        (rich imported ONLY in
                                                                         deploy/tool.py:48-50)
Logging not print                    NOTHING                            344  T201                 select T201
                                                                        (logging imported 11/135;
                                                                         getLogger x12)
                                                                        LOG=0, G=0 -> free but
                                                                        VACUOUS (nothing logs)
Dataclasses not dicts                NOTHING                            141 dict-returning fns    NO RUFF RULE EXISTS
                                                                        vs 115 @dataclass in
                                                                        48/135 files
Config in YAML not hardcoded         PARTIAL — 11 ecosystem/*.yaml       61  PLR2004              select PLR2004
                                     registries + provider-registry-      1 hardcoded abs path
                                     agreement hook (.pre-commit:~230)
Pure fns / explicit data flow        NOTHING                             92  FBT (boolean trap)   select FBT,PLW0603,
                                                                         38  PLR0913               B006,PLR0913
                                                                          9  PLW0603 (global)
Single-responsibility modules        NOTHING                             71  C901 (>10)           select C901,PLR0912,
                                                                         42  PLR0912                     PLR0915
                                                                         27  PLR0911
                                                                         18  PLR0915
```

**Library-first phase-in, measured tree-wide.** Rules that cost **zero today** — switching them on is a free ratchet: `T203`, `LOG`, `G`, `ICN`, `INT`, `SLOT`, `TID`, `NPY`, `W`, `YTT`, `ASYNC`, `FA`. **Honest caveat: `LOG`/`G` read 0 only because logging is barely used at all** (11 of 135 files) — turning them on is free and nearly meaningless until `T201` forces logging to exist.
Near-free (≤20 tree-wide): `ISC` 1, `A` 1, `PIE` 2, `RET` 6, `B` 15, `FLY` 16, `C4` 17.
Costed, ascending: `SIM` 37, `DTZ` 49, `BLE` 51, `Q` 61, `PERF` 68, `EXE` 70, `PTH` 72, `C901` 72, `N` 110, `I` 113, `FBT` 155, `UP` 183, `COM` 260, `RUF` 337, `T20` 349, `ARG` 353, `EM` 388, `TRY` 397, `PL` 901, `D` 5190, `ANN` 6910.

**One qualifier the raw `T201` count hides.** Of 344 non-test prints, **336 sit in files carrying a `__main__` guard** — terminal output, not diagnostic logging. Only **8** are in importable-library-only modules (`.claude/skills/verify/verify.py` ×5; `scripts/codemap/{generator,check,ast_walker}.py` ×1 each). Against the standard as written the 344 are all violations; against intent, the real reading is *"Rich, not bare print, for CLI output"* — which makes the Rich gap (1 of 135) and the print gap the **same** gap, not two.

---

## 2. Worst-offender map

Ranked by composite ruff count over `T20,PL,C90,ANN,B,ARG,PTH,FBT,PERF,BLE,DTZ,SIM,RET,C4` (non-test only). Measurement, no proposals.

1. **`scripts/audit.py` — 122.** 4671 LOC, 106 functions, 2 classes, **1 dataclass**. 7×C901: `:828 _git_linked_worktrees` (15>10), `:1435 _select_active_bundle` (15>10), `:1537 check_handoff_probes` (13>10), `:2316 _ratchet_findings` (11>10), `:3158 check_preflight_backlog_ids` (12>10). `PLR2004` ×9 — the most magic values in the repo. The single largest module and the god-module exemplar.
2. **`scripts/fleet_parity.py` — 70.** 2053 LOC, 50 fns, 6×C901, 6 dict-returning fns.
3. **`scripts/nopack_sandbox.py` — 49.** 2501 LOC, 70 fns, **8×C901 — the highest complexity density in the repo**, 8 dict-returners, 11 prints.
4. **`scripts/fleet_health.py` — 46.** 1017 LOC, 35 fns, **0 classes / 0 dataclasses**, 4 dict-returning fns, 14 prints. Pure dict-plumbing at 1k lines.
5. **`scripts/gen_task_tree.py` — 43.** 1367 LOC, 44 fns, **31 prints — the most in the repo**, 2×C901.
6. **`scripts/enforcement_coverage.py` — 41.** 1180 LOC, 54 fns, 8 dict-returners (6 dataclasses present — mixed).
7. **`scripts/validate_backlog.py` — 39.** 2×C901.
8. **`scripts/gen_dashboard.py` — 39.** 1368 LOC, **65 fns**, 9 prints.
9. **`scripts/single_flight.py` — 33.** 836 LOC, **17 prints, 0 dataclasses**.
10. **`plugins/tier1-lifecycle/scripts/propose_closures.py` — 32** and **`scripts/propose_closures.py` — 31**. Near-duplicate modules (550 vs 532 LOC) that `diff` reports as **differing** — two copies of one responsibility, drifted.

**Outside the top 10 but the sharpest single reading:** `deploy/carrier_precommit.py` — 5×C901 including `:521 _apply_one_op` (**22>10**) and `:304 _reconcile` (**21>10**), the two most complex functions in the tree.

**Dict-plumbing exemplar, and it is documented rather than accidental:** `scripts/provider_registry.py:50` — `load_registry(...) -> dict[str, Any]`. It validates through the pydantic model `ecosystem/schema/provider_registry.ProviderRegistry` and then **returns the raw mapping**; 9 of its 11 functions return dicts. The docstring at `:65-68` states the choice verbatim: *"Returns the RAW mapping, not the validated model. Deliberate… re-pointing them at attribute access would be a rewrite whose only gain is style."* This is `dataclasses not dicts` failing **after a typed model already exists** — the cheapest possible place to have honoured it. Only two non-test files pair ≥5 dict-returning functions with **zero** dataclasses: this one (9) and `deploy/carrier_floor.py` (6, 946 LOC, 42 fns, 1 class).

---

## 3. Kodeks shape — where the standard should live

**Option A — `pyproject.toml` `[tool.ruff.lint]` as the sole carrier.** Replace `extend-select = []` at `pyproject.toml:182` with an explicit rule list, and add a fifth parity surface pinning it MUST-uniform beside `ruff-target-version`. **Trade-off:** it is the only option where the standard *executes* — a consumer inherits enforcement by having the file, and `fleet_parity` already knows how to read `pyproject.toml` (`fleet_parity.py:754-772`). It also caps what can be said: ruff has **no rule** for Click-vs-argparse, Rich-vs-print, or dataclass-vs-dict — three of the standard's seven substantive items are simply unrepresentable. And `templates/ruff-config-block.toml:34-40` currently declares `select` **REPO-PERSONAL by name**, so this option requires reversing a recorded ARC-4 ruling, not just editing a table.

**Option B — a hub doc as the carrier.** Promote `PLAYBOOK.md:3551-3557` into a real canonical section (or a `protocols/PYTHON_STANDARD.md`) with `last_reviewed`, rationale, and the measurements above. **Trade-off:** it can express all eleven items, including the three ruff cannot reach, and it can record *why* (e.g. the `provider_registry.py:65` deviation belongs in prose, not a lint suppression). But it enforces nothing, and this repo has a named failure mode for exactly that — the standard has sat in PLAYBOOK for months while the hub's own 135 modules diverged from every unmeasurable clause. A doc-only kodeks reproduces the state this report is documenting.

**Option C — both, split on enforceability.** The ruff table carries every item ruff *can* decide (`ANN`, `T201`, `PT`, `C901`, `PLR09xx`, `FBT`, `PLR2004`), pinned as a parity surface; the doc carries the three it cannot (Click, Rich, dataclasses-over-dicts) plus the rationale and the recorded deviations, and names the ruff table as its executable half. **Trade-off:** two surfaces to keep in agreement — which is precisely the drift class this repo already builds regen-and-diff gates for, and the `provider-registry-agreement` hook (`.pre-commit-config.yaml`, `scripts/check_provider_registry.py`) is a working precedent for holding a doc and a config in agreement against a YAML source of truth. It is the most work and the only shape where nothing has to be dropped or left inert. **This is the recommendation.**

---

## 4. Universalization note

**Transfers to a consumer with zero hub code.** Everything in `[tool.ruff.lint]`. A consumer that has `pyproject.toml` + the pinned `astral-sh/ruff-pre-commit` hook gets full enforcement with no hub script present — ruff is the runtime, and the fleet already ships the hook rev (`.pre-commit-config.yaml:298-308`, fleet-canonical, matching corp-monorepo and ai-council). The four existing MUST-uniform parity surfaces prove the channel works: a fifth surface pinning the rule set costs nothing new to distribute. Same for `pytest minversion`. **This is the whole of the standard's mechanically-enforceable half, and it needs no carrier.**

**Needs a carrier.** The three unrepresentable items — Click-for-CLI, Rich-for-output, dataclasses-over-dicts — have no ruff rule and would require a hub script, i.e. a new organ shipped through `deploy/carrier_precommit.py`'s `hub_hooks` list (`deploy/manifest-v1.4.0.yaml:96-110`). Note what `scripts/enforcement_coverage.py:1-30` already establishes about that path: presence is not enforcement, and hub-hardcoded standalone checkers land as `absent` on consumers. A new checker for these three would enter as Group C — the genuinely-unclosable-without-porting class. **Recommendation: do not build it.** Carry these three as doc-level intent (Option B's half of C), and let the measured numbers — 13/78 Click, 1/135 Rich — be the argument for or against amending the standard rather than enforcing it.

**Also needs a carrier, and is cheaper than it looks:** the `tests/fixtures/**` per-file-ignores idiom (`pyproject.toml:184-185`). Any consumer switching on `ANN` or `T201` will need an equivalent test-scoped ignore block, or the rule lands as thousands of violations in test code (`ANN` is 302 non-test vs **6910** tree-wide — 96% of it is tests). That block belongs in `templates/ruff-config-block.toml` beside the values it already carries.

---

## Proposed rows — CANDIDATE only, not filed

Per ADR-111 these are CANDIDATEs requiring an ADR-98 intake before any row exists. Nothing here has been written to `tasks/` or `BACKLOG.md`.

1. **Free-ratchet the zero-cost ruff families** · *Done when:* `pyproject.toml:182` selects the twelve families measuring 0 tree-wide (`T203, LOG, G, ICN, INT, SLOT, TID, NPY, W, YTT, ASYNC, FA`) plus the ≤20 tier (`ISC, A, PIE, RET, B, FLY, C4` — 58 fixes total), `ruff check .` exits 0, pre-commit green. *Size:* **S**
2. **Rule the standard's three unrepresentable items** · *Done when:* an operator/architect ruling records, per item (Click-for-CLI at 13/78, Rich-for-output at 1/135, dataclasses-over-dicts at 141 dict-returners), one of {enforce via new organ · amend the standard · accept as aspiration}, and `PLAYBOOK.md:3551-3557` is edited to match the ruling. *Size:* **S** (decision, not build)
3. **Make the ruff rule set a parity surface** · *Done when:* `ecosystem/parity-surfaces.yaml` carries a fifth MUST-uniform ruff surface covering `[tool.ruff.lint]`, `templates/ruff-config-block.toml:34-40`'s REPO-PERSONAL declaration for `select` is superseded on the record, and `fleet_parity` reports it across all three repos. *Size:* **M** (depends on 1 and 2)
4. **Costed phase-in of the four enforceable standard clauses** · *Done when:* `T201` (344), `ANN001/ANN201` (211 non-test), `C901+PLR0912/0915` (131), `PLR2004` (61) are each either selected-and-clean or carry a dated, reasoned `per-file-ignores` entry naming the module — with `scripts/audit.py`, `scripts/nopack_sandbox.py` and `deploy/carrier_precommit.py` explicitly dispositioned. *Size:* **L**