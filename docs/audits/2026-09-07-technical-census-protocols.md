# Census — `protocols/` — 2026-09-07 · sweep lane S-09 (READ-ONLY)

**Consumer:** `[#227]` (AGENT_FRAMEWORK relocation — this census supplies its measured witness), `[#628]` (ESSENTIALS dissolution — §"ESSENTIALS consumer census" below is the D9 input), `[#285]` (PLAYBOOK + ENVIRONMENT freshness gating), `[#356]` (RULING-W legibility — two of its evidence locators are re-measured here), `[#327]` (protocols-as-interface-genre ruling). The substantive citations are the paths carried in every row below; the ids above are the governance surfaces that consume this file.

> **What this file is.** A read-only inventory of `protocols/` — 14 files at the top level plus 2 under `archive/` — with one verdict per file and a witness behind each. **Nothing was moved, edited, renamed or deleted.** Every verdict is a **PROPOSAL** the operator rules. Three defects found in passing are **reported, not repaired** (§Proposals → "Reported, not fixed").
>
> Beyond the plain inventory this lane was asked three questions: **consumers per protocol**, **duplicated doctrine across two files**, and the **`ESSENTIALS.md` consumer census** feeding D9. All three are answered below.

**Provenance.** Measured on branch `claude/census-protocols`, synced to `origin/main` at `5f27b20` (merge was already up to date). Consumer counts are `grep -rIl` over the tree with `.git` excluded, bucketed into **live** (`scripts/ tests/ .claude/ templates/ deploy/ ecosystem/ tasks/ config/ plugins/` + root canonical docs), **historical** (`docs/ JOURNAL.md LESSONS.md logs/`) and **sibling** (other `protocols/*.md`). The bucketing is deliberate and follows `scripts/consumer_at_landing.py`'s own pool doctrine: *"A mention in a session log or a machine baseline is a record that the file existed, not evidence that anything consumes it."*

**Two measurement constraints, stated before the numbers rather than after.** (1) The clone is **shallow** — `.git/shallow` carries 17 grafts and `git log` reaches only 278 commits back to 2026-09-01, so *last-content-commit* is a usable witness for **10** of the 16 files and **unavailable** for 6 (see Honest limits). Every verdict below therefore rests on a **consumer** or **generator** witness, never on a date alone. (2) `uv run --locked` **cannot execute here** — the pin is `==0.11.19`, the container has `0.8.17` — so no repo validator, gate or test was run. Where a gate's behaviour is asserted below it was derived by reading the module and, in one case, re-implementing its regex by hand against the live tree; that is said explicitly at each site.

---

## Inventory

Sizes in bytes. **live/hist/sib** = consumer files by bucket. **Witness** = what the verdict rests on.

| File | Bytes | Lines | Frontmatter | live / hist / sib | Witness | Verdict |
|---|---|---|---|---|---|---|
| `AGENT_FRAMEWORK.md` | 3,747 | 54 | `last_reviewed: 2026-09-06` · `status: active` | 1 / 31 / 2 | **Zero** references in `scripts/`, `tests/`, `.claude/`, `templates/`, `deploy/`. Its one live hit is the open row that proposes moving it: `tasks/227-relocate-agent-framework-md-out-of-protocols.md`. Self-labelled *"v0.1 stub, NOT implemented"* (line 10). | **RELOCATE** → `docs/` |
| `AI_COUNCIL_PROCESS.md` | 26,409 | 433 | `last_reviewed: 2026-09-04` · `status: active` | 14 / 76 / 5 | Gate-bound: member of `audit.py::_HUB_ONLY_FRESHNESS_FILES` (line 479) and of `canonical_docs.STRUCTURE_DOCS`; read by `scripts/check_provider_registry.py`, `tests/test_provider_registry.py`, `tests/test_audit.py`. | **KEEP** |
| `DEFINITION_OF_DONE.md` | 13,588 | 197 | `last_reviewed: 2026-09-02` · `status: active` | 11 / 132 / 6 | Member of `_HUB_ONLY_FRESHNESS_FILES`; read by `scripts/audit.py`, `tests/test_doc_code_edge.py`. Named as canon by `HANDOFF_BOOT.md:245`. | **KEEP** |
| `ENVIRONMENT.md` | 20,005 | 347 | **NONE** — prose `Last updated: 2026-09-06` only | 5 / 102 / 4 | **Zero** `scripts/`/`tests/` references. Witnessed instead by two open rows that presuppose it — `tasks/71-…md` (reconcile its `~/.claude/` tree) and `tasks/285-…md`, whose scope was **widened 2026-09-05 (R5/B10)** to fold ENVIRONMENT in — plus the roster entry at `protocols/README.md:25`. | **KEEP** (ungated — see Proposals) |
| `ESSENTIALS.md` | 16,461 | 189 | `last_reviewed: 2026-09-01` · **`status: superseded`** | 32 / 356 / 8 | Member of `canonical_docs.FRESHNESS_FILES` — the **portable** base every consumer inherits — and of `STRUCTURE_DOCS`; declared `freshness_gated: true` in **six** `deploy/manifest-v{1.1.0,1.2.0,1.3.0,1.3.1,1.4.0,1.5.0}.yaml`. Dissolution is owned by `[#628]`. | **KEEP** pending `[#628]` — explicitly **NOT** retire |
| `FUNNEL_LIFECYCLE.md` | 34,353 | 475 | `last_reviewed: 2026-09-06` · `status: active` | 0 / 12 / 1 | **Zero named references anywhere in code.** Its real consumer is positional: `scripts/funnel_lifecycle.py::ready_threshold` globs `protocols/*.md` and returns the first regex match. Re-implementing `_READY_THRESHOLD_RE` (`funnel_lifecycle.py:174-180`) by hand against the live tree resolves to **`protocols/FUNNEL_LIFECYCLE.md:322`, N=30 days** — this file arms that gate today. | **KEEP** |
| `HANDOFF_BOOT.md` | 17,987 | 258 | `last_reviewed: 2026-09-07` · `reconciled_with: handoff-process@7.0.0` | 44 / 320 / 8 | Read by `scripts/assemble_paste.py`, `scripts/audit_checks/check_boot_byte_budget.py`, `scripts/gen_trend_dashboard.py`; 3 test modules. | **KEEP** |
| `HANDOFF_PROCESS.md` | 116,411 | 1,563 | `last_reviewed: 2026-09-06` · `status: stable` · `Version: 7.0.0` | 126 / 500 / 11 | The most-consumed file in the folder: **9 scripts, 15 test modules**. It is the spec of record in `validate_reconciliation._SPEC_REGISTRY` and the version source for `check_handoff_version_stamp`. | **KEEP** |
| `OPERATOR-INTERFACE.md` | 18,038 | 276 | `last_reviewed: 2026-09-06` · `reconciled_with: handoff-process@7.0.0` | 5 / 29 / 5 | Read by `scripts/assemble_paste.py`. Carries a live `reconciled_with` edge, so `validate_reconciliation.enumerate_edges` enumerates it. | **KEEP** |
| `PLAYBOOK.md` | 490,615 | 6,157 | `reconciled_with: handoff-process@7.0.0` — **no `last_reviewed`** | 96 / 532 / 10 | **10 scripts, 16 test modules**; member of `STRUCTURE_DOCS`; read by `scripts/gen_lane_contract.py`, `dispatch_drift.py`, `validate_doc_structure.py`. | **KEEP** |
| `README.md` | 3,543 | 57 | `last_reviewed: 2026-09-06` · `reconciled_with: handoff-process@7.0.0` | 6 / 17 / 1 | Read by `scripts/preflight_contract.py` and `tests/test_canonical_docs.py`; it is the folder's own genre charter and the roster every other row here is checked against. | **KEEP** |
| `REPO_ONBOARDING.md` | 15,206 | 262 | `last_reviewed: 2026-09-06` · `status: active` | 6 / 17 / 1 | `tests/test_validate_hermetization.py` — the ADR-101 home-allowlist test that admits it into `protocols/` after the 2026-07-22 `docs/runbooks/` collapse. Thinnest code footprint of the KEEPs: **1 test, 0 scripts**. | **KEEP** |
| `SESSION_SETUP.md` | 9,401 | 236 | `last_reviewed: 2026-09-02` · `status: active` · `reconciled_with: handoff-process@7.0.0` | 7 / 94 / 5 | Member of `_HUB_ONLY_FRESHNESS_FILES`; read by `scripts/audit.py`, `tests/test_audit.py`. | **KEEP** (body drift reported below) |
| `STANDING_RULINGS.md` | 287,055 | 4,091 | `last_reviewed: 2026-09-06` · `status: active` | 145 / 319 / 6 | Highest live consumer count in the folder: **19 scripts**, incl. `validate_landing_predicate.py` which names it `_DEFAULT_REGISTER` (line 54) and parses its ` ```landed ` blocks; plus `silent_rule_detector.py`, `validate_hermetization.py`, `journal_anchor.py`, `preflight_contract.py`. | **KEEP** |
| `archive/HANDOFF_PROCESS_v3.4.md` | 53,121 | 898 | none (`ARCHIVED 2026-05-29` banner) | — | Already **at** its retention home. Cited by `protocols/STANDING_RULINGS.md:2995` as an un-repointable citer in the W6 `exempt-permanent` ruling; `protocols/archive/` is a sanctioned dir in `ecosystem/fleet-shape-spec.yaml:215` and a scan-exclusion in `canonical_docs.py:214`. | **KEEP** (in place) |
| `archive/HANDOFF_PROCESS_v4.4.md` | 39,856 | 671 | none (`ARCHIVED 2026-06-11` banner) | — | **Not merely history — an active-path spec.** `.claude/commands/handoff.md:213` names it *"Spec (frozen)"* for the v4 flow, and `:63`/`:72` route to it. Also `tests/test_canonical_docs.py:435`. | **KEEP** (in place) |

**Folder totals:** 16 files, 1,165,796 B, 16,164 lines. Two files — `PLAYBOOK.md` and `STANDING_RULINGS.md` — carry **66.7 %** of the folder's bytes.

---

## Consumers per protocol — the ranking, and what it does and does not mean

Live-bucket consumer counts, descending: `STANDING_RULINGS` 145 · `HANDOFF_PROCESS` 126 · `PLAYBOOK` 96 · `HANDOFF_BOOT` 44 · `ESSENTIALS` 32 · `AI_COUNCIL_PROCESS` 14 · `DEFINITION_OF_DONE` 11 · `SESSION_SETUP` 7 · `README`/`REPO_ONBOARDING` 6 · `ENVIRONMENT`/`OPERATOR-INTERFACE` 5 · `AGENT_FRAMEWORK` 1 · `FUNNEL_LIFECYCLE` 0.

Three cautions the number alone would hide:

1. **`FUNNEL_LIFECYCLE.md`'s 0 is not orphanhood.** `scripts/funnel_lifecycle.py:344-360` scans the **folder**, not the file, and its docstring says so deliberately: *"Scans `protocols/*.md` only — the contract names `protocols/` as where FM-1 lands it, and widening the scan would let an arbitrary audit or draft arm a gate."* The file is load-bearing and invisible to a name-grep.
2. **`ESSENTIALS.md`'s 32 is mostly a superseded file's own gate wiring** — see the census below.
3. **`AGENT_FRAMEWORK.md`'s 1 is the row proposing its removal.** That is the only live consumer, and it is a consumer that wants the file gone.

---

## `ESSENTIALS.md` consumer census (feeds D9)

`status: superseded`; `CLAUDE.md:25` and `protocols/README.md:19` both route nobody to it. **32 live consumer files.** The census is what makes `[#628]`'s framing — *"a FLEET-COUPLED release act, not a doc lane"* — checkable rather than asserted:

**A. Gate/registry membership (the coupling — 4 sites).**
- `scripts/canonical_docs.py:101` `ESSENTIALS_PATH`; it is a member of **`FRESHNESS_FILES`** (resolved live: `('ARCHITECTURE.md', 'CLAUDE.md', 'CONTRIBUTING.md', 'docs/handoffs/README.md', 'protocols/ESSENTIALS.md')`) and of **`STRUCTURE_DOCS`**.
- `scripts/canonical_freshness_gate.py:52` — the **fallback** literal list, i.e. the value a consumer inherits when it cannot import `canonical_docs`.
- `scripts/audit.py:481` — `_FRESHNESS_FILES = DEFAULT_FRESHNESS_FILES + _HUB_ONLY_FRESHNESS_FILES`, so the audit freshness check reads it.
- `tests/test_audit.py:1218` asserts the membership; `tests/test_canonical_freshness_gate.py:195` asserts it is **not** in `PRESENCE_REQUIRED` (three consumers are recorded ABSENT at `canonical_freshness_gate.py:63-65` — `corp-monorepo`, `ai-council`, `win-tooling`).

**B. Released-manifest surface (the reason this is a release act — 6 sites).** `deploy/manifest-v1.1.0.yaml:416`, `v1.2.0:631`, `v1.3.0:696`, `v1.3.1:705`, `v1.4.0:871`, `v1.5.0:989` — each a `doc_shapes` entry with `spine: []` and **`freshness_gated: true`**. Five of the six are **released artifacts**; `canonical_docs.py:255-268` records the precedent that editing a shipped manifest's `doc_shapes` is answered by a **version bump, not a retro-edit**.

**C. Templates that still hand it to a consumer (4 live + 5 archived).** Live: `templates/claude-regions/first-read.md:4` (the hub region single-sourced into `CLAUDE.md` §1 — it already carries the SUPERSEDED wording), `templates/CLAUDE-md-template.md:19` (**still instructs a new consumer to read it**, with no superseded marker), `templates/handoff/02_METHODOLOGY.md.tmpl:12`. Archived: `templates/archive/{AGENTS-md-template,HANDOFF_TEMPLATE,HANDOFF_QUESTION_TEMPLATE,HANDOFF_FOLDER_TEMPLATE}.md` (the last with 7 sites, incl. the `04_ESSENTIALS.md` full-copy rule).

**D. Live doctrine pointers (5).** `CLAUDE.md:16`, `CLAUDE.md:25`, `README.md:65`, `protocols/README.md:19`, `protocols/ENVIRONMENT.md:206` — all five already say *superseded*, so the routing half of the dissolution has landed and the **wiring** half has not.

**E. Machine baselines / disposition (4).** `ecosystem/index.yaml:123` and `ecosystem/.dev-knowledge/history/2026-07-31.md:38,89` carry the standing `undeclared_edges` WARN *"protocols/ESSENTIALS.md -> handoff-process (tier 1)"*; `ecosystem/disposition-register.yaml:126-129` dispositions it, and the disposition's stated reason is the coupling itself — *"ESSENTIALS.md is canonical_freshness-gated."*

**F. Sibling protocol files (8).** Incl. `STANDING_RULINGS.md:2631/2647` (RULING-W evidence — **both locators stale**, below), `PLAYBOOK.md:1237/1267/351/784`, `HANDOFF_PROCESS.md:1179`, `AI_COUNCIL_PROCESS.md:423` (which itself records a cross-reference to a *"heading that no longer exists"*), and both `archive/` files.

**D9 bottom line, measured:** the file can be **routed around** — that is done — but it cannot be **removed** without touching a freshness registry, its fallback literal, two test assertions, a live consumer-facing template, and a `doc_shapes` block in six manifests of which five are released. `[#628]`'s "release act" framing is confirmed by measurement, not accepted on assertion.

---

## Duplicated doctrine across two files

Verbatim duplication is **near zero**: a normalized ≥70-character sentence scan across all 14 top-level files found **exactly one** shared sentence (`AI_COUNCIL_PROCESS.md` × `PLAYBOOK.md`, *"reversal cost 1 hour — backing out the decision means meaningful rework"*). Duplication in this folder is **doctrinal restatement**, not copy-paste, and it is mostly governed. Four clusters, each with the canonical home named:

1. **RULING-W (hub→consumer writes) — 3 sites, 1 canonical, and the pointer is correct.** `PLAYBOOK.md:1598` is canonical; `ESSENTIALS.md:90` is a one-line summary that *ends in a pointer* (`→ PLAYBOOK Ch8; ADR-36/41`); `STANDING_RULINGS.md` T-34 restates it as `[#356]` evidence. This is the healthy shape — **but both of T-34's locators are stale** (below).
2. **Session-close / definition-of-done — 4 sites, 1 canonical, and the restatements are pointer-shaped.** `DEFINITION_OF_DONE.md` is canon; `HANDOFF_BOOT.md:243-256` restates only *where the teeth sit* and says so in terms — *"The rest is not resident on purpose — ask CC to pull `protocols/DEFINITION_OF_DONE.md` rather than acting on a remembered shape."* `PLAYBOOK.md` (16 hits) and `ESSENTIALS.md` §"Ending a Session" also carry it. **No contradiction found**; all four agree the Stop hook is advisory since the ADR-85 amendment 2026-08-03 and that `/override` discharges nothing.
3. **The governance funnel — 4 sites, and the overlap is *declared* rather than discovered.** `FUNNEL_LIFECYCLE.md` §7 (*"Sources — what is restated, and what goes further"*) is a 15-row table marking every clause **restated**, **extended** or **new** against ADR-98/100/111/70 and `STANDING_RULINGS` H3. This is the best-governed duplication in the folder and is the pattern the other three clusters do not have. Token density elsewhere: `STANDING_RULINGS` 102, `PLAYBOOK` 27, `HANDOFF_PROCESS` 12.
4. **The handoff protocol — `HANDOFF_PROCESS.md` (91 hits) canonical, restated in `PLAYBOOK` (30), `STANDING_RULINGS` (16), `HANDOFF_BOOT` (6), `OPERATOR-INTERFACE` (4), `SESSION_SETUP` (3).** `SESSION_SETUP.md:222` states the discipline correctly — *"Not restated here so this file can't drift from it"* — **and then drifts anyway on the version number.** This is the one cluster where restatement has produced a live contradiction; it is the H13 finding, below.

**Doctrine anchors present in only one file** (so: no duplication risk, but also no redundancy if that file is wrong): *output-formatting / code-fence* — `PLAYBOOK` only (5); *worktree provisioning* — `PLAYBOOK` (17) + one `ESSENTIALS` line; *library-first* — `PLAYBOOK` (2) + `STANDING_RULINGS` (6), and **absent from `ESSENTIALS`** despite `CLAUDE.md` §4 carrying it as an always-on rule.

---

## Proposals

### RELOCATE (1)

**`protocols/AGENT_FRAMEWORK.md` → `docs/`.**
*Witness:* zero references in `scripts/`, `tests/`, `.claude/`, `templates/`, `deploy/`; the sole live consumer is `tasks/227-relocate-agent-framework-md-out-of-protocols.md`, an **open** row (`[#227]`, P3/S, currently `DEFER` from the 2026-08-27 45-day icebox sweep) whose Done-when is *"AGENT_FRAMEWORK.md lives under `docs/` and every inbound ref resolves to the new path."* The file self-describes as *"v0.1 stub, NOT implemented"* (`:10`).
*Inbound refs that would need repointing:* `protocols/README.md:21` (the roster line) and `tasks/227-…md`'s own `refs` clause. Both are named in the row already.
*Caveat the operator should weigh:* `protocols/README.md`'s casing rule (ADR-34, `Protocols → UPPERCASE_WITH_UNDERSCORES.md`) is folder-scoped, so a move to `docs/` implies a rename to kebab-case under the §4 convention. The row does not say this. **Reported, not decided.**

### KEEP (15)

All 13 remaining top-level files and both `archive/` files. Each row's witness is in the Inventory table. Four KEEPs carry a caveat worth the operator's eye:

- **`ESSENTIALS.md` — KEEP, and specifically *not* RETIRE.** Its `status:` is `superseded` and nothing boots from it, which makes RETIRE the tempting verdict; the census above shows why that verdict would be wrong from this lane. The act is owned by `[#628]` and is fleet-coupled.
- **`ENVIRONMENT.md` — KEEP, but it is the folder's only file with *no frontmatter at all*.** `last_reviewed` therefore cannot be parsed by any gate, and the file is in neither `FRESHNESS_FILES` nor `_HUB_ONLY_FRESHNESS_FILES`. `[#285]` (scope-widened 2026-09-05) owns the fix and forbids the shortcut: *"a bare stamp to green a gate is forbidden."* Note the file's own header records a **2026-09-06 end-to-end re-read** — so the re-read `[#285]` requires appears to have happened while the frontmatter it was to enable did not land. **Reported; verifying that reading is beyond this lane's read-only scope.**
- **`PLAYBOOK.md` — KEEP, same gap.** `reconciled_with` but no `last_reviewed`; 490,615 B and the second-most-consumed file in the folder, gated for structure but not for freshness. Also `[#285]`.
- **`archive/HANDOFF_PROCESS_v4.4.md` — KEEP, and note it is not inert.** `.claude/commands/handoff.md:213` treats it as the live frozen spec for the v4 flow. Any future "archive is history" sweep should not assume otherwise.

### ARCHIVE (0) · RETIRE (0)

**None proposed, and the zero is measured rather than default.** Both `archive/` residents are already at their retention home and both have live citers; `ESSENTIALS.md` is the only retire-shaped candidate and is blocked by the coupling above. No file in this folder is uncited.

### Reported, not fixed (3 defects)

**R1 · `STANDING_RULINGS.md` T-34 cites two locators that no longer resolve.** Lines `2631` and `2647` both give RULING-W's live prose as **`protocols/ESSENTIALS.md:86`** and **`protocols/PLAYBOOK.md:1388`**. Re-opened this lane: `ESSENTIALS.md:86` is a **blank line** (the RULING-W bullet is at **`:90`**), and `PLAYBOOK.md:1388` is a paragraph about `Decommission:` fields and orphan accumulation — RULING-W's canonical site is **`PLAYBOOK.md:1598`**, 210 lines away. T-34 is the **Evidence** block of a row recorded `CLOSED` (`tasks/356-…md` carries `status: closed`, consistent), so the closure rests on two locators a reader cannot resolve. Severity: the ruling itself is intact and findable; only its citations rot.

**R2 · The H13 stale-version class is live, has grown its gap, and `STANDING_RULINGS` records that nothing owns it.** `STANDING_RULINGS.md:2976-2977` names *"an 11-site `HANDOFF_PROCESS v5` cluster in a file whose frontmatter declares `reconciled_with: handoff-process@6.2.0`"* and states: *"If the census is to be executed it needs a new row, and this entry is the record that no open row currently owns it."* Re-measured tonight against live `Version: 7.0.0`:

- `PLAYBOOK.md` — **3 instruction-shaped stale sites**: `:1246` (bundle row, *"per HANDOFF_PROCESS v5.4"*), `:4050` and `:4142` (both `/handoff` roster rows, *"per HANDOFF_PROCESS v5"*). A 4th hit at `:5547` is a dated 2026-06-23 reconciliation note and is **history, not drift** — not counted.
- `SESSION_SETUP.md` — **4 instruction-shaped stale sites**: `:142`, `:208` (*"the HANDOFF_PROCESS v6 Claude-Code protocol"*), `:210` (*"follow HANDOFF_PROCESS **v6.3.0**"*) and `:222` (*"Mechanics live in `protocols/HANDOFF_PROCESS.md` (v6.3.0 — the single source of truth)"*).
- `OPERATOR-INTERFACE.md:203` reads *"Through HANDOFF_PROCESS v6.2.0 the assembler inlined…"* — **historical by construction; not counted as drift.**

So the class is **7 live sites across 2 files**, down from H13's 11 but no longer confined to one file, and **both files now declare `reconciled_with: handoff-process@7.0.0`** — the frontmatter advanced while the bodies did not, widening the gap H13 named. **Why no gate catches it:** `scripts/validate_reconciliation.py` compares the frontmatter **token** to the spec's live `Version:` and nothing else (both files therefore PASS as `match`), and `scripts/audit_checks/check_handoff_version_stamp.py` scans `_STAMP_FILES = ["ARCHITECTURE.md", "CONTRIBUTING.md"]` — **no `protocols/` file is in its scope**. The semantic half is the `check-against-spec` skill, which `validate_reconciliation`'s docstring states is *"DELIBERATELY NOT the trigger"* for the ship gate. This is a structural blind spot, not an oversight, and it is exactly what H13 predicted.

**R3 · `protocols/README.md:9` cites a backlog id that resolves to nothing.** Its scope marker reads *"**Scope marker (BACKLOG #314 / #327).**"* — `[#327]` is live (`tasks/327-protocols-as-interface-genre-ruling.md`), but `[#314]` appears in **neither `tasks/`, nor `tasks/archive/` (25 rows), nor `BACKLOG.md`**. It has 11 `JOURNAL.md` mentions, so it existed; it is not a live row today. The same id anchors the file's closing line (*"Seed shell (BACKLOG #314 partial)"*), so the folder's own charter rests on a dangling id.

### Fragility noted, no defect (1)

**`funnel_lifecycle.ready_threshold` binds to a filename sort, not to a file.** It globs `sorted(protocols/*.md)` and returns the **first** regex match; today that is `FUNNEL_LIFECYCLE.md:322` (N=30). Any future `protocols/*.md` sorting earlier — `AGENT_FRAMEWORK`, `AI_COUNCIL_PROCESS`, `DEFINITION_OF_DONE`, `ENVIRONMENT`, `ESSENTIALS` all do — that happens to carry a line matching `READY threshold: <n> days` would silently re-arm the gate with a different number. The module's docstring defends the *folder* scope deliberately; it does not defend the *first-match* rule. Not a defect today; a trap tomorrow. **No row proposed** — that is the operator's call.

---

## Counts before → proposed after

```
protocols/ top level        14 files  →  13 files   (−1: AGENT_FRAMEWORK.md relocates to docs/)
protocols/archive/           2 files  →   2 files   (unchanged; both already at retention home)
folder total                16 files  →  15 files
folder bytes             1,165,796 B  →  1,162,049 B   (−3,747 B, −0.32 %)

verdicts:  KEEP 15  ·  RELOCATE 1  ·  ARCHIVE 0  ·  RETIRE 0  ·  UNDETERMINED 0
defects reported, not fixed: 3   ·   fragilities noted: 1   ·   files edited by this lane: 0
```

No count above is a closure. Every one is a proposal awaiting an operator ruling.

---

## Honest limits

**What I could not establish.**

1. **Last-content-commit is unavailable for 6 of 16 files.** The clone is shallow (`.git/shallow`, 17 grafts; 278 reachable commits back to 2026-09-01). `bcf21b1` is a **graft boundary** — it reports *2,938 files changed, 629,480 insertions* and shows `ESSENTIALS.md` as `new file mode`, which is an artifact of the graft, not a creation. So for `ESSENTIALS.md`, `AI_COUNCIL_PROCESS.md`, `DEFINITION_OF_DONE.md`, `SESSION_SETUP.md` and both `archive/` files, **I cannot date the last real content change.** Their verdicts rest on consumer and generator witnesses only. Separately, the 10 files I *can* date are all dated within six days — because two corpus-wide sweeps (`c87d54b` re-stamp, `948911c`) touched them — so **recency here does not evidence review**, and I have not used it as one.
2. **No repo gate, validator or test was executed.** `uv run --locked` refuses: `required-version = "==0.11.19"`, container has `0.8.17`. Where a gate's behaviour is claimed above I read the module; the one live measurement I made — `ready_threshold` → `FUNNEL_LIFECYCLE.md:322`, N=30 — was produced by **re-implementing `_READY_THRESHOLD_RE` by hand** against the tree, not by calling the function (`scripts/funnel_lifecycle.py` cannot import: `ModuleNotFoundError: click`). It agrees with the value `JOURNAL.md:6971` records, which is corroboration, not proof.
3. **The authority file was never read.** The brief names `to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md` (5,422 B) as operator's word and instructs *"Read that file yourself."* **It is not reachable from this container** — no `to-cc/` exists in the repo or on disk, and it lives on the operator's Drive transport. This lane therefore executed the **working copy** in the brief. If the frozen contract disagrees with it, **the frozen contract wins and this census was produced without seeing it.**
4. **Consumer counting is `grep`, with `grep`'s limits.** A reference by section title, by concept, or through a variable is invisible to it — `FUNNEL_LIFECYCLE.md`'s live consumer is precisely such a case and I found it only by reading `funnel_lifecycle.py`. **There may be more positional consumers I did not find**, in this folder or pointed at it. The live/historical bucketing is a judgement borrowed from `consumer_at_landing.py`; a different bucketing yields different numbers and I have shown the raw counts so the judgement is inspectable.
5. **"Duplicated doctrine" was measured two ways, and both are incomplete.** A ≥70-char normalized-sentence scan (finds copy-paste; found 1) and a 17-anchor regex cross-tab (finds topic co-presence; found the four clusters). **Neither detects a rule restated in genuinely different words** — the case most likely to hide a contradiction. The four clusters I report were then read by hand; clusters I did not think to probe were not.
6. **R2's site classification is a judgement call.** I split 8 pre-v7 mentions into 7 "instruction-shaped" and 2 "historical" by reading each line's grammar (`OPERATOR-INTERFACE.md:203`'s *"Through … v6.2.0"* and `PLAYBOOK.md:5547`'s dated note are the two I excluded). A reader could count 8 or 9. The **direction** is not in doubt; the exact integer is a reading.
7. **`ENVIRONMENT.md`'s re-read status is unresolved.** Its header claims a 2026-09-06 end-to-end re-read; `[#285]` requires a re-read *then* a stamp. Whether that re-read satisfies the row is a judgement about work I did not witness, and I did not make it.
8. **I did not verify `[#227]`'s premise that "no living doc references it."** `protocols/README.md:21` **does** reference `AGENT_FRAMEWORK.md`, and `protocols/README.md` is a living doc. The row's Done-when accounts for inbound refs, so this may be wording rather than error — but the premise as stated is not accurate today, and I am flagging it rather than resolving it.

**Tooling actually used.**

- **Gemini fan-out: `NONE`.** `command -v gemini` → not on PATH. **Gemini-read files: 0. Gemini-returned locators: 0. Fabrications: 0** — and that zero means *no locators were offered*, not *the offered locators were clean*. Absence is being reported as absence.
- **Copilot Enterprise offload: NOT AVAILABLE** — gated on `#75`, not ratified. Recorded here so no later reading can claim it was used.
- Every locator in this file was opened by me in this session before being cited. Where one did not resolve, that is the finding (R1, R3), not a silent correction.
