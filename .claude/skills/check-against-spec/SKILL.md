---
name: check-against-spec
description: Reconcile a dependent doc against its spec when the spec version advances. Runs the deterministic site enumerator, then verdicts EACH extracted site (stale|fine|not-relevant; +transclusion-candidate), and writes the by-category checklist into the re-stamp commit message. Consumes a {dependent_path, spec_path, old_version, new_version} flag.
---

The semantic half of the coherence spine. The deterministic enumerator
(`scripts/coherence_enumerator.py`) guarantees the **complete** list of candidate
reference sites; your job is to **verdict each one**. You cannot omit a site that
exists — that is the whole point: a missed walkthrough step or an un-updated
diagram must not pass silently.

**Input — the flag** (Prompt A's checker produces it; until wired, build the dict
by hand): `{dependent_path, spec_path, old_version, new_version}`.

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
