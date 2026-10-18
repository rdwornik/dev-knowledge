"""The branch matrix every form must satisfy, with a stub service layer (no subprocess, runs in ms)."""
from __future__ import annotations

OK = {
    "schedule": {"ok": True}, "parse_contract": {"ok": True}, "validate": {"ok": True}, "tier": {"ok": True},
    "claim": {"ok": True}, "dependency": {"status": "READY"}, "serialize": {"clear": True},
    "substrate": {"substrate": "local"}, "cap_ram": {"action": "FIRE"}, "route_codespace": {"ok": True},
    "prelaunch": {"passed": True}, "held": {"held": ""}, "spawn": {"returncode": 0, "stdout": "backgrounded abc12345"},
    "identify": {"job_id": "abc12345", "session_id": "s", "name": "n"}, "receipt": {"written": []},
}

# (case id, service overrides, interrupt event after launch, expected terminal node)
CASES = [
    ("clean", {}, "lane_handback", "end_launched"),
    ("reaped", {}, "lane_reaped", "end_reaped"),
    ("end-early", {}, "lane_ended_early", "end_early"),
    ("parse-disagree", {"parse_contract": {"ok": False}}, None, "end_refused"),
    ("invalid", {"validate": {"ok": False}}, None, "end_refused"),
    ("claim-refused", {"claim": {"ok": False}}, None, "end_refused"),
    ("dep-waiting", {"dependency": {"status": "WAITING"}}, None, "end_hold"),
    ("dep-failed", {"dependency": {"status": "BLOCKED-FAILED"}}, None, "end_refused"),
    ("serialize-blocked", {"serialize": {"clear": False}}, None, "end_hold"),
    ("substrate-codespace", {"substrate": {"substrate": "codespace"}}, None, "end_routed_codespace"),
    ("substrate-cloud", {"substrate": {"substrate": "cloud"}}, None, "end_refused"),
    ("cap-full", {"cap_ram": {"action": "HOLD"}}, None, "end_hold"),
    ("prelaunch-refused", {"prelaunch": {"passed": False}}, None, "end_refused"),
    ("already-launched", {"held": {"held": "job abc is running"}}, None, "end_already_launched"),
    ("listing-unreadable", {"held": {"held": "", "unreadable": "x"}}, None, "end_refused"),
    ("spawn-fails", {"spawn": {"returncode": 1, "stdout": "boom"}}, None, "end_refused"),
    ("unresolved", {"identify": {"job_id": "", "session_id": "", "name": ""}}, None, "end_unresolved"),
]


class Stub:
    def __init__(self, overrides):
        self.table = {**OK, **overrides}

    def __getattr__(self, name):
        if name not in self.table:
            raise AttributeError(name)
        return lambda *a, **k: self.table[name]
