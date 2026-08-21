# CLOUD-R1 — governance drift audit: ARCHITECTURE.md · CLAUDE.md · VISION.md

<!-- scope: meta -->

**Lane:** cloud — READ-ONLY review lane (`cloud-r1-governance-drift`), effort high
**Branch:** `claude/cloud-r1-governance-drift` · **Base:** detached `78267fd` (`origin/main` tip in this clone)
**Posture:** this lane REPORTS. It edits no doctrine, rules nothing, files no rows, closes no ids.
Every finding is EVIDENCE + RECOMMENDATION; the architect rules.

> **Citation note.** Every `:NNN` below is a **measurement taken on 2026-08-21 against `78267fd`**,
> not an anchor. Each is paired with a quoted phrase so it stays resolvable after the lines move —
> which they will, since finding **A5** of this audit is what happens when they don't.

---

## Contract conflict — reported, not improvised

The brief instructs: *"You mutate NOTHING except ONE file: `ARTIFACT-<slug>.md` … committed once on
your own session branch."* **The repo refuses that path**, and the brief's own clause says the repo
wins. Verified live against the gate module, not inferred:

```
$ python -c "import validate_hermetization as h; print(h.rule_a_violation('ARTIFACT-cloud-r1-governance-drift.md'))"
unsanctioned new top-level file 'ARTIFACT-cloud-r1-governance-drift.md' -- Tier-1 files are a
closed class (ADR-101 section 1); a genuinely new class is an ADR-101 amendment, not a drive-by add
```

`SANCTIONED_TIER1_FILES` (`scripts/validate_hermetization.py:82`) is a 20-entry closed set; a new
root file-class enters it only by ADR-101 amendment. `docs/audits/ARTIFACT-…md` is refused too — Rule
B, ADR-101 R4 casing. **Resolution taken:** the artifact is written to the repo-conformant home
`docs/audits/2026-08-21-fresh-eyes-cloud-r1-governance-drift.md` — `fresh-eyes` is a live member of
`AUDIT_CLASS_ENUM`, and the shape has direct precedent in a cloud read-only lane one day earlier
(`docs/audits/2026-08-20-technical-playbook-status.md`, branch `claude/playbook-status-census-2026-08-20`).
All three hermetization rules return `None` for this path. Still ONE file, still one commit.

**One debt is owed and deliberately NOT paid here:** adding a file to `docs/audits/` makes
`docs/audits/README.md` stale, and `audit-index-freshness` will BLOCK the operator's next commit.
Regenerating it would be a second mutation, which the brief forbids and which is the integrator's
surface, not a read-only lane's. **Run `python scripts/gen_audit_index.py --write` before your next
commit.**

## Environment limits — stated, so no green here over-reads

| Limit | Evidence | Consequence for this audit |
|---|---|---|
| **Shallow clone** | `.git/shallow` present, 12 graft points, 314 commits | Spine-walking instruments (`validate_git_backlog`, `validate_no_ff`, `block_ff_push`, `journal_anchor`) **were not run** — per the brief's guard. Finding **A15** is `UNVERIFIABLE-IN-CLONE` for this reason. |
| **`click` absent** | `ModuleNotFoundError: No module named 'click'` on `scripts/audit.py` | `audit.py checks` could not be executed. `ALL_CHECKS` was counted **from source** instead (`scripts/audit.py:3398-3445`) — a stricter read, not a weaker one. |
| **`uv` version mismatch** | `Required uv version ==0.11.19 does not match the running version 0.8.17` (ADR-106 pin) | No gate could be run through `uv run --locked`. |
| **pre-commit not armed** | no `.git/hooks/pre-commit`; `ModuleNotFoundError: No module named 'pre_commit'` | No gate fired on this commit. **This is not a defect** — it is exactly what ARCHITECTURE Ch4 predicts (see **A14**), and it is why the ADR-101 refusal above had to be checked by hand. |
| **No `gh` / GitHub Issues reach** | repo scope | Ch6's "15 open `nightly-triage` Issues, newest 2026-06-25" is `UNVERIFIABLE` (**A17**). |

---

## The operator's answer, in one paragraph

**Neither "stale" nor "stable by design" — the split runs exactly along the generated/hand-maintained
boundary, and it is systematic rather than incidental.** Every surface in these three files that is
machine-generated behind a regen-and-diff gate measured **exactly current**: CLAUDE.md §7's command
roster (8/8 vs disk), §11's ADR roster (carries **ADR-113**, Accepted 2026-08-19), §9's 19-id
pre-commit roster (set-identical to `.pre-commit-config.yaml`), `ecosystem/doc-counts.md` (43 checks
= live `ALL_CHECKS`; 19 gates = live config). Every confirmed STALE finding below is a
**hand-maintained enumeration that must be re-typed when a sibling surface moves** — the ADR roster,
the gate id list, the organ table, four `file:line` locators. CLAUDE.md does not change often because
it is **budget-bound at 198/200 counted lines** (measured live via its own checker), not because it is
finished: its two real defects are doctrine contradictions a roster gate structurally cannot catch.
And ARCHITECTURE is not merely aged — it is **silent on the working mode the repo actually runs**:
parallel worktree lanes, batch dispatch, the `.devcontainer` off-machine substrate (this very
session), and `deploy/lived_sandbox`. The most damning single number: ARCHITECTURE's own Ch2 note
names `ecosystem/organ-index.md` as its **verified source** and says *"when they disagree, trust the
index"* — the index counts **53 organs across 8 classes**; Ch2's hand table has **33 rows** and omits
three whole classes.

**Drift is proven, not inferred from age.** 8 STALE + 9 MISSING-COVERAGE across the three files;
14 claims verified CURRENT and recorded as such.

---

## 1. ARCHITECTURE.md — claim-by-claim

`last_reviewed: 2026-08-14` · 1021 lines · six chapters

| # | Claim (site) | Live evidence | Verdict | Proposed one-line fix |
|---|---|---|---|---|
| **A1** | Governing ADRs list ends at **ADR-112** (`:1012-1016`) | `docs/decisions/ADR-113-l0-l5-maturity-ladder-ratification.md` exists, **Accepted 2026-08-19**; `.claude/generated/recent-adrs.md` carries it | **STALE** | Add the ADR-113 bullet (L0–L5 maturity ladder ratified; one of three "L" namespaces). |
| **A2** | Purpose: *"It holds operational protocols, ADRs, intake docs, handoffs, templates, and **read-only validators**"* (`:130`); also `:372` *"Layer 2 hosts **read-only** validators"* | ~23 scripts under `scripts/` mutate state; `scripts/audit.py:3967` runs `git push origin`. Corrected at CLAUDE.md §5 rule 4 (v2.61), CLAUDE.md §3 (v2.62), and `VISION.md` `## Vision` ([#558], closed 2026-08-18) | **STALE** — **4th site** | Re-scope onto the landed CLAUDE.md wording: *"hub-local validators, generators and gates"*; the prohibition is on driving a CHILD repo's state. |
| **A3** | Ch2 pre-commit gate enumeration (`:600-621`) names **18** ids | `.pre-commit-config.yaml` declares **19**: `block-commit-on-main` is absent from the prose list. The same sentence's own parenthetical records *"sixteen of seventeen … then seventeen of eighteen … the same defect twice"* | **STALE** — **3rd recurrence** | Add `block-commit-on-main`; or delete the enumeration and keep only the pointer the sentence already carries. |
| **A4** | Ch2 header: *"Every enforcement/awareness organ, with its trigger…"* (`:269`) — a completeness claim | `ecosystem/organ-index.md` (Ch2's own declared verified source, `:262-267`): **53 organs across 8 classes**. Ch2's table: **33 rows**. Missing whole classes — `agent` (`ecosystem-snapshot`, `report-generator`), `rule` (`core-invariants`, `git-discipline`), `plugin` (`tier1-lifecycle` v0.1.11); missing organs — `/preflight`, `/lane-boot`, `/lane-integrate`, `/override`, `check-against-spec`, `arm_hooks.py`, `claude-notify.ps1` (×2), `block-commit-on-main` | **MISSING-COVERAGE** | Replace the completeness claim with the pointer the note already licenses (*"may be replaced by a pointer to it"*), keeping only the **failure-posture** column the index states it cannot carry. |
| **A5** | Ch2 `fleet_health.py` row cites the daily throttle at **`fleet_health.py:82`** (`:300`) | `:82` is a comment about a result-set ceiling. The `return d != date.today()` throttle is at **`:156`** | **STALE** (locator rot) | `fleet_health.py:82` → `fleet_health.py:156`. |
| **A6** | §Validators: *"Four claims (`_CLAIMS`, `validate_doc_claims.py:225-236`)"* (`:417`) | `_CLAIMS` is declared at **`:224`** and closes at **`:240`**; 4 claims ✓ | **STALE** (minor locator) | `:225-236` → `:224-240`. |
| **A7** | No pointer anywhere in Ch2/Ch6 to `ecosystem/conformance.md`; the path appears **only** in the ADR-85/86/87 governing bullet (`:994`) | The dashboard is **built and committed** — `scripts/gen_dashboard.py` ([#171] stage 1), `ecosystem/conformance.md` as-of 2026-08-20 HEAD `d436d64fff86`, plus an HTML sibling by operator addendum 2026-08-19. ADR-86 §2 requires *"ARCHITECTURE Ch2 gains a pointer to it (resolves the G7 coverage-matrix gap) — the pointer lands with the build (#171)"*. `tasks/171-*.md` is **`status: open`** with that pointer inside its Done-when | **MISSING-COVERAGE** | Add a Ch2 line pointing at `ecosystem/conformance.md` — **this is the last item blocking `[#171]`.** |
| **A8** | Ch3/Ch4/Ch5 are silent on the **off-machine substrate** | `.devcontainer/{devcontainer.json,Dockerfile,provision.sh}` tracked since 2026-08-18 ([#554]); **ADR-101 amendment 2026-08-18** adds `.devcontainer/` to the §1 sanctioned Tier-1 dirs; `validate_hermetization.py:78,162` carries it in both `SANCTIONED_TIER1_DIRS` and `_HOME_PATTERNS`. `docs/audits/2026-08-20-technical-codespaces-audit.md` is the cost/perf memo | **MISSING-COVERAGE** | One Ch4 row: the off-machine substrate as a distribution/execution context, pointing at ADR-101's 2026-08-18 amendment and `[#554]`. |
| **A9** | ADR-110 parallel/batch execution appears **only** in Governing ADRs (`:1005-1008`); no chapter covers it | This is the repo's dominant working mode — JOURNAL entries are overwhelmingly `worktree-lane-*` / `batch-N`; `check_stale_worktrees` is a live `ALL_CHECKS` member ([#505], `audit.py:3407`); `scripts/{batch_manifest,worktree_seed,worktree_import_proof}.py` and `.worktreeinclude` exist; `/lane-boot` + `/lane-integrate` ship. **The doctrine has a canonical home** — `protocols/PLAYBOOK.md` **Ch8 "Session boundaries"** (`:1233`, 166 lane/worktree/batch hits) — and ARCHITECTURE points at it **nowhere** (`grep -n "PLAYBOOK.*Ch8\|Session boundaries" ARCHITECTURE.md` → 0) | **MISSING-COVERAGE** | Add the pointer, not the doctrine: *"Parallel lanes / worktree dispatch / the ADR-110 batch protocol → PLAYBOOK Ch8."* This is exactly the file's stated design (*"Deep dives leave this map"*). |
| **A10** | `deploy/lived_sandbox/` is absent from §Validators, Ch2, Ch3, Ch4 | An 8-module Python package (`__init__/arc/cli/consumer/isolation/observe/oracle/spawn`) that **spawns a headless `claude -p` session** and verdicts enforcement-in-effect from transcript events + git state (Slice A isolation proof; Slice B acceptance instrument, [#252]) | **MISSING-COVERAGE** | One §Validators bullet; Ch3 needs a cell for *operator-invoked deterministic observer over an LLM stimulus* — its axis table has no home for this shape today. |
| **A11** | Ch5 Filenames names only `YYYY-MM-DD-slug.md` for dated artifacts (`:759-761`) | `docs/archive/` now holds **12** Workflow-produced research notes on a distinct grammar — `YYYY-MM-DD-research-<topic>-wf-<8-hex>.md`, all since 2026-08-09 | **MISSING-COVERAGE** | Name the `-wf-<id>` research-artifact grammar in Ch5, or record it as deliberately unruled. |
| **A12** | Codemap: *"Two modules (`scripts/codemap/` and `scripts/toc/` both qualify as Python packages)"* (`:159`) | `find scripts -name __init__.py` → exactly those two. `scripts/audit_checks/` (18 modules, [#533]) has **no** `__init__.py`, so it is correctly not a node | **CURRENT** | — |
| **A13** | Ch4: *"the hub's **six** exported hook ids — `codemap-freshness`/`-generate`, `toc-freshness`/`-generate`, `backlog-id-on-close`, `block-ff-push`"* (`:704`) | `.pre-commit-hooks.yaml` exports exactly those six (`:23,32,41,49,59,69`) | **CURRENT** | — |
| **A14** | Ch4: *"The plugin/pre-commit channels are **inert by design** in a fresh cloud clone — not bugs"* (`:714-715`) | Verified live in this cloud clone: `.git/hooks/` holds only `*.sample`; `import pre_commit` → `ModuleNotFoundError` | **CURRENT** — and load-bearing: it is what makes A-conflict above a manual check rather than a gate refusal | — |
| **A15** | `last_reviewed: 2026-08-14` vs the file's last commit | `git log -1 -- ARCHITECTURE.md` → `9997bc3` (2026-08-16, batch-6 merge). **But `9997bc3` is a graft point in `.git/shallow`**, so the file renders as a 1020-line ADD and no content diff exists here | **UNVERIFIABLE-IN-CLONE** | Operator: run `git log --no-merges -1 --format=%ad -- ARCHITECTURE.md` on the full clone. If it post-dates 2026-08-14, `canonical_freshness` (A2 leg) is FAILing and the brief's premise (*"stamp equal to its last touch"*) is false. |
| **A16** | Open-ticket claims: `#369` (boundary_headers wiring), `#391` (fleet_analytics nightly), `#366` (staged-blob gap), `#428` (dead triage producer), `#426` (routine retrofit), `#440` (tombstone), `#218` (deferred L3 phases) | `tasks/*`: all six `status: open`; `#218` `status: deferred` — matches the prose exactly | **CURRENT** | — |
| **A17** | Ch6: *"currently **15 open**, the newest opened 2026-06-25"* (`:902-903`) | No GitHub Issues reach from this lane | **UNVERIFIABLE** | Re-point at a computed surface rather than a restated count — the A3/A1 failure class applied to Issues. |
| **A18** | Frontmatter `reconciled_with: handoff-process@6.2.0` | `protocols/HANDOFF_PROCESS.md` → `Version: 6.2.0` | **CURRENT** | — |
| **A19** | Locators `fleet_parity.py:123` (`EVENTS_PATH`), `session_end_backpressure.py:14` (*"no longer has a HARD leg"*), `ADR-92:95` (amendment marker), `fleet_health.py:610,642,689` (`collect_load`/`load_line`/`append_load_row`) | All four resolve **exactly** | **CURRENT** — worth recording: the locators added most recently are the ones that hold | — |

---

## 2. CLAUDE.md — claim-by-claim

`last_reviewed: 2026-08-16` · version 2.62 · **198/200 counted lines, headroom 2**

> Budget measured live with the file's own checker, not estimated:
> `validate_doc_rot.scan_file_budget('CLAUDE.md', text, 200)` → `[]`; counted lines **198**
> (242 physical). **Every recommendation below is priced in counted lines**, because at headroom 2 the
> price is the decision.

| # | Claim (site) | Live evidence | Verdict | Proposed one-line fix |
|---|---|---|---|---|
| **C1** | §4 File lifecycle: *"**Living**: … `BACKLOG.md` (**update in place**)"* (`:65`) | `BACKLOG.md` is **GENERATED** from `tasks/` since the ADR-107 §7.2 source-of-truth flip ([#439], 2026-07-28). `tasks/` holds **300** task files + `manifest.json`; regeneration is `scripts/gen_task_tree.py --emit-source`; `audit.py::check_task_tree_coherence` gates it. ARCHITECTURE Ch5 (`:774-799`) and PLAYBOOK (`:3952`) both state the flip correctly — **CLAUDE.md is the only one of the three that still tells the executor to hand-edit it** | **STALE** — highest operator impact in this audit | Move `BACKLOG.md` out of *Living*: *"Generated: `BACKLOG.md` — edit `tasks/`, then `gen_task_tree.py --emit-source` (ADR-107)."* Cost: **0 net counted lines** (in-place edit). |
| **C2** | §5 rule 7: *"**No executable rules in this repo** — those go in `~/.claude/` with `verify:` lines"* (`:95`) | `.claude/rules/git-discipline.md` is a repo-local rule file carrying **three** `verify:` lines — and §9 (`:186-187`) lists it approvingly. The file also carries two load-bearing standing operator orders (**MERGE IS ATOMIC**, **WORKTREE TEARDOWN IS TWO BRANCHES**) | **STALE** — the file forbids at §5 what it rosters at §9 | Re-scope rule 7 the way rule 4 was re-scoped in v2.61 (converge on the accurate site), or record the `.claude/rules/` carve-out. **Needs a ruling** — the same shape as the v2.61 Position-0 act. |
| **C3** | §7/§8/§9 enumerate commands, skills, hooks, rules — **no agent class, no workflow class** | `.claude/agents/artifact-reader.md` and `.claude/workflows/conformance-hub.js` are live organs (`ecosystem/organ-index.md` classes `agent`, `workflow`; ARCHITECTURE Ch2 rows `:310`, `:314`). A session reading only CLAUDE.md never learns `artifact-reader` exists — the organ built precisely for the >20k-token files this repo is made of | **MISSING-COVERAGE** | One line under §8: *"Agents/workflows: `.claude/agents/artifact-reader` (>20k-token reads), `.claude/workflows/conformance-hub.js`; full inventory `ecosystem/organ-index.md`."* Cost: **1 counted line**. |
| **C4** | §1 names PLAYBOOK as *"consult on demand"* with **no index of which chapter answers what**; §3's chapter pointers route only into ARCHITECTURE | The daily working mode — worktree lanes, dispatch, batch protocol, model/effort routing — lives in **PLAYBOOK Ch8 "Session boundaries"** (`:1233`). CLAUDE.md never names it (`grep -c "Ch8\|Session boundaries" CLAUDE.md` → 0) | **MISSING-COVERAGE** | Extend §3's pointer line: *"lanes / worktrees / batch dispatch → PLAYBOOK Ch8."* Cost: **0 counted lines** (append to the existing §3 pointer sentence). |
| **C5** | §2 Critical paths: `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`, `ARCHITECTURE.md` (`:40`) | Omits **`tasks/`** (300 files, the BACKLOG source of truth since 2026-07-28) and **`ecosystem/`** (`organ-index.md`, `doc-counts.md`, `registry.md`, `index.yaml`, `parity-surfaces.yaml`, `disposition-register.yaml`, `conformance.md`) — the two trees a wrong edit does the most damage in | **MISSING-COVERAGE** | Append `tasks/`, `ecosystem/` to the Critical-paths line. Cost: **0 counted lines**. |
| **C6** | §6 Session start protocol — one procedure, no off-machine variant (`:107-114`) | Steps 1 and 5 behave differently on the `[#554]` substrate: shallow clone (spine instruments unrunnable), hooks unarmed (`pre-commit install` owed), `uv` pin unsatisfiable. Encountered live by this lane | **MISSING-COVERAGE** | Add a cloud clause: *"off-machine (`.devcontainer`/cloud): confirm hooks armed + history unshallowed before trusting any spine check."* Cost: **1 counted line.** |
| **C7** | §9 pre-commit roster — 19 named hooks (`:162-180`) | Set-identical to `.pre-commit-config.yaml`'s 19 ids, order-independent. This is the claim `validate_doc_claims` claim 2b (`precommit_hook_roster@CLAUDE.md`) machine-holds — and it is **the one enumeration in these three files that a gate protects, and the one that is right** | **CURRENT** | — (the control case: gate the enumeration and it stops drifting) |
| **C8** | §7 repo command roster (generated fragment) | `.claude/generated/commands-repo.md` lists 8; `.claude/commands/` holds exactly those 8 | **CURRENT** | — |
| **C9** | §11 recent ADRs (generated fragment) | Lists ADR-109…**113** — i.e. CLAUDE.md is **ahead of ARCHITECTURE** on the ADR horizon (A1), purely because a generator does what a hand-list can't | **CURRENT** | — |
| **C10** | §8 skills: *"`.claude/skills/` holds `verify` + `check-against-spec`"* | `ls .claude/skills/` → exactly those two | **CURRENT** | — |
| **C11** | §9 session hooks sentence: 4 SessionStart surfacing organs + `arm_hooks.py` (3 hook types) + Stop backpressure + PreToolUse guard | `.claude/settings.json`: SessionStart = `fleet_health.py`, `surface_triage.ps1`, `billing_leak_sentinel.ps1`, `changelog_sentinel.py`, `arm_hooks.py`; Stop = `session_end_backpressure.py`; PreToolUse = `scripts/hooks/block_immutable_edits.py`. Hook types = pre-commit / commit-msg / pre-push = 3 | **CURRENT** | — |
| **C12** | §3: ARCHITECTURE is *"a six-chapter map"* | Ch1 Layers · Ch2 Organs · Ch3 Automation axes · Ch4 Distribution · Ch5 Zones · Ch6 Verification mesh | **CURRENT** | — |
| **C13** | §4 Freshness cadence: *"`last_reviewed` … means re-read end-to-end and confirmed accurate — **not** merely touched"* (`:66`) | The discipline is visibly held: v2.57, v2.60 and v2.62 each explicitly refuse or justify a same-day re-stamp | **CURRENT** — and it is why this class needs **no** new line (see M9) | — |
| **C14** | §12 locator `scripts/audit.py:4707` *"pushes to `origin`"* (`:228`, `:230`) | Live push site is **`scripts/audit.py:3967`** (`_replicate_automation_branch`) | **STALE** (historical record; §12 is a record and is not edited backwards per the v2.56/B6 precedent) | Note only — do not edit. |

---

## 3. VISION.md — claim-by-claim

`last_reviewed: 2026-08-18` · 190 lines · freshness **CURRENT** (last commit `82fb036`, 2026-08-18, non-merge)

| # | Claim (site) | Live evidence | Verdict | Proposed one-line fix |
|---|---|---|---|---|
| **V1** | Audit support: *"`scripts/audit.py` per ADR-36 — `health`/`repo`/`run`/`registry`/`ship-gate`/`checks` commands, **read-only**"* (`:158-160`) | `audit.py:3967` runs `git push origin`; `_commit_routine_outputs` writes commits to `automation/fleet-audit`. **This is the 5th site of the claim [#558] closed on 2026-08-18** — three lines below the `## Vision` sentence that ticket fixed, in the same file, on the same day. [#558]'s own Done-when demanded *"a fleet-wide re-measurement of the claim covers files beyond `CLAUDE.md`"* | **STALE** — **5th site**, and the strongest single piece of evidence in this audit | Drop `read-only` or re-scope it: the invariant is *read-only **on siblings*** (ARCHITECTURE invariant 2, `:207-210`), which is true and checkable. |
| **V2** | Command list `health`/`repo`/`run`/`registry`/`ship-gate`/`checks` | `scripts/audit.py:4140,4226,4266,4286,4410,4502` — exactly six, exactly those | **CURRENT** | — |
| **V3** | *"The fleet is **nine** git repos (ADR-104): the hub … plus eight child repositories — `ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`, `demo-prep`, `life-architect`, `terminal-setup`, `win-tooling`"* (`:107-111`) | `ecosystem/registry.md` carries exactly those 9 rows | **CURRENT** | — |
| **V4** | *"`ecosystem/registry.md` — hand-maintained; add a row when a repo joins"* (via the surfaces it defers to) | **ADR-109 §2 rules that `ecosystem/registry.md` LOSES AUTHORITY** — ARCHITECTURE carries this (`:1011`); VISION never mentions ADR-109, the desired-state contract, or `ecosystem/schema/` at all | **MISSING-COVERAGE** | One clause in Relationships: *"registry authority is superseded by the ADR-109 desired-state contract; file retirement is [#383] work."* |
| **V5** | References list (`:181-189`): ESSENTIALS · PLAYBOOK · JOURNAL · BACKLOG · CONTRIBUTING · `docs/decisions/` · ADR-88 | Omits **`ARCHITECTURE.md`** (mandatory for every repo per ADR-51 as amended 2026-05-23, and this file's own structural sibling), **`LESSONS.md`** (the artifact VISION's own *"Lessons capture as default"* emphasis calls first-class), **`protocols/STANDING_RULINGS.md`** (the live operator-ruling register, cited 5× in CLAUDE.md), and **`tasks/`** (BACKLOG's source of truth) | **MISSING-COVERAGE** | Add the four. References is the one list a fresh reader actually walks. |
| **V6** | *"archive as `docs/archive/YYYY-MM-DD-vision-vN-realized.md`"* (`:165-166`) | `docs/archive/` is now a **mixed genre** — 12 of its 22 entries are Workflow research notes (`-wf-<id>`), all since 2026-08-09 | **MISSING-COVERAGE** (minor) | Note that `docs/archive/` also hosts research artifacts, so a future vision-realized file lands beside them by design. |
| **V7** | Host-binding paragraph: `ecosystem/index.yaml`, the marketplace path in `.claude/settings.json`, `scripts/fleet-baseline.task.xml`, gitignored `ecosystem/*/state.yaml` (`:17-27`) | All four verified present; `.claude/settings.json` carries `C:\Users\1028120\Documents\Dev\.dev-knowledge` | **CURRENT** — unusually precise, and it is the paragraph that made this cloud lane legible | — |
| **V8** | *"the self-audit `health` (all registered `ALL_CHECKS` — **count via `scripts/audit.py checks`**)"* (`:161`) | `ALL_CHECKS` = **43** (`audit.py:3398-3445`, counted from source); `ecosystem/doc-counts.md` = **43** ✓ | **CURRENT** — and it is the model fix for A1/A3/A17: point at the computing surface, never restate | — |
| **V9** | *"Tier classification retired 2026-05-23 … `.dev-knowledge` declares no tier"* (`:169-175`) | No `tier:`/`scale:` in any frontmatter of the three files | **CURRENT** | — |

---

## 4. CLAUDE.md extra pass — repeated executor mistakes, ranked

**Method.** `JOURNAL.md` split on its `###` entry headers → **947 entries**; each class counted as
*entries containing it* (not raw line hits), so one entry narrating a mistake five times counts once.
`docs/audits/*.md` → **641 files**, counted as *files mentioning*. Both are lower bounds: they count
mistakes that were **recorded**, and a mistake nobody caught is invisible to this method.

Ranked by frequency. **Cost is in counted lines against the live headroom of 2.**

---

**M1 · Acting on a locator without resolving it — 110/947 JOURNAL entries · 104/641 audits**

The single most frequent recorded failure, and it is still live today.

- `JOURNAL.md` 2026-08-20 (k): a handoff supplement asserted *"'Push-before-delete on every harvest' — JOURNAL entry (i) exists."* → **"It does not, and never did."** The same entry records that `protocols/STANDING_RULINGS.md:1866` (Q3) cites the same non-existent entry — *"one origin, not two independent errors."*
- `ARCHITECTURE.md:960-964`: *"this line said it 'survives as BACKLOG **#85**', but #85 was closed on 2026-06-07 … the pointer had been dead for two months."*
- `ARCHITECTURE.md:893`: the named conformance branch *"is long gone."*
- This audit's **A5** (`fleet_health.py:82` → `:156`) and **A6** — the same class, found again.

**The repo already built the cure and CLAUDE.md never names it.** `/preflight` — *"Verify every repo
locator a contract or prompt cites — file:line, headings, SHAs, `[#id]` liveness — BEFORE acting on
it"* — exists, ships, and is **wired into no gate**. It appears in CLAUDE.md only as a one-line entry
inside a generated fragment.

> **Line that would have prevented it (§10 anti-pattern, cost 1):**
> **Acting on an unresolved locator** — a `file:line`, heading, SHA, branch or `[#id]` you have not
> resolved is a claim, not evidence. Run `/preflight` on any contract before you act on it.

---

**M2 · Restating a volatile count or roster in prose — 29/947 entries · 95/641 audits**

ARCHITECTURE is its own best witness, four times over:

- `:616-621` — *"this list named **sixteen of seventeen** from 2026-08-03 to 2026-08-10 … then **seventeen of eighteen** from 2026-08-11 to 2026-08-12 … **the same defect twice**."* **This audit makes it eighteen of nineteen — three.** (A3)
- `:147-149` — *"A bare 'ratified through ADR-NN' horizon is not stated here — it rots at the next accepted ADR **and did**."* The curated list then rotted anyway at ADR-113. (A1)
- `:541` — the carrier roster *"said 'five' until 2026-08-10."*
- `:474` — doc→code coverage *"said '13' while `coverage_scope` held 15."*

The fix pattern is already doctrine (`ecosystem/doc-counts.md` header; VISION **V8**) — it is simply
not stated as a rule an executor must follow.

> **Line that would have prevented it (§4 Conventions, cost 1):**
> **Never restate a count or roster in prose** — cite the surface that computes it (`audit.py checks`,
> `ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, the manifest `carriers:` block). A number
> typed into a doc is stale at the next commit.

---

**M3 · A drift sweep scoped to the file being edited — 5 confirmed sites of ONE claim**

The cleanest evidence chain in the repo, because each step is dated:

1. `CLAUDE.md:228` (v2.61, 2026-08-16) fixes §5 rule 4; records a **second site** at §3 and leaves it.
2. `CLAUDE.md:226` (v2.62, same day) fixes §3 and declares **"Fleet-wide drift on this claim is now 0 sites."**
3. `tasks/558-*.md` (2026-08-17): **third site** in `VISION.md` — *"Both of those entries recorded fleet-wide drift on this claim as reaching 0 sites — `VISION.md` is the evidence that the count was measured over `CLAUDE.md` alone, **which is the reusable finding here: a drift sweep scoped to the file being edited will keep reporting zero.**"* Closed 2026-08-18.
4. **This audit: sites four and five** — `ARCHITECTURE.md:130` (**A2**) and `VISION.md:160` (**V1**), the latter three lines from the sentence [#558] repaired.

[#558]'s Done-when explicitly required the re-measurement to *"cover files beyond `CLAUDE.md`"*. It
did not.

> **Line that would have prevented it (§10 anti-pattern, cost 1):**
> **Declaring a claim fixed "everywhere" after a single-file sweep** — measure repo-wide
> (`grep -rn --include=*.md`) before writing "0 sites"; the sweep that only reads the file you are
> editing always returns zero.

---

**M4 · Leftovers: worktrees, branches and scratch not torn down — 87/947 entries · 62/641 audits**

The rule text itself records the recurrence count. `.claude/rules/git-discipline.md`:

- *"**MERGE IS ATOMIC** (standing operator rule, **established after three repeats**)"* — merge + push + delete source branch are one operation.
- *"**WORKTREE TEARDOWN IS TWO BRANCHES, NOT ONE** … A leftover provisioning branch is a defect, not a pending decision — **it is the half of teardown that gets forgotten** because the work branch is the one you were thinking about."*

`check_stale_worktrees` was built for this ([#505], now a live `ALL_CHECKS` member). CLAUDE.md §5
rule 9 covers *"no leftovers"* generically but **never names the two-branch teardown or MERGE IS
ATOMIC** — both live only in a rule file that §9 mentions in a single line.

> **Line that would have prevented it (§5 rule 9 extension, cost 1):**
> Teardown is **two** branches — `worktree remove` + `prune` + delete the work branch **and** the
> `worktree-<name>` provisioning branch; and a merge you were authorized to make already includes
> push + delete of the source (MERGE IS ATOMIC, `.claude/rules/git-discipline.md`).

---

**M5 · A green that proves nothing — 34/947 entries · 77/641 audits ("vacuous") · 18 ("self-referential")**

- `JOURNAL.md` 2026-08-11 (s): *"a 0 that proves nothing until you break it on purpose."*
- `JOURNAL.md`: *"the registry test is parametrized **over the registry**, so it has no external denominator; **second instance of one recurring shape** (a validator checked against its own artifact, after the rule-14 leg-(a) map-vs-map vacuity)."*
- `ARCHITECTURE.md:588-591`: *"No green — test name, output, or this map — reads as 'fully proven' while a cell is skipped or gapped."*
- `ARCHITECTURE.md:324`: `routine_consumers` — *"COVERAGE BOUNDARY — green says almost nothing."*

CLAUDE.md §10 carries only the narrow *"Running validators with no args"*. The class is wider: same
denominator on both sides, skipped cells, scope narrower than the claim.

> **Line that would have prevented it (§10, replacing the narrow one, cost 0):**
> **Trusting a green you did not try to break** — always pass `--all` or explicit paths; a check
> compared against its own artifact has no external denominator. State what your green excludes
> (skips, scope, `n/a`).

---

**M6 · Asserting a fact from belief rather than a live read — 46/947 entries · 81/641 audits ("unverified")**

`JOURNAL.md` 2026-08-20 (k) names the mechanism exactly: *"the outgoing architect **believed** the
entry existed and the transcription seat **carried the belief** into the register without checking
it."* This is M1's upstream cause — the locator is unresolved because the fact was inherited.

> **Line (§10, cost 1):** **Carrying a fact from a brief, summary or prior chat** — the repo is the
> record; re-read the subject from disk before you write about it.

---

**M7 · `--no-verify` / `SKIP=` used as convenience — 84/947 entries · 105/641 audits**

The tell is that a *clean* run is worth recording: merge `9997bc3`'s body reads *"Full gate stack;
**no `--no-verify`, no `SKIP=`**."* `CLAUDE.md:180` already states the escape and its backstop
(`journal_spine_anchor` FAILs, not WARNs). **Adequately covered — no new line owed**; the existing
§9 text carries it.

---

**M8 · Merging to `main` without a JOURNAL SHA anchor — 55/947 entries**

`scripts/session_end_backpressure.py:14-22` records why the teeth moved: the Stop-hook hard leg
*"fired **NINE** consecutive times"* on 2026-08-03 with zero enforcement pressure. `CLAUDE.md:226`
records `audit-health` **blocking a merge** on `journal_spine_anchor` as recently as batch 6.
**Adequately covered** by §9's `block-unanchored-push` row — the frequency reflects the gate working,
not the rule missing. **No line owed.**

---

**M9 · `last_reviewed` re-stamped without a genuine re-read — 10/947 entries**

`ecosystem/doc-counts.md`'s header names the origin (*"the 2026-07-01 forced-false-stamp failure"*).
CLAUDE.md §4's Freshness-cadence line already states the rule, and v2.57/v2.60/v2.62 each visibly
refuse a same-day re-stamp. **Covered — no line owed.** Recorded here because "low frequency after a
line landed" is the control case proving M1–M5 are line-shaped problems.

---

**M10 · Hand-editing (or hand-merging) a generated artifact — 3/947 entries, 8 gates**

Low recorded frequency **because it was mechanized**: `codemap-`, `toc-`, `roster-`,
`claude-rosters-`, `audit-index-`, `organ-index-`, `intake-index-freshness` plus
`check_task_tree_coherence` — eight regen-and-diff gates. Merge `9997bc3`: *"Generated-file
conflicts, if any, resolved by **REGENERATION** … rather than hand-merge."* The one place the rule
is **not** mechanized is the one where it is still wrong in prose — **C1**, `BACKLOG.md`.

> **Line (§4 File lifecycle, cost 0 — replaces the wrong clause):**
> **Generated:** `BACKLOG.md` (from `tasks/` — edit the tree, then `gen_task_tree.py --emit-source`;
> never hand-edit, never hand-merge a generated file's conflict).

---

**Budget arithmetic for the operator.** M1–M6 total **5 counted lines** against a live headroom of
**2**. M5 and M10 are free (in-place rewrites of existing lines). So the affordable set today is
**M5 + M10 + two of {M1, M2, M3}**. Buying more means condensing §12's oldest bullets to git first —
the v2.59 and v2.62 precedent, and ADR-49/ADR-65 §1 both name git as the destination.

---

## 5. Top-10 fixes, ranked by operator impact

```
 1. CLAUDE.md §4 — move BACKLOG.md from "Living: update in place" to "Generated from tasks/";
    it has been generated since [#439], 2026-07-28.                          {SAFE-MECHANICAL}
 2. VISION.md :160 — drop/re-scope "read-only" on audit.py (it pushes to origin at
    audit.py:3967); 5th site of the [#558] claim, in the file [#558] fixed.  {SAFE-MECHANICAL}
 3. ARCHITECTURE.md :130 — re-scope "read-only validators" onto the landed CLAUDE.md
    §5 rule-4 wording; 4th site of the same claim.                           {SAFE-MECHANICAL}
 4. ARCHITECTURE.md Governing ADRs — add the ADR-113 bullet (Accepted 2026-08-19);
    CLAUDE.md §11's generator already carries it.                            {SAFE-MECHANICAL}
 5. ARCHITECTURE.md :609 — add `block-commit-on-main` to the Ch2 gate list (18 of 19);
    third recurrence, recorded in that sentence's own parenthetical.         {SAFE-MECHANICAL}
 6. ARCHITECTURE.md Ch2 — add the `ecosystem/conformance.md` pointer ADR-86 requires;
    it is the last open item inside [#171]'s Done-when.                      {SAFE-MECHANICAL}
 7. ARCHITECTURE.md :300 / :417 — locator repair: fleet_health.py:82 -> :156,
    validate_doc_claims.py:225-236 -> :224-240.                              {SAFE-MECHANICAL}
 8. ARCHITECTURE.md Ch2 — retire the "every organ" completeness claim in favour of the
    pointer to ecosystem/organ-index.md (53 organs/8 classes vs 33 rows), keeping only
    the failure-posture column the index states it cannot carry.        {NEEDS-ARCHITECT-RULING}
 9. ARCHITECTURE.md + CLAUDE.md — point at PLAYBOOK Ch8 for lanes/worktrees/ADR-110 batch
    dispatch, and add Ch4 rows for the .devcontainer substrate and deploy/lived_sandbox;
    the dominant working mode is absent from the map.                   {NEEDS-ARCHITECT-RULING}
10. CLAUDE.md — condense §12's oldest bullets to git (v2.59/v2.62 precedent) to buy budget,
    then spend it on M1 (/preflight before acting on a locator) and M2 (never restate a
    count); and resolve §5 rule 7 against .claude/rules/git-discipline.md.
                                                                        {NEEDS-ARCHITECT-RULING}
```

**Owed by this lane, unpaid on purpose:** `python scripts/gen_audit_index.py --write` — see the
contract-conflict section above.

---

**Lane:** cloud-r1-governance-drift · **read-only** · no rows filed, no ids closed, no doctrine edited.
