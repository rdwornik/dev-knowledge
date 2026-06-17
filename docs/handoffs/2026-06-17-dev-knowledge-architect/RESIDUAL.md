# Residual — 2026-06-17 session, **architect mode** (v5.2 canonical §13)
<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — this time the
> headline is **mostly clean**: `main` is back **in sync** and the merged stragglers were cleaned
> since 2026-06-16, but **one actionable drift carries** (§1: the `ARCHITECTURE.md` `pytest_collected`
> count, now 511→**534**). Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and
> the **durable** serialize-group graph (#156), not re-narrated IDs. Generated from inside the repo at
> HEAD `ef62dd8`, working tree clean, `main` in sync with `origin/main`. Re-derive HEAD/sync at
> read-time (P3).
>
> **Provenance — reconstructed, not witnessed-live.** This is a **fresh CC session**; the v5.2 arc it
> hands off was done in a **prior** session, so there is **no live session reasoning** to transmit. The
> planning "why" below is **reconstructed from the repo** — JOURNAL (the 2026-06-17 entry + last ~6),
> BACKLOG, and the 2026-06-16 `-architect` bundle. State facts (§1, §5) are **witnessed** (verified live
> at generation); design framing (§2–§4) is **recall/inferred** from those sources — verify against the
> live BACKLOG (§5), do not trust the re-narration.
>
> **Scope — a fresh handoff at an arc boundary.** The state moved since 2026-06-16: the 2026-06-16
> bundle's **first-dogfood finding** (a cold/`/clear`ed handoff produced **no** supplement file) **landed
> its fix as HANDOFF_PROCESS v5.2** — the architect strategic supplement is now an **always-generated,
> committed, fillable file** with a defined cold-handoff disposition. Orient first (`PROBES.md` P1),
> **then ask the operator for off-repo context** (§13d / #159 — the supplement ANSWERS are empty this
> session, so the beat fires **full**), then resume the design.
>
> **This bundle is itself the v5.2 cold case — read §2 "Where v5.2 leaves the dogfood".** This is the
> **first architect handoff generated under v5.2**, and like 2026-06-16 it is cold (fresh CC session, no
> outgoing browser). v5.2 makes that case **defined, not a gap**: `SUPPLEMENT.md` is generated and
> committed with empty ANSWERS. But the **real** #159 dogfood — a supplement filled with *actual* answers,
> folded into a `PASTE_THIS` — is **still owed** (surfaced, not buried).

---

## 1. Drift-flags — the headline (this time: **mostly clean, one carry**)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus CC's
state read at generation. **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (16/19 pass; 2 `[--]` n/a + 1 `[~~]` informational — health exits OK). Re-derive at
read-time (P3/P4/P6/P7).

### DRIFT — actionable: `ARCHITECTURE.md` **`pytest_collected` is stale** *(the headline carry — fix owed)*

`validate_doc_claims` reports `pytest_collected@ARCHITECTURE.md` **doc=511, actual=534** — the count
moved **further** past the doc since 2026-06-16 (was 511→530; the v5.2 `assemble_paste` ANSWERS-fold
tests added the +4). This is the **same** drift the 2026-06-16 bundle flagged, **still unfixed** —
carried, not introduced here. **Honest enforcement limit:** `audit.py health`'s integrated `doc_claims`
check reports `[OK] 3 self-claims match` and **does NOT catch this** — it gates only 3 of the 4 claims
(`audit_check_count`, `precommit_hook_count`, `precommit_hook_roster`); **only the standalone
`validate_doc_claims.py` (which probe P6 binds to) surfaces `pytest_collected`.** So `health: OK` is
*not* sufficient evidence the doc-claims are clean here.

- **Fix path (next-session work, not this handoff):** bump ARCHITECTURE's `**N collected**` claim
  (line 274) to the live `pytest --collect-only` count, then **genuinely re-read + re-stamp
  `last_reviewed`** (ARCHITECTURE is a canonical living doc — `canonical_freshness` will FAIL the
  *next* commit if the count edit lands without a re-stamp; the JOURNAL 2026-06-16 "operational gotcha"
  documents this exact sequencing trap). Left as a flagged drift, not silently patched mid-handoff.
- **Confirm:** `python scripts/validate_doc_claims.py` (the `pytest_collected` line).

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable — carried)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still present
(open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77
  legitimately stays open. Direction-(a) #90a structurally cannot distinguish a misattributed closure
  from a real one; only arc-content inspection (**#139** / direction-(b)) can.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py`.

### STATE — `main` is **in sync** with `origin/main`; **no merged stragglers** *(a clean change from 2026-06-16)*

The 2026-06-16 bundle flagged `main` **ahead 9** of origin (unpushed) + **six merged stragglers**. Since
then the v5.2 arc was **pushed** and the stragglers were **`-d`'d** — `git status -sb` reports
`## main...origin/main` (in sync) and `git branch --merged main` shows **only `main`**. The only other
branch is `automation/fleet-audit` (**never merges to main by design — ADR-84**, NOT a loose end).
**This handoff's own commits will put `main` ahead of origin again until pushed** (push is
operator-gated). Re-derive at read-time — `git status -sb` + `git branch --merged main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The 2026-06-16 first-dogfood finding drove this window's work: it landed its fix as v5.2.** Since
2026-06-16 [witnessed via JOURNAL + audit state]:

- **v5.1 ephemeral block → v5.2 always-generated fillable file (the window's headline ship).** v5.1
  made the architect's strategic *why* a first-class advisory supplement, but the supplement became a
  durable artifact **only after** the outgoing browser answered an **ephemeral terminal interview block**
  — so a cold/`/clear`ed handoff produced **no file at all** (missing-deliverable look, zero git tracking,
  operator un-led). That is exactly what the 2026-06-16 bundle's §2 surfaced as a design question. **v5.2
  answers it structurally:** CC now writes `<bundle>/SUPPLEMENT.md` **unconditionally** (a self-documenting
  3-step header + a QUESTIONS section for the outgoing chat + an empty ANSWERS section), **commits it on
  the handoff branch** (empty or filled) for durable tracking, and `scripts/assemble_paste.py` folds the
  **ANSWERS region only, and only when non-empty** (was: whole-file fold + `[warn]`-if-absent). The
  **cold-handoff disposition** is now *defined* (empty ANSWERS = committed N/A, not folded; the incoming
  §13(d) beat fires full). Contract unchanged: advisory, why-only, never teeth, **never fabricated**
  (unanswered = committed empty). Coupled atomic move: `CONTRIBUTING.md` stamp v5.1→**v5.2** (the only
  gate-forced surface — major stays 5, so `CLAUDE.md` / `.claude/commands/handoff.md` unchanged); ADR-82
  amended in-file 2026-06-17. **Dogfooded** by rewriting the 2026-06-16 bundle's own `SUPPLEMENT.md` in
  the new always-file format (empty ANSWERS — the cold case), verifying the cold path folds nothing and
  leaves the immutable `PASTE_THIS.md` unchanged.
- **The carried governance themes are unchanged this window** — ADR-85 lifecycle-gate (the deterministic
  no-LLM Stop-gate: hard JOURNAL leg + advisory BACKLOG leg + HEAD-bound `/override`) shipped its v1 and
  the loop-defect fix (#142) in the *prior* window; this window touched none of it. The two ADR-85 build
  chains (#170→#168 traceability spine, #171→#169 conformance dashboard) and ADR-86 stand as filed.

**The design tensions now on the table** [recall/inferred]:

- **(A″) The hybrid handoff is shipped, hardened (v5.2), but the *value* is STILL un-dogfooded.** v5.1
  answered the *design* question; v5.2 closed the *cold-handoff* gap and hardened the mechanism (always-
  file, ANSWERS-only fold, defined N/A). But **no supplement has ever been filled with real answers and
  folded into a live `PASTE_THIS`.** Until one real run, "judgment transmits via the supplement" is a spec
  assertion, not an empirical fact. **This handoff is again cold** — so it again does not exercise the
  filled path unless the operator routes the QUESTIONS to a chat holding the v5.2 deliberation. The #159
  candidate persists; see "Where v5.2 leaves the dogfood" below.
- **(B) PLAYBOOK Move 2 — maintainability, not parallelism (unchanged, still Council-bound).** Move 1
  barely shrank the file; Move 2 (the structural split → thin `§N`-index + per-section modules) is
  justified on **maintainability** (≈84k tokens, ~3.5× the read-cap, frequently edited), **not**
  parallelism. Council-bound because the `§N`-index design is a genuine fork — the §1–§19 spine is the
  **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so the split must preserve §N
  addressability. See §3 Q-B.

### Where v5.2 leaves the dogfood (the #159 signal, surfaced — not a defect this time)

The 2026-06-16 §2 raised this as an open *question*; v5.2 **resolved the design and now this bundle
demonstrates the resolved behaviour** [witnessed this session]:

- **2026-06-16's open question is RESOLVED — do not re-open it.** "Does the v5.1 flow need a defined
  behaviour for the cold/`/clear`ed handoff?" → **yes, and v5.2 is it**: always-generate + commit the
  empty `SUPPLEMENT.md`, fold ANSWERS-only-if-non-empty, fire the incoming §13(d) beat full. This bundle's
  own `SUPPLEMENT.md` is the live demonstration (committed, empty ANSWERS).
- **What STILL stands open is the *empirical* leg, not the design.** #159's only-remaining clause is to
  exercise the **filled** path once — operator routes QUESTIONS → a chat holding the strategic *why*
  authors answers → CC commits the filled file → `assemble_paste.py` folds the ANSWERS region into the
  next session's `PASTE_THIS`. v5.2 makes that path *reachable and durable*; it does not *run* it.
- **The standing meta-argument (persists, now sharper):** every v5 bundle — **including this one** — is
  **hand-assembled** by CC following the spec; this is now also the first hand-assembly of the v5.2
  always-file `SUPPLEMENT.md`. That growing hand-maintained surface is the live case for **#164 (the
  generator)** and **#161 (the probe-core)**.

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The live questions:

- **Q-A″ — run the real supplement dogfood + finish the generator (#159 + #164).** v5.2 shipped the
  *mechanism* (always-file + cold disposition + ANSWERS-only fold); the open work is (i) **exercise a
  *filled* supplement end-to-end in a real architect session** (#159's only-remaining clause — this
  session is again the candidate, but cold), and (ii) **#164 wires the emission durably in the always-file
  form** (the generator must write the unconditional `SUPPLEMENT.md` from
  `templates/handoff/v5/SUPPLEMENT.md.tmpl`).
- **Q-B — PLAYBOOK Move 2 (Council-bound, unchanged).** The structural split → thin `§N`-index +
  per-section modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N
  addressability — the consumer API). Maintainability-justified, not urgent. **Unblocks #39;
  decouples #18 / #67 / #77 / #146** (the playbook serialize-group).
- **Q-C — #164, the v5 generator (the last machinery item).** `.claude/commands/handoff.md` still
  carries the v4 8-file two-phase generator (marked SUPERSEDED); the v5 emissions are specified but not
  the wired generator. **Open sub-decisions:** (i) the **per-repo-runbook sync key** —
  write-if-absent-or-version-changed, but *keyed how* (handoff-process version? a content hash?); (ii)
  the **cross-repo v4 routing** (ADR-83) — a v4 target repo (lacking `scripts/audit.py`) needs a
  deterministic route to the v4 Phase-1/2 path; (iii) **architect-mode supplement emission in the v5.2
  always-file form** — the generator must write the unconditional `SUPPLEMENT.md` (QUESTIONS + empty
  ANSWERS) and re-run the assembler on `supplement filled`; (iv) a `PASTE_THIS.md` **freshness gate vs its
  sources** (audit F4 — today the assembled snapshot can silently drift).
- **Q-D — #162, architect actor-vs-mode vocab.** Disambiguate "architect" the Layer-1 **actor**
  (browser-chat role) from "architect" the §13 **mode** atomically across every surface — rename one
  sense or formally scope both; do not leave the collision live.
- **Q-E — #161, teeth probe-core.** Define a stable shared probe-core (the ~5 forced-read probes) + the
  architect orientation probe, so bundles **stop hand-assembling probe sets** per handoff. Capture-only
  (scoping is a future architect decision) — but note **this bundle is again a hand-assembled probe
  set** (the persisting capture point).
- **Q-F — #166, doctrine_enforcement_coherence check (audit-py).** A read-only `audit.py` check
  flagging any ADR/amendment still `PROPOSED` / `NOT RATIFIED` while its implementing task is closed
  (live enforcement ahead of its doctrine — the #156 gap reconciled by hand on 2026-06-14; ADR-82 still
  reads "Proposed" in-header vs operator-ratified is a live instance).
- **Q-G — #167, multi serialize-group schema + parser anchoring.** `_parse_serialize_group` reads only
  the FIRST clause, so a task colliding on two surfaces can't be fully encoded — the 2026-06-14 pass
  dropped two real edges (#105↔#112 on `block_immutable_edits.py`, #5↔#77 on `ESSENTIALS.md`). Also
  **anchor the parser to clause position** so prose tokens can't self-trip it (the 2026-06-14 incident).
- **Q-H — #165, ASCII-vs-mermaid selection rule.** A *proposed* ADR-51-family amendment (operator-set
  2026-06-12; first applied when the v5 runbook chose mermaid), awaiting ratification — not a
  unilaterally minted ADR. Record where the diagram convention lives once ratified.
  `serialize-group: architecture`.
- **Q-J — #170 → #168, the traceability spine.** Design + land the traceability-spine ADR (issue-ID↔commit
  anchor) — the airtight, **always-warranted** link that promotes ADR-85's BACKLOG leg from advisory to a
  **hard** gate (#168 depends-on #170). The spine is the un-gameable AND always-warranted anchor the
  interim structural-marker check lacks.
- **Q-K — #171 → #169, the conformance dashboard.** Build `ecosystem/conformance.md` (ADR-86 / ADR-85 R2)
  — a read-only validator generates **and commits its own output** (ADR-80 committed-generated-zone writer
  policy). It is the deterministic surface #169's ungated-doc staleness signal (ARCHITECTURE/VISION/
  LESSONS/CONTRIBUTING untouched >N sessions while code changed) lands in, and ARCHITECTURE Ch2 will
  point to it.
- **Q-L — ADR-85 standing governance obligation (not a design question — a watch).** The gate is **live**.
  A **4-week scope-freeze runs to ~2026-07-14**; watch `logs/OVERRIDES.md` for override-rate (**>~10% →
  tune the rules**). Surfaced so the next session doesn't re-open ADR-85's shape mid-freeze.

**Resolved-since 2026-06-16 (do NOT re-open):** the v5.1 cold-handoff supplement gap (→ **HANDOFF_PROCESS
v5.2** — always-generated fillable file + defined cold disposition + ANSWERS-only fold; only the *empirical*
#159 dogfood + #164 wiring remain) · the hybrid-handoff *design* (v5.1) · the Stop-hook loop defect
(#142) · ADR-85 v1 itself (only the R1/R2 hardenings #168/#169 remain as Q-J/Q-K).

---

## 4. The task-graph (durable hard edges — #156 shipped)

#156 shipped — **hard edges are DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. Point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b).

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** **9 serialize-groups**
  at generation. The **handoff** group = `{#1, #26, #159, #161, #162, #164, #10}` — these **serialize**
  (do not co-schedule). The **playbook** group = `{#146, #77, #67, #18, #39}`. The **audit-py** group =
  `{#153, #7, #36, #95, #140, #139, #166}`. The **architecture** group = `{#165, #35}`. (Plus `claude-md`,
  `claude-md-template`, `environment`, `pre-commit-config`, `settings-json` — see the validator's full
  summary line.) Hard precedence edges (`depends-on`): **#168 → #170**, **#169 → #171**. Parallel-safety
  is **derived** (no shared group + no `depends-on` path).
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q-A″ (#159 dogfood) is exercisable THIS session** — off the build path; but only if a chat holding
    the strategic *why* fills the supplement (this bundle is cold — see §2).
  - **#164 (Q-C) is the last big build item** — gated on the Q-C(i)–(iv) decisions; now also wires the
    v5.2 always-file `SUPPLEMENT.md` emission.
  - **#170 (Q-J) unblocks #168**; **#171 (Q-K) unblocks #169** — two independent ADR-85 build chains,
    parallel to each other and to the handoff group.
  - **Move 2 (Q-B) unblocks #39** and **decouples #18 / #67 / #77 / #146** — landing it dissolves the
    playbook serialize-group.
  - **#166 / #167 are independent cleanups** — #166 serializes within the audit-py group; #167 is bare.

(The "decision-not-build / unblocks / parallel" framing is residual judgment; the serialize-group +
`depends-on` edges are the schema fact. #156 made the *hard* edges durable, not these *soft* ones.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` themes **"Handoff continuity"** (the handoff group),
  **"Enforced governance"** (#168/#170, #166, #167), and **"Canonical-file integrity"** (#169/#171) for
  the live tickets. Do **not** trust any re-narrated ID text — open the live BACKLOG (the §3 text is
  recall; the file is truth). `validate_backlog`: **75 tasks, 0 warnings, 7 themes, 19 stories, 9
  serialize-groups** at generation.
- **Live branches at generation** (`git branch -v`): `main` (**in sync** with origin at generation; this
  handoff's own commits put it ahead until pushed); `automation/fleet-audit` (**never merges to main by
  design — ADR-84**, NOT a loose end). **No merged stragglers** (cleaned since 2026-06-16). This handoff's
  own branch `docs/handoff-2026-06-17-architect` merges on completion.
- **Drift-flags:** the **actionable** `pytest_collected` 511→534 (§1, fix owed — carried from 2026-06-16)
  + the carried-benign `git_backlog_drift` #90a `[~~]` (#77). `main` in sync at generation. Re-derive:
  `python scripts/audit.py health` + `python scripts/validate_doc_claims.py` + `git status -sb`.
- **Audit-gating note:** `audit.py` check #19 `handoff_probes` validates the **lexically-max** v5
  bundle. `2026-06-17-dev-knowledge-architect` is now lexically-max → it **is** this check's target
  (superseding 2026-06-16). Its probes were verified to bind via `python scripts/verify_handoff_probes.py
  docs/handoffs/2026-06-17-dev-knowledge-architect`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **20 closure proposals** await — `/review-closures` (human-gated, done-items-leave).
- **changelog drift** — `claude-code 2.1.179 > last reviewed 2.1.177` — `/changelog-review`.
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **`main` will be ahead of origin after this handoff's commits** — push is the operator's call (the
  serial-push gate). At generation `main` was in sync.
- **ARCHITECTURE `pytest_collected` drift** (§1) — bump 511→live count + genuine re-read/re-stamp.
- **ADR-85 override-rate watch** — `logs/OVERRIDES.md`; scope-freeze to ~2026-07-14.
