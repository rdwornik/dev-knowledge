# Codex adversarial review — the ADR-111 amendment and the ADR-115 draft

**Class:** codex · **Date:** 2026-08-26 · **Branch:** `docs/endgame-2026-08-26`
**Reviewed:** `docs/decisions/ADR-115-agents-md-portable-instruction-layer.md` (`Status: Proposed`)
and the ADR-111 amendment diff (`cd25cb4e`, `docs/decisions/ADR-111-finding-triage-pipeline.md`)
**Mode:** adversarial, refute-first · **Invoked by:** the 2026-08-26 endgame governance session, act 3

> **Model deviation, stated rather than silent.** The brief specified **`gpt-5.6-sol`**. The
> repo's review wrapper `~/.claude/bin/codex-review.ps1` hard-pins `gpt-5.6-terra` (the L0 pin,
> registry seam S19, with no `-Model` parameter), and `ecosystem/provider-registry.yaml` records
> `gpt-5.6-sol` under `roles: [provenance]` while `gpt-5.6-terra` holds `roles: [reviewer]`.
> This review was therefore run as a direct `codex exec -c model=gpt-5.6-sol`, **not** through the
> wrapper. **No pin, registry row or role was changed** — the invocation is a one-off, and the
> reviewer-lane pin still names terra. Recorded so a later reader does not read this artifact as
> evidence that the reviewer pin moved.

## Verdict

**"Do not ratify ADR-115 in its present form."** 4 Critical · 4 High · 2 Medium.
**Counted from this artifact, not from a tool tally line** — the wrapper's severity tally is a
known-unreliable heuristic and was not used.

## Session disposition — what this session did with the verdict

**Ratification is HELD, and the reason is the review's first Critical, independently re-measured
before being acted on** (this session refuses to act on a reviewer's claim it has not verified —
the same rule it applies to its own transferred facts):

- ADR-115 §2 claims the C01 decision criterion — *"≥2 admitted providers natively consume
  `AGENTS.md` and not `CLAUDE.md`"* — is **MET**, on a table whose two qualifying rows are
  **OpenAI Codex** and **Cursor**.
- **Cursor is not an admitted provider.** `ecosystem/provider-registry.yaml` has exactly six
  `providers:` entries — `anthropic`, `openai`, `xai`, `google`, `antigravity`, `deepseek`
  (verified live). Cursor appears **only as a comment block**, whose own closing words are
  *"This declares no provider and adds no key."* The registry records it BLOCKED-WITH-CAUSE
  (poisoned-name collision; PATH-shadowed), and this session's own landed
  `2026-08-26-technical-provider-surface-repair-summary.md` records it as **not installed by rule**.
- **Strike Cursor and the count is 1, not 2** — so the criterion is **NOT met**, and C01's own
  stated fallback for that branch is not "accept anyway" but **"Otherwise → retire R-1."**
- ADR-115 §2 also omits `antigravity`, which IS a registry provider, and was not measured.

**An ADR is immutable once accepted.** Ratifying on a premise this session has measured false
would freeze the error, and correcting it would then require a superseding ADR. The acceptance act
is therefore **not taken**, and the question is returned to the operator/architect as the one
decision this session declined to make for them. The three remaining Criticals (the amendment's
intake-only clause, the §1-versus-§5 characterisation of what ADR-53 forbade, and the acceptance
act's incomplete carrier set) are decision content and are likewise the architect's to resolve.

**What this session DID take from act 3:** close-packet debt **D-1**, which is independent of the
ratification question — the two `test_validate_adr_status` baselines moved because ADR-115's FILE
was added (`a2e49855`), not because of any status VALUE. Verified: ADR-115 parses as grammar
**G1** with raw `'Proposed'`, and G1 is a status-line SHAPE, so the re-measured baseline holds
across any later `Proposed → Accepted` flip. Live measurement: **88 ADRs**, grammar
`{G1: 41, G2: 34, G3: 12, G4: 1}` — pinned in this commit, clearing the 2 suite REDs.

---

## Review output, verbatim

Do not ratify ADR-115 in its present form. The decision criterion is not met against the repository’s own provider registry, and the acceptance act leaves several live contradictions.

## CRITICAL [ADR-115 §2](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:44) — Cursor is counted despite explicitly not being an admitted provider

**What:** The claimed count of two depends on Cursor, but [provider-registry.yaml](/C:/Users/1028120/Documents/Dev/.dev-knowledge/ecosystem/provider-registry.yaml:176) records Cursor only in comments as `BLOCKED-WITH-CAUSE` and explicitly says, “This declares no provider.” The six actual provider entries include Antigravity, which ADR-115 omits and does not measure.

**Why:** Applying the criterion strictly to the repository’s admitted providers yields only one demonstrated zero-configuration match—OpenAI Codex—not the required two.

**Fix direction:** Recompute the criterion against a resolved, authoritative admitted-provider roster before ratification.

## CRITICAL [ADR-111 amendment §“The ruling”](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-111-finding-triage-pipeline.md:145) — a non-intake packet cannot satisfy unchanged intake-only birth rules

**What:** The amendment declares a packet simultaneously to be the §3 ratifying decision, while original [§2–§3](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-111-finding-triage-pipeline.md:64) say the only path is `CANDIDATE → intake → ratification` and only a ratified intake births rows; the amendment then claims at [lines 187–195](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-111-finding-triage-pipeline.md:187) that §3 and §4’s “birth requires a ratified intake” rule remain unchanged.

**Why:** The packet explicitly has no intake, so “direct birth is lawful” and “birth still requires a ratified intake” cannot both be true. ADR-115 cites this amendment as its birth-path authority.

**Fix direction:** The amendment must explicitly amend the intake-only clauses or stop authorizing direct births.

## CRITICAL [ADR-115 §1 versus §5](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:24) — the ADR gives opposite descriptions of what ADR-53 forbade

**What:** §1 correctly says ADR-53 names the `AGENTS.md` filename and not a duplication condition; [§5 line 170](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:170) then asserts “what ADR-53 forbade was duplication.”

**Why:** This is the exact “substance reading” the ADR earlier refutes as absent from ADR-53.

**Fix direction:** Resolve which characterization the decision relies on before freezing it.

## CRITICAL [ADR-115 §4.3](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:139) — the acceptance act leaves live surfaces asserting the superseded rule

**What:** Executing the listed act leaves all of these live:

- [CLAUDE.md:12](/C:/Users/1028120/Documents/Dev/.dev-knowledge/CLAUDE.md:12): “Single canonical agent-instruction file.”
- [CLAUDE.md:207](/C:/Users/1028120/Documents/Dev/.dev-knowledge/CLAUDE.md:207): “AGENTS.md is retired.”
- [antipatterns-universal.md:4](/C:/Users/1028120/Documents/Dev/.dev-knowledge/templates/claude-regions/antipatterns-universal.md:4): the byte-coupled copy of the same prohibition.
- [tasks/577…md:13](/C:/Users/1028120/Documents/Dev/.dev-knowledge/tasks/577-adopt-agents-md-as-the-portable-instruction-layer.md:13) and [BACKLOG.md:218](/C:/Users/1028120/Documents/Dev/.dev-knowledge/BACKLOG.md:218): R-1 is binding and ADR-53 forbids duplication rather than the filename.
- [tasks/584…md:13](/C:/Users/1028120/Documents/Dev/.dev-knowledge/tasks/584-claude-md-10-in-lockstep-with-its-form-a-templat.md:13) and [BACKLOG.md:192](/C:/Users/1028120/Documents/Dev/.dev-knowledge/BACKLOG.md:192): R-1 made the prohibition false, contradicting §6’s ruling that R-1 never bound.

**Why:** The act fails intake #48’s requirement for exactly one live normative answer and immediately leaves the new precedence rule contradicted by executable work carriers.

**Fix direction:** Include all live normative and generated carriers in the acceptance closure, including the task sources and regenerated BACKLOG.

## HIGH [ADR-115 §5](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:170) — ADR-53 Decisions 1 and 4 are narrowed by more than the word “single”

**What:** ADR-53 D4 says `CLAUDE.md` is substantive and carries the full contract; ADR-115 moves the portable substance to `AGENTS.md` and leaves only a Claude-specific remainder in `CLAUDE.md`.

**Why:** Removing only “single” does not repair “substantive” or “carrying the full contract,” so the stated supersession scope is incomplete.

**Fix direction:** Name every displaced part of D1/D4 before changing ADR-53’s status.

## HIGH [ADR-115 §4.3 item 8](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:150) — the “file-by-file” nine-item set is not a nine-file closed set

**What:** Item 8 entails deleting the live intake, adding its archive destination, changing `docs/intake/README.md`, and regenerating `docs/intake/manifest.json`; item 9 is “generated fragments,” not a named file.

**Why:** The exact mutation footprint cannot be derived from the purported file list, and `docs/intake/manifest.json` is absent from it despite being the output of the required `gen_intake_tree.py --write`.

**Fix direction:** Enumerate every changed path explicitly.

## HIGH [ADR-115 §4.4](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:161) — the two named measurements are insufficient and one rationale is false

**What:** `precommit_hook_roster` reads `.pre-commit-config.yaml` plus `CLAUDE.md` §9, neither changed by item 4; `pytest_collected` measures test count, while item 4 only changes an existing test body. The act instead perturbs:

- `validate-hermetization` directly;
- `test_validate_hermetization_seals_exactly_the_registry_living_docs`;
- `check_adr_status_grammar` header/index coherence;
- `intake-index-freshness`;
- `intake_tree_coherence`;
- `claude-rosters-freshness`;
- the conformance-dashboard freshness input set in [generated_artifact_freshness.py:127](/C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/generated_artifact_freshness.py:127).

**Why:** The prescribed pre-flight can pass without exercising the behavior, status, intake-tree, or generated-surface changes the acceptance commit makes.

**Fix direction:** Replace the unrelated measurements with the targeted tests and affected gate checks.

## HIGH [ADR-115 §8 versus §9](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:202) — the claimed structural mitigation does not exist after acceptance

**What:** §8 says the importer and byte-cap test structurally keep the two-file model safe; [§9](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:208) admits the acceptance act creates neither the file/importer nor the byte-cap test.

**Why:** Immediately after ratification, the stated mitigation is future work, not a live structural property.

**Fix direction:** Describe it as an unimplemented dependency or include it in the acceptance act.

## MEDIUM [ADR-115 §4.3 item 6](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:148) — both PLAYBOOK line locators are stale

**What:** The cited `:318` and `:4163` anchors are currently at [PLAYBOOK.md:319](/C:/Users/1028120/Documents/Dev/.dev-knowledge/protocols/PLAYBOOK.md:319) and [PLAYBOOK.md:4360](/C:/Users/1028120/Documents/Dev/.dev-knowledge/protocols/PLAYBOOK.md:4360).

**Why:** The second locator misses by 197 lines; only the quoted anchor text makes it recoverable.

**Fix direction:** Remove the stale numeric claims or update them immediately before ratification.

## MEDIUM [ADR-115 §7](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-115-agents-md-portable-instruction-layer.md:192) — the known CONTRIBUTING contradiction is left standing

**What:** [CONTRIBUTING.md:237–243](/C:/Users/1028120/Documents/Dev/.dev-knowledge/CONTRIBUTING.md:237) still labels `Partially superseded` a legacy off-enum carve-out, while §7 declares that premise stale; CONTRIBUTING is absent from the acceptance act.

**Why:** Ratification would knowingly leave a living governance guide contradicting the status enum.

**Fix direction:** Include that living surface in the same closure act.

Sound checks:

- `SANCTIONED_TIER1_FILES`, `CANONICAL_MANDATORY`, and `test_validate_hermetization_seals_exactly_the_registry_living_docs` all resolve. The measured enum size 20 and proposed post-size 21 are correct.
- `precommit_hook_roster` and `pytest_collected` both exist, although §4.4 misstates their relevance.
- Intake #48, intake #25 W-9(a), packet row C01, register R-1, register section U, tasks #577/#584, ADR-94, ADR-98 §3, ADR-101 §1, ADR-108 §A, ADR-113 and ADR-114 all resolve.
- `Partially superseded — <reason>` is accepted by `STATUS_ENUM`, and the README index parser recognizes it. The §7 token itself is sound.
- The §6 precedence rule is coherent in isolation; the defect is that the acceptance act leaves live task carriers contradicting it.

I did not independently replay external vendor runtimes or the 46-minute DSH/npm probe. Those claims resolve to repository research/probe artifacts, but their underlying external observations were not reproduced here.