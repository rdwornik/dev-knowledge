# [#504] LANE C — paste-block for the stale fail-soft claim at `ARCHITECTURE.md:327`

- **Class:** verification (ADR-101 enum) · **Date:** 2026-08-06 · **Slug:** lane-c-arch-327
- **Subject:** `ARCHITECTURE.md` still describes `scripts/block_ff_push.py` as *"fail-soft to
  exit 0 on any git error"* — the posture the ADR-85 amendment 2026-08-03 §A6 retired. The code
  fix and its in-file docstring landed in this lane; `ARCHITECTURE.md` is **integrator-owned**,
  so this file carries the exact replacement instead of the edit.
- **Method:** read-only against `ARCHITECTURE.md` at lane base `df815c7c`. Lane C did **not**
  edit `ARCHITECTURE.md`.
- **Filename note:** the lane contract named this artifact
  `docs/audits/2026-08-06-lane-c-arch-327.md`. That name is **refused by a live hard gate** —
  see "Escalation 1" below. The name here is the minimal conforming variant.

---

## The paste-block

**Target:** `ARCHITECTURE.md` · **Anchor text** (unique in the file — do not trust a line
number, this lane's own edits already moved line numbers once):

```
HUB-ONLY; fail-soft to exit 0 on any git error.
```

At time of writing this sits at `ARCHITECTURE.md:327`, inside the hand-authored
`scripts/` inventory of Ch3 — **not** inside the generated `<!-- CODEMAP:START -->` /
`<!-- CODEMAP:END -->` block (lines 88–99). The codemap generator will not rewrite it, and
`codemap-freshness` has no opinion on it.

### OLD — remove these three lines verbatim

```
  pre-push`); HUB-ONLY; fail-soft to exit 0 on any git error. Client-side teeth (bypassable
  via `git push --no-verify`) — the `no_ff_merges` audit WARN stays the post-hoc backstop;
  bypass-proof server-side teeth deferred under #153 (#153; ADR-84; core-invariants #5).
```

### NEW — paste these four lines in their place

```
  pre-push`); HUB-ONLY; **fails CLOSED (exit 2) on internal error** (ADR-85 amendment
  2026-08-03 §A6). Client-side teeth (bypassable via `git push --no-verify`) — the
  `no_ff_merges` audit WARN stays the post-hoc backstop; bypass-proof server-side teeth
  deferred under #153 (#153; ADR-84; core-invariants #5).
```

Only the posture clause changes; the two-space continuation indent, the em dashes, and the
closing citation `(#153; ADR-84; core-invariants #5)` are preserved byte-for-byte. The bold
`**…**` matches the existing convention for posture words in this file (e.g. `:234`, `:521`).

### Verify after pasting

```bash
grep -n "fail-soft to exit 0" ARCHITECTURE.md      # must return NOTHING
grep -n "fails CLOSED (exit 2)" ARCHITECTURE.md    # must return the pasted line
```

### Two gate consequences the integrator inherits

1. **`ARCHITECTURE.md` is freshness-stamped.** Editing it without re-stamping `last_reviewed`
   trips the `canonical_freshness` A2 gate (FAIL blocks the commit). Per CLAUDE.md §4 the stamp
   means *re-read end-to-end and confirmed accurate* — a genuine re-read, not a touch. That
   re-read is the integrator's call; this lane does not presume it.
2. Editing this file also fires `normalize-dated-headers`, `codemap-freshness`, and
   `audit-health` (`ARCHITECTURE.md:500-501`).

---

## Scope check — is `:327` the only stale claim in `ARCHITECTURE.md`?

Enumerated every mention (`grep -n "block_ff\|block-ff" ARCHITECTURE.md`):

| Line | Content | Verdict |
|---|---|---|
| 321–329 | `scripts/block_ff_push.py` inventory entry | **STALE at `:327`** — this paste-block |
| 325 | names the `block-ff-push` hook wiring | fine, no posture claim |
| 499 | pre-commit roster entry, "#153 prevent half" | fine, no posture claim |

Rows `:235`–`:240` say `fail-soft (WARN)` about `no_ff_merges`, `doc_claims`, `git_backlog_drift`
etc. Those are the **audit checks**, which really are fail-soft — correct, leave them.

---

## Terra review — severity tally and dispositions

Run on the code-only diff **before** this prose file existed, to avoid the mixed-diff lane
collapse (a single `.py` routes a mixed batch to the code profile and the prose is never
doc-reviewed). Artifact: `docs/audits/2026-08-06-codex-lane-c-504-failclosed.md`
(model `gpt-5.6-terra`, `mode=diff-review`, head `47331e26`).

| Severity | Count |
|---|---|
| Critical | 2 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

The wrapper's own heuristic banner under-counted this as `Critical 1`; the artifact body
carries **two** Critical bullets. The table above is the body count.

**C1 — "any internal error → exit 2" is false; `find_violations` can still degrade to `[]`
and `main()` returns 0.** — **ACCEPTED, fixed in-lane, docstring only.** Terra is right that
`violations_in_range` proves only `git rev-list` readable; a failure inside the delegated
`git log` afterwards still returns `[]`. The claim was overbroad, so the claim was narrowed —
the docstring now enumerates COVERED / NOT COVERED / BY DESIGN and names that residual window
explicitly. Closing the window itself would mean changing the shared FF-signature (the one
scan `validate_no_ff` and this gate deliberately share), which is a behaviour change well
outside an S-class claim fix — see Escalation 2.

**C2 — make `_rev_parse` / `_reconstruct_main_range` raise instead of degrading to `''` /
`None`.** — **REJECTED in-lane.** Terra's cited `:159` and `:175` are the post-edit positions
of the pre-edit `:153` and `:169` — the exact pair this lane's contract forbids touching as a
hard anti-pattern, on the ground that their fail-soft degradation is *correct*. It is also a
behaviour change, not a claim fix. Recorded, not actioned — see Escalation 2.

---

## Escalations (budget items (b) and (c))

**Escalation 1 — rule-vs-contract conflict on this artifact's own filename.** The contract
named `docs/audits/2026-08-06-lane-c-arch-327.md`. The ADR-101 Rule B gate refuses it. Verified
live, not read from code:

```
validate_hermetization: refused -- ADR-101 hermetization violation(s):
  docs/audits/2026-08-06-lane-c-arch-327.md: class: '2026-08-06-lane-c-arch-327.md' has no
  CLOSED-enum <class> token after the date (ADR-101 R3: technical/functional/qa/census/
  verification/ecosystem-audit/conformance-nightly-digest/changelog-review/codex/fresh-eyes/
  incident-evidence; whole-token longest-match)
```

Resolved in-lane by the minimal conforming rename — `verification` class inserted after the
date, slug `lane-c-arch-327` unchanged — because the alternative was `--no-verify` past a hard
gate. Flagged rather than silently absorbed: a batch contract that names an off-enum audit
filename will do it again, so the fix belongs in whatever authors the contracts.

**Escalation 2 — one residual fail-soft window and one contested helper pair, both out of
S-class scope.** C1's narrow window (`find_violations` failing after the range probes readable)
and C2's leaf-helper proposal are both real design questions about the shared FF-signature.
Neither is a claim fix and neither should ride an S-class lane. They want a ticket.

**Cross-lane note — lane B (`lane-b-503-doc-currency`, [#503]) owns this exact class.**
Everything lane C touched is a **doc-currency** defect: prose that outlived the behaviour it
describes. The `:39` docstring, `ARCHITECTURE.md:327`, and the ADR-85 text below are three
instances of one class, and that class is lane B's subject, not lane C's. Two consequences for
the integrator:

- **Collision risk on the same anchor.** If lane B's currency sweep also rewrites
  `ARCHITECTURE.md:327`, the paste-block above is redundant and the two lanes conflict on one
  line of one integrator-owned file. Apply lane B first, then re-run the two `grep` checks
  above; if `fail-soft to exit 0` is already gone, drop this paste-block rather than merge it.
- **Coverage question worth asking lane B.** Lane C found its two stale claims by enumerating
  one symbol (`grep -n "block_ff\|block-ff" ARCHITECTURE.md`) — a per-symbol sweep, run because
  the contract named one organ. If lane B's sweep is doc-driven rather than symbol-driven, the
  ADR-85 instance below is the kind it structurally cannot see, because it lives in an
  immutable file where "stale" is not obviously a defect.

**Escalation 3 — `ADR-85` carries the same retired posture as live text.**
`docs/decisions/ADR-85-session-lifecycle-enforcement.md:322-324` reads *"`block_ff_push.py:205-207`
currently **fails soft** … Until that fix lands, the prevent organ can be silently absent."*
That fix has landed. ADRs are immutable (CLAUDE.md §5 item 3 — amend by appending a marker,
never edit prose in place), and this is the amendment's own pre-fix diagnosis, so it is arguably
correct as a historical record. Surfaced, deliberately untouched — a reader arriving at ADR-85
cold still reads "currently fails soft" about code that no longer does.
