# The integrator seat's cost line — the measurement definition, frozen

Consumers: `[#737]` — its last two open done-when clauses are this file's subject. The row asks
for *"the dispatcher and integrator seats observed booting at `sonnet` and `opusplan`
respectively, which is the only evidence that the ruling took effect rather than merely being
recorded."* §2 is that observation and it came back negative — the integrator ran 100% Opus — and
§3–§4 are why `opusplan` was never a reachable target for that clause. This lane does not close
the row; the correction is filed here for its owner.

> Lane `aa-2`, batch AA. Carried by `docs/audits/2026-09-15-technical-batch-aa-manifest.md`.
> **This file exists so that the next batch's integrator figure is comparable with USD 82.53.**
> A paired comparison is worth exactly as much as the sameness of its two measurements, and the
> definition below is the half that has to be written down before the second one is taken.

---

## 1 · The definition

> **The integrator line** is the sum over **one attended seat session's own transcript**
> (`~/.claude/projects/<project>/<session-id>.jsonl`), turns de-duplicated on `message.id`,
> **every model's four token counts** — `input_tokens`, `output_tokens`,
> `cache_creation_input_tokens`, `cache_read_input_tokens` — priced through
> `provider_registry.resolve_rate` against the registry's declared rate card, **bounded by a
> declared UTC `[since, until]` window**, reported **per model**.

Five clauses, and each is load-bearing rather than descriptive:

**(a) By SESSION, never by directory.** The five attended seats run in the primary checkout, and
Claude Code's session store is keyed per *directory*. Asking `lane_cost` for the batch-Z
integrator by its directory returns **USD 8,714.37 over 52,822 calls across six models** — that
checkout's lifetime — against a real **USD 82.53**. The close packet's own words: *"A
per-directory tally reported as a per-lane cost would have overstated the night by 32x."*

**(b) De-duplicated on `message.id`.** The batch-Z transcript carries **1,382 turn records for
624 distinct calls** — 2.2x. Summing records doubles the bill, and a doubled bill is
indistinguishable from a busy night.

**(c) Cache reads are IN.** They are **80.8% of this seat's money** (see §3). `logs/TOKEN-LOG.md`
drops them "for comparability"; a seat figure that did the same would understate the integrator
line by four fifths.

**(d) The window is DECLARED and rides the row.** A session transcript keeps growing. The same
batch-Z file prices at **USD 82.53 at 06:51:12.577Z** and **USD 89.88 at end-of-file** — 9%
apart, both honest. The window is therefore a *parameter*, stored on the ledger row and never
derived from the turns found: a window computed from the data can never disagree with the data,
so it could not catch the case it exists for.

**(e) Per model.** A split seat runs two models in one sitting. A row reporting only a total
would look **identical** whether the split fired or not.

**Honest limit, inherited and restated:** these are list prices × counted tokens. Not an invoice —
no subscription, allowance, discount or partner route. The right use is comparison.

## 2 · The baseline, reproduced

The contract's instruction was *"find where that figure is computed and reproduce it yourself
before you change anything. A number you inherited is a claim."* It was not computed anywhere: no
verb in this repository could take a session id. The figure was produced by hand at the batch-Z
close, by a method that lived nowhere in the tree.

Reproduced first by reading the transcript directly with `lane_cost.read_transcript_usage` +
`lane_cost.price_usage`, then — after the build — by the verb this lane added:

```
uv run --locked python scripts/lane_cost.py seat --session 9b8de937 --batch Z \
    --since 2026-09-14T23:00:00Z --until 2026-09-15T06:51:12.577Z

seat 9b8de937  batch=Z  USD 82.53 over 561 call(s)  [rates as_of 2026-06-24]
  tokens: in 1,122 / out 406,590 / cache-write 768,862 / cache-read 135,106,713
          / total 136,283,287
  window 2026-09-14T23:00:00Z .. 2026-09-15T06:51:12.577Z
  claude-opus-5: USD 82.53 (136,283,287 tokens, 561 call(s), 100% of the row)
```

**Exact on both figures** against the close packet's `USD 82.53` / `136,283,287 tokens`. The
cutoff `06:51:12.577Z` was *recovered*, not assumed: the packet stated the window as
`23:07Z -> 06:51Z`, and a running total over the de-duplicated turns lands on the packet's token
count to the token at that timestamp. The packet's `23:07Z` start is one minute before the
session's first assistant turn (`23:08:17.500Z`), so the lower bound is not binding and any value
at or before it reproduces the same figure.

`100% of the row` is the decorative-split detector reading correctly: the seat was ordered
`opusplan` and ran entirely on `claude-opus-5`.

## 3 · Where the money actually goes — and why it decided the design

Whole session (all 624 calls, the unwindowed read), `claude-opus-5`, rates `as_of 2026-06-24`:

```
leg                    tokens   $/MTok    USD    share    at sonnet    saved
input                   1,248    5.000    0.01    0.0%         0.00     0.00
output                472,169   25.000   11.80   13.1%         4.72     7.08
cache-write           866,249    6.250    5.41    6.0%         2.17     3.25
cache-read        145,314,211    0.500   72.66   80.8%        29.06    43.59
TOTAL             146,653,877            89.88  100.0%        35.95    53.93
```

**Three facts follow, and all three are measurements rather than inferences.**

**(1) Opus is 2.50x Sonnet on EVERY leg.** `claude-opus-5` is 5.0/25.0 and `claude-sonnet-5` is
2.0/10.0 (`ecosystem/provider-registry.yaml`), and both cache legs are multipliers on the input
rate (x1.25 write, x0.1 read), so the ratio is uniform. Moving work from Opus to Sonnet saves
**60% of its dollars regardless of its token shape** — there is no input-vs-output asymmetry to
model, and a plan built on one would be built on a number that is not there.

**(2) The seat's bill is 81% cache reads** — the context re-sent every turn. Its cost is
therefore *(context size) × (turn count) × (rate)*, and **context is a lever equal to rate**.

**(3) The prompt cache is PER MODEL, so a model switch re-writes the whole context.** Measured on
six mixed-model transcripts on this host — every one of them, and the instrument discriminates
(non-switch turns sit at the median):

| transcript | switch | median cache-write | AT the switch | ratio |
|---|---|---|---|---|
| `2403449b` | opus-4-8 → fable-5 | 1,187 | 294,673 | 248x |
| `2a19ac13` | fable-5 → opus-4-8 | 1,234 | 263,952 | 214x |
| `49368812` | fable-5 → opus-5 | 972 | 379,585 | 391x |
| `4f7e9b52` | sonnet-4-6 → opus-4-8 | 614 | 29,751 | 48x |
| `b2e0e415` | fable-5 → opus-5 | 1,759 | 214,498 | 122x |
| `c975ae5f` | fable-5 → opus-5 | 1,166 | 241,535 | 207x |

At the switch turn `cache_read` also collapses to ~20–25K from a session median of 245K–429K —
the small shared prefix. Every one of these sessions switched **exactly once**.

**The arithmetic that chose the design.** At the integrator's own mean context (145,314,211
cache-read tokens / 624 calls = **232,875 tokens per call**):

- one switch **into Opus**: 232,875 × $6.25/MTok = **USD 1.46**
- one switch **into Sonnet**: 232,875 × $2.50/MTok = **USD 0.58**
- a round trip Opus→Sonnet→Opus: **USD 2.04**
- one turn moved Opus→Sonnet saves 232,875 × $0.30/MTok + (472,169/624) × $15/MTok =
  **USD 0.0812**

**Break-even: 25 consecutive Sonnet turns per round trip.** Batch Z's seat ran 624 calls across
roughly six merges; a merge walk has on the order of eight mechanical turns between judgments.
**A per-turn split at this context size loses money.**

## 4 · What that ruled out, and what it ruled in

**`opusplan` cannot carry this split**, and the reason is mechanical rather than a preference.
It is Opus while the session is in *plan mode* and Sonnet after — it keys on a UI mode, while
this seat's halves divide on *judgment vs. mechanics*, which interleave many times per merge.
Each toggle is a model switch, and §3 prices those. It was also already measured **inert on a
background shape** (`dispatch_surface.BACKGROUND_INERT_MODELS`: `lane-x-689-conductor-e-proof`
ordered `opusplan`, ran 84 of 84 turns on `claude-sonnet-5`).

**AX22-3's substance is kept and its named means is replaced.** The ruling (2026-09-11) said the
integrator *"judges merge verdicts on Opus while running suites and teardowns on Sonnet"*. That
clause is now encoded directly, in `gen_seat_boot.SEAT_PHASES`, rather than routed through a tier
keyword that cannot express it. **A ruling binds its merits, not its quoted token** — and this is
flagged for the operator rather than absorbed, because replacing a ruling's stated mechanism is
visible to whoever made it. Rationale is carried in `gen_seat_boot.SPLIT_RATIONALE`, beside the
map, so the next seat to read it does not have to find this file.

**The split is two SESSIONS, and the seam is a FILE.** Each session holds its own context on its
own model, permanently cached; an escalation is a message between two live sessions rather than a
switch that re-caches 232,875 tokens. Ch8 point 6 already rules STATE IS FILES — this applies that
rule to the seam inside one seat. It also cuts the *other* lever: the execute session boots from a
plan file rather than inheriting the plan half's accumulated deliberation, so its context — the
81% leg — starts small.

## 5 · The projection, named as a projection

**This is not a measurement and must not be cited as one.** The next batch's integrator line is
measured by the next batch.

| assumption | integrator line | vs USD 82.53 |
|---|---|---|
| 40% plan / 60% execute turns, execute context the SAME 232,875 (pessimistic) | ~USD 52.82 | −36% |
| same split, execute context half (it boots from a plan file, not a deliberation) | ~USD 43 | −48% |

Both are above the floor a pure rate cut would give (0.4 × 82.53 = USD 33). The turn split is the
assumption doing the most work here and it is **unmeasured** — nothing in the batch-Z transcript
labels a turn as judgment or mechanics, and this lane did not invent a classifier to pretend
otherwise.

## 6 · Where the evidence stops

- **The 232,875-token mean context is batch Z's**, not a constant. A quieter batch re-prices every
  figure in §3, and the break-even moves with it. The numbers carried into the boot paste are
  labelled with the session they came from for that reason.
- **The per-model cache finding is six transcripts on one host**, all Claude Code, none of them an
  integrator seat. It is consistent and the instrument discriminates, but it is not a vendor
  statement, and none of the six switched more than once — so nothing here measures a *repeated*
  switch directly; the round-trip figure is two single switches added.
- **Nothing here measures the split running.** Every figure is the unsplit seat, priced two ways.
  The done-when's second half — *"the next batch's integrator line is measured and lower"* — is
  **not this lane's to close**, and this lane does not claim it. What is delivered is the split
  plus the instrument, wired so the figure appears without anyone remembering to look.
- **The USD 82.53 baseline is a floor in one respect inherited from the registry**:
  `claude-haiku-4-5-20251001` carries no rates row, so any seat that ran haiku would report it
  UNPRICED. The batch-Z integrator ran only `claude-opus-5`, so this does not touch the baseline —
  but a future seat's figure could be a floor for that reason, and the row says so when it is.
