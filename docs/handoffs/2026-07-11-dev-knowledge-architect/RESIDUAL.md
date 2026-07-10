# Residual — 2026-07-11-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
All drift-flags this window are **STANDING and dispositioned** in `ecosystem/disposition-register.yaml`; the handoff-generation arc introduced **none new** (the bundle was authored net-neutral — no new `doc_rot`, no new edge). Standing classes, by reference: `no_ff_merges` — the grandfathered journal-wrap + transcript-archive direct-to-main commits (`#210` is the standing-rule proposal that would retire the per-instance dispositions); `doc_rot` backlog-accretion — `#262` + `#278` (dispositioned; self-induced trims kept net-neutral); `undeclared_edges` — the six tier-1-doc → handoff-process prose edges (`#241`). The `handoff_probes` P1a/P1b/P8 SKIPs are **environmental, not drift** — grep/sed/ls PATH-absence in a bare PowerShell shell; they bind `[OK]` (10 probes) the moment the standard tools resolve (git-bash / the pre-commit shell), so a PowerShell-only ship-gate reads a spurious RED that clears under the real gate. Run **P4/P6/P7** for the live verdict / count / `[stale]` — this file names none by design. _[witnessed — `audit.py ship-gate` + `health` re-run live this generation under git-bash: GREEN / OK, 11 WARN dispositioned, zero new content drift]_
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = the **2026-07-10 execution arc** (the plan-v3 §D session; 5 JOURNAL entries + ~40 commits since the 07-10 bundle was cut at `3bc2adb`). The map (detail in the `JOURNAL.md` 2026-07-10 entries + `git log 3bc2adb..HEAD`):
- **ADR-101 hermetization RATIFIED** (Proposed→Accepted, `1d2d962`) — sanctioned top-level set + 11-class audit-name enum + refusal-gate spec; **Amends ADR-34**; `templates/audit-template.md` added. Lands plan-v3's **d.iii** (prospective + grandfather + CLASS enum).
- **#299 CLOSED** (`44da4b8`, fire-test basis) — G8 runbook Layer-6 verify exercises the hook's real interpreter. **This unblocks B-S2** (the n=2 runbook gate's precondition).
- **#303–#309 filed** + #262/#302 augmented (`f436e33`) — the morning-verdict batch: seeder child-class-awareness (#303), runbook fixes (#304/#305), hermetization build tickets (#306/#307), branch-protection parity (#302/#309).
- **#310 filed / #311 closed** — cold-bundle annotation surface (M15, `cec46d7`); fleet_health groom-parser twin fix (`7024ec4`).
- **Lane-N night consolidation integrated** (`bee5b0d`) — 6-corpus census + morning brief + changelog review (`docs/audits/2026-07-11-*`).

State pointer: `BACKLOG.md` — **7 themes / 20 stories / 89 tasks** (§4 sets the current priority — the filled SUPPLEMENT's universalization/hermetization audit leads; #270 at position 2). _[witnessed count — `validate_backlog.py` re-run this generation; the arc itself is recall — reconstructed from the 2026-07-10 JOURNAL entries + `git log`, not lived this session]_
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Priority per the FILLED `SUPPLEMENT` (operator, this fill) — read it first; it supersedes the repo-derived ordering below.** The operator's **P1 headline is a fleet universalization/hermetization boundary audit** (dev-knowledge / ai-council / corp-monorepo → an evidence-based methodology-vs-project boundary per surface, a **divergence matrix** with per-item disposition, then PLAYBOOK + mechanisms — *not* prose; "all onboarded = all OK" is a **rejected** claim shape — Wave-1 n=2 proved *enforcement* in effect, never *structural uniformity*). One big read-only comparative fan-out that **builds on** (never repeats) the 2026-07-11 corp root-hygiene audit + naming census + ADR-101 + the QA n=2 scorecard, ending in a matrix + dispositions, **never a verdict**. **#270 is demoted to position 2.** The full charter, tensions weighed, and rejected options are in the folded SUPPLEMENT — not re-narrated here.

The operator's **execution-first bar still governs** — visible outcomes over governance. Most of plan-v3 §D executed on 2026-07-10 (§2); the **repo-derived work inventory** below is the remaining backlog — read it as inventory, **not** the priority order (the SUPPLEMENT sets priority):

- **#270 operator-load gauge — position 2** (`[P1]`, §S20; was the repo-derived headline — the 2026-07-10 JOURNAL M12 named it the *next architect-session headline* — **demoted to position 2 by the operator's filled SUPPLEMENT**). Still the gating FIRST element *within* any Tier-2 nightly-layer revival — it lands **before** #271 (nightly proposal loop, `depends-on #270`). The build-ready design + ex-ante success metric + pre-registered kill criterion are already specced (`docs/audits/2026-07-05-draft-tier2-nightly-layer.md`); this is a **build, not a re-decision**. _[recall — plan-v3 OD4 + 2026-07-10 JOURNAL 'Next']_
- **B-S2 corp-monorepo onboarding — now UNBLOCKED** (#299 G8 fix closed today). The **n=2** runbook gate after the ai-council n=1 pilot; a dedicated corp chat (ADR-41), plan-first. Runs the leg-b seeder as first real consumer; surfaces #262/#295 (corp is the *second* concrete failing codemap layout — **node-granularity, not tach-presence, is the blocker**, per #262's 2026-07-11 correction) + the runbook fixes #303/#304/#305 the corp gap-notes (G10/G12/G13) raised. _[recall — plan-v3 §D · #299 close]_
- **EPIC G QA-role decomposition** — waits on the operator's **functional QA intake session** (still pending; the functional boot is printed/ready). Then technical decomposition → ADR (role · protocol · report-gate) → build → **FLEET CARRIER** (every onboarded repo inherits it). Evidence set: incidents I1–I6 + OD2 proportional test-depth keyed to the T1–T5 scope-tags (#278 test-suite hygiene is the nearest live consumer; #144 feature-DoD E2E adjacent). _[recall — plan-v3 §A/§B]_
- **Hermetization — RULED, now BUILD** (ADR-101 Accepted today). d.iii is landed; the follow-ups are **#306** (`validate_hermetization.py` refusal-gate — HUB-ONLY, prospective-only, added-paths-filter) + **#307** (`gen_intake_index.py`); d.i/d.ii landings + closing **#300** remain. Filed, not built, per the 07-10 mandate (capture-precedes-construction). _[witnessed — BACKLOG #300/#306/#307 open; ADR-101 Accepted]_
- **EPIC H — subagent/model-routing doctrine** (OD3): research spike → PLAYBOOK doctrine (Opus = orchestration/judgment · Sonnet = bounded probes/mechanical · Haiku = cheap fan-out where the quality floor allows) → binds EPIC G's QA runs as the first consumer. The 2026-07-10 night run (Opus orchestrator + 6 Sonnet read-only subagents, all git mutations serial in the main thread) is another clean datapoint. _[recall — plan-v3 OD3]_
- **Operator-owed (not CC work):** P7 3-mode one-liner (formally closes EPIC C — #164 itself already closed) · the QA-functional session · close the 3 live worktree sessions + re-run the verdict-sheet Section C removes (`lane-a -d`; `lane-b`/`lane-n -D`, superseded). _[recall — 2026-07-10 JOURNAL 'Next']_
- **Corp session (ADR-41, separate chat — queue-only here):** CLAUDE.md §4 YAML one-liner · models/eval READMEs · the D4 ARCHITECTURE refresh · #262 corp codemap · #283 dup · #126 loop pilot. _[recall — 2026-07-10 JOURNAL 'Next']_

**Provenance (honest).** This architect self-handoff was cut from a fresh `/clear` CC session, so the repo-derived frontier above is **reconstructed** from the 2026-07-10 JOURNAL 'Next' lines + live `BACKLOG.md`, not witnessed deliberation (hence the `recall` tags). The operator has since **FILLED `SUPPLEMENT.md`** — the strategic "why" (intent · tensions weighed · rejected options · the reprioritization above) now travels in the folded SUPPLEMENT, so the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

**This bundle supersedes `docs/handoffs/2026-07-10-dev-knowledge-architect/`** (complete + immutable — its plan-v3 was executed 2026-07-10; boot THIS one, the 07-10 bundle stays as history). Slug dated **2026-07-11** (next working session) because the 07-10 slug is held by that consumed bundle — the same convention the 07-10 bundle used to avoid its 07-09 collision.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
