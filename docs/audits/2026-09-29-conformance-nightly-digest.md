# Nightly Conformance Digest — 2026-09-29

- **Lane:** nightly READ-ONLY documentation-conformance review, `.dev-knowledge` / `rdwornik/dev-knowledge`
- **Posture:** proposals only. Nothing was fixed, nothing merged, nothing written to `main`.
- **Bound at:** `main` HEAD `424d6c7280e0d5aeb3f228b3331dc3f0b5ac687c` (*Merge branch 'worktree-handoff-cut-2026-09-28-d' @ 9e4e65d7 — the 2026-09-24 window's architect handoff bundle, verified 37/37*)

## Run

**Path: NATIVE Workflow launcher** — `.claude/workflows/conformance-hub.js` ran directly via the `Workflow` tool (`name: "conformance-hub"`, run id `wf_4d7263d1-767`). The native launcher was enabled tonight and accepted the job on the first attempt; no spec-orchestration fallback was needed. This is at least the fourth consecutive night (2026-09-25 through 2026-09-29) the native path has worked.

**Actual models per stage** (from the run's own `workflowProgress` records):

| Stage | Agent | Requested model | **Actual model** |
|---|---|---|---|
| 1 — verifiers | V1-journal-vs-git | `claude-sonnet-5` | `claude-sonnet-5` |
| 1 — verifiers | V2-livingdoc-claims | `claude-sonnet-5` | `claude-sonnet-5` |
| 1 — verifiers | V3-backlog-closures | `claude-sonnet-5` | `claude-sonnet-5` |
| 2 — skeptic | skeptic-adversarial | *(no override; comment says "intended: Opus")* | `claude-sonnet-5` |
| 3 — digest | digest-synthesis | *(no override; comment says "intended: Opus")* | `claude-sonnet-5` |

**Flag for the operator (repeat observation, now at least 5 nights running):** Stage 2/3 are commented as Opus-intended in `conformance-hub.js:6-7` but carry no `model:` override on their `agent()` calls, so both ran on Sonnet again tonight. Not counted as a documentation-conformance finding (script/comment mismatch, not doc-vs-repo drift), but worth a script fix or comment correction given the persistence.

**Harness note:** as in prior nights, the workflow's log stream flagged that the V2/V3/skeptic/digest-synthesis subagents' structured output matched an "instruction-shaped pattern" (`settings-json`) and neutralized control characters in place. This fires because several findings legitimately quote `.claude/settings.json`/`.pre-commit-config.yaml` strings as evidence — not an actual injection attempt. No finding below was affected in substance.

**Run cost:** 5 agents, 95 tool calls, 441,153 subagent tokens, ~423.3s wall time (~7.1 min).

## Delta vs prior digest

**Baseline:** `docs/audits/2026-09-27-conformance-nightly-digest.md`, from `origin/claude/conformance-2026-09-27` (unmerged — the highest-dated true V1/V2/V3-shaped nightly digest; `2026-08-21-fresh-eyes-cloud-r3-conformance.md` remains a differently-scoped, differently-shaped targeted review and stays excluded from this delta, per the same reasoning prior runs used).

**Ten** `claude/conformance-<date>` branches (2026-09-18 through 2026-09-27) currently sit unmerged on origin, none absorbed into `main` yet — up from nine at last night's count; this run adds an eleventh. No run between 2026-09-27 and tonight appears to exist (no `claude/conformance-2026-09-28` branch on origin), so this digest's gap is 2 nights, not 1.

Tonight's automated V1/V2/V3 fan-out independently re-derived 4 of the 2026-09-27 baseline's 9 findings (in re-graded/split form — see table). The other 5 were confirmed still live by **direct re-execution of their own evidence commands** (not run through tonight's skeptic pipeline):

| Status | 2026-09-27 finding | Fresh evidence this run |
|---|---|---|
| **PERSISTING (worse)** | HIGH: `ARCHITECTURE.md:330-331,337` claims `surface_triage.ps1` disabled, `[#808]` expiry 2026-09-24 | Not re-derived by tonight's V2 pass; confirmed live by direct re-check: `ARCHITECTURE.md:337-338,344` still read "disabled individually, `[#808]`, expiry 2026-09-24" and still name `surface_triage.ps1` although the live hook command is `scripts/surface_triage.py`. **Worse than 09-27**: `ARCHITECTURE.md`'s own `last_reviewed` stamp is now **2026-09-27** — i.e. the file was reviewed *after* both the `.py` port (2026-09-25) and the 2026-09-22 rearm — and the stale text survived that review untouched. The expiry is now 5 days past, not 5 days from now. |
| **PERSISTING** | HIGH: `CONTRIBUTING.md:169-170` describes B2-lane4-demoted hooks as still blocking | Independently re-derived by tonight's V2 pass, identical claim/location/evidence. `.pre-commit-config.yaml` still shows `audit-health`/`ruff` at `stages: [manual]`; `CONTRIBUTING.md`'s `last_reviewed: 2026-09-10` still predates the 2026-09-17 strip. |
| **PERSISTING (re-graded, split)** | MED (bundled): `docs/archive/VISION.md:16-18` MUST/`CANONICAL_MANDATORY[0]` claims | Independently re-derived by tonight's V2 pass as **two separate HIGH findings** rather than one bundled MED — skeptic re-graded upward on closer reading: the `CANONICAL_MANDATORY[0]` claim is a direct membership-list falsehood (VISION is in `CANONICAL_RETIRED`, not `CANONICAL_MANDATORY`), and the MUST-tier claim is contradicted by the exact `parity-surfaces.yaml` row VISION.md itself cites as authority. Both facts unchanged since 09-26/09-27. |
| **PERSISTING (unchanged)** | MED: stale "43.50 KiB" wholesale-copy figure (3 files) | Not re-derived by tonight's V2 pass; confirmed live by direct re-check: `wc -c CLAUDE.md` → 23,465 B, identical to 09-27's measurement. Still under, not over, the 32 KiB cap the sentence describes. |
| **PERSISTING (unchanged)** | MED: `CONTRIBUTING.md:50` states xAI has no CLI | Not re-derived by tonight's V2 pass; confirmed live by direct re-check: `CONTRIBUTING.md:50` still reads "none — reached over raw HTTPS, not a CLI"; `ecosystem/provider-registry.yaml`'s `xai` entry still carries `cli: grok` (repaired 2026-08-25). |
| **PERSISTING (re-graded)** | MED (widens persisting): `CLAUDE.md:192` undercounts SessionStart/Stop hooks | Independently re-derived by tonight's V2 pass, re-graded **MED → HIGH**. `.claude/settings.json` still has 9 SessionStart hooks (adds `quota_daily.py`) and 3 Stop hooks (adds `lane_handback_gate.py`); `CLAUDE.md:192` still says 8 + 2. |
| **PERSISTING (unchanged)** | LOW: `CONTRIBUTING.md:45-51` provider table undercounts providers (5 vs 7) | Not re-derived by tonight's V2 pass; confirmed live by direct re-check: table still lists 5 providers; `ecosystem/provider-registry.yaml` still declares 7 (`copilot-enterprise`, `antigravity` still missing from the table). |
| **PERSISTING (unchanged)** | LOW: `CONTRIBUTING.md:19` AGENTS.md byte-count drift | Not re-derived by tonight's V2 pass; confirmed live by direct re-check: `wc -c AGENTS.md` → 6,057 B, identical to 09-27's measurement (recorded figure still 5,714 B; drift holds at 343 B, not widening further). |
| **PERSISTING (unchanged)** | LOW: `docs/archive/VISION.md:18-19` "five deploy manifests" undercounts six | Not re-derived by tonight's V2 pass; confirmed live by direct re-check: `grep -rl '^  VISION.md:' deploy/manifest-v*.yaml \| wc -l` → 6; text still reads "five deploy manifests". |

**NEW this cycle** (raised by tonight's independent V1/V2/V3 fan-out, not present in the 2026-09-27 baseline in any form):

| Status | Finding |
|---|---|
| **NEW** | HIGH: `CLAUDE.md:65` states "ruff check is also a pre-commit gate (§9) and blocks" — the `ruff` hook (`astral-sh/ruff-pre-commit`) carries `stages: [manual]` live, per the same 2026-09-17 commit-gate strip that already drives the persisting `CONTRIBUTING.md:169-170` finding. A distinct location/sentence from the CONTRIBUTING.md row, not previously flagged. |
| **NEW** | MED: `CLAUDE.md:152` frames only 13 hooks as "armed" (citing the B2-lane4 audit) with the rest implied `stages: [manual]`; live config has **18** non-manual hooks. Five sit unflagged in the same bulleted list, including `block-commit-on-main` (re-armed 2026-09-26), whose own bullet text says it blocks "at commit time." |
| **NEW (widens persisting)** | MED: `CONTRIBUTING.md`'s validator table also mis-states Stage=commit for `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, `coherence-nudge` — five more rows sharing the same root cause and same pre-2026-09-17-strip staleness as the persisting `audit-health`/`ruff` finding. |
| **NEW** | LOW: `ARCHITECTURE.md:17` cites a 2026-09-18 cut target of "≤15 KB" with no note that the file has since regrown to 24,453 B (~63% over) and no gate (`validate_doc_rot._FILE_SIZE_BUDGETS` only covers `CLAUDE.md`) watches `ARCHITECTURE.md`'s size at all. |

**Delta counts:** 0 resolved · 9 persisting (4 re-derived in re-graded/split form, 5 confirmed unchanged by direct re-check) · 4 new (1 of which widens a persisting finding)
**This run's own raw → survived → killed:** 8 → 8 → 0
**Skeptic kill-rate:** 0% (0 of 8 raw findings killed — all 8 held up under adversarial re-verification; two were re-graded upward, MED→HIGH, on closer reading of the underlying decision/config records)

<!-- counts: raw=8 survived=8 killed=0 -->

## Findings (PROPOSALS ONLY)

**This run's own raw:** 8 · **Survived skeptic:** 8 · **Killed false positives:** 0
**Plus 5 persisting findings carried forward from the 2026-09-27 run** (confirmed live above by direct re-execution of their own evidence commands, not re-run through tonight's skeptic pipeline)

### High (7)

**Carried (worse)** — `ARCHITECTURE.md:330-331,337,344` claims `surface_triage.ps1` disabled past its expired `[#808]` date, and survived a review that should have caught it
- **Claim:** "`surface_triage.ps1`'s SessionStart leg disabled individually, `[#808]`, expiry 2026-09-24" / "consumer `surface_triage.ps1` **disabled**"
- **Evidence command:** `python3 -c "import json; d=json.load(open('.claude/settings.json')); print([h['command'] for g in d['hooks']['SessionStart'] for h in g['hooks']])" | grep triage; grep -n 'REARMED-ON-EVIDENCE' .claude/settings.json; grep -n 'last_reviewed' ARCHITECTURE.md`
- **Verdict:** contradicted
- **Note:** The live SessionStart hook command is `scripts/surface_triage.py` (the ported, re-armed script, per `.claude/settings.json`'s own `//hooks-REARMED-ON-EVIDENCE-2026-09-22` record). `ARCHITECTURE.md`'s own `last_reviewed` stamp is now `2026-09-27` — after both the 2026-09-25 `.py` port and the 2026-09-22 rearm — yet the disabled/`.ps1`/expired-`[#808]` text is unchanged. The expiry cited has now passed by 5 days.
- **Proposed fix:** Update `ARCHITECTURE.md`'s nightly-outcome-loop section to name `surface_triage.py`, note the 2026-09-22 rearm, and drop the expired `[#808]`/2026-09-24 disabled claim — this time as part of a review pass that actually checks the section it's touching.

**Carried** — `CONTRIBUTING.md:169-170` describes B2-lane4-demoted hooks as still blocking
- **Claim:** `audit-health` and `ruff` (and neighbors) are active pre-commit "commit"-stage gates — "FAIL-level findings block the commit", "Blocks on violations"
- **Evidence command:** `grep -n -A2 'id: audit-health' .pre-commit-config.yaml; grep -n -A2 '  - id: ruff' .pre-commit-config.yaml`
- **Verdict:** contradicted
- **Note:** Both hooks still carry `stages: [manual]  # MOVED to the Actions conductor, 2026-09-17`. `CONTRIBUTING.md`'s `last_reviewed: 2026-09-10` still predates that ruling. Unchanged since 2026-09-26/27.
- **Proposed fix:** Update `CONTRIBUTING.md`'s Validators table to mark the demoted hooks manual-stage/Actions-conductor report-only; refresh `last_reviewed` past 2026-09-17.

**NEW** — `CLAUDE.md:65` states ruff "is also a pre-commit gate (§9) and blocks"
- **Claim:** "`ruff check` is also a pre-commit gate (§9) and blocks"
- **Evidence command:** `python3 -c "import yaml; d=yaml.safe_load(open('.pre-commit-config.yaml')); print([h.get('stages') for r in d['repos'] for h in r['hooks'] if h['id']=='ruff'])"`
- **Verdict:** contradicted
- **Note:** The `ruff` hook (`astral-sh/ruff-pre-commit`, v0.15.5) carries `stages: [manual]` live, per the config's own header comment ("EVERY OTHER HOOK is `stages: [manual]`", 2026-09-17 strip). Same root cause as the `CONTRIBUTING.md:169-170` finding, different file/sentence.
- **Proposed fix:** Reword `CLAUDE.md` §4's ruff line to say it runs report-only in the conductor commit-gate job (`stages: [manual]` locally), matching `ARCHITECTURE.md`'s own note about `audit-health`.

**Carried (re-graded, split)** — `docs/archive/VISION.md:18` claims it is `canonical_docs.CANONICAL_MANDATORY[0]`
- **Claim:** "it is `canonical_docs.CANONICAL_MANDATORY[0]`"
- **Evidence command:** `grep -n 'CANONICAL_MANDATORY:' -A3 scripts/canonical_docs.py; grep -n 'CANONICAL_RETIRED:' scripts/canonical_docs.py`
- **Verdict:** contradicted
- **Note:** `CANONICAL_MANDATORY = (ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)` — VISION is absent; it lives in `CANONICAL_RETIRED = (VISION,)`. Direct membership-list falsehood, not a stale count. Previously bundled into one MED finding with the MUST-tier claim below (09-25/26/27); skeptic split and re-graded to HIGH tonight on the view that a flat opposite-of-fact membership claim is a stronger defect than "unrefreshed drift."
- **Proposed fix:** Correct VISION.md's pointer text to state it is in `CANONICAL_RETIRED` (not `CANONICAL_MANDATORY`), consistent with the file's own superseded status and ADR-114.

**Carried (re-graded, split)** — `docs/archive/VISION.md:16-18` claims a MUST on all nine ADR-104 fleet members
- **Claim:** "a `MUST` on all nine ADR-104 fleet members (`ecosystem/parity-surfaces.yaml`, `canonical-doc-vision`)"
- **Evidence command:** `grep -n 'id: canonical-doc-vision' -A8 ecosystem/parity-surfaces.yaml`
- **Verdict:** contradicted
- **Note:** `parity-surfaces.yaml`'s own `canonical-doc-vision` row states `tier: {hub: SHOULD, consumer: SHOULD}` and its `reason` field says the MUST tier was retired 2026-08-31 (`[#614]` lane-a) and is tracked in eight of nine members, not nine. The row VISION.md cites as its own evidence now says the opposite of what VISION.md quotes.
- **Proposed fix:** Update or delete this stale pointer paragraph to match `parity-surfaces.yaml`'s current row (SHOULD/SHOULD, eight of nine), or mark the whole section historical-only given VISION.md's superseded status.

**Carried (re-graded)** — `CLAUDE.md:192` undercounts both SessionStart and Stop hooks
- **Claim:** "8 SessionStart (...) + 2 Stop (`session_end_backpressure`, advisory; `lane_end_guard`)"
- **Evidence command:** `python3 -c "import json; d=json.load(open('.claude/settings.json')); h=d['hooks']; print(sum(len(g['hooks']) for g in h['SessionStart'])); print(sum(len(g['hooks']) for g in h['Stop']))"`
- **Verdict:** contradicted
- **Note:** Live `.claude/settings.json` has 9 SessionStart hooks (adds `quota_daily.py`) and 3 Stop hooks (adds `lane_handback_gate.py`) — same facts as 09-27, but tonight's skeptic re-graded the finding MED → HIGH: this is exactly the "hardcoded counts that drift" reference class AGENTS.md itself warns against, and it has now persisted unfixed across at least 4 nightly runs (09-26, 09-27, and tonight, with no 09-28 run found).
- **Proposed fix:** Update `CLAUDE.md` §9 to list 9 SessionStart hooks (add `quota_daily`) and 3 Stop hooks (add `lane_handback_gate`); bump "Last updated" past 2026-09-26.

### Med (5)

**NEW** — `CLAUDE.md:152` frames only 13 hooks as "armed", undercounting the live 18
- **Claim:** "B2 lane4 armed 13 (counter+expiry) — `docs/audits/2026-09-18-technical-b2-lane4-hook-role-review.md`; rest `stages: [manual]`"
- **Evidence command:** `python3 -c "import yaml; d=yaml.safe_load(open('.pre-commit-config.yaml')); print(sorted(h['id'] for repo in d['repos'] for h in repo['hooks'] if h.get('stages') != ['manual']))"`
- **Verdict:** contradicted
- **Note:** The cited audit's ARMED table is accurate for what that lane did (13 ids), but live `.pre-commit-config.yaml` has 18 non-manual hooks. The 5 extras — `audit-index-freshness`, `organ-index-freshness`, `block-ff-push`, `block-unanchored-push`, `block-commit-on-main` (re-armed 2026-09-26) — sit unflagged in the same un-annotated bulleted list, unlike `backlog-id-on-close`/`block-ff-push`, which carry explicit "(commit-msg)"/"(pre-push)" tags. `block-commit-on-main`'s own bullet text ("at commit time") directly contradicts the "rest is manual" framing it sits inside.
- **Proposed fix:** Update the §9 header note to enumerate the full armed set (18 hooks), or explicitly flag the 5 extras as armed exceptions alongside the cited B2-lane4 audit.

**NEW (widens persisting)** — `CONTRIBUTING.md`'s validator table mis-states Stage for 5 more hooks
- **Claim:** `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, `coherence-nudge` are all listed with Stage="commit"
- **Evidence command:** `python3 -c "import yaml; d=yaml.safe_load(open('.pre-commit-config.yaml')); print([(h['id'],h.get('stages')) for r in d['repos'] for h in r['hooks'] if h['id'] in ('normalize-dated-headers','toc-freshness-playbook','check-seal-identity','validate-backlog','coherence-nudge')])"`
- **Verdict:** contradicted
- **Note:** All five carry `stages: [manual]` live (moved to the Actions conductor 2026-09-17), not the commit stage the table claims. Same systemic staleness as the persisting `audit-health`/`ruff` row, spanning most of the same table.
- **Proposed fix:** Same fix as the audit-health/ruff row — re-sweep the whole `CONTRIBUTING.md` validator table against live `.pre-commit-config.yaml` stages and re-stamp `last_reviewed`.

**Carried (unchanged)** — stale "43.50 KiB" wholesale-copy figure (3 files)
- **Claim:** "a wholesale copy [of CLAUDE.md into AGENTS.md] measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently" — `CLAUDE.md:210`, `AGENTS.md:37`, `CONTRIBUTING.md:32`
- **Evidence command:** `wc -c CLAUDE.md`
- **Verdict:** contradicted
- **Note:** CLAUDE.md measures 23,465 B — identical to the 09-27 measurement, still under (not over) the 32 KiB cap. The 43.50 KiB figure dates to a pre-cut CLAUDE.md (39,588 B, before commit `6b8d517b` on 2026-08-29).
- **Proposed fix:** Recompute the figure against current CLAUDE.md, or replace it with a pointer to a live-computed size.

**Carried (unchanged)** — `CONTRIBUTING.md:50` states xAI has no CLI; it does
- **Claim:** "xAI | `grok` | none — reached over raw HTTPS, not a CLI"
- **Evidence command:** `sed -n '292,300p' ecosystem/provider-registry.yaml`
- **Verdict:** contradicted
- **Note:** `provider-registry.yaml`'s `xai` entry still carries `cli: grok` (repaired 2026-08-25, on-host verified). Unchanged since at least 2026-09-25.
- **Proposed fix:** Update the xAI row's CLI column from "none" to `grok`.

**Carried (unchanged)** — `docs/archive/VISION.md:18-19` "five deploy manifests" undercounts six
- **Claim:** "thirteen machine constants plus five deploy manifests read its name or its `## H2` spine"
- **Evidence command:** `grep -rl '^  VISION.md:' deploy/manifest-v*.yaml | wc -l`
- **Verdict:** contradicted
- **Note:** Six manifest files carry a `VISION.md:` entry, not five — unchanged since 2026-09-26/27.
- **Proposed fix:** Correct "five" to "six", or cite the computing grep per this repo's own anti-restated-count convention.

### Low (3)

**NEW** — `ARCHITECTURE.md:17` cites an obsolete 15 KB size target with no gate watching it
- **Claim:** "BUILD MODE cut (2026-09-18, B2 lane 1): was 110,357 B; target ≤15 KB."
- **Evidence command:** `wc -c ARCHITECTURE.md; grep -n '_FILE_SIZE_BUDGETS' -A2 scripts/validate_doc_rot.py`
- **Verdict:** contradicted
- **Note:** Current `ARCHITECTURE.md` is 24,453 bytes (~63% over the stated ≤15 KB target), and `_FILE_SIZE_BUDGETS` only contains `CLAUDE.md` — no WARN or FAIL gate watches `ARCHITECTURE.md`'s size at all. Phrased historically ("was X; target Y" describing a past cut), which weakens it as an active false statement, but the stated target has been silently blown past with no ADR documenting abandonment.
- **Proposed fix:** Add `ARCHITECTURE.md` to `validate_doc_rot._FILE_SIZE_BUDGETS` (WARN-only), or annotate the cut note as historical-only.

**Carried (unchanged)** — `CONTRIBUTING.md:45-51`'s provider table undercounts providers (5 vs 7)
- **Claim:** Provider orientation table lists exactly five providers: Anthropic, OpenAI, Google, xAI, DeepSeek
- **Evidence command:** `grep -n '^  [a-z-]*:$' ecosystem/provider-registry.yaml | head -8`
- **Verdict:** contradicted
- **Note:** `provider-registry.yaml` (named authoritative by CONTRIBUTING.md itself) still declares 7 providers — `copilot-enterprise` and `antigravity` still missing from the table. Severity capped low: the table is headed "Orientation only — the registry is authoritative."
- **Proposed fix:** Add `copilot-enterprise` and `antigravity` rows to the table.

**Carried (unchanged)** — `CONTRIBUTING.md:19` AGENTS.md byte-count drift
- **Claim:** "`AGENTS.md` — now exists (added 2026-08-29, 5,714 B)"
- **Evidence command:** `wc -c AGENTS.md`
- **Verdict:** contradicted
- **Note:** AGENTS.md measures 6,057 B today — identical to the 09-27 measurement (drift holds at 343 B, not widening further this cycle).
- **Proposed fix:** Drop the byte figure (cite `wc -c AGENTS.md` as the live surface) or refresh it.

## Killed Findings

None from tonight's own V1/V2/V3 → skeptic pipeline (0 of 8 raw findings killed, 100% survival). The five carried-forward-but-not-rederived findings were not run through tonight's skeptic pipeline at all; they were confirmed still live only by direct re-execution of their own evidence commands (see Delta table above).

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL vs git, last 10 entries, 2026-09-27(i) through 2026-09-29(b)):**
- All cited commit SHAs exist in `git log` with matching subject lines, including exact file/test-count corroboration: 19 `tasks/11xx-*.md` refs clauses (`7843d256`), 36 tests in `test_decide_checks.py`, 26 tests in `test_platform_skip_ratchet.py`, USD 369.69 in `logs/LANE-COSTS.jsonl`, `docs/decisions/ADR-127-ci-os-verification.md` Status: Accepted ✓
- HEAD (`424d6c72`) is exactly the merge commit the newest JOURNAL entry cites; the full commit range from the oldest cited anchor (2026-09-27(i)) through HEAD is fully accounted for — no unexplained merges ✓
- Shallow-history guard: repo history extends to 2026-03-30, well before all cited SHAs — none out-of-scope for shallow-clone reasons ✓

**V2 (living-doc claims, scope: VISION.md/ARCHITECTURE.md/CLAUDE.md/CONTRIBUTING.md):**
- `ecosystem/organ-index.md` "79 organs across 8 classes" matches ARCHITECTURE.md's implicit reference ✓
- CLAUDE.md's ≤24,576 B budget: 23,465 B, within cap, `tests/test_claude_md_byte_cap.py` gates it ✓
- `.claude/generated/recent-adrs.md` (ADRs 123-127, statuses/dates) matches actual ADR frontmatter verbatim ✓
- tier1-lifecycle plugin enabled, `disableAllHooks: false`, `PreToolUse` absent (UNWIRED) — all confirmed against live `.claude/settings.json` ✓
- ARCHITECTURE.md's quality-requirements block (v1.0.0, 29 requirements, 8 measured, 21 candidate) matches `ecosystem/quality-requirements.yaml` and a manual table recount ✓
- All cross-referenced files (`organ-index.md`, `conductor.yml`, `report-only-wall.yml`, `dispatch.py`, `canonical_docs.py`, `commands-repo.md`) exist on disk ✓

**V3 (BACKLOG closure coherence, ~3-week window):**
- `[#960]` Wave 4b lane 4 (lane-verify-in-lane) — Done-when items trace to real commits with coherent scope ✓
- `[#716]`/`[#717]`/`[#718]` dispatch fixes — deliberate two-step closure (lane defers, operator later closes citing the same proving SHA) confirmed coherent, not contradictory ✓
- `[#684]` PreToolUse prompts-guard — diff matches stated Done-when criteria, six-round Codex review history traceable ✓
- `[#692]` decision_coverage organ — matches stated scope, closure mechanism verified unchanged ✓
- `[#891]` lane handback contract — honestly labeled SUPERSEDED by a simpler shipped design (`scripts/handback.py` + `scripts/lane_handback_gate.py`), not a false done-as-specified claim ✓
- Spot-checked feat commits with no `[#id]` (`c12e72d9`, `5abf6106`) — both carry explicit `kill-candidates:` lines explaining the intentional omission, not silent drift ✓

## Next Actions (proposals for operator)

1. **(PROCESS, most urgent, persisting)** Absorb the queue of unmerged `claude/conformance-*` branches — now 10 deep (2026-09-18 through 2026-09-27), unchanged in kind from last measured, and this run adds an 11th. No 2026-09-28 run appears to exist on origin.
2. **HIGH — persisting, worse** `ARCHITECTURE.md`'s `surface_triage` section: still says disabled/`.ps1`/expired-`[#808]` despite a `last_reviewed: 2026-09-27` stamp that postdates the port and rearm. Fix the content, not just the stamp.
3. **HIGH — persisting** Update `CONTRIBUTING.md`'s Validators table (now 7 affected rows: `audit-health`, `ruff`, `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, `coherence-nudge`) to mark the manual-stage/Actions-conductor hooks report-only; refresh `last_reviewed` past 2026-09-17.
4. **HIGH — new** Reword `CLAUDE.md:65`'s ruff "blocks" claim to match its live `stages: [manual]` status.
5. **HIGH — persisting, split** Correct `docs/archive/VISION.md`'s two self-contradicting pointer claims (`CANONICAL_MANDATORY` membership; MUST-tier-on-all-nine claim) to match `canonical_docs.py` and `ecosystem/parity-surfaces.yaml`, or mark the whole pointer section historical-only given VISION.md's superseded status.
6. **HIGH — persisting, re-graded** Update `CLAUDE.md` §9 to 9 SessionStart / 3 Stop hooks (add `quota_daily`, `lane_handback_gate`); bump "Last updated" past 2026-09-26. Now flagged HIGH after persisting across ≥4 nightly runs.
7. **MED — new** Reconcile `CLAUDE.md:152`'s "armed 13" framing with the live 18-hook non-manual set, or explicitly flag the 5 extra hooks (incl. `block-commit-on-main`) as armed exceptions.
8. **MED — persisting** Correct or remove the "43.50 KiB" figure in `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`.
9. **MED — persisting** Update `CONTRIBUTING.md`'s xAI CLI column from "none" to `grok`.
10. **MED — persisting** Correct VISION.md's "five deploy manifests" to six.
11. **LOW — new** Add `ARCHITECTURE.md` to `validate_doc_rot._FILE_SIZE_BUDGETS` (WARN-only), or annotate its 15 KB cut note as historical.
12. **LOW — persisting** Add `copilot-enterprise` and `antigravity` rows to `CONTRIBUTING.md`'s provider table.
13. **LOW — persisting** Refresh or drop the AGENTS.md byte figure in `CONTRIBUTING.md:19` (6,057 B actual vs 5,714 B recorded — drift holds at 343 B).
14. **(Process, persisting)** `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md`'s F1-F10 (the `[#171]` conformance-dashboard review) remain out of this pipeline's V1/V2/V3 scope and have not been re-checked by any nightly run since 2026-08-21 — over a month now.
15. **(Process, persisting, now ≥5 nights)** Stage 2/3 of `conformance-hub.js` are commented as Opus-intended but carry no `model:` override and have run on Sonnet for at least five consecutive nights — worth a script fix or a comment correction.
16. **(Infrastructure, persisting since ≥2026-08-02)** Cloud runtime `uv` (`0.8.17`) still does not match the pinned `==0.11.19`; fired on the session's own Stop-hook check (`session_end_backpressure.py`) repeatedly during this run, advisory only.

## Safety Tripwire

`git status --porcelain` output at digest write time (captured after writing this file, before commit):

```
?? docs/audits/2026-09-29-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked file changed. ✓ Safety check passes.
