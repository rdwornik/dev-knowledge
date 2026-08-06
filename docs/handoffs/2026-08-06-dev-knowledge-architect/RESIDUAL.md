# Residual — 2026-08-06-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Every flag you will see is STANDING and carries a register entry.** Read them at
`ecosystem/disposition-register.yaml`; do not re-adjudicate them from this list. By family:
the legacy `no_ff_merges` non-merge commits on main (inherited June history — **never** rewrite
them); `reconciled_versions` on the CONTRIBUTING template (`#335`); `doc_rot` backlog-accretion
on the ruled Grok peg (`#492` — the one genuine rule-vs-ruling conflict, dispositioned rather
than trimmed); the `undeclared_edges` → handoff-process family (`#241`); `fleet_parity` on the
ai-council root `conftest.py` (`#430`); and `preflight_backlog_ids` (`#310`, RETIRE-ON-CLOSE).

**NEW this window: exactly one, and it is already RESOLVED rather than dispositioned** —
`fleet_audit_replication`. It was **self-induced**: a `[#296]` repro invoked
`audit.py repo … --repo-path`, whose ADR-80 replication push failed, leaving the durable-record
branch behind. The remedy was to complete the push, not to file an exemption — which is the
trim-vs-disposition ruling applied (self-induced findings get fixed; a disposition is reserved
for genuine rule-vs-ruling conflict). If it reappears, the cause is a failed replication push,
not a new defect class.

**Two test REDs are expected and both belong to `[#457]`** — legs (i) and (ii), inherited and
RED-first by design. Leg (i) rides the `#430` disposition above, so a green ship-gate and a red
test are consistent here, not contradictory. Do not "fix" either without the row's census.

State-of-flags values (verdict, counts, `[stale]`) are deliberately absent — P4/P7 re-derive them.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Detail is in `JOURNAL.md` 2026-08-06 **(a)** and **(b)** — this is the map only.

- **Night batch integrated** — 8 cloud commits, all `docs/audits/`. Its FINDING-0 (claimed lost
  work on `origin/main`) was **REFUTED**, not fixed: nothing was ever at risk.
- **A2 register fix** — `protocols/STANDING_RULINGS.md`: forward-only expiry, PERMANENT lawful
  with a ruling citation, plus two corrected locators. Register edit was held to A2 by ruling.
- **Finding-1 scope split** — `protocols/PLAYBOOK.md` + `templates/prompt-template.md` **v1.7**,
  cross-pointed both ways; PLAYBOOK wins on epic-lane criteria. The two lane ceilings are kept
  as **different axes** and deliberately not reconciled.
- **Closed:** `[#363]` (superseded by `[#469]`), `[#394]`, `[#432]` (ADR-106; clean-checkout
  `uv sync --locked` run as its done-when required).
- **Narrowed:** `[#338]` → legs (b)–(e); `[#317]` → leg (a).
- **Annotated, still OPEN:** `[#146]` (clause (a) landed, authorship unverified), `[#296]`.
- **Re-scoped:** `[#487]` — pipeline-repair-first, four ordered legs, L, not first batch.
- **Born:** `[#501]` `[#502]` `[#503]` `[#504]`. **B3 (vale) born zero rows** — refuted.
- `[S24]`'s completed-story disposition was **verified as already landed** (`3c050b15`), not
  re-done. `[#170]` untouched. Everything else cold and live-pegged.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**1. `[#501]`'s path is sanctioned but the directory does not exist, and that was deliberate.**
The operator approved `.github/workflows/` as a *path in the row*, explicitly creating nothing
this window, so **zero coupled gates have fired yet**. At BUILD they will: hermetization sanction
(ADR-101 closed sets), the parity root row, the derived-tree prose-edge exclusion, doc-counts
regen, and the codemap check — roughly five, and the standing precedent is to conform them **by
precedent, in the same commit**, never by dispositions. The open question is whether that
conformance rides `[#501]`'s build commit or is split; splitting it means main briefly carries an
unsanctioned tree.

**2. The tier answer forecloses a plan people will otherwise keep making.** The account is
**Free** and the repo stays **private** by standing ruling (employer material), so `[#501]` has
**no promote-to-gate path** — it is a report-only recorder indefinitely, and **the ADR-at-arming
has no live trigger until the tier changes**. This is written into the row precisely so nobody
drafts that ADR early. The value is real and narrow: a server-side record no `--no-verify` can
erase. Revisit only if the tier changes.

**3. `[#502]` is structurally blocked on `[#501]`, not merely sequenced after it.** mutmut needs
`fork()`; Windows-native is out; WSL is out by operator constraint; so CI is the only host and
the wall must exist first. The dependency edge is written into both row bodies. One empirical
unknown survives deliberately: **`mutmut` under `uv run --locked` is NOT VERIFIED** — settle it
by running the pilot, not by more reading.

**4. `[#504]` owes a terra review before merge, and carries a trap in its own body.** The
`:153`/`:169` fail-soft descriptions in `block_ff_push.py` are **correct** and are not to be
"fixed" — only the module-level posture claim at `:39` (and `ARCHITECTURE.md:327`) contradicts
the ADR-85 §A6 fail-closed flip. `[#501]` and `[#504]` share `serialize-group: architecture`
because both touch `ARCHITECTURE.md`; run them serially, never concurrently on that file.

**5. Three V-1 doctrine lessons are owed into `STANDING_RULINGS.md` next window**, along with the
**B2 label update** (today's register edit was held to A2 by ruling): (i) the exact `uv` pin is
load-bearing for the *entire* organ mesh — the mesh is wrapped in `uv run --locked`, and an
unpinned environment silently loses both the commit gates and the `Stop` hook, which has **two
distinct silences and only one means "fine"**; (ii) mid-flight corrections to a probe lane are
indistinguishable from injection — load-bearing content belongs in the lane's *original*
contract; (iii) **no read of `origin/*` is evidence about the remote without a fetch first** —
the night session reasoned about exactly this risk and still got it wrong, calling
`git ls-tree origin/main` "ancestry-free" when it reads a *local* tracking ref.

**6. `[#499]`'s flip evidence chain has STARTED and can be broken by silence.** This window is
seal #1 with a false-positive count of **zero** on local gates. The bar is zero across **two
consecutive** seals, and nothing mechanically enforces the reporting — a seal that omits the
count does not merely fail to advance the chain, it breaks it. The next seal owes the count
explicitly. Related: the cloud's `canonical_freshness` FAILs were **shallow-clone environment
artifacts**, not false positives of this leg, and must not be counted against it.

**7. The `[#296]` finding generalizes, and that is the part worth keeping.** `audit.py repo
--repo-path` does write its report — to the `automation/fleet-audit` replication branch — so the
path it prints resolves to nothing in the working tree. The class is **"the artifact exists, the
locator lies"**, which no gate catches because nothing is missing. Worth asking whether other
ADR-80 replication paths print working-tree locators for branch-resident artifacts.

**8. `[#487]` stays L and out of the first batch.** Its re-scope inverted the order for a reason:
adjudicating 149 parked proposals produced by a defective pipeline just re-parks them. Legs (i)
and (ii) share one root cause — nothing writes `- [x]`, so an unchecked-still-open id pins
`since_commit` open forever. Repair before consumption.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
