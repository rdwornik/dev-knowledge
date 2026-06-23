# PLAYBOOK Fidelity Audit — 2026-06-23

> **Scope:** `protocols/PLAYBOOK.md` (3352 L) — a FIDELITY audit (does each section reflect how we actually work *now*, is it reconciled with its governing ADR incl. status, is it still load-bearing, is it correctly placed, and does PLAYBOOK document the harmony surfaces?).
> **Distinct from** the same-day HYGIENE audit (`docs/audits/2026-06-23-canonical-corpus-coherence-audit.md`, findings PB-A…PB-L), which asked *"is this line stale/dead/duplicated?"* This audit cross-references those findings and adds the fidelity lens; it does not re-derive them.
> **Method:** 8 read-only section agents tiling lines 1–3352 with zero gaps (A–F apply lenses 1–4 span-local + emit harmony signals; G owns the whole-doc lens-5 verdict), then **orchestrator re-verification of every high-impact / full-scope claim** (the hygiene audit's load-bearing lesson — it refuted 6 of its own agents' claims for wrong-scope commands).
> **Posture:** DIAGNOSTIC ONLY. No PLAYBOOK content is edited. Removals/restructure are a separate, per-item operator-approved arc.
> **Branch:** `audit/playbook-fidelity` · **machine baseline:** `audit.py health` = GREEN (`health: OK`).

---

## §0 — Headline

**Overall fidelity verdict: HIGH.** PLAYBOOK accurately and currently documents the methodology. Of ~62 section-level dispositions, **~40 are KEEP** (the section faithfully describes current practice and reconciles with its ADR), including every load-bearing workflow, the handoff (v5.2), the worktree discipline, the Council/ADR pipeline, the codemap/auto-TOC tooling, and the appendices' "point-don't-restate" deferrals. The drift that exists is **concentrated, currency-type, and mostly already-tracked** — stale platform pins, dead path/procedure tombstones, and a few un-cited or pending-ADR reconciliations. **No section misrepresents a Proposed ADR as settled** (the one suspected case turned out to be the *brief's own premise* being stale — see §6). The structural "two-documents-glued" form is comprehension-aiding given the maintained auto-TOC, **not** a defect warranting restructure (§7).

**Highest-confidence drift — the platform-currency cluster (all MACHINE-VERIFIED):**
- CC version pin **`2.1.168`** (L2118) vs live **`2.1.186`** — stale by 18 patch releases.
- Hooks "auto vs manual" table (~L1693, self-stamped 2026-06-01) lists **6** pre-commit hooks; the live `.pre-commit-config.yaml` has **10** — and the table's CC-hook rows describe the **retired** `/boot`+`/evolve` evolution-scorecard machinery while omitting the entire live repo-level session-hook layer.
- Effort enum `low/medium/high/xhigh` is missing the live **`max`** tier (confirmed against this session's own tool schemas).
- `~/.claude/ROUTING.md` (canonical, deferred-to by App B) still encodes a **Sonnet-default** routing that contradicts §2's **Opus-4.8-default/floor** doctrine.

**Harmony-coverage verdict (lens 5): ADEQUATE, with correct delegation.** PLAYBOOK documents the Layer-1 browser-architect role for its own scope (the prompt contract) and rightly delegates the 3-layer model + invariants to `ARCHITECTURE.md` Ch1 rather than restating them — that delegation is this repo's reason-to-exist, not a gap. The only genuine soft gap is the cross-document **"architect" actor-vs-mode vocabulary ambiguity (#162)**, which PLAYBOOK participates in but does not create.

**Counts by verdict (distinct material findings; the ~40 KEEPs are listed in §2 but excluded here):**

| Verdict | Count | Findings |
|---|---|---|
| REMOVE-candidate | 1 | B3 (=PB-A) |
| UPDATE-to-current | 14 | A1, A10(=PB-I), C2(=PB-J), D1(=PB-C), D2(=PB-G), D3, D4, D5(=PB-K), E1-1(=PB-H), E1-2, E1-3, E2-2, F1/F2(=PB-D), F6 |
| RECONCILE-with-ADR | 3 | E2-1, E2-4, F4 |
| CONDENSE | 2 clusters | B2/§525-overlap; PB-E scatter (B10/D9/E2-3 + F3 enabler) |
| PROMOTE-to-enforcement | 1 | B11 (=PB-L) |
| ADD-coverage | 3 | D6, F3, G1(=#162) |
| JUDGMENT-flagged (low-confidence / uncertain) | 3 | D7, E1-4, F5 |

---

## §1 — Phase-0 machine baseline

`python scripts/audit.py health` → **`health: OK`** (self-audit 18/26 pass; remainder `[--]` n/a or `[~~]` informational WARN; **no FAIL**). PLAYBOOK carries **no machine FAIL** — confirming fidelity findings are predominantly JUDGMENT + targeted file/grep checks, not audit.py output. Relevant signals (evidence floor):

```
doc_code_edge        : 5/5 doc->code edges resolved; none broken/ambiguous
reconciled_versions  : 1/1 reconciled_with edge matches live spec version
doc_claims           : 3/3 doc self-claims match repo state
canonical_freshness  : 6 canonical living files fresh   (PLAYBOOK is NOT in this set — see A1)
doc_rot (WARN)       : BACKLOG#164/#77/#134 accretion bloat  (BACKLOG, not PLAYBOOK)
no_ff_merges (WARN)  : 2 pre-existing non-merge commits on main (2026-06-19) — not from this audit
git_backlog_drift(~~): #77 closed-but-present (the known voided-#77)
```

`python scripts/audit.py checks` → 23 registered checks (drift-proof from `ALL_CHECKS`). **ADR-status authority** is `docs/decisions/README.md` — but see §6: the README index and CLAUDE §11 lag the in-file ADR amendments for ADR-88/89.

**Hygiene cross-ref base loaded:** PB-A…PB-L + the §6 refuted-claims ledger. This audit confirms PB-A, PB-B, PB-C, PB-D, PB-G, PB-H, PB-I, PB-J, PB-K, PB-L on re-verification and adds the fidelity lens; it does not re-surface them as new.

---

## §2 — Per-section findings

Format: `ID | file:line | lens | VERDICT | confidence | ADR | BACKLOG | hygiene-xref`. `protocols/PLAYBOOK.md` implied for line refs. Orchestrator re-verification status noted where I personally re-ran the command.

### Header / intro / TOC (lines 1–217) — Agent A

- **A1 | :4 | lens1 | UPDATE-to-current | MACHINE | ADR:none | BACKLOG:NEW | hygiene:none**
  Header reads `> Last updated: 2026-06-19`; `git log -1 -- protocols/PLAYBOOK.md` → **`25394c9 2026-06-22 19:30`**. Edited 3 days after its self-declared stamp. **Re-verified by orchestrator.** Note: PLAYBOOK uses a plain `Last updated` line, **not** a `last_reviewed` frontmatter stamp, so `audit.py` check #10 (covers VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS) does **not** catch this. Nothing auto-detects PLAYBOOK header drift.
- **A2 | :14–216 | lens4 | KEEP | MACHINE** — TOC is auto-generated (`<!-- TOC:START/END -->`, `do not edit by hand`); covers both halves. Generated-and-skipped, not silently dropped. Intro prose (L1–13) is current.

### System Architecture + CLAUDE.md-contract + Repo conventions (218–519) — Agent A

- **A10 | :494,501 | lens1/3 | UPDATE-to-current | MACHINE | ADR:33,34 | BACKLOG:NEW | hygiene:PB-I**
  Two `[TBD — Stream C session 3, ADR-33/34]` placeholders (Secrets storage path L494; Capitalization L501). **Re-verified:** `ADR-33` = "VISION.md universalization", `ADR-34` = "File naming convention" — both exist. **Fidelity nuance beyond PB-I:** ADR-33 does **not** govern a secrets path, so L494 is *mis-tagged*, not merely a stale forward-pointer; resolving it requires deciding whether the topic is answered elsewhere or genuinely still-open. L501→ADR-34 is plausibly answerable (file-naming covers casing). Confirms PB-I; adds the mis-tag wrinkle.
- **A11 | :505–516 | lens2 | KEEP (suspected-RECONCILE, refuted) | MACHINE | ADR:89** — the rule-ID naming pointer cites "ADR-89 OQ1 — ADOPTED" and explicitly preserves "Advisory-first; hard-gate is a later data-gated arc." PLAYBOOK does **not** overclaim a Proposed ADR; the OQ1 sub-item is genuinely adopted+deployed (`ecosystem/doc-code-edge.yaml` + live `rule:` tokens). KEEP.
- **A3–A9, A12 | KEEP** — System Architecture correctly delegates the 3-layer model to ARCHITECTURE Ch1 (A3); CLAUDE-contract/ADR-53 (A4), source→gate→agent (A5), child-floor/ADR-78 (A6), LLM-LLM back-and-forth/ADR-87 (A7), process-versioning (A8), repo-convention ADR pointers (A9) all reconcile. A12 flags the L288 "stale-numbers" example as a *deliberate, self-annotated* anti-pattern illustration — do not "fix."

### Writing prompts / complexity bands / doc-types (520–974) — Agent B

- **B3 | :818–829 | lens1/3 | REMOVE-candidate | MACHINE | ADR:40 | BACKLOG:#77 | hygiene:PB-A**
  `### Tier transition procedures (ADR-40) — DEPRECATED 2026-05-23` — a dead-procedure tombstone (ADR-40 status = `Deprecated (was: Accepted)`; tier system retired 2026-05-23 / ADR-38 A5). **Re-verified L818 verbatim.** Confirms PB-A. The tombstone's regression-guard *intent* ("not silently re-introduced") should survive as a one-liner if removed. Delete needs per-item operator approval + confirm-live.
- **B7 | :855 | lens1/2 | UPDATE-to-current | MACHINE | ADR:82 | BACKLOG:NEW | hygiene:PB-B**
  File-type table labels handoffs `(v4 bundle) … generated from source (HANDOFF_PROCESS v4)` though v5.2 is canonical (`handoff_version_stamp` GREEN @ v5.2). The same section's L960–961 already marks v4 "historical" — L855 is the stale straggler. **Re-verified L855 verbatim.** Confirms PB-B.
- **B11 | :941–944 | lens3 | PROMOTE-to-enforcement | MACHINE | ADR:none | BACKLOG:NEW | hygiene:PB-L**
  "Supersession & decommissioning" states a MUST (a non-empty `Decommission:` field "becomes a BACKLOG item and stays open until the obsolete artifact is removed"), but **`grep -c Decommission scripts/audit.py` = 0** — no detector. **Re-verified.** Asserted-but-unenforced; confirms PB-L. *(Agent's `#199` cross-ref does not exist live → NEW; see §6.)*
- **B2 | :525 | lens1/4 | CONDENSE | JUDGMENT | ADR:87 | BACKLOG:#77** — the self-flagged overlap between the reference-half "Writing prompts" section and numbered §2 is duplication-by-design, honestly flagged; the consolidation is #77's substance. Record under #77, don't re-file.
- **B10 | :849,870,924–927,931,968 | lens3 | CONDENSE | JUDGMENT | ADR:49 | BACKLOG:#77 | hygiene:PB-E** — ~5 in-span "CHANGELOG retired (ADR-49)" annotations; part of the corpus-wide PB-E scatter (see F3 for the blocker).
- **B1, B4, B5, B6, B8, B9, B12 | KEEP** — prompts section reflects ADR-87 (B1); complexity-bands intro correctly re-frames S/M/L as *informal descriptors not declared tiers* (B4), with testing-rules (B5) and VS Code workspace (B6) load-bearing-not-tier-dead; freshness-cadence accurately describes `canonical_freshness` with honest limits (B8); handoff-format-spec is a correct pointer (B12). **B9 (suspected-RECONCILE, refuted):** L895–909 asserts the ADR-88 coherence-spine paradigm as settled — **correct**, because ADR-88 is now Accepted (§6).

### Boundaries & automation (975–1515) — Agent C

- **C1 | :1484–1515 | lens2 | UPDATE-to-current | MACHINE | ADR:85 | BACKLOG:NEW | hygiene:C5**
  "Definition of done (organs)" / "Definition of shipped (closure gate)" cite ADR-81 but make **zero reference to `protocols/DEFINITION_OF_DONE.md`** — the ADR-85 single-source for session-close "done" (`test -e` → present). The scopes are coherent (feature-lifecycle vs session-gate); this is a **missing pointer**, not a contradiction. *(Agent's `#147` cross-ref not found live → NEW; cross-ref hygiene C5.)*
- **C2 | :1035 | lens1 | UPDATE-to-current | JUDGMENT | ADR:37 | BACKLOG:NEW | hygiene:PB-J** — `Why these numbers: observed empirically from 2026-04-24 session`. Refines PB-J: the date is *in* the JOURNAL window (history → 2026-03-29), so not unverifiable — the defect is presenting an n=1 anecdote as "empirical." Reword to "working threshold." Low impact; guideline itself load-bearing.
- **C3–C11 | KEEP** — worktree discipline matches ADR-61 + the seed-state/`--worktree`/`/ship`-refuses facts (C3); no-leftovers invariant is built+gating (C4); tier-1 plugin propagation matches the live `tier1-lifecycle` plugin (C5); two-tier doctrine/ADR-74/80 (C6); routine `Routine:` trailer correctly marked "not built / #123 open" (C7); ADR-68 night-agent correctly marked never-registered, superseded by cloud Routine, ADR-72/73 cited correctly (C8 — reinforces the hygiene §6 refutation that "ADR-72/73 don't exist"); routine-DoD (C9); review-postures (C10); resumption (C11).

### Continuous Improvement + Claude Code internals (1516–1964) — Agent D

- **D1 | :1618,1637 | lens2/3 | UPDATE-to-current | MACHINE | ADR:60 | BACKLOG:#77 | hygiene:PB-C**
  PLAYBOOK says tech-radar "archived to `docs/archive/tech-radar/`" (L1637) and "`docs/tech-radar/` is archived" (L1618). **Re-verified:** `docs/archive/tech-radar` **ABSENT**; `docs/archive/` holds dated research `.md` + README only. The *retirement* is real; the *cited path is wrong* at two sites. Confirms PB-C (+L1618 second site).
- **D2 | :1693–1704 | lens1/2 | UPDATE-to-current | MACHINE | ADR:48 | BACKLOG:#77 | hygiene:PB-G**
  Hooks "auto vs manual" table (self-stamped `1.0 — 2026-06-01`) lists **6** pre-commit hooks; live `.pre-commit-config.yaml` has **10** (adds `toc-freshness`, `toc-freshness-playbook`, `coherence-nudge`, `block-ff-push`) — matching CLAUDE §9. **Re-verified live hook ids.** The table's own caveat ("the filesystem wins — re-ground before trusting") has come true. Confirms PB-G.
- **D3 | :1696–1697 | lens1/3 | UPDATE-to-current | MACHINE | ADR:none | BACKLOG:#77 | hygiene:extends PB-G (NEW)**
  The PB-G table's Claude-Code-hook rows describe a **SessionStart "evolution reminder (rule/correction counts)"** + **Stop "evolution scorecard"** — the retired `/boot`+`/evolve` self-evolution loop (retired 2026-06-05 Phase-C3). **Re-verified live configs:** `~/.claude/settings.json` = SessionStart→`surface-closures.ps1`, Stop→`claude-notify.ps1`, PreToolUse→`block-onedrive.ps1`; **the entire repo `.claude/settings.json` session layer** (`session_end_backpressure.py`, `block_immutable_edits.py`, `fleet_health.py`, `surface_triage.ps1`, `billing_leak_sentinel.ps1`, `changelog_sentinel.py`) is **absent from the table**. NEW (hygiene PB-G covered only the pre-commit side).
- **D4 | :1687 | lens1 | UPDATE-to-current | MACHINE | ADR:none | BACKLOG:NEW | hygiene:CL-C-analog (NEW occurrence)**
  PB-G Skills row tags `| verify | user |`. **Re-verified full scope:** `verify` is **repo-level** — `.claude/skills/verify/verify.py` EXISTS; `~/.claude/skills/` holds only `gotchas`. Re-tag `repo`. *Does not repeat the hygiene-refuted "verify is dead"* — verify exists; the table just mislabels its level. (Related corpus drift, out of scope: CLAUDE §8 still says "no repo-level skills directory exists yet" — `.claude/skills/` now holds `verify` + `check-against-spec`. Flag for CLAUDE groom.)
- **D5 | :1870 | lens4 | UPDATE-to-current | MACHINE | ADR:none | BACKLOG:NEW | hygiene:PB-K** — "Distinct from PLAYBOOK Section 6 Continuous Improvement" — but §6 = "Code Review" (L2628) and Continuous Improvement is **unnumbered** (L1516). Broken internal xref. **Re-verified both headings.** Confirms PB-K. (Contrast: the §5 council xref at L1591 resolves correctly — D agent verified.)
- **D6 | :1671–1680,1774–1782 | lens1/3 | ADD-coverage | MACHINE | ADR:none | BACKLOG:NEW | hygiene:none**
  `/changelog-review` is a live repo command (CLAUDE §7) but **`grep -c changelog-review protocols/PLAYBOOK.md` = 0** — absent from both the PB-G usage table and the 7b command-examples list. **Re-verified.** Coverage gap in the CC-internals reference. NEW.
- **D7 | :1524–1531 | lens1 | UPDATE/JUDGMENT (low-confidence) | ADR:none** — "Six stages" header vs a de-facto 7th "Recording" subsection (L1634). Internally consistent for the *numbered* stages; either renumber Recording as Stage 7 or keep "six + recording note" explicit. Minor; may be intentional.
- **D8, D9, D10 | KEEP** — subagent examples match live `~/.claude/agents/` exactly (D8); D9 = PB-E in-span instances; adoption protocol still accurate, its plugin-distribution thinness is tracked #67 (D10).

### §1–§4 (1965–2301) — Agent E1

- **E1-1 | :2115,2118 | lens1 | UPDATE-to-current | MACHINE | ADR:84(closed) | BACKLOG:NEW | hygiene:PB-H**
  "Model / effort platform doctrine (Claude Code **2.1.x**)"; L2118 pins "Claude Code **2.1.168**". `claude --version` → **`2.1.186`**. **Re-verified.** Stale by 18 patches. **Model *names* are NOT stale** — "Opus 4.8 is the default" (L2120) matches the live lineup; the hypothesized stale-name finding does not materialize. *(The L2118 "#84" reference is a closed/departed item, not a live BACKLOG id → NEW.)*
- **E1-2 | :2062,2107–2113,2122 | lens1 | UPDATE-to-current | MACHINE | ADR:none | BACKLOG:NEW | hygiene:none**
  Effort enum listed as `low / medium / high / xhigh` at three sites. The live effort ladder includes a top **`max`** rung. **Re-verified against this session's own tool schemas** (`effort: 'low' | 'medium' | 'high' | 'xhigh' | 'max'`). Additive UPDATE across the three sites (and a whole-doc sweep — App B, ESSENTIALS, `templates/prompt-template.md` also restate the enum).
- **E1-3 | :2217 | lens3 | UPDATE-to-current | MACHINE | ADR:56 | BACKLOG:NEW | hygiene:none (NEW site, PB-C class)**
  Cites a frozen copy at `templates/archive/handoff-v4/02_METHODOLOGY.md.tmpl`. **Re-verified:** `templates/archive/` holds only `AGENTS-md-template.md`; the live file is `templates/handoff/02_METHODOLOGY.md.tmpl`. Dead-path (same class as PB-C, distinct site). Repoint or drop the frozen-copy clause.
- **E1-4 | :2123 | lens1 | UPDATE/JUDGMENT (low-confidence, unverified) | ADR:80 | BACKLOG:NEW** — `Fast mode … ≈2× token cost`. `/fast` is current and same-model (qualitative claim holds), but the ≈2× cost multiplier is unverified for Opus 4.8 and likely drifted from the 4.6/4.7 era. **Not machine-confirmed either way** — flag for re-verify + `last-verified` stamp, do not assert.
- **E1-5–E1-10 | KEEP** — ADR-29 grandfathering cited correctly ("123 original entries", historical not current-count) (E1-5); lesson-becomes-rule is the canonical home, hygiene-C1 already reconciled (E1-6); **§2's ADR-87 split is faithful word-for-word** to ADR-87 Decision §2, `[A]`/`[CC]` legend tags = the resolved 2026-06-19 contradiction (E1-7); Dynamic Workflow / `ultracode` current (E1-8); ADR-56 Prompt-Generation-Card (E1-9, apply E1-3 path-fix); §1 scaffold (E1-10, optional nit: L2034 shows a **bare `git merge`, not `--no-ff`** — illustrative greenfield, but harmonizing it with core-invariant #5 would help).

### §5 Council / ADR (2302–2627) — Agent E2

- **E2-1 | :2473–2535 | lens2 | RECONCILE-with-ADR | MACHINE | ADR:77 | BACKLOG:#112 | hygiene:none**
  The Amendment-vs-Reopen protocol describes only the **manual in-file-marker** path and makes no mention of the BACKLOG #112 `adr_amend.py` helper-only path. **Re-verified:** `scripts/adr_amend.py` and `scripts/hooks/adr_amend.py` both **ABSENT**; **#112 OPEN**. So §5 honestly describes *current* practice (the helper doesn't exist yet — **good**, no false-enforcement claim). The reconcile is forward-looking: when #112 lands, §5 must flip to "helper-only" (#112 explicitly names "resolve the CLAUDE.md §5 self-contradiction"; PLAYBOOK §5 is a sibling site, `serialize-group: claude-md`).
- **E2-2 | :2503–2506 | lens1 | UPDATE-to-current | MACHINE | ADR:88 | BACKLOG:NEW** — §5 prescribes the amendment block as a **blockquote** (`> **Amendment YYYY-MM-DD…**`); the two live 2026-06-21 worked examples (ADR-88/89) use an **H2 heading** form (`## Amendment — 2026-06-21: Accepted…`) + inline status-flip. **Re-verified the live form** (§6). Core mechanism matches (append-only, original frozen); the literal template diverges from real practice. UPDATE the template or note both acceptable.
- **E2-4 | :2350–2361 | lens2 | RECONCILE/JUDGMENT | MACHINE(ADR-67 facts) | ADR:67 | BACKLOG:none** — bare `council-cli` examples predate ADR-67's `/council-question` entry point; partially absorbed by the L2307 pointer to `AI_COUNCIL_PROCESS.md`. Low severity; consider naming `/council-question` as the current trigger.
- **E2-5 | :2537–2624 | lens3 | KEEP | MACHINE | ADR:54 | hygiene:PB-7(refuted)** — Codex review archival protocol is fully live. **Re-verified full scope:** `~/.claude/commands/codex-review.md` EXISTS; ~29 archived `docs/audits/*codex*` files; the protocol's target path matches the live command's output. **Explicitly confirms the hygiene §6 refutation of PB-7** ("retired tool → REMOVE" — REFUTED). Do NOT remove.
- **E2-3 | CONDENSE (=PB-E)**; **E2-6, E2-7 | KEEP** — council-archival reconciles with ADR-43 (`docs/decisions/transcripts/` populated; `docs/research/` correctly absent) (E2-6); post-debate ADR-in-CC authorship (E2-7).

### §6–§19 + appendices (2628–3352) — Agent F

- **F1/F2 | :2929,2938 | lens1/2 | UPDATE-to-current | MACHINE | ADR:32 | BACKLOG:#77 | hygiene:PB-D**
  §14's own `> **STALE — Handoff and Snapshots/reports rows**` blockquote admits the Handoff row predates the folder format and the Snapshots "delete after 90 days" lifecycle "does not match practice (audits kept indefinitely)." **Re-verified L2929 verbatim.** Confirms PB-D. Self-declared known-stale.
- **F3 | :2926–2944 | lens1 | ADD-coverage | MACHINE | ADR:49 | BACKLOG:NEW | hygiene:PB-E (enabler)**
  **§14 Markdown Governance contains NO canonical "CHANGELOG retired (ADR-49)" statement** (`awk 2926–2975 | grep -i changelog` → no match). **Re-verified.** The PB-E condense (collapse ~19 scattered annotations to one canonical home) is **blocked** until the canonical statement is *added* to §14 first. This is the structural prerequisite PB-E omitted.
- **F4 | :3083–3157 | lens2 | RECONCILE-with-ADR | MACHINE | ADR:63 | BACKLOG:NEW | hygiene:none**
  §19 Scrum-Master Review Propagation cites **zero** authorizing ADR (`grep -c ADR-63` over the span = 0). Its governing ADR is **ADR-63** (Accepted 2026-05-30, N=3 — superseding the Reserved ADR-44 N=2 hold). **Re-verified.** §19 correctly does *not* claim ADR-44 authority, but fails to cite ADR-63. Add the citation. (Related index drift, out of span: the ADR-44 README row still points to "PLAYBOOK §17" while the content lives in §19.)
- **F6 | :2814 | lens1 | UPDATE-to-current | MACHINE | ADR:66 | BACKLOG:none** — §10 says quarterly grooming "first review: **2026-07-01**" (8 days out). A one-time "first review" date silently rots into a past date; reword to a recurring cadence. Same false-precision class as PB-J.
- **F5 | :3126 | lens2 | UPDATE/JUDGMENT (low-confidence) | ADR:43 | BACKLOG:NEW** — §19 labels a column "Cross-repo amendment handshake **(ADR-43 pattern)**", but ADR-43 = "Cross-project transcript routing", not an amendment handshake. Possible mis-cite or loose analogy. Verify the intended ADR or reword.
- **F7–F19 | KEEP** — **§8 Handoff correctly describes v5.2** (CC-owned residual + thin boot, ADR-82-by-waiver; exemplary summarize-then-point) (F7); BACKLOG grooming schema + `validate_backlog.py` live (F8); context-budget read-scoping (F9); render-layer rationale→CLAUDE §4 split (F10); **codemap (F11) and auto-TOC (F12) tools confirmed live**; App B defers to live `ROUTING.md` (F13); App A shortcuts carry no version stamp + remain accurate (F14); App C token doctrine current (F15); cross-tool/code-review/code-quality reviewer roles (F16–F18); §19 is load-bearing (F19; its ADR-citation gaps are F4/F5).

---

## §3 — Harmony-coverage analysis (lens 5, Agent G)

**Verdict: ADEQUATE-with-correct-delegation** (one minor JUDGMENT-level vocab gap). A fresh CC session reading PLAYBOOK reaches every load-bearing L1 fact via an explicit pointer.

**Correct delegation — credited, NOT flagged** (this is the repo's anti-drift reason-to-exist):
- **L221 System Architecture** hands the 3-layer model, the diagram, the authority chain, and the Layer-2 invariants to `ARCHITECTURE.md` Ch1 and states *why* it does not restate them ("a resident copy is exactly the drift this repo exists to kill"). Verified against ARCHITECTURE Ch1 (the mermaid + invariants are present there).
- **L2044–2052 "Architect output vs CC consumption-spec"** is the one place PLAYBOOK is *meant* to be canonical (per ADR-87); it carries the full emit-split. Correct **ownership**, not a gap.
- **L2695 §8** delegates mode-awareness to HANDOFF_PROCESS §13, the residual to §2/§5, Roles to ESSENTIALS § Roles — each naming "resident-copy drift" as its failure mode. All targets confirmed live.

**ADD-coverage finding:**
- **G1 | whole-doc (hooks L523/L2044/L2695) | ADD-coverage | JUDGMENT | ADR:28,87 | BACKLOG:#162**
  PLAYBOOK uses "architect" **exclusively as the Layer-1 actor** ("browser is architect, CC is executor" L523; "the command the architect hands the operator" L1163; "Architect output vs CC consumption-spec" L2044). The orthogonal **handoff *mode*** sense (architect|execution) is explicitly delegated out at L2695 ("not described here"). So PLAYBOOK is internally clean (single-sense) and does **not create** the #162 collision — but it offers no one-line signpost that "architect" is overloaded elsewhere (HANDOFF_BOOT "Architect mode"). A reader who meets "architect mode" elsewhere gets no bridge from PLAYBOOK. **This is the already-tracked #162 vocab decision** ("disambiguate atomically across all enumerated surfaces"); PLAYBOOK is one enumerated surface. Low severity — the fix is the #162 atomic ruling, not a PLAYBOOK-local patch.

**Whole-doc harmony observations (cross-surface, watch-for-drift):**
1. **ROUTING.md ↔ §2 model default (real contradiction).** `~/.claude/ROUTING.md` (canonical, App-B-deferred) still encodes Sonnet-default routing; §2 "How to choose Model" (L2065–2073) + platform doctrine (L2120) say Opus-4.8-default/floor. The two surfaces disagree on the default. ROUTING.md is the stale one. (Out of PLAYBOOK's edit-scope, but PLAYBOOK App B points at it.)
2. **Effort-enum `max` sweep (E1-2)** is whole-document — App B, ESSENTIALS, `templates/prompt-template.md` all restate `xhigh`-without-`max`.
3. **CHANGELOG-retired scatter (PB-E)** is whole-document; **F3** is the enabling prerequisite (add the canonical statement to §14 before collapsing the scatter).
4. **Amendment-format coherence cluster (E2-2)** — PLAYBOOK §5 (blockquote) vs CLAUDE §5 (critical rule) vs the actual ADR files (heading form); `#112 serialize-group: claude-md` is the declared edge meant to reconcile them.

---

## §4 — Roll-up tables

**Table A — material findings (non-KEEP), by verdict**

| ID | Location | Verdict | Conf | ADR | BACKLOG | Hygiene |
|---|---|---|---|---|---|---|
| B3 | :818 | REMOVE-candidate | M | 40 | #77 | PB-A |
| A1 | :4 | UPDATE | M | — | NEW | — |
| A10 | :494,501 | UPDATE | M | 33,34 | NEW | PB-I |
| C2 | :1035 | UPDATE | J | 37 | NEW | PB-J |
| D1 | :1618,1637 | UPDATE | M | 60 | #77 | PB-C |
| D2 | :1693 | UPDATE | M | 48 | #77 | PB-G |
| D3 | :1696 | UPDATE | M | — | #77 | PB-G(ext) |
| D4 | :1687 | UPDATE | M | — | NEW | CL-C-analog |
| D5 | :1870 | UPDATE | M | — | NEW | PB-K |
| E1-1 | :2118 | UPDATE | M | 84(closed) | NEW | PB-H |
| E1-2 | :2062,2107 | UPDATE | M | — | NEW | — |
| E1-3 | :2217 | UPDATE | M | 56 | NEW | — |
| E2-2 | :2503 | UPDATE | M | 88 | NEW | — |
| F1/F2 | :2929,2938 | UPDATE | M | 32 | #77 | PB-D |
| F6 | :2814 | UPDATE | M | 66 | — | — |
| E2-1 | :2473 | RECONCILE | M | 77 | #112 | — |
| E2-4 | :2350 | RECONCILE | J/M | 67 | — | — |
| F4 | :3083 | RECONCILE | M | 63 | NEW | — |
| B11 | :941 | PROMOTE | M | — | NEW | PB-L |
| D6 | :1671 | ADD | M | — | NEW | — |
| F3 | :2926 | ADD | M | 49 | NEW | PB-E |
| G1 | whole | ADD | J | 28,87 | #162 | — |
| B2 | :525 | CONDENSE | J | 87 | #77 | — |
| B10/D9/E2-3 | multi | CONDENSE | J | 49 | #77 | PB-E |
| D7 | :1524 | UPDATE? | J | — | — | — |
| E1-4 | :2123 | UPDATE? | J(unverified) | 80 | NEW | — |
| F5 | :3126 | UPDATE? | J | 43 | NEW | — |

**Table B — REMOVE-candidates (need per-item operator approval + confirm-live before removal)**

| ID | What | Caveat |
|---|---|---|
| B3 (=PB-A) | `### Tier transition procedures (ADR-40) — DEPRECATED` (L818–829) | Preserve the regression-guard intent as a one-liner if removed. |

**Table C — RECONCILE-with-ADR (incl. the Proposed-vs-settled check)**

| ID | Section | ADR | Reconcile note |
|---|---|---|---|
| E2-1 | §5 amendment protocol | 77 / #112 | Honest today (manual path; helper absent); flip to helper-only when #112 lands. |
| F4 | §19 scrum-master | 63 | Add the missing ADR-63 authority citation. |
| E2-4 | §5 council-cli | 67 | Name `/council-question` as the current trigger. |
| *(no finding)* | §Repo-conv L505 / §doc-types L895 | 88, 89 | **Suspected Proposed-asserted-as-settled — REFUTED.** ADR-88/89 are Accepted (§6); the assertions are correct. |

**Table D — ADD-coverage**

| ID | Gap | Maps to |
|---|---|---|
| D6 | `/changelog-review` absent from CC-internals command lists | NEW (or #67) |
| F3 | §14 lacks the canonical "CHANGELOG retired" statement (blocks the PB-E collapse) | NEW |
| G1 | No signpost that "architect" is overloaded (actor vs mode) elsewhere | #162 |

---

## §5 — New-vs-known

**Fidelity-NEW (not in the hygiene audit's PB-A…PB-L):**
- **A1** — PLAYBOOK header `Last updated` drift (and the fact that PLAYBOOK is outside the `canonical_freshness` gate).
- **D3** — the PB-G table's CC-hook rows describe retired `/boot`+`/evolve` machinery and omit the entire repo-level session-hook layer (hygiene PB-G covered only the pre-commit side).
- **D4** — PLAYBOOK PB-G table mislabels `verify` as user-level (distinct PLAYBOOK occurrence of the hygiene CL-C class).
- **D6** — `/changelog-review` undocumented in PLAYBOOK.
- **E1-1** — the CC version pin is *numerically* stale (PB-H only asked for a `last-verified` marker).
- **E1-2** — effort enum missing `max`.
- **E1-3** — dead `templates/archive/handoff-v4/` path (PB-C class, new site).
- **E2-1 / E2-2** — §5 amendment protocol: no #112 forward-pointer; blockquote-vs-heading format divergence.
- **F3** — §14 lacks the canonical CHANGELOG statement (the structural blocker PB-E omitted).
- **F4 / F6** — §19 missing ADR-63 citation; §10 "first review" date rot.
- **C1** — DoD section missing the `DEFINITION_OF_DONE.md` pointer.
- **G1 + the ROUTING.md/§2 contradiction** — harmony-layer.

**Known (confirmed + fidelity-lensed, already tracked):** PB-A→B3 (#77), PB-B→B7, PB-C→D1 (#77), PB-D→F1/F2 (#77), PB-E→B10/D9/E2-3+F3 (#77), PB-G→D2 (#77), PB-H→E1-1, PB-I→A10, PB-J→C2, PB-K→D5, PB-L→B11. Most UPDATE/CONDENSE items fall under the open **#77** protocols-consolidation umbrella (itself CLOSURE-VOIDED 2026-06-09 — still live).

**Related corpus drift surfaced (out of PLAYBOOK scope — for the relevant owner, not this audit's edits):**
- **CLAUDE §11 + the audit brief + README prose** still call ADR-88/89 "Proposed" — they are Accepted (§6).
- **CLAUDE §8** states "no repo-level skills directory exists yet" — `.claude/skills/` now holds `verify` + `check-against-spec`.
- **ADR-44 README row** points to "PLAYBOOK §17"; scrum-master content lives in §19.
- **`~/.claude/ROUTING.md`** Sonnet-default contradicts the Opus-4.8-default doctrine.

---

## §6 — Confidence ledger (the integrity record)

Unlike the hygiene audit (which refuted 6 of its own agents' MACHINE claims), **no Phase-1 agent existence-claim was refuted on orchestrator re-verification** — every "dead/missing/stale" claim was re-checked in full scope (`~/.claude/` AND repo, both filename conventions) and held. Crediting the cause: the agents were given the full-scope confirm-live instruction + the §6 lesson upfront. What re-verification *did* correct:

1. **Brief premise REFUTED — ADR-88/89 are Accepted, not Proposed.** The audit brief, CLAUDE §11, and the README prose ("acceptance pending") all say "Proposed." **Re-verified:** both ADRs carry an in-file operator-ratified amendment `## Amendment — 2026-06-21: Accepted (operator ratification)` (ADR-88:167, ADR-89:306), committed by **`911b561` (2026-06-21 17:02), confirmed on `main`** (`git branch --contains`). Their *frozen* `**Status:** Proposed` headers are unchanged by the immutability convention; the README index carries no status prefix (convention-consistent with Accepted). **Consequence:** the two PLAYBOOK sections suspected of asserting a Proposed ADR as settled (B9 L895–909, A11 L505) are **correct → KEEP, not RECONCILE.** *(Meta: the stale "Proposed" premise is itself an instance of ADR-88's FC1 failure class — "accepting inherited framing without verifying state.")*
2. **Agent BACKLOG-id mis-assignments corrected** (the findings stand; the cross-ref ids were wrong):
   - **E1-1** cited `#84` — closed/departed (the platform-max audit completed; the L2118 text quotes "#84" as provenance) → finding is **NEW**.
   - **C1** cited `#147` — not found live → **NEW** (cross-ref hygiene C5).
   - **B11** cited `#199` — not found live → **NEW** (cross-ref hygiene PB-L).
3. **A10 nuance added:** ADR-33 = "VISION universalization", which does **not** govern a secrets path, so the L494 `[TBD]` is *mis-tagged*, not a clean stale forward-pointer — PB-I's "just resolve them" needs a topic-vs-ADR decision.
4. **Count nit:** an agent said "30 archived codex reviews"; actual `ls | grep -c codex` = **29**. Immaterial (both confirm "many"; PB-7-refutation stands).
5. **E1-4 (fast-mode ≈2× cost) is UNVERIFIED** — relied on an external guide, not machine-confirmed. Carried as low-confidence JUDGMENT, **not** asserted as fact.

---

## §7 — Proposed RESTRUCTURE recommendation (recommendation only, not executed)

**Recommendation: do NOT undertake a large two-halves restructure.** The "two-documents-glued" form (unnumbered Foundations reference chapters 218–1963 + numbered §1–§19 recipes 1965–3157 + appendices 3159–3352) is **comprehension-aiding, not a defect**, because:
- The **maintained auto-TOC** (L14–216, freshness-gated) indexes both halves, so navigation does not depend on a uniform numbering scheme.
- The split is semantically real: Foundations = *doctrine/reference*; §1–§19 = *step-by-step recipes*. A reader looking for "how do I write a prompt" finds §2; a reader looking for "what is CLAUDE.md" finds the Foundations chapter. Merging them would lose that.
- Length is not the target (the brief is explicit); **currency and fidelity are** — and those are addressable by the localized fixes in §2, not by re-architecting.

**Targeted legibility improvements that ARE warranted** (each a small, per-item-approved edit in the separate cleanup arc, re-confirmed live first):
1. **Single `last-verified: YYYY-MM-DD` stamp** on the platform-doctrine block (L2115–2123) so the CC-version / model / effort / fast-mode pins drift visibly (addresses E1-1/E1-2/E1-4 + PB-H as a class).
2. **Re-ground the PB-G hooks table** (L1693) to the live 10-hook pre-commit set + the live session-hook layer, or replace the enumerated table with a pointer to CLAUDE §9 (the canonical roster) to stop the table re-drifting (D2/D3).
3. **Add the canonical "CHANGELOG retired (ADR-49)" statement to §14** (F3), *then* collapse the ~19 scattered annotations to pointers (PB-E) — in that order.
4. **Fix the broken internal pointers** (D5 §6-xref; F4 add ADR-63; B7/F1/F2/D1 path+label corrections) — mechanical, low-risk.
5. **Resolve the two `[TBD]` placeholders** (A10) with the topic-vs-ADR decision, not a blind ADR-33/34 substitution.

**One structural consideration deferred to the operator:** whether to bring PLAYBOOK under a machine freshness signal (it is currently outside `canonical_freshness`; A1 went undetected). That is an `audit.py` scope decision, not a PLAYBOOK edit, and is noted, not recommended.

---

*Diagnostic only. No PLAYBOOK content was edited. Every REMOVE/UPDATE above must be re-confirmed live at the moment the separate, operator-approved cleanup arc acts on it.*
