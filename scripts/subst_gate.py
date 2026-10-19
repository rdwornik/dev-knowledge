#!/usr/bin/env python
"""subst_gate.py -- a silent model substitution becomes a refusal in code (P1, R139, S2, S4).

WHY IT EXISTS. e1-p0-fix ran Sonnet in the Grok and Copilot roles with passing probes and no notice
(R139). Nothing in code compared the model a contract names with the model the role table names, and
nothing at the merge gate asked what a lane was actually served or whether `dispatch.py` launched it.
This module is the three checks, composed from what the repo already has (library-first: the role
table is `ecosystem/provider-registry.yaml` read through `provider_registry.py`; the contract's head
row and Dispatch line are read by `dispatch.parse_contract_model_effort` / `parse_dispatch_block`;
the launch receipt is the one `dispatch._write_launch_records` writes):

  contract_problems      pre-launch (`moment:pre-launch`, organ `model_per_role`): the contract's
                         `| Model | Mode | Effort |` head row, its Dispatch `--model`, the model the
                         lane is actually launched with (HARNESS_MODEL) and every row of a
                         `| Phase | Model | Substrate |` table must name the model the registry's role
                         table names for that role. The lane head IS the implementer (R153: Sonnet
                         writes the code), so the head is judged against the `implement` role -- no
                         new role, no change to `orchestrate` (Opus-only, AX21-1).
  check_models_block     merge gate: a handback must carry a `MODELS:` block, and every phase line
                         with served != requested must carry a `VENDOR-FAIL: <ref>` (the substitution
                         is then printed, so it reaches the handback and the ledger).
  launch_receipt_problems merge gate (S4): a lane with no `dispatch.py` LAUNCH receipt is refused --
                         local: `logs/receipts/LAUNCH-<SLUG>.json` with `"organ": "launch"` and the
                         batch; Codespace: a `logs/CODESPACE-RECEIPTS.jsonl` row for the slug in the
                         batch. A raw `claude --bg`, the PATH `dispatch` wrapper and `dispatch.py
                         queue` leave neither, so they are refused BY CONSTRUCTION; nothing here tries
                         to detect them any other way.

APPLICABILITY. The gate applies to batches from E2.0 on (`batch_applies`), plus any contract that
carries a phase table. An older batch is reported "not applicable", never silently passed as checked.

Layer-2 contract (ADR-28/36): read-only. It reads files and compares strings; it starts nothing.

Run:  uv run --locked python scripts/subst_gate.py contract --lane <slug> --contract <path>
      uv run --locked python scripts/subst_gate.py handback --slug <slug> --batch <id> --handback <path>
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

import provider_registry as pr  # noqa: E402

#: The first batch the gate applies to: BATCH-E2-0 onward (history does not turn red).
FIRST_BATCH = (2, 0)
_BATCH_RE = re.compile(r"^E(\d+)\.(\d+)")

#: The head of a lane is the implementer (R153); the registry has no separate lane-head role.
HEAD_ROLE = "implement"

_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")      # dispatch.py's own slug grammar
_PHASE_HEAD = re.compile(r"^\|\s*Phase\s*\|\s*Model\s*\|\s*Substrate\s*\|\s*$", re.IGNORECASE)

#: Phase name -> (role, provider the row must name). First match wins; order matters ("write the RED /
#: isolated tests" must not fall into the verify rule, "review, Codex half" must not fall into implement).
_PHASE_RULES: tuple[tuple[re.Pattern, str, Optional[str]], ...] = (
    (re.compile(r"review.*copilot|copilot.*review"), "review", "copilot-enterprise"),
    (re.compile(r"review.*codex|codex.*review"), "review", "openai"),
    (re.compile(r"\bred\b|isolated tests?|write .*tests?"), "red", None),
    (re.compile(r"verify"), "verify", None),
    (re.compile(r"implement|orchestrat"), HEAD_ROLE, None),
    (re.compile(r"\bread\b"), "read", "anthropic"),
)


def batch_applies(batch: str) -> bool:
    """True for a batch id from E2.0 on (`E2.0`, `E2.1`, `E3.0`, ...); False for older ids and for none."""
    m = _BATCH_RE.match((batch or "").strip())
    return bool(m) and (int(m.group(1)), int(m.group(2))) >= FIRST_BATCH


# --- pre-launch: model per role ---------------------------------------------------------------------

def _refused(lane: str, role: str, contract_model: str, table_model: str, what: str) -> str:
    return (f"REFUSED [model-per-role]: lane {lane}, role {role}: {what} names {contract_model!r} "
            f"but the role table (ecosystem/provider-registry.yaml) names {table_model}")


def _entry_label(entry: dict) -> str:
    return entry.get("model") or "Copilot CLI (default model)"


def _phase_rows(text: str) -> list[tuple[str, str]]:
    """`(phase, model cell)` for each row of the contract's `| Phase | Model | Substrate |` table."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not _PHASE_HEAD.match(line.strip()):
            continue
        rows = []
        for ln in lines[i + 1:]:
            ln = ln.strip()
            if not ln.startswith("|"):
                break
            cells = [c.strip().strip("`") for c in ln.strip("|").split("|")]
            if len(cells) < 2 or set(ln) <= set("|-: "):
                continue
            rows.append((cells[0], cells[1]))
        return rows
    return []


def _role_entry(role: str, provider: Optional[str], registry_path) -> Optional[dict]:
    order = pr.role_order(role, registry_path)
    if provider is None:
        return order[0] if order else None
    return next((e for e in order if e.get("provider") == provider), None)


def _named_models(cell: str, known_models: list[str]) -> set[str]:
    """The registry model ids a cell names, matched on whole tokens (`claude-sonnet-5` is a registry
    id AND a prefix of `claude-sonnet-5-5`)."""
    low = cell.lower()
    return {m.lower() for m in known_models
            if re.search(r"(?<![\w.-])" + re.escape(m.lower()) + r"(?![\w.-])", low)}


def _cell_matches(cell: str, entry: dict, known_models: list[str]) -> bool:
    """A pinned entry: the cell names exactly that model. A provider-only entry (the Copilot CLI at its
    default): the cell names the provider and no registry model at all."""
    named = _named_models(cell, known_models)
    if entry.get("model"):
        return named == {entry["model"].lower()}
    alias = str(entry.get("provider", "")).split("-")[0].lower()
    return alias in cell.lower() and not named


def contract_problems(text: str, *, lane: str, batch: str = "", launch_model: str = "",
                      registry_path=None) -> tuple[list[str], list[str]]:
    """`(problems, notes)` for a lane contract. See the module docstring for what is judged."""
    rows = _phase_rows(text)
    if not batch_applies(batch) and not rows:
        return [], [f"model-per-role: not applicable (batch {batch or '-'} predates E2.0 and the "
                    f"contract carries no `| Phase | Model | Substrate |` table)"]
    import dispatch as d                              # lazy: the heavy import is paid only when judged
    problems: list[str] = []
    notes: list[str] = []
    head_entry = _role_entry(HEAD_ROLE, None, registry_path)
    if head_entry is None:
        return [f"REFUSED [model-per-role]: lane {lane}: the registry has no `{HEAD_ROLE}` role"], notes
    table_head = _entry_label(head_entry)
    try:
        head_model, _effort = d.parse_contract_model_effort(text)
    except d.DispatchRefused as exc:
        return [f"REFUSED [model-per-role]: lane {lane}, role {HEAD_ROLE}: the head row is unreadable "
                f"({exc}); the role table names {table_head}"], notes
    try:
        line = d.parse_dispatch_block(text)
    except d.DispatchRefused as exc:
        return [f"REFUSED [model-per-role]: lane {lane}, role {HEAD_ROLE}: the Dispatch line is "
                f"unreadable ({exc}); the role table names {table_head}"], notes
    dispatch_model = line.model if line else ""
    if dispatch_model and dispatch_model.lower() != head_model.lower():
        problems.append(f"REFUSED [model-per-role]: lane {lane}, role {HEAD_ROLE}: the head row names "
                        f"{head_model!r} but the Dispatch --model names {dispatch_model!r} (the role "
                        f"table names {table_head}); they must agree")
    for what, got in (("the head row", head_model), ("the Dispatch --model", dispatch_model),
                      ("the launch --model", launch_model)):
        if got and got.lower() != table_head.lower():
            problems.append(_refused(lane, HEAD_ROLE, got, table_head, what))
    if not rows:
        notes.append("model-per-role: no `| Phase | Model | Substrate |` table -- judged on the head "
                     "row and the Dispatch line only")
        return list(dict.fromkeys(problems)), notes
    known = pr.model_ids(registry_path)
    for phase, cell in rows:
        rule = next(((role, prov) for pat, role, prov in _PHASE_RULES if pat.search(phase.lower())), None)
        if rule is None:
            problems.append(f"REFUSED [model-per-role]: lane {lane}: phase {phase!r} maps to no registry "
                            f"role (known phases: implement/orchestrate, red tests, verify, review "
                            f"Copilot/Codex half, read) -- a row the gate cannot judge is a row that "
                            f"could carry a silent substitution (P1)")
            continue
        role, provider = rule
        entry = _role_entry(role, provider, registry_path)
        if entry is None:
            problems.append(f"REFUSED [model-per-role]: lane {lane}, role {role}: phase {phase!r} "
                            f"expects provider {provider}, which the role table does not list")
            continue
        if not _cell_matches(cell, entry, known):
            problems.append(_refused(lane, role, cell, _entry_label(entry), f"phase {phase!r}"))
    return list(dict.fromkeys(problems)), notes


# --- merge gate: the MODELS block -------------------------------------------------------------------

_VENDOR_FAIL = re.compile(r"\[?\s*VENDOR-FAIL:\s*([^\]\s][^\]]*?)\s*\]?\s*$")
_PHASE_LINE = re.compile(r"^\s+([^:\s][^:]*?)\s*:\s*(.*\S)\s*$")


def check_models_block(text: str) -> tuple[list[str], list[str]]:
    """`(problems, substitution_lines)` for the `MODELS:` block of a handback."""
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip() == "MODELS:"), None)
    if start is None:
        return ["REFUSED [models-block]: the handback carries no `MODELS:` block (BATCH-E2-0 section 3: "
                "`<phase>: requested=<model/effort> served=<model as the CLI reported it> "
                "[VENDOR-FAIL: <ref>]`)"], []
    problems: list[str] = []
    subs: list[str] = []
    seen = 0
    for ln in lines[start + 1:]:
        if not ln.strip():
            continue                                  # a blank line does not end the block
        m = _PHASE_LINE.match(ln)
        if m is None:
            break                                     # first un-indented line ends the block
        seen += 1
        phase, rest = m.group(1), m.group(2)
        if re.search(r"\bnot run\b", rest, re.IGNORECASE) and "requested=" not in rest:
            continue
        req = re.search(r"requested=(.+?)\s+served=", rest)
        srv = re.search(r"served=(.*)$", rest)
        if req is None or srv is None:
            problems.append(f"REFUSED [models-block]: phase {phase!r} is not `requested=... served=...` "
                            f"nor `NOT run`: {rest!r}")
            continue
        fail = _VENDOR_FAIL.search(srv.group(1))
        served = (srv.group(1)[:fail.start()] if fail else srv.group(1)).strip()
        requested = req.group(1).strip().split("/")[0].strip().lower()
        if requested.startswith("copilot") or served.lower() == requested:
            continue                                  # Copilot's served model is recorded, not compared
        if fail:
            subs.append(ln.strip())
        else:
            problems.append(f"REFUSED [models-block]: phase {phase!r} requested {req.group(1).strip()!r} "
                            f"but was served {served!r} and no `VENDOR-FAIL: <ref>` is on the line (P1: "
                            f"a silent substitution)")
    if not seen:
        problems.append("REFUSED [models-block]: the `MODELS:` block has no phase lines")
    return problems, subs


def _phase_text(value: object) -> str:
    """One phase of a dict-shaped JSON `models` value, rendered in the block's own grammar."""
    if not isinstance(value, dict):
        return str(value)
    text = f"requested={value.get('requested', '')} served={value.get('served', '')}"
    fail = value.get("vendor_fail") or value.get("VENDOR-FAIL")
    return f"{text} VENDOR-FAIL: {fail}" if fail else text


def read_handback_models(path) -> str:
    """The text holding the MODELS block: a JSON handback's `models`/`MODELS` value, else the raw text."""
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    try:
        data = json.loads(raw)
    except ValueError:
        return raw
    if isinstance(data, dict):
        for key in ("models", "MODELS"):
            value = data.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, list):
                lines = [str(v).rstrip() for v in value]
                if not any(ln.strip() == "MODELS:" for ln in lines):
                    lines = ["MODELS:"] + [ln if ln[:1].isspace() else "  " + ln for ln in lines]
                return "\n".join(lines)
            if isinstance(value, dict):
                return "MODELS:\n" + "\n".join(f"  {k}: {_phase_text(v)}" for k, v in value.items())
    return raw


# --- merge gate: the LAUNCH receipt (S4) ------------------------------------------------------------

def launch_receipt_problems(root, slug: str, batch: str, receipts_dir=None) -> list[str]:
    """Empty when the lane has a `dispatch.py` LAUNCH receipt for `batch`, local or Codespace."""
    if not _SLUG_RE.match(slug or ""):
        return [f"REFUSED [launch-receipt]: {slug!r} is not a lane slug (letters, digits, `.`, `_`, `-`) "
                f"-- it is never put into a receipt path"]
    root = Path(root)
    local = Path(receipts_dir) if receipts_dir else root / "logs" / "receipts"
    path = local / f"LAUNCH-{slug.upper()}.json"
    why = f"{path} does not exist"
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        body = None
    except (OSError, ValueError) as exc:
        body = None
        why = f"{path} is unreadable ({type(exc).__name__})"
    else:
        if isinstance(body, dict) and body.get("organ") == "launch" and body.get("batch") == batch:
            return []
        why = f"{path} is not a launch receipt for batch {batch} (organ={body.get('organ')!r}, " \
              f"batch={body.get('batch')!r})" if isinstance(body, dict) else f"{path} is not a JSON object"
    ledger = root / "logs" / "CODESPACE-RECEIPTS.jsonl"
    try:
        for row in ledger.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(row)
            except ValueError:
                continue
            if (isinstance(rec, dict) and rec.get("kind", "codespace") == "codespace"
                    and rec.get("slug") == slug and rec.get("batch") == batch):
                return []
        ledger_why = f"{ledger} has no row for slug {slug} in batch {batch}"
    except OSError:
        ledger_why = f"{ledger} does not exist"
    return [f"REFUSED [launch-receipt]: lane {slug} has no dispatch.py LAUNCH receipt for batch {batch} "
            f"-- local: {why}; Codespace: {ledger_why}. A raw `claude --bg`, the PATH `dispatch` wrapper "
            f"and `dispatch.py queue` leave none (S4)"]


def handback_problems(root, slug: str, batch: str, handback: Optional[Path],
                      receipts_dir=None) -> tuple[list[str], list[str]]:
    """The merge gate as `merge_path.land` runs it: `(problems, substitution_lines)`. Not applicable
    (`([], [])`) for a batch before E2.0."""
    if not batch_applies(batch):
        return [], []
    if handback is None or not Path(handback).is_file():
        problems = [f"REFUSED [models-block]: no handback file was given for lane {slug} "
                    f"(batch {batch}) -- the MODELS block cannot be read"]
        subs: list[str] = []
    else:
        problems, subs = check_models_block(read_handback_models(handback))
    problems = problems + launch_receipt_problems(root, slug, batch, receipts_dir)
    return problems, subs


# --- CLI --------------------------------------------------------------------------------------------

def _cmd_contract(args) -> int:
    text = Path(args.contract).read_text(encoding="utf-8", errors="replace")
    problems, notes = contract_problems(text, lane=args.lane, batch=os.environ.get("HARNESS_BATCH", ""),
                                        launch_model=os.environ.get("HARNESS_MODEL", ""))
    for line in problems:
        print(line)
    for note in notes:
        print(note)
    return 1 if problems else 0


def _cmd_handback(args) -> int:
    rdir = os.environ.get("HARNESS_RECEIPTS_DIR")
    problems, subs = handback_problems(args.root, args.slug, args.batch, Path(args.handback),
                                       receipts_dir=rdir)
    for line in problems:
        print(line)
    for line in subs:
        print(f"SUBSTITUTION (VENDOR-FAIL recorded): {line}")
    return 1 if problems else 0


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="verb", required=True)
    c = sub.add_parser("contract", help="the pre-launch organ: model per role")
    c.add_argument("--lane", required=True)
    c.add_argument("--contract", required=True)
    c.set_defaults(fn=_cmd_contract)
    h = sub.add_parser("handback", help="the merge gate's MODELS block + LAUNCH receipt checks")
    h.add_argument("--slug", required=True)
    h.add_argument("--batch", required=True)
    h.add_argument("--handback", required=True)
    h.add_argument("--root", default=str(_REPO_ROOT))
    h.set_defaults(fn=_cmd_handback)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except OSError as exc:
        print(f"ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
