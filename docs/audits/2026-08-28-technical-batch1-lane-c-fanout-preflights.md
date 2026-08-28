# Batch-1 lane L3 — fan-out acceptance preflights, and the precondition verdict

- **Lane:** L3 (`lane-c-491-fanout-acceptance`), batch-1, 2026-08-28
- **Contract:** `docs/audits/2026-08-28-technical-batch1-launch-contracts/BATCH1-LANE-CONTRACTS-2026-08-28.md`
- **Substrate:** LOCAL (Q1 YES → not cloud; Q2 YES → operator disk holds the vendor CLIs)

## Verdict, first, because it decides everything below

> **PRECONDITIONS FAILED. The fan-out pack was NOT started, and no producer item was run.**

This is the contract's own designed path, not a lane failure. Step 2 exists to run the
preflights **"BEFORE any pack spend"** so a blocking defect is discovered **"now, not after 71
items"**, and step 3 is explicitly conditional: **"Q0–Q7 preconditions hold or the run does not
start."** They do not hold. The lane stopped where it was told to stop.

**No verdict word is emitted about any provider.** The three verdict words are the architect's
ruling on the evidence; this artifact carries computed gates and measurements only. Where a
contract clause is *named* below (C-9's ceiling, C-8's `unknown`), that names the MECHANISM the
clause specifies — it is not this lane ruling, and an integrator should not read it as one.
(Terra HIGH, 2026-08-28: an earlier draft of this artifact used a verdict word directly while
claiming not to. Corrected, and recorded rather than quietly reworded.)

## Blocker 1 — the SDA-1 artifact does not exist on this machine

The lane's **first act** is *"Persist the SDA-1 design+critique artifact **verbatim** into
`docs/audits/`, with a header noting its cloud provenance and receipt id."*

**It is not present.** Searched: the operator's prompts dir (`~/Downloads`), the whole of
`docs/`, and the repo tree. The only occurrence of the token `SDA-1` anywhere reachable is
**inside the batch contract itself**. There is no artifact, no cloud provenance, and no receipt
id to record.

**The lane did not synthesise one, and the reason is the lane's own subject matter.** L3 exists
to measure whether fan-out heads can be trusted not to fabricate; writing a plausible
"adversarial artifact" from the contract's summary of it would be precisely the failure the
fan-out scar records — content with the shape of evidence and no evidence behind it. An
artifact that cannot be persisted verbatim is reported missing.

Since the contract makes that artifact **this lane's frame** (*"Sol's verdict is ACCEPTED as
this lane's frame"*), steps 3–4 have no ratified basis to execute against even if the transports
were healthy. They are not.

## Blocker 2 — three of four providers have no working transport

Probed live on this host, 2026-08-28:

| provider | transport | state | evidence |
|---|---|---|---|
| **Kimi** | `kimi` | **ABSENT** | not on `PATH` |
| **GLM** | `glm` | **BROKEN** | `/c/Users/1028120/bin/glm` is **HTML, not a binary** — its first bytes are `<!DOCTYPE html>`, a failed download that has been sitting on `PATH` masquerading as a CLI. Invoking it yields a shell syntax error, and note it exits **rc=0** while doing so |
| **DeepSeek** | `deepseek` | **ABSENT** | not on `PATH`. Consistent with ADR-115 §2.1: DSH's runtime is recorded as *not viable today* |
| **agy** | `agy` | **PRESENT** | `1.1.21`, responds correctly to a print-mode probe |

The GLM row is the one worth carrying forward: a corrupt download on `PATH` that **exits 0** is
worse than an absent binary, because a harness testing "is the CLI callable?" by exit code reads
it as healthy.

## Preflight results for the one live transport (`agy`)

Probe: `agy --output-format json --effort low -p "Reply with the single token PROBE-OK"`.
Returned `status: SUCCESS`, `response: "PROBE-OK"`, 1.77 s, 13,761 total tokens.

Note the flag shape, since the contract's other lanes may reuse it: **`agy` rejects `-o`** — the
long form `--output-format` is required, and `--effort` is mandatory for this path.

| probe | required by | result |
|---|---|---|
| **Q2 — served-id** | **C-9** | **FAIL.** The JSON envelope carries `conversation_id`, `status`, `response`, `duration_seconds`, `num_turns`, `usage` — and **no model identifier of any kind**. The transport cannot report which model served the round. Per C-9 a transport that cannot report its served id **hits that clause's ceiling** — the clause is named, not applied as a ruling — which is the precise defect the preflight step was added to surface before 71 items were spent. Self-report is not a substitute: the recorded behaviour of this CLI is that `status` misreports, so asking the model which model it is would be evidence of nothing |
| **rate-shape** | **C-8** | **`unknown` → precondition failure.** `usage` reports token counts and no billing mode or price. The auth path is an OAuth session, which *suggests* subscription, but that is **inferred from how it authenticates, not measured from what it reports**. C-8 requires the tag to come from the probe, and `unknown` is defined as a precondition failure |
| **instruction-file precedence** | **C-10** | **NOT RUN.** Recorded as owed. It is a measurement *for the future producer pack*, and running it against a single surviving transport whose served id is unknowable would produce a result nothing could be attributed to |

## Raw receipts (terra asked for them, correctly)

```
$ agy --output-format json --effort low -p "Reply with the single token PROBE-OK"
{"conversation_id":"784d24e7-acc6-4c66-8fe0-c312d9a1ec68","status":"SUCCESS",
 "response":"PROBE-OK
","duration_seconds":1.7732591,"num_turns":1,
 "usage":{"input_tokens":13757,"output_tokens":4,"thinking_tokens":0,
          "cache_read_tokens":0,"total_tokens":13761}}

$ head -3 /c/Users/1028120/bin/glm
<!DOCTYPE html>

$ glm --version
/c/Users/1028120/bin/glm: line 9: syntax error near unexpected token `newline'
/c/Users/1028120/bin/glm: line 9: `<!DOCTYPE html>'
rc=0

$ which kimi deepseek   ->  (no output)
$ agy --version         ->  1.1.21
```

The `agy` envelope above is the whole of it: there is no model field to omit.

## What this means for the gates, stated so it is not re-derived

The contract already required `UNCALIBRATED` beside every absolute floor (C-2, incumbent
billing-blocked) and `VACUOUS` where G1v2 clause (a) is vacuous at `R_i=0`. Those disciplines
never got to apply: with **one** transport live, **no** served-id reporting, and **no** ratified
basis artifact, there is no matrix to emit that would mean anything. Emitting one would be a
green nothing earned — the exact class Z-G4 and the `UNCALIBRATED` discipline exist to prevent.

## Candidate filings handed to the integrator

Per shared clause A5, the lane files nothing itself.

1. **CANDIDATE — producer-pack prerequisites.** C-1's rejection-tax cost model, C-6's
   adversarial suite, C-15's load-bearing list. Unchanged by this lane; still owed before any
   producer item runs.
2. **CANDIDATE — corpus rotation (C-13).** Ground truth never committed alongside the items.
3. **CANDIDATE — served-id reporting is an admission precondition.** A transport that cannot
   report which model served a round hits C-9's ceiling, so this is not a nice-to-have:
   it decides whether a provider can be evaluated at all. Measure it at admission, not at pack time.
4. **CANDIDATE — a transport-health preflight that does not trust exit codes.** The GLM row is
   the witness: an HTML file on `PATH` exiting 0. Any future fan-out harness should assert the
   binary is a binary before it counts a provider as available.
5. **CANDIDATE — locate or re-commission SDA-1.** The batch contract treats it as existing and
   as this lane's frame. Either it lives somewhere not reachable from this host and needs a
   locator recorded, or it was never produced and the contract's basis clause is unfounded.

## Honest limits of this artifact

Everything above is a measurement on **one host at one moment**. `PATH` absence is not proof a
provider is unavailable to the operator by another route, and a corrupt `glm` is a local
install defect rather than a statement about GLM. What the lane can say is bounded to what it
could run, and it says only that.
