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
