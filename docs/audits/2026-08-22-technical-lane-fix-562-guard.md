# LANE-FIX-562-GUARD — the two confirmed Criticals on the held cloud-1 branch, repaired

**Date:** 2026-08-22
**Lane:** `lane-fix-562-guard` · branch `worktree-lane-fix-562-guard` · repo `.dev-knowledge`
**Brief:** `LANE-FIX-562-guard.md` (frozen contract of record)
**Held branch merged:** `origin/claude/cloud-1-562-admission-rerun` at `7c646699`, `--no-ff`, unmodified
**Terra:** `gpt-5.6-terra` (pinned), twelve passes, `docs/audits/2026-08-22-codex-562-guard-fix-terra*.md`
**Status:** both contract Criticals fixed; terra Critical/High at **0**; pytest green

---

## 1. What the architect ruled, and what this lane did with it

The ruling was **fix on-branch, containment model stands, no re-scope**: the design is
sound and the implementation lacked provenance checks. That held. Nothing about the two
guard layers, the canary set, the redaction rules or the probe's shape was redesigned. What
changed is that the operations which can destroy or execute now prove what they are acting
on first.

The held branch was merged into this lane `--no-ff` and **unmodified**, so every
before/after below is a real diff rather than a description of one. The one merge conflict
was `docs/audits/README.md`, a generated index, resolved by regeneration.

---

## 2. Critical 1 — teardown provenance

### Before

`scripts/nopack_sandbox.py` at `7c646699`:

```python
def teardown(sandbox: Sandbox | Path) -> bool:
    """Remove a sandbox and VERIFY the removal (CLAUDE.md section 5 rule 9, no leftovers)."""
    path = sandbox.path if isinstance(sandbox, Sandbox) else Path(sandbox)
    if path.exists():
        shutil.rmtree(path)
    return not path.exists()
```

Reachable straight from the CLI's `--sandbox`. A typo, or a path pointing at a real
checkout or a synced directory, destroyed it. This is the hazard class this fleet's own P0
exclusion rules exist for — the recorded history is cleanup scripts that deleted personal
files alongside their intended targets — which is why the review held the lane rather than
filing it forward.

### After

Both checks, never either, as the Done-contract requires:

1. **Containment.** The RESOLVED path — symlinks followed *first*, which is the leg that
   stops `<root>/link -> /real/checkout` from looking contained — must be a strict
   descendant of the configured sandbox root (`--sandbox-root`, else
   `$NOPACK_SANDBOX_ROOT`, else `<tempdir>/nopack-sandboxes`). `provision` enforces the
   same boundary, so what could never have been provisioned cannot later be presented for
   deletion.
2. **Provenance.** The path must carry `.git/nopack/marker.json`, written by provisioning
   with a 128-bit per-run nonce whose `sandbox` field names that same resolved path, AND
   have a matching entry in `<root>/.nopack-registry.json` — a file that lives beside the
   sandboxes rather than inside one, and that teardown never deletes. The marker alone was
   forgeable by anyone who could write in the tree they wanted deleted; the pair means a
   forger has to reach outside it, into this tool's own records.

The marker and the identity of the directory are re-verified immediately before the
`rmtree`, and the refusal raises `TeardownRefused` with the CLI exiting 126 having deleted
nothing. This is the one refusal in the tool that is deliberately **not** neutral: the
alternative to a legible refusal is an operator reaching for `rm -rf` by hand.

### Live evidence

```
--- teardown on an arbitrary path OUTSIDE the root:
sandbox guard: teardown refused: ...\victim-checkout is outside the configured sandbox root ...\nopack-root
rc=126
    victim intact: precious work
--- teardown on a marker-less dir INSIDE the root:
sandbox guard: teardown refused: ...\nopack-root\markerless carries no valid provisioning
marker (.git/nopack/marker.json); this tool did not provision it
rc=126
    intact: also precious
--- teardown on the provisioned sandbox:
removed and verified
rc=0
```

Tests, including the four the contract names: arbitrary path refuses; a marker-less
directory inside the root refuses (using the fixture's *real git repo*, i.e. the actual
typo case); a provisioned sandbox succeeds; a symlink does not escape. Plus marker
laundering, nonce mismatch, provision-side containment, and registry disagreement.

### Also fixed here

* **Critical 2 of the review** — provisioning wrote `<dest parent>/sandbox-manifest.json`
  unconditionally, destroying any unrelated file at that path. The manifest lives inside
  the sandbox at `.git/nopack/manifest.json` now, written with exclusive-create `x` mode.
  `.git/` is the right home for three separate reasons: our own clone made it, `scan_tree`
  skips it so the manifest's list of stripped paths cannot fail provisioning's own
  postcondition, and `git status` never surfaces it so the lane still sees a clean tree.
* **High 1** — a post-clone failure left the FULL unstripped clone at `dest`: a
  no-leftovers violation *and* the answer key readable on disk. Every path after the clone
  now removes and verifies. A destination that has *vanished* is reported as an ANOMALY
  rather than a clean abort, because the clone was created, so an empty path means
  something moved it and the unstripped tree survives under a name we do not know.
* `shutil.rmtree` raised `PermissionError` on every sandbox this tool provisioned on
  Windows, because git marks `.git/objects` read-only — a no-leftovers organ that could not
  remove its own leftovers.

---

## 3. Critical 2 — kill the shell

### Before

`run_guarded` screened top-level shell **segments** with an allowlist and then executed
with `shell=True` (line ~726):

```python
    trip = screen_command(command, names)
    if trip is not None:
        return GuardedResult(command, REFUSAL_EXIT, "", REFUSAL_TEXT, refused=True, trip=trip)

    proc = subprocess.run(
        command,
        shell=True,
        ...
```

So `cat $(touch file)` ran `touch` — a command the allowlist had never seen and would have
refused. Screening harder cannot fix that: the gap is between the string that was checked
and the string the shell re-interprets.

### After

There is no shell. `parse_pipeline` lexes a command into literal argv, splits it on `|`,
and every stage runs with `shell=False` from an argv that was itself screened. One parse,
one screen, and the argv that was screened is the argv that executes.

```
$ nopack_sandbox.py exec --sandbox <box> --json -- "cat \$(touch PWNED)"
rc=1 refused=False
stderr: /usr/bin/cat: '$(touch': No such file or directory
        /usr/bin/cat: 'PWNED)': No such file or directory
RESULT: no file created by the substitution
```

Command substitution, backticks and `$VAR` are not screened for; they have **no meaning**,
which is a stronger claim than refusing them. An AST assertion holds `shell=True` out of
the module, and a runtime spy asserts every executed `args` is a list with `shell=False`.

### The capability this costs — reported, per the contract's "STOP and report which"

Shell **loops, conditionals and `;`/`&&`/`||` chains are refused, not interpreted.** This
file's own comments recorded that C1-K2 and C1-K3 adjudicate with `for s in ...; do git log
-1 $s; done`, and an earlier test asserted those were allowed. They are not, and cannot be:
interpreting a loop requires a shell.

The contract says to STOP if any call genuinely requires a shell feature. **No call in the
delivered code does.** The shell features its own call sites use are pipelines, globs and
quoting, and all three are implemented in-process without a shell. The loop shapes are
candidate-issued convenience, and `exec` runs exactly one command per call, so a transport
can issue three. What is lost is batching, not the reachability of any item. That is why
this proceeded rather than stopping, and it is stated here rather than left to be
discovered.

### Deleted, and flagged because deletion is not a thing to do quietly

`_segments`, `_command_tokens`, `_argv0`, `_SEGMENT_SPLIT`, `_REDIRECT`,
`_CONSTRUCT_HEADS`, `_CONSTRUCT_PREFIXES` — the segment-splitting screen this change was
told to replace. Leaving them would read as live screening of a shell that no longer
exists, which is the misreading the finding is made of. They remain in git at `0b6f4943^`.

---

## 4. Terra re-pass — twelve rounds to zero

Run on the full lane diff (`main..worktree-lane-fix-562-guard`), model `gpt-5.6-terra`
pinned, after every fix commit.

```
round   artifact                                    C/H/M/L   what it found
r1      2026-08-22-codex-562-guard-fix-terra.md     4/1/0/0   interpreters in the allowlist;
                                                              glob expansion after validation;
                                                              teardown check-to-delete race;
                                                              a forgeable marker
r2      ...-terra-r2.md                             2/1/0/0   git option operands bypass write
                                                              detection; sed w/e commands;
                                                              registry not atomic
r3      ...-terra-r3.md                             3/1/0/0   literal path operands escape;
                                                              compact `sed -eSCRIPT`; git
                                                              helper programs; lock stealing
r4      ...-terra-r4.md                             5/1/0/0   exec accepts an unproven sandbox;
                                                              symlinked operands; grep -f;
                                                              sort write modes; GPG paths;
                                                              vacuous positive controls
r5      ...-terra-r5.md                             2/1/0/0   _load has no provenance check;
                                                              attached option values;
                                                              pipelines hide stage failures
r6      ...-terra-r6.md                             3/0/0/0   short-option arity; symlink-
                                                              following traversal; library
                                                              callers bypass _load
r7      ...-terra-r7.md                             2/0/0/0   ls -LR; PATH/cwd executable
                                                              shadowing
r8      ...-terra-r8.md                             2/0/0/0   bare Path drops the denylist;
                                                              --manifest reads any host file
r9      ...-terra-r9.md                             1/0/0/0   symlinked metadata read
r10     ...-terra-r10.md                            1/0/0/0   boundary inferred from the tree
                                                              being judged
r11     ...-terra-r11.md                            2/0/0/0   filename streams via stdin;
                                                              git symbolic-ref / --edit-description
r12     ...-terra-r12.md                            0/0/0/0   CLEAN PASS
```

**27 Critical and 5 High across the arc, all fixed. Final state 0/0.** Round 12's verdict,
verbatim: *"Clean pass: no remaining Critical or High findings in the requested files."*

**A correction to the record.** The round-5 commit message says round 4 returned "4
Critical". The artifact says **5** — the fifth (`exec` accepting an unproven sandbox path)
scrolled off the console tail this lane was reading from. Nothing was lost: terra re-raised
it as round 5's C1 and it was fixed there. The tally table above is counted from the
artifacts, not from those commit messages.

### What the arc was actually about

The findings moved in a legible direction: from *"the guard does not do the thing"* (r1–r3)
to *"one route into the guard skips a check the other routes make"* (r5–r10) to *"a
specific tool has a mode nobody modelled"* (r11). Every fix landed at the boundary rather
than on the route — `verify_provenance` is shared by `teardown` and `_load`;
`screen_stages` runs pre- and post-expansion; `_require_provisioned` sits at execution
where every caller passes through it.

**Three vacuous checks were found in three consecutive rounds, and they are the lesson.**

1. Refusing `-p` everywhere (a round-4 fix) turned probe vector V5b — `git cat-file -p
   <blob>`, the *only* vector exercising Layer B's content leg on a blob no command names —
   into a Layer A refusal. It still reported PASS. It was testing nothing. `-p` is
   `--paginate` only *before* the subcommand; after it, `git log -p` is a patch.
2. A positive control that named a missing file passed, because "not refused" was the whole
   test. The controls exist precisely to stop a refuse-everything guard passing a
   refusal-only probe — an anti-vacuity device that was itself vacuous.
3. A control whose *upstream* pipeline stage failed passed, because a pipeline reports its
   final status: `cat missing | wc -l` exits 0 with `0`. The default V8 control **is** a
   pipeline, so this was live.

Each was green because its precondition had quietly stopped holding. Each was caught by
looking at what the check *did* — which layer fired, which stage ran — not at the word it
printed. `GuardedResult` now carries `stage_returncodes`; a control must exit zero, produce
output, and have had no stage fail.

### Defects this lane found on its own, outside terra's findings

* **`git stash` with no arguments is `git stash push`** — a write. It was in the
  bare-listing set as a read. Found by hand-checking the table against real git behaviour
  rather than against its own comment.
* **`shlex` cannot answer the question this parser has.** Its POSIX mode strips quotes and
  forgets; its non-POSIX mode tokenizes differently, and pairing the two desynchronises on
  the ordinary `--format='%h %ad'` shape — measured, it turned C1-K2's own command into an
  "unparseable" refusal. Hence a hand-written lexer that returns each word *with its
  unquoted characters*, so `grep -n '>' file` is a read and not a refused redirect.
* **`_option_forms` over-generates on purpose**, which is right for a refusal table (more
  matches means more refusals) and wrong for a semantic decision: it reports `-e` for
  `-fescape`, which made `-fescape` read as a pattern. A refusal table and a semantic
  decision cannot share an over-approximating parser.

---

## 5. What the guard does NOT guarantee

Carried in the module docstring, where a reader meets it, not only here.

* An **accident boundary, not an adversarial-security boundary**. A model that
  deliberately exfiltrates in chunks or base64s defeats Layer B's literal matching. The
  failure mode being prevented is "a model greps and finds", which is the one that
  happened.
* The command allowlist screens argv0 plus a table of known exec/write flags. It is **not a
  proof** that no allowlisted tool has another write mode — sed's `w` command is one it
  cannot see by flag. What contains that is the sandbox being a disposable clone.
* `teardown` re-verifies immediately before deleting, but a check and an `rmtree` are two
  syscalls. **This narrows the race, it does not close it**: closing it needs no-follow
  traversal from a directory descriptor, which Windows does not offer portably. What is
  closed is the failure on record — a wrong path sitting there statically.
* The marker and the registry are both files. Someone who can write to the sandbox root can
  forge both. They raise forgery from "create one file" to "tamper with this tool's own
  records", which is the honest size of the claim.
* `_resolve_executable` trusts the PATH the session started with. If that is hostile, so is
  the machine, and no guard inside one process fixes it.

### Known over-refusals, recorded rather than chased

* `git worktree list` — `list` is an operand and the bare-only rule is uniform. A sandbox
  clone has one worktree.
* A git flag taking a **detached** value appears as an operand and is refused; the
  `--opt=value` spelling is how to pass one.
* `sed` accepts only address/print/substitute scripts; the `;` split is naive, so an exotic
  substitution containing `;` is refused rather than admitted. That is the correct direction
  for a guard to be wrong in.
* An unquoted Windows path cannot name its file at all: `\` is the lexer's escape
  character, so `-fC:\host\secrets` lexes to `-fC:hostsecrets`. "It was refused" and "it
  could never have worked" are different facts; this is the second.

---

## 6. Verification

**Full guard suite: 111 passed, 0 failed** (`tests/test_nopack_sandbox.py`).

Baseline on this host before any change, for comparison: **34 passed, 8 failed, 13 errors**
— the failures were `shutil.rmtree` PermissionError on git's read-only pack files (fixed in
Critical 1's commit) and `test_layer_b_catches_the_history_leg`, whose second leg passed
quotes through to `cmd.exe` literally so the pathspec matched nothing and Layer B's content
leg was never exercised. Proper quote handling made that test do what it always claimed to.

**Live end-to-end against this repo, with the real pack present**, re-run after every fix
commit:

```
provision:  rc=0 · 31 files removed · 34 redacted · postcondition_clean=True
probe:      11/11 vectors as expected
            V1-V6b, V5b refused (V5b on layer B, verified explicitly)
            V7 69 bytes · V8 3 bytes ("87" ADRs) · V9 177 bytes — all rc=0
exec:       cat $(touch PWNED) -> inert, no file created
            ls docs/decisions/ADR-*.md | wc -l -> 87
teardown:   outside root -> 126, nothing deleted
            marker-less inside root -> 126, nothing deleted
            provisioned sandbox -> removed and verified
```

`ruff check` clean throughout. Every fix is its own commit, per the contract.

---

## 7. What this does NOT resolve

Leg 3 of `[#562]` — the actual A/B rerun — remains **BLOCKED on credentials and network**,
exactly as the held lane's own §2 recorded. This lane repaired the guard; it did not run
anything through it and produces no admission verdict. Per the contract, the LOCAL
admission run (LANE-562-local) becomes dispatchable only after the integrator merges this
branch.

The held branch `claude/cloud-1-562-admission-rerun` is **not deleted**. It retires only
after this branch supersedes it at merge, push-before-delete.

---

## AMENDMENT — 2026-08-22, full-suite result and one pre-existing RED

§6 above reported the **guard** suite (111 passed, 0 failed), which was the run available
when this file was written. The **full** suite finished afterwards. Recorded here as an
amendment rather than edited into §6, per CLAUDE.md §5 rule 3.

```
py -m pytest -q -x --tb=short
1 failed, 1561 passed, 2 skipped, 1 xfailed in 741.79s (12:21)
```

The single failure is **`tests/test_enforcement_coverage.py::
test_anchor_gate_probe_distinguishes_installed_from_absent`**, and it is **not this
lane's**. Evidence, in the order it was established:

1. **The lane touches none of its inputs.** `git diff --name-only main...HEAD` is
   `docs/audits/*`, `scripts/nopack_sandbox.py`, `tests/test_nopack_sandbox.py`. The test
   reads `tests/test_enforcement_coverage.py`, `scripts/enforcement_coverage.py`,
   `scripts/block_unanchored_push.py`, `scripts/journal_anchor.py` and the pre-commit
   config — none of them changed here.
2. **It does not probe the live repo.** `_anchor_organ_consumer` builds a synthetic
   consumer in `tmp_path`, so this lane's 15 unanchored commits cannot reach it. That
   matters because the ADR-85 organ is exactly the kind a lane's own spine state normally
   *does* perturb, and here it does not.
3. **It fails identically at bare `main`.** Run at `d9073b71` — the merge base, before the
   first commit of this lane — in a throwaway detached worktree: same test, same
   assertion, same evidence string, 1 failed in 7.79s. The worktree was removed and its
   removal verified (`git worktree list` back to two entries).

Its evidence line: *"pre-push organ REFUSED an anchored push too (exit 1) — it does not
discriminate; a constant refusal enforces nothing"*. So the probe's ANCHORED control is
being refused as well, which collapses the organ's verdict to `absent`. `uv run --locked`
works in this worktree (checked), so it is not the lane's environment; the refusal is
inside the synthetic consumer the probe builds.

**This is filed, not fixed.** It is a defect in the ADR-85 enforcement-coverage probe,
which is outside this lane's contract (`no guard feature growth`, and the contract's scope
is `scripts/nopack_sandbox.py`). It is stated here so the integrator sees a RED that
predates the merge and is not caused by it — and because the failure is itself an instance
of this lane's own recurring theme: **a probe whose control has stopped discriminating
measures nothing**, which is precisely what that test was written to catch.
