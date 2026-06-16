# Residual — 2026-06-16 session, **architect mode** (v5.1 canonical §13)
<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — and this time the
> headline is **NOT clean** (§1: an actionable ARCHITECTURE count drift + the unpushed `main`).
> Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and the **durable**
> serialize-group graph (#156), not re-narrated IDs. Generated from inside the repo at HEAD
> `0752efa`, working tree clean, `main` **ahead 9** of `origin/main` (unpushed). Re-derive HEAD/sync
> at read-time (P3).
>
> **Provenance — reconstructed, not witnessed-live.** This session was `/clear`ed immediately before
> the handoff, so there is **no live session reasoning** to transmit. The planning "why" below is
> **reconstructed from the repo** — JOURNAL (last ~7 entries), BACKLOG, and the 2026-06-15
> `-architect` bundle. State facts (§1, §5) are **witnessed** (verified live at generation); design
> framing (§2–§4) is **recall/inferred** from those sources — verify against the live BACKLOG (§5),
> do not trust the re-narration.
>
> **Scope — a fresh handoff at an arc boundary.** The state moved **decisively** since 2026-06-15:
> the 2026-06-15 bundle's headline design thread — **(A) the hybrid handoff** ("v5 has no formal slot
> for browser-authored judgment") — **substantially landed as HANDOFF_PROCESS v5.1** (the architect
> strategic supplement). A **new** governance theme also shipped its v1: **ADR-85 session-lifecycle
> enforcement** + the Stop-hook loop fix. Orient first (`PROBES.md` P1), **then ask the operator for
> off-repo context** (§13d / #159), then resume the design.
>
> **First v5.1 supplement dogfood — read §2 "The supplement-interview finding".** This is the **first
> architect handoff to emit the v5.1 supplement interview block**. The honest empirical finding is
> already in hand (a cold/`/clear`ed handoff has no *outgoing* browser to interview) — that is exactly
> the #159 dogfood signal, surfaced not buried.

---

## 1. Drift-flags — the headline (this time: **NOT clean**)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus CC's
state read at generation. **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (16/19 pass; 2 `[--]` n/a + 1 `[~~]` informational — health exits OK). Re-derive at
read-time (P3/P4/P6/P7).

### DRIFT — actionable: `ARCHITECTURE.md` **`pytest_collected` is stale** *(the headline — fix owed)*

`validate_doc_claims` reports `pytest_collected@ARCHITECTURE.md` **doc=511, actual=530** — the
recent ADR-85 (+ Stop-hook +26 backpressure tests), v5.1 (+3 `assemble_paste` tests) and prior test
additions moved the live collected count past ARCHITECTURE's claim. **Honest enforcement limit:**
`audit.py health`'s integrated `doc_claims` check reports `[OK] 3 self-claims match` and **does NOT
catch this** — it gates only 3 of the 4 claims; **only the standalone `validate_doc_claims.py` (which
probe P6 binds to) surfaces it.** So `health: OK` is *not* sufficient evidence the doc-claims are
clean here.

- **Fix path (next-session work, not this handoff):** bump ARCHITECTURE's `**N collected**` claim to
  the live `pytest --collect-only` count, then **genuinely re-read + re-stamp `last_reviewed`**
  (ARCHITECTURE is a canonical living doc — `canonical_freshness` will FAIL the *next* commit if the
  count edit lands without a re-stamp; the JOURNAL 2026-06-16 "operational gotcha" documents this
  exact sequencing trap). Left as a flagged drift, not silently patched mid-handoff.
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

### STATE — `main` is **ahead 9** of `origin/main` (unpushed) + **six merged stragglers** *(operator-gated)*

A change from 2026-06-15 (which was in sync after that day's push). The ADR-85 lifecycle-gate arc,
the v5.1 verification pass, and the Stop-hook loop fix all landed locally and were **not pushed** —
`git status -sb` reports `## main...origin/main [ahead 9]`. Six merged-but-undeleted feature branches
remain (`docs/handoff-v5.1-architect-supplement`, `docs/handoff-v5.1-boot-beatd-refinement`,
`docs/journal-v5.1-verification`, `feat/adr-85-lifecycle-gate`, `fix/stop-hook-active-is-present`,
`fix/stop-hook-no-autobypass`). Plus `automation/fleet-audit` (**never merges to main by design —
ADR-84**, NOT a loose end). Push + `-d` cleanup are **operator-gated** (no push / no branch deletion
without operator OK). This handoff's own commits will increment the ahead-count further.

- **Confirm:** `git status -sb` + `git branch --merged main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The 2026-06-15 headline thread landed; the work re-centred on enforcement + the un-dogfooded
supplement.** The 2026-06-15 architect bundle named **two** Council-bound threads — **(A) the hybrid
handoff** and **(B) PLAYBOOK Move 2**. Since then [witnessed via JOURNAL + audit state]:

- **(A) the hybrid handoff → SHIPPED as HANDOFF_PROCESS v5.1.** The 2026-06-15 Q-A asked for a
  *formal slot for committed, browser-authored judgment* (v5's residual is by spec CC-authored /
  repo-derived and "structurally cannot carry operator intent"). **v5.1 is that slot:** the architect's
  strategic *why* (intent · tensions · options rejected · open Qs · decomposition rationale · off-repo
  context) is now a **first-class advisory supplement produced by a structured 6-question interview**
  — CC emits a paste-ready block, the operator relays it to the **outgoing** browser, the browser's
  answers become `<bundle>/SUPPLEMENT.md` **verbatim** (no re-typing), folded into the next session's
  `PASTE_THIS` by `assemble_paste.py`. Hard scope-constraint: the interview asks **only**
  non-re-derivable *why* — never repo state / counts / SHAs (those stay forced-read, §3/§5);
  advisory, never teeth; a per-session transient (not a v4-disease maintained surface). ADR-82
  amended 2026-06-16. **Residual clauses: #159 (dogfood — this session) + #164 (the generator must
  wire the emission + the verbatim SUPPLEMENT.md write).**
- **NEW theme — ADR-85 session-lifecycle enforcement v1 shipped.** The executor (not the human) is now
  the session-close trigger via a deterministic, **no-LLM** Stop-gate: a **hard** `decision:block`
  JOURNAL leg (the arc's `JOURNAL.md` additions must name ≥1 `base..HEAD` commit-SHA — un-gameable,
  supersedes the old soft journal-presence check), an **advisory** BACKLOG-marker leg (R1: nudge not
  block in v1), and a pure-read HEAD-bound `/override` token (logged to gitignored `logs/OVERRIDES.md`,
  no auto-bypass). Canon: `protocols/DEFINITION_OF_DONE.md`. **Then the loop-defect fix** (#142): the
  Stop hook **can never loop to the block-cap** — a structural floor (standalone advisory never keeps
  the turn going; it rides only folded inside a hard block) + a freshness same-day exemption + a
  fire-once guard (`stop_hook_active`, witnessed **ACTIVE** at this runtime's wrap, with the floor as
  backstop). The gate is **fail-closed on real non-compliance, fail-open on its own errors**.
- **Consolidation pass under the new DoD** → filed **#170** (traceability-spine ADR — the issue-ID↔commit
  anchor) and **#171** (conformance dashboard at `ecosystem/conformance.md`), plus **ADR-86**
  (dashboard-location decision). These are the new build edges (§3 Q-J / Q-K).

**The two design tensions now on the table** [recall/inferred]:

- **(A′) The hybrid handoff is shipped but UN-DOGFOODED — value is unproven.** v5.1 answered Q-A's
  *design* question, but the supplement interview has **never been exercised end-to-end** (operator
  relays → outgoing browser authors → CC writes `SUPPLEMENT.md` verbatim → folds into the next
  `PASTE_THIS`). Until one real run, the claim "judgment transmits via the supplement" is a spec
  assertion, not an empirical fact. **This session is the first dogfood** — see the finding below.
- **(B) PLAYBOOK Move 2 — maintainability, not parallelism (unchanged, still Council-bound).** Move 1
  barely shrank the file; Move 2 (the structural split → thin `§N`-index + per-section modules) is
  justified on **maintainability** (≈84k tokens, ~3.5× the read-cap, frequently edited), **not**
  parallelism. Council-bound because the `§N`-index design is a genuine fork — the §1–§19 spine is the
  **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so the split must preserve §N
  addressability. See §3 Q-B.

### The supplement-interview finding (first v5.1 dogfood — the #159 signal, surfaced)

This is the **first architect handoff to reach the v5.1 supplement step**, and a cold-handoff design
gap surfaced immediately [witnessed this session]:

- The v5.1 flow targets the **OUTGOING** architect-browser — "*still in context at session end, the
  only actor holding this session's strategic deliberation*." **This handoff was generated after a
  `/clear`** — there is **no outgoing browser in context**, and the residual itself is reconstructed,
  not witnessed-live. So there is no live deliberation for the interview to extract here.
- **Honest disposition (not a fabricated supplement):** CC still emits the paste-ready interview block
  (architect-mode deliverable). The operator routes it to whoever holds the strategic context — a
  still-open prior architect-browser, or the operator answering as the strategic holder — **or skips
  it**, in which case the **incoming** architect's §13(d) operator-context beat (the inbound twin of
  Q6) captures the off-repo context fresh at session start. `assemble_paste.py` will `[warn]`
  `SUPPLEMENT.md` absent — **expected and correct** (no supplement was authored because no outgoing
  browser was in context); CC must **not** synthesize one (that would re-create the v4 disease and
  violate the advisory/non-fabricated contract).
- **The design question for the next architect session (feeds #159/#164):** does the v5.1 flow need a
  defined behaviour for the **cold/`/clear`ed handoff** case — e.g. explicitly fold the supplement into
  the incoming §13(d) beat, or mark it N/A — so "expected in architect mode" doesn't read as a missing
  deliverable when there is structurally no one to interview?

**The standing meta-argument (persists, now sharper):** every v5 bundle — **including this one** — is
**hand-assembled** by CC following the spec, and this is now **also** the first hand-assembly of the
v5.1 supplement-interview emission. That growing hand-maintained surface is the live case for **#164
(the generator)** and **#161 (the probe-core)**.

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The live questions:

- **Q-A′ — dogfood + finish the hybrid handoff (#159 + #164).** v5.1 shipped the *design*; the open
  work is (i) **exercise the supplement interview + the §13(d) beat in a real architect session**
  (#159's only-remaining clause — **this session is the candidate**), and (ii) resolve the
  cold-handoff behaviour above. Then #164 wires the emission durably.
- **Q-B — PLAYBOOK Move 2 (Council-bound, unchanged).** The structural split → thin `§N`-index +
  per-section modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N
  addressability — the consumer API). Maintainability-justified, not urgent. **Unblocks #39;
  decouples #18 / #67 / #77 / #146** (the playbook serialize-group).
- **Q-C — #164, the v5 generator (the last machinery item, L).** `.claude/commands/handoff.md` still
  carries the v4 8-file two-phase generator (marked SUPERSEDED); the v5 emissions are specified but not
  the wired generator. **Open sub-decisions:** (i) the **per-repo-runbook sync key** —
  write-if-absent-or-version-changed, but *keyed how* (handoff-process version? a content hash?); (ii)
  the **cross-repo v4 routing** (ADR-83) — a v4 target repo (lacking `scripts/audit.py`) needs a
  deterministic route to the v4 Phase-1/2 path; (iii) **architect-mode supplement emission** — the
  generator must emit the §13 interview block from `templates/handoff/v5/SUPPLEMENT.md.tmpl` and write
  the browser's answers to `<bundle>/SUPPLEMENT.md` (the v5.1 addition); (iv) a `PASTE_THIS.md`
  **freshness gate vs its sources** (audit F4 — today the assembled snapshot can silently drift).
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
- **Q-J — #170 → #168, the traceability spine (NEW this window).** Design + land the traceability-spine
  ADR (issue-ID↔commit anchor) — the airtight, **always-warranted** link that promotes ADR-85's
  BACKLOG leg from advisory to a **hard** gate (#168 depends-on #170). The spine is the un-gameable
  AND always-warranted anchor the interim structural-marker check lacks.
- **Q-K — #171 → #169, the conformance dashboard (NEW this window).** Build `ecosystem/conformance.md`
  (ADR-86 / ADR-85 R2) — a read-only validator generates **and commits its own output** (ADR-80
  committed-generated-zone writer policy). It is the deterministic surface #169's ungated-doc staleness
  signal (ARCHITECTURE/VISION/LESSONS/CONTRIBUTING untouched >N sessions while code changed) lands in,
  and ARCHITECTURE Ch2 will point to it.
- **Q-L — ADR-85 standing governance obligation (not a design question — a watch).** The gate is **live
  this session**. A **4-week scope-freeze runs to ~2026-07-14**; watch `logs/OVERRIDES.md` for
  override-rate (**>~10% → tune the rules**). Surfaced so the next session doesn't re-open ADR-85's
  shape mid-freeze.

**Resolved-since 2026-06-15 (do NOT re-open):** the hybrid-handoff *design* (Q-A → HANDOFF_PROCESS
v5.1; only #159 dogfood + #164 wiring remain) · the Stop-hook loop defect (#142 — closed by the
structural-floor fix) · ADR-85 v1 itself (shipped; only the R1/R2 hardenings #168/#169 remain as
Q-J/Q-K).

---

## 4. The task-graph (durable hard edges — #156 shipped)

#156 shipped — **hard edges are DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. Point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b).

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** **9 serialize-groups**.
  The **handoff** group = `{#1, #26, #159, #161, #162, #164, #10}` — these **serialize** (do not
  co-schedule). The **playbook** group = `{#146, #77, #67, #18, #39}`. The **audit-py** group =
  `{#153, #7, #36, #95, #140, #139, #166}`. Hard precedence edges (`depends-on`): **#168 → #170**,
  **#169 → #171**. Parallel-safety is **derived** (no shared group + no `depends-on` path).
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q-A′ (#159 dogfood) is exercisable THIS session** — off the build path; the supplement-interview
    finding above is its first signal.
  - **#164 (Q-C) is the last big build item** — `L`, gated on the Q-C(i)–(iv) decisions; pairs with the
    already-shipped #163 validator + the new v5.1 supplement emission.
  - **#170 (Q-J) unblocks #168**; **#171 (Q-K) unblocks #169** — two independent NEW build chains from
    the ADR-85 consolidation; parallel to each other and to the handoff group.
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
  recall; the file is truth). `validate_backlog`: **75 tasks, 0 warnings, 9 serialize-groups** at
  generation (7 themes, 19 stories).
- **Live branches at generation** (`git branch -v`): `main` (**ahead 9** of origin, unpushed);
  `automation/fleet-audit` (**never merges to main by design — ADR-84**, NOT a loose end); and **six
  merged stragglers** (the §1 STATE list) — candidates for `-d` cleanup, **operator-gated**, carried
  not deleted here. This handoff's own branch `docs/handoff-2026-06-16-architect` merges on completion.
- **Drift-flags:** the **actionable** `pytest_collected` 511→530 (§1, fix owed) + the carried-benign
  `git_backlog_drift` #90a `[~~]` (#77). `main` **ahead 9** (unpushed). Re-derive: `python
  scripts/audit.py health` + `python scripts/validate_doc_claims.py` + `git status -sb`.
- **Audit-gating note:** `audit.py` check #19 `handoff_probes` validates the **lexically-max** v5
  bundle. `2026-06-16-dev-knowledge-architect` is the only 2026-06-16 bundle → it **is** this check's
  target now (unlike 2026-06-15, where `-session` > `-architect` shadowed the architect bundle). Its
  probes were verified to bind via `python scripts/verify_handoff_probes.py
  docs/handoffs/2026-06-16-dev-knowledge-architect`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **20 closure proposals** await — `/review-closures` (human-gated, done-items-leave).
- **changelog drift** — `claude-code 2.1.179 > last reviewed 2.1.177` — `/changelog-review`.
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **`main` is ahead 9 of origin (unpushed)** + six merged stragglers — push + `-d` cleanup are the
  operator's call (the serial-push gate).
- **ARCHITECTURE `pytest_collected` drift** (§1) — bump 511→live count + genuine re-read/re-stamp.
- **ADR-85 override-rate watch** — `logs/OVERRIDES.md`; scope-freeze to ~2026-07-14.
