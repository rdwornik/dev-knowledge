"""Behavioural regression guard for scripts/billing_leak_sentinel.py -- the LANE-5B-5
lane-hooks-port Python port of scripts/billing_leak_sentinel.ps1.

Presence-only tripwire: warn once, ASCII, never echo the key value, always exit 0.

RED-FIRST (ADR-108 SS B): written and collected before scripts/billing_leak_sentinel.py
existed -- every test here failed with a collection ModuleNotFoundError.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "billing_leak_sentinel.py"


def _run(key):
    env = dict(os.environ)
    if key is None:
        env.pop("ANTHROPIC_API_KEY", None)
    else:
        env["ANTHROPIC_API_KEY"] = key
    return subprocess.run([sys.executable, str(_SCRIPT)], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env)


def test_no_key_is_silent():
    proc = _run(None)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == ""


def test_empty_key_is_silent():
    proc = _run("")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == ""


def test_whitespace_only_key_is_silent():
    proc = _run("   ")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == ""


def test_a_visible_key_warns_once_and_never_echoes_the_value():
    secret = "sk-ant-totally-secret-value-12345"
    proc = _run(secret)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.count("\n") == 1, proc.stdout
    assert proc.stdout.startswith("[billing] WARN:")
    assert secret not in proc.stdout
    assert "ANTHROPIC_API_KEY" in proc.stdout


def test_always_exits_0():
    for key in (None, "", "present"):
        assert _run(key).returncode == 0
