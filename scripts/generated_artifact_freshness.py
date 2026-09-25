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
WAS when the leg was written (dashboard: **4 days**, measured at `aeec0fd1` WITH THIS
MODULE'S OWN RELATION -- artifact committed 2026-08-20, newest input `docs/audits` committed
2026-08-24). The leg therefore starts quiet and fires only when staleness gets WORSE than the state
that motivated it. It is a ratchet, not an allowance: the honest reading of "4" is *this repo
tolerated four days of drift once*, not *four days of drift is fine*.

The number was **3** until 2026-08-24 and that was a real defect, not a typo: it had been measured
with the module's FIRST relation (author date, no `--first-parent`), and when that relation was
replaced (committer date on both sides, first-parent spine) nobody re-derived the constant it had
produced. `docs/audits` reads 2026-08-23 by author date and 2026-08-24 by committer date, so the
baseline moved 3 -> 4 under a measurement it no longer described. Found by terra, round 8. A
"measured baseline" that was measured by a relation the code no longer uses is exactly the
false-claim-about-a-mechanism defect this whole lane exists to fix, so it is corrected here rather
than rounded away.

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

Read-only (Layer-2, ADR-28/36): spawns only read-only git commands -- `git log` here, plus the
`git rev-parse` that `gitenv` and the CLI's root resolution each run -- writes nothing, and arms
no hook. Degrades to `unmeasurable` without git rather than inventing a verdict.

CLI: `python scripts/generated_artifact_freshness.py` prints one line per registered artifact and
**always exits 0** -- it is a measurement, and this leg is not a commit gate by ruling.
"""
from __future__ import annotations

import importlib.util
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path

# `gitenv` is loaded BY PATH, never by name: `import gitenv` and `from scripts import gitenv`
# each have a shadow hole (terra HIGH x3, 2026-08-08 -- see that module's docstring), and both
# holes end with the scrub silently becoming the EMPTY set. `spec_from_file_location` against a
# sibling path is the spelling no `sys.path` entry can intercept.
#
# THERE IS NO FALLBACK, DELIBERATELY. An earlier version returned None on a load failure and
# every date lookup then became `unmeasurable` -- which the audit leg renders `unavailable`, and
# the ship-gate does not block on `unavailable`. A broken loader would therefore have converted a
# STALE artifact into a quietly passing one: the gate disarming itself in the one situation where
# it should be loudest (terra, 2026-08-23). `gitenv.py` is a stdlib-only leaf sitting in this very
# directory, so a failure here means the `scripts/` tree is broken, and the right response is to
# fail LOUDLY at import -- `audit.py` will not import, `audit-health` errors, and somebody looks.
def _load_sibling(name: str):
    path = Path(__file__).resolve().with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(f"_gaf_{name}", path)
    if spec is None or spec.loader is None:  # pragma: no cover -- defensive
        raise ImportError(f"cannot load sibling module {path}")
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
    #: OPTIONAL exact verifier: `(repo_path) -> True (current) | False (drifted)`. When an
    #: artifact has one, its answer OUTRANKS the date relation, because it answers the same
    #: question exactly. A verifier that RAISES yields `unverifiable` (a WARN) rather than
    #: falling back to dates — see `_exact_verdict` for why that distinction is load-bearing.
    #:
    #: THIS FIELD EXISTS BECAUSE THE DATE RELATION HAS A FLOOR OF ONE DAY, and for one
    #: artifact that floor swallowed the whole guarantee (terra HIGH, 2026-08-26). `%cs` is a
    #: calendar DATE: an audit committed and an index regenerated on the same day are `0d
    #: stale`, i.e. `fresh`, no matter which happened first -- and audits land ~10/day, so the
    #: `audits-index` leg would have reported clean on essentially every real staleness it was
    #: registered to catch. Day granularity is right for the dashboard (a multi-input artifact
    #: with no cheap exact check, where the question really is "has an input moved since?");
    #: it is simply not an answer for an artifact whose generator can regenerate-and-diff in
    #: milliseconds. So the relation is kept as the general fallback and exactness is opt-in.
    #:
    #: A verifier is a CALLABLE, not a shell command, on purpose: no subprocess, no PATH, no
    #: quoting, and it stays trivially injectable in tests. It must be read-only and must not
    #: raise -- `_exact_verdict` converts any exception into `unverifiable` rather than
    #: letting a verifier wedge the leg that calls it, or quietly excuse it.
    content_check: object | None = None


#: `[#171]` stage 1, ADR-86. `inputs` mirrors `gen_dashboard.INPUT_RELPATHS`; see the module
#: docstring for why it is a literal, and the agreement test that keeps it honest.
#: `docs/intake/archive` is inside `docs/intake` and needs no separate entry.
#: The input set is DATA + CODE. The code half is not decoration: a change to the generator or to
#: any parser it borrows changes what is rendered, so an artifact left uncommitted across a parser
#: rewrite is stale in exactly the sense this leg means. A first version of this list carried only
#: the data half and would have reported "fresh" forever across such a rewrite -- found by terra,
#: 2026-08-23, and it is the one defect in this module that could have made it decorative.
DASHBOARD = GeneratedArtifact(
    name="conformance-dashboard",
    outputs=("ecosystem/conformance.md", "ecosystem/conformance.html"),
    inputs=("BACKLOG.md", "tasks", "docs/intake", "docs/decisions", "docs/audits",
            "scripts/gen_dashboard.py", "scripts/gen_task_tree.py",
            "scripts/gen_intake_index.py", "scripts/gen_claude_rosters.py",
            "scripts/backlog_source.py"),
    baseline_days=4,
    regen_command="python scripts/gen_dashboard.py --write",
    # Gitignored (`.gitignore:95`) and absent as of 2026-08-23; the generator existence-probes it
    # and reads its size. It has no git history, so it cannot carry a commit date and cannot
    # participate in a git-date relation. Stated, not silently dropped.
    untracked_inputs=("logs/TELEMETRY.db",),
)

#: `inputs` is DATA + CODE, the same rule the dashboard's set follows. Note the index EXCLUDES
#: itself from its own scan (`gen_audit_index.collect_audits` skips README.md), so listing the
#: directory here cannot make the artifact its own input.
def _audit_index_matches(repo_path: Path) -> bool | None:
    """Regen-and-diff the audits index IN `repo_path`. True current / False drifted / None n-a.

    The SAME comparison `gen_audit_index --check` makes, called in-process rather than shelled
    out, so the gate and the CLI cannot disagree about what current means. Repo-parameterized
    through the generator's own `audits_dir` / `tracked` arguments, so it answers about the
    repo it is handed rather than about the module's pinned globals.

    IT INHERITS THE GENERATOR'S DETERMINISM BOUNDARY, including its fail-open edge: outside a
    git work tree `tracked_files` returns None and filtering is DISABLED, so an untracked
    scratch audit would then read as drift. Inside a checkout — the only place this leg runs —
    an untracked file is correctly not drift, which is what keeps the verdict a function of
    COMMITTED state rather than of one machine's private files.
    """
    try:
        from scripts import gen_audit_index as _gai
    except ImportError:  # pragma: no cover - the scripts/-on-sys.path entrypoint
        import gen_audit_index as _gai
    audits = Path(repo_path) / "docs" / "audits"
    target = audits / "README.md"
    if not target.is_file():
        return None          # absence is the date leg's verdict to give, not this one's
    return target.read_text(encoding="utf-8") == _gai.render_index(
        audits, _gai.tracked_files(Path(repo_path)), Path(repo_path))


#: `[#590]` — the audits index, registered here on 2026-08-26 as the OTHER HALF of taking
#: `docs/audits/README.md` out of the merge path. Its `audit-index-freshness` pre-commit hook
#: was narrowed to the index itself the same day, so a lane writing an audit no longer has to
#: regenerate and commit it — which is exactly what had put this file in 6 of the last 7
#: conflicted merges. Removing that obligation without replacing the guarantee would leave the
#: index free to rot silently, so the guarantee moved to SHIP time, where the index is
#: actually read: this leg refuses an index that does not match what its generator emits, and
#: `cmd_ship_gate` REDs on an undispositioned WARN. The integrator discharges it by running
#: the regen command below and committing the result.
#:
#: `content_check` is what makes that guarantee REAL rather than nominal — see the field's own
#: docstring for the one-day floor that made the date relation blind here. `baseline_days=0`
#: remains as the fallback relation for the case where the exact check cannot answer.
AUDIT_INDEX = GeneratedArtifact(
    name="audits-index",
    outputs=("docs/audits/README.md",),
    inputs=("docs/audits", "scripts/gen_audit_index.py"),
    baseline_days=0,
    regen_command="uv run --locked python scripts/gen_audit_index.py --write",
    content_check=_audit_index_matches,
)

REGISTRY: tuple[GeneratedArtifact, ...] = (DASHBOARD, AUDIT_INDEX)

#: verdict -> the audit `Finding.status` it must be reported as. THE MAPPING LIVES HERE, not in
#: the audit leg, and that is a structural answer to a defect terra found twice (2026-08-23): a
#: leg written as `if stale: warn / else: pass` silently reported every verdict added afterwards
#: as a PASS. With the table here, the leg is a lookup, an unknown verdict raises `KeyError`
#: instead of passing quietly, and a verdict cannot be added without deciding what it means.
#: `unmeasurable` maps to `unavailable`; the audit leg overrides it to `n/a` SUBJECT-ABSENT when
#: `Measurement.subject_absent` is set (a consumer repo that simply has no such artifact).
STATUS_FOR_VERDICT: dict[str, str] = {
    "fresh": "pass",
    "stale": "warn",          # older than its inputs by more than the measured baseline
    "deleted": "warn",        # has git history, gone from the tree
    "uncommitted": "warn",    # present in the tree, never committed -- "committed-generated" is
                              # the zone class's own claim, so this violates its premise
    "unverifiable": "warn",   # a DECLARED input could not be measured, so the relation over the
                              # rest cannot be presented as a freshness verdict
    "content-stale": "warn",  # [#590] — the EXACT verdict: the artifact does not match what
                              # its generator emits. Distinct from `stale`, which is a
                              # DATE relation and can only ever say "an input moved since";
                              # this one says "regenerating would change these bytes", which
                              # is the claim the reader of a generated index actually needs.
    "unmeasurable": "unavailable",
}

#: The verdicts that must produce a WARN. Derived, so it cannot drift from the table above.
WARN_VERDICTS: tuple[str, ...] = tuple(
    v for v, status in STATUS_FOR_VERDICT.items() if status == "warn")


def git_last_commit_date(repo_path: Path, pathspec: str) -> date | None:
    """COMMITTER date (`%cs`) of the newest commit touching `pathspec`, or None.

    ONE DATE SEMANTIC, ON BOTH SIDES, and it is deliberately NOT the sibling's. This is the one
    place the leg diverges from `canonical_freshness_gate`, and the divergence is forced by the
    question, not by taste:

      * The sibling compares a git date against a `last_reviewed` STAMP A HUMAN WROTE, so its
        question is *when was the content edited* -- and author date is right, because it survives
        rebase / cherry-pick / amend.
      * This leg compares two git dates AGAINST EACH OTHER. Its question is *did any input land in
        this history after the artifact landed* -- an ordering question about THIS history, which
        is exactly what committer date records.

    Author date is wrong here in both directions, and terra demonstrated both (2026-08-23): a
    cherry-picked INPUT keeps its original author date and hides behind it, reporting `fresh`
    while the checked-out input is genuinely newer; and a rebased OUTPUT keeps its old author date
    and reports a spurious `stale`. An earlier version took `max(author, committer)` on inputs and
    `min` on outputs to be conservative in both directions -- which fixed the first hole, kept the
    second, and left the module with no single stated relation. Committer date on both sides is
    one semantic that answers the actual question; a whole-branch rebase rewrites every committer
    date uniformly, so relative order -- the only thing this relation reads -- is preserved.

    `--first-parent`, AND IT IS LOAD-BEARING IN THIS REPO SPECIFICALLY. Core-invariant #5 makes
    every change arrive by `--no-ff` merge, so a plain `git log -1 -- <path>` follows the path
    into the SIDE BRANCH and answers with the feature commit rather than the merge that put the
    path on this branch. A lane whose commits are three weeks old but which merges today would
    then measure as three weeks OLD -- reported `fresh` indefinitely, in the exact workflow this
    repo mandates (terra, 2026-08-23). Walking the first-parent spine answers *when did this land
    HERE*, which is the question. It is also the repo's own idiom for landing-order: `block_ff_push`
    and `validate_no_ff` scan `--first-parent` for the same reason.

    The repo-location env vars are SCRUBBED via `gitenv`: an inherited `GIT_DIR` overrides both
    `cwd=` and `git -C`, which is how a validator comes to read the parent repo while labelling
    the answer with the target's id ([#355]). Returns None when git is absent, the path is not a
    repo, or the pathspec has no history on this branch's spine.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "log", "-1", "--first-parent", "--format=%cs",
             "--", pathspec],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=_gitenv.scrubbed_git_env(),
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


def _git_available(repo_path: Path) -> bool:
    """Is `repo_path` inside a git repo this process can read? One cheap `rev-parse`.

    Exists so "git could not answer" is distinguishable from "this path has no history". They
    look identical from a single `git log` call, and collapsing them makes a non-git checkout
    report a committed artifact as never-committed.
    """
    try:
        r = subprocess.run(["git", "-C", str(repo_path), "rev-parse", "--git-dir"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env=_gitenv.scrubbed_git_env())
    except OSError:
        return False
    return r.returncode == 0


@dataclass(frozen=True)
class Measurement:
    """The P5-shaped relation for one artifact, plus the evidence that produced it."""

    artifact: str
    verdict: str                      # a key of STATUS_FOR_VERDICT
    #: Only meaningful when `verdict == "unmeasurable"`. True when an output FILE is absent from
    #: disk (a consumer repo that simply has no dashboard -> the audit leg renders `n/a`
    #: SUBJECT-ABSENT); False when the file is there but git could not answer (-> `unavailable`).
    #: The two are different facts and collapsing them is exactly the "skip rendered as pass"
    #: class `_na_reason` exists to prevent.
    subject_absent: bool
    staleness_days: int | None
    baseline_days: int
    output_date: date | None
    stalest_output: str | None
    input_date: date | None
    newest_input: str | None
    detail: str


def _exact_verdict(repo_path: Path, artifact: GeneratedArtifact) -> bool | None:
    """Run `artifact.content_check`, or None when it has none / cannot answer.

    NEVER RAISES, and that is the contract the field's docstring promises. A verifier is
    generator code called from inside a gate leg; letting it propagate would let a bug in a
    generator wedge the audit that reports on it.

    BUT A FAILED VERIFIER IS NOT "NO VERIFIER" (terra HIGH, round 2). The first version
    swallowed the exception and returned None, which falls back to the date relation — and
    for the very artifact this field exists for, that relation returns `fresh` on a same-day
    pair. So an index whose exact verification CRASHED would have been reported clean: the
    green-by-skip state the whole field was added to prevent, reintroduced by its own error
    handler. A configured-but-failing verifier is now `unverifiable` (a WARN), which is the
    verdict this module already uses for "a declared input could not be measured, so the
    relation over the rest is not a verdict".

    Three answers, deliberately not two: `None` = no verifier declared (fall back to dates),
    `"unverifiable"` = declared and could not answer, `True`/`False` = it answered.
    """
    check = artifact.content_check
    if check is None:
        return None
    try:
        return check(repo_path)
    except Exception:  # noqa: BLE001 — see the docstring: a verifier must not wedge the leg
        return "unverifiable"


def measure(repo_path: Path, artifact: GeneratedArtifact = DASHBOARD, *,
            git_date_fn=git_last_commit_date) -> Measurement:
    """Compare the artifact's own commit date against the newest of its inputs'.

    `output_date` is the **minimum** across the output faces: two faces are written by one run
    and normally share a commit, but if one ever lags, the pair is as fresh as its stalest half.
    `input_date` is the **maximum** across the inputs: any one input moving forward is what makes
    the artifact out of date.

    SIX VERDICTS, because a shorter list kept collapsing a defect into a pass -- each one is a
    distinct real state with a distinct operator action, and `STATUS_FOR_VERDICT` says what each
    reports as:

      fresh         within the baseline
      stale         older than its inputs by more than the baseline
      deleted       has git history, gone from the tree
      uncommitted   present in the tree, never committed (the zone class claims otherwise)
      unverifiable  a DECLARED input (or one face of a multi-face artifact) cannot be measured --
                    the relation over what remains is not a verdict and must not be shown as one
      unmeasurable  nothing here to govern (with `subject_absent`, a repo that has no such
                    artifact at all)
    """
    def _unmeasurable(detail: str, *, subject_absent: bool = False) -> Measurement:
        return Measurement(artifact.name, "unmeasurable", subject_absent, None,
                           artifact.baseline_days, None, None, None, None, detail)

    # GIT-ABSENT IS ITS OWN ANSWER, and it has to be checked before anything else. Without this,
    # a non-git checkout makes every date lookup return None, the outputs are present, and the
    # loop below concludes `uncommitted` -- WARNING that a committed artifact "was never
    # committed" purely because nothing could be asked. One probe, once, per measurement.
    if git_date_fn is git_last_commit_date and not _git_available(repo_path):
        return _unmeasurable("git is unavailable here — freshness cannot be measured")

    if not artifact.outputs:
        return _unmeasurable("artifact declares no outputs")

    # EVERY PATH IS QUERIED EXACTLY ONCE. An earlier version asked each input twice -- once to
    # test measurability, once to read the date -- doubling the subprocess cost of a check that
    # `cmd_health` runs on every commit (terra, 2026-08-23). One `git log` per declared path is
    # the floor, because the per-path date is what names the offender in the evidence.
    dates = {rel: git_date_fn(repo_path, rel)
             for rel in (*artifact.outputs, *artifact.inputs)}

    # ALL OUTPUT FACES ARE CLASSIFIED BEFORE ANY VERDICT IS RETURNED. Returning on the first face
    # let a two-face artifact with one never-present face short-circuit to `n/a` while the OTHER
    # face was stale -- an absence swallowing a defect (terra, 2026-08-23). Presence is read
    # first for each face, because `git log -1 -- <deleted-path>` answers with the DELETION
    # commit's recent date, and a date-first reading would call a deleted artifact `fresh`.
    absent_no_history, deleted, uncommitted = [], [], []
    out_dates: list[tuple[str, date]] = []
    for rel in artifact.outputs:
        present, d = (Path(repo_path) / rel).is_file(), dates[rel]
        if not present and d is None:
            absent_no_history.append(rel)      # never existed here
        elif not present:
            deleted.append((rel, d))           # has history, gone from the tree
        elif d is None:
            uncommitted.append(rel)            # in the tree, never committed
        else:
            out_dates.append((rel, d))

    # Ordered worst-first: a real defect on ANY face outranks absence on another.
    if deleted:
        rel, d = deleted[0]
        return Measurement(
            artifact.name, "deleted", False, None, artifact.baseline_days, None, rel, None, None,
            f"{artifact.name}: output {rel} is MISSING from the tree but has git history "
            f"(last touched {d.isoformat()}) — the committed generated artifact was deleted")
    if uncommitted:
        # `--check` does NOT catch this: it reports MISSING only for an ABSENT file, so a
        # present-but-untracked face passes it. And "committed-generated" is the zone class's own
        # claim, so this violates the leg's premise -- WARN, never a quiet `unavailable`.
        return Measurement(
            artifact.name, "uncommitted", False, None, artifact.baseline_days,
            None, uncommitted[0], None, None,
            f"{artifact.name}: output(s) present but with NO git history — "
            f"{', '.join(uncommitted)}; a committed-generated artifact that was never committed")
    if absent_no_history and out_dates:
        # Partial artifact: one face governed, another simply not here. Not "nothing to govern".
        return Measurement(
            artifact.name, "unverifiable", False, None, artifact.baseline_days,
            None, None, None, None,
            f"{artifact.name}: declared output(s) absent with no history — "
            f"{', '.join(absent_no_history)} — while {len(out_dates)} other face(s) exist; "
            f"a partial artifact cannot be given a freshness verdict")
    if not out_dates:
        # Every face absent and unhistoried: a repo that simply has no such artifact.
        return _unmeasurable(
            f"output(s) not present in this repo — {', '.join(absent_no_history)}",
            subject_absent=True)

    # EVERY DECLARED INPUT MUST BE MEASURABLE. An earlier version dropped unmeasurable inputs and
    # reported freshness from whatever remained -- so if the input that had actually moved was the
    # unreadable one, the artifact was called `fresh` on the strength of the others. That is the
    # gate quietly excusing itself, and terra named it (2026-08-23). A declared input that cannot
    # be measured is a defect in the DECLARATION (or a broken/shallow tree); either way the
    # relation over the survivors is not a freshness verdict and must not be presented as one.
    unmeasured = [rel for rel in artifact.inputs if dates[rel] is None]
    if unmeasured:
        return Measurement(
            artifact.name, "unverifiable", False, None, artifact.baseline_days,
            None, None, None, None,
            f"{artifact.name}: declared input(s) with no git history — "
            f"{', '.join(unmeasured)}; freshness cannot be verified over a partial input set")
    in_dates = [(rel, dates[rel]) for rel in artifact.inputs]

    stalest_output, output_date = min(out_dates, key=lambda pair: pair[1])
    newest_input, input_date = max(in_dates, key=lambda pair: pair[1])
    staleness = max(0, (input_date - output_date).days)
    verdict = "stale" if staleness > artifact.baseline_days else "fresh"
    detail = (f"{artifact.name}: {staleness}d stale (baseline {artifact.baseline_days}d) — "
              f"{stalest_output} committed {output_date.isoformat()}, newest input "
              f"{newest_input} committed {input_date.isoformat()}")

    # THE EXACT ANSWER OUTRANKS THE DATE RELATION ([#590]; terra HIGH 2026-08-26). Placed HERE
    # and not earlier on purpose: the classification above resolves absence, deletion and the
    # never-committed case, which are states the content check has no opinion about and which
    # would be mis-reported as "drifted" if it spoke first. Reaching this point means every
    # output face exists and is committed, so "do these bytes match a regeneration" is exactly
    # the right question — and where the answer is yes, it is also strictly better news than a
    # `0d stale` computed from calendar dates that cannot order two commits made today.
    exact = _exact_verdict(repo_path, artifact)
    if exact == "unverifiable":
        # A DECLARED verifier that could not answer. Reported, never swallowed into the date
        # relation — see `_exact_verdict`. Same posture the declared-input leg above takes.
        return Measurement(
            artifact.name, "unverifiable", False, None, artifact.baseline_days,
            None, None, None, None,
            f"{artifact.name}: its declared content verifier RAISED, so exactness cannot be "
            f"established; the {staleness}d commit-date relation is not a substitute — "
            f"regenerate and compare by hand: {artifact.regen_command}")
    if exact is False:
        verdict = "content-stale"
        detail = (f"{artifact.name}: does NOT match what its generator emits — regenerating "
                  f"would change {stalest_output}. ({staleness}d by commit date, which cannot "
                  f"see a same-day drift)")
    elif exact is True and verdict == "stale":
        # Dates say stale, bytes say identical. The bytes win, and the reason is named rather
        # than silently swallowed: an input can be touched by a commit that changes nothing
        # the generator renders (a comment, a reordering), and WARNing then is a false
        # positive that trains the reader to disposition this leg by reflex.
        verdict, detail = "fresh", (
            f"{artifact.name}: matches its generator exactly, despite {staleness}d by commit "
            f"date — an input moved without changing what is rendered")
    # THE BLIND SPOT RIDES ON THE FINDING, not only in this file's comments. An untracked input
    # has no commit date, so nothing it does can ever move the relation -- the artifact can be
    # reported fresh while a section rendered from that input is stale, indefinitely. Declaring
    # it in `untracked_inputs` documents the gap for a reader of the code; saying so in the
    # evidence puts it in front of whoever is reading the ship-gate (terra, 2026-08-23).
    #
    # A NOTE AND NOT A WARN, deliberately: the dashboard's telemetry section is a function of the
    # store's existence and SIZE, so once `[#529]`'s store lands, a WARN keyed on it would fire on
    # every emit. A gate that fires constantly gets routed around -- the same reasoning that put
    # this leg on the ship-gate rather than pre-commit. It is surfaced only when the untracked
    # input actually EXISTS, because an absent one contributes nothing to the render but "absent".
    live_untracked = [rel for rel in artifact.untracked_inputs
                      if (Path(repo_path) / rel).exists()]
    if live_untracked:
        detail += (f" [not covered: {', '.join(live_untracked)} — untracked, so changes to it "
                   f"cannot move this verdict]")
    return Measurement(artifact.name, verdict, False, staleness, artifact.baseline_days,
                       output_date, stalest_output, input_date, newest_input, detail)


def evaluate(repo_path: Path, artifacts: tuple[GeneratedArtifact, ...] | None = None, *,
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
        if m.verdict in WARN_VERDICTS:
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
