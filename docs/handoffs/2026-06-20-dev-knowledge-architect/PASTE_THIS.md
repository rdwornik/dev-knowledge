=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-20-dev-knowledge-architect` |
| **Mode** | **architect** (v5.2 §13 — planning / way-of-working scope) |
| **Purpose** | **Session-wrap audit** closing the **dependency-arc** wave. The wave shipped; this session **buttoned it up and planned the downstream**: closed **#197** (§4.4 ship-gate disposition — done-when met, `ship-gate` GREEN), reconciled doc-currency (inventoried `scan_undeclared_edges.py` in `ARCHITECTURE.md`; fixed the **OQ-labeling muddle** — #194's gate now names **ADR-89 OQ1**, #196 disambiguated to the *brief's* OQ1), reviewed PLAYBOOK/ESSENTIALS (they correctly omit the hub edge-model organ — the open #77 doctrine), and produced the **next-ship action plan** (`RESIDUAL.md` §3). The wave's organ is live + green: **`reverse_dep_oracle.py`** (#193, ADR-89 OQ2 resolved), **`scan_undeclared_edges.py`** (#179, ADR-88 FC2), **`validate_doc_structure.py`** (#192 = `doc_structure` check #22). **ADR-88 + ADR-89 remain Proposed** (unratified). The next architect **decides + sequences**: ready builds (**#195-2a** safe-removal gate phase-2a, now unblocked by the oracle; **#199** refscan immutable-zone prune; **#196** closure spike) vs gated work (**#194** needs the ADR-89 OQ1 decision; **#195-2b** gated on #196; **#153** is the FF-prevention that stops the `no_ff_merges` class) — plus ADR-88/89 ratification readiness. The **conformance dashboard (#171) is explicitly deferred** (out of scope this session). |
| **Generated at** | HEAD `db61dd0`, working tree clean. This bundle's own commit + the `--no-ff` merge move HEAD; `main` runs ahead of `origin` until pushed. **Re-derive HEAD / sync at read-time** (`PROBES.md` P3). |

> **⚠ UPDATE — supplement FILLED (post-generation).** This bundle was generated **COLD** (CC-driven
> session-wrap audit, no outgoing browser architect), but the operator then `supplement filled` a
> rich architect **design-intent brief** — committed **verbatim** in `SUPPLEMENT.md` and folded
> (ANSWERS-only) into `PASTE_THIS.md`. Read the folded `SUPPLEMENT.md` as the **authoritative
> strategic *why*** of this handoff (the harmony-vs-frontier frame; the disposition lean-reversal;
> ADR-89 OQ1 as the keystone decision; the `claude -w` lessons). Two consequences: the §13(d)
> operator-context beat **NARROWS** to "anything changed since the supplement?" (it does **not** fire
> full), and the teeth probes (P2–P9) are **unchanged** (they bind to live state, which the fill does
> not touch). Read any "COLD / beat fires full / ANSWERS empty" phrasing below as **generation-time
> history**.

> **This bundle is COLD.** It was produced by a **CC-driven session-wrap audit** (no outgoing
> browser architect in the loop). `SUPPLEMENT.md` is committed with **empty ANSWERS** — the defined
> cold-handoff disposition (HANDOFF_PROCESS §13), not a missing deliverable. The §13(d)
> operator-context beat therefore fires **FULL** (nothing to narrow against). The strategic *why* of
> this session is **CC-derived and lives in `RESIDUAL.md`** (the next-ship plan + key rulings), since
> there was no browser-side deliberation to capture.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale
> lives **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the
> walkthrough. This file carries only the **session header** (above) + the **paste-pointer** (below).
> v5 bundles carry **no per-bundle README** (the 2026-06-12 canonical-runbook collapse —
> `HANDOFF_PROCESS.md` §13).

---

=== protocols/HANDOFF_BOOT.md ===

# HANDOFF_BOOT — thin browser boot (HANDOFF_PROCESS v5)
<!-- scope: meta -->

> **What this is.** The whole boot for a fresh browser (Claude.ai) chat. Paste this one
> file to start a session — it replaces the old multi-file bundle. Everything else is
> pulled just-in-time *via CC* (Claude Code holds the repo; you do not).
> Process: **HANDOFF_PROCESS v5** (canonical) — the live spec is `protocols/HANDOFF_PROCESS.md`,
> which CC holds; ask CC to pull any part you need.

## Core — these three lines are the boot. Read them first.

1. **Who you are.** You are the **critical architect** for this work. Claude Code (**CC**)
   is your junior: it holds the repo, runs the tools, and executes. You direct; it does.
2. **One rule.** Do **not** act unilaterally on anything the methodology governs — route
   through CC or ask. The methodology lives in the repo and is enforced mechanically; you
   *reference* it, you do not restate or reinvent it.
3. **First move.** Read **CC's handoff** (its residual + pointers + **drift-flags**). Do
   nothing else until you have it.

**On load, reply exactly:** `Booted as the Layer-1 browser under HANDOFF_PROCESS v5. Ready for CC's handoff.`
— so a partial or missing paste is visible (if you can't, say what's missing).

## Your operating role — execution mode (default)

You have **no file access** — CC is your hands on the repo. Your job is judgment, not
retrieval. (This is the **execution** posture; when CC's handoff names **architect mode**, use
the generative posture below instead — HANDOFF_PROCESS v5 §13.) Concretely:

- **Reactive partner + filter.** Surface only the errors and decisions that genuinely need
  human judgment; keep the operator at the feature / epic / user-story level. Do not relay
  routine CC output back to the operator — absorb it and act.
- **Research.** You do the open-web / cross-domain research CC cannot reach from inside the
  repo; bring back synthesized findings, not raw dumps.
- **Exception-handler.** When CC hits something the methodology doesn't cover, or a genuine
  fork, you adjudicate — or escalate to the operator with a recommendation, not a menu.
- **Launch-config support — genuine forks only.** Help choose model / effort / autonomy
  **only** when there's a real fork. Routine is already handled by CC's own `opusplan`
  (Opus plans, Sonnet implements) and auto mode (classifier-gated approvals). You do **not**
  review routine plans — only architecturally risky ones.

## Architect mode — generative posture

When CC's handoff names **architect mode** (a planning / define-the-way-of-working session),
your role shifts from the reactive filter above to a **generative, decompositional** posture.
The verification split, bidirectional adjudication, and plan-review contract below still apply.

- **Orient first — before any mechanism.** CC's handoff carries an *orientation probe*: an exact
  line to quote from `VISION.md` (`## Vision` — *what `.dev-knowledge` is*) and from
  `ARCHITECTURE.md` Chapter 1 (*where this work sits — Layer 2 of the three-layer model*). You
  have no files, so reply **"run `<command>`"**; CC reads the **live** file and substring-checks
  the quote. Do nothing else until you hold those two orienting lines — they cannot be bluffed
  from a summary, and that is the point.
- **Ask the operator for off-repo context — after orienting, before you decompose.** CC's handoff
  is repo-derived; it cannot carry operator intent or off-repo findings. Make **one** targeted ask:
  *"what off-repo context for this planning session — intent, priorities, findings not in the repo,
  changed decisions?"* This is **off-repo only** — do **not** re-narrate CC's residual (that is the
  repo-side "why"), and it is **not** the old heavy file-by-file interview, just the one ask.
  Architect mode only. (v5.2: when CC's paste carries the supplement's **ANSWERS**, its Q6 already
  captured this off-repo context at handoff time — narrow the ask to *"anything changed since the
  supplement was written?"* rather than re-asking it whole — but an **empty** supplement (a cold / cleared handoff) carries no
  answers, so ask the full question; `HANDOFF_PROCESS.md` §13(d), "(d)
  refined, not duplicated".)
- **Drive decomposition.** Turn the architecture work into the task-graph — what blocks what,
  what can run in parallel — and hand it back as residual + `BACKLOG.md` pointers. (The graph
  lives in the residual this pass; it is not yet a durable BACKLOG field — #156.)
- **Hand CC a build prompt as intent + mode + a thin governance-pointer — not the skeleton.**
  When a build task falls out of decomposition, emit *intent* + *closure* + *anti-patterns* +
  the *plan/auto mode* (with its basis) + a *thin governance-pointer* (the ADR/LESSONS/sibling-spec
  the task touches — CC won't self-infer it). CC owns the skeleton, code-impact context, generic
  gotchas, and model/effort, and self-loads them reliably for code-impact tasks; the **format
  stays in PLAYBOOK** — you carry the contract, not the form. Equilibrium contract: ADR-87 /
  PLAYBOOK §2 "Architect output vs CC consumption-spec".
- **Hold the whole-system view.** Keep the big picture and the `ARCHITECTURE.md` map in frame;
  do not collapse to a single ticket.
- **Surface design tensions proactively.** You are stress-testing the design, not just filtering
  CC's output — name the trade-offs and the open questions, escalate the genuine forks.

## Verification split (who checks what)

- **You verify the *artifact*.** With no file access, you check that CC's handoff is
  internally coherent and aligned with the architectural intent — fresh-eyes, file-free.
  Watch for two claims that can't both be acted on (a self-contradiction at the recency
  peak) and for a residual that reads plausibly but doesn't add up.
- **CC verifies *state fidelity*.** Claims vs live disk/git are CC's job — it runs the
  drift-checks and the forced primary-source read. If you need a fact confirmed against the
  repo, ask CC to verify it; don't assert it from the handoff alone.

## Adjudication is bidirectional

Correct CC's errors **and** pull missing context — not one-shot. If the handoff omits
something you need, ask CC to pull the primary source (it can; you can't). If CC's read of
state looks wrong, push back and have it re-derive from disk.

## Plan-review output contract (non-negotiable)

When you review a CC plan or proposal, emit **exactly one** of these — never prose the
operator has to translate into CC actions:

1. **The exact CC option to select** — e.g. `Select option 2`, or the verbatim answer to
   CC's question.
2. **Exact paste-ready English feedback** — the verbatim text the operator pastes straight
   into CC (no editorializing around it).
3. **A plain `approve`** — when the plan is sound as-is.

If your judgment doesn't reduce to one of these three, you are still thinking — finish, then
emit one of the three.

## Closing a session — definition of done

Plan with closure in mind from the start. The session-end Stop-gate (ADR-85) is
deterministic and **mechanically enforced** — the canon is `protocols/DEFINITION_OF_DONE.md`
(ask CC to pull it). The two load-bearing rules:

- **JOURNAL — hard.** A session that lands commits is **blocked from stopping** until its
  `JOURNAL.md` entry names ≥1 commit-SHA from this session. Not a nudge — a block.
- **BACKLOG — advisory (v1).** Landing commits without a structural-marker change in
  `BACKLOG.md` raises a nudge, not a block (it hardens later — ADR-85 R1).

The four other living docs (ARCHITECTURE/VISION/LESSONS/CONTRIBUTING) are *update-when-
materially-affected*, not per-session-gated. A wrong block exits **only** via CC running
`/override [reason]` (logged) — there is no auto-bypass.

---

=== RESIDUAL.md ===

# Residual — 2026-06-20 session-wrap audit handoff (the part the repo does not already encode)

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **COLD handoff** (CC-driven session-wrap audit; `SUPPLEMENT.md` committed empty — §13 cold
> disposition). The strategic *why* is CC-derived and lives in §3–§5 below, not in a browser
> supplement. The §13(d) operator-context beat fires **FULL**.
>
> **⚠ UPDATE — supplement FILLED (post-generation).** Generated COLD, but the operator then
> `supplement filled` a rich architect design-intent brief — committed **verbatim** in
> `SUPPLEMENT.md`, folded (ANSWERS-only) into `PASTE_THIS.md`. It is the **authoritative strategic
> *why*** (read it alongside §3–§5 here). The §13(d) beat **NARROWS** ("anything changed since the
> supplement?"); the drift-checks below are **unchanged** (live state, untouched by the fill). Read
> any "COLD / beat fires full / empty ANSWERS" phrasing as **generation-time history**.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py health` / `ship-gate`,
`validate_git_backlog`, `validate_doc_claims`, `validate_backlog`) at generation. **Re-derive each
at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ✅ HEADLINE — `ship-gate` is now GREEN (the inverse of the 2026-06-19 bundle)

The 2026-06-19 bundle's headline was `ship-gate` **RED**: two wrap commits (`3a894ee` journal-wrap,
`d0f9ead` transcript-archive) landed direct-on-`main` (FF/direct, core-invariant #5), holding the
`no_ff_merges` check RED. **That is resolved.** Both commits are **dispositioned** via sha-scoped
`ecosystem/disposition-register.yaml` entries (`warn-no-ff-3a894eeb5-journal-wrap`,
`warn-no-ff-d0f9ead67-transcript-archive`), and **#197** (the §4.4 ship-gate disposition decision)
is **closed** this session.

`python scripts/audit.py ship-gate` → **GREEN** — verification organs green against this arc
(**8 WARN dispositioned**).

### Other flags (benign / dispositioned — unchanged)

- `git_backlog_drift`: **#77** `[~~]` — the known voided-closure false positive (`77e5d7d` closes
  #77 but #77 is still in BACKLOG by design). Dispositioned (`warn-77-voided-closure`). **Do not
  touch** (standing false positive).
- `doc_rot`: history-accretion `[~~]` on BACKLOG#164 / #77 / #134 / #10 + CLAUDE.md section-history
  (21 entries). All dispositioned (`warn-doc-rot-*`). Grooming candidates (#140 family), not blockers.

> **Health vs ship-gate seam.** `audit.py health` still prints the two `no_ff_merges` as `[~~]`
> WARNs (health does not apply the disposition register the way `ship-gate` does — health gates each
> *commit*, FAIL-only). That is expected and not a regression; **`ship-gate` is the arc gate, and it
> is GREEN.**

### Surfaced this session — non-blocking, for the architect (NOT gated, NOT fixed here)

- **CLAUDE.md §11 "Recent ADRs (last 5)" is stale** — still lists ADR-76…80; live newest is ADR-89.
  Operator-deferred twice (CLAUDE §12 v2.17/v2.19). A proper fix is a **focused groom** (genuine
  end-to-end re-read + `last_reviewed` restamp + rotate to 85–89), not a drift-patch — left for that
  groom. (Not `doc_claims`-gated, so no gate flags it.)
- **`scan_undeclared_edges` precision** — the live scan reports **257 candidates / 106 weak**, but
  walks the whole working tree: immutable zones (handoff bundles, ADRs, audits, append-only logs)
  **and gitignored scratch** (`temp/`, the operator's personal files). #199 prunes immutable zones;
  whether the scan should also honor `.gitignore` is an open scope question (see §4). The raw count
  over-states the actionable set.
- **JOURNAL newest entry predates HEAD** — the dependency-arc consolidation commits (`c67a4d3` →
  `a07435f`, plus this session) are not separately journaled; git is the implementation record
  (CLAUDE §5). This session's own JOURNAL entry (written at wrap) reconciles it.

---

## §2 — Shipped state (the dependency-arc wave, verified live)

**Organ — each exists, tested, registered where it should be:**

| Component | Item | Tested | Registration | Status |
|---|---|---|---|---|
| `scripts/reverse_dep_oracle.py` | #193 (Track A) | `test_reverse_dep_oracle.py` | **NOT** in `ALL_CHECKS` (query TOOL, not a gate); inventoried in ARCHITECTURE | live, green |
| `scripts/scan_undeclared_edges.py` | #179 (FC2) | `test_scan_undeclared_edges.py` | **NOT** in `ALL_CHECKS` (awareness scan, writes nothing, exits 0); **now** inventoried in ARCHITECTURE (this session) | live, green |
| `scripts/validate_doc_structure.py` | #192 | `test_validate_doc_structure.py` | **IS** `ALL_CHECKS` #22 (`doc_structure`); inventoried in ARCHITECTURE | live, green |

**ADR statuses — verified live (not assumed):**

- **ADR-88** (file-oriented dependency management) — **Proposed**, NOT ratified. OQ1–OQ4 all open
  (FC-taxonomy completeness; #170 edge-model reuse; global/local contract; #181 data-gate). Its OQ2 =
  the **#170 issue↔commit edge** — a *distinct* edge, not ADR-89's.
- **ADR-89** (computed code-dependency edges) — **Proposed**. **OQ2 RESOLVED 2026-06-20 (#193)**
  in-file (the oracle's `reverse-dep-oracle/v1` provenance payload). **OQ1 (doc→code ID-scheme) and
  OQ3 (advisory→gate promotion) remain open** → stays Proposed.

**Green at generation:** `pytest` 738 passed / 1 skipped (**739 collected**) · `ruff` clean ·
`audit.py health` OK · **`ship-gate` GREEN** · `validate_backlog` OK (7 themes, 22 stories, **86
tasks**) · `doc_claims` 4/4 (checks 22/22, hooks 9/9 + roster, pytest 739/739) · `codemap-freshness`
Passed. (All are `PROBES.md` teeth — re-derive at read-time.)

---

## §3 — Next-ship action plan (prioritized, dependency-aware)

Status legend: **READY** = buildable now · **NEEDS-DECISION** = an architect/Council call gates it ·
**GATED** = blocked on another item. Parallel-safety is **derived** from the #156 durable task-graph
(no shared `serialize-group` + no `depends-on` path).

| # | What | Status | Gate / blocker | Parallel-safe with |
|---|---|---|---|---|
| **#195-2a** | Safe-removal gate **phase 2a** — a pre-commit/check that any deletion was accompanied by the reverse-dep check + a log entry (process gate) | **READY — highest build** | none: its gate (the oracle, #193) **shipped** | #199, #196 (distinct groups) |
| **#199** | Prune immutable zones from the undeclared-edge scan so the candidate list is actionable | **READY — buildable** | none: #179 shipped. Consider also pruning gitignored dirs (`temp/`) — new finding (§4) | #195-2a, #196 |
| **#196** | Closure-computation spike (**brief's OQ1**) — cross-artifact closure computation; design/research (plan-mode) | **READY — design spike** | none (plan-mode); it **gates #195-2b** | #195-2a, #199 |
| **#194** | Track B — doc→code declared edge (rule-IDs + structural integrity) | **NEEDS-DECISION** | **ADR-89 OQ1** (doc→code ID-scheme / rule-ID granularity — architect lean **clause-level, UNCONFIRMED**) | decide first; shares `code-edge` group with #195 once it builds |
| **#195-2b** | Safe-removal gate **phase 2b** — full closure-gate (zero external refs to the removal closure + green post-removal build) | **GATED** | the #196 closure-computation spike | — |
| **#153** | Pre-push direct-to-main / true-FF block — the mechanical FF-*prevention* | **READY — assess priority** | none. It is what stops future `no_ff_merges` (the exact class #197 was a symptom of) | independent (`audit-py` group) |
| **ADR-89 ratification** | Proposed → Accepted | **GATED (decision)** | OQ1 (doc→code ID-scheme) + OQ3 (advisory→gate). OQ2 resolved | — |
| **ADR-88 ratification** | Proposed → Accepted | **GATED (decision)** | OQ1 (FC-taxonomy) + OQ2 (#170 edge-model) + OQ3 (global/local contract) + OQ4 (#181 data-gate) | — |

**Recommended sequencing.** The three **READY** items (**#195-2a**, **#199**, **#196**-spike) carry
no shared blocker and sit in distinct serialize-groups (`code-edge` / `coherence` / none) → run them
**in parallel**. Resolve the **decisions** on a parallel track: **ADR-89 OQ1** unblocks **#194**;
the **#196** spike output unblocks **#195-2b**. **#153** is independent — prioritize it if preventing
the `no_ff_merges` recurrence (vs only dispositioning it after the fact) is the goal.

---

## §4 — Open decisions the next session must make

1. **Rule-ID granularity for #194** = **ADR-89 OQ1** (doc→code ID-scheme). Architect lean =
   **clause-level**, but **UNCONFIRMED** — an architect/Council decision *before* #194 builds.
2. **ADR-89 ratification readiness** — needs OQ1 (doc→code ID-scheme) + OQ3 (advisory→gate) resolved.
   OQ2 is already resolved (#193).
3. **ADR-88 ratification readiness** — needs OQ1–OQ4. At ratification, add the ADR-88→ADR-89 back-link
   (deferred per the immutability convention; ADR-89 already carries the forward link).
4. **#153 priority** — the mechanical FF-prevention (pre-push true-FF block). It stops the
   `no_ff_merges` class that #197 dispositioned after the fact; #153 also owns the unsettled
   `--no-ff` *scope boundary* (hub vs `~/.claude` vs child repos) and the methodology-reach question.
5. **Scan precision (new finding)** — should the undeclared-edge scan honor `.gitignore` (exclude
   `temp/`-style scratch) in addition to #199's immutable-zone pruning? Decides whether this is a #199
   scope-extension or a sibling micro-item. (Not filed — surfaced for the architect.)
6. **Conformance dashboard (#171)** — explicitly **deferred** this session (out of scope per the
   prompt). The #169 ungated-doc staleness signal rides it; depends-on #171.
7. **CLAUDE.md §11 currency groom** — rotate "last 5 ADRs" 76–80 → 85–89 in a focused groom
   (re-read + restamp). Twice-deferred; surfaced, not done here.

---

## §5 — Key rulings from THIS session (so they aren't re-litigated)

1. **#197 closed** — option **B** (sha-scoped disposition) landed → `ship-gate` GREEN; **C moot**
   (the wrap-workflow already mandates branch → `--no-ff` per core-invariant #5, verified live, so no
   direct-commit prescription remained to tighten); **A rejected** (architect lean B+C). The residual
   mechanical FF-*prevention* is owned by **#153**, not #197.
2. **ADR-89 OQ numbering (authoritative, read live from the ADR):** OQ1 = doc→code ID-scheme (open),
   OQ2 = oracle provenance payload (**RESOLVED #193**), OQ3 = advisory→gate (open). **#194's gate is
   ADR-89 OQ1** (was mislabeled "OQ3" — fixed this session). **#196's "(OQ1)" is the dependency-
   legibility *brief's* OQ1** (closure-computation — a *different* namespace; disambiguated to
   "brief's OQ1" this session so the two don't collide).
3. **ADR-88 OQ2 = the #170 issue↔commit edge** — a distinct edge; ADR-89 makes no claim on it. There
   is **no ADR-88 OQ6** (OQ1–OQ4 only).
4. **Organ registration is by design:** `reverse_dep_oracle.py` (query tool) and
   `scan_undeclared_edges.py` (awareness scan, writes nothing / exits 0) are **deliberately NOT** in
   `ALL_CHECKS`; only `validate_doc_structure.py` is a check (#22). The scan is now inventoried in
   ARCHITECTURE (parity with the oracle).
5. **PLAYBOOK/ESSENTIALS correctly omit the hub edge-model organ** — they are the *universal* protocol
   + 1-page cheat-sheet; the oracle/scan/linter + ADR-88/89 live in ARCHITECTURE (the map) + the ADRs.
   This matches the open **#77** direction (keep hub-only tooling out of the universal PLAYBOOK).
6. **Carried from the dependency arc (don't re-derive):** registry-only authority set;
   Tier-1+2 candidates / Tier-3 retained-and-enumerated surfacing; fail-soft breadth = gate-safe for
   #195; sha-scoped disposition is the accepted one-off mechanism.

---

## §6 — Pointers (read the source, never a copy)

- **Plan / task-graph:** `BACKLOG.md` (story-map; `code-edge` group = #194/#195, `coherence` group =
  #180/#181/#182/#199). Schema machine-checked by `scripts/validate_backlog.py`.
- **Doctrine:** `docs/decisions/ADR-88-file-oriented-dependency-management.md` (declared edge),
  `docs/decisions/ADR-89-computed-code-dependency-edges.md` (computed edge + OQ list).
- **Organ map / inventory:** `ARCHITECTURE.md` Ch2 (organ map) + §Validators (the `scripts/`
  inventory, incl. the new `scan_undeclared_edges.py` bullet).
- **This session's commits:** `git log --oneline` on `chore/session-wrap-audit` (close #197;
  ARCHITECTURE scan bullet; OQ-fix; this bundle).
- **Prior context:** `docs/handoffs/2026-06-19-dev-knowledge-architect/` (the bundle whose RED
  headline this session resolved).

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (v5 §5 + §13c)
<!-- scope: meta -->

> **⚠ UPDATE (post-generation) — supplement FILLED.** This bundle was generated COLD, but the
> operator then `supplement filled` real architect answers (now in `SUPPLEMENT.md`, folded into
> `PASTE_THIS.md`). The teeth probes (P2–P9) are **unchanged** — they bind to **live state**, which
> the fill does not touch. The only changes: the **§13(d) beat in P1's gate NARROWS** to "anything
> changed since the supplement?" (it does **not** fire full), and **P8's ANSWERS state is FILLED**
> (not empty). Read any "COLD / empty ANSWERS / beat fires full" phrasing below as **generation-time
> history**; read the folded `SUPPLEMENT.md` first.

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no
> answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** —
> surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live
> state at check-time**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks
> onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> The answers — the orienting lines, the check count + last name, the HEAD sha, the drifted `#id` +
> closing sha, the serialize-group membership, the counts, the dates — are deliberately **absent from
> this whole bundle**. That is what gives the probes teeth. Do not infer them; run the command.
>
> **This bundle is COLD** (CC-driven session-wrap audit; `SUPPLEMENT.md` committed with empty
> ANSWERS), so the §13(d) operator-context beat in P1's gate **fires FULL** — there is nothing to
> narrow against.

## P1 — Orientation (the architect's **first move**, before any mechanism — v5 §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC
reads live and substring-checks.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what `.dev-knowledge` is*. | `VISION.md` `## Vision` (line 11) | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits (Layer 2 of the ADR-28 three-layer model)*. | `ARCHITECTURE.md` `## Purpose [CORE]` (line 47) | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (v5 §13d):** the
browser asks the operator one targeted question for **off-repo** context (intent / priorities /
findings not in the repo / changed decisions). **This bundle is COLD** (empty ANSWERS), so the beat
**fires FULL** — there is no this-session supplement answer to narrow against.

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at this generation HEAD was `db61dd0`, the tree clean — but this handoff's own commit + `--no-ff` merge move HEAD and put `main` ahead until pushed; re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle — **expected: the standing `#77` voided-closure false positive, no more** | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, what does `pytest --collect-only` collect **right now**, and **do they match**? | `ARCHITECTURE.md` `**N collected**` (in the `tests/` validators bullet) + live pytest | the live count drifts on any test change; neither integer appears in the residual — **expected to MATCH (739/739)**, but the live count is the only ground truth and the pass test is "answered from the live source," not "matches a remembered number" | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — `audit.py health` does **not** isolate this; use the standalone |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, and **how many WARNs are dispositioned**? | live git ∩ `main` history ∩ `disposition-register.yaml` | **THIS is the §1 headline — the INVERSE of the 2026-06-19 bundle:** at generation `ship-gate` is **GREEN** (the two 2026-06-19 `no_ff_merges` wrap commits are now dispositioned; #197 closed; **8 WARN dispositioned**) — but the live answer is the only ground truth (a new direct-on-`main` commit would re-RED it), and the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present (and is its ANSWERS region empty or filled), and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count; the live bundle + spec are the only ground truth — **expected: no `README.md`; `SUPPLEMENT.md` present with ANSWERS EMPTY (this bundle is COLD); boilerplate lives once in `docs/handoffs/README.md`** | `ls docs/handoffs/2026-06-20-dev-knowledge-architect/` ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`s are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle — **expected: `code-edge` = #194/#195, `coherence` = #180/#181/#182/#199** | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — one off-repo ask, firing
   **FULL** (this bundle is COLD, empty ANSWERS) — before design. Then run P2–P9, each against **live
   state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P9 are *expected to move* between generation and check-time — that is the design. **P7 is
   the headline: expected GREEN** (the prior bundle's two undispositioned `no_ff_merges` are now
   dispositioned; #197 closed) — but the pass criterion is **"answered from the live source,"** never
   "matches the verdict the summary remembered." **P2** is expected to read **22** (last name
   `doc_structure`; #192 landed it as check #22). **P6** is expected to **MATCH** (739/739). **P8**
   pins the COLD four/five-file shape (`SUPPLEMENT.md` present, ANSWERS **empty**; no README). **P9**
   pins the now-durable serialize-group graph (#156).

---

=== SUPPLEMENT.md ===

# Architect design-intent handoff — dependency-legibility organ

> **What this is.** The v5.2 state-bundle (`docs/handoffs/2026-06-20-dev-knowledge-architect/`)
> captures *verifiable state* — what shipped, what's gated, the PROBES that bind it. This doc
> captures what the machinery **cannot** derive from the repo: the *design reasoning*. Read
> both. The bundle tells you where things are; this tells you **why**, and where the settled
> ground ends and your judgment begins.
>
> Frame: two layers. **The harmony** — settled decisions you inherit as given; do not
> re-derive them. **The frontier** — the open questions where you actually think. Most of a
> good handoff is being clear about which is which.
>
> State anchor: main @ `1c4663d`. Shipped: oracle (#193), refscan (#179), linter (#192),
> ADR-88/89 doctrine (both **Proposed**). #197 closed. #199 filed.

---

## 1. Strategic intent (the way-of-working goal — not a task)

**Give the organ teeth, then ratify it.** Right now the organ has *legibility* without
*enforcement*: the oracle (A) and the scan (C) **surface** dependency edges, but nothing yet
**stops** the silent-overwrite failure they were built to prevent. The oracle answers "what
depends on this" — but no gate consumes that answer to refuse an unsafe removal. So the
methodology goal is **Track D (safe-removal gate)**: turn the advisory legibility into an
enforced gate, *safely* — which is the same act as resolving ADR-89 OQ3 (advisory→gate
promotion). Legibility was this session; **teeth** is next.

Second: **ratify the doctrine.** ADR-88 and ADR-89 are still Proposed. The organ is currently
an experiment with a clear shape, not a ratified foundation. Completing the methodology means
the doctrine that *defines* the organ reaches Accepted — which gates on resolving the ADRs'
open OQs.

The deeper intent: **preserve the pattern this session established** while completing the
organ — declare-what-you-can't-compute / compute-what-you-can; advisory-first; closure-level
(not per-symbol) gating; and **dogfood the organ on its own corpus.** The pattern is the
inheritance; the remaining tracks are its application.

## 2. Tensions weighed — where I landed and why

1. **Recall vs precision (the scan).** Human-confirm makes false-positives cheap but
   false-*negatives* expensive (a missed edge = the staleness bug) — yet humans fatigue on
   noise. → **Tiered surfacing:** Tier 1+2 actionable, Tier 3 *retained-and-enumerated*
   below the line. Optimizes both: strong candidates get attention, weak signals stay
   auditable + promotable, **no silent recall loss.** This is the general pattern for any
   human-in-the-loop discovery surface.

2. **Registry-only vs all-specs (the authority set).** → **Registry-only.** The registry is
   the *declared* authority set — consistent with the thesis. "All specs" needs a fuzzy
   heuristic = a competing *undeclared* definition of spec-hood = drift; and it is
   self-contradictory to build the undeclared-edge scanner on an undeclared authority set.
   Growth lever = register more specs (the governed action). **The organ's own inputs must be
   declared.**

3. **Pyright vendoring (the oracle).** Reproducibility/fidelity vs repo-footprint purity. →
   **Local npm, pinned + gitignored.** For an oracle, **determinism is load-bearing** —
   ADR-89 mandates provenance precisely for auditability. The npm-pinned path is the *exact*
   benchmark-proven invocation (zero re-proving) and proves closure now; the pip-wrapper's
   `>=` floor + opaque bundled toolchain + *unproven* invocation eroded the determinism that
   justifies the oracle. Footprint cost (a node manifest in a markdown repo) is **tooling, not
   content** — acceptable.

4. **Disposition (A) vs push-past (B) for the ship-gate RED.** → **Disposition, sha-scoped.**
   And note: **I reversed my own filed lean** (was "B+C, reject A"). Live evidence falsified
   the framing — the RED was *recurring* (carried across multiple ships), not a one-off, so
   push-past had already eroded the gate; and #197's own done-when ("gate no longer RED")
   *requires* A, which B can't satisfy. **Update leans when live evidence contradicts them.**
   A safety gate that is permanently overridden is worse than one made honestly green.

5. **Prose-gating vs declared depends-on edges (the backlog reconcile).** → **Prose+refs**
   (matched #180/#181 precedent) — it's a filing, not a design decision, and phased gating
   (2a→A, 2b→spike) doesn't map to one item-level edge. **But** I flagged the dogfooding
   tension (the dependency-legibility project encoding its *own* task-gating as undeclared
   prose) as an open question, not a filing change. Don't smuggle design into filings.

6. **Universal PLAYBOOK vs hub-specific organ** (CC corrected my framing here). → The organ
   is **hub-specific tooling**; PLAYBOOK is the **universal** methodology; hub-specific lives
   in ARCHITECTURE + the ADRs. Documenting the organ in PLAYBOOK would wrongly universalize
   it (matches #77's direction). **Internalize this boundary** — it will come up every time
   you're tempted to "document the new thing in the PLAYBOOK."

## 3. Considered + rejected — do NOT relitigate

- **Custom code graph / codemap** for code→code — rejected; the benchmark proved Pyright
  suffices. Don't rebuild it.
- **All-specs authority set** — rejected (fuzzy/self-contradictory).
- **All-tiers / Tier-1-only** surfacing — rejected (flood vs miss).
- **pip-wrapper / global Pyright** — rejected (reproducibility/fidelity).
- **Push-past-RED as the gate resolution; a blanket "direct-commits OK" waiver** — rejected
  (disposition was sha-scoped, narrow).
- **Documenting the organ in PLAYBOOK** — rejected (hub-specific ≠ universal).
- **Auto-declaring edges in the scan** — rejected; **the human confirms every candidate.**
  This is the load-bearing safety rule of the scan — never weaken it.
- **Parallelizing tiny follow-through tasks** — rejected (worktree overhead > benefit).
- **Reopening #197 for mechanical FF-prevention** — rejected; that's **#153's** scope.
- **Closing #5/#77** — never; they cite the #167-misattribution and are standing
  false-positives.

## 4. Open questions — unresolved or deliberately deferred

- **ADR-89 OQ1 — doc→code rule-ID granularity** (clause vs heading vs file). **Gates Track B
  (#194).** My lean: **clause-level** (impl = a callable or a file-constant). **UNCONFIRMED.**
  This is *the* decision that unblocks the declared-edge half — likely worth a Council debate
  or a deliberate architect call, not a snap pick.
- **ADR-89 OQ3 — advisory→gate promotion.** The meta-question for the *whole* organ: by what
  criteria does an advisory edge-check earn the right to *enforce*? This is **intertwined with
  Track D** — the removal-gate *is* an advisory→enforced promotion. Resolve OQ3 and build D
  together, not separately.
- **ADR-88 OQ1–OQ4 — all open** (incl. OQ2 = the #170 issue↔commit edge). ADR-88 ratification
  gates on these.
- **Closure computation (#196 spike; the brief's OQ1)** — how to compute a removal *closure*
  across heterogeneous artifact kinds (tests→symbols, config string-refs, cross-language).
  **The hardest unsolved piece.** Gates Track D-2b. Attack it early to de-risk D.
- **Scan precision scope** — the refscan walks **gitignored temp/scratch** (a real bug CC
  surfaced) plus immutable-zone noise (#199). Where's the precision boundary?
- **Dogfooding gap** — should the organ's *own* task-gating be declared edges (not the
  prose+refs I filed)? Deferred.
- **#153 priority** — the mechanical pre-push direct-commit/FF block (the recurrence-prevention
  #197 delegated). Cheap, high-leverage; I'd elevate it.
- **Deferred by scope:** dashboard (#171); CLAUDE §11 stale-ADR groom.

## 5. Decomposition rationale — what NOT to redo vs what to decide fresh

**Why this shape.** The tracks are not arbitrary — they are the *distinct edge populations*.
The architect consolidation found that the original brief (code-coupled edges) and the 06-19
supplement (prose-internal + structure) cover **complementary, near-non-overlapping** edge
populations; **the organ = their union.** Each population needs its own mechanism:
- **A (code→code) computed** — Pyright. Shipped first: it's the keystone (settles ADR-89 OQ2,
  and Track D-2a depends on its oracle).
- **C (prose) shipped in parallel** — independent of A (different file surfaces).
- **B (doc→code) declared** — gated on the rule-ID granularity decision (OQ1) *because the
  ID-scheme shapes the entire mechanism; building before deciding = rework.*
- **D (removal-gate) phased** — 2a (process-gate, uses A's oracle, doable now) vs 2b
  (closure-gate, gated on the #196 spike) *because the closure computation is the hard unsolved
  piece — split the doable-now from the research-gated.*

**Do NOT re-decide (the harmony):** the track decomposition; the declare-vs-compute assignment;
Track A's oracle design (Pyright + provenance v1, OQ2 resolved); Track C's scan/linter; the
Fork-1/Fork-2 calls; the disposition; the A-first / B-gated / D-phased sequencing.

**DECIDE fresh (the frontier):** OQ1 (→ unblocks B); OQ3 (→ shapes D's enforcement); the #196
closure-computation design (→ unblocks D-2b).

## 6. Off-repo context

- **The disposition lean-reversal** (Q2.4) — the repo shows the final disposition; it does
  *not* show that the backlog item's recorded lean was "B+C, reject A." If you see that and
  wonder: it was correctly *superseded* at the decision point by live evidence. Don't reopen.
- **OQ-numbering hygiene** — the dependency-legibility *brief* numbered its OQs in a namespace
  that collided with ADR-89's. CC fixed the in-repo references; the standing lesson: **read the
  ADR's actual OQ numbers; never trust a brief's labels.**
- **Priorities (my read):** (1) **Track D-2a** is the highest-ready build — oracle shipped,
  gives the organ teeth. (2) **OQ1** is the highest-leverage *decision* — unblocks B. (3) the
  **#196 closure-spike** is the hardest — start it early to de-risk D-2b. (4) **#153** is cheap
  recurrence-prevention worth elevating.
- The **universal/hub-specific boundary** (Q2.6) — carry it; it's not written as a rule
  anywhere portable.

---

## Handoff-process meta — what worked, what didn't, what was missing

- **Worked:** the v5.2 bundle pattern — PASTE_THIS + **PROBES that bind live** (10/10) +
  RESIDUAL §3 plan / §4 open-decisions. The PROBES are the strength: they force the next
  session to *verify state*, not trust the summary. Keep that.
- **The gap:** the machinery captures **verifiable state** well and **design intent** not at
  all. The *why* — trade-offs weighed, options rejected, strategic intent, lean-evolutions —
  is not derivable from the repo; it lives in the outgoing architect's head and **must be
  written by hand.** This document is that missing layer. **Methodology improvement: the
  handoff bundle should carry a design-intent section (these 6 questions) as a first-class
  artifact, filled by the architect — not just the CC-generated state-bundle.** Without it, a
  successor re-derives settled trade-offs or, worse, relitigates rejected options.
- **Also weak:** the bundle records final state, not **decision evolution** (e.g. the B+C→A
  flip). A successor seeing a backlog lean that contradicts the shipped decision has no way to
  know it was a *reasoned supersession*. The intent layer must carry evolutions.

## The `claude -w` worktree lessons (→ #198; candidate for the lessons skill)

These recurred enough to be real, not anecdotal:
- `claude -w <name>` is the **one-verb** primitive (don't hand-roll `git worktree add`). It
  creates the worktree **and** a placeholder branch `worktree-<name>`. **Cleanup must delete
  both** (the work branch *and* the placeholder).
- **Parallel worktrees always collide on the 2nd `--no-ff` merge** on (a) `JOURNAL.md` — each
  journals → **keep both entries, newest-first**; and (b) any **shared additive claim** — both
  bumped `pytest_collected` to *different local values*, neither equal to the merged total →
  **reconcile to the live combined number, never assume.**
- The two CC instances named their work branches **inconsistently** (one committed onto the
  placeholder, one made a `feat/` branch). **#198 should codify the convention.**

These belong in **#198 (claude -w lifecycle)**, already filed. Whether to also write them to the
lessons/gotchas skill is a next-session call — not urgent; #198 is the owner.

## What remains to complete the methodology (your read was right — and here's the full set)

You saw it on the diagram: **Track B and Track D** remain. Confirmed — and the complete set is:

**Build (the unshipped edge organs):**
- **Track B (#194)** — doc→code declared edge. *Decision-gated* on OQ1 (rule-ID granularity).
- **Track D (#195)** — safe-removal gate. **2a is ready now** (oracle shipped); **2b is gated**
  on the #196 closure-spike.
- **#196 closure-spike** — the hard cross-artifact closure computation that D-2b needs.

**Doctrine (still Proposed — the organ isn't yet a ratified foundation):**
- **ADR-88 ratification** — OQ1–OQ4 all open.
- **ADR-89 ratification** — OQ1 (rule-ID granularity) + OQ3 (advisory→gate) open.

**Enforcement (the teeth):**
- **ADR-89 OQ3 — advisory→gate promotion.** The organ is advisory-first; making it *enforce*
  is the point of Track D. This + Track D are one problem.

**Hardening:** #153 (mechanical FF-block) · #199 + the gitignored-walk scan-precision gap.

**Deferred:** dashboard (#171) · CLAUDE §11 groom.

So: **the organ is half-built (A + C shipped; B + D + the spike remain) and the doctrine is
unratified.** "Complete" = build B + D + spike, give the organ teeth (resolve advisory→gate),
ratify ADR-88/89. That is the road. The map is in RESIDUAL §3; the *why* is here.

---

*Inherit the harmony. Think only at the frontier. The pattern holds — apply it.*
