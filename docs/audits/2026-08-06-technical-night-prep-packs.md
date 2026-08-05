# Implementation prep packs — B1–B5 and the [#487] re-scope

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-06
- **Source-session:** unattended night batch, Claude Code on the web; branch `claude/night-batch-2026-08-06-p59kml`; HEAD `8e2be6a1`
- **Status:** PROPOSAL-ONLY — build-ready briefs, zero build, zero rows born
- **Model:** claude-opus-5 orchestrating; Sonnet-class read-only footprint lanes

Every footprint below was verified against the live tree this session. Where a claim from the
recon packet did **not** reproduce, the correction is stated in place rather than smoothed.
Library verdicts come from `docs/audits/2026-08-06-technical-night-library-research.md`; two of
them were not delivered and say so.

**No rows were born.** These are briefs for the day lane to file and build.

## B1 — GitHub Actions report-only wall

**Intent.** Produce a server-side, tamper-evident record that the suite and `audit.py health`
were run against what actually landed on `main` — an observation organ, with **no required-check
arming** and no branch protection touched.

**Done-when (draft, testable).** A push to `main` produces a workflow run whose job summary
records, for that exact SHA: the `uv` version actually used, the `pytest` counts
(passed/failed/skipped) and its exit code, the `audit.py health` verdict line and its exit code,
and the JOURNAL-anchor backstop's verdict — and the job **succeeds regardless of those exit
codes**. Verified by one deliberate red-making push showing the run green with the red recorded
in its summary. No required check is configured; `git push` behaviour is unchanged.

**Expected footprint.**
- `.github/workflows/report-only-wall.yml` — **NEW · PENDING-OPERATOR-PATH-APPROVAL.** The
  directory is absent at HEAD, but it is **not virgin ground**: `ARCHITECTURE.md:748-749`
  records that `.github/` existed and was deleted at `82227f08`, retiring
  `nightly-conformance-triage.yml` under `[#255]`, "because a PR-triggered organ under a
  local-merge workflow was vacuous — it never fired." Re-creating the directory is the operator
  path decision.
- `ARCHITECTURE.md` Ch2 organ row + Ch6 mesh row — **required in the same commit** (see the
  R-A red-team in the window review: the Layer enum at `:193-196` has no server-side value, so
  this is a model change, not a row addition).
- Nothing else. No `scripts/`, no `pyproject.toml`, no `.pre-commit-config.yaml`.

**Six hard requirements, each earned empirically in this container.** These are the difference
between a wall that means something and a third `ARMED (tells-you-nothing)` organ.

1. **`on: push`, not `pull_request`.** The repo merges locally with `--no-ff` and pushes; a
   PR-triggered organ never fires. This is exactly what killed the predecessor.
2. **`fetch-depth: 0`.** A shallow checkout makes `audit.py health` produce **three classes of
   false finding**, proven here: `canonical_freshness` returned 5 false FAILs (the graft root
   `27c82d4` appears to add whole files — `git show --numstat 27c82d4 -- CONTRIBUTING.md` →
   `219 0`, so the stamp is compared against the graft date); `no_ff_merges` false-WARNed on a
   real 2-parent merge whose parents were truncated; and `journal_spine_anchor` raised a
   FAIL-class `AnchorError` ("disposition floor `24882f8cc` is not an ancestor of main") because
   the ancestry path is cut. Without this line the wall reports garbage, in FAIL class.
3. **Pin `uv` to exactly `0.11.19`.** `pyproject.toml:25` sets
   `required-version = "==0.11.19"` (ADR-106), and **every** hook `entry:` in
   `.pre-commit-config.yaml` is wrapped in `uv run --locked`. A runner with any other `uv`
   fails every step on a version-mismatch error before a single real check runs — witnessed
   here with 0.8.17.
4. **`uv sync --locked --group analytics`.** The `dev` group alone leaves `pandas` uninstalled
   and **21 `test_fleet_analytics.py` tests fail** on the missing module. Measured: 22 failures
   in that file with `dev` only, 1 after adding the group.
5. **Expect a non-zero suite exit, and do not treat it as breakage.** The `[#457]` leg-(ii)
   test is a by-design RED (`tests/test_audit.py:2296` — asserts "1 declared routine row"
   against a live "2 declared routine row(s)"), so `pytest` exits 1 legitimately.
   `audit.py health` likewise exits 1 whenever any WARN-or-worse exists, which is today's
   normal state. **A wall that goes red on both from day one is a wall the operator learns to
   ignore** — the exact pathology `ARCHITECTURE.md:214` warns about. Hence: record, do not judge.
6. **Decide the Pyright shape.** The suite is not green on a **PATH-only Pyright** environment
   — which is what a CI runner is. `ARCHITECTURE.md:477-479` models only two shapes (vendored →
   8/8; unprovisioned → 7/8 with 1 skip); a runner with `pyright-langserver` on PATH and no
   `node_modules/pyright` is a third, and it produces 7 failures, one of which is a test
   asserting on ambient PATH state (`tests/test_reverse_dep_oracle.py:130`). Either vendor
   Pyright in the workflow, or record these 7 as expected.

**Draft workflow YAML — ready to place once the path is approved.**

```yaml
# .github/workflows/report-only-wall.yml
# REPORT-ONLY observation organ. Records; never blocks. No required check is armed by this
# file -- arming one is a separate, ADR-owing decision (see the R-A red-team).
# Trigger is `push`, not `pull_request`: the repo merges locally with --no-ff and pushes, so a
# PR-triggered organ would never fire -- the [#255] vacuity that retired the last .github/ organ.
name: report-only wall

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read          # least privilege; no issues:write -- this organ records, it does not emit

concurrency:
  group: report-only-wall-${{ github.ref }}
  cancel-in-progress: false   # every landed SHA gets its own record; never cancel a record

jobs:
  record:
    runs-on: ubuntu-latest
    timeout-minutes: 45       # serial suite is ~9m42s on the operator host, 13m19s observed in a container
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0      # REQUIRED: a shallow clone makes canonical_freshness,
                              # no_ff_merges and journal_spine_anchor report false findings

      - name: Install the pinned uv
        uses: astral-sh/setup-uv@v5
        with:
          version: "0.11.19"  # MUST equal pyproject.toml [tool.uv] required-version exactly
          python-version-file: ".python-version"

      - name: Assert the toolchain pin is satisfied
        run: |
          uv --version
          grep -q 'required-version = "==0.11.19"' pyproject.toml \
            || { echo "::error::pyproject uv pin moved -- update this workflow in the same commit"; exit 1; }

      - name: Sync the locked environment
        run: uv sync --locked --group analytics   # analytics group or 21 fleet_analytics tests fail

      - name: pytest (recorded, never blocking)
        id: pytest
        continue-on-error: true
        run: |
          set +e
          uv run --locked pytest -q --tb=line 2>&1 | tee pytest.out
          echo "exit=${PIPESTATUS[0]}" >> "$GITHUB_OUTPUT"

      - name: audit.py health (recorded, never blocking)
        id: audit
        continue-on-error: true
        run: |
          set +e
          uv run --locked python scripts/audit.py health 2>&1 | tee audit.out
          echo "exit=${PIPESTATUS[0]}" >> "$GITHUB_OUTPUT"

      - name: JOURNAL-anchor backstop (recorded, never blocking)
        id: anchor
        continue-on-error: true
        run: |
          set +e
          # The pre-push organ takes the push protocol on stdin:
          #   <local_ref> <local_sha> <remote_ref> <remote_sha>
          # github.event.before is the pre-push tip of main, which is exactly remote_sha.
          echo "refs/heads/main ${{ github.sha }} refs/heads/main ${{ github.event.before }}" \
            | uv run --locked python scripts/block_unanchored_push.py 2>&1 | tee anchor.out
          echo "exit=${PIPESTATUS[0]}" >> "$GITHUB_OUTPUT"

      - name: Write the tamper-evident record
        if: always()
        run: |
          {
            echo "## report-only wall — \`${{ github.sha }}\`"
            echo
            echo "| leg | exit | verdict |"
            echo "|---|---|---|"
            echo "| pytest | ${{ steps.pytest.outputs.exit }} | \`$(tail -1 pytest.out)\` |"
            echo "| audit.py health | ${{ steps.audit.outputs.exit }} | \`$(grep -E '^health:' audit.out || echo n/a)\` |"
            echo "| journal anchor | ${{ steps.anchor.outputs.exit }} | \`$(tail -1 anchor.out)\` |"
            echo
            echo "uv: \`$(uv --version)\`"
            echo
            echo "> Report-only. Non-zero legs are recorded, not enforced. A non-zero pytest is"
            echo "> EXPECTED while the [#457] leg-(ii) test is by-design RED; a non-zero"
            echo "> audit.py health is expected whenever any WARN exists."
          } >> "$GITHUB_STEP_SUMMARY"

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: wall-record-${{ github.sha }}
          path: |
            pytest.out
            audit.out
            anchor.out
          retention-days: 90
```

**Dependency edges.** Coupled to `#24-P2` (cron + dead-man's switch) and inherited by
`#25-W-4` (reusable fleet workflow). Behind the NC-A5 unverified-premise brake for the *gate*
variant; the report-only variant is the exempted "different deliverable"
(`STANDING_RULINGS.md:198-200`).

**Test approach.** No unit tests — the artifact is a workflow. Verification is one deliberate
red-making push (the wall must stay green with the red recorded), plus a `workflow_dispatch`
run to confirm the pin assertion fires when `pyproject.toml`'s pin moves.

**Risk register.**
| risk | mitigation |
|---|---|
| The workflow silently stops firing (schedule/inactivity/plan change) and the green badge means nothing | Requirement 5's honest summary text; `#24-P2`'s watchdog is the real answer, and it shares the failure mode (research item 6c) |
| Permanent red trains the operator to ignore it | `continue-on-error` + the always-green record job |
| A shallow default checkout reintroduces the 3 false-finding classes | `fetch-depth: 0`, asserted in review |
| The `uv` pin drifts and the wall goes vacuous | The explicit pin-assertion step fails loudly |
| Private-repo required-checks need a paid tier | Out of scope: report-only arms nothing |

**Library verdict.** N/A — GitHub-native by construction. Related: research item 6 confirms
`schedule:` may **drop** queued runs, that scheduled runs fire only on the default branch, and
that the documented 60-day auto-disable is stated for **public** repos only — private-repo
applicability is genuinely unresolved and matters for `#24-P2`.

**Size:** M. **Lane:** sole owner of `.github/workflows/` — see §Lane routing.

## B2 — mutation-testing evaluation

**Intent.** Measure whether the enforcement organs' tests actually detect broken behaviour, using
a known-vacuous test as the calibration case.

**Done-when (draft).** A mutation run scoped to the four enforcement modules completes inside a
declared time budget, and its report is recorded as an audit artifact with an explicit
ADOPT/DROP verdict; the pilot's calibration case (below) is either killed by an improved
assertion or recorded as a surviving mutant with a reason.

**Expected footprint.** `pyproject.toml` (NEW dev-dep + tool config — `mutmut` appears nowhere
today, grepped); `tests/test_fleet_analytics.py:144-146`; a new
`docs/audits/2026-08-06-*-mutation-pilot.md`. Subjects (read, not edited): `scripts/audit.py`,
`scripts/validate_backlog.py`, `scripts/enforcement_coverage.py`,
`scripts/canonical_freshness_gate.py` — all four have dedicated test files.

**The pilot's live evidence case, verified.** `tests/test_fleet_analytics.py:144-146`:

```python
def test_canonical_path_survives_a_cycle():
    alias = {"a": "b", "b": "a"}
    assert fa.canonical_path("a", alias) in {"a", "b"}  # terminates, does not hang
```

Against `canonical_path` (`scripts/fleet_analytics.py:341-351`), the call returns `"b"`
deterministically — it is a `.get()` chase, not dict iteration. The assertion passes for
**either** member of the cycle, so it cannot catch a regression that flips which one is
returned. Crash-safety landed; correctness did not. The correctness assertion is
`== "b"`. This is the ideal mutation-testing calibration case: a mutant that changes *which*
node is returned survives today and must be killed after.

**Correction to the recon packet:** it referenced "9 test files" for the enforcement organs. No
registry of nine exists. The closest formal registry, `scripts/enforcement_coverage.py:791-797`
(`TIER1_ORGANS`), names **five** organs: `block_unanchored_push`, `canonical_freshness`,
`reconciled_versions`, `doc_claims`, `git_backlog_drift`. The four named subject modules each
have a test file; the "9" figure is unsupported.

**Dependency edges.** None hard. Shares `pyproject.toml` with `#25-W-2` / `#25-W-5` / `#25-W-6`
— a real collision for lane routing.

**Test approach.** The tool is the test. Guard rails: a declared scope (four modules, not the
tree) and a declared wall-clock budget; the 2228-test suite makes an unscoped run impractical.

**Risk register.** Runtime blow-up on an unscoped run (mitigation: module scoping is a
precondition, not an optimization); a flood of low-value surviving mutants (mitigation: the
verdict is about the four organs, not a global score); `uv`-under-mutation interaction unknown
(see the library gap).

**LIBRARY VERDICT: NOT DELIVERED.** The research lane for mutmut vs cosmic-ray did not return.
Four questions decide adoption and none is answered: current maintenance state of both tools;
`uv`-with-locked-env compatibility; Windows behaviour (mutmut historically had problems);
and — decisive — whether runs can be **scoped to selected modules with cached incremental
re-runs**. Do not start B2 until these are answered; the brief is otherwise complete.

**Size:** M. **Lane:** owns `pyproject.toml` in its batch.

## B3 — prose-lint (vale) evaluation

**Intent.** Test whether an off-the-shelf prose linter can absorb part of the silent-rule
ratchet and the `doc_claims` overlap.

**Done-when (draft).** A recorded verdict on one decisive question — can vale express a
**corpus-wide numeric ceiling** (441 across 57 files) or only per-file/per-scope counts — with a
working config if yes, and a named "cannot express" if no.

**Expected footprint.** NEW `.vale.ini` + a styles directory; `.pre-commit-config.yaml` (a new
hook entry); reads `ecosystem/*.yaml` (9 files), `scripts/silent_rule_detector.py`,
`scripts/validate_doc_claims.py`. Deliberately **not** `pyproject.toml` — vale is a Go binary,
so keeping it on the pre-commit mirror leaves `pyproject.toml` free for B2 and the lanes stay
disjoint.

**Dependency edges.** Shares its target surface with `#25-W-6` (schema-as-code over the same 9
`ecosystem/*.yaml`). Both trace to one **unfiled** tension that has no BACKLOG id at all — it
exists only as a frontier item in the 2026-08-05 bundle's `RESIDUAL.md`. Worth surfacing: two
candidate births currently point at a parent that was never filed.

**Test approach.** Adopt-or-refute against the live 441 measurement: any vale config claiming to
cover the ratchet must reproduce 441 over the same 57-file scope, or state precisely which part
it cannot count. The live number is confirmed
(`detector: silent-rule-v4 / files: 57 / count: 441`, baseline 441).

**Risk register.** Highest risk is a **partial** adoption that appears to cover the ratchet but
counts per-file, silently lowering enforcement — the "fails-toward-silence" class the register
already names at A5. Mitigation: the done-when is the corpus-wide question, not "vale runs."

**LIBRARY VERDICT: NOT DELIVERED** — same lane. One relevant fact did surface from the item-3
research and is recorded: **no Vale plugin does code-reference staleness**, so the `doc_claims`
overlap vale could plausibly cover is the *prose* half only, never the claims-vs-code half.

**Size:** M. **Lane:** owns `.pre-commit-config.yaml` + `.vale.ini` in its batch.

## B4 — doc-currency S-row

**Intent.** Reconcile the documents that describe retired enforcement models as live.

**Done-when (draft).** Each of the eight sites below either carries corrected text or a recorded
deferred-with-reason; `CONTRIBUTING.md`'s `last_reviewed` is re-stamped only after a genuine
end-to-end re-read (per the §4 freshness cadence, which means re-read and confirmed, not touched).

**Expected footprint — verified live. Scope is CONTRIBUTING ×6, not ×5.**

| # | site | what is wrong |
|---|---|---|
| 1 | `CONTRIBUTING.md:215-219` | "enforced **mechanically and deterministically** by the session-end Stop-hook … the only escape is `/override [reason]`" — retired by ADR-85 §A2/§A5 |
| 2 | `CONTRIBUTING.md:118` | "Hub-only, **fail-soft**" for `block-ff-push`; actual is fail-CLOSED (`block_ff_push.py:210-213`, `return 2` at `:240`; `.pre-commit-config.yaml:160-162` agrees with the code) |
| 3 | `CONTRIBUTING.md:96-119` | hook table has 15 rows; `check-seal-identity` and `block-unanchored-push` are both absent |
| 4 | `CONTRIBUTING.md:193-197` | ADR-82/88/89 described as frozen `Proposed`; all three flipped to **Accepted on 2026-08-04** (`ADR-82:3`, `ADR-88:5`, `ADR-89:5`) |
| 5 | `CONTRIBUTING.md:14-27` | branch-naming lists only `feat/ fix/ docs/ chore/` and says "these four only"; the three machine-lane prefixes (`worktree-<name>`, `epic/<slug>`, `claude/<slug>`) are absent |
| 6 | `CONTRIBUTING.md:128-156` | **NEW, sixth leg** — §"Nightly outcome management" describes the **deleted** Action in the present tense. `ARCHITECTURE.md:788-792` already flags it and declares reconciling it out of scope, so this is a known-unreconciled item |
| 7 | `protocols/DEFINITION_OF_DONE.md:141-149` | §Override: "A blocked turn exits **only** via `/override [reason]`" — both clauses dead |
| 8 | `.claude/commands/override.md:6-9` | the Stop-hook "**hard-blocks**" and `/override` is "the **only** exit" |

**The mechanism finding, corrected.** `DEFINITION_OF_DONE.md` is **not in the gated set**:
`canonical_freshness_gate.py:32-33` lists `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`,
`CONTRIBUTING.md`, `docs/handoffs/README.md`, `protocols/ESSENTIALS.md`, and `audit.py:266` adds
only `protocols/SESSION_SETUP.md` and `protocols/AI_COUNCIL_PROCESS.md`. So it carries a
`last_reviewed: 2026-06-19` stamp that **no check ever reads** — 45+ days stale with zero
mechanical pressure, describing a retired model. That is the sharpest single finding in B4.

`CONTRIBUTING.md` **is** gated, and the packet's "reads fresh, so world-moved-past-it drift is
structurally invisible" framing needs one correction: the *predicate limit* is real and
documented in the code itself (`audit.py:837-840` — it "does NOT verify content against
external decisions"), so leg 4 (the ADR flips) is genuinely invisible to it. But the specific
"reads fresh" observation could not be reproduced here, because this container's shallow clone
makes every file look last-edited at the graft date. Treat the predicate limit as confirmed and
the freshness *state* as unverified from this container.

**Dependency edges.** Same fail-soft-vs-fail-closed **class** as B5, at different sites — the
two should cite each other so a reader does not fix one and assume the class is closed.
`#24-P5`/`#497` part (b) touch the same fact in `.pre-commit-hooks.yaml`.

**Test approach.** Documentation-only, so the honest test is a **regen-and-diff or claim check**,
not a unit test: extend `doc_claims` (or add a targeted check) so the hook-table row count and
each named hook's posture are machine-derived from `.pre-commit-config.yaml`. Without that, B4
fixes eight sites and buys no protection against the ninth. Note `doc_claims` currently checks
only **3** self-claims live, so the mechanism is thin today.

**Risk register.** Re-stamping `last_reviewed` without a genuine re-read (mitigation: the
cadence rule is explicit that the stamp means re-read); fixing prose while the generating
mechanism stays unguarded (mitigation: the claim-check leg above).

**Library verdict.** N/A — in-repo doc work. Adjacent: **lychee is an ADOPT-candidate** for the
neighbouring rot class (local links + renamed-heading anchors via `--include-fragments`) but
cannot check a `file.py:123` locator — that is `/preflight`'s job.

**Size:** S. **Lane:** owns `CONTRIBUTING.md`, `protocols/DEFINITION_OF_DONE.md`,
`.claude/commands/override.md`.

## B5 — `block_ff_push.py:39` docstring defect

**Intent.** Make the canonical implementation file stop contradicting itself on the exact point
the ADR-85 amendment changed.

**Done-when (draft).** `scripts/block_ff_push.py`'s module docstring states the fail-CLOSED
posture, and a test pins the posture so the docstring and behaviour cannot diverge again.

**Expected footprint (verified).**
- `scripts/block_ff_push.py:39` — "Fail-soft: any git error → return 0 (never wedge a legitimate
  push)", contradicting `main()`'s own docstring at `:210-213` ("Exit codes: … `2` = internal
  error, refuse. Fail **CLOSED** on error per the ADR-85 amendment 2026-08-03 §A6") and the
  actual `return 2` at `:240`.
- `ARCHITECTURE.md:327` — U-1, the *same* stale claim ("fail-soft to exit 0 on any git error").
  `[#497]` owns this posture at two **other** sites (`carrier_mesh.py:75`,
  `.pre-commit-hooks.yaml`) but its Done-when does not name `ARCHITECTURE.md:327`. Folding U-1
  in here is cheap and closes a third unfiled site of one class.
- `tests/test_block_ff_push.py` — the pinning test.

**Precision note that keeps the fix honest.** Lines `:153` and `:169` describe two small pure
helpers (`_rev_parse`, `_reconstruct_main_range`) as fail-soft and are **correct** — do not
"fix" them. Line `:190` already states the split explicitly ("THE DELEGATE IS FAIL-SOFT AND
THIS GATE IS NOT"), which makes `:39`'s unqualified claim doubly wrong and gives the corrected
wording a model to follow.

**Dependency edges.** Same class as B4. Adjacent to `[#497]`.

**Test approach.** RED-first: a test asserting `main()` returns 2 on a forced internal error,
plus a docstring-posture assertion (the repo already uses this pattern — the twin-parity test
pins regexes across two files, so pinning a posture string is idiomatic here).

**Risk register.** Low. The one real risk is a docstring-only fix with no test, which leaves the
next amendment free to re-diverge.

**This is code-impact**, so a terra review artifact is owed in the day lane —
`review_artifact_coverage` is live and currently clean ("0 code-impact merge(s) since 2026-08-05
each carry a linked review artifact with a parseable tally"), so an unreviewed code merge will
show up.

**Library verdict.** N/A. **Size:** S. **Lane:** owns `scripts/block_ff_push.py`,
`ARCHITECTURE.md`, `tests/test_block_ff_push.py`.

## [#487] re-scope — pipeline-repair-first

**Intent.** Repair the closure-proposal pipeline's *detection* and *confirm* path before asking
anyone to adjudicate its output.

**Three corrections to the re-scope premise, from live code.** Each changes what the spec asks
for, so they come first.

1. **"Frozen `since_commit`" is the wrong diagnosis.** `resolve_window()`
   (`scripts/propose_closures.py:329-361`) is a deliberate fail-safe: a file is pending iff
   `unchecked & open_ids` is non-empty (`:348`), and it then re-covers from the **earliest**
   pending file — "files are date-sorted, so pending[0] is the earliest -> widest safe window"
   (`:350-351`). It refuses to advance past unreviewed proposals. The real defect is sharper:
   **one ancient unresolved WEAK id pins the baseline for everything, including STRONG
   detection.** So the repair is *separating the STRONG and WEAK baselines*, not "unfreezing a
   counter" — which would discard unreviewed candidates.
2. **The confirm action is not merely unexercised — the checkbox path does not exist.**
   `render()` emits `- [ ]` unconditionally (`:226`, `:241`), and a grep across `scripts/`, the
   plugin scripts and the plugin commands finds **no writer of `- [x]` anywhere**. The only real
   confirm signal is BACKLOG-row removal. So "exercise the confirm action end-to-end" needs
   splitting: either implement the checkbox flip, or delete the checkbox framing and document
   row-removal as the confirm. The CLI it *does* have is real and wired
   (`scripts/review_closures.py:277-292`, `plan --ids`, documented at
   `plugins/tier1-lifecycle/commands/review-closures.md:43`).
3. **The addendum's line-anchoring premise does not apply here.** Proposal evidence is already
   **content-anchored**: `` `{sha[:9]} {subj}` `` for STRONG (`:225-228`) and
   `` `{path}` changed in `{sha[:9]}` `` for WEAK (`:240-243`) — no bare line numbers anywhere,
   and `review_closures.plan_closures` uses the **raw BACKLOG row text** as its `Edit`
   `old_string` (`:175`, `:213-217`). The [#359] locator-rot mode is real in the repo but not in
   this pipeline. One soft spot remains: the displayed task summary is re-read live
   (`:172-174`), so an old unresolved file can show stale *wording* while its id and SHA still
   anchor correctly — cosmetic.

**Done-when (draft, three legs).**
(i) The STRONG detector recognizes the `[#432]` class, proven by a test over that arc's real
commit shapes. (ii) The confirm path is exercised end-to-end by a subprocess-level test that
invokes the CLI exactly as the command file instructs. (iii) STRONG detection advances
independently of unresolved WEAK proposals, proven by a test where an ancient pending WEAK id
does not suppress a new STRONG find.

**Repair surface (verified, file:line).**

| concern | site | current | change |
|---|---|---|---|
| regex bug | `propose_closures.py:51` | `fixes?` matches `fixe`/`fixes`, **never** bare `fix` | `fix(?:es)?` |
| missing verbs | same line | no `resolves`/`resolved`; no colon form (`Closes: #N`); no bare `[#N]` in a merge subject | add `resolves?`/`resolved`; bare-bracket needs a **new lower-confidence tier**, not a `CLOSES_RE` edit — unguarded `[#N]` is the false-positive class `_STRIP_RES` (`:63-70`) already fights |
| twin parity | `tests/test_propose_closures_twin_parity.py:31` (`_TWIN_REGEXES = ("CLOSES_RE",)`) | hub and plugin copies byte-pinned | any regex fix is two-file by construction; the parity test is the gate and already exists |
| window pinning | `propose_closures.py:348-353` + plugin twin `:369-374` | oldest pending file anchors everything | separate STRONG/WEAK baselines |
| no `- [x]` writer | whole file, both copies | `render()` only emits `- [ ]` | implement the flip or drop the framing |
| baseline unresolvable in CI | `:352`, `:359` (`git_valid_rev` guard) | falls back to full-history re-scan | store something durable (a date or reachable ref) — proven necessary: a shallow CI clone cannot resolve a pre-horizon SHA |
| confirm path untested | `review_closures.py:257-274`, `:277-292` | `tests/test_review_closures.py` calls `plan_closures()` directly, never the CLI | subprocess test with `CLAUDE_PROJECT_DIR` set |
| no twin-parity test for `review_closures` | `plugins/.../review_closures.py` vs `scripts/review_closures.py` | copies currently agree outside `_host_root()`; nothing pins it | add a mirror of the propose twin-parity test |

**Evidence base, honestly bounded.** `logs/PROPOSALS-*.md` **does not exist in this container**
(`ls logs/` → `TOKEN-LOG.md` only; gitignored at `.gitignore:26`; the repo itself says the
accumulation "exists only on the operator's machine",
`docs/audits/2026-08-04-technical-closure-proposal-ranked-sheet.md:35-36`). So 149/62/`3c5e476ba`
are unverified here. Corroboration from git-tracked sources instead: `#277` (`BACKLOG.md:68`) —
"the 2026-07-07 /review-closures run proposed 49 items, **0 valid**"; the 2026-07-29 triage —
132 WEAK, **0 closable**; `#487`'s own row — 139 parked, **0 verdicts**. Direction and magnitude
corroborated; exact figures not.

**Risk register.** Widening `CLOSES_RE` raises false positives (mitigation: bare-bracket goes in
a separate tier, never into `CLOSES_RE`); separating baselines could surface a backlog of STRONG
finds at once (mitigation: expected and desirable — but announce it); the hardcoded Windows
marketplace path in `.claude/settings.json` means the Stop hook's liveness is
environment-dependent, so a "repaired" pipeline may still not fire on some hosts.

**Library verdict.** N/A — bespoke. **Size:** L. **Not proposed for the first V-1 batch**: it
touches two script copies plus tests and needs its own arc.

## Lane routing for the first V-1 batch

Footprint-disjoint, verified against the live tree. Five lanes, two of them blocked.

```
lane  item  owns (exclusive)                                       status
----  ----  -----------------------------------------------------  ---------------------------
A     B1    .github/workflows/ + ARCHITECTURE.md Ch2/Ch6 rows       BLOCKED: path approval
B     B4    CONTRIBUTING.md, protocols/DEFINITION_OF_DONE.md,       READY
            .claude/commands/override.md
C     B5    scripts/block_ff_push.py, tests/test_block_ff_push.py,  READY (code-impact:
            ARCHITECTURE.md:327 (U-1)                               terra review owed)
D     B2    pyproject.toml, tests/test_fleet_analytics.py           BLOCKED: library verdict
E     B3    .pre-commit-config.yaml, .vale.ini, styles/             BLOCKED: library verdict
```

**One collision inside this batch, and it is resolvable.** Lanes A and C both touch
`ARCHITECTURE.md` — A adds Ch2/Ch6 rows, C fixes the stale `:327` claim. Since A is blocked on
path approval, the clean sequencing is **C first, A after**; if both are authorized together,
`ARCHITECTURE.md` belongs to exactly one lane and the other files a follow-up. Do not run them
concurrently on that file.

**B1 is the sole `.github/workflows/` owner.** The recon packet showed four candidates
converging on that one absent directory (`#24-P1-gate`, `#24-P1-report-only`, `#24-P2`,
`#25-W-4`). Only the report-only variant is authorized-shaped today, and it takes the directory.

**Hazard flagged: `#25-W-9(a)`.** The proposed root `AGENTS.md` collides with an existing,
**different** artifact: `codex/AGENTS.md` (3891 bytes) is Codex-CLI reviewer config — its own
header reads "# AGENTS.md — Global Codex Reviewer Configuration … **Canonical source** for
`~/.codex/AGENTS.md`", with a "Role: Review Only / Codex MUST NOT modify any file" section. Root
`AGENTS.md` does not exist. Two files with the same basename and unrelated purposes is a
name-collision trap; W-9(a) should either pick a different filename or state explicitly how the
two coexist. Not in this batch, but it is the kind of thing that gets discovered mid-build.

**Cross-lane note on B4/B5.** They fix the same fail-soft-vs-fail-closed class at different
sites. Whichever lands first should name the other, so the class does not read as closed when
half of it is.
