"""[#664]/[#746] guards `.devcontainer/provision.sh` against the two shapes that broke a container.

`safe_remove`'s static importer scan cannot see a referrer that names a module by file path
(`scripts/<name>.py` in a shell command) rather than by `import` — which is how six call sites
naming the retired `scripts/cloud_provisioning.py` survived that module's own deletion at
`3c9418cc` ([#734]) and false-PASSed as safe. `test_provision_sh_names_no_retired_module_path`
asserts that class stays closed going forward: provision.sh must never name a `scripts/*.py`
path that is not on disk.

[#746] ADDS THE SECOND HALF, and it is the half the outage actually turned on. Closing the class
"provision.sh names a path that does not exist" does nothing about "provision.sh is not the file
that is running" — witnessed 2026-09-14 23:37Z, `lane-z-substrate-probe`'s creation.log: the
image snapshot carried a `provision.sh` at `1059d04d` (1401 commits behind), `refresh_source_tree`
fast-forwarded the TREE to `b5270d63`, and the already-running bash went on executing the stale
body it had already read, reached the pre-[#664] `leg2b_history`, and killed the container into a
recovery container. A gate that reads the file on disk is blind to that by construction, so what
is asserted here instead is that the script HANDS OVER to the refreshed copy.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PROVISION_SH = _REPO_ROOT / ".devcontainer" / "provision.sh"

#: Bash spawn budget for the login-path test: it starts four bash processes and took 48 s alone on
#: a Windows host, so the old 30 s / 60 s budgets read as a failure on a loaded box while the same
#: test passed on the Codespace (b2-codespace-green run 7; the failing run kept only a verdict,
#: so a timeout is the likely cause, not a proven one).
_BASH_SPAWN_TIMEOUT_S = 240

#: Matches an actual invocation, not a prose mention of the path — this file's own
#: retirement-record comments cite retired paths by name deliberately.
#:
#: WIDENED [#746]. The [#664] version matched `python scripts/<name>.py` only, so three
#: spellings that produce the identical `[Errno 2]` slipped straight through: `python3 …`
#: (which is what the container's own `.venv/bin/python3` is, and exactly what the creation.log
#: recorded), a `-m scripts.<name>` module invocation, and a bare `scripts/<name>.py` run
#: through its shebang. A guard against "names a path that is not there" that only recognises
#: one of four ways to name it is a guard against a spelling.
_INVOCATION_RE = re.compile(
    r"""(?:
          \bpython[0-9.]*\s+(?P<path>scripts/[A-Za-z0-9_]+\.py)   # python / python3 scripts/x.py
        | \bpython[0-9.]*\s+-m\s+scripts\.(?P<mod>[A-Za-z0-9_]+)  # python -m scripts.x
        | (?<![-\w/])(?P<bare>scripts/[A-Za-z0-9_]+\.py)\b        # bare scripts/x.py (shebang)
        )""",
    re.X,
)


def _named_scripts(text: str) -> set[str]:
    """Every `scripts/<name>.py` the text actually INVOKES, in any of the three spellings."""
    named: set[str] = set()
    for match in _INVOCATION_RE.finditer(text):
        if match.group("path"):
            named.add(match.group("path").split("/", 1)[1])
        elif match.group("mod"):
            named.add(f"{match.group('mod')}.py")
        else:
            named.add(match.group("bare").split("/", 1)[1])
    return named


def _uncommented(text: str, marker: str = "#") -> str:
    """`text` with whole-line comments dropped.

    provision.sh explains the defects it closed by QUOTING them, so a naive substring search
    finds a retired declaration in the prose that records its retirement. Stripping comment
    lines is what makes these assertions about the code rather than about the commentary.
    """
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith(marker))


def _working_bash() -> str:
    """The first `bash` -- on PATH, else beside git -- that actually runs a command.

    `shutil.which("bash")` returns the first PATH hit, and on a Windows workstation that is
    `...\\WindowsApps\\bash.EXE` -- the WSL launcher, which prints "no installed distributions"
    in UTF-16 and exits 1 -- ahead of Git Bash. The two tests that RUN bash then failed here
    and passed in a Codespace (`codespace_parity.py` condition 2, 2026-10-03), a verdict that
    came from the machine's PATH, not from the code. Each candidate is probed; none working is
    a loud failure, never a silent skip.
    """
    candidates = [shutil.which("bash", path=d) for d in os.environ.get("PATH", "").split(os.pathsep)
                  if d]
    git = shutil.which("git")
    if git:  # Git for Windows ships bash beside git even when its `bin` is not on PATH
        root = Path(git).resolve().parent.parent
        candidates += [str(root / "bin" / "bash.exe"), str(root / "usr" / "bin" / "bash.exe")]
    for candidate in candidates:
        if candidate is None or not Path(candidate).is_file():
            continue
        try:
            probe = subprocess.run([candidate, "-c", "echo bash-ok"], capture_output=True,
                                   text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if probe.returncode == 0 and probe.stdout.strip() == "bash-ok":
            return candidate
    raise AssertionError("no bash on PATH can run a command (a WSL launcher with no "
                         "distribution does not count)")


def _bash_function(text: str, name: str) -> str:
    """The body of one bash function, bounded at its closing brace.

    Splitting on `f"{name}() {{"` and taking the tail reaches the END OF THE FILE, so an
    assertion about one function is silently satisfiable by any later one (terra HIGH round 6,
    2026-08-21). Bash formatting here is uniform: a top-level function closes with `}` at
    column 0.
    """
    after = text.split(f"{name}() {{", 1)[1]
    return after[:after.index("\n}")]


# --- the [#664] class: a path that is not on disk -------------------------------------------


def test_provision_sh_names_no_retired_module_path():
    text = _PROVISION_SH.read_text(encoding="utf-8")
    named = _named_scripts(_uncommented(text))
    missing = sorted(name for name in named if not (_REPO_ROOT / "scripts" / name).exists())
    assert not missing, f"provision.sh invokes retired scripts/ path(s): {missing}"


def test_the_guard_recognises_every_spelling_of_an_invocation():
    """The guard above is only as good as what it can SEE, so what it sees is pinned.

    A guard whose regex misses `python3 scripts/x.py` would have watched the measured failure go
    past — `.venv/bin/python3` is the interpreter the creation.log names — and reported clean.
    """
    assert _named_scripts("uv run --no-sync python scripts/gone.py history") == {"gone.py"}
    assert _named_scripts("uv run --no-sync python3 scripts/gone.py history") == {"gone.py"}
    assert _named_scripts("/workspaces/dev-knowledge/.venv/bin/python3 scripts/gone.py") == {"gone.py"}
    assert _named_scripts("uv run python -m scripts.gone check") == {"gone.py"}
    assert _named_scripts("bash scripts/gone.py") == {"gone.py"}
    # A DOC path in the same shape is not an invocation and must not be read as one.
    assert _named_scripts("see tests/test_gone.py for why") == set()


# --- the [#746] legs: B1 history sufficiency and L5 ecosystem registration -------------------


def test_provision_sh_wires_both_restored_legs():
    """[#746]: the legs are wired to the module that implements them, by both call shapes.

    RED before the restoration — `[#664]` removed `leg2b_history` and `leg5_ecosystem` outright
    and provisioning has asserted neither since `3c9418cc`.
    """
    code = _uncommented(_PROVISION_SH.read_text(encoding="utf-8"))
    for leg, subcommand in (("leg2b_history", "history"), ("leg5_ecosystem", "ecosystem")):
        body = _bash_function(code, leg)
        assert f"provision_legs.py --quiet {subcommand}" in body, leg
        assert f"provision_legs.py {subcommand} --repair" in body, leg


def test_provision_sh_asks_before_repairing_so_c1_accounting_stays_honest():
    """A run that repairs must not report itself idempotent.

    Witnessed 2026-08-21: the first live container run seeded a state.yaml and still printed
    "DONE — idempotent: nothing changed". Each leg runs the read-only check FIRST and bumps
    CHANGED on its verdict.
    """
    code = _uncommented(_PROVISION_SH.read_text(encoding="utf-8"))
    for subcommand in ("history", "ecosystem"):
        assert f"provision_legs.py --quiet {subcommand} || CHANGED=" in code
        assert code.index(f"provision_legs.py --quiet {subcommand}") < \
               code.index(f"provision_legs.py {subcommand} --repair")


def test_the_gate_asserts_both_legs_read_only():
    """`--gate` (postStartCommand) ASSERTS; it never repairs. A resumed container can lose both
    conditions without any pin moving — a repo re-fetched into a branch-only shape, and a
    gitignored `ecosystem/` wiped by a rebuild — so the gate refuses and provisioning fixes."""
    code = _uncommented(_PROVISION_SH.read_text(encoding="utf-8"))
    gate = _bash_function(code, "gate")
    assert "provision_legs.py --quiet history" in gate
    assert "provision_legs.py --quiet ecosystem" in gate
    assert "--repair" not in gate, "the gate must assert, never repair"


def test_provision_sh_runs_the_history_repair_before_arming_hooks():
    """B1's ordering claim is checkable, so it is checked rather than asserted in prose.

    The FULL sequence, not just the two restored legs (terra HIGH round 3, 2026-08-21): an
    earlier version asserted only relative order, so deleting `leg1_uv`, `leg2_unshallow` or
    `write_stamp` from main() left the suite green while a fresh container provisioned nothing.

    Honest limit, stated so nobody reads more into this than it does: this asserts the CALL
    LIST, not the behaviour of each leg. What stands in for executing the whole script is the
    live container evidence in this lane's end-of-lane artifact.
    """
    body = _uncommented(_bash_function(_PROVISION_SH.read_text(encoding="utf-8"), "main"))
    steps = [ln.strip() for ln in body.splitlines()
             if ln.strip().startswith("leg")
             or ln.strip() in ("refresh_source_tree", "sync_environment",
                               "smoke_gate_liveness", "write_stamp")]
    assert steps == [
        "leg1_uv", "leg2_unshallow", "refresh_source_tree", "sync_environment",
        "leg2b_history", "leg5_ecosystem", "leg3_hooks", "leg_pc_login_path", "leg_f1_claude",
        # b2w2-codespace-finish (R87.3): codex's subscription policy and the login-shell key unset
        # land BEFORE the first leg that starts a codex process (`scrub_model_keys` is the prologue)
        "leg_f6_codex_subscription",
        # foundation-13: the lane's toolset, pinned and asserted, after the agent feature's own assert
        "leg_f5_claude_pin", "leg_f5_gh", "leg_f5_codex", "leg_f5_rclone", "leg_f5_agy",
        # b2-codespace-1to1 (R63): the fourth model CLI, after the other three
        "leg_f5_grok",
        # b2-codespace-subscription-auth: the model CLI the registry names that had no leg
        # (b2w2-codespace-finish, R88b: its sibling `leg_f5_gemini` was removed with the gemini CLI)
        "leg_f5_copilot",
        "leg_f2_git_credential", "leg_f4_workspace_trust", "smoke_gate_liveness", "write_stamp",
        # L1 ([#554]) is LAST, and the position is the claim: the provenance marker records what
        # is LIVE, so every tool it names must already be installed when it is written. Anywhere
        # before `leg_f1_claude` it would record `claude: null` on a container that has one, and
        # a marker that under-reports the substrate refuses a healthy container at the next
        # lane's step 0 — the noise direction a refusal gate cannot afford.
        "leg_l1_provenance",
    ]


# --- the [#746] class: the script is not the file that is running ---------------------------


def test_refresh_source_tree_hands_over_to_the_refreshed_script():
    """THE MEASURED OUTAGE, closed at its cause.

    `refresh_source_tree` fast-forwards the checkout, which can replace `provision.sh` itself —
    and bash goes on executing the body it already read. On 2026-09-14 that body was 1401 commits
    old and called a module retired 12 days earlier, so the container died into a recovery
    container even though the tree on disk was, by then, entirely correct.

    Asserted: the function compares its own bytes across the fast-forward and `exec`s the new
    copy when they differ, guarded so it can happen at most once.
    """
    code = _uncommented(_PROVISION_SH.read_text(encoding="utf-8"))
    body = _bash_function(code, "refresh_source_tree")
    assert "exec" in body, "a refreshed provision.sh is never handed control"
    assert "REEXEC" in body, "the hand-over has no once-only guard, so it can loop"


def test_the_handover_guard_is_exported_so_the_new_process_can_see_it():
    """A once-only guard that is not EXPORTED is not a guard: `exec` replaces the process image
    and a plain shell variable does not survive it, so the successor would re-exec forever."""
    code = _uncommented(_PROVISION_SH.read_text(encoding="utf-8"))
    assert re.search(r"export\s+DEV_KNOWLEDGE_PROVISION_REEXEC", code), "not exported"


# --- the WAVE5B-N2 repair-1 class: pre-commit exists in the venv but is invisible to a fresh
# login shell, which is what the codespace admission test actually runs -----------------------


@pytest.mark.skipif(shutil.which("bash") is None, reason="no bash on PATH")
def test_leg_pc_login_path_persists_precommit_onto_a_fresh_shells_path(tmp_path: Path):
    """REFUSED-lane-codespace-proof.md (WAVE5B-N2 repair 1): `.venv/bin/pre-commit` existed
    (`uv sync` installs it, pyproject.toml pins `pre-commit>=4.5`) but a codespace's LOGIN
    shell — the shell the admission test runs `command -v pre-commit` in, right after
    provisioning — has no `.venv/bin` on its PATH; only a shell that already ran `uv run` or
    activated the venv sees it. `pre_commit is not on the login PATH -- a lane that commits
    here would land work past every gate` was the refusal.

    This runs the extracted leg body against a FAKE HOME + FAKE venv (no real container), then
    proves the fix in a SEPARATE, genuine `bash -lc` process — the EXACT invocation the
    codespace admission test runs, and a LOGIN-but-NOT-INTERACTIVE shell. `~/.bashrc` here is
    seeded with the REAL Debian/Ubuntu skeleton's early-return guard
    (`case $- in *i*) ;; *) return;; esac`), which fires for exactly this shell shape and is
    what sank the first version of this leg — it appended to `~/.bashrc` and the terra review
    caught that `bash -lc` never reaches a line below that guard
    (`docs/audits/2026-09-25-codex-codex-lane-codespace-proof-repair-1.md`). A test that
    sourced `~/.bashrc` directly (skipping the guard) or checked only the leg's own process PATH
    would miss that failure entirely.
    """
    text = _PROVISION_SH.read_text(encoding="utf-8")
    body = _bash_function(text, "leg_pc_login_path")
    bash_exe = _working_bash()

    home = tmp_path / "home"
    home.mkdir()
    venv_bin = tmp_path / "repo" / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    fake_pc = venv_bin / "pre-commit"
    fake_pc.write_text("#!/usr/bin/env bash\necho fake-pre-commit\n", encoding="utf-8")
    fake_pc.chmod(0o755)
    # THE REALISTIC GUARD, verbatim from Debian/Ubuntu's /etc/skel/.bashrc. Left untouched by
    # the leg (it must never need to touch ~/.bashrc), and proving it stays untouched is part of
    # what this test checks.
    (home / ".bashrc").write_text(
        "# If not running interactively, don't do anything\n"
        "case $- in\n"
        "    *i*) ;;\n"
        "      *) return;;\n"
        "esac\n"
        "\n"
        "echo 'THIS LINE MUST NEVER RUN UNDER bash -lc' >&2\n"
        "export PATH=\"/this/path/must/never/be/used:$PATH\"\n",
        encoding="utf-8")

    # RESOLVE THE CANONICAL PATH SPELLING THROUGH BASH ITSELF, not `Path.as_posix()`. A real
    # container computes REPO_ROOT via `cd .. && pwd` (top of this file) and every path it ever
    # writes is already POSIX-native — there is no second spelling to reconcile. This dev host
    # is Windows, so `tmp_path.as_posix()` (`C:/Users/.../AppData/Local/Temp/...`) is a spelling
    # bash accepts when RESOLVING a path (`cd`, `ls`) but does not re-derive when a later
    # `export PATH=...` merely copies that string verbatim — MSYS/Cygwin's win->posix path
    # translation runs on specific env vars AT PROCESS STARTUP (HOME among them, confirmed
    # below), never on a value assigned by a running shell. Resolving once through `cd && pwd`
    # gets the SAME canonical form the leg's own `export PATH=...` line will carry, so the two
    # can be compared, and a later shell's PATH search actually finds the file.
    def _canon(p: Path) -> str:
        r = subprocess.run([bash_exe, "-c", f'cd "{p.as_posix()}" && pwd'],
                            capture_output=True, text=True, timeout=_BASH_SPAWN_TIMEOUT_S)
        assert r.returncode == 0, f"could not resolve {p} through bash: {r.stderr!r}"
        return r.stdout.strip()

    home_c = _canon(home)
    repo_root_c = _canon(tmp_path / "repo")
    venv_bin_c = f"{repo_root_c}/.venv/bin"
    fake_pc_c = f"{venv_bin_c}/pre-commit"

    harness = tmp_path / "harness.sh"
    harness.write_text(
        "set -euo pipefail\n"
        f'HOME="{home_c}"\n'
        f'REPO_ROOT="{repo_root_c}"\n'
        'CHANGED=0\n'
        'say() { printf "[t] %s\\n" "$*"; }\n'
        'noop() { printf "[t] %s (no-op)\\n" "$*"; }\n'
        'die() { printf "[t] REFUSED: %s\\n" "$*" >&2; exit 1; }\n'
        f'leg_pc_login_path() {{{body}\n}}\n'
        'leg_pc_login_path\n',
        encoding="utf-8")

    run = subprocess.run([bash_exe, str(harness)], capture_output=True, text=True,
                         timeout=_BASH_SPAWN_TIMEOUT_S)
    assert run.returncode == 0, f"stdout={run.stdout!r} stderr={run.stderr!r}"

    # NOT ~/.bashrc: none of `.bash_profile`/`.bash_login`/`.profile` existed, so the leg must
    # have created `~/.profile` (the documented fallback) — and left the decoy `~/.bashrc`
    # completely alone, since nothing in the real login-shell resolution chain reads it here.
    profile = home / ".profile"
    assert profile.exists(), "the leg must create a real login-startup file when none exists"
    assert venv_bin_c in profile.read_text(encoding="utf-8"), (
        "the leg must persist the venv bin dir onto every login shell's PATH, "
        "not only export it inside its own process")
    bashrc_after = (home / ".bashrc").read_text(encoding="utf-8")
    assert "dev-knowledge provision" not in bashrc_after, (
        "the leg must never touch ~/.bashrc — that file is what sank the first version of "
        "this leg (a non-interactive login shell never reaches a line below its guard)")

    # THE PROOF: a SEPARATE, GENUINE `bash -lc` process — the EXACT invocation the codespace
    # admission test runs — inheriting nothing from this run except HOME and a bare PATH, which
    # is what a fresh login shell has before anything is sourced.
    child_env = dict(os.environ)
    child_env["HOME"] = home_c
    child_env["PATH"] = "/usr/bin:/bin"
    fresh = subprocess.run(
        [bash_exe, "-lc", "command -v pre-commit"],
        capture_output=True, text=True, timeout=_BASH_SPAWN_TIMEOUT_S, env=child_env,
    )
    assert "THIS LINE MUST NEVER RUN UNDER bash -lc" not in fresh.stderr, (
        "the decoy ~/.bashrc ran — the test setup does not isolate what it claims to")
    assert fresh.returncode == 0, (
        f"pre-commit did not resolve in a real `bash -lc` login shell: "
        f"stdout={fresh.stdout!r} stderr={fresh.stderr!r}")
    assert fake_pc_c in fresh.stdout


@pytest.mark.skipif(shutil.which("bash") is None, reason="no bash on PATH")
def test_self_digest_actually_distinguishes_a_replaced_script(tmp_path: Path):
    """The hand-over's PREDICATE, run rather than grepped.

    Everything above reads the file; this runs the real `self_digest` body out of it against a
    copy of provision.sh that is then modified, which is the exact comparison
    `refresh_source_tree` makes across its own fast-forward. A predicate that could not tell the
    two apart would leave the guard permanently silent and nothing static would notice.

    HONEST LIMIT: this proves the predicate, not the `exec`. What stands in for executing the
    whole hand-over is the live container run recorded in this lane's end-of-lane artifact —
    running it here would need git, uv and a remote.
    """
    text = _PROVISION_SH.read_text(encoding="utf-8")
    body = _bash_function(text, "self_digest")

    target = tmp_path / "provision.sh"
    target.write_text("#!/usr/bin/env bash\n# original\n", encoding="utf-8")
    harness = tmp_path / "harness.sh"
    harness.write_text(
        f'set -euo pipefail\nSCRIPT_DIR="{tmp_path.as_posix()}"\nself_digest() {{{body}\n}}\n'
        'self_digest\n',
        encoding="utf-8")

    # The resolved path, not the bare name: on Windows `CreateProcess` finds
    # `System32\bash.exe` (the WSL launcher, which prints "no installed distributions" and
    # exits 1) BEFORE it consults PATH, so a bare "bash" never reaches the Git Bash the skipif
    # above resolved. `_working_bash` walks PATH and probes each hit.
    bash_exe = _working_bash()

    def digest() -> str:
        run = subprocess.run([bash_exe, str(harness)], capture_output=True, text=True, timeout=60)
        assert run.returncode == 0, run.stderr
        return run.stdout.strip()

    before = digest()
    assert before, "no digest tool on PATH would make the hand-over silently unreachable"
    assert digest() == before, "the digest is not stable across two reads of one file"
    target.write_text("#!/usr/bin/env bash\n# replaced by a fast-forward\n", encoding="utf-8")
    assert digest() != before


# --- b2w2-codespace-finish (R87.3, plan M4): codex is signed in by subscription, never a key -------
#
# Launch paths 4 and 5 of the five the plan enumerates (1-3 are in test_dispatch_codespace.py and
# test_codespace_parity.py). Each runs the extracted function bodies in a genuine bash against a
# stub `codex` that records BOOLEANS ONLY -- whether each key variable reached it.

_NEVER_A, _NEVER_B = "SENTINEL-SECRET-CODEX-0001", "SENTINEL-SECRET-OPENAI-0002"
_CODEX_STUB = (
    "#!/usr/bin/env bash\n"
    'rec="${CODEX_STUB_RECORD:?}"\n'
    '{ for n in CODEX_API_KEY OPENAI_API_KEY; do\n'
    '    if [ -n "${!n:-}" ]; then echo "$n=yes"; else echo "$n=no"; fi\n'
    '  done; echo "argv=$*"; } >> "$rec"\n'
    'echo "codex-cli 0.0.0"\n'
)


def _stub_dir(bash_exe: str, tmp_path: Path) -> tuple[str, Path, str]:
    """(the stub's directory spelled as bash sees it, the record file, the record spelled for bash)."""
    stub_dir = tmp_path / "stubbin"
    stub_dir.mkdir()
    stub = stub_dir / "codex"
    stub.write_text(_CODEX_STUB, encoding="utf-8", newline="\n")
    stub.chmod(0o755)
    record = tmp_path / "record.txt"
    return _canon_path(bash_exe, stub_dir), record, _canon_path(bash_exe, tmp_path) + "/record.txt"


def _canon_path(bash_exe: str, p: Path) -> str:
    r = subprocess.run([bash_exe, "-c", f'cd "{p.as_posix()}" && pwd'], capture_output=True, text=True,
                       timeout=_BASH_SPAWN_TIMEOUT_S)
    assert r.returncode == 0, f"could not resolve {p} through bash: {r.stderr!r}"
    return r.stdout.strip()


def _saw(record: Path) -> dict:
    out = {}
    for line in record.read_text(encoding="utf-8").splitlines():
        key, _, value = line.partition("=")
        out[key] = value
    return out


def test_main_scrubs_the_model_keys_first_and_writes_the_codex_policy_before_any_codex_call():
    code = _uncommented(_bash_function(_PROVISION_SH.read_text(encoding="utf-8"), "main"))
    calls = [ln.strip() for ln in code.splitlines() if ln.strip() and not ln.strip().startswith(("say", "case"))]
    assert "scrub_model_keys" in calls and "leg1_uv" in calls
    assert calls.index("scrub_model_keys") < calls.index("leg1_uv"), "the scrub is the prologue"
    assert calls.index("leg_f6_codex_subscription") < calls.index("leg_f5_codex"), (
        "the login shells that probe codex's version must already unset the keys")


def test_provision_scrubs_the_keys_before_any_child_it_starts(tmp_path: Path):
    """Launch path 5: the processes provision.sh itself starts (`provision_legs.py tools check` runs
    `codex --version`, `uv run`, the hooks) inherit its environment. Seeded with both keys, a child
    started after `scrub_model_keys` sees neither, and sees both without it -- the control that shows
    the harness isolates what it claims to.

    WHAT THIS DOES NOT CLAIM, and why: a LOGIN shell child (`bash -lc`) re-reads the login chain, and in
    a real Codespace that chain re-exports the user secrets from
    /workspaces/.codespaces/shared/user-secrets-envs.json no matter what the parent unset. The first
    version of this test asserted that too; the live parity run's gates leg (2026-10-09, Codespace
    `b2w2-codespace-finish-parity-...`) failed it there and passed it on the laptop, and a login shell
    under a bare HOME printed `CODEX_API_KEY=yes` while the real HOME, carrying leg_f6's block, printed
    `no`. So the login-shell guarantee belongs to `leg_f6_codex_subscription`, tested by launch path 4,
    and this test states only what the scrub itself guarantees.
    """
    bash_exe = _working_bash()
    body = _bash_function(_PROVISION_SH.read_text(encoding="utf-8"), "scrub_model_keys")
    home = tmp_path / "home"
    home.mkdir()
    stub_c, record, record_c = _stub_dir(bash_exe, tmp_path)
    home_c = _canon_path(bash_exe, home)
    probe = "bash -c 'command -v codex >/dev/null 2>&1 && codex --version'"

    def run(with_scrub: bool) -> dict:
        record.unlink(missing_ok=True)
        harness = tmp_path / "harness.sh"
        harness.write_text(
            "set -euo pipefail\n"
            f'HOME="{home_c}"\n'
            f'export PATH="{stub_c}:$PATH"\n'
            'say() { printf "[t] %s\\n" "$*"; }\n'
            f"scrub_model_keys() {{{body}\n}}\n"
            + ("scrub_model_keys\n" if with_scrub else "")
            + f"{probe}\n", encoding="utf-8", newline="\n")
        env = {**os.environ, "HOME": home_c, "CODEX_API_KEY": _NEVER_A, "OPENAI_API_KEY": _NEVER_B,
               "CODEX_STUB_RECORD": record_c}
        res = subprocess.run([bash_exe, str(harness)], env=env, capture_output=True, text=True,
                             timeout=_BASH_SPAWN_TIMEOUT_S)
        assert res.returncode == 0, (res.stdout, res.stderr)
        assert _NEVER_A not in res.stdout + res.stderr and _NEVER_B not in res.stdout + res.stderr
        if with_scrub:
            assert "CODEX_API_KEY was set" in res.stdout, "the scrub says which NAME it removed"
        return _saw(record)

    assert run(with_scrub=False)["CODEX_API_KEY"] == "yes", "control: without the scrub the key arrives"
    seen = run(with_scrub=True)
    assert seen["CODEX_API_KEY"] == "no" and seen["OPENAI_API_KEY"] == "no"


def test_leg_f6_makes_every_login_shell_unset_the_keys_and_forces_the_chatgpt_sign_in(tmp_path: Path):
    """Launch path 4. The Codespaces secrets are exported by the login chain before `~/.profile`
    (simulated here by exporting them FIRST in `~/.profile`); the leg's marked block comes after and
    removes them, so a login shell -- the shell every lane head runs in -- hands `codex` neither.
    The same leg forces the ChatGPT sign-in in `~/.codex/config.toml`, merging into an existing
    file and idempotent on a second run."""
    bash_exe = _working_bash()
    body = _bash_function(_PROVISION_SH.read_text(encoding="utf-8"), "leg_f6_codex_subscription")
    home = tmp_path / "home"
    (home / ".codex").mkdir(parents=True)
    stub_c, record, record_c = _stub_dir(bash_exe, tmp_path)
    home_c = _canon_path(bash_exe, home)
    (home / ".profile").write_text(
        f'export PATH="{stub_c}:$PATH"\n'
        f"export CODEX_API_KEY={_NEVER_A}\nexport OPENAI_API_KEY={_NEVER_B}\n",
        encoding="utf-8", newline="\n")
    existing = '[projects."/workspaces/x"]\ntrust_level = "trusted"\n'
    (home / ".codex" / "config.toml").write_text(existing, encoding="utf-8", newline="\n")

    def login_probe() -> dict:
        record.unlink(missing_ok=True)
        env = {**os.environ, "HOME": home_c, "PATH": "/usr/bin:/bin", "CODEX_STUB_RECORD": record_c}
        res = subprocess.run([bash_exe, "-lc", "codex login status"], env=env, capture_output=True,
                             text=True, timeout=_BASH_SPAWN_TIMEOUT_S)
        assert res.returncode == 0, (res.stdout, res.stderr)
        return _saw(record)

    assert login_probe()["CODEX_API_KEY"] == "yes", "control: the login chain exports the secrets"

    def run_leg() -> str:
        harness = tmp_path / "harness.sh"
        harness.write_text(
            "set -euo pipefail\n"
            f'HOME="{home_c}"\nPATH="{_python3_dir(bash_exe, tmp_path)}:$PATH"\nCHANGED=0\n'
            'say() { printf "[t] %s\\n" "$*"; }\n'
            'noop() { printf "[t] %s (no-op)\\n" "$*"; }\n'
            'die() { printf "[t] REFUSED: %s\\n" "$*" >&2; exit 1; }\n'
            f"leg_f6_codex_subscription() {{{body}\n}}\n"
            "leg_f6_codex_subscription\n", encoding="utf-8", newline="\n")
        res = subprocess.run([bash_exe, str(harness)], capture_output=True, text=True,
                             timeout=_BASH_SPAWN_TIMEOUT_S)
        assert res.returncode == 0, (res.stdout, res.stderr)
        return res.stdout

    run_leg()
    seen = login_probe()
    assert seen["CODEX_API_KEY"] == "no" and seen["OPENAI_API_KEY"] == "no"
    config = (home / ".codex" / "config.toml").read_text(encoding="utf-8")
    assert config.splitlines()[0] == 'forced_login_method = "chatgpt"', "a top-level key precedes every table"
    assert config.endswith(existing), "the existing config is merged into, never replaced"
    profile_once = (home / ".profile").read_text(encoding="utf-8")
    again = run_leg()
    assert "(no-op)" in again
    assert (home / ".codex" / "config.toml").read_text(encoding="utf-8") == config
    assert (home / ".profile").read_text(encoding="utf-8") == profile_once, "the marked block is added once"


def test_leg_f6_rewrites_a_forced_api_login_and_keeps_the_rest_of_the_file(tmp_path: Path):
    bash_exe = _working_bash()
    body = _bash_function(_PROVISION_SH.read_text(encoding="utf-8"), "leg_f6_codex_subscription")
    home = tmp_path / "home"
    (home / ".codex").mkdir(parents=True)
    home_c = _canon_path(bash_exe, home)
    cfg = home / ".codex" / "config.toml"
    cfg.write_text('model = "x"\nforced_login_method = "api"\n[tui]\nnotifications = true\n',
                   encoding="utf-8", newline="\n")
    harness = tmp_path / "harness.sh"
    harness.write_text(
        "set -euo pipefail\n"
        f'HOME="{home_c}"\nPATH="{_python3_dir(bash_exe, tmp_path)}:$PATH"\nCHANGED=0\n'
        'say() { printf "[t] %s\\n" "$*"; }\n'
        'noop() { printf "[t] %s (no-op)\\n" "$*"; }\n'
        'die() { printf "[t] REFUSED: %s\\n" "$*" >&2; exit 1; }\n'
        f"leg_f6_codex_subscription() {{{body}\n}}\n"
        "leg_f6_codex_subscription\n", encoding="utf-8", newline="\n")
    res = subprocess.run([bash_exe, str(harness)], capture_output=True, text=True,
                         timeout=_BASH_SPAWN_TIMEOUT_S)
    assert res.returncode == 0, (res.stdout, res.stderr)
    assert cfg.read_text(encoding="utf-8") == (
        'model = "x"\nforced_login_method = "chatgpt"\n[tui]\nnotifications = true\n')


# --- b2w3 close-out review (Codex gpt-6-astra, 2026-10-10), HIGH: L-F6 ignored TOML scope --------
#
# RED on 2fee6fce: the leg proved `forced_login_method = "chatgpt"` with a whole-file `grep -Fx` and
# rewrote with a whole-file `sed`, so the same text inside a `[table]` or a multiline string passed
# as the TOP-LEVEL policy (provisioning reported success with the policy absent) and a sed hit
# inside a string or table corrupted unrelated settings. The leg now parses the file (tomllib),
# edits only the top-level key, re-parses, and refuses rather than claim a result it cannot show.

_F6_KEY = "forced_login_method"


def _python3_dir(bash_exe: str, tmp_path: Path) -> str:
    """A directory holding a `python3` that is THIS interpreter (tomllib, 3.11+), spelled for bash.

    The leg runs `python3` as the Codespace image provides it; a workstation's PATH may carry none,
    an older one, or a Store alias, and a verdict that depends on that is the host's, not the code's.
    """
    import sys

    exe = Path(sys.executable)
    bin_dir = tmp_path / "pybin"
    bin_dir.mkdir(exist_ok=True)
    shim = bin_dir / "python3"
    shim.write_text(f'#!/usr/bin/env bash\nexec "{_canon_path(bash_exe, exe.parent)}/{exe.name}" "$@"\n',
                    encoding="utf-8", newline="\n")
    shim.chmod(0o755)
    return _canon_path(bash_exe, bin_dir)


def _run_f6(tmp_path: Path, config: str | None, *, again: bool = False):
    """Run the leg in a genuine bash over `tmp_path/home`; `again=True` re-runs over what is there."""
    bash_exe = _working_bash()
    body = _bash_function(_PROVISION_SH.read_text(encoding="utf-8"), "leg_f6_codex_subscription")
    home = tmp_path / "home"
    cfg = home / ".codex" / "config.toml"
    if not again:
        (home / ".codex").mkdir(parents=True)
        if config is not None:
            cfg.write_bytes(config.encode("utf-8"))
    home_c = _canon_path(bash_exe, home)
    py_c = _python3_dir(bash_exe, tmp_path)
    harness = tmp_path / "harness.sh"
    harness.write_text(
        "set -euo pipefail\n"
        f'HOME="{home_c}"\nPATH="{py_c}:$PATH"\nCHANGED=0\n'
        'say() { printf "[t] %s\\n" "$*"; }\n'
        'noop() { printf "[t] %s (no-op)\\n" "$*"; }\n'
        'die() { printf "[t] REFUSED: %s\\n" "$*" >&2; exit 1; }\n'
        f"leg_f6_codex_subscription() {{{body}\n}}\n"
        "leg_f6_codex_subscription\n", encoding="utf-8", newline="\n")
    res = subprocess.run([bash_exe, str(harness)], capture_output=True, text=True,
                         timeout=_BASH_SPAWN_TIMEOUT_S)
    return res, cfg


def _toml(text: str) -> dict:
    import tomllib

    return tomllib.loads(text)


def test_leg_f6_does_not_mistake_a_nested_table_for_the_top_level_policy(tmp_path: Path):
    """The same key under a `[table]` is a different setting: the top-level one must still be added."""
    existing = f'[profiles.work]\n{_F6_KEY} = "chatgpt"\nmodel = "x"\n'
    res, cfg = _run_f6(tmp_path, existing)
    assert res.returncode == 0, (res.stdout, res.stderr)
    new = cfg.read_text(encoding="utf-8")
    assert _toml(new)[_F6_KEY] == "chatgpt", "the TOP-LEVEL key is now present"
    assert new.endswith(existing), "the nested table is untouched"
    assert "(no-op)" not in res.stdout.split("L-F6 OK")[0], "adding the key is a change, not a no-op"


def test_leg_f6_does_not_mistake_a_multiline_string_for_the_top_level_policy(tmp_path: Path):
    existing = f'notes = """\n{_F6_KEY} = "chatgpt"\n"""\n'
    res, cfg = _run_f6(tmp_path, existing)
    assert res.returncode == 0, (res.stdout, res.stderr)
    new = cfg.read_text(encoding="utf-8")
    parsed = _toml(new)
    assert parsed[_F6_KEY] == "chatgpt" and parsed["notes"] == f'{_F6_KEY} = "chatgpt"\n'
    assert new.endswith(existing)


def test_leg_f6_rewrites_only_the_top_level_key_not_a_nested_or_quoted_copy(tmp_path: Path):
    existing = (f'notes = """\n{_F6_KEY} = "api"\n"""\n{_F6_KEY} = "api"  \n'
                f'[profiles.work]\n{_F6_KEY} = "api"\nmodel = "x"\n')
    res, cfg = _run_f6(tmp_path, existing)
    assert res.returncode == 0, (res.stdout, res.stderr)
    parsed = _toml(cfg.read_text(encoding="utf-8"))
    assert parsed[_F6_KEY] == "chatgpt"
    assert parsed["notes"] == f'{_F6_KEY} = "api"\n', "a copy inside a string is data, not the setting"
    assert parsed["profiles"]["work"][_F6_KEY] == "api", "a nested table's own setting is left alone"
    assert parsed["profiles"]["work"]["model"] == "x"


def test_leg_f6_keeps_crlf_and_is_idempotent(tmp_path: Path):
    existing = f'{_F6_KEY} = "api"\r\nmodel = "x"\r\n'
    res, cfg = _run_f6(tmp_path, existing)
    assert res.returncode == 0, (res.stdout, res.stderr)
    assert cfg.read_bytes() == f'{_F6_KEY} = "chatgpt"\r\nmodel = "x"\r\n'.encode()
    once = cfg.read_bytes()
    again, _ = _run_f6(tmp_path, None, again=True)
    assert again.returncode == 0, (again.stdout, again.stderr)
    assert cfg.read_bytes() == once and "already forces the ChatGPT sign-in" in again.stdout


def test_leg_f6_refuses_an_invalid_config_and_leaves_it_untouched(tmp_path: Path):
    """A file the leg cannot parse is not one it can safely edit: refuse, say why, change nothing."""
    broken = f'{_F6_KEY} = "api\n[unclosed\n'
    res, cfg = _run_f6(tmp_path, broken)
    assert res.returncode != 0
    assert "REFUSED" in res.stderr and "L-F6" in res.stderr
    assert cfg.read_text(encoding="utf-8") == broken


def test_leg_f6_creates_the_config_when_there_is_none(tmp_path: Path):
    res, cfg = _run_f6(tmp_path, None)
    assert res.returncode == 0, (res.stdout, res.stderr)
    assert _toml(cfg.read_text(encoding="utf-8")) == {_F6_KEY: "chatgpt"}


# --- Codex re-review (gpt-6-astra, 2026-10-10 19:46Z), CRITICAL: the atomic replace widened a config's mode
#
# RED on b6f26d04: `f6_config` wrote its temp file with the default mode (0644 under umask 022) and
# `os.replace`d it over the original, so an existing 0600 `~/.codex/config.toml` -- which may hold
# secret-valued MCP env/header settings -- became world-readable (the old `sed -i` kept the mode).
# The temp file is now created 0600 and takes the ORIGINAL's mode only just before it replaces it
# (0600 for a file that is new), so the new content is never more readable than the original was.
# A Windows interpreter cannot represent 0600, so the first test records the calls the helper makes
# (an order and a value, which is the same on every host) and a POSIX host also reads the real bits.


def _f6_config_source() -> str:
    """The python the leg pipes to `python3 -` (heredoc body of the nested `f6_config`)."""
    text = _PROVISION_SH.read_text(encoding="utf-8")
    opener = "python3 - \"$@\" <<'PY'\n"
    start = text.index(opener, text.index("f6_config() {")) + len(opener)
    return text[start:text.index("\nPY\n", start) + 1]


def _run_f6_config_recording(cfg: Path, monkeypatch) -> list[tuple]:
    """Run `f6_config ensure <cfg>` in-process, recording its os.open / os.chmod / os.replace calls."""
    import io
    import sys

    events: list[tuple] = []
    real_open, real_chmod, real_replace = os.open, os.chmod, os.replace

    def rec_open(path, flags, mode=0o777, **kw):
        events.append(("open", str(path), mode))
        return real_open(path, flags, mode, **kw)

    def rec_chmod(path, mode, **kw):
        events.append(("chmod", str(path), mode))
        return real_chmod(path, mode, **kw)

    def rec_replace(src, dst, **kw):
        events.append(("replace", str(src), str(dst)))
        return real_replace(src, dst, **kw)

    out = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
    with monkeypatch.context() as m:
        m.setattr(os, "open", rec_open)
        m.setattr(os, "chmod", rec_chmod)
        m.setattr(os, "replace", rec_replace)
        m.setattr(sys, "argv", ["-", "ensure", str(cfg)])
        m.setattr(sys, "stdout", out)
        with pytest.raises(SystemExit) as stop:
            exec(compile(_f6_config_source(), "f6_config.py", "exec"), {"__name__": "__main__"})
    assert stop.value.code in (0, None), stop.value.code
    return events


def test_f6_config_writes_a_private_temp_file_and_restores_the_originals_mode_before_replacing(
        tmp_path: Path, monkeypatch):
    import stat

    cfg = tmp_path / "config.toml"
    cfg.write_bytes(f'{_F6_KEY} = "api"\nmodel = "x"\n'.encode())
    os.chmod(cfg, 0o640)
    original_mode = stat.S_IMODE(os.stat(cfg).st_mode)   # what THIS host can represent of 0o640

    events = _run_f6_config_recording(cfg, monkeypatch)

    kinds = [e[0] for e in events]
    assert kinds == ["open", "chmod", "replace"], events
    (_, tmp_name, open_mode), (_, chmod_target, chmod_mode), (_, replaced, destination) = events
    assert open_mode == 0o600, "the temp file is created private: never more readable than the original"
    assert tmp_name == chmod_target == replaced and tmp_name.startswith(str(cfg) + ".tmp.")
    assert destination == str(cfg)
    assert chmod_mode == original_mode, "it takes the original's mode just before it replaces it"
    assert _toml(cfg.read_text(encoding="utf-8"))[_F6_KEY] == "chatgpt"
    if os.name != "nt":   # a POSIX host can read the real bits back (CI Linux, the Codespace)
        assert stat.S_IMODE(os.stat(cfg).st_mode) == 0o640


def test_f6_config_makes_a_new_file_private(tmp_path: Path, monkeypatch):
    import stat

    cfg = tmp_path / "config.toml"
    events = _run_f6_config_recording(cfg, monkeypatch)
    assert [e[0] for e in events] == ["open", "chmod", "replace"], events
    assert events[0][2] == 0o600 and events[1][2] == 0o600
    assert _toml(cfg.read_text(encoding="utf-8")) == {_F6_KEY: "chatgpt"}
    if os.name != "nt":
        assert stat.S_IMODE(os.stat(cfg).st_mode) == 0o600


def test_a_parity_version_probe_is_keyless_even_when_a_login_shell_exports_the_keys(tmp_path: Path):
    """Done 2 on the parity side (Codex Critical, 2026-10-10). The probe is `bash -lc`, so a profile
    that exports the secrets AFTER the parent's env was scrubbed re-injects them -- the old probe
    printed codex's version with both keys set. The stub records BOOLEANS only; the sentinels
    must also never appear in anything the probe printed."""
    import sys

    sys.path.insert(0, str(_REPO_ROOT))
    from scripts import codespace_parity as cp

    bash_exe = _working_bash()
    home = tmp_path / "home"
    home.mkdir()
    stub_c, record, record_c = _stub_dir(bash_exe, tmp_path)
    home_c = _canon_path(bash_exe, home)
    (home / ".profile").write_text(
        f'export PATH="{stub_c}:$PATH"\n'
        f"export CODEX_API_KEY={_NEVER_A}\nexport OPENAI_API_KEY={_NEVER_B}\n",
        encoding="utf-8", newline="\n")
    env = {**os.environ, "HOME": home_c, "PATH": "/usr/bin:/bin", "CODEX_STUB_RECORD": record_c}

    def probe(argv: list[str]) -> "subprocess.CompletedProcess[str]":
        record.unlink(missing_ok=True)
        res = subprocess.run([bash_exe, *argv[1:]], env=env, capture_output=True, text=True,
                             timeout=_BASH_SPAWN_TIMEOUT_S)
        assert _NEVER_A not in res.stdout + res.stderr and _NEVER_B not in res.stdout + res.stderr
        return res

    control = probe(["bash", "-lc", "command -v codex >/dev/null 2>&1 && codex --version"])
    assert control.returncode == 0 and _saw(record)["CODEX_API_KEY"] == "yes", \
        "control: the login chain re-exports the keys, so an un-guarded probe does reach codex with them"

    argv = cp._tool_probe("codex", posix=True)
    assert argv[0] == "bash" and argv[1] == "-lc"
    res = probe(argv)
    assert res.returncode == 0 and "codex-cli" in res.stdout, (res.stdout, res.stderr)
    seen = _saw(record)
    assert seen["CODEX_API_KEY"] == "no" and seen["OPENAI_API_KEY"] == "no"


# --- foundation-13-codespace-toolset (R63 step 1): the five tool legs ------------------------
#
# RED on origin/main 864b0b9f: provision.sh has no leg for `gh`, `codex`, `rclone`, `agy`, and
# nothing pins `claude`. The container that carried 2.1.272 against the workstation's 2.1.288, and
# no gh/codex/agy/rclone, is `docs/audits/2026-10-03-technical-codespace-parity-run.md` condition 1.

#: leg -> (tool, the install command the tool's OWN documentation names, as it appears in the leg)
_TOOLSET_LEGS = {
    "leg_f5_claude_pin": ("claude", "claude.ai/install.sh"),
    "leg_f5_gh": ("gh", "github.com/cli/cli/releases/download/v${want}"),
    "leg_f5_codex": ("codex", "@openai/codex@${want}"),
    "leg_f5_rclone": ("rclone", "downloads.rclone.org/v${want}"),
    "leg_f5_agy": ("agy", "antigravity.google/cli/install.sh"),
    # b2-codespace-1to1 (R63, operator 2026-10-04: "1:1, all models in sync -- Grok, Codex, Gemini"):
    # xAI's first-party installer, which takes a version (`bash -s <X.Y.Z>`, read 2026-10-04).
    "leg_f5_grok": ("grok", "x.ai/cli/install.sh"),
    # b2-codespace-subscription-auth: the vendor's documented npm install, pinned to the laptop's
    # version (docs.github.com "Install Copilot CLI", read 2026-10-06).
    "leg_f5_copilot": ("copilot", "@github/copilot@${want}"),
}
_VERSION_LITERAL = re.compile(r"(?<![\w.$-])\d+\.\d+\.\d+(?![\w.])")


@pytest.mark.parametrize("leg", sorted(_TOOLSET_LEGS))
def test_each_tool_has_its_own_leg_that_refuses_when_the_tool_is_absent(leg: str):
    code = _uncommented(_PROVISION_SH.read_text(encoding="utf-8"))
    assert f"{leg}()" in code, f"provision.sh has no {leg}"
    body = _bash_function(code, leg)
    tool, method = _TOOLSET_LEGS[leg]
    assert method in body, f"{leg} installs {tool} by something other than its documented method"
    assert "die " in body, f"{leg} must refuse, not log"
    # the ASSERT is the leg: through the LOGIN shell the parity check and admission test use
    assert f"tools check --only {tool} --login" in body, leg


@pytest.mark.parametrize("leg", sorted(_TOOLSET_LEGS))
def test_no_tool_leg_types_a_version(leg: str):
    """N2: the pin is data, written once, never typed twice. A version literal in a leg body is
    a second copy that drifts from `provisioning.yaml`."""
    body = _bash_function(_uncommented(_PROVISION_SH.read_text(encoding="utf-8")), leg)
    assert not _VERSION_LITERAL.findall(body), (leg, _VERSION_LITERAL.findall(body))


@pytest.mark.parametrize("leg", ["leg_f5_claude_pin", "leg_f5_gh", "leg_f5_codex", "leg_f5_rclone",
                                 "leg_f5_agy", "leg_f5_grok", "leg_f5_copilot"])
def test_a_pinned_leg_reads_its_pin_from_the_declaration(leg: str):
    body = _bash_function(_uncommented(_PROVISION_SH.read_text(encoding="utf-8")), leg)
    tool = _TOOLSET_LEGS[leg][0]
    assert f"provision_legs.py tools get {tool}" in body, leg


def test_the_claude_pin_leg_stops_the_container_updating_itself_away_from_the_pin():
    """The pin is worthless if the native updater moves the binary an hour later. The documented
    switch (code.claude.com/docs/en/setup, "Disable auto-updates") is `DISABLE_AUTOUPDATER` in
    settings.json `env`."""
    body = _bash_function(_uncommented(_PROVISION_SH.read_text(encoding="utf-8")),
                          "leg_f5_claude_pin")
    assert "DISABLE_AUTOUPDATER" in body
    assert 'bash "${installer}" "${want}"' in body, \
        "the documented `bash -s <version>` form, run from a script `fetch_installer` has checked"


def test_agy_is_pinned_and_the_leg_asserts_the_pin_its_installer_cannot_honour():
    """b2-codespace-1to1 (R63): `agy`'s installer takes `--dir` and no version, so it installs the
    manifest's latest. The leg therefore cannot SELECT the pin, but it still ASSERTS it -- a
    vendor release that moves past the workstation is then a named refusal, not a silent skew.
    (Before this lane the row read `version: null`, presence only.)"""
    body = _bash_function(_uncommented(_PROVISION_SH.read_text(encoding="utf-8")), "leg_f5_agy")
    assert "tools get agy" in body and "tools check --only agy --login" in body


def test_the_grok_leg_installs_the_pinned_version_and_never_carries_a_credential():
    """The installer's documented forms are `bash -s <version>` (a pin) and `GROK_DEPLOYMENT_KEY=...`
    (a credential). The leg uses the first and never the second: a login is an OPERATOR-ACTION
    (R13, N5), never a key typed into a provisioning script."""
    code = _uncommented(_PROVISION_SH.read_text(encoding="utf-8"))
    body = _bash_function(code, "leg_f5_grok")
    assert 'bash "${installer}" "${want}"' in body, "the version is the installer's first argument"
    for secret in ("GROK_DEPLOYMENT_KEY", "XAI_API_KEY", "GROK_API_KEY", "auth.json"):
        assert secret not in code, f"provision.sh names {secret}: a login is an operator act, not a script's"


def test_a_vendor_installer_is_fetched_checked_to_be_a_script_and_never_piped_into_bash_blind():
    """The first fresh-Codespace run of b2-codespace-1to1 (2026-10-04, creation.log) refused at

        bash: line 1: syntax error near unexpected token `)'
        [provision] REFUSED: L-F5 the Antigravity installer failed

    `curl -fsSL https://antigravity.google/cli/install.sh | bash` had been handed COMPRESSED bytes
    where the script should be, and bash tried to run them. The same line had passed the run
    before. A vendor endpoint that answers differently from one run to the next is not a reason to
    lose a whole container, and a refusal that says 'the installer failed' does not say why: the
    helper asks for the encoding it will accept, retries, refuses anything that is not a `#!`
    script, and names what it got."""
    code = _uncommented(_PROVISION_SH.read_text(encoding="utf-8"))
    helper = _bash_function(code, "fetch_installer")
    assert "--compressed" in helper, "decode what the CDN compresses"
    assert "--retry" in helper
    assert "#!" in helper, "refuse a payload that is not a script"
    assert "first bytes" in helper, "say what was received"
    # the claude leg is in the list on the reviewer's finding (codex terra, 2026-10-04): it still
    # piped `curl | bash -s <version>` straight into a shell, past the check the others now have
    for leg, url in (("leg_f5_agy", "antigravity.google/cli/install.sh"),
                     ("leg_f5_grok", "x.ai/cli/install.sh"),
                     ("leg_f5_claude_pin", "claude.ai/install.sh")):
        body = _bash_function(code, leg)
        assert 'fetch_installer "https://' + url in body, leg
        assert "| bash" not in body, f"{leg} pipes a download into bash unchecked"


def test_no_gemini_leg_tool_row_or_feature_survives_the_registry_dropping_the_cli():
    """R88b, RED-first (b2w2-codespace-finish): the gemini CLI is gone from the registry, so
    `provisioning.yaml` declares no `tools.gemini` / `features.leg_f5_gemini` and `provision.sh`
    installs, calls and asserts nothing for it. A leg left behind would install a CLI nothing
    signs in and would fail the container build on a tool no check expects."""
    import yaml
    code = _uncommented(_PROVISION_SH.read_text(encoding="utf-8"))
    assert "leg_f5_gemini" not in code and "gemini-cli" not in code
    cfg = yaml.safe_load(
        (_REPO_ROOT / ".devcontainer" / "provisioning.yaml").read_text(encoding="utf-8"))
    assert "gemini" not in cfg["tools"]
    assert "leg_f5_gemini" not in (cfg.get("features") or {})


# --- b2w2-codespace-finish (M3, R88c, Done 1): agy -----------------------------------------------
#
# The vendor installer takes no version, so it serves its LATEST. A pin that a vendor release has
# passed cannot be met by this leg; it used to `die`, which turned a container that has agy (and a
# perfectly good toolchain) into a recovery container (heartbeat run 37968009244: "agy is 1.3.2,
# pinned 1.2.17"). The leg still dies when agy does not resolve in a login shell; a version skew is a
# RECORDED state -- present, BLOCKED-AUTH, one OPERATOR-ACTION line -- and parity C1 still names it.

_AGY_HARNESS = (
    "set -uo pipefail\n"
    'say() { printf "[t] %s\\n" "$*"; }\n'
    'noop() { printf "[t] %s (no-op)\\n" "$*"; }\n'
    'die() { printf "[t] REFUSED: %s\\n" "$*" >&2; exit 1; }\n'
    "CHANGED=0\n"
    "UV_BIN_DIR=/nonexistent\n"
    # the pin reader and the version check, answered from the harness's own variables
    "uv() {\n"
    '  case "$*" in\n'
    '    *"tools get agy"*) echo "$PIN" ;;\n'
    '    *"tools check"*) [ "$INSTALLED" = "$PIN" ] ;;\n'
    "  esac\n"
    "}\n"
    "fetch_installer() { echo /dev/null; }\n"
    "ensure_login_resolvable() { :; }\n"
    'login_resolves() { echo "agy is /stub/agy"; }\n'
)


def _run_agy_leg(tmp_path: Path, *, pin: str, installed: str | None) -> subprocess.CompletedProcess:
    bash_exe = _working_bash()
    body = _bash_function(_PROVISION_SH.read_text(encoding="utf-8"), "leg_f5_agy")
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    stub_dir = tmp_path / "stubbin"
    stub_dir.mkdir(exist_ok=True)
    if installed is not None:
        stub = stub_dir / "agy"
        stub.write_text(f'#!/usr/bin/env bash\necho "{installed}"\n', encoding="utf-8", newline="\n")
        stub.chmod(0o755)
    stub_c = _canon_path(bash_exe, stub_dir)
    (home / ".profile").write_text(f'export PATH="{stub_c}:$PATH"\n', encoding="utf-8", newline="\n")
    harness = tmp_path / "agy-harness.sh"
    harness.write_text(_AGY_HARNESS + f"leg_f5_agy() {{{body}\n}}\nleg_f5_agy\n", encoding="utf-8",
                       newline="\n")
    env = {**os.environ, "HOME": _canon_path(bash_exe, home), "PIN": pin,
           "INSTALLED": installed or "", "PATH": stub_c + ":/usr/bin:/bin"}
    return subprocess.run([bash_exe, str(harness)], env=env, capture_output=True, text=True,
                          timeout=_BASH_SPAWN_TIMEOUT_S)


def test_an_agy_skew_is_a_recorded_blocked_auth_state_with_one_operator_action(tmp_path: Path):
    run = _run_agy_leg(tmp_path, pin="1.2.17", installed="1.3.2")
    assert run.returncode == 0, (run.stdout, run.stderr)
    assert "agy 1.3.2 (pin 1.2.17" in run.stdout and "present, BLOCKED-AUTH" in run.stdout
    actions = [ln for ln in run.stdout.splitlines() if "OPERATOR-ACTION:" in ln]
    assert len(actions) == 1 and "sign in to agy in the Codespace once" in actions[0], run.stdout


def test_an_agy_at_its_pin_is_the_ordinary_ok_with_no_operator_action(tmp_path: Path):
    run = _run_agy_leg(tmp_path, pin="1.3.2", installed="1.3.2")
    assert run.returncode == 0, (run.stdout, run.stderr)
    assert "OK" in run.stdout and "OPERATOR-ACTION" not in run.stdout


def test_an_agy_that_does_not_resolve_in_a_login_shell_still_refuses(tmp_path: Path):
    run = _run_agy_leg(tmp_path, pin="1.2.17", installed=None)
    assert run.returncode == 1 and "REFUSED" in run.stderr and "agy" in run.stderr, (run.stdout, run.stderr)


@pytest.mark.parametrize("leg", ["leg_f5_claude_pin", "leg_f5_gh", "leg_f5_codex", "leg_f5_rclone",
                                 "leg_f5_agy", "leg_f5_grok", "leg_f5_copilot"])
def test_a_pre_install_probe_leaves_no_skew_or_absent_line_in_the_container_log(leg: str):
    """Done 1 reads `SKEW`/`ABSENT` lines in the heartbeat log as END states. The probe that decides
    whether to install is not one: its stderr is discarded, so only the final assertion can print them."""
    body = _bash_function(_uncommented(_PROVISION_SH.read_text(encoding="utf-8")), leg)
    tool = _TOOLSET_LEGS[leg][0]
    probes = [ln for ln in body.splitlines() if "--quiet tools check" in ln]
    assert probes, leg
    assert all("2>/dev/null" in ln for ln in probes), (leg, probes)
    assert tool in probes[0]


def test_every_model_cli_and_tool_the_lane_needs_is_pinned_to_an_exact_version():
    """Item 2 of the b2-codespace-1to1 contract: claude, codex, grok, agy, gh and rclone are each an
    exact `x.y.z` string in `provisioning.yaml` `tools:`. RED on `e67f27ac`: no `grok` row, and
    `agy` is `version: null`."""
    import yaml
    tools = yaml.safe_load(
        (_REPO_ROOT / ".devcontainer" / "provisioning.yaml").read_text(encoding="utf-8"))["tools"]
    for name in ("claude", "codex", "grok", "agy", "gh", "rclone", "copilot"):
        assert name in tools, f"{name}: no row in provisioning.yaml tools:"
        version = tools[name].get("version")
        assert isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+", version), (name, version)


def test_tool_legs_follow_the_claude_assert_and_precede_the_provenance_marker():
    """A tool leg that ran before `leg_f1_claude` would install over a feature that has not
    delivered; one that ran after `leg_l1_provenance` would leave the marker under-reporting."""
    body = _uncommented(_bash_function(_PROVISION_SH.read_text(encoding="utf-8"), "main"))
    order = [ln.strip() for ln in body.splitlines() if ln.strip().startswith("leg")]
    legs = list(_TOOLSET_LEGS)
    assert [o for o in order if o in legs] == legs
    assert order.index("leg_f1_claude") < order.index(legs[0])
    assert order.index(legs[-1]) < order.index("leg_l1_provenance")


def test_the_toolset_legs_each_carry_a_library_first_verdict():
    import yaml
    declared = yaml.safe_load(
        (_REPO_ROOT / ".devcontainer" / "provisioning.yaml").read_text(encoding="utf-8"))["features"]
    for leg in _TOOLSET_LEGS:
        assert leg in declared, f"{leg}: no library-first verdict in provisioning.yaml"
