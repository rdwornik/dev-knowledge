"""LANE-5B5-2 (B1): `moment:seat-release` -- a single refusing transaction over a released
handoff bundle (PROPOSAL-ADR-HANDOFF-SYSTEM-2026-09-26.md Part 2 rule 1). It refuses to
publish unless the outgoing notes (SUPPLEMENT.md), the generated bundle (HANDOFF_BOOT.md), the
cut manifest (HANDOFF_RECEIPT.json's `manifest.files`, self-hash-verified against the bundle's
own files via `verify_handoff_probes._rule_bd_manifest`, reused not copied) and the transport
copy (sha-equal published files, via `gen_handoff.verify_published`) all exist -- naming
whichever is missing. Scoped to an architect-mode bundle (DECIDED-BY-LANE): that is the mode
that writes SUPPLEMENT.md, the outgoing seat's fixed-slot notes.

RED-FIRST (ADR-108 SS B). On origin/main (sha 9ec8aaf13682a0192d7642559af41a4f7e42a616, before
this lane), `moment:seat-release` did not exist -- `uv run --locked doit -f scripts/dodo.py
moment:seat-release` exited 3:
    ERROR: Invalid parameter: "moment:seat-release". Must be a command, task, or a target.
    Type "doit.exe help" to see available commands.
    Type "doit.exe list" to see available tasks.
`test_moment_is_not_declared_on_a_harness_without_it` below reproduces that shape structurally
(a synthetic harness with no `seat-release` moment) so the RED witness stays runnable, not just
a one-off transcript. Green on this lane's tip: every test below runs the REAL
`ecosystem/harness.yaml` this lane wrote.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_DODO = _REPO / "scripts" / "dodo.py"
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import gen_handoff as gh  # noqa: E402
import graph_queries as gq  # noqa: E402

_RECEIPT_NAMES = {"MOMENT-SEAT-RELEASE-NOTES.json", "MOMENT-SEAT-RELEASE-BUNDLE.json",
                  "MOMENT-SEAT-RELEASE-MANIFEST.json", "MOMENT-SEAT-RELEASE-COPY.json"}


def _env(tmp: Path, bundle: Path, copy: "Path | None") -> dict[str, str]:
    env = {**os.environ, "HARNESS_RECEIPTS_DIR": str(tmp / "receipts"),
           "HARNESS_SEAT_RELEASE_BUNDLE": str(bundle),
           "DEV_KNOWLEDGE_TELEMETRY_DB": str(tmp / "telemetry.db")}
    env.pop("HARNESS_YAML", None)
    if copy is not None:
        env["HARNESS_SEAT_RELEASE_COPY"] = str(copy)
    else:
        env.pop("HARNESS_SEAT_RELEASE_COPY", None)
    return env


def _doit(tmp: Path, *targets: str, env: dict[str, str],
         timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "doit", "-f", str(_DODO), "--dir", str(tmp),
         "--db-file", str(tmp / ".doit.db"), *targets],
        capture_output=True, text=True, env=env, cwd=tmp, timeout=timeout)


# --- RED-FIRST, reproduced structurally (ADR-108 SS B) -------------------------------------

def test_moment_is_not_declared_on_a_harness_without_it(tmp_path):
    """The shape of origin/main before this lane: no `seat-release` moment, so the doit
    target does not exist. Real-repo evidence (sha 9ec8aaf1...) is this file's own docstring."""
    harness = tmp_path / "harness.yaml"
    harness.write_text(yaml.safe_dump({"stages": [], "moments": [], "fates": []}),
                       encoding="utf-8")
    env = {**os.environ, "HARNESS_YAML": str(harness),
           "HARNESS_RECEIPTS_DIR": str(tmp_path / "receipts")}
    env.pop("HARNESS_SEAT_RELEASE_BUNDLE", None)
    result = _doit(tmp_path, "moment:seat-release", env=env)
    assert result.returncode == 3, result.stdout + result.stderr
    assert "Invalid parameter" in result.stdout + result.stderr


# --- the real declaration: one dry-cut bundle, reused (read-only) by every test below -------

@pytest.fixture(scope="module")
def dry_bundle(tmp_path_factory) -> Path:
    """One real architect-mode dry cut (`gen_handoff.generate(..., dry_cut=True)`), generated
    ONCE -- it walks live repo state and costs real wall-clock. Every test that needs to
    mutate a bundle works on its own copy (`_fresh_bundle`) so this fixture instance is never
    written to."""
    root = tmp_path_factory.mktemp("seat-release-dry-cut")
    res = gh.generate(_REPO, mode="architect", dry_cut=True, bundle_root=root,
                      assemble=True, boot_turns=1, boot_dispatch="test")
    return res.bundle_dir


def _fresh_bundle(dry_bundle: Path, tmp_path: Path) -> Path:
    dest = tmp_path / "bundle"
    shutil.copytree(dry_bundle, dest)
    return dest


def _published_copy(bundle: Path, tmp_path: Path) -> Path:
    dest = tmp_path / "transport-copy"
    gh.publish_bundle(bundle, dest)
    return dest


# --- Done-when 1: the whole transaction, one receipt per organ ------------------------------

def test_moment_writes_one_receipt_per_organ_on_a_complete_release(dry_bundle, tmp_path):
    bundle = _fresh_bundle(dry_bundle, tmp_path)
    copy = _published_copy(bundle, tmp_path)
    result = _doit(tmp_path, "moment:seat-release", env=_env(tmp_path, bundle, copy))
    assert result.returncode == 0, result.stdout + result.stderr
    receipts = sorted((tmp_path / "receipts").glob("MOMENT-SEAT-RELEASE-*.json"))
    assert {p.name for p in receipts} == _RECEIPT_NAMES, sorted(p.name for p in receipts)
    for p in receipts:
        data = json.loads(p.read_text(encoding="utf-8"))
        assert data["status"] == "ok" and data["exit_code"] == 0, (p.name, data)


# --- Done-when 2: one test per missing artifact, refused and NAMED --------------------------

def test_refuses_and_names_notes_when_supplement_is_absent(dry_bundle, tmp_path):
    bundle = _fresh_bundle(dry_bundle, tmp_path)
    copy = _published_copy(bundle, tmp_path)
    (bundle / "SUPPLEMENT.md").unlink()
    result = _doit(tmp_path, "moment:seat-release", env=_env(tmp_path, bundle, copy))
    assert result.returncode != 0
    assert "missing artifact: notes" in result.stdout + result.stderr
    # the chain STOPS at the first organ -- the rest never ran
    assert not (tmp_path / "receipts" / "MOMENT-SEAT-RELEASE-BUNDLE.json").exists()


def test_refuses_and_names_bundle_when_the_boot_file_is_absent(dry_bundle, tmp_path):
    bundle = _fresh_bundle(dry_bundle, tmp_path)
    copy = _published_copy(bundle, tmp_path)
    (bundle / "HANDOFF_BOOT.md").unlink()
    result = _doit(tmp_path, "moment:seat-release", env=_env(tmp_path, bundle, copy))
    assert result.returncode != 0
    assert "missing artifact: bundle" in result.stdout + result.stderr
    assert not (tmp_path / "receipts" / "MOMENT-SEAT-RELEASE-MANIFEST.json").exists()


def test_refuses_and_names_manifest_when_the_receipt_carries_none(dry_bundle, tmp_path):
    bundle = _fresh_bundle(dry_bundle, tmp_path)
    copy = _published_copy(bundle, tmp_path)
    receipt_path = bundle / "HANDOFF_RECEIPT.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["manifest"] = None
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    result = _doit(tmp_path, "moment:seat-release", env=_env(tmp_path, bundle, copy))
    assert result.returncode != 0
    assert "missing artifact: manifest" in result.stdout + result.stderr
    # the chain STOPS before copy, which would otherwise ALSO fail on the same missing manifest
    assert not (tmp_path / "receipts" / "MOMENT-SEAT-RELEASE-COPY.json").exists()


def test_refuses_and_names_copy_when_the_transport_copy_is_absent(dry_bundle, tmp_path):
    bundle = _fresh_bundle(dry_bundle, tmp_path)
    result = _doit(tmp_path, "moment:seat-release",
                   env=_env(tmp_path, bundle, tmp_path / "no-such-copy"))
    assert result.returncode != 0
    assert "missing artifact: copy" in result.stdout + result.stderr
    # notes/bundle/manifest all held -- only copy is missing
    for stem in ("NOTES", "BUNDLE", "MANIFEST"):
        data = json.loads((tmp_path / "receipts" / f"MOMENT-SEAT-RELEASE-{stem}.json")
                          .read_text(encoding="utf-8"))
        assert data["status"] == "ok" and data["exit_code"] == 0, (stem, data)


def test_refuses_and_names_copy_when_a_published_file_is_tampered(dry_bundle, tmp_path):
    """The `copy` organ is a SHA check, not a mere existence check -- a copy that exists but no
    longer matches the bundle's manifest is refused the same way an absent copy is."""
    bundle = _fresh_bundle(dry_bundle, tmp_path)
    copy = _published_copy(bundle, tmp_path)
    (copy / "HANDOFF_BOOT.md").write_text("tampered", encoding="utf-8")
    result = _doit(tmp_path, "moment:seat-release", env=_env(tmp_path, bundle, copy))
    assert result.returncode != 0
    assert "missing artifact: copy" in result.stdout + result.stderr
    assert "HANDOFF_BOOT.md" in result.stdout + result.stderr


# --- Done-when 3: the two B1 fates are retired, and the census now calls their doc files -----

def test_the_two_b1_fates_are_retired():
    doc = yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))
    fated = {f["path"] for f in doc["fates"]}
    assert ".claude/commands/handoff.md" not in fated, fated
    assert ".claude/commands/handoff-verify.md" not in fated, fated


def test_the_retired_fates_are_now_declared_at_the_seat_release_moment():
    """Backs the fates removal above: `graph_queries.organ_moments` classifies a roster path as
    MOMENT_DECLARED only when some organ's command NAMES it (`_COMMAND_PATH_RE`) -- prove the
    two retired command docs are named by the organs whose checks they document, without
    needing the full persisted graph store (`load_declaration` is a pure YAML read)."""
    declared = gq.load_declaration(_REPO)
    by_organ = {d.organ: d for d in declared if d.moment == "seat-release"}
    assert set(by_organ) == {"seat_release.notes", "seat_release.bundle",
                             "seat_release.manifest", "seat_release.copy"}
    assert ".claude/commands/handoff.md" in by_organ["seat_release.notes"].paths
    assert ".claude/commands/handoff.md" in by_organ["seat_release.bundle"].paths
    assert ".claude/commands/handoff-verify.md" in by_organ["seat_release.manifest"].paths
    assert ".claude/commands/handoff-verify.md" in by_organ["seat_release.copy"].paths


# --- Done-when 4: the CI leg (conductor.yml's `handoff-manifest` job) reds a tampered bundle ---

_WORKFLOW = _REPO / ".github" / "workflows" / "conductor.yml"


def _resolve_real_bash() -> "str | None":
    """The Git-for-Windows bash `shell: bash` resolves to -- never the System32 WSL launcher
    stub (same concern test_conductor_governance_jobs.py names for the other jobs' steps)."""
    found = shutil.which("bash")
    system_root = Path(os.environ.get("SystemRoot", r"C:\Windows"))
    try:
        if found and Path(found).resolve().parent.samefile(system_root / "System32"):
            found = None
    except OSError:
        pass
    if found:
        return found
    program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
    for candidate in (Path(program_files) / "Git" / "bin" / "bash.exe",
                      Path(program_files) / "Git" / "usr" / "bin" / "bash.exe"):
        if candidate.is_file():
            return str(candidate)
    return None


_REAL_BASH = _resolve_real_bash()
requires_bash = pytest.mark.skipif(_REAL_BASH is None, reason="no usable bash found")


def _handoff_manifest_run_step(name_substr: str) -> str:
    """The literal `run:` text of one step of conductor.yml's `handoff-manifest` job -- read
    from the file, never restated, so this test cannot drift from what CI actually runs."""
    doc = yaml.safe_load(_WORKFLOW.read_text(encoding="utf-8"))
    job = doc["jobs"]["handoff-manifest"]
    step = next(s for s in job["steps"] if name_substr in s.get("name", ""))
    return step["run"]


def _run_ci_manifest_step(cwd: Path) -> subprocess.CompletedProcess:
    """Runs the job's own BD-manifest step (unmodified) with PYTHONPATH pointed at this repo's
    `scripts/` -- the step's `sys.path.insert(0, 'scripts')` is then a harmless no-op (`cwd`
    carries no `scripts/` of its own) and `import verify_handoff_probes` resolves via
    PYTHONPATH instead, exactly as the real job resolves it by being IN the repo checkout."""
    script = _handoff_manifest_run_step("BD-manifest over every committed")
    env = {**os.environ, "PYTHONPATH": str(_SCRIPTS)}
    return subprocess.run([_REAL_BASH, "-c", script], capture_output=True, text=True,
                          cwd=cwd, env=env, timeout=120)


def _scratch_manifest_bundle(dry_bundle: Path, tmp_path: Path) -> Path:
    """`<tmp_path>/docs/handoffs/<slug>` -- the CI step's own hardcoded `Path('docs/handoffs')`,
    seeded with one real, manifest-carrying bundle (copied from the module-scoped dry cut)."""
    dest = tmp_path / "docs" / "handoffs" / dry_bundle.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(dry_bundle, dest)
    return dest


@requires_bash
def test_ci_manifest_step_passes_on_a_clean_manifest_era_bundle(dry_bundle, tmp_path):
    _scratch_manifest_bundle(dry_bundle, tmp_path)
    result = _run_ci_manifest_step(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "checked 1 manifest-era bundle" in result.stdout


@requires_bash
def test_ci_manifest_step_reds_and_names_a_tampered_bundle_file(dry_bundle, tmp_path):
    bundle = _scratch_manifest_bundle(dry_bundle, tmp_path)
    (bundle / "HANDOFF_BOOT.md").write_text("tampered", encoding="utf-8")
    result = _run_ci_manifest_step(tmp_path)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "HANDOFF_BOOT.md" in result.stdout
    assert bundle.name in result.stdout


@requires_bash
def test_ci_manifest_step_skips_pre_manifest_era_bundles(dry_bundle, tmp_path):
    """A bundle with no manifest at all (126 of the 127 committed today) is EXEMPT, not failed
    -- the step must not even count it, so a historical bundle can never red this job."""
    dest = tmp_path / "docs" / "handoffs" / "2026-05-09-pre-manifest-era"
    dest.mkdir(parents=True)
    (dest / "HANDOFF_BOOT.md").write_text("no receipt here at all", encoding="utf-8")
    result = _run_ci_manifest_step(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "checked 0 manifest-era bundle" in result.stdout
