# ARCHITECTURE Fidelity Audit — 2026-06-23

> **Scope:** `ARCHITECTURE.md` (604 L), the doc that `PLAYBOOK.md` **delegates** the 3-layer model,
> the authority chain, and the Layer-2 invariants to. This audit verifies that **delegation target is
> sound** — same fidelity lens as the same-day PLAYBOOK fidelity audit (`855f748`), adapted.
> **Distinct from** the same-day HYGIENE audit (`docs/audits/2026-06-23-canonical-corpus-coherence-audit.md`,
> findings AR-A…AR-D), which asked *"is this line stale/dead/duplicated?"* This audit cross-references
> those findings and adds the fidelity lens; it does **not** re-derive them.
> **Distinct from** the PLAYBOOK fidelity audit, whose §3 *credited* ARCHITECTURE Ch1 as the canonical
> home; this audit checks that credit is earned.
> **Diagnostic only** — no ARCHITECTURE edit, no removal. Removals are a separate per-item operator-approved arc.
> **Method:** 4 read-only section agents tiling lines 1–604 with zero gaps (A–D apply lenses 1–4 span-local
> + emit lens-5 signals), then **orchestrator re-verification of every high-impact / novel MACHINE claim**
> (the hygiene audit's load-bearing lesson — it refuted 6 of its own agents' wrong-scope claims), and the
> **whole-doc lens-5 delegation-soundness verdict is orchestrator-owned** (like the PLAYBOOK audit's Agent G).
> Run from worktree `worktree-architecture-fidelity`, refreshed in place to main `a39e416`.

---

## §0 — Headline

**Overall fidelity verdict: HIGH.** ARCHITECTURE.md describes the system as it currently IS. Across
604 lines the audit found **0 REMOVE-candidates**, **0 inaccurate/contradicted claims**, and only
**4 material non-KEEP findings** — all UPDATE / ADD-coverage / cross-ref-confirm class, none blocking.

**Delegation-soundness verdict (lens 5, whole-doc): SOUND.** Every load-bearing fact PLAYBOOK
delegates here — the **3-layer model**, the **authority chain**, the **Layer-2 invariants**, and the
**safety invariants** — is *present, complete, correct, and current* in ARCHITECTURE, sourced to its
governing ADR. The PLAYBOOK fidelity audit's §3 credit ("ARCHITECTURE Ch1 is the canonical home; a
resident copy is exactly the drift this repo exists to kill") is **earned**. (§3.)

**Highest-confidence drift (all minor):**
- **AR-A (cross-ref, MACHINE):** the harmony content lives in *prose* but the frontmatter declares no
  `reconciled_with: handoff-process@5.2` edge — the known #172 coherence-spine gap; ARCHITECTURE is a
  prime declare-candidate. *(Affects formal edge-tracking, not prose accuracy.)*
- **GA-1 (NEW, JUDGMENT):** the curated Governing-ADRs list (L583–600) stops at **ADR-84**, omitting
  ADR-85–89 — including the **ADR-88/89 legibility ADRs the doc itself heavily cites in Ch2**. ADD-coverage.
- **AR-B (cross-ref, JUDGMENT/low):** one bare ``HANDOFF_PROCESS.md`` at **L564** (other refs are §-qualified
  or path-qualified). Hygiene cited L534; the actual bare ref is L564 (line drift). Style consistency.

**Counts:** 11 sections (5 `[CORE]`) · 4 generated/maintained regions verified-as-generated (not hand-audited) ·
findings: **KEEP ≈ 30** (consolidated), **UPDATE/ADD/PROMOTE = 3** (AR-A, GA-1, AR-B) + **1 NEW code-conformance
side-note** (out of strict scope) · **REMOVE-candidates = 0**.

---

## §1 — Phase-0 machine baseline (lead, read-only; all re-verifiable)

| Probe | Command | Result |
|---|---|---|
| Worktree currency | `git merge --ff-only main` | refreshed in place `5d10cfc → a39e416` (zero orphan; native branch kept) |
| ARCHITECTURE size/stability | `wc -l`; `git log 5d10cfc..a39e416 -- ARCHITECTURE.md` | **604 L**, untouched since `5d10cfc` (Phase-2 edits already baked at `3103340`) |
| Registered checks | `py -m scripts.audit checks` | **23** (last = `doc_code_edge`) |
| Self-conformance | `py -m scripts.audit health` | **OK** |
| pytest collect (claim-3) | `py -m pytest --collect-only -q` | **800** — claim-3 reconciled (was 793 at hygiene-audit time; `3103340` moved it) |
| doc self-claims | health → `doc_claims` | **3/3 match** repo state |
| doc→code edges | health → `doc_code_edge` | **5 resolved, none broken/ambiguous** |
| reconciled_with edges | health → `reconciled_versions` | **1 edge matches** live spec version |
| codemap + both TOC freshness | `codemap.cli check`; `toc.cli check` ×2 | **clean** (benign orphan-module warning only) |
| undeclared edges (AR-A) | `py scripts/scan_undeclared_edges.py` | **ARCHITECTURE → handoff-process (tier 1) LIVE** — AR-A confirmed |
| Phase-2 edits landed | `git show --stat 3103340` | ARCHITECTURE **+32 L** + `test_legibility_graph_conformance.py` **+293 L** |
| FF commits on main (AR-D) | health → `no_ff_merges` | **2** (`3a894eeb5`, `d0f9ead67`, 2026-06-19) — grandfathered, KEEP |

**Prior-audit cross-ref base loaded:** hygiene AR-A…AR-D + KEEP-healthy block; PLAYBOOK fidelity §3
delegation credits. This audit confirms AR-A, AR-B, AR-C, AR-D on re-verification and adds the fidelity
lens; it does not re-surface them as new.

**Encoding note (gotcha):** `scripts/audit.py checks` crashes on Windows cp1252 emitting the `→` glyph;
all baseline commands were run with `export PYTHONIOENCODING=utf-8`. (Pre-existing tooling gotcha, not
an ARCHITECTURE finding.)

---

## §2 — Per-section findings (the spine)

Format: `ID | ARCHITECTURE.md:line | lens | VERDICT | conf | ADR | BACKLOG | hygiene-xref`.
Orchestrator re-verification noted where I personally re-ran the command.

### Span A — frontmatter + Purpose + Codemap + Layer Boundaries + Authority (L1–175, Ch1)

- **A-KEEP (harmony core) | :89–141 | lens1/2/3/5 | KEEP | MACHINE+JUDGMENT | ADR:28,36,29,39,31,63,69 | — | —**
  The 3-layer model + mermaid (L96–120), the authority chain ("architect proposes; **operator is the
  consent gate**; the architect never executes" L122–128), and the five Layer-2 invariants (L129–141,
  incl. "Layer 2 never executes" + validators-read-only + append-only + dated-immutable) are all present,
  current, and sourced. Cited ADRs all Accepted. **This is the harmony core — see §3.**
- **A-GEN | :32–45, :69–85 | lens4 | KEEP-as-generated | MACHINE | ADR:51,50,59,60 | — | —**
  Auto-TOC + CODEMAP mermaid fence markers intact; `toc.cli check` and `codemap.cli check` pass.
  Verified-as-generated, not hand-audited.
- **AR-A | :1–5 (frontmatter) | lens1/3 | PROMOTE/UPDATE | MACHINE | ADR:88 | BACKLOG:#172 | hygiene:AR-A**
  No `reconciled_with: handoff-process@5.2`. `scan_undeclared_edges` → ARCHITECTURE→handoff-process tier-1.
  **Re-verified by orchestrator.** Prose is correct; the edge is merely undeclared (the #172 spine gap).
- Purpose (L47) + Authority and governance (L150) — **KEEP**; prose matches ADR-31/36/63/69, tier-system
  retirement noted per ADR-38 A5.

### Span B — Organ map + Validators & enforcement (L176–379, Ch2)

- **B-KEEP (organ/validator inventory) | :176–336 | lens1/2/3 | KEEP | MACHINE | ADR:28,36,66,69,77,85 | — | hygiene:KEEP-healthy**
  Organ map and Validators section match live state: **23 registered checks** named/consistent; **10
  pre-commit hooks** match `.pre-commit-config.yaml`; every named validator script exists in `scripts/`;
  all are read-only (Layer-2 invariant holds). `validate_no_ff` (WARN) / `block_ff_push` (pre-push prevent)
  pair correctly described (L252–271). **Re-verified: 23 / 10 / 800 all live.**
- **B-GEN (legibility graph) | :338–357 | lens3 | KEEP-as-maintained | MACHINE | ADR:88,89 | BACKLOG:#194,#195 | —**
  The conformance map (landed `3103340`, +32 L) is internally consistent with the four edge-validators it
  documents (`validate_reconciliation` / `validate_doc_code_edge` / `scan_undeclared_edges` /
  `reverse_dep_oracle`); "4/4 PROVEN this env" tally matches (code↔code skipif-guarded). Not hand-audited.
- **B-CLAIM3 | :367 | lens1 | KEEP | MACHINE | — | — | —** "800 collected" matches live
  `pytest --collect-only`; gate-covered by `check_doc_claims`. **Re-verified.**

### Span C — Automation axes + Distribution & transfer + Key conventions & zones (L380–513, Ch3–5)

- **C-KEEP | :380–513 | lens1/2/5 | KEEP | MACHINE | ADR:70,74,80,84,78,75,77,39,53,34,59 | BACKLOG:#123,#121 | —**
  Two-tier (judgment) axis correctly orthogonal to the ADR-70/74 friction tiers (L391–392); automation-writer
  isolation matches ADR-84 live (`automation/conformance-digest` + `automation/fleet-audit`; `surface_triage.ps1`
  reads `?ref=automation/conformance-digest`); `tier1-lifecycle` plugin carriers + child methodology-floor
  wiring (`generate_floor.py`, `methodology_surface` zone) live; the **zone register + "no organ = decoration"**
  (L499–507) is sound, every zone has a live enforcing organ. Spec-orchestration fallback accurate as of the
  2026-06-05 re-probe (L425–431).
- **NEW-1 (code-conformance side-note, OUT OF STRICT SCOPE) | conformance-hub.js:167,192 | lens1 | (ARCHITECTURE=KEEP) | MACHINE | ADR:70,80 | BACKLOG:NEW | —**
  ARCHITECTURE L419–423 ("**Unpinned fan-out is a bug** — inherits the main session model (Opus 4.8)") is an
  **accurate doctrine statement** (KEEP). Surfaced while verifying it: `.claude/workflows/conformance-hub.js`
  pins only the 3 verifiers (`model: 'claude-sonnet-4-6'`, L150–152); the **skeptic (L167) and digest (L192)
  agent() calls carry no `model:`** — they rely on Opus-4.8 *inheritance* (meta.phases L6–7 explicitly say
  "(Opus)", so the effect matches intent). Per the doctrine's strict letter this is "unpinned" — a minor code
  hardening, not an ARCHITECTURE fidelity defect. **Re-verified by orchestrator** (`grep -n agent( conformance-hub.js`).

### Span D — Verification mesh & decision flow + Governing ADRs + footer (L514–604, Ch6)

- **D-KEEP (verification mesh / decision flow / supersession) | :514–576 | lens1/5 | KEEP | MACHINE | ADR:84,67,43,68,72,76,80,85 | BACKLOG:#85 | —**
  Five-layer verification mesh, nightly outcome loop (ADR-84 branch discipline), Council decision flow
  (ADR-67/43), and the ADR-68 supersession-in-reality note are all accurate and live. ADR-85 correctly
  *scoped out* of the mesh (it governs session-end lifecycle, a separate layer) — a correct boundary, not a gap.
- **GA-1 | :583–600 (Governing ADRs) | lens1/4 | ADD-coverage | JUDGMENT | ADR:85,86,87,88,89 | BACKLOG:NEW | —**
  The curated list stops at **ADR-84**; ADR-85 (session-gate), 86 (conformance dashboard), 87 (architect↔CC),
  and **88/89 (the legibility ADRs cited 9× in Ch2)** are absent. The "curated, not exhaustive" caveat (L579)
  makes this defensible, but the omission of the doc's own most-cited recent governing ADRs is the one
  coverage gap worth a groom. **Re-verified: ARCHITECTURE cites 88/89 in Ch2; no "Proposed" string anywhere.**
- **AR-B | :564 | lens4 | UPDATE-to-current | JUDGMENT/low | ADR:82 | BACKLOG:NEW | hygiene:AR-B**
  ``context → Handoff v5 (`HANDOFF_PROCESS.md`, ADR-82)`` — bare filename, no `protocols/` prefix. **Re-verified:
  exactly one bare occurrence (L564), not L534 as hygiene cited (line drift).** Style consistency, not semantic.
- **D-ADR82 (NOT a finding) | :592 | lens2 | KEEP | MACHINE | ADR:82 | — | —**
  ARCHITECTURE says "ADR-82, canonical 2026-06-11" — **accurate** (operator-waiver flip #149). The ADR-82
  *file header* still reads "Status: Proposed" by the **frozen-header immutability convention** (in-place marker
  L11) — identical to the ADR-88/89 pattern. ARCHITECTURE reflects the real status; no drift here.
- **D-footer | :604 | lens4 | KEEP | MACHINE | — | — | —** "Maintained by: Rob" current (`git log -1` author = robdwornik).

---

## §3 — Delegation-soundness analysis (lens 5 — whole-doc, orchestrator-owned)

**Verdict: SOUND.** PLAYBOOK delegates four things to ARCHITECTURE; all four land:

| Delegated content | PLAYBOOK pointer | In ARCHITECTURE? | Evidence (re-verified) |
|---|---|---|---|
| **3-layer model + diagram** | L221 → "ARCHITECTURE Ch1" | ✅ present/correct/current | mermaid L96–120 (browser-architect → operator → CC executor → Layer-2 reads); matches ADR-28 |
| **Authority chain** | L221 | ✅ present/correct | L122–128 "architect proposes; operator is the consent gate; architect never executes" |
| **Layer-2 invariants** | L221 | ✅ present/correct/backed | five invariants L129–141; **backed by** the 23-check read-only validator inventory (Span B) — "Layer 2 never executes" holds (no mutation code in `scripts/*.py`) |
| **Safety invariants** | (zones / floor) | ✅ present/correct/enforced | zone register L499–507 (P0 exclusion, immutable-paths, `methodology_surface`); every zone has a live enforcing organ |

**Why the credit is earned:** the PLAYBOOK fidelity audit's §3 explicitly declined to restate this content
("a resident copy is exactly the drift this repo exists to kill") and pointed here instead. The target is
accurate, so the delegation is not just clean *structurally* — it is clean *in substance*. A fresh CC
session that follows PLAYBOOK's pointer reaches a correct, current model of the system.

**The one soundness caveat (formal, not substantive):** the harmony content is carried in **prose**, but the
machine-readable `reconciled_with` edge that would let the coherence spine *verify* ARCHITECTURE stays in
step with `handoff-process` is **undeclared** (AR-A / #172). So today the delegation target's *currency* is
protected by the freshness gate (`last_reviewed`) and human review, not by the declared-edge machinery that
ADR-88 exists to provide. Declaring the edge (#172) would close the gap between "the prose is right" and "a
machine proves the prose stays right." This is the single highest-leverage follow-up.

**Whole-doc harmony observations (watch-for-drift, not defects):**
1. **Governing-ADRs list lag (GA-1).** The doc's curated ADR roster trails its own body by 5 ADRs; the body
   cites 88/89 as binding while the roster omits them. Cosmetic today; a drift vector if the roster is ever
   treated as the authority (it explicitly defers to `docs/decisions/README.md`, which mitigates).
2. **Frozen-header convention is load-bearing and undocumented in-doc.** ADR-82/88/89 all show header
   "Proposed" while being canonical/Accepted; the real status lives in in-place markers + the index. The
   audit (and any reader) must know this convention to reconcile ARCHITECTURE's "canonical"/Accepted claims
   against the ADR files. ARCHITECTURE is correct; the convention is just easy to trip over. *(Already an
   established repo memory: ADR-index status-prefix convention.)*

---

## §4 — Roll-up tables

**Table A — material findings (non-KEEP), by verdict**

| ID | Location | Verdict | Conf | ADR | BACKLOG | Hygiene |
|---|---|---|---|---|---|---|
| AR-A | :1–5 frontmatter | PROMOTE/UPDATE | M | 88 | #172 | AR-A |
| GA-1 | :583–600 | ADD-coverage | J | 85–89 | NEW | — |
| AR-B | :564 | UPDATE-to-current | J/low | 82 | NEW | AR-B |
| NEW-1 | conformance-hub.js:167,192 (ARCHITECTURE=KEEP) | code-conformance (out of strict scope) | M | 70,80 | NEW | — |

**Table B — REMOVE-candidates (need per-item operator approval + confirm-live before removal)**

| ID | What | Caveat |
|---|---|---|
| *(none)* | — | **No REMOVE-candidates.** No dead/superseded/aspirational prose found in ARCHITECTURE; the ADR-68 supersession + the 2 grandfathered FF commits are correctly *labelled* historical, not stale. Strong signal. |

**Table C — RECONCILE-with-ADR (incl. the Proposed-vs-settled check)**

| Section | ADR | Reconcile note |
|---|---|---|
| Ch2 legibility / Governing ADRs | 88, 89 | **Accepted** (`911b561` in-place markers). ARCHITECTURE cites them as binding doctrine, **no "Proposed" string present** — correct. *(Frozen header L5 says Proposed by immutability convention — not a finding.)* |
| Governing ADRs :592 / mesh :555 | 82, 84 | ARCHITECTURE "canonical 2026-06-11" / "Accepted" — both match index. Correct. |
| Governing ADRs (omission) | 40 | ADR-40 **Deprecated** (2026-05-23) — correctly **omitted** from Governing ADRs. Correct. |

**Table D — ADD-coverage**

| ID | Gap | Maps to |
|---|---|---|
| GA-1 | Curated Governing-ADRs roster stops at ADR-84; omits 85–89 (incl. body-cited 88/89) | NEW |
| AR-A | No declared `reconciled_with: handoff-process@5.2` edge for the harmony content | #172 |

---

## §5 — New-vs-known

**Confirmed-from-prior-audits (cross-ref, NOT re-derived):**
- **AR-A** (undeclared handoff-process edge, #172) — re-verified live.
- **AR-B** (bare `HANDOFF_PROCESS.md`) — re-verified; **corrected line number L534 → L564**.
- **AR-C** (conformance-dashboard pointer absent = KEEP-known, #171/ADR-86) — unchanged.
- **AR-D** (2 grandfathered FF commits = KEEP) — re-verified (still 2).
- Hygiene KEEP-healthy block (organ/validator inventory matches; 23/10; "Layer 2 never executes") — re-confirmed,
  with the **count moved 793 → 800** since that audit (legibility commit; now correct + gate-confirmed).
- PLAYBOOK fidelity §3 delegation credit — **independently re-verified as earned** (§3).

**Fidelity-NEW (this audit):**
- **GA-1** — Governing-ADRs roster lag (ADD-coverage).
- **NEW-1** — `conformance-hub.js` skeptic/digest unpinned (code-conformance side-note; ARCHITECTURE doctrine accurate).
- **Substantive lens-5 verdict** — the delegation target is *substantively* sound, not merely structurally
  delegated (the PLAYBOOK audit credited the pointer; this audit verified the destination).

---

## §6 — Confidence ledger (the integrity record)

- **MACHINE-VERIFIED by orchestrator (re-ran personally):** 23 checks; health OK; pytest=800; doc_claims 3/3;
  doc_code_edge 5/5; scan_undeclared_edges (AR-A); `3103340` diffstat; FF-commit count; conformance-hub.js
  model params (NEW-1); ADR-82/88/89 header-vs-index status; ARCHITECTURE "Proposed"-string absence; bare
  `HANDOFF_PROCESS.md` occurrence count (L564, single).
- **JUDGMENT (not machine-checkable):** GA-1 severity (curated-list lag is cosmetic-today); AR-B severity
  (style consistency); the "delegation is substantively sound" verdict (evidence-backed reasoning, not a gate).
- **Agent claims the orchestrator corrected:** C1 reclassified from "CONDENSE (live code violates the rule)"
  to "ARCHITECTURE doctrine accurate + NEW-1 code side-note" (the unpinned stages inherit Opus, matching
  intent). D1's "ADR-82 file-header stale" downgraded to **not-an-ARCHITECTURE-finding** (frozen-header
  convention, by design). AR-B line number corrected (L534 → L564).
- **Out of strict scope (surfaced, not actioned):** NEW-1 (a `conformance-hub.js` code change, not an
  ARCHITECTURE edit).

---

## §7 — Restructure recommendation (recommendation only, not executed)

**No restructure warranted.** The Ch1–Ch6 reader-entry framing + the `[CORE]` tagging place the harmony
core (Ch1) first and keep the validator-dense executable inventory (Ch2) adjacent — navigation is sound and
the chapter pointers in CLAUDE.md §3 resolve. The file sits at 604 L with no budget gate (unlike CLAUDE.md);
no condense pressure.

**Recommended follow-ups (each its own operator-gated arc, in leverage order):**
1. **AR-A / #172 — declare `reconciled_with: handoff-process@5.2` on ARCHITECTURE frontmatter.** Highest
   leverage: converts the harmony target's currency from human-protected to machine-protected. The doc is the
   prime declare-candidate already named by both prior audits.
2. **GA-1 — refresh the curated Governing-ADRs roster to include 85–89** (or add a one-line "85–89 in CLAUDE
   §11" pointer mirroring the existing L581 note). Low effort, closes the body-cites-but-roster-omits gap.
3. **AR-B — qualify L564 to `protocols/HANDOFF_PROCESS.md`** for path consistency. Trivial; fold into any
   ARCHITECTURE groom.
4. **NEW-1 (separate repo, not ARCHITECTURE) — pin `conformance-hub.js` skeptic/digest to `model:
   'claude-opus-4-8'`** to satisfy the doc's own "no unpinned fan-out" doctrine explicitly rather than by
   inheritance.

None of these are blocking; ARCHITECTURE is fit to serve as PLAYBOOK's delegation target today.

---

**Audit run:** 2026-06-23 · worktree `worktree-architecture-fidelity` @ main `a39e416` · diagnostic only,
no ARCHITECTURE edit · 4 section agents (zero-gap tile 1–604) + orchestrator re-verification.
