# lane-x-675-instrument-fixes — the three `[#675]` false-pass holes, resolved and closed

Consumers: `[#742]`, `[#743]`, `[#744]` — the three rows the integrator seat filed at batch-X3
close, which this lane implements against. Parent `[#675]` stays OPEN (operator NO-GO on
closing it, ratification item 3); this lane closes none of the four — a lane hands back a
branch and closure is the operator's act.

**Lane:** `lane-x-675-instrument-fixes` · branch `worktree-lane-x-675-instrument-fixes` ·
contract `LANE-x-675-instrument-fixes.md` · base `dbac84b8`.

---

## Part 1 — the locators, resolved in THIS tree (step 1)

The contract's rule 6: *"a line number is a claim until opened"*. All three were opened at
`dbac84b8`, the same commit the review and the integrator read them on. **All three hold, and
all three defects are still present.** Nothing had drifted.

### `[#742]` — `scripts/actions_verdict.py:205-213`

The locator is exact. Lines 206-213 are the second `gh` call:

```
206:    jobs = ["gh", "run", "view", str(match["databaseId"]), "--json", "jobs"]
207:    try:
208:        proc = subprocess.run(jobs, cwd=..., capture_output=True,
209:                              text=True, timeout=GH_TIMEOUT_S, check=False)
210:        match["jobs"] = json.loads(proc.stdout or "{}").get("jobs", []) if proc.returncode == 0 \
211:            else []
212:    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
213:        match["jobs"] = []
```

Every failure mode — non-zero exit (line 211), `OSError`, `subprocess.TimeoutExpired` (a
`SubprocessError` subclass) and `json.JSONDecodeError` (line 213) — lands on the same
`match["jobs"] = []`. `verdict_for` then computes `failing = set()` over that empty list and
returns `STATE_PASS`. **An unreadable job list renders as a clean pass.**

The row's own observation holds too: the FIRST `gh` call, at 190-200, raises
`ActionsUnavailable` on exactly these conditions. The module already knows how to say *"I could
not read this"*; the second call simply does not use it.

**A second-order defect found while resolving this one, not in the row.** `verdict_for`'s
baseline leg (240-249) reads the baseline run's jobs through the same `fetch`. An unreadable
baseline job list yields `base_jobs = {}` with `base_read = True`, so `base_failing` is empty
and **every** failing job at the tip is attributed as `newly_failing` → `STATE_REGRESSED`. That
is a false *accusation* rather than a false pass — the same hole with the sign flipped — and it
is fixed in the same pass because it is the same missing distinction.

### `[#743]` — the step-0 collision extractor, `scripts/seat_refusals.py:303-339`

Two independent legs both require a directory, so a root-level file is invisible twice over:

- `_CONTRACT_PATH_RE` (305-306) requires `(?:\.?[A-Za-z0-9_][A-Za-z0-9_.-]*/)+` — **one or more**
  path segments ending in `/`. `ARCHITECTURE.md` produces no match at all.
- `_WRITE_ROOTS` (310-314) is a tuple of directory prefixes, and the filter is
  `path.startswith(_WRITE_ROOTS)`. Even if the regex matched, the root has no admitting prefix.

**The hole is live in THIS batch, and it was measured, not reasoned about.** Running the
step-0 refusal over wave 4's own four frozen contracts:

```
file-collision: PASS -- 4 contract(s), 21 declared path(s), no file claimed twice
```

with the per-lane footprints reading:

```
LANE-x-628-docs-cut              -> protocols/ESSENTIALS.md, protocols/PLAYBOOK.md,
                                    scripts/canonical_docs.py, tests/test_claude_md_byte_cap.py
LANE-x-664-dead-callers          -> scripts/boundary_report.py, scripts/cloud_provisioning.py,
                                    tests/test_e2e_consumer_lifecycle.py
LANE-x-664-delete-list-execution -> .claude/settings.json, scripts/archive_row_body.py, ... (13)
LANE-x-675-instrument-fixes      -> scripts/actions_verdict.py
```

`lane-x-628-docs-cut` declares `ARCHITECTURE.md` in its Done-contract and it does not appear.
`lane-x-664-delete-list-execution` declares `.pre-commit-config.yaml` and it does not appear.
The two happen not to collide with each other, so **the PASS above is correct by luck rather
than by check** — which is the row's whole claim, now with this batch's own numbers behind it.

**A third observation, on this lane's own footprint.** `LANE-x-675-instrument-fixes` extracts
exactly ONE path — `scripts/actions_verdict.py` — while this lane demonstrably writes three
scripts. `scripts/seat_refusals.py` and `scripts/merge_receipt.py` are named in the contract's
**Steps** section, and `declared_footprint` reads the **Done-contract** section only. That is a
deliberate, measured choice documented in the function's own docstring (whole-file extraction
made every lane share references and the refusal meaningless), and it is not this row's scope
to change. It is recorded because it bounds what the fixed check can promise: widening the
extractor to see root-level files does not widen it to see paths declared outside the
Done-contract, and a reader of a future PASS should know which of the two limits they are
relying on.

### `[#743]` sub-question — does `file_purpose_graph._REL_PATH_RE` share the blindness?

**Yes, and byte-for-byte.** `scripts/file_purpose_graph.py:677-678` is character-identical to
`seat_refusals._CONTRACT_PATH_RE`:

```
r"(?:^|[\s`'\"(\[])((?:\.?[A-Za-z0-9_][A-Za-z0-9_.-]*/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9]{1,6})"
```

That identity is intentional — `_CONTRACT_PATH_RE`'s own comment says so: *"Same shape
`file_purpose_graph._REL_PATH_RE` uses, deliberately: two organs disagreeing about what counts
as a path is a class of defect this repo already carries."* The consequence is that a task row
naming `ARCHITECTURE.md`, `CLAUDE.md`, `pyproject.toml` or `.pre-commit-config.yaml` in its body
produces **no `IMPLEMENTS` edge**, so `graph-task-coverage` cannot see that the row claims the
file.

The disposition of that finding is recorded in Part 3, after the fix that answers it.

### `[#744]` — `scripts/merge_receipt.py:449-466`, `median_report`

`wanted = [r for r in receipts if r.kind == kind]` is the only filter. Nothing reads `closed`,
nothing reads `failed_steps()`, nothing reads `missing_required()`. Two further surfaces make
the same unchecked claim in prose:

- `read_ledger` (369) is docstringed *"Every closed receipt, oldest first"* and filters nothing.
- `MedianReport.render` prints `n=… closed receipt(s)` and, at n=0, *"holds no closed … receipt
  yet"*.

**This hole is not hypothetical either — it is fully realised in the live ledger.**
`logs/MERGE-RECEIPTS.jsonl` holds exactly two rows, and **both have failed steps**:

```
lane-x-675-step-4  kind=arc  steps=[lint, regen, regen-organ, targeted, targeted-retry,
                                    targeted-code, targeted-livetree]  FAILED=[targeted, targeted-retry]
lane-x-675-step-7  kind=arc  steps=[targeted-lane]                     FAILED=[targeted-lane]
```

and the tool at `dbac84b8` reports, over exactly that data:

```
arc minutes over n=2 closed receipt(s)
  median   9.4 min   (target 3.6: under 30 -> MET)
  range    0.0 .. 18.7 min
  per merge 0.0, 18.7
```

A **0.0-minute** entry — one receipt that recorded a single step, which failed — is half the
sample, and the instrument answers **"target 3.6: MET"**. That is `[#675]`'s filed failure class
verbatim: a reader returning a plausible, flattering value because the discriminating field is
absent from what it looks at.

---
