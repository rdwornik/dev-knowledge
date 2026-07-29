# Residual — 2026-07-29-dev-knowledge-architect — the part the repo does not already encode

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
**Nothing new was introduced by this window's wind-down arc; everything below is inherited or environmental.** Read this as a map of *which* flags to expect and *why they are what they are* — P4/P6/P7/P9 supply every value.

- **Standing / dispositioned.** The WARN set carried into this window is the one the register already
  holds (`ecosystem/disposition-register.yaml`); the wind-down arc dispositioned nothing and added no
  register entry. If a `[stale]` line appears, treat it as a register-vs-live-WARN mismatch to resolve
  by ownership, not as this arc's residue.
- **Known red, external, not actionable here — [#430](b).** `fleet_parity` reads **live sibling-repo
  state**, so a concurrent merge in ai-council or corp-monorepo reddens this repo's gate with no action
  available in this tree. The row names both halves; (b) is the one that bites at ship time. Reproduce
  on bare `main` before spending any time on it.
- **`doc_rot` backlog-accretion loci — pre-existing, unchanged.** The accreted rows are [#344], [#421],
  [#422], [#332], [#278]. This arc measured its two row writes **before** writing them ([#441] edited,
  [#445] added) and both sit under the gross cap, so the locus set is byte-for-byte the one that
  existed at the window's start. Do not read a locus here as new.
- **[#364] is the live meta-flag, and it took a fresh hit this window.** The 2026-07-29 `.vscode` ruling
  could **not** be recorded into the [#371] or [#352] rows — both sit within ~16 and ~34 characters of
  the cap — so the ruling went to its own audit artifact instead. That is the "gate degrading the record
  it protects" failure the row predicted, now witnessed rather than argued. Recorded in
  `docs/audits/2026-07-29-technical-vscode-w1-visibility-ruling.md`, final section.
- **Environmental, recurring, never a finding.** The worktree-dir-name deployed-version WARN and the
  sibling-absent legs on a VM are environment artifacts. Also: run the gates from **Git Bash**, not
  PowerShell — a PATH-absence SKIP reds `handoff_probes` spuriously and invites a false disposition.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
The 2026-07-28→29 window, one line each. Detail is in `JOURNAL.md` entries 2026-07-28 (k)–(n) and
2026-07-29 (a)–(b); this is the map, not the recap.

- **[#439] — ADR-107 strangler step 3 executed.** `tasks/` is the source of truth; `BACKLOG.md` is
  generated. `ARCHITECTURE.md` Ch5 source zone + `tasks/README.md` are the conformed reference set.
- **[#437] — shared closure-token core.** One `strip_quoted_contexts` / `closure_ids` detection core
  consumed by both scanners plus the plugin twin, under a byte-parity test. Closed on two independent
  MET verdicts.
- **[#444] — `tier1-lifecycle` 0.1.11 released.** The [#437] fix reaches the version-keyed cache;
  5-manifest anchor lockstep. Closed.
- **[#441] — codified, then ADOPTED (operator, 2026-07-29).** PLAYBOOK Ch8 carries one launch test:
  fat prompt on primary is the default, worktrees behind the four-condition test. The DRAFT marker and
  its self-contradicting ratification note are gone (terra H3 resolved); the row's `§8/Ch5` citation is
  corrected to Ch8. **The row stays OPEN** — closing it is the closure loop's call, and one condition-2
  reconciliation is still owed (§4).
- **Post-flip stale-procedure batch — audit rows 1–12 applied**, rows 14–19 no-ops by verdict, row 13
  routed to the ratification session. Terra doc-lane review paid the review leg the cloud night lane
  could not run: H1 + M1 fixed, H2 + H3 dispositioned then both resolved in this wind-down arc.
- **Two operator rulings recorded at their convention homes, one artifact-borne.** The sanctioned
  shortened-sequence precedent sits at PLAYBOOK Ch8 *Integration authority*; the [#441] adoption at the
  Ch8 launch-decision block; the `.vscode` W1 ruling at
  `docs/audits/2026-07-29-technical-vscode-w1-visibility-ruling.md` (its surface is immutable, so the
  ruling gets its own dated artifact).
- **[#445] filed** — the `codex-review` wrapper path-guard reports SUCCESS having reviewed nothing on a
  mixed diff. Third instance of the [#431] family; mechanism-scoped.
- **`ARCHITECTURE.md` delta-checked, deliberately untouched** — reasoning in §4.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### The decision this session owes (its whole reason to exist)

**Intake #18 ratification** — dossier `docs/audits/2026-07-29-technical-intake18-ratification-dossier.md`.
The un-committed "why" the dossier cannot carry: the pack was written as *eleven independent amendments*,
but §B(b) (one-round-trip boot) is a **workflow reshape**, not an amendment, and A7 / A4-item-3 are its
content rather than its peers. Rule the direction first or the content rulings land unanchored — that
sequencing is the dossier's own recommendation and it is the tension worth protecting. The v5.8-vs-v6
label follows the §B(b) call honestly; it is not a separate aesthetic decision.

**The [#441] condition-2 vs A5 conflict — deliberately left open, and it is a real fork, not a wording
tidy.** [#441] condition 2 cites "pre-allocated JOURNAL letters" as a contract that pre-resolves lane
contention; intake #18 A5 rules the opposite mechanism — letters are assigned **at integration**, never
by lanes. Both cannot be canon. The design argument the dossier makes (and this session should test
rather than accept): pre-allocation fails on the *second unplanned lane*, whereas assign-at-integration
cannot collide by construction. If A5 wins, [#441]'s condition-2 example list is amended **in the same
ruling** — one statement in the corpus, which is the whole point of the [#441] codification. The live
text of both sides is at PLAYBOOK Ch8 *Open reconciliation* and dossier A5 / pack-finding 2.

### Carried residue — what is open, and why it stayed open

- **Queued cross-repo arc (`.vscode` W1), RULING-W shape, not started.** Three legs, all consumer-side:
  the corp-monorepo manual `.vscode` decoration copy (the ai-council precedent, ADR-93 merge-not-clobber),
  and the `review_date: 2026-08-13 → 2026-08-26` e1 re-date in **both** consumers' `.methodology.yaml`.
  Ruled 2026-07-29, recorded in `docs/audits/2026-07-29-technical-vscode-w1-visibility-ruling.md`,
  executed **nowhere** — the operator scoped it as its own follow-up arc. Re-witness each consumer live
  before editing; the sizing surface's reads are dated 2026-07-28.
- **The 2026-08-26 cluster is now four things, not one.** The drain slice ([#356], [#358]–[#361] —
  prep artifact `2026-07-28-technical-drain-slice-prep.md`), the 26-row D-queue
  (`2026-07-28-technical-d-queue-0826.md`), [#364] build option 4(a) plus the disposition reviews, and —
  newly folded in by the 2026-07-29 ruling — **the `.vscode` mechanism-DATE selection**. That session is
  getting heavy; whether it splits is an architect call worth making *before* it arrives, not at its door.
- **[#433] stays open on §6.2 grounds — two concordant NOT-MET verdicts.** The ADR-107 §6.2
  generalization obligation is undischarged by design (its owner is [#383], open) and §6.3 is ruled but
  not structurally discharged; §7.5 bars closing on the ADR alone. This is the correct state, not a
  stalled one — do not let a closure sweep re-litigate it without the second-surface demonstration.
- **[#440] / [#442] / [#443] open, unbuilt.** [#440] — the `tasks/` id ledger is not tamper-evident (a
  *deleted* retired record silently frees its id; the gate only catches a re-issue while both holders are
  present). [#442] — plugin command-cache staleness: cached command text can outlive a workflow change,
  and this window witnessed exactly that. [#443] — planning artifacts outside the three enforced classes
  carry no rent rule. All three are honest gaps, none blocking.
- **H2-class residue: none outstanding.** H2 was the ADR-65 "closing adds no new per-item write" claim,
  falsified as a *mechanism* statement post-flip. Fixed in this arc by rewording to outcome language
  matching the converged host-branching sentence audit rows 5/9 landed. The **class** — pre-flip
  mechanism claims surviving as prose in un-swept files — is not provably drained; the night audit's
  19-row sweep plus this fix is the coverage, and a further instance would be a new finding, not a
  reopening.
- **Plugin-bump deferral state.** `plugin.json` holds at **0.1.11**. The morning batch's documentation-only
  plugin edits (the `/review-closures` host-shape branching) are therefore **not** in the version-keyed
  cache; an explicit cache-lag notice sits in `plugins/tier1-lifecycle/INSTALL.md`. Deliberate: a
  half-release (bump landed, marketplace + three-repo `plugin update` + restart not run) is worse than a
  documented lag for a docs-only change. The bump folds into the next release act — it is owed, not lost.
- **[#430] is the known red** — see §1. Reproduce on bare `main` before treating it as this arc's.

### One thing deliberately NOT done, so the next session does not redo it

`ARCHITECTURE.md` was delta-checked against this window's shipped set (flip live, shared closure core,
plugin 0.1.11, [#441] codified) and **left untouched**, with `last_reviewed` unbumped. Reasoning: Ch5's
source zone was already conformed at the flip and the night audit lists it in the conformed reference
set; the plugin version is pinned in `deploy/manifest-v*.yaml`, never in ARCHITECTURE; the [#437] shared
core lives under `plugins/` (outside the codemap's `scripts` source-root) and changed implementation, not
organ identity or posture; the [#441] launch test is PLAYBOOK doctrine, which ARCHITECTURE points at
rather than restates. The one borderline line — Ch2's closure-loop arrow ending "`BACKLOG.md` updated" —
is outcome language that still holds post-flip (the regen updates it), and the night audit adjudicated
exactly that class as CORRECT in its rows 15–17. A stamp bump without a genuine end-to-end re-read would
have been the dishonest move; the re-read was not run, so the stamp did not move.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
