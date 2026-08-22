# DECISION PACKET — intake R1: is `AGENTS.md` admitted or refused, and under which reading of ADR-53?

- **For:** the architect / operator. **This packet exists to be ruled from — on its own, without reading anything else.**
- **Discharges:** the four inputs `docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md` §2.5 names as *"what CLOUD-4 should deliver instead"*, plus intake open-question **Q3** (*"What is the actual live Codex instruction size? R5 assumes it is under 32 KiB; **nobody has measured it**"*) — now measured.
- **Rules on:** `docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md` **PROPOSED ROW R1** — *"Rule on AGENTS.md: two memos vs ADR-53's single-instruction-file rule"*, whose hard gate at line 107 reads **"Must: rule on R1 before any AGENTS.md file is created."**
- **Produced by:** the CLOUD-4 v2 lane, bound at `ff01fd10` on `feat/cloud-4v2-universalization`. Every measurement below is reproducible at that revision with the command quoted beside it.
- **NO `AGENTS.md` FILE WAS CREATED.** That is the gate, honoured. This packet is input to the ruling, never a pre-emption of it. `docs/intake/` was read only; no status edited.

---

## 0. The question, in one paragraph

Two independent memos in this repo recommend adopting the `AGENTS.md` open standard so a non-Claude agent reads the same doctrine a Claude session reads. `CLAUDE.md` §10 names *"Narrating or managing AGENTS.md"* an anti-pattern and states *"AGENTS.md is retired (ADR-53)"*; ADR-53 Decision 2 reads *"`AGENTS.md` as a separate per-repo file is retired."* R1 asks whether that ruling forbids the **filename** or forbids **two files that both carry content** — because the shape both memos actually propose is a one-line `CLAUDE.md` = `@AGENTS.md` pointer, which preserves one substantive file while inverting the letter.

**Four inputs were owed before that could be ruled. All four are below.** A fifth section states what the ruling unblocks either way.

---

## Input 1 — the precedence collision, PRICED against the 32 KiB cap

### The mechanism (from the repo's own verified research memo)

`docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md:31`, graded VERIFIED against OpenAI's Codex docs, states the Codex precedence chain verbatim:

> `~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md` (global) → repo-root → intermediate dirs → cwd; `AGENTS.override.md` beats `AGENTS.md` at each level; **concatenated, later wins; 32 KiB cap (`project_doc_max_bytes`)**; `project_doc_fallback_filenames` for alternates

Two consequences follow, and the second is the one nobody had measured.

**(a) A repo-root `AGENTS.md` layers ON TOP OF the hub-owned reviewer role.** `codex/AGENTS.md` (79 lines) is the canonical source for `~/.codex/AGENTS.md` under ADR-54 — carried by `deploy/carrier_globalconfig.py:53–54` and `deploy/tool.py:340`. It defines *"Codex is a read-only code reviewer across all repos"* plus the severity checklist, and `protocols/PLAYBOOK.md:4261` pins it **HUB-OWNED (R1 — fleet doctrine) … Consumers never edit it.** Under later-wins concatenation, a root `AGENTS.md` carrying repo doctrine can **silently override that role**. This is the collision `docs/intake/2026-08-12-func-repo-self-description-consolidation.md:138–146` calls *"THE DECISION IS THE `AGENTS.md` COLLISION"*.

**(b) The combined payload has a hard ceiling, and it has now been measured.**

### The measurement

*Reproduce:* `wc -c codex/AGENTS.md CLAUDE.md` and the section-extraction over `CLAUDE.md`'s numbered H2s (the mover set is R2 §2.3's table: §2, §3, §4, §6 whole; §5 rules 1–5, 8, 9; §10).

```
Codex 32 KiB cap (project_doc_max_bytes)              32,768 B   32.00 KiB  100.0% of cap
~/.codex/AGENTS.md  (= in-repo codex/AGENTS.md)        3,891 B    3.80 KiB   11.9% of cap
hypothetical root AGENTS.md (R2 2.3 mover set)        11,548 B   11.28 KiB   35.2% of cap
COMBINED (global + root)                              15,439 B   15.08 KiB   47.1% of cap
                                                    headroom:   17,329 B   16.92 KiB

CLAUDE.md whole file, for contrast                    40,651 B   39.70 KiB  124.1% of cap
COMBINED if CLAUDE.md were copied wholesale           44,542 B   43.50 KiB  135.9% of cap
                                              -> OVER cap by:   11,774 B   11.50 KiB
```

### What the numbers say

1. **The proposed shape FITS, with 17 KiB to spare.** At 15,439 B the combined payload is 47.1% of the cap. **The role config survives the layering on size grounds** — R2 §2.5 input 1 asked whether it could, and the answer is yes. Truncation is not the blocker.
2. **The naive shape does NOT fit, and fails silently.** Copying `CLAUDE.md` wholesale into a root `AGENTS.md` lands at 43.50 KiB — **11.50 KiB over the cap**. Codex truncates at 32 KiB; nothing in this repo would say so. That is intake **ROW R5**'s whole justification, now with a number attached rather than an assumption.
3. **`CLAUDE.md` alone already exceeds the cap** at 39.70 KiB. Worth stating plainly because it kills a tempting shortcut: `project_doc_fallback_filenames` pointed at the existing `CLAUDE.md` would truncate on day one.
4. **A line budget is not a byte budget, and this repo's lines are long.** The mover set is 99 lines / 11,548 B — **~117 B/line**. The intake's Q1 bar (≤30 lines) implies ~3.5 KiB; R2's reconciliation bar (≤120 lines) implies ~14 KiB. Both are legal here, but *a ≤N-line rule does not bound the thing the cap measures.* **If R1 is admitted, the guard R5 asks for should be BYTES, not lines.**
5. **An unpriced third layer exists, and this lane found it.** The chain includes **intermediate dirs**. `codex/AGENTS.md` sits at `codex/` **inside this repo** — so a Codex session whose cwd is at or below `codex/` reads the reviewer role **twice**: once as the global copy, once as an intermediate repo file. Harmless today (identical bytes, later-wins), but if R1 is admitted and root `AGENTS.md` becomes doctrine, that path yields `role → doctrine → role` — **the role wins by position, not by intent.** Not a blocker; a thing the ruling should know it is choosing. *Reproduce:* `find . -name "AGENTS*.md" -not -path "./.git/*"` → `./codex/AGENTS.md`, `./templates/archive/AGENTS-md-template.md` (the latter retired 2026-05-19, superseded by ADR-53, and not on any read path).

**R2 §2.5's conditional does not fire.** It said: *"If it cannot [survive the layering], R1 must refuse the root filename and pick a `project_doc_fallback_filenames` alternate instead."* It can. **The size argument for refusal is unavailable to this ruling** — refusal, if ruled, rests on doctrine, not on bytes.

---

## Input 2 — the ADR-53 reading question, quoted verbatim

From `docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md`, Open Questions, item 1 — reproduced exactly, including its own framing of who owns it:

> 1. Does ADR-53's "single instruction file" ruling forbid *AGENTS.md specifically*, or forbid
>    *two files that both carry content*? A one-line `CLAUDE.md` = `@AGENTS.md` pointer arguably
>    satisfies the second reading and violates the first. This is a technical-architect
>    question about the ruling's intent and is deliberately not answered here.

And the shape the memos actually propose, quoted from the same intake, §D line 54:

> - **Q1 (portable layer):** In your hub repo, write one **AGENTS.md** (≤30 lines: build/test commands, boundaries, PR rules) + a one-line **`CLAUDE.md` = `@AGENTS.md`** + a **`.gemini/settings.json`** with `context.fileName: ["AGENTS.md"]`. That single trio makes Claude Code, Codex, and Gemini read the same rules today, Windows-safe.

**The lane's recommendation, offered as a recommendation and not as a finding:** rule on the **substance** reading and **supersede ADR-53 Decision 2 explicitly**. The substance ADR-53 protects is *one place where doctrine lives*, and a one-line pointer preserves that exactly. But the letter says otherwise, and a **silent** reinterpretation of a ruling is precisely the drift ADR-53 was written to end — so the reading has to be ruled out loud, in an ADR that supersedes, rather than assumed by whoever writes the first file. If R1 admits `AGENTS.md`, `CLAUDE.md` §10's first anti-pattern bullet is deleted or inverted in the same commit; if R1 refuses, that bullet stands and this packet closes the question with a price attached.

**One caveat on the quoted Q1 that the ruling should not inherit uncritically:** `.gemini/settings.json` would be a **new top-level directory**, which `scripts/validate_hermetization.py` Rule A blocks absent an ADR-101 §1 amendment — and ADR-53 records the active toolset as *"Claude Code + Codex only"*. **Gemini is a cost with no present consumer.** R1 can admit the `AGENTS.md` + `CLAUDE.md`-pointer pair without admitting the third leg.

---

## Input 3 — the region-axis reconciliation

### The finding

`CLAUDE.md` is **already region-split with byte-coupled carriers** — 8 HUB regions carried in `templates/claude-regions/` (6,447 B total across 8 files), 7 REPO regions owned locally. The coupling is asserted by `tests/test_boundary_headers.py::test_hub_region_bodies_still_byte_match_the_templates`.

**But its axis is HUB-vs-REPO — who owns the words. An `AGENTS.md` split needs UNIVERSAL-vs-PROVIDER — which tool reads the words. The two are orthogonal and they cross-cut**, demonstrably:

| region | existing axis | needed axis | cross-cuts? |
|---|---|---|---|
| `hooks-repo-roster` | REPO-owned | deeply Claude-specific | yes |
| `conventions-commit-branch` | HUB-owned | almost entirely provider-agnostic — **except** its enum contains `claude/<slug>` and `claude --worktree` (R2 seam S1) | yes |
| `critical-rules-records` | HUB-owned | universal | no |
| `commands-repo-roster` | REPO-owned | Claude-only (`.claude/commands/*.md`) | no |

R1 has to say which of two mechanisms is built.

### The two options, priced

**(a) SECOND AXIS on the existing carriers.** Each `templates/claude-regions/*.md` gains an `audience: universal | claude` marker; one generator emits both `AGENTS.md` and `CLAUDE.md` from one carrier set; **one** byte-coupling test stays. Cost: the carrier files gain a second meaning, and `conventions-commit-branch` has to be *split* to shed its two Claude-specific enum members — which is a **doctrine act** (`CLAUDE.md` §4 states a branch prefix *"enters this enum only via a recorded ruling (never silently); the enum stays the checkable surface"*), not a mechanical one.

**(b) PARALLEL carrier tree** (`templates/agents-regions/`). Cost: a second byte-coupling test, a second regen-and-diff gate, a new home under ADR-101, and — the real cost — **two carrier sets that can disagree**, which is the drift class this repo spends most of its enforcement budget preventing. Benefit: clearer, and each tree means exactly one thing.

**Recommend (a)**, and R2 §2.5 recommends the same: it is cheaper, it keeps one byte-coupling test, and — decisively — **the repo already runs generation + content-hash + regen-and-diff seven times over** (`.claude/CLAUDE-FLOOR.md` + `.sha256` + `check_floor_hash.py`; and the six gates `roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `organ-index-freshness`, `intake-index-freshness`, `codemap-freshness`). An `AGENTS.md` guard under (a) is an **eighth instance of a live pattern**, not a new organ family. That is library-first inside this repo, which is the bar the whole CLOUD-R2 brief was set at.

**Named cost of (a), so the recommendation is not free:** the `conventions-commit-branch` split needs a recorded ruling on the branch-prefix enum in the same act. R1 should either make that ruling or explicitly defer it and accept that `conventions-commit-branch` stays Claude-side until it lands.

---

## Input 4 — the efficacy caveat, verbatim and on the record

From `docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md:120`, quoting the study's own abstract. Reproduced in full because the point of putting it here is that the ruling cannot say it was not shown this:

> **Instruction-file portability is empirically weak as a *quality* lever.** The ETH Zurich study "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" (Gloaguen, Mündler, Müller, Raychev & Vechev; SRI Lab / LogicStar.ai; **arXiv:2602.11988, Feb 12–13 2026**; 138 tasks / 12 repos across SWE-bench Lite + AGENTbench) states in its abstract: "we find that providing context files does not generally improve task success rates, while increasing inference cost by over 20% on average." Developer-written files improved success ~4% on AGENTbench; LLM-generated files reduced it ~0.5% (SWE-bench Lite) to ~2% (AGENTbench); agents spent 14–22% more reasoning tokens and 2–4 extra steps. The mechanism: "agents dutifully process every instruction, whether it helps or not." A separate study on instruction adherence reports **within-session compliance attenuation** — each additional function the agent generates lowers adherence — and found structural variables (file size, position, conflict) had no detectable effect. **Implication: keep AGENTS.md short and high-signal (a ~150-line threshold is widely cited), and do NOT rely on it to carry enforcement.**

And the memo's own two caveats on its own evidence, quoted so the ruling weighs the study fairly rather than only harshly:

> **arXiv identifiers:** The context-file efficacy study is confirmed as arXiv:2602.11988 (ETH Zurich, Feb 2026); other arXiv numbers cited during research were not reliably verifiable and are described by finding rather than ID.

> **The instruction-file efficacy studies** measured test-pass rates, not code quality/maintainability/style — AGENTS.md may help in unmeasured dimensions (noted by study critics on Hacker News).

**The honest framing for R1:** adopt `AGENTS.md` **for portability insurance, not for quality**, and hold it to a stated ceiling. Do not let the adoption argument rest on a benefit the cited evidence does not support. R2 §2.5 recommends ≤120 lines; **this packet's Input 1 finding refines that: state the ceiling in BYTES**, because at this repo's ~117 B/line a line count does not bound what the cap measures.

**The counter-evidence to the counter-evidence, also on the record** (memo lines 13, 154), because R1 is choosing between two defensible positions and not one: the repo's Claude-specific mechanisms — hooks, slash commands, subagents, skills, permissions — *"do NOT port"*, and the memo's own steelman is *"do NOT sacrifice Claude-specific mechanisms to the lowest common denominator."* R2 §3.2 measured how little is actually at stake on the enforcement axis: **19 pre-commit / commit-msg / pre-push gate ids plus a GitHub-Actions wall already run under any agent**, and ADR-85's 2026-08-03 amendment deliberately moved the teeth off the Claude-specific Stop hook. **The expensive part of universalization is already done; `AGENTS.md` is the cheap part, and it buys insurance rather than capability.**

---

## 5. What the ruling unblocks, either way

- **[#82] agentic-review profiles is waiting on this.** Its first design input is *"heterogeneous second reader (different model architecture) is the field-validated shape — same-model self-review fails to sycophantic convergence."* Heterogeneity requires ≥2 providers reading the **same** doctrine; otherwise the different-architecture reader reviews against different instructions and the heterogeneity is confounded. R2 §4.3 grades §2 → [#82] as **PRIMARY — blocking**.
- **Intake ROW R5** (the 32 KiB truncation guard) becomes buildable the moment R1 admits, and Input 1 supplies both its threshold and its unit. If R1 refuses, R5 should be **killed**, not left open — with no root `AGENTS.md` there is nothing to concatenate, and the check would guard an empty class.
- **A refusal is also a result.** If R1 refuses, `CLAUDE.md` §10's anti-pattern bullet stops being an inherited assumption and becomes a ruled one, and the intake's own acceptance criterion is met: *"a reader can determine, from a committed artifact, whether AGENTS.md is admitted or refused."* **This packet plus a one-line ruling satisfies that criterion in either direction.**

## 6. Honest limits of this packet

- **`~/.codex/AGENTS.md` was measured from its in-repo canonical source**, `codex/AGENTS.md`, because no `~/.codex/` exists in this container (`ls ~/.codex` → no such directory). ADR-54 makes the in-repo file the canonical copy and `deploy/carrier_globalconfig.py` the carrier, so the substitution is the sanctioned one — but it measures the **declared** global config, not a specific workstation's live file. If a workstation has drifted from the carrier, its real number is different.
- **The 11,548 B "hypothetical root AGENTS.md" is R2 §2.3's mover set measured verbatim**, headers included, with no editing for concision. A real `AGENTS.md` would be shorter (the mover set carries hub-region markers and cross-references that a portable file would drop). **It is therefore an upper bound on that shape** — which is the useful direction for a cap argument.
- **`AGENTS.override.md` is not modelled.** The chain's top level would beat everything below it at every level. No such file exists anywhere in this fleet's declared config today, so it is out of scope here — but it is the mechanism a ruling would reach for if the role config ever needed to win by intent rather than by position.
- **No `.gemini/`, no `.github/copilot-instructions.md`, and no eval of the distilled set** were produced. Those are intake rows R2/R3/R4 and Q2/Q3, out of this lane's scope and downstream of R1.
