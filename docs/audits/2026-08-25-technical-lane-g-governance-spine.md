# LANE G — governance spine: the R-F1 amendment, eight births, and the F3 ADR draft

**Contract:** `LANE-G-governance-spine.md` (frozen, operator-supplied) · **Serves** `[E4]` ·
**Authority:** `protocols/STANDING_RULINGS.md` section U → `docs/audits/2026-08-25-technical-register-ruling-packet.md` (immutable).
**Branch:** `worktree-lane-g-governance`, cut at `origin/main` `436e7375` · **Commit-and-STOP; not merged.**

## 1. What landed

| # | Commit | Act |
|---|---|---|
| 1 | `cd25cb4e` | **ADR-111 amendment** (in-file marker) — a landed adjudication packet SATISFIES the §2 funnel; two guards. Index note on `docs/decisions/README.md`. |
| 2 | `5252a1c0` | **Eight births** — `tasks/` + manifest placement + `gen_task_tree.py --emit-source`. `BACKLOG.md` regenerated, never hand-edited (ADR-107 §7.2). |
| 3 | `a2e49855` | **ADR-115 (Proposed)** — supersedes ADR-53 D2, amends ADR-101 §1, designed as ONE commit at acceptance. Index row + `gen_claude_rosters.py --write`. |
| 4 | this file | Lane report. |

### 1.1 The amendment (step 1)

An adjudication packet pointed at by `STANDING_RULINGS.md` and carrying a per-row reason
**satisfies** the CANDIDATE → intake → ratification funnel — it is that funnel executed in one
recorded act, not an exception to it. Direct births are lawful **only** under such a packet;
outside one, §2 stands unweakened.

- **Guard (i)** — every direct birth cites the packet row id it derives from, one-to-one
  traceable: row → packet row → reason, one hop.
- **Guard (ii)** — birth rights flow only from a **landed, byte-identical** packet. An unlanded or
  editable packet confers **none**, not reduced ones.

The laundering failure mode is priced by (ii) (a launderer must land an immutable, register-pointed
artifact with a stated reason per row — the same cost as the intake it replaces) and made visible
by (i). **No gate is armed**, deliberately: ADR-111's own n=2 discipline applies to its amendment,
and this lane's births are the first of the two measurements a gate would be argued from.

### 1.2 The eight births (step 2) — guard (i) trace

Packet row ids were derived **from the packet**; the contract deliberately named none.

| Row | Size | Theme / story | Packet row | Packet locator |
|---|---|---|---|---|
| `[#579]` code doctrine & FDD | P1/L | [E2]/[S3] | **C22 + C23** | §3 ARC-A |
| `[#580]` atomic id allocation + SOLE source | P1/M | [E7]/[S19] | **C08 + C09** | §3 ARC-B |
| `[#581]` backlog vitals | P1/L | [E7]/[S18] | **C10 + C11 + C13** | §3 ARC-C |
| `[#582]` substrate router | P1/L | [E7]/[S18] | **C30 + C31 + C32** (+ D-vis) | §3 ARC-D + addendum |
| `[#583]` green-by-skip sweep | P2/M | [E2]/[S3] | **C18** (skip half) | §3 ARC-E |
| `[#584]` CLAUDE.md §10 lockstep + §6/§9 extraction | P2/M | [E5]/[S14] | **C02** | §3 ARC-G |
| `[#585]` `anchor_gate_probe` disposition | P2/S | [E5]/[S13] | **C18** (constant-refusal half) | §3 ARC-E |
| `[#586]` `export_backlog_view` carve-out | P3/S | [E7]/[S18] | **C04** | §3 ARC-G |

Ids allocated `max(tasks/) + 1` = **579**, the synthetic `[#777]` excluded per standing precedent.

### 1.3 ADR-115 (step 3)

`Proposed`. Supersedes **ADR-53 Decision 2**; amends **ADR-101 §1**. The acceptance act is
specified file by file at §4 — nine items, including the exact `SANCTIONED_TIER1_FILES` diff
(**20 → 21**, live size verified) as fenced specification text. **`scripts/` was not edited.**

Criterion **MET**: Codex and Cursor read `AGENTS.md` natively and `CLAUDE.md` not at all, with no
configuration step (R-L matrix, corroborated by an independent matrix 16 days earlier). Gemini CLI
is a third *on a setting* and is not counted; Grok/Copilot/Zed/opencode/Amp read both and fail the
second leg. **DeepSeek is unmeasured at runtime** — PROBE-DSH read shipped source only and found
DSH consumes both files, so it is NEUTRAL — and is named as an open input, never a blocker.

Two of intake #42's three open questions are **closed rather than deferred**: the register is
**subordinate** to a ratified ADR (a ruling may interpret, never contradict — so R-1 did not bind
while ADR-53 D2 stood, which is exactly what the gate demonstrated), and the status token comes
from the **live enum**, not invention.

## 2. Nine things measured, not carried

Each is recorded in the artifact that depends on it, not only here.

1. **`JOURNAL.md:1719`** — the packet's locator for the 777-vs-577 double-bite — **no longer
   resolves** (that line now carries a `[#578]` sentence). `[#580]` cites the entry by anchor text.
2. **`[#429]`**, which ADR-107 names as owner of the concurrent-allocation hole, is **CLOSED**, and
   its Done-when is worktree-provisioning portability. Nothing live owned the hole — which is why
   `[#580]` is a birth and not an ADR-111 OWNED attachment.
3. **`[#433]`** is **CLOSED** too; cited in `refs`, never as a kill-candidate.
4. **`[#270]` is CLOSED and `[#166]` is `deferred`** — both were dropped from kill-candidate
   *values*, since `preflight_backlog_ids` WARNs on a non-open row in that assertion role.
5. **The contract-frozen sweep path is REFUSED by the live gate.**
   `classify('docs/audits/2026-08-25-green-by-skip-sweep.md')` → *"has no CLOSED-enum `<class>`
   token after the date"*. It can only land as `...-technical-green-by-skip-sweep.md`. **Not
   renamed by this lane** — the token is frozen in two lanes — but `[#583]` cites both forms and
   says which the gate admits. **Integrator decision owed.**
6. **"`anchor_gate_probe` pre-existing since 2026-08-22" is itself a carried fact.**
   `docs/audits/2026-08-20-technical-codespaces-audit.md` already records the same test FAIL on
   both platforms and *pre-existing*. `[#585]` says **2026-08-20**.
7. **The ADR-115 enum diff BREAKS a live test by construction.**
   `tests/test_canonical_docs.py::test_validate_hermetization_seals_exactly_the_registry_living_docs`
   asserts the Tier-1 `.md` members are *exactly* the ADR-38 canonical seven. That is the test doing
   its job — it is the organ that stops `AGENTS.md` being absorbed into the canonical set unnoticed
   — so its widening is specified in the same act. **A one-line enum add would have RED-ed the
   suite at acceptance.**
8. **ADR-53 Decision 3 is already discharged, not owed.** `templates/AGENTS-md-template.md` is
   absent from the tree, and `protocols/ESSENTIALS.md` contains **zero** `AGENTS` references.
   PLAYBOOK's two *"single canonical agent-instruction file"* claims **do** need re-pointing and are
   item 6 of the acceptance act.
9. **Intake #42's status-token premise is stale.** It records `Partially superseded` as *"a legacy
   off-enum carve-out, not precedent"*; `docs/decisions/README.md` §"Status enum" declares it, and
   ADR-46/47 carry it verbatim.

## 3. Decision packet (the V-2 batch)

Everything below was decided per contract defaults and batched here rather than asked, per the
lane's decision budget. Three items want an operator or integrator word.

| # | Decision | Basis | Wants a word? |
|---|---|---|---|
| D1 | Branch is `worktree-lane-g-governance`, not the contract's `lane/g-governance` | `lane/` is **not** in the ratified branch-prefix enum (`CLAUDE.md` §4, core-invariant #5); the worktree was already provisioned lawfully. No new prefix invented. | no |
| D2 | ADR id **115** taken, per the contract's "derive the next free id from `docs/decisions/`" | 115 is next-free on disk. **But** `docs/audits/2026-08-19-technical-n3-ratification-pack.md` carries a *provisional* "ADR-115" for an unlanded `done_when` ADR that is **held** ("fork unruled"). That draft must renumber. Flagged rather than silently collided with. | **yes** |
| D3 | `[#583]` and `[#585]` both cite **C18** | A bijection onto packet rows was never available — the packet itself merges C-rows into arcs. The two are scoped as the ADOPT's distinct halves (silent skip vs constant refusal). Stated, not hidden. | no |
| D4 | Arc definitions read from packet **§3**, not §4 | The contract says "section U §4 arc definitions"; the packet's §4 is *Sequencing* and §3 is *The rulings — 37 rows into ten arcs*. | no |
| D5 | The frozen sweep path is left unrenamed and its refusal recorded | Finding 5 above. Renaming a cross-lane frozen token unilaterally is worse than recording the measurement. | **yes** |
| D6 | `[#585]` **narrows** `[#569]` and names it as a kill-candidate | `[#569]` item (A) grouped both standing REDs; its sibling half was discharged at `353149ab` (verified). Proposal only — nothing auto-removed. The alternative (amend `[#569]` instead of birthing) was rejected because the contract's row count is 8 and a grouped row cannot carry an owner. | **yes** |
| D7 | `.claude/generated/recent-adrs.md` regenerated | Outside the contract's three-directory scope, but the `claude-rosters-freshness` hook would otherwise block the commit. Disclosed. | no |
| D8 | This report lands in `docs/audits/` | The Final step instructs a lane report; ADR-101 refuses a root artifact; the UNDERSTAND "failure mode" line names three directories and predates the Final step. Resolved toward the explicit instruction. | no |
| D9 | Intake **#42** stays `READY` | Its terminal flip is **item 8 of ADR-115's acceptance act**, not this lane's — the contract said draft as Proposed and take no execution. | no |

## 4. Deviations from the contract, stated

- **Substrate.** The contract specifies the Codespaces devcontainer. This lane ran on the local
  Windows workstation with gates armed (`arm_hooks` self-arm confirmed at session start; every
  commit passed the full pre-commit set). No gate was skipped and `--no-verify` was never used.
- **`docs/decisions/README.md`** was edited three times (the ADR-111 amendment note, the ADR-115
  index row). It is inside the permitted `docs/decisions/`.
- Nothing under `scripts/`, `ecosystem/`, `protocols/`, `CLAUDE.md`, `templates/` or any Form-A
  region was touched. No ninth row was born. ADR-114 was not opened.

## 5. Validator evidence

Run at `a2e49855` (tip before this report), every command through the locked env per ADR-106.

```
$ uv run --locked python scripts/validate_backlog.py BACKLOG.md
WARN  user story with no tasks - story "[S24] Declare desired state once, as data, inste" line 438
validate_backlog: OK (9 themes, 26 stories, 191 tasks, 1 warning(s))
    -> the [S24] WARN is pre-existing; that story is marked COMPLETED 2026-08-01.

$ uv run --locked python scripts/gen_task_tree.py --check
gen_task_tree: check ok

$ uv run --locked python scripts/validate_doc_claims.py
validate_doc_claims: OK - 4 claim(s) checked, no prose drift
         skipped  audit_check_count (doc - / actual <ground truth unavailable>)
           match  precommit_hook_count (doc 21 / actual 21)
           match  precommit_hook_roster (21 / 21)
           match  pytest_collected (doc 3949 / actual 3949)
    -> the `skipped` leg beside an OK header is the green-by-skip defect itself,
       reproduced live; it is [#583]'s seed instance, not this lane's regression.

$ uv run --locked python scripts/audit.py health
[OK]  preflight_backlog_ids: every kill-candidates assertion names an open row
[~~]  adr_status_grammar: 88 ADR status field(s); 0 enum/single-field defects;
      baseline WARNs: coherence=3, duplicate-id=2, grammar=47, wrapped-value=1
health: OK
    -> 87 -> 88 status fields is ADR-115 entering the corpus; grammar WARNs held at
       47, so the new status line is clean. All other WARNs (29 funnel_coverage,
       review_artifact_coverage, journal_spine_anchor by-mention) are the pre-existing
       baseline and predate this branch.

$ uv run --locked python scripts/validate_adr_status.py
    -> ADR-115 resolves `Proposed` with no coherence and no UNINDEXED defect.

$ uv run --locked pytest -p no:randomly -n 0 \
    tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent \
    tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export
1 failed  assert 'absent' == 'enforcing-local'  (pre-push organ REFUSED an anchored push too)
1 failed  the export is read by governance: ecosystem/conformance.{html,md} reference
          'export_backlog_view'
    -> both reproduce at origin/main 436e7375; neither is this lane's work. They are
       [#585] and [#586].

$ git push -u origin worktree-lane-g-governance
Block direct-to-main / FF push to main (#153 prevent - core-invariant .......... Passed
Block a push to main carrying an unanchored spine entry (ADR-85 amend.) ........ Passed
```

Every commit passed the full pre-commit set (`audit-health` included). `--no-verify` was
never used and no `SKIP=` was set. The full suite was **not** run in-lane: per PLAYBOOK
Ch5 / `[#528]`, a lane runs the targeted files covering its diff and the full suite runs
once at integration. This lane's diff adds no code, so its targeted set is the two REDs
above plus the validators.

## 6. What is NOT done, and who owns it

- **ADR-115 is `Proposed`.** The acceptance act is specified, not executed; it is a follow-up after
  adversarial review. `scripts/validate_hermetization.py` still refuses `AGENTS.md`.
- **No `AGENTS.md` exists.** `[#577]`.
- **`CLAUDE.md` §10's false anti-pattern still stands** — a fourth consecutive version. `[#584]`
  now owns the two-site act; this lane was barred from Form-A regions and did not take it.
- **Both suite REDs remain RED.** `[#585]` and `[#586]` own the dispositions; neither is this
  lane's work and both reproduce on bare `origin/main`.
- **The branch is pushed and NOT merged.** Integration is a separate session.
