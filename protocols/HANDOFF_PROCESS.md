# HANDOFF_PROCESS v5
<!-- scope: meta -->

Version: 5.7
Status: stable
Effective: 2026-06-11 (canonical)
Decision: ADR-82 (operator-ratified 2026-06-11; Council gate waived by operator authority per #149)
Supersedes: HANDOFF_PROCESS v4.4 (archived at `protocols/archive/HANDOFF_PROCESS_v4.4.md`),
and the heavy-bundle delivery ADR-79 mandated.
Authority: this protocol is the single canonical source of truth for handoff mechanics.

> **Why a rewrite.** v4 treats a handoff as onboarding a new chat with a heavy 8-file
> teaching bundle pasted into a browser. The 2026-06-10 lesson named the load-bearing
> failure: a handoff that *points* at the methodology but does not *force* the receiver to
> open it lets the new session work from the lossy in-context **compaction summary** (a
> SECONDARY source) instead of the files on disk (the PRIMARY source). v4's comprehension
> questions are answerable from the bundle itself, so the forced-read is vacuous —
> "fake-green, like a test that passes without the behavior." v5 inverts the model:
> **CC owns the handoff, the browser is a thin reactive partner, and the forced read has
> teeth.**

---

## 1. The model (model C)

CC (Claude Code, Layer-3, has file access) **owns and initiates** the handoff. The browser
(Layer-1 architect, **no** file access) is a thin reactive partner — "critical architect;
CC is your junior." The three-layer invariants (ADR-28) are unchanged; what changes is *who
initiates*, since CC is the only actor holding live repo state.

| Actor | In v5 |
|---|---|
| **CC** (Layer 3) | Stateful executor. Generates the handoff from inside the repo; runs the drift-checks + state read; runs the teeth-y forced read; verifies **state fidelity**. |
| **Browser** (Layer 1) | Thin reactive architect. Boots from `HANDOFF_BOOT.md`; verifies the **artifact**; filters CC output to the operator; research; exception-handler; launch-config for genuine forks. |
| **Operator** | Relays between CC and the browser; makes the calls the browser surfaces; runs the promotion gate. |

---

## 2. What CC emits — the residual (not a re-transmission)

CC's handoff is **only the residual** — what the repo does not already encode:

1. **Un-committed session reasoning** — the lived "why" that is not in git, JOURNAL, or BACKLOG.
2. **Pointers (paths)** — where the next session reads, not copies of what's there.
3. **Drift-flags — the headline.** Where reality and the written record disagree, surfaced
   first, not buried. Produced by the read-only drift-checks (`validate_doc_claims` #89,
   `validate_git_backlog` #90) plus CC's state read.

It does **not** re-transmit methodology or state the repo already encodes. Methodology is a
*pointer* + mechanical enforcement (§3); task-state is a *pointer* to the BACKLOG (§6).
Re-narration is the v4 disease (it drifts from its source — the proven `/review` vs
`/codex review` drift class); v5 removes it.

The residual is written to `docs/handoffs/<slug>/` as CC's handoff artifact (lean — the
residual + the probe manifest + the drift-flag table, not an 8-file bundle).

---

## 3. Methodology is enforced mechanically, referenced thinly

The methodology is **not re-stated as prose per session.** It lives in the repo
(`PLAYBOOK`, `ESSENTIALS`, `CLAUDE.md`, the ADRs) and is enforced mechanically: pre-commit
gates, `audit.py` checks, hooks, skills. The handoff carries **pointers** to it and relies
on the **forced read** (§5) to make the receiver actually open the primary source. Heavy
*enforcement*, thin *prose*.

---

## 4. The thin browser boot

A fresh browser chat boots from **`protocols/HANDOFF_BOOT.md`** — a ~3-line core (identity /
one meta-rule / first-move) that replaces the heavy multi-file bundle. Everything else is
pulled just-in-time via CC.

**Browser-role delivery (load-bearing).** The browser's operating role (§7) is **resident in
the boot file**, not left only in this spec (which CC holds and the browser never sees). If
the role lived only here, the browser — booting from 3 lines + CC's per-session handoff —
would never learn it, and the role would silently not happen. The boot carries it directly;
alternatively CC serves it on the browser's first move. Either way the role **must reach the
browser** — never assume a CC-held file transmits to a file-less actor.

The boot ends with an on-load acknowledgment line so a partial/missing paste is visible
(the ADR-79 visible-paste idea).

---

## 5. The teeth-y forced primary-source read (#148 a)
<!-- rule: handoff-probes-bind -->

The forced read has **teeth** when its verification **cannot be answered from the compaction
summary** — the answer exists only in the live primary file/state at answer-time. A probe is
teeth-bearing when all three hold:

1. **Live-only answer** — volatile or high-entropy (a count that drifts, a sha, an exact
   line) that a summary rounds off or omits.
2. **Generator-excluded** — the handoff ships the **question + source-locator + the exact
   verification command**, and **never the answer**. (A probe that bakes its answer in is, by
   construction, bluffable — and is rejected.)
3. **CC-checkable** — CC re-derives the ground truth read-only from disk/git at check-time
   and compares, exactly as the existing validators do.

### Probe manifest (reuses the existing read-only validators)

| Probe | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|
| **Live check count** | `ALL_CHECKS` in `scripts/audit.py` | the count drifts every time a check lands; a hardcoded number goes stale | `python scripts/audit.py checks` (count + last name) |
| **Exact-line quote** | a named `PLAYBOOK`/`ESSENTIALS`/spec section | a paraphrase from a summary is not byte-identical | read the live section; the quote must be a substring |
| **Live HEAD / tree** | live git | the summary holds the *generation-time* sha; new commits move HEAD | `git rev-parse --short HEAD` + `git status` |
| **Ship-gate read-back** | `audit.py ship-gate` ∩ `ecosystem/disposition-register.yaml` | the GREEN/RED verdict, the dispositioned-WARN **count**, and any `[stale]` line are computed at answer-time over live git ∩ `main`-history; a new direct-on-`main` commit re-REDs it — the values are absent from the bundle, so do **not** trust the residual's headline. Folds the former **drift-flag set** + **freshness witness** probes: `git_backlog_drift` and `canonical_freshness` are both `ALL_CHECKS` members, so running the gate re-derives them and prints their evidence inline | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) |
| **Pointer round-trip** | the live `PLAYBOOK` section a pointer names | re-narration is outlawed (§2/§3); the answer exists only by opening it | read the live section; compare |

### Who runs it (the file-access reality)

The browser has **no file access**, so the teeth are enforced at the **CC ↔ primary-source**
boundary. CC ships the probe manifest in the handoff (questions + locators + commands, no
answers). The browser, lacking files, **must respond "run `<command>`"** for any live probe —
which *surfaces* the off-bundle dependency rather than hiding it. CC runs each verification
command against **live state at check-time**, re-derives ground truth, and emits PASS/FAIL.
**Any FAIL blocks onboarding** (the escalation ladder, §10). The reconciliation in one line:
"force the receiver to open the primary source" becomes "**force CC to re-derive every
load-bearing fact from the live primary source at check-time, and block onboarding on any
mismatch.**"

### Empirical proof is a promotion gate (operator ruling)

That the teeth *bite* is proven empirically, not by review: at promotion, dogfood one real v5
handoff and attempt to answer each probe **from the compaction summary alone** — every probe
**must fail** to be bluffed. A probe answerable from the summary is removed or hardened. The
flip gate tests that the teeth force a primary-source read, not merely that the spec reads
well (§11).

### Structural enforcement — anti-bluff by construction (v5.4; RF-1 option b)

Item 2's "never the answer" contract is **machine-held, not hand-discipline** (landed
`9d5ebe5`, 2026-07-04, after the 06-20..07-03 `expected:`-hint erosion showed hand-copy
alone regresses):

- **Answer-hint FAIL rung** — `scripts/verify_handoff_probes.py` FAILs any probe **row**
  carrying an `expected[ :]`-form answer hint (row-scoped, so historical bundles stay judged
  by their own era; the deployed `handoff_probes` check reads the latest bundle and gates
  `/ship`).
- **Answer-free by construction** — `scripts/gen_handoff.py` never hands the render
  functions the generation-time hint VALUES (HEAD / check counts / ship-gate verdict /
  backlog counts); those are diverted to a **stdout JOURNAL-draft** for the wrap entry —
  never into a browser-visible bundle file, never auto-appended.
- The empirical dogfood above therefore re-runs **structurally on every bundle** via the
  gate, not once at promotion.

---

## 6. Lean task-state — pointer, not narration (#148 b)

The **BACKLOG is the spec; items are tickets** (Pocock). The handoff **points** to it — it
does not re-narrate IDs. Task-state in the residual is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** the `validate_git_backlog`
check raises (e.g. a `closes [#id]` still open). Re-narrating item text splits the truth and
drifts; the pointer + the drift-flag is the whole task-state.

Pointer integrity depends on the primary source being **fresh** — `canonical_freshness` /
`doc_claims` / #145 guard that. A stale primary source makes a faithful pointer point at a
lie; the drift-flags surface exactly that.

---

## 7. Browser role + plan-review output contract (#148 model C item 4)

The browser's operating role (delivered via the boot, §4):

- **Reactive partner + filter** — surface only errors and decisions needing human judgment;
  keep the operator at feature / epic / user-story level; absorb routine CC output.
- **Research** — open-web / cross-domain research CC can't reach; synthesized, not raw.
- **Exception-handler** — adjudicate what the methodology doesn't cover, or escalate with a
  recommendation (not a menu).
- **Launch-config support — genuine forks only.** Help choose model / effort / autonomy only
  for real forks; routine is CC's own `opusplan` + auto mode. The browser does **not** review
  routine plans — only architecturally risky ones.

**Plan-review output contract (non-negotiable).** When the browser reviews a CC plan it emits
**exactly one** of — never prose the operator must translate into CC actions:

1. the **exact CC option to select** (e.g. `Select option 2` / the verbatim answer to CC's
   question);
2. **exact paste-ready English feedback** (the verbatim text the operator pastes into CC);
3. a plain **`approve`**.

---

## 8. Verification split

- **Browser verifies the *artifact*** — file-free, fresh-eyes: is CC's handoff internally
  coherent and aligned with the architectural intent? This includes the **self-consistency**
  check (2026-06-10 lesson): scan for two load-bearing claims that **cannot both be acted
  on** (a recency-peak self-contradiction that drift-checks and structural lints both pass,
  because they check each claim against state, never against each other).
- **CC verifies *state fidelity*** — claims vs live disk/git: it runs the drift-checks and the
  teeth-y forced read (§5). Each actor checks what it is positioned to check.

---

## 9. Adjudication is bidirectional

The browser **corrects CC's errors AND pulls missing context** — not one-shot. If the
handoff omits something the browser needs, it asks CC to pull the primary source (CC can; the
browser can't). If CC's read of state looks wrong, the browser pushes back and CC re-derives
from disk. The handoff is a back-and-forth, not a one-way transfer (the PLAYBOOK "handoff is
back-and-forth" rule, generalized).

---

## 10. Self-updating `/handoff` + failure handling (#148 c)

`/handoff` is **self-updating**: it pulls the **current** process + methodology **pointers**
live at handoff time and carries **no hand-copied** process or methodology. The version/status
it stamps is read from the live spec header, never hardcoded; the methodology it references is
a pointer, never a copy. (Command wiring: `.claude/commands/handoff.md`.)

**Failure handling — degrade loudly.** A probe that can't be answered → **FAIL**, routed
through the escalation ladder (re-read the named primary source → CC verifies the fact →
ABORT onboarding). A moved anchor (source reworded) → WARN `anchor-missing`, re-anchor — never
a synthesized pass. An infra hiccup (git absent) → reported as *skipped* (degraded coverage
visible), never silently counted as pass. Silent truncation or fabrication is the failure mode
to avoid: degrade loudly.

---

## 11. Promotion record (v5 → canonical, 2026-06-11)

v5 was promoted from beta to **canonical in a single atomic flip** on 2026-06-11 (#149). It
had shipped beta in parallel while v4.4 stayed canonical; the flip retired that parallel-ship
period. Promotion was gated on:

1. **ADR-82 ratification** — the AI Council gate was **waived by operator authority** (#149):
   the operator ruled v5 ready; ADR-82 stands operator-ratified pending any later Council note.
2. **One fresh-eyes review** meeting the beta→stable criterion (v4.3.1 §B: Stage-1 **<2
   critical findings** AND a Stage-3 verdict of **PROMOTE / PROMOTE-WITH-CAVEATS**, reviewer
   judgment overriding count);
3. **The empirical teeth dogfood** (§5): one real v5 handoff where every forced-read probe
   **failed** to be answered from the compaction summary alone.

The flip moved the canonical `Version:` and its four coupled surfaces together —
`CLAUDE.md`, `.claude/commands/handoff.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md` — which
`audit.py`'s coupling gates (`check_amendment_coherence`, `check_handoff_version_stamp`) force
to be **atomic**. The flip: renamed this file to `protocols/HANDOFF_PROCESS.md`
(`Version: 5.0`, `Status: stable`); archived v4.4 to `protocols/archive/HANDOFF_PROCESS_v4.4.md`;
kept `templates/handoff/**` LIVE as the v5 template set (this record previously claimed these were archived to `templates/archive/handoff-v4/` — corrected 2026-06-26: that directory never existed and the folder set is live, read by the v5 `/handoff` command; the superseded flat v3/v4 single-file templates `templates/HANDOFF_*.md` were the ones archived, to `templates/archive/` on 2026-06-26); scoped audit checks
#8/#9 to historical v4 bundles; closed #148 / #124 / #25. The bespoke read-only teeth
validator (`scripts/verify_handoff_probes.py`) was deferred to a post-flip ticket; it has
since **landed (#163)** and gates `/ship` — registered in `audit.py`'s `ALL_CHECKS` as
`check_handoff_probes` (FAIL-class, so a toothless probe blocks the ship-gate). It mechanizes
the manual probe-gate (§5), which remains the rationale-quality backstop.

---

## 12. Relationship to v4

| v4.4 | v5 |
|---|---|
| 8-file teaching bundle pasted into the browser | thin boot (`HANDOFF_BOOT.md`) + residual + probe manifest |
| Comprehension questions answerable from the bundle | teeth-y probes answerable only from live state |
| Task-state re-narrated in `05_NOW` | pointer to BACKLOG + drift-flags |
| Methodology extracts copied into `02_METHODOLOGY` | methodology referenced by pointer; enforced mechanically |
| Browser receives + proves; CC consolidates | CC owns/initiates; browser is a thin reactive partner |
| Verification = Phase-2 self-check + operator visual | split: browser=artifact, CC=state fidelity |

What v4 got right and v5 keeps: ephemeral generation (no hand-maintained surfaces), degrade-
loudly, the escalation ladder, the beta→stable judgment-augmented promotion criterion, and the
sender's lived "why" as the irreducible thing only the prior session can transmit (now the
"residual," §2).

---

## 13. Modes — architect | execution (residual profile + browser posture)

One process, **two modes**, not two machines. A mode is selected by a `/handoff` parameter
(§10) and resolves to a **residual profile** (what CC emits, §2) + a **browser posture** (the
operating role, §4/§7). The mode is chosen from what the *next* session will do:
**advance-a-backlog-item → execution**; **define-or-reshape-the-way-of-working → architect**
(architecture / planning scope — the audit's scope D). Default is **execution**.

**Operator invocation** — which mode, the exact `scripts/gen_handoff.py` command, and one
copy-paste example per mode (architect · execution · epic · developer · functional) — is the
single runbook **PLAYBOOK §8 "How to hand off"** (the command surface is
`.claude/commands/handoff.md`). This section is the *mechanics*; that runbook is the
*invocation table* — it points here, not the reverse.

### Execution mode (default)

v5 exactly as specified in §§1–12 — the mode label on the current behaviour, nothing added:

- Residual (§2): scoped to the task — un-committed "why" + pointers + drift-flags.
- Task-state (§6): pointer to `BACKLOG.md` + live branches + drift-flags.
- Browser posture (§7): reactive partner + filter.

### Architect mode

For a session that *defines or reshapes the way of working*. Same residual machinery (§2),
re-profiled, with two architect-only in-session layers added — orientation, then the
operator-context beat:

- **(a) Residual scoped to the planning session** — the planning "why": which design tensions
  were weighed, which options were considered and rejected, what is still open. Not a single
  task's "why."
- **(b) Task-state = a pointer to the whole `BACKLOG.md` / the relevant theme(s)** — the
  task-graph, not one item. **Durable encoding shipped via #156** (ratified ADR-66 amendment
  2026-06-14): the BACKLOG schema now carries OPTIONAL `· depends-on: #id, #id` (hard
  precedence) and `· serialize-group: <label>` (shared-mutable-resource mutual exclusion) task
  clauses, with reference-existence + no-cycle enforced read-only in `validate_backlog.py`.
  Parallel-safety is **derived** (no `depends-on` path + no shared `serialize-group`), not
  declared. So an architect can encode genuine hard edges durably in BACKLOG; **soft/provenance
  relations stay residual prose** (the `depends-on` clause is hard-blocked-by ONLY), and any
  graph reading the architect has not encoded as a schema edge is still residual, not a schema
  fact. See ADR-66 §Amendments (2026-06-13, ratified 2026-06-14).
- **(c) Orientation (the vision frame) — a §5 "exact-line quote" probe; a forced-read *tool* that
  establishes the vision, not the navigation gate.** The opening sequence is **role → vision →
  standing topics → backlog**: role is set by §4, this layer establishes the vision, standing
  topics (the active epic themes + `status: ACCEPTED, disposition: active` intakes) are reconciled
  next (intake #18 A7 — the P0 probe legs land with the §B(b) build), and **the backlog (b) is what
  navigates** — once role, vision and standing topics are in hand the architect starts from
  `BACKLOG.md`, not from the orientation read. This is the scope-D fix, delivered the v5 way: **forced read, never a copy,
  never a paraphrase.**
  - A plain-language "what is this project" answer is **summary-bluffable** and so fails §5's
    own bar (§5: *a probe answerable from the compaction summary is removed or hardened*).
    Re-narrating VISION into the handoff is equally barred (§2/§3). Orientation is therefore
    neither summarized nor copied.
  - Instead, bind an **exact-line probe** (§5 manifest "exact-line quote" row) to a **specific
    orienting line**: the opening sentence of `VISION.md` `## Vision` (*what `.dev-knowledge`
    is*) and the `ARCHITECTURE.md` Ch1 opening line (*where this work sits — Layer 2 of the
    ADR-28 three-layer model*). The handoff ships the **source-locator + the substring-check
    command, never the line itself** (generator-excluded, §5 condition 2). The orienting line
    enters the session **only** by CC reading it from the **live** primary source at
    check-time; the quote must match as a **substring**. The read is *forced*; comprehension
    follows from having to surface the exact line, not from a paraphrase a summary could fake.
  - Net: **readable-first is a verified property of the handoff** — the architect cannot
    proceed without the live orienting line in hand — **with zero content copied**; the
    no-re-narration rule (§2/§3) and the no-bluff rule (§5) both hold. This is the layer the v5
    execution bundle lacked.
- **(d) Operator-context beat — one targeted ask for off-repo context; after orienting, before
  design begins.** CC's handoff is **repo-derived** and structurally cannot carry operator intent
  or off-repo findings, so once the orienting lines are in hand the architect makes **one** targeted
  ask: *what off-repo context for this planning session — intent, priorities, findings not in the
  repo, changed decisions?* **Architect mode only** — execution carries no such beat (the
  strategic-vs-tactical split: human-in-the-loop steering belongs at the planning layer, not the
  execution layer). **Off-repo only:** it does **not** duplicate or re-narrate the CC-generated
  residual (§2 — the residual is the repo-side, un-committed "why"); it is the off-repo channel that
  the residual structurally cannot be. It restores the v4 interview's **operator-injection** function
  **without** the gap-filling — it is **not** the v4 eight-file interview (the residual fills the gaps
  now), just the one ask. Local proof of the gap: this track's own `profile ↔ repo` overlap finding
  was browser-side and nearly lost for want of this channel. **(v5.2 reconciliation):** when the outgoing supplement carries **answers**, the outbound
  interview's Q6 now captures off-repo context **at handoff time** (carried in `SUPPLEMENT.md` — see
  *Architect strategic supplement* below), so this inbound beat narrows to the lighter *"anything
  changed since the supplement was written?"* — **kept** (operator intent can shift between sessions),
  its role refined, not duplicated. **When the supplement is empty** (a cold / `/clear`ed handoff —
no answers carried), the beat fires **full** — there is nothing to narrow against (the empty
supplement is the defined cold-handoff disposition; see *Architect strategic supplement* below).
- **(e) Open architecture questions** travel as residual — the design decisions not yet made,
  surfaced (not buried) so the next session resumes the design rather than rediscovering it.

**Browser posture — generative / decompositional** (resident in `HANDOFF_BOOT.md`, §4 — the
posture must reach the file-less browser). Distinct from §7's reactive execution-filter: the
architect **drives decomposition** (turns the architecture into the task-graph), **holds the
whole-system view** (orientation + the `ARCHITECTURE.md` map), and **surfaces design tensions
proactively** — it stress-tests the design, it does not merely filter CC's output. The §7
plan-review output contract still applies.

### The return channel is already here — no new artifact

Execution's divergence-from-plan reaches the next architect session through the **existing**
up-channel, not a new leg: the **residual** (§2 — the un-committed "why," including where
execution departed from the plan), the **drift-flags** (§2 — reality vs the written record),
and the **BACKLOG pointer + drift-flag** (§6). v5 §2 + §6 **are** the architect's inbound
signal. Architect mode adds **no** return-leg artifact — adding one would re-create the v4
hand-maintained-surface disease (§12).

### Architect strategic supplement (v5.2 — always-generated fillable file)

v5's one structural gap: the architect's strategic *why* — the intent, the tensions weighed, the
options rejected — originates in the **browser** (Layer 1), but the residual is **CC-emitted**
(repo-derived), so CC structurally cannot emit that *why*. The supplement closes that gap: an
**always-generated, self-documenting, fillable file**, committed on the handoff branch, folded into
the next session **only if answered**. **Architect-mode-additive only; the v5 model (§§1–12) and
execution mode are unchanged.**

**The lifecycle (CC generates the file; the operator fills it async; CC commits it; the assembler
folds it if answered):**

1. On `/handoff … architect`, CC writes `docs/handoffs/<slug>/SUPPLEMENT.md` **unconditionally** from
   `templates/handoff/v5/SUPPLEMENT.md.tmpl` — the fixed 6-question *why*-only schema below (CC MAY
   append 1–2 session-specific items it observed as `A./B.` addenda; it adds nothing else). The file
   is self-documenting: an operator 3-step header, a **QUESTIONS** section for the **outgoing**
   architect chat, and an empty **ANSWERS** section below a divider line.
2. CC commits the file (empty at first) **on the handoff branch** — so the artifact exists and is
   tracked even when no one fills it. This is the durable record the v5.1 ephemeral block lacked.
3. The operator copies the QUESTIONS into the **outgoing** architect chat (the chat that did this
   session's work — the only actor holding this session's strategic deliberation), pastes that chat's
   answers (combining one or more chats if needed) into the ANSWERS section, and tells CC
   `supplement filled`.
4. CC commits the now-filled file on the branch **verbatim** (no re-typing; **CC never fabricates
   answers**), and `scripts/assemble_paste.py` folds the **ANSWERS region only** into the next
   session's `PASTE_THIS.md` — **only when non-empty** (the QUESTIONS are for the outgoing browser,
   not the incoming session).
   **What "verbatim" means, operationally (supplement + intake transport):** the **content line
   stream is byte-identical** — every non-empty line reproduced exactly, in order, with no
   rewording, reordering, trimming, or summarizing. **Whitespace-only additions are permitted
   solely for markdown rendering** (e.g. a blank line before a list so it renders as a list) **and
   MUST be reported** when the transport is reported. Anything that changes a non-empty line is not
   verbatim, however small.

**Cold-handoff disposition (the defined N/A, not a defect).** When there is **no outgoing chat** to
ask — a cold / `/clear`ed handoff — the operator leaves ANSWERS **empty**. The empty file is **still
committed** (a durable record that this session carried no transmissible live *why*); the assembler
prints an `ANSWERS empty ... not folded` note and folds nothing; the **incoming** architect's §13(d)
operator-context beat fires **full** (no answers were carried, so there is nothing to narrow against).
This resolves the first-dogfood finding (the 2026-06-16 bundle `RESIDUAL.md` §2): "expected in
architect mode" no longer reads as a missing deliverable when there is structurally no one to interview.

**The schema = the interview questions (non-re-derivable *why* ONLY).** Canonical source:
`templates/handoff/v5/SUPPLEMENT.md.tmpl` (kept generic/portable so the deferred #164 cross-repo
generator carries it unchanged):

1. **Strategic intent** — what the next session should achieve at the way-of-working level (a
   design/methodology goal, not a task).
2. **Tensions weighed** — which design trade-offs were weighed this session, where you landed, and why.
3. **Considered + rejected** — options considered and rejected, with the reason (so the next session
   does not relitigate).
4. **Open questions** — design questions still unresolved or deliberately deferred.
5. **Decomposition rationale** — why this task-graph shape; what the next session must NOT redo or
   re-decide.
6. **Off-repo context** — intent / priorities / changed decisions / findings not in the repo.

**Hard scope constraint (load-bearing — this is what keeps the supplement from becoming the v4
disease).** The interview asks **only** the *why* above. It **never** elicits repo state, methodology,
task-state, counts, or SHAs — those stay **source-authoritative + forced-read** (§3/§5). The
supplement is **advisory, not teeth-bearing**: where any answer touches verifiable state, the existing
drift-checks (§5/§8) catch staleness; the supplement is never trusted over the repo. `SUPPLEMENT.md`
is a **per-session artifact** — generated fresh each architect handoff and committed for tracking,
then consumed (its ANSWERS folded) by the next session, exactly like
`RESIDUAL.md` / `PROBES.md` — **not** a maintained surface, so it does not re-create the v4
hand-maintained-surface disease (§12). And it is a **forward** brief (outgoing architect → next
session via `PASTE_THIS`), distinct from the return channel above — it adds **no** return-leg.

**Generator note (v5.4).** The bundle lifecycle above is emitted by `scripts/gen_handoff.py`
(#164 RF-2 slice, `9d5ebe5`): `HANDOFF_BOOT.md`/`RESIDUAL.md` are **state-filled scaffolds**
whose FILL-IN narrative survives a `--filled` re-render byte-for-byte; `PROBES.md` renders from
the answer-free probe-core template (`templates/handoff/v5/PROBES.md.tmpl` — the §5 structural
contract); `SUPPLEMENT.md` is written unconditionally in architect mode (the v5.2 flow above,
unchanged); and `scripts/assemble_paste.py` warns past a paste size budget (the re-narration
creep counterweight). The cold→FILLED flip is mechanized via the assembler's shared fill-state —
the §13(d) beat fires FULL exactly when ANSWERS is empty. Adoption note: the generator exists
and is dogfooded against a stub repo; live bundles MAY still be hand-authored until #164's
adoption slice closes (hand-authored bundles remain bound by the same §5 gate).

**Residual completeness — the FILL-IN contract (ARC-5).** A bundle's hand-authored FILL-IN
regions **must be authored before the bundle is committed**; a region that is **empty** or
still carries its **generator placeholder** fails the ship-gate. Two placeholder forms are governed: `_(fill: …)_`
in `RESIDUAL.md` / `PASTE_THIS.md`, and `_FILL-IN (root): …_` in `HANDOFF_BOOT.md` /
`EPIC_BOOT.md` / `FUNCTIONAL_BOOT.md`. Enforced by `residual_completeness` (an `ALL_CHECKS`
FAIL-class member; logic in `scripts/validate_residual_completeness.py`). **Diff-triggered:** it
examines bundle files added or modified against HEAD, so an already-committed bundle is
grandfathered while the commit that *lands* an unfilled one is refused. *Honest limit:* it
reads the **working-tree** copy, not the staged blob, so a bundle staged unfilled and then
filled without re-staging is not caught ([#366]). It asserts only that the
placeholder was **replaced** — never that any particular value is present, because §5's
anti-bluff contract requires the ship-gate verdict, the WARN count and drifted ids to be
**absent** from the bundle; `PROBES.md` is therefore never inspected by this check. *Origin:* the
ARC-5 bundle merged with §1 ("THE HEADLINE"), §2 and §4 ("the residual's core payload") as
literal unfilled templates and no organ objected.

**The carrier is the file itself.** The interview **answers ARE the artifact** — carried verbatim
and advisory; the file exists from generation as the durable workspace + tracking record.

**Relation to beat (d).** Q6 (off-repo context) is captured here **only when the supplement carries answers**, so the inbound
operator-context beat (d) narrows to *"anything changed since?"* The two are **one channel split
across the session boundary**, not two asks — (d) refined, not duplicated.

Mode is carried by `/handoff … v5 <architect|execution>` (§10 self-updating; default
`execution`; mode applies only in v5 mode — v4.4 has no modes). Command wiring:
`.claude/commands/handoff.md`.

**Bundle shape (no per-bundle README — one canonical runbook).** A v5 bundle carries **four**
files — `HANDOFF_BOOT.md` + `RESIDUAL.md` + `PROBES.md` + `PASTE_THIS.md` — and **no README**.
The stable operator boilerplate (who-each-file-is-for · the same-name role-file/bundle-pointer
collision · `PROBES.md`-handed-once · the run loop with its *why* · the flow diagram · the
rationale) lives once in the **canonical per-repo operator runbook at `docs/handoffs/README.md`**
(operator-first: walkthrough first, rationale demoted) — not copied into each bundle. Each
bundle's **session-specific header** (slug · one-line purpose · mode) lives in its own
`HANDOFF_BOOT.md`, which points back at the runbook; the bundle `HANDOFF_BOOT.md` carries that
header + the paste-pointer and does **not** repeat the walkthrough. The runbook is generic across
repos of the same handoff version: the #164 generator seeds/updates each repo's
`docs/handoffs/README.md` idempotently from one source (`templates/handoff/v5/README.md.tmpl`, a
deferred stub until #164 lands) and emits the four-file bundle — never a per-bundle README.

**`PASTE_THIS.md` convention.** Assembled by `scripts/assemble_paste.py <bundle_dir>` at handoff
generation time; **never hand-edited**. Regenerate each handoff by re-running the assembler.
Manifest in order: (0) bundle `HANDOFF_BOOT.md` session-header block (slug/mode/purpose/generated-at,
extracted up to the first `## ` heading — optional; skipped if the bundle carries no HANDOFF_BOOT.md),
(1) `protocols/HANDOFF_BOOT.md` (required — browser role file + boot line), (2) `RESIDUAL.md`
(required), (3) `PROBES.md` (required), (4) `SUPPLEMENT.md` (the v5.1 architect interview answers —
**expected in architect mode**, optional elsewhere; the assembler `[warn]`s in architect mode /
`[skip]`s otherwise if absent). Sections delimited by `\n\n---\n\n` with
`=== <label> ===` headers. P1 orienting answers are **not** embedded — they are obtained only via
the CC run loop (the teeth of the probe mechanism). The operator pastes `PASTE_THIS.md` as the
single file; the browser receives the complete role + residual + probes + supplement in one shot.

---

## 14. Epic-lane handoffs — EPIC (§14a) + EPIC RETURN (§14b)

Tree orchestration (**ADR-97**; operating model in PLAYBOOK §8) adds two handoff types for
**epic lanes** — additive to §13, which is unchanged for root-to-root architect succession.
An epic lane is an L1 browser chat with the same stance as §1's browser, scoped down to one
epic inside a **root-provisioned worktree** (branch `epic/<slug>`). The governing invariant:
**every lane boots from a generated handoff and closes with a return** — no lane runs on
chat-prose instructions; the contract is the artifact (ADR-97 invariant 5).

### §14a — EPIC handoff (architect → epic chat)

A scope-contract, generated per epic at lane spawn. Carries:

1. **Epic scope** — the BACKLOG slice (epic id, stories, done-when per story).
2. **Epic done-contract** — the hard closure metric for the whole epic (ex-ante,
   architect-authored, immutable to the lane).
3. **Worktree + branch** — names provisioned by the architect (`claude --worktree
   <epic-slug>`; branch `epic/<slug>`); **RELATIVE PATHS ONLY** (the
   absolute-path-bypasses-worktree lesson is a hard rule).
4. **FILE-BOUNDARY** — the explicit file/dir set the lane may touch. This is the parallelism
   ruling made mechanical — two concurrent epics MUST have disjoint boundaries; a needed file
   outside the boundary = **escalate, don't touch**.
5. **Escalation rules** — ADR-worthy fork, boundary-breach need, cross-epic dependency
   discovered → STOP, return to the architect. Everything intra-epic is the lane's own
   judgment.
6. **Refusals** — no merge to main, no ADRs, no backlog structure, no worktree lifecycle ops,
   no new top-level folders, no content deletion without operator ask.
7. **Execution MODE** — the lane's execution mode, declared ex-ante by the root
   (plan / plan-then-auto / auto-accept) with its basis. **L-sized epic stories default
   plan-first**, and **every architect prompt into the lane re-declares MODE** — a lane
   inherits no mode from a prior prompt. (v5.6 corrective, origin the 2026-07-06 mission
   plan gate; mode criteria live in PLAYBOOK Ch4 "How to choose Mode", not here.)

### §14b — EPIC RETURN handoff (epic chat → architect)

The lane's closing report, **required before any merge**:

1. Commits on the epic branch (SHAs, one line each) + branch state (clean tree, tests green
   ON THE BRANCH).
2. **Contract-vs-outcome per story** (met / partial / dropped, with evidence) — closure
   claimed on the hard metric, never "committed".
3. Self-adjudications + anything ARCHITECT-REVIEW-PENDING.
4. **Proposed BACKLOG delta** (structural changes for the architect to apply — the
   BACKLOG-single-writer-for-structure ruling, ADR-97).
5. **Merge-readiness checklist**: boundary respected (diff touches only the declared set), no
   main merges performed, JOURNAL entry on branch names session SHAs.

The architect then: reviews the return vs the contract → serial merge `--no-ff` → applies the
backlog delta → declares closure → teardown (worktree remove + prune + branch -d + orphan
check). **The loop closes at the root, always.**

**Generator.** `templates/handoff/epic/{EPIC_BOOT,EPIC_RETURN}.md.tmpl`, emitted by
`scripts/gen_handoff.py --mode epic` (reuses the v5 assembler; **probes stay** — an epic lane
still boots on live-state probes scoped to its boundary; the §5 answer-free structural
contract applies unchanged). `--mode developer` is an **additive alias** of `--mode epic`
(ADR-98 — the executor mode's go-forward name, alias-first; a developer-mode bundle is
byte-identical to an epic one and its header renders `epic` until the deferred naming flip).

---

## 15. Token-log cadence (session-boundary maintenance, runs on /session-summary)

Relocated from PLAYBOOK §8 (#152, 2026-06-15): this is session-boundary maintenance fired by `/session-summary`, so it belongs with handoff mechanics rather than as a resident copy in PLAYBOOK. PLAYBOOK §8 now points here. (Renumbered §14 → §15 in v5.5 — the epic-lane handoff types took §14, keeping the handoff-type sections contiguous with §13; pre-v5.5 references to "§14" in the Section history below mean this section.)

Every /session-summary run checks TOKEN-LOG.md staleness. If latest entry >7 days old, a new short-format snapshot is appended via `ccusage --json`. Otherwise skipped.

**Trigger:** /session-summary staleness check; conditional execution (not every session).

**Source:** `ccusage --json` (reads local Claude Code usage data — see ENVIRONMENT.md)

**Threshold:** 7 days. Most recent entry's date extracted from first `## YYYY-MM-DD` header line in `logs/TOKEN-LOG.md`.

**Format (short, sustainable):**

```
## YYYY-MM-DD (since YYYY-MM-DD delta)

Cost: $X.XX | Sessions: N | Active days: N
Tokens (in+out): X.XM
Top models: Model-A X%, Model-B Y%, Model-C Z%
Peak day: $X.XX on YYYY-MM-DD
Notable: [1-2 line signal e.g. "Opus 4.7 adoption curve", "Haiku routing shift"]
```

**Order convention:**
- TOKEN-LOG.md: newest-first (prepend). Rationale: logs optimize for current-state scanning. (CHANGELOG.md retired — ADR-49.)
- LESSONS.md: append-only (oldest-first). Rationale: chronological narrative; order preserves "what we learned when".

New TOKEN-LOG entries go at the top (after file header, before previous newest entry). /session-summary reads the first matching `## YYYY-MM-DD` header for the staleness check.

**Cache tokens** excluded from in+out for cross-period comparability. Note cache only when notable.

**Rationale:**
- Per-session cadence rejected: ~$0.02/run overhead wasteful for weekly-sufficient data
- Manual weekly ritual rejected: forgetting risk (4 weeks stale before ccusage adoption)
- Threshold-based: amortized ~$0.006/run, auto-triggers on staleness, zero forgetting risk
- Short format keeps entries scannable over months; full format reserved for migrations

---

## 16. Functional mode — the intake-capture boot (ADR-98)

The requirements-intake handoff type: a boot for the **functional architect** — a lightweight
browser chat whose **sole product is an intake document** (WHAT/WHY: problem, scenarios,
requirements, ex-ante acceptance criteria — never HOW). Additive to §13 (unchanged —
functional is a new boot contract, not a third §13 residual profile) and §14. Pipeline
position + genre demarcation (intake doc / ADR / backlog epic): **ADR-98**; the one-place
chain documentation: PLAYBOOK Part II §2; artifact format + lifecycle + confirm-gate:
`docs/intake/README.md` + `templates/intake-template.md`.

**The boot (one file, generated).** `scripts/gen_handoff.py --mode functional` emits
`FUNCTIONAL_BOOT.md` from `templates/handoff/functional/FUNCTIONAL_BOOT.md.tmpl` — the whole
paste (no `PROBES.md` / `RESIDUAL.md` / `SUPPLEMENT.md` / `PASTE_THIS.md`, no assembler; the
§14 epic-mode precedent). It carries:

1. **Role contract** — does / does-NOT (listen, probe with scenario questions, structure the
   operator's intent; never solutionize, never write ADRs, never touch the backlog), the
   output format, the conversion path (converse → CC converts the synthesis into the intake
   template → **the operator approves the draft before it lands** — the ADR-98 §4
   confirm-gate), and the deflection rule: a technical-factual turn is answered *"that's a
   technical-architect question"* and recorded as an open question, never guessed.
2. **Vision extract** — the committed `VISION.md` `## Vision` body, copied mechanically at
   generation time.
3. **CC-authored state summary** — one FILL-IN paragraph (the RF-6 splice; a re-render
   preserves it byte-for-byte).
4. **Intake index** — a committed-state enumeration of `docs/intake/*.md` (id · status · title;
   README excluded) so conversations don't re-discover open/parked docs and seeds.

**NO live-state probes — by design, not omission.** The functional chat's subject is the
operator's head, not the repo; ground-truth verification is the technical architect's lane
(§13). A functional boot is therefore deliberately **state-carrying** — committed-state
copies, not probe answers — and the §5 answer-free invariant applies in **narrowed form**: no
counts, SHAs, verdicts, or date-relations enter the boot; generation-time values still flow
only to the JOURNAL draft, never the bundle.

**Rent (ex-ante).** The scene's consumer is the technical-architect triage; intake docs
unconsumed after ~1 month put the scene under review for removal (ADR-98 §6). The
intake↔epic edge stays **advisory until n=2** intake docs are consumed end-to-end (ADR-98 §5).

---

## Section history

- v5.0-beta → v5.0 (2026-06-11 → 2026-06-15, seven entries condensed 2026-07-05 per ADR-49/65 —
  info-preserving; full prior entries: `git log --follow -p -- protocols/HANDOFF_PROCESS.md`) —
  the v5 genesis arc: initial parallel-ship beta recording model C (ADR-82 — CC-owned handoff,
  thin browser boot, residual + drift-flags-as-headline, teeth-y forced primary-source reads);
  §13 `architect | execution` modes added (#150); **promoted to canonical** in the #149 atomic
  flip (v4.4 archived, Council gate operator-waived, ADR-82 ratified; #159/#161/#162 carried
  open); §13 bundle-shape iterated README-tmpl → no-per-bundle-README + canonical per-repo
  operator runbook (`docs/handoffs/README.md`) → **four-file bundle** (`HANDOFF_BOOT.md` +
  `RESIDUAL.md` + `PROBES.md` + `PASTE_THIS.md`, assembled by `scripts/assemble_paste.py`,
  single-paste onboarding; #164 rescoped to the generator); §14 token-log cadence relocated in
  from PLAYBOOK §8 (#152). Version ended 5.0 (all additive post-flip).
- v5.1 (2026-06-16, §13 architect strategic supplement — interview extraction) — **Version → 5.1**
  (first minor bump; additive, architect-mode only). New §13 sub-section "Architect strategic
  supplement — interview extraction": the architect's strategic *why* (intent · tensions weighed ·
  options rejected · open questions · decomposition rationale · off-repo context) becomes a
  **first-class advisory supplement produced by a structured 6-question interview** — CC emits a
  paste-ready interview block (sourced from `templates/handoff/v5/SUPPLEMENT.md.tmpl`), the operator
  relays it to the **outgoing** browser, and the browser's answers become `SUPPLEMENT.md` verbatim
  (no re-typing), which `scripts/assemble_paste.py` folds into `PASTE_THIS` (expected in architect
  mode; `[warn]` if absent). Closes v5's one structural gap (the *why* originates browser-side but the
  residual is CC-emitted, so v5.0 leaned on operator-relay / human memory). Hard scope constraint: the
  interview asks **only** non-re-derivable *why* — never repo state / methodology / task-state (those
  stay source-authoritative + forced-read, §3/§5); the supplement is advisory, never teeth, and a
  per-session transient (not a v4-disease maintained surface). §13(d) operator-context beat refined to
  the lighter "anything changed since the supplement?" check (Q6 captures off-repo context at handoff
  time); beat kept, not duplicated. Coupled atomic move: `CONTRIBUTING.md` stamp v5.0→v5.1 (the only
  gate-forced surface; major stays 5, so `CLAUDE.md` / `.claude/commands/handoff.md` unchanged).
  ADR-82 amended in-file (2026-06-16). §§1–12, §14 unchanged. Refs #159 (operator-context beat),
  #164 (cross-repo generator — schema kept portable for it).
- v5.2 (2026-06-17, §13 architect strategic supplement — always-generated fillable file) — **Version
  → 5.2** (second minor bump; additive, architect-mode only). The §13 supplement is reworked from a
  v5.1 **ephemeral terminal interview block** (durable only *after* the outgoing browser answered — a
  cold/`/clear`ed handoff produced no file, no tracking, no lead-by-hand) into an **always-generated,
  self-documenting, fillable file**: CC writes `docs/handoffs/<slug>/SUPPLEMENT.md` unconditionally
  (QUESTIONS for the outgoing chat + an empty ANSWERS section), commits it on the handoff branch for
  durable tracking, and `scripts/assemble_paste.py` folds the **ANSWERS region only, only when
  non-empty** into the next `PASTE_THIS` (was: whole-file fold + warn-if-absent). Defines the
  **cold-handoff disposition** (empty ANSWERS = committed N/A, not folded; the incoming §13(d) beat
  fires full) — resolving the first-dogfood finding (2026-06-16 `RESIDUAL.md` §2). Contract unchanged:
  advisory, why-only, never teeth, never fabricated (unanswered = committed empty). Coupled atomic
  move: `CONTRIBUTING.md` stamp v5.1→v5.2 (the only gate-forced surface; major stays 5, so `CLAUDE.md`
  / `.claude/commands/handoff.md` unchanged). ADR-82 amended in-file (2026-06-17). §§1–12, §14
  unchanged. Refs #159 (the real dogfood — mechanism defined here, not yet exercised), #164 (generator
  must emit the always-file form).
- v5.2 (2026-06-24, §13 narration condense) — condensed the v5.0→v5.1→v5.2 evolution-narration in the
  architect-supplement subsection to its current state (info-preserving: the evolution stays in this
  Section history + git). Live mode spec / lifecycle / schema / `SUPPLEMENT.md.tmpl` pointers all
  **unchanged**. **Version unchanged (5.2; condense-only — no rule change.)** Companion to the STEP-0
  finding that the C1/C4/C6 v4-corpus *removal* premise is refuted (the named targets are live/gated,
  not dead) — this arc removed nothing, only the redundant evolution prose. Refs #164.
- v5.3 (2026-06-25, §5 probe-manifest consolidation) — **Version → 5.3** (third minor bump; a
  probe-contract / bundle-shape change like the v5.1/v5.2 supplement bumps — not a condense). §5's
  **drift-flag set** + **freshness witness** probes fold into one **Ship-gate read-back** row: both
  bind to checks `ship-gate` already runs (`git_backlog_drift`, `canonical_freshness` — `ALL_CHECKS`
  members whose evidence prints inline), so running the gate re-derives them with **zero verification
  coverage lost**. Anti-bluff preserved — the read-back's teeth rest on the dispositioned-WARN count +
  any `[stale]` line (both drift, neither is the §1 headline), not the bluffable GREEN/RED verdict.
  Kept verbatim, the four probes `ship-gate` structurally cannot recover: Live check count (its token
  lives in `audit.py checks`, not the verdict), Exact-line quote (anti-bluff), Live HEAD/tree (volatile
  sha), Pointer round-trip (orientation). Net 6 → 5 probes. No `audit.py` change — `parse_probes` reads
  the bundle PROBES.md table generically; the consolidated §5 keeps the 4-column schema. **Coupled
  atomic move (this commit):** `CONTRIBUTING.md` stamp v5.2→v5.3, the 2 `reconciled_with` edges
  (`ARCHITECTURE.md`, `docs/handoffs/README.md`) @5.2→@5.3, and the 3 freshness-gated docs re-read +
  restamped (the re-read filed #204 — a stale CONTRIBUTING nightly-outcome section). Major stays 5
  (`CLAUDE.md` / `.claude/commands/handoff.md` unchanged). Executes the deferred "Arc 2 = 5.3 bump +
  full reconciliation" (afb7421). Refs #161, #204.
- v5.4 (2026-07-05, §5 structural anti-bluff + §13 generator note) — **Version → 5.4** (fourth
  minor bump; additive only — no rule removed or weakened). §5 gains "Structural enforcement —
  anti-bluff by construction": the item-2 "never the answer" contract is now machine-held
  (row-scoped `expected[ :]` FAIL rung in `verify_handoff_probes.py`; `gen_handoff.py` renders
  bundles answer-free by construction, diverting generation-time values to a stdout
  JOURNAL-draft; the promotion dogfood re-runs structurally per-bundle via the gate). §13 gains
  the generator note (#164 RF-2 slice: scaffold fill-preservation, answer-free probe template,
  unconditional SUPPLEMENT, paste size-warn, mechanized cold→FILLED flip) with the honest
  adoption caveat (live bundles MAY still be hand-authored until #164's adoption slice closes).
  Documents the RF-1 option-b mechanism landed `9d5ebe5` (2026-07-04) — the spec catches up to
  shipped structure, deferred at that merge to fold into this reconciliation arc. **Coupled
  atomic move (this arc):** `CONTRIBUTING.md` stamp v5.3→v5.4, the 5 `reconciled_with` edges
  (`ARCHITECTURE.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `docs/handoffs/README.md`,
  `protocols/HANDOFF_BOOT.md`) @5.3→@5.4 (each site-enumerated + verdicted per
  `check-against-spec`), freshness-gated dependents genuinely re-read + restamped, and the 3
  PLAYBOOK advisory version strings refreshed. Major stays 5. Refs #164, RF-1 (2026-07-04
  handoff-adoption review), 2026-07-05 overnight run Block D.
- v5.5 (2026-07-05, §14 epic-lane handoffs + token-log renumber §14→§15) — **Version → 5.5**
  (fifth minor bump; additive — no §1–§13 rule changed). New **§14 "Epic-lane handoffs"**
  records the two tree-orchestration handoff types (**ADR-97**; operating model PLAYBOOK §8):
  **§14a EPIC handoff** (architect → epic chat scope-contract: epic scope · ex-ante immutable
  done-contract · root-provisioned worktree/branch, relative paths only · FILE-BOUNDARY as the
  parallelism ruling made mechanical · escalations · refusals) and **§14b EPIC RETURN** (epic
  chat → architect closing report, required before any merge: branch commits/state ·
  contract-vs-outcome on the hard metric · self-adjudications · proposed BACKLOG delta ·
  merge-readiness checklist), plus the root's post-return sequence (review → serial `--no-ff`
  merge → backlog delta → closure → teardown). Generator: `templates/handoff/epic/` +
  `gen_handoff.py --mode epic` (v5 assembler reuse; §5 answer-free probe contract unchanged,
  boundary-scoped). The former §14 (token-log cadence) renumbered → **§15** verbatim (the only
  live external pointer, PLAYBOOK's relocation note, updated in the same commit; historical
  "§14" mentions in this Section history refer to it, per the §15 renumber note). §13 is
  untouched — epic lanes are a new handoff type, not a third §13 mode. **Coupled atomic move
  (this commit-set, root-granted boundary extension 2026-07-05):** the 5 `reconciled_with`
  edges (`ARCHITECTURE.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `docs/handoffs/README.md`,
  `protocols/HANDOFF_BOOT.md`) @5.4→@5.5 (each site-enumerated + verdicted per
  `check-against-spec`), version-string sites refreshed, freshness-gated dependents genuinely
  re-read + restamped. Major stays 5. Refs ADR-97, Epic 2 (tree-orchestration §14
  integration), 2026-07-04 lived precedent.
- v5.6 (2026-07-06, §14a execution-MODE item — the plan-mode corrective) — **Version → 5.6**
  (sixth minor bump; additive — §1–§13 and §14b untouched). **§14a gains item 7:** the EPIC
  handoff carries a mandatory **execution-MODE declaration** (plan / plan-then-auto /
  auto-accept, root-declared ex-ante with its basis); **L-sized epic stories default
  plan-first**, and **every architect prompt into a lane re-declares MODE** (a lane inherits
  no mode from a prior prompt). Template: `templates/handoff/epic/EPIC_BOOT.md.tmpl` gains the
  Execution-mode header row + a root-authored `FILL-IN:exec-mode` region (the generic FILL-IN
  splice carries it — no generator change). PLAYBOOK carries the operating rule (Ch4 Per-Scale
  L + Ch8 tree-orchestration). Origin: the 2026-07-06 overnight-mission plan gate
  (architect-approved corrective CH-1, full (a)+(b)+(c)). **Coupled atomic move (this
  commit):** the 5 `reconciled_with` edges (`ARCHITECTURE.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
  `docs/handoffs/README.md`, `protocols/HANDOFF_BOOT.md`) @5.5→@5.6, each site-enumerated +
  verdicted per `check-against-spec` (compressed sweep — the change is additive §14a-only:
  only the frontmatter stamps + CONTRIBUTING's §Handoff-process version clause stale; every
  other site fine/not-relevant); freshness-gated dependents genuinely re-read + restamped.
  Major stays 5.
- v5.7 (2026-07-07, §16 functional mode + §14 developer alias — the ADR-98 intake scene) —
  **Version → 5.7** (seventh minor bump; additive — §1–§15 rules unchanged; §14 gains one
  alias sentence). New **§16 "Functional mode — the intake-capture boot"**: the
  requirements-intake handoff type (ADR-98) — a one-file, probe-free `FUNCTIONAL_BOOT.md`
  (role contract · VISION extract · CC-authored state-summary FILL-IN · intake index),
  emitted by `gen_handoff.py --mode functional` from `templates/handoff/functional/`;
  deliberately state-carrying (committed-state copies, not probe answers), the §5
  answer-free invariant kept in narrowed form (no counts/SHAs/verdicts; generation-time
  values stay JOURNAL-draft-only). §14's generator note gains `--mode developer` as a pure
  additive alias of epic (byte-identical bundles; header renders `epic` until the deferred
  naming flip). Artifact format/lifecycle/confirm-gate: `docs/intake/README.md` +
  `templates/intake-template.md`; chain documentation: PLAYBOOK Part II §2. **Coupled
  atomic move (this commit):** `CONTRIBUTING.md` stamp v5.6→v5.7, the 5 `reconciled_with`
  edges (`ARCHITECTURE.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `docs/handoffs/README.md`,
  `protocols/HANDOFF_BOOT.md`) @5.6→@5.7, each site-enumerated + verdicted per
  `check-against-spec` (compressed sweep — the change is additive §16 + one §14 sentence);
  freshness-gated dependents genuinely re-read + restamped. Major stays 5. Refs ADR-98,
  #268 (Arc 2 intake-scene build).
