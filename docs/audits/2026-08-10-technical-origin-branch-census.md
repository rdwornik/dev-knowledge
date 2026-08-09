# Origin branch census — every ref on `origin`, classified

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** origin-branch-census
- **Seat:** CC (Opus 5), CLOUD lane N-C, branch `claude/night-batch-cloud-lanes-a4mpkp`
- **Posture:** **nothing deleted, nothing merged.** Deletion candidates are reported, never
  executed — standing operator ruling. Only this lane's own report branch was pushed.

## Run conditions — hand-run, not gate-passed

Cloud container, `[#453]` conditions confirmed: `uv 0.8.17` vs the `==0.11.19` pin
(`pyproject.toml:25`) → `uv run --locked` hook entries refuse, **no gate fired**;
`.git/hooks/` samples only; `audit.py health` structurally unpassable here.

**The unshallow mattered for this lane specifically.** The clone arrived shallow;
`git fetch --unshallow` ran first (4777 commits). Every ahead/behind count, ancestry test and
date below is measured against full history — **not** a floor. A shallow clone would have
reported ancestry wrongly for exactly the branch that matters most here.

Filename pre-verified against `validate_hermetization.classify()` (`None`) and
`gen_audit_index.py`'s parser.

## Scope, and one correction to the premise

Enumerated with `git ls-remote --heads origin` against
`https://github.com/rdwornik/dev-knowledge`, cross-checked against `refs/remotes/`.

**`origin` carries 8 heads: `main` + 7 others.** The brief's premise — *"a large and growing
set of branches"* — is **half right and worth stating precisely: the set is small (7 non-main)
but it is genuinely growing, and it grows by one every night.** Six of the seven are
machine-produced nightly artefacts from the last seven days. The perception of a large set is
the perception of a *steady accumulation with no reaper*, which is a real problem with a small
current number.

**Satellite repos: not reachable.** The brief asks for each satellite via `git -C`. `ls ..`
shows no sibling repos — a cloud clone is single-repo by construction, and this session's GitHub
scope is `rdwornik/dev-knowledge` alone. **The satellite half of this census is UNDONE, not
clean.** It needs a run from the operator's machine.

**One anomaly, recorded:** `refs/remotes/origin/claude/night-batch-cloud-lanes-a4mpkp` exists
locally at `e67fb8db` but is **absent from `git ls-remote`** — the harness pre-seeded the
tracking ref before the branch existed on `origin`. It is this lane's own branch and is excluded
from the census below; it will exist on `origin` once this report is pushed.

---

## The table

| Branch | Tip | Last commit | Ahead | Behind | Ancestor of `main`? | Touched files | Class |
|---|---|---|---|---|---|---|---|
| `automation/fleet-audit` | `d2036202` | 2026-08-09 · robdwornik | 163 | 4777 | **no — disjoint** | `docs/`, `ecosystem/` (own tree) | **UNIQUE WORK** |
| `claude/conformance-2026-08-03` | `5693919b` | 2026-08-03 · Claude | 1 | 463 | no | 1 digest | **PROTECTED + UNIQUE** |
| `claude/conformance-2026-08-04` | `3d083660` | 2026-08-04 · Claude | 1 | 406 | no | 1 digest | **PROTECTED + UNIQUE** |
| `claude/conformance-2026-08-05` | `19fc2371` | 2026-08-05 · Claude | 1 | 354 | no | 1 digest | **PROTECTED + UNIQUE** |
| `claude/conformance-2026-08-07` | `cee4472b` | 2026-08-07 · Claude | 1 | 242 | no | 1 digest | **PROTECTED + UNIQUE** |
| `claude/conformance-2026-08-08` | `f18419fc` | 2026-08-08 · Claude | 2 | 161 | no | digest + audits index | **PROTECTED + UNIQUE** |
| `claude/conformance-2026-08-09` | `ad1822c9` | 2026-08-09 · Claude | 1 | 54 | no | digest + audits index | **PROTECTED + UNIQUE** |

**Counts per class: MERGED 0 · UNIQUE WORK 7 (6 of them also PROTECTED) · PROTECTED 6 ·
UNDETERMINED 0.**

**Not one branch on `origin` is safe to delete on merged-content grounds.** `git merge-base
--is-ancestor <tip> origin/main` is **false for all seven**. There is no cleanup to authorise
here — which is itself the answer to the question that prompted the lane.

## The protecting clause, quoted

`.claude/rules/git-discipline.md:17-20`:

> *"A branch merged into main and pushed is deleted in the same step, without separate operator
> authorization. **Exceptions exist only by EXPLICIT PROTECTION (currently `claude/conformance-*`)**;
> silence is not protection. A merged branch left alive is a defect, not a pending decision."*

and its verify line, `:27-28`:

> *"verify: `git branch --merged main` lists nothing but `main` and explicitly protected branches
> (`claude/conformance-*`)."*

Quoted rather than inferred, as the brief directs. **All six `claude/conformance-*` branches fall
squarely inside this protection.** Note the protection is written for the *merged* case; these
six are unmerged, so they are protected **and** carry unique content — belt and braces.

`automation/fleet-audit` is **not** covered by any explicit protection clause. Its prefix was
admitted to the branch-naming enum on 2026-08-06 (`3879d28b`, register
`protocols/STANDING_RULINGS.md` B5, CLAUDE.md §12 v2.52), but admission to the *naming* enum is
not deletion protection, and I found no clause granting it any. **Silence is not protection** —
per the rule above, that cuts against it. It is retained here on **content** grounds, not rule
grounds.

## The two findings that matter

### 1. `automation/fleet-audit` is an ORPHAN branch, not a stale one

`git merge-base origin/main origin/automation/fleet-audit` → **no common ancestor.** It has its
own root commit `333ae85d`; `main`'s root is `b635615f`. The two histories have never touched.

That explains the shape the brief noticed: *"163 ahead and never merged"* is exactly right, and
the reason is structural, not neglectful. The `4777 behind` figure is not a staleness
measurement — it is the entire history of `main`, which this branch simply does not contain.
`git diff --name-only origin/main...HEAD` returning zero files is an artefact of the same
disjointness, **not** evidence that its content is on `main`.

Content: 163 commits, 2026-06-15 → 2026-08-09, uniformly
`chore(routine/fleet-audit): record <date> baseline`. Tree holds only `docs/` and `ecosystem/`.
This is a **nightly recorder's append-only data branch** — a deliberate orphan pattern, correctly
built. It should never be merged; merging it would drag a disjoint root into `main`'s spine.

**Disposition: RETAIN. Do not merge, do not delete.** What is missing is not cleanup — it is a
*written* protection clause, because it currently survives only because nobody has run the
reaper against it.

### 2. Six nightly conformance digests have never reached `main` — and the stream stopped 2026-08-02

This is the finding I did not expect and the one worth the architect's attention.

`main` carries **19** `*-conformance-nightly-digest.md` files under `docs/audits/`. The most
recent is **`2026-08-02`**. Every digest since — 08-03, 08-04, 08-05, 08-07, 08-08, 08-09 — is
**ABSENT FROM `main`** and exists only on its own unmerged branch (verified per file with
`git cat-file -e origin/main:<path>`; all six report absent).

So the nightly conformance organ has been running and producing output for a week, and **none of
that output has landed on the canonical surface.** The digests are not lost — each is safe on its
branch — but they are invisible to anything that reads `docs/audits/` on `main`, including
`gen_audit_index.py`, which is why the generated index shows no sign of them.

**`2026-08-06` has no branch at all.** Either the job did not run that night, or it ran and
failed to push. I cannot distinguish those two from here, and I am not going to guess: the run
logs are outside this clone.

The 08-08 branch is worth one extra note — its second commit is
*"amend 2026-08-08 conformance digest — all 5 findings killed by skeptic"*, i.e. real
adjudication work happened on that branch and is stranded with it.

**Disposition: PROTECTED, retain, but the stranding is a defect that outlives the branches.**
The branches are doing their job; the merge step is missing.

## Proposed disposition per branch

| Branch | Proposed disposition | Basis |
|---|---|---|
| `automation/fleet-audit` | **RETAIN — and give it a written protection clause** | orphan-by-design nightly recorder; content genuinely unique; currently protected by nothing |
| `claude/conformance-2026-08-03` | **RETAIN** (explicitly protected) — decide whether its digest lands on `main` | `git-discipline.md:19` |
| `claude/conformance-2026-08-04` | **RETAIN** — same | same |
| `claude/conformance-2026-08-05` | **RETAIN** — same | same |
| `claude/conformance-2026-08-07` | **RETAIN** — same | same |
| `claude/conformance-2026-08-08` | **RETAIN** — same; carries an amendment commit | same |
| `claude/conformance-2026-08-09` | **RETAIN** — same | same |

**Zero deletion candidates.** Not a single branch on `origin` meets the merged-content test, so
this census proposes no deletions at all.

## Needs a ruling

1. **Do the six stranded digests land on `main`?** Six nights of conformance output sit on
   unmerged branches, and the `docs/audits/` stream on `main` stops at 2026-08-02. Three
   readings, and I cannot choose between them: (a) the digests are *meant* to stay on branches
   and `main`'s 19 are the historical exception, (b) the merge step broke around 08-03 and this
   is a week-old outage, (c) they should be merged in a batch now. **If (b), this is the finding
   with the shortest fuse in tonight's batch** — the organ is running and nobody is reading it.
2. **What happened on 2026-08-06?** No branch exists. Job didn't run, or ran and didn't push. Not
   determinable from inside the repo.
3. **Does `automation/fleet-audit` get a written protection clause?** It is an orphan data branch
   with 163 unique commits and **no** rule protecting it, in a repo whose rule says *"silence is
   not protection"* and mandates same-step deletion of merged branches. It survives on the
   accident that it is unmerged. One line in `git-discipline.md` naming `automation/fleet-audit`
   (or `automation/*`) alongside `claude/conformance-*` would close that gap.
4. **Is the retention policy for `claude/conformance-*` unbounded?** The protection clause names
   the pattern with no expiry, and the set grows by one branch per night. At the current rate
   that is ~365 branches a year, each holding one file. The clause is doing what it says; the
   question is whether "protected" was meant to mean "kept forever". **This is the actual
   mechanism behind the operator's impression of a growing set** — not that any branch is stale,
   but that nothing ever removes one.
5. **Who runs the satellite half?** This census covers `origin` for the hub only. The satellites
   are unreachable from a cloud clone and their branch sets are **unexamined, not clean.**
