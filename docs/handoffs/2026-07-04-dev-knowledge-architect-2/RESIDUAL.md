# Residual — 2026-07-04 architect handoff (#2) — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **This is the SECOND architect handoff of 2026-07-04.** The first (`c185c09`,
> `docs/handoffs/2026-07-04-dev-knowledge-architect/`) closed [#244] P1→P4 and had its supplement
> **filled** (`0684174`) — the operator's answers **re-sequenced the whole program** around
> **deployment · sandbox · tests**, ruled **P5/P6 WAIT**, and set the phase order **Phase 0 (safety +
> self-honesty) → Phase 1 (build the sandbox as the retroactive acceptance instrument for P1–P4) →
> Phase 2 (fleet re-gated)**, with the rot-algorithm **deferred-until-after-sandbox**. **This window
> executed into that program.** Read the prior bundle's filled `SUPPLEMENT.md` — it is the strategic
> frame this residual sits inside, and it is NOT re-narrated here.
>
> **The delta this window = four lanes, all merged to `main`:** (1) ARCHITECTURE currency re-read,
> (2) RF-2 hub self-arm, (3) the handoff-generator (anti-bluff made structural), (4) **lived-workflow
> sandbox Slice A — STOP at the review gate.** **The next session's PRIMARY job is the Slice A review**
> (§4.1).
>
> **`SUPPLEMENT.md` is generated EMPTY** — the operator fills it from the outgoing architect chat
> (`supplement filled`) or leaves it empty for a cold handoff (§13 disposition). Until filled, the
> incoming §13(d) operator-context beat fires **FULL**.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate outputs);
> `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved — the load-bearing
> ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**, on branch
`docs/2026-07-04-architect-handoff-2` off `main` `a523fca`, tree clean, in sync with `origin/main`).
**Re-derive each at read-time via `PROBES.md`** — the teeth are there, not in trusting these lines. Per
the ratified RF-1 corrective, the bluffable values (the GREEN/RED verdict, the dispositioned count) are
**withheld here and obtained live via P7**; only the *named, structural* standing flags are listed.

### ✅ HEADLINE — the gate carries **only the standing dispositioned set; no new regression this window**

`python scripts/audit.py ship-gate` (**run it — P7**) returns the verification organs against the `main`
arc. The dispositioned WARNs are the **same standing set** as the prior handoff — this window added no new
drift class:

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but #77
  stays in BACKLOG by design — operator ruled keep-open). Dispositioned (`warn-77-voided-closure`).
  **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits — **expected seam, not a
  regression.** **#210** (open) proposes converting this class to a standing rule.
- `undeclared_edges`: **6** `…→handoff-process` prose edges (`BACKLOG.md`, `VISION.md`,
  `AI_COUNCIL_PROCESS.md`, `ESSENTIALS.md`, `PLAYBOOK.md`, `SESSION_SETUP.md`) dispositioned under
  **#241**. **The carried Fable coherence-spine review (RF-4) argues these 6 are major-granularity edges
  mis-served by an `@5.3` remedy — a §4 decision, unchanged.**

### One `ALL_CHECKS` change this window (structural, not a drift)

- `ALL_CHECKS` **grew by one** — RF-2 added **`hooks_armed`** (the hub self-arm check). The count and the
  last-registered check **name** are the live answer to **P2** (withheld here). The `doc_code_coverage_drift`
  guard reports **all** members covered (annotated or exempt) — no coverage escape.

### Two non-blocking informational legs (by design — not WARNs)

- `deployed_methodology_version` for **.dev-knowledge** = `unset` (`[--]`) — the hub **is** the methodology
  source; its own entry stays null. **ai-council** records **`1.2.0`** (unchanged this window — no new deploy;
  P6 fleet still held). corp-monorepo / corp-ops / corp-sca-time-automation still `null`.
- `enforcement_coverage` (`[--]`) — read-only, never FAIL/WARN; per-consumer truth is the `--fire` test.

_(No `[stale]` disposition — witnessed. Verify via P7; do not trust this line.)_

---

## §2 — Shipped this window (prior `-architect` bundle `c185c09` → now) — the map, not the narration

Pointer-first (`git log --first-parent c1454e4..HEAD`, `JOURNAL.md` top 2 entries). **All on `main`
(`a523fca`)** — every lane merged `--no-ff`; nothing left on a feature branch. **recall/inferred** from the
window; re-derive load-bearing values via `PROBES.md`.

**Four lanes landed (the sealed backdrop — do NOT redo):**

- **(1) ARCHITECTURE 2026-07-04 currency re-read** (merged `fbf88ae`; `docs/architecture-currency-2026-07-04`):
  cleared the **coherence-spine review's "demonstrated self-blindness"** — `undeclared_edges` is now
  confirmed live in `ALL_CHECKS` (not just asserted by the review), the omitted **`roster-freshness`** gate
  was added to the ARCHITECTURE inventory, and `last_reviewed` was **honestly re-stamped** after a genuine
  end-to-end read. This resolved the dirty-tree precondition the sandbox lane needed. (Operator change #1.)
- **(2) RF-2 hub self-arm + `hooks_armed`** (merged `2e7b072`; Fable arch review §4 — *the sandbox's own
  precondition*): `scripts/arm_hooks.py` (idempotent / fail-soft SessionStart self-arm) + a new
  `audit.py::check_hooks_armed` that resolves the hooks dir via `git rev-parse --git-path hooks`.
  **`ALL_CHECKS` 28→29.** **Demonstrated live:** delete `pre-push` → `audit.py health` goes **DEGRADED**.
  The redundant `core.hooksPath` (= default) was unset per operator so `pre-commit install` works normally.
- **(3) The handoff-generator lane** (merged `9d5ebe5`; `feat/handoff-generator`; [#164] RF-2 / [#161] /
  [#163] — **NOT closed**): built `scripts/gen_handoff.py` (assembles a valid v5 bundle from **committed**
  state) + `templates/handoff/v5/{PROBES,HANDOFF_BOOT,RESIDUAL}.md.tmpl` + a size-warn on
  `assemble_paste.py`. **The load-bearing win: the anti-bluff RF-1 fix is now STRUCTURAL, not
  hand-discipline** — the `/expected[ :]/`→FAIL rung rides `verify_handoff_probes._classify` (row-scoped;
  live 07-04 bundle passes 10/10, historical 06-25 fails 6 in isolation, ship-gate `handoff_probes` stays
  GREEN because the deployed check reads only the latest bundle). Answer-hint VALUES now go to a
  **JOURNAL-draft on stdout**, never a browser-visible file — so the `expected:` erosion (0→peak-5 across
  06-20..07-03) **cannot silently return**. **Zero `scripts/audit.py` edits** (stayed file-disjoint from
  the sandbox lane).
- **(4) Lived-workflow sandbox Slice A** (merged `a523fca`; `feat/lived-sandbox-slice-a`; **[#252]**;
  scaffold `ac3461c` + Codex fixes `ad719b9`): `deploy/lived_sandbox/` — an isolated `claude -p` **spawn** +
  clone/teardown + the **isolation proof**. **Correctness property PROVEN empirically + via the module:**
  SessionStart hooks DO fire under `claude -p` headless on Windows; `CLAUDE_CONFIG_DIR` governs user-level
  hooks (sentinel present-configA / absent-configB, both exit 0). **Codex review** (gpt-5.5 high,
  `docs/audits/2026-07-04-codex-lived-sandbox-slice-a.md`) found **2 CRITICAL + 2 HIGH — all fixed + tested
  + isolation re-PROVEN** (false-green exit-gating; teardown blast-radius anchored to system-temp;
  `extra_env` can't override protected keys; subprocess→`SandboxError`). Module suite 16 passed / 1 skipped;
  full suite 1210 passed / 1 skipped / **1 failed = the pre-existing [#251] only**. **STOP at the Slice A
  gate** — the whole point of the lane (§4.1).

**Also logged (not built):** **[#251]** — a pre-existing deploy-CLI success-render red (`record_branch`
dropped; stale-test-vs-regression TBD), captured `f62d4f4` so the sandbox suite's "1 failed" is a known
quantity, not a new break.

**Carried, unchanged this window (the prior bundle's real work — still the next session's load):** the
**four Fable read-only reviews** (handoff-adoption / coherence-spine / rot-algorithm design / Fable-5
architecture review) are all merged and **none acted on**. RF-1 (anti-bluff) has now advanced *structurally*
(lane 3) but its **spec re-ratification + first bluff-dogfood-rerun are still owed** (§4.2). See the prior
`RESIDUAL.md` §2/§4 for their full statement — not re-narrated here.

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** — **7 themes, 23 stories, 109 tasks** (witnessed via `validate_backlog`;
  +2 vs the prior bundle = the new **[#251]** deploy-CLI red + **[#252]** sandbox epic). The `[#244]` epic
  records **P1/P2/P3/P4 SHIPPED**, **P5/P6 remaining (WAIT per operator)**. The spec; items are tickets.
  Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (all window work integrated), this handoff
  branch `docs/2026-07-04-architect-handoff-2`, and `automation/fleet-audit` (a routine baseline branch,
  unmerged — separate concern, **leave**). **No unmerged feature branch this window** — the sandbox +
  handoff-generator lanes already merged. No merged stragglers to `-d` beyond what `/ship` will handle.
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the serialize-groups
  (verify via `PROBES.md` P9). This window's new groups: **`sandbox` = [#252]**, **`deploy` = [#251]**;
  the audit-py / coherence / code-edge groups are unchanged from the prior bundle. Open the file for
  placement of the new follow-ups.

---

## §4 — The next frontier (open architecture decisions)

**The next session is a REVIEW-then-BUILD session gated on one thing: the Slice A foundation.** The
[#244] build epic is sealed (P1–P4, P5/P6 held); the operator's re-sequenced program (prior supplement) put
the **sandbox** as Phase 1 — the retroactive acceptance instrument for everything already shipped — and this
window delivered its **Slice A** to a STOP gate. Everything else is carried and sequenced *after* that gate.
**recall/inferred** — the outgoing chat's strategic *why* fills `SUPPLEMENT.md`.

### (1) PRIMARY — review the lived-workflow sandbox Slice A, then build Slice B ([#252])

This is the session's reason to exist. Slice A is the **spawn + isolation foundation** for the episodic
lived-workflow harness (the operator's continuous-conformance instrument). It is **built, Codex-hardened,
and STOPPED for architect review** — autonomous progression past the gate was deliberately withheld.

- **The review:** adjudicate `deploy/lived_sandbox/` (spawn / clone / teardown / isolation proof) +
  `docs/audits/2026-07-04-codex-lived-sandbox-slice-a.md` (the 2 CRIT + 2 HIGH, all fixed). Is the isolation
  contract sound — `CLAUDE_CONFIG_DIR`-governed hooks, system-temp-anchored teardown blast-radius, protected
  env keys, exit-gating not false-green? Is the abstraction the right seam for Slice B to build on?
- **On approval — build Slice B** (the sandbox's actual acceptance value, from the prior "Next"): the
  **OUTER deterministic observer** + the **`engages:`-spec oracle** (essence-spec as the pass/fail source)
  + the **six-hook arc** + **seeded-EXPECTED-BUT-SILENT closure** (inject a should-fire-but-doesn't organ,
  prove the harness catches the silence). Opus, plan-first. This is what makes the sandbox a *retroactive
  acceptance instrument for P1–P4*, not just a spawn wrapper.
- **Live security flag from the Slice A session (act before/independently):** an `ANTHROPIC_API_KEY` was
  printed into this session's **local transcript** via a `${KEY:-}` bash bug (local only — not committed,
  not external). **Rotation recommended** (the harness reads the key fresh each spawn, so a rotate is
  cheap). Gotcha logged (`~/.claude/skills/gotchas/gotchas.md`, `${VAR:-}` secret-leak entry).

### (2) Integrate the handoff-generator's DEFERRED spec arc (this window created the debt)

Lane 3 shipped the generator + the structural anti-bluff fix but **deliberately deferred the spec
reconciliation to the architect at serial integration** (operator ruling Q1), because it collides with
**sandbox-owned `ARCHITECTURE.md`** and touches freshness-gated CLAUDE/ARCHITECTURE. Owed:

- **HANDOFF_PROCESS §5/§13 additive reconciliation to RF-1 "option b"** (the structural withhold) + the
  **`5.3 → 5.4` version bump** + **5 `reconciled_with` re-stamps** (the coupled surfaces the version bump
  forces atomic). Fold into an ARCHITECTURE-currency pass so the freshness gate rides the content commit.
- **Adjudicate [#164]'s formal BACKLOG disposition:** RF-2 slice + RF-1 "option b" are **done**; cross-repo
  probe sets + v4-prose removal remain open (both ADR-83-gated). [#161]/[#163] similarly partial.
- **Reconcile the shared `ecosystem/doc-counts.md` `pytest_collected`** once, after all test-adding branches
  are integrated (this window's suite grew; regenerate, don't hand-edit).

### (3) Route the four carried Fable reviews (RF-1 now half-done — finish it)

All four landed in the *prior* window and remain the meaty methodology work. Priority order (RF-1 changed):

- **RF-1 (handoff-adoption) — the STRUCTURAL fix landed (lane 3); the DOCTRINE half is still owed.** The
  operator re-ratified withholding and `verify_handoff_probes` now enforces it, but §5/§13 has not been
  amended to say so (that is item (2) above) **and the first bluff-dogfood has still not re-run since
  2026-06-11 promotion.** Close both to actually retire RF-1.
- **RF-3b — the boot-transcript echo that could close #159 on evidence** (cheap; a 12-supplement-old
  unclosable ticket).
- **Coherence-spine RF-5 FAIL-trap + the residual self-blindness** — the ARCHITECTURE re-read (lane 1)
  cleared the *demonstrated* self-blindness, but **RF-5 (the two doc↔doc walkers disagree on corpus scope)
  is a live correctness bug**, unfixed.
- **RF-4 — CLAUDE.md §5 "handoffs immutable" vs the §13 fill/fold lifecycle.** Standing doctrine
  contradiction; reconcile to the ADR-94 status-line-mutable precedent or carve a §13 exception.

### (4) Held + carried (do NOT advance without an explicit operator unlock)

- **P5 (`#130` hub self-prune) → P6 (`#221` fleet roll n=2+): still WAIT** (operator rule from the filled
  supplement — do not onboard n=2+ through a moving corpus while RF-1/RF-4 and the sandbox are in flight).
  P6 stays gated on **#225** (surgical precommit carrier) + FU **#250** (codemap-freshness component).
- **The rot-algorithm / continuous-conformance build: defer-until-after-sandbox** (operator rule — the
  sandbox and the rot-report share the observer machinery; build the sandbox first, then the rot-report on
  top). The Fable design (`docs/audits/2026-07-04-rot-algorithm-design.md`) stays a landed design, not a
  filed build, until the sandbox proves the shared primitives.
- **Standing debt — ai-council `CLAUDE.md` A2-stale (off-repo, LIVE):** `last_reviewed` < last edit; the
  now-**deployed** `canonical_freshness` gate **WILL block ai-council's next real commit** until a **genuine
  re-review + re-stamp** (never a faked stamp) — the transferred organ dogfooding itself in a consumer.
- **Smaller adjacent (unchanged):** `#220` MODIFY/semantic-drift axis (presence ≠ currency — verify-first
  whether any organ gates a meaning-change-without-version-bump), `#242` ADR status-flip coherence, `#210`
  journal-wrap no-ff standing rule, `#243` the #168-hard vs Fable-WARN JOURNAL-leg conflict.

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **The strategic frame (READ FIRST — it is the program this residual sits inside):** the prior bundle's
  **filled** `docs/handoffs/2026-07-04-dev-knowledge-architect/SUPPLEMENT.md` (the re-sequenced
  deployment · sandbox · tests program, P5/P6 WAIT, phase order) + its `RESIDUAL.md` §4 (the four Fable
  reviews in full — not re-narrated here).
- **The Slice A review input (§4.1 — the PRIMARY):** `deploy/lived_sandbox/` (the package),
  `tests/test_lived_sandbox.py` + `tests/fixtures/lived-workflow/`,
  `docs/audits/2026-07-04-codex-lived-sandbox-slice-a.md` (the 2 CRIT + 2 HIGH review),
  `JOURNAL.md` top entry (the program-session Did/Result/Next).
- **The handoff-generator (§4.2):** `scripts/gen_handoff.py`, `scripts/verify_handoff_probes.py` (the
  `_classify` anti-bluff rung), `templates/handoff/v5/*.tmpl`, and `protocols/HANDOFF_PROCESS.md` §5/§13
  (the spec to reconcile + version-bump).
- **RF-2 hub-arm (§2 lane 2):** `scripts/arm_hooks.py`, `audit.py::check_hooks_armed`, `.claude/settings.json`.
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook), `protocols/ESSENTIALS.md`, `CLAUDE.md`
  — referenced by pointer, enforced mechanically (§3), never re-narrated.
- **The four Fable reviews (carried adjudication input — §4.3):** `docs/audits/2026-07-04-*.md`.
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.
