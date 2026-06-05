<!-- scope: meta -->

# ADR-72 — Cloud Routines are hub-independent (self-containment); ADR-71's URL-swap hatch is closed for a private hub

**Status:** Accepted — 2026-06-06 (operator-ruled, Path A of the #86.2 fork). Records **#86 sub-decision 2** — the cloud-session resolution model for hub references that ADR-71 left as "URL-swappable later."
**Amends (does not edit):** ADR-71 §"Local-path reachability now, URL-swappable later" — the URL/git-source escape hatch it anticipated is **closed for the cloud case** by the hub's private visibility (see Decision 3). ADR-71 itself is immutable and unchanged.
**Related:** ADR-71 (doc-tooling hook source repo), ADR-70 (three-tier process; Tier-1 plugin), ADR-28/ADR-69 (Layer-2 never executes / read-only cross-repo), BACKLOG #86 (cloud-night decision package), PLAYBOOK "Routine/night deployment standard", `docs/archive/2026-06-05-agent-automation-external-research-note.md` §1 (sandbox-compromise stance).

## Context

#86.2 set out to make hub references (hooks, shared scripts, methodology files) **resolvable in a cloud Routine that clones only the child repo**, distributing them via plugin/skill per the #86.3 ruling. The UNDERSTAND phase (2026-06-06) **falsified that premise** with four verified facts:

- **The hub `.dev-knowledge` is PRIVATE** (`gh api repos/rdwornik/dev-knowledge --jq .visibility` = `private`; ai-council = public, corp-monorepo = private). A git-URL / git-source marketplace pointing at the hub would require credentials **inside** the cloud sandbox.
- **The `tier1-lifecycle` plugin is VERIFIED INERT in cloud** — JOURNAL 2026-06-04 (the Step-6 cloud test): *"tier1-lifecycle plugin inert in cloud — local-only marketplace path — harmless."* The `extraKnownMarketplaces` source is a `directory` at a local Windows path that does not exist on the Linux runner, so the plugin never loads. Plugin/skill — the #86.3 vehicle — therefore does **not** resolve in cloud for a private hub.
- **The cloud runtime is a single-repo Linux clone** at `/home/user/<repo>/` (2026-06-05 conformance digest, evidence line 61). `../.dev-knowledge` does not exist; only the Routine's target repo is present.
- **The conformance verifiers are self-referential** — `conformance-hub.js` scans the *cloned repo's own* `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS`, its own git history, and its own BACKLOG. It consults **no** hub path at runtime (the #86 pilot "ported hardcoded Windows paths for the Linux cloud clone").

### Hub-reference inventory (what a child-repo session depends on, and its cloud behavior)

- **Class A — pre-commit doc-tooling hooks** (`toc-freshness`/`toc-generate`, codemap-\* hub-only) via `repo: ../.dev-knowledge` `rev: 69558c7`. Cloud: sibling path absent; pre-commit is not installed in a fresh clone → hooks never fire. **Not load-bearing** (a read-only Routine commits no source).
- **Class B — CC plugin `tier1-lifecycle`** (Stop→propose_closures, `/review-closures`) via a local-directory marketplace. Cloud: **verified inert / harmless**. **Not load-bearing** (and unwanted — it would write `logs/PROPOSALS` in a read-only run).
- **Class C — methodology / standards files** (`../.dev-knowledge/protocols/ESSENTIALS.md`, `PLAYBOOK.md`, `docs/handoffs/`, `LESSONS.md`, `codex/AGENTS.md`). Cloud: absent. **Not load-bearing** for the self-referential conformance Routine; load-bearing only for a *hypothetical* cross-repo-standards audit in cloud (none planned).
- **Class D — user skills / gotchas** (`~/.claude/skills/gotchas`, `verify`; corp-monorepo also carries a repo-local `.claude/skills/gotchas` that travels with the clone). Cloud: `~/.claude/skills` not in the clone; a committed repo-local copy resolves. **Not load-bearing** (advisory).

For the **currently planned** read-only conformance Routine, **no hub reference is load-bearing in cloud** — every class degrades, and the references that exist are inert-by-design.

## Decision

1. **Cloud Routines are self-contained.** A cloud Routine consults only the repo it clones — its own git, living docs, and backlog. No hub reference sits on the executing path. Authoring a cloud workflow spec that reads `../.dev-knowledge/...` (or any hub path) is a defect, not a feature gap.

2. **The existing hub references are inert-by-design in cloud, and that is acceptable.** The Class-A pre-commit hooks never fire (pre-commit uninstalled in a fresh clone; a read-only run commits no source); the Class-B plugin never loads (local-directory marketplace absent on Linux — verified harmless). They remain wired for **local** sessions and are simply absent in cloud. No child-repo edits are required to "fix" them (and none are made here — ADR-41).

3. **ADR-71's "URL-swappable later" hatch is closed for the cloud case by the hub's private visibility.** Switching a consumer's `repo:` (or a marketplace) to a git URL pointing at the private hub would require auth **inside** the cloud sandbox. The #86 rulings forbid that: no embedded secrets, and the sandbox is treated as already compromised (research note §1). Plugin/skill distribution (#86.3) consequently cannot make a **private** hub resolvable in cloud. URL-fetch of the hub is **off the table** (private).

4. **No resolver code is shipped.** A plugin-cache resolver (the original #86.2 hypothesis) would be **inert in cloud** — the plugin that would host it does not load there — so it would be machinery that cannot run in the environment it targets (false coverage). The guarantee here is **structural** (self-containment), not a script.

5. **STOP-and-escalate rule for the future.** If a future cloud Routine genuinely needs a hub reference (methodology, standards, or shared tooling) at runtime, that need **cannot** be satisfied for a private hub by plugin/skill/URL without either publishing a hub subset (reverses the private posture) or standing up an auth'd cloud-reachable source (new infra/secrets). That is an **operator decision** — surface it and stop; do not improvise it inside a session.

## Consequences

- **Positive.** Cloud Routines need no hub clone, no hub auth, and no new infrastructure; the private-hub posture is preserved intact. This is exactly the #86 design intent — *"the hub should not need to be reachable from the cloud."*
- **Honest limit — degradation is silent, not loud.** This doctrine does **not** make hub references resolvable in cloud; it declares them out of scope there. The inert references fail *quietly* (pre-commit simply doesn't run; the plugin simply doesn't load) — there is no logged no-op line, because the very machinery that would log it is what doesn't run. The "loud" guarantee is therefore relocated to **design time**: a cloud workflow spec must be authored self-contained, and any spec that *does* depend on a hub ref must fail-closed at the consumer/Action layer that actually executes (PLAYBOOK "put the code guarantee where the bytes actually flow"). A reviewer cannot rely on a runtime warning to catch a hub-coupled cloud spec — it must be caught in review.
- **Local sessions unchanged.** `../.dev-knowledge` hooks and the `tier1-lifecycle` plugin keep working on the dev machine; this ADR changes nothing about the local loop.
- **Child-side.** Nothing to install or remove; the inert refs are harmless. If a child later wants its cloud-inert config made visibly intentional, that is a child-session edit (rides the repo's next session per ADR-41), not done here.
- **`ai-council` is public**, but that does not help — the hub ships the methodology/tooling and the hub is private; a public child does not make hub references reachable.

## Alternatives considered (the #86.2 operator fork)

- **B — publish a methodology subset** (a public hook-source / marketplace, e.g. a separate public repo or selectively-public `protocols/` + doc-tooling): the **only** path to genuinely cloud-resolvable hub distribution for the ecosystem, but it reverses the private posture for the published subset — a data-classification call. **Deferred to the operator; kept open as the escalation target for Decision 5.** Not chosen now.
- **C — pre-bake the cloud image** (a Routine setup step that clones the hub / installs the plugin via an auth'd source): **rejected** — new infra/secrets; violates the sandbox-compromise stance (research note §1).
- **Extend the plugin + a plugin-cache resolver** (the original #86.2 hypothesis): **rejected** — verified infeasible (the plugin is inert in cloud), so it would be cloud-inert machinery / false coverage.

## References

- BACKLOG #86 (cloud-night decision package; sub-decision 2 = this ADR).
- ADR-71 (the doc-tooling hook source repo; the "URL-swappable later" clause this amends).
- ADR-28 / ADR-69 (Layer-2 never executes; read-only cross-repo) — why the hub never writes a sibling and why generation is local.
- JOURNAL 2026-06-04 (Step-6 cloud test: plugin inert in cloud) · `docs/audits/2026-06-05-conformance-nightly-digest.md` (Linux `/home/user/<repo>/`, single clone) · `docs/archive/2026-06-05-agent-automation-external-research-note.md` §1 (sandbox-compromise / secrets-boundary).
- PLAYBOOK "Routine/night deployment standard" §"Cloud-session hub-independence" (operational cross-reference).
