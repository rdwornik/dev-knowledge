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
# rather than anticipated (`docs/audits/2026-08-19-technical-554-proof.md`):
#   L2b the clone has the REFS a spine walker reads, not merely the DEPTH L2 restores. The proof
#       lane's container had 5329 commits and no local `main`, and every first-parent-spine
#       instrument then errored out. This is contract amendment B1, and it runs before hooks are
#       armed. Declared, not hardcoded: `.devcontainer/provisioning.yaml`.
#   L5  at least one repo is registered under `ecosystem/`. `audit.py health` counts
#       `ecosystem/*/state.yaml`, that glob is gitignored, and so no clone has ever carried one —
#       which is the single remaining `[!!]` between this substrate and the row's D1a Done-when.
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

# --- the environment itself: exact interpreter + locked deps -------------------------------------

sync_environment() {
  local py_want py_have
  py_want="$(read_python_pin)"

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

  py_have="$(uv run --locked python -c 'import platform; print(platform.python_version())')"
  [ "${py_have}" = "${py_want}" ] \
    || die "interpreter is ${py_have}, .python-version pins ${py_want}"
  say "environment OK — Python ${py_have} (.python-version), deps from uv.lock via --locked"
}

# --- L2b: history SUFFICIENCY, not merely depth (contract amendment B1) --------------------------

leg2b_history() {
  # L2 above proves the clone is not shallow. That is necessary and NOT sufficient: the proof
  # lane's codespace had 5329 commits and no local `main`, and every instrument that walks main's
  # first-parent spine then ERRORED ("fatal: Not a valid object name main") instead of passing
  # vacuously. This runs the repair — and it runs HERE, before hooks are armed and before any
  # lane work, which is what "before any spine-walking instrument in a cloud lane" means in
  # practice. Which refs are required, and which instruments walk a spine, are declared in
  # .devcontainer/provisioning.yaml, never hardcoded.
  local rc=0
  uv run --locked python scripts/cloud_provisioning.py history --repair || rc=$?
  case "${rc}" in
    0) say "B1 OK — the refs every spine-walking instrument reads resolve, and the walk succeeds" ;;
    1) die "B1 the clone cannot satisfy a spine-walking instrument (see the errors above) — a cloud lane here would run gates that ERROR rather than gates that pass" ;;
    *) die "B1 the history guard could not look (exit ${rc}) — an unknown history state is not a clean one" ;;
  esac
}

# --- L5: the ecosystem registration a fresh clone cannot inherit ---------------------------------

leg5_ecosystem() {
  # `audit.py health` counts `ecosystem/*/state.yaml`, that glob is gitignored, and so no clone
  # has ever carried one — which is why a container reports `repos registered (none)` and health
  # exits non-zero. On the workstation `scripts/worktree_seed.py` copies these from the primary
  # checkout; a container has no primary, so it audits the one repo it has. Not a named row leg:
  # it is the last thing standing between this substrate and [#554]'s D1a Done-when.
  local rc=0
  uv run --locked python scripts/cloud_provisioning.py ecosystem --repair || rc=$?
  case "${rc}" in
    0) say "L5 OK — at least one repo is registered; audit.py health's operational block can pass here" ;;
    1) die "L5 nothing is registered and the seed did not land — audit.py health will report 'repos registered (none)' and exit 1" ;;
    *) die "L5 the ecosystem guard could not look (exit ${rc})" ;;
  esac
}

# --- L3: all three hook types armed, asserted ----------------------------------------------------

assert_hooks_armed() {
  # REUSE, not a re-implementation. scripts/arm_hooks.py already owns this predicate — it resolves
  # the hooks dir through `git rev-parse --git-path hooks` (so core.hooksPath is honoured, which is
  # how the witnessed relic silently disarmed the gates) and treats a shim bound to a stale
  # interpreter as unarmed. Duplicating that logic here would give the repo two answers to one
  # question; calling it gives one.
  uv run --locked python - <<'PY'
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
    uv run --locked python scripts/arm_hooks.py || true
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
  out="$(uv run --locked python scripts/validate_backlog.py 2>&1)" \
    || { printf '%s\n' "${out}" >&2; die "C2 gate-liveness smoke FAILED — validate_backlog did not exit 0, so this environment cannot run the gate mesh"; }
  printf '[provision] C2 smoke: %s\n' "$(printf '%s\n' "${out}" | head -n 1)"
  say "C2 OK — a real gate executed here and returned 0"
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
  assert_hooks_armed || die "L4 git hooks are not armed"

  # The two conditions a RESUMED container can lose without any pin moving: a repo re-cloned or
  # re-fetched into a branch-only shape, and a gitignored ecosystem/ wiped by a rebuild. Both are
  # asserted, never repaired — `--gate` refuses; provisioning is what fixes.
  uv run --locked python scripts/cloud_provisioning.py history --quiet \
    || die "L4 the refs a spine-walking instrument reads do not resolve — re-provision (bash .devcontainer/provision.sh)"
  uv run --locked python scripts/cloud_provisioning.py ecosystem --quiet \
    || die "L4 no repo is registered under ecosystem/ — audit.py health cannot pass here; re-provision"

  say "gate OK — uv ${have_uv}, full history + spine refs, ecosystem registered, three hook types armed, stamp current"
}

usage() {
  cat <<'USAGE'
Usage: bash .devcontainer/provision.sh [--gate|--help]

  (no args)  Provision this container and ASSERT all four [#554] legs plus the
             history-sufficiency (B1) and ecosystem-registration (L5) legs, run the
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

  # ORDER IS LOAD-BEARING. leg2b/leg5 need the venv, so they follow sync_environment; both
  # precede leg3_hooks, so nothing that walks a spine or reads ecosystem/ can be reached by a
  # hook before its precondition has been repaired.
  say "provisioning ${REPO_ROOT}"
  leg1_uv
  leg2_unshallow
  sync_environment
  leg2b_history
  leg5_ecosystem
  leg3_hooks
  smoke_gate_liveness
  write_stamp

  if [ "${CHANGED}" -eq 0 ]; then
    say "DONE — idempotent: nothing changed, all four legs were already satisfied (second run is a no-op)"
  else
    say "DONE — ${CHANGED} leg(s) acted; all four legs assert clean and a real gate ran here"
  fi
}

main "$@"
