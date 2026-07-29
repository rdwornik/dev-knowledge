# Intake #18 ratification record — verdicts applied 2026-07-30 ([#435])

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-30 · **Slug:** intake18-ratification-record
- **Serves:** the durable per-amendment verdict ledger of the intake #18 ratification session
  (architect + operator, 2026-07-30) and the application arc that landed it (branch
  `docs/intake18-ratification`, cut from `376ee882`).
- **Inputs:** intake `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md` (the pack) ·
  dossier `docs/audits/2026-07-29-technical-intake18-ratification-dossier.md` (decision surface) ·
  audit `docs/audits/2026-07-27-verification-handoff-process-audit.md` (BW-*/RM-* evidence).
- **Authority:** verdicts are the operator's/architect's, immutable to the applying arc; this
  record transcribes them and cites where each landed. This file is an immutable record
  (CLAUDE.md §5 rule 3) — supersede, never edit.

## Per-amendment verdict ledger

| A | Verdict | Landed at / deferred to |
|---|---|---|
| A1 | ADOPT in full | `scripts/assemble_paste.py` END-of-paste sentinel (n sections · bytes) + `protocols/HANDOFF_BOOT.md` ack "({n} sections received.)" + boot Verification-split truncation rule + PLAYBOOK Ch4 report-direction sibling; tests 15–16 |
| A2 | ADOPT | HANDOFF_PROCESS §13 transport-medium paragraph verbatim (terra H1 carve-out: supplement Q/A relay stays chat) + ESSENTIALS report-direction one-liner (disciplines 5→6) + assembler over-budget warn extension |
| A3 | ADOPT, enum AMENDED | CLAUDE.md §4 region + `templates/claude-regions/conventions-commit-branch.md` lockstep (byte-match): THREE machine-produced lane prefixes — `worktree-` · `epic/` · `claude/` — plus the class-rule sentence "a new machine-produced lane prefix enters this enum only via a recorded ruling (never silently); the enum stays the checkable surface" (v2.47). **`~/.claude/rules/core-invariants.md` #5 sibling edit = OPEN operator ruling** (global infra, core-invariant #6; trigger: operator's explicit go) |
| A4 | items 1–2 ADOPT; item 3 DEFER | PLAYBOOK §2 "Multi-agent / fan-out prompt checklist" (s7 §4 draft adopted verbatim; mutual citations with the Ch8 [#441] launch test) + HANDOFF_PROCESS §13 destination contract. Item 3 (boot-header `Destination` row + P3 comparison leg) rides the §B(b) build |
| A5 | ADOPT (=U3) | PLAYBOOK Ch8 letter-allocation convention: assigned at integration, lanes never allocate; scoped dispatch-contract exception inside a sanctioned worktree pair; [#441] condition-2 example re-cited in the same edit unit; the Ch8 *Open reconciliation* paragraph deleted (the arc's sole paragraph deletion). `normalize-dated-headers` hook leg DEFERRED (S, later — as the intake stages it) |
| A6 | ADOPT | SUPPLEMENT.md.tmpl question 7 (ratified-in-chat register) + §13 schema line 6→7 with the capture-only scope note. Nothing else (the `.claude/commands/handoff.md:117` "6-question" mention is a named residual, outside the ruled write set) |
| A7 | §13(c) line ADOPT now; P0 legs DEFER | §13(c) opening sequence → role → vision → standing topics → backlog. P0a/P0b/P0c probe legs land inside the §B(b) one-evidence-block emission, not as ferry turns |
| A8 | ADOPT | Assembler PROMOTION-DEBT advisory block (grep `BINDING / do not relitigate / MUST NOT / ruling` over folded ANSWERS; never blocks) + §10 search-soundness sentence; tests 17–18. Interim by design — deletable when [#433] lands |
| A9 | ADOPT | §13 PLAN.md D3 four-state paragraph verbatim (DRAFT → REVIEWED → APPROVED → CLOSED(outcomes)); build stays [#301] (peg #298); `docs/handoffs/README.md` untouched (owner's next freshness window) |
| A10 | ADOPT all four + audit row 13 | RM-1 §15 newest-first fix · RM-3 §4 honest boot core (**byte-budget number + assembler warn DEFERRED to the §B(b) build** — architect confirmation 3) · RM-4 §5 condition 4 Bounded-deterministic (intro: "when all four hold (the fourth — bounded-deterministic — ratified at intake #18)") · §14a items 4/6 RULING-W + ADR-101 cross-refs · row-13 §14b clarifier "applied per the queue's shape (`tasks/` edit + regen on a flipped host)" — one edit unit, never a separate hotfix |
| A11 | DEFER to the §B(b) build | Carries pack-finding 1's re-scope: RM-7's premise stale (`_select_active_bundle` landed 2026-07-23, add-date selection + ambiguous-FAIL); the gate-coverage guard re-scopes to "every candidate bundle in the staged diff". Rides with: RM-8 overwrite refusal · `verify_handoff_probes.main()` params · [#421] second-tokenizer absorption. [#422] leg REJECT-as-already-owned (the row's Done-when carries it) |

## Direction, label, riders

- **U1 — intake #19 §B(b) direction: ADOPTED** (operator, 2026-07-30). One CC-side command → one
  evidence block → one operator paste. The BUILD (P0 legs, A4 item 3, A11 legs, `main()` params,
  generator changes) is a follow-up arc — task row [#446] filed by this arc; nothing of §B(b) was
  built here.
- **U5 — label: v6 CUT.** The §B(b) direction is a workflow reshape → v6 per the accepted
  derivation rule. **The version bump rides the §B(b) build landing** (the §13-at-5.7 precedent:
  "bump rides intake #18"). This arc landed ratified content at spec `Version: 5.7` unchanged;
  `reconciled_with` stamps did NOT move to 6.0. **Bump-carrier: the [#446] §B(b) build arc.**
- **U6 — riders, both DEFERRED with triggers (record-file only, no task rows — confirmation 5):**
  (a) intake #19 §B standing night-batch section + ADR-105 activation record — trigger: the next
  night-batch request; (b) standing closure delegation (ADR-70 amendment) — trigger: the next
  `/review-closures` batch, operator's call.

## Silent-rule ratchet — operator-ruled baseline raise (mid-arc ruling, 2026-07-30)

The [#436] ratchet (FAIL-class) correctly detected the ruled-verbatim texts growing the
normative-token pool; draining was unavailable without violating the verbatim adoptions. The
operator ruled the designed escape: **baseline 428 → 441** (the final measured count at arc end,
detector `silent-rule-v4`), committed with this record per condition (a). SKIP stayed surgical
(condition b): only the `audit-health` hook id was skipped on affected commits, and
`audit.py health` was re-run after each such commit verifying `silent_rule_ratchet` was the
ONLY failing finding. **Token-delta accounting (condition c) — pre-arc live 427, final 441,
+14 occurrences, all attributable to ruled edits, nothing else:**

- +1 U3/A5 statement — "lanes **never** allocate" (PLAYBOOK Ch8)
- +5 A4 item 1 checklist (ruled verbatim, s7 §4) — items 2 "tree **must** be clean", 3 "**MUST**
  cite" + "**never** an unmediated write", 6 "**must** write to", 7 "**never** silently absorbed"
- +2 A10 — RM-3 "**never** transmits" (staged text) + §14a item 4 "**never** a direct push"
- +1 A2 §13 — "**never** as chat-paste" (staged text)
- +1 A9 §13 — "**never** pasted" (staged text)
- +1 A6 §13 — "(**never** trusted over the repo)" (staged scope note)
- +3 A3 template extract (`templates/claude-regions/`, in detector scope) — "**never**
  self-merged", "**never** author-invented", "(**never** silently)"

Condition (d): until the operator's merge lands this baseline on `main`, the branch-side
`silent_rule_ratchet` finding reads raise-rejected vs `origin/main` (428) — **expected and
self-healing at merge** (previous == value on `main` afterwards), reported, not dispositioned.

## Residuals (named, not silent)

- `.claude/commands/handoff.md:117` still says "fixed 6-question" — outside A6's ruled write set
  ("nothing else"); candidate for the [#446] arc or the command's next touch.
- `protocols/HANDOFF_PROCESS.md` §Section history v5.1 entry says "6-question interview" —
  historical record, correct by construction, untouched.
- The three `warn-undeclared-intake18-*` disposition-register rows: handled per the ruled
  amendment (removed only if `[stale]` at this arc's gates; else left live) — outcome recorded in
  the arc's final report.
- Intake #18 frontmatter flipped DRAFT → ACCEPTED (`decided-by`: this session; `disposition:
  active` — consumer: the [#446] §B(b) build). Intake #19 stays SEED (only its §B(b) *direction*
  was ruled; this record carries it).

---

## Amendments (2026-07-30)

> **In-file amendment marker** per CLAUDE.md §5 rule 3 ("supersede with a new file **or an in-file
> amendment marker**"). The decision content above is **byte-untouched** — nothing in the verdict
> ledger or the riders section was edited. This section records two later operator acts against
> items this record left OPEN, so the register stays in its one convention home.

**1. A3 sibling ruling — OPEN → EXECUTED.** The A3 row recorded the
`~/.claude/rules/core-invariants.md` #5 sibling edit as an OPEN operator ruling (global infra,
core-invariant #6; trigger: the operator's explicit go). **The go was given 2026-07-30** and the
edit is executed. One line, no other global-infra change:

- **old:** ``EVERY change — including one-line doc edits — goes branch → merge `--no-ff`; never commit direct to `main`. Branches off `main`: `feat/ fix/ docs/ chore/`.``
- **new:** the same sentence, with `feat/ fix/ docs/ chore/` qualified as author-chosen ("these four only") and the **three machine-produced lane prefixes** added — `worktree-<name>`, `epic/<slug>`, `claude/<slug>` — plus the ratified class rule: lane branches are never self-merged and never author-invented, and a new machine-produced lane prefix enters the enum only via a recorded ruling (never silently), the enum staying the checkable surface.

This mirrors the ratified A3 text already carried by the hub `CLAUDE.md` §4
`conventions-commit-branch` region and its byte-matched
`templates/claude-regions/conventions-commit-branch.md` extract (v2.47). The global file is
off-repo and untracked, so its evidence is this record plus the arc's JOURNAL entry; the repo-side
surfaces are unchanged by it.

**2. U6(b) standing closure delegation — NOT ADOPTED.** The riders section recorded U6(b)
(standing closure delegation, an ADR-70 amendment) as DEFERRED with trigger "the next
`/review-closures` batch, operator's call". **That batch arrived 2026-07-30 and the operator
declined the standing delegation.** Closures remain **per-batch operator words**: each closure
batch is approved explicitly and is scoped to the batch presented. The trigger is therefore
**spent and reset**, not still pending — it is not re-fired by the next `/review-closures` run,
and no task row is filed (the U6 riders are record-file only, per confirmation 5).

The batch that carried this ruling closed exactly one row — **[#435]**, the single typed id —
with every other presented candidate ruled STAYS-OPEN and [#433] not re-adjudicated.

**Rider U6(a) is unaffected** and stays DEFERRED with its original trigger (the next night-batch
request).
