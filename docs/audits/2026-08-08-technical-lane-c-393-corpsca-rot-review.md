# [#393] corp-sca rot review — three verdicts, one prepared patch, zero consumer writes

**Lane:** LANE-C (batch 3) · **Mode:** REPORT-ONLY · **Date:** 2026-08-08
**Target repo:** `corp-sca-time-automation` (read-only; not mutated by this lane)
**Discharges:** part of `[#384]`'s done-when — "rot findings become tickets/verdicts"
**Execution precondition:** apply the prepared patch when corp-sca is organ-provisioned; see the batch-3 packet. Nothing in this document has been applied.

---

## 0. Verdicts at a glance

| # | File | Verdict | Execution remainder |
|---|---|---|---|
| 1 | `config/category_mapping.yaml` | **confirmed-live** | none |
| 2 | `config/excluded.yaml` | **confirmed-live** | none |
| 3 | `requirements.txt` | **prune-entries** (1 entry: `azure-identity>=1.15`) | §4.3 patch, dry-run verified |

`[#393]`'s done-when is **discharged as a review**: each of the three is now confirmed-live or dispositioned. The row is **not** closable with zero mutations — verdict 3 leaves one named execution remainder (a single-line prune). See §7.

**Read state (all evidence below is against this state):**
- corp-sca HEAD `3661b3a` on `feature/tenrox-loader`; `main` = `origin/main` = `c16fc24`.
- The three target blobs are **byte-identical across `main`, `origin/main`, `feature/tenrox-loader`, `origin/feature/tenrox-loader`** — no branch-dependent verdict.

---

## 1. Live ages, re-derived (the row's figures are input, not truth)

The `[#393]` row carries figures from the first `fleet_analytics` run (2026-07-22). All three are re-derived here from live git.

| File | Row figure (@ run 2026-07-22) | **Live last touch** | **Live age @ 2026-08-08** |
|---|---|---|---|
| `config/category_mapping.yaml` | 204d | `8dac83b` 2025-12-30 | **221d** |
| `config/excluded.yaml` | 203d | `8dac83b` 2025-12-30 | **221d** |
| `requirements.txt` | 199d | `c013b11` 2026-03-21 | **140d** |

Commands (each run per-ref; all four refs agreed, with and without `--follow`):

```
git -C <corp-sca> log -1 --format="%h %ad %s" --date=short <ref> -- <path>
```

### 1.1 The 199d refutation — recorded, and then explained

**As a last-touch figure the row's 199d is REFUTED.** `requirements.txt` was last touched by `c013b11` (2026-03-21), which is **140d** at 2026-08-08 and 123d at the run date — not 199d. The contract carries this refutation with the figure 139d; the exclusive day-count from 2026-03-21 to 2026-08-08 is **140**, and 140 is the figure used throughout this report.

**But the row's 199 is not a defect — it is a faithful output of a different measure, and all three row figures reproduce exactly.** The rot frame does not rank on last touch. `scripts/fleet_analytics.py:last_meaningful_ts` ranks on the most recent **meaningful** edit: a non-merge commit that changed at least `min_meaningful_churn` (**default 3**, `fleet_analytics.py:194`) lines *of that file*, in a commit touching at most `max_commit_files` (30) files. Age is then `(now_ts - ts) // 86400` on **committer** timestamps (`fleet_analytics.py:683`).

Per-commit churn against that floor (`git show --numstat`):

| Commit | Date (committer) | `category_mapping.yaml` | `excluded.yaml` | `requirements.txt` |
|---|---|---|---|---|
| `e28afee` | 2025-12-29 19:19:34 +0100 | 21/0 → **21 ✓** | 6/0 → **6 ✓** | 6/0 → **6 ✓** |
| `8dac83b` | 2025-12-30 10:39:33 +0100 | 1/1 → 2 ✗ *below floor* | 2/2 → **4 ✓** | — |
| `be4109b` | 2026-01-03 16:25:42 +0100 | — | — | 15/4 → **19 ✓** |
| `c013b11` | 2026-03-21 20:59:08 +0100 | — | — | 1/0 → 1 ✗ *below floor* |

So the frame's `last_meaningful_ts` resolves to `e28afee`, `8dac83b`, and `be4109b` respectively — and the floor-div age at a run before 09:39 UTC on 2026-07-22 is:

| File | frame's meaningful commit | computed age | row figure |
|---|---|---|---|
| `config/category_mapping.yaml` | `e28afee` | **204** | 204 ✓ |
| `config/excluded.yaml` | `8dac83b` | **203** | 203 ✓ |
| `requirements.txt` | `be4109b` | **199** | 199 ✓ |

All three reproduce to the day. Two consequences worth carrying:

- The contract's phrasing that "the other two figures reproduce (last-touch 2025-12-30)" is numerically right but mechanically imprecise: `category_mapping.yaml`'s 204 comes from `e28afee` (2025-12-29), **not** from its last touch `8dac83b` — its last touch was a 2-line edit that fell below the floor. The two files share a last-touch commit yet legitimately carry different row ages.
- **The gap is semantic, not a bug.** "199d" answers "how long since a substantial edit", the row reads as "how long since any edit". For `requirements.txt` the two diverge by 59 days because its most recent edit was a one-line dependency add.

### 1.2 An unenumerated honest-limit in the rot frame (hub-side observation, `[#384]`)

`fleet_analytics.py`'s HONEST LIMITS block (lines 57–84) enumerates limit #9: a file with **no** meaningful-edit record is invisible to the frame, and that count is surfaced as `files_no_edit_record`. The case found here is the adjacent one and is **not** enumerated: a file **with** a record whose *most recent* edits fall below the churn floor reports an age **older than its true last touch**, silently and with no surfaced counter. Two of three candidates in this single sample hit it.

This is an observation about the hub's frame, not about corp-sca, and it is **not** filed — no BACKLOG row was added by this lane. Filing it against `[#384]` is the operator's call.

### 1.3 Calibration — the three candidates against their neighbours

| Path | Last touch | Age @ 2026-08-08 |
|---|---|---|
| `src/excel_preview.py`, `src/gap_filler.py`, `src/tenrox.py`, `src/aggregator.py`, `config/tenrox_mapping.yaml` | 2026-07-05 | 34d |
| `.pre-commit-config.yaml` | 2026-06-08 | 61d |
| `pytest.ini` | 2026-05-28 | 72d |
| `src/config.py`, `config/settings.yaml` | 2026-04-02 | 128d |
| `src/excel_writer.py`, `src/sharepoint.py`, `src/gemini_client.py` | 2026-03-29 | 132d |
| **`requirements.txt`** | **2026-03-21** | **140d** |
| `src/overlap.py`, `src/models.py`, `src/text_utils.py`, `src/loader.py`, `src/mapper.py` | 2026-03-15 | 146d |
| **`config/excluded.yaml`**, **`config/category_mapping.yaml`** | **2025-12-30** | **221d** |

`requirements.txt` at 140d sits mid-pack — **younger** than five `src/` modules nobody has flagged. The two YAMLs are the oldest tracked files in the repo bar `src/__init__.py`. Age alone separates nothing here; every verdict below is made from usage.

---

## 2. Verdict 1 — `config/category_mapping.yaml`: **confirmed-live**

21 lines, two top-level keys: `mapping` (11 Outlook-category → SharePoint-category pairs) and `sales_categories` (5 names).

### Usage evidence

| Site | Line | Evidence | Kind |
|---|---|---|---|
| `src/config.py` | 55–57 | `def get_category_mapping() -> dict:` → `return load_yaml("category_mapping.yaml")` | loader |
| `src/mapper.py` | 8 | `from src.config import get_category_mapping` | import |
| `src/mapper.py` | 14 | `mapping = get_category_mapping()["mapping"]` inside `map_category()` | **production read** |
| `src/excel_preview.py` | 91 | `resolve_overlaps_by_hour(events, lambda e: map_category(e["category"]))` | production caller |
| `src/excel_preview.py` | 99 | `sp_category = map_category(event["category"])` | production caller |
| `tests/test_overlap_fix.py` | 40, 47 | `map_category(...)` | test caller |

### Reachability from a CLI entry point (verified link by link)

```
scripts/run.py:135  cmd_preview      ─┐
scripts/run.py:428  cmd_catchup      ─┴→ generate_final_preview   (src/excel_preview.py:182)
                                        → generate_aggregated_preview (:202 → def :142)
                                        → generate_preview            (:162 → def :56)
                                        → map_category                (:91, :99)
                                        → get_category_mapping        (src/mapper.py:14)
                                        → load_yaml("category_mapping.yaml") (src/config.py:57 → :30)
```

Every hop confirmed by direct read of the blob on `feature/tenrox-loader`. Both CLI commands reach the file; there is no branch on which the read is skipped.

**Verdict: confirmed-live.** Deleting it raises `FileNotFoundError` in `load_yaml` on every `preview` and `catchup` run — the repo's two primary commands. No patch prepared; no remainder.

### Sub-file observation (not a verdict, no patch)

The `sales_categories` key (lines 15–21) has **no live consumer**. Whole-repo grep for `sales_categories` on `feature/tenrox-loader` returns three hits: the YAML definition itself, and two lines of `docs/archive/2026-03-15_CODE_REVIEW_REPORT.md` (`:39`, `:41`) recording that `src/excel_preview.py:78` once held an unused `sales_categories` variable and that the review removed it. Only `["mapping"]` is read at `src/mapper.py:14`.

Flagged, deliberately **not** patched: the key encodes a business rule ("categories requiring Opportunity ID") that may be intentional documentation, and it is outside `[#393]`'s three-file scope. Dispositioning it is the operator's call.

---

## 3. Verdict 2 — `config/excluded.yaml`: **confirmed-live**

6 lines, two keys: `categories: ["PERSONAL"]` and `title_keywords: []`.

### Usage evidence

| Site | Line | Evidence | Kind |
|---|---|---|---|
| `src/config.py` | 60–62 | `def get_excluded() -> dict:` → `return load_yaml("excluded.yaml")` | loader |
| `src/loader.py` | 9 | `from src.config import get_settings, get_excluded` | import |
| `src/loader.py` | 39–41 | `excluded = get_excluded()` → `{c.upper() for c in excluded["categories"]}` → filter | **production read** |
| `src/loader.py` | 67 | `events = filter_excluded(events)` inside `load_and_filter()` | production caller |
| `src/excel_preview.py` | 82 | `events = load_and_filter(weeks_back=weeks_back)` | production caller |
| `src/gap_filler.py` | 375, 377 | `from src.loader import load_and_filter` → `events = load_and_filter()` | production caller |

### Reachability from a CLI entry point

```
scripts/run.py:135 / :428 → generate_final_preview (src/excel_preview.py:182)
   ├─ :202 → generate_aggregated_preview → generate_preview → load_and_filter (:82)
   └─ :207 → fill_gaps_with_new_entries (src/gap_filler.py:363) → load_and_filter (:377)
                                        → filter_excluded (src/loader.py:67 → def :37)
                                        → get_excluded     (src/loader.py:39)
                                        → load_yaml("excluded.yaml") (src/config.py:62 → :30)
```

**Two independent production paths** reach the file — the preview path and the gap-fill path. Both CLI commands traverse at least one.

**Verdict: confirmed-live.** Deleting it raises `FileNotFoundError` in `filter_excluded` on every `preview` and `catchup` run. Beyond the crash, it is the only mechanism excluding `PERSONAL` calendar events from a SharePoint upload — a data-correctness surface, not just a config read. No patch prepared; no remainder.

### Sub-file observation (not a verdict, no patch)

`filter_excluded` reads **only** `excluded["categories"]` (`src/loader.py:40`). The `title_keywords: []` key has no reader. The whole-repo grep for `title_keywords` returns the YAML line plus `src/mapper.py:18` and `:96` — but those are the function `extract_client_from_title_keywords(title, company_names)`, which takes company names from `project_codes.xlsx` and never touches this file. **Name collision, not a consumer** — worth stating explicitly, because a grep-only sweep reads it as a live reference.

The key is an empty list with a `# optional` comment: declared-but-unimplemented, not rot. Not patched.

---

## 4. Verdict 3 — `requirements.txt`: **prune-entries** (one entry)

Per the contract: this file cannot be retired wholesale — the repo runs on it. The honest verdicts are `confirmed-live` or `prune-entries`. The evidence supports **prune-entries**, with exactly one entry to remove.

### 4.1 Declared → used (two-way fact table)

| Line | Entry | Import name | Import sites | Status |
|---|---|---|---|---|
| 2 | `pandas>=2.0.0` | `pandas` | 18 sites — `src/aggregator.py:5`, `src/excel_writer.py:5`, `src/gap_filler.py:5`, `src/project_codes.py:5`, `src/excel_preview.py:5`, `src/tenrox.py:31`, `src/sharepoint.py:278`, `scripts/run.py:36`, `scripts/manager_report.py:5`, + 9 tests | **USED** |
| 3 | `python-dotenv>=1.0.0` | `dotenv` | `src/config.py:8`, `src/sharepoint.py:11`, `tests/conftest.py:5` | **USED** |
| 4 | `pyyaml>=6.0` | `yaml` | `src/config.py:9`, `scripts/generate_clients_yaml.py:20` | **USED** |
| 7 | `openpyxl>=3.1.0` | `openpyxl` | `src/excel_writer.py:7,8,9,10`, `scripts/manager_report.py:8,9,10`, `tests/test_excel_writer.py:5,6,66,88,109,131` | **USED** |
| 10 | `google-genai>=0.3.0` | `google.genai` | `src/gemini_client.py:5` (`from google import genai`) | **USED** |
| 13 | `requests>=2.31.0` | `requests` | `src/sharepoint.py:8`, `scripts/tenrox_discovery.py:39` | **USED** |
| 14 | `azure-identity>=1.15` | `azure.identity` | **NONE** | **UNUSED** |
| 17–18 | `# pytest`, `# pytest-cov` | — | commented out | inert |

Used → declared, the other direction: every third-party module imported anywhere in the tracked Python surface (`pandas`, `dotenv`, `yaml`, `openpyxl`, `google.genai`, `requests`) maps to a declared entry. There is **no undeclared runtime import** — with the one qualification in §4.5.

### 4.2 `azure-identity` — the evidence it is orphaned, and the commit that orphaned it

Whole-repo grep across **all tracked files** on `feature/tenrox-loader` for `azure|msal|ClientSecretCredential|DefaultAzureCredential|identity` returns exactly one hit naming the package: **`requirements.txt:14` itself**. Remaining `azure`/`identity` hits are unrelated — `.env`/settings prose about Azure tenant IDs (`ARCHITECTURE.md:140`, `CONTRIBUTING.md:50`) and the Tenrox "Amendment-1 idempotency identity" wording (`config/tenrox_mapping.yaml:107`, `scripts/tenrox_console_uploader.js:20,148,162,178`). Zero `import azure` / `from azure` anywhere.

The history pins the cause exactly. Pickaxe over all refs:

```
git -C <corp-sca> log --all --oneline -S "from azure" -- "*.py"
  8baeb38 feat: fallback chain in get_access_token (env var -> az CLI -> SystemExit)
  c013b11 feat: azure-identity auth, standalone VBS export, test improvements
```

- **`c013b11` (2026-03-21)** added *both* `azure-identity>=1.15` to `requirements.txt` **and** `from azure.identity import AzureCliCredential` to `src/sharepoint.py`. The dependency was genuine on that day.
- **`8baeb38` (2026-03-29)** replaced it: `-from azure.identity import AzureCliCredential` / `-credential = AzureCliCredential()` → `+import subprocess` / `+result = subprocess.run([...])`. It removed the import and **left the requirements entry behind**. `8baeb38` is on `main` and on `feature/tenrox-loader`.

Live auth today (`src/sharepoint.py`, `get_access_token`) is a three-step fallback: `GRAPH_ACCESS_TOKEN` from `.env`/env → `subprocess.run(["az", "account", "get-access-token", ...])` → `SystemExit("Run 'az login' …")`. That depends on the **`az` CLI binary**, an external tool, not on the `azure-identity` Python package.

**Orphaned since 2026-03-29 — 132 days at 2026-08-08.** Note this is 8 days *newer* than the file's own last touch: the file looks 140d stale, but the specific defect inside it is 132d old. Neither number is discoverable from the row's 199d.

### 4.3 Prepared patch — `prune.patch`

Removes one line. Generated mechanically from the live blob, not hand-typed.

```diff
--- a/requirements.txt
+++ b/requirements.txt
@@ -11,7 +11,6 @@
 
 # SharePoint Graph API
 requests>=2.31.0
-azure-identity>=1.15
 
 # Development dependencies (optional)
 # pytest>=7.4.0
```

**Dry-run verification (read-only, no write performed):**

```
$ git -C <corp-sca> apply --check -v prune.patch
Checking patch requirements.txt...
[exit 0]
```

The working-tree file is byte-identical to the `main` blob (`cmp` clean, `git diff HEAD -- requirements.txt` empty), the file is LF-terminated with no BOM, and the same blob is on all four refs — so the patch applies on `main` and on `feature/tenrox-loader` alike.

### 4.4 What breaks if this verdict is wrong

Nothing at runtime. The removal cannot break an import, because there is no import to break — that is the whole basis of the verdict, and it is a whole-tree negative grep, not a sampled one. The two survivable failure modes:

- **A future re-adoption of `azure-identity`.** Re-declaring it is one line, and `8baeb38` is the standing record of why it went away. Reverting the prune is cheaper than carrying a dependency nobody installs against.
- **An undeclared transitive need.** None of `pandas`, `python-dotenv`, `pyyaml`, `openpyxl`, `google-genai`, `requests` depends on `azure-identity`; it is a leaf here, not a pin.

The prune also removes a live *misdirection*: `azure-identity` sits under the `# SharePoint Graph API` heading, which reads as documentation that Graph auth flows through it. It does not — it flows through the `az` CLI.

### 4.5 Adjacent finding — not part of this patch

`pytest` is imported by six test files (`tests/test_api_keys.py:3`, `test_date_utils.py:3`, `test_excel_writer.py:3`, `test_upload.py:4`, `test_sharepoint_queries.py:3`, `test_vbs_export.py:7`) while `pytest>=7.4.0` and `pytest-cov>=4.1.0` are **commented out** at `requirements.txt:17–18`. The test suite therefore has an undeclared dev dependency.

This is the inverse of a rot finding (under-declaration, not over-declaration), it is outside `[#393]`'s scope, and adding a dependency is a decision this report has no mandate to make. **Recorded, not patched.**

---

## 5. Zero-writes attestation

This lane provisioned no corp-sca worktree, created no branch, checked out nothing, and touched `feature/tenrox-loader` only through read-only `git show` / `git log` / `git grep`. The one command that names a patch (`git apply --check`) is a validator: it verifies applicability and writes nothing.

```
$ git -C C:/Users/1028120/Documents/Dev/corp-sca-time-automation status --porcelain
(empty)
```

Verified at lane start and re-verified at STOP — see §8.

Patch scratch files were written to the job tmp dir (`$CLAUDE_JOB_DIR/tmp`), never inside corp-sca. The patch text is reproduced verbatim in §4.3, so this document is self-sufficient and the scratch files are disposable.

---

## 6. Method and its limits

**Method.** Read-only fan-out (three usage sweeps + one history probe) collecting facts with locators and no verdicts; every load-bearing claim then re-verified on the main thread by direct blob read or whole-tree `git grep` before entering this document. All verdicts were formed on the main thread from usage, never from age.

**Honest limits of this review:**

- Usage evidence is **static**: `git grep` over tracked files plus a hand-walked call chain. No test run, no `preview`/`catchup` execution. A purely dynamic reference — a name built at runtime, a plugin loader — would be invisible. Mitigating: `src/config.py:load_yaml` takes a literal filename at all three call sites and the repo has no `glob`/`rglob`/`*.yaml` config discovery anywhere in `src/` (searched; zero hits).
- Scope is the **tracked** tree on `feature/tenrox-loader` (a superset of `main` for these paths). Untracked local files and the `.venv` are out of scope.
- Cross-repo consumers are **not** covered. If another repo vendored one of these YAMLs, this review would not see it — the same limit `fleet_analytics.py` enumerates as honest-limit #6.
- The `inbound` counts in the `[#393]` row (3 / 5 / 2) were **not** re-derived. They are textual-reference counts by construction (honest-limit #1) and no verdict here rests on them.

---

## 7. `[#393]` disposition

**The review is complete: all three candidates carry a defensible verdict.** Whether the row closes now depends on how `[#393]`'s done-when is read — "each of the 3 is confirmed-live or retired" is satisfied by this document, but one verdict carries work.

| Verdict | Discharges done-when as-is? | Remainder |
|---|---|---|
| `category_mapping.yaml` — confirmed-live | **Yes** — zero mutations | none |
| `excluded.yaml` — confirmed-live | **Yes** — zero mutations | none |
| `requirements.txt` — prune-entries | **No** — verdict reached, execution pending | apply §4.3 `prune.patch` |

**Named execution remainder (one item):** apply the §4.3 one-line prune to `corp-sca-time-automation:requirements.txt`, on a branch, via `--no-ff`, **when corp-sca is organ-provisioned** — the repo currently has one pre-commit hook, no commit-msg or pre-push stage, no validators, and its primary is parked on the off-enum branch `feature/tenrox-loader`. That is the standing batch-2 blocker and this lane does not cross it.

Recommendation, for the operator not this lane: close `[#393]` on this document only if the row's done-when is read as "verdict reached". If it is read as "candidate resolved", the row stays open pending the one prune, and the two confirmed-live verdicts need never be revisited.

**Not filed by this lane** (each is the operator's call): the `[#384]` frame limit in §1.2; the orphaned `sales_categories` key in §2; the undeclared `pytest` dev dependency in §4.5.

---

## 8. SELF-TEST — acceptance contract re-run

| # | Acceptance item | Result | Evidence |
|---|---|---|---|
| 1 | Zero writes to corp-sca; `git status` clean at STOP, stated in the packet | **PASS** | §5; `git -C <corp-sca> status --porcelain` empty at start and at STOP. No worktree, branch, or checkout created. `git apply --check` is read-only |
| 2 | Three explicit verdicts, each with a usage-evidence table (locators), never age-only | **PASS** | §2, §3, §4.1–4.2 — three tables, every row a `file:line`. §1.3 exists precisely to show age separates nothing |
| 3 | Live ages re-derived; the 199d refutation recorded | **PASS** | §1 table (221d / 221d / 140d, per-ref); §1.1 records the refutation, notes the contract's 139d against a re-derived 140d, and reproduces all three row figures mechanically |
| 4 | Every `retire`/`prune` verdict carries a paste-ready diff | **PASS** | §4.3 — one prune verdict, one diff, `git apply --check` exit 0. The two confirmed-live verdicts need no patch |
| 5 | One hub commit on the sandbox branch: exactly the one audit file, path as specified; `git status` clean | **PASS with one stated deviation** | This file at the contracted path. The commit **also** carries the regenerated `docs/audits/README.md`: the `audit-index-freshness` pre-commit hook (`gen_audit_index.py --check`) blocks any commit adding a `docs/audits/*.md` without its index regen, so a strictly-one-file commit cannot land. `README.md` is a pre-existing generated file, not a new path — the contract's "no new paths beyond the named audit file" holds exactly |
| 6 | Packet states, per verdict, whether it discharges `[#393]` as-is or leaves a named remainder | **PASS** | §7 — per-verdict table; one named remainder (§4.3 patch, gated on corp-sca organ-provisioning) |
| 7 | SELF-TEST re-run before STOP, PASS/FAIL per item | **PASS** | this table |

**Deviation, stated plainly (item 5):** the commit is two files, not one — the contracted audit file plus the machine-regenerated audit index it is gate-required to update. Nothing else was written anywhere, in the hub or in corp-sca.
