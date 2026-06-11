# HANDOFF_PROCESS v5 (beta — parallel)
<!-- scope: meta -->

Version: 5.0-beta
Status: beta
Effective: 2026-06-11 (beta; **not yet canonical**)
Decision: ADR-82 (Proposed — Council-pending per #148 / ADR-41)
Supersedes (at promotion, not now): HANDOFF_PROCESS v4.4 (`protocols/HANDOFF_PROCESS.md`),
and the heavy-bundle delivery ADR-79 mandated.

> **Status of this file.** v5 ships **alongside** the live v4.4 spec, which stays the
> canonical authority until promotion. While v5 is beta, `protocols/HANDOFF_PROCESS.md`
> (v4.4) governs any handoff actually run. Promotion to canonical is a single atomic flip
> gated on (1) AI Council ratification of ADR-82 and (2) one fresh-eyes review meeting the
> beta→stable criterion **plus the empirical teeth dogfood** (§11). Do not bump the
> canonical `Version:` line or the coupled surfaces until that flip — `audit.py` forces
> them to move together.

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
| **Drift-flag set** | live git ∩ `BACKLOG.md` | the drifted `#id` set is computed at answer-time, documented nowhere | `validate_git_backlog` / `audit.py health` |
| **Freshness witness** | `CLAUDE.md` frontmatter + live git | a relation (`last_reviewed` vs last commit) over post-handoff commits | `audit.py` freshness inputs |
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

## 11. Migration & promotion (parallel-ship)

v5 ships **beta, as this parallel file**, while v4.4 stays canonical and live. Promotion to
canonical is a single **atomic flip commit**, gated on:

1. **AI Council ratification** of ADR-82 (#148 / ADR-41 routing);
2. **One fresh-eyes review** meeting the beta→stable criterion (v4.3.1 §B: Stage-1 **<2
   critical findings** AND a Stage-3 verdict of **PROMOTE / PROMOTE-WITH-CAVEATS**, reviewer
   judgment overriding count);
3. **The empirical teeth dogfood** (§5): one real v5 handoff where every forced-read probe
   **fails** to be answered from the compaction summary alone.

The flip moves the canonical `Version:` and its four coupled surfaces together —
`CLAUDE.md`, `.claude/commands/handoff.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md` — which
`audit.py`'s coupling gates (`check_amendment_coherence`, `check_handoff_version_stamp`) force
to be **atomic**. At the flip: rename this file to `protocols/HANDOFF_PROCESS.md`
(`Version: 5.0`, `Status: stable`); archive v4.4 to `protocols/archive/HANDOFF_PROCESS_v4.4.md`;
archive `templates/handoff/*` to `templates/archive/handoff-v4/`; retarget audit checks
#8/#9 to historical v4 bundles; close #148 / #124 / #25. Tracked by the named successor
backlog item.

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

### Execution mode (default)

v5 exactly as specified in §§1–12 — the mode label on the current behaviour, nothing added:

- Residual (§2): scoped to the task — un-committed "why" + pointers + drift-flags.
- Task-state (§6): pointer to `BACKLOG.md` + live branches + drift-flags.
- Browser posture (§7): reactive partner + filter.

### Architect mode

For a session that *defines or reshapes the way of working*. Same residual machinery (§2),
re-profiled, with one layer added:

- **(a) Residual scoped to the planning session** — the planning "why": which design tensions
  were weighed, which options were considered and rejected, what is still open. Not a single
  task's "why."
- **(b) Task-state = a pointer to the whole `BACKLOG.md` / the relevant theme(s)** — the
  task-graph, not one item. **Honest scope (this pass):** the BACKLOG schema (ADR-66 /
  `validate_backlog`) does **not** encode dependencies or parallelization, so the
  *what-blocks-what / what-parallelizes* graph is carried **in the residual, ephemerally** — it
  is **not** a durable BACKLOG-resident graph, and architect mode must not present it as one.
  Durable encoding is deferred to **#156** (depends-on / parallel fields + an ADR-66 amendment +
  a `validate_backlog` extension). Until then the architect emits the graph as residual prose
  and points at the live BACKLOG.
- **(c) Orientation — a §5 "exact-line quote" probe; the architect's first move, before any
  mechanism.** This is the scope-D fix, delivered the v5 way: **forced read, never a copy,
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
- **(d) Open architecture questions** travel as residual — the design decisions not yet made,
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

Mode is carried by `/handoff … v5 <architect|execution>` (§10 self-updating; default
`execution`; mode applies only in v5 mode — v4.4 has no modes). Command wiring:
`.claude/commands/handoff.md`.

---

## Section history

- v5.0-beta (2026-06-11) — initial parallel-ship beta. Records model C (ADR-82, Proposed):
  CC owns/initiates the handoff; thin browser boot (`HANDOFF_BOOT.md`) replaces the heavy
  bundle; residual + drift-flags-as-headline; teeth-y forced primary-source read reusing the
  existing read-only validators; lean pointer-not-narration task-state; verification split +
  bidirectional adjudication; self-updating `/handoff`. Ships beta beside live v4.4; promotion
  to canonical is Council + fresh-eyes + empirical-teeth-dogfood gated (§11).
- v5.0-beta (2026-06-11, §13 added) — `architect | execution` modes as residual-profile +
  browser-posture variants selected by a `/handoff` parameter (#150). Architect mode adds the
  scope-D orientation layer as a §5 **exact-line-quote** probe bound to `VISION.md` /
  `ARCHITECTURE.md` Ch1 (forced read, never copied, never paraphrased), a planning-scoped
  residual, and a generative/decompositional browser posture; execution mode is the existing
  §§1–12 behaviour. Durable task-graph encoding deferred to #156; the return channel stays
  §2/§6 (no new artifact). Version unchanged (still 5.0-beta; §13 is additive).
