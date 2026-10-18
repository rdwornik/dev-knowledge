#!/usr/bin/env python
"""probe.py -- the M1 model probe driver (lane-dz-0-m1-model-probe). Scratch, never merged.

  probe.py cell  <task> <label> <model> <effort|default>   run ONE cell in its own throwaway worktree
  probe.py copilot b                                       the Copilot CLI cell (task b)
  probe.py check <task> <clone>                            the deterministic check alone
  probe.py grade                                           blind-grade every raw output
  probe.py ledger                                          print the running USD sum

Every cell: a fresh `git worktree add --detach <tmp> <BASE_SHA>`; a headless `claude -p
--output-format json`; the raw JSON kept under raw/; the deterministic check run on the clone;
one row appended to ledger.jsonl with the running USD sum. Stops at BUDGET_USD.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE_SHA = (HERE / "BASE_SHA").read_text().strip()
BUDGET_USD = 8.0
LEDGER = HERE / "ledger.jsonl"
RAW = HERE / "raw"
TASKS = HERE / "tasks"
PYTEST = ["uv", "run", "--locked", "pytest", "-q", "-p", "no:cacheprovider", "-n0"]


def run(argv, cwd, timeout=900, env=None, stdin=None):
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env,
                          stdin=subprocess.DEVNULL if stdin is None else stdin)


def spent() -> float:
    if not LEDGER.exists():
        return 0.0
    return sum(json.loads(l).get("usd") or 0.0 for l in LEDGER.read_text().splitlines() if l.strip())


def make_clone(task: str, label: str) -> Path:
    clone = Path(tempfile.mkdtemp(prefix=f"m1-{label}-"))
    shutil.rmtree(clone)
    r = run(["git", "worktree", "add", "--detach", str(clone), BASE_SHA], REPO)
    if r.returncode:
        raise SystemExit(f"worktree add failed: {r.stderr}")
    if task == "c":                      # [#1350] is already fixed at the base sha: re-seed the pre-fix lock
        for argv in (["git", "apply", str(TASKS / "c_fix" / "seed.patch")],):
            r = run(argv, clone)
            if r.returncode:
                raise SystemExit(f"seed failed: {r.stderr}")
        shutil.copy(TASKS / "c_fix" / "RED_test.py", clone / "tests" / "test_transport_delete_pending.py")
        run(["git", "add", "-A"], clone)
        r = run(["git", "-c", "user.name=probe", "-c", "user.email=probe@x", "commit", "--no-verify", "-qm", "seed"], clone)
        if r.returncode:
            raise SystemExit(f"seed commit failed: {r.stderr}")
    return clone


def drop_clone(clone: Path) -> None:
    run(["git", "worktree", "remove", "--force", str(clone)], REPO)
    run(["git", "worktree", "prune"], REPO)


# --- deterministic checks -------------------------------------------------------------------------

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().strip("`").lower()


def check_a(clone: Path, result_text: str) -> dict:
    key = json.loads((TASKS / "a_read" / "key.json").read_text())
    m = re.search(r"\[.*\]", result_text, re.S)
    try:
        got = {int(o["q"]): o for o in json.loads(m.group(0))}
    except Exception as exc:
        return {"pass": False, "score": 0, "detail": f"unparseable final message: {exc}"}
    ok_answer = ok_cite = 0
    detail = []
    for it in key["items"]:
        o = got.get(it["q"])
        if not o:
            detail.append(f"Q{it['q']}: missing")
            continue
        if _norm(it["answer"]) in _norm(o.get("answer", "")):
            ok_answer += 1
        else:
            detail.append(f"Q{it['q']}: wrong answer {o.get('answer')!r}")
        try:
            lines = (clone / str(o["file"])).read_text(encoding="utf-8").split("\n")
            if _norm(o.get("quote", "")) and _norm(o["quote"]) in _norm(lines[int(o["line"]) - 1]):
                ok_cite += 1
            else:
                detail.append(f"Q{it['q']}: cited line {o.get('file')}:{o.get('line')} does not hold the quote")
        except Exception as exc:
            detail.append(f"Q{it['q']}: bad citation ({exc})")
    return {"pass": ok_answer == 6 and ok_cite == 6, "score": ok_answer, "answers_ok": ok_answer,
            "citations_ok": ok_cite, "detail": detail}


def _junit(clone: Path, target: str) -> tuple[int, list[dict]]:
    xml = clone / "junit.xml"
    r = run(PYTEST + [target, "--tb=short", f"--junitxml={xml}"], clone)
    cases = []
    if xml.exists():
        for tc in ET.parse(xml).getroot().iter("testcase"):
            f, e = tc.find("failure"), tc.find("error")
            cases.append({"name": tc.get("name"), "failure": (f.get("message") if f is not None else None),
                          "error": (e.get("message") if e is not None else None)})
    return r.returncode, cases


def check_b(clone: Path, _text: str) -> dict:
    test = clone / "tests" / "test_queue_already_launched.py"
    if not test.exists():
        return {"pass": False, "detail": "tests/test_queue_already_launched.py was not written"}
    other = [l for l in run(["git", "status", "--porcelain"], clone).stdout.splitlines()
             if "test_queue_already_launched.py" not in l and "junit.xml" not in l]
    rc, cases = _junit(clone, "tests/test_queue_already_launched.py")
    failed = [c for c in cases if c["failure"]]
    errored = [c for c in cases if c["error"]]
    asserting = [c for c in failed if re.match(r"\s*(AssertionError|assert\b)", c["failure"] or "")]
    red_ok = bool(failed) and not errored and len(asserting) == len(failed) and not other
    # non-vacuity: the reference fix must turn the same test green
    green_ok = False
    if red_ok:
        a = run(["git", "apply", str(TASKS / "b_red" / "REFERENCE_fix.patch")], clone)
        if a.returncode == 0:
            rc2, cases2 = _junit(clone, "tests/test_queue_already_launched.py")
            green_ok = rc2 == 0 and bool(cases2)
            run(["git", "checkout", "scripts/dispatch.py"], clone)
    return {"pass": red_ok and green_ok, "red_on_base_for_an_assertion": red_ok,
            "green_under_reference_fix": green_ok, "other_files_touched": other,
            "detail": [c["failure"] or c["error"] for c in cases if c["failure"] or c["error"]][:3]}


def check_c(clone: Path, _text: str) -> dict:
    names = run(["git", "diff", "--name-only", "HEAD"], clone).stdout.split()
    stat = run(["git", "diff", "--numstat", "HEAD", "--", "scripts/transport.py"], clone).stdout.split()
    changed = (int(stat[0]) + int(stat[1])) if len(stat) >= 2 and stat[0].isdigit() else 0
    only = names == ["scripts/transport.py"]
    rc1, c1 = _junit(clone, "tests/test_transport_delete_pending.py")
    rc2, c2 = _junit(clone, "tests/test_transport.py")
    ok = only and 0 < changed <= 15 and rc1 == 0 and rc2 == 0 and bool(c1) and bool(c2)
    return {"pass": ok, "only_transport_py": only, "changed_lines": changed,
            "new_test_green": rc1 == 0 and bool(c1), "existing_transport_tests_green": rc2 == 0 and bool(c2),
            "files": names}


def check_d(_clone: Path, result_text: str) -> dict:
    first = result_text.strip().splitlines()[0].strip().strip("`*") if result_text.strip() else ""
    verdict_ok = first.upper().startswith("REQUEST-CHANGES")
    named = bool(re.search(r"re\.search|\bsearch\b", result_text)) and \
        bool(re.search(r"re\.match|match|anchor|contain|relative|substring|anywhere", result_text, re.I))
    return {"pass": verdict_ok and named, "verdict": first[:30], "names_the_defect": named}


CHECKS = {"a": check_a, "b": check_b, "c": check_c, "d": check_d}


# --- one cell ---------------------------------------------------------------------------------------

def metrics(raw: dict) -> dict:
    mu = raw.get("modelUsage") or {}
    u = raw.get("usage") or {}
    return {"served_models": sorted(mu), "usd": raw.get("total_cost_usd"),
            "input_tokens": u.get("input_tokens"), "output_tokens": u.get("output_tokens"),
            "cache_read_tokens": u.get("cache_read_input_tokens"),
            "cache_creation_tokens": u.get("cache_creation_input_tokens"),
            "turns": raw.get("num_turns"), "is_error": raw.get("is_error")}


def record(row: dict) -> None:
    row["usd_running"] = round(spent() + (row.get("usd") or 0.0), 4)
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")
    print(json.dumps(row))


def cell(task: str, label: str, model: str, effort: str) -> int:
    if spent() >= BUDGET_USD:
        print(f"BUDGET: USD {spent():.2f} >= {BUDGET_USD}; not running {label}")
        return 3
    RAW.mkdir(exist_ok=True)
    prompt = (TASKS / {"a": "a_read", "b": "b_red", "c": "c_fix", "d": "d_verdict"}[task] / "prompt.md").read_text()
    clone = make_clone(task, label)
    argv = ["claude", "-p", "--output-format", "json", "--model", model]
    if effort != "default":
        argv += ["--effort", effort]
    argv += ["--permission-mode", "bypassPermissions", prompt]
    t0 = time.monotonic()
    try:
        r = run(argv, clone, timeout=1500)
        wall = round(time.monotonic() - t0, 1)
        (RAW / f"{label}.stdout.json").write_text(r.stdout, encoding="utf-8")
        (RAW / f"{label}.stderr.txt").write_text(r.stderr, encoding="utf-8")
        try:
            raw = json.loads(r.stdout)
        except Exception:
            raw = {"is_error": True, "result": r.stdout[:500]}
        text = raw.get("result") or ""
        chk = CHECKS[task](clone, text)
        if task in "bc":
            (RAW / f"{label}.diff").write_text(run(["git", "diff", "HEAD"], clone).stdout
                                               + "\n--- untracked ---\n"
                                               + run(["git", "status", "--porcelain"], clone).stdout, encoding="utf-8")
        row = {"label": label, "task": task, "model_requested": model, "effort": effort, "exit": r.returncode,
               "wall_s": wall, "check": chk, **metrics(raw)}
        record(row)
        return 0
    finally:
        drop_clone(clone)


def copilot(task: str = "b") -> int:
    RAW.mkdir(exist_ok=True)
    prompt = (TASKS / "b_red" / "prompt.md").read_text()
    clone = make_clone("b", "copilot-b")
    t0 = time.monotonic()
    try:
        try:
            r = run(["copilot", "-p", prompt, "--allow-all-tools"], clone, timeout=1500)
        except FileNotFoundError as exc:
            record({"label": "copilot-b", "task": "b", "vendor": "copilot", "usd": None,
                    "vendor_fail": f"VENDOR-FAIL: {exc}"})
            return 0
        wall = round(time.monotonic() - t0, 1)
        (RAW / "copilot-b.stdout.txt").write_text(r.stdout, encoding="utf-8")
        (RAW / "copilot-b.stderr.txt").write_text(r.stderr, encoding="utf-8")
        if r.returncode != 0:
            record({"label": "copilot-b", "task": "b", "vendor": "copilot", "usd": None, "wall_s": wall,
                    "vendor_fail": f"VENDOR-FAIL: exit {r.returncode}: {(r.stderr or r.stdout).strip()[:600]}"})
            return 0
        chk = check_b(clone, r.stdout)
        (RAW / "copilot-b.diff").write_text(run(["git", "status", "--porcelain"], clone).stdout, encoding="utf-8")
        record({"label": "copilot-b", "task": "b", "vendor": "copilot", "usd": None, "wall_s": wall,
                "usd_note": "UNVERIFIED: the Copilot CLI reports premium requests, not USD", "check": chk})
        return 0
    finally:
        drop_clone(clone)


# --- blind grading ----------------------------------------------------------------------------------

def grade() -> int:
    rows = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    rows = [r for r in rows if "check" in r]
    letters = "ABCDEFGHIJKLM"
    mapping = {letters[i]: r["label"] for i, r in enumerate(rows)}
    (HERE / "blind").mkdir(exist_ok=True)
    (HERE / "blind" / "MAPPING.json").write_text(json.dumps(mapping, indent=1))   # the grader never sees this
    results = {}
    for task in "abcd":
        mine = [(k, v) for k, v in mapping.items() if v.split("-")[0] == task or (task == "b" and v == "copilot-b")]
        if not mine:
            continue
        tdir = {"a": "a_read", "b": "b_red", "c": "c_fix", "d": "d_verdict"}[task]
        gdir = Path(tempfile.mkdtemp(prefix="m1-grader-"))
        body = [f"# TASK\n{(TASKS / tdir / 'prompt.md').read_text()}\n",
                "# KEY (ground truth)\n" + "\n".join((TASKS / tdir / n).read_text() for n in
                                                     ("key.json", "REFERENCE_test.py") if (TASKS / tdir / n).exists()) + "\n"]
        for opaque, label in mine:
            lr = next(r for r in rows if r["label"] == label)
            out = (RAW / f"{label}.stdout.json")
            text = json.loads(out.read_text()).get("result", "") if out.exists() and out.suffix == ".json" and label != "copilot-b" \
                else (RAW / f"{label}.stdout.txt").read_text()
            diff = (RAW / f"{label}.diff").read_text() if (RAW / f"{label}.diff").exists() else ""
            body.append(f"# OUTPUT {opaque}\n## final message\n{text}\n## repo changes\n{diff}\n"
                        f"## deterministic check\n{json.dumps(lr['check'])}\n")
        body.append("Score each OUTPUT 0-3 (0 wrong/unusable, 1 partly right, 2 right with a flaw, 3 fully right) against the "
                    "TASK and KEY. The deterministic check result is evidence, not a verdict. Final message: ONLY a JSON object "
                    '{"A": {"score": 2, "reason": "one line"}, ...} keyed by the opaque ids above.')
        r = run(["claude", "-p", "--output-format", "json", "--model", "claude-sonnet-5-5", "--effort", "high",
                 "--permission-mode", "bypassPermissions", "\n".join(body)], gdir, timeout=900)
        raw = json.loads(r.stdout)
        record({"label": f"grader-{task}", "task": task, "grader": True, **metrics(raw), "wall_s": None})
        m = re.search(r"\{.*\}", raw.get("result", ""), re.S)
        results[task] = json.loads(m.group(0)) if m else {"error": raw.get("result", "")[:300]}
        shutil.rmtree(gdir, ignore_errors=True)
    joined = {}
    for opaque, label in mapping.items():
        for t in results.values():
            if opaque in t:
                joined[label] = t[opaque]
    (HERE / "blind" / "GRADES.json").write_text(json.dumps({"by_opaque_id": results, "joined_after_grading": joined}, indent=1))
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "cell":
        sys.exit(cell(*sys.argv[2:6]))
    if cmd == "copilot":
        sys.exit(copilot())
    if cmd == "check":
        print(json.dumps(CHECKS[sys.argv[2]](Path(sys.argv[3]), sys.stdin.read() if not sys.stdin.isatty() else ""), indent=1))
    elif cmd == "grade":
        sys.exit(grade())
    elif cmd == "ledger":
        print(f"USD {spent():.4f} of {BUDGET_USD}")
