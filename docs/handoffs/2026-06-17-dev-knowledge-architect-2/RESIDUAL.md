# Residual — 2026-06-17 session (#2), **architect mode** (v5.2 canonical §13)
<!-- scope: meta -->

> **⚠ UPDATE (post-generation) — the supplement was FILLED. This banner overrides the cold-case
> language below.** This bundle was *generated* cold (fresh CC session — true, and preserved below
> as generation-time history), but the operator then obtained **real architect answers** and
> `supplement filled` them into `SUPPLEMENT.md` — the **second real #159 fill→fold dogfood**. Two
> things change for *you*, the incoming architect: **(1)** the `SUPPLEMENT.md` ANSWERS folded into
> your `PASTE_THIS` are **real, not empty** — read them as the authoritative strategic *why* (the
> 107-candidate brainstorm → why coherence spine v1 is a *proof-of-concept for a doctrine* not just
> a feature; the crux-flip "the **enumerator** is load-bearing, not the trigger"; the
> deterministic-trigger / AI-per-site-verdict / human-signature boundary; the §16 do-not-build list;
> DEC-01/03/04/07; and the priority order of the next coherence-by-memory failure classes). **(2)**
> the §13(d) operator-context beat **narrows to "anything changed since the supplement was
> written?"** — it does **NOT** "fire full." Every "cold / empty ANSWERS / beat fires full" phrasing
> below is **generation-time history**; the folded answers + this banner are the live truth.
>
> **⚠ Operationally load-bearing (from the answers — surfaced, not buried):** the architect's
> **first backlog action** is to **extract the v2-deferred items out of `#172`'s body into their own
> backlog IDs BEFORE `#172` is closed** — else the roadmap orphans on closure. The operator is
> poised to `/review-closures` `#172`; do the extraction first. Also decided in the answers: **name
> the paradigm as an ADR, not a VISION** (a VISION invites the maximalism just resisted); the §7
> review-command canon resolves to a **graduated rule** (interim/small → `/code-review high`; final
> pre-merge, 3+ files → `/codex-review` for the independent lens — confirm Codex auth-mode first).
> Do **not** reparent `#169`/`#166` yet (deferred until ≥2 real drifts); do **not** hand-close `#172`.

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — this time the
> headline is **clean on doc-claims**: the actionable carry the *prior* bundle flagged
> (`ARCHITECTURE.md` `pytest_collected` 511→534) was **resolved** (now 587/587), `main` is **in
> sync** with origin, and `audit.py health` is **OK**. Two residual loose ends remain — the
> carried-benign `#77` `[~~]` WARN and **two merged handoff stragglers** awaiting `-d` (operator-gated).
> Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` + the **durable**
> serialize-group graph (#156), not re-narrated IDs. Generated from inside the repo at HEAD
> `adf0cbe`, working tree clean, `main` in sync with `origin/main`. Re-derive HEAD/sync at
> read-time (`PROBES.md` P3).
>
> **Provenance — reconstructed, not witnessed-live.** This is a **fresh CC session** (`/clear`ed);
> the arc it hands off (the supplement-fill dogfood + the coherence-spine v1 integration) was done
> in **prior** sessions, so there is **no live session reasoning** to transmit. State facts (§1, §5)
> are **witnessed** (verified live at generation via the read-only drift-checks); design framing
> (§2–§4) is **recall/inferred** from JOURNAL (the four 2026-06-17 entries + the last ~6), BACKLOG,
> and the two prior bundles — verify against the live BACKLOG (§5), do not trust the re-narration.
>
> **Scope — a fresh handoff one arc-boundary past `…-architect` (this is bundle #2 of 2026-06-17).**
> The state moved since the `2026-06-17-dev-knowledge-architect` bundle was generated: (1) that
> bundle's `SUPPLEMENT.md` was **filled** with real architect answers — the **first end-to-end #159
> fill→fold dogfood** — surfacing the operator's strategic reframe ("**file-oriented dependency
> management**"); and (2) the **coherence-spine v1** shipped whole (#172 done-when met; #171 now
> buildable) — *the first concrete v1 of that very reframe*. Orient first (`PROBES.md` P1), **then ask
> the operator for off-repo context** (§13d — **per the UPDATE banner the supplement was FILLED, so this beat NARROWS to "anything changed since the supplement?"**; see §2), then resume the design.
>
> **This bundle is itself a v5.2 cold case.** Like the prior two architect bundles it is cold (fresh
> CC session, no outgoing browser holding *this generation's* deliberation). v5.2 makes that
> **defined, not a gap**: `SUPPLEMENT.md` is generated + committed with **empty ANSWERS** (the
> assembler folds nothing; the incoming §13(d) beat fires full). The *prior* bundle's filled
> supplement + the JOURNAL "Notable" line carry the operator's most recent strategic *why* — read
> them as the planning context (pointer in §2), then the beat asks what changed since.

---

## 1. Drift-flags — the headline (this time: **clean on doc-claims; two loose ends**)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90, plus CC's
state read at generation). **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (17/20 pass; 2 `[--]` n/a + 1 `[~~]` informational — health exits OK). Re-derive at
read-time (P3/P4/P5/P6/P7).

### STATE — the prior bundle's actionable carry is **RESOLVED**: `pytest_collected` now matches

The `2026-06-17-dev-knowledge-architect` bundle flagged `pytest_collected@ARCHITECTURE.md` as
doc=511 vs live=534 (the headline "fix owed"). During the coherence-spine arc that drift was
**fixed**: `ARCHITECTURE.md` line 274 was bumped to the live count and re-stamped (commits
`79ff7dd` 511→564, then `3fd2621` 564→587). `validate_doc_claims` now reports **all 4 claims match**
— `pytest_collected (doc 587 / actual 587)`, `audit_check_count (20/20)`, `precommit_hook_count
(9/9)`, roster matches. **No actionable doc-claim drift this handoff.** *(Honest enforcement limit
still stands: `audit.py health`'s integrated `doc_claims` gates only 3 of the 4 claims — only the
standalone `validate_doc_claims.py` (probe P6) surfaces `pytest_collected`; so "health: OK" alone is
not proof the count is clean — P6 re-derives it.)* **Confirm:** `python scripts/validate_doc_claims.py`.

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable — carried)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still present
(open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77
  legitimately stays open. Direction-(a) #90a structurally cannot distinguish a misattributed closure
  from a real one; only arc-content inspection (**#139** / direction-(b)) can.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py`.

### STATE — `main` is **in sync** with origin; **two merged handoff stragglers** await `-d`

`git status -sb` reports `## main...origin/main` (in sync at generation — the coherence-spine arc was
pushed). But `git branch --merged main` now shows **two merged stragglers**:
`docs/handoff-2026-06-17-architect` and `docs/handoff-2026-06-17-supplement-filled` — both merged,
neither `-d`'d. (The only other branch, `automation/fleet-audit`, **never merges to main by design —
ADR-84**, NOT a loose end.) Deleting merged branches is **operator-gated** (no-branch-deletion-without-
asking) — surfaced, not done. **This handoff's own branch** `docs/handoff-2026-06-17-architect-2`
merges on completion and **puts `main` ahead of origin until pushed**. Re-derive at read-time —
`git status -sb` + `git branch --merged main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The arc this window: the operator's strategic reframe became the first concrete mechanism.** Two
linked things landed since the `…-architect` bundle [witnessed via JOURNAL + audit state]:

- **#159 fill→fold dogfood (the supplement proven live).** The operator relayed **real** architect
  answers into the prior bundle's `SUPPLEMENT.md` and said `supplement filled`; CC committed them
  **verbatim** (advisory/non-fabricated contract) and `assemble_paste.py` folded the **ANSWERS region
  only** (zero QUESTIONS leakage, verified) into that bundle's `PASTE_THIS.md`. This is the **first
  end-to-end exercise** of the v5.1/v5.2 fill→fold path — #159's *fill* half. **Surfaced, not buried —
  the load-bearing output:** the operator reframed the whole methodology as a **"file-oriented
  dependency management"** paradigm (Markdown files = objects, the AI = runtime), the systemic fix for
  the coherence-by-memory failure class. That reframe is now in external research and is the **candidate
  top thread** for the next architect session. **Pointer (not re-narrated here):**
  `docs/handoffs/2026-06-17-dev-knowledge-architect/SUPPLEMENT.md` (the verbatim answers) + the JOURNAL
  2026-06-17 "supplement FILLED" entry "Notable" line.
- **Coherence spine v1 — the first concrete v1 of that reframe (the window's headline ship, #172).**
  Built in three parallel-then-integration prompts: **(A)** a generic deterministic **reconciliation
  checker** (`scripts/validate_reconciliation.py`) reading each dependent's `reconciled_with:
  <spec-id>@<version>` frontmatter edge against the spec's **live** version — registered as the **20th
  `ALL_CHECKS` entry** (`check_reconciled_versions`; mismatch → `Finding(fail)`, malformed → `Finding(warn)`
  fail-open) — plus a **non-blocking forgotten-version-bump nudge** (`scripts/coherence_nudge.py`,
  instrumented to `logs/coherence-nudge.log`); **(B)** a **reconciliation enumerator**
  (`scripts/coherence_enumerator.py`) + the `check-against-spec` skill that, given a stale-edge flag,
  **over-extracts every candidate reference site** by category (sections / walkthrough_steps / diagrams /
  commands / summaries — "never miss") and an LLM verdicts **each** (`stale|fine|not-relevant`); **(C)**
  the **integration** — wired the enumerator to A's real `enumerate_edges()` contract (replacing B's stub),
  deduped the spec-version parser to one, added the **e2e closure gate** (`tests/test_coherence_integration.py`:
  spec 5.2→5.3 + stale walkthrough + un-updated mermaid → real `Finding(fail)` → both missed sites named
  by category), and **locked the `Finding` output format** for #171's dashboard. **#172's "Done when" is
  fully met** → ready for the operator-gated Tier-1 closure loop (`/review-closures`).

**The design tensions now on the table** [recall/inferred]:

- **(A‴) "File-oriented dependency management" — the paradigm is named + has a v1, but is un-elaborated
  as doctrine.** The coherence spine is its *first* mechanism (specs are the "definition", dependents
  declare a `reconciled_with` edge, a deterministic check + LLM enumerator catch version-lag drift). The
  open architecture work is whether/how to elaborate this into a named governing model (an ADR? a
  VISION/ARCHITECTURE thread?) and which *other* coherence-by-memory failure classes it should next
  cover. This is the candidate top thread (§3 Q-A‴).
- **(B) The deterministic-vs-judgment split is now a shipped invariant — guard it.** The spine's R2
  framing (operator ruling): the **deterministic** guarantee is *version-lag-detected + every candidate
  site enumerated*; the **staleness verdict is the LLM/human advisory gate** (`check-against-spec`),
  never claimed by the test. Coherence v2 must preserve that line (don't let the enumerator's output
  harden into an auto-edit). See §3 Q-A‴(v2).
- **(C) PLAYBOOK Move 2 — maintainability, not parallelism (unchanged, still Council-bound).** The
  structural split → thin `§N`-index + per-section modules is justified on **maintainability** (≈84k
  tokens, ~3.5× the read-cap, frequently edited), **not** parallelism. Council-bound: the §1–§19 spine
  is the **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so the split must preserve §N
  addressability. See §3 Q-C.

### Where the coherence spine leaves v2 (the firing-rate-gated triggers, surfaced)

v1 deliberately stopped at *surface + advise*; v2 is **data-gated**, not scheduled [witnessed via JOURNAL]:

- **The nudge's escape-hatch / deferred-hash / promote-to-gate decision is gated on real firing data.**
  Every forgotten-version-bump fire appends to `logs/coherence-nudge.log`; **v2 fires when that log
  accumulates signal** (a too-noisy nudge → escape hatch or content-hash; a reliably-correct nudge →
  promote to a gate). Do not pre-decide it — read the log first.
- **#171 dashboard is now buildable** against the locked `Finding` format (the integration's deliverable).
- **A surfaced R3 reconcile (do not lose):** the JOURNAL flagged that **PLAYBOOK §7 (~line 1620) names
  `/codex-review` as the canonical pre-merge gate, but this feature's actual practice used `/code-review
  high`.** A `/review` vs `/codex review`-class doc-vs-practice drift — **surfaced for reconcile**, not
  silently resolved. (Also pre-existing, flagged-not-fixed in the enumerator JOURNAL: `CLAUDE.md` §8 still
  says "No repo-level skills directory exists yet" while `.claude/skills/verify/` + `.claude/skills/check-against-spec/`
  now exist — a doc-claim the coherence spine itself could eventually cover.)

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The live questions:

- **Q-A‴ — elaborate "file-oriented dependency management" + run coherence v2 (the top candidate thread).**
  v1 shipped the *first* mechanism (#172). Open: (i) **whether to elaborate the paradigm as named
  doctrine** (the operator's reframe — Markdown = objects, AI = runtime — currently lives only in a
  filled SUPPLEMENT + external research, not in VISION/ARCHITECTURE/an ADR); (ii) **coherence v2**, which
  is *firing-rate-gated* on `logs/coherence-nudge.log` (escape-hatch / deferred-hash / promote-nudge-to-
  gate) — read the log before deciding; (iii) **which next coherence edges** to declare beyond the v1
  single edge (`docs/handoffs/README.md` → `handoff-process@5.2`).
- **Q-A″ — finish the v5 generator (#164) + the *incoming*-beat half of #159.** #159's **fill→fold** half
  is now **exercised** (this window); its only-remaining clause is the **incoming §13(d) beat** — run when
  the *next* architect session boots on a `PASTE_THIS` (this bundle's beat fires full — cold). **#164**
  still carries the v4 8-file generator in `.claude/commands/handoff.md` (marked SUPERSEDED); the v5
  emissions are specified but not the wired generator (must emit the v5.2 always-file `SUPPLEMENT.md`).
- **Q-C — PLAYBOOK Move 2 (Council-bound, unchanged).** Structural split → thin `§N`-index + per-section
  modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N addressability — the
  consumer API). Maintainability-justified, not urgent. **Unblocks #39; decouples #18 / #67 / #77 / #146**
  (the playbook serialize-group).
- **Q-D — #162, architect actor-vs-mode vocab.** Disambiguate "architect" the Layer-1 **actor**
  (browser-chat role) from "architect" the §13 **mode** atomically across every surface — rename one
  sense or formally scope both; do not leave the collision live.
- **Q-E — #161, teeth probe-core.** Define a stable shared probe-core (the ~5 forced-read probes) + the
  architect orientation probe, so bundles **stop hand-assembling probe sets** per handoff. Capture-only
  (scoping is a future architect decision) — note **this bundle is again a hand-assembled probe set** (the
  persisting capture point; serialize-group `handoff`).
- **Q-F — #166, doctrine_enforcement_coherence check (audit-py).** A read-only `audit.py` check flagging
  any ADR/amendment still `PROPOSED` / `NOT RATIFIED` while its implementing task is closed (live
  enforcement ahead of its doctrine — ADR-82 still reads "Proposed" in-header vs operator-ratified is a
  live instance). Serializes within the `audit-py` group.
- **Q-G — #167, multi serialize-group schema + parser anchoring.** `_parse_serialize_group` reads only
  the FIRST clause, so a task colliding on two surfaces can't be fully encoded — two real edges were
  dropped (#105↔#112 on `block_immutable_edits.py`, #5↔#77 on `ESSENTIALS.md`). Also **anchor the parser
  to clause position** so prose tokens can't self-trip it.
- **Q-H — #165, ASCII-vs-mermaid selection rule.** A *proposed* ADR-51-family amendment (operator-set
  2026-06-12; first applied when the v5 runbook chose mermaid), awaiting ratification — not a unilaterally
  minted ADR. Record where the diagram convention lives once ratified. `serialize-group: architecture`.
- **Q-J — #170 → #168, the traceability spine.** Design + land the traceability-spine ADR (issue-ID↔commit
  anchor) — the airtight, **always-warranted** link that promotes ADR-85's BACKLOG leg from advisory to a
  **hard** gate (#168 depends-on #170). *Note the overlap with Q-A‴:* the coherence spine's `reconciled_with`
  edge model is a sibling pattern (a frontmatter-declared dependency edge); whether the traceability spine
  reuses it is an open design connection.
- **Q-K — #171 → #169, the conformance dashboard.** Build `ecosystem/conformance.md` (ADR-86 / ADR-85 R2)
  — a read-only validator generates **and commits its own output** (ADR-80 committed-generated-zone writer
  policy). **Now unblocked** by the coherence integration's locked `Finding` format — the dashboard can
  consume `Finding`s directly. ARCHITECTURE Ch2 will point to it.
- **Q-L — ADR-85 standing governance obligation (a watch, not a design question).** The gate is **live**.
  A **4-week scope-freeze runs to ~2026-07-14**; watch `logs/OVERRIDES.md` for override-rate (**>~10% →
  tune the rules**). Surfaced so the next session doesn't re-open ADR-85's shape mid-freeze.

**Resolved-since the `…-architect` bundle (do NOT re-open):** the `pytest_collected` actionable carry
(→ bumped 511→587 + re-stamped) · the #159 *fill→fold* half (→ exercised live) · the coherence-spine v1
*design* (→ #172 shipped; only v2's firing-rate-gated decisions remain) · the v5.1 cold-handoff supplement
gap (→ HANDOFF_PROCESS v5.2, prior window).

---

## 4. The task-graph (durable hard edges — #156 shipped)

#156 shipped — **hard edges are DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. Point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b).

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** **9 serialize-groups**
  at generation. The **handoff** group = `{#1, #26, #159, #161, #162, #164, #10}` — these **serialize**
  (do not co-schedule). The **audit-py** group = `{#153, #7, #36, #95, #140, #139, #166, #172}` (**#172
  added** this window — the coherence-spine story). The **playbook** group = `{#146, #77, #67, #18, #39}`.
  The **architecture** group = `{#165, #35}`. (Plus `claude-md {#112,#157}`, `claude-md-template`,
  `environment`, `pre-commit-config`, `settings-json` — see the validator's full summary line.) Hard
  precedence edges (`depends-on`): **#168 → #170**, **#169 → #171**. Parallel-safety is **derived** (no
  shared group + no `depends-on` path).
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q-A‴ (coherence v2 / paradigm doctrine) is the top candidate thread** — but v2's sub-decisions are
    *firing-rate-gated* on `logs/coherence-nudge.log`; not schedulable until the log has signal.
  - **#171 (Q-K) is now unblocked** — the integration locked the `Finding` format the dashboard consumes;
    it still **depends-on #171's parent** in the `#169→#171` chain only as encoded.
  - **#164 (Q-A″) is the last big handoff-machinery item** — serializes within the `handoff` group; now
    must also emit the v5.2 always-file `SUPPLEMENT.md`.
  - **#170 (Q-J) unblocks #168**; the coherence `reconciled_with` edge is a *sibling* of the traceability
    edge — a possible reuse, surfaced as a design connection, not a schema fact.
  - **Move 2 (Q-C) unblocks #39** and **decouples #18 / #67 / #77 / #146** — landing it dissolves the
    playbook serialize-group.
  - **#166 / #167 are independent cleanups** — #166 serializes within the audit-py group; #167 is bare.

(The "candidate-thread / unblocks / sibling" framing is residual judgment; the serialize-group +
`depends-on` edges are the schema fact. #156 made the *hard* edges durable, not these *soft* ones.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` themes — the coherence work lives under the audit/governance
  themes (#172 in the `audit-py` group; #171/#169 conformance dashboard; #166/#167 cleanups), the handoff
  group (#159/#161/#162/#164), and the playbook group (Move 2 / #39). Do **not** trust any re-narrated ID
  text — open the live BACKLOG (the §3 text is recall; the file is truth). `validate_backlog`: **76 tasks,
  0 warnings, 7 themes, 20 stories, 9 serialize-groups** at generation.
- **Live branches at generation** (`git branch -v`): `main` (**in sync** with origin at generation; this
  handoff's own commits put it ahead until pushed); `automation/fleet-audit` (**never merges to main by
  design — ADR-84**, NOT a loose end); **two merged stragglers** — `docs/handoff-2026-06-17-architect`,
  `docs/handoff-2026-06-17-supplement-filled` (await operator `-d`, §1). This handoff's own branch
  `docs/handoff-2026-06-17-architect-2` merges on completion.
- **Drift-flags:** doc-claims **clean** (the prior `pytest_collected` carry resolved — §1) + the
  carried-benign `git_backlog_drift` #90a `[~~]` (#77). `main` in sync at generation; two merged
  stragglers to `-d`. Re-derive: `python scripts/audit.py health` + `python scripts/validate_doc_claims.py`
  + `git status -sb` + `git branch --merged main`.
- **Audit-gating note (load-bearing):** `audit.py` check #19 `handoff_probes` validates the
  **lexically-max** v5 bundle. `2026-06-17-dev-knowledge-architect-2` is now lexically-max → it **is** this
  check's target (superseding `…-architect`). Its 10 probes were verified to bind via
  `python scripts/verify_handoff_probes.py docs/handoffs/2026-06-17-dev-knowledge-architect-2`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **21 closure proposals** await — `/review-closures` (human-gated, done-items-leave). **#172 is the
  ready one** (its "Done when" is met — close it here).
- **changelog drift** — `claude-code 2.1.179 > last reviewed 2.1.177` — `/changelog-review`.
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **two merged handoff stragglers** — `docs/handoff-2026-06-17-architect`,
  `docs/handoff-2026-06-17-supplement-filled` — `-d` is the operator's call (§1).
- **`main` will be ahead of origin after this handoff's commits** — push is the operator's call (the
  serial-push gate). At generation `main` was in sync.
- **ADR-85 override-rate watch** — `logs/OVERRIDES.md`; scope-freeze to ~2026-07-14.
