---
last_reviewed: 2026-09-07
status: active
owner: Rob
---

# Token bottlenecks — census S-14 (SWEEP 2026-09-07, cloud, read-only)

> **Consumer:** `[#528]` (lane-latency — the full suite multiplied per lane and per merge) and
> **intake #50** (cost-and-delivery telemetry). Section 5 is written as the pickup for `[#528]`
> leg 3 and for intake #50's collection gap; section 2's ranking is the evidence `[#528]` says it
> lacks. Secondary: `ADR-110` (the batch protocol whose per-lane contract shape is sink S-1) and
> `STANDING_RULINGS` AE-2 (a row that cannot be computed prints its reason rather than acquiring a
> store to become computable — the rule this whole census obeys).
>
> **Read-only census.** Nothing was moved, edited, deleted or renamed. This is not a build:
> the ranking and the mechanisms are proposals; the operator rules.

## 0 · The premise, stated before the numbers

**No per-lane token figure exists in this repo, and this census does not invent one.**
`scripts/cost_usage_telemetry.py` (23,284 B) declares itself in its own second line as
*"Library only; no call sites"*, and a grep across `scripts/`, `tests/`, `.claude/` and
`.pre-commit-config.yaml` finds it referenced by exactly one test
(`tests/test_cost_usage_telemetry.py`, which loads it by path) and by audit prose. **Zero
production call sites — verified here, not restated from A-05.**

So every number below is one of three things, and each is labelled:

```
MEASURED     a byte count, file count or line count taken in this session, on this checkout
WITNESSED    a figure a committed in-tree artifact states, cited to its file
NOT RECORDED nothing in-tree carries it -- named as absent, never estimated
```

**Bytes are not tokens.** Every "MEASURED" figure here is bytes of text. The bytes→tokens
conversion depends on the tokenizer and on how much of a file a session actually reads, and this
repo instruments neither. A byte figure is a *lower-bound proxy for delivery cost*, and it is
offered as exactly that. Where the honest answer is "unmeasurable", section 6 says so.

## 1 · Per lane / seat — what is actually recorded

Batch T (2026-09-06 NIGHT, 15 rows) and Batch U (NIGHT-2) are the two batches with in-tree
manifests and contract sets. Batch T also has a close packet; **Batch U has none yet** — its
close packet path does not exist, which is what keeps the batch open under
`batch_manifest.open_batches`.

```
AXIS                          BATCH T                        BATCH U
bytes of brief handed         MEASURED, per lane (S-1)       MEASURED, per lane (S-1)
wall time                     1 of 15 lanes (3.8: 36 min)    NOT RECORDED -- no close packet
turns                         2 of 15 (3.9: 45; 3.8: 114)    NOT RECORDED
tool calls                    NOT RECORDED -- no seat any    NOT RECORDED
                              records tool-call counts
bytes of STATUS read          NOT MEASURABLE IN-TREE --      same
                              STATUS-*/RATIFICATION-* live
                              on the Drive transport
reviewer rounds               RECORDED AS ZERO for every     NOT RECORDED; U's contracts
                              merged lane ("every one        require a review= tally and
                              logged NO REVIEW")             the integrator refuses
                                                             review=NONE on a code branch
full-suite runs               1 of 15 lanes (3.8, twice --   NOT RECORDED
                              a git-stash A/B)
dispatcher polling wake-ups   NOT RECORDED anywhere          NOT RECORDED
re-derivations of one fact    RECORDED, but as prose, not    NOT RECORDED
                              per lane (see S-6)
substrate                     local 8 / cloud 3 / codespace  declared per contract
                              2 / wave-2 1 / never-launched 1
```

**Seven of the nine axes the contract asks about are not recorded for either batch.** That is
the census's first finding and it is why section 5 exists.

## 2 · The ten largest sinks, ranked

Ranked by the size of the measured or witnessed quantity, with delivery-cost sinks (bytes handed
to a seat) and wall-clock sinks interleaved — they are the same budget from the operator's side.

---

### S-1 · Lane-contract boilerplate, replicated once per lane — **MEASURED**

The largest thing this census can measure exactly.

```
BATCH  CONTRACTS  CORPUS BYTES  BYTES BYTE-IDENTICAL IN *ALL* CONTRACTS   SHARE
T      13         211,550       121,602                                   57.5%
U      19         351,568       234,289                                   66.6%
                  -----------   ----------------------------------------
       32         563,118       355,891
```

Method: every line longer than 40 characters was hashed across the contract set; a line present
in all N files of its batch counted once per file it appears in. Batch U's threshold curve is
flat — the shared block is the same whether you ask for lines in 9/19, 15/19 or 19/19 files, so
this is a genuine common preamble, not an artefact of the threshold.

**Delivered-more-than-once:** `234,289 x 18/19 = 221,958 B` in U and `121,602 x 12/13 = 112,248 B`
in T — **334,206 B of byte-identical text handed out a second-through-Nth time across two
batches.** Genuinely lane-specific content in U averages `(351,568 - 234,289) / 19 = 6,173 B` per
lane against an 18,503 B mean contract.

Inspection of `LANE-u-000-dispatch-receipt-is-work.md` shows what the shared block is: Dispatch,
Worktree pairing, Done-contract clauses C-6/C-7, the footprint rules, and the gate warnings — the
same text every lane must obey and none of them may vary.

> **Mechanism: brief-by-reference.** The shared preamble becomes one versioned file; each contract
> carries a pointer plus a pin (path + SHA), and only its own `Intent`/`Closure`/`before → after`
> inline. On U's numbers that is 351,568 B → roughly 19 x 6,173 + 19 x pointer + one 234,289 B
> shared file, i.e. **~1.6x fewer bytes delivered per batch**.
> **Cost:** a pointer can fail to resolve, and this repo has already paid for that once — batch T
> lane 3.8 attempt 1 refused on locators it said did not resolve, one of which was verified to
> exist on `origin/main`, and returned a clean receipt over zero work. Brief-by-reference makes
> that failure mode *the normal path* rather than an edge case. It is only safe alongside a
> resolve-before-you-act step (`/preflight` exists) and a pinned SHA, and it trades a frozen page
> for a page whose version must be verified.

---

### S-2 · The full suite, multiplied by lanes and by merges — **WITNESSED**

`tasks/528-lane-latency-full-suite-multiplied-across-a-batch.md`, witnessed 2026-08-14:

```
full suite                    1001 s
paid                          ~once per lane + once per merge
4-leg batch wall-clock        ~50 min
```

And its 2026-09-05 amendment, which retires the original hypothesis:

```
tree-globbing tests, corpus   2,420 files (0 worktrees) -> 14,510 files (5 worktrees)
                              12,090 of them duplicates under .claude/worktrees/*
normalize_text over corpus    78.57 s pre-fix -> 12.96 s post-fix   (~65 s lever)
```

The mechanism was **misdiagnosed in writing before it was measured**: the architect's guess named
pytest collection, and `docs/audits/2026-09-05-verification-lane-h0-suite-speed.md` shows
collection never paid for worktrees at all (`4917 tests collected`, ~1.4–1.9 s at 0, 2 and 5
worktrees) because pytest's default `norecursedirs` already prunes `.claude`. The real cost was
two tests calling `Path.rglob` themselves, which consults neither `.gitignore` nor
`norecursedirs`. **This grows with lane count** — which is precisely the batch axis.

> **Mechanism: suite once at integration.** `[#528]` leg 2 is already written into `CLAUDE.md`
> §4 and `AGENTS.md` ("In a lane, run the targeted tests… the full suite runs once, at
> integration"). Leg 1 — `-n auto --dist worksteal` at the *gate-run* call sites, not just the
> tuned `verify` path — is still open. Leg 3 (emit `test_run` duration) is section 5's work.
> **Cost:** a lane that never runs the full suite can hand back a diff that only fails in
> combination with another lane's, and the integrator absorbs that serially at the merge queue,
> where it is most expensive to unpick. The rule trades N cheap detections for one late one.

---

### S-3 · The browser chat re-processing its own history — **WITNESSED, and the only figure in this census expressed as a share of a usage window**

`protocols/OPERATOR-INTERFACE.md:151`, measured 2026-09-06:

> an outgoing browser chat spent roughly **30% of a usage window in 20 minutes of short answers**

with the cause stated precisely: not the Drive transport, but *"a five-day chat whose every turn
re-processes its whole history, by then 30+ pasted session outputs of 10-20 KB and about 30
uploaded files, on the most expensive model."*

**This is the single largest identified sink in the whole census** and it is the one that costs
the operator directly rather than a lane. The asymmetry it names is the census's sharpest
sentence: *a Drive read is cheap and one-shot; a pasted transcript is permanent and is re-billed
on every later turn.*

> **Mechanism: browser rules 030/032**, already written in that same table — one window per
> sitting (a single milestone or ~40 turns, then wrap); CC output **read** from the transport
> (`STATUS-*`, `LEDGER-<repo>`, `QUESTION-*`, close packets) rather than pasted, with a pasted
> session log counted as a browser-seat defect; `STATUS-*` at or under 5,000 B with a "now"
> section on top; one chat per window with the model switched per act.
> **Cost:** wrapping a window discards continuity the operator was relying on, and the bundle has
> to carry it instead — which is what makes S-4 and S-8 load-bearing rather than cosmetic. Note
> the table's own finding that a second parallel chat buys nothing, because the cost is context
> **length**, not chat count.

---

### S-4 · `PASTE_THIS.md` over its own ceiling, and the ceiling does not block — **MEASURED**

```
FILE                                                        BYTES   CEILING  OVER
docs/handoffs/2026-09-01-.../PASTE_THIS.md                 32,264   20,000   +61%
docs/handoffs/2026-09-06-.../PASTE_THIS.md                 27,829   20,000   +39%
docs/handoffs/2026-09-06-.../HANDOFF_BOOT.md               12,395   18,000    ok
docs/handoffs/2026-09-01-.../HANDOFF_BOOT.md               11,252   18,000    ok
CLAUDE.md                                                  23,551   24,576    ok (96%)
```

`PASTE_BYTE_CEILING = 20_000` at `scripts/assemble_paste.py:46`; the check at `:363` emits
`[warn]` and assembly still succeeds — `tests/test_assemble_paste.py:471` asserts that posture
explicitly ("a paste past `PASTE_BYTE_CEILING` trips a `[warn]` — but assembly still succeeds").
**Both live bundles are over, and the boot budget is the half that holds.** This matters because
`PASTE_THIS.md` is the one artefact designed to be pasted in full, and S-3 is about paste cost.

> **Mechanism:** make the ceiling block, or split the paste into a boot half and an on-demand
> half. **Cost:** a blocking ceiling can strand a window at generation time, at the worst moment —
> the operator is mid-handoff. The softer version (split) preserves generation and moves the
> decision to the reader, at the price of a second fetch.

---

### S-5 · Work performed and never committed — **WITNESSED**

From `docs/audits/2026-09-06-technical-batch-t-close-packet.md` §1 and §2.5:

```
lane 3.9 trace-scorecard    45 turns of real work, cut off mid-sentence waiting on a
                            background test, NEVER COMMITTED, no branch anywhere.
                            Total loss. The only copy is inside a stopped codespace
                            on a 24h retention clock.
lane 3.8 attempt 1          Ok:True / RemoteExitCode:0 / is_error:false / status:DONE
                            over ZERO WORK. Re-dispatch cost a second full lane, which
                            then landed at 114 turns / 36 minutes.
```

**This is the largest witnessed waste per unit of work in either batch** — 45 turns yielding
nothing, plus one wholly duplicated lane. The close packet's own generalisation is that *a
codespace receipt proves TRANSPORT, not WORK*, and it reached that by noticing four instrument
failures of one shape in a single night.

> **Mechanism:** the fix was written and never dispatched — **COMMIT BEFORE YOU RUN THE SUITE**,
> inverting the lane's order so a cut-off costs the tail rather than everything. Alongside it, a
> receipt predicate that distinguishes "did the work" from "connected successfully"; W1-2's
> contract (`LANE-u-000-dispatch-receipt-is-work.md`) is exactly that lane, requiring a
> `git ls-remote` witness before DONE.
> **Cost:** more commits of intermediate, possibly non-green state on a lane branch, which makes
> the branch history noisier and pushes tidy-up to the integrator. Cheap against 45 lost turns.

---

### S-6 · Re-deriving the same fact — **WITNESSED, and the cheapest thing on this list to fix**

The close packet §9 tallies the ADR-85 anchor predicate misreading across one night:

```
dispatcher      3 times
integrator      1
lane 3.6        1  (and it spent a --no-verify bypass on it, then withdrew it)
lane 3.1        1  (diagnosed unaided)
2 further lanes    minutes from spending a bypass before being talked down
```

Seven seat-instances of one predicate, in one batch. The packet's verdict: *"a predicate misread
that many times in one night is a documentation defect, not seven lapses"* — and, by both the
integrator's assessment and the dispatcher's, **the highest-payoff one-paragraph fix on the dawn
list**. The asymmetry is one sentence: `check_journal_spine_anchor` reads the SPINE from `main`
and the JOURNAL TEXT from the WORKING TREE, so a lagging tree reports gaps that do not exist; the
remedy is `git merge origin/main`, never a bypass.

A second instance of the same class: **`intake-id` was double-allocated four times** (14, 42, 70,
72), because next-free was computed from a folder listing, which cannot see ids allocated on
unmerged branches. Lane 3.7's fix — scan every `docs/intake/` blob reachable from **any** ref (269
blobs, 72 ids, max 72, no gaps) — is the allocator this repo should have.

> **Mechanism:** write the asymmetry down once, at the point of use, and make the scan-every-ref
> derivation the allocator. **Cost:** effectively zero — one paragraph and one function. This is
> the highest ratio on the list and it should be ranked first for *action* even though it is
> sixth by magnitude.

---

### S-7 · `JOURNAL.md` as a grep target — **MEASURED**

```
JOURNAL.md    3,529,468 B    32,913 lines    the largest tracked file in the repo
```

The boot contract asks for the last 5 entries, which is cheap. The expensive path is that the
ADR-85 anchor predicate is checked *by grepping this file* — and S-6 records seven seats doing
exactly that, several of them repeatedly and wrongly, because grepping for a merge's own hash
returns nothing by construction.

> **Mechanism:** an anchor sidecar or index the predicate reads instead of the prose. **Cost:** a
> derived index over an append-only file drifts, so it needs its own freshness gate — this repo
> already carries several, and each one is a check somebody pays for at every commit. A cheaper
> variant is to leave the file alone and fix only the documented predicate (S-6), which costs
> nothing and removes most of the traffic.

---

### S-8 · The handoff corpus, and 16 frozen PLAYBOOK snapshots inside it — **MEASURED**

```
AREA                       BYTES        FILES
docs/audits               17,593,435     1,031
docs/handoffs             10,976,132       762
tests                      4,339,597       223
(root files)               4,261,638        20
scripts                    3,043,911       135
protocols                  1,165,796        16
TOTAL TRACKED             46,953,934     2,998

frozen PLAYBOOK copies inside handoff bundles:  16 files, 1,820,788 B
protocols/PLAYBOOK.md itself:                            490,615 B
```

**16 bundle-local snapshots of PLAYBOOK cost 1.82 MB, 3.7x the live file.** Individual copies run
106,813–141,973 B. Bundle thinning is already a lane
(`docs/audits/2026-09-02-technical-lane-g-611-bundle-thinning.md`).

> **Mechanism:** a bundle carries a pointer plus a SHA to the PLAYBOOK revision it was cut
> against, not a copy. **Cost:** the bundle stops being self-contained — which is the property it
> was given a copy for. The pin has to resolve at read time, and an old bundle whose SHA has been
> garbage-collected becomes unreadable rather than merely stale. This is the same trade as S-1,
> and it should be ruled once for both.

---

### S-9 · Reviewer rounds — a cost that measured **zero**, which is its own finding — **WITNESSED**

The close packet, on batch T's integration:

> Every lane merge ran 9-28s against a 5-minute docs bar, and **every one logged NO REVIEW** — no
> lane reported a terra tally, and per C-7 an empty invocation is NO REVIEW, never clean. […]
> seven lanes merged without a review artifact, and the packet should not be read as though they
> carried one.

**The "one reviewer round" mechanism cannot cut a cost that measured zero in batch T.** It becomes
a real lever only in U, where each contract's done-clause 3 requires a
`review=codex HIGH:n MED:n LOW:n` tally and the integrator refuses `review=NONE` on a code branch.
Listing this as a sink without that qualification would be exactly the plausible-number error this
contract forbids.

> **Mechanism: one reviewer round, docs-only exempt.** **Cost:** assurance, and batch T shows the
> bill is already being paid implicitly — seven lanes merged with no review artifact at all. The
> honest framing is that U is *adding* this cost deliberately, and capping it at one round is how
> the addition stays bounded, not how an existing cost gets cut.

---

### S-10 · Offload of read-only lanes — **unavailable, and uncounted by construction**

Three separate blocks, each verified here:

```
gemini on PATH (this container)   ABSENT -- `command -v gemini` returns nothing
                                  fan-out: NONE
Copilot Enterprise offload        UNAVAILABLE until intake #75 is ratified
                                  (docs/intake/README.md:51 -- "The `offload` role, and a
                                  witnessed account / token-scope map")
tokens_saved_by_offload           HARD-CODED PLACEHOLDER = 0
                                  scripts/window_metrics.py:434-438, verbatim: "PLACEHOLDER
                                  = 0 -- printed as a line by instruction and NOT computed.
                                  The offload instrumentation (lane D15) has not landed, so
                                  no surface exists to read"
```

**`fan-out: NONE`, and that absence is not clean.** This census ran single-seat because it had to,
not because fan-out was judged unnecessary; a fanned-out version would have read the U contract
set and the T close packet in parallel. `uv` in this container is **0.8.17** against the pinned
`==0.11.19`, so no gate and no scorecard could be executed here either (see section 6).

> **Mechanism: offload of read-only lanes** to a cheaper substrate. A census lane like this one is
> the ideal candidate — it writes one file and reads many.
> **Cost:** unmeasurable today, in both directions. The *saving* has no surface (the placeholder
> above), and the *risk* — a cheaper model producing a plausible census — is exactly the failure
> mode section 0 exists to guard against. Ratifying #75 buys the capability; measuring whether it
> pays needs section 5's work first. **Do not offload on an argument; offload on the number.**

---

### Ranking, condensed

```
RANK  SINK                                  QUANTITY                        KIND
S-1   contract boilerplate per lane         334,206 B re-delivered / 2 batches   MEASURED
S-2   full suite x (lanes + merges)         1001 s x N; ~50 min per 4-leg batch  WITNESSED
S-3   browser chat re-processing history    ~30% of a usage window / 20 min      WITNESSED
S-4   PASTE_THIS over ceiling, WARN-only    32,264 B and 27,829 B vs 20,000      MEASURED
S-5   work performed, never committed       45 turns lost + 1 duplicated lane    WITNESSED
S-6   re-deriving one fact                  7 seat-instances; 4 id collisions    WITNESSED
S-7   JOURNAL.md as a grep target           3,529,468 B / 32,913 lines           MEASURED
S-8   handoff corpus + PLAYBOOK snapshots   10.98 MB; 1.82 MB in 16 copies       MEASURED
S-9   reviewer rounds                       ZERO in T; becomes real in U         WITNESSED
S-10  offload of read-only lanes            NOT COMPUTED by construction         --
```

**By fix-cost-to-payoff rather than by magnitude, S-6 ranks first** — one paragraph and one
function against seven seat-instances and a spent bypass.

## 3 · The instrumentation gap — what must be wired before "tokens per lane" is a number

This section is the pickup for the next batch's first code lane. It is ordered so each item
unblocks the next, and each names the exact surface.

**The controlling rule, so nobody widens this into a platform:** STANDING_RULINGS **AE-2** — a row
that cannot be computed from an existing surface prints its reason and *"does not acquire a store
in order to become computable."* Three of the four items below are wiring, not new stores. Item
G-2 is the one genuine new collection, and it is the one intake #50 already owns.

---

### G-1 · Wire `cost_usage_telemetry.py`'s call sites — **the A-05 gap, precisely stated**

**State, verified this session:** the module exists at 23,284 B, exposes
`emit_genai_span(system, request_model, response_model, input_tokens, output_tokens,
cache_read_tokens, duration_ms, cost_estimated_usd, lane_id, batch_id, substrate, …)`, ships an
`AtRestExporter` writing OTel-GenAI-shaped rows into local SQLite, and has **zero callers**.

**The precedent that says how this goes wrong:** `[#529]`'s leg 1 was declared STALE on
2026-09-01 by a lane that had counted **imports** rather than call sites, and the amendment was
withdrawn the same day after direct re-measurement found `emit_check_run` had exactly one caller
(`scripts/governance_health.py:636`) and `emit_event` / `emit_hook_run` / `emit_blocker_fired`
had zero — while three of the six importing modules import `default_db_path` *specifically in
order not to use it*. **The done-when predicate is WIRED CALL SITES, and it must be measured as
callers, never as importers.**

**Work:** identify the seam where a lane's model calls are observable at all — which today is
nowhere in-repo, because lane sessions run outside this process. That is the honest blocker:
`emit_genai_span` has no in-repo caller *because there is no in-repo moment when a model call
happens*. So G-1's real content is **choosing the seam**: either (a) the dispatch wrapper records
per-lane usage from the session's own export where one exists, or (b) the lane writes its own span
at handback from figures it can see. Option (b) is available today; option (a) is blocked by the
gap in G-4.
**Done when:** at least one live lane produces a span in the at-rest store, and the span's
`lane_id` matches a branch that exists on origin.

---

### G-2 · There is no store — `logs/TELEMETRY.db` is gitignored and does not exist

**Witness:** intake #50's 2026-08-29 amendment, which is the first honest enumeration this
question has had:

```
backlog velocity (net banked - births)   IMPROVING  +16 rows/week   4 samples, LIVE
commit-gate wall-time                    ABSENT     logs/TELEMETRY.db is gitignored and
                                                    does not exist -- there is no store at all
suite wall-time                          ABSENT     no store
per-model change quality                 ABSENT     nothing records the authoring model
```

Confirmed here: `.gitignore:119` carries `logs/TELEMETRY.db*` and `.gitignore:178` carries
`logs/prompts/`. **Both of the two surfaces that would answer "what did this lane cost" are
deliberately untracked.** That is a defensible design (a WAL store and per-dispatch traces are
local artefacts, not durable records) and it is *also* precisely why no number exists.

**Work:** decide, as a ruling and not as a lane's improvisation, what the durable record is.
Three shapes, cheapest first — (i) the lane's HANDBACK line carries its own figures, so the record
is the commit message and needs no store; (ii) a per-batch committed receipt artefact under
`docs/audits/`, which is where every other batch fact already lives; (iii) the SQLite store plus a
read path (`[#576]`), which is the largest option and is already sequenced behind a
store-performance row.
**Done when:** one shape is ruled and the close packet of the next batch carries per-lane cost in
it. **Recommendation: (ii)** — it reuses the artefact class the batch protocol already produces,
needs no gitignore exception, and is diffable.

---

### G-3 · The scorecard's placeholder, and the six rows beside it that already print their reason

`scripts/window_metrics.py` is the closest thing this repo has to the deliverable, and it is
**honest by construction**: `value is None` means not computed, never zero. Its `--scorecard` mode
carries ten rows plus three addenda. The ones relevant here, verbatim from source:

```
tokens_by_model_class        NOT COMPUTED -- logs/TOKEN-LOG.md is a hand-curated weekly
                             narrative, not a structured artifact; parsing it would be new
                             instrumentation, the named anti-pattern
tokens_saved_by_offload      PLACEHOLDER = 0 -- the offload instrumentation (lane D15) has
                             not landed, so no surface exists to read
turns_per_window             NOT COMPUTED -- browser turns happen off-repo and leave no
                             committed artifact. 031 states a turn BUDGET (<= 40), which is a
                             ceiling, not a measurement, and printing it would launder one
                             into the other
connector_bytes_per_window   NOT COMPUTED -- the connector reads the transport dir, which is
                             outside the repo and uncommitted
failing_nodeids_baseline     THE BASELINE-SECONDS HALF IS NOT COMPUTED: no committed artifact
                             records suite wall-clock
pct_lanes_codespace          [computable] from the DECLARED `**Shape:**` of each frozen
                             contract -- "not a post-hoc observation of where it ran -- the
                             run record lives in gitignored logs/prompts/ traces"
```

**This is the gap list already written, by the repo, in the right place.** Section 5's job is not
to restate it but to point at it: **W1-6 left `tokens_saved_by_offload` as a placeholder line, and
`logs/TOKEN-LOG.md`'s weekly narrative is the only token surface that exists.**

`logs/TOKEN-LOG.md` (6,709 B, 130 lines) holds weekly `ccusage --json` deltas — per-window, per-model,
fleet-wide. Most recent entry, 2026-08-04: 10 active days, $1,676.83, 8.36M tokens in+out, Opus 5 at
72.1%. **It is a fleet weekly total. It cannot be divided by lane, and it should not be.** Every
entry also records `sessions N/A (not in ccusage --json)`, so even sessions — the coarsest possible
denominator — are absent.

**Work:** make `tokens_by_model_class` computable by giving `ccusage` output a structured landing
place beside the narrative (the narrative stays; it is append-only and is the readable record).
Then `tokens_saved_by_offload` acquires a basis the moment an offload substrate exists.
**Done when:** `--scorecard` prints a number for `tokens_by_model_class` with a basis citing a
committed structured artefact, and `logs/TOKEN-LOG.md` is unchanged in form.

---

### G-4 · Per-lane cost from receipts into the scorecard — the row this census was commissioned against

**Anchor:** intake #50's second scenario, verbatim — *"As the architect pricing D1, I read measured
cost-per-lane on each substrate instead of arguing from wall-times taken on a contended
workstation."* That is the requirement, filed 2026-08-26 and still unmet.

**And the trap it must avoid, witnessed by batch T §4.6:** intake #71's 664 s → 75 s baseline was
taken on a slow Windows process-spawn substrate; on the Linux devcontainer the same gate was
already ~28 s **before lane 3.8 changed anything**. *"A lane that measured wall-clock would have
reported a large success, honestly, and been wrong."* Lane 3.8 measured **git spawns and file
reads** instead — `1310 → 645` spawns, `13854 → 4170` reads — and got a result that survives the
substrate.

**So the per-lane cost row must be a COUNT, not a DURATION**, or it will price D1 wrong in exactly
the direction the operator is trying to avoid. Wall-clock may ride alongside, labelled by
substrate, never as the comparison key.

**Work:** (1) rule G-2's shape; (2) define the per-lane receipt fields — at minimum
`lane_id, batch_id, substrate, turns, tool_calls, brief_bytes, full_suite_runs, review_rounds,
commits_pushed`, all counts; (3) have the close-packet generator read them into the per-lane table
that batch T's §1 already has a column shape for; (4) feed the same rows to `collect_scorecard` so
`time_to_merge_per_lane` gains a sibling.
**Done when:** a batch close packet prints per-lane cost as counts, and `--scorecard` reads the
same committed rows rather than re-deriving them. **`brief_bytes` is free today** — it is
`os.path.getsize` of the lane's own contract file, and section 2's S-1 table is that column already
computed for 32 lanes.

## 4 · What the mechanisms cost, together

Two of the mechanisms above (S-1 brief-by-reference, S-8 bundle thinning) are **the same trade**:
replace a frozen copy with a pinned pointer. They should be ruled once, not twice, and the ruling
turns on a single question the operator owns — **is a pinned pointer that fails to resolve worse
than a stale copy that resolves?** Batch T's evidence says a failed resolve is expensive (lane 3.8
attempt 1 burned a whole lane on it), and also that the fix is known and cheap (a pre-resolved
locator table plus `git cat-file -e origin/main:<path>`, which made attempt 2 land).

Two more (S-5 commit-before-suite, S-6 document the predicate) cost essentially nothing and are
already written. They are not proposals so much as unshipped work.

The remaining ones each buy speed at the price of assurance (S-2, S-9) or of the operator's
continuity (S-3, S-4). **Those are the operator's calls and this census does not make them.**

## 5 · Honest limits — what I could not establish

**This section is the spine of the deliverable, and for this lane it carries most of the answer.**

1. **No per-lane token figure exists, and none is offered.** Section 0 states the verification.
   Every quantity in section 2 is bytes, seconds, turns or counts. **The bytes→tokens conversion
   is not instrumented anywhere in this repo**, so S-1's 334,206 B is a delivery-cost proxy and is
   not convertible to a token figure without inventing a tokenizer assumption. I did not invent
   one.

2. **The two authority files are not readable from here.**
   `to-cc\AMEND-SWEEP-001.md` (3,600 B) and `to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md`
   (5,422 B) live on the Drive transport, which is **not in the repository** — `ls to-cc` returns
   *No such file or directory* in this cloud container. I worked from the brief's working copy
   alone. **If the authority files disagree with it, they win, and this document has not been
   checked against them.** Their byte sizes are the operator's figures, restated, not measured.

3. **"Bytes of STATUS / RATIFICATION read" is unanswerable in-tree, for every lane and every
   seat.** `STATUS-DISPATCHER.md`, `RATIFICATION-2026-09-06.md`, `SESSION-dispatcher.md` and the
   `LEDGER-<repo>.md` surfaces are all `to-browser\` transport files. In-tree I can cite only the
   **rule** — `HANDOFF_PROCESS.md:366`, P8b: each `STATUS-<seat>.md` is ≤ **5,000 bytes**, decimal
   convention, chosen because "5 KB" reads as 5,000 or 5,120 and a file measured at 5,114 sits
   between them. I cannot say whether any actual STATUS file obeyed it.

4. **`intake C-F` does not resolve in-tree.** A grep for `C-F` across `docs/intake/`,
   `docs/audits/2026-09-0*` and the batch directories returns exactly one hit, and it is unrelated
   (a *"C-F Shape mis-parse fix"* in `2026-09-06-technical-closure-proposals.md:882`). I anchored
   section 3 to **intake #50** (`docs/intake/2026-08-26-tech-cost-and-delivery-telemetry.md`,
   `intake-id: 50`), whose scenario 2 is verbatim *"measured cost-per-lane on each substrate"* —
   which is what the contract describes C-F as being. **If `C-F` is a distinct row on a browser-side
   candidate sheet, section 3 is anchored to the wrong id and needs re-pointing, though its content
   stands.**

5. **I could not run a single gate, test, or the scorecard itself.** `uv` in this container is
   **0.8.17** against `required-version = "==0.11.19"`, so every `uv run --locked` command refuses.
   Running `scripts/window_metrics.py --scorecard` with system `python3` fails on
   `ModuleNotFoundError: No module named 'click'` (via `assemble_paste`). **So every scorecard
   figure in section 3 is read from source, not from output**, and the `NOT COMPUTED` bases are
   quoted from the code that would print them rather than from a run. That distinction is
   load-bearing: I have verified what the code *says* it cannot compute, not what it *does* emit
   today. **Nor did any commit gate run on this file**: `pre-commit` is not on PATH in this
   container and `.git/hooks/{pre-commit,commit-msg,pre-push}` do not exist, so the commit landing
   this artefact passed through **no** gate — not by bypass, but by absence. `consumer_at_landing`
   was therefore checked by applying its own `_CITATION_RES` patterns directly to this file's text
   (all four classes match: `[#528]`, `ADR-110`, `STANDING_RULINGS`, `intake #50`). **The
   integrator should treat this artefact as ungated and run the real gate on merge.**

6. **Batch U has no close packet, so its lanes have no outcomes here.** Everything section 1
   reports for U is dispatch-time (contract bytes, declared substrate, required review tally).
   Any U figure that looks like an outcome would be a forecast.

7. **Tool calls and dispatcher polling wake-ups are recorded nowhere, for any lane, in either
   batch.** I grepped the T close packet and both manifests. This is not a gap in my search; it is
   a gap in the record, and section 3's G-4 field list is where it gets closed.

8. **`re-derivations of the same fact` is recorded as prose, not as a count.** The seven
   anchor-predicate seat-instances in S-6 are the close packet's own tally, assembled by a human
   noticing a pattern across a night. **Nothing counts them mechanically**, so the "four times in
   one night" figure the contract cites and the "seven seat-instances" figure in §9 of the same
   packet are two different countings of overlapping events, not a discrepancy — §2.3 counts
   misreadings *by the dispatcher and integrator within the batch*, §9 counts *all seats including
   lanes*. I have cited both with their scopes rather than reconciling them into one number.

9. **The S-1 duplication measure is line-based and therefore conservative.** It counts a line as
   shared only if it is byte-identical. Near-identical lines that differ only by the lane's own
   slug — and there are many, since the slug is interpolated throughout the preamble — count as
   *unique* and so land in the 33.4% "lane-specific" remainder. **The true shared fraction is
   higher than 66.6%, not lower.** I did not compute the fuzzy version because a fuzzy threshold
   is a judgment I would then have had to defend as a measurement.

10. **`fan-out: NONE`, and that is not clean.** `command -v gemini` returns nothing in this
    container. Copilot Enterprise offload is unavailable until **intake #75** is ratified. This
    census was therefore single-seat throughout, which is a limit on its breadth: a fanned-out
    version would have read all 19 U contracts individually rather than sampling one and measuring
    the rest by hash, and would have read the full T close packet rather than four targeted ranges.

11. **No JOURNAL entry, no merge, no full suite** — per the contract. The known RED on main
    (`test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object`)
    was not encountered, because no suite was run at all here; it is recorded as not mine and not
    reproduced.
