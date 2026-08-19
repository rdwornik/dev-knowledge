<!-- scope: meta -->
# N4 grooming wave 1 — the 72 git-silent rows, one evidence sheet each · 2026-08-19

**Produced by:** CC, night-N4 research lane, branch `claude/n4-grooming-wave1-audit-ahltfa`,
under the frozen contract `docs/audits/2026-08-19-technical-n4-grooming-wave1-contract.md`
(committed first, contract-of-record).
**Posture:** READ-ONLY. **No closures, no status edits, no BACKLOG/`tasks/` writes, no merge.**
Every line below is *evidence* plus a RECOMMENDED CLASS. The live/dead/awaiting-ruling **verdict is
the architect's**; nothing here proposes a closure as settled.

## §0 · The answer first

```
rows evaluated                72   (every `**git silent**` row of the merged P10 sheet)
themes covered                9 of 9   — E1 E2 E3 E4 E5 E6 E7 E8 E9, ALL COMPLETE
  LIVE                        57   (79.2%)  ask stands, target verified real
  AWAITING-RULING             14   (19.4%)  one architect decision is the whole remaining work
  DEAD-CANDIDATE               1   ( 1.4%)  [#348] — done-when reads satisfied on its face
  MALFORMED                    0   ( 0.0%)  none; see §12 for why, incl. the row named "Design question"
```

**The headline is the 57.** Git silence predicted almost nothing: of 72 rows the P10 sheet could
not measure, **71 still name a target that exists and an ask that is unmet**, and **37 of the 72
carry a precise `file:line` locator** in their evidence, most of them pinning a defect that
reproduces on a source read. Several rows are
*self-documented in the code they indict* — `check_fleet_parity`'s own docstring says the fix is a
filed follow-up (`scripts/audit.py:1810-1812`), and `_ORGAN_TO_COMPONENT` carries an eight-line
HONEST LIMIT comment saying the mismatch is "deliberately NOT fixed here"
(`scripts/enforcement_coverage.py:887-895`). Git silence is a fact about **how rows are written**
— prose, globs, `~/.claude` paths, not-yet-existing files — exactly as P10 §2 warned.

**Do not expect a closure harvest from this wave.** The contract asked for a TOP-15
DEAD-CANDIDATE table; the evidence supports **one** entry, and manufacturing fourteen more would
be the "verdict language stronger than the four classes" the contract forbids. §11 gives the
honest table (n=1) and then the substitute the architect can actually spend: the 14
AWAITING-RULING rows, ranked by how self-contained each decision is.

## §1 · Reading rules this sheet enforces

**TWO DIFFERENT 72s. Do not conflate them.** This sheet's 72 = the P10 sheet's **git-silent** rows
(`n == 0` resolved paths). `protocols/STANDING_RULINGS.md:1319` names a *different* 72 — the
**PROSE-CONVERTIBLE** rows the W4 conversion campaign converts, from
`docs/audits/2026-08-10-technical-backlog-testability-census.md:74`. The two sets are drawn on
different axes over different denominators (194 open rows vs 170 censused) and are **not** the same
rows. The numerical collision is a coincidence and is the single likeliest misreading of this file.

**A DEAD LOCATOR IS NOT A DEAD ROW.** Six rows cite a `file:line` that no longer resolves while the
mechanism they indict is alive at a new line. Each is classed on the *mechanism*, with the repaired
locator quoted. §10 collects them — that is [#534]'s subject, measured on a fresh population.

**"AWAITING-RULING" here includes rows that ARE the decision request.** The contract defines the
class as "depends on an open decision — name it". A question-shaped row whose own Done-when reads
*"a ruling records either X or Y"* depends on a decision that has not been taken — its own. Twelve
of the 14 are already recorded as such: `protocols/STANDING_RULINGS.md` **L-5** names a
**15-row PROSE-JUDGMENT carve-out class** — `[#43]` `[#122]` `[#126]` `[#153]` `[#281]` `[#323]`
`[#397]` `[#400]` `[#406]` `[#407]` `[#420]` `[#449]` `[#450]` `[#488]` `[#507]` — "verified at
close by the architect against the row's own named criterion". Twelve of those fifteen are in tonight's
72, and are marked **(L-5)** below. They are sanctioned judgment rows, **not** hygiene defects.

**Evidence is source-read + git only.** See §13 — the pinned toolchain does not run in this
container, so no gate was executed live.

---

## [E1] Handoff continuity — 5 rows

**[#298] Handoff-generator polish** — ASK: three generator enhancements — EPIC_BOOT auto-pulls a
BACKLOG slice as an AUTO-PULLED draft, a non-live `--epic-slug` leading id WARNs, `--epic-slug` in
an ignoring mode WARNs.
TARGET: real and all three legs unbuilt. `--epic-slug` is defined at `scripts/gen_handoff.py:840`
and consumed at `:780`, `:863`; `templates/handoff/epic/EPIC_BOOT.md.tmpl` exists. `grep -rn
'AUTO-PULLED' scripts/ templates/` returns **zero hits**, and no id-liveness or mode-mismatch WARN
exists on the option.
**CLASS: LIVE.**

**[#344] Session-close gate + consumer hub-write guard** — ASK: two mechanisms — a pre-handoff gate
refusing bundle regeneration until (a) a session-audit artifact exists, (b) doc-currency legs are
green, (c) an operator close-readiness token is recorded; plus a consumer-side PreToolUse guard
blocking writes under `.dev-knowledge/` / `~/.claude/`.
TARGET: the row is marked NEEDS-RULING in its own text and no `protocols/STANDING_RULINGS.md`
section names `[#344]` (grep: zero). **Ask 1(c) is overtaken:** it specifies an "`/override`-shaped,
HEAD-bound" token, and the ADR-85 amendment 2026-08-03 §A2 **RETIRED that local-token path**
(`CLAUDE.md` §7 records `/override` "discharges no gate"). Ask 2 is wholly unbuilt.
**CLASS: AWAITING-RULING** — the open decision is Ask 1(c)'s replacement now that its named
mechanism is retired; Asks 1(a)/1(b)/2 stay buildable underneath it.

**[#404] gen_handoff execution-mode SUPPLEMENT leak** — ASK: make framing tokens mode-aware and P8
mode-conditional, so an execution render carries no SUPPLEMENT reference.
TARGET: defect intact and reproducible. `_tokens()` at `scripts/gen_handoff.py:630` sets
`"SUPPLEMENT_BANNER": _framing("SUPPLEMENT_BANNER", filled)` and `"P1_GATE_NOTE": _framing(...,
filled)` at `:647-648` — keyed on **fill-state only**, `mode` unused for either.
`templates/handoff/v5/PROBES.md.tmpl:99` P8 unconditionally binds `SUPPLEMENT.md`. The v5 template
dir is still the live one (no `templates/handoff/v6/`), so the target did not move under the v6
process flip.
**CLASS: LIVE.**

**[#422] `reflow_framing`'s partial flip has no detector** — ASK: add a post-fold check that FAILs
on cold-state framing prose surviving a FILLED flip — explicitly *not* a wider replace.
TARGET: mechanism alive, **both locators dead**. Row cites `scripts/gen_handoff.py:270-293`; the
function is now at **`:578`**. Row cites `scripts/assemble_paste.py:97-105`; the call is now at
**`:135-136`**. No post-fold cross-claim check exists anywhere.
**CLASS: LIVE** (locator repair owed — see §10).

**[#449] Assembled-paste byte budget** — ASK: rule whether `PASTE_THIS.md` gains a hard ceiling, or
record an accepted-with-reason hold citing the supplement fold as the elasticity argument.
TARGET: state unchanged since filing. `scripts/assemble_paste.py:32` still reads
`_SIZE_WARN_BYTES = 65_000`, and `:214-215` still `click.echo`es a `[warn]` and never blocks.
Question-shaped by its own text; **L-5 carve-out member**.
**CLASS: AWAITING-RULING** (the budget ruling itself).

**Rollup [E1]:** LIVE 3 · AWAITING-RULING 2 · DEAD-CANDIDATE 0 · MALFORMED 0.
All five targets verified present; the theme's whole `serialize-group: handoff` chain is intact.
Two locator repairs owed inside `[#422]` — the only maintenance debt this theme carries.

---

## [E2] Enforced governance — 28 rows

**[#99] FLEET-HEALTH digest names the failing check** — ASK: a red repo's digest line carries the
failing check name(s), not just a count.
TARGET: `scripts/fleet_health.py:327` returns `(name, n_pass, n_fail, n_warn)` — **counts only**;
nothing in the digest render carries a check name. Defect intact.
**CLASS: LIVE.**

**[#112] `adr_amend` helper + ADR immutable-zone extension** — ASK: make a helper the only
sanctioned writer of an ADR status/Amendment line, deny every other in-place ADR edit, and
de-contradict `CLAUDE.md` §5.
TARGET: **`scripts/hooks/adr_amend.py` does not exist.** The row carries `depends-on: "#23"` and
`[#23]` is `status: open`, so it is blocked, not stalled.
**CLASS: LIVE.**

**[#116] Hooks hygiene** — ASK: migrate PowerShell hooks to exec-form `args:[]` and give ≥1
PreToolUse guard an `if:` scope filter.
TARGET: `~/.claude/settings.json` — **off-repo and outside this container**; unverifiable here (§13).
Nothing in-tree supersedes it and no ruling retires it.
**CLASS: LIVE** (target unverifiable from the hub tree — flagged, not assumed).

**[#117] Evaluate prompt/agent-based hooks** — ASK: run the VF-1 auth probe, then record a go/no-go
on a `type:"prompt"` Tier-1 eval.
TARGET: no VF-1 result and no go/no-go recorded anywhere in-tree. Un-deferred 2026-08-11 on a met
peg (`[#270]` closed at `679d8eca`), so it is deliberately live rather than dormant.
**CLASS: LIVE.**

**[#153] Enforcement-completeness pass** — ASK: mechanize-or-accept each remaining prose-only
constraint, **define core-invariant #5's `--no-ff` scope boundary**, and decide the
`~/.claude`-reach question.
TARGET: the two named decisions are unmade — no scope-boundary definition exists in-tree and
`[#189]` still cites `[#153]` as its decider. **L-5 carve-out member.**
**CLASS: AWAITING-RULING** (the `--no-ff` scope boundary + the methodology-reach question).

**[#170] Traceability-spine ADR** — ASK: an ADR defining the issue-ID↔commit linkage, plus the
absorbed `#168` half promoting ADR-85's BACKLOG leg to a hard gate.
TARGET: no such ADR exists. The census called this row DEFECTIVE for a dead `#168` referent — **that
finding is now stale**: the row was RE-PHRASED 2026-08-12 (register M-7 / `N2-R1-01`) to state the
absorbed half in-row. `tasks/168-*.md` is still absent, but only as a `refs` pointer, not a
dependency.
**CLASS: LIVE.**

**[#171] Conformance dashboard** — ASK: `ecosystem/conformance.md` generated + committed by a
read-only validator, with an ARCHITECTURE Ch2 pointer.
TARGET: **`ecosystem/conformance.md` does not exist.** Un-deferred 2026-08-09 on a met peg; it
un-blocks the `[#169]`/`[#322]` chain.
**CLASS: LIVE.**

**[#185] GAP-2 gotcha-injection guard** — ASK: a read-only PreToolUse guard injecting the matching
gotcha on a seeded commit-message / Edit-deletion pattern.
TARGET: no such guard. `.claude/settings.json` registers the ADR-77 `block_immutable_edits.py`
PreToolUse guard and no gotcha hook; `grep -rn 'gotcha' .claude/settings.json` returns zero.
**CLASS: LIVE.**

**[#189] Execute in `~/.claude`** — ASK: a session-end check surfacing uncommitted `~/.claude`
config/safety drift.
TARGET: off-repo by design (queue-only here, `#100` execute-elsewhere precedent) and unverifiable
in this container. Its gating question is `[#153]`'s methodology-reach decision, still unmade.
**CLASS: LIVE** (blocked on `[#153]`).

**[#242] ADR status-flip coherence check** — ASK: an audit leg flagging an ADR whose header status
diverges from its README-index effective status.
TARGET: no such check — neither `scripts/audit.py` nor any of the 16 `check_*.py` modules in
`scripts/audit_checks/` carries a status-flip leg. Also **constrained by `[#362]`**, which forbids `[#242]`
reaching a terminal status first.
**CLASS: LIVE.**

**[#267] Scope-exercising arc extension** — ASK: a consumer measurement showing `hub-toc-hooks` +
`floor-hash-verify-hook` FIRED under a scope-matching edit, with `engages:` carrying the scope
condition.
TARGET: real. `deploy/lived_sandbox/arc.py:150` still defines `ARC_PROMPT`; `engages:` blocks are
live in `deploy/manifest-v1.4.0.yaml:397,416`. The row's own record says half-b is DONE and half-a
(live re-measurement) is deferred — a stated partial, not silence.
**CLASS: LIVE.**

**[#289] Hub-own the OneDrive-Blue-Yonder guard** — ASK: give the fleet-level P0 guard a
hub-canonical versioned source + policy doc, a deploy carrier, and Informant coverage.
TARGET: `~/.claude/hooks/block-onedrive.ps1` is off-repo, but **the hub-side state is checkable and
recorded as NOT-owned**. `deploy/manifest-v1.4.0.yaml:130-133` names `payload: block-onedrive` under
**`l0_scope: → deferred_deployables:`** with `status: 'live, fleet-deployed; candidate for future
L0-payload coverage'` — a deferral record, not a carrier. All three legs stand: no canonical source
in-tree (`find -iname '*onedrive*'` matches only this task file), deployment explicitly deferred,
and no Informant coverage (zero hits in `enforcement_coverage.py` / `deploy/carrier_mesh.py`).
**CLASS: LIVE.**

**[#297] Dry `observe-arc` coverage mode** — ASK: an `observe-arc` dry mode reporting per-organ
armed/fired state with no billed child spawn.
TARGET: intact. `deploy/lived_sandbox/cli.py:114` is `cmd_observe_arc(freeze, model, leg_e)` — no
dry/coverage flag; `:481` still spawns a real arc via `_spawn.spawn(clone, ARC_PROMPT, ...)`.
**CLASS: LIVE.**

**[#303] Make `seed_runbook.py` child-class-aware** — ASK: a `--check`/seed run against an ADR-36
child must skip-or-redirect, never write `docs/handoffs/`.
TARGET: defect intact and stated in the module's own docstring — `scripts/seed_runbook.py:24`:
"writes ONLY `<target>/docs/handoffs/README.md`", with `_RUNBOOK_REL` hard-bound at `:42`. No
handoff-locality class is read anywhere in the file.
**CLASS: LIVE.**

**[#323] Design question: carry `codemap-generate`/`toc-generate` in `hub_hooks`?** — ASK: decide
(explicitly *do not build*) whether the two generate hooks join the carried `hub_hooks` install set.
TARGET: undecided. `deploy/manifest-v1.3.0.yaml` and `deploy/carrier_precommit.py` both exist and
`hub_hooks` still carries freshness-only, per `[#319]`'s correction. **L-5 carve-out member.**
**Not malformed** — see §12; the title is a stub but the body states one closed question.
**CLASS: AWAITING-RULING** (carry-vs-freshness-only, a consumer-behaviour policy call).

**[#324] Phase-6 axis-2 carrier** — ASK: the night-batch becomes a standing routine with an
ADR-105 `· routine:` block that `routine_consumers` passes, a named morning verdict-sheet consumer,
and an audit-corpus verb-list.
TARGET: **the row itself still carries no `· routine:` block** (`BACKLOG.md:138` — 9 rows in the
file do; this is not one). No verdict-sheet consumer is named anywhere.
**CLASS: LIVE.**

**[#346] Persist the two-tier new-path executor rule into `~/.claude`** — ASK: `~/.claude/rules/`
carries the rule with a `verify:` line, **or** `STANDING_RULINGS.md` records why it stays hub-side.
TARGET: the `~/.claude` half is off-repo; **the in-repo escape hatch is checkably unused** — no
`STANDING_RULINGS.md` section names `[#346]` (grep: zero). The behaviour itself is already in force
per the ADR-101 two-tier amendment, so only durability is owed.
**CLASS: LIVE.**

**[#349] Mechanize session-discipline inheritance** — ASK: a boot-injected + Stop-gated mechanism
carrying test-then-close, **or** a recorded fold into `[#344]`.
TARGET: neither. `scripts/session_end_backpressure.py` carries four checks
(`check_journal_sha_anchor`, `check_backlog_marker`, `check_dirty_tree`,
`check_canonical_freshness` — `:299/:339/:412/:427`) and no discipline-inheritance leg; no
`STANDING_RULINGS.md` section names `[#349]`.
**CLASS: LIVE.**

**[#353] Session-boot contract hardening** — ASK: a mechanism refusing a mid-session externally
authored order whose side effects are not worktree-scoped while the tree is dirty.
TARGET: unbuilt, and no `STANDING_RULINGS.md` section names `[#353]`. `[#356]` independently cites
this row as "a backlog ticket, not a decision record" for a rule binding in force today — two
rows agreeing the gap is real.
**CLASS: LIVE.**

**[#405] Session-end leftover check** — ASK: build the already-RULED organ (a) — a hygiene leg in
the `session_end_backpressure` Stop hook flagging each named leftover class.
TARGET: the ruling is recorded (2026-07-25, organ (a) over (b)/(c)); the build is absent — the four
checks at `scripts/session_end_backpressure.py:299/:339/:412/:427` include no worktree, branch, or
orphan-dir leg. `CLAUDE.md` §5 rule 9 remains prose-only here.
**CLASS: LIVE** — ruled, unbuilt; sequenced with or after `[#417]` by its own text.

**[#406] Commit-time `doc_rot` surfacing** — ASK: an architect ruling picks the enforcement point
among (a) nudge / (b) pre-commit leg / (c) accept-as-is.
TARGET: `.pre-commit-config.yaml` contains **no `doc_rot` entry** (grep: zero), so (c) is the de
facto state without having been chosen. **L-5 carve-out member.**
**CLASS: AWAITING-RULING** (the ADR-108 §A re-routed enforcement-point pick).

**[#451] CA layer-edge check** — ASK: port the ai-council layer-edge review as the missing Layer-2
organ, land it read-only, state its honest scope, and have ADR-108's "mechanized check" clause cite
it.
TARGET: **no layer-edge check exists** — `grep -rn 'layer_edge\|layer-edge' scripts/*.py` returns
zero. The ADR-108 §B ruling is settled; only the organ is missing, exactly as the row states.
**CLASS: LIVE.**

**[#457] Two live-repo tests fail on main** — ASK: both named tests pass on main for verified
reasons, with the verification recorded in the fixing commit.
TARGET: both tests are present — `tests/test_audit.py:2268`
(`test_check_fleet_parity_green_on_live_repo`) and `:2434`
(`test_routine_consumers_live_backlog_governs_exactly_one_row`). Their pass/fail state could not be
executed here (§13); the row's own 2026-08-18 note names the two owned REDs as `routine_consumers`
+ the doc_rot accretion arm.
**CLASS: LIVE** (targets confirmed; RED-state unverified in this container).

**[#478] `changelog_sentinel` drops PEP 440 suffixes** — ASK: suffixed versions compare per PEP 440,
with a prerelease-then-GA and `.post` test.
TARGET: defect intact at the exact cited site. `scripts/changelog_sentinel.py:38` is
`_VER_RE = re.compile(r"(\d+(?:\.\d+)+)")`; `parse_version` (`:46-52`) returns
`tuple(int(p) for p in m.group(1).split("."))`, discarding every suffix, and `is_newer` (`:55+`)
does a length-normalised tuple compare. `packaging` is already a declared dep, so the fix adds none.
**CLASS: LIVE** — one of the cleanest build-ready rows in the set.

**[#496] `_ORGAN_TO_COMPONENT` misattributes the pre-push organ** — ASK: map the organ to the
component that carries it, or declare the split, pinned by a test.
TARGET: intact, and **the code says so itself**. `scripts/enforcement_coverage.py:897-899` maps
`"block_unanchored_push": "session-end-backpressure"`, directly under an eight-line comment at
`:887-895`: "an ABSENT verdict about the pre-push organ is attributed to a component that does not
carry it … Behavior is held IDENTICAL here … the mismatch is filed separately." This row is that
filing. (Row cites `:895`; the map begins at `:897` — 2-line drift.)
**CLASS: LIVE.**

**[#514] Two rival `LANE_BRANCH_RE` constants** — ASK: provisioning refuses an off-enum lane name
(leg 1), one clean batch runs under it, exactly one definition remains (leg 3).
TARGET: leg 3 discharged 2026-08-11; **leg 1 confirmed unbuilt** — `KIND_UNKNOWN` appears only in
`scripts/validate_branch_naming.py` (`:96,163,175,187,191,202`) as a *classification*, and in no
provisioning path or `.claude/commands/*.md`. The row's own 2026-08-18 note measured 2 of 8 lanes
off-grammar.
**CLASS: LIVE** (P1 — the highest-priority row in tonight's 72).

**[#518] `audit.py::_git` — two reproduced defects** — ASK: the call site scrubs the environment and
decodes explicitly, with a test reproducing each defect first.
TARGET: **both defects intact at `scripts/audit.py:2104-2109`** —
`subprocess.run(["git", *args], cwd=str(repo_path), capture_output=True, text=True, timeout=15,
check=False)`: no `env=` (defect a — `GIT_DIR` leakage, and lane worktrees export it absolutely) and
no `encoding=`/`errors=` (defect b). Contrast `_git_registered_worktrees` at `:581-583`, which
passes `encoding="utf-8"` — confirming the row's "outlier" claim.
**CLASS: LIVE.**

**[#536] The ARM-2 row-length pile has no owner** — ASK: a ruling records either a drain target with
its number, or the ceiling re-derived for converted rows with its basis.
TARGET: the ceiling is live — `scripts/validate_doc_rot.py:68` `_BACKLOG_ROW_CEILING = 1320`, with
`:87-92` recording the 1200→1320 recalibration as already stale. `ecosystem/disposition-register.yaml`
carries **6** `backlog-row-length` entries against the row's measured 19 loci — 13 undispositioned.
No ruling exists.
**CLASS: AWAITING-RULING** (drain target vs re-derived ceiling).

**Rollup [E2]:** LIVE 24 · AWAITING-RULING 4 (`[#153]` `[#323]` `[#406]` `[#536]`) ·
DEAD-CANDIDATE 0 · MALFORMED 0.
Zero superseded targets across 28 rows — the largest theme is also the most intact. Six rows are
off-repo (`~/.claude`) and unverifiable here; each is flagged rather than assumed
(`[#116]` `[#153]` `[#189]` `[#289]` `[#346]`, plus `[#117]`'s VF-1 probe).
Build-ready today with no decision owed: `[#478]` `[#518]` `[#496]` `[#99]` `[#303]` `[#297]`.

---

## [E3] Lessons feedback loop — 1 row

**[#130] Memory-hygiene review** — ASK: one hygiene pass emits a ratify-only candidates digest with
per-class counts, **and** the gotcha/memory write path gains a dedupe-against-existing step proven
by a test.
TARGET: split across the Layer-2 boundary. `MEMORY.md` and `~/.claude/skills/gotchas` are both
**off-repo** (`find . -name MEMORY.md` → zero in-tree). The in-repo half is checkable and absent:
no `docs/audits/*-technical-*` hygiene digest exists, and the census notes the digest artifact is
unnamed (`…testability-census.md:156`).
**CLASS: LIVE.**

**Rollup [E3]:** LIVE 1 · AWAITING-RULING 0 · DEAD-CANDIDATE 0 · MALFORMED 0.
Single-row theme; the ask stands but half its target sits outside any tree this repo governs.
Naming the digest artifact would make the in-repo half mechanically verdictable at no design cost.

---

## [E4] Decision management — 2 rows

**[#23] Validate ADR frontmatter relation-fields** — ASK: an audit check flags an ADR whose
supersedes/related/amends field names a non-existent ADR-id.
TARGET: **no such check** in `scripts/audit.py` or any of the 16 `check_*.py` modules in
`scripts/audit_checks/`.
One correction the builder needs: **the corpus does not use YAML frontmatter** — 1 of 85 ADRs opens
with `---`; the relation fields are bold-bullet header lines (`**Related:**` on 58 ADRs, `**Amends`
23, `**Supersedes` 8, e.g. `ADR-112:6`). The validator must read that form, not frontmatter.
Blocks `[#112]` (`depends-on: "#23"`).
**CLASS: LIVE.**

**[#450] Per-section intake ratification** — ASK: rule whether the intake schema gains section-level
status, or promotion-to-ADR is the intended terminal path with ADR-108's pattern written up as the
convention.
TARGET: doc-level status confirmed — `scripts/gen_intake_index.py:116` reads one
`fm.get("status","")` per file and groups on it (`docs/intake/README.md:21-50` renders SEED 10 /
DRAFT 9 / READY 1 / ACCEPTED 14). The ADR-108 promotion precedent is live. **L-5 carve-out member.**
**CLASS: AWAITING-RULING** (schema-vs-convention).

**Rollup [E4]:** LIVE 1 · AWAITING-RULING 1 · DEAD-CANDIDATE 0 · MALFORMED 0.
Both targets real; neither superseded. `[#23]` is build-ready once its frontmatter premise is
corrected to the bold-bullet form — a one-line scope repair, not a re-file.
`[#450]` is a pure decision and needs no build to reach a verdict.

---

## [E5] Canonical-file integrity — 1 row

**[#71] Reconcile ENVIRONMENT.md's `~/.claude/` tree** — ASK: the ENVIRONMENT `~/.claude/` tree
matches live `ls ~/.claude/{commands,skills}`, and the folded-in `#119` half — the "No Codex CLI /
Rejected" lines contradicting the live `/codex-review` command — is reconciled in the same pass.
TARGET: the doc exists (`protocols/ENVIRONMENT.md`); the comparand is `~/.claude`, **off-repo and
outside this container**, so the drift cannot be measured here (§13). Corroborating in-tree
evidence that the `#119` half is real: `protocols/PLAYBOOK.md:4238` documents `/codex-review` as a
live wrapper and `:2673-2674` list it among active commands.
**CLASS: LIVE** (drift unmeasurable from the hub tree — flagged, not assumed).

**Rollup [E5]:** LIVE 1 · AWAITING-RULING 0 · DEAD-CANDIDATE 0 · MALFORMED 0.
The single-row theme is the sheet's clearest case of "git-silent because the target is another
tree" — no path it names could ever resolve against `git ls-files`.
It is verifiable in one command from any operator machine, and nowhere else.

---

## [E6] Cross-repo universalization — 5 rows

**[#82] Per-repository agentic-review profiles** — ASK: every member of the `adr104-fleet-members`
declaration carries a recorded agentic-review profile (which review, what cadence), or is named
there with its reason.
TARGET: the denominator is now countable — `docs/decisions/ADR-104-fleet-repository-shape.md:149ff`
declares **9 repo ids** (mirrored at `ecosystem/index.yaml:186` and `audit.py::ADR104_FLEET_DECLARATION`).
**0 of 9 carry a profile**: no `agentic-review`/`review_profile` key exists anywhere in `ecosystem/`.
Its design inputs have aged well — `/code-review` and `/simplify` are live natives in this session.
**CLASS: LIVE.**

**[#281] Re-peg the ai-council ADR-66 story-map convergence** — ASK: re-peg the convergence to the
Wave-1 onboarding arc, or accept Track-X as durable, recorded.
TARGET: ADR-99 is live and still frames the collision (`ADR-99:14-21`). The row already records the
2026-07-08 pilot as executed and honest-partial. What remains is a decision, not a build.
**L-5 carve-out member.**
**CLASS: AWAITING-RULING** (re-peg vs accept-Track-X).

**[#342] `fleet_parity` gate-ahead max-fidelity hardening** — ASK: three fidelity items — verify the
pinned gate tag exports the required hook ids; refuse an AMBIGUOUS `precommit_remote` match; assert
the tag peels to the recorded commit.
TARGET: item (2) verified intact verbatim — `scripts/fleet_parity.py:694`:
`hit = next((r for r in remotes if token in r["repo"]), None)` — first-wins, silent. `gate_rev_ahead`
is live (`:340-356`, `:717-720`, `:1174`) with no peel assertion, and `precommit_remote` (`:228`,
`:692`) checks only that the stanza lists the ids.
**CLASS: LIVE.**

**[#343] `fleet_parity` ship-gate-only scoping** — ASK: a hub pre-commit stops paying the ~8s
fleet_parity walk while ship-gate still blocks on it, with a test proving both.
TARGET: **the defect is documented in the code it indicts.** `check_fleet_parity`
(`scripts/audit.py:1797`) closes its own docstring at `:1810-1812`: "the walk is ~8s and ALL_CHECKS
also runs on the per-commit audit-health gate; **ship-gate-only scoping is a filed follow-up, not
this arc**." The reusable skip-flag pattern the row names still exists (`:279`, claim-3 skip).
**CLASS: LIVE** — every commit in this repo still pays it, including this lane's.

**[#407] Universal fleet Python style** — ASK: an architect ruling records a functional-vs-OOP
stance AND a uniform naming convention as fleet doctrine, or records deferred-with-reason. Filing
only, zero build, by its own text.
TARGET: unruled. ADR-108 (Accepted 2026-07-31, "Decision-routing doctrine + standing engineering
standards") is the row's re-routed home and does not carry a paradigm or naming clause; the
2026-07-19 parity arc covered lint + test config only. **L-5 carve-out member.**
**CLASS: AWAITING-RULING.**

**Rollup [E6]:** LIVE 3 · AWAITING-RULING 2 (`[#281]` `[#407]`) · DEAD-CANDIDATE 0 · MALFORMED 0.
`[#343]` is the theme's standout: a self-documented performance debt every hub commit pays, with the
reuse pattern already built — the shortest distance from filed to fixed in tonight's 72.
`[#82]` gained a countable 0-of-9 denominator, which is what its census note said it lacked.

---

## [E7] Tooling & evaluation — 21 rows

**[#122] Retire the PATH shim** — ASK: the operator approves and `claude.cmd` is removed, or the
item closes as keep-for-defence-in-depth.
TARGET: off-repo shim, unverifiable here. By its own text operator approval **is** the substance —
"removal needs an explicit operator ask per the no-delete invariant". **L-5 carve-out member.**
**CLASS: AWAITING-RULING** (the operator's remove-vs-keep call).

**[#126] Backpressure-loop pattern evaluation** — ASK: a recorded go/no-go with the doctrine bounds
plus a corp pilot result, or an explicit operator drop.
TARGET: unruled. **Fresh evidence for its "VERIFY FIRST" leg**: `/loop` is live in this session's
skill roster with in-session recurring semantics, so the ADR-74 amendment's persistence-only framing
can now be checked against a running host rather than docs. Pilot executes in corp (ADR-41).
**L-5 carve-out member.**
**CLASS: AWAITING-RULING.**

**[#127] `verify` skill failure-output contract** — ASK: a seeded failure produces a
file/expected/received/directive block plus a semantic exit code; success stays 3-line.
TARGET: defect intact. `.claude/skills/verify/verify.py:52-60` prints `--- Full output ---` and
dumps raw per-check text, then `sys.exit(1)` — no structured fields, no semantic code. Success is
already the 3-line form (`:49-51`), so only the failure half is owed.
**CLASS: LIVE.**

**[#273] Changelog-review staleness escalation** — ASK: an over-threshold unreviewed window renders
an escalation line in the SessionStart digest, with the N/days thresholds recorded.
TARGET: the *pattern* exists but not for this signal — `scripts/fleet_health.py:186`
`groom_escalation_line()` escalates the overdue **quarterly BACKLOG groom** only. No changelog-window
escalation exists in `fleet_health.py` or `changelog_sentinel.py`, and no thresholds are recorded.
**CLASS: LIVE** — the shape to copy is already in the same file.

**[#288] Model-identity guard for unattended runs** — ASK: a read-only detector flags a mid-mission
model swap and the mission ledger names the model in effect.
TARGET: absent — no model-identity detector in `scripts/fleet_health.py` or elsewhere; confirmed
ABSENT by the 2026-07-08 Wave-0 row and unchanged since. `[#271]`'s survival-metric review depends
on like-for-like comparison, so the dependency is live too.
**CLASS: LIVE.**

**[#317] Default-parallel test invocation** — ASK (leg a): point the per-step verify cadence at
parallel and reconcile the `CLAUDE.md` §4 convention text; plus the measured <60s `not slow` run and
the D1 operator ruling.
TARGET: **the primary change has already landed.** `.claude/skills/verify/verify.py:38` runs
`pytest -n auto --dist worksteal --max-worker-restart=0 -x --tb=short` — the row's prescribed
replacement, live. Leg (b) shipped (`slow` marker at `pyproject.toml:124`; row cites `:61`, drifted).
**Residual: `CLAUDE.md` §4 still reads `pytest -x --tb=short`**, the <60s measurement is unrecorded,
and D1 is unruled.
**CLASS: LIVE** — substantially satisfied; re-scope to the residual rather than rebuild.

**[#340] `/ship` pre-flight honors the consumer's canonical test gate** — ASK: `/ship`'s code-diff
validator applies the repo's declared marker filter, bare-suite fallback only when none is declared.
TARGET: defect intact verbatim. `plugins/tier1-lifecycle/commands/ship.md:37` — "**code diff** →
`pytest -n auto --dist worksteal -x --tb=short && ruff check` — the full suite in parallel". No
marker-filter read; the docs-only branch at `:32` proves the command *can* express one (`-m
live_repo`).
**CLASS: LIVE.**

**[#341] Codex producer-lane activation mechanism** — ASK: legs (i)–(iv) each resolved or named with
a reason in a `STANDING_RULINGS.md` section citing `[#341]`, one activation run recorded, and
PLAYBOOK §16 describing the shipped mechanism.
TARGET: no `STANDING_RULINGS.md` section names `[#341]` (grep: zero). PLAYBOOK's Codex-utilization
doctrine (§16, at `:4243+`) describes **lanes and model strings**, not producer activation. Nothing
is superseded.
**CLASS: LIVE.**

**[#347] Formalize the engineering loop/harness + safe-deletion pattern** — ASK: decompose the loop
into filed `tasks/*.md` rows whose ids are listed in the closing commit, and document the
safe-deletion pattern (or record why it stays unruled).
TARGET: neither leg discharged — no `STANDING_RULINGS.md` section names `[#347]`, and PLAYBOOK
carries no safe-deletion pattern. The junkyard effect it names is corroborated by `[#552]`'s finding
that every archival move in repo history was executed by hand.
**CLASS: LIVE.**

**[#348] Backlog grooming as a standing routine** — ASK: capture the grooming cadence as a routine
definition (trigger, scope, consumption path), gated behind `[#270]`'s load-gauge.
TARGET: **both clauses read satisfied.** The row carries a complete ADR-105 `· routine:` block at
`BACKLOG.md:290` — `trigger=on-demand (operator/session boot) · scope=BACKLOG.md rows · consumer=any
session reading BACKLOG.md · consumption_path=BACKLOG.md in place · verified_by=validate_backlog ·
review_date=2026-08-26` — all six fields populated; and the gate `[#270]` is `status: closed`
(`tasks/270-operator-load-gauge.md`).
**COUNTER-EVIDENCE, stated so the architect is not surprised:** the row is the live anchor for the
whole grooming arc — it carries "2026-08-18: owns the full 194-verdict grooming arc (batch-2 lane)"
and **governs this contract**. Closing it orphans that anchor; re-scoping may serve better.
**CLASS: DEAD-CANDIDATE** (done-when satisfied on its face — the sole one in tonight's 72).

**[#397] `scripts/` target structure** — ASK: the operator rules adopt/reject on the mapped
grouping; if adopt, moves land with every caller updated, else flat-is-fine is recorded.
TARGET: unruled, **and the map it would rule on has drifted**: the row's inventory says ~50 files;
live count is **66** `scripts/*.py` at top level plus 4 packages (`codemap`, `hooks`, `toc`, and
`audit_checks` — the last added by `[#533]`, a de facto partial regrouping that landed without this
ruling). **L-5 carve-out member.**
**CLASS: AWAITING-RULING** (and the map needs a refresh before it is ruled on).

**[#403] Extend `doc_claims` to ARCHITECTURE's machine-derivable claims** — ASK: carrier-set AND
child-roster claims gated by `doc_claims` or a regen-and-diff sibling, with tests.
TARGET: unbuilt. `scripts/validate_doc_claims.py:224` `_CLAIMS` holds exactly **four** claims —
`audit_check_count`, `precommit_hook_count`, `precommit_hook_roster`, `pytest_collected` — targeting
only `ecosystem/doc-counts.md` and `CLAUDE.md`. **Zero ARCHITECTURE claims**, no carrier-set
(`make_carriers` lives ungated at `deploy/tool.py:304`), no child-roster.
**CLASS: LIVE.**

**[#419] Routines whose output nobody consumes** — ASK: `routine_consumers` reports zero routines
missing `consumer:`/`consumption_path:`, unconsumed output is reported by a detector, and legs
(i)–(iii) for the nightly conformance routine each land with a test.
TARGET: amended 2026-08-11 (Fork 3 / I-F3) so the absorb step became this row's organ. Nine BACKLOG
rows carry `· routine:` blocks; no queue-depth detector and no scheduler-run distinguisher exist.
Its own `verified_by` test is one of the two owned suite REDs named by `[#457]`.
**CLASS: LIVE.**

**[#431] `codex-review` silently drops the doc lane on mixed diffs** — ASK: a mixed diff gets both
profiles or a loud skipped-prose warning naming the unreviewed files, AND the severity counter
agrees with the body.
TARGET: **locator dead, doctrine alive and unchanged.** The row cites `protocols/PLAYBOOK.md:3439`;
that line is now inside "Council Debate Archival Protocol (**RETIRED** 2026-07-22)". The live site is
**`protocols/PLAYBOOK.md:4240`**, which still reads: "Mixed code+prose diffs filter to the code
subset (code profile)" — the designed defect, verbatim. The wrapper is `~/.claude`-side, so both
fixes remain operator-ruled global infra.
**CLASS: LIVE** (locator repair owed — see §10).

**[#470] `audit.py checks` crashes on a cp1252 console** — ASK: ASCII-swap the U+2192 and add a
regression asserting every `ALL_CHECKS` docstring first line is cp1252-encodable.
TARGET: **defect intact at the exact site.** `scripts/audit.py:1619` is `check_doc_code_edge`'s
docstring first line: `"""#194 doc→code declared-edge integrity (advisory-first, ADR-89 OQ1).` —
still carrying `→`. `cmd_checks` (`:4320`) still echoes each check's first docstring line. No
mitigation in place.
**CLASS: LIVE** — a one-character fix plus a test.

**[#486] `desired_state_report.py` dies on a cp1252 console** — ASK: ASCII-swap the U+21C4 and add a
regression over every console-emitted line.
TARGET: intact, and worse than the module docstring — `scripts/desired_state_report.py:176` is a
**console-emitted string literal**: `"  No observational join is claimed (surface⇄finding joins
await the G9"`. (`:25` carries the same glyph in the docstring.) `[#470]`'s swap does not reach it,
exactly as the row says.
**CLASS: LIVE.**

**[#488] Priority axis** — ASK: the research leg reports measured comparisons against the live
corpus, then the architect rules the axis; any build is a separate row filed after.
TARGET: research unrun, axis unruled. A standing ruling already binds its research contract
(`protocols/STANDING_RULINGS.md:94-96` — "Homed by its own declaration to the `[#488]` row body
(research contract input) … Binding on `[#488]`'s research contract"), so the constraints are
pre-set. **L-5 carve-out member.**
**CLASS: AWAITING-RULING** (with a research leg owed before the ruling can be taken).

**[#494] Ladder ratification (L0–L5)** — ASK: the ladder is ratified or explicitly retired by ADR,
and any surface citing a level as authority resolves to that ADR or drops the citation.
TARGET: **no ladder ADR exists** — no `docs/decisions/ADR-*.md` defines L0–L5 (the grep hits are
handoff-format ADRs, unrelated). Un-deferred 2026-08-15 on a fired peg. Its operative half — "until
ruled, nothing cites L2 as authority" — binds now regardless.
**CLASS: AWAITING-RULING.**

**[#535] `audit.py` has two module identities** — ASK: one spelling reaches `audit` from every
caller, proven by a test asserting `sys.modules` holds exactly one module object.
TARGET: **defect intact at all three cited line numbers.**
`scripts/enforcement_coverage.py:566`, `:695`, `:753` each do `from scripts import audit as _audit`
with `import audit as _audit` fallbacks at `:569`, `:698`, `:756` — two distinct module objects from
one file, so a test's monkeypatch through one spelling is invisible to the other.
**CLASS: LIVE** — the sheet's most precisely-located row; every locator holds exactly.

**[#537] `disposition token` is a Done-when branch nothing defines** — ASK: enumerate the accepted
tokens where the predicate names them (or withdraw the branch), with a test asserting the `NIE` line
does not satisfy it for `[#409]`.
TARGET: intact and re-verified. The phrase occurs **only** in `tasks/409`, `tasks/410`, `tasks/411`
and their `BACKLOG.md` renderings — no definition, no enumeration, no validator. The near-miss
candidate is live where the row says: `protocols/STANDING_RULINGS.md` **L-8** (~`:1353`) declines a
**fold** for `[#409]`, not the row.
**CLASS: LIVE** (rare case where a `:line` locator still resolves precisely).

**[#540] `harvest_batch.py`** — ASK: a script that reports each lane's board state and fetches every
done lane's packet by `git show`, never by parsing `claude logs`, with a test.
TARGET: **`harvest_batch` has zero occurrences in any `.py` file in the tree** — the row's own
"verified live" claim re-confirmed tonight. `scripts/batch_manifest.py` and
`.claude/commands/lane-integrate.md` both exist as the surfaces it would join.
**CLASS: LIVE.**

**Rollup [E7]:** LIVE 15 · AWAITING-RULING 5 (`[#122]` `[#126]` `[#397]` `[#488]` `[#494]`) ·
**DEAD-CANDIDATE 1** (`[#348]`) · MALFORMED 0.
The largest theme carries the sheet's only dead candidate and its two cheapest fixes — `[#470]` is
one character plus a test, `[#486]` one more. `[#317]` is the one row whose primary build already
landed: re-scope it to the `CLAUDE.md` §4 text rather than rebuild.
Two locator repairs owed (`[#431]` → `PLAYBOOK.md:4240`, `[#317]` → `pyproject.toml:124`).

---

## [E8] ARC-5 execution — 7 rows

**[#354] W6 seed-1 recurrence half** — ASK: a staged-diff CO-CHANGE checker with explicit
ADR-36/41/101 → PLAYBOOK/ESSENTIALS edges, flagging an amendment that lands without its companion
text.
TARGET: unbuilt, **and the row's exclusion re-verified**: `scripts/coherence_nudge.py:37-39`
single-sources its spec set from `validate_reconciliation._SPEC_REGISTRY` — it detects a
*registered spec changed without a version bump* and nothing else. No ADR→PLAYBOOK edge exists
anywhere in the file, confirming "coherence-nudge cannot serve this".
**CLASS: LIVE.**

**[#356] RULING-W + merge-delegation composite** — ASK: each carries a live mechanism with a test,
**or** an entry in `ecosystem/silent-rule-baseline.yaml` with `owner:` and `review_date:`; plus a
ratified ADR or a `STANDING_RULINGS.md` section naming `[#356]`.
TARGET: **the census's blocker has cleared, and the row is now buildable.** The testability census
called this row's register one that "DOES NOT EXIST anywhere in the repo";
`ecosystem/silent-rule-baseline.yaml` **now exists** — but carries **0 `owner:` fields**, so the
done-when is unmet. No `STANDING_RULINGS.md` section names `[#356]`.
**CLASS: LIVE** — status improved from unbuildable to buildable; the census note is stale.

**[#362] `[#242]` carries a substantive guard loss** — ASK: enumerate the 49 dropped rules and carry
each into a live surface, supersede it by a named ADR, or record it in a `STANDING_RULINGS.md`
section naming `[#362]`; and `[#242]` must not reach terminal status first.
TARGET: nothing discharged — no section names `[#362]`, and the dropped-rule set is un-enumerated in
the row or any commit. The blocking constraint is live: `[#242]` is `status: open`, so the ordering
this row protects still holds.
**CLASS: LIVE.**

**[#366] `residual_completeness` scans the working tree, not the staged blob** — ASK: read staged
blob content at commit time, with a regression seeding a staged-unfilled + working-filled pair; or
record the accepted limit in `STANDING_RULINGS.md`.
TARGET: **defect intact and self-declared.** `scripts/validate_residual_completeness.py:41` states
"reads the working tree and shells `git status --porcelain`"; `changed_bundle_files()` shells
`git status --porcelain -uall -z` at `:138`; `scan_file()` reads from disk via
`path.read_text(...)` at `:120`. No `git show :0:`-shaped staged read anywhere.
**CLASS: LIVE.**

**[#400] Ownership-model: the hub-mandated-STRUCTURE / repo-owned-CONTENT cell** — ASK: the
ownership-model ruling explicitly covers the roster cell and is recorded.
TARGET: **the row's own premise is confirmed by the tree.** `[#370]` is now `status: closed` — and
the row predicted exactly that, stating the `owner=user` ruling is "NOT satisfied, NOT
closure-eligible" for this cell. `templates/claude-regions/` carries 8 hub-region carriers and
**no roster region**; `CLAUDE.md` marks all four roster regions `[REPO - local]`. The cell is real
and unruled. **L-5 carve-out member.**
**CLASS: LIVE** (recorded as a decision-shaped row; the closed `[#370]` does not reach it).

**[#402] Intake naming clause — deploy the `<class>` half** — ASK: README §4 carries the ruled
`<class>` grammar AND each post-ratification off-pattern doc is dispositioned.
TARGET: leg 1 unmet — `docs/intake/README.md:146` still carries the 2026-07-08-ratified
`YYYY-MM-DD-{func|tech}-slug.md` infix, and the source audit confirms these are different grammars
(`…status-enum-reconcile.md:106`: "The 2026-07-19 ruling also set naming
(`YYYY-MM-DD-<class>-<slug>`). NOT deployed this lane: README §4 carries a 2026-07-08-ratified
`{func|tech}` infix"). **Leg 2 has grown: 6 post-ratification off-pattern docs today, against the
row's measured 4.**
**CLASS: LIVE** (with a re-measured scope — the pile is larger than filed).

**[#448] A11 staged-diff guard — cover EVERY candidate bundle** — ASK: a staged diff containing two
candidate bundles fails the guard when either is uncovered.
TARGET: unbuilt. `check_handoff_probes` still verifies only `_select_active_bundle`'s single pick —
the same selector `CLAUDE.md` §1 names as the boot-bundle resolver — so an uncovered second
candidate passes silently. Additive by design; erases no selector outcome.
**CLASS: LIVE.**

**Rollup [E8]:** LIVE 7 · AWAITING-RULING 0 · DEAD-CANDIDATE 0 · MALFORMED 0.
The only theme where every row is LIVE, and the one where evidence quality is highest: three rows
(`[#366]` `[#354]` `[#400]`) are confirmed by the indicted code or the tree stating the defect
itself. Two rows carry re-measured scope: `[#402]`'s off-pattern pile grew 4→6, `[#356]`'s blocking
register now exists.

---

## [E9] Fleet Desired-State System (North Star) — 2 rows

**[#392] `fleet_analytics` rename-alias loses history on path-reuse** — ASK: make rename resolution
commit-time-aware and add a real-git rename-back regression test.
TARGET: defect intact by design-read. `build_rename_alias()` (`scripts/fleet_analytics.py:~327`)
builds a single global `old → newer` map in one newest-first pass — its own docstring explains the
single-pass construction — which structurally cannot represent `a→b→a`. The only rename test present
is `tests/test_fleet_analytics.py:73`
(`test_parse_rename_consumes_two_following_tokens`), a **numstat-parse** test, not a history one.
**CLASS: LIVE.**

**[#393] corp-sca rot review — 3 candidates** — ASK: `config/category_mapping.yaml`,
`requirements.txt` and `config/excluded.yaml` in `corp-sca-time-automation` each carry a recorded
confirmed-live-or-retired verdict, and a later `fleet_analytics` run stops flagging the retired ones.
TARGET: **the target repo is not in this session's scope** — only `rdwornik/dev-knowledge` is
attached, and `corp-sca-time-automation` is a declared fleet member
(`ADR-104-fleet-repository-shape.md:149ff`) that the hub by contract does not drive (ADR-28/36).
Unverifiable here **by design**, not by omission.
**CLASS: LIVE** (consumer-repo work; routes via corp-sca, per the row's own text).

**Rollup [E9]:** LIVE 2 · AWAITING-RULING 0 · DEAD-CANDIDATE 0 · MALFORMED 0.
Both rows survive; neither is superseded. `[#393]` is the sheet's cleanest example of a row that
*must* read git-silent from the hub — every path it names lives in another repo, so
`git ls-files` could never resolve it.
`[#392]` is build-ready with the defect located and the missing test class identified.

---

## §10 · Cross-cutting: locator rot, measured on a fresh population

`[#534]` filed "`scripts/audit.py:<line>` locators on four open rows died". Tonight's 72 give an
independent sample, and the rate is material — **6 dead-or-drifted locators across 5 rows (6.9% of
rows)**, none of which killed the row:

```
[#422]  scripts/gen_handoff.py:270-293   -> reflow_framing now at :578          DEAD
[#422]  scripts/assemble_paste.py:97-105 -> call site now at :135-136           DEAD
[#431]  protocols/PLAYBOOK.md:3439       -> doctrine now at :4240               DEAD (points into a RETIRED section)
[#317]  pyproject.toml:61                -> `slow` marker now at :124           DRIFTED
[#496]  scripts/enforcement_coverage.py:895 -> map begins at :897               DRIFTED (2 lines)
[#170]  refs #168                        -> tasks/168-*.md absent in any status DEAD REFERENT (dependency already re-phrased out)
```

`[#431]`'s is the dangerous shape: the cited line still *exists* and still reads like doctrine, but
it now sits inside a section headed **RETIRED**. A reader checking that locator without reading the
heading would conclude the row's premise was withdrawn. Rows whose locators held exactly:
`[#535]` (3 of 3), `[#478]`, `[#518]`, `[#342]`, `[#537]`, `[#470]`.

## §11 · TOP-15 DEAD-CANDIDATE table — honest population: **1**

The contract asked for fifteen ranked by evidence strength. **The evidence supports one.** The
remaining 71 rows name a target that exists and an ask that is unmet; ranking them as dead
candidates would be the stronger-than-the-four-classes language the contract forbids.

| # | id | evidence that the ask is already satisfied | strength |
|---|---|---|---|
| 1 | `[#348]` | Done-when clause 1 — the `· routine:` block is present and **all six ADR-105 fields are populated** at `BACKLOG.md:290`. Clause 2 — the gate `[#270]` is `status: closed` (`tasks/270-operator-load-gauge.md`). **Caveat:** the row is the live anchor of the grooming arc and governs this contract; closure orphans that anchor, so re-scope may beat close. | strong, with a stated caveat |

**The substitute the architect can actually spend tomorrow.** The 14 AWAITING-RULING rows are the
fast verdicts: each needs **one decision and no build** to reach a terminal state. Ranked by how
self-contained the decision is — top rows need nothing beyond the row and this sheet:

| # | id | the one decision owed | pre-work? |
|---|---|---|---|
| 1 | `[#122]` | remove the PATH shim, or keep it as defence-in-depth | none (L-5) |
| 2 | `[#323]` | carry `codemap-generate`/`toc-generate` in `hub_hooks`, or freshness-only | none (L-5) |
| 3 | `[#407]` | the functional-vs-OOP stance + naming convention, or deferred-with-reason | none (L-5) |
| 4 | `[#450]` | section-level intake status schema, or promotion-to-ADR as the terminal path | none (L-5) |
| 5 | `[#449]` | a hard `PASTE_THIS.md` ceiling with its number, or an accepted-with-reason hold | none (L-5) |
| 6 | `[#406]` | the `doc_rot` enforcement point: nudge / pre-commit leg / accept-as-is | none (L-5) |
| 7 | `[#281]` | re-peg the ai-council convergence to Wave-1, or accept Track-X as durable | none (L-5) |
| 8 | `[#494]` | ratify the L0–L5 ladder by ADR, or retire it explicitly | none |
| 9 | `[#126]` | go/no-go on the backpressure-loop primitive | verify live `/loop` semantics first |
| 10 | `[#536]` | a drain target with its number, or the row ceiling re-derived with its basis | 13 loci undispositioned |
| 11 | `[#153]` | core-invariant #5's `--no-ff` scope boundary + the `~/.claude`-reach question | none (L-5); gates `[#189]` |
| 12 | `[#344]` | Ask 1(c)'s replacement now that the `/override` token path is retired | none |
| 13 | `[#397]` | adopt or reject the `scripts/` grouping | **refresh the map first — 50→66 files** |
| 14 | `[#488]` | the ranking axis | research leg owed before the ruling |

Rows 1–8 are rulable from this sheet alone. Rows 9–14 name their pre-work explicitly.

## §12 · MALFORMED count: **0 of 72**

No row's text was too vague to evaluate. The contract named the likely offender —
titles like "Design question" — so it was tested directly rather than assumed:

**`[#323]`, whose title is literally "Design question", is NOT malformed.** Its body states one
closed question ("add `codemap-generate`/`toc-generate` to the carried `hub_hooks` install list?"),
names the decision type (consumer-behaviour policy, operator-gated), names its origin (`[#319]`'s
A5 correction of the v1.3.0 manifest claim), and carries a Done-when that is verdictable in one
read. Only its *title* is a stub; the ASK is unambiguous. Judging on title alone would have
produced a false positive on the sheet's single best test case.

Two other rows read thin at the title — `[#239]` "Follow-up" and `[#43]` "Decide +" — and neither is
in tonight's 72 (both resolved paths in P10 and are therefore out of scope here). If a title-hygiene
ruling is wanted, **the defect is titles, not row bodies**, and it should be scoped to a title
regeneration pass rather than to re-filing rows.

Twelve of the 72 sit in the recorded **L-5 PROSE-JUDGMENT carve-out**
(`protocols/STANDING_RULINGS.md:1316-1317`): `[#122]` `[#126]` `[#153]` `[#281]` `[#323]` `[#397]`
`[#400]` `[#406]` `[#407]` `[#449]` `[#450]` `[#488]`. These are **sanctioned** judgment rows —
"verified at close by the architect against the row's own named criterion". A hygiene ruling that
treated prose-shaped Done-whens as defects would collide with L-5 head-on.

## §13 · Honest limits

1. **No gate ran in this container.** `click` is not installed and `uv` is 0.8.17 against the
   `pyproject.toml` floor of 0.11.19, so `audit.py`, `routine_consumers`, `validate_doc_rot` and the
   test suite could not execute. Every claim here is **source-read + git**, never a live verdict.
   Rows whose state would benefit from execution are flagged in place (`[#457]`, `[#419]`, `[#536]`).
   This is itself a data point for `[#453]` (cloud night-run container gaps).
2. **Six rows target `~/.claude`,** which is outside both this repo and this container:
   `[#116]` `[#153]` `[#189]` `[#289]` `[#346]` `[#71]` (plus `[#130]`'s memory half and `[#431]`'s
   wrapper half). Their in-repo halves were checked and are reported; the off-repo halves are
   **flagged as unverifiable, never assumed satisfied**.
3. **`[#393]` targets `corp-sca-time-automation`,** not attached to this session. Unverifiable here
   by the Layer-2 contract, not by omission.
4. **LIVE means "ask unmet, target real", not "worth doing".** Nothing here ranks value, priority or
   effort. `[#514]` is the only P1 in the set; that is a field, not this sheet's judgment.
5. **Two rows are partially satisfied and reported as LIVE:** `[#317]` (its primary build landed at
   `.claude/skills/verify/verify.py:38`) and `[#514]` (leg 3 discharged). Both would be better
   *re-scoped* than closed or rebuilt — a distinction the four classes cannot express, so it is
   stated here.
6. **`[#348]`'s DEAD-CANDIDATE rests on a facial reading of its own Done-when.** The row is in
   active use as this arc's anchor. The class is a recommendation with its counter-evidence stated;
   the verdict is the architect's.

---

**Lane footprint:** this file, the contract-of-record
`docs/audits/2026-08-19-technical-n4-grooming-wave1-contract.md`, and the
`audit-index-freshness`-mandated regeneration of `docs/audits/README.md`. Zero rows born, zero rows
edited, zero status fields touched, zero registers written, zero scripts added, nothing merged.

---

## AMENDMENT 2026-08-18 — the container gap in §13 is FIXABLE; root cause and fix recorded

**Appended under an amendment marker, not written into §13** — audits are immutable (`CLAUDE.md` §5
rule 3). Same route the batch-1 integrator packet took on 2026-08-18. **§13 limit 1 stands exactly
as written**: no gate ran while the 72 rows were evaluated, and every class in this sheet rests on
source-read + git. This amendment corrects only the *diagnosis* it hands `[#453]`, which said the
toolchain "does not run in this container" and stopped there.

**Root cause.** `uv self update 0.11.19` fails with *"version 0.11.19 was not found"* because it
resolves from the GitHub releases API, which this container's proxy answers **HTTP 403**. The
version is not missing — it is unreachable by that route.

```
api.github.com/repos/astral-sh/uv/releases/tags/0.11.19   HTTP 403   <- what uv self update reads
pypi.org/pypi/uv/0.11.19/json                             HTTP 200   <- the version does exist
```

**Fix, verified live in this session.** `pip install uv==0.11.19` yields a working pinned binary;
`uv run --locked` then resolves and installs the declared environment (27 packages), and the Stop
hook's verbatim command — `uv run --locked python scripts/session_end_backpressure.py` — exits **0**
with all four advisory checks clean. The `pyproject.toml:25` pin (`==0.11.19`, ADR-106) was **not**
touched; relaxing a declared toolchain pin to suit one container is fixing the wrong end.

**What this hands the two owning rows:**
- **`[#453]` (cloud night-run runbook — the container gaps):** the gap is a *provisioning* defect
  with a one-line remedy, not an environment that cannot host a night lane. The runbook line is
  `pip install uv==$(pinned)`, because the self-update path is proxy-blocked by design.
- **`[#554]` (devcontainer + provisioning script):** this is a concrete provisioning-script
  requirement — install the pinned `uv` from PyPI, never via `uv self update`, in any image whose
  egress is proxied.

**Unchanged by this amendment:** all 72 class recommendations, every count in §0, and §13 limits
2–6. Six rows still target `~/.claude` and one targets `corp-sca-time-automation`; those remain
unverifiable from here, and a working toolchain does not change that.
