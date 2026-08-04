#!/usr/bin/env python
"""preflight_contract.py — verify the repo locators a contract or prompt cites, before acting.

THE DEFECT THIS ANSWERS (lesson 8). Nine architect premise errors landed in the 2026-08-03/04
window, every one caught downstream by accident — three arcs in, by a human re-deriving a number
that a machine could have checked in a second. Four were pure LOCATOR claims:

    "len(ALL_CHECKS) stays 38"                          live 39
    "ALL_CHECKS registered at scripts/audit.py:3381"    live 3429
    leg-4 contract AC-2's "38 -> 37" arithmetic         live 39 -> 38
    "five consumer dailies for 2026-08-02"              tree tops out at 2026-07-31

The cost of these is not that they were wrong — a frozen contract is allowed to be wrong, and
the ex-ante rule says report the discrepancy rather than edit it. The cost is WHEN they were
found. This runs first and reports every citation a contract makes about this repo.

WHAT IT CHECKS (mechanically decidable claims only):
    file-line    `path/to/file.py:123`   the file exists AND has >= 123 lines
    heading      `FILE.md` heading "..."  the heading text occurs in that file
    sha          `abc1234`                reachable in this repo's history
    backlog-id   `[#123]`                 currently OPEN in BACKLOG.md

WHAT IT CANNOT CHECK, stated so nobody reads more into a PASS than it carries: whether a
citation points at the RIGHT line (`:3381` and `:3429` are both real lines in a 3800-line file);
whether a claim's reasoning holds; whether a contract contradicts itself (two of this window's
nine were an internal contradiction and an unmet precondition, neither a locator). A PASS here
means "every locator resolves", never "the contract is correct".

POSTURE
    exit 0  every extracted claim resolved
    exit 1  at least one claim did not — each named with the LIVE value
    exit 2  internal error / the contract could not be read -- FAIL CLOSED. Modelled on
            `check_seal_identity`: an error is never a silent pass, and 2 is distinct from 1 so
            "I could not look" stays distinguishable from "I looked and it is wrong".

ADOPTION FIRST: this is wired into NO gate. Whether it should become one is a separate ruling
(its BACKLOG row carries the question). Layer-2 read-only (ADR-28/36) — it reads and writes
nothing.

Usage:
    python scripts/preflight_contract.py docs/audits/<contract>.md
    python scripts/preflight_contract.py <contract> --repo-root /path/to/repo
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent

# The claim vocabulary, in ONE place. Tests derive the set from here rather than restating it,
# so a class added without a fixture is visible instead of silently uncovered.
CLAIM_KINDS = ("file-line", "heading", "sha", "backlog-id")

# Deliberately conservative. A verifier that extracts nothing PASSES everything — this window's
# defining failure mode — but one that extracts too much buries the reader in false failures and
# gets ignored, which is the same outcome arriving more slowly. So every pattern requires a
# syntactic marker a human put there on purpose: backticks, or the `[#id]` bracket form.
#
# `path:line` must look like a repo path (a slash or a known suffix) so `3:1` ratios and `14:30`
# times are not locators.
# The optional `[A-Za-z]:` head keeps a Windows ABSOLUTE locator extractable. Without it,
# `C:\repo\scripts\audit.py:12` was silently skipped, so a contract carrying only such a locator
# reported a clean 0/0 — and a verifier that extracts nothing passes everything, which is this
# window's defining failure mode (terra HIGH, 2026-08-04).
_FILE_LINE_RE = re.compile(r"`((?:[A-Za-z]:)?[A-Za-z0-9_./\\ -]+\.[A-Za-z0-9]{1,6}):(\d+)`")
# A bare 7-40 hex string in backticks. Version strings like `1.2.3` have dots; prose "deadbeef"
# has no backticks. Pure-digit runs are excluded -- they are far more often counts than SHAs.
_SHA_RE = re.compile(r"`([0-9a-f]{7,40})`")
_BACKLOG_RE = re.compile(r"\[#(\d+)\]")
_HEADING_RE = re.compile(r"`([A-Za-z0-9_./\\-]+\.md)`\s+heading\s+[\"“]([^\"”]+)[\"”]")


@dataclass(frozen=True)
class Claim:
    kind: str
    raw: str
    detail: str = ""
    ok: bool = True


@dataclass
class Report:
    checked: list[Claim] = field(default_factory=list)

    @property
    def failed(self) -> list[Claim]:
        return [c for c in self.checked if not c.ok]

    def render(self) -> str:
        lines = []
        for c in self.checked:
            lines.append(f"  {'PASS' if c.ok else 'FAIL'}  [{c.kind}] {c.raw}"
                         + (f" -- {c.detail}" if c.detail else ""))
        n, bad = len(self.checked), len(self.failed)
        lines.append(f"preflight_contract: {n - bad}/{n} locator claim(s) resolved"
                     + (f"; {bad} FAILED" if bad else ""))
        return "\n".join(lines)


class PreflightError(RuntimeError):
    """The contract itself could not be read or scanned -- exit 2, never a silent pass."""


# This repo habitually cites a script by bare filename -- `normalize_headers.py:32` means
# `scripts/normalize_headers.py:32`. Resolving only against the repo root produced SIX false
# FAILs on the very first real artifact this tool was pointed at (the L-D dossier), and a
# verifier that cries wolf gets ignored just as surely as one that never fires. So a bare name
# is tried against the source roots before it is called missing.
_SOURCE_ROOTS = ("", "scripts", "deploy", "tests", "protocols", "docs")


def _resolve(repo_root: Path, rel: str) -> tuple[Path | None, str]:
    """Resolve `rel`, returning (path, note). An AMBIGUOUS bare name resolves to nothing.

    A path given relative to the repo root wins outright. A BARE name is searched across the
    source roots, and if more than one root holds it the claim is UNRESOLVED and says so
    (terra HIGH, 2026-08-04): first-match-wins would have verified `README.md:1` against
    `protocols/README.md` while the contract meant some other one, so a stale locator could
    pass by pointing at a file it never named. An ambiguous citation is a defect in the
    citation; the fix is to qualify it, not to guess.
    """
    direct = repo_root / rel
    if direct.is_file():
        return direct, ""
    hits = [repo_root / root / rel for root in _SOURCE_ROOTS if root
            and (repo_root / root / rel).is_file()]
    if len(hits) == 1:
        return hits[0], ""
    if len(hits) > 1:
        where = ", ".join(sorted(h.relative_to(repo_root).as_posix() for h in hits))
        return None, f"ambiguous bare name -- matches {where}; qualify the path"
    return None, f"{rel} does not exist"


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo_root), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _open_backlog_ids(repo_root: Path) -> set[str]:
    """Ids currently carried as rows in the generated BACKLOG.md.

    Read from BACKLOG.md rather than tasks/: a closed row keeps its task file as the
    id-allocation record (ADR-107 §6.3, retire-not-delete), so the file's existence says
    nothing about whether the row is open.
    """
    backlog = repo_root / "BACKLOG.md"
    if not backlog.exists():
        raise PreflightError(f"no BACKLOG.md at {backlog} -- cannot judge [#id] liveness")
    return set(re.findall(r"(?m)^- \[#(\d+)\]", backlog.read_text(encoding="utf-8",
                                                                   errors="replace")))


def verify(contract: Path, repo_root: Path = _REPO_ROOT) -> Report:
    """Extract every locator claim in `contract` and check it against `repo_root`."""
    try:
        text = Path(contract).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise PreflightError(f"cannot read contract {contract}: {exc!r}") from exc

    report = Report()
    seen: set[tuple[str, str]] = set()
    # Repo health established ONCE, before any SHA verdict is allowed to depend on it.
    git_healthy = _git(repo_root, "rev-parse", "--git-dir").returncode == 0

    def add(kind: str, raw: str, ok: bool, detail: str = "") -> None:
        if (kind, raw) in seen:
            return
        seen.add((kind, raw))
        report.checked.append(Claim(kind, raw, detail, ok))

    for m in _HEADING_RE.finditer(text):
        rel, heading = m.group(1), m.group(2)
        raw = f'{rel} heading "{heading}"'
        target = repo_root / rel
        if not target.exists():
            add("heading", raw, False, f"{rel} does not exist")
        elif heading in target.read_text(encoding="utf-8", errors="replace"):
            add("heading", raw, True)
        else:
            add("heading", raw, False, f"heading text not found in {rel}")

    for m in _FILE_LINE_RE.finditer(text):
        rel, line = m.group(1), int(m.group(2))
        raw = f"{rel}:{line}"
        target, note = _resolve(repo_root, rel)
        if target is None:
            add("file-line", raw, False, note)
            continue
        n = len(target.read_text(encoding="utf-8", errors="replace").splitlines())
        if line < 1 or line > n:
            add("file-line", raw, False, f"{target.relative_to(repo_root).as_posix()} "
                                         f"has {n} lines")
        else:
            add("file-line", raw, True)

    for m in _SHA_RE.finditer(text):
        sha = m.group(1)
        if sha.isdigit():
            continue  # a run of digits is a count far more often than a commit
        r = _git(repo_root, "cat-file", "-e", f"{sha}^{{commit}}")
        if r.returncode == 0:
            add("sha", sha, True)
        elif git_healthy:
            add("sha", sha, False, "not reachable in history")
        else:
            # "could not check" is NOT "checked and stale" (terra HIGH, 2026-08-04). git exits 1
            # for BOTH a missing object and a broken invocation, so without the health probe a
            # dead git would have rendered every SHA as a tidy ordinary failure at exit 1 --
            # precisely the confusion [#465] leg 4 removed from the audit writer, reintroduced
            # here in the tool built to answer that class.
            raise PreflightError(
                f"git is not usable at {repo_root} -- cannot judge SHA {sha}; refusing to "
                "report it as stale")

    open_ids = _open_backlog_ids(repo_root)
    for m in _BACKLOG_RE.finditer(text):
        tid = m.group(1)
        ok = tid in open_ids
        add("backlog-id", f"[#{tid}]", ok, "" if ok else "not open in BACKLOG.md")

    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="preflight_contract",
                                 description="Verify the repo locators a contract cites.")
    ap.add_argument("contract", help="contract/prompt file to verify")
    ap.add_argument("--repo-root", default=str(_REPO_ROOT), help="repo to verify against")
    args = ap.parse_args(sys.argv[1:] if argv is None else argv)

    try:
        report = verify(Path(args.contract), Path(args.repo_root))
    except PreflightError as exc:
        print(f"preflight_contract: INTERNAL ERROR: {exc} -- refusing to report clean; "
              "an error is never a silent pass", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 -- fail CLOSED, the check_seal_identity posture
        print(f"preflight_contract: INTERNAL ERROR: {exc!r} -- refusing to report clean",
              file=sys.stderr)
        return 2

    print(report.render())
    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main())
