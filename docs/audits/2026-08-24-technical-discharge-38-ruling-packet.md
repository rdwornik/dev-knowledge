# DISCHARGE-38 — PHASE 2 RULING PACKET (architect, 2026-08-24)

Paste this whole file into the waiting DISCHARGE-38 session. It answers every row, the four
register-side items, and grants eight bounded edit authorizations (E1–E8). Where a granted edit
turns out larger than the cited lines, STOP that item, keep its row open, report — never widen.

**Expected outcome, stated up front: 27 certain closures + up to 3 conditional = 27–30.
Open count 212 → 182–185. Silent-rule 443 → 443. Suite stays 3 failed. Zero births.**

---

## A. The 21 CLEAN — 19 APPROVE as drafted, 2 AMEND

**APPROVE as drafted (19):**
`[#344]` `[#350]` `[#346]` `[#353]` `[#425]` `[#408]` `[#417]` `[#423]` `[#239]` `[#443]`
`[#338]` `[#412]` `[#415]` `[#463]` `[#464]` `[#409]` `[#410]` `[#411]` `[#366]`

Notes that bind the landing:
- `[#409]`/`[#410]`/`[#411]`: the `###` heading literally carries the id — your pre-note 1 is
  approved for ALL 21 (strictest form everywhere).
- `[#417]` and `[#399]`: sections cite the LIVE locators you verified (`audit.py:4130-4139`,
  `HANDOFF_PROCESS.md:723`), never the stale ones.
- `[#353]`: the recorded honest limit (`current_branch()` returns `None` → ALLOWS on git failure)
  additionally goes into your final report's queue section as a candidate small fix — fail-open
  on error is worth one guard clause someday. Not this session's work.

**AMEND `[#484]`** — add one sentence to the section: *"Measured on the sole operator machine in
scope; if a second machine enters service, the per-machine measurement is owed there before 'on
each' is claimed."* Then it closes. Your instinct to offer this was right; take it.

**AMEND `[#453]`** — one substitution, and it matters: leg (3)'s precedent must NOT be *"a
recorded `--no-verify`"*. `--no-verify` is banned in this repo without exception; the sanctioned
lever for exactly this case is a **declared `SKIP=audit-health` with the measured reason in the
commit body** (Ch8 Q1), which is what every lane and the integrator actually used this window.
Replace the precedent sentence accordingly. A register section must not enshrine a banned lever.

## B. The 17 NEEDS-JUDGMENT — ruled one by one

**`[#162]` — APPROVE section + E1 grants the sweep → closes if green.**
The scoping ruling stands as drafted (actor = bare noun; mode never bare, always `architect`
mode). **E1:** grep the three named files for bare-mode uses of "architect" that violate the
ruled scoping and conform them — mechanical word-level edits only. If anything needs more than
word-level substitution, stop, keep the row open, report the sites.

**`[#349]` — APPROVE both, with the retirement sentence.** The fold lands AND `[#344]` closes in
the same packet; therefore `[#349]`'s section carries this sentence verbatim: *"The test-then-close
inheritance discipline is retired as a hub obligation, not orphaned: its only buildable form is a
consumer-side `~/.claude` guard, which R-2 places with the operator."* Eyes open, no zombie owner.

**`[#389]` — APPROVE section; row stays OPEN.** R6 = SOFT is ruled on your boundary argument
(off-repo prompts are unreachable by hooks; the contract is the enforcement surface). The
per-field WARN + tests remain the row's open leg.

**`[#210]` — APPROVE section + E2 → closes if the three entries are dead.**
Shape (b) ruled; (a) refused — your overtaken-by-`block-commit-on-main` reasoning is exactly
right, and note the class is not merely exempted but eliminated by a live gate. **E2:** remove the
three journal-wrap per-instance entries from `ecosystem/disposition-register.yaml` **only after
verifying each matches no live WARN** (MINI flagged 3 `[stale]` dispositions — check whether these
are those). Any of the three still matching a live WARN → stop, row stays open, report.

**`[#418]` — APPROVE section; row stays OPEN.** The structural diagnosis (throttle keyed on a
gitignored per-tree file) and the recorded fix-shape land. The reproduction artifact the Done-when
demands unconditionally does not exist; do not manufacture it here. Queue note: it is one
`git log --format=%cd --date=short automation/fleet-audit | sort | uniq -c` away for a future session.

**`[#414]` — APPROVE section; row stays OPEN.** Organ (b) ruled; (a) refused — a merge cannot
name its own hash, so demanding the HEAD SHA makes the discharge unsatisfiable (your own Step-4
deviation this morning is the live proof); (c) refused as unbuildable from inside the policed
session. The recorded-operator-GO mechanism stays the open leg.

**`[#456]` — APPROVE with the substitution ruled lawful → closes.** The Done-when's intent is a
durable, findable enumeration; a row file is deleted at closure, so "in this row" is the one place
the enumeration cannot durably live. Ruled: the register section + **the closing commit message
carrying all 38 ids** satisfy it. Routing per ADR-108 §A as drafted, `[#346]` operator-owned,
`[#537]` flagged mis-cohorted.

**`[#263]` — APPROVE section + E3 → closes if no new RED.** **E3:** remove the
`mermaid_theme_directive` exempt entry (2 lines) from `ecosystem/doc-code-edge.yaml`, then run the
doc-code-edge check. If removal surfaces a RED, revert the removal, keep the section, row stays
open, report — the exemption was load-bearing and that is a different finding.

**`[#351]` — APPROVE section; date RATIFIED: next review 2026-11-24; row stays OPEN.** The
coordinated-path artifact across the nine `adr104-fleet-members` is unconditional and unbuilt.

**`[#341]` — AMEND (i), then APPROVE section; row stays OPEN.** (i) may not cite R-1 as settling
admission: R-1's basis is refuted by measurement (the phrase it cites appears nowhere in ADR-53;
ADR-53 Decision 2 stands `Accepted`; `validate_hermetization` refuses the file on two machines)
and **intake #42 (2026-08-24) carries the fork, architect leaning retire-R-1.** Rewrite (i) as:
*"Nested-`AGENTS.md` precedence stays OPEN pending intake #42; Codex activation must not assume a
root `AGENTS.md` exists."* (ii)–(iv) as drafted. The activation run and §16 stay the open legs.

**`[#491]` — APPROVE the R-G section; row stays OPEN.** R-G lands exactly as drafted —
retrieval-only, measured boundary, 3.7-Flash refusal recorded, effort medium per Q8. Standing
instruction into the section: *"the next genuine retrieval task in any lane routes to the Gemini
lane and doubles as the acceptance run this row still owes."*

**`[#537]` — APPROVE via the withdrawal option → closes. E7.** Its own Done-when offers "(or the
branch is withdrawn)". **E7:** edit `tasks/537-*.md` to withdraw the disposition-token branch,
citing this packet. The test conjunct is ruled **discharged by mootness** — a test pinning a line
against a branch that no longer exists has no subject — and the section records the withdrawal,
the mootness, and your grep proof that the vocabulary has no user outside the closing rows.

**`[#356]` — APPROVE section + E4 → closes.** The named alternative is structurally impossible
(the yaml's documented data model forbids per-rule entries) — a Done-when naming an impossible
shape is a defect, same class as `[#577]`. **E4:** rewrite the alternative leg of
`tasks/356-*.md`'s Done-when to: *"or `protocols/STANDING_RULINGS.md` carries a section naming
`[#356]` recording each item's owner and next review date."* The section then lands with
**owner: operator, next review 2026-11-24**, records the ORIGINAL wording + the defect + the
replacement in full (transparent goalpost repair, not a quiet one), and the row closes.

**`[#358]` — your refusal is CONFIRMED; E5 → closes without a register section.** There is no
defensible reason for the divergence to stand, and the register will not bless a doc-vs-code
contradiction. **E5:** correct the misdescriptions to the blocking reality — 
`ecosystem/parity-surfaces.yaml:6` and the `fleet_parity.py` comments at `:142`, `:898`, `:1986`
(cite `[#337]`'s registration as the authority). Comment/manifest text only, zero behaviour
change; run the check after. Row closes on its first leg. Declining to draft was the correct act
and is recorded as such.

**`[#399]` — APPROVE + E6 → closes.** Ruled: the template's existing first line ("DEFERRED STUB …
v5 bundles no longer carry a per-bundle README") states the status with MORE precision than either
enum word and satisfies the second conjunct. **E6:** one-line correction at
`protocols/HANDOFF_PROCESS.md:723` — the false "rendered idempotently from the template" claim is
marked as describing the deferred design, with the seeder's actual source named. Fixing a false
protocol claim beats registering distrust of it (M6: docs to ACTUAL state).

**`[#362]` — APPROVE section; row stays OPEN.** The six named dispositions and the
`mixed-uncertain` inversion finding (safety default → permissive default in v5) land — that
finding alone justifies the section. The 49-rule enumeration is a seven-ADR re-read this session
did not perform: do not attempt it. Queue note: bounded future lane. The `[#242]` ordering clause
is respected — `[#242]` is not in this cohort and must not be closed anywhere before `[#362]`.

**`[#347]` — parse ruled: (a). APPROVE section; row stays OPEN.** The "or" attaches to the
safe-deletion clause only — both alternatives it joins are about documenting the pattern, and
reading it wider would let a deferral sentence discharge a decomposition mandate. The
decomposition into filed rows stays required and becomes a named consumer of the births this
packet banks. The safe-deletion reasoning (no deletion-by-pattern-match licence) is exactly right.

## C. Register-side acts — all four approved

1. **R12 gets its register section** (your pre-note 3): a short `S.` entry recording the ruling,
   its date, and pointers to `silent_rule_detector.py:51-66`, its test, and the baseline
   provenance. The ruling that unblocked the register lives in the register. **E8a.**
2. **The stale Editing note** (pre-note 2): do NOT rewrite it in place. **E8b:** append one dated
   line beneath it: *"(2026-08-24, post-R12: this file is excluded from the silent-rule detector's
   scope; the declarative-phrasing constraint above no longer applies — write rulings in whatever
   mood is clearest.)"* Append-discipline holds even for metadata.
3. **Metric expectations** (pre-note 4): confirmed — 443 → 443 with register-only attribution now
   meaning zero movement; open rows 212 → 212 − N; suite 3 failed.
4. **Closing mechanics** (pre-note 5): confirmed as written — terminal `status:` AND manifest-node
   removal, `gen_task_tree.py --emit-source` + `--check`, no hand-edit of `BACKLOG.md`.

## D. Phase 3 execution order

1. Register appends (21 + 6 open-row sections from B + R12 + Editing-note line) — one commit.
2. Bounded edits E1–E7, each verified per its own condition — one commit, or split if cleaner.
3. Closures: every row marked "closes" above whose conditions held. List the final set in the
   closing commit message, including `[#456]`'s 38-id enumeration.
4. Regenerate, suite unpiped vs 3-failed baseline, validators, ledger line
   (`window: N closed / 0 born / net −N` + banked), JOURNAL entry (anchor-before-merge lesson from
   this morning applies), `D38-FINAL`, STOP. No push.

**Conditional rows report their outcome explicitly** — "closed" or "held open because <condition>
failed" — never silently either way.
