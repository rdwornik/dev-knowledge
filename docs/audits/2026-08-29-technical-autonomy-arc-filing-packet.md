# FILING PACKET — 2026-08-29 side-session, items 4 + 5

**Status: RECONCILED, NOT LANDED.** The reconcile-before-birth is complete and is below. The
in-repo landing is **deferred on a measured collision**, per the operator's own instruction
(*"if any item collides with a running lane, defer it and say so"*).

## WHY DEFERRED — measured twice, 2026-08-29. The reason CHANGED mid-session; both are recorded.

**Measurement 1 — at the start of this session (the night-batch-2 merge queue, mid-flight):**

| Fact | Measurement |
|---|---|
| `main` vs `origin/main` | **40 commits ahead** — the whole wave-2 queue merged **locally and unpushed** |
| Unpushed spine | 8 lane merges (H, I, J, K, L, M, N, O) + `docs/batch-2-w2-integration` |
| Worktrees standing | **8**, at `.claude/worktrees/lane-{h..o}-*` — teardown had not run |

**Measurement 2 — later in the same session. THIS COLLISION HAS CLEARED:**

| Fact | Measurement |
|---|---|
| `main` tip | `3345d303` *"the wave-2 anchor discharge (B6, append-only) + the single regeneration pass"* |
| `main` vs `origin/main` | **0 — pushed** |
| Worktrees standing | **0** (primary only) — teardown complete |

**But a second, different collision is live, and it is why the landing still waits:** two sessions
are currently active in the **primary checkout** — `962c3716` (this session's own `THESIS-COMPARE`
lane, dispatched deliberately **without** a worktree so it would not perturb the night mission's
tree) and `a0d31a41`. Branching in the primary checkout swaps HEAD underneath both. That is the
recorded failure mode *"concurrent session swaps HEAD in primary — check live sessions before
branching."*

**Nothing below is blocked by a decision; it is blocked by a clock.** Land it when
`THESIS-COMPARE` has written `~/Downloads/THESIS-COMPARE-OUT-2026-08-29.md` and no other session
holds the primary checkout.

**Everything below is decision-ready.** Amend-vs-birth is decided per item, each names its funnel
home, and every blocker that would bounce it at triage is named with its locator.

---

# ITEM 4 — the four filings

## (a) PROMPT DISTILLER → **AMEND. The folder the operator remembers is REVOKED, not lost.**

**FOUND — and it is both an intake and a folder.** Root `prompts/` was created and then revoked:

- `c57aeada` (2026-08-25) — *"feat(prompts): prompts/<date>/ — a batch's launch inputs become
  committed evidence"*. Landed `prompts/2026-08-25/` with five contracts byte-identical, and added
  `SANCTIONED_TIER1_DIRS += "prompts"` + `_HOME_PATTERNS += "prompts/*"`.
- `23409c9c` (2026-08-26) — *"relocate batch-1 launch contracts out of the revoked root `prompts/`"*.
  **Operator ruling: "root is sacred."** All five moved to
  `docs/audits/2026-08-25-technical-batch1-launch-contracts/`.

**The live successor home is already ruled** — `protocols/PLAYBOOK.md` heading *"Where the contract
file lives — two homes, one of them in the tree"* (`:2657-2683`): operator-side
`$env:CLAUDE_PROMPTS_DIR` (default `~\Downloads`), in-tree
`docs/audits/<date>-technical-<batch>-launch-contracts/`, copied byte-identical. `:2671-2676`
states root `prompts/` is **REVOKED** and *"Rule A refuses it if recreated."*

> **A birth proposing `docs/prompts/` re-opens a settled operator ruling and will be refused by the
> ADR-101 hermetization gate.** This is the single most important thing to carry forward.

**Funnel home: AMEND `docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md`
(intake #29, `status: ACCEPTED`).** It already owns both halves:
- **S1 `:23`** — *"the lane/arc contract template gains a SUB-AGENT ROUTING section —
  retrieval/reads/greps → haiku; bounded edits + gate runs → sonnet; design/judgment/review → the
  main opus thread."* That is the tool-plan half, already ratified.
- **S3 `:27`** — the distillation engine, **MEASURE-FIRST**.

**BLOCKER — cite it or triage bounces the whole thing.** Intake #29's S3a MEASURE-FIRST
precondition is `decided-by` operator ruling and **binding** (`:5`, `:48`): *"Building (c) before
(a) is out of scope by this intake's own text."* A distiller engine built before the
instrumentation data exists is refused by ratified text.

**Second blocker, evidentiary:** `docs/intake/2026-08-01-func-distillation-and-library-first.md`
(SEED) `:32-34` records that **repomix measured 0% compression on markdown** and the paste-budget
half was **rejected on evidence**. Do not re-litigate it.

**Genuinely uncovered (the amendment's actual content, three narrow deltas):**
1. Extend the ruled launch-contracts home to **non-batch** (single-lane / interactive) distilled
   prompts — the current home is *per-batch by construction*. This is the operator's "persist the
   final distilled prompt" ask, in the shape the tree will accept.
2. **Skills/commands/subagents columns** in the lane contract. `scripts/gen_lane_contract.py`
   carries Model/Mode/Effort only (`:189-196` `_ROUTING_ROW_RE`; `:92-93` `MODEL_ENUM`).
3. **An organ** that compiles intent → tool plan. `ADR-56-prompt-generation-card.md` (Accepted)
   keeps that authority *in the browser chat, as a human-followed card* (`:34-46`: classify task →
   choose model/mode/effort → fill skeleton → validate). No organ does it.

Also live and relevant: `tasks/509` (the `<PROMPTS_DIR>` token reaches `claude --bg` unexpanded),
`tasks/389` (prompt-lint over ADR-87's five architect fields; its honest limit — *an off-repo
prompt pasted into a browser cannot be gated by a repo hook* — is **unruled** and is exactly the
question a distiller forces).

## (b) COMMANDS + SKILLS LIBRARY → **AMEND. And the drift claim is FALSE — file it as NOT-REPRODUCED.**

**The `/handoff-verify` v5 claim does not reproduce.** `.claude/commands/handoff-verify.md` cites
**v6 consistently and never cites v5**:

```
  3: … the v6 one-round-trip boot (HANDOFF_PROCESS §5)
  6: Run the entire live comprehension gate for a **v6** handoff bundle in one pass
  7: … This is the CC side of the v6 …
 10: **Pre-v6 bundles are EXEMPT, not failed.**
 19: Source of truth: protocols/HANDOFF_PROCESS.md §5
102: | P0a / P0b / P0c | … v6 bundles only — n/a on a pre-v6 bundle. |
```

Live process: `protocols/HANDOFF_PROCESS.md` — `# HANDOFF_PROCESS v6`, `Version: 6.3.0`,
`Status: stable`, `v6 cut 2026-07-31`. **There is no `handoff-verify` skill** — it is a command
only, single copy, no stale plugin duplicate.

**Do not mis-file these as drift:** `.claude/commands/handoff.md:59,61,63,100-101,119` name a
**lineage** (*"The v5 lineage is the default flow"*) and a **template directory**
(`templates/handoff/v5/…`), not a version claim. Correct by lineage.

**Funnel home: AMEND `tasks/412` + `protocols/STANDING_RULINGS.md` T-13.** `tasks/412`
(`status: closed`) is the closest prior object and its Done-when is item (b) almost verbatim:
*"a `docs/audits/<date>-technical-*` artifact captures Anthropic's published command/skill set with
a per-item fleet-adoption verdict."* It **closed by DEFERRAL, not delivery** — T-13 `:2226-2240`:
*"Deferred because its two halves have owners that are not this row."*

**BLOCKER:** T-13 `:2229-2233` rules routing doctrine an **L0 question** (`~/.claude/ROUTING.md`,
outside this repo); a PLAYBOOK doctrine would be *"a third authority over a table the hub does not
hold."* **A census is description, not routing authority — say so explicitly, or T-13 kills this
the same way it killed #412.**

**Genuinely uncovered:**
1. **Anthropic-shipped organs are outside every census.** `ecosystem/organ-index.md:4-7` enumerates
   its sources (`.claude/{agents,commands,skills,workflows,rules}`, `settings.json`,
   `.pre-commit-config.yaml`, plugin manifest, DECLARED L0 rows) — **none reaches** `dataviz`,
   `artifact-design`, `code-review`, `simplify`, `loop`, `schedule`, `claude-api`, deep research.
   Current coverage, generated: *"55 organs across 8 classes — agent 3 · command 12 · skill 3 ·
   workflow 1 · rule 2 · session-hook 12 · git-hook 21 · plugin 1."*
2. **Usage ranking.** The index columns are Name/Class/Trigger/Source/Distribution/Status — no
   invocation count. The one artifact that ever had a *"Used in practice?"* column
   (`docs/audits/2026-05-17-skills-hooks-usage-review.md`) is hand-written and badly stale (lists
   retired `/boot`, `/evolve`).
3. **Overlap dedupe.** Nothing computes command↔skill overlap.

## (c) CLOUD MONITOR → **PREMISE CORRECTED TWICE. Amend [#610]; the organ is a win-tooling birth.**

**Correction 1 — `Harvest-Cloud` EXISTS. The repo's own audits are stale.** Probed live on the
operator host, 2026-08-29:

```
Harvest-Cloud -> Alias : Save-CloudSessionReport
Save-CloudSessionReport [Function] from module DispatchHelpers
module: ~\.dispatch-helpers\Modules\DispatchHelpers\DispatchHelpers.psd1
```

Three repo artifacts say otherwise and are **now stale**:
`docs/audits/2026-08-27-technical-night-harvest-consumption-ledger.md:32` (*"`Dispatch-After` and
`Harvest-Cloud` as its two missing verbs"*), `2026-08-28-technical-batch-2-manifest.md:145`
(*"Harvest-Cloud is half extraction, half new"*), `2026-08-28-technical-nb2-c-packet.md:262-263`.
**`[#610]`'s done-when may already be half-discharged** — verify `Save-CloudSessionReport` against
the row's *"a usage line and its API surface recorded"* before doing any work. Audits are immutable;
the correction rides the amendment, not an edit.

`Get-CloudSession` is likewise live (18-function export incl. `Get-CloudSessionRecord`,
`Get-CloudSessionBinding`, `Invoke-CloudApi`). **Both this session's cloud lanes were dispatched
with these verbs and returned G1/G2/G3 receipts** — that is the witness.

**Correction 2 — there is NO existing monitor to extend.** `grep -rn -i "monitor" tasks/` returns
**zero**. The four things carrying "sentinel" (`changelog_sentinel.py`, `billing_leak_sentinel.ps1`,
`surface_triage.ps1`, `fleet_health.py`) are **single-shot SessionStart tripwires, not pollers**;
none knows about cloud sessions. `~/.claude/night-agent/` has no poll/monitor/watch reference.
**The item's word "extend" does not describe an available act — this is a birth.**

**Funnel home: AMEND `tasks/610` (`status: open`, P2/M)** — the carrier row, whose done-when already
names both verbs — with the requirements spine at
`docs/intake/2026-08-27-tech-night-batch-protocol.md` (intake #60, **`status: READY`**), which
already names the five phases *"dispatch, **sentinel**, harvest, manifest, morning adjudication"*
(`:32-33`) and carries the sentinel as a **`Could:`** (`:72-73`).

**HARD BOUNDARY — where the organ may live.** Intake #60 `:98-99` **Non-goals**: *"Not a hub script.
The two verbs are win-tooling, operator-owned — a hub script that drives state elsewhere would
breach the Layer-2 invariant."* A poller in `.dev-knowledge/scripts/` **violates Critical Rule #4**.
It belongs in `win-tooling`, with a hub-side *requirements* row — exactly the shape `[#610]` already
has.

**Open question the birth must answer, already filed** — intake #60 `:118`: *"Is the sentinel worth
building at all, given last night needed no second sleep? One clean night is n=1."*

## (d) AUTONOMY ARC umbrella → **the fuzzy deferral has NO funnel carrier. Highest-confidence birth in the sweep.**

**The operator's mapping is CONFIRMED and exact.**
`docs/decisions/ADR-81-feature-lifecycle-definition-of-done.md:45`, Amendment 2026-06-24, heading
**"Scope — deterministic only; fuzzy deferred"**:

> *"This binds **deterministic build tasks**, where 'done' can reduce to an exact, executable
> assertion. The **fuzzy band** — decks, prose, judgment artifacts where closure cannot be an exact
> pass/fail — is **explicitly deferred to its own arc** (it needs a different, non-binary acceptance
> shape). Naming the deferral here keeps it honest rather than silently over-claiming."*

**And the consultation link the operator asserts is explicit in the record** —
`docs/handoffs/2026-06-25-dev-knowledge-architect/SUPPLEMENT.md:135`:
*"**The one confirmed Council candidate remains the fuzzy acceptance-contract arc (§4)** — that is
where multi-model divergence is real."* (`:74`: *"Fuzzy acceptance-contract arc (deferred from A2) —
semantic done-criteria vs deterministic gates. Its own arc."*)

**THE FINDING: the deferral is held by no funnel object.** `fuzzy` appears in ADR-81, ADR-85,
PLAYBOOK `:3267`, `DEFINITION_OF_DONE.md:192`, `HANDOFF_BOOT.md:69`, and 15 immutable handoff
bundles — and **zero times in `tasks/`, `tasks/manifest.json`, `BACKLOG.md`, or `docs/intake/`**.
It lives only in an ADR body, three protocol restatements, and frozen bundles. It is the
no-carrier class already named by `tasks/548`, `tasks/549`, `tasks/550`.

> **This is the amend target the operator asked for — and the honest finding is that there is
> nothing to amend. Amending ADR-81 is not available: ADRs are immutable but for the status line
> (ADR-94). So the correct act is to BIRTH the carrier the ADR's own words promise ("its own arc"),
> transcluding ADR-81`:45`, `HANDOFF_BOOT.md:69`, `PLAYBOOK.md:3267`, `DEFINITION_OF_DONE.md:192`
> and the Council-candidate line above. Birth on a proven gap — this is the proof.**

**The other three legs — AMEND, do not birth:**

**Boot inversion ("plan?" → proposal): AMEND `docs/intake/2026-07-25-tech-consolidation-decision.md`
(intake #17, `status: ACCEPTED`, `disposition: active`).** Its §5 `:158` already carries the exit
test, falsifiable and ratified:

> *"a fresh session boots and its FIRST message quotes the top-5 ready-set with rationales + every
> ruling overdue > 8 days, zero operator memory involved."*

§4 `:140-148` carries the scoring machinery (`score = (priority + alignment + age_boost) / effort`
on Fibonacci; `unblock_count` **its own column, never folded in**; sticky operator override).
`docs/intake/2026-07-30-tech-browser-architect-orientation.md` (#21) `:94` measures **all of that
mechanism as ❌**. **The test exists and is accepted; the organ does not. File the carrier for #17's
exit test — not a new requirement.**

**Planner organ (funnel-health → drafted batch): genuinely uncovered, but bounded.**
`governance_health.py` *renders* (and **computes none of FM-4's four fields** — enforced by
`tests/test_governance_health.py::test_no_fm4_owned_field_is_derivable_from_this_module`);
`funnel_lifecycle.py` *validates* (and states *"EXTENDS THREE EXISTING ORGANS, RIVALS NONE"*);
`[#581]` (P1/L, open) *measures*; `[#574]` *emits a manifest for an already-decided batch*.
**Nothing drafts a batch from health numbers.**

**Consultation-with-weights: AMEND ADR-95 / intake #7 — weights are undefined anywhere.**
`ADR-95-ai-council-query-lane-split.md` (Accepted) `:20-23` rules the split (architect frames *"the
evidence to weigh"*, CC mechanically expands) and `:29` is **record-only** — *"it does not build the
`/council` wiring."* The only "weights" precedent in the whole decision corpus is
`ADR-89:78` (*"not fixed weights"*). Nothing defines weighted consultation.

**BLOCKERS for the umbrella — all five, with locators:**
1. `docs/intake/README.md` §8 `:314-315` — the nightly loop is **gated on the load-gauge landing per
   standing operator ruling**. *Conflicting evidence:* `tasks/270` is listed live, but `tasks/117`'s
   body records *"peg #270 MET at `7e4d503e` … closed at `679d8eca`."* **Resolve which reading
   governs before asserting the gate is clear.**
2. Intake #8 `:15`, `:67` — *"it **never gains new autonomy** — judgment sleeps with the architect."*
3. `[#600]` — an unbounded boot-time classification sweep is **already refused** by
   `HANDOFF_PROCESS.md` §5 condition 4. A boot proposal must be bounded (the top-5 shape, not "every
   open item").
4. `[#488]` (closed) — the ranking axis is **research-first, build-after-ruling**; and its
   sum-not-product ruling binds any weighting scheme (`#17:146`: *a product of three estimated terms
   compounds error and lets one low estimate zero an item*).
5. `[#271]` **RE-CUT 2026-08-28 (K4): the charter half is STRUCK** — *"Carrying a rival charter
   beside a live one is how two protocols drift."* Its §6 constraints travelled to intake #60.
   **Filing a second planner charter beside #60 is exactly the drift that re-cut just removed.**

---

# ITEM 5 — CLAUDE-MD-REVIEW-2026-08-29.md as consumed evidence

**Source:** `~/Downloads/CLAUDE-MD-REVIEW-2026-08-29.md` (3,445 B) — Layer-1 architect review of
CLAUDE.md v2.68, produced at the operator's request (*"very low quality — propose"*).

**It names its own funnel home, and that home is correct:** *"Evidence FOR the
doctrine-consolidation arc (next window's first ruled arc, prior-seat mandate §6 + operator ruling
'no single-file folders' + codex fold). **Not a new birth**; this file is consumed by that arc's
contract and archived when the arc closes."*

**Destination:** `docs/audits/` — the evidence zone. Filename must carry an enum class from the
**closed 11-class enum** (`scripts/validate_hermetization.py:135` `AUDIT_CLASS_ENUM`; Rule B blocks
an off-grammar or off-enum name at commit time). Grammar `<date>-<class>[-<slug>]`. Resolve the
exact class token against the live enum at landing time — do not guess it from this packet.

**What it carries (five findings, each with an in-file witness):**
- **E1 GAMED PROXY BUDGET** — header claims *"≤200 lines"* and §12 records *"closes 196/200,
  headroom 4"*; the physical file is **240 lines / 39,147 B**, one v2.68 history bullet being
  ~3.5 KB. *"Line count is satisfied by density; the real boot cost (bytes/tokens, paid EVERY
  session start) is unbudgeted."*
- **E2 CHANGELOG IN A BOOT FILE** — §12 already condenses v1.0–v2.67 to git *"per ADR-49/65
  (info-preserving)"*, proving the file rules that git IS the history — *"yet each new version
  re-inflates."*
- **E3 DUPLICATION AGAINST ITS OWN §10** — §7–§9 carry per-hook essays **while** pointing at
  *"Full live organ inventory → ARCHITECTURE.md Ch2"*. Pointer + full text violates §10's own
  anti-pattern.
- **E4 MIXED AUDIENCE** — imperatives interleaved with archival rationale.
- **E5 WHAT MUST SURVIVE** — the region mechanism, the generated `@imports`, the `@AGENTS.md`
  portable split (ADR-115), and **AGENTS.md itself as the genre exemplar**.

**Target shape it proposes** (operator cuts): CLAUDE.md becomes a thin Claude-runtime boot contract
— §1 first-read, §2 identity + `@AGENTS.md`, pointers, `@imports` of all generated rosters, §10
imperatives — **budgeted in BYTES with a gate, reusing [#577]'s byte-cap test pattern**. §12 removed
entirely (git carries it); §7–§9 prose collapsed to the generated roster + Organ-map pointer.
**Every removal is a relocation with a named destination, per the operator's no-deletion rule.**

> **This dovetails with a gap [#577] already left open, recorded in CLAUDE.md §12 v2.68:** that
> lane measured the combined global+root payload at **9,161 B = 28.0 % of the 32 KiB cap** but
> its done-when's *test* was outside the lane's write-scope — *"the byte figures are measured and
> reported but **unguarded by a gate**; handed to the integrator as a candidate."* E1's proposed
> byte gate is that candidate's natural home.

## THE OPERATOR RULING TO CARRY — verbatim intent

> **The master's thesis is the NORTH STAR input for the AUTONOMY arc design (library-first, TDD,
> measured spectrum). Cite it in that arc's contract.**

This ruling binds the AUTONOMY arc contract (item 4d above), not the doctrine-consolidation arc.
It is recorded here because this packet is where both were filed. **The three lanes dispatched
2026-08-29 exist to serve it**: `THESIS-COMPARE` (local, the north-star read itself), `AUT-R1`
(cloud, orchestration survey), `AUT-R2` (cloud, decision-quality frameworks). Their artifacts are
the arc contract's evidence base and should be cited in it alongside the thesis.

Note the honest tension the arc contract must resolve rather than paper over: **"TDD" is a
build-arc standard here, not a blanket mandate** — ADR-108 §B binds every build arc to RED-first
witnesses, but Council **rejected "Mandatory TDD"** (`protocols/ENVIRONMENT.md` Rejected list) and
nothing reinstated it. Say partial where it is partial.

---

## LANDING CHECKLIST — mechanical, once the queue drains

1. Confirm the collision has cleared: `git rev-list --count origin/main..main` is 0 (or the arc is
   pushed), and `git worktree list` shows no `lane-*` trees.
2. Branch off `main` — `docs/` prefix. Never commit direct to main.
3. Item 5: land the review into `docs/audits/` under a name whose class token is verified against
   the live `AUDIT_CLASS_ENUM`. **Do not regenerate the audits index** — `[#590]` narrowed that
   hook; leaving it stale is correct for a non-integrator lane.
4. Item 4: amend the four named objects. Intake status edits need **two generators**
   (`gen_intake_index.py`, `gen_intake_tree.py`) — only one is gated.
5. A commit that ADDS a backlog id carries a flush-left `kill-candidates:` line; one that closes an
   id carries `[#id]`.
6. `uv run --locked python scripts/audit.py health` before pushing. Expect the known
   `silent_rule_ratchet` zero-headroom behaviour on any `protocols/` doctrine edit.
