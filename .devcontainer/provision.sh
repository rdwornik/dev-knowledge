#!/usr/bin/env bash
# .devcontainer/provision.sh — [#554] NB4-G stage 1: idempotent provisioning + the four asserts.
#
# WHAT THIS IS FOR. A lane that runs off the operator's workstation fails in a shape that looks
# like success: the container builds, the session starts, the gates run — and every one of them
# is vacuous. Intake #39 §D and [#554] name the four measured causes, and this script closes each
# one by ASSERTING it, never by logging it:
#
#   L1  the provisioned `uv` equals the ADR-106 pin        (a wrong uv resolves a different tree)
#   L2  the clone is not shallow                           (history-dependent detectors read clean)
#   L3  all THREE git hook types are armed                 (the witnessed relic-hooksPath class)
#   L4  a half-provisioned environment refuses to start    (`--gate`, wired to postStartCommand)
#
# plus the two obligations the first lane contract added on top of the row:
#   C1  idempotent — a second run is a no-op AND SAYS SO
#   C2  a gate-liveness smoke — run one cheap REAL gate and assert exit 0. Provisioning that
#       cannot prove its gates execute is precisely the failure shape above.
#
# plus two more the 2026-08-21 lane added, both of them things the 2026-08-19 proof lane MEASURED
# rather than anticipated (`docs/audits/2026-08-19-technical-554-proof.md`), and BOTH REMOVED
# [#664] (2026-09-13) — see the retirement record immediately below:
#   L2b (REMOVED) the clone has the REFS a spine walker reads, not merely the DEPTH L2 restores.
#       The proof lane's container had 5329 commits and no local `main`, and every
#       first-parent-spine instrument then errored out. This was contract amendment B1, and it
#       ran before hooks were armed. Declared, not hardcoded: `.devcontainer/provisioning.yaml`.
#   L5  (REMOVED) at least one repo is registered under `ecosystem/`. `audit.py health` counts
#       `ecosystem/*/state.yaml`, that glob is gitignored, and so no clone has ever carried one —
#       which was the single remaining `[!!]` between this substrate and the row's D1a Done-when.
#
# [#664] RETIREMENT RECORD (2026-09-13), read verbatim out of git history before the six call
# sites that implemented L2b/L5 were removed from this file — `scripts/cloud_provisioning.py`
# implemented both and was retired at `3c9418cc` ([#734]) WITHOUT its six callers here being
# removed, which is what this lane closes. Its own docstring, quoted so the "what was lost"
# question never has to be re-derived from the call names alone:
#
#   history  (L2b) "Leg 2 unshallows, so a cloud clone has DEPTH. It does not necessarily have
#            REFS: the proof lane's codespace carried 5329 commits and no local `main`, and
#            every instrument that walks main's first-parent spine then ERRORED ... rather than
#            passing vacuously. 'Not shallow' is necessary and insufficient; this asserts the
#            sufficient precondition and repairs it BEFORE a lane can reach a spine walker."
#            Repair (`history --repair`) deepened the clone, fetched each `required_refs` entry
#            named in `.devcontainer/provisioning.yaml`, and fast-forwarded it — REFUSING (never
#            force-updating) a ref that had diverged or reached the remote tip only off the
#            first-parent spine, so it could not discard local commits.
#   ecosystem (L5) "`audit.py health` reports `repos registered (none)` in a fresh container ...
#            not structural: `discover_repos()` counts `ecosystem/*/state.yaml`, that glob is
#            GITIGNORED, and so no clone has ever carried one. The workstation copies them from
#            the primary checkout ...; a container has no primary, so it audits the one repo it
#            has and saves the genuine result." Repair (`ecosystem --repair`) ran `audit.audit_repo`
#            + `audit.save_state` against THIS checkout and wrote its `ecosystem/<name>/state.yaml`.
#
# MEASURED, not assumed, the same day: before removal, with the module gone, every one of the six
# now-removed calls (two in `leg2b_history`, two in `leg5_ecosystem`, two in `gate()`) exited 2
# ("can't open file ... No such file or directory"), which the surrounding `case`/`|| die` treated
# as failure. So provisioning did NOT "quietly do nothing" here — a fresh
# `bash .devcontainer/provision.sh` had been dying at `leg2b_history`, and `--gate` (wired to
# postStartCommand) had been refusing every container start, since `3c9418cc` landed, both with a
# "re-provision" message that could not succeed because the module it named was gone for good.
# Removing the six dead call sites (this lane) stops that crash; it does not restore L2b or L5,
# which is why this lane also files BACKLOG `[#746]` for the real repair.
#
# SINGLE SOURCE OF PINS. Nothing below hardcodes a version that already has a home in the repo:
#   uv          <- pyproject.toml [tool.uv] required-version   (read, and required to be `==`)
#   interpreter <- .python-version
#   deps        <- uv.lock, via `uv sync --locked`
# Bumping any of those needs no edit here; the assert re-reads the source and the stamp goes stale,
# which is exactly what makes `--gate` refuse a container provisioned against the old pin.
#
# PORTABILITY (row Done-when clause 2 — "the *identical* script is runnable via `devcontainer up`
# on a VPS"). There is no Codespaces-specific branch anywhere in this file: it discovers its own
# repo root, reads pins from the repo, and talks to nothing but git, curl and uv.
#
# HONEST LIMIT, stated rather than left to be discovered. The devcontainer spec has no hook that
# can hard-abort a container mid-start. The strongest refusal available is a non-zero
# `postStartCommand`, which the runtime surfaces as a failed start and which leaves the lane
# looking at an error instead of at a green prompt; `"waitFor": "postCreateCommand"` is what stops
# a session attaching before provisioning has finished. So L4 refuses LOUDLY and blocks the
# session's start path — it does not stop the container process itself. Nothing here is a
# server-side gate either: a determined operator can run the tools by hand.
#
# SECOND HONEST LIMIT, measured on 2026-08-18 rather than reasoned about. L3 reuses
# `arm_hooks._armed`, which counts a hook shim bound to a DIFFERENT interpreter as unarmed. Git
# gives every worktree of a repo the SAME hooks directory (`git rev-parse --git-path hooks`
# resolves to the common dir) while `uv sync` gives every worktree its OWN venv — so on a host
# running N worktrees off one clone, at most one of them satisfies L3 and the rest are refused
# with "bound to a stale interpreter". That was reproduced here: all three shims were present and
# pre-commit-managed, with INSTALL_PYTHON pointing at a sibling lane's venv. Inside a container
# this does not arise — one checkout, one venv — but intake #39's own stage-2 model is "N git
# worktrees" on the VPS, so anyone extending this script there inherits the limit. It belongs to
# `arm_hooks._stale_interpreter`, not to this file, and is left there deliberately: duplicating a
# softened copy of the predicate here would give the repo two answers to one question, which is
# the drift this reuse exists to avoid.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# The env gate's own knob. NOT declared in devcontainer.json any more — see the long comment
# there: `containerEnv` cannot reference `containerEnv`, so the declaration arrived here
# UNEXPANDED and `mkdir -p "$(dirname ...)"` created a directory literally named
# `${containerEnv:HOME}` inside the working tree on every container start (measured,
# `docs/audits/2026-08-19-technical-554-proof.md` §2.1). A VPS host that wants the stamp
# somewhere else exports the variable itself; everyone else gets the $HOME default the old
# declaration only claimed to produce. The stamp is written ONLY after every assert below passes.
STAMP="${DEV_KNOWLEDGE_PROVISION_STAMP:-${HOME}/.dev-knowledge-provision-stamp}"
STAMP_SCHEMA="dev-knowledge-provision/1"

# Close the CLASS, not just the instance. Any host — Codespaces, a VPS, a future spec revision —
# can hand this script a path whose `${...}` never expanded. Creating a directory with that name
# is silent corruption of the tree the lane is about to work in, so it is refused here instead.
case "${STAMP}" in
  *'${'*)
    printf '[provision] REFUSED: DEV_KNOWLEDGE_PROVISION_STAMP is %s — an UNEXPANDED ${...} path.\n' "${STAMP}" >&2
    printf '[provision]           Creating it would put a junk directory inside the working tree.\n' >&2
    printf '[provision]           Unset the variable to use the ${HOME} default, or export a literal path.\n' >&2
    exit 1
    ;;
esac

UV_BIN_DIR="${HOME}/.local/bin"
export PATH="${UV_BIN_DIR}:${PATH}"

CHANGED=0                       # C1: how many legs actually DID something this run

say()  { printf '[provision] %s\n' "$*"; }
noop() { printf '[provision] %s (no-op)\n' "$*"; }
die()  { printf '[provision] REFUSED: %s\n' "$*" >&2; exit 1; }

# --- pin readers: the single-source discipline, in code ------------------------------------------

# pyproject.toml [tool.uv] required-version, section-scoped. Section scoping is not decoration:
# [tool.ruff] carries a `required-version` too, and a naive grep would read the ruff floor as the
# uv pin. The pin is REQUIRED to be an exact `==` spec — [#554]'s leg 1 is "a pinned-uv assert",
# and a range is not a pin.
read_uv_pin() {
  local spec
  spec="$(awk '
    /^\[/                                            { section = $0 }
    section == "[tool.uv]" && /^required-version[[:space:]]*=/ {
      if (match($0, /"[^"]*"/)) { print substr($0, RSTART + 1, RLENGTH - 2); exit }
    }
  ' pyproject.toml)"
  [ -n "${spec}" ] || die "pyproject.toml [tool.uv] required-version not found — cannot assert the uv pin (L1)"
  case "${spec}" in
    "=="*) printf '%s\n' "${spec#==}" ;;
    *)     die "pyproject.toml pins uv as '${spec}', which is not an exact '==' pin — [#554] leg 1 requires one (ADR-106)" ;;
  esac
}

read_python_pin() {
  [ -f .python-version ] || die ".python-version not found — cannot assert the interpreter"
  tr -d '[:space:]' < .python-version
}

installed_uv_version() {
  command -v uv >/dev/null 2>&1 || return 1
  uv --version 2>/dev/null | awk '{print $2}'
}

# --- L1: pinned uv, installed AND asserted -------------------------------------------------------

leg1_uv() {
  local want have
  want="$(read_uv_pin)"
  have="$(installed_uv_version || true)"

  if [ "${have}" = "${want}" ]; then
    noop "L1 uv already at the pinned ${want}"
  else
    say "L1 installing uv ${want} (found: ${have:-none})"
    # The astral installer takes the version in the URL, so this installs the PIN, never "latest".
    # `latest` is what silently drifted a cloud channel onto 0.8.17 against this repo's 0.11.19 —
    # half the reason [#554] exists.
    curl -LsSf "https://astral.sh/uv/${want}/install.sh" \
      | env UV_INSTALL_DIR="${UV_BIN_DIR}" INSTALLER_NO_MODIFY_PATH=1 sh >/dev/null
    CHANGED=$((CHANGED + 1))
  fi

  # THE ASSERT — this is the leg, not the install above.
  have="$(installed_uv_version || true)"
  [ "${have}" = "${want}" ] || die "L1 uv is '${have:-none}', pinned '${want}' (pyproject [tool.uv] required-version)"
  say "L1 OK — uv ${have} == pin ${want}"

  # Persist PATH for every later shell in this container (idempotent: marker-guarded append).
  if [ -f "${HOME}/.bashrc" ] && ! grep -Fq '# dev-knowledge provision: uv on PATH' "${HOME}/.bashrc"; then
    { echo ''
      echo '# dev-knowledge provision: uv on PATH'
      echo "export PATH=\"${UV_BIN_DIR}:\$PATH\""
    } >> "${HOME}/.bashrc"
    CHANGED=$((CHANGED + 1))
  fi
}

# --- L2: unshallow, because the gates read history -----------------------------------------------

leg2_unshallow() {
  # git refuses to operate on a bind-mounted tree owned by another uid until it is trusted. Adding
  # this is idempotent by check-then-add — `git config --add` would otherwise duplicate every run.
  if ! git config --global --get-all safe.directory 2>/dev/null | grep -Fxq "${REPO_ROOT}"; then
    git config --global --add safe.directory "${REPO_ROOT}"
    CHANGED=$((CHANGED + 1))
  fi

  if [ "$(git rev-parse --is-shallow-repository)" = "true" ]; then
    say "L2 clone is shallow — fetching full history"
    # Guarded: `--unshallow` is an error on a complete clone, which is why this is inside the if.
    git fetch --unshallow --quiet \
      || die "L2 'git fetch --unshallow' failed — a shallow clone with no reachable remote cannot be repaired here"
    CHANGED=$((CHANGED + 1))
  else
    noop "L2 clone already has full history"
  fi

  [ "$(git rev-parse --is-shallow-repository)" = "false" ] \
    || die "L2 repository is STILL shallow — every history-dependent gate (journal_spine_anchor, no_ff_merges, the git-log detectors) would be vacuous"
  say "L2 OK — full history ($(git rev-list --count HEAD) commits reachable from HEAD)"
}

# --- [#593]: FRESHNESS — a prebuilt image is a snapshot, and it lies quietly ----------------------
#
# THE MEASURED DEFECT (close packet §11 defect 3, 2026-08-26). A codespace created from the
# prebuilt image came up with in-container `HEAD` at `0360d6d0`, a 2026-08-22 commit, while the
# pushed tip was `6882ef74` — and `git status -sb` printed `## main...origin/main` with NO
# divergence, because the clone had never fetched. Nothing in the container was wrong; the whole
# machine was three days old and said so nowhere. The consequence was not academic: lane CS's
# merge — the very change that installs Claude Code — was absent, so `claude` was not on PATH in
# the container built to prove it. This is the "flag lost across substrates" family: the assertion
# looked at the old artifact.
#
# WHY THIS IS THE ENFORCEABLE HALF, and the prebuild trigger is not. `provisioning.yaml`'s
# `prebuild.trigger` is server-side operator UI state with no public API — the repo can DECLARE it
# and `cloud_provisioning.py prebuild` can report drift, and that is all. This function is the half
# that runs, and it makes the image's own age irrelevant: whatever snapshot the container booted
# from, provisioning brings the tree to the current default branch before any pin is read.
#
# WHERE IT RUNS, from the two docs rather than by preference. containers.dev's JSON reference:
# "postCreateCommand: This command is the last of three that finalizes container setup when a dev
# container is created", and "postStartCommand: A command to run each time the container is
# successfully started". A Codespaces prebuild bakes `onCreateCommand` and `updateContentCommand`
# and never `postCreateCommand` — so `postCreateCommand`, which this script is wired to, runs at
# EVERY creation including a creation from a stale prebuilt image. That is exactly the path the
# defect above travelled, and it is why the repair belongs in provisioning rather than in a new
# lifecycle hook.
#
# WHAT IT WILL NOT DO, stated because the row's brief says "fetch+reset" and this deliberately is
# not `reset --hard`. A container is also where a lane WORKS: it commits locally and pushes. A hard
# reset would delete that work on the next start, and a codespace may legitimately be created from
# a non-default branch. So the repair is narrowed to the one shape that cannot lose anything — on
# the default branch, with a clean tree, STRICTLY BEHIND origin — where a fast-forward and a hard
# reset produce a byte-identical result. Every other shape (dirty, diverged, or a different branch)
# is REPORTED and left alone. A stale tree that says so is the defect closed; a destroyed tree
# would be a worse one opened.
#
# HONEST LIMITS, three, none of them discovered later:
#   * `--assert` mode REPORTS staleness, it does not refuse. Being behind a push made minutes ago
#     is not the half-provisioned state `--gate` exists to refuse, and dying on it would make every
#     container un-startable whenever anything lands on main. L4's pin/stamp refusals are untouched.
#   * It runs AFTER `leg1_uv`, so a run whose fetch also moves the uv pin installs the OLD pin
#     first. That is why a successful fast-forward RE-RUNS `leg1_uv` against what is now on disk —
#     and if that still disagreed, `leg1_uv` dies loudly rather than stamping a lie.
#   * It is not covered by the exact-call-list assertion in
#     `tests/test_cloud_provisioning.py::test_provision_sh_runs_the_history_repair_before_arming_hooks`,
#     which filters on the `leg` prefix. This lane's decision budget was `.devcontainer/` only, so
#     it could not extend that test; deleting the call below therefore still leaves the suite
#     green. Named as owed work in the lane report, not left to be found.

default_branch() {
  # The clone records its own default in `origin/HEAD`. Fall back to the ref
  # `provisioning.yaml` names as the branch a prebuild is built from.
  git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' \
    || true
}

refresh_source_tree() {
  local mode="${1:-repair}" def cur head_sha want_sha

  git remote get-url origin >/dev/null 2>&1 \
    || { noop "freshness: no origin remote — nothing to refresh against"; return 0; }

  def="$(default_branch)"
  [ -n "${def}" ] || def="main"

  # A failed fetch is an OFFLINE host, not a broken one. Say that currency is unverified and
  # carry on; refusing here would make a network blip indistinguishable from a real defect.
  if ! git fetch --quiet --prune origin 2>/dev/null; then
    say "freshness: WARNING — could not fetch origin; currency is UNVERIFIED this run"
    return 0
  fi
  # Only `rev-parse --verify --quiet` distinguishes "missing" from "unreadable"; a single-branch
  # refspec is the shape that leaves the default branch unfetched, so ask for it by name.
  if ! git rev-parse --verify --quiet "origin/${def}" >/dev/null 2>&1; then
    git fetch --quiet origin "+refs/heads/${def}:refs/remotes/origin/${def}" 2>/dev/null \
      || { say "freshness: WARNING — origin/${def} does not resolve; currency is UNVERIFIED"; return 0; }
  fi

  cur="$(git rev-parse --abbrev-ref HEAD)"
  head_sha="$(git rev-parse HEAD)"
  want_sha="$(git rev-parse "origin/${def}")"

  if [ "${head_sha}" = "${want_sha}" ]; then
    noop "freshness: at origin/${def} ($(git rev-parse --short HEAD))"
    return 0
  fi
  if [ "${cur}" != "${def}" ]; then
    say "freshness: on '${cur}', not the default branch '${def}' — leaving it alone (origin/${def} is $(git rev-parse --short "origin/${def}"))"
    return 0
  fi
  if ! git merge-base --is-ancestor HEAD "origin/${def}" 2>/dev/null; then
    say "freshness: '${cur}' has DIVERGED from origin/${def} — local commits exist, so nothing is reset here"
    return 0
  fi
  if [ -n "$(git status --porcelain)" ]; then
    say "freshness: '${cur}' is behind origin/${def} but the tree is DIRTY — refusing to move it; commit or clean, then re-provision"
    return 0
  fi

  say "freshness: '${cur}' is behind origin/${def} by $(git rev-list --count HEAD.."origin/${def}") commit(s) — $(git rev-parse --short HEAD) -> $(git rev-parse --short "origin/${def}")"
  if [ "${mode}" = "--assert" ]; then
    say "freshness: assert-only — this container is running a STALE tree; re-provision (bash .devcontainer/provision.sh)"
    return 0
  fi

  # Strictly behind + clean: a fast-forward and a hard reset are the same bytes, and this one
  # cannot eat anything.
  git merge --ff-only --quiet "origin/${def}" \
    || die "freshness: fast-forward to origin/${def} failed on a tree reported clean and strictly behind — refusing to guess"
  CHANGED=$((CHANGED + 1))
  say "freshness: OK — now at origin/${def} ($(git rev-parse --short HEAD))"

  # The tree just moved, so every pin read before this point was read from the OLD tree. Re-assert
  # the one that was already acted on; the rest are read after this function returns.
  leg1_uv
}

# --- the environment itself: exact interpreter + locked deps -------------------------------------

sync_environment() {
  local py_want py_have
  py_want="$(read_python_pin)"

  # C1 accounting for the environment itself. Both steps below are idempotent and therefore
  # silent when there is nothing to do, so neither could bump CHANGED — a container that
  # rebuilt a missing `.venv` still printed "idempotent: nothing changed" (terra HIGH round 2,
  # 2026-08-21). ASK FIRST, in the same read-only form the gate uses.
  uv python find "${py_want}" >/dev/null 2>&1 || CHANGED=$((CHANGED + 1))
  uv sync --locked --group analytics --check >/dev/null 2>&1 || CHANGED=$((CHANGED + 1))

  # uv provisions the EXACT interpreter, so the base image's own Python never decides what the
  # gates run on. Idempotent by uv's own design (a present version is reported, not re-downloaded).
  uv python install "${py_want}" >/dev/null 2>&1 \
    || die "could not provision Python ${py_want} (from .python-version) via uv"

  # `--locked` REFUSES to update uv.lock: if the lock and pyproject disagree this fails rather
  # than silently resolving something else. The analytics group is included deliberately — a venv
  # without it reds the L5a tests, so `pytest -m 'not slow'` (Done-when D1) would not be green.
  # pyproject documents this invocation as the superset of the plain dev sync.
  uv sync --locked --group analytics >/dev/null \
    || die "'uv sync --locked --group analytics' failed — the lockfile and pyproject.toml disagree, or a dependency is unavailable"

  py_have="$(uv run --no-sync python -c 'import platform; print(platform.python_version())')"
  [ "${py_have}" = "${py_want}" ] \
    || die "interpreter is ${py_have}, .python-version pins ${py_want}"
  say "environment OK — Python ${py_have} (.python-version), deps from uv.lock via --locked"
}

# --- L2b/L5: REMOVED [#664] (2026-09-13) — both called the retired scripts/cloud_provisioning.py
# (six call sites total, here and in `gate()` below) and have not run since 3c9418cc ([#734]).
# The record of what B1 (history sufficiency) and L5 (ecosystem self-registration) did lives in
# this file's top-of-file "[#664] RETIREMENT RECORD" comment. The real repair is tracked, not
# reimplemented here: BACKLOG [#746].

# --- L3: all three hook types armed, asserted ----------------------------------------------------

assert_hooks_armed() {
  # REUSE, not a re-implementation. scripts/arm_hooks.py already owns this predicate — it resolves
  # the hooks dir through `git rev-parse --git-path hooks` (so core.hooksPath is honoured, which is
  # how the witnessed relic silently disarmed the gates) and treats a shim bound to a stale
  # interpreter as unarmed. Duplicating that logic here would give the repo two answers to one
  # question; calling it gives one.
  uv run --no-sync python - <<'PY'
import pathlib
import sys

sys.path.insert(0, "scripts")
import arm_hooks  # noqa: E402  (path is set immediately above)

root = pathlib.Path.cwd()
hooks = arm_hooks._hooks_dir(root)
if hooks is None:
    print("hooks directory unresolvable via `git rev-parse --git-path hooks`", file=sys.stderr)
    raise SystemExit(1)
print(f"[provision] L3 resolved hooks dir: {hooks}")
missing = [h for h in arm_hooks.HOOK_TYPES if not (hooks / h).exists()]
if missing:
    print(f"hook type(s) absent: {', '.join(missing)}", file=sys.stderr)
    raise SystemExit(1)
if not arm_hooks._armed(hooks):
    print("hooks present but NOT pre-commit-managed or bound to a stale interpreter", file=sys.stderr)
    raise SystemExit(1)
PY
}

leg3_hooks() {
  local relic
  relic="$(git config --get core.hooksPath || true)"
  [ -z "${relic}" ] || say "L3 note — core.hooksPath is set to '${relic}'; the assert below resolves through it"

  if assert_hooks_armed >/dev/null 2>&1; then
    noop "L3 all three hook types already armed"
  else
    say "L3 arming git hooks (pre-commit / commit-msg / pre-push)"
    # arm_hooks.py is fail-SOFT by design — it must never block a session at SessionStart. That is
    # the wrong posture at provision time, so the install is delegated to it and the REFUSAL is
    # ours: [#554] leg 3 says deterministic, and intake #39 §D(3) says "fails if not armed".
    uv run --no-sync python scripts/arm_hooks.py || true
    CHANGED=$((CHANGED + 1))
  fi

  assert_hooks_armed \
    || die "L3 hooks are NOT armed — a lane here would produce commits that never passed a gate (the relic-hooksPath class, witnessed twice)"
  say "L3 OK — pre-commit / commit-msg / pre-push all armed and pre-commit-managed"
}

# --- C2: gate-liveness smoke — prove a REAL gate actually executes --------------------------------

smoke_gate_liveness() {
  # `validate_backlog` is the cheap real gate the lane contract names. The invocation is the one
  # .pre-commit-config.yaml's `validate-backlog` hook uses, verbatim, so this proves the same
  # command line the hook will run — not a lookalike. Exit 0 is asserted; its stdout is kept
  # because a passing gate that printed nothing would be indistinguishable from one that no-oped.
  local out
  out="$(uv run --no-sync python scripts/validate_backlog.py 2>&1)" \
    || { printf '%s\n' "${out}" >&2; die "C2 gate-liveness smoke FAILED — validate_backlog did not exit 0, so this environment cannot run the gate mesh"; }
  printf '[provision] C2 smoke: %s\n' "$(printf '%s\n' "${out}" | head -n 1)"
  # F3 (2026-08-31): a SECOND real gate, named by the admission ruling. `validate_backlog` proves
  # a gate runs; this proves the LOCKED resolver runs, which is the leg that actually failed on
  # the measured container -- `uv` was absent, so every `uv run --locked` invocation in the mesh
  # was unrunnable while the container still reported a successful build.
  local tt
  tt="$(uv run --locked python scripts/gen_task_tree.py --check 2>&1)"     || { printf '%s
' "${tt}" >&2; die "F3 FAILED — \`uv run --locked python scripts/gen_task_tree.py --check\` did not exit 0; the locked resolver does not work in this container"; }
  say "F3 OK — the LOCKED resolver ran a real generator check and returned 0"
  say "C2 OK — a real gate executed here and returned 0"
}

# --- F1: the Claude CLI, installed here and ASSERTED ---------------------------------------------
# The `claude-code:1.0` devcontainer feature was dropped 2026-08-31. The original reason recorded
# here -- "it left NO binary on two builds, one of them a `--full` cache-busting rebuild" -- is
# WITHDRAWN and re-scoped the same day: a `rebuild --full` does not re-apply `devcontainer.json`,
# so neither build had run the feature at all. What the evidence supports is "a rebuilt container
# does not re-run features or postCreate", not "the feature is broken" (JOURNAL 2026-08-31 (j),
# ruling CREATE-NEVER-REBUILD). The removal stands on the remaining reason: Anthropic's docs call
# the native installer the recommended path, it ships a native binary with no Node runtime
# dependency, and installing here is what makes the ASSERT below possible.
# THE ASSERT IS THE POINT: a container without a working agent must never read as a good build.
leg_f1_claude() {
  if command -v claude >/dev/null 2>&1; then
    say "L-F1 ok — claude already present ($(claude --version 2>/dev/null | head -1))"
    return 0
  fi
  say "L-F1 — installing the Claude CLI (native installer)"
  curl -fsSL https://claude.ai/install.sh | bash >/dev/null 2>&1 || true
  export PATH="${UV_BIN_DIR}:${PATH}"
  command -v claude >/dev/null 2>&1 || die "L-F1 FAILED — no \`claude\` on PATH after the native install. A container without an agent is not a provisioned container; refusing rather than reporting success."
  CHANGED=$((CHANGED + 1))
  say "L-F1 ok — claude installed ($(claude --version 2>/dev/null | head -1))"
}

# --- F4: workspace trust, so the DECLARED permission set is the EFFECTIVE one --------------------
# Measured on the 2026-08-31 admission probe, twice, and it survives provisioning: a headless
# `claude -p` prints "Ignoring 1 permissions.allow entry from .claude/settings.json: this
# workspace has not been trusted" and then runs anyway, under a NARROWER permission set than the
# repo declares. Nothing in the lane's own output says so -- the receipt is a clean success.
# The documented remedy is an interactive trust dialog, which by definition cannot happen on a
# headless substrate, so the container-side write is the only form available here.
# Idempotent, and it merges into whatever `.claude.json` already holds rather than replacing it.
leg_f4_workspace_trust() {
  local cj="${HOME}/.claude.json"
  python3 - "${cj}" "${REPO_ROOT}" <<'PY' || die "L-F4 FAILED — could not record workspace trust; a lane would silently run under a narrowed permission set"
import json, pathlib, sys
cj, root = pathlib.Path(sys.argv[1]), sys.argv[2]
d = json.loads(cj.read_text()) if cj.exists() else {}
proj = d.setdefault("projects", {}).setdefault(root, {})
if proj.get("hasTrustDialogAccepted") is True:
    print("already-trusted")
else:
    proj["hasTrustDialogAccepted"] = True
    cj.write_text(json.dumps(d, indent=2))
    print("trusted")
PY
  say "L-F4 ok — workspace trust recorded for ${REPO_ROOT}; declared permissions are now the effective ones"
}

# --- F2: git credential wiring, from the token Codespaces already issues -------------------------
# Measured 2026-08-31: `git fetch` in this container failed with "could not read Username for
# https://github.com" — no credential helper on the raw ssh path, so a committing lane could
# neither fetch nor push. GitHub issues a repo-scoped token to every codespace at create AND at
# every restart, read/write when the user has write access (GitHub Codespaces security docs), so
# NO PAT is invented here: this wires the token that already exists.
# The helper is written to the repo-local config, never global, and never echoes the value.
leg_f2_git_credential() {
  local tok="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
  if [ -z "${tok}" ]; then
    say "L-F2 SKIP — no GITHUB_TOKEN/GH_TOKEN in this environment; git auth left untouched"
    return 0
  fi
  git -C "${REPO_ROOT}" config --local credential."https://github.com".helper     '!f() { echo username=x-access-token; echo "password=${GITHUB_TOKEN:-$GH_TOKEN}"; }; f'
  say "L-F2 ok — git credential helper wired to the codespace token (value never echoed)"
  CHANGED=$((CHANGED + 1))
}

# --- the stamp: what `--gate` reads --------------------------------------------------------------

write_stamp() {
  local uv_pin py_pin
  uv_pin="$(read_uv_pin)"
  py_pin="$(read_python_pin)"
  mkdir -p "$(dirname "${STAMP}")"
  {
    echo "schema=${STAMP_SCHEMA}"
    echo "repo_root=${REPO_ROOT}"
    echo "uv_pin=${uv_pin}"
    echo "python_pin=${py_pin}"
    echo "head=$(git rev-parse HEAD)"
  } > "${STAMP}"
  say "stamp written: ${STAMP}"
}

# --- L4: the env gate — refuse a half-provisioned environment ------------------------------------

gate() {
  say "gate: re-asserting the four legs against ${STAMP}"
  [ -f "${STAMP}" ] \
    || die "L4 no provisioning stamp at ${STAMP} — this container was never provisioned, or was resumed from an image that predates provisioning. Run: bash .devcontainer/provision.sh"

  # shellcheck disable=SC1090
  local stamped_schema stamped_uv stamped_py want_uv want_py
  stamped_schema="$(sed -n 's/^schema=//p' "${STAMP}")"
  stamped_uv="$(sed -n 's/^uv_pin=//p' "${STAMP}")"
  stamped_py="$(sed -n 's/^python_pin=//p' "${STAMP}")"
  want_uv="$(read_uv_pin)"
  want_py="$(read_python_pin)"

  [ "${stamped_schema}" = "${STAMP_SCHEMA}" ] \
    || die "L4 stamp schema is '${stamped_schema}', expected '${STAMP_SCHEMA}' — re-provision"
  # THE STALENESS LEG. Bump the uv pin or the interpreter in the repo and a container still
  # running the old one is half-provisioned BY DEFINITION — it refuses here instead of handing a
  # lane a toolchain the repo no longer sanctions.
  [ "${stamped_uv}" = "${want_uv}" ] \
    || die "L4 stamped uv pin ${stamped_uv} != repo pin ${want_uv} — the pin moved; re-provision"
  [ "${stamped_py}" = "${want_py}" ] \
    || die "L4 stamped interpreter ${stamped_py} != .python-version ${want_py} — re-provision"

  # The stamp says what WAS true; these say what IS true. Both are required — a stamp alone is a
  # claim, and this row exists because claims looked like proof.
  local have_uv
  have_uv="$(installed_uv_version || true)"
  [ "${have_uv}" = "${want_uv}" ] || die "L4 uv is '${have_uv:-none}', pinned '${want_uv}'"
  [ "$(git rev-parse --is-shallow-repository)" = "false" ] || die "L4 repository is shallow"

  # [#593] freshness, REPORT-ONLY here. `--assert` fetches and says whether this container is
  # running a stale tree; it never moves it, so the gate keeps its "must not repair what it is
  # asserting" contract. It does not die either — see the honest limit above the function: being
  # behind a push made minutes ago is currency, not the half-provisioned state this gate refuses.
  refresh_source_tree --assert

  # THE GATE MUST NOT REPAIR WHAT IT IS ASSERTING (terra HIGH round 2, 2026-08-21). Every Python
  # call below goes through `uv run`, and `uv run` SYNCS by default — it will create or update a
  # missing `.venv` and then happily run in it. That turns the assert-only gate into a silent
  # repair, and worse, the environment it silently builds need not carry the `analytics` group
  # provisioning installs. So the environment is asserted read-only FIRST, and every later call
  # runs with `--no-sync`.
  uv sync --locked --group analytics --check >/dev/null 2>&1 \
    || die "L4 the virtualenv does not match uv.lock (or is absent) — this container is half-provisioned; re-provision (bash .devcontainer/provision.sh)"

  assert_hooks_armed || die "L4 git hooks are not armed"

  # REMOVED [#664] (2026-09-13): two calls into the retired scripts/cloud_provisioning.py used to
  # assert here that a repo re-cloned or re-fetched into a branch-only shape still resolves the
  # refs a spine-walking instrument reads, and that a gitignored ecosystem/ wiped by a rebuild is
  # still registered. Neither condition is checked here any more — see this file's top-of-file
  # "[#664] RETIREMENT RECORD" and BACKLOG [#746] for the real repair.

  say "gate OK — uv ${have_uv}, full history, three hook types armed, stamp current"
}

usage() {
  cat <<'USAGE'
Usage: bash .devcontainer/provision.sh [--gate|--help]

  (no args)  Provision this container and ASSERT all four [#554] legs, run the
             gate-liveness smoke, then write the stamp. Idempotent: a second run
             changes nothing and says so. Wired to postCreateCommand.
  --gate     Assert only — refuse (exit 1) if the environment is half-provisioned
             or the repo's pins have moved since the stamp. Wired to postStartCommand.
  --help     This text.
USAGE
}

main() {
  case "${1:-}" in
    --gate) gate; return 0 ;;
    --help|-h) usage; return 0 ;;
    "") ;;
    *) usage >&2; die "unknown argument: $1" ;;
  esac

  say "provisioning ${REPO_ROOT}"
  leg1_uv
  leg2_unshallow
  # [#593]: bring the tree to the current default branch BEFORE any dependency is resolved from it.
  # It follows leg2_unshallow because `--is-ancestor` needs real history to answer, and precedes
  # sync_environment so the lockfile that is synced is the one that is actually current.
  refresh_source_tree
  sync_environment
  leg3_hooks
  leg_f1_claude
  leg_f2_git_credential
  leg_f4_workspace_trust
  smoke_gate_liveness
  write_stamp

  if [ "${CHANGED}" -eq 0 ]; then
    say "DONE — idempotent: nothing changed, all four legs were already satisfied (second run is a no-op)"
  else
    say "DONE — ${CHANGED} leg(s) acted; all four legs assert clean and a real gate ran here"
  fi
}

main "$@"
