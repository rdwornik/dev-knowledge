"""The RED test for [#1350] (written by the lane, given to the cell). A Windows delete-pending lock
file makes `os.open(O_CREAT|O_EXCL)` raise PermissionError; the lock must read that as contention,
retry inside the same deadline, and not let it escape. Simulated by monkeypatching `os.open`."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import pytest

import transport


def test_a_delete_pending_permission_error_is_contention_not_an_escape(tmp_path, monkeypatch):
    real_open = os.open
    calls = {"n": 0}

    def flaky_open(path, flags, *a, **kw):
        if str(path).endswith(".append.lock") and calls["n"] < 3:
            calls["n"] += 1
            raise PermissionError(13, "delete pending")
        return real_open(path, flags, *a, **kw)

    monkeypatch.setattr(os, "open", flaky_open)
    monkeypatch.setattr(transport._DestinationLock, "_POLL_S", 0.001)
    with transport._DestinationLock(tmp_path / "SESSION-x.md", 5.0):
        pass
    assert calls["n"] == 3


def test_a_permission_error_that_never_clears_ends_at_the_deadline(tmp_path, monkeypatch):
    def always_denied(path, flags, *a, **kw):
        raise PermissionError(13, "delete pending")

    monkeypatch.setattr(os, "open", always_denied)
    monkeypatch.setattr(transport._DestinationLock, "_POLL_S", 0.001)
    with pytest.raises(transport.TransportWriteRefused):
        with transport._DestinationLock(tmp_path / "SESSION-x.md", 0.05):
            pass
