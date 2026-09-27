# Nightly Conformance Digest — 2026-09-27

- **Lane:** nightly READ-ONLY documentation-conformance review, `.dev-knowledge` / `rdwornik/dev-knowledge`
- **Posture:** proposals only. Nothing was fixed, nothing merged, nothing written to `main`.
- **Bound at:** `main` HEAD `3ac878941657f5aeee77567082b26e2918d10873` (*Merge branch 'worktree-lane-decision-debt' @ 2594dd29 — decision debt discharged or named; carrier_landed_check flags a landed decision left OPEN*)

## Run

**Path: NATIVE Workflow launcher** — `.claude/workflows/conformance-hub.js` ran directly via the `Workflow` tool (`name: "conformance-hub"`, run id `wf_424bf642-cfd`). The native launcher was enabled tonight, the third consecutive night it has worked (2026-09-25, 2026-09-26, 2026-09-27). No spec-orchestration fallback was needed.

**Actual models per stage** (from the run's own `workflowProgress` records):

| Stage | Agent | Requested model | **Actual model** |
|---|---|---|---|
| 1 — verifiers | V1-journal-vs-git | `claude-sonnet-5` | `claude-sonnet-5` |
| 1 — verifiers | V2-livingdoc-claims | `claude-sonnet-5` | `claude-sonnet-5` |
| 1 — verifiers | V3-backlog-closures | `claude-sonnet-5` | `claude-sonnet-5` |
| 2 — skeptic | skeptic-adversarial | *(no override; comment says "intended: Opus")* | `claude-sonnet-5` |
| 3 — digest | digest-synthesis | *(no override; comment says "intended: Opus")* | `claude-sonnet-5` |

**Flag for the operator (repeat observation, now 3+ nights running):** Stage 2/3 are commented as Opus-intended in `conformance-hub.js:6-7` but carry no `model:` override on their `agent()` calls, so both ran on Sonnet again tonight. Not counted as a documentation-conformance finding (script/comment mismatch, not doc-vs-repo drift), but worth a script fix or comment correction given the persistence.

**Harness note:** as in the two preceding nights, the workflow's log stream flagged that the V1, V2, skeptic, and digest-synthesis subagents' structured output each matched an "instruction-shaped pattern" (`settings-json`) and neutralized control characters in place. This fires because several findings legitimately quote `.claude/settings.json` hook-command strings as evidence — not an actual injection attempt. No finding below was affected in substance.

**Run cost:** 5 agents, 116 tool calls, 448,621 subagent tokens, ~680.5s wall time (~11.3 min) — noticeably longer than the 2026-09-26 run (~393s), driven mostly by V2's living-doc scan (67 tool calls, ~446s) and the skeptic's re-verification pass (~180s).

## Delta vs prior digest

**Baseline:** `docs/audits/2026-09-26-conformance-nightly-digest.md`, from `origin/claude/conformance-2026-09-26` (unmerged — the highest-dated true V1/V2/V3-shaped nightly digest; `2026-08-21-fresh-eyes-cloud-r3-conformance.md` remains a differently-scoped, differently-shaped targeted review and stays excluded from this delta, per the same reasoning the two preceding runs used).

**Nine** `claude/conformance-<date>` branches (2026-09-18 through 2026-09-26) currently sit unmerged on origin, none absorbed into `main` yet — unchanged count from last night; this run does not attempt to fix that.

Tonight's automated V1/V2/V3 fan-out independently re-derived 2 of the 2026-09-26 baseline's 4 survivors (in bundled/updated form — see table). The other 2, plus both of the 2026-09-26 run's own "NEW" findings not re-derived tonight, were confirmed still live by **direct re-execution of their own evidence commands** (not run through tonight's skeptic pipeline):

| Status | 2026-09-26 finding | Fresh evidence this run |
|---|---|---|
| **PERSISTING (bundled)** | HIGH ×2: `VISION.md:18` `CANONICAL_MANDATORY[0]` claim; `VISION.md:17` MUST-on-nine claim | Independently re-derived by tonight's V2 as **one combined finding** (`docs/archive/VISION.md:16-18`); skeptic re-graded it **MED** ("unrefreshed drift, not an intentionally preserved decision"). Both underlying facts unchanged: `CANONICAL_MANDATORY` still excludes VISION; `parity-surfaces.yaml` still shows `SHOULD/SHOULD`. |
| **PERSISTING (unchanged)** | MED: stale "43.50 KiB" wholesale-copy figure (3 files) | Independently re-derived, identical text and evidence. `wc -c CLAUDE.md` → 23,465 B (was 23,988 B on 09-26 — CLAUDE.md itself has shrunk further, still well under the 32 KiB cap). |
| **PERSISTING** | LOW: `CONTRIBUTING.md:19` AGENTS.md byte-count drift (recorded 5,714 B) | Not re-derived by tonight's V2 pass; confirmed live by direct re-run: `wc -c AGENTS.md` → **6,057 B** (drift widened from 129 B on 09-26 to **343 B** tonight — AGENTS.md keeps growing while the cited figure doesn't move). |
| **PERSISTING** | HIGH: `CONTRIBUTING.md:169-170` describes B2-lane4-demoted hooks (`audit-health`, `ruff`) as still blocking | Not re-derived by tonight's V2 pass; confirmed live by direct re-run: `.pre-commit-config.yaml:766,867` both still read `stages: [manual]  # MOVED to the Actions conductor, 2026-09-17`, while `CONTRIBUTING.md:169-170` still say "FAIL-level findings block the commit" / "Blocks on violations". `CONTRIBUTING.md`'s `last_reviewed: 2026-09-10` still predates the 09-17 ruling. |
| **PERSISTING** | LOW: `docs/archive/VISION.md:18-19` "five deploy manifests" undercounts six | Not re-derived by tonight's V2 pass; confirmed live by direct re-run: `grep -rl '^  VISION.md:' deploy/manifest-v*.yaml \| wc -l` → 6; `VISION.md:18-19` still reads "thirteen machine constants plus five deploy manifests". |

**NEW this cycle** (raised by tonight's independent V1/V2/V3 fan-out, not present in the 2026-09-26 baseline):

| Status | Finding |
|---|---|
| **NEW** | HIGH: `ARCHITECTURE.md:330-331,337` claims `surface_triage.ps1`'s SessionStart leg is disabled (`[#808]`, expiry 2026-09-24, now passed); it was ported to `.py` and **re-armed 2026-09-22** per `.claude/settings.json`'s own `//hooks-REARMED-ON-EVIDENCE-2026-09-22` record (`PASS — exit 0, 3.99s vs 10s budget, 0 orphans`). `ARCHITECTURE.md`'s `last_reviewed: 2026-09-19` predates both the `.py` port (commit `76eda9c1`, 2026-09-25) and the rearm evidence. |
| **NEW** | MED: `CONTRIBUTING.md:50` states xAI's CLI is "none — reached over raw HTTPS, not a CLI"; `ecosystem/provider-registry.yaml`'s `xai` entry was repaired 2026-08-25 to `cli: grok`, verified on-host (`grok --version` → exit 0). A direct factual reversal, not merely an omission, predating `CONTRIBUTING.md`'s 2026-09-10 `last_reviewed` stamp by 16 days. |
| **NEW** | MED: `CLAUDE.md:192` "8 SessionStart + 2 Stop" hook roster; live `.claude/settings.json` now has **9** SessionStart hooks (adds `quota_daily.py`, wired 2026-09-26) and **3** Stop hooks (adds `lane_handback_gate.py`, wired 2026-09-25) — this widens the 09-26 run's Stop-only finding (then HIGH, 2 vs 3) to cover SessionStart too; skeptic re-graded the combined finding **MED**. |
| **NEW** | LOW: `CONTRIBUTING.md:45-51`'s provider orientation table lists 5 providers (Anthropic, OpenAI, Google, xAI, DeepSeek); `ecosystem/provider-registry.yaml` — the file `CONTRIBUTING.md` itself names as authoritative — declares **7** (also `copilot-enterprise`, `antigravity`, both added before the file's own `last_reviewed` stamp). Severity capped low: the table is explicitly headed "Orientation only — the registry is authoritative." |

**Delta counts:** 0 resolved · 7 persisting (2 bundled/re-graded, 5 unchanged — 3 of the 5 confirmed by direct re-check rather than tonight's own pipeline) · 4 new (1 of which subsumes/widens a persisting finding rather than being wholly independent)
**This run's own raw → survived → killed:** 6 → 6 → 0
**Skeptic kill-rate:** 0% (0 of 6 raw findings killed — all 6 held up under adversarial re-verification; two were re-graded down in severity, from HIGH to MED, on closer reading of the underlying decision record)

<!-- counts: raw=6 survived=6 killed=0 -->

## Findings (PROPOSALS ONLY)

**This run's own raw:** 6 · **Survived skeptic:** 6 · **Killed false positives:** 0
**Plus 3 persisting findings carried forward from the 2026-09-26 run** (confirmed live above by direct re-execution of their own evidence commands, not re-run through tonight's skeptic pipeline)

### High (2)

**NEW** — `ARCHITECTURE.md:330-331,337` claims `surface_triage` is disabled past its stated expiry; it was re-armed
- **Claim:** "consumer `surface_triage.ps1` **disabled**" / "its SessionStart leg disabled individually, `[#808]`, expiry 2026-09-24"
- **Evidence command:** `python3 -c "import json; d=json.load(open('.claude/settings.json')); print([h['command'] for g in d['hooks']['SessionStart'] for h in g['hooks']])" | grep surface_triage; grep -n 'hooks-REARMED-ON-EVIDENCE-2026-09-22' .claude/settings.json`
- **Verdict:** contradicted
- **Note:** `scripts/surface_triage.py` (ported from the `.ps1`, same behaviour per its own docstring) is actively wired in the live SessionStart hooks array today. It was re-armed 2026-09-22 with a passing probe recorded in `settings.json` itself. `ARCHITECTURE.md`'s `last_reviewed: 2026-09-19` predates both the port (`76eda9c1`, 2026-09-25) and the rearm evidence; its cited expiry (2026-09-24) has since passed uncorrected.
- **Proposed fix:** Update `ARCHITECTURE.md`'s nightly-outcome-loop section to note the `.py` port and 2026-09-22 rearm; drop the expired `[#808]`/2026-09-24 disabled claim.

**Carried** — `CONTRIBUTING.md:169-170` describes B2-lane4-demoted hooks as still blocking
- **Claim:** `audit-health` and `ruff` (and neighbors) are active pre-commit "commit"-stage gates — "FAIL-level findings block the commit", "Blocks on violations"
- **Evidence command:** `grep -n -A2 'id: audit-health' .pre-commit-config.yaml; grep -n -A2 '  - id: ruff' .pre-commit-config.yaml`
- **Verdict:** contradicted
- **Note:** Both hooks (and several neighbors) still carry `stages: [manual]  # MOVED to the Actions conductor, 2026-09-17`. `CONTRIBUTING.md`'s `last_reviewed: 2026-09-10` still predates that ruling by a week. Unchanged since 2026-09-26; not independently re-derived by tonight's V2 pass, confirmed live by direct re-check.
- **Proposed fix:** Update `CONTRIBUTING.md`'s Validators table to mark the demoted hooks manual-stage/Actions-conductor report-only; refresh `last_reviewed` past 2026-09-17.

### Med (4)

**Carried (bundled, re-graded MED)** — `docs/archive/VISION.md:16-18` still claims pre-retirement MUST/CANONICAL_MANDATORY[0] status
- **Claim:** "a `MUST` on all nine ADR-104 fleet members ... `canonical_docs.CANONICAL_MANDATORY[0]`"
- **Evidence command:** `grep -n -A3 'CANONICAL_MANDATORY: tuple' scripts/canonical_docs.py; grep -n -A2 'canonical-doc-vision' ecosystem/parity-surfaces.yaml`
- **Verdict:** contradicted
- **Note:** `CANONICAL_MANDATORY = (ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)` — VISION is absent; it lives in `CANONICAL_RETIRED`. `parity-surfaces.yaml`'s `canonical-doc-vision` row confirms the `[#614]` lane-a retirement to `SHOULD/SHOULD` (2026-08-31). VISION.md's `last_reviewed` (2026-08-29) predates the retirement by 2 days and was never revisited. Unchanged since 2026-09-25/26; skeptic combined the two prior HIGH findings into one and graded it MED as unrefreshed drift rather than a live self-contradiction risk.
- **Proposed fix:** Rewrite VISION.md's "Why this file is still here" note to state the current `[#614]` lane-a SHOULD status and eight-of-nine tracking, dropping the MUST/`CANONICAL_MANDATORY[0]` claim.

**Carried (unchanged)** — stale "43.50 KiB" wholesale-copy figure (3 files)
- **Claim:** "a wholesale copy [of CLAUDE.md into AGENTS.md] measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently" — `CLAUDE.md:210`, `AGENTS.md:35-37`, `CONTRIBUTING.md:31-32`
- **Evidence command:** `wc -c CLAUDE.md`
- **Verdict:** contradicted
- **Note:** CLAUDE.md now measures 23,465 B — under, not over, the 32 KiB cap (shrunk further from 23,988 B on 09-26). The 43.50 KiB figure dates to a pre-cut CLAUDE.md (39,588 B, before commit `6b8d517b` on 2026-08-29). Unchanged since at least 2026-09-25.
- **Proposed fix:** Recompute the figure against current CLAUDE.md, or replace it with a pointer to a live-computed size.

**NEW** — `CONTRIBUTING.md:50` states xAI has no CLI; it does
- **Claim:** "xAI | `grok` | none — reached over raw HTTPS, not a CLI"
- **Evidence command:** `sed -n '292,300p' ecosystem/provider-registry.yaml`
- **Verdict:** contradicted
- **Note:** `provider-registry.yaml`'s `xai` entry was repaired 2026-08-25 to `cli: grok`, with an on-host verification (`grok --version` → exit 0) superseding the earlier `cli: null` premise — a direct factual reversal, 16 days before CONTRIBUTING.md's own `last_reviewed: 2026-09-10` stamp.
- **Proposed fix:** Update the xAI row's CLI column from "none" to `grok`.

**NEW (widens a persisting finding)** — `CLAUDE.md:192` undercounts both SessionStart and Stop hooks
- **Claim:** "8 SessionStart (...) + 2 Stop (`session_end_backpressure`, advisory; `lane_end_guard`)"
- **Evidence command:** `python3 -c "import json; d=json.load(open('.claude/settings.json')); h=d['hooks']; print(sum(len(g['hooks']) for g in h['SessionStart'])); print(sum(len(g['hooks']) for g in h['Stop']))"`
- **Verdict:** contradicted
- **Note:** Live `.claude/settings.json` has 9 SessionStart hooks (adds `quota_daily.py`, wired by commit `5567155a`, 2026-09-26) and 3 Stop hooks (adds `lane_handback_gate.py`, wired by commit `e1a30321`, 2026-09-25). The 09-26 digest flagged only the Stop-hook gap (then HIGH); tonight's independent pass also caught the SessionStart gap and the skeptic graded the combined finding MED.
- **Proposed fix:** Update CLAUDE.md §9 to list 9 SessionStart hooks (add `quota_daily`) and 3 Stop hooks (add `lane_handback_gate`); bump "Last updated" past 2026-09-26.

### Low (3)

**NEW** — `CONTRIBUTING.md:45-51`'s provider table undercounts providers (5 vs 7)
- **Claim:** Provider orientation table lists exactly five providers: Anthropic, OpenAI, Google, xAI, DeepSeek
- **Evidence command:** `grep -n '^  [a-z-]*:$' ecosystem/provider-registry.yaml | head -8`
- **Verdict:** contradicted
- **Note:** `provider-registry.yaml` (named authoritative by CONTRIBUTING.md itself) declares 7 providers — `copilot-enterprise` (added 2026-08-29) and `antigravity` (added 2026-08-25) are missing, both predating the file's 2026-09-10 `last_reviewed` stamp. Severity capped low: the table is headed "Orientation only — the registry is authoritative."
- **Proposed fix:** Add `copilot-enterprise` and `antigravity` rows to the table.

**Carried** — `CONTRIBUTING.md:19` AGENTS.md byte-count drift (widened)
- **Claim:** "`AGENTS.md` — now exists (added 2026-08-29, 5,714 B)"
- **Evidence command:** `wc -c AGENTS.md`
- **Verdict:** contradicted
- **Note:** AGENTS.md measures 6,057 B today — drift widened to 343 B from 129 B on 2026-09-26. Not independently re-derived by tonight's V2 pass; confirmed live by direct re-check.
- **Proposed fix:** Drop the byte figure (cite `wc -c AGENTS.md` as the live surface) or refresh it.

**Carried** — `docs/archive/VISION.md:18-19` "five deploy manifests" undercounts six
- **Claim:** "thirteen machine constants plus five deploy manifests read its name or its `## H2` spine"
- **Evidence command:** `grep -rl '^  VISION.md:' deploy/manifest-v*.yaml | wc -l`
- **Verdict:** contradicted
- **Note:** Six manifest files carry a `VISION.md:` entry, not five — unchanged since 2026-09-26. Not independently re-derived by tonight's V2 pass, confirmed live by direct re-check.
- **Proposed fix:** Correct "five" to "six", or cite the computing grep per this repo's own anti-restated-count convention.

## Killed Findings

None from tonight's own V1/V2/V3 → skeptic pipeline (0 of 6 raw findings killed, 100% survival). The three carried-forward-but-not-rederived findings were not run through tonight's skeptic pipeline at all; they were confirmed still live only by direct re-execution of their own evidence commands (see Delta table above).

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL vs git, last 10 entries, 2026-09-26(a) through 2026-09-26(j)):**
- All 10 entries' cited commit hashes exist in `git log` with matching subject lines, including two spot-read commit messages matching their JOURNAL summaries near-verbatim (`87f44c7`, `4fccfc2`) ✓
- Files claimed created/modified all exist and match description: `scripts/carrier_landed_check.py` (207 lines), `scripts/hooks/quota_daily.py` wired into SessionStart, `scripts/task_record.py`'s typed `refs` field, 39 new task files in the 1016-1075 range, ADR-122's Accepted status in both the ADR file and README index ✓
- A specific numeric claim (Actions minutes at 188.4% of the 3,000/month quota) corroborated against the live `logs/QUOTA-READS.jsonl` record ✓
- HEAD (`3ac8789`) is exactly the merge commit the newest JOURNAL entry cites; `git log 3ac8789..HEAD` is empty — no significant merged work omitted ✓

**V2 (living-doc claims, scope: VISION.md/ARCHITECTURE.md/CLAUDE.md/CONTRIBUTING.md):**
- CLAUDE.md's ≤24,576 B budget: 23,465 B, within cap, gating test file exists ✓
- ARCHITECTURE.md's Codemap block reproduces byte-for-byte via `python -m scripts.codemap.cli generate` ✓
- ARCHITECTURE.md's "29 requirements, 8 measured, 21 candidate" matches `ecosystem/quality-requirements.yaml` computed counts ✓
- CONTRIBUTING.md's ruff pin (v0.15.5) matches `.pre-commit-config.yaml` and `pyproject.toml`'s required-version floor ✓
- AGENTS.md/CONTRIBUTING.md's `uv` pin claim (`==0.11.19`) matches `pyproject.toml` `[tool.uv]` verbatim ✓
- `.claude/generated/recent-adrs.md` (ADRs 122-126, statuses/dates) matches actual ADR frontmatter ✓
- CLAUDE.md §9's pre-commit hook roster: every hook id in `.pre-commit-config.yaml` appears in CLAUDE.md §9; the "armed 13" live-stage count matches an actual count of 13 ✓

**V3 (BACKLOG closure coherence, ~3-week window):**
- `[#960]` lane-verify-in-lane closure — 4 Done-when clauses delivered before the bookkeeping-only closure commit, including real gh-CLI-sourced measurement data (not a stub) ✓
- `[#891]` HANDBACK design — closed SUPERSEDED (not DONE) with the replacement mechanism (`scripts/handback.py` + `scripts/lane_handback_gate.py`) verified on disk and test-covered; a disclosed closure category, not a false claim ✓
- `[#716]`/`[#717]`/`[#718]` dispatch-lane-base fixes — closure commit matches scope, named tests exist, and internally-consistent sequencing with the later `[#727]` fix ✓
- `[#684]` PreToolUse guard — closure citing a "six rounds clean" Codex review corroborated by matching audit files on disk ✓
- 39-row filing merge (`41d61643`/`7ebf63ba`) — diff confirms exactly 39 rows `[#1016]`-`[#1054]` added, matching the commit's own count claim ✓

## Next Actions (proposals for operator)

1. **(PROCESS, most urgent, persisting)** Absorb the queue of unmerged `claude/conformance-*` branches — still 9 deep (2026-09-18 through 2026-09-26), unchanged from last night; this run adds a 10th.
2. **HIGH — new** Update `ARCHITECTURE.md`'s nightly-outcome-loop section: `surface_triage` was ported to `.py` and re-armed 2026-09-22; drop the expired `[#808]`/2026-09-24 disabled claim.
3. **HIGH — persisting** Update `CONTRIBUTING.md`'s Validators table to mark `audit-health`/`ruff`/neighbors as manual-stage/Actions-conductor report-only; refresh `last_reviewed` past 2026-09-17.
4. **MED — persisting (bundled)** Rewrite VISION.md's retention note to the current `[#614]` lane-a SHOULD status, dropping the MUST/`CANONICAL_MANDATORY[0]` claim.
5. **MED — persisting** Correct or remove the "43.50 KiB" figure in `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`.
6. **MED — new** Update `CONTRIBUTING.md`'s xAI CLI column from "none" to `grok`.
7. **MED — new (widens persisting)** Update CLAUDE.md §9 to 9 SessionStart / 3 Stop hooks (add `quota_daily`, `lane_handback_gate`); bump "Last updated" past 2026-09-26.
8. **LOW — new** Add `copilot-enterprise` and `antigravity` rows to CONTRIBUTING.md's provider table.
9. **LOW — persisting** Refresh or drop the AGENTS.md byte figure in CONTRIBUTING.md:19 (6,057 B actual vs 5,714 B recorded — drift now 343 B).
10. **LOW — persisting** Correct VISION.md's "five deploy manifests" to six.
11. **(Process, persisting)** `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md`'s F1–F10 (the `[#171]` conformance-dashboard review) remain out of this pipeline's V1/V2/V3 scope and have not been re-checked by any nightly run since 2026-08-21 — over a month now.
12. **(Process, persisting, now 3+ nights)** Stage 2/3 of `conformance-hub.js` are commented as Opus-intended but carry no `model:` override and have run on Sonnet for at least three consecutive nights (09-25, 09-26, 09-27) — worth a script fix or a comment correction.
13. **(Infrastructure, persisting since ≥2026-08-02)** Cloud runtime `uv` (`0.8.17`) still does not match the pinned `==0.11.19`; fired on the session's own Stop-hook check (`session_end_backpressure.py`) during this run, advisory only.

## Safety Tripwire

`git status --porcelain` output at digest write time (captured after writing this file, before commit):

```
?? docs/audits/2026-09-27-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked file changed. ✓ Safety check passes.
