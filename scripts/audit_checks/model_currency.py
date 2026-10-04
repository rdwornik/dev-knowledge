"""`check_model_currency` -- the R61 model-currency organ as a registered `audit.py health` finding.

Thin ADAPTER half; the logic lives in `scripts/check_model_currency.py`, which is also the CLI.
Same module-import + thin-adapter shape as `check_routing_agreement` and `check_dispatch_drift`,
reused rather than reinvented.

WARN TIER, BY THE LANE CONTRACT'S OWN WORDS: it informs and blocks nothing. Two consequences are
stated here because they are easy to read the other way round:

* The verdict is `pass` or `warn`, never `fail`. An unreadable registry is a `warn` too -- the
  registry's own validity is held by `check_provider_registry` and the loader, and a second
  organ turning that into a commit-blocking FAIL would be a new gate by another name.
* It runs at the COMMIT tier so the finding shows in `audit.py health`. `audit.py ship-gate` runs
  every tier and reads a `warn` that no disposition covers as RED, so a standing `warn` there is
  a decision for the operator, not for this check -- the lane handback names it.

What the finding covers is the repository's own surface: the registry, `templates/` and the
tracked `LANE-*.md` files. Live contracts live on the operator's transport, outside the
repository, so they reach the check only by path (`check_model_currency.py --contracts ...`).

Child-repo-safe: a repo with no `ecosystem/provider-registry.yaml` yields `n/a` (subject absent),
not a warning. Read-only (Layer 2): file reads and one `git ls-files`, no writes.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding, _na, _NA_SUBJECT_ABSENT

try:
    from scripts import check_model_currency as _cmc
except ImportError:  # pragma: no cover - the scripts/-on-sys.path entrypoint
    import check_model_currency as _cmc

CHECK_NAME = "model_currency"

#: How many ids of one kind the one-line evidence names before it says "+N more".
_SHOWN = 4

_KIND_ORDER = ("unknown-id", "stale", "unverified", "evidence-missing")


def _evidence(report) -> str:
    ids = {p.model_id for p in report.pins if p.kind == "id"}
    parts = []
    for kind in _KIND_ORDER:
        names = sorted({f.model_id for f in report.flags if f.kind == kind})
        if not names:
            continue
        shown = ", ".join(names[:_SHOWN])
        more = f" +{len(names) - _SHOWN} more" if len(names) > _SHOWN else ""
        parts.append(f"{kind} x{len(names)}: {shown}{more}")
    return (f"{len(report.flags)} flag(s) over {len(ids)} pinned ids -- " + "; ".join(parts)
            + " (list: uv run --locked python scripts/check_model_currency.py)")


def check_model_currency(repo_path: Path) -> list[Finding]:
    """R61: every pinned model id is in the registry, and each row was verified within 14 days."""
    root = Path(repo_path)
    if not (root / _cmc.REGISTRY_REL).is_file():
        return [_na(CHECK_NAME, _NA_SUBJECT_ABSENT,
                    f"no {_cmc.REGISTRY_REL} -- this repo carries no provider registry")]
    try:
        report = _cmc.analyse(root)
    except _cmc.CurrencyError as exc:
        return [Finding(CHECK_NAME, "warn",
                        f"the model-currency scan could not run: {exc}".replace("|", "/"))]
    if report.flags:
        return [Finding(CHECK_NAME, "warn", _evidence(report).replace("|", "/"))]
    ids = {p.model_id for p in report.pins if p.kind == "id"}
    return [Finding(CHECK_NAME, "pass",
                    f"{len(ids)} pinned ids, all in the registry, every row verified within "
                    f"{_cmc.MAX_AGE_DAYS} days")]
