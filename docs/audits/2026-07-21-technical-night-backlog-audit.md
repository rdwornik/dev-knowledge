# Night audit — backlog trust (Lane 3 of 3)

**Date:** 2026-07-21 · **HEAD:** `e3e79ada` · **Branch:** `worktree-night-backlog-audit`
**Scope:** all 133 open tasks in `BACKLOG.md` · **Posture:** DETECT-AND-PROPOSE, read-only.

> **This report edits nothing.** No BACKLOG line was struck, no ticket closed, no id filed.
> The operator runs `/review-closures` — the only path that edits the backlog — and approves
> strikes in bulk on one GO.

## Triage criteria (binding on this report)

A **kill-candidate is actionable ONLY if it names hard closing evidence** — a merge sha, a
file/function that implements every Done-when clause, or a superseding id. Anything without
that goes to **CHECK MANUALLY**, never to the auto-approvable kill list. Multi-clause
Done-whens ("X AND Y") require **every** clause satisfied. A ticket is "done" only if the
evidence is in the record, not inferred.

## Method

Seven parallel verifiers, one per epic-group, each cross-checking its batch against git
first-parent history, `git log --all`, `JOURNAL.md`, `logs/`, the live code/config, and — for
consumer-side clauses — the actual consumer repos (`ai-council`, `corp-monorepo`, `corp-ops`,
`corp-sca-time-automation`, `demo-prep`). Every returned kill-candidate was then
**independently re-verified** by the orchestrator before reaching the list below. That second
pass changed two verdicts (`#339`, `#327` — both demoted) and refuted one orchestrator
hypothesis (`#343` — the fleet_parity skip was never wired).

## Headline

**The backlog is trustworthy.** Three independent integrity checks came back clean:

- **Zero open tickets carry a genuine `closes [#id]` tag.** A full `git log --all` scan found
  exactly one apparent hit (`#370` at `12e6b45b`) and it is a **false positive** — the commit
  body quotes the string `closes [#370]` as prose while *asserting no such tag exists*.
  Closure hygiene (`backlog-id-on-close` + ADR-65 done-items-leave) is working.
- **Zero orphan ids.** Every one of the 221 ids referenced anywhere in `BACKLOG.md` resolves
  to either a live ticket or real commit history. No id is unaccounted for.
- **Zero silently-deleted tickets.** The 19 gaps in the id sequence
  (`#49-52, 54, 56, 58-64, 173-178`) were **never allocated** — confirmed by
  `git log -S"[#id]" -- BACKLOG.md` returning nothing for each. They are numbering gaps
  (the same reserved-but-unconsumed pattern as today's `#373`-`#380`), not lost work.
- `validate_backlog`: **OK — 8 themes, 22 stories, 133 tasks, 0 warnings.**

The real finding is not rot but **staleness of in-ticket status prose**: six tickets describe
themselves as pending work that has since shipped. Every one of them says so in its own text
("per-consumer rollout pending", "BUILD PARTIAL"), written hours-to-days before the work
landed. That is the failure mode this audit exists to catch.

**Counts:** 116 LIVE · 9 MERGED-NOT-CLOSED · 6 kill-candidates · 2 demoted to check-manually.

---

## KILL CANDIDATES (6) — done-but-listed, evidence-backed

Formatted for one `/review-closures` pass. Each carries its closing evidence and a
`kill-candidates:` line. **No ticket ids are filed by this report.**

### `#302` — Branch-protection parity (block-ff-push to consumers)
**Classification:** DONE-BUT-LISTED · **Confidence: HIGH**
**Evidence:** Both consumers carry the guard at hub rev `v1.3.1` —
`ai-council/.pre-commit-config.yaml:68,79` and `corp-monorepo/.pre-commit-config.yaml:91,94`
(verified on disk). Rollout merges `111c999` (ai-council) / `f6f5b21` (corp), both 2026-07-11.
**Firing witnessed, not merely installed:** ai-council JOURNAL:1545 — *"direct-to-main push →
`block-ff-push` REFUSED (exit 1, 'REFUSED — 1 non-merge commit(s)…'); a `--no-ff` merge push
PASSED"*; corp JOURNAL:338 — *"a synthetic `main`-bound range of 9 real non-merge commits
REFUSED (exit 1)"*. Manifest rows `deploy/manifest-v1.3.0.yaml:495,508`, carried into v1.4.0.
**Why still open:** the ticket's "(b) per-consumer rollout pending" note was written hours
before the rollout completed the same day.
`kill-candidates: none — the ticket's own rollout-pending note is stale; both Done-when clauses (consumer gains guard; verified FIRING) are satisfied at n=2 with witnessed refusals`

### `#309` — Commit-msg-gate parity for consumers
**Classification:** DONE-BUT-LISTED · **Confidence: HIGH**
**Evidence:** `backlog-id-on-close` carried to both consumers at `v1.3.1`
(`ai-council/.pre-commit-config.yaml:74`, `corp-monorepo/.pre-commit-config.yaml:93`) via
`deploy/manifest-v1.3.0.yaml:519,526`. **Firing witnessed:** ai-council JOURNAL:1545 —
*"removing a `- [#id]` BACKLOG line uncited → `backlog-id-on-close` BLOCKED"*; corp
JOURNAL:338 — *"block on removed `[#777]` unreferenced (exit 1), pass when cited (exit 0)"*.
The OR-branch is also discharged: `backlog-filing-backpressure` is recorded
hub-only-by-construction with a reason at `deploy/manifest-v1.4.0.yaml:42-43`.
`kill-candidates: none — both branches of the Done-when (portable gate shipped + firing, non-portable gate recorded hub-only-with-reason) are satisfied; the rollout-pending note is stale`

### `#131` — Repo-onboarding runbook (6-layer install sequence)
**Classification:** DONE-BUT-LISTED · **Confidence: HIGH**
**Evidence:** `docs/runbooks/repo-onboarding.md` exists (merge `32db7eb7`, 2026-07-07).
`## Install sequence (#131)` at `:30` lists all six layers in order — Floor `:46` · Carriers
`:57` · Lifecycle command `:68` · Review profile `:84` · Ecosystem registration `:95` ·
Re-anchor mechanic `:107` — matching the ticket's stated sequence exactly. Pilot clause met
at `:155-157`: *"ai-council = n=1, corp-monorepo = n=2, both deployed v1.2.0"*. The three
must-appear live steps (`pre-commit install`, floor `.gitignore` negations, orphaned-root-floor
deletion) are present at `:164+`.
`kill-candidates: none — runbook exists, all 6 layers in order, piloted n=1 with the n=2 gate recorded; every Done-when clause has a named line`

### `#215` — Onboard + verify methodology (conformance-verify half)
**Classification:** DONE-BUT-LISTED · **Confidence: MEDIUM-HIGH**
**Evidence:** Same runbook carries a **distinct** `## Conformance verify (#215)` section at
`:130-137` — run-X-expect-Y rows naming commands, with the last three exercising organs
actually firing (*"Configured ≠ armed ≠ proven"*). The runbook header `:13-14` states this
ticket's Done-when verbatim and asserts the split from `#131` (*"do not merge the ids"*).
**Caveat:** the ticket's body ties the verify half to `#171` (`ecosystem/conformance.md`),
which is **unbuilt and separately open**. That tie is a scoping note, not a Done-when clause —
the Done-when reads *"one onboard runbook + a conformance verification exist"*, and both do.
`kill-candidates: none — the conformance-verify section exists as a distinct deliverable; the #171 dashboard tie is a scoping note, not a Done-when clause, and #171 stays open on its own`

### `#314` — `protocols/` as a fleet-mandated genre
**Classification:** DONE-BUT-LISTED · **Confidence: MEDIUM**
**Evidence:** Clause 1 — hub `protocols/README.md:5-27` documents the mandated genre and the
hub-pointer-vs-local-marked split, citing `#314 / #327`. Clause 2 (n≥1) — **exceeded at n=2**,
verified on disk and git-tracked: `corp-monorepo/protocols/{README.md,CORP_INTERFACE.md}` and
`ai-council/protocols/{README.md + 3 interface docs}`. Merges `2cae1fa4`, `2b21cb26`
(2026-07-12). The ticket's own `BUILD PARTIAL` note scopes "full genre wording" **out** to
`#327`, so that residue is not this ticket's clause.
**Caveat (must ride with the close):** consumer files still carry stale forward-markers —
`corp-monorepo/protocols/README.md:20` and `CORP_INTERFACE.md:8` both read *"Full genre wording
deferred to #327"*. Sweep them when `#327` resolves.
`kill-candidates: none — both clauses met at n=2 with the full-genre-wording residue explicitly scoped to #327 by this ticket's own BUILD PARTIAL note`

### `#292` — Handoff-completeness (`(fill:`) gate
**Classification:** DONE-BUT-LISTED · **Confidence: MEDIUM** — read the caveat before approving.
**Evidence:** `scripts/validate_residual_completeness.py` (shipped `622baedb`, hardened
`e2c2d9f7`) + `check_residual_completeness` registered in `ALL_CHECKS`
(`scripts/audit.py:1973` def, `:2419` registration) + `tests/test_residual_completeness.py`.
FAIL-class, so it refuses at ship-gate. Satisfies the literal Done-when: *"a
ship-time/assemble-time check refuses a bundle carrying an unfilled `(fill:` marker, with a
test"*.
**Caveat — satisfied-by-elimination, and narrower than the ticket asked:** no commit cites
`#292`; it was discharged by an unrelated ARC-5 arc. The shipped gate is narrower in three
ways: it matches only markers constituting a FILL-IN region's **entire body** (a stray `(fill:`
in prose escapes the ticket's "grep-the-bundle" shape); it is **diff-triggered /
prospective-only**, so already-committed bundles are grandfathered; and `PROBES.md` is
deliberately never inspected. Two open tickets record defects in this very gate — `#366`
(scans working tree, not the staged blob) and `#365` (doc↔code edge still `exempt:`).
**Adjudicate together with `#310`**, whose kill-candidates line points here.
`kill-candidates: #310 — the cold-bundle annotation surface; #310's own kill line defers to this ticket's evidence text, so the pair must be ruled together, not independently`

---

## CHECK MANUALLY (2) — proposed as done, demoted on re-verification

These came back DONE-BUT-LISTED from a verifier and **failed the orchestrator's independent
re-check**. They are *not* auto-approvable. Both are close calls the operator should rule.

### `#339` — LESSONS legacy-split build
**Demoted from:** DONE-BUT-LISTED · **Reason: the ticket text and the ADR disagree.**
By the **ticket's** Done-when, it reads satisfied: the threshold + mechanism are defined
(`ADR-29:87` — trip at >300 entries, drain to ~180), ADR-29 was ratified by append
(`ADR-29:126`, *"Ratified 2026-07-17"*, merged `e0cbffdb`), the ADR-39 six-element registry
entry landed (`ADR-39:403-407`), and the OR-branch "recorded not-yet-needed with the threshold"
holds — `LESSONS.md` is **241 entries < 300** (verified `grep -c '^### '`).
**But ADR-29 defines this ticket's build leg as three parts, and one is unbuilt.** `ADR-29:124`
— *"[#339]'s build leg (execute-once or record not-yet-needed, **+ the A2 helper**, + the ADR-39
six-element registry entry)"* — and `:126` — *"blocked until the ADR-39 registry entry **and the
A2 byte-identity helper** exist"*. The registry entry exists; **the A2 byte-identity helper does
not** (`ls scripts/ | grep -iE 'lesson|legacy|byte'` → empty), and **no successor ticket owns
it** (`BACKLOG` grep for "byte-identity"/"LESSONS-legacy" returns only `#339` itself).
**Operator call:** close only alongside filing the helper, or re-scope `#339` to the unbuilt
helper. Closing as-is drops the A2 helper on the floor with no owner.

### `#327` — Protocols-as-interface genre ruling
**Demoted from:** DONE-BUT-LISTED · **Reason: the consumers contradict the claim.**
Both clauses appear met — hub `protocols/README.md:6-8` defines the interface genre verbatim
(*"what other repos/agents must know to interact with THIS repo"*), and corp (README +
`CORP_INTERFACE.md`) and ai-council (README + 3 interface docs) both carry the shape, corp
included as the Done-when requires.
**Contradicting evidence in the record:** `corp-monorepo/protocols/CORP_INTERFACE.md:8` reads
*"Full genre wording deferred to #327"* and `corp-monorepo/protocols/README.md:20` repeats it.
The deliverable this ticket owns is declared **still outstanding by the very files that would
be its proof**. Either the wording is complete and those markers are stale (sweep them in the
closing arc), or it is genuinely incomplete and `#327` is LIVE. The record does not settle it.

---

## MERGED-NOT-CLOSED (9) — merged ≠ done; the open clause is named

| id | What merged | **Open clause (verbatim-ish)** |
|---|---|---|
| `#244` | Essence-spec epic P1–P4 all shipped (P2 `2c869518`; P3 `gen_methodology_roster.py:101`; P4 `25b104ed` + `fleet_health.py:323`) | **P5 (hub self-prune) + P6 (fleet).** `deploy/manifest-v1.4.0.yaml:465`: *"P6 fleet rollout MUST re-evaluate before propagating this removal"*. P5 has no build commit. *Note: the 3 literal Done-when clauses arguably all have evidence — if the Done-when text governs rather than the phase list, this is closable. Operator call.* |
| `#352` | `.vscode` region decoration merged `21ec4653`/`3fc9458d`; hub config versioned, 2 marker-keyed regexes, 15/15 hub regions match, zero hand-maintained state | **Clause (f) render witness.** `docs/audits/2026-07-20-…-render-diagnostic.md:9`: *"Clause (f) — **OPEN**, not closed by this document"*; render status *"PREDICTED / PENDING-ADOPTION — NOT WITNESSED"*. Witnessable only in a consumer; blocked on `#371` (both consumers carry a 72B/77B `settings.json` with zero highlight keys). |
| `#153` | `no_ff_merges` WARN + `block_ff_push.py` prevent organ both shipped and in `ALL_CHECKS` | **Three clauses open:** core-invariant #5's `--no-ff` **scope boundary** undefined (hub vs `~/.claude` vs children); the `~/.claude`-reach question undecided (`#189` still points here for it); minimal-diffs / append-only / no-CHANGELOG neither mechanized nor recorded-as-accepted. |
| `#162` | Boot-ack narrow slice landed (`HANDOFF_BOOT.md:24`) | **"An ADR or operator ruling lands the disambiguation across all enumerated surfaces."** Both senses still live: `HANDOFF_BOOT.md:16` *"You are the critical architect"* (actor) vs `HANDOFF_PROCESS.md:272` *"Modes — architect \| execution"* (mode). No ADR disambiguates. |
| `#324` | Leg (c) audit-corpus verb-list merged `65c9827e` | **Legs (a)+(b).** `docs/audits/2026-07-16-…-fleet-structure-census.md:138`: *"no `settings.json` SessionStart/Stop wiring and no nightly routine … unbuilt"*. Charter-only by design. |
| `#267` | Half-b shipped `ffe4d875`; `engages:` scope conditions at `manifest-v1.4.0.yaml:511,610` | **Half-a live re-measurement.** *"a consumer measurement shows both components FIRED under a scope-matching edit"* — never re-run. *Ad-hoc firing witnesses DO exist* (toc-freshness FAILed in ai-council, merge `71e1307`; floor-hash BLOCKED 2026-07-09). If the operator accepts lived-QA witnesses over a `lived_sandbox` run, the substance is met and only the instrument leg is missing. |
| `#123` | Clause 1 shipped — `Routine: <name>` trailer convention recorded (`PLAYBOOK:1694`, `ADR-80:36`) **and adopted** (live `chore(routine/…)` commits; `ADR-84:15`) | **"AND one morning-funnel value review records per-routine findings-acted-on vs noise."** Every hit is prospective ("when built"); no review recorded. |
| `#71` | `~/.claude` tree clause satisfied — `ENVIRONMENT.md:59` matches live `ls ~/.claude/{commands,skills}` exactly | **"The Codex/Rejected lines are reconciled to live state."** `ENVIRONMENT.md:250` *"No Codex CLI, no Gemini CLI"* and `:262` *"Codex CLI (no advantage over Haiku subagents)"* carry no reconciliation note, while the repo ships `/codex-review` + a `codex-review` skill. The pattern was applied to the analogous stale line at `:264` and not here. |
| `#300` | d.ii ruling landed — `ADR-101 §5 (L72-77)`: mode-boot bundles are EPHEMERAL, ratified 2026-07-11 | **"The committed functional bundle's fate is landed."** `docs/handoffs/2026-07-07-dev-knowledge-functional/` is still on disk; `ADR-101:8` *"removal … tracked under #300. This draft removes nothing."* Awaiting explicit operator deletion GO — no drive-by deletion. |

---

## ANOMALIES (flagged, not resolved)

**A1 — Hub registry contradicts consumer disk (untracked, unfiled).**
`ecosystem/deployed-versions.yaml` records `corp-monorepo: 1.2.0 / 2026-07-07 / v1.2.0`, but
corp's `.pre-commit-config.yaml:91` pins hub hooks at **`v1.3.1`** and its JOURNAL:933 records
the v1.3.1 rollout on 2026-07-11. Corp's own JOURNAL:937 names the owed fix — *"`deployed_methodology_version` bump for corp"* — never done. **The hub's registry of what it has
deployed is wrong about a consumer**, so any hub-side reasoning keyed on it is wrong. No ticket
owns this. Independently confirmed by the orchestrator.

**A2 — `#370` / `#372` id collision: resolved and documented; three stale citations accepted.**
Two parallel worktrees each allocated `[#370]`. Operator ruling 2026-07-20 (`12e6b45b`):
`[#370]` **stays** with the ownership-model ticket (already cited in merge `3fc9458d` and in an
**immutable** audit — citations that cannot be unwound); the bundle-selection ticket became
`[#372]`, since closed at `520bfd56` and correctly absent from `BACKLOG.md`. Renumbering
happened on-branch so main never saw a duplicate. Three commit messages (`40c7bce3`,
`b0443523`, `36ca03f0`) carry now-stale `[#370]` citations — **operator-ruled acceptable as
stale** rather than rewriting history, and independently confirmed **inert** (none carries a
`closes` tag, so none can trip `git_backlog_drift`). *Near-miss worth noting:* `12e6b45b`'s own
body records that the two additions sat at different line offsets, so git would have merged
**both** cleanly and the duplicate would have reached main before `validate_backlog` hard-failed.
**The repo has no id-uniqueness gate** — `check_backlog_filing.py` gates `kill-candidates`, never
the id; `validate_backlog` only detects a duplicate post-merge.

**A3 — `R9`/`R10`/`R11` do not exist.** The `[E8]` ruling set is R1–R8 (+R1b), nine picks. An
exhaustive search of the ARC-5 bundle, all fourteen `2026-07-19-*` night artifacts, and
`JOURNAL.md` found only those; the sole `R9`–`R11` strings belong to an unrelated R-namespace
in `docs/audits/2026-06-07-methodology-transfer-audit.md`. The filing correctly **declined to
invent rulings** and filed the census decision as `R12`. **Flagged, not resolved:** if the
operator holds R9–R11 off-repo they must be supplied.

**A4 — Two tickets rest on evidence that cannot persist.** `#277` cites
`logs/PROPOSALS-2026-07-07.md` for its 49:0 ratio and `#181` is data-gated on
`logs/coherence-nudge.log` — **both are gitignored by design** (`.gitignore:26,67`, ephemeral,
never committed). Neither claim is reproducible from the record. *Live measurements:* `#277`'s
ratio has **worsened to 91:0** (1 STRONG + 90 WEAK) against the 49:0 baseline its Done-when must
beat, and leg (b) is untouched (`_CHURN_FILES` still bare at `propose_closures.py:62`);
`#181`'s log is at 9 firings, up from 4.

**A5 — Broken and stale intra-ticket references.**
- `#344` cites `docs/intake/2026-07-17-hub-feedback-session-close-gate.md` — **absent in the
  hub**; it lives in `ai-council/docs/intake/`. A hub ticket carrying an unqualified
  consumer-relative path.
- `#244` cites *"P5 hub self-prune (**#130** sibling)"* — `#130` is *Memory-hygiene review*,
  unrelated. It also points at `#221` for P6, but **`#221` is closed** (`8aab4356`).
- `#349` cites bare `DEFINITION_OF_DONE.md`; the real path is `protocols/DEFINITION_OF_DONE.md`.
- `scripts/verify_handoff_probes.py:383` carries an unresolved `#NNN` placeholder where
  `#234`'s id belongs — a free hygiene fix.

**A6 — `#320`'s premise is factually obsolete.** The ticket says corp-ops has *"no git remote"*;
all three named repos now **have** `origin` remotes. The live gap is **unpushed commits** —
corp-ops 4, corp-sca-time-automation 4, demo-prep 53. Rewrite the body rather than working it
as stated; the data-safety concern is real, the stated cause is not.

**A7 — Line-number citation drift (verification hazard).** Several `[E8]` tickets cite lines
that have since shifted: `#358` cites `audit.py:1961` (now `:2425`), `#359` cites
`HANDOFF_PROCESS.md:502-503` (now `:517-518`), `#361` cites `block_immutable_edits.py:83` (now
`:81-84`). Every substantive claim still holds — but a reviewer re-verifying **by line number
alone** would get false "not found" results and might wrongly close a live ticket.

**A8 — `doc_rot` cap crowding (bears on `#364`).** `#353` measures **exactly 1189 / 1200 chars**
— 11 left, as filed. But seven more lines now sit within 60 chars of the cap (`#359` 1184,
`#371` 1184, `#369` 1179, `#357` 1179, `#370` 1167, `#365` 1144). `#364`'s "a gate degrading the
record it is meant to protect" concern is **broader than `#353` alone**.

**A9 — Not an anomaly, recorded for completeness.** The 19 never-allocated ids
(`#49-52, 54, 56, 58-64, 173-178`) are numbering gaps, **not deleted tickets** — each verified
absent from all of `BACKLOG.md` history. They match the reserved-but-unconsumed pattern of
today's `#373`-`#380` range (verified: no ticket filed into it; next-free is `[#381]`).

---

## Operator watch-outs before running `/review-closures`

1. **Dispositions orphan on close.** `ecosystem/disposition-register.yaml` references open
   tickets `#241` (×4 entries: backlog/vision/ai-council/essentials → handoff-process), `#210`
   (×2 no-ff journal-wrap), `#146`, `#277`, and `#335` (`auto_clearable_by`). Closing any of
   these without retiring its register entries makes ship-gate print
   `[stale] disposition … matched no live WARN`. Retire in the same arc.
2. **None of the 6 kill-candidates is in that set** — no disposition cleanup is required for
   this batch. `#314` is the only one needing a companion edit (the stale `#327`
   forward-markers in corp's two `protocols/` files).
3. **`#292` and `#310` must be ruled together** — `#310`'s kill line defers to `#292`'s evidence.
4. **`#339` and `#327` are demotions, not rejections.** Both are close; both need one operator
   sentence, not more evidence.
5. **Pairs worth merging rather than closing:** `#304`+`#305` (each names the other; one doc
   pass closes both; zero commits touch `repo-onboarding.md` since filing) and `#262`+`#295`
   (both consumers now carry hand-authored compact-text codemaps and explicitly declare
   themselves not-generator-managed — both tickets' own kill notes propose abandoning
   generator-management for flat/single-package layouts).
6. **Cheap closures blocked only on a recorded decision:** `#281` and `#331` are substantively
   done on consumer disk (both consumer BACKLOGs carry the epic schema; both run
   `validate-backlog`) but their Done-whens ask for a *recorded ruling* nobody wrote. The
   2026-07-19 night-s5 audit already flagged this at `:85`.
7. **`#270` is the load-bearing blocker of E7.** `#271` and `#348` both `depends-on: #270`, and
   the routines pilot design gates on it too. Nothing in the nightly cluster can close until the
   `[load]` section ships.

## Contract compliance

Read-only. This report is the only file written. `BACKLOG.md` untouched; no ticket id filed; no
merge; no push to main; committed to this worktree's own branch and STOP.
