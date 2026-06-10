# Consolidation audit — recent arc verified against the Definition of Shipped

<!-- scope: meta -->

**Date:** 2026-06-10
**Type:** consolidation / closure-gate audit (immutable record per CLAUDE.md §5)
**Trigger:** the 2026-06-10 "deployment is half the success" LESSON + the new PLAYBOOK
"Definition of shipped (closure gate)" — applied retroactively to the recent arc.
**Outcome:** all 5 in-scope executable organs PASS (E2E-witnessed live, teeth-confirmed);
JOURNAL↔BACKLOG reconciled (close #11/#111, keep #77 voided, #139→P2); 3 findings
(F1/F2/F3) dispositioned; shipped on `main` `e979730`.

> This record is the archival half the audit itself initially missed: Definition-of-Shipped
> point (5) names *archive*, and the ecosystem convention is audits → `docs/audits/`. The
> first close updated JOURNAL/BACKLOG/PLAYBOOK/gotchas but not this record, so (5) was only
> **partially** met and "all six met" over-claimed. This file completes (5). (Honest by design —
> the audit dogfooding its own doctrine, caught on operator review.)

---

## Scope window

- **Outer boundary:** `1b4bf26` (2026-06-04) → `fb1ecfe` (2026-06-10) — **135 first-parent merges**.
- **Confirmation method:** `git log --since="6 days ago" --first-parent main`; drift detection
  (`git_backlog_drift`) scans the WHOLE backlog vs WHOLE history, so the window only bounds which
  JOURNAL closure-claims were verified against git.

### In-scope set

- **Group A — executable organs (E2E targets):** #11 amendment-coherence gate, #89
  `validate_doc_claims` (folding #141), #90a `validate_git_backlog`, the child methodology floor
  lifecycle (#121/#137), `/ship`.
- **Group B — prose/methodology arcs (gate-validated in PHASE 1, not user-flow E2E):** #111,
  worktree-codification, #146, #147, #34/ADR-81, #135, #136, #115, #77, BACKLOG resync, #107
  (out-of-window feature; in-window work was codification — completion gap tracked as #143).

---

## PHASE 2 — E2E / user-flow witness table (observed behavior, not inferred)

| organ | tamper / exercise | observed behavior | verdict |
|---|---|---|---|
| **#11** amendment_coherence | `.claude/commands/handoff.md:2` `v4`→`v3` straggler | `health: DEGRADED`, `[!!] amendment_coherence: straggler '3' != anchor '4.4'`, **health exit 1 (BLOCKS)**; revert → PASS, exit 0 | PASS (teeth) |
| **#89** validate_doc_claims (+#141) | (a) clean run + `git status`; (b) `ARCHITECTURE.md` `17 registered checks`→`99` | (a) OK exit 0, tree clean after = read-only deriver (#141a); (b) printed `DRIFT mismatch audit_check_count doc=99 actual=17` (#141b teeth) — **but exit 0** (awareness-layer → F1); revert → OK | PASS (teeth) |
| **#90a** validate_git_backlog | remove `[#11]` from a temp BACKLOG copy, call `reconcile()` | baseline drift `{11,77,111}` → modified `{77,111}` — reads LIVE backlog, not hardcoded | PASS (non-vacuous) |
| **floor** lifecycle (#121/#137) | generate (sha256 `4d268f3…`, 887/1500 tok) → install (hook+config+stubs) → commit → arm → tamper floor body | **Guard 1** child pre-commit `Failed` exit 1 `floor hash drift 74a9b3… != 4d268f…`, `git commit` BLOCKED; **Guard 2** hub `floor_integrity` `severity=fail` hash drift; restore (`git checkout HEAD --`) → both green; teardown → child removed, no leftovers | PASS (both guards) |
| **/ship** | source-read ship.md; then live-witnessed at FINAL | auto-delete (step 10 `-d`, never `-D`), inline `-m` no-temp-file (step 7), 4 pre-flight refusals; live: merge `--no-ff` `e979730`, push `fb1ecfe..e979730`, branch auto-deleted | PASS |

All tamper cycles reverted via `git checkout HEAD -- <file>` (HEAD form, not the index form);
hub tree verified pristine after each. No E2E surfaced a real bug requiring a STOP.

---

## Findings + dispositions

| id | finding | disposition | refs |
|---|---|---|---|
| **F1** | `#89`/`#90a` are **awareness-layer**: the standalone verifiers `main()` return 0 even on drift (per their own docstrings — "never gates; CLI prints and exits 0"), and their audit adapters emit WARN-not-FAIL. So Definition-of-Shipped point (6) "organs run green" cannot be tested by exit code. | Sharpened **#147**'s note (gate must parse OUTPUT or add a `--gate` mode + **disposition WARNs** — block on new/undispositioned only) and **PLAYBOOK point (6)** to a class-specific rule (the absolute "no WARN" was un-satisfiable — `git_backlog_drift` WARNs on #77 permanently). | commit `83a41b4` |
| **F2** | `python scripts/audit.py checks` (the LISTING subcommand) crashed `UnicodeEncodeError` on the cp1252 Windows console — `check_git_backlog_drift`'s docstring-first-line (printed verbatim as its summary) carried a non-cp1252 bidirectional-arrow glyph. Non-gating (health/run unaffected; #89 derives `ALL_CHECKS` in-process). | ASCII-folded both console-reachable instances to `git<->backlog`; stdout NOT switched to utf-8 (preserves the ASCII-only console convention). `audit.py checks` now exit 0, full list. | commit `fe405b4` |
| **F3** | A defensive P0 path-safety check that embeds the literal exclusion-zone string inside a PowerShell/Bash command **self-trips** the `block-onedrive` PreToolUse guard (it scans command TEXT), blocking the whole command before any read/write. | Captured as a gotcha: verify via `.Contains('OneDrive')` or build temp paths under the structurally-safe `LOCALAPPDATA`/`TEMP` root (AppData\Local is never redirected). | `~/.claude` commit `2439268` |

---

## JOURNAL ↔ BACKLOG reconciliation

Seed = `git_backlog_drift` `{#11, #77, #111}` closed-but-present.

| id | class | git evidence | action | rationale |
|---|---|---|---|---|
| **#11** | (a) shipped-but-open | `closes [#11]` in `5193de5` | **CLOSED** (removed, ADR-65) | gate shipped + E2E-witnessed live this session; Done-when met; de-hardcode residual tracked as #146 |
| **#111** | (a) shipped-but-open | `closes [#111]` in `6c337ef` | **CLOSED** (removed, ADR-65) | (a)+(b)+readiness valve landed in PLAYBOOK; Done-when met |
| **#77** | (b) misattributed / `CLOSURE-VOIDED` | `closes [#77]` in `77e5d7d` ("Tier-1 use-case closeout") | **KEPT OPEN** (no action) | content-consolidation never shipped; the `closes` was a misattribution; #90a true-positive **by design** until #139 |
| (c) | obsolete / subsumed | — none found — | NONE | recent grooming (#134 n=1, 06-09 resync) already cleared obsolete items |

Also: **#139 bumped P3→P2** — this audit is its justification: `git_backlog_drift` direction-(a)
structurally cannot distinguish a *voided* closure (#77) from a *real* one (#11/#111); arc-content
inspection (#139/#90b) is required. Net: **67→65 tasks**; drift now `{#77}` only.

---

## Definition of Shipped — 6-point checklist for THIS audit

1. **Git clean + merged + pushed** — ✓ `e979730` on `main`, pushed `fb1ecfe..e979730`, branch auto-deleted, 0 commits ahead.
2. **Version surfaces coherent** — ✓ `amendment_coherence` OK.
3. **E2E / user-flow test passes** — ✓ 5 Group-A organs witnessed (table above), teeth-confirmed.
4. **Checked against the original expectation in a back-and-forth** — ✓ operator-ratified at the PHASE 3 reconcile gate and the PHASE 6 proposal gate (including the operator's correction of the un-satisfiable absolute "no WARN").
5. **Records updated, incl. ARCHIVE** — ✓ **completed BY this record.** The arc updated JOURNAL/BACKLOG/PLAYBOOK/gotchas, but the audit's own `docs/audits/` archive was the missing piece; the first close over-claimed (5) as fully met. This file closes the gap.
6. **The verification organs RUN green against THIS arc** — ✓ close gate + post-ship: FAIL-class organs exit 0, awareness organs show only the **dispositioned** #77 WARN (per the refined point (6)), pytest 407p/1s, ruff clean.

---

## Commit pointers

| commit | what |
|---|---|
| `e979730` | the `--no-ff` merge to `main` (`Closes [#11] [#111]`) |
| `88ab795` | PHASE 4 — backlog reconcile (close #11/#111, #139→P2, grooming-log) |
| `fe405b4` | PHASE 5 / F2 — `audit.py` ASCII-fold |
| `83a41b4` | PHASE 6 / F1 — PLAYBOOK point (6) + #147 note sharpen |
| `8859c9e` | JOURNAL session entry |
| `2439268` (`~/.claude`) | F3 — P0 self-trip gotcha |

---

## Process gotcha captured

**`/ship`-ing a branch that REMOVED backlog tasks needs the bracketed `[#id]` in the merge summary.**
The `backlog-id-on-close` commit-msg hook fires on the **merge commit** and blocks if a removed
task's id is not referenced in bracketed form (`[#11]` / `closes [#11]`) — bare prose like
"close #11" does NOT satisfy it. Witnessed 2026-06-10: the FINAL `/ship` merge was rejected
("BACKLOG task(s) #11, #111 removed but not referenced") and recovered by completing the staged
merge with a bracketed-id message. `ship.md`'s usage line already hints this
(`/ship "<merge summary [closes #id]>"`). Mirrored into the `~/.claude` gotchas skill.
