> **PROVENANCE - harvested cloud artifact, body VERBATIM below this header.**
> Lane `batch-e-a5-harness-portability-map` | receipt id `cse_018bwHzUJuxV4pCEd59jf3TS` | dispatched 2026-08-31, harvested 2026-08-31 by
> `Save-CloudSessionReport` (the `Harvest-Cloud` alias). Batch E tier (A); the frozen contract is
> `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a5-harness-portability-map.md`.
> Selection rule: the LONGEST assistant text, not the last - text #3 of 12 across 4 pages.
> Bytes written unchanged: **12,493**.
> Harvester DEVIATION, recorded not repaired: the report does not open with its own heading -- the first heading is line 8; bytes UNCHANGED.
> Nothing below this line was edited, reflowed or trimmed.
>
> **Consumed by:** the AUTONOMY arc's decision tree (leaf: the harness-portability map, routed `not-a-candidate`).
>
> **This lane was READ-ONLY by contract** - zero tree writes, zero commits, zero rows, no gate
> run and none asserted.

---

Reconciliation done, draft below. Read: the AUT-R4-A audit Part 1, the decision-tree leaf, `AGENTS.md`, ADR-115 (incl. the 2026-08-27 amendment), ADR-101 §1, `ecosystem/provider-registry.yaml` header + provider block, `ecosystem/substrate-registry.yaml`, `deploy/global-instructions-codex.md`, PLAYBOOK Ch2 (:318–:390), Ch8 (:2538–:2600, :1440–:1470), `scripts/gen_lane_contract.py`, `scripts/validate_branch_naming.py`.

**Reconciliation verdict (done-item 3):** the doctrine exists for **exactly one organ** and for no other. ADR-115 §3.2/§3.3 and PLAYBOOK `:323` already rule the *instruction-file* split — the draft points at them and restates nothing. No surface anywhere states the boundary rule for the other five organs, and `provider-registry.yaml`'s own header scopes itself to model **identity**, not harness coupling, while `substrate-registry.yaml` declares "*carries no doctrine*". That is the hole the section fills.

---

```
### Portability boundary — which rules survive a harness swap, and where each kind is written

<!-- scope: meta -->

Claude Code is currently both the producer and the harness: it writes the diffs and it is also
the runtime that boots the lane, reads the contract, holds the worktree and ends the session.
That is a single point of dependency underneath a doctrine that calls itself provider-agnostic.
Provider-agnosticism in this fleet is real at the MODEL layer and absent at the HARNESS layer —
`ecosystem/provider-registry.yaml` admits six providers and holds their model strings in
agreement by a checker, but every verb in `ecosystem/substrate-registry.yaml` launches `claude`.

This section is not a recommendation to swap harnesses. It states where the coupling actually
sits, and it gives the author of the next rule a test to apply before writing it.

**Already ruled elsewhere — do not restate it here.** The per-repo instruction layer is two
files with one contract: ADR-115 §3.2 (the portable half, the importer, the byte guard, the
scope-resolved precedence) and §3.3 (`AGENTS.md` is Tier-1 payload, deliberately NOT an ADR-38
canonical living doc). Ch2's Purpose paragraph carries the same split. That organ is settled.
What follows covers the organs nothing has ruled.

#### The boundary rule

A rule is HARNESS-BOUND only if its enforcement reads or writes an artifact the harness itself
produces. Everything a git operation, a file on disk, or `uv run --locked` can check is
PORTABLE, and is written without a vendor name. Where a vendor name is genuinely unavoidable it
is confined to ONE enumerated constant with a validator, and that constant is the SEAM.

Applied as three questions, in order, before a rule is written:

1. Would this still fire if the operator typed the commit by hand, with no agent in the room?
   Yes: PORTABLE. Write it with no vendor name, and enforce it as a hook, a test, or an
   `AGENTS.md` line.
2. Is it portable in mechanism but carries a vendor token? Then the token goes in an enumerated
   constant with a checkable surface — never inline in prose, never in a regex spelled out at
   the call site. That is a SEAM, and a seam is admitted, not merely tolerated.
3. Does the rule read something only one harness produces — a session transcript, a `.claude/`
   directory contract, a launch verb? Then it is HARNESS-BOUND. Its home is `CLAUDE.md`,
   `.claude/`, or L0, and it may never be written into `AGENTS.md` or into a gate.

The rule is a placement rule, not a purity rule. Harness-bound rules are legitimate and this
repo needs several of them. What is illegitimate is a harness-bound rule wearing portable
clothes: a vendor assumption inside a gate, or a Claude-runtime fact inside `AGENTS.md`.

#### Where this repo actually sits

The teeth are portable. Every local pre-commit, commit-msg and pre-push entry is
`language: system` running `uv run --locked python scripts/<x>.py`, staged on GIT lifecycle
events rather than agent lifecycle events; the sole non-local entry is the pinned `ruff` rev,
which is harness-neutral too. No hook invokes an agent, reads a transcript, or depends on a
session existing. The gates bind whoever holds the checkout. So does `audit.py`. So do the lane
packets, which are markdown with SHAs and name no harness at all. A harness swap costs these
organs nothing, and that is a property that was built, not inherited — it follows directly from
"LLMs advise; hooks/tests enforce" above.

The coupling is concentrated in three places and nowhere else:

- The `## Dispatch` block, baked into every generated lane contract. `gen_lane_contract.py`
  selects the literal command line from the contract's declared shape and its check leg refuses
  a contract that carries none of the recognised forms. A contract naming a non-Claude executor
  is a refusal today. This is a SEAM: the generator is already shape-selecting, so admitting a
  fourth shape is the same edit the cloud shape was — one enum widening in one module plus its
  tests.
- The Ch8 Layer-2 verb table. Layer-1 routing is substrate logic and portable — gate
  dependency, operator disk, read-only reconnaissance, everything else — and names no vendor.
  Layer 2 is three verbs that all launch `claude`, implemented in a PowerShell module this repo
  does not carry. The swap cost here is real and it is NOT this repo's to pay, which is a
  finding rather than a relief: the most harness-coupled organ in the fleet is the one the hub
  cannot gate. Note also that the single-literal-site discipline is itself load-bearing —
  the four-rival-commands failure is measured, and a swap that reintroduces rival commands
  re-buys it.
- The live-session check. It is authoritative on transcript-cwd — a mangled directory under the
  harness's own projects tree plus a `cwd` grep — and the section states plainly that process
  inspection cannot answer the question. A harness with a different transcript layout, or none,
  leaves this check with no implementation. This is the sharpest hidden coupling in the repo and
  it is a SAFETY check, not a convenience.

Two organs sit on the boundary and are worth naming so they are not misfiled. The worktree rule
is PORTABLE in mechanism — "one checkout, one committing session" is a git-concurrency
invariant true of any agent, any human, any harness — and a SEAM in naming, because `claude/`
is a vendor name inside a gated branch-prefix enum. It is correctly filed: the enum is closed,
it lives in one constant, `validate_branch_naming.py` is its checkable surface, and a fifth
prefix enters only by recorded ruling. That is the seam discipline working. The `.claude/`
skills, commands and plugin surface is CC-COUPLED by file format and PORTABLE by content: the
knowledge inside is markdown and moves, the invocation surface does not.

**The conclusion the map forces: a harness swap is a dispatch-layer project, not a
governance-layer project.** It was not guaranteed, and it is the reason the anxiety about
single-harness dependency can be retired at zero cost rather than paid down with a migration.

#### What this section does not settle

It states portability; it does not witness it. The declared half and the witnessed half are
different claims, and the ask for the witnessed half is live and unratified: intake §H
("portability probe — provider-independence, witnessed not declared") asks for ONE full arc run
by a non-Claude builder, and ADR-108 explicitly names §H as NOT ratified. Nothing here grants
it. If a probe is ever run, the cheapest form that settles anything is narrow: point a second
harness at a throwaway worktree, hand it one already-completed lane contract with the
`## Dispatch` block removed, and measure exactly two things — does its commit pass the local
hook set unaided, and does the unanchored-push gate refuse its push. Both hold, and the
portability claim above is proven rather than inferred. Either fails, and there is a coupling
this section missed. Delete the worktree either way.

It also does not admit a second executor. `substrate-registry.yaml` carries no non-Claude verb,
`provider-registry.yaml` carries no non-Claude `cli:` for an executor role, and this section
changes neither. The two registries stay the machine-readable projection; this section is the
placement doctrine they do not carry and were never meant to.
```

---

## Lane end packet

**Destination — one, argued (done-item 4).** `protocols/PLAYBOOK.md` **Ch2**, as a new `###` section placed immediately after *"Drift-proofing precedence: source → gate → agent"* (`:382`).

The argument, and why the two rivals lose:

- **Ch2 is already the home of one placement rule of exactly this genre.** `source → gate → agent` answers *"where does a rule live so it cannot rot?"* on the **durability** axis. The portability boundary answers the same question on the **portability** axis. They are siblings, they compose (a portable rule still prefers the earliest durable tier), and putting them adjacent is what stops a future author from consulting one and missing the other.
- **Not an ADR.** An ADR ratifies a decision, and this section decides nothing that is not already decided — ADR-115 ruled the instruction-file split, ADR-101 §1 the Tier-1 class, standing ruling B5 the branch-prefix enum. What is missing is a *placement rule for future authors*, and PLAYBOOK is where placement rules live. The decision tree's `not-a-candidate` routing says the same thing from the other direction: a finding that carries no decision to ratification does not become an ADR to give itself weight.
- **Not `AGENTS.md`.** `AGENTS.md` is portable-instruction payload — non-inferable facts only, byte-capped against Codex's 32 KiB `project_doc_max_bytes` (live: `AGENTS.md` 5,714 B + `CLAUDE.md` 23,931 B, measured with `wc -c` this lane). A doctrine section there would be the exact drift ADR-115 §3.2 bounds it against, and it would spend cap headroom on rationale rather than on facts.

**Reconciliation result (done-item 3), stated so it is checkable.** The instruction-file half of this doctrine **already exists** at ADR-115 §3.2/§3.3 and PLAYBOOK `:323`; the draft cites them and restates none of them. `provider-registry.yaml`'s own header scopes it to model **identity** and explicitly excludes doctrine seams and code seams; `substrate-registry.yaml` states "*WHAT THIS FILE IS NOT. It carries no doctrine.*"; `deploy/global-instructions-codex.md` is a **reviewer-role** file whose collision with the repo layer is already scope-resolved in `AGENTS.md`'s header per ADR-115 §3.2. So no existing surface carries the boundary rule for the five non-instruction-file organs. The section is additive, not duplicative.

**One finding beyond the brief, reported not repaired.** ADR-108 §H — *"portability probe (provider-independence, witnessed not declared)"* — is a **live, unratified ask** whose sequencing note pairs it with §C's shadow review as one step. It is the witnessed counterpart to this declared doctrine. The draft names it and explicitly does not discharge it. No row filed, no intake written — reporting only, per the write-scope.

**Evidence I observed myself (not taken from the audit).** Reading `.pre-commit-config.yaml` with `grep`: 21 `id:` lines, of which 20 carry `uv run` entries — consistent with the audit's "20 local hooks + the pinned remote `ruff` rev". `SHAPE_ENUM = ("local", "cloud", "interactive")` and `PERMISSION_MODE = "--permission-mode bypassPermissions"` at `scripts/gen_lane_contract.py:104,116`; `LANE_PREFIXES = ("worktree-", "epic/", "claude/", "automation/")` at `scripts/validate_branch_naming.py:75`.

**Gate declaration.** **I ran no gate and assert none** — read-only by contract. Every repo fact above comes from `grep`, `sed`, `wc` and file reads. I did not attempt `uv run --locked`, and I did not invoke `python3` either, so there is no interpreter claim to declare.

**Write-scope compliance.** ZERO tree writes, ZERO commits, ZERO rows, no branch created, no push, no JOURNAL entry, no index regeneration. Working tree left exactly as cloned. No hook or closure proposal fired; had one, it would have been declined.

**Decision budget (V-2).** Zero escalations. No curated-baseline touch, no rule-vs-ruling conflict, no fork class without a standing ruling. No refuted premise found — the decision-tree leaf, the `not-a-candidate` routing, and all four named reconciliation targets resolved as the contract described them.