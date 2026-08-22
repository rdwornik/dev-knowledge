#!/usr/bin/env python3
"""No-pack sandbox guard for the C1 seeded-defect A/B — [#562].

WHY THIS EXISTS
---------------
The 2026-08-20 Grok 4.6 run (`docs/audits/2026-08-20-technical-grok-ab-results-2.md` §6)
scored two of fourteen items against a tree that contained the pack's own answer key.
`docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md` is a tracked file: it carries,
per item, the prompt AND the ground truth AND the PASS-iff clause. The candidate grepped it
(C1-R4: printed pack lines 180-230; C1-N2: printed the first 50 000 characters, i.e. the whole
file). A rerun over a tree that still contains its own answer key measures nothing.

WHAT THE GUARD GUARANTEES, AND WHAT IT DOES NOT
-----------------------------------------------
Guaranteed, and proven by `probe()` rather than asserted:
  * The sandbox WORKING TREE contains zero answer-key bytes. This is a mechanical
    postcondition of provisioning (`Sandbox.postcondition_clean`), not a curation claim:
    after the curated Class-A removals, the whole tree is re-scanned and any remaining
    canary-bearing line is redacted, then re-scanned again and asserted empty.
  * A command that NAMES a stripped artifact is refused before it executes (Layer A).
  * A command whose OUTPUT carries answer-key content is refused after it executes but
    before the model sees it (Layer B). This is the leg that covers git history: the blobs
    stay reachable by sha (they must - the items ask about those shas), so a path-only
    guard would be defeated by `git show <sha>:<pack>` or `git log -p`.

NOT guaranteed - stated here because a guard whose limits are unstated is a worse guard:
  * This is an ACCIDENT boundary, not an adversarial-security boundary. A model that
    deliberately exfiltrates in chunks, base64s, or reverses the bytes defeats Layer B's
    literal matching. The failure mode being prevented is "a model greps and finds", which
    is the failure mode that actually happened.
  * A refusal is itself information: the model learns a guard exists. The refusal text is
    deliberately neutral (it never names the canary that tripped or the artifact) but the
    existence signal cannot be removed.
  * Layer A/B do not stop a model from reasoning correctly about the repo. They are not a
    difficulty knob; every item stays answerable from the substrate the pack intends.

USAGE (the seam the candidate transport calls)
----------------------------------------------
    export NOPACK_SANDBOX_ROOT=/tmp/nopack-sandboxes      # or pass --sandbox-root
    python3 scripts/nopack_sandbox.py provision --dest "$NOPACK_SANDBOX_ROOT/ab"
    python3 scripts/nopack_sandbox.py probe    --sandbox "$NOPACK_SANDBOX_ROOT/ab"
    python3 scripts/nopack_sandbox.py exec     --sandbox "$NOPACK_SANDBOX_ROOT/ab" -- 'git log --oneline -3'
    python3 scripts/nopack_sandbox.py teardown --sandbox "$NOPACK_SANDBOX_ROOT/ab"

`exec` is the whole integration surface: whatever transport runs the candidate (direct API
with a `run` tool, or a CLI lane) calls it, so both lanes are guarded by one mechanism and
neither lane's guard can drift from the other's.

EXECUTION POSTURE (see `parse_pipeline`)
----------------------------------------
`exec` never spawns a shell. A command is lexed into literal argv, split into pipeline
stages on `|`, and each stage is run with `shell=False`. Command substitution, backticks
and variable expansion therefore have no meaning rather than being screened for: `cat
$(touch f)` hands `cat` two filenames and creates nothing. The cost is stated where it is
incurred - shell loops, conditionals and `;`/`&&` chains are refused, not interpreted, so
a multi-command shape is issued one `exec` call at a time.

DESTRUCTION POSTURE (see the "Provenance" section)
--------------------------------------------------
`teardown` deletes a tree, so it is the one operation here that can destroy work that is
not its own. It refuses unless BOTH hold, never either:

  1. the RESOLVED path (symlinks followed first) is a strict descendant of the configured
     sandbox root - `--sandbox-root`, else `$NOPACK_SANDBOX_ROOT`, else
     `<tempdir>/nopack-sandboxes`; and
  2. that path carries a provisioning MARKER (`.git/nopack/marker.json`) whose per-run
     nonce is well formed and whose recorded `sandbox` field names that same resolved
     path - so a marker copied out of a real sandbox does not launder an unrelated
     directory, and a real checkout that lands inside the root by typo has no marker at
     all.
"""

from __future__ import annotations

import argparse
import fnmatch
import glob
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------------------
# Canaries - the content that must never reach a candidate model
# --------------------------------------------------------------------------------------

# Each canary is (id, compiled pattern, why it is here). The ids are reported on a trip so
# a run record can say WHICH class leaked without reproducing the leaked bytes.
_CANARY_SPECS: tuple[tuple[str, str, str], ...] = (
    (
        "item-id",
        r"\bC1-(?:R[1-5]|K[1-3]|X[1-4]|N[1-3])\b",
        "a pack item identifier - only the pack, its results docs and the row that cites "
        "them use this namespace, so any output carrying one is answer-key adjacent",
    ),
    (
        "pack-title",
        r"seeded-defect acceptance pack",
        "the pack's own title line",
    ),
    (
        "pass-iff",
        r"PASS iff",
        "the pack's per-item scoring clause marker",
    ),
    (
        "admit-iff",
        r"ADMIT iff",
        "the acceptance-bar conjunction (G1 and G2 and G3)",
    ),
    (
        "ground-truth",
        r"Ground truth",
        "the pack's per-item answer-key header",
    ),
    (
        "answer-key",
        r"answer[- ]key",
        "prose naming the key itself",
    ),
    (
        "fabrication-trap",
        r"fabrication trap",
        "names C1-R4/C1-R5 as traps, which is a hint even without the answers",
    ),
    (
        "contamination-probe",
        r"contamination probe",
        "names C1-X4/C1-R3 as probes",
    ),
    (
        "gate-arithmetic",
        r"Phi_[ci]\b|\bP_[ci]\b",
        "the scoring symbols used by the acceptance bar",
    ),
    (
        "refusal-hint",
        r"refusal is tested|refusal item|role gate",
        "reveals that declining is the correct response on the N items",
    ),
    (
        "acceptance-run",
        r"model-acceptance|fan-out candidacy|trajectory-inclusive|G[123] (?:failure|gate|pass)",
        "prose describing the acceptance run itself - tells a lane it is being measured",
    ),
    (
        "gate-conjunction",
        r"G1\s*(?:∧|and|AND|&&|\+)\s*G2",
        "the admission conjunction - names the bar without naming an item",
    ),
)

CANARIES: tuple[tuple[str, re.Pattern[str], str], ...] = tuple(
    (cid, re.compile(pat, re.IGNORECASE if cid in {"pack-title", "answer-key", "refusal-hint"} else 0), why)
    for cid, pat, why in _CANARY_SPECS
)

# Curated Class-A seed: whole files that are removed from the sandbox tree even when their
# canary density is low, because the FILE is an instrument artifact. The mechanical sweep
# below does not replace this list - it backstops it.
CLASS_A_GLOBS: tuple[str, ...] = (
    "docs/audits/*c1-seeded-defect*.md",
    "docs/audits/*c1-seeded-defects-contract*.md",
    "docs/audits/*-ab-results*.md",
    "docs/audits/*-ab-lane-contract*.md",
    "docs/audits/*grok-shadow-ab*.md",
    "docs/audits/*c-lanes-consolidated*.md",
    "docs/audits/*final-integrator-contract*.md",
    "docs/audits/*transcription-seat-contract*.md",
    "docs/audits/*annotation-and-rulings-ledger*.md",
    "docs/audits/*admission-rerun*.md",
    "docs/audits/*cloud-c1-brief*.md",
    "docs/handoffs/2026-08-20-dev-knowledge-architect*/*",
    "tasks/491-*.md",
    "tasks/492-*.md",
    "tasks/562-*.md",
)

# A file this many canary-bearing LINES deep is escalated from redaction to whole-file
# removal even if no curated glob names it. This is what keeps the guard correct when a
# NEW answer-key artifact lands that nobody thought to add to CLASS_A_GLOBS.
#
# Lines, not occurrences: this fleet's prose is one-paragraph-per-line, so a single
# BACKLOG row cites five item ids on one line. Counting occurrences escalated BACKLOG.md
# and LESSONS.md - two append-only living records - to deletion over one row each, which
# strips legitimate substrate to remove a leak that a single redaction closes.
DENSITY_ESCALATION = 5

# ...or this share of its own non-blank lines, which catches a SHORT dense artifact that
# never reaches the absolute count.
DENSITY_SHARE = 0.25

# Spine files are redacted, never escalated to removal, even when dense. Their ABSENCE is a
# louder signal than a redaction inside them, they are the lane's legitimate substrate
# (C1-N1 adjudicates against CLAUDE.md; C1-R3 against its section 12), and none of them is
# an instrument artifact. Measured: adding the `acceptance-run` canary pushed
# `protocols/STANDING_RULINGS.md` over the density line and deleted the repo's whole
# standing-rulings register to close three bullets.
NEVER_REMOVE: tuple[str, ...] = (
    "CLAUDE.md",
    "ARCHITECTURE.md",
    "VISION.md",
    "BACKLOG.md",
    "LESSONS.md",
    "JOURNAL.md",
    "pyproject.toml",
    "protocols/*.md",
    "docs/decisions/*.md",
    "docs/audits/README.md",
)

REDACTION_MARKER = "[redacted: no-pack sandbox guard]"

REFUSAL_TEXT = (
    "sandbox guard: refused. This command is outside the read surface available to this "
    "lane. Re-issue a narrower query against the repository."
)

REFUSAL_EXIT = 126

# --------------------------------------------------------------------------------------
# Read-only shell posture (the D4 shape of the 2026-08-20 run, kept so the two lanes stay
# comparable). Secondary to the contamination guard, and deliberately modest.
# --------------------------------------------------------------------------------------

ALLOWED_ARGV0: frozenset[str] = frozenset(
    {
        "awk", "basename", "cat", "comm", "cut", "diff", "dirname", "echo", "file", "find",
        "git", "grep", "head", "ls", "md5sum", "nl", "printf", "python", "python3", "rg",
        "sed", "sha256sum", "sort", "stat", "tail", "test", "tr", "uniq", "wc", "xargs",
    }
)

_GIT_WRITE_SUBCOMMANDS: frozenset[str] = frozenset(
    {
        "add", "am", "apply", "branch", "checkout", "cherry-pick", "clean", "clone", "commit",
        "config", "fetch", "filter-branch", "gc", "init", "merge", "mv", "notes", "prune",
        "pull", "push", "rebase", "reset", "restore", "revert", "rm", "stash", "switch",
        "tag", "update-ref", "worktree",
    }
)

# A markdown line that OPENS a block. Redaction stops at these, so a canary inside one
# list item never eats its neighbours - measured: extending to every contiguous non-blank
# line took 318 lines out of `docs/audits/README.md`, which is one long list.
_BLOCK_START = re.compile(r"^\s{0,3}(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|>|\||```|~~~)")

_GIT_LISTING_WHEN_BARE: frozenset[str] = frozenset({"branch", "tag", "config", "stash", "worktree"})

_FENCE_LINE = re.compile(r"^\s{0,3}(?:```|~~~)")

DEVNULL = "/dev/null"

# Characters that make a token a glob. Expansion is done in-process against the sandbox
# (see `_expand_globs`) because there is no shell left to do it.
_GLOB_CHARS = frozenset("*?[")

# Tokens that would ask a shell to run a SECOND command. There is no shell, so rather than
# hand them to a program as literal arguments - which reads as success and silently does
# the wrong thing - they are refused.
_SEPARATOR_TOKENS = frozenset({";", "&", "&&", "||", ";;", "|&"})
_SEPARATOR_CHARS = frozenset(";&|")

# Shell keywords. Checked at argv0 only: `cat do` is a file called `do`, and refusing that
# would be a false positive of exactly the kind the first allowlist was measured for.
_SHELL_KEYWORDS = frozenset(
    {
        "for", "while", "until", "if", "then", "else", "elif", "fi", "do", "done", "case",
        "esac", "select", "function", "time", "coproc", "{", "}", "(", ")", "((", "[[",
        "!", ".", "source", "eval", "exec", "export", "alias", "set", "unset", "trap",
    }
)


# --------------------------------------------------------------------------------------
# Scanning
# --------------------------------------------------------------------------------------


def scan_text(text: str) -> list[str]:
    """Return the ids of every canary present in `text`, in declaration order."""
    return [cid for cid, pattern, _why in CANARIES if pattern.search(text)]


def scan_lines(text: str) -> list[int]:
    """Return the 0-based indexes of lines carrying at least one canary."""
    return [i for i, line in enumerate(text.splitlines()) if scan_text(line)]


_PROSE_SUFFIXES = frozenset({".md", ".txt", ".rst"})


def _is_prose(rel: str) -> bool:
    """True for files where line-replacement redaction is a meaningful, non-corrupting edit."""
    return any(rel.endswith(suffix) for suffix in _PROSE_SUFFIXES)


def _is_probably_text(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return False
    return b"\x00" not in chunk


def scan_tree(root: Path, skip: tuple[str, ...] = (".git",)) -> dict[str, list[str]]:
    """Map repo-relative path -> canary ids, for every text file under `root`.

    This is the completeness leg. It is what lets provisioning assert a postcondition
    rather than trust a curated list.
    """
    hits: dict[str, list[str]] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(root).as_posix()
        if any(rel == s or rel.startswith(f"{s}/") for s in skip):
            continue
        if not _is_probably_text(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeDecodeError):
            continue
        found = scan_text(text)
        if found:
            hits[rel] = found
    return hits


def redact(text: str, extra_terms: tuple[str, ...] = ()) -> tuple[str, int]:
    """Redact every canary-bearing PARAGRAPH, returning (new_text, lines_redacted).

    Paragraph, not line, because line-level redaction leaves the sentences AROUND the
    canary standing - and in this fleet's prose those sentences carry the leak. Measured
    on `protocols/STANDING_RULINGS.md`: redacting the one line that matched left the
    preceding line, which states the admission conjunction, fully readable.
    """
    lines = text.splitlines(keepends=True)
    marked = {
        i
        for i, line in enumerate(lines)
        if scan_text(line) or any(term in line for term in extra_terms)
    }
    if not marked:
        return text, 0
    doomed: set[int] = set()
    for idx in marked:
        start = idx
        while start > 0 and not _BLOCK_START.match(lines[start]) and lines[start - 1].strip():
            start -= 1
        end = idx
        while (
            end + 1 < len(lines)
            and lines[end + 1].strip()
            and not _BLOCK_START.match(lines[end + 1])
        ):
            end += 1
        doomed.update(range(start, end + 1))
    # Never replace a fence delimiter: a canary inside a fenced block would otherwise take
    # the opening ``` with it and leave the document with an unbalanced fence - which is
    # the fence-corruption defect class (substrate inventory section 2.4) that this repo
    # already has a rewriting hook for. The guard must not manufacture one.
    doomed = {i for i in doomed if not _FENCE_LINE.match(lines[i])}
    for idx in sorted(doomed):
        newline = "\n" if lines[idx].endswith("\n") else ""
        lines[idx] = f"{REDACTION_MARKER}{newline}"
    # Line-preserving on purpose: redaction replaces in place and NEVER deletes, so every
    # line number in a redacted file still resolves. An earlier draft collapsed runs of
    # markers and shifted the substrate inventory from 428 lines to 424 - which would have
    # made the guard a generator of exactly the stale-locator class the pack is built from.
    return "".join(lines), len(doomed)


def is_dense(text: str) -> bool:
    """True when a file reads as an instrument artifact rather than a record that mentions one."""
    hit_lines = len(scan_lines(text))
    if hit_lines >= DENSITY_ESCALATION:
        return True
    if hit_lines < 2:
        # One leaking line is a record that mentions the instrument, never the instrument -
        # and on a short file the share rule alone would escalate exactly that case.
        return False
    non_blank = sum(1 for line in text.splitlines() if line.strip())
    return bool(non_blank) and (hit_lines / non_blank) >= DENSITY_SHARE


# --------------------------------------------------------------------------------------
# Provenance - what makes a directory provably OURS before anything deletes it
#
# The first draft of this file reached `shutil.rmtree(path)` from the CLI guarded only by
# `path.exists()`. A typo in `--sandbox`, or a path pointing at a real checkout or a synced
# directory, destroyed it. That is the hazard class this fleet's own P0 exclusion rules
# exist for - the recorded history is cleanup scripts that deleted personal files alongside
# their intended targets - so the repair is a positive proof of ownership, not a blocklist.
# --------------------------------------------------------------------------------------

# Both live under `.git/` on purpose. That directory is created by our own `git clone`, so
# nothing of anyone else's can already be sitting there; `scan_tree` skips it, so the
# manifest's list of stripped paths cannot fail provisioning's own postcondition; and
# `git status` / `git ls-files` never surface it, so the sandbox working tree stays clean
# (run-protocol P4). Storing the manifest OUTSIDE the sandbox - the first draft wrote
# `<dest parent>/sandbox-manifest.json` unconditionally - silently destroyed whatever
# unrelated file happened to hold that name.
SANDBOX_META_DIR = ".git/nopack"
MARKER_RELPATH = f"{SANDBOX_META_DIR}/marker.json"
MANIFEST_RELPATH = f"{SANDBOX_META_DIR}/manifest.json"

# The marker's self-identifying kind string. A JSON file that happens to exist at the
# marker path but does not carry this is not a marker.
MARKER_KIND = "nopack-sandbox"

# 128 bits of per-run nonce. Its job is not secrecy - anyone who can read the sandbox can
# read it - but IDENTITY: it lets a caller that holds a Sandbox (or its manifest) assert
# that the directory in front of it is the one THIS run provisioned, and not a different
# sandbox that happens to sit in the same root.
_NONCE_BYTES = 16
_NONCE_RE = re.compile(r"\A[0-9a-f]{32}\Z")

ENV_SANDBOX_ROOT = "NOPACK_SANDBOX_ROOT"


class TeardownRefused(RuntimeError):
    """`teardown` was handed a path it could not prove it provisioned."""


def default_sandbox_root() -> Path:
    """The configured sandbox root: `$NOPACK_SANDBOX_ROOT`, else `<tempdir>/nopack-sandboxes`.

    Deliberately NOT the repo, the cwd, or a caller-supplied parent: the root is the outer
    containment boundary, and a boundary that moves with the caller is not one.
    """
    env = os.environ.get(ENV_SANDBOX_ROOT, "").strip()
    return Path(env) if env else Path(tempfile.gettempdir()) / "nopack-sandboxes"


def _resolve(path: Path | str) -> Path:
    """Fully resolve a path - symlinks INCLUDED - so every comparison is on real targets.

    This is the leg that stops a symlink escape: `<root>/link -> /real/checkout` resolves
    to `/real/checkout`, which is not inside the root, so containment refuses it. Comparing
    the un-resolved string would have compared `<root>/link` and passed.
    """
    return Path(path).expanduser().resolve()


def _is_contained(resolved: Path, root: Path) -> bool:
    """True when `resolved` is a STRICT descendant of `root`. The root itself is not."""
    return resolved != root and root in resolved.parents


def read_marker(sandbox_path: Path) -> dict[str, object] | None:
    """Return the provisioning marker at `sandbox_path`, or None if it is absent/invalid.

    "Invalid" is anything that is not a marker this tool wrote FOR THIS DIRECTORY: wrong
    kind, malformed nonce, unparseable JSON, or a `sandbox` field naming somewhere else.
    That last check is what keeps a marker from being laundered - copying one out of a real
    sandbox into an unrelated tree does not make that tree deletable.
    """
    marker_file = Path(sandbox_path) / MARKER_RELPATH
    if not marker_file.is_file():
        return None
    try:
        data = json.loads(marker_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or data.get("marker") != MARKER_KIND:
        return None
    nonce = data.get("nonce")
    if not isinstance(nonce, str) or not _NONCE_RE.fullmatch(nonce):
        return None
    claimed = data.get("sandbox")
    if not isinstance(claimed, str) or _resolve(claimed) != _resolve(sandbox_path):
        return None
    return data


def write_marker(sandbox_path: Path, nonce: str, sandbox_root: Path) -> Path:
    """Write the provisioning marker. Exclusive creation - never clobbers."""
    marker_file = Path(sandbox_path) / MARKER_RELPATH
    marker_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "marker": MARKER_KIND,
        "nonce": nonce,
        "sandbox": str(_resolve(sandbox_path)),
        "sandbox_root": str(_resolve(sandbox_root)),
    }
    with open(marker_file, "x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    return marker_file


def _force_writable(func, path, _exc) -> None:
    """rmtree error hook: clear the read-only bit and retry once.

    Git marks the files under `.git/objects` read-only. On Windows `shutil.rmtree` cannot
    unlink a read-only file, so teardown raised `PermissionError` on every sandbox it had
    itself provisioned - a no-leftovers organ that could not remove its own leftovers.
    """
    try:
        os.chmod(path, stat.S_IWRITE)
    except OSError:
        raise
    func(path)


def _rmtree_force(path: Path) -> None:
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=_force_writable)
    else:  # pragma: no cover - the fleet floor is 3.12
        shutil.rmtree(path, onerror=_force_writable)


# --------------------------------------------------------------------------------------
# Provisioning
# --------------------------------------------------------------------------------------


@dataclass
class Sandbox:
    """A provisioned no-pack sandbox and the record of what was done to it."""

    path: Path
    source: Path
    head: str
    strip_commit: str
    removed: list[str] = field(default_factory=list)
    redacted: dict[str, int] = field(default_factory=dict)
    postcondition_clean: bool = False
    residual: dict[str, list[str]] = field(default_factory=dict)
    denied: list[str] = field(default_factory=list)
    reference_residual: list[str] = field(default_factory=list)
    # Provenance. `nonce` is empty on a Sandbox rehydrated without a manifest, and
    # `teardown` treats that as "no expectation to check", NOT as "check passed" - the
    # marker and containment legs still both have to hold.
    sandbox_root: Path | None = None
    nonce: str = ""
    marker: str = MARKER_RELPATH

    def denied_names(self) -> set[str]:
        """Every string a command may not mention. Computed at provision time (see `_denied`)."""
        return set(self.denied) if self.denied else {rel for rel in self.removed}

    def manifest(self) -> dict[str, object]:
        return {
            "path": str(self.path),
            "source": str(self.source),
            "head": self.head,
            "strip_commit": self.strip_commit,
            "removed": self.removed,
            "redacted": self.redacted,
            "postcondition_clean": self.postcondition_clean,
            "residual": self.residual,
            "denied": self.denied,
            "reference_residual": self.reference_residual,
            "sandbox_root": None if self.sandbox_root is None else str(self.sandbox_root),
            "nonce": self.nonce,
            "marker": self.marker,
        }


def _denied(removed: list[str], all_tracked: list[str]) -> list[str]:
    """Full paths always; a basename or stem ONLY when it is unique in the tree.

    A handoff bundle's files are `HANDOFF_BOOT.md`, `PROBES.md`, `RESIDUAL.md`,
    `SUPPLEMENT.md`, `PASTE_THIS.md` - names shared by every bundle in the repo. Denying
    the bare basename of a stripped bundle's file would refuse any command that so much as
    lists another bundle, and would refuse the OUTPUT of `ls docs/handoffs/*/` outright.
    Uniqueness is the discriminator: the pack's basename occurs once, `PROBES.md` does not.
    """
    counts: dict[str, int] = {}
    for rel in all_tracked:
        base = rel.rsplit("/", 1)[-1]
        counts[base] = counts.get(base, 0) + 1

    names: set[str] = set()
    for rel in removed:
        names.add(rel)
        base = rel.rsplit("/", 1)[-1]
        if counts.get(base, 0) <= 1:
            names.add(base)
            if base.endswith(".md"):
                names.add(base[:-3])
    return sorted(names)


def _git(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def is_shallow(repo: Path) -> bool:
    return _git(repo, "rev-parse", "--is-shallow-repository").strip() == "true"


def provision(
    source: Path,
    dest: Path,
    head: str = "HEAD",
    *,
    allow_shallow: bool = False,
    class_a_globs: tuple[str, ...] = CLASS_A_GLOBS,
    sandbox_root: Path | str | None = None,
) -> Sandbox:
    """Clone `source` at `head` into `dest` and strip every answer-key byte from the tree.

    `dest` must be a strict descendant of the configured sandbox root (see
    `default_sandbox_root`): provisioning and teardown share one containment boundary, so
    a sandbox that could not have been provisioned cannot later be presented for deletion.

    Raises RuntimeError if the postcondition (zero canaries in the working tree) does not
    hold, so a broken guard fails loudly at provisioning rather than silently at run time.
    Every failure path after the clone removes the sandbox and verifies the removal - a
    half-provisioned tree is the full unstripped clone, i.e. the answer key on disk, which
    is both a no-leftovers violation (CLAUDE.md section 5 rule 9) and the exact disclosure
    this guard exists to prevent.
    """
    source = source.resolve()
    root = _resolve(sandbox_root) if sandbox_root is not None else _resolve(default_sandbox_root())
    dest = Path(dest)
    if dest.exists():
        raise RuntimeError(f"sandbox destination already exists: {dest}")
    resolved_dest = _resolve(dest)
    if not _is_contained(resolved_dest, root):
        raise RuntimeError(
            f"sandbox destination is outside the configured sandbox root: {resolved_dest} "
            f"is not a strict descendant of {root}. Set {ENV_SANDBOX_ROOT} or pass "
            f"sandbox_root= to move the boundary deliberately."
        )
    if not allow_shallow and is_shallow(source):
        raise RuntimeError(
            "source repository is shallow; the pack's items cite commits outside a shallow "
            "window. Run `git fetch --unshallow` first (pack section 0.1 precedent), or pass "
            "allow_shallow=True for a guard-only probe."
        )

    dest.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["git", "clone", "--local", "--quiet", str(source), str(dest)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        # Nothing to clean: a failed clone that never created `dest` leaves nothing, and
        # one that did is removed by git itself.
        if dest.exists():
            _rmtree_force(resolved_dest)
        raise RuntimeError(f"clone failed: {proc.stderr.strip()}")

    nonce = secrets.token_hex(_NONCE_BYTES)
    try:
        write_marker(dest, nonce, root)
        return _strip_and_seal(source, dest, head, root, nonce, class_a_globs)
    except BaseException:
        _abort_provision(resolved_dest, root, nonce)
        raise


def _abort_provision(resolved_dest: Path, root: Path, nonce: str) -> None:
    """Remove a partially provisioned sandbox, announcing any failure to do so.

    Provenance teardown is tried FIRST, so the ordinary abort path exercises the same
    proof every other caller has to satisfy. The direct fallback exists for one narrow
    window - the marker is written immediately after the clone, so an abort in between has
    no marker to check - and it is safe there for reasons this function can actually
    verify: `provision` established that `resolved_dest` did not exist before this call and
    that it is a strict descendant of `root`, so the tree can only be the one we just made.
    """
    try:
        teardown(resolved_dest, sandbox_root=root, expected_nonce=nonce)
        return
    except TeardownRefused:
        pass
    if _is_contained(resolved_dest, root) and resolved_dest.is_dir():
        try:
            _rmtree_force(resolved_dest)
        except OSError as exc:  # never silent: an unremoved clone is the leftover
            print(f"nopack_sandbox: FAILED to remove {resolved_dest}: {exc}", file=sys.stderr)
    if resolved_dest.exists():
        print(
            f"nopack_sandbox: LEFTOVER - {resolved_dest} survived an aborted provision "
            f"and may contain unstripped content; remove it by hand",
            file=sys.stderr,
        )


def _strip_and_seal(
    source: Path,
    dest: Path,
    head: str,
    root: Path,
    nonce: str,
    class_a_globs: tuple[str, ...],
) -> Sandbox:
    """The stripping passes. Split out of `provision` so every exit here is cleaned up."""
    resolved_head = _git(source, "rev-parse", head).strip()
    _git(dest, "checkout", "--quiet", "--detach", resolved_head)

    removed: list[str] = []
    redacted: dict[str, int] = {}

    # Pass 1 - curated Class A: whole-file removal.
    tracked = _git(dest, "ls-files").splitlines()
    for rel in tracked:
        if any(fnmatch.fnmatch(rel, glob) for glob in class_a_globs):
            target = dest / rel
            if target.exists():
                target.unlink()
                removed.append(rel)

    # Pass 2 - mechanical sweep: dense residue escalates to removal, sparse residue is
    # redacted. This is the leg that does not depend on my curation.
    for rel, _ids in sorted(scan_tree(dest).items()):
        target = dest / rel
        text = target.read_text(encoding="utf-8")
        spine = any(fnmatch.fnmatch(rel, pat) for pat in NEVER_REMOVE)
        # Redaction is a PROSE operation. Replacing a line inside a .json/.yaml/.py file
        # produces a syntactically broken file, and the paragraph rule - which keys on
        # blank lines - has no meaning there. A structured file that carries answer-key
        # content is removed instead; measured on `tasks/manifest.json`, where the sweep
        # would otherwise have marked 1687 of its lines and left invalid JSON behind.
        if (is_dense(text) or not _is_prose(rel)) and not spine:
            target.unlink()
            removed.append(rel)
            continue
        redacted_text, count = redact(text)
        if count:
            target.write_text(redacted_text, encoding="utf-8", newline="\n")
            redacted[rel] = count

    # Pass 3 - reference sweep. A file that merely NAMES a stripped artifact is a live
    # pointer to it: `docs/audits/README.md` still listed every removed artifact by
    # filename, so `cat docs/audits/README.md | head -20` tripped Layer B on a wholly
    # legitimate read. Removing the dangling references makes the tree self-consistent and
    # takes that class of over-refusal off the lane's back.
    denied = tuple(_denied(sorted(removed), tracked))
    for rel in _git(dest, "ls-files").splitlines():
        path = dest / rel
        if not path.is_file() or not _is_prose(rel) or not _is_probably_text(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if not any(term in text for term in denied):
            continue
        new_text, count = redact(text, extra_terms=denied)
        if count:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            redacted[rel] = redacted.get(rel, 0) + count

    # HARD postcondition: no answer-key CONTENT anywhere, in any file type.
    residual = scan_tree(dest)
    # SOFT residual, recorded not fatal: a structured file may still NAME a stripped
    # artifact, because it cannot be redacted without being corrupted. Layer B covers the
    # disclosure; the cost is that reading such a file is refused. Reported, never silent.
    reference_residual = sorted(
        rel
        for rel in _git(dest, "ls-files").splitlines()
        if (dest / rel).is_file()
        and _is_probably_text(dest / rel)
        and any(term in (dest / rel).read_text(encoding="utf-8", errors="ignore") for term in denied)
    )
    for rel in reference_residual:
        if _is_prose(rel):
            residual.setdefault(rel, []).append("stripped-artifact-reference")
    clean = not residual

    _git(dest, "-c", "user.name=sandbox", "-c", "user.email=sandbox@invalid", "add", "-A")
    _git(
        dest,
        "-c",
        "user.name=sandbox",
        "-c",
        "user.email=sandbox@invalid",
        "-c",
        "core.hooksPath=/dev/null",
        "commit",
        "--quiet",
        "--no-verify",
        "-m",
        "chore: lane substrate",
    )
    strip_commit = _git(dest, "rev-parse", "HEAD").strip()

    sandbox = Sandbox(
        path=dest,
        source=source,
        head=resolved_head,
        strip_commit=strip_commit,
        removed=sorted(removed),
        redacted=redacted,
        postcondition_clean=clean,
        residual=residual,
        denied=list(denied),
        reference_residual=reference_residual,
        sandbox_root=root,
        nonce=nonce,
    )
    if not clean:
        # No leftovers, even on abort (CLAUDE.md section 5 rule 9): a sandbox that failed
        # its own postcondition is not evidence worth keeping, and leaving it behind leaves
        # an unguarded checkout on disk. `provision`'s except clause does the removal; the
        # residual list travels in the exception instead.
        raise RuntimeError(
            f"provisioning postcondition FAILED and the sandbox was removed: "
            f"{len(residual)} file(s) still carried canaries: {sorted(residual)[:5]}"
        )
    write_manifest(dest, sandbox.manifest())
    return sandbox


def write_manifest(sandbox_path: Path, manifest: dict[str, object]) -> Path:
    """Persist the run manifest INSIDE the sandbox, by exclusive creation.

    Both legs matter and neither is sufficient alone. Inside, because the first draft wrote
    `<dest parent>/sandbox-manifest.json` - a path the caller does not own and may well
    already be using. Exclusively, because "inside" is an argument about what SHOULD be
    there and `x` mode is the assertion that checks it.
    """
    target = Path(sandbox_path) / MANIFEST_RELPATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "x", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, indent=2)
    return target


def teardown(
    sandbox: Sandbox | Path,
    *,
    sandbox_root: Path | str | None = None,
    expected_nonce: str | None = None,
) -> bool:
    """Remove a sandbox we can PROVE we provisioned, and verify the removal.

    Both checks are required, never either (Done-contract item 1):
      * containment - the resolved path is a strict descendant of the sandbox root; and
      * provenance  - it carries a valid marker for itself, and, when the caller holds one,
        the marker's nonce is the one that run recorded.

    Raises `TeardownRefused` when either fails. Returns True when the tree is gone and that
    absence has been re-checked on disk (CLAUDE.md section 5 rule 9, no leftovers).
    """
    if isinstance(sandbox, Sandbox):
        path: Path = sandbox.path
        if sandbox_root is None:
            sandbox_root = sandbox.sandbox_root
        if expected_nonce is None and sandbox.nonce:
            expected_nonce = sandbox.nonce
    else:
        path = Path(sandbox)

    root = _resolve(sandbox_root) if sandbox_root is not None else _resolve(default_sandbox_root())
    # Resolve BEFORE every comparison. `<root>/link -> /real/checkout` is the escape this
    # closes: unresolved it looks contained, resolved it is plainly outside.
    resolved = _resolve(path)

    if not resolved.exists():
        return True  # idempotent: nothing to remove, and nothing was removed

    if not resolved.is_dir():
        raise TeardownRefused(f"refused: not a directory: {resolved}")
    if not _is_contained(resolved, root):
        raise TeardownRefused(
            f"refused: {resolved} is outside the configured sandbox root {root}"
        )
    marker = read_marker(resolved)
    if marker is None:
        raise TeardownRefused(
            f"refused: {resolved} carries no valid provisioning marker ({MARKER_RELPATH}); "
            f"this tool did not provision it"
        )
    if expected_nonce is not None and marker.get("nonce") != expected_nonce:
        raise TeardownRefused(
            f"refused: {resolved} was provisioned by a different run (nonce mismatch)"
        )

    _rmtree_force(resolved)
    return not resolved.exists()


# --------------------------------------------------------------------------------------
# Layer A - command screening (pre-execution)
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Trip:
    layer: str
    kind: str
    detail: str


class UnsupportedShell(Exception):
    """A command asked for a shell feature this sandbox does not have."""

    def __init__(self, kind: str, detail: str) -> None:
        super().__init__(detail)
        self.kind = kind
        self.detail = detail


@dataclass(frozen=True)
class Stage:
    """One pipeline stage: literal argv, plus which streams the command sent to /dev/null.

    `globbable` runs parallel to `argv` and marks the words whose glob characters arrived
    UNQUOTED. A quoted glob is a literal - `git show <sha> -- '*.md'` hands git a pathspec
    it expands itself - while an unquoted one is ours to expand. Both shapes are the
    instrument's own commands, so conflating them breaks one of them either way.
    """

    argv: tuple[str, ...]
    globbable: tuple[bool, ...]
    drop_stdout: bool = False
    drop_stderr: bool = False


def _lex(command: str) -> list[tuple[str, str]]:
    """Split `command` into (value, unquoted-part) words. Quote-aware, expansion-free.

    `shlex` cannot answer the question this parser actually has, which is not "what are the
    words" but "which characters were quoted". Its POSIX mode strips quotes and forgets;
    its non-POSIX mode keeps them but tokenizes differently, so pairing the two streams
    desynchronises on the ordinary `--format='%h %ad'` shape. So the second element here is
    the word with quoted spans REMOVED, and every structural test - pipe, separator,
    redirect, glob - reads that rather than the value. `grep -n '>' file` is the case that
    forces it: the `>` is data, and a parser that cannot tell refuses a legitimate read.
    """
    words: list[tuple[str, str]] = []
    value: list[str] = []
    bare: list[str] = []
    started = False
    quote: str | None = None
    index = 0
    while index < len(command):
        char = command[index]
        if quote is not None:
            if char == quote:
                quote = None
            elif quote == '"' and char == "\\" and index + 1 < len(command):
                index += 1
                value.append(command[index])
            else:
                value.append(char)
            index += 1
            continue
        if char.isspace():
            if started:
                words.append(("".join(value), "".join(bare)))
                value, bare, started = [], [], False
            index += 1
            continue
        started = True
        if char in ("'", '"'):
            quote = char
        elif char == "\\" and index + 1 < len(command):
            index += 1
            value.append(command[index])  # escaped: literal, and NOT structural
        else:
            value.append(char)
            bare.append(char)
        index += 1
    if quote is not None:
        raise UnsupportedShell("unparseable", "unbalanced quote")
    if started:
        words.append(("".join(value), "".join(bare)))
    return words


def _redirect_split(word: str) -> tuple[str, str] | None:
    """Return (operator, inline target) if `word` begins a redirect, else None."""
    for op in ("2>>", "1>>", "&>>", "2>", "1>", "&>", ">>", ">", "<<", "<"):
        if word.startswith(op):
            return op, word[len(op) :]
    return None


def parse_pipeline(command: str) -> list[Stage]:
    """Lex `command` into pipeline stages of LITERAL argv. No shell is involved, ever.

    WHAT IS SUPPORTED, and it is deliberately the read surface and nothing else: quoting,
    `|` pipelines, unquoted globs, and `>/dev/null` / `2>/dev/null` (which only ever mean
    "discard this stream", never "write a file").

    WHAT IS NOT, stated because a silent capability loss is worse than a loud one:

      * Command substitution, backticks and variable expansion are not INTERPRETED and not
        refused - they have no meaning without a shell, so `cat $(touch f)` hands `cat` two
        filenames, `$(touch` and `f)`, and creates nothing. That inertness is the point of
        the whole change, and it is what the allowlist could never deliver: the previous
        implementation screened top-level shell SEGMENTS and then executed with
        `shell=True`, so a substitution ran a command the allowlist had never seen.
      * Loops, conditionals and `;`/`&&`/`||` chains are REFUSED. This is a real capability
        reduction and it is not hypothetical: the guard's own comments record that C1-K2
        and C1-K3 adjudicate with `for s in <shas>; do git log -1 $s; done`. Those shapes
        must now be issued as one `exec` call per command, which the transport already
        supports because `exec` runs exactly one command at a time. The alternative was to
        keep a shell and screen it, which is the defect.
      * Redirects to anything but `/dev/null` are refused, as they were before. Output is
        captured and returned, so a file redirect could only ever be a write.

    Raises `UnsupportedShell`; callers turn that into a Layer A refusal.
    """
    if "\n" in command or "\r" in command:
        raise UnsupportedShell("shell-construct", "multi-line commands are not available here")
    words = _lex(command)
    if not words:
        raise UnsupportedShell("unparseable", "empty command")

    stages: list[Stage] = []
    argv: list[str] = []
    globbable: list[bool] = []
    drop_stdout = False
    drop_stderr = False

    def flush() -> None:
        nonlocal argv, globbable, drop_stdout, drop_stderr
        if not argv:
            raise UnsupportedShell("shell-construct", "empty pipeline stage")
        stages.append(Stage(tuple(argv), tuple(globbable), drop_stdout, drop_stderr))
        argv, globbable = [], []
        drop_stdout = drop_stderr = False

    index = 0
    while index < len(words):
        value, bare = words[index]
        index += 1

        if bare == "|" and value == "|":
            flush()
            continue
        if bare in _SEPARATOR_TOKENS or _SEPARATOR_CHARS.intersection(bare):
            # Includes the embedded case: `cat a; rm -rf b` lexes `a;` as one word. With no
            # shell the second command could never run, but handing `a;` to `cat` as a
            # filename reads as success while doing something else entirely.
            raise UnsupportedShell(
                "shell-construct",
                f"'{value}' chains commands; issue one command per call",
            )

        redirect = _redirect_split(bare)
        if redirect is not None:
            operator, inline = redirect
            target = inline
            if not target:
                if index >= len(words):
                    raise UnsupportedShell("redirect", "redirect with no target")
                target = words[index][0]
                index += 1
            if operator.startswith("<") or target != DEVNULL:
                raise UnsupportedShell("redirect", f"redirect to {target} is not permitted")
            if operator.startswith("2"):
                drop_stderr = True
            elif operator.startswith("&"):
                drop_stdout = drop_stderr = True
            else:
                drop_stdout = True
            continue

        argv.append(value)
        globbable.append(bool(_GLOB_CHARS.intersection(bare)))

    flush()
    return stages


def _screen_words(text: str, denied_names: set[str]) -> Trip | None:
    """The two content checks, applied to a command string or to expanded argv."""
    for name in sorted(denied_names, key=len, reverse=True):
        if name and name in text:
            return Trip("A", "stripped-artifact-path", f"command names a stripped artifact ({name})")
    for cid, pattern, _why in CANARIES:
        if pattern.search(text):
            return Trip("A", "canary-in-command", f"command carries canary '{cid}'")
    return None


def screen_pipeline(
    command: str, denied_names: set[str] | None = None
) -> tuple[Trip | None, list[Stage]]:
    """Screen a command and, when it may proceed, hand back the parsed stages.

    One parse, one screen: `run_guarded` executes exactly the stages that were screened,
    so there is no window in which the string that was checked and the string that runs can
    differ. Under `shell=True` that window was the whole defect.
    """
    denied_names = denied_names or set()

    trip = _screen_words(command, denied_names)
    if trip is not None:
        return trip, []

    try:
        stages = parse_pipeline(command)
    except UnsupportedShell as exc:
        return Trip("A", exc.kind, exc.detail), []

    for stage in stages:
        argv0 = stage.argv[0].rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        if argv0 in _SHELL_KEYWORDS:
            return (
                Trip("A", "shell-construct", f"'{argv0}' is a shell construct, not a command"),
                [],
            )
        if argv0 not in ALLOWED_ARGV0:
            return Trip("A", "argv0-not-allowed", f"'{argv0}' is not in the read-only allowlist"), []
        if argv0 == "git":
            # Real argv now, not a regex over a segment: `git commit` is refused because
            # `commit` IS the first non-flag argument, not because a pattern happened to
            # match it somewhere in the string.
            tokens = [t for t in stage.argv[1:] if not t.startswith("-")]
            if tokens and tokens[0] in _GIT_WRITE_SUBCOMMANDS:
                # `git branch -a`, `git tag`, `git config --list` and `git stash` with no
                # operand are LISTING commands. Refusing them was a measured false
                # positive on `git branch -a`; an operand (or a mutating flag, which
                # always takes one) is what makes them writes.
                if tokens[0] in _GIT_LISTING_WHEN_BARE and len(tokens) == 1:
                    continue
                return Trip("A", "git-write", f"git {tokens[0]} mutates state"), []
    return None, stages


def screen_command(command: str, denied_names: set[str] | None = None) -> Trip | None:
    """Refuse a command before it runs. Returns None when the command may proceed."""
    return screen_pipeline(command, denied_names)[0]


def _expand_globs(stage: Stage, cwd: Path) -> list[str]:
    """Expand unquoted globs against the sandbox. No shell, so this is ours to do.

    Unmatched patterns are passed through literally, which is bash's default (nullglob off)
    and is what keeps `git show <sha> -- 'docs/**'` working when nothing matches.
    """
    expanded: list[str] = []
    for word, globbable in zip(stage.argv, stage.globbable):
        if not globbable:
            expanded.append(word)
            continue
        matches = sorted(glob.glob(word, root_dir=str(cwd)))
        expanded.extend(matches if matches else [word])
    return expanded


# --------------------------------------------------------------------------------------
# Layer B - output screening (post-execution, pre-delivery)
# --------------------------------------------------------------------------------------


def screen_output(text: str, denied_names: set[str] | None = None) -> Trip | None:
    """Refuse an output that carries answer-key content. This is the git-history leg.

    Path screening is on this layer as well as on Layer A, and it is not redundant: a
    command that never names a stripped artifact can still PRINT its name. `git show <sha>
    --stat` is the case that found this - it lists the pack's path without the command ever
    mentioning it, which hands the model the exact string it needs to go looking.
    """
    for name in sorted(denied_names or set(), key=len, reverse=True):
        if name and name in text:
            return Trip("B", "stripped-artifact-path-in-output", "output names a stripped artifact")
    found = scan_text(text)
    if found:
        return Trip("B", "canary-in-output", f"output carries canary(s) {','.join(found)}")
    return None


@dataclass
class GuardedResult:
    command: str
    returncode: int
    stdout: str
    stderr: str
    refused: bool
    trip: Trip | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "command": self.command,
            "returncode": self.returncode,
            "refused": self.refused,
            "trip": None if self.trip is None else {"layer": self.trip.layer, "kind": self.trip.kind},
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


def run_guarded(
    command: str,
    sandbox: Sandbox | Path,
    *,
    denied_names: set[str] | None = None,
    timeout: int = 120,
    max_output_bytes: int = 100_000,
) -> GuardedResult:
    """Run one command inside the sandbox, with both guard layers applied and NO shell.

    Every stage is executed with `shell=False` from an argv list that was itself screened,
    so nothing between the check and the exec can reinterpret the string.
    """
    if isinstance(sandbox, Sandbox):
        cwd = sandbox.path
        names = denied_names if denied_names is not None else sandbox.denied_names()
    else:
        cwd = Path(sandbox)
        names = denied_names or set()

    trip, stages = screen_pipeline(command, names)
    if trip is not None:
        return GuardedResult(command, REFUSAL_EXIT, "", REFUSAL_TEXT, refused=True, trip=trip)

    # Globs expand to real paths, so the expansion is screened too: a pattern that names
    # nothing forbidden can still MATCH something forbidden.
    expanded = [_expand_globs(stage, cwd) for stage in stages]
    trip = _screen_words(" ".join(word for argv in expanded for word in argv), names)
    if trip is not None:
        return GuardedResult(command, REFUSAL_EXIT, "", REFUSAL_TEXT, refused=True, trip=trip)

    # Stages run in sequence, each fed the previous stage's stdout, rather than as
    # concurrently-piped processes: with every stream captured, concurrent pipes deadlock
    # on a full buffer, and the read surface here is small and bounded by `timeout`. The
    # visible difference from a real pipeline is that `head -5` does not terminate its
    # upstream early - it truncates instead.
    piped = ""
    stderr_parts: list[str] = []
    returncode = 0
    remaining = float(timeout)
    for stage, argv in zip(stages, expanded):
        started = time.monotonic()
        try:
            proc = subprocess.run(
                argv,
                shell=False,
                cwd=str(cwd),
                input=piped,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=max(remaining, 0.1),
                check=False,
            )
        except subprocess.TimeoutExpired:
            return GuardedResult(command, 124, "", "sandbox guard: command timed out.", refused=False)
        except (FileNotFoundError, NotADirectoryError):
            # There is no shell to say "command not found", so the guard says it - with the
            # conventional exit code, and without pretending the command succeeded.
            return GuardedResult(
                command, 127, "", f"sandbox guard: command not found: {argv[0]}", refused=False
            )
        except OSError as exc:
            return GuardedResult(
                command, 126, "", f"sandbox guard: could not run {argv[0]}: {exc}", refused=False
            )
        remaining -= time.monotonic() - started
        returncode = proc.returncode
        piped = "" if stage.drop_stdout else proc.stdout
        if proc.stderr and not stage.drop_stderr:
            stderr_parts.append(proc.stderr)

    stderr = "".join(stderr_parts)
    combined = f"{piped}\n{stderr}"
    trip = screen_output(combined, names)
    if trip is not None:
        return GuardedResult(command, REFUSAL_EXIT, "", REFUSAL_TEXT, refused=True, trip=trip)

    stdout = piped
    if len(stdout.encode("utf-8")) > max_output_bytes:
        stdout = stdout.encode("utf-8")[:max_output_bytes].decode("utf-8", errors="ignore")
        stdout += "\n[output truncated by sandbox guard]"
    return GuardedResult(command, returncode, stdout, stderr, refused=False)


# --------------------------------------------------------------------------------------
# The probe - the Done-when's proof, including its positive controls
# --------------------------------------------------------------------------------------

PACK_PATH = "docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md"


@dataclass
class ProbeVector:
    name: str
    command: str
    expect: str  # "refused" | "allowed"
    outcome: str
    passed: bool
    detail: str = ""


DEFAULT_CONTROLS: tuple[tuple[str, str], ...] = (
    ("V7 positive control - repo doc", "sed -n '1,3p' CLAUDE.md"),
    ("V8 positive control - C1-R5's own adjudicating command", "ls docs/decisions/ADR-*.md | wc -l"),
    (
        "V9 positive control - C1-X1's own adjudicating command",
        "git show 94652fdf:scripts/block_ff_push.py | sed -n '151,153p'",
    ),
)


def probe(
    sandbox: Sandbox,
    pack_path: str = PACK_PATH,
    controls: tuple[tuple[str, str], ...] = DEFAULT_CONTROLS,
) -> list[ProbeVector]:
    """Deliberately try to read the pack, several ways, and assert every attempt fails.

    Positive controls are part of the probe by design: a guard that refuses EVERYTHING
    would pass a refusal-only probe while destroying the instrument, so legitimate
    commands (two of them the pack's own adjudicating commands) must be ALLOWED.
    """
    vectors: list[tuple[str, str, str]] = [
        ("V1 direct read", f"cat {pack_path}", "refused"),
        ("V2 ranged read", f"sed -n '180,230p' {pack_path}", "refused"),
        (
            "V3 historical vector (C1-N2's actual command shape)",
            f"python3 -c \"print(open('{pack_path}').read()[:50000])\"",
            "refused",
        ),
        ("V4 git-object read", f"git show HEAD~1:{pack_path}", "refused"),
        ("V5 content grep, path not named", "grep -rn 'Ground truth' . | head -5", "refused"),
        ("V6 strip-commit diff", "git show HEAD", "refused"),
        ("V6b path disclosure via stat", "git log --stat -1", "refused"),
    ]
    # V5b isolates Layer B's CONTENT leg: the command names no path and carries no canary,
    # so nothing but the output scan can refuse it. Without this vector the probe could pass
    # on path screening alone and the content leg would be untested.
    blob = _git(sandbox.path, "rev-parse", f"HEAD~1:{pack_path}", check=False).strip()
    if blob:
        vectors.append(("V5b raw blob by hash, no path, no canary", f"git cat-file -p {blob}", "refused"))

    vectors.extend((name, command, "allowed") for name, command in controls)
    results: list[ProbeVector] = []
    for name, command, expect in vectors:
        res = run_guarded(command, sandbox)
        outcome = "refused" if res.refused else "allowed"
        detail = ""
        if res.trip is not None:
            detail = f"layer {res.trip.layer}: {res.trip.kind}"
        elif expect == "allowed":
            detail = f"rc={res.returncode}, {len(res.stdout)} bytes"
        results.append(ProbeVector(name, command, expect, outcome, outcome == expect, detail))
    return results


def scan_transcript(commands: list[str], denied_names: set[str] | None = None) -> dict[str, object]:
    """Post-hoc contamination scan of a run transcript, in the shape of results-2 section 6."""
    flagged = []
    for command in commands:
        trip = screen_command(command, denied_names)
        if trip is not None:
            flagged.append({"command": command, "kind": trip.kind})
    return {"total": len(commands), "flagged": len(flagged), "detail": flagged}


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="No-pack sandbox guard ([#562])")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_prov = sub.add_parser("provision", help="clone and strip a sandbox")
    p_prov.add_argument("--dest", required=True)
    p_prov.add_argument("--source", default=None)
    p_prov.add_argument("--head", default="HEAD")
    p_prov.add_argument("--allow-shallow", action="store_true")
    p_prov.add_argument(
        "--sandbox-root",
        default=None,
        help=f"containment boundary for provision and teardown (default: ${ENV_SANDBOX_ROOT}, "
        f"else {default_sandbox_root()})",
    )

    p_probe = sub.add_parser("probe", help="prove the pack is unreadable")
    p_probe.add_argument("--sandbox", required=True)
    p_probe.add_argument("--manifest", default=None)

    p_exec = sub.add_parser("exec", help="run one guarded command in a sandbox")
    p_exec.add_argument("--sandbox", required=True)
    p_exec.add_argument("--manifest", default=None)
    p_exec.add_argument("--json", action="store_true")
    p_exec.add_argument("command", nargs=argparse.REMAINDER)

    p_scan = sub.add_parser("scan", help="scan a tree for answer-key content")
    p_scan.add_argument("--root", default=None)

    p_down = sub.add_parser("teardown", help="remove a sandbox and verify removal")
    p_down.add_argument("--sandbox", required=True)
    p_down.add_argument(
        "--sandbox-root",
        default=None,
        help=f"containment boundary (default: ${ENV_SANDBOX_ROOT}, else {default_sandbox_root()})",
    )

    args = parser.parse_args(argv)

    if args.cmd == "provision":
        source = Path(args.source) if args.source else _repo_root()
        sandbox = provision(
            source,
            Path(args.dest),
            args.head,
            allow_shallow=args.allow_shallow,
            sandbox_root=args.sandbox_root,
        )
        # The manifest is already persisted INSIDE the sandbox by `provision`; printing it
        # is for the caller's transcript, and writing it anywhere else is not this tool's
        # to decide.
        print(json.dumps(sandbox.manifest(), indent=2))
        return 0

    if args.cmd == "probe":
        sandbox = _load(args.sandbox, args.manifest)
        vectors = probe(sandbox)
        for vec in vectors:
            flag = "PASS" if vec.passed else "FAIL"
            print(f"{flag}  {vec.name:<52} expect={vec.expect:<8} got={vec.outcome:<8} {vec.detail}")
        failed = [v for v in vectors if not v.passed]
        print(f"\nprobe: {len(vectors) - len(failed)}/{len(vectors)} vectors as expected")
        return 1 if failed else 0

    if args.cmd == "exec":
        sandbox = _load(args.sandbox, args.manifest)
        command = " ".join(a for a in args.command if a != "--")
        res = run_guarded(command, sandbox)
        if args.json:
            print(json.dumps(res.as_dict(), indent=2))
        else:
            sys.stdout.write(res.stdout)
            sys.stderr.write(res.stderr)
        return res.returncode

    if args.cmd == "scan":
        root = Path(args.root) if args.root else _repo_root()
        hits = scan_tree(root)
        for rel, ids in sorted(hits.items()):
            print(f"{rel}: {','.join(ids)}")
        print(f"\n{len(hits)} file(s) carry answer-key content")
        return 0

    if args.cmd == "teardown":
        try:
            ok = teardown(Path(args.sandbox), sandbox_root=args.sandbox_root)
        except TeardownRefused as exc:
            # The one refusal in this tool that is NOT deliberately neutral: nothing was
            # deleted and the operator needs to know exactly why, because the alternative
            # to a legible refusal is an operator reaching for `rm -rf` by hand.
            print(f"sandbox guard: teardown {exc}", file=sys.stderr)
            return REFUSAL_EXIT
        print("removed and verified" if ok else "REMOVAL FAILED")
        return 0 if ok else 1

    return 2


def _load(sandbox_path: str, manifest_path: str | None) -> Sandbox:
    """Rehydrate a Sandbox from disk, so `exec`/`probe` work across process boundaries."""
    path = Path(sandbox_path)
    candidate = Path(manifest_path) if manifest_path else path / MANIFEST_RELPATH
    if candidate.exists():
        data = json.loads(candidate.read_text(encoding="utf-8"))
        recorded_root = data.get("sandbox_root")
        return Sandbox(
            path=path,
            source=Path(data["source"]),
            head=data["head"],
            strip_commit=data["strip_commit"],
            removed=list(data["removed"]),
            redacted=dict(data["redacted"]),
            postcondition_clean=bool(data["postcondition_clean"]),
            residual=dict(data.get("residual", {})),
            denied=list(data.get("denied", [])),
            sandbox_root=Path(recorded_root) if recorded_root else None,
            nonce=str(data.get("nonce", "")),
        )
    # No manifest: the content layer still holds; only the path layer is degraded, and
    # that degradation is announced rather than silent.
    print("nopack_sandbox: no manifest found - Layer A path screening is degraded", file=sys.stderr)
    return Sandbox(path=path, source=path, head="unknown", strip_commit="unknown")


if __name__ == "__main__":
    raise SystemExit(main())
