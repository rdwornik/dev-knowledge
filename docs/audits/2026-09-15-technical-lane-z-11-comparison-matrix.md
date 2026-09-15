# lane-z-11 — the gap matrix, read-only

> **Step 2 of `lane-z-11-three-repo-comparison`.** Slots and witness commits:
> `2026-09-15-technical-lane-z-11-comparison-slots.md`. Dispositions — what we adopt and
> what we refuse, with reasons — `2026-09-15-technical-lane-z-11-comparison-dispositions.md`.
>
> **Reading rule.** Every row resolves to a **concrete surface in THIS repo that would
> change**. A row whose right-hand column is an aspiration rather than a path is not a gap,
> it is an opinion, and it does not belong here. Rows are graded `GAP` (they have it, we do
> not), `PARTIAL` (we have a narrower version), `OWNED` (we have it, recorded so it is not
> re-proposed) or `DISCARDED` (the measurement did not survive scrutiny).

Shorthand: **SK** = `github/spec-kit` · **BM** = `bmad-code-org/BMAD-METHOD` ·
**SP** = `obra/superpowers`.

---

## The matrix

|ID|Axis|What the comparison repos do|What this repo does|Surface here that would change|Grade|
|---|---|---|---|---|---|
|G-1|Reference validation over the **committed corpus**|BM `tools/validate_file_refs.py` resolves cross-file references across all source files, refuses absolute-path leaks, warn-only by default|`scripts/preflight_contract.py` owns the predicates but its input is ONE contract handed to it; `check_doc_code_edge` covers 4 declaration docs and one annotation form, fail-soft|`scripts/preflight_contract.py` (a corpus mode) or a sibling module + a `.pre-commit-config.yaml` row|**GAP**|
|G-2|Command → executable join is **data, not prose**|SK command frontmatter carries `scripts: {sh, ps, py}`; `tests/test_command_template_py_scripts.py` and `test_check_prerequisites_python_parity.py` assert the three agree|`.claude/commands/*.md` frontmatter is `name` + `description` only; the module a command runs sits in a fenced bash block in prose|`.claude/commands/*.md` frontmatter · `scripts/gen_claude_rosters.py` · the `[#664]` census input list · ADR-119|**GAP**|
|G-3|Skill-shape validator|BM `tools/validate_skills.py` — 10 deterministic rules (name format, name==dirname, description quality, body present, no time estimates)|No validator asserts skill frontmatter shape; `.claude/skills/` holds two skills|a new validator + a pre-commit row|**GAP** (disposed REJECTED — see dispositions R-4)|
|G-4|Per-provider **behavioural** tests|SP ships a `tests/` directory per provider: `claude-code`, `codex`, `devin`, `hermes`, `kimi`, `opencode`, `pi`, `antigravity`|`scripts/check_provider_registry.py` asserts the nine seams' **strings** agree; `ecosystem/parity-surfaces.yaml` declares surfaces|`ecosystem/parity-surfaces.yaml` · `tests/test_provider_registry.py`|**PARTIAL**|
|G-5|Cross-artifact consistency **before** implementation|SK `analyze` — a non-destructive consistency and quality pass over spec + plan + tasks, run after generation and before implement|`coherence-nudge` is **non-blocking** (`CLAUDE.md` §9) and fires on a spec version-bump signal, not on artifact content; `check-against-spec` is operator-invoked|the `coherence-nudge` hook · `_SPEC_REGISTRY` · the `check-against-spec` skill|**PARTIAL**|
|G-6|Structured ambiguity resolution before planning|SK `clarify` — up to 5 targeted questions on under-specified areas, answers encoded **back into the spec**|ADR-108 §A routes questions by class (operator functional / architect technical) and `/boot-session` surfaces OPERATOR ASKS, but nothing **generates** the question set from a frozen contract|`/lane-boot` (the V-2 budget) · `preflight_contract.py --freeze` predicates|**PARTIAL**|
|G-7|A predicate that **cannot look** must say so|—|`preflight_contract.py`'s `sha` leg reports "not present in this repo's object store" for a SHA that is merely outside a shallow clone's depth|`scripts/preflight_contract.py` sha leg|**DISCARDED as a corpus measurement, kept as an organ finding** — see below|
|G-8|One-command consumer onboarding|SK ships an installable CLI (`src/specify_cli`): `specify init`, `specify check`|`templates/consumer-onboarding-runbook.md` + `INSTALL.md` are prose; deploy is manifest + carriers|`deploy/` + the runbook|**GAP** (disposed REJECTED — see dispositions R-1)|
|G-9|One aggregated "run what CI runs" entry point|BM `tools/quality.py` — "run every check CI runs, in the same order", pre-commit over the whole tree then the docs-site scripts|`audit.py health`, pre-commit and pytest are invoked separately; the `verify` skill runs pytest + ruff + git-status|the `verify` skill · `scripts/audit.py`|**PARTIAL**|
|G-10|Corpus versioning and release stamping|BM `tools/stamp_release.py` + CHANGELOG + `web-bundles/`; SK `bundles/`, `presets/`, releases|`deploy/manifest-v1.5.0.yaml` · `ecosystem/deployed-versions.yaml` · ADR-91|— (nothing changes)|**OWNED**|
|G-11|Extension points declared in data, with an explicit no-silent-skip rule|SK `.specify/extensions.yml` + `hooks.before_analyze`; the command text says that if the YAML cannot be parsed the agent must **tell the user** rather than skip silently|Same doctrine, stated harder: `.claude/settings.json` reasons explicitly about fail-closed vs fail-OPEN posture per guard, and the `[#727]` guard is fail-open **by design**|— (nothing changes)|**OWNED**|
|G-12|Corpus internationalisation|BM ships docs in `cs/`, `fr/`, `ko-kr/`, `vi-vn/` plus `README_CN/KR/VN`|English-only by operator preference|— (nothing changes)|**GAP** (disposed REJECTED — R-2)|
|G-13|Tasks exported to a tracker|SK `taskstoissues` turns generated tasks into GitHub issues|`tasks/` are files; `BACKLOG.md` is generated from them with a byte-exact round-trip (ADR-109)|`tasks/` · `scripts/gen_task_tree.py`|**GAP** (disposed REJECTED — R-3)|
|G-14|A rendered documentation site|BM `docs-site/` (Astro, with a sidebar validator in `quality.py`)|`ecosystem/conformance.html`; dashboards-as-local-HTML is already an intake (`#9`)|— (already in the funnel)|**OWNED**|
|G-15|Process enforced at the point of use by a skill|SP `test-driven-development`, `verification-before-completion`, `writing-plans`, `executing-plans`, `dispatching-parallel-agents`, `using-git-worktrees`|TDD is an ADR-108 §B **build-arc** standard — a blanket mandate was rejected by Council; the `verify` skill and `/lane-integrate`'s refuse-to-finish checklist cover the rest|— (nothing changes)|**OWNED**|

---

## G-1, measured rather than asserted

The gap is scope of application, not capability, so it can be measured with the organ this
repo already owns. `preflight_contract.verify()` was imported as a library and pointed at
127 committed files (`*.md`, `protocols/`, `docs/decisions/`, `ecosystem/`,
`.claude/commands/`). Read-only; nothing was written and no gate was run.

```
files scanned                    127
locator claims extracted       4,646
unresolved (raw)               4,096
```

**That raw number is not a finding, and reporting it as one would be the error this repo
calls restating a count.** It decomposes into three classes, only one of which survives:

```
sha                 3,774 / 3,894   DISCARDED -- shallow-clone artifact (G-7)
backlog-id            282 /   499   FALSE POSITIVE by calibration -- see below
file-line              39 /   252   of which 37 are bare prose filenames
                                     and 2 are REAL
```

- **`sha` — discarded.** This session's checkout carries `.git/shallow` and 275 commits, so
  a historical SHA is absent from the object store for a reason that has nothing to do with
  the citation being wrong. The leg cannot be evaluated here at all.
- **`backlog-id` — a calibration mismatch, not a defect.** The predicate asks "is this id
  **currently OPEN** in `BACKLOG.md`". That is the right question for a contract at freeze
  time and the wrong one for the corpus, where an immutable ADR citing a long-closed row is
  a *correct* citation. A corpus mode needs a closed-id-tolerant predicate.
- **`file-line` — 37 of 39 are prose, 2 are real.** The 37 are bare filenames carrying a
  colon-number that the extractor reads as a locator: `gotchas.md:333`, `REVIEW.md:85`,
  `SUPPLEMENT.md:133`, and — decisively — `huggingface.co:443`, a host and port. A corpus
  mode must restrict the leg to **repo-relative paths that resolve**.

The two that survive are the same citation in two places:

```
protocols/STANDING_RULINGS.md:4074  ->  templates/handoff/v5/PROBES.md.tmpl:96
JOURNAL.md:6171                     ->  templates/handoff/v5/PROBES.md.tmpl:96
live:  templates/handoff/v5/PROBES.md.tmpl is 77 lines
```

`JOURNAL.md` is append-only and historical — the entry was true when written and must not
be edited. **`protocols/STANDING_RULINGS.md` is a living governing document**, and it
carries a locator that does not resolve. That is precisely the class `CLAUDE.md` §4 names
as *"the most-recorded executor failure in the 2026-08-21 governance-drift audit"*, sitting
in a file a session is told to obey, defended by an organ that — as `/preflight`'s own
frontmatter says — is *"wired into no gate"*.

**Yield, stated honestly:** one live broken locator across 127 files. That is a *low* yield,
and it is an argument for a cheap warn-only check rather than for a hard gate. It is
recorded at that strength in the dispositions file.

## G-7 — the organ finding this lane produced by accident

The discarded measurement is itself worth keeping. `preflight_contract.py` renders a SHA
that is outside a shallow clone's depth as `not present in this repo's object store` — a
verdict indistinguishable from "this SHA is wrong". In a full clone that is correct. In
**every cloud lane**, which is exactly where a shallow clone lives, it is a false refusal
at a rate of 3,774 in 3,894.

The organ is read-only and ungated today, so nothing breaks. The finding is about what
would happen on promotion: ADR-119 and the `[#664]` census are actively asking which
operator-invoked organs deserve wiring, and this one would fail closed for the wrong reason
in the substrate this very lane ran on.

This repo already holds the doctrine that answers it. `.claude/settings.json` reasons at
length about a guard that *"permits when it cannot run"* being *"declared enforcement
without enforcement"*, and the `[#727]` guard is fail-OPEN by design for the opposite
reason. The missing verdict here is the third one: **cannot evaluate**, distinct from both
pass and fail — which is the posture `preflight_contract.py` already implements for its own
internal errors, where exit 2 is kept distinct from exit 1 so that *"I could not look" stays
distinguishable from "I looked and it is wrong"*. The `sha` leg simply does not extend that
distinction to a shallow clone.

---

## Convergence worth recording

Three findings where an independent project reached this repo's answer. They are not gaps,
and they are recorded because convergence is evidence a decision is right — and because a
future reader comparing these repos will otherwise re-derive them as gaps.

1. **Adoption-first posture on a reference checker.** BM's `validate_file_refs.py` docstring:
   *"Default mode is warning-only (exit 0) so adoption is non-disruptive."*
   `preflight_contract.py`: *"ADOPTION FIRST: this is wired into NO gate."* Two projects,
   same organ, same posture, reached independently.
2. **Precision over recall on a corpus detector.** BM defers bare backticked filenames and
   template placeholders explicitly because they are *"indistinguishable from runtime-output
   mentions"*. `validate_doc_rot.py` states the same constraint in its own words —
   *"each precision-over-recall (one false positive kills adoption)"*. The 37 prose
   false-positives measured above are the same class both projects predicted.
3. **A parse failure must not be a silent skip.** SK's `analyze` instructs the agent to
   report an unreadable `extensions.yml` rather than skip its hooks; this repo's
   `.claude/settings.json` argues the same point down to the exit code.

---

**Lane:** `lane-z-11-three-repo-comparison` · **Substrate:** cloud (no gate run) · **Date:** 2026-09-15
