---
name: check-against-spec
description: Reconcile a dependent doc against its spec when the spec version advances. Runs the deterministic site enumerator, then verdicts EACH extracted site (stale|fine|not-relevant; +transclusion-candidate), and writes the by-category checklist into the re-stamp commit message. Consumes a {dependent_path, spec_path, old_version, new_version} flag.
---

The semantic half of the coherence spine. The deterministic enumerator
(`scripts/coherence_enumerator.py`) guarantees the **complete** list of candidate
reference sites; your job is to **verdict each one**. You cannot omit a site that
exists — that is the whole point: a missed walkthrough step or an un-updated
diagram must not pass silently.

## Trigger (#205)

Invoked from the **reconciled_with re-stamp flow**, not on a schedule and not from the
ship-gate. When a spec version bumps, `audit.py reconciled_versions` reports a **mismatch**
and `scripts/validate_reconciliation.py` (CLI + `restamp_invocations(repo_root)`) **emits
the exact invocation** for this skill — the `{dependent_path, spec_path, old_version,
new_version}` flag plus the `coherence_enumerator.py` command. Run that, then do the verdict
work below, and land the filled checklist in the **re-stamp commit message** (the commit that
bumps the dependent's `reconciled_with` to the new version). Full procedure: PLAYBOOK
§"Declared-edge reconciliation" → "Re-stamp flow — the semantic half".

**The ship-gate is deliberately NOT the trigger** (recorded note). Gating every reconciliation
on an LLM verdict is a false-positive death-spiral; the gate gates the *version mismatch* only,
and this skill is triggered by the re-stamp flow. See §Scope (v1) — "do not wire the ship-gate".

**Input — the flag** (Prompt A's checker produces it): `{dependent_path, spec_path,
old_version, new_version}`. The checker's `validate_reconciliation.enumerate_edges(repo_root)`
yields one real `Edge` per declared reconciliation edge; the enumerator consumes it directly
via `coherence_enumerator.enumerate_from_edge(edge, repo_root)` (or `enumerate_repo(repo_root)`
for every edge at once) — no hand-built stub. You may still build the dict by hand for a
one-off edge the checker does not yet declare.

## 1. Enumerate (deterministic — do not skip, do not free-enumerate)

Run the extractor against the flagged edge:

```powershell
py scripts/coherence_enumerator.py --dependent <dependent_path> --spec <spec_path> --old-version <old> --new-version <new>
```

It prints a flat, by-category **checklist skeleton** — every candidate site, with
empty categories stated explicitly (`[none found]`) and an empty `verdict: ___`
slot per site. This list is exhaustive and **immutable**: you verdict it, you
never trim it.

## 2. Verdict EACH site

Read the spec (and, where available, the `old_version`→`new_version` diff of the
spec — e.g. `git log -p`/`git diff` on the spec file) and the dependent. For
**every** extracted site, fill its slot with exactly one verdict:

- **`stale`** — the site reflects the old spec and must change.
- **`fine`** — no change needed. This is a **first-class verdict**, not a blank;
  most sites will be `fine`.
- **`not-relevant`** — the enumerator over-extracted; this site has nothing to do
  with the spec change.

Add **`transclusion-candidate`** to a site that is **verbatim-duplicated** from
the spec — flag it for later de-duplication. **Do not** remove it and **do not**
build a transclusion mechanism now (v2).

Every site gets exactly one verdict; **none may be omitted or dropped.**

**Additive escape (additive only).** You MAY add sites the enumerator could not
see — chiefly anchor-less spec restatements / semantic paraphrases that carry no
detectable key-term — under the checklist's `additional (LLM-noticed)` section.
You may **ADD**; you may **NEVER drop** an extracted site.

## 3. Output — into the commit message, never a JSON file

Assemble the filled by-category checklist and put it in the **re-stamp commit
message** (the commit that reconciles the dependent to the new spec version). Do
**not** persist it as a JSON or any other file. When you surface it to the
operator in chat, wrap the whole checklist in a triple-backtick code fence so the
TUI renders it raw (CLAUDE.md §4 render-layer rule) — it is flat text with no
tables, safe to fence.

## Scope (v1)
One edge at a time. Do not build the trigger/checker (Prompt A), wire the
ship-gate (Integration), add an escape hatch, reparent any check, or hardcode the
spec version (the enumerator reads it live). Verdict the extracted list; do not
free-enumerate beyond the additive escape.
