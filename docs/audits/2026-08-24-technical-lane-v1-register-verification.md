# LANE V1 — register verification, domain V1 (governance documents & agent context)

Verification of every `domain: V1` row of `docs/audits/2026-08-24-technical-research-candidate-register.md`,
read against `docs/audits/2026-08-24-technical-research-register-addendum.md` (**the addendum governs
where the two disagree**), plus the lane-specific command/skill census the addendum assigns to V1 by
name under C31.

**This lane rules nothing.** Every verdict below is evidence for the architect's batch ruling.

## Execution environment (declared)

- Substrate: `cloud-session`, shallow clone of `origin/main` at `e4e5b6b`.
- **uv probe:** PATH `uv` measured **0.8.17**; `pyproject.toml:25` `required-version = "==0.11.19"`.
  **Mismatch** — so the pinned uv was installed per the brief
  (`python3 -m pip install --target ./uvpin "uv==0.11.19"`, verified `uv 0.11.19`), and **every
  executed probe in this artifact ran under `./uvpin/bin/uv run --locked`**, never the PATH uv.
  This is the C18 inert-gate class the register itself names; recording it so the verdicts are not
  silently unpinned.
- `./uvpin/` is a build artifact of this lane, untracked and not committed.

## Verdicts — C01…C07

| row | verdict | locator | note |
|---|---|---|---|
| C01 | **CONFLICTS** — ADR-53 Decision 2 | `docs/decisions/ADR-53-claude-md-single-instruction-file.md:25` (Status `Accepted`, `:3`); rejected alternative `:47` | Addendum governs; register's `conflicts: none` is refuted. Root `AGENTS.md` **absent** from tree; `classify('AGENTS.md')` refuses — re-executed here (third machine). |
| C02 | **PARTIAL** — ceiling landed, "everything procedural leaves" not | `scripts/validate_doc_rot.py:121` (`_FILE_SIZE_BUDGETS = {CLAUDE: 200}`); measured **195/200, headroom 5** | Register's `conflicts:` "headroom measured at 2-3 lines" is **stale** — measured 5 here with the repo's own checker. CLAUDE.md still carries procedure (§6, §9). |
| C03 | **PARTIAL** — on-demand landed, chapter→skill split absent | `CLAUDE.md:14` and `:27` (PLAYBOOK is reference, not boot-read); `protocols/PLAYBOOK.md` = 4996 lines, Ch8 at `:1237` | Only two `SKILL.md` exist in-tree, neither a PLAYBOOK chapter. `changes:` claim not met — `CLAUDE.md:14` still literally says "consult `protocols/PLAYBOOK.md` on demand". Conflicts note holds: Ch8 is freshly authored, ~1400 lines. |
| C04 | **ABSENT** — checked `protocols/PLAYBOOK.md`, `protocols/ESSENTIALS.md`, `CLAUDE.md` | no hit for delete-prose-a-gate-enforces doctrine on any of the three | Nearest relative is `scripts/silent_rule_detector.py` — a *counter* that drains rules with a normative home elsewhere, not a deletion doctrine. **Collision to weigh:** `CLAUDE.md:232` records §9's hook roster as deliberately restated *because* `validate_doc_claims::precommit_hook_roster` reads it — "collapsing it would disarm the gate". |
| C05 | **PARTIAL** — mechanism present, scoping unused | `.claude/rules/git-discipline.md:2` — `paths: "**/*"` | The `paths:` frontmatter the row proposes already exists, but with a **universal glob**, so no directory-scoping is in effect; `.claude/rules/` holds n=1 file. Conflicts field is accurate: the carve-out is real at `CLAUDE.md:101` (§5 rule 7). |
| C06 | **CONFLICTS** — `CLAUDE.md:23` §1 first-read (hub region `first-read`) | census: `scripts/canonical_docs.py:73`, `:82`, `:88`, `:95`; `scripts/canonical_freshness_gate.py:50` | **The row's own escape clause fires.** Five code surfaces read ESSENTIALS (`CANONICAL_OPTIONAL`, `FRESHNESS_FILES`, `SECTION_HISTORY_DOCS`, `STRUCTURE_DOCS`, and the gate's standalone fallback list), and §1 mandates it as a boot read. The census the row demands has been run and it says do not retire. |
| C07 | **PARTIAL** — generated half exists, proposed mechanism collides | `ARCHITECTURE.md:221` + `:237` (codemap auto-generated, `codemap-freshness` pre-commit gate); stamp `ARCHITECTURE.md:2` `last_reviewed: 2026-08-23` | Structural claims are **already** generated for the codemap. But the row's proposed `pyreverse/pydeps -> Mermaid` output collides with a landed amendment: `CLAUDE.md:83` — the ADR-51 amendment 2026-07-05 **moved Mermaid out** of canonical `ARCHITECTURE.md`, "its codemap is now compact text". Conflicts note confirmed: the docs-governance lane re-stamped the file 2026-08-23. |

### `evidence: measured-here` obligation

**Zero V1 rows carry `evidence: measured-here`.** C01/C02/C07 are `independent`, C03 `vendor+independent`,
C04/C06 `practitioner`, C05 `vendor`. No measurement-artifact locator is owed for this domain, and no
`DOWNGRADE-TO-PRACTITIONER` applies. (The register's own count — "11 ADOPTs rest on `measured-here`" —
is therefore carried entirely by V2–V5.)

### C01 — the detail, because the addendum's correction rests on it

Four things measured in this container:

1. **Root `AGENTS.md` does not exist.** `git ls-files` returns only `codex/AGENTS.md` and
   `templates/archive/AGENTS-md-template.md`. Neither is a root instruction file.
2. **ADR-53 Decision 2 is live**, `Status: Accepted` (`:3`), un-superseded, verbatim (`:25`):
   > **`AGENTS.md` as a separate per-repo file is retired.** Existing `AGENTS.md` files in
   > `.dev-knowledge` and `ai-council` are to be removed and their content merged into each repo's
   > `CLAUDE.md` (subsequent implementation chunk).
3. **The shape C01 proposes is the alternative ADR-53 rejected**, verbatim (`:47`):
   > **Keep AGENTS.md alongside CLAUDE.md, with CLAUDE.md as a thin pointer** — rejected: perpetuates
   > the two-file drift problem without benefit; both tools read CLAUDE.md directly, making any
   > pointer model unnecessary overhead.
4. **The phrase the register's `conflicts: none` comment relies on is not in ADR-53.** Grep for
   "two content-carrying files" across `docs/decisions/` returns **0 hits**. The addendum's refutation
   is confirmed independently here.

**The gate agrees with the ADR, executed not quoted:**

```
validate_hermetization.classify('AGENTS.md')
-> "unsanctioned new top-level file 'AGENTS.md' -- Tier-1 files are a closed class
   (ADR-101 section 1); a genuinely new class is an ADR-101 amendment, not a drive-by add"
```

This is the third machine to return that refusal (cloud container 2026-08-23/24, operator's Windows
checkout, this container).

**Fork state, for the architect only:** intake **#42** is filed and `READY` —
`docs/intake/2026-08-24-tech-agents-md-admission-vs-adr53.md:2` (`intake-id: 42`), registered in
`docs/intake/manifest.json:450`. Register ruling **R-1** is live at
`protocols/STANDING_RULINGS.md:1920` ("`AGENTS.md` is ADMITTED, on the substance reading of ADR-53").
Carrier `[#577]` is **open** (`tasks/577-adopt-agents-md-as-the-portable-instruction-layer.md:13`,
mirrored `BACKLOG.md:229`) and its Done-when opens with "a root `AGENTS.md` ≤120 lines exists" — which
the hermetization gate refuses today. The addendum's `ADOPT → BLOCKED-ON-ADR` and its
"Done-when ruled unexecutable as written" both hold against measured state.

## V1 lane duty — command/skill census (addendum, C31)

Eleven files, matching the addendum's expected surface exactly (8 commands · 2 skills + `verify.py`).
Purpose and trigger are taken from each file's own frontmatter/body, not inferred.

| file | purpose (one line) | trigger |
|---|---|---|
| `.claude/commands/changelog-review.md` | Review tool changelogs since last review (claude-code + codex), classify per the audit-trio rubric, write a digest, bump the state file. | Operator-invoked, **PUSH only**; the SessionStart `changelog_sentinel.py` merely nudges. Never implements adoptions. |
| `.claude/commands/handoff-verify.md` | Run the whole live probe gate for a handoff bundle in ONE pass, emit exactly ONE evidence block. | Boot of a v6 handoff bundle (HANDOFF_PROCESS §5) — one command → one evidence block → one operator paste. |
| `.claude/commands/handoff.md` | Generate or complete a handoff bundle per HANDOFF_PROCESS.md v6 (CC-owned residual + thin browser boot). | Operator says "please create handoff for `<repo>`" or "complete handoff for `<repo>`". |
| `.claude/commands/lane-boot.md` | Boot ONE batch lane: provision the worktree per the naming enum, seed it, load the frozen contract, state the V-2 decision budget before any work. | Start of one lane of a batch; doctrine in PLAYBOOK Ch8. |
| `.claude/commands/lane-integrate.md` | Walk a batch's merge queue serially from the primary checkout, then run the six-item refuse-to-finish checklist mechanically. | Batch integration, run **from the primary checkout**, never from a lane. |
| `.claude/commands/override.md` | **RETIRED** (ADR-85 amendment 2026-08-03 §A2) — discharges no gate; arms a local telemetry token only. | Should not be invoked to discharge anything; `_override_active()` is kept inert. |
| `.claude/commands/preflight.md` | Verify every repo locator a contract or prompt cites — `file:line`, headings, SHAs, `[#id]` liveness — before acting on it. | Before acting on any contract/brief/handoff. Read-only, adoption-first, wired into no gate. |
| `.claude/commands/save.md` | Stage all changes and commit with a descriptive Conventional Commits message. | Any commit; git history IS the changelog here (no CHANGELOG.md since 2026-05-16). |
| `.claude/skills/verify/SKILL.md` | Run the standard check cadence (pytest + ruff + git-status), report compact 3-line pass/fail. | After each numbered step; any FAIL blocks the current step. |
| `.claude/skills/verify/verify.py` | The bundled script the `verify` skill runs; PASS/FAIL per check, full output only on failure, exit 1 on any fail. | Invoked by the skill as `uv run --locked python .claude/skills/verify/verify.py`. |
| `.claude/skills/check-against-spec/SKILL.md` | Semantic half of the coherence spine: run the deterministic site enumerator, then verdict EACH site (stale/fine/not-relevant, +transclusion-candidate) into the re-stamp commit message. | A spec version advances; consumes `{dependent_path, spec_path, old_version, new_version}`. |

### Procedures flagged as CONFLICTS against a landed ruling

Two, both quoted verbatim. The lane flags; it does not rule.

**CENSUS-1 · `.claude/commands/lane-boot.md:132-133` CONFLICTS with P-1**
(`protocols/STANDING_RULINGS.md:1783`).

The command instructs a **lane** to journal:

> - Write the lane's JOURNAL entry **on this branch, ahead of any merge** — see PLAYBOOK
>   "JOURNAL-rides-the-branch".

P-1 says the opposite for a lane, verbatim:

> ### P-1 · `JOURNAL.md` is the integrator's surface; a lane records its work in its artifact
> > A lane leaves `JOURNAL.md` alone. One entry per batch or night, written by the integrating
> > seat, anchors the whole set; a lane's deliverable is its own artifact plus its commits.

This is a genuine two-surface collision, not a misreading: the rule `/lane-boot` cites is real and
also live — `protocols/PLAYBOOK.md:1908`, "**JOURNAL-rides-the-branch is the anchoring law.** An arc's
JOURNAL entry is written **on that** [branch]". P-1 scopes to a **lane**, PLAYBOOK Ch8 scopes to an
**arc**, and `/lane-boot` applies the arc rule to a lane. P-1's own provenance records the breach that
produced it (N4 committed two lane-authored JOURNAL entries; the branch was refused at the gate). **A
lane booted by `/lane-boot` today is instructed into exactly that breach** — which is why this brief
had to carry "No JOURNAL entry (P-1: a lane never journals)" as an explicit override. Architect's call:
scope-correct `/lane-boot`, or scope-correct P-1.

**CENSUS-2 · `.claude/commands/handoff-verify.md:73` CONFLICTS with ADR-106 §4** (as stated at
`CLAUDE.md:71`).

The command's step 2 says:

> 2. **Structural pre-check.** Run `python scripts/verify_handoff_probes.py <bundle-dir>`.

`CLAUDE.md:71` rules that shape a defect, verbatim:

> Every gate invokes `uv run --locked …`, so a bare `python`/`pytest` in a doc or runbook is a defect,
> not a shorthand.

Measured, not assumed: this is the same class L5 recorded at `CLAUDE.md:232` — a bare
`python scripts/…` "provably fails on a clean checkout (`ModuleNotFoundError: click`)". It is the
**only** bare invocation left across the eleven files; every other command already uses
`uv run --locked` (`preflight.md:9`, `lane-boot.md:25/33/78/125`, `lane-integrate.md:64/97`,
`verify/SKILL.md`, `verify.py:42`). One-line fix, outside this read-only lane's write scope.

### Rulings the census could not check, stated rather than glossed

The addendum names four rulings to flag against. **Only one has an in-repo locator under the name
given:** P-1 (`protocols/STANDING_RULINGS.md:1783`). Grep across `protocols/STANDING_RULINGS.md` and
every `docs/audits/2026-08-24-*.md` returns **0 hits** for "sentinel-on-tip", "regenerate-never-pick"
and "measure-once"/"N-dependent" — the only occurrence of all three strings anywhere in the tree is
the addendum's own line 95 that names them. The underlying *practices* are visible in the batch close
(`docs/audits/2026-08-24-technical-batch-close.md:30` "Every tip was asserted to BE its sentinel commit
before merging"; `:136` a lane "shipped an audit artifact without regenerating the [index]"; `:182`
"R8's own diff directed the integrator to re-measure after the LAST [change]"), but a practice recorded
in a close report is not a ruling with an id a lane can cite. **The three were checked against those
descriptions and no command or skill contradicts them** — but that finding rests on the batch-close
prose, not on a registered ruling, and is offered at that strength. If they are meant to bind, they owe
a `STANDING_RULINGS.md` entry.

## Scope compliance

- Writes: this file only. No `tasks/`, `BACKLOG.md`, `protocols/`, `docs/decisions/` edit; no JOURNAL
  entry (P-1); no merge.
- The generated audits index (`docs/audits/README.md`) **was regenerated**, by
  `gen_audit_index.py --write`, never by hand. Recorded precisely because it is a second write:
  **no hook demanded it** — `.git/hooks/pre-commit` is **NOT-ARMED** in this container, which is
  the cloud-session gap the register's own C30/A1 correction names ("no armed hooks"). The gate's
  own checker was run read-only instead (`gen_audit_index.py --check` → "docs/audits/README.md is
  stale vs docs/audits/") and it is this lane's added file that made it stale, so leaving it would
  hand the integrator a failing gate on an armed checkout. Regenerated, not hand-picked.
