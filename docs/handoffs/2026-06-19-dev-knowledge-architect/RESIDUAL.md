# Residual — 2026-06-19 architect handoff (the part the repo does not already encode)

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to BACKLOG, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," the
> task-state points at the whole BACKLOG / relevant themes, and the open architecture questions
> travel as residual so the next session resumes the design rather than rediscovering it.
>
> **⚠ UPDATE — supplement FILLED (warm).** Generated cold (reconstructed from JOURNAL + live git in
> a fresh `/clear`ed session, not witnessed-live; the drift-checks below were run **live** at
> generation), but the operator then `supplement filled` real architect answers — see **§2**, now the
> authoritative strategic *why*. The §13(d) beat **narrows**. Read any "COLD / empty ANSWERS / beat
> fires full" phrasing below as **generation-time history**.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py health` / `ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation. **Re-derive each at read-time** — the
teeth are in `PROBES.md`, not in trusting these lines.

### ⚠ HEADLINE — `ship-gate` is RED: two wrap commits landed direct-on-`main` (undispositioned)

`python scripts/audit.py ship-gate` → **RED — 2 new/undispositioned WARN(s)**, both `no_ff_merges`:

- `3a894ee` (2026-06-19) `docs(journal): 2026-06-19 session-wrap — anchor d0f9ead (transcript archive)`
- `d0f9ead` (2026-06-19) `chore(transcripts): archive 2 deep-research reports (dependency-detection + doc<->code traceability)`

Both are **non-merge commits on `main`** (FF/direct), violating **core-invariant #5** (every
change — including one-line doc edits — goes branch → merge `--no-ff`; never direct to `main`).
They are the 2026-06-19 **session-wrap** commits: the wrap journal entry + the transcript archive
were committed straight onto `main` instead of via a branch + `--no-ff` merge. The session-wrap
JOURNAL entry records the work but **does not note** that these two went direct.

**Why this is a next-session decision, not fixed here:**
- They are **already pushed** — `main` was in sync with `origin/main` (0 ahead / 0 behind) at
  generation. Un-FF'ing them means a published-history rewrite — **off the table** (P0: no
  destructive history ops without explicit operator approval).
- So the resolution is a **judgment call the architect/operator must make**, not a mechanical fix:
  **(option A)** add a `disposition-register.yaml` entry classing direct-on-`main` *journal/chore
  wrap* commits as accepted (and decide whether to carve that pattern in generally — risky, it
  weakens core-invariant #5), **or (option B)** operator-accept the RED as a one-off slip and let
  it age out of the `no_ff_merges` window, **or (option C)** tighten the wrap workflow so even the
  journal-wrap goes through a branch (the real prevention). **This handoff surfaces it; it does not
  pick.** (Memory: *don't self-declare operator verdicts*; *state honest enforcement limits*.)
- **Process note for THIS handoff:** its own commits go on `docs/handoff-2026-06-19-architect` and
  merge `--no-ff`, so the handoff does **not** add to the `no_ff` drift. After the handoff merge,
  `ship-gate` will **still** be RED (the two pre-existing wrap commits remain) — that is expected;
  `PROBES.md` P7 binds to it.

### Other flags (benign / dispositioned)

- **`#77` closed-but-present** `[~~]` — `validate_git_backlog` flags `#77` (closes in `77e5d7df9`)
  still in `BACKLOG.md`. **Dispositioned** (`warn-77-voided-closure`) — a known voided/misattributed
  closure, carried benign. (Memory: *re-verify STRONG closure content* — `#77`/`#5` are the standing
  false-positive STRONG hits; do **not** close them on a tag match.)
- **5 `doc_rot` history-accretion WARNs** `[~~]` — BACKLOG `#164`/`#77`/`#134`/`#10` + CLAUDE.md
  `§section-history` (21 entries). All **grandfathered** (ref `#140`) when the `doc_rot` gate landed
  this window — the arc introduced the *detector*, not the debt; new accretion still blocks.

### ✅ Cleared since the last bundle — `pytest_collected` re-drift is FIXED

The 2026-06-18 bundle headlined `pytest_collected@ARCHITECTURE.md` doc=587 vs live=614. The
2026-06-19 **consolidation** session bumped `ARCHITECTURE.md` to the integrated live count on a
genuine end-to-end re-read. `validate_doc_claims` now reads **OK — 4 claims match**
(`pytest_collected` doc **667** / actual **667**; `audit_check_count` 21/21; hook count 9/9; hook
roster matches). `PROBES.md` P6 is therefore **expected to MATCH** this time — but the pass
criterion is still "answered from the live source," never "matches a remembered number."

---

## §2 — Supplement status (FILLED — warm) — the authoritative strategic *why*

`SUPPLEMENT.md` was generated cold (empty ANSWERS, committed) and then **FILLED** post-generation
with **real outgoing-architect answers**. `scripts/assemble_paste.py` folds the **ANSWERS region
only** into `PASTE_THIS.md` (answers-only — no QUESTIONS leakage); the incoming **§13(d) beat
narrows** to "anything changed since the supplement was written?". **Read the folded `SUPPLEMENT.md`
ANSWERS in full — they are the design authority for the next session.** The headline, surfaced (not
buried):

- **The through-line — everything this session did was ONE thing: grounding ADR-88 (file-oriented
  dependency management) in reality.** Model: *markdown files are objects; their references
  (commands / ADRs / §-sections / files) are edges; the repo is a graph; a retired target leaves a
  **dangling edge** read as if live — that is the rot.* The repo has a dangling-edge detector for
  **one** node type (the #156/#179 BACKLOG task-graph) and **none for prose**.
- **Strategic intent:** turn ADR-88 from *Proposed-and-partially-detected* into an **enforced
  lifecycle organ for the whole repo** — three organs: **(1) referential-currency detector** (does
  every edge resolve?), **(2) structural linter** (graph shape — numbering / headers / ToC, the
  things the architect *provably cannot eyeball* — proven 2/2 false this session), **(3)
  "earns-its-keep" check** (does each node — file, automation, branch, folder — still justify
  existing?). The two deterministic triggers already shipped this window are FC3 dedup (#187) + FC4
  history-accretion (#140); the **structural + lifecycle halves remain unbuilt**.
- **Sequence (locked):** prove-the-problem (this session's audit + manual groom = the *prototype*) →
  **design the mechanism** (a **debate running in another chat** — the next session's primary design
  input + design authority) → build + enforce → **then** deploy methodology (**#131**). The organ
  must exist **before** #131 — you cannot deploy onto a base that silently rots.
- **The two CC-observed addenda, answered:** **(A)** ratify ADR-88 via a **Council-equivalent
  deliberation first** (the running debate may serve), *before* the build — it is foundational
  doctrine, not the ADR-82/#149 narrow-operator-ratify class; it gates whether #179–#183 + the
  shipped detectors are *doctrine* vs *proposal*. **(B)** ship-gate RED → **(B) operator-accept the
  one-off + (C) tighten the wrap workflow so even a journal-wrap branches; reject (A)** —
  dispositioning direct-wraps away erodes core-invariant #5 (the genuine fork is acknowledged, but
  the architect's call is *tighten, don't disposition*).
- **Do NOT redo** (per the answers): the confirm-live ledger, the committed currency audit, the
  note-vs-usable distinction, the *structural-claims-need-a-live-organ* lesson, or the groom itself —
  and **do not re-audit PLAYBOOK/ESSENTIALS by hand**; build the organ so hand-auditing is never
  needed again.

**Prior-window context (still relevant, not superseded):** the **2026-06-18 filled supplement**
(`docs/handoffs/2026-06-18-dev-knowledge-architect/SUPPLEMENT.md`) — *unify + encapsulate into ONE
self-enforcing deployable whole, #131 as the first deployment test, enforcement > documentation*.
This window's answers **sharpen** that into its first concrete dependency: the lifecycle organ for
ADR-88 must exist before #131.

---

## §3 — Planning *why*: the 2026-06-19 window arc (what the design did and why)

The window executed the **"machinery not memory" closures** the 2026-06-18 supplement named as the
unify-goal's dependency — the enforcement gaps that let the methodology be bypassed:

1. **Phase-1 "seal" — three worktree tracks integrated `--no-ff`, then closed via `/review-closures`.**
   - **seal-hooks (`442c994`)** — **#188** hook-completeness audit [left OPEN per operator] (no
     uncovered zones; the live finding = the P0 `block-onedrive` guard sees only the shell command
     string, not `Edit`/`Write` `file_path` → **#191** filed as the `file_path` PreToolUse guard);
     the **C1** fix in `session_end_backpressure.py` (the JOURNAL SHA-anchor was computed at the
     *push* boundary, so deferred-serial-push let one prior citation vaccinate a multi-session arc —
     narrowed to the **session** boundary, `--first-parent`); **ADR-85 amendment** records the
     per-session-anchor semantics.
   - **seal-dedup (`dd025c3`)** — **#187** deterministic near-duplicate-title WARN on the hub
     `validate_backlog.py` (token-overlap, explicit stated limit, never a hard-fail); **#186**
     floor-sync of the **#156** task-graph checks (`depends-on` reference-existence + no-cycle)
     **verbatim** into the plugin floor, with an ADR-78 carrier-doctrine twin-marker.
   - **grooming (`e48da28`)** — **#140** `doc_rot` grooming-gate: new `scripts/validate_doc_rot.py`
     + `audit.py check_doc_rot` (`ALL_CHECKS` 20→**21**), the **Layer-2 deterministic trigger for
     ADR-88 FC4** (history-accretion bloat). DETECT-only / condense-preserving; 5 pre-existing loci
     grandfathered (teeth verified RED→GREEN).
2. **ADR-88 *file-oriented dependency management* authored (`7e6f996`, Proposed).** The capstone the
   2026-06-18 supplement directed ("name the paradigm as an ADR, not a VISION"). It names markdown-
   as-a-design-pattern and the failure classes the paradigm addresses; `#140` is its FC4 trigger,
   already shipped. **Status: Proposed — unratified** (open question §4).
3. **Consolidation doc-currency seal.** `DEFINITION_OF_DONE` JOURNAL-gate boundary rewritten
   **push→session** (the C1 amendment); **ESSENTIALS** brought under the canonical freshness gate
   (`audit.py` check #10 / `_FRESHNESS_FILES`) with the coherent four→five ripple; a sealed
   sealed/open/sequenced **state report** (`docs/audits/2026-06-19-consolidation-state-report.md` —
   the **text precursor to the visual workflow/dependency dashboard**). The session **refuted its
   own central hypothesis** ("PLAYBOOK prompt-format lags ADR-87" — PLAYBOOK §2 already carried the
   ADR-87 contract verbatim), so the real laggard was `DEFINITION_OF_DONE`.
4. **Currency groom + session-wrap.** PLAYBOOK/ESSENTIALS reconciled against live state (purged the
   archived `/boot`,`/evolve` from usable positions → one consolidated retired-machinery note; fixed
   two off-by-one §-cross-refs; tagged the ADR-87 split in the prompt skeletons). Wrap: pushed
   `main`, deleted 9 merged branches + 3 seal worktrees (no-loss verified), archived 2 deep-research
   transcripts (dependency-detection + doc↔code-traceability — these **feed** the doc-lifecycle /
   dependency Council arc). **← This wrap is where the §1 direct-on-`main` slip happened.**

**The through-line:** every track this window was an *enforcement* move (a gate, an anchor fix, a
detector, a floor-sync) — exactly the "machinery not memory" the unify-goal depends on. The capstone
doctrine (ADR-88) now exists to name *why* they cohere. What is **not** yet done is the unification
itself — composing these into ONE articulable, deployable whole and proving it on **#131**.

---

## §4 — Open architecture questions (travel as residual — resume the design, don't rediscover it)

> **Reframed by the FILLED supplement (§2).** The **top thread is now the ADR-88 lifecycle-organ
> design** — taken from a **debate running in another chat** (the design authority; the next session's
> first move is to incorporate its output, **not** a re-audit). Q1 and Q4 below now carry an architect
> **lean** from the answers (still open = *decide/execute*, not *rediscover*). The 2026-06-18 "#184
> first" sequencing is **subordinated** to "the lifecycle organ exists before #131."

0. **The lifecycle-organ mechanism (NEW top thread).** Design + build the three organs (§2:
   referential-currency detector · structural linter · earns-its-keep check). Primary input = the
   running mechanism debate. Open *inside* it: how does the detector mechanically tell a *note* from a
   *usable* dead-ref (the note-vs-usable distinction is load-bearing — ~18 `CHANGELOG retired` notes
   are keep, not purge)? How does the linter cope with a two-documents-glued file (the PLAYBOOK
   one-doc-or-two question)? Does the organ start prose-only or span all node types (files / automation
   / branches / folders)?
1. **ADR-88 ratification path** *(lean in §2: Council-equivalent first, before the build)*. ADR-88 is
   **Proposed**. The answer leans **ratify via a Council-equivalent deliberation** (the running debate
   may serve) **before** the build, since it is foundational doctrine (not the ADR-82/#149
   narrow-operator-ratify class); it gates whether `#179–#183` + the shipped detectors are *doctrine*
   vs *proposal*. **Decide + execute.**
2. **The unify + encapsulate goal — sequence it.** The strategic spine (§2) is still unbuilt as a
   *whole*. With the enforcement gaps now closed (#140/#187/#186/#191) and the capstone authored,
   what is the **decomposition** of "ONE self-enforcing deployable whole → test on #131"? The
   2026-06-18 supplement's sequencing held **#184 first** (demonstrate ADR-87, riding #131's
   onboarding as the real build). Re-confirm or re-decide.
3. **§7 graduated review-command rule — still not landed.** The 2026-06-18 supplement specified
   interim → `/code-review high`; final pre-merge (3+ files) → `/codex-review`, with Codex auth =
   ChatGPT-authed default (no per-token billing). **Not encoded in PLAYBOOK §7.** A small encoding
   that "rides along" — but still open.
4. **The §1 `ship-gate` RED disposition** *(lean in §2: B + C, reject A)*. The answer leans
   **(B) operator-accept the already-pushed one-off + (C) tighten the wrap workflow so even a
   journal-wrap branches**, and **reject (A)** (dispositioning direct-wraps away erodes core-invariant
   #5 — "the ship-gate going RED is the system correctly flagging the erosion; honor it by tightening,
   not by dispositioning it away"). The genuine fork is acknowledged (A is defensible if a journal-only
   wrap is judged low-risk-enough to exempt). **Operator decision + execute.**
5. **Standing design threads (unchanged from the prior bundle, still open):** **#181** coherence-v2
   (data-gated on `logs/coherence-nudge.log` accumulating signal); **#164** the v5 cross-repo handoff
   generator (+ the deferred `verify_handoff_probes.py` teeth validator); **#162** architect
   actor-vs-mode vocab; **#161** the teeth probe-core; the **#170→#168** / **#171→#169** ADR-85
   chains; the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14 — is the session-end gate
   over-firing?).

---

## §5 — Task-state (pointer, not narration — v5 §6)

- **The BACKLOG is the spec; items are tickets.** Read `BACKLOG.md` directly. Live shape:
  `validate_backlog: OK — 7 themes, 20 stories, 82 tasks, 0 warnings`. Themes: Big picture · Handoff
  continuity · Enforced governance · Lessons feedback loop · Decision management · Canonical-file
  integrity · Cross-repo universalization · Tooling & evaluation.
- **Serialize-groups (#156 durable task-graph — live):** 10 groups. The **handoff** group =
  `#1, #26, #159, #161, #162, #184, #164, #10`; the **coherence** group = `#179, #180, #181, #182`.
  *(These are live schema facts that drift on any BACKLOG edit — `PROBES.md` P9 re-derives them; do
  not trust this line.)* The soft/provenance graph beyond the hard `depends-on` edges stays residual
  prose (ADR-66 amendment: `depends-on` is hard-blocked-by only).
- **Closures pending:** the SessionStart surfaced **16 closure proposals** — `/review-closures` is a
  separate human-gated loop, **not** this handoff's job. Standing false-positive STRONG hits to
  exclude: `#5` / `#77`.
- **Branches:** `main` + `automation/fleet-audit` (KEPT — by-design ADR-84 writer-isolation infra,
  not a straggler). No merged stragglers at generation. This handoff adds
  `docs/handoff-2026-06-19-architect` (merges `--no-ff`, then deletable).
- **Drift-flag (task-state):** the only `validate_git_backlog` flag is the dispositioned `#77` (§1).
