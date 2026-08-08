# Codex Review — deploy-doc-carrier

**Date:** 2026-08-08
**Branch:** `worktree-lane-280-315-carriers`
**HEAD:** `17b0ceb9`
**Diff range:** `main..worktree-lane-280-315-carriers`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 1/1/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- deploy/carrier_docs.py is a NEW generic file-copy carrier. Scrutinise the path-safety guard (_safe_rel): can any manifest-declared source or path still escape the hub root or the consumer root on either Windows or POSIX? Consider symlinks, drive-relative paths, UNC, trailing dots/spaces, unicode.
- Verify the D9 claim: detect (_classify_docs) and verify (_verify_docs) must share NO correctness-judgment code path. Is _hub_text a judgment or a spec read?
- _classify_docs state machine: is present == 0 -> ABSENT correct when pairs is empty or when a doc exists but is empty? Any state a real consumer could reach that classifies wrongly?
- apply() is not atomic across multiple files — a mid-loop exception leaves a partial write. Is that acceptable given detect classifies partial as DRIFTED?
- Manifest v1.4.0: the new docs carrier + intake-area / install-guide components. Do they satisfy release_lint C6/C8 semantics honestly, or merely syntactically? Is kind: config and waivable: true the right call for carried docs?
- Shipping the hub's docs/intake/README.md verbatim means the consumer inherits a generated 23-doc index it cannot regenerate (gen_intake_index.py is hub-only). Assess the severity of that.

---

## Findings
## CRITICAL

### deploy/carrier_docs.py:99 — lexical path guard permits root escapes

**What:** `_safe_rel` rejects only textual traversal; hub-source and consumer-destination paths can still traverse symlinked components, and Windows trailing-space/dot aliases such as `".. "` can evade the `"..”` check.  
**Why:** A declared source can read outside the hub, while a consumer symlink/alias can make `apply()` write outside the consumer tree, risking arbitrary external overwrite.  
**Fix direction:** Resolve and containment-check source paths and every destination ancestor against canonical roots; reject symlinks/Windows-normalized ambiguous segments and write via non-following atomic replacement.

## HIGH

### deploy/manifest-v1.4.0.yaml:372 — ships a hub-specific generated index into consumers

**What:** The copied `docs/intake/README.md` advertises and links 23 hub intake documents, but this carrier copies only that README and the template.  
**Why:** Every greenfield consumer immediately receives broken links and an index it cannot regenerate because `gen_intake_index.py` and the indexed documents are hub-only.  
**Fix direction:** Carry a consumer-specific intake README without the hub-generated index, or also provide a supported consumer-side generation/input model.

## MEDIUM

(none)

## LOW

(none)

D9 is satisfied: `_hub_text` is a shared spec read, not a correctness judgment. Empty `doc_paths` are rejected, and an empty existing document is treated as present. The non-atomic apply is explicitly recoverable because verification blocks staging/recording and a retry reconciles partial output.