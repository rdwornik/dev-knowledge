# Residual — 2026-07-20-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> ## ⚠ CROSS-REPO BUNDLE (ADR-36/41)
>
> **The subject of this handoff is `ai-council`. The bundle lives in the `.dev-knowledge` hub.**
> Every `#id`, file path, ADR number, and `BACKLOG.md` reference below is **ai-council's** unless
> explicitly marked hub. The two repos have same-named files with different contents — `BACKLOG.md`,
> `ARCHITECTURE.md`, `VISION.md`, `LESSONS.md`, `JOURNAL.md`, and even `scripts/validate_backlog.py`
> exist in both. Reading the wrong one is the primary failure mode of a cross-repo bundle; `PROBES.md`
> names a **run-in root** per probe for exactly this reason.
>
> **The hub is read-only w.r.t. the target** — this session plans `ai-council` work; it does not edit
> the hub's governance corpus. The stock generator probes were hub-bound and have been **re-authored
> against verified-live ai-council surfaces** (see the `PROBES.md` cross-repo header for which four
> and why).

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo note first (structural, and it IS the headline).** `ai-council` has **no counterpart to
the hub's drift-flag machinery** — no `audit.py ship-gate`, no `ecosystem/disposition-register.yaml`,
no `validate_doc_claims`, no `validate_git_backlog`. There is therefore **no dispositioned-WARN set to
inherit and no standing-vs-new distinction to make** in the hub's sense. The target's drift surface is
four independent read-only validators plus judgment over `BACKLOG.md` ∩ git — which is exactly why
`PROBES.md` P2/P4/P6/P7 were re-bound rather than run as generated. **Treat the absence of a
consolidated verdict as the flag**, not as a green light: several of those gates pass *silently*, so
"no output" is not "no drift" (P7 reads exit codes explicitly for this reason).

**Standing, by reference — carried deliberately, not oversights:**

- **`options_considered` is corrupted on `main` right now** — the single most consequential standing
  flag, and it sits on the **delegation surface** (the verdict package a consuming repo reads). Filed
  as **[#77]**, recorded explicitly in the 2026-07-20 JOURNAL entry. Deliberately filed as **one
  contract-scoped ticket rather than a patch queue**: this is the *second* window in which the
  function is known-broken and half-fixed (the night audit found it broken both ways; **[#60]** fixed
  one half), and a third round of partial patches is the pattern that filing exists to stop.
- **Manifest-vs-reality gap** — **[#76]**: the verdict package's `artifacts[]` can name a return-dir
  copy that the subsequent write failed to produce. `scripts/verify_output_writes.py` already reports
  this as a standing **GAP**; that visibility is the *interim mitigation, explicitly not a fix*.
- **Asymmetric routing failure** — **[#75]**: `secondary_dir` raises where ADR-43 `target_paths`
  swallows, so a `secondary_dir` failure can abort before canonical artifacts land — the same
  canonical-loss class **[#35]/[#62]** closed for `--return-dir`.
- **[#66] stays OPEN, gated on [#27]** (CLI-backend scoring); no billed witness has been authorized.
  This is cost-gated, awaiting an operator call — not a stalled task.

**New this window:** the six sol-pass filings (**[#75] [#76] [#77] [#78] [#79]**, plus **[#69]** from
the terra pass) were classified **REGRESSION vs PRE-EXISTING by differential run** against `27a45d1`
in a temporary detached worktree — not by reading the diff. All six reproduce byte-identically on both
trees, so **none were introduced by this window's merges**; they are pre-existing defects newly made
visible. The two genuine regressions (F8 marker substring-match, F2 sidecar-before-raise) were
**repaired on `main` immediately** per the operator's repair-regressions-now rule and proven by
individual reversion.

**Do not trust the above as current state** — P4/P7/P9/P10 re-derive all of it live.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map only — `JOURNAL.md` (entries **2026-07-19** reintegration and **2026-07-20** sol
disposition) already encodes the detail; do not re-read it as narrative here.

- **Three-lane serial reintegration** (A2 → A1 → C, operator-gated at every merge). Order was
  load-bearing, not convenience: A1 adds raises in the writer layer while the interactive-debate
  boundary had **no handler at all**, so A2 had to close that window first. → JOURNAL 2026-07-19.
- **The cross-lane seam defect** — the finding that session existed for: A1 green + A2 green + merged
  `main` **RED**. `OutputRoutingError`'s constructor took a `list[RoutingFailure]` with no type guard;
  `str` is iterable, so a message was shredded into one "deliverable" per character. Repaired
  fix-forward with an explicit type guard. **Two per-lane checkers were structurally blind to it** —
  each half sound, the composition broken. → JOURNAL 2026-07-19.
- **End-to-end witness mechanized** — `scripts/verify_output_contract_e2e.py`: **4/4** paths vs a
  **1/4** negative control on original `main` (three paths previously exited 0, silently). Driven by a
  real filesystem failure with providers mocked. The blind spot is now a re-runnable checker, not a
  fixed bug. → JOURNAL 2026-07-19.
- **Sol adversarial disposition** — 2 regressions repaired, 6 filed. → JOURNAL 2026-07-20, audit
  `docs/audits/2026-07-19-codex-a1-failloud-adversarial.md`.
- **Closures / strikes:** **[#67] [#68]** closed via `/review-closures` (ADR-70 Tier-1, WEAK tier, each
  named individually, citing the lane's own merge — *not* the gate's stale pre-merge evidence);
  **[#35] [#62] [#63] [#60] [#65] [#71]** struck; **[#74]** filed and closed in-arc.
- **Synthesizer Branch A (openai) shipped** 2026-07-18 as the durable config default (operator ruling,
  `docs/audits/2026-07-17-synthesizer-ruling-gemini-to-openai.md`). **Remaining scope is the ADR-01
  amendment text only** — see **[#2] [#3]**; the code decision is done.
- **New enforcement surface:** `validate_sealed_keys` **[#67]** and `validate_docs_registry` **[#68]**
  joined the pre-commit set (the latter **fails CLOSED** as `GUARD MALFUNCTION`).
- **Housekeeping closed out:** scratch dirs cleaned, both empty provisioner stub branches deleted,
  all three worktrees removed/pruned/verified absent; `main` pushed. One held-back scratch dir
  (`qfm_mhrt`) awaits an operator ruling.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The design questions this window **surfaced but deliberately did not settle**. Resume these; do not
rediscover them.

> **⚠ READ THE SUPPLEMENT SECTION FIRST — it outranks this section's ordering.** This residual is
> **repo-derived**; the supplement carries the outgoing architect's own *why*, and on three points it
> **corrects** what follows:
> 1. **`[#27]` Phase-3 blind scoring (0/12) is the gating item** — non-delegable, one operator
>    sitting, and it gates the ADR-12 §5 flip → `[#41]` → `[#66]`. **This section does not mention it
>    at all.** Rank it first; my ordering below was derived from the defect surface, which cannot see
>    an operator-blocked scoring task.
> 2. **Do not couple a compliance fix to the 1.1 bump.** Item (2) below floats folding `[#77]` into
>    Contract-Version 1.1; the supplement rejects that coupling for Contract A on the ground that a
>    compliance fix forces no version bump (precedent `[#39]`). `[#34]` + `[#76]` remain 1.1.
>    Treat item (2)'s "argument for folding it in" as **answered, not open**.
> 3. **Scope:** this window was the **output-contract** arc. The Python/stack/assets/mypy work is
>    **ARC 5, hub-side — a different repo and a different handoff.** If the live pain is stack config,
>    the next session is not an ai-council window at all.
>
> Where the two disagree, the supplement wins on *intent and priority*; this section stays
> authoritative on *what the defects are*. Everything factual in both is still re-derived live (P4–P10).

Ordered below by how much each constrains the others — **after** applying the correction above.

**(1) `options_considered` — settle it as a CONTRACT, not a third patch. [#77]**
The live decision, not a bug-fix task. The function has now been known-broken across two windows and
half-fixed once; the filing was deliberately scoped to **one** ticket to force an *ex-ante* contract
with **tests written before the fix** (bullet grammar `-`/`*`/`+`/`1.`/`1)`; exact-marker removal that
never eats a payload character — `3D`, `2026` must survive; emphasis unwrapped as real markdown
delimiters, not edge-stripped; a named test per rule). **The open architectural question is the
boundary**, not the regexes: should option extraction remain *heuristic parsing of synthesizer prose
at the output layer at all*, or should the synthesizer be asked to emit structured options directly so
there is nothing to parse? Every patch so far has assumed the former without ever deciding it. **The
F8 precedent is the relevant prior:** the operator rejected scan-narrowing in favour of removing the
defective marker, accepting a real cost (`Approaches Considered` now falls through to the question
fallback) — **under-match toward the loud failure**. `[]` is honestly empty; `['Risk one']` is
plausibly wrong and consumed silently. That principle should govern the contract.

**(2) Contract-Version 1.1 — decide the bundle and cut it. [#34] + [#76]**
Both are flagged 1.1 candidates and both change the delegation surface, so they must be **versioned
together**, not shipped piecemeal. **[#34]** = research-path verdict-package parity (the research lane
emits no `council-verdict-*.json` at all, so a Lane A research commission gets no transcript-free
deliverable — debate-path-only was an explicit architect ruling on 2026-07-17, not an oversight).
**[#76]** = two-pass write, so the manifest is serialized only after the writes it describes have
landed. Open: **is that the whole of 1.1, or does the [#77] contract belong in the same version bump?**
Argument for folding it in: all three are the same delegation-surface-honesty theme, and consumers
should absorb one break, not two.

**(3) The inbox/CLI parity blind spot — structural fix or stop calling it a blind spot. [#69]**
`LESSONS.md` records this pattern **three separate times** (`--full`, `--mode`, target-project
routing), each with the same rule: *"investigate whether the two paths can share a common processor
function; if not addressable structurally, add a parity-check test."* **[#69] is the next instance** —
frontmatter `models:` is dead in the default path *and* the two entry points guard it on **different
conditions**, so the same brief file yields a different panel via `--file` than via `--inbox`. The
recurrence count now argues the structural change was warranted several instances ago and was never
made. **Decide it: shared processor helper, or an enforced parity test as the permanent answer.**
Patching [#69] in isolation makes it instance four of five.

**(4) Enforcement asymmetry with the hub — deliberate thinness, or a gap to close?**
The genuinely cross-repo question, and the one the architect is uniquely positioned to rule on.
`ai-council` has four independent read-only validators and **no consolidated gate**; the hub has
`audit.py` with a registry, a ship-gate verdict, and a disposition register. Two honest readings:
(a) correct — `ai-council` is a *code* repo and the hub is a *governance* repo, so their enforcement
shapes should differ; or (b) a gap — several `ai-council` gates pass **silently**, so there is no
single place to read "is this repo healthy," which is precisely the composition-blindness that let the
seam defect through (two sound checkers, broken composition). **Note the recurring evidence for (b):**
this window's central lesson was that per-lane green does not compose to whole-repo green. Do not
close this by defaulting to hub parity — rule on it.

**(5) Verification-as-code — established doctrine; decide its remaining scope.**
`LESSONS.md` now carries the rule explicitly (*"a report without a re-runnable checker is a claim, not
a witness"*), and this window shipped three checkers plus a negative control. The doctrine is settled.
What is open is **coverage**: which remaining prose claims in `docs/audits/` and `ARCHITECTURE.md`
still assert something no script re-proves. That is a bounded sweep, and it is the natural next
application of the doctrine rather than a new decision.

**(6) Awaiting an operator ruling — not stalled work, but blocking if left.**
**[#66]** gated on **[#27]** (CLI-backend scoring; no billed witness authorized — a cost decision).
The held-back `qfm_mhrt` scratch dir (a 2026-07-18 CLI-seat witness run, unreferenced anywhere in the
repo). The `codex-review.ps1` severity-summary regex fix — **operator-owned, report-only, and
deliberately not edited**; measured across 68 audits in four repos, 8 reports printed `High=0` while
their bodies carried 26 High findings. **No committed audit is wrong** (the counts were never written
to any file); the damage was transient console output that could have been read as "clean" at review
time. Route the hub-owned `/review-closures` staleness class upward to the hub, not fixed here.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the backlog, the live
in-progress branches (`git branch -v`), and any **drift-flag** raised over it (§1 / `PROBES.md`
P4/P10). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is the
whole task-state.

**Cross-repo disambiguation (load-bearing — both repos have a `BACKLOG.md`):**

- **The spec for this session is `ai-council/BACKLOG.md`** — theme backbone `[E1]`–`[E7]`, story-map
  schema per ADR-66. Every `#id` in this residual is an **ai-council** id. `[E1]` (invocation surface
  & delegation-readiness) carries the delegation-surface work §4 is about.
- The hub's own `.dev-knowledge/BACKLOG.md` is **out of scope** here — this is a cross-repo handoff
  and the hub is **read-only-adjacent**: it hosts the bundle, it is not the subject. The one item
  routed *toward* it is the `/review-closures` staleness class (§4 item 6), which is filed upward, not
  fixed in `ai-council`.
- `ai-council` has **no `validate_git_backlog.py`** — the mechanical drift-check the hub row assumes
  does not exist there. P4 substitutes a manual `BACKLOG.md` ∩ `git log --first-parent` intersection,
  and **P10 is the judgment layer over it** (groom every open `#id` as live / dead / awaiting-ruling).
  This grooming is the operator-ruled boot obligation, not optional.
