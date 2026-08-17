<!-- scope: meta -->
# Audit disposition ledger — batch 7a, lane a · 2026-08-17

**Produced by:** CC (`claude-opus-5`), batch-7a lane `a`, branch `worktree-lane-a-534-audit-dispositions`.
**Contract of record:** `docs/audits/2026-08-17-technical-batch-7a-lane-a-contract.md` (committed `875509bd`).

> *Architect standing ruling, 2026-08-17 — audit-to-row conversion authority.* Every audit artifact
> carries exactly one disposition: **ACTIONED** (conclusion already live — cite the commit),
> **FILED** (a row owns it — cite the id), **REJECTED** (a ruling declined it — cite it),
> **SUPERSEDED** (a later artifact replaced it — cite it). An undisposed audit is a defect, not a
> document.

---

## §0 · The answer first

```
audits 80 · ACTIONED 49 · FILED 25 · REJECTED 2 · SUPERSEDED 2 · PENDING 2
births 9 — [#534] [#535] [#536] [#537] [#538] [#539] [#540] [#541] [#542]
follow-on 49 earlier uncited audits, named in §4 (a named list, not a row — §1 says why)
```

**Three findings were re-verified against the live tree and turned out to be live and unowned**, which
is the whole return on this pass:

1. **Four open rows cite `scripts/audit.py` by a line number that no longer resolves** — `[#417]`'s
   pin `:4751-4760` is *past EOF* (the file is 4271 lines after the `[#533]` decomposition), and the
   same row is simultaneously proposed NOW-CLOSABLE by the closing campaign. → `[#534]`
2. **`audit.py` loads into two distinct module objects in one process** — `audit` and `scripts.audit`.
   Reproduced: patching `audit._FRESHNESS_FILES` leaves `enforcement_coverage._freshness_files()`
   returning the unpatched list, so a test can pass while exercising a module it never patched.
   → `[#535]`
3. **`ARCHITECTURE.md:427` still enumerates four `doc_rot` sub-detectors; the detector declares five**
   (`[#532]` split the BACKLOG scanner into two arms). `validate_doc_claims` checks 4 claims and this
   is not one of them, so nothing catches it. It was named in the batch-6 packet's Owed list and never
   paid. → `[#542]`

## §1 · Corpus, and why it is 80 and not 129

The contract's set is *every audit since 2026-08-14, plus every earlier audit no artifact cites as
consumed*. Measured mechanically over `git ls-files` (excluding the generated `docs/audits/README.md`,
which cites everything by construction, and excluding an artifact's citations of itself):

```
docs/audits/*.md tracked                     567
dated 2026-08-14 or later                     66
uncited anywhere in the tree                  83   (of which 20 are inside the 66)
earlier-and-uncited                           63
union of the two legs                        129   -> over the contract's cap of 80
ledgered here (newest 80)                     80   = the 66, plus the 14 newest earlier-uncited
named follow-on (§4)                          49
```

The 80/49 split falls on a clean date boundary: everything dated 2026-08-07 or later is ledgered, and
the follow-on is 2026-08-06 and older.

**The remainder is a named list, not a row.** The contract permits one row if the remainder is
genuinely its own arc; it is not. **30 of the 49 are `codex-*` review artifacts** whose fixes
typically landed in the same commit that added them — the `2026-07-27-codex-436-ratchet*` series
alone is 8 files from one gate-by-gate sweep, plus its parent `codex-436-silent-rule-ratchet` — and
**3 are `conformance-nightly-digest` files** of exactly the class this pass dispositioned three of.
That is a mechanical second pass, not an arc.

## §2 · The ledger

**Method.** Every `final metric line` cell below is extracted **verbatim from the artifact by a
program**, never retyped — by anchor where the artifact's summary line is not its last paragraph,
otherwise the last paragraph. Cells longer than 300 characters are truncated with ` …` and nothing
else is altered except `|` escaping. Dispositions are derived against the **live tree**, not against
what an artifact says about itself; where an artifact's own claim disagreed with the tree, the tree
won and the disagreement is recorded in the evidence column.

**A note on the REJECTED/PENDING conventions used here, stated so a reader can check them:**

- **REJECTED** is used where a named authority declined the finding, not where the finding merely
  went away. Two cases: a nightly conformance digest whose adversarial skeptic stage killed **all**
  of its raw findings (citing that artifact's own `§Killed Findings` block, which names a kill reason
  per finding); and `codex-o-review`, whose one HIGH the phase-1 adjudication ruled *"an operator
  decision, not an unnoticed bug"* — the fix was declined and the hole is carried verbatim as a
  stated limit in the `CLAUDE.md` §9 `block-commit-on-main` roster row rather than papered over.
- **PENDING** is used only where the decision is genuinely not this lane's: an operator GO on intake
  transitions and a bundle deletion, and a scope question on a low-severity finding set. Each carries
  the exact question it needs. A wrong ACTIONED retires a live finding, so PENDING is the correct
  answer where the evidence stops.

| file | final metric line (verbatim) | disposition | evidence locator |
|---|---|---|---|
| `docs/audits/2026-08-17-technical-batch-7a-manifest.md` | …  close, or edit a single BACKLOG row. **Births — ZERO.** The 24 reserved ids are *reserved*, not allocated: no `tasks/` file exists for any of them at this instant, and each is born by its own lane's own commit or not at all. - It does not edit `protocols/STANDING_RULINGS.md` or any register. The 20 … | **ACTIONED** | `f72541c1` opened it at dispatch; merged `397cfdae`. This batch is running under it now. |
| `docs/audits/2026-08-17-technical-batch-7a-lane-a-contract.md` | **If the set exceeds 80: ledger the newest 80 and list the remainder as a named follow-on — do not stall.** The follow-on is a named list in the ledger, not a row (a row for "finish the ledger" is a process row; the architect ruling births rows for CONCLUSIONS, not for lane residue) — unless the rem … | **ACTIONED** | `875509bd` — step 0 leg 3 of this lane; the ledger below is its step 2/4 discharge. |
| `docs/audits/2026-08-16-verification-nb6-backlog-truth.md` | **Claims verified 26/31 · mismatches: `[#417]`'s conversion replaced a met clause with an unmet one and its new locator is already dead (§1.8) · `[#531]` still records three occurrences, not four (§1.1) · untestable denominator 29 → 28 arithmetic, 19–57 measured band (§2.2) · the ARM-1 RED has two l … | **FILED** | births `[#534]` `[#535]` `[#536]` `[#537]`; queue items already owned by `[#533]` `[#293]` `[#492]` `[#506]`; §1.7's ten unmerged reports ACTIONED at `70e01a46` |
| `docs/audits/2026-08-16-verification-nb6-achievements.md` | **net-closed 0 (5 closed, 5 born) · mechanisms-live 4 of 6 shipped (`block-commit-on-main`, `doc_rot` two arms, manifest-at-dispatch, 16/43 decomposed — `telemetry_emit` and `single_flight` are landed with zero call sites) · promised-with-dates 5 of 5 answered, but only 1 carries a calendar date (Gr … | **FILED** | `[#505]` — the batch/finish-line program row owns net-closure and the under-100 target |
| `docs/audits/2026-08-16-verification-nb4-playbook-gap.md` | TALLY      covered 1 / partial 6 / absent 6   (of the 13 rows the brief enumerates) | **FILED** | birth `[#538]`; verified live — none of the 12 acts is in `protocols/PLAYBOOK.md` (0 hits for `Honest-RED`, `Land-then-delete`, `Position 0`) |
| `docs/audits/2026-08-16-verification-nb4-equilibrium.md` | **JUDGMENT 13 · MECHANIZABLE 13 · ALREADY-MECHANIZED-BUT-BYPASSED 2 (+5 already-mechanized and used, of 33 acts); the single highest-leverage mechanization is M1 — `gen_lane_contract.py` as assembly-not-generation with a `--check` pre-commit leg — because it moves the measured 48.3% mechanical half … | **FILED** | birth `[#539]`; verified live — `gen_lane_contract` has zero occurrences in `tasks/`, `protocols/`, `scripts/` |
| `docs/audits/2026-08-16-technical-w2f-conversions-lane-contract.md` | ## LANE f — CONTRACT-W2F.md · worktree `worktree-lane-f-130-conversions` Ids #130 #274 #350 #417 (#417 conversion carries the unlanded remainder per phase-1 D6.4(b)). Same. OWNED-FILES: 4 tasks files. | **ACTIONED** | `8e8d55a2` — batch 6 merge 5/11, lane f |
| `docs/audits/2026-08-16-technical-w2d-lane-contract.md` | Live checks at step 0: - `git worktree list` shows eleven provisioned lanes (`a b c d e f g h i k m x` — k not dispatched per the manifest) plus the primary; lane **d** is this checkout, branch `worktree-worktree-lane-d-351-conversions`, unique. - OWNED-FILES resolved to the five task files named by … | **ACTIONED** | `4ca67eed` — batch 6 merge 7/11, lane d |
| `docs/audits/2026-08-16-technical-w2c-conversions-lane-contract.md` | ## LANE c — CONTRACT-W2C.md · worktree `worktree-lane-c-146-conversions` Ids #146 #266 #438 #443. Same. OWNED-FILES: 4 tasks files. | **ACTIONED** | `b4862b9b` — batch 6 merge 3/11, lane c |
| `docs/audits/2026-08-16-technical-nb6-handoff-prep.md` | **Nothing here is ruled or filed.** `[#453]` already owns the class and its Done-when already names the runbook; this is evidence against that row, not a new one. The `Stop` hook is **advisory in full** (ADR-85 amendment 2026-08-03 §A5) and has no hard leg, so nothing was bypassed and there was noth … | **FILED** | `[#453]` — the report names it as the owning row and declines to file a new one |
| `docs/audits/2026-08-16-technical-nb5-seam-repoint.md` | … g a cleaner result than I measured. - **H2 is a pre-existing defect this report does not fix.** `audit.py` is executed twice per pytest session today via `scripts/enforcement_coverage.py:566`. The proposed design is immune to it, but the double execution remains — wasted work, doubled import side ef … | **FILED** | `[#533]` (seam work, open) + birth `[#535]` for the H2 defect the report explicitly declined to file |
| `docs/audits/2026-08-16-technical-nb5-consumer-home.md` | **Compiled by:** CC (`claude-opus-5`), lane nb5-B, 2026-08-16. Read-only w.r.t. every consumer repo and w.r.t. the hub spine; this report and the regenerated `docs/audits/README.md` index are the lane's entire write footprint. | **FILED** | `[#293]` (BLOCKED-ON-RULING) + `[#303]` (its named prerequisite), both open |
| `docs/audits/2026-08-16-technical-nb4-telemetry-read.md` | **Two prerequisites that belong to `[#529]`, not to Stage 2, and should be stated on that row before either D1 or D2 is scheduled:** leg 1 must say *time the checks*, not merely *wire the call sites* (F1); and the `default_db_path()` worktree split must be fixed via `git rev-parse --git-common-dir`, … | **FILED** | `[#529]` — the report's two prerequisites are that row's legs; RESIDUAL: neither is stated on the row yet |
| `docs/audits/2026-08-16-technical-nb4-llm-acceptance.md` | **Gemini enters second, in the fan-out (retrieval) role only** — where seeds NB4-F-1 and NB4-F-2 test exactly the property its ruling is about, its free tier makes the run cost nothing, and its Windows story (Windows 11 24H2+, PowerShell, Node 20+) is the better of the two on the operator's actual m … | **FILED** | `[#491]` (open) — the R-G Gemini ruling is that row's own first move |
| `docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate-v2.md` | **Secondary `[2°]` — re-verify on the vendor's page before spending:** [Codespaces pricing](https://toolradar.com/tools/github-codespaces/pricing) · [Codespaces prebuilds](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds) · [Hetzner cloud price incr … | **FILED** | birth `[#541]` — verified live: no row anywhere in `tasks/` owns the scale-out substrate decision |
| `docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate.md` | > **This document is superseded by > `docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate-v2.md`.** > > Route per CLAUDE.md §5 rule 3: an immutable audit is superseded **with a new file**, and this > marker is the pointer. Nothing above is edited or withdrawn — §0–§5 and AMENDMENTS 1–3 remain … | **SUPERSEDED** | `docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate-v2.md`, via the artifact's own in-file supersession marker |
| `docs/audits/2026-08-16-technical-nb4-fleet-parity.md` | **in-parity 2/8 · seeding-ready 0/8** | **FILED** | F1 → `[#293]`/`[#303]`; F2 (`corp-sca-time-automation` divergent-silent) → `[#393]`, all open |
| `docs/audits/2026-08-16-technical-nb4-consolidated-briefing.md` | **Three deliberate non-actions, each on a rule this repo already carries.** The pin is **not bumped** — `pyproject.toml` states a uv upgrade *"is its OWN gated change … never incidentally mid-arc"*, and this is a read-only lane. **No row is born** — `[#453]` owns this class and its `kill-candidates: … | **ACTIONED** | `70e01a46` landed it; its three non-actions are deliberate and each cites the rule it defers to |
| `docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md` | - corp-monorepo: `# Handoffs — operator runbook (`corp-monorepo`)` - corp-ops: `# Handoffs — operator runbook (`corp-ops`)` - corp-sca-time-automation: `# Handoffs — operator runbook (`corp-sca-time-automation`)` - life-architect: `# Handoffs — operator runbook (`life-architect`)` - terminal-setup: … | **FILED** | `[#293]` — the row carries the full BLOCKED-ON-RULING record and names `[#303]` as prerequisite |
| `docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-contract.md` | ## LANE k (OPTIONAL — operator word) — CONTRACT-K-293-SEEDING.md · worktree `worktree-lane-k-293-seeding` Feature/satellite: execute the [#293] cross-repo seeding per the corrected row (0-of-8, ADR-104 members): for each consumer repo, seed its runbook per the row's Done-when on a feature branch in … | **ACTIONED** | `94f9307b` — batch 6 merge 11/12, lane k |
| `docs/audits/2026-08-16-technical-batch-6-packet.md` | … writes, not test-pin dependencies.* - **Owed:** the D3.1–D3.5 promotions, `ARCHITECTURE.md:427`, and the `[#415]`/`[#425]` Form-E repairs. … | **ACTIONED** | `1829d86a` + `88422f5c` (batch 6 closes). RESIDUAL: of its Owed list, `ARCHITECTURE.md:427` is still unpaid → birth `[#542]`; D3.1–D3.5 are recorded at STANDING_RULINGS M-7/M-8/M-9; `[#415]`/`[#425]` are open rows |
| `docs/audits/2026-08-16-technical-batch-6-manifest.md` | **Ruled a DISPATCH-TEMPLATE defect, not lane error.** No lane authored its own branch name. | **ACTIONED** | `cd5cd32d` opened it, `1829d86a` closed it; the open provisioning class is `[#531]` |
| `docs/audits/2026-08-16-technical-82-conversions-lane-contract.md` | ## Done-when (frozen) (1) Each of `[#82]` `[#145]` `[#239]` `[#263]`'s Done-when clause reads its wave-2 draft verbatim; (2) `BACKLOG.md`/manifest regenerated clean, `validate_backlog` OK; (3) lane packet: T_start · manifest as executed · per-step commit shas · targeted-test evidence · deviations se … | **ACTIONED** | `65cd26a0` — batch 6 merge 4/11, lane e |
| `docs/audits/2026-08-16-technical-533-audit-decompose-lane-contract.md` | **Row update:** set `[#533]`'s status at the `tasks/` source and regenerate; do **not** hand-edit `BACKLOG.md`. | **ACTIONED** | `d714cfea` — batch 6 merge 12/12, PARTIAL BY DESIGN (16 of 43 extracted); `[#533]` stays open for the remainder |
| `docs/audits/2026-08-16-technical-532-docrot-arms-lane-contract.md` | ## LANE x — CONTRACT-H1-DOCROT-ARMS.md · worktree `worktree-lane-x-532-docrot-arms` [HUB] Execute the ruled §A6 amendment on validate_doc_rot: split into ARM 1 backlog-accretion (citation-blind distinct dates ≥3 AND span ≥30d AND >700ch) + ARM 2 backlog-row-length (declared ceiling 1320, no percenti … | **ACTIONED** | `e2403a44` + the close restore `121c3417`; `[#532]` closed |
| `docs/audits/2026-08-16-technical-409-conversions-lane-a-contract.md` | ## LANE a — CONTRACT-W2A.md · worktree `worktree-lane-a-409-conversions` Ids #409 #410 #411 #419. Apply each id's reviewed draft from docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md to its tasks/<id>-*.md Done-when (Form R for the routine trio — the conversion IS the ruled declaration … | **ACTIONED** | `51d7fa08` — batch 6 merge 1/11, lane a |
| `docs/audits/2026-08-16-technical-310-ledger-docs-lane-contract.md` | - `protocols/PLAYBOOK.md` — K1 declares (L1183 handoff-process, L1739 prompt-template) - `protocols/SESSION_SETUP.md` — K1 declare (L191 handoff-process) - `ecosystem/disposition-register.yaml` — the 14 K2/K3/K6 permanent-defer re-annotations (the contract names "the 14 edge docs"; the re-annotation … | **ACTIONED** | `b150bfe4` — batch 6 merge 8/11, lane h |
| `docs/audits/2026-08-16-technical-277-issues-evidence-lane-contract.md` | ## LANE i — CONTRACT-L9-ISSUES-EVIDENCE.md · worktree `worktree-lane-i-277-issues-evidence` Finish-line: (1) close the 15 triage Issues via gh (list = the SessionStart 15), recording count 15 in the closing commit per D5, with the PARTIAL-discharge wording for #428 leg 2 quoted; (2) append the 154:0 … | **ACTIONED** | `fa746e14` — batch 6 merge 9/11, lane i |
| `docs/audits/2026-08-16-technical-271-conversions-lane-contract.md` | ## LANE g — CONTRACT-W2G.md · worktree `worktree-lane-g-271-conversions` Ids #271 #324 #391 #412 #491 (#391 = the ruled (a) shape — dead disjunct dropped; #324/#412 homes per A1; #412 conversion only, measurement leg NOT started per do-not #2). Same. OWNED-FILES: 5 tasks files. | **ACTIONED** | `9997bc32` — batch 6 merge 6/11, lane g |
| `docs/audits/2026-08-16-technical-210-conversions-lane-contract.md` | **Committed verbatim from the operator's frozen `~/Downloads/CONTRACT-W2B.md` (I-D3, step 0).** Batch-6 (phase-2) manifest: `docs/audits/2026-08-16-technical-batch-6-manifest.md` roster row **b** — rows `#210 #285 #361`, bucket finish-line, contract of record `CONTRACT-W2B.md`. | **ACTIONED** | `40dd51d8` — batch 6 merge 2/11, lane b |
| `docs/audits/2026-08-16-census-nb6-archive-sweep.md` | **Pending one operator GO, not a mechanism: 3 intake status transitions (#26, #28, #18) and 1 handoff bundle deletion (`[#300]`).** | **PENDING** | Q: does the operator GO the 3 intake status transitions (#26, #28, #18) and the `[#300]` handoff-bundle deletion? Not decidable by this lane — `docs/intake/**` is lane b's this batch and `[#300]` is `deferred` |
| `docs/audits/2026-08-16-census-nb4-closing-campaign.md` | **NOW-CLOSABLE 2 / AFTER-WAVE 0 / campaign batches 6** | **FILED** | `[#506]` (open) — the whole-set P10 grooming arc owns the campaign; its two NOW-CLOSABLE proposals (`#417`, `#506`) are both still `open`, awaiting `/review-closures` ratification |
| `docs/audits/2026-08-15-verification-night3-warn-ledger.md` | **Nothing in this document was applied.** No register entry written, no row born, no detector edited, no test changed, no branch or worktree created or deleted. The one experiment (§3.2) ran in a throwaway clone under the session scratchpad and was removed; `git status` is clean and `git worktree li … | **FILED** | `[#531]` + `[#532]`(closed) + `ecosystem/disposition-register.yaml`, each of which cites this artifact by name |
| `docs/audits/2026-08-15-verification-night3-landed-review.md` | **Proposed closeable: 1 — `[#527]` only.** | **ACTIONED** | its single proposal `[#527]` is `closed`; the gate landed at `60eefbb7` |
| `docs/audits/2026-08-15-technical-w20-draft-landing-lane-contract.md` | Rulings D6.1–D6.6 cross-checked live against `~/Downloads/MORNING-ADJUDICATION-2026-08-15.md` §A: D6.3 (`#391`) RULED (a) and D6.4 (`#417`) RULED (b) both verbatim-match this contract's step 2(b)/(c) wording — no drift between the ruling register and the dispatched contract. | **ACTIONED** | `bce5838a` — phase-1 lane s |
| `docs/audits/2026-08-15-technical-night3-sessionplan.md` | GO-READY:  NO as of this reading -- 6 of 8 phase-2 premises GO, 2 NO-GO. Both NO-GOs are clearable inside the adjudication hour; neither needs new work. | **ACTIONED** | batch 6 dispatched on this plan — `cd5cd32d` (manifest at dispatch); its §5 CORRECTION is carried by `[#484]` |
| `docs/audits/2026-08-15-technical-night3-research.md` | 1. **Q1 — change nothing about the invocation: the integrator's run already used xdist** (`addopts = "-n auto"`, confirmed live by `bringing up nodes...`), and the 1431 s is a ~2.95× Windows-host penalty over this container's 485.55 s on the identical tree, floored by one 269.73 s test; if one thing … | **FILED** | Q1 ACTIONED (`.claude/skills/verify/verify.py` + `protocols/PLAYBOOK.md` cite it live); Q2 unowned → birth `[#540]`, verified: `harvest_batch` has zero occurrences in-tree |
| `docs/audits/2026-08-15-technical-night3-decision-queue.md` | **Decisions queued 14, batch-ratifiable 5, stale drafts 0.** | **ACTIONED** | the 2026-08-15 morning adjudication ruled the queue — `d62796ad` (gate 41→11, closes #524 #352, births #529 #530) |
| `docs/audits/2026-08-15-technical-night2-consolidated-briefing.md` | **7 of 7 lanes present. No MISSING lanes.** Each branch was read via `git show <branch>:<path>`; no branch was merged, and the seven remain unmerged on `origin`. | **ACTIONED** | `ed3abe9f` landed the unique holds; merged `65dc3183` |
| `docs/audits/2026-08-15-technical-gateclose-drain8-lane-contract.md` | ## Steps 0b. COMMIT-if-changed — **[#523] verification (review item 3):** born 2026-08-12. Read its history: if the fat is its own BIRTH content → drain = trim the birth text, say so in the packet; if the accretion metric misfires on young rows → EXCLUDE #523 from the drain, and write the finding (m … | **ACTIONED** | `8c9163e0` — phase-1 lane r |
| `docs/audits/2026-08-15-technical-batch-phase1-packet.md` | - **Deleted nothing** — no branch, no worktree, no ref, local or remote. All 8 night-2 branches and all 7 lane worktrees are exactly as they were found. - **Did not close `[#527]`**, `[#528]`, `[#529]`, `[#530]` or `[#293]`. Only `[#527]` is *proposed*. - **Did not execute the `[#293]` cross-repo se … | **ACTIONED** | `b798d31d` + `6a80f98c` — closes batch 5 |
| `docs/audits/2026-08-15-technical-batch-phase1-manifest.md` | …  close, or edit a single BACKLOG row. **Births — ZERO.** … | **ACTIONED** | `a8208619` opened it; `b798d31d` (the phase-1 packet) closed it |
| `docs/audits/2026-08-15-technical-530-single-flight-lane-packet.md` | **STOPPED.** | **FILED** | `[#530]` (open) — the library is landed with zero call sites |
| `docs/audits/2026-08-15-technical-530-single-flight-lane-contract.md` | ## Steps 1. COMMIT — `single_flight.py`: claim/release/inspect; refusal message prints how to inspect and release a stale hold (no TTL in git — ruled residual, option (a)). 2. COMMIT — tests against a LOCAL BARE remote fixture: T1 claim-new ok · T2 unfetched-clone refused (stale info, exit 1) · T3 d … | **ACTIONED** | `50daad05` — phase-1 lane p |
| `docs/audits/2026-08-15-technical-529-telemetry-emit-lane-packet.md` | **STOPPED.** | **FILED** | `[#529]` (open) — landed with zero call sites; the EMIT legs are owed |
| `docs/audits/2026-08-15-technical-529-telemetry-emit-lane-contract.md` | **Explicitly NOT touched:** `scripts/audit.py`, any hook or dispatcher script, `pyproject.toml`, `uv.lock`, `BACKLOG.md`/`tasks/529-*.md` row state, `.gitignore`, `CLAUDE.md`, `ARCHITECTURE.md`. | **ACTIONED** | `4ad2025d` — phase-1 lane m |
| `docs/audits/2026-08-15-technical-528-legs12-packet.md` | **STOPPED.** Branch `worktree-lane-n-528-legs12-latency` is handed back at `d0610add` plus this packet commit. Not merged, not pushed. `[#528]` stays open — leg (3) is owed after `[#529]`. | **FILED** | `[#528]` (open) — the artifact itself states leg 3 is owed after `[#529]` |
| `docs/audits/2026-08-15-technical-528-legs12-manifest.md` | - `silent_rule_ratchet` measured **440 ≤ baseline 441** before any edit (`audit.py health`), i.e. one token of headroom. Both leg-2 targets sit in the detector's scope (`protocols/*.md`, non-recursive), so the doctrine is phrased declaratively and adds no `must\|shall\|never` token. - `protocols/ESS … | **ACTIONED** | `7d1f6ce0` — phase-1 lane n |
| `docs/audits/2026-08-15-technical-528-legs12-latency-lane-contract.md` | ## Steps 0b. COMMIT — print the DERIVED manifest (exact files + locators) as a packet artifact before editing. 1. COMMIT — leg 1: flags at the derived call sites (excluding O's files). 2. COMMIT — leg 2: the doctrine paragraph(s), declarative phrasing (ratchet!), citing the measured basis (serial 70 … | **ACTIONED** | `7d1f6ce0` — phase-1 lane n |
| `docs/audits/2026-08-15-technical-527-block-main-lane-contract.md` | ## Steps 1. COMMIT — the hook script: refuse non-merge commit when HEAD resolves to main; allow when MERGE_HEAD exists; detached HEAD passes (stated hole, by design). 2. COMMIT — tests = the acceptance matrix VERBATIM as cases: E1 refused · E2 allowed · E3 clean --no-ff merge never fires the hook · … | **ACTIONED** | `60eefbb7` — phase-1 lane o; `[#527]` is `closed` and the hook is live in CLAUDE.md §9 |
| `docs/audits/2026-08-15-technical-293-consumer-runbook-fan-out-lane-packet.md` | STOPPED. | **SUPERSEDED** | `docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md` — its STOP-and-report 0/6 was overtaken when the operator gave the word and lane k executed 7 of 8 |
| `docs/audits/2026-08-15-technical-293-consumer-runbook-fan-out-lane-contract.md` | ## Steps 1. COMMIT — per-consumer runbooks per the row's spec (one commit per coherent group), each home justified by a quoted source. 2. Targeted checks: any doc hooks touching your files. Packet: row's Done-when clause-by-clause vs delivered, 0/6 → n/6 stated. STOPPED. | **ACTIONED** | `dce393ec` — phase-1 lane q |
| `docs/audits/2026-08-15-codex-p-review.md` | It records that the review happened, against which branch and range, and what it said. It does not re-verify the two real findings on today's tree; both are live open legs on `[#530]`. Line numbers are as-of `73da833c`, the reviewed tip. | **FILED** | `[#530]` (open) — the artifact states both findings are live open legs on that row |
| `docs/audits/2026-08-15-codex-o-review.md` | It records that the review happened, against which branch and range, and what it said. It does not re-verify the finding on today's tree. Line numbers are as-of `9732daea`. | **REJECTED** | the phase-1 adjudication, quoted verbatim in the artifact, ruled its one HIGH an **operator decision, not an unnoticed bug**; the fix was declined and the hole is carried verbatim as a stated limit in the `CLAUDE.md` §9 `block-commit-on-main` roster row |
| `docs/audits/2026-08-15-codex-n-review.md` | It records that the review happened, against which branch and range, and what it said. It does not re-verify the finding on today's tree, and landing it does not close `[#528]` or discharge the finding. The cited line numbers are as-of `03814f6c`; note that `protocols/PLAYBOOK.md` has been edited si … | **FILED** | `[#528]` (open) — the artifact states landing it does not discharge the finding |
| `docs/audits/2026-08-15-codex-m-review.md` | It records that the review happened, against which branch and range, and what it said. It does not re-verify the finding on today's tree, and landing it does not close `[#529]` or discharge the finding — the finding remains open work, and the line numbers above are as-of `d45fdb9e`, not as-of `main` … | **FILED** | `[#529]` (open) — the artifact states the finding remains open work |
| `docs/audits/2026-08-14-verification-night2-plancheck.md` | 61 claims verdicted. Zero repo edits beyond this file and the regenerated `docs/audits/README.md` index. | **ACTIONED** | `ed3abe9f`; consumed by `docs/audits/2026-08-15-technical-night2-consolidated-briefing.md` |
| `docs/audits/2026-08-14-verification-night2-hygiene.md` | **The lesson, recorded because it is the same class this report audits:** a tool's own "version not found" was accepted as ground truth about availability without checking the package index. That is an unverified inference presented as a derived fact — precisely what §0.1 catches the shallow clone d … | **ACTIONED** | `ed3abe9f`; consumed by the night-2 consolidated briefing |
| `docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md` | **These drafts bind nothing.** They apply only under a later operator ruling, after architect review and the wave-2 GO. Conversion lanes consume this file; they do not inherit authority from it. | **ACTIONED** | the seven batch-6 conversion lanes applied the drafts — `51d7fa08` `40dd51d8` `b4862b9b` `65cd26a0` `8e8d55a2` `9997bc32` `4ca67eed`. ACTIONED means APPLIED, not correct: `[#417]`'s application replaced a met clause with an unmet one whose locator is already dead, which is `[#534]` |
| `docs/audits/2026-08-14-technical-night2-research.md` | In-repo locators cited above: `protocols/STANDING_RULINGS.md:973` (I-D3) · `scripts/fleet_health.py:730` (`O_EXCL` precedent) · `pyproject.toml:79-91` (mutmut/xdist interaction), `:100-103` (markers), `:140` (`addopts = "-n auto"`) · `.pre-commit-config.yaml:8,17` · `scripts/arm_hooks.py` docstring … | **ACTIONED** | `7d1f6ce0`; cited live by `protocols/PLAYBOOK.md` and `.claude/skills/verify/verify.py` |
| `docs/audits/2026-08-14-technical-night2-latency.md` | **Serial 11.7 min vs xdist 7.9 min (ratio 1.48×) vs proposed targeted-gate ~0.9 min.** | **ACTIONED** | `7d1f6ce0`; the measurement is cited live by `protocols/PLAYBOOK.md` and `.claude/skills/verify/verify.py` |
| `docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` | **Net for this packet:** 0 births, 0 closes performed by this act. It reports one row's discharge that already happened in the tree (`[#513]`, evidenced elsewhere) and states the current carried/closed split, the CODEX-524 landing, the W4 arithmetic, the git-surgery mechanism gap's new owner (`[#527 … | **ACTIONED** | `e4e1624b`; `[#513]` is `closed` and the git-surgery gap's new owner `[#527]` is `closed` too |
| `docs/audits/2026-08-14-technical-525-arch-organ-rows-lane-contract.md` | ## Done-when (frozen) (1) Each governing row's Done-when satisfied as written; (2) every new organ claim carries a live locator; (3) ratchet ≤ 441; (4) stamp current; (5) lane packet: shas · rows closed/advanced · decision-budget report · confirmation no W3/CORPUS-492-named file touched. | **ACTIONED** | `d581c60f`; `[#525]` is `closed` |
| `docs/audits/2026-08-14-qa-night2-quality.md` | **Findings: 0 HIGH · 3 MEDIUM (M-1, M-2, M-3) · 7 LOW (L-1 … L-7) · 10 total.** | **PENDING** | Q: do the seven LOW findings (L-1..L-4, L-6, L-7 and the L-5 count-pin maintenance cost) get an owner, or are they recorded accepted-with-reason? M-2/M-3/L-5 feed `[#529]`; L-5 re-measured live and the `43` count still AGREES at every pin, so it is a maintenance cost and not a live defect |
| `docs/audits/2026-08-14-codex-524-check-extensions.md` | **Disposition:** False positive — not this lane's edit. `git diff --stat main...HEAD -- tasks/manifest.json` (three-dot, merge-base-relative — what this lane actually changed) is EMPTY; `git status --short` confirms `tasks/manifest.json` carries zero uncommitted changes and no commit on this branch … | **ACTIONED** | `789a86a5` implemented it, `62f42dad` merged it; `[#524]` is `closed`. Its one HIGH was dispositioned in-artifact as a false positive of a two-dot diff range |
| `docs/audits/2026-08-14-census-night2-census.md` | **Generated** 2026-08-14 by the read-only night-2 census lane on `claude/night2-census-audit-btqr42`, base `main` @ `7bbb067`. **Zero edits beyond this file.** No close is executed by this artifact; every verdict above is a proposal for the booted architect's P10 pass ([#506]). | **FILED** | `[#506]` (open) — the artifact states every verdict is a proposal for the booted architect's P10 pass, which is that row |
| `docs/audits/2026-08-10-conformance-nightly-digest.md` | Expected: one untracked file (this digest). No other tracked files changed. ✓ Safety check passes. | **ACTIONED** | both PERSISTING findings re-verified FIXED on the live tree: `cf039756` (ARCHITECTURE `five carrier` → 0 hits, 6 files) and `6e76b3f0` (`protocols/ESSENTIALS.md:124` now says `/override` is RETIRED) |
| `docs/audits/2026-08-08-technical-lane-c-393-corpsca-rot-review.md` | **Deviation, stated plainly (item 5):** the commit is two files, not one — the contracted audit file plus the machine-regenerated audit index it is gate-required to update. Nothing else was written anywhere, in the hub or in corp-sca. | **FILED** | `[#393]` (open) — the corp-sca rot-review row owns the three verdicts and the prepared patch |
| `docs/audits/2026-08-08-technical-closure-wave-proposals.md` | **Produced by:** lane `worktree-lane-wave-closures`, `[#506]` closure-proposal wave. **Writes made by this arc:** this file, plus the `audit-index-freshness`-mandated regeneration of `docs/audits/README.md`. No `tasks/` edit, no `BACKLOG.md` edit, no `logs/` write, no write to the primary checkout, … | **FILED** | `[#506]` (open) — the closure-proposal wave belongs to the whole-set grooming arc; the artifact executed no close |
| `docs/audits/2026-08-08-conformance-nightly-digest.md` | **Raw:** 5 · **Survived skeptic:** 0 · **Killed false positives:** 5 | **REJECTED** | declined in-artifact: **0 of 5** raw findings survived its own adversarial skeptic stage — §Killed Findings K1–K5, each with a named kill reason |
| `docs/audits/2026-08-08-codex-lane-e-396-512-gitenv-scrub.md` | **Honest limit of this artifact:** the reviewer ran read-only and could not execute `pytest` (its sandbox disallows cache/temp creation). Every "CONFIRMED by reproduction" above is the lane's own reproduction, run in this worktree and cited in the fixing commit; the reviewer's contribution is the fi … | **ACTIONED** | `33fdc64f`; both reviewed rows `[#396]` and `[#512]` are `closed` |
| `docs/audits/2026-08-08-codex-deploy-doc-carrier.md` | D9 is satisfied: `_hub_text` is a shared spec read, not a correctness judgment. Empty `doc_paths` are rejected, and an empty existing document is treated as present. The non-atomic apply is explicitly recoverable because verification blocks staging/recording and a retry reconciles partial output. | **ACTIONED** | `295f3594` — the fix landed in the same commit that added the review artifact |
| `docs/audits/2026-08-07-conformance-nightly-digest.md` | … \| \| **PERSISTING** \| prior S2 (MED): VISION.md `last_reviewed: 2026-07-25` predates last content change 2026-07-26 \| Unchanged — stamp still backward-dated. Now seven days unfixed. Today's S1. \| \| **NEW survivors** \| — \| None. \| … | **ACTIONED** | its one surviving finding does not reproduce on full history: `VISION.md` `last_reviewed: 2026-07-25` vs last content change `30a8c42b` (2026-07-25), and `canonical_freshness_gate.py --all` runs clean live. The artifact's own shallow-clone caveat is the reason it read otherwise |
| `docs/audits/2026-08-07-codex-pre2-selfreview-arc.md` | Two consecutive reviews, two HIGHs, both on the exemption's committed-ness boundary — and the second landed on the fix for the first. A hardening that looks obviously correct is exactly the kind that needs a second reader, because the author has already convinced themselves. This is the fourth time … | **ACTIONED** | `d961bc12` — the HEAD-based committed-manifest fix landed in the same commit |
| `docs/audits/2026-08-07-codex-pre2-arc-retro.md` | `review_artifact_coverage` fired on the integrator's own merge, and the review found three defects in the exemption mechanism before batch 2 ran under it. The condition-3 clause that binds the integrator is not ceremony. | **ACTIONED** | `e62c412a` — all 5 HIGHs fixed in the same commit |
| `docs/audits/2026-08-07-codex-mutmut-sandbox-skip.md` | **Recorded rather than absorbed:** if [#502] moves to ADOPT, tightening this detection is part of that work, and this artifact is the reference. Until then the honest description is *the skip is keyed on a directory name and would fire for any tree so named* — which the test's own comment now says. | **FILED** | `[#502]` (open) — the artifact states the tightening is part of that row's work if it moves to ADOPT |
| `docs/audits/2026-08-07-codex-morning-f4-retro.md` | **Suite after the fixes:** `tests/test_stale_worktrees.py` 23 passed. | **ACTIONED** | `16269f79` — the two own-code defects were fixed in the same commit |
| `docs/audits/2026-08-07-codex-lane-b-503-retro.md` | **Not raised, and worth naming anyway:** line-number pinning in `tests/test_reverse_dep_oracle.py` is a known recurring maintenance cost in this repo — an `audit.py` insertion shifts it every time. Out of scope here (the row is closed and this is a retroactive pass), and it is already lived knowledg … | **ACTIONED** | `16269f79`; `[#503]` is `closed` |
| `docs/audits/2026-08-07-codex-lane-a-501-retro.md` | **Two known-open items were excluded from this review by the focus hints** and are therefore NOT evidence of absence: the `setup-uv` `python-version-file:` input (LA-2) and the `mutation-pilot` paths gating (LA-4). Both are fixed in the PRE-2 arc's step 3. | **ACTIONED** | `16269f79`; `[#501]` is `closed` |
| `docs/audits/2026-08-07-codex-lane-1-490-430-parity-manifest.md` | `--` inside a reason is preserved by the one-time split. A `RepoTarget.note` without `--` silently renders the generic fallback and loses any reason, though `resolve_fleet()` currently always emits the delimiter. No direct dangling disposition ID, RETIRE-ON-CLOSE citation, or old review-date referen … | **ACTIONED** | `b025c15e`; `[#490]` is `closed` and the artifact reports no live defect found |

## §3 · The FILED births — nine rows, and what each is sourced from

Each was **re-verified live before filing**; none is taken on the source artifact's word. `[#535]`
comes from a report that named the finding and *explicitly declined to file it* (*"It deserves its
own row; this report does not file one"*), and `[#542]` from a packet **Owed** list — a list that
owns nothing and is watched by no organ. Both are exactly the residue the standing ruling exists to
convert.

| id | sha | row | source artifact | live re-verification |
|---|---|---|---|---|
| `[#534]` | `dee37a4d` | `scripts/audit.py:<line>` locators on four open rows died at the `[#533]` decomposition | nb6-backlog-truth §1.8 | `audit.py` is 4271 lines; `#417` pins `:4751-4760` (past EOF), `#477` `:2300`→`:1862`, `#357` `:363`→`:490`, `#358` `:2425`→`:3405` |
| `[#535]` | `df6b63e9` | `audit.py` has two module identities in one process | nb5-seam-repoint §H2 (unfiled there) | `sys.modules` holds `audit` **and** `scripts.audit`, identity `False`; a patch through one is invisible to the other |
| `[#536]` | `69282bd9` | The ARM-2 row-length pile has no owner | nb6-backlog-truth §1.4 | `validate_doc_rot --all` → 21 loci, 19 of them `backlog-row-length`; `[#532]` closed, `[#364]` retired |
| `[#537]` | `b8bcae98` | `disposition token` is a Done-when branch nothing defines | nb6-backlog-truth §1.6 | the phrase occurs only in `#409`/`#410`/`#411` and `BACKLOG.md`; no definition, no validator |
| `[#538]` | `606e9b11` | The NB4-C PLAYBOOK gap arc — twelve paste-ready acts, none landed | nb4-playbook-gap | `Honest-RED`, `Land-then-delete`, `Position 0` each return **0 hits** in `protocols/PLAYBOOK.md` |
| `[#539]` | `3b592974` | `gen_lane_contract.py` — assembly-not-generation with a `--check` leg | nb4-equilibrium (M1) | `gen_lane_contract` has **0 occurrences** in `tasks/`, `protocols/`, `scripts/` |
| `[#540]` | `19e6a979` | `harvest_batch.py` — read the board, fetch packets by `git show` | night3-research Q2, re-recommended nb6 Q9 | `harvest_batch` has **0 occurrences** in-tree |
| `[#541]` | `903dbfbd` | Scale-out substrate decision — unowned after two reports | nb4-g-scaleout-substrate-v2 | the only substrate row in `tasks/` is `[#521]`, which is the `sys.path` substrate and unrelated |
| `[#542]` | `4836512f` | `ARCHITECTURE.md` still claims four `doc_rot` sub-detectors; there are five | batch-6 packet (Owed list) | detector declares `backlog-accretion`, `backlog-row-length`, `section-history`, `file-budget`, `grooming-cadence`; `doc_claims` checks 4 claims, not this one |

**Every birth was measured against the `[#532]` ARM-2 ceiling of 1320 characters before it was
written**, and three drafts were trimmed to fit (1377→1311, 1414→1302, 1342→1290). Filing `[#536]`
about the row-length pile while adding to it would be self-defeating — the same guard the batch-6
wrap commit applied to its own repair script.

**Ids 543, 544 and 545 of this lane's reserved block are unused.** A reserved block is a bound, not a
quota.

**One gate refusal, recorded rather than worked around.** `[#537]` and `[#542]` were first drafted at
size `XS`, which is not in the schema's `[P][S|M|L]` enum, and the `validate-backlog` pre-commit hook
refused `[#542]`'s commit:

```
FAIL  task missing [P][S|M|L] band — [#542] line 190
```

The refusal was correct and caught a defect in **two** rows before either reached the tree. Both were
re-sized to `S`, the refused staging state was reset to `606e9b11`, and the remaining births re-ran.
No `--no-verify`, no `SKIP=` — the refusal is the gate working, which is why it is in the ledger
instead of only in a shell history.

## §4 · Named follow-on — 49 earlier uncited audits, not ledgered here

Enumerated so the remainder is a list rather than a gap. All are dated 2026-08-06 or earlier and no
tracked artifact cites any of them.

- `docs/audits/2026-08-06-verification-lane-c-arch-327.md`
- `docs/audits/2026-08-06-technical-night-morning-packet.md`
- `docs/audits/2026-08-06-technical-lane-a-architecture-rows.md`
- `docs/audits/2026-08-05-conformance-nightly-digest.md`
- `docs/audits/2026-08-05-codex-480-review-artifact-organ.md`
- `docs/audits/2026-08-04-conformance-nightly-digest.md`
- `docs/audits/2026-08-04-codex-483-terra-round2.md`
- `docs/audits/2026-08-04-codex-465-terra-round2.md`
- `docs/audits/2026-08-04-codex-465-leg4-inert-check-detector.md`
- `docs/audits/2026-08-03-codex-arc3-terra-round2.md`
- `docs/audits/2026-08-03-codex-arc2-vacuous-green-trio.md`
- `docs/audits/2026-08-03-codex-arc2-terra-round2.md`
- `docs/audits/2026-08-03-codex-472-terra-round2.md`
- `docs/audits/2026-08-03-codex-472-declaration-anchor.md`
- `docs/audits/2026-08-01-technical-night-batch-plan-prep.md`
- `docs/audits/2026-07-31-technical-closure-ids-negation-defect.md`
- `docs/audits/2026-07-31-technical-433-spike-prep.md`
- `docs/audits/2026-07-31-codex-intake-split-generality-discharge.md`
- `docs/audits/2026-07-30-codex-446-v6-boot-prose.md`
- `docs/audits/2026-07-29-conformance-nightly-digest.md`
- `docs/audits/2026-07-28-technical-364-cap-option-matrix.md`
- `docs/audits/2026-07-27-codex-436-silent-rule-ratchet.md`
- `docs/audits/2026-07-27-codex-436-ratchet-recheck.md`
- `docs/audits/2026-07-27-codex-436-ratchet-gate9.md`
- `docs/audits/2026-07-27-codex-436-ratchet-gate8.md`
- `docs/audits/2026-07-27-codex-436-ratchet-gate7.md`
- `docs/audits/2026-07-27-codex-436-ratchet-gate6.md`
- `docs/audits/2026-07-27-codex-436-ratchet-gate5.md`
- `docs/audits/2026-07-27-codex-436-ratchet-gate10.md`
- `docs/audits/2026-07-27-codex-436-ratchet-clear.md`
- `docs/audits/2026-07-26-codex-routine-consumer-prose.md`
- `docs/audits/2026-07-25-codex-fix-live-backlog-test.md`
- `docs/audits/2026-07-20-codex-leg2-handoff-bundle-selection.md`
- `docs/audits/2026-07-20-codex-leg1-fleet-parity-gitdir-scrub.md`
- `docs/audits/2026-07-19-verification-night-e1-probe-fire-evidence.md`
- `docs/audits/2026-07-19-technical-night-s9-testing-harness-agentic.md`
- `docs/audits/2026-07-19-technical-night-s8-fleet-state-management.md`
- `docs/audits/2026-07-19-technical-night-s6-worktree-discipline.md`
- `docs/audits/2026-07-19-technical-night-s5-consumer-disk-info-audit.md`
- `docs/audits/2026-07-19-technical-night-s3-archives-lifecycle-records.md`
- `docs/audits/2026-07-19-technical-night-s2-backlog-decision-ops.md`
- `docs/audits/2026-07-19-technical-night-s1-intake-adr-lifecycle.md`
- `docs/audits/2026-07-19-technical-night-luna-carrier-inventory.md`
- `docs/audits/2026-07-18-codex-ruling-w-adr-amendment-v2.md`
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path-v5.md`
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path-v4.md`
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path-v3.md`
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path-v2.md`
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path.md`


## §5 · What this ledger deliberately does NOT do, and its honest limits

- **It edits no row it did not birth.** `[#417]`'s dead locator, the two `[#529]` prerequisites that
  the telemetry report says *should be stated on that row*, and the `disposition token` predicate on
  `#409`/`#410`/`#411` are all defects **in existing rows' text**, and `tasks/` files outside this
  lane's reserved block are not this lane's to write. Each is carried by a birth that names it
  instead.
- **It edits nothing in `docs/decisions/**` or `docs/intake/**`** — lane b's this batch. The
  nb6-archive-sweep intake transitions are therefore PENDING here rather than executed, which is a
  lane-boundary fact and not a judgement about them.
- **It ruled nothing, closed nothing, and executed no `/review-closures` proposal.** The closing
  campaign's two NOW-CLOSABLE candidates (`#417`, `#506`) are both still `open` and stay that way;
  ratification is an architect act. Worth naming: `#417` is proposed closable by one artifact and
  shown to carry a dead locator by another, and `[#534]` is where that conflict now lives.
- **Disposition is per ARTIFACT, not per finding.** A FILED artifact may contain findings the named
  row does not individually enumerate — `2026-08-14-qa-night2-quality` is the clearest case and is
  PENDING for exactly that reason. This ledger records which artifact is owned by what; it is not a
  finding-level register.
- **The citation sweep is substring-based.** "Uncited" means no tracked file outside the artifact
  itself contains its stem. An artifact referred to only by a paraphrase, a lane letter, or a partial
  name reads as uncited here. That biases the corpus toward *including* artifacts, which is the safe
  direction for this pass, but it means the 83 figure is an upper bound on genuine orphans.
- **`docs/audits/README.md` was regenerated** after `git add` of this file, because the generator
  reads tracked files only and the `audit-index-freshness` hook gates it. That regen and this file are
  this lane's entire write footprint outside `tasks/` and the two regen surfaces.

---

**audits 80 · ACTIONED 49 · FILED 25 (ids `[#534]` `[#535]` `[#536]` `[#537]` `[#538]` `[#539]` `[#540]` `[#541]` `[#542]`, plus existing owners `[#293]` `[#303]` `[#393]` `[#453]` `[#491]` `[#502]` `[#505]` `[#506]` `[#528]` `[#529]` `[#530]` `[#531]` `[#533]`) · REJECTED 2 · SUPERSEDED 2 · PENDING 2 (operator GO on the nb6 archive sweep; owner-or-accept on the qa-night2 LOW set) · follow-on 49**
