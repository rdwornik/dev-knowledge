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
    sha          `abc1234`                present in this repo's object store
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

THE FREEZE-TIME PREDICATES ([#591] extension, 2026-08-28). Everything above verifies what a
contract CITES. Four more classes shipped into batch-1's frozen contract that no locator
check can see, and they are answered in the second half of this file: an off-repo input
assumed on disk, a "verified"/"measured" claim with no witness, a cited id naming the wrong
row, and a do-not-touch claim contradicted by the detector's own scope roots. They are opt-in
(`--freeze` / `--predicates-only`) and, like everything else here, wired into no gate.

Usage:
    python scripts/preflight_contract.py docs/audits/<contract>.md
    python scripts/preflight_contract.py <contract> --repo-root /path/to/repo
    python scripts/preflight_contract.py <contract> --freeze      # + the four predicates
    python scripts/preflight_contract.py <contract> --predicates-only
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

_REPO_ROOT = _SCRIPTS.parent

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


# --- [#483] R2 role rule: ASSERTION vs CITATION -----------------------------------------
#
# An `[#id]` is an ASSERTION (it claims the row is OPEN) only on forward-committing surfaces:
# emitted prompts/contracts, plan documents, OPEN-claiming BACKLOG references. It is a CITATION
# (no open-claim) in historical narration. Before this rule the leg read EVERY `[#id]` as an
# assertion: its first production run over the 2026-08-04 handoff bundle flagged 11 ids, all of
# them correct historical citations, so a gate wired on that behaviour would RED every handoff
# bundle by construction ([#483] ruling R1/R2, verbatim at
# docs/audits/2026-08-04-technical-483-enforcement-ruling.md).
#
# Two mechanical layers. Neither is an id allow-list and neither is a path waiver: role is
# derived from where the text sits and what shape it sits in.
ASSERTION, CITATION = "assertion", "citation"

# Layer 1 — surface path CLASS. Measured over the tracked corpus: these carry 4810 of 7178
# `[#id]` occurrences (67%). docs/audits/ + docs/handoffs/ is [#483] sub-question (b), ruled.
_CITATION_PREFIXES = ("docs/audits/", "docs/handoffs/")
_CITATION_FILES = ("JOURNAL.md", "LESSONS.md")

# Layer 2 — in-line context on an assertion-role surface.
# Backtick-quoted spans are PROSE quoting a convention, not the convention being used. Stripping
# them must happen FIRST: this repo's own BACKLOG carries a row whose prose reads
# "the `kill-candidates: #370` resting on it, are spent", and a scan that matches the field
# before stripping reads that quote as a live field. Measured on the live BACKLOG, the ordering
# is worth 24 -> 2 -> 1 flags.
# Run-aware: markdown allows ``double-tick`` spans, so a fixed single-tick pair would mask the
# wrong extent. An UNBALANCED tick matches nothing and therefore masks nothing — the safe
# direction, since unmasked text stays assertion-role rather than being suppressed.
_TICK_SPAN = re.compile(r"(`+)[\s\S]*?\1")
# A BACKLOG task row. In one, only the `kill-candidates:` VALUE is an open-claim -- `refs` and
# the reason prose after the em-dash cite related work, including closed rows, by design.
#
# The `[P#][size]` tags are REQUIRED, not decoration. Matching a bare `- [#123]` bullet as a row
# made every such bullet a row-with-no-kill-candidates-field, i.e. a CITATION -- which silently
# suppressed a real assertion in an ordinary markdown list. Caught by an existing extraction test
# rather than by inspection; an over-broad citation rule is the dangerous direction, because it
# fails toward saying nothing.
_BACKLOG_ROW = re.compile(r"^- \[#\d+\]\s+\[P\d\]\[[SMLX]+\]")
#
# DELIMITER-ANCHORED, and EVERY field is scanned, not just the first (terra HIGH 2026-08-04).
# `search()` on an unanchored pattern stopped at the first `kill-candidates:` in the row, so a
# row reading "· kill-candidates: none — spent · kill-candidates: [#479]" hid a genuinely stale
# assertion behind an earlier benign field. That is the silent-suppression direction — the one
# this tool must never fail in — so the field must begin a row-field (start of line or `·`).
_KILL_FIELD = re.compile(r"(?:^|·)\s*kill-candidates:\s*([^·\n]*)")
_REASON_SEP = re.compile(r"\s+(?:—|--|-\s)")
# `since [#436]` -- a provenance clause names where something came from, never that it is open.
_PROVENANCE = re.compile(r"\bsince\s*$")
# A markdown table row under a header whose first cell is a closed/shipped/superseded state.
_TABLE_ROW = re.compile(r"^\s*\|")
# The first cell must be EXACTLY a closed-state word — the cell has to end there (terra HIGH
# 2026-08-04). A `\b` boundary let `| closed-loop notes |` open closed-table mode and suppress
# every following row of an unrelated table.
_CLOSED_HEADER = re.compile(r"^\s*\|\s*(closed|shipped|superseded|retired|done)\s*\|", re.I)
# A real markdown table has a separator row under its header. Requiring it stops a stray
# pipe-prefixed prose line from opening suppression on everything that follows.
_TABLE_SEPARATOR = re.compile(r"^\s*\|[\s:|-]*-[\s:|-]*\|?\s*$")


def kill_candidate_value_spans(line: str) -> list[tuple[int, int]]:
    """(start, end) of EVERY delimited `kill-candidates:` VALUE in `line`, original coordinates.

    Ticks are masked to equal length first, so a field QUOTED in prose is not mistaken for a
    real one while offsets stay comparable to the unmasked line.
    """
    masked = _mask_ticks(line)
    spans: list[tuple[int, int]] = []
    for m in _KILL_FIELD.finditer(masked):
        start = m.start(1)
        sep = _REASON_SEP.search(m.group(1))
        spans.append((start, start + (sep.start() if sep else len(m.group(1)))))
    return spans


def surface_role(contract: Path, repo_root: Path) -> str:
    """Layer 1 — the role every `[#id]` in this file carries by virtue of WHERE it lives.

    Defaults to ASSERTION, deliberately. A contract emitted outside the repo (the common case
    for a session prompt) is forward-committing, and an unknown in-repo surface is one nobody
    has classified -- both must keep being checked. Silence is the failure mode this tool
    exists to remove, so the default may never be CITATION.
    """
    try:
        rel = Path(contract).resolve().relative_to(Path(repo_root).resolve()).as_posix()
    except ValueError:
        return ASSERTION                      # outside the repo: an emitted contract
    if rel.startswith(_CITATION_PREFIXES):
        return CITATION
    if rel in _CITATION_FILES or rel.startswith("LESSONS-legacy"):
        return CITATION
    return ASSERTION


def _mask_ticks(line: str) -> str:
    """Blank out backtick spans, PRESERVING length so offsets stay comparable to the original."""
    return _TICK_SPAN.sub(lambda m: " " * (m.end() - m.start()), line)


def line_role(line: str, id_start: int, *, in_closed_table: bool = False) -> str:
    """Layer 2 — the role of ONE `[#id]` occurrence, from the shape around it.

    `id_start` is the occurrence's offset, so a line carrying both an assertion and a citation
    is judged per occurrence rather than wholesale.
    """
    # NO blanket "inside backticks -> citation" rule, deliberately. An earlier cut had one, and
    # it was a SILENT-SUPPRESSION HOLE: this repo backticks `[#id]` as ordinary formatting
    # (`| `[#479]` | ... |` is the normal closed-table shape), so every properly formatted stale
    # assertion would have been waved through. Caught by this arc's own closed-table test, not by
    # inspection. Backticks still matter, but ONLY where they quote a FIELD NAME — and that is
    # handled by masking inside `kill_candidate_value_spans`, which is the narrow, testable place
    # for it.
    if _PROVENANCE.search(line[:id_start]):          # "... GENERATED since [#436]"
        return CITATION
    if in_closed_table and _TABLE_ROW.match(line):   # a row under a `| closed |` header
        return CITATION
    if _BACKLOG_ROW.match(line):
        # Only a kill-candidates VALUE claims openness. `refs` and the reason prose after the
        # em-dash cite related work -- including closed rows -- by design. EVERY field is
        # considered: a row may carry more than one, and stopping at the first hid a real
        # stale assertion behind an earlier benign one.
        return (ASSERTION
                if any(s <= id_start < e for s, e in kill_candidate_value_spans(line))
                else CITATION)
    return ASSERTION


@dataclass(frozen=True)
class Claim:
    kind: str
    raw: str
    detail: str = ""
    ok: bool = True


@dataclass
class Report:
    checked: list[Claim] = field(default_factory=list)
    #: What this report is ABOUT, for the summary line. The locator legs and the freeze-time
    #: predicates render through the same Report and must not both claim to be counting
    #: "locator claims" -- a run that mixes them would otherwise report one number for two
    #: different things.
    label: str = "locator claim"

    @property
    def failed(self) -> list[Claim]:
        return [c for c in self.checked if not c.ok]

    def render(self) -> str:
        lines = []
        for c in self.checked:
            lines.append(f"  {'PASS' if c.ok else 'FAIL'}  [{c.kind}] {c.raw}"
                         + (f" -- {c.detail}" if c.detail else ""))
        n, bad = len(self.checked), len(self.failed)
        lines.append(f"preflight_contract: {n - bad}/{n} {self.label}(s) resolved"
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

    # The source-root search applies ONLY to a syntactically BARE filename (terra HIGH r2,
    # 2026-08-04). A qualified or absolute path names exactly one place; searching elsewhere
    # after it fails to resolve would let `scripts/typo.py:1` quietly verify against
    # `deploy/typo.py`, which is the same wrong-file defect the ambiguity guard exists to stop.
    if "/" in rel or "\\" in rel or (len(rel) > 1 and rel[1] == ":"):
        return None, f"{rel} does not exist"

    # The repo root is IN the ambiguity set: a bare name present at the root AND in a source
    # root is ambiguous too, and the early `direct` return above only covers the case where the
    # root copy exists at all.
    hits = [repo_root / root / rel if root else repo_root / rel
            for root in _SOURCE_ROOTS if (repo_root / root / rel if root
                                          else repo_root / rel).is_file()]
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
    # Repo health is probed LAZILY, once, and only if a SHA claim actually needs it (terra
    # HIGH r2, 2026-08-04). Probing eagerly and ignoring the result outside the SHA loop let a
    # file-only contract return a clean report against an unusable repo -- a failed operational
    # probe going silent, which is the posture this tool claims not to have. Probing eagerly and
    # failing hard would be worse in the other direction: it would refuse to verify a
    # file-and-heading contract in a tree that has no git at all, which is a legitimate use.
    _health: list[bool] = []

    def git_healthy() -> bool:
        if not _health:
            _health.append(_git(repo_root, "rev-parse", "--git-dir").returncode == 0)
        return _health[0]

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
        # A short sha made only of digits IS a sha (about 1 commit in 48 abbreviates to one).
        # It used to be dropped here as "a count more often than a commit", which made the
        # locator neither checked nor failed -- a false CLEAN ([#936]). It is checked like any
        # other; when it does not resolve, the failure says it may be a count, so the operator
        # can tell a stale sha from a number that was never one.
        r = _git(repo_root, "cat-file", "-e", f"{sha}^{{commit}}")
        if r.returncode == 0:
            add("sha", sha, True)
        elif git_healthy():
            # HONEST WORDING (terra HIGH r2, 2026-08-04): `cat-file -e` proves the object is
            # PRESENT IN THIS REPO'S OBJECT STORE, not that it is reachable from any ref, so a
            # dangling commit passes. Saying "not reachable in history" over-claimed what the
            # probe establishes. Ref-set reachability is a real improvement and is recorded as
            # a known limit on [#483] rather than half-built here.
            add("sha", sha, False,
                "all-digit token, not present in this repo's object store (a stale sha, or a "
                "count that is not one)" if sha.isdigit()
                else "not present in this repo's object store")
        else:
            # "could not check" is NOT "checked and stale" (terra HIGH, 2026-08-04). git exits 1
            # for BOTH a missing object and a broken invocation, so without the health probe a
            # dead git would have rendered every SHA as a tidy ordinary failure at exit 1 --
            # precisely the confusion [#465] leg 4 removed from the audit writer, reintroduced
            # here in the tool built to answer that class.
            raise PreflightError(
                f"git is not usable at {repo_root} -- cannot judge SHA {sha}; refusing to "
                "report it as stale")

    # backlog-id: the ONLY claim kind carrying the [#483] role rule. A file:line or a SHA means
    # the same thing wherever it is written; an `[#id]` does not -- in narration it names a row,
    # in a contract it claims one is live. The other kinds are deliberately left untouched.
    if surface_role(contract, repo_root) == ASSERTION:
        open_ids = _open_backlog_ids(repo_root)
        # Closed-table suppression requires a VALIDATED table: a header whose first cell is
        # exactly a closed-state word, immediately followed by a markdown separator row (terra
        # HIGH 2026-08-04). Entering on the header alone let a stray pipe-prefixed line — or a
        # table merely headed `| closed-loop notes |` — suppress everything that followed.
        lines = text.splitlines()
        in_closed_table = False
        for idx, line in enumerate(lines):
            if _CLOSED_HEADER.match(line):
                nxt = lines[idx + 1] if idx + 1 < len(lines) else ""
                in_closed_table = bool(_TABLE_SEPARATOR.match(nxt))
            elif not _TABLE_ROW.match(line):
                in_closed_table = False                   # any non-table line ends the table
            for m in _BACKLOG_RE.finditer(line):
                if line_role(line, m.start(), in_closed_table=in_closed_table) == CITATION:
                    continue
                tid = m.group(1)
                ok = tid in open_ids
                add("backlog-id", f"[#{tid}]", ok, "" if ok else "not open in BACKLOG.md")

    # Predicate (vi) rides the LOCATOR run as well as the freeze run, because that is where its
    # subject lives: a declared input is a locator claim, and `/preflight` is the surface a seat
    # points at a contract BEFORE acting on it. Appended rather than folded into `add()` so the
    # one implementation serves both callers -- two copies of a path check is how the two
    # answers start to disagree.
    report.checked.extend(check_consumed_artifacts(text, Path(repo_root)))
    return report


# =========================================================================================
# FREEZE-TIME PREDICATES -- the [#591] extension
# =========================================================================================
#
# WHAT THESE ANSWER. `verify()` above checks locators a contract CITES. It cannot see the
# four defect classes the architect shipped into batch-1's frozen contract on 2026-08-28,
# because none of them is a stale `file:line`:
#
#   (i)   an off-repo artifact ASSUMED on disk. Batch-1 L3's `**Basis:** the SDA-1
#         adversarial artifact` -- finding C-G, "either it is unreachable from this host
#         and needs a locator recorded, or it was never produced".
#   (ii)  a "verified"/"measured" claim carrying NO WITNESS. Batch-1 L5 item 3: *"Ratchet
#         untouched (ecosystem/ + code are outside its scope roots -- verified, not
#         assumed)"*. Nothing was verified; the word did the work of the check.
#   (iii) a cited id naming the WRONG ROW. Batch-1 L2 names `[#587]` twice for a seam that
#         is `[#608]`. Note what this one is NOT: `[#587]` is open, same theme, same story,
#         same serialize-group, same file. LIVENESS ALONE CANNOT CATCH IT -- which is why
#         this leg reports every resolved row's TITLE and flags a title that shares no
#         content word with the prose around the citation.
#   (iv)  a do-not-touch claim contradicted by the detector's own scope roots. The same L5
#         sentence: `ecosystem/*.yaml` IS `silent_rule_detector`'s third scope root.
#
# WHY THEY LIVE HERE AND NOT IN `validate_substrate.py`. The [#591] contract permits "its
# ruled sibling", and this is the honest home. `validate_substrate` answers ONE question --
# does a contract's declared SUBSTRATE agree with its content -- against a substrate
# registry it reads. None of these four is a substrate question. All four are this module's
# charter verbatim: *"verify the repo locators a contract or prompt cites, before acting"*.
# Leg (iii) is already half-built here (`backlog-id`), and legs (i)/(ii) reduce to "does
# this claim carry a locator that resolves". Putting them in the substrate validator would
# have made it two organs sharing a filename.
#
# POSTURE. Same as the module's: 0 clean, 1 violation, 2 internal error -- and an internal
# error BLOCKS (Z-G4: a check that cannot compute its ground truth FAILS, it does not skip).
# WIRED INTO NO GATE, deliberately: arming a hook is a separate act with its own roster and
# doc consequences (`ARCHITECTURE.md` Ch2, `CLAUDE.md` §9). Reported as a candidate filing.

PREDICATE_KINDS = ("off-repo-input", "unwitnessed-claim", "cited-id", "do-not-touch-scope",
                   "open-batch")


# --- text units: the thing a claim is judged in ------------------------------------------
#
# NOT the line. This corpus hard-wraps at ~90 chars, so a claim and its witness routinely
# sit on different lines -- batch-1's `... the region template and `CLAUDE.md` render` /
# `identically (region mechanism verified, not eyeballed)` is one sentence across two. A
# line-unit detector would report that as unwitnessed because the witness wrapped, which is
# a false positive produced purely by typography.

_FENCE_RE = re.compile(r"^ {0,3}(?:```|~~~).*?(?:^ {0,3}(?:```|~~~)|\Z)", re.M | re.S)
_QUOTE_LINE_RE = re.compile(r"^ {0,3}>.*$", re.M)
_BLOCK_BREAK_RE = re.compile(r"^\s*(?:$|#{1,6}\s|[-*+]\s|\d+\.\s|\|)")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(`*\[])")


def _blank_out(text: str, pattern: re.Pattern[str]) -> str:
    """Replace every match with blanks of equal length -- offsets and line numbers survive."""
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def claim_units(text: str, *, drop_quotes: bool = True) -> list[tuple[str, int]]:
    """`(unit_text, 1-based line)` for every sentence-ish unit in `text`.

    Fenced blocks are blanked: a command inside a fence is a TEMPLATE the executor will run,
    not a claim the architect is making.

    Blockquoted lines are blanked when `drop_quotes` -- and that is the design note's own
    false-positive warning made mechanical. This batch's bundles QUOTE each lane's contract
    verbatim under `>`, so a scan that reads quoted text as first-person claims reports the
    same defect once per bundle that ever repeated it. Leg (i) opts OUT (`drop_quotes=False`)
    because a dispatch line's operator path is usually inside exactly such a block, and an
    unreachable path is unreachable whoever wrote it.
    """
    body = _blank_out(text, _FENCE_RE)
    if drop_quotes:
        body = _blank_out(body, _QUOTE_LINE_RE)

    units: list[tuple[str, int]] = []
    buf: list[str] = []
    start = 1
    for lineno, line in enumerate(body.splitlines(), start=1):
        if _BLOCK_BREAK_RE.match(line):
            if buf:
                units.append((" ".join(buf), start))
            buf, start = ([line.strip()], lineno) if line.strip() else ([], lineno + 1)
            continue
        if not buf:
            start = lineno
        buf.append(line.strip())
    if buf:
        units.append((" ".join(buf), start))

    out: list[tuple[str, int]] = []
    for block, lineno in units:
        for piece in _SENTENCE_SPLIT_RE.split(block):
            if piece.strip():
                out.append((piece.strip(), lineno))
    return out


# --- (i) off-repo inputs -----------------------------------------------------------------
#
# "Off-repo" is the design note's own definition: an absolute operator-disk path, and a
# name resolving against the prompts dir. Existence is checked AT FREEZE, on the machine
# doing the freezing, and a MISS is a REFUSAL naming the path -- not a warning.

#: The lookbehind excludes `\w` ONLY. It must NOT exclude a backtick: a contract's normal
#: spelling of a path is a backticked span, so a lookbehind that rejected `` ` `` skipped the
#: common case entirely and extracted nothing -- and a verifier that extracts nothing passes
#: everything, this module's own defining failure mode.
_OFF_REPO_PATH_RE = re.compile(
    r"(?<!\w)((?:[A-Za-z]:[\\/]"
    r"|\\\\[A-Za-z0-9_.-]+[\\/]"          # a UNC share -- \\server\share\...
    r"|~[\\/]"
    r"|%USERPROFILE%[\\/]"
    r"|\$env:CLAUDE_PROMPTS_DIR[\\/]"
    r"|\$CLAUDE_PROMPTS_DIR[\\/]"
    r"|<PROMPTS_DIR>[\\/]"
    # POSIX absolute, restricted to real filesystem roots (terra HIGH, this arc). A bare
    # leading `/` is NOT usable here: this corpus writes `/preflight`, `/lane-boot`,
    # `/handoff` and a dozen other slash-commands in ordinary prose, and matching those
    # would bury every real finding under command names. Naming the roots keeps the recall
    # without the noise -- and the noise is what gets a detector switched off.
    r"|/(?:home|mnt|Users|users|tmp|var|opt|root|srv|workspaces)/)"
    r"[^\s`'\"<>|]+)")

# An INPUT CLAUSE that carries no locator at all -- the C-G shape. `**Basis:** the SDA-1
# adversarial artifact` names a thing the contract depends on and gives the executor nothing
# to open. This is the half of (i) that a path-existence check structurally cannot reach:
# there is no path to check, and that IS the defect.
_INPUT_CLAUSE_RE = re.compile(
    r"^ {0,3}\*{0,2}(?P<field>Basis|Inputs?|Reads|Reads from|Fixture|Source artifact|"
    r"Prior art|Depends on)\*{0,2}\s*:\*{0,2}[ \t]*(?P<body>\S.*)$", re.M | re.I)
# A locator is something OPENABLE, and backticks alone do not make it one (terra HIGH, this
# arc): ``**Basis:** `SDA-1 artifact` `` is the same unopenable claim with quotes around it,
# and accepting it would let the C-G defect discharge itself by adding punctuation. So a
# backticked span counts only if it looks like a path -- a slash, or a file extension. Bare
# hex is excluded on purpose: `defaced` is seven characters of [0-9a-f], and so is a lot of
# prose.
_LOCATOR_RE = re.compile(
    r"`[^`\n]*(?:/|\\|\.[A-Za-z0-9]{1,6}\b)[^`\n]*`|\[#\d+\]|\bADR-\d+\b")
# "nothing" is a real, complete answer to `**Depends on:**` and must not read as a miss.
_NO_INPUT_RE = re.compile(r"^\s*(nothing|none|n/?a)\b", re.I)


def _expand_off_repo(raw: str) -> tuple[Path | None, str]:
    """`(resolved, note)` for one off-repo path token.

    An UNSET variable resolves to nothing and is reported as unresolvable rather than
    skipped: "I could not look" is a refusal here, because the whole point of the leg is
    that the freezing machine can reach what the contract names.
    """
    text = raw.replace("\\", "/")
    for token, var in (("$env:CLAUDE_PROMPTS_DIR", "CLAUDE_PROMPTS_DIR"),
                       ("$CLAUDE_PROMPTS_DIR", "CLAUDE_PROMPTS_DIR"),
                       ("<PROMPTS_DIR>", "CLAUDE_PROMPTS_DIR"),
                       ("%USERPROFILE%", "USERPROFILE")):
        if text.startswith(token):
            base = os.environ.get(var)
            if not base:
                return None, (f"names {token}, which is unset on the freezing machine -- "
                              f"the path cannot be resolved, so it cannot be confirmed")
            text = base.replace("\\", "/").rstrip("/") + text[len(token):]
            break
    else:
        if text.startswith("~/"):
            text = Path.home().as_posix().rstrip("/") + text[1:]
    return Path(text), ""


def check_off_repo_inputs(text: str) -> list[Claim]:
    """Predicate (i): every referenced off-repo input EXISTS at freeze."""
    out: list[Claim] = []
    seen: set[str] = set()

    # Fences are NOT stripped here, deliberately: a lane's operator-disk path lives in its
    # `## Dispatch` code block precisely because that block is the literal command, and an
    # unreachable path is unreachable whether or not it is fenced.
    for m in _OFF_REPO_PATH_RE.finditer(text):
        raw = m.group(1).rstrip(".,;:)")
        if raw in seen:
            continue
        seen.add(raw)
        resolved, note = _expand_off_repo(raw)
        if resolved is None:
            out.append(Claim("off-repo-input", raw, note, False))
        elif resolved.exists():
            out.append(Claim("off-repo-input", raw, "exists at freeze", True))
        else:
            out.append(Claim("off-repo-input", raw,
                             f"does not exist at freeze ({resolved.as_posix()}) -- the "
                             f"executor cannot reach it", False))

    for m in _INPUT_CLAUSE_RE.finditer(text):
        field, body = m.group("field"), m.group("body").strip()
        raw = f"{field}: {body[:60]}" + ("..." if len(body) > 60 else "")
        if _NO_INPUT_RE.match(body) or _LOCATOR_RE.search(body):
            out.append(Claim("off-repo-input", raw, "input clause carries a locator", True))
        else:
            out.append(Claim("off-repo-input", raw,
                             f"the `{field}:` clause names an input with NO locator -- no "
                             f"path, no [#id], no ADR. Nothing here can be opened, so "
                             f"nothing here can be confirmed to exist", False))
    return out


# --- (ii) witness-carrying claims --------------------------------------------------------
#
# THE PRECISION/RECALL TRADE, stated because the design note requires it and because a
# detector this repo cannot trust is a detector it will disable.
#
# RECALL is deliberately capped at one axis: the trigger words are the contract's own,
# `verif*` and `measur*`. No attempt is made to read English for unmarked assertions.
#
# PRECISION is bought three ways, each one paying for a measured false positive on the
# batch-1 corpus: fenced blocks and blockquotes are dropped (the bundles quote their own
# lanes); the trigger must sit OUTSIDE a backtick span (prose quoting the convention is not
# the convention being used -- the same ordering `kill_candidate_value_spans` above depends
# on); and the unit is a sentence, not a line, so a witness that hard-wrapped still counts.
#
# NO ATTEMPT IS MADE to separate a past-tense CLAIM ("verified, not assumed") from a future
# OBLIGATION ("verify no leftovers"), and that is a decision, not an omission. Both want the
# same thing, and the repo's own forward rule (LESSONS.md 2026-08-28) is unconditional:
# *"the word 'verified' in a contract must name the command that verified it."* An
# obligation that names its command is a better obligation. Measured on batch-1's frozen
# contract this costs nothing: every obligation there that fires is one a reader would
# agree should name a command.

_CLAIM_TRIGGER_RE = re.compile(r"\b(?:verif|measur)\w*", re.I)

#: What counts as a witness: a COMMAND or a LOCATOR, never a bare subject. `CLAUDE.md` is
#: what a claim is ABOUT; `boundary_headers.py --check` is what established it.
#:
#: A MULTI-WORD BACKTICKED SPAN IS NOT ITSELF A WITNESS (terra HIGH, this arc). The first cut
#: accepted any backticked text containing whitespace, so *"verified in `the artifact`"*
#: passed -- which hands every author a two-word escape from the predicate and makes the leg
#: worse than absent, because it renders green. A command line has to look like one: it
#: begins with a runnable verb this repo actually invokes, or it carries a path, a script or
#: a flag.
_COMMAND_VERBS = (r"uv|git|python|py|pytest|ruff|pre-commit|grep|rg|wc|sed|awk|find|ls|"
                  r"codex|claude|gh|npm|node|bash|pwsh|powershell|cat|head|tail|diff")
_WITNESS_RES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("a file:line locator", re.compile(r"`[^`\n]*\.[A-Za-z0-9]{1,6}:\d+`")),
    ("a command line", re.compile(rf"`\s*(?:{_COMMAND_VERBS})\s+\S[^`\n]*`")),
    ("a script", re.compile(r"`[^`\n]*\.(?:py|ps1|sh)\b[^`\n]*`")),
    ("a flag", re.compile(r"`[^`\n]*--[A-Za-z][^`\n]*`")),
    ("a repo path", re.compile(r"`[^`\n]*[a-z_]+/[A-Za-z0-9_.*-]+[^`\n]*`")),
    # A dotted callable: lowercase snake_case both sides, tail not a file extension. This is
    # what keeps `validate_doc_rot.scan_file_budget` a witness and `CLAUDE.md` a subject.
    ("a named callable",
     re.compile(r"`[a-z_][a-z0-9_]*\.(?!(?:md|py|ps1|sh|ya?ml|json|txt|toml|cfg|ini|lock|"
                r"jsonl|log|tmpl|xml|csv)\b)[a-z_][a-z0-9_.]*`")),
)


def _outside_ticks(unit: str) -> str:
    """The unit with backtick spans blanked -- where a trigger word has to be to count."""
    return _mask_ticks(unit)


def check_witnessed_claims(text: str) -> list[Claim]:
    """Predicate (ii): every "verified"/"measured" claim carries a witness."""
    out: list[Claim] = []
    for unit, lineno in claim_units(text):
        if not _CLAIM_TRIGGER_RE.search(_outside_ticks(unit)):
            continue
        trigger = _CLAIM_TRIGGER_RE.search(_outside_ticks(unit))
        assert trigger is not None
        word = unit[trigger.start():trigger.end()]
        excerpt = unit if len(unit) <= 110 else unit[:107] + "..."
        raw = f"line {lineno}: {excerpt}"
        found = [label for label, pattern in _WITNESS_RES if pattern.search(unit)]
        if found:
            out.append(Claim("unwitnessed-claim", raw, f"witnessed by {found[0]}", True))
        else:
            out.append(Claim("unwitnessed-claim", raw,
                             f"asserts {word!r} and names no witness -- a witness is a "
                             f"command or a file:line in the same sentence, and the word "
                             f"is doing the work of the check", False))
    return out


# --- (iii) live id resolution ------------------------------------------------------------
#
# `[#id]` resolves against `tasks/`, NOT `BACKLOG.md`. `_open_backlog_ids` above reads
# BACKLOG.md and is left alone -- it answers a different question (is this row OPEN) for the
# locator leg. This leg needs a different one, and the difference is the whole point of
# batch-1 defect 2: BACKLOG.md collapses "this id was never allocated" and "this id names a
# closed row" into the same negative, and `tasks/` keeps them apart because a closed row
# KEEPS its file as the id-allocation record (ADR-107 §6.3, retire-not-delete).
#
# HONEST LIMIT, stated first because it bounds what a clean run means: `[#587]` cited for
# `[#608]`'s seam is a LIVE, OPEN row. No liveness check catches it, and no strengthening of
# one ever will. What this leg does instead is what LESSONS.md's forward rule asks -- *"a
# contract citing an id must quote that row's title beside it"* -- in the only two mechanical
# forms available: every resolved id's TITLE is carried into the evidence line so a freezer
# reads it beside their own prose, and a citation whose surrounding prose describes the row
# in content words the title does not share is FLAGGED.

_TASK_ID_RE = re.compile(r'^id:\s*"?\[#(\d+)\]"?', re.M)
_TASK_TITLE_RE = re.compile(r'^title:\s*"?(.*?)"?\s*$', re.M)
_TASK_STATUS_RE = re.compile(r'^status:\s*"?([A-Za-z-]+)"?', re.M)
TERMINAL_STATUSES = frozenset({"closed", "retired", "superseded"})

_ADR_RE = re.compile(r"\bADR-(\d{1,3})\b")
#: A register id is checked ONLY where the contract marks it as one. Two measured false
#: positives on batch-1's contract set this boundary, and both are the same shape -- an id
#: namespace that is not the register:
#:   * `per ADR-85`   -- `[A-Z]{1,2}-?[A-Z]?` happily eats `ADR-`, so every ADR citation was
#:                       also looked up as a ruling. Excluded by lookahead; ADRs have their
#:                       own leg two lines up.
#:   * `per W2/D5`    -- a SESSION-PLAN id, not a register id. `per` and `under` are simply
#:                       too weak a marker: they precede lane letters, plan steps and Q-cuts
#:                       as readily as rulings.
#: So the keyword set is the explicit ones only, plus any candidate inside a sentence that
#: names the register file. RECALL COST, stated rather than hidden: a bare `per Z-G3` -- a
#: real register citation, and the spelling batch-1 actually uses -- is NOT checked. That is
#: the deliberate direction. A false refusal on a lane letter is the noise that gets a
#: detector switched off, and this one is opt-in and ungated; it has to be worth running.
_REGISTER_KEYWORD_RE = re.compile(
    r"\b(?:register|registers|standing ruling|standing rulings|ruling|rulings)\s+"
    r"(?:`[^`]*`\s+)?(?:`|\*\*)?(?!ADR-)([A-Z]{1,2}-?[A-Z]?-?\d{1,2})(?:`|\*\*)?\b")
_REGISTER_BARE_RE = re.compile(r"(?:`|\*\*)?(?!ADR-)\b([A-Z]{1,2}-?[A-Z]?-?\d{1,2})\b")
_REGISTER_FILE_RE = re.compile(r"STANDING_RULINGS", re.I)
#: `per`/`under` are readmitted -- but ONLY for an id whose SECTION LETTER is one the live
#: register actually uses (terra HIGH, this arc). Dropping the weak keywords outright was
#: correct about `per W2/D5` (a session-plan id) and wrong about `per Z-G3`, which is a real
#: register citation and the spelling batch-1 uses. Reading the register's own section
#: letters separates the two WITHOUT restating anything: `Z` is live so `per Z-Q9` is
#: checked and refused, `W` is not a register section so `per W2` is left alone. A typo
#: inside a live section still surfaces, which is the case that matters.
_REGISTER_WEAK_RE = re.compile(
    r"\b(?:per|under)\s+(?:`|\*\*)?(?!ADR-)([A-Z]{1,2}-?[A-Z]?-?\d{1,2})(?:`|\*\*)?\b")
_REGISTER_HEADING_RE = re.compile(r"^#{2,4}\s+([A-Z]{1,2})-?[A-Z]?-?\d{1,2}\b", re.M)

#: How far past an `[#id]` to read for a description of the row. Bounded by the first
#: clause-ending mark: the words immediately after a citation are the ones making a claim
#: about it, and a whole sentence away is a different subject.
_ID_WINDOW_RE = re.compile(r"[^,;.·()\[\]—\n]{0,120}")
#: The mirror window, kept for the both-sides experiment recorded above; see check_cited_ids.
_ID_WINDOW_BEFORE_RE = re.compile(r"[^,;.·()\[\]—\n]{0,120}$")
#: Below this many content words there is no description to disagree with. `[#592]-shaped`
#: is a bare pointer -- it says nothing about the row, so it cannot say anything WRONG about
#: it. Firing there was a measured false positive on batch-1 (twice), and it is the exact
#: over-reach that would make this leg untrustworthy.
_ID_DESCRIPTION_FLOOR = 2

_STOPWORDS = frozenset(
    "the a an and or of to in on at by for with from is are was were be been it its this "
    "that these those as not no than then so if into per via when where which who whom "
    "lane lanes contract done when item items green must shall never only also".split())


def _content_words(phrase: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]{4,}", phrase.lower()) if w not in _STOPWORDS}


def load_task_rows(repo_root: Path) -> dict[str, tuple[str, str]]:
    """`{id: (title, status)}` from `tasks/*.md` frontmatter -- the source of truth [#589].

    RAISES when `tasks/` is absent. An empty index would make every cited id "unresolved"
    or, worse under a different default, make every id pass; either way the leg would be
    reporting about a corpus it never read (Z-G4).
    """
    tasks = Path(repo_root) / "tasks"
    if not tasks.is_dir():
        raise PreflightError(
            f"no tasks/ directory at {tasks} -- cannot resolve any [#id]; refusing to "
            "report clean about ids this run never looked up")
    rows: dict[str, tuple[str, str]] = {}
    for path in sorted(tasks.glob("*.md")):
        head = path.read_text(encoding="utf-8", errors="replace")[:1200]
        m = _TASK_ID_RE.search(head)
        if m is None:
            continue
        title = _TASK_TITLE_RE.search(head)
        status = _TASK_STATUS_RE.search(head)
        rows[m.group(1)] = (title.group(1).strip() if title else "",
                            (status.group(1).strip().lower() if status else "unknown"))
    if not rows:
        raise PreflightError(
            f"tasks/ at {tasks} yielded no rows -- the frontmatter shape this leg reads "
            "has changed; refusing to report clean against an empty index")
    return rows


def check_cited_ids(text: str, repo_root: Path) -> list[Claim]:
    """Predicate (iii): every cited `[#id]` / ADR / register id resolves live."""
    rows = load_task_rows(repo_root)
    out: list[Claim] = []
    seen: set[tuple[str, str]] = set()

    def add(raw: str, ok: bool, detail: str) -> None:
        if (raw, detail) not in seen:
            seen.add((raw, detail))
            out.append(Claim("cited-id", raw, detail, ok))

    for unit, lineno in claim_units(text, drop_quotes=False):
        for m in _BACKLOG_RE.finditer(unit):
            tid = m.group(1)
            raw = f"[#{tid}]"
            if tid not in rows:
                add(raw, False, f"names no allocated row in tasks/ -- line {lineno}")
                continue
            title, status = rows[tid]
            if status in TERMINAL_STATUSES:
                add(raw, False, f"resolves to a {status.upper()} row {title!r} -- line "
                                f"{lineno}; a contract cannot dispatch work against it")
                continue
            # The identity echo. `[#587]`-for-`[#608]` is OPEN, right theme, right story,
            # right serialize-group and right file; ONLY the title separates the two rows,
            # so the title is what gets put in front of the freezer -- on the passing line
            # as much as the failing one.
            # Two different spans, on purpose. The GATE is the adjacent window -- is there a
            # description here at all? The TEST is the whole sentence -- does anything in it
            # share the row's vocabulary? Splitting them is what a measured pass over
            # batch-1 forced: gating on the sentence flagged `[#592]-shaped`, a bare pointer
            # that describes nothing and so cannot describe anything wrongly; testing on the
            # window flagged `## L1 — [#577]+[#584]: root AGENTS.md ..., lockstep — M`,
            # where the agreeing word sat one comma past the window's edge. Narrow gate,
            # generous test: fire only when a description exists AND nothing in the sentence
            # corroborates it.
            # AFTER-ONLY, and this is a MEASURED decision, not an oversight. Terra raised
            # the gap correctly -- a description sitting BEFORE the id is not gated, so
            # `the tiling seam at [#587]` would pass. The both-sides variant was built and
            # run, and it reintroduced a false positive on the live corpus: batch-1's
            # *"the agreement check's code home per the [#592] pattern"* is an ANALOGY
            # citation, where the preceding prose describes the LANE'S work rather than the
            # row, so nothing in it can be expected to share the row's title. Text AFTER an
            # id is usually an appositive naming the row; text BEFORE it is usually the
            # sentence's own subject. Since this organ is advisory and ungated, a measured
            # false positive costs more than a hypothetical false negative -- so the gap
            # stays, named, rather than being closed at the price of trust.
            after = _ID_WINDOW_RE.match(unit, m.end())
            described = _content_words(after.group(0) if after else "")
            if title and len(described) >= _ID_DESCRIPTION_FLOOR \
                    and not (_content_words(unit) & _content_words(title)):
                add(raw, False,
                    f"resolves to {title!r} ({status}), which shares no content word with "
                    f"the description beside it -- line {lineno}. Liveness is not identity: "
                    f"two open rows in one theme, story and serialize-group are told apart "
                    f"by their title and nothing else. Quote the row's title beside the id, "
                    f"or fix the id")
            else:
                add(raw, True, f"{title!r} ({status})")

        for m in _ADR_RE.finditer(unit):
            num, raw = m.group(1), m.group(0)
            hits = list(Path(repo_root).glob(f"docs/decisions/ADR-{num}-*.md"))
            add(raw, bool(hits),
                hits[0].name if hits else f"no docs/decisions/ADR-{num}-*.md -- line {lineno}")

        marked = _REGISTER_FILE_RE.search(unit)
        finders = ((_REGISTER_BARE_RE,) if marked
                   else (_REGISTER_KEYWORD_RE, _REGISTER_WEAK_RE))
        letters = _register_section_letters(repo_root)
        for finder in finders:
            for m in finder.finditer(unit):
                rid = m.group(1)
                # A weak-keyword hit is only a register citation if its section letter is
                # one the register uses; otherwise it is a lane letter or a plan step.
                if finder is _REGISTER_WEAK_RE and \
                        re.match(r"[A-Z]{1,2}", rid).group(0) not in letters:
                    continue
                ok = _register_heading_exists(repo_root, rid)
                add(f"register {rid}", ok,
                    "resolves to a STANDING_RULINGS heading" if ok else
                    f"no `### {rid}` heading in protocols/STANDING_RULINGS.md -- line "
                    f"{lineno}")
    return out


def _register_section_letters(repo_root: Path) -> frozenset[str]:
    """The section-letter prefixes the LIVE register actually uses -- read, never restated."""
    reg = Path(repo_root) / "protocols" / "STANDING_RULINGS.md"
    if not reg.is_file():
        raise PreflightError(
            f"no {reg} -- cannot judge register ids; refusing to report them clean")
    body = reg.read_text(encoding="utf-8", errors="replace")
    return frozenset(_REGISTER_HEADING_RE.findall(body))


def _register_heading_exists(repo_root: Path, rid: str) -> bool:
    """Is `rid` a live STANDING_RULINGS heading? Raises if the register is unreadable."""
    reg = Path(repo_root) / "protocols" / "STANDING_RULINGS.md"
    if not reg.is_file():
        raise PreflightError(
            f"no {reg} -- cannot judge register ids; refusing to report them clean")
    body = reg.read_text(encoding="utf-8", errors="replace")
    return re.search(rf"^#{{2,4}}\s+{re.escape(rid)}\b", body, re.M) is not None


# --- (iv) do-not-touch vs detector scope roots -------------------------------------------
#
# The scope roots are READ from `silent_rule_detector`, never restated. That is the design
# note's instruction and it is also the defect's own moral: batch-1's RATCHET preamble
# restated the roots as `protocols/*.md` + `templates/*`, dropped the third, and L5 then
# reasoned from the incomplete enum to a claim it labelled "verified".

_UNTOUCHED_RE = re.compile(
    r"\b(?:untouched|not touched|do(?:es)? not touch|must not touch|outside\b[^.]{0,60}?"
    r"\bscope|delta (?:is|of|must be)\s*(?:0|zero)|zero delta)", re.I)
_RATCHET_CTX_RE = re.compile(r"\bratchet\b|\bscope root|silent[_ -]rule", re.I)
#: Casefolded, because the detector casefolds (`silent_rule_detector._fold`). `Ecosystem/`
#: and `ecosystem/` are the same root to it, so they must be the same root here.
_DIR_TOKEN_RE = re.compile(r"(?<![\w/])([A-Za-z][A-Za-z0-9_-]*)/")
#: A path token in a write-scope clause: `ecosystem/routing-table.yaml`,
#: `templates/claude-regions/*.md`, `CLAUDE.md`.
_PATH_TOKEN_RE = re.compile(r"`([^`\n]+)`")
_WRITE_SCOPE_RE = re.compile(
    r"^ {0,3}\*{0,2}Write[- ]scope\*{0,2}\s*:\*{0,2}[ \t]*(?P<body>\S.*)$", re.M | re.I)


def ratchet_scope_roots() -> tuple[str, ...]:
    """The detector's own scope-root directory names. Raises if it cannot be read (Z-G4)."""
    try:
        import silent_rule_detector as srd
        return tuple(dirname for dirname, _recurse, _suffixes in srd._SCOPE_RULES)
    except Exception as exc:  # noqa: BLE001 -- an unreadable ground truth FAILS
        raise PreflightError(
            f"cannot read silent_rule_detector._SCOPE_RULES ({exc!r}) -- refusing to judge "
            "a do-not-touch claim against a scope set this run never read") from exc


def path_in_ratchet_scope(rel: str) -> bool:
    """Is this path in ratchet scope? Answered by the DETECTOR'S OWN PREDICATE.

    Not by matching the leading directory (terra HIGH, this arc). The roots carry SUFFIX and
    DEPTH rules the root name alone does not: `ecosystem/` admits only `*.yaml` at depth 2,
    so `ecosystem/README.md` is NOT in scope and flagging it is a false refusal, while
    `templates/` recurses and `templates/claude-regions/x.md` IS. "Read the detector, do not
    restate it" applies to its PREDICATE, not only to its list of root names.
    """
    try:
        import silent_rule_detector as srd
        return bool(srd._in_scope(rel.replace("\\", "/").lstrip("./")))
    except Exception as exc:  # noqa: BLE001 -- an unreadable ground truth FAILS
        raise PreflightError(
            f"cannot read silent_rule_detector._in_scope ({exc!r}) -- refusing to judge a "
            "write-scope against a scope predicate this run never ran") from exc



# --- predicate (vi): a DECLARED INPUT that is an in-repo artifact must OPEN -----------------

#: The declared-input fields, a superset of `_INPUT_CLAUSE_RE`'s: that leg asks whether a clause
#: carries a locator AT ALL, this one asks whether the locator it carries RESOLVES. `Consumed
#: by` and `refs` are added because they are how the audit corpus and the backlog rows declare a
#: consumed artifact, and they were outside the earlier leg's vocabulary.
_CONSUMED_CLAUSE_RE = re.compile(
    r"^ {0,3}[-*]?[ ]?\*{0,2}(?P<field>Basis|Inputs?|Reads|Reads from|Fixture|"
    r"Source artifact|Prior art|Depends on|Consumed by|Consumes|refs)\*{0,2}"
    r"\s*:\*{0,2}[ \t]*(?P<body>\S.*)$", re.M | re.I)

#: A backticked token inside such a clause. Judged only if it looks like an in-repo PATH:
#: it carries a `/`, and it either has a file extension or ends in `/` (a directory, which is how
#: this corpus names a launch-contracts folder).
_CONSUMED_TOKEN_RE = re.compile(r"`([^`\n]+)`")
_CONSUMED_SHAPE_RE = re.compile(r"^[^ ]*/[^ ]*(?:\.[A-Za-z0-9]{1,6}|/)$")
#: `path.md:12` belongs to the file-line leg. Reporting it here too would be one defect with two
#: findings, which is how a report stops being countable.
_LINE_SUFFIX_RE = re.compile(r":\d+$")


def check_consumed_artifacts(text: str, repo_root: Path) -> list[Claim]:
    """Predicate (vi): every in-repo artifact a contract DECLARES as an input exists.

    MEASURED GAP, 2026-09-01. A probe contract citing
    `docs/audits/2026-01-01-technical-DOES-NOT-EXIST.md` beside two real locators reported
    **2/2 locator claim(s) resolved**: `_FILE_LINE_RE` needs a `:line`, `_HEADING_RE` needs a
    heading, and `_OFF_REPO_PATH_RE` only matches paths that LEAVE the repo. An in-repo artifact
    named as an input, with no line number, was invisible to every predicate this module had --
    which is the single most common shape a consumed-artifact citation actually takes.

    SCOPED TO DECLARED INPUTS, AND THE SCOPING IS THE DESIGN. A frozen contract's
    `## Write-scope` names files it is about to CREATE, so a leg that judged every in-repo path
    would refuse every contract this repo freezes -- for naming its own output. Prose that
    mentions a file in passing is not the contract asserting it can open one either. So this
    reads only clauses that DECLARE a dependency. If you say it is an input, it opens.

    Deliberately NOT reported here, each because another leg owns it: an off-repo path
    (`check_off_repo_inputs`), a `path:line` locator (the file-line leg), and a clause carrying
    no locator at all (`check_off_repo_inputs`' C-G shape). One defect, one finding.
    """
    out: list[Claim] = []
    seen: set[str] = set()
    root = Path(repo_root)
    for clause in _CONSUMED_CLAUSE_RE.finditer(text):
        for tok in _CONSUMED_TOKEN_RE.finditer(clause.group("body")):
            raw = tok.group(1).strip()
            if raw in seen or not _CONSUMED_SHAPE_RE.match(raw):
                continue
            if _LINE_SUFFIX_RE.search(raw) or _OFF_REPO_PATH_RE.search(raw):
                continue
            seen.add(raw)
            target = root / raw.rstrip("/")
            ok = target.exists()
            detail = ("resolves in the repo" if ok else
                      f"declared as an input by `{clause.group('field')}:` and NOT present -- "
                      f"a consumed artifact that does not open is a claim, not an input")
            out.append(Claim("consumed-artifact", raw, detail, ok))
    return out


def check_do_not_touch(text: str) -> list[Claim]:
    """Predicate (iv): a declared do-not-touch set, checked against the detector's roots."""
    roots = ratchet_scope_roots()
    out: list[Claim] = []
    claims_untouched = False

    for unit, lineno in claim_units(text):
        if not (_UNTOUCHED_RE.search(unit) and _RATCHET_CTX_RE.search(unit)):
            continue
        claims_untouched = True
        excerpt = unit if len(unit) <= 110 else unit[:107] + "..."
        # The SENTENCE leg names bare roots ("ecosystem/ + code are outside its scope
        # roots"), not files, so the root name is the only thing there is to compare -- and
        # it is compared casefolded, because the detector folds.
        inside = sorted({d.lower() for d in _DIR_TOKEN_RE.findall(unit)
                         if d.lower() in roots})
        if inside:
            out.append(Claim("do-not-touch-scope", f"line {lineno}: {excerpt}",
                             f"claims {', '.join(f'{d}/' for d in inside)} sits outside the "
                             f"ratchet's scope, but silent_rule_detector._SCOPE_RULES makes "
                             f"it a scope root ({', '.join(f'{r}/' for r in roots)}) -- the "
                             f"premise is false, whatever the conclusion", False))
        else:
            out.append(Claim("do-not-touch-scope", f"line {lineno}: {excerpt}",
                             "no scope root claimed outside scope", True))

    if claims_untouched:
        for m in _WRITE_SCOPE_RE.finditer(text):
            body = m.group("body")
            lineno = text.count("\n", 0, m.start()) + 1
            # The WRITE-SCOPE leg names actual PATHS, so it asks the detector's own
            # predicate -- suffix and depth rules included.
            inside = sorted({p for p in _PATH_TOKEN_RE.findall(body)
                             if path_in_ratchet_scope(p)})
            excerpt = body if len(body) <= 90 else body[:87] + "..."
            if inside:
                out.append(Claim("do-not-touch-scope", f"line {lineno}: Write-scope: {excerpt}",
                                 f"the contract claims the ratchet is untouched, but its own "
                                 f"write-scope names {', '.join(inside)}, which "
                                 f"silent_rule_detector._in_scope puts INSIDE ratchet scope",
                                 False))
            else:
                out.append(Claim("do-not-touch-scope",
                                 f"line {lineno}: Write-scope: {excerpt}",
                                 "write-scope is clear of the ratchet's scope roots", True))
    return out


def check_open_batch(repo_root: Path) -> list[Claim]:
    """Predicate (v): a batch is OPEN at freeze, or the first lane does not dispatch.

    RULED 2026-08-29 by the operator, and the ruling names the failure it prevents. A batch
    manifest is authored AT DISPATCH carrying `closed_by:`, which names the end-of-batch packet
    path; the pair *committed manifest + absent `closed_by` target* IS the open state, per
    `batch_manifest`'s own design. There are no mutable status flags: a `status:` line is
    documentation for humans, and `batch_manifest` does not read it.

    WHY THIS SITS AT FREEZE. Before this predicate, an inert manifest -- one carrying no
    `closed_by:`, which "opens nothing at all" in the module's own words -- produced no signal at
    all. Its only symptom was that lane merges silently got NO ADR-110 exemption, which surfaces
    much later as a `journal_spine_anchor` FAIL on a merge that looks like it should have been
    covered. Witnessed 2026-08-29 on batch D: the integrator wrote a manifest with `status: open`
    and no `closed_by:`, believed the exemption armed, and misdiagnosed the consequence THREE
    times -- twice as an anchoring mistake to repair, once as a per-lane status rule that does not
    exist -- before reading the predicate. A loud stop at freeze costs one line; the silent
    version cost three misdiagnoses.

    Unresolvable state (the module is absent or raises) is reported as a FAILED claim, never as a
    pass: a predicate that cannot answer has not answered.
    """
    try:
        from batch_manifest import open_batches            # noqa: PLC0415
    except ImportError:
        try:
            from scripts.batch_manifest import open_batches  # type: ignore  # noqa: PLC0415
        except ImportError as exc:
            return [Claim("open-batch", "batch_manifest",
                          f"did not import ({exc}) -- the freeze cannot tell whether a batch "
                          f"is open, and an unanswerable predicate is not a pass", False)]
    try:
        found = open_batches(Path(repo_root))
    except Exception as exc:                                # noqa: BLE001
        return [Claim("open-batch", "open_batches()",
                      f"raised {type(exc).__name__}: {exc}", False)]
    if found:
        names = ", ".join(sorted(Path(b.path).name for b in found))
        return [Claim("open-batch", names,
                      "a committed manifest declares an OPEN batch", True)]
    return [Claim("open-batch", "open_batches() -> []",
                  "NO committed manifest declares an open batch, so the ADR-110 exemption is "
                  "not armed and every lane merge in this batch would need its own JOURNAL "
                  "anchor. Author the manifest AT DISPATCH with a `closed_by:` naming the "
                  "end-of-batch packet path -- a manifest carrying no `closed_by:` opens "
                  "nothing at all, and a `status:` line is read by nothing", False)]


def freeze_predicates(contract: Path, repo_root: Path = _REPO_ROOT) -> Report:
    """All four freeze-time predicates over ONE contract file.

    Every predicate reports every finding -- a contract with two defects is told about both,
    the posture `validate_contract` and `parse_contract` already take at layers 1 and 2.
    """
    try:
        text = Path(contract).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise PreflightError(f"cannot read contract {contract}: {exc!r}") from exc

    report = Report(label="freeze-time predicate")
    report.checked.extend(check_off_repo_inputs(text))
    report.checked.extend(check_consumed_artifacts(text, Path(repo_root)))
    report.checked.extend(check_witnessed_claims(text))
    report.checked.extend(check_cited_ids(text, Path(repo_root)))
    report.checked.extend(check_do_not_touch(text))
    report.checked.extend(check_open_batch(Path(repo_root)))
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="preflight_contract",
                                 description="Verify the repo locators a contract cites.")
    ap.add_argument("contract", help="contract/prompt file to verify")
    ap.add_argument("--repo-root", default=str(_REPO_ROOT), help="repo to verify against")
    ap.add_argument("--freeze", action="store_true",
                    help="also run the five freeze-time predicates ([#591] extension): "
                         "off-repo input existence, witness-carrying claims, live id "
                         "resolution, do-not-touch vs detector scope roots")
    ap.add_argument("--predicates-only", action="store_true",
                    help="run ONLY the freeze-time predicates, skipping the locator legs")
    args = ap.parse_args(sys.argv[1:] if argv is None else argv)

    # The freeze-time predicates QUOTE contract prose back at the reader, and this corpus
    # writes em dashes, arrows and `≠` freely. On a cp1252 console that is an
    # UnicodeEncodeError at print time -- i.e. the tool crashes on exactly the contracts it
    # is for, and a crash is indistinguishable from an internal error. Re-encode rather than
    # demanding `PYTHONUTF8=1` at every call site; `errors="replace"` keeps a stray
    # unencodable byte from ever being the reason a refusal goes unreported.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except (AttributeError, ValueError, OSError):
            pass

    reports: list[Report] = []
    try:
        if not args.predicates_only:
            reports.append(verify(Path(args.contract), Path(args.repo_root)))
        if args.freeze or args.predicates_only:
            reports.append(freeze_predicates(Path(args.contract), Path(args.repo_root)))
    except PreflightError as exc:
        print(f"preflight_contract: INTERNAL ERROR: {exc} -- refusing to report clean; "
              "an error is never a silent pass", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 -- fail CLOSED, the check_seal_identity posture
        print(f"preflight_contract: INTERNAL ERROR: {exc!r} -- refusing to report clean",
              file=sys.stderr)
        return 2

    for report in reports:
        print(report.render())
    return 1 if any(r.failed for r in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
