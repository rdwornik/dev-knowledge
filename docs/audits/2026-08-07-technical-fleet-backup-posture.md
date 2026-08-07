# Fleet backup posture — [#320] every unpushed ref pushed or dispositioned

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-07 · **Slug:** fleet-backup-posture
- **Lane:** `worktree-lane-c-320-backup` (naming note: the frozen contract named
  `lane-3-320-backup`; `validate_branch_naming.py` requires a single lowercase letter, not a
  digit, in that slot — operator chose `lane-c-320-backup`, 3rd lane, at boot)
- **Scope:** git-ops + this one document — no file edits, no deletes, no branch deletions, no
  force-pushes, no remote-settings changes in any repo. Review artifact: not required (no code
  diff — docs+ops lane).
- **Contract:** for every fleet repo, enumerate local branches vs tracking remotes and stashes;
  push unpushed refs (safe, additive, never force) or record an explicit accept-local decision;
  done-when is zero silently-unpushed refs.
- **Repo roster:** the 9 repos in `ecosystem/registry.md` (hub + 8 satellites).

## Per-repo table

| Repo | Refs found | Pushed | Accept-local / refused | Stashes |
|---|---|---|---|---|
| `.dev-knowledge` (hub) | `main` (=), `automation/fleet-audit` (=), `docs/am4-dispatch-visibility` + 5× `worktree-*` — all at the same commit as `main`'s tip, zero unique commits | none needed | accept-local: the `docs/am4-dispatch-visibility` and `worktree-*` refs are ephemeral session/provisioning branches with no commits beyond `main`'s tip — nothing to lose; `git-discipline.md` "WORKTREE TEARDOWN" already governs their lifecycle (deleted at teardown, never pushed) | none |
| `ai-council` | `main` (=) | none needed | already in sync | none |
| `corp-monorepo` | `main` (behind origin 2, not ahead), `docs/327-interface-genre-markers` (1 ahead, no upstream), `vk/c35d-test` (0 ahead of origin/main — stale vibe-kanban worktree snapshot, all commits already reachable from origin/main) | **`docs/327-interface-genre-markers` pushed** — new branch created on origin (`4c7d7f4` docs-only, commit message itself says "left unmerged for a corp session to review and ship") | accept-local: `vk/c35d-test` has zero unique commits, nothing to push; `main`'s behind-2 is a pull gap, not an unpushed-work gap, out of this contract's scope | none |
| `corp-ops` | `main` (ahead 4, no divergence) | **pushed**, `40d703a..d040fcb` | — | none |
| `corp-sca-time-automation` | `main` (ahead 4, no divergence), `feature/tenrox-loader` (=) | **`main` pushed**, `2fb2627..c16fc24` | — | none |
| `demo-prep` | `main` (ahead 60, no divergence), `fix/audit-needs-input` (=, parked-state checkpoint) | **`main` pushed**, `e5dd417..63a9644` (ADR-001 repo-invariants gate passed) | — | none |
| `life-architect` | `main` (ahead 4, no divergence) | **pushed**, `c57d045..7688b76` | — | none |
| `terminal-setup` | `main` (=) | none needed | already in sync | none |
| `win-tooling` | `main` + 13 `chore/docs/feat/fix` branches, all real typewhisper-stability work, **none with an upstream** | **none — REFUSED at the repo level: no `origin` remote is configured at all** (`git remote -v` empty, confirmed via `.git/config`) | **flagged, not accept-local** — this is not a "pushing is wrong" decision, it's "there is nowhere to push to." 14 branches of real work sit on local disk only. Recovery (deciding whether/where to add a remote) is the architect's per the contract's REFUSED clause; this lane made no remote-settings change | none |

## Stash sweep

`git stash list` (and `--all` where checked) came back empty in every repo checked. No stash
findings anywhere in the fleet.

## Done-when check

- 7 of 9 repos: zero silently-unpushed refs — either already in sync or pushed this session.
- `.dev-knowledge` + `corp-monorepo`'s `vk/c35d-test`: zero-unique-commit refs, accept-local,
  reason recorded above.
- `win-tooling`: **not clean** — 14 branches of unpushed work with no remote to push to. This is
  the one open item this lane could not close within its git-ops-only, no-remote-settings-changes
  boundary. Flagged to the operator; not silently dispositioned as accept-local.

## What this lane did NOT do

Per the frozen contract's exclusions: no file edits, no deletes, no branch deletions, no
force-pushes, no remote configuration changes (in particular, `win-tooling` was left exactly as
found rather than having a remote invented for it). No file content touched in any of the 9 repos
beyond this one record, committed in this lane's own worktree.
