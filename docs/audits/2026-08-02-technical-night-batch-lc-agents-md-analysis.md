# Night batch 2026-08-02 · lane L-C — universal AGENTS.md migration analysis

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-02 · **Slug:** night-batch-lc-agents-md-analysis
- **Status:** **ANALYSIS ONLY — PROPOSAL.** No file was renamed, created, or moved. No `AGENTS.md`
  was authored anywhere. `CLAUDE.md` was read, never edited. The morning architect rules.
- **Operator's intent, as given:** *one universal `AGENTS.md` per repo instead of `CLAUDE.md`, so
  multiple LLM providers (not only Anthropic) consume the same instruction surface.*
- **Method:** read-only + web research. Every external claim carries a URL; every repo claim
  carries a path.

---

## 1. Recommendation up front

**Do not migrate now. Adopt "provider-fallback-config-first" as the standing posture.**

Three findings drive it, in order of weight:

1. **This repo already ran this experiment and reversed it on evidence.** ADR-52 (2026-05-19)
   adopted the AGENTS.md convention; **ADR-53 superseded it the same day** on empirical
   falsification — "Based on empirical verification (codex-cli 0.131.0, sentinel test PASS),
   evidence: `docs/audits/2026-05-19-cohort1-verification.md`". Nothing found in this research
   rebuts the falsification premise.
2. **The concrete multi-provider need is already met, for free, by a config knob.** Codex reads
   this repo's `CLAUDE.md` today via `project_doc_fallback_filenames = ["CLAUDE.md"]` in
   `~/.codex/config.toml` — documented in `protocols/PLAYBOOK.md` at **three** places (`:304`,
   `:951`, `:3185`). The provider-portability goal is *already achieved* for the one non-Anthropic
   provider actually in use.
3. **Claude Code does not read `AGENTS.md` natively.** Verified against the
   `anthropics/claude-code` CHANGELOG (zero mentions) and issue
   [#6235](https://github.com/anthropics/claude-code/issues/6235) — opened 2025-08-21, **still
   open**, with three later duplicates also open. A migration today would *lose* the surface the
   primary provider auto-reads, to gain one the secondary provider already reaches by config.

**Revisit when** either (a) Claude Code ships native AGENTS.md support, or (b) a specific new tool
is onboarded that reads AGENTS.md and offers **no** fallback knob. Both are observable triggers,
not calendar items.

**However — one part of the operator's question should be actioned regardless of the migration
ruling.** See §3: the §12 measurement is decisive and independent of AGENTS.md.

---

## 2. The AGENTS.md standard, as actually adopted

| Question | Finding | Source |
|---|---|---|
| Who steers it | Originated by OpenAI/Codex Aug 2025; **donated to the Linux Foundation's Agentic AI Foundation 2025-12-09**, alongside Anthropic's MCP and Block's goose. **Anthropic is a founding co-donor of the foundation stewarding it.** | [openai.com](https://openai.com/index/agentic-ai-foundation/) · [linuxfoundation.org](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) · [techcrunch](https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/) |
| Who reads it | Amp · Codex · Cursor · Devin · Factory · Gemini CLI · GitHub Copilot · Jules · VS Code | OpenAI's published list |
| Does Claude Code | **No** — not natively | CHANGELOG (0 mentions); issue #6235 open since 2025-08-21 |
| Adoption scale | **60,000+ repos** (OpenAI, Dec 2025) | best-sourced figure available |
| Layering syntax | Spec has **"no special syntax"** — plain markdown, nesting by directory | agents.md spec |

**One number deliberately NOT carried forward.** A secondary blog claims "20,000+ as of early
2026" — lower than OpenAI's own Dec 2025 figure and internally inconsistent. Flagged rather than
averaged, per intake #16 §5 lesson 6 (the 10–20-repo failure class). **Use 60,000+, sourced.**

**The governance direction is genuinely favourable** — Anthropic co-founding the foundation that
stewards AGENTS.md is the strongest signal yet that this converges. That argues for *watching*,
not for migrating ahead of the tooling.

### The `@import` problem — a hard mechanical blocker

`CLAUDE.md` currently splices in three generated fragments via Claude-proprietary `@import`:
`.claude/generated/commands-repo.md`, `.claude/generated/recent-adrs.md`,
`.claude/methodology-roster.md`. The AGENTS.md spec has **no include syntax**. Moved as-is into a
universal AGENTS.md, those three lines render as **dead literal text** to every non-Claude tool —
so the "one surface all providers consume" goal fails precisely for the generated rosters that
exist to prevent hand-rot. Any migration must first rule what happens to `@import`.

---

## 3. The CLAUDE.md inventory — and §12, measured

`CLAUDE.md` = **238 lines · 42,663 bytes**, with **194 prose lines** against ADR-53's ≤200-line
budget (**97% full**).

**The §12 measurement, which is the operator's actual question:**

| Metric | §12 "Section history" | Share of file |
|---|---|---|
| Raw lines | 20 | 8.4% |
| **Bytes** | **19,383** | **45.4%** |

*(Independently re-measured by this orchestrator against the live file — not taken from the probe.)*

**Nearly half the agent-instruction file, by substance, is per-file version history** — hidden
behind a line-count metric that reads as 8%. The divergence is not accidental: new history is
folded into ever-denser paragraphs rather than new lines, and several entries **say so in their
own text** — *"folded here (not a new §12 bullet) to hold the section-history count at 11 (ADR-49/65
condense threshold)"*. The file is optimising the metric the gate measures while the content it is
supposed to bound grows unchecked.

**Verdict against the repo's own conventions — it does not belong there:**

- **ADR-49 / ADR-65** — git is the technical record; JOURNAL's `Changes:` line replaces per-file
  changelogs. ADR-65 **explicitly rejected** "one-line stubs in-file" on the reasoning that
  *"stubs still accrete and re-bloat"*. §12 is the predicted re-bloat, arriving as dense prose
  instead of stubs.
- **CLAUDE.md §5 rule 8** — `CHANGELOG.md` is deleted and must not be recreated. §12 is a
  per-file changelog living inside the instruction file.
- **§12's own entries** repeatedly point at `git log --follow -p -- CLAUDE.md` as the real record,
  which is an admission that the in-file copy is a duplicate.
- **ADR-53** sets the ≤200-line budget for this file *as an agent-instruction contract*. A
  session-boot reader pays 45% of the file's bytes for history it will never act on.

**RECOMMENDATION (independent of the AGENTS.md ruling): relocate the un-condensed history
(v2.31–v2.48) behind the existing git pointer**, matching how v1.0–v2.30 were already handled.
This needs **no new ADR** — ADR-49/65 already authorise it and the precedent is in the file.

**One precaution before relocating.** Some §12 entries carry *rulings* recorded nowhere else. Two
of fifteen un-condensed entries were spot-checked for uniqueness — v2.42 (ADR-29 chronological
archival ratification) and v2.44 (the [#352] colour-spec correction) — and **both are
independently recorded elsewhere** (in ADR-29 itself; in `tasks/352-*.md` and
`docs/audits/2026-07-20-technical-352-*.md`). **A full 15-entry uniqueness pass is owed before
relocation** — cheap, and it converts a plausible-looking safe edit into a verified one.

### Fleet-wide surface

- **72 distinct files, 255 occurrences** hardcode the string `"CLAUDE.md"` — scripts/ (22),
  tests/ (27), templates/ (10), deploy/ (9), .claude/ (3), `.pre-commit-config.yaml`.
  **That count is the mechanical migration cost, hub-side only, before any consumer repo.**
- 8 consumer repos declared; only 3 (hub, ai-council, corp-monorepo) carry live floor/boundary
  infrastructure today.
- **An `AGENTS.md` already exists in this repo: `codex/AGENTS.md`** — the ADR-54 convention. Any
  universal-AGENTS.md ruling collides with it and must say which wins.

---

## 4. Migration design options

| Option | Mechanism | Pros | Cons / blast radius |
|---|---|---|---|
| **(a) Universal AGENTS.md + thin provider shims** | `AGENTS.md` becomes canonical; `CLAUDE.md` a pointer | one authored surface; matches the emerging standard | Claude Code does not read AGENTS.md, so the *primary* provider now reads a shim; `@import` dies for non-Claude tools; re-keys 255 sites; boundary markers, floor hash, `.vscode` decoration all keyed to the filename |
| **(b) Symlink / include indirection** | `AGENTS.md` → `CLAUDE.md` | near-zero authoring change | symlinks are unreliable on the fleet's Windows substrate; regen-and-diff gates and the floor **sha256** may hash the link, not the target; `@import` still non-portable |
| **(c) Status quo + provider fallback config** | keep `CLAUDE.md`; point each provider's fallback knob at it | **already working for Codex**; zero migration cost; fully reversible | depends on each tool exposing a knob; no knob = no reach |
| **(d) Additive AGENTS.md, hub only** | plain provider-neutral `AGENTS.md` alongside `CLAUDE.md`, no `@import` | fully additive, fully reversible; tests the standard cheaply | two surfaces to keep coherent — a **new drift axis**, which is the failure mode CLAUDE.md §5 rule 6 names |

**Recommended: (c) now, with (d) as the smallest reversible probe** if the architect wants to move
regardless — hub only, no `@import`, `CLAUDE.md` untouched.

### Two breakage points that would fail *silently*

Worth naming because neither surfaces as a red gate:

1. **`.vscode` `filterFileRegex`** — the boundary decoration matches on filename; a rename
   silently stops decorating and nothing reports it.
2. **`release_lint`'s manifest mirror** — if not wired into pre-commit, a filename change passes
   the commit gate and fails later at release time.

Add the **floor hash** (`.claude/CLAUDE-FLOOR.md` + sha256 sidecar, ADR-78/93) and the
**boundary byte-match** between CLAUDE.md's 8 `owner=hub` regions and their
`templates/claude-regions/` extracts — both are exact-match contracts that a migration must
re-establish deliberately.

---

## 5. The governance this needs — ADR-110

**Proposed title:** *Universal AGENTS.md adoption — filename of record, precedence, and fleet
re-keying.* (ADR-110 is the next free number after ADR-109.)

**What it must rule** — none of these can be left implicit:

1. **Filename of record** per repo.
2. **Precedence** when both files exist (both-read? one wins? which?).
3. **Collision with ADR-54** — the live `codex/AGENTS.md` convention.
4. Whether `boundary_report.py` / `boundary_headers.py` **re-key** off their hardcoded
   `"CLAUDE.md"`, and whether the 15 Form-A regions move.
5. Whether the **methodology floor** renames — and how its sha256 sidecar is re-established.
6. **Consumer rollout order** (the hub is the boundary diff baseline, so it cannot go last).
7. **Provider-specific content disposition** — what layers where, given no include syntax.
8. **`@import` disposition** — inline the generated rosters, drop them, or keep them Claude-only.
9. **Explicit re-affirmation or reversal of ADR-53**, naming the new evidence. *This research found
   none* — so as things stand, ADR-110 would have to overturn ADR-53 on preference rather than
   evidence, which is exactly the bar ADR-53 itself cleared with a sentinel test.

Item 9 is the one the architect should weigh first: **ADR-53 was decided by measurement. Reversing
it should be too.**

## 6. Costs, risks, and the falsifiable test

**Cost:** 255 hardcoded sites across 72 files, hub-side only; plus floor re-hash, boundary
re-key, `.vscode` re-key, and the same again per consumer repo.

**Risk profile:** the dangerous failures are the *silent* ones — hash guards, regen-and-diff
gates, and the boundary byte-match all fail closed and loudly, but the `.vscode` regex and the
release-lint mirror fail open and quiet.

**The cheap experiment that would settle it** (mirroring ADR-53's own method): drop a sentinel
line into a plain `AGENTS.md` in one repo, start a Claude Code session, and check whether the
sentinel is in context. That is a one-session test and it is the *only* evidence that should move
ADR-53.

## 7. Blocking questions for the architect

| # | Question | Decision shape |
|---|---|---|
| C-1 | Migrate to universal AGENTS.md, or hold at provider-fallback-config? | migrate / hold / additive-probe (option d) |
| C-2 | **Relocate §12 (45.4% of CLAUDE.md by bytes) behind the git pointer?** Independent of C-1; needs no new ADR. | relocate / keep / relocate-after-uniqueness-pass |
| C-3 | If migrating: does ADR-110 overturn ADR-53 on preference, or is a sentinel re-test run first? | re-test-first / overturn-on-preference |
| C-4 | What happens to the three `@import` fragments, which have no portable equivalent? | inline / drop / keep-Claude-only |
| C-5 | Does a universal AGENTS.md supersede the live `codex/AGENTS.md` (ADR-54)? | supersede / coexist / re-scope ADR-54 |

---

*Analysis only. No `AGENTS.md` was created, no `CLAUDE.md` was renamed or edited, and no
file moved. Every recommendation above is a proposal for the morning architect.*
