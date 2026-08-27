"""The green-by-skip sweep's standing guards (STANDING_RULINGS section U, 2026-08-25).

The swept rule: **a check that cannot compute its ground truth must FAIL, never report a
status the caller renders as green.**

Why `Finding.status == "unavailable"` counts as green here, since that is the whole crux:
`_STATUS_LABEL` renders it as "N/A" and `_check_outcome` projects it onto `pass`, and
`cmd_ship_gate` blocks only on `fail` plus undispositioned `warn`. So an "unavailable"
detector ships. `check_silent_rule_ratchet` already refused the word for exactly this
reason at terra HIGH 2026-07-27 --

    # FAIL, not "unavailable" (terra HIGH, 2026-07-27): ship-gate blocks only on `fail`
    # and undispositioned `warn`, so an "unavailable" detector would ship GREEN having
    # measured nothing at all.

-- and that call was never swept across the rest of the registry. This module holds the
sweep's two fixed instances plus the invariants that keep the class from regrowing.

The counter-rule matters as much: a check whose SUBJECT IS ABSENT is inapplicable, not
failed, and must keep its NOT-APPLICABLE. Over-applying fail-closed turns a consumer repo
green->red for a check that was never meant to run there, which is how a fail-closed fix
becomes a false gate. Both directions are asserted.
"""
from __future__ import annotations

import ast
import inspect
import textwrap
from pathlib import Path

import pytest

import audit as aud


# --- fixed instance 1: routine_consumers ------------------------------------

def test_unreadable_backlog_fails_routine_consumers(tmp_path, monkeypatch):
    """A backlog source EXISTS but cannot be read -> FAIL, not a green 'unavailable'.

    [#589] widened what "the source" means (the `tasks/` reassembly on the hub, the file on
    a consumer) and the evidence string moved with it; the invariant under test — an
    available ground truth that fails to compute is a FAIL, never an N/A that ship-gate
    projects onto `pass` — is unchanged.
    """
    (tmp_path / "BACKLOG.md").write_text("# backlog\n", encoding="utf-8")

    def boom(self, *args, **kwargs):
        raise OSError("permission denied")

    # `read_bytes`, not `read_text`, since [#589] — and the swap is the point, not bookkeeping.
    # `backlog_source.canonical_text` decodes strictly (`read_bytes().decode()`), so patching
    # `read_text` no longer intercepts anything: this test PASSED-as-green against an
    # unpatched read, which is the exact green-by-skip shape the file is named for. Patch what
    # the code under test actually calls.
    monkeypatch.setattr(Path, "read_bytes", boom)
    findings = aud.check_routine_consumers(tmp_path)
    assert findings[0].status == "fail"
    assert findings[0].status != "unavailable"          # the defect being closed
    assert "cannot read the backlog source" in findings[0].evidence


def test_absent_backlog_stays_not_applicable_for_routine_consumers(tmp_path):
    """The counter-rule: no BACKLOG.md at all is INAPPLICABLE, not a failed computation."""
    findings = aud.check_routine_consumers(tmp_path)
    assert findings[0].status != "fail"
    assert findings[0].status in {"n/a", "unavailable"}


# --- standing invariants over the whole registry ----------------------------

def _handlers(check):
    src = textwrap.dedent(inspect.getsource(check))
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.ExceptHandler):
            yield node


def _finding_statuses(node):
    for inner in ast.walk(node):
        if (isinstance(inner, ast.Call)
                and getattr(inner.func, "id", None) == "Finding"
                and len(inner.args) >= 2
                and isinstance(inner.args[1], ast.Constant)):
            yield inner.args[1].value


def test_no_registered_check_reports_pass_from_an_error_handler():
    """No ALL_CHECKS member may return `pass` from an exception handler.

    The sweep's invariant as a standing guard rather than a one-time reading, so it covers
    checks added after this lane: a handler that emits `pass` is by construction a check
    reporting success for a computation that raised.
    """
    offenders = [c.__name__ for c in aud.ALL_CHECKS
                 for h in _handlers(c) if "pass" in set(_finding_statuses(h))]
    assert not offenders, f"check(s) report `pass` from an except handler: {offenders}"


# DELIBERATELY NOT ADDED: a `len(ALL_CHECKS) == 46` tripwire for the sweep's coverage.
# Five such pins already exist (test_audit.py:2326, :2342; test_doc_code_edge.py:248, :715;
# test_writer_integrity.py:185) plus an order pin in test_audit_parallel.py, so adding a
# sixth would cost every future check another edit site while buying nothing the existing
# five do not already force. The substantive guard is behavioural, not numeric: the AST
# test above fails for ANY newly added check that reports `pass` from an error handler,
# with no roster to keep current.


@pytest.mark.live_repo
def test_the_two_swept_checks_are_green_on_the_live_repo():
    """The fail-closed change must not RED the live tree (contract risk (b)).

    A fail-closed fix that turns a healthy repo red is a worse defect than the skip it
    replaced, so this asserts the two changed checks still pass where they should.
    """
    root = Path(aud._REPO_ROOT)
    for check in (aud.check_routine_consumers, aud.check_fleet_audit_replication):
        findings = check(root)
        assert findings[0].status != "fail", (
            f"{check.__name__} FAILs on the live repo: {findings[0].evidence}")
