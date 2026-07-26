# Codex Review — routine-consumers check (adversarial, two passes)

**Date:** 2026-07-26
**Branch:** `docs/0726-brake-discharge`
**Reviewer:** `gpt-5.6-sol`, reasoning effort high, `--sandbox read-only`
**Invocation:** `codex exec` direct with `-c model=gpt-5.6-sol`. The wrapper's
CODE lane passes no model flag and would have inherited `gpt-5.6-terra` from
`~/.codex/config.toml`; a per-call flag was used rather than editing global config.
**Mode:** adversarial — prompted to REFUTE, not approve.

---

## Pass 1 — review of `bd9de975` (initial implementation)

Verdict: 0 Critical / 3 High / 3 Medium. **All six real; all six fixed** in `57d6458f`.

## Critical

None.

## High

### [scripts/audit.py:2433](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2433>) — Fields outside the routine declaration satisfy the gate

**Input:** `- [#701] proposal · consumer=example · consumption_path=example · routine: trigger=nightly · scope=hub`

**What:** The whole line is searched, so fields preceding `· routine:` make this pass even though the declaration itself lacks both required fields. Duplicate fields are also last-wins: `· routine: ... · consumer= · consumer=operator · consumption_path=boot` passes.

**Why:** Activated routines can bypass the gate through prose, examples, or ambiguous duplicates.

**Fix direction:** Parse only the declaration suffix and reject duplicate required fields.

### [scripts/audit.py:2397](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2397>) — Any nonempty token counts as a “named” consumer

**Input:** `- [#702] active · routine: trigger=x · consumer=<who reads it> · consumption_path=<how output reaches a decision>`

**What:** Template placeholders pass. So do `consumer== · consumption_path==` and visually blank `consumer=\u200b · consumption_path=\u200b`.

**Why:** The gate promises named values but validates only Python truthiness after `strip()`.

**Fix direction:** Reject placeholders, invisible-only content, and values lacking meaningful identifier text.

### [scripts/audit.py:2429](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2429>) — Markdown examples falsely activate the gate

**Input:** `- [#706] proposal says the activated row will later add \`· routine:\` · Done when: ruled in`

**What:** This legitimate proposal fails for missing fields. Likewise, a task-shaped line inside a fenced block—`- [#707] example · routine: trigger=nightly`—is treated as live.

**Why:** The scanner has no inline-code, quotation, or fenced-block awareness, breaking the activation-versus-filing boundary.

**Fix direction:** Exclude Markdown code/example contexts before detecting declarations.

## Medium

### [scripts/audit.py:2396](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2396>) — Lookalike markers fail open

**Input:** `- [#708] active • routine: trigger=x · consumer= · consumption_path=`

**What:** Replacing `·` with visually similar `•` makes the row pass as zero declarations.

**Why:** A malformed activation marker is silently treated like an unmarked proposal.

**Fix direction:** Surface activation-like malformed markers instead of ignoring them.

### [scripts/audit.py:2405](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2405>) — Docstring omits the one-row cardinality

**Input:** The current `BACKLOG.md` contains one governed row, `[#348]`; the check reports `1 declared routine row`.

**What:** The docstring says “marked BACKLOG rows” but never states that acceptance-time coverage is exactly one row or names `[#348]`.

**Why:** It is weaker than ADR-105’s explicit warning and the commit’s claim that the docstring says “ONE row wide.”

**Fix direction:** State the current one-row boundary and that green means only `[#348]` passed.

### [tests/test_audit.py:2251](</C:/Users/1028120/Documents/Dev/.dev-knowledge/tests/test_audit.py:2251>) — Adversarial parser behavior is untested

**Input:** Fields before the marker, duplicate fields, placeholders, `=`, zero-width values, exact markers inside inline/fenced code, and lookalike delimiters.

**What:** None of these cases is asserted. The proposal test contains only bare `routine:`, avoiding the exact syntax that causes the false positive.

**Why:** All demonstrated parser failures can regress or remain unnoticed.

**Fix direction:** Add regression tests for each adversarial class and pin the live one-row count.

## Low

None.
---

## Pass 2 — re-review of `57d6458f` (the FIX itself)

Prompted to refute the closure claim and hunt for regressions the fix introduced.
Verdict: **2 of 6 genuinely closed, 4 overstated** — and one regression (blunt
inline-code stripping erasing legitimate backticked values) was more likely to
bite than the original bug. Corrected in `138e3cb2`.

All six original regression fixtures pass, but the broader “fixed” claim is refuted: suffix scoping, Markdown stripping, lookalike detection, and placeholder validation still have exploitable or blocking edge cases.

## Critical

None.

## High

### [scripts/audit.py:2405](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2405>) — inline-code stripping is not context-preserving

**Triggering inputs:**

```text
- [#709] live · routine: trigger=x · consumer=`ops-bot` · consumption_path=`SessionStart`
```

This legitimate declaration returns FAIL because both values are erased.

```text
- [#710] proposal quotes ``· routine:`` · Done when: ruled in
```

This standard double-backtick code span returns FAIL as a declaration: the regex removes the paired delimiters but exposes the marker.

**Why:** The audit is commit-blocking, so this both rejects valid declarations and activates valid proposals.

**Fix direction:** Track Markdown code-span boundaries by delimiter-run length; ignore syntax occurring inside spans without deleting code-formatted field values.

### [scripts/audit.py:2406](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2406>) — fence toggling can fail open or parse fenced examples

**Fail-open trigger:**

~~~~text
    ```
- [#713] live · routine: trigger=x · consumer= · consumption_path=
~~~~

Four-space indentation makes the first line an indented-code literal, not a fence. The checker nevertheless enters fence mode and returns PASS with zero declarations.

**Nested-fence trigger:**

~~~~text
````markdown
```text
- [#712] example · routine: trigger=x
```
````
~~~~

The inner triple-backtick line incorrectly closes the four-backtick fence, so the example is checked and FAILs. Tilde fences (`~~~`) are also ignored entirely.

**Fix direction:** Track fence character and opening length, honor Markdown indentation/closing rules, and support both backtick and tilde fences.

### [scripts/audit.py:2470](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2470>) — a second marker can lend fields to an incomplete first declaration

**Triggering input:**

```text
- [#717] first · routine: trigger=nightly · scope=A · routine: trigger=weekly · consumer=ops · consumption_path=boot
```

The checker returns PASS because it takes every field after the first marker, allowing the first incomplete declaration to borrow the second declaration’s fields.

**Why:** This preserves a fail-open variant of claimed fix 1.

**Fix direction:** Reject multiple live `· routine:` markers in one row, or parse and validate each declaration independently.

### [scripts/audit.py:2404](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2404>) — lookalike detection blocks legitimate prose

**Triggering input:**

```text
- [#714] docs compare labels: • routine: recurring task; • project: one-off
```

This unmarked documentation row returns FAIL solely because prose contains `• routine:`.

**Why:** The rule cannot distinguish a mistyped declaration from quoted or comparative prose.

**Fix direction:** Require stronger declaration context around lookalikes, or surface ambiguous prose as WARN rather than FAIL.

### [scripts/audit.py:2418](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2418>) — all angle-wrapped values are treated as placeholders

**Triggering input:**

```text
- [#715] live · routine: trigger=x · consumer=<mailto:ops@example.com> · consumption_path=<https://intranet.example/runbook>
```

Both valid Markdown autolinks are rejected.

**Why:** Placeholder rejection overreaches into legitimate consumers and consumption paths, creating a blocking false positive.

**Fix direction:** Recognize the actual template placeholders rather than rejecting every value enclosed by `<` and `>`.

## Medium

### [scripts/audit.py:2421](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2421>) — conventional placeholders still count as names

**Triggering input:**

```text
- [#721] live · routine: trigger=x · consumer=TBD · consumption_path=TODO
```

This returns PASS because both values contain alphanumeric characters.

**Why:** Neither value actually names a consumer or mechanism, contradicting `_routine_value_is_named`.

**Fix direction:** Reject explicit sentinel placeholders such as `TBD`/`TODO`, preferably through a defined field-value policy.

## Low

None.

Closure verdict:

- **1 — Partial:** the original “fields before marker” case is closed, but multiple markers bypass declaration scoping.
- **2 — Closed:** duplicate required fields are rejected.
- **3 — Not closed:** only simple single-backtick spans and simple triple-backtick fences work.
- **4 — Narrowly closed:** the listed invalid values fail, but legitimate angle-wrapped values regress.
- **5 — Narrowly closed:** `•` is surfaced, but legitimate prose now false-FAILs.
- **6 — Closed:** the docstring explicitly states exactly one governed row.

Numeric-only and non-Latin values both pass, as they should. Pytest collection could not run because the read-only environment provides no writable temporary directory; the triggering cases above were executed directly against the committed parser using a no-write in-memory harness.