# Silent-rule census — the four-state ledger baseline

- **Class:** census (ADR-101 enum) · **Date:** 2026-07-19 · **Slug:** silent-rule-ledger
- **Source-session:** ARC-5 silent-rule census (Opus 4.8, 1M), read-only measurement lane, zero mutations
- **Pinned to:** HEAD `bf49cbf959acf1ca0dfb970b17bf02f34a9862ef` — every row below was measured at that sha
- **Why archived here:** `[E8]` records the baseline *numbers*; this artifact is the *evidence* behind them — the 176-item itemisation, the declared list, the near-misses, and the pending-#242 extraction. Filed so the measurement is reproducible from the repo rather than resident on one machine.
- **Scope:** `protocols/` + `templates/` + `ecosystem/*.yaml`. `docs/decisions/` deferred to `[#357]`, so **N_silent 176 is a floor, not a total.**

---


## Ruled definitions applied (verbatim — for `[E8]` plan of record)

These govern the metric and were operator-ruled in-session. Recorded here because they cannot live
only in a session transcript.

> **Denominator.** MUST-shaped normative statements (MUST / never / only / required / shall) in
> `docs/decisions/`, `protocols/`, `templates/`, `ecosystem/*.yaml`. The unit is the RULE, not the
> ADR. One ADR contributes 0..n rules.

> **No fifth state.** Advisory-by-design statements ("recommended convention, not CI-enforced";
> "otherwise it remains a non-binding convention") are NOT MUST-shaped and fall OUT of the
> denominator entirely. They are not a bucket. A MUST-shaped rule that explicitly states it is not
> mechanised is `declared-unenforced`.

> **Declaration test — on-surface AND bound to an OPEN ticket. Both conditions, not either.**
> *On-surface:* the clause must appear at the rule's own file:line or its canonical
> PLAYBOOK/ESSENTIALS span. `silent` means a reader OF THE RULE cannot tell it is unenforced — that
> is the entire diagnostic value, and an admission filed somewhere else does not restore it.
> *Open ticket:* the clause must name an open ticket carrying the remaining work. ADR-81(d) requires
> a deferral to name the gap AND what remains. Without this condition a rule could be moved out of
> `silent` by prose alone, and N_silent becomes gameable by writing "this isn't enforced" next to
> every rule. That failure mode is worse than the gap it would hide.

> **pending-#242.** Handoff cluster ADR-32/37/42/55/56/57/58 → excluded from the denominator,
> counted and reported separately.

---

## Method

**Pass 1 — mechanical.** Token sweep over the four corpora. Raw: **5,389 candidate lines / 180
files**. Scoped per ruling (3) to `protocols/` + `templates/` + `ecosystem/*.yaml`, archives
excluded as non-live: **812 candidate lines / 44 files**.

**Pass 2 — judgment on the residue.** Four read-only extractors, partitioned by corpus. Each was
required to (a) key mechanism lookups on the rule's SUBJECT, never an ADR number; (b) OPEN any
candidate mechanism and confirm it implements the rule before claiming a hit; (c) report `none`
honestly; (d) report tool failures loudly rather than returning clean rows.

**Tooling assertions.** `rg` / `grep` / `python` / `git` confirmed present before use. `bc` was
**absent** and the first count attempt **failed loudly** (exit 127) rather than returning zeros —
re-run without it. No swallowed `FileNotFoundError`; no MECH=0 row rests on a silent failure.

**Contamination control.** A live locked worktree exists at `.claude/worktrees/arc5-plan-of-record`
(branch `docs/arc5-plan-of-record` @ `496ac6ac`, gitignored). It is outside the denominator roots
and was excluded from every mechanism lookup.

---

## Controls

| Control | Location | Mechanism | Declaration | State | Verdict |
|---|---|---|---|---|---|
| **(i)** ADR MUST-cite intake-id | `templates/ADR-template.md:9` | **none** | none | **silent** | **LANDS AS PREDICTED** |
| **(ii)a** worktree side-effect | `protocols/PLAYBOOK.md:1131-1133` · `protocols/ESSENTIALS.md:82` | **none** | on-surface + `[#353]` **open** | **declared-unenforced** | **CORRECTED** |
| **(ii)b** consumer-leg merge delegation | `protocols/PLAYBOOK.md:1247-1255` · `protocols/ESSENTIALS.md:84` | **none** | none on-surface | **silent** | **LANDS AS PREDICTED** |

**Control (i) detail.** `templates/ADR-template.md:9` — *"RULE: an ADR born from an intake doc MUST
cite its intake-id — the docs/intake/ ↔ ADR traceability edge (ADR-98)."* Neither ADR-102 nor
ADR-103 carries an `Intake:` line. Exhaustive negative search: **no script reads an ADR's
`**Intake:**` field.** `scripts/check_backlog_filing.py` Leg 3 is a **different subject** — its
regexes operate on `git diff --cached` of `BACKLOG.md` task bullets only and never open
`docs/decisions/**`. `gen_intake_index.py` parses the producer side (`docs/intake/*.md` frontmatter),
not the ADR consumer side. Rule is unmechanised and carries no admission.

**Control (ii)a — why CORRECTED, not failed.** Merge `8c913a6a` added an explicit non-mechanisation
clause at both surfaces: PLAYBOOK:1138 *"**Honest limit:** this is **prose discipline today, not a
mechanism.**"* and ESSENTIALS:82 *"Prose today, not a gate ([#353] open)"*, with `[#353]` open in
`BACKLOG.md:42`. Under the ruled declaration test this satisfies both conditions. **The inoculation
converted a silent rule into a declared one — the mechanism working as designed.** The model is not
wrong; the pre-measurement expectation was stale w.r.t. what that merge landed.

**Control (ii)b — why it stays silent.** Its only admission is off-surface, in a test docstring:
`tests/test_merge_serialization.py:20-21` — *"a primary-checkout self-merge is byte-identical to a
legitimate operator merge, so no hook can distinguish it. Those are covered by the commit-and-STOP /
integrate-from-the-primary prose rules."* Off-surface fails condition (a); its ticket `#200` is
closed, failing condition (b). Both conditions fail independently.

**Seed-1 four (RULING-W · two-tier · worktree side-effect · merge-delegation):**

| Rule | Location | State |
|---|---|---|
| RULING-W (hub→consumer write shape) | `ESSENTIALS.md:83` · `PLAYBOOK.md:1233-1235`, `:1237-1238`, `:1239-1240` | **silent** |
| Two-tier new-path rule | `PLAYBOOK.md:507`, `:510`, `:511-512` | **declared-unenforced** (`[#345]` open) |
| Worktree side-effect | `PLAYBOOK.md:1131-1133` · `ESSENTIALS.md:82` | **declared-unenforced** (`[#353]` open) |
| Consumer-leg merge delegation | `PLAYBOOK.md:1247-1255` · `ESSENTIALS.md:84` | **silent** |

---

## Tallies

| Corpus | Rules | enforced (incl. partial) | declared-unenforced | **silent** |
|---|---:|---:|---:|---:|
| `protocols/PLAYBOOK.md` | 159 | 61 | 8 | **90** |
| `protocols/` (other 9 files) | 122 | 49 | 5 | **68** |
| `templates/` | 26 | 11 | 0 | **15** |
| `ecosystem/*.yaml` | 13 | 9 | 1 | **3** |
| **DENOMINATOR** | **320** | **130** | **14** | **176** |

**N_silent = 176 · N_declared = 14 · N_enforced = 130** (denominator 320; `docs/decisions/`
deferred to run 2 per ruling (3)).

**pending-#242 (excluded, reported separately): 73 MUST-rules across 7 ADRs.**

### Diagnostic matrix — recorded × enforced × legible

"Recorded" = the rule exists in canon. "Legible" = a reader of the rule can tell its enforcement
status. Every row in the denominator is recorded by construction.

| recorded | enforced | legible | count | meaning |
|:---:|:---:|:---:|---:|---|
| ✓ | ✓ | ✓ | 130 | mechanised; enforcement discoverable from the rule or its named organ |
| ✓ | ✗ | ✓ | 14 | **declared-unenforced** — honest gap, ticketed, on-surface |
| ✓ | ✗ | ✗ | **176** | **silent** — reads as binding, nothing enforces it, nothing says so |
| ✓ | ✓ | ✗ | — | not separately counted; partials folded into row 1 (see Limitations) |

**The load-bearing number is row 3: 176 rules — 55% of the denominator — read as binding while
nothing enforces them and nothing admits it.**

---

## N_silent — itemised

### A. `protocols/PLAYBOOK.md` (90)

`:247` judgment-phases never delegated · `:326` ARCHITECTURE §3 pointer required every repo ·
`:346` archived command must not head a live list · `:377` floor generator operator-invoked only,
never a hook · `:405` 200-line cap not exceeded · `:407` only per-repo governance stays in CLAUDE.md ·
`:412` handoff must not manage CLAUDE.md · `:463` main default branch, no exceptions · `:524` commit
summary never "wip"/"fix"/"stuff" · `:525` body required for non-trivial change · `:552` files that
MUST remain at root · `:566` `.env.example` do not create · `:577` no `files.exclude` to hide root
configs · `:609` `<domain>` a theme, never a location · `:656` every architect prompt re-declares
MODE · `:661` operator choice structured, never free-form · `:673` architect never writes inline
git/shell in chat prose · `:687` English only in prompt body · `:688` Model/Mode/Effort table
verbatim, never paraphrased · `:791` tests must exist and pass before merge · `:813-815` tests
derived from acceptance criteria, never from implementation · `:832-834` test must distinguish met
from silently-not-evaluated · `:1028` deploy field never hand-fabricated · `:1060-1063` decision MUST
name what becomes obsolete (`Decommission:`) · `:1099` transient status never in governance docs ·
`:1101` single-source overrides never-delete only for canonical duplicates · `:1213` wait for prompt,
never improvise · `:1227` one checkout = one committing session · `:1229` parallel sessions
commit-and-STOP, never self-merge · `:1233-1235` only sanctioned write shape is consumer
worktree/branch → report **(RULING-W)** · `:1237-1238` never a direct push into a live consumer
checkout · `:1239-1240` re-witness the consumer live before any edit · `:1247-1255` hub never merges
its own consumer branch **(control ii.b)** · `:1273-1274` two items on the same substantive file go
serial · `:1334-1343` seed `ecosystem/*/state.yaml`, do not delete `.worktreeinclude` · `:1347`
worktrees stay under `.claude/worktrees/` · `:1480-1482` `remove` not idempotent, never a second
`remove` · `:1507` sub-worktree only by architect escalation · `:1510-1512` concurrent epics MUST
have disjoint boundaries · `:1515-1517` only the root merges to main, one at a time · `:1582`
`--scope project` mandatory · `:1590` boundary question resolves audit → ruling → mechanism, never
ad-hoc · `:1604` operator-invoked, never scheduled · `:1683` cloud Routine self-contained, no hub
reference load-bearing · `:1685` hub-needing Routine is STOP-and-escalate · `:1690` graduation
requires all criteria · `:1695` no `fallbackModel` on a pinned stage · `:1697` routine with no funnel
consumer is not deployed · `:1698` n=2 evidence gate before graduation · `:1737` review runs BEFORE
STOP, never deferred · `:1739` acceptance criterion frozen ex-ante, immutable to executor · `:1925`
`/codex-review` code only, never markdown-only · `:1929` `/changelog-review` never implements
adoptions · `:1938` subagents read-only fan-out, never code-gen peers · `:2065` `--no-verify` never
habit · `:2067` validator/hook must enforce identically · `:2076` children consume agents, never
author · `:2305` governance pointer required for read-only/governance tasks · `:2307` summary table
required at top of every formal prompt · `:2379` anti-conflation of the Opus fallback · `:2383`
`ultracode` never a fourth effort level · `:2386` pinned stages MUST NOT set `fallbackModel` ·
`:2405` governance pointer required · `:2447` 3+ files → formal prompt required · `:2456` clean
`git status` between numbered steps · `:2458` bypass permissions almost never · `:2629` ADR
distillation mandatory, never a manual hand-off · `:2632` never reopen a decided topic · `:2733` ADR
generated in CC, never hand-pasted · `:2892` code review stays on Sonnet, never Haiku · `:2900` never
auto-apply suggested changes · `:2915` `git status` must be clean at session start · `:2938` main
thread never full-reads a large artifact · `:2954` summary must not duplicate live-source mechanics ·
`:3104` Council ADR distillation mandatory automated step · `:3156` handoffs pointer-only, never
duplicate the queue · `:3222` BACKLOG actionable items only · `:3227` handoffs must NOT duplicate the
pending queue · `:3269` never duplicate a schema · `:3347` `CHANGELOG.md` must not be recreated ·
`:3396` never rename without impact analysis first · `:3407` commit after each logical change ·
`:3441` per-repo `AGENTS.md` only repo-specific rules · `:3446` exact model strings only · `:3447`
sol/luna only when lane strength fits (`[#333]` **closed** → fails declaration test) · `:3455`
consumers never edit global Codex config · `:3487` audit-first, fix-second · `:3574` audit before
route · `:3575` never reverse Strażnik roles · `:3807` auto-TOC only past the threshold

### B. `protocols/` other files (68)

**ESSENTIALS.md (9):** `:38` browser no filesystem access · `:51` Scale S/M+ delivery format · `:52`
plan-mode decision structured, never free-form · `:53` Witnessed/Inference/Unknown markers · `:54`
operator never does technical adjudication · `:83` RULING-W hub→consumer write shape · `:84`
consumer-leg merge delegation **(control ii.b)** · `:126` review-before-STOP · `:162` data
sanitization before writing lessons

**HANDOFF_PROCESS.md (20):** `:49` no re-transmission of repo-encoded state · `:62` methodology not
re-stated as prose · `:109` do not trust the residual's headline · `:116-117` browser must respond
"run `<command>`" · `:154` handoff points, does not re-narrate IDs · `:175-176` browser reviews only
risky plans · `:178-185` plan-review output contract (exactly one of three) · `:369-370` architect
mode adds no return-leg artifact · `:422-426` supplement hard scope constraint · `:455-457` v5 bundle
carries four files and no README · `:468-469` `PASTE_THIS.md` never hand-edited · `:487-489` every
lane boots from a generated handoff · `:496-497` epic done-contract immutable to the lane · `:499-500`
RELATIVE PATHS ONLY · `:502-503` FILE-BOUNDARY, concurrent epics MUST be disjoint · `:504-506`
escalation rules · `:510-513` every architect prompt re-declares MODE · `:517` closing report required
before any merge · `:522` closure claimed on the hard metric · `:600-602` functional-architect role
contract

**HANDOFF_BOOT.md (10):** `:18-20` no unilateral action on governed matters · `:21-22` first move,
do nothing else · `:24` exact on-load reply · `:37` CC produces, browser reviews · `:86-88` do not
relay routine output · `:95-96` review only risky plans · `:143-145` parallel-split decision-rule ·
`:170-171` don't assert from the handoff alone · `:181-188` emit exactly one of three · `:190-194`
feedback is an artifact, not chat prose

**DEFINITION_OF_DONE.md (2):** `:107-109` 4-week scope freeze — **expired in place** (window
`~2026-07-14` elapsed; repo date 2026-07-19; no successor clause) · `:113-118` build acceptance
contract frozen ex-ante

**AI_COUNCIL_PROCESS.md (14):** `:44-51` Council justification threshold · `:53-54` max 2 debates ·
`:61-62` step must pass its gate · `:95-96` one-sentence question gate · `:154` never >5 options ·
`:161-162` recency/source rules mandatory · `:168` synthesizer must not be on the panel · `:169` max
2 rounds · `:193-195` do not drop a failing brief into the inbox · `:276-280` commit routed
transcripts before the next debate · `:330-334` debate not complete until its ADR exists · `:350`
**ADRs are immutable, never edit in place** · `:373-375` briefs ephemeral, do not commit · `:22-23`
diagram/prose disagreement resolution

**ENVIRONMENT.md (6):** `:196` vault pre-sales only · `:231` audit Gemini API tier · `:242` code
review never Haiku · `:243` Haiku only for reports/snapshots · `:248` vault/dev-knowledge scope split ·
`:258` rejected items, do not revisit before Q3

**AGENT_FRAMEWORK.md (2):** `:20-26` framework requirements · `:37` promote to a discrete task

**SESSION_SETUP.md (5):** `:102` never generate filesystem commands from memory · `:105` max 2
objectives · `:164-165` English, single code block, `[CONTEXT LOST]` · `:210-213` session-start
BACKLOG read · `:218` cite the BACKLOG entry, don't copy it

### C. `templates/` (15)

`ADR-template.md:9` MUST cite intake-id **(control i)** · `ARCHITECTURE-template.md:41`+`:103`
diagrams never inline in canonical docs (the check that covered this — `check_mermaid_theme_directive` —
was **retired**, `audit.py:532`) · `CLAUDE-md-template.md:42` read-before-structural-changes half ·
`CONTRIBUTING-md-template.md:34` branch-prefix four-only half (exhaustive grep for a prefix allowlist:
**zero hits**) · `:70` cross-repo refs repo-qualified (declaration names `#328` — **closed**, and
#328 shipped as the parity manifest which does **not** check this) · `:72` historical commits never
rewritten · `:139` a handoff never writes to a target repo · `:13` CONTRIBUTING byte-identical to hub ·
`claude-regions/critical-rules-records.md:1` **LESSONS.md / logs/TOKEN-LOG.md append-only** ·
`:2` **JOURNAL.md append-only newest-first** · `:3` **ADRs/transcripts/handoffs/audits immutable**
(guard covers transcripts only — `block_immutable_edits.py:81` *"Deliberately NOT `docs/decisions/`"*) ·
`claude-regions/antipatterns-universal.md:3` Layer-2 validators-only invariant ·
`claude-regions/conventions-output-formatting.md:1` flat + fenced report format ·
`claude-regions/session-start-protocol.md:7` wait for prompt, never improvise ·
`consumer-onboarding-runbook.md:29` GATE-0 failed → STOP · `codex-review-config-template.md:21`
Codex MUST NOT write · `prompt-template.md:61` only READY proceeds · `intake-template.md:16` intake
genre WHAT/WHY only

### D. `ecosystem/*.yaml` (3)

`disposition-register.yaml:20` one Finding per concern (convention-only; no check verifies a **new**
organ complies) · `doc-code-edge.yaml:33` rollout must drive to 100% resolved ·
`satellite-onboarding-rulings.yaml:61-63` onboarding arc must surface the plan-gate choice, never
silently (validator self-declares NON-BLOCKING, in no `ALL_CHECKS`)

---

## N_declared — itemised (14)

| Rule | Ticket | Open? |
|---|---|:---:|
| `PLAYBOOK.md:507` ambiguity → operator authorization | `[#345]` | ✓ |
| `PLAYBOOK.md:510` citation mandatory for every proceed | `[#345]` | ✓ |
| `PLAYBOOK.md:510-511` folder creation hard-gated in all cases | `[#345]` | ✓ |
| `PLAYBOOK.md:511-512` path auth ≠ content auth | `[#345]` | ✓ |
| `PLAYBOOK.md:1131-1133` worktree side-effect **(control ii.a)** | `[#353]` | ✓ |
| `PLAYBOOK.md:1485-1487` `worktree remove` silent no-op re-check | `[#4]` | ✓ |
| `PLAYBOOK.md:3456` Codex producer lane charter-only | `[#341]` | ✓ |
| `PLAYBOOK.md:3457` interim producer fallback writes nothing | `[#341]` | ✓ |
| `ESSENTIALS.md:82` worktree side-effect **(control ii.a)** | `[#353]` | ✓ |
| `HANDOFF_PROCESS.md:529-531` serial merge `--no-ff` / teardown | `[#153]` | ✓ |
| `README.md:12-14` hub protocols never copied | `[#314]`/`[#327]` | ✓ |
| `README.md:25-26` consumers hub-pointer | `[#314]`/`[#327]` | ✓ |
| `README.md:26-28` consumer protocols local-marked only | `[#314]`/`[#327]` | ✓ |
| `parity-surfaces.yaml:75-77` `gate_rev_ahead` restriction | `[#342]` | ✓ |

**Borderline, flagged not silently resolved:** the three `README.md` rows cite a *seed-shell*
clause that declares the rule **incomplete**, not specifically **un-mechanised**. Counted as
declared on the ticket test; a stricter reading moves them to silent (N_silent 176 → 179).

**Near-misses that FAILED the test and are therefore counted silent** — each has an on-surface
admission but a closed or absent ticket: `PLAYBOOK.md:3447` (`[#333]` closed) ·
`CONTRIBUTING-md-template.md:70` (`#328` closed) · `HANDOFF_PROCESS.md:441` (`[#164]` closed) ·
`HANDOFF_PROCESS.md:426`, `DEFINITION_OF_DONE.md:79-83`, `DEFINITION_OF_DONE.md:111`,
`AI_COUNCIL_PROCESS.md:183`+`:197`, `AGENT_FRAMEWORK.md:5`+`:46` (no ticket). This is the ruled
test doing exactly what it was chosen to do: prose alone does not buy a rule out of `silent`.

---

## pending-#242 — MUST-rule list (named artifact, excluded from denominator)

**73 MUST-rules across the 7 cluster ADRs. 49 DROPPED in HANDOFF_PROCESS v5.7 · 12 CHANGED · 12
CARRIED. Zero of the 73 has any mechanical enforcement.**

**All 7 declared statuses are STALE — and the supersession vector is v4, not v5.** Six of seven
carry an in-file `Amendment 2026-05-29 — Superseded by v4` marker while their headers still read
`Accepted`. **No document states "superseded by v5" for any of the 7**; v5 (`protocols/HANDOFF_PROCESS.md`)
never cites them — grep returns zero matches. The cluster is only *transitively* superseded
(v3.4 → v4 via ADR-62 → v5 via ADR-82). Confirms the ruling: **the defect is a stale STATUS, not a
silent rule.**

| ADR | Status line (verbatim) | Rules | Dropped | Staleness |
|---|---|---:|---:|---|
| 32 | `**Status:** Accepted` + `**Superseded by:** none` | 11 | 7 | **Worst** — actively asserts non-supersession; no in-file marker |
| 37 | `Status: Accepted` | 9 | 5 | No in-file marker; only PLAYBOOK:2958 calls it "design history" |
| 42 | `Status: Accepted (amended four times…)` | 25 | 17 | **Doubly stale** — header `Accepted`, body says superseded by v4, v4 itself archived |
| 55 | `- **Status:** Accepted` | 6 | 2 | Header/body contradiction |
| 56 | `- **Status:** Accepted` | 5 | **5** | Header/body contradiction; **entire procedure dropped** |
| 57 | `- **Status:** Accepted` | 8 | 7 | Core rule *reversed* by v5 §3 |
| 58 | `- **Status:** Accepted` | 9 | 6 | Header/body contradiction |

**Highest-value DROPPED rules — the risk set for W3 seed 3** (no successor governs them):

- **R55** ADR-56:49-50 — dual-maintenance anti-drift rule; nothing governs prompt-convention drift now
- **R56** ADR-56:51-52 — ≤200-line size budget with an escalation trigger
- **R51** ADR-55:50-52 — operator audit trace; v5 has **no anti-rubber-stamp record**
- **R60** ADR-57:36-37 — `mixed-uncertain` fail-safe → worst-case. **v5's default (`execution`) inverts the safety direction**
- **R70** ADR-58:47 — general confident-claim-requires-verification trigger; only a narrow living-doc analogue (`doc_claims`, WARN-class) survives
- **R63/R64** ADR-57:67-68, :81-82 — no-free-form-additions / expand-only-by-amendment guards
- **R21/R36/R57** — full-invariant bundle copies, **REVERSED** by v5:59-65 (deliberate, not drift)

`ADR-94` explicitly names **`#242`** as the unbuilt "status-flip coherence check" — this exact
defect class is a known named deferral, consistent with the bucketing.

---

## Escalations beyond the enumeration

1. **`ecosystem/parity-surfaces.yaml` misdescribes its own enforcement posture at HEAD.** Header
   `:6` and `:93-94` still declare *"WARN-only v1, zero blocking gates"* / *"the checker never
   blocks"*, and `scripts/fleet_parity.py:131` carries *"never blocks in v1"*. Contradicted by
   `audit.py:1961` (*"a BLOCKING ALL_CHECKS member"*), `ARCHITECTURE.md:192` (*"fail-closed"*), and
   `JOURNAL.md:213` (`[#337]` promotion). The `[#337]` promotion updated `audit.py` and
   `ARCHITECTURE.md` but not these three sites. A reader trusting the header draws the wrong
   conclusion about what a MUST row costs. **Documentation defect at HEAD, not a classification note.**

2. **`protocols/HANDOFF_PROCESS.md:502-503` claims a mechanism that does not exist.** It asserts the
   FILE-BOUNDARY rule is *"the parallelism ruling **made mechanical**"* — no mechanism exists.
   `scripts/boundary_report.py` is a keyword false-friend (fleet CLAUDE.md methodology regions,
   self-declared *"a reporter, NOT a gate… deliberately NOT registered in audit.ALL_CHECKS"*).
   **This is the inverse of ESSENTIALS:82: a silent rule that reads as gated.** Worse than a plain
   silent rule, because it actively misleads.

3. **ADR immutability is prose while its sibling transcript rule is gated.**
   `AI_COUNCIL_PROCESS.md:350` and `claude-regions/critical-rules-records.md:3` assert all four
   classes immutable; `block_immutable_edits.py:83` covers `/docs/decisions/transcripts/` only, and
   the exclusion is declared **only in the hook's source** — never in the protocol.

4. **`DEFINITION_OF_DONE.md:107-109` is expired in place.** Its 4-week freeze window (`~2026-07-14`)
   elapsed before HEAD (2026-07-19) with no successor clause.

---

## Limitations (stated, not smoothed)

- **`docs/decisions/` is deferred** to run 2 per ruling (3). The denominator is the non-ADR corpora,
  which is where the ADR-keyed pass structurally could not reach — but N_silent is a **floor**, not a
  total.
- **Partial mechanisms are folded into `enforced`.** ~55 rules have a mechanism covering one leg or
  an adjacent/narrower subject (e.g. `CONTRIBUTING:34` — the no-direct-to-main half is gated, the
  branch-prefix half is not). A stricter split would move a substantial share of these to silent,
  **raising** N_silent. The reported 176 is conservative.
- **One extractor mis-reported `tests/` as containing 4 files; it holds 69 on disk / 98 tracked.**
  Its mechanism verdicts rested on `scripts/` + `.pre-commit-config.yaml` + `.claude/settings.json`,
  which it did search, so gate-level findings hold — but test-side evidence for the `protocols/`
  rows is thin by search failure, not by construction.
- **Rule-count reconciliation.** The PLAYBOOK extractor self-reported 41 confirmed / 104 none; the
  mechanical parse of its own rows yields 54 / 94. The parse is authoritative for itemisation
  (every row traceable to file:line); the discrepancy is in confirmed-vs-partial labelling, not in
  rule identity. The protocols extractor self-counted 93 rules; mechanical parse of its emitted
  blocks yields 122 (restatements counted at their own file:line, per the ruled unit).
- Counts are **per file:line**, so a rule restated at two canonical surfaces (e.g. the worktree
  side-effect rule at PLAYBOOK **and** ESSENTIALS) is counted at each site, matching the ruled unit.

---

## Disposition — what this census produced

Every follow-up this census named has since landed (2026-07-19):

- **The declaration test** is recorded verbatim in `BACKLOG.md` `[E8]` — commit `45edaf07`. It was transcript-only when this measurement was taken.
- **The baseline** (320 / 176 / 130 / 14, pinned `bf49cbf9`) is recorded in `[E8]`, pointing at this artifact for the evidence.
- **Open decision R12** is filed UNRULED, no recommendation attached: clause (b) is unreachable in one arc at N_silent 176 — narrow the target, or gate the growth.
- **Six tickets** under `[S22]`: `[#357]` run 2 over `docs/decisions/` · `[#358]` parity-surfaces posture self-contradiction · `[#359]` phantom enforcement (P1) · `[#360]` expired scope-freeze · `[#361]` ADR-immutability declared only in the hook · `[#362]` the `#242` substantive guard loss.
- **The educate artifact** for the arc is `docs/audits/2026-07-19-technical-arc5-educate.md`.

Filed, not fixed: `[#358]`–`[#361]` belong to their waves. This artifact is the measurement record, not a remediation record.

---

## Acceptance

| Criterion | Status |
|---|---|
| Every row traceable to file:line | ✓ |
| Controls land correctly | ✓ (i) silent · (ii)b silent · (ii)a **CORRECTED** to declared, per the ruled definition |
| N_silent itemised as a list | ✓ 176 items, §A–D |
| pending-#242 MUST-rule list delivered | ✓ 73 rules, 7 statuses, risk set named |
| Zero commits | ✓ working tree untouched |
| SHA pinned | ✓ `bf49cbf959acf1ca0dfb970b17bf02f34a9862ef` |
| ADR-keyed lookups | ✓ none — all lookups subject-keyed |
| Swallowed errors | ✓ none — `bc` absence failed loudly and was re-run |
