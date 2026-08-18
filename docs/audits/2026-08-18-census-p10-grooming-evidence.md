<!-- scope: meta -->
# P10 grooming evidence sheet — every open row, mechanically · 2026-08-18

**Produced by:** CC (`claude-opus-5`), lane `lane-f-p10-evidence`, branch
`worktree-lane-f-p10-evidence`, under the frozen contract
`docs/audits/2026-08-18-technical-p10-regen-lane-contract.md` (committed first, contract-of-record).
**Posture:** READ-ONLY DERIVATION. **No adjudication, no closures, no BACKLOG/`tasks/` writes, no
new committed scripts, no merge, no push.** Every cell below is *evidence*; the live / dead /
awaiting-ruling verdicts are the architect's, downstream. Nothing here proposes one.

**Why this file exists twice:** the 2026-08-18 recon produced this sheet once and its only copy died
with the job tmp dir. The architect ruled REGENERATE on the live tree rather than recover from
transcript — so this is a fresh deterministic derivation at the SHA below, not a reconstruction.

## §0 · Derivation provenance

```
derivation timestamp : 2026-08-18T13:07:27Z
ref scanned          : main = 328d108666d057133182e61d49f95f7ae0f68751
HEAD at derivation   : 328d108666d057133182e61d49f95f7ae0f68751
row set              : tasks/*.md with `status: open`  (the contract's definition)
first-parent merges  : 1173 scanned on main
```

## §1 · The answer first — mechanical summary

```
open rows                    194
git silent (n == 0 paths)     72   (37.1%)
>= 1 merge mention           113   (58.2%)
validator closures             1   (#505 — and ONLY #505)
open rows with a branch ref    4   (#502, #533, #554, #558)
```

Self-check (contract STEP 2), reconciled against the backlog generator's own figures:

```
propose_closures.open_tasks_from_backlog(BACKLOG.md, validate_backlog.parse) = 218
validate_backlog.py BACKLOG.md                                              = 218 tasks
tasks/ status census : open 194 · deferred 24 · closed 66 · retired 3 · superseded 1
194 open + 24 deferred = 218 = the generator's active list, exactly
set identity verified: (open ∪ deferred) == the generator's id set; residue []
```

The 218 figure is BACKLOG.md's whole *active* list — it counts deferred rows, which are not dead and
not open. The contract scopes this sheet to `status: open`, so 194 is the row count, and 218 − 194 =
24 deferred is the entire, fully-accounted difference.

## §2 · Two reading rules this sheet is built to enforce

**A MENTION IS NOT A CLOSURE.** The recon's first pass ranked `[#id]` merge mentions by recency and
took the newest as the closing commit. On the one case with an independently known answer it named
the wrong SHA. The `closure` column here is parsed from `validate_git_backlog` ONLY; the mention
count and its newest SHA sit in their own column and are *informative*, never authoritative.

The known-answer test, live at this SHA:

```
#505 — merge mentions on main : 12
       newest mention          : bbacd6c03  2026-08-11
       validator closure       : 25ff8ec37  2026-08-07
```

The newest mention is four days and eleven merges away from what the validator names. Ranking by
recency is not a closure detector.

Recorded so the architect can adjudicate `#505` downstream without re-deriving: the validator's
STRONG predicate is `propose_closures.CLOSES_RE` =
`\b(?:closes?|closed|fixes?|fixed)\s+\[#(\d+)\]` applied after quoted-context stripping, and the
text it matched in `25ff8ec37` is the **subject line** —
`Merge branch 'docs/consolidate-batch2-lessons' — batch-2 lessons become mechanisms; 3 rows filed, 0
closed [#505] [#430]` — i.e. the token `closed [#505]` inside the phrase *"0 closed"*. The same
commit's body says *"nothing closed on [#505]/[#502]"*. **That reading is the architect's call, not
this lane's** — reported as the mechanical fact it is, because a closure column that hides its own
match text is exactly the trap rule A exists to close. `#505` is also the sole `validate_git_backlog`
direction-(a) drift finding on the whole tree, and `[#556]` is the open row that already names it.

**`git silent` is the absence of evidence, NOT evidence of death.** A row is marked `git silent`
when *zero* backtick-quoted tokens in its body resolve against the tracked tree — which happens
when the row is written in prose, names a path that does not exist yet (most design/build rows do),
names a glob or brace form (`.claude/{agents,commands}`, `docs/handoffs/*/`), or names a surface
outside this repo. 72 of 194 rows are silent, and that number is a statement about how rows are
*written*, not about whether the work is alive. Do not read the `last touch` column as a liveness
signal on those rows; it is blank because there was nothing to measure.

## §3 · Column definitions (fixed by the contract's corrected method)

- **id / theme / title** — from the task file's own frontmatter (`tasks/<id>-<slug>.md`); title
  truncated to 60 chars, theme to 34, both with `…`.
- **last touch** — the newest commit date (`%cs`) on `main` of any tracked path the row names.
- **n** — how many distinct tracked paths the row resolved. Extraction rule (deterministic):
  backtick-quoted tokens only, first whitespace-separated word, trailing `,.;:)` and `/` stripped,
  `http*`/`#`/`[` prefixes skipped, then tested for membership in `git ls-files` or in the set of
  directories those files imply. `n == 0` → **git silent** (see §2).
- **merge mentions** — count of first-parent merges on `main` carrying `[#id]` in the **subject**,
  plus the newest such SHA and its date. Informative only (see §2).
- **closure (authoritative)** — from `validate_git_backlog.reconcile` and nothing else; `—` means
  the validator names no closing commit for that id.
- **branch refs** — every local or remote branch name containing the bare id as a standalone number.

## §4 · Commands used (verbatim, paste-reproducible)

Run from the repo root. Nothing below writes.

```bash
# row set + status census
grep -l '^status: open' tasks/*.md | wc -l
grep -h '^status:' tasks/*.md | sort | uniq -c

# the generator's own figures (the STEP-2 self-check denominator)
py scripts/validate_backlog.py BACKLOG.md
py -c "import sys,pathlib; sys.path.insert(0,'scripts'); \
from propose_closures import open_tasks_from_backlog,_load_validate_backlog; \
vb=_load_validate_backlog(); \
print(len(open_tasks_from_backlog(pathlib.Path('BACKLOG.md').read_text(encoding='utf-8'),vb.parse)))"

# authoritative closures (direction (a) STRONG, full history, --first-parent)
py scripts/validate_git_backlog.py

# the three git passes the sheet is built from
git ls-files
git log main --format=$'\x01%cs' --name-only
git log main --first-parent --merges --format=$'%H\x01%cs\x01%s'
git branch -a --format='%(refname:short)'

# the known-answer test
git log main --first-parent --merges --format='%h %cs %s' | grep -F '[#505]'
git show -s --format='%B' 25ff8ec3

# the sheet itself (inline helper — see §6; never committed)
py derive_p10.py "$(pwd)" main
```

## §5 · The sheet

| id | theme | title | last touch | n | merge mentions | closure (authoritative) | branch refs |
|---|---|---|---|---|---|---|---|
| [#23] | [E4] Decision management | Validate ADR frontmatter relation-fields | **git silent** | 0 | 0 | — | — |
| [#43] | [E6] Cross-repo universalization | Decide + | 2026-07-22 | 1 | 0 | — | — |
| [#71] | [E5] Canonical-file integrity | Reconcile ENVIRONMENT.md's `~/.claude/` directory tree with… | **git silent** | 0 | 0 | — | — |
| [#82] | [E6] Cross-repo universalization | Define per-repository agentic-review profiles | **git silent** | 0 | 1 · 65cd26a0f 2026-08-16 | — | — |
| [#99] | [E2] Enforced governance | FLEET-HEALTH digest names the failing check per red repo | **git silent** | 0 | 0 | — | — |
| [#112] | [E2] Enforced governance | adr_amend helper + ADR immutable-zone extension | **git silent** | 0 | 1 · a4fc652dc 2026-08-13 | — | — |
| [#116] | [E2] Enforced governance | Hooks hygiene | **git silent** | 0 | 0 | — | — |
| [#117] | [E2] Enforced governance | Evaluate prompt/agent-based hooks | **git silent** | 0 | 1 · 7f752a892 2026-08-11 | — | — |
| [#122] | [E7] Tooling & evaluation | Retire the PATH shim | **git silent** | 0 | 0 | — | — |
| [#123] | [E7] Tooling & evaluation | Routine observability convention + value review | 2026-08-16 | 1 | 1 · a4fc652dc 2026-08-13 | — | — |
| [#126] | [E7] Tooling & evaluation | Backpressure-loop pattern evaluation | **git silent** | 0 | 0 | — | — |
| [#127] | [E7] Tooling & evaluation | verify skill failure-output contract | **git silent** | 0 | 0 | — | — |
| [#130] | [E3] Lessons feedback loop | Memory-hygiene review | **git silent** | 0 | 1 · 8e8d55a2e 2026-08-16 | — | — |
| [#145] | [E3] Lessons feedback loop | Codification-completeness pass | 2026-08-16 | 1 | 1 · 65cd26a0f 2026-08-16 | — | — |
| [#146] | [E2] Enforced governance | De-hardcode-first doctrine + sweep | 2026-08-16 | 1 | 1 · b4862b9be 2026-08-16 | — | — |
| [#153] | [E2] Enforced governance | Enforcement-completeness pass | **git silent** | 0 | 0 | — | — |
| [#162] | [E1] Handoff continuity | Vocab decision | 2026-08-16 | 4 | 1 · a4fc652dc 2026-08-13 | — | — |
| [#170] | [E2] Enforced governance | Design + land the traceability-spine ADR | **git silent** | 0 | 0 | — | — |
| [#171] | [E2] Enforced governance | Build the conformance dashboard at `ecosystem/conformance.m… | **git silent** | 0 | 0 | — | — |
| [#185] | [E2] Enforced governance | GAP-2 deterministic gotcha-injection guard | **git silent** | 0 | 0 | — | — |
| [#189] | [E2] Enforced governance | Execute in ~/.claude | **git silent** | 0 | 0 | — | — |
| [#210] | [E2] Enforced governance | Convert journal-wrap no-ff WARNs from per-instance disposit… | 2026-08-18 | 3 | 2 · 40dd51d8f 2026-08-16 | — | — |
| [#220] | [E2] Enforced governance | MODIFY / semantic-drift axis | 2026-08-18 | 1 | 2 · a4fc652dc 2026-08-13 | — | — |
| [#227] | [E5] Canonical-file integrity | Relocate AGENT_FRAMEWORK.md out of protocols/ | 2026-08-18 | 3 | 1 · fbf4a2d02 2026-07-01 | — | — |
| [#234] | [E2] Enforced governance | Cross-repo probe validator | 2026-08-16 | 1 | 1 · fef026edc 2026-07-02 | — | — |
| [#239] | [E2] Enforced governance | Follow-up | 2026-08-16 | 2 | 1 · 65cd26a0f 2026-08-16 | — | — |
| [#241] | [E2] Enforced governance | Undeclared-edge groom | 2026-08-16 | 1 | 1 · bbacd6c03 2026-08-11 | — | — |
| [#242] | [E2] Enforced governance | ADR status-flip coherence check | **git silent** | 0 | 0 | — | — |
| [#244] | [E6] Cross-repo universalization | Essence-spec lifecycle epic | 2026-07-05 | 1 | 4 · 25b104ed6 2026-07-04 | — | — |
| [#245] | [E6] Cross-repo universalization | Add-path status-awareness | 2026-08-08 | 1 | 0 | — | — |
| [#263] | [E5] Canonical-file integrity | Protocols/edge-map reconciliation residuals | 2026-08-16 | 5 | 1 · 65cd26a0f 2026-08-16 | — | — |
| [#266] | [E3] Lessons feedback loop | Codify the test-scoped-grant language lesson | 2026-07-08 | 1 | 1 · b4862b9be 2026-08-16 | — | — |
| [#267] | [E2] Enforced governance | Scope-exercising arc extension | **git silent** | 0 | 4 · ffe4d875f 2026-07-06 | — | — |
| [#269] | [E5] Canonical-file integrity | Audit-index count-tiered shape + freshness hook | 2026-08-18 | 1 | 0 | — | — |
| [#271] | [E7] Tooling & evaluation | Nightly proposal loop | 2026-08-17 | 1 | 1 · 9997bc324 2026-08-16 | — | — |
| [#273] | [E7] Tooling & evaluation | Changelog-review staleness escalation | **git silent** | 0 | 1 · 02389890e 2026-07-07 | — | — |
| [#274] | [E7] Tooling & evaluation | Dogfood-signal prior in the /changelog-review ADOPT rubric | 2026-07-29 | 1 | 2 · 8e8d55a2e 2026-08-16 | — | — |
| [#276] | [E6] Cross-repo universalization | D2 per-consumer waiver-honoring | 2026-08-04 | 1 | 0 | — | — |
| [#277] | [E2] Enforced governance | propose_closures signal repair | 2026-08-18 | 2 | 2 · fa746e14b 2026-08-16 | — | — |
| [#278] | [E7] Tooling & evaluation | Test-suite hygiene epic | 2026-08-18 | 2 | 1 · a4fc652dc 2026-08-13 | — | — |
| [#281] | [E6] Cross-repo universalization | Re-peg the ai-council ADR-66 story-map convergence | **git silent** | 0 | 0 | — | — |
| [#285] | [E5] Canonical-file integrity | Extend hub freshness gating to PLAYBOOK | 2026-08-16 | 2 | 1 · 40dd51d8f 2026-08-16 | — | — |
| [#288] | [E7] Tooling & evaluation | Model-identity guard for unattended runs | **git silent** | 0 | 0 | — | — |
| [#289] | [E2] Enforced governance | Hub-own the OneDrive-Blue-Yonder guard | **git silent** | 0 | 0 | — | — |
| [#293] | [E1] Handoff continuity | Consumer runbook fan-out | 2026-08-17 | 3 | 1 · 94f9307b3 2026-08-16 | — | — |
| [#296] | [E2] Enforced governance | `audit.py repo <name> --repo-path` prints a report path tha… | 2026-07-31 | 1 | 0 | — | — |
| [#297] | [E2] Enforced governance | Lightweight/dry `observe-arc` coverage mode | **git silent** | 0 | 0 | — | — |
| [#298] | [E1] Handoff continuity | Handoff-generator polish | **git silent** | 0 | 0 | — | — |
| [#303] | [E2] Enforced governance | Make seed_runbook.py child-class-aware | **git silent** | 0 | 0 | — | — |
| [#317] | [E7] Tooling & evaluation | Default-parallel test invocation | **git silent** | 0 | 3 · 7c1b94fc5 2026-07-11 | — | — |
| [#323] | [E2] Enforced governance | Design question | **git silent** | 0 | 0 | — | — |
| [#324] | [E2] Enforced governance | Phase-6 axis-2 carrier | **git silent** | 0 | 2 · 9997bc324 2026-08-16 | — | — |
| [#327] | [E6] Cross-repo universalization | Protocols-as-interface genre ruling | 2026-08-16 | 2 | 0 | — | — |
| [#329] | [E6] Cross-repo universalization | VS Code ownership visualization | 2026-08-07 | 3 | 0 | — | — |
| [#331] | [E6] Cross-repo universalization | Consumer BACKLOG schema adoption ruling | 2026-08-04 | 1 | 0 | — | — |
| [#332] | [E6] Cross-repo universalization | Fleet dependency-version parity | 2026-08-04 | 1 | 3 · 2bc02196c 2026-07-13 | — | — |
| [#334] | [E6] Cross-repo universalization | Fleet-wide ruff hook id migration `ruff` → `ruff-check` | 2026-08-16 | 1 | 1 · 97cf58e06 2026-07-12 | — | — |
| [#335] | [E2] Enforced governance | Exempt `templates/` from the `reconciled_versions` check | 2026-08-12 | 2 | 0 | — | — |
| [#338] | [E7] Tooling & evaluation | codex-review drift consolidation | 2026-05-19 | 1 | 2 · 8a0912785 2026-08-13 | — | — |
| [#340] | [E7] Tooling & evaluation | /ship pre-flight validator honors the consumer repo's canon… | **git silent** | 0 | 0 | — | — |
| [#341] | [E7] Tooling & evaluation | Codex producer-lane activation mechanism | **git silent** | 0 | 1 · 8a0912785 2026-08-13 | — | — |
| [#342] | [E6] Cross-repo universalization | fleet_parity gate-ahead max-fidelity hardening | **git silent** | 0 | 0 | — | — |
| [#343] | [E6] Cross-repo universalization | fleet_parity ship-gate-only scoping | **git silent** | 0 | 0 | — | — |
| [#344] | [E1] Handoff continuity | Session-close gate for handoff generation + consumer hub-wr… | **git silent** | 0 | 2 · 8a0912785 2026-08-13 | — | — |
| [#345] | [E2] Enforced governance | Externalize the ADR-101 frozensets → machine-readable path-… | 2026-08-18 | 1 | 0 | — | — |
| [#346] | [E2] Enforced governance | Persist the two-tier new-path executor rule into `~/.claude` | **git silent** | 0 | 1 · 8a0912785 2026-08-13 | — | — |
| [#347] | [E7] Tooling & evaluation | Formalize the engineering loop/harness end-to-end + sanctio… | **git silent** | 0 | 1 · 8a0912785 2026-08-13 | — | — |
| [#348] | [E7] Tooling & evaluation | Backlog grooming as a standing routine, not ad-hoc | **git silent** | 0 | 1 · 054502455 2026-08-05 | — | — |
| [#349] | [E2] Enforced governance | Mechanize session-discipline inheritance | **git silent** | 0 | 1 · 8a0912785 2026-08-13 | — | — |
| [#350] | [E1] Handoff continuity | Handoff-process refinements | 2026-08-16 | 2 | 1 · 8e8d55a2e 2026-08-16 | — | — |
| [#351] | [E6] Cross-repo universalization | Fleet-Python-upgrade ticket | 2026-08-16 | 2 | 1 · 4ca67eed8 2026-08-16 | — | — |
| [#353] | [E2] Enforced governance | Session-boot contract hardening | **git silent** | 0 | 1 · 8a0912785 2026-08-13 | — | — |
| [#354] | [E8] ARC-5 execution | W6 seed-1 recurrence half | **git silent** | 0 | 0 | — | — |
| [#356] | [E8] ARC-5 execution | RULING-W and the merge-delegation composite are LEGIBLE but… | **git silent** | 0 | 2 · 8a0912785 2026-08-13 | — | — |
| [#357] | [E8] ARC-5 execution | Silent-rule census run 2 | 2026-08-16 | 3 | 1 · 8a0912785 2026-08-13 | — | — |
| [#358] | [E8] ARC-5 execution | `ecosystem/parity-surfaces.yaml` misdescribes its own enfor… | 2026-08-14 | 2 | 1 · 8a0912785 2026-08-13 | — | — |
| [#359] | [E8] ARC-5 execution | PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md` §14a F… | 2026-08-12 | 2 | 0 | — | — |
| [#361] | [E8] ARC-5 execution | ADR-immutability's real coverage is declared only in code, … | 2026-08-13 | 4 | 1 · 40dd51d8f 2026-08-16 | — | — |
| [#362] | [E8] ARC-5 execution | #242 carries a SUBSTANTIVE guard loss, not status hygiene | **git silent** | 0 | 1 · 8a0912785 2026-08-13 | — | — |
| [#365] | [E8] ARC-5 execution | Promote `residual_completeness` from `exempt:` to `coverage… | 2026-08-08 | 1 | 0 | — | — |
| [#366] | [E8] ARC-5 execution | `residual_completeness` scans the WORKING TREE, not the sta… | **git silent** | 0 | 1 · 8a0912785 2026-08-13 | — | — |
| [#369] | [E8] ARC-5 execution | Wire `boundary_headers.py --check` into pre-commit | 2026-08-16 | 2 | 1 · 0e5d015b4 2026-07-20 | — | — |
| [#371] | [E8] ARC-5 execution | Consumer editor-config write-through — declared at v1.4.0, … | 2026-08-16 | 3 | 2 · 8a0912785 2026-08-13 | — | — |
| [#383] | [E9] Fleet Desired-State System (… | Execution waves per surface | 2026-08-07 | 2 | 2 · 42ff1323c 2026-08-03 | — | — |
| [#385] | [E9] Fleet Desired-State System (… | L4 tech-currency lane | 2026-07-21 | 1 | 1 · 4ca67eed8 2026-08-16 | — | — |
| [#387] | [E7] Tooling & evaluation | Rewrite the buy-vs-build intake BEFORE anything ingests it | 2026-07-22 | 1 | 1 · 5eb1269f5 2026-08-13 | — | — |
| [#388] | [E5] Canonical-file integrity | The \"10–20 repo\" fleet-scale target is FABRICATED — corre… | 2026-07-21 | 1 | 0 | — | — |
| [#389] | [E2] Enforced governance | Prompt-lint — gate the five architect fields before a lane … | 2026-08-16 | 1 | 2 · 5eb1269f5 2026-08-13 | — | — |
| [#390] | [E1] Handoff continuity | Resolve the ADR-87 effort-ownership contradiction, then tru… | 2026-08-11 | 1 | 2 · bbacd6c03 2026-08-11 | — | — |
| [#391] | [E9] Fleet Desired-State System (… | Wire fleet_analytics into a nightly lane, or narrow #384 to… | 2026-08-08 | 1 | 2 · 9997bc324 2026-08-16 | — | — |
| [#392] | [E9] Fleet Desired-State System (… | fleet_analytics rename-alias loses history on path-reuse | **git silent** | 0 | 0 | — | — |
| [#393] | [E9] Fleet Desired-State System (… | corp-sca rot review — confirm-live-or-retire 3 candidates | **git silent** | 0 | 2 · 4ca67eed8 2026-08-16 | — | — |
| [#397] | [E7] Tooling & evaluation | scripts/ target structure — rule on the mapped grouping, th… | **git silent** | 0 | 0 | — | — |
| [#399] | [E8] ARC-5 execution | `templates/handoff/v5/README.md.tmpl` — phantom source clai… | 2026-08-16 | 4 | 1 · 5eb1269f5 2026-08-13 | — | — |
| [#400] | [E8] ARC-5 execution | Ownership-model: the hub-mandated-STRUCTURE / repo-owned-CO… | **git silent** | 0 | 1 · 624b0485f 2026-07-23 | — | — |
| [#401] | [E2] Enforced governance | ai-council routing still ARMED at the deleted hub landing z… | 2026-08-13 | 1 | 4 · 19cf25dcb 2026-07-25 | — | — |
| [#402] | [E8] ARC-5 execution | Intake naming clause — DEPLOY the `YYYY-MM-DD-<class>-<slug… | **git silent** | 0 | 1 · fb868199f 2026-07-23 | — | — |
| [#403] | [E7] Tooling & evaluation | Extend `doc_claims` to ARCHITECTURE's machine-derivable cla… | **git silent** | 0 | 2 · 44e47b48f 2026-07-23 | — | — |
| [#404] | [E1] Handoff continuity | gen_handoff execution-mode SUPPLEMENT leak (mode-blind fram… | **git silent** | 0 | 1 · de402b1ce 2026-07-23 | — | — |
| [#405] | [E2] Enforced governance | Session-end leftover check — nothing verifies \"no leftover… | **git silent** | 0 | 2 · f3ead30b6 2026-07-23 | — | — |
| [#406] | [E2] Enforced governance | Commit-time doc_rot surfacing — an over-threshold BACKLOG t… | **git silent** | 0 | 1 · 023520f0e 2026-07-24 | — | — |
| [#407] | [E6] Cross-repo universalization | Universal fleet Python style — functional-vs-OOP stance + u… | **git silent** | 0 | 0 | — | — |
| [#408] | [E2] Enforced governance | Auto-coupled doc updates — closing a backlog item must mech… | 2026-08-18 | 4 | 2 · 5eb1269f5 2026-08-13 | — | — |
| [#409] | [E7] Tooling & evaluation | Standing night batch — CODE review (formalize as routine) | 2026-08-16 | 2 | 1 · 51d7fa081 2026-08-16 | — | — |
| [#410] | [E7] Tooling & evaluation | Standing night batch — ARCHITECTURE review (formalize as ro… | 2026-08-16 | 1 | 1 · 51d7fa081 2026-08-16 | — | — |
| [#411] | [E7] Tooling & evaluation | Standing night batch — creative session, and the recurring … | 2026-08-16 | 1 | 1 · 51d7fa081 2026-08-16 | — | — |
| [#412] | [E7] Tooling & evaluation | Subagent / workflow routing + configured fan-out + online r… | 2026-08-16 | 2 | 1 · 9997bc324 2026-08-16 | — | — |
| [#413] | [E8] ARC-5 execution | Colors semantics — visually distinguish global/hub-managed … | 2026-08-08 | 1 | 1 · 5eb1269f5 2026-08-13 | — | — |
| [#414] | [E2] Enforced governance | Self-acting-on-main incident family — a session changed `ma… | 2026-08-16 | 1 | 2 · 5eb1269f5 2026-08-13 | — | — |
| [#415] | [E7] Tooling & evaluation | Tests must bind fixtures, not live mutable repo content (he… | 2026-08-18 | 2 | 2 · 5eb1269f5 2026-08-13 | — | — |
| [#417] | [E2] Enforced governance | `check_dirty_tree` runs with no pathspec, so the Stop gate … | 2026-08-18 | 2 | 1 · 8e8d55a2e 2026-08-16 | — | — |
| [#418] | [E2] Enforced governance | `automation/fleet-audit` records 0–10 baselines a day, not … | 2026-08-16 | 1 | 1 · 5eb1269f5 2026-08-13 | — | — |
| [#419] | [E7] Tooling & evaluation | We run routines whose output nobody consumes | **git silent** | 0 | 4 · 51d7fa081 2026-08-16 | — | — |
| [#420] | [E5] Canonical-file integrity | Does a TOP-LEVEL `docs/archive/` still make sense? | 2026-08-18 | 5 | 0 | — | — |
| [#422] | [E1] Handoff continuity | `reflow_framing`'s cold→FILLED flip is partial by design, a… | **git silent** | 0 | 2 · c74f918ce 2026-07-26 | — | — |
| [#423] | [E2] Enforced governance | The integration sequence runs on prose every time, never me… | 2026-08-16 | 2 | 2 · 5eb1269f5 2026-08-13 | — | — |
| [#424] | [E2] Enforced governance | Backlog `depends-on` gates are INERT — `_DEPID_RE` requires… | 2026-07-29 | 1 | 1 · 42ff1323c 2026-08-03 | — | — |
| [#425] | [E2] Enforced governance | The suite is green on a format the file does not use | 2026-08-16 | 3 | 1 · 781bd4ff9 2026-08-13 | — | — |
| [#426] | [E7] Tooling & evaluation | Declare `consumer` + `consumption_path` for every LIVE rout… | 2026-08-16 | 1 | 3 · bbacd6c03 2026-08-11 | — | — |
| [#427] | [E8] ARC-5 execution | Region templates carry a repo-POSITION-DEPENDENT path | 2026-08-11 | 3 | 1 · 863cb804b 2026-07-26 | — | — |
| [#428] | [E7] Tooling & evaluation | `nightly-triage` reports a dead producer to every session s… | 2026-08-07 | 2 | 4 · b150bfe41 2026-08-16 | — | — |
| [#430] | [E6] Cross-repo universalization | Consumer template rejects root `conftest.py`; `fleet_parity… | 2026-08-07 | 1 | 5 · 781bd4ff9 2026-08-13 | — | — |
| [#431] | [E7] Tooling & evaluation | `codex-review` silently drops the doc lane on any mixed diff | **git silent** | 0 | 2 · feb95e184 2026-07-27 | — | — |
| [#438] | [E3] Lessons feedback loop | Codify gate-class posture: terra design review BEFORE build… | 2026-08-18 | 2 | 2 · b4862b9be 2026-08-16 | — | — |
| [#440] | [E7] Tooling & evaluation | Make the `tasks/` id ledger tamper-evident — a deleted reti… | 2026-08-18 | 1 | 0 | — | — |
| [#442] | [E2] Enforced governance | Plugin command-cache staleness — cached command text can si… | 2026-08-18 | 1 | 1 · 952c10ade 2026-07-28 | — | — |
| [#443] | [E3] Lessons feedback loop | Planning artifacts outside the three enforced classes carry… | 2026-08-17 | 4 | 2 · b4862b9be 2026-08-16 | — | — |
| [#445] | [E7] Tooling & evaluation | `codex-review` wrapper path-guard reports SUCCESS having re… | 2026-07-29 | 2 | 0 | — | — |
| [#447] | [E1] Handoff continuity | Self-referential gate family — the committing act cannot sa… | 2026-08-16 | 3 | 1 · ebda157e0 2026-07-29 | — | — |
| [#448] | [E8] ARC-5 execution | A11 staged-diff guard — cover EVERY candidate bundle, not j… | **git silent** | 0 | 1 · 3f4a1819b 2026-07-30 | — | — |
| [#449] | [E1] Handoff continuity | Assembled-paste byte budget — should `PASTE_THIS.md` gain a… | **git silent** | 0 | 1 · 65a549bf9 2026-07-30 | — | — |
| [#450] | [E4] Decision management | Per-section intake ratification — the `status:` field is do… | **git silent** | 0 | 0 | — | — |
| [#451] | [E2] Enforced governance | CA layer-edge check — port the ai-council layer-edge review… | **git silent** | 0 | 0 | — | — |
| [#453] | [E7] Tooling & evaluation | Cloud night-run runbook — the container gaps that silently … | 2026-08-16 | 3 | 1 · 781bd4ff9 2026-08-13 | — | — |
| [#454] | [E2] Enforced governance | `closure_ids` negation defect — the parser reads a negated … | 2026-07-29 | 1 | 0 | — | — |
| [#456] | [E4] Decision management | Ruling-blocked cohort sweep — re-route the remaining Done-w… | 2026-08-16 | 1 | 1 · 781bd4ff9 2026-08-13 | — | — |
| [#457] | [E2] Enforced governance | Two live-repo tests fail on main against green gates — test… | **git silent** | 0 | 3 · 054502455 2026-08-05 | — | — |
| [#463] | [E7] Tooling & evaluation | win-tooling onboarding debt — 2 FAILs + 2 WARNs unchanged s… | 2026-08-16 | 2 | 2 · 781bd4ff9 2026-08-13 | — | — |
| [#464] | [E7] Tooling & evaluation | corp-*/ai-council governance drift — five findings live 15–… | 2026-08-16 | 1 | 2 · 781bd4ff9 2026-08-13 | — | — |
| [#470] | [E7] Tooling & evaluation | `audit.py checks` crashes mid-listing on a cp1252 console —… | **git silent** | 0 | 1 · b0af8e92e 2026-08-01 | — | — |
| [#477] | [E2] Enforced governance | `deployed_methodology_version` keys the registry by repo-ro… | 2026-07-21 | 1 | 1 · 0c64a76a5 2026-08-03 | — | — |
| [#478] | [E2] Enforced governance | `changelog_sentinel` drops PEP 440 suffixes — a prerelease … | **git silent** | 0 | 0 | — | — |
| [#484] | [E2] Enforced governance | ADR-106 system-Python divergence — named deferral, not an o… | 2026-08-16 | 2 | 1 · 4ca67eed8 2026-08-16 | — | — |
| [#485] | [E2] Enforced governance | A shared LF-enforcing write helper — the mechanism that rep… | 2026-08-18 | 2 | 0 | — | — |
| [#486] | [E7] Tooling & evaluation | `desired_state_report.py` dies on a cp1252 console — U+21C4… | **git silent** | 0 | 0 | — | — |
| [#487] | [E7] Tooling & evaluation | Closure-proposal consumption arc — repair the pipeline first | 2026-08-18 | 3 | 1 · 781bd4ff9 2026-08-13 | — | — |
| [#488] | [E7] Tooling & evaluation | Priority axis — the backlog has no ranking function beyond … | **git silent** | 0 | 0 | — | — |
| [#491] | [E7] Tooling & evaluation | Gemini scanning lane — ruling R-G plus an acceptance contra… | 2026-08-18 | 2 | 2 · 9997bc324 2026-08-16 | — | — |
| [#493] | [E7] Tooling & evaluation | B-2 investigation — the scheduled fleet-baseline task has b… | 2026-08-18 | 1 | 1 · 781bd4ff9 2026-08-13 | — | — |
| [#494] | [E7] Tooling & evaluation | Ladder ratification — L0–L5 promote-vs-leave is unruled, an… | **git silent** | 0 | 0 | — | — |
| [#496] | [E2] Enforced governance | `_ORGAN_TO_COMPONENT` attributes the pre-push organ to a co… | **git silent** | 0 | 0 | — | — |
| [#497] | [E2] Enforced governance | Two stale claims on carrier/hook declarations | 2026-08-16 | 2 | 0 | — | — |
| [#500] | [E2] Enforced governance | The Stop hook's BACKLOG advisory reads a correctly-closed t… | 2026-08-18 | 1 | 2 · 054502455 2026-08-05 | — | — |
| [#502] | [E7] Tooling & evaluation | mutmut 3.7.0 mutation-testing evaluation — CI-hosted | 2026-08-11 | 2 | 7 · 4ca67eed8 2026-08-16 | — | `worktree-lane-e-502-mutmut`, `origin/worktree-lane-e-502-mutmut` |
| [#505] | [E3] Lessons feedback loop | Batch-protocol encoding — the parallel-execution way-of-wor… | 2026-08-16 | 1 | 12 · bbacd6c03 2026-08-11 | 25ff8ec37 | — |
| [#506] | [E5] Canonical-file integrity | Whole-set P10 grooming arc — the open set is unreconciled | 2026-08-18 | 4 | 4 · 781bd4ff9 2026-08-13 | — | — |
| [#507] | [E2] Enforced governance | Report-only wall — decide the fourth recorded leg (`pre-com… | 2026-08-14 | 3 | 1 · 945598f99 2026-08-07 | — | — |
| [#509] | [E7] Tooling & evaluation | `Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR` | 2026-08-16 | 2 | 0 | — | — |
| [#510] | [E2] Enforced governance | Scope the R-1 exemption to the lanes its manifest enumerate… | 2026-08-14 | 2 | 1 · 0136cec6a 2026-08-11 | — | — |
| [#511] | [E1] Handoff continuity | The 30-minute handoff cut is ~99.8% session authoring, not … | 2026-08-16 | 4 | 4 · 781bd4ff9 2026-08-13 | — | — |
| [#514] | [E2] Enforced governance | Two rival `LANE_BRANCH_RE` constants ship in one repo | **git silent** | 0 | 1 · 0136cec6a 2026-08-11 | — | — |
| [#518] | [E2] Enforced governance | `scripts/audit.py::_git` — one call site, two REPRODUCED de… | **git silent** | 0 | 0 | — | — |
| [#519] | [E2] Enforced governance | The close path is two edits, and nothing makes a half-done … | 2026-08-18 | 1 | 1 · 78ab77b45 2026-08-09 | — | — |
| [#520] | [E2] Enforced governance | No sanctioned way to retire a committed bundle whose seal i… | 2026-08-17 | 2 | 1 · 78ab77b45 2026-08-09 | — | — |
| [#522] | [E2] Enforced governance | A re-cut handoff sibling carries its predecessor's payloads… | 2026-08-07 | 1 | 1 · 3b711e87b 2026-08-11 | — | — |
| [#523] | [E7] Tooling & evaluation | Executive-index render leg on the generated `BACKLOG.md` | 2026-08-18 | 1 | 0 | — | — |
| [#526] | [E5] Canonical-file integrity | Root-hygiene audit — which root files MUST be root, which a… | 2026-08-18 | 7 | 0 | — | — |
| [#528] | [E7] Tooling & evaluation | Lane-latency — the full suite multiplied by per-lane + per-… | 2026-08-11 | 1 | 0 | — | — |
| [#529] | [E7] Tooling & evaluation | Telemetry v1 EMIT — stage-1 events from the gate mesh | 2026-08-17 | 3 | 0 | — | — |
| [#530] | [E2] Enforced governance | Single-flight dispatch guard — one contract execution at a … | 2026-08-16 | 1 | 0 | — | — |
| [#531] | [E2] Enforced governance | Lane-grammar enforcement at PROVISIONING — the enum is chec… | 2026-08-16 | 2 | 0 | — | — |
| [#533] | [E2] Enforced governance | Decompose the `audit.py` check monolith into `scripts/audit… | 2026-08-16 | 5 | 3 · e32093fd8 2026-08-16 | — | `worktree-lane-a-533-leg2` |
| [#534] | [E2] Enforced governance | `scripts/audit.py:<line>` locators on four open rows died a… | 2026-08-18 | 2 | 0 | — | — |
| [#535] | [E7] Tooling & evaluation | `audit.py` has two module identities in one process, and a … | **git silent** | 0 | 0 | — | — |
| [#536] | [E2] Enforced governance | The ARM-2 row-length pile has no owner, and the conversion … | **git silent** | 0 | 0 | — | — |
| [#537] | [E7] Tooling & evaluation | `disposition token` is a Done-when branch nothing defines | **git silent** | 0 | 0 | — | — |
| [#538] | [E3] Lessons feedback loop | The NB4-C PLAYBOOK gap arc — twelve paste-ready acts, none … | 2026-08-16 | 1 | 0 | — | — |
| [#539] | [E7] Tooling & evaluation | `gen_lane_contract.py` — assembly-not-generation, with a `-… | 2026-08-18 | 3 | 0 | — | — |
| [#540] | [E7] Tooling & evaluation | `harvest_batch.py` — read the board, then fetch packets by … | **git silent** | 0 | 0 | — | — |
| [#541] | [E7] Tooling & evaluation | Scale-out substrate decision — unowned after two reports an… | 2026-08-18 | 1 | 0 | — | — |
| [#542] | [E5] Canonical-file integrity | `ARCHITECTURE.md` still claims four `doc_rot` sub-detectors… | 2026-08-14 | 2 | 0 | — | — |
| [#546] | [E4] Decision management | ADR-60's `docs/` taxonomy no longer describes the tree it g… | 2026-08-18 | 4 | 0 | — | — |
| [#547] | [E1] Handoff continuity | Split-brain prevention is instructed against a handoff sect… | 2026-08-16 | 5 | 0 | — | — |
| [#548] | [E4] Decision management | Intake #12's SETTLED ownership manifest is parked on a depa… | 2026-08-18 | 3 | 0 | — | — |
| [#549] | [E4] Decision management | The operator-approved Fleet-Hygiene plan-of-record (intake … | 2026-07-23 | 1 | 0 | — | — |
| [#550] | [E4] Decision management | Intake #14's ruled SIEM requirements outlived the ruling th… | 2026-08-18 | 2 | 0 | — | — |
| [#551] | [E5] Canonical-file integrity | Audit artifacts carry no `status:`, so a consumed audit is … | 2026-08-18 | 2 | 0 | — | — |
| [#552] | [E2] Enforced governance | Window-close disposition + archival routine — every new aud… | 2026-08-16 | 2 | 0 | — | — |
| [#553] | [E5] Canonical-file integrity | `docs/decisions/README.md`'s ADR census is hand-maintained,… | 2026-08-18 | 3 | 0 | — | — |
| [#554] | [E7] Tooling & evaluation | Devcontainer + provisioning script (NB4-G stage 1) | 2026-08-17 | 1 | 1 · 409374fd1 2026-08-18 | — | `worktree-lane-c-554-devcontainer` |
| [#555] | [E7] Tooling & evaluation | Closing campaign batch 1 + kill-candidates instrument | 2026-08-17 | 1 | 1 · 409374fd1 2026-08-18 | — | — |
| [#556] | [E2] Enforced governance | `[#505]` is closed-but-present — the ADR-65 done-items-leav… | 2026-08-18 | 2 | 0 | — | — |
| [#557] | [E2] Enforced governance | Three `[stale]` dispositions match no live WARN — the ADR-7… | 2026-08-16 | 1 | 0 | — | — |
| [#558] | [E5] Canonical-file integrity | `VISION.md` still describes `scripts/` as read-only validat… | 2026-08-16 | 4 | 0 | — | `worktree-lane-d-558-vision` |

## §6 · The inline helper, in full

The contract is library-first: **no new scripts committed.** The helper below ran once from the job
scratch dir, wrote nothing, and was never added to the tree. It is recorded here verbatim so the
sheet is reproducible from this artifact alone — paste it to a scratch path and run
`py <path> "$(pwd)" main`.

```python
#!/usr/bin/env python
"""derive_p10.py — INLINE helper for the P10 grooming evidence sheet.

Read-only. Never committed (lane contract STEP 1: "library-first: no new scripts
committed — if a helper is needed, it runs inline and its full text is recorded in
the artifact"). Emits the evidence table to stdout; writes nothing.

Usage:  py derive_p10.py <repo-root> <ref>
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = sys.argv[2] if len(sys.argv) > 2 else "main"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout


# ---------------------------------------------------------------- tracked tree
tracked = set(git("ls-files").splitlines())
tracked_dirs: set[str] = set()
for p in tracked:
    parts = p.split("/")
    for i in range(1, len(parts)):
        tracked_dirs.add("/".join(parts[:i]))

# ------------------------------------------- path -> newest commit date (%cs)
# git log is reverse-chronological, so the FIRST date seen for a path is newest.
newest: dict[str, str] = {}
cur = None
for line in git("log", REF, "--format=\x01%cs", "--name-only").splitlines():
    if line.startswith("\x01"):
        cur = line[1:]
    elif line.strip() and cur:
        newest.setdefault(line.strip(), cur)


def dir_newest(d: str) -> str | None:
    hits = [v for k, v in newest.items() if k.startswith(d + "/")]
    return max(hits) if hits else None


# ------------------------------------------ first-parent merges on <ref>
merges = []  # (sha, date, subject)
for line in git("log", REF, "--first-parent", "--merges",
                "--format=%H\x01%cs\x01%s").splitlines():
    if line.count("\x01") >= 2:
        sha, date, subj = line.split("\x01", 2)
        merges.append((sha, date, subj))

# ------------------------------------------------- validator closures (STRONG)
sys.path.insert(0, str(ROOT / "scripts"))
from validate_git_backlog import reconcile  # noqa: E402

drift = reconcile(ROOT, ROOT / "BACKLOG.md")   # {id: [(sha, subject), ...]}

# ------------------------------------------------------------------ open rows
FM = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
TOKEN = re.compile(r"`([^`]+)`")

rows = []
for f in sorted((ROOT / "tasks").glob("*.md")):
    m = FM.match(f.read_text(encoding="utf-8", errors="replace"))
    if not m:
        continue
    fm, body = m.group(1), m.group(2)

    def field(name: str) -> str:
        mm = re.search(rf"^{name}:\s*(.*)$", fm, re.M)
        return mm.group(1).strip().strip('"') if mm else ""

    if field("status") != "open":
        continue
    tid = field("id").strip("[]#")

    # paths the row NAMES = backticked tokens that resolve against the tracked tree
    resolved: set[str] = set()
    for tok in TOKEN.findall(body):
        tok = tok.split()[0] if tok.split() else ""
        tok = tok.strip().rstrip(",.;:)").rstrip("/")
        if not tok or tok.startswith(("http", "#", "[")):
            continue
        if tok in tracked or tok in tracked_dirs:
            resolved.add(tok)

    touches = []
    for p in resolved:
        d = newest.get(p) or dir_newest(p)
        if d:
            touches.append(d)
    last_touch = max(touches) if touches else None

    mentions = [(s, d, subj) for s, d, subj in merges if f"[#{tid}]" in subj]

    closure = ""
    if tid in drift:
        closure = "; ".join(f"{sha[:9]}" for sha, _ in drift[tid])

    brefs = [b.strip() for b in git("branch", "-a", "--format=%(refname:short)").splitlines()
             if re.search(rf"(?<!\d){tid}(?!\d)", b)]

    rows.append({
        "id": tid, "theme": field("theme"), "title": field("title"),
        "priority": field("priority"), "size": field("size"),
        "last_touch": last_touch, "n": len(resolved),
        "mentions": mentions, "closure": closure, "brefs": brefs,
    })

rows.sort(key=lambda r: int(r["id"]))


def cell(s: str) -> str:
    return s.replace("|", "\\|")


def trunc(s: str, n: int = 60) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"


print("| id | theme | title | last touch | n | merge mentions | closure (authoritative) | branch refs |")
print("|---|---|---|---|---|---|---|---|")
for r in rows:
    lt = r["last_touch"] or "**git silent**"
    if r["mentions"]:
        s, d, _ = r["mentions"][0]           # first-parent log is newest-first
        mm = f"{len(r['mentions'])} · {s[:9]} {d}"
    else:
        mm = "0"
    cl = r["closure"] or "—"
    br = ", ".join(f"`{b}`" for b in r["brefs"]) or "—"
    print(f"| [#{r['id']}] | {cell(trunc(r['theme'], 34))} | {cell(trunc(r['title']))} "
          f"| {lt} | {r['n']} | {mm} | {cl} | {br} |")

print()
print("SUMMARY")
print(f"  open rows           : {len(rows)}")
print(f"  git silent (n == 0) : {sum(1 for r in rows if r['n'] == 0)}")
print(f"  >=1 merge mention   : {sum(1 for r in rows if r['mentions'])}")
print(f"  validator closures  : {sum(1 for r in rows if r['closure'])}")
print(f"  branch refs         : {sum(1 for r in rows if r['brefs'])}")
print(f"  HEAD                : {git('rev-parse', 'HEAD').strip()}")
print(f"  ref scanned         : {REF} = {git('rev-parse', REF).strip()}")
print(f"  first-parent merges : {len(merges)}")
print(f"  drift ids           : {sorted(drift, key=int)}")
```

## §7 · Honest limits of this sheet

Stated so a downstream reader does not over-trust a column:

1. **Path resolution is backtick-scoped.** A row that names a path in bare prose resolves nothing
   and reads as `git silent`. This is deliberate — a prose scan would resolve English words as
   paths — but it means `n` is a floor, never a ceiling.
2. **`last touch` measures the path, not the row.** A row naming `scripts/audit.py` inherits the
   date of the *last commit to that file by anyone*, which is usually another row's work. High
   traffic on a shared file is not evidence that this row moved.
3. **Merge mentions count the subject only.** An arc that advanced a row without naming it in the
   merge subject — or that named it only in the body — counts 0 here.
4. **The closure column inherits `validate_git_backlog`'s predicate**, including its quoted-context
   stripping and its keyword regex. §2 records the one live match's exact text for that reason.
5. **Branch refs are name-matched.** A branch that works a row without carrying its number in the
   name is invisible; the four hits are the four live lane worktrees at this SHA.
6. **Nothing here is a liveness verdict.** No row was ranked, scored, proposed for closure, or
   marked dead. That is the next act, and it is the architect's.

---

**Lane footprint:** this file, the contract-of-record
`docs/audits/2026-08-18-technical-p10-regen-lane-contract.md` (commit `356232ae`), and the
`audit-index-freshness`-mandated regeneration of `docs/audits/README.md`. Zero rows born, zero rows
edited, zero registers touched, zero scripts added, nothing merged, nothing pushed.
