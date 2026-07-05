# 2026-07-05 — Audit-vs-reality diff (Tier-1.2)

> Every finding of the five 2026-07-04 audits, classified against `main` @ `b557239`
> (repo probes ran against `main` explicitly — `git show main:`, `git grep … main`;
> user-config surfaces `~/.claude/settings.json` / `block-onedrive.ps1` / `ROUTING.md`
> read live, so those rows carry witnessed state instead of SHAs).
> Produced during the 2026-07-05 overnight autonomy run (Block C); drafted by a
> read-only fan-out pass, spot-verified in the main session (three classes probed
> directly: RF-7 live-read, handoff-RF-1 BUILT evidence, rot-INC-1 stale claim — all
> three confirmed).
>
> Verdict classes: **BUILT** (SHA + evidence) · **PARTIAL** (shipped part + remainder)
> · **PENDING** (where filed) · **REJECTED** (where the refusal is recorded) ·
> **INFO** (a verdict/credit/ruling that demands no action) · **UNKNOWN** (probe given).
> **Zero findings unaccounted; zero UNKNOWN.**

## Table

| doc | finding | verdict | evidence/where |
| --- | --- | --- | --- |
| arch | RF-1 OneDrive Edit/Write vector open + map claims closed | PARTIAL | Guard LANDED in ~/.claude (live read): settings.json PreToolUse matcher now `Bash\|PowerShell\|Edit\|Write\|NotebookEdit`; block-onedrive.ps1 inspects `file_path`/`notebook_path`; witnessed firing "blocked CC from writing .secrets/.env" (JOURNAL supplement 38b1e1a, merge 299a6dc). Map row fixed: main ARCHITECTURE.md:196 (e5885c7, merge fbf88ae). Remains: seeded leg-e test; BACKLOG [#191] still OPEN on main |
| arch | RF-2 hub does not self-arm | BUILT | Merge 2e7b072: scripts/arm_hooks.py wired as 5th SessionStart hook + audit.py::check_hooks_armed; ALL_CHECKS 28->29 (29 verified on main); delete-pre-push -> health DEGRADED demonstrated (JOURNAL 07-04) |
| arch | RF-3 "un-gameable" overstated in canon | BUILT | f41460d in merge 3a95e49; main:protocols/DEFINITION_OF_DONE.md:69 "## Honest limits — what this gate does NOT prove" (dirty-tree short-circuit; platform block-cap) |
| arch | RF-4 organ-collision resolved by paperwork (#210 + recurrence-at-n=2) | PENDING | BACKLOG [#210] open on main ("Decide the shape when built"); no register-recurrence rule (grep scripts/ zero); carried architect-2 RESIDUAL §4.4 |
| arch | RF-5 leg-e does not reach the lived workflow | PARTIAL | Harness answer shipped: [#252] Slice A merged a523fca; handoff generator merged 9d5ebe5. Remains: cmd_checks cp1252 crash UNFIXED (audit.py echoes docstring first-lines raw); Slice B unmerged (overnight Block A DEGRADED, merge 5ed18b2) |
| arch | RF-6 consult-lane unwritten (router + record-before-expiry) | PENDING | No consult-tier router line in main PLAYBOOK (grep); no ADR/backlog id; named only in review §8 item 6 |
| arch | RF-7 model-routing smear (ROUTING vs PLAYBOOK) | PENDING | ~/.claude/ROUTING.md:22 still "## SONNET (default Claude Code session)" (live read 2026-07-05, re-verified in-session); no reconciliation anywhere |
| arch | RF-8 ALL_CHECKS accretion (2 v4-era checks) | PENDING | check_handoff_bundle_structure + check_handoff_tag_canonicity still in main ALL_CHECKS; folded to P5 hub-self-prune which is operator-WAIT (RESIDUAL §4.4) |
| arch | RF-9 audit checks mis-key off worktree dir names | PENDING | deployed_methodology_version / no_sibling_orphans unchanged; only the NEW check_hooks_armed resolves via `git rev-parse --git-path hooks` — pattern adopted for the new organ only |
| arch | §3.3 grill #5 --no-verify bypass uncounted | PENDING | No bypass-counting organ on main (no grep hit); unfiled |
| arch | §7 item 1 (Edit/Write guard + map fix) | PARTIAL | = RF-1 row (guard + map landed; seeded test + [#191] closure remain) |
| arch | §7 item 2 (hub self-arm + armed-state check) | BUILT | = RF-2 row (2e7b072) |
| arch | §7 item 3 (DoD honest-limits) | BUILT | = RF-3 row (f41460d / 3a95e49) |
| arch | §7 item 4 (#139 merged-arc verifier before fleet) | PENDING | BACKLOG [#139] open on main |
| arch | §7 item 5 (ASCII-output test + cmd_checks fix) | PENDING | cmd_checks unchanged on main; no ASCII CLI regression test in tests/ |
| arch | §7 item 6 (sandbox harness per §6) | PARTIAL | [#252] Slice A merged a523fca; Slice B held on branch @ c1647f1 (GATE-0 FAILED overnight — marker confound; merge 5ed18b2); consumer seam added on feat/consumer-arc (Codex-gated, unmerged; [#253]) |
| arch | §7 item 7 (register-recurrence rule >=2 same-class) | PENDING | Not built (grep zero); no filed id |
| arch | §7 item 8 (consult-lane codification) | PENDING | = RF-6 row |
| arch | §7 item 9 (operator-load gauge in fleet_health) | PENDING | main:scripts/fleet_health.py has no ratification-count line (grep); routed "load-gauge -> Phase-0 batch" in the 38b1e1a supplement but the merged batch 3a95e49 contains only 4 items, none of them this — Block E drafts it tonight |
| arch | §7 item 10 (ROUTING <-> PLAYBOOK reconcile) | PENDING | = RF-7 row |
| arch | §7 item 11 (release_lint wired to deploy preflight) | PENDING | Zero release_lint refs in main:deploy/tool.py (grep); BACKLOG [#244]: "lint is MANUAL this phase" |
| arch | §7 item 12 (PLAYBOOK freshness posture decided) | PENDING | PLAYBOOK absent from DEFAULT_FRESHNESS_FILES and carries no last_reviewed; no recorded exemption found |
| arch | §7 refusal: no LLM-judged hard gates on semantic properties | REJECTED | Recorded in review §7; main state consistent (nothing built) |
| arch | §7 refusal: no transclusion engine while detection suffices | REJECTED | Recorded §7; [#180] on main still "GATED on DEC-04" |
| arch | §7 refusal: no second conformance organ / no per-component semver | REJECTED | Recorded §7 ("both rightly rejected already") |
| arch | §7 refusal: no scheduled active-push deployer | REJECTED | Recorded §3.2/§7 (breaches autonomy-no); no such job on main |
| arch | §7 refusal: no container layer / no nightly cadence for sandbox | REJECTED | Recorded §7; honored verbatim in BACKLOG [#252] |
| arch | §7 refusal: no new per-session hard gates during ADR-85 freeze | REJECTED | Recorded §7; no new Stop-gates added on main |
| arch | §8 roadmap 1 (P0 edge) | PARTIAL | Guard + map row landed (RF-1 row); seeded-block test absent; [#191] open |
| arch | §8 roadmap 2 (hub arming mesh) | BUILT | 2e7b072; accept criterion met — delete pre-push -> health non-green DEMONSTRATED |
| arch | §8 roadmap 3 (truth-in-canon RF-3+RF-7) | PARTIAL | DoD honest-limits BUILT (3a95e49); ROUTING.md unreconciled (live read) — the "fresh session reading L0" acceptance still fails |
| arch | §8 roadmap 4 (cp1252 fix + ASCII test) | PENDING | = §7 item 5 row |
| arch | §8 roadmap 5 (#139 + recurrence rule + #210 shape) | PENDING | [#139] open, [#210] open, recurrence unbuilt |
| arch | §8 roadmap 6 (consult-lane) | PENDING | = RF-6 row |
| arch | §8 roadmap 7 (P2 PRUNE + sandbox v1 + lint preflight + #221 fleet) | PARTIAL | P2 PRUNE shipped merge 2c86951 (ADR-96; ruff verified-ABSENT on ai-council); sandbox Slice A a523fca; release_lint preflight PENDING; [#221] fleet operator-WAIT |
| arch | §8 roadmap 8 (grooming wave: v4 checks, #130, #212, #213, #229) | PENDING | All four ids open on main; both v4 checks still registered |
| arch | §8 roadmap 9 (operator-load gauge) | PENDING | = §7 item 9 row |
| arch | §6 Q1 ruling (real red flag; split verdict classes, never gate engagement) | PARTIAL | Standard encoded in [#252] frozen contract; implementing slice (B) unmerged |
| arch | §6 Q2 ruling (harness sound; outer deterministic observer; inner never self-certifies) | PARTIAL | Slice A spawn/teardown/isolation merged a523fca; observer + GATE-0 exist only on unmerged feat/lived-sandbox-slice-b @ c1647f1 |
| arch | §6 Q3 SPAWN fork (claude -p in throwaway clone, isolated CLAUDE_CONFIG_DIR, scrubbed env, Sonnet budget) | BUILT | a523fca: deploy/lived_sandbox/spawn.py — _KEEP_ENV scrub, CLAUDE_CONFIG_DIR pinned, CLAUDE_PROJECT_DIR dropped, Sonnet default; isolation PROVEN (and re-proven 3/3 on a consumer clone overnight) |
| arch | §6 Q3 SCOPE fork (v1 deterministic six-hook arc + commands) | PARTIAL | Scoped verbatim into [#252] done-when; arc not yet green — first live run GATE-0 FAILED (marker confound) AND the child never executes the arc (permission/refusal wall, [#253](a)) |
| arch | §6 Q3 ORACLE fork (essence-spec engages: expectations) | PENDING | No `engages:` key in main deploy/manifest (grep); Slice B deliverable per [#252] (exists on the unmerged branch) |
| arch | §6 Q4 ruling (episodic placement, own item + ex-ante contract, RF-2 precondition first) | BUILT | [#252] filed with ex-ante ADR-81 contract + the three refusals; RF-2 arming shipped BEFORE the sandbox (2e7b072) |
| arch | §0 verdict paragraph (sound; detect>prevent; 3 rings) | INFO | Verdict; its 3 named rings each row'd above |
| arch | §3.1 modifiability ACHIEVED (+flat-priority watch item) | INFO | Verdict; watch item still true on main (BACKLOG tiers remain P2/P3-only) |
| arch | §3.2 deployability ACHIEVED@n=1 / AT-RISK-fleet (+§7.6 per-carrier ruling) | INFO | Verdict; conditions tracked at §7-11 (PENDING) + [#221] WAIT |
| arch | §3.3 integrity AT-RISK | INFO | Verdict; both drivers since moved: RF-2 BUILT, RF-1 PARTIAL |
| arch | §3.4 testability ACHIEVED-organs / AT-RISK-workflow | INFO | Verdict; workflow ring advancing via [#252]/[#253] (PARTIAL) |
| arch | §3.5 secondary QAs (availability/performance/security; temp/ exposure) | INFO | Verdict; the actionable half is [#229], still open on main (operator-gated) |
| arch | §5.3 equilibrium verdict ACHIEVED-AND-FRAGILE | INFO | Verdict; fragility (a) = load gauge, still PENDING (Block E drafts it) |
| arch | §8 overall verdict ARCHITECTURALLY SOUND + grade line | INFO | Verdict only |
| arch | EQ: context degradation -> handoff v5 STRONG | INFO | Credit; subsequently reinforced by 9d5ebe5 (generator + anti-bluff) |
| arch | EQ: role-drift -> prose-only ADEQUATE, un-mechanizable | INFO | Credit/limit statement; no action demanded |
| arch | EQ: held-by-memory residual (consult-expiry near-miss; one-line rule) | PENDING | The "ADR before the consult window closes" rule unrecorded (= RF-6) |
| arch | EQ: rot add-only surfaces (prune unbuilt residual) | PARTIAL | P2 PRUNE since shipped (2c86951); gotchas/handoffs/checks unpruned ([#130]/[#212]/RF-8 open) |
| arch | EQ: continuous-conformance design notes (binary verdict + evidence_command; n=2 gate) | INFO | Adopted into the rot design doc §7 |
| arch | EQ: version/state smear residual (lint manual; ROUTING contradiction) | PENDING | Both residuals still open (= §7-11, RF-7) |
| arch | EQ: consumer-surface divergence residual (#95; rosters declarative until P3) | PARTIAL | P3 roster generated (merge a750456) + P4 drift line/Tier-3 shipped (merge 25b104e); #95 template-drift still filed |
| arch | EQ: premature-closure counter-tactics (proxy-gaming persists; #222 pattern) | INFO | Credit; no new ask |
| arch | EQ: operator saturation — THE UNMEASURED LEAK | PENDING | No gauge on main (= §7 item 9); unfiled as a BACKLOG id; Block E drafts the Tier-2 nightly layer with the load-gauge as its FIRST element (standing operator rule) |
| arch | §5.2 degraded-and-restored judged ("it is repeating") | INFO | Verdict only |
| handoff | RF-1 anti-bluff contract inverted (expected: hints) | PARTIAL | Option (b) made STRUCTURAL, merge 9d5ebe5: `_ANSWER_HINT_RE` row-scoped FAIL rung (verified on main in-session) + answer-free PROBES template + hint values diverted to stdout JOURNAL-draft; both 07-04 bundles authored answer-free, dogfood 10/10. OWED: HANDOFF_PROCESS §5/§13 reconciliation + 5.3->5.4 bump (main still `Version: 5.3`) + first manual bluff-dogfood re-run — Block D territory |
| handoff | RF-2 generator unbuilt (#164); hand-copy propagates deviation | PARTIAL | scripts/gen_handoff.py + v5 templates + size-warn + mechanized cold->FILLED flip all merged 9d5ebe5. Remains: live adoption (the 07-04-2 bundle still hand-authored), [#164] open (formal disposition owed; v4-prose removal ADR-83-gated; runbook seeding; cross-repo) |
| handoff | RF-3 browser-side unwitnessable; #159 unclosable as written | PENDING | BACKLOG [#159] open with UNCHANGED done-when; boot-transcript echo unbuilt; carried RESIDUAL §4.3 |
| handoff | RF-4 CLAUDE.md §5 immutability vs §13 fill/fold lifecycle | PENDING | main:CLAUDE.md §5.3 unchanged (ADR-94 status-line exception only; no handoff post-consumption scoping); carried RESIDUAL §4.3 |
| handoff | RF-5 run loop unreliable on default shell (cp1252 / git-bash folklore) | PENDING | cmd_checks unfixed on main; no shell-neutral probe-authoring change evidenced |
| handoff | RF-6 re-narration creep (quadruplicated banner; no size budget) | PARTIAL | Size-warn BUILT citing RF-6 by name (assemble_paste.py `_SIZE_WARN_BYTES = 65_000`, merge 9d5ebe5); paste shrank 59KB->48.9KB; BOOT/RESIDUAL now scaffold-templated. Remains: banner single-sourcing + BOOT-Purpose cap as spec text; priority-as-BACKLOG-field unaddressed |
| handoff | RF-7 nothing verifies PASTE_THIS currency | PENDING | Zero PASTE_THIS/assemble_paste refs in main:scripts/audit.py (grep); no backlog id; recorded only as audit §4 route 7 |
| handoff | RF-8 dead execution-mode default; un-specced lean CC shape | PENDING | HANDOFF_PROCESS unchanged (v5.3, two browser modes only); [#162] open (the fold target); no ruling recorded |
| handoff | RF-9 sequence #234 + runbook-seeding before #221 | PENDING | [#234] and [#221] both open; sequencing de facto preserved by the operator's P6 WAIT rule |
| handoff | §4 route 1 (decide the anti-bluff contract) | PARTIAL | Operator re-ratified withholding (07-04 supplement) + structural rung landed (9d5ebe5); §5 spec edit owed (Block D) |
| handoff | §4 route 2 (boot-transcript echo) | PENDING | = RF-3 row |
| handoff | §4 route 3 (CLAUDE.md §5.3 scoping) | PENDING | = RF-4 row |
| handoff | §4 route 4 (#164 cheap slice: template + size-warn + flip) | BUILT | All three slice items merged 9d5ebe5 — plus the full generator beyond the asked slice |
| handoff | §4 route 5 (single-source banner + cap BOOT Purpose) | PARTIAL | Scaffold templates bound the shape (9d5ebe5); explicit banner single-source + Purpose cap not evidenced in spec/templates |
| handoff | §4 route 6 (shell-neutral probe commands) | PENDING | = RF-5 row |
| handoff | §4 route 7 (paste-currency audit leg) | PENDING | = RF-7 row |
| handoff | §4 route 8 (spec the real population, before #164 builds dead path) | PENDING | = RF-8 row; NB the generator (9d5ebe5) shipped anyway — the "before" sequencing was not honored |
| handoff | §4 route 9 (fleet sequencing) | PENDING | = RF-9 row |
| coherence | RF-1 mechanism-state claims rot (3 surfaces; +doc_claims kind; +grep-canon rule) | PARTIAL | ARCHITECTURE surfaces FIXED (e5885c7 / merge fbf88ae); PLAYBOOK surfaces FIXED (1a41630 / merge 3a95e49). REMAINS: tests/test_legibility_graph_conformance.py:235 still "awareness CLI, NOT in gate by design"; (b) doc_claims mechanism-state kind unbuilt; (c) grep-canon rule unrecorded |
| coherence | RF-2 registry-of-one; ESSENTIALS<->PLAYBOOK edge unmechanized | PENDING | `_SPEC_REGISTRY` still exactly 1 spec on main; PLAYBOOK has no `Version:` line; [#180] still DEC-04-gated |
| coherence | RF-3 blind re-stamp gameable; commit-msg ritual check | PENDING | No reconciled_with commit-msg hook in main:.pre-commit-config.yaml (grep); deeper axis [#220] open |
| coherence | RF-4 fragmented edge vocabulary; #241 needs CoupledSet granularity | PENDING | [#241] open UNCHANGED (still offers the `reconciled_with` remedy the review disputes); scan still frontmatter-only |
| coherence | RF-5 asymmetric corpus walkers — latent FAIL-trap | PENDING | `_EXCLUDE_DIRS` unchanged (no immutable-zone prune port); explicitly flagged "a live correctness bug, unfixed" in architect-2 RESIDUAL §4.3 |
| coherence | RF-6 vanished spec degrades to WARN | PENDING | main reconcile() still maps spec-path-absent -> 'unknown-spec' -> WARN; no FAIL split |
| coherence | RF-7 nudge log has data nobody reads (#181) | PENDING | No coherence-nudge surfacing in main fleet_health.py or .claude/settings.json (grep zero); [#181] open |
| coherence | RF-8 self-model lag (docstrings + untracked 12-rules count) | PARTIAL | validate_reconciliation.py docstring FIXED (5c6765d / merge 3a95e49). REMAINS: main:ARCHITECTURE.md:336 still "live on 12 rules" — prose count, no _CLAIMS deriver |
| coherence | RF-9 test fixtures inside scanned universe | PENDING | No tests/fixtures prune tuple in main:scripts/scan_undeclared_edges.py (grep zero); confirm-hint unchanged |
| coherence | §3 mandate answers (2 genuine edges; divergence narrower-than-stated; 2 stale-edge soft spots; doc_claims incomplete; ceremony watch) | INFO | Analysis answers; their action halves tracked at RF-2/4/5/6 rows + [#241]/[#220] |
| coherence | §4 seq 1 (fix 3 surfaces + 2 docstrings) | PARTIAL | ARCH + PLAYBOOK + validate_reconciliation docstring fixed (fbf88ae, 3a95e49); test-ledger string outstanding |
| coherence | §4 seq 2 (RF-5 port + RF-6 split + RF-9 prune validator arc) | PENDING | None of the three on main (probes above) |
| coherence | §4 seq 3 (adjudicate #241 via CoupledSet; retire 6 dispositions) | PENDING | [#241] open; 6 dispositions still standing |
| coherence | §4 seq 4 (surface nudge log; decide #181 on 4 rows) | PENDING | = RF-7 row |
| coherence | §4 seq 5 (registry-growth vs transclusion; doc_claims kind) | PENDING | Unbuilt; ADR-88 unamended |
| rot | Overall recommendation: build rot_report.py v1 small | PENDING | No scripts/rot_report.py on main; no BACKLOG item; operator rule "defer-until-after-sandbox" (architect-2 RESIDUAL §4.4) — correctly honored tonight (Phase-2 rule, OUT OF SCOPE) |
| rot | D-A report home = gitignored logs/ (default) | PENDING | Approved-on-record; build deferred with v1 |
| rot | D-B host = sibling Task Scheduler task (default) | PENDING | Same — no task registration on main |
| rot | D-C v1 predicates = P1+P2+P3 (default) | PENDING | Same — no predicate code exists on main |
| rot | D-D prune-candidates appendix ships in v1 (default) | PENDING | Same |
| rot | Refusals (§8: no LLM per node; no graph DB; no transitive alarms; no auto-fix/auto-declare; no new declaration format; §3 excluded predicates) | REJECTED | Recorded in doc §3/§8; main consistent (nothing contradicting built) |
| rot | INC-1 manifest stale "components: INERT to deploy/tool.py" claim | PENDING | Still stale on main (verified in-session): deploy/manifest-v1.2.0.yaml:39-40 vs deploy/tool.py reading `components:` status:removed since P2 (merge 2c86951); no filed id |
| rot | INC-2 release_lint docstring "only status: active is legal" | PENDING | Still stale on main: deploy/release_lint.py:15-16 though P2 shipped and the lint validates `removed`/`removed_in`; no filed id |
| codex | CRITICAL-1 teardown guard effectively bypassed | BUILT | Fixed ad719b9, merged a523fca; teardown anchored to `tempfile.gettempdir()` — and witnessed refusing nothing / cleaning fully on tonight's failure path (zero leftovers) |
| codex | CRITICAL-2 failed child runs can still prove isolation | BUILT | `passed` now requires both exits 0; verdict string flags a failed child; isolation re-PROVEN |
| codex | HIGH-1 extra_env can reintroduce scrubbed state | BUILT | `_child_env` pins isolation-critical keys AFTER `extra_env` merge (witnessed working across 4 live spawns tonight) |
| codex | HIGH-2 subprocess failures not normalized | BUILT | spawn() wraps FileNotFoundError / TimeoutExpired / OSError to `SandboxError` |

## Counts

- findings per doc: arch 61 · handoff 18 · coherence 15 · rot 8 · codex 4 — **TOTAL 106**
- per-verdict: **BUILT 12 · PARTIAL 20 · PENDING 53 · REJECTED 7 · INFO 14 · UNKNOWN 0**

## What improved in ~24h (07-04 audits -> main @ b557239)

- **Hub self-arming closed same-day** (2e7b072): SessionStart self-arm + `hooks_armed` check, ALL_CHECKS 28->29, delete-a-hook -> DEGRADED demonstrated live — the review's "cheapest fix in the whole review" landed first.
- **The single highest-severity gap (arch RF-1) substantially closed at L0**: the PreToolUse matcher extended to Edit|Write|NotebookEdit with file_path inspection, map row corrected on main, and the guard WITNESSED firing on its own author — only the seeded test + [#191] closure remain.
- **The anti-bluff property went from hand-discipline to structure** (9d5ebe5): `/expected[ :]/` FAIL rung + answer-free generator/templates + paste size-warn; the next two bundles shipped answer-free (59KB->48.9KB, 10/10 dogfood).
- **Sandbox Slice A built, cross-vendor reviewed, and hardened within one day** (a523fca): Codex's 2 CRITICAL + 2 HIGH all fixed with isolation re-PROVEN — and tonight isolation held 3/3 on a REAL consumer clone (the first `--consumer` measurement, [#253]).
- **The Phase-0 truth-in-canon batch** (3a95e49) cleared three audit findings in one merge: DoD honest-limits (arch RF-3), PLAYBOOK gate-state surfaces (coherence RF-1), validate_reconciliation docstring (coherence RF-8), plus the #251 test red.
- **The honesty machinery caught its own defects instead of shipping false greens**: GATE-0 refused to freeze a facade on the hub self-clone (Block A DEGRADED with an evidence-grade diagnosis), and the first consumer runs exposed the observer's C1 result-field leak + the arc's permission wall ([#253]) — exactly the failure classes the outer-observer doctrine exists to catch.
- **Discipline held under speed**: nothing self-closed — #191/#251/#252/#164 all left open for the operator loop; all four Fable audits merged analysis-only; the rot design stays a landed design, deliberately unfiled until the sandbox proves the shared primitives.

## Residual concentration (where the PENDING mass sits)

The 53 PENDINGs are not uniform: ~14 are deliberate WAITs (P5/P6 fleet, rot-build Phase-2 rule, ADR-83-gated removals) already carrying operator rules; ~12 are filed BACKLOG ids awaiting their turn; the unfiled remainder clusters in four lanes — the consult-lane record rule (RF-6), the cp1252/ASCII CLI class (arch §7-5 / handoff RF-5), the coherence validator arc (RF-5/6/9 — one small arc), and the operator-load gauge (EQ leak; Block E drafts it tonight). Zero PENDINGs contradict a refusal.
