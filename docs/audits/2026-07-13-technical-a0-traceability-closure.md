# A0 traceability closure table — the mechanism guaranteeing nothing the operator dictated was lost

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-13
- **Evidence heads:** `.dev-knowledge` `97cf58e0` · `ai-council` `68fc30c` · `corp-monorepo` `0bc74fd`
- **Status:** COMPLETE TRACEABILITY CENSUS — implementation deferrals remain only where named below
- **Sources:** intake #11 · fleet-parity register · 30-row content-parity inventory

## UNRESOLVED

None.

## Scope and method

Read-only inspection covered source files, repository history since 2026-07-12, the 2026-07-12/13 JOURNAL entries in all three repositories, all three `.methodology.yaml` states, and the live hub BACKLOG.

Source abbreviations:

- **I11:** `.dev-knowledge/docs/intake/2026-07-11-tech-fleet-divergence-register.md`
- **FPR:** `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md`
- **CP:** `.dev-knowledge/docs/audits/2026-07-13-technical-content-parity-inventory.md`
- **HBL:** `.dev-knowledge/BACKLOG.md`

For FPR, the census boundary is its declared “master table — one row per divergence” at lines 12–36: 19 rows. `SUPERSEDED` is a single traceability edge to a later source row or operator ruling; the successor is mapped exactly once in its own table.

Current declaration state was checked directly: the hub has no `.methodology.yaml` at `97cf58e0`; corp declares `ruff-gate`, `hub-codemap-hooks`, `hub-toc-hooks`, `audit-casing-r4`, and `github-ci-local` (`corp-monorepo/.methodology.yaml:4-87`); ai declares `ruff-gate`, `hub-codemap-hooks`, both hub-hermetization exclusions, and `claude-md-section-11-title` (`ai-council/.methodology.yaml:4-70`).

Adjacent control tickets were also read so they could not become implicit substitutes for census rows: #314 (`HBL:159`), #315 (`HBL:188`), #325 (`HBL:98`), #327 (`HBL:171`), #328 (`HBL:172`), #331 (`HBL:174`), #332 dependency-version parity (`HBL:175`), #333 Codex doc-lane (`HBL:205`), and #334 coordinated ruff-id migration (`HBL:176`).

## Census

|Source|Expected|Mapped|Unresolved|
|---|---:|---:|---:|
|Intake #11 actual numbered items|23|23|0|
|Fleet-parity master-register rows|19|19|0|
|Content-parity inventory rows|30|30|0|
|**Grand total**|**72**|**72**|**0**|

**Content-parity verification: 30/30.**

## Source 1 — intake #11

|ID|Source row|Disposition|Named target|Evidence|
|---|---|---|---|---|
|I11-01|`.mypy_cache` (`I11:18`)|SUPERSEDED|FPR-e6 cache-parity row|FPR records all three cache classes ignored and at parity (`FPR:31`, `FPR:115-123`); operator accepted all register verdicts (`.dev-knowledge/JOURNAL.md:234`).|
|I11-02|`.pytest_cache` (`I11:19`)|SUPERSEDED|FPR-e6 cache-parity row|`FPR:31`, `FPR:115`; accepted-register ruling at `.dev-knowledge/JOURNAL.md:234`.|
|I11-03|`.ruff_cache` (`I11:20`)|SUPERSEDED|FPR-e6 cache-parity row|`FPR:31`, `FPR:116`; accepted-register ruling at `.dev-knowledge/JOURNAL.md:234`.|
|I11-04|`.hypothesis` (`I11:21`)|SUPERSEDED|FPR-e2|The successor isolates the real remaining gap to missing hub/ai ignore lines (`FPR:27`, `FPR:118`, `FPR:127`).|
|I11-05|`.venv` (`I11:22`)|SUPERSEDED|FPR §5 `.venv` at-parity ruling|All three states are recorded at parity (`FPR:119`); the ruling was accepted at `.dev-knowledge/JOURNAL.md:234`.|
|I11-06|ai-council `.env` (`I11:23`)|SUPERSEDED|Intake #12 Tier-3/Tier-4 ownership rows|The later ownership source records `.env` as ai-local, verified CWD fallback, and ignored ephemera (`docs/intake/2026-07-11-tech-ownership-manifest.md:41-45`); ai’s ignore rule is `.gitignore:26`.|
|I11-07|`.vscode/settings` (`I11:24`)|SUPERSEDED|FPR-e1|The successor turns the open question into the carry-or-local ruling (`FPR:26`, `FPR:120`, `FPR:125`); its execution is mapped under FPR-e1.|
|I11-08|`.github` (`I11:25`)|SUPERSEDED|FPR-e3|The successor corrects the premise: corp, not hub, carries the two workflows (`FPR:28`, `FPR:121`, `FPR:129`).|
|I11-09|ai-council `assets/` (`I11:26`)|SUPERSEDED|FPR-e4|The successor verifies the tracked ruff asset and requires a declaration (`FPR:29`, `FPR:122`, `FPR:131`).|
|I11-10|ARCHITECTURE ToC + Mermaid (`I11:32`)|SUPERSEDED|Operator #326 CC-facing ruling|The ruling is live at `HBL:170`; FPR split it into a1/a2 (`FPR:18-19`). Both execution rows are mapped below.|
|I11-11|`INSTALL.md` (`I11:33`)|SUPERSEDED|CP-C8|The later row verifies byte-parity but isolates durable carrier ownership (`CP:237-245`); CP-C8 maps to #315 below.|
|I11-12|`protocols/` (`I11:34`)|SUPERSEDED|CP-F3|The later row defines the fleet genre and exact remaining file set (`CP:368-376`); CP-F3 maps its execution below.|
|I11-13|Audit filename convention (`I11:35`)|SUPERSEDED|FPR-d1|The successor records lowercase ADR-101 R4 as the winning prospective convention (`FPR:25`, `FPR:95-107`).|
|I11-14|BACKLOG schema (`I11:36`)|SUPERSEDED|CP-D1|The later exhaustive row specifies E/S/task migration plus validator teeth (`CP:249-257`).|
|I11-15|CLAUDE archived references (`I11:37`)|SUPERSEDED|Operator #330 ruling|The rule and exact hub sweep are recorded in `.dev-knowledge/JOURNAL.md:106-116`; substantive SHAs `6a417b4` and `144050a`.|
|I11-16|`code-review` versus `codex-review` (`I11:43`)|SUPERSEDED|FPR-c2 keep-both ruling|FPR distinguishes built-in Claude review from the custom Codex path (`FPR:23`, `FPR:82-89`); operator accepted the verdict at `.dev-knowledge/JOURNAL.md:234`.|
|I11-17|`/evolve` (`I11:44`)|SUPERSEDED|FPR-c3 archived-correct ruling|FPR verifies fleet-wide absence as correct parity (`FPR:24`, `FPR:85`, `FPR:91`); accepted at `.dev-knowledge/JOURNAL.md:234`.|
|I11-18|`/save` (`I11:45`)|SUPERSEDED|FPR-c1|FPR isolates the hub-only command (`FPR:22`, `FPR:78`, `FPR:87`); the successor maps to live #325 below.|
|I11-19|`/handoff` absent in consumers (`I11:46`)|SUPERSEDED|Accepted ADR-36/42 centralized-handoff ruling|FPR marks the absence correct (`FPR:79`); current consumer contracts point to hub handoffs and prohibit local copies (`ai-council/CONTRIBUTING.md:139-145`; `corp-monorepo/CONTRIBUTING.md:140-148`).|
|I11-20|hub `runbox/` (`I11:52`)|SUPERSEDED|FPR-f2 premise-void ruling|No disk or Git-history object existed (`FPR:33`, `FPR:141`); NO-ACTION accepted at `.dev-knowledge/JOURNAL.md:234`.|
|I11-21|hub `temp/` (`I11:53`)|SUPERSEDED|FPR-f1|The successor verified it empty/untracked and recorded the deletion candidate (`FPR:32`, `FPR:139`); execution is mapped under FPR-f1.|
|I11-22|Machine-readable ownership/parity mechanism (`I11:59`)|DEFERRED+ticket|[#328], owner: hub architecture/audit tooling|The live ticket requires the manifest, WARN check, hub `.methodology.yaml`, declared/undeclared tests, and advisory review-date behavior (`HBL:172`).|
|I11-23|Root-archive prohibition (`I11:60`)|DONE|hub `6a417b49` + `144050ac`, merged `35e5d580`|The rule and sweep are execution-recorded at `.dev-knowledge/JOURNAL.md:92-116`; #330 was then removed under done-items-leave (`JOURNAL.md:94-102`).|

## Source 2 — fleet-parity master register

|ID|Source row|Disposition|Named target|Evidence|
|---|---|---|---|---|
|FPR-a1|ARCHITECTURE Mermaid (`FPR:18`)|DONE|corp `df29a3c`|The corp execution stripped ToC and Mermaid and converted the codemap to text; Git history names `df29a3c docs(architecture): strip ToC + Mermaid, codemap→text [#326]`. Hub/ai were already Mermaid-free.|
|FPR-a2|ARCHITECTURE ToC (`FPR:19`)|DONE|hub `f7a548d2`; corp `df29a3c`; ai `30e4dce` verified no-op|The #326 hub leg is recorded at `.dev-knowledge/JOURNAL.md:206`; ai’s no-op is recorded at `ai-council/JOURNAL.md:66-72`; current ARCHITECTURE files contain no ToC markers.|
|FPR-b1|BACKLOG epic-id scheme (`FPR:20`)|DONE|ai `d420399`; corp `8371c08`|The consumer execution records E-spine/E-S adoption at `ai-council/JOURNAL.md:36-42` and `corp-monorepo/JOURNAL.md:25-30`.|
|FPR-b2|BACKLOG schema gate (`FPR:21`)|DONE|ai `649b484`; corp `8371c08`|Both consumers wired `validate-backlog`; ai evidence is `JOURNAL.md:38-42`, corp evidence `JOURNAL.md:26-30`.|
|FPR-c1|`/save` (`FPR:22`)|DEFERRED+ticket|[#325], owner: hub carrier maintainer|The live ticket requires a manifest command-artifact carrier and witnessed consumer presence while keeping `/handoff` hub-only (`HBL:98`).|
|FPR-c2|Review-command coexistence (`FPR:23`)|SUPERSEDED|Operator ACCEPT ruling: keep both distinct reviewer paths|The register’s distinct-purpose finding is at `FPR:82-89`; all verdicts were accepted at `.dev-knowledge/JOURNAL.md:234`. CP independently confirms the shared command baseline (`CP:27-30`).|
|FPR-c3|`/evolve` absence (`FPR:24`)|SUPERSEDED|Operator ACCEPT ruling: archived-correct parity|`FPR:85`, `FPR:91`, and `.dev-knowledge/JOURNAL.md:234`.|
|FPR-d1|Audit filename casing (`FPR:25`)|DONE|corp `5221e92`, merged `3a2547c`|Corp deployed the prospective lowercase gate; current declaration precisely names `audit-casing-r4` and its boundary (`corp-monorepo/.methodology.yaml:48-78`).|
|FPR-e1|`.vscode/` (`FPR:26`)|DONE|ai `2707d73`; corp `d9c1f56`|The operator chose carry-to-consumers. Ai’s execution and witnessed state are at `ai-council/JOURNAL.md:46-52`; corp’s commit is `d9c1f56 chore(vscode): adopt hub files.watcherExclude`.|
|FPR-e2|`.hypothesis/` ignore parity (`FPR:27`)|DEFERRED+ticket|[#328], owners: hub + ai consumer maintainer|The two missing ignore declarations remain captured as a parity surface (`FPR:118`, `FPR:127`); #328 owns undeclared-surface WARN behavior and declarations (`HBL:172`). Corp is already ignored at `corp-monorepo/.gitignore:46`.|
|FPR-e3|corp `.github/` (`FPR:28`)|DECLARED|corp `.methodology.yaml` component `github-ci-local`|Exact declaration and two workflow names: `corp-monorepo/.methodology.yaml:79-87`; executing commit `7a56127`, merged `c5550a7`.|
|FPR-e4|ai-council `assets/` (`FPR:29`)|DEFERRED+ticket|[#328], owner: ai-council methodology maintainer|The verified local asset remains absent from ai’s current declaration list (`ai-council/.methodology.yaml:4-70`); #328 is the live declaration/check mechanism (`HBL:172`).|
|FPR-e5|hub `node_modules/` (`FPR:30`)|SUPERSEDED|Operator ACCEPT ruling: ignored hub-tooling parity|The accepted AT-PARITY finding is `FPR:30`, `FPR:123`, and `.dev-knowledge/JOURNAL.md:234`.|
|FPR-e6|Caches (`FPR:31`)|SUPERSEDED|Operator ACCEPT ruling: ignore parity, not folder parity|Evidence matrix `FPR:115-119`; accepted at `.dev-knowledge/JOURNAL.md:234`.|
|FPR-f1|hub `temp/` (`FPR:32`)|DONE|non-Git local execution anchored by hub record `5d9b20c`, closure merge `c82857bd`|The immutable amendment records empty/untracked verification and deletion (`FPR:206-210`); the same execution is recorded at `.dev-knowledge/JOURNAL.md:162-168`.|
|FPR-f2|hub `runbox/` (`FPR:33`)|SUPERSEDED|Operator ACCEPT ruling: NO-ACTION, premise void|The absence and empty history are recorded at `FPR:141`; accepted at `.dev-knowledge/JOURNAL.md:234`.|
|FPR-g1|corp handoff-process v4 reference (`FPR:34`)|DONE|corp `20daab9`|The content-parity doc-review commit corrected the v5 handoff pointer; execution ledger `corp-monorepo/JOURNAL.md:25-30`; current contract at `corp-monorepo/CONTRIBUTING.md:140-144`.|
|FPR-g2|hub `/boot` in live session-start protocol (`FPR:35`)|DONE|hub `144050ac`, merged `35e5d580`|Exact removal and archive-prohibition sweep at `.dev-knowledge/JOURNAL.md:106-116`; formal #330 closure at `JOURNAL.md:92-102`.|
|FPR-M|Hub `.methodology.yaml` absence (`FPR:36`)|DEFERRED+ticket|[#328], owner: hub architecture/audit tooling|The file remains absent from hub tree at `97cf58e0`; #328 explicitly requires the hub to carry its own `.methodology.yaml` (`HBL:172`).|

## Source 3 — content-parity inventory

|ID|Source row|Disposition|Named target|Evidence|
|---|---|---|---|---|
|CP-A1|`first-read` (`CP:33-40`)|DONE|hub `af4a1ad2`; ai `b46e6ce`; corp `fa8a4e3`|Hub made the canonical body consumer-safe (`.dev-knowledge/JOURNAL.md:36-42`); both consumer adoptions are recorded at `ai-council/JOURNAL.md:36-42` and `corp-monorepo/JOURNAL.md:25-30`.|
|CP-A2|`conventions-commit-branch` (`CP:43-50`)|DONE|hub `af4a1ad2`; ai `b46e6ce`; corp `fa8a4e3`|The exact branch-prefix/type/`--no-ff` contract is recorded at `.dev-knowledge/JOURNAL.md:38-40`; current consumer forms are `ai-council/CONTRIBUTING.md:17-30` and `corp-monorepo/CONTRIBUTING.md:15-28`.|
|CP-A3|`conventions-output-formatting` (`CP:53-60`)|DONE|hub template `c46e1837`; ai `b46e6ce`; corp `fa8a4e3`|Eight canonical region extracts and both consumer materializations are recorded at `.dev-knowledge/JOURNAL.md:50-60`, `ai-council/JOURNAL.md:38-42`, and `corp-monorepo/JOURNAL.md:26-30`.|
|CP-A4|`critical-rules-records` (`CP:63-70`)|DONE|hub `c46e1837`; ai `b46e6ce`; corp `fa8a4e3`|Same eight-region execution ledger: `.dev-knowledge/JOURNAL.md:50-60`; consumer ledgers above.|
|CP-A5|`critical-rules-consistency` (`CP:73-80`)|DONE|hub `c46e1837`; ai `b46e6ce`; corp `fa8a4e3`|Canonical extract plus both consumer inserts; `.dev-knowledge/JOURNAL.md:52-54`.|
|CP-A6|`critical-rules-no-leftovers` (`CP:83-90`)|DONE|hub `af4a1ad2`; ai `b46e6ce`; corp `fa8a4e3`|Hub removed hub-specific incident wording before consumer adoption (`.dev-knowledge/JOURNAL.md:38-40`).|
|CP-A7|`session-start-protocol` (`CP:93-100`)|DONE|hub `c46e1837`; ai `b46e6ce`; corp `fa8a4e3`|Canonical extraction and consumer byte-match evidence: `.dev-knowledge/JOURNAL.md:52-54`; `ai-council/JOURNAL.md:38-40`; `corp-monorepo/JOURNAL.md:26-28`.|
|CP-A8|`antipatterns-universal` (`CP:103-110`)|DONE|hub `c46e1837`; ai `b46e6ce`; corp `fa8a4e3`|Same eight-region execution chain and consumer ledger citations.|
|CP-B1|Shell metadata, marker coverage, section naming (`CP:115-122`)|DONE|hub `ba4508eb`; ai `b46e6ce` + `d96ef6d`; corp `fa8a4e3`|The 15-region shell template landed in hub (`.dev-knowledge/JOURNAL.md:52-56`); ai’s truthful §11-title residual is exactly declared as `claude-md-section-11-title` (`ai-council/.methodology.yaml:59-70`).|
|CP-B2|Project-local prose outside owner regions (`CP:125-132`)|DONE|ai `b46e6ce`; corp `fa8a4e3`|Both consumer ledgers state local prose was retained in adjacent `owner=repo` blocks (`ai-council/JOURNAL.md:38`; `corp-monorepo/JOURNAL.md:26`).|
|CP-B3|Commands-available roster form (`CP:135-142`)|DONE|ai `b46e6ce`; corp `fa8a4e3`|The consumer CLAUDE shell/roster fixes are recorded at `ai-council/JOURNAL.md:38-42` and `corp-monorepo/JOURNAL.md:26-30`; `/save` distribution remains separately mapped to #325.|
|CP-B4|Skills versus rules taxonomy (`CP:145-152`)|DONE|ai `b46e6ce`; corp `fa8a4e3`|Ai explicitly relabelled `.claude/rules/` as rules (`ai-council/JOURNAL.md:38`); corp materialized the same shell with local organs preserved (`corp-monorepo/JOURNAL.md:26-29`).|
|CP-B5|Hooks-active roster currency (`CP:155-162`)|DONE|hub `247a4ba0`; ai `b46e6ce`; corp `fa8a4e3`|Hub added the missing `arm_hooks.py` claim (`.dev-knowledge/JOURNAL.md:52-54`); both consumers set-matched local rosters (`ai-council/JOURNAL.md:38`; `corp-monorepo/JOURNAL.md:26-28`).|
|CP-C1|LESSONS preamble/schema (`CP:167-174`)|DONE|hub template `ba4508eb`; ai `db24af6`; corp `2a67020`|Existing entries were preserved; consumer preamble adoptions are recorded at `ai-council/JOURNAL.md:38-42` and `corp-monorepo/JOURNAL.md:26-30`.|
|CP-C2|JOURNAL header/preamble (`CP:177-184`)|DONE|hub `247a4ba0` + `ba4508eb`; ai `db24af6`; corp `2a67020`|Hub corrected the ordering label and templated the preamble (`.dev-knowledge/JOURNAL.md:52-54`); current consumer preambles are `ai-council/JOURNAL.md:1-18` and `corp-monorepo/JOURNAL.md:1-14`.|
|CP-C3|CONTRIBUTING shell/audience (`CP:187-194`)|DONE|hub template `ba4508eb`; ai `0887391`; corp `8bab043`|Consumer adoption recorded at `ai-council/JOURNAL.md:38-42` and `corp-monorepo/JOURNAL.md:26-30`.|
|CP-C4|CONTRIBUTING branch/commit contract (`CP:197-204`)|DONE|hub `af4a1ad2`; ai `0887391`; corp `8bab043`|Canonical wording is recorded at `.dev-knowledge/JOURNAL.md:38-40`; current consumer lines: `ai-council/CONTRIBUTING.md:17-30`, `corp-monorepo/CONTRIBUTING.md:15-28`.|
|CP-C5|Backlog-id and closure semantics (`CP:207-214`)|DONE|hub template `ba4508eb`; ai `0887391`; corp `8bab043`|Current shared closure grammar and qualified references appear at `ai-council/CONTRIBUTING.md:54-78` and `corp-monorepo/CONTRIBUTING.md:53-77`.|
|CP-C6|Gates, validators, local operations (`CP:217-224`)|DONE|hub `247a4ba0`; ai `0887391` + `7239476`; corp `8bab043` + `20daab9` + `285b400`|Hub set-matched its live 15-hook roster (`.dev-knowledge/JOURNAL.md:52-54`); current consumer rosters are `ai-council/CONTRIBUTING.md:103-123` and `corp-monorepo/CONTRIBUTING.md:102-119`.|
|CP-C7|ADR and definition-of-done pointers (`CP:227-234`)|DONE|hub template `ba4508eb`; ai `0887391`; corp `8bab043`|Current consumer pointer-level forms are `ai-council/CONTRIBUTING.md:125-155` and `corp-monorepo/CONTRIBUTING.md:123-157`.|
|CP-C8|INSTALL ownership/carrier (`CP:237-244`)|DEFERRED+ticket|[#315], owner: hub deploy/carrier maintainer|The canonical source and both exact consumer copies already exist, but the live ticket still requires the manifest doc-artifact carrier (`HBL:188`).|
|CP-D1|E/S/task story-map hierarchy (`CP:249-256`)|DONE|ai `d420399` + `649b484`; corp `8371c08`|Ai adopted the E spine and validator; corp adopted E/S plus validator. Execution ledgers: `ai-council/JOURNAL.md:38-42`; `corp-monorepo/JOURNAL.md:26-30`.|
|CP-D2|Unqualified `[#id]` collision surface (`CP:259-266`)|DONE|hub `247a4ba0`; ai `0887391`; corp `8bab043`|The operator chose repo-qualified references. Current exact rule: `.dev-knowledge/CONTRIBUTING.md:61`, `ai-council/CONTRIBUTING.md:66`, `corp-monorepo/CONTRIBUTING.md:65`. Automated checking remains within #328, but the required choice is executed.|
|CP-E1|Unique `.claude` subtrees (`CP:306-313`)|DEFERRED+ticket|[#328], owners: hub manifest owner + each consumer maintainer|The source explicitly routes declarations through #328; the live ticket owns root/organ ownership and undeclared-surface WARN behavior (`HBL:172`).|
|CP-E2|`settings.json` baseline versus local hooks (`CP:316-323`)|DEFERRED+ticket|[#328], owners: hub carrier owner + each consumer maintainer|Current `.methodology.yaml` files do not yet enumerate each repo-owned hook block; #328 is the live manifest/declaration mechanism (`HBL:172`).|
|CP-E3|ai tracked `settings.local.json` (`CP:326-333`)|DONE|ai `8361660`, merged `f8f9e58`|Ai untracked the file while retaining it ignored on disk; execution record `ai-council/JOURNAL.md:38-42`.|
|CP-E4|Worktrees and scheduled-task runtime state (`CP:336-343`)|DEFERRED+ticket|[#328], owner: hub manifest owner; corp cleanup already executed|Corp removed the empty `cm-deep-vault` orphan during `872be4b` (`corp-monorepo/JOURNAL.md:26-28`); the remaining runtime-ephemera ownership declaration belongs to #328 (`HBL:172`).|
|CP-F1|`.claude` ignore/tracking policy (`CP:348-355`)|DONE|ai `8361660`; corp `872be4b`|Both consumer ledgers record adoption of tracked-by-default with named local/runtime exclusions (`ai-council/JOURNAL.md:38-42`; `corp-monorepo/JOURNAL.md:26-30`).|
|CP-F2|Project-specific ignore payloads (`CP:358-365`)|DEFERRED+ticket|[#328], owners: each repo maintainer through hub manifest|Project payloads were retained, but their explicit LOCAL ownership awaits the #328 declaration surface (`HBL:172`).|
|CP-F3|`protocols/` genre and ownership split (`CP:368-375`)|DONE|hub `6772ca8a`; corp `6ddc5f2`; ai already conformant|Hub seeded the canonical genre shell (`.dev-knowledge/JOURNAL.md:52-56`); corp added `protocols/README.md` plus `CORP_INTERFACE.md` (`corp-monorepo/JOURNAL.md:26-30`); ai’s existing README/domain split was verified conformant (`ai-council/JOURNAL.md:38`).|

## Supplemental carried-open and stalled state

These four rows are outside the 72-row source census.

|ID|State|Disposition|Live ticket and next-step owner|Evidence|
|---|---|---|---|---|
|SUP-01|hub `automation/fleet-audit` data branch|DEFERRED+ticket|[#254] — owner: hub operations/architecture maintainer; push the current 16-commit delta, reconcile the stale progress text, then close the ticket without merging the data branch to `main`|Local tip `be95b39e`; remote tip `d74d88cf`; branch is 16 commits ahead. The organ is already named at `ARCHITECTURE.md:181`; live ticket at `HBL:211`.|
|SUP-02|hub `docs/file-arch-cc-facing-ruling` branch|DEFERRED+ticket|[#326] — owner: hub repository maintainer; verify the fulfilled fleet-wide Done-when, close #326, then delete the fully merged branch|Branch tip `24079299` is an ancestor of `main`; #326 remains live at `HBL:170`. The branch was explicitly carried open at `.dev-knowledge/JOURNAL.md:74`, `JOURNAL.md:168`.|
|SUP-03|corp `docs/backlog-transcript-mime-fix` branch|DEFERRED+ticket|corp [#15] — owner: corp product-code maintainer; first integrate the ticket-only branch, then replace the literal MP4 MIME with the uploaded file MIME and add non-MP4 regression coverage|Unmerged branch tip `daa8578`; its live task is `docs/backlog-transcript-mime-fix:BACKLOG.md:64`. The branch was carried forward at `.dev-knowledge/JOURNAL.md:74` and the Phase-A0 handoff `RESIDUAL.md:62`.|
|SUP-04|Five-day-stalled intake-scene-build session|DEFERRED+ticket|[#280] — next-step owner: Rob closes the stale session after confirming no uncommitted state; hub deploy/carrier owner then propagates the intake scene under #280|The build itself completed on 2026-07-07 (`.dev-knowledge/JOURNAL.md:895-905`) and #268 was closed by `4e0e867e`; the remaining fleet propagation is the live #280 task (`HBL:187`).|

## Closure verdict

Traceability is closed: **72 expected source rows, 72 mapped exactly once, 0 unresolved; content-parity is explicitly 30/30.**

This is not a claim that every implementation is finished. Remaining work is bounded by named live tickets: chiefly #328 for the ownership/declaration/check mechanism, #315 and #325 for carriers, plus the explicitly identified supplemental branch/session owners. No operator-dictated row remains dependent on memory alone.