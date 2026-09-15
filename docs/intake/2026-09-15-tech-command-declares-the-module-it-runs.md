---
intake-id: 97
status: DRAFT
origin: lane `lane-z-11-three-repo-comparison`, 2026-09-15 — measured against github/spec-kit command frontmatter and its parity tests; see `docs/audits/2026-09-15-technical-lane-z-11-comparison-matrix.md` row G-2
consumed-by:
---

# A command file does not declare the module it runs, so no machine can join the two

## Problem / motivation

A command in this repo names its executable in **prose**. `.claude/commands/preflight.md`
carries frontmatter of exactly two keys — `name` and `description` — and the module it
invokes appears below, inside a fenced bash block:

```
uv run --locked python scripts/preflight_contract.py <contract-or-prompt-file>
```

A human reads that correctly. Nothing else can. The edge from `/preflight` to
`scripts/preflight_contract.py` exists only as text a reader interprets, so no generator,
census or gate can traverse it without parsing prose.

This is load-bearing right now, on two live surfaces:

- **ADR-119** (Accepted, 2026-09-13) ruled that *"a command file counts as a `[#664]`
  wiring surface only while invocations are recorded — adoption decays, it is not
  conferred."* Deciding whether a command is adopted requires knowing what a command
  *reaches*; today that is prose.
- **The `[#664]` orphan census** asks what nothing triggers, across five wiring surfaces.
  Intake `#94` already records the consequence: a command file is none of those five, so
  *"every operator-invoked organ in this repo reads as an orphan by construction"* — 21 of
  37 disposition rows on the 2026-09-13 census. A declared command→module edge does not
  settle the adoption question, but it supplies the join the census currently has to
  approximate.

A comparable project makes this edge data. In `github/spec-kit`, a command's frontmatter
carries a structured `scripts:` key naming the executable per shell:

```
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireSpec -RequireTasks
  py: scripts/python/check_prerequisites.py --json --require-spec --require-tasks
```

Because it is data, spec-kit can and does test it: `tests/test_command_template_py_scripts.py`
and `tests/test_check_prerequisites_python_parity.py` assert the declared invocations agree.
Our equivalent assertions cannot be written at all, because there is nothing to read.

The drift this permits is ordinary and silent: a module is renamed, the command's prose
still names the old path, and the failure surfaces when the operator runs the command.
`derived-copies-rebind` already guards the analogous case for registered sources — *"a
staged registered source whose derived copy did not move"* — so the repo has both the
pattern and the appetite; commands are simply outside it.

## Scenarios (+1 view)

- As the **`[#664]` census**, I enumerate what nothing triggers. I cannot see command files
  as wiring, so I report a standing majority of organs as orphans and every reader must be
  told to discount the register.
- As the **architect applying ADR-119**, I ask what a given command reaches before ruling on
  its adoption. The answer is in prose, so the ruling rests on a hand-read.
- As a **module author** renaming `scripts/foo.py`, nothing tells me a command still names
  the old path. The operator finds out by running it.
- As **`gen_claude_rosters.py`**, I already parse this frontmatter for `name` and
  `description`. A third key costs me nothing and gives every downstream surface a join.

## Functional requirements

- **Must:** a command file declares, as machine-readable data, the repo module(s) it
  invokes.
- **Must:** a declared target that does not exist is detectable — the point of the
  declaration is that it can go stale and be caught.
- **Should:** the declaration is reachable by the existing roster generator and by the graph
  (`file_purpose_graph.py`), so the edge joins the surfaces that already ask these
  questions rather than starting a sixth register.
- **Should:** a command that legitimately invokes nothing can say so explicitly, so absence
  is a declaration rather than an omission.
- **Could:** the declared invocation and the prose example are asserted to agree, which is
  the parity test spec-kit can write and we currently cannot.

## Acceptance criteria (ex-ante)

1. For every file in `.claude/commands/`, a machine can list the repo modules that command
   invokes, without parsing prose.
2. Renaming a module that a command declares, without updating the command, is detected.
3. A command that invokes no module is distinguishable from one whose declaration is
   missing.
4. `[#664]`'s census and ADR-119's adoption question can both consume the result — this is
   an input to those, not a competing answer.

## Non-goals

- **Re-opening ADR-119.** Adoption still decays and is still evidenced by recorded
  invocations. This supplies the *join*, never the adoption verdict, and must not be read as
  conferring adoption on a command because it declares a target.
- Changing what any command does.
- A sixth wiring register. If this cannot land on an existing surface it is probably the
  wrong shape.
- Multi-shell invocation triplets. spec-kit needs `sh`/`ps`/`py` because it ships to three
  shells; we run `uv run --locked python` and copying the triplet would import a problem we
  do not have.

## Impact sketch (4+1 lite)

- **Logical:** an edge that exists in prose becomes an edge in data.
- **Process:** the census's input list gains a surface it currently approximates.
- **Development:** frontmatter across 8 command files, the roster generator, one checker.
- **Physical:** none.

## Open questions

- What is the key's shape — a single string, a list, or a structured record? Technical.
- Does this land on `file_purpose_graph.py` as a new edge kind, on the census input list, or
  both? Technical, and it decides whether this is small or structural.
- Do the deploy-carried commands (`/review-closures`, `/ship`, `/boot-session`) carry the
  same declaration, and does that change the manifest? Technical — touches `deploy/`.

## Status

DRAFT — filed by lane `lane-z-11-three-repo-comparison`, 2026-09-15. Not triaged.
