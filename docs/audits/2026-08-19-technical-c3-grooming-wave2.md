<!-- scope: meta -->
# C3 grooming wave 2 — the 116 non-silent open rows, one evidence sheet each · 2026-08-19

**Produced by:** CC, cloud lane C3, branch `claude/c3-grooming-wave2`, under the frozen contract
`docs/audits/2026-08-19-technical-c3-grooming-wave2-contract.md` (dispatch-stamped first, 26 lines,
contract-of-record).
**Posture:** READ-ONLY. **No closures, no status edits, no BACKLOG/`tasks/` writes, no index
regeneration, no JOURNAL write, no merge.** Every line below is *evidence* plus a RECOMMENDED CLASS.
The live / dead / awaiting-ruling **verdict is the architect's**; nothing here proposes a closure as
settled, and no language stronger than the four classes appears.

## §0 · The answer first

```
rows evaluated                116   (every open row N4 did not cover, minus the excluded six)
themes covered                  9 of 9   — E1 E2 E3 E4 E5 E6 E7 E8 E9, ALL COMPLETE
  LIVE                        105   (90.5%)  ask stands, target verified real
  AWAITING-RULING              10   ( 8.6%)  one named decision is the whole remaining work
  DEAD-CANDIDATE                1   ( 0.9%)  [#388] — both Done-when conjuncts read satisfied
  MALFORMED                     0   ( 0.0%)  none; see §12
```

**Wave 2 harvested less than wave 1, not more — and the contract predicted the wrong direction.**
The brief expected "landed work since 2026-08-15 ALREADY satisfies the ask" to be "the likeliest
wave-2 harvest". It is not. Of 116 rows with git activity, **zero** carry a validator-strength closure
signature (`propose_closures.CLOSES_RE` over all 1,189 first-parent merges on `main` returns **0 hits**
for every wave-2 id), and exactly one row's Done-when reads satisfied on its face. What the git
activity mostly records is **Done-when *conversion*** — the W4a–W4d and batch-6 conversion lanes
rewrote row *text* across dozens of these ids without touching the mechanisms they describe. A merge
naming `[#N]` is, in this corpus, more often a lane that made the row *checkable* than a lane that
made it *done*.

**What the wave did produce, and it is worth more than a closure list:** twenty-three rows are
**partially discharged** — one conjunct landed, the other owed — and in almost every case the residue
is the load-bearing half. Those are enumerated in §11b, because dispatching a lane against them
without reading the partial is how a row gets re-done.

## §1 · Reading rules this sheet enforces

**GIT ACTIVITY IS NOT COMPLETION.** This sheet inverts N4's population: N4 took the P10 sheet's
git-*silent* rows, this takes the rest. The inversion changed almost nothing about the outcome —
90.5% LIVE here against N4's 79.2% — which is itself the result. **Git silence predicted nothing in
wave 1; git activity predicts nothing in wave 2.**

**A MENTION IS NOT A CLOSURE, AND A CONVERSION IS NOT A BUILD.** Merge-mention counts appear below only
as context. Where a row's most recent mention is a Done-when conversion lane (`a4fc652dc`,
`8a0912785`, `5eb1269f5`, `781bd4ff9`, and batch 6's `51d7fa081` … `b4862b9be`), that is stated
explicitly, because a reader ranking rows by recency would otherwise read those merges as progress.

**A DEAD LOCATOR IS NOT A DEAD ROW.** Seven rows cite a `file:line` that no longer resolves while the
mechanism they indict is alive elsewhere, and seven more carry a stale *count* or premise in their own
body. Each is classed on the *mechanism*, with the repaired
locator quoted inline. §10 collects them — that is `[#534]`'s subject, and §10 also records that
`[#534]`'s **own** repaired locators have drifted again since it was filed two days ago.

**"AWAITING-RULING" means one named decision is the whole remaining work.** Ten rows qualify; each
names its decision in the class line. Two are members of the L-5 PROSE-JUDGMENT carve-out
(`protocols/STANDING_RULINGS.md:1317`) — `[#420]` and `[#507]` — and are sanctioned judgment rows, not
hygiene defects.

**THE ARCHITECT'S VERDICT IS NOT PRE-EMPTED.** Where evidence points strongly at a disposition the row
does not have (e.g. `[#428]`'s leg 2, `[#383]`'s clauses (a)/(b)), this sheet says so as evidence and
stops at the class boundary.

## §2 · Derivation of the row set — the exact arithmetic

The contract defines wave 2 as *all open ids minus N4's 72 minus rows closed since*, with six ids
excluded. Derived mechanically at `HEAD = 4541155` (`main`, 2026-08-19):

```
status: open in tasks/*.md                      183     (the P10 predicate; frontmatter, not manifest)
  minus N4's 72 that are still open              63     (9 of N4's 72 have closed since: see below)
  minus excluded still-open ids                   4     ([#529] [#530] [#533] [#554])
                                              -------
wave 2                                          116
```

`[#171]` and `[#486]`, also on the exclusion list, were already inside N4's 72 and so were never in
this population. **Closed since N4 ran (9 of its 72):** `[#122] [#281] [#323] [#406] [#407] [#449]
[#450] [#494] [#536]` — eight of them today, under the S-1 seat arc (`7e793eca8`) and the `[#122]`
KEEP close (`4541155`).

**Two denominators, and why this sheet uses 183 rather than 207.** `tasks/manifest.json` carries 207
task nodes; `tasks/*.md` frontmatter carries 183 `status: open` plus 24 `deferred` — 183 + 24 = 207
exactly, so the manifest's active list includes deferred rows. P10 and N4 both scope to `status: open`,
and this sheet follows them. **This is the same three-way denominator disagreement `[#555]` exists to
resolve** (§E7), measured live tonight rather than quoted.

**Live worktree branches: none observable.** The contract also excludes "any row a live worktree branch
names". `git worktree list` shows one checkout and `git branch -a` shows only `main` and
`origin/main` — a cloud container sees no operator-side worktrees. **No row was removed on that ground**,
so if an operator worktree currently names a wave-2 row, that row is evaluated here and should be
treated as excluded by the architect. This is a stated limit, not a silent one.

**Eighteen wave-2 rows have zero merge mentions** and were therefore in *neither* wave's original
population: `[#43] [#245] [#269] [#276] [#327] [#331] [#335] [#345] [#359] [#526] [#538] [#539]
[#541] [#547] [#548] [#549] [#550] [#551]`. Most were filed after the P10 sheet's 2026-08-18 SHA. They
are evaluated here because the contract's arithmetic — *all open ids minus N4's 72* — puts them here,
and leaving them out would have left the two waves short of the open set.

## §3 · Method

Per the contract, identical to N4's. For each row: its `tasks/<id>-*.md` file read **in full**; the ASK
stated in one line from the body; the TARGET STATE established by live evidence (`file:line`, ADR,
sha, directory listing, or a grep whose result is quoted); an explicit check of whether work landed
**since 2026-08-15** already satisfies the ask; then a RECOMMENDED CLASS. Rows are grouped by the
`theme:` field of their own frontmatter — **not** by BACKLOG position, which mis-assigns rows cited
inside other rows' `refs` lines.

---
## [E1] Handoff continuity — 7 rows

**[#162] Vocab decision — "architect" actor vs mode** — ASK: disambiguate "architect" as the Layer-1
*actor* (ADR-28 / ARCHITECTURE Ch1) from the handoff *mode* (`architect|execution`), atomically, and
land it in an ADR or `protocols/STANDING_RULINGS.md`.
TARGET: real and the collision is still live in one file — `protocols/HANDOFF_BOOT.md:16` says "You
are the **critical architect**" (actor) while `:83` and `:102` say "when CC's handoff names
**architect mode**" (mode); `protocols/HANDOFF_PROCESS.md:408` is "§13. Modes — architect |
execution". No ADR and no `STANDING_RULINGS.md` section lands the disambiguation: `grep '#162'` over
`protocols/STANDING_RULINGS.md` returns **zero**, and the only ADR hits (ADR-98:6/:32, ADR-99:6/:21/:41)
cite #162 as the *class* their own rename belongs to — they name the collision, they do not rule it.
Landed work since 2026-08-15: none touching this.
**CLASS: LIVE.**

**[#293] Consumer runbook fan-out** — ASK: seed each onboarded consumer's `docs/handoffs/README.md`
from the hub canonical source via `scripts/seed_runbook.py --target-root <repo>`, denominator 8.
TARGET: `scripts/seed_runbook.py` exists; the seeding was **executed 7-of-8 and REVERTED IN FULL** at
lane k (`94f9307b3`, 2026-08-16) because ADR-60 forbids a child repo carrying a local
`docs/handoffs/` — the exact path the row's own prose names. The row body records itself as
"BLOCKED-ON-RULING since lane k" and names its prerequisite `[#303]`, which is **still open**
(`tasks/303-make-seed-runbook-py-child-class-aware.md:4` → `status: open`). The open question is not
work, it is *which consumer-side home is correct*.
**CLASS: AWAITING-RULING** — decision: the correct consumer-side home for the seeded runbook under
ADR-60 (the two candidates are carried in `docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md`).

**[#350] Handoff-process refinements** — ASK: three legs — (a) a non-CC browser can TRIGGER a
handoff, (b) the bundle-cites-a-moved-file dependency class is detected or accepted, (c) each filed
refinement carries a BACKLOG id.
TARGET: real and unbuilt on every leg. `grep -n 'trigger' protocols/HANDOFF_PROCESS.md` returns two
hits (`:663` diff-triggered probes, `:855` threshold auto-trigger) and **neither is a non-CC trigger
path**; no file-dependency check exists in `scripts/gen_handoff.py` or the probe set. The row's own
escape hatch is equally unused: `grep '350' protocols/STANDING_RULINGS.md` returns **zero**, so no
deferral section names it. Operator-dictated priority-program item 5, explicitly LAST.
**CLASS: LIVE.**

**[#390] ADR-87 effort-ownership contradiction + prompt-template true-up** — ASK: resolve the
ADR-87-vs-PLAYBOOK contradiction over who owns *model/effort*, then make
`templates/prompt-template.md` match the live effort ladder.
TARGET: **the ADR half looks satisfied, the template half measurably is not.** ADR-87 carries
`## Amendment — 2026-08-08: the population boundary on model/effort` (`:112`), explicitly
"an amendment section, not an edit" (`:125`) — which is exactly the append-only marker the row asks
for — though it self-limits to "who states the boot tier, not what it is" (`:133`). The second
conjunct fails live: `templates/prompt-template.md:68` still reads `<low | medium | high | xhigh>`
against the live five-rung ladder, which `protocols/PLAYBOOK.md:3064`/`:3126`/`:3138` state as
`low / medium / high / xhigh / max`. **A second, adjacent defect this re-read surfaced:**
`PLAYBOOK.md:2141` itself declares "Effort is a CLOSED enum — `{low | medium | high | xhigh}`",
contradicting its own §3064 table four rungs later — so PLAYBOOK is now the *third* disagreeing
surface, not the arbiter the row assumes.
**CLASS: LIVE.**

**[#447] Self-referential gate family** — ASK: two mechanisms — (1) a commit *raising* a ratchet
must be judged by the raised value, (2) a wrap commit must be able to satisfy its own JOURNAL-anchor
gate; with tests.
TARGET: **leg (2) has a landed mechanism and is the likeliest harvest here.** ADR-85`:327` states
"At pre-push, discharge is **range-level**" — a JOURNAL entry naming ≥1 SHA the range *introduces* —
and `scripts/journal_anchor.py:2-11` defines that predicate once for both `block_unanchored_push.py`
and `audit.check_journal_spine_anchor`, which is precisely the "cannot self-anchor" recursion the row
cites. `tests/test_journal_anchor.py` and `tests/test_silent_rule_ratchet.py` both exist. Leg (1) is
untouched: `scripts/arm_hooks.py:1-20` still installs at SessionStart and its docstring claims only
idempotence and `core.hooksPath` tolerance — nothing about being judged by a raised value — and no
test asserts the raise-and-be-judged property. The row's Done-when is a conjunction, so one landed
leg does not satisfy it.
**CLASS: LIVE** (with the honest note that leg 2 may be dischargeable on inspection).

**[#511] The 30-minute handoff cut is ~99.8% session authoring** — ASK: rule the cut of the
NON-MECHANIZED loads (FILL-IN count vs RF-6, probe count vs §5, or verify pass vs anti-bluff), land it
in `HANDOFF_PROCESS.md` with a version bump, re-stamp dependents, and measure one post-change handoff.
TARGET: no cut has landed. `protocols/HANDOFF_PROCESS.md:4` reads `Version: 6.2.0` and its own
history tail (`:1078`) attributes 6.2.0 to "2026-08-08, §4 BOOT DRILL — ARC-dispatch-surface-codify"
— a different subject; the last three bumps (`:1028`, `:1050`, `:1078`) carry no cut. The FILL-IN
population is live and larger than the row's own figure: 39 across `templates/handoff/`
(`RESIDUAL.md.tmpl` 7, `EPIC_BOOT.md.tmpl` 17, `FUNCTIONAL_BOOT.md.tmpl` 5, `HANDOFF_BOOT.md.tmpl` 3,
`PROBES.md.tmpl` 1) versus the row's "15 FILL-IN regions" — the row's measurement is stale low, which
strengthens rather than weakens the ask.
**CLASS: LIVE.**

**[#547] Split-brain prevention has no referent under v6** — ASK: the split-brain drift check must
either name v6 artifacts that exist, or be recorded as retired with a named successor.
TARGET: **confirmed live, both halves measured this session.** `protocols/PLAYBOOK.md:4015` still
carries `### Split-brain prevention` (and `:195` its TOC entry), and a case-insensitive count of
`current state|future state` over `protocols/HANDOFF_PROCESS.md` returns **0** — the sections the
instruction tells the incoming seat to read do not exist in the live v6.2.0 spec. Zero merge mentions
on main; filed 2026-08-17 from the batch-7a lane-b ADR currency sweep.
**CLASS: LIVE.**

**[E1] rollup — 7 rows: 6 LIVE · 1 AWAITING-RULING · 0 DEAD-CANDIDATE · 0 MALFORMED.** Theme
COMPLETE. The one harvest signal is inside `[#447]`, whose leg 2 has a landed mechanism
(`journal_anchor.py` + ADR-85 §A5 range-level discharge) — a *partial*, not a closure, because the
row's Done-when is a conjunction and leg 1 is untouched. `[#390]` is the inverse: its ADR half looks
discharged by the 2026-08-08 amendment while its template half is falsifiably unmet at
`templates/prompt-template.md:68`.
---

## [E2] Enforced governance — 35 rows

**[#146] De-hardcode-first doctrine + sweep** — ASK: (a) de-hardcode-first recorded as doctrine in
PLAYBOOK's `amendment_coherence` honest-limits section, (b) a sweep artifact naming every
hand-maintained version surface with a per-surface verdict.
TARGET: **(a) is landed — at a drifted locator — and (b) has not run.** The row pins
`PLAYBOOK:1016-1024`; the text actually sits at **`protocols/PLAYBOOK.md:1109`** ("The superior fix
for a coupled surface is to **de-hardcode** it — make it interpolate the spec version … de-hardcoded
surfaces carry nothing to compare and are out of scope by design"). No `docs/audits/*` slug matches a
de-hardcode or version-surface sweep. The row's own honesty note stands: the text is there, nothing
ties its authorship to this row.
**CLASS: LIVE** (residue = the sweep).

**[#210] Convert journal-wrap no-ff WARNs to a standing rule** — ASK: the shape recorded in a
`STANDING_RULINGS.md` section naming `[#210]`, AND either a tested `no_ff_merges` exemption or the wrap
moved behind `--no-ff`; and none of the 3 per-instance entries left in the disposition register.
TARGET: real, all three conjuncts unmet. `grep -c 'journal-wrap' ecosystem/disposition-register.yaml`
= **3** — the per-instance entries are all still there. `grep '210' protocols/STANDING_RULINGS.md`
finds no section (the hits are unrelated line numbers). `scripts/validate_no_ff.py` carries no
path-scoped exemption; its only exemption language (`:34`, `:61`, `:94`) is the ADR-84 automation
exemption it explicitly refuses to add ("a marker-based exemption on main would be dead code AND a
spoofable backdoor").
**CLASS: LIVE.**

**[#220] MODIFY / semantic-drift axis (verify-first spike)** — ASK: a committed fixture exercising a
semantic/MODIFY change, a `docs/audits/` record naming which organs fired and which did not, with the
design leg deferred pending that result.
TARGET: real and unrun — no `tests/fixtures/` entry and no `docs/audits/*` slug matches a MODIFY or
semantic-drift subject. The row's discipline (VERIFY-FIRST SPIKE ONLY, "do NOT design ahead of it") is
intact and un-violated, which is worth noting: nothing has been built prematurely.
**CLASS: LIVE.**

**[#234] Cross-repo probe validator — `.claude/` target paths need FAIL teeth** — ASK: a cross-repo
bundle whose floor-guard probe names a present `.claude/<file>` PASSes and one naming an absent file
FAILs, with tests.
TARGET: real and unhardened — `scripts/verify_handoff_probes.py:113` still reads
`_FALLBACK_EXCLUDE_DIRS = {".git", ".claude", "node_modules", "aborted", "in-progress"}`, and `:366`
still prunes any path whose parts intersect it. So a foreign `.claude/<file>` target still degrades to
`skipped`/WARN exactly as the row describes. Last merge mention 2026-07-21.
**CLASS: LIVE.**

**[#239] Informant Tier-2 beyond the four deploy carriers** — ASK: skills, commands (incl.
`/codex-review`) and review-closure tooling each carry a `detect()` + versioned target-state that
`enforcement_coverage.py` reports present-and-wired, or a `STANDING_RULINGS.md` section naming
`[#239]` per element.
TARGET: real and unbuilt. `scripts/enforcement_coverage.py` has **no `detect()` definition** and no
`skill`-facing surface; what it reads are hook strings (`_settings_hook_commands` at `:273`, used at
`:405`, `:538`, `:672`) and pre-commit hook strings — the carrier axis, not the skills/commands axis.
`grep '239' protocols/STANDING_RULINGS.md` = **0**.
**CLASS: LIVE.**

**[#241] Undeclared-edge groom** — ASK: every id the `undeclared_edges` ship-gate leg surfaces is
either declared (`reconciled_with`) or recorded permanent-defer-with-reason, and each disposition entry
retires or is re-annotated — predicate reads the live surfaced set, never a fixed count.
TARGET: real and partially declared. `protocols/PLAYBOOK.md` carries 4 `reconciled_with` occurrences
and `protocols/SESSION_SETUP.md` 1 — the two the row predicted as genuinely version-coupled. But
**`VISION.md` and `protocols/ESSENTIALS.md` each carry 0**, and both are `canonical_freshness`-gated,
which is precisely the constraint the row names ("declarations must ride a genuine freshness
re-stamp"). The disposition register still carries 48 `undeclared`-related entries.
**CLASS: LIVE.**

**[#277] `propose_closures` signal repair** — ASK: the two STRONG false positives (#5, #77) no longer
surface, pinned by a test each; and one run over the last 30 days of `main` yields a
STRONG:WEAK-actioned ratio better than 49:0, with the numbers in the closing commit.
TARGET: real and **the metric has moved the wrong way**, which the row itself now records:
"RE-MEASURED 2026-08-16 — degraded 3x+", sourced to night-3's D3 (161:0 on the night clone, 154:0 on
the host). `scripts/propose_closures.py` carries no permanent suppression of #5/#77 — the only `#5`
hit is a comment at `:74` about synthesized directives — and the `weak_suppressed` path (`:178`,
`:198`) is the cold-start case, not an FP suppression. Leg (a) is the cheap half and is unbuilt.
**CLASS: LIVE.**

**[#296] `audit.py repo <name> --repo-path` prints a report path that isn't there** — ASK: the command
writes the report where it says, or prints where it actually lands, with a test.
TARGET: real. `scripts/audit.py` still emits a bare `click.echo(f"Report: {out}")` at **`:4050`** and
**`:4090`** with no indication that the artifact lands as a commit on `automation/fleet-audit` rather
than in the working tree. The row's own 2026-08-06 repro already refuted the "lost report" reading and
re-aimed at the locator; nothing has changed since.
**CLASS: LIVE.**

**[#335] Exempt `templates/` from `reconciled_versions`** — ASK: `reconciled_versions` no longer flags
a `templates/` file carrying a placeholder, with a test, and the standing disposition
`warn-reconciled-versions-contributing-template` auto-clears.
TARGET: real and unfixed. `templates/CONTRIBUTING-md-template.md:3` still reads
`reconciled_with: handoff-process@<version>` — the placeholder that is malformed *by construction* —
and the disposition `warn-reconciled-versions-contributing-template` is still present in
`ecosystem/disposition-register.yaml`. Zero merge mentions in 1,189 merges. The smallest
check-precision fix in the theme.
**CLASS: LIVE.**

**[#345] Externalize the ADR-101 frozensets** — ASK: a standalone `ecosystem/<name>.yaml` registry
ships, the gate reads it (frozensets gone), Rule-B naming generalizes beyond `docs/audits/`, lockstep
collapsed, with tests.
TARGET: real and unbuilt — `scripts/validate_hermetization.py:60` still defines
`SANCTIONED_TIER1_DIRS: frozenset[str]` and `:110` `AUDIT_CLASS_ENUM`, with `:123` deriving
`_ENUM_BY_LEN` from the latter; `ls ecosystem/*.yaml` shows ten files and **none** is a path-pattern
registry. Note the row's own gate on itself: creating a new registry file "needs an explicit
operator-authorization line (predates its own pattern)".
**CLASS: LIVE.**

**[#389] Prompt-lint — gate the five architect fields** — ASK: a seeded prompt missing any one of the
five ADR-87 §5 fields is refused or WARNed, one test per field; AND R6's disposition recorded in
ADR-87 or a `STANDING_RULINGS.md` section naming `[#389]`.
TARGET: no prompt-lint script exists in `scripts/`, and the `STANDING_RULINGS.md` hits for "389" are
line numbers inside unrelated entries plus one passing mention at `:1358` — **no section dispositions
R6**. The row also carries `depends-on: "390"` in frontmatter, and `[#390]` is LIVE (E1). The row's
own text names the blocker: the off-repo-prompt question is "[E8] W6, **UNRULED**".
**CLASS: AWAITING-RULING** — decision: R6, the hard-probe-vs-soft-check question (or an explicit
scoping to hook-reachable surfaces, which is itself the ruling the Done-when wants recorded).

**[#401] ai-council routing still ARMED at the deleted hub landing zone** — ASK: (a) ai-council drops
`.dev-knowledge` from `target_projects`, AND (b) `routing.py` refuses the `.dev-knowledge` target per
the recorded ruling.
TARGET: **both legs are off-tree and neither is verifiable here** — `ls scripts/routing.py` → no such
file; the component lives in ai-council. What is verifiable in the hub: the landing zone is gone
(`docs/decisions/transcripts/` absent, deleted `b4435fad`), so the hazard the row names — a
`target-project:` run silently re-creating it as untracked files — is still exactly as described.
Clause (b)'s ruling is recorded and merged (`c5f65165e`, 2026-07-25, "does NOT close").
**CLASS: LIVE** (both legs consumer-side; ADR-41 queue-only here).

**[#408] Auto-coupled doc updates** — ASK: a test seeds a close with no `ARCHITECTURE.md`/`JOURNAL.md`
edit and asserts the organ surfaces or blocks it, plus a second test for the clean case; or a
`STANDING_RULINGS.md` section naming `[#408]`.
TARGET: real, filing-only by its own text, and unbuilt. The design draft exists and is committed
(`docs/audits/2026-08-06-technical-night-408-coupling-manifest-design.md`), and `grep '[#408]'
protocols/STANDING_RULINGS.md` = **0**. **The first gate on any build is an operator decision the
draft deliberately did not settle** — per-section granularity — so this row is build-blocked on a
choice, not on capacity.
**CLASS: LIVE** (with an operator decision sitting in front of its build leg).

**[#414] Self-acting-on-main incident family** — ASK: a mechanism refuses or flags (a) a change to
`main` with no recorded operator GO and (b) an unanchored change to `main`, with a test per case; and
the organ choice recorded in an ADR or a `STANDING_RULINGS.md` section naming `[#414]`.
TARGET: **half (b) has a landed organ; half (a) has none, and the organ choice is unrecorded.**
`block_unanchored_push` + the `journal_spine_anchor` backstop (ADR-85 §A5/§A8) refuse an unanchored
push to main, which is (b). Nothing implements an operator-GO precondition on merge/push — `/ship`
checks no precondition at all (see `[#423]`) — and `grep '414' protocols/STANDING_RULINGS.md` returns
one unrelated line (`:892`), no section. The row's three candidate organs (a/b/c) remain unchosen.
**CLASS: LIVE.**

**[#417] `check_dirty_tree` runs with no pathspec** — ASK: the `history_specs`/`pathspecs` scope list
extracted into a location shared with `check_dirty_tree`'s exclusion scope, narrowed; or a
`STANDING_RULINGS.md` section naming `[#417]` stating why extraction was rejected.
TARGET: **the filter landed; the extraction did not — and the row's own locator is dead.**
`scripts/session_end_backpressure.py:402` defines `_is_lane_owned_daily` and `:418` applies it inside
`check_dirty_tree` (`:412`), exactly the 2026-08-16 landing the row records. The scope list it must be
merged with still lives separately at **`scripts/audit.py:3844`** (`history_specs`) / `:3853`
(`pathspecs`) — the row pins `:4751-4760`, which is **past EOF** on a 4,341-line file. Two definitions,
no extraction.
**CLASS: LIVE** (residue = extraction; locator dead — see `[#534]`).

**[#418] `automation/fleet-audit` records 0–10 baselines a day** — ASK: an audit artifact recording a
reproduction with observed per-day counts, and either a check FAILing on a second baseline for the same
date (with a test) or a `STANDING_RULINGS.md` section naming `[#418]`.
TARGET: real, uninstrumented, and **now compounded by total silence**. The causal mechanism the row
names is confirmed: `logs/FLEET-HEALTH.md` is gitignored (`.gitignore:30`) and therefore
per-working-tree, so every clone believes the baseline is stale — and `.gitignore:34` even documents
the sibling pattern. No reproduction artifact exists. Live: the baseline stream has produced **nothing
since 2026-07-31** across all five `ecosystem/*/history/` directories, so the multiplicity the row
measures has become absence (`[#493]`).
**CLASS: LIVE.**

**[#423] The integration sequence runs on prose every time** — ASK: the preconditions enumerated in
`plugins/tier1-lifecycle/commands/ship.md` and each checked by `/ship` at run time with a test per
precondition; or a `STANDING_RULINGS.md` section naming `[#423]`.
TARGET: real and untouched — `grep -ci 'precondition' plugins/tier1-lifecycle/commands/ship.md` = **0**
and `grep -c '423' protocols/STANDING_RULINGS.md` = **0**. `/ship` still automates merge, push and
delete and checks nothing before them. The row's evidence (two round-trips lost to prose defects in
one arc) is unaddressed.
**CLASS: LIVE.**

**[#424] Backlog `depends-on` gates are INERT** — ASK: every `depends-on` clause parses, a regression
test pins the bare-id form, and the `plugins/tier1-lifecycle` twin moves in lockstep.
TARGET: **the defect is live and the census has moved again — a third distinct count.**
`scripts/validate_backlog.py:83` still reads `_DEPID_RE = re.compile(r"#(\d+)")`, consumed at `:113`.
Live census tonight: **4 clauses, 2 parse, 2 inert** — PARSED `[#112] "#23"` and `[#169] "#171"`;
**INERT** `[#385] "383"` and `[#389] "390"`. The row records 6/4/2 (itself a correction of a stale
8/4). The two inert clauses are still exactly the ones the row flags: the [E9] chain edge and
`[#389]`. Every prior census figure in the row is now stale, and the defect is not.
**CLASS: LIVE.**

**[#425] The suite is green on a format the file does not use** — ASK: an artifact enumerating each
parser-facing test corpus against the input forms its parser accepts, with every gap closed by a
negative-form fixture or listed as justified; or a `STANDING_RULINGS.md` section naming `[#425]`.
TARGET: real and unrun. `tests/test_validate_backlog.py` carries 38 hashed-`#NNN` occurrences and the
enumeration artifact does not exist; the `STANDING_RULINGS.md` hits for 425 are the L-8 fold NIE
(`:1353`, `:1585`), not a blanket reason. The row's generalizable claim — "a fixture corpus samples the
format its author intended, not the format the file contains" — is corroborated live by `[#424]`'s
still-inert clauses.
**CLASS: LIVE.**

**[#442] Plugin command-cache staleness** — ASK: a stale cached command cannot be served unnoticed —
invalidation on edit, or a load-time stamp comparison — with a test seeding a stale copy.
TARGET: real and unbuilt — `grep -ci 'cache|stamp' plugins/tier1-lifecycle/commands/review-closures.md`
= **0**; no invalidation or stamp mechanism exists anywhere in the plugin. The row correctly routes
itself through `[#438]`'s refusal-gate class ("design review BEFORE build applies"), and `[#438]` is
itself LIVE (E3) — so this row inherits an unbuilt doctrine as its precondition.
**CLASS: LIVE.**

**[#454] `closure_ids` negation defect** — ASK: RED-first tests over the three recorded reproduction
strings, a bounded parser change making negated mentions non-closing in BOTH copies, and terra review
pre-merge.
TARGET: real and unfixed — `grep -n 'negat|not close|does NOT close' scripts/propose_closures.py`
returns **zero**: the parser has no negation handling at all, so a commit body *denying* a closure
still yields a STRONG proposal. The twin in `plugins/tier1-lifecycle` is parity-pinned, so the fix is
necessarily a lockstep two-file change. This is the third distinct defect in one detector after
`[#437]` (fixed) and two recorded false positives.
**CLASS: LIVE.**

**[#477] `deployed_methodology_version` keys the registry by repo-root BASENAME** — ASK: the check
resolves the hub's row from a checkout whose directory name differs from the registry key, with a test
seeding a differently-named root.
TARGET: **reproducible in this very container.** `scripts/audit.py:1863` still computes
`repo_key = _git_repo_root_name(repo_path) or Path(repo_path).name`, looked up at `:1864` against
`ecosystem/deployed-versions.yaml:25`, whose hub row is keyed **`.dev-knowledge`**. This lane's
checkout root is `/home/user/dev-knowledge` — the exact GitHub-clone shape the row names — so the hub
cannot resolve its own row here. The row pins `:2300`; live is `:1863` (see `[#534]`).
**CLASS: LIVE.**

**[#484] ADR-106 system-Python divergence** — ASK: the divergence closed on the operator's machines
with a recorded interpreter-version check each, or a `STANDING_RULINGS.md` section naming `[#484]`
stating the deferral reason; and the cp1252 console class fixed at source with a test, or declared out
of scope in that same section.
TARGET: `grep '[#484]' protocols/STANDING_RULINGS.md` = **0**, so the named-deferral branch the row
itself proposes has not been taken — which is the whole point of the row ("filed as a named deferral
… rather than left as unowned drift"). The machine-side half is off-tree. No repo-wide encoding
posture exists.
**CLASS: LIVE.**

**[#485] A shared LF-enforcing write helper** — ASK: repo writers route through one LF-enforcing
helper, a test proves a CRLF write cannot land through it, and the gotcha entry retires or is
re-scoped.
TARGET: real and unbuilt — there is no shared write-helper module in `scripts/` and no
`STANDING_RULINGS.md` entry. The row's sharpest instance is verifiable in principle here: a CRLF
`tasks/` file stops matching `gen_task_tree`'s provenance line and the tree is REFUSED as foreign,
because the parser reads the working tree rather than the git blob — `.gitattributes` cannot save it.
Operator-directed.
**CLASS: LIVE.**

**[#497] Two stale claims on carrier/hook declarations** — ASK: BOTH claims corrected and the carrier's
own test asserting the deployed shape against the live probe rather than the prose.
TARGET: **both claims reproduce verbatim.** `deploy/carrier_mesh.py:75` still reads
`Must contain "session_end_backpressure" (locate)`, and `.pre-commit-hooks.yaml:74` — the declaration a
**consumer installs** — still reads "Fail-soft: exits 0 on any git error", a posture ADR-85 §A6
retired when `block-ff-push` went fail-CLOSED (exit 2). The hub's own `.pre-commit-config.yaml` states
it correctly, so the carried declaration teaches consumers the opposite of the hub's truth.
`grep '[#497]' protocols/STANDING_RULINGS.md` = **0**.
**CLASS: LIVE** — the highest ratio of consumer-facing harm to fix cost in the theme.

**[#500] The Stop hook's BACKLOG advisory reads a correctly-closed task as "nothing closed"** — ASK:
the advisory recognises row-DELETION plus the paired `tasks/*.md` terminal-status flip as a closure
signal, pinned by a test that closes a row the sanctioned way and asserts silence.
TARGET: real and unfixed — no closure-by-deletion recognition exists in
`scripts/session_end_backpressure.py`, and `grep '[#500]' protocols/STANDING_RULINGS.md` = **0**. The
defect is structural to ADR-107: a close deletes the generated row, and a deletion matches no
structural-marker-change pattern. The row's own framing is the reason it matters — "an advisory firing
hardest when the work was done right gets ignored" — and **eight rows closed correctly today**, every
one of which would have tripped it.
**CLASS: LIVE.**

**[#507] Report-only wall — the fourth recorded leg** — ASK: a ruling recording either the leg landed
(with a run showing a bypassed violation recorded server-side) or an explicit accepted-with-reason hold
naming what stays unrecorded.
TARGET: the wall exists (`.github/workflows/report-only-wall.yml` is the repo's only workflow) and
carries **no `pre-commit run --all-files` and no `ruff` leg** — grep returns zero for both — so the
coverage gap the row names is intact: a `--no-verify` push carrying a ruff violation leaves no server
record. The row is a **named member of the L-5 PROSE-JUDGMENT carve-out** (`STANDING_RULINGS.md:1317`)
and its own first words are "A DECISION, not a chore".
**CLASS: AWAITING-RULING** — decision: land the fourth leg vs an accepted-with-reason hold naming what
stays unrecorded (L-5 carve-out member).

**[#510] Scope the R-1 exemption to the lanes its manifest enumerates** — ASK: the exemption resolves
against a lane roster the open manifest declares, the no-roster posture ruled and encoded, a test
proving an out-of-roster lane branch is not exempt mid-batch, and Ch8 + the manifest template carrying
the field.
TARGET: **narrowed, not closed — exactly as the row states.** `scripts/batch_manifest.py` reads the
ratified grammar via the imported `LANE_BRANCH_RE` (`:16`, `:51`), which is W1's narrowing at
`1c6d4255`. All four roster legs stand: `grep 'lanes:' scripts/batch_manifest.py templates/*.md`
returns **zero**, so there is no manifest roster field, no template carrier, and nothing for the
exemption to resolve against — a conforming branch name is still self-grantable.
**CLASS: LIVE.**

**[#519] The close path is two edits, and nothing makes a half-done close visible** — ASK: a test seeds
a status-only close, runs the generator, and FAILS on the revert — the close path is atomic, or its
non-atomicity is gate-visible.
TARGET: real and unguarded. `scripts/gen_task_tree.py:274` `emit_task_file_text` still re-templates
frontmatter from the body on every emit (documented at `:67`), so a status-only close is silently
reverted by the next `--emit-source`. **No test asserts it:** neither `tests/test_gen_task_tree.py` nor
`tests/test_task_tree_gate.py` contains a status-only / revert / atomicity case. P1, and the row's
witnessed instance (`cd38fb8a`: 3 closes claimed, 194 rows before and after, every gate green) was
caught by an unrelated cross-check.
**CLASS: LIVE** — one of only four P1s in the wave, and the one whose failure mode is invisible.

**[#520] No sanctioned way to retire a committed bundle whose seal is wrong** — ASK: the marker surface
defined, that bundle carrying one, and `check_seal_identity` skipping a marked-retired bundle, with a
test pinning both halves.
TARGET: real, and the collision is intact — both `docs/handoffs/2026-08-01-dev-knowledge-architect` and
`…-architect-2` exist, which is precisely why the `-2` bundle's self-references verify green *about the
wrong bundle*. `scripts/check_seal_identity.py` has no retired/marker concept. The direction is already
ruled (external dated marker, bundle byte-unchanged), so what is missing is the build, not the
decision.
**CLASS: LIVE.**

**[#522] A re-cut handoff sibling carries its predecessor's payloads** — ASK: (a) `--allow-suffix`
refuses unless a predecessor is named, (b) a refusal test, (c) a carry test, (d) the validator's stated
limit closed for the re-cut path or re-annotated.
TARGET: real, all four legs unbuilt. `scripts/gen_handoff.py` documents `--allow-suffix` at `:241`,
`:289` and `:300` with **no `--carry-from` anywhere**. The validator's self-stated limit reproduces
verbatim at `scripts/validate_residual_completeness.py:25-33`: "It asserts only *placeholder-replaced*,
never *value-present*. A by-reference fill that names no verdict, count, or sha PASSES". So a
thinner refill still passes.
**CLASS: LIVE.**

**[#531] Lane-grammar enforcement at PROVISIONING** — ASK: creating an off-grammar
`refs/heads/worktree-lane-*` branch is REFUSED at creation with a reason, conforming names unaffected,
non-lane ref updates untouched, the escape explicit and non-silent, and `/lane-boot` step 1 restated as
a friendly pre-check.
TARGET: real and unwired — `grep -rn 'reference-transaction' .pre-commit-config.yaml scripts/` returns
**zero**, and `validate_branch_naming` appears in no pre-commit hook. The validator exists and is
imported by `batch_manifest` (`[#510]`'s narrowing), which is what makes this row cheap: the mechanism
is written, only the wiring point is missing.
**CLASS: LIVE.**

**[#534] `scripts/audit.py:<line>` locators on four open rows died at the `[#533]` decomposition** —
ASK: each of `[#357]` `[#358]` `[#417]` `[#477]` cites its construct by anchor text or a live-resolving
locator, and a check FAILs on a `scripts/*.py:<line>` locator in `tasks/` that does not resolve.
TARGET: **live, and this lane re-measured the row's own repaired locators as already stale — which is
the strongest possible argument for its second conjunct.** `scripts/audit.py` is now **4,341 lines**
(the row says 4,271, filed two days ago). Re-measured tonight against the row's stated repairs:
`repo_key` — row says `:1862`, live **`:1863`**; `discover_repos` — row says `:490`, live **`:491`**;
the `history_specs` scope list — row says `:3779-3788`, live **`:3844`**. Every one of the row's own
corrections has drifted again inside 48 hours. No check exists over `scripts/*.py:<line>` locators in
`tasks/`.
**CLASS: LIVE** — and the evidence above is a finding in its own right, not merely a status.

**[#552] Window-close disposition + archival routine** — ASK: both legs built with their tests, the
ADR-100 exclusion stated in the check's docstring, and one window closing with every new audit
dispositioned and zero terminal-status documents outside an `archive/`.
TARGET: real and unbuilt — there is no `archival_residency` member in `scripts/audit_checks/` (the
directory listing has no archival module and the name has zero occurrences), and `propose_closures.py`
has no archival section. This row **does** carry a genuine `· routine:` block (one of only four in
`tasks/`), fully populated with `review_date=2026-11-17`. Its own honest limit stands: leg (a) cannot
fire on an ADR whose supersession was never written into its status line, which is the live corpus's
state — the gap `[#242]`/`[#362]` own.
**CLASS: LIVE.**

**[#560] `review_artifact_coverage` reads only the FIRST branch/HEAD triple per file** — ASK: the
reader parses EVERY triple, a multi-branch artifact links every branch it reviews, the title predicate
admits the forms actually in `docs/audits/` while still admitting 0 of the 13 non-review docs carrying
`**Branch:**`, one Finding per unlinked merge, and any residual WARN on an immutable artifact
dispositioned.
TARGET: real, and both defects are readable in the source. `scripts/audit.py:3143` defines
`_REVIEW_TITLE_RE = re.compile(r"(?m)^# Codex Review\b")` — a single literal that cannot admit lane A's
`# TERRA REVIEW …` — and `:3234` gates on `_REVIEW_TITLE_RE.search(txt)` plus the first
`branch_m`/`head_m`, which is the take-the-first-triple defect. `check_review_artifact_coverage` is at
`:3160` (the row's `:3117-3320` range holds). Filed today from N5 §4.
**CLASS: LIVE.**

**[E2] rollup — 35 rows: 33 LIVE · 2 AWAITING-RULING · 0 DEAD-CANDIDATE · 0 MALFORMED.** Theme
COMPLETE. This is the wave's largest theme and its **least harvestable**: not one row's Done-when reads
satisfied, and the three that came closest are partials whose *remaining* half is the load-bearing one
(`[#146]` doctrine-landed/sweep-owed, `[#417]` filter-landed/extraction-owed, `[#510]`
grammar-narrowed/roster-owed). Four structural findings:
(1) **`[#534]` is self-demonstrating** — its own repaired locators drifted again within 48 hours
(`:1862`→`:1863`, `:490`→`:491`, `:3779-3788`→`:3844`), and `audit.py` moved 4,271→4,341 lines. Any
disposition that ratifies a line-number locator will be stale before it is read.
(2) **`[#424]`'s census has now changed three times** (8/4 → 6/4/2 → live **4 clauses / 2 parse / 2
inert**) while the parser defect at `validate_backlog.py:83` has not changed at all — the row's
numbers rot, its defect does not.
(3) **`[#477]` reproduces inside this container** — the checkout is `dev-knowledge`, the registry key
is `.dev-knowledge`, so the hub cannot resolve its own row from a GitHub clone right now.
(4) **`[#497]` mis-teaches consumers**: `.pre-commit-hooks.yaml:74`, the declaration a consumer
installs, still advertises `block-ff-push` as fail-soft, a posture ADR-85 §A6 retired.
Cheapest genuine fixes in the theme, on evidence: `[#335]` (one placeholder exemption, one test),
`[#497]` (two prose corrections plus a test), `[#531]` (wire an existing validator at one point).
---

## [E3] Lessons feedback loop — 5 rows

**[#145] Codification-completeness pass** — ASK: an audit artifact enumerating what a fresh session
CANNOT do from PLAYBOOK + the handoff bundle alone, with every enumerated gap carrying a BACKLOG id
or a stated closure in that same artifact.
TARGET: **the closest candidate is today's and it does not satisfy the ask.**
`docs/audits/2026-08-19-technical-n5-codification-pack.md` landed this very night and is
codification-shaped, but its five verdict items are dispatch-runbook codification, the
parallel-default memo, the D8 memo, the review-artifact linkage gap and a session-lessons sweep —
`grep -n '145'` over it returns **zero**, and none of the five is the fresh-session-can't-do-X
enumeration across PLAYBOOK + the active bundle. No `docs/audits/*` file carries that enumeration.
**CLASS: LIVE.**

**[#266] Codify the test-scoped-grant language lesson** — ASK: state at BOTH
`templates/handoff/epic/EPIC_BOOT.md.tmpl` FILE-BOUNDARY and ADR-97 §14a that a narrow test-scoped
grant includes the mechanical count/pinning assertions the change forces.
TARGET: real, both conjuncts unmet. `EPIC_BOOT.md.tmpl:50` is `## FILE-BOUNDARY (hard)` and its
FILL-IN body reads only "May touch: … · May NOT touch: … A needed file outside the boundary → STOP,
escalate" — no count/pinning clause. `grep -in 'grant' docs/decisions/ADR-97-tree-orchestration.md`
returns **zero hits**, so §14a carries no grant-authoring language at all. The only
`mechanical count` hit in `protocols/` is `HANDOFF_PROCESS.md:1012`, an unrelated point about legs
with no mechanical counterpart.
**CLASS: LIVE.**

**[#443] Planning artifacts outside the three enforced classes carry no rent rule** — ASK: handoff
bundles, session plans and audit docs each get a stated rent/binding rule at their canonical home, or
a `STANDING_RULINGS.md` section naming `[#443]` recording them deliberately un-ruled.
TARGET: real and neither branch taken. `grep -in 'rent' protocols/HANDOFF_PROCESS.md
protocols/PLAYBOOK.md` returns only false positives on `current`/`different`/`apparent` — no rent
rule at either named home — and `grep '443' protocols/STANDING_RULINGS.md` returns **zero**, so the
deliberately-un-ruled escape is not taken either. The three enforced classes the row contrasts
against are all still live (`DEFINITION_OF_DONE.md` journal leg, ADR-105 activation, intake §7).
**CLASS: LIVE.**

**[#538] The NB4-C PLAYBOOK gap arc — twelve paste-ready acts** — ASK: land each of the 12 acts in
`protocols/PLAYBOOK.md` or record it declined with a reason, then re-run the coverage matrix.
TARGET: **re-measured live tonight and still zero.** Six of the act names counted over
`protocols/PLAYBOOK.md`, case-insensitively: `Honest-RED` 0 · `Land-then-delete` 0 · `Position 0` 0 ·
`integrator-on-a-clock` 0 · `single-flight` 0 · `adjudication hour` 0. The row's own claim ("0 of them
are in PLAYBOOK") reproduces exactly. Zero merge mentions on main; filed 2026-08-16 from
`docs/audits/2026-08-16-verification-nb4-playbook-gap.md`. The row is ruling-shaped — the drafts
exist, so the cost is a reading — but nothing has been read.
**CLASS: LIVE.**

**[#438] Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs** — ASK:
`protocols/PLAYBOOK.md` carries a refusal-gate class rule naming which arcs it binds and the questions
its pre-build design pass must answer, plus one `docs/audits/` record showing a design pass preceding
first implementation.
TARGET: real and unbuilt. `grep -ci 'refusal-gate|refusal gate' protocols/PLAYBOOK.md` returns **0**;
the only `fail-open` discussion in PLAYBOOK is incidental, not a class rule. The row's evidence base is
itself intact and unusually strong — the `[#436]` ratchet's 10-pass terra loop and the five fail-opens
that passed the suite (`5e655cc1`) — so the ask is a codification of an already-paid-for lesson.
Landed since 2026-08-15: `[#438]` appears in the batch-6 Done-when conversion merge `b4862b9be`
(2026-08-16), which converted the row's *Done-when text*, not the rule.
**CLASS: LIVE.**

**[E3] rollup — 5 rows: 5 LIVE · 0 AWAITING-RULING · 0 DEAD-CANDIDATE · 0 MALFORMED.** Theme
COMPLETE. `[#538]` is the highest-value of the five and the cheapest: 12 drafted acts awaiting a
reading, not authoring. `[#145]`'s near-miss against tonight's N5 pack is worth the architect's
attention — the artifact class is right, the enumeration axis is not.
---

## [E4] Decision management — 5 rows

**[#456] Ruling-blocked cohort sweep (ADR-108 §A re-route)** — ASK: enumerate the ~30 remaining
ruling-blocked rows as an explicit `[#id]` list **in this row**, then re-route each under ADR-108 §A,
list it operator-owned with a reason, or name it in a `STANDING_RULINGS.md` section citing `[#456]`.
TARGET: real and the enumeration has not happened. The row body names exactly **eight** ids
(`[#122] [#189] [#322] [#346] [#406] [#407] [#414] [#456]`) against a cohort the row itself sizes at
33 (18% of rows) — the three already re-routed plus five illustrative operator-owned cases, not a
list. `grep '456' protocols/STANDING_RULINGS.md` returns **zero**, so the third branch is untaken
too. Landed since 2026-08-15 that bears on it: **three of the eight ids the row names are now
`status: closed`** — `[#122]`, `[#406]`, `[#407]`, all closed today under the L-5 seat arc — so the
cohort is shrinking by attrition while the enumeration the Done-when demands still does not exist.
The other five read `open` (`[#189]` `[#346]` `[#414]`) or `deferred` (`[#322]`).
**CLASS: LIVE.**

**[#546] ADR-60's `docs/` taxonomy no longer describes the tree** — ASK: an appended amendment marker
re-scoping the enumeration (preserving Rule 5), or ADR-101 recorded as successor for the genre set —
and no living doc still asserting the six-folder taxonomy.
TARGET: **confirmed live by direct listing.** `ls docs/` returns exactly five entries — `archive
audits decisions handoffs intake` — while `ADR-60:32` and `:35` still assign roles to
`council-questions/` (INPUTS) and `research/` (WORKING), neither of which exists. The machine truth
sits in `scripts/validate_hermetization.py:102` `SANCTIONED_GENRES`, enforced at `:231`. ADR-60's two
existing amendment sections are both from 2026-05-27/28 (`:95`, `:137`, `:156`) and predate the
divergence — no marker addresses the genre enumeration, and no successor pointer to ADR-101 exists.
**CLASS: LIVE.**

**[#548] Intake #12's SETTLED ownership manifest is parked on a departed id** — ASK: give intake #12's
TIER-1/TIER-2 manifest a live carrier, or re-anchor its `trigger:` onto a live id or a date, and
repoint `[#329]`/`[#331]`/`[#332]`'s dangling `#328` references in the same act.
TARGET: real, verified this session. `docs/intake/2026-07-11-tech-ownership-manifest.md:3` is
`status: ACCEPTED` and `:7` is `trigger: "#328 build"`; `ls tasks/328-*` returns **no such file** and
`#328` appears in `BACKLOG.md` only three times, all as *inbound refs from the three dependents* —
so the peg's referent is gone and cannot fire. No carrier row exists.
**CLASS: LIVE.**

**[#549] The operator-approved Fleet-Hygiene plan-of-record (intake #13 v4) has no carrier** — ASK:
record intake #13 SUPERSEDED with [E9]/ADR-109 named as successor for the overlapping phases, or
re-anchor its `trigger:` onto a live id or a date.
TARGET: real and identical in shape to `[#548]`.
`docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md:3` = `status: ACCEPTED`, `:8` =
`trigger: "#328 build"`, referent absent. ADR-109 (Accepted, 2026-07-31) exists and is the named
successor candidate, so the *material* for the ruling is on the shelf; what is missing is the
disposition. The fork the row names — superseded-in-part vs re-anchored — is a decision, not work.
**CLASS: AWAITING-RULING** — decision: whether intake #13 is superseded-in-part by [E9]/ADR-109 or
re-anchored (per-clause), which the row states nothing in the corpus currently answers.

**[#550] Intake #14's ruled SIEM requirements outlived the ruling that shelved them** — ASK: mark each
ruled requirement clause shelved-with-reason / live-and-carried / dead, and stop the `trigger:` naming
a departed id.
TARGET: real. `docs/intake/2026-07-12-siem-requirements-ruled-pack.md:3` = `status: ACCEPTED`, `:7` =
`trigger: "#328 build"` — same departed peg as `[#548]`/`[#549]`, so all three are one defect with
three instances. The row's own collision is intact: the document is simultaneously the authority
BACKLOG's W-wave cites for a REJECTED item and an ACCEPTED doc with no carrier. No clause-level
disposition exists.
**CLASS: LIVE.**

**[E4] rollup — 5 rows: 4 LIVE · 1 AWAITING-RULING · 0 DEAD-CANDIDATE · 0 MALFORMED.** Theme
COMPLETE. **The theme's dominant fact is one defect with three instances:** `[#548]` `[#549]` `[#550]`
are all *the same departed peg* — `trigger: "#328 build"` on three ACCEPTED intake docs whose id has
no task file. An architect ruling on the peg policy (re-anchor to a date on the `[#322]` precedent)
would move all three at once; ruling them individually costs three times as much for the same
mechanism. `[#546]` is the cheapest single act in the theme — one appended marker on ADR-60.
---

## [E5] Canonical-file integrity — 11 rows

**[#227] Relocate `AGENT_FRAMEWORK.md` out of `protocols/`** — ASK: move the v0.1 stub to `docs/` and
repoint every inbound ref.
TARGET: real and unmoved — `protocols/AGENT_FRAMEWORK.md` exists, `docs/AGENT_FRAMEWORK.md` does not.
**The row's own premise has drifted, and this is the finding:** it asserts "no living doc references
it", but `protocols/README.md:18` lists it (`- 'AGENT_FRAMEWORK.md' — agent / subagent operating
framework`) — a living doc. The other inbound refs are all immutable (`protocols/archive/
HANDOFF_PROCESS_v4.4.md:450`, three `docs/handoffs/*/05_NOW.md`), so the move's true repoint cost is
one line, not zero.
**CLASS: LIVE.**

**[#263] Protocols/edge-map reconciliation residuals** — ASK: drop the `mermaid_theme_directive`
exempt entry + stale comment word from `ecosystem/doc-code-edge.yaml`, and resolve-or-record the two
stale ESSENTIALS refs, with `doc_code_coverage_drift` still OK.
TARGET: real, all three loci still live and one count is off. `ecosystem/doc-code-edge.yaml:115`
still carries `- mermaid_theme_directive`. `protocols/AI_COUNCIL_PROCESS.md:325` still reads
`per ESSENTIALS § "Repo artifacts in…"`. **The PLAYBOOK leg is smaller than the row says:** the row
claims "×2", live `grep -c 'English-only' protocols/PLAYBOOK.md` = **1** (`:645`) — one of the pair
was resolved without the row being updated. `grep '263' protocols/STANDING_RULINGS.md` = **zero**, so
the record-instead-of-fix branch is untaken.
**CLASS: LIVE.**

**[#269] Audit-index count-tiered shape + header repoint** — ASK: render the ADR-100 count-tiered
shape in the generated `docs/audits/README.md` and repoint its header from #212 to ADR-100.
TARGET: **half the ask is already landed and the generator says so in its own source.** The header
repoint is DONE — `docs/audits/README.md:5-6` names ADR-100 and `grep -c '#212'` over it = **0**. The
shape is not: `scripts/gen_audit_index.py:9-10` states "ADR-100 ALSO names a count-tiered index
shape, which is **not built here** — this module still groups by month", and the rendered index
carries the same disclosure at `:6` over **604 audit documents** flat-listed by month.
**CLASS: LIVE** (the residue is the shape only; the header conjunct is discharged).

**[#285] Extend hub freshness gating to PLAYBOOK** — ASK: `protocols/PLAYBOOK.md` gains
`last_reviewed` frontmatter, joins `_HUB_ONLY_FRESHNESS_FILES`, the test stops asserting its absence,
and the re-read is evidenced by per-section notes.
TARGET: real, none of the four conjuncts met. `protocols/PLAYBOOK.md` frontmatter is
`reconciled_with: handoff-process@6.2.0` **only** — no `last_reviewed`; the file still carries a prose
`> Last updated: 2026-08-01` line at `:7`. `scripts/audit.py:322` `_HUB_ONLY_FRESHNESS_FILES` lists
`SESSION_SETUP.md` and `AI_COUNCIL_PROCESS.md` and not PLAYBOOK. The row's guard against a cheap
close is intact and correct: "a bare stamp to green a gate is forbidden".
**CLASS: LIVE.**

**[#388] The "10–20 repo" fleet-scale target is FABRICATED** — ASK: every surface restating the figure
carries 5–8+ going forward, and the immutable four remain unedited with the correction record
standing.
TARGET: **both conjuncts read satisfied on a live scan.** A repo-wide grep for `10–20`/`10-20` finds
**no living surface restating it as a target**: the hits are the four immutable records the row
itself names (`docs/audits/2026-07-21-technical-night-vision-audit.md:341-342`, and
`PASTE_THIS.md:427,:653` / `RESIDUAL.md:164` / `SUPPLEMENT.md:109` in the two 2026-07 architect
bundles), later immutable audits *quoting the incident as a precedent*, grooming sheets quoting the
row's own title, and `docs/intake/2026-07-21-func-fleet-north-star.md:40,:102,:108,:126`, which names
the figure only to declare it fabricated. The correction record stands in living doctrine at
`docs/decisions/ADR-104-fleet-repository-shape.md:113` ("priced at the real 5–8+ … the '10–20 repo'
figure … is fabricated and is not used here"). The four immutable files were each last touched
**2026-07-21**, their creation date — unedited, exactly as the row requires.
**CLASS: DEAD-CANDIDATE** (evidence: no living surface restates the figure; the immutable four are
unedited at `2026-07-21`; the correction stands at `ADR-104:113`. The row was additionally **ruled
2026-07-28 "HOLD at P3, no bump, do not re-litigate"**, so its own governance already treats it as
finished business.)

**[#420] Does a TOP-LEVEL `docs/archive/` still make sense?** — ASK: rule the top-level archive
kept-with-a-restated-charter or dissolved into per-area homes, with each file given a destination.
TARGET: the question is unanswered and **its population has more than doubled since the row was
written**: the row says "9 external-research / scoping / evidence files", `ls docs/archive/ | wc -l`
returns **22**. `[#420]` is a named member of the L-5 PROSE-JUDGMENT carve-out
(`protocols/STANDING_RULINGS.md:1317`) and register `N2-D1-07` (`:1558`) cross-references it as the
owner "with its do-not-touch order quoted" — so the corpus already treats it as a pending ruling, not
pending work. Its own `Do NOT touch docs/archive/ while this is open` order is being honoured.
**CLASS: AWAITING-RULING** — decision: kept-with-restated-charter vs dissolved-into-per-area-homes
(operator/architect, L-5 carve-out member). Note the destination count the ruling must cover is now
22, not 9.

**[#506] Whole-set P10 grooming arc** — ASK: a `docs/audits/` sheet carrying one row per `status: open`
task with last-touch + closing-merge cross-check, **each id verdicted** live/dead/awaiting-ruling, and
every dead id closed per ADR-65 or named deferred.
TARGET: **this row is directly downstream of the sheet you are reading, and the honest answer is
"two of three conjuncts, and the third is not this lane's to give".** Conjunct 1 is met across two
artifacts: `docs/audits/2026-08-18-census-p10-grooming-evidence.md` carries the mechanical per-row
sheet (194 rows at its SHA), and the evaluative coverage is now N4's 72 plus this file's 116 = **179
of the 183 live `status: open` rows**, the residue being the 4 in-flight rows the contract excludes.
Conjunct 2 is **not** met and cannot be met by a lane: both sheets carry *RECOMMENDED* classes, and
the verdict is the architect's by every contract in the chain. Conjunct 3 (dead ids closed) is
untouched — this lane executes no closures.
**CLASS: LIVE** — with the note that its evidence half is now as discharged as a read-only lane can
make it; what remains is adjudication, not generation.

**[#526] Root-hygiene audit** — ASK: an audit artifact enumerating every sanctioned Tier-1 root entry
with a MUST-be-root / movable verdict and the tool-convention citation backing each.
TARGET: real and unwritten. No `docs/audits/*` file matches a root-hygiene or root-census slug, and
zero merge mentions on main. The row is scoped read-only by its own text ("no moves executed here"),
so it is a pure authoring act with no gate dependency — and its refusal-gate framing is correct:
`scripts/validate_hermetization.py` Rule A seals the Tier-1 top level, so a move without this census
would be a drive-by against a live gate.
**CLASS: LIVE.**

**[#542] `ARCHITECTURE.md` still claims four `doc_rot` sub-detectors** — ASK: `ARCHITECTURE.md` names
the five live categories, and `ecosystem/doc-code-edge.yaml` carries the claim so `doc_claims` fails
on disagreement.
TARGET: **confirmed by direct read, verbatim.** `ARCHITECTURE.md:427` still reads "Four read-only
sub-detectors — BACKLOG inline-history accretion, per-section Section-history accretion, file-bloat
vs a self-declared budget, grooming-cadence lapse". `scripts/validate_doc_rot.py` documents the split
at `:16` (ARM 1 `backlog-accretion`), `:23-25` (ARM 2 `backlog-row-length`, "Renamed out of
`backlog-accretion` because it was never accretion") and `:63`/`:67` — five categories live. The
`doc-code-edge.yaml` claim does not exist, so nothing catches the drift. The row's own provenance is
the finding: the debt was booked to a packet's "Owed" list, and a packet owns nothing.
**CLASS: LIVE.**

**[#551] Audit artifacts carry no `status:`** — ASK: a `status:` field on `docs/audits/*.md` with the
closed enum LIVE | CONSUMED | SUPERSEDED stated at a canonical home, read by the index generator, with
a named writer and the ADR-100 no-move invariant restated.
TARGET: real, and **the live corpus makes the case stronger than the row does.** `grep -n 'status'
scripts/gen_audit_index.py` returns **zero** — the generator reads no such field. But 59 of the 604
audits *already carry an ad-hoc `status:` frontmatter line* (e.g.
`docs/audits/2026-05-12-handoff-process-audit.md:5` → `status: complete`) on an **unruled value
outside the proposed enum** — so the field exists de facto, ungoverned, in ~10% of the corpus, which
is a worse state than absence and is not what the row describes. The batch-7a disposition ledger the
row names as the writer exists (`docs/audits/2026-08-17-technical-audit-disposition-ledger.md`).
**CLASS: LIVE.**

**[#553] `docs/decisions/README.md`'s ADR census is hand-maintained, ungated, and wrong twice** — ASK:
the census figures are machine-generated with a regen-and-diff gate (or carry a dated re-measurement
matching a live count), and the ADR-61 claim states the three-format parser hazard instead of
asserting an absent status line.
TARGET: real, both defects still on disk. `docs/decisions/README.md:30` still opens "**Measured at
declaration, so the enum describes the corpus rather than an intention:**" with no re-measurement, and
`:39` still asserts `ADR-61-git-worktree-parallel-sessions.md` "carries **no parsable status line at
all**". Live corpus is **86** `ADR-*.md` files. No gate covers this index — the regen-and-diff family
(`audit-index-freshness`, `claude-rosters-freshness`, `roster-freshness`) has no member for
`docs/decisions/README.md`.
**CLASS: LIVE.**

**[E5] rollup — 11 rows: 9 LIVE · 1 AWAITING-RULING · 1 DEAD-CANDIDATE · 0 MALFORMED** (`[#506]`
counted LIVE). Theme COMPLETE. **This theme carries the wave's only DEAD-CANDIDATE, `[#388]`** — both
Done-when conjuncts read satisfied on a live scan and the row was separately ruled HOLD/do-not-
re-litigate on 2026-07-28. Two rows are *partially* discharged and worth the architect's eye before
any lane is spent on them: `[#269]`'s header repoint is done (shape only remains) and `[#506]`'s
evidence conjunct is now as complete as a read-only lane can make it. Three rows carry a **stale
figure in their own body** — `[#227]` ("no living doc references it": `protocols/README.md:18` does),
`[#263]` ("×2": live count 1) and `[#420]` ("9 files": live 22) — none of which changes the ask, but
each of which would mislead an executor who trusted the row over the tree.
---

## [E6] Cross-repo universalization — 12 rows

**[#43] Decide + author a one-step new-repo scaffold** — ASK: record the decision, and author
`templates/new-repo-skeleton/` (ADR + templates, no scripts) if approved.
TARGET: `ls templates/new-repo-skeleton` → **no such file**, and the requirements spine the row was
folded into, `docs/intake/2026-07-08-func-new-project-bootstrap.md:3`, is still `status: SEED` — the
earliest intake state, not ACCEPTED. So the *decision* the row's Done-when leads with has not been
taken, and the build half is conditional on it. Zero merge mentions on main in 1,189 first-parent
merges.
**CLASS: AWAITING-RULING** — decision: whether to author a new-repo scaffold at all (intake #6 must
advance past SEED before the build half can be scoped).

**[#244] Essence-spec lifecycle epic** — ASK: a tombstoned component's artifacts demonstrably REMOVED
from a consumer and verified ABSENT, the roster regenerating without it, and per-repo drift surfacing
in `fleet_health`.
TARGET: P1–P4 shipped per the row (4 merges on main, `25b104ed6` / `a7504565f` / `2c8695183`,
2026-07-04); the manifest series is live through `deploy/manifest-v1.4.0.yaml`, and the remove leg is
real in code — `deploy/tool.py:407`, `:475`, `:652`, `:983` are all `status:removed`-driven. The row's
own residue is explicit and unowned: "**P5 hub self-prune · P6 fleet (both UNOWNED — #221 closed at
8aab4356; no successor)**", and `grep 'self-prune'` over `deploy/` and ADR-96 returns **zero**.
**CLASS: LIVE** (residue = P5/P6, both unowned by the row's own text).

**[#245] Add-path status-awareness** — ASK: the deploy add-path skips re-adding a `status: removed`
component with no manual add-target drop, AND a source-drifted prune target classifies against
last-deployed bytes, with tests.
TARGET: **the second conjunct has landed for one carrier and the first has not.** The last-deployed
oracle exists — `deploy/carrier_precommit.py:707` ("the last-deployed-shape oracle
(`expected: {rev, hooks}`)"), `:716`, `:759` ("True iff the consumer repo entry byte-matches the
last-deployed shape") and `deploy/contract.py:124` `PRESENT_CLEAN`. No `apply()` on any carrier
(`carrier_docs:240`, `carrier_floor:884`, `carrier_globalconfig:188`, `carrier_mesh:274`,
`carrier_plugin:323`, `carrier_precommit:849`) consults `status: removed` — the add-path is still
blind, exactly as the row states. Zero merge mentions.
**CLASS: LIVE.**

**[#276] D2 per-consumer waiver-honoring** — ASK: a consumer-declared divergence causes BOTH the prune
sweep to SKIP and the add/converge leg to NOT re-append, with tests.
TARGET: real and unbuilt on the decisive point — **`grep -rn 'methodology.yaml' deploy/*.py` returns
zero**, so neither deploy leg reads the allowlist; the only `divergence` hit in `deploy/` is
`carrier_precommit.py:761`, a byte-match comment about the prune oracle, not a waiver. The row's
prediction therefore still stands unchanged: `--execute` would re-append `codemap-freshness` to
consumers that legitimately exclude it. Zero merge mentions.
**CLASS: LIVE.**

**[#327] Protocols-as-interface genre ruling** — ASK: `protocols/` documented as the interface genre
AND each onboarded repo carries `protocols/README.md` + ≥1 interface doc (n≥1, corp included).
TARGET: **the hub half is done and the residue is off-tree.** `protocols/README.md:5` reads
"`protocols/` — canonical universal-methodology genre (hub)", the genre wording the row's Lane D note
says already existed. The unmet half is a consumer-repo merge — corp branch
`docs/327-interface-genre-markers` @ `4c7d7f4`, recorded UNMERGED — which **this repo cannot verify or
land**: Layer 2 never drives a child repo's state (CLAUDE §5 rule 4). Zero merge mentions here, which
is expected rather than informative for a row whose residue lives in another repo.
**CLASS: LIVE** (blocked off-tree; the hub-side conjunct is discharged).

**[#329] VS Code ownership visualization** — ASK: a generator emits `.vscode` folder icon/color config
from the #328 manifest for ≥1 repo and regenerates deterministically.
TARGET: real and unbuilt — no such generator exists in `scripts/`. **But its stated input is a
departed id:** the row derives from "the #328 fleet_parity manifest", and `ls tasks/328-*` returns no
file (the same departed peg `[#548]` documents for three intake docs). The live substitutes the row
also names — `ecosystem/parity-surfaces.yaml` and `.methodology.yaml` — do exist, so the ask is
buildable, but the row's provenance sentence points at nothing.
**CLASS: LIVE** (with the `#328` reference defect `[#548]` already owns).

**[#331] Consumer BACKLOG schema adoption ruling** — ASK: a recorded ruling stating, per consumer,
adopt-at-P6 vs accept-durable, declared in `.methodology.yaml` via the #328 mechanism.
TARGET: the row is a DECISION ticket by its own first clause ("A DECISION ticket, not the execution")
and no ruling is recorded — zero merge mentions in 1,189 merges, and its declaration vehicle (#328)
is the departed id above. Its named dependency `[#281]` (the ai-council re-peg) **closed today** under
the L-5 seat arc, which removes one of the two blockers it cites.
**CLASS: AWAITING-RULING** — decision: per consumer (ai-council, corp-monorepo), adopt-the-hub-story-map
at P6 vs accept-durable-divergence (ADR-99 clause A / register b1).

**[#332] Fleet dependency-version parity** — ASK: a versioned dependency manifest ships with the
methodology package AND an automated check WARNs a version-drifted consumer while an at-parity one
does not, with a test.
TARGET: real, and the row already records its own partial honestly — "ARC-A: corp pytest-xdist
declared+installed (sanctioned one-time bootstrap …) — **STAYS OPEN, Done-when clause-1 (deploy
carrier / ships-with-package) unbuilt**". That remains true: the manifest series
`deploy/manifest-v1.0.0` … `v1.4.0` carries components, not a dependency-version set. The row's most
recent merge mention is `2bc02196c` (2026-07-13), the `#328` checker landing — a *sibling*, not this.
**CLASS: LIVE.**

**[#334] Fleet-wide ruff hook id migration `ruff` → `ruff-check`** — ASK: all three repos use
`ruff-check`, the legacy `ruff` alias gone, witnessed per repo by a staged violating `.py` BLOCKED
under the new id.
TARGET: **unmigrated in the one repo this lane can measure.** `.pre-commit-config.yaml:241` still reads
`- id: ruff`. The other two repos are off-tree and unverifiable from here. One merge mention
(`97cf58e06`, 2026-07-12) and it is the *filing* commit, not an implementation.
**CLASS: LIVE.**

**[#351] Fleet-Python-upgrade ticket (RULING-PY)** — ASK: an audit artifact defining the coordinated
upgrade path across every `adr104-fleet-members` entry, and the baseline raised for all of them in one
arc (ruff `target-version` + the `pyproject.toml` required-version floor moving together) — or a
`STANDING_RULINGS.md` section naming `[#351]` with a next-review date.
TARGET: **the row's own marker is still in the file it governs.** `pyproject.toml:176` reads
`target-version = "py311"  # RULING-PY baseline; "always newest Python" lift = #351`, against
`requires-python = ">=3.12"` at `:15` — the two knobs the Done-when requires to move together are
currently one minor version apart. No coordinated-path audit artifact exists, and
`grep '351' protocols/STANDING_RULINGS.md` finds no section naming it (the single hit at `:129` is an
unrelated applied-instances line).
**CLASS: LIVE.**

**[#430] Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on outside
state** — ASK: (a) the conftest ruling cited in `ecosystem/parity-surfaces.yaml` at the affected row,
(b) two ship-gate runs on the same subject state from different checkouts producing the same verdict,
pinned by a test **that varies the surrounding state**.
TARGET: **(a) is landed and citable, (b) is not.** `ecosystem/parity-surfaces.yaml:292` carries the
comment `# [#430](a) -- root conftest.py: PERMITTED FLEET-WIDE, MANDATED NOWHERE (operator …)`, with
the surface `- id: root-conftest` at `:307` and `declared_by: ruling-2026-08-07-root-conftest` at
`:310` — the missing locator the row asked someone to confirm now exists. For (b),
`tests/test_fleet_parity.py:1195` `test_determinism_two_runs_identical` runs the gate twice against
**identical** fixture state (`f1 == f2`) — it pins repeatability, not independence from sibling state,
which is the property (b) names. 13 merge mentions, the most recent `8c9163e0b` (2026-08-15).
**CLASS: LIVE** (residue = (b) only).

**[#559] Kernel/lab check tiering + `dev-knowledge-kernel` as an installable package** — ASK: every
`ALL_CHECKS` member carries a `kernel`/`hub` tier; `dev-knowledge-kernel` is installable from the hub
at a git tag and ≥1 consumer resolves it as a pinned dependency; the package pins `requires-python` +
uv `required-version` and exposes a shared ruff config consumers `extend`.
TARGET: real and entirely unbuilt — `grep -rn 'dev-knowledge-kernel' --include=*.py --include=*.toml`
returns **zero**, and `scripts/audit_checks/registry.py` carries no `tier` field. The row's own
liveness claim reproduces exactly. Filed 2026-08-19 (`7e793eca8`, today's seat arc) as the fleet's
oldest ACCEPTED-unfiled debt (intake #25 W-2, ACCEPTED 2026-08-05).
**CLASS: LIVE** — and note the coupling the row states: `[#332]`, `[#334]` and `[#351]`, three other
LIVE rows in this same theme, are all waiting on the one-version-bump mechanism this row defines.

**[E6] rollup — 12 rows: 10 LIVE · 2 AWAITING-RULING · 0 DEAD-CANDIDATE · 0 MALFORMED.** Theme
COMPLETE. **The structural finding is a dependency star, not twelve independent rows:** `[#559]`
defines the fleet-wide toolchain pin that `[#332]`, `[#334]` and `[#351]` each separately wait on, and
`[#244]`/`[#245]`/`[#276]` are three consecutive legs of one deploy-path defect (add-path blind to
`status: removed`, no waiver read, P5/P6 unowned). Two rows are partially discharged and the partial
is the useful part: `[#430]`'s (a) locator now exists at `parity-surfaces.yaml:292-310`, and `[#327]`'s
hub conjunct is met with only an off-tree consumer merge outstanding. Two rows point at the departed
`#328` (`[#329]`, `[#331]`) — the same defect `[#548]` owns for the intake docs.
---

## [E7] Tooling & evaluation — 28 rows

**[#123] Routine observability convention + value review** — ASK: the `Routine: <name>` marker
convention recorded in PLAYBOOK, every `routine_consumers`-declared routine carrying it, and one
value-review audit recording per-routine findings-acted-on vs noise.
TARGET: **conjunct 1 is landed; 2 and 3 are not.** `protocols/PLAYBOOK.md:2409` records
"**`Routine: <name>` commit trailer** on every automation commit … (#123)", and `:2332` says outright
"*Wiring is captured as a follow-up item — not built in the ratifying session.*" Live: **zero** of the
last 300 first-parent commits carry a `chore(routine…)` scope or `Routine:` trailer, and no
value-review artifact exists in `docs/audits/`.
**CLASS: LIVE** (residue = wiring + the value review).

**[#271] Nightly proposal loop** — ASK: the loop runs nightly under a `· routine:` block that
`routine_consumers` passes with `[#270]`'s load-gauge live; each of the four §6 constraints enforced by
a check or test; and a 2-week survival review with a measured accept-rate against the <20% kill
threshold.
TARGET: real, unbuilt, with one blocker cleared. `tasks/270-*.md` is `status: closed`, so the
load-gauge precondition is met. But **`[#271]` carries no genuine routine block**: the only four rows
in `tasks/` whose text contains `· routine: trigger=` are `[#348]`, `[#426]`, `[#461]` and `[#552]` —
`[#271]`'s apparent hit is the phrase *inside its own Done-when*. No check enforces the cap, the
7-day expiry, or the SEED-landing rule, and no survival-review artifact exists.
**CLASS: LIVE.**

**[#274] Dogfood-signal prior in the `/changelog-review` ADOPT rubric** — ASK: the rubric names the
dogfood-signal prior, and one subsequent digest cites it by name against ≥1 classified item.
TARGET: real and unbuilt — `grep -ci 'dogfood' .claude/commands/changelog-review.md` = **0**. Three
changelog-review digests exist (2026-06-07, 2026-06-15, 2026-07-06), none of which can cite a prior
the rubric does not carry. Smallest row in the theme by a wide margin.
**CLASS: LIVE.**

**[#278] Test-suite hygiene epic** — ASK: both intake ACs hold with their text quoted in the closing
commit, the theatricality review ships as a `docs/audits/` artifact, and impacted-test selection is
live in the verify cadence with a test.
TARGET: real and unbuilt on every leg — no `docs/audits/*` file matches a theatricality or
test-suite-hygiene slug, and `grep -rn 'impacted' scripts/*.py` returns **zero**, so no selection
mechanism exists. The row's PRECONDITION (answer *why the suite got faster* with evidence before any
cleanup) remains unanswered, and it is the conjunct that makes this row unsafe to close cheaply.
**CLASS: LIVE.**

**[#338] codex-review drift consolidation** — ASK: each of (b) invalid bare `gpt-5.6`, (c) the
wrapper under version control, (d) the stale README, (e) the read-only-sandbox HALT — resolved with
evidence, or a `STANDING_RULINGS.md` section naming `[#338]` per item.
TARGET: `grep '[#338]' protocols/STANDING_RULINGS.md` = **0**, so the record-instead-of-fix branch is
untaken. **Honest limit of this lane:** legs (b)–(e) all target `~/.claude/bin/codex-review.ps1`,
which **does not exist in this container** (`ls` → no such file) because `~/.claude` here is not the
operator's machine. Leg (c) — bring the wrapper under version control — is itself the reason the
evidence is unreachable from a cloud lane, which is a datum in the row's own favour.
**CLASS: LIVE** (legs (b)/(d)/(e) unverifiable from here; leg (c) verified unmet by that very fact).

**[#387] Rewrite the buy-vs-build intake before anything ingests it** — ASK: the archived
platform-feature-scan intake carries the ruled position (amendment marker) or a superseding intake
exists and the old one's `status:` names it, AND no ADR cites the un-rewritten doc.
TARGET: **the second conjunct is measurably violated right now.**
`docs/intake/archive/2026-07-06-platform-feature-scan.md:3` reads `status: CONSUMED` with no
amendment marker and no superseding pointer, and
`docs/decisions/ADR-98-intake-pipeline.md:77` cites it by name ("intake-id 2
(`platform-feature-scan` → consumed by #272)") as part of the n=2 hardening evidence. The row's
liveness argument also holds: `[#371]` still names the buy-vs-build ADR as its deciding vehicle, so
the stale recommendation sits upstream of open work.
**CLASS: LIVE.**

**[#409] Standing night batch — CODE review (formalize as routine)** — ASK: an ADR-105 `· routine:`
block with all six fields that `routine_consumers` passes, or a `STANDING_RULINGS.md` §-section naming
`[#409]`, or a disposition token.
TARGET: real and unformalized. `[#409]` carries **no** genuine routine block (verified against the
`· routine: trigger=` predicate — only `[#348]` `[#426]` `[#461]` `[#552]` do). The
`STANDING_RULINGS.md` hits at `:1353` and `:1584` are the **L-8 fold ruling** ("`[#409]`/`[#410]`/
`[#411]` stay distinct → NIE"), which declines a *merge of the rows* and is emphatically not a
disposition of the routine — a distinction worth stating because the id appears in the file and a
grep-only pass would read it as discharged.
**CLASS: LIVE.**

**[#410] Standing night batch — ARCHITECTURE review** — ASK: identical shape to `[#409]`, over shape
rather than diff.
TARGET: identical evidence — no routine block, and the only `STANDING_RULINGS.md` mention is the same
L-8 fold NIE. The two rows are deliberately distinct by that ruling, so neither can borrow the
other's discharge.
**CLASS: LIVE.**

**[#411] Standing night batch — creative session + recurring Q&A cadence** — ASK: the creative-session
batch **and** the recurring Q&A cadence each carry a passing `· routine:` block, or each is ruled out.
TARGET: identical evidence to `[#409]`/`[#410]`, with a wider conjunction (two routines, not one)
because `[#348]`'s half (c) was folded here in 2026-07-25. Neither routine exists.
**CLASS: LIVE.**

**[#412] Subagent / workflow routing + configured fan-out + online research** — ASK: an audit artifact
capturing Anthropic's published command/skill set with a per-item fleet-adoption verdict, AND a routing
doctrine in PLAYBOOK; or a `STANDING_RULINGS.md` deferral section.
TARGET: real and unbuilt. No `docs/audits/*` slug matches an Anthropic-organ or routing survey;
`grep -in 'routing doctrine|when to fan out' protocols/PLAYBOOK.md` = **0** (PLAYBOOK's 14 `fan-out`
hits are operational mentions, not a doctrine section); `grep '412' protocols/STANDING_RULINGS.md` =
**0**. Filing-only by its own text ("Filing only, zero build"), so no work was expected — but nothing
has moved either.
**CLASS: LIVE.**

**[#415] Tests must bind fixtures, not live mutable repo content** — ASK: an audit artifact enumerating
every test that reads live repo content, each re-pointed or listed as an intentional integration smoke
test with a reason; or a blanket `STANDING_RULINGS.md` section naming `[#415]`.
TARGET: **the triggering instance is fixed and the enumeration is not.**
`tests/test_validate_backlog.py:361` `test_dedup_specificity_holds_on_a_distinct_fixture` exists (the
re-point the row records), and `:163` `test_live_backlog_passes_inplace_check` still reads live
content — the sibling the row calls "plausibly a distinct class". No enumeration artifact exists
(`docs/audits/2026-07-25-codex-fix-live-backlog-test.md` is the fix record, not the census), and the
`STANDING_RULINGS.md` hits are the L-8 fold NIE, not a blanket reason.
**CLASS: LIVE** (residue = the ~10-test enumeration, which the row explicitly scopes as
enumerate-do-not-fix).

**[#426] Declare `consumer` + `consumption_path` for every LIVE routine** — ASK: every live routine
declares a consumer and consumption path or is retired; the dead-producer nags resolved; and
`routine_consumers`' stated boundary closed or recorded permanent-defer-with-reason.
TARGET: partially moved and structurally open. This row **does** carry a genuine `· routine:` block
(`trigger=operator night-batch request … review_date=2026-08-26`) — one of only four in `tasks/` —
so it declares itself, but its subject is the **30 hooks and schedules that are not BACKLOG rows**,
none of which the gate can see. The dead-producer half moved on 2026-08-16 (`b150bfe41`,
"K1 declares, 14 permanent-defer re-annotations"; `fa746e14b`, "15 nightly-triage Issues closed"), and
`.claude/settings.json:37` still wires `surface_triage.ps1` at SessionStart. Note its own
`review_date` falls **2026-08-26**, one week out.
**CLASS: LIVE.**

**[#428] `nightly-triage` reports a dead producer to every session start** — ASK: no session-start
surface asserts pending work from a producer with no run in 30 days (with a test seeding a dead
producer), AND the Issue backlog closed out or `surface_triage.ps1` no longer reading it, with the
count recorded in the commit.
TARGET: **the second conjunct now looks discharged and the first is untouched — the sharpest
wave-2 harvest signal in E7.** `7257f4fe` (2026-08-16) is literally "close 15 nightly-triage Issues
(D4/D5)", merged at `fa746e14b`, which is the count-in-the-commit the Done-when asks for; and the
producer's absence is confirmed — `.github/workflows/` holds only `report-only-wall.yml`. Leg 1 is
not built: `grep -in 'stale|last run|dead|days' scripts/surface_triage.ps1` returns **zero**, so
nothing distinguishes "ran clean" from "never ran", and `tests/test_surface_triage.py` seeds no dead
producer. The row's own text still says "Leg 2 is PARTIAL" — that text is now stale in the row's
favour.
**CLASS: LIVE** (residue = leg 1 only; the architect may want to re-read leg 2 against `7257f4fe`).

**[#440] Make the `tasks/` id ledger tamper-evident** — ASK: a deleted retired record FAILs the gate,
with a test seeding a retirement then deleting the file.
TARGET: real, unbuilt, and **self-documented in the module that would carry it**:
`scripts/gen_task_tree.py:700` reads "tombstone record and is [#440]; ADR-107 §6.3 already records the
directory as 'not …'". `:404` and `:452` confirm the prune path that deleted retired files is gone but
nothing declares which files ought to exist. Live corroboration from this lane's own census: `tasks/`
holds 292 `NNN-*.md` files against 207 manifest entries, i.e. **84 retired/closed records whose sole
protection is that nobody deletes them**.
**CLASS: LIVE.**

**[#445] `codex-review` wrapper path-guard reports SUCCESS having reviewed nothing** — ASK: a mixed
diff can no longer report as reviewed while its prose went unreviewed — fail-loud or dual-route — with
a test seeding a docstring-only `.py` beside prose.
TARGET: same container limit as `[#338]` — the target is `~/.claude/bin/codex-review.ps1`, absent
here. What is verifiable: `grep '[#445]' protocols/STANDING_RULINGS.md` = **0** (no accepted-with-reason
record), and the witnessed evidence the row cites is a committed artifact
(`docs/audits/2026-07-29-codex-postflip-fix-batch-review.md`). Silent-success is the failure mode the
row names, and nothing in-tree contradicts it.
**CLASS: LIVE** (mechanism unverifiable from a cloud lane; no disposition recorded).

**[#453] Cloud night-run runbook — the container gaps** — ASK: `SESSION_SETUP.md` (or a named cloud
runbook) records the three container gaps with a workaround each, and a preflight performs the
unshallow and asserts the `uv` pin with a test; or a `STANDING_RULINGS.md` section naming `[#453]`.
TARGET: **this lane reproduced gap (1) tonight, which is about as live as evidence gets.** The
container arrived a **shallow clone** — `.git/shallow` present, `git rev-list --count main` = **299**
against a real 5,328, and only 65 first-parent merges visible versus 1,189 after
`git fetch --unshallow`. Had this sheet been derived pre-unshallow it would have reported 73 wave-2
rows as git-silent instead of 18 — wrong in the reassuring direction, exactly the trap the row names.
Meanwhile `grep -in 'unshallow|shallow|cloud' protocols/SESSION_SETUP.md` = **0** and
`grep '[#453]' protocols/STANDING_RULINGS.md` = **0**: nothing is recorded, so every cloud lane
rediscovers it. (N5's lane hit the identical gap tonight and recorded it in its own §0.)
**CLASS: LIVE** — and on this evidence the highest-value P2 in the theme relative to its cost.

**[#463] win-tooling onboarding debt** — ASK: `python scripts/audit.py repo win-tooling` reports no
FAIL/WARN from the four named checks, or a `STANDING_RULINGS.md` section naming `[#463]` with an
accepted reason per item.
TARGET: unresolved, and **now un-measurable by the Done-when's own instrument**: the row's evidence
base is `ecosystem/win-tooling/history/`, which holds exactly **one** file, `2026-07-31.md` — the
baseline stream stopped 19 days ago (see `[#493]`). `grep '[#463]' protocols/STANDING_RULINGS.md` =
**0**. Consumer-repo work, queue-only here by ADR-41.
**CLASS: LIVE** (blocked on the silent baseline `[#493]` diagnoses).

**[#464] corp-*/ai-council governance drift — five findings** — ASK: each of the five findings absent
from its repo's **next fleet baseline**, or a `STANDING_RULINGS.md` section naming `[#464]` with an
accepted reason per finding.
TARGET: the Done-when names an artifact that has not been produced since **2026-07-31** — every
`ecosystem/*/history/` directory ends on that date (ai-council n=17, corp-monorepo n=15, corp-ops
n=14, corp-sca-time-automation n=14). So the row cannot be discharged by evidence until the scheduler
runs again, and `grep '[#464]' protocols/STANDING_RULINGS.md` = **0**. The row's own EVIDENCE GAP note
(51 unpushed baseline commits) compounds this.
**CLASS: LIVE** (blocked on `[#493]`, same as `[#463]`).

**[#487] Closure-proposal consumption arc** — ASK: legs (i)–(iv) land in both `propose_closures.py` and
the `plugins/tier1-lifecycle` copy with a lockstep test, a ranked sheet covers every parked proposal
with a verdict per id, and a routine declaring `consumer:`/`consumption_path:` passes
`routine_consumers`.
TARGET: leg (iii) is directly falsifiable and unbuilt — `scripts/propose_closures.py:51` still reads
`CLOSES_RE = re.compile(r"\b(?:closes?|closed|fixes?|fixed)\s+\[#(\d+)\]", re.I)`, i.e. `fixes?`, so
bare `fix [#N]` is still missed exactly as the row says; `since_commit` is still the pin
(`:185`, `:315`, `resolve_window` at `:329`). **Honest limit:** the "149 parked" population is
invisible here — `logs/PROPOSALS-*.md` is gitignored (`.gitignore:26`) and `logs/` holds only
`TOKEN-LOG.md` in-tree, so the parked count cannot be re-derived from a clone.
**CLASS: LIVE.**

**[#491] Gemini scanning lane — ruling R-G plus an acceptance contract** — ASK: `STANDING_RULINGS.md`
carries the R-G ruling in a section naming `[#491]`, and one acceptance run over real work is recorded
in a `docs/audits/` artifact naming the spot-verified rows and the outcome.
TARGET: `grep '[#491]' protocols/STANDING_RULINGS.md` = **0** — the ruling half, which is the row's
first conjunct and the cheaper one, has not been written. No acceptance-run artifact exists. The row's
substrate is real (`[#487]`'s ranked sheet is a named candidate subject) but `[#487]` is itself LIVE,
so the acceptance target is not yet available.
**CLASS: AWAITING-RULING** — decision: R-G itself (whether the Gemini CLI is admitted as a
retrieval-only scanning lane, Antigravity excluded pending the identity question).

**[#493] B-2 investigation — the scheduled fleet-baseline task has been silent 10+ days** — ASK: a
`docs/audits/` artifact naming the cause with its evidence command, and naming the signal that would
have surfaced the silence within one cadence, with that signal filed or landed.
TARGET: real, undiagnosed, and **the silence has grown**. Both cited scripts exist
(`scripts/fleet-baseline.task.xml`, `scripts/setup-fleet-scheduler.ps1`), and every
`ecosystem/*/history/` stream ends at **2026-07-31** — **19 days** as of 2026-08-19, against the row's
"10+ days" at filing. No diagnosis artifact exists. This row is the upstream blocker for `[#463]` and
`[#464]`, whose Done-whens both name a fleet baseline that is not being produced.
**CLASS: LIVE** — three rows unblock behind it.

**[#509] `Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR`** — ASK: the wrapper resolves
`<PROMPTS_DIR>` / `$env:CLAUDE_PROMPTS_DIR` (default `~/Downloads`) in either shape, with a test, and a
variable-form dispatch line launches unedited.
TARGET: the hub-side half of the contract is intact and documented —
`protocols/PLAYBOOK.md:2050` states the override variable and `:2054` names
`scripts/dispatch/Invoke-Dispatch.ps1` as the resolver — but the wrapper lives in **win-tooling**, so
the build half is off-tree and unverifiable here. The row declares this itself ("Cross-repo: filed
from `.dev-knowledge`, built in `win-tooling`; no hub code changes").
**CLASS: LIVE** (off-tree build; nothing in the hub blocks it).

**[#523] Executive-index render leg on the generated `BACKLOG.md`** — ASK: `BACKLOG.md` opens with a
P1→P3 index, one line per live row; `--check` still byte-verifies; `--roundtrip` still proves
losslessness; and a `--status` mode prints velocity + horizon + top-priority ids.
TARGET: real and unbuilt. `BACKLOG.md`'s opening is the generated banner, "Big picture" prose and the
theme backbone, then straight into `## [E1]` — **no index**. `scripts/gen_task_tree.py` carries
`--roundtrip` (`:36`, `:51`) and `--check`, so the two preservation conjuncts already hold, but there
is no `--status` mode. The row's framing is worth keeping: this is a renderer defect on an
already-owned generator, not a new machinery family.
**CLASS: LIVE.**

**[#528] Lane-latency — the full suite multiplied across a batch** — ASK: (1) gate-run call sites use
`-n auto --dist worksteal` or a recorded reason, (2) the tiered-suite rule written in
PLAYBOOK/ESSENTIALS, (3) `test_run` duration events landing via the telemetry leg.
TARGET: **legs 1+2 are merged and leg 3 is explicitly owed — the row says so in its own body and the
tree agrees.** `pyproject.toml:93` records "`[tool.pytest.ini_options]` addopts is `-n auto`
(parallel by default…)" with the 5.2× A/B at `:156`, and the row's own INTEGRATION note dates legs 1+2
to `7d1f6ce0` (2026-08-15). Leg 3 is not landed: `scripts/telemetry_emit.py:7` states plainly that
`test_run` is the memo's **Stage 2** and that the module is "nothing more" than `emit_event()`. The
row also records a live doc defect — `PLAYBOOK.md` L844/L866 "still call the two night-2 audits
unmerged drafts".
**CLASS: LIVE** (P1; residue = leg 3, itself sequenced after the excluded `[#529]`).

**[#539] `gen_lane_contract.py` — assembly-not-generation with a `--check` leg** — ASK: the script
assembles the mechanical regions of a lane contract from the batch manifest, leaves judgment regions as
FILL-IN, and its `--check` leg refuses an off-enum branch name or an unresolvable locator, with a test
each.
TARGET: real and unbuilt — `ls scripts/gen_lane_contract.py` → **no such file**, and the name has zero
occurrences anywhere in `scripts/` or `protocols/`, reproducing the row's own liveness check. The
design point stands: the `--check` leg would **arm two organs wired into no gate**
(`validate_branch_naming`, `preflight_contract`) rather than create a third. Zero merge mentions.
**CLASS: LIVE.**

**[#541] Scale-out substrate decision — unowned after two reports** — ASK: a ruling recording the
chosen scale-out substrate with its crossover rule and time-to-deploy, or the decision deferred with a
dated peg, citing the v2 report's option set.
TARGET: the input exists and is committed —
`docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate-v2.md` — and nothing consumes it. Zero merge
mentions in 1,189 merges. This is a decision with a priced option set and no owner, which is the row's
own diagnosis ("A priced recommendation with no owner is how a spend decision quietly expires").
**CLASS: AWAITING-RULING** — decision: which scale-out substrate to rent (or a dated deferral),
against the v2 report's option set. Note `[#561]` explicitly does **not** answer it.

**[#555] Closing campaign batch 1 + kill-candidates instrument** — ASK: the first batch closes
**net-negative** — closures strictly greater than births — measured against the live denominator at
that batch's close, both figures re-derived.
TARGET: real, and **its premise (three disagreeing denominators) reproduces exactly tonight**:
`tasks/*.md` frontmatter gives **183 `status: open`**, the `tasks/manifest.json` active list gives
**207** (open ∪ 24 deferred), and the P10 sheet's own self-check recorded a third pairing (194 open /
218 active) at its SHA eight days ago. So the "name ONE predicate" first act is still owed, and the
figures have moved since the row was written — which is itself the argument for mechanizing the gauge.
P1. Filed under today's window.
**CLASS: LIVE.**

**[#561] Re-base the compute plan onto the Hetzner CX shared line** — ASK: intake #32 carries an
amendment or superseded-by pointer naming intake #39, and no live doc cites a CCX price as current.
TARGET: real, unmet, and cheap. `docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md`
is `status: ACCEPTED` (`:3`) and contains **zero** references to intake #39 or its filename — no
amendment, no superseded-by. The correcting evidence is already committed at
`docs/intake/2026-08-17-tech-off-machine-agent-substrate.md:21-23` and `:36` (CCX rose 2.13×–2.73×, CX
only ~1.3×–1.4×; "Switch the spec to the CX shared line"), and the ERRATUM precedent the row cites is
live in intake #25's `decided-by`. The row's own cost argument holds: acting on #32 as written budgets
roughly 3× the real spend.
**CLASS: LIVE** — the cheapest correction-of-a-live-authority in the wave.

**[E7] rollup — 28 rows: 26 LIVE · 2 AWAITING-RULING · 0 DEAD-CANDIDATE · 0 MALFORMED.** Theme
COMPLETE. **Four findings the architect should not have to re-derive:**
(1) **`[#493]` is a blocker for two other rows** — the fleet-baseline stream stopped 2026-07-31 (19
days), and `[#463]`/`[#464]` both name "the next fleet baseline" in their Done-whens, so neither can
be discharged until the scheduler is diagnosed.
(2) **`[#428]`'s leg 2 looks landed** (`7257f4fe`, "close 15 nightly-triage Issues", count in the
commit) while its own body still calls leg 2 PARTIAL — a row stale in its own favour.
(3) **`[#453]` was reproduced live by this lane tonight** (shallow clone, 65 visible merges vs 1,189
after `--unshallow`), and nothing about it is recorded in `SESSION_SETUP.md` or `STANDING_RULINGS.md`.
(4) **Three rows target `~/.claude` or `win-tooling` and are unverifiable from a cloud lane**
(`[#338]`, `[#445]`, `[#509]`) — stated as a limit, not scored as evidence. Partial discharges worth
reading before dispatch: `[#123]` conjunct 1, `[#415]`'s re-point, `[#523]`'s `--check`/`--roundtrip`,
and `[#528]`'s legs 1+2.
---

## [E8] ARC-5 execution — 10 rows

**[#357] Silent-rule census run 2 (the ADR corpus)** — ASK: every `must|shall|never` occurrence in
`docs/decisions/ADR-*.md` enumerated in the sweep artifact and stated in
`ecosystem/silent-rule-baseline.yaml`, with the combined denominator + N_silent replacing the [E8]
figures and `silent_rule_ratchet` green at the new numbers.
TARGET: real and unrun. `docs/audits/` carries three silent-rule artifacts — the run-1 ledger
(`2026-07-19-census-silent-rule-ledger.md`) and two ratchet-arming records — and **none sweeps the
ADR corpus**. `ecosystem/silent-rule-baseline.yaml:21` reads `baseline: 441` (prior 428 @ 2026-07-27,
`:34`) and the file explicitly warns at `:41` that this number "is not the census's N_silent (176)",
so the replacement the Done-when demands has not happened.
**CLASS: LIVE.**

**[#358] `parity-surfaces.yaml` misdescribes its own enforcement posture** — ASK: each of the three
sites states the post-`[#337]` blocking posture, or `STANDING_RULINGS.md` records why the divergence
stands.
TARGET: **the contradiction is live and two of the row's three locators have drifted — a repaired
locator is given here.** `ecosystem/parity-surfaces.yaml:6` still reads "read-only, WARN-only v1"; the
site the row cites as `:93-94` now sits at **`:99-100`** ("WARN-only v1: severity labels are REPORT
labels; the checker never blocks and never mutates"); and `scripts/fleet_parity.py:131` is now
**`:142`** ("never blocks in v1"). Against them, `scripts/audit.py:4229` and `:4304` both state
fleet_parity "is now a blocking ALL_CHECKS member ([#337])". `grep '358' protocols/STANDING_RULINGS.md`
= zero.
**CLASS: LIVE** (dead locators, live mechanism — the `[#534]` class).

**[#359] PHANTOM ENFORCEMENT — §14a FILE-BOUNDARY claims a mechanism that does not exist** — ASK: the
false claim corrected or the mechanism built, AND the ledger model given an explicit disposition for
the phantom-enforcement class.
TARGET: **confirmed verbatim at the re-pegged locator.** `protocols/HANDOFF_PROCESS.md:775-776` reads
"**FILE-BOUNDARY** — … This is the parallelism ruling made mechanical — two concurrent epics MUST have
disjoint boundaries", and the only candidate mechanism disclaims itself:
`scripts/boundary_report.py:8-9` — "reporter, NOT a gate … deliberately NOT registered in
`audit.ALL_CHECKS`, so it never reddens the ship-gate". The second conjunct (a ledger cell for the
class) is untouched. P1, zero merge mentions in 1,189 merges.
**CLASS: LIVE** — the highest-priority row in this theme and among the very few P1s in the wave.

**[#361] ADR-immutability's real coverage is declared only in code** — ASK: the two protocol surfaces
state the guard's real zone (and that the zone is a live no-op), or the hook widens to ADRs / handoffs
/ audits with a test per newly-covered class.
TARGET: real, and the "live no-op" half is now doubly true.
`templates/claude-regions/critical-rules-records.md:3` still asserts all four classes immutable, and
`protocols/AI_COUNCIL_PROCESS.md:344` (the row cites `:350` — drifted) still says "ADRs are
immutable". `scripts/hooks/block_immutable_edits.py` scopes itself by
`_ZONE_SEGMENT = "/docs/decisions/transcripts/"`, and `ls docs/decisions/transcripts` returns **no such
file** — the guard's only zone does not exist, so it is armed over nothing while two protocols promise
four-class coverage.
**CLASS: LIVE.**

**[#365] Promote `residual_completeness` from `exempt:` to `coverage_scope`** — ASK: doc marker + both
`# rule:` code markers + `multi_site: 2` in ONE commit, edge resolves, row moves to `coverage_scope:`,
ship-gate holds.
TARGET: real, unbuilt, and **self-documented in the file it must change**.
`ecosystem/doc-code-edge.yaml:161` still lists `- residual_completeness` under the exempt block, and
the preceding comment (`:150-160`) records the whole state: the doc-side rule "is now DONE", it stays
exempt because the edge needs both halves, adding the doc marker alone was witnessed to produce
`broken_edge (doc sites=1, code sites=0)`, and — literally — "**[#365] adds both markers in one
commit**".
**CLASS: LIVE.**

**[#369] Wire `boundary_headers.py --check` into pre-commit** — ASK: the hook registered and blocking a
hand-edited header, listed in `CLAUDE.md` §9, with `ecosystem/doc-counts.md` agreeing with the live
hook roster.
TARGET: real and unwired — `grep 'boundary_headers|boundary-headers' .pre-commit-config.yaml CLAUDE.md
ecosystem/doc-counts.md` returns **zero hits in all three**. The row's 2026-08-12 re-scope (register
`N2-R1-05`) is worth preserving as a pattern: it moved the Done-when off an absolute gate count onto
agreement-with-the-regen, precisely because an absolute number "re-breaks every time a hook lands" —
and this wave contains several rows that still carry absolute counts (`[#420]`'s 9, `[#263]`'s ×2).
**CLASS: LIVE.**

**[#371] Consumer editor-config write-through** — ASK: an ADR names the carrier vehicle, both consumers
carry the editor config under it, and `deploy/manifest-v1.4.0.yaml`'s `implemented:` matches the live
per-consumer state with `fleet_parity` green.
TARGET: real and unchanged — `deploy/manifest-v1.4.0.yaml:327` still reads `implemented: false` for
`- id: editor-config` (`:325`), with the manifest comment at `:319` stating "the hub half is built,
the consumer write-through is the next ticket". The row's first conjunct is a *decision* it explicitly
defers to another artifact ("Vehicle decided by the buy-vs-build fleet-template ADR (intake pending) —
do NOT implement bespoke"), so build work here would be premature by the row's own instruction.
**CLASS: AWAITING-RULING** — decision: the carrier vehicle, per the pending buy-vs-build fleet-template
ADR (the row forbids a bespoke implementation until it lands).

**[#399] `templates/handoff/v5/README.md.tmpl` — phantom source claim** — ASK: the source claim matches
what `scripts/seed_runbook.py` actually does (corrected, built, or recorded in a `STANDING_RULINGS.md`
section naming `[#399]`), and the template's first line states whether it is live or superseded.
TARGET: **one conjunct is already satisfied and this is the wave's clearest partial in E8.** The
template's first line reads `<!-- HANDOFF v5 — runbook source template (DEFERRED STUB).` — it *does*
state its own status. The claim conjunct is not met: `protocols/HANDOFF_PROCESS.md:723` (the row cites
`:481` — drifted) still says `docs/handoffs/README.md` is rendered "idempotently from one source
(`templates/handoff/v5/README.md.tmpl` …)", while `scripts/seed_runbook.py:85` generalizes from
`source_readme` — defaulted at `:106` to "the hub's docs/handoffs/README.md", **the rendered file, not
the template** — and a grep of `scripts/` for `README.md.tmpl` is null. `grep '399'
protocols/STANDING_RULINGS.md` = zero.
**CLASS: LIVE** (residue = the `:723` claim only).

**[#413] Colors semantics — global/hub-managed vs per-repo in governed markdown** — ASK: **on or after
2026-10-22**, either the colors semantics cite the ruled ownership model in
`deploy/manifest-v1.4.0.yaml` (referencing `[#400]`'s ruling), or ai-council's declaration carries a
new `review_date:` later than 2026-10-22.
TARGET: **this row is not yet evaluable, and that is the finding.** Its Done-when is explicitly
date-gated to 2026-10-22; today is 2026-08-19, so **neither limb can be assessed for 64 more days** by
the row's own construction. The supporting state is consistent with the row's text: `[#400]` is
`status: open`, and `grep 'review_date' deploy/manifest-v1.4.0.yaml` returns zero. The row already
declares itself "partially unblocked, NOT satisfied, NOT closure-eligible".
**CLASS: LIVE** — flagged as **date-gated (2026-10-22)**: no lane should be spent on it before then,
and no grooming pass should re-derive its status until the date passes.

**[#427] Region templates carry a repo-POSITION-DEPENDENT path** — ASK: the carry mechanism supports a
per-consumer substitution (or explicit per-position variants), and ai-council's
`claude-md-token-log-address` divergence retires by reference.
TARGET: real, verified at both cited lines.
`templates/claude-regions/critical-rules-records.md:1` and
`templates/claude-regions/antipatterns-universal.md:2` both name the token log as bare
`logs/TOKEN-LOG.md` — correct at the hub, wrong at every consumer. The row's analysis holds: because
the regions are carried **byte-verbatim**, no single string is true in both positions, so this is a
substitution problem and rewriting to the `.dev-knowledge/` form would only invert the error. The
divergence-retirement half is off-tree and unverifiable from here.
**CLASS: LIVE.**

**[E8] rollup — 10 rows: 9 LIVE · 1 AWAITING-RULING · 0 DEAD-CANDIDATE · 0 MALFORMED.** Theme
COMPLETE. **`[#359]` is the theme's and arguably the wave's most serious row** — a P1 phantom-
enforcement claim, reproduced verbatim tonight at `HANDOFF_PROCESS.md:775-776` against a reporter that
disclaims gate status in its own docstring, with zero merge activity in 1,189 merges. Three rows carry
**drifted locators with live mechanisms** (`[#358]` `:93-94`→`:99-100` and `:131`→`:142`, `[#361]`
`:350`→`:344`, `[#399]` `:481`→`:723`) — the `[#534]` class, and the repaired locators are given inline
above so the next executor does not re-derive them. `[#413]` is **date-gated to 2026-10-22** and should
be excluded from grooming until then.
---

## [E9] Fleet Desired-State System (North Star) — 3 rows

**[#383] Execution waves per surface** — ASK: for every `kind: gitignore-effect` row in
`ecosystem/parity-surfaces.yaml`, (a) `desired_state_report.py` shows no `diverge` cell, (b)
`fleet_parity.py --run-date <d>` reports 0 warn-undeclared / 0 must-absent / 0 tombstone-violated,
naming any unwalkable repo, and (c) both runs are pasted verbatim into the wave record and the
operator has read them.
TARGET: **the closest row in this wave to its own Done-when, and it still misses on two measurable
counts.** `docs/audits/2026-08-03-technical-383-caches-wave-record.md:125` carries an in-file
amendment marker and `:131` records **EXECUTED 2026-08-04**, with clause (a) verbatim at §5.1
("no `diverge` cell on any of the 8 rows") and clause (b) verbatim at §5.2 ("0 warn-undeclared, 0
must-absent, 0 tombstone-violated"). **But the evidence is over 8 rows and the selector now resolves
9:** `grep -c 'kind: gitignore-effect' ecosystem/parity-surfaces.yaml` = **9**, and the ninth,
`ai-env-ignored` (`:977`), appears in neither pasted run. Clause (c) is half-open by the row's own
text — "(c) operator read PENDING" — and the record's own §5.3 caveat is that the clause is met "over
3 of the fleet's 9 declared repos".
**CLASS: LIVE** — but the honest note is that it is one re-run over the 9th row plus one operator
read away from its Done-when, which makes it the wave's best closure prospect rather than a
DEAD-CANDIDATE.

**[#385] L4 tech-currency lane** — ASK: one version-bump proposal written into the desired-state
contract, ruled, and distributed through the apply channel, with the resulting version visible in
`ecosystem/deployed-versions.yaml` and the proposal never mutating the contract directly.
TARGET: real and gated. `ecosystem/deployed-versions.yaml` exists (the observable the Done-when
names), but no apply channel does: `grep -rn 'apply channel' scripts/*.py ecosystem/*.yaml` returns
**zero**. The row carries `depends-on: "383"` in its own frontmatter and `[#383]` is still open, so
the dependency is real and unsatisfied — this is a *blocked* row, not a stale one. Landed since
2026-08-15: `4ca67eed8` (2026-08-16) is a Done-when conversion merge, not build work.
**CLASS: LIVE** (blocked-on-`[#383]`, by its own declared `depends-on`).

**[#391] Wire `fleet_analytics` into a nightly lane, or narrow #384 to a manual reporter** — ASK:
`scripts/fleet_analytics.py` fires on a schedule under a `· routine:` block that `routine_consumers`
passes, fail-soft — or #384 is narrowed to a manual reporter.
TARGET: real and unwired. `scripts/fleet_analytics.py` exists (`:2` docstring, `:116` `_CHECK`), and
the ADR-105 machinery it must register with is live — `scripts/audit_checks/check_routine_consumers.py`
gates rows carrying a `· routine:` marker (`:89`). But **no `· routine:` marker names
`fleet_analytics` anywhere**: a repo-wide grep for `fleet_analytics` outside `docs/audits/`, `tasks/`
and `BACKLOG.md` resolves to the script itself, `scripts/audit.py:194` (a codemap comment) and
`JOURNAL.md` prose only. The script's own `:960` fallback string — "no report yet -- run
scripts/fleet_analytics.py" — is itself evidence that invocation is manual.
**CLASS: LIVE.**

**[E9] rollup — 3 rows: 3 LIVE · 0 AWAITING-RULING · 0 DEAD-CANDIDATE · 0 MALFORMED.** Theme
COMPLETE. **`[#383]` is this wave's single best closure prospect** and the finding that pays for the
theme: two of its three clauses have verbatim executed evidence in the wave record, and what stands
between it and its own Done-when is a re-run covering `ai-env-ignored` (the 9th selector row, added
after the 8-row runs) plus the operator read the row itself marks PENDING. `[#385]` cannot move until
`[#383]` does — its `depends-on` is declared in frontmatter, not just prose. `[#391]`'s cheap branch
is the ruling (narrow #384's claim), not the build.
---

## §10 · Dead and drifted locators — measured, with repairs

Seven wave-2 rows pin a `file:line` that no longer resolves. Each was classed on its **mechanism**,
which is alive in every case; the repaired locator is given here so the next executor does not
re-derive it. This is `[#534]`'s subject, measured on a population it does not cover.

```
row     row's locator            live location            construct
#146    PLAYBOOK.md:1016-1024    PLAYBOOK.md:1109         the de-hardcode-first doctrine paragraph
#357    audit.py:363             audit.py:491             def discover_repos
#358    parity-surfaces.yaml     parity-surfaces.yaml     "the checker never blocks and never mutates"
          :93-94                   :99-100
#358    fleet_parity.py:131      fleet_parity.py:142      "never blocks in v1"
#361    AI_COUNCIL_PROCESS:350   AI_COUNCIL_PROCESS:344   "ADRs are immutable"
#399    HANDOFF_PROCESS:481      HANDOFF_PROCESS:723      "idempotently from one source (…tmpl)"
#417    audit.py:4751-4760       audit.py:3844 / :3853    history_specs / pathspecs  (row's pin is past EOF)
#477    audit.py:2300            audit.py:1863            repo_key = _git_repo_root_name(...)
```

**`[#534]`'s own repairs have already drifted.** The row was filed 2026-08-17 with corrected line
numbers; re-measured tonight at `HEAD = 4541155`:

```
                     [#534] says      live 2026-08-19    delta
audit.py length      4271 lines       4341 lines         +70
repo_key             :1862            :1863              +1
discover_repos       :490             :491               +1
history_specs        :3779-3788       :3844 / :3853      +65
```

Two days, four drifts. This is direct evidence for `[#534]`'s **second** conjunct — a check over
`scripts/*.py:<line>` locators in `tasks/` — rather than for its first: repairing line numbers by hand
produces a locator that is stale before it is read.

**Seven further rows carry a stale count or premise in their own body** (not a locator, so they are
listed separately — none changes the ask):

```
#227   "no living doc references it"        →  protocols/README.md:18 does
#263   "PLAYBOOK 'English-only' refs ×2"    →  live grep -c = 1
#420   "9 files under docs/archive/"        →  live ls | wc -l = 22
#424   "6 clauses / 4 parse / 2 inert"      →  live 4 clauses / 2 parse / 2 inert  (third distinct census)
#493   "silent 10+ days"                    →  19 days (streams end 2026-07-31)
#511   "15 FILL-IN regions"                 →  39 across templates/handoff/
#428   "Leg 2 is PARTIAL"                   →  15 Issues closed 2026-08-16 at `7257f4fe`
```

## §11 · The TOP-15 DEAD-CANDIDATE table, with honest population

**The evidence supports one entry.** The contract asked for a TOP-15 table; manufacturing fourteen
more would be the "language stronger than the four classes" it forbids. N4 reached the same honest
population (n=1) from the opposite half of the open set, so across the whole 179 rows the two waves
evaluated, **two** rows read done-on-their-face.

```
rank  row     why it reads satisfied                                          evidence
1     #388    both Done-when conjuncts hold on a live scan: no living surface  repo-wide grep for 10–20;
              restates "10–20 repo", and the immutable four are unedited       ADR-104:113; the four files
                                                                              last touched 2026-07-21
--    --      NO SECOND ENTRY. 115 further rows examined; none reads done.     see §11b for the partials
```

Ranks 2–15 are **deliberately empty**. The substitute the architect can actually spend is below.

## §11b · The twenty-three partially-discharged rows — ranked by how much is left

This is wave 2's real product. Each of these has at least one Done-when conjunct verifiably landed and
at least one owed; **in nearly every case the owed half is the load-bearing one**, so none is a closure
candidate — but dispatching a lane without reading the partial risks re-doing landed work.

**Group A — one small, named conjunct left (7):**
```
#269   count-tiered index shape        header repoint to ADR-100 already DONE
#399   the HANDOFF_PROCESS:723 claim   template's own first line already says "DEFERRED STUB"
#417   extract the scope list          the _is_lane_owned_daily filter already landed 2026-08-16
#428   dead-producer staleness guard   15 Issues already closed 2026-08-16 (`7257f4fe`)
#146   the version-surface sweep       de-hardcode-first doctrine already at PLAYBOOK:1109
#123   wiring + value review           the `Routine: <name>` convention already at PLAYBOOK:2409
#415   the ~10-test enumeration        the triggering test already re-pointed to a fixture
```

**Group B — a landed half plus a genuinely large remainder (9):**
```
#383   clauses (a)+(b) EXECUTED 2026-08-04 over 8 rows; selector now resolves 9 (ai-env-ignored) + (c) operator read
#447   leg 2's recursion answered by ADR-85 §A5 range-level discharge; leg 1 (ratchet raise) untouched
#528   legs 1+2 merged `7d1f6ce0`; leg 3 (test_run telemetry) owed, sequenced after the excluded [#529]
#510   W1 narrowed the grammar via one imported LANE_BRANCH_RE; all four ROSTER legs stand
#430   (a) landed — parity-surfaces.yaml:292-310 carries the ruling and declared_by; (b) determinism test absent
#414   (b) covered by block_unanchored_push + the backstop; (a) operator-GO gate has no organ, choice unrecorded
#244   P1–P4 shipped 2026-07-04; P5 hub self-prune and P6 fleet both UNOWNED by the row's own text
#245   the last-deployed oracle exists at carrier_precommit.py:707-759; the add-path is still blind
#365   the doc-side rule is DONE and the file says so; the two code markers + multi_site owed
```

**Group C — landed on a surface this lane can see, remainder off-tree (4):**
```
#327   hub genre wording landed (protocols/README.md:5); corp branch `docs/327-interface-genre-markers` unmerged
#332   ARC-A corp bootstrap done; Done-when clause 1 (ships-with-package) unbuilt
#241   PLAYBOOK (4) + SESSION_SETUP (1) declared; VISION and ESSENTIALS carry 0 and are freshness-gated
#390   ADR-87's 2026-08-08 amendment answers the ADR half; templates/prompt-template.md:68 still 4-rung
```

**Group D — evidence conjunct met, adjudication conjunct outstanding (3):**
```
#506   one-row-per-open-task coverage now stands at 179 of 183 across the P10 sheet + N4 + this file;
       the per-id VERDICT is the architect's and cannot be supplied by a lane
#523   --check and --roundtrip already hold in gen_task_tree.py; the index and --status modes are owed
#552   the routine block is fully declared (review_date 2026-11-17); neither leg is built
```

## §11c · The ten AWAITING-RULING rows, ranked by how self-contained the decision is

```
rank  row     the decision, stated                                                          self-contained?
1     #549    intake #13 superseded-in-part by [E9]/ADR-109, or re-anchored to a date       yes — ADR-109 exists
2     #507    land the wall's 4th leg, or an accepted-with-reason hold naming the gap       yes — L-5 carve-out
3     #420    docs/archive/ kept-with-restated-charter or dissolved (22 files, not 9)       yes — L-5 carve-out
4     #331    per consumer: adopt the hub story-map at P6 vs accept-durable divergence      yes — [#281] closed today
5     #541    which scale-out substrate to rent, or a dated deferral                        yes — v2 report priced
6     #491    R-G: admit the Gemini CLI as a retrieval-only scanning lane                   yes — one section
7     #43     whether to author a new-repo scaffold at all                                  needs intake #6 off SEED
8     #371    the carrier vehicle for consumer editor-config write-through                  no — pending buy-vs-build ADR
9     #389    R6: hard-probe vs soft-check for off-repo prompts                             no — [E8] W6, also gates other work
10    #293    the correct consumer-side home for the seeded runbook under ADR-60            no — [#303] must land first
```

Ranks 1–6 are each one recorded ruling with its evidence already committed. Ranks 7–10 have a
prerequisite in front of the decision and should not be put to the architect as if they were free.

## §12 · MALFORMED count: 0 — and why

**No row in the 116 is MALFORMED.** The bar applied is the contract's: a row is malformed if its ASK
cannot be read out of its body, or its Done-when cannot in principle be evaluated. Candidates
considered and rejected:

- **`[#239]` is titled just "Follow-up"** and `[#43]` just "Decide +". Both bodies carry a complete ask
  and an evaluable Done-when; a thin *title* is not a malformed *row*.
- **`[#413]` is date-gated to 2026-10-22** and therefore cannot be evaluated today. That is a
  deliberate, stated construction, not a defect — it is flagged in E8 so no grooming pass wastes a
  verdict on it before the date.
- **Rows whose own counts are stale** (§10, second table) still state an evaluable ask; the stale
  figure changes the *size* of the work, not its readability.
- **Rows whose Done-when depends on an off-tree repo** (`[#327]` `[#334]` `[#401]` `[#427]` `[#509]`)
  are evaluable in principle — this lane simply cannot see the evidence, which is recorded as a limit
  in §13, not scored as a defect in the row.

## §13 · Honest limits of this sheet

1. **The container's clone arrived SHALLOW and was repaired mid-lane.** `.git/shallow` was present,
   `git rev-list --count main` returned **299** against a true **5,328**, and only **65** first-parent
   merges were visible against **1,189** after `git fetch --unshallow origin main` (read-only). **Every
   merge-mention figure in this file is post-repair.** Had it not been repaired, 73 wave-2 rows would
   have been reported as having zero merge mentions instead of the true 18 — a wrong answer in the
   reassuring direction. This is `[#453]`'s exact defect, hit for at least the third recorded time
   (2026-07-31 night batch, tonight's N5 lane, this lane).
2. **No gate was executed live.** The pinned toolchain is not installed in this container, so every
   verdict rests on source reads, directory listings, `git log` and `grep` — never on a gate run. Where
   a Done-when requires a gate result (`[#463]`'s `audit.py repo win-tooling`, `[#383]`'s two runs),
   that is stated in the row rather than inferred.
3. **Off-tree surfaces are unverifiable from here.** `~/.claude/bin/codex-review.ps1`, win-tooling's
   `Invoke-Dispatch.ps1`, ai-council's `routing.py` and `settings.yaml`, and every consumer repo's
   working tree are absent. Rows depending on them (`[#338]` `[#401]` `[#427]` `[#445]` `[#463]`
   `[#464]` `[#509]`, and the consumer halves of `[#327]` `[#332]` `[#334]` `[#371]`) are classed on
   what the hub can see, with the gap named in the row.
4. **Gitignored state is invisible.** `logs/PROPOSALS-*.md` (`.gitignore:26`) and `logs/FLEET-HEALTH.md`
   (`:30`) do not exist in a clone, so `[#487]`'s "149 parked" and `[#418]`'s throttle behaviour could
   not be re-derived — only their mechanisms could.
5. **The live-worktree exclusion could not be applied** (§2). A cloud container sees only `main`.
6. **`status: open` is this sheet's predicate**, matching P10 and N4. Deferred rows (24) are out of
   scope by that choice, not by judgment.

## §14 · Provenance

```
HEAD at derivation      4541155  (main, 2026-08-19)
clone repaired          git fetch --unshallow origin main  -> 5328 commits, 1500 first-parent
first-parent merges     1189 scanned for [#id] mentions
strong-closure scan     propose_closures.CLOSES_RE over all first-parent commits -> 0 hits on any wave-2 id
row bodies read         116 of 116, in full, from tasks/<id>-*.md
theme grouping          each row's own frontmatter `theme:` field
predecessor sheets      docs/audits/2026-08-18-census-p10-grooming-evidence.md  (mechanical, 194 rows)
                        docs/audits/2026-08-19-technical-n4-grooming-wave1.md   (72 git-silent rows)
```

**Coverage across the two waves:** N4's 72 + this file's 116 = **179 rows evaluated**; the live open set
is **183**; the residue is the four excluded in-flight rows `[#529] [#530] [#533] [#554]`. That is the
whole open set, and it is the evidence half of `[#506]`'s Done-when.
