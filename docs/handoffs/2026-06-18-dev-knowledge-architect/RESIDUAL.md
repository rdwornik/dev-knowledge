# Residual — 2026-06-18 session, **architect mode** (v5.2 canonical §13)
<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — this time the
> headline is an **actionable re-drift**: `pytest_collected@ARCHITECTURE.md` says **587** but live
> pytest now collects **614** (this window added ~27 tests and the doc count was not re-bumped). The
> lone other flag is the carried-benign `#77` `[~~]` voided closure. `main` is **in sync** with origin
> and there are **no merged stragglers** this time. Pointers are paths, not copies. Task-state is a
> pointer to `BACKLOG.md` + the **durable** serialize-group graph (#156), not re-narrated IDs.
> Generated from inside the repo at HEAD `62763d7`, working tree clean, `main` in sync with
> `origin/main`. Re-derive HEAD/sync at read-time (`PROBES.md` P3).
>
> **Provenance — reconstructed, not witnessed-live.** This is a **fresh CC session** (`/clear`ed); the
> 2026-06-18 arc it hands off (the equilibrium contract, the coherence-spine consolidation, the backlog
> groom, the worktree-lifecycle gap-fill) was done in **prior** sessions, so there is **no live session
> reasoning** to transmit. State facts (§1, §5) are **witnessed** (verified live at generation via the
> read-only drift-checks); design framing (§2–§4) is **recall/inferred** from JOURNAL (the nine
> 2026-06-18 entries) + BACKLOG + the two prior architect bundles — verify against the live BACKLOG
> (§5), do not trust the re-narration.
>
> **Scope — a fresh handoff one workday past the `2026-06-17-dev-knowledge-architect-2` bundle.** The
> state moved across a heavy 2026-06-18 workday: **ADR-87** (the architect/CC equilibrium contract) was
> ratified + codified; the **coherence-spine consolidation** landed (#172 *closed*, its v2 roadmap
> *extracted* into **#179–#183** — the operator's "extract before close" first-action from the prior
> filled supplement); a **backlog groom** condensed the giants + filed #187–#189; the **worktree /
> parallel-arc lifecycle** was codified in PLAYBOOK; and the floor/schema machinery advanced (#120 +
> #138 closed, #167 multi-serialize-group landed, #186 floor-gap filed). Orient first (`PROBES.md` P1),
> **then ask the operator for off-repo context** (§13d — this bundle is **cold**, so the beat fires
> **full**; see §2), then resume the design.
>
> **This bundle is a v5.2 cold case (no UPDATE banner — unlike `…-architect-2`).** Fresh CC session, no
> outgoing browser holding *this* window's deliberation. v5.2 makes that **defined, not a gap**:
> `SUPPLEMENT.md` is generated + committed with **empty ANSWERS** (the assembler folds nothing; the
> incoming §13(d) beat fires full). The *prior* bundles' **filled** supplements carry the operator's
> most recent strategic *why* (the "file-oriented dependency management" reframe, the §16 do-not-build
> list, "name the paradigm as an ADR") — read them as the planning context (pointers in §2), then the
> beat asks what changed since.

---

## 1. Drift-flags — the headline (this time: **one actionable re-drift + one benign carry**)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90, plus CC's
state read at generation). **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (17/20 pass; 2 `[--]` n/a + 1 `[~~]` informational — health exits OK). Re-derive at
read-time (P2–P9).

### DRIFT — `pytest_collected@ARCHITECTURE.md` **RE-DRIFTED**: doc=587 vs live=614 *(actionable — fix owed)*

`validate_doc_claims` reports `pytest_collected@ARCHITECTURE.md` as **doc=587 / actual=614** — a real
mismatch. The 2026-06-18 window added ~27 tests (the #120 child-BACKLOG probe +22, #167 serialize-group
+3, the equilibrium/floor work) and the `**N collected**` claim in `ARCHITECTURE.md` was **not**
re-bumped. This is the **same drift class** the `2026-06-17-dev-knowledge-architect` bundle headlined
(then doc=511 vs live=534) — it re-drifts on every test-adding window unless the doc is re-stamped.

- **Why it does NOT block the commit (and why this handoff did not "fix" it):** `audit.py health`'s
  *integrated* `doc_claims` gates only **3 of the 4** claims (`audit_check_count`, `precommit_hook_count`,
  `precommit_hook_roster`) — it does **not** gate `pytest_collected`. Only the **standalone**
  `validate_doc_claims.py` (probe **P6**) surfaces it, and that script is **not** a pre-commit hook. So
  "health: OK" is **not** proof the count is clean — P6 re-derives it. The correct fix is a *count bump
  **+** a `last_reviewed` re-stamp*, and the freshness cadence forbids re-stamping `ARCHITECTURE.md`
  without a **genuine end-to-end re-read** (a handoff is not one); a count-bump *without* the re-stamp
  would itself trip the `canonical_freshness` gate (stamp predates last edit). So this is a proper
  **next-session fix** (re-read → bump 587→614 → re-stamp), surfaced here, not silently half-done.
- **Confirm:** `python scripts/validate_doc_claims.py` (the `pytest_collected` line).

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable — carried)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still present
(open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77 legitimately
  stays open. Direction-(a) #90a structurally cannot distinguish a misattributed closure from a real
  one; only arc-content inspection (**#139** / direction-(b)) can. Re-verified again this window in the
  #167-closure session (#5/#77 both **NOT** closed on content grounds — see JOURNAL 2026-06-18).
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py`.

### STATE — `main` is **in sync** with origin; **no merged stragglers** this time

`git status -sb` reports `## main...origin/main` (in sync at generation). `git branch --merged main`
shows **only `main`** — the prior bundle's two merged handoff stragglers were `-d`'d. The only other
branch, `automation/fleet-audit`, **never merges to main by design — ADR-84**, NOT a loose end.
**This handoff's own branch** `docs/handoff-2026-06-18-architect` merges on completion and **puts
`main` ahead of origin until pushed** (push is the operator's call — the serial-push gate). Re-derive
at read-time — `git status -sb` + `git branch --merged main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The arc this window: the architect/CC division of labor became doctrine, and the coherence-spine
roadmap was made durable.** Four linked things landed across 2026-06-18 [recall/inferred via JOURNAL +
audit state]:

- **ADR-87 — the architect/CC equilibrium contract (the window's headline *way-of-working* ship).**
  STEP 3 of the equilibrium arc codified the prompt division of labor that follows from the STEP-1
  self-load finding (*CC self-loads context reliably **only for code-impact tasks**; read-only / GAP-1,
  execution-gotcha / GAP-2, governance / GAP-3 are unreliable — so an intent-only prompt is
  **conditional**, not universal*). **ADR-87 (Accepted, Path A)** is the canonical home: the **architect
  emits** intent + closure + anti-patterns + plan/auto mode + a thin per-task **governance-pointer**;
  **CC owns** code-impact context, generic gotchas, the skeleton (now reframed as CC's *consumption-spec*),
  model/effort. Carried into four durable surfaces (PLAYBOOK §2, `templates/prompt-template.md`,
  ESSENTIALS, `HANDOFF_BOOT.md`). The empirical close is **#184** (demonstrate on a real build — stays
  OPEN; codification ≠ demonstration); the GAP-2 residue is **#185** (a deterministic gotcha-injection
  PreToolUse guard — filed, *not* built, because prose can't fix an execution-time micro-decision class
  that recurred n=2/n=3 even with the standing "check gotchas" line). **Pointer:**
  `docs/decisions/ADR-87-equilibrium-contract.md` + JOURNAL 2026-06-18 "equilibrium contract STEP 3".
- **Coherence-spine consolidation — the prior bundle's load-bearing first-action, executed.** The prior
  `…-architect-2` filled supplement's *critical first backlog action* was: **extract #172's v2-deferred
  items into their own IDs BEFORE closing #172, or the roadmap orphans.** This window did exactly that —
  the v2 roadmap was extracted into **#179–#183** (a **new `coherence` serialize-group**: #179 AGENT-11
  undeclared-edge scan, #180 transclusion engine [gated on DEC-04], #181 nudge-response [data-gated],
  #182 folder-level contracts [DEC-07], #183 reparent #169/#171/#166 [evidence-gated]), and **only then**
  was **#172 closed** via the operator-gated `/review-closures` loop. The coherence doctrine now has a
  durable task-graph home. **Pointer:** `BACKLOG.md` `coherence` group + JOURNAL 2026-06-18 entries
  "#172 v2-roadmap extract" + "close #172".
- **Backlog groom — operationalizing "make the backlog genuinely load-bearing" (the supplement's #1
  intent).** Applied the approved 2026-06-18 groom: **closed #138** (done-undetected), **condensed** the
  giants (#159/#164 + a lighter set, ADR-65 history→git, ADR-83 LIVE constraint on #164 preserved
  verbatim), **pruned** the grooming log to a git-pointer, **absorbed 8 findings**, **filed** #187
  (dedup-on-entry) / #188 (deny-rule + hook completeness audit) / #189 (`~/.claude` commit-check,
  execute-elsewhere). Net 80→83 tasks, 0 warnings. **Pointer:** `BACKLOG.md` + JOURNAL 2026-06-18
  "apply approved backlog groom".
- **Worktree / parallel-arc lifecycle — a way-of-working gap-fill (W1).** Codified the worktree
  discipline **in place** (PLAYBOOK §"Parallel sessions & worktree discipline", *not* a new doc — the
  lifecycle was ~80% already documented). **Empirically verified the load-bearing premise** the
  `seed-state-yaml` memory had wrong: native `claude --worktree` **auto-seeds** all 5 `ecosystem/*/state.yaml`
  (incl. the dot-prefixed hub) and `audit.py health` returns OK from inside the worktree — the seed-block
  is the **raw `git worktree add`** path, which does not honor `.worktreeinclude`. **Pointer:** PLAYBOOK
  §"Parallel sessions & worktree discipline" + JOURNAL 2026-06-18 "W1".

**The design tensions now on the table** [recall/inferred]:

- **(A) "File-oriented dependency management" — the paradigm is roadmapped but still un-named as
  doctrine.** The prior filled supplement was explicit: **"Name it — as an ADR, not a VISION"** (a VISION
  invites the maximalism just resisted; an ADR earns the proven-in-miniature mechanism a decision-record
  + a coherent frame so v2 reads as "extending the paradigm" not ad-hoc feature-adding). This window
  delivered the *durable v2 task-graph* (#179–#183) but **not** the capstone ADR — so #179–#183 currently
  read as a loose feature list, exactly the failure mode the supplement warned against. **This is the
  candidate top thread** (§3 Q1).
- **(B) The architect/CC division of labor is now a *codified* invariant (ADR-87) — but unproven.** STEP 3
  is the codification; the contract has **never been exercised on a real build** (#184). The open
  way-of-working risk is whether the conditional intent-only prompt actually holds in practice, and
  whether GAP-2 (the execution-time micro-decision) genuinely needs the deterministic guard (#185) or
  whether the prompt contract covers it. See §3 Q4.
- **(C) The backlog-load-bearing intent is being lived, not just stated.** The supplement's #1 intent
  ("the architect drives from the backlog and delegates; freewheeling is the anti-pattern to kill") is
  now visibly operationalized — the groom + the #172/#167/#120 operator-gated closures + the durable
  task-graph (#156/#167 multi-serialize-group). The open question is whether **#168** (promote ADR-85's
  BACKLOG leg from advisory → hard, depends-on #170) should now be sequenced to make it *enforced*, not
  just practiced. See §3 Q7.
- **(D) PLAYBOOK Move 2 — maintainability, not parallelism (unchanged, still Council-bound).** The
  structural split → thin `§N`-index + per-section modules is justified on **maintainability** (the
  PLAYBOOK is ~3.5× the read-cap, frequently edited), **not** parallelism. Council-bound: the §1–§19 spine
  is the **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so the split must preserve §N
  addressability. See §3 Q5.

### A surfaced doc-vs-practice reconcile (do not lose)

- **§7 review-command canon — the graduated rule the prior supplement specified did NOT land.** The
  prior `…-architect-2` filled supplement (answer B) resolved the `/codex-review` vs `/code-review` drift
  to a **graduated rule**: interim / small → `/code-review high`; final pre-merge (3+ files) →
  `/codex-review` (independent GPT lens — confirm Codex auth mode first). **PLAYBOOK §7 still names a flat
  `/codex-review` for "3+ files / safety-critical"** (lines ~569, ~1651) — the graduated rule was never
  encoded. A `/review` vs `/codex review`-class doc-vs-practice drift — **surfaced for reconcile**, not
  silently resolved. (Also still live, flagged-not-fixed: `CLAUDE.md` §8 says "No repo-level skills
  directory exists yet" while `.claude/skills/verify/` + `.claude/skills/check-against-spec/` now exist —
  a doc-claim the coherence spine itself could eventually cover.)

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The live questions:

- **Q1 — name "file-oriented dependency management" as an ADR (the top candidate thread).** The prior
  supplement's explicit directive. Open: (i) author the **paradigm ADR** (decision + principles
  — coherence-by-mechanism; deterministic trigger + AI per-site verdict + human signature;
  graph-in-repo-not-model; narrow-first; the §16 do-not-build list as *part of* the doctrine — + the v1
  proof + the distilled roadmap); (ii) **which coherence-by-memory failure classes** the spine covers next
  and **in what order** (the supplement's priority sketch: more `reconciled_with` edges → graph-from-
  frontmatter / cross-repo → removal-via-transclusion → content-hash floor → undeclared-edge inference →
  intra-file + whole-graph sweeps). **Pointer for the *why*:**
  `docs/handoffs/2026-06-17-dev-knowledge-architect/SUPPLEMENT.md` (the verbatim answers) +
  `…-architect-2/SUPPLEMENT.md`.
- **Q2 — coherence v2 (the durable #179–#183 graph).** #181 (nudge-response: escape-hatch / deferred-hash
  / promote-nudge-to-gate) is **data-gated** on `logs/coherence-nudge.log` — read the log before deciding
  (the supplement's lean: *promote-to-gate if the nudge fires accurately + rarely; escape-hatch/deferred-hash
  only if noisy*). #180 (transclusion) is **gated on DEC-04** (lead-with-removal vs detection — unresolved).
  #182 (folder contracts) is gated on DEC-07. #183 (reparent #169/#171/#166) is **evidence-gated** (≥2 real
  drifts + a #169-fit decision — a deliberate gate, *not* an oversight; do not reparent yet).
- **Q3 — §7 review-command graduated rule (a doc-vs-practice reconcile, not yet a tracked task).** Encode
  the supplement's graduated rule in PLAYBOOK §7 (interim → `/code-review high`; final pre-merge 3+ files →
  `/codex-review`); confirm Codex auth mode first (ChatGPT-authed = no extra cost; API-key = bills per
  token → flip toward `/code-review` or switch auth). Surfaced in §2; not yet a `#id`.
- **Q4 — ADR-87 demonstration + the GAP-2 guard.** **#184** (demonstrate the equilibrium contract on a
  real build — the empirical close, OPEN) and **#185** (the GAP-2 deterministic gotcha-injection PreToolUse
  guard — filed, not built). Open: whether #185 is genuinely needed once #184 exercises the contract, or
  whether the prompt contract subsumes it.
- **Q5 — PLAYBOOK Move 2 (Council-bound, unchanged).** Structural split → thin `§N`-index + per-section
  modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N addressability — the consumer
  API). Maintainability-justified, not urgent. **Unblocks #39; decouples #18 / #67 / #77 / #146** (the
  playbook serialize-group).
- **Q6 — handoff-machinery residue.** **#164** (implement the v5 generator — replace the SUPERSEDED v4
  8-file mechanics still in `.claude/commands/handoff.md`; must emit the v5.2 **always-file** `SUPPLEMENT.md`
  + seed each repo's `docs/handoffs/README.md` runbook; **ADR-83 LIVE constraint must survive** — v4
  templates stay live for corp-monorepo until the v5 cross-repo generator lands). **#159** (the *incoming*
  §13(d) beat — its only-remaining clause; the fill→fold half is dogfooded). **#162** (architect actor-vs-mode
  vocab — disambiguate atomically, do not leave the collision live). **#161** (stable probe-core + the
  orientation probe — *capture-only*; **note this bundle is again a hand-assembled probe set**, the
  persisting capture point).
- **Q7 — the ADR-85 enforcement chains + the load-bearing-backlog escalation.** **#170 → #168** the
  traceability spine (issue-ID↔commit anchor — the always-warranted link that promotes ADR-85's BACKLOG
  leg from advisory to a **hard** gate). **#171 → #169** the conformance dashboard (`ecosystem/conformance.md`,
  ADR-86 — now unblocked by the locked `Finding` format). *Connection to Q1:* the coherence `reconciled_with`
  edge model is a **sibling** of the traceability edge — whether #170 reuses it is an open design link.
- **Q8 — ADR-85 standing governance obligation (a watch, not a design question).** The gate is **live**. A
  **4-week scope-freeze runs to ~2026-07-14**; watch `logs/OVERRIDES.md` for override-rate (**>~10% → tune
  the rules**). Surfaced so the next session doesn't re-open ADR-85's shape mid-freeze.
- **Q9 — #186, sync #156 task-graph checks into the distributed plugin floor.** The hub's `validate_backlog.py`
  carries the #156 depends-on reference-existence + no-cycle checks; the **distributed plugin floor**
  (`plugins/tier1-lifecycle/scripts/validate_backlog.py`) carries only the ADR-66 structural checks, so a
  child's installed `validate-backlog` hook would NOT catch a dangling edge / cycle. The #120 probe is
  **floor-faithful** (mirrors the floor as-shipped, deliberately does not compensate), so the gap is tracked
  here — do **before/with** distributing `validate-backlog` to children.

**Resolved this window (do NOT re-open):** #172's v2 roadmap **extracted** (→ #179–#183) + #172 **closed** ·
the equilibrium-contract **codification** (→ ADR-87 STEP 3; only the *demonstration* #184 remains) · #167
multi-serialize-group schema (→ closed) · #120 child-BACKLOG conformance probe (→ closed) · #138 floor
INSTALL_NOTE gitignore-negation (→ closed) · the worktree/parallel-arc lifecycle (→ codified in PLAYBOOK,
native auto-seed verified).

---

## 4. The task-graph (durable hard edges — #156 shipped)

#156 shipped — **hard edges are DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. Point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b).

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** **11 serialize-groups**
  at generation. The **handoff** group = `{#1, #26, #159, #161, #162, #184, #164, #10}` (**#184 added** this
  window — the equilibrium-demo). The **coherence** group = `{#179, #180, #181, #182}` — **NEW this window**
  (the extracted #172 v2 roadmap; #183 is bare). The **audit-py** group = `{#153, #7, #36, #95, #140, #139,
  #166}` (**#172 removed** — closed this window). The **playbook** group = `{#146, #77, #67, #18, #39}`. The
  **architecture** group = `{#165, #35}`. (Plus `claude-md {#112,#157}`, `claude-md-template {#17,#109}`,
  `environment {#71,#119}`, `pre-commit-config {#15,#132}`, `settings-json {#116,#117}`, `validate-backlog
  {#187}` — see the validator's full summary line.) Hard precedence edges (`depends-on`): **#168 → #170**,
  **#169 → #171**. Parallel-safety is **derived** (no shared group + no `depends-on` path).
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q1 (name the paradigm ADR) is the top candidate thread** — but it is *not* a schema edge: #179–#183
    are durably grouped, the **capstone ADR is the soft "frame" they hang off**, carried here as judgment.
  - **#181 (Q2) is the data-gated one** — not schedulable until `logs/coherence-nudge.log` has firing signal.
  - **#184 (Q4) is the ADR-87 empirical close** — serializes within the `handoff` group; closes on the next
    real build that exercises the contract.
  - **#164 (Q6) is the last big handoff-machinery item** — serializes within the `handoff` group; must emit
    the v5.2 always-file `SUPPLEMENT.md`.
  - **#170 (Q7) unblocks #168**; the coherence `reconciled_with` edge is a *sibling* of the traceability
    edge — a possible reuse, surfaced as a design connection, not a schema fact.
  - **Move 2 (Q5) unblocks #39** and **decouples #18 / #67 / #77 / #146** — landing it dissolves the playbook
    serialize-group.
  - **#186 (Q9) is independent** — sync the #156 checks into the plugin floor before distributing.

(The "candidate-thread / unblocks / sibling" framing is residual judgment; the serialize-group +
`depends-on` edges are the schema fact. #156 made the *hard* edges durable, not these *soft* ones.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` themes — the coherence work is now its own `coherence` group
  (#179–#183) + #183 bare; the handoff group (#159/#161/#162/#164/#184); the audit-py group (#166/#139 +
  the closed-out #172 gone); the playbook group (Move 2 / #39); the floor/distribution items (#186). Do
  **not** trust any re-narrated ID text — open the live BACKLOG (the §2/§3 text is recall; the file is
  truth). `validate_backlog`: **83 tasks, 0 warnings, 7 themes, 20 stories, 11 serialize-groups** at
  generation.
- **Live branches at generation** (`git branch -v`): `main` (**in sync** with origin at generation; this
  handoff's own commits put it ahead until pushed); `automation/fleet-audit` (**never merges to main by
  design — ADR-84**, NOT a loose end). **No merged stragglers** — the prior bundle's two were `-d`'d. This
  handoff's own branch `docs/handoff-2026-06-18-architect` merges on completion.
- **Drift-flags:** **one actionable** — `pytest_collected@ARCHITECTURE.md` doc=587 vs live=614 (re-drifted,
  fix owed — §1) — plus the **carried-benign** `git_backlog_drift` #90a `[~~]` (#77). `main` in sync; no
  stragglers. Re-derive: `python scripts/audit.py health` + `python scripts/validate_doc_claims.py` +
  `git status -sb` + `git branch --merged main`.
- **Audit-gating note (load-bearing):** `audit.py` check #19 `handoff_probes` validates the
  **lexically-max** v5 bundle. `2026-06-18-dev-knowledge-architect` is now lexically-max → it **is** this
  check's target (superseding `…-architect-2`). Its 10 probes were verified to bind via
  `python scripts/verify_handoff_probes.py docs/handoffs/2026-06-18-dev-knowledge-architect`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **`pytest_collected` fix owed** — the headline (§1): re-read `ARCHITECTURE.md` → bump 587→614 →
  re-stamp `last_reviewed`. A next-session doc-coherence fix (not this handoff's, per §1).
- **17 closure proposals** await — `/review-closures` (human-gated, done-items-leave). Re-verify the
  STRONG candidates' evidence SHAs before closing (#5/#77 are the known false-positive/voided pair).
- **changelog drift** — `claude-code 2.1.181 > last reviewed 2.1.177` — `/changelog-review`.
- **nightly may have silently skipped** — the SessionStart reminder flagged the expected
  `docs/audits/2026-06-18-conformance-nightly-digest.md` is **NOT** on the `automation/conformance-digest`
  branch (no retry). Worth a look — not a handoff artifact.
- **10 nightly triage findings** await (#37, #35, #33, #31, #29, #27, #25, #23, #21, #19 — Issues tab).
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **`main` will be ahead of origin after this handoff's commits** — push is the operator's call (the
  serial-push gate). At generation `main` was in sync.
- **ADR-85 override-rate watch** — `logs/OVERRIDES.md`; scope-freeze to ~2026-07-14 (§3 Q8).
