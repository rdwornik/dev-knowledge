# OWNED-FILES manifest — lane N, `[#528]` legs 1+2 (lane-latency)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-15 · **Slug:** 528-legs12-manifest
- **Lane:** `lane-n-528-legs12-latency`, branch `worktree-lane-n-528-legs12-latency`
- **Contract of record:** `docs/audits/2026-08-15-technical-528-legs12-latency-lane-contract.md`
  (committed byte-identical at step 0, `ff2066ee`)
- **T_start:** 2026-08-15T14:33:31Z
- **Purpose of this file:** the contract's step 0b — the **derived** manifest, printed before any
  edit, so the footprint is a repo derivation rather than an authored guess.

---

## §1 How the list was derived

The contract states the candidate class rather than the list: *"the Python call sites that invoke
pytest for gate purposes + `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md`"*, and instructs
step 0 to derive the exact set from the repo. Derivation command, run over tracked files only:

```
git grep -n -E '("|'\'')pytest("|'\'')|pytest -[a-z]|-m pytest|pytest --' -- '*.py' ':!tests/*'
```

with a second, wider pass over non-`.py` surfaces (`.claude/**`, `.pre-commit-config.yaml`,
`plugins/**`, `deploy/**`, `templates/**`, `*.toml`, `*.yaml`, `*.yml`) so that anything outside
the candidate class is **enumerated and reported** rather than silently unseen.

Every hit was then read at its line to separate a real **invocation** from a mention in a comment,
docstring or printed instruction string. That distinction is the whole derivation: 17 of the 20
`.py` hits are prose about pytest, and exactly **three** spawn it.

---

## §2 IN the manifest — the files this lane may modify

| # | Path | Locator | Why it is in |
|---|---|---|---|
| 1 | `.claude/skills/verify/verify.py` | L24 `run("uv run --locked pytest -x --tb=short")` | the one Python call site that runs the suite for gate purposes — leg 1's subject |
| 2 | `protocols/PLAYBOOK.md` | Ch5 "Testing rules (scaled by repo complexity)", after "Per-step test cadence" (L815–825); Ch8 batch-protocol refuse-to-finish bullet "Full suite run once on the merged result" (L1793) | leg 2's doctrine home, named by the contract |
| 3 | `protocols/ESSENTIALS.md` | "Parallel sessions" section (L78–86) | leg 2's pointer home, named by the contract; ESSENTIALS points, never copies |

**Regen-at-merge surfaces excluded from the footprint count, per the contract's file discipline:**
`docs/audits/README.md` (audit-index regen, mandated by the `audit-index-freshness` hook for any
new audit file). No BACKLOG or `tasks/` edit is planned by this lane — leg 3 is not this lane's,
so `[#528]` does not close here.

---

## §3 Python call sites carrying a RECORDED REASON they do not take the flags

`[#528]`'s Done-when leg (1) reads *"gate-run call sites use `-n auto --dist worksteal` (or a
recorded reason one does not)"*. These are the recorded reasons. Both sites are left byte-unchanged.

| Path | Locator | Command as it stands | Recorded reason |
|---|---|---|---|
| `scripts/validate_doc_claims.py` | L137 | `[sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"]` | **collection, not a test run.** `--dist <policy>` governs how *tests* are handed to workers, and this invocation runs none; `--max-worker-restart=0` guards a crash during a run that does not happen here. The site already carries `-p no:cacheprovider`, which is the ladder item that does apply to it. It inherits `-n auto` from `addopts` and is left inheriting it — narrowing collection to `-n 0` is a behaviour change this contract does not authorize. |
| `scripts/worktree_import_proof.py` | L416–422 | `*interpreter, "-m", "pytest", <one generated test>, "-q", "-p", "no:cacheprovider", "-o", "addopts=", "--rootdir", ...` | **the site already refuses xdist on purpose, in-source.** `-o addopts=` drops the repo's own `addopts` (the comment names `-n auto` explicitly) and `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` (L391) unloads the xdist plugin entirely; a `-n` flag added here would land in the exact `unrecognized arguments: -n` exit-4 shape the `pyproject.toml` mutmut comment (L83–91) documents. The workload is one generated test, so a worker pool costs spawn time and buys nothing. |

Two further `.py` files matched the grep and are **not** call sites: `scripts/audit.py` (four
docstring/comment mentions; it delegates the expensive claim-3 to `validate_doc_claims`) and
`scripts/worktree_seed.py` L130/L139 (printed instruction text inside the seed plan).

---

## §4 OUT of the candidate class — enumerated, untouched, owed at integration

Every remaining pytest-invoking surface in the tree. None is a "Python call site", so none is in
this lane's footprint; each is listed so the integrator inherits a list rather than a gap.

| Path | Locator | Command | Disposition |
|---|---|---|---|
| `plugins/tier1-lifecycle/commands/ship.md` | L37 | `pytest -n auto --dist worksteal -x --tb=short && ruff check` (code-diff branch) | **already carries leg 1's flags**; lacks `--max-worker-restart=0`. Markdown command in the deployed plugin corpus — a change here propagates to every consumer, so it is **owed at integration**, not taken by a lane whose contract names Python call sites. `[#340]` already owns this command's pre-flight shape. |
| `plugins/tier1-lifecycle/commands/ship.md` | L32 | `pytest -m live_repo -q && ruff check` (docs-only branch) | marker-filtered fast path; inherits `-n auto`. Same out-of-class reasoning. Owed at integration. |
| `.claude/commands/lane-integrate.md` | L37, L59 | `uv run --locked pytest -q` | this **is** the tiered law's tier B (the one full suite on the merged result). Inherits `-n auto`. Markdown, out of class; owed at integration. |
| `.github/workflows/report-only-wall.yml` | L141 | `uv run --locked pytest -q --tb=line` | **not a gate** — the job is `continue-on-error: true` and the summary says "Report-only, permanently … no required check exists to arm". A non-gate is outside "gate-run call sites" by the row's own words. |
| `templates/child-methodology-floor.md.tmpl` | L16 | `pytest -x --tb=short && ruff check && git status` | carrier text shipped to consumers (hash-guarded floor); out of class, and a carrier edit is its own arc. |
| `templates/CLAUDE-md-template.md` | L52 | `<e.g. pytest -x --tb=short>` | placeholder inside a template, not an invocation. |
| `templates/claude-regions/session-start-protocol.md` | L6 | `pytest --collect-only` | byte-coupled hub region (`test_hub_region_bodies_still_byte_match_the_templates`); a discovery sanity check, not a gate run. |

**HARD EXCLUSION honoured, and the collision turned out to be empty.** The contract reserves
`.pre-commit-config.yaml` and every hook script to lane O (`lane-o-527-block-main`). Checked rather
than assumed: `grep -n pytest .pre-commit-config.yaml` returns **nothing**, and this repo has no
`.claude/hooks/` directory. So no gate-run pytest call site is stranded in lane O's property — the
exclusion costs this lane no coverage, and there is nothing for the integrator to reconcile there.

---

## §5 The measured basis leg 2 cites

| Figure | Value | Source |
|---|---|---|
| host full suite | **918.90 s** | `JOURNAL.md` 2026-08-15 (a), the boot-acts arc's own run |
| cloud serial | **701.60 s** | night-2 lane-latency audit §1, commit `8387ff2a` (unmerged, branch `claude/night2-latency-audit-6s1k6p`) |
| cloud `-n auto` (4 workers) | **473.02 s** — ratio **1.48×**, failure sets identical | same, §2 |
| parallel floor | one 268.74 s test = 38.4 % of the suite | same, §1b/§2b |
| tier-A derivation | 2797 tests (96.5 %) cost 154.64 s (22.1 %); `-n 4` lower bound 38.7 s | same, §3 — **derived arithmetic, explicitly not measured** |
| xdist settings ladder | `--max-worker-restart=0`; `--maxprocesses=N`; `-n 0` under forking parents; `-p no:xdist` is not serial; `--dist loadfile`/`loadgroup` for shared-tree tiers; `-p no:cacheprovider` in hooks; stray-worker detection | night-2 research audit §2.6/§2.3, commit `757077f2` (unmerged, branch `claude/night2-research-d30vhu`) |

Both source audits are **unmerged drafts**; they are cited by commit SHA rather than by tracked
path, and the doctrine text says so, so a reader can reach the evidence without the citation
implying a file that `git ls-tree main` does not carry.

---

## §6 Constraints this lane is holding

- `silent_rule_ratchet` measured **440 ≤ baseline 441** before any edit (`audit.py health`), i.e.
  one token of headroom. Both leg-2 targets sit in the detector's scope (`protocols/*.md`,
  non-recursive), so the doctrine is phrased declaratively and adds no `must|shall|never` token.
- `protocols/ESSENTIALS.md` is in `DEFAULT_FRESHNESS_FILES`
  (`scripts/canonical_freshness_gate.py:32`), so editing it moves `last_reviewed` — which is
  discharged by a genuine end-to-end re-read, done this session before the edit.
- `protocols/PLAYBOOK.md` is deliberately **out** of the freshness gate (`scripts/audit.py:287`,
  `tests/test_audit.py:1025`), so no stamp moves there. Its TOC covers `##`/`###` only, so the
  new `####` subsection leaves `toc-freshness-playbook` unmoved.
- No `--no-verify`, no `SKIP=`, no merge, no push to main, no new `[#id]`, no new repo path.
