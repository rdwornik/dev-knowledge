# ADR-100: Audit retention — keep-all-accepted + count-tiered index (folds and closes #212)

- **Status:** Accepted
- **Date:** 2026-07-07
- **Decision tier:** Architecture (Path A — direct operator ruling, 2026-07-07 architect ratification session)
- **Related:** ADR-49 / ADR-65 (condense-past-recording-to-git — the sibling retention doctrine, applied here to a different tree), ADR-82 (immutable handoff bundles — #212's subject, folded in), ADR-36 (audit-tool architecture — cites the `docs/audits/` directory structurally), ADR-60 (docs/ folder taxonomy — `audits/` = outputs role, cites the directory structurally), ADR-98 (intake pipeline — the genre-demarcation counterpart: audit vs intake), #212 (folded + closed by this ADR), #269 (the Q2 index-currency freshness-hook follow-up)
- **Decommission:** none
- **Source:** 2026-07-07 architect ratification session (operator ruling R3); consumes the draft `docs/audits/2026-07-07-DRAFT-audit-retention-index-rule-proposal.md` on branch `drafts/2026-07-07-proposals` @ `3da29ea` **by ratification, not by merge** (tag `archive/drafts-2026-07-07`). Folds and closes BACKLOG #212 (the `docs/handoffs/**` retention question — same immutable-dated-artifact-tree class).

## Context

Two of the corpus's immutable dated-artifact trees grow monotonically and unbounded by design: `docs/audits/**` and `docs/handoffs/**`. The hub already condenses two *other* accretion vectors — doc section-history (ADR-49/65 → git pointer) and BACKLOG inline-history (`doc_rot`) — but these two trees had no deliberate retention call. Block-3.3 shipped a navigation index (`docs/audits/README.md`) but deliberately deferred the *policy*; #212 asks the same question for handoffs. Both were left to this decision.

### Evidence base (the 2026-07-07 architect session's measured basis)

- **196 audit files**, flat tree, **no `archive/` dir exists.**
- **125 citation lines across 42 citing docs.**
- **~78% of citation lines sit in immutable ADRs / append-only LESSONS / immutable transcripts** — they can **never be re-pointed**. A physical file move would **permanently break** them.
- **ADR-36 and ADR-60 additionally cite the `docs/audits/` directory structurally** (the audit-tool architecture and the docs-taxonomy role).

**Known gap in the blast-radius estimate (recorded, not hidden):** the citation scan covered the **doc corpus only** — **audit→audit cross-references and `ecosystem/*.yaml` were NOT scanned.** The 125/42 figures are a floor, not a ceiling.

## Decision

### 1. Keep-all-accepted (no physical move, no roll-up, no compaction)

Every accepted audit is **kept, unbounded**; audit files are **never physically moved, rolled up, or compacted.** Audits are the **evidence spine** — ADRs, LESSONS, transcripts, and the tooling cite them by path, and ~78% of those citations are in immutable/append-only files that can never be re-pointed. The storage cost is trivial; the referential cost of a move is permanent breakage. Keep-all is the deliberate, recorded call — not silent drift.

### 2. Count-tiered index (navigability without moving files)

Navigability is provided by the **index** (`docs/audits/README.md`), **count-tiered, not age-tiered:**

- The **fresh section** of the index holds the **~20 most recent** audits.
- **Everything older moves to an archive *section of the index*** — **a section of the index, not the filesystem.** **Files never move; only their index grouping does.**
- **Count-based, not age-based** — the operator takes breaks, so **dates mislead** (a quiet month is not a stale month); a fixed recent-count is the honest freshness signal.

### 3. Any future physical move is gated

Should a physical move of audit files ever be contemplated, it requires **both** a **referential-currency scan** (closing the known gap above — audit→audit + `ecosystem/*.yaml`) **and an explicit architect ruling.** Keep-all is the default precisely because the move is expensive and under-scanned.

### 4. Genre demarcation — audit vs intake

**Audit = evidence *about* state. Intake (ADR-98) = a request to *change* state.** They are **separate genres with separate lifecycles.** Keep-all is safe for audits **precisely because they are the evidence spine** — the same policy would be wrong for a different genre. (The intake genre pays rent and is reviewed for removal, ADR-98 §6; audits are never removed. The two are governed oppositely on purpose.)

### 5. #212 (handoffs) resolves the same way — keep-all-accepted

`docs/handoffs/**` is the **same immutable-dated-artifact-tree class** (immutable per ADR-82, unbounded, cited). #212's policy question — "a compaction/rollup mechanism + window, **or** an explicit 'keep all; unbounded accepted' with a recorded reason" — is answered **keep-all; unbounded accepted**, for the same reason: handoff bundles are cited and immutable, so a physical move / roll-up breaks references it cannot re-point. This **closes #212**; any handoff-index navigation mechanism is implementation, not a re-opened policy question.

### 6. Q2 (index-currency gate) — advisory now, hook is a follow-up

The count-tiered index has **no freshness gate yet** — index currency is **advisory now**. A freshness hook (mirroring `roster-freshness` / `claude-rosters-freshness`) **lands once the index shape settles** (draft rec 2a). **Not built here** — filed as **#269.**

## Consequences

- **Easier:** the corpus's two largest growth vectors get a deliberate, recorded retention call; the evidence spine stays grep-able and every existing citation keeps resolving (nothing moves); the index makes an unbounded tree navigable.
- **Cost / mechanism (deferred to #269):** applying the count-tiered shape to `docs/audits/README.md` is a **build** action on its generator (`gen_audit_index.py`) — the index is generated ("do not hand-edit"), and its header still names #212 as the open policy; both update when #269 lands. Recording the rule now, building the index shape + freshness hook later, follows ADR-70's capture-precedes-construction pattern. **This arc moves no audit file and hand-edits no generated index.**
- **What this does NOT decide:** the freshness-hook design/timing (advisory until the shape settles, #269); whether the handoff tree gets its own index (implementation, not policy).

## Alternatives considered

- **Roll-up by year / compact older audits into a per-year digest** (draft option 1b). Rejected: any roll-up that moves or de-indexes files risks breaking the ~78% of citations in immutable/append-only docs that can never be re-pointed — the evidence-integrity cost outweighs a trivial storage saving.
- **Age-tier the index** (draft option 1c, the draft's recommendation). Not adopted: age misleads because the operator takes breaks — a quiet period is not staleness. **Count-tiering** (~20 most recent) is the honest, break-tolerant signal.
- **Physically move older audits to an `archive/` dir.** Rejected here and gated for the future (§3): no `archive/` dir exists, the move is under-scanned (the known gap), and ADR-36/ADR-60 cite the directory structurally — a move needs a full referential-currency scan **plus** an explicit architect ruling.
- **Decide handoffs (#212) separately / divergently toward roll-up.** Not adopted: handoffs are the same immutable-dated-artifact class; folding #212 into one keep-all doctrine is coherent and closes the question in one decision.
