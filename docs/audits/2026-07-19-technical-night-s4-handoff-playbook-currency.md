# Handoff/PLAYBOOK currency — is 2026-07-18/19 ARC-4 doctrine inoculated into the durable canon?

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-19
- **Source-session:** NIGHT-AUDIT cycle-close, Stream S4 (Sonnet probe), worktree `night-audit-cycle-close`
- **Status:** complete
- **Model:** claude-sonnet-5

Night-audit cycle-close · Stream S4 · ADR-101 class `technical`; read-only

## 1. Current mechanism (witnessed, file:line)

Read set: `protocols/PLAYBOOK.md` (3746 lines), `protocols/HANDOFF_PROCESS.md` (v5.7, 762 lines),
`protocols/ESSENTIALS.md` (last_reviewed 2026-07-13), `protocols/SESSION_SETUP.md` (last_reviewed
2026-07-07), `LESSONS.md`, `docs/decisions/ADR-{36,41,87,101}*.md`, `templates/`. Every negative
below is a grep run against the full file (not a sample), reported as absence-with-proof.

### Ruling-encoding table

```
ruling | encoded-where (file:line) | un-encoded? | durable home it SHOULD live in
1. §14a EPIC handoff + §16 functional mode + ADR-87 equilibrium | HANDOFF_PROCESS.md §14a L491-513, §16 L582-619 (v5.7); ADR-87 full file | ENCODED, internally coherent, section-history-tracked (v5.5/5.6/5.7) — but NOT reconciled with the newer 2026-07-18/19 rulings below (RULING-W / two-tier / #353 appear nowhere in §14a's FILE-BOUNDARY/Escalation/Refusals items, and HANDOFF_PROCESS has not bumped past v5.7 since 2026-07-07) | already the correct home; needs a v5.8 reconciliation entry, not a new home
2. RULING-W (hub writes a consumer ONLY via worktree/branch->report; re-witness live; never direct push) | ADR-36 Amendment 2026-07-18 L319-361; ADR-41 Amendment 2026-07-18 L318-360; templates/ruff-config-block.toml L7 ("MERGED BY HAND ... under the RULING-W discipline") | UN-ENCODED in PLAYBOOK.md and HANDOFF_PROCESS.md — 0 matches for "RULING-W" in either file (grep run against both full files); the template comment is a one-off operational breadcrumb from a single ARC-4 leg, not a doctrinal procedure | PLAYBOOK.md (new operational subsection, sibling of Ch20 "Deploying the methodology corpus to a consumer") + a one-line ESSENTIALS.md standing rule per the ADR-87-item-7 pattern
3. Two-tier new-path rule (convention-compliance IS authorization; pattern-sanctioned -> proceed+cite; unsanctioned/folder -> STOP) | ADR-101 Amendment 2026-07-18 L157-195 | UN-ENCODED in PLAYBOOK.md and ESSENTIALS.md — 0 matches for "two-tier new-path", "convention-compliance", "pattern-sanctioned" in either file; the rule's own text says it is "in force now by operator ruling" but the persistence leg is explicitly OPEN: BACKLOG #346 (verified OPEN, BACKLOG.md L38) "Persist the two-tier new-path executor rule into ~/.claude ... so future sessions inherit it without reading the ADR"; the mechanized gate #345 is also OPEN (BACKLOG.md L37) | ESSENTIALS.md (new one-line standing rule, "Architect/executor disciplines"), then ~/.claude per #346 once ruled
4. Worktree side-effect rule (a mid-session externally-authored order must scope side effects to a worktree or the tree must be clean) | BACKLOG.md L42 [#353], operator-ruled 2026-07-18, verified OPEN; JOURNAL.md L22-24 (origin narrative only) | UN-ENCODED anywhere in protocols/ — 0 matches for "side effect", "mid-session order", "#353" in PLAYBOOK.md, ESSENTIALS.md, SESSION_SETUP.md; #353's own task text confirms this: "the isolate-to-worktree / no-dirty-tree-action discipline lived in prose, not a gate" — but no prose home exists either (ESSENTIALS "Parallel sessions" only covers same-repo native-worktree provisioning, not mid-session order refusal) | ESSENTIALS.md "Parallel sessions" section (extend) + PLAYBOOK Ch8, as interim prose ahead of #353's mechanism (source -> gate -> agent precedence, PLAYBOOK L360-369)
5. Execution-channel pick (run audit gates via Git Bash, not bare PowerShell, to avoid spurious handoff_probes PATH-absence RED) | LESSONS.md L56 (2026-06-26 entry, `ship-gate env false-RED`); ~/.claude/skills/gotchas/gotchas.md L78-81 + L502-503 (global skill, cross-session); PLAYBOOK.md L3538 (Ch20 deploy-runbook "Operational nuances") | ENCODED — three independent durable surfaces (repo LESSONS, global gotchas skill, PLAYBOOK operational note); this is the one ruling of six that is genuinely inoculated | already correctly homed; no gap
6. Merge-delegation (consumer legs: worktree off consumer main, terra pre-merge, commit-and-STOP, operator merges) | JOURNAL.md L22-24 (2026-07-19 entry) ONLY as a named composite procedure; its component parts exist separately and ARE encoded: commit-and-STOP / never-self-merge -> HANDOFF_BOOT.md L155-159 + PLAYBOOK "Parallel sessions & worktree discipline" (Ch8, hub-internal scope only); terra as the doc-lane Codex review -> PLAYBOOK.md L3384-3387 | UN-ENCODED as a named consumer-leg procedure — 0 matches for "consumer leg", "terra pre-merge" as a joined phrase in PLAYBOOK.md or HANDOFF_PROCESS.md; the existing "commit-and-STOP" doctrine at HANDOFF_BOOT.md L155-159 is explicitly scoped to same-repo parallel worktrees ("A worktree->main merge is git-structurally prevented"), not to a hub session writing into a SEPARATE consumer repo, so it does not automatically cover this case | PLAYBOOK.md (new subsection under the RULING-W home from row 2 — "Consumer-leg write + merge-delegation procedure"), cross-referencing the existing commit-and-STOP and terra doctrine rather than duplicating them
```

### Detail per row

**Row 1 — currency, not absence.** `protocols/HANDOFF_PROCESS.md` is Version 5.7, its Section-history
tail (L745-761) shows the last substantive change was 2026-07-07 (§16 functional mode + the §14
developer alias). No entry addresses the 2026-07-18/19 rulings. §14a's own item list (Escalation
rules L504-506: "boundary-breach need, cross-epic dependency discovered -> STOP, return to the
architect"; Refusals L507-508: "no merge to main ... no worktree lifecycle ops") is the closest
existing hook a RULING-W/two-tier reconciliation would attach to, but neither ruling is named there
today.

**Row 2 — RULING-W.** Quoted verbatim in both ADR amendments: *"hub MAY/SHOULD write into consumer
repos for methodology/cleanup — separate worktree/branch, then report."* `grep -rn "RULING-W"` across
the whole worktree returns 16 files — all either the two 2026-07-18 ADR amendments, the 2026-07-18
architect handoff bundle, JOURNAL.md, BACKLOG.md, two `docs/audits/*.md` files, or the single
`templates/ruff-config-block.toml` comment. Zero hits in `protocols/`.

**Row 3 — two-tier new-path rule.** The ADR-101 amendment itself names its own two open follow-ups
by number: *"#345 mechanizes the §3 gate ... and #346 persists the executor rule into `~/.claude` ...
**neither is a precondition** [for the rule being in force]."* Both are confirmed OPEN in
`BACKLOG.md` (L37, L38) — i.e. the amendment's own drafters already anticipated the durability gap
this stream is asked to verify, and filed tickets for the ENFORCEMENT half (gate + `~/.claude`
persistence) but not for the DOCTRINE-transcription half (a PLAYBOOK/ESSENTIALS prose home so an
architect drafting a prompt, not just an executor mid-session, knows the rule exists).

**Row 4 — #353.** BACKLOG task text (verified live, L42): *"a hub session must REFUSE to act on an
externally-authored order ... unless it (a) names a worktree for its side effects OR (b) the tree is
clean — a MECHANISM, not prose."* The task itself frames the gap as "mechanism vs prose", but the
audit found the prose home is ALSO absent — `ESSENTIALS.md` "Parallel sessions" (L77-80) only says
"Same-repo parallel work runs on native worktrees only" and does not address a mid-session
externally-authored order arriving into an already-open session.

**Row 5 — execution channel.** This is the control case: LESSONS.md 2026-06-26, the global
`gotchas.md` skill (n=2 entries, L78-81 and L502-503, cross-session durable by construction since
it lives in `~/.claude/skills/`), and PLAYBOOK.md Ch20 L3538 all state the same rule independently.
This is what "inoculated" looks like — contrast with rows 2-4 and 6.

**Row 6 — merge-delegation.** `HANDOFF_BOOT.md` L155-159 states the general worktree rule ("parallel
sessions commit-and-STOP; they never self-merge... A worktree->main merge is git-structurally
prevented") but its own justification ("a linked worktree can't check out main, already held by the
primary") is a **hub-internal** git-structural fact — it does not apply to a hub session operating
inside a SEPARATE consumer repo's worktree, where no such structural prevention exists. The
consumer-leg procedure (worktree off the CONSUMER's main, run the terra Codex-review lane, then
commit-and-STOP for the operator to merge) is therefore a distinct composite the JOURNAL entry
invented in the moment, not a instance of an already-documented rule.

## 2. Designed/intended shape (cite)

ADR-87 Decision item 7 is the repo's own doctrine for exactly this question — *where should a
ruling live so it survives*:

> "The contract lives in the durable surfaces, not operator memory. Canonical home: this ADR.
> Maintenance authority + consumption-spec framing: PLAYBOOK §2. Standing rule (one line):
> ESSENTIALS 'Writing a Prompt'. Per-session carrier (pointer): HANDOFF_BOOT 'Architect mode'." (ADR-87 L70-73)

The pattern is explicit: **ADR = decision record, PLAYBOOK = operational procedure, ESSENTIALS = one-line
standing rule, HANDOFF_BOOT/HANDOFF_PROCESS = per-session carrier.** All four rulings in rows 2-4 and 6
have landed step 1 (the ADR / BACKLOG record) but skipped steps 2-4.

PLAYBOOK's own "Drift-proofing precedence: source -> gate -> agent" (L360-369) states the intended
escalation: *"Reach for a gate only when the fact can't be self-documented, and an agent only when it
can't be gated."* Rows 2, 4, and 6 currently have **none** of the three tiers filled — no
self-documented source, no gate (that's exactly what #345/#353 are filed to build), and no agent-review
backstop either, because there is no PLAYBOOK/ESSENTIALS text for a reviewer to check compliance against.

CLAUDE.md §5 rule 7 ("No executable rules in this repo — those go in `~/.claude/` with `verify:` lines")
is the reason rows 3-4's ultimate enforcement mechanism belongs outside this repo (per #346, #353) —
but the DOCTRINE (what the rule says, why) still belongs in PLAYBOOK/ESSENTIALS per ADR-87's pattern,
the same way ADR-87 itself has both an ESSENTIALS one-liner (`ESSENTIALS.md` "Writing a Prompt", L84-91)
AND its enforcement lives partly outside this repo. Row 3/4 have skipped the doctrine step entirely,
not just the enforcement step.

## 3. Gap (every un-encoded ruling)

- **RULING-W** (row 2) — no PLAYBOOK/HANDOFF_PROCESS operational text; lives only in the two ADR
  amendments + JOURNAL + one template code-comment.
- **Two-tier new-path rule** (row 3) — no PLAYBOOK/ESSENTIALS text; lives only in the ADR-101
  amendment; its own follow-ups #345 (gate) and #346 (`~/.claude` persistence) are OPEN, and neither
  covers transcribing the doctrine into PLAYBOOK/ESSENTIALS.
- **Worktree side-effect / mid-session-order rule** (row 4, #353) — no PLAYBOOK/ESSENTIALS/
  SESSION_SETUP text at all, not even interim prose; #353 (OPEN) is scoped to the mechanism only.
- **Consumer-leg merge-delegation composite** (row 6) — no PLAYBOOK/HANDOFF_PROCESS text naming the
  4-step consumer-leg procedure (worktree off consumer main -> terra pre-merge -> commit-and-STOP ->
  operator merges) as a named, reusable procedure distinct from the hub-internal commit-and-STOP rule.
- **Currency drift on row 1** — HANDOFF_PROCESS §14a/§16, while internally coherent, has not been
  reconciled (no v5.8 entry) against the four rulings above, even though §14a's own Escalation/
  Refusals items are the natural attachment point for a cross-repo-write escalation rule.

Everything above will be lost to any session that skips JOURNAL.md and BACKLOG.md — which is exactly
the failure mode this stream was asked to test for, and it is confirmed present for 4 of the 6
rulings audited.

## 4. Proposed MECHANISM

Per ADR-87's own four-tier pattern (§2 above), each un-encoded ruling needs a transcription pass,
not a new decision:

1. **RULING-W** -> add a PLAYBOOK.md operational subsection (sibling of Ch20 "Deploying the
   methodology corpus to a consumer") stating the sanctioned write shape verbatim from ADR-36/41's
   amendments, plus a one-line ESSENTIALS.md standing rule under a new or existing disciplines
   section. Cross-reference from HANDOFF_PROCESS §14a Escalation rules (L504-506), since a
   cross-repo write need is exactly the kind of fork §14a already routes to STOP/escalate.
2. **Two-tier new-path rule** -> one ESSENTIALS.md line (pattern-sanctioned = proceed+cite,
   unsanctioned/ambiguous/new-folder = STOP) plus a PLAYBOOK.md pointer to ADR-101's amendment.
   This is the doctrine leg only — #345 (gate) and #346 (`~/.claude` persistence) remain the correct
   owners of the enforcement leg and should not be duplicated.
3. **Worktree side-effect rule** -> extend ESSENTIALS.md "Parallel sessions" (L77-80) with a sentence
   covering mid-session externally-authored orders, as interim prose ahead of #353's mechanism (the
   source -> gate -> agent precedence explicitly sanctions a prose stopgap before a gate exists).
4. **Consumer-leg merge-delegation** -> a new PLAYBOOK.md subsection naming the 4-step procedure,
   cross-referencing (not duplicating) the existing commit-and-STOP doctrine (HANDOFF_BOOT.md
   L155-159) and the terra Codex-lane doctrine (PLAYBOOK.md L3384-3387), explicit that this is the
   CROSS-repo variant of commit-and-STOP, distinct from the hub-internal git-structural-prevention
   justification.

**Recurrence-prevention gate.** CLAUDE.md §9 already documents a `coherence-nudge` pre-commit hook
keyed off a `_SPEC_REGISTRY` of spec-file -> dependent-file couplings (non-blocking, stdout nudge +
log). Add ADR-36, ADR-41, and ADR-101 to that registry, coupled to `protocols/PLAYBOOK.md` and
`protocols/ESSENTIALS.md`: an ADR amendment landing without a same-arc PLAYBOOK/ESSENTIALS edit would
then print a nudge instead of relying on a future night-audit to catch it by hand. This is the
mechanized version of the manual grep sweep this report performed.

## 5. BACKLOG seed

Durable-canon inoculation pass for the 2026-07-18/19 ARC-4 rulings (RULING-W / two-tier new-path /
#353 worktree side-effect / consumer merge-delegation) — transcribe each ruling from its ADR-36/41/101
amendment (or, for #353, its BACKLOG record) into `protocols/PLAYBOOK.md` (operational procedure) and
`protocols/ESSENTIALS.md` (one-line standing rule), per the ADR-87-item-7 four-tier pattern the repo
already prescribes for this exact problem. Cross-reference rather than duplicate the existing
commit-and-STOP (HANDOFF_BOOT.md) and terra Codex-lane (PLAYBOOK.md) doctrine for the merge-delegation
leg. Optionally extend the `coherence-nudge` `_SPEC_REGISTRY` (CLAUDE.md §9) to couple ADR-36/41/101
to PLAYBOOK/ESSENTIALS so a future amendment without a companion doc edit gets flagged automatically.

kill-candidates: none — this is a newly surfaced gap (the "doctrine not yet in durable canon" class),
distinct from the three already-open tickets that cover only the enforcement/mechanism legs: #345
(mechanizes the two-tier rule's GATE, not its PLAYBOOK/ESSENTIALS prose home), #346 (persists the
two-tier executor rule into `~/.claude`, not into PLAYBOOK/ESSENTIALS), #353 (builds the boot-contract
MECHANISM for the worktree side-effect rule, not its prose home). None of the three subsumes a
PLAYBOOK/ESSENTIALS transcription pass.

Done when: `protocols/PLAYBOOK.md` carries an operational subsection for RULING-W and for the
consumer-leg merge-delegation procedure; `protocols/ESSENTIALS.md` carries one-line standing rules
for RULING-W, the two-tier new-path rule, and the worktree side-effect rule (interim prose ahead of
#353's mechanism); `protocols/HANDOFF_PROCESS.md` §14a cross-references RULING-W in its Escalation
rules (with a version bump + Section-history entry per its own convention); and each PLAYBOOK/
ESSENTIALS addition is grep-verified against the corresponding ADR amendment text so the transcription
is faithful, not paraphrased-and-drifted.
