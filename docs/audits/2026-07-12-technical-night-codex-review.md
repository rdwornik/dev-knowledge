# Codex adversarial review — night-batch 2026-07-11→12 (N1)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-12
- **Source-session:** night-batch N1; Codex gpt via codex-cli 0.144.0, `--sandbox read-only`, effort=high
- **Status:** complete — 10 HIGH surfaced (4 arc = triage inputs; 6 post-build = FIXED tonight); 0 critical/med/low
- **Model:** reviewer = Codex (codex-cli 0.144.0); orchestrator = claude-opus-4-8

## Executive so-what

Five Codex passes ran: 3 over today's landed arc (#312 reporter + doc-rot, LANE-B carriers,
v1.3.0 manifest), 2 post-build over the night's own #306/#307 code, 1 E2E coverage-gap pass.
**10 HIGH findings, 0 critical.** The 6 post-build findings were all in files this night
touched → fixed in-branch tonight (trivial-and-owned rule) with regression tests. The **4 arc
findings are morning-triage inputs** — they sit in already-landed code (#312/#302/#309), NOT in
tonight's builds, so per the hard limits they were captured, not fixed. Two of them (A3 adapter,
A4 carrier-append) are real **enforcement-transfer gaps that undercut the #302/#309 parity work**
and deserve early triage.

## Findings — ARC (morning-triage inputs; NOT fixed tonight)

```
id  sev   file:line                        finding + fix direction
A1  HIGH  scripts/boundary_report.py:129   duplicate owner=hub region ids are silently
                                           overwritten (dict collapse in diff_consumer +
                                           build_baseline); a malformed file with dup ids can
                                           report CLEAN if the surviving body matches.
                                           fix: detect dup ids pre-map, emit a parse WARN.
A2  HIGH  scripts/validate_doc_rot.py:156  _is_comment_only exempts EVERY full-line HTML
                                           comment, not just machine markers/sentinels — real
                                           prose can hide in <!-- --> and dodge the CLAUDE.md
                                           budget. fix: allowlist known metadata comment forms
                                           (methodology markers, scope/version, generated).
A3  HIGH  .pre-commit-hooks.yaml:77        block-ff-push carrier rides pre-commit's pre-push
                                           adapter, which may not preserve the full native ref
                                           stream: empty-remote initial push + multi-ref pushes
                                           can leave block_ff seeing no protected main range ->
                                           returns 0 -> a consumer lands a direct/FF push to main
                                           unblocked. fix: reconstruct every pushed main range
                                           (or native wrapper); add E2E for those cases.
                                           NOTE: tonight's E2E gauntlet adapter probe REFUSED the
                                           COMMON single-ref push (rc=1) — so A3 is edge-case-
                                           specific (empty-remote / multi-ref), not a blanket
                                           failure. Those edges remain unexercised.
A4  HIGH  deploy/manifest-v1.3.0.yaml:173  carrier only bumps `rev` for an existing hub-hooks
                                           entry; it does NOT append the new block-ff-push /
                                           backlog-id-on-close ids -> a v1.2.0 consumer can be
                                           RECORDED v1.3.0 while still lacking both new gates.
                                           fix: make the carrier append+verify hub-hooks additions.
A5  HIGH  deploy/manifest-v1.3.0.yaml:170  hub_hooks.hooks omits codemap-generate / toc-generate
                                           while the component rows claim them deployed. fix: add
                                           both ids to the target hook list, or drop the claim.
```

## Findings — POST-BUILD (all FIXED tonight, in-branch, with tests)

```
id  sev   file (this-night build)          finding -> fix (commit)
P1  HIGH  validate_hermetization.py (#306)  rename bypass: --diff-filter=A skips a rename (R),
                                            so a rename to a bad path slipped through.
                                            FIXED: --no-renames (rename -> delete+ADD). [26f3802]
P2  HIGH  validate_hermetization.py (#306)  malformed slug: `technical-.md` / `technical--foo.md`
                                            passed. FIXED: _SLUG_RE post-class validation. [26f3802]
P3  HIGH  validate_hermetization.py (#306)  uppercase `.MD` dodged Rule B entirely. FIXED:
                                            extension-case-insensitive apply + full-filename
                                            casing check. [26f3802]
P4  HIGH  gen_intake_index.py (#307)        missing intake-id rendered a misleading `[2026]`.
                                            FIXED: loud `MISSING-ID` label. [3223f90]
P5  HIGH  gen_intake_index.py (#307)        _splice validated only marker presence; reversed/dup
                                            markers could corrupt doctrine. FIXED: exactly-one +
                                            order validation. [3223f90]
P6  HIGH  gen_intake_index.py (#307)        unterminated frontmatter scanned whole-doc as meta.
                                            FIXED: track closing ---, else empty. [3223f90]
```

## Findings — E2E COVERAGE GAPS (E2E-3 pass — the honest boundary of the E2E claim)

These are gaps in the GAUNTLET's coverage, NOT defects in it — the E2E is honest about what
it asserts. Several are already covered by the organs' OWN unit tests (noted). This list is
the deliverable's point: the explicit boundary of tonight's E2E claim.

```
sev   gap (tests/test_e2e_consumer_lifecycle.py)                covered elsewhere?
HIGH  real pre-push ADAPTER not asserted (capture-only) — a     partially: the native-stdin
      broken adapter/PRE_COMMIT_* mapping could pass this E2E    gate LOGIC probe IS asserted;
      while real pushes are unprotected                          the adapter is Codex-A3's own
                                                                 concern, deliberately capture-only
HIGH  hermetization leg self-skips on feat/e2e-lifecycle         yes: 3 green standalone runs on
      (#306 not on this branch) — no red witness in THIS diff    feat/306 (evidence file); auto-
                                                                 activates when #306 merges to main
HIGH  synthetic repo: local hook wiring bypasses the REAL        NO — real-carrier fidelity
      manifest/deploy carrier (hub repo + rev pin + carrier      (deploy detect/apply/verify,
      verify + detect/apply/verify transitions)                  packaged .pre-commit-hooks.yaml)
                                                                 is genuinely unexercised
HIGH  floor lifecycle entirely outside the gauntlet (no          NO — floor carrier + hash guard
      CLAUDE-FLOOR.md / sidecar hash / check_floor_hash /         + SessionStart self-arm are a
      floor-hash-verify / SessionStart self-arm)                  distinct untested lifecycle
MED   block-ff edges narrow (no true-FF merge, non-main push,    yes: block_ff_push.py own unit
      new-remote main, main deletion, fail-soft git-error)       tests cover these states
MED   backlog-id: only close-without-id (no close-WITH-id pass,  yes: check_backlog_commit_msg
      multi-id, reword-no-trigger, missing-BACKLOG fail-open)    own unit tests cover these
MED   reporter: mocked-fleet match/drift/parsewarn only (no      yes: test_boundary_report.py
      unmarked/missing/orphan/unavailable/hub-skip/CLI digest)   covers these unit-level
```

**Routing:** the two genuinely-uncovered lifecycle areas — **real-carrier install fidelity**
(HIGH) and the **floor lifecycle** (HIGH) — are the honest limit of tonight's rehearsal. Recommend
they gate the E2E's scope-claim wording (narrow the claim, or extend the gauntlet in a follow-up).
They are NOT blockers for the ai-council rollout GO (the carried gates themselves are proven to
fire); they bound how much the E2E rehearses vs the real carrier.

## Recommendations / routing

- **Triage first (real parity gaps):** A3 (pre-push adapter ref-stream) + A4 (carrier hook-append)
  — both undercut the #302/#309 branch-protection/commit-msg parity the fleet rollout depends on.
  Recommend filing both as BACKLOG follow-ups against #302/#309 before the ai-council rollout arms
  the carriers.
- **A1/A2** are hub-organ hardening (boundary_report dup-id WARN; validate_doc_rot comment
  allowlist) — file against #312 / the doc-rot organ.
- **A5** is a manifest-roster coherence fix — pairs with the release-lint.
- **P1-P6** need no action (fixed + tested tonight); listed for the record.

## Scope / method

5 Codex passes, each `codex exec --sandbox read-only -c model_reasoning_effort=high` over a git
diff range (arc merges 6ca9d7e / fa7a775 / f583509; build branches feat/306 / feat/307;
feat/e2e-lifecycle). Code-only (Codex excludes .md) — the CLAUDE.md Form-A marker prose was NOT
Codex-reviewed (out of its code scope); it was placed by a genuine end-to-end read this session.
Every finding carries a file:line cite. Codex did not run tests (read-only constraint).
