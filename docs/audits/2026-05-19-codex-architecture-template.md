# Codex Review — architecture-template

**Date:** 2026-05-19
**Branch:** `main`
**HEAD:** `706c4ba`
**Diff range:** `1be2f8b..HEAD`
**Codex version:** codex-cli 0.122.0
**Mode:** diff-review

---

## Focus

(none specified)

---

## Findings
**Critical**

- (none)

**High**

- `High` — `templates/ARCHITECTURE-template.md:42` — **What:** the template makes the codemap a text-first, canonical structural artifact and describes diagrams as a complement rather than the required primary form for M/L repos. **Why:** ADR-51 says M/L repositories use a graphical codemap; this template tells adopters to do something different, so a repo can follow the template and still violate the governing ADR. **Fix direction:** rewrite the template so the required M/L codemap is the graphical artifact, with any text tree framed only as an optional supplement or as temporary migration guidance outside the canonical template.

**Medium**

- `Medium` — `templates/ARCHITECTURE-template.md:25` — **What:** the “inherited unchanged” template hardcodes `.dev-knowledge/...` paths and `.dev-knowledge/BACKLOG.md` ownership into cross-references. **Why:** once a child repo adopts this file, those are no longer valid relative paths from that repo, and the “tracked in BACKLOG” note points at the wrong repository’s backlog. That produces broken references immediately in every consumer. **Fix direction:** replace hardcoded `.dev-knowledge/...` relative paths with either placeholders, an explicit cross-repo reference convention, or plain-text governance references that do not pretend to be local relative links.

**Low**

- `Low` — `templates/ARCHITECTURE-template.md:48` — **What:** the codemap machine region uses an undocumented three-marker sequence: `CODEMAP:START`, `/CODEMAP:START`, `CODEMAP:END`. **Why:** the future generator/checker work depends on a stable insertion contract; an extra pseudo-closing marker makes the boundary ambiguous and increases the chance that tooling replaces the wrong region. **Fix direction:** standardize on one documented marker pair, such as `CODEMAP:START` / `CODEMAP:END`, and use that exact contract everywhere.

I could not locate an `AGENTS.md` file in the current checkout, so the banding above uses the requested `Critical / High / Medium / Low` levels directly.
