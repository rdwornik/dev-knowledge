# Architect strategic supplement — 2026-07-20-dev-knowledge-architect-arc5

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-19

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# SUPPLEMENT ANSWERS — authored by the outgoing browser architect (2026-07-19); CC transcribes VERBATIM

STRATEGIC INTENT — operator-dictated, one line: **AUDITS ARE OVER. ARC 5 IS EXECUTION.** The night audit (14 artifacts, sol-validated on all 8 domains, terra-corrected ×7) reduced the whole system to one meta-finding: **"decision recorded ≠ decision enforced ≠ decision legible."** ARC 5 closes that gap by BUILDING — no new audits, no new studies; every wave below lands mechanisms and visible file changes. Growth-side is proven sound (E1 fire-tests); all work is lifecycle-side. The operator's bar, verbatim in spirit: "I keep repeating the same pains for 10-20 chats — stop theorizing, execute."

OPERATOR PAIN → BUILD MAP (his named pains, each with its concrete build; this ordering IS the wave order):

**W1 — VISIBLE BOUNDARY (the "colors" — the operator's most-repeated ask).**
Build #329/#352: versioned `.vscode` background decoration (grey/navy, dark theme) of `owner=hub` / `owner=repo` regions, deployed fleet-wide as carrier material; PLUS a sweep completing RULING-S reader-visible universal-vs-repo section headers in every governed file across all three repos (CLAUDE.md + configs). Done-when: the operator opens any governed file in any repo and SEES which lines are methodology and which are repo-personal. P4a .vscode ruling shelf-life 2026-08-13 — this wave must land before it.

**W2 — STRUCTURE EQUALIZATION LEG 2 (the assets/ folder, mypy, "why do folders differ").**
Named forever-pain: `ai-council/assets/ruff-pre-commit.yaml` sits in an undeclared root `assets/` folder. Ruling R1 below disposes it. Plus: mypy/cache-handling posture per repo (declare or equalize — R1b), `hub-toc-hooks` resolution (S5 §4.2 — recommend path (b): hub manifest re-scope v1.3.2 matching the hub's own retirement, then prune ai-council + retire corp's waiver), #331 ratification + `parity-surfaces.yaml` consumer-tier rows for the BACKLOG story-map schema + gate (both consumers already adopted de facto — S5 gap 1), reconcile the corp-vs-ai `validate_backlog.py` fork (S5 gap 2: ai adopts corp's full plugin form via RULING-W leg, or a time-boxed declared divergence), corp `deployed-versions.yaml` currency (evidence for #276). All consumer writes via RULING-W worktree/branch → report; all changes land as manifest/template carrier material (replication-first).

**W3 — LIFECYCLE MECHANISMS (intake→ADR→backlog→close→DELETE — "the process problem").**
Seed 2 (sol-upgraded): `validate_intake.py` HARD pre-commit gate — closed status enum (+ ratified tech-extension per R4), unique `intake-id` (fixes the live id:14 triple collision), required `consumed-by` on CONSUMED, machine-readable `Intake:` provenance field on ADRs + citation enforcement (ADR-102/103 backfill or recorded non-intake-origin). Seed 3: build #242 (ADR header↔README status reconciliation; ADR-88/89 frozen-Proposed case). Seed 4: `gen_grooming_worksheet.py` + `audit.py` grooming-cadence/net-delta WARN (witnessed accretion 74→116 in 11 days, ~3.8/day — this makes it a standing signal); extend `safe_remove.py` M2/M3 as #347's sanctioned REAL-DELETION mechanism (R3). #269 build (count-tiered audit index per ADR-100).

**W4 — ARCHIVE LEGIBILITY (the operator's archiving ask — see R2, honest tension).**
The operator wants: when something is archived, its genre (intake/decision/audit) must be knowable from the name. Facts: file NAMES already encode genre+date by convention (ADR-NN-slug, date-class-slug audits, date-genre-slug intakes); the ruled convention is stay-in-place (join keys, ADR-101 seal) with status on index surfaces. R2 decides the shape; whichever way it goes, the build is this wave: either the index/status surfaces (seeds 2/3 + #269 + handoff-README micro-era clause) OR a physical `archive/` with a genre-preserving naming rule via ADR amendment. NOT both by default; no silent relitigating.

**W5 — SESSION/WRITE GUARDS (worktree pain, #353/#344/#349).**
sol's strongest contribution (R5): ONE unifying organ — a HEAD-bound operator-authorization token (names worktree + branch + allowed paths) checked by a PreToolUse guard — satisfies #344 Ask-2 (consumer hub-write guard), #353 (boot contract: refuse mid-session external orders without clean-tree-or-named-worktree), and the S7 prompt-attestation at once. Plus S6's boot-snapshot SessionStart hook, the `.claude/.session-lock` HEAD-movement advisory, #349 close-discipline boot echo, and sol's signed integration-return token for self-merge detection. Five recovered-not-prevented incidents justify this wave.

**W6 — CANON INOCULATION + PROMPT EQUILIBRIUM (PLAYBOOK/handoff currency, "ekwilibrium").**
Seed 1 (cheapest, highest leverage — may run FIRST in parallel as a doc lane): transcribe the four un-inoculated rulings (RULING-W · two-tier · worktree side-effect rule · consumer merge-delegation composite) into PLAYBOOK (operational) + ESSENTIALS (one-liner), grep-verified against the ADR amendments; build the staged-diff CO-CHANGE checker (NOT a `coherence-nudge` extension — terra) with explicit ADR-36/41/101→PLAYBOOK/ESSENTIALS edges. Seed 7: the 7-item inbound prompt-spec as a PLAYBOOK §2 amendment + handoff-time self-check probe (R6 decides hard-probe vs soft). Handoff-README micro-era documentation (stage1/stage2 archive class).

**W7 — TESTING + FLEET STATE (last, per dependency).**
Seed 9: dynamic-test evidence gate (code-impact tier in ship.md or versioned `test-harness.yaml`), WARN-first then FAIL after two demonstrated runs, depends-on #270; `protocols/AGENTIC_TESTING.md` as #348 config material. Seed 8 (sol-sharpened): a scheduled `fleet_collect` PULL collector with watermarks ("silence ≠ absence") subsuming the two reporters; SQL/SIEM stays SHELVED until a witnessed join-pain (matches the intake #14 ruling — confirm as standing answer, R7).

NEEDS-RULING (operator's bounded picks — recommendations attached; answerable one word each):
- **R1** `assets/` disposition: (a) DISSOLVE — relocate `ruff-pre-commit.yaml` content to the canonical config location, delete the folder (RULING-W leg + safe-deletion path), or (b) UNIVERSALIZE `assets/` as a fleet deployment convention. **Recommend (a)** — one file, no fleet role, and (b) would mint a new mandatory folder fleet-wide for no carrier need. R1b: mypy posture — declare ai-council's mypy as sanctioned divergence (recommend) vs roll out fleet-wide.
- **R2** archive shape: (a) INDEX-ARCHIVE — status/count-tiered index surfaces, files stay, names already carry genre (recommend — zero join-key breakage, builds already seeded), or (b) PHYSICAL `archive/` folders with genre-preserving rename rule via ADR-98/100/101 amendments. **Recommend (a).**
- **R3** #347 safe-deletion = `safe_remove.py` M2/M3 extension as THE sanctioned mechanism. **Recommend YES.**
- **R4** intake enum: ratify the 6 off-canon statuses as a documented tech-genre extension vs reclassify the docs. **Recommend ratify-with-documentation** (they are functioning plan-of-record artifacts).
- **R5** unifying HEAD-bound authorization token as ONE organ for #344/#353/attestation vs three separate builds. **Recommend ONE organ.**
- **R6** prompt-spec: hard handoff probe vs soft self-check. **Recommend hard probe on the bundle side** (the off-repo prompt itself can't be gated — attestation covers the paste).
- **R7** fleet-state: confirm "collector + reporters now, SQLite shelved" as standing. **Recommend confirm.**
- **R8** (carried, corp-side) #38 channel pick: 1 primary-direct / 2 worktree / 3 epic-dev.

BINDING (travel verbatim; do NOT relitigate): the ARC-4 rulings (RULING-W/S/PY/CF, two-tier "compliance IS authorization" in force now), the terra ×7 corrections as applied, sol's 4 mechanism upgrades as accepted strengthenings, satellite wave FROZEN until Wave-1 lessons extracted, luna's floor-misreport corrected (consumers DO carry the floor, hash-matched — Haiku fan-out is indicative, not authoritative), E1 scope honesty (only two organs fire-proved this run).

CONSIDERED + REJECTED: SQL/SIEM now (premature per intake #14 + S8); `coherence-nudge` extension for co-change (terra: not implementable); blanket new-path blocking (two-tier rule supersedes); physical file moves for archival as default (R2 decides, convention says stay-in-place); more audits (operator: enough).

DO-NOT-REDO: the nine seeds' adjudication (terra-corrected kill-candidates stand); the 8-domain gap derivation (sol-triangulated); the ARC-4 equalization values (py311/120/>=0.15.5/minversion 9.0 — at-parity, verified); the grooming closes #306/#307/#328.

OFF-REPO CONTEXT: the 14 audit artifacts live on branch `audit/2026-07-19-cycle-close` (worktree `night-audit-cycle-close`, base 6077c428) — MERGE IS THE FIRST MECHANICAL ACT of the next session (serial, --no-ff, operator GO) so the seeds become citable from main. The e5-registry bundle sits quarantined on `docs/corp-e5-registry-developer-handoff` (3b6b3f18) pending R8. Corp freshness debt cleared by corp's own session (verified genuine re-read). Operator frustration is itself context: visible results per wave (W1 first is deliberate — colors are the most visible), one wave = one merged arc, educate artifact per wave with file-level before→after.

DECOMPOSITION RATIONALE: waves are ordered by operator pain-priority, not dependency elegance; W6 seed-1 doc lane may run parallel from day one (file-disjoint from W1/W2). Every wave: frozen acceptance contract before delegation, Codex terra pre-merge, RULING-W for any consumer write, replication material over one-off fixes, educate with before→after. The successor's first three moves: (1) merge the audit branch, (2) collect R1–R8 rulings (single bounded-pick message to the operator), (3) open W1.
