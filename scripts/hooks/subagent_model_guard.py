#!/usr/bin/env python
"""subagent_model_guard.py -- PreToolUse guard on the `Agent` tool (R177/R178, lane e2-model-routing).

A subagent runs only the registry's `read` model (haiku) or the `seat-orchestrator` model (Sonnet) for a
bounded probe. Opus, any other model, and an UNSET model (which would inherit the parent's tier) are
refused. The allowed ids are READ from `ecosystem/provider-registry.yaml`, plus the two bare aliases
`haiku` and `sonnet`; no model id is held in this file.

Protocol: the hook payload is JSON on stdin. To DENY print
`{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", ...}}` and exit 0;
to ALLOW print nothing. Fails CLOSED: a payload that cannot be parsed is denied, since a guard that
permits what it cannot check is declared enforcement without enforcement.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import provider_registry as pr  # noqa: E402

#: The bare Claude CLI aliases the Agent tool accepts for the two allowed tiers.
_ALIASES = ("haiku", "sonnet")
_GUARDED_TOOLS = frozenset({"Agent", "Task"})


def allowed_models() -> list[str]:
    """The registry `read` model, the `seat-orchestrator` model, and their bare aliases."""
    ids = [pr.anthropic_role_model("read"), pr.anthropic_role_model("seat-orchestrator")]
    return [*ids, *_ALIASES]


def decide(tool_input: dict, allowed: list[str]) -> tuple[str, str]:
    """`("allow"|"deny", reason)` for one Agent call's `tool_input`."""
    model = tool_input.get("model") if isinstance(tool_input, dict) else None
    allowed_low = {m.lower() for m in allowed}
    if isinstance(model, str) and model.strip().lower() in allowed_low:
        return "allow", ""
    shown = repr(model) if model else "unset"
    return "deny", (
        f"subagent model {shown} is not allowed: an Agent call must set `model` to one of "
        f"{sorted(allowed)} -- haiku (the registry `read` role) or sonnet (the `seat-orchestrator` "
        f"role); Opus and an unset model are refused (ecosystem/provider-registry.yaml, R177)")


def _deny(reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                              "permissionDecision": "deny",
                                              "permissionDecisionReason": reason}}))


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read())
        if not isinstance(payload, dict):
            raise ValueError("payload is not an object")
    except ValueError as exc:
        _deny(f"subagent_model_guard could not parse the hook payload ({exc}); refusing what it cannot "
              f"check (ecosystem/provider-registry.yaml: haiku or sonnet only)")
        return 0
    if payload.get("tool_name") not in _GUARDED_TOOLS:
        return 0
    try:
        allowed = allowed_models()
    except Exception as exc:  # noqa: BLE001 -- an unreadable registry must not open the guard
        _deny(f"subagent_model_guard could not read ecosystem/provider-registry.yaml ({exc}); refusing "
              f"what it cannot check (haiku or sonnet only)")
        return 0
    verdict, reason = decide(payload.get("tool_input") or {}, allowed)
    if verdict == "deny":
        _deny(reason)
    return 0


if __name__ == "__main__":
    sys.exit(main())
