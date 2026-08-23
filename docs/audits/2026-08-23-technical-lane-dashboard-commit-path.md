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

<!-- SECTIONS 2-7 APPENDED BY LATER STEPS OF THIS LANE -->
