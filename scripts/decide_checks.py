#!/usr/bin/env python
"""decide_checks.py -- the `/decide` deterministic checks (R14; `[#964]`-adjacent).

WHY THIS EXISTS. The CI/OS-verification decision (`PROPOSAL-ADR-CI-VERIFICATION-2026-09-26`)
showed what a multi-model decision run catches that one seat does not -- and its own producer's
arithmetic was wrong in 12 of 15 matrix totals until a script recomputed them. R14 says CC
decides through the system (research, subagents, multi-model review, a Proposed ADR, the
operator's ratification) rather than by one seat's say-so, and names `/decide` as the command
that shape becomes. This module is the part of that shape which must never be a prompt: eight
checks the two source proposals name (`PROPOSAL-ADR-CI-VERIFICATION-2026-09-26-seat-71020de7.md`
Step 5, `PROPOSAL-ADR-REMOTE-LANE-OBSERVABILITY-2026-09-26.md` Step 5), each one a defect a
free-text review missed on the record.

POSTURE. Read-only (Layer-2, ADR-28/36): every check here reads a decision run's artifacts (an
evidence file, a matrix table, evaluator records, subagent briefs, an ADR draft) and reports
defects. Nothing here writes a decision, drafts an ADR, or calls a model -- that is `/decide`'s
job (`.claude/commands/decide.md`); this module is its gate.

THE EIGHT CHECKS (contract order):
  1. `check_paths_resolve`         -- every path:line / heading / sha / [#id] claim resolves.
  2. `check_matrix`                -- (recompute + unmeasured-cap share one parse; split below)
  3. `check_matrix`                -- a 4-5 score with no measured citation is capped at 3.
  4. `check_evaluator_attestation` -- served-model recorded and independent of the producer.
  5. `check_response_coverage`     -- every eval finding id has exactly one accept/reject row.
  6. `check_adr_sections`          -- size caps + the ADR-124 D5 sections (reuses
                                      `validate_adr_status.section_state`).
  7. `check_subagent_brief_exclusions` -- the exclusion list named in every subagent brief.
  8. `check_subagent_claims`       -- every relied-on subagent claim carries a machine-checkable
                                      probe, run here, or is marked `{unverified}`.

PREMISE-FAILED (recorded, not silently patched -- R14/R17; common rules S1 "CC validates").
Two of this contract's cited reuse targets do not exist in this tree:
  - `.claude/skills/preflight/SKILL.md` -- MISSING. Check 1 instead reuses the real mechanism,
    `scripts/preflight_contract.py::verify`, which the shipped `/preflight` command already
    wraps and which already existed before this lane (not a lane-scope-guard artefact at all).
  - `ecosystem/excluded-roots.yaml` ("as merged by lane-scope-guard") -- MISSING.
    `lane-scope-guard` FAILED terminally 2026-09-27T12:45 and was never merged (confirmed against
    `to-browser/SESSION-integrator-wave5b-n4-2026-09-26.md`: its STATE lines run
    REFUSED -> WAITING -> FAILED, and unlike `lane-claim-marker` / `lane-decide-command` /
    `lane-subagent-cost` / `lane-dispatch-port-hub` it was NOT one of the four lanes the
    integrator re-admitted at 15:16 -- it stays FAILED). `load_excluded_roots` below falls back
    to `_FALLBACK_EXCLUDED_ROOTS` (the one root R15 and this batch's own proposal name by hand:
    "OneDrive - Blue Yonder") and reads the real file transparently once it exists -- ROWS-OWED
    when it lands, not blocking check 7 meanwhile.

HONEST LIMITS.
  * Checks 2/3 (matrix) and 8 (subagent claims) are governed by a markup contract this module
    defines (`.claude/commands/decide.md` documents it for a producer to write against) -- they
    do not retrofit the historical proposal's free-form prose, which predates this mechanism.
  * Check 8's probes cover three forms (`path:line`, `git check-ignore <path>`,
    `grep -c '<pattern>' <path>`) -- the three kinds the two source proposals actually name
    ("path:line exists; `git check-ignore`; grep count"). A claim needing a different probe
    shape is `{unverified}` until this module grows one.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import yaml

import preflight_contract
import validate_adr_status as vas

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

#: A decision-run document's byte cap -- the same "pointer, not overflow" discipline this repo
#: applies to `CLAUDE.md` (ADR-53, common rules S2(c)), sized generously for an evidence file
#: or ADR draft rather than reused verbatim from a different document's budget.
DECIDE_DOC_BYTE_CAP = 65_536

#: The one root this batch's own proposal names by hand (a T5 subagent line-counted a file
#: under it while resolving `$PROFILE` -- PROPOSAL-ADR-CI-VERIFICATION Step 5, "Make it a
#: command/skill" bullet) -- kept until `ecosystem/excluded-roots.yaml` exists to read instead.
_FALLBACK_EXCLUDED_ROOTS: tuple[str, ...] = ("OneDrive - Blue Yonder",)


class DecideChecksError(RuntimeError):
    """An input could not be read or parsed -- exit 2, never a silent pass."""


@dataclass(frozen=True)
class Defect:
    rule: str
    where: str
    detail: str

    def render(self) -> str:
        return f"  [{self.rule}] {self.where} -- {self.detail}"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise DecideChecksError(f"unreadable: {path} ({exc})") from exc


# --- check 1: paths resolve (reuses preflight_contract) -------------------------------------

def check_paths_resolve(evidence_files: Sequence[Path],
                        repo_root: Path = _REPO_ROOT) -> list[Defect]:
    """Every `path:line` / heading / sha / `[#id]` claim in each file resolves.

    Delegates entirely to `preflight_contract.verify` -- the "existing /preflight" the contract
    names -- rather than re-implementing locator resolution.
    """
    defects: list[Defect] = []
    for f in evidence_files:
        if not f.is_file():
            raise DecideChecksError(f"not a file: {f}")
        report = preflight_contract.verify(f, repo_root)
        for claim in report.failed:
            defects.append(Defect("decide.paths_resolve", str(f),
                                  f"[{claim.kind}] {claim.raw}"
                                  + (f" -- {claim.detail}" if claim.detail else "")))
    return defects


# --- checks 2/3: the matrix ------------------------------------------------------------------
#
# Markup contract (`.claude/commands/decide.md` documents this for a producer):
#
#   Weights: fidelity=25 portability=20 throughput=20 cost=10 modifiability=10 observability=15
#   | Option | fidelity | portability | throughput | cost | modifiability | observability | Σ |
#   |---|---|---|---|---|---|---|---|
#   | A1 today | 3 | 1 | 1 | 2 | 3 | 1 | 1.80 |
#   | A7 armed | 4[^1] | 4[^2] | 4 | 4 | 3 | 4 | 3.90 |
#
#   [^1]: measured -- run 36234959090, jobs/70677588/tmp/vtop-suite.log:561
#   [^2]: measured -- docs.github.com/actions/reference/runners, read 2026-09-26

_WEIGHTS_RE = re.compile(r"^Weights:\s*(?P<body>.+)$", re.MULTILINE)
_WEIGHT_PAIR_RE = re.compile(r"(?P<name>[A-Za-z][\w-]*)\s*=\s*(?P<weight>\d+(?:\.\d+)?)")
_TABLE_ROW_RE = re.compile(r"^\|(?P<cells>.+)\|\s*$", re.MULTILINE)
_SEP_CELL_RE = re.compile(r"^:?-{2,}:?$")
_CELL_SCORE_RE = re.compile(r"^(?P<score>\d+(?:\.\d+)?)(?:\[\^(?P<note>\w+)\])?$")
_FOOTNOTE_DEF_RE = re.compile(r"^\[\^(?P<note>\w+)\]:\s*(?P<body>.+)$", re.MULTILINE)


def _parse_weights(text: str) -> dict[str, float]:
    m = _WEIGHTS_RE.search(text)
    if not m:
        raise DecideChecksError("no `Weights: name=n ...` line found")
    return {name: float(weight) for name, weight in _WEIGHT_PAIR_RE.findall(m.group("body"))}


def _split_row(row: str) -> list[str]:
    return [c.strip() for c in row.strip("|").split("|")]


def _find_matrix_table(text: str, weight_names: Sequence[str]) -> tuple[list[str], list[list[str]]]:
    """The first table whose header carries every weighted column name, in order.

    CONTIGUOUS ONLY (terra HIGH, 2026-09-28): an evidence file routinely carries a SECOND table
    below the matrix -- a response table, another decision's matrix -- and reading every
    matched-header table's rows out of a flat, whole-document row list let that later table's
    rows be scored as if they were the matrix's own data. This walks physical lines from the
    header instead, and stops at the first line that is not part of THIS table (a blank line,
    prose, or a later table's own header)."""
    lines = text.splitlines()
    table_rows = [(i, _split_row(m.group("cells"))) for i, line in enumerate(lines)
                  if (m := _TABLE_ROW_RE.match(line))]
    by_line = dict(table_rows)
    for i, header in table_rows:
        lowered = [c.lower() for c in header]
        if not all(name.lower() in lowered for name in weight_names):
            continue
        if i + 1 not in by_line or not all(_SEP_CELL_RE.match(c) for c in by_line[i + 1]):
            continue  # a real table header is followed immediately by a separator row
        body: list[list[str]] = []
        j = i + 2
        while j in by_line:
            body.append(by_line[j])
            j += 1
        return header, body
    raise DecideChecksError("no matrix table header names every weighted column, "
                            "immediately followed by a separator row")


def check_matrix(evidence_file: Path) -> list[Defect]:
    """Checks 2 and 3: recomputed totals, and a 4-5 score capped without a measured citation."""
    text = _read(evidence_file)
    weights = _parse_weights(text)
    if abs(sum(weights.values()) - 100) > 0.01:
        return [Defect("decide.matrix_weights", str(evidence_file),
                       f"weights sum to {sum(weights.values())}, not 100: {weights}")]
    names = list(weights)
    header, rows = _find_matrix_table(text, names)
    lowered_header = [c.lower() for c in header]
    col_index = {name: lowered_header.index(name.lower()) for name in names}
    total_idx = next((i for i, c in enumerate(header) if c.strip("Σ ").lower() in ("", "sigma", "total")
                      or c.strip() in ("Σ", "Sigma", "Total")), None)
    if total_idx is None:
        raise DecideChecksError("matrix table has no Σ / Total column")

    footnotes = {m.group("note"): m.group("body") for m in _FOOTNOTE_DEF_RE.finditer(text)}
    defects: list[Defect] = []
    for row in rows:
        option = row[0] if row else "<row>"
        total = 0.0
        for name in names:
            cell = row[col_index[name]]
            m = _CELL_SCORE_RE.match(cell)
            if not m:
                defects.append(Defect("decide.matrix_cell", str(evidence_file),
                                      f"{option}/{name}: unparseable cell {cell!r}"))
                continue
            score = float(m.group("score"))
            total += score * weights[name]
            if score >= 4:
                note = m.group("note")
                cited = bool(note) and note in footnotes and "measured" in footnotes[note].lower()
                if not cited:
                    defects.append(Defect(
                        "decide.unmeasured_cap", str(evidence_file),
                        f"{option}/{name}: score {score:g} has no measured citation "
                        f"-- caps at 3"))
        expected = round(total / 100, 2)
        try:
            declared = float(row[total_idx])
        except ValueError:
            defects.append(Defect("decide.matrix_recomputed", str(evidence_file),
                                  f"{option}: Σ cell {row[total_idx]!r} is not a number"))
            continue
        if abs(declared - expected) > 0.005:
            defects.append(Defect("decide.matrix_recomputed", str(evidence_file),
                                  f"{option}: declared Σ {declared:g}, recomputed {expected:g}"))
    return defects


# --- check 4: evaluator attestation -----------------------------------------------------------

_FIELD_RE = re.compile(r"^(?P<key>[\w-]+):\s*(?P<value>.+)$", re.MULTILINE)


def _fields(text: str) -> dict[str, str]:
    return {m.group("key").lower(): m.group("value").strip()
            for m in _FIELD_RE.finditer(text)}


def check_evaluator_attestation(eval_files: Sequence[Path], producer_model: str) -> list[Defect]:
    """Each eval file declares a `served-model:` and `attestation-source:`, independent
    of the producer (`excludes_producer`)."""
    defects: list[Defect] = []
    producer = producer_model.strip().lower()
    for f in eval_files:
        fields = _fields(_read(f))
        served = fields.get("served-model", "")
        source = fields.get("attestation-source", "")
        if not served:
            defects.append(Defect("decide.evaluator_attestation", str(f),
                                  "no `served-model:` line"))
            continue
        if not source:
            defects.append(Defect("decide.evaluator_attestation", str(f),
                                  "no `attestation-source:` line"))
        if served.strip().lower() == producer:
            defects.append(Defect("decide.evaluator_not_independent", str(f),
                                  f"served-model {served!r} == producer {producer_model!r}"))
    return defects


# --- check 5: response coverage ----------------------------------------------------------------

_FINDING_ID_RE = re.compile(r"^-\s*id:\s*(?P<id>[A-Za-z][\w-]*)\b", re.MULTILINE)
_RESPONSE_ROW_RE = re.compile(
    r"^\|\s*(?P<id>[A-Za-z][\w-]*(?:\s*/\s*[A-Za-z][\w-]*)*)\s*\|.*\|\s*"
    r"(?P<response>\*\*(?:Accepted|Rejected)\b.*)\|\s*$", re.MULTILINE)


def check_response_coverage(eval_files: Sequence[Path], response_file: Path) -> list[Defect]:
    """Every finding id named across `eval_files` has exactly one accept/reject row.

    Duplicate ids are reported, not silently collapsed (terra HIGH, 2026-09-28): two distinct
    findings sharing one id used to disappear into a `set`, letting one response row satisfy
    both."""
    id_occurrences: list[tuple[str, Path]] = [
        (m.group("id"), f) for f in eval_files for m in _FINDING_ID_RE.finditer(_read(f))]
    counts: dict[str, int] = {}
    for fid, _ in id_occurrences:
        counts[fid] = counts.get(fid, 0) + 1
    defects: list[Defect] = [
        Defect("decide.duplicate_finding_id", str(f),
              f"finding id {fid!r} is used {counts[fid]} times across the evaluator files "
              "-- each finding needs its own id")
        for fid, f in id_occurrences if counts[fid] > 1]
    ids: set[str] = set(counts)
    response_text = _read(response_file)
    covered: dict[str, int] = {}
    for m in _RESPONSE_ROW_RE.finditer(response_text):
        for part in m.group("id").split("/"):
            covered[part.strip()] = covered.get(part.strip(), 0) + 1
    for fid in sorted(ids):
        n = covered.get(fid, 0)
        if n == 0:
            defects.append(Defect("decide.response_coverage", str(response_file),
                                  f"finding {fid} has no accept/reject row"))
        elif n > 1:
            defects.append(Defect("decide.response_coverage", str(response_file),
                                  f"finding {fid} has {n} rows, not exactly one"))
    return defects


# --- check 6: ADR sections + size caps ---------------------------------------------------------

_QA_HEADING_RE = re.compile(
    r"^ {0,3}(?P<h>#{2,4})\s+(?:\d+[.)]\s*)?[*_]*Quality attributes(?:[\s:*_]|$)",
    re.IGNORECASE)
_ATX_HEADING_RE = re.compile(r"^ {0,3}(?P<h>#{1,6})(?:\s|$)")


def _section_body(text: str, heading: re.Pattern[str]) -> str | None:
    """The body text under the first heading `heading` matches, up to the next heading of the
    same or shallower depth. `None` if the heading is absent. Simpler than
    `validate_adr_status.section_state` (no fence/comment/blockquote awareness) because it
    reads only documents this module's own producer wrote, never third-party ADRs."""
    lines = text.splitlines()
    depth: int | None = None
    body: list[str] = []
    for line in lines:
        if depth is None:
            m = heading.match(line)
            if m:
                depth = len(m.group("h"))
            continue
        h = _ATX_HEADING_RE.match(line)
        if h and len(h.group("h")) <= depth:
            break
        body.append(line)
    return "\n".join(body) if depth is not None else None


def check_adr_sections(adr_draft: Path) -> list[Defect]:
    """Size caps, plus the ADR-124 D5 required sections (Flip-condition, Alternatives
    considered -- reused from `validate_adr_status`; Quality attributes -- D5's new section,
    not yet wired into that module's own `REQUIRED_SECTIONS`, so checked here directly)."""
    text = _read(adr_draft)
    defects: list[Defect] = []
    size = len(text.encode("utf-8"))
    if size > DECIDE_DOC_BYTE_CAP:
        defects.append(Defect("decide.size_cap", str(adr_draft),
                              f"{size} bytes > cap {DECIDE_DOC_BYTE_CAP}"))
    for label, heading in (("Flip-condition", vas._FLIP_HEADING_RE),
                           ("Alternatives considered", vas._ALTS_HEADING_RE),
                           ("Quality attributes", _QA_HEADING_RE)):
        state = vas.section_state(text, heading)
        if state != "present":
            defects.append(Defect("decide.adr_section", str(adr_draft),
                                  f"`## {label}` is {state}"))
    qa_body = _section_body(text, _QA_HEADING_RE)
    if qa_body is not None:
        lowered = qa_body.lower()
        for sub in ("quality attribute(s)", "scenario", "response measure", "decision evidence"):
            if sub not in lowered:
                defects.append(Defect("decide.adr_section", str(adr_draft),
                                      f"`## Quality attributes` is missing its {sub!r} part "
                                      "(ADR-124 D5)"))
    return defects


# --- check 7: the exclusion list in every subagent brief ---------------------------------------

def load_excluded_roots(repo_root: Path = _REPO_ROOT) -> tuple[list[str], bool]:
    """`(roots, is_fallback)`. Prefers `ecosystem/excluded-roots.yaml`; falls back to
    `_FALLBACK_EXCLUDED_ROOTS` while `lane-scope-guard` stays unmerged (see module docstring)."""
    path = repo_root / "ecosystem" / "excluded-roots.yaml"
    if path.is_file():
        data = yaml.safe_load(_read(path)) or {}
        roots = data.get("roots", data) if isinstance(data, dict) else data
        if isinstance(roots, list) and roots:
            return [str(r) for r in roots], False
    return list(_FALLBACK_EXCLUDED_ROOTS), True


def check_subagent_brief_exclusions(brief_files: Sequence[Path],
                                    repo_root: Path = _REPO_ROOT) -> list[Defect]:
    roots, _ = load_excluded_roots(repo_root)
    defects: list[Defect] = []
    for f in brief_files:
        text = _read(f)
        for root in roots:
            if root not in text:
                defects.append(Defect("decide.subagent_exclusion", str(f),
                                      f"brief does not name excluded root {root!r}"))
    return defects


# --- check 8: subagent claims spot-checked ------------------------------------------------------

_CLAIMS_HEADING_RE = re.compile(r"^ {0,3}(?P<h>#{1,4})\s+Subagent claims\b", re.IGNORECASE)
_PROBE_RE = re.compile(r"\{probe:\s*(?P<probe>[^}]+)\}\s*$")
_UNVERIFIED_RE = re.compile(r"\{unverified\}\s*$")
_GREP_PROBE_RE = re.compile(r"^grep\s+-c\s+'(?P<pat>[^']*)'\s+(?P<path>\S+)$")
_PATH_LINE_PROBE_RE = re.compile(r"^(?P<path>[^:]+):(?P<line>\d+)$")


def _contained_path(repo_root: Path, rel: str) -> Path | None:
    """`repo_root / rel`, resolved, and refused if it escapes `repo_root` (terra HIGH,
    2026-09-28): an evidence file is subagent-authored prose a producer did not necessarily
    vet, and an unguarded join let a `{probe: ...}` reach an absolute path or a `..`-escaped
    one outside this decision's own repository -- exactly the frame-leaving R15 exists to
    refuse elsewhere. `None` means refused; never raises."""
    root = repo_root.resolve()
    candidate = (root / rel).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _run_probe(probe: str, repo_root: Path) -> tuple[bool, str]:
    probe = probe.strip()
    m = _GREP_PROBE_RE.match(probe)
    if m:
        target = _contained_path(repo_root, m.group("path"))
        if target is None:
            return False, f"probe path escapes the repository: {m.group('path')!r}"
        if not target.is_file():
            return False, f"grep target missing: {m.group('path')}"
        count = len(re.findall(m.group("pat"), _read(target)))
        return count > 0, f"{count} match(es)"
    if probe.startswith("git check-ignore "):
        path = probe[len("git check-ignore "):].strip()
        target = _contained_path(repo_root, path)
        if target is None:
            return False, f"probe path escapes the repository: {path!r}"
        result = subprocess.run(["git", "-C", str(repo_root), "check-ignore", path],
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        return result.returncode == 0, f"exit {result.returncode}"
    m = _PATH_LINE_PROBE_RE.match(probe)
    if m:
        line_no = int(m.group("line"))
        if line_no < 1:
            return False, f"line {line_no} is not a valid 1-indexed locator"
        target = _contained_path(repo_root, m.group("path"))
        if target is None:
            return False, f"probe path escapes the repository: {m.group('path')!r}"
        if not target.is_file():
            return False, f"file missing: {m.group('path')}"
        n_lines = len(_read(target).splitlines())
        return n_lines >= line_no, f"{n_lines} lines, cites line {line_no}"
    return False, f"unrecognised probe syntax: {probe!r}"


def check_subagent_claims(evidence_file: Path, repo_root: Path = _REPO_ROOT) -> list[Defect]:
    """Every claim in `## Subagent claims` carries a probe this module can run, or is
    `{unverified}` -- the "verify-the-subagent step" both source proposals ask for."""
    text = _read(evidence_file)
    body = _section_body(text, _CLAIMS_HEADING_RE)
    if body is None:
        return [Defect("decide.subagent_claims", str(evidence_file),
                       "no `## Subagent claims` section")]
    defects: list[Defect] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        if _UNVERIFIED_RE.search(stripped):
            continue
        m = _PROBE_RE.search(stripped)
        if not m:
            defects.append(Defect("decide.subagent_claim_unchecked", str(evidence_file),
                                  f"no {{probe: ...}} or {{unverified}} marker: {stripped}"))
            continue
        ok, detail = _run_probe(m.group("probe"), repo_root)
        if not ok:
            defects.append(Defect("decide.subagent_claim_probe_failed", str(evidence_file),
                                  f"{stripped} -- {detail}"))
    return defects


# --- CLI -----------------------------------------------------------------------------------

def _print_defects(label: str, defects: list[Defect]) -> None:
    if not defects:
        print(f"decide_checks: {label}: 0 defects")
        return
    print(f"decide_checks: {label}: {len(defects)} defect(s)")
    for d in defects:
        print(d.render())


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except (AttributeError, ValueError, OSError):
            pass

    # `--repo-root` is on a shared PARENT parser, added to every subparser, so it may be
    # written either before or after the subcommand name -- argparse does not let a
    # top-level-only option follow a subparser's own positional args.
    repo_root_parent = argparse.ArgumentParser(add_help=False)
    repo_root_parent.add_argument("--repo-root", default=str(_REPO_ROOT))

    ap = argparse.ArgumentParser(prog="decide_checks",
                                 description="The /decide command's eight deterministic checks.",
                                 parents=[repo_root_parent])
    sub = ap.add_subparsers(dest="check", required=True)

    p1 = sub.add_parser("paths", parents=[repo_root_parent],
                        help="check 1: every path/heading/sha/[#id] claim resolves")
    p1.add_argument("files", nargs="+", type=Path)

    p2 = sub.add_parser("matrix", parents=[repo_root_parent],
                        help="checks 2/3: totals recomputed; 4-5 needs a citation")
    p2.add_argument("file", type=Path)

    p3 = sub.add_parser("evaluators", parents=[repo_root_parent],
                        help="check 4: served-model attestation + independence")
    p3.add_argument("files", nargs="+", type=Path)
    p3.add_argument("--producer-model", required=True)

    p4 = sub.add_parser("response-coverage", parents=[repo_root_parent],
                        help="check 5: every finding id has one row")
    p4.add_argument("eval_files", nargs="+", type=Path)
    p4.add_argument("--response-file", required=True, type=Path)

    p5 = sub.add_parser("adr-sections", parents=[repo_root_parent],
                        help="check 6: size caps + ADR-124 D5 sections")
    p5.add_argument("file", type=Path)

    p6 = sub.add_parser("subagent-exclusions", parents=[repo_root_parent],
                        help="check 7: exclusion list in every brief")
    p6.add_argument("files", nargs="+", type=Path)

    p7 = sub.add_parser("subagent-claims", parents=[repo_root_parent],
                        help="check 8: claims spot-checked or unverified")
    p7.add_argument("file", type=Path)

    args = ap.parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path(args.repo_root)

    try:
        if args.check == "paths":
            defects = check_paths_resolve(args.files, repo_root)
        elif args.check == "matrix":
            defects = check_matrix(args.file)
        elif args.check == "evaluators":
            defects = check_evaluator_attestation(args.files, args.producer_model)
        elif args.check == "response-coverage":
            defects = check_response_coverage(args.eval_files, args.response_file)
        elif args.check == "adr-sections":
            defects = check_adr_sections(args.file)
        elif args.check == "subagent-exclusions":
            defects = check_subagent_brief_exclusions(args.files, repo_root)
        elif args.check == "subagent-claims":
            defects = check_subagent_claims(args.file, repo_root)
        else:  # pragma: no cover -- argparse `required=True` on the subparsers forecloses this
            raise DecideChecksError(f"unknown check {args.check!r}")
    except DecideChecksError as exc:
        print(f"decide_checks: INTERNAL ERROR: {exc} -- refusing to report clean",
              file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 -- fail CLOSED
        print(f"decide_checks: INTERNAL ERROR: {exc!r} -- refusing to report clean",
              file=sys.stderr)
        return 2

    _print_defects(args.check, defects)
    return 1 if defects else 0


if __name__ == "__main__":
    sys.exit(main())
