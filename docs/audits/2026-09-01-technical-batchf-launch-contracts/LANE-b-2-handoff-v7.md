# LANE lane-b-2-handoff-v7 — HANDOFF v7 as the BOOT-INVERSION carrier -- a generated-from-live-state bundle plus the /boot-session organ and its SessionStart digest, so a fresh seat can rule what-next from the output alone

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

**No-consumer:** a frozen lane contract is consumed by its DISPATCH and by the batch manifest that enumerates its slug, never by a governance-surface citation — and its filename carries no `YYYY-MM-DD` prefix, so neither `consumer_at_landing` token regex could resolve a citation even if one existed. Declared per that check's own escape.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-b-2-handoff-v7 LANE-b-2-handoff-v7.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-b-2-handoff-v7 · lane-b-2-handoff-v7]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-b-2-handoff-v7` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-b-2-handoff-v7` -> branch `worktree-lane-b-2-handoff-v7` -> contract `LANE-b-2-handoff-v7.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

- `protocols/HANDOFF_PROCESS.md`
- `protocols/HANDOFF_BOOT.md`
- `scripts/assemble_paste.py`
- `tests/test_assemble_paste.py`
- `scripts/boot_frontier.py`
- `tests/test_boot_frontier.py`
- `.claude/commands/boot-session.md`
- `.claude/commands/handoff.md`
- `.claude/commands/handoff-verify.md`
- `.claude/settings.json`
- `scripts/fleet_health.py`
- `tests/test_fleet_health.py`
- `deploy/manifest-v1.5.0.yaml`

`scripts/funnel_lifecycle.py` is READ, never written — it already exposes `measure()` and
`findings()`, which are the rot/orphan source. `deploy/manifest-v1.5.0.yaml` is in THIS lane's
scope rather than lane-e-5's: two new deploy-carried organs must be declared somewhere, and one
file needs one owner. While in it, this lane also corrects the stale archival note still
recording VISION's archival as *"MEASURED AND BLOCKED"* on a `vision_md` FAIL that stopped
existing on 2026-09-01.

## Done-contract (immutable)

1. **The bundle's sections are GENERATED FROM LIVE STATE, not hand-copied** — FUNNEL HEALTH;
   north-star arcs with priorities; the rot/orphan list from `funnel_lifecycle`; open asks for
   the browser; and a **PROPOSED NEXT BATCH** of decision-tree-ranked leaves, ledger-bounded.
   Exactly ONE small hand-written **RESIDUAL** carries the judgment a generator cannot have:
   rejections, tensions, and why. **`HANDOFF_PROCESS` is at v7.0.0, ROLE PIN 7.0.0, and a v6
   bundle is REFUSED** — refused, not warned, or the inversion is optional and therefore absent.
2. **TWO ORGANS, AND THE HARD PART IS A LIBRARY, NOT A SKILL.** (a)
   `.claude/commands/boot-session.md`, repo-level and deploy-carried like any organ, assembles
   the sections and emits a browser-paste block. (b) A SessionStart **one-line FUNNEL HEALTH
   digest** — rot / orphans / unblocked / proposed batch. **The deterministic part is a
   library**: the unblocked frontier by `rustworkx` topological order, the scoring, and batch
   selection under disjointness, width and the ledger bound all live in importable, testable
   code. **The command NARRATES and names the questions; it does not compute.** A prompt that
   computes a frontier is a frontier nobody can test.
3. **EXTEND THE EXISTING TRIPWIRES — NEVER A FIFTH RIVAL.** `SessionStart` already runs four
   surfacing organs plus `arm_hooks`. `scripts/fleet_health.py` is the measured natural host: it
   already prints a one-line digest and already carries the overdue-groom escalation. Confirm
   against live docs and extend; a rival hook printing a competing summary is the failure this
   item names.
4. **NO NEW DEPENDENCY. `rustworkx` IS ALREADY DECLARED** — `pyproject.toml` carries it for
   FPG-1 (`scripts/file_purpose_graph.py`) on the operator's A3 mandate, resolved from a
   prebuilt wheel and hash-pinned in `uv.lock`, with its numpy transitive cost already stated
   there. This lane REUSES it and follows FPG-1's precedent; adding a graph library would be a
   gated change this contract does not authorise.
5. **THE SCORING RULE IS A DECLARED SEAM, PINNED LATER — NOT INVENTED HERE.** BOOT-R1's survey
   is still RUNNING. This lane lands the STRUCTURE with the scoring model behind a named,
   swappable interface and a documented placeholder; the rule is pinned when that artifact
   returns. **A scoring model invented to fill a gap is the thing the survey exists to prevent.**
6. **The bounding rules come from AUT-R1's self-planning axis**
   (`docs/audits/2026-08-29-technical-aut-r1-autonomous-sdlc-orchestration.md`): never endless,
   never only-easy, and human approval represented explicitly as a **GO**. Cite it; do not
   re-derive it.
7. **The prefix-first naming convention is FILED AS A CANDIDATE, and nothing is renamed here.**
   `boot-session` / `boot-lane` / `boot-batch` goes to the commands+skills census as an ADR-111
   CANDIDATE — not a row birth. **`/lane-boot` is renamed THERE, with an alias, not in this lane.**
8. **The four stale VISION pointers in this lane's own files are re-pointed to `README.md`'s
   `## Vision`** — `HANDOFF_PROCESS.md:535` and `:960`, `HANDOFF_BOOT.md:116`,
   `.claude/commands/handoff.md:111`, `handoff-verify.md:99`. They are stale TODAY, independently
   of `[#621]`.
9. **The budget is measured, not hoped.** An assembled paste from a REAL cut measures
   **<=20 KB at >=70% window-specific content**, recorded. `HANDOFF_BOOT.md` stays under its
   18,000 B budget — **17,196 B today, 804 B of headroom**, and the ROLE PIN change spends from
   it. If v7 will not fit, that is a finding to REPORT, never a budget to quietly raise.
10. **EX-ANTE, and this is the acceptance test:** a fresh seat runs `/boot-session` and can rule
   *what next* from its output alone; the digest fires on every session start **in the hub AND
   in a deployed consumer**. Proven by re-running `reconciled_versions`, `silent_rule_ratchet`
   and `verify_handoff_probes`.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. `/preflight` `[#611]`'s Done-when, AUT-R1's self-planning axis, and the live command/hook
   syntax in the current docs. Derive the syntax; do not recall it. **COMMIT**
2. Build `scripts/boot_frontier.py` FIRST — frontier, scoring seam, batch selection — with its
   tests. The library before the narration, so the hard part is testable. **COMMIT**
3. Land `.claude/commands/boot-session.md` over that library, and extend the existing tripwire
   with the one-line digest. **COMMIT**
4. Take `HANDOFF_PROCESS` to v7.0.0, re-point the four stale VISION citations, and declare both
   organs in the deploy manifest (correcting its stale VISION archival note in the same pass).
   **COMMIT**
5. Cut a REAL paste and MEASURE it — size and window-specific ratio, both recorded. File the
   naming convention as a CANDIDATE. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
