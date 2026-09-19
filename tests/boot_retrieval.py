"""Boot-base retrieval discipline -- does a session FETCH a pointer's target when the task arises?

LEG 1 (2026-09-19) itemised the always-loaded boot base and proposed replacing the
"retrievable" items with ~150 B pointers, and said in its own anti-claims that the whole saving
"assumes a pointer reliably gets the right item re-read ... which this session did not test".
This module is that test. It has two halves:

* DETERMINISTIC (imported by `test_boot_retrieval.py`, runs in the suite): the boot-base
  measurement, the transcript scorer, and the bindings that keep a conversion honest.
* LIVE (`py tests/boot_retrieval.py probe`, NOT in the suite -- it spends model tokens): drives a
  child `claude -p` over a scratch copy in two arms per item, BODY (today's CLAUDE.md) and POINTER
  (the converted one), and writes the result to `ecosystem/boot-retrieval-evidence.json`.

A conversion is admitted only where that evidence shows the pointer arm fetched a declared
target AND the body arm could answer at all (a probe the body arm fails measures nothing).

This lives under `tests/`, not `scripts/`, on purpose: it is a measurement instrument for a
one-off decision, and a new script would raise the mechanism count that the BUILD-LIST ratchet
forbids raising.

HONEST LIMITS -- read before quoting a number from here
-------------------------------------------------------
* The child is a small model (default Haiku) in a scratch directory holding a COPY of the boot
  files and the pointer targets, not the live repo. It answers "what would you do", it does not
  edit. A real seat is a different model with a live tree and a live task: a hit rate here is a
  lower-fidelity signal, not a guarantee.
* `fetched` means a Read/Grep/Glob/Bash tool call touched an accepted target. It does not mean the
  session UNDERSTOOD it; the canary check (a string only the target holds) is the answer-side half.
* n is three pointer runs and one body run per item. A miss is informative; 3 hits are not a rate.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOME_CLAUDE = Path.home() / ".claude"
EVIDENCE = REPO / "ecosystem" / "boot-retrieval-evidence.json"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
# The BODY arm is pinned to the last commit BEFORE the conversion, not to HEAD: at HEAD the file is
# already pointer-form and a re-run would compare pointer against pointer (Codex terra HIGH).
BODY_REV = "14d273fb"
_IMPORT = re.compile(r"(?m)^@(\S+)\s*$")


@dataclass(frozen=True)
class Item:
    """One retrievable boot item and the probe that tests a pointer to it."""

    id: str
    task: str            # task-shaped; must not name a target path or contain the canary
    targets: tuple[str, ...]  # repo-relative paths any of which counts as the right fetch
    canary: str          # a string only the target holds -- present in the answer iff it was read
    body_marker: str     # present in CLAUDE.md's import closure iff the item is still BODY-form
    pointer: str = ""    # the literal path CLAUDE.md's pointer form must carry (binds the run to the text)


ITEMS: tuple[Item, ...] = (
    Item(
        "hooks-roster",
        "A commit of mine was refused by the `graph-task-coverage` gate. What exactly does it "
        "check, and what is the correct way to get past it?",
        (".pre-commit-config.yaml",),
        "inbound `implements` edge",
        "`graph-task-coverage` — a staged file no OPEN row claims",
        ".pre-commit-config.yaml",
    ),
    Item(
        "repo-commands",
        "I need to run one command that checks the whole probe gate of a handoff bundle in a "
        "single pass. Which repo command is it and what does it emit?",
        (".claude/generated/commands-repo.md", ".claude/commands/handoff-verify.md"),
        "ONE evidence block",
        "`/handoff-verify` — Run the whole live probe gate",
        ".claude/generated/commands-repo.md",
    ),
    Item(
        "recent-adrs",
        "Which ADR most recently made a command file count as a wiring surface, and what is its "
        "status?",
        (".claude/generated/recent-adrs.md",),
        "adoption decays, it is not conferred",
        "ADR-119 (Accepted, 2026-09-13)",
        ".claude/generated/recent-adrs.md",
    ),
    Item(
        "methodology-roster",
        "I am deploying this hub's methodology to a consumer repo. Which pre-commit hooks does a "
        "fully-deployed consumer receive, per the deploy manifest?",
        (".claude/methodology-roster.md",),
        "floor-hash-verify",
        "floor-hash-verify — verifies",
        ".claude/methodology-roster.md",
    ),
    Item(
        "skills-roster",
        "A spec's version advanced and a dependent doc may now be stale. Is there a repo-level "
        "skill for reconciling the two? Name it and say what it does first.",
        (".claude/skills/check-against-spec/SKILL.md", ".claude/skills"),
        "site enumerator",
        "`check-against-spec` (spec-reconciliation site enumerator)",
        ".claude/skills/",
    ),
    Item(
        "architecture-pointer",
        "I am about to change how two organs relate. Where do I learn how each organ fails and "
        "what to read before a structural change?",
        ("ARCHITECTURE.md",),
        "failure posture",
        "Where to jump:** **Ch2** organ map",
        "ARCHITECTURE.md",
    ),
)

# No target: the task needs no pointer. Any fetch of an item target here is over-fetch.
CONTROL = "In README.md, fix a typo in the first sentence of the first paragraph -- describe the edit only."


def import_closure(claude_md: Path, _seen: set[Path] | None = None) -> list[Path]:
    """Files a Claude Code session loads because `claude_md` @-imports them, transitively."""
    seen = _seen if _seen is not None else set()
    out: list[Path] = []
    for rel in _IMPORT.findall(claude_md.read_text(encoding="utf-8")):
        path = (claude_md.parent / rel).resolve()
        if path.is_file() and path not in seen:
            seen.add(path)
            out.append(path)
            out.extend(import_closure(path, seen))
    return out


def _journal_head(journal: Path, entries: int = 5) -> int:
    """Bytes from the first `### ` entry heading up to the (entries+1)th -- CLAUDE.md s1's 'last 5'."""
    text = journal.read_bytes()
    starts = [m.start() for m in re.finditer(rb"(?m)^### ", text)]
    if not starts:
        return 0
    end = starts[entries] if len(starts) > entries else len(text)
    return end - starts[0]


def boot_base(repo: Path = REPO, home: Path = HOME_CLAUDE, memory: Path | None = None) -> dict[str, int]:
    """LEG 1's method: bytes on disk of everything a session loads before its first action.

    Keys are labels. `ARCHITECTURE.md` is reported under its own key but is NOT in
    `always_on`: it is a preload CANDIDATE (L6), measured separately by the caller.
    """
    sizes: dict[str, int] = {}
    for label, path in (
        ("global CLAUDE.md", home / "CLAUDE.md"),
        *((f"global rules/{p.name}", p) for p in sorted((home / "rules").glob("*.md"))),
        ("CLAUDE.md", repo / "CLAUDE.md"),
        *((f"import {p.relative_to(repo).as_posix()}", p) for p in import_closure(repo / "CLAUDE.md")),
        *((f"rules/{p.name}", p) for p in sorted((repo / ".claude" / "rules").glob("*.md"))),
        ("MEMORY.md", memory) if memory else ("MEMORY.md", Path()),
    ):
        if path.is_file():
            sizes[label] = path.stat().st_size
    if (repo / "JOURNAL.md").is_file():
        sizes["JOURNAL.md last 5"] = _journal_head(repo / "JOURNAL.md")
    sizes["always_on"] = sum(sizes.values())
    if (repo / "ARCHITECTURE.md").is_file():
        sizes["ARCHITECTURE.md (candidate, not in always_on)"] = (repo / "ARCHITECTURE.md").stat().st_size
    return sizes


def body_form(item: Item, claude_md: Path) -> bool:
    """True while the item's body is still inside CLAUDE.md or its @-import closure."""
    files = [claude_md, *import_closure(claude_md)]
    return any(item.body_marker in f.read_text(encoding="utf-8") for f in files)


def _events(stream: str) -> list[dict]:
    out = []
    for line in stream.splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def touched(stream: str, scratch: Path, targets: tuple[str, ...]) -> list[str]:
    """Targets a Read/Grep/Glob tool call actually pointed at, as `Tool:relative-path`.

    Prose that names a target does not count, and neither does a shell command's text: Bash is
    disallowed in the probe, and substring-matching a command would score `echo <target>` as a read.
    """
    want = {(scratch / t).resolve() for t in targets}
    hits: list[str] = []
    for ev in _events(stream):
        if ev.get("type") != "assistant":
            continue
        for block in ev.get("message", {}).get("content", []):
            if block.get("type") != "tool_use" or block.get("name") not in ("Read", "Grep", "Glob"):
                continue
            args = block.get("input", {})
            p = args.get("file_path") or args.get("path")
            if p and any(Path(p).resolve() == w or w in Path(p).resolve().parents for w in want):
                hits.append(f"{block['name']}:{Path(p).resolve().relative_to(scratch.resolve()).as_posix()}")
    return hits


def fetched(stream: str, scratch: Path, targets: tuple[str, ...]) -> bool:
    return bool(touched(stream, scratch, targets))


def answer(stream: str) -> str:
    for ev in reversed(_events(stream)):
        if ev.get("type") == "result":
            return ev.get("result") or ""
    return ""


def _claude() -> str:
    exe = shutil.which("claude")
    if not exe:
        raise SystemExit("claude CLI not on PATH")
    return exe


def build_scratch(claude_md_text: str, dest: Path, repo: Path = REPO) -> Path:
    """A scratch tree: the boot files (given CLAUDE.md variant) plus every pointer target."""
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "CLAUDE.md").write_text(claude_md_text, encoding="utf-8")
    for rel in ("AGENTS.md", "ARCHITECTURE.md", "README.md", ".pre-commit-config.yaml",
                "ecosystem/organ-index.md"):
        if (repo / rel).is_file():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo / rel, dest / rel)
    if (repo / ".claude").is_dir():
        shutil.copytree(repo / ".claude", dest / ".claude", dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("worktrees", "settings*.json", "hooks"))
    return dest


def run_probe(scratch: Path, task: str, model: str, max_turns: int = 8) -> str:
    """One child run. Prompt on STDIN, `--setting-sources local` (memory: child-claude-p-harness)."""
    prompt = (
        "You are working in this repository. Do NOT edit anything. Answer the task below by "
        "using the repo's own documentation where you need it, then state your answer.\n\n"
        f"TASK: {task}"
    )
    proc = subprocess.run(
        [_claude(), "-p", "--setting-sources", "local", "--model", model,
         "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns),
         "--allowedTools", "Read,Grep,Glob", "--disallowedTools", "Write,Edit,NotebookEdit,Bash,WebFetch,WebSearch",
         "--no-session-persistence"],
        input=prompt, capture_output=True, text=True, encoding="utf-8", cwd=scratch, timeout=300,
    )
    if not answer(proc.stdout):  # no result event: CLI/auth/model failure, not a miss
        raise RuntimeError(f"child claude produced no result (rc={proc.returncode}): {proc.stderr[:400]!r}")
    return proc.stdout


def _row(item: str, arm: str, run: int, out: str, scratch: Path, targets: tuple[str, ...], canary: str) -> dict:
    """One evidence row: the scorer's booleans AND what they were computed from (auditable)."""
    ans = answer(out)
    hits = touched(out, scratch, targets)
    at = ans.lower().find(canary.lower()) if canary else -1
    return {"item": item, "arm": arm, "run": run, "fetched": bool(hits), "touched": hits,
            "canary": at >= 0, "canary_witness": ans[max(0, at - 60): at + len(canary) + 60] if at >= 0 else "",
            "answer_sha256": hashlib.sha256(ans.encode("utf-8")).hexdigest()[:16], "answer_head": ans[:200]}


POINTER_RUNS = 3   # per item; the body arm runs once -- it only proves the probe is answerable
ADMIT_AT = 2       # pointer runs (of POINTER_RUNS) that must fetch AND answer


def probe(pointer_claude_md: Path, model: str = DEFAULT_MODEL, items: tuple[Item, ...] = ITEMS) -> dict:
    """Run every item in both arms plus the no-target control; return the evidence record."""
    body_src = subprocess.run(["git", "show", f"{BODY_REV}:CLAUDE.md"], cwd=REPO, capture_output=True,
                              text=True, encoding="utf-8", check=True).stdout
    arms = {"body": body_src, "pointer": pointer_claude_md.read_text(encoding="utf-8")}
    rows = []
    with tempfile.TemporaryDirectory(prefix="boot-retrieval-") as tmp:
        for arm, text in arms.items():
            scratch = build_scratch(text, Path(tmp) / arm)
            runs = POINTER_RUNS if arm == "pointer" else 1
            for it in items:
                for n in range(runs):
                    out = run_probe(scratch, it.task, model)
                    rows.append(_row(it.id, arm, n, out, scratch, it.targets, it.canary))
            every = tuple(t for it in items for t in it.targets)
            for n in range(runs):
                out = run_probe(scratch, CONTROL, model)
                rows.append(_row("control", arm, n, out, scratch, every, ""))
    return {"measured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "model": model,
            "body_rev": BODY_REV, "pointer_arm_sha256": hashlib.sha256(arms["pointer"].encode("utf-8")).hexdigest(),
            "pointer_runs": POINTER_RUNS, "admit_at": ADMIT_AT, "rows": rows}


def admitted(evidence: dict, item: Item) -> bool:
    """Admitted iff the body arm answered (probe valid) and >= ADMIT_AT DISTINCT pointer runs (of
    POINTER_RUNS) fetched a declared target AND answered with a witnessed canary.

    The thresholds are this module's constants, never read from the record: a record that says
    `admit_at: 0` or repeats one successful run must not admit anything (Codex terra HIGH).
    """
    rows = [r for r in evidence.get("rows", []) if r.get("item") == item.id]
    body = [r for r in rows if r["arm"] == "body"]
    if not (body and body[0]["canary"] and item.canary.lower() in body[0].get("canary_witness", "").lower()):
        return False
    hits = {r["run"] for r in rows if r["arm"] == "pointer" and r["run"] in range(POINTER_RUNS)
            and set(r["touched"]) and all(t.split(":", 1)[1].startswith(item.targets) for t in r["touched"])
            and r["canary"] and item.canary.lower() in r.get("canary_witness", "").lower()}
    return len(hits) >= ADMIT_AT


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "measure"
    if cmd == "measure":
        mem = next(iter(sorted((HOME_CLAUDE / "projects").glob("*Dev--dev-knowledge/memory/MEMORY.md"))), None)
        for label, n in boot_base(memory=mem).items():
            print(f"{n:>8,}  {label}")
        return 0
    if cmd == "probe":
        model = argv[2] if len(argv) > 2 else DEFAULT_MODEL
        record = probe(REPO / "CLAUDE.md", model)
        EVIDENCE.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
        for r in record["rows"]:
            print({k: v for k, v in r.items() if k != "answer_head"})
        return 0
    print("usage: boot_retrieval.py measure | probe [model]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
