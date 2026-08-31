# PROBE batch-e-c-codespace-admission — does a FRESH codespace clear all three receipt legs and run one hub gate end-to-end?

**This is a PROBE, not a lane.** It is deliberately NOT named `LANE-*.md`: it pairs to no
branch, writes no tree file, and creates no commit, so treating it as a lane contract would
put a non-lane through the lane gates. Batch E §1(C).

| Runs on | Mode | Effort |
|---|---|---|
| codespace (fresh) | execute | high |

## WHY THIS PROBE EXISTS

Ruling Z-G3 made "GitHub compute is the DEFAULT substrate" **CONDITIONAL**, naming the W4
defects. `[#616]` recorded W4 defect 3 live on 2026-08-29: a codespace presented a clone
**50 commits behind** with nothing in the session surfacing it — in-container HEAD
`7709613…` against pushed `origin/main` `66662c7…`, `git status -sb` reading
`## main...origin/main [behind 50]`. The paired contrast on a FRESH codespace 8 minutes later
matched pushed HEAD exactly and reported `uv 0.11.19`.

**The hypothesis on record is codespace AGE, not an image defect.** This probe tests it on a
fresh machine and reports the three legs either way.

## THE THREE RECEIPT LEGS — a conjunction, reported individually

Report each leg's value explicitly. A probe that reports a verdict without its legs has not
produced a receipt.

```
L1  Ok                    the dispatch itself succeeded
L2  RemoteExitCode == 0   the remote command ran and exited clean
L3  receipt HEAD == pushed HEAD
```

**PUSHED HEAD AT DISPATCH: `666f2dcb12fcd886e665105d6da3a9c66b2373b5`** (`origin/main`).
L3 compares the in-container `git rev-parse HEAD` against that SHA, verbatim.

## STEPS — in this order, because the order is the test

1. **Report the environment BEFORE changing it.** This is the W4 defect-3 measurement and it
   must be taken on arrival, not after a fetch:
   ```
   pwd
   git rev-parse HEAD
   git status -sb
   git log -1 --format=%cI
   ```
   Print all four verbatim. If `git status -sb` says `behind`, **say so plainly** — that is
   the defect reproducing, and reporting it is worth more than a green run.

2. **Fetch to pushed HEAD.** `git fetch origin main` then `git checkout 666f2dcb12fcd886e665105d6da3a9c66b2373b5`
   (detached is fine). Re-print `git rev-parse HEAD`. **This is L3's measurement.**

3. **Provision `uv` by the measured step — do NOT trust the image's `uv`.**
   ```
   python3 -m pip install --target ./uvpin "uv==0.11.19"
   ./uvpin/bin/uv --version
   ```
   Expect exactly `uv 0.11.19` (the ADR-106 `required-version = "==0.11.19"` pin). Report what
   you actually got. Also report the image's own `uv --version` if one is on PATH, so the two
   are on the record side by side.

4. **Run ONE hub gate end-to-end**, using the provisioned uv:
   ```
   ./uvpin/bin/uv run --locked python scripts/audit.py health --parallel
   ```
   Report its **exit code** and its final `health:` line verbatim. This is the "gate green" half
   of the admission condition. If it exits non-zero, report the failing check by name — a named
   defect is the deliverable, not a pass.

5. **Print the receipt block** as the final message, in exactly this shape:
   ```
   L1 Ok:               <true|false>
   L2 RemoteExitCode:   <n>
   L3 receipt HEAD:     <sha>   pushed: 666f2dcb12fcd886e665105d6da3a9c66b2373b5   MATCH: <yes|no>
   GATE exit:           <n>
   GATE line:           <the health: line verbatim>
   UV (provisioned):    <version>
   UV (image, if any):  <version|absent>
   ARRIVAL HEAD:        <sha from step 1>   BEHIND: <yes|no>
   ```

## WRITE-SCOPE (frozen)

**NONE — this probe writes no tree file, creates no branch and makes no commit.** `./uvpin/`
is a scratch directory inside the disposable container and is never committed. If a hook or a
closure proposal invites a commit, decline: this probe is read-only by contract.

## WHAT NOT TO DO

- No commit, no push, no branch, no merge.
- No JOURNAL entry, no row, no index regeneration.
- **Do not repair a red leg.** If the clone is stale, if `uv` is wrong, if the gate REDs —
  **report it**. The admission condition is allowed to fail; a probe that fixes the thing it
  was measuring has destroyed its own measurement.
- Do not report a gate result you did not observe.
