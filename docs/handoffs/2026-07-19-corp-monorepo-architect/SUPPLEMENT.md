# Architect strategic supplement — 2026-07-19-corp-monorepo-architect

Repo: corp-monorepo · Mode: architect · Date: 2026-07-19

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

========== SUPPLEMENT ANSWERS — corp-monorepo, outgoing architect, 2026-07-19/20 ==========
State at handoff: main 1dfee3e · single branch · zero worktrees · 2730 tests green · no
unmerged work anywhere. Companion artifact: SOURCE-MAP-corp-monorepo-successor.md (the
"which file answers which question" index — read it with this).

--- 1. STRATEGIC INTENT (way-of-working level) ---

The repo crossed from consolidating knowledge to building with it. Consolidation is DONE and
measured: 52 of 53 consumable July artifacts have witnessed downstream consumption; the one
outstanding (intake-16) is ratified and in build. So the next session's goal is NOT "consume
more" and NOT "audit more". It is to make the loop hold MECHANICALLY instead of by architect
vigilance. Three way-of-working goals, in priority order:

(a) COMPLETE ONE FULL EPIC CYCLE, DELIBERATELY. The developer/epic pipeline has never run
    end-to-end: G-A (intake→ADR→epic with stories+done-when) → G-B (architect-authored
    ex-ante done-contract, FILE-BOUNDARY, escalation, MODE) → build → G-C (RETURN → review →
    serial merge → closure on the HARD metric → teardown). #38 was a STORY return inside a
    lane, not a closed epic. E5 (#40 → #36 → #55) is the right vehicle: finish it as a real
    epic cycle with a return artifact and a teardown, so the pipeline is proven once before
    KE and RFP ride on it.

(b) GUARDS MUST BE PROVABLY GUARDING. This session found a PASSING safety test in front of a
    VIOLATED invariant (details in Q4/Q6). The methodology's load-bearing claim is
    "instructions are requests, MECHANISMS are guarantees" — a mechanism that cannot see what
    it claims to guard is worse than prose, because it manufactures confidence. The
    generalizable rule the next session should establish: every safety/invariant test
    declares WHAT it scans, and is itself verified against a known-violating negative
    fixture. Start with the one concrete instance (vault-writer), then decide whether the
    rule belongs hub-side.

(c) RE-WITNESS AT POINT OF USE. A document produced two days ago contradicted a merged,
    witnessed fix (F1/O2 — see Q4). The rule that caught it was applied ad hoc by the
    architect. Make it routine: any ruling that cites an F-number, an audit finding, or a
    count re-witnesses it live at the moment it drives work. Evidence has a shelf life; the
    census counts alone were corrected twice this arc (17→19 digests, 3→8 audits).

Standing product goal underneath all three (unchanged, operator-ruled): four focus modules to
DEPLOYED-AND-WITNESSED — metadata/Obsidian · URL/source registry · knowledge extractor · RFP
agent. Acceptance = a green WITNESSED sandbox end-to-end run per module. C1 is closed; C2, C3,
C4, C6 remain. Decks are the NEXT phase (C5 and the SIM-2 run deferred with it).

--- 2. TENSIONS WEIGHED ---

(a) Consolidate vs build. The operator was (rightly) tired of circling; building on unconsumed
    knowledge would have repeated work already paid for. LANDED: one evidence census, then
    build. WHY: the census proved the felt problem was execution, not consumption — and it
    cost hours, not days. Do not re-open; do not re-audit July.

(b) Archive hygiene vs reference integrity. The operator wants consumed artifacts out of the
    working folders; moving them strands citations inside immutable ADRs. LANDED: #68 policy —
    relocation requires FULLY CONSUMED **and** SUPERSEDED; citations move in the same commit;
    JOURNAL is never edited; a move that would strand a live citation is BLOCKED; LIVE specs
    archive at closure only (intake-16 at E5 closure, the SIM spec at deck-phase closure).
    2026-07-06-technical-architect-intake was DEFERRED, not moved, for exactly this reason.
    WHY: a tidy folder is worth less than a resolvable citation graph.

(c) Facts revival vs staying dead. Evidence overturned a premise mid-arc: key_facts is densely
    populated (392/488 notes), which made revival CHEAP — and cheap is seductive when a signed
    deletion (Arc-B B2) stands behind the current state. LANDED (ADR-37): the pipeline stays
    dead; add exactly ONE projection (facts_count from frontmatter) so the 29 consumer sites
    stop reporting a lie; a key_facts RETRIEVAL surface is parked behind a quantified trigger
    (witnessed post-F6 grounding failure in real RFP use). WHY: cheap ≠ needed; the chosen
    retrieval surface is body-FTS, and reversing a signed deletion on enthusiasm would gut the
    deletion doctrine.

(d) Canonical layer: frontmatter vs DB. LANDED: frontmatter canonical, index.db a derived,
    disposable projection, NO dual-write ever. WHY: witnessed reality — the DB is
    drop/recreate on rebuild and never projected the richest frontmatter fields.

(e) Two build channels. Worktree lane in-terminal vs epic outsourcing via a dev-knowledge
    developer bundle are BOTH legitimate; compounding them cost a session of confusion and
    contaminated a live hub session. LANDED: the channel is an OPERATOR pick, asked BEFORE any
    provisioning; corp currently runs primary + `claude --worktree`. The generated E5 bundle
    is quarantined hub-side — do not recreate it in corp.

(f) Path safety vs friction. After the docs/templates violation I hard-gated all new paths;
    that then STOPPED a fully convention-compliant ADR path and wasted a round-trip. LANDED
    (operator ruling, codified hub-side as ADR-101): compliance IS authorization — a path
    matching a codified, citable convention proceeds WITH its citation as the audit trail;
    unsanctioned paths and ALL new folders stay hard-gated. Also settled in the same family:
    docs/audits/ is markdown-only at the root — no subdirectories, no working corpora.

(g) Serial orders vs orchestrated fan-out. Serial single-thread CC orders are simpler but
    degrade badly on read-heavy multi-module work. LANDED: audit/review-scale work runs as
    Opus orchestrator + Sonnet bounded probes + Haiku read-only fan-out + an independent Codex
    derivation, in its own worktree, with ALL git mutations serial in the main thread. PROVEN
    this arc: a blind sol derivation from src/ alone added three real edges the CC probes
    missed, while the CC probes caught one thing sol was structurally blind to.

(h) Deterministic scoring vs learning. LANDED: equal weights day-1 with `weights_version` as
    the tuning seam; neighbour-prior is single-pass from intrinsic scores (the bounded form);
    bandit only at cycle 3+ behind the quantified trigger (≥3 cycles, ≥30 labelled, top-3
    precision <70% twice). Literal PageRank is permanently NOT-listed. Safety/consent gates
    numerically override any score — `exclude` means non-rankable and cannot be outvoted by
    arithmetic.

(i) BACKLOG shape. New themes (E8/E9/E10) vs stories under existing themes. LANDED: Option B —
    stories under E3/E4/E5/E7. WHY: theme SEQUENCE carries R10 priority, so appending new
    themes after E7 would have buried the operator's own focus modules at the bottom of the
    priority order. Execution order is lane-scheduled by the architect, never derived from
    theme position.

(j) Comprehensibility vs completeness. The cold-reader probe (4/4 ANSWERED) proves what is
    written is understandable from the repo alone — it does NOT prove the map is complete.
    Completeness rests on two blind derivations agreeing. Keep both instruments; do not let a
    green probe create false confidence.

--- 3. CONSIDERED + REJECTED (do not relitigate) ---

· Literal PageRank — permanently NOT-listed (A3). Neighbour-prior single-pass is the sanctioned
  bounded form.
· Reviving facts / facts_fts tables, loader, or FTS — rejected in ADR-37 even after evidence
  made it cheap.
· Dual-write between frontmatter and the DB — rejected (ADR-37).
· A speculative key_facts retrieval index before body-FTS proves insufficient — parked behind
  the quantified trigger, not built.
· Building a data/kb canonical-JSON producer for the RFP agent — REJECTED on evidence: the
  Word/Excel lane is already vault-wired via rfp/vault_adapter.py (subprocess `corp retrieve`);
  the canonical JSON is a VESTIGIAL FALLBACK to retire, not an orphan needing a producer. This
  overturns the process audit's F11 framing — build body-FTS instead.
· New BACKLOG themes E8/E9/E10 — rejected (see 2(i)).
· Relocating 2026-07-06-technical-architect-intake — DEFERRED (#69): would strand four
  immutable-ADR citations. Only a forwarding-marker arc makes it movable.
· Recreating the E5 developer bundle inside corp — rejected; it is quarantined hub-side and the
  active channel is primary + worktree.
· Blanket pre-commit blocking of every new path — rejected in favour of the two-tier rule.
· Rewriting ARCHITECTURE.md now — rejected: that is the A3 R9 "as-is docs rewritten once" arc.
  Only the item-by-item drift list and a proposed rewrite scope were produced.
· Deck / PowerPoint work this phase — operator ruling: next phase.
· Any service, mesh, or message-bus shape — A3 NOT-list at 3-RFPs/month scale. If a plan
  reaches for an infrastructure tier, reject it on sight.
· Editing signed manifests, ADRs, audits, or JOURNAL in place — supersede or use the sanctioned
  amendment marker; never in-place.
· Fixing test_cke_paths_resolve inside the E5 lane — rejected as out-of-boundary; it was fixed
  on main by the night batch instead.

--- 4. OPEN QUESTIONS ---

DESIGN (need a ruling):
· Does the classify→finalize inbox path have to trigger extraction? Today it does NOT, so files
  routed that way land with no knowledge note — silently. Product decision, operator-owned.
· Vault-writer invariant fix SHAPE: route copy_to_vault through write_note, extend the AST
  scanner to follow helper calls, or both (my ruling: both). The generalization — should every
  safety test carry a negative fixture and declare its scan scope? — is probably a hub-level
  methodology question, not a corp one.
· INDEX_EXTRA_ROOTS federation vs ADR-22 merge: federation is BUILT and TESTED (config.py:100,
  schema/pipeline_config.py:77); ADR-22 was ratified-but-never-built and is superseded by
  ADR-33; the ACTIVATION ratification is not witnessed anywhere. Needs a decision inside the
  RFP intake.
· ADR-27 canonical-output prose (02_sources/ vs the actual 01_Knowledge/ routing) — amendment
  marker now; the full doc rewrite belongs to R9.
· How does the E5 epic CLOSE, given the bundle is quarantined — a close-out audit doc (my
  ruling) or a regenerated return artifact? Process question for the hub.
· Who schedules the A3 R9 as-is-docs rewrite arc? Its trigger and authorship have been
  unscheduled since the ruling was written.

DELIBERATELY DEFERRED (do not treat as forgotten):
· ARCHITECTURE.md rewrite → R9. · #69 ADR archival (forwarding-marker arc on ADR-33/34/35/36) →
  operator: run now or hold. · key_facts retrieval → quantified trigger. · Paper-only ADR-34/35/36
  enforcement → stories #63–#65 (enforce OR record an explicit deferral naming the gap). ·
  Deck lane C5 + the SIM-2 run → deck phase. · #35 follow-ups: the ≥80% dry-run match check and
  the DR-6/7 zone renames (renames blocked on the operator's final zone names).

STATUS UNKNOWNS (not design — someone must simply look):
· The RFP terrain-recon lane was launched and its return was NEVER reported; no *terrain*/*rfp*
  branch exists in corp. Locate it or treat the recon as not-yet-produced before relying on it
  for the RFP intake.
· The night CR batch (N1-A..D) status since it was rescheduled.

OPERATOR-ONLY (only Rob can close):
· Which RFP-KB product families count as "gold" (evidence: the KB is real submitted BY answers,
  mixed quality, Planning-heavy 894/1329 — so it is neither a curated gold set nor a dump). ·
  Final zone names (DR-6/7). · 90_Archive: JOURNAL says 9 stale projects were moved, the zone is
  empty — where did they go? · SharePoint/Salesforce: is automation wanted, or is the manual
  interface deliberate? · Whether the sanctioned-pattern path guard gets built (may already be
  absorbed hub-side).

--- 5. DECOMPOSITION RATIONALE ---

SHAPE. Themes E1–E7 carry R10 priority in their SEQUENCE (knowledge loop E5/E6 before the RFP
rewrite E4), so new work enters as STORIES under existing themes and never as appended themes.
One build unit = one story cluster = one lane; lanes are file-disjoint by construction — E5 owns
src/corp/ops registry surfaces, KE owns extraction/index surfaces, RFP owns retrieve/rfp
surfaces, doc lanes own docs/. That disjointness is what makes two lanes safe in parallel, with
the operator as the single serial merge gate.

REGISTRY ORDER IS FIXED AND D8-CORRECTED — do not re-conflate: #35 is the ContentRegistry
ROUTING gate (DONE, closed C1); the FR-10 SOURCE registry is #38 (DONE — primitives only) →
#40 (seed the three golden sources, resolve, score) → #36 (scout pilot, day-1 deterministic
rank) → #55 (draft Content-Manifest, the deck-facing tail, DRAFT schema, small, NOT a deck-lane
beachhead).

REPAIR PRIORITY PRINCIPLE (use it to schedule lanes, it was derived from the connection map):
failures cluster as (a) BYPASSES of the main path, (b) DERIVED DATA nobody writes, (c)
CAPABILITY not yet wired. Close bypasses first — they cause silent wrongness that nobody
notices for months; missing capability is visible the moment you need it.

MUST NOT BE REDONE OR RE-DECIDED:
· The July knowledge census (52/53) — do not re-audit July.
· The module connection map — consolidate FROM it; but re-witness any individual cell before
  acting on it (see the F1/O2 trap in Q6).
· The process audit, the architecture ground-truth recon, the A3 R1–R10 ruling, the deletion
  doctrine and its amendments, the S13 manifest rulings — all settled records.
· intake-16 and its D1/D3/D4/D5 picks — ratified.
· ADR-37 and ADR-38 — accepted; changing either requires a SUPERSEDING ADR with new evidence,
  not a re-argument.
· The Option B backlog structure.
· The #38 build rulings: a single `weights_version` field (no separate score_version),
  round-half-UP (not banker's), `exclude` → gated with score forced to zero.

--- 6. OFF-REPO CONTEXT ---

OPERATOR WORKING CONTRACT (hold this or lose him — every item below was learned the hard way):
· Plain human terms first, acronyms explained; insight-first with the "so what"; scannable;
  zero corporate filler; shortest complete answer.
· Bounded A/B picks for decisions, never questionnaires. He is a peer, not a menu.
· Progress reports must be product-owner concrete — use case by use case, evidence, and an
  explicit what's-missing list. Abstract shorthand gets rejected.
· NEVER create, move, or delete a path without his word. Two violations this window (a template
  file in a new docs/ folder; an acceptance spec dropped at docs/ root on an inherited path).
  Every path an order emits is either convention-cited or delegated as
  "derive-quote-propose-STOP". He signs every deletion (ADR-38 manifest).
· ANY side-effect-producing task while the primary is busy goes to a WORKTREE, always — the
  cost is not merge conflict, it is the primary losing trust in its own state. Propose the
  worktree unprompted; state its NAME in chat, paired 1:1 with the prompt filename.
· The build CHANNEL (primary vs worktree vs epic-outsourcing) is HIS pick, asked BEFORE
  provisioning. Never compound two mechanisms.
· He is the serial merge gate; lanes commit-and-STOP and never self-merge.
· Paste blocks must be SELF-CONTAINED. The night batch ran degraded because a full spec never
  reached the executing session; the #38 plan review stalled for the same reason. Assume the
  receiving session has NO chat context.
· Multi-agent utilization is mandatory for audit/review-scale work; under-use is a routing
  failure, and he will say so.
· Prose→mechanism: a recurring instruction written as prompt text is a routing failure. Guards,
  checks and verification belong in scripts/hooks/skills.
· Night missions are PRE-AUTHORIZED — never insert an approval gate between the paste and the
  start; safety lives in the stop conditions. Record the matrix in the log instead.
· Codex: terra reviews EVERY code merge (it earned it — six P1 findings on #38 across five
  passes); sol for independent/adversarial derivations and cold reads; luna for cheap read-only
  fan-out; smoke before relying (quota has been volatile). Every plan names its Codex lane or
  gives a one-line reason for its absence.
· No LLM budget ceiling. Sky-is-the-limit first, optimise later if he asks.
· He signs off on the SUPPLEMENT: the architect authors these answers in chat; CC only
  transcribes them verbatim.

OPERATOR PHILOSOPHY (recorded, and it decides design defaults): manual first, automate later.
Deploy the system first, improve it iteratively. Deterministic before learned. A safety gate is
never outvoted by a computed score.

FINDINGS THAT ARE NOT (YET) IN ANY FILE — these travel only here:
1. STALE EVIDENCE TRAP. The night decision-plan doc's §5.3.9 and option O2 still describe the
   ingest cold-start crash (F1) as OPEN. It is FIXED — #35, merge 6c36f61, witnessed by the
   SIM-1 diagnostic (fresh env self-seeds the registry, 95% match, real assets untouched). Do
   not spend a lane on it; re-witness before believing any F-number.
2. P1 REPAIR, RULED BUT NOT BUILT. copy_to_vault — live in the extract_project workflow — writes
   into the protected 02_sources/ zone via shutil.copy2, bypassing write_note (no frontmatter,
   no quality gate, no conflict protection), while tests/safety/test_vault_writer_invariant.py
   PASSES because its AST scanner reads only actions/*.py textually and cannot see the mutation
   inside the called helper in vault_io.py. Fix the mechanism now; only the ADR-27 prose
   correction defers to R9.
3. NEW SILENT GAP. The secondary inbox path classify→finalize never calls extraction; files
   routed that way land with no knowledge note and no error.
4. A RULING TO DROP. The "E4=WARN routed to primary" entry could not be witnessed anywhere in
   src/, config/, or intake-16 — it was a chat-level test disposition, and the night batch
   actually FIXED that test (repo-toplevel identity instead of checkout basename). Moot.
5. THE CHEAPEST HIGH-VALUE ITEM ON THE BOARD. `com` (deal loop) is config-stalled, not
   abandoned: four unset env vars plus one template-filename correction, ZERO code, confirmed by
   two independent witnesses; corp/config.py already defaults the same env names to the real
   MyWork paths. Reviving it also activates the dormant com→index edge.

CROSS-REPO: corp is A0-closed — methodology comes FROM the hub, corp never invents it. The
two-tier new-path rule is codified hub-side (ADR-101, "compliance IS authorization"), in force.
The E5 developer bundle is QUARANTINED on a hub branch, not destroyed. Methodology questions
route to the hub, not to this chat's successor.

TRUST POSTURE — the single most important line in this supplement: inherit NO verdict from any
prior chat, audit, or summary without a live probe. This arc overturned census counts twice,
a bundle premise (Graph consent), an audit's F-list entry, and two senior verdicts. The repo is
the truth; documents are its shadow, and shadows go stale.
========== END SUPPLEMENT ANSWERS ==========
