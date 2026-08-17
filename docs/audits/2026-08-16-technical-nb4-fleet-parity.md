---
title: "nb4 fleet-parity sweep — the 8 ADR-104 non-hub members, read-only, from remote HEAD"
date: 2026-08-16
class: technical
status: DRAFT
---

# nb4 fleet-parity sweep (DRAFT)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-16
- **Source-session:** `nb4-F · fleet-parity`, branch `claude/adr-104-fleet-parity-audit-f1lr7a`, hub HEAD `d137cc6`
- **Status:** DRAFT — read-only sweep, **zero writes to any consumer repo**; proposals only, no row advanced, no gate changed
- **Model:** claude-opus-5
- **Inherited-vs-measured:** every per-repo cell below was **MEASURED** this run against remote HEAD
  (clone SHAs recorded in §1). The hub-side contract cells (`ecosystem/*.yaml`, `BACKLOG.md`,
  the 2026-07-08 ruling) were **MEASURED** against the live hub tree at `d137cc6`. Nothing is
  inherited from an earlier parity artifact — in particular this sweep does **not** carry forward
  `docs/audits/2026-07-11-technical-fleet-parity-register.md`'s verdicts.

## 1. Scope, method, and the limits that bound every number below

**Population.** The 8 non-hub members of the ADR-104 declaration
(`docs/decisions/ADR-104-fleet-repository-shape.md:15`, and its machine-locatable
`declaration:start id=adr104-fleet-members` block): `ai-council`, `corp-monorepo`, `corp-ops`,
`corp-sca-time-automation`, `demo-prep`, `life-architect`, `terminal-setup`, `win-tooling`.

**Method.** Read-only clone (`--filter=blob:none`, no checkout side-effects) or definitive
reachability probe per member; then a differential read of the hub's own contract surfaces.
No consumer repo was written to, branched, pushed, or attached for push access.

### 1a. THE LIMIT THAT MATTERS: this is a remote-HEAD view, not the hub checker's view

`ecosystem/registry.md` addresses every member by a **local Windows path**
(`C:\Users\1028120\Documents\Dev\<repo>`), and `scripts/fleet_parity.py` is explicitly built on
**working-tree reads by design (bounded, no clones — AC-7)**. This sweep could not read those
working trees; it read **GitHub remote HEAD**. The two disagree for any repo whose local tree is
ahead of, behind, or divergent from its remote — and for 5 members there is no remote at all.

**Consequence, stated plainly: this report cannot reproduce `fleet_parity.py`'s verdict and does
not claim to.** It is a parity view of *what is published*. Where the local tree is the authority
(it is, for the hub's own machinery), a follow-up run on the operator's machine is the only way
to close the remaining 5 rows.

**This limit was confirmed by the hub's own machinery, not merely asserted.** `scripts/audit.py health`
was run this session and reported, for the two walked consumers:

```
[~~] fleet_parity: ai-council fleet-membership unavailable: unresolved: /home/user/ai-council is not a git repo
[~~] fleet_parity: corp-monorepo fleet-membership unavailable: unresolved: /home/user/corp-monorepo is not a git repo
```

The checker resolves members as **siblings of the hub checkout** and found none, because in a cloud
session there are none. So in this environment `fleet_parity` walks **0 of 9** — it is not that its
verdict was ignored in favour of this sweep's, it is that it had no tree to read. That is precisely
why the clone-based method above was used, and precisely why its results are labelled a remote-HEAD
view rather than a parity verdict.

**Two further environment facts, recorded so no number here is over-read.** (i) The hub checkout is a
**shallow clone** (281 commits; graft boundary in `.git/shallow`), so `audit.py health` reports
`journal_spine_anchor` as `[!!] backstop could not complete … 24882f8cc is not a valid object name`
— the disposition floor lies beyond the graft. This is tree-independent (the underlying
`git merge-base --is-ancestor 24882f8cc main` fails identically with a clean index) and is **not**
caused by this sweep. (ii) The container's pre-commit stages are **not armed**
(`hooks-armed WARN … stage(s) NOT armed: commit-msg, pre-commit, pre-push`). Overall `health: DEGRADED`
in this container is therefore an environment reading, and no claim in this report rests on it.

### 1b. Reachability — measured, not inferred

`mcp__Claude_Code_Remote__list_repos` returned 41 repos, `has_more: false`. Each unlisted member
was then probed individually via `add_repo` to get a backend answer rather than an absence-from-a-listing:

| Member | Probe result | Evidence |
|---|---|---|
| `ai-council` | reachable, public | cloned, HEAD `7a3c057` (2026-08-12) |
| `corp-monorepo` | reachable, private | attached + cloned, HEAD `fd3325e` (2026-08-09) |
| `corp-sca-time-automation` | reachable, public | cloned, HEAD `1a80a9e` (2026-08-08) |
| `corp-ops` | **NOT REACHABLE** | `add_repo` → *"you don't have access to rdwornik/corp-ops"* |
| `demo-prep` | **NOT REACHABLE** | `add_repo` → *"you don't have access to rdwornik/demo-prep"* |
| `life-architect` | **NOT REACHABLE** | `add_repo` → *"you don't have access to rdwornik/life-architect"* |
| `terminal-setup` | **NOT REACHABLE** | `add_repo` → *"you don't have access to rdwornik/terminal-setup"* |
| `win-tooling` | **NOT REACHABLE** | `add_repo` → *"you don't have access to rdwornik/win-tooling"* |

**3 of 8 are observable from a cloud session. 5 of 8 are not.** "Not reachable" here means *no
remote resolvable under this session's credential* — it does **not** prove the repo does not exist.
`ecosystem/registry.md` gives all five a local path, and `life-architect`'s row records
*"GitHub origin CONFIRMED Private (operator, 2026-07-08)"* — so at least one of the five has a
remote this session simply cannot see. The honest reading is **local-first fleet, partial publication**,
not **missing repos**.

## 2. The 8-row parity table

Version columns: `dep.` = `ecosystem/deployed-versions.yaml`; `hub live` = `deploy/manifest-v1.4.0.yaml`
(the newest manifest, **untagged** — see F3). Runbook column = `docs/handoffs/README.md`, the
`[#293]` seed target, read **post-correction** (see §3).

| # | Repo | Role (`parity-surfaces.yaml:104-129`) | Methodology consumed | vs hub live | Runbook `docs/handoffs/README.md` | Parity-surface state | Last hub-sync | Divergence: declared vs silent |
|---|---|---|---|---|---|---|---|
| 1 | `ai-council` | `consumer` (`:106`) | **1.3.1**, deployed 2026-07-11, `source_tag v1.3.1` (`deployed-versions.yaml:30-33`) | at the **tagged ceiling**; 1 minor behind the untagged v1.4.0 manifest | **ABSENT — and CONFORMANT** (ruling `2026-07-08-census-amendment…:45`) | **WALKED**. Floor byte-exact: `4d268f32…` == `templates/child-methodology-floor.sha256` | `.claude/` 2026-08-12 `eaf4e32`; `.methodology.yaml` 2026-07-29 `e4f002e` | **9 DECLARED** in `.methodology.yaml`. ⚠ `dep-pytest-xdist` carries `review_date: 2026-08-16` — **expires today** |
| 2 | `corp-monorepo` | `consumer` (`:107`) | **1.2.0**, deployed 2026-07-07, `source_tag v1.2.0` (`deployed-versions.yaml:34-41`) | 2 releases behind the tagged ceiling — **BY DESIGN**, ADR-102 `gate_rev_ahead`; #336 ruled NOT to bump | **ABSENT — and CONFORMANT** (same ruling) | **WALKED**. Floor byte-exact: `4d268f32…` | `.methodology.yaml` 2026-07-29 `65a8a35`; `.claude/` 2026-07-07 `0cab8be` (the v1.2.0 deploy) | **7 DECLARED**, incl. an 11-file grandfathered UPPERCASE skip-set enumerated in-line |
| 3 | `corp-ops` | `pre-deploy` (`:108`) | **null** (`deployed-versions.yaml:42-45`) | n/a — no deploy record | **NOT OBSERVABLE** (no reachable remote) | **NOT WALKED** — `fleet_parity.py:527` | unknown | **NOT ASSESSABLE.** Registry entry exists, so no `reason:` is required or given |
| 4 | `corp-sca-time-automation` | `pre-deploy` (`:109`) | **null** (`deployed-versions.yaml:46-49`) | n/a — no deploy record | **ABSENT — and CONFORMANT** (same ruling) | **NOT WALKED** — yet it demonstrably **carries the floor** (`4d268f32…`, byte-exact), the sha256 sidecar, `check_floor_hash.py`, the `floor-hash-verify` pre-commit hook, and `.claude/rules/` | `.claude/` + `.pre-commit-config.yaml` both 2026-06-08 `df59f31` (ADR-78 floor adoption) — **69 days stale** | **SILENT — and structurally unable to be otherwise.** No `.methodology.yaml` exists in the repo → nothing can be declared. **F2 below.** |
| 5 | `demo-prep` | `pre-deploy` (`:122-123`) | **absent from the registry entirely** | n/a | **NOT OBSERVABLE** | **NOT WALKED** | unknown | **DECLARED-ABSENT**: `reason:` present and load-bearing (`resolve_fleet` refuses a reason-less pre-deploy absentee) |
| 6 | `life-architect` | `pre-deploy` (`:124-125`) | **absent from the registry** | n/a | **NOT OBSERVABLE** | **NOT WALKED** | unknown | **DECLARED-ABSENT** — `reason:` cites `satellite-onboarding-rulings.yaml` |
| 7 | `terminal-setup` | `pre-deploy` (`:126-127`) | **absent from the registry** | n/a | **NOT OBSERVABLE** | **NOT WALKED** | unknown | **DECLARED-ABSENT** — `reason:` records no `VISION.md`, no `CLAUDE.md`, no deploy record |
| 8 | `win-tooling` | `pre-deploy` (`:128-129`) | **absent from the registry** | n/a | **NOT OBSERVABLE** | **NOT WALKED** | unknown | **DECLARED-ABSENT** — `reason:` present |

### 2a. Two structural readings that fall out of the table

**(i) The parity checker walks at most 3 of 9 declared members.** Roles are hub ×1 + consumer ×2 +
pre-deploy ×6; `fleet_parity.py:1734` computes `walked` as *"role != pre-deploy"*. So every
"fleet parity" verdict is a statement about the hub and two consumers. This is the same shape the
`[#490]` comment already called out for *membership* (`parity-surfaces.yaml:110-115` — "every
'fleet parity GREEN' verdict was a claim about five repos wearing the word 'fleet'"); `[#490]`
fixed the **map** to 9/9 but the **walk** is still 3/9. The declared-absence `reason:` machinery
makes the 6 skips honest, which is exactly why this is a scope statement and not a defect.

**(ii) Where parity IS measurable, it is good.** All three observable repos carry the methodology
floor **byte-identical** to each other and to the hub's own source-of-truth hash
(`templates/child-methodology-floor.sha256` = `4d268f329a7edc8dc95a1c8fded9bdf8244ad8de60be69bf8e250a9b15a8111f`).
Both walked consumers carry a well-formed `.methodology.yaml` with mandatory reasons and
time-boxed `review_date`s. The hub has **no** `.claude/CLAUDE-FLOOR.md` of its own — that is
correct, not a gap: `.claude/methodology-roster.md` states the roster "includes components (e.g.
the floor) the hub itself does not install."

## 3. The `[#293]` runbook column, read post-correction

`BACKLOG.md:23` carries **two** corrections to `[#293]`, and applying only the first is what makes
the row look like a simple 0/N gap:

1. **Denominator ruled 8, not 6** (phase-1 integration R6): *"ADR-104's declared non-hub members;
   governance outranks row prose, so read '0 of 6' above as **0 of 8**."*
2. **The row is `OPERATOR-GATED, not executed`** — lane Q merged `dce393ec` and advanced it **by
   zero by design**, because *"the Done-when needs consumer-repo writes nothing authorised."*

Measured against remote HEAD: **0 of the 3 observable repos carry `docs/handoffs/README.md`, and
none carries a `docs/handoffs/` directory at all.** The 5 unobservable rows cannot be measured,
so the live figure is **0 of 3 measured, 0 of 8 claimable**.

**But the count is the wrong question**, which is F1.

## 4. Seeding readiness for lane k

The question asked: *branch protection? PR conventions? anything that would block a runbook PR?*

| Repo | Remote for a PR? | `main` protected | PR conventions observed | Blocking verdict for lane k |
|---|---|---|---|---|
| `ai-council` | yes (public) | **not measurable** — API scope denied (`list_branches` → *"not configured for this session"*); git-proxy clone worked, GitHub API did not | **No** `.github/`, **no** PR template. `CONTRIBUTING.md` present. Merge history is local `--no-ff` branch merges, **no PR numbers** | **BLOCKED — target forbidden (F1)** |
| `corp-monorepo` | yes (private, attached) | **`protected: false`** on `main` (measured, `list_branches`); only 2 branches | **No** PR template. `.github/` has 2 workflows (`nightly-conformance-triage.yml`, `tach.yml`). HEAD `fd3325e` is `…(#52)` → **does use PRs** | **BLOCKED — target forbidden (F1)** |
| `corp-sca-time-automation` | yes (public) | not measurable (same API-scope limit) | **No** `.github/`, no PR template, `CONTRIBUTING.md` present. Local `--no-ff` merges only | **BLOCKED — target forbidden (F1)** |
| `corp-ops` | **no reachable remote** | n/a | n/a | **BLOCKED — cannot open a PR at all** |
| `demo-prep` | **no reachable remote** | n/a | n/a | **BLOCKED — cannot open a PR at all** |
| `life-architect` | **no reachable remote** | n/a | n/a | **BLOCKED — cannot open a PR at all** |
| `terminal-setup` | **no reachable remote** | n/a | n/a | **BLOCKED — cannot open a PR at all** |
| `win-tooling` | **no reachable remote** | n/a | n/a | **BLOCKED — cannot open a PR at all** |

**Seeding-ready: 0 of 8**, and the two blocking reasons are independent — either alone is sufficient:

- **5 of 8** have no remote this session can reach, so no PR can be opened regardless of content.
- **8 of 8** are blocked on content: the artifact `[#293]` would seed is the one artifact a standing
  ruling forbids child repos to carry (F1). This blocks the 3 reachable repos too.

Two secondary notes, neither of which changes the verdict: branch protection is **not** a blocker
where measurable (`corp-monorepo`'s `main` is unprotected), and the fleet's dominant workflow is
**local `--no-ff` branch merges, not GitHub PRs** — only `corp-monorepo` shows PR-numbered commits.
A lane framed as "open a runbook PR" mismatches how 2 of the 3 reachable repos actually take changes.

## 5. Findings — the top 3 silent divergences

### F1 — `[#293]`'s Done-when requires creating the exact directory a standing ruling forbids

**Severity: HIGH.** This is the finding that reframes the whole row.

`BACKLOG.md:23` requires *"each onboarded consumer carries the seeded runbook"*, and
`scripts/seed_runbook.py:24` writes **only** `<target>/docs/handoffs/README.md` (`:42`,
`_RUNBOOK_REL = Path("docs") / "handoffs" / "README.md"`).

`docs/audits/2026-07-08-census-amendment-docs-handoffs-ruling.md:25-28` rules, architect-ratified:

> **ADR-60 / ADR-42 WIN.** Child repos do **NOT** create a local `docs/handoffs/`. Handoffs are
> centralized in `.dev-knowledge` — this is **intended divergence, not drift**. […] `docs/handoffs/`
> is **removed** from any child-repo `docs/` target.

and at `:45-52`:

> ai-council's absence of `docs/handoffs/` is **CONFORMANT** (intended divergence); no ai-council
> action is owed on this axis. […] Any runbook / onboarding surface that names `docs/handoffs` as a
> child-repo target **is stale and must read `docs/intake`-only.**

**Therefore the measured "0 of 8 seeded" is not a gap — it is conformance**, and executing `[#293]`
as written would push all 8 members *out* of conformance in one move.

**Why this is silent.** The divergence is between two hub governance surfaces, and nothing gates
their agreement. `[#293]` was **un-deferred 2026-08-09** and **denominator-ruled to 8** at phase-1
integration — both *after* the 2026-07-08 ruling, and neither cites it. Meanwhile `[#303]`
(`BACKLOG.md:131`) is **open** and already names this exact hazard — *"a literal seed creates the
exact dir ADR-36 forbids"* — and lists `#293` as its own kill-candidate. The contradiction is
recorded in three places and reconciled in none.

**Proposal (not executed):** `[#303]` is the prerequisite, not a sibling — lane k should be gated
behind it, or `[#293]`'s Done-when re-scoped to `docs/intake`-only per the ruling's `:50-52`
instruction. This finding is offered to the operator; no row was touched.

### F2 — `corp-sca-time-automation` carries live methodology surfaces that no contract describes and no checker walks

**Severity: MEDIUM-HIGH.** The clearest true *silent* divergence in the fleet.

The repo demonstrably carries: `.claude/CLAUDE-FLOOR.md` (byte-exact to the hub source hash),
`.claude/CLAUDE-FLOOR.md.sha256`, `.claude/check_floor_hash.py`, an active `floor-hash-verify`
pre-commit hook, and `.claude/rules/{code-standards,python-env,testing}.md`.

Yet:
- its role is `pre-deploy` (`parity-surfaces.yaml:109`) → `fleet_parity.py:527` renders it
  **`"pre-deploy: not walked"`** and skips it;
- `deployed-versions.yaml:46-49` records `null` on all three fields — no version, no date, no tag;
- **it has no `.methodology.yaml` at all**, so there is no file in which a divergence *could* be declared.

The three surfaces agree it is "unonboarded" while the tree says it is partially onboarded. Only
`ecosystem/registry.md` hints otherwise, in prose, in a status cell: *"registered · unonboarded
**(floor-carrying)**"*. That parenthetical is the sole record that this repo carries methodology
material — and it is not machine-read by anything.

Its last methodology touch is **2026-06-08 `df59f31`** (the original ADR-78 floor adoption), **69
days ago**. If the floor were revised hub-side, nothing in the fleet machinery would report this
repo as stale, because nothing walks it. It happens to be current today; that is luck, not a gate.

### F3 — the hub's live manifest v1.4.0 has no release tag, so the deploy ceiling cannot move

**Severity: MEDIUM.**

`git ls-remote --tags origin` on the hub returns exactly: `archive/drafts-2026-07-07`, `v1.0.0`,
`v1.2.0`, `v1.3.0`, `v1.3.1`. There is **no `v1.4.0` tag** — and no `v1.1.0` tag either, though
`deploy/manifest-v1.1.0.yaml` exists.

`deploy/manifest-v1.4.0.yaml:9-10` states the constraint itself:

> The tool's preflight requires that tag to resolve before `--execute`, so **v1.4.0 must be tagged
> by the operator before the real deploy runs.**

So the hub's newest declared corpus is **unreleasable**: `deployed-versions.yaml` can never record
a consumer at 1.4.0, and the highest attainable consumer state is v1.3.1 — which `ai-council`
already holds. `ai-council` is simultaneously **fully current** (against tags) and **one minor
behind** (against manifests), depending on which surface you read.

**Why this is silent.** Nothing checks manifest↔tag agreement. `deployed-versions.yaml` is
written by the deploy runbook and read by `check_deployed_methodology_version`, but no organ
asserts that the newest `deploy/manifest-v*.yaml` has a corresponding tag. A manifest can sit
declared-but-unreleased indefinitely and every version check stays green.

### Secondary observations (not in the top 3)

- **`ai-council` `dep-pytest-xdist` declaration expires TODAY** — `review_date: 2026-08-16`. Its own
  text says the review must decide "whether to pin `pytest-xdist>=3.8` in pyproject […] or keep it
  ambient." Due now, in the consumer's tree, not the hub's.
- **The `.vscode` declarations in both consumers carry `review_date: 2026-08-26`** — 10 days out, and
  both are tied to the same open hub ruling (fleet-parity register e1).
- **`vscode-boundary-decoration` is DECLARED-UNTIL-MECHANISM in both consumers**, adopted by hand
  ahead of a carrier that `manifest-v1.4.0.yaml` still marks `implemented: false`. The declarations
  are correct and time-boxed; the point is that F3's untagged v1.4.0 is what keeps the carrier from
  ever shipping to retire them.

## 6. What this sweep did NOT do

- **No consumer repo was written to.** No branch, no commit, no push, no PR, no issue, no comment.
  `corp-monorepo` was attached read-only; the other two were cloned over the public git proxy.
- **No hub row was advanced, closed, or filed.** `[#293]` and `[#303]` are discussed, not touched.
- **`fleet_parity.py` was not run.** It reads local sibling working trees that do not exist in this
  container; running it here would have produced a false result, not a partial one.
- **5 of 8 rows are unmeasured, not measured-and-clean.** Every cell for `corp-ops`, `demo-prep`,
  `life-architect`, `terminal-setup`, and `win-tooling` is a hub-side contract reading only.

---

**in-parity 2/8 · seeding-ready 0/8**

> *in-parity 2/8* = `ai-council` + `corp-monorepo`, the only two members both walked by the fleet
> machinery and verified against it this run. Of the remaining 6: **1 divergent-silent**
> (`corp-sca-time-automation`, F2) and **5 not assessable** (no reachable remote; hub-side records
> read but tree state unverified). It is **not** a claim that 6 members failed.
>
> *seeding-ready 0/8* = every member is blocked, on two independent grounds: 5 have no reachable
> remote, and all 8 — including the 3 reachable ones — would have to receive the one artifact the
> 2026-07-08 ruling forbids child repos to carry (F1).
