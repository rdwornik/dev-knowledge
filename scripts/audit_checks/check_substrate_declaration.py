"""`check_substrate_declaration` — the `[#591]` substrate validator as a registered gate.

The thin ADAPTER half of a two-site rule; the logic lives in `scripts/validate_substrate.py`.
Same module-import + thin-adapter shape as `check_adr_status_grammar` / `check_safe_removal`.

WHAT IT GATES. The committed lane-contract corpus: every `*.md` under a
`docs/audits/<date>-technical-<batch>-launch-contracts/` directory (the in-tree home ruled
2026-08-26, ADR-101 amendment 2026-08-26 (b)) plus any `docs/audits/**/LANE-*.md`. That corpus
exists precisely so a batch's launch inputs are committed evidence — which is what makes them
gateable at all. Contracts hand-authored off-repo stay invisible to every commit-time gate, and
this check does not pretend otherwise.

THE DATE CUTOFF IS A GRANDFATHER, NOT A SKIP, and the precedent is this corpus's own. The
`lane-contract-check` pre-commit hook already grandfathers the eleven batch-1 contracts on a
ruled basis — *"retro-fitting them would falsify what was actually dispatched"* (architect,
2026-08-21). The same reasoning binds here: a contract is a RECORD of a dispatch that already
happened, so editing one to satisfy a validator written afterwards would falsify the record.
Everything dated before `ARM_DATE` is therefore reported as grandfathered debt in the evidence
line rather than silently dropped — the count is visible on every run.

MEASURED BEFORE ARMING, which is why the REFUSE legs are armed at FAIL rather than WARN. On
the live corpus at arm time the five committed batch-1 contracts produce four refusals
(one `codespaces` near-miss for the ruled `codespace`, three declaring no substrate at all) and
ALL FOUR are pre-`ARM_DATE`. The post-cutoff corpus measures **0**, so arming cannot RED a
clean tree — the same evidence bar `check_adr_status_grammar` used to arm its `enum` and
`single-field` legs. Leg 4 (`substrate-second-local-writer`) is a WARN by the row's own words.

FAIL-CLOSED ON ITS OWN INPUTS, deliberately. An unreadable substrate registry, an undecodable
contract or an undatable one are reported as `fail`/`warn`, never as `pass` and never as
`unavailable`: a validator that cannot compute its ground truth and reports a status the
caller renders green is the exact class `[#583]`/`[#596]` sweep for, and `_STATUS_LABEL`
renders `unavailable` as "N/A".

HONEST LIMITS, the module's own and its logic module's:
  * It gates the COMMITTED corpus. A contract dispatched from the prompts dir and never copied
    in-tree is not checked by anything, here or elsewhere.
  * An undatable contract cannot be placed relative to the cutoff. It is WARNed by name rather
    than assumed old — assuming old is how a cutoff becomes an escape hatch.
  * Everything `validate_substrate`'s own docstring records: leg 2 is token-based, leg 3 matches
    path shapes, leg 4 sees only the contracts in one directory, and none of them says a
    contract asks for the RIGHT work.

Child-repo-safe: a repo with no `docs/audits/` yields `n/a` (subject-absent), not a FAIL.
Read-only (Layer 2): no git, no writes.
"""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

from ._common import Finding, _na, _NA_SUBJECT_ABSENT

try:
    from scripts import validate_substrate as _vsub
except ImportError:
    import validate_substrate as _vsub

CHECK_NAME = "substrate_declaration"
AUDITS_RELPATH = "docs/audits"

#: Contracts landed on or after this date are gated; earlier ones are grandfathered records
#: of an already-executed dispatch. The date this check armed.
ARM_DATE = _dt.date(2026, 8, 27)

#: The in-tree launch-contract home's directory-name shape (PLAYBOOK Ch8, "Where the contract
#: file lives"). The leading date is the contract's landing date.
_LAUNCH_DIR_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-.*-launch-contracts$")
#: A dated artifact filename, for a contract sitting directly under `docs/audits/`.
_DATED_NAME_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-")


def _contract_date(path: Path, audits_dir: Path) -> _dt.date | None:
    """The landing date of one contract, or None when nothing on the path carries one.

    Read from the launch-contracts directory name first (the ruled home names the batch's
    date), then from the file's own leading date. None is returned rather than a guess: the
    caller WARNs by name instead of silently placing the file on the safe side of the cutoff.
    """
    for parent in path.parents:
        if parent == audits_dir.parent:
            break
        match = _LAUNCH_DIR_RE.match(parent.name)
        if match:
            try:
                return _dt.date.fromisoformat(match.group("date"))
            except ValueError:
                return None
    match = _DATED_NAME_RE.match(path.name)
    if match:
        try:
            return _dt.date.fromisoformat(match.group("date"))
        except ValueError:
            return None
    return None


def _corpus(audits_dir: Path) -> list[Path]:
    """Every committed lane contract, deduplicated and ordered."""
    found: set[Path] = set()
    for directory in audits_dir.iterdir():
        if directory.is_dir() and _LAUNCH_DIR_RE.match(directory.name):
            found.update(p for p in directory.glob("*.md") if p.is_file())
    found.update(p for p in audits_dir.rglob("LANE-*.md") if p.is_file())
    return sorted(found)


def check_substrate_declaration(repo_path: Path) -> list[Finding]:
    """`[#591]` layer 2: a committed lane contract whose substrate contradicts its content.

    One Finding PER refusal, never a bundle. The `#147` disposition register suppresses an
    ENTIRE Finding on a substring match, so a bundled Finding would let one dispositioned
    contract wave through every other refusal beside it — the reason `git_backlog_drift` emits
    one per drifted id and `funnel_coverage` one per artifact.
    """
    audits_dir = Path(repo_path) / AUDITS_RELPATH
    if not audits_dir.is_dir():
        return [_na(CHECK_NAME, _NA_SUBJECT_ABSENT,
                    f"no {AUDITS_RELPATH}/ — this repo carries no committed lane contracts")]

    try:
        registry = _vsub.load_registry(Path(repo_path))
    except _vsub.SubstrateRegistryError as exc:
        # FAIL, not "unavailable": the ship-gate blocks only on `fail` plus undispositioned
        # `warn`, so an "unavailable" verdict here would ship a validator that measured
        # nothing (`check_silent_rule_ratchet`'s 2026-07-27 terra call, swept 2026-08-25).
        return [Finding(CHECK_NAME, "fail",
                        f"substrate registry unreadable, so no contract was validated: "
                        f"{exc}".replace("|", "/"))]

    try:
        paths = _corpus(audits_dir)
    except OSError as exc:
        return [Finding(CHECK_NAME, "fail",
                        f"could not enumerate {AUDITS_RELPATH}: {exc!r}".replace("|", "/"))]

    out: list[Finding] = []
    gated: dict[str, str] = {}
    grandfathered = 0
    for path in paths:
        rel = path.relative_to(repo_path).as_posix()
        landed = _contract_date(path, audits_dir)
        if landed is None:
            out.append(Finding(CHECK_NAME, "warn",
                               f"{rel} carries no resolvable landing date, so it cannot be "
                               f"placed against the {ARM_DATE.isoformat()} cutoff — it is "
                               f"reported rather than assumed grandfathered"))
            continue
        if landed < ARM_DATE:
            grandfathered += 1
            continue
        try:
            gated[rel] = path.read_text(encoding="utf-8")
        except OSError as exc:
            out.append(Finding(CHECK_NAME, "fail",
                               f"could not read {rel}: {exc!r}".replace("|", "/")))
        except UnicodeDecodeError as exc:
            out.append(Finding(CHECK_NAME, "fail",
                               f"{rel} is not valid UTF-8 ({exc}), so it was not "
                               f"validated".replace("|", "/")))

    for refusal in _vsub.validate_batch(gated, registry=registry):
        status = "fail" if refusal.severity == _vsub.SEVERITY_REFUSE else "warn"
        out.append(Finding(CHECK_NAME, status, refusal.render().replace("|", "/")))

    if not out:
        out.append(Finding(CHECK_NAME, "pass",
                           f"{len(gated)} lane contract(s) landed on/after "
                           f"{ARM_DATE.isoformat()} agree with their declared substrate "
                           f"({grandfathered} earlier contract(s) grandfathered as records "
                           f"of an already-executed dispatch)"))
    return out
