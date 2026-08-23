#!/usr/bin/env python
"""generated_artifact_freshness.py -- the committed-generated staleness leg (ADR-86, amended
2026-08-23; `[#171]` leg 1 / f7).

WHAT THIS ANSWERS. *Is a committed generated artifact older than the inputs it was generated
from?* ADR-86's 2026-08-23 amendment rules that a **human or integrator** commit satisfies
"committed" -- the generator has no writer of its own. That makes the header honest; it does
nothing to keep the output current. An honest header on a stale trust surface is still a stale
trust surface, so this module is the second half of that ruling.

WHAT IT DELIBERATELY DOES NOT ANSWER, because the two questions are different defects and the
Phase-0 packet is explicit that they must not be blurred:
  * *Does the committed copy byte-match a regeneration?* -- that is `gen_dashboard.py --check`,
    which is armed nowhere (R3 **F5**, a GATING gap). `--check` is HEAD-pinned: the dashboard
    renders HEAD's sha and commit date, so `--check` drifts on EVERY commit and a gate keyed on
    it would fire constantly. This leg keys on the artifact's **content inputs** instead, which
    is why it can carry a meaningful baseline at all.
  * *Who committed it?* -- ADR-86 as amended: whoever ran the generator. Not this leg's subject.

SHAPE -- probe **P5**, not a second idiom. P5 asks whether `ARCHITECTURE.md`'s `last_reviewed`
stamp is on-or-after that file's last git touch: a relation between two git dates. Same relation
here, different subject -- the artifact's own last-commit date against the newest last-commit date
across its declared inputs. `scripts/canonical_freshness_gate.py` is the same relation wearing an
audit leg, and this module copies its `(fails, warns)` return shape so the two cannot drift apart.

WARN, NEVER FAIL -- and `fails` is empty BY CONSTRUCTION, not by accident. The signature returns
`(fails, warns)` so it matches its sibling exactly, and `fails` is always `[]`. Promoting this leg
to FAIL is a later act that needs its own ruling; when that ruling lands it is a one-line change
here, with the ruling cited on the line. A leg that quietly turned RED on a wall-clock threshold
nobody ratified is the failure mode this note exists to prevent.

THE BASELINE IS MEASURED, NOT CHOSEN. `baseline_days` is what the artifact's staleness actually
WAS when the leg was written (dashboard: **3 days**, measured at `aeec0fd1` on 2026-08-23 --
artifact committed 2026-08-20, newest input commit 2026-08-23). The leg therefore starts quiet and
fires only when staleness gets WORSE than the state that motivated it. It is a ratchet, not an
allowance: the honest reading of "3" is *this repo tolerated three days of drift once*, not *three
days of drift is fine*.

THE INPUT SET IS DECLARED, NOT INFERRED -- and it is a LITERAL here on purpose. `gen_dashboard`
loads three sibling generators at module scope (`_gtt`/`_gii`/`_gcr`, `:150-152`), so importing it
to read its constants would drag four modules into every audit run. It is also the module this leg
reports on, and `gen_dashboard`'s own stated principle is that a reporter must not call what it
reports on ("this generator must not call the gate it reports on"; "telemetry is read as a FILE,
never as an import"). The symmetric rule applies: the gate does not import the generator. Drift
between the literal and the generator's own `INPUT_RELPATHS` is caught by
`tests/test_generated_artifact_freshness.py::test_input_set_agrees_with_generator`, which CAN
afford the import -- the same fallback-literal-plus-agreement-test pattern
`canonical_freshness_gate.py` uses for `canonical_docs`.

Read-only (Layer-2, ADR-28/36): spawns `git log` and nothing else, writes nothing, arms no hook.
Degrades to `unmeasurable` without git rather than inventing a verdict.

CLI: `python scripts/generated_artifact_freshness.py` prints one line per registered artifact and
**always exits 0** -- it is a measurement, and this leg is not a commit gate by ruling.
"""
from __future__ import annotations

import importlib.util
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

# `gitenv` is loaded BY PATH, never by name: `import gitenv` and `from scripts import gitenv`
# each have a shadow hole (terra HIGH x3, 2026-08-08 -- see that module's docstring), and both
# holes end with the scrub silently becoming the EMPTY set. `spec_from_file_location` against a
# sibling path is the spelling no `sys.path` entry can intercept.
def _load_sibling(name: str):
    path = Path(__file__).resolve().with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(f"_gaf_{name}", path)
    if spec is None or spec.loader is None:  # pragma: no cover -- defensive
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_gitenv = _load_sibling("gitenv")


@dataclass(frozen=True)
class GeneratedArtifact:
    """One committed-generated artifact and the tracked inputs it is generated from."""

    name: str
    #: Every committed output face. The pair is only as fresh as its STALEST face.
    outputs: tuple[str, ...]
    #: Tracked git pathspecs the generator reads. Directories are fine (`git log -- tasks`).
    inputs: tuple[str, ...]
    #: The measured staleness at the moment this leg was armed. See the module docstring.
    baseline_days: int
    #: What the operator runs to discharge a WARN.
    regen_command: str
    #: Read by the generator but NOT git-trackable -- recorded so the carve-out is visible
    #: rather than a silent omission from `inputs`.
    untracked_inputs: tuple[str, ...] = ()


#: `[#171]` stage 1, ADR-86. `inputs` mirrors `gen_dashboard.INPUT_RELPATHS`; see the module
#: docstring for why it is a literal, and the agreement test that keeps it honest.
#: `docs/intake/archive` is inside `docs/intake` and needs no separate entry.
DASHBOARD = GeneratedArtifact(
    name="conformance-dashboard",
    outputs=("ecosystem/conformance.md", "ecosystem/conformance.html"),
    inputs=("BACKLOG.md", "tasks", "docs/intake", "docs/decisions", "docs/audits"),
    baseline_days=3,
    regen_command="python scripts/gen_dashboard.py --write",
    # Gitignored (`.gitignore:95`) and absent as of 2026-08-23; the generator existence-probes it
    # and reads its size. It has no git history, so it cannot carry a commit date and cannot
    # participate in a git-date relation. Stated, not silently dropped.
    untracked_inputs=("logs/TELEMETRY.db",),
)

REGISTRY: tuple[GeneratedArtifact, ...] = (DASHBOARD,)


def git_last_commit_date(repo_path: Path, pathspec: str) -> Optional[date]:
    """Author date (short ISO) of the newest commit touching `pathspec`, or None.

    Author date (`%as`), not committer date -- the same choice
    `canonical_freshness_gate.git_last_commit_date` makes and for the same reason: author date
    survives rebase / cherry-pick / amend, so the relation keys off when content was actually
    edited rather than when history was rewritten.

    The repo-location env vars are SCRUBBED via `gitenv`: an inherited `GIT_DIR` overrides both
    `cwd=` and `git -C`, which is how a validator comes to read the parent repo while labelling
    the answer with the target's id ([#355]). Returns None when git is absent, the path is not a
    repo, or the pathspec has no history -- callers then report `unmeasurable`.

    IF `gitenv` COULD NOT BE LOADED, THIS REFUSES TO ANSWER rather than answering unscrubbed.
    Falling back to `env=None` would inherit any ambient `GIT_DIR` and read a DIFFERENT repo
    while labelling the answer with this one's paths -- a wrong verdict, silently, which is
    strictly worse than no verdict. `gitenv` is a leaf sibling file in this very directory, so
    this branch means the tree is broken, and `unmeasurable` is the honest report.
    """
    if _gitenv is None:  # pragma: no cover -- only reachable with a broken scripts/ tree
        return None
    env = _gitenv.scrubbed_git_env()
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "log", "-1", "--format=%as", "--", pathspec],
            capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
        )
    except OSError:
        return None
    out = result.stdout.strip()
    if result.returncode != 0 or not out:
        return None
    try:
        return date.fromisoformat(out)
    except ValueError:
        return None


@dataclass(frozen=True)
class Measurement:
    """The P5-shaped relation for one artifact, plus the evidence that produced it."""

    artifact: str
    verdict: str                      # "fresh" | "stale" | "unmeasurable"
    #: Only meaningful when `verdict == "unmeasurable"`. True when an output FILE is absent from
    #: disk (a consumer repo that simply has no dashboard -> the audit leg renders `n/a`
    #: SUBJECT-ABSENT); False when the file is there but git could not answer (-> `unavailable`).
    #: The two are different facts and collapsing them is exactly the "skip rendered as pass"
    #: class `_na_reason` exists to prevent.
    subject_absent: bool
    staleness_days: Optional[int]
    baseline_days: int
    output_date: Optional[date]
    stalest_output: Optional[str]
    input_date: Optional[date]
    newest_input: Optional[str]
    detail: str


def measure(repo_path: Path, artifact: GeneratedArtifact = DASHBOARD, *,
            git_date_fn=git_last_commit_date) -> Measurement:
    """Compare the artifact's own commit date against the newest of its inputs'.

    `output_date` is the **minimum** across the output faces: two faces are written by one run
    and normally share a commit, but if one ever lags, the pair is as fresh as its stalest half.
    `input_date` is the **maximum** across the inputs: any one input moving forward is what makes
    the artifact out of date.

    An output with no git history means the artifact is not committed at all -- a different
    defect, and one `gen_dashboard.py --check` already reports as MISSING -- so this returns
    `unmeasurable` rather than inventing a staleness number for a file that was never there.
    """
    def _unmeasurable(detail: str, *, subject_absent: bool = False) -> Measurement:
        return Measurement(artifact.name, "unmeasurable", subject_absent, None,
                           artifact.baseline_days, None, None, None, None, detail)

    out_dates: list[tuple[str, date]] = []
    for rel in artifact.outputs:
        d = git_date_fn(repo_path, rel)
        if d is None:
            # Disk presence is consulted ONLY to explain a failure to measure, never to produce
            # one: a consumer repo with no dashboard at all is SUBJECT-ABSENT (`n/a`), while a
            # file that exists but whose history git could not read is `unavailable`.
            absent = not (Path(repo_path) / rel).is_file()
            return _unmeasurable(
                f"output {rel} is not present in this repo" if absent
                else f"no git history for output {rel}", subject_absent=absent)
        out_dates.append((rel, d))
    if not out_dates:
        return _unmeasurable("artifact declares no outputs")

    in_dates = [(rel, d) for rel in artifact.inputs
                if (d := git_date_fn(repo_path, rel)) is not None]
    if not in_dates:
        return _unmeasurable("no git history for any declared input "
                             f"({', '.join(artifact.inputs)})")

    stalest_output, output_date = min(out_dates, key=lambda pair: pair[1])
    newest_input, input_date = max(in_dates, key=lambda pair: pair[1])
    staleness = max(0, (input_date - output_date).days)
    verdict = "stale" if staleness > artifact.baseline_days else "fresh"
    detail = (f"{artifact.name}: {staleness}d stale (baseline {artifact.baseline_days}d) — "
              f"{stalest_output} committed {output_date.isoformat()}, newest input "
              f"{newest_input} committed {input_date.isoformat()}")
    return Measurement(artifact.name, verdict, False, staleness, artifact.baseline_days,
                       output_date, stalest_output, input_date, newest_input, detail)


def evaluate(repo_path: Path, artifacts: Optional[tuple[GeneratedArtifact, ...]] = None, *,
             git_date_fn=git_last_commit_date) -> tuple[list[str], list[str]]:
    """Pure evaluation -> `(fails, warns)`, matching `canonical_freshness_gate.evaluate`.

    **`fails` is `[]` unconditionally, by construction.** ADR-86's 2026-08-23 amendment arms this
    leg at WARN against a measured baseline; RED is a later act with its own ruling. The empty
    list is returned rather than the signature being narrowed so that (a) the two freshness
    modules keep one shape and (b) the promotion, when ruled, is one line.

    An `unmeasurable` artifact contributes nothing to either list -- absence of evidence is not
    a finding here; the audit leg renders it as `unavailable`.
    """
    warns: list[str] = []
    for artifact in (REGISTRY if artifacts is None else artifacts):
        m = measure(repo_path, artifact, git_date_fn=git_date_fn)
        if m.verdict == "stale":
            warns.append(f"{m.detail}; regenerate + commit: {artifact.regen_command}")
    return [], warns


def measure_all(repo_path: Path, *, git_date_fn=git_last_commit_date) -> list[Measurement]:
    """Every registered artifact's measurement, WARN or not -- what the CLI prints."""
    return [measure(repo_path, a, git_date_fn=git_date_fn) for a in REGISTRY]


def _resolve_repo_root() -> Path:
    """git-toplevel-first, cwd as the fallback -- the sibling gate's resolution order.

    Unlike `git_last_commit_date` this MAY fall back unscrubbed: `--show-toplevel` is being used
    to FIND a repo, not to answer a question about a named one, and cwd is the backstop either
    way. The asymmetry is deliberate and is why it is written down.
    """
    env = _gitenv.scrubbed_git_env() if _gitenv is not None else None
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", env=env)
        if r.returncode == 0 and r.stdout.strip():
            return Path(r.stdout.strip())
    except OSError:
        pass
    return Path.cwd()


def main() -> int:
    """Print one line per registered artifact. ALWAYS exits 0 -- WARN-only by ruling."""
    root = _resolve_repo_root()
    for m in measure_all(root):
        print(f"generated_artifact_freshness: {m.verdict.upper()} {m.detail}")
    return 0


if __name__ == "__main__":  # pragma: no cover -- exercised via subprocess in tests
    raise SystemExit(main())
