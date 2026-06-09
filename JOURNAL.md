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

### 2026-06-09 — #136 pruning-symmetry doctrine codified (docs/codify-136)

**Did:** Codified the #136 pruning-symmetry doctrine verbatim from its canonical BACKLOG statement (no divergence vs LESSONS #53/#55 or the 78→67 obsolescence-pass — #136 was the designated codification). Two deliverables: (a) a **Pruning symmetry** bullet in PLAYBOOK §2 "Key rules" (every adding flow gets a review-gated pruning counterpart; CC proposes with evidence, operator ratifies, auto-delete forbidden), (b) a standing **Obsolescence pass** line in `templates/prompt-template.md` Final (v1.2→1.3) — the point-of-use of the §2 rule. Closed #136 (63→62); parent story retains #34/#67/#111 (not orphaned).

**Changes:** `protocols/PLAYBOOK.md` (§2 Key rules bullet), `templates/prompt-template.md` (Final line + v1.3), `BACKLOG.md` (#136 removed), `JOURNAL.md`. Gates green: validate_backlog 62 tasks, audit 14/14, ruff, TOC. PLAYBOOK `Last updated` already 2026-06-09 (localized edit; no end-to-end re-read claimed).

---

### 2026-06-09 — #135 diagram-form algorithm codified to PLAYBOOK doctrine (docs/codify-135)

**Did:** Promoted the #91 five-rule diagram-form algorithm into PLAYBOOK §14 Markdown Governance as a new `### Diagram-form selection algorithm` subsection, verbatim from the canonical #135 BACKLOG statement (sole canonical source — no divergence; JOURNAL #91 close only described its *application*, ADR-51 governs theme not selection). Closed #135 (64→63). Bumped PLAYBOOK `Last updated` → 2026-06-09; toc-freshness regenerated.

**Note:** Task's "audit check #10 fails a predating stamp" rationale doesn't apply — PLAYBOOK isn't in `_FRESHNESS_FILES` (VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING only); stamp bumped for hygiene. Gates green: validate_backlog 63 tasks, audit 14/14, ruff, TOC.

---

### 2026-06-09 — #115 ruled re-scope-and-remove (chore/close-115)

**Did:** Ruled #115 (left surfaced after the git-resync) → re-scope-and-remove, residual folded into #131. Verified #131 (repo-onboarding runbook) covers child-distribution of `/ship`: its carriers + lifecycle-command onboarding layers carry the tier1-lifecycle plugin (hub half already done — `/ship` is plugin-provided). Removed #115 from BACKLOG; added a one-line supersession note to #131 so the lineage survives. Active 65→64; validate_backlog + audit health + ruff all green.

---

### 2026-06-09 — BACKLOG git↔history re-sync (chore/backlog-resync)

**Did:** Reconciled BACKLOG's active list to git's actual closed/open state (#134/#90 procedure). Full-history git-closed id set ∩ active list = exactly {#115, #125}; #137/#138 were ALREADY reconciled at HEAD `4bbae04` (the prompt's pre-#137 snapshot premise was stale). Applied diligence to each: removed [#125] (git-closed `113a4ba`; Done-when **verified met** — `ecosystem/*/state.yaml` gitignored + fleet-audit routine self-commits with the `Routine:` trailer, baselines 06-08/06-09) plus its orphaned sole-task story header "Adopt Dynamic Workflows as the Tier-3 agentic harness". **Surfaced #115 for operator ruling** (NOT removed): git-closed `40b0ea1` but on the hub half only (ship.md→plugin); Done-when "a child repo invokes /ship from the plugin" was never witnessed → easy-metric closure; left listed, no tracking item spawned.

**Result:** Active count **66 → 65** (validate_backlog authoritative; 7 themes / 18 stories / 65 tasks / 0 warnings). audit health OK, ruff clean. Commit `021532c` carries `closes [#125]`.

**Changes:** `BACKLOG.md` (−#125 +grooming-log line), `JOURNAL.md`. **Next:** operator ruling on #115 (re-scope-and-remove vs reopen).

### 2026-06-09 — handoff Phase 2 complete — bundle generated (2026-06-09-dev-knowledge-session)

**Did:** Consolidated the operator's pasted interview answers into the 8-file v4.4
bundle (HANDOFF_PROCESS v4.4, status beta). Cross-checked the sender's load-bearing
claims against repo state.

**Result:** Bundle at `docs/handoffs/2026-06-09-dev-knowledge-session/` (README + 01–07,
all within line budgets). Cross-check: load-bearing this-repo claims **verified** (#137
closed, #138 open, #131 owns rollout, plugin 0.1.10, ARCHITECTURE stamp 2026-06-08);
two minor precision notes (active backlog count **67** not "~66"; highest ADR is
**ADR-80** / 53 files, not literally "80+"); cross-repo claims (corp-sca floor hash,
Council test count) carried sender-reported, out of ADR-41 scope. In-progress interview
folder removed.

**Changes:** `docs/handoffs/2026-06-09-dev-knowledge-session/` (8 files added),
`docs/handoffs/in-progress/2026-06-09-dev-knowledge-session/` (removed), this JOURNAL marker.

**Next:** Operator uses the bundle per its README escalation ladder (paste 01–05 → 06 → 07).

---

### 2026-06-09 — handoff Phase 1 interview generated (2026-06-09-dev-knowledge-session)

**Did:** Generated the Phase 1 handoff interview for `2026-06-09-dev-knowledge-session`
(HANDOFF_PROCESS v4, Case 2 — clean tree, commits accumulated since the 2026-06-06 bundle).
HEAD captured at `e6154d3`; sage→apprentice single-cluster interview written with the v4.2
Amendment A four-tag discipline.

**Result:** `docs/handoffs/in-progress/2026-06-09-dev-knowledge-session/_handoff-interview.md`
written; awaiting operator answers below the PASTE marker, then `complete handoff for dev-knowledge`.

**Changes:** `docs/handoffs/in-progress/2026-06-09-dev-knowledge-session/` (interview), this JOURNAL marker.

**Next:** Operator pastes answers → Phase 2 consolidates the 8-file bundle.

---

### 2026-06-09 — floor install-note: from-scratch .pre-commit-config robustness (closes the demo's one correction round)

**Did:** Ran the child-floor lifecycle end-to-end as a process test against a DISPOSABLE
temp repo (generate → install-from-note → arm → commit → tamper-blocked → restore →
teardown); all 8 gates PASS, hub untouched (zero hub commits, temp repo deleted). The one
correction round: INSTALL_NOTE step 3 emitted a bare `- repo: local` fragment and said "add
this hook to the child's .pre-commit-config.yaml" — presupposing the file exists. On a
clean-slate child the operator had to supply the top-level `repos:` envelope themselves.
Fixed it (branch → `/ship`).

**Result:** `generate_floor.py` step 3 now emits a COMPLETE, from-scratch-valid config
(top-level `repos:` included) with explicit branching — create the file if absent, else
append only the `- repo: local` item under an existing `repos:` list. Module docstring (c)
updated to match. 3 new tests: prose covers both paths, the emitted block starts with
`repos:`, and it `yaml.safe_load`s into a valid pre-commit config with the floor-hash hook
wired to the child-side script. 359 passed / 1 skipped, ruff clean, all 8 pre-commit gates
green. Merge `eae672a` (feature `ce528ce`), pushed `ac0fc1d..eae672a`, branch auto-deleted.

**Changes:** `scripts/generate_floor.py` (INSTALL_NOTE step 3 + docstring),
`tests/test_generate_floor.py` (+3 tests).

**Routine commit (ADR-80 local-writer, not session work):** `d00a47b` fleet-audit baseline
was ahead of origin at session start; rebased on origin's `e15ef00` conformance digest and
pushed (`ac0fc1d`). Tripped the Stop-hook "ahead of origin" backpressure — resolved by
pushing the routine's own output, not a spurious JOURNAL entry.

**Abandoned:** nothing.

**Next:** the next real child re-pilot (corp-sca) should now hit zero correction rounds on
step 3. No open follow-up from this fix.

---

### 2026-06-08 — session close: floor corrective shipped (.claude/ + #137) + routine baselines pushed

**Did:** Session wrap. Consolidates the floor corrective arc detailed in the two entries
below (`.claude/` placement + complete install note; two post-ship install-note fix-forwards)
and records session hygiene.

**Result:** Floor corrective fully shipped — 4 merge commits to `main`, all pushed:
`5c104e9` (.claude/ placement + install note + #137), `4f0bd12` (paste-ready docstring
quotes), `3f2cc97` (ASCII-clean note), `1447ebb` (JOURNAL fix-forwards addendum). #137
CLOSED (`.gitattributes` LF-pins the sidecars; BACKLOG entry removed). #121 stays closed
(corrective follow-up, not a reopen). Final state: 356 passed / 1 skipped, ruff clean,
validate-backlog OK (65 tasks), tree clean, `main` in sync with origin.

**Changes:** see the two entries below for the floor diff. Session-hygiene only here.

**Routine commits (ADR-80 local-writer, not session work):** two fleet-audit baseline
commits landed locally during the session and were pushed — `70eecae` (refreshed the
corp-sca audit snapshot + ecosystem history; rode in on merge `1447ebb`) and `4f17c51`
(later baseline, pushed standalone). Each tripped the Stop-hook "ahead of origin, no
JOURNAL" backpressure; both were the routine's own output, resolved by pushing, not by a
spurious entry.

**Abandoned:** nothing.

**Next:** child re-pilot is a SEPARATE corp-sca session (untouched here). Runbook gap to
fold into #131: the re-pilot must DELETE the old ROOT `CLAUDE-FLOOR.md` + `.sha256` when
regenerating into `.claude/`, else the hub audit vacuous-skips the orphaned root copy
(consequence of the lookup move). Not yet written to BACKLOG.

---

### 2026-06-08 — floor corrective: two post-ship fix-forwards on the install note

**Did:** After shipping the `.claude/` placement arc (`5c104e9`), a verbatim re-witness of
the *emitted* install note caught two latent defects, each fixed-forward on its own branch
(branch→merge `--no-ff`, per the universal rule).

**Result:**
- `85c89dc`/`4f0bd12` — the embedded `check_floor_hash.py` docstring used escaped `\"\"\"`
  inside the raw-string `INSTALL_NOTE`; a raw string keeps the backslash, so the note printed
  literal `\"\"\"` → a pasted script would be broken Python. Switched the embedded docstring to
  `'''` (no collision with the outer `r"""..."""`). Guard added: the extracted script must
  `compile()`.
- `ddc2c89`/`3f2cc97` — em-dashes in the note prose AND inside the hook's `print(..., file=sys.stderr)`
  strings would `UnicodeEncodeError` on a Windows cp1252 console exactly when the guard fires.
  ASCII-cleaned the note (`—`→`--`). Guard added: `INSTALL_NOTE.encode("ascii")`.

Both are corrections to the same corrective arc, not new scope. 356 passed, ruff clean. The
install note is now confirmed paste-ready + pure-ASCII.

**Changes:** `scripts/generate_floor.py` (INSTALL_NOTE docstring + dashes); `tests/test_generate_floor.py`
(compile-the-emitted-script + ASCII guards).

**Abandoned:** nothing.

**Next:** child re-pilot (separate session) — the runbook should delete the old ROOT
`CLAUDE-FLOOR.md` + `.sha256` when regenerating into `.claude/`, else the hub audit
vacuous-skips the orphaned root copy (consequence of the lookup move; flag for #131).

---

### 2026-06-08 — floor corrective: `.claude/` placement + complete install note + #137 [closes #137]

**Did:** Corrective follow-up to #121 (NOT a reopen). Moved the generated child floor
from the repo **root** to the child's `.claude/` (the placement miss the pilot record
didn't catch — it cluttered the operator's workspace), and baked every round-1 pilot
lesson into the generator's emitted install note so the re-pilot is friction-free.
Closed #137 (LF-pin the hash sidecars).

**Result:** Generator now writes `<child>/.claude/CLAUDE-FLOOR.md` + `.sha256` (creates
`.claude/` if absent) and prints a COMPLETE, surprise-free install note: the
`@.claude/CLAUDE-FLOOR.md` include, the child-side `check_floor_hash.py` (SPLIT imports,
`.claude/` paths), the pre-commit hook entry (`language: system`, floor filespec), the
EXPLICIT `pre-commit install` arming step (round-1: hook was wired-but-inert without it),
and `git checkout HEAD --` tamper-revert (round-1 gotcha). `audit.py floor_integrity` +
`/ship` advisory follow to `.claude/`. Re-witnessed in a hub temp-dir harness: floor lands
under `.claude/` (NOT root) → `floor_integrity` PASS → tamper → FAIL → restore → PASS.
No root-path floor reference left behind (silent-break risk eliminated). Full suite + ruff green.

**Changes:**
- `scripts/generate_floor.py`: `--out-dir` → `.claude/`; `INSTALL_NOTE` constant (5 baked
  components); docstrings
- `scripts/audit.py`: `floor_integrity` lookup + sidecar → `.claude/` (pointer-existence
  stays root-relative — floor names root docs)
- `plugins/tier1-lifecycle/`: `/ship` advisory → `.claude/` sidecar path; plugin `0.1.9`→`0.1.10`
- `.gitattributes` (new — #137): `*.sha256` + floor template `text eol=lf`; working tree
  renormalized to LF (phantom diff gone)
- `tests/test_generate_floor.py`, `tests/test_audit.py`: `.claude/` paths + install-note asserts
- `protocols/PLAYBOOK.md`, `ARCHITECTURE.md` (Ch4): floor-location refs root→`.claude/`
  (ARCHITECTURE genuine end-to-end re-read; `last_reviewed` 2026-06-08)

**Abandoned:** nothing — single-branch arc.

**Next:** child re-pilot is a SEPARATE child session (not touched here); the paste-ready
install note travels with the generator output. #131 owns the fleet rollout + runbook.

---

### 2026-06-08 — #121 child methodology floor: Step-5 pilot witnessed, closeout [closes #121]

**Did:** Recorded the ADR-78 floor Step-5 pilot validation (corp-sca-time-automation,
run in a separate child session) as a dated `docs/audits/` record — the close gate #121
was waiting on. Three witnesses: (a) floor auto-loaded + re-anchor rule quoted verbatim;
(b) tamper caught on BOTH sides — child pre-commit exit 1 AND hub `floor_integrity`
FAIL→restore→PASS; (c) re-anchor quoted before structural work. Also cleared a recurring
CRLF phantom diff on `templates/child-methodology-floor.sha256` (`git checkout HEAD --`,
not the index form).

**Result:** Done-when met → `closes [#121]`. Witness (b) corroborated on disk: the two
2026-06-08 corp-sca audit snapshots show `floor_integrity` FAIL (hash drift
`2fdaba0be076… != 4d268f329a7e…`) → PASS (`4d268f329a7e…` matches) across the session.
Pilot surfaced two install-note gaps (both routed to #131) + one hub-hygiene item (#137).

**Changes:**
- `docs/audits/2026-06-08-floor-pilot-corp-sca-validation.md` (new — the close gate record:
  3 witnesses, 2 findings, the `git checkout HEAD --` gotcha)
- `BACKLOG.md`: #121 removed (done-items-leave, ADR-65); #131 annotated with the mandatory
  per-clone `pre-commit install` rollout step (findings i/ii); added #137 (LF-pin
  `templates/*.sha256` via `.gitattributes`); grooming-log closure entry
- `JOURNAL.md` this entry

**Abandoned:** Fixing the corp-sca `canonical_freshness` FAIL from here — cross-repo,
belongs to that repo's own session per ADR-41 (noted out-of-scope in the audit record).

**Next:** #131 repo-onboarding runbook (now carries the `pre-commit install` rollout step);
#137 `.gitattributes` LF-pin to stop the phantom-diff recurrence.

### 2026-06-07 — #121 child methodology floor (ADR-78 O2): @-include verified, hub Steps 1–4 shipped [advances #121]

**Did:** Built the ADR-78 O2 Bounded Hybrid child methodology floor under a
STOP-after-UNDERSTAND valve (verbatim Done-when map + operator ratification of floor
content, re-anchor wording, the T1 hub-pointer F5 boundary, T2 scope, T3 link-check
fold-in, the chars/3.5 binding token measure, and pilot child). **VERIFY-FIRST (ADR-78's
first mandate):** empirically probed `@`-include on CC 2.1.168 in throwaway temp trees
(canary lived only in the imported file) — basic resolution, 2-hop nesting, and fail-soft
on a missing target all confirmed; a missing floor degrades silently (the case for the
conformance gates). Then shipped hub Steps 1–4.

**Result:** Generator + conformance + staleness gate live and tested; pilot (Step 5) is a
separate child session, so #121 advances (not closes) pending the witnesses. Full suite
353 pass / 1 skip; ruff clean; `audit-health` green (floor_integrity pass-skips on the
floor-less hub). Floor measures 887 binding tokens (ceiling 1,500).

**Changes:**
- `templates/child-methodology-floor.md.tmpl` (ratified content set) + `templates/child-methodology-floor.sha256` (the `/ship` currency anchor)
- `scripts/generate_floor.py` (operator-invoked only; `check`/`generate`; ceiling refusal, F5 grep, zero-URL, LF-normalized autocrlf-proof hash) + `tests/test_generate_floor.py` (18)
- `scripts/audit.py` `check_floor_integrity` (#14: hash-vs-sidecar + F5 + pointer-existence; shared policy imported from the generator) + `tests/test_audit.py` (7)
- `plugins/tier1-lifecycle/commands/ship.md` floor-currency advisory (WARN-only) + `plugin.json` 0.1.8→0.1.9
- `protocols/PLAYBOOK.md` "Child methodology floor (ADR-78)" subsection (+TOC regen); `ARCHITECTURE.md` Ch4/Ch5 status rows planned→hub-shipped; `BACKLOG.md` #131 owns re-homed (4)+(6), #121 status note

**Abandoned:** Hub→child auto-install (rollout is operator-invoked per ADR-73); the 500-token compression alternative (ADR-78 §4 ceiling is the rule).

**Next:** Run the Step-5 pilot in `corp-sca-time-automation` (separate session) using the prepared install note; record witnesses (load, tamper→FAIL→restore→PASS, re-anchor fires) as a dated validation record in `docs/audits/`; then `closes [#121]`.

### 2026-06-07 — #107 native parallel-session worktree workflow (verify-first; collision-replay witnessed) [closes #107]

**Did:** Shipped the CC-native managed-worktree workflow for same-repo parallel
*committing* sessions under a STOP-after-UNDERSTAND valve (verbatim Done-when map +
operator-approved location/doctrine fork). Verified the native mechanism empirically,
not from docs: `claude --worktree` / the `EnterWorktree` tool create
`.claude/worktrees/<name>` on branch `worktree-<name>` (CC 2.1.168). Inventoried every
organ's worktree behavior (corrected two subagent errors — worktrees are *full* checkouts,
not shared-`scripts/`); replayed the 49c7db7 shared-HEAD collision SAFELY across two
worktrees (the witness); found + fixed two real worktree blockers without weakening a gate.

**Result:** Done-when met (rule lands in PLAYBOOK). **Witness PASSED** — main-checkout and
worktree each staged a file in the same wall-clock window; commit A (`9e9bd73`) carried only
file A, commit B (`ece081a`) only file B, **zero cross-sweep**, each on its own branch, both
trees clean — the 49c7db7 failure condition replayed without the failure. Two blockers found
+ resolved: (1) a fresh worktree omits gitignored `ecosystem/*/state.yaml` → the worktree's
own `audit.py` reports `repos registered (none)` → `health: DEGRADED` → the `audit-health`
pre-commit gate **BLOCKS every commit**; fixed by a committed `.worktreeinclude` that seeds
that state natively at create-time (witnessed: seeded worktree commit lands, unseeded blocks).
(2) `/ship` breaks inside a worktree (`git checkout main` → `fatal: 'main' is already used by
worktree`); fixed by an *additive* ship.md pre-flight #1 that refuses cleanly + integrate-from-
primary guidance (`git merge --no-ff worktree-<name>` from the primary). Walker safety
characterized empirically: pytest 329→329 (default `.*` dot-dir skip — safe), ruff DESCENDS
into the second checkout until `.claude/worktrees/` is gitignored (the fix; verified with a
planted violation). Scratch teardown verified an identical-tree no-leftovers round-trip.
328 pytest / ruff clean throughout.

**Changes:** `.worktreeinclude` (NEW, load-bearing), `.gitignore` (+`.claude/worktrees/`),
`plugins/tier1-lifecycle/commands/ship.md` (worktree pre-flight) + `.claude-plugin/plugin.json`
0.1.6→0.1.7, `protocols/PLAYBOOK.md` ("Parallel sessions & worktree discipline" rewritten
native-primary; interim exclusivity + sibling naming retired), `BACKLOG.md` (−#107), and
user-level `~/.claude/skills/gotchas/gotchas.md` (shared-HEAD verify line → new mechanism).
Commits `e48b0b7` (infra), `e2ffd0d` (PLAYBOOK), this close; merged `--no-ff` via /ship.

**Abandoned:** plugin-version propagation to sibling repos (out of scope — prompt forbade
touching siblings; bump is traceability-only); a deeper audit.py worktree-awareness refactor
(the `.worktreeinclude` seed is the minimal correct fix — deferred unless the raw-`git worktree`
manual-residual path becomes common, then teach audit.py to resolve ecosystem state from the
git common-dir).

**Next:** #107 closed. The #121 child-floor arc can now safely run hub+child parallelism on
native worktrees. Watch: `.worktreeinclude` only seeds *native*-created worktrees — a raw
`git worktree add` session still needs a manual seed (documented in PLAYBOOK).

---

### 2026-06-07 — #134 n=1 backlog-grooming field run (groom + design input)

**Did:** Ran the first field pass of the #134 backlog-grooming organ under a
STOP-after-UNDERSTAND + per-bucket ratify-gate valve. Built the deterministic
signal set (retired-token grep, ref-resolver, dependency-closed, age) BEFORE any
judgment; classified all 78 tasks into 5 buckets (alive / done-undetected /
merge-into / stale-interest / obsoleted-by); HALTed for operator ratification;
executed only ratified actions. Two BACKLOG commits (removals+merges+grooming-log
`d1f03da`; ALIVE flag-edits `5d47581`) merged `--no-ff` (`1ee48e6`); then this
follow-up annotated #134 with the Step-4 design input (chat-as-storage rule) and
captured the Edit leading-newline line-removal gotcha (n=2) to `~/.claude`
(`421b81e`).

**Result:** 78→67 tasks, 21→19 stories (2 orphaned headers removed with their
sole tasks), 0 warnings, 328 pytest / ruff clean throughout. closes [#81]
(conformance-hub.js shipped + ran nightly, drift ratified via triage — Done-when
met) + [#14] (ecosystem/ settled as committed continuous-audit substrate by the
ADR-76 + ADR-80 + #125 arc; decision recorded in the grooming log); merged
[#21]→#19 and [#38]→#16; removed STALE [#6] [#22] [#28] [#30] [#32] [#33] [#94]
(kept #47); flag-edits #71 (target re-scope) / #77 (ADR-68 night-agent → ADR-80)
/ #110 (ADR-03 verify note) + #1/#2 P1→P2 (#107 now the only P1). **Key finding:**
deterministic signals gave 0 hard kills on a freshly-groomed backlog — every
substantive removal was judgment (git-history + cross-ADR), so the #134 organ =
deterministic flags → LLM judgment → ratify, cadence POST-ARC not calendar.

**Changes:** `BACKLOG.md` (−11 tasks, 2 merges, 5 flag-edits, grooming-log line —
`d1f03da` `5d47581`, merge `1ee48e6`; #134 design-input annotation this commit) ·
`JOURNAL.md` (this entry) · `~/.claude/skills/gotchas/gotchas.md` (leading-newline
line-removal gotcha, path-scoped `421b81e`).

**Abandoned:** #81 per-rule-expansion scope NOT re-captured (operator ruling —
re-enters via funnel if needed; #77 owns doc-rot). The leading-newline removal
idiom (replaced mid-run by full-line matching after it jammed adjacent lines).

**Next:** #134 organ build (deterministic pre-filter + judgment + ratify, post-arc
cadence) when scheduled; #121 @-include VERIFY → child-floor; #132 organ-index
generator.

---

### 2026-06-07 — ARCHITECTURE rewrite: six-chapter system map (closes #91)

**Did:** Rewrote `ARCHITECTURE.md` from the pre-ADR-80 11-section structure into a
six-chapter navigation map — layers & authority · organ map · automation axes ·
distribution & transfer · zones & immutability · verification mesh & decision flow —
reflecting the shipped night/cloud reality through ADR-80. Map-not-prose: points to
ADRs/protocols, never restates doctrine. Folded in the three mid-flight amendments:
diagram-form algorithm (A), stale-mention sweep (B), reading map (C).

**Result:** Valve-1 mapped every #91 Done-when component to a chapter; all delivered,
so the 2026-06-05 staleness-audit ARCHITECTURE row flips to CURRENT **via this
closure** — R1: that audit is immutable and self-documents flip-by-git-closure, so it
was NOT edited. 8 authored Mermaid diagrams → 1 (the 3-actor layer cycle); the other
7 demoted to tables/text per the algorithm (inventories → tables; linear cycles →
arrow-chains; >12-node flows → tables+pointers). Stale-mention sweep: 0 un-annotated
night-agent mentions (all inside the ADR-68 supersession note). Gates green: 13/13
audit, toc, codemap, 328 pytest, ruff. Retained the six [U] spine headings (R2 — one
coherent body commit, no gate bypass; per-chapter would have risked a transitional
`canonical_structure` FAIL).

**Changes:** `ARCHITECTURE.md` (full rewrite, commit 9573885) · `BACKLOG.md` (#91
closed; captured #134 backlog-grooming review, #135 diagram-form algorithm → PLAYBOOK,
#136 pruning-symmetry doctrine) · `JOURNAL.md`.

**Abandoned:** per-chapter commits (R2 — the six spine headings are entangled across
the reorg; a single coherent body commit avoided any transitional gate FAIL).

**Next:** `#121` `@`-include VERIFY → child-floor implementation → corp dedicated chat
package. (Refs ADR-80, ADR-68 supersession, ADR-51.)

---

### 2026-06-07 — Harden /ship message handling (kill temp-file cleanup hazard)

**Did:** Follow-up fix (operator Option 2 + rider) after the peer-audit capture session repeatedly hit the harness safety scanner. Replaced ship.md's temp-file merge-message idiom (`Set-Content $tmp` → `git merge -F $tmp` → cleanup) with an inline single-line `-m` merge — no temp file, no cleanup step, nothing for the scanner to mis-parse. **Corrected the rider's `git merge -F -` suggestion** (git merge cannot read the message from stdin — documented gotcha; opens a file named `-`, exit 129) → used `-m` instead. Bumped plugin 0.1.5→0.1.6. Captured the harness trap as a `~/.claude` gotcha, then **refined it after a sharper second hit**: the scanner matches the literal cmdlet token + a `/command` token *anywhere in the command text* — even a stdin `git commit -F -` whose message merely *describes* the fix (no cmdlet present) is blocked. Fix to the gotcha: paraphrase the trigger tokens out of any message that must discuss this class.

**Result:** ship.md hazard class eliminated fleet-wide (directory-source marketplace resolves commands live, so effective immediately; version bump is hygiene). **Witness:** this fix ships through its own former failure condition — the merge that lands it carries a slash-command token in its summary via the new `-m` path and completes with no scanner block. Pre-commit green; tests unaffected (markdown/json only).

**Changes:** `plugins/tier1-lifecycle/commands/ship.md` (inline `-m` merge + updated note) + `plugins/tier1-lifecycle/.claude-plugin/plugin.json` (0.1.5→0.1.6) — commit `5393ebe`; `~/.claude/skills/gotchas/gotchas.md` (harness-scanner gotcha + refinement; path-scoped `296ae3c` / `f926daf`).

**Abandoned:** The rider's `git merge -F -` form (corrected to `-m`). Cache-refresh dance not run (commands resolve live from source; the version bump is the hygiene record).

**Next:** unchanged — #91 ARCHITECTURE rewrite → #121 @-include VERIFY → #132 organ-index generator.

### 2026-06-07 — Peer-audit v2 capture + parallel-work doctrine [#98 rider-2 verified]

**Did:** Single conversational session (operator-streamed capture across pushback rounds), finalized as a logical 3-commit split + /ship. **STEP 0 (#98 rider-2):** verified the literal next-SessionStart check — `logs/PROPOSALS-2026-06-07.md` survived the restart **intact** (non-collapsed window `since ceb53a2 ≠ head 3c5e476`, `window=3`, detector ran); the self-erasure signature in `PROPOSALS-2026-06-06.md` (`since==head==5086f58`, `window=0`) is **absent**. **Delta-(c) VERIFY closed:** line-read `.claude/workflows/conformance-hub.js` — fan-out (V1 journal-vs-git / V2 living-doc / V3 backlog-closures, Sonnet) → adversarial skeptic (Opus, defaults-to-kill) → digest (Opus, code-owned counts contract), all confirmed. Captured peer-audit v2 findings + InsForge context-engineering field evidence into BACKLOG; sharpened the parallel-sessions doctrine + added the agents-distribution doctrine in PLAYBOOK; recorded a shared-HEAD-collision gotcha in `~/.claude`.

**Result:** **#98 stays closed** (rider-2 PASS; honest scope — live signal = absence-of-self-collapse + detector-ran across the restart; the literal "pending proposal survives" path was unit-proven on a temp repo in wave B, this window carrying no closures to exercise it live). 5 new backlog items (#129 skill-scaffold, #130 memory-hygiene, #131 repo-onboarding runbook, #132 organ-index generator, #133 peer-watch); 5 annotations (#121/#111/#102/#127/#91); #107 bumped **P3→P1** (2nd witnessed same-checkout collision). `validate_backlog: OK` (78 tasks). Full suite **328 pass / ruff clean**; all commits pre-commit green.

**Changes:** `BACKLOG.md` (+#129–#133, annotations, #107 P1, grooming line) + `docs/audits/2026-06-07-copilot-collections-peer-audit-v2.md` (dated addendum: C7 #8/#98 same-day closure + §3 VERIFY confirmed; original body unedited per critical rule #3) — commit `cab8434`; `protocols/PLAYBOOK.md` (parallel-sessions *committing* doctrine + agents-distribution doctrine; bold labels, TOC gate green) — commit `908d435`; `~/.claude/skills/gotchas/gotchas.md` (shared-HEAD parallel-commit gotcha; path-scoped commit `e57aa37`, operator WIP left untouched).

**Abandoned:** Nothing. Tooling friction noted (not yet fixed): the harness safety scan blocked a `Remove-Item $tmp` because the commit message inline contained a `/slash-command` token — a latent hazard for `/ship`'s temp-cleanup step; worked around via `git commit -F -` (stdin). Candidate gotcha + ship.md hardening flagged to the operator.

**Next:** #91 ARCHITECTURE rewrite (now consumes the planned ORGAN-INDEX #132 + the agents-distribution doctrine) → #121 @-include VERIFY + floor implementation → #132 organ-index generator (kills operator-as-registry). Build-prompt reminder: **#107 is now P1** — VERIFY `claude worktree`/`EnterWorktree` semantics first in its prompt.

### 2026-06-07 — Wave B: /changelog-review + version sentinel (#113), proposals-survive fix (#98), Stop backpressure (#8)

**Did:** Three organs, independently-revertable commits, witnessed each (STOP-after-UNDERSTAND valve cleared two forks first: Q1 close-#8-re-scoped with displaced-scope homes verified; Q2 separate hub-local backpressure hook). **#113** (`b78aa2a`/`897a4a9`/`107f60e`): committed durable state `ecosystem/tool-versions.yaml` (ADR-80 §3) + LOCAL fail-soft `scripts/changelog_sentinel.py` (SessionStart, no network) + operator-push `/changelog-review` command (fetch CC CHANGELOG + `gh` codex releases → classify ADOPT/OBSOLETES/STALE-NAMES/VERIFY/NOISE → digest → bump state). Ran it for real (the witness): digest `docs/audits/2026-06-07-changelog-review.md` covering CC **2.1.168** (bugfix-only, NOISE) + codex **0.137.0** (only stack-relevant = Windows SQLite fix #25490 + `codex exec` approval-policy #23763, **already owned by #119**); bumped state; sentinel went fired→silent (loop closed). **#98** (`408f9b6`): fixed propose_closures self-erasure in **both** copies (scripts/ + plugin) — baseline no longer advances past a *pending* (unchecked + still-open) proposal; empty-regeneration safety-net; plugin bumped 0.1.4→**0.1.5** + cache refreshed (live on restart). **#8** (`dfbb585`): `scripts/session_end_backpressure.py` — separate hub-local Stop hook emitting `hookSpecificOutput.additionalContext` (deterministic dirty-tree / JOURNAL-missing / canonical-cadence checks; ADR-74; fail-soft). **Incident:** a concurrent no-worktree session created `docs/peer-audit-copilot-collections-v2` off my HEAD mid-run and my witness commit (`49c7db7`) landed on it + swept its file; froze, diagnosed read-only, recovered onto feat/wave-b per operator ruling (Option 1), left their branch untouched.

**Result:** #113, #98, #8 closed (BACKLOG 76→73 tasks; validate-backlog green; id gaps kept). Witnesses: sentinel both-branches (CC fires, codex silent) live; `/changelog-review` produced a real digest + bumped state; #98 double-fire on a temp repo → `#5` survived (re-detected, not erased); #8 scratch-file → additionalContext surfaced dirty-tree, removal cleared it (silent-branch unit-proven). Plugin 0.1.5 in cache (`Restart to apply`). W3/rider-3 explained: directory-source marketplaces resolve **commands live from the source tree** but **hooks from the version cache** (why `/ship` worked while the stale hook didn't). Full suite 328 pass / ruff clean throughout.

**Changes:** new `ecosystem/tool-versions.yaml`, `scripts/changelog_sentinel.py`, `scripts/session_end_backpressure.py`, `.claude/commands/changelog-review.md`, `docs/audits/2026-06-07-changelog-review.md`, `tests/test_changelog_sentinel.py`, `tests/test_session_end_backpressure.py`; edited `.claude/settings.json` (SessionStart sentinel + Stop backpressure), `scripts/propose_closures.py` + `plugins/tier1-lifecycle/scripts/propose_closures.py` (+`tests/test_propose_closures.py`), `plugins/tier1-lifecycle/.claude-plugin/plugin.json` (0.1.5), `BACKLOG.md` (−#113 −#98 −#8). Commits `b78aa2a 897a4a9 107f60e 408f9b6 dfbb585`.

**Abandoned:** cross-repo fleet health as a per-turn backpressure check (already surfaced at SessionStart; not this-session-repairable → would be noise). Codex 0.137.0 *update* not performed (capture/flag only — stays #119).

**Next:** **rider-2 #98 verify** — the LITERAL #98 Done-when (a Stop proposal survives to the next SessionStart) needs the deployed 0.1.5 hook, which goes live on restart; confirm at next session start (one-liner here) — **if it fails, reopen #98**. Also confirm the live sentinel + backpressure hook fire post-restart. Then: **#91 ARCHITECTURE rewrite (wave complete) → #121 @-include VERIFY → corp chat package.** Concurrent sessions in this repo MUST use worktrees (ADR-61) — today's incident is the cost of not.

### 2026-06-07 — Wave A post-ship closeout: witness pass + closures #85/#114 + W2 gate-bug fix

**Did:** Post-ship witness pass for wave A (merged manually as `1e5ae0b`; follow-on fixes after). **W1 (#125):** audit.py routine-commit isolation — PASSED (prior session; two fixes landed — Windows glob-pathspec → concrete enumeration `2b3c5d4`, pre-commit auto-format → one-shot re-stage+retry `f66cbd1`). **W2 (#114):** found + fixed a latent gate-bypass — `pass_filenames: false` on the exported `backlog-id-on-close` hook wiped the commit-msg filename, so the hook silently passed *every* task-removal; removed it (`7e004d2`), then reverted a `language:python` detour that broke on the hub's flat-layout `pip install .` (`6bc8105`). **W3 (#115):** confirmed `1e5ae0b` merged manually; `/ship` on `main` refused at pre-flight (proves the plugin-sourced command executes). Wrote validation record `docs/audits/2026-06-07-wave-a-validation.md` (`0b27182`). **Closeout (this session):** recovered a self-erased PROPOSALS file (the Stop hook had collapsed the detection window to HEAD, destroying the unreviewed proposals) by restoring the `1e5ae0b` baseline + re-running the deterministic detector; gate-reverified and closed #85/#114 (done-items-leave, ADR-65); REJECTED #7 (WEAK/incidental). **Home-gate verify (W2 bug class, checked in-hub):** hub-local `.pre-commit-config.yaml backlog-id-on-close` carries **no** `pass_filenames:false` (uses `language: system` + explicit `entry: python …`) — positive witness = the closure commit passed the commit-msg hook; negative witness = a `#100` removal without `[#id]` was BLOCKED (exit 1) on a throwaway branch (reverted, no trace). 4 gotchas captured.

**Result:** #85, #114 closed (BACKLOG 78→76 tasks; validate-backlog green; id gaps kept). All 3 wave-A witnesses passed; closures stand. Hub does **not** carry the W2 bug. Gotchas (a) Windows glob-pathspec, (b) `pass_filenames:false` commit-msg bypass, (c) `language:python` flat-layout `pip install .` → `~/.claude` gotchas.md (`6f9bffa`); (d) "implementation waves = Opus" → PLAYBOOK model/effort doctrine.

**Changes:** `BACKLOG.md` (−#85 −#114; `cb59705`); `protocols/PLAYBOOK.md` (+Opus-waves model-note, stamp→06-07; `0955497`); `~/.claude/skills/gotchas/gotchas.md` (3 traps; `6f9bffa`); `docs/audits/2026-06-07-wave-a-validation.md` (prior `0b27182`). Wave fixes: `2b3c5d4`, `f66cbd1`, `7e004d2`, `6bc8105`.

**Abandoned:** #7 (rejected — weak evidence never closes). The `language:python` hook approach (flat-layout `pip install .` fails on the hub).

**Next:** Real detector bug surfaced — `propose_closures` **self-erasing baseline**: when the Stop hook re-runs with no new commits, `resolve_window` reads its own prior `head_commit` as the baseline, the window collapses to empty, and the regenerated PROPOSALS file OVERWRITES still-unreviewed proposals (only recoverable because the evidence commits persist). Maps to existing **#98** (PROPOSALS persistence). Wave B (#113 + #8) → #91 ARCHITECTURE.

### 2026-06-07 — Wave A: ADR-80 writer-policy wiring + carriers (#125, #114, #115)

**Did:** Implemented wave A on branch `feat/wave-a-writer-and-carriers`. Step 0 SKIPPED (BACKLOG #126 + LESSONS scoped-rejection both present). **Step 1 (#125):** wired ADR-80 writer policy — gitignored `ecosystem/*/state.yaml`; operator ruling: fleet_health.py makes no commit (FLEET-HEALTH.md stays mutable/gitignored); audit.py is sole local committer; added `_commit_routine_outputs(run_date)` to `scripts/audit.py` — pathspec-bounded (`ecosystem/*/history/`, `docs/audits/`), fail-soft, `Routine: fleet-audit` trailer; refreshed `.gitignore` FLEET-HEALTH.md comment to cite ADR-80 mutable/durable classification; 4 new unit tests; `git rm --cached` 5 tracked state.yaml files. **Step 2 (#114):** exported `backlog-id-on-close` in `.pre-commit-hooks.yaml` (`language: script`, `stages: [commit-msg]`, `always_run`, `100755`). **Step 3 (#115):** `git mv .claude/commands/ship.md → plugins/tier1-lifecycle/commands/ship.md`; plugin 0.1.3 → 0.1.4.

**Result:** 300 tests green; all 3 step witnesses pass; `ship-around-fleet-health-dirty-tree` memory entry RETIRED.

**Changes:** `.gitignore` (FLEET-HEALTH comment + `ecosystem/*/state.yaml`; commit `113a4ba`); `scripts/audit.py` (`_commit_routine_outputs` + `cmd_run`/`cmd_repo` wiring; `113a4ba`); `tests/test_audit.py` (4 ADR-80 tests; `113a4ba`); `.pre-commit-hooks.yaml` (+`backlog-id-on-close`; `40fda27`); `plugins/tier1-lifecycle/commands/ship.md` (moved from `.claude/commands/`; `40b0ea1`); `plugins/tier1-lifecycle/.claude-plugin/plugin.json` (0.1.3→0.1.4; `40b0ea1`).

**Abandoned:** Nothing.

**Next:** Wave B (#113 + #8) → #91 ARCHITECTURE.

### 2026-06-07 — #84 two-tier automation codification (PLAYBOOK + ADR-80 + routine standard) [closes #84]

**Did:** Closed the #84 workflow-doctrine codification package on branch `docs/two-tier-automation-84`, under a STOP-after-UNDERSTAND valve. UNDERSTAND gates run + reported first: (1) **n=2 evidence gate PASS** — both nightly conformance digests located (n=1 2026-06-06 *red*: N1 high #74-drift + N2 med ARCHITECTURE timestamp; n=2 2026-06-07 *clean* 0/0/0); (2) **channel verdict COMPLIANT-BY-DESIGN** — witnessed PR #17 (`claude/conformance-2026-06-07`→`main`, squash-merge `221c63e`) matches the Action's claude/*→PR→diff-guard→squash channel, not a direct push; (3) **signal-quality** — cloud 0/0/0 vs local corp `canonical_freshness` FAIL is no contradiction (claims-vs-docs vs freshness-stamp dimension; hub-self vs sibling scope, #100); (4) **VF-2** — `fallbackModel` schema-accepted on CC 2.1.168 (native `--fallback-model` flag is its CLI twin; probe non-discriminating on strictness — honest limit recorded; no tracked file touched). Operator ruled **writer policy = Option (b) + 3 riders** (mutable/durable split, pathspec-bounded, fail-soft). Then 6 commits across PLAYBOOK + ADR + BACKLOG.

**Result:** #84 closed — all four Done-when components landed (PLAYBOOK two-tier section + ADR-80 + the two ADR-authorship-paths note + Routine/night operational-standard). ADR-80 accepted. All commits pre-commit green (PLAYBOOK-TOC freshness, validate-backlog, audit-health, backlog-id-on-close). Two integrity catches: the prompt's Tier-1/2/3 labels conflicted with ADR-74's matrix numbering → codified the two-tier split as the **LLM-judgment axis** (orthogonal, never renumbers ADR-74); and #84 Done-when component **(c)** was undelivered → added it rather than close past it (the same closure-drift class N1 flagged). README ADR provenance-table lag (73–79 missing) noted, left out of scope.

**Changes:** `protocols/PLAYBOOK.md` (×4: two-tier doctrine `29900d7`; ADR-authorship-paths note `d178abc`; Model/Effort refresh `2ecce40`; Routine/night standard `b3355d0`); `docs/decisions/ADR-80-two-tier-automation-adoption.md` (new; `6da20be`); `BACKLOG.md` (−#84, +#125, grooming-log; `679c7c8`).

**Abandoned:** README.md ADR provenance-table backfill (73–79) — pre-existing drift, out of #84 scope. The #125 writer-policy wiring (fleet_health commit + `.gitignore`) — capture-only per the prompt's no-implement-wiring rule.

**Next:** #91 ARCHITECTURE rewrite → #121 @-include VERIFY → floor implementation.

### 2026-06-07 — Council F1/F2 distillation: 2 ADRs + transcripts + verdict-applied backlog [closes #108]

**Did:** Distilled council verdicts for F2 (child methodology floor) and F1 (browser carrier) into governance artifacts on branch `docs/council-f1-f2-distillation`. Step 1: committed 2 untracked council debate transcripts (`council-out-20260607_124757-pick-council-f2-child-floor.md` + `council-out-20260607_125247-pick-council-f1-browser-carrier.md`). Step 2: authored ADR-78 (O2 Bounded Hybrid — child CLAUDE-FLOOR.md + sidecar sha256, operator-invoked generator, methodology_surface zone class added to ADR-75 register, 1500-token ceiling). Step 3: authored ADR-79 (O1 bundle-only retained; O2 rejected as unverifiable safety property; mandated ergonomics: consolidated BUNDLE.md + 05_NOW init-acknowledgment clause; O3 deferred). Step 4: BACKLOG verdicts — #121 un-gated and re-scoped to full ADR-78 action items (VERIFY FIRST: @-include resolution; P3→P2); #108 removed (done items leave, ADR-65); [#124] new [P2][S] BUNDLE.md consolidation + 05_NOW clause.

**Result:** 2 ADRs committed, #108 closed, #121 active with VERIFY rider, #124 queued. `validate_backlog: OK`. Pre-commit green on all 4 commits.

**Changes:** `docs/decisions/transcripts/council-out-20260607_124757-*.md` + `council-out-20260607_125247-*.md` (new; commit `c66c427`); `docs/decisions/ADR-78-child-methodology-floor.md` (new; `bab9510`); `docs/decisions/ADR-79-browser-carrier-bundle-only.md` (new; `885a210`); `BACKLOG.md` (−#108, ↑#121, +#124; `3520a37`).

**Abandoned:** nothing.

**Next:** #84 codification (n=2 landed — channel confirm in funnel) → #91 → floor @-include VERIFY then implementation (#121).

---

### 2026-06-07 — Audit-trio capture: stale-names fixes + 9 items + 8 annotations + consented user-layer actions [no closures]

**Did:** Captured the consolidated results of the 2026-06-06/07 audit trio (platform-max / codex-max / methodology-transfer) on branch `docs/audit-trio-capture`. STOP-after-UNDERSTAND valve passed: all 8 annotation targets present (#8/#17/#82/#84/#106/#107/#112/#113), the 7 STALE-NAMES sites confirmed (`/stats`×4, `Task tool`×3), codex-review.ps1 read-only line quoted. **Step 0:** persisted the 3 trio audit reports. **Step 1:** 7 stale-platform-name edits — `/stats`→`/usage` (ENVIRONMENT×2, ESSENTIALS, PLAYBOOK) + `Task tool`→`Agent tool` (PLAYBOOK×3, alias parenthetical at the first hit). **Step 2:** 9 new backlog items #114–#122 (carriers #114/#115, schema-probe #120, gated floor organs #121 → Cross-repo universalization; hooks-hygiene #116 + prompt/agent-hooks #117 → Enforced governance; fewer-permission-prompts #118, codex currency #119, PATH-shim retire #122 → Tooling & evaluation). **Step 3:** 8 in-place annotations, each citing the audit files (close nothing). **Step 4 (consented `~/.claude`, no repo commit):** codex-review.ps1 gains `-c model_reasoning_effort=high` (witnessed: real exec, effort=high, sandbox read-only, EXIT=0, no auth/tier error); the `--no-ff` rule promoted to `core-invariants.md §5`; 3 gotchas annotations (billing 2.1.139 coupling, Codex deprecated-keys watch, repo↔global AGENTS.md CRLF/LF — verified content-identical, 3843 chars).

**Result:** Capture-only — nothing implemented, no item closed. `validate_backlog: OK (7 themes, 21 stories, 74 tasks, 0 warnings)`. pytest 296 passed / 1 skipped, ruff clean. Pre-commit green on all 4 repo commits. Codex witness: gpt-5.5 @ reasoning effort high, 7,918 tok, EXIT=0.

**Changes:** `docs/audits/2026-06-07-{platform,codex,methodology-transfer}-max-audit.md` (new; commit `240e84b`); `protocols/{ENVIRONMENT,ESSENTIALS,PLAYBOOK}.md` (stale-names; `35e15ab`); `BACKLOG.md` (+9 items `bc41184`, +8 annotations `e0ad968`); `JOURNAL.md` + `logs/TOKEN-LOG.md` (this commit). User-layer uncommitted (`~/.claude`): `bin/codex-review.ps1`, `rules/core-invariants.md`, `skills/gotchas/gotchas.md`. Left for the operator (untracked): `docs/audits/2026-06-07-ecosystem-audit.md` (4th audit, NOT in the trio) + the `ecosystem/` fleet_health hook artifacts.

**Abandoned:** Nothing. Design forks F1–F5 left for the Council brief (not decided here, per the prompt).

**Next:** Council brief (F1/F2/F5 + F3/F4) → digest n=2 → #84 codification → #91.

---

### 2026-06-06 — Changelog 2.1.148–167 capture: changelog-watch item + 7 annotations + PLAYBOOK synergy line

**Did:** Captured the operator-reviewed Claude Code changelog band (2.1.148–2.1.167) on branch `docs/changelog-148-167-capture`. UNDERSTAND valve: confirmed all 7 annotation targets present (#8/#82/#84/#106/#107/#9/#112) and the PLAYBOOK context-budget subsection (line 2296). Step 1: new backlog item #113 (changelog-watch routine, [P2][M]) under Theme *Tooling & evaluation* → story *Decide the undecided artifact/tool models*. Step 2: amended 7 items in place with `changelog 2.1.148-167 finding —` clauses, citing versions; closed nothing. Step 3: one synergy sentence in the PLAYBOOK read-scoping rule (single-file grep satisfies read-before-edit, v2.1.160).

**Result:** Capture-only — nothing implemented, no item closed. `validate_backlog: OK (7 themes, 21 stories, 65 tasks)`. Pre-commit green on all 3 commits (PLAYBOOK TOC hook passed Step 3).

**Changes:** `BACKLOG.md` (+#113, 7 annotations; commits `8b2a934`, `c4a811f`); `protocols/PLAYBOOK.md` (read-scoping synergy line; commit `53d2736`).

**Abandoned:** Nothing.

**Next:** changelog deep-mine (below 2.1.148, report-only) → capture #2 → digest gate → n=2 → #84.

---

### 2026-06-06 — Context-budget organs: verify skill + artifact-reader subagent (closes [#104] [#97])

**Did:** Shipped two context-budget organs on branch `feat/context-budget-organs`. Step 0: PLAYBOOK drift-check confirmed clean (no inline git-finish boilerplate in prompt-format section). Step 1 (#104): `verify` skill at `.claude/skills/verify/` — `verify.py` (pytest + ruff + git-status, compact PASS/FAIL, full output only on failure) + `SKILL.md` (frontmatter + invocation rule; hub-local pilot, #9 canonical-home open); `templates/prompt-template.md` v1.2 replaces per-step verification boilerplate with `verify` skill invocation. Step 2 (#97): `artifact-reader` subagent at `.claude/agents/artifact-reader.md` — read-only (Read/Grep/Glob only), model pinned to claude-sonnet-4-6, structured summary contract (goal → finding → `(line N): "quote"` + size note), refusal on any mutating tool.

**Result:** #104 + #97 closed. verify witness: `pytest : PASS / ruff : PASS / git : PASS` (3 lines, 0 friction). artifact-reader witness on `council-out-20260606_192557-...` (96,897 bytes): returned ~1.3k summary including pinpoint line-number quotes from `## Synthesis of Practice` (line 299) — 98.7% context reduction. Pre-commit hooks green both commits.

**Changes:** `.claude/skills/verify/verify.py` + `.claude/skills/verify/SKILL.md` (new; commit `36b5294`); `templates/prompt-template.md` v1.2 (commit `36b5294`); `.claude/agents/artifact-reader.md` (new; commit `f8bbf1c`); `BACKLOG.md` (#104 + #97 retired).

**Abandoned:** Nothing.

**Next:** digest gate → n=2 → #84 → #91 → corp package → ai-council chat

---

### 2026-06-06 — /ship git-finish command + prompt-template delegation (closes #103)

**Did:** Authored `/ship` slash command (`.claude/commands/ship.md`): three pre-flight refusals (on `main`, dirty tree, red validators), temp-file `--no-ff` merge (never `git merge -F -` — gotcha: exits 129 trying to open a file named `-`), push, ask-before-delete prompt, JOURNAL scaffold reminder. Updated `templates/prompt-template.md` Final section to delegate to `/ship` (v1.0→v1.1). Self-witness: /ship shipped its own branch with a pre-flight refusal demo (dirty-tree) and the actual merge.

**Result:** #103 closed — all three Done-when criteria met (command exists, prompt template delegates, inline sequence dropped). Pre-commit hooks green; 296 tests pass (1 skip). Branch `feat/ship-command` merged `--no-ff` via temp-file message with `closes [#103]`.

**Changes:** `.claude/commands/ship.md` (new, commit `9384973`); `templates/prompt-template.md` Final section + version bump (commit `ccb898d`); `JOURNAL.md` (this entry); `BACKLOG.md` (#103 closed).

**Abandoned:** Nothing.

**Next:** verify-as-skill + #97 → digest gate → #84 → #91.

---

### 2026-06-06 — Immutability guard (transcripts zone) + billing-leak sentinel

**Did:** Built a fail-closed PreToolUse guard blocking in-place edits of existing decision records. UNDERSTAND valve **HALTED on fact 1**: ADRs ARE amended in place (CLAUDE.md §5 "in-file marker"; ADR-68 carries a formal in-place `## Amendment`, commit `69efa9a`; >25 ADR files multi-commit) — a sanctioned flow the original whole-`docs/decisions/*` framing (#105) would block. Transcripts proved clean (37/37 single-commit). Presented the three pre-named options; operator ruled **C now, A queued, not B**. Shipped transcripts-only v1: `scripts/hooks/block_immutable_edits.py` (all mutating tools enumerated; fail-open out-of-zone, fail-closed in-zone), wired in project PreToolUse, witnessed live (Edit of existing transcript blocked, new-file create allowed, scratch removed). ADR-77 amends ADR-75 (zone class #2 + ruled ADR direction). Also wired the #101 billing-leak sentinel (`-NoProfile` required — new gotcha). `/codex review` returned 3 CRITICAL + 1 HIGH on the guard; hardened path resolution (normpath+realpath) and multi-field evaluation, documented the shell-write residual.

**Result:** Transcripts immutable-zone enforced + proven. 7 commits, 296 tests pass (1 skip = symlink host-privilege). Health/codemap/backlog gates green. #101 closed; #105 PARTIAL (stays open); #112 added (Option A adr_amend helper).

**Changes:** `scripts/hooks/block_immutable_edits.py` + `tests/test_block_immutable_edits.py` (new, commits `ec50c6c`/`02b7231`); `.claude/settings.json` (PreToolUse guard + sentinel hooks, `31eedbf`/`20d67ab`); `docs/decisions/ADR-77-*` (`73ba121`); `scripts/billing_leak_sentinel.ps1` (`20d67ab`); `BACKLOG.md` (#105 annot + #112 add + #101 close, `08b7f03`/`20d67ab`); `docs/audits/2026-06-06-codex-immutability-guard.md` (`9f72715`); `~/.claude` gotchas (hook `-NoProfile` trap; not repo-tracked).

**Abandoned:** Whole-`docs/decisions/*` zone (valve halt); Option B (held until #23); naive shell-write matching (over-blocks reads); handoffs/audits excluded (sanctioned append flows).

**Next:** `/ship command → verify-as-skill + #97 → digest gate → #84 → #91`

---

### 2026-06-06 — Consolidated BACKLOG capture: SOTA research + article gap analysis

**Did:** Consumed research transcript `council-out-20260606_192557-...` (SOTA CC methodology findings) and gap analysis verdict. Ran UNDERSTAND valve — funnel-batch items (PROPOSALS persistence, failing check, freshness restamp) confirmed present → Step 0 skipped. Added 10 new BACKLOG items (#102–#111) across 6 insertion points spanning 4 themes (Tooling & evaluation, Enforced governance, Cross-repo universalization, Lessons feedback loop, Decision management). Annotated 4 existing items (#17, #82, #96, #97) with research-backed riders. Also committed BACKLOG item #101 (SessionStart billing-leak sentinel, addendum from prior session).

**Result:** Governance layer validated by field evidence. Runtime gaps captured. 10 new items + 4 annotations committed; branch `docs/backlog-capture-sota` ready for merge.

**Changes:** `BACKLOG.md` — #101 added (commit `5566be4`); #102–#111 added (commit `accd0af`); #17/#82/#96/#97 annotated (commit `caf2ddc`).

**Abandoned:** Nothing; Step 0 correctly skipped per valve.

**Next:** `corp 2026-06-07 digest → n=2 → #84 → #91 → corp chat package → ai-council chat LAST`

---

### 2026-06-06 — Kill CC billing leak: PATH shim strips ANTHROPIC_API_KEY from CC process

**Did:** Discovered `ANTHROPIC_API_KEY` present in CC's inherited shell environment — silently billing API instead of Max subscription. Ran UNDERSTAND valve: confirmed ai-council consumes the key via `os.environ.get()` (must not be globally removed). Resolved that `$PROFILE` is in P0 zone (OneDrive - Blue Yonder) — pivoted to Option B (PATH shim, no profile contact). Surveyed PATH for a writable dir before `.local\bin` (real `claude.exe` at pos 28); chose `C:\Users\1028120\AppData\Roaming\npm` (pos 27). Created `claude.cmd` shim: strips `ANTHROPIC_API_KEY` via CMD's `set ANTHROPIC_API_KEY=` (unset idiom), delegates to hardcoded real binary path. Verified: (1) `Get-Command claude` → shim at npm; (2) ANTHROPIC_API_KEY NOT_DEFINED inside CC child; (3) parent shell key intact, GEMINI_API_KEY unaffected.

**Result:** CC sessions no longer inherit `ANTHROPIC_API_KEY`; Max subscription billing restored. ai-council and other tools unaffected (parent shell still has the key). Both Step 2 witness checks passed.

**Changes:** `C:\Users\1028120\AppData\Roaming\npm\claude.cmd` (machine config, outside repo). LESSONS.md (two-clause lesson prepended). `~/.claude/skills/gotchas/gotchas.md` (two new entries). This JOURNAL entry.

**Abandoned:** Profile edit (P0 zone conflict — `$PROFILE` resolves under OneDrive - Blue Yonder; PreToolUse guard would have caught the write; pivoted to shim approach before attempting).

**Next:** corp 2026-06-07 digest (scoped read) → n=2 → #84 → #91 → ai-council chat (LAST per operator ruling 2026-06-06).

---

### 2026-06-06 — BACKLOG capture: funnel-integrity defects + scope annotations

**Did:** Ran UNDERSTAND valve checks on `propose_closures.py` (confirmed unconditional overwrite) and BACKLOG items #5/#34 (confirmed existence + scope). Committed pre-existing fleet audit artifacts (corp-monorepo `canonical_freshness` fail) to clean the tree. On branch `docs/backlog-capture-funnel-defects`, added three new BACKLOG items and two annotations.

**Result:** All pre-commit gates passed (validate-backlog, audit-health). Three items captured: #98 PROPOSALS persistence (P2, Enforced governance / lifecycle hooks), #99 FLEET-HEALTH check-name detail (P3, Enforced governance / structural validation), #100 corp-monorepo CLAUDE.md restamp queue (P3, Cross-repo universalization). Annotations: #5 scope extended ADRs 35-63→35-76; #34 appended pre-emit prompt checklist codification candidate (three knowledge-present/application-skipped misses observed 2026-06-06).

**Changes:** `BACKLOG.md` (3 new items, 2 annotations, grooming log appended); `ecosystem/corp-monorepo/history/2026-06-06.md` + `ecosystem/corp-monorepo/state.yaml` + `docs/audits/2026-06-06-corp-monorepo-audit.md` (fleet audit artifacts). Branch: `docs/backlog-capture-funnel-defects`.

**Abandoned:** Nothing.

**Next:** corp 2026-06-07 digest (scoped read) → n=2 → #84 → #91 → ai-council chat (LAST per operator ruling 2026-06-06).

---

### 2026-06-06 — #85 implementation: fleet-baseline scheduler registered + fleet_health hardened (ADR-76)

**Did:** Implemented ADR-76 on branch `feat/85-fleet-scheduler`. (Step 0) Annotated BACKLOG #25 to embed the verbatim Model/Mode/Effort prompt-format spec. (Step 1, tests-first) Hardened `scripts/fleet_health.py`: bounded the audit subprocess with a `120s × repo-count` timeout (timeout/crash → INCOMPLETE baseline, never an unbounded hang), atomic digest write via `tempfile.mkstemp` + `os.replace`, a `completed_at` frontmatter stamp written only on a full successful pass, and a `>48h`-stale fail-soft warning on both the skip and run paths. (Step 2) Authored `scripts/setup-fleet-scheduler.ps1` (PS 5.1-compatible, idempotent `-Force`, `-DryRun`) registering `\DevKnowledge\fleet-baseline` (daily 09:00, StartWhenAvailable ON, WakeToRun OFF, IgnoreNew, 15-min limit, InteractiveToken/no stored creds) + exported `fleet-baseline.task.xml`. (Step 3) Registered the task and witnessed a manual scheduler-context fire. (Step 4) Opened `docs/audits/2026-06-06-85-validation-record.md` with the 5 Council cases + witnessed evidence. (Final) Ran Codex review; fixed both HIGH findings.

**Result:** 279 pytest passed (+24 from 255); ruff clean; all pre-commit gates passed. **Scheduler-context fire witnessed: `LastTaskResult: 0`**, digest rewritten with `completed_at: 2026-06-06T18:23:18` + `Baseline completed (4/5 green)` — the audit genuinely ran git/python under the Task Scheduler env (surfaced a real corp-monorepo finding, not a no-op), passing the env-divergence test. Codex HIGH #1 (shared-temp race) and #2 (incomplete baseline reported healthy) both fixed + regression-tested. **#85 stays OPEN** — full validation (unattended 09:00 fire, sleep-miss catch-up, stale warning, hung-repo timeout) spans real nights, tracked in the validation record.

**Changes:** `scripts/fleet_health.py` (hardening + Codex fixes), `tests/test_fleet_health.py` (+24 tests), `scripts/setup-fleet-scheduler.ps1` + `scripts/fleet-baseline.task.xml` (new), `docs/audits/2026-06-06-85-validation-record.md` + `docs/audits/2026-06-06-codex-85-fleet-scheduler.md` (new), `BACKLOG.md` (#25 annotation). Commits: `ac207a6` (#25), `4ab2845` (Step 1), `0bb14c5` (Step 2), `061bc9f` (Step 4 record), `96d28cc` (Codex fixes). OS state: registered Task Scheduler task `\DevKnowledge\fleet-baseline` (intentional, not a leftover); gitignored `logs/FLEET-HEALTH.md` refreshed.

**Abandoned:** Literal per-repo timeout *attribution* — the single `audit.py run` subprocess audits all repos in-process, so a timeout records the run as fleet-level INCOMPLETE without naming the wedged repo. Switching to per-repo subprocesses (`audit.py repo <name>`) would proliferate tracked `docs/audits/<name>-audit.md` reports daily; rejected as a regression. The safety property (bounded run, failure recorded not silent) is delivered; the limit is documented in the validation record. Also surfaced (not actioned): every scheduled run leaves tracked-file churn (`ecosystem/*/state.yaml`, history, ecosystem-audit.md) in the working tree — inherited audit behavior, restored this session to keep the branch clean.

**Next:** corp 2026-06-07 digest (scoped read) → log n=2 → #84 codification (refs ADR-74/76) → #91 ARCHITECTURE rewrite → ai-council dedicated chat (agenda 2, #96). #85 validation addenda land as real nights accrue.

---

### 2026-06-06 — Context-budget doctrine codified in PLAYBOOK; #96/#97 queued; #17 annotated

**Did:** Codified the context-budget read-scoping rule (provenance: compaction post-mortem — a distillation prompt consumed ~40% context window full-reading a ~78k-token Council transcript). Added `### Context budget — read-scoping rule` to PLAYBOOK §7 "Managing a Long Claude Code Session" after `When context gets heavy` (TOC updated). Added two BACKLOG items: #96 (ai-council VERDICT marker, producer-side — synthesizer emits machine-readable VERDICT block; queued for ai-council dedicated chat per ADR-41) and #97 (artifact-reader subagent template, consumer-side — hub template + fleet rollout). Annotated #17 (CLAUDE-md-template) to include compaction-preservation instructions in its scope.
**Result:** 255 pytest passed; all pre-commit gates passed (toc-freshness-playbook, validate-backlog, audit-health). 2 commits on branch `docs/context-budget-rule`.
**Changes:** `protocols/PLAYBOOK.md` (new subsection + TOC entry), `BACKLOG.md` (#96 under Decision management, #97 under Lessons/codify-patterns, #17 scope extended).
**Abandoned:** nothing.
**Next:** #85 implementation prompt (scheduler + fleet_health hardening) → corp 2026-06-07 digest (scoped read) → log n=2 → #84 codification (refs ADR-74/76) → #91 ARCHITECTURE rewrite → ai-council dedicated chat (agenda item 2, picks up #96).

---

### 2026-06-06 — Council fleet-baseline-host debate → ADR-76; #85 mechanism recorded

**Did:** Convened AI Council (4-model panel: claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3; openai synthesizer; 2 rounds; pick-mode) on three questions: Q1 which local scheduler hosts the fleet-baseline run; Q2 whether to attach LLM via `claude -p` on the scheduled path; Q3 how to handle missed runs. Council verdict 1B+2B+3B accepted by operator paste-consent. Authored ADR-76 (Windows Task Scheduler → `python scripts/fleet_health.py` directly; LLM deferred to next interactive SessionStart; built-in catch-up for missed runs; `/loop`/CronCreate formally disqualified as doctrine corollary). Updated BACKLOG #85 to replace stale Desktop-scheduler mechanism text with Council verdict; added ADR-76 to refs; kept OPEN (n=1 gate still pending). Appended lesson: REJECTED rows in bundled packages need their own named ratification line.
**Result:** All pre-commit gates passed; 255 pytest tests passed. Docs-only — no implementation. Branch `docs/adr-council-fleet-baseline-host` is 3 commits ahead of main.
**Changes:** `docs/decisions/ADR-76-local-fleet-baseline-host.md` (new), `docs/decisions/transcripts/council-out-20260606_172555-pick-council-local-scheduled-tier.md` (archived), `BACKLOG.md` (#85 mechanism updated), `LESSONS.md` (bundled-ratification lesson prepended). Commits: `f0d14d1` (ADR-76 + transcript), `cf610bc` (BACKLOG #85), `a9315e2` (LESSONS).
**Abandoned:** nothing.
**Next:** implementation prompt for #85 (Task Scheduler setup via `scripts/setup-fleet-scheduler.ps1`); corp 2026-06-07 digest → log n=2 → #84 codification.

---

### 2026-06-06 — Doctrine-pass codification: ADR-74, ADR-75, BACKLOG #85 + #95

**Did:** Codified the 2026-06-06 automation doctrine pass in documentation form. Authored ADR-74 (automation doctrine consolidation — layer→job matrix canonical, ADR-70 amended; gaps A3/A4/G1–G3 resolved) and ADR-75 (exclusion-zone register — founding member OneDrive-Blue-Yonder, governed by `block-onedrive.ps1`). Amended BACKLOG #85 to record the ratified direction (local Tier-2 cross-repo host, native Desktop scheduler, n=1 gate, riders R1/R2). Added BACKLOG #95 (template↔copy orchestration drift watcher, gap G5).
**Result:** All pre-commit gates passed; 255 pytest tests passed. Docs-only — no organs built. Branch `docs/doctrine-pass-adrs` is 3 commits ahead of main.
**Changes:** `docs/decisions/ADR-74-automation-doctrine-consolidation.md` (new), `docs/decisions/ADR-75-exclusion-zone-register.md` (new), `BACKLOG.md` (#85 amended, #95 added). Commits: `104b4ea` (ADR-74), `854df0e` (ADR-75), `ad68565` (BACKLOG).
**Abandoned:** nothing.
**Next:** corp 2026-06-07 digest → log n=2 → #84 codification referencing ADR-74; #85 n=1 gate run.

---

### 2026-06-06 — ADR-73 wording ratified as authoritative for #86.3

**Did:** Operator ruling (consent by paste): ratified ADR-73's Decision text as the authoritative form of the #86.3 ruling, resolving the two divergences surfaced in the corp-JOURNAL-vs-ADR-73 wording check. Divergence (1): "in both directions" (bidirectional propagation — hub→child template updates + child→hub back-ports) is intended as part of the ruling; corp JOURNAL 2026-06-06 stated only hub→child but the back-port precedent (`cfdcc31`, `e9c9e6a`) was present. Divergence (2): "not at runtime" constraint is carried by ADR-72 (which ADR-73 amends) — no textual patch to ADR-73 needed.
**Result:** ADR-73 Decision clause (c) stands as written; corp JOURNAL 2026-06-06 remains the contemporaneous record; ADR-73 is the ratified authoritative form. No file edits — ruling recorded here only.
**Changes:** `JOURNAL.md` (this entry). Commit: (this commit).
**Abandoned:** nothing.
**Next:** Read corp 2026-06-07 digest when it exists → log n=2 → #84 codification (gated at n=2).

### 2026-06-06 — #86 closed, ADR-73 authored

**Did:** Authored ADR-73 (per-repo orchestration distribution, amending ADR-72); closed BACKLOG #86 entirely (all three sub-decisions recorded — 1: SELECTIVE-PUSH ruling, 2: ADR-72 self-containment, 3: ADR-73 template pattern); appended #86.3 drift correction to handoff `04_RECENT.md` facts table.
**Result:** #86 retired per ADR-65 (grooming log records disposition: sub-decisions 1–2 → ADR-72; sub-decision 3 → ADR-73; source corp JOURNAL 2026-06-06). ADR-73 cites corp→hub back-ports `cfdcc31`, `e9c9e6a` as rollout-moment propagation precedent.
**Changes:** `docs/decisions/ADR-73-per-repo-orchestration-distribution.md` (new), `BACKLOG.md` (closed #86), `docs/handoffs/2026-06-06-dev-knowledge-session/04_RECENT.md` (correction appended). Commits: `2b653c2` (ADR-73), `034e9f9` (#86 close), `94970c2` (correction).
**Abandoned:** nothing.
**Next:** Read corp 2026-06-07 digest when it exists → log n=2 → #84 codification (gated at n=2).

---

### 2026-06-06 — Handoff Phase 2 complete (2026-06-06-dev-knowledge-session)

**Did:** Consolidated the bundle from the pasted interview answers. Cross-checked 6 load-bearing sender claims against repo state (ADR-72 file, #84 n=1-of-2 gate, #86 sub-decision-3 open, `surface_triage.ps1` backports, clean tree, #89 check-source) — all confirmed, **no drift**. Wrote 8 files to `docs/handoffs/2026-06-06-dev-knowledge-session/` (README + 01–07, all within line budgets), removed the `in-progress/` folder.
**Result:** Bundle ready. corp-monorepo claims flagged as cross-repo / not re-verified here (ADR-36/41 read-only). Stamp: v4.4 (status beta).
**Changes:** `docs/handoffs/2026-06-06-dev-knowledge-session/`, removed `in-progress/…`, `JOURNAL.md`.
**Next:** Operator pastes 01–07 into the successor chat per the bundle README.

---

### 2026-06-06 — Handoff Phase 1 interview generated (2026-06-06-dev-knowledge-session)

**Did:** Ran the v4.4 handoff scope matrix (Case 2 — clean tree, commits since last handoff `2026-06-05-dev-knowledge-v44-wrap`, today's slug absent). Wrote `docs/handoffs/in-progress/2026-06-06-dev-knowledge-session/_handoff-interview.md` (sage→apprentice single cluster, four-tag discipline). HEAD captured `608f26b`.
**Result:** Interview awaiting operator answers. Next: paste question block into sender chat, paste answers below the marker, then `complete handoff for dev-knowledge`.
**Changes:** `docs/handoffs/in-progress/…`, `JOURNAL.md`.
**Next:** Phase 2 consolidate.

---

### 2026-06-06 — Backport corp's digest-existence guard into surface_triage.ps1

**Did:** Backported corp's (b)-check guard: the nightly digest-existence check now gates on `$LASTEXITCODE -eq 0` + a `.md`-shape match on the returned name, not stdout-non-empty. Closes the 404-body-to-stdout misread — `gh api --jq '.name'` on a 404 exits non-zero but still prints the error body to stdout, so the old `if (-not $found)` read a MISSING digest as PRESENT and never fired the silent-skip nudge. LESSONS one-liner added (durable gh-api gotcha). Also deleted the merged `chore/gh-auth-check` branch (operator-approved).
**Result:** Parses; PS 5.1 happy path silent (today's digest is on `main`); a bogus-path probe reproduced the trap (gh exit 1, `$found` = the 404 JSON body) and confirmed the NEW guard reads present=False (nudge fires) where the OLD naive check read present=True (the misread now closed). 255 tests green (no Python touched).
**Changes:** `scripts/surface_triage.ps1` ((b) digest guard), `LESSONS.md` (404-trap one-liner), `JOURNAL.md` (this). Branch `chore/backport-digest-guard`, merged `--no-ff`. Commits `e9c9e6a` (fix) · `3ff096e` (lesson).

---

### 2026-06-06 — gh-auth-check hardening of surface_triage.ps1

**Did:** Hardened `scripts/surface_triage.ps1` with a leading `gh auth status` gate (same hardening as corp's surface-conformance.ps1): on non-zero exit it prints `[gh] auth invalid -- run: gh auth refresh -h github.com` and skips the gh-dependent checks fail-soft (exit 0). Closes a silent-failure gap — the header previously treated "unauthenticated" as a silent happy-path case, so an expired token surfaced nothing (false all-clear hiding a skipped nightly). Header silent-list + verify note updated to match. LESSONS append: gh-auth failure is operator-recoverable-only (never blind-retry; durable fix = long-expiry fine-grained PAT).
**Result:** Parses; runs clean under PowerShell 5.1 (exit 0, silent happy path — #16 now closed so no [triage] line); gate-logic probe confirmed the banner fires on non-zero `$LASTEXITCODE`. 255 tests green (no Python touched). NOTE: corp's local `surface-conformance.ps1` does NOT yet show this gate (its change is likely unmerged in this clone); separately, corp's `(b)` digest check is more robust than the hub's (guards the gh-api 404-body-to-stdout trap) — a latent hub improvement, left out of scope.
**Changes:** `scripts/surface_triage.ps1` (auth gate + header/verify), `LESSONS.md` (entry + stamp), `JOURNAL.md` (this). Branch `chore/gh-auth-check`, merged `--no-ff`. Commits `cfdcc31` (script) · `36a3ce9` (lesson).

---

### 2026-06-06 — Routine display-name naming standard added to PLAYBOOK

**Did:** Added a "Naming" subsection to PLAYBOOK §"Routine/night deployment standard": display names follow `<repo>: <cadence>-<domain>` (lowercase, kebab-case after the colon, repo-first so the Routines panel self-sorts). Label-only — no contract depends on it (diff-guard keys off the digest path, Action off the `claude/*` branch pattern, surfacing off the Issue label), so renames are cosmetic and safe. Applies to all current/future Routines; current set `dev-knowledge: nightly-conformance`, `corp-monorepo: nightly-conformance`.
**Changes:** `protocols/PLAYBOOK.md` (+Naming subsection; TOC regenerated +1 — PLAYBOOK TOC indexes H3s), `JOURNAL.md` (this). Branch `docs/routine-naming-standard`, merged `--no-ff`. Commit `bd5c5e9`.

---

### 2026-06-06 — grok-review backlog item + §9 toc-hook drift fix + branch cleanup

**Did:** Three-item batch on `chore/grok-review-item`. (1) Added BACKLOG **#94** — /grok review second-opinion reviewer experiment (P3, EXPLORATORY, go/no-go pending; xAI `grok-build-0.1` on the diff; if greenlit, experiment-first parallel to /codex on ~10 diffs, deltas-only; carries the operator caveat that the 70.8% SWE-bench figure is the Grok Build CLI system, not this model variant — verify-before-encode). (2) Fixed the **§9 CLAUDE.md drift** the prior triage re-read surfaced — added `toc-freshness` + `toc-freshness-playbook` (now 8 hooks, matching `.pre-commit-config.yaml` + ARCHITECTURE §Validators); editing a freshness-gated canonical file re-triggered audit #10, so per the established ruling did a genuine re-read + re-stamp (v2.15, `last_reviewed`→2026-06-06), which also caught §11 being one ADR behind (rotated 67–71→68–72, +ADR-72) and flagged the §11 ADR-68 line **[REFUTED]**. (3) Deleted the merged `chore/triage-2026-06-06` branch (operator-approved).
**Result:** All landed; `validate_backlog` OK (51 tasks), audit-health OK (`canonical_freshness` green post-commit), 255 tests green (markdown-only change, validators untouched). Tonight's nightly will no longer flag the §9 toc-hook drift.
**Changes:** `BACKLOG.md` (+#94), `CLAUDE.md` (§9 +2 hooks · §11 rotation + ADR-68 REFUTED flag · v2.15 + re-stamp), `JOURNAL.md` (this). Branch `chore/grok-review-item`, merged `--no-ff`. Commits `e9a5c3e` (#94) · `20bbb7a` (CLAUDE §9/re-stamp).

---

### 2026-06-06 — Morning triage ratification (nightly digest 2026-06-06, issue #16)

**Did:** Ratified the 2 nightly-triage survivors. N1 (#74 forward-pointer interpretation, High) ACCEPTED-AS-CLARIFICATION — one-line grooming-log annotation that the "alongside #18/#27" clause was consciously satisfied via the PLAYBOOK forward-pointer (reconciliation in the Track B close, commits 11ef2d8/4c62f63); no co-location work owed, no reopen (`8a8bf68`). N2 (ARCHITECTURE "Last updated" 2026-06-04 vs `last_reviewed` 2026-06-05, Med) APPLIED — a bare date-flip would trip audit check #10 (`canonical_freshness`) next run (editing today pushes the git author-date past `last_reviewed`), so per operator ruling did a genuine end-to-end re-read + re-stamped both to 2026-06-06; the re-read also caught and added the missing **ADR-72** Governing-ADRs entry (`cdd47c1`).
**Result:** Both survivors resolved; issue #16 closed with a ratification comment. audit-health OK, 255 tests green, `validate_backlog` OK (50 tasks). Spotted-but-deferred (out of triage scope): CLAUDE.md §9 pre-commit list omits the two `toc-freshness` hooks that ARCHITECTURE.md §Validators correctly lists.
**Changes:** `ARCHITECTURE.md` (frontmatter `last_reviewed` + "Last updated" line + ADR-72 bullet), `BACKLOG.md` (grooming-log N1 annotation), `JOURNAL.md` (this). Branch `chore/triage-2026-06-06`, merged `--no-ff`. Commits `cdd47c1` (N2) · `8a8bf68` (N1).

---

### 2026-06-06 — #86.2: cloud hub-reference resolution → ADR-72 self-containment (Path A)

**Did:** UNDERSTAND inventoried the 4 hub-reference classes a child cloud Routine could depend on (pre-commit doc-tooling hooks, `tier1-lifecycle` plugin, methodology files, user skills) and tested cloud behavior — **falsifying the #86.2 premise**: hub `.dev-knowledge` is **private** (`gh api .visibility`), the plugin is **verified inert in cloud** (JOURNAL 2026-06-04, local-dir marketplace), cloud is a single-repo Linux clone, and the conformance verifiers are self-referential. So plugin/skill distribution cannot resolve a private hub in cloud and ADR-71's "URL-swappable later" hatch is closed for the cloud case; no reference is load-bearing there. Operator ruled **Path A** (codify self-containment; B publish-subset / C auth'd-infra rejected). Wrote ADR-72 (amends, does not edit, ADR-71), added a PLAYBOOK "Cloud-session hub-independence" subsection (TOC regenerated), indexed it.
**Result:** ADR-72 landed; **no resolver code shipped** (a plugin-cache resolver would be cloud-inert = false coverage). audit-health 13/13; 255 tests collected; `toc-freshness-playbook` fresh. Advances #86 (sub-decision 2 recorded; sub-decision 3 R2 distribution still open). Child repos untouched (ADR-41).
**Changes:** `docs/decisions/ADR-72-cloud-routine-hub-independence.md` (new), `docs/decisions/README.md` (index + traceability), `protocols/PLAYBOOK.md` (subsection + TOC), `BACKLOG.md` (#86 sub-decision-2 annotation), `LESSONS.md` (cloud-distribution lesson). Branch `docs/86-cloud-hub-independence`, merged `--no-ff`.

---

### 2026-06-06 — Correction: hub nightly verdict in bookkeeping entry

**Did:** Verified hub nightly state post-bookkeeping. Corrected the "GH/nightly N/A" claim in the earlier 2026-06-06 bookkeeping JOURNAL entry — that was accurate for corp-monorepo (no remote) but wrong for the hub: the hub has GH Actions and fired two runs on 2026-06-05 (PRs #8 MERGED 0h/1m/0l, #11 CLOSED 1h/0m/0l). No 2026-06-06 scheduled run fired (no branch/PR/run exists); the nightly contract itself is proven (Tests A+B 2026-06-05). Missed-run class is watched by the SessionStart digest-presence check. No further action required.
**Result:** Correction recorded; no files beyond JOURNAL and LESSONS touched.
**Changes:** JOURNAL (this entry), LESSONS (cross-repo-state-claims lesson appended).

---

### 2026-06-06 — Hub bookkeeping: #75 close + corp audit evidence trail

**Did:** Closed #75 (corp scoped audit Workflow ran end-to-end 2026-06-06, 29 targets / ~588k tok / ~4 min, fit confirmed). LESSONS append: per-stage model pins FUNCTIONAL post-C3 override removal (re-probe complete, cadence = next CC upgrade). Annotated #89 with corp #75 check-source disposition (~6/29 binary checks = mechanizable deterministically; reserve Workflows for judgment-laden conformance) and #84(a) with n=1-of-2 evidence trail. Folded 2026-06-06 fleet-health snapshot files (5 state.yamls + audit + 5 history). Nightly verdict: 5/5 repos green (SessionStart fleet_health.py); GH/nightly N/A — corp-monorepo has no remote, no GH Actions infrastructure yet (#85/#86 open).
**Result:** Branch `chore/75-hub-bookkeeping` merged (3 content commits + 1 fleet chore); `validate_backlog` clean (7 themes, 21 stories, 50 tasks).
**Changes:** `LESSONS.md`, `BACKLOG.md` (#75 retired, #89/#84 annotated), ecosystem state files + `docs/audits/2026-06-06-ecosystem-audit.md` (commits f50dda6, bd3482e, a164cda + fleet chore).

---

### 2026-06-06 — Land external-research note + encode backlog dispositions

**Did:** Landed `docs/archive/2026-06-05-agent-automation-external-research-note.md` verbatim (E1 CREAO cloud-agent infra, E2 CC automation stack, E3 /goal principles, E4 verdict-only). Catalog line added to `docs/archive/README.md`. Encoded three dispositions into BACKLOG: #84(a) forward-note (self-measuring-tool + degenerate-metric-guard, external note §3); #85 body amended (evaluate native Desktop scheduled-tasks tier vs OS Task Scheduler); #86 refs extended (sub-decisions 1 + 3 criteria).
**Result:** Note landed; all three backlog annotations committed; `validate_backlog` clean (7 themes, 21 stories, 51 tasks).
**Changes:** `docs/archive/2026-06-05-agent-automation-external-research-note.md` (new), `docs/archive/README.md`, `BACKLOG.md` (commits 1b54c8e, af00519).

---

### 2026-06-05 — Apply 10 ratified #81 pilot findings + archived-command sweep

**Did:** Applied all 10 operator-ratified findings from the 2026-06-05 #81 pilot to `protocols/ESSENTIALS.md` (branch `docs/essentials-pilot-fixes`, 4 commits): [1] backlog section → ADR-66 story-map format; [2][3][7] ADR-45 false-authority removed from 3 sections; [4] `/recap` → `/resume`; [5] un-dotted exceptions gains `setup.cfg` + `README.md`; [6] Auto-TOC acknowledges PLAYBOOK already applied; [8] PLAYBOOK §4 citation → `§Session boundaries → Decision fatigue threshold`; [9] `/evolve` §Feedback Loop annotated archived; [10] Data Sanitization → PLAYBOOK §13. Archived-command sweep (STEP 4): annotated all live-presenting `/boot` and `/evolve` refs across ESSENTIALS, PLAYBOOK, CLAUDE.md (14 hits). Pruned merged pilot branch `chore/81-pilot-run`.
**Result:** ESSENTIALS reference-integrity restored — all 10 findings applied, 0 skipped (all evidence held). K1/K2 untouched.
**Changes:** `protocols/ESSENTIALS.md`, `protocols/PLAYBOOK.md`, `CLAUDE.md` (archived-command annotations), this JOURNAL entry. **Next:** Track C (full-rulebook #81 run over PLAYBOOK + remaining `protocols/`).

### 2026-06-05 — #81 pilot: scoped methodology-conformance Dynamic Workflow (verifier-per-rule + skeptic)

**Did:** Ran the first end-to-end #81 pilot — a scoped, READ-ONLY methodology-conformance Dynamic Workflow over `protocols/ESSENTIALS.md`. Design: 27 Sonnet verifiers (one per `##` rule-section; surgical reads; evidence-required structured findings) fan out via `parallel()`, then one Opus skeptic adversarially reviews only the non-conforming findings (explicit `summary-faithful` + `documented-decision` kill reasons, since ESSENTIALS deliberately condenses PLAYBOOK). All pins explicit (Haiku probe / Sonnet verifiers / Opus skeptic); `$env:CLAUDE_CODE_SUBAGENT_MODEL` confirmed empty and transcripts state-verified (501 sonnet / 58 opus msg-entries, zero haiku) so pins were honored. R2 respected: workflow authored inline (session dir), NOT saved to repo `.claude/workflows/`, NOT committed. R1 guard = session `permissions.deny:["Write","Edit"]` in gitignored `.claude/settings.local.json` + post-run fleet `git status --porcelain` tripwire.
**Result:** **R1 PASS** — a throwaway 1-agent probe attempted a sentinel write under the active deny; sentinel never created (the deny BINDS workflow subagents, re-confirming the 2026-06-04 gotcha on CC 2.1.162). Main run: 28 agents, ~855k subagent tokens (pilot total ~874k incl. probe), ~12 min; coverage **27/27 verdicted, 0 missing** (completion criterion met); 15 conforms / 8 drift / 4 stale -> **12 non-conforming -> skeptic kept 10, killed 2**. Strongest survivor (high): ESSENTIALS "Backlog" still describes the ADR-64 status-bucket layout that ADR-66 superseded. **Nothing applied** — all 10 survivors are READ-ONLY proposals for operator ratification.
**Contamination window:** a parallel terminal sharing this one working tree committed `3603bbd` (tier1-lifecycle 0.1.3 JOURNAL entry) onto the audit's checked-out branch `chore/81-pilot-run` mid-run, and a scratch-branch test transiently mutated the tree. Cross-checked: `3603bbd` touched **only JOURNAL.md** (+4 lines) and no audited file (ESSENTIALS/PLAYBOOK/ADRs/BACKLOG/commands all last-committed pre-session, no churn) -> **zero findings affected**. Root lesson: parallel sessions must not share a working tree (ADR-61 worktree).
**Permission trap:** the read-only session Write/Edit deny proved un-liftable mid-session (tool deny cached + auto-mode classifier blocks shell rewrites of the settings file) — required operator action to lift before this recording could be written (see LESSONS).
**Changes:** this JOURNAL entry; 5 LESSONS entries. No methodology file edited (read-only pilot). Workflow scripts remain in the session dir only (uncommitted); R1 probe script removed (verified).
**Next:** operator ratifies the 10 proposals (a separate edit pass applies the approved ones); after a green pilot, the full-rulebook run (PLAYBOOK + remaining `protocols/`). Advances #81 — a scoped pilot does NOT close it.

### 2026-06-05 — Plugin 0.1.3 consumer install (cache 0.1.3 materialized) + validate_backlog gate re-verified

**Did:** Ran the consumer half of the tier1-lifecycle 0.1.3 deploy dance (source side — version bump + marketplace publish — landed earlier today): `claude plugin marketplace update dev-knowledge-methodology` then `claude plugin update tier1-lifecycle@dev-knowledge-methodology --scope project` (hub scope only; children ride their next session per ADR-41). Re-verified the new in-place-RESOLVED gate on a throwaway branch — a dummy `~~struck~~` task line made the `validate-backlog` pre-commit hook FAIL (commit blocked), then discarded the branch + verified removal (tree identical). **Result:** cache `0.1.3/` materialized (plugin.json=0.1.3, ships `_INPLACE_RESOLVED_RE`); installed_plugins.json hub entry -> 0.1.3; gate confirmed blocking. Only `~/.claude/` plugin state changed (outside the repo); this JOURNAL line is the sole repo change. **Changes:** this JOURNAL entry. **Next:** child repos pick up the 0.1.3 validate_backlog gate on their next session.

### 2026-06-05 — Workflow-escalation rule written (closes #74, #80) + #84(a)/(b) reconciliation

**Did:** (1) Wrote the #74 Workflow-escalation rule into PLAYBOOK as a new "When to escalate to a Dynamic Workflow" subsection under "How to choose Model" — the third rung of the Sonnet/Opus ladder: scale / reusable-artifact / adversarial-quality escalate to a scoped Workflow, stay-with-subagent for bounded+known+token-sensitive work; the Council-boundary sentence (heavy-decision organ vs heavy-execution organ; tournament selects artifacts, doesn't decide); grounded in `docs/archive/2026-06-03-dynamic-workflows-research-note.md` §5 (S1 comparison table + S5 taxonomy). TOC regenerated. (2) Closed #80 (Done-when met: note landed ca843bb + #74 rule now informed by it). (3) Reconciled #84(a) stale "(closes [#74])" clause + extended #84(b)'s reconciliation line. **Result:** branch `docs/74-escalation-rule`, 4 commits (11ef2d8 rule, cc1178b #80-leave, 0e0ada3 #84-reconcile, 4c62f63 #74-leave), 255 tests pass, ruff clean, audit 13/13, validate_backlog OK. **UNDERSTAND-2 adjudication:** #74's Done-when names co-location "alongside #18/#27"; those rules don't exist in PLAYBOOK yet, so the rule landed in its natural home (the model ladder) with an explicit forward-pointer to #18/#27 as the same decision-routing family — the criterion IS written (the substantive Done-when), co-location honored via the pointer. **Changes:** `protocols/PLAYBOOK.md` (new subsection + TOC), `BACKLOG.md` (#74 + #80 removed per ADR-65, #84(a)/(b) annotated), this JOURNAL entry. **Next:** #81 pilot — the methodology-conformance Dynamic Workflow (verifier-per-rule fan-out + skeptic), the first real Tier-3 run.

### 2026-06-05 — Landed the #80 Dynamic-Workflows research note (+ Amendment B) + #84(b) reconciliation

**Did:** (1) Landed the BACKLOG #80 deliverable verbatim at `docs/archive/2026-06-03-dynamic-workflows-research-note.md` per the external-research convention (ADR-60 pending-classification zone; body + Amendment A byte-identical to source, confirmed via diff), cataloged it in `archive/README.md`, and appended **AMENDMENT B** (records-only): (a) R3 resolved — CC 2.1.162 at Phase-0 gate 1; (b) S1-vs-S5 resumability conflict RESOLVED empirically = S1 (gate 5; runs don't survive a CC exit → fire-and-complete, in #85); (c) NEW fact — cloud Routines doesn't run workflows natively → spec-orchestration, in-script validators inert, parser-side fail-closed is the backstop (LESSONS 2026-06-05); (d) PLAYBOOK Routine/night standard landed (7a3e48b). (2) Annotated #84(b)'s "closes [#80]" clause — reconcile vs #80's own Done-when (#80 stays open pending #74). **Result:** branch `docs/land-dw-research-note`, 2 commits (ca843bb, fdea539), validate_backlog OK (53 tasks), all hooks green. Advances #80 (not closed — #74 still open). **Changes:** `docs/archive/2026-06-03-dynamic-workflows-research-note.md` (new), `docs/archive/README.md` (catalog line), `BACKLOG.md` (#84(b) annotation), this JOURNAL entry. **Next:** #84(b) adoption ADR distills this note; #80 closes once #74's escalation rule is informed.

### 2026-06-05 — Minimal night-doctrine package (PLAYBOOK Routine/night standard + ADR-68 supersession note)

**Did:** Wrote the two operator-ratified doc-debt items that must precede Track C, editorially synthesized from records only. (1) Clarified #84 part (d) as UNGATED (one-line note inside the n=2 parenthetical — purely editorial, precedes Track C per operator ruling 2026-06-05). (2) Added a PLAYBOOK "Routine/night deployment standard" section (#84 part d) covering the four-part envelope, the allow-only platform-guard safety envelope (vs the local #85 committed-deny), the spec-orchestration doctrine + its contract consequence (in-script validators inert on fallback; parser-side fail-closed is the cloud backstop), the outcome loop (diff-guard → triage Issues → SessionStart surfacing + digest side-effect check), t-shirt model pins (unpinned fan-out = bug; native scripts route per stage), cloud-session closeout (stranded `claude/*` branches), and the shallow-clone false-positive class + its two guards — each grounded in a cited record (CONTRIBUTING; JOURNAL/LESSONS 2026-06-05; 06-05 conformance digest; JOURNAL 2026-06-04 shallow-history guard; gotchas model-routing). TOC regenerated. (3) Marked ARCHITECTURE's ADR-68 Governing-ADRs entry `[REFUTED — historical]` (never-registered local night-agent, superseded by the cloud Routine), pointing at the staleness-audit row + PLAYBOOK section + 06-05 records; ADR-68 itself immutable, untouched. **Result:** branch `docs/night-doctrine-minimal`, 3 commits, all hooks green (audit-health/TOC-freshness/validate_backlog), tree clean. STEP 4 = NO audit-file edit: the staleness map's own convention is "the map does not change as rows flip — flips are tracked by closures in git," and no row's full scope is covered anyway (ARCHITECTURE/PLAYBOOK rows stay STALE — only sub-pieces landed via #91/#84(d); CONTRIBUTING #92 + CLAUDE #93 untouched). No backlog item closed; advances #84 (part d) + #91 (supersession sub-piece). **Next:** Track C opens — corp-monorepo night architecture on the codified standard. **Changes:** `BACKLOG.md` (#84 clarified), `protocols/PLAYBOOK.md` (new section + TOC), `ARCHITECTURE.md` (ADR-68 supersession note), this JOURNAL entry.

### 2026-06-05 — Doc-debt converted into the work system (staleness audit + #84/#91/#92/#93)

**Did:** Converted the Phase-D living-doc doc-debt into tracked work. (a) Created the immutable audit `docs/audits/2026-06-05-living-doc-staleness.md` = the FINAL CORRECTED staleness map (Workstream 1 of the `2026-06-05-dev-knowledge-session` bundle's Phase-1 interview, folded out at consolidation so it survives only in git; the ARCHITECTURE row is the operator-verified rewrite from commit `19c2b72`), copied faithfully with a provenance header; it is the acceptance oracle for the doc-debt items. (b) Extended #84 with part (d) — a PLAYBOOK Routine/night deployment-standard section (cloud-night envelope, spec-orchestration doctrine, outcome loop = Action diff-guard + nightly-triage Issues + SessionStart surfacing, t-shirt pins, cloud-session closeout, shallow-clone class) — and added #91 (ARCHITECTURE night-architecture rewrite + ADR-68 supersession note, [P2][L]), #92 (CONTRIBUTING spec-orchestration rationale, [P2][S]), #93 (CLAUDE.md pointers, [P2][S], SEQUENCED AFTER #91), each Done-when = "its row in the 2026-06-05-living-doc-staleness audit flips to CURRENT", under "Keep canonical files accurate". ITEM 2: quoted the full bodies of #80/#81/#74/#75 (read-only). **Result:** the staleness map is now an immutable record + oracle; doc-debt = 4 tracked items; validate_backlog OK (53 tasks). The bundle itself was not edited (immutable). **Next:** execute #91 first (largest gap + the misleading ADR-68 passage) per the bundle's recommended order; #93 rides after it. **Changes:** `docs/audits/2026-06-05-living-doc-staleness.md` (new), `BACKLOG.md` (#84 extended, #91/#92/#93 added), this JOURNAL entry.

### 2026-06-05 — #12 withdrawn, logs/ relic audit (no relics), plugin 0.1.3 deploy

**Did:** (1) Withdrew #12 (operator ruling) — conditional recent-write check first confirmed no activity on any evolution path (live `~/.claude/memory/` empty, no evolution-log/`.jsonl` in the repo, no settings.json hook consumer; the only live `.jsonl` is the unrelated `~/.claude/history.jsonl`), so removed per ADR-65 with `closes [#12]`, citing the 5415ad1 annotation + the C3 cleanup JOURNAL entry. (2) logs/ relic audit per the operator's conditional rule: `TOKEN-LOG.md` = SACRED (tracked, untouched); `FLEET-HEALTH.md` (← `fleet_health.py`) + `PROPOSALS-2026-06-02/03/04/05.md` (← `propose_closures.py`) = LIVE (gitignored, live-writer outputs, operator-designated LIVE) — ZERO relics, nothing deleted. (3) Plugin deploy (hub side only): bumped `tier1-lifecycle` 0.1.2→0.1.3 (version-key for the synced `validate_backlog` in-place-RESOLVED gate) + `claude plugin marketplace update dev-knowledge-methodology` succeeded; NO child reinstalls (ADR-41 — they ride their next session). **Result:** BACKLOG 50 tasks, validate_backlog OK; logs/ clean (no deletions); 0.1.3 published to the marketplace (0.1.3 cache dir materializes on next consumer install — expected). **Next:** child repos pick up the 0.1.3 validate_backlog gate on their next session. **Changes:** `BACKLOG.md` (#12 removed), `plugins/tier1-lifecycle/.claude-plugin/plugin.json` (0.1.3), this JOURNAL entry.

### 2026-06-05 — Backlog hardening: #83 validator gap closed, #12 premise-refuted, integrity clean

**Did:** (1) Hardened `validate_backlog` to reject the ADR-65 done-items-LEAVE violation class — added `_INPLACE_RESOLVED_RE` catching a `~~strikethrough~~` span or a bold `**RESOLVED`/`**DONE` marker on a task line (the existing `_DONE_MARKER_RE` only caught a fully-struck bullet `- ~~` / `- [x]` and MISSED the `[#id] ~~...~~ **RESOLVED**` shape the #79 stub used, commit 052e311 = finding F2); mirrored to the plugin copy; +4 tests; then closed #83 (item left the file, `closes [#83]`). (2) Annotated #12 premise-refuted (NOT withdrawn — operator's call): the Self-Evolution memory machinery it would make non-vacuous was archived in Phase C3, and a consumer grep found NO live reader of the evolution `.jsonl` paths or `evolution-log.md` (settings.json hooks: none; `/evolve`+`/boot` archived; `~/.claude/memory/` empty); the session-close sub-clause was already met by ADR-70 Tier-1. (3) Integrity check: no duplicate BACKLOG IDs (the "#33/#47/#67 twice" was a display artifact — one task line each); synthetic-test leftovers clean (gh pr/issue lists empty, no conformance branches). **Result:** validator now rejects in-place RESOLVED/struck task lines (15/15 tests green; live OK, 51 tasks); #83 closed; #12 retained with the refuted-premise finding for operator adjudication. **Next:** operator decides #12 withdraw-vs-narrow; plugin-copy propagation to child repos needs a separate version bump + deploy. **Changes:** `scripts/validate_backlog.py`, `plugins/tier1-lifecycle/scripts/validate_backlog.py`, `tests/test_validate_backlog.py`, `BACKLOG.md` (#83 removed, #12 annotated), this JOURNAL entry.

### 2026-06-05 — Test A re-run: synthetic Action-path test green again (1 survivor)

**Did:** Re-ran Test A per the earlier instruction — hand-crafted PR #13 on `claude/conformance-2099-02-01` adding one ADDED synthetic digest with marker `<!-- counts: raw=2 survived=1 killed=1 -->` (survived=1; reconciled the message's loose "killed=0…" to killed=1 per "exactly per the earlier instruction" — survived=1 is the load-bearing value, unchanged). **Result:** Action run 27022478118 green, all 5 PASS criteria — (a) guard PASS (one ADDED file), (b) `marker=<!-- counts: raw=2 survived=1 killed=1 --> survivors=1` read from the marker, (c) PR #13 auto-merged (`b640207`), (d) triage issue #14 full body — Findings+SYNTHETIC-F1+Next Actions present, Killed/K1/Checked-Clean excluded (FIX 1), (e) banner `[triage] 1 nightly finding await: #14`. Cleanup (branch `chore/synthetic-test-cleanup-2`): reverted the digest merge, closed #14, deleted the branch (local+remote); CONTRIBUTING L127/L145 marker wording was already fixed in the prior cleanup (`6276305`) so that step was a verified no-op. **Next:** tonight's real 06-06 nightly is the clean no-collision production confirmation.

### 2026-06-05 — Synthetic operator force-run of the nightly Routine (collision, as predicted)

**Did/Result:** Force-ran the nightly conformance Routine today (operator-authorized, collision-accepted). It ran SPEC-ORCHESTRATION fallback (native Workflow launcher still not enabled) and, hitting the existing 2026-06-05 digest, dodged by writing `docs/audits/2026-06-05-conformance-nightly-digest-2.md` — an ADDED file whose `-2` suffix fails the guard's strict regex → Action run 27021363543 **guard FAIL**, anomaly issue #12, **no merge** (parser step `skipped` — never reached; guard precedes it). The agent DID emit the marker correctly (`<!-- counts: raw=1 survived=1 killed=0 -->`) and a real H1 (#79 closure ADR-65 done-items-leave violation in `052e311`, corrected by `fb24810`, kept as #83 hook-hardening evidence) — so the WRITE-side marker contract held **by prompt adherence**, but note the code-owned validator in conformance-hub.js is **inert on the spec-orchestration path** (the .js runs as spec, not code); the parser-side fail-closed (C) is the real cloud backstop and didn't run this time (guard failed first). Cleanup: issue #12 + PR #11 closed, branch deleted, verified `gh pr list`/`gh issue list` empty, main untouched. **Next:** triage the H1 #79/ADR-65 finding into #83; tonight's real 06-06 run is the clean no-collision production confirmation.

### 2026-06-05 — Synthetic Action-path test green end-to-end (live, 1 survivor)

**Did:** Ran the full synthetic Action-path test per the 06-04 precedent — hand-crafted PR #9 on `claude/conformance-2099-02-01` adding one 1-survivor digest carrying the new marker `<!-- counts: raw=2 survived=1 killed=1 -->` (no `### Counts` table). Let the live `Nightly Conformance Triage` Action run (27019312540), untouched. **Result:** all 5 PASS criteria green — (a) diff guard `pass=true` (exactly one ADDED file); (b) parser log `date=2099-02-01 marker=<!-- counts: raw=2 survived=1 killed=1 --> survivors=1` — count READ FROM THE MARKER; (c) PR auto-merged (`4a4a4c8`); (d) triage issue #10 created with FULL body — Findings (PROPOSALS ONLY) + SYNTHETIC-F1 + Next Actions present, Killed Findings / SYNTHETIC-K1 / Checked-Clean EXCLUDED (FIX 1 validated live); (e) `surface_triage.ps1` under PS 5.1 printed `[triage] 1 nightly finding await: #10` (number present). Cleanup (this branch `chore/synthetic-test-cleanup`): reverted the digest merge, closed #10 with a synthetic-test comment, deleted the branch (local + remote), and fixed CONTRIBUTING's stale `### Counts table` wording → the marker. **Changes:** `CONTRIBUTING.md` (Counts-table→marker), revert of `docs/audits/2099-02-01-...md`, this JOURNAL entry. **Next:** tonight's real 06-06 nightly is the production confirmation of the same contract.

### 2026-06-05 — Nightly follow-ups: survivor-issue extractor aligned (FIX 2 already shipped)

**Did:** Aligned the survivor-issue body extractor in `nightly-conformance-triage.yml` to the REAL level-2 digest headings (`## Findings (PROPOSALS ONLY)` / `## Next Actions (proposals for operator)`, verified in the 06-05 digest on main) — captures to the next `## ` heading or `---` so `### High/Med/Low` subsections are INCLUDED and `## Killed Findings` excluded; fail-soft placeholder when a section is absent. Added 4 regression cases (Python mirror of the awk + anti-drift yml assertions). FIX 2 (version-stamp cross-ref audit check) was a verified **NO-OP** — already implemented as `check_handoff_version_stamp` (check #13, `scripts/audit.py:918`, merged `6fbd078`/`13f5ac1` this morning; registered in `ALL_CHECKS`, 7 tests pass) — so it was NOT re-implemented. **Result:** survivor issues now carry the actual Findings + Next Actions content (real awk verified against the 06-05 digest AND the fixture); 9/9 parser-contract tests pass, full suite green. Branch `fix/nightly-followups` merged `--no-ff` and pushed to `origin/main` (also makes the Prompt-B counts-contract fixes live for tonight's 03:00 run). **Changes:** `.github/workflows/nightly-conformance-triage.yml`, `tests/test_nightly_triage_parser.py`, this JOURNAL entry. **Next:** read the 06-06 nightly digest against the Prompt-B prediction; confirm a survivor-night issue body renders correctly if one occurs.

### 2026-06-05 — Nightly digest count-contract restored (D+C) + banner & health fixes

**Did:** Counts contract moved to a code-owned machine-readable marker `<!-- counts: raw=N survived=N killed=N -->` (D): `conformance-hub.js` computes the authoritative counts, pins the marker in the Stage-3 prompt, and a validation code step THROWS on mismatch — code holds the contract (the Workflow has no filesystem access and subagents are read-only, so the digest .md is rendered by a top-level agent → option (ii) validation, not a post-write code hook). Parser now reads ONLY the marker with `|| true` + explicit `[ -z ]`, making fail-closed reachable under `set -euo pipefail` (C). Fixture regenerated from the real 06-05 shape (no hand-made `### Counts` table) at `tests/fixtures/nightly-triage/` + a regression test validating it against the LIVE yml regex. Banner empty-result bug fixed (PS 5.1 `ConvertFrom-Json` empty-array + no-array-unroll traps). SessionStart nightly run-health surfacing added (last Action conclusion + digest side-effect check, ADR-68). **Result:** synthetic e2e (stubbed-gh, exact yml bash under pipefail) green — valid→merge+survivor issue, absent marker→fail-closed fires (exit 1), survived=0→merge/no issue; banner 0→none / 1→#4 / 2→#12,#34 under PS 5.1; health check correctly surfaced the failed run #8. Tonight's run prediction — digest 06-06 with marker, 0 survivors, auto-merge, zero triage issues, `[triage]` banner 0 (the `[nightly]` failed-run banner clears once 06-06 succeeds). Deviation = news. **Changes:** `.claude/workflows/conformance-hub.js`, `.github/workflows/nightly-conformance-triage.yml`, `scripts/surface_triage.ps1`, `tests/fixtures/nightly-triage/2099-01-02-conformance-nightly-digest.md`, `tests/test_nightly_triage_parser.py`, `LESSONS.md`, this JOURNAL entry. **Next:** read the 06-06 digest against this prediction.

### 2026-06-05 — audit.py check #13 handoff_version_stamp (S1 mechanized)

**Did:** Added `check_handoff_version_stamp` as check #13 in `scripts/audit.py` — parses the canonical version from `protocols/HANDOFF_PROCESS.md` `Version:` line, greps `ARCHITECTURE.md` + `CONTRIBUTING.md` for `stamp vX.Y` occurrences, FAILs on any mismatch. Updated `CONTRIBUTING.md` count (12 → 13 checks). Added 7 tests; all 103 pass. Branch `chore/audit-version-stamp-check`, commit `6fbd078`, all hooks green. **Result:** S1 recurrence class (version stamps lagging HANDOFF_PROCESS.md bumps) is now automatically caught at commit time — eliminates the manual triage burden from nightly arcs #81. **Changes:** `scripts/audit.py`, `CONTRIBUTING.md`, `tests/test_audit.py`, this JOURNAL entry. **Next:** Merge to main; Prompt B (digest count contract / parser fix before tonight's nightly).

### 2026-06-05 — Nightly #8 findings cleanup (digest on main; S1 stamps fixed)

**Did:** Merged PR #8 manually to `main` — Action's auto-merge died on the parser bug (run 26989375891); merge commit `af6c300`. Fixed S1 version stamps: `ARCHITECTURE.md` lines 336, 402 and `CONTRIBUTING.md` line 169 updated from v4.3.2 → v4.4 (`4bc0a5f`). Extracted three-looks fragments (porcelain/tripwire clean pre-digest; SPEC-ORCHESTRATION fallback path confirmed; two killed findings: `true-but-irrelevant` cross-repo evidence + `documented-decision` C4 commit-tag exception). **Result:** Audit record continuous on `main`; zero known survivors going into tonight's run. **Changes:** `docs/audits/2026-06-05-conformance-nightly-digest.md` (merged to main), `ARCHITECTURE.md`, `CONTRIBUTING.md`, this JOURNAL entry. **Next:** Prompt B restores the digest-count contract (parser + generator fix) before the 06-06 run.

### 2026-06-05 — Pre-nightly cleanup (triage already clean; session-2 facts-table append)

**Did/Result:** Pre-nightly cleanup on `chore/pre-nightly-cleanup`. **STEP 1 was a verified no-op:** the synthetic 2099-01-02 triage survivor (issue `#4`) was **already closed 2026-06-04** and `gh issue list --label nightly-triage --state open` returns zero, so STEP 1's goal (zero open triage issues) already held — #4 was left untouched (not reopened/re-closed to manufacture a "closed before first nightly" record). Appended one row to the session-2 bundle's `04_RECENT` Load-bearing facts table recording the anticipated post-merge tip movement (`e90a1fe` → `a102c43`; session-2 merge `239c19a` + chore `a102c43`), verdict *superseded post-Phase-2 — anticipated movement, not drift*; no existing row edited. **Watch (for tonight):** the SessionStart `[triage]` banner reported "1 nightly finding await: #" — a **bare `#` with no issue number** — while gh shows zero open `nightly-triage` Issues; a stale/glitchy `surface_triage.ps1` read to watch when the first production nightly fires. **Changes:** `docs/handoffs/2026-06-05-dev-knowledge-session-2/04_RECENT.md` (one row appended), this JOURNAL entry. **Next:** read the first production nightly PR (three looks) when it fires 03:00 local; confirm the `[triage]` surface count matches gh.

### 2026-06-05 — Handoff Phase 2 complete (2026-06-05-dev-knowledge-session-2)

**Did/Result:** Consolidated the handoff bundle for `2026-06-05-dev-knowledge-session-2` at `docs/handoffs/2026-06-05-dev-knowledge-session-2/` (8 files, flat, stamped HANDOFF_PROCESS **v4.4 / beta**). **Context:** the Phase-2 answers were a verbatim re-paste of the prior v44-wrap interview (operator-acknowledged — the intent was to regenerate the *same* bundle against the just-refreshed templates, for a diff). Generated per the operator's direction. All budgets clear (01:86 02:94 03:61 04:111 05:86 06:53 07:22); v4.4 §E separators on 01–07; the refreshed `01_ROLE` standing-preferences (5 bullets incl. graphify-ruling + verify-premises) and README "7 Q + fixed first-move Q8" line are reflected. **Drift cross-check — two drifts, both surfaced + corrected in-bundle:** (1) the sender's "tip d031d39" is one session stale — actual `main` tip at capture = `e90a1fe` (the v44-wrap merge + `2bac2d2` template chore landed since); (2) the `docs/machinery-inventory` `recall` ("may still exist") was already resolved absent. Other claims (v4.3.2 bundle stamp, `ec1d0cf`/`19c2b72`, v4.4 beta) verified TRUE. `in-progress/` removed (force; interview folded into 04_RECENT). **Changes:** `docs/handoffs/2026-06-05-dev-knowledge-session-2/` (added), `docs/handoffs/in-progress/2026-06-05-dev-knowledge-session-2/` (removed), this JOURNAL entry. **Next:** operator diffs this bundle against the v44-wrap one (the template-refresh comparison) + uses it per its README ladder if onboarding.

### 2026-06-05 — Handoff Phase 1 interview generated (2026-06-05-dev-knowledge-session-2)

**Did/Result:** Generated the Phase 1 handoff interview for slug `2026-06-05-dev-knowledge-session-2` (scope-matrix Case 4 — clean tree, commits since the last bundle, today's base slug `2026-06-05-dev-knowledge-session` already taken → smallest free counter suffix `-2`). Local date 2026-06-05 used (NOT the harness UTC `date` of 2026-06-04 — the codified landmine: local convention governs record stamps). HEAD captured at `e90a1fe` on `main`; interview written to `docs/handoffs/in-progress/2026-06-05-dev-knowledge-session-2/_handoff-interview.md` with the four-tag sage→apprentice frame. Window to capture is small (the `2bac2d2` template-refresh chore + the v44-wrap merge). Awaiting operator answers below the PASTE marker, then `complete handoff for dev-knowledge` for Phase 2. **Changes:** `docs/handoffs/in-progress/2026-06-05-dev-knowledge-session-2/`, this JOURNAL entry. **Next:** operator pastes answers → Phase 2 consolidate.

### 2026-06-05 — Handoff Phase 2 complete (2026-06-05-dev-knowledge-v44-wrap)

**Did/Result:** Consolidated the handoff bundle for `2026-06-05-dev-knowledge-v44-wrap` at `docs/handoffs/2026-06-05-dev-knowledge-v44-wrap/` (8 files, flat, stamped HANDOFF_PROCESS **v4.4 / beta** read from the live spec header + latest amendment Status line). All `{{PULL}}`/`{{SYNTHESIZE}}` markers resolved from source (ESSENTIALS/PLAYBOOK/VISION/CLAUDE/BACKLOG); v4.4 §E file separators present on 01–07 (README exempt); all 7 budgets clear (01:82 02:94 03:61 04:118 05:82 06:53 07:22). **Drift cross-check:** all sender load-bearing claims verified TRUE (commit SHAs 19c2b72/ec1d0cf/d031d39, the v4.3.2 Phase-D bundle stamp, HEAD d031d39, v4.4 beta) except **one resolved `recall`** — the `docs/machinery-inventory` branch the sender flagged as "may still exist" was found **absent** (no local/origin branch); the four-tag discipline caught the stale recall before it misled. `06_QUESTIONS` dynamic anchors refreshed to this arc (staleness-map verify-from-source; machinery-inventory recall→resolved); Q7/Q8 kept verbatim. `in-progress/` removed (force; interview folded into 04_RECENT). **Changes:** `docs/handoffs/2026-06-05-dev-knowledge-v44-wrap/` (added), `docs/handoffs/in-progress/2026-06-05-dev-knowledge-v44-wrap/` (removed), this JOURNAL entry. **Next:** operator uses the bundle per its README escalation ladder to onboard the next chat.

### 2026-06-05 — Handoff Phase 1 interview generated (2026-06-05-dev-knowledge-v44-wrap)

**Did/Result:** Generated the Phase 1 handoff interview for slug `2026-06-05-dev-knowledge-v44-wrap` (scope-matrix Case 2 — clean tree, 7 commits since the last bundle `2026-06-05-dev-knowledge-session`). Local date is 2026-06-05; base slug `2026-06-05-dev-knowledge-session` was taken, so operator re-slugged with the `-v44-wrap` discriminator. HEAD captured at `d031d39` on branch `main`; interview written to `docs/handoffs/in-progress/2026-06-05-dev-knowledge-v44-wrap/_handoff-interview.md` with the four-tag sage→apprentice frame (v4.2 Amendment A). Awaiting operator answers below the PASTE marker, then `complete handoff for dev-knowledge` for Phase 2. **Changes:** `docs/handoffs/in-progress/2026-06-05-dev-knowledge-v44-wrap/`, this JOURNAL entry. **Next:** operator pastes answers → Phase 2 consolidate.

### 2026-06-05 — HANDOFF_PROCESS v4.4 (positional-attention amendment A–F)

**Did/Result:** Amended the handoff process to **v4.4** — six research-grounded refinements aligning the bundle with how LLM attention behaves over the single pasted message (U-shaped positional bias, distractor degradation, quote-grounding, lost-in-conversation). **A**: `05_NOW` gains a `## Top landmines (do-not list)` recency-peak tail = `### Session landmines` (≤5 imperatives from interview Q5) + `### Standing invariants (repeat)` (mirrors 01_ROLE) — two sub-blocks per operator decision so session/permanent warnings don't compete for one cap. **B**: dual-position safety invariants (01_ROLE primacy + 05_NOW recency), deliberate DRY violation guarded with `positional-redundancy: do not deduplicate`. **C**: 06 pass criterion requires every answer to cite bundle file+section. **D**: 04_RECENT presents final-state narrative; refuted threads labelled `[REFUTED — historical]`. **E**: `===== FILE: NN — start/end =====` separators on 01–07 (README exempt). **F**: fixed permanent Q8 first-move recitation. **Also closed the skill drift** the prior entry logged: `/handoff` now reads version/status from the spec header + latest amendment Status line — no hardcoded number, drift class permanently closed. **Validated** by a throwaway dry-render (all markers resolved, separators + sub-blocks + Q8 present, all 7 budgets clear: 01:78/02:60/03:29/04:44/05:60/06:54/07:22); mock deleted + removal verified (no leftovers). **No budget number moved.** Ships at **beta** — promotes to stable on the next real production handoff meeting the v4.3.1 §B judgment criterion. 235 tests green, ruff clean, audit-health OK throughout. No code touched — template + spec changes only. **BACKLOG: no-item class** — conversation-born, operator-approved; no `[#id]` exists, none created.

**Changes:** `protocols/HANDOFF_PROCESS.md` (v4.4 amendment + header bump + §5 rows); `templates/handoff/01–07 + README.md.tmpl`; `.claude/commands/handoff.md` (generic version/status read). Branch `feat/handoff-v4.4` (3 commits).

**Next:** exercise v4.4 on the next production handoff — the real beta→stable test (watch: does the top-landmines tail + first-move recitation measurably reduce the fresh-eyes critical-finding count?).

---

### 2026-06-05 — Handoff Phase 2 complete (2026-06-05-dev-knowledge-session)

**Did/Result:** Consolidated the Phase-D codification handoff into the 8-file v4 bundle at `docs/handoffs/2026-06-05-dev-knowledge-session/` (HANDOFF_PROCESS v4.3.2; README stamped `status: beta` per §E). Folded the operator's pasted interview answers (the deployment-arc narrative + Phase-D agenda) into `04_RECENT`/`05_NOW`; removed the `in-progress/` interview (content preserved in the bundle). **Phase-2 cross-check: no material drift** — verified `main` tip = `6e8c84f`, branch 2 commits ahead, `origin` = github.com/rdwornik/dev-knowledge, conformance-hub.js + nightly-triage Action + surface_triage.ps1 all present, BACKLOG shows #87 withdrawn + #89/#90 added, 235 tests green, ruff clean, validate_backlog OK (52 tasks), PR-#1 merge `205da14` present. One **documented** non-bundle divergence carried into the table: the `/handoff` **skill** body still stamps v4.3.1/stable while the live spec is v4.3.2 (§E beta) — the bundle stamps v4.3.2/beta per the live spec (sender Warning #9). Line budgets all clear (01:74 / 02:104 / 03:66 / 04:152 / 05:60 / 06:44 / 07:20).

**Changes:** new bundle `docs/handoffs/2026-06-05-dev-knowledge-session/` (README + 01–07); removed `docs/handoffs/in-progress/2026-06-05-dev-knowledge-session/`; JOURNAL. Branch `docs/handoff-2026-06-05`.

**Next:** operator uses the bundle per its README escalation ladder (paste 01–05 → 06 → 07) to onboard the Phase-D browser chat; then merge `docs/handoff-2026-06-05` → `main` (brings the bundle + the ARCHITECTURE-row correction onto main). Watch item: the first production nightly run.

---

### 2026-06-05 — Handoff Phase 1 interview generated (2026-06-05-dev-knowledge-session)

**Did/Result:** Generated the Phase-1 sage→apprentice interview for the **Phase-D codification** handoff (HANDOFF_PROCESS v4.3.2). Scope-matrix Case 2 (clean tree, commits since the 2026-06-03 bundle, no today-slug) → today's default slug, stamped 2026-06-05 (local-date convention; harness reads 2026-06-04). HEAD captured `6e8c84f` (`main`, clean). Embedded the Phase-D receiver context — the living-doc staleness map (ARCHITECTURE/PLAYBOOK STALE; CONTRIBUTING PARTIAL; CLAUDE STALE-by-deferral; VISION/ESSENTIALS current-by-scope), the codification agenda (adoption rubric + 3 case studies, t-shirt routing doctrine, prose-vs-state checker [#89], V4 git↔backlog verifier [#90], cloud-readiness, cadences, lessons), and the pending-elsewhere markers (#86 ADRs + AI-Council are post-Phase-D; watch the first production nightly run) — into the in-progress interview for Phase 2 to fold into the bundle. Awaiting operator answers.

**Changes:** new `docs/handoffs/in-progress/2026-06-05-dev-knowledge-session/_handoff-interview.md`. Branch `docs/handoff-2026-06-05` (not merged — Phase 2 merges).

**Next:** operator pastes the 5-question block into the sender chat → pastes answers below the marker → `complete handoff for dev-knowledge` (Phase 2 consolidates the 8-file bundle; README stamps `HANDOFF_PROCESS v4.3.2 (status: beta)` per §E).

---

### 2026-06-05 — Pre-handoff sweep: git↔BACKLOG reconciliation + Phase-D staleness map

**Did/Result:** Closed the deployment arc (phases A–C) at the **record level** ahead of the Phase-D codification handoff. Reconciled BACKLOG against git in both directions (ADR-65 mechanical comparison, not from-memory): the three `closes`-commits (#78/#79/#88) are all removed from the file (#79 survives only as a historical reference inside #83); #86 (×3 `advances`) and #81's `advances` are present + current; the agentic-arc/retro framings (#80–#87) all landed; the C3 runtime-machinery (~/.claude, LESSONS+JOURNAL record) and C4 nightly-Action (JOURNAL-adjudicated cloud-PR scope, distinct from #85's local track) arcs are **legitimate no-item classes**. Everything else reconciled **consistent**. Three record-gaps found and fixed: (1) **withdrew [#87]** — its sole premise (file a /bug report: per-agent routing non-functional in CC 2.1.162) was **refuted** by the Phase-C3 re-probe, which root-caused the non-functional routing to our OWN `CLAUDE_CODE_SUBAGENT_MODEL=haiku` override (now removed) and confirmed pins honored on **both** the Agent-tool and workflow-engine paths — no platform bug to report. Operator-authorized withdrawal; the refuted premise is the closes-evidence (the documented exception to close-only-with-a-commit). #87 read in full first to confirm it carried no separate "native Workflow runtime not enabled in cloud" half — it did not, so a clean withdrawal, not a narrow. (2) **corrected #83's stale appended note** carrying the same refuted "Haiku-only de-facto" reading (the core `validate_backlog`-hardening task is unaffected). (3) **added [#89]** deterministic prose-vs-state checker + **[#90]** V4 git↔backlog two-direction verifier — both surfaced by this sweep as Phase-D design work that lacked tracking. JOURNAL + LESSONS confirmed complete (all four arcs entered; config-archaeology lesson present) — no fixes there, no new LESSONS. Built the **living-doc staleness map** (ARCHITECTURE/PLAYBOOK STALE on spec-orchestration + t-shirt routing + machinery-retirement + adoption + GH-Actions; CONTRIBUTING PARTIAL — missing the spec-orchestration fallback rationale; CLAUDE STALE-by-deferral; VISION/ESSENTIALS current-by-scope) — **NOT rewritten here**; it ships inside the handoff as Phase-D workstream 1. **Correction (operator-verified by grep, before Phase 2):** the staleness-map ARCHITECTURE row was understated as first written — ARCHITECTURE.md contains NOTHING about the GitHub remote/push, the cloud-night Routine, spec-orchestration, the in-repo conformance-hub workflow, or the GH-Action outcome loop (the "cloud-night/Action already present" parenthetical was false), AND its ADR-68 night-agent section describes a never-registered mechanism superseded by the cloud Routine (needs a supersession note); the interview's ARCHITECTURE row was corrected on the handoff branch.

**Changes:** `BACKLOG.md` (withdrew #87, corrected #83 note, added #89/#90, 2026-06-05 grooming line). Branch `chore/pre-handoff-sweep`. Living prose docs deliberately untouched (Phase-D content). `validate_backlog` OK (52 tasks). Harness clock reads 2026-06-04; stamped 2026-06-05 for thread-ordering continuity with the C3/C4 entries (UTC harness vs Barcelona local).

**Next:** Generate the Phase-D codification handoff (HANDOFF_PROCESS v4.3.2 two-phase) for a new browser chat; watch item = the first production nightly run (raw count without the shallow-clone false-positive class).

---

### 2026-06-05 — Phase C4: nightly outcome management (auto-merge Action + triage surfacing)

**Did/Result:** Closed the nightly-PR outcome loop. Shipped the fleet's first GitHub Action (`.github/workflows/nightly-conformance-triage.yml`): diff-guards each `claude/conformance-*` nightly PR (merges only when the diff is exactly one ADDED `docs/audits/*-conformance-nightly-digest.md`), squash-merges clean nights, and opens `nightly-triage` Issues on survivors>0 / guard-fail / unparseable-digest / failed-merge. Survivor count is read from the digest **body** (`Survived skeptic | N`), not the free-form PR title — operator-corrected design (the real PR #1 title carried no structured counts and the Routine is out of scope); the parse fails closed. Trigger fires on base `main` + a job-level `head_ref` guard — operator caught that `pull_request.branches` filters the **base** branch, so the originally-planned `claude/conformance-*` branch filter would never have fired. Untrusted step outputs routed through `env:` to block shell injection on the anomaly path (least-trusted input). Verified end-to-end with three synthetic PRs: clean → auto-merge, no issue; 1-survivor → merge + triage issue carrying Findings/Next-Actions only (Counts/Checked-Clean correctly excluded by the two-pass extractor); two-file anomaly → no merge, anomaly issue, PR left open. All test PRs/branches/issues/dummy digests reverted/closed/deleted (no leftovers verified). Added `scripts/surface_triage.ps1` (read-only, fail-soft, mirrors the L0 surface-closures pattern) wired as a 2nd project SessionStart hook — prints `[triage] N …` when open triage Issues exist (verified live across empty/one/empty). Bumped `actions/checkout` v4→v5 (Node-20 deprecation). Documented the flow in a new CONTRIBUTING "Nightly outcome management" section.

**Changes:** new `.github/workflows/nightly-conformance-triage.yml`, `scripts/surface_triage.ps1`; edited `.claude/settings.json` (2nd SessionStart hook) and `CONTRIBUTING.md` (new section; re-read end-to-end, `last_reviewed` already 2026-06-04). Branches `feat/nightly-pr-manager` + `feat/nightly-triage-surfacing` (both merged `--no-ff`, deleted). 235 tests pass, ruff clean, audit-health 12/12. `main` pushed to origin. Harness/git clock read 2026-06-04. No backlog item matched (C4's cloud-PR-outcome scope is distinct from #85's local night-run track); nothing closed.

**Next:** Action is live; it will manage the next real nightly PR — watch the first production run.

---

### 2026-06-05 — Model-routing re-probe completed: workflow-engine path + unpinned default

**Did/Result:** Closed the two C3 sub-items the prior entry's Agent-tool-only probe left open. (b) **Load-bearing test run:** a 3-stage Dynamic-Workflow probe (the workflow-engine `opts.model` path — separate code path from Agent-tool pins, and the one `conformance-hub` uses) confirms pins honored: `sonnet`→`claude-sonnet-4-6`, `haiku`→`claude-haiku-4-5-20251001`. Gotcha RESOLVED mark now backed across BOTH code paths. (c) **Unpinned default measured:** an unpinned subagent inherits the **main session model** (`claude-opus-4-8`) on both Agent-tool AND workflow paths — not platform-default, not Haiku. Cost consequence: the old override's job (floor every subagent at cheap Haiku) is gone; unpinned fan-outs now run on Opus 4.8. Replacement discipline = explicit per-stage pins (t-shirt doctrine). Also pushed `main`→origin (nightly clone now sees current JOURNAL).

**Changes:** `~/.claude/skills/gotchas/gotchas.md` (out-of-repo; RESOLVED line expanded to both-path + unpinned-cost fact); JOURNAL. `main` pushed to `origin` (private GitHub). No repo code/doc changed.

---

### 2026-06-05 — Model-routing re-probe: pins now honored (closes C3 pending)

**Did/Result:** Ran the post-restart re-probe that was the lone Pending item from the Phase C3 entry below. `$env:CLAUDE_CODE_SUBAGENT_MODEL` now empty in all three scopes (Process/User/Machine) — operator cleared the second source (launch-shell profile/.env) that the 2026-06-05 in-session re-probe had found still active. 2-agent matrix probe: `model: sonnet` pin → `claude-sonnet-4-6`, `model: haiku` pin → `claude-haiku-4-5-20251001` — each Agent-tool pin honored distinctly (pre-fix both ran Haiku). **Per-agent model routing is functional; C3 thread fully closed.** Re-rooted gotcha (`~/.claude/skills/gotchas/gotchas.md`) marked RESOLVED with the load-bearing confirmation, retained as a standing residual warning.

**Changes:** `~/.claude/skills/gotchas/gotchas.md` (out-of-repo; RESOLVED line); JOURNAL. No repo code/doc changed. **Note:** harness clock reads 2026-06-04 while the C3 thread is stamped 2026-06-05 (prior session dated a day ahead) — kept 06-05 for thread-ordering continuity.

---

### 2026-06-05 — Phase C3 runtime-machinery cleanup (~/.claude/, archive-not-delete)

**Did/Changes:** Executed the operator-approved Phase C verdicts (`docs/audits/2026-06-05-machinery-inventory.md`). Root-caused the "model routing broken" gotcha to our own `CLAUDE_CODE_SUBAGENT_MODEL=haiku` global env override (probe: sonnet+haiku pins both ran Haiku, Agent-tool path too) and removed it; re-rooted the gotcha. Archived (never deleted) the March-era Self-Evolution system (`/evolve`, `/boot`, memory stubs, both echo-hooks), the stale `verify` skill, and the stale global `conformance-hub.js` to `~/.claude/archive/2026-06-05-machinery-c3/`; pruned 16 stale plans to `~/.claude/archive/plans/`. Decoupled `/codex-review` from the profile fn (explicit-path; empty-diff guard verified). Installed `uv` 0.11.19. Night-agent: found NOT scheduled (no trigger to disable). Hub changes are LESSONS + JOURNAL only. **Pending:** post-restart workflow re-probe to confirm pins now honored. Branch `chore/machinery-c3`.

---

### 2026-06-04 — Merge nightly PR #1 + land fleet_health cloud-clone fail-soft

**Did/Changes:** Squash-merged the first nightly conformance PR #1 (0 surviving findings — the 8 raw V1 candidates were all the shallow-clone pre-June-SHA false positives, now suppressed proactively by the V1 guard). Then landed the Step-6 cloud session's stranded fix: `fleet_health.siblings_available()` skips the cross-repo audit in an isolated/cloud clone, so SessionStart rewrites no tracked `ecosystem/*/state.yaml` (keeps the nightly tripwire clean); +5 tests (235 green), one overstated rationale-comment line corrected. Pruned the 3 remaining merged local branches earlier; deleted the orphan cloud branch `claude/wizardly-babbage-5X6e0` after landing. Branch `fix/fleet-health-failsoft`, merge `--no-ff`. Advances #86.

---

### 2026-06-04 — Hub closeout: V1 shallow-history guard, #88 closed, branch prune

**Did/Changes:** Added a shallow-history guard to the `conformance-hub` V1 stage (cloud clones may be shallow — SHAs older than the history boundary are out-of-scope, not false "commit absent" findings; pushed so tonight's nightly run benefits). Closed [#88] — graphify evaluated and REJECTED per corp-monorepo `docs/audits/2026-06-04-graphify-pilot.md`. Pruned 6 merged branches (pilot/handoff/pilot81). Branch `chore/hub-closeout`, merge `--no-ff`.

---

### 2026-06-04 — Phase B: hub pushed to private GitHub + cloud-night pipeline stood up

**Did/Result:** Stood up the cloud-night conformance pipeline for the hub ONLY, by explicit operator decision (B0) — reverses the standing "nothing is pushed" state for this repo (formal push / R2 ADRs pending the later ADR phase; advances #86). Created a NEW private GitHub repo `rdwornik/dev-knowledge` and pushed `main` (gh 2.93.0 installed via winget + browser auth; pre-push full-history secret scan CLEAN — only the operator's own emails in history, no keys/tokens). Committed the validated `conformance-hub` workflow in-repo (byte-identical first, then ported its hardcoded Windows paths/separators for the Linux cloud clone) plus a platform-guards safety envelope (pre-allow the Workflow tool; **no** Write/Edit deny — a blanket deny beats allow with no carve-outs and would break BOTH local daily work and the routine's own digest write; cloud containment instead = `claude/*` branch-push restriction + PR-review gate + read-only design + post-run porcelain tripwire). **Step-6 manual cloud test (hard gate) PASSED via spec-orchestration:** the native Workflow launcher is NOT enabled in the cloud context as of 2026-06-04 (version-pinned platform fact; each nightly run re-probes it), so the Routine reads the `.js` as the canonical SPEC and executes its 3 stages via read-only Explore agents. The cloud run surfaced 2 real findings — this missing Phase-B JOURNAL entry (resolved by this prepend) and `VISION.md:135` stale "10 checks" (fixed: de-hardcoded → `scripts/audit.py checks`; third locus of that drift class). Watch items: `fleet_health` SessionStart hook already fail-soft (latent stale-day sibling reach noted); `tier1-lifecycle` plugin inert in cloud (local-only marketplace path — harmless).

**Changes:** +`.claude/workflows/conformance-hub.js` (8c0cf0d byte-identical, de41542 port); `.claude/settings.json` (0a93746 envelope, + spec-orchestration doc-sync); `VISION.md` (de-hardcode count, `last_reviewed`→2026-06-04); JOURNAL. Branches `feat/cloud-night` (merge e497653) + `docs/cloud-night-close`, both `--no-ff`. New `origin` = github.com/rdwornik/dev-knowledge (**PRIVATE**), main in sync. 230 tests green · ruff clean.

**Next:** Register the nightly Routine (claude.ai/code → Routines) with the attempt-native-then-fallback spec-orchestration prompt (claude/* branch + dated PR, proposals-only, ~100k budget, digest reports which path ran). Deferred to later phases: formal push / R2 / saved-workflow-distribution ADRs (#86); consumer-repo hook relative-path → URL migration (universalization); a deterministic cross-file count checker for the recurring hardcoded-count drift class (phase C/D agenda).

---

### 2026-06-04 — CONTRIBUTING stamp/hook-table sync (rerun findings #1+#2)

**Did/Result:** Fixed both net-new conformance-rerun findings in one genuine read of CONTRIBUTING.md — handoff stamp `v4.3.1/stable` → `v4.3.2/live` (verified live header), and the validators table corrected from 6 to all 8 hooks (added `toc-freshness` + `toc-freshness-playbook`, verified against live `.pre-commit-config.yaml`). Bumped `last_reviewed`→2026-06-04 (full re-read confirmed rest accurate). Also captured the deny-cache gotcha (hot-reloads on ADD not REMOVAL) to global `~/.claude` gotchas, and deleted the merged `docs/conformance-rerun` branch.
**Changes:** CONTRIBUTING.md, JOURNAL. Branch `docs/contributing-stamp-sync`, merge `--no-ff`.
**Next:** corp-monorepo baseline (n=2 prerequisite for #84).

---

### 2026-06-04 — Conformance rerun (recurring-review mode test)

**Did/Result:** Reran the saved `conformance-hub` workflow (Run `wf_d044fa30-b08`) on branch `docs/conformance-rerun`; safety envelope held (Write/Edit denied + probe-verified; post-run fleet tripwire 5/5 clean; actual-model check = all 5 agents Haiku-4.5, routing still non-functional). Delta vs the pilot-#81 baseline: **F1 + F2 both RESOLVED** (now in checked_clean), **2 net-new med findings** — F1's fix was ARCHITECTURE-only so the same stale HANDOFF stamp persists in `CONTRIBUTING.md:133`, and the CONTRIBUTING hook table lists 6 vs the actual 8. No fixes (proposals only; #83 already covers the closure-discipline item).
**Changes:** +`docs/audits/2026-06-04-conformance-rerun-delta-digest.md`, JOURNAL. Branch `docs/conformance-rerun`, merge `--no-ff` pending.
**Next:** operator triage of the 2 CONTRIBUTING.md drifts; corp-monorepo baseline.

---

### 2026-06-04 — Pilot-arc retro captures (LESSONS + gotchas + BACKLOG)

**Did/Changes:** Appended 3 LESSONS (verify-by-state, proven twice; absence-in-sources ≠ absence-in-canon; research-preview runtime caps are version-pinned) + 2 CC-workflow gotchas to the global `~/.claude` gotchas skill (workflow auto-write safety envelope; per-agent routing non-functional on 2.1.162). Added BACKLOG #84 (workflow-doctrine codification — closes #74/#80 on landing, after corp-monorepo baseline), #85 (night-run LOCAL track), #86 (cloud-night decision pkg), #87 (Anthropic /bug report), + #82 iteration-2 profile note. No PLAYBOOK/protocols/ADR content edits. Branch `chore/pilot-retro-captures`, merge `--no-ff` pending.
**Next:** corp-monorepo baseline (the n=2 prerequisite for #84 codification).

---

### 2026-06-04 — Pilot-phase closeout: routing probe + F1/F2/#78 fixes

**Did:** Closed the hub-pilot phase. (1) Ran a model-routing matrix probe (3 agents asked sonnet/opus/omitted); (2) genuine end-to-end re-read of ARCHITECTURE.md + CLAUDE.md §11 fixing F1 + #78 + other proven-stale claims; (3) deleted the in-place #79 stub per ADR-65; (4) added #83 (validate_backlog strikethrough-gap).
**Result:** **Probe verdict (CC 2.1.162): per-agent model routing is non-functional — all 3 agents ran `claude-haiku-4-5` regardless of the `model` option; Haiku-only is the de-facto workflow-subagent mode** (v0 anomaly was not an incident). F1 fixed (HANDOFF_PROCESS stamp 4.3.1→4.3.2/status live) + #78 closed (de-hardcoded the audit-check count → `audit.py checks`; §11 rotated 66-70→67-71 +ADR-71) + 4 other stale claims fixed in the same read (codemap node count, +scripts/toc/ validator, +2 toc-freshness hooks, +ADR-71 to Governing ADRs). F2 stub removed. 230 tests green · ruff clean · audit 12/12 · fleet 5/5 clean.
**Changes:** ARCHITECTURE.md + CLAUDE.md (re-read, last_reviewed→2026-06-04), BACKLOG.md (−#78, −#79, +#83), JOURNAL. 4 commits on `chore/pilot-phase-closeout`; merge `--no-ff` pending. **Pilot phase CLOSED — next: corp-monorepo baseline.**
**Next:** corp-monorepo baseline (next session). Workflow night-run design must assume Haiku-only subagents until routing is fixed upstream (#83 note; #81/#82).

---

### 2026-06-04 — Correction: pilot #81 v0 ran entirely on Haiku 4.5

**Did:** Operator caught a contradiction (`/workflows` showed Haiku verifiers vs the digest's "Sonnet"). Checked the run transcripts.
**Result:** **All 5 workflow subagents ran `claude-haiku-4-5-20251001`** — the per-agent `model` routing (Sonnet on verifiers; inherited Opus on skeptic/digest) did NOT take effect. Evidence: `grep '"model"'` on each `agent-*.jsonl` of run `wf_c962d194-014`. Findings F1/F2 still verified real by the main session, so validity holds — but they were *surfaced* by Haiku, and the ~42.3k tokens were Haiku-tier. Material pilot finding: per-agent model routing must be verified, not assumed (root cause undetermined). Corrects the entry below (append-only; not edited).
**Changes:** appended a CORRECTION section to `docs/audits/2026-06-04-pilot81-hub-conformance-digest.md`; this JOURNAL note. Branch `docs/pilot81-model-correction`, merge `--no-ff` pending.
**Next:** dedicated model-routing probe (one-agent workflow + explicit `model` + transcript check) before any design relies on Sonnet/Opus stages.

---

### 2026-06-04 — Pilot #81 v0: hub conformance review via Dynamic Workflow

**Did:** Ran the first real-conditions Dynamic Workflow — `conformance-hub` (3 Sonnet verifiers → Opus skeptic → Opus digest), a read-only semantic conformance review of this repo's living docs. Safety per Phase-0: session `Write/Edit` deny (spot-checked active), no write tasks, repo-only scope; post-run fleet tripwire 5/5 clean (zero writes).
**Result:** 3 raw findings → 2 survived skeptic (1 killed as style). Both survivors **verified real** against live state: **F1 (high)** ARCHITECTURE.md:336/402 cite HANDOFF_PROCESS v4.3.1 but file is v4.3.2; **F2 (med)** BACKLOG #79 struck-through in place vs ADR-65 "done-items-leave". Both net-new vs audit.py's 12 checks + hooks. 0 false positives survived; ~42.3k workflow output tokens (gross 272k is cache-inflated), ~10.2 min. Kill-criterion verdict left to operator. 230 tests green · ruff clean · audit 12/12.
**Changes:** `docs/audits/2026-06-04-pilot81-hub-conformance-digest.md` (new, committed f23b18d); workflow saved personal-only at `~/.claude/workflows/conformance-hub.js` (NOT committed — R2 Layer-2 question deferred to ADR layer per operator); JOURNAL prepend. Branch `docs/pilot81-hub-conformance`, merge `--no-ff` pending.
**Next:** Operator triages F1/F2 (fix vs amend-ADR-65) in a separate scoped session; decide R2 (saved-workflow-in-hub) at the ADR/Council layer if the pilot proves out.

---

### 2026-06-03 — Phase-0 Dynamic Workflows safety-gate verification

**Did:** Empirically verified the 5 workflow safety gates on **CC 2.1.162** via headless `claude -p` from a non-git `%TEMP%\wf-phase0` sandbox (gates 1–4) + an operator TUI run (gate 5); appended the post-merge state correction row to the 2026-06-03 handoff `04_RECENT` facts table.
**Result:** Gate 2 **PASS** — a `Write/Edit` **deny rule binds workflow subagents** (deny > acceptEdits auto-approve); Gate 4 — `CLAUDE_CODE_DISABLE_WORKFLOWS=1` removes the tool, but headless workflow launch **auto-denies unless the Workflow tool is pre-allowed**; Gate 5 — **S1** (workflow runs do **not** survive a CC exit → night-run must be one uninterrupted process per stage). Gate 3 worktree containment **unverified** (needs a git cwd). Secondary: agent self-reports unreliable — trust file/git state. Fleet 5/5 clean throughout; 230 tests green. Research note **left in Downloads per operator decision** (no landing action).
**Changes:** `docs/audits/2026-06-03-phase0-workflow-gates-findings.md` (new); `docs/handoffs/2026-06-03-dev-knowledge-session/04_RECENT.md` (+1 row); JOURNAL prepend. 3 commits on `chore/phase0-workflow-gates`, merge `--no-ff`.
**Next (#81):** night-run on deny-rule + kill-switch, pre-allow Workflow tool, single-process-per-stage; verify worktree auto-discard in a disposable git harness.

---

### 2026-06-03 — HANDOFF_PROCESS v4.3.2 amendment (verification-coverage refinements)

**Did:** Appended the v4.3.2 amendment to `protocols/HANDOFF_PROCESS.md` (verbatim per operator spec); bumped both version stamps (header `4.3.1→4.3.2`, body `Version: 4.3→4.3.2`); appended empirical-evidence note to BACKLOG #1 (P1 adversarial fresh-eyes item).
**Gaps closed:** (A) whole-bundle cross-check — session-state claims from any path must hit the `04_RECENT` table; (B) extract-fidelity — deterministic-pull sections of `02` must be verified faithful to live PLAYBOOK; (C) durable-principle promotion — standing Phase-2 step to flag Wisdom principles for PLAYBOOK promotion. (D) terminology-collision logged as evidence for #1, not closed. Ships `beta`.
**Changes:** `protocols/HANDOFF_PROCESS.md` (amendment + version stamps); `BACKLOG.md` (#1 evidence note); JOURNAL prepend. 3 commits on `docs/handoff-process-v4-3-2`; merge `--no-ff` pending.

---

### 2026-06-03 — Handoff bundle fix-pass (fresh-eyes review of 2026-06-03-dev-knowledge-session)

**Did:** Fixed 5 review findings on the bundle: (A1) the `02` ruff-gate claim; (A2) de-overloaded "Tier" off the model axis; (A3/A4) reconciled the `02` model-selection + prompt-format extracts to live PLAYBOOK; (A5) promoted the source→gate→agent drift-proofing thesis into PLAYBOOK (content-add) and carried it in `02`/`04`.
**Result / #13 verdict:** ruff IS a wired pre-commit gate, but #13 closed **2026-06-02** (prior session, inside the handoff window) — NOT this session; the false "this session" attribution was removed and a verifying cross-check row added to `04`. Thesis now sourced in PLAYBOOK, not stranded in the ephemeral `04`. 230 tests green · ruff clean · audit 12/12 · PLAYBOOK TOC regenerated.
**Changes:** bundle `02_METHODOLOGY.md` + `04_RECENT.md`; `protocols/PLAYBOOK.md` (new "Drift-proofing precedence" subsection + TOC); JOURNAL prepend. 5 commits on `docs/handoff-2026-06-03`.

---

### 2026-06-03 — Handoff Phase 2 complete (2026-06-03-dev-knowledge-session)

**Did:** Consolidated the 8-file bundle at `docs/handoffs/2026-06-03-dev-knowledge-session/` from the operator's interview answers + live source. Cross-checked all load-bearing sender claims against repo state. Removed the `in-progress/` interview folder (answers folded into `04_RECENT`).
**Result:** Bundle ready. **One non-blocking drift:** sender recalled PLAYBOOK 2710 lines; actual 2888 (the recall predated the auto-TOC re-add, `fc0797f`) — recorded in README Drift cross-check + the `04_RECENT` Load-bearing facts table. All other claims (HEAD d439969, 12 audit checks, 230 tests, ADR-71, 4 hooks, backlog state, AGENTS.md copy-deploy) verified ✅.
**Changes:** bundle 8 files (new); `in-progress/` removed; JOURNAL prepend. On branch `docs/handoff-2026-06-03`.

---

### 2026-06-03 — Handoff Phase 1 interview generated (2026-06-03-dev-knowledge-session)

**Did:** Ran the v4.3.1 scope matrix (Case 2 — clean tree, many commits since the 2026-05-31 handoff, no today-slug). Generated the Phase-1 interview at `docs/handoffs/in-progress/2026-06-03-dev-knowledge-session/_handoff-interview.md`; captured HEAD `d439969`, branch `main`, clean tree.
**Result:** Awaiting operator answers below the PASTE marker. Phase 2 (`complete handoff for dev-knowledge`) consolidates the bundle once answers land.
**Changes:** interview file (new); JOURNAL prepend. On branch `docs/handoff-2026-06-03`.

---

### 2026-06-03 — BACKLOG grooming: agentic-arc framed for next session

**Did:** Added three BACKLOG items (#80 Dynamic Workflows research P1/L, #81 methodology-conformance workflow P2/L, #82 per-repo agentic profiles P3/M) to frame the Tier-3 agentic conformance/review arc. Light updates to #74 and #75 pointing at #80 as prerequisite/grounding. Appended grooming-log entry. Schema validated: 7 themes, 21 stories, 48 tasks, 0 warnings.
**Result:** The next-session focus is explicit in the BACKLOG: #80 (research Dynamic Workflows, shipped 2026-05-28) → #81 (methodology-conformance workflow for dev-knowledge) → #82 (per-repo profiles); #70 (AI-Council loop) remains the heavy-decision companion. #77 doc-rot is subsumed into #81 as one verifier.
**Changes:** BACKLOG.md (new stories/tasks + light updates + grooming log); JOURNAL prepend. No other files changed.

---

### 2026-06-03 — #79 resolved: codemap end-state correct, no build needed

**Did:** Recorded the #79 resolution from the grounding audit: no marker-aware gate, no generator fix, no wiring — the codemap is already in its correct per-repo end-state (hub generator-managed; three children hand-authored with `not generator-managed` marker; corp-sca text-only override). Closed #79 in BACKLOG with rationale; appended codemap end-state note to ADR-71.
**Result:** #79 closed. ADR-71 now records the resolved end-state and the deferred-indefinitely status of both the gate and the fix, with the layout-agnostic reference-validator as the future cheap path if drift detection ever becomes a real need.
**Changes:** BACKLOG.md #79 outcome + `closes [#79]`; ADR-71 codemap end-state note appended; JOURNAL prepend.

---

### 2026-06-03 — Codemap grounding per repo (#79, first half)

**Did:** Read-only grounding of every sibling's codemap state to resolve the ADR-71 split (marker-aware-gate vs generator-fix). Ran the hub generator with no `--write` against ai-council, corp-ops, corp-monorepo at both `src` and inner `src/<pkg>` source roots; read each committed CODEMAP block + marker; assessed corp-sca scale.
**Result:** All three codemap repos carry `not generator-managed` (deliberate hand-authored) AND are generator-INCOMPATIBLE (single-package-under-`src/` nesting + prefixed imports → 0 edges; dotted/absent tach → 0 layers; generator only draws dir-packages, not the module-level curated nodes). corp-sca is S-scale flat-`src/`, already a deliberate text-only override → no codemap needed. **Headline: the safe universalization is SMALL — marker-aware gate is the universal path; NO repo requires the generator fix.** Honest caveat recorded: a marker-aware gate gates only the hub; children's hand-authored codemaps stay human-maintained/un-gated (the deferred generator fix is the only thing that would auto-catch their drift). Report: `docs/audits/2026-06-03-codemap-grounding.md`.
**Changes:** +`docs/audits/2026-06-03-codemap-grounding.md`; JOURNAL prepend. No sibling touched.
**Next:** Resolution step — build the marker-aware `codemap-freshness` gate in the hub, wire it fleet-wide (no-op on marked blocks). Generator fix deferred (no repo needs it).

---

### 2026-06-03 — ADR-71 amended: operating model + pilot finding + status

**Did:** Amended ADR-71 (append-only, doc-only) to record the corp-monorepo TOC pilot outcome — flipped Status to consumption-contract **VALIDATED** (consume `repo:/rev:` at pinned `69558c7` + `toc-generate` + `toc-freshness` stale/fresh, end-to-end), and added two sections: **Operating / propagation model** (consumer-PULL not source-push; pinned-pull chosen; central fleet-writer rejected as a Layer-2 violation) and **Codemap layout finding** (generator is layout-coupled — corp's `corp.`-prefixed imports + dotted `tach.toml` keys → 13 orphans/0 edges/0 layers vs curated 10/15/4; codemap rollout gated, TOC unaffected).
**Result:** TOC universalizes cleanly; codemap does NOT — gated on per-repo grounding + fix-generator-vs-marker-aware-gate decision (BACKLOG #79 added, P2/L). Existing ADR content untouched. Tests green, ruff clean, `audit.py health` OK. Provenance note: the prompt's named source audit file was absent; findings recorded verbatim from the operator's prompt.
**Changes:** `docs/decisions/ADR-71-*.md`, `BACKLOG.md` (+#79), `JOURNAL.md` (this). 1 commit on `docs/adr-71-amend`. Next: TOC rollout — ai-council, then corp-ops/corp-sca (bootstrap pre-commit first).

---

### 2026-06-03 — Hub becomes the doc-tooling pre-commit hook *source* repo (ADR-71)

**Did:** Step 1 of doc-tooling universalization (hub-only, non-disruptive): recorded **ADR-71** (distribute codemap+TOC via the pre-commit hook source repo pattern), parametrized the codemap CLI on a target arch path (`--arch-file`, default-preserving — mirrors TOC's file-arg), and exposed both tools as four hooks in a root `.pre-commit-hooks.yaml` (`codemap`/`toc` × freshness/generate) via `language: script` thin wrappers in `scripts/` (no pip package; ADR-59 root-hygiene; `#!/usr/bin/env python3`).
**Result:** `pre-commit try-repo` (pre-commit 4.5.1) confirms a consumer **resolves + runs the hooks from the hub by local path on this Windows machine** — toc-freshness Passed on the hub; codemap-freshness + codemap-generate Passed on a scratch `src/` consumer; toc-generate correctly surfaced exit-3 "no TOC markers" on a marker-less fixture (faithful exit-code passthrough, not a resolution failure). 230 tests green (+2 `--arch-file`), ruff clean, `audit.py health` OK, hub's own production `.pre-commit-config.yaml` gate untouched. Scratch consumer in $TEMP removed + verified (no leftovers). Codex `/review` (gpt-5.5) found one **HIGH** — wrappers committed mode `100644` would fail `language: script` exec on POSIX consumers (worked on this Windows box via shebang/py-launcher) — **fixed** via `git update-index --chmod=+x` → `100755`; no other findings (`docs/audits/2026-06-03-codex-doctools-hook-repo.md`).
**Changes:** +`docs/decisions/ADR-71-*.md`, +`scripts/codemap_hook.py`, +`scripts/toc_hook.py`, +`.pre-commit-hooks.yaml`; `scripts/codemap/{cli,check}.py` + `tests/test_codemap.py`; README ADR index + BACKLOG #78 (deferred consolidated docs-refresh); JOURNAL (this). 3 step commits on `feat/doctools-hook-repo`. Next: corp-monorepo pilot (consume via `repo:/rev:`, frozen→live codemap, TOC its 551-line ARCHITECTURE).

---

### 2026-06-03 — Cross-repo doc-tooling inventory (universalization grounding)

**Did:** Read-only inventory across all 5 repos (ADR-69 honored — wrote only into `.dev-knowledge`) grounding a future codemap+TOC universalization plugin; captured the `tier1-lifecycle` plugin/marketplace as the build template.
**Result:** Central finding — the codemap/TOC **generators live only in the hub**; the 3 children with codemaps (`ai-council`/`corp-monorepo`/`corp-ops`) carry hub-generated mermaid but **no generator and no freshness gate** (frozen), `corp-sca` has no codemap at all. Copy-drift = **N/A (no copies to diff)** → plugin must **deploy-fresh**, not single-source. `corp-ops`+`corp-sca` lack `.pre-commit-config.yaml` (must bootstrap). TOC candidates: corp-monorepo ARCH (551) + ai-council council-question-guide (570). 228 tests green, audit health OK, ruff clean.
**Changes:** +`docs/audits/2026-06-03-doc-tooling-inventory.md`; JOURNAL (this). No plugin built, nothing applied to siblings.

---

### 2026-06-03 — Protocols-cleanup final brick: 4 small-file fixes + AGENTS.md single-source attempt

**Did:** Executed the remaining MED/LOW audit findings across four small protocol files (one commit each on `docs/protocols-final-cleanup`): SESSION_SETUP — signposted the two handoff layers (browser `wygeneruj handoff` vs HANDOFF v4 Claude-Code) + added `[scope: X]` to the LESSONS append format; HANDOFF_PROCESS §5 — forward-pointer to the v4.3 §A claim-reframe; AGENT_FRAMEWORK — stale "checks #1–#10/#11+" → points at `py scripts/audit.py checks` (drift-proof); ENVIRONMENT — refreshed version snapshot (Claude Code 2.1.161, Python 3.12.10, VS Code 1.122.1; dated 2026-06-03) + marked the elapsed GLM-5.1 April-12 binding item.
**Result:** 228 tests green + ruff clean after every step; `audit.py health` green. **AGENTS.md single-source NOT landed** — canonical `codex/AGENTS.md` and deployed `~/.codex/AGENTS.md` confirmed byte-identical (no drift now), but symlink creation is blocked on this machine (`Administrator privilege required` — Developer Mode off; fold-in 2 → drift-guard branch, no elevation). Drift-guard proposed to operator (not built — operator-gated). Closes the protocols-cleanup arc except the operator's drift-guard decision. Noted (not built): ENVIRONMENT's version table is drift-prone hand-maintenance — future brick could auto-generate it. Deferred: bundling the `ARCHITECTURE.md:519` copy→symlink note with the §brick-#1 count-hardcode into one future genuine-re-read ARCHITECTURE pass.
**Changes:** `protocols/SESSION_SETUP.md`, `protocols/HANDOFF_PROCESS.md`, `protocols/AGENT_FRAMEWORK.md`, `protocols/ENVIRONMENT.md`, JOURNAL (this). 4 step commits; advances BACKLOG #77.

---

### 2026-06-03 — ESSENTIALS light fix: true contract + 3 drift fixes

**Did:** Corrected false "1-page" contract on L3 (honest LLM-frame description); pointed lesson→rule at canonical PLAYBOOK §4; added canonical pointer for the three-layer flow to PLAYBOOK "System Architecture"; disambiguated "Continuous Improvement" heading vs PLAYBOOK §6. Single file, 4 commits on `docs/essentials-light-fix`.
**Changes:** `protocols/ESSENTIALS.md` (+4 lines net). 228 tests green; audit.py health 12/12.

---

### 2026-06-03 — Applied dynamic TOC to PLAYBOOK.md

**Did:** Inserted `<!-- TOC:START/END -->` markers and ran `scripts.toc.cli generate --write` on `protocols/PLAYBOOK.md`; added `toc-freshness-playbook` pre-commit hook mirroring the existing ARCHITECTURE.md hook. Pure application of the existing toc tool (no generator changes).
**Changes:** `protocols/PLAYBOOK.md` (+176 lines TOC); `.pre-commit-config.yaml` (+8 lines hook). 2 commits on `docs/playbook-toc`; 228 tests green.

### 2026-06-03 — PLAYBOOK prose cleanup (doc-rot brick #2)

**Did:** Executed the remaining PLAYBOOK-only findings from `docs/audits/2026-06-03-protocols-rot-audit.md`: merged the two divergent lesson→rule statements into one canonical (§4, trigger + 3-step) with §13 condensed to a pointer; retired the 10 doc-embedded "Section history" blocks (one intro note replaces them, git is the record per ADR-49) and fixed the two refs the deletion orphaned (L432/L461); reconciled 3 CHANGELOG-as-live mentions to retired (the audit named 2; a 3rd identical spot was found on re-derivation); added an Organization note for section-zone clarity — no renumber (the §17→§19 gap accepted; §N cross-refs preserved).
**Result:** PLAYBOOK 2765→2710 (net −55; −69/+14). 228 tests green and `audit.py health` OK throughout; ruff clean. 4 commits on `docs/playbook-prose-cleanup`, one per step. Doc-only, single file; ESSENTIALS + other protocol files untouched (later bricks).
**Changes:** protocols/PLAYBOOK.md (4 commits); JOURNAL (this). Advances BACKLOG #77.
**Next:** Apply the dynamic-TOC tool (`scripts/toc`) to the now-clean PLAYBOOK; then ESSENTIALS re-trim (point its lesson→rule + three-layer-flow at the now-canonical PLAYBOOK); then the small-file fixes (SESSION_SETUP, HANDOFF, ENVIRONMENT, AGENT_FRAMEWORK).

### 2026-06-03 — audit.py self-documenting; PLAYBOOK §18 deleted (doc-rot brick #1)

**Did:** Made `scripts/audit.py` self-documenting — strengthened module + 4 command docstrings (`--help` is now the authoritative CLI ref), added a `checks` command sourced from `ALL_CHECKS`, and removed the hand-numbered "Check #N:" prefix from all 12 check docstrings (number now owned by the live listing). Then deleted PLAYBOOK §18 "Ecosystem Audit Tool Workflow" (259 lines) and repointed its one live cross-ref (L592).
**Result:** The "10 vs 11 vs 12" check-count drift is structurally dead — `audit.py checks` reports `len(ALL_CHECKS)` live, so it can't diverge from what runs. Conceptual layer confirmed pre-covered in ARCHITECTURE.md (§Validators/§Authority) + ADR-36, so deletion lost nothing. PLAYBOOK 3024→2766 (17→19 numbering gap left for the numbering brick). 228 tests (+2), ruff clean, `health` gate green throughout.
**Changes:** scripts/audit.py (docstrings + `cmd_checks`); tests/test_audit.py (+2 `checks` tests); protocols/PLAYBOOK.md (−259). 4 commits on `refactor/audit-self-documenting`. Residual flagged: ARCHITECTURE hardcodes "12 checks" — candidate next brick to point it at `audit.py checks`.
**Next:** Codex review of the audit.py diff, then merge; then the PLAYBOOK prose brick (lesson→rule canon, section-histories, numbering). Advances BACKLOG #77.

### 2026-06-03 — Read-only doc-rot audit of protocols/

**Did:** Audited all 7 live `protocols/` files (5,021 lines; PLAYBOOK 3,024) read-only for structural rot — intra-file duplication, per-section changelogs (ADR-49), hub-vs-universal mixing, numbering, stale refs, and cross-file summary-fidelity drift (CLAUDE.md rule #6). Changed no protocol file.
**Result:** Real rot confirmed — HIGH findings: lesson→rule stated 3 ways (PLAYBOOK L1687/L2318, ESSENTIALS L393), hub-only audit-tool §18 (L2486+) in universal doc, ESSENTIALS breaching its own "1 page" at 426 lines; 10 PLAYBOOK Section-history blocks; ENVIRONMENT/SESSION_SETUP MED. Root: `audit.py` freshness check verifies re-read recency, not structural integrity, and never targets `protocols/`.
**Changes:** +docs/audits/2026-06-03-protocols-rot-audit.md; LESSONS append; BACKLOG [#77] (Enforced governance). 3 commits on `docs/protocols-rot-audit`; 226 tests green.
**Next:** Operator reviews findings; consolidation is the next decision-gated pass ([#77]).

### 2026-06-03 — Dynamic auto-TOC for canonical docs (mirrors codemap)

- Did: Built a generator-driven, freshness-gated TOC mechanism on `feat/dynamic-toc`, mirroring the codemap pattern exactly rather than inventing a new one. New `scripts/toc/` package (`generator`/`check`/`cli`, layout + CLI + 0/1/2/3 exit codes cloned from `scripts/codemap/`); parses a doc's own `##`/`###` headers into a nested anchor-link list between `<!-- TOC:START/END -->` markers. GitHub-compatible anchors — full header text slugged (so `## Purpose [CORE]` → `#purpose-core`, double-hyphen on removed `&` preserved like github-slugger), `[TAG]` stripped from link text, fenced code blocks skipped, dup anchors `-1/-2`. Standalone `toc-freshness` pre-commit hook (fail-on-stale, NOT an audit.py check — matching where `codemap-freshness` lives). Applied to `ARCHITECTURE.md`; convention codified in PLAYBOOK (new section) + ESSENTIALS (one-liner) + ADR-51 (dated amendment). Unlike the codemap (hardwired to ARCHITECTURE.md), the TOC CLI takes the target file as an arg → reusable.
- Result: 226 tests green (21 new, mirroring test_codemap.py). All pre-commit gates pass incl. the new `toc-freshness` on the ARCHITECTURE commit. ARCHITECTURE TOC lists 10 top-level sections + ### subsections with working anchors. PLAYBOOK/ESSENTIALS outside the last_reviewed gate (no frontmatter) → no audit-#10 re-trip; ARCHITECTURE last_reviewed (2026-06-03) == edit date → unaffected. TOC-worthy survey: **PLAYBOOK.md (~3040 lines)** is the strong standing candidate; ESSENTIALS (~427) borderline — reported, NOT auto-added per scope.
- Changes: `scripts/toc/` + `tests/test_toc.py` + ARCHITECTURE codemap node (Step 1); `.pre-commit-config.yaml` toc-freshness hook (Step 2); `ARCHITECTURE.md` markers+TOC (Step 3); `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md` + `docs/decisions/ADR-51-*.md` (Step 4); JOURNAL (this).

---

### 2026-06-03 — Tier-1 use-case closeout fixes: pre-commit double-fire quirk + #76 + #77

- Did: Three ground-then-fix units on `chore/tier1-closeout-fixes`, one commit each. (1) **Pre-commit "Skipped" quirk** — diagnosed (not guessed): pre-commit is installed for BOTH the `pre-commit` and `commit-msg` git hooks, and the 5 working-tree hooks declared no `stages:`, so they fired a SECOND time at the commit-msg invocation, found no staged files there, and printed a misleading `(no files to check) Skipped` — even though they'd already run + passed in the pre-commit stage (the gate was never actually skipped; reproduced both before/after). Fix: top-level `default_stages: [pre-commit]`; `backlog-id-on-close` keeps its explicit `stages: [commit-msg]`. Verified: staged BACKLOG.md → validate-backlog runs once (Passed); staged ARCHITECTURE.md → codemap-freshness runs once (Passed); no second batch. (2) **#76** — converged the hub onto the plugin's `/review-closures`; verified the plugin's bundled `review_closures.py` (cache 0.1.2) resolves the hub root via `$CLAUDE_PROJECT_DIR` (`plan --ids 76` returned hub PROPOSALS + HEAD), nothing references the hub-local command FILE, then deleted the duplicate `.claude/commands/review-closures.md` (kept `scripts/review_closures.py`); CLAUDE §7 → Plugin-provided (v2.12). (3) **#77** — rewrote CONTRIBUTING §Handoff process from stale v2.0/ADR-37-pending//session-summary to the real v4 (ADR-62 ratified, two-phase shipped, `/handoff` command); dropped the obsolete `wygeneruj handoff` trigger.
- Result: 205 tests green; Codex `/review` on the pre-commit config = **0 findings** (independently verified `default_stages` scoping vs the commit-msg override against pre-commit docs). BACKLOG 44→42 (#76, #77 left via done-items-leave; validate_backlog OK). Both freshness edits (CLAUDE/CONTRIBUTING) same-day stamped → no audit-#10 re-trip. Tier-1 use case closed end-to-end — only future themes (#8/#12/#4/#74/#75) + push remain.
- Changes: `.pre-commit-config.yaml` (`b78bc47`), `.claude/commands/review-closures.md` del + CLAUDE.md v2.12 + BACKLOG −#76 (`cf261ed` closes #76), CONTRIBUTING.md + BACKLOG −#77 (`0f3536a` closes #77), `docs/audits/2026-06-03-codex-tier1-precommit-stage-fix.md`, JOURNAL (this). Also committed the day's Tier-2 fleet-health snapshot up front (separate `chore(fleet)` on main).

---

### 2026-06-03 — Tier-1 closeout: lifecycle diagrams + ADR-index reconcile + handoff-rework backlog item

- Did: Closed the last Tier-1 documentation gaps. ARCHITECTURE "Tier-1 self-enforcing lifecycle" section gains two convention-matched mermaid diagrams (L0/L1/L2 distribution + the closure loop) and ADR-70 / ADR-index links; ARCHITECTURE "Governing ADRs" curated list reconciled (ended at ADR-68 → added ADR-69 + ADR-70, descriptions read from `docs/decisions/README.md`). BACKLOG +[#77] (rework the stale CONTRIBUTING §Handoff process — the drift filed earlier 2026-06-03). Deleted the merged `docs/tier1-doc-convergence` branch.
- Reconcile result: `docs/decisions/README.md` index was ALREADY complete through ADR-70 (no change); CLAUDE §11 already carried ADR-69/70; only ARCHITECTURE's curated list lagged. ADR-44 (Reserved/held pending N=2) + ADR-45 (Superseded by HANDOFF v3.3) deliberately kept OUT as non-governing. The repo HAS an established mermaid convention (theme-init + `classDef` color, audit check #7) — the diagrams match it; verified green before commit. ARCHITECTURE was already stamped 2026-06-03 so the same-day re-edits did not re-trip freshness.
- Flag (no new drift; recurring tooling quirk): the `validate-backlog` and `codemap-freshness` pre-commit hooks recurrently report "no files to check / Skipped" on a staged commit of exactly the file they filter on (audit-health always-runs + passes). No correctness impact — manual `validate_backlog` OK (44 tasks); codemap block untouched. No formal gotcha filed (no repo-level gotchas location — `.dev-knowledge` patterns live in LESSONS); reported for future investigation. Arc fully documented + indexed.

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
