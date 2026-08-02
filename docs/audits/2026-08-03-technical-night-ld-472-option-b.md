# Night batch 2026-08-03 · lane L-D — [#472] option B dossier (amendment-shaped)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-03 · **Slug:** night-ld-472-option-b
- **Status:** PROPOSAL — read-only night batch, unattended. **RULING INPUT ONLY.** No repo file
  was edited, staged, committed, or generated. The three artifacts below are drafts for the
  operator/architect to accept, amend, or reject; none of them has been applied.
- **Base:** `main` = `c7628a3` (working tree clean at open and at close).
- **Method:** read-only. Every claim carries a live `path:line` or command output. `audit.py`
  and `validate_hermetization.py` were **imported** and called on read-only inputs from the
  scratchpad interpreter; no generator was run with `--write`, no `--force` anywhere.
- **Builds on:** `docs/audits/2026-08-02-technical-night-batch-lf-backlog-health.md:169-176`
  (lane L-F), which verdicted [#472] **verify-then-reword** and identified the surviving core:
  *"`resolve_fleet_members` was deliberately not widened (a named §2 ruling), which is the part
  of [#472] that plainly survives."* This dossier does **not** repeat that triage. It supplies
  the thing L-F stopped short of: the concrete option-B mechanism — anchor form, checker
  binding, migration order.

---

## Verdict

Option B is **buildable exactly as ruled, with one correction to the brief**: ADR-104 has **no
§15**. Its headings run §1–§5 (`ADR-104:21,33,47,78,93`); the fleet enumeration is at
**`ADR-104:15` — a line, not a section**. The `[#462]` module comment already reads it that way
(`scripts/audit.py:3200`: *"the constant can drift from ADR-104:15 silently"*). Every other
ruled constraint is supported by its cited source.

The mechanism is cheaper than the row implies. The repo has already built the hard half twice:
ADR-101's amendments are the standing precedent for *"a closed set lives as a script constant,
and an ADR amendment is the authority that grows it, in same-commit lockstep with a pinning
test"* (`ADR-101:155,207,213`). Option B adds the one thing that precedent lacks — a machine
check on the lockstep, so the ADR↔constant edge stops being upheld by discipline alone.

**No new persisted file is needed, and no registry authority is conferred**: the amendment is
read as an *authority to agree with*, never as the census's membership input. The constant stays
the value `classify_membership` receives (`scripts/audit.py:3339`).

---

## Constraint set as verified

**C1 — The declaration arrives as an APPENDED AMENDMENT to ADR-104 (the ADR-94 path); ADR-104
§15's body is NEVER edited.**
**SUPPORTED in mechanism · FLAGGED on citation.**
Mechanism, `ADR-94:24`: *"An ADR's **decision content remains frozen** — changed only by
superseding with a new file or by an appended in-file amendment marker, never edited in place."*
Restated at `CLAUDE.md` §5 item 3 (quoted verbatim inside `ADR-94:29`).
**FLAG:** there is no `§15`. Heading enumeration of the whole file returns
`## Context (11) · ## Decision (19) · ### 1 (21) · ### 2 (33) · ### 3 (47) · ### 4 (78) ·
### 5 (93) · ## Consequences (99) · ## Alternatives considered (107)`; the file is 113 lines.
The declaration is `ADR-104:15`. A repo-wide `grep "§15"` returns only `HANDOFF_PROCESS.md` and
PLAYBOOK/JOURNAL hits — none referring to ADR-104. Correct the locus before drafting, or the
amendment will cite a section that does not exist.

**C2 — The checker binds to the AMENDMENT'S ANCHOR (a stable machine-locatable anchor inside the
amendment).**
**CONSISTENT — no source cited, none contradicts.** This is a design constraint, not a doctrine
claim, so there is nothing to verify it *against*; nothing in ADR-94/104/109 or CLAUDE.md bars
it. It is well-served here: the repo parses **five distinct HTML-comment marker grammars** and
**zero** fenced-block info-string grammars (evidence under Artifact 1).

**C3 — NO new persisted file (ADR-109 §2/§9 bars it).**
**SUPPORTED, twice, verbatim.**
`ADR-109:87` (§2): *"**No new physical contract file is created in v1.** Schema v1 is a *model
over the existing sources*; a single persisted desired-state document, and the physical
retirement/freezing of absorbed sources, are per-surface migration decisions owned by the [#383]
waves."*
`ADR-109:265-266` (§9): *"- **A new persisted desired-state file in v1** — rejected (§2):
model-over-existing-sources first; physical consolidation is per-surface migration work with its
own contracts."*
**Scope note (precision, not a flag):** the bar is on a new *persisted desired-state / physical
contract* file **in v1**. It does not reach a test case or a leg inside an existing check —
which is why option B fits under it rather than around it. The `[#462]` comment already reasons
this way at `scripts/audit.py:3196-3198`: *"its option (c) collides with ADR-109 §2 ... A
constant needs no new file, no `SourceSurface` value and no loader change."*

**C4 — NO registry authority (the amendment is not a registry; it does not become a second
source of truth for membership).**
**SUPPORTED.** `ADR-109` amendment 2026-08-01, lines 382-384: *"**NOT changed —
`resolve_fleet_members` is not widened.** Resolving membership toward `deployed-versions.yaml`
is a **named §2 ruling**, not incidental code, and widening it revisits that ruling. It stays as
ruled; **[#472]** owns any future change."* Reinforced in code at `scripts/audit.py:3299-3300`:
*"`resolve_fleet_members` is NOT consulted and NOT widened: that resolution is a named ADR-109
§2 ruling and belongs to [#472]."*
Artifact 2 honours this by construction: the amendment is compared to the constant and never
substituted for it as the census input.

**Additional verified facts the artifacts rest on**

- The `[#462]` constant, verbatim, `scripts/audit.py:3203-3207`:
  `ADR104_FLEET_DECLARATION = (".dev-knowledge", "ai-council", "corp-monorepo", "corp-ops",
  "corp-sca-time-automation", "demo-prep", "life-architect", "terminal-setup", "win-tooling",)`
- Its self-declared open cost, `scripts/audit.py:3200-3202`: *"Its honest cost, named not
  claimed away: the constant can drift from ADR-104:15 silently. Closing that IS [#472]'s
  Done-when."* — i.e. the `[#462]` author already scoped this dossier's job.
- The live census passes today (run read-only this session):
  `PASS | 9 declared (ADR-104); 5 resolved members (deployed-versions); coverage registry-md
  9/9, index-yaml 6/9, deployed-versions 5/9, parity-surfaces 5/9, onboarding-rulings 4/9,
  state-dirs 0/9; declared-but-not-deployed: demo-prep [...]; life-architect [...];
  terminal-setup [registry-md]; win-tooling [...]`
- `VISION.md:107-112` states the same nine, attributed to ADR-104 — the second prose surface the
  row names. It is **out of scope for option B** as drafted (one anchor, one authority); binding
  VISION too would create the second source of truth C4 forbids.
- `ecosystem/doc-code-edge.yaml:148` has already anticipated this decision:
  *"membership_agreement ... Its rule is declared in ADR-104 ... **Admitting it would mean adding
  ADR-104 to `declaration_docs`, a separate ruling and not a side effect of landing a check.**"*
  This dossier is an input to exactly that separate ruling (see Artifact 2, optional leg).

**FLAGGED — this file's own name is off-grammar and cannot be committed as-is.**
The mandated filename omits the ADR-101 R3 class token. Live output from
`validate_hermetization.rule_b_violation`:
`class: '2026-08-03-night-ld-472-option-b.md' has no CLOSED-enum <class> token after the date
(ADR-101 R3: technical/functional/qa/census/verification/ecosystem-audit/
conformance-nightly-digest/changelog-review/codex/fresh-eyes/incident-evidence;
whole-token longest-match)`
The same call on `2026-08-03-technical-night-ld-472-option-b.md` returns `None` (clean). Every
sibling night-batch audit carries the `technical` token
(`docs/audits/2026-08-02-technical-night-batch-ld-currency-audit.md` et al). The file was
written at the mandated path per the lane's absolute constraint; **rename it before it is ever
staged**, or the `validate-hermetization` pre-commit hook refuses the add.

---

## Artifact 1 — amendment text

**Anchor form chosen: a lowercase, `id=`-keyed HTML-comment marker PAIR** —
`<!-- declaration:start id=adr104-fleet-members v=1 -->` … `<!-- declaration:end id=adr104-fleet-members -->`
— **because in this repo an HTML comment is the only marker class scripts actually parse, and a
fence is never one.** Evidence: five distinct comment grammars are parsed for content location
(`boundary_report.py:56-58` `methodology:start/end id=…`; `gen_doc_counts.py:45-46`
`COUNTS:START/END`; `gen_intake_index.py:32-33` `INTAKE-INDEX:START/END`; `gen_handoff.py:482-484`
`FILL-IN:<name> START/END`; `validate_doc_code_edge.py:53` `<!-- rule: ID -->`), while
`grep -rn '```[a-z]' scripts/*.py` returns **nothing** — every fence handler in the repo
(`normalize_headers.py:32`, `validate_doc_structure.py:113`, `boundary_headers.py:132`,
`gen_task_tree.py:178`, `audit.py:2381`) treats a fence as a region to *skip*, never as a typed
block. Two forms were rejected for cause: `methodology:start/end` is boundary_report's
hub/repo-ownership axis (semantically wrong, and `boundary_headers.py:62-67` deliberately
excludes `docs/` from its scan), and the UPPERCASE `X:START/END` form is used by three
*generators* — putting it in an immutable ADR would falsely signal a machine may rewrite the
block. The inner fence is **render decoration only** (without it markdown joins the ids into one
paragraph); the parser keys on the comment markers, never on the fence.

Shape mirrors `ADR-109`'s two existing amendments (`ADR-109:287-293` and `ADR-109:341-348`) —
`## Amendment — YYYY-MM-DD (…)` plus the blockquote in-file marker citing CLAUDE.md §5 item 3 /
ADR-94, then `### What this changes — and, deliberately, what it does not`. The lockstep clause
is lifted from ADR-101's precedent (`ADR-101:155,207,213`).

> Note on the fence below: this artifact contains a triple-backtick fence, so it is wrapped in a
> **four**-backtick fence. Paste the inner content only (from `## Amendment` to the last line),
> appended after `ADR-104:113`.

````
## Amendment — 2026-08-03 (the fleet declaration gains a machine-locatable anchor; [#472] / ADR-94)

> **In-file amendment marker (CLAUDE.md §5 item 3 / ADR-94).** The decision body above is
> preserved **verbatim** — nothing in it is edited, including the line-15 fleet enumeration this
> section makes machine-readable. It adds **no member, removes none, and changes no ruling**: it
> re-states the SAME nine repos inside a delimited block a checker can locate, so the
> enumeration stops being reachable only by prose. Landed under **[#472]**, whose Done-when is
> *"a ruling records how the ADR-104 declaration becomes loadable without violating ADR-109 §9"*.

- **Source:** [#472] (clause 2 split out of [#462], architect ruling 2026-08-01). In-file
  amendment per **ADR-94** — an own-invariant refinement of THIS ADR's own enumeration, not a
  new domain; the same channel ADR-101 uses to grow a closed set (`ADR-101` amendments
  2026-07-13 / 2026-07-27 ×2).
- **Correction of a recurring mis-citation:** the enumeration is at **line 15 of this file**, in
  the Context section. This ADR has **no §15** — its sections are §1–§5. Cite `ADR-104:15` or
  "the Context enumeration", never "§15".

### Why an anchor, and deliberately not a new file

The declaration has been machine-consumed since [#462] — as the hardcoded constant
`ADR104_FLEET_DECLARATION` in `scripts/audit.py`, whose own comment names the gap: *"the
constant can drift from ADR-104:15 silently."* That constant was the right call and stays: a new
persisted declaration file is **rejected by ADR-109 §2** (*"No new physical contract file is
created in v1"*) and again by **ADR-109 §9** (*"A new persisted desired-state file in v1 —
rejected"*). This amendment closes the drift without crossing that bar: the ADR — already the
authority — is made *locatable*, and the constant is checked against it.

### The declaration block

The block below is the ADR-104 fleet declaration in machine-locatable form. Its content is
byte-identical to the line-15 enumeration and to `scripts/audit.py::ADR104_FLEET_DECLARATION`.
One repo id per line; ordering is not significant; the delimiters, not the fence, are the
contract.

<!-- declaration:start id=adr104-fleet-members v=1 -->
```
.dev-knowledge
ai-council
corp-monorepo
corp-ops
corp-sca-time-automation
demo-prep
life-architect
terminal-setup
win-tooling
```
<!-- declaration:end id=adr104-fleet-members -->

**Lockstep in the SAME commit** (the `ADR-101` 2026-07-13 / 2026-07-27 precedent):
`scripts/audit.py::check_membership_agreement` gains the declaration-agreement leg that reads
this anchor, and `tests/test_membership_agreement.py` pins both directions of the diff. Unlike
that precedent, the lockstep here is **machine-checked, not conventional** — an edit to either
side without the other REDs the `audit-health` gate.

### What this changes — and, deliberately, what it does not

- **Changed:** the fleet declaration is now locatable by a checker. A constant that drifts from
  this ADR fails a gate instead of ageing silently.
- **NOT changed — membership resolution.** `resolve_fleet_members` is **not** widened and this
  block is **not** consulted for it. Resolving membership toward `deployed-versions.yaml` is a
  named **ADR-109 §2** ruling (restated in the ADR-109 2026-08-01 amendment); this anchor is an
  authority to *agree with*, never the census's membership input.
- **NOT changed — no registry is created.** The block confers no authority this ADR did not
  already hold. It is not a second source of truth: `ecosystem/`'s surfaces remain the machine
  surfaces, and the census still diffs THEM against the declaration, not against each other.
- **NOT changed — no new file, no new directory.** ADR-109 §2/§9 hold intact.
- **NOT changed — `VISION.md`.** VISION states the same nine (`VISION.md:107-112`) and remains a
  prose restatement. Binding it as a second machine surface would create exactly the second
  source of truth this amendment refuses; if that is later wanted, it is its own ruling.
- **NOT changed — the fold verdict, the tree count, or any §1–§5 ruling.** Nine were declared
  before this amendment and nine after.
````

---

## Artifact 2 — checker-binding spec

**Validator: `scripts/audit.py::check_membership_agreement`** (the `[#462]` organ, defined at
`scripts/audit.py:3286`, registered in `ALL_CHECKS` at `scripts/audit.py:3381`). A **new leg
inside the existing check** — not a new check function, not a new module.

Why this one, and not another:

- It **already owns the constant** (`scripts/audit.py:3203`) and its own comment already assigns
  this drift to [#472] (`scripts/audit.py:3200-3202`). The check and the defect are the same
  organ; anywhere else would split them.
- It is **already gated**: `audit-health` runs `audit.py health` pre-commit, *"FAIL blocks the
  commit; WARN only informs"* (`.pre-commit-config.yaml:121-126`). No new gate wiring.
- It is **already hub-only by repo identity** (`scripts/audit.py:3302-3304`, `_is_hub` at
  `scripts/audit.py:62-67`). Required: `docs/decisions/ADR-104-*.md` exists only in the hub, so
  a consumer must not FAIL for lacking it. A new standalone validator would have to re-earn this
  guard — the check's own docstring warns that guarding on artifact presence instead of repo
  identity *"would report FAIL across the fleet and manufacture a gap that does not exist"*.
- It **keeps `len(ALL_CHECKS)` at 38**, verified live this session, matching the claim
  `ecosystem/doc-counts.md:14` *"audit: **38 registered checks**"* that
  `validate_doc_claims.py` reconciles. A new check function would silently red that claim.
- Rejected alternative: `scripts/validate_doc_claims.py` is conceptually adjacent (prose-vs-state
  with an anchor-missing policy) but is scoped to **living** docs' count/list accuracy and
  degrades a missing anchor to a WARN (`validate_doc_claims.py:28-30`). An immutable ADR is not
  a living doc, and a lost anchor here must FAIL, not nudge.

**Attach point:** immediately after the `_is_hub` early return (`scripts/audit.py:3302-3304`)
and **before** the surfaces loop (`scripts/audit.py:3307`) — so the constant is verified before
it is handed to `classify_membership` (`scripts/audit.py:3339`), and so a declaration/constant
disagreement is still reported when a later surface read fails.

**What it asserts (three assertions, nothing more):**

1. **Anchor presence and uniqueness.** The `declaration:start id=adr104-fleet-members` /
   `declaration:end id=adr104-fleet-members` pair occurs **exactly once** in
   `docs/decisions/ADR-104-fleet-repository-shape.md`. Absent or duplicated → FAIL. This carries
   forward the check's existing rule that *"a gate that can be satisfied by deleting what it
   checks is not a gate"* (`scripts/audit.py:3312-3314`).
2. **Set agreement, both directions.** The ids parsed from between the markers equal
   `ADR104_FLEET_DECLARATION` as a set **and** in count (so a duplicated line is caught).
   Disagreement → FAIL naming both differences separately, because which side is stale is the
   first question a human asks — the same asymmetry-naming discipline as
   `scripts/audit.py:3270-3272`.
3. **Nothing else.** It does **not** feed the amendment into the census: `classify_membership`
   keeps receiving the module constant. This is the line that keeps C4 intact — the amendment is
   the authority the constant is *checked against*, never the loader input, and
   `resolve_fleet_members` is untouched.

**Creates no persisted file** (it reads a file that already exists and writes nothing; the
check's docstring already binds it: *"Read-only. It never regenerates a surface"*,
`scripts/audit.py:3298-3299`). **Confers no registry authority** (assertion 3).

**Failure output — exact message shape.** `Finding(check_name, status, evidence)`; `status` from
the five-value enum; `evidence` must be **ASCII-only and pipe-free**
(`scripts/audit.py:321-334` + `scripts/audit.py:3263`).

```
# anchor absent
Finding("membership_agreement", "fail",
        "ADR-104 declaration anchor 'adr104-fleet-members' not found in "
        "docs/decisions/ADR-104-fleet-repository-shape.md -- the declaration source cannot be "
        "satisfied by deleting what it checks ([#472])")

# anchor duplicated
Finding("membership_agreement", "fail",
        "ADR-104 declaration anchor 'adr104-fleet-members' appears 2 times in "
        "docs/decisions/ADR-104-fleet-repository-shape.md; exactly one is required ([#472])")

# unterminated pair
Finding("membership_agreement", "fail",
        "ADR-104 declaration anchor 'adr104-fleet-members' has a start marker with no matching "
        "end marker ([#472])")

# drift between the ADR and the constant
Finding("membership_agreement", "fail",
        "ADR-104 declaration and audit.ADR104_FLEET_DECLARATION disagree: "
        "in the ADR amendment only: new-repo; "
        "in the constant only: win-tooling; "
        "the constant and its declaring ADR have drifted -- fix whichever is stale, in one "
        "commit with the other ([#472])")

# agreement (the new pass leg; the existing census pass leg is unchanged and still emitted)
Finding("membership_agreement", "pass",
        "declaration source: ADR-104 anchor 'adr104-fleet-members', 9 ids, agrees with "
        "audit.ADR104_FLEET_DECLARATION")
```

**Optional second leg — NOT recommended in this pass.** Adding
`<!-- rule: fleet-membership-declaration -->` to the amendment plus `# rule:
fleet-membership-declaration` at `scripts/audit.py:3203` would register a real doc→code edge via
`validate_doc_code_edge.py:53`. But it only bites once ADR-104 joins `declaration_docs` in
`ecosystem/doc-code-edge.yaml`, and that file states at line 148 that doing so is *"a separate
ruling and not a side effect of landing a check."* It also adds **identity** coverage, not
**content** coverage — it proves the anchor and the code annotation both exist, never that the
nine ids match. The three assertions above are what [#472]'s Done-when asks for. File the
doc-code-edge admission separately if wanted.

---

## Artifact 3 — migration note

```
1. Land the ADR-104 amendment FIRST (heading + blockquote marker + anchor pair + block, ids
   copied byte-for-byte from scripts/audit.py:3203-3207); body untouched; index the amendment in
   docs/decisions/README.md in the same commit (precedent: commit 16ebdeb0, which indexed the
   ADR-109 2026-08-01 amendment).
2. THEN add the leg to scripts/audit.py::check_membership_agreement, attached after the _is_hub
   guard (3302-3304) and before the surfaces loop (3307); ADR104_FLEET_DECLARATION remains the
   value classify_membership receives at 3339 -- no new file, no new check function,
   resolve_fleet_members untouched.
3. TEST, RED before GREEN, in tests/test_membership_agreement.py: four tmp-tree ADR copies (one
   id removed / one added / one duplicated / anchor deleted) must each FAIL with the id named,
   and the live hub must PASS under @pytest.mark.live_repo, beside the existing
   test_live_hub_declaration_is_the_nine_of_adr_104 (tests/test_membership_agreement.py:139-141).
4. VERIFY before commit: len(ALL_CHECKS) still 38 (ecosystem/doc-counts.md:14 claim, reconciled
   by validate_doc_claims), pytest -x --tb=short green, ruff check clean, and
   `python scripts/audit.py health` clean -- the FAIL-blocks gate at .pre-commit-config.yaml:121-126.
5. DO NOT delete the constant: it stays the census input and the amendment becomes its checked
   AUTHORITY, not its loader -- that is what keeps ADR-109 section 2/9 (no new persisted file)
   and the "not a registry" constraint intact; reopening either is a separate ruling.
```

---

## Coverage

**Verified live, this session:** BACKLOG.md:440 (the [#472] row, read in full) · ADR-104
end-to-end (113 lines; heading enumeration; the line-15 declaration) · ADR-109 §1/§2/§9 plus
both in-file amendments · ADR-94 end-to-end (42 lines) · ADR-101's five amendments (the
closed-set-plus-lockstep precedent) · `scripts/audit.py:3187-3339` (the whole [#462] block) ·
`scripts/audit.py::check_membership_agreement` executed read-only against the live hub ·
`validate_hermetization.rule_b_violation` executed on this file's own name and on the
conformant variant · `ecosystem/doc-code-edge.yaml` (the membership_agreement exclusion note) ·
`ecosystem/doc-counts.md:14` · `.pre-commit-config.yaml:121-129` ·
`tests/test_membership_agreement.py` · `VISION.md:107-112` · `docs/decisions/README.md`
(ADR-104/ADR-109 ledger rows) · anchor-grammar survey across `scripts/*.py` · three sibling
audits for heading conventions.

**Prior art consumed, not repeated:**
`docs/audits/2026-08-02-technical-night-batch-lf-backlog-health.md:169-176` (lane L-F's
verify-then-reword verdict on [#472]). This dossier starts where that stopped.

**UNVERIFIABLE — `uv run --locked`.** The environment's uv is 0.8.17 against a `pyproject.toml`
pin of `==0.11.19`, so the gates could not be run through their real entrypoints. `audit.py` and
`validate_hermetization.py` were imported directly from the scratchpad interpreter instead;
their *outputs* are live, but the `uv`-wrapped pre-commit invocation was not exercised.

**UNVERIFIED BY CONSTRUCTION — the artifacts themselves.** No amendment was appended, no leg was
written, no test was added. Artifacts 1–3 are drafts; their behaviour is reasoned from the code
they would attach to, not demonstrated.

**Two deviations from the lane brief, declared:**
(1) *"YAML frontmatter matching sibling files"* — the siblings carry **no YAML frontmatter**;
they use an H1 followed by a bold key-value bullet block
(`docs/audits/2026-08-02-technical-night-batch-ld-currency-audit.md:1-8`). Disk truth was
matched over the brief's description.
(2) *"ASCII only"* — read as the house no-box-drawing/no-glyph-table rule (CLAUDE.md §4
"Output formatting"), which is honoured: every table here is flat and every copyable artifact is
fenced. Em dashes and `§` are retained because every sibling audit and every ADR uses them, and
an ASCII-normalized amendment would not be paste-ready into ADR-104.

## Nothing landed

No repo file was created, modified, deleted, staged, committed, merged, or checked out, other
than this single new file at the mandated path
`docs/audits/2026-08-03-night-ld-472-option-b.md`. No ADR was edited. No generator ran with
`--write` or `--force`. `git status` was clean at open and shows only this untracked file at
close. **This document is a ruling input, not an implementation.**

---

> **Editor's note (wrap, lane L-A) — this file was RENAMED before commit.** It was written to
> the brief's mandated path `docs/audits/2026-08-03-night-<lane>.md` and is committed as
> `docs/audits/2026-08-03-technical-night-<lane>.md`. Reason: the mandated pattern is refused
> by this repo's own `validate-hermetization` Rule B — `night` is not a member of the ADR-101
> R3 closed class enum (`scripts/validate_hermetization.py:89-98`). Inserting the `technical`
> class token is what every 2026-08-01/02 night-batch sibling already does. **The gate was not
> weakened, bypassed or amended.** Any occurrence of the old `2026-08-03-night-...` form below
> is preserved deliberately as the evidence that produced this finding — it is a quotation of
> the blocked name, not a live path. Verified post-rename: `rule_a_violation` and
> `rule_b_violation` both return `None` for all seven artifacts of this batch.
