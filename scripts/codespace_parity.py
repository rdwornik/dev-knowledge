#!/usr/bin/env python
"""codespace_parity.py -- "a Codespace lane works" as a repository check, not a lifecycle that
merely completed (`[#1335]`; `to-browser/CODESPACE-PARITY-DEFINITION-2026-10-03.md`; lane
foundation-5-codespace-parity, batch FOUNDATION).

WHAT IT ANSWERS. One real task, run once in a local worktree and once in a Codespace from the same
base sha, must agree on five conditions. This script builds the evidence for each in the
environment it runs in (`collect`), compares two such records (`check`), and prints ONE verdict per
condition -- `PASS`, `FAIL`, or `NOT-RUN <reason>` -- with the two values compared as evidence:

    1 environment   Python, `uv`, the `uv.lock` hash, `uv sync --locked` exit, the versions of the
                    tools a lane needs (`claude`, `gh`, `codex`, `grok`, `agy`), the installed
                    git-hook set -- identical except the OS-specific entries declared below, in
                    code. EACH MODEL CLI ALSO ANSWERS ONE CALL (b2-codespace-1to1, R63): the id it
                    SERVED is read from the tool's own record and must equal what
                    `ecosystem/provider-registry.yaml` routes that CLI's role to (R61) -- a CLI that
                    prints the pinned `--version` and silently serves another model is a FAIL naming
                    both ids. A tool the Codespace has but is not logged in to is a NAMED auth item
                    (`PASS except named auth items: ...`), never a silent exception.
    2 gates         a FIXED set of pre-commit hooks, `audit.py health` and a FIXED pytest
                    selection, same verdict on both sides or a declared OS case with its own row.
    3 landing       same base sha and tree; the Codespace's pushed branch resolves to its HEAD.
                    The integrator leg (local `--no-ff` merge + the CI push verdict) is NOT-RUN:
                    a lane cannot merge, and a check that printed PASS for a leg nobody ran would
                    be the vacuous pass this file exists to refuse.
    4 transport     the Codespace reads the Drive transport by rclone (the secret is checked for
                    PRESENCE only, never read into a record). The write leg is NOT-RUN unless
                    `collect --probe-write NAME` is given (foundation-13): a write probe creates a
                    transport path, so a contract must name the file; it is read back and deleted.
    5 cleanup/cost  after teardown no Codespace is listed and no run branch is on origin; wall
                    time and core-hours are recorded (`codespace_regime.uptime_minutes`, the one
                    uptime formula).

THE NO-VACUOUS-PASS RULE (R59). A Codespace that cannot be created, reached or read, or whose
record is empty, unparseable, the wrong shape, or claims to be the local side (two local records
compared would be green by construction), is a typed failure -- exit 3, `FAILURE
RemoteUnavailable: <why>` -- and every condition prints `NOT-RUN`. No condition that needed the
remote side can print a green verdict. Exit codes: 0 all PASS | 1 at least one FAIL | 2 no FAIL,
at least one NOT-RUN | 3 remote side unavailable | 4 local record unusable.

WHERE THE CODESPACE DRIVER LIVES. Two drivers exist and this file moves neither: win-tooling's
`Dispatch-Codespace` (outside the hub) and the hub's `scripts/dispatch.py` `codespace-*` verbs
(R11(3)). This check needs no agent, so the run is plain `gh codespace create / cp / ssh / delete`;
the only remote read is `gh codespace ssh ... cat` (measured: `cp` has failed this transport three
ways, `cat` fails visibly).

PRIOR-ART CHECK (library-first). stdlib (`json`, `hashlib`, `subprocess`, `xml.etree` for the
pytest junit file) plus the already-declared `click` and `pyyaml` (the registry is read as the YAML
file it is, not through a second parser); `pre-commit` and `pytest` are the existing runners;
`codespace_regime.uptime_minutes` is reused for cost. The served-id probes (b2-codespace-1to1) call
each CLI's own headless mode and read each CLI's own record -- no vendor SDK, no new dependency.

    uv run --locked python scripts/codespace_parity.py collect --out record.json [--push-branch B]
    uv run --locked python scripts/codespace_parity.py check --local l.json --remote r.json
    uv run --locked python scripts/codespace_parity.py check --local l.json --codespace NAME
    uv run --locked python scripts/codespace_parity.py verify-cleanup --codespace NAME ...
"""
from __future__ import annotations

import enum
import hashlib
import json
import logging
import os
import platform
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping, Optional, Sequence

import click
import yaml

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import codespace_regime as _regime
except ImportError:  # pragma: no cover
    import codespace_regime as _regime

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("codespace-parity")

SCHEMA = 1

#: The Codespace side's record, where `collect` writes it and `check --codespace` reads it.
DEFAULT_REMOTE_FILE = "/tmp/parity-remote.json"

# ============================================================ what is declared, in code

#: Where the non-model tools a lane needs (`gh` lands it, `rclone` reads the transport) are DECLARED:
#: the Codespace's own provisioning file. Read at call time so a test can point it elsewhere.
PROVISIONING_PATH = _REPO_ROOT / ".devcontainer" / "provisioning.yaml"

#: The provider registry's own location (the served-id comparison reads it too -- see below).
#: Declared first because the tool sets below are READ from it, never typed (R70, W1-13 item 1).
REGISTRY_PATH = _REPO_ROOT / "ecosystem" / "provider-registry.yaml"


def load_registry(path: Optional[Path] = None) -> dict:
    """The provider registry as a plain mapping; `{}` when it cannot be read (every expected id is
    then absent, which the comparison reports by name rather than skipping)."""
    target = Path(path) if path is not None else REGISTRY_PATH
    try:
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    return data if isinstance(data, dict) else {}


def registry_for(root: Optional[Path] = None) -> dict:
    """The registry under `root` when it has one, else the module's own (`REGISTRY_PATH`)."""
    if root is not None:
        candidate = Path(root) / "ecosystem" / "provider-registry.yaml"
        if candidate.is_file():
            return load_registry(candidate)
    return load_registry()


def model_clis(registry: Optional[Mapping] = None) -> tuple[str, ...]:
    """The CLIs of the registry's providers, in registry order -- the set C1 probes for a served
    model id (R61, R63). READ from `providers:` and never typed: a provider added to the registry
    is probed with no edit here (W1-13 item 1, R70)."""
    registry = load_registry() if registry is None else registry
    out: list[str] = []
    for row in (registry.get("providers") or {}).values():
        cli = row.get("cli") if isinstance(row, Mapping) else None
        if cli and cli not in out:
            out.append(str(cli))
    return tuple(out)


def providers_without_cli(registry: Optional[Mapping] = None) -> tuple[str, ...]:
    """Registry providers that name no CLI (`deepseek` today): nothing to mirror or probe, and said
    so by name instead of being dropped without a word."""
    registry = load_registry() if registry is None else registry
    return tuple(name for name, row in (registry.get("providers") or {}).items()
                 if not (isinstance(row, Mapping) and row.get("cli")))


def declared_tools(path: Optional[Path] = None) -> tuple[str, ...]:
    """The tool names `provisioning.yaml` `tools:` declares -- where `gh` and `rclone` come from,
    since they serve no model and so are not registry providers."""
    target = Path(path) if path is not None else PROVISIONING_PATH
    try:
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return ()
    tools = (data or {}).get("tools") if isinstance(data, dict) else None
    return tuple(str(k) for k in tools) if isinstance(tools, Mapping) else ()


def lane_tools(registry: Optional[Mapping] = None, provisioning: Optional[Path] = None
               ) -> tuple[str, ...]:
    """The tools a lane's close-out needs on EITHER substrate: every registry CLI, then every other
    tool the Codespace declares (`gh` lands the lane, `rclone` reads the transport). A tool absent
    on one side, absent on both, or at two versions is a FAIL naming it."""
    models = model_clis(registry)
    return models + tuple(t for t in declared_tools(provisioning) if t not in models)


def __getattr__(name: str):  # noqa: N807 -- module attribute, resolved at access time
    """`MODEL_CLIS` and `LANE_TOOLS` stay importable names, but they are the registry's answer NOW,
    not tuples frozen when this file was written (b2-codespace-subscription-auth, R70)."""
    if name == "MODEL_CLIS":
        return model_clis()
    if name == "LANE_TOOLS":
        return lane_tools()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

#: Condition-1 manifest entries that legitimately differ by OS, each with its reason. Everything
#: else in the manifest must be equal. `platform` is the OS and CPU by definition.
OS_SPECIFIC_ENTRIES: dict[str, str] = {
    "platform": "the operating system and CPU architecture differ by definition between a "
                "Windows workstation and a Linux container",
}

#: Condition-2 differences forgiven because they are a known OS case with its OWN row: key (a
#: hook id or a pytest node id) -> the row id. Empty on purpose: nothing is pre-forgiven, and an
#: entry without a row id is refused by `declared_cases_problems`.
DECLARED_OS_CASES: dict[str, str] = {}

#: Condition 2's fixed hook set -- the hooks armed at the `pre-commit` stage whose verdict does
#: not depend on the staged diff or the branch name (so the same sha gives the same answer).
GATE_HOOKS: tuple[str, ...] = (
    "codemap-freshness",
    "roster-freshness",
    "claude-rosters-freshness",
    "organ-index-freshness",
    "quality-requirements-freshness",
    "provider-registry-agreement",
)

#: Condition 2's fixed pytest selection: the owned fix sites' own tests plus this check's.
GATE_TESTS: tuple[str, ...] = (
    "tests/test_codespace_parity.py",
    "tests/test_codespace_admission.py",
    "tests/test_codespace_regime.py",
    "tests/test_provision_legs.py",
    "tests/test_provision_sh.py",
)

#: Condition 1's AUTH ITEMS (foundation-13, R63 step 1). Installing a tool does not log it in, and a
#: login or token is something a repository check must neither create nor hide. `collect` records
#: each tool's login state by its own status command (output discarded -- no token can enter a
#: record); `check` then NAMES every tool the Codespace has installed but not authenticated, with
#: what it needs, as `AUTH-ITEM` evidence and in the verdict line. They are exceptions to the
#: environment PASS, never silent ones: condition 1 reads `PASS except named auth items: ...`.
#: `agy` and `grok` have no non-interactive status command, so they are `unprobed` until their model
#: call answers (that call is then the proof of login) and named for that reason otherwise.
AUTH_PROBES: dict[str, Optional[tuple[str, ...]]] = {
    "claude": ("claude", "auth", "status"),
    "gh": ("gh", "auth", "status"),
    # `codex login status` reads the ChatGPT login only: it printed "Not logged in" on a Codespace
    # whose `CODEX_API_KEY` answered every call (night leg 5, D9), so C1 named codex an auth item
    # on every run. Like grok and agy it has no status command that tells the truth; its served-id
    # call is the proof of login (`_fold_model_proof_into_auth`).
    "codex": None,
    "grok": None,
    "agy": None,
    # a CLI the registry names that has no status command is `unprobed` until its served-id call
    # answers; `copilot` is such (W1-13). `rclone` answers its own listing.
    "copilot": None,
    "rclone": ("rclone", "lsd", "gdrive:", "--max-depth", "0"),
}

AUTH_NEEDS: dict[str, str] = {
    "claude": "the CLAUDE_CODE_OAUTH_TOKEN Codespaces secret (from `claude setup-token`)",
    "gh": "GITHUB_TOKEN or GH_TOKEN in the environment, or `gh auth login`",
    "codex": "the laptop's ChatGPT sign-in cache `~/.codex/auth.json`, mirrored at launch (R87); "
             "`codex login --device-auth` is manual recovery only",
    "grok": "the XAI_API_KEY Codespaces secret (the laptop signs grok in with that key)",
    "agy": "an `agy` sign-in: run `agy` once in the Codespace (`gh codespace ssh`), open the Google "
           "URL it prints in a browser and complete the sign-in (no login subcommand, no Codespaces "
           "secret; its model call is what shows the login)",
    "copilot": "the COPILOT_GITHUB_TOKEN Codespaces secret (a fine-grained token with the "
               "'Copilot Requests' account permission; R88a)",
    "rclone": "the RCLONE_CONFIG_GDRIVE_TOKEN Codespaces secret (the Drive token, `[#1379]`)",
}


# ---- the laptop's own sign-in, per CLI (W1-13, R87): what is mirrored, what is not, and why ----

@dataclass(frozen=True)
class SignIn:
    """What one CLI signs in with. `files` are paths relative to HOME (the first is the PRIMARY
    cache); `env_keys` are the API-key variables the CLI honours; `route` is how a Codespace gets
    the same sign-in: `mirror` (copy the file at launch), `secret-token` (a long-lived token held
    as a Codespaces secret -- a separate credential the laptop never refreshes), `env-key` (the
    laptop itself uses the key) or `waiting` (no file to copy). `refresh` is the vendor's refresh
    behaviour (`safe`: refresh tokens do not rotate; `guarded`: they rotate, so the copy is made only
    while the Codespace can never need a refresh; `rotates`: never mirror; `unknown`; `none`)."""

    files: tuple[str, ...] = ()
    env_keys: tuple[str, ...] = ()
    route: str = "waiting"
    refresh: str = "unknown"
    renew: str = ""
    why: str = ""
    fallback: str = ""


#: DECIDED-BY-LANE (b2-codespace-subscription-auth): measured on the laptop 2026-10-06 (booleans and
#: paths only), vendor docs retrieved the same day and quoted in the run record. A CLI absent from
#: this table is NAMED by C1 as having no declared sign-in, never skipped.
SIGN_IN: dict[str, SignIn] = {
    "claude": SignIn(
        (".claude/.credentials.json",), ("CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY"),
        route="secret-token", refresh="rotates",
        renew="run `claude setup-token` on the laptop, then `gh secret set CLAUDE_CODE_OAUTH_TOKEN "
              "--user` with its output",
        why="the laptop signs in by its OAuth file, whose refresh token rotates (the access token "
            "lasts 8 h); the Codespace uses the long-lived setup token of the same subscription, a "
            "credential the laptop never refreshes"),
    "codex": SignIn(
        (".codex/auth.json",), ("CODEX_API_KEY", "OPENAI_API_KEY"),
        route="mirror", refresh="guarded",
        renew="run `codex login` on the laptop (browser ChatGPT sign-in) and relaunch",
        why="OpenAI documents copying ~/.codex/auth.json to a headless machine; it also says not to "
            "share the file across concurrent machines, so the copy is made only while it is "
            "fresh enough that the Codespace never has to refresh it (`credential_expiry`)",
        fallback="seed a SEPARATE ChatGPT login for Codespaces: `codex login --device-auth` with "
                 "CODEX_HOME pointing at an empty scratch folder, then `gh secret set CODEX_AUTH_JSON "
                 "--user < <scratch>/auth.json` (the launch writes it to ~/.codex/auth.json)"),
    "grok": SignIn(
        (), ("XAI_API_KEY",), route="env-key", refresh="none",
        renew="issue a new XAI_API_KEY at console.x.ai and run `gh secret set XAI_API_KEY --user`",
        why="the laptop has no grok sign-in file and no keyring entry: it uses XAI_API_KEY itself"),
    "agy": SignIn(
        (), (), route="waiting", refresh="unknown",
        renew="BLOCKED-AUTH: sign in to agy in the Codespace once (`gh codespace ssh`, open the URL it prints)",
        why="the laptop's sign-in is the Windows Credential Manager entry `gemini:antigravity`; the "
            "vendor docs name only the OS keyring, or GEMINI_API_KEY with modelProvider=gemini, "
            "which the laptop does not use -- there is no file to mirror"),
    "copilot": SignIn(
        (), ("COPILOT_GITHUB_TOKEN",), route="secret-token", refresh="none",
        renew="create a fine-grained personal access token owned by your personal account with the "
              "'Copilot Requests' account permission, then `gh secret set COPILOT_GITHUB_TOKEN --user` "
              "with it",
        why="the laptop's sign-in is the Windows Credential Manager entry `copilot-cli`, which the "
            "Codespace cannot hold; GitHub's docs name an environment token as the form for "
            "containers and non-interactive environments, and check COPILOT_GITHUB_TOKEN first "
            "(R88a). The token is the same account's Copilot seat, not a metered key"),
    "gh": SignIn(
        (), ("GH_TOKEN", "GITHUB_TOKEN"), route="env-key", refresh="none",
        renew="`gh auth refresh` on the laptop; the Codespace's GITHUB_TOKEN is issued by Codespaces",
        why="the laptop's token is in the OS keyring; gh's documented headless path is the "
            "GITHUB_TOKEN the Codespace is issued, which answers `gh auth status` by itself"),
    "rclone": SignIn(
        (), ("RCLONE_CONFIG_GDRIVE_TOKEN",), route="secret-token", refresh="none",
        renew="`rclone config reconnect gdrive:` on the laptop, then `gh secret set "
              "RCLONE_CONFIG_GDRIVE_TOKEN --user` (`[#1379]` owns the expiry)",
        why="the laptop's rclone.conf also holds other remotes (an employer drive), which must not be "
            "copied; the Codespace reads the Drive by its own token secret"),
}

#: Pairs of mechanism classes that are the SAME sign-in for EVERY CLI. None: what is equivalent is a
#: fact about one CLI's vendor, so it lives in `AUTH_EQUIVALENT_FOR` below. Anything that differs
#: between the laptop and the Codespace and is in neither is the R87 failure -- a provider answering
#: through a credential the laptop does not use.
AUTH_EQUIVALENT: frozenset[tuple[str, str]] = frozenset()

#: (laptop class, codespace class) pairs that are the same sign-in for ONE named CLI. Copilot only
#: (R88a): the laptop holds its login in the OS keyring, the Codespace the token of that same
#: account's Copilot seat in COPILOT_GITHUB_TOKEN. An `api-key` there stays the R87 failure.
AUTH_EQUIVALENT_FOR: dict[str, frozenset[tuple[str, str]]] = {
    "copilot": frozenset({("keyring", "subscription")}),
}

#: The refresh interval after which Codex refreshes `~/.codex/auth.json` on its next call (OpenAI's
#: CI/CD auth docs: "approximately 8 days"), and the margin kept so a Codespace's copy can never reach it.
CODEX_REFRESH_DAYS = 8.0
CODEX_MIRROR_MAX_AGE_DAYS = 7.0

#: The folders a probe may write into besides the transport root: exactly one, `to-browser/`, where
#: the lanes' own handbacks go. A probe addresses ONE file there -- never a deeper path, never a
#: sibling folder, never `..` -- so it can only ever create the file a contract names.
TRANSPORT_PROBE_DIRS: tuple[str, ...] = ("to-browser",)

#: The one path `collect --probe-write` may write on the transport: a single plain file name at the
#: root, or a single plain file name directly inside one of `TRANSPORT_PROBE_DIRS`.
_PROBE_NAME_RE = re.compile(r"^(?:(?:" + "|".join(re.escape(d) for d in TRANSPORT_PROBE_DIRS)
                            + r")/)?[A-Za-z0-9][A-Za-z0-9._-]*$")

def _probe_name_ok(name: str) -> bool:
    """A probe name the regex admits AND that is not a folder's own name (a root file called
    `to-browser` would collide with the folder it shadows)."""
    return bool(_PROBE_NAME_RE.fullmatch(name)) and name not in TRANSPORT_PROBE_DIRS


HOOK_NAMES: tuple[str, ...] = ("pre-commit", "commit-msg", "pre-push")
_HOOK_SIGNATURE = "File generated by pre-commit"  # scripts/arm_hooks.py::_SIGNATURE

LANDING_MERGE_NOT_RUN_REASON = (
    "no integration record was supplied: the local --no-ff merge of the test lane's branch on a "
    "scratch `worktree-integrate-*` branch, the re-run of the outcome test and that branch's CI "
    "push verdict are measured by `integrate` and read here by `check --integration`; a leg "
    "nobody ran is NOT-RUN, never PASS")

TRANSPORT_WRITE_NOT_RUN_REASON = (
    "the write leg was not exercised: `collect --probe-write PATH` exercises it (PATH is one plain "
    "file name, or one file in `to-browser/`, that the contract names); until it runs only the "
    "read leg is measured")

#: CI states a scratch-branch merge may LAND on -- `merge_path.LANDABLE_STATES`, restated so this
#: reader needs no import of the merge path (a test holds the two equal). `PASS` is the only green;
#: `PRE-EXISTING` is every failing test accounted for against the base.
CI_LANDABLE_STATES: tuple[str, ...] = ("PASS", "PRE-EXISTING")
#: CI states that MEASURED a red: the leg ran and failed.
CI_FAILED_STATES: tuple[str, ...] = ("REGRESSED", "RED", "CANCELLED")

#: The only branch a scratch integration may push: the integrator's own prefix (`merge_path.
#: INTEGRATION_BRANCH_PREFIX`) and a plain slug, never `main`.
_SCRATCH_BRANCH_RE = re.compile(r"^worktree-integrate-[a-z0-9][a-z0-9-]*$")
_RUN_BRANCH_RE = re.compile(r"^worktree-[a-z0-9][a-z0-9-]*$")
_FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

#: Cores per Codespace machine type -- the multiplier GitHub bills core-hours by. A machine not
#: listed is refused (`core_hours`), never priced at zero.
MACHINE_CORES: dict[str, int] = {
    "basicLinux32gb": 2,
    "standardLinux32gb": 4,
    "premiumLinux": 8,
    "largePremiumLinux": 16,
}

CONDITION_NAMES = {1: "environment", 2: "gates", 3: "landing", 4: "transport", 5: "cleanup"}

_REQUIRED_KEYS = ("environment", "gates", "landing", "transport", "base_sha", "tree_sha", "side")


#: CI reds a scratch integration branch shows BY CONSTRUCTION, keyed by test node id (no OS prefix)
#: -> `[#row] why`. A test that asks about the checkout itself reads red on a branch that is not
#: `main` and green on main's own run, so it reads NEW against the main baseline on every
#: integration. A declaration forgives that one id only, and only when it is the sole red.
DECLARED_CI_CASES: dict[str, str] = {
    "tests/test_worktree_seed.py::test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH":
        "[#716] asks whether the live checkout is `main`; a scratch integration branch is not",
}

_CI_RED_NAME_RE = re.compile(r"^pytest \([^)]*\): (\S+)$")
_CI_RED_COUNTS_RE = re.compile(r"^(\d+) new red test\(s\), 0 non-test failure\(s\), 0 job\(s\) broken")


def declared_cases_problems() -> list[str]:
    """Each declared OS or CI case must carry a row id -- a bare forgiveness is a hidden FAIL."""
    return [k for table in (DECLARED_OS_CASES, DECLARED_CI_CASES) for k, row in table.items()
            if not str(row).startswith("[#")]


def _declared_only_reds(ci: Mapping) -> list[str]:
    """The declared ids when EVERY red of a REGRESSED verdict is a declared case, else `[]`.

    The verdict's own count must close: N reds named, N counted, no non-test failure, no broken
    job, no missing context. A verdict whose reason cannot be read, or whose list was cut short,
    forgives nothing."""
    counts = _CI_RED_COUNTS_RE.match(str(ci.get("reason") or ""))
    reds = [str(r) for r in (ci.get("new_reds") or [])]
    if not counts or ci.get("missing_contexts") or not reds or int(counts.group(1)) != len(reds):
        return []
    names = []
    for red in reds:
        m = _CI_RED_NAME_RE.match(red)
        if not m or m.group(1) not in DECLARED_CI_CASES or m.group(1) in declared_cases_problems():
            return []
        names.append(m.group(1))
    return sorted(set(names))


# =============================================================================== types

class RemoteUnavailable(RuntimeError):
    """The Codespace side could not be created, reached or read -- the typed R59 failure."""


class LocalRecordUnusable(RuntimeError):
    """The local record is missing or malformed -- nothing to compare against."""


@dataclass(frozen=True)
class CmdResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


Runner = Callable[..., CmdResult]


@dataclass(frozen=True)
class Verdict:
    condition: int
    name: str
    status: str  # PASS | FAIL | NOT-RUN
    reason: str
    evidence: tuple[str, ...] = ()

    def render(self) -> str:
        head = f"{self.status} cond={self.condition} {self.name}"
        return f"{head} {self.reason}".rstrip() if self.reason else head


def _verdict(n: int, status: str, reason: str = "", evidence: Sequence[str] = ()) -> Verdict:
    return Verdict(n, CONDITION_NAMES[n], status, reason, tuple(evidence))


class Leg(enum.Enum):
    """What ONE measured leg of a condition came to -- three values that cannot stand in for each
    other (N1, R59). `NOT_RUN` is not a weak `PASS` and not a soft `FAIL`: it is the leg nobody
    measured, and a condition made of legs is `PASS` only when every leg is `PASS`."""

    PASS = "PASS"
    FAIL = "FAIL"
    NOT_RUN = "NOT-RUN"


@dataclass(frozen=True)
class LegResult:
    leg: Leg
    detail: str


def fold_legs(legs: Sequence[LegResult]) -> tuple[str, str]:
    """`(status, reason)` of a condition from its legs: FAIL if any leg failed, else NOT-RUN if
    any leg was unmeasured -- or if there are no legs at all (an empty fold would be `all passed`
    by vacuity, the pass this check exists to refuse) -- else PASS."""
    failed = [r.detail for r in legs if r.leg is Leg.FAIL]
    if failed:
        return "FAIL", "; ".join(failed)
    unmeasured = [r.detail for r in legs if r.leg is Leg.NOT_RUN]
    if unmeasured or not legs:
        return "NOT-RUN", "; ".join(unmeasured) or "no leg was measured"
    return "PASS", ""


def default_run(argv: Sequence[str], *, cwd: Optional[Path] = None, timeout: int = 900,
                env: Optional[Mapping[str, str]] = None) -> CmdResult:
    """The one place a subprocess starts. Never raises: a command that cannot be started is
    exit 127 and one that timed out is 124 -- data the verdicts reason about."""
    exe = shutil.which(argv[0])
    if exe is None:
        return CmdResult(127, "", f"{argv[0]}: not found on PATH")
    try:
        # stdin is closed: `codex exec` prints "Reading additional input from stdin..." and waits
        # forever on an open pipe (found building the served-id probe, 2026-10-04).
        proc = subprocess.run([exe, *argv[1:]], cwd=str(cwd) if cwd else None, text=True,
                              encoding="utf-8", errors="replace", capture_output=True,
                              stdin=subprocess.DEVNULL,
                              timeout=timeout, env=dict(env) if env is not None else None)
    except OSError as exc:
        return CmdResult(127, "", str(exc))
    except subprocess.TimeoutExpired:
        return CmdResult(124, "", f"timed out after {timeout}s")
    return CmdResult(proc.returncode, proc.stdout or "", proc.stderr or "")


_SEMVER = re.compile(r"\d+\.\d+(?:\.\d+)*")


def _semver(text: str) -> Optional[str]:
    match = _SEMVER.search(text or "")
    return match.group(0) if match else None


# =============================================================================== collectors

def _tool_probe(name: str) -> list[str]:
    """A lane runs under a LOGIN shell on a Codespace (`codespace_admission.py`: PATH is only
    complete there), so on POSIX a tool is probed through `bash -lc`."""
    if os.name == "nt":
        return [name, "--version"]
    return ["bash", "-lc", f"command -v {name} >/dev/null 2>&1 && {name} --version"]


def _status_probe(argv: Sequence[str]) -> list[str]:
    """A login-state command, run the way `_tool_probe` runs a version: a LOGIN shell on POSIX."""
    if os.name == "nt":
        return list(argv)
    return ["bash", "-lc", shlex.join(argv)]


def collect_auth(run: Runner, tools: Mapping[str, Mapping], *, root: Path = _REPO_ROOT,
                 names: Optional[Sequence[str]] = None) -> dict:
    """Each lane tool's login state, from its own status command. The command's output is read
    for one boolean and discarded; the record carries only the state and the command's name."""
    auth: dict[str, dict] = {}
    for name in (names if names is not None else lane_tools(registry_for(root))):
        cmd = AUTH_PROBES.get(name)
        label = " ".join(cmd) if cmd else "(no non-interactive status command)"
        if not (tools.get(name) or {}).get("present"):
            state = "tool-absent"
        elif cmd is None:
            state = "unprobed"
        else:
            res = run(_status_probe(cmd), cwd=root, timeout=60)
            if res.returncode in (124, 127):
                # timed out / would not start: no login was observed either way. Recording it as
                # `unauthenticated` would let C1 print a named exception for a check that never ran.
                state = "probe-error"
            elif name == "claude":
                state = "authenticated" if res.returncode == 0 and re.search(
                    r'"loggedIn"\s*:\s*true', res.stdout or "") else "unauthenticated"
            else:
                state = "authenticated" if res.returncode == 0 else "unauthenticated"
        auth[name] = {"state": state, "probe": label}
    return auth



# ====================================================== C1 served model ids (b2-codespace-1to1)

#: The registry file the served ids are compared with is `REGISTRY_PATH` (declared above, beside the
#: tool sets read from it).

#: Where the registry says a model CLI's id lives when the CLI's role is NOT simply the first one
#: that pins a model for its provider: (role, or None for the provider's single `models:` row).
#: `claude` is the lane's runner (`implement`); `codex` and `grok` are the review routes; `agy` has no
#: role-level model, so its id is the one `antigravity` row under `models:`. A CLI absent here takes
#: the default rule in `_seam_for` -- so a provider added to the registry needs no edit.
_SEAM_ROLE_OVERRIDES: dict[str, Optional[str]] = {
    "claude": "implement",
    "codex": "review",
    "grok": "review",
    "agy": None,
}


def _seam_for(registry: Mapping, cli: str) -> tuple[Optional[str], Optional[str]]:
    """`(provider id, role)` for `cli`: the provider the registry gives that CLI, and the role whose
    order pins its model (an override, else the first role in registry order that pins one for it,
    else None: the provider's single `models:` row)."""
    provider = next((name for name, row in (registry.get("providers") or {}).items()
                     if isinstance(row, Mapping) and row.get("cli") == cli), None)
    if provider is None:
        return None, None
    if cli in _SEAM_ROLE_OVERRIDES:
        return provider, _SEAM_ROLE_OVERRIDES[cli]
    for role, row in (registry.get("roles") or {}).items():
        for entry in (row or {}).get("order") or []:
            if isinstance(entry, Mapping) and entry.get("provider") == provider and entry.get("model"):
                return provider, role
    return provider, None

#: agy lists each family in tiers (`agy models`: gemini-3.8-flash-{high,medium,low}); the registry
#: row is the family, so a served tier of that family is the registered model.
_AGY_TIERS = ("high", "medium", "low")

#: What a failed call says when the login is what is missing. Matched only on a call whose nonce did
#: not come back, so a model's own words about "signing in" in an answer never reclassify it (agy
#: logs its model label before it authenticates, so a served id is not proof the call went through).
_LOGIN_MISSING = re.compile(
    r"not (?:logged|signed) in|please (?:run /)?log ?in|sign(?:ed)?[ -]?in|log ?in required"
    r"|unauthori[sz]ed|\b401\b|missing credentials|authentication (?:required|failed)",
    re.IGNORECASE)

#: What a refused call says when the ACCOUNT behind the key has no credit left. Checked before the
#: login patterns: such a call can carry a 401 too, and a key with no credit is not a missing login.
_NO_CREDITS = re.compile(r"no credits remaining|insufficient[_ ]quota|exceeded your current quota"
                         r"|add credits to continue", re.IGNORECASE)

PROBE_TIMEOUT = 240


@dataclass(frozen=True)
class ExpectedModel:
    id: Optional[str]
    where: str


def expected_models(registry: Mapping) -> dict[str, ExpectedModel]:
    """cli -> the id the registry routes that CLI to, and where the registry says so. The CLI set is
    the registry's own (`model_clis`), so a provider added there is compared with no edit here."""
    out: dict[str, ExpectedModel] = {}
    for cli in model_clis(registry):
        provider, role = _seam_for(registry, cli)
        if role is not None:
            order = ((registry.get("roles") or {}).get(role) or {}).get("order") or []
            entry = next((e for e in order if isinstance(e, Mapping)
                          and e.get("provider") == provider), None)
            model = (entry or {}).get("model")
            where = f"roles.{role}, provider {provider}"
            out[cli] = ExpectedModel(str(model) if model else None,
                                     where if model else f"{where}: no model pinned")
        else:
            rows = [name for name, row in (registry.get("models") or {}).items()
                    if isinstance(row, Mapping) and row.get("provider") == provider]
            where = f"models row of provider {provider}"
            out[cli] = ExpectedModel(rows[0] if len(rows) == 1 else None,
                                     where if len(rows) == 1 else f"{where}: {len(rows)} rows, need one")
    return out


def served_matches(cli: str, served: Optional[str], expected: Optional[str]) -> bool:
    """Exact equality; `agy` alone also accepts a tier of the registered family."""
    if not served or not expected:
        return False
    if served == expected:
        return True
    return cli == "agy" and served.startswith(expected + "-") \
        and served[len(expected) + 1:] in _AGY_TIERS


def probe_prompt(nonce: str) -> str:
    """One line, no quotes: it crosses a login shell and, on Windows, a `.cmd` shim. It is not an
    instruction to repeat an exact string -- grok refuses that wording -- but a check code to return."""
    return f"This is a connectivity check and the check code is {nonce}. Please reply with the check code."


def model_probe_argv(cli: str, nonce: str, model: str, log_file: str) -> list[str]:
    """The one trivial headless call for `cli`, asking for the registry's id by name. A lane asks
    for its model by id too, so the probe tests that the CLI SERVES the id it was asked for."""
    prompt = probe_prompt(nonce)
    if cli == "claude":
        return ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json",
                "--verbose", "--no-session-persistence", "--max-turns", "1",
                "--setting-sources", "user"]
    if cli == "codex":
        return ["codex", "exec", "--skip-git-repo-check", "--color", "never", "-m", model,
                "-s", "read-only", prompt]
    if cli == "grok":
        return ["grok", "-m", model, "-p", prompt, "--output-format", "json", "--max-turns", "1"]
    if cli == "agy":
        return ["agy", "-p", prompt, "--output-format", "json", "--log-file", log_file]
    if cli == "copilot":
        return ["copilot", "-p", prompt, "--model", model, "--output-format", "json"]
    raise ValueError(f"no served-id probe is declared for {cli!r}")


def read_copilot(stdout: str, nonce: str) -> tuple[Optional[str], bool]:
    """(served id, answered). `copilot --output-format json` is JSONL; the id is the `model` of the
    `assistant.message` event -- the tool's own record of the reply -- and the answer is the nonce in
    that event's `content` (measured 2026-10-06 on `--model auto`: `gpt-6-luna`)."""
    served: Optional[str] = None
    texts: list[str] = []
    for obj in _json_lines(stdout):
        if obj.get("type") != "assistant.message":
            continue
        data = obj.get("data") or {}
        if data.get("model") and served is None:
            served = str(data["model"])
        texts.append(str(data.get("content") or ""))
    return served, nonce in "\n".join(texts)


def _json_lines(text: str) -> list[dict]:
    rows = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def _json_object(text: str) -> Optional[dict]:
    """The first JSON object in `text` (a CLI may print a warning line before it)."""
    text = text or ""
    start = text.find("{")
    if start < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def read_claude(stdout: str, nonce: str) -> tuple[Optional[str], bool]:
    """(served id, answered). The id is the stream's own assistant message `message.model` -- the
    transcript record -- and `<synthetic>` (what Claude Code writes for its own error text) is not a
    served model."""
    served: Optional[str] = None
    texts: list[str] = []
    for obj in _json_lines(stdout):
        if obj.get("type") != "assistant":
            continue
        message = obj.get("message") or {}
        model = message.get("model")
        if model and model != "<synthetic>" and served is None:
            served = str(model)
        for block in message.get("content") or []:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(str(block.get("text") or ""))
    return served, nonce in "\n".join(texts)


_ANSI = re.compile("\x1b\\[[0-9;]*m")


def read_codex(stderr: str, stdout: str, nonce: str) -> tuple[Optional[str], bool]:
    """(served id, answered). The id is the `model:` line of Codex's own run header -- the block
    between the first two rules of STDERR (colour-coded when a terminal is attached, measured
    2026-10-04). Nothing the model prints can reach it: STDOUT is never searched for the id, and a
    `model:` line the transcript echoes after the header is outside the block. The answer is the
    nonce on STDOUT, the final message; the prompt echoed on stderr carries it too and is not one."""
    parts = re.split(r"^-{8}\s*$", _ANSI.sub("", stderr or ""), maxsplit=2, flags=re.MULTILINE)
    header = parts[1] if len(parts) >= 3 else ""
    match = re.search(r"^model:\s*(\S+)", header, re.MULTILINE)
    return (match.group(1) if match else None), nonce in _ANSI.sub("", stdout or "")


def read_grok(stdout: str, nonce: str, home: Path) -> tuple[Optional[str], bool]:
    """(served id, answered). The id is `primaryModelId` in the session store's `usage.json`
    (`~/.grok/sessions/<cwd>/<session>/usage.json`) for the session this call printed."""
    obj = _json_object(stdout)
    if obj is None:
        return None, False
    answered = nonce in str(obj.get("text") or "")
    session = str(obj.get("sessionId") or "")
    served: Optional[str] = None
    if session and re.fullmatch(r"[A-Za-z0-9._-]+", session):
        for usage in sorted(Path(home, ".grok", "sessions").glob(f"*/{session}/usage.json")):
            try:
                data = json.loads(usage.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            primary = ((data or {}).get("session") or {}).get("primaryModelId")
            if primary:
                served = str(primary)
                break
    return served, answered


def _label_slug(label: str) -> str:
    return re.sub(r"[^a-z0-9.]+", "-", label.lower()).strip("-")


def read_agy(stdout: str, log_text: str, nonce: str) -> tuple[Optional[str], bool]:
    """(served id, answered). The id is the model label agy's own run log propagates to its
    backend (`label="Gemini 3.8 Flash (High)"`), as the slug `agy models` lists it under."""
    obj = _json_object(stdout) or {}
    answered = obj.get("status") == "SUCCESS" and nonce in str(obj.get("response") or "")
    labels = re.findall(r'label="([^"]+)"', log_text or "")
    return (_label_slug(labels[-1]) if labels else None), answered


#: The CLIs `model_probe_argv` and the readers know. A registry CLI outside this set is probed by
#: name and FAILS by name (`no-probe-declared`) -- present in the record, never dropped.
_PROBE_DECLARED = ("claude", "codex", "grok", "agy", "copilot")


#: The API-key variables no invocation of a CLI may see, whatever else is on this side (R87.3,
#: b2w2-codespace-finish). Codex only: OpenAI documents `forced_login_method` (`chatgpt` | `api`) and
#: a non-interactive API-key route, but not which wins when both are present, so the call is made
#: without the keys and says "not logged in" instead of being answered by one.
NEVER_KEYS: dict[str, tuple[str, ...]] = {"codex": ("CODEX_API_KEY", "OPENAI_API_KEY")}


def unused_keys(cli: str, home: Path, env: Mapping[str, str]) -> tuple[str, ...]:
    """The API-key variables of `cli` that are set in `env` and must not reach its call: every
    `NEVER_KEYS` name (R87.3), and any key the CLI has a sign-in CACHE on this side to make
    unnecessary -- a key the laptop does not use for it (R87). A CLI with no cache (grok) keeps its
    key: the laptop itself signs in with it."""
    forced = tuple(k for k in NEVER_KEYS.get(cli, ()) if env.get(k))
    spec = SIGN_IN.get(cli)
    if spec is None or not spec.files:
        return forced
    if not (Path(home) / spec.files[0]).is_file():
        return forced
    return forced + tuple(k for k in spec.env_keys if env.get(k) and k not in forced)


def _probe_one(cli: str, run: Runner, workdir: Path, expected: Optional[ExpectedModel],
               nonce: str, home: Path, timeout: int,
               env: Optional[Mapping[str, str]] = None) -> dict:
    log_file = workdir / "agy.log"
    if cli not in _PROBE_DECLARED:
        return {"state": "no-probe-declared", "served_id": None,
                "detail": f"no served-id probe is declared for {cli}: add its argv and reader here"}
    if expected is None or not expected.id:
        why = expected.where if expected else "no registry entry"
        return {"state": "no-expected", "served_id": None,
                "detail": f"the registry names no model for {cli} ({why}); the call was not made"}
    argv = model_probe_argv(cli, nonce, expected.id, str(log_file))
    base_env = dict(os.environ if env is None else env)
    strip = unused_keys(cli, home, base_env)
    for key in strip:
        base_env.pop(key, None)
    if strip and os.name != "nt":
        # a login shell re-reads the profile that exports the Codespaces secrets, so the unset has
        # to happen INSIDE it (`env -u` runs the CLI with those names removed)
        argv = ["env", *[x for k in strip for x in ("-u", k)], *argv]
    res = run(_status_probe(argv), cwd=workdir, timeout=timeout, env=base_env)
    if res.returncode in (124, 127):
        how = "timed out" if res.returncode == 124 else "could not start"
        return {"state": "probe-error", "served_id": None,
                "detail": f"the call did not run (exit {res.returncode}: {how})"}
    out = res.stdout or ""
    if cli == "claude":
        served, answered = read_claude(out, nonce)
    elif cli == "codex":
        served, answered = read_codex(res.stderr or "", out, nonce)
    elif cli == "grok":
        served, answered = read_grok(out, nonce, home)
    elif cli == "copilot":
        served, answered = read_copilot(out, nonce)
    else:
        try:
            log_text = log_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            log_text = ""
        served, answered = read_agy(out, log_text, nonce)
    if served and answered:
        return {"state": "served", "served_id": served,
                "detail": "served id read from the tool's own record; the nonce came back"}
    said = out + "\n" + (res.stderr or "")
    if not answered and _NO_CREDITS.search(said):
        return {"state": "no-credits", "served_id": None,
                "detail": (f"OPERATOR-ACTION: add credits to the account that issued the {cli} key "
                           "(the call said none remain); not a login item")}
    if not answered and _LOGIN_MISSING.search(said):
        return {"state": "unauthenticated", "served_id": None,
                "detail": "the call said the login is missing"}
    return {"state": "no-answer", "served_id": served,
            "detail": (f"exit {res.returncode}; "
                       + ("the nonce did not come back" if served else "no served id in the tool's record"))}


def collect_models(run: Runner, tools: Mapping[str, Mapping], auth: Mapping[str, Mapping],
                   expected: Mapping[str, ExpectedModel], *, home: Optional[Path] = None,
                   nonce: Optional[str] = None, timeout: int = PROBE_TIMEOUT,
                   clis: Optional[Sequence[str]] = None,
                   env: Optional[Mapping[str, str]] = None) -> dict:
    """Each model CLI's served id, from ONE call each, run in an empty directory so no project
    context shapes the answer. The record keeps state, id and a one-line detail only -- never the
    model's output, the nonce or any credential. `clis` defaults to the registry's own set."""
    home = Path(home) if home is not None else Path.home()
    nonce = nonce or "CHK-" + secrets.token_hex(4).upper()
    out: dict[str, dict] = {}
    with tempfile.TemporaryDirectory(prefix="parity-probe-") as tmp:
        for cli in (clis if clis is not None else model_clis()):
            if not (tools.get(cli) or {}).get("present"):
                out[cli] = {"state": "tool-absent", "served_id": None, "detail": f"{cli} is not installed"}
            elif ((auth.get(cli) or {}).get("state")) == "unauthenticated":
                out[cli] = {"state": "not-probed-auth", "served_id": None,
                            "detail": "login missing -- a named auth item; the call was not made"}
            else:
                out[cli] = _probe_one(cli, run, Path(tmp), expected.get(cli), nonce, home, timeout,
                                      env)
    return out


def measure_mechanism(cli: str, home: Path, env: Mapping[str, str]) -> dict:
    """How `cli` is signed in on THIS side, measured -- the class (`subscription` for a sign-in cache
    or claude's long-lived setup token, `api-key` for an API-key variable alone, `none`), the way
    (a path or variable NAME) and whether an API-key variable is set. Booleans, paths and names
    only: no value is ever read into the record (R13)."""
    spec = SIGN_IN.get(cli)
    if spec is None:
        return {"class": "none", "via": "no sign-in declared", "api_key_env_present": False}
    keys_set = [k for k in spec.env_keys if env.get(k)]
    if cli == "claude" and env.get("CLAUDE_CODE_OAUTH_TOKEN"):
        return {"class": "subscription", "via": "env CLAUDE_CODE_OAUTH_TOKEN",
                "api_key_env_present": bool(env.get("ANTHROPIC_API_KEY"))}
    if cli == "copilot" and env.get("COPILOT_GITHUB_TOKEN"):
        # the account's Copilot seat through a token (R88a), not a metered API key
        return {"class": "subscription", "via": "env COPILOT_GITHUB_TOKEN", "api_key_env_present": False}
    if spec.files and (Path(home) / spec.files[0]).is_file():
        return {"class": "subscription", "via": f"file {spec.files[0]}",
                "api_key_env_present": bool(keys_set)}
    if keys_set:
        return {"class": "api-key", "via": "env " + ", ".join(keys_set), "api_key_env_present": True}
    return {"class": "none", "via": "no cache file and no key variable", "api_key_env_present": False}


def collect_auth_mechanism(names: Sequence[str], home: Path, env: Mapping[str, str],
                           models: Mapping[str, Mapping]) -> dict:
    """The measured mechanism per CLI. A CLI whose served-id call ANSWERED with no file and no key
    on this side signs in through something this code cannot see -- the OS keyring -- and is recorded
    as `keyring`, never as `none`."""
    out: dict[str, dict] = {}
    for cli in names:
        mech = measure_mechanism(cli, home, env)
        if mech["class"] == "none" and (models.get(cli) or {}).get("state") == "served":
            mech = {"class": "keyring", "via": "answered with no cache file and no key variable",
                    "api_key_env_present": False}
        out[cli] = mech
    return out


def _iso(text: object) -> Optional[datetime]:
    try:
        parsed = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _ms(value: object) -> Optional[datetime]:
    try:
        return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc)
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def credential_expiry(cli: str, home: Path, *, now: Optional[datetime] = None) -> dict:
    """Is the sign-in cache of `cli` on this side usable? `{"state", "renew", "detail"}` from the
    file's own timestamps -- no value is read out of it. `ok`: it can serve or renew itself;
    `due`: its next call refreshes it (Codex, past `CODEX_REFRESH_DAYS`); `expired`: neither the
    access nor the refresh token can serve any more; `not-a-file`: the CLI has no cache to read here.
    `renew` is the ONE step that fixes it (R59, R65)."""
    now = now or datetime.now(timezone.utc)
    spec = SIGN_IN.get(cli)
    if spec is None or not spec.files:
        return {"state": "not-a-file", "renew": spec.renew if spec else "", "detail": "no cache file"}
    path = Path(home) / spec.files[0]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"state": "expired", "renew": spec.renew, "detail": f"{spec.files[0]} is missing or unreadable"}
    if cli == "claude":
        oauth = data.get("claudeAiOauth") or {}
        access, refresh = _ms(oauth.get("expiresAt")), _ms(oauth.get("refreshTokenExpiresAt"))
        if refresh is not None and refresh <= now:
            return {"state": "expired", "renew": spec.renew, "detail": "the refresh token has expired"}
        if access is not None and access <= now and refresh is None:
            return {"state": "expired", "renew": spec.renew, "detail": "the access token has expired"}
        return {"state": "ok", "renew": spec.renew, "detail": "the refresh token is live"}
    if cli == "codex":
        if str(data.get("auth_mode")) != "chatgpt":
            return {"state": "expired", "renew": spec.renew, "detail": "the cache is not a ChatGPT sign-in"}
        refreshed = _iso(data.get("last_refresh"))
        if refreshed is None:
            return {"state": "due", "renew": spec.renew, "detail": "no last_refresh recorded"}
        age = (now - refreshed).total_seconds() / 86400.0
        if age >= CODEX_REFRESH_DAYS:
            return {"state": "due", "renew": spec.renew, "age_days": round(age, 2),
                    "detail": f"last refreshed {age:.1f} days ago; the next call refreshes it"}
        return {"state": "ok", "renew": spec.renew, "age_days": round(age, 2),
                "detail": f"last refreshed {age:.1f} days ago"}
    return {"state": "ok", "renew": spec.renew, "detail": "cache present"}


def _fold_model_proof_into_auth(auth: dict, models: Mapping[str, Mapping],
                                clis: Optional[Sequence[str]] = None) -> None:
    """A model call is the only login probe `grok` and `agy` have: an answered call proves the login,
    and one that said the login is missing names it. Status-command verdicts are left alone."""
    for cli in (clis if clis is not None else model_clis()):
        entry, model = auth.get(cli), models.get(cli) or {}
        if entry is None:
            continue
        if model.get("state") == "served" and entry.get("state") == "unprobed":
            auth[cli] = {"state": "authenticated", "probe": "a model call answered (served-id probe)"}
        elif model.get("state") == "unauthenticated":
            auth[cli] = {"state": "unauthenticated", "probe": entry.get("probe", "")}


def installed_hooks(run: Runner, root: Path) -> list[str]:
    """Hook types whose shim exists and is pre-commit-managed in the RESOLVED hooks dir."""
    where = run(["git", "rev-parse", "--git-path", "hooks"], cwd=root)
    if where.returncode != 0 or not where.stdout.strip():
        return []
    hooks_dir = Path(where.stdout.strip())
    if not hooks_dir.is_absolute():
        hooks_dir = root / hooks_dir
    found = []
    for name in HOOK_NAMES:
        shim = hooks_dir / name
        try:
            if shim.is_file() and _HOOK_SIGNATURE in shim.read_text(encoding="utf-8",
                                                                      errors="replace"):
                found.append(name)
        except OSError:
            continue
    return sorted(found)


def collect_environment(run: Runner, *, root: Path = _REPO_ROOT,
                        hooks: Optional[Sequence[str]] = None, home: Optional[Path] = None,
                        nonce: Optional[str] = None) -> dict:
    """Condition 1's manifest, built in the environment this runs in. The tools probed are the
    registry's CLIs plus the non-model tools the Codespace declares (`lane_tools`), read here and
    never typed (R70)."""
    uv = run(["uv", "--version"], cwd=root)
    sync = run(["uv", "sync", "--locked"], cwd=root)
    py = run(["uv", "run", "--locked", "python", "-c",
              "import platform;print(platform.python_version())"], cwd=root)
    lock = root / "uv.lock"
    registry = registry_for(root)
    names = lane_tools(registry)
    clis = model_clis(registry)
    tools = {}
    for name in names:
        res = run(_tool_probe(name), cwd=root, timeout=60)
        present = res.returncode == 0
        first = (res.stdout.strip().splitlines() or [""])[0]
        tools[name] = {"present": present,
                       "version": (_semver(first) or first or None) if present else None}
    auth = collect_auth(run, tools, root=root, names=names)
    side_home = Path(home) if home is not None else Path.home()
    models = collect_models(run, tools, auth, expected_models(registry), home=side_home,
                            nonce=nonce, clis=clis)
    _fold_model_proof_into_auth(auth, models, clis)
    mechanism = collect_auth_mechanism(names, side_home, os.environ, models)
    expiry = {cli: credential_expiry(cli, side_home) for cli in names
              if (tools.get(cli) or {}).get("present") and SIGN_IN.get(cli) and SIGN_IN[cli].files}
    return {
        "python": py.stdout.strip() or None if py.returncode == 0 else None,
        "uv": _semver(uv.stdout) if uv.returncode == 0 else None,
        "uv_lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest() if lock.is_file() else None,
        "uv_sync_exit": sync.returncode,
        "tools": tools,
        "auth": auth,
        "models": models,
        "auth_mech": mechanism,
        "credential_expiry": expiry,
        "hooks": sorted(hooks) if hooks is not None else installed_hooks(run, root),
        "platform": {"system": platform.system(), "machine": platform.machine()},
    }


_HOOK_STATUS = re.compile(r"(Passed|Failed|Skipped)\s*$", re.MULTILINE)


def _hook_verdict(res: CmdResult) -> str:
    """pass | fail | skipped, read from pre-commit's own status word -- exit 0 alone cannot tell
    a hook that ran from one pre-commit skipped for want of files (a vacuous green)."""
    found = _HOOK_STATUS.findall(res.stdout or "")
    if res.returncode != 0:
        return "fail"
    return found[-1].lower() if found else "unknown"


def parse_junit(path: Path) -> dict[str, str]:
    """`classname::name` -> passed | failed | skipped | error. A missing or unparseable file is
    an EMPTY selection, which `compare_gates` refuses rather than reading as 'nothing differs'."""
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError):
        return {}
    out: dict[str, str] = {}
    for case in root.iter("testcase"):
        key = f"{case.get('classname', '')}::{case.get('name', '')}"
        if case.find("failure") is not None:
            out[key] = "failed"
        elif case.find("error") is not None:
            out[key] = "error"
        elif case.find("skipped") is not None:
            out[key] = "skipped"
        else:
            out[key] = "passed"
    return out


def collect_gates(run: Runner, *, root: Path = _REPO_ROOT, via_gate: bool = False) -> dict:
    """Condition 2's verdict set: the fixed hooks, `audit.py health`, the fixed pytest selection."""
    hooks = {}
    for hook in GATE_HOOKS:
        res = run(["uv", "run", "--locked", "pre-commit", "run", hook, "--hook-stage",
                   "pre-commit", "--all-files"], cwd=root, timeout=600)
        hooks[hook] = _hook_verdict(res)
    health = run(["uv", "run", "--locked", "python", "scripts/audit.py", "health"], cwd=root,
                 timeout=900)
    with tempfile.TemporaryDirectory() as tmp:
        xml = Path(tmp) / "junit.xml"
        pytest_argv = ["uv", "run", "--locked", "pytest", *GATE_TESTS, "-p", "no:cacheprovider",
                       "-q", "--junitxml", str(xml)]
        if via_gate:  # the gate computes and appends `-n <workers>`; verdicts do not depend on it
            argv = ["uv", "run", "--locked", "python", "scripts/memory_admission_gate.py", "run",
                    "--workers-flag", "-n", "--", *pytest_argv]
        else:
            argv = [*pytest_argv, "-n0"]
        run(argv, cwd=root, timeout=3600)
        tests = parse_junit(xml)
    return {"hooks": hooks, "audit_health": "pass" if health.returncode == 0 else "fail",
            "tests": tests}


def _exact_head(ls_remote_stdout: str, branch: str) -> Optional[str]:
    """The sha of `refs/heads/<branch>` itself. `git ls-remote <pattern>` also returns every
    head that merely ENDS with the pattern (`refs/heads/a/<branch>`), so the first line is not
    the branch (review finding, grok-4.7 P3)."""
    for line in (ls_remote_stdout or "").splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] == f"refs/heads/{branch}":
            return parts[0]
    return None


def collect_landing(run: Runner, *, root: Path = _REPO_ROOT,
                    push_branch: Optional[str] = None) -> dict:
    """Condition 3's facts. The push leg runs only when a branch name is given (the Codespace
    side); `ls-remote` is read back so the pushed sha is origin's, not this process's belief."""
    head = run(["git", "rev-parse", "HEAD"], cwd=root).stdout.strip()
    tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=root).stdout.strip()
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root).stdout.strip()
    dirty = bool(run(["git", "status", "--porcelain"], cwd=root).stdout.strip())
    landing: dict = {"pushed_branch": None, "pushed_sha": None, "push_exit": None}
    if push_branch:
        push = run(["git", "push", "origin", f"HEAD:refs/heads/{push_branch}"], cwd=root,
                   timeout=300)
        landing["push_exit"] = push.returncode
        if push.returncode == 0:
            listed = run(["git", "ls-remote", "--heads", "origin", push_branch], cwd=root,
                         timeout=120)
            sha = _exact_head(listed.stdout, push_branch) if listed.returncode == 0 else None
            if sha:
                landing["pushed_branch"], landing["pushed_sha"] = push_branch, sha
    return {"base_sha": head, "tree_sha": tree, "branch": branch, "dirty": dirty,
            "landing": landing}


def _probe_write(run: Runner, name: str) -> dict:
    """Condition 4's write leg: write ONE named file, read it back byte-for-byte, delete it, and
    list the remote to prove it is gone. The delete is attempted whenever the write succeeded,
    so a failing read-back cannot leave the probe behind; a file that survives is reported as
    `gone_after: False` and is the caller's to remove (the record names it)."""
    folder, _, leaf = name.rpartition("/")   # "" and the whole name for a root-level probe
    content = (f"{name}\nwritten by scripts/codespace_parity.py collect --probe-write\n"
               f"nonce {hashlib.sha256(os.urandom(16)).hexdigest()[:16]}\n")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / leaf
        src.write_text(content, encoding="utf-8", newline="\n")
        wrote = run(["rclone", "copyto", str(src), f"gdrive:{name}"], timeout=120)
    leg: dict = {"name": name, "write_exit": wrote.returncode, "readback_ok": False,
                 "delete_exit": None, "gone_after": None}
    if wrote.returncode == 0:
        back = run(["rclone", "cat", f"gdrive:{name}"], timeout=120)
        leg["readback_ok"] = back.returncode == 0 and back.stdout == content
        leg["delete_exit"] = run(["rclone", "deletefile", f"gdrive:{name}"], timeout=120).returncode
    # absence is read in the probe's OWN folder: a listing of the root would never show a file
    # that lives in `to-browser/`, and so would call a surviving probe gone
    listed = run(["rclone", "lsf", f"gdrive:{folder}", "--files-only", "--include", leaf],
                 timeout=120)
    if listed.returncode == 0:
        leg["gone_after"] = not listed.stdout.strip()
    return leg


def collect_transport(run: Runner, *, env: Optional[Mapping[str, str]] = None,
                      probe_write: Optional[str] = None) -> dict:
    """Condition 4's read leg -- and, when a contract names the file, its write leg
    (`probe_write`). The secret is a BOOLEAN here -- its value never enters a record."""
    if probe_write is not None and not _probe_name_ok(probe_write):
        raise ValueError(f"--probe-write {probe_write!r} is not a single plain file name "
                         "(letters, digits, '.', '_', '-'), optionally directly inside "
                         f"{' or '.join(d + '/' for d in TRANSPORT_PROBE_DIRS)}; a probe never "
                         "addresses any other path")
    env = os.environ if env is None else env
    ver = run(["rclone", "--version"], timeout=60)
    present = ver.returncode == 0
    out: dict = {
        "rclone": {"present": present,
                   "version": _semver((ver.stdout.strip().splitlines() or [""])[0]) if present else None},
        "token_present": bool(env.get("RCLONE_CONFIG_GDRIVE_TOKEN")),
        "read_exit": None,
        "read_entries": None,
    }
    if present:
        read = run(["rclone", "lsf", "gdrive:", "--max-depth", "1"], timeout=120)
        out["read_exit"] = read.returncode
        out["read_entries"] = (len([ln for ln in read.stdout.splitlines() if ln.strip()])
                               if read.returncode == 0 else None)
        # no write to a transport that could not even be read
        if probe_write is not None and read.returncode == 0 and out["read_entries"]:
            out["write"] = _probe_write(run, probe_write)
    return out


# ================================================ C3's integration leg (b2-codespace-green)

def _default_verdict(sha: str, **kw):
    """CI's one verdict for `sha` -- `merge_path.read_verdict`, the integrator's own reader."""
    try:  # pragma: no cover -- exercised by whichever path the caller uses
        from scripts import merge_path as mp
    except ImportError:  # pragma: no cover
        import merge_path as mp
    return mp.read_verdict(sha, **kw)


def collect_integration(run: Runner, *, root: Path, run_branch: str, scratch_branch: str, base: str,
                        outcome_test: Sequence[str], workdir: Path, ci_timeout_s: int = 3600,
                        ci_interval_s: int = 30, verdict_fn: Optional[Callable] = None,
                        onto: Optional[str] = None, ci_base: Optional[str] = None,
                        ci_reruns: int = 1, sleep_fn: Callable[[float], None] = time.sleep,
                        control: bool = True) -> dict:
    """The integrator's acts on the test lane's pushed branch, on a SCRATCH branch, never on main.

    1. read the run branch's tip on origin and fetch it;
    2. cut `scratch_branch` (`worktree-integrate-*`) from `onto` (default `base`) in a temporary
       worktree and merge the run tip into it with `--no-ff` -- the local merge the integrator
       does. `base` is the parity base the run branch must descend from; `onto` is what the
       integrator cuts from, origin/main: CI's spine job judges an integration-branch push as if
       it landed on main, so a scratch branch cut from a lane tip would show the lane's own
       commits as direct ones (b2-codespace-green run 2);
    3. re-run the outcome test on the merged tree;
    4. push the scratch branch alone and read CI's push verdict for the merge commit
       (`merge_path.read_verdict`, the one verdict function the merge path itself uses);
    5. ALWAYS delete the scratch branch on origin, the worktree and the local branch, and read each
       back -- `cleanup` records what was PROVEN gone, not what was asked.

    A leg that did not run leaves its key out of the record (`compare_landing` reads that as
    NOT-RUN); nothing here is ever pushed to `main`, and a scratch name that is not an integrate
    branch is refused before any command runs."""
    if not _SCRATCH_BRANCH_RE.fullmatch(scratch_branch):
        raise ValueError(f"scratch branch {scratch_branch!r} is not a `worktree-integrate-<slug>` "
                         "branch; the integration leg never pushes anywhere else")
    if not _RUN_BRANCH_RE.fullmatch(run_branch) or run_branch == scratch_branch:
        raise ValueError(f"run branch {run_branch!r} is not a `worktree-<slug>` branch")
    if not _FULL_SHA_RE.fullmatch(base):
        raise ValueError(f"base {base!r} is not a full 40-hex sha")
    onto = base if onto is None else onto
    if not _FULL_SHA_RE.fullmatch(onto):
        raise ValueError(f"onto {onto!r} is not a full 40-hex sha")
    # `ci_base` is the commit whose CI run the merge's run is judged AGAINST: main as it is now when
    # the caller knows it (CI runs the scratch branch against the current `main` ref, so an older
    # baseline reads every main-side change since as NEW -- b2-codespace-green run 5); default the
    # commit the scratch branch was cut from.
    ci_base = onto if ci_base is None else ci_base
    if not _FULL_SHA_RE.fullmatch(ci_base):
        raise ValueError(f"ci_base {ci_base!r} is not a full 40-hex sha")
    workdir = Path(workdir)
    record: dict = {"schema": SCHEMA, "side": "integration", "run_branch": run_branch,
                    "scratch_branch": scratch_branch, "base_sha": base, "onto_sha": onto, "ci_base_sha": ci_base, "run_sha": None,
                    "run_cut_from_base": None}
    listed = run(["git", "ls-remote", "--heads", "origin", run_branch], cwd=root, timeout=120)
    run_sha = _exact_head(listed.stdout, run_branch) if listed.returncode == 0 else None
    if not run_sha:
        record["note"] = f"the run branch {run_branch} is not on origin: nothing to merge"
        return record
    record["run_sha"] = run_sha
    fetched = run(["git", "fetch", "origin", run_branch], cwd=root, timeout=300)
    if fetched.returncode != 0:
        record["note"] = f"git fetch of {run_branch} exited {fetched.returncode}"
        return record

    created = pushed = control_pushed = False
    try:
        added = run(["git", "worktree", "add", "-b", scratch_branch, str(workdir), onto],
                    cwd=root, timeout=300)
        if added.returncode != 0:
            record["note"] = f"git worktree add exited {added.returncode}"
            return record
        created = True
        merge_base = run(["git", "merge-base", base, run_sha], cwd=root, timeout=120)
        record["run_cut_from_base"] = (merge_base.returncode == 0
                                       and merge_base.stdout.strip() == base)
        merged = run(["git", "merge", "--no-ff", "--no-edit", "-m",
                      f"Merge {run_branch} @ {run_sha[:8]} (parity integration leg, scratch)",
                      run_sha], cwd=workdir, timeout=300)
        record["merge"] = {"exit": merged.returncode, "sha": None, "parents": []}
        if merged.returncode != 0:
            resolved = _resolve_union_conflicts(
                workdir, f"Merge {run_branch} @ {run_sha[:8]} (parity integration leg, scratch)")
            if not resolved:
                return record
            record["merge"].update({"exit": 0, "resolved": resolved})
        head = run(["git", "rev-parse", "HEAD"], cwd=workdir, timeout=60).stdout.strip()
        parents = run(["git", "rev-list", "--parents", "-n", "1", "HEAD"], cwd=workdir,
                      timeout=60).stdout.split()
        record["merge"].update(sha=head or None, parents=parents[1:])
        tested = run(list(outcome_test), cwd=workdir, timeout=3600)
        counted = re.search(r"(\d+) passed", tested.stdout or "")
        record["outcome_test"] = {"argv": list(outcome_test), "exit": tested.returncode,
                                  "passed": int(counted.group(1)) if counted else 0}
        if tested.returncode != 0 or not head:
            return record
        push = run(["git", "push", "origin", f"HEAD:refs/heads/{scratch_branch}"], cwd=workdir,
                   timeout=300)
        pushed = push.returncode == 0
        record["push_exit"] = push.returncode
        if pushed:
            baseline = ci_base
            if control:
                # An EMPTY commit on `onto`, pushed beside the merge: CI judges both against the
                # main it fetches NOW, so whatever main's motion or the branch shape turns red
                # turns red in both, and the merge is judged against the control (runs 6, 9, 10).
                control_branch = f"{scratch_branch}-control"
                record["control"] = {"branch": control_branch, "sha": None, "push_exit": None}
                tree = run(["git", "rev-parse", f"{onto}^{{tree}}"], cwd=workdir, timeout=60)
                made = run(["git", "commit-tree", tree.stdout.strip(), "-p", onto, "-m",
                            "control: no lane content (parity integration leg, scratch)"],
                           cwd=workdir, timeout=60)
                control_sha = made.stdout.strip() if made.returncode == 0 else ""
                if _FULL_SHA_RE.fullmatch(control_sha):
                    cpush = run(["git", "push", "origin",
                                 f"{control_sha}:refs/heads/{control_branch}"], cwd=workdir,
                                timeout=300)
                    record["control"].update(sha=control_sha, push_exit=cpush.returncode)
                    control_pushed = cpush.returncode == 0
                if control_pushed:
                    baseline = control_sha
                    if not _wait_run_completed(run, root, control_branch, ci_timeout_s,
                                               ci_interval_s, sleep_fn):
                        record["control_note"] = (
                            f"the control run on {control_branch} had not completed within "
                            f"{ci_timeout_s}s: a baseline that is not completed reads UNATTRIBUTED")
                else:
                    record["control_note"] = ("the control commit was not pushed: the baseline "
                                              "stays ci_base, main's tip")
            record["ci"] = _read_ci(head, base=baseline, root=root, timeout_s=ci_timeout_s,
                                    interval_s=ci_interval_s, verdict_fn=verdict_fn)
            attempts = [record["ci"]]
            for _ in range(max(0, ci_reruns)):
                if not _rerunnable(record["ci"]):
                    break
                listed_main = run(["git", "ls-remote", "--heads", "origin", "main"], cwd=root,
                                  timeout=120)
                main_now = _exact_head(listed_main.stdout, "main") if listed_main.returncode == 0 else None
                if main_now != onto:
                    record["ci_rerun_note"] = (
                        f"main moved from {onto} to {main_now or '(unreadable)'} since the "
                        "scratch branch was cut: a re-run would judge a tree that lacks it")
                    break
                started, why = _rerun_failed(run, root, record["ci"]["run_id"], sleep_fn)
                if not started:
                    record["ci_rerun_note"] = why
                    break
                record["ci"] = _read_ci(head, base=baseline, root=root, timeout_s=ci_timeout_s,
                                        interval_s=ci_interval_s, verdict_fn=verdict_fn)
                attempts.append(record["ci"])
            if len(attempts) > 1:
                record["ci_attempts"] = attempts
        return record
    finally:
        if control_pushed:
            run(["git", "push", "origin", "--delete", f"{scratch_branch}-control"], cwd=root,
                timeout=300)
        if pushed:
            run(["git", "push", "origin", "--delete", scratch_branch], cwd=root, timeout=300)
        if created:
            run(["git", "worktree", "remove", "--force", str(workdir)], cwd=root, timeout=300)
            # DECIDED-BY-LANE: `-D`, not `-d`. The scratch branch is unmerged into main BY DESIGN
            # (it is the test lane's merge, never landed), so `-d` can only refuse; it is this
            # call's own branch, created above, and deleted only after it was pushed or abandoned.
            run(["git", "branch", "-D", scratch_branch], cwd=root, timeout=60)
        record["cleanup"] = _read_cleanup(run, root, scratch_branch, workdir,
                                          f"{scratch_branch}-control" if control_pushed else None)


def default_onto(run: Runner, *, root: Path, base: str) -> str:
    """The main commit the integrator cuts its scratch branch from: origin/main's tip, after a fetch.

    CI judges a pushed integration branch as if it landed on main now, so a tree cut from an older
    main fails the checks that main's newer commits satisfy (b2-codespace-green run 6: three spine
    entries anchored by main's newer JOURNAL read as unanchored, 38 handoff-cut tests red). A lane
    that main has outrun is the integrator's re-sync, done before the lane is frozen; a merge that
    conflicts here says the lane is not synced, and the record carries that exit."""
    fetched = run(["git", "fetch", "origin", "main"], cwd=root, timeout=300)
    if fetched.returncode != 0:
        raise ValueError(f"git fetch origin main exited {fetched.returncode}: pass --onto explicitly")
    found = run(["git", "rev-parse", "origin/main"], cwd=root, timeout=120)
    onto = found.stdout.strip() if found.returncode == 0 else ""
    if not _FULL_SHA_RE.fullmatch(onto):
        raise ValueError(f"cannot read origin/main: pass --onto explicitly (base {base})")
    return onto


def _read_ci(sha: str, *, base: str, root: Path, timeout_s: int, interval_s: int,
             verdict_fn: Optional[Callable]) -> dict:
    try:
        verdict = (verdict_fn or _default_verdict)(sha, base=base, root=root, timeout_s=timeout_s,
                                                   interval_s=interval_s)
    except Exception as exc:  # noqa: BLE001 -- an unreadable CI is NOT-RUN, said by name
        return {"sha": sha, "state": "GH-UNAVAILABLE", "landable": False, "run_id": None,
                "missing_contexts": [], "reason": f"{type(exc).__name__}: {exc}"[:300]}
    state = str(getattr(verdict, "state", "") or "")
    missing = [str(c) for c in (getattr(verdict, "missing_contexts", ()) or ())]
    return {"sha": sha, "state": state, "landable": state in CI_LANDABLE_STATES and not missing,
            "run_id": getattr(verdict, "run_id", None), "missing_contexts": missing,
            "reason": str(getattr(verdict, "reason", "") or "")[:300],
            "new_reds": [str(r) for r in (getattr(verdict, "new_reds", ()) or ())][:40],
            "flagged": [str(f) for f in (getattr(verdict, "flagged", ()) or ())][:20]}


def _wait_run_completed(run: Runner, root: Path, branch: str, timeout_s: int, interval_s: int,
                        sleep_fn: Callable[[float], None]) -> bool:
    """Poll the newest push run on `branch` until its status is `completed` (True), or give up
    after `timeout_s` of polling every `interval_s` (False). A listing that cannot be read is one
    more poll that did not complete."""
    step = max(1, int(interval_s))
    for attempt in range(max(1, int(timeout_s) // step)):
        if attempt:
            sleep_fn(interval_s)
        listed = run(["gh", "run", "list", "--branch", branch, "--event", "push", "--limit", "1",
                      "--json", "status"], cwd=root, timeout=120)
        try:
            rows = json.loads(listed.stdout) if listed.returncode == 0 else []
        except ValueError:
            rows = []
        if rows and isinstance(rows[0], dict) and rows[0].get("status") == "completed":
            return True
    return False


def _rerunnable(ci: Mapping) -> bool:
    """A verdict worth one re-run: REGRESSED by named TESTS alone (the count closes: N named, N
    counted, no non-test failure, no broken job, no missing context), with a run to re-run, and not
    already only declared cases. Anything else is a measured red, not a flake candidate."""
    counts = _CI_RED_COUNTS_RE.match(str(ci.get("reason") or ""))
    reds = ci.get("new_reds") or []
    return bool(ci.get("state") == "REGRESSED" and ci.get("run_id") and counts and reds
                and int(counts.group(1)) == len(reds) and not ci.get("missing_contexts")
                and not _declared_only_reds(ci))


def _rerun_failed(run: Runner, root: Path, run_id, sleep_fn: Callable[[float], None]) -> tuple[bool, str]:
    """`gh run rerun <id> --failed`, then wait for the run to leave `completed` -- a verdict read
    straight after the request would still be the OLD attempt's."""
    asked = run(["gh", "run", "rerun", str(run_id), "--failed"], cwd=root, timeout=120)
    if asked.returncode != 0:
        return False, f"CI re-run of run {run_id} refused (exit {asked.returncode})"
    for _ in range(24):
        seen = run(["gh", "run", "view", str(run_id), "--json", "status", "--jq", ".status"],
                   cwd=root, timeout=60)
        if seen.returncode == 0 and seen.stdout.strip() not in ("", "completed"):
            return True, ""
        sleep_fn(5)
    return False, f"CI re-run of run {run_id} never started: the run stayed completed"


def _read_cleanup(run: Runner, root: Path, scratch_branch: str, workdir: Path,
                  control_branch: Optional[str] = None) -> dict:
    """What is PROVEN gone, each read back: the scratch ref on origin, the worktree, the local
    branch, and the control ref when one was pushed. A read that could not be made is False --
    'could not look' is not 'gone'."""
    heads = run(["git", "ls-remote", "--heads", "origin", scratch_branch], cwd=root, timeout=120)
    remote_gone = heads.returncode == 0 and _exact_head(heads.stdout, scratch_branch) is None
    trees = run(["git", "worktree", "list", "--porcelain"], cwd=root, timeout=60)
    here = Path(workdir).as_posix().lower()
    worktree_gone = trees.returncode == 0 and here not in trees.stdout.replace("\\", "/").lower()
    local = run(["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{scratch_branch}"],
                cwd=root, timeout=60)
    out = {"remote_deleted": remote_gone, "worktree_removed": worktree_gone,
           "local_branch_removed": local.returncode != 0 and local.returncode != 127}
    if control_branch:
        ctl = run(["git", "ls-remote", "--heads", "origin", control_branch], cwd=root, timeout=120)
        out["control_remote_deleted"] = (ctl.returncode == 0
                                         and _exact_head(ctl.stdout, control_branch) is None)
    return out


#: Append-only / newest-first logs a lane and main both write at the same end, so a textual
#: conflict on them means two entries, not two opinions. The integrator keeps both; so does this.
UNION_MERGE_FILES: tuple[str, ...] = ("JOURNAL.md", "logs/MERGE-RECEIPTS.jsonl")


def _resolve_union_conflicts(workdir: Path, message: str) -> list[str]:
    """After a conflicted `git merge` in `workdir`: when EVERY conflicted file is a
    `UNION_MERGE_FILES` log, keep both sides' lines (`git merge-file --union`), stage them and
    commit the merge. Returns the resolved files, or `[]` having changed nothing."""
    def git(*args: str, data: Optional[bytes] = None):
        return subprocess.run(["git", *args], cwd=str(workdir), capture_output=True, input=data,
                              timeout=120, check=False)

    try:
        listed = git("diff", "--name-only", "--diff-filter=U")
    except (OSError, subprocess.SubprocessError):  # no worktree to resolve in: nothing resolved
        return []
    files = [ln.strip() for ln in listed.stdout.decode("utf-8", "replace").splitlines() if ln.strip()]
    if listed.returncode != 0 or not files or any(f not in UNION_MERGE_FILES for f in files):
        return []
    merged: dict[str, bytes] = {}
    for name in files:
        stages = [git("show", f":{n}:{name}") for n in (2, 1, 3)]
        if any(s.returncode != 0 for s in stages):
            return []
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for label, s in zip(("ours", "base", "theirs"), stages):
                p = Path(tmp) / label
                p.write_bytes(s.stdout)
                paths.append(str(p))
            joined = subprocess.run(["git", "merge-file", "-p", "--union", *paths], capture_output=True,
                                    timeout=120, check=False)
        if joined.returncode < 0 or joined.returncode > 127:
            return []
        merged[name] = joined.stdout
    for name, body in merged.items():
        (Path(workdir) / name).write_bytes(body)
        if git("add", "--", name).returncode != 0:
            return []
    done = git("commit", "-m", message, "-m", "kill-candidates: none - a scratch merge files no row")
    return files if done.returncode == 0 else []


def collect_record(run: Runner = default_run, *, root: Path = _REPO_ROOT, side: str = "",
                   push_branch: Optional[str] = None, via_gate: bool = False,
                   skip_gates: bool = False, probe_write: Optional[str] = None) -> dict:
    if probe_write is not None and not _probe_name_ok(probe_write):
        # refused BEFORE the gates run: a bad name must not cost a long collect to find out
        raise ValueError(f"--probe-write {probe_write!r} is not a single plain file name, or "
                         "one file directly inside to-browser/")
    if not side:
        side = "codespace" if os.environ.get("CODESPACES") == "true" else "local"
    landing = collect_landing(run, root=root, push_branch=push_branch)  # first: before any run dirties the tree
    return {
        "schema": SCHEMA,
        "side": side,
        "os": platform.system(),
        "base_sha": landing["base_sha"],
        "tree_sha": landing["tree_sha"],
        "branch": landing["branch"],
        "dirty": landing["dirty"],
        "environment": collect_environment(run, root=root),
        "gates": ({"hooks": {}, "audit_health": None, "tests": {}} if skip_gates
                  else collect_gates(run, root=root, via_gate=via_gate)),
        "landing": landing["landing"],
        "transport": collect_transport(run, probe_write=probe_write),
    }


def write_record(path: Path, record: Mapping) -> None:
    Path(path).write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8",
                          newline="\n")


# ============================================================================ cost

def core_hours(created: Optional[datetime], deleted: Optional[datetime], machine: str) -> float:
    if machine not in MACHINE_CORES:
        raise ValueError(f"unknown Codespace machine type {machine!r} -- refusing to price it at "
                         f"zero (known: {', '.join(sorted(MACHINE_CORES))})")
    return _regime.uptime_minutes(created, deleted) / 60.0 * MACHINE_CORES[machine]


# =========================================================================== comparators

def compare_environment(local: Mapping, remote: Mapping,
                        registry: Optional[Mapping] = None) -> Verdict:
    le, re_ = local["environment"], remote["environment"]
    registry = load_registry() if registry is None else registry
    names = lane_tools(registry)
    clis = model_clis(registry)
    problems: list[str] = []
    evidence: list[str] = []
    for key in sorted(set(le) | set(re_)):
        if key in OS_SPECIFIC_ENTRIES:
            evidence.append(f"{key}: declared OS-specific ({OS_SPECIFIC_ENTRIES[key]}) -- "
                            f"local={le.get(key)} codespace={re_.get(key)}")
            continue
        if key in ("tools", "uv_sync_exit", "hooks", "auth", "models", "auth_mech",
                   "credential_expiry"):
            continue    # compared below, each with its own verdict wording
        lv, rv = le.get(key), re_.get(key)
        evidence.append(f"{key}: local={lv} codespace={rv}")
        if lv != rv or lv is None:
            problems.append(f"{key} differs (local={lv} codespace={rv})")
    for side, env in (("local", le), ("codespace", re_)):
        evidence.append(f"uv sync --locked exit ({side})={env.get('uv_sync_exit')}")
        if env.get("uv_sync_exit") != 0:
            problems.append(f"uv sync --locked exit {env.get('uv_sync_exit')} on {side}")
    for name in names:
        lt = le.get("tools", {}).get(name, {"present": False, "version": None})
        rt = re_.get("tools", {}).get(name, {"present": False, "version": None})
        evidence.append(f"{name} version local={lt.get('version')} codespace={rt.get('version')}")
        if not lt.get("present") and not rt.get("present"):
            problems.append(f"{name} absent on both sides")
        elif lt.get("present") != rt.get("present"):
            where = "codespace" if lt.get("present") else "local"
            problems.append(f"{name} absent on {where}")
        elif lt.get("version") != rt.get("version"):
            problems.append(f"{name} version skew (local={lt.get('version')} "
                            f"codespace={rt.get('version')})")
    lh, rh = list(le.get("hooks", [])), list(re_.get("hooks", []))
    evidence.append(f"hook set local={lh} codespace={rh}")
    if sorted(lh) != sorted(rh) or not lh:
        problems.append(f"hook set differs (local={lh} codespace={rh})")
    model_named = _compare_models(le, re_, registry, problems, evidence)
    _compare_auth_mechanism(le, re_, clis, problems, evidence)
    _compare_credential_expiry(le, re_, problems, evidence)
    auth_items = _auth_items(le, re_, evidence, model_named, names)
    for name in names:     # an auth probe that never ran is a FAIL, not a named exception
        if ((re_.get("auth") or {}).get(name) or {}).get("state") == "probe-error":
            problems.append(f"the auth probe for {name} could not run on the codespace -- its "
                            "login state is unknown")
    if problems:
        return _verdict(1, "FAIL", "; ".join(problems), evidence)
    if auth_items:
        return _verdict(1, "PASS", "except named auth items: " + ", ".join(auth_items), evidence)
    return _verdict(1, "PASS", "", evidence)


def _compare_models(le: Mapping, re_: Mapping, registry: Mapping, problems: list[str],
                    evidence: list[str]) -> set[str]:
    """Each model CLI's served id against the registry (R61), on both sides. Returns the CLIs the
    CODESPACE could not probe for want of a login: they are named as auth items, never failed, never
    passed silently. The workstation is the reference, so a local CLI with no served id fails."""
    expected = expected_models(registry)
    clis = model_clis(registry)
    named: set[str] = set()
    if not clis:
        problems.append("the registry names no provider with a CLI: C1 would probe nothing, and a "
                        "check that probes nothing proves nothing")
    for cli in clis:
        if not expected[cli].id:
            problems.append(f"the registry names no model for {cli} ({expected[cli].where}): "
                            "its served id cannot be checked")
    for side, env in (("local", le), ("codespace", re_)):
        models = env.get("models")
        if not isinstance(models, Mapping):
            problems.append(f"no served model id on the {side}: the record has no model probe "
                            f"({', '.join(clis)})")
            continue
        for cli in clis:
            rec = models.get(cli) or {}
            state, served, exp = rec.get("state"), rec.get("served_id"), expected[cli]
            if state == "tool-absent":
                continue    # reported once, by the tool comparison above
            if state in ("not-probed-auth", "unauthenticated") and side == "codespace":
                evidence.append(f"served model {cli} {side}: not probed -- login missing "
                                "(a named auth item)")
                named.add(cli)
                continue
            if state == "served" and served:
                evidence.append(f"served model {cli} {side}={served} registry={exp.id} ({exp.where})")
                if exp.id and not served_matches(cli, served, exp.id):
                    problems.append(f"{cli} served {served!r} on the {side} but the registry routes "
                                    f"it to {exp.id!r} ({exp.where})")
                continue
            detail = rec.get("detail") or "no detail recorded"
            evidence.append(f"served model {cli} {side}: none ({state or 'no record'})")
            problems.append(f"{cli} returned no served model id on the {side} "
                            f"({state or 'no record'}: {detail})")
    return named


def _compare_auth_mechanism(le: Mapping, re_: Mapping, clis: Sequence[str], problems: list[str],
                            evidence: list[str]) -> None:
    """R87: a model CLI must sign in on the Codespace the way it signs in on the laptop. A CLI that
    answers there through an API key the laptop does not use -- or through any mechanism class the
    laptop does not -- is a FAIL naming both, even when its served id matches the registry. A record
    that carries no mechanism section on EITHER side is an older record and is not judged; a laptop
    that recorded one against a Codespace that did not is a FAIL (no vacuous pass)."""
    lm, rm = le.get("auth_mech"), re_.get("auth_mech")
    if not isinstance(lm, Mapping) and not isinstance(rm, Mapping):
        return
    if not isinstance(lm, Mapping) or not isinstance(rm, Mapping):
        where = "codespace" if isinstance(lm, Mapping) else "local"
        problems.append(f"no auth mechanism recorded on the {where}: the sign-in each CLI uses "
                        "cannot be compared with the other side's")
        return
    for cli in clis:
        ours, theirs = lm.get(cli) or {}, rm.get(cli) or {}
        lc, rc = ours.get("class"), theirs.get("class")
        evidence.append(f"auth mechanism {cli}: local={lc} ({ours.get('via')}) "
                        f"codespace={rc} ({theirs.get('via')})")
        if lc is None or rc is None:
            problems.append(f"no auth mechanism recorded for {cli} on the "
                            f"{'local' if lc is None else 'codespace'} side")
        elif lc != rc and (lc, rc) not in AUTH_EQUIVALENT | AUTH_EQUIVALENT_FOR.get(cli, frozenset()):
            problems.append(f"{cli} signs in by {rc} on the codespace but by {lc} on the laptop: not "
                            "the laptop's own sign-in (R87)")


def _compare_credential_expiry(le: Mapping, re_: Mapping, problems: list[str],
                               evidence: list[str]) -> None:
    """A recorded `expired` credential on either side is a FAIL that names the ONE renew step
    (R59, R65): the failure is reported before a lane runs on it."""
    for side, env in (("local", le), ("codespace", re_)):
        for cli, rec in sorted((env.get("credential_expiry") or {}).items()):
            state = (rec or {}).get("state")
            evidence.append(f"credential {cli} {side}: {state} ({(rec or {}).get('detail', '')})")
            spec = SIGN_IN.get(cli)
            if side == "codespace" and not (spec and spec.route == "mirror"
                                            and spec.refresh in ("safe", "guarded")):
                # a cache the launch never copies is absent there by design (claude signs in by the
                # setup-token variable): its mechanism is compared by `_compare_auth_mechanism`
                continue
            if state == "expired":
                problems.append(f"the {cli} credential on the {side} side has expired -- "
                                f"OPERATOR-ACTION: {(rec or {}).get('renew') or 'renew its sign-in'}")


def _auth_items(le: Mapping, re_: Mapping, evidence: list[str],
                model_named: Sequence[str] = (), names: Optional[Sequence[str]] = None) -> list[str]:
    """The tools the Codespace has installed but not logged in, each named with what it needs.

    An exception is only ever NAMED here -- it neither fails condition 1 (installation is what
    condition 1 measures) nor passes silently. A record with no `auth` section (an older one)
    names nothing, so no exception can be invented for a side that was never probed. A CLI whose
    model call found the login missing (`model_named`) is named even where its auth state was
    `unprobed`, which is the only state `grok` and `agy` can have before they answer."""
    named: list[str] = []
    for name in (names if names is not None else lane_tools()):
        theirs = (re_.get("auth") or {}).get(name)
        if ((re_.get("models") or {}).get(name) or {}).get("state") in ("no-answer", "no-credits"):
            continue    # a call that ran and gave nothing is its own FAIL, never a login item
        if name not in model_named and (
                not theirs or theirs.get("state") in ("authenticated", "tool-absent", "probe-error")):
            continue    # tool-absent and probe-error are each their own FAIL, not an exception
        ours = ((le.get("auth") or {}).get(name) or {}).get("state")
        evidence.append(f"AUTH-ITEM {name}: codespace={(theirs or {}).get('state', 'unprobed')} "
                        f"local={ours} -- needs {AUTH_NEEDS.get(name, 'a sign-in for ' + name)}")
        named.append(name)
    return named


def compare_gates(local: Mapping, remote: Mapping) -> Verdict:
    lg, rg = local["gates"], remote["gates"]
    problems: list[str] = []
    evidence: list[str] = []
    for side, g in (("local", lg), ("codespace", rg)):
        if not g.get("tests"):
            problems.append(f"empty pytest selection on {side} -- nothing ran, nothing to compare")
        hooks = g.get("hooks") or {}
        unexercised = [h for h in GATE_HOOKS if hooks.get(h) in (None, "", "unknown", "skipped")]
        if unexercised or g.get("audit_health") not in ("pass", "fail"):
            problems.append(f"the pre-commit hooks or audit.py health never ran on {side} -- two "
                            "empty verdict sets compare equal on nothing")
    flat_l: dict[str, str] = {}
    flat_r: dict[str, str] = {}
    for src, dst in ((lg, flat_l), (rg, flat_r)):
        for hook, v in (src.get("hooks") or {}).items():
            dst[hook] = v
        dst["audit.py health"] = src.get("audit_health")
        for node, v in (src.get("tests") or {}).items():
            dst[node] = v
    differing = []
    for key in sorted(set(flat_l) | set(flat_r)):
        lv, rv = flat_l.get(key), flat_r.get(key)
        if lv == rv:
            continue
        if key in DECLARED_OS_CASES and key not in declared_cases_problems():
            evidence.append(f"declared OS case {key} -> {DECLARED_OS_CASES[key]} "
                            f"(local={lv} codespace={rv})")
            continue
        differing.append(f"{key} (local={lv} codespace={rv})")
    evidence.append(f"compared {len(set(flat_l) | set(flat_r))} verdicts; "
                    f"{len(differing)} differ, {len(DECLARED_OS_CASES)} declared case(s)")
    if differing:
        problems.append(f"{len(differing)} verdict(s) differ: " + "; ".join(differing[:12])
                        + (f"; +{len(differing) - 12} more" if len(differing) > 12 else ""))
    if problems:
        return _verdict(2, "FAIL", " | ".join(problems), evidence)
    return _verdict(2, "PASS", "", evidence)


def stamp_lane(run: Runner, *, root: Path, record_path: Path, branch: str) -> dict:
    """Write `lane` = {branch, sha} into the Codespace record: the branch the test lane worked and
    the tip it resolves to IN THIS TREE. Run in the Codespace after the lane pushed, so C3 can
    refuse an integration record for any other branch or tip. A branch that does not resolve, or a
    tip that is not a full sha, writes nothing."""
    if not _RUN_BRANCH_RE.fullmatch(branch):
        raise ValueError(f"lane branch {branch!r} is not a `worktree-<slug>` branch")
    res = run(["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"], cwd=root,
              timeout=60)
    if res.returncode != 0:
        raise ValueError(f"could not resolve refs/heads/{branch} in {root} (exit "
                         f"{res.returncode}): nothing stamped")
    sha = res.stdout.strip()
    if not _FULL_SHA_RE.fullmatch(sha):
        raise ValueError(f"{branch} resolved to {sha!r}, which is not a full sha: nothing stamped")
    record = json.loads(Path(record_path).read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise ValueError(f"{record_path} is not a JSON object")
    record["lane"] = {"branch": branch, "sha": sha}
    write_record(Path(record_path), record)
    return record["lane"]


def lane_binding(remote: Optional[Mapping]) -> Optional[tuple[str, str]]:
    """The (branch, tip) the Codespace record says its test lane worked -- `lane`, stamped by
    `stamp-lane` after the lane ran -- or None when the record carries no usable one. Anything
    but a non-empty branch string and a full 40-hex tip is unmeasured, never a partial binding."""
    lane = (remote or {}).get("lane") if isinstance(remote, Mapping) else None
    if not isinstance(lane, Mapping):
        return None
    branch, sha = lane.get("branch"), lane.get("sha")
    if (isinstance(branch, str) and branch and isinstance(sha, str)
            and _FULL_SHA_RE.fullmatch(sha)):
        return branch, sha
    return None


def integration_legs(local: Mapping, integration: Optional[Mapping],
                     evidence: list[str], remote: Optional[Mapping] = None) -> list[LegResult]:
    """C3's integrator legs, each judged from what `integrate` MEASURED. A leg whose record is
    absent or carries no result is `NOT_RUN`; one that ran and failed is `FAIL`; only a measured
    pass is `PASS`. CI is judged by its STATE (`landable` is a convenience flag, never trusted).

    BOUND TO THIS RUN (review P1-1): the merge leg also compares the integration record's
    `run_branch` / `run_sha` with the lane branch and tip the CODESPACE record says it worked
    (`lane_binding`). A green record for another branch, or a stale one cut from the same base at
    an earlier tip, is a FAIL naming both; a Codespace record that names no lane is NOT-RUN -- the
    binding was not measured, so the leg cannot pass."""
    if not isinstance(integration, Mapping):
        return [LegResult(Leg.NOT_RUN, f"merge leg NOT-RUN: {LANDING_MERGE_NOT_RUN_REASON}")]
    legs: list[LegResult] = []
    base = local.get("base_sha")

    merge = integration.get("merge")
    if not isinstance(merge, Mapping) or merge.get("exit") is None:
        legs.append(LegResult(Leg.NOT_RUN, "merge leg NOT-RUN: no merge was attempted "
                              f"({integration.get('note') or 'the record carries none'})"))
    else:
        parents = list(merge.get("parents") or [])
        evidence.append(f"merge: {integration.get('scratch_branch')} merged "
                        f"{integration.get('run_branch')} at {integration.get('run_sha')} onto "
                        f"{integration.get('onto_sha') or integration.get('base_sha')} (base "
                        f"{integration.get('base_sha')}) -> {merge.get('sha')} "
                        f"(exit {merge.get('exit')})")
        if merge.get("resolved"):
            evidence.append("merge conflicts kept both sides of: " + ", ".join(merge["resolved"]))
        control = integration.get("control")
        if isinstance(control, Mapping) and control.get("sha"):
            evidence.append(f"CI baseline: the control commit {control['sha']} on "
                            f"{control.get('branch')} (cut from the same onto, no lane content)")
        elif integration.get("control_note"):
            evidence.append(f"CI baseline: main's tip -- {integration['control_note']}")
        bad = []
        if integration.get("base_sha") != base:
            bad.append(f"the integration base {integration.get('base_sha')} is not the compared "
                       f"base {base}")
        if integration.get("run_cut_from_base") is not True:
            bad.append("the run branch was not cut from the compared base")
        if merge.get("exit") != 0:
            bad.append(f"merge exit {merge.get('exit')}")
        elif len(parents) != 2:
            bad.append(f"the merge commit is not a two-parent merge ({len(parents)} parent(s))")
        else:
            onto_sha = integration.get("onto_sha") or integration.get("base_sha")
            if parents[0] != onto_sha:
                bad.append(f"the merge's first parent {parents[0]} is not the commit the scratch "
                           f"branch was cut from ({onto_sha})")
            if parents[1] != integration.get("run_sha"):
                bad.append(f"the merge's second parent {parents[1]} is not the run branch tip")
        bound = lane_binding(remote)
        if bound is not None:
            lane_branch, lane_sha = bound
            if integration.get("run_branch") != lane_branch:
                bad.append(f"the integration record merged {integration.get('run_branch')}, not "
                           f"the lane branch {lane_branch} this Codespace worked")
            if integration.get("run_sha") != lane_sha:
                bad.append(f"the integration record merged {integration.get('run_sha')}, not the "
                           f"tip {lane_sha} of the lane branch this Codespace worked")
            if not bad:
                evidence.append(f"bound to this run: {lane_branch} at {lane_sha} is the branch "
                                "and tip the Codespace worked and the integration merged")
        if bad:
            legs.append(LegResult(Leg.FAIL, "; ".join(bad)))
        elif bound is None:
            legs.append(LegResult(Leg.NOT_RUN, "merge leg NOT-RUN: the Codespace record carries "
                                  "no `lane` (branch and tip) to bind the integration record to "
                                  "(run `stamp-lane` in the Codespace after the lane pushed)"))
        else:
            legs.append(LegResult(Leg.PASS, "merge"))

    outcome = integration.get("outcome_test")
    if not isinstance(outcome, Mapping) or outcome.get("exit") is None:
        legs.append(LegResult(Leg.NOT_RUN, "outcome test NOT-RUN: it was not re-run on the merge"))
    else:
        evidence.append(f"outcome test: exit {outcome.get('exit')}, {outcome.get('passed')} "
                        f"passed ({' '.join(outcome.get('argv') or [])})")
        if outcome.get("exit") != 0:
            legs.append(LegResult(Leg.FAIL, f"outcome test exit {outcome.get('exit')} on the merge"))
        elif not isinstance(outcome.get("passed"), int) or outcome["passed"] < 1:
            legs.append(LegResult(Leg.FAIL, "outcome test passed no test on the merge (a run that "
                                  "selected nothing is not a pass)"))
        else:
            legs.append(LegResult(Leg.PASS, "outcome test"))

    ci = integration.get("ci")
    state = str((ci or {}).get("state") or "") if isinstance(ci, Mapping) else ""
    if not isinstance(ci, Mapping):
        legs.append(LegResult(Leg.NOT_RUN, "CI verdict NOT-RUN: the scratch branch's push run "
                              "was not read"))
    else:
        evidence.append(f"CI: {state or '(no state)'} for {ci.get('sha')} (run {ci.get('run_id')}"
                        f"; missing contexts {list(ci.get('missing_contexts') or [])})")
        merge_sha = (merge or {}).get("sha") if isinstance(merge, Mapping) else None
        attempts = integration.get("ci_attempts")
        if isinstance(attempts, list) and len(attempts) > 1:
            evidence.append("CI re-run (failed jobs only): " + " -> ".join(
                f"attempt {i} {a.get('state')} (run {a.get('run_id')})"
                + (f" [{'; '.join(map(str, a.get('new_reds') or []))}]" if a.get("new_reds") else "")
                for i, a in enumerate(attempts, 1) if isinstance(a, Mapping)))
        if integration.get("ci_rerun_note"):
            evidence.append(f"CI re-run NOT made: {integration['ci_rerun_note']}")
        declared =_declared_only_reds(ci) if state == "REGRESSED" else None
        if declared:
            evidence.append("declared CI case(s), the ONLY reds: " + "; ".join(
                f"{k} -> {DECLARED_CI_CASES[k]}" for k in declared))
            if merge_sha and ci.get("sha") != merge_sha:
                legs.append(LegResult(Leg.FAIL, f"the CI verdict is for {ci.get('sha')}, not the "
                                      f"merge commit {merge_sha}"))
            else:
                legs.append(LegResult(Leg.PASS, "CI verdict (declared cases only)"))
        elif state in CI_FAILED_STATES:
            legs.append(LegResult(Leg.FAIL, f"CI verdict {state}: {ci.get('reason') or 'red'}"))
        elif state in CI_LANDABLE_STATES:
            if merge_sha and ci.get("sha") != merge_sha:
                legs.append(LegResult(Leg.FAIL, f"the CI verdict is for {ci.get('sha')}, not the "
                                      f"merge commit {merge_sha}"))
            elif ci.get("missing_contexts"):
                legs.append(LegResult(Leg.FAIL, "CI verdict has missing required contexts: "
                                      + ", ".join(map(str, ci["missing_contexts"]))))
            else:
                legs.append(LegResult(Leg.PASS, "CI verdict"))
        else:
            legs.append(LegResult(Leg.NOT_RUN, f"CI verdict NOT-RUN: state {state!r} is not a "
                                  "measured pass or fail"))

    cleanup = integration.get("cleanup")
    if not isinstance(cleanup, Mapping):
        legs.append(LegResult(Leg.NOT_RUN, "scratch cleanup NOT-RUN: nothing was read back"))
    else:
        keys = ["remote_deleted", "worktree_removed", "local_branch_removed"]
        if "control_remote_deleted" in cleanup:
            keys.append("control_remote_deleted")
        left = [k for k in keys if cleanup.get(k) is not True]
        evidence.append(f"scratch cleanup read back: {dict(cleanup)}")
        legs.append(LegResult(Leg.FAIL, "the scratch integration was not cleaned up: "
                              + ", ".join(left)) if left else LegResult(Leg.PASS, "scratch cleanup"))
    return legs


def compare_landing(local: Mapping, remote: Mapping,
                    integration: Optional[Mapping] = None) -> Verdict:
    evidence = [f"base sha local={local.get('base_sha')} codespace={remote.get('base_sha')}",
                f"tree sha local={local.get('tree_sha')} codespace={remote.get('tree_sha')}"]
    problems = []
    if local.get("base_sha") != remote.get("base_sha"):
        problems.append("the two sides did not start from the same base sha")
    if local.get("tree_sha") != remote.get("tree_sha"):
        problems.append("the trees differ at the compared commits")
    for side, rec in (("local", local), ("codespace", remote)):
        if rec.get("dirty"):
            problems.append(f"the {side} work tree was dirty: the compared commit is not what ran")
    landing = remote.get("landing") or {}
    pushed = landing.get("pushed_branch")
    if pushed:
        evidence.append(f"pushed branch {pushed} on origin at {landing.get('pushed_sha')}; "
                        f"codespace HEAD {remote.get('base_sha')}")
        if landing.get("pushed_sha") != remote.get("base_sha"):
            problems.append("the pushed branch is not the Codespace's HEAD")
    if problems:
        return _verdict(3, "FAIL", "; ".join(problems), evidence)
    push_leg = (LegResult(Leg.PASS, "push") if pushed else
                LegResult(Leg.NOT_RUN, f"push leg not exercised (the Codespace pushed no branch; "
                          f"push exit {landing.get('push_exit')})"))
    status, reason = fold_legs([push_leg, *integration_legs(local, integration, evidence, remote)])
    return _verdict(3, status, reason, evidence)


def compare_transport(local: Mapping, remote: Mapping) -> Verdict:
    t = remote["transport"]
    lt = local.get("transport") or {}
    problems = []
    if not (t.get("rclone") or {}).get("present"):
        problems.append("rclone absent on the Codespace")
    if not t.get("token_present"):
        problems.append("RCLONE_CONFIG_GDRIVE_TOKEN not set on the Codespace")
    if (t.get("rclone") or {}).get("present"):
        if t.get("read_exit") != 0:
            problems.append(f"read exit {t.get('read_exit')}")
        elif not t.get("read_entries"):
            problems.append(f"read returned {t.get('read_entries')} entries")
    evidence = [f"read: {'FAIL' if problems else 'PASS'} (exit {t.get('read_exit')}, "
                f"{t.get('read_entries')} entries; local {lt.get('read_entries')})"]
    write = t.get("write")
    if write is None:
        evidence.append(f"write: NOT-RUN -- {TRANSPORT_WRITE_NOT_RUN_REASON}")
        if problems:
            return _verdict(4, "FAIL", "; ".join(problems), evidence)
        return _verdict(4, "NOT-RUN", TRANSPORT_WRITE_NOT_RUN_REASON, evidence)
    # The write leg ran (`collect --probe-write`): it is judged on its own steps, and a good write
    # never rescues a failed read.
    name = write.get("name")
    wp: list[str] = []
    if not name:
        wp.append("the write probe carries no file name")
    elif write.get("write_exit") != 0:
        wp.append(f"write exit {write.get('write_exit')}")
    else:
        if not write.get("readback_ok"):
            wp.append("the read-back of the probe file did not match what was written")
        if write.get("delete_exit") != 0:
            wp.append(f"delete exit {write.get('delete_exit')}")
    if name and write.get("gone_after") is not True:
        wp.append(f"probe file {name} is still on the transport (or its absence could not be read)")
    evidence.append(
        f"write: {'FAIL' if wp else 'PASS'} ({name}: write exit {write.get('write_exit')}, "
        f"read-back {'identical' if write.get('readback_ok') else 'NOT identical'}, delete exit "
        f"{write.get('delete_exit')}, absent afterwards {write.get('gone_after')})")
    problems.extend(wp)
    if problems:
        return _verdict(4, "FAIL", "; ".join(problems), evidence)
    return _verdict(4, "PASS", "", evidence)


def compare_cleanup(cleanup: Optional[Mapping]) -> Verdict:
    if cleanup is None:
        return _verdict(5, "NOT-RUN",
                        "no cleanup record supplied (run `verify-cleanup` after teardown)")
    problems = []
    evidence = []
    if cleanup.get("listing_exit") != 0 or cleanup.get("ls_remote_exit") != 0:
        problems.append("the cleanup record carries no read evidence (listing_exit and "
                        "ls_remote_exit must both be 0): it was not written by `verify-cleanup`")
    if cleanup.get("codespace_listed_after"):
        problems.append(f"codespace {cleanup.get('codespace')} still listed after teardown")
    if cleanup.get("branch_listed_after"):
        problems.append(f"branch {cleanup.get('branch')} still on origin")
    # the extra branches a run creates (the test lane's own, C3's scratch integration): each one
    # must carry a READ of its absence, and every read must say gone
    after = cleanup.get("extra_branches_listed_after")
    for extra in cleanup.get("extra_branches") or []:
        if not isinstance(after, Mapping) or extra not in after:
            problems.append(f"branch {extra} was named for cleanup but no read of it is recorded")
        elif after[extra] is not False:
            problems.append(f"branch {extra} still on origin")
    try:
        created = datetime.fromisoformat(cleanup["created"]) if cleanup.get("created") else None
        deleted = datetime.fromisoformat(cleanup["deleted"]) if cleanup.get("deleted") else None
        if created is None or deleted is None:
            problems.append("no creation or deletion time recorded: the cost is not measurable")
        else:
            wall = _regime.uptime_minutes(created, deleted)
            hours = core_hours(created, deleted, cleanup.get("machine", ""))
            evidence.append(f"wall time {wall:.1f} min on {cleanup.get('machine')}; "
                            f"core-hours {hours:.2f} ({MACHINE_CORES[cleanup['machine']]} cores)")
            if wall <= 0:
                problems.append("zero recorded uptime")
    except (ValueError, KeyError, TypeError) as exc:
        problems.append(f"cost not computable: {exc}")
    if problems:
        return _verdict(5, "FAIL", "; ".join(problems), evidence)
    extras = list(cleanup.get("extra_branches") or [])
    evidence.append(f"codespace {cleanup.get('codespace')} and branch {cleanup.get('branch')} "
                    + (f"and {len(extras)} more branch(es) ({', '.join(extras)}) " if extras else "")
                    + "all gone")
    return _verdict(5, "PASS", "", evidence)


def compare_all(local: Mapping, remote: Mapping, cleanup: Optional[Mapping] = None,
                registry: Optional[Mapping] = None,
                integration: Optional[Mapping] = None) -> list[Verdict]:
    return [compare_environment(local, remote, registry), compare_gates(local, remote),
            compare_landing(local, remote, integration), compare_transport(local, remote),
            compare_cleanup(cleanup)]


def exit_code(verdicts: Sequence[Verdict]) -> int:
    statuses = {v.status for v in verdicts}
    if "FAIL" in statuses:
        return 1
    if "NOT-RUN" in statuses:
        return 2
    return 0


# ============================================================================ loading, checking

def _validate(text: str, side: str, exc: type) -> dict:
    if not text or not text.strip():
        raise exc("the record is empty")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as err:
        raise exc(f"the record is not JSON ({err.msg} at char {err.pos})") from err
    if not isinstance(data, dict):
        raise exc("the record is not a JSON object")
    if data.get("schema") != SCHEMA:
        raise exc(f"the record's schema is {data.get('schema')!r}, expected {SCHEMA}")
    missing = [k for k in _REQUIRED_KEYS if k not in data]
    if missing:
        raise exc(f"the record lacks {', '.join(missing)}")
    if data.get("side") != side:
        raise exc(f"the record says side={data.get('side')!r}, expected {side!r} -- comparing "
                  "a side with itself would be green by construction")
    return data


def load_local(path: Path) -> dict:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise LocalRecordUnusable(f"cannot read the local record: {exc}") from exc
    return _validate(text, "local", LocalRecordUnusable)


def read_remote_file(path: Path) -> dict:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise RemoteUnavailable(f"cannot read the Codespace record: {exc}") from exc
    return _validate(text, "codespace", RemoteUnavailable)


def read_remote_via_gh(name: str, remote_file: str, run: Runner) -> dict:
    """`gh codespace ssh ... cat`, never `cp` (measured: `cp` exits 0 having written nothing)."""
    res = run(["gh", "codespace", "ssh", "-c", name, "--", "cat", remote_file], timeout=300)
    if res.returncode != 0:
        detail = (res.stdout or res.stderr or "").strip().replace("\n", " ")[:200]
        raise RemoteUnavailable(f"gh codespace ssh exited {res.returncode} reading {remote_file}"
                                f"{': ' + detail if detail else ''}")
    return _validate(res.stdout, "codespace", RemoteUnavailable)


def _unavailable_report(why: str, label: str = "RemoteUnavailable") -> str:
    lines = [f"FAILURE {label}: {why}"]
    for n, name in CONDITION_NAMES.items():
        lines.append(f"NOT-RUN cond={n} {name} remote side unavailable -- nothing was compared")
    return "\n".join(lines)


def render_report(verdicts: Sequence[Verdict]) -> str:
    lines = []
    for v in verdicts:
        lines.append(v.render())
        lines.extend(f"    {e}" for e in v.evidence)
    return "\n".join(lines)


def run_check(local_path: Path, *, remote_path: Optional[Path] = None,
              codespace: Optional[str] = None, remote_file: str = DEFAULT_REMOTE_FILE,
              cleanup_path: Optional[Path] = None, run: Optional[Runner] = None,
              save_remote: Optional[Path] = None,
              integration_path: Optional[Path] = None) -> tuple[int, str]:
    """Compare the two records. Returns (exit code, report text); never raises.

    `integration_path` is the record `integrate` wrote: condition 3's merge, outcome-test and CI
    legs. Without it those legs are NOT-RUN and the check cannot exit 0.

    `save_remote` keeps the record read over gh: the Codespace is deleted at teardown, and a
    verdict whose remote evidence died with it cannot be re-derived (found on the first run)."""
    try:
        local = load_local(local_path)
    except LocalRecordUnusable as exc:
        return 4, _unavailable_report(str(exc), "LocalRecordUnusable")
    try:
        if remote_path is not None and codespace:
            raise RemoteUnavailable("both --remote and --codespace were given: a file would "
                                    "stand in for a Codespace that was never contacted -- give one")
        if remote_path is not None:
            remote = read_remote_file(remote_path)
        elif codespace:
            remote = read_remote_via_gh(codespace, remote_file, run or default_run)
        else:
            raise RemoteUnavailable("no remote record and no Codespace named -- nothing to compare")
    except RemoteUnavailable as exc:
        return 3, _unavailable_report(str(exc))
    if save_remote is not None:
        write_record(save_remote, remote)
    cleanup: Optional[dict] = None
    cleanup_problem = ""
    if cleanup_path is not None:
        try:
            cleanup = json.loads(Path(cleanup_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            cleanup_problem = f"the cleanup record is unreadable ({exc})"
    integration: Optional[dict] = None
    integration_problem = ""
    if integration_path is not None:
        try:
            integration = json.loads(Path(integration_path).read_text(encoding="utf-8"))
            if not isinstance(integration, dict) or integration.get("schema") != SCHEMA:
                integration_problem = "the integration record is not a schema-1 JSON object"
                integration = None
        except (OSError, json.JSONDecodeError) as exc:
            integration_problem = f"the integration record is unreadable ({exc})"
    verdicts = compare_all(local, remote, cleanup, integration=integration)
    if cleanup_problem:
        verdicts[4] = _verdict(5, "FAIL", cleanup_problem)
    if integration_problem:
        verdicts[2] = _verdict(3, "FAIL", integration_problem)
    code = exit_code(verdicts)
    return code, render_report(verdicts) + f"\nexit={code}"


# ============================================================================ verify-cleanup

def verify_cleanup(name: str, branch: str, created: str, deleted: str, machine: str,
                   run: Runner = default_run, *, root: Path = _REPO_ROOT,
                   extra_branches: Optional[Sequence[str]] = None) -> dict:
    """Condition 5's record: read AFTER teardown that the Codespace is not listed and the run
    branch (and every `extra_branches` entry -- the test lane's own, C3's scratch integration) is
    not on origin. A listing that cannot be read raises -- 'could not look' is not 'gone'."""
    listing = run(["gh", "codespace", "list", "--json", "name"], timeout=120)
    if listing.returncode != 0:
        raise RemoteUnavailable(f"gh codespace list exited {listing.returncode}: cannot say "
                                "the Codespace is gone")
    try:
        names = [row.get("name") for row in json.loads(listing.stdout or "[]")]
    except (json.JSONDecodeError, AttributeError) as exc:
        raise RemoteUnavailable(f"gh codespace list returned unreadable output: {exc}") from exc
    heads = run(["git", "ls-remote", "--heads", "origin", branch], cwd=root, timeout=120)
    if heads.returncode != 0:
        raise RemoteUnavailable(f"git ls-remote exited {heads.returncode}: cannot say the "
                                "branch is gone")
    record = {"schema": SCHEMA, "codespace": name, "machine": machine, "created": created,
              "deleted": deleted, "codespace_listed_after": name in names, "branch": branch,
              "branch_listed_after": _exact_head(heads.stdout, branch) is not None,
              "listing_exit": listing.returncode, "ls_remote_exit": heads.returncode}
    if extra_branches:
        after: dict[str, bool] = {}
        for extra in extra_branches:
            more = run(["git", "ls-remote", "--heads", "origin", extra], cwd=root, timeout=120)
            if more.returncode != 0:
                raise RemoteUnavailable(f"git ls-remote exited {more.returncode} for {extra}: "
                                        "cannot say the branch is gone")
            after[extra] = _exact_head(more.stdout, extra) is not None
        record["extra_branches"] = list(extra_branches)
        record["extra_branches_listed_after"] = after
    return record


# ============================================================================================ CLI

@click.group()
def cli() -> None:
    """The five-condition Codespace parity check ([#1335])."""


@cli.command("collect")
@click.option("--out", "out", required=True, type=click.Path(path_type=Path))
@click.option("--side", default="", help="local | codespace; default: from $CODESPACES.")
@click.option("--push-branch", default=None, help="Codespace side: push HEAD to this branch.")
@click.option("--via-gate", is_flag=True, help="Run the pytest leg through memory_admission_gate.")
@click.option("--skip-gates", is_flag=True, help="Debug only: an empty gates leg, which `check` refuses.")
@click.option("--probe-write", "probe_write", default=None,
              help="Condition 4's write leg: write, read back and delete this ONE file name on "
                   "the transport (a root-level name or one file directly in to-browser/; a "
                   "contract must name it). Default: not exercised.")
def collect_cmd(out: Path, side: str, push_branch: Optional[str], via_gate: bool,
                skip_gates: bool, probe_write: Optional[str]) -> None:
    """Build this environment's record (conditions 1-4's evidence) and write it to --out."""
    try:
        record = collect_record(side=side, push_branch=push_branch, via_gate=via_gate,
                                skip_gates=skip_gates, probe_write=probe_write)
    except ValueError as exc:
        raise click.UsageError(str(exc)) from exc
    write_record(out, record)
    click.echo(f"record written: side={record['side']} base={record['base_sha'][:12]} -> {out}")


@cli.command("check")
@click.option("--local", "local_path", required=True, type=click.Path(path_type=Path))
@click.option("--remote", "remote_path", default=None, type=click.Path(path_type=Path))
@click.option("--codespace", default=None, help="Read the remote record over gh codespace ssh.")
@click.option("--remote-file", default=DEFAULT_REMOTE_FILE, show_default=True)
@click.option("--cleanup", "cleanup_path", default=None, type=click.Path(path_type=Path))
@click.option("--save-remote", "save_remote", default=None, type=click.Path(path_type=Path),
              help="Keep the record read over gh, so the evidence outlives the Codespace.")
@click.option("--integration", "integration_path", default=None, type=click.Path(path_type=Path),
              help="The record `integrate` wrote: condition 3's merge / outcome-test / CI legs.")
def check_cmd(local_path: Path, remote_path: Optional[Path], codespace: Optional[str],
              remote_file: str, cleanup_path: Optional[Path], save_remote: Optional[Path],
              integration_path: Optional[Path]) -> None:
    """One verdict per condition; exit 0 all PASS | 1 FAIL | 2 NOT-RUN | 3 remote unavailable."""
    code, text = run_check(local_path, remote_path=remote_path, codespace=codespace,
                           remote_file=remote_file, cleanup_path=cleanup_path,
                           save_remote=save_remote, integration_path=integration_path)
    click.echo(text)
    sys.exit(code)


@cli.command("integrate")
@click.option("--run-branch", required=True, help="The test lane's pushed branch (worktree-<slug>).")
@click.option("--scratch-branch", required=True, help="worktree-integrate-<slug>; never main.")
@click.option("--base", required=True, help="Full 40-hex sha the run branch was cut from.")
@click.option("--onto", default=None,
              help="Full sha the scratch branch is cut from; default: origin/main's tip "
                   "after a fetch. Not --base itself: CI judges the push as if it landed on main "
                   "now, so sync the lane to main before it is frozen.")
@click.option("--ci-base", "ci_base", default=None,
              help="Full sha whose CI run the merge's run is judged against; default: origin/main's "
                   "tip now (CI runs the scratch branch against the current main ref).")
@click.option("--workdir", required=True, type=click.Path(path_type=Path),
              help="Where the scratch worktree is created (and removed).")
@click.option("--test", "outcome_test", required=True,
              help="The outcome test as a JSON argv list, run on the merged tree.")
@click.option("--ci-timeout", "ci_timeout_s", default=3600, show_default=True, type=int)
@click.option("--ci-reruns", "ci_reruns", default=1, show_default=True, type=click.IntRange(0, 2),
              help="Re-runs of the FAILED jobs when the only reds are named tests (a flake "
                   "candidate); both verdicts are kept in the record. 0 never re-runs.")
@click.option("--out", "out", required=True, type=click.Path(path_type=Path))
def integrate_cmd(run_branch: str, scratch_branch: str, base: str, onto: Optional[str],
                  ci_base: Optional[str], workdir: Path, outcome_test: str, ci_timeout_s: int,
                  ci_reruns: int, out: Path) -> None:
    """Condition 3's integration legs: merge the run branch on a scratch branch, test, read CI."""
    try:
        argv = json.loads(outcome_test)
        if not (isinstance(argv, list) and argv and all(isinstance(a, str) for a in argv)):
            raise ValueError("--test must be a non-empty JSON list of strings")
        if onto is None:
            onto = default_onto(default_run, root=_REPO_ROOT, base=base)
        if ci_base is None:
            listed = default_run(["git", "ls-remote", "--heads", "origin", "main"], cwd=_REPO_ROOT,
                                 timeout=120)
            ci_base = _exact_head(listed.stdout, "main") if listed.returncode == 0 else None
            if not ci_base:
                raise ValueError("could not read origin/main for the CI baseline: pass --ci-base")
        record = collect_integration(default_run, root=_REPO_ROOT, run_branch=run_branch,
                                     scratch_branch=scratch_branch, base=base, onto=onto,
                                     ci_base=ci_base, outcome_test=argv, workdir=workdir,
                                     ci_timeout_s=ci_timeout_s, ci_reruns=ci_reruns)
    except (ValueError, json.JSONDecodeError) as exc:
        raise click.UsageError(str(exc)) from exc
    write_record(out, record)
    click.echo(f"integration record written: merge={record.get('merge')} "
               f"ci={(record.get('ci') or {}).get('state')} -> {out}")


@cli.command("stamp-lane")
@click.option("--record", "record_path", required=True, type=click.Path(path_type=Path),
              help="The Codespace's record (`collect --side codespace --out`), stamped in place.")
@click.option("--branch", required=True, help="The test lane's branch (`worktree-<slug>`).")
def stamp_lane_cmd(record_path: Path, branch: str) -> None:
    """Bind the Codespace record to the lane it worked: its branch and that branch's tip."""
    try:
        lane = stamp_lane(default_run, root=_REPO_ROOT, record_path=record_path, branch=branch)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise click.UsageError(str(exc)) from exc
    click.echo(f"lane stamped: {lane['branch']} at {lane['sha'][:12]} -> {record_path}")


@cli.command("verify-cleanup")
@click.option("--codespace", "name", required=True)
@click.option("--branch", required=True)
@click.option("--created", required=True, help="ISO-8601 creation time.")
@click.option("--deleted", required=True, help="ISO-8601 deletion time.")
@click.option("--machine", required=True)
@click.option("--also-branch", "also_branches", multiple=True,
              help="Another branch that must be gone from origin (repeatable): the integration "
                   "scratch branch.")
@click.option("--out", "out", required=True, type=click.Path(path_type=Path))
def verify_cleanup_cmd(name: str, branch: str, created: str, deleted: str, machine: str,
                       also_branches: tuple[str, ...], out: Path) -> None:
    """After teardown: read that the Codespace and the run branch are gone; write the record."""
    try:
        record = verify_cleanup(name, branch, created, deleted, machine,
                                extra_branches=list(also_branches) or None)
    except RemoteUnavailable as exc:
        click.echo(f"FAILURE RemoteUnavailable: {exc}")
        sys.exit(3)
    write_record(out, record)
    click.echo(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    cli()
