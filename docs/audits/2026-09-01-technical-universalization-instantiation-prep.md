# UNIVERSALIZATION PREP — instantiation contracts for `corp-monorepo` and `ai-council`

> **Class:** technical · **Landed:** 2026-09-01 · **Author:** CC (Opus 5, night orchestrator seat).
>
> **Consumed by:** `[#614]` (the VISION→README supersession arc, whose CUT-1 ruling sets the
> migration order this file plans) and **ADR-114** (which ruled the front door and left the
> fleet-wide filename migration as a sequenced program). The `deploy/manifest-v1.5.0.yaml`
> release candidate drafted in the same act reads this file by name for its consumer-state block.
>
> **PREP ONLY — ZERO WRITES TO ANY CONSUMER REPO.** Every consumer fact below was read live on
> 2026-09-01 with `git ls-files` and `deploy/tool.py <repo> --target <tag>` in its **read-only
> assess mode**. Deployment is an attended morning act (P1 class) and nothing here performs one.

## 1 · Live premise verification — what actually holds, measured not inherited

`git ls-files` in each member's own checkout, 2026-09-01. This table is the reason the contracts
below are short: **the methodology surface is already present in all three CUT-1 consumers**, so
instantiation is a reconcile, not a build.

```
member                     README   VISION   AGENTS   uv.lock  .python-version
.dev-knowledge (hub)       yes      yes      yes      yes      yes
ai-council                 --       yes      --       --       --
corp-monorepo              --       yes      --       --       --
corp-ops                   --       yes      --       --       --
corp-sca-time-automation   --       yes      --       --       --
demo-prep                  --       yes      --       --       --
life-architect             --       yes      --       --       --
terminal-setup             yes      --       --       --       --
win-tooling                yes      yes      --       --       --
```

**Three premises CONFIRMED, one REFINED, and the refinement matters.**

- **CONFIRMED** — `ecosystem/parity-surfaces.yaml`'s claim that *"only 2 of the 8 ADR-104 children
  carry a root `README.md` (terminal-setup, win-tooling)"* re-measures exactly true.
- **CONFIRMED** — `terminal-setup` has never had a `VISION.md`. It is the member the
  `canonical-doc-vision` retirement to SHOULD turned from a latent RED into a legible WARN.
- **CONFIRMED** — win-tooling is the most-deployed consumer (v1.4.0, 2026-08-29), which is what
  makes it the instantiation template.
- **REFINED** — `AGENTS.md` is **hub-only across the entire fleet**. ADR-115 made it the portable
  instruction layer eight days ago and no consumer carries one. That is not a defect (the
  `root-agents-md` row is `consumer: LOCAL` by design) but it means *the portable layer is not yet
  portable in practice*, and any statement that the fleet reads `AGENTS.md` is true of one repo.

**Both CUT-1 consumers are on OLDER releases than the template:** corp-monorepo `1.2.0`
(2026-07-07), ai-council `1.3.1` (2026-07-11), win-tooling `1.4.0` (2026-08-29). The migration
order `hub -> monorepo -> ai-council -> win-tooling` therefore walks from the **least**-current
consumer to the **most**-current one, which is the opposite of a risk-first order and is
deliberate: CUT-1 ruled win-tooling last precisely because it is the one that can afford to wait.

## 2 · The derived plan — identical for both consumers, including its blocker

`deploy/tool.py <repo> --target v1.4.0` (read-only assess). **Run against `v1.4.0`, not `v1.5.0`,
and that is a finding rather than a shortcut:** the tool's preflight REFUSES an untagged target —
*"target tag 'v1.5.0' does not resolve in the hub -- the release is not tagged yet"* — even in
assess mode. So a release candidate cannot be dry-run against a consumer until the operator tags
it. v1.5.0 adds no carrier and no component, so the v1.4.0 plan is the v1.5.0 plan plus three
version anchors; that equivalence is stated here so the morning does not re-derive it.

```
carrier            order  detected state    planned action
global-config          1  present_correct   skip
tier1-plugin           2  present_correct   skip
precommit              3  present_drifted   reconcile (merge required pins into .pre-commit-config.yaml)
floor                  4  present_drifted   reconcile (regenerate .claude/CLAUDE-FLOOR.md + .sha256)
enforcement-mesh       5  present_drifted   reconcile (seb + freshness-gate scripts, /override, Stop hook, logs/)
editor-config          6  n/a               skip -- declaration-only at this cut
docs                   7  present_drifted   reconcile (intake area + INSTALL.md)

Summary (BOTH repos): 4 need apply, 2 already correct, 0 undetectable, 1 not implemented.
```

**THE BLOCKER IS THE SAME IN BOTH, AND IT IS A HARD REFUSAL, NOT A WARNING.** The remove leg
finds `ruff-gate` (status `removed` since 1.2.0) **`present_modified` — locally modified since
deploy — and the prune WOULD REFUSE.** The hash guard is doing exactly its job: a consumer edited
the component after it was deployed, so the tool will not destroy the edit. `--execute` aborts
with **no record written and no staging**, because the version-record write is gated on every
carrier verifying AND every prune verifying absent. **So neither instantiation can complete until
that one component is adjudicated**, and adjudicating it means reading what the local
modification actually is — which is a consumer-repo read the morning seat should do with the
diff in front of it, not a guess made at night.

## 3 · Instantiation contract — `corp-monorepo` (migration step 1)

**Premises, verified live:** branch `main`, clean tree, origin
`https://github.com/rdwornik/corp-monorepo.git`, HEAD `37b8aa1`, 821 tracked files, 8 tracked
under `.claude/`. Carries CLAUDE.md, ARCHITECTURE.md, CONTRIBUTING.md, JOURNAL.md, LESSONS.md,
BACKLOG.md, `.pre-commit-config.yaml`, `pyproject.toml`, `.claude/CLAUDE-FLOOR.md`,
`.claude/settings.json`, `.vscode/settings.json`, `docs/intake/README.md`, `INSTALL.md`, VISION.md.
Does **not** carry README.md, AGENTS.md, `uv.lock`, `.python-version`.

**Done-when — four items, each checkable:**

1. `deploy/tool.py corp-monorepo --target v1.5.0 --execute` completes with a version record at
   `1.5.0`, which requires the `ruff-gate` refusal above to be resolved FIRST.
2. The `ruff-gate` local modification is **read and adjudicated**: either the edit is reverted so
   the prune verifies absent, or the component is declared in corp-monorepo's own
   `.methodology.yaml` and the declaration is what suppresses the concern. **Deleting the edit
   unread is the one act this contract forbids.**
3. No parity row is flipped in the same act (see §5). The deploy carries files; the tier flip is a
   separate, later commit at the hub.
4. `audit.py repo corp-monorepo` is green afterwards, and the run is recorded.

**Out of scope, named so it is not attempted:** a root `README.md` for this repo. Its payload —
`templates/README-md-template.md` — does not exist anywhere in the corpus. Carrying the hub's own
front door would copy this repo's title, its strategic-emphasis section and (until R-README, its
fleet roster) into an employer-material monorepo. The manifest calls that "not a migration, a
mis-carry" and it is correct.

## 4 · Instantiation contract — `ai-council` (migration step 2)

**Premises, verified live:** branch `main`, clean tree, origin
`https://github.com/rdwornik/ai-council.git`, HEAD `7a3c057`, 254 tracked files, 8 tracked under
`.claude/`. Same surface inventory as corp-monorepo. Deployed at `1.3.1` (2026-07-11).

**Done-when:** items 1–4 of §3, with `ai-council` substituted, **plus** two repo-specific ones:

5. **The `satellite-onboarding-rulings.yaml` gap is closed or declared.** DC-5 found (and did not
   fix, being outside its write-scope) that ai-council carries **no entry** in
   `ecosystem/satellite-onboarding-rulings.yaml`, unlike every other ruled consumer. That is a
   hub-side file, so closing it is a hub act and needs no consumer write.
6. **The version-provenance tension recorded by DC-5 is carried, not re-litigated.** ai-council's
   `1.3.1` was registered 2026-07-11 — chronologically EARLIER than win-tooling's 2026-08-29
   deploy — so CUT-1's *"win-tooling FIRST instantiated, ai-council consumer #2"* is a statement
   about the CURRENT engine path, not about calendar order. CUT-1 affirmed the order regardless.

**Also carried forward from DC-5, unresolved and deliberately so:** nothing in the tree records
*why* ai-council's declared target (v1.4.0) was never reached from 1.3.1. No schema field exists
for that reason and inventing one is the bespoke path DC-5 was written to refuse. Registered gap
G11, `docs/audits/2026-07-31-technical-382-registry-prep-dossier.md`.

## 5 · Parity impact plan — which members go red at each step, and the mechanical fix

The rows that move, read live from `ecosystem/parity-surfaces.yaml`:

```
row                     tier today                    probe
root-readme-md          hub MUST / consumer LOCAL     path_tracked README.md
root-agents-md          hub MUST / consumer LOCAL     path_tracked AGENTS.md
canonical-doc-vision    hub SHOULD / consumer SHOULD  path_tracked VISION.md
```

**`LOCAL` is why the fleet is green today** — `fleet_parity` reports *at parity, 0 blocking
verdicts*. A `LOCAL` row asks nothing of a consumer. The migration's whole risk sits in **when the
tier flips**, and a tier flip is a hub-side one-line commit that can outrun the carrier by
accident.

**The blast radius, counted rather than estimated:**

| If this is flipped consumer-wide TODAY | members that go MUST-absent (severity ERROR; `check_fleet_parity` BLOCKS) |
|---|---|
| `root-readme-md` LOCAL -> MUST | **6** — ai-council, corp-monorepo, corp-ops, corp-sca-time-automation, demo-prep, life-architect |
| `root-agents-md` LOCAL -> MUST | **8** — every ADR-104 child |

**The mechanical fix, and it is not "flip it later".** `fleet_parity` has exactly one legitimate
suppressor: a **`.methodology.yaml` declaration in the consumer's own repo**, which yields
`PASS-declared` and suppresses **one** concern by exact id equality. That is a WRITE TO A CONSUMER
REPO, so it cannot precede the carrier — which produces the correct sequencing rule:

1. **Land the payload first.** `templates/README-md-template.md` at the hub (the missing template),
   then the `readme-front-door` component declared against it in a manifest at or after v1.5.0.
2. **Deploy the carrier to ONE member.** The record in `ecosystem/deployed-versions.yaml` is the
   evidence that member is ready.
3. **Only then flip that member's expectation** — and because the tier is a two-role scalar
   (`hub` / `consumer`) rather than a per-member map, *the consumer role stays `LOCAL` until the
   LAST member has the file*. Per-member progress is tracked by `deployed-versions.yaml`, not by
   the parity tier. **Any attempt to express partial progress in the `tier:` field turns the
   not-yet-migrated members RED in one commit.**
4. `canonical-doc-vision` needs no further action for the migration: at `SHOULD/SHOULD` it warns
   rather than blocks, which is precisely the state that lets `VISION.md` leave a member without
   that member going RED.

**The `doc_shapes` coupling, which bites at step 1 and not at step 3.** `release_lint` C7 asserts
EXACT dict equality between a manifest's `doc_shapes` spines and the live `audit._CANONICAL_SPINE`
— and it lints **v1.1.0 and v1.2.0 against those same live constants**. Adding `README.md` to
either side alone REDs shipped specs. Verified on the v1.5.0 draft: it lints 8/8 with only the
expected C2-tag WARN, which is true **only because `_CANONICAL_SPINE` does not yet carry
`README.md`**. The spine re-point is therefore a coordinated edit across every live manifest, and
it is ADR-114 option (C)'s work rather than a step in this migration.

## 6 · What this prep does NOT do

- **No consumer repo was written to.** Every consumer fact is a read.
- **No release was tagged.** `deploy/manifest-v1.5.0.yaml` is a candidate; the operator tags per
  ADR-91, and until he does `release_lint --version v1.5.0` reports C2-tag as its only finding.
- **No parity tier was flipped**, for the reason §5 counts.
- **No template was authored.** `templates/` was a live lane's frozen write-scope for the whole
  window, so `templates/README-md-template.md` — the one payload the migration is actually waiting
  on — remains the first morning act.
