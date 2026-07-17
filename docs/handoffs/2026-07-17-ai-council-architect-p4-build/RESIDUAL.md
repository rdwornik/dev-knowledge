# Residual — 2026-07-17-ai-council-architect-p4-build — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the ai-council `BACKLOG.md`, §6). Mode: **architect** (§13); the session's WORK is **product BUILD**. **Target repo: ai-council** — this bundle is hosted in the hub (ADR-36/42), derived READ-ONLY from `../ai-council`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the ai-council plan-of-record / JOURNAL / git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** The outgoing architect's answers are folded into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"* (not full).

---

## §1 — Pause LIFTED + the build spec (THE HEADLINE)

**Feature-work pause is LIFTED.** `recall`: G2 (consolidation + GOV-1, ai-council `#31`) lifted the pause; the lift merge is ai-council **`2a00c37`** (`witnessed` at derivation as the ai-council `main` HEAD — **P1 re-derives live**, it will have moved once the build wave commits). The build wave (**P4**) and the post-pause quick unlock (DOC-3, shipped `#30`) were gated on G2; they are now runnable.

**The build spec is the plan-of-record — design AGAINST it, do not redesign.** Canonical source: ai-council `docs/intake/2026-07-16-plan-of-record.md` (the operator's frozen phase plan, materialized). This chat's job is to drive **P4 build wave 1** in order:

1. **#25 doctor** (P4) — pre-work **A2**: decompose `cli.py:main` → a `@click.group` with `run` / `doctor` subcommands. `doctor` consumes `healthcheck.py` — **never rewrites it** (do-not-touch reference module). Same-module adjacencies A5/B5/B7 touch `cli.py`; land the A2 decomposition first.
2. **#16 CLI seats (claude + codex)** (P4, existing task) — pre-work **A1 → A3**: template-method provider base, then the one error classifier + timeout/retry contract (the five-token cause vocabulary = `seats[].fallback_events[]`). A4/B3/B7 touch `output.py`/`policy.py`.
3. **#26 verdict package** (P4) — pre-work **A4**: decompose `save_to_file`; `save_verdict_package` lands as a **sibling** (never more lines in `save_to_file`) + **B3** (shared tz-aware timestamp helper for the deterministic `<ts>`). Emits `council-verdict-<ts>-<mode>-<slug>.json` per DRAFT-INT-1 — a transcript-free caller deliverable.

**"A1, A2, and A3 are the load-bearing three"** (refactoring guide, via plan-of-record §5). Part A structural = unblocks the wave; Part B mechanical = do anytime.

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P4), not in trusting these lines.** This bundle states **no** sha, count, armed-state, or phase-table text.

---

## §2 — The sidecar seam rule + contention map (the design constraint that governs ordering)

**Sidecar seam rule (frozen, verbatim):** *first lane defines the extension mechanism, never built concurrently.* Concretely: `seats[]` (from L-CLI, i.e. #16) and `synthesis` (from L-EPI) both extend the `_metrics.json` sidecar — **whichever lands first defines how the sidecar is extended; the second conforms.** Serialize; never build both extensions in parallel sessions. **The verdict package (#26) is NOT a sidecar extension** — it is a separate caller-facing artifact (the sidecar is telemetry; the package is the deliverable); it consumes `seats[]`/`synthesis` facts **by reference** and designs neither.

**The five cross-lane seam contracts are canonical in the intake §3** (ai-council `docs/intake/2026-07-06-technical-architect-intake.md`) — **design against, never redesign**: (1) metrics sidecar namespacing, (2) doctor ownership (L-DOC owns; L-INT consumes as optional pre-flight; L-CLI contributes exactly the identity re-probe), (3) Epic B gate (L-EPI owns), (4) parity evidence (L-CLI owns; only CLI-4 results ratify the ADR-12 §5 flip), (5) enforcement (L-GOV owns; hub-carrier work is a hub arc).

**Contention map (plan-of-record §5):** `output.py` is the **highest-contention** module of the wave (A4 + B3 + `seats[]` sidecar + verdict package) — **serialize** work touching it. `cli.py` is second (A2/A5/B5/B7 + doctor). Do-anytime, no deps: B2, B3, B4, B5, B6, A5. **Do-not-touch reference module:** `healthcheck.py`.

---

## §3 — Carried residuals (the three the operator flagged — NOT re-derivable from the repo alone)

**(a) G3 is OPEN — the operator's blind-scoring mission, un-gates Epic B.** `#24` (EPI-1 archaeology) is **prepped but unscored**. An overnight-prepared **40-item blind-scoring pack** sits at ai-council `docs/audits/2026-07-17-epi1-archaeology/` (`OPERATOR-SCORING-README.md` = self-sufficient runbook; `items/ITEM-01..40.md`; `scoring-sheet.md`). The operator scores 40 historical syntheses blind (5 yes/no criteria from `SYNTHESIS_QUALITY_RUBRIC.md`), un-blinds with the sealed key, and tallies per-author pass-rates (gemini vs openai). **The flow:** operator blind scoring → a **Beat-1 mini-session** → the **#24 single-recommendation report** (Branch A swap / Branch B keep-gemini) + the operator's **ruling**. **That ruling IS the G3 event = Epic B** — it un-gates **#18 / #19 / #9** (plus D12/D13 and the v2 crux-resolver ranking, ADR-13). **This build chat does NOT do G3** — it is the operator's decision authority (ruling r3 / OQ-3); the LLM-judge second opinion is a *secondary* signal, segregated, never the verdict. G3 is **pause-independent** and can run before/during/after the P4 wave.

**(b) Hub-feedback file to carry hub-side — the Codex producer-lane conflict (NEEDS-RULING).** ai-council `docs/intake/2026-07-17-hub-feedback-codex-producer-lane.md` is a consumer→hub NEEDS-RULING note (EPIC-H). **The conflict:** a day-session plan tasked **Codex as PRODUCER** (#30 DOC-3), but two machine-level facts block it: (1) `~/.codex/AGENTS.md` is a *global read-only reviewer* policy — `codex exec` refuses to write even with `-s danger-full-access`; (2) the Windows write-sandbox can't apply patches (`workspace-write` refused). So Codex-as-producer is **unrealizable on this machine without editing hub-owned global infra — which a consumer must not do (core-invariant #6).** **The ruling the hub owes:** reconcile the Codex-producer doctrine with the global read-only `AGENTS.md` policy — either (a) formally adopt "Codex is review-only; CC/other agents produce" (retire Codex-as-producer from build plans), or (b) define a sanctioned producer-lane exception a consumer can invoke without editing global infra (and if (b), fix the Windows sandbox). **This is a HUB session's work**, not this ai-council build chat's — but the browser should know the ruling is pending so it does not re-plan Codex-as-producer for the P4 wave.

**(c) Interim Codex-producer fallback rule — IN FORCE NOW (operator ruling 2026-07-17).** Until the hub reconciles (b): **bounded build tasks run as CC-implements-Codex's-design + terra read-only review** (`codex exec review`) pre-merge. Codex/terra stays in its configured reviewer role. This shipped #30 cleanly (terra review: no Critical/High) and is recorded as a machine-level gotcha (`~/.claude/skills/gotchas/gotchas.md`). **Apply this to the whole P4 wave:** CC produces the code; Codex/terra reviews read-only; never plan Codex to write.

---

## §4 — Next-frontier (the design "why" that travels)

**Primary — drive P4 build wave 1 in order (#25 → #16 → #26), against the plan-of-record, honoring the sidecar seam rule + the pre-work map (§1/§2).** The whole-system view the architect must hold: the seam contracts are fixed (design against, never redesign); `output.py` is serialized (highest contention); the sidecar's first-lander defines the extension; the verdict package consumes by reference. The specific starting lane + launch config (model / effort / autonomy) rides the filled supplement (Q6 + addendum A: #25→#16→#26 is the recommended default, not dogma; #23 qualifies as an early disjoint parallel lane, #22 must wait for A2) — the narrowed §13(d) beat only re-checks whether anything changed since.

**Carry-open (do NOT redo / re-decide in this build chat):**
- **G3 (#24)** is the **operator's** blind-scoring mission (§3a) — its ruling is the Epic B event that un-gates #18/#19/#9. This chat builds P4; it does not score or rule.
- **The Codex producer-lane ruling (§3b)** is a **hub** session's — do not re-plan Codex-as-producer here; use the interim fallback (§3c).
- **P5 is evidence-gated:** CLI-4 parity (n=12, `#27`, depends-on #16) → default-flip; #18/#19/#9 only after G3. **P5 does not start in this wave** — #16 must land first to produce the parity evidence.
- **P6 is a completion backstop, not a start gate:** the `--file` gap "falls out of" A2's `cli.py:main` decomposition, so #22/#23 (CONTRACT §7 known-deviations) MAY close early during P4 — but the P6 row only verifies the window is complete (CONTRACT §7 emptied). Any **methodology / hub** question → the hub `.dev-knowledge`.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the ai-council **`BACKLOG.md`** (story-map, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P2) + the frozen **`docs/intake/2026-07-16-plan-of-record.md`** phase→task map (P4 = #25/#16/#26; P4 quote re-derived live, `PROBES.md` P4), the live in-progress branches (`git branch -v` — P1 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **The anti-bluff PROBES manifest (`PROBES.md`, P1–P4) is the load-bearing carrier: every claim above that could drift has a probe.**
