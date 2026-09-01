# TIER (B) B-2 — SDA-1 expressed in Harbor task/trial/verifier form, as a translation and not an adoption

> **PROVENANCE — harvested COPILOT-ENTERPRISE artifact, body VERBATIM below this header.**
> Payload `B-2` from
> `docs/audits/2026-08-31-technical-batche-launch-contracts/TIER-B-COPILOT-PAYLOADS.md`, run
> 2026-09-01 from the integrator seat. Provider `copilot-enterprise`, CLI `copilot` 1.0.81,
> identity **`Robert-Dwornik_ghub`** asserted with `gh api user` before the call. Nothing below
> this line was edited, reflowed or trimmed — including the CLI's own tool-trace lines and its
> credits footer, which are part of the receipt.
>
> **Consumed by:** DM-1 (`lane-e-5-eval-sda1-harbor`), which was BLOCKED on this draft and is unblocked by it, and `[#614]` (batch E's frozen execution arc).
>
> **THE PACK'S ROUTING CLAIM WAS REFUTED BY WITNESS, and this run is the witness.**
> `TIER-B-COPILOT-PAYLOADS.md` states *"Enterprise Copilot is not driveable from this seat"*, and
> the 2026-09-01 night window took that at face value and did NOT dispatch DM-1/DM-2 as a result.
> **The operator refuted it**, citing the SDA-1 adversarial incumbent baseline
> (`docs/audits/2026-08-29-technical-sda1-adversarial-incumbent-baseline.md`, 21.15 credits,
> identity recorded) as an existing enterprise run from this machine. The mechanism is a
> **per-invocation `GH_TOKEN`** — `gh auth token --user Robert-Dwornik_ghub` scoped to the call,
> never `gh auth switch`, which this repo has recorded as unreliable. Provenance stays exactly
> where the pack assigned it: this is a copilot-enterprise artifact, not a re-route.

---

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(grep)[39m
  [38;2;145;152;161m│ "SDA-1"[39m
  [38;2;145;152;161m└ 54 files found[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252mLANE-e-5-eval-sda1-harbor.md[39m
  [38;2;145;152;161m│ docs\audits\2026-08-31-technical-batche-launch-contracts\LANE-e-5-eval-sda1-harbor.md[39m
  [38;2;145;152;161m└ 63 lines read[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252mTIER-B-COPILOT-PAYLOADS.md[39m
  [38;2;145;152;161m│ docs\audits\2026-08-31-technical-batche-launch-contracts\TIER-B-COPILOT-PAYLOADS.md[39m
  [38;2;145;152;161m└ 155 lines read[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252m2026-08-28-technical-sda1-benchmark-design-adversarial.md[39m
  [38;2;145;152;161m│ docs\audits\2026-08-28-technical-sda1-benchmark-design-adversarial.md[39m
  [38;2;145;152;161m└ 1 line read[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252m2026-08-29-technical-sda1-adversarial-incumbent-baseline.md[39m
  [38;2;145;152;161m│ docs\audits\2026-08-29-technical-sda1-adversarial-incumbent-baseline.md[39m
  [38;2;145;152;161m└ 49 lines read[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252m2026-08-28-technical-sda1-benchmark-design-adversarial.md[39m
  [38;2;145;152;161m│ docs\audits\2026-08-28-technical-sda1-benchmark-design-adversarial.md[39m
  [38;2;145;152;161m└ L1:120 (119 lines read)[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252m2026-08-28-technical-sda1-benchmark-design-adversarial.md[39m
  [38;2;145;152;161m│ docs\audits\2026-08-28-technical-sda1-benchmark-design-adversarial.md[39m
  [38;2;145;152;161m└ L120:260 (141 lines read)[39m

[38;2;63;185;80m●[39m [1mWeb Search [22m[38;2;145;152;161m(MCP: github-mcp-server) · Harbor evaluation framework task trial verifier shape (…[39m [38;2;145;152;161m42s[39m
  [38;2;145;152;161m└ {"type":"output_text","text":{"value":"From the information available, here’s...[39m

## SDA-1 → Harbor translation (comparison-run scope only)

**Scope check before the translation:** this is one pack, mapped to Harbor's shape, for one comparison run. Nothing below recommends running Harbor beyond that, installs anything, or argues for admitting it as a second executor. Where the mapping strains, I say so rather than smoothing it over.

### 1. The one-to-one mapping

Harbor's primitives are, per its own docs: a **task** (instruction.md + task.toml + environment/ + tests/test.sh + optional solution/solve.sh), a **trial** (one agent attempt inside that task's sandbox, producing a trajectory log plus workspace state), and a **verifier** (runs at trial end, inspects the resulting state, emits a scalar/JSON reward and a pass/fail).

Mapped onto SDA-1's own units:

- **One SDA-1 item → one Harbor task.** The item's frozen file(s) become `environment/` (the single synthetic commit, history-flattened, is exactly the kind of static sandbox state a Dockerfile-defined environment already assumes). The item's ground-truth statement and defect class become `task.toml` metadata. The item's prompt becomes `instruction.md`, extracted mechanically as SDA-1's Q4 already requires — this is a genuine improvement in strictness, not a loss, since Harbor's format forces the same "never retyped" discipline SDA-1 states as a precondition.
- **One (provider, item, repeat) invocation → one Harbor trial.** SDA-1's `k=3` repeat requirement (C-4) is exactly what Harbor's trial concept exists to represent: several independent attempts at the same task, same environment, logged separately. This is the cleanest part of the mapping.
- **One item's machine-checkable pass predicate → one Harbor verifier / test.sh.** For the roughly two-thirds of the corpus marked `adjudication: machine` (most producer seeded-defect items, most reviewer clean-diff items, the fan-out retrieval items), the pass predicate translates directly: the verifier script checks whether the hidden post-hoc suite goes green, whether a diff touched a forbidden file, whether a locator resolves.
- **The per-role item packs (24/20/12/15) → four Harbor task sets ("benchmarks" in Harbor's vocabulary).** Producer, reviewer, adversarial and fan-out each become a distinct dataset of tasks, which mirrors SDA-1's own insistence that one score does not fit four roles.

That much survives cleanly. What does not is the more important half of this deliverable.

### 2. Where the mapping is NOT one-to-one

- **The role-level gates (P1–P6, R1–R5, A1–A4, and the universal F0–F2) have no Harbor object.** Harbor's verifier is scoped to a single task/trial; it does not natively express "correctness ratio across 16 seeded items, compared against a named incumbent, with an absolute floor" (P1), or "zero patches across 4 clean controls" (P2), or "Phi across the whole role pack must be absolute zero" (P4). These are cross-trial aggregates. Translating them means writing an aggregator that reads N trial results after the fact and computes the SDA-1 gate — which is new code sitting *outside* Harbor's shape, not a Harbor concept. The gate logic — the part of SDA-1 that actually decides anything — is invented at this seam, not translated.
- **Phi (fabrication) is trajectory-inclusive by definition** (§4.1: "every intermediate turn is read, not only the final answer"). Harbor's verifier contract is written around inspecting final workspace state via test.sh. Checking Phi means a second, non-standard verifier pass that parses `trajectory.json` for invented API calls, invented test runs, or invented severities — a pattern the shape can technically hold (the trajectory file exists) but does not treat as the normal verifier job. Something is invented here, not merely relocated.
- **Hand-adjudicated items (poisoned diffs, planted false positives, "kills the finding" items) don't fit test.sh's scalar-reward contract.** The honest options are: (a) a verifier that can only ever return INDETERMINATE, with the actual judgment left as an artifact for a human to read — which quietly demotes several SDA-1 gates (R3, A1) from "computed" to "not computed by the harness at all," or (b) an LLM-judge verifier that reads the transcript and rules. Option (b) puts a second model into the decision loop as an execution party. That is close enough to "a second executor" that it deserves to be named and stopped on, not smoothed past — this is exactly the kind of drift the brief warns against, so I am flagging it rather than resolving it.
- **Items whose correct output is a question, not a patch** ("under-specified items," 2 of 24 in the producer pack) invert Harbor's assumption that a trial produces file-state a verifier inspects. Success here is a trajectory property ("did it ask"), not a workspace property. Same seam as Phi: the verifier has to move upstream from state to transcript, and Harbor's shape treats that as an exception, not the default case.
- **Clean controls ("no change needed") have no reference solution.** Harbor's optional `solution/solve.sh` field goes structurally unused for these items — small, but worth naming because it means roughly a sixth of the corpus (4 of 24 producer items, 6 of 20 reviewer items, 3 of 12 adversarial items) sits at the edge of what the format was designed to hold.
- **F0's served-id substitution guard (Q2) is not naturally re-derivable inside Harbor.** Harbor's own harness treats "which model it invoked" as its own configuration truth; it does not independently re-confirm the served id every round the way SDA-1's Q2 was built to catch a vendor quietly substituting a cheaper model. If this check isn't re-implemented as an explicit out-of-band probe, the exact defect the fleet already paid for (`[#492]`) can silently re-enter through the harness's own trust in itself.
- **The human-review-minutes term of P5** and **the architect's ADMIT/REFUSE/INDETERMINATE ruling on top of computed gates** both sit entirely above anything a task/trial/verifier can produce. Harbor closes at "trial passed/failed with a reward"; the multi-role verdict layer SDA-1 explicitly reserves for a human ruling (§5) has no Harbor equivalent at all, translated or otherwise.

A clean-looking version of this translation would present sections 3–4's items as fully mapped and quietly fold the aggregate gates, Phi, and the hand-adjudicated items into "verifier logic" as if that were native. It would be silently dropping the load-bearing half of the design — the clean controls and planted false positives are, in SDA-1's own words, "the load-bearing halves."

### 3. What the Harbor shape buys, and what it costs

**Buys, concretely:**
- Removes a documented failure the fleet already hit: the incumbent baseline run itself was "transcribed verbatim by the architect from the session's delivered output" because the cloud scratchpad wasn't reachable. Harbor's per-trial job directory (trajectory + verifier output, saved by the harness) removes that manual, lossy transcription step for future runs.
- Native repeat-trial support gives k=3 (C-4) a structural home instead of manually launched and manually aggregated sessions.
- Uniform sandboxing (one Dockerfile-defined environment per task) mechanizes Q0 (guard armed) and Q3 (same head, clean tree) instead of relying on a hand-run script's discipline each time.
- Automatic trajectory logging makes F2 (locator resolution) and, with extra tooling, Phi checks auditable after the fact rather than dependent on a human having watched the session live.

**Costs, concretely:**
- The actual judgment logic SDA-1 was built to defend — P5's cost-per-accepted-patch, R2's precision floor, A1's self-kill requirement — has to be authored as a bespoke aggregator outside Harbor's primitives. Harbor changes *where execution happens*, not *where the SDA-1-specific scoring lives*. That scoring code is no smaller or more trustworthy for having a Harbor task underneath it.
- Authoring 71 items across 4 packs into task.toml/environment/test.sh form is a real, one-time cost that this run does not amortize — the brief scopes exactly one comparison run, so nearly all of that authoring cost is sunk with no second run to spread it over.
- Hand-adjudicated and trajectory-dependent items push toward an LLM-judge verifier pattern, which is a scope risk the brief specifically asks to be named rather than absorbed.
- F0's substitution guard needs independent re-implementation or it silently weakens.
- Nothing about the format touches the human-review-minutes term of P5, or the architect's final ruling — those stay exactly as manual as before. Reporting that Harbor "solves" P5 would be false.

### 4. The comparison protocol

Run the same frozen head, same provider/model id, same effort tier, same `k`, over an identical item subset (a full pack, or, if cost-bound, one full role pack chosen so both a machine-adjudicated majority and at least one hand-adjudicated minority are represented — the reviewer pack's 20 items, including its 2 poisoned diffs, is a reasonable single choice) under both the hand-rolled harness and the Harbor translation. For each side, record and report side by side, not as one aggregate score (SDA-1 itself refuses aggregation, §0, and the comparison must honor that or it isn't measuring the same thing):

- Per-item verdict (pass/fail/indeterminate) and which gate, if any, failed.
- Wall-clock and token/dollar cost per item, and whether these were captured natively by the harness or bolted on afterward.
- Human minutes spent per item confirming the harness's verdict is trustworthy — this is the honesty check on Harbor itself: if a human still has to re-derive the P5/R2/A1-class gates by hand because the harness only produced trial-level rewards, that time counts against Harbor, not for it.
- Count of gates that could **not** be computed inside the shape and required an external aggregator, named individually (this is section 2's list, counted rather than described).
- Rate of INDETERMINATE or exhausted outcomes on the hand-adjudicated and trajectory-dependent items specifically, since these are the items most likely to silently degrade under translation.
- One-time authoring/setup time for each side, recorded even though it is a sunk cost for this single run, so it isn't hidden from the final report.
- Result on the existing C-1…C-15 adversarial tally (2026-08-29 baseline): for each of the 15 findings, does the Harbor-translated run reproduce the same NO/PARTIAL/YES verdict the hand-rolled baseline already recorded, a worse one, or a better one. This existing tally is the one calibration instrument this repo already trusts, so using it as the yardstick makes the single run decidable against a real prior measurement rather than an invented new bar.

The run is decidable if it either (a) reduces manual transcription/aggregation time or catches something the hand-rolled run missed, without weakening any of C-1…C-15 relative to the recorded baseline, or (b) it does not — in which case the honest conclusion is that the format changed where the work sits without changing how much of it there is, and that is a reportable, non-adoption-relevant result in itself.



Changes    +0 -0
AI Credits 30 (3m 9s)
Tokens     ↑ 474.2k (429.0k cached, 45.2k written) • ↓ 10.1k (5.4k reasoning)
Resume     copilot --resume=b9c5709d-0c8b-45d7-aeea-2dc53e9f17c0
