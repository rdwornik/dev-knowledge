# 2026-06-21 — OPS + TASK layer audit (BACKLOG · CLAUDE · CONTRIBUTING · VISION · LESSONS)

> **Run:** overnight worktree audit (`claude -w audit-ops`), Opus, max effort.
> **Branch:** `feat/audit-ops` (off `main` `dec7726`). **Merge-back is OWED** — operator merges `--no-ff` from the primary after review; nothing reached `main` unsupervised.
> **Mode:** auto-apply mechanical currency fixes (committed + logged in §1); PROPOSE everything that removes / condenses / restructures / touches a rule (§§3–6).
> **Source of truth:** `JOURNAL.md`, read in full (artifact-reader full pass + targeted re-reads) + the deterministic `git log`/`audit.py` signals. Every claim below carries its verify command.

---

## 0. Headline

- **BACKLOG closure reconciliation is CLEAN.** No done/closed item is wrongly still listed. `#199`, `#196`, `#197`, `#193`, `#179` correctly left the file; `#153` is correctly present + open; the only two `closes`-tag hits still in BACKLOG (`#5`, `#77`) are the **known false-positives** (verified, do **not** remove — §3e).
- **Two mechanical currency fixes auto-applied** (CLAUDE.md §11/§7 groom + restamp; CONTRIBUTING Validators table 8→10) — §1.
- The backlog was **groomed 2026-06-18 + reconciled 2026-06-20**, so it is fresh; the prune opportunity is **condensation + a small verify-and-close set**, not a pile of stale items (§3). Next quarterly groom is **2026-07-01** — this doc is its decision input.
- LESSONS: **3 entries proposed** (§4), incl. the operator-named worktree + disposition-discipline lessons. CLAUDE §12 itself is now a `doc_rot` WARN — **condensation proposed** (§5). Cross-domain drift flagged, not fixed (§6) — chiefly `protocols/ENVIRONMENT.md` is badly stale.

---

## 1. Auto-applied mechanical fixes (committed on `feat/audit-ops`)

| Commit | File | Fix (verifiable reconciliation) |
|--------|------|---------------------------------|
| `4f4dd1a` | `CLAUDE.md` | **§11 "last 5 ADRs" rotated 76–80 → 85–89** after a genuine read of ADR-85..89 (ADR-88/89 annotated **Proposed**, not "binding"). **§7 reconciled to the live command dirs** — added repo-level `/changelog-review` + `/override` (the deferred ADR-85-escape entry) and plugin `/ship`; synced §8. **Stale version comment** `2.19` → `2.21` (a v2.20 §12 entry had landed without bumping it). `last_reviewed`/footer/version restamped 2026-06-21; §12 v2.21 entry added. |
| `d5bcddb` | `CONTRIBUTING.md` | **Validators table 8 → 10 hooks** — added `coherence-nudge` (commit, non-blocking) + `block-ff-push` (pre-push, #153), which the live `.pre-commit-config.yaml` carries and CLAUDE §9 already listed. `last_reviewed` restamped 2026-06-21. |

Both pass `audit.py health` (`canonical_freshness` GREEN). *Note:* the CLAUDE.md groom left the file at **201 lines** (its header claims ≤200) and §12 at **23 entries** (a `doc_rot` WARN) — both are evidence for the §5 condensation proposal, not separate defects.

**Not auto-applied to BACKLOG/VISION:** no purely-mechanical, content-preserving BACKLOG text fix exists that isn't a judgment call (the recent groom left the text current); VISION is fresh (`last_reviewed` 2026-06-19) with no mechanical gap. All BACKLOG changes are proposals below.

---

## 2. BACKLOG ↔ JOURNAL closure reconciliation (the brief's priority) — method + result

**Deterministic check** (`git log --grep 'closes [#'` across all HEAD ancestors ∩ open BACKLOG ids):
only **#5** and **#77** intersect. Both are the standing false-positives:

- **#77** — BACKLOG already carries `[CLOSURE-VOIDED 2026-06-09: … 77e5d7d closes [#77] was a misattribution — shipped CONTRIBUTING→v4, not this work]`. Genuinely **open** (content-consolidation work). The `audit.py git_backlog_drift` WARN on it is expected.
- **#5** — `closes [#5]` exists off the first-parent spine (a false-positive STRONG hit). JOURNAL 2026-06-19 (`line 226`): *"Closing #5/#77 (false-positive STRONG hits — review-closures-verify-strong-content discipline held)"* — declined at `/review-closures`. Genuinely **open**.

**Verify:** `git log --grep 'closes \[#5\]'` / `'\[#77\]'` then `git show <sha>` — confirms misattribution, per the *review-closures-verify-strong-content* memory.

**One artifact-reader lead chased to ground (the verify-at-source win):** the JOURNAL's 2026-05-28 *"Closed BACKLOG #4"* (`line 2945`) refers to a **different item under the pre-2026-06-01 numbering** — the *AI Council runbook* ("AI Council Flow operationalization"), which IS done (`protocols/AI_COUNCIL_PROCESS.md` exists). The **current** #4 = "Build lessons-index.json + SessionStart retrieval + CLI query": `lessons-index.json` **does not exist**, there is **no `closes [#4]` tag**, and JOURNAL `line 2334` treats it as not-yet-built. **#4 is genuinely open.**

**Result: no done-but-still-listed item.** Every other `closes`-tagged id is gone from BACKLOG. Shipped items correctly left.

---

## 3. BACKLOG prune / condense proposal — **CENTERPIECE** (PROPOSE-ONLY; no item auto-removed)

> The no-remove invariant is absolute here. Nothing below was removed. Each is a candidate with evidence + a recommended disposition for operator ratification (or the 2026-07-01 quarterly groom).

### 3a. Condense candidates — `audit.py doc_rot` WARNs (history-accretion bloat)

These are flagged by the repo's own checker. Condensing = removing/rewriting content → operator-gated.

| Item | Size | Signal | Recommendation |
|------|------|--------|----------------|
| **#164** | 1583 chars | `doc_rot` (>1200) | Heaviest task in the file. The v5-machinery detail (four-file bundle spec, ADR-83 LIVE constraint) reads like a spec dump. **Trim** to the done-when + a pointer to `HANDOFF_PROCESS.md §2–§10/§13`; the spec belongs in that file, not the ticket. |
| **#134** | 1550 chars | `doc_rot` + retired-token *self-trip* | The 2026-06-07 "n=1 field-run design input" block is a mini-essay. **Trim** the design-input paragraph to its 3 signals + cadence; the rationale is in git/JOURNAL. (The `/boot`,`/evolve`,`AGENTS.md` token hits are **self-reference** — it's the grooming item quoting the tokens its own grep hunts — *not* staleness.) |
| **#77** | 1002 chars | `doc_rot` (3 dated blocks) | Carries the full CLOSURE-VOIDED forensic note. **Trim** to "re-scoped to content-consolidation; 77e5d7d closure voided (see git)". |
| **#10** | 931 chars | `doc_rot` (3 dated blocks) | See 3b — likely **closeable**, which dissolves the bloat. |

**Risk:** trimming a ticket can drop a load-bearing constraint (e.g. #164's "ADR-83 LIVE: v4.4 stays canonical"). Each trim must preserve the done-when + any hard gate; do it as a net-negative-char edit (per the §4 disposition-discipline lesson). **Do not** let any trim *raise* another task over threshold.

### 3b. Verify-and-likely-close (state shows the work effectively done)

| Item | Evidence work is done | Recommendation |
|------|------------------------|----------------|
| **#10** (TOKEN-LOG doc refs → HANDOFF_PROCESS §14) | Done-when (a): `PLAYBOOK.md:2689` points cadence to `HANDOFF_PROCESS.md §14` (#152). Done-when (b): CLAUDE.md + ARCHITECTURE.md name `logs/TOKEN-LOG.md` consistently (verify: `grep -n TOKEN-LOG CLAUDE.md ARCHITECTURE.md`). | **Spot-check the 11 PLAYBOOK `TOKEN-LOG` refs** for any stale "PLAYBOOK §8" cadence pointer; if none, **close #10** (done-items-leave). |
| **#47** (classify corp-knowledge-extractor / corp-by-os / corp-rfp-agent) | All three are **absent from `ecosystem/index.yaml`** (registered repos = the 5 live ones). Origin 2026-05-11. | Classification is effectively "**uncloned/dropped**" (not in the ecosystem). Operator confirms → **close #47**. |
| **#35** (self-owned low-sev cleanups) partial | The "VISION stale `last_reviewed`" sub-part is **moot** — VISION `last_reviewed` is now 2026-06-19 (fresh). | **Re-scope:** verify the ARCHITECTURE diagram-attribution + SBAR-label + VISION adoption-signal (WF-3 / GO-1/2) against the current files; close the resolved parts, keep only any genuine residual. The original `coherence-audit` WF-3/GO refs are old — confirm they still mean anything. |

**Risk:** low — these are confirm-then-close. The only risk is closing #10 while a stale PLAYBOOK cadence pointer remains; the spot-check covers it.

### 3c. Aging decision-items for operator judgment (P3; age + low signal, NOT deterministic kills)

Per the #134 grooming design, age alone never kills — these are surfaced for a yes/no, not proposed for removal:

- **#42** — "decide whether mermaid-theme check #7 expands beyond ARCHITECTURE.md." A scope **decision** that has sat since the durability audit. Operator: extend or accept-as-is → either way it closes.
- **#37 + #39** — both gated on a **"Move 2 structural split"** and on #158 (now **closed**). Verify the Move-2 dependency is still a live plan; if it was abandoned, #37/#39 should be re-scoped or closed, not left blocked on a dead gate.
- **#67** — "PLAYBOOK §7 polish (skill/command naming note)." Low-value polish, origin methodology-audit C10/C12. Keep or drop.

**Risk:** none from listing; these need the operator's intent, which the repo can't supply.

### 3d. Overlap to adjudicate (not proposed as merges — flagged for a call)

- **#169 ↔ #171** — #169 (ungated-doc staleness signal) explicitly "rides with" and `depends-on` #171 (build `ecosystem/conformance.md`). Tightly coupled (ADR-85 R2 / ADR-86). **Option:** fold #169 into #171 as a sub-deliverable, or keep as the build + the signal. Operator call.
- **#157 ↔ #190** — related but **distinct** (specific CLAUDE §4/§5 instance vs the general intra-file dup detector, ADR-88/#140 lineage). **Keep both** — noted so a groom doesn't mistake them for duplicates.

### 3e. Do **NOT** remove — verified false-positives / known dispositions

- **#5, #77** — false-positive `closes` hits (§2). Open.
- **#134** retired-token hits — self-reference (§3a). Not stale.
- **#110** `refs ADR-03` — a **cross-repo** ref (ADR-03 lives in `ai-council`, not here); BACKLOG already annotates "verify in the ai-council chat." Per the grooming design, a cross-repo ref is "verify elsewhere," **not a kill**.
- All `REFS-CLOSED` hits across the file (#180–183→#172, #131→#115/#138, #146/#166→#11, etc.) are **precedent/sibling** references — the foundation shipped; they are the active roadmap, not stale deps. No `depends-on` points at a closed id (verified).

---

## 4. LESSONS — proposed entries (append at TOP; PROPOSE-ONLY, not appended)

Grounded in the JOURNAL arc; confirmed absent from current LESSONS (`grep -ni "disposition|net-neutral|placeholder|keep both" LESSONS.md`). The state.yaml-seeding worktree lesson is **already** captured (LESSONS `line 16`, n=3) — these are the *uncaptured* facets.

**Entry A — `claude -w` worktree lifecycle (branch-naming + 2nd-merge collision):**
```
### 2026-06-20 | dependency-arc parallel worktrees (#193/#199 build + #192 integration) | `claude -w <name>` provisions the worktree at `.claude/worktrees/<name>` on a PLACEHOLDER branch `worktree-<name>`; you then cut the real `feat/...` branch off it — so teardown must delete BOTH the feature branch AND the `worktree-<name>` placeholder, then `git worktree prune` (`git worktree remove` is NOT idempotent). `/ship` refuses inside a worktree — integrate to `main` via `--no-ff` FROM THE PRIMARY. When two worktree arcs branched off DIFFERENT bases both merge, `JOURNAL.md` collides (each lacks the other's newest entry) and any live counter (`pytest_collected`) diverges: resolve by KEEPING BOTH session entries newest-first by commit time (drop nothing) and RECONCILING the count to the live COMBINED tree — never trust a worktree's pre-integration count. | methodology | [scope: meta] | grounds #198 (codify the `claude -w` lifecycle into PLAYBOOK/HANDOFF); strengthens the seed-state-yaml + branch-merge-noff memories
```

**Entry B — disposition discipline (fix your own fresh drift; never disposition it):**
```
### 2026-06-21 | ops/task audit (BACKLOG doc_rot self-induced WARN) | When YOUR OWN edit creates a fresh gate finding, FIX the edit — never disposition the self-induced drift. A prose edit pushing a BACKLOG task past the `doc_rot` threshold (>1200 chars, or >=3 dated blocks & >700) mints a NEW WARN and reds the ship-gate; the correct response is to trim the edit back net-neutral (the #153 arc — `f24a8ce`/`dec7726` trimmed #153 1362->1176 rather than dispositioning the WARN it had just created), NOT to add a disposition entry. Dispositioning is for PRE-EXISTING findings judged acceptable; using it to silence drift you just introduced launders a regression into "accepted." | process | [scope: meta] | reinforces the BACKLOG-edit-doc_rot memory + ADR-65 done-items-leave; applied in this audit (CLAUDE §12 growth surfaced for condensation, not dispositioned)
```

**Entry C — pre-push / `core.hooksPath` activation — RECOMMEND the GOTCHAS SKILL, not LESSONS.**
This is a **universal** pre-commit mechanic (not `.dev-knowledge`-specific), so per CLAUDE §8 its home is `~/.claude/skills/gotchas/gotchas.md` — **out of this audit's write scope.** Proposed gotcha for the operator/next session to add there:
```
**Gotcha:** A new pre-commit hook STAGE (pre-push / commit-msg) is inert in an existing clone until armed — adding it to `.pre-commit-config.yaml` `default_install_hook_types` only wires it on a FRESH `pre-commit install`.
**Trigger:** adding or relying on a pre-push/commit-msg hook (e.g. block-ff-push #153).
**Symptom:** the gate never fires; `git push`/commit succeeds though the hook should block.
**Fix:** `pre-commit install --hook-type pre-push` (and/or `--hook-type commit-msg`) once per machine.
**core.hooksPath note:** if `git config core.hooksPath` is redirected, pre-commit's `.git/hooks/` shims may not be found at all — verify it is unset/expected.
**Last triggered:** 2026-06-20.
```
**Decision asked:** confirm the gotchas-skill home (recommended), and confirm/adjust the `core.hooksPath` line — JOURNAL evidences the *activation* half (lines 50/56) but carries no `core.hooksPath` incident, so that clause is included on the operator's flag; drop it if no interaction was witnessed.

---

## 5. CLAUDE §12 condensation — proposed (operator-gated)

`audit.py doc_rot` flags **`section-history CLAUDE.md#section-history` — 23 entries (>= 12; condense to git per ADR-49/65)**. This is the repo's **own named failure class** (history-accretion) applied to its own contract file, and it just pushed CLAUDE.md to **201 lines** (>200 self-claim). 

**Proposal:** condense §12 to the last ~5 version notes + a pointer ("full version history in `git log -- CLAUDE.md`"), per ADR-49 (CHANGELOG retired → git is the record). **Why operator-gated:** §12 entries are historical record; condensing removes content (the no-remove invariant). **JOURNAL evidence:** the same pattern was applied to PLAYBOOK section-history (#77 scope) and is exactly what ADR-49/65 prescribe. **Risk:** low — git retains every note; the cross-references inside old §12 notes are themselves historical.

---

## 6. Cross-domain inconsistencies — FLAGGED, not fixed (out of this layer's scope)

- **`protocols/ENVIRONMENT.md` is badly stale (last_reviewed 2026-06-03).** Its `~/.claude/` tree still lists `boot.md` + `evolve.md` as **live** (archived 2026-06-05); no Codex version row; a Binding Council Decision **"No Codex CLI"** that contradicts the live `/codex-review` command + ADR-54. Claude Code version row says 2.1.161 (session-start changelog sentinel reports 2.1.183). **This confirms #71 and #119 are genuinely open** (real currency debt, not prune candidates). Owner: a future ENVIRONMENT-scope pass (#71).
- **`ecosystem/index.yaml` is a stale cached snapshot** (`generated: 2026-06-02`; it records CLAUDE.md as 12094 chars vs the live 26227). It auto-regenerates on `audit.py run`, so not actionable here — flagged only so a reader doesn't trust its cached evidence.
- **Two historical `no_ff_merges` WARNs** on `main` (`3a894ee`, `d0f9ead`, 2026-06-19) — pre-date the `block-ff-push` gate; forward-only per ADR-84, the post-hoc WARN is the accepted backstop. No action.

---

## 7. Closure status & what's owed

- **Done (this run):** (1) ops/task docs mechanically reconciled to JOURNAL/state — auto-applied + logged (§1); (2) this findings doc with the BACKLOG prune proposal as its centerpiece (§3) + LESSONS proposals (§4) + §12 condensation (§5) + cross-domain flags (§6). Docs are **factually current**; the prune/proposal list is **decision-ready**.
- **OWED — operator, in the morning:** review → `git merge --no-ff feat/audit-ops` **from the primary** (not from this worktree — `/ship` refuses; seed-state-yaml lesson), then **delete both `feat/audit-ops` and the `worktree-audit-ops` placeholder branch** + `git worktree prune` (the §4 Entry-A lesson, dogfooded).
- **Open decisions for the operator:** the §3 prune ratifications (esp. close #47, #10; trim #164/#134/#77); the §5 §12-condensation; the §4 LESSONS appends + the gotchas-skill home for Entry C. Feeds the **2026-07-01 quarterly groom**.

*Self-audit note:* this doc is a `docs/audits/` output (new file, existing folder — within the no-new-paths invariant). No BACKLOG item was removed or edited; no rule was changed; no folder was created.
