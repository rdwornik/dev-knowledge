# L7 — Dispatch codification (M10): PLAYBOOK Ch8 + `gen_lane_contract` emits the command

| Field | Value |
|---|---|
| **Lane** | L7 `dispatch-codification` · branch `worktree-dispatch-codification` |
| **Contract** | `LANE-L7-dispatch-codification.md` (operator-side, `$env:CLAUDE_PROMPTS_DIR`) |
| **Scope** | `protocols/PLAYBOOK.md` Ch8 (exclusive) · `scripts/gen_lane_contract.py` · its tests |
| **Shape** | local background lane, commit-and-STOP |
| **Base** | `aeec0fd1` |

---

## 1. Ground truth — Ch8 and `gen_lane_contract` as they stand

Recorded before any edit, so every delta below is attributable.

### 1.1 What Ch8 already says about dispatch

Ch8 spans `protocols/PLAYBOOK.md` lines 1236–2512 and carries **fifteen** `###` subsections. Four
are dispatch-bearing, which is why "codify the cheat-sheet" is *not* a green-field write:

- **"Dispatch prompts and the contract of record — two locations, one of them in the tree."**
  The prompts-dir rule (`~/Downloads` by default, `CLAUDE_PROMPTS_DIR` override) and the Q6
  contract-as-file ruling. States that a dispatch line cites `<PROMPTS_DIR>\<file>` **rather than
  a hard-coded absolute path**, so the line stays portable and one operator's directory layout
  stays out of an artifact other people read.
- **"The dispatch surface is `dispatch <file>` — the contract file is the source ([#509] v2)."**
  Claims in its opening sentence that *"the operator's whole dispatch surface is one typed line:
  `dispatch <contract.md>`"*, implemented by `win-tooling`
  `scripts/dispatch/Invoke-Dispatch.ps1` (merged `d743937`). Carries the batch-6 doubled-prefix
  incident, the `## Dispatch`-block contract mode, the table fallback, the closed effort enum and
  the execution gate.
- **"Cloud lanes — the receipt gate and the fresh-branch rule."** Q5 receipt gate, Q4
  fresh-off-`origin/main` hygiene, and the `claude/<slug>` branch prefix. Explicitly records
  **which-substrate as OWED, not ruled** — *"a section about cloud lanes is hard to apply without
  a test for which lanes are one, and this chapter carries none today."*
- **"Model + effort are stated at dispatch — the routing matrix."** The opus/sonnet/haiku table,
  the 2026-08-07 context-load amendment, `max` held out of *routing*, and the three dispatch
  constants.

**What Ch8 does NOT carry today — the gap M10 names:**

1. **No local-vs-cloud boundary a seat can apply.** The cloud-lane section says so in its own
   words and files the gap as G1 of `docs/audits/2026-08-20-technical-playbook-status.md`. The
   operator's cheat-sheet resolves it (does the work need his disk, or is everything on
   `origin/main`?) and that resolution is nowhere in the chapter.
2. **No enumeration of the three command shapes.** `Dispatch-Lane` and `Dispatch-CloudV2` appear
   **nowhere in `protocols/`** — verified by grep across the whole repo: every hit is in
   `scripts/gen_lane_contract.py`, its tests, `tasks/539-*`, two handoff bundles and six
   `docs/audits/` files. Zero doctrine hits.
3. **A stale headline claim.** *"The operator's whole dispatch surface is one typed line:
   `dispatch <contract.md>`"* is true of one shape of three. `Invoke-Dispatch.ps1` dispatches a
   **local** contract; it is not the cloud transport and not the interactive form. A seat reading
   that sentence while holding a cloud brief has no next move.
4. **No integration-is-always-local-and-interactive rule.** Ch8's parallel-session section rules
   that integration happens from the primary checkout on operator GO; it never states the
   consequence for *dispatch* — that integration cannot be a background lane at all, because a
   background lane can neither merge to main nor ask a question.

**Stale Ch8 claims handed over by LANE-L5:** *none received.* At the time of this write L5 had not
landed — `git worktree list` shows six sibling lanes all still at the batch base `aeec0fd1` with
no lane commits, and `docs/audits/` carries no L5 artifact. Recorded as **not-received**, not as
none-existing.

**One claim IS inherited, from the predecessor lane.** `docs/audits/2026-08-21-technical-ch8-
dispatch-codification.md` (batch-1 lane A, `[#539]` — the lane that wrote the Q1/Q3–Q6 rulings
into Ch8 and built this generator) closes with an open item aimed squarely here:

> `templates/prompt-template.md` v1.14 carries the effort enum as the closed four and shows a
> `claude --bg --model … --effort …` dispatch line, while `[#539]`'s contract shows the
> `Dispatch-Lane` form. Both are live; neither is wrong. **If `Dispatch-Lane` becomes the stated
> surface, the card is the point-of-use copy that would follow** — not this lane's file.

This lane **does** make `Dispatch-Lane` the stated surface. The card is therefore now owed an
update, and it is outside this lane's write scope (`protocols/` Ch8 + the generator). Carried as
residual R1 in §6.

### 1.2 What the generator already emits — and the defect in it

`scripts/gen_lane_contract.py` (576 lines, Click-based, `emit` / `check` / `enums`).
`render_contract` is pure: same `LaneSpec` in, byte-identical markdown out. Emitted sections:
`Dispatch`, `Worktree pairing`, `[Receipt gate]`, `Done-contract`, `Decision budget`, `Steps`,
`What NOT to do`.

It **already emits a command line** — the surprise of step 1, and it sharpens the deliverable. In
`render_contract`, unconditionally:

~~~
## Dispatch

```
Dispatch-Lane {slug} {fname} -Effort {effort}
```
~~~

**The defect is the one the contract's failure-mode paragraph predicts, with the polarity
reversed.** `spec.cloud` is honoured in exactly one place — it adds the `## Receipt gate` section
— and **nowhere else**. So, before this lane:

- `gen_lane_contract emit --cloud` produced a contract whose command line was **`Dispatch-Lane`**,
  the *local* helper. **A cloud lane handed a local command** — authoritative-looking and wrong.
- That contract's pairing line declared branch **`worktree-<slug>`**, while Ch8's own cloud-lane
  section rules a cloud lane onto **`claude/<slug>`**.
- There was **no interactive shape at all**. `MODE_ENUM` (`execute | plan-then-auto | plan`) is a
  *lane mode*, not a substrate; nothing in the generator's model could express "this is an
  interactive seat act."

`parse_contract` mirrored the blind spot: `_DISPATCH_LINE_RE` matched `Dispatch-Lane` and nothing
else, so a contract carrying the **correct** cloud command would have been refused by the live
`lane-contract-check` pre-commit hook as *"no dispatch line found"*. The gate enforced the wrong
shape onto two cases of three.

**Consequence for the closure contract.** Item 2 is not "add a missing emission" — it is "make the
existing emission *shape-selective*, and make the checker able to verify the selection". The test
the contract demands (*a generated contract with no command line fails*) is necessary but not
sufficient on its own: it would have passed on 2026-08-22 against a generator that emitted the
wrong command for two shapes out of three. **Item 3 is the load-bearing one.**

### 1.3 Cheat-sheet verified against the live helpers

The contract calls the operator's cheat-sheet authoritative. It was still checked against source,
because a command line that does not exist is precisely the failure this lane exists to close.
`win-tooling/config/dispatch-helpers/DispatchHelpers.psm1` (1211 lines) is the stated source of
truth; `scripts/dispatch-helpers/Apply-DispatchHelpers.ps1` deploys it SHA-256-compared and
auto-loading.

| Cheat-sheet claim | Source | Verdict |
|---|---|---|
| `Dispatch-Lane <slug> <FILE.md> [-Effort]` | alias L1196 → `Start-DispatchLane` L47; `Slug`/`File`/`Extra` positional 0/1/2 | **confirmed** |
| optional 3rd positional = extra instruction | `[Parameter(Position = 2)][string]$Extra` | **confirmed** |
| `-Effort ∈ {low,medium,high,xhigh,max}` | `$effortMap`, plus `l`/`m`/`med`/`h`/`x` shorthands | **confirmed** (shorthands are an undocumented bonus) |
| model defaults `opus`; `bypassPermissions` default | `$Model = 'opus'`, `$PermissionMode = 'bypassPermissions'` | **confirmed** |
| creates `worktree-<slug>`, refuses if that branch exists | guard 1, "SKIP-IF-BRANCH-EXISTS" | **confirmed** |
| `Dispatch-CloudV2 <FILE.md> -Title '<slug>'` | alias L1198 → `Start-DispatchCloudV2` L871; `File` positional 0, `Title` named | **confirmed** |
| whole file is the brief, JSON body | `New-CloudSessionBody`; docstring *"puts the brief in a JSON body"* | **confirmed** |
| binds Revision `main` | `[string]$Revision = 'main'` | **confirmed** |
| G1 created / G2 bound / G3 receipt; empty `sources` = hard fail | docstring: G1+G2 **HARD**, G3 **SOFT ON TIMEOUT** | **confirmed** |

Two facts the cheat-sheet omits and a seat should have, both folded into the Ch8 codification:
`Start-DispatchLane` polls up to `-WaitSeconds 120` for the branch and reports a **timeout as a
WARNING, not an error** (the lane may still be coming up — it refuses to claim a failure it has
not established); and `Dispatch-CloudBrief` is a **superseded** third alias that prints its own
supersession notice on every call.

### 1.4 Library-first verdict (required by the contract)

**Verdict: no external library. The library-first move is internal, and it was taken.**

The mechanization half is string emission from a generator that already exists. There is no
external candidate for "emit a line into a template" that would not become a second templating
idiom beside `render_contract`'s `parts: list[str]` accumulation — the contract names exactly that
hazard, and it is the real risk here.

Reused rather than rebuilt, itemised:

- **`render_contract`'s `parts.append` idiom** — the command emission is one more branch inside
  the same function. No template engine, no `str.format` layer, no second renderer.
- **`_DISPATCH_LINE_RE`'s regex-per-shape idiom** — the two new shapes get sibling patterns
  compiled beside it, read by the same `parse_contract`, rather than a parser rewrite.
- **`validate_branch_naming.validate_lane_worktree_name`** — still called, still not
  re-implemented; the module docstring's existing library-first claim stays true.
- **`LaneContractError` and the `validate_*` refusal posture** — the new shape enum refuses
  through the same class with the same *name the enum, never round to a neighbour* message shape.
- **`click.Choice`** — shape selection is a CLI enum the same way model/mode/effort already are.

The one thing deliberately **not** reused: `MODE_ENUM`. It was the tempting hook — already a
declared enum on the spec — and it is the wrong one. Mode is *how a lane thinks*; shape is *where
it runs*. Overloading it would have made `plan` imply a substrate.
