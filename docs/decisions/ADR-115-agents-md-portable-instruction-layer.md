# ADR-115: `AGENTS.md` is the portable instruction layer — ADR-53 Decision 2 superseded and the ADR-101 Tier-1 file class amended in ONE act

- **Status:** Proposed
- **Date:** 2026-08-25
- **Decision tier:** Architecture (Path A — architect ruling under ADR-108 §A. The lane never self-accepts: the operator ratifies by merge, per ADR-94.)
- **Supersedes:** **ADR-53 Decision 2** in full. Consequentially, the word *"single"* in ADR-53 Decisions 1 and 4 stops describing the live model — named at §5 rather than left to rot. ADR-53's supersession of ADR-52 is untouched and stands.
- **Amends:** **ADR-101 §1** — the sanctioned Tier-1 top-level file set gains `AGENTS.md`. The exact `SANCTIONED_TIER1_FILES` diff is specified at §4 and is **deliberately not applied by this draft.**
- **Related:** ADR-52 (superseded by ADR-53), ADR-111 as amended 2026-08-25 (the birth-path authority this ADR rides), ADR-106 (the `uv run --locked` invocation form every command here uses), ADR-113 (the `L0` vocabulary), ADR-94 (status-line-only in-place edits), ADR-98 §3 (intake → rows), **ADR-114 (PARKED, operator-owned — explicitly untouched: the root `README.md` question is a different filename and a different decision, and nothing here un-parks it)**
- **Intake:** **#48** — `docs/intake/2026-08-24-tech-agents-md-admission-vs-adr53.md` (`READY`), which names the fork and sets the decision criterion. **#25** — `docs/intake/2026-08-05-func-simplification-distribution-wave.md` (`ACCEPTED`), whose **W-9(a)** is the ratified shape: *"CLAUDE.md → AGENTS.md with a thin CLAUDE.md shim containing `@AGENTS.md` + Claude-only overrides."*
- **Decommission:** register ruling **R-1** (`protocols/STANDING_RULINGS.md`) — retired on acceptance and replaced by this decision. A *reading* of an ADR is not a substitute for amending it; see §6.
- **Source:** **packet row `C01`** — `docs/audits/2026-08-25-technical-register-ruling-packet.md`, §"Decisions & rejections outside arcs" — pointed at by `protocols/STANDING_RULINGS.md` section U. **This ADR births no backlog row:** C01's carrier `[#577]` already exists, so ADR-111 guard (i) is discharged by this line and no ninth row is created.

<!-- Decommission: if non-empty, each listed item becomes a BACKLOG entry and stays open until removed. A decision is not complete while its Decommission items remain. -->

## 1. Context — two live surfaces asserting opposite permissions

Intake #42 measured the conflict and declined to resolve it, correctly: it is not an executor's call.

- **`protocols/STANDING_RULINGS.md` R-1** — *"`AGENTS.md` is ADMITTED, on the substance reading of ADR-53"*, reasoning that *"ADR-53 Decision 2 forbids two files that both carry content, not the filename `AGENTS.md`."*
- **`docs/decisions/ADR-53` Decision 2** — *"**`AGENTS.md` as a separate per-repo file is retired.** Existing `AGENTS.md` files … are to be removed and their content merged into each repo's `CLAUDE.md`."* `Status: Accepted`, un-superseded.

Three measurements from that intake, none of them softened here:

1. **The phrase R-1 quotes is not in ADR-53.** `grep -ci "two files that both carry content"` over ADR-53 returns **0**. Its nearest sentence argues the other way: *"Two instruction files create ongoing divergence with no compensating benefit."*
2. **ADR-53 Decision 2 names the filename**, not a content-duplication condition — so the "substance reading" is a reinterpretation, not a reading.
3. **The admitted shape is materially the alternative ADR-53 declared moot** (*"ADR-52 Decision 5 explicitly reserved a Codex-only `AGENTS.md` model for a future ADR; that reservation is now moot"*).

And the conflict is not academic. `scripts/validate_hermetization.py` **refuses the add today** — verified live in this lane, 2026-08-25:

```
$ uv run --locked python -c "import sys; sys.path.insert(0,'scripts'); import validate_hermetization as v; print(v.classify('AGENTS.md'))"
unsanctioned new top-level file 'AGENTS.md' -- Tier-1 files are a closed class
(ADR-101 section 1); a genuinely new class is an ADR-101 amendment, not a drive-by add
```

So `[#577]` could not execute without either an ADR-101 amendment or a `--no-verify` bypass the repo forbids. **The gate was right, and R-1 was the thing that was wrong** — see §6.

## 2. The criterion, and the measurement that meets it

Packet row **C01** did not rule on a lean. It set a **decision criterion** and deferred:

> **If ≥2 admitted providers natively consume `AGENTS.md` and not `CLAUDE.md` → supersede ADR-53 D2 with C01's thin-file spec (≤120 lines, non-inferable facts, importer). Otherwise → retire R-1.** Criterion over lean; the matrix is a one-session measurement.

**The measurement has landed and the criterion is MET.** `docs/audits/2026-08-25-technical-research-agents-md-standard.md` (R-L, compiled 2026-08-25) carries the per-tool matrix: instruction file(s) read, native-`AGENTS.md` yes/no, discovery/precedence rule, dated source. Read **strictly** against this fleet's six admitted providers:

| Provider | Reads `AGENTS.md` natively | Reads `CLAUDE.md` | Satisfies "and not CLAUDE.md" |
|---|---|---|---|
| **OpenAI Codex** | yes | not at all | **YES** |
| **Cursor** | yes (alongside `.cursor/rules/*.mdc`) | not at all | **YES** |
| Gemini CLI | on a one-line `context.fileName` setting (default `GEMINI.md`) | never | not counted — configuration required |
| Grok Build | yes | **also** auto-reads `CLAUDE.md` / `.claude/rules/` | no |
| Claude Code | no (its `/init` may *read* one to *generate* `CLAUDE.md`, which is not runtime consumption) | yes | no — the holdout in the other direction |
| DeepSeek | see §2.1 | see §2.1 | **unmeasured at runtime** |

**Two, with no configuration step. The count is deliberately not inflated:** Copilot, Zed, opencode and Amp each read both and therefore fail the second leg, exactly as Grok does; Gemini CLI is recorded as a third-on-a-setting and not counted.

**Corroborating prior art, independently derived 16 days earlier.** `docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md` carries its own matrix (`| Tool | Reads AGENTS.md natively? | File(s) it reads / precedence | Nested/subdir? |`) over Codex, Gemini CLI, Copilot, Cursor, Claude Code, Aider and Windsurf, and reaches the same structural finding: `AGENTS.md` ports natively across the fleet, and Claude Code is the exception. Two measurements, sixteen days apart, agreeing. *(That this artifact was unremembered when R-L was commissioned is the window's third owned-unconsumed incident; it is ARC-C's argument, not this ADR's.)*

### 2.1 DeepSeek — named as an open input, not a blocker

The record here is stated precisely because three successive sources said different things.

- **R-L recorded** *"no official first-party coding CLI/instruction convention"*. **Superseded** by the operator correction of 2026-08-25 (verified at `deepseek.com/harness`): DeepSeek ships **DSH**, a first-party developer-preview harness, MIT, `npx @deepseek-ai/dsh web`.
- **PROBE-DSH (2026-08-25)** answered the instruction-file question **from shipped source (tarballs); the runtime was never observed.** Its finding: **DSH consumes BOTH `AGENTS.md` AND `CLAUDE.md`** (candidates walked `.git`-root → cwd, `.local.md` overlays, 64 KiB batch budget). DeepSeek is therefore **NEUTRAL** in the intake-#42 matrix — it fails the "and not `CLAUDE.md`" leg exactly as Grok does — and a `CLAUDE.md`-only repo remains fully consumed by it.
- **Runtime verdict: not viable today.** `npx @latest` livelocked npm's resolver for 46 min / 2688 s CPU / zero output. Retry paths are recorded in the probe report; `pnpm` is absent.

**Consequence for this decision: none, in either direction.** Codex and Cursor already satisfy the criterion without DeepSeek, and a NEUTRAL provider cannot move a count of providers that read `AGENTS.md` *and not* `CLAUDE.md`. **DeepSeek's runtime consumption stays UNMEASURED and is named here as an open input** so that a later measurement is recognised as new evidence rather than as a contradiction. Any DSH lane admission goes through the R3 measured-acceptance gate like every other provider — preview status raises that bar, it does not lower it.

## 3. Decision

**3.1 A root `AGENTS.md` is ADMITTED. ADR-53 Decision 2 is superseded.** The active toolset is no longer the two tools ADR-53 measured; the premise its rejection rested on — *"both tools read CLAUDE.md directly"* — is false against a six-provider fleet, and `codex/AGENTS.md` already exists in-tree as an L0 carrier.

**3.2 The shape is C01's thin-file spec, as ratified by intake #25 W-9(a) — and the bounds are inherited from R-1 and `[#577]`, not re-derived:**

- **`AGENTS.md` is the portable layer**: build/test commands, boundaries, PR rules — **non-inferable facts only**. It carries **no** Claude-runtime specifics.
- **`CLAUDE.md` keeps the Claude-runtime remainder plus a thin `@AGENTS.md` import.** The relation is an **importer, never a symlink** — symlinks are ruled OUT on measurement (packet, ARC-D addendum): on Windows checkouts git materialises them as plain text files under the `core.symlinks=false` default, and creating real ones needs elevated rights, so the link would break silently per clone.
- **The size guard is stated in BYTES, not lines.** `≤120 lines` is the shape; the *guard* is the Codex `project_doc_max_bytes` 32 KiB cap, because this corpus averages ~117 B/line and a line ceiling does not bound what the cap measures. Measured basis (`docs/audits/2026-08-22-technical-intake-r1-decision-packet.md`): the proposed shape is **15,439 B = 47.1 %** of the cap, 16.9 KiB of headroom.
- **Two traps are named so they are not re-discovered:** copying `CLAUDE.md` wholesale lands at **43.50 KiB — 11.50 KiB OVER the cap, and Codex truncates silently**; and the precedence chain has a third layer *inside this repo* — `codex/AGENTS.md` sits at an intermediate directory, so a cwd at or below `codex/` yields `role → doctrine → role` and the role wins by position rather than by intent.
- **The `~/.codex` precedence collision is resolved BY SCOPE, stated in the file header:** the repo `AGENTS.md` governs in-repo work; the L0 reviewer pin governs the reviewer role.
- **`.gemini/settings.json` is still NOT admitted.** It would be a new Tier-1 top-level directory that Rule A refuses absent a separate ADR-101 amendment, and this ADR amends the **file** set only.

**3.3 `AGENTS.md` becomes a sanctioned ADR-101 §1 Tier-1 file — and NOT an ADR-38 canonical living doc.** These are two different memberships that happen to share a filename shape, and conflating them is the failure this clause exists to prevent. `AGENTS.md` is portable-instruction *payload*: it carries no `last_reviewed` stamp, is not in `FRESHNESS_FILES`, and has no section history. Enrolling it in `canonical_docs.CANONICAL_MANDATORY` would silently subject it to the freshness gate **and** to every consumer repo's canonical-set conformance check. §4 therefore adds it as an explicit literal.

**3.4 Execution stays where it already lives, and this ADR births nothing.** The root file is `[#577]`'s bounded lane (*"this row is the execution, not the decision"*). The `CLAUDE.md` §10 + `templates/claude-regions/antipatterns-universal.md` lockstep is `[#584]`'s. See §4's exclusion table for why neither is folded into the acceptance commit.

## 4. The acceptance act — ONE commit, specified here so it is reviewable before it exists

**Nothing in this section is applied by this draft.** `scripts/` is untouched by the lane that authored it. Acceptance is a follow-up act, taken after adversarial review.

### 4.1 The `SANCTIONED_TIER1_FILES` diff

The enum is a **closed set, live size 20**, measured this session:

```
$ uv run --locked python -c "import sys; sys.path.insert(0,'scripts'); \
    import validate_hermetization as v; print(len(v.SANCTIONED_TIER1_FILES))"
20
```

The intended diff, in full — `scripts/validate_hermetization.py`:

```diff
     # build / package manifests
     "package.json", "package-lock.json", "pyproject.toml",
     # uv toolchain (ADR-101 amendment 2026-07-27, [#432]/ADR-106): the committed
     # dependency lockfile + interpreter pin -- same class as package-lock.json.
     "uv.lock", ".python-version",
+    # portable instruction layer (ADR-101 amendment 2026-08-25, ADR-115; execution
+    # [#577]). DELIBERATELY a literal and NOT a member of _cdocs.CANONICAL_MANDATORY:
+    # AGENTS.md is an UPPERCASE.md Tier-1 file but it is NOT an ADR-38 canonical
+    # living doc -- no `last_reviewed` stamp, absent from FRESHNESS_FILES, no section
+    # history. Adding it to CANONICAL_MANDATORY would silently enrol it in the
+    # freshness gate and in every consumer's canonical-set conformance check.
+    "AGENTS.md",
 })
```

**Post-condition: size 21**, and `classify('AGENTS.md')` returns `None` (no refusal).

### 4.2 The test that moves in the same commit — because it currently REFUSES the diff

`tests/test_canonical_docs.py::test_validate_hermetization_seals_exactly_the_registry_living_docs` asserts the Tier-1 `.md` members are **exactly** the ADR-38 canonical seven. §4.1 breaks it by construction, which is the test doing its job: it is the organ that stops `AGENTS.md` from being absorbed into the canonical set unnoticed. It is widened to name the **one** sanctioned divergence explicitly:

```diff
 def test_validate_hermetization_seals_exactly_the_registry_living_docs():
-    """ADR-101 §1's file enum and the ADR-38 canonical set now provably name one set."""
+    """ADR-101 §1's Tier-1 `.md` set = the ADR-38 canonical set PLUS `AGENTS.md`.
+
+    ADR-115 admits `AGENTS.md` as a Tier-1 file WITHOUT making it a canonical living
+    doc: it is portable-instruction payload, not a freshness-stamped governance
+    surface. The `| {"AGENTS.md"}` is the ONE sanctioned divergence and is written as
+    an explicit exception so that a second one cannot slip in unnamed.
+    """
     md_members = {n for n in vh.SANCTIONED_TIER1_FILES if n.endswith(".md")}
-    assert md_members == set(cdocs.CANONICAL_MANDATORY)
+    assert md_members == set(cdocs.CANONICAL_MANDATORY) | {"AGENTS.md"}
```

### 4.3 The whole act, file by file

| # | File | Change |
|---|---|---|
| 1 | this ADR | `Status: Proposed` → `Accepted` (ADR-94 status-line-only in-place edit) |
| 2 | `docs/decisions/ADR-53-claude-md-single-instruction-file.md` | status line → `Partially superseded — Decision 2 superseded by ADR-115 (2026-08-25); the ADR-52 supersession stands` (ADR-94 status-line-only; §5) |
| 3 | `scripts/validate_hermetization.py` | the §4.1 diff — enum 20 → 21 |
| 4 | `tests/test_canonical_docs.py` | the §4.2 diff |
| 5 | `protocols/STANDING_RULINGS.md` R-1 | terminal marker: retired, superseded by ADR-115 (§6). This file is **excluded from the silent-rule detector's scope** post-R12, so the edit carries no baseline cost. |
| 6 | `protocols/PLAYBOOK.md` — two sites, cited by anchor text because line numbers rot: *"**Substantive single canonical per-repo agent-instruction file (≤200 lines).** Per ADR-53."* (§"Purpose", `:318` at time of writing) and *"CLAUDE.md is the single canonical agent-instruction contract; the handoff process does not narrate or manage it (ADR-53)"* (`:4163`) | both re-pointed at the two-file model. **PLAYBOOK IS in the ratchet corpus — see §4.4.** |
| 7 | `docs/decisions/README.md` | an ADR-115 index row, and the supersession note on ADR-53's row |
| 8 | `docs/intake/2026-08-24-tech-agents-md-admission-vs-adr53.md` | `status: READY` → a terminal status with `decided-by: ADR-115`, then the README §5 byte-identical relocation to `docs/intake/archive/`, then `uv run --locked python scripts/gen_intake_index.py --write` (the `intake-index-freshness` hook gates the index; the intake tree generator is a second, ungated regen and is run too) |
| 9 | generated fragments | `uv run --locked python scripts/gen_claude_rosters.py --write` — ADR-115 enters `.claude/generated/recent-adrs.md`, which the `claude-rosters-freshness` hook gates |

**Deliberately EXCLUDED from the act, with owners and reasons:**

| Excluded | Owner | Why not folded in |
|---|---|---|
| creating the root `AGENTS.md` | `[#577]` | it is a **bounded execution lane** with four binding bounds and a byte-cap test of its own; folding it in would make one commit both the decision and an untested build |
| `CLAUDE.md` §10 + `templates/claude-regions/antipatterns-universal.md` | `[#584]` | §10 is a **HUB-single-sourced Form-A region** that must stay byte-identical to its template. The two sites move together or fleet parity breaks — a different blast radius from a decision, and already owned |
| `.gemini/settings.json` | nobody | not admitted (§3.2) |

### 4.4 Two pre-flight measurements the act owes before it commits

1. **The silent-rule ratchet.** `protocols/PLAYBOOK.md` is inside the detector's corpus, and the live baseline is **443 / detector v5** (`ecosystem/silent-rule-baseline.yaml`, `measured_at: 2026-08-24` — CONTRA-9 adjudicates the three circulating numbers as three moments: 441 pre-R12, 445 probe-branch pre-merge, **443 live**). The baseline may be lowered or held but **not raised without an operator ruling**, and a raise FAILs `silent_rule_ratchet`, which blocks the commit through the `audit-health` hook. **Measure before and after; if item 6 raises the count, re-phrase declaratively rather than requesting headroom** — the register's own documented discipline.
2. **`validate_doc_claims`.** Its `precommit_hook_roster` and `pytest_collected` legs both read live surfaces that item 4 perturbs; re-run it in the same act.

## 5. What this does to ADR-53, stated rather than left implicit

**Decision 2 is superseded in full.** `AGENTS.md` is not retired; it is admitted, bounded, and gated.

**Decisions 1 and 4 are narrowed, and the narrowing is named here so a future reader does not find the word standing unqualified.** D1 (*"`CLAUDE.md` is the single canonical per-repo agent-instruction file"*) and D4 (*"CLAUDE.md … is now the substantive single canonical per-repo agent-instruction file"*) survive **except for the word "single"**. What each still asserts, and what stands: D1's supersession of ADR-52 stands; D4's **three authority levels** (universal protocols → per-repo instruction file → `.claude/` runtime config) stand unchanged — the per-repo level is now **two files with one contract**, `AGENTS.md` carrying the portable half and `CLAUDE.md` the Claude-runtime half plus the import. The substance ADR-53 protected — *one place where each fact lives* — is preserved by the importer; what ADR-53 forbade was duplication, and no fact is duplicated.

**Decision 3 needs no supersession — it is already discharged.** `templates/AGENTS-md-template.md` is absent from the tree (verified 2026-08-25), and the template it retired described the ADR-52 two-content-file model, not this one. The PLAYBOOK/ESSENTIALS half of D3 is item 6 of §4.3. **`protocols/ESSENTIALS.md` contains no `AGENTS` reference at all** (verified 2026-08-25), so it needs no edit — recorded because D3's text implies otherwise.

**Status token:** ADR-53 becomes `Partially superseded`. This is **not** an invented value — §7.

## 6. The precedence rule this case forces (intake #42's second open question)

Intake #42 asked, and said the answer generalises far beyond `AGENTS.md`:

> Does a recorded ruling ever outrank a ratified `Accepted` ADR, or is the register strictly subordinate?

**Ruled: the register is subordinate. A ratified ADR governs until an ADR changes it.**

A register entry may **interpret** an ADR, **apply** it, or **record** how it was executed. It may not **contradict** it. Where a ruling and a ratified ADR disagree on a permission, the ADR governs, the ruling is a defect, and the repair is an ADR — not a better reading. The reasoning is the repo's own: ADR-94 already holds that only a *status line* is editable in place, precisely because decision content is not something a later act may quietly reinterpret; a register that could outrank an ADR would make ratification advisory.

**Applied to R-1, without softening it:** R-1 admitted `AGENTS.md` on a reading whose key phrase does not appear in the text it construes (§1, measured). It **did not bind** while ADR-53 Decision 2 stood, which is exactly what `validate_hermetization` demonstrated by refusing the file — the gate and the ADR agreed, and the ruling was the outlier. R-1's *substance* is nonetheless adopted here in full: the bounds it carried are §3.2's, and its byte measurement is §3.2's guard. **The reasoning was right and the instrument was wrong.** R-1 is retired on acceptance and carries a terminal marker; this ADR replaces it.

**The generalisation, for the next case:** a ruling that needs an ADR to change is an **intake**, not a ruling. `STANDING_RULINGS.md` remains the right home for rulings that fill a gap the corpus does not cover — its many entries doing exactly that are unaffected.

## 7. The status token, answered from the live enum (intake #42's third open question)

Intake #42 asked what status a partly-superseded ADR carries, noting that `CONTRIBUTING.md` records `Partially superseded` as *"a legacy off-enum carve-out, not precedent."*

**That premise is stale, and the answer needs no invention.** `docs/decisions/README.md` §"Status enum" — declared 2026-08-12, register `M-6` / `N2-D2-i` — lists **`Partially superseded`** as a permitted value, glossed *"still binding in part; the superseding artifact is named in the status line"*, and its own measured census records **2 live instances**. Verified 2026-08-25: `ADR-46` and `ADR-47` both carry `Status: Partially superseded — retained as convention, NOT audit-enforced`, which is also the live *shape* (`Partially superseded — <reason>`). `scripts/validate_adr_status.py` adopts the same enum verbatim.

So ADR-53's new status line follows the enum and the live shape, and this question is **closed rather than deferred**.

## 8. Consequences

**Easier.** `[#577]` becomes executable: the gate stops refusing the file, and the Done-when clause that was unexecutable as written (`CLAUDE.md` §10, a Form-A region) is now owned by `[#584]` instead of being an obligation with no lawful path. A consumer repo asking which file is canonical gets one answer that contradicts nothing. The fleet gains a portable layer that Codex and Cursor read with zero configuration, which is the provider-agnosticism criterion ARC-D rules on from the other direction.

**Harder, and deliberately.** There are now two files where there was one, which is the drift risk ADR-53 correctly identified. **The mitigation is structural rather than procedural:** one importer, one direction, and a byte-cap test — no fact is written twice, so there is nothing to diverge. The two-file model is only as safe as that property, and `[#577]`'s test is what keeps it true.

**A new precedence rule is now live** (§6) and it binds every future ADR-vs-register disagreement, not just this one. That is a larger consequence than the filename, and it is the reason this ADR is worth its length.

## 9. Honest limits — what this ADR does NOT decide

- **It does not create the file.** The tree still has no root `AGENTS.md` after acceptance. `[#577]` does that.
- **It does not measure DeepSeek at runtime** (§2.1), and does not claim the six-provider matrix is complete for all time.
- **It does not admit any other new Tier-1 path** — one file, `AGENTS.md`, added as a literal. `.gemini/settings.json` stays refused.
- **It does not touch ADR-114.** The root-`README.md` question is PARKED and operator-owned; this ADR neither un-parks it nor borrows its reasoning, and the fact that ADR-114's park note says *"revisit only if the `AGENTS.md` track fails the universal-entry purpose"* is a **pointer at**, not a **dependency on**, this decision.
- **It arms no gate against its own new rule.** Nothing checks that `AGENTS.md` stays ≤32 KiB across `AGENTS.md` + `CLAUDE.md` until `[#577]` writes that test, and nothing checks that a future ADR does not silently re-contradict §6. Both are named, neither is built here.
- **The `AGENTS.md` filename is not ruled fleet-wide.** Whether consumer repos inherit this is `[#577]`'s scope note and the deploy manifest's, not this ADR's — stated because intake #42 listed it as a `Could`, and an unstated scope reads as universal.

## 10. Alternatives considered

- **Retire R-1 and keep ADR-53 Decision 2 as-is** — the criterion's own `Otherwise` branch, and it would have been the right outcome had the matrix come back short. It came back **met** on two providers with no configuration step, corroborated by an independent measurement 16 days earlier. Rejected on the evidence, not on a lean.
- **Leave both surfaces standing and let the gate arbitrate** — the status quo. Rejected: the gate arbitrates only for *adds*, which means the contradiction stays live for every reader while being enforced against exactly one actor.
- **Admit `AGENTS.md` by a further register ruling instead of an ADR** — rejected, and §6 is why: it is the precise move that produced the defect.
- **Make `CLAUDE.md` a symlink to `AGENTS.md`** (C01's own second option) — rejected on measurement, not taste: on Windows checkouts git materialises symlinks as plain text under the `core.symlinks=false` default, so the link degrades silently per clone. The `@AGENTS.md` importer is the documented interop and behaves identically on every platform.
- **Add `AGENTS.md` to `canonical_docs.CANONICAL_MANDATORY`** — the one-line version of §4.1, and it is a trap: it would enrol a portability payload in the freshness gate and in every consumer's canonical-set conformance check, changing what `AGENTS.md` *is* in order to save six lines of enum. Rejected; §4.2's test is the guard that makes the rejection stick.
