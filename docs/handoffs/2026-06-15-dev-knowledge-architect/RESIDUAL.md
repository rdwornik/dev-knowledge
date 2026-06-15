# Residual — 2026-06-15 session, **architect mode** (v5 canonical §13)
<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — and this time the
> headline is **clean** (§1). Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md`
> and the now-**durable** serialize-group graph (#156 shipped), not re-narrated IDs. Generated from
> inside the repo at HEAD `ea9f190`, working tree clean, `main` **in sync** with `origin/main`.
> Re-derive HEAD/sync at read-time (P3).
>
> **Provenance — reconstructed, not witnessed-live.** This session was `/clear`ed immediately before
> the handoff, so there is **no live session reasoning** to transmit. The planning "why" below is
> **reconstructed from the repo** — JOURNAL (last ~8 entries), BACKLOG, the 2026-06-13 `-architect`
> bundle, and today's `2026-06-15-dev-knowledge-session` bundle (whose §2 embedded the architect
> brief verbatim — the richest source of the planning judgment). State facts (§1, §5) are
> **witnessed** (verified live at generation); design framing (§2–§4) is **recall/inferred** from
> those sources — verify against the live BACKLOG (§5), do not trust the re-narration.
>
> **Scope — a fresh handoff at an arc boundary, not a refresh.** Unlike 2026-06-13 (an honest
> carry-forward "no design move landed"), the state has moved **decisively** since: the entire
> 2026-06-13 Q-set is largely **resolved** (§3 "Resolved-since"). The modularization arc closed; two
> Council-bound design threads are queued. Orient first (`PROBES.md` P1), **then ask the operator for
> off-repo context** (§13d / #159), then resume the design.

---

## 1. Drift-flags — the headline (this time: clean)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus CC's
state read at generation. **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (18/19 pass; the one `[~~]` below is informational — health exits OK). Re-derive at
read-time (P3/P4/P7).

### CLEAN — `main` is **in sync** with `origin/main`; `no_ff_merges` is **OK** *(the two prior bundles' headlines are both gone)*

The 2026-06-13 `-architect` bundle's headline was a `main↔origin/main` **divergence** (ahead 3 /
behind 1); today's `-session` bundle's headline was an **ahead-8 origin gap**. **Both are resolved.**
`git status -sb` reports a bare **`## main...origin/main`** (no ahead/behind) at generation — the
2026-06-15 push reconciled the gap. And `no_ff_merges` reports **OK** ("no non-merge commits on main
since 2026-06-15"), because **ADR-84 (automation-writer isolation, 2026-06-14)** moved both unattended
writers off `main` (`automation/fleet-audit` local-first + `automation/conformance-digest` on origin)
and removed the `no_ff_merges` exemption — so the **Q9 collision is resolved by design, not carried**.

- **Confirm:** `git status -sb` (in sync) + `python scripts/audit.py health` (the `no_ff_merges` line).

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable — carried)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still present
(open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77
  legitimately stays open. Direction-(a) #90a structurally cannot distinguish a misattributed
  closure from a real one; only arc-content inspection (**#139** / direction-(b)) can.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py`.

### OPERATIONAL ALERT — last night's **nightly may have silently skipped** *(not a drift-flag; an ADR-84-pipeline reliability signal — operator look owed)*

The SessionStart surfacing reported: the expected digest `docs/audits/2026-06-15-conformance-nightly-digest.md`
is **NOT** on the `automation/conformance-digest` branch — *"last night's nightly may have silently
skipped (no retry)."* This is the cloud-Routine conformance pipeline (ADR-84). **Not a way-of-working
design question; an operator check** — was the 2026-06-15 Action run skipped/failed, and does the
no-retry posture want hardening? Surfaced so it is not lost. **Confirm:** the GitHub Actions run for
`nightly-conformance-triage.yml` + `git log --oneline origin/automation/conformance-digest`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The theme shifted — the machinery is (almost) done; the design threads are the work.** The
2026-06-12/06-13 architect theme was *"finish the v5 handoff machinery deferred at the #149 flip."*
Since 2026-06-13 that theme **largely landed** [witnessed via JOURNAL + audit state]:

- **#163 — teeth validator shipped** (`scripts/verify_handoff_probes.py`, merged `dba11d0`
  2026-06-13; now `audit.py` check #19 `handoff_probes`, resolve-only). The manual probe-gate every
  prior bundle leaned on is now **mechanically enforced** on the active bundle.
- **#156 — durable task-graph shipped** (BACKLOG schema carries `serialize-group` / `depends-on`,
  enforced in `validate_backlog.py`) **and ADR-66 ratified 2026-06-14** (operator authority, Path A).
- **Q9 — resolved by ADR-84** (automation-writer isolation): both unattended writers moved off `main`;
  the `--no-ff`-universal × ADR-80-automation-writer collision is closed by design.
- **PLAYBOOK Move 1 pointerized** (#152 + #158): 4 of 5 playbook-cluster tasks left the serialize-group;
  the token-log cadence relocated to `HANDOFF_PROCESS §14`. PLAYBOOK 3288 → 3211 lines.
- **Collision graph encoded** (2026-06-14): 34 tasks annotated across 9 serialize-groups; the
  parallelizable surface **re-measured on real data** (hub-internal N = 9). #167 / #166 filed.

**What that re-measure decided — don't build hub delegate-mode** [recall, from today's `-session`
§2 brief]. The data-grounded NO: *capacity ≠ demand.* The backlog's independent epics are sporadic
periphery; the sustained work (handoff / playbook / audit) lives in **contended-core serialize-groups
that serialize regardless of orchestration** — so a delegate fleet wouldn't speed the work actually
done. Delegate stays for **cross-repo (ADR-41) + research**. The real lever was **contention
reduction** (PLAYBOOK modularization), which is why Move 1 happened and Move 2 is queued. North-star:
the architect **owns the backlog across sessions** and **tracks a delegation ledger** (delegate where
independent, serialize where contended).

**The two design tensions now on the table** [recall/inferred]:

- **(A) The hybrid handoff — v5 has no formal slot for browser-authored judgment.** v5's residual is
  by spec **CC-authored and repo-derived** — it "structurally cannot carry operator intent or off-repo
  findings." Today's `-session` bundle **demonstrated** the hybrid by embedding the architect's
  strategic brief *verbatim* in the residual "why" §, but that placement is **ad-hoc** (the closest
  existing slot, not a designed one). The tension: facts transmit well, **judgment/priorities transmit
  poorly** — yet the architect role *is* judgment/priorities. See §3 Q-A and §4.
- **(B) PLAYBOOK Move 2 — maintainability, not parallelism.** Move 1 barely shrank the file (−2.3%)
  because most "duplicated" content was genuinely PLAYBOOK-canonical and correctly stayed. So Move 2
  (the structural split) is justified on **maintainability** (≈84k tokens, ~3.5× the read-cap,
  frequently edited), **not** parallelism. It is **Council-bound** because the `§N-index` design is a
  genuine fork — the §1–§19 spine is the **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so
  the split must preserve §N addressability. See §3 Q-B.

**The standing meta-argument:** every v5 bundle — **including this one** — is **hand-assembled** by CC
following the spec. That is exactly the drift-prone hand-maintained surface the methodology outlaws
everywhere else; it is the live case for **#164 (the generator)** and **#161 (the probe-core)**.

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The 2026-06-13 Q1–Q11 set is **largely resolved** (see
"Resolved-since" below); the live questions are:

- **Q-A — the hybrid handoff design (Council-bound, NEW headline).** Formalize the handoff as **two
  authored components**: CC repo-bundle (*facts*) + architect strategic brief (*through-line +
  priorities + delegation state*). **Open:** v5 has **no formal slot** for a *committed,
  browser-authored* strategic section (today's §4 finding) — design one, and explicitly **reconcile
  with #159** (which chose the *in-session-ask* form and **rejected** a new-bundle-file), with **#161 /
  #162**, and with the residual's **repo-derived / off-repo boundary** so the two channels (CC residual
  + architect brief) are **complementary, not overlapping**. Demonstrated today; needs the Council
  design. (Substrate: today's `-session` `RESIDUAL.md` §2 + §4.)
- **Q-B — PLAYBOOK Move 2 (Council-bound).** The structural split → thin `§N`-index + per-section
  modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N addressability — the
  consumer API). Maintainability-justified, not urgent. **Unblocks #39; decouples #18 / #67 / #77 /
  #146** (the playbook serialize-group).
- **Q-C — #164, the v5 generator (the last machinery item, L).** `.claude/commands/handoff.md` still
  carries the v4 8-file two-phase generator (marked SUPERSEDED); the v5 emissions are specified but not
  the wired generator. **Open sub-decisions:** (i) the **per-repo-runbook sync key** —
  write-if-absent-or-version-changed, but *keyed how* (handoff-process version? a content hash?) so a
  genuine runbook edit isn't clobbered and a stale one isn't left; (ii) the **cross-repo v4 routing**
  (ADR-83) — a v4 target repo (one lacking `scripts/audit.py`) needs a deterministic route to the v4
  Phase-1/2 path, since the v5 emissions can't bind a target with no audit checks to probe.
- **Q-D — #162, architect actor-vs-mode vocab.** Disambiguate "architect" the Layer-1 **actor**
  (browser-chat role) from "architect" the §13 **mode** atomically across every surface — rename one
  sense or formally scope both; do not leave the collision live.
- **Q-E — #159, operator-context beat (exercise in a real architect session).** The §13d beat landed
  in the canonical spec; the **only-remaining clause is exercising it in a real architect session** —
  **this session is the candidate** (the beat fires after orientation per the boot, step 6).
- **Q-F — #161, teeth probe-core.** Define a stable shared probe-core (the ~5 forced-read probes) + the
  architect orientation probe, so bundles **stop hand-assembling probe sets** per handoff. Capture-only
  (scoping is a future architect decision) — but note **this is again a hand-assembled probe set** (the
  persisting capture point).
- **Q-G — #166, doctrine_enforcement_coherence check (audit-py).** A read-only `audit.py` check
  flagging any ADR/amendment still `PROPOSED` / `NOT RATIFIED` while its implementing task is closed
  (live enforcement ahead of its doctrine — the #156 gap reconciled by hand on 2026-06-14).
- **Q-H — #167, multi serialize-group schema + parser anchoring.** `_parse_serialize_group` reads only
  the FIRST clause, so a task colliding on two surfaces can't be fully encoded — the 2026-06-14 pass
  dropped two real edges (#105↔#112 on `block_immutable_edits.py`, #5↔#77 on `ESSENTIALS.md`). Also
  **anchor the parser to clause position** so prose tokens can't self-trip it (the 2026-06-14 incident).
- **Q-I — #165, ASCII-vs-mermaid selection rule.** A *proposed* ADR-51-family amendment (operator-set
  2026-06-12; first applied when the runbook chose mermaid), awaiting ratification — not a unilaterally
  minted ADR. Record where the diagram convention lives once ratified. `serialize-group: architecture`.

**Resolved-since 2026-06-13 (do NOT re-open):** Q2/#163 (teeth validator — shipped `dba11d0`, audit
check #19) · Q3/#156 (durable task-graph — shipped + ADR-66 ratified 2026-06-14) · Q9
(automation-writer vs `--no-ff` — ADR-84 isolation) · Q1's runbook-collapse half (the canonical runbook
landed; the *generator* half persists as Q-C) · Q11 (nightly #26 dispositions — largely cleared; the
residual triage items folded into the operator queue, §6).

---

## 4. The task-graph (now **partly durable** — #156 shipped)

**The biggest change from 2026-06-13:** the task-graph is **no longer purely ephemeral prose.** #156
shipped — **hard edges are now DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. So point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b: "soft/provenance relations stay residual").

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** 9 serialize-groups.
  The **handoff** group = {#1, #26, #159, #161, #162, #164, #10} — these **serialize** (do not
  co-schedule). The **playbook** group = {#146, #77, #67, #18, #39}. The **audit-py** group includes
  #166. Parallel-safety is **derived** (no shared group + no `depends-on` path), now a schema-checkable
  property, not a hand-wave.
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q-A (hybrid) and Q-B (Move 2) are decision items, not build items** — resolve via Council /
    ratification; parallel to each other.
  - **#164 (Q-C) is the last big build item** — `L`, gated on the Q-C(i)/(ii) decisions; pairs with the
    already-shipped #163 validator (its output is now mechanically checkable).
  - **Move 2 (Q-B) unblocks #39** and **decouples #18 / #67 / #77 / #146** — landing it dissolves the
    playbook serialize-group.
  - **#159 (Q-E) is exercisable THIS session** — off the build path.
  - **#166 / #167 are independent cleanups** — #166 serializes within the audit-py group; #167 is bare.

(The "decision-not-build / Council-bound / unblocks" framing is residual judgment; the serialize-group
edges are the schema fact. #156 made the *hard* edges durable, not these *soft* ones.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` themes **"Handoff continuity"** (the handoff group),
  **"Enforced governance"** (#166), and **"Tooling & evaluation"** for the live tickets. Do **not**
  trust any re-narrated ID text — open the live BACKLOG (the §3 text is recall; the file is truth).
  `validate_backlog`: **72 tasks, 0 warnings**, 9 serialize-groups at generation.
- **Live branches at generation** (`git branch -v`): `main` (in sync with origin); `automation/fleet-audit`
  (**never merges to main by design — ADR-84**, NOT a loose end); this handoff's own
  `docs/handoff-2026-06-15-architect` (merges on completion); and **three merged stragglers** —
  `chore/ratify-adr66-156-amendment`, `feat/encode-collision-graph`, `feat/playbook-pointerize-152-158`
  (already in main; **candidates for `-d` cleanup**, carried from today's `-session` §3, deliberately
  not deleted here — out of this handoff's scope).
- **Drift-flags:** only `git_backlog_drift` #90a `[~~]` (#77, known-benign/dispositioned). `main`
  **in sync** (no divergence, no origin gap). The nightly-skip alert (§1) is operational, not drift.
  Re-derive: `python scripts/audit.py health` + `git status -sb`.
- **Audit-gating quirk (note, not a problem):** `audit.py` check #19 `handoff_probes` validates the
  **lexically-max** bundle. For 2026-06-15, `"session" > "architect"`, so **today's `-session` bundle
  stays the audit-gated one** — this `-architect` bundle is **not** the check's target. Its probes were
  verified to bind separately via `python scripts/verify_handoff_probes.py docs/handoffs/2026-06-15-dev-knowledge-architect`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **15 closure proposals** await — `/review-closures` (human-gated, done-items-leave).
- **changelog drift** — `claude-code 2.1.177 > last reviewed 2.1.168` — `/changelog-review`.
- **7 nightly triage findings** await — #31, #29, #27, #25, #23, #21, #19 (Issues tab).
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **nightly-skip alert** (§1) — the 2026-06-15 conformance digest is absent from
  `automation/conformance-digest`; check the Action run (no-retry posture).
