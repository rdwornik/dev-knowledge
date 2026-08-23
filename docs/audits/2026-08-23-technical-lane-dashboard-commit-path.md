# LANE L4 — Generated-output commit path + freshness gate (M8 + `[#171]` leg 1)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-23 · **Slug:** `lane-dashboard-commit-path`
- **Lane:** L4, batch of 2026-08-23 · **Worktree:** `worktree-dashboard-commit-path`
- **Merge base:** `aeec0fd1` (`main`, "Merge branch 'chore/phase0-preconditions-2026-08-23'")
- **Governing contract:** `LANE-L4-dashboard-commit-path.md` (REISSUE, 2026-08-23) — frozen,
  immutable to this lane
- **Ruling executed:** **R1 — option (b)**, plus a freshness leg that is not a writer. This lane
  executed the ruling; it did not evaluate it, and found no rule-vs-ruling conflict.

---

## 1. Ground truth (Step 1)

Everything in this section was measured live in the lane worktree at merge base `aeec0fd1`,
before any file in this lane was edited.

### 1.1 The two artifact strings, verbatim

Both are **committed artifact text**, quoted from the tracked files rather than from the
generator that emits them.

`ecosystem/conformance.md:7` —

```
> **Generated, committed, read-only** (ADR-86 location + ADR-80 zone class). It answers four standing operator questions — what finished, where the telemetry is, whether the intakes passed their gate, and whether implemented ADRs are archived — and it **reports rather than repairs**: every VIOLATION and flag below is left exactly where it was found.
```

`ecosystem/conformance.html:45` —

```
<p class="note">Generated, committed, read-only (ADR-86 location + ADR-80 zone class). It reports rather than repairs: every VIOLATION and flag below is left exactly where it was found.</p>
```

Their emitters are `scripts/gen_dashboard.py:931` (`_preamble`) and `scripts/gen_dashboard.py:1175`
(`render_html`).

**A third false claim, in the same family, that the contract's "two strings" does not name.** The
generator's own module docstring, `scripts/gen_dashboard.py:9-11`:

```
LOCATION + ZONE CLASS are ruled, not chosen here: ADR-86 puts the dashboard at
`ecosystem/conformance.md` as an ADR-80 **committed-generated** zone -- a read-only validator
generates it and commits its own output.
```

This is the sentence the Phase-0 packet quotes as *the root* (§Premise B). It is not an artifact
string — it never reaches `ecosystem/` — but it asserts the same non-existent mechanism, to the
next reader of the code rather than the next reader of the dashboard. Corrected in Step 3 and
recorded here so the correction is not mistaken for scope creep.

### 1.2 What runs `gen_dashboard.py` today — **nothing**

Searched every arming surface in the repo (`.pre-commit-config.yaml`, `.claude/settings.json`,
`*.yaml`/`*.yml`/`*.json`/`*.ps1`/`*.py`/`*.md`), excluding the generator, its own outputs, its
test file and prose that merely names it:

```
grep -rn "gen_dashboard" --include=*.yaml --include=*.yml --include=*.json \
     --include=*.md --include=*.ps1 --include=*.py .
grep -rn "dashboard" .pre-commit-config.yaml .claude/settings.json   ->  rc=1 (no match)
```

Every hit is prose (`ARCHITECTURE.md`, `JOURNAL.md`, the handoff bundle) or
`tests/test_gen_dashboard.py`. **No hook, no session hook, no scheduler, no routine, no CI job
invokes it.** Its only non-test caller is a human typing the command.

This is R3 **F5** — `--check` armed nowhere — and the Phase-0 packet is explicit that F5 is a
**different defect** from this lane's (a gating gap, not a writer gap). It is recorded here as
measured ground truth, **not fixed**: arming `--check` is not in this lane's closure contract, and
the ship-gate leg this lane does arm (§5) answers a different question — *is the committed output
current?* — from the one `--check` answers — *does the output byte-match a regeneration?*

### 1.3 Who consumes the output

| Consumer | Site | Nature |
|---|---|---|
| `ARCHITECTURE.md` Ch2 organ map | `ARCHITECTURE.md:335-348` | Doctrinal pointer, required by **ADR-86 §3** ("lands with the build, not before"). Already carries the honest-limits note naming F3 and F5. |
| The operator, by opening the file | `ecosystem/conformance.md` · `ecosystem/conformance.html` | The HTML sibling exists (operator addendum, 2026-08-19) precisely so the artifact is **openable without running anything** — which is what makes a stale committed copy a stale *trust surface* rather than a stale cache. |
| `ADR-85 R2` / `[#169]` staleness signal | Designated landing site (ADR-86 §4) | Designated, not yet wired. |

No machine consumer reads it. That matters for the freshness leg's severity: a stale dashboard
misleads a **reader**, it does not corrupt a computation.

### 1.4 How stale it is right now — the number

Artifact's last commit — both faces, one commit:

```
5e776542c5d14f226cad101a36bb450d598bcfe7  2026-08-20  rdwornik
docs(dashboard): regenerate over every landing of the day, and anchor the Codespaces landing
```

Newest commit date per declared input path (§5.1 derives the set):

```
2026-08-23  BACKLOG.md
2026-08-23  tasks/
2026-08-23  docs/intake/
2026-08-22  docs/decisions/
2026-08-23  docs/audits/
```

| Metric | Value at `aeec0fd1` |
|---|---|
| **Staleness, in days** (newest input commit date − artifact commit date) | **3** (2026-08-23 − 2026-08-20) |
| Commits on `HEAD` since the artifact was committed | **213** |
| …of those, on the first-parent spine | **42** |
| …of those, touching the declared input set | **78** |
| `gen_dashboard.py --check` | **rc=1** — `STALE ecosystem/conformance.md`, `STALE ecosystem/conformance.html` |

The day-delta (**3**) is the metric the §5 leg uses, because it is the metric probe **P5** uses for
the same question. The commit counts are recorded as context: they are what makes "3 days" concrete
— **42 first-parent landings** happened against a dashboard that claims to describe the repo.

### 1.5 Library-first check — the internal move, and the absence it found

The contract asks for the generator that already commits its own output, to follow its shape.

**There is none.** Every `git add` / `git commit` subprocess site in `scripts/` was enumerated:

| Site | What it is |
|---|---|
| `scripts/enforcement_coverage.py:493,494,515,516,635,636` | Builds throwaway probe **clones** to prove gates fire. Not the repo. |
| `scripts/nopack_sandbox.py:1167,1176` | Sandbox fixture tree. Not the repo. |
| `scripts/review_closures.py:187` | `git_commit_exists` — a **read**. |
| `scripts/single_flight.py:419` | `git cat-file commit` — a **read**. |
| `scripts/cloud_provisioning.py:322` | Compares `cat-file -t` output to the string `"commit"` — a **read**. |

**No generator in this repo commits its own output. `ADR-80 §3`'s writer policy has zero
implementations here.** Per the contract, that absence is itself a finding, and it is the single
strongest piece of evidence for R1 option (b): the ruling does not decline a working convention in
favour of prose — it ratifies the **only** convention this repo has ever actually run.

The shape every generator does follow, verified across `gen_task_tree`, `gen_audit_index`,
`gen_intake_index`, `gen_doc_counts`, `gen_methodology_roster`, `gen_claude_rosters`,
`generate_organ_index`, `gen_intake_tree`:

> **write → print what was written → a human commits it → a `--check` regen-and-diff pre-commit
> hook refuses a stale copy.**

`gen_dashboard.py` implements the first two legs and has the fourth available but unarmed (§1.2).
Steps 3–5 make it honest about the third and give it the freshness half of the fourth.

---

## 2. The ruling, and what executing it meant (Step 2)

**R1, executed not evaluated.** The contract names one condition under which this lane may stop
and ask — a genuine rule-vs-ruling conflict, of which "implement (a) instead of (b)" is the named
instance. **No such conflict arose.** The derivation ran the other way: the library-first sweep
(§1.5) found that ADR-80 §3's writer policy has **zero implementations** anywhere in this repo, so
(b) is not a concession to convenience — it ratifies the only convention that has ever actually
run here, and (a) would have introduced this repo's first self-committing writer.

**Form.** `docs/decisions/ADR-86-conformance-dashboard-location.md` gains an **appended
`## Amendment — 2026-08-23`** marker at the file end. §2's original decision text is
byte-unmodified. The form is not a choice this lane made: `CLAUDE.md` §5 rule 3 and
`protocols/STANDING_RULINGS.md` **J-3** both prescribe it, and ADR-94's in-place exception is
scoped to the *status line* only — which this amendment does not touch (ADR-86 stays **Accepted**).

**What the amendment withdraws, and what it keeps.** Withdrawn: only the clause that the
**validator itself** commits. Kept: the location, the ADR-80 **committed-generated** zone class
*and its name*, the Layer-2 posture, pathspec-boundedness, and the diffable-and-auditable
rationale that rejected generate-on-demand. The zone class was always a claim about the artifact's
**state** — committed rather than regenerated on demand — and (b) preserves that property whole.
**ADR-80 §3 is not repealed:** it remains live doctrine for any unattended job that dirties the
tree. It is simply not this artifact's mechanism, and ADR-86 no longer says it is.

**A third thing the amendment settles, which the contract did not ask for but §2 left open.**
ADR-86's *Deferred to the build (#171)* paragraph explicitly deferred "the exact write channel
(committed on `main` as a navigable surface vs. an `automation/*` branch per the ADR-84
writer-isolation pattern)". (b) answers it: **committed on `main`**. ADR-84's isolation pattern
exists for *unattended* writers, and under (b) there is no unattended writer. Recorded because
leaving a settled fork marked "deferred" is the same class of stale claim this lane exists to
remove.

**One in-place edit, disclosed.** `docs/decisions/README.md`'s ADR-86 row carried the withdrawn
claim in its own editorial one-liner ("a read-only validator generates + commits its own output").
That file is a **living index**, not an immutable ADR, and its ADR-101 / ADR-104 rows already
carry in-row `**Amended <date>**` clauses — so the same in-place form was used. Left alone, the
index would still be describing a superseded reading of a file it points at.

---

## 3. Both artifact strings corrected — and the third site (Step 3)

The contract names two strings. **Three sites** carry the same false mechanism; all three are
corrected, and the third is called out rather than folded in silently, because it sits outside the
contract's literal wording.

| # | Site | Reaches | In the contract's "two strings"? |
|---|---|---|---|
| 1 | `gen_dashboard.py::_preamble` → `ecosystem/conformance.md:7` | The operator opening the markdown | **Yes** |
| 2 | `gen_dashboard.py::render_html` → `ecosystem/conformance.html:45` | The operator opening the HTML | **Yes** |
| 3 | `gen_dashboard.py` module docstring `:9-11` | The next reader of the code | **No** — but it is the sentence the Phase-0 packet quotes as *the root* (§Premise B) |

**Not made true by being made vague.** The contract names the risk precisely: *"Generated" is not
an honest replacement for a false "generated and committed."* Both faces now state the mechanism
in full — **who** commits (the person or integrator who ran `--write`), **that** the generator
commits nothing, **what the commit is bounded to** (pathspec-bounded, both faces), **when the copy
is current to** ("exactly as current as its own last commit, never fresher"), and **which ruling**
they describe (ADR-86 amended 2026-08-23).

**Both committed faces were regenerated**, so the correction is live on the surface a reader
actually opens — not merely in the generator that could produce it. Correcting the emitter and
leaving the committed artifact carrying the false string would have reproduced the exact failure
this lane exists to fix: judging a mechanism by its header rather than by the thing itself.

**Six tests pin it** (`tests/test_gen_dashboard.py`). A negative assertion alone would have been
insufficient — deleting the sentence entirely passes "the false string is gone" while telling the
reader nothing — so the positive content is asserted too: each face must name who commits, must
say what it is current to, and must cite the amendment. The sixth covers the docstring site.

---

## 4. The commit path, explicit and observable in the code (Step 4)

The contract's fourth closure condition is the sharp one: the human/integrator commit path must be
**observable in the code, not merely described in prose**. Prose describing a mechanism is exactly
what `[#171]` leg 1 already had, and it is what fooled an integrator review pass.

**What landed in `scripts/gen_dashboard.py`:**

- **`commit_pathspec()`** — derived from `_TARGETS`, the same tuple `write_outputs` iterates. The
  pathspec therefore *is* the write targets, never a re-typed literal that can drift from what was
  actually written. ADR-80 **Rider 1** ("stages exactly its own declared output paths — never
  `git add -A`") survives the amendment intact: what (b) changes is **who runs** the commit, not
  what it is bounded to.
- **`commit_path_commands()`** — the two-command path as **argv lists**, built in code.
- **`render_commit_path()`** — the same commands as copy-pasteable shell.
- **`--commit-path`** — a CLI verb printing exactly those commands. It needs no git and touches no
  file, so an integrator or a runbook can ask the generator what its commit path *is* without
  running anything.
- **`--write` prints the path it did not run**, every time, immediately after writing.
- **Both artifact faces carry the same pathspec**, sourced from the same function.

Live output:

```
$ python scripts/gen_dashboard.py --write
gen_dashboard: wrote ecosystem/conformance.md
gen_dashboard: wrote ecosystem/conformance.html
gen_dashboard: NOT committed. This generator has no writer of its own; a human or integrator commit satisfies "committed" (ADR-86 amended 2026-08-23).
gen_dashboard: commit path, pathspec-bounded to exactly the files just written:
    git add -- ecosystem/conformance.md ecosystem/conformance.html
    git commit -m "docs(dashboard): regenerate ecosystem/conformance.{md,html}"
```

**And the negative half is asserted where it cannot lie.** A header that says "commits nothing"
can be wrong — that is this entire lane. So a test runs `--write` against a **real git repo** and
asserts that HEAD has not moved and both outputs are sitting dirty afterwards. That is the ADR-81
leg **(e)** functional proof for the ruling's negative half: not "the code appears to have no
writer", but "it was observed not to write".

*(Asserted behaviourally rather than by monkeypatching `subprocess.run`, which would rewrite the
stdlib module object for the whole xdist worker.)*

---

## 5. The freshness leg (Step 5)

### 5.1 The input set, named — and it *is* derivable

The contract's hardest constraint: *define "older than its inputs" concretely; name the input set;
if it is not derivable, report the gap rather than inventing a proxy.*

It is derivable, and from the generator's own constants rather than from judgment.
`gen_dashboard.build()` reads exactly these tracked paths:

| Input | Read by | Generator constant |
|---|---|---|
| `BACKLOG.md` | `closed_rows_*`, `theme_stats`, `_rows_by_id` | `BACKLOG_RELPATH` |
| `tasks/` | `theme_stats` (the `tasks/` tree) | `TASKS_RELDIR` |
| `docs/intake/` | `intake_rows` (incl. `archive/`, which is inside it) | `INTAKE_RELDIR`, `INTAKE_ARCHIVE_RELDIR` |
| `docs/decisions/` | `adr_rows` | `DECISIONS_RELDIR` |
| `docs/audits/` | `gate_health` | `AUDITS_RELDIR` |

These are now exported as **`gen_dashboard.INPUT_RELPATHS`** — a declaration in the generator, not
a re-derivation in the gate.

**Two inputs are deliberately excluded, and both exclusions are stated rather than silent:**

1. **`logs/TELEMETRY.db`** — read by `telemetry_state` (existence + size), but **gitignored**
   (`.gitignore:95`) and absent from disk. It has no git history, so it cannot carry a commit date
   and cannot take part in a git-date relation. It is declared in the artifact spec's
   `untracked_inputs` field, so the carve-out is visible in code rather than missing from a list.
2. **HEAD itself** — `head_sha()` and `head_date()` are inputs to the *rendering*, not to the
   *content*. This is the load-bearing distinction, and it is why this leg can carry a baseline at
   all: because the dashboard prints HEAD's sha and commit date, **any** commit makes a
   regeneration differ — which is precisely why `gen_dashboard.py --check` "reports drift after
   HEAD moves" by the generator's own admission. A gate keyed on that would fire on every commit
   in the repo and be routed around within a day. Keying on the content input set asks the
   question an operator actually cares about: *has anything the dashboard describes moved since
   the dashboard was committed?*

### 5.2 The relation — probe P5's shape, not a second idiom

P5 asks whether `ARCHITECTURE.md`'s `last_reviewed` stamp is on-or-after that file's last git
touch: a relation between two git dates, passing on-or-after. The same relation, different subject:

```
staleness_days = max(0, newest_input_commit_date − stalest_output_commit_date)
WARN  iff  staleness_days > baseline_days
```

- **`min` over the outputs** — the two faces are written by one run and normally share a commit,
  but if one ever lagged, the pair is only as fresh as its stalest half.
- **`max` over the inputs** — any single input moving forward is what makes the artifact stale.
- **Author date (`%as`), not committer date** — the same choice
  `canonical_freshness_gate.git_last_commit_date` makes, and for the same reason: author date
  survives rebase / cherry-pick / amend, so the relation keys off when content was actually edited
  rather than when history was rewritten.
- **Repo-location env vars are scrubbed** via `gitenv` (loaded by path, per that module's
  terra-hardened contract): an inherited `GIT_DIR` overrides both `cwd=` and `git -C`, which is how
  a validator comes to read the parent repo while labelling the answer with the target's id
  (`[#355]`). A live test proves the scrub by pointing `GIT_DIR` at a decoy repo. **If `gitenv`
  cannot be loaded the function refuses to answer rather than answering unscrubbed** — a wrong
  verdict delivered silently is strictly worse than no verdict.

The module is **`scripts/generated_artifact_freshness.py`** and returns `(fails, warns)` — the
identical signature to `canonical_freshness_gate.evaluate`, so the two freshness organs cannot
drift into two shapes.

### 5.3 The baseline is measured, and it is a ratchet

Re-derived at merge base `aeec0fd1` with the leg's own relation, before any edit in this lane:

```
$ git log -1 --format=%as aeec0fd1 -- ecosystem/conformance.md   ->  2026-08-20
$ git log -1 --format=%as aeec0fd1 -- docs/audits                ->  2026-08-23   (newest input)
                                                        staleness =  3 days
```

**`baseline_days = 3`**, and a test pins the number rather than leaving it a comment — silently
raising a baseline rebases the metric the gate exists to hold, a failure mode this repo has already
caught once at terra HIGH (`audit.py:2288`).

**The honest reading of "3" is not "three days of drift is acceptable."** It is *this repo
tolerated three days of drift once, and the leg forbids worse.* Tightening it is a later act.

**WARN, never FAIL — and the class is load-bearing rather than timid.** Verified against the two
gates' own source, not assumed:

- `audit.py::cmd_health` (the **pre-commit** gate) computes `self_fail = any(f.status == "fail")`
  and exits 1 only on that. **A `warn` does not block a commit.**
- `cmd_ship_gate`'s contract: *"any `warn` NOT dispositioned by the register → RED, exit 1."*

So a WARN-class Finding lands at **ship time** and taxes no ordinary commit — exactly the placement
the contract specifies (*ship-gate, not pre-commit*), bought by choosing a **status class** rather
than by adding a hook. The leg also emits **one Finding per artifact**, which the ship-gate's
disposition contract requires (a matched token suppresses a whole Finding, so aggregate organs must
split). `evaluate` returns `fails == []` **unconditionally, by construction**, with the reason
written on the function: promotion to FAIL is a later act with its own ruling, and one line.

### 5.4 It was observed to fire

ADR-81 leg **(e)**: presence is not proof. The leg's body — the exact code in the fenced diff
below — was run against three trees:

```
--- live repo ---
          pass  generated_artifact_freshness: conformance-dashboard: 0d stale (baseline 3d) — ecosystem/conformance.md committed 2026-08-24, newest input docs/decisions committed 2026-08-24
--- a tree with no dashboard ---
           n/a  generated_artifact_freshness: [n/a-reason:SUBJECT-ABSENT] output ecosystem/conformance.md is not present in this repo
--- a genuinely stale tree ---
          warn  generated_artifact_freshness: conformance-dashboard: 22d stale (baseline 3d) — ecosystem/conformance.md committed 2026-08-01, newest input BACKLOG.md committed 2026-08-23; regenerate + commit: python scripts/gen_dashboard.py --write
```

`tests/test_generated_artifact_freshness.py` (20 tests) pins the same behaviour, half against
injected dates for the boundary arithmetic and half against real throwaway git repos.

### 5.5 Registration — the fenced diff, and what this lane may NOT author

`scripts/audit.py`, `scripts/audit_checks/registry.py` and `ecosystem/doc-code-edge.yaml` are
shared-collision files this batch. Per the contract and the Phase-0 packet §5.3's amended
ownership model, this lane ships its **module** and **tests** as new files and its **registration**
as a diff.

**The lane authors no count pin, and that is correctness rather than politeness.**
`len(ALL_CHECKS)` is pinned by exact equality in **six** places (`tests/test_audit.py` ×2,
`tests/test_doc_code_edge.py` ×2, `tests/test_writer_integrity.py`, and the *generated*
`ecosystem/doc-counts.md`). Their correct value is **N-dependent**: if three lanes each add a
check, each would author `43 → 44` and all three would be wrong. **Preferred position:**
immediately after `check_canonical_freshness` — same family, same question. A preference, not an
assumption: `CHECK_ORDER` is byte-contract-load-bearing and the order is the integrator's call.

```diff
--- a/scripts/audit.py
+++ b/scripts/audit.py
@@ context: just after the canonical_freshness_gate dual-mode import (~:195-198) @@
 try:
     from scripts import canonical_freshness_gate as _cfg
 except ImportError:
     import canonical_freshness_gate as _cfg
 
+# Generated-artifact staleness leg (ADR-86 as amended 2026-08-23; `[#171]` leg 1 / f7). Exactly
+# the relationship this module already has with `_cfg` above: the relation lives in ONE module,
+# and the leg below only wraps its verdict in the Finding envelope. Dual-mode import for the
+# same reason (`python scripts/audit.py` vs `python -m scripts.audit`).
+try:
+    from scripts import generated_artifact_freshness as _gaf
+except ImportError:
+    import generated_artifact_freshness as _gaf
+
```

```diff
--- a/scripts/audit.py
+++ b/scripts/audit.py
@@ context: beside the existing audit-level freshness aliases (~:545-546) @@
 _parse_last_reviewed = _cfg.parse_last_reviewed
 _git_last_commit_date = _cfg.git_last_commit_date
+# Audit-level alias for the same reason the two above exist: it keeps a monkeypatch seam, so a
+# test that rewrites the name on the `audit` module still reaches the leg.
+_gaf_git_last_commit_date = _gaf.git_last_commit_date
```

```diff
--- a/scripts/audit.py
+++ b/scripts/audit.py
@@ context: immediately after check_canonical_freshness's return (~:592) @@
     return [Finding("canonical_freshness", "pass",
                     f"{len(_FRESHNESS_FILES)} canonical living files fresh "
                     f"(last_reviewed not before last edit; within {_FRESHNESS_CADENCE_DAYS}d)")]
 
+
+def check_generated_artifact_freshness(repo_path: Path) -> list[Finding]:
+    """Committed-generated staleness — is a committed generated artifact older than its inputs?
+
+    ADR-86 as AMENDED 2026-08-23 rules that a human or integrator commit satisfies "committed".
+    That makes the dashboard's header honest; it does nothing to keep the output CURRENT. An
+    honest header on a stale trust surface is still a stale trust surface, so this leg is the
+    other half of the same ruling: WARN when the committed artifact has fallen further behind its
+    declared inputs than the baseline measured when the leg was armed (dashboard: 3 days, at
+    `aeec0fd1` on 2026-08-23). The baseline is a RATCHET, not an allowance — it records that this
+    repo tolerated three days of drift once, and forbids worse.
+
+    WARN-CLASS BY RULING, and the class is load-bearing rather than timid. `cmd_health` (the
+    pre-commit gate) exits 1 only on a `fail`, while `cmd_ship_gate` REDs on any undispositioned
+    `warn` — so this signal lands at ship time and does NOT tax every commit that touches an
+    input. A gate that taxes ordinary work gets routed around. RED here is a later act with its
+    own ruling, and when it comes it is a one-line change in
+    `generated_artifact_freshness.evaluate`.
+
+    DISTINCT FROM `gen_dashboard.py --check`, deliberately: the Phase-0 packet is explicit that
+    the two must not be blurred. `--check` asks whether the committed bytes match a regeneration;
+    it is HEAD-pinned, so it drifts on EVERY commit and could carry no meaningful baseline. This
+    asks whether the committed copy is current with respect to its CONTENT inputs. That `--check`
+    is armed nowhere (R3 F5) is a gating gap this leg does not close.
+
+    ONE Finding PER ARTIFACT so the #147 ship-gate dispositions each independently — the same
+    contract `git_backlog_drift` carries, and required by the disposition rule that a matched
+    token suppresses a WHOLE Finding. Logic single-sourced in
+    `scripts/generated_artifact_freshness.py`; this leg only wraps it, passing the audit-level
+    git-date alias so a monkeypatch at the audit level still applies. Read-only; degrades rather
+    than inventing a verdict — an absent artifact is `n/a` SUBJECT-ABSENT (a consumer repo with
+    no dashboard), an unreadable history is `unavailable`.
+    """
+    name = "generated_artifact_freshness"
+    findings: list[Finding] = []
+    for artifact in _gaf.REGISTRY:
+        m = _gaf.measure(repo_path, artifact, git_date_fn=_gaf_git_last_commit_date)
+        if m.verdict == "unmeasurable":
+            findings.append(
+                _na(name, "SUBJECT-ABSENT", m.detail) if m.subject_absent
+                else Finding(name, "unavailable", m.detail.replace("|", "/")))
+        elif m.verdict == "stale":
+            findings.append(Finding(name, "warn",
+                                    f"{m.detail}; regenerate + commit: "
+                                    f"{artifact.regen_command}".replace("|", "/")))
+        else:
+            findings.append(Finding(name, "pass", m.detail.replace("|", "/")))
+    return findings
+
```

```diff
--- a/scripts/audit.py
+++ b/scripts/audit.py
@@ context: the ALL_CHECKS literal (~:3407) @@
     check_handoff_bundle_structure,
     check_canonical_freshness,
+    check_generated_artifact_freshness,   # ADR-86 amd. 2026-08-23 / `[#171]` leg 1 — WARN-tier
+                                          # by ruling; RED is a later act with its own ruling
     check_no_sibling_orphans,
```

```diff
--- a/scripts/audit_checks/registry.py
+++ b/scripts/audit_checks/registry.py
@@ context: CHECK_ORDER, beside check_canonical_freshness @@
     "check_canonical_freshness",          # facade — _git_last_commit_date seam
+    "check_generated_artifact_freshness",  # facade — _gaf_git_last_commit_date seam
     "check_no_sibling_orphans",           # facade — _git_registered_worktrees seam
```

```diff
--- a/ecosystem/doc-code-edge.yaml
+++ b/ecosystem/doc-code-edge.yaml
@@ context: the exempt: list, after review_artifact_coverage @@
   - review_artifact_coverage
+  # ADR-86 amd. 2026-08-23 generated-artifact staleness leg. **TEMPORARY**, on the
+  # `review_artifact_coverage` precedent directly above and for the same reason: enforcement
+  # ahead of its written rule runs only under a NAMED, EXPIRING exemption. The rule this leg
+  # embodies — "a committed generated artifact must not fall further behind its inputs than its
+  # measured baseline" — is currently written only in an ADR amendment, which is an immutable
+  # decision record, not a living doc a `# rule:` marker can bind to. When that rule lands in
+  # PLAYBOOK this entry converts to `coverage_scope` and the marker is added. Carried by intake
+  # #42; the row is specified in
+  # docs/audits/2026-08-23-technical-lane-dashboard-commit-path.md §7.4 and NOT filed
+  # (R2 `banked = 0`, no births this batch).
+  - generated_artifact_freshness
```

**Integrator checklist for this diff** (the lane's own, offered rather than assumed):

1. Apply the six hunks above.
2. Count `ALL_CHECKS` **once**, across every sibling lane that added one, and set pins 1–5 to the
   resulting number.
3. Run `python scripts/gen_doc_counts.py --write` for pin 6 — it is generated and must never be
   hand-edited.
4. `python scripts/audit.py checks` should list the new member; `python scripts/audit.py health`
   should show it `pass` on a current tree.

### 5.6 Honest limits — stated, because the leg's value depends on knowing them

1. **Written and tested, not yet armed.** Until the fenced diff is applied, the leg is an ADR-81
   leg-**(d)** *explicit documented deferral*, not a live gate. It is named as such inside the
   ADR-86 amendment itself, so a later audit does not have to rediscover it.
2. **It measures currency, not correctness.** A dashboard regenerated from a broken parser is
   fresh and wrong; this leg would call it fresh.
3. **It cannot see an untracked input.** The telemetry store could change hourly and the relation
   would not move. Stated in §5.1, declared in code.
4. **Day granularity.** Two commits on the same day are indistinguishable — inherited from P5 and
   from `%as`, and deliberately not "improved" into a second idiom.
5. **No rename following.** `git log -- <path>` is used without `--follow`; if an input path is
   renamed, its pre-rename history stops counting until the declaration is updated. The
   declaration lives in `gen_dashboard.INPUT_RELPATHS`, next to the code that would be renaming it.
6. **It does not close R3 F5.** `gen_dashboard.py --check` is still armed nowhere. Different
   defect, different act — the Phase-0 packet draws that boundary explicitly.

