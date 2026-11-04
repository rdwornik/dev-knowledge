"""The landing's read of a conductor round: its phase receipts, and what the run cost ([#1858]).

TWO READS OVER FILES THE HARNESS ALREADY LEAVES, both read-only except the explicit cost write:

* `landing_problems` (C12) -- the check `merge_path.land()` runs, before any push, for a lane a
  conductor round took to ACCEPT. It returns a list of problem strings (empty = the chain holds).
  The round is the HIGHEST-numbered `r<N>` directory under `<home>/LANE-<slug>/`; its own rendered
  `harness.contract.yaml` names the phases it ran and the gate of each; `P2..P7` are always
  required (P1 is outside the ratified range, ruling Q-G-1b). Every required receipt must validate
  as a `PhaseReceipt` of the one lane and row, and carry the `head_sha` it ran on: equal to the
  lane tip for every phase after P3, an ancestor-or-equal of it for P2 and P3 (which ran before
  their own commits). P7 must carry the payload outcome ACCEPT, the round must hold a
  `ROUND-VERDICT.json` ACCEPT at the tip, and the owed artifacts must exist (a payload for a
  `gate: payload` phase, an OUTPUT file for a `gate: exit` phase, a landable CI verdict for P6c).
  It proves the receipts are present, consistent and tip-current, NOT that no one forged them:
  forging needs write access to the receipts home, the trust the LAUNCH receipt already has.

* `cost_record` (C24) -- `run-cost/1`: one row per attempt, read from the artifacts `run_phase`
  leaves in the round directory, totalled per provider and unit. A phase whose artifact is absent
  or lacks the field is `measured: false` with a reason and is counted in `unmeasured_attempts`,
  never summed as zero. The caps that bound a run are another lane's; this module only measures.

Run as a script: `round_receipts.py check --lane L --tip SHA [--receipts DIR]` and
`round_receipts.py cost --lane L --receipts DIR [--write]`.
"""

from __future__ import annotations

import json
import os
import string
import sys
import types
from pathlib import Path, PureWindowsPath
from typing import Callable, Optional, Sequence

import click
import yaml

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
for _path in (str(_SCRIPTS), str(_REPO_ROOT)):  # dual-import shim, as every sibling uses
    if _path not in sys.path:
        sys.path.insert(0, _path)
from ecosystem.schema import phase_receipt as _pr  # noqa: E402

Runner = Callable[[Sequence[str]], "tuple[int, str]"]

#: The receipt field the lane tip is compared with (`PhaseReceipt.head_sha`).
RECEIPT_HEAD_FIELD = "head_sha"
#: The harness the round RAN under, rendered into every round directory by the conductor.
ROUND_HARNESS_NAME = "harness.contract.yaml"
#: The conductor's durable verdict for a round.
ROUND_VERDICT_NAME = "ROUND-VERDICT.json"
COST_NAME = "RUN-COST.json"
COST_SCHEMA = "run-cost/1"

#: Always required, whatever the round's harness lists. P1 is outside the ratified range.
FLOOR_PHASES = ("P2", "P3", "P4", "P5", "P6a", "P6b", "P7")
#: These ran BEFORE their own commits, so their head is an ancestor of the tip, not the tip.
EARLY_PHASES = ("P2", "P3")
JUDGE_PHASE = "P7"
CI_PHASE = "P6c"

_HEX = frozenset("0123456789abcdef")
_EXTENSIONS = (".exe", ".cmd", ".ps1", ".bat")
_TOKENS_MARK = "tokens used"

COMPLETE_MEANS = (
    "complete is true when every SURVIVING receipt was measured from its surviving artifact; a "
    "rerun of a phase overwrites its OUTPUT, usage file and receipt and leaves no trace of the "
    "attempt it replaced, so such an attempt is not counted here; only a fallback substitution "
    "leaves a visible primary row"
)


# --- helpers ----------------------------------------------------------------------------------

def receipts_home(root) -> Path:
    """The receipts home `land()` already reads for the LAUNCH receipt."""
    env = os.environ.get("HARNESS_RECEIPTS_DIR")
    return Path(env) if env else Path(root) / "logs" / "receipts"


def _split_phase(name: str) -> "Optional[tuple[int, str]]":
    """`P<digits><lowercase letters>` -> (number, suffix), else None. ASCII only."""
    if not name.startswith("P") or not name.isascii():
        return None
    body = name[1:]
    digits = body.rstrip(string.ascii_lowercase)
    suffix = body[len(digits):]
    return (int(digits), suffix) if digits.isdigit() else None


def _phase_key(phase: str) -> "tuple[int, str]":
    split = _split_phase(phase)
    return split if split else (10**6, phase)


def _is_receipt_file(name: str) -> bool:
    return name.endswith(".json") and _split_phase(name[: -len(".json")]) is not None


def _round_number(name: str) -> Optional[int]:
    body = name[1:]
    return int(body) if name.startswith("r") and body.isascii() and body.isdigit() else None


def _is_full_sha(value) -> bool:
    return isinstance(value, str) and len(value) == 40 and set(value) <= _HEX


def _slug_ok(slug) -> bool:
    import subst_gate
    return bool(subst_gate._SLUG_RE.match(slug or ""))


def _default_git(root) -> Runner:
    import merge_path
    return merge_path._run_git(Path(root))


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _is_ancestor(git: Runner, older: str, newer: str) -> "tuple[Optional[bool], str]":
    """(True | False | None when git cannot answer, git's output)."""
    code, out = git(["merge-base", "--is-ancestor", older, newer])
    if code == 0:
        return True, out
    if code == 1:
        return False, out
    return None, out.strip()[:160]


# --- C12: the landing check -------------------------------------------------------------------

def _round_dirs(lane_dir: Path) -> "list[tuple[int, Path]]":
    found = []
    try:
        entries = list(lane_dir.iterdir())
    except OSError:
        return []
    for entry in entries:
        number = _round_number(entry.name)
        if number is not None and entry.is_dir():
            found.append((number, entry))
    return sorted(found)


def _read_harness(path: Path) -> "tuple[Optional[dict], str]":
    """{phase id: gate} of the round's rendered harness, or (None, why)."""
    if not path.is_file():
        return None, f"{ROUND_HARNESS_NAME}: the harness the round ran under is missing: {path}"
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return None, f"{ROUND_HARNESS_NAME}: {path} is unreadable: {exc.__class__.__name__}"
    rows = doc.get("phases") if isinstance(doc, dict) else None
    if not isinstance(rows, list):
        return None, f"{ROUND_HARNESS_NAME}: {path} has no `phases:` list"
    gates: dict = {}
    for row in rows:
        phase_id = row.get("id") if isinstance(row, dict) else None
        if not isinstance(phase_id, str) or _split_phase(phase_id) is None:
            return None, f"{ROUND_HARNESS_NAME}: {path} names a phase id {phase_id!r} that is not P<n>"
        gates[phase_id] = row.get("gate")
    return gates, ""


def _check_sha(phase: str, path: Path, head, tip: str, git: Runner, problems: list) -> None:
    """Rule (d) for one phase after the head field was read."""
    if not isinstance(head, str) or not _is_full_sha(head.strip().lower()):
        problems.append(f"{phase}: {path} {RECEIPT_HEAD_FIELD} {head!r} is not a full 40-hex sha "
                        f"(the lane tip is {tip})")
        return
    if phase in EARLY_PHASES:
        verdict, out = _is_ancestor(git, head, tip)
        if verdict is None:
            problems.append(f"{phase}: {path} ancestry of {RECEIPT_HEAD_FIELD} {head} against the "
                            f"lane tip {tip} could not be read: {out}")
        elif not verdict:
            problems.append(f"{phase}: {path} {RECEIPT_HEAD_FIELD} {head} is not an ancestor of the "
                            f"lane tip {tip}")
        return
    import merge_path
    if not merge_path._same(head, tip):
        problems.append(f"{phase}: {path} ran on {head} but the lane tip is {tip}: a stale receipt "
                        f"is refused")


def _check_ci_output(path: Path, tip: str, problems: list) -> None:
    """P6c's OUTPUT: ONE JSON object whose sha is the tip and which `merge_path.is_landable` accepts."""
    import merge_path
    if not path.is_file():
        problems.append(f"{CI_PHASE}: the CI verdict {path} is missing")
        return
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        obj = None
    if not isinstance(obj, dict):
        problems.append(f"{CI_PHASE}: {path} is not one JSON object")
        return
    if not merge_path._same(str(obj.get("sha") or ""), tip):
        problems.append(f"{CI_PHASE}: {path} judged sha {obj.get('sha')!r}, not the lane tip {tip}")
    state = obj.get("state")
    if not isinstance(state, str) or not state:
        problems.append(f"{CI_PHASE}: {path} carries no `state`")
        return
    verdict = types.SimpleNamespace(state=state, missing_contexts=tuple(obj.get("missing_contexts") or ()))
    if not merge_path.is_landable(verdict):
        problems.append(f"{CI_PHASE}: {path} is not landable (state {state!r}, missing contexts "
                        f"{list(verdict.missing_contexts)})")


def _check_round_verdict(round_dir: Path, tip: str, problems: list) -> None:
    """The conductor's durable verdict: lane A's post-P7 independence check can refuse an accepted P7."""
    import merge_path
    path = round_dir / ROUND_VERDICT_NAME
    prefix = f"{JUDGE_PHASE}: round verdict {path}"
    if not path.is_file():
        problems.append(f"{prefix} is missing")
        return
    data = _read_json(path)
    if not isinstance(data, dict):
        problems.append(f"{prefix} is unreadable")
        return
    if data.get("verdict") != "ACCEPT":
        problems.append(f"{prefix} says {data.get('verdict')!r}, not ACCEPT (refused_by "
                        f"{data.get('refused_by')!r}, halted_at {data.get('halted_at')!r})")
    if not merge_path._same(str(data.get("head_sha") or ""), tip):
        problems.append(f"{prefix} was written at {data.get('head_sha')!r}, not the lane tip {tip}")


def landing_problems(root, slug: str, lane_tip: str, git: Optional[Runner] = None,
                     receipts_dir=None) -> list:
    """Everything wrong with the lane's last round as the evidence for landing `lane_tip`.
    Empty = pass. Reads files and runs one `git merge-base` per early phase; writes nothing."""
    if not _slug_ok(slug):
        return [f"lane slug {slug!r} is not a valid slug: no receipts path is built from it"]
    git = git or _default_git(root)
    home = Path(receipts_dir) if receipts_dir else receipts_home(root)
    lane_dir = home / f"LANE-{slug}"
    rounds = _round_dirs(lane_dir)
    if not rounds:
        return [f"no round directory (r<N>) under {lane_dir}: no conductor round left receipts for "
                f"lane {slug}"]
    round_no, round_dir = rounds[-1]
    tied = [str(path) for number, path in rounds if number == round_no]
    if len(tied) > 1:
        return [f"round {round_no} has several directories ({', '.join(tied)}): the highest-numbered "
                f"round is ambiguous and no receipt chain is chosen by name order"]
    gates, why = _read_harness(round_dir / ROUND_HARNESS_NAME)
    if gates is None:
        return [why]
    required = sorted(set(FLOOR_PHASES) | (set(gates) - {"P1"}), key=_phase_key)
    problems: list = []

    # the receipt set must match the harness the round ran under
    for entry in sorted(round_dir.iterdir()):
        if _is_receipt_file(entry.name):
            phase = entry.stem
            if phase != "P1" and phase not in required:
                problems.append(f"{phase}: receipt {entry} is not a phase of the round's harness: "
                                f"the harness source disagrees with the round ({ROUND_HARNESS_NAME} "
                                f"is missing or the root harness differs)")

    heads: dict = {}
    reference_row: Optional[str] = None
    for phase in required:
        path = round_dir / f"{phase}.json"
        if not path.is_file():
            problems.append(f"{phase}: receipt {path} is missing")
            continue
        data = _read_json(path)
        if not isinstance(data, dict):
            problems.append(f"{phase}: receipt {path} is unreadable")
            continue
        try:
            _pr.PhaseReceipt.model_validate(data)
        except ValueError as exc:
            problems.append(f"{phase}: receipt {path} is not a valid PhaseReceipt: "
                            f"{str(exc).splitlines()[0][:120]}")
            continue
        import run_phase
        if not run_phase.phase_succeeded(data):
            problems.append(f"{phase}: receipt {path} did not succeed (status {data.get('status')!r}, "
                            f"outcome {(data.get('payload') or {}).get('outcome')!r})")
        for key, expected in (("lane", slug), ("phase", phase), ("round", round_no)):
            if data.get(key) != expected:
                problems.append(f"{phase}: receipt {path} says {key} {data.get(key)!r}, not {expected!r}")
        row = data.get("row")
        if not row:
            problems.append(f"{phase}: receipt {path} has an empty row")
        elif reference_row is None:
            reference_row = row
        elif row != reference_row:
            problems.append(f"{phase}: receipt {path} is for row {row!r}, the chain's row is "
                            f"{reference_row!r}")
        head = data.get(RECEIPT_HEAD_FIELD)
        if head is None:
            problems.append(f"{phase}: receipt {path} has no {RECEIPT_HEAD_FIELD} (key absent or null): "
                            f"it is bound to no sha")
        else:
            heads[phase] = (head, path)
            _check_sha(phase, path, head, lane_tip, git, problems)
        gate = gates.get(phase, "payload")
        if gate == "exit":
            output = round_dir / f"{phase}-OUTPUT.txt"
            if not output.is_file():
                problems.append(f"{phase}: the gate is exit and {output} is missing")
        elif data.get("payload") is None or data.get("payload_sha256") is None:
            problems.append(f"{phase}: receipt {path} carries no payload (gate {gate!r})")
        if phase == JUDGE_PHASE:
            outcome = (data.get("payload") or {}).get("outcome")
            if outcome != "ACCEPT":
                problems.append(f"{phase}: receipt {path} judge outcome is {outcome!r}, not ACCEPT")

    if "P2" in heads and "P3" in heads:
        (p2, p2_path), (p3, p3_path) = heads["P2"], heads["P3"]
        if _is_full_sha(str(p2).strip().lower()) and _is_full_sha(str(p3).strip().lower()):
            verdict, out = _is_ancestor(git, p2, p3)
            if verdict is not True:
                problems.append(f"P2: receipt {p2_path} {RECEIPT_HEAD_FIELD} {p2} is not an "
                                f"ancestor-or-equal of P3's {p3} ({p3_path})" + (f": {out}" if out else ""))

    _check_round_verdict(round_dir, lane_tip, problems)
    if CI_PHASE in required:
        _check_ci_output(round_dir / f"{CI_PHASE}-OUTPUT.txt", lane_tip, problems)
    return problems


def cost_home_problem(root, home) -> str:
    """"" when writing under `home` cannot dirty the repository at `root`; else why not.
    A home outside the repository is fine; inside it, only `<root>/logs/receipts` (ignored) and below."""
    resolved_home, resolved_root = Path(home).resolve(), Path(root).resolve()
    try:
        resolved_home.relative_to(resolved_root)
    except ValueError:
        return ""
    ignored = resolved_root / "logs" / "receipts"
    if resolved_home == ignored or ignored in resolved_home.parents:
        return ""
    return (f"the receipts home {home} is inside the repository but not under logs/receipts: "
            f"writing {COST_NAME} there would dirty the worktree the landing requires clean")


# --- C24: the cost record ---------------------------------------------------------------------

def _head(command) -> str:
    name = PureWindowsPath(str(command[0])).name.lower() if command else ""   # both separators
    for ext in _EXTENSIONS:
        if name.endswith(ext):
            return name[: -len(ext)]
    return name


def _number(value) -> Optional[float]:
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _read_claude(round_dir: Path, phase: str) -> "tuple[list, str, str]":
    path = round_dir / f"{phase}-OUTPUT.txt"
    if not path.is_file():
        return [], path.name, f"{path.name} is absent"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return [], path.name, f"{path.name} is unreadable"
    if not text.strip():
        return [], path.name, f"{path.name} is empty"
    candidates = [text, *reversed([ln.strip() for ln in text.splitlines() if ln.strip().startswith("{")])]
    for candidate in candidates:
        try:
            obj = json.loads(candidate)
        except ValueError:
            continue
        cost = _number(obj.get("total_cost_usd")) if isinstance(obj, dict) else None
        if cost is not None:
            return [{"unit": "usd", "amount": cost}], path.name, ""
    return [], path.name, f"{path.name} holds no result envelope with total_cost_usd"


def _usage_arg(command) -> Optional[str]:
    found = None
    for i, token in enumerate(command):
        if token == "--usage-output-file" and i + 1 < len(command):
            found = command[i + 1]
        elif isinstance(token, str) and token.startswith("--usage-output-file="):
            found = token.split("=", 1)[1]
    return found


def _read_copilot(round_dir: Path, command, root: Path) -> "tuple[list, str, str]":
    arg = _usage_arg(command)
    if not arg:
        return [], "", "the recorded command names no --usage-output-file"
    usage = Path(arg)
    if not usage.is_absolute():
        usage = Path(root) / usage                  # the child's cwd is the repository root
    try:
        usage.resolve().relative_to(round_dir.resolve())
    except ValueError:
        return [], usage.name, "usage file outside the round directory"
    if not usage.is_file():
        return [], usage.name, f"usage file {usage.name} is absent"
    data = _read_json(usage)
    premium = _number(data.get("totalPremiumRequestCost")) if isinstance(data, dict) else None
    if premium is None:
        return [], usage.name, f"usage file {usage.name} lacks totalPremiumRequestCost"
    nano = _number(data.get("totalNanoAiu"))
    if nano is None:
        return [], usage.name, f"usage file {usage.name} lacks a numeric totalNanoAiu"
    return ([{"unit": "premium_requests", "amount": premium},
             {"unit": "aiu", "amount": nano / 1e9}], usage.name, "")


def _last_token_total(text: str) -> Optional[int]:
    """The number after the LAST `tokens used` (any case; `tokens used: 7,099` or the number on the
    next line), or None."""
    lowered, end = text.lower(), len(text)
    while True:
        at = lowered.rfind(_TOKENS_MARK, 0, end)
        if at < 0:
            return None
        rest = text[at + len(_TOKENS_MARK):].lstrip(": \t\r\n")
        digits = ""
        for char in rest:
            if char not in "0123456789,":
                break
            digits += char
        digits = digits.replace(",", "")
        if digits:
            return int(digits)
        end = at


def _read_codex(round_dir: Path, phase: str) -> "tuple[list, str, str]":
    path = round_dir / f"{phase}-OUTPUT.txt.stderr"
    if not path.is_file():
        return [], path.name, f"{path.name} is absent"
    try:
        total = _last_token_total(path.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return [], path.name, f"{path.name} is unreadable"
    if total is None:
        return [], path.name, f"{path.name} reports no `tokens used` total"
    return [{"unit": "tokens", "amount": total}], path.name, ""


def _measure(data: dict, phase: str, round_dir: Path, root: Path) -> "tuple[list, str, str]":
    command = data.get("command") or []
    head = _head(command)
    if head == "claude":
        return _read_claude(round_dir, phase)
    if head == "copilot":
        return _read_copilot(round_dir, command, root)
    if head == "codex":
        return _read_codex(round_dir, phase)
    return [], "", f"no cost reader for command head {head!r} (vendor {data.get('vendor')!r})"


def _row(round_no: int, phase: str, attempt: str, vendor, served, measurements: list, source: str,
         measured: bool, lower_bound: bool, reason: str) -> dict:
    return {"round": round_no, "phase": phase, "attempt": attempt, "vendor": vendor,
            "served_model": served, "measurements": measurements, "source": source,
            "measured": measured, "lower_bound": lower_bound, "reason": reason}


def cost_record(lane: str, receipts_dir, root=None) -> dict:
    """The `run-cost/1` record of every round of `lane`. Raises FileNotFoundError when the lane has
    no receipts directory. `root` is the repository root a relative usage path is resolved against."""
    if not _slug_ok(lane):
        raise ValueError(f"lane slug {lane!r} is not a valid slug")
    lane_dir = Path(receipts_dir) / f"LANE-{lane}"
    if not lane_dir.is_dir():
        raise FileNotFoundError(f"no receipts directory for lane {lane}: {lane_dir}")
    root = Path(root) if root is not None else Path.cwd()
    rows: list = []
    for round_no, round_dir in _round_dirs(lane_dir):
        files = sorted((p for p in round_dir.iterdir() if _is_receipt_file(p.name)),
                       key=lambda p: _phase_key(p.stem))
        for path in files:
            phase = path.stem
            data = _read_json(path)
            if not isinstance(data, dict):
                rows.append(_row(round_no, phase, "only", "unknown", None, [], "", False, False,
                                 f"receipt {path.name} is unreadable"))
                continue
            measurements, source, reason = _measure(data, phase, round_dir, root)
            measured = bool(measurements)
            partial = measured and data.get("status") in ("KILLED", "FAILED")
            origin = data.get("substituted_from")
            rows.append(_row(round_no, phase, "fallback" if origin else "only", data.get("vendor"),
                             data.get("served_model"), measurements,
                             f"r{round_no}/{source}" if source else "", measured, partial, reason))
            if origin:
                rows.append(_row(round_no, phase, "primary", origin, None, [], "", False, False,
                                 "overwritten by the fallback's spawn"))
    totals: dict = {}
    for row in rows:
        bucket = totals.setdefault(row["vendor"], {"unmeasured_attempts": 0})
        if not row["measured"]:
            bucket["unmeasured_attempts"] += 1
        for item in row["measurements"]:
            bucket[item["unit"]] = round(bucket.get(item["unit"], 0) + item["amount"], 9)
    return {"schema": COST_SCHEMA, "lane": lane, "rows": rows, "totals_by_provider": totals,
            "complete": all(row["measured"] for row in rows), "complete_means": COMPLETE_MEANS}


def render_cost(record: dict) -> str:
    return json.dumps(record, sort_keys=True, indent=2) + "\n"


def write_cost_record(lane: str, receipts_dir, root=None) -> Path:
    """Write `<receipts>/LANE-<lane>/RUN-COST.json` (LF newlines) and return its path."""
    lane_dir = Path(receipts_dir) / f"LANE-{lane}"
    try:
        lane_dir.resolve().relative_to(Path(receipts_dir).resolve())
    except ValueError:
        raise ValueError(f"{lane_dir} resolves outside the receipts home {receipts_dir}: "
                         f"{COST_NAME} is not written through a link") from None
    record = cost_record(lane, receipts_dir, root=root)
    target = lane_dir / COST_NAME
    scratch = target.with_name(COST_NAME + ".tmp")
    text = render_cost(record)
    with open(scratch, "x", encoding="utf-8", newline="\n") as out:   # FileExistsError: never over an old entry
        out.write(text)
    os.replace(scratch, target)
    return target


# --- the verbs --------------------------------------------------------------------------------

@click.group()
def cli() -> None:
    """Read a conductor round's phase receipts: the landing check and the run cost record."""


@cli.command("check")
@click.option("--lane", required=True, help="the lane slug")
@click.option("--tip", required=True, help="the full sha of the lane tip being landed")
@click.option("--receipts", "receipts", default=None, type=click.Path(path_type=Path),
              help="the receipts home (default: HARNESS_RECEIPTS_DIR, else <root>/logs/receipts)")
@click.option("--root", "root", default=".", type=click.Path(path_type=Path),
              help="the repository root (default: the current directory)")
def check_cmd(lane: str, tip: str, receipts: Optional[Path], root: Path) -> None:
    """Print each problem that stops the landing, one per line (exit 1), or OK (exit 0)."""
    problems = landing_problems(root, lane, tip, receipts_dir=receipts)
    if problems:
        for problem in problems:
            click.echo(problem)
        sys.exit(1)
    click.echo("OK")


@cli.command("cost")
@click.option("--lane", required=True, help="the lane slug")
@click.option("--receipts", "receipts", default=None, type=click.Path(path_type=Path),
              help="the receipts home (default: HARNESS_RECEIPTS_DIR, else <root>/logs/receipts)")
@click.option("--root", "root", default=".", type=click.Path(path_type=Path),
              help="the repository root a relative usage path is resolved against")
@click.option("--write", "write", is_flag=True, default=False,
              help=f"also write {COST_NAME} into the lane's receipts directory")
def cost_cmd(lane: str, receipts: Optional[Path], root: Path, write: bool) -> None:
    """Print the run's cost record: cost per provider and unit, every unmeasured phase named."""
    home = receipts or receipts_home(root)
    try:
        record = cost_record(lane, home, root=root)
    except (FileNotFoundError, ValueError) as exc:
        click.echo(f"round_receipts: {exc}", err=True)
        sys.exit(2)
    click.echo(render_cost(record), nl=False)
    if write:
        click.echo(f"wrote {write_cost_record(lane, home, root=root)}", err=True)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
