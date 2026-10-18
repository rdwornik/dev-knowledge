"""Runs in the HUB's locked env: `uv run --locked python scratch/b-vs-c-spike/common/probe.py <cmd> '<json>'`.

The spike's one seam onto the pure decision functions of `scripts/dispatch.py` that have NO CLI
dry-run surface (`dependency_status`, `serialize_group_clear`, `decide_lane`, `_held_by`,
`_identify`, `_write_launch_records`, `launch_lane`). Nothing here starts a process: the spawn
seam is replaced by a recorder (the same seam `tests/test_dispatch_launch.py` replaces), the job
listing is a literal list, and every receipt goes to a throwaway HARNESS_RECEIPTS_DIR.

Prints exactly one JSON object on the last stdout line.
"""
from __future__ import annotations

import atexit
import dataclasses
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

from scripts import dispatch as d  # noqa: E402

_TMP = tempfile.mkdtemp(prefix="b-vs-c-receipts-")
os.environ["HARNESS_RECEIPTS_DIR"] = _TMP
atexit.register(shutil.rmtree, _TMP, True)   # no leftovers


def _lanes(contracts):
    return d.load_queue([Path(c) for c in contracts])


def _lane(contracts, slug):
    return next(lane for lane in _lanes(contracts) if lane.slug == slug)


def _request(contract):
    return d.request_from_contract(Path(contract))


def cmd_dep(p):
    return {"status": d.dependency_status(_lane(p["contracts"], p["slug"]), p.get("states") or {})}


def cmd_serial(p):
    lanes = _lanes(p["contracts"])
    lane = next(x for x in lanes if x.slug == p["slug"])
    return {"clear": d.serialize_group_clear(lane, lanes, p.get("live") or [])}


def cmd_substrate(p):
    text = Path(p["contract"]).read_text(encoding="utf-8")
    return {"substrate": d.lane_substrate(text)}


def cmd_capram(p):
    # decide_lane has the cap and the RAM floor INLINE (dispatch.py:1661,1664), not as functions:
    # neutralise the earlier gates (no dependency, no group, local) so only they can answer.
    lane = dataclasses.replace(_lane(p["contracts"], p["slug"]), starts_after=(), serialize_group=None,
                               substrate="local")
    free = p.get("free_mb")
    if free is None:
        free = d.mag.free_memory_mb()
    dec = d.decide_lane(lane, states={}, live_slugs=[], all_lanes=[lane], local_cap=p["cap"],
                        local_live_count=p["live_count"], free_mb=free, floor_mb=p["floor_mb"])
    return {"action": dec.action, "reason": dec.reason, "free_mb": round(free)}


def cmd_held(p):
    slug = p["slug"]
    if p.get("receipt"):
        d._write_json(d._receipt_path(slug), p["receipt"])
    try:
        held = d._held_by(slug, d.read_launch_receipt(slug), lambda: p.get("agents") or [])
    except d.ListingUnreadable as exc:
        return {"held": "", "unreadable": str(exc)}
    return {"held": held}


def _fake_listing(slug, job="abc12345"):
    return [{"id": job, "sessionId": job + "-0000-4000-8000-000000000000", "name": slug,
             "state": "running", "cwd": f"/box/.claude/worktrees/{slug}", "startedAt": int(time.time() * 1000)}]


def cmd_spawn(p):
    request = _request(p["contract"])
    rc = p.get("returncode", 0)
    # the recorder: what spawn_process would have been handed. NOTHING is executed.
    out = "" if p.get("empty_listing") else ("backgrounded abc12345 " + request.slug if rc == 0 else "boom")
    return {"argv": request.argv, "returncode": rc, "stdout": out}


def cmd_identify(p):
    request = _request(p["contract"])
    started = d.Spawned(0, p["stdout"], None)
    listing = [] if p.get("empty_listing") else _fake_listing(request.slug)
    job, session, name = d._identify(request, started, "", lambda: listing,
                                     lambda s: None, time.time())
    return {"job_id": job, "session_id": session, "name": name}


def cmd_receipt(p):
    request = _request(p["contract"])
    result = d.LaunchResult(slug=request.slug, provider=request.provider, model_requested=request.model,
                            model_reported=d.MODEL_PENDING, job_id=p["job_id"], worktree="(recorded)",
                            session_name=request.session_name, session_name_reported=p.get("name", ""),
                            session_id=p.get("session_id", ""), argv=list(request.argv))
    d._write_launch_records(request, result)
    return {"written": sorted(x.name for x in Path(_TMP).glob("LAUNCH-*"))}


def cmd_oracle(p):
    """The REAL `launch_lane` with the process boundary faked: the outcome the model must agree with."""
    request = _request(p["contract"])
    if p.get("receipt"):
        d._write_json(d._receipt_path(request.slug), p["receipt"])
    spawned = []

    rc = p.get("spawn_returncode", 0)
    blank = p.get("empty_listing")

    def spawn(argv, env, cwd):
        spawned.append(list(argv))
        return d.Spawned(rc, "" if blank else ("backgrounded abc12345" if rc == 0 else "boom"), None)

    def agents():   # before the spawn: what the scenario says is live; after it: the new job
        return (([] if blank else _fake_listing(request.slug)) if spawned else (p.get("agents") or []))

    verdict = d.PreLaunch(**p["prelaunch"])
    try:
        out = d.launch_lane(request, prelaunch=lambda r: verdict, spawn=spawn,
                            agents=agents,
                            cwd=Path(_TMP), secrets_file=None, sleep=lambda s: None)
    except d.LaunchIncomplete as exc:
        return {"outcome": "unresolved", "exit": exc.exit_code, "message": exc.message[:160], "spawned": len(spawned)}
    except d.LaunchRefused as exc:
        kind = "already-launched" if "is already launched" in exc.message else "refused"
        return {"outcome": kind, "exit": exc.exit_code, "message": exc.message[:160], "spawned": len(spawned)}
    return {"outcome": "launched", "exit": 0, "job_id": out.job_id, "spawned": len(spawned)}


COMMANDS = {k[4:]: v for k, v in globals().items() if k.startswith("cmd_")}

if __name__ == "__main__":
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    print(json.dumps(COMMANDS[sys.argv[1]](payload)))
