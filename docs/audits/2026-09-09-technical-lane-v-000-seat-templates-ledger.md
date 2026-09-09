# LANE v-000 seat-templates-ledger — end-of-lane artifact

<!-- Batch V, lane V-6. Frozen contract:
     `docs/audits/2026-09-08-technical-batch-v-launch-contracts/LANE-v-000-seat-templates-ledger.md`
     Branch `worktree-lane-v-000-seat-templates-ledger`, base `main` @ 33bcb0bd.
     Commit-and-STOP: nothing here was merged, pushed, or journaled. -->

## What this lane built

Five refusals as code, five seat templates that carry them as runnable lines, a renderer that
generates the five SEAT-BOOT pastes from PLAYBOOK Ch8 with probe P12 behind it, and a generator
for the operator's LEDGER read surface.

| Commit | What |
|---|---|
| `57632b9b` | `scripts/seat_ch8.py` — the Ch8 extraction map |
| `6c894137` | `scripts/seat_refusals.py` + five `templates/handoff/seats/*.md.tmpl` |
| `a767a0bc` | `scripts/gen_seat_boot.py`, probe P12, the `gen_handoff.py` cut-time hook |
| `f8218f0e` | `scripts/gen_ledger.py` + the witnessed run |

## Done-contract — every clause, with its evidence

**1 · Refusals 0/4 → 4/4, plus the fifth from AMEND-BATCH-V-002 §1 — 5/5.**

Each is a function that RAISES `SeatRefusal`, reachable as one command line, with a trip-test that
fails the moment it stops raising and a passing-path test so it cannot satisfy its own trip-test
by refusing everything.

- `sleeping-poll` — a wait stated as an intention with no `<!-- WAIT: … -->` declaration, or a
  declaration missing a positive interval, a positive bound or a predicate. Quoted Ch8 regions and
  fenced code are exempt: Ch8's own `**WAITS.**` paragraph contains the phrase, and it is the rule
  rather than an instance of breaking it.
- `lane-ceiling` — width > 6, a duplicate lane name, and being **called late**. Ch8 says the
  placement is the whole mechanism, so a call made with anything already provisioned is itself
  refused; `--check-worktrees` reads the live list rather than asking the dispatcher to
  self-report. The ceiling is `boot_frontier.BATCH_WIDTH_MAX` by identity, not a retyped `6`.
- `reviewer-mismatch` — exact model-id comparison. `gpt-5.6` where `gpt-5.6-terra` was contracted
  is a mismatch, not a near miss, and a substitution that does not report `review=NONE` is refused.
- `carried-by` — anchored **and** valued, both legs, because a bare substring match is a different
  and broken check. `write_decision_file` refuses *before* it writes: a check that writes and then
  complains has refused nothing.
- `dryrun-step0` — present, LAST, and covering every generated contract.

**2 · LEDGER absent → present, one witnessed run.**

```
uv run --locked python scripts/gen_ledger.py --date 2026-09-09
-> H:\My Drive\CLAUDE PROMPT DIR\to-browser\LEDGER-dev-knowledge.md (4139 B, refreshed 2026-09-09)
```

The prior hand-written v4 was archived first, byte-verified, per the convention that file's own
header records — sha1 `07dd6d74e9570fe10211e3475ed855071caab8c0`, identical at
`to-browser/archive/2026-09-09/LEDGER-dev-knowledge-v4-superseded-2026-09-09.md`.

**3 · SEAT-BOOT 0/5 → 5/5, plus probe P12.**

`gen_seat_boot.py write --bundle <dir>` renders all five; `gen_handoff.py` calls it at cut time.
P12 (`gen_seat_boot.py verify`) re-renders and byte-compares, and fails on each of the four ways a
drifted bundle looks correct: a hand-edited file, a hand-written file with no render header, an
**absent** file, and Ch8 moving underneath.

**4 · English, hyphen-only names, logging over print, Click CLIs, tests green.** Targeted suite
122 passed, 0 failed. Two Click CLIs (`seat_refusals`, `gen_seat_boot`) plus one Click command
(`gen_ledger`); `seat_ch8` stays argparse, matching its `boot_frontier` / `gen_north_star`
neighbours, because it is a read-only map inspector rather than an operator verb.

## Decisions taken under contract defaults — reported, not escalated (V-2)

**a · `templates/seats/` was refused; the seat templates live at `templates/handoff/seats/`.**
`validate_hermetization` Rule C refused the first location as a home the grammar has no convention
for, and it was right to. The fix is not a baseline touch: INBOX-dev-knowledge-2026-09-08-038 names
its own footprint as `templates/handoff/*`, and AMEND-BATCH-V-001 §1 calls seat boots "generated
bundle artifacts" rendered "at bundle-cut time" — so they belong beside `v5/`, `epic/` and
`functional/` under the already-admitted `templates/handoff/*` pattern. No spec edit was made and
none is owed.

**b · Ch8's INTERACTIVE dispatch row is rendered with ONE declared rewrite, not quoted verbatim.**
That row carries the literal `<PROMPTS_DIR>` placeholder and the sentence "expand the path by eye".
AMEND-BATCH-V-002 §3(b) forbids a placeholder in a rendered artifact and says in terms that "the
generator makes it structural", so `PLACEHOLDER_REWRITES` maps `<PROMPTS_DIR>` → `$d`, the variable
each boot's own §0 binds from User scope. **The rewritten block's label says it is rewritten
instead of claiming VERBATIM** — a label that overstates its own fidelity is the failure this whole
mechanism exists to end. Not escalated: §3(b) rules on this exact text and names this exact file.

**c · The silent-rule ratchet was DRAINED, not raised.** The templates first measured +3 against a
zero-headroom baseline. All three tokens were section headings describing the Ch8 block beneath
them rather than binding anyone; the rules themselves live in the extracted regions and are
untouched. Quoted before/after in `6c894137`'s commit body. Live is back at 447 == baseline.

**d · A Ch8 edit invalidates all five boots, not only the seat quoting the edited paragraph.**
Each render header carries a sha256 of the whole chapter. A per-block digest would re-issue only
the boots that happened to quote the edited text and leave the rest asserting a chapter state that
no longer exists.

**e · `SEAT_REFUSALS["dispatcher"]` is ordered so `lane-ceiling` opens step 0 and `dryrun-step0`
closes it.** Not cosmetic: the rendered step 0 is fed to the DryRun refusal against its own text,
so a reorder fails the suite rather than quietly moving the check off the boundary it guards.

## The question the step-0 coupling scan left open

**C3 — the `carried-by:` write-time refusal was assigned twice**, to V-5 (c) and to V-6 refusal #4.
The dispatcher resolved it to THIS lane and pinned V-5 out, filing a QUESTION rather than dropping
it. Built here as the WRITE-TIME leg only: `refuse_uncarried_decision_write` /
`write_decision_file` check that a carrier value is well-formed and refuse before the write.
**Whether a path value resolves on `main` is deliberately not asked here** — that is `[#643]`'s
read-time `preflight_rows` leg, and at write time the carrier has often not landed yet. The two are
different organs and neither subsumes the other; nothing needs merging between them.

## Three defects this lane's own tests caught

1. **The rendered dispatcher step 0 carried the CHECKER but not the `-DryRun` line.** Step 0
   verified a DryRun that was not there. Caught by running the refusal against the artifact rather
   than trusting the template.
2. **The LEDGER read the first `##` for its JOURNAL head**, but entries are depth 3 under a depth-1
   title — so it rendered `UNAVAILABLE` against a perfectly readable file. A wrong answer wearing a
   missing file's clothes.
3. **`worktrees: 6` listed five names.** "How many trees exist" and "how many lanes are live"
   differ by one, always; now rendered as `primary + N`.

## Honest limits

- **`refuse_sleeping_poll` reads TEXT.** It catches a wait written as an English intention and a
  declaration missing one of its three parts. It cannot tell whether a well-formed predicate is
  true of the file surface, or whether the loop carrying it was ever run.
- **`refuse_lane_ceiling` is called by a seat; nothing calls it for one.** It is wired into the
  dispatcher template and asserted there by test — a **wiring proof, not an enforcement proof**.
  No gate counts a plan's lane list, which is what Ch8's own "honest limits" already says.
- **P12 proves a rendered file equals a fresh render of the CURRENT Ch8.** It does not prove Ch8 is
  right, and it does not prove the render reached anyone. A bundle carrying five perfect SEAT-BOOT
  files that no seat opens is a green probe over an unread artifact; INBOX 038's own Done-when —
  "the incoming seat's first dispatch uses one verbatim" — is not a property any test here holds.
- **`gen_ledger` runs no gate and no suite**, so it carries no ship-gate verdict, test count or
  WARN census. Its BLOCKED BY section sees `depends-on` blockage among open rows and nothing else,
  which is not most of what actually blocks this repo — the rendered artifact says so itself.
- **P12 is not wired into any gate.** It is a CLI and a test; `verify_handoff_probes` was not
  extended, because that file is a shared surface this lane's footprint does not own.

## Suite state

Baseline for batch V is **28 RED @ `08c35b9c`** — compared against, never against zero.

- **Targeted (this lane's diff): 122 passed, 0 failed.** `test_seat_ch8.py` (14),
  `test_seat_refusals.py` (57), `test_gen_seat_boot.py` (25), `test_gen_ledger.py` (26) — 103
  before the review, plus 19 regression tests for the seven findings.
- **Regression on the modules this lane touched:** `test_gen_handoff.py`,
  `test_gen_handoff_preflight.py`, `test_handoff_modes.py`, `test_verify_handoff_probes.py`,
  `test_boot_frontier.py`, `test_batch_manifest.py` — **5 failed, 324 passed** (160 s). Measured a
  second time **with the `gen_handoff.py` hook reverted**: the same 5 fail, 214 passed over the
  smaller set. Inherited, not introduced. They are `test_epic_bundle_has_no_failing_probe` (6≠5),
  `test_dogfood_generated_bundle_has_no_failing_probe` and
  `test_dogfood_no_probe_row_carries_an_answer_value` (both 15≠13 — the probe roster grew past
  what the constants assert), `test_boot_carries_both_postures`, and
  `test_suffixed_bundle_probes_resolve_against_their_own_directory`.
- A sixth, `test_verify_handoff_probes.py::test_every_batched_selector_git_call_still_receives_the_scrubbed_env`,
  **passes under xdist and fails when run alone** — order-dependent, and it fails alone at the
  reverted baseline too. Recorded rather than attributed: it is not this lane's, and calling it
  green because the parallel run said so would be reporting the scheduler rather than the test.

The full suite is **not** run in-lane by design (`[#528]`; PLAYBOOK Ch5 tiered suite) — it runs
once, at integration, on the merged tree.

## Gate bypasses declared

Every commit in this lane declares `SKIP=doc-counts-pytest-freshness` in its body, and nothing
else. The added tests move the `pytest_collected` claim in `ecosystem/doc-counts.md`; per the
frozen contract the integrator is gate-of-record and regenerates once at the merge, and six lanes
each regenerating the same one-line count would produce six guaranteed conflicts. **No
`--no-verify` was used anywhere in this lane.** This artifact's own commit additionally declares
`SKIP=audit-index-freshness` for the same reason: `docs/audits/README.md` is generated and
regenerating it here is the index regeneration the contract reserves to the integrator.

## Terra pre-merge review — 7 HIGH, 7 fixed

Run per the batch gate ("terra pre-merge on V-2/V-3/V-5/V-6/V-7"), model pinned by the wrapper,
against `main..worktree-lane-v-000-seat-templates-ledger` at `f8218f0e` (codex-cli 0.145.0, code
profile). **The review artifact is deliberately NOT in `docs/audits/`**: the wrapper writes there
by default, and for a batch lane that collides with two standing rules at once — the lane is
forbidden to regenerate the generated audits index, and a freshly-landed uncited audit raises the
very `consumer_at_landing` count the batch is measured on. The findings and their resolutions are
carried here instead, which is where D1 reads them.

Every finding was real. Each is fixed with its own regression test — 19 tests added on top of the
103 the lane already had.

**`scripts/seat_refusals.py`**

1. **One unrelated WAIT declaration vouched for every prose intention.** The check was
   per-document (`if intents and not decls`), so a valid wait anywhere in a file satisfied an
   unbounded one elsewhere and the refusal reported PASS. Now per-intention: each stated wait
   needs a declaration within 10 lines of it.
2. **The DryRun checker read the whole file, not step 0.** The rendered boot passes
   `--step0 <this file>`, whose later sections made a correct step 0 fail — and, worse, a DryRun
   in a later section would have MASKED a step 0 carrying none. `isolate_step0()` now slices the
   step-0 section first, which is what makes "the LAST line of step 0" mean step 0's last line.
3. **`value.startswith("OPEN")` admitted `OPENING` and `OPEN-not-a-carrier`.** Now `^OPEN(?:\s|$)`
   — the literal token, alone or followed by a reason, which is what the probe accepts.

**`scripts/gen_seat_boot.py`**

4. **A refused render left a PARTIAL set on disk.** Boots were written as they rendered, so a
   late refusal left earlier files behind while the cut-time hook reported "no boots written"
   about a directory that had three. Now: render all five, then write all five.

**`scripts/gen_ledger.py`** — three instances of one class, and it is the class that matters most
in a read surface: **a failed probe rendered as a fact.**

5. **An unreadable queue rendered `open rows: 0`** — inviting the reader to conclude there is no
   pending work. Now `UNAVAILABLE` with the reason.
6. **A failed batch read rendered `no integration-arc exemption is live`** — a claim about
   ADR-110 that the ledger had no basis for, and exactly what an operator opens this file to
   learn. The reader now returns `(batches, error)` and the error reaches the render.
7. **`_UNKNOWN` slid into concrete state** — a failed `git status` became `DIRTY - 1 path(s)`, a
   failed `worktree list` became `primary only`, a failed `git branch` became `0`. Three small
   renderers now keep the sentinel visible per field.

The LEDGER witnessed run was **re-run after the fixes** so the file on the transport is the output
of the shipped code, not of the reviewed-and-since-changed code: same path, 4139 B, refreshed
2026-09-09.

## Tally

```
Tally: review=lane-v-000-seat-templates-ledger reviewer=gpt-5.6-terra findings=7 fixed=7
Severity: Critical 0 / High 7 / Medium 0 / Low 0
```

The reviewer that ran is the reviewer the batch gate named, so this is a tally and not a
`review=NONE`. Checked with this lane's own organ — the first consumer of refusal #3 is this
artifact, run both ways:

```
$ seat_refusals.py reviewer --contracted gpt-5.6-terra <this file>
reviewer: PASS -- review=lane-v-000-seat-templates-ledger reviewer=gpt-5.6-terra      (exit 0)

$ seat_refusals.py reviewer --contracted gpt-5.6-sol <this file>
REFUSED [reviewer-mismatch]: the contract named gpt-5.6-sol and gpt-5.6-terra ran ...  (exit 1)
```

The second line is the one worth having: the refusal fires on a substitution rather than
reporting a finding count nobody can attribute.

## For the integrator

- Branch `worktree-lane-v-000-seat-templates-ledger`, five commits, merged nowhere.
- `git merge origin/main` was run before handback per the C2 coupling scan (V-5 shares
  `scripts/gen_handoff.py` in disjoint functions).
- On merge, regenerate `ecosystem/doc-counts.md` and `docs/audits/README.md` once, for the batch.
- Nothing in `preflight_rows`, `assert_preflight` or any `_row_*` function was touched — V-5's.
- No JOURNAL entry was written: that is the integrator's surface (`STANDING_RULINGS.md` P-1).
