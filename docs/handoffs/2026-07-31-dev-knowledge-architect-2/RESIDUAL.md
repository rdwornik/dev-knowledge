# Residual — 2026-07-31-dev-knowledge-architect-2 — the part the repo does not already encode

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
**All STANDING, none new this window.** Two WARNs survive the ship-gate and both are
long-dispositioned, not fresh drift: the `templates/CONTRIBUTING-md-template.md`
`reconciled_with` placeholder (a false-positive **by construction** — the template carries
`@<version>` for the consumer to resolve; owned by **[#335]**), and the ai-council root-sweep
`conftest.py` entry (owned by **[#430]**). Both carry live entries in
`ecosystem/disposition-register.yaml`.

**Two test failures are likewise standing, and were PROVEN not-mine** by stashing to HEAD and
re-running: `test_check_fleet_parity_green_on_live_repo` (the same ai-council conftest) and
`test_routine_consumers_live_backlog_governs_exactly_one_row` (the live BACKLOG now declares
**two** routine rows where the test pins one — a real, unowned drift worth a row if it recurs).
Re-derive all of it live via P7/P4/P6/P9 — this file states no verdict, count or `[stale]`
status.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
One arc, merged in two `--no-ff` commits. **Do not re-narrate — read the merges.**

- **[#446]** — the §B(b) one-round-trip boot + **HANDOFF_PROCESS v6.0** (ADR-82 lineage). One
  `--no-ff` merge, 22 commits,
  built to a RED-first frozen contract (`tests/test_v6_frozen_contract.py`, frozen at
  a frozen commit *before* any build code), then codex (code lane) + terra (prose lane) reviewed
  with all 8 findings fixed RED-first. Rulings: `docs/audits/2026-07-31-technical-v6-open-rulings.md`
  (R1..R7 + amendments **A1** the 18,000-byte budget, **A2** the P0c narrowing).
- **the window seal** (second `--no-ff` merge): [#446] and [#421] CLOSED (ADR-107
  retire-never-delete),
  **[#448]** filed for the carried A11 leg, intake #18 **A6** recorded not-built at its owner,
  three LESSONS one-liners. **Both merge SHAs are in `JOURNAL.md` 2026-07-31 (d)** —
  stated there, deliberately not here (P3 re-derives live HEAD; a bundle that names a sha
  hands a probe its answer).

**What is now IN EFFECT on `main`, not merely merged:** `/handoff-verify` (one CC-side run →
one evidence block → one operator paste) · the P0a/P0b/P0c standing-topic legs · the
`Destination` boot row + its P3 comparison · the 18,000-byte boot budget (assembler WARNs,
`audit.py::check_boot_byte_budget` FAILs) · RM-8 overwrite refusal · the [#421] tokenizer
absorption. **This bundle is the mechanism's first live exercise.**
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### The frontier — [#382], now due

Its pull-forward was **declined last window** as a deliberate scope call; that reason has
expired with the v6 arc landing. It is the window's substantive work and its shape is unruled —
decide the shape before decomposing.

### Standing debts, each named with its owner

1. **Night branch `claude/night-2026-07-30-boot-prep` @ `5b3895dc`** — UNTOUCHED all window by
   standing instruction. Awaiting its **ADR-105 consumption decision**; the path if adopted is
   *branch-only → local gates → operator merge*. **This is a decision, not a task** — nothing
   should touch that branch until it is made.
2. **[#448]** — the A11 staged-diff guard (sol acceptance item 10), filed this window with the
   triage text verbatim. Carried out of [#446] unbuilt and named rather than dropped.
3. **Intake #18 A6** — the SUPPLEMENT 7th question (ratified-in-chat register). Recorded
   NOT-BUILT at its owner, `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md` §7,
   with reason and pickup pointer. Unblocked and independent of v6.
4. **[#441] ADR-61 leg** — untouched this arc (Ch8 was not in the diff). Stays named; **no
   discharge is claimed.**
5. **[#277] closure-detector repair** — until it lands, **every closure stays manual**. This
   window's two closures were hand-adjudicated, which is the cost being paid each time.
6. **08-26 cluster entry gate** — the **§3.2-vs-[#364]-4(a) cap conflict** is unresolved, and
   the *split-or-not* first call is still unmade. Both are entry conditions for that cluster.

### Transcription debt — five chat-ratified items, VERIFIED unlanded

Checked live in the files this window (grep, not recall) — **none has reached canon**, so each
is promotion debt with a named target home (items (d) and (e) were ratified later in the same
window and are recorded here at the same bar) (intake #18 A8: a ruling stranded in a consumed
transient is debt):

- **(a) The GREEN-on-branch vs GREEN-on-main honesty split** — zero hits in `PLAYBOOK`,
  `ESSENTIALS`, `LESSONS.md`, `docs/handoffs/README.md`. Target home: **PLAYBOOK Ch8** (or a
  LESSONS one-liner). The practice was followed all window; only the *rule* is unwritten.
- **(b) The authorized-integration-act framing** — zero hits in `PLAYBOOK` or
  `HANDOFF_PROCESS`. Target home: **PLAYBOOK Ch4 + HANDOFF_PROCESS §13**.
- **(c) Closure-polarity → [#447]** — present ONLY in immutable audits and the *previous*
  window's bundle/supplement. `tasks/447-*.md` is **open** and its row does **not** mention
  polarity. Target home: the **[#447] row** (it currently covers only the ratchet/bootstrap
  deadlock family).
- **(d) The decision-routing boundary** — the operator rules FUNCTIONAL questions; the architect
  decides / records / reverts TECHNICAL ones in its own lane; the Council distills contested ones.
  Exercised live and enforced by the operator mid-window. Target home: **ratifies via the ingested
  intake §A** (`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md`, **#22
  SEED** — ingested this close, NOT ratified; §I.3 makes ratification the next window's first
  ruling batch).
- **(e) Supplement authorship** — SUPPLEMENT answers are **architect-authored**; the executor
  supplies **verified facts only**. The defect occurred in THIS bundle: the close instruction
  delegated the fill to the executor, the operator caught it, and the ANSWERS were re-authored
  wholesale. Target home: **a HANDOFF_PROCESS §13 one-liner + PLAYBOOK**. Codification is owed —
  the correction happened, the rule is still unwritten.

### One seam this bundle itself surfaces

Its own `Destination` branch field reads **`main`** — the honest boot destination for a
primary-tree architect seat — but HANDOFF_PROCESS §13(c″) says the field carries a branch *in a
sanctioned lane shape*, and `main` is not one. P3 will PASS at boot and FAIL the moment this
seat branches (as invariant #5 requires it to). **Not fixed here** — it is a spec question, not
a bundle defect: does the Destination row mean *boot destination* or *lane*? First live evidence
for the next window to rule on.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
