# Residual — 2026-07-19-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13). **Target repo: `ai-council`** — this bundle is hosted in the hub
> (ADR-36/41) and derived **READ-ONLY** from the ai-council checkout. Every probe command runs
> **in ai-council**, not the hub.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the ai-council JOURNAL / BACKLOG / git window, may have moved (the load-bearing
> ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

**The load-bearing drift this window was a FALSE PREMISE, not a stale count — and it had gated a whole class of work.** `witnessed` (from the ai-council JOURNAL 2026-07-19 entries): the standing assumption *"codex credits are exhausted until 2026-07-23"* was **empirically falsified** by a live terra probe ($0 under subscription). A body of review debt had been **date-gated on that unverified premise**; lifting it immediately discharged #33 (pass-3 CLEAN) and #44 (the 8-surface review set). **The architect should treat this as the pattern-level flag, not the incident:** a date-gate resting on an unprobed assumption is indistinguishable from a real block until someone probes it.

**Standing flags to re-derive, not trust (values deliberately absent — that is the anti-bluff contract):**
- **Gate-green is a claim, not a fact here.** `check.ps1` reportedly returns clean after the `types-PyYAML` declaration landed — **re-derive via `PROBES.md` P6**; this bundle states no exit code, test count, or mypy verdict.
- **BACKLOG shape moved hard** (#33 struck, #44 closed, #69–#72 filed, #68 re-prioritized) — counts and `OK`/FAIL come from **P3**, membership/liveness from **P7**. No count appears here.
- **ai-council carries no hub-style drift mesh.** There is no `audit.py ship-gate`, no `validate_git_backlog`, no `validate_doc_claims`, no disposition register in this repo — so the hub's usual §1 flag-set structurally **does not exist** here. The equivalents are `validate_backlog.py` + `check.ps1` + `canonical_freshness_gate.py`. Stated explicitly so the architect does not hunt for a mesh that isn't there, or read its absence as a finding.

**A live honesty flag worth the architect's attention (`witnessed`, from the JOURNAL):** **#44 was closed via its done-when's explicit "(or fixes filed)" clause — NOT because the reviewed surfaces came back clean.** Two P2 defects (#69, #71) are the reason a clean-only bar was not met. If the operator's intent was clean-only closure, reopening #44 is one edit. **This is a decision to surface, not inherit silently.**

**Two stale references recorded, not yet fixed:** `scripts/codex-review.ps1` is cited as the runner in both #33 and #44 but **does not exist** (the reviews ran `codex exec` directly); and the #33 pass-3 CLEAN verdict carries an asterisk (terra's read-only sandbox threw a `tempfile` error mid-pass, though its ~40k-token spend indicates real analysis). Neither is filed as a task yet — **an architect call: file or waive.**

---

## §2 — Shipped this window (the map — pointer, not re-narration)

Terse map only; ai-council `JOURNAL.md` (2026-07-18 → 2026-07-19 entries) and `BACKLOG.md` already encode the detail. Do **not** re-derive this narrative — read it there.

- **Review debt discharged** — #33 (verdict-package terra pass-3, CLEAN) and #44 (the 2026-07-18 arc set, now 8/8 surfaces reviewed: 5 in the night pass, 3 in the 2026-07-19 pass) both **struck**. The date-gate that blocked them was falsified (§1).
- **Night-consolidation verification** — 8/8 legs witnessed at $0 via live execution of shipped code, codified as `scripts/verify_night_consolidation.py`; a blind Codex `sol` derivation agreed on all 8 verdicts. Report: `docs/audits/2026-07-19-night-consolidation-verification.md`.
- **Worktree consolidation** — the `s14-cleanup` and smoke-pair branches closed out into `main`; a **sealed-key leak was caught and untracked pre-merge**; the `docs/smoke/` leftover struck under §5 item 9.
- **Type-stub hygiene** — `types-PyYAML>=6.0` **declared** in `[project.optional-dependencies] dev` (not ad-hoc installed); **#20's scope widened** from "the openai 2.x migration" to type-stub hygiene generally, on the reasoning that two stub-class gate failures in one day means the root cause is undeclared typing dependencies, not any single library.
- **Filed from review** — **#69, #70, #71, #72**. Every terra claim was **verified against source before filing**; two severities were **downgraded with the reasons recorded on the items**. While verifying #69, a **second distinct defect the review missed** was found (the inbox/`--file` panel divergence).

---

## §3 — Carried residuals (still live — NOT re-derivable from the repo alone)

**(a) The `--file` vs `--inbox` divergence is an inverted recurrence of a known anti-pattern.** #69 is not one bug but two: a documented frontmatter key silently discarded on every default run, *and* the two entry points guarding on **different conditions**, so the same brief yields a different panel via `--file` than via `--inbox`. This is the CLAUDE.md §10 inbox-parity anti-pattern **inverted** — interactive is the broken half this time. **Design implication that travels:** the fix is a **shared helper**, not two parallel patches; #64 touches the same `--file` surface and should likely merge with it.

**(b) `#71` is shipped code violating the rule that was being enforced the same day.** `--no-persist` calls `mkdtemp()` with **no cleanup anywhere in the module** — a live violation of §5 item 9 "No leftovers." It is also a **concrete instance of the #68 guard proposal**, which strengthens that proposal's case materially. Whether that converts #68 from proposal to accepted work is an **architect call**.

**(c) The two consumer→hub NEEDS-RULING intakes remain hub-tracked, ruling pending.** Filed locally in ai-council `docs/intake/` and carried across the boundary (the sanctioned consumer→hub path): `2026-07-17-hub-feedback-codex-producer-lane.md` (hub `#341`) and `2026-07-17-hub-feedback-session-close-gate.md` (hub `#344`). **Do not re-plan these in an ai-council chat** — they are a hub session's work. `unknown`: whether either has been ruled since filing.

> **Supplement correction (§13: advisory, never trusted over the repo).** The filled `SUPPLEMENT.md`
> §4 cites the session-close-gate ticket as hub **`#343`**. That is **wrong** — `witnessed` against the
> live hub `BACKLOG.md` this generation: **`#344`** is "Session-close gate for handoff generation +
> consumer hub-write guard (NEEDS-RULING)"; **`#343`** is an unrelated `fleet_parity` ship-gate-scoping
> perf item. The supplement is committed **verbatim and unedited** (CC never rewrites the architect's
> answers) — so the wrong id stands in that file by design, and this note is the correction. **Use
> `#344`.**

**(d) The interim Codex-producer fallback — verify before assuming it still binds.** The 2026-07-17 ruling held that bounded build tasks run as **CC-implements + terra read-only review pre-merge** (never Codex-writes), pending the hub's #341 reconciliation. It shipped several arcs cleanly and terra caught real defects each time. **But its stated rationale referenced the credit-exhaustion premise that §1 falsified** — so the *fallback* may still be right while its *stated reason* is now partly stale. Worth an explicit re-confirmation rather than silent inheritance.

**(e) The §6.3 scope-boundary fork — still awaiting an explicit ruling.** The plan-of-record / consolidation-brief fork (pure-governance vs thinking-aid scope) is implicitly held at "pure governance" but was never formally adjudicated. Carry-open; raise only if the operator does.

---

## §4 — Next-frontier decisions (the design "why" that travels)

**The window that just closed was a *verification and debt* window. The next one is a *fix and unblock* window.** The architect's job is to decide the shape of that, not to re-derive what shipped.

**The four open threads, with the tension in each:**

1. **The two P2 silent-failure defects — #69 and #71 (the ready slack).** Both are *silent* failure class: neither surfaces an error, both produce a plausible-looking success. #69's fix is a shared-helper refactor across two entry points (§3a) and likely merges with #64; #71 is a cleanup-on-exit fix that doubles as evidence for #68 (§3b). **Tension:** patch each locally (fast, but re-splits the `--file`/`--inbox` surface a third time) vs land the shared helper (correct, larger, touches the highest-contention module family).

2. **The silent-failure *trio* — #62, #63, #65 — needs grooming as a class, not as three tickets.** All three are the same shape: a write/route failure that returns success. #62 research `--return-dir` is best-effort; #63 a metrics-sidecar failure **suppresses the verdict package entirely**; #65 `doctor` ignores the #39 output controls. **The architect question is whether these plus #35 are one epic-level fix — a uniform fail-loud output-routing contract — rather than four independent S-sized patches.** That is a way-of-working decision, which is why it belongs in this session and not an execution lane.

3. **The two proposed guards — #67 and #68 — await a decide/drop ruling.** #67 is a pre-commit gate on staged `SEALED-KEY*.json` (motivated by a *real* near-miss this window, not a hypothetical); #68 is a registry check on new `docs/` directories, and #71 just supplied it a live instance. **Tension:** both are hub-methodology-shaped guards living in a consumer repo — the standing question of whether a consumer may grow its own gates or must file the need to the hub.

4. **#27 CLI-4 parity remains the blocking centerpiece.** Phase 1+2 are done (24 blinded transcripts + scoring sheet committed); **Phase 3 is operator scoring — non-delegable and blind.** Until it is scored and unsealed, the **ADR-12 §5 CLI default-flip stays blocked**, which in turn blocks **#41 end-to-end** and **#66**. **This is the single highest-leverage unblock in the repo and it is gated on a human action, not on engineering.** The architect should decide whether to sequence work around that gate or press for the scoring session.

**Carry-open (do NOT redo / re-decide):** the hub NEEDS-RULING intakes (§3c) are hub work; the §6.3 fork (§3e) awaits the operator; the [S13]/#36–#38 caller-side advisor is **filed only** — build when prioritized, and #36 must reconcile with #9 rather than duplicate it.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to ai-council's **`BACKLOG.md`**
(seven-theme story-map, machine-checked by `scripts/validate_backlog.py` — counts re-derived live via
`PROBES.md` **P3**, the #69/#71 ready slack read live via **P4**, the whole open set groomed at boot via
**P7**), plus the **`docs/audits/2026-07-19-night-consolidation-verification.md`** report (this window's
evidence base — point at it, do not re-narrate it), the live branches (`git branch -v`), and any drift
the repo's own gates raise.

> **Pointer correction (`witnessed` this generation — do not inherit the old one).** The phase→task
> plan-of-record has been **ARCHIVED** to `docs/intake/archive/2026-07-16-plan-of-record.md`, and the
> seam-contract intake likewise to `docs/intake/archive/2026-07-06-technical-architect-intake.md`.
> Prior ai-council bundles cite both at live `docs/intake/` paths; those citations are now **stale**.
> The archived plan-of-record is **history, not the navigation surface** — **`BACKLOG.md` navigates**
> (§13c). Read the archive only for provenance on a decision, never to derive current scope. Re-narrating item text splits the truth — the pointer + the live probe is the whole
task-state. **The anti-bluff `PROBES.md` manifest (P1–P7) is the load-bearing carrier.**
