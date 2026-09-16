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

import re
import shutil
import subprocess
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PROVISION_SH = _REPO_ROOT / ".devcontainer" / "provision.sh"

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
        "leg2b_history", "leg5_ecosystem", "leg3_hooks", "leg_f1_claude",
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

    def digest() -> str:
        run = subprocess.run(["bash", str(harness)], capture_output=True, text=True, timeout=60)
        assert run.returncode == 0, run.stderr
        return run.stdout.strip()

    before = digest()
    assert before, "no digest tool on PATH would make the hand-over silently unreachable"
    assert digest() == before, "the digest is not stable across two reads of one file"
    target.write_text("#!/usr/bin/env bash\n# replaced by a fast-forward\n", encoding="utf-8")
    assert digest() != before
