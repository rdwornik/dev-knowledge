# Journal — .dev-knowledge

<!-- scope: meta -->

> Per-session tactical log of `.dev-knowledge` Claude Code work. Entry shape
> as of 2026-05-16 (Council Simplification): `Did / Result / Changes /
> Abandoned / Next`. Newest-first prepend ordering.
>
> Distinct from LESSONS (per-learning generalized rules, oldest-top per
> ADR-29) and handoffs (per-session boundary artifacts for browser-chat
> resumption). JOURNAL is the within-Claude-Code-sessions tactical log
> enabling context recovery across sessions in same repo. The `Changes:`
> line records what files / areas moved — replacing the deleted CHANGELOG.md.
>
> Update protocol: prepend new session entry at top of entry list (under this
> intro blockquote, before existing entries). One entry per Claude Code session
> OR per workday for heavy days. Each entry cites commit hashes, handoff doc,
> or ADR for deeper detail. JOURNAL summarizes, doesn't duplicate.

---

### 2026-06-03 — Tier-1 doc convergence: record the ADR-70 reality into the canonical docs (closes nothing; advances doc-currency)

- Did: 9-document convergence pass making the canonical docs match the shipped Tier-1 layer. One commit per doc on `docs/tier1-doc-convergence`, additive except authorized false-state corrections. CLAUDE §9 (the false hub-hook description) corrected + §8 plugin note + §11 ADR-70; ARCHITECTURE gains a "Tier-1 self-enforcing lifecycle" section (L0/L1/L2 + closure loop); CONTRIBUTING/PLAYBOOK/ESSENTIALS gain the closes-vs-advances rule + closure-loop usage + plugin-propagation runbook; LESSONS +2 (advances-defeats-detection; scan-before-delete); ADR-70 +shipped-reality addendum (L0 relocation + forward closes rule); VISION notes the self-enforcing dimension; BACKLOG +[#76] (the `/review-closures` dedup residual).
- Freshness gate (operator-approved handling): editing the 4 canonical files (VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING) trips audit #10, so each got a genuine end-to-end re-read + `last_reviewed`→2026-06-03 in its own commit. The re-reads surfaced extra **false-state corrected in-place** (clear-false-state rule, same class as §9): ruff "not wired" → wired ([#13] already closed) in ARCHITECTURE + CONTRIBUTING §Validators; audit "10 checks" → 12 (#11 `no_sibling_orphans`, #12 `canonical_structure`) in both.
- Drift FILED (not edited — restructuring, out of scope): CONTRIBUTING §"Handoff process" is broadly stale — says HANDOFF_PROCESS "v2.0 / ADR-37 two-phase overlay pending" + trigger "/session-summary", but the protocol is v4 (stamp 4.3.1, ADR-62 ratified, two-phase shipped) with a dedicated `/handoff` command. Needs a coherent section rework; left for a future pass.
- Changes: CLAUDE.md (v2.11), ARCHITECTURE.md, CONTRIBUTING.md, LESSONS.md, docs/decisions/ADR-70 (addendum), protocols/PLAYBOOK.md, VISION.md, protocols/ESSENTIALS.md, BACKLOG.md (+#76). Commits `c769a07`·`e395a02`·`a68e894`·`4df91b7`·`102ed27`·`89686e8`·`9e89c33`·`ed12ac4`·`31c5896` + this. validate_backlog OK (43 tasks); audit-health green on every commit.
- Flag: [#13] (ruff gate) is already closed/retired — the stale doc refs to it are now corrected; **no closure action needed**. The `validate-backlog` pre-commit hook reported "Skipped" on the BACKLOG commit (pre-commit staged-file quirk) — validated manually instead (OK).
- Next: optional rework of CONTRIBUTING §Handoff process (filed drift); [#76] grooming decision when usage shows whether the command-name collision bites.

---

### 2026-06-02 — Close [#73]: Tier-1 self-enforcing lifecycle plugin rollout complete (operator-approved)

- Did: Operator explicitly approved closing #73. Removed the #73 task line from BACKLOG.md (done-items-leave, ADR-65); validate_backlog OK (42 tasks). Deleted merged branch `chore/5c-converge-hub`.
- Evidence: 5a `9f31f32` (plugin packaged + ai-council pilot) · 5b corp-monorepo `14af351`, corp-ops `262d8bf`, corp-sca `a63e69a` (rolled out to all 4 child repos) · 5c `382a502`+`b1e3345`+merge `f903a68` (hub converged onto its own plugin). The whole arc used `advances [#73]`; this is the closing `closes [#73]` commit.
- Process note (honest): the propose/gate auto-path did NOT propose #73 — STRONG detection keys on a prior `closes [#73]` commit, and none existed (arc used "advances"). `review_closures.py plan --ids 73` correctly refused ("not a proposed candidate"). This was therefore a DIRECT operator close, not a gate-verified propose-close; the underlying work genuinely landed (verified), and this closing commit is the canonical evidence + satisfies the `backlog-id-on-close` hook.
- Next: #73 done. Open follow-ups untouched (#74 Workflow-escalation rule, #75 corp-monorepo Tier-3 Workflow). Possible future groom: hub-local `.claude/commands/review-closures.md` duplicates the plugin's `/review-closures` (flagged in 5c entry).

---

### 2026-06-02 — Unit 5c: converge the hub onto its own plugin — drop duplicate Tier-1 wiring (advances [#73])

- Did: Removed the hub's own Tier-1 wiring so it runs Tier-1 like the children — **subtractive only**. Dropped two redundant hooks from `.claude/settings.json`: `Stop → scripts/propose_closures.py` and `SessionStart → scripts/review_closures.py surface`. Kept the `SessionStart → scripts/fleet_health.py` (Tier-2) hook untouched. Ran the reference scan to decide deletions.
- Why: The hub double-ran Tier-1 — its own settings.json hooks fired alongside the enabled `tier1-lifecycle` plugin's Stop hook (propose_closures 2×/Stop) and the global `~/.claude` `surface-closures.ps1` (doubled surfacing). The plugin (Stop→propose, enabled in hub settings) + global L0 (surface) now cover the loop; verified `surface-closures.ps1` exists at L0 before removing the hub-local surface.
- Scripts removed vs kept: **0 removed.** The ref-scan refuted the "stale orphan" premise — all three hub-local scripts are still referenced after the hook removal, so all kept: `propose_closures.py` (imported by tests/test_propose_closures.py + test_review_closures.py), `review_closures.py` (tests + `.claude/commands/review-closures.md`), `validate_backlog.py` (tests + `.pre-commit-config.yaml` validate-backlog gate + the command). `fleet_health.py` has no dep on the trio (shells out to audit.py only).
- Result: Step-4 hard metric met — ran the **plugin's** propose_closures.py with `CLAUDE_PROJECT_DIR`=hub; it regenerated the hub's `logs/PROPOSALS-2026-06-02.md` (host-root resolution; nothing stray under plugins/), exit 0. 205 tests green; the three kept scripts' tests pass (confirming the keep). git clean (logs/ gitignored).
- Changes: `.claude/settings.json` (−2 hooks, `//` comment corrected to reflect plugin-driven Tier-1), `JOURNAL.md` (this). Commit `382a502` (hook removal). No deletion commit (empty deletion set). #73 5c convergence done; 5a+5b+5c complete.
- Abandoned / flagged: The hub-local `.claude/commands/review-closures.md` now duplicates the plugin's `/review-closures` command (both define the same name) — out of scope for this subtractive pass (scope was the 2 hooks + orphaned scripts); flagged for a future grooming decision. The hub-local scripts/ trio remains the canonical *source* the plugin copies from + the test/pre-commit target, so it correctly stays.
- Next: #73 can close (5a/5b/5c all landed) pending operator review-closures.

---

### 2026-06-02 — Unit 5b: roll out Tier-1 plugin to corp-monorepo, corp-ops, corp-sca (advances [#73])

- Did: Installed `tier1-lifecycle@dev-knowledge-methodology` (the 5a-proven plugin) on the 3 remaining child repos. Per-repo sequence: lint debt check → prep install → verify loop (b/c/d) + gate (a) where applicable. Verifications used a throwaway `#999` item, reverted after each repo. Repos where `.claude/` is fully gitignored (corp-ops, corp-sca) used `git add -f` to make the enablement tracked/reproducible.
- Result: **corp-monorepo** — ruff already clean + gate already installed (v0.15.8); loop installed (`.claude/settings.json` committed normally); loop verified (b/c/d). **corp-ops** — lint clean, no pre-commit; loop + gate asset installed (force-add); loop verified (b/c/d). **corp-sca** — lint clean, no pre-commit; loop + gate asset installed (force-add); loop verified (a/b/c/d). All 3 merged `--no-ff`; all probes reverted leaving repos pristine.
- Changes: corp-monorepo `14af351`, corp-ops `262d8bf`, corp-sca `a63e69a`. `.dev-knowledge`: BACKLOG #73 annotated (5a+5b done; 5c convergence remains), JOURNAL.
- Abandoned / flagged: corp-monorepo already had ruff at v0.15.8 (gate asset not duplicated). Interactive `claude plugin install` + `/reload-plugins` is still the operator's manual step. One error corrected mid-session: deleted the feature branch before merging twice; fixed by re-creating from the commit SHA; no test commits reached any repo's main.
- Next: 5c — converge `.dev-knowledge` itself onto the plugin (retire the bespoke Unit-1..4 `scripts/`+`settings.json`+`pre-commit` wiring). #73 remains open until that convergence.

---

### 2026-06-02 — Unit 5a: package Tier-1 as a portable CC plugin + pilot on ai-council (advances [#73])

- Did: **GROUND FIRST** — confirmed the Claude Code plugin convention against the official docs (via the claude-code-guide agent, not memory): manifest `.claude-plugin/plugin.json`; components at plugin root (`commands/`, `hooks/hooks.json`, `scripts/`); bundled-script refs via `${CLAUDE_PLUGIN_ROOT}`; host repo root via `${CLAUDE_PROJECT_DIR}`; local install via a `.claude-plugin/marketplace.json` + `claude plugin install --scope project`. Then packaged `plugins/tier1-lifecycle/` (plugin.json + hooks.json[Stop→propose, SessionStart→surface] + `/review-closures` command + de-hardcoded copies of propose_closures/review_closures/validate_backlog) and a root `.claude-plugin/marketplace.json` (the hub becomes the methodology marketplace). De-hardcoding: `_host_root()` resolves the data root (BACKLOG/logs/git) from `$CLAUDE_PROJECT_DIR`, while `_SCRIPTS_DIR` stays `__file__`-relative for the bundled validate_backlog — so the script follows the plugin but the data follows the host.
- Result: 4 portability tests (incl. an e2e proving the plugin writes the HOST repo's logs/, not its own dir); 204 suite green + ruff clean + audit-health OK. **Pilot on ai-council — all 4 parts verified** (throwaway `#999`, fully reverted): (a) staged lint error → ruff v0.15.5 gate exit 1 (blocks); (b) `closes [#999]` commit → propose_closures wrote `ai-council/logs/PROPOSALS` proposing #999 STRONG (evidence `79785887d`); (c) surface → `[closures] 1 strong … run /review-closures`; (d) plan re-verified #999 against ai-council's backlog → close removed it + `closes [#999]` commit. ai-council restored pristine (main unchanged at `2e1d409`, no leftover branch/item/logs/files).
- Changes: `.dev-knowledge` only — `plugins/tier1-lifecycle/**` (new), `.claude-plugin/marketplace.json` (new), `BACKLOG.md` (#73 annotated), `JOURNAL.md` (this). `.dev-knowledge`'s own Tier-1 setup UNCHANGED (5b converges). ai-council: no commit (see flag). Commit `9f31f32` (package) + this doc commit.
- Abandoned / flagged: **(1) Ruff gate is NOT a CC-plugin artifact** — a CC plugin cannot ship `.pre-commit-config.yaml` (pre-commit framework is outside plugin scope, confirmed in docs); shipped instead as `assets/ruff-pre-commit.yaml` (pinned rev v0.15.5) + INSTALL.md, installed alongside. **(2) No install committed to ai-council** — ai-council gitignores `.claude/` (`.gitignore:28`), so a project-scoped `enabledPlugins`/`extraKnownMarketplaces` config would need `git add -f` (overriding the repo's deliberate ignore); left for operator decision rather than forced. **(3) Interactive `/plugin install` + live-session hook-firing not driven from here** — verified every mechanical piece the install depends on (hook command strings run exactly as CC would, env vars set), which is the faithful proof available headless. **(4)** `#73` scope corrected: lesson-promotion dropped (Unit-6 deferral); plugin bundles propose/gate/review/surface only.
- Next: 5b — converge `.dev-knowledge` itself onto the plugin (retire its bespoke Unit-1..4 wiring in favor of the installed plugin) + roll the plugin out to corp-monorepo / corp-ops / corp-sca; operator decides the `.claude/`-gitignore install-commit policy per repo.

---

### 2026-06-02 — Unit 6 (lesson-promotion) deferred after STEP 0 grounding

- Did: STEP 0 grounding before any code. Read #4, #12, ADR-35, ADR-70. Found a material scope mismatch: the "lesson-promotion skill" in ADR-70 is actually three separate things — (#4) lessons-index.json + retrieval + CLI query, (#12) `~/.claude/memory/` evolution .jsonl capture substrate, and a third thing (failure-escalation detector from gotcha `verify:` lines + audit history) that Unit 6 proposed. None of these was ready to build: #4 has a different Done-When (retrieval/queryability, not escalation), #12's capture substrate doesn't exist yet, and only 2 of 10 gotcha `verify:` lines are auto-runnable (8 are `verify: manual`).
- Result: No code written, no branch created, no backlog changes. Operator confirmed: the lesson-automation triad (retrieve/capture/promote) is **deliberately deferred** (ADR-35 → future ADR-36), premature at current scale. **Tier-1 is complete-enough as-is.** STEP 0 prevented a wrong build.
- Changes: `JOURNAL.md` only (this entry). Backlog left untouched.
- Abandoned / flagged: The ADR-70 label "lesson-promotion skill — moves captured lessons toward enforced rules (the #4 lessons-feedback-loop machinery)" is loose — it conflated retrieval (#4), evolution-log capture (#12), and escalation-detection (undefined item). Future sessions should not interpret this as a single unit; each arm is its own build with its own prerequisites.
- Next: the triad stays deferred. Tier-1 lifecycle is: ruff gate (#13 ✓) + propose-closures Stop (#8 partial ✓) + review-closures SessionStart+command (#8 partial ✓) + fleet-health Tier-2 (#72 ✓). Unit 5 (plugin bundling, #73) is the natural next step.

---

### 2026-06-02 — Unit 4: Tier-2 fleet-health daily cross-repo audit (closes [#72])

- Did: Implemented ADR-70 Tier-2 session-start-throttled cross-repo audit on `chore/tier2-fleet-health`. `scripts/fleet_health.py` wraps `audit.py run` with a daily throttle: if `logs/FLEET-HEALTH.md` is missing or stale (run_date != today), runs the full 5-repo audit as a subprocess; then reads the per-repo state.yaml files to write a fresh digest; always surfaces a one-liner `[fleet] N/5 repos green as of <date>`. Reuses `audit.py` exclusively — no audit reimplementation. Added a second SessionStart hook to `.claude/settings.json` (timeout 60s, exits 0 always, failures loud on stderr). `logs/FLEET-HEALTH.md` is gitignored (daily snapshot, auto-regenerated).
- Result: 15 tests (throttle, digest, surface, state-yaml parsing, round-trip); 200 suite green throughout. **Step-3 verification (no leftovers):** (A) stale/missing → full audit ran, digest created with today's date, 5/5 green; (B) fresh → `fleet_health.py` skipped the audit (just surfaced cache — confirmed no "running" line); (C) seeded empty `ai-council-orphan-test/` → daily audit caught it (`ai-council | !! | 1`) → removed orphan dir → re-ran → 5/5 green + `no_sibling_orphans: pass` in state.yaml. Dir confirmed removed. **Closes [#72]:** `no_sibling_orphans` now runs automatically on all 5 registered repos, not only at `.dev-knowledge` commit time.
- Changes: `scripts/fleet_health.py` (new), `tests/test_fleet_health.py` (new, 15), `.gitignore` (+`logs/FLEET-HEALTH.md`), `.claude/settings.json` (+SessionStart fleet-health hook), `BACKLOG.md` (#72 retired, grooming-log), `CLAUDE.md` v2.10 (§9 fleet hook), `JOURNAL.md` (this). Commits `1527dee` (fleet script+tests) · `bb02929` (SessionStart hook) · this close.
- Abandoned / flagged: `cmd_run` exits 1 on structural drift FAILs — treated as "ran with issues" (not a crash), so the fleet script writes the digest and surfaces the issue count. The `run_audit` helper considers exit <=1 a healthy execution. `ecosystem/index.yaml` is NOT regenerated by `cmd_run` (it uses `cmd_registry update`); the digest instead reads per-repo state.yaml files directly, which ARE updated by `cmd_run`.
- Next: Unit 5 — bundle all Tier-1/2 hooks into the methodology plugin (#73) for cross-repo install.

---

### 2026-06-02 — Unit 3: /review-closures — human-gated review + closure execution (closure loop now whole; advances [#8])

- Did: Built the review half of the ADR-70 Tier-1 closure loop on `chore/review-closures` — the first contract-driven backlog mutation, so safety is layered. `scripts/review_closures.py` is **read-only on governed state** (reads PROPOSALS + BACKLOG + git, emits a verified plan; never writes BACKLOG, never commits — the agent does that via the command, keeping `scripts/` read-only per CLAUDE §5 #4). The gate `plan_closures` closes ONLY ids passed in (operator-approved), re-verifies each (currently open; STRONG must still have a live evidence commit via `git cat-file`), and returns the exact verbatim task line so the agent's removal Edit is exact-match. `/review-closures` (`.claude/commands/`) is the human-gated orchestrator: surface → present STRONG (`y`) / WEAK (type each `#N`, never bulk) → `plan` → exact-line Edit → `validate_backlog` → JOURNAL + `closes [#N]` commit. Added a project `SessionStart` hook (`review_closures.py surface`) beside the Stop hook: prints a one-line "N closures proposed" when candidates exist, silent otherwise.
- Result: 14 tests (gate matrix + producer↔consumer round-trip + real-git evidence check + a full sandbox done-items-leave loop), 185 suite green + ruff clean + audit-health 10/10. **Step-3 verification (no real item closed):** sandbox loop proved approve #5 → item gone + `closes [#5]` commit, #6/#7 unapproved → untouched; live CLI `plan` re-verified #7→close (real evidence) / #99→skip (not open) with BACKLOG hash untouched (read-only); surfacing prints with candidates (ASCII, cp1252-safe) and is silent + exit 0 with none. Safety layers: human approval → re-verify (open+evidence) → exact-line Edit (fails on mismatch) → `backlog-id-on-close` commit-msg hook.
- Changes: `scripts/review_closures.py` (new), `tests/test_review_closures.py` (new, 14), `.claude/commands/review-closures.md` (new), `.claude/settings.json` (+SessionStart), `BACKLOG.md` (#8 annotated — loop whole, not closed), `CLAUDE.md` v2.9 (§7 command + §9 SessionStart hook), `JOURNAL.md` (this). Commits `9c6b80b` (gate+command+tests) · `0fafd75` (SessionStart) · `5141732` (full-loop integration test) · this doc commit.
- Abandoned / flagged: kept the executor **read-only** (agent applies the Edit) rather than letting a script mutate BACKLOG — resolves the tension with CLAUDE §5 #4 "scripts/ = read-only validators only". WEAK re-verify is open-check only (the operator's typed `#N` is the judgment; WEAK has no closing-commit to re-verify). The surface em-dash was switched to ASCII after it mojibaked in a cp1252 console (the §4 render-layer caveat). **#8 NOT closed** — the closure loop is whole, but session-end clean-tree/staleness + SessionStart lessons-retrieval (#4 territory) + the review-hook overlap remain.
- Next: remaining #8 pieces; Unit 5 bundles propose+surface+review into the methodology plugin (#73). The loop is now self-hosting — future sessions get surfaced proposals at start and close via `/review-closures`.

---

### 2026-06-02 — Unit 2: propose-closures Stop hook — detect-and-propose, never auto-close (advances [#8])

- Did: Built the ADR-70 Tier-1 session-end closure detector on `chore/propose-closures-hook`. `scripts/propose_closures.py` — deterministic (no LLM, cheap at Stop), read-only: scans git for closure evidence against open BACKLOG ids and writes `logs/PROPOSALS-<date>.md` for review at next `/boot`. **Detect-and-propose ONLY — never closes/removes/modifies a backlog item.** STRONG = a `closes [#N]` commit landed but `[#N]` is still open (precise, guarded by still-open). WEAK = an open task names a concrete repo-relative file a no-`closes` commit modified (inferred; exact-path match, churn files excluded; suppressed on cold start where there's no session baseline, to honor precision-over-recall). Reuses `validate_backlog.parse` (loaded by path — no parallel parser, no codemap edge). Wired via a project-level `.claude/settings.json` Stop hook (merges with the user-level hooks; `$CLAUDE_PROJECT_DIR`, timeout 15s, exits 0 → non-blocking). Proposals are gitignored (ephemeral; durable record stays the eventual `closes [#N]` commit + JOURNAL, ADR-65).
- Result: 15 tests (incl. a real-git integration proof: STRONG surfaces a closes+open id, NOT a closed-but-removed one; WEAK fires on a real file-touch). 171 suite green + ruff clean + audit-health 10/10 throughout. **Step-3 verification:** ran the exact wired hook command → artifact produced; BACKLOG `git hash-object` identical before/after (never mutated); real-data precision confirmed — history carries `closes [#13]`/`closes [#29]…` yet 0 strong because those ids were removed (deliberate non-candidates not surfaced); steady-state window mechanism works (prior-baseline → 2-commit window). **Advances [#8]; does NOT close it** (clean-tree/staleness + SessionStart lessons-retrieval + review-hook overlap remain).
- Changes: `scripts/propose_closures.py` (new), `tests/test_propose_closures.py` (new, 15), `.gitignore` (+`logs/PROPOSALS-*.md`), `.claude/settings.json` (new — Stop hook), `BACKLOG.md` (#8 annotated, not closed), `CLAUDE.md` v2.8 (§9 Session-hooks subsection), `JOURNAL.md` (this). Commits `b7f2aa0` (detector+tests) · `750a121` (Stop hook) · this doc commit.
- Abandoned / flagged: first version used a `@dataclass` for Commit — failed under importlib-by-path load (module not in `sys.modules` → dataclass annotation scan hit `None`); switched to a plain class (more robust for the Unit-5 plugin's by-path loading too). WEAK on cold-start was initially noisy (151+ commit window surfaced months-old `audit.py`/`PLAYBOOK.md` edits as false positives) → suppressed WEAK when there's no prior session baseline. ARCHITECTURE.md §Scripts list left unedited (already non-exhaustive — omits `migrate_links.py`; the new script is documented in CLAUDE §9 instead, avoiding a dishonest freshness re-stamp).
- Next: Unit 3 (the `/boot`-side review that consumes PROPOSALS and proposes the actual closures). Remaining #8 pieces (clean-tree/staleness, lessons-retrieval, review-hook overlap). Unit 5 bundles this into the methodology plugin (#73).

---

### 2026-06-02 — Unit 1: wire the version-pinned ruff pre-commit gate (closes [#13])

- Did: Wired ruff as an enforced pre-commit gate on `chore/ruff-precommit-gate`. Added `pyproject.toml` with `[tool.ruff] required-version = ">=0.15.5"` (ruff itself enforces the floor; guards the phantom-I001 trap). Added a local hook to `.pre-commit-config.yaml` using `language: system` (system binary — no pre-commit virtualenv, no version mismatch possible). Gate mode: `ruff check` (no `--fix`) so violations are surfaced to the developer, not auto-silenced. Proved it blocks (step 3): staged `import os`, attempted commit, hook rejected with F401 and `exit 1`. Cleaned up the test file (no leftovers, verified). Updated CLAUDE.md v2.7 (§4 ruff now enforced gate; §9 ruff hook added to the list, stale BACKLOG #13 parenthetical removed; re-read end-to-end before stamping). Retired #13 from BACKLOG (done-items-leave, ADR-65).
- Result: `ruff check` blocks commits on violations. Three independently-revertable commits. 156 tests green + ruff clean + validate_backlog OK (44 tasks) + audit-health 10/10 throughout. **Closes [#13].**
- Changes: `.pre-commit-config.yaml` (ruff hook added), `pyproject.toml` (new; `[tool.ruff]` floor), `CLAUDE.md` v2.7 (§4/§9/§12), `BACKLOG.md` (#13 removed, grooming-log line), `JOURNAL.md` (this entry). Commits `1de2049` (gate) · `63adc83` (claude) · this close.
- Abandoned / flagged: first test file used `# noqa: F401` which suppressed the violation (hook passed instead of blocking) — caught, test file rewritten without the suppressor, proof re-run correctly. The `reset --soft` left tree clean; no phantom worktrees or leftover files.
- Next: #73 (bundle Tier-1 as plugin + cross-repo install) depends on #8/#12/#4 completing first; #13 was the standalone Tier-1 gate — now closed.

---

### 2026-06-02 — Land the three-tier process-automation plan into the durable record (capture-only)

- Did: Recorded the just-decided three-tier self-enforcing process architecture (AI Council verdict 2026-06-02 + the operator's three-tier synthesis) across its three durable surfaces, before any implementation — on `chore/land-process-automation-plan`, one revertable commit per surface, pytest/ruff/validate_backlog green after each. **No building** — capture only.
- Result: ADR-70 written (three tiers: Tier-1 native-primitive lifecycle bundled as one methodology plugin · Tier-2 scheduled `audit.py run` → `fleet-health.md` · Tier-3 explicit/scoped Dynamic Workflows; the Workflow=heavy-execution-analog-of-the-Council escalation rule; supersedes the evidence-ledger custom-file design — git is the ledger). 3 LESSONS captured (tool-adoption symmetry; apply-your-own-enforcement-standard; closure-is-a-manual-step-big-arcs-skip). BACKLOG incorporation: annotated #13/#8/#12/#4/#72 `refs ADR-70` as the Tier-1/2 build units; added net-new #73 (Tier-1 plugin bundle + cross-repo install), #74 (Workflow-escalation rule), #75 (first scoped corp-monorepo Tier-3 Workflow). Merged `--no-ff` (`7c3af75`); branch deleted; tree clean; 156 tests green.
- Changes: `docs/decisions/ADR-70-three-tier-process-automation.md` (new) + `docs/decisions/README.md` (index + traceability), `LESSONS.md` (+3, header re-stamped), `BACKLOG.md` (5 annotations + #73/#74/#75 + grooming-log line), `JOURNAL.md` (this entry). Commits `6b5126b` (ADR) · `93dc32b` (lessons) · `8ca04f8` (backlog) · merge `7c3af75`.
- Abandoned / flagged: nothing dropped. Used `git commit -F -` via the PowerShell tool (Bash-tool here-strings mangle commit subjects — the 2026-06-01 channel-discipline lesson); `git merge` does not accept `-F -` (stdin), so the merge message went through a `$env:TEMP` file that was removed + verified gone (no-leftovers). Noted: operator commit `e8f3998` (ai-council handoff revert) landed on `main` from another terminal mid-session; this branch built cleanly on top.
- Next: build the units when scheduled — #73 (Tier-1 plugin) depends on #13/#8/#12/#4; #75 (Tier-3) adopts + exercises Dynamic Workflows on a scoped corp-monorepo audit.

---

### 2026-06-02 — BACKLOG groom: git-verified retroactive closure of 6 done-but-open items (ADR-65 business record)

- Did: Grooming pass on `chore/backlog-groom`. The backlog wasn't shrinking because work done inside larger arcs (the ecosystem unification; the April–May overhaul) satisfied open items without ever closing them — the arc merges named their own scope, never `closes [#N]`, and nobody removed the items. Git-verified which open items are actually complete (evidence-based, never memory — the discipline that catches false notes like #45's "corp-monorepo not started"), then retired them via ADR-65 done-items-leave. Six closed, two re-scoped to their genuine residual, two updated (gate-lift + de-bloat), one new ADR (ADR-69) recording the #44 reach decision.
- Result: BACKLOG 6 items lighter (gaps stay; ids never reused), `validate_backlog.py` green. **ADR-65 business record — each retired item → closing evidence → one-liner:**
  - **[#29]** cross-repo compliance run — DONE: `audit.py run` discovers + audits all 5 registered repos → per-repo matrix; registration `a94664a`/`039643d`; reach model recorded in ADR-69 (`711e62c`).
  - **[#44]** audit reach decision — DONE: cross-repo runner, Layer-2 read-only; recorded in **ADR-69** (`711e62c`). #72 carries the commit-time residual.
  - **[#45]** baseline → ai-council + corp-monorepo — DONE: both pass adr38_baseline + canonical_md_visibility + canonical_structure and carry all 7 canonical files. ai-council unify `e91ba24`/`b4135e3`; corp-monorepo unify `4c54dd5`/`f1cb75b` (+ prior `b6fe17a`/`7f4351f`). The "corp-monorepo not started" note was FALSE.
  - **[#46]** ADR-63 review cycle → remaining repos — DONE: each child had a conformance/coherence cycle — ai-council `a9785c5`/`2036c4b`, corp-monorepo `b6fe17a`/`bb49f8c`, corp-ops `9d377fb`/`04fb696`, corp-sca `0b4c1bd`/`2331b00`.
  - **[#31]** Council-level migration plan — MOOT: ADR-38 A6 (`2c1f11e`) migrated all 4 repos via Path A (operator-directed, no Council); the Council-plan approach was deliberately not taken.
  - **[#40]** requirements*.txt dot-prefix exception — DONE/no-op: present in ADR-59 (line 47) + mirrored in `audit.py` `_DOT_PREFIX_EXCEPTIONS`.
- Changes: `BACKLOG.md` (−6 tasks; removed the now-empty "Give the auditor cross-repo reach" story; re-scoped #17 + #13; updated #70 + #10; grooming-log line), `docs/decisions/ADR-69-cross-repo-audit-reach-model.md` (new) + `docs/decisions/README.md` (index), `JOURNAL.md` (this entry). Commits `711e62c` (ADR-69) + this groom.
- Abandoned / flagged: **#17 NOT closed** — re-scoped to the genuine residual (encode ADR-54–63 content; the structural lock IS done, the stale "§11 last-5 = 61-65" sub-spec dropped — the template uses generic `ADR-NN` placeholders by design). **#13 NOT closed** — re-scoped to enforce-only ("wire the ruff pre-commit hook, version-pinned" per the corp-monorepo phantom-I001 lesson); the OR-branch (docs corrected) was satisfied, but the operator keeps the enforcement tracker, so the CLAUDE §4/§9 "BACKLOG #13" refs stay valid. **CLAUDE §11 left at 64-68** (not rotated to include ADR-69) — editing CLAUDE.md would trip the `canonical_freshness` gate without a genuine re-review; rotation waits for the next CLAUDE review. #19/#36/#42 scanned, left open (no closure evidence).
- Next: build #13 (version-pinned ruff hook) + #70 (ADR-67 council loop) when scheduled; merge `--no-ff`.

---

### 2026-06-02 — Ecosystem unification: locked the 7-file canonical standard (ADR-38 A6) + unified all 4 child repos

- Did: Two-phase ecosystem-unification arc. **Phase 1 — lock `.dev-knowledge`:** operator-confirmed the Stage-0 standard at the gate (7-file canonical set; ADR-66 story-map backlog form with *proportional depth*, bound to all repos; the CLAUDE 12-section template). Authored ADR-38 §A6 (7-file mandate + identical-spine/proportional-depth structure standard + backlog-form binding) + an ADR-41 Amendments section (supersession chain 41→47→64/65→66; closes BACKLOG #20); bumped `templates/CLAUDE-md-template.md` v2.2 (added the required `last_reviewed` frontmatter it lacked); expanded `audit.py` (mandatory 4→7 + new read-only `check_canonical_structure` #12 with a boundary-aware heading matcher); ran `/codex-review` (one HIGH — the matcher false-passed near-misses — fixed + regression-tested). **Phase 2 — unify the four child repos:** one `chore/ecosystem-unify` branch per repo — built missing canonical files with *real* content (not stubs), normalized every file to the spine, migrated each BACKLOG ADR-41/47 → ADR-66 story-map preserving every open item, stripped stale refs.
- Result: **All 5 repos PASS** `adr38_baseline + canonical_md_visibility + canonical_structure` — the post-lock gap map's 12 child-repo failures → 0. `.dev-knowledge`: 156 tests, ruff clean, self-audit 12/12. Open backlog items preserved: ai-council 11, corp-monorepo 9, corp-ops 1, corp-sca 7. Each child unify: docs-only diff, ruff clean (or pre-existing-debt-only), tests collect, merged `--no-ff` + branch deleted; all five trees clean, no leftover branches.
- Changes: `.dev-knowledge` — `docs/decisions/{ADR-38,ADR-41,README}.md`, `templates/CLAUDE-md-template.md`, `BACKLOG.md` (#20), `scripts/audit.py`, `tests/test_audit.py` + `tests/fixtures/repo-with-structural-checks/*`, two `docs/audits/` snapshots, `ecosystem/`. Child repos — each repo's seven canonical files. Children merged: `b4135e3` (ai-council)·`f1cb75b` (corp-monorepo)·`60610a1` (corp-ops)·`cb063b7` (corp-sca).
- Abandoned / flagged: corp-monorepo's 3 already-closed backlog items left the active file (ADR-65 done-items-leave — `validate_backlog` rejects done tasks; mapped in its JOURNAL migration bridge + git history), flagged for operator. ai-council carries 17 pre-existing ruff errors in `.py` (untouched — docs-only scope). The prompt's `check_doc_refs.py` does not exist; used `audit.py` + `validate_backlog.py`.
- Next: optional — clear ai-council's 17 ruff errors (separate `chore`); execute migrated backlog items in their home repos.

---

### 2026-06-02 — Upstream universalization support: pytest.ini exception + corp-ops/corp-sca registration

- Did: Two `.dev-knowledge`-side actions the readiness scouts surfaced, on `chore/universalization-upstream-support`, one commit each. **Step 1:** added `pytest.ini` to the ADR-59 dot-prefix exception list (it cannot be dot-prefixed — pytest won't read `.pytest.ini` — and is a standard config name like the exempt `pyproject.toml`/`setup.cfg`/`tox.ini`); mirrored in `audit.py` `_DOT_PREFIX_EXCEPTIONS`, recorded as an append-only ADR-59 amendment (2026-06-02), and covered by an exemption test. This was a standard gap (corp-sca FAILed `dot_prefix_discipline` with no in-place fix). **Step 2:** registered `corp-ops` + `corp-sca-time-automation` into the ecosystem manifest via `audit.py run --repo-path` (read-only on the child repos — both child trees verified clean), then `registry update` to regenerate `index.yaml`. Closes the silent coverage gap (the recurring sweep only covers registered repos).
- Result: 140 tests green + ruff clean + audit health 10/10 on every commit. All 5 repos now registered (`['.dev-knowledge','ai-council','corp-monorepo','corp-ops','corp-sca-time-automation']`). The run report surfaces each newly covered repo's own conformance failures (corp-ops 3, corp-sca 4) — that surfacing is the point. Commits `039643d` (audit/ADR-59) · `a94664a` (ecosystem registration).
- Changes: `scripts/audit.py` (+`pytest.ini`), `tests/test_audit.py` (+exemption test), `docs/decisions/ADR-59-*.md` (amendment), `ecosystem/` (new `corp-ops/` + `corp-sca-time-automation/` state+history, refreshed existing state/history, regenerated `index.yaml`), `docs/audits/2026-06-02-ecosystem-audit.md` (run report).
- Abandoned / flagged: nothing dropped. Used `git commit -F <file>` (not the PowerShell `@'…'@` here-string, which the Bash tool mangles into a leading `@` subject — the gotcha flagged in the prior entry); Step 1's first attempt hit it and was message-amended before any second commit.
- Next: touches code (`audit.py`) → `/code-review ultra` before merge. **DO NOT MERGE** until operator GO, then `merge --no-ff` + delete branch.

---

### 2026-06-01 — Process-hardening sweep (G3–G6 + R): render-layer output fix, worktree lifecycle + no-leftovers invariant, command/hook usage protocol, tech-radar retirement

- Did: Ran the G3→G6 + residue process-hardening sweep on `chore/process-hardening-sweep` — sequential phases, one revertable commit per change, per-commit pytest/ruff/audit-health, governed by the audit-health gate + per-phase HARD-criterion gate. **G3:** rewrote the CLAUDE §4 box-drawing rule to target the *render* layer (the TUI paints pipe-tables client-side; the no-op was banning Claude from emitting glyphs it never emits) — fix is flat + code-fenced copy-back output; PLAYBOOK §8 rationale subsection added. **G4:** named the worktree provision→use→ephemeral-teardown lifecycle + a decide-first (different-repo→no-worktree) line + a verify-teardown step, grounded in the `.dev-knowledge-cadence`/`-night-adr` orphans. **G5:** authored the no-leftovers invariant (PLAYBOOK §Session-boundaries + CLAUDE §5 rule #9) with a provision→cleanup round-trip verification (3-command check; ADR-68 ephemeral-worktree precedent + 2026-05-17 decommissioning-gap LESSON). **G6:** added a grounded command/hook usage-protocol table to PLAYBOOK §Claude-Code-internals, reconciled CLAUDE §7/§8 to live `~/.claude` state, added a hooks/commands-in-play line to the CC-prompt skeleton + the ADR-56-mandated `02_METHODOLOGY.tmpl` dual-update (also fixed its false "pre-commit runs ruff" guidance). **R:** dropped the retired `docs/tech-radar/` substrate from §Continuous-Improvement (archived per ADR-60; Stage 6 quarterly→on-trigger; records redirected to ADR/BACKLOG/JOURNAL), fixed the ENVIRONMENT runtime line (Opus 4.8, `/code-review ultra`).
- Result: **8 phase commits, green every commit** (139 tests, ruff clean, audit health 10/10, pre-commit gate passed throughout). All five phase HARD criteria met. CLAUDE.md → v2.5. Filed **BACKLOG [#71]** (reconcile ENVIRONMENT `~/.claude` tree). Captured a tooling LESSON (commit-message channel discipline on a PowerShell-default box).
- Changes: `CLAUDE.md` (§4/§5/§7/§8/§12+version), `protocols/PLAYBOOK.md` (§8 output note, §Session-boundaries parallel-lifecycle + no-leftovers invariant, §Claude-Code-internals usage protocol, §2 prompt skeleton, §Continuous-Improvement tech-radar retirement), `protocols/ENVIRONMENT.md` (runtime line), `templates/handoff/02_METHODOLOGY.md.tmpl` (hook guidance + box-drawing comment), `BACKLOG.md` (+[#71]), `LESSONS.md` (+1). Commits `d97482b`·`19a8845`·`4e1320c`·`1e075a8`·`7117c07`·`77b7445`·`ef8cbfa`·`9edab70` + this wrap.
- Abandoned / flagged: v3.x `templates/HANDOFF_*TEMPLATE.md` **LISTED AND LEFT** — deletion needs the operator's go AND an ADR-39 decommission amendment (they remain registered in ADR-39 lifecycle governance), not a bare `git rm`; §14 Markdown-Governance left (self-flagged deferred); `audit.py` §3.1 console mojibake left (Phase C code not opted in). CLAUDE §8 commands-as-skills taxonomy noted, not over-claimed. **Cosmetic leading `@` on the 5 earlier commit subjects** (PowerShell here-string × Bash tool — see LESSON) — flagged for optional pre-merge reword.
- Next: operator reviews per-phase commits + the final report; **DO NOT MERGE** until GO, then `merge --no-ff` + delete branch. After merge, the night agent can run the independent read-only pass.

---

### 2026-06-01 — Doc-coherence completion (G1 part 2): D1/D2 resolved, engine graphical, PLAYBOOK+protocols+VISION audited

- Did: Closed G1 on `chore/doc-coherence-completion`. Resolved the two part-1 escalations (D1: scope-clarified CLAUDE §4 + converted the methodology-engine ASCII flow to a mermaid graph matching its §Processes siblings; D2: TOKEN-LOG → `logs/` doc refs + an append-only ADR-59 amendment scoping the root rule to governance docs). Reconciled the ADR-43 governing line (target-parameterized, grounded in `routing.py`) + hardened the handoff diagram. Then deep-read the surface part 1 left: PLAYBOOK (full, 2911 lines), AI_COUNCIL_PROCESS, AGENT_FRAMEWORK, ENVIRONMENT, VISION body.
- Result: **~30 mechanical drifts fixed across 13 commits.** PLAYBOOK was systemically stale to the post-2026-05-16 core: live CHANGELOG instructions (ADR-49 retired it, ~13 sites), v3.x handoff content (§8 + format-spec + prompt-card → v4), retired `docs/research/` + nonexistent `OPEN_DECISIONS.md` refs, §18 audit-tool (3→10 checks, health=#69 gate, fixed an internal contradiction), scaffold baseline. Plus VISION body (scope-tag/ADR-43/audit.py), AGENT_FRAMEWORK (check#, backlog ref), ENVIRONMENT (worktree vs ADR-61), ESSENTIALS Polish→English, ADR-68 traceability row. AI_COUNCIL_PROCESS v2.0 was already clean. Green every commit: 139 tests, ruff, audit health 10/10.
- Changes: `CLAUDE.md`, `ARCHITECTURE.md`, `VISION.md`, `protocols/{PLAYBOOK,ESSENTIALS,AGENT_FRAMEWORK,ENVIRONMENT}.md`, `docs/decisions/{README,ADR-59}.md`. 13 commits `6f0d2c9`…+ this.
- Escalated / flagged (not fixed): **docs/tech-radar/** references (folder archived by ADR-60, no grounded replacement — where does tech-eval tracking live now?); ENVIRONMENT runtime state (Opus 4.7→4.8, /ultrareview) is operator-maintained; §14 Markdown-Governance is self-flagged-stale-deferred; lingering v3.x `templates/HANDOFF_*TEMPLATE.md` (deletion needs ask); ADR-68's Council transcript not archived in this repo; two §"Repo conventions" `[TBD]` markers; the audit.py `§3.1` console mojibake (code, not docs).
- Next: operator reviews + decides the tech-radar question; **DO NOT MERGE** until GO, then `merge --no-ff` + delete branch. G1 base is coherent for the audited surface.

---

### 2026-06-01 — Doc-coherence audit (G1 pre-universalization gate): #10 doc-truth set closed

- Did: Ran the pre-universalization coherence audit over the canonical doc set + ADRs on `chore/doc-coherence-audit`. Step-1 `audit.py health` was green but only covers 4 files' freshness + structural checks, so grounded the hard metric (each doc vs reality AND vs the other docs) with file:line — incl. cross-repo verification that ADR-43 routing is actually implemented (`ai-council/src/ai_council/routing.py` `TargetResolver`). Fixed the mechanical drifts one revertable commit each; escalated the genuine convention/placement calls.
- Result: **13 mechanical drifts fixed across 8 commits** — CLAUDE §7 /handoff + §9 ruff/hook-list + §11 ADR-list (64-68) + §4 + version; ARCHITECTURE §Authority/§Validators audit.py status, governing-ADRs 55-68, handoff section+diagram redrawn v3.4→v4 two-phase; ESSENTIALS:364 ADR-43 routing (verified-false "pending" → implemented) + :221 v4 bundle shape; SESSION_SETUP handoff trigger v3.1→v4 (NEW, off-#10); LESSONS header stamp. **2 escalated (decision-required):** D1 ASCII-vs-graphical (CLAUDE §4 vs ADR-51); D2 TOKEN-LOG placement (`logs/` vs root / ADR-59). Green every commit: 139 tests, ruff, audit health 10/10, validate_backlog OK; pre-commit gate passed throughout.
- Changes: `CLAUDE.md`, `ARCHITECTURE.md`, `protocols/ESSENTIALS.md`, `protocols/SESSION_SETUP.md`, `LESSONS.md` (header stamp only — no entry touched), `BACKLOG.md` ([#10] closure-noted, residual escalated). Commits `c0b4f2f`·`cdca459`·`b7bdebb`·`97991a0`·`06ce81c`·`e183bec`·`c099e78`·`4ee8d73` + this.
- Abandoned / flagged: did NOT fix D1/D2 (operator's call); DOCS-ONLY — did NOT wire ruff or touch `audit.py` (ruff = BACKLOG #13). NEW low-signal noted, not fixed: ESSENTIALS:348 Polish text in a universal doc; README ADR↔transcript table has no ADR-68 row.
- Next: operator reviews + decides D1/D2; **DO NOT MERGE** until GO, then `merge --no-ff` + delete branch. [#10] stays open pending the TOKEN-LOG decision.

---

### 2026-06-01 — Backlog allocation pass: #70 (ADR-67), #10 night-agent drifts, ML-3 lesson

- Did: Tidy step 2 on `chore/backlog-allocation` — added **[#70]** (operationalize the ADR-67 Council gated loop; P3/deferred, under a new "Operationalize the Council decision loop" story in Decision management); promoted the night agent's 3 morning-review drifts into **[#10]** (CLAUDE §11 five ADRs behind; ESSENTIALS↔ARCHITECTURE ADR-43 routing contradiction; ESSENTIALS:221 retired v3.x `contents/` subfolder); appended the **2026-05-29 v3.4-abort LESSON** (ML-3 — N+2 of #9 + straggler/multi-surface sub-lessons) in date order.
- Result: validate_backlog OK, audit health green, pre-commit gate passed, tree clean. **Night agent stays built + validated, go-live pending the operator's decision** (ADR-68 merged; dry-run + microtest briefings produced) — no backlog task added (done items leave, ADR-65).
- Next: merged `--no-ff` to main this session per operator instruction; operator eyeballs the #70 wording + #10 additions post-hoc. Night-agent go-live remains the operator's call.

---

### 2026-06-01 — Worktree-sprawl consolidation + parallel-work discipline captured

- Did: Closed out this session's parallel-work sprawl — merged ADR-68 night-agent `--no-ff` (resolved the README index conflict, ordered ADR-66→67→68), pruned 2 stale worktrees (cadence/audit-cleanup) + deleted 5 merged branches; captured the hard-won discipline as a LESSON and reorganized PLAYBOOK §Parallel-sessions (refs ADR-61).
- Result: `main` clean (139 tests, ruff, audit health 10/10). Phase B (LESSONS + PLAYBOOK + this entry) sits on `chore/worktree-discipline`, unmerged, for fresh-eyes review. Orphaned `.dev-knowledge-cadence` dir remains on disk (locked by another process; deregistered from git) — needs a manual `Remove-Item`.
- Next: fresh-eyes review of `chore/worktree-discipline` → merge on GO. The night-adr anchor worktree + its merged branch are removed at session end (can't delete the worktree a live session runs from).

---

### 2026-06-01 — Pre-commit enforcement gate: audit.py health now blocks (closes [#69])

- Did: Turned the detectable-on-demand standard into an actual **gate** (Phase-1 precondition for universalization). Added the `audit-health` pre-commit hook (`python scripts/audit.py health`, `always_run`, `pass_filenames: false`) — reuses the existing pre-commit framework, joins the already-gating validate-backlog + codemap-freshness + commit-msg `[#id]` hooks. **#8's actual scope is session-lifecycle hooks, not this** — flagged at the checkpoint; operator allocated **#69** (next real free id; verbal #69/#70 reservations released, ML-3 is a lesson).
- Result: **FAIL blocks / WARN informs comes for free** — `cmd_health` exits 1 only on a FAIL finding; WARN-level (A1 30-day backstop, missing `last_reviewed`, etc.) prints but exits 0. **Gate proven live:** a throwaway `badconfig.toml` (root `.toml` → check #4 FAIL) was blocked (`git commit` exit 1, HEAD unchanged); cleanup restored `health: OK`. ~1.4s/commit; `--no-verify` bypass. Dual review: **Codex 0 findings**; **fresh-eyes technically-sound** (FAIL/WARN contract, config, docs, bypass, scope all verified). Green: 139 tests, ruff, audit health 10/10, validate_backlog OK.
- Changes: `.pre-commit-config.yaml` (+audit-health hook), `CONTRIBUTING.md` + `protocols/PLAYBOOK.md` (record the gate; replaced the now-false "manual-only / not gated" claims), `BACKLOG.md` (+[#69] then removed on close; [#10] +1 filed drift), `docs/audits/2026-06-01-codex-…` + `…-fresh-eyes-precommit-enforcement-gate.md`. Commits `03913d0`·`0ec9774`·`a81cd6c`·`fb7f717` + this.
- Abandoned / filed-forward / noted: **FE-1** — the gate made ARCHITECTURE §Validators' "audit.py manual invocation" imprecise → **fixed on operator GO** (`7ce5faa`): §Validators now states audit.py's dual mode (`run` manual, `health` pre-commit-gated); the FE-1 clause was removed from [#10]. **FE-2 (I1)** — `cmd_health`'s operational checks (`ecosystem/` present, repos-registered) also exit 1; code correct, `ecosystem/` is git-tracked so present in normal flow, `--no-verify` escapes.
- **Phase-2 constraint (from FE-2):** the universalized gate must run a *conformance-only subset* — drop the `.dev-knowledge`-specific operational checks (`ecosystem/` presence, repos-registered) — so it is portable to child repos.
- Next: Phase 2 = disseminate the gate pattern (conformance-only) to child repos. Session-lifecycle hooks remain [#8]. Merged to `main` (`--no-ff`) this session on operator GO.

---

### 2026-06-01 — ARCHITECTURE methodology-engine section (closes [#68])

- Did: Added `## The methodology engine (feedback loop)` to ARCHITECTURE (#68 — formalized at the next monotonic id; verified #68 free: the parallel `adr67`/`adr68` branches use ADR decision-numbering, not BACKLOG ids). Expresses the repo as a feedback *engine*, not a doc pile: Lessons->ADR->Conventions->Enforcement->Dissemination->loop, with an ASCII flow + a stage->artifact table + the Phase-1-hardens-Enforcement / Phase-2-is-Dissemination framing. Placed between Layer Boundaries and Processes (structural "why" before operational flows); complements ESSENTIALS' tactical "Feedback Loop", not a duplicate.
- Result: Independent fresh-eyes pass = **CONFIRMED-SOUND** (loop logically cyclical; all stage->artifact mappings truthful + spot-verified; placement/voice fit; ASCII-only per CLAUDE §4; no duplication; tight scope — one section + BACKLOG edits, no unrelated rewrites). Genuine end-to-end re-read of ARCHITECTURE; `last_reviewed` stays 2026-06-01. Green: 139 tests, ruff, audit health 10/10, validate_backlog OK.
- Changes: `ARCHITECTURE.md` (+engine section + "Last updated" note); `BACKLOG.md` (+[#68] then removed on close; [#10] extended with 2 filed drifts). Commits `7c8132c` (formalize) · `410ebb5` (section) · `93bb42b` (file drift) + this close.
- Abandoned / filed-forward: did NOT fix the drift surfaced while reviewing — filed to **[#10]**: §Authority "audit.py pending full implementation" (it ships 10 checks) + handoff diagram/version v3.4->v4.3.1 (describes the retired 13-file flow). Marked [#10]'s "ARCHITECTURE validators" sub-item done (handled in the #3 merge). No Codex (prose, single file). Did NOT create a review-artifact file (operator's no-new-files rule). NOT merged.
- Next: operator review + merge GO. The night agent owns the rest of [#10].

---

### 2026-06-01 — Freshness cadence: dual review (Codex + fresh-eyes) applied (closes [#24])

- Did: Ran both pre-merge reviews on the check-#10 branch. **Codex** (code-only path-guard → audit.py + tests): 0 critical, 3 High. **Fresh-eyes** (independent zero-context subagent, full diff): 0 critical, 1 important — independently corroborating the test-coverage gap.
- Result / dispositions: **Codex H2** (`%cs` committer-date false-fails after rebase) → **ACCEPTED**, switched to `%as` author date (stable across rebase/cherry-pick). **Codex H3** (tests over-mock `_git_last_commit_date`) → **ACCEPTED**, added 4 real-git integration tests (committed-stale FAIL, equal-date PASS, no-history `None`, not-a-repo `None`) exercising the shipped subprocess path. **Codex H1** (A2 misses uncommitted/working-tree edits) → **REJECTED + DOCUMENTED**: folding working-tree state would FAIL mid-edit before the stamp is bumped, and contradicts the operator's explicit commit-based A2 definition; post-commit/eventually-consistent boundary now in the docstring + PLAYBOOK. **Fresh-eyes FE-1** (CLAUDE §4 stamped fresh while line 49 carried a stale known-failing-test clause — that test now passes) → **FIXED**, clause removed, **[#24] closed**. Green: 139 tests, ruff, audit health 10/10, validate_backlog OK.
- Changes: `scripts/audit.py` (%cs→%as + working-tree caveat), `tests/test_audit.py` (+4 real-git tests), `protocols/PLAYBOOK.md` (commit-based caveat), `CLAUDE.md` (−stale clause), `BACKLOG.md` (−[#24]), `docs/audits/2026-06-01-codex-sacred-files-cadence-check10.md` + `…-fresh-eyes-sacred-files-cadence.md` (review records); this entry.
- Abandoned: did NOT implement Codex H1 (commit-based by design); did NOT merge (awaiting operator GO).
- Next: operator merge GO. Then Phase 2 (drop check #10 into child repos).

---

### 2026-06-01 — Sacred-files freshness cadence: audit check #10 (closes [#3])

- Did: Built the durable, **portable** canonical-file freshness mechanism (posture-audit C4 — highest-leverage durable fix). `audit.py` **check #10 `canonical_freshness`** (registered in `ALL_CHECKS` → runs in `audit health`/`run`) over the 4 living docs (VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING): **A2 (primary, FAIL)** = `last_reviewed` predates the file's last git-commit date (edited-but-not-re-reviewed); **A1 (backstop, WARN, 30d)** = calendar nudge. Append-only (JOURNAL/LESSONS) + per-session (BACKLOG) excluded; missing stamp → WARN (child-repo-safe); degrades gracefully without git. Operator-tuned from my matrix (A1 was 90d/FAIL → 30d/WARN). +11 tests.
- Result: **dogfood worked** — first run FAILed on ARCHITECTURE (`last_reviewed 2026-05-24 < last edit 2026-05-28`); VISION tripped neither signal (operator predicted this). Genuinely re-read VISION (vs ADRs 60-66 — vision substance holds; fixed stale "Stream backlog"→story-map term, resolving **[#35] GO-2**) + ARCHITECTURE before bumping stamps; added minimal `last_reviewed` frontmatter to CLAUDE + CONTRIBUTING; reconciled ARCHITECTURE+CONTRIBUTING §Validators to the real hook set (dropped retired `backlog_extract.py`). `last_reviewed` semantics ("re-read & confirmed, or drift filed — not touched") + honest scope (edit-hygiene only, NOT content-vs-ADR drift) + **manual-only caveat** (no CI/pre-commit trigger — detectable on demand, does not gate) documented in PLAYBOOK + CLAUDE §4. Green: **135 tests, ruff, audit health 10/10, codemap 0, validate_backlog OK**.
- Changes: `scripts/audit.py` (+check #10 + `_parse_last_reviewed`/`_git_last_commit_date`), `tests/test_audit.py` (+11), `VISION.md` `ARCHITECTURE.md` `CLAUDE.md` `CONTRIBUTING.md` (stamps + reconcile), `protocols/PLAYBOOK.md` (freshness-cadence subsection), `BACKLOG.md` (−[#3]); this entry. Commits `24e95a1` + this.
- Abandoned: did NOT wire a trigger (pre-commit/CI/session-close) — deliberate separate decision; did NOT chase residual doc-truth drift (CLAUDE §7/§8, ARCHITECTURE governing-ADR list, ruff, TOKEN-LOG) — stays tracked under **[#10]/[#13]**; the stale CLAUDE §4 known-failing-test clause is already **[#24]** (that test now passes); **[#35]** stays open for WF-3 + GO-1 (only GO-2 resolved here). NOT merged.
- Next: operator runs Codex `/review` + a fresh-eyes pass (new enforcement + Phase-2 foundation); merge only on operator GO. Phase 2 = drop check #10 into child repos unchanged.

---

### 2026-06-01 — methodology-audit reconciled into main

- Did: Reconciled the 2026-05-31 methodology audit (C1–C12) against main — C1/C2 implemented in the BACKLOG migration; C3–C7/C9/C11 already captured as tasks (#10/#3/#12/#13/#8/#41/#43); C8 (frontmatter) deliberately untracked (low value); the remaining C10/C12 gap closed via new task **[#67]**.
- Result: every methodology-audit finding is now implemented, tracked, or deliberately-untracked; captured the arc LESSON ("fix the model, not the symptom; the operator is the readability oracle"). Docs-only; validator / 124 tests / ruff green.
- Next: pick off [#67] + the other captured tasks (each closes via `[#id]`).

---

### 2026-06-01 — Story-map dual review (Codex + fresh-eyes) + merge

- Did: Ran Codex `/review` (code-only path-guard → the validator + commit-msg hook) and an independent zero-context fresh-eyes pass on the story-map branch; applied Codex's 4 High fixes + committed tests; merged to `main` (`--no-ff`).
- Result: **Codex 0 critical / 4 high — all fixed** (H1 done-marker scoped to structured tokens; H2 hook except narrowed to OSError + loud fail-open; H3 require exactly one `## Big picture`; H4 19 committed unit tests). **Fresh-eyes: 0 critical, merge-ready** — verified ID accounting (all 66 main ids: 1-47 BACKLOG / 48-65 relocation queue / #66 closed `190fce9`), story-map integrity (7 themes/19 stories/47 tasks), both scripts, invariants, docs coherence. Baseline green: **124 tests**, audit 9/9, `validate_backlog` OK. Readability verdict remains the operator's (not self-declared).
- Changes: `scripts/validate_backlog.py` (H1/H3), `scripts/check_backlog_commit_msg.py` (H2), `tests/test_validate_backlog.py` + `tests/test_check_backlog_commit_msg.py` (new, H4), `docs/audits/2026-06-01-codex-backlog-story-map.md` + `…-fresh-eyes-story-map.md` (review records); this JOURNAL entry. Branch (whole readability+story-map arc) merged → `main`.
- Abandoned: did NOT fail-closed the commit-msg hook (kept fail-open-loud, explained); did NOT push to remote; did NOT delete the merged branch.
- Next: pick off backlog tasks (each closes via `[#id]`, hook-enforced); child-repo items relocate via their own sessions (queue drains).

---

### 2026-06-01 — BACKLOG story-map hierarchy (ADR-66): Big Picture → Theme → Story → Task

- Did: Restructured `BACKLOG.md` into a story map (branch `docs/backlog-readability-2026-06-01`, continued). (1) **ADR-66** (Path A; supersedes ADR-64 Decision 2 / layout only). (2) Skeleton (7 themes + 19 user stories) → **operator GO at the checkpoint** with taxonomy adjustments (#6 → own story; #9 + #31 → Cross-repo universalization; #28 kept). (3) Filed all 47 items as task bullets (`[#id] [P][size] · Done when · refs`) under their stories. (4) PLAYBOOK §10 + validator rewritten for the hierarchy (dropped `repo:`). (5) `commit-msg` `[#id]` hook + CONTRIBUTING + the "what's implemented" query.
- Result: BACKLOG = **7 themes / 19 stories / 47 tasks, 152 lines**. `validate_backlog` OK (hierarchy: themes/stories/tasks, every task has id+Done-when, every story has So-that, no orphans); `commit-msg` hook **self-tested live** (task removal without `[#id]` blocked; `closes [#id]` passes); pytest 105, ruff clean, audit 9/9. **Readability verdict is the operator's — NOT self-declared.** **NOT merged** (priority-one rewrite + validator change → operator runs Codex `/review` + a fresh-eyes pass).
- Changes: `docs/decisions/ADR-66-backlog-story-map-hierarchy.md` (new) + README index; `BACKLOG.md` (story map); `protocols/PLAYBOOK.md` §10; `scripts/validate_backlog.py` (hierarchy parser); `scripts/check_backlog_commit_msg.py` (new) + `.pre-commit-config.yaml` (commit-msg stage); `CONTRIBUTING.md`; this JOURNAL entry. Branch commits `90d407b`..`a6e26ea` + this.
- Abandoned: did NOT merge; did NOT touch any child repo; did NOT enforce id monotonicity (uniqueness only — by design).
- Next: operator reviews (Codex + fresh-eyes), merges if it reads right; then tasks get picked off (each closes via `[#id]`, enforced by the hook).

---

### 2026-06-01 — BACKLOG readability pass (terse format, evict child-repo items, seed Now)

- Did: Readability refactor of `BACKLOG.md` (branch `docs/backlog-readability-2026-06-01` off main `db352ee`), after the operator reported the migrated file was still not scannable. (1) PLAYBOOK §10 terse 3-line entry schema + validator rewritten to parse it and fold in the deferred H2/H3 hardening — which **closed [#66]** (its scope was implemented in `ad2ca92`; done item left per ADR-65); `## Now` relaxed to {open,in-progress} (resolves ADR-64 open-Q4). (2) All entries → terse. (3) Evicted the 18 child-repo items (ids 48-65) from `## Coordination` to the relocation queue. (4) Seeded `## Now` with the 3 P1 items as `(suggested)` + moved the preamble to a footer.
- Result: BACKLOG **603 → 223 lines**; 65 → **47 in-file entries** (18 in the queue doc). Validator OK (47 entries, 0 warnings); pytest 105, ruff clean, audit 9/9. **Readability verdict deliberately NOT self-declared — awaits the operator** (the prior pass over-claimed it; readability is the operator's call). **NOT merged** — another priority-one rewrite + validator change → operator runs Codex `/review` + a fresh-eyes pass.
- Changes: `protocols/PLAYBOOK.md` §10 (terse schema), `scripts/validate_backlog.py` (terse parser + H2/H3 + size band), `BACKLOG.md` (terse + evict + Now/footer), `docs/audits/2026-06-01-child-repo-relocation-proposal.md` (now the live queue, 18 items); this JOURNAL entry. Branch 5 commits `ad2ca92`..`534a03f` + this.
- Abandoned: did NOT enforce id monotonicity (uniqueness only — by design); did NOT merge; did NOT touch any child repo (eviction = into the queue doc, not into child repos).
- Next: operator reviews (Codex + fresh-eyes), merges if it reads well; child-repo items relocate via their own sessions (queue drains).

---

### 2026-06-01 — BACKLOG migration: dual review (Codex + fresh-eyes) + merge

- Did: Ran the two pre-merge reviews on `docs/backlog-migration-adr64-2026-06-01` — Codex `/review` (code-only path-guard → `validate_backlog.py` + hook) and an independent zero-context fresh-eyes pass (full-migration integrity). Applied the one consensus finding, tracked the rest, and merged to `main` (`--no-ff`).
- Result: **Both reviews PASS, 0 critical.** Fresh-eyes independently verified all 6 claims (42 removed + recoverable via tag; 65 restructured with unique ids; taxonomy-drop justified by ADR-64; validator read-only + Coordination-exemption safe; docs coherent; no invariant breach). **Consensus finding** (Codex H1 ≡ fresh-eyes Important-1): the validator didn't enforce `id` uniqueness → **fixed** (`44eeae8`, hard-fail on duplicates). Deliberately did NOT add file-order/contiguous monotonicity — wrong by design for stable-ids + gaps-on-removal (documented in code + PLAYBOOK). Codex H2/H3 (repo:/section enforcement) + the regex NTH **deferred** to new item **[#66]** (the implementation prompt scoped the validator narrow). The `validate-backlog` pre-commit hook fired + passed on the [#66] BACKLOG edit (dogfooded end-to-end). Baseline green: 105 tests, audit 9/9, validator OK (66 entries).
- Changes: `scripts/validate_backlog.py` (id-uniqueness + docstring), `protocols/PLAYBOOK.md` §10 (id/done wording), `BACKLOG.md` (+id 66), `docs/audits/2026-06-01-codex-backlog-migration-adr64.md` (Codex artifact) + `…-fresh-eyes-backlog-migration.md` (fresh-eyes record); this JOURNAL entry. Branch (16 commits) merged → `main`.
- Abandoned: did NOT enforce id monotonicity (wrong by design); did NOT auto-apply Codex H2/H3 (deferred to [#66] per narrow-scope directive); did NOT push to remote; did NOT delete the merged branch.
- Next: pick off [#66] validator hardening; execute the child-repo relocations (Coordination drains 21→~3 as those sessions run); quarterly grooming 2026-07-01.

---

### 2026-06-01 — BACKLOG migration: retire 41 verified-done items (ADR-64/65 Step 5)

- Did: Implemented ADR-64/65 Step 5 — removed all **42** done (`closed`/`superseded`/`resolved`) entries from `BACKLOG.md`. Each was SHA/artifact-verified in git first (Step-0 inventory `docs/audits/2026-06-01-backlog-migration-inventory.md`); **zero flagged-unverifiable**. *(Count correction: the Step-0 inventory stated 41; the true count is **42** — it under-listed the `docs/tech-radar/` entry, and the earlier "107 total" used a strict `[status]` regex that skipped the dated-bracket `[closed 2026-05-28]`. This map below is the complete, authoritative removal record: 13 + 6 + 23 = 42.)* This is the one-time bulk-migration JOURNAL map (ADR-65: normally a done item's record rides its own session entry + closing commit — no per-item write; this map exists only because these 41 are removed in bulk outside their original sessions). Removal commit tagged `backlog-migration-2026-06-01` (revert restores any entry verbatim).
- Result: BACKLOG **108 → 66 open entries** (42 done removed); zero done items remain. The technical record stays in git (closing commits below); the business record is in the original per-session JOURNAL entries (this repo's history). Recoverable two ways: `git revert` the tagged removal commit, or the closing commit.
- Changes: `BACKLOG.md` (41 done entries removed; 66 open preserved verbatim); this JOURNAL entry. Restructure into the status-priority layout + `id:`/`repo:` is the next commit (Step 6).
- Abandoned: N/A — nothing flagged; no entry removed without a verified closing anchor.
- Next: Step 6 restructure (status-and-priority layout, assign `id:`); Step 7 child-repo relocation proposal; Step 9 validator.

**Retired-item map — A. embedded closing SHA, verified in git:**

| Retired item | Closing SHA | Delivered |
|---|---|---|
| backlog_extract.py references deleted archive | `a5ed940` | script + tests retired (drift removed) |
| migrate_links SKIP_NAMES stale CHANGELOG | `dc46565` | SKIP_NAMES corrected |
| README ADR index missing 45-50/54 | `dc46565` | index + ARCHITECTURE list completed |
| Codemap generator output spec | `b2296ff` | generator built + convention landed |
| v4 first real test | `93b7b1c` | v4.1 bundle generated end-to-end |
| v3.4 Stage-1 question template | `b4afff3` | claims/scope/gate added to template |
| v3.4 skill pinned v3.3.3 | `e2f85f4` | handoff.md rewritten to v3.4 |
| v3.4 HANDOFF_PROCESS self-consistency | `581c3cb` `60df5b6` `4e3cc3e` | file-count/refs/synthesis/slug reconciled |
| v3.4 ADR-42 Q5 file-count addendum | `581c3cb` | ADR-42 append-only count supersession |
| v3.4 FOLDER_TEMPLATE version drift | `b696474` | version strings normalized to v3.4 |
| v3.4 broken evidence citations | `256e26b` `a86c18d` | 9 refs repointed to docs/archive |
| v3.4 stale refs in ADR-45 | `4e3cc3e` | ADR-45 current-authority pointer added |
| workspace "ADRs" folder alias | `f5322837` | dated-folder aliases removed |

**B. closed by an ADR (verified via the ADR's introducing commit):**

| Retired item | Closing ADR → commit |
|---|---|
| AI Council cross-project transcript routing | ADR-43 → `f6c616f` |
| Draft 5 handoff-methodology ADRs | ADR-55..58 → `aa41258` |
| AI Council debate → ADR for v4 handoff | ADR-62 → `986d350` |
| Codify scrum-master review authority | ADR-63 → `986d350` |
| Folder taxonomy ADR | ADR-60 → `be92f55` |
| Codify git worktree pattern | ADR-61 → `42f2be1` |

**C. artifact/state-verified (closing artifact present/absent in git HEAD):**

| Retired item | Verification |
|---|---|
| ai-council needs AGENTS.md | satisfied then retired by ADR-53 (closure in ai-council repo) |
| ADR-38 self-compliance (src/pyproject) | ADR-38 amendment A5 (2026-05-23) |
| ADR-29 prepend-ordering amendment | superseded by ADR-46 |
| check_backlog_organization regex | verified-by-absence (grep at HEAD → none) |
| Council CLI dual-write trigger | superseded → ADR-43 (`f6c616f`) |
| VISION tier declarations | tier system deprecated (ADR-33/40 amendments) |
| Council research: repo complexity | tier system deprecated (moot) |
| Mechanical gate code (ADR-42 Q5) | superseded by HANDOFF_PROCESS v4 → ADR-62 (`986d350`) |
| audit.py check #8 (handoff structure) | check present in scripts/audit.py (`a7576dd`) |
| v4.2 first real test | v4.2-rerun bundle present under docs/handoffs/ |
| Promote beta→stable (3-run criterion) | superseded by fresh-eyes criterion (v4.3) |
| v4.3 first real test | 2026-05-30 bundle present under docs/handoffs/ |
| Promote v4 beta→stable (fresh-eyes) | v4.3.1 stamp in handoff.md |
| Ecosystem standards audit | superseded by scrum-master review pattern |
| Scale tier evaluation re-eval | resolved — tier system dropped (ADR-40 deprecated) |
| ADR-42 single vs multi-artifact | superseded by ADR-62 (`986d350`) |
| Content-scoped archival principle | superseded by ADR-60 flat-archive (`be92f55`) |
| Fix pre-existing test failure (ratio) | verified-by-absence (test gone; suite green) |
| Option B council-questions folder | created then retired by ADR-60 amendment |
| Decide future of `docs/tech-radar/` | retired — `git mv` to archive then `git rm` (ADR-60 amendment); absent at HEAD |
| AI Council Flow runbook | protocols/AI_COUNCIL_PROCESS.md present (`7ef4fe8`) |
| Mermaid render verification protocol | baked into ADR-51 v2 amendment |
| audit.py mermaid theme check (#7) | check present in scripts/audit.py (`a7576dd`) |

---

### 2026-06-01 — ADR-64 ratified (BACKLOG architecture) + methodology-audit branch merged

- Did: Operator convened the AI Council (pick mode, 4-model panel + openai synthesizer, 2 rounds) on the BACKLOG-architecture question from the 2026-05-31 diagnosis §G brief and authored **ADR-64**. Committed ADR-64 + its routed transcript, brought `docs/decisions/README.md` ADR index current (added rows **62/63/64** — 62/63 were missing) + ADR-64 traceability, and merged the audit branch to `main` (`--no-ff`).
- Result: **ADR-64 Accepted.** Verdict: Q1-A done-items-leave (honor ADR-47); Q2-A status-and-priority taxonomy (named-stream + session-arc sections retired → `repo:` field; `## Now / Open-P1..P3 / Blocked / Coordination`); Q3-A relocate child-repo execution items (separate child-repo sessions per ADR-41); Q4-B-narrow restore rigid schema + add a narrow read-only `scripts/validate_backlog.py`. Active file projected 107 → ~46 entries. Baseline green: 105 tests, ruff clean, audit health 9/9. **Migration itself NOT executed** — it is a follow-on session gated on a migration spec (ADR-64 §"Open implementation questions").
- Changes: `docs/decisions/ADR-64-backlog-architecture.md` (new); `docs/decisions/transcripts/council-out-20260601_103339-pick-council-backlog-architecture-2026-05-31.md` (new, routed); `docs/decisions/README.md` (index rows 62/63/64 + ADR-64 traceability); this JOURNAL entry. Branch `docs/methodology-canonical-audit-2026-05-31` (7 audit + ADR/README + journal commits) merged → `main`.
- Abandoned: N/A. Did NOT edit `BACKLOG.md` (migration is a separate spec'd session); did NOT execute the migration; did NOT push to remote; did NOT delete the merged branch.
- Next: write the BACKLOG migration spec resolving ADR-64's 4 open implementation questions (child-repo triage rule; minimal schema; `## Now` mechanics; in-progress surface); then execute the revertable migration (purge done / relocate child-repo / restructure / add validator) + reconcile PLAYBOOK §10. Add BACKLOG follow-up entries (migration tracking; line-70 obsolescence) when BACKLOG editing resumes.

---

### 2026-05-31 — Methodology + canonical-files audit vs copilot-collections (analysis-only)

- Did: Audited the full `.dev-knowledge` methodology surface (Track 1 artifacts: skills/commands/hooks/instructions; Track 2 canonical living-files) against the `copilot-collections` Customization-track reference, and produced a Council-ready architecture diagnosis of `BACKLOG.md` (Track 3, operator priority-one). A bounded sub-agent studied the reference (Customization track only); Phase-0 grounding read CLAUDE/VISION/ARCHITECTURE/BACKLOG(full)/ESSENTIALS/AI_COUNCIL_PROCESS/PLAYBOOK(TOC+§7+§10)/ADR-39/41/47/48 and verified Track-1 facts against live files. **NO BACKLOG edits, NO structural changes, NO merge.**
- Result: Two draft artifacts in `docs/audits/`. **Headline:** the reference mostly *validates* our artifact methodology (PLAYBOOK §7 already encodes separation-of-concerns / progressive-disclosure / gate-review — several mechanisms richer than the reference); the one high-leverage transfer is severity + progressive-disclosure organization for the BACKLOG actionable surface. **Root cause of BACKLOG bloat = a methodology self-contradiction:** PLAYBOOK §10 still teaches "archive done items to `BACKLOG-archive/`" (a file deleted 2026-05-16, forbidden by CLAUDE §5) while ADR-47-retained says "done items leave; git history is the record" — practice follows neither. Live metrics: 871 lines, 107 entries (66 open / 41 closed-in-place = 38%); the stream taxonomy routes only **15%** of open items, **56%** sit in 4 session-arc sections. Recommended **Option 2 (honor ADR-47)** + **Council route** (forward-looking, multi-ADR ripple, not Path A). Baseline green throughout: 105 tests, ruff clean, audit unaffected (docs-only).
- Changes: `docs/audits/2026-05-31-methodology-canonical-audit.md` (new — §0 inventory · §1 catalog · §2 mapping matrix · §3 severity audit · §4 action plan); `docs/audits/2026-05-31-backlog-architecture-diagnosis.md` (new — problem verification · options matrix · recommendation · Council brief); this JOURNAL entry + `logs/TOKEN-LOG.md` append. Branch `docs/methodology-canonical-audit-2026-05-31`, 7 commits `e1b2339`..(this).
- Abandoned: N/A — deliberately did NOT edit BACKLOG, author ADR-64, revive `BACKLOG_ARCHIVE.md`, re-home cross-repo items, port VS Code/Copilot artifacts, or touch other repos.
- Next: operator runs a fresh-eyes review (Codex `/review` or separate chat — methodology-significant, ≥3 files; self-review insufficient). Then convene Council on the BACKLOG architecture (diagnosis §G brief; subsumes BACKLOG line 70) and, if approved, add the 2 proposed NEW entries (N1 Council architecture; N2 PLAYBOOK §10 reconcile). Branch left for review; **NOT merged.**

---

### 2026-05-31 — BACKLOG marathon-arc reconciliation (2026-05-26 → 05-31)

- Did: Reconciled `BACKLOG.md` against the marathon arc after a full re-read of all 839 lines + arc evidence (LESSONS top-11, JOURNAL window, ADRs 59-63, session-2 bundle, audit.py). Produced a classification table (`docs/audits/2026-05-31-backlog-reconciliation-classification.md`) gated for operator review at the Step-1 STOP, then applied the approved set. Method per operator decision: **update-in-place** (flip `[open]`→`[closed]`/`[superseded]` header + dated note, preserve all prior text). Two NEEDS-DECISION items + the new-entry set were operator-approved before writing.
- Result: **BACKLOG truthful again.** Zero missed full closures (the arc closed its own items in-place). 418 superseded by v4/ADR-62; 576 superseded by ADR-60; 257/286/392/504 partial-updated; 47/801 scope-extended to ADRs 62-63; 3 BACKLOG + 1 LESSONS entries added. Branch-tip verification: **105 tests pass, ruff clean, audit 9/9** (check #8 now sees 4 stamped v4 bundles). Caught + recorded honestly: line 257's sub-items were exercised only at the session-2 bundle-INSTANCE level — the `.tmpl` templates were NOT edited (verified), so template-level work remains open.
- Changes: `BACKLOG.md` (6 entries updated + 3 added + header stamp); `LESSONS.md` (1 prepend); `docs/audits/2026-05-31-backlog-reconciliation-classification.md` (new). Branch `chore/backlog-reconciliation-arc-2026-05-31`, 7 commits `7820b7d`..`b1d4e34` + this JOURNAL entry.
- Abandoned: N/A.
- Next: operator merges `chore/backlog-reconciliation-arc-2026-05-31` → main (`git merge --no-ff`). New entries seed forward work (ecosystem-folder operating model, AI-Council convene-vs-Path-A criterion, Phase-1 operator-invariants section).

---

### 2026-05-31 — Fix: audit check #8 stamp regex skipped v4.3.1 bundles

- Did: Fixed `scripts/audit.py` check #8 (`handoff_bundle_structure`). Its `_BUNDLE_STAMP_RE` matched only two-segment version stamps (`v(\d+)\.(\d+) `), so three-segment `v4.3.1` stamps (first used 2026-05-31) silently failed to match — both v4.3.1 bundles (morning cold-start + session-2) were SKIPPED, not validated. Added optional non-capturing patch segment `(?:\.\d+)?`. Found during the session-2 Phase 2 handoff (audit reported "2 stamped" when 4 v4-era bundles existed).
- Result: **check #8 now detects v4.3.1 bundles** — audit went 2 → 3 stamped valid on main (the +1 is the morning bundle now seen; session-2 adds the 4th once its branch merges). major.minor still drive the v4.3+ four-tag gate (4.3.1 ≥ 4.3 enforced). 2 regression tests added (3-segment detected + still enforces v4.3 rules); suite 103 → 105. Backward compatible — 2-segment stamps still match.
- Changes: `scripts/audit.py` (_BUNDLE_STAMP_RE + comment); `tests/test_audit.py` (2 tests); this JOURNAL entry. Branch `fix/audit-check8-version-stamp-2026-05-31`.
- Abandoned: N/A.
- Next: operator merges `fix/audit-check8-version-stamp-2026-05-31` → main; after both this and the session-2 handoff branch merge, audit will report 4 stamped valid.

---

### 2026-05-31 — Handoff Phase 2 complete (session-2 bundle, matrix Case 4)

- Did: Consolidated Phase 2 for slug `2026-05-31-dev-knowledge-session-2`. Read the sender interview (rich 6-day-arc narrative), cross-checked load-bearing local claims against repo state, resolved all template markers from source (VISION/ESSENTIALS/PLAYBOOK/CLAUDE/BACKLOG/AI_COUNCIL_PROCESS), and generated the 8-file v4.3.1 bundle. Honored the two embedded operator asks: inspected `ecosystem/` folder and named its gap (static snapshot ≠ continuous audit process) in 03_PROJECT; described AI Council convene-vs-Path-A operational flow in 02_METHODOLOGY.
- Result: **Bundle at `docs/handoffs/2026-05-31-dev-knowledge-session-2/` (README + 01–07), all within line budgets (550 total).** Minor drift surfaced + recorded (non-blocking): HEAD `f7de267`→`a21e355` (Phase-1 commit advanced it, benign); "63 ADRs" is actually 36 files numbered to ADR-63; LESSONS "50" unverified (pipe-delimited, header probe inconclusive). Cross-repo ai-council claims left unverified per ADR-41. in-progress/ folder removed.
- Changes: 8 bundle files; this JOURNAL entry. Branch `docs/handoff-session-2-2026-05-31`.
- Abandoned: N/A.
- Next: operator merges `docs/handoff-session-2-2026-05-31` → main; uses the bundle per its README escalation ladder to onboard a fresh chat. Matrix-validation loop note: next handoff invocation will hit Case 4 again (this merge adds commits), not Case 5.

---

### 2026-05-31 — Handoff Phase 1 interview generated (matrix Case 4 live test)

- Did: First live test of the new comprehensive 5-case matrix. Invoked `please create handoff for dev-knowledge`; matrix ran silently and resolved **Case 4** (clean tree + commits since last handoff + today's slug `2026-05-31-dev-knowledge-session` already exists) → auto-selected counter-suffix slug `2026-05-31-dev-knowledge-session-2`. **No scope question, no menu fired** — the fix works as designed. Generated Phase 1 interview for the auto-selected slug.
- Result: Interview at `docs/handoffs/in-progress/2026-05-31-dev-knowledge-session-2/_handoff-interview.md` (four-tag sage→apprentice cluster). HEAD captured `f7de267`; working tree clean. Awaiting operator answers below the PASTE marker.
- Changes: new interview file; this JOURNAL entry. Branch `docs/handoff-session-2-2026-05-31`.
- Abandoned: N/A.
- Next: operator pastes the question block into the sender chat, pastes answers below the marker, saves, then says `complete handoff for dev-knowledge` to run Phase 2.

---

### 2026-05-31 — Handoff skill: comprehensive 5-case decision matrix

- Did: Added a comprehensive **5-case scope/slug decision matrix** to `.claude/commands/handoff.md` as the single entry point for scope decisions on `please create handoff for dev-knowledge`. Cases: (1) uncommitted → capture session; (2) clean+commits+slug-free → capture window; (3) clean+no-commits+slug-free → cold-start; (4) clean+commits+slug-collision → auto counter-suffix (`-2`,`-3`,…); (5) clean+no-commits+slug-exists → clean exit, no Phase 1. Superseded the State-machine "bundle exists → FLAG and ask" line and added a `--slug` operator override.
- Result: **No scope/menu question fires in any state** — every invocation state resolves deterministically from `git status`+`git log`+`ls`. Eliminates the ad-hoc scope-question that surfaced earlier this session (slug-collision Case 4). Skill 135 → 201 lines. Baseline green (103 tests / audit 9/9 / ruff clean).
- Changes: `.claude/commands/handoff.md` — new "Default scope decision — comprehensive matrix" section + State-machine ambiguity line reconciled; this JOURNAL entry. Commits `8e4b5ea` (skill) + this entry. Branch `feat/handoff-skill-comprehensive-fix-2026-05-31`.
- Abandoned: N/A. **Context correction:** the prior partial auto-scope tree was NOT replaced in place — it had already been *reverted* (commit `0c98611`) at the operator's request before this work, so the matrix was added to the clean v4.3.1 base. The abandoned Phase-1 branch + in-progress dir were also already cleaned in that revert; no cleanup commit was needed here. Did NOT touch `HANDOFF_PROCESS.md` (skill is living code per `protocols/*` classification; no spec amendment).
- Next: operator merges `feat/handoff-skill-comprehensive-fix-2026-05-31` → `main`, then tests in the current state (Case 5: today's slug exists, no commits since last handoff). Expected: clean-exit message, no menu, no Phase 1. A future `HANDOFF_PROCESS.md` could absorb the matrix as a first-class spec section (v5 candidate).

---

### 2026-05-31 — Cold-start handoff bundle generated (forward-looking)

- Did: Generated a forward-looking handoff bundle for the next `.dev-knowledge` session. No live session to capture (last real work — ADR-62/63 — already merged + journaled 2026-05-30), so per operator's "forward-looking setup" choice the bundle was reconstructed from the institutional record (JOURNAL arc + BACKLOG + git) rather than a live Phase-1 interview. Single-branch flow (`docs/handoff-cold-start-2026-05-31`) folding both phases; no `in-progress/` interview created (vestigial with no browser-architect sender).
- Result: **8-file v4.3.1/stable bundle at `docs/handoffs/2026-05-31-dev-knowledge-session/` (README + 01–07).** All within line budgets (04 at 54/250); no unresolved markers; audit 9/9 (check #8 validates the stamped bundle). Load-bearing facts re-verified at generation: HEAD `a637f5f`, working tree clean, 103 tests pass, audit 9/9 — drift table all ✅. 04_RECENT carries the four-tag canonical section (v4.3+ requirement); recent-arc facts tagged **inferred** (record-derived, not lived-session) per honest framing. 05_NOW reflects the open queue (P1 routine-handoff adversarial pass, sacred-files enforcement, Council-decisions consolidation; P2/P3 batch).
- Changes: `docs/handoffs/2026-05-31-dev-knowledge-session/` (8 new files), this JOURNAL entry. Branch `docs/handoff-cold-start-2026-05-31`.
- Abandoned: did NOT run a live sage→apprentice interview (no session to interview); did NOT create `in-progress/` (no operator answers to await); did NOT promote/alter the methodology or touch other repos. Baseline left green; nothing fabricated — every drift-table claim carries its verification command.
- Next: operator merges `docs/handoff-cold-start-2026-05-31` → `main` if the bundle reads well. The bundle is the next session's inheritance; use it per its README escalation ladder. Open queue unchanged — operator picks.

---

### 2026-05-30 — ADR patches round 2: Codex /review closure

- Did: Applied 4 mechanical fixes to ADR-62 + ADR-63 + BACKLOG per Codex `/review` findings on first patch session.
- Result: **ADRs ready for permanent merge. Codex's high-severity finding (architect over-thoroughness in previous Patch 1 — expanded "one sentence" reviewer spec into 6-sentence essay) addressed via redistribution: Trade-off 1 returned to brief acceptance phrasing matching repo convention (ADR-59/60/61); extended cost-value reasoning moved to Consequences where rationale belongs.**
- Changes: ADR-62 Trade-off 1 — redistributed to brief ML-2 one-sentence pointer; extended cost-value reconciliation moved to Consequences as final bullet; ADR-63 References — stale "(Facet 2 N+3)" → "(Facet 2, 5 total catches in 24h)"; ADR-62 citation placement — merged `(LESSONS 2026-05-30)` into the n=1 caveat parenthetical; BACKLOG — added one-sentence note on why ADR-44 numbering / ADR-26 amendment path was not taken. Commit `986d350`.
- Abandoned: N/A — all 4 fixes applied per Codex specification; no further Codex review pass (running Codex on its own recommendations is convergence-anti-pattern).
- Next: Merge to main. ADRs lock immutable per ADR-39. Branch: `docs/adrs-v4-ratification-and-scrum-master-codification-2026-05-30`. Merge command: `git checkout main && git merge --no-ff docs/adrs-v4-ratification-and-scrum-master-codification-2026-05-30`. **Self-critique captured (for next LESSONS batch):** architect failure mode in previous Patch 1 — insider over-eagerness. Reviewer specified "one sentence"; I wrote 6 sentences treating the spec as opportunity for full relax-vs-gate exposition. When a reviewer specifies a brevity budget, respect it. Triangulation working at fifth meta-level: Codex caught over-thoroughness at the patch-execution layer.

---

### 2026-05-30 — ADR patches per fresh-eyes review (MERGE WITH PATCHES)

- Did: Applied 5 mechanical patches to ADR-62 + ADR-63 per fresh-eyes Opus 4.8 review verdict. Single ADR commit + BACKLOG entry + this JOURNAL entry.
- Result: **ADRs ready for permanent merge. Sharpest cross-ADR finding (relax-vs-gate tension between ADR-62 and ADR-63 for the same ML-2 disease) acknowledged in Patch 1 + tracked as BACKLOG P3.** Line counts: ADR-62 210→224 lines; ADR-63 191→200 lines. Baseline green throughout (103 / 9/9 / ruff clean).
- Changes: ADR-62 Trade-off 1 — added ML-2 acknowledgment + relax-vs-gate deliberate framing; ADR-62 — "confirmed empirically" → "observed empirically (n=1 bundle; single data point)"; ADR-62 — header renamed "Empirical validation" → "Empirical grounding"; ADR-63 — added one-line Facet 1 inheritance clarifier (inherits ADR-36 unchanged; Option E applies to Facet 2 specifically); ADR-63 — "N+3+" → "5 total catches in 24h (May 29-30): 3 operator + 2 CC" across all three occurrences (main + inline + Empirical grounding); BACKLOG — relax-vs-gate principle (P3, candidate future LESSONS/ADR). Commits `4907d6e` (patches), `19e76fb` (BACKLOG).
- Abandoned: N/A — all 5 patches applied cleanly. One grammatical fit applied to the compact parenthetical form in the Alternatives section (`Facet 2: 5 catches in 24h`). No substantive deviations from reviewer specification.
- Next: Codex `/review` (foundational ADRs = safety-critical per ADR-54), then merge to main. Branch: `docs/adrs-v4-ratification-and-scrum-master-codification-2026-05-30`. Merge: `git checkout main && git merge --no-ff docs/adrs-v4-ratification-and-scrum-master-codification-2026-05-30`. ADRs are permanent records (ADR-39 immutability — no further body edits after merge).

---

### 2026-05-30 — Two foundational ADRs written: v4 ratification (ADR-62) + scrum-master codification (ADR-63)

- Did: Path A chosen over an AI Council convene — wrote both ADRs directly via CC because (1) v4 ratification is post-hoc record of a decision already made + implemented + validated by an independent fresh-eyes Opus 4.8 (PROMOTE WITH CAVEATS), and (2) scrum-master codification has clear empirical grounding pointing to one option (E, hybrid B+C). Phase 0 read the dominant recent ADR convention (ADR-55–60: `# ADR-NN: Title` + bulleted Status/Date/Related/Decommission/Source metadata block + Context/Decision/Consequences, with ADR-58-style Alternatives) and matched it rather than the prompt's section list. Verified every load-bearing citation against the repo before writing.
- Result: **ADR-62 (210 lines) + ADR-63 (191 lines) landed; baseline green throughout (103 tests / audit 9/9 / ruff clean after every commit).** ADR-62 ratifies v4+v4.2+v4.3+v4.3.1 collectively as canonical (stable as of 2026-05-30) and disambiguates the **"v4" naming collision** with ADR-45 (explored-not-adopted "Handoff Architecture v4" — a different design sharing the version label by coincidence; ADR-45 still supersedes nothing). ADR-63 codifies the **unified** asymmetric review-authority structure: Facet 1 = cross-repo strażnik review (N=3, the original BACKLOG P1 grounding); Facet 2 = operator→architect intra-session review (N+3+ in 24h), operationalized via Option E (trigger + per-artifact-class). Both BACKLOG items closed.
- Changes: `docs/decisions/ADR-62-v4-handoff-process-ratification.md` (new), `docs/decisions/ADR-63-scrum-master-review-authority.md` (new), `BACKLOG.md` (2 closures), this JOURNAL entry. Commits `6c9107d` (ADR-62), `551b6c2` (ADR-63), `4855ed4` (BACKLOG), + this entry — branch `docs/adrs-v4-ratification-and-scrum-master-codification-2026-05-30`.
- Abandoned: did NOT use the prompt's literal section list where it diverged from repo convention (matched the ADR-55–60 bulleted-metadata format; flagged the ADR-61 YAML-frontmatter outlier as the single deviation, not the norm). **Corrected three inaccurate prompt citations** before they shipped: ADR-39 is "File Lifecycle Governance" (not "immutability via append" — append-only is one of its lifecycle categories); ADR-41 is "Cross-Session Backlog Architecture" (the prompt's "cross-repo ownership — handoff bundle covers own repo" maps to no real ADR — dropped, not forced); dropped the ADR-43 "informs Phase 2 verification" link as a manufactured connection. **Caught a scope mismatch:** the prompt framed scrum-master codification purely as operator→architect, but BACKLOG P1 actually tracked the cross-repo strażnik review (N=3) — wrote ADR-63 to cover BOTH facets so the closure is honest rather than mismatched (flagged for the planned fresh-eyes review). Did NOT convene Council (Path A); did NOT touch other repos, other ADRs, or any file beyond the 4 expected.
- Next: triangulation per the v4.3.1 codified pattern — insider review (architect chat) + an independent fresh-eyes Opus 4.8 review of both ADRs (foundational records warrant it even though Path A skipped Council). The scope reconciliation in ADR-63 (Facet 1 + Facet 2 under one structure) is the highest-value thing for the outsider to scrutinize. Iterate to convergence; operator merges `docs/adrs-v4-ratification-and-scrum-master-codification-2026-05-30` → `main` when both reviews return <2 critical (judgment-augmented).

---

### 2026-05-30 — LESSONS update: marathon-arc pattern capture (11 entries)

- Did: Closed the LESSONS.md staleness gap (stale since 2026-05-25, flagged across the v4.1/v4.2/v4.3 fresh-eyes reviews + v4.3.1 amendment). First downstream work after v4 stable promotion. Prepended 11 entries capturing patterns from the May 26–30 ecosystem-consolidation + v4-handoff saga.
- Result: **LESSONS.md 386 → 408 lines; append-only preserved (git numstat: insertions only, 0 deletions).** Entries: curse-of-knowledge in insider review · triangulation as a versioning-scoped quality gate · cluster-as-diagnosis · easy-metric closure (sharpening of the 2026-05-24 premature-closure lesson) · new-folder-without-checking N+3 (sharpening of the 2026-05-24 scope lesson) · sage-tagging three-iteration convergence · hand-maintained surface count as the fragility metric · prompt-level convention drift · multi-step intermediate-state verification · honest no-op over fabricated commit · meta-level curse-of-knowledge recursion (the arc-level capstone).
- Changes: `LESSONS.md` (11 entries prepended at top of Entries section), this JOURNAL entry.
- Abandoned: did NOT impose the prompt's `**Observed:**/**Pattern:**/**Recommendation:**/**verify:**` multi-section format — the repo's actual LESSONS convention is single-line pipe-delimited (`### date | source | lesson | category | [scope] | action`), newest-first prepend; converted all 11 to match (the prompt pre-authorized aligning to the real format). Dated all 11 `2026-05-30` (capture-session date, per the log's batching convention — cf. the ~8-entry 2026-05-24 batch) with the 05-29 events cited inline. Did NOT append at end (convention is prepend) and did NOT touch the `Last updated:` header (would register a deletion, breaking the append-only numstat check). Used today's date `2026-05-30`, not the prompt's `2026-05-31` (future date).
- Next: operator merges `docs/lessons-update-marathon-arc-2026-05-30` → `main`. Triangulation deliberately NOT applied here — LESSONS is a routine artifact, operator visual check is the gate (v4.3.1 §A honest scoping). Subsequent operator-prioritized work: Council ratification ADR for v4/v4.2/v4.3/v4.3.1 (P2), scrum-master review-authority codification (P1), doc-truth sweep + remaining ecosystem-audit findings, agent-framework full impl (P1). Merged arc branches are branch-cleanup candidates (ask-first).

---

### 2026-05-30 — v4 HANDOFF_PROCESS promoted to STABLE via v4.3.1 caveat patch

- Did: Merged the v4.3 bundle branch `docs/handoff-2026-05-30` → `main` (`e876f8d`), then ran the v4.3.1 caveat patch on `feat/handoff-v4.3.1-caveat-patch-and-stable-promotion-2026-05-30`. The v4.3 fresh-eyes outsider review (independent Opus 4.8, second pass) returned **PROMOTE WITH CAVEATS**: object-level convergence (4/4 v4.2 critical closed, no new contradictions) but two architectural caveats — **N1** (triangulation codified for the promotion gate only, NOT routine handoffs — curse-of-knowledge inherits to routine artifacts) and **MO1** (`<2 critical → promote` is itself an easy-metric, violating the bundle's own hard-metric rule). Patch operationalizes the verdict across spec amendment (Phase A), PLAYBOOK + ESSENTIALS (B), templates (C), skill (D), BACKLOG (F), JOURNAL (G).
- Result: **v4 HANDOFF_PROCESS promoted `beta → stable` as of the v4.3.1 amendment (2026-05-30); baseline green throughout (103 tests / audit 9/9 / ruff clean after every commit).** Caveats closed: N1 → triangulation scoped honestly in spec §A (guards versioning, not per-artifact); MO1 → promotion criterion restated **judgment-augmented** (mechanical <2 critical AND reviewer Stage-3 verdict PROMOTE/PROMOTE-WITH-CAVEATS; **reviewer judgment overrides count**) in spec §B + PLAYBOOK + ESSENTIALS; N4 → `05_NOW` template conditional block clarifies the operator runs the fresh-eyes review while the apprentice awaits results; N2 → `02_METHODOLOGY` clarifies check #9 is **syntactic** (enumeration/pointer), does NOT catch mis-labeled tags. Version stamp source-of-truth (skill Phase-2 defaults) now `version=4.3.1` / `status=stable`; `README.md.tmpl` carries it via `{{VERSION}}`/`{{STATUS}}` interpolation. Spec 443 → 504 lines (ADR-39 append-only growth).
- Changes: `protocols/HANDOFF_PROCESS.md` (v4.3.1 amendment + header bump), `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md` (judgment-augmented criterion), `templates/handoff/{05_NOW,02_METHODOLOGY}.md.tmpl`, `.claude/commands/handoff.md` (stamp defaults), `BACKLOG.md` (2 closures + 2 new items + Council-ratification scope update), this JOURNAL entry.
- Abandoned: **Phase E was a no-op** — `README.md.tmpl` uses `{{VERSION}}`/`{{STATUS}}` placeholders, not a literal stamp, so the skill's Phase-D default change already drives it; no template edit existed to make, no separate commit. Did NOT introduce the prompt's `## P1 —` top-level BACKLOG headers (would be a new structural pattern) — adapted to the existing `### [PN] [status] Title — slug` convention under the cross-stream section. Did NOT add audit check #10 (semantic tag-lint is BACKLOG, not this patch). Did NOT convene Council (promotion is operator's call; ratification ADR is separate P2). Did NOT touch v4.1/v4.2/v4.3 historical bundles or other repos.
- Next: operator merges `feat/handoff-v4.3.1-caveat-patch-and-stable-promotion-2026-05-30` → `main`. v4 is **stable** — leave alone. Then operator-prioritized downstream: LESSONS.md update (hygiene gate, ~30 min Sonnet/medium), Council ratification ADR for v4/v4.2/v4.3/v4.3.1 (P2), scrum-master review-authority codification (P1), doc-truth sweep + remaining ecosystem-audit findings, agent-framework full impl (P1, Council scope; the N1 routine-handoff adversarial pass is its first concrete extension). Meta-pattern captured: curse-of-knowledge persists at the meta-level — each iteration closes pointed object-level defects cleanly while introducing blind spots one layer up (criterion-as-easy-metric, triangulation-scoped-to-promotion-only). The reviewer's self-referential move (declining mechanical promotion because it violates the bundle's own hard-metric rule) is why the criterion is now judgment-augmented. v4 saga: closed.

---

### 2026-05-30 — Handoff Phase 2: v4.3 bundle consolidated (v4.3 first real test)

- Did: Ran handoff Phase 2 (consolidate) for slug `2026-05-30-dev-knowledge-session` on branch `docs/handoff-2026-05-30`. Read the operator-pasted four-tag sage→apprentice answers (7-wave arc narrative), re-captured repo state, cross-checked all load-bearing claims against repo/git (incl. read-only corp-monorepo per ADR-41), resolved every template marker from source (VISION/CLAUDE/PLAYBOOK/ESSENTIALS/BACKLOG/JOURNAL + interview), generated the 8-file v4.3 bundle (README + `01`–`07`) at `docs/handoffs/2026-05-30-dev-knowledge-session/`, and removed the consumed `in-progress/` interview folder.
- Result: **Bundle consolidated; no drift detected — and one sage `unknown` resolved to known.** Cross-check verified 8 load-bearing claims (HEAD `5a5ab83`, tests 103 / audit 9/9 / ruff, spec 443 / skill 134 / stub 48 lines, LESSONS stale since 2026-05-25, `ecosystem/` no-dot, corp-monorepo `extract-p1-2` unmerged at `a1007b1`, both prior bundles preserved). The `987edac` aborted-folder-cleanup intentionality (sage-tagged `unknown`) resolved at Phase 2 to **intentional** (commit msg "delete aborted handoffs folder (2026-05-29 abort artifact)") — the four-tag discipline turning an unknown into a verified non-event, working as designed. All 8 files within line budgets (04 at 143/250). Bundle carries the four-tag canonical section inline (v4.3 item B) + Phase-2-verdict-labelled facts table + `Generated by HANDOFF_PROCESS v4.3 (status: beta)` stamp. audit.py check #8 validates the stamped bundle structure.
- Changes: `docs/handoffs/2026-05-30-dev-knowledge-session/` (8 new files), removed `docs/handoffs/in-progress/2026-05-30-dev-knowledge-session/`, this JOURNAL entry.
- Abandoned: nothing fabricated; no source files missing (no graceful degradation). Reused the v4.2-rerun bundle's resolved 02/03 marker content as baseline (same sources, generated 1 day prior) + added the v4.3 four-tag-canonicity section to 02. Did NOT promote to stable (gated on fresh-eyes review). Did NOT touch prior bundles, corp-monorepo, or introduce any new folder/convention.
- Next: operator runs the fresh-eyes outsider review of this bundle with the existing meta-reviewer prompt. <2 critical findings → promote v4 `beta → stable` (single commit flipping the stamp in skill + README template); ≥2 critical → v4.4 cycle. Merge `docs/handoff-2026-05-30` → `main` like prior handoff branches.

---

### 2026-05-30 — Handoff Phase 1 interview generated (v4.3 re-test)

- Did: Merged `feat/handoff-v4.3-comprehensive-close-2026-05-29` → `main` via `--no-ff` (merge commit `5a5ab83`; 13 files, +611/−46). Then ran handoff Phase 1 (interview) for slug `2026-05-30-dev-knowledge-session` on branch `docs/handoff-2026-05-30` off `main` tip `5a5ab83`. Wrote `docs/handoffs/in-progress/2026-05-30-dev-knowledge-session/_handoff-interview.md` with the four-tag sage→apprentice preamble (HANDOFF_PROCESS v4.3 Amendment A) + the verbatim §3.1 Past/Present/Future/Wisdom/Warnings cluster.
- Result: Interview awaiting operator answers below the PASTE marker. Post-merge `main` verified green: audit health 9/9. HEAD captured `5a5ab83`, working tree clean at capture.
- Changes: `JOURNAL.md` (this entry), `docs/handoffs/in-progress/2026-05-30-dev-knowledge-session/_handoff-interview.md` (new).
- Abandoned: nothing. Did NOT regenerate over an existing interview (state was Fresh). Did NOT proceed to Phase 2 (no answers yet).
- Next: operator pastes the architect's sage→apprentice answers below the marker, saves, then says `complete handoff for dev-knowledge` → Phase 2 generates the v4.3 bundle. Then fresh-eyes review; <2 critical → promote `beta → stable`.

---

### 2026-05-29 — Handoff v4.3 comprehensive close + enforcement groundwork

- Did: A fresh-eyes outsider review (independent Opus 4.8, zero project context) of the v4.2-rerun bundle surfaced **4 critical + 6 medium + 4 minor findings + the "generated from source" meta-question** that insider review missed. Implemented v4.3 on branch `feat/handoff-v4.3-comprehensive-close-2026-05-29` (off `main` tip `7db738e`): spec amendment (append-only per ADR-39, `cc491aa`), 4 template updates (`7c670ea`), skill alignment (`59a8392`), PLAYBOOK + ESSENTIALS process-versioning rule (`eb9611c`), §3.1 cross-reference pointer (`6b7cf88`), audit checks #8+#9 + fixtures + tests (`e615121`), AGENT_FRAMEWORK.md v0.1 stub (`494afae`), BACKLOG + JOURNAL bookkeeping (this entry). Phase F (§3.1 pointer) was committed **before** Phase E (checks) — reversed from the prompt order — so the test `test_health_ok_with_registered_repo` (which runs `cmd_health` against the real repo) never goes red: check #9's drift-catching ability is proven by its failing fixture, not by a broken commit.
- Result: **v4.3 live at `status: beta`; 90 → 103 tests / audit health 7/7 → 9/9 / ruff clean after every commit.** Critical fixes: C1+C2 — four-tag definitions now inlined as a required standalone section in `04_RECENT` (apprentice applies the discipline from the bundle alone, no PLAYBOOK read); C3 — §3.1 carries a "superseded by Amendment A" pointer (also enforced by new check #9); C4+M2 — `01_ROLE` restructured with a "Who's who" disambiguation table collapsing the architect/browser/Layer-1/sage/sender synonym sprawl into one row. M1 — load-bearing-facts column relabelled `Verdict` → `Phase-2 verdict`. M4/M5 — Q5 rewritten to test *application* (a hypothetical 5-finding audit through the cluster-as-diagnosis lens) and Q7 added testing the two named anti-patterns. Enforcement: `audit.py` check #8 (handoff bundle structure, scoped to **stamped v4 bundles** so pre-stamp v4.1 + v3.x sync bundles are out of scope; four-tag required only v4.3+) and check #9 (§3.1 tag-canonicity lint). Architectural claim sharpened from "8 files generated from source" to "**persistently-maintained surfaces collapsed via ephemeral per-handoff generation + per-generation verification**" — honest about what v4 IS (between-session surface collapse) and IS NOT (zero synthesis-time imperfection). Beta→stable promotion criterion codified (<2 critical on one fresh-eyes review; no Council convene) and the prior "three end-to-end runs" heuristic superseded in spec + BACKLOG. Spec now 437 lines (over the ≤350 budget; append-only ADR-39 growth, accepted; v5 consolidation remains BACKLOG).
- Changes: `protocols/HANDOFF_PROCESS.md` (v4.3 amendment + version bump + §3.1 pointer), `templates/handoff/{01_ROLE,02_METHODOLOGY,04_RECENT,06_QUESTIONS}.md.tmpl`, `.claude/commands/handoff.md`, `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md` (process-versioning), `scripts/audit.py` (checks #8/#9) + `tests/test_audit.py` (+13 tests), `protocols/AGENT_FRAMEWORK.md` (new v0.1 stub), `BACKLOG.md` (closed v4.2-test + check-#8 items; superseded three-runs criterion; +3 items: v4.3 test, fresh-eyes promotion, P2 governance-artifact extension), this JOURNAL entry.
- Abandoned: nothing papered over (every phase self-critique passed). Did NOT rewrite v4.1/v4.2 amendment bodies (append-only). Did NOT touch the v4.1 first-run or v4.2-rerun bundles (preserved historical evidence). Did NOT change v4 architecture (two-phase, 8-file, sage frame all intact). Did NOT invoke Phase 1 of the v4.3 re-test (operator triggers separately). Did NOT convene Council, declare v4.3 stable, create any new folder/naming convention, or use Sonnet for any sub-step. README.md.tmpl had no `Verdict` column to relabel (its drift section is prose) — B5 was a no-op. The "Parallel waves" condensation (B1) had no literal target in the template (it lives in generated bundles); added as a one-line guidance hint in the arc `{{SYNTHESIZE}}` comment instead.
- Next: operator reviews + merges `feat/handoff-v4.3-comprehensive-close-2026-05-29` → `main` (`git merge --no-ff`), then invokes Phase 1 of the v4.3 re-test (`please create handoff for dev-knowledge`), does the architect back-and-forth, runs Phase 2, then a fresh-eyes review with the existing meta-reviewer prompt. <2 critical → promote `beta → stable` (update stamp in skill + README template); ≥2 critical → v4.4 cycle.

---

### 2026-05-29 — Handoff v4.2 re-test Phase 2: bundle consolidated (v4.2 first real run complete)

- Did: Ran handoff Phase 2 (consolidate) for slug `2026-05-29-dev-knowledge-session-v4.2-rerun` on branch `fix/handoff-v4.2-refinements-and-rerun-2026-05-29`. Read the operator-pasted four-tag sage→apprentice answers, re-captured repo state, cross-checked the sender's load-bearing claims against repo/git (incl. read-only corp-monorepo per ADR-41), resolved all template markers from source (VISION/CLAUDE/PLAYBOOK/ESSENTIALS/BACKLOG/JOURNAL + interview), generated the 8-file v4.2 bundle (README + `01`–`07`) at `docs/handoffs/2026-05-29-dev-knowledge-session-v4.2-rerun/`, and removed the consumed `in-progress/` interview folder.
- Result: **Bundle complete; all 7 teaching files within budget (45/84/56/93/56/30/21 vs 100/200/150/250/100/80/50); 0 unresolved markers; no degradation (all sources present).** Cross-check found **1 drift of 9 load-bearing claims**: the sender's `.ecosystem/` registry path — actual registry is `ecosystem/<repo>/state.yaml` (no dot prefix). The sender had correctly pre-tagged it `unknown`, so the v4.2 four-tag discipline prevented it from propagating as fact — the upstream-discipline goal of v4.2 working on its first real run. All 8 other claims verified ✅ (branch-unmerged, LESSONS staleness, `987edac` aborted-folder deletion, v4.1 bundle preserved, corp-monorepo CM-1 unmerged at `a1007b1`, spec 395-line budget, §3.1↔Amendment A supersedence, AI_COUNCIL_PROCESS 343 lines). This completes the **v4.2 first real test** (P3 BACKLOG) end-to-end. README carries the v4.2 status stamp + drift-up section; `04_RECENT` carries the always-emit verification table with verification commands — both v4.2 refinements confirmed live in generated output.
- Changes: `docs/handoffs/2026-05-29-dev-knowledge-session-v4.2-rerun/` (8 new files), removed `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session-v4.2-rerun/`, this JOURNAL marker.
- Abandoned: nothing. NOTE: the operator's raw pasted interview answers were working-tree only by design (never committed); consumed/synthesized into `04_RECENT.md` per the v4 consumption step.
- Next: operator uses the bundle per its `README.md` escalation ladder (paste 01–05 → 06 comprehension → 07 ask-back), then merges `fix/handoff-v4.2-refinements-and-rerun-2026-05-29` → `main`. v4.2 re-test = run 2 of 3 toward `status: beta → stable` (BACKLOG P3). First-move for the next apprentice: LESSONS.md update (hygiene gate), then Council → v4+v4.2 ratification ADR.

---

### 2026-05-29 — Handoff v4.2 re-test Phase 1: interview generated

- Did: Ran the handoff skill (Phase 1) for `.dev-knowledge` self-handoff, slug `2026-05-29-dev-knowledge-session-v4.2-rerun`, on branch `fix/handoff-v4.2-refinements-and-rerun-2026-05-29` (HEAD `fc461f0`, clean tree). State detected = Fresh. Generated the v4.2 sage→apprentice single-cluster interview (Past/Present/Future/Wisdom/Warnings) with the **four-tag** role-frame preamble (witnessed/recall/inferred/unknown — v4.2 Amendment A) at `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session-v4.2-rerun/_handoff-interview.md`.
- Result: Interview written; awaiting operator answers below the PASTE marker. This is the **v4.2 first real test** (re-run) — exercising the v4.2 refinements end-to-end starting at Phase 1.
- Changes: `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session-v4.2-rerun/_handoff-interview.md` (new), this JOURNAL marker.
- Abandoned: nothing. Phase 2 NOT advanced — requires operator-architect paste cycle.
- Next: operator copies the question block into the sender browser chat, gets four-tag-tagged answers, pastes below the marker, saves, then says `complete handoff for .dev-knowledge` → Phase 2 → v4.2 bundle at `docs/handoffs/2026-05-29-dev-knowledge-session-v4.2-rerun/`.

---

### 2026-05-29 — Handoff v4.2 refinements + re-test invoked

- Did: v4.1's first end-to-end run (handoff bundle for THIS session, merged to `main` this evening, merge `93b7b1c`) surfaced **7 refinement-level issues — no architectural defects; v4 design sound.** Implemented v4.2 on branch `fix/handoff-v4.2-refinements-and-rerun-2026-05-29`: spec amendment (append-only per ADR-39, `a333265`), 4 template updates (`ac0d2b4`), skill alignment (`08aa5d9`), PLAYBOOK + ESSENTIALS methodology-rule elevation (`41fc541`), BACKLOG + JOURNAL bookkeeping. Then (Phase 6) invoked Phase 1 of a v4.2 re-test handoff to validate end-to-end with the refinements.
- Result: **v4.2 live; 90 tests / audit 7/7 / ruff clean after every commit.** Key change: sage tagging now uses four tags (witnessed / recall / inferred / unknown) — v4.1's single "witnessed" was ambiguous and bit on the aborted-folder claim (effectively `recall`, tagged `witnessed`). Verification table now a required section of every `04_RECENT` (drift or no drift), columns `Claim | Repo fact | Verdict | Verification command`. README drift cross-check moved up (after escalation ladder, before bundle contents). Version + status stamp added (`Generated by HANDOFF_PROCESS v4.2 (status: beta)`). Bundle-maintenance-during-session path defined. 05_NOW forced-ranking warning. Codex clarity sentence. "Handoff is back-and-forth" promoted from handoff-only to general PLAYBOOK methodology (all LLM-LLM context transfer) + ESSENTIALS one-liner. Spec now 395 lines — **over the ≤350 budget by 45**; append-only amendment (ADR-39) + "don't rewrite v4.1 body" make shrinking impossible without violating governance (flagged, accepted).
- Changes: `protocols/HANDOFF_PROCESS.md` (v4.2 amendment + version bump), `templates/handoff/{README,04_RECENT,02_METHODOLOGY,05_NOW}.md.tmpl`, `.claude/commands/handoff.md`, `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md` (LLM-LLM transfer rule), `BACKLOG.md` (closed v4-first-test; +2 P3 items; amended Council-ADR item), this JOURNAL entry. v4 architecture unchanged — template/spec polish only.
- Abandoned: nothing. Did NOT write an ADR (v4 + v4.2 ratify together via AI Council — operator standing pref). Did NOT advance Phase 2 of the re-test (requires operator-architect paste cycle). Did NOT touch the v4.1 first-run bundle (preserved as historical evidence). Did NOT add/remove templates or file types. No /review (docs/templates/skill; no safety-critical code).
- Next: operator does the copy-paste-architect back-and-forth on the generated `_handoff-interview.md` (four-tag answers), pastes below the marker, then `complete handoff for .dev-knowledge` → Phase 2 → v4.2 bundle at `docs/handoffs/2026-05-29-dev-knowledge-session-v4.2-rerun/`. Merge `fix/handoff-v4.2-refinements-and-rerun-2026-05-29` when satisfied.

---

### 2026-05-29 — Handoff v4 Phase 2: bundle consolidated (first post-fix real run complete)

- Did: Ran handoff Phase 2 (consolidate) for slug `2026-05-29-dev-knowledge-session` on branch `docs/handoff-2026-05-29`. Read the operator-pasted sage→apprentice answers, re-captured repo state, cross-checked load-bearing claims against repo/git, resolved all template markers from source (VISION/CLAUDE/PLAYBOOK/ESSENTIALS/BACKLOG/JOURNAL), generated the 8-file bundle (README + `01`–`07`) at `docs/handoffs/2026-05-29-dev-knowledge-session/`, and removed the consumed `in-progress/` interview folder (content folded into `04_RECENT.md`).
- Result: **Bundle complete; all 7 teaching files within line budgets (41/81/69/104/71/36/22 vs 100/200/150/250/100/80/50); no unresolved markers; no degradation (all sources present).** Two drifts surfaced in cross-check and recorded in `04_RECENT` + README: (1) the "aborted handoff folder" the sender said to preserve was in fact **deliberately deleted** (commit `987edac`) — surviving record is `docs/audits/2026-05-29-handoff-v3.4-process-audit.md`; (2) corp-monorepo P1-2 branch `chore/extract-p1-2-to-backlog-2026-05-28` is **still unmerged** (HEAD `a1007b1`) despite operator's belief it was merged — confirms BACKLOG CM-1, routed to corp-monorepo per ADR-41. This completes the **post-fix first real v4 test** (P3 BACKLOG) end-to-end (Phase 1 interview → operator answers → Phase 2 consolidation).
- Changes: `docs/handoffs/2026-05-29-dev-knowledge-session/` (8 new files), removed `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session/_handoff-interview.md`, this JOURNAL marker. Commit on `docs/handoff-2026-05-29`.
- Abandoned: nothing. NOTE: the operator's raw pasted interview answers were never committed (working-tree only by design); they are consumed/synthesized into `04_RECENT.md` and no longer on disk per the v4 consumption step.
- Next: operator uses the bundle per its `README.md` escalation ladder (paste 01–05 → 06 comprehension → 07 ask-back). Merge `docs/handoff-2026-05-29` → `main` once the bundle is approved. Candidate first-move for the apprentice: AI Council → ADR ratifying v4 (P2), preceded by the overdue LESSONS.md update.

---

### 2026-05-29 — Handoff v4 Phase 1: interview generated (first post-fix real run)

- Did: Ran the handoff skill (Phase 1) for `.dev-knowledge` self-handoff, slug `2026-05-29-dev-knowledge-session`, on branch `docs/handoff-2026-05-29` (off `main` tip `367c81e`). State detected = Fresh (no `in-progress/<slug>/_handoff-interview.md`). Generated the sage→apprentice single-cluster interview (Past/Present/Future/Wisdom/Warnings) per HANDOFF_PROCESS v4.1 §3.1 at `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session/_handoff-interview.md`. HEAD/branch/working-tree captured (clean tree).
- Result: Interview written; awaiting operator answers below the PASTE marker. This is the **post-fix first real v4 test** (P3 BACKLOG item) — the v4.1 sage-frame and `in-progress/` folder convention exercised end-to-end through Phase 1.
- Changes: `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session/_handoff-interview.md` (new), this JOURNAL marker. Commit on `docs/handoff-2026-05-29`.
- Abandoned: nothing.
- Next: operator copies the question block into the sender browser chat, pastes answers below the marker, saves, then says `complete handoff for .dev-knowledge` to trigger Phase 2 (consolidate → bundle at `docs/handoffs/2026-05-29-dev-knowledge-session/`).

---

### 2026-05-29 — Handoff v4 fix: sage-frame interview + in-progress/ folder

- Did: Fixed two design defects in the v4 implementation that surfaced on the first Phase 1 invocation, on branch `fix/handoff-v4-sage-interview-and-folder-2026-05-29` (off merged `main` tip `555d2f4`). (1) **Folder convention** — the original v4 prompt unilaterally introduced `docs/handoffs/_scratch/` for the interview file; reverted to the existing `docs/handoffs/in-progress/<slug>/` convention (standing operator pref: no new folders without approval). (2) **Interview frame** — Phase 1 had two clusters (project + methodology); the methodology cluster duplicated `PLAYBOOK`/`ESSENTIALS`, which the next chat reads independently. Redesigned as a single **sage→apprentice** cluster of 5 questions (Past / Present / Future / Wisdom / Warnings): theory lives in the books; the sage (sender chat) transmits only this project's lived implementation of that theory this session. Spec edits added §3.1 with the verbatim interview block; skill rewritten to generate it.
- Result: **Both defects closed; spec/skill aligned; baseline green.** `_scratch/` reduced to zero live references (two remain only in the spec's v4.1 section-history entry, describing the fix). Spec `protocols/HANDOFF_PROCESS.md` bumped to v4.1, held to 350 lines (≤350 budget — pruned the redundant ASCII flow diagram + verbose history/rationale prose to absorb the +70-line interview block). Skill 112 lines (≤200). Templates verified unchanged: `06_QUESTIONS.md.tmpl` is the receiver-side comprehension check (new chat → answers about 01–05), correctly distinct from the Phase 1 sender interview — no `_scratch/` anywhere in `templates/handoff/`. Note: the prior Phase 1 invocation left **no committed artifacts** (clean tree, no `_scratch/`, no JOURNAL marker) — Phase 1 "revert" was a no-op; only the fix branch was created.
- Changes: `protocols/HANDOFF_PROCESS.md` (v4.1 — §3.1 sage interview, `in-progress/` paths, version bump, prose pruning), `.claude/commands/handoff.md` (`in-progress/` paths + sage-frame Phase 1 generation), `BACKLOG.md` (re-homed "v4 first real test" → post-fix; new P3 metaphor-communication item; corrected stale `_scratch` ref in the audit check-#8 item), this JOURNAL entry. Commits `225c926` (spec), `5b5548b` (skill), + this docs commit on the fix branch.
- Abandoned: nothing. Did NOT codify metaphor-based methodology in PLAYBOOK/ESSENTIALS (captured as P3 BACKLOG, separate session per no-bundling); did NOT touch ADRs (architecture unchanged — this corrects an implementation defect, not a decision); templates left unedited (separate concern).
- Meta: third unilateral folder/structure decision in prompts violating standing prefs in ~24h (`docs/strategic/`, `_scratch/`, now fixed). Confirms the ML-2 ecosystem-audit finding (un-enforced guards) — the prompt-author convention is documented but not gated.
- Next: operator merges `fix/handoff-v4-sage-interview-and-folder-2026-05-29` to `main` (`git merge --no-ff`). The next handoff invocation then generates the interview at `docs/handoffs/in-progress/<slug>/_handoff-interview.md` with the sage-frame single cluster — the post-fix first real v4 test (P3 BACKLOG).

---

### 2026-05-29 — Handoff v4 implementation (radical simplification of v3.4)

- Did: Redesigned the handoff process from v3.4 to v4 on branch `feature/handoff-v4-redesign-2026-05-29` (off `main` tip `987edac`), per a frozen operator+browser-architect design discussion. v4 reframes a handoff as **onboarding a new chat — a teaching protocol, not a file transfer**: two phases (Phase 1 interview / Phase 2 consolidate) replace the three-stage flow; eight bundle files (README + `01`–`07`) **generated from source** replace v3.4's 13/14 hand-maintained files; an operator escalation ladder (Tier 1/2/3) replaces structured ratification; a content-based three-state machine replaces six-state file-existence detection. 6 phases, one commit each, `pytest`/`ruff`/`audit.py health` green after every commit. **No ADR authored** — v4 formalization is deferred to AI Council per standing operator preference.
- Result: **v4 live and structurally verified; 90 tests / audit 7/7 / ruff clean throughout.** Removed from v3.4: Stage vocabulary, placeholder-file dance, JSON manifest sidecar, gate-probe artifact, separate `11_CLAIMS.md`, `12_OPERATIONAL_*` layer, `00_first-message.md`. Kept: self-vs-cross-repo slug convention, feature-branch-per-handoff, ADR-41 cross-repo ownership respect, JOURNAL markers at each phase. v3.4 spec archived verbatim at `protocols/archive/HANDOFF_PROCESS_v3.4.md`. The v3.4 Q1–Q5 concepts are mapped into v4: claims → inline cross-checked narrative in `04_RECENT`; scope → `05_NOW` narrative; gate probe → receiver-side `06_QUESTIONS` comprehension check; Prompt Card → `02_METHODOLOGY`; manifest → README-declared structure; ratification → escalation ladder. New spec 218 lines (≤350), skill 96 lines (≤200), 8 templates all under per-file budgets.
- Changes: `protocols/HANDOFF_PROCESS.md` (rewritten v4), `protocols/archive/HANDOFF_PROCESS_v3.4.md` (archived via `git mv` + archive note), `templates/handoff/{README,01_ROLE,02_METHODOLOGY,03_PROJECT,04_RECENT,05_NOW,06_QUESTIONS,07_ASK_BACK}.md.tmpl` (new), `.claude/commands/handoff.md` (rewritten v4), `docs/decisions/ADR-42/45/55/56/57/58` (append-only v4-supersession amendments), `BACKLOG.md` (v3.4 mechanical-gate P2 → superseded; 3 new v4 follow-ups: Council→ADR P2, audit.py check #8 P3, first-real-test P3). Commits on `feature/handoff-v4-redesign-2026-05-29`.
- Abandoned: nothing. Single-purpose implementation — no observability hooks, eval stubs, or extra files beyond the agreed design. NOT done this session (by design): the v4 ADR (Council first), audit.py check #8 (separate enforcement session), and the first real v4 run (post-merge).
- Next: operator merges `feature/handoff-v4-redesign-2026-05-29` to `main` (`git merge --no-ff`). The next handoff invocation then uses v4; the first real v4 test is handing off THIS chat to the next Opus 4.8 session.

---

### 2026-05-29 — Overnight: ecosystem coherence audit (continuation of the v3.4 fix campaign)

- Did: After completing the v3.4 fix campaign (entry below), ran the operator's queued overnight continuation — a read-only ecosystem coherence audit across 7 dimensions (skills, hooks, workflows, goals, corp-monorepo cross-repo, cross-doc harmony, memory/feedback) on branch `docs/ecosystem-coherence-audit-2026-05-29` (off the fix-campaign tip). 7 scratch reports (`docs/audits/scratch/2026-05-29-ecosystem-*.md`), one consolidated report (`docs/audits/2026-05-29-ecosystem-coherence-audit.md`), BACKLOG entries, and the headline deliverable `docs/audits/2026-05-29-overnight-morning-briefing.md`. Strictly read-only outside `.dev-knowledge` (ADR-41) — corp-monorepo inspected via status/log/CLAUDE-head/test-collect, never modified.
- Result: **22 findings (0 critical, 0 high, 12 medium, 10 low); ecosystem health green** (90 tests, audit.py 7/7, ruff clean, corp-monorepo 2554 tests collectable, clean trees). Two dominant patterns: (1) **documentation-truth drift** — CLAUDE.md + ARCHITECTURE describe their own commands/skills/handoff-version/governing-ADRs inaccurately, and name a non-existent `scripts/backlog_extract.py` + a non-existent `TOKEN-LOG.md` as canonical (12 of 22 findings, none breaking); (2) **un-enforced guards** — ML-2: LESSON #9's cross-case-trace guard was advisory prose, not a gate, which is the root cause of the v3.4 abort the fix campaign just remediated. The abort is not yet promoted to a LESSON (ML-3). corp-monorepo's P1-2 security-finding extraction sits on an unmerged branch (CM-1). Findings grouped into a recommended fix sequence (doc-truth sweep / feedback-loop enforcement / evolution-logs+hooks / corp-monorepo merge / low cleanups).
- Changes: `docs/audits/scratch/2026-05-29-ecosystem-{skills,hooks,workflows,goals,corp-monorepo-coherence,cross-doc-harmony,memory-feedback}.md` (new), `docs/audits/2026-05-29-ecosystem-coherence-audit.md` (new), `docs/audits/2026-05-29-overnight-morning-briefing.md` (new), `BACKLOG.md` (6 ecosystem-audit entries + existing Hooks-audit P2 marked audit-done + a stray duplicate-status line from the fix-campaign closure removed). Commits `07f0be6` → this entry (~11 on the audit branch).
- Abandoned: nothing. Diagnose-only — every finding routed to BACKLOG; fixes are separate focused sessions per the continuation's "no big-bang" rule.
- Next: operator merges both branches (`fix/handoff-v3.4-complete-campaign-2026-05-29` first, then `docs/ecosystem-coherence-audit-2026-05-29`). Morning briefing §4 has the exact merge commands + the 7-item next-session sequence. Top follow-up: the doc-truth sweep (Sonnet, fast) + feedback-loop enforcement (Opus — guard→gate, the structural win).

---

### 2026-05-29 — Handoff v3.4 fix campaign (Path C, all 13 findings) — retry-ready

- Did: Executed the complete remediation of all 13 findings from the 2026-05-29 v3.4 process-audit post-mortem, sequentially in the audit's recommended fix order, on branch `fix/handoff-v3.4-complete-campaign-2026-05-29` (off `main` tip `2327e27`). 8 phases, one commit per phase group, `pytest`/`ruff`/`audit.py health` after each. ADR-39 immutability respected throughout — ADR-42/45/55/56/57/58 corrected by **appended amendments only**, never in-place body edits; spec/skill/templates direct-edited.
- Result: **13/13 closed; hard-metric simulation PASS; handoff process retry-ready.** Phase 1 rebuilt the Stage 1 template so the architect is now asked — inside the architect-facing paste block — for `next_session_scope` (ADR-57 vocab inline), `11_CLAIMS.md` content (ADR-58 schema inline), and gate-probe accuracy review (ADR-55), plus an audience-routing invariant forbidding required artifacts from living only in operator-facing Section A (B1+B2+E3). Phase 2 rewrote the skill to v3.4 with content-aware state detection + M-5/ancestry/claims/UNVERIFIED gates (A1+A2). Phase 3 brought the spec's folder-structure + file-responsibilities sections to include 10/11/12, reconciled the count to **13 fixed content files (self) / 14 (cross-repo)** + json sidecar + conditional operational layer, and appended the ADR-42 Q5 file-count addendum (F1+F2+D2). Phases 4–7 closed D1 (folder-template version normalization), E1 (evidence-file repoint to `docs/archive/` + 4 ADR amendments), F3 (synthesis prompt canonical = `00_first-message.md`), F4 (`{date}-{slug}`→`{slug}`), E2 (ADR-45 authority pointer). Phase 8 verified: zero v3.3.3 live stragglers, count consistent across all live surfaces, zero live stale evidence paths; hard-metric simulation of a fresh Stage 1 generation confirmed all three v3.4 outputs are requested in Section B.
- Changes: `templates/HANDOFF_QUESTION_TEMPLATE.md`, `.claude/commands/handoff.md`, `protocols/HANDOFF_PROCESS.md`, `templates/HANDOFF_FOLDER_TEMPLATE.md`, `docs/decisions/ADR-42/45/55/56/57/58` (append-only amendments), `BACKLOG.md` (7 entries closed), `docs/audits/2026-05-29-handoff-v3.4-fix-campaign-verification.md` (new). Commits `b4afff3` → `7e4bd33` (10 commits).
- Abandoned: nothing — Path C closed all 13; no finding deferred. The 5 Council transcript evidence-path refs were deliberately left unchanged (immutable; annotating undermines their semantics) — a closed decision, not an open item.
- Next: operator merges `fix/handoff-v3.4-complete-campaign-2026-05-29` to `main` (`git merge --no-ff`); a v3.4 handoff retry can then be initiated in a new session. (Overnight continuation — ecosystem coherence audit — runs on a separate branch off this tip; see its own JOURNAL entry / morning briefing.)

---

### 2026-05-29 — Handoff v3.4 test ABORTED at Stage 3 + process audit post-mortem

- Did: Halted the in-flight `2026-05-29-dev-knowledge-session-sync` handoff (first real HANDOFF_PROCESS v3.4 run) at Stage 3 readiness on operator scrum-master review. Committed the architect's populated `stage2-response.md` verbatim as abort evidence (`cf9edb7`), renamed `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session-sync/` → `docs/handoffs/aborted/2026-05-29-dev-knowledge-session-sync-ABORTED/` + added `ABORT_NOTE.md` (`2372d29`). Then ran an empirical full-read audit of the v3.4 process across 6 dimensions (spec ↔ skill, Stage 1 ↔ Stage 3 requirements, operator-facing vs architect-facing, ADR cross-consistency, version/path refs, spec-internal) — read `HANDOFF_PROCESS.md`, both handoff templates, the generated stage1/stage2 artifacts, and ADR-42/45/55/56/57/58 in full. Wrote `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` (`dcb1436`) and 7 BACKLOG entries tagged `handoff-v3.4-audit-2026-05-29` (`59aaf0c`).
- Result: **13 findings (2 critical, 4 high, 6 medium, 1 low) — above the browser review's 4–6 floor.** Root cause: the v3.4 "Phase C" amendment updated the Stage 3 folder template + the spec but left `HANDOFF_QUESTION_TEMPLATE.md` (Stage 1) and `.claude/commands/handoff.md` (skill) at v3.3.3 — so the architect was never asked for `next_session_scope` or `11_CLAIMS.md`, and indeed produced neither (only the 5 pipeline sections). Classic `universal-without-cross-case-verification` (LESSON #9) — the cross-stage trace v3.3.2 was meant to mandate was not run. Secondary cluster: broken evidence-file citations (9 refs, all wrong — file is at `docs/archive/`, cited as `docs/research/` ×8 + `docs/council-questions/` ×1; ironic for ADR-58, the citation-verification decision); spec-internal file-inventory/count drift (11/12/13/14 stated four ways; reference sections stop at file 09); folder-template internal version drift (v3.3.3 / v3.2 / v3.4 in one file).
- Changes: `docs/handoffs/aborted/2026-05-29-dev-knowledge-session-sync-ABORTED/` (renamed from in-progress, + `ABORT_NOTE.md`); `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` (new); `BACKLOG.md` (7 entries); this JOURNAL entry. **No process files edited** — diagnose-and-abort only; HANDOFF_PROCESS.md, the templates, the skill, the ADRs, and stage1-question.md were left untouched per the prompt.
- Abandoned: the handoff itself — not retried. Retry is gated on the two P1 fixes (Stage 1 template + skill to v3.4). The architect's Stage 2 answers were sound and are preserved; the failure was process plumbing, not the architect.
- Meta: N+1 grounding for the P1 "Codify scrum-master review authority pattern" item — the operator's independent review caught a plausible-but-unverifiable chat-mode Stage 2 narrative that only a file:line ground-truth read exposed. (The aborted Stage 2 itself nominated that same codification as the next session's top goal.)
- Next: operator merges `docs/handoff-2026-05-29-session-sync` to `main` (`git merge --no-ff`) — one branch covering attempt + abort + diagnosis. Then schedule the P1 fixes (Stage 1 question template → v3.4; handoff skill → v3.4) as separate focused sessions before any v3.4 handoff retry; P2/P3 doc-consistency fixes follow per the post-mortem's recommended fix order.

---

### 2026-05-29 — Handoff Stage 1 generated (session-sync)

- Did: Generated handoff Stage 1 for slug `2026-05-29-dev-knowledge-session-sync` (self-handoff, HANDOFF_PROCESS v3.4). Captured HEAD `5582cf544fab2b4236e7d292d5506ce85ad63c55`, branch `main`, clean tree. Wrote `stage1-question.md` (5-question pipeline + epistemic/self-containment/coherence/format guidance, current-state summary of the 2026-05-28 universalization arc, relevant own-repo BACKLOG items) and pre-created `stage2-response.md` placeholder.
- Result: Awaiting Stage 2 — architect response from OLD browser chat. Work on branch `docs/handoff-2026-05-29-session-sync`.
- Changes: `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session-sync/stage1-question.md` (new); `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session-sync/stage2-response.md` (new placeholder); this JOURNAL entry.
- Abandoned: nothing.
- Next: Rob pastes the PASTE_BOUNDARY block into the OLD `.dev-knowledge` chat, replaces the placeholder in `stage2-response.md` with the architect response (+ `stage2-claims.md` + `next_session_scope`), then says "complete handoff for dev-knowledge" → Stage 3.

---

### 2026-05-28 — Universalization durability + template-completeness audit (pre-handoff)

- Did: Read-only audit verifying that today's universalization (ADR-59 visual pattern + ADR-60 taxonomy + 2026-05-28 addendum + ADR-51 v2 mermaid theme + ADR-61 worktree + AI_COUNCIL_PROCESS runbook + handoff v3.4 + process diagrams C1-C4 + audit check #7 + baseline-folder uniformity) is encoded in template / PLAYBOOK / ESSENTIALS / ADRs / `audit.py` — DURABLE — versus only applied to current state. Produced `docs/audits/2026-05-28-universalization-durability-audit.md` (per-convention durability table + three durability questions + corp-monorepo P1 findings capture analysis + clear/judgment gap list). Three clear gaps closed in additive cross-ref commits (C1: PLAYBOOK §Codemap workflow gets mermaid-theme-directive paragraph; C2: ESSENTIALS gets `## Mermaid theme (ADR-51 v2)` cheat section; C3: `CLAUDE.md` §11 ADR-list rotated 49–53 → 57–61 per the file's own "last 5" header; bumped to v2.3). Four judgment gaps appended to BACKLOG: J1 CLAUDE-md-template refresh [P2], J4 audit.py mermaid scope widening [P3], J5 child-repo audit reach [P3], J6 new-repo scaffolding starter pack [P3]. J2 (workspace templates) + J3 (folder-semantics audit check) were already captured in existing BACKLOG entries — not duplicated. Corp-monorepo branch-deletion gate: HOLD — P1-1/P1-3 (OneDrive) covered by multi-layer enforcement (global hook + global CLAUDE.md rule + `_guard_onedrive()` + corp ADR-27); P2 (vault single-writer) covered by corp ADR-27 Decision 2 + CI test; **P1-2 (path traversal in `cleanup/executor.py:68/85`) NOT captured in main** — analysis exists only on `verify/codex-p1-findings`. Operator must extract to corp-monorepo BACKLOG before `git branch -D`.
- Result: 7 of 11 conventions fully DURABLE; 3 of 11 PARTIAL (mermaid theme — closed here in C1/C2; template scaffolding — flagged J1; child-repo audit reach — flagged J5); 0 of 11 ONLY-APPLIED. 90/90 tests pass + ruff clean + `audit.py health` 7/7 after every commit. Branch `docs/universalization-durability-audit-2026-05-28` 5 commits (audit report + C1 + C2 + C3 + this entry/BACKLOG); awaiting operator merge.
- Architectural contract: zero ai-council writes; corp-monorepo touched only as a one-file read-only inspection from `verify/codex-p1-findings` (restored clean immediately after); Layer-2 invariant intact (no scripts added; only governance docs + audit report). Three clear-gap commits each <10 lines of additive content (no restructuring); BACKLOG additions appended (no rewrites). All commits passed pre-commit hooks. Per the prompt: NO new template authored; NO conventions invented; NO branches deleted.
- Changes: `docs/audits/2026-05-28-universalization-durability-audit.md` (new); `protocols/PLAYBOOK.md` (one paragraph under §Codemap workflow); `protocols/ESSENTIALS.md` (one section between §Repo visual pattern and §docs/ taxonomy); `CLAUDE.md` (§11 ADR list rotation + §12 v2.3 history line); `BACKLOG.md` (4 new entries — J1 P2 + J4/J5/J6 P3, appended before existing corp-sca entry under "Council Pipeline + Consolidation Follow-ups (2026-05-26 session)"); this JOURNAL entry.
- Abandoned: nothing scoped was deferred. The audit prompt explicitly forbade authoring new templates / scaffolding tools / conventions — those land as J1/J6 BACKLOG entries for operator decision.
- Next: operator merges `docs/universalization-durability-audit-2026-05-28` to `main` (`git merge --no-ff`). Then the corp-monorepo branch-deletion gate: operator extracts P1-2 path-traversal analysis to corp-monorepo `BACKLOG.md` (text supplied in the audit report's "Branch deletion gate" section), THEN runs `git branch -D verify/codex-p1-findings feature/dead-code-audit` in corp-monorepo. Pending handoff per the prior queue.

---

### 2026-05-28 — audit.py check #7: Mermaid theme directive enforcement (BACKLOG P3 closed)

- Did: Added `check_mermaid_theme_directive` as check #7 to `scripts/audit.py`. Enforces ADR-51 v2 standard: (1) every Mermaid block in scanned files must begin with `'theme':'base'` + `themeVariables` directive; (2) every `classDef` with `fill:#` must also carry `color:#`. Scans `ARCHITECTURE.md` + `templates/ARCHITECTURE-template.md`; excludes `docs/audits/`, `docs/decisions/ADR-*`, `JOURNAL.md`, `docs/archive/` (immutable dated artifacts per ADR-39). Added 2 fixtures (mermaid-theme-pass, mermaid-theme-fail) and 5 unit tests. ADR-51 appended with enforcement note. BACKLOG P3 closed.
- Result: `audit health` now reports 7/7 pass against `.dev-knowledge`. 90/90 tests pass. ruff clean. Branch `feat/audit-mermaid-theme-check-2026-05-28` awaiting operator merge.
- Changes: `scripts/audit.py` (check #7 + ALL_CHECKS registration); `tests/test_audit.py` (5 new tests); `tests/fixtures/mermaid-theme-pass/ARCHITECTURE.md` (new); `tests/fixtures/mermaid-theme-fail/ARCHITECTURE.md` (new); `docs/decisions/ADR-51-architecture-doc-convention.md` (enforcement note appended); `BACKLOG.md` (P3 closed).
- Abandoned: nothing.
- Next: operator merges branch with `git checkout main && git merge --no-ff feat/audit-mermaid-theme-check-2026-05-28`.

---

### 2026-05-28 — Mermaid readability v2 (root-cause diagnosis + custom-theme rollout)

- Did: Diagnosed why the 2026-05-28 v1 dark-theme fix only worked for the layer-model block. Root cause: bare `%%{init:{'theme':'dark'}}%%` flips default text color toward light; classDefs that set light-pastel `fill:` but omitted `color:` inherited that light default → light-on-light = unreadable. Layer model worked because its classDefs already pinned `color:#000`/`#222`. Replaced the directive ecosystem-wide with a custom `'theme':'base'` + `themeVariables` block and added explicit `color:#000`/`#222` to every classDef with a light-pastel fill across .dev-knowledge ARCHITECTURE.md (3 process diagrams), ai-council, corp-ops, corp-monorepo, the codemap generator's `_ALL_CLASS_DEFS`, the test fixture, and the ARCHITECTURE template. ADR-51 amended (v2 amendment 2026-05-28) supersedes the v1 bare-`'dark'` standard. Verification doc + BACKLOG updates landed; render-verification P3 closed (operator-confirmed); audit.py-check P3 retargeted to the v2 directive + companion `color:` rule.
- Result: 12 Mermaid blocks across 4 repos now carry the custom themeVariables directive + color-pinned classDefs. 85/85 tests pass in .dev-knowledge; ruff clean; `scripts/audit.py health` green; codemap-freshness pre-commit hook passes; corp-ops/ai-council pre-commits clean; corp-monorepo hooks skipped (no Python touched). Four branches `fix/mermaid-readability-v2-2026-05-28` (.dev-knowledge: 3 commits; ai-council/corp-ops/corp-monorepo: 1 commit each) awaiting operator merge.
- Changes: `scripts/codemap/mermaid_emit.py` (new `_THEME_DIRECTIVE`; `_ALL_CLASS_DEFS` gains `,color:#...`); `ARCHITECTURE.md` (6 directives swapped, workflow/council/handoff classDefs gain `color:`); `tests/fixtures/codemap-arch-clean/ARCHITECTURE.md` (refresh); `templates/ARCHITECTURE-template.md`; `docs/decisions/ADR-51-architecture-doc-convention.md` (Amendment 2026-05-28 v2 appended); `docs/audits/2026-05-28-mermaid-readability-v2-verification.md` (new); ai-council/corp-ops/corp-monorepo `ARCHITECTURE.md` (in-file); BACKLOG (one P3 closed, one P3 retargeted).
- Abandoned: nothing. The prompt's literal "change `color:#000`→`color:#f0f0f0`" recipe was rejected after diagnosis (would have inverted the already-working layer model); operator confirmed before applying the inverted-from-prompt fix.
- Next: operator opens each `ARCHITECTURE.md` on black background and confirms all diagrams (not just the layer model) now render readably. If green: merge all four branches with `git merge --no-ff`. P3 `audit.py` Mermaid check remains a future tightening.

---

### 2026-05-28 — archive/ first triage (ADR-60 periodic review)

- Did: First periodic review of `docs/archive/` (14 files accumulated from 2026-05-27 taxonomy simplification). Read all 14; classified per ADR-60 rubric. Promoted 7 AI Council debate transcripts (full `# AI Council Debate:` format) to `docs/decisions/transcripts/` — same structure as existing council-out-* files there. Kept 7 pending: 4 external research reports (Perplexity/Gemini outputs), 1 scoping note (Kimi K2, BACKLOG #243), 2 handoff-methodology artifacts (failures evidence + question index) that remain active references in ADR-55–58 and HANDOFF_PROCESS.md. No delete-candidates: all kept files have active references or pending BACKLOG items. No ADR candidates flagged; no files deleted.
- Result: `docs/archive/` reduced from 14 to 7 classification items. Pre-commit clean; branch `chore/archive-first-triage-2026-05-28` awaiting operator merge.
- Changes: 7 files `docs/archive/ → docs/decisions/transcripts/`; `docs/archive/README.md` updated (first-review marker, promoted list, revised current-contents).
- Abandoned: nothing.
- Next: operator merges branch. Second review of remaining 7 (due after one more review pass per ADR-60); at that point: external research reports likely DELETE-CANDIDATES if content absorbed; kimi-k2-scoping resolved when BACKLOG #243 executes.

---

### 2026-05-28 — AI Council operational runbook (protocols/AI_COUNCIL_PROCESS.md v1.0)

- Did: Authored `protocols/AI_COUNCIL_PROCESS.md` v1.0 — the prose end-to-end operational runbook for the AI Council pipeline, companion to the ARCHITECTURE.md C3 "AI Council debate pipeline" Mermaid diagram landed earlier today. Six stages (frame → author → route → debate → verdict → ADR → close), each with owner, gate check, code grounding (cli.py, inbox.py, routing.py, runner.py, orchestrator.py, synthesis.py + council-question-guide.md). Includes frontmatter reference table, exit-code convention (ADR-08), routing rules (ADR-43), troubleshooting matrix, cross-references. Cross-linked from PLAYBOOK § 5 lead-in, ESSENTIALS § "Artifact generation direction" (Council ADR distillation paragraph), and the ARCHITECTURE.md C3 diagram source block. Closed **BACKLOG #4** (P2 "AI Council Flow operationalization — lifecycle runbook") — both halves of the 2026-05-25 pipeline proposal Option B (visual + prose) now landed.
- Result: Council pipeline has a single operational home; operator no longer re-derives the flow each time. 85/85 tests pass; ruff clean; pre-commit hooks pass; codemap check passes. Branch `docs/ai-council-runbook-2026-05-28` (3 commits: runbook + cross-links + BACKLOG close) awaiting operator merge.
- Changes: `protocols/AI_COUNCIL_PROCESS.md` (new, 343 lines), `protocols/PLAYBOOK.md` (§5 lead-in pointer), `protocols/ESSENTIALS.md` (Council ADR distillation pointer), `ARCHITECTURE.md` (C3 diagram source block pointer), `BACKLOG.md` (P2 entry closed).
- Abandoned: nothing.
- Next: operator merges `docs/ai-council-runbook-2026-05-28` to `main`. JOURNAL entry will land with the merge.

---

### 2026-05-28 — Git worktree pattern codification (ADR-61)

- Did: Codified the git worktree pattern for parallel Claude Code sessions as **ADR-61** (`docs/decisions/ADR-61-git-worktree-parallel-sessions.md`). Added `### Parallel sessions` subsection to PLAYBOOK `## Session boundaries` (v1.1). Added `## Parallel sessions` cheat-sheet section to ESSENTIALS. Added ADR-61 to `docs/decisions/README.md` index. Closed **BACKLOG #5** [P1].
- Result: Pattern fully documented. Distinction codified: different-repo parallel = safe (separate `.git/`); same-repo parallel = `git worktree add` required. Setup/cleanup commands, naming convention (`<repo>-parallel` / `<repo>-wt-<purpose>`), and pre-flight check (`git worktree list`) documented in three locations. 85/85 tests pass; all pre-commit hooks pass. Branch `docs/git-worktree-pattern-2026-05-28` awaiting operator merge.
- Changes: `docs/decisions/ADR-61-git-worktree-parallel-sessions.md` (new); `protocols/PLAYBOOK.md` (§Session boundaries parallel-sessions subsection); `protocols/ESSENTIALS.md` (new section); `docs/decisions/README.md` (ADR-61 index row); `BACKLOG.md` (#5 closed).
- Abandoned: nothing — scope delivered exactly.
- Next: operator merges branch with `git merge --no-ff docs/git-worktree-pattern-2026-05-28`.

---

### 2026-05-28 — Mermaid dark-theme standard — cross-repo fix + codify

- Did: Made every Mermaid diagram readable on Rob's black VS Code background by prepending `%%{init: {'theme':'dark'}}%%` as the first line inside every Mermaid fence across the ecosystem. **Phase A (.dev-knowledge, branch `fix/mermaid-dark-theme-2026-05-28`):** updated `scripts/codemap/mermaid_emit.py` to emit the directive automatically; updated the matching `tests/fixtures/codemap-arch-clean/ARCHITECTURE.md` fixture so `test_check_clean` still passes; regenerated `ARCHITECTURE.md` codemap block via `py -m scripts.codemap.cli generate . --source-root scripts --write`; added directive to the 5 hand-authored Mermaid blocks in `ARCHITECTURE.md` (layer model + 4 process diagrams); added directive to the canonical codemap example in `templates/ARCHITECTURE-template.md`; appended **ADR-51 Amendment 2026-05-28** codifying the standard, naming immutable dated artifacts (audits/transcripts/ADRs per ADR-39) as out-of-scope for retrofit, and documenting the custom-base `themeVariables` variant as a per-block escape hatch. **Phase B (child repos):** discovered that ai-council / corp-ops / corp-monorepo CODEMAP blocks are hand-authored (trailer comment "not generator-managed") — running the generator there would replace rich curated graphs with an orphan-only single-node graph because the AST walker doesn't find the expected imports for those source layouts. Reverted the regen attempts; added the directive in-place to both Mermaid blocks in each child repo's `ARCHITECTURE.md`. corp-sca has no Mermaid blocks — no change. **Phase C:** wrote `docs/audits/2026-05-28-mermaid-dark-theme-verification.md` (per-repo counts, generator change, audit-check deferral rationale, branches awaiting merge, operator visual-confirmation reminder); added BACKLOG P3 entry for the deferred `audit.py check_mermaid_theme_directive` check (held back pending an exclusion list for immutable-artifact paths).
- Result: 12 Mermaid blocks across 4 repos; 12 directives — counts match (`grep -c "theme':'dark'"` vs `grep -c '\`\`\`mermaid'`). 85/85 tests pass on `.dev-knowledge`. Pre-commit (normalize-dated-headers + codemap-freshness) passes on every commit. Working trees clean on all branches. 4 commits on `.dev-knowledge` `fix/mermaid-dark-theme-2026-05-28`; 1 commit each on ai-council, corp-ops, corp-monorepo `fix/mermaid-dark-theme-2026-05-28`. None pushed; awaiting operator merge per repo.
- Changes: `.dev-knowledge` — `scripts/codemap/mermaid_emit.py` (emit directive); `tests/fixtures/codemap-arch-clean/ARCHITECTURE.md` (fixture match); `ARCHITECTURE.md` (codemap regen + 5 hand-edits); `templates/ARCHITECTURE-template.md` (directive in canonical example); `docs/decisions/ADR-51-architecture-doc-convention.md` (Amendment 2026-05-28); `docs/audits/2026-05-28-mermaid-dark-theme-verification.md` (new); `BACKLOG.md` (new P3 entry for deferred audit check). Child repos: 1 `ARCHITECTURE.md` edit each in ai-council / corp-ops / corp-monorepo.
- Abandoned: (1) Generator-based regen for ai-council / corp-ops / corp-monorepo — the CODEMAP blocks are explicitly hand-authored ("not generator-managed" trailer). Generator regen would have destroyed the curated layered graphs. Reverted; added directive in-place. (2) `audit.py` mechanical check — deferred to BACKLOG (needs exclusion list for immutable-artifact paths before it can be merged without false positives). (3) Retrofit of Mermaid blocks embedded in immutable audit/decision artifacts — per ADR-39 they are point-in-time records; new ones going forward should include the directive.
- Next: Operator visual-confirms each `ARCHITECTURE.md` in VS Code on black background. If `'theme':'dark'` proves insufficient on any block, switch that block (or the standard) to the custom-base `themeVariables` variant documented in the ADR-51 amendment. Operator merges all 4 feature branches with `git merge --no-ff` per repo.

### 2026-05-28 — final-state verification + child-repo baseline uniformity + process-diagrams

- Did: Single autonomous session anchored in `.dev-knowledge`, three outcomes. **Phase A:** read-only final-state verification of all 5 repos against ADR-60 variants (table in `docs/audits/2026-05-28-final-state-and-process-diagrams-verification.md`). 3/5 already conformant from the taxonomy work merged to `main`; corp-ops and corp-sca were on minimalist `archive/`-only state. **Phase B:** brought corp-ops + corp-sca to the full child-repo baseline (`decisions/` + `audits/` + `archive/`, each README-seeded) on branch `chore/baseline-template-2026-05-28` in each repo (one commit each). Codified the operator's uniformity-over-minimalism decision as an **ADR-60 addendum 2026-05-28** (append-only, original 2026-05-27 amendment text preserved) on `.dev-knowledge` branch `docs/process-diagrams-and-baseline-2026-05-28`. ai-council + corp-monorepo verified no-op. **Phase C:** replaced the stale `## Diagrams` section in `ARCHITECTURE.md` ("no Mermaid diagrams currently") with a `## Processes` section housing 4 grounded Mermaid diagrams — (C1) Ecosystem layer model extended (methodology + `~/.claude` + child repos + Obsidian vault), (C2) Development workflow (complexity routing → execute → operator merge → capture → handoff loop), (C3) AI Council pipeline (council_inbox → cli --inbox → 5-provider debate → blind vote → synthesizer → ADR-43 routing → ADR), (C4) Handoff process v3.4 (Stage 1/2/3 + applied-task gate + structured ratification). Each diagram carries a prose preamble + `**Source:**` line citing the implementation doc(s) it was derived from. Reality-vs-sketch correction: the AI Council pipeline diagram follows the **ephemeral** `council_inbox/` + `~/Downloads/` brief flow per ADR-60 amendment, not the retired committed-`council-questions/` sketch. **Phase D:** verification report + BACKLOG (annotation on the open "AI Council Flow operationalization" entry pointing at the new diagram + 2 new P3 entries: `PROCESS.md` split candidate, Mermaid render verification protocol) + this entry.
- Result: 6 mermaid blocks in `ARCHITECTURE.md` (1 codemap + 1 static layer model + 4 new process) verified by grep; `ARCHITECTURE.md` 175 → 405 lines. 5 commits on `.dev-knowledge` feature branch (ADR-60 addendum, process diagrams, verification report, BACKLOG, this JOURNAL); 1 commit each on corp-ops + corp-sca feature branches. Pre-commit hooks (normalize-dated-headers + codemap-freshness) pass on every commit. Working tree clean.
- Decision / scope notes: operator override 2026-05-28 — child-repo baseline always-present (README-seeded) supersedes the ADR-60 amendment's "added on first need" line **for the baseline folders only**; `diagrams/` remains optional. Sketch-vs-reality correction in diagram C3: the prior browser sketch of a committed `docs/council-questions/` Council-inputs folder was rendered obsolete by the 2026-05-27 ADR-60 amendment that retired `council-questions/`; reality is ephemeral inputs (`council_inbox/` gitignored, `~/Downloads/` with Council marker), permanent records are transcript + ADR. The diagram follows reality. The `## Diagrams` section's old "no Mermaid diagrams currently" claim was already stale (the layer-model Mermaid existed in `## Layer Boundaries`) — replaced, not preserved.
- Changes: `docs/decisions/ADR-60-docs-folder-taxonomy.md` (Addendum 2026-05-28 appended); `ARCHITECTURE.md` (replaced `## Diagrams` with `## Processes` + 4 diagrams + sources); `docs/audits/2026-05-28-final-state-and-process-diagrams-verification.md` (new); `BACKLOG.md` (annotated AI Council Flow entry; 2 new P3 entries — PROCESS.md split candidate + Mermaid render verification); this entry. Plus child-repo seeding: `corp-ops/docs/{decisions,audits}/README.md` (new) on branch `chore/baseline-template-2026-05-28`; same for `corp-sca-time-automation`. All three branches unmerged, unpushed — awaiting operator merge approval (`git merge --no-ff main` in each repo).
- Architectural contract: zero `.dev-knowledge` orchestration (Layer 2 invariant intact — no script drove the child-repo writes; they were authored locally on branches in each repo via explicit `git -C` + bounded `cd`). ADR-60 *appended* via addendum, not rewritten (immutability respected per Rule 5 of ADR-60 itself). No new deps; no tool config touched; no hook altered; no push; no auto-merge.
- Abandoned: none.
- Next: operator merges three branches in this order — corp-ops `chore/baseline-template-2026-05-28` → corp-sca-time-automation `chore/baseline-template-2026-05-28` → `.dev-knowledge` `docs/process-diagrams-and-baseline-2026-05-28` (all `git merge --no-ff`). After merge, the Mermaid render-verification check (new P3) should be applied retroactively to the 4 diagrams as a one-time visual pass — confirms each renders as intended in VS Code. Then the queued work resumes per the prior entry: 4× child-repo ADR-59 retrofits (now P1 git-worktree pattern applies), the ai-council universalization execution plan (P1), the AI Council Flow runbook prose (P2 — visual half now done), the first real handoff under process v3.4.

---

### 2026-05-28 — .dev-knowledge consolidation (sort fix + BACKLOG truth-up)

- Did: Single short consolidation session on branch `chore/dev-knowledge-consolidation-2026-05-27` off `main` (4 commits). Phase B: investigated the operator-reported sorting regression ("dated content now sorts oldest-first; before it was newest-first") empirically rather than trusting the 2026-05-27 visual-pattern session's "sortOrderReverse is not a real VS Code setting" claim. Verified against microsoft/vscode PR #149952 — the setting WAS implemented and merged 2024-07-30 (insiders-released, verified); the prior session's conclusion was wrong. Restored `explorer.sortOrderReverse: true` alongside `lexicographic: upper` in the workspace. Phase B (cont.): amended ADR-59 with a 2026-05-27 correction section (append-only per immutability convention) documenting the false-premise rejection + the corrected decision + the verification lesson; updated the one PLAYBOOK reference that carried the false claim. Phase C: scanned for empty/unnecessary files — all 0-byte files are intentional `__init__.py` package markers in test fixtures + one negative-case `ARCHITECTURE.md` test fixture; no `.env` files in tree; nothing to delete. Phase D: BACKLOG truth-up — closed the "Draft ADRs from 5 transcripts" P1 (implemented as ADRs 55-58 + ADR-42 amendment in the 2026-05-26 handoff-stabilization session, already on `main`) + closed the "📋 ADRs alias removal" P3 (superseded by commit `f5322837` that removed all dated-folder aliases); escalated the git worktree pattern entry P2 → P1 citing the 2026-05-27 visual-pattern session's misplaced-branch incident as second evidence; added 4 new entries — ADR-59 child-repo retrofits (sub-itemed per repo with dependencies, e.g., corp-monorepo blocked on ruff-strictness), AI Council Flow operationalization (the remaining Option B piece), audit-tool folder-semantics check (ADR-60 candidate), and a sort-regression verification protocol (PR + visual check before workspace-setting commits). Phase E: this entry. Phase F: full verification.
- Result: sorting regression fixed; ADR-59 corrected via amendment (original body untouched per immutability); PLAYBOOK reference updated; BACKLOG accurately reflects 2026-05-26/27 work (2 closures, 1 escalation, 4 new entries). 85 tests green + ruff clean + `audit.py health` 6/6 after every commit; workspace JSONC validated; tree clean. No `.env` deletions, no content-bearing deletions.
- Verification correction: the originating session's removal of `sortOrderReverse` was based on the issue page (#149951, titled "would like to reverse the file order" — read as ask) without following through to the linked PR (#149952) which shows the implementation merged. The corrected decision keeps BOTH the lexicographic-upper visual-pattern setting AND the reverse setting (they compose — visual pattern + dated newest-first). New BACKLOG P3 captures the verification rule (PR + visual editor check) so this class of misverification has a documented guard.
- Changes: `.dev-knowledge.code-workspace` (restore `sortOrderReverse: true` + corrected comment); `docs/decisions/ADR-59-universal-visual-repository-pattern.md` (append 2026-05-27 amendment); `protocols/PLAYBOOK.md` (one-line truth-up of the §"Date-sorted folders" reference); `BACKLOG.md` (#1 close, #10 close, #5 escalate, +4 new entries — ADR-59 retrofits / AI Council Flow runbook / folder-semantics check / sort-regression verification protocol); this entry. Branch unmerged, unpushed — awaiting operator merge approval.
- Architectural contract: zero child-repo writes (read-only audit/plans only); zero ai-council writes; Layer-2 invariant intact (no scripts added); ADR immutability respected (amendment, not rewrite); the 4 ADR-59 child-repo retrofit plans remain queued in `docs/audits/` for separate per-repo sessions.
- Abandoned: none.
- Next: operator merges `chore/dev-knowledge-consolidation-2026-05-27` to `main` (`git merge --no-ff`). Then the previously-queued work resumes: 4× child-repo visual-pattern retrofits (separate sessions, worktree pattern — now P1), the ai-council universalization execution plan (P1), the AI Council Flow runbook (P2 new), and the first real handoff under process v3.4. The git-worktree codification (P1, escalated) is the highest-value process change — every concurrent session until then risks another misplaced-branch incident.

---

### 2026-05-27 — docs/ folder taxonomy implementation (ADR-60)

- Did: Implemented the docs/ folder taxonomy (Option B of the 2026-05-25 pipeline proposal) on branch `docs/folder-taxonomy-implementation-2026-05-27` off `main` (~13 commits, one revertable unit each). **Pre-session:** found the Universal Visual Pattern work (ADR-59) sitting *unmerged* on `docs/universal-visual-pattern-codification-2026-05-27` with a second concurrent CC session committing to it (5 commits landed during my pre-flight; last was a JOURNAL entry = session wrapped). The operator's instruction assumed a clean `main` with a staged TOKEN-LOG; reality differed (TOKEN-LOG already committed in `98dd74f`; ADR-59 not on main). With operator approval at each fork: merged ADR-59 branch → `main --no-ff` first (the taxonomy prompt's dependency gate), verified 85 green + health 6/6, then branched taxonomy off the now-ADR-59-bearing main. Phase B: **ADR-60** + README index/Related. Phase C: PLAYBOOK "docs/ folder taxonomy" section + ESSENTIALS line. Phase D: created `docs/council-questions/` (+ semantic README) + `git mv`'d the 7 Council inputs (Q1–Q5 + evidence + set index) from `research/`. Phase E: `git mv`'d the audit chain (pipeline discovery/audit/proposal/index, debate-forensics, mechanism-discovery, handoff-stabilization discovery+validation) to `audits/` and the consolidation preflight (transient) to `archive/2026/`. Phase F: archived dormant `tech-radar/` → `archive/tech-radar/`. Phase G: rewrote `research/README.md` codifying the WORKING semantic. Phase H: closed 3 BACKLOG entries + this entry.
- Result: every `docs/` subfolder now carries one semantic role (inputs/outputs/working/archived); pipeline-audit finding A1 (HIGH) closed. 85 tests green + ruff clean after every commit; `audit.py health` OK; tree clean. `research/` retains 12 genuinely-exploratory files + README; `council-questions/` holds the 7 inputs + README; `audits/` gained 8 migrated outputs.
- Decision / scope notes: per **ADR-60 Rule 5**, append-only + immutable records (ADR-55..58, the 5 handoff-Q transcripts, JOURNAL) that cite since-moved files were left intact as point-in-time history — only living docs (BACKLOG, HANDOFF_PROCESS, READMEs) + the moved files' *own* internal cross-refs were repointed. So a grep for old `research/` paths still shows historical hits in JOURNAL/ADRs/transcripts **by design**, not as a miss. The prompt referred to the tech-radar BACKLOG item as "#9"; it is entry **#8** in the current section (closed by content, numbering noted).
- Changes: `docs/decisions/ADR-60-*` (new) + `decisions/README.md` (index + Related); `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md` (taxonomy sections); `docs/council-questions/` (new folder + README + 7 migrated inputs); `docs/audits/` (+8 migrated outputs, internal refs fixed); `docs/archive/2026/` + `docs/archive/tech-radar/` (new); `docs/research/README.md` (rewritten); `protocols/HANDOFF_PROCESS.md` (evidence path); `BACKLOG.md` (3 closures + path refs); this entry. Branch unmerged, unpushed — awaiting operator merge approval.
- Architectural contract: zero ai-council writes (read-only: confirmed the `council-question-guide.md` path + CLI frontmatter only); Layer-2 invariant intact (no scripts added; `audit.py` untouched — folder-semantics validation left as a BACKLOG candidate per ADR-60); ADR-43 transcript routing untouched.
- Abandoned: none.
- Next: operator merges `docs/folder-taxonomy-implementation-2026-05-27` to `main` (`git merge --no-ff`). Candidate follow-up: extend `audit.py` with a folder-semantics check (BACKLOG candidate noted in ADR-60). The ADR-59 child-repo visual-pattern retrofits remain queued from the prior session.

---

### 2026-05-27 — Codify + enforce the universal visual repository pattern (ADR-59)

- Did: Closed the "audit PASS but visual chaos at root" gap from the 2026-05-26 universalization, on branch `docs/universal-visual-pattern-codification-2026-05-27` off `main` (10 commits, one revertable unit each). Phase A: repointed the misplaced `docs/cross-repo-universalization-verification-2026-05-26` branch from `f532283` → `ab303c8` (its namesake report content, already on `main`; non-destructive — operator chose repoint over delete) + documented the concurrency anomaly. Phase B: new **ADR-59** (Universal Visual Repository Pattern) + PLAYBOOK "Universal visual pattern" subsection + ESSENTIALS cheat line. Phase C: three new read-only `audit.py` checks (`dot_prefix_discipline`, `canonical_md_visibility`, `workspace_settings`) with a JSONC-tolerant parser, 13 unit tests, and a self-conformance section wired into `audit.py health`; expanded `ALL_CHECKS` to 6 + made the synthetic fixture a conforming exemplar. Phase D: applied the pattern to `.dev-knowledge`'s own workspace. Phase E: 4 read-only child-repo retrofit plans. Phase F: full verification.
- Result: 85 tests green + ruff clean after every commit; `audit.py health` self-audit **6/6 PASS** on `.dev-knowledge`; tree clean. Pattern is now codified (ADR-59), enforced (audit tool), self-applied, and planned for rollout.
- Verification corrected the originating plan on three points (checked, not assumed): VS Code `explorer.sortOrderLexicographicOptions` must be **`upper`** not `default` (default mixes case) to cluster ALL-CAPS files; `explorer.sortOrderReverse` is **not a real VS Code setting** (no-op — the prior "newest dates first" never worked) so it was removed; the canonical-file check requires **4 mandatory** files not the plan's 7 (LESSONS/PLAYBOOK/ESSENTIALS/TOKEN-LOG are `.dev-knowledge`-only — requiring them would falsely fail every child repo). Empirically verified `tach` 0.34.0 ignores `.tach.toml`, so `tach.toml` is a dot-prefix exception.
- Changes: `docs/decisions/ADR-59-*` (new) + `docs/decisions/README.md` (index); `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md` (visual-pattern sections); `scripts/audit.py` (3 checks + `_strip_jsonc` + health) + `tests/test_audit.py` (+13 tests) + `tests/fixtures/repo-with-structural-checks/.repo-with-structural-checks.code-workspace` (new); `.dev-knowledge.code-workspace` (sort settings); `docs/audits/2026-05-27-{concurrency-anomaly-cleanup, ai-council, corp-ops, corp-sca-time-automation, corp-monorepo}-*.md` (new); this entry. Branch unmerged, unpushed — awaiting operator merge approval.
- Architectural contract: zero writes to any child repo (read-only inspection for the retrofit plans); Layer-2 invariant intact (audit.py extension is read-only enforcement per ADR-36); no orchestration script added.
- Next: operator merges `docs/universal-visual-pattern-codification-2026-05-27` to `main` (`git merge --no-ff`). Then run the 4 retrofit sessions (one CC session per child repo, separate workdirs) consuming the plans in `docs/audits/`; corp-monorepo needs the open ruff-strictness decision first. Operator may want a BACKLOG entry escalating #5 (git worktree pattern — this session's anomaly is fresh evidence).

---

### 2026-05-26 — Handoff process stabilization: implement all 5 Council decisions (Q1-Q5)

- Did: Implemented the full output of the 2026-05-26 AI Council handoff debate (Q1-Q5) on branch `docs/handoff-process-stabilization-2026-05-26` off `main` (`31a95b9`), step-by-step / one revertable commit per unit (16 commits). Phase A: pre-flight gate (consolidation merged, 5 transcripts present) + discovery snapshot. Phase B: 4 new ADRs (ADR-55 applied-task gate / ADR-56 Prompt Generation Card / ADR-57 two-layer bundle contract / ADR-58 structured claims) + an ADR-42 Q5 amendment, each citing source transcript line ranges and registered in `docs/decisions/README.md`. Phase C: amended `HANDOFF_FOLDER_TEMPLATE.md` (new `10_GATE_PROBE.md` + `11_CLAIMS.md` sections, two-layer contract + scope mapping, applied-task gate replacing the 4-item paraphrase gate, inline Prompt Generation Card, manifest invariant-integrity hashes + `next_session_scope`); bumped `HANDOFF_PROCESS.md` v3.3.3 → v3.4 (structured ratification, gate-failure protocol, verification trigger rule); added the PLAYBOOK card-maintenance rule; added a BACKLOG P2 for the deferred mechanical gate code. Phase D: validation report mapping every action item → commit SHA. Phase E: full verification.
- Result: 5/5 Council decisions implemented as ADR + template/protocol amendment; 4/4 operator extensions (hook guidance, JOURNAL mandate, workflow mandate, git workflow) embedded in the card skeleton. 72 tests green + ruff clean after every commit; `audit.py health` OK; pre-commit hooks pass; tree clean. Two items deferred with explicit tracking: mechanical gate code (BACKLOG P2) and the 5-10-handoff measurement plan (post-rollout).
- Adaptation (flagged, resolved with operator before execution): the prompt assumed standalone `templates/handoff/08_GATE_PROBE.md`/`09_CLAIMS.md` files; the repo defines every bundle file as a section inside `HANDOFF_FOLDER_TEMPLATE.md`, and 08/09 are already `TREE`/`EXECUTION_EVIDENCE`. Operator chose: sections-in-template + numbers `10_`/`11_` (no renumber). Also baked: gate probe is CC-drafted + sender-reviewed (not sender-authored) to mitigate the authoring/hallucination risk Council flagged. Card mirrors PLAYBOOK's full Model/Mode/Effort taxonomy to honor the anti-drift rule.
- Changes: `docs/decisions/ADR-55..58*` (new), `docs/decisions/ADR-42-handoff-format-v3.md` (+2026-05-26 amendment), `docs/decisions/README.md` (index + traceability), `templates/HANDOFF_FOLDER_TEMPLATE.md` (gate/card/claims/two-layer/manifest), `protocols/HANDOFF_PROCESS.md` (v3.4), `protocols/PLAYBOOK.md` (card-maintenance rule), `BACKLOG.md` (+1 P2), `docs/research/2026-05-26-handoff-stabilization-{discovery,validation-report}.md` (new), this entry. Branch unmerged, unpushed — awaiting operator merge approval.
- Architectural contract: zero ai-council writes (read-only context only); Layer-2 invariant intact (mechanical validator is a documented contract, deferred — explicitly forbids workflow sequencing per ADR-28); ADR-45 not reopened.
- Next: operator merges `docs/handoff-process-stabilization-2026-05-26` to `main` (`git merge --no-ff`). Then the new handoff process is active for the next real handoff; create the measurement BACKLOG entry at first handoff; implement mechanical gate code (BACKLOG P2) when ready (Codex review per ADR-54).

---

### 2026-05-26 — Multi-branch consolidation + governance truth-up + BACKLOG codification

- Did: Recovered the scattered-commit state left by three parallel Claude Code sessions (2026-05-25 → 26) that shared one working tree (single `.git/`, HEAD switched mid-session → commits landed on wrong branches). Pre-flight snapshot (`docs/research/2026-05-26-consolidation-preflight.md`) verified 11 commit SHAs + a clean tree, then: (B) re-homed commits via cherry-pick onto three clean branches — pipeline+taxonomy (4), ai-council universalization v2 (3), force-completion (3); (C) merged all three to `main` `--no-ff` in order (`577c314` force-completion → `7e02fbd` pipeline → `bf16c41` universalization); (D) truthed-up ADR-43 routing language; (E) amended the universalization plan with operator decisions 2–5; (F) codified 9 BACKLOG entries; (G) this entry. All work after the merges sits on `chore/consolidation-and-backlog-codification-2026-05-26`, awaiting operator merge approval.
- Result: `main` now holds all deliverables from the three sessions (5 Q1–Q5 transcripts, forensics + mechanism-discovery research docs, the 4-doc pipeline/taxonomy chain, the ai-council audit-refresh + execution-plan). 72 tests green and ruff clean after every commit. Pipeline-audit findings **E1** (3 stale "routing pending/manual" locations across PLAYBOOK + decisions/README) and **E2** (BACKLOG P2 open for shipped routing) closed; **E3** (mechanism doc absent from `main`) closed by preserving `f909768`.
- Adaptation (flagged): the prompt's 9-commit inventory omitted `f909768`/`2006395` (a duplicate `council-mechanism-discovery.md` from the race). The literal plan's chore `reset --hard` would have orphaned it; included it in the chore rebuild so the doc reaches `main` — exactly what audit E3 asks. ADR-43 routing premise verified real (`ai-council/routing.py` `TargetResolver`, opt-in via `target-project:`); truth-up text reflects the opt-in nature, not a blanket auto-mirror.
- Operator decisions captured this session:

  | Question | Decision | Source |
  |---|---|---|
  | README (ai-council) disposition | Delete | Universalization Q1 |
  | Question-files location | New `docs/council-questions/` (Option B) | Pipeline Q1 / proposal |
  | `docs/tech-radar/` status | Keep — BACKLOG decision | Pipeline Q2 |
  | Stage-2 inbox copy | Keep manual | Pipeline Q3 |
  | Reclassify history | New artifacts only | Pipeline Q4 |
  | Folder taxonomy ADR-worthy | Yes | Pipeline Q5 |
  | ADR-43 governance truth-up | Done this session | Pipeline Q6 |
  | Codemap (ai-council) | Hand-authored Mermaid | Universalization Q2 |
  | `.env.example` (ai-council) | Remove | Universalization Q3 |
  | LESSONS scope-tags (ai-council) | Defer | Universalization Q4 |
  | Scrum-master codification | Parallel (entry pre-exists) | Universalization Q5 |
  | Workspace tier-residue (`.dev-knowledge`) | Separate BACKLOG entry | Universalization Q5 |

- Changes: `protocols/PLAYBOOK.md` (ADR-43 truth-up ×2 blocks); `docs/decisions/README.md` (ADR-43 truth-up); `BACKLOG.md` (E2 routing entry closed, README-disposition ai-council=delete recorded, +9 new entries); `docs/research/2026-05-25-ai-council-universalization-execution-plan.md` (decisions 2–5 amendment); `docs/research/2026-05-26-consolidation-preflight.md` (new); this entry. `main` advanced via 3 `--no-ff` merges. Branch `docs/ai-council-universalization-audit-and-plan-2026-05-25` (mislabeled v1) deleted; content preserved on the pipeline branch + v2.
- Pattern: shared-working-tree race condition across concurrent Claude Code sessions. Forward fix = git worktree per session (BACKLOG Council-Pipeline-Follow-ups #5).
- Next: operator merges `chore/consolidation-and-backlog-codification-2026-05-26` to `main`; then the codified P1 wave (draft 5 ADRs, apply `docs/council-questions/`, run the ai-council universalization session, folder-taxonomy ADR). The `chore/council-debate-execution-2026-05-25-handoff-methodology` branch (duplicate mechanism doc `2006395`) was left untouched — operator may delete it post-merge.

---

### 2026-05-25 — Handoff Stage 3 complete (dev-knowledge session-sync)

- Did: Completed Stage 3 for `2026-05-25-dev-knowledge-session-sync`. Thinness pre-flight (M-5) passed — all 5 Stage 2 sections substantive. Drift check passed (Stage 1 `328ded7` is ancestor of Stage 3 HEAD `2b29329`). Generated the 11-file flat bundle at `docs/handoffs/2026-05-25-dev-knowledge-session-sync/` (+ `01_manifest.json` with SHA-256 of all 11), ran the verification layer over witnessed claims, and moved Stage 1+2 inputs to `docs/handoffs/archive/{slug}/`.
- Result: Bundle ready for upload to a fresh chat. Self-handoff → 11 tracked files (`02b` correctly omitted). Verified against repo: ADR-45 supersession withdrawal, SESSION_SETUP.md:209 CHANGELOG drift, CLAUDE.md §4 stale-test note (suite green, 72 passed), three named unmerged branches all exist. Flagged two soft discrepancies in `06_STATE_OF_PLAY.md`: architect's "12-file" count is the cross-repo case (this self-handoff is 11), and "six medium findings" vs five M-residual commits in the log.
- Changes: `docs/handoffs/2026-05-25-dev-knowledge-session-sync/` (12 files new); `docs/handoffs/archive/2026-05-25-dev-knowledge-session-sync/` (stage1+2 moved); this entry.
- Note: Generated on branch `docs/handoff-stage1-2026-05-25-dev-knowledge` (a parallel corp-monorepo Stage 1 was stacked on this branch in `e16d56f`; switched back here so the dev-knowledge Stage 3 commit stays off the corp-monorepo branch). No BACKLOG items closed by this handoff (session-sync).
- Next: Rob opens a NEW claude.ai chat, uploads the bundle, pastes `00_first-message.md`. Old chat can close.

---

### 2026-05-25 — Handoff Stage 3 complete (corp-monorepo session-sync)

- Did: Completed ADR-42 v3.0 Stage 3 for `2026-05-25-corp-monorepo-session-sync`. Generated 12-file cross-repo session-sync bundle in `docs/handoffs/2026-05-25-corp-monorepo-session-sync/`. Archived stage1/stage2 inputs to `docs/handoffs/archive/`. Committed on branch `feat/handoff-2026-05-25-corp-monorepo` (SHA `7b49a61`).
- Failed: Nothing failed. 72 tests pass, ruff clean.
- Next: Rob uploads bundle to new claude.ai chat, sends `00_first-message.md`, runs `07_ACTION_PLAN.md` directive #1 (ADR-27 implementation audit) in corp-monorepo Claude Code session.

---

### 2026-05-25 — Handoff Stage 1 generated (corp-monorepo session-sync)

- Did: Generated handoff Stage 1 for `2026-05-25-corp-monorepo-session-sync`. Captured corp-monorepo HEAD `32a47f85b07d697be20066c1ec69df3cf92cb1f6` on `main`, clean working tree. Wrote `stage1-question.md` (5-question pipeline customized with P1 tier-deprecation + scrum-master ADR tasks, audit GAP findings, and relevant P2 BACKLOG items) and the `stage2-response.md` placeholder.
- Result: Stage 1 committed; awaiting Stage 2 (old-chat architect response).
- Changes: `docs/handoffs/in-progress/2026-05-25-corp-monorepo-session-sync/stage1-question.md` (new), `.../stage2-response.md` (new placeholder), this entry.
- Next: Rob takes the PASTE_BOUNDARY block to the old corp-monorepo chat; replaces the placeholder in `stage2-response.md` with the response; says "complete handoff for corp-monorepo" → Stage 3.

---

### 2026-05-25 — Handoff Stage 1 generated (dev-knowledge session-sync)

- Did: Generated handoff Stage 1 for `2026-05-25-dev-knowledge-session-sync` (self-handoff, session-sync). Captured HEAD `328ded75b3a64b4191fca1fe418374671a120a14` on `main`, clean working tree. Wrote `stage1-question.md` (5-question pipeline customized with the post-arc state + relevant open BACKLOG items) and the `stage2-response.md` placeholder under `docs/handoffs/in-progress/{slug}/`.
- Result: Stage 1 committed; awaiting Stage 2 (old-chat architect response). Validators run pre-commit.
- Changes: `docs/handoffs/in-progress/2026-05-25-dev-knowledge-session-sync/stage1-question.md` (new), `.../stage2-response.md` (new placeholder), this entry.
- Next: Rob takes the PASTE_BOUNDARY block to the old `.dev-knowledge` chat; replaces the placeholder in `stage2-response.md` with the response; says "complete handoff for dev-knowledge" → Stage 3.

---

### 2026-05-25 — Handoff audit residuals (re-scoped from a stale refactor prompt)

- Did: Received a 2026-05-24 handoff prompt to refactor the handoff process — headline was an 11→4 bundle consolidation plus resolution of six 2026-05-20 audit findings. Before executing, verified the prompt against repo state and found its core premise broken: (1) the 11→4 mapping table named files that exist nowhere in the repo (`02_TASK`, `03_BOUNDARIES`, `04_AUDIT_CONTEXT`, `05_BACKLOG_REFS`, `08_DIRECTIVES`, `10_ROLE`, `11_FORMAT_RULES` — grep returned zero; real bundle is `00_README/00_first-message/01_MANIFEST/01_manifest.json/02_VISION/03_PLAYBOOK/04_ESSENTIALS/05_GOVERNANCE_ESSENCES/06_STATE_OF_PLAY/07_ACTION_PLAN/08_TREE/09_EXECUTION_EVIDENCE`); (2) consolidating 11→4 silently drops the full VISION/PLAYBOOK/ESSENTIALS invariant copies + SHA-256 manifest — materially ADR-45's bundle-collapse direction, which the 2026-05-20 audit §6 records as explored and rolled back. Flagged to operator; operator chose "audit fixes only, re-scope consolidation separately."
- Result: Repo-state check showed the 2026-05-22 drift-burndown already resolved M-1 (named surfaces), M-3 (Stage 3 step 12), L-3, and M-2's Status line, and deliberately deferred M-5 + M-6. Resolved the genuine residuals across 5 commits on `docs/handoff-audit-residuals-2026-05-25`. `pytest` 72 passed, `ruff` clean after every commit. Consolidation, ADR-42 amendment, and `_in_progress`→`in-progress` rename NOT done (re-scoped / awaiting operator).
- Changes:
  - `CLAUDE.md` — §7 `/handoff` label v3.1 → v3.3.3 (M-1 residual surface the burndown missed)
  - `protocols/HANDOFF_PROCESS.md` — struck residual CHANGELOG from Stage 3 Output line (M-3); added Stage 2 thinness pre-flight (step 2 + checkpoints row, M-5)
  - `templates/HANDOFF_FOLDER_TEMPLATE.md` — struck residual CHANGELOG from generation step 17 (M-3)
  - `docs/decisions/ADR-45-handoff-architecture-v4.md` — withdrew `Supersedes: ADR-42` header claim (strikethrough + Amendment 2026-05-25), reconciling with the already-fixed Status line (M-2)
  - `docs/decisions/ADR-39-file-lifecycle-governance.md` — registered `HANDOFF_QUESTION_TEMPLATE.md` + `HANDOFF_FOLDER_TEMPLATE.md`, marked stale `HANDOFF_TEMPLATE.md` entry superseded (M-6)
  - `BACKLOG.md` — narrowed P3 template-registry entry to the remaining non-handoff template class decision
- Abandoned: 11→4 bundle consolidation + the ADR-42 consolidation amendment — premise broken (fictional file map; contradicts audit "preserve what works" + ADR-45 rollback). `_in_progress`→`in-progress` rename — independent and safe but not an audit finding; left for operator to greenlight. Prompt's "add ADR-39 frontmatter" mechanism for M-6 — wrong mechanism; ADR-39 registers via its Registry, used that instead.
- Next: operator merge approval for `docs/handoff-audit-residuals-2026-05-25`. If consolidation is still wanted, it needs a reality-based 11→N design and an explicit decision to re-open ADR-45 (drop or keep the invariant full-copies) — not hygiene. Optional: `in-progress` rename; non-handoff template class decision (BACKLOG P3).

---

### 2026-05-24 — Session: self-audit + alignment (capping the 2026-05-23/24 reconciliation arc)

- Did: Ran a comprehensive self-audit of `.dev-knowledge`'s own canonical files against its amended (post-tier-deprecation) standards, then remediated every finding. Entry also records the broader 2026-05-23 → 2026-05-24 session arc.
- Result: 14 findings fixed across 7 files (2 HIGH, 9 MEDIUM, 3 LOW). Immutable audit report at `docs/audits/2026-05-24-dev-knowledge-self-audit.md`; 2 open questions logged. `pytest` 72 passed, `ruff` clean, `audit.py health` OK throughout.
- Changes: `docs/audits/2026-05-24-dev-knowledge-self-audit.md` (new); `ARCHITECTURE.md`, `protocols/ESSENTIALS.md`, `CONTRIBUTING.md`, `VISION.md`, `protocols/PLAYBOOK.md`, `protocols/ENVIRONMENT.md`, `CLAUDE.md` (residue cleanup, one commit each); `LESSONS.md` (session patterns); this entry.
- Branch: `chore/self-audit-and-alignment-2026-05-24` (unmerged, unpushed).

**Self-audit findings remediated:**
- A1 [HIGH] `ESSENTIALS.md` "Project Scale Tiers" — a live deprecated-tier prescription (referenced struck `[L only]`/`[L+M]` tags + a renamed PLAYBOOK section). Sat beyond a naive grep's hit cap → why Prompt 10 missed it.
- A2 [HIGH] `ARCHITECTURE.md` `## Diagrams [M/L]` tier-letter tag (operator-flagged seed).
- A3-A5 [MED] `ARCHITECTURE.md` governing-ADR descriptions: ADR-38 self-contradiction, ADR-40 deprecation note, ADR-41 "M+ tier" gating.
- A6 [MED] `CONTRIBUTING.md` BACKLOG "M+ tier mandate" → universal.
- B1-B5 deprecated-feature residue: CHANGELOG refs in VISION (×2), PLAYBOOK (taxonomy row + branch-rename step), ENVIRONMENT (version-tracking).
- E1 [MED] `CLAUDE.md` §8 dangling repo gotchas-skill reference (no `.claude/skills/` exists).
- E2 [MED] `ENVIRONMENT.md` stale structure diagram (listed deleted README/CHANGELOG; missing ARCHITECTURE/VISION/BACKLOG/CONTRIBUTING).
- E3 [LOW] `VISION.md` "audit tool pending / until tool exists" — tool exists and runs.
- Preserved (historical, not prescriptive): BACKLOG tier residue in closed/superseded items + descriptive rollout context; correctly-framed deprecation notes in VISION/ARCHITECTURE; PLAYBOOK's reconciled S/M/L informal bands.
- Open questions: OQ-1 (ESSENTIALS task-scale "Scale S/M+" terminology collision — left intact, not a violation); OQ-2 (reframe vs create the repo gotchas skill — reframed, no artifact created).

**Session arc 2026-05-23 → 2026-05-24 (for the record):**

Cross-repo deep audits (scrum-master review pattern):
- corp-monorepo deep audit (Opus) — `docs/audits/2026-05-23-corp-monorepo-deep-audit.md`.
- ai-council re-pass (Opus) — `docs/audits/2026-05-23-ai-council-deep-audit.md`.
- Pattern now N=3 (ai-council 2026-05-12 + corp-monorepo 2026-05-23 + ai-council re-pass 2026-05-23).

Standard reconciliation — tier system deprecation (merge `427f9a6`):
- ADR-38 amended (universal baseline A5; CHANGELOG struck; ARCHITECTURE universal; README deprecated); ADR-33 amended (tier/scale out of VISION frontmatter); ADR-40 DEPRECATED; ADR-51 amended (ARCHITECTURE mandatory universally).
- Audit tool: `check_adr38_baseline` → governance-docs-only.
- PLAYBOOK: tier-gating struck, model-selection criteria added, root-hygiene convention added.
- Self-application included .dev-knowledge frontmatter/workspace/README — but missed residue (ESSENTIALS section, ARCHITECTURE `[M/L]`, ADR descriptions); this self-audit session closed that gap.

Root hygiene pass 2 + workspace combo (merge `4ae9bff` + follow-ups):
- `ecosystem-index.yaml` → `ecosystem/index.yaml`; `ruff.toml` → `.ruff.toml`.
- PLAYBOOK root-hygiene section expanded (`.env.example` no-create, dot-prefix-where-supported, no `files.exclude` for config visibility).
- Multi-root workspace + dated-folder aliases + three open-latest tasks.
- Sort iteration spanned 6 commits (`d87bd31`, `6b0ccac`, `ee68675`, `dfda077`, `ebea02d`, `dd350e1`) — see LESSONS reactive-patching entry.

Workspace combo FINAL state (read from `.dev-knowledge.code-workspace` at audit time — supersedes the earlier same-day entry's "reverted to default" note):
- Multi-root order: `📓 .dev-knowledge`, `⚙️ ~/.claude (config)`, `📅 Audits`, `📅 Handoffs`, `📋 ADRs` (aliases at bottom).
- `explorer.sortOrder: "default"` + `explorer.sortOrderReverse: true` + `compactFolders: false` — "newest dates first in aliases AND dotfiles grouped in main root" (operator decision; primary + secondary goals both satisfied).
- Open-latest tasks installed; keybindings remain a post-merge user-scope action.

- Next: operator review + merge approval for `chore/self-audit-and-alignment-2026-05-24`. `.dev-knowledge` then serves as the clean reference for the corp-monorepo + ai-council tier-deprecation rollout sessions (BACKLOG "Tier Deprecation + Root Hygiene Cross-Repo Rollout").

---

### 2026-05-24 — Workspace combo setup: multi-root + open-latest tasks + sort decision

- Did: Set up a native VS Code multi-root workspace combo for fast access to dated artifacts — no extensions required.
- Result: `.dev-knowledge.code-workspace` now has 5 roots (`.dev-knowledge`, `~/.claude (config)`, `📅 Audits`, `📅 Handoffs`, `📋 ADRs`), three open-latest tasks, and `explorer.sortOrder` trialled as `"modified"` then reverted to `"default"` (modified didn't group dotfiles as expected).
- Changes: `.dev-knowledge.code-workspace` (multi-root folders + tasks added; sort reverted). `docs/notes/2026-05-24-workspace-combo-setup.md` folded into this entry and removed.

**Setup details:**

1. **Multi-root workspace** — 5 folders: `📓 .dev-knowledge` (repo root), `⚙️ ~/.claude (config)`, `📅 Audits` → `docs/audits/`, `📅 Handoffs` → `docs/handoffs/`, `📋 ADRs` → `docs/decisions/`. Each dated-folder alias appears as a separate Explorer root so its contents are immediately visible without drilling through `docs/`.

2. **Workspace tasks** — three tasks for single-keystroke access to the latest file in each dated folder:
   - `open-latest-audit` — opens newest `*.md` in `docs/audits/` by name-desc
   - `open-latest-handoff` — opens newest `HANDOFF.md` in `docs/handoffs/` by directory-desc
   - `open-latest-adr` — opens newest `ADR-*.md` in `docs/decisions/` by name-desc

3. **Sort decision** — `explorer.sortOrder: "modified"` trialled; reverted to `"default"` because modified sort didn't group dotfiles as expected.

**Recommended user-scope keybindings** (add to personal `keybindings.json`):

```json
{ "key": "ctrl+alt+a", "command": "workbench.action.tasks.runTask", "args": "open-latest-audit" },
{ "key": "ctrl+alt+h", "command": "workbench.action.tasks.runTask", "args": "open-latest-handoff" },
{ "key": "ctrl+alt+d", "command": "workbench.action.tasks.runTask", "args": "open-latest-adr" },

  // Canonical governance files (added 2026-05-24):
  { "key": "ctrl+alt+v", "command": "workbench.action.tasks.runTask", "args": "open-vision" },
  { "key": "ctrl+alt+j", "command": "workbench.action.tasks.runTask", "args": "open-journal" },
  { "key": "ctrl+alt+b", "command": "workbench.action.tasks.runTask", "args": "open-backlog" },
  { "key": "ctrl+alt+r", "command": "workbench.action.tasks.runTask", "args": "open-architecture" },
  { "key": "ctrl+alt+l", "command": "workbench.action.tasks.runTask", "args": "open-lessons" },
  { "key": "ctrl+alt+c", "command": "workbench.action.tasks.runTask", "args": "open-claude-md" }
]
```

**Mnemonics:** A/H/D for dated artifacts (Audit, Handoff, aDR). V/J/B/L/C for canonical name initial (Vision, Journal, Backlog, Lessons, Claude). R for aRchitecture (A is taken).

**Trial criteria:** 1 week. If muscle memory establishes for the 9 shortcuts → keep as primary access pattern. If access friction persists → escalate to BACKLOG P3 (Pinned Files extension build).

**Post-merge operator actions:**
1. Reopen workspace — File → Open Workspace from File → `.dev-knowledge.code-workspace`
2. Add all 9 keybindings above (user-scope, cannot be committed to repo)
3. Trial 2–3 days for original combo + 1 week for full 9-key set

**Revert path (if combo doesn't work):**
- Partial revert (keep root hygiene, revert workspace): `git revert d87bd31` (Step 4 commit)
- Full revert of workspace+tasks: `git revert d87bd31 <step5-sha>`
- Root hygiene file moves (Steps 1+2) are low-risk and worth keeping regardless

**Why this approach** (comparison table):

| Option | Approach | Cost |
|--------|----------|------|
| A (this) | Multi-root aliases + modified sort + tasks | Native, no ext, ~5 Explorer roots |
| B | Filename prefix hack (00-, 01- prefixes) | Pollutes filenames, affects git log |
| C | `explorer.sortOrderReverse: true` (v1.93+) | Reverses ALL folders, not just dated ones |
| D | Custom extension | Build cost ~4–8h; overkill for 3 folders |

Option A chosen for empirical trial per operator decision 2026-05-23.

---

### 2026-05-23 — Tor B.1: Codemap generator convention landed end-to-end

- Did: Landed the full ADR-51 codemap generator convention — amendment + template update + PLAYBOOK section + pre-commit hook + first dogfood on `.dev-knowledge`'s own ARCHITECTURE.md. Branch: `feat/codemap-amendment-and-dogfood`, 6 sequential commits off main.
- Result: End-to-end pipeline validated: AST analysis → Mermaid generation → in-place ARCHITECTURE.md rewrite → freshness check round-trip. Pre-commit codemap-freshness hook passes. 41 non-audit tests green (24 codemap + 17 normalize); 1 pre-existing audit failure (known, tracked in BACKLOG). BACKLOG Stream C P2 closed.
- Arc summary: Spec design 2026-05-22 (browser chat architect role) → Prompt 1 build (5 modules in scripts/codemap/, 24 tests, Codex review with HIGH x2 fixes + CRITICAL deferred to amendment; merged main b2296ff) → Prompt 2 land (this work: ADR amendment, template update, PLAYBOOK section, pre-commit hook, dogfood).
- Design decisions made:
  - Embedded Mermaid block in ARCHITECTURE.md (vs prior external SVG reference) — driven by VS Code 1.121 native Mermaid preview (released 2026-05-20); no SVG generation step needed.
  - `scripts/codemap/` location (vs new `tools/` genre) — minimal new ground, extends existing scripts genre.
  - stdlib-only argparse (vs Click) — eliminates pip install ceremony per consumer repo.
  - Layer 2 invariant: reframe-in-ADR-51 (vs split tool / amend ADR-28-36 / AI Council) — codemap-generator as distinct category from validators (check = validator, generate --write = generator). Smallest blast radius; no upstream ADR edits needed.
  - `.dev-knowledge` source root override: `--source-root scripts` (no `src/` in this repo).
- Dogfood result: Single-node diagram (only `scripts/codemap/` is a Python package; `:::orphan` class, honest representation of current state). Rich diagrams will appear with corp-monorepo rollout (6 packages + Tach layer assignments).
- Lessons learned candidates (N≥2 confirmation pending):
  - **TUI rendering vs LLM output**: 4 iterations of CLAUDE.md output-format rule strengthening before web_search revealed Claude Code TUI renders unfenced markdown tables as Unicode box-drawing (~3× token cost when pasted to browser chat). Fix: wrap session reports in fenced code block. Validated empirically across Prompt 1 + Prompt 2 session reports. Pattern: if behavioral fix doesn't take effect after 1–2 iterations, search for underlying mechanism before escalating fix.
  - **Self-check 2× discipline**: applied during Tor B.1 design — first strawman (`tools/` new genre, pip install distribution, SVG output) replaced with simpler/lighter alternatives after second look. Pattern: catching first-pass over-engineering before locking in.
  - **Codex CRITICAL handling**: Layer 2 invariant violation flagged in Prompt 1 deferred to ADR amendment in Prompt 2 — legitimate scope split, not avoidance. Pattern: CRITICAL findings can defer when (a) tool not yet activated, (b) right venue exists for resolution, (c) deferral has explicit destination.
- Changes:
  - `docs/decisions/ADR-51-architecture-doc-convention.md` — amendment appended (9cb5aef)
  - `templates/ARCHITECTURE-template.md` — canonical codemap form → embedded Mermaid (09ba1ad)
  - `protocols/PLAYBOOK.md` — § Codemap workflow added (392d0c9)
  - `.pre-commit-config.yaml` — codemap-freshness hook added (ed28304)
  - `ARCHITECTURE.md` — CODEMAP region replaced with auto-generated single-node Mermaid (b439cbd)
  - `BACKLOG.md` — Stream C P2 closed (this commit)
- Abandoned: none — all 6 steps completed.
- Next: Cross-repo rollout (corp-monorepo, ai-council) is future-session work per Hard Constraint #1 in original handoff. Each repo opts in independently; corp-monorepo will produce the first rich diagram (6 packages + Tach layer assignments). Template drift in those repos (external SVG ref in their current ARCHITECTURE.md) will surface at opt-in time — flag at that session.
- Flag: `templates/ARCHITECTURE-template.md` canonical-target update may cause drift signals in corp-monorepo / ai-council if they follow the old SVG-reference template form. Out of scope to fix now; flag at their opt-in sessions.

---

### 2026-05-22 — Drift burndown: mechanical audit fixes

- Did: Resolved findings M-1, M-2, M-3, L-3 from 2026-05-20 handoff-process audit; X1/M-4 from posture audit. Conditional Step 7 + pre-checks in Steps 5/6 caught prior commit dc46565 had already resolved X2/X3/C1; Step 4 mandatory grep caught test orphan and prompted retire-both decision.
- Result: chore/drift-burndown-2026-05-22 merged to main via --no-ff (4de8980). 5 substantive commits + 1 Codex audit artifact. 27 tests green; Codex no findings.
- Changes:
  - `.claude/commands/handoff.md`, `templates/HANDOFF_FOLDER_TEMPLATE.md` — version labels → v3.3.3 (2072ff7)
  - `protocols/HANDOFF_PROCESS.md` — Stage 3 step 12 (CHANGELOG append) removed (9434966)
  - `templates/HANDOFF_FOLDER_TEMPLATE.md` — absolute-date conversion directive added (2dd5dcc)
  - `docs/decisions/ADR-45-handoff-architecture-v4.md` — Status → "Explored, not adopted; ADR-42 v3.2 remains canonical authority" (abb76a7)
  - `scripts/backlog_extract.py` + `tests/test_backlog_extract.py` — retired together (ADR-49 dormant target; orphan tests caught by Step 4 grep) (a5ed940)
- Abandoned: ESSENTIALS additions for ADRs 35–54 (content authorship, separate session); Stage 2 thinness check (new feature); ADR-39 registry for handoff templates (judgment call).
- Next: Operator to decide Tor B (codemap spec) vs Tor C (corp-monorepo coding) post-session.

---

### 2026-05-20 — Handoff process audit (mechanism, conformance, gaps)

- Did: Read-only audit of how the handoff process actually works at HEAD. Read ADR-42, ADR-45 (head), `protocols/HANDOFF_PROCESS.md` (v3.3.3), both templates (head), `.claude/commands/handoff.md`, `scripts/backlog_extract.py`, `scripts/migrate_links.py`. Verified the just-completed 2026-05-19 cycle: 12-entry bundle (`docs/handoffs/2026-05-19-dev-knowledge-session-sync/`) + Stage 1+2 archive present. Wrote `docs/audits/2026-05-20-handoff-process.md` — mechanism-first, stage-by-stage, severity-tagged gaps.
- Result: Audit immutable. Six MEDIUM gaps surfaced (version-string skew across slash command / template / protocol; ADR-45 status semantics ambiguous; Stage 3 still references deleted CHANGELOG; `scripts/backlog_extract.py` targets deleted `BACKLOG_ARCHIVE.md`; Stage 2 thinness has no validator; ADR-39 registry gap on templates). Three LOW gaps (Stage 2.5 placement framing; drift detection same-session assumption; time-bound REALITY clauses). Two INFO notes (Self-Containment Rule discipline-only; JOURNAL per-stage append). All recommended fixes are < 10 lines each.
- Changes: `docs/audits/2026-05-20-handoff-process.md` (new); JOURNAL prepend.
- Abandoned: None — read-only audit; no tooling, ADRs, templates, or samples modified.
- Next: Decide whether to act on the six MEDIUM gaps. The version-label fixes (M-1) and CHANGELOG-step removal (M-3) are pure cleanup; M-2 (ADR-45 status) is a small governance question worth raising before action.

---

### 2026-05-20 — Posture audit verification + triage + quick-win fixes

- Did: (1) Verified the 2026-05-19 posture audit against ground truth — wrote `docs/audits/2026-05-20-posture-audit-verification.md` scoring each finding CONFIRMED / PARTIAL / REFUTED / BONUS. (2) Surfaced 4 bonus drift items the witness-based audit could not see: `scripts/backlog_extract.py` references deleted `BACKLOG_ARCHIVE.md`; `scripts/migrate_links.py` SKIP_NAMES includes deleted `CHANGELOG.md`; `docs/decisions/README.md` ADR Index missing ADRs 45-50 + 54; `ARCHITECTURE.md` Governing ADRs missing ADR-54. (3) Triaged into BACKLOG: updated C1 (sacred-files — drop CHANGELOG from `.dev-knowledge` list) and C2 (ESSENTIALS — expand scope from ADRs 35-41 to 35-54); added 4 new Stream C entries (backlog_extract drift, migrate_links drift, ADR index gaps, ADR relationship index); added 1 new Cross-stream entry (PLAYBOOK codifications from audit H3/H4/T1/T2). (4) Executed two safe quick wins: removed `CHANGELOG.md` from `migrate_links.py` SKIP_NAMES; extended ADR index in `docs/decisions/README.md` with ADRs 45-50 + 54; added ADR-54 to `ARCHITECTURE.md` Governing ADRs.
- Result: Audit + verification both immutable. LESSONS count corrected from audit's ~39 to actual 135 (3.5x undercount). Tier 1 items (B1 codemap generator, D1 ADR-38 self-compliance, C1 sacred-files coherence) flagged as needing design decisions — out of scope for autonomous run; remain in BACKLOG.
- Changes: `docs/audits/2026-05-20-posture-audit-verification.md` — new immutable artifact (verification companion to 2026-05-19 audit); `BACKLOG.md` — C1 + C2 updated, 5 entries added (4 in Stream C, 1 in Cross-stream); `scripts/migrate_links.py:4` — CHANGELOG.md removed from SKIP_NAMES; `docs/decisions/README.md` — ADR index table extended with 7 entries; `ARCHITECTURE.md` — Governing ADRs list extended with ADR-54; `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Operator review of BACKLOG additions. Tier 1 work (codemap generator + CI freshness check per ADR-51 — already named next-session OBJECTIVE in Stage 2 handoff) and Tier 1 decisions (ADR-38 self-compliance approach: src/ migration vs ADR amendment) are the largest open threads.

---

### 2026-05-20 — Filed external posture audit (read-only, browser-chat architect)

- Did: Filed `docs/audits/2026-05-19-dev-knowledge-posture-audit.md` — a read-only structural / principle-level audit produced by the browser-chat architect (Claude Opus 4.7) following the ADR-53 / ADR-54 effort closure. Witness-based, no file-state verification; explicit "Unknown — verify against repo" markers. Surfaces 17 principles, findings across 10 areas (A–J), 6 principle tensions, 17-item prioritization (Tier 1 names codemap generator + CI freshness, ADR-38 self-compliance, sacred-files coherence).
- Result: Audit immutable per ADR convention; available as input for next session's file-state verification pass against ground truth. Tier 1 recommendations align with Stage 2 OBJECTIVE for codemap generator + CI freshness check (ADR-51 open item).
- Changes: `docs/audits/2026-05-19-dev-knowledge-posture-audit.md` — new (immutable artifact); `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Operator-driven decision on whether to (a) verify findings against actual file state, (b) triage into BACKLOG, or (c) proceed directly to Tier 1 work (codemap generator). Audit's own §7 notes sequencing is the operator's call.

---

### 2026-05-20 — Handoff Stage 3 complete for 2026-05-19-dev-knowledge-session-sync

- Did: Stage 3 reconciliation + folder generation per ADR-42 v3 / HANDOFF_PROCESS v3.3.3. Ancestor check passed (Stage 1 `c4d7c858` is ancestor of HEAD `1f7a985`). Parsed Stage 2 architect response (5-section response targeting codemap generator + CI freshness check spec per ADR-51 open item). Generated 11-file bundle at `docs/handoffs/2026-05-19-dev-knowledge-session-sync/` (self-handoff — no `02b_ECOSYSTEM_VISION.md`). Curated `05_GOVERNANCE_ESSENCES.md` for ADR-51 and ADR-54 (cited in 07). Archived Stage 1 + Stage 2 inputs at `docs/handoffs/archive/2026-05-19-dev-knowledge-session-sync/`.
- Result: Handoff bundle ready for upload to a NEW `.dev-knowledge` browser chat. OLD chat (Stage 2 source) can be closed.
- Changes: `docs/handoffs/2026-05-19-dev-knowledge-session-sync/` — new (11 files); `docs/handoffs/archive/2026-05-19-dev-knowledge-session-sync/` — new (stage1-question.md + stage2-response.md moved from `_in_progress/`); `docs/handoffs/_in_progress/2026-05-19-dev-knowledge-session-sync/` — removed; `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Operator zips/uploads bundle into NEW chat, pastes `00_first-message.md`, runs articulation gate + synthesis; new session targets codemap generator + CI freshness check spec per ADR-51 open item.

---

### 2026-05-19 — Handoff Stage 1 generated for 2026-05-19-dev-knowledge-session-sync

- Did: Generated Stage 1 handoff artifacts for self-handoff of `.dev-knowledge`. Captured HEAD `c4d7c858` at clean working tree on `main`. Created `_in_progress/2026-05-19-dev-knowledge-session-sync/` with `stage1-question.md` (PASTE_BOUNDARY block for OLD chat) and `stage2-response.md` placeholder.
- Result: Awaiting Stage 2 architect response from OLD `.dev-knowledge` browser chat.
- Changes: `docs/handoffs/_in_progress/2026-05-19-dev-knowledge-session-sync/stage1-question.md` — new; `docs/handoffs/_in_progress/2026-05-19-dev-knowledge-session-sync/stage2-response.md` — new (placeholder); `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Rob carries paste block to OLD chat; populates `stage2-response.md`; says "complete handoff for dev-knowledge" → Stage 3.

---

### 2026-05-19 — Codex reviewer config globalized (ADR-54)

- Did: Branch `docs/codex-reviewer-global-standard`. Authored `codex/AGENTS.md` as the canonical global Codex reviewer config (generic reviewer role, pre-review ARCHITECTURE.md read instruction, checklist, output format — corp-monorepo-specific items dropped). Deployed to `~/.codex/AGENTS.md` (filesystem action, not committed). Added ADR-54 recording the global-standard decision and scope clarification vs ADR-53 (tool config ≠ instruction contract). Added PLAYBOOK §16 note on config ownership. Corrected ARCHITECTURE.md §Authority line to reflect the new model.
- Result: `~/.codex/AGENTS.md` live with generic reviewer config. All repos benefit without per-repo duplication. `corp-monorepo/AGENTS.md` retirement queued as a follow-up chunk in that repo.
- Changes: `codex/AGENTS.md` — new; `docs/decisions/ADR-54-codex-reviewer-global-standard.md` — new; `protocols/PLAYBOOK.md` §16 — 2-line addition; `ARCHITECTURE.md` line 137 — rewritten; `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Retire `corp-monorepo/AGENTS.md` (follow-up chunk in corp-monorepo).

---

### 2026-05-19 — Correct corp-monorepo AGENTS.md violation framing in ARCHITECTURE.md

- Did: Branch `docs/correct-corp-monorepo-agents-violation`. Corrected ARCHITECTURE.md §Authority line 137 — corp-monorepo/AGENTS.md is a Codex tool config, not an ADR-53 instruction contract; ADR-53 has no scope over tool-native config. Violation was a mis-classification, not a real non-conformance.
- Result: Known violations counter → 0 open. ARCHITECTURE.md accurately reflects ecosystem state.
- Changes: `ARCHITECTURE.md` line 137 — rewritten; `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: —

---

### 2026-05-19 — Post-ai-council cross-repo sweep: stale AGENTS.md refs resolved

- Did: Grepped `.dev-knowledge` for ai-council AGENTS.md references after ai-council ADR-53 chunk 4 (AGENTS.md deleted, CLAUDE.md v2.1 live at 139 lines). Branch `docs/post-ai-council-cross-repo-sweep`. 2 commits to live docs.
- Result: All stale ai-council AGENTS.md references in live docs resolved. Immutable docs (ADRs, research transcripts, audits) left untouched per policy.
- Changes: `ARCHITECTURE.md` — removed resolved violation (1) for ai-council CLAUDE.md exceeding 200-line target (now 139 lines); "Two known violations" → "One known violation" (corp-monorepo AGENTS.md remains). `BACKLOG.md` — removed "AGENTS.md removal (future chunk)" from Phase 2 rollout item and ai-council ADR-38 compliance item; both now reflect completion.
- Abandoned: nothing.
- Next: corp-monorepo ADR-53 chunk — AGENTS.md removal and CLAUDE.md migration (the remaining known violation in ARCHITECTURE.md).

---

### 2026-05-19 — Chunk 4: retire AGENTS.md, CLAUDE.md v2.1 live

- Did: Migrated all AGENTS.md content into CLAUDE.md (v2.1 template, 12 sections) and retired AGENTS.md for `.dev-knowledge`. Branch `docs/chunk4-dev-knowledge-claude-md-migration`. 3 commits.
- Result: CLAUDE.md is now the single canonical agent-instruction file per ADR-53. AGENTS.md deleted. All content placed per approved disposition map — no silent drops. Three approved condensations: ADR list trimmed to last 5 (ADR-49–53) with pointer to ARCHITECTURE.md; scope tags reduced to one bullet; per-file update triggers dropped from CLAUDE.md (live in each file's own header). Live-doc references updated in BACKLOG.md (Phase 2 status + ai-council item).
- Changes: `CLAUDE.md` (rewritten to v2.1, ~130 lines); `AGENTS.md` (deleted); `BACKLOG.md` (status updates for Phase 2 and ai-council items).
- Abandoned: Nothing.
- Next: Merge branch to main. ai-council AGENTS.md retirement is a separate future chunk (ADR-53 Decision 2).

---

### 2026-05-19 — Complete CLAUDE.md standard — template v2.1

- Did: Completed the CLAUDE.md template and standard so the next chunk's AGENTS.md→CLAUDE.md migration has a content-preserving target. Branch `docs/complete-claude-md-standard`. 2 commits.
- Result: CLAUDE-md-template.md is v2.1 (12 sections, 126 lines). §3 Architecture (pure pointer to ARCHITECTURE.md) and §4 Conventions (naming/commits/testing/linting/out-of-scope) added. All stale "CLAUDE.md Section 5 (Tools active)" cross-references in PLAYBOOK.md and codex-review-config-template.md reconciled to named-section references — that label was an AGENTS.md artifact never present in the CLAUDE.md template. Content-distribution map added to PLAYBOOK §CLAUDE.md as part of the documented standard. ADR-53 Decision point 4 already correct — no change needed.
- Changes: `templates/CLAUDE-md-template.md` (v2.1); `protocols/PLAYBOOK.md` (distribution map, section-number fixes, cross-reference heading); `templates/codex-review-config-template.md` (section reference fix).
- Abandoned: Nothing.
- Next: Chunk 4 — remove `.dev-knowledge/AGENTS.md` and `ai-council/AGENTS.md`; merge substantive content into each repo's CLAUDE.md per ADR-53 Decision 2.

---

### 2026-05-19 — Chunk 3: bring standard docs into line with ADR-53

- Did: Updated all live governance docs to retire AGENTS.md convention and establish CLAUDE.md as the single canonical per-repo agent-instruction file per ADR-53. Branch `docs/chunk3-standard-to-adr53`. 8 commits across 8 steps.
- Result: No live governance doc references AGENTS.md prescriptively. PLAYBOOK §CLAUDE.md is the new canonical section (replaces retired §AGENTS.md); dual-read mechanism documented; authority hierarchy updated to 3 levels. CLAUDE-md-template.md is v2.0. AGENTS-md-template.md archived. ADR-53 Decision 4 corrected (thin-pointer framing retired).
- Changes: `docs/decisions/ADR-53` (Decision 4 wording); `templates/CLAUDE-md-template.md` (v2.0, thin-pointer refs removed); `protocols/PLAYBOOK.md` (§AGENTS.md section removed, §CLAUDE.md rewritten, 8 additional stale refs fixed across file); `protocols/ESSENTIALS.md` (ADR-53 citation, Scale L definition); `templates/AGENTS-md-template.md` → `templates/archive/` (retired); `ARCHITECTURE.md` (codemap, living-files list, violation statement, ADR index); `BACKLOG.md` (open-item wording); `README.md`, `VISION.md`, `templates/codex-review-config-template.md`, `templates/prompt-template.md` (sweep cleanup).
- Abandoned: Nothing dropped — all 8 steps completed. AGENTS.md root file and CLAUDE.md instruction file untouched (next chunk per scope constraint).
- Next: Chunk 4 — remove `.dev-knowledge/AGENTS.md` and `ai-council/AGENTS.md`; merge substantive content into each repo's CLAUDE.md per ADR-53 Decision 2.

---

### 2026-05-19 — ADR-53: retire ADR-52, establish CLAUDE.md as single instruction file

- Did: Authored ADR-53 superseding ADR-52. Marked ADR-52 superseded (status line only — body untouched). Updated `docs/decisions/README.md` ADR index and traceability table (ADR-52 and ADR-53 both added; ADR-52 was missing from the index). Branch `docs/adr-53-retire-agents-md`.
- Result: Decision record corrects the false premise in ADR-52 Decision 1 (Claude Code does not auto-read `AGENTS.md`; both active tools read `CLAUDE.md`). Empirical evidence cited: `docs/audits/2026-05-19-cohort1-verification.md`. Three commits: `1d161f0` (ADR-53), `7d70807` (ADR-52 superseded), `bc59e9d` (index).
- Changes: `docs/decisions/ADR-53-claude-md-single-instruction-file.md` (new, 49 lines); `docs/decisions/ADR-52-agents-md-convention.md` (status line only: Accepted → superseded); `docs/decisions/README.md` (4 lines added: two index rows, two traceability rows).
- Abandoned: Nothing — scope held cleanly. No PLAYBOOK/ESSENTIALS edits, no AGENTS.md deletions, no template changes (subsequent chunks).
- Next: (1) Subsequent chunk — remove AGENTS.md from `.dev-knowledge` and `ai-council`, merge content into each repo's CLAUDE.md; (2) update PLAYBOOK/ESSENTIALS, retire AGENTS-md-template.md; (3) resolve open violations from prior session (ai-council CLAUDE.md 200-line trim, corp-monorepo AGENTS.md 10-section form).

---

### 2026-05-19 — ADR-51 + ADR-52 conformance: AGENTS.md + ARCHITECTURE.md

- Did: Created `AGENTS.md` at repo root (10-section ADR-52 contract); rewrote `ARCHITECTURE.md` to ADR-51 template (three CORE sections, corrected stale references). Branch `feat/dev-knowledge-adr51-52-conformance`. Full approved plan with dispositions R1–R6 + R8 applied.
- Result: `.dev-knowledge` now self-conformant with its own ADR-51 + ADR-52 conventions. Two commits: `f8160ac` (AGENTS.md), `58ad1d8` (ARCHITECTURE.md). Pytest 50/51 (known failure unchanged). Ruff clean.
- Changes: `AGENTS.md` (new, 146 lines); `ARCHITECTURE.md` (rewrite: +144 −89 lines, `scale: M` frontmatter, `## Purpose [CORE]`, `## Codemap [CORE]` with CODEMAP markers, `## Layer Boundaries & Invariants [CORE]` with 5 numbered invariants, `## Diagrams [M/L]` stub, governing ADRs extended to ADR-52, deleted-file refs removed R1–R3, scope-tag enforcement clause removed R4, hybrid-ratio bullet removed R5, `version:` frontmatter replaced R6, violation count corrected to two R8).
- Abandoned: R7 (full deletion of violations bullet) — not approved; two violations remain open.
- Next: (1) `ai-council` ARCHITECTURE.md (ADR-51, effort M); (2) `ai-council` AGENTS.md §7 bookkeeping — add ADR-51 + ADR-52 (effort S); (3) resolve open violations — ai-council CLAUDE.md 200-line trim, corp-monorepo AGENTS.md ADR-52 10-section form.

---

### 2026-05-19 — rollout-readiness audit (ADR-51 / ADR-52 gap analysis)
- Did: Independent verification of `.dev-knowledge` `main` against all reported session changes; gap analysis of `.dev-knowledge` and `ai-council` (read-only) against ADR-51 + ADR-52. All 14 session commits verified by SHA. All reported files verified as non-trivial. Path-guard block in `codex-review.ps1` confirmed present. One discrepancy found and classified: Stage 3 handoff named wrong failing test (`test_ratio_pass_when_stable_above_ceiling`); actual failure is `test_audit_run_passes_structural_checks_on_synthetic_repo` — self-diagnosed in JOURNAL, not a repo state error.
- Result: `.dev-knowledge` main VERIFIED as reported. Report at `docs/audits/2026-05-19-rollout-readiness.md`. Branch `audit/rollout-readiness-2026-05-19` merged to main. 50/51 pytest pass (known failure unchanged).
- Changes: `docs/audits/2026-05-19-rollout-readiness.md` (new, 250 lines).
- Abandoned: nothing.
- Next: execute rollout in recommended order — (1) `.dev-knowledge` AGENTS.md (ADR-52, effort M), (2) `.dev-knowledge` ARCHITECTURE.md rewrite to ADR-51 template (effort M), (3) `ai-council` ARCHITECTURE.md (ADR-51, effort M), (4) `ai-council` AGENTS.md §7 bookkeeping — add ADR-51 + ADR-52 (effort S).

---

### 2026-05-19 — codex-review sidequest: misdiagnosis correction + code-only path-guard + empty-diff guard
- Did: Diagnose-first Plan Mode investigation of the operator's report that codex-review was "broken for some time" (stale `gpt-5.2-codex` pin + token-burning hook retries). Phase 1 Explore agents found the entire premise wrong: **no hook exists** (`/codex-review` is a manually invoked slash command, `~/.claude/settings.json` registers no codex hook), **no model pin in the wrapper** (`~/.claude/bin/codex-review.ps1` passes no `--model` flag — CLI default `gpt-5.4` is used; `~/.codex/config.toml` auto-migrates legacy `gpt-5.2-codex` → `gpt-5.4`), **no retry loop** (single `codex exec` call, fails fast). Gating Step 1 live verification (Codex on `c9f796d~1..c9f796d` via unmodified wrapper) PASSED — codex returned a real review on `gpt-5.4`, ~48k tokens. Then layered the real fixes: code-only path-guard (extension allowlist `.py .ps1 .sh .ts .tsx .js .jsx .go .rs .rb .java .cs .cpp .c .h .sql .toml .yaml .yml .json .ini`), empty-diff guard, FullAudit-no-src/ guard — all in `codex-review.ps1`. Updated `~/.claude/commands/codex-review.md` Rules block. Documented the code-only rule in PLAYBOOK §16 + §17 and ESSENTIALS "Ending a Session". Verified end-to-end with five cases (5a pure code, 5b pure markdown, 5c empty diff, 5d mixed, 5e -FullAudit with synthetic markdown in `src/`); all PASS. Test artifacts deleted (zero-finding audits per archival protocol; temp git repo removed).
- Result: codex-review working end-to-end — YES. Branch `fix/codex-review-hook`, one tracked commit `7ef77f0` (docs PLAYBOOK + ESSENTIALS). Three untracked `~/.claude/` runtime edits enumerated in Changes below. 50 of 51 pytest pass — baseline failure `test_audit_run_passes_structural_checks_on_synthetic_repo` (`adr38_baseline`) unchanged, out of scope.
- Changes: `~/.claude/bin/codex-review.ps1` (NEW: code-only path-guard block after diff-range resolution + empty-diff guard + FullAudit-no-src/ guard; both prompt templates now include the "Restrict review to these code files only:" block); `~/.claude/commands/codex-review.md` (Rules: added code-only, empty-diff, FullAudit guard bullets + extension allowlist list); `protocols/PLAYBOOK.md` (§16 Cross-Tool Review: added "Code-only rule" paragraph naming the wrapper as enforcement point; §17 Code Quality Audit Process: added "Scope distinct from per-change codex-review" clarification that monthly audit remains deliberately whole-`src/`); `protocols/ESSENTIALS.md` (step 3 "Ending a Session": appended code-only / doc-only-diff-skipped note). Runtime `~/.claude/` edits are outside this repo's git — recorded HERE is their only durable trace.
- Abandoned: Past-failure archaeology (git/audit history dig for evidence of the actual original breakage). Operator approved skipping it once the live healthcheck confirmed the wrapper is working — the "broken" recollection was a stale memory of a transient model-rejection error pre-CLI-auto-migration, not a current state.
- Next: monitor next real-world use; if the path-guard's extension allowlist proves too narrow (Dockerfile, Makefile, .mk asked for), widen per operator request — design contemplated but not added pending demand. Merge `fix/codex-review-hook` → `main` after closeout commit lands.

---

### 2026-05-19 — Action Plan Directives 1+2+3 executed (ADR-51 template, ADR-52 AGENTS.md, PLAYBOOK scope fix)
- Did: Executed all three directives from `07_ACTION_PLAN.md` of the 2026-05-18 session-sync handoff. **Directive 1a** — read-only inspection of `corp-monorepo/ARCHITECTURE.md` + Mermaid→SVG pipeline (`scripts/render-diagrams.ps1`, 3 `.mermaid` sources, manual render, no CI integration); wrote `docs/audits/2026-05-19-corp-monorepo-architecture-inspection.md` as the ADR-51-mandated reference input; satisfied content mandatory minimum, flagged absent auto-generation + CI as corp-monorepo's own gap (ADR-36 read-only contract — not resolved here). **Directive 2** — ratified ADR-52 (`AGENTS.md` cross-tool agent-instruction contract convention) formalizing the extant PLAYBOOK convention with the explicit "agent-instruction contract, not handoff artifact" precision. **Directive 3** — added "Handoff scope" precision block to PLAYBOOK §AGENTS.md and a one-liner in ESSENTIALS clarifying that the Claude-oriented handoff process must not narrate/manage AGENTS.md as handoff content. **Directive 1b** — authored `templates/ARCHITECTURE-template.md` (single canonical template per ADR-51, scale conditionals inline, no per-tier variants), appended BACKLOG Stream C P2 entry for the codemap generator output-spec open item, then ran `codex-review` (1 HIGH + 1 MEDIUM + 1 LOW, all legitimate) and fixed forward in one follow-up commit. Two micro-fixes from operator (header/footer date de-duplication + pointer-convention moved to pre-§1) verified in the committed template. Plan-mode used and approved before authoring. Branch flow deviated mid-session (operator-side branch switch during Plan Mode landed me on `main`); per operator decision, proceeded on `main` with codex-review + fix-forward instead of feat-branch + merge.
- Result: 5 commits on `main` this session — `18da5b5` (inspection report, via merged `inspect/corp-monorepo-architecture-reference` FF), `3cc7197` (ADR-52), `1be2f8b` (PLAYBOOK/ESSENTIALS scope fix), `2acaa96` (template), `706c4ba` (BACKLOG entry), `7f0129b` (codex fix-forward + audit artifact). Orphan `feat/architecture-template-adr51` branch deleted (strict ancestor of `main`). 50 of 51 pytest tests pass; the lone pre-existing failure is `test_audit_run_passes_structural_checks_on_synthetic_repo` (`adr38_baseline` synthetic-repo check missing `tests/` + `ARCHITECTURE.md`) — **note:** the Stage 3 `06_STATE_OF_PLAY.md` named `test_ratio_pass_when_stable_above_ceiling` as the known failure; the actual failing test is the audit-baseline one, recorded here so future handoffs cite the right test.
- Changes: `docs/audits/2026-05-19-corp-monorepo-architecture-inspection.md` (new, 208 lines); `docs/decisions/ADR-52-agents-md-cross-tool-convention.md` (new — added before this session by Directive 2 worker); `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md` (Directive 3 precision block + pointer); `templates/ARCHITECTURE-template.md` (new, ~280 lines after codex-fix); `BACKLOG.md` (Stream C P2 codemap-generator entry appended); `docs/audits/2026-05-19-codex-architecture-template.md` (codex audit artifact). Orphan staged `logs/TOKEN-LOG.md` 2026-05-19 ccusage entry left untouched (predates Directive 1b work; flagged for operator review).
- Abandoned: nothing. The feat-branch + merge git workflow specified in Prompt 2 was abandoned mid-stream when operator-side branch switching during Plan Mode landed me on `main`; operator confirmed proceed-on-main as the non-destructive resolution.
- Next: (1) operator decides what to do with the orphan staged `logs/TOKEN-LOG.md` change; (2) Phase 2 rollout — apply `ARCHITECTURE-template.md` to the M/L cohort (corp-monorepo migrates `docs/ARCHITECTURE.md` → root + adapts to template; ai-council adopts; corp-ops trigger-based); (3) codemap generator output spec (BACKLOG Stream C P2) — design the auto-generated graphical codemap artifact and the CI freshness-check hook; until then, child repos hand-maintain the transitional text-tree form documented in the template; (4) ADR-51 remaining open questions (shared-tooling versioning, pilot criteria) still pending.

---

### 2026-05-18 — Handoff Stage 3 complete for .dev-knowledge (session-sync)
- Did: Generated 11-file self-applied handoff bundle for `2026-05-18-dev-knowledge-session-sync`. Verified HEAD `aeaf1582d68c8e2ae4ff304bf08972f6e01eec10` as ancestor of Stage 1 pin (PASS). Caught one VERIFICATION FAILED: Stage 2 claimed "AGENTS.md currently has no canonical template equivalent" but `templates/AGENTS-md-template.md` EXISTS (10 sections); correction recorded in `06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md` reframed accordingly. Archived stage1/stage2 inputs to `docs/handoffs/archive/2026-05-18-dev-knowledge-session-sync/`.
- Result: Bundle ready at `docs/handoffs/2026-05-18-dev-knowledge-session-sync/`. Directives 1/2/3 from `07_ACTION_PLAN.md` validated: ARCHITECTURE-template.md does NOT yet exist (Directive 1 valid); AGENTS.md convention/decision record does NOT exist (Directive 2 valid, template already present); PLAYBOOK/ESSENTIALS AGENTS.md scope clarification pending (Directive 3 valid).
- Changes: `docs/handoffs/2026-05-18-dev-knowledge-session-sync/` (11 files new); `docs/handoffs/archive/2026-05-18-dev-knowledge-session-sync/` (stage1-question.md, stage2-response.md archived); `docs/handoffs/_in_progress/2026-05-18-dev-knowledge-session-sync/` (removed).
- Abandoned: nothing.
- Next: execute `07_ACTION_PLAN.md` Directives 1/2/3 — author `templates/ARCHITECTURE-template.md` (inspect corp-monorepo first); decide AGENTS.md convention + verify existing template; update PLAYBOOK + ESSENTIALS re: AGENTS.md scope.

---

### 2026-05-18 — Handoff Stage 1 generated (session-sync)
- Did: Generated Stage 1 handoff for `.dev-knowledge` session-sync. Captured HEAD `aeaf158`, clean working tree. Created `_in_progress/2026-05-18-dev-knowledge-session-sync/` with stage1-question.md and stage2-response.md placeholder.
- Result: Stage 1 complete; awaiting Stage 2 architect response from old chat.
- Changes: `docs/handoffs/_in_progress/2026-05-18-dev-knowledge-session-sync/stage1-question.md` (new); `docs/handoffs/_in_progress/2026-05-18-dev-knowledge-session-sync/stage2-response.md` (placeholder, new).
- Abandoned: nothing.
- Next: Rob takes stage1-question.md paste block to old browser chat; pastes response into stage2-response.md; says "complete handoff for dev-knowledge".

---

### 2026-05-18 — ADR-51 architecture-doc convention + automated distillation rule
- Did: Committed architecture-documentation convention ADR from 2026-05-18 Council debate. Transcript already untracked in `docs/decisions/transcripts/` — committed first. Verified ADR number as 51 (highest filed was ADR-50). Aligned draft to `templates/ADR-template.md` (number substitution + Source field; no content changes). Added ADR-51 row + traceability entry to `docs/decisions/README.md`. Recorded ADR distillation as a mandatory automated post-debate step in PLAYBOOK § 5 "Post-debate protocol"; added one-liner pointer in ESSENTIALS.md "Artifact generation direction". 51 tests passed.
- Result: 3 commits on `docs/architecture-doc-adr`: `23652c1` (transcript), `a552454` (ADR-51 + index), `949e9f5` (process rule). Branch merged to `main` with `--no-ff`.
- Changes: `docs/decisions/transcripts/council-out-20260518_215241-pick-2026-05-18_council-debate-architecture-doc.md` (new); `docs/decisions/ADR-51-architecture-doc-convention.md` (new); `docs/decisions/README.md` (ADR-51 index + traceability rows); `protocols/PLAYBOOK.md` (post-debate protocol step 2 expanded); `protocols/ESSENTIALS.md` (Council ADR distillation pointer).
- Abandoned: nothing.
- Next: create `templates/ARCHITECTURE-template.md`; review `corp-monorepo` existing `ARCHITECTURE.md` + C4 pipeline as input to template and codemap generator design.

---

### 2026-05-18 — Handoff Stage 1 generated for ai-council
- Handoff Stage 1 generated for `2026-05-18-ai-council-session-sync`: HEAD `ce885827aada41f582e784fa210f73ff125a18de` captured; awaiting Stage 2.
- Changes: `docs/handoffs/_in_progress/2026-05-18-ai-council-session-sync/stage1-question.md` (new); `docs/handoffs/_in_progress/2026-05-18-ai-council-session-sync/stage2-response.md` (placeholder).

---

### 2026-05-18 — ADR-38 A4 + PLAYBOOK AGENTS.md taxonomy fix
- Did: Appended A4 amendment to ADR-38 closing the corp-monorepo `ARCHITECTURE.md` root-placement migration deferral (A3, 2026-05-11) — deferral is now expired as the universalization rollout executes the move. Corrected PLAYBOOK file-type taxonomy entry for `AGENTS.md`: was "Cross-tool canonical governance" (inaccurate); now "Codex agent-instruction config; per-repo specifics — cross-tool canonical governance is CLAUDE.md + PLAYBOOK/ESSENTIALS". 51 tests passed.
- Result: two commits on `docs/close-architecture-deferral`: `5dc7f29` (ADR-38 A4), `d1dac86` (PLAYBOOK taxonomy fix).
- Changes: `docs/decisions/ADR-38-universal-repo-architecture.md` (A4 appended); `protocols/PLAYBOOK.md` (taxonomy row corrected).
- Abandoned: nothing.
- Next: merge `docs/close-architecture-deferral` to main; proceed with corp-monorepo rollout (Workstreams B/C/D + ARCHITECTURE→root move).

---

### 2026-05-18 — .dev-knowledge session-sync: monorepo rollout prep + scoping
- Did: **Directive 1** — verified ecosystem audit state from Stage 3 handoff; specifically resolved the "possible third governance ADR" (governance-trim) that was unconfirmed in Stage 3. Read-only; no commit. **Directive 2** — wrote `docs/audits/2026-05-17-corp-monorepo-governance-rollout-plan.md`: a phase-by-phase plan rolling the `.dev-knowledge` documentation-governance simplification (ADR-48/49/50) into `corp-monorepo`; two follow-up fix commits reconciled Phase 8 cross-layer write and Q3 review default vs. single-branch model. **Directive 3** — wrote `docs/research/2026-05-17-kimi-k2-scoping.md`: scoping note for incorporating Kimi K2 (Moonshot AI MoE model) into the ai-council panel — covers integration surface, test checklist, and open questions; no implementation. **Directive 4** — wrote `docs/audits/2026-05-17-skills-hooks-usage-review.md`: ecosystem review of all skills and hooks; found `verify` skill is a stub, project-level gotchas pattern exists only in corp-monorepo, no project-level hooks anywhere; surfaced 5 recommendations for a future session.
- Result: rollout plan on disk (`docs/corp-monorepo-rollout-plan` branch, 3 commits: `0faf5a2`, `5ee4193`, `fe4140a`); scoping notes on `docs/session-scoping-notes` branch (2 commits: `99c784f`, `d00c7ff`). Neither branch merged to main yet.
- Changes: `docs/audits/2026-05-17-corp-monorepo-governance-rollout-plan.md` (new); `docs/research/2026-05-17-kimi-k2-scoping.md` (new); `docs/audits/2026-05-17-skills-hooks-usage-review.md` (new).
- Abandoned: nothing.
- Next: merge both branches to main; run corp-monorepo rollout execution in a dedicated session using the rollout plan as spec; evaluate Kimi K2 API access before scheduling integration session; fill `verify` skill body (low effort, Directive 4 recommendation M).

---

### 2026-05-17 — Handoff Stage 3 complete for .dev-knowledge (session-sync)
- Did: generated full 11-file self-applied handoff bundle for `2026-05-17-dev-knowledge-session-sync`; archived `_in_progress/` inputs to `docs/handoffs/archive/`; verified HEAD `9a911952aa9c912218c839f54317170e647a5f44` is descendant of Stage 1 pin `c784845c659a98c59f2c161301577d72e17a4801` (ancestor check PASS, no drift).
- Result: handoff bundle ready for Rob to upload to new `.dev-knowledge` browser chat. Stage 3 verified architect's witnessed claims about branch-cleanup outcome (`git branch` shows `main` only at HEAD) and partial verification of "3 governance ADRs filed" claim (ADR-46 + ADR-47 confirmed present; possible third "governance-trim" ADR unconfirmed — passed through to Directive 1).
- Changes: `docs/handoffs/2026-05-17-dev-knowledge-session-sync/` (11 files: 00_README.md, 00_first-message.md, 01_MANIFEST.md, 01_manifest.json, 02_VISION.md, 03_PLAYBOOK.md, 04_ESSENTIALS.md, 05_GOVERNANCE_ESSENCES.md, 06_STATE_OF_PLAY.md, 07_ACTION_PLAN.md, 08_TREE.txt, 09_EXECUTION_EVIDENCE.md); `docs/handoffs/archive/2026-05-17-dev-knowledge-session-sync/` (stage1-question.md + stage2-response.md moved from _in_progress).
- Abandoned: nothing.
- Next: Rob opens NEW `.dev-knowledge` browser chat, uploads bundle, pastes 00_first-message.md as first message, completes articulation gate + synthesis confirmation, runs generated prompts in Claude Code.

### 2026-05-17 — Handoff Stage 1 generated for .dev-knowledge
- Handoff Stage 1 generated for `2026-05-17-dev-knowledge-session-sync`: HEAD `c784845c659a98c59f2c161301577d72e17a4801` captured; awaiting Stage 2.
- Changes: `docs/handoffs/_in_progress/2026-05-17-dev-knowledge-session-sync/stage1-question.md` (new); `docs/handoffs/_in_progress/2026-05-17-dev-knowledge-session-sync/stage2-response.md` (placeholder).
- Next: Rob pastes `stage1-question.md` PASTE_BOUNDARY block into OLD `.dev-knowledge` browser chat; fills `stage2-response.md`; then "complete handoff for .dev-knowledge".

---

### 2026-05-17 — Document audit test fixtures
- Did: assessed `tests/fixtures/` documentation state; found no README or other discoverable explanation of the fixtures directory. Created `tests/fixtures/README.md` covering what the directory is, the naming convention, an inventory of the one current fixture (`repo-with-structural-checks`) with the test that consumes it, and the maintenance rule tying fixture lifecycle to audit check changes. Committed to branch `docs/document-test-fixtures` branched from `feat/handoff-ai-council-2026-05-17` (which holds fixture rename `c0b7512`).
- Result: `tests/fixtures/README.md` added (`d0c8169`). Branch left unmerged, unpushed.
- Changes: `tests/fixtures/README.md` (new).
- Abandoned: nothing.
- Next: review and merge `docs/document-test-fixtures` into `feat/handoff-ai-council-2026-05-17` or main when ready.

---

### 2026-05-17 — Consolidate the Stage 2 handoff instruction set
- Did: created `docs/consolidate-handoff-template` branch; restructured the Stage 2 instruction set in `templates/HANDOFF_QUESTION_TEMPLATE.md` from 3 "CRITICAL" sections + 7 during-drafting rules + 3 pre-send checks into four numbered parts under one "How to write the response" heading — (1) Epistemic honesty kept as-is, (2) Self-containment with opening principle plus deduplicated rules (old rules 2+3 merged; old rule 5 corrected per Finding 2 to apply only to files not already in the bundle; concision cue per Finding 3 folded in; old pre-send checks 1+3 absorbed into the closing audience-simulation paragraph), (3) Coherence check kept standalone, (4) Format requirements kept as-is; three CRITICAL banners collapsed to one framing paragraph. Then reframed RATIONALE per Finding 1 — section framing question now allows "Unknown" as an acceptable answer; epistemic note made the non-answer explicitly preferred over a constructed rationale; new generation rule requires the `{customized_rationale_prompt}` placeholder to be materialized with non-presupposing "If you witnessed the reasoning for X, state it; otherwise mark Unknown" phrasing. Built a 16-row mapping table BEFORE rewriting to guarantee no rule's substance was dropped; re-checked it against the rewritten file after. 2 commits.
- Result: same substance, stated once. Stage 2 instructions now have 4 named parts instead of 13+ scattered items. Mapping table confirms every original rule's substance survives. No change to the 3-stage process or to ADR-42. Branch left unmerged, unpushed per prompt spec.
- Changes: `templates/HANDOFF_QUESTION_TEMPLATE.md` (Stage 2 instruction block restructured; RATIONALE section + generation rules updated).
- Abandoned: none.
- Next: empirical test on the next real Stage 2 — does the consolidated version actually hold in one's head and reduce drift? If yes, keep; if not, iterate on what slipped through.

---

### 2026-05-17 — Handoff Stage 3 complete for ai-council (session-sync)
- Did: generated full 13-file handoff bundle for `2026-05-17-ai-council-session-sync`; archived `_in_progress/` inputs to `docs/handoffs/archive/`; verified ai-council HEAD `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8` (ancestor check PASS, no drift).
- Result: handoff bundle ready for Rob to upload to new ai-council browser chat. Pre-resolved: `docs/HANDOFF.md` confirmed absent (Stage 3 verification). AGENTS.md absence flagged as governance gap (Council #28) and captured in Directive 2.
- Changes: `docs/handoffs/2026-05-17-ai-council-session-sync/` (13 files: 00_README.md, 00_first-message.md, 01_MANIFEST.md, 01_manifest.json, 02_VISION.md, 02b_ECOSYSTEM_VISION.md, 03_PLAYBOOK.md, 04_ESSENTIALS.md, 05_GOVERNANCE_ESSENCES.md, 06_STATE_OF_PLAY.md, 07_ACTION_PLAN.md, 08_TREE.txt, 09_EXECUTION_EVIDENCE.md); `docs/handoffs/archive/2026-05-17-ai-council-session-sync/` (stage1-question.md + stage2-response.md moved from _in_progress).
- Abandoned: nothing.
- Next: Rob opens NEW ai-council browser chat, uploads 12 files (all except 00_README.md), pastes 00_first-message.md as first message, confirms synthesis, runs generated prompts in Claude Code.

### 2026-05-17 — Fixture cleanup + Stage 1 regeneration for ai-council
- Did: renamed stale test fixture `repo-with-all-five-checks` → `repo-with-structural-checks`; updated its internal VISION.md (stale "all five checks" description → accurate 3-check description); deleted two stale fixture files (`BACKLOG_ARCHIVE.md`, `CHANGELOG.md`) left over from `deedc10` audit-check removal; updated `tests/test_audit.py` fixture path reference. Regenerated `stage1-question.md` for `2026-05-17-ai-council-session-sync` with current template structure (coherence-check concern added, RATIONALE sub-questions reframed as non-presuppositional per template spec).
- Result: 28 tests pass. `stage1-question.md` now faithful to current template structure. `stage2-response.md` placeholder preserved unchanged.
- Changes: `tests/fixtures/repo-with-structural-checks/` (renamed from `repo-with-all-five-checks/`; VISION.md updated; BACKLOG_ARCHIVE.md + CHANGELOG.md deleted), `tests/test_audit.py` (fixture path), `docs/handoffs/_in_progress/2026-05-17-ai-council-session-sync/stage1-question.md` (regenerated).
- Abandoned: nothing.
- Next: Rob pastes `stage1-question.md` PASTE_BOUNDARY block into OLD ai-council browser chat; fills `stage2-response.md`; then "complete handoff for ai-council".

### 2026-05-17 — Handoff Stage 1 generated for ai-council
- Handoff Stage 1 generated for `2026-05-17-ai-council-session-sync`: HEAD `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8` captured; awaiting Stage 2

### 2026-05-17 — Decommissioning discipline: close the orphan gap
- Did: created `feat/decommissioning-discipline` branch; added decommissioning-gap lesson to LESSONS.md; added "Supersession & decommissioning" subsection to PLAYBOOK.md (under Documentation file types); added condensed supersession rule to ESSENTIALS.md; created `templates/ADR-template.md` with `Decommission:` header field. 4 commits total.
- Result: audit health passes. All 4 doc files updated consistently. Branch left unmerged, unpushed per prompt spec.
- Changes: `LESSONS.md` (new entry prepended), `protocols/PLAYBOOK.md` (new ### subsection), `protocols/ESSENTIALS.md` (new ## section), `templates/ADR-template.md` (new file).
- Abandoned: nothing.
- Next: review branch on main and merge when ready; backfill `Decommission:` field on any existing ADRs that supersede or relocate artifacts (starting with ADR-42 handoff centralization).

### 2026-05-16 — Council Simplification slice: .dev-knowledge governance trim
- Did: applied AI Council simplification verdict to `.dev-knowledge` on `feat/docs-governance-simplification` over 6 commits (Steps 2–7). Trimmed `scripts/audit.py` to structural-only checks (vision_md / adr38_baseline / claude_md); deleted CHANGELOG.md + BACKLOG_ARCHIVE.md; demoted ADR-46 + ADR-47 to non-enforced conventions; added deterministic `scripts/normalize_headers.py` + pre-commit auto-format hook; removed the scope-tag enforcement system (`validate_scope_tags.py`, tests, pre-commit hook, CLAUDE.md vocabulary section); documented git-as-changelog + Conventional Commits standard + new `Did/Result/Changes/Abandoned/Next` JOURNAL shape.
- Result: tests 51 passed / 0 failed (was 53 passed / 3 failing). `ruff` clean. Audit output no longer references CHANGELOG / BACKLOG_ARCHIVE / dated-entries / backlog-organization checks. Branch left at `1401618` + this JOURNAL commit; NOT merged, NOT pushed.
- Changes: `scripts/audit.py`, `scripts/normalize_headers.py` (new), `tests/test_audit.py`, `tests/test_normalize_headers.py` (new), `tests/test_validate_scope_tags.py` (deleted), `tests/fixtures/{backlog-*,dated-entries-*}/` (deleted), `scripts/validate_scope_tags.py` (deleted), `CHANGELOG.md` + `BACKLOG_ARCHIVE.md` (deleted), `docs/decisions/ADR-46-*.md` + `ADR-47-*.md` (condensed), `.pre-commit-config.yaml`, `CLAUDE.md`, `CONTRIBUTING.md`, `protocols/ESSENTIALS.md`, `.claude/commands/save.md`, `JOURNAL.md` (this entry + intro rewrite).
- Abandoned: keeping per-entry required-fields check in `check_backlog_organization` — flagged as marginal in the Step 2 commit body; classified as entry-body format-detail and removed. If you want it back as a structural check, the call is in the Step 2 commit body. Pre-existing `adr38_baseline` FAIL (`.dev-knowledge` lacks `src/` + `pyproject.toml`) NOT addressed — out of scope for this branch; surfaced for separate triage.
- Next: morning review of branch `feat/docs-governance-simplification` (7 commits incl. this JOURNAL entry). On approval: rebase / merge to main; otherwise raise the flagged-ambiguity (required-fields-per-entry) and any rollback of demoted ADRs.

---

### 2026-05-16 — Session D: .dev-knowledge ADR-46+47 cleanup complete
- Resolved all 5 FAIL groups from 2026-05-15 dogfood audit: dated_entries_lessons +
  dated_entries_changelog now PASS; BACKLOG_ARCHIVE.md created; 15 entries extracted;
  8 Why: fields added; no [done] tokens in active BACKLOG. Two hidden tail-ordering
  issues surfaced (LESSONS.md and CHANGELOG.md) — fixed in scope.
- Deferred WARNs accepted: Cross-stream 41% (structural; Stream taxonomy grooming P2
  item added for quarterly grooming 2026-07-01); adr38_baseline FAIL is pre-existing
  out-of-scope. Branch: feat/cleanup-adr-46-47-dev-knowledge — awaiting merge approval.

---

### 2026-05-15 — ai-council cleanup handoff bundle dispatched (D2)
- Generated 12-file cross-repo handoff bundle at `docs/handoffs/2026-05-15-ai-council-cleanup/`;
  ADR-42 v3.3.2 format + `02b_ECOSYSTEM_VISION.md` for cross-repo case
- Bundle carries locked migration decisions: `[blocked]`→`[open]`+annotation (ADR-47 vocab);
  session-numbered envelope→ISO (ADR-46); ready for ai-council Claude Code session to consume
- BACKLOG Stream B P1 items annotated in-flight; verification via `.dev-knowledge` re-audit
  post-execution; Session D complete after clean audit pass

---

### 2026-05-15 — Audit Tool P2: ADR-46 + ADR-47 checks + extraction script shipped (Session E)
- `check_dated_entries_format` (ADR-46) + `check_backlog_organization` (ADR-47) + `backlog_extract.py`
  implemented; 56 tests passing; audit tool now 5 checks (was 3)
- Dogfood: 51 checks across `.dev-knowledge` + `ai-council` — 6 pass / 42 fail / 3 warn;
  ai-council git status clean (ADR-36 read-only contract intact)
- Session D scope inventoried: 4 new BACKLOG items (Stream C P1 x2 + Stream B P1 x2)
  anchoring ADR-46/47 cleanup across both repos; extraction script ready for `[done]` extraction

---

### 2026-05-15 — Governance ADRs B+C ratified (ADR-46 + ADR-47)
- Council pipeline (research + pick) executed for both entries; ADR-46 (cross-repo
  dated-entries format) winner B-1 Lightweight Hybrid + sniff-test; ADR-47
  (cross-repo BACKLOG organization) winner C-2 Stream-grouped + Two-file state with
  operational hardening (session-start validator, deterministic script not LLM prompt)
- BACKLOG Stream C P1 Entry 1 + Entry 2 → [done]; Stream C P2 ADR-29 prepend item →
  [superseded] by ADR-46; new Stream C P3 ADR-41 amendment sub-item added
- Files unchanged in this session — Session D (cleanup pass across all repos) and
  Session E (audit tool extension + extraction script) are downstream

---

### 2026-05-15 — Audit Tool P1 MVP shipped
- `scripts/audit.py` CLI (4 commands per ADR-36), ecosystem state schema (`ecosystem/{repo}/state.yaml`
  + `history/`), 3 checks (vision_md, adr38_baseline, claude_md), markdown report to `docs/audits/`
- 27 tests passing; ruff clean; pre-existing test failure unchanged
- Self-audit: `.dev-knowledge` FAIL — `adr38_baseline` missing `src/` + `pyproject.toml` (governance
  repo, not code repo — new BACKLOG Stream C P2 item). Cross-repo: `ai-council` PASS/WARN
  (ARCHITECTURE.md optional, absent)
- Pre-flight gate value confirmed: inferred mandatory-files list in handoff draft was wrong
  (LESSONS.md/JOURNAL.md not universal per ADR-38; src/tests/pyproject.toml missing from inferred
  list). ADR-38 canonical spec used for implementation.
- BACKLOG Stream C P1 "Audit tool P1 implementation" marked [done]

---

### 2026-05-15 — Handoff validation v3.3.3
- Replaced strict-equality HEAD check with ancestor check (`git merge-base --is-ancestor`) across
  template surfaces and HANDOFF_PROCESS; bumped v3.3.2 → v3.3.3
- Empirically verified on 2026-05-15 case: `b640bcf9` confirmed ancestor of `777af78` (exit 0)
- Unblocks: Audit Tool P1 (A) inherits clean handoff workflow; eliminates manual operator override
  on every future handoff

---

### 2026-05-15 — Session close: v3.3.2 template fix + ai-council bundle regenerated
- Template fix implemented: `templates/HANDOFF_FOLDER_TEMPLATE.md` parameterized for cross-repo
  use (`{repo}` in gate #1; target VISION as 02_VISION source; conditional 02b_ECOSYSTEM_VISION);
  Bug C fixed (BOUNDARIES → Hard Constraints). HANDOFF_PROCESS bumped v3.3.1 → v3.3.2.
- ai-council bundle regenerated in-place (13 total files including new 02b_ECOSYSTEM_VISION.md);
  broken state preserved in git history at `c09ee71`.
- Mandatory cross-case trace verification executed before template commit — both traces passed.
- BACKLOG v3.3.2 entry marked [done]. Preceding session work already landed: directive #3
  PLAYBOOK additions merged `72f486e`; LESSON #9 captured `5b51cdc`; LESSONS canonical rewrite `99a104e`.

### 2026-05-14 — Same-day LESSONS canonical rewrite + top relocation
- Same-day LESSONS correction: 9 entries rewritten to canonical 6-field schema, moved from tail to top of dated-entries section
- Surfaced by operator's empirical observation that opening LESSONS.md showed pre-existing 2026-04-21 entry at top — visibility convention need
- ADR-29 ordering amendment deferred to BACKLOG Stream C P2; going-forward formalization is its own scope

### 2026-05-14 — Closed Stream C P1: PLAYBOOK additions for ADRs 36/37/40/41
- Closed Stream C P1 methodology debt: new §10 BACKLOG Grooming (ADR-41), new §18 Ecosystem Audit Tool (ADR-36), §8 amended for ADR-37 two-phase protocol, Project Scale Tiers extended with ADR-40 tier transitions; §10–17 renumbered to §11–17+§19
- Verification: scope tags pass, hybrid ≤25%, BACKLOG Stream C P1 marked [done], 9 cross-ref hits updated in 4 living files

### 2026-05-14 — Interleaved capture: 9th LESSON + BACKLOG v3.3.2 entry
- Interleaved capture: 9th LESSON (`universal-without-cross-case-verification`) + BACKLOG entry for v3.3.2 template fix
- Both bugs witnessed during parallel ai-council Stage 3 generation; template fix deferred per Hard Constraint #3 (Option B over Option A)
- Operator mitigation: no new cross-repo handoffs until v3.3.2 ships

### 2026-05-14 — Append 8 architect-discipline LESSONS entries
- Appended 8 architect-discipline LESSONS entries (5 primary + 3 secondary) from extended-session observations
- Source: docs/handoffs/2026-05-14-dev-knowledge-session-sync/06_STATE_OF_PLAY.md "Work in progress not yet captured"
- Action: captured for review; promotion to ESSENTIALS invariants deferred to operator decision

### 2026-05-14 — Handoff Stage 3 complete for ai-council (session-sync)
- Handoff Stage 3 complete for `2026-05-14-ai-council-session-sync`: 11-file bundle at `docs/handoffs/2026-05-14-ai-council-session-sync/`; Stage 1+2 inputs archived at `docs/handoffs/archive/2026-05-14-ai-council-session-sync/`
- Stage 3 verification: 8 witnessed claims verified, 0 contradictions; 4 architect inferences preserved; 0 unknowns
- No SHA drift (Stage 1 and Stage 3 both captured HEAD `0f069554`)
- Next: open NEW claude.ai chat; upload 11-file bundle; paste 00_first-message.md; confirm `role confirmed` then `synthesis confirmed`

### 2026-05-14 — Handoff Stage 1 generated for ai-council (session-sync)
- Handoff Stage 1 generated for `2026-05-14-ai-council-session-sync`: HEAD `0f069554b894802504aa4e5ce140b1d481ae9ec8` captured; awaiting Stage 2

### 2026-05-14 — Handoff Stage 3 complete (session-sync, v3.3.1)
- Handoff Stage 3 complete for `2026-05-14-dev-knowledge-session-sync`: 11-file bundle at `docs/handoffs/2026-05-14-dev-knowledge-session-sync/`; Stage 1+2 inputs archived at `docs/handoffs/archive/2026-05-14-dev-knowledge-session-sync/`
- Stage 3 verification: 7 witnessed claims verified, 0 contradictions; ESSENTIALS.md line count resolved (323 lines — architect had flagged Unknown)
- SHA drift (8663a7c → ef7f66e) confirmed as expected (Stage 1 commit itself); operator approved proceed
- Next: open NEW claude.ai chat; upload 11-file bundle; paste 00_first-message.md; assess v3.3.1 articulation gate empirically

### 2026-05-14 — Handoff Stage 1 generated (v3.3.1) + v3.3.1 amendment
- Handoff Stage 1 regenerated under v3.3.1 for `2026-05-14-dev-knowledge-session-sync`: HEAD `8663a7c` captured; awaiting Stage 2
- Handoff v3.3.1 amendment landed: audience-awareness rules in
  HANDOFF_QUESTION_TEMPLATE.md. Empirical trigger — 2026-05-14
  self-review of Stage 2 response under v3.3 surfaced 7 patterns
  that confuse new chat (which never sees Stage 1). v3.3 had
  explicitly excluded Stage 1 template from refinement scope; that
  was a scope error. v3.3.1 fixes the upstream template so future
  Stage 2 responses naturally exhibit audience awareness without
  manual downstream patching. AI Council research transcript
  (docs/decisions/transcripts/, separate commit) provides
  concept-level reinforcement with documented caveats about
  hallucinated citations and question-framing bias.

### 2026-05-13 — Handoff v3.3 minimum-viable refinement
- Did: handoff v3.3 minimum-viable refinement landed: audit-validated language
  fixes in 06/07 (plain-English section names, code glosses, Hard Constraints /
  Narrow Scope split, verb-led sentences) + mandatory articulation gate in
  00_first-message. Empirical trigger — 2026-05-13 browser session (5+ hours)
  showed architect had VISION in bundle but did not internalize; operator
  uploaded VISION twice during session. Refinement is template/process-level;
  ADR-42 v3 flow + file count + responsibilities preserved. ADR-45 v1
  superseded (v2 rewrite deferred). Sequential loading + question battery
  deferred pending empirical test of minimum.
- Failed: —
- Next: generate handoff from 2026-05-13 browser session using new v3.3 format;
  empirically test articulation gate; measure against baseline

### 2026-05-13 — Four additional 2026-05-12/13 lessons promoted to ESSENTIALS invariants
- Did: promoted LESSONS #1 (epistemic markers), #2 (completion verification), #6 (validation routing), #8 (artifact-direction) to ESSENTIALS as invariant architect rules; each as own commit for revertability; rule bodies preserved verbatim
- Failed: —
- Next: implementation prompts for ADR-45 — shared validator script first

### 2026-05-13 — ESSENTIALS architect channel-discipline rule documented
- Did: moved channel-discipline rule from LESSONS #10 into ESSENTIALS so it loads as invariant at browser-chat session start per ADR-45 architect-compliance path; PLAYBOOK cross-reference skipped (no matching section exists)
- Failed: —
- Next: implementation prompts for ADR-45 (shared validator first, then hooks, templates, sync-script, dry-run, pilot)

### 2026-05-13 — ADR-45 handoff architecture v4 accepted; session lessons archived
- Did: drafted ADR-45 codifying invariant/session separation + 2-file handoff + defense-in-depth enforcement (grounded in Council research debate `council-out-20260513_102702-...` + pick debate `council-out-20260513_111424-...` + audit `docs/audits/2026-05-12-handoff-process-audit.md`); appended 10 methodology lessons to LESSONS.md; flipped ADR-45 status to Accepted; merged to main with --no-ff
- Failed: architect (browser chat) wrote inline git ops in review approval message; surfaced as 10th lesson (channel-discipline) and folded into this session
- Next: implementation prompts in this order — (1) shared validator script `.dev-knowledge/scripts/validator.py`, (2) MANIFEST + NEXT templates with schemas, (3) session-boundary semantics, (4) three enforcement hooks (git pre-commit + Claude Code PreToolUse + `/save`) calling shared validator, (5) sync-script for @path fallback, (6) bootstrap dry-run on throwaway repo, (7) pilot on `.dev-knowledge` for 2 weeks, (8) gate check, (9) fleet rollout one-at-a-time. Also: ESSENTIALS.md update to document architect channel-discipline rule from lesson #10

### 2026-05-12 — Handoff process audit
- Did: read process spec + templates + slash commands + sample artifacts (current + archive + legacy); wrote audit report describing the process end-to-end in plain prose at `docs/audits/2026-05-12-handoff-process-audit.md`
- Failed: —
- Next: browser chat reads audit, proposes improvements (conversational rethink or Council debate, depending on findings depth)

### 2026-05-12 — Inline reminder questions added to Stage 1 questionnaire
- Did: added brief reminder block at end of Stage 1 questionnaire flow surfacing cross-repo + internal-coherence check categories with explicit pointer to HANDOFF_PROCESS Universal Self-Containment Rule as source of truth
- Result: defense-in-depth for handoff lifecycle achieved without sync drift risk — master rule single source; questionnaire surfaces awareness at moment of writing
- Next: continued testing of fresh handoff generation; observe whether reminder reduces residual failure modes

### 2026-05-12 — Residual logging (LESSON + BACKLOG)
- Did: appended methodology LESSON on name-conflict audit framing; added P2 BACKLOG entry for pre-existing test_ratio_pass_when_stable_above_ceiling failure
- Failed: —
- Next: residual handoff items (skills review, token log analysis) remain as separate-session candidates

### 2026-05-12 — Hooks review proper (/review → /codex-review)
- Did: renamed user-defined slash command `/review` → `/codex-review` (resolves shadow collision with Claude Code built-in PR review skill); updated PLAYBOOK § 15 and ESSENTIALS step 3 Codex-wrapper references; produced resolution audit note with pre-rename shadowing observation (both registered simultaneously, disambiguation scenario); merged `chore/2026-05-12-resolve-review-conflict` to main
- Failed: —
- Next: residual handoff items (BACKLOG grooming, token log, skills review) — separate scope

### 2026-05-12 — Universal handoff self-containment rule added to HANDOFF_PROCESS
- Did: added Universal Self-Containment Rule section to HANDOFF_PROCESS.md covering Stage 1 packaging / Stage 2 generation / Stage 3 reception with per-section scope rules + pre-send coherence checklist + ADR-41 per-repo scope reference; appended LESSON capturing empirical failure observed in session as universal pattern (not repo-specific)
- Result: handoff process rule now universal across all repos handoff lifecycles; structurally prevents repeating cross-repo-in-DIRECTIVES failure in any future handoff (corp-monorepo, ai-council, future child repos)
- Next: BACKLOG cross-repo contamination cleanup (separate concern; operator-confirmed scope only)

### 2026-05-12 — Hooks reconnaissance + ai-council check
- Did: produced docs/audits/2026-05-12-hooks-discovery.md; identified review name-conflict location(s) — user-defined `~/.claude/commands/review.md` (Codex wrapper) vs. Claude Code built-in `/review` skill (PR review); recommended Shape (a) for Prompt 4; confirmed ai-council implemented all 10 scrum-master findings + I7/I8 addendum + council-out-* emitter rename
- Failed: —
- Next: hooks review proper (Prompt 4) — scope locked by recon findings (Shape a, low effort)

### 2026-05-12 — PLAYBOOK § 17 + cover-letter template
- Did: added § 17 Scrum-Master Review Propagation + templates/scrum-master-cover-letter.md; closed BACKLOG P2 propagation-structuring entry
- Failed: —
- Next: hooks reconnaissance (Prompt 3) → hooks review proper (Prompt 4, scope locked by recon findings)

### 2026-05-12 — Cleanup pass
- Did: resolved orphaned 2026-05-12-session-handoff deletion (D2 — already committed as 471ecd3); marked ADR-34 ai-council propagation BACKLOG entry as done (D3); added ADR-42 single-vs-multi-artifact amendment-candidate BACKLOG entry P3 (D7)
- Failed: —
- Next: PLAYBOOK § 17 + scrum-master cover-letter template (Prompt 2)

### 2026-05-12 — Handoff Stage 3 complete for ai-council (session-sync)

**Did:** Stage 3 generated 12-file handoff folder at `docs/handoffs/2026-05-12-ai-council-session-sync/`. Stage 1+2 inputs archived at `docs/handoffs/archive/2026-05-12-ai-council-session-sync/`. HEAD `f094d08` pinned (no drift). Stage 2 architect knowledge preserved: Step 5 smoke test as next action, cost-optimization principle captured, 12 witnessed claims verified against repo state, stale BACKLOG items flagged. BACKLOG items updated.

---

### 2026-05-12 — Handoff Stage 1 generated for ai-council (session-sync)

- Handoff Stage 1 generated for `2026-05-12-ai-council-session-sync`: HEAD `f094d0821a279f3aa36de554943c1b44576d0924` captured; awaiting Stage 2

---

### 2026-05-12 — Handoff Stage 3 complete for dev-knowledge (session-sync)

**Did:** Stage 3 generated 11-file handoff folder at `docs/handoffs/2026-05-12-dev-knowledge-session-sync/`. Stage 1+2 inputs archived. HEAD `0125f1b` pinned. Stage 2 architect knowledge (10 boundaries, 8 directives) captured. CHANGELOG updated.

---

### 2026-05-12 — Handoff Stage 1 generated for dev-knowledge (session-sync)

**Did:** Handoff Stage 1 generated for slug `2026-05-12-dev-knowledge-session-sync`; HEAD `ec44148` captured; awaiting Stage 2 (old chat response).

---

### 2026-05-12 — Prompt N: Session handoff generated

**Did:** Composed session handoff at `docs/handoffs/2026-05-12-session-handoff/` covering session scope (14 commits, 7 prompt cycles), state at end, operator pending actions, deferred substantive work, and critical process principles. Verified browser-provided inventory against repo state; flagged one adjusted item (`2026-05-11-cross-repo-pattern-audit.md` not found in `docs/audits/` — browser claim adjusted).

**Result:** Fresh-session context primer ready (49 lines); next chat reads handoff as session-start input.

**Next:** Fresh session picks up handoff; substantive work (skills review + hooks audit + token logging + methodology proposal review + Phase 2 cross-repo migrations) starts with clean context.

---

### 2026-05-12 — Prompt M: Governance freshness audit + targeted updates

**Did:** Read-audited 8 governance files (ARCHITECTURE.md, CLAUDE.md, CONTRIBUTING.md, README.md, VISION.md, PLAYBOOK.md, ESSENTIALS.md, HANDOFF_PROCESS.md) plus subdirectory READMEs for stale convention references post 2026-05-11 amendments (ADR-34 universal hyphen mandate + ADR-38 ARCHITECTURE.md root placement + A2 archive folder rename). Applied 10 targeted fixes across 4 files (ARCHITECTURE.md × 2, CONTRIBUTING.md × 2, README.md × 2, PLAYBOOK.md × 4). Added 1 new BACKLOG entry (Cross-stream P2: scrum-master review propagation process codification).

**Result:** Governance docs aligned with ratified amendments; all `ADR-NN_` underscore prescription references updated to `ADR-NN-` hyphen; PLAYBOOK §File naming conventions TBD block replaced with ADR-34 pointer; archival step filenames updated to council-out-* format. VISION.md, ESSENTIALS.md, HANDOFF_PROCESS.md, CLAUDE.md — no stale references found.

**Next:** Handoff to fresh session for substantial new scope (skills review + hooks review + token logging + methodology proposal review + Phase 2 cross-repo migrations).

---

### 2026-05-12 — Prompt L: Scrum-master review of ai-council + legacy transcripts relocation

**Did:**
- Produced structured scrum-master review report for ai-council at `docs/audits/2026-05-11-ai-council-scrum-master-review.md` (Scale M; first empirical instance of scrum-master review authority pattern): 10 findings (1 critical, 6 important, 3 minor); covers governance files, ADR-34 compliance, documentation staleness, tasks/ folder hygiene, dead code scan, folder structure
- Relocated 3 legacy `DECISION_NN_*` transcripts from `docs/decisions/transcripts/` to `docs/decisions/transcripts/archive/legacy/` (pre-CLI historical class separation per content-scoped archival principle); updated path references in ADR-31, ADR-32, decisions/README.md, CHANGELOG.md
- Updated BACKLOG: marked AI Council transcript routing [done]; added Cross-stream P2 (codify scrum-master review pattern) + P3 (extend to other repos)
- Appended LESSON: scrum-master review authority pattern (first empirical instance)

**Result:** ai-council review report ready for operator routing to architect. Legacy transcript cleanup complete. Branch merged to main.

**Next:** Operator routes ai-council review to architect for implementation. Scrum-master pattern awaits N=2 before ADR-level codification (see BACKLOG Cross-stream P2).

---

### 2026-05-12 — Prompt K: Atomic file-level cleanup

**Did:**
- K1 (a95318d): 16 ADR renames (underscore → hyphen); 14 transcript renames (council_out_ → council-out-); `docs/handoffs/_archive/` → `archive/` folder rename; 6 legacy flat .md + v2 folder relocated to `docs/handoffs/archive/legacy/`; 23 living docs updated (link refs, path refs, naming convention desc); scope tag validator: pass
- K2 (this commit): BACKLOG P1 `.dev-knowledge atomic migration` marked done; LESSONS: 2 new entries (merge/cleanup completion pattern, punted-migration anti-pattern); JOURNAL + CHANGELOG updated
- K1.4 skipped: cycle 2 propagation artifact absent from Downloads (not present at time of execution)
- Branch: `chore/atomic-cleanup-hyphen-migration` (2 commits, ready for K3 merge)

**Result:** .dev-knowledge file-level mess fully resolved. All upstream decisions (ADR-34 amendment + A2 + Council ratification) now have matching file-level state. Clean working tree on branch.

**Next:** K3 merge to main. Then: cross-repo handshake (BACKLOG P1 — operator routes to ai-council); Phase 2 migrations per BACKLOG P2 entries.

---

### 2026-05-12 — Prompt J: ADR-34 + ADR-38 amendments + BACKLOG reclassification + content-scoped archival principle

**Did:**
- J1: Amended ADR-34 — separator convention changed to universal hyphen mandate for filenames AND foldernames across .dev-knowledge and all child repos; ADR and transcript table rows updated from underscore to hyphen; example set added; scope changed from mandate/recommendation split to universal; Amendments trail added (commit ec45b2c)
- J2: Amended ADR-38 — ARCHITECTURE.md root placement now explicit (was unspecified); conversational A3 decision; Amendments trail added (commit f264966)
- J3: BACKLOG updated — Prompt H entries added in reclassified state (2 marked done: ADR naming + ARCHITECTURE.md placement; 2 kept open: handoff format + undiscovered repos; archive convention marked done per Council vote; A5 designated legacy/opportunistic); 7 new migration sequence entries added (P1 Prompt K atomic migration, P1 cross-repo handshake, P2 CI enforcement, P2 corp-monorepo migration expanded, P2 ai-council migration expanded, P2 content-scoped archival codification, P3 A5 Phase 2 retirement); LESSONS entry appended (content-scoped archival principle); JOURNAL + CHANGELOG updated
- Branch: chore/adr-34-amendment-hyphen-convention (3 commits ahead of main)

**Result:** ADR-34 + ADR-38 ratified per Council decision and operator A3 decision; migration work scoped into Prompt K (.dev-knowledge atomic, includes _archive/ → archive/ rename + propagation artifact archival); content-scoped archival principle captured as BACKLOG P2 awaiting second empirical instance

**Next:** Operator routes cross-repo notification artifact to ai-council; Prompt K executes .dev-knowledge atomic migration

---

### 2026-05-11 — Item 0 epilogue: session-close artifacts
- Did: appended 4 LESSONS entries (codex M1 prompt-craft, M2/L3 bundle staleness, press-back posture validation, advisory framing leakage); added BACKLOG Cross-stream P2 entry for handoff framing receiver-behavior leakage
- Result: 2026-05-11 session lessons captured; empirical finding tracked for future classification
- Next: ported to main 2026-05-17 from chore/session-close-lessons-backlog

---

### 2026-05-11 — Item 0 Prompt C: Codex M1 fix
- Did: reconciled PLAYBOOK dual-write contradiction at "Council Debate Archival Protocol" section (~line 1458); accepted M2 (bundle ESSENTIALS snapshot) + L3 (bundle manifest state) as pre-existing bundle state per point-in-time artifact convention
- Result: PLAYBOOK Council output guidance internally consistent; operators no longer instructed to skip manual archival they actually need to perform; Item 0 closed
- Next: merge `chore/session-sync-stage3-generation` to main after Rob confirms

---

### 2026-05-11 — Item 0 Prompt B: docs alignment + BACKLOG updates

**Did:**
- Rewrote `docs/handoffs/README.md` for v3.2 current format + pre-v3.2 legacy classification
- Rewrote `docs/decisions/README.md` with full ADR index 27-42, transcript naming convention, ADR↔transcript traceability table (spot-checked uncertain mappings)
- Added "Council output convention (current state)" section to PLAYBOOK Section 5
- Corrected `protocols/ESSENTIALS.md` Council output convention from aspirational dual-write to actual single-target + manual archival

**BACKLOG:**
- Added Cross-stream P1 "AI Council cross-project transcript routing"
- Added Stream B P2 "ai-council needs AGENTS.md (PLAYBOOK governance gap)"
- Superseded Stream C P3 "Council CLI dual-write trigger logic" (broader P1 addresses root cause)
- Updated Cross-stream P1 "Council decisions management consolidation" — inventory sub-item closed

**Result:** Canonical docs now match reality; AI Council routing feature properly tracked; ai-council AGENTS.md gap surfaced

**Next:** /review (5 files touched, above 3-file threshold per ESSENTIALS) → Rob gates merge to main

---

### 2026-05-11 — Item 0 Prompt A: handoff lifecycle cleanup

**Did:**
- Confirmed Stage 3 folder + archive already committed (e428a5e); only _in_progress/ orphans remain uncommitted
- Appending JOURNAL baseline entry to mark session start for 0a/0b/0c sequence

**Result:**
- Clean baseline: all Stage 3 artifacts committed; working tree has only untracked _in_progress/ orphans
- Ready for 0b (HANDOFF_PROCESS.md fix) and 0c (orphan cleanup)

**Next:**
- 0b: rewrite Stage 3 step 10 with explicit Move-Item semantics + empty-dir cleanup + post-state validator
- 0c: verify and delete _in_progress/ orphans (ai-council-audit-sync empty dir + dev-knowledge-session-sync post-archive)

---

### 2026-05-09 (night) — Stage 3 complete: .dev-knowledge session-sync handoff generated

**Did:**
- Generated Stage 3 handoff folder: `docs/handoffs/2026-05-09-dev-knowledge-session-sync/`
  (12 files flat per ADR-42 v3.2)
- Applied verification layer to Stage 2 architect claims:
  5 witnessed claims verified against repo; 1 conversation-history claim preserved;
  4 architect unknowns resolved (including DoD fix target clarification)
- Archived stage1-question + stage2-response to `_archive/2026-05-09-dev-knowledge-session-sync/`
- Stage 3 note: DoD bug ("5 required sections") is in the *generated*
  ai-council 07_ACTION_PLAN.md:9, not in HANDOFF_FOLDER_TEMPLATE itself
- Drift between Stage 1 SHA and Stage 3 HEAD confirmed safe (4 intra-session
  methodology commits; Rob explicitly confirmed proceed)

**Result:**
- Self-handoff bundle ready for upload to fresh .dev-knowledge browser chat
- Return trip template (09_EXECUTION_EVIDENCE.md) pre-created in bundle
- OLD .dev-knowledge browser chat can now be closed

**Next:**
- Open NEW claude.ai chat, upload 12-file bundle, paste `00_first-message.md`
- NEW chat presents synthesis; confirm; optional Q&A loop
- NEW chat generates Claude Code prompt(s) for refinement-partner session
- Execute in Claude Code (.dev-knowledge context)
- Return `09_EXECUTION_EVIDENCE.md` to `docs/handoffs/2026-05-09-dev-knowledge-session-sync/`

---

### 2026-05-09 (night, refinement) — BACKLOG strategic priorities + stage1 regenerated

**Did:**
- Added 9 Cross-stream BACKLOG items capturing Rob's strategic plan for
  next sessions: Council decisions management consolidation [P1], Sacred-files
  maintenance enforcement [P1], Hooks audit + consolidation [P2], Skills
  universalization [P2], Ecosystem standards audit [P2], Kimi K2 evaluation
  [P3], Scale tier re-evaluation [P3], Large repo migration prep [P3],
  VS Code productivity [P3]
- Regenerated stage1-question.md Section B: fresh BACKLOG snippet
  (all existing + 9 new items), updated HEAD sha to f87a5cc
- Added "press back on vague items" instruction to stage1-question Section B
  — next chat (post-Stage 3) is refinement partner, not just executor

**Result:**
- BACKLOG.md now captures Rob's full intended scope for next sessions
- stage1-question.md ready: architect can answer Stage 2 with full
  strategic context; Stage 3 bundle will carry complete BACKLOG

**Next:**
- Rob copies stage1-question.md PASTE_BOUNDARY content to current
  browser chat (the OLD chat for this session-sync)
- Architect provides Stage 2 response (5 sections: OBJECTIVE/REALITY/
  RATIONALE/DIRECTIVES/BOUNDARIES; no outer code fence)
- Rob saves response to stage2-response.md (replace below marker line)
- Next Claude Code session (after /clear): "complete handoff for
  dev-knowledge" → Stage 3 generates bundle
- ai-council branch docs/audit-sync-2026-05-09 awaits separate
  review/merge (not urgent)

---

### 2026-05-09 (night) — Session wrap-up

**Did:**
- Committed ai-council audit-sync execution evidence (return trip closed,
  branch `chore/session-2026-05-09-wrap-up`, commit 818a1c6)
- Added Strategic emphasis section to VISION.md (4 directions: velocity,
  consistency, evolution, lessons-as-default; conversational clarification,
  no specific repo/file references, scope: meta tagged, commit f578ac4)
- Generated Stage 1 question for .dev-knowledge session-sync handoff
  (session-sync variant; 5 pipeline questions adapted from template;
  eat-dogfood test of v3.1+v3.2 infrastructure for self-handoff)
- Pre-created stage2-response.md template in _in_progress slug directory

**Result:**
- Return trip for ai-council audit-sync closed — ADR-42 end-to-end test
  fully documented
- VISION strategic emphasis made explicit (continuous improvement
  principle operationalized as 4 concrete current directions)
- Session handoff infrastructure deployed: Stage 1 ready, Stage 2
  template awaiting architect response from OLD chat

**Next:**
- Rob copies stage1-question.md PASTE_BOUNDARY content to current
  browser chat (this chat IS the OLD chat for the session-sync)
- Architect responds with 5 sections (OBJECTIVE/REALITY/RATIONALE/
  DIRECTIVES/BOUNDARIES) — no code fence wrapper
- Rob saves response to stage2-response.md (replace below marker line)
- Next Claude Code session (after /clear): "complete handoff for
  dev-knowledge" → Stage 3 generates bundle
- ai-council branch docs/audit-sync-2026-05-09 awaits separate
  review/merge decision (not blocked)

---

### 2026-05-09 — Handoff Format v3.0 implemented + ai-council handoff regenerated

**Did:**

#### Council research → ADR-42 ratified
Council research debate (council_out_20260509_144836_research) surveyed
industry patterns (LangGraph, AutoGen, Cline Memory Bank), mature-domain
protocols (SBAR, I-PASS, SITREP), knowledge management theory (SECI,
Diátaxis). Three providers converged on flat folder, manifest + checksums,
5-7 question pipeline, mandatory receiver verification. Rob's refinements:
full VISION/PLAYBOOK/ESSENTIALS as invariants, ADR essences only (not full
copies), separate first-message.md for UX, tree.txt preserved.

ADR-42 ratified implementing three-stage flow: Claude Code generates
question prompt → Browser-2 architect provides project intelligence →
Claude Code reconciles + generates flat 11-file folder.

#### v3.0 artifacts created
- `docs/decisions/ADR-42_handoff_format_v3.md` (commit 1)
- `protocols/HANDOFF_PROCESS.md` rewritten v3.0 (commit 2)
- `templates/HANDOFF_QUESTION_TEMPLATE.md` (commit 3)
- `templates/HANDOFF_FOLDER_TEMPLATE.md` (commit 4)
- `protocols/SESSION_SETUP.md` updated (commit 5)

#### ai-council handoff regenerated
Broken v2.0 handoff (2026-04-30-ai-council-audit-sync, 3-level nesting,
missing VISION/PLAYBOOK) replaced with v3.0 flat 11-file structure (commit
6). Drift flagged: config/settings.yaml modified in ai-council working tree.

#### BACKLOG P1 closed
`[P1] HANDOFF_PROCESS + HANDOFF_TEMPLATE + first-message.md updates`
closed (commit 8).

**Failed / methodology debt:**
- v2.0 handoff (created 2026-04-30) was structurally wrong on 6 dimensions
  (nested 3 levels, missing VISION/PLAYBOOK/ESSENTIALS, 7 full ADR copies,
  no question pipeline, no return trip). Surfaced by Rob; corrected via
  Council research + v3.0 implementation. Recurring "prescriptive writing
  without verification" pattern (see LESSONS 2026-04-30 entry).

**Next (updated evening — Stage 3 complete):**
- Handoff Stage 3 complete for 2026-05-09-ai-council-audit-sync
  (11-file folder generated; _in_progress archived; verification layer applied;
  config/settings.yaml actual diff: grok model string, not timeout — flagged)
- BACKLOG Cross-stream P1 "Phase 1 validation" marked done (governance cycle
  complete from .dev-knowledge side; execution test in NEW chat is next)
- ADR-39 amendment to register new template files (P3 BACKLOG, still open)
- PLAYBOOK content additions for ADRs 36-41 (P1 BACKLOG, still open)

---

### 2026-04-30 — Stream C session 6

**Did:**

#### ADR-33 ratified — VISION.md universalization
Trigger-based mandate (≥1 dependent), two-tier content (Standard/Lite),
child repo VISION.md required, hybrid enforcement (passive AGENTS.md
note + auditor primary). Migration cohort: ai-council + corp-monorepo
immediate; corp-ops + corp-sca-time-automation trigger-based by
2026-06-30.

#### ADR-34 ratified — File naming convention (cross-repo)
No universal master rule, table per file type. Living docs UPPERCASE,
Protocols UPPERCASE_WITH_UNDERSCORES, ADRs ADR-NN_topic_underscores,
Council transcripts council_out_YYYYMMDD_HHMMSS_*, audits/handoffs
YYYY-MM-DD-topic-dashes, templates kebab-case, configs kebab-case.yaml.
Hybrid enforcement (passive + future auditor).

#### ADR-35 ratified — Lessons base activation
Storage + retrieval + querying. LESSONS.md remains canonical narrative
+ derived lessons-index.json. Push retrieval (SessionStart hook,
scope+recency filter, 60 days). Pull querying (`lessons query`).
Bidirectional pipeline: corrections.jsonl → LESSONS.md → lessons-index
+ ~/.claude/rules/. Cross-repo discovery via DEV_KNOWLEDGE_PATH env
var + walk-up fallback. Promotion automation deferred.

#### ADR-37 ratified — Session Boundary Protocol (two-phase handoff)
Augments ADR-32. Top-level `## Current State` + `## Future State` over
existing 9-section structure (renamed to `## Detailed Context`).
Type-dependent mandate: audit handoffs STRONG, session handoffs MEDIUM
with explicit "undetermined" justification (cognitive exhaustion /
scope mismatch / dependency unresolved). Two-layer drift mitigation:
Browser 2 validation + Browser 1 instrumentation (timestamp + commit
SHA). Confidence level dropped (no enforcement mechanism = decoration).
Forward-only, no migration of historical handoffs.

**Failed:**
- Methodology debt surfaced: JOURNAL.md not updated, LESSONS.md not
  appended, BACKLOG.md proposed without verifying existing files already
  cover function. Strażnik łamiący metodologię. Cleanup before resuming
  Phase 1 closure (ADR-36 audit tool, ADR-38 backlog re-evaluation).

**Next pending:**
- ADR-38 (Cross-Session Backlog Architecture) — paused for re-evaluation
  after JOURNAL + LESSONS cleanup
- ADR-36 (Audit Tool Architecture) — Council debates done, draft pending
- HANDOFF_PROCESS / HANDOFF_TEMPLATE / first-message.md updates reflecting
  ADR-37 overlay (separate session)
- Phase 2 universalization rollout (ai-council + corp-monorepo immediate
  cohort)

**Afternoon addendum (post-ratification work):**
- Phase 1 validation initiated: ai-council audit Faza A1 discovery completed
  (output `docs/audits/2026-04-30-ai-council-discovery.md`); revealed
  ADR-38 architecture violation (flat src/, no src/ai_council/).
  ai-council migration brief generated for browser-2 architect session.
- ADR-40 amendment proposed (coefficient recalibration) then withdrawn —
  observed L-classification of ai-council was symptom of non-compliance,
  not algorithm error. Coefficients (b=12, c=8, d=15) retained pending
  validation against compliant repo measurements.
- `.dev-knowledge` self-audit performed (`docs/audits/2026-04-30-dev-knowledge-self-audit.md`):
  14 registered files audited; surfaced 8 small alignment gaps + ADR-39
  registry self-error (Tach taxonomy conflation).
- This commit applies Tier 1+2+3 batch fixes from self-audit (stale text,
  missing ADR refs, ADR-39 registry correction).

---

### 2026-04-28 | Heavy audit + VISION.md + ARCHITECTURE.md + Council convention reflection

**Did:**
- Heavy audit pass on `.dev-knowledge` after Stream C session 1 deliverables landed (ADR-31, ADR-32, HANDOFF_PROCESS.md v2.0). Phase A read-only audit surfaced: missing VISION.md/ARCHITECTURE.md, stale "personal operating system" framing in README/CLAUDE, JOURNAL/CHANGELOG gaps, PLAYBOOK §12 cap-language vs trigger-language inconsistency, missing Council CLI dual-write convention documentation, LESSONS.md format inconsistency in 4 post-ADR-29 entries, and `docs/decisions/transcripts/` naming dual-track (`DECISION_NN_*.md` vs `YYYYMMDD_HHMMSS_*.md`).
- Phase B created: `VISION.md` (universal-brain mission, charter format per AI Council debate Topic VISION); `ARCHITECTURE.md` (structural model per ADR-28 + ADR-31 Scale-M-with-one-L-tier-artifact); appended 6 lessons (dates-as-deadlines anti-pattern, don't-create-files-unnecessarily, session-close ≠ stream-done, message-count ≠ measurement, prompts always English, distinguish triggers from limits); standardized 4 multi-line LESSONS entries to single-line format per ESSENTIALS spec (content preserved verbatim, missing fields marked `[unknown]`).
- Phase C updated: README mission framing + index + Current state date 2026-04-27 → 2026-04-28; CLAUDE.md files-table adds VISION/ARCHITECTURE + Council output convention subsection + Topic 1/2 entries; ESSENTIALS adds mission anchor + Council convention note; PLAYBOOK §12 trigger language fix + §13 stale notice block + §5 Council Debate Archival Protocol dual-write blockquote (light update; manual path retained).
- Validator change: `scripts/validate_scope_tags.py` IN_SCOPE_FILES expanded to include VISION.md and ARCHITECTURE.md so they participate in section-tag validation and hybrid-ratio counting. Hybrid ratio steady at 18% post-changes (HEAD 18%, delta -0%).
- Predecessor commits folded into this session's narrative (no separate JOURNAL entries warranted): `df637c3` (CONTRIBUTING.md add — gets standalone CHANGELOG line per Rob's rule), `638a916` (VISION debate transcript moved to docs/decisions/transcripts/), `53e7da9` (ADR filename slug fixes from previous session pickup).

**Failed:**
- Pre-existing test break in `tests/test_validate_scope_tags.py::test_ratio_pass_when_stable_above_ceiling`: test references unqualified `"ESSENTIALS.md"` while IN_SCOPE_FILES uses `"protocols/ESSENTIALS.md"`. Verified pre-existing (failure reproduces on `main` HEAD before this audit's changes). Out of scope to fix in this audit; flagged for follow-up.
- LESSONS.md normalization for the 4 multi-line entries had to leave Category and Action fields as `[unknown]` for 3 of them (post-ADR-29 entries that omitted those fields); content preserved per "never delete content," missing structure marked rather than inferred.

**Next pending (Stream C / future sessions):**
- **Pattern dissemination ADR.** Formal ADR universalizing VISION.md template across child repos (corp-monorepo, ai-council, corp-ops, corp-sca-time-automation). Currently flagged in VISION.md Relationships as "pending formal ADR." Templates `CLAUDE-md-template.md` and `AGENTS-md-template.md` would also gain VISION.md / ARCHITECTURE.md cross-refs in that session.
- **Audit tool implementation.** ADR-31 prescribes `tools/audit.py` (read-only cross-repo conformance audit + `repos.toml` manifest + `AUDIT.md` report). Per ADR-31 baseline rule, three known violations (ai-council AGENTS.md missing, ai-council CLAUDE.md trim ≤200 lines, corp-monorepo AGENTS.md correct template) must be remediated before audit ships green. Also implements VISION.md Lifecycle "verification mechanism."
- **`docs/decisions/transcripts/` naming consolidation.** Recommended: standardize on `DECISION_NN_topic.md` for the curated location; rename today's `20260428_125133_format-and-structure-of-visionmd-for-dev.md` → `DECISION_30_vision_format.md`. Defer to dedicated session with ADR for naming convention.
- **Lessons base activation strategy.** Lessons accumulate in LESSONS.md but lack mechanisms for retrieval, promotion, or querying. Future Stream C item; possibly Council-debate territory.
- **PLAYBOOK §8 substantive rewrite.** Already flagged stale (HANDOFF_PROCESS.md v2.0 supersedes); rewrite is its own session per scope discipline.
- **PLAYBOOK §13 substantive rewrite.** Stale notice added this session; rewrite is its own session.
- **ADR-32 §6 diagram errata.** Carried forward from prior JOURNAL entry — Council session decides whether to reissue ADR-32 or accept diagram as known slip.
- **Pre-existing test fix** for `tests/test_validate_scope_tags.py::test_ratio_pass_when_stable_above_ceiling` (path qualification: `"ESSENTIALS.md"` → `"protocols/ESSENTIALS.md"`).

(refs: this branch = `feat/heavy-audit-vision-mission`; commits = VISION add, ARCHITECTURE add, lessons append, lessons normalize, README, CLAUDE, ESSENTIALS, PLAYBOOK, plus this JOURNAL + CHANGELOG entries; VISION debate transcript at `docs/decisions/transcripts/20260428_125133_format-and-structure-of-visionmd-for-dev.md`)

---

### 2026-04-28 | HANDOFF_PROCESS.md v2.0 rewrite

**Did:**
- Full rewrite of `protocols/HANDOFF_PROCESS.md` (v1.x → v2.0) per ADR-32. 9-section table form, folder anatomy, point-in-time copies, charter + step-verification controls, extract-to-task mechanics with defer-requires-justification rule. ~290 lines, hybrid ratio 18%. 4 commits on `feat/handoff-process-rewrite`: protocol rewrite (`b9a7486`), template update (`f21a4d9`), cross-references (`dbca501`), CHANGELOG (`b04605c`).
- `templates/HANDOFF_TEMPLATE.md` rewritten to 9-section skeleton matching new structure.
- `CONTRIBUTING.md` "rewrite pending" notice removed; `PLAYBOOK.md §8` got a one-line stale notice pointing to v2.0 (substantive §8 rewrite deferred to its own session).

**Failed:** —

**Next pending (cross-stream):**
- **ADR-32 §6 diagram amendment.** ADR-32 §6 ASCII diagram puts `HANDOFF.md` at folder root; live first instance + PLAYBOOK + new HANDOFF_PROCESS.md v2.0 put it inside `contents/`. Live layout wins (drag-drop target). HANDOFF_PROCESS.md §4 documents this as known errata. Future Council session decides: reissue ADR-32 or accept diagram as known slip. Do NOT amend ADR-32 silently.
- Substantive PLAYBOOK §8 rewrite (currently stub with stale notice).

---

### 2026-04-28 | ADR-31 + ADR-32 formalized

**Did:**
- Drafted ADR-31 (authority model) + ADR-32 (handoff format) from DECISION_28 + DECISION_29 transcripts. 4 commits on feature branch, merged clean. 2 amendments after Rob review (manifest name softened, extract-to-task follow-up pointer added).

**Failed:** —

**Next:** (a2) `protocols/HANDOFF_PROCESS.md` rewrite referencing ADR-32 — own session.

---

### 2026-04-27 | Stream C session 1 bonus scope — audit infrastructure + Path B + Tier 3 Prompt 2 + X1 + JOURNAL backfill

**Did:**
- ESSENTIALS.md 4-commit refactor (C1-C4): structural cleanup (`2bbe340`, `7421d9e`, `957baee`, `66382ca`, `e1c30cf`), skills reference sub-bullet (`2132a77`), Feedback Loop restructured with Auto vs Manual cadence labels (`e6baca9`), new "How Claude thinks" thinking-quality directives section (`ac96b2c`)
- CLAUDE.md stale references update — PLAYBOOK section count, TOKEN-LOG cadence, ESSENTIALS rule, Council #28 added (`fc8d8b5`)
- README.md Current state section updated to reflect post-Stream-B reality (`2de7826`); handoffs clarified as persistent stream-level decision archive (`3997f11`)
- Deep cleansing diagnostic audit created — 18 findings across 7 files (`8c4a10a`, see `docs/audits/2026-04-27-deep-cleansing-diagnostic.md`)
- ENVIRONMENT.md stale "Last updated: 2026-03-29" fixed → 2026-04-27 (`9e166d9`)
- Path B numbers audit + classification (`d52c243`, see `docs/audits/2026-04-27-numbers-audit.md`); 5-tier execution: Tier A removals (`44f795f`), Tier B replacements (`cff571b`), Tier D rationale (`81edce3`), Tier E decisions (`9a700d9`), merged (`9058238`)
- Tier 3 Prompt 2 audit findings fixes — T1 + C2 + anomaly in CLAUDE.md (`0993669`), E2 + E3 in ESSENTIALS (`3cb9f98`), R2 in README (`3adb6b2`), merged (`0d199e3`)
- X1 verification (Outcome C: PLAYBOOK has its own ### Roles at line 1716 in Section 8, partial overlap with ESSENTIALS canonical version) → blockquote cross-ref added to PLAYBOOK (`b17092d`); audit X1 marked PARTIALLY-INVALID/RESOLVED (`586e360`)
- PLAYBOOK Documentation file types v1.1 — JOURNAL ordering flipped oldest-top → newest-first prepend per Rob's preference (`167c11b`); aligns with TOKEN-LOG/CHANGELOG, LESSONS retains oldest-top per ADR-29
- This JOURNAL.md created with full historical backfill (10 entries, repo creation through today)

**Failed:**
- Audit hallucination N1: deep cleansing audit fabricated specific file metadata (1019 lines, exact filename) for a file that does not exist on disk and has no git history. Discovered via filesystem check + git log verification. Finding marked INVALID (`1d4f3af`); audit reliability flagged. Lesson appended to LESSONS.md.
- Tier 3 Prompt 2 session summary listed 4 items as PENDING that were actually already done in same session (R1/R3/N1/E1). Acknowledged after Rob's pushback. Cause: had git log visible, didn't cross-check before listing pending. Pattern: model produces plausible-looking state claims that read as confirmed evidence.
- Initial JOURNAL backfill prompt halted at Step 1 pre-write after archaeology revealed PLAYBOOK already formally documents JOURNAL.md at three locations with deliberate contradictory spec (oldest-top, Did/Failed/Next, per-session, Scale-conditional). Surfaced conflict, prompt re-issued with PLAYBOOK ordering amendment included.

**Next:**
- CHANGELOG Path B entry (MEDIUM gap — substantive content changes uncovered)
- Handoff doc `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md` append items 21-26 covering today's 6 unlogged Krok 3 bonus-scope work areas
- README "Current state (2026-04-26)" date refresh to 2026-04-27 (LOW cosmetic)
- H1 audit finding (HANDOFF_PROCESS path template) — Krok 5 deferred
- 34 stale feature branches from Streams A/B — future hygiene pass
- Stream C session 2: file naming convention (per Stream C plan)

(refs: 39 commits today; 16 files modified; `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md`; audit docs `2026-04-27-deep-cleansing-diagnostic.md` + `2026-04-27-numbers-audit.md`)

---

### 2026-04-26 | Stream B close + Stream C session 1 — ADR-30 default branch + PLAYBOOK Repo conventions skeleton

**Did:**
- HANDOFF_PROCESS.md v1.1 amendment — 3 artifacts not 1 per Vibe Code 4 protocol patch (`ee7e644`, `4055006`)
- Stream B → Stream C handoff document created (`16bb05c`, see `docs/handoffs/2026-04-26-stream-b-complete-stream-c-scope.md`)
- 8 lessons promoted from CHANGELOG to LESSONS.md as standalone pre-work before session 1 ADR-30 work (`aa6b34f`, branch `chore/lessons-promotion-stream-b-leftovers`)
- ADR-30 created — universal `main` default branch rule for all Rob's repos (`2b337bf`, see `docs/decisions/ADR-30_default_branch_main.md`)
- PLAYBOOK "Repo conventions" section added with 5-subsection skeleton: 1 filled (Default branch), 4 TBD with forward-references to ADR-31/32/33/34 (`274221b`)
- README ADR count updated (`341548c`); CHANGELOG Stream C session 1 entry (`415f275`); HANDOFF_PROCESS + prompt-template master→main updates (`7289cdd`); ADR-30 prompt-template "Merge to master" prose fix (`3a2bf18`); PLAYBOOK ADR-32 placeholder wording standardized (`fabb6eb`)
- `.dev-knowledge` repo renamed master→main (Phase 2; remote rename N/A — local-only repo)
- Codex audit of ADR-30 work (`bc85704`, see `docs/audits/2026-04-26-codex-adr-30-default-branch-main.md`)
- 8 commits on `feat/adr-30-default-branch-main`, merged via `9df901e`
- Stream C session 1 handoff document created with full 11-session plan (`3c97dd2`, see `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md`)

**Failed:**
- Codex audit found 1 Medium ("Merge to master" prose in prompt-template) — fixed in `3a2bf18`. 2 Low findings: Finding 1 accepted as deliberate extended ADR schema, Finding 2 fixed in `fabb6eb`.
- Phase 2 master→main rename reduced scope: Steps 11-14 (push/delete/GitHub UI) N/A — `.dev-knowledge` is local-only repo, no remote configured. First full-flow validation deferred to Stream C sprint 1 (corp-monorepo + ai-council).

**Next:**
- Stream C session 2: file naming convention (per 11-session plan)
- Sprint 1 (session 4): per-repo branch renames + corp-monorepo `.claude/settings.local.json` audit
- Council #27 filter-by-tag rule — UNRESOLVED follow-up (logged in handoff item 17)

(refs: `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md`; ADR-30; Codex audit `docs/audits/2026-04-26-codex-adr-30-default-branch-main.md`)

---

### 2026-04-25 | Stream B implementation marathon — 19 of 19 gaps closed + 1 amendment

**Did:**
- Stream B gaps mapping audit — 19 gaps with placement + dependencies (`5aa3b35`, see `docs/audits/2026-04-24-stream-b-gaps-mapping.md`)
- Gap #6 AGENTS.md template + canonical governance section (`ed82b46`, `f3d981a`); template renamed to codex-review-config-template.md after purpose clarification (`c9d6c07`, `e838b1a`)
- Gap #1 Roles section v1.0 in ESSENTIALS — browser/Claude Code division (`54d7289`)
- Validator/hook H3 divergence discovered + fixed: validator no-args fallback (`446abbe`); validator/hook alignment on heading level scope (`7eaa2c2`)
- Gap #5 CLAUDE.md template v1.0 (thin pointer, hybrid pattern) + PLAYBOOK section (`001fbb2`, `e87525d`)
- Gap #2 + #3 prompt template v1.0 + writing prompts PLAYBOOK section (`1bd4442`, `76af001`)
- Gap #4 + #18 PLAYBOOK Documentation file types and session continuity section — 12-file taxonomy + Scale matrix + 4 common confusions + order conventions (`9a0ed10`)
- Gap #11 HANDOFF_PROCESS.md v1.0 — Vibe Code 4 protocol; handoff-prompts aligned (`5c3ddb5`, `b45a9b5`)
- Gap #12 + #19 PLAYBOOK — Council vs single-model + critic gating; amendment vs reopen decision protocol (`bc4946b`, `6145b8c`)
- Gap #13 PLAYBOOK session boundaries section v1.0 (`80fac2f`)
- Gap #15 + #16 PLAYBOOK — testing rules per Scale tier; Codex review archival protocol (`5aecf57`, `370cf16`)
- Gap #17 PLAYBOOK Continuous Improvement section v1.0 (`0e9105a`); validator skip pattern for docs/tech-radar/ added (`3088a2d`)
- Gap #7a-d PLAYBOOK Claude Code internals section v1.0 (`9a31446`); Gap #7d amendment — subagents factually active (`3860d4d`, `f008489`)
- Gap #10 PLAYBOOK adoption protocol for Claude Code extensions (`8dfe69c`)
- Gap #8 VS Code workspace templates S/M/L (`0b00f70`, `2d890a9`, `05d08a2`) + PLAYBOOK section (`4be065c`)
- Gap #9 Claude Code features inventory audit (`271d6d6`, see `docs/audits/2026-04-25-claude-code-features-inventory.md`); tech-radar cross-link (`a684fc1`)
- Stream B COMPLETE: 19/19 gaps + 1 amendment (`1c9ff9a`)

**Failed:**
- Validator/hook H3 divergence discovered during Gap #1 work — manual validator passed but pre-commit hook failed on H3 tags. Root cause: hook called validator with no args; validator's no-args fallback was vacuous-pass instead of scanning all in-scope files. Fixed in same session.
- Gap #7d initial pass missed that subagents are factually active per `~/.claude/agents/` — amendment commit added explicitly noting this.
- AGENTS.md mental model reverted twice in 48h despite docs documenting reconciliation — logged as lesson candidate (mental model drift after recent reconciliation).

**Next:**
- Stream B → Stream C handoff (Gap #18 amendment candidate: Scale matrix recalibration based on actual project sizes)
- Stream C scope definition + session 1 planning

(refs: `docs/audits/2026-04-24-stream-b-gaps-mapping.md`; `docs/audits/2026-04-25-claude-code-features-inventory.md`; CHANGELOG entries 2026-04-25)

---

### 2026-04-24 | Stream A close + plumbing — ratio-aware enforcement, ADR-27 amendment, TOKEN-LOG cadence, scope-tag rollout

**Did:**
- Research archival (`ccc91d6`, `71ca513`); Council #28/#29 transcripts + research archived (`731cf9d`, `292a4a7`); 7 historical Council debates retroactively archived (`802a533`); README.md created for `docs/research/` and `docs/decisions/` (`60ee717`)
- Council archival protocol added to PLAYBOOK Section 5 (`bd5e6c5`)
- Stream A gap report created with supersession note on consolidated actions (`6945921`); repo sync + CHANGELOG + CLAUDE.md (`4bc8859`)
- PLAYBOOK Phase 2 tagging sanity check (Stream A prompt 3.5) — 5 top-level scope tags corrected on S4/S6/S7/S14/S15 + cascade inherit-parent fixes (`85190db`, `c3f8e0d`, `f3e1956`, `2bb5528`)
- Phase 2 audit applied — sections tagged in ESSENTIALS, SESSION_SETUP, HANDOFF_PROCESS, ENVIRONMENT (`fd96b5a`, `8a25a19`, `bcd0c36`, `b533d12`)
- ADR-29 amendment — file-level scope tag for LESSONS, [scope: X] inline format for new entries (`b0df750`, `296767a`, `8013d9c`, `496c9f0`)
- ADR-27 amendment — commit-time enforcement prescription (ratio-aware, `aec1a4b`); validator implementation (`b54cddd`); unit tests (`3987348`); ruff + decimal precision fixes (`c02e57e`, `9ea94d3`, `8c5ea66`)
- Stream A CLOSED — gap report marked complete, lessons extracted (`19d6516`, `f0702f2`)
- LESSONS 50-entry split deferred with rationale (`eaf3f53`); 2026-04-21 inventory marked SUPERSEDED (`b940661`); ADR-27 filename simplified (`722960b`); handoff/ → handoff-prompts/ rename (`a65b495`)
- README user-first rewrite reflecting post-Stream-A state (`093d545`)
- ccusage tool adopted — TOKEN-LOG snapshot (`2fe0b99`); ENVIRONMENT documentation (`c6f3351`); PLAYBOOK reference (`6db896f`)
- TOKEN-LOG cadence formalized (`eb7cc03`, `7d6e51a`); TOKEN-LOG order flipped to newest-first matching CHANGELOG convention (`43eb577`, `7d8219a`)
- ESSENTIALS data sanitization rule for lessons (`8605202`); validator rename-collision lesson + file-level tag pattern lesson (`717d649`)

**Failed:**
- Validator rename collision: handoff/ → handoff-prompts/ rename initially broke validator's path resolution. Fix: file-level tag pattern documented as workaround, lesson appended.
- Original ADR-27 prescription was flat 25% blocking; turned out to cause "stuck above ceiling" failure mode. Amended to delta-rule (blocks regressions only).

**Next:**
- Stream B scope mapping (became 2026-04-25 marathon)
- Per-Scale Stream B gap implementation

(refs: `docs/audits/2026-04-24-stream-a-gap-report.md`; ADR-27 amendment; ADR-29 amendment; CHANGELOG entries 2026-04-24)

---

### 2026-04-23 | corp-monorepo Scale L operating model audit

**Did:**
- corp-monorepo Scale L operating model analysis audit (`54c9644`, see `docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md`)
- Audit extended with AI Council integration analysis, ADR-27 collision flag, naming conventions deviation, VS Code workspace findings (`a29b0d9`)

**Failed:**
- (none recorded)

**Next:**
- Apply Stream A scope tagging per audit findings; Council #28 + #29 follow-up

(refs: `docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md`)

---

### 2026-04-22 | ADR-27 + ADR-29 created + validator scaffolding

**Did:**
- ADR-27 Council #27 scope tagging architecture (binding, Council 4/5 consensus, Option A) — five tag values dev/llm/hybrid/runtime/meta, pre-commit enforcement, evidence-triggered reopening (`b878cce`, see `docs/decisions/ADR-27_scope-tagging.md`)
- ADR-29 LESSONS.md grandfathering (binding, derivative of ADR-27) — existing entries untouched, [scope: X] inline field on new entries (`00e4467`, see `docs/decisions/ADR-29_lessons-grandfathering.md`)
- CHANGELOG sync 2026-04-21 ADR-27 + ADR-29 (`f0bc0e3`)
- `validate_scope_tags.py` validator created (`42588b3`); pre-commit config + `requirements-dev.txt` (`1acdf84`)
- CLAUDE.md scope tags section + all sections tagged as meta (`2a048b4`); README sections tagged as meta (`d106c78`)
- CHANGELOG vocab + hook + self-tag entry (`29c867e`)

**Failed:**
- (none recorded)

**Next:**
- Phase 2 audit — section-level tagging across all `.dev-knowledge` files
- corp-monorepo audit (became 2026-04-23 work)

(refs: ADR-27; ADR-29; CHANGELOG entries 2026-04-22)

---

### 2026-04-21 | Tech radar + Council #27 + dev-knowledge architecture redefinition

**Did:**
- Tech radar handoff (`b297677`); ESSENTIALS handoff process expanded with template (`8f99f9b`); HANDOFF_PROCESS.md extracted as dedicated file (`a704aaf`, `1bc115a`); redundant codex-review stub removed (`4a22305`); handoff prompts extracted to dedicated files (`588e4d4`); /handoff renamed to /session-summary (`a5330fe`) avoiding naming conflict
- `.dev-knowledge` inventory audit (`2fd99c5`, see `docs/audits/2026-04-21-dev-knowledge-inventory.md`)
- Phase 2 scope tagging audit — 63 sections classified across 8 primary files; distribution: 14% dev, 22% llm, 21% hybrid, 8% runtime, 35% meta (`0395a04`, see `docs/audits/2026-04-21-dev-knowledge-scope-tagging.md`)
- Council #27 brief — 3 architecture options with decision matrix (`bd0c9bb`); Option 0 added with honest LESSONS framing + matrix caveat (`2f287a6`)
- 2026-04-21 session handoff with dev-knowledge redefinition (`25808c3`)
- ADR-28 three-layer architecture (descriptive — browser → `.dev-knowledge` → projects) added to PLAYBOOK System Architecture section (`695e54c`, `0704f06`); Section 12 cross-ref (`4ace660`); CHANGELOG entry (`40a857d`)
- 2 process lessons appended — browser-as-tutor defaulting violates three-layer (`fbf0863`); session-level lessons (`906b61c`)
- S15 + ESSENTIALS + CHANGELOG codex-review automation update (`9b5785a`)
- Codex review for smoke-test added then deleted (`88aa66a`, `49d6647`)

**Failed:**
- Codex review smoke-test audit added then deleted same-day — premature artifact, pattern not yet stable. Deleted before any consumers.

**Next:**
- ADR-27 from Council #27 (became 2026-04-22 work)
- ADR-29 LESSONS grandfathering (Council #27 raised this open question)
- Validator implementation (Phase 2 enforcement)

(refs: `docs/handoffs/2026-04-21-dev-knowledge-architecture-redefinition.md`; `docs/handoffs/2026-04-21-tech-radar-session.md`; `docs/audits/2026-04-21-council-27-brief.md`; ADR-28)

---

### 2026-04-15 to 2026-04-17 | Codex/Tach/Opus 4.7 tooling adoption + handoff workflow formalization

**Did:**
- Codex CLI installed (ChatGPT Plus, GPT-5.4 default); AGENTS.md created in corp-monorepo (severity calibrated, two review modes); `/review` slash command in `~/.claude/commands/review.md`
- PLAYBOOK Section 15 Cross-Tool Review [L+M] added; Section 16 Code Quality Audit Process [L only] added
- ESSENTIALS updated with monthly Codex audit + Codex review step in "Ending a Session"
- Opus 4.7 + xhigh effort level added to ESSENTIALS (`a6f7a10`) and PLAYBOOK prompt template (`5168c64`)
- 3 Tach adoption lessons appended to LESSONS.md (`beaecfb`)
- ENVIRONMENT.md updated with Opus 4.7 and new settings (`ef0ae1e`); .claude/settings.local.json gitignored (`567ed61`)
- 2026-04-15 session handoff added (`0e999e7`); handoff workflow formalized in ESSENTIALS (`9a17db3`); verified handoff step (`615e116`); verified tech radar session handoff added (`1ba8a05`)

**Failed:**
- Magistrala verification deferred (pipeline still unverified end-to-end since Council #24 MyWork restructure)
- One A/B test deferred (per session handoff status)

**Next:**
- Tech radar continuation (became 2026-04-21 session)
- Handoff process refinement (became 2026-04-21 work)
- Magistrala verification (carried as standing follow-up)

(refs: `docs/handoffs/2026-04-15-codex-tach-opus47-session.md`; `docs/handoffs/2026-04-15-tech-radar-session.md`)

---

### 2026-04-14 | Dev practice OS state audit

**Did:**
- Audit of dev practice OS state after 2026-03-30 session (`4ba0513`) — point-in-time snapshot before tooling evaluation work begins

**Failed:**
- (none recorded)

**Next:**
- Tooling evaluation (Codex CLI, Tach, Opus 4.7) — became 2026-04-15 session

(refs: commit `4ba0513`)

---

### 2026-03-30 | Repo creation — initial scaffolding + same-day expansion

**Did:**
- Initial commit — dev practice knowledge base scaffolding, 9 files (`b635615`)
- `.claude/` project config with git-discipline rule and `/save` command (`583f335`)
- Codex review step added to ESSENTIALS.md "Ending a Session" (`2f70713`); Section 15 Cross-Tool Review added to PLAYBOOK (`d6bfddb`); Codex review integration spec (`73e8a9a`); 5 Codex audit lessons appended + Section 16 added to PLAYBOOK + ESSENTIALS updated (`343abdf`)
- Project Scale Tier system added to PLAYBOOK (`0741aeb`); tier tags applied to scale-dependent sections (`665ff14`); post-structural-change documentation rule with tier scaling (`3f186be`); ESSENTIALS Project Scale Tier reference (`fe0d6ca`); LESSONS Project Scale Tier lesson (`9a3f25f`)
- AGENTS.md template with L and M scale variants (`f34dc7a`); TODO management lesson (`dd58836`)

**Failed:**
- (none recorded — initial creation session)

**Next:**
- Dev practice OS state audit (became 2026-04-14 standalone)
- Tooling evaluations (Codex CLI, Tach, Opus 4.7)

(refs: 13 commits 2026-03-30; initial commit `b635615`)
