# NB2 · LANE C packet — [#610] the night-batch protocol chapter (RATCHET LANE)

**Branch:** `worktree-lane-c-610-night-protocol` · **Contract of record:**
`docs/audits/2026-08-28-technical-batch2-launch-contracts/NB2-LANE-C-610-night-protocol.md`
(architect's lane id **N3**) · **Substrate:** local · **Written:** 2026-08-29.

**Headline, stated before the detail so it is not buried.** The ratchet authorization this lane
carried — the batch's only one — **went unused**. The section is **token-free**: silent-rule-v5
measured **443 before the first commit and 443 after the last**, files 61 → 61, delta **ZERO**.
The diff against `main` is **273 insertions, 0 deletions** across exactly the two files in
write-scope, so
Ch8's dispatch table and its Q1 row are untouched by construction rather than by assertion.

---

## 1 · Per-done-item verdicts

Every row carries a witness. A claim with no witness is not a claim.

### (1) A named PLAYBOOK section enumerating all five phases, each with inputs, outputs, refusal conditions — **MET**

`protocols/PLAYBOOK.md:2179` `### The night batch — the batch protocol run unattended, in five
phases`, running to `:2415` (the section ends where `### Dispatch visibility` resumes at `:2416`).
It carries a five-row phase table and then one `####` block per phase, each opening with
*Inputs.* / *Outputs.* and closing with *Refusal conditions.*

```
$ grep -n '^#### Phase\|^### The night batch\|^### Dispatch visibility' protocols/PLAYBOOK.md
2179:### The night batch — the batch protocol run unattended, in five phases
2214:#### Phase 1 — Dispatch
2232:#### Phase 2 — Manifest
2273:#### Phase 3 — Night run
2309:#### Phase 4 — Morning adjudication
2328:#### Phase 5 — Ledger
2416:### Dispatch visibility — Agent View shows DISPATCHED sessions only (STANDING_RULINGS B7)
```

**Terra caught this one at PARTIAL, and it was fixed rather than argued.** On `7156d432` phase 2
carried *Inputs.* and *Outputs.* but **no *Refusal conditions.*** — the only phase of the five
that did not. `4db2e107` adds four (PENDING absent rather than empty · a Reports block short a
field · a Verification section that repairs a deviation instead of recording it · a dispatch half
landing after the lanes boot). The verdict above is MET **as of `4db2e107`**, and was PARTIAL
before it.

**Placement decision, stated as the contract asked.** The section is a **`###` sibling under
Ch8**, not a new chapter, placed immediately after *"The wave close"* and immediately before
*"Dispatch visibility"*. Three reasons, in order of weight: intake #60's own open question
answers itself (*"It is a session-boundary protocol by shape, which argues for Ch8"*); a new
chapter would renumber Ch12–Ch14 and break every cross-reference to them for a purely cosmetic
gain; and the position groups it with the batch protocol / lane lifecycle / wave close it
composes, while leaving the contiguous dispatch-mechanics block (Dispatch visibility → Model +
effort) intact. It was **not** appended at the end of Ch8 because the lane-lifecycle text calls
*"Handoff prep for the next architect"* **"this chapter's closing subsection"** — appending after
it would falsify that sentence, which is the drift class this repo exists to refuse.

### (2) Manifest shape specified so two seats produce identical sections; the 2026-08-27 landed manifest validates as the reference instance — **MET**

`protocols/PLAYBOOK.md:2244-2263` specifies four ordered clauses — header · `## Reports` ·
`## PENDING` · `## Verification` — followed at `:2265-2271` by the phase's refusal set. Validated clause-by-clause against
`docs/audits/2026-08-27-technical-night-harvest-manifest.md` (3,695 B, 55 lines):

| Clause | Reference instance | Verdict |
|---|---|---|
| header names the night, the read-only transport, and what was written where | `# CLOUD-NIGHT MANIFEST — harvest of 2026-08-26` + *"`GET /v1/code/sessions/{cse_id}/events`, paginated by `next_cursor`"* + *"Nothing was written to any repo; these five files are the only artifacts."* | validates |
| `## Reports`, a labelled block per session carrying four fields in a fixed order | four blocks (`**1. night c1 doc-diet**` …), each with `file:` `bytes:` `first heading:` `top recommendation:` | validates |
| `## PENDING`, written out even when empty | `## PENDING` → *"None. All four sessions had delivered their report before the first wake."* | validates |
| `## Verification`, deviations recorded rather than repaired | `## Verification` → the C1/C3 prose-preamble record | validates |

### (3) Byte-identical-or-state-the-deviation, citing the two C-reports that opened with prose — **MET**

`protocols/PLAYBOOK.md:2287-2294`. The rule is stated (*"the artifact wins and the Verification
section records the deviation"*) and the worked example names both reports and both facts: C2 and
C4 open at byte 0 with their own heading; **C1 and C3 do not** — each wrapped its report in a code
fence behind one line of prose, putting the heading on **line 4**. Both were landed verbatim; both
deviations were written into Verification. Source:
`docs/audits/2026-08-27-technical-night-harvest-manifest.md` §Verification.

### (4) Report-selection rule names the Stop-hook-noise trap — **MET**

`protocols/PLAYBOOK.md:2295-2303`. States that the report is **not** reliably the last assistant
text; names the trap at its measured cause (trailing Stop-hook backpressure — *"Unchanged. Done."*,
*"Nothing further."* — from a container where `uv run --locked` could not start, uv 0.8.17 against
the pin `==0.11.19`); states the consequence (taking the last text harvests noise, four times
over); states the rule that held (**longest assistant text**, which was #2, immediately after the
RECEIPT in all four sessions); and adds the checkability beat — name the selector in the manifest,
so a wrong selection is visible rather than silent.

### (5) Ledger is a REQUIRED output — **MET**

`protocols/PLAYBOOK.md:2328-2346`, `#### Phase 5 — Ledger`: *"The ledger is a REQUIRED output of
the protocol, not an optional one."* Reference instance named
(`docs/audits/2026-08-27-technical-night-harvest-consumption-ledger.md`); the rejected-items-stay-
listed rule carried; intake #60's open question (`docs/audits/` vs a handoff bundle) **answered**
on the reference instance's precedent, with the reason given; and two refusal conditions stated.

### (6) intake-#60 constraints travel here — **MET**

`protocols/PLAYBOOK.md:2348-2368`, `#### The night's four standing constraints`: the ~5
proposals/night cap · 7-day auto-expire · no autonomous semantic refactoring at night · proposals
land in `docs/intake/` as `status: SEED`. Each carries its reason, and the block closes with the
honest limit that all four are prose and `[#271]`'s survival review has not been run.

**Provenance correction, recorded rather than smoothed.** The contract calls these *"intake-#60
constraints"*. They are **not in intake #60's text** — I opened it
(`docs/intake/2026-08-27-tech-night-batch-protocol.md`) and it carries none of the four. Their
actual chain is: intake brief #1 §6
(`docs/intake/archive/2026-07-06-functional-architect-nightly-loop.md:49`) → `[#271]`, whose
**2026-08-28 K4 re-cut** struck that row's rival charter and routed the list onward → `[#610]`,
whose row body says so in terms (*"the intake brief #1 §6 constraints … travel here as the
protocol's own constraints rather than living in a rival charter"*,
`tasks/610-the-night-batch-protocol-named-with-its-two-verb.md:12`). The section cites that chain
rather than the contract's shorthand, because a locator that does not resolve is the defect class
this batch was built to catch.

### (7) prior-seat R-Q1/R-Q2 land as doctrine + HANDOFF_PROCESS forms-card carries both — **PARTIAL**

**The doctrine half is MET.** `protocols/PLAYBOOK.md:2370-2404`,
`#### Two standing boundary rules the night inherits`:

- **(a) session boundary** — the architect does not propose session closure and does not initiate
  the bundle; the operator declares closure; the window rhythm *boot → plan → freeze → GO →
  integrate → audit → next batch*. Witness: seat lesson **L-S2**,
  `docs/audits/2026-08-28-technical-night-mission-authorization.md`.
- **(b) substrate routing** — ruling **Z-G3** (`protocols/STANDING_RULINGS.md:3149`), its three
  W4 defects, `LOCAL` as the conditional default, the smoke-6 receipt that has not been produced,
  and the untouched 2026-08-20 Codespaces position. The **uv nuance** is stated at the resolution
  the night measured — *unrunnable by default, runnable after a one-step `pip install --target`
  provisioning* — sourced to `docs/audits/2026-08-26-technical-handoff-census.md` Appendix B.

**The forms-card half is PARTIAL, and the gap is structural rather than an omission.**
`protocols/HANDOFF_PROCESS.md:169-192` now carries a **FORMS-CARD DELTA** clause naming both
lines and binding them to their doctrine home, rendered-not-copied in the same shape form 1 uses
for the dispatch line. But the card a bundle actually ships is rendered from
`templates/handoff/v5/HANDOFF_BOOT.md.tmpl`, and `templates/` is **outside this lane's
write-scope** — the shared clause A5 puts every non-C lane's `protocols/+templates/` delta at 0
and this lane's scope names two `protocols/` files and nothing else. So **the spec asks for the
two lines; no generated bundle carries them yet.** The clause says exactly that in its own honest
limit rather than reading as shipped. Candidate filing C-2 below carries the remainder.

### (8) Ratchet old → new reported — **MET**

```
BEFORE (working tree clean at HEAD, pre-edit)     AFTER (staged, pre-commit)
detector: silent-rule-v5                          detector: silent-rule-v5
files:    61                                      files:    61
count:    443                                     count:    443
```

Delta **0**. Dispatch-time measurement (443 / 61 / silent-rule-v5) reproduced exactly at boot, so
the baseline was confirmed rather than assumed. The audit check agrees:

```
[OK] silent_rule_ratchet: live 443 <= baseline 443 under detector silent-rule-v5 (61 file(s) in scope)
```

**How token-free was achieved, since "we managed it" is not a method.** The detector counts
`\b(?:must|shall|never)\b` case-insensitively over `protocols/*.md`, `templates/**`,
`ecosystem/*.yaml`, reading **staged blobs** via `git ls-files -s` → `git cat-file`. The section
was drafted, then scanned mechanically before staging; the single hit was a *quoted heading*
(Ch11's `"What every routine must meet"`), which was replaced by a descriptive reference
(*"Ch11's operational standard for a routine, item 7 — the n=2 graduation gate"*) rather than by
mangling the heading text. Normative force is carried by refusal grammar instead — *refuses*,
*is a defect*, *does not*, *has left the envelope*, *stays UNVERIFIED-UNTIL-LOCAL*.

**The `--accept` path was not taken and no baseline was raised.**

---

## 2 · Commits on this branch, in order

| # | SHA | What |
|---|---|---|
| 1 | `7156d432` | `docs(playbook): name the night-batch protocol — five phases, manifest shape, ledger required [#610]` — the section, the Ch11 pointer, the regenerated PLAYBOOK TOC, the HANDOFF_PROCESS forms-card delta |
| 2 | `4db2e107` | `docs(playbook): phase 2 gains its refusal conditions; the manifest block's label is not one of its four fields [#610]` — discharges terra's one High, plus one defect this lane found in its own text |
| 3 | *(this packet)* | `docs(audit): NB2 lane C packet — [#610] night-batch protocol` |

`git diff main..HEAD --numstat` → `29 0 protocols/HANDOFF_PROCESS.md` · `244 0
protocols/PLAYBOOK.md`. **Zero deletions against `main`** is the mechanical proof that the
dispatch table, the Q1 row and every other pre-existing line of both files are byte-unchanged —
terra verified the same property independently. (Commit 2 reads `13 insertions, 5 deletions`
against commit 1; those five lines are its own, written an hour earlier.)

**No generated-surface regeneration except the one a gate forced:** the PLAYBOOK **TOC**, which
`toc-freshness-playbook` blocks the lane's own commit without. The contract named that regen as
inside this lane. It rides in commit 1 rather than its own commit because it is a two-line
addition to a gated block inside a file this lane already owns, and splitting it would produce a
commit that cannot pass its own gate.

---

## 3 · Terra tally

**Reviewer:** `codex exec --model gpt-5.6-terra -c model_reasoning_effort=high --sandbox read-only`,
run over `7156d432` from this worktree — `codex exec`, not `/codex-review`, because that lane dies
on a mixed doc/code diff. 70,649 tokens.

```
Critical: 0 · High: 1 · Medium: 0 · Low: 0
```

**The one High — CONFIRMED, and discharged by `4db2e107`.**

> `[HIGH] protocols/PLAYBOOK.md:2232 — Manifest phase lacks refusal conditions.` Phase 2 supplies
> `*Inputs.*` and `*Outputs.*` … then moves through the manifest specification directly to
> `#### Phase 3`; unlike phases 1, 3, 4, and 5, it has no refusal-conditions clause. This misses
> the frozen contract's requirement that every phase carry inputs, outputs, and refusal conditions.

It was right, and it is exactly the gap a self-review misses: phase 2 *looked* complete because it
was the longest of the five.

**Terra's own contract verdicts:** item 1 PARTIAL for the reason above, items 2–7 MET. And,
load-bearing, its **independent confirmation of this lane's hard constraints**:

> I verified the required hard constraints in the diff: only the two named `protocols/` files
> changed; the Ch8 dispatch table and Q1 were untouched; added lines contain zero
> `must`/`shall`/`never` matches.

**One defect terra did NOT find, self-reported here.** The `## Reports` clause read *"four fields
in this order: the session's label, `file:`, `bytes:`, `first heading:`, `top recommendation:"* —
five things under a count of four. The label is the block's heading, not a field. Also fixed in
`4db2e107`. A reviewer that finds one real High is not a reviewer that found everything.

**Terra's stated limits, carried rather than dropped:** it ran no validation or test commands and
audited nothing outside the diff. Every gate figure in §7 is this lane's own run, not terra's.

---

## 4 · Candidate filings for the integrator (reported, not filed)

Lane D is the batch's exclusive `tasks/` writer; nothing below was filed here.

- **C-1 · `HANDOFF_PROCESS.md` owes a version bump and a three-site re-stamp.** The forms-card
  delta changes a **registered spec** (`validate_reconciliation._SPEC_REGISTRY` → `handoff-process`
  → `protocols/HANDOFF_PROCESS.md`) without moving `Version: 6.3.0`. `coherence-nudge` fired and
  logged it, as designed:
  `2026-08-29T00:27:44 protocols/HANDOFF_PROCESS.md version=6.3.0 head=83dadbf4914c staged=6bcb4376ed38`.
  **The bump was deliberately not taken in-lane**: three dependents declare
  `reconciled_with: handoff-process@6.3.0` (`ARCHITECTURE.md:3`, `CLAUDE.md:3`,
  `CONTRIBUTING.md:3`), all three are outside this lane's write-scope, and bumping without them
  turns `check_reconciled_versions` **FAIL** → `audit-health` FAIL → the lane's own commit blocked.
  The integrator (or a follow-up arc) owns bump + three re-stamps + a `## Section history` entry,
  as one act. `check-against-spec` is the built organ for the re-stamp flow.
- **C-2 · `templates/handoff/v5/HANDOFF_BOOT.md.tmpl` owes the two boundary lines.** The spec now
  asks the forms card to carry them (item 7 above); the template that renders the card does not.
  Natural sibling of `[#602]` (*"Land the ruled dispatch verb in the bundle's forms card"*), which
  already owns the card's rendering seam. Until it lands, no bundle boots the two lines.
- **C-3 · "five-pillar close" is an unlocatable term.** The frozen contract and the frozen bundle
  both name it as part of the session-boundary rule. `grep -rn "five-pillar\|five pillar"` over the
  whole tree returns **only those two files** — it resolves to no doctrine surface. The two clauses
  the contract itself enumerates (architect does not initiate the bundle; operator declares
  closure) were landed; the term was **reported rather than reconstructed**. If it names a real
  five-part close, the prior seat owns stating it; if it was shorthand for the lane-lifecycle's
  five legs, saying so retires the term.
- **C-4 · X8's phase list and this contract's phase list differ, and the difference is now
  reconciled in prose rather than in the register.** X8 (`STANDING_RULINGS.md` §X) names *dispatch
  → sentinel → harvest → manifest → morning adjudication*; the contract names *dispatch · manifest
  · night run · morning adjudication · ledger*. The section reconciles them explicitly
  (`PLAYBOOK.md:2207-2212`): X8's "manifest" is the **return half only**, sentinel and harvest sit
  inside phase 3, and the ledger is promoted to a phase per intake #60's acceptance criterion 6. An
  X8 amendment marker recording that reconciliation is a **register** act, which this lane cannot
  take.
- **C-5 · The two verbs are the unbuilt half of `[#610]`.** `Dispatch-After` (documented in the
  section as the *deferred form of* the ruled `Dispatch` verb, §V, not a rival) and `Harvest-Cloud`
  are **win-tooling, operator-owned**. This lane is the doc half only; the row does not close on
  this branch. Lane N2/B carries the dispatch-verb half of the batch.
- **C-6 · `docs/audits/` `consumer_at_landing` WARNs will grow by one.** This packet lands as a new
  `docs/audits/` artifact with no citing governance surface, exactly like the other fifteen
  NB2 artifacts already WARNing. Inherited class, named so it is not rediscovered.

---

## 5 · Decisions taken under the V-2 budget

None escalated. The budget escalates on three classes only — curated-baseline touches, genuine
rule-vs-ruling conflicts, and fork classes with no standing ruling — and each decision below fell
outside them, so each was taken per contract defaults and is reported here instead.

1. **Placement: `###` sibling under Ch8, after "The wave close".** The contract explicitly
   delegated this (*"your call, stated in the packet"*). Reasoning in item (1) above.
2. **A pointer line added to Ch11's "Night-batch work" subsection** (`PLAYBOOK.md:3201-3206`), so
   doctrine (Ch11) and sequence (Ch8) point at each other instead of becoming two live readings.
   In write-scope (`protocols/PLAYBOOK.md`), not the dispatch table, token-free.
3. **`HANDOFF_PROCESS.md` version deliberately NOT bumped.** See candidate C-1. The alternative
   blocks this lane's own commit and requires three out-of-scope files. `coherence-nudge` is
   non-blocking by design and its log is the record.
4. **No `## Section history` entry added to `HANDOFF_PROCESS.md`.** Its entries are keyed to
   version bumps; adding one without a bump would put a version-less row in a version-indexed
   block, and the block is under the `doc_rot` 12-entry accretion threshold. Travels with C-1.
5. **Ch8's Q1 row cited, not resolved.** The dispatcher's honest note flagged the risk of two live
   readings in one chapter. The section states the routing answer **and** names Q1's *"amendment
   candidate, routing unchanged pending a ruling"* status verbatim, so a seat reading only the new
   text routes exactly as Q1 routes today. Q1 was not edited; the diff proves it (0 deletions).
6. **The uv nuance stated at the higher of two measurements.** Z-G3 says `uv` is *absent* from the
   container; the 2026-08-26 census measured it *present but wrong* (0.8.17 vs `==0.11.19`) and
   provisionable in one step. The section carries the **census** resolution because it is the later
   and more specific measurement, and attributes it. The routing conclusion is identical either
   way, so this is a precision choice, not a routing change.

---

## 6 · Deviations and inherited state, each with an owner

| # | What | Owner |
|---|---|---|
| D-1 | **Inherited RED:** `tests/test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings`. **Not this lane's.** All 8 findings are `BACKLOG#nnn` loci (`#146 #277 #171 #267 #297 #145 #82 #276`); this lane's diff is two `protocols/` files and touches neither `BACKLOG.md` nor `tasks/`. The same findings were present in the pre-edit baseline run of `validate_doc_rot.py --all` before a single byte was changed. Lane D (`[#612]` doc-rot archival) | integrator / lane D |
| D-2 | `coherence-nudge` fired on `HANDOFF_PROCESS.md` (non-blocking by design; logged). Deliberate — candidate C-1 | integrator |
| D-3 | Forms-card requirement landed; the template that renders the card did not — candidate C-2 | integrator / `[#602]` |
| D-4 | `[#610]` does **not** close on this branch: it is a two-half row and this lane is the doc half | `/review-closures` |
| D-5 | "five-pillar close" unlocatable — candidate C-3 | prior architect seat |

**Pre-existing REDs the contract named that did NOT fire here:** the full suite was not run
(targeted-only in-lane, per [#528]); `test_stale_worktrees` and the anchor-gate probe test were
outside the targeted set, so this lane makes no claim about them either way.

---

## 7 · Gate state at STOP

```
uv run --locked python scripts/audit.py health        -> health: OK
   [OK] silent_rule_ratchet: live 443 <= baseline 443 under detector silent-rule-v5 (61 file(s) in scope)
   [OK] dispatch_drift: 12 literal command(s) in Ch8's dispatch table resolve
   [OK] reconciled_versions: 8 reconciled_with edge(s) match live spec version(s)
   [OK] amendment_coherence: 2 coupled-surface version mention(s) coherent across 1 set(s)
uv run --locked python scripts/validate_doc_structure.py --all
   -> validate_doc_structure: OK - no structural rot (numbering / headers / ToC)
uv run --locked python -m scripts.toc.cli check protocols/PLAYBOOK.md   -> clean (exit 0)
uv run --locked pytest tests/test_toc.py tests/test_validate_doc_rot.py
  tests/test_validate_doc_structure.py tests/test_dispatch_drift.py tests/test_dispatch_surface.py
  tests/test_coherence_nudge.py tests/test_coherence_integration.py tests/test_coherence_enumerator.py
  tests/test_validate_reconciliation.py tests/test_handoff_modes.py tests/test_gen_handoff.py
  tests/test_verify_handoff_probes.py
   -> 390 passed, 1 failed (D-1, inherited) in 111.98s
git status --porcelain -> clean
git stash list         -> empty
```

---

## 8 · What this packet does NOT claim

- **No gate reads the new section.** It is prose, and it says so in its own `#### Honest limits`.
  No organ counts a night's proposals against the ~5 cap, expires an untriaged item at 7 days,
  checks a manifest for its four sections, or refuses a night that closes with no ledger.
- **The manifest shape was validated against ONE instance.** "Two seats produce identical
  sections" is an argument from the specificity of the clauses, not a measurement — no second seat
  has produced a manifest from this text.
- **The protocol has been witnessed once** (2026-08-26). By this chapter's own evidence gate
  (Ch11's operational standard, item 7) that is **n=1** — a recorded practice, not a graduated
  standard. The section states this itself.
- **The full suite was not run in-lane** (targeted-only, [#528]); it runs once at integration.
- **This lane did not journal, did not merge, filed no row and regenerated no shared index.**

---

**STOP.** Branch `worktree-lane-c-610-night-protocol` at its tip, handed to the integrator
queue. Merge order is the integrator's; this lane names no merge command.
