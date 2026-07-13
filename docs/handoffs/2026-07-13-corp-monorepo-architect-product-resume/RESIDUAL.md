# Residual — 2026-07-13-corp-monorepo-architect-product-resume — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the corp `BACKLOG.md`, §6). Mode: **architect** (§13); the session's WORK is **product**. **Target repo: corp-monorepo** — this bundle is hosted in the hub (ADR-36/42), derived READ-ONLY from `../corp-monorepo`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the corp JOURNAL/git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is EMPTY (cold handoff).** ANSWERS committed empty; the incoming §13(d) operator-context beat fires **FULL**.

---

## §1 — Methodology-layer status + drift-flags (THE HEADLINE)

**The methodology layer is A0-CLOSED (declaration 2026-07-13)** — corp-monorepo passed the witnessed operational minimum, 4/4 organ classes (hooks · skills · commands · handoff), corp JOURNAL 2026-07-12 "A0 exit leg b". The operator is **unblocked for product work here.** Methodology questions route to the **hub** (`.dev-knowledge`), not this chat.

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P4), not in trusting these lines.** This bundle states **no** sha, count, armed-state, or region text — those are the probes' live answers. `witnessed` at derivation: corp carried an **in-flight, actively-committing methodology lane** (`chore/w3-corp-legs`) — HEAD is a moving target, which is exactly why P1 re-derives it live.

---

## §2 — Pending / shipped this window (pointer, not re-narration)

**PENDING — unmerged branches (non-product methodology residual; carried, NOT for this product chat to merge):**
- **`chore/w3-corp-legs`** — the in-flight W3 methodology micro-lane (new `docs/intake/README.md`; ruff config home moved `.ruff.toml` → `pyproject.toml [tool.ruff.lint]`; `.gitattributes` fleet baseline; the `.methodology.yaml` `ruff-gate` waiver KEPT). `recall`, folded from the corp JOURNAL session-summary: **corp `main` is ahead of `origin/main` by the `e349d8b` dev-terminals merge set (unpushed) — do NOT push from a chat; flagged for the operator's morning merge pass**; then the operator merges `chore/w3-corp-legs` `--no-ff` (`block-ff-push` enforces). An **802-path `.gitattributes` renormalize** is queued **report-only** (deferred to its own arc).
- **`docs/backlog-transcript-mime-fix`** — a carried pre-existing branch holding **corp#15** ("hardcoded video mime breaks non-mp4 transcript" — a BACKLOG add, ~1 commit ahead of corp main). **Next step:** the next corp session decides/implements #15 (adjudicate in the OWNING repo, ADR-41). Not this product chat's to merge.

**SHIPPED (recent, by reference — detail lives in the corp `JOURNAL.md`, not recapped here):** the T1 content-parity baseline adoption (owner=hub CLAUDE regions materialized verbatim from the hub `templates/claude-regions/`; CONTRIBUTING template; LESSONS/JOURNAL preamble parity; BACKLOG E/S story-map + the `validate_backlog` twin); the A0 leg-b witnessed operational minimum; the W3 legs above. This is a **map** — the corp `JOURNAL.md` (2026-07-12/13 entries) is the record.

---

## §4 — Next-frontier (the design "why" that travels)

**Primary — resume PRODUCT work.** The operator's product backlog waits in corp `BACKLOG.md` (E1–E5 theme/story-map). This chat's job is product decomposition + execution support, **not** methodology. The specific product focus is off-repo — the §13(d) beat (FULL, since the supplement is empty) captures it live from the operator.

**Carry-open (non-product — do NOT redo in this product chat):**
- The `chore/w3-corp-legs` merge + the unpushed dev-terminals-set push + the 802-path renormalize (all detailed in §2) are the **operator's morning merge pass** (or a hub/methodology chat), not this product chat.
- **corp#15** (transcript MIME) on `docs/backlog-transcript-mime-fix` — a corp bug/product item the next corp session rules on.
- Any **methodology** question (a gate, a region, a carried organ, a template, a version) → the **hub** `.dev-knowledge`, per the A0-closed posture. This chat does not reshape the way-of-working.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the corp **`BACKLOG.md`** (E1–E5 story-map, machine-checked by `validate_backlog` — count re-derived live, `PROBES.md` P2), the live in-progress branches (`git branch -v` — the §2 lanes; P1 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **The anti-bluff PROBES manifest (`PROBES.md`, P1–P4) is the load-bearing carrier: every claim above that could drift has a probe.**
