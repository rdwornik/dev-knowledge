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
  * The command allowlist screens argv0 and a table of known exec/write flags. It is not a
    proof that no allowlisted tool has another write mode (`sed`'s `w` command is one it
    cannot see). What contains that is the sandbox being a disposable clone: a write inside
    it survives nothing, and every byte leaving it goes through Layer B.
  * `teardown`'s provenance is checked immediately before deletion, but a check and an
    `rmtree` are two syscalls. Closing that gap needs no-follow traversal from a directory
    descriptor, which Windows does not offer portably, so what is closed is the failure on
    record - a wrong path sitting there statically - not a live attacker winning a race.
  * The marker and the root registry are both files. Someone who can write to the sandbox
    root can forge both. They raise forgery from "create one file" to "tamper with this
    tool's own records", which is the honest size of the claim.

USAGE (the seam the candidate transport calls)
----------------------------------------------
    export NOPACK_SANDBOX_ROOT=/tmp/nopack-sandboxes      # every subcommand reads this
    python3 scripts/nopack_sandbox.py provision --dest "$NOPACK_SANDBOX_ROOT/ab"
    python3 scripts/nopack_sandbox.py probe    --sandbox "$NOPACK_SANDBOX_ROOT/ab"
    python3 scripts/nopack_sandbox.py exec     --sandbox "$NOPACK_SANDBOX_ROOT/ab" -- 'git log --oneline -3'
    python3 scripts/nopack_sandbox.py teardown --sandbox "$NOPACK_SANDBOX_ROOT/ab"

Every subcommand - not just provision and teardown - takes `--sandbox-root`, because the
root is the boundary each of them checks the given path against BEFORE reading anything
there. Set the environment variable once and none of them needs the flag.

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
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

# CLOUD-4 v2 (R2 §1.5 GO-b) precedent: a retired-and-relocated canonical doc's current path
# comes from the one registry, not a literal here ([#614] lane-e-5, 2026-09-01 -- VISION.md
# moved to docs/archive/VISION.md and this module's literal silently lost spine protection).
try:
    from scripts import canonical_docs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoints
    import canonical_docs

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
    canonical_docs.CANONICAL_RETIRED_LOCATIONS[canonical_docs.VISION],
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

# Removing `shell=True` does not by itself make the surface read-only: an allowlisted
# program can be an execution engine in its own right. `python3 -c ...`, `awk 'BEGIN{system(
# "sh")}'` and `xargs sh` each spawn whatever they are told to, and no argv0 check sees it.
# So the general-purpose interpreters are OUT of the allowlist entirely - there is no
# read-only mode of "run this program" to carve out - and the survivors that have a write
# or exec MODE are constrained by flag below.
ALLOWED_ARGV0: frozenset[str] = frozenset(
    {
        "basename", "cat", "comm", "cut", "diff", "dirname", "echo", "file", "find",
        "git", "grep", "head", "ls", "md5sum", "nl", "printf", "rg",
        "sed", "sha256sum", "sort", "stat", "tail", "test", "tr", "uniq", "wc",
    }
)

# Flags that turn an allowlisted reader into a writer or a launcher. Matched against the
# whole argument and against its `=`-prefix, so `--exec=rm` is caught as well as `-exec`.
#
# HONEST LIMIT, stated because an overstated guard is worse than a modest one: this is a
# table of the KNOWN execution and write modes of these tools, not a proof that no other
# exists. The load-bearing containment is elsewhere - the sandbox is a disposable clone and
# a write INSIDE it harms nothing, Layer B screens every byte on the way out, and teardown
# refuses anything it cannot prove it made. This table closes the paths by which a
# read-only surface would otherwise reach OUTSIDE the sandbox.
_FORBIDDEN_ARGS: dict[str, frozenset[str]] = {  # noqa: RUF012
    # `find` is kept because it is a genuine read tool; its ACTION primaries are what run
    # or delete things.
    # Action primaries run or delete things. `-L`/`-H`/`-follow` DEREFERENCE symlinks
    # during traversal, which is how a command whose every operand is inside the sandbox
    # still reads outside it - the operand check can only see what was written down.
    "find": frozenset(
        {"-exec", "-execdir", "-ok", "-okdir", "-delete", "-fprintf", "-fls", "-fprint",
         "-fprint0", "-L", "-H", "-follow", "--dereference"}
    ),
    # In-place edit is the write mode. sed's `w` command and GNU `e` command are NOT
    # detectable by flag - see the limit above; they write and run relative to the
    # sandbox, which is the disposable clone.
    # `-i` is the obvious write mode; `-f` loads a script from a file, which cannot be
    # screened, so the script must arrive inline where `_sed_script_is_read_only` sees it.
    "sed": frozenset({"-i", "--in-place", "-f", "--file"}),
    # `-R` is the recursive mode that FOLLOWS symlinks (`-r` does not), so it walks out of
    # the tree without any operand saying so. `--dereference-recursive` is its long form.
    "grep": frozenset({"-R", "--dereference-recursive", "-r--dereference"}),
    # ripgrep can run a preprocessor per file, which is `-exec` by another name; `--follow`
    # is grep's `-R`.
    "rg": frozenset({"--pre", "--hostname-bin", "--search-zip", "-z", "-L", "--follow"}),
    # `sort -o FILE` writes wherever it is pointed and `--compress-program` runs a program.
    # `-T` relocates its temporary files. All three are outside a read surface.
    "sort": frozenset({"-o", "--output", "--compress-program", "-T", "--temporary-directory",
                       "--files0-from"}),
    # `ls -L` dereferences, and with `-R` it walks the host through any symlink in the
    # tree while the only operand it was given is `.`.
    "ls": frozenset({"-L", "--dereference", "-H", "--dereference-command-line",
                     "--dereference-command-line-symlink-to-dir"}),
    # diff DEREFERENCES by default (`--no-dereference` is the opt-out), so recursing it
    # over the tree walks out through any symlink the same way.
    "diff": frozenset({"-r", "--recursive"}),
    # --- filename STREAMS ---------------------------------------------------------
    # These modes take their file list from stdin or from another file rather than from
    # argv, so `_screen_paths` - which reads argv - sees nothing at all:
    # `printf '/etc/passwd\n' | file -f -` reads a host file with no path in any argument.
    # A pipeline makes the producer trivial, since `printf` is allowlisted.
    "file": frozenset({"-f", "--files-from"}),
    "wc": frozenset({"--files0-from"}),
    "md5sum": frozenset({"-c", "--check", "--strict"}),
    "sha256sum": frozenset({"-c", "--check", "--strict"}),
}

# ...and the same class on tools that already have a row above.
_FORBIDDEN_ARGS["find"] |= frozenset({"-files0-from"})
_FORBIDDEN_ARGS["sort"] |= frozenset({"--files0-from"})

# git is an ALLOWLIST, not a denylist. A denylist of write subcommands lets every
# subcommand nobody thought of through, and git has a lot of them.
_GIT_READ_SUBCOMMANDS: frozenset[str] = frozenset(
    {
        "annotate", "blame", "cat-file", "check-attr", "check-ignore", "cherry",
        "count-objects", "describe", "diff", "diff-index", "diff-tree", "for-each-ref",
        "grep", "log", "ls-files", "ls-tree", "merge-base", "name-rev",
        "range-diff", "rev-list", "rev-parse", "shortlog", "show", "show-branch",
        "show-ref", "status", "whatchanged",
        # `help` is NOT here: it launches a browser or a man viewer. Neither are
        # `verify-commit` / `verify-tag`: they shell out to GPG, which reads the host's
        # own configuration and can launch a pinentry helper of its choosing.
    }
)

# These have a read form and a write form, told apart by whether they carry an operand.
# Refusing `git branch -a` outright was a measured false positive; an operand (or a
# mutating flag, which always takes one) is what makes them writes.
#
# `stash` is NOT here, though the first draft listed it as a bare listing: modern `git
# stash` with no arguments is `git stash push`, so the bare form is the write. Found while
# hand-checking this table against real git behaviour rather than against its own comment.
_GIT_LISTING_WHEN_BARE: frozenset[str] = frozenset(
    {"branch", "config", "notes", "reflog", "remote", "tag", "worktree"}
)

# git's PRE-command options, which is where the real bypass lived: the screen skipped
# option tokens but not their operands, so `git -C . config --global user.name x` read `.`
# as the subcommand and sailed through. These options do not merely take a value - they
# RELOCATE git (`-C`, `--git-dir`, `--work-tree`) or inject configuration into it (`-c`,
# `--config-env`), and `-c alias.x=!sh` is a shell by another road. All refused outright:
# nothing a lane needs to read requires moving git off the sandbox it was pointed at.
_GIT_RELOCATING_OPTIONS: frozenset[str] = frozenset(
    {
        "-C", "-c", "--exec-path", "--git-dir", "--work-tree", "--namespace",
        "--config-env", "--super-prefix", "--attr-source",
    }
)

# Valueless pre-command options, safe to step over while looking for the subcommand.
_GIT_BARE_OPTIONS: frozenset[str] = frozenset(
    {
        "-P", "--no-pager", "--bare", "--literal-pathspecs",
        "--glob-pathspecs", "--noglob-pathspecs", "--icase-pathspecs",
        "--no-replace-objects", "--no-optional-locks", "--no-lazy-fetch",
        "--version", "--html-path", "--man-path", "--info-path",
    }
)

# Options that hand git's work to ANOTHER program - a pager, a browser, an external diff
# driver, a textconv filter. Each is `-exec` wearing git's clothes, and none is needed to
# read a repository. `--paginate` is here rather than in the bare set for the same reason:
# output is captured, so forcing a pager can only ever mean launching one.
# Split by POSITION, and the split is load-bearing. `-p` before the subcommand is
# `--paginate`; after it, it belongs to the subcommand and means something else entirely -
# `git log -p` is a patch, `git cat-file -p` is a pretty-print. Refusing `-p` everywhere
# turned the probe's own V5b vector (`git cat-file -p <blob>`, the ONLY vector that tests
# Layer B's content leg on a raw blob) into a Layer A refusal: still a PASS, but a vacuous
# one, testing nothing. Caught by watching which layer the probe reported.
_GIT_PRE_HELPER_OPTIONS: frozenset[str] = frozenset({"-p", "--paginate", "--pager", "--exec"})
_GIT_ANY_HELPER_OPTIONS: frozenset[str] = frozenset(
    {
        "--ext-diff", "--textconv", "--open-files-in-pager", "--web", "--gui", "--tool",
        "--extcmd",
        # signature verification is GPG, i.e. another program with its own config
        "--show-signature", "--gpg-sign", "--signing-key",
    }
)

# `git config` reads only with one of these, and never with more than one operand (the
# key). `git config --global user.name x` carries two, which is what makes it a write.
_GIT_CONFIG_READ_FLAGS: frozenset[str] = frozenset(
    {"--list", "-l", "--get", "--get-all", "--get-regexp", "--get-urlmatch", "--get-color"}
)

# `git symbolic-ref HEAD` READS where HEAD points; `git symbolic-ref HEAD refs/heads/main`
# WRITES it, re-attaching a sandbox that provisioning deliberately detached. One operand
# is the read, two is the write, and `-d` is a delete - so it cannot be a plain read
# subcommand and it is not a no-operand listing either.
_GIT_ONE_OPERAND_READS: frozenset[str] = frozenset({"symbolic-ref"})

# Per-subcommand flag allowlists for the listing forms. "No operand" is not sufficient on
# its own: `git branch --edit-description` has no operand and opens the host's EDITOR,
# which is a program outside the guarded argv surface entirely. A flag that takes a
# detached value shows up as an operand and is refused by the operand rule; the `--opt=v`
# spelling is the way to pass one.
_GIT_LISTING_READ_FLAGS: dict[str, frozenset[str]] = {  # noqa: RUF012
    "branch": frozenset(
        {"-a", "--all", "-r", "--remotes", "-l", "--list", "-v", "-vv", "--verbose",
         "-q", "--quiet", "--show-current", "--color", "--no-color", "--column",
         "--no-column", "--sort", "--format", "--contains", "--no-contains", "--merged",
         "--no-merged", "--points-at", "-i", "--ignore-case", "--omit-empty"}
    ),
    "tag": frozenset(
        {"-l", "--list", "-n", "--contains", "--no-contains", "--merged", "--no-merged",
         "--points-at", "--sort", "--format", "--color", "--no-color", "-i",
         "--ignore-case", "--omit-empty"}
    ),
    "config": frozenset(
        _GIT_CONFIG_READ_FLAGS
        | {"--local", "--global", "--system", "--worktree", "--file", "--blob", "--null",
           "-z", "--name-only", "--show-origin", "--show-scope", "--type", "--includes",
           "--no-includes", "--default"}
    ),
    "remote": frozenset({"-v", "--verbose"}),
    "notes": frozenset(),
    "reflog": frozenset(),
    "worktree": frozenset(),
}

# A markdown line that OPENS a block. Redaction stops at these, so a canary inside one
# list item never eats its neighbours - measured: extending to every contiguous non-blank
# line took 318 lines out of `docs/audits/README.md`, which is one long list.
_BLOCK_START = re.compile(r"^\s{0,3}(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|>|\||```|~~~)")


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

# The registry lives in the ROOT, beside the sandboxes rather than inside one, and teardown
# never deletes it. It is what makes the marker PROOF rather than a claim: a marker is a
# file inside the tree being deleted, so anything that can write there can fabricate one.
# Requiring the registry to agree means a forger has to reach outside the tree it is trying
# to get deleted, into a file this tool owns.
#
# Its honest limit: a writer with access to the whole root can still edit both. The
# registry raises the bar from "drop one file in" to "tamper with the tool's own records",
# and the boundary that actually stops the recorded failure - a typo, a stale path - is
# containment plus this pair.
REGISTRY_NAME = ".nopack-registry.json"


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


def read_metadata_file(sandbox_path: Path, relpath: str) -> str | None:
    """Read one of the sandbox's own metadata files, or None if it is not genuinely one.

    `_meta_dir` refuses to WRITE through a symlink; this is the reading half, and it was
    missing. A directory that was never provisioned can have `.git/nopack/manifest.json`
    be a symlink to any JSON file on the host, and `_load` opened it BEFORE proving
    anything - so the control path itself read outside the clone. Every component is
    checked, the final target is resolved, and it has to still be inside the sandbox.
    """
    sandbox_path = Path(sandbox_path)
    current = sandbox_path
    for part in PurePosixPath(relpath).parts:
        current = current / part
        if current.is_symlink():
            return None
    if not current.is_file():
        return None
    try:
        resolved = current.resolve()
        root = sandbox_path.resolve()
    except OSError:
        return None
    if not _is_contained(resolved, root):
        return None
    try:
        return current.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def read_marker(sandbox_path: Path) -> dict[str, object] | None:
    """Return the provisioning marker at `sandbox_path`, or None if it is absent/invalid.

    "Invalid" is anything that is not a marker this tool wrote FOR THIS DIRECTORY: wrong
    kind, malformed nonce, unparseable JSON, or a `sandbox` field naming somewhere else.
    That last check is what keeps a marker from being laundered - copying one out of a real
    sandbox into an unrelated tree does not make that tree deletable.
    """
    raw = read_metadata_file(sandbox_path, MARKER_RELPATH)
    if raw is None:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
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


def _meta_dir(sandbox_path: Path) -> Path:
    """The sandbox's metadata directory, created with no symlinked component.

    `mkdir(exist_ok=True)` and `open(..., "x")` both follow parent symlinks, so a
    substituted `.git/nopack` would silently redirect the marker and the manifest outside
    the sandbox. Each component is created and then checked, and the finished directory is
    re-resolved and required to still be inside the sandbox.
    """
    sandbox_path = Path(sandbox_path)
    current = sandbox_path
    for part in PurePosixPath(SANDBOX_META_DIR).parts:
        current = current / part
        if current.is_symlink():
            raise RuntimeError(f"refusing to write metadata through a symlink: {current}")
        current.mkdir(exist_ok=True)
    resolved_root = _resolve(sandbox_path)
    if not _is_contained(_resolve(current), resolved_root):
        raise RuntimeError(f"sandbox metadata directory escapes the sandbox: {current}")
    return current


def write_marker(sandbox_path: Path, nonce: str, sandbox_root: Path) -> Path:
    """Write the provisioning marker. Exclusive creation - never clobbers."""
    marker_file = _meta_dir(sandbox_path) / Path(MARKER_RELPATH).name
    payload = {
        "marker": MARKER_KIND,
        "nonce": nonce,
        "sandbox": str(_resolve(sandbox_path)),
        "sandbox_root": str(_resolve(sandbox_root)),
    }
    with open(marker_file, "x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    return marker_file


def _registry_path(sandbox_root: Path) -> Path:
    return Path(sandbox_root) / REGISTRY_NAME


def read_registry(sandbox_root: Path) -> dict[str, str]:
    """Map resolved-sandbox-path -> nonce. A missing or corrupt registry reads as empty."""
    path = _registry_path(sandbox_root)
    if not path.is_file() or path.is_symlink():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items() if isinstance(v, str)}


def _write_registry(sandbox_root: Path, entries: dict[str, str]) -> None:
    """Replace the registry ATOMICALLY. Never truncate the live file.

    Writing in place means a crash or a concurrent read lands on a half-written registry,
    and an unreadable registry makes every teardown refuse - which turns a write race into
    permanently undeletable sandboxes, i.e. leftovers.
    """
    path = _registry_path(sandbox_root)
    if path.is_symlink():
        raise RuntimeError(f"refusing to write the registry through a symlink: {path}")
    Path(sandbox_root).mkdir(parents=True, exist_ok=True)
    payload = json.dumps(entries, indent=2, sort_keys=True)
    temp = path.with_name(f"{path.name}.{os.getpid()}.{secrets.token_hex(4)}.tmp")
    temp.write_text(payload, encoding="utf-8", newline="\n")
    os.replace(temp, path)


# A waiter may not break a lock merely because IT got bored. An earlier draft unlinked the
# lock after its own 10-second timeout, which lets a slow holder resume and overwrite a
# newer registry - and lets two waiters each think they hold it. Breaking requires the lock
# to be provably ancient, and the break itself is a rename, so exactly one waiter wins it.
STALE_LOCK_SECONDS = 300.0


@contextmanager
def _registry_lock(sandbox_root: Path, timeout: float = 10.0):
    """Serialise read-modify-write on one root's registry.

    An exclusive-create lock file, because it is the one primitive that behaves the same on
    Windows and POSIX. On timeout this RAISES rather than stealing: a lost registry entry
    is a sandbox that can never be torn down, which is the leftover this organ exists to
    prevent, so refusing loudly is the better failure.
    """
    Path(sandbox_root).mkdir(parents=True, exist_ok=True)
    lock = _registry_path(sandbox_root).with_suffix(".lock")
    deadline = time.monotonic() + timeout
    held = False
    while True:
        try:
            handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(handle, f"{os.getpid()} {time.time()}".encode())
            os.close(handle)
            held = True
            break
        except (FileExistsError, PermissionError):
            # PermissionError, not just FileExistsError: on Windows an exclusive create
            # against a file another process is in the middle of unlinking raises errno 13
            # rather than EEXIST. Treating that as a hard failure made a lock RELEASE look
            # like a lock error to whoever was waiting for it.
            if time.monotonic() > deadline:
                if not _break_stale_lock(lock):
                    raise RuntimeError(
                        f"registry lock held by another process: {lock}. Nothing was "
                        f"changed; retry, or remove the lock if you know it is orphaned."
                    )
                deadline = time.monotonic() + timeout
            time.sleep(0.02)
    try:
        yield
    finally:
        if held:
            try:
                lock.unlink()
            except OSError:  # pragma: no cover - already broken as stale
                pass


def _break_stale_lock(lock: Path) -> bool:
    """Break a lock ONLY if it is provably ancient. Returns True when this caller broke it."""
    try:
        age = time.time() - lock.stat().st_mtime
    except OSError:
        return True  # it vanished: the holder released it, so the retry will win normally
    if age < STALE_LOCK_SECONDS:
        return False
    claim = lock.with_name(f"{lock.name}.stale.{os.getpid()}.{secrets.token_hex(4)}")
    try:
        # A rename is atomic, so of N waiters that agree the lock is ancient exactly one
        # gets the file; the losers see FileNotFoundError and go back to waiting.
        os.replace(lock, claim)
    except OSError:
        return False
    try:
        claim.unlink()
    except OSError:  # pragma: no cover
        pass
    return True


def register_sandbox(sandbox_root: Path, sandbox_path: Path, nonce: str) -> None:
    with _registry_lock(sandbox_root):
        entries = read_registry(sandbox_root)
        entries[str(_resolve(sandbox_path))] = nonce
        _write_registry(sandbox_root, entries)


def unregister_sandbox(sandbox_root: Path, sandbox_path: Path) -> None:
    with _registry_lock(sandbox_root):
        entries = read_registry(sandbox_root)
        if entries.pop(str(_resolve(sandbox_path)), None) is not None:
            _write_registry(sandbox_root, entries)


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
        encoding="utf-8",
        errors="replace",
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
        encoding="utf-8",
        errors="replace",
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
        register_sandbox(root, dest, nonce)
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

    A destination that has VANISHED is an anomaly here, not a success: the clone WAS
    created, so if its path is now empty something moved it, and the unstripped tree is
    still on disk under a name this function does not know. Saying so is the whole job of a
    no-leftovers organ; `teardown`'s own idempotent "already absent, nothing to do" would
    have reported that as a clean abort.
    """
    if not resolved_dest.exists():
        print(
            f"nopack_sandbox: ANOMALY - {resolved_dest} disappeared during an aborted "
            f"provision; the clone it held may survive elsewhere and is UNSTRIPPED",
            file=sys.stderr,
        )
        unregister_sandbox(root, resolved_dest)
        return
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
    unregister_sandbox(root, resolved_dest)
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
    target = _meta_dir(sandbox_path) / Path(MANIFEST_RELPATH).name
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

    marker = verify_provenance(resolved, root, expected_nonce=expected_nonce, error=TeardownRefused)

    # Re-verify immediately before deleting, and pin the directory's identity across the
    # gap. HONEST LIMIT, because this narrows the check-to-delete race rather than closing
    # it: closing it needs no-follow traversal from a directory descriptor, which Windows -
    # the platform this runs on - does not offer portably. What remains is a race an
    # attacker with write access to the root must win against microseconds; what is closed
    # is the failure actually on record, which is a wrong path sitting there statically.
    identity = _dir_identity(resolved)
    if read_marker(resolved) != marker or _dir_identity(resolved) != identity:
        raise TeardownRefused(f"refused: {resolved} changed underneath the provenance check")

    _rmtree_force(resolved)
    removed = not resolved.exists()
    if removed:
        unregister_sandbox(root, resolved)
    return removed


def verify_provenance(
    resolved: Path,
    root: Path,
    *,
    expected_nonce: str | None = None,
    error: type[Exception] = RuntimeError,
) -> dict[str, object]:
    """Prove `resolved` is a sandbox THIS tool provisioned, or raise. Returns its marker.

    Shared by `teardown` and `_load` on purpose. `exec` pointed at an arbitrary directory
    runs commands with that directory as `cwd`, so every relative operand reads from it -
    which makes "is this really a sandbox" exactly as load-bearing before running a command
    as it is before deleting a tree. One function, so the two answers cannot drift.
    """
    if not resolved.is_dir():
        raise error(f"refused: not a directory: {resolved}")
    if not _is_contained(resolved, root):
        raise error(f"refused: {resolved} is outside the configured sandbox root {root}")
    marker = read_marker(resolved)
    if marker is None:
        raise error(
            f"refused: {resolved} carries no valid provisioning marker ({MARKER_RELPATH}); "
            f"this tool did not provision it"
        )
    registered = read_registry(root).get(str(resolved))
    if registered is None:
        raise error(
            f"refused: {resolved} is not in the sandbox registry ({REGISTRY_NAME}); a marker "
            f"inside a tree is a claim, not a provenance"
        )
    if registered != marker.get("nonce"):
        raise error(f"refused: {resolved} disagrees with the registry (nonce mismatch)")
    if expected_nonce is not None and marker.get("nonce") != expected_nonce:
        raise error(f"refused: {resolved} was provisioned by a different run (nonce mismatch)")
    return marker


def _dir_identity(path: Path) -> tuple[int, int] | None:
    """(st_dev, st_ino) when the platform supplies them, else None. Best-effort by design."""
    try:
        info = path.stat()
    except OSError:
        return None
    return (info.st_dev, info.st_ino) if info.st_ino else None


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


# The environment a guarded command inherits is part of its attack surface: git reads the
# host's global and system config, so a pager, an alias or a textconv filter configured on
# the machine would run inside the sandbox without ever appearing in the command. Every
# stage gets a scrubbed environment instead of the session's.
_ENV_KEEP: tuple[str, ...] = (
    "PATH", "PATHEXT", "SYSTEMROOT", "SystemRoot", "COMSPEC", "WINDIR", "TEMP", "TMP",
    "HOME", "USERPROFILE", "LANG", "LC_ALL", "TZ",
)


def _child_env() -> dict[str, str]:
    env = {key: os.environ[key] for key in _ENV_KEEP if key in os.environ}
    env.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_ATTR_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_EXTERNAL_DIFF": "",
            "GIT_ASKPASS": "",
            "GIT_PAGER": "cat",
            "PAGER": "cat",
        }
    )
    return env


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

    trip = screen_stages(stages)
    return (trip, []) if trip is not None else (None, stages)


def screen_stages(stages: list[Stage], cwd: Path | None = None) -> Trip | None:
    """The structural policy. Runs over parsed argv AND again over expanded argv.

    Running it twice is the point. Expansion changes argv - that is what expansion IS - so
    validating only the pre-expansion form leaves the executed command unvalidated, which
    is the same class of gap as screening a string and then handing it to a shell.
    """
    for stage in stages:
        argv0 = stage.argv[0]
        # A glob may not choose the program or the subcommand. `git *` expanding to `git
        # commit`, or `*/python3` selecting an unscreened binary, is exactly the
        # screened-one-thing-ran-another defect in a new costume.
        if stage.globbable and stage.globbable[0]:
            return Trip("A", "glob-in-command-position", "the command name may not be a glob")

        name = argv0.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        if name in _SHELL_KEYWORDS:
            return Trip("A", "shell-construct", f"'{name}' is a shell construct, not a command")
        if name not in ALLOWED_ARGV0:
            return Trip("A", "argv0-not-allowed", f"'{name}' is not in the read-only allowlist")
        if argv0 != name:
            # `bin/cat` resolves by path, so allowlisting the basename would let any
            # binary named `cat` anywhere on disk through.
            return Trip("A", "argv0-not-allowed", "the command must be a bare name, not a path")

        forbidden = _FORBIDDEN_ARGS.get(name, frozenset())
        for token in stage.argv[1:]:
            hit = next((option for option in _option_forms(token) if option in forbidden), None)
            if hit is not None:
                return Trip("A", "forbidden-argument", f"'{hit}' gives {name} an exec or write mode")

        if name == "git":
            trip = _screen_git(stage)
        elif name == "sed":
            trip = _screen_sed(stage)
        else:
            trip = None
        if trip is not None:
            return trip

        trip = _screen_paths(stage, cwd)
        if trip is not None:
            return trip
    return None


# An argument that is an absolute path, or that climbs out with `..`, reaches the HOST
# filesystem. `cwd=<sandbox>` is a starting point, not a boundary: `cat ../secret`,
# `ls /` and `sed -n '1p' /etc/passwd` all read outside a clone the guard is supposed to
# confine reads to. Globs were already confined; literal operands were not.
_ABSOLUTE_PATH = re.compile(r"^(?:[/\\]|[A-Za-z]:[/\\])")

# Tools whose arguments are DATA, never paths to open. Exempting them keeps the rule from
# refusing `echo /usr/bin` - which reads nothing - for looking like a path.
_NON_READING_COMMANDS: frozenset[str] = frozenset({"echo", "printf"})

# Where a tool's FIRST operand is a pattern rather than a file. `grep '/usr' file` searches
# for a string that starts with a slash; refusing it would be the `git branch -a` false
# positive all over again.
_PATTERN_FIRST: frozenset[str] = frozenset({"grep", "rg"})

# Options that supply the pattern. `-e`'s value IS the pattern, so it is exempt from the
# path rule; `-f`'s value is a FILE the tool opens, so it is emphatically not - and either
# one means the first bare operand is a file rather than the pattern. An earlier draft
# lumped them together, which let `grep -f /etc/passwd CLAUDE.md` through: `-f` suppressed
# nothing, so `/etc/passwd` was exempted as "the pattern" and then opened as a file.
_PATTERN_VALUE_FLAGS: frozenset[str] = frozenset({"-e", "--regexp"})
_PATTERN_FILE_FLAGS: frozenset[str] = frozenset({"-f", "--file"})


# Short options of grep/rg that CONSUME a value. Needed in order, because in a bundle the
# first value-taking letter owns everything after it: `-fescape` is `-f escape`, and `-rn`
# is two booleans. `_option_forms` deliberately over-generates (safe for a refusal table,
# where more matches means more refusals) and must NOT be used to decide what a value MEANS
# - it reports `-e` for `-fescape`, which is how `-fescape` was once read as a pattern.
_GREP_VALUE_LETTERS = "efmABCD"


def _short_option_value(token: str) -> tuple[str, str]:
    """(value-taking letter, attached value) for a short-option token, else ("", "")."""
    if token.startswith("--") or not token.startswith("-"):
        return "", ""
    for position, letter in enumerate(token[1:], start=1):
        if letter in _GREP_VALUE_LETTERS:
            return letter, token[position + 1 :]
        if not letter.isalnum():
            break
    return "", ""


def _pattern_positions(stage: Stage) -> set[int]:
    """Indexes whose contents are a PATTERN (data), not a path this tool will open."""
    exempt: set[int] = set()
    supplied = False
    index = 1
    while index < len(stage.argv):
        token = stage.argv[index]
        long_head = token.split("=", 1)[0] if token.startswith("--") else ""
        letter, attached = _short_option_value(token)
        is_pattern = long_head in _PATTERN_VALUE_FLAGS or letter == "e"
        is_file = long_head in _PATTERN_FILE_FLAGS or letter == "f"
        if is_pattern or is_file:
            supplied = True
            if attached or (token.startswith("--") and "=" in token):
                if is_pattern:
                    exempt.add(index)  # `-epattern` / `--regexp=pattern`: the token is data
            else:  # the value is the NEXT argument
                if is_pattern:
                    exempt.add(index + 1)
                index += 1  # ...and either way it is not a positional
        elif letter:
            # some other value-taking option (`-m5`, `-A 3`): its value is not a path,
            # and a detached one must not be mistaken for the positional pattern
            if not attached:
                index += 1
        index += 1
    if not supplied:
        for index, token in enumerate(stage.argv[1:], start=1):
            if not token.startswith("-"):
                exempt.add(index)  # the bare form: the first operand is the pattern
                break
    return exempt


# Splits a flag token into its option part and whatever is attached to it. Short options
# take attached values with no separator - `sort -o../outside` is `-o` plus `../outside` -
# so a check that only understood `--opt=value` never saw the path at all.
_OPTION_SPLIT = re.compile(r"^(?P<dashes>-{1,2})(?P<name>[A-Za-z0-9][A-Za-z0-9-]*)?=?(?P<rest>.*)$")


def _option_forms(token: str) -> list[str]:
    """Every option name a token could be naming. `-ni` is `-n` AND `-i`; `--x=1` is `--x`."""
    if not token.startswith("-") or token == "-" or token == "--":
        return []
    if token.startswith("--"):
        return [token.split("=", 1)[0]]
    forms = [token.split("=", 1)[0]]
    for letter in token[1:]:
        if not letter.isalnum():
            break  # an attached value has begun; the letters before it are the options
        forms.append(f"-{letter}")
    return forms


def _attached_values(token: str) -> list[str]:
    """Every value a flag token could be carrying.

    Short options take attached values with no separator and no way, without per-tool
    arity, to know where the option letters stop and the value starts: `-fescape` is `-f
    escape`, and `-rn` is two flags with no value at all. An earlier draft guessed by
    matching alphanumerics greedily, which read `-fescape` as one long option name and
    missed the path entirely - and read `-fC:\\host\\secrets` as the option `-fC`.

    So it does not guess. It returns EVERY suffix, and the callers are both safe under
    over-generation: the lexical check only fires on something shaped like an escaping
    path, and the resolved check only fires on something that actually exists in the tree.
    """
    if token.startswith("--"):
        head, sep, value = token.partition("=")
        return [value] if sep and value else []
    body = token[1:]
    values = [body[index:] for index in range(1, len(body))]
    if "=" in token:
        values.append(token.split("=", 1)[1])
    return [value for value in values if value]


def _attached_value(token: str) -> str:
    """The most likely single attached value - the whole remainder after the first letter."""
    values = _attached_values(token)
    return values[0] if values else ""


def _escapes_sandbox(token: str) -> bool:
    """True when `token` names somewhere the sandbox does not contain.

    `..` is checked as a path COMPONENT, so git's revision ranges (`main..HEAD`,
    `origin/main..HEAD`) are untouched - the `..` there is not a directory. Flags are
    checked through their ATTACHED value as well as their `=` value, because `-o../out`
    and `--output=../out` are the same instruction written two ways.
    """
    values = [token] if not token.startswith("-") else _attached_values(token)
    for value in values:
        if not value:
            continue
        if _ABSOLUTE_PATH.match(value) or ".." in re.split(r"[\\/]", value):
            return True
    return False


def _screen_paths(stage: Stage, cwd: Path | None = None) -> Trip | None:
    """Refuse any argument that reaches outside the sandbox clone."""
    name = stage.argv[0]
    if name in _NON_READING_COMMANDS:
        return None
    exempt = _pattern_positions(stage) if name in _PATTERN_FIRST else set()
    for index, token in enumerate(stage.argv[1:], start=1):
        if index in exempt:
            continue
        if name == "sed" and token in _sed_scripts(stage.argv):
            continue  # the script is a program, and it has its own grammar check
        if _escapes_sandbox(token):
            return Trip(
                "A",
                "path-outside-sandbox",
                f"'{token}' names a path outside the sandbox",
            )
        if cwd is not None and _resolves_outside(token, cwd):
            return Trip(
                "A",
                "path-outside-sandbox",
                f"'{token}' resolves to a path outside the sandbox",
            )
    return None


def _resolves_outside(token: str, cwd: Path) -> bool:
    """True when an operand that EXISTS in the sandbox actually points out of it.

    The lexical check catches `../secret` and `/etc/passwd`. It cannot catch a symlink:
    `escape -> /host/secret` is a plain relative name, and only resolving it says
    otherwise. This runs where `cwd` is known - at execution - so `screen_command` alone
    stays lexical, and `run_guarded` is where the resolved leg applies.
    """
    # A flag's ATTACHED value is a path too: `grep --file=escape` and `grep -fescape` both
    # open `escape`. Checking only bare operands left every attached form uncovered.
    values = _attached_values(token) if token.startswith("-") else [token]
    try:
        root = cwd.resolve()
    except OSError:  # pragma: no cover
        return True
    for value in values:
        if not value:
            continue
        candidate = cwd / value
        if not os.path.lexists(candidate):
            continue  # not a path in this tree, so it is data, not an operand
        try:
            resolved = candidate.resolve()
        except OSError:  # pragma: no cover - a resolve that fails is not proof of safety
            return True
        if resolved != root and root not in resolved.parents:
            return True
    return False


def _screen_git(stage: Stage) -> Trip | None:
    """Parse a git command line properly, then allow only read subcommands.

    The bypass this replaces: the old screen took the first argument not starting with `-`
    as the subcommand, so `git -C . config --global user.name x` offered it `.` - an
    OPERAND of `-C`, not a subcommand - and then ran a global config write. Options and
    their operands have to be told apart before anything about the subcommand is true.
    """
    for token in stage.argv[1:]:
        if token.split("=", 1)[0] in _GIT_ANY_HELPER_OPTIONS:
            return Trip("A", "git-helper", f"'{token}' hands git's work to another program")

    index = 1
    while index < len(stage.argv):
        token = stage.argv[index]
        if not token.startswith("-"):
            break
        head = token.split("=", 1)[0]
        if head in _GIT_PRE_HELPER_OPTIONS:
            return Trip("A", "git-helper", f"'{token}' hands git's work to another program")
        if head in _GIT_RELOCATING_OPTIONS:
            return Trip("A", "git-relocated", f"'{head}' moves or reconfigures git itself")
        if token in _GIT_BARE_OPTIONS:
            index += 1
            continue
        return Trip("A", "git-relocated", f"'{token}' is not a recognised git pre-command option")
    if index >= len(stage.argv):
        return None  # bare `git`, or `git --version`: prints usage, changes nothing

    if stage.globbable[index]:
        # A glob in git's SUBCOMMAND slot could expand to `commit`. Elsewhere on a git
        # command line a glob is an ordinary pathspec and stays allowed.
        return Trip("A", "glob-in-command-position", "the git subcommand may not be a glob")

    subcommand = stage.argv[index]
    rest = stage.argv[index + 1 :]
    if subcommand in _GIT_READ_SUBCOMMANDS:
        return None

    operands = [token for token in rest if not token.startswith("-")]
    flags = [token.split("=", 1)[0] for token in rest if token.startswith("-")]

    if subcommand in _GIT_ONE_OPERAND_READS:
        if len(operands) > 1:
            return Trip("A", "git-write", f"git {subcommand} with two operands writes")
        if flags:
            return Trip("A", "git-write", f"git {subcommand} takes no flags in its read form")
        return None

    if subcommand not in _GIT_LISTING_WHEN_BARE:
        return Trip("A", "git-write", f"git {subcommand} is not in the read-only surface")

    allowed_flags = _GIT_LISTING_READ_FLAGS.get(subcommand, frozenset())
    unknown = [flag for flag in flags if flag not in allowed_flags]
    if unknown:
        return Trip("A", "git-write", f"git {subcommand} {unknown[0]} is not a read form")

    if subcommand == "config":
        # `git config --list` reads; `git config --global user.name x` writes. The read
        # forms all carry a get/list flag and name at most the key.
        if not set(flags) & _GIT_CONFIG_READ_FLAGS or len(operands) > 1:
            return Trip("A", "git-write", "git config is available only in its read forms")
        return None
    if operands:
        return Trip("A", "git-write", f"git {subcommand} with an operand mutates state")
    return None


# sed's script is a small language, and two of its commands leave the sandbox: `w`
# writes a file at any path, and GNU's `e` executes a command. Neither is a flag, so the
# `-i` refusal never saw them. Rather than blocklisting letters inside a language that can
# quote them, the script must MATCH a read-only grammar: optional address or range, then
# print/delete/quit/line-number, or a substitution whose flags carry no `w` and no `e`.
_SED_ADDR = r"(?:\d+|\$|/(?:\\.|[^/\\])*/)"
_SED_RANGE = rf"{_SED_ADDR}(?:\s*,\s*{_SED_ADDR})?"
_SED_PRINT = re.compile(rf"^\s*(?:{_SED_RANGE}\s*)?!?\s*[pdq=]?\s*$")
_SED_SUBST = re.compile(
    rf"^\s*(?:{_SED_RANGE}\s*)?!?\s*s(?P<d>[^\w\s])"
    r"(?:\\.|(?!(?P=d)).)*(?P=d)(?:\\.|(?!(?P=d)).)*(?P=d)[gpiImM0-9]*\s*$"
)


# sed short options that consume a value, either attached to the letter or as the next
# argument. `-e` is the one that carries a PROGRAM, and it is the one an earlier draft of
# this parser missed in its attached form: `sed -e'1w /tmp/out' file` looks like a flag
# bundle, so no script was extracted and the grammar check ran over nothing.
_SED_VALUE_LETTERS = "eflis"
_SED_FORBIDDEN_LETTERS = "fi"


def _sed_scripts(argv: tuple[str, ...]) -> list[str]:
    """Every argument sed will treat as a program, in every form sed accepts."""
    scripts, _forbidden = _parse_sed(argv)
    return scripts


def _parse_sed(argv: tuple[str, ...]) -> tuple[list[str], str | None]:
    """Return (scripts, first forbidden short option). Handles attached and bundled forms."""
    scripts: list[str] = []
    expecting: str | None = None
    have_bare_script = False
    for token in argv[1:]:
        if expecting is not None:
            if expecting == "e":
                scripts.append(token)
            expecting = None
            continue
        if token == "--":
            continue
        if token.startswith("--"):
            head, sep, value = token.partition("=")
            if head == "--expression":
                if sep:
                    scripts.append(value)
                else:
                    expecting = "e"
                continue
            if head in ("--file", "--in-place"):
                return scripts, head
            continue
        if token.startswith("-") and len(token) > 1:
            rest = token[1:]
            while rest:
                letter, rest = rest[0], rest[1:]
                if letter in _SED_FORBIDDEN_LETTERS:
                    return scripts, f"-{letter}"
                if letter in _SED_VALUE_LETTERS:
                    if rest:  # attached value: `-e1w /tmp/out`
                        if letter == "e":
                            scripts.append(rest)
                        rest = ""
                    else:  # detached value: `-e` then the next argument
                        expecting = letter
                    break
            continue
        if not have_bare_script and not scripts:
            scripts.append(token)  # the bare form: `sed -n '1,3p' FILE`
            have_bare_script = True
    return scripts, None


def _screen_sed(stage: Stage) -> Trip | None:
    scripts, forbidden = _parse_sed(stage.argv)
    if forbidden is not None:
        return Trip("A", "forbidden-argument", f"'{forbidden}' gives sed an exec or write mode")
    for script in scripts:
        if not _sed_script_is_read_only(script):
            return Trip(
                "A",
                "sed-script-not-read-only",
                "only address/print/substitute sed scripts are available here",
            )
    return None


def _sed_script_is_read_only(script: str) -> bool:
    """True when every `;`-separated command matches the read-only grammar.

    The split is naive, so a substitution whose pattern contains `;` is refused rather than
    admitted. That is the correct direction for a guard to be wrong in.
    """
    parts = [part for part in script.split(";")]
    return all(_SED_PRINT.match(part) or _SED_SUBST.match(part) for part in parts)


def screen_command(command: str, denied_names: set[str] | None = None) -> Trip | None:
    """Refuse a command before it runs. Returns None when the command may proceed."""
    return screen_pipeline(command, denied_names)[0]


def _expand_globs(stage: Stage, cwd: Path) -> Stage:
    """Expand unquoted globs against the sandbox, returning a fully-literal Stage.

    Unmatched patterns are passed through literally, which is bash's default (nullglob off)
    and is what keeps `git show <sha> -- 'docs/**'` working when nothing matches. The result
    is re-screened by the caller, so expansion cannot smuggle anything past the policy.
    """
    expanded: list[str] = []
    for word, globbable in zip(stage.argv, stage.globbable):
        if not globbable:
            expanded.append(word)
            continue
        # A pattern may only reach INTO the sandbox. An absolute or `..`-bearing pattern
        # would otherwise enumerate the host filesystem from a command that named nothing
        # outside the tree, which is a disclosure the caller never asked to authorise.
        if Path(word).is_absolute() or ".." in Path(word).parts:
            expanded.append(word)
            continue
        matches = sorted(glob.glob(word, root_dir=str(cwd)))
        expanded.extend(matches if matches else [word])
    return Stage(
        tuple(expanded),
        (False,) * len(expanded),
        stage.drop_stdout,
        stage.drop_stderr,
    )


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
    # Every stage's exit code, not just the last. A pipeline reports its FINAL status, so
    # `cat missing | wc -l` succeeds with "0" while the read it was doing failed - which is
    # how a positive control passes having demonstrated nothing.
    stage_returncodes: tuple[int, ...] = ()

    @property
    def pipeline_failed(self) -> bool:
        """True when ANY stage exited non-zero, including one whose failure was swallowed."""
        return any(code != 0 for code in self.stage_returncodes)

    def as_dict(self) -> dict[str, object]:
        return {
            "command": self.command,
            "returncode": self.returncode,
            "stage_returncodes": list(self.stage_returncodes),
            "refused": self.refused,
            "trip": None if self.trip is None else {"layer": self.trip.layer, "kind": self.trip.kind},
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


def _resolve_executable(name: str, env: dict[str, str], sandbox_root: Path) -> str | None:
    """Find `name` on the trusted PATH and refuse anything reachable from the sandbox.

    Bare names are resolved by the OS at exec time, and on Windows `CreateProcess` searches
    the CURRENT DIRECTORY first - which is the sandbox. A candidate that writes `git.exe`
    into the tree it is allowed to write in would then BE git. Resolving to an absolute
    path here means the OS searches nothing, and refusing a resolution that lands inside
    the sandbox root closes the same door on PATH.

    The honest limit: this trusts the PATH the session was started with. If that is already
    hostile, so is everything else on the machine, and no guard inside one process fixes it.
    """
    found = shutil.which(name, path=env.get("PATH"))
    if found is None:
        return None
    resolved = _resolve(Path(found))
    if _is_contained(resolved, sandbox_root) or resolved == sandbox_root:
        return None
    return str(resolved)


def _require_provisioned(sandbox: Sandbox | Path, cwd: Path, sandbox_root: Path | None = None) -> Path:
    """Prove the cwd is a real sandbox before ANY guarded command runs.

    Hardening `_load` hardened the CLI. It did nothing for a direct caller, and
    `run_guarded` accepts a bare `Path` - so `run_guarded(cmd, Path("/somewhere"))` ran the
    command with that as `cwd` and read the host through relative operands. The check
    belongs at the execution boundary, where every route passes through it, not at one of
    the routes into it.
    """
    resolved = _resolve(cwd)
    nonce = sandbox.nonce if isinstance(sandbox, Sandbox) else ""
    # The root comes from the caller, or from a Sandbox that `provision`/`_load` already
    # verified, or from the configured default - never from metadata inside the tree being
    # judged, which would be the boundary asking the suspect where the boundary is.
    root = sandbox_root
    if root is None and isinstance(sandbox, Sandbox) and sandbox.sandbox_root is not None:
        root = sandbox.sandbox_root
    root = _resolve(root) if root is not None else _resolve(default_sandbox_root())
    verify_provenance(resolved, root, expected_nonce=nonce or None)
    return root


def run_guarded(
    command: str,
    sandbox: Sandbox | Path,
    *,
    denied_names: set[str] | None = None,
    sandbox_root: Path | str | None = None,
    timeout: int = 120,
    max_output_bytes: int = 100_000,
) -> GuardedResult:
    """Run one command inside the sandbox, with both guard layers applied and NO shell.

    Every stage is executed with `shell=False` from an argv list that was itself screened,
    so nothing between the check and the exec can reinterpret the string.
    """
    # A bare `Path` - or a Sandbox someone built by hand - carries no denylist, and an
    # empty denylist is not a milder guard: Layer A stops refusing commands that NAME a
    # stripped artifact and Layer B stops refusing output that DISCLOSES one, so
    # `git log --stat -1` hands back the pack's path. The manifest is on disk inside the
    # sandbox and `_load` verifies it, so the fix is to go and read it rather than to
    # proceed with nothing.
    if not isinstance(sandbox, Sandbox) or not (sandbox.denied or sandbox.removed):
        target = sandbox.path if isinstance(sandbox, Sandbox) else Path(sandbox)
        known_root = sandbox_root
        if known_root is None and isinstance(sandbox, Sandbox):
            known_root = sandbox.sandbox_root
        sandbox = _load(str(target), None, str(known_root) if known_root else None)
    cwd = sandbox.path
    names = denied_names if denied_names is not None else sandbox.denied_names()
    verified_root = _require_provisioned(
        sandbox, cwd, Path(sandbox_root) if sandbox_root else None
    )

    trip, stages = screen_pipeline(command, names)
    if trip is not None:
        return GuardedResult(command, REFUSAL_EXIT, "", REFUSAL_TEXT, refused=True, trip=trip)

    # Expansion changes argv, so the WHOLE policy runs again over the result - the content
    # check (a pattern that names nothing forbidden can still MATCH something forbidden)
    # and the structural one (a glob must not have chosen the program or the subcommand).
    expanded = [_expand_globs(stage, cwd) for stage in stages]
    trip = _screen_words(" ".join(word for stage in expanded for word in stage.argv), names)
    if trip is None:
        trip = screen_stages(expanded, cwd)
    if trip is not None:
        return GuardedResult(command, REFUSAL_EXIT, "", REFUSAL_TEXT, refused=True, trip=trip)

    # Stages run in sequence, each fed the previous stage's stdout, rather than as
    # concurrently-piped processes: with every stream captured, concurrent pipes deadlock
    # on a full buffer, and the read surface here is small and bounded by `timeout`. The
    # visible difference from a real pipeline is that `head -5` does not terminate its
    # upstream early - it truncates instead.
    piped = ""
    stderr_parts: list[str] = []
    stage_codes: list[int] = []
    returncode = 0
    remaining = float(timeout)
    env = _child_env()
    for stage in expanded:
        argv = list(stage.argv)
        # Resolve the program HERE, from the trusted PATH, and hand the OS an absolute
        # path so it searches nothing - the sandbox least of all.
        program = _resolve_executable(argv[0], env, verified_root)
        if program is None:
            return GuardedResult(
                command, 127, "", f"sandbox guard: command not found: {argv[0]}", refused=False
            )
        argv[0] = program
        started = time.monotonic()
        try:
            proc = subprocess.run(
                argv,
                shell=False,
                cwd=str(cwd),
                env=env,
                input=piped,
                capture_output=True,
                text=True,
                # The child speaks UTF-8; without this the decode falls back to the
                # platform codepage (cp1252 here) and delivers mojibake for every
                # non-ASCII byte -- on an item set that scores em dashes verbatim.
                encoding="utf-8",
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
        stage_codes.append(proc.returncode)
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
    return GuardedResult(
        command, returncode, stdout, stderr, refused=False, stage_returncodes=tuple(stage_codes)
    )


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
        passed = outcome == expect
        if res.trip is not None:
            detail = f"layer {res.trip.layer}: {res.trip.kind}"
        elif expect == "allowed":
            # A positive control that is merely NOT REFUSED proves nothing: a missing file,
            # a sha that is not in this clone, or a pipeline whose first stage failed all
            # produce "allowed" with no output. The control exists to show the instrument
            # still works, so it has to have worked.
            detail = f"rc={res.returncode}, {len(res.stdout)} bytes"
            if res.pipeline_failed:
                # EVERY stage, not just the last. `cat missing | wc -l` exits 0 with "0",
                # so a final-status check calls it a pass while the read it existed to
                # demonstrate never happened - and the default V8 control is a pipeline.
                codes = ",".join(str(code) for code in res.stage_returncodes)
                passed, detail = False, f"{detail} - a stage failed (rc per stage: {codes})"
            elif not res.stdout.strip():
                passed, detail = False, f"{detail} - no output, so it demonstrated nothing"
        results.append(ProbeVector(name, command, expect, outcome, passed, detail))
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
    p_probe.add_argument("--sandbox-root", default=None)

    p_exec = sub.add_parser("exec", help="run one guarded command in a sandbox")
    p_exec.add_argument("--sandbox", required=True)
    p_exec.add_argument("--manifest", default=None)
    p_exec.add_argument("--sandbox-root", default=None)
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
        sandbox = _load(args.sandbox, args.manifest, args.sandbox_root)
        vectors = probe(sandbox)
        for vec in vectors:
            flag = "PASS" if vec.passed else "FAIL"
            print(f"{flag}  {vec.name:<52} expect={vec.expect:<8} got={vec.outcome:<8} {vec.detail}")
        failed = [v for v in vectors if not v.passed]
        print(f"\nprobe: {len(vectors) - len(failed)}/{len(vectors)} vectors as expected")
        return 1 if failed else 0

    if args.cmd == "exec":
        sandbox = _load(args.sandbox, args.manifest, args.sandbox_root)
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


def _load(sandbox_path: str, manifest_path: str | None, sandbox_root: str | None = None) -> Sandbox:
    """Rehydrate a Sandbox from disk, PROVING first that it is one.

    There is deliberately no degraded mode. An earlier draft accepted any directory,
    printed "Layer A path screening is degraded", and carried on - but `exec` runs its
    command with that directory as `cwd`, so pointing it at an unprovisioned tree does not
    degrade the guard, it removes it: every relative operand then reads a directory nobody
    stripped. A warning is not a substitute for the check it warns about.
    """
    path = Path(sandbox_path)
    # The boundary is established BEFORE anything is read, and it is NOT taken from the
    # manifest: inferring the containment root from the file whose legitimacy is in
    # question is circular, and it let `_load` open a regular manifest sitting in any
    # directory `--sandbox` happened to name. The root comes from the caller, the
    # environment, or the default - the three places that are not under the tree's control.
    root = _resolve(sandbox_root) if sandbox_root else _resolve(default_sandbox_root())
    resolved = _resolve(path)
    if path.is_symlink():
        raise RuntimeError(f"refused: {path} is a symlink, not a sandbox directory")
    if not _is_contained(resolved, root):
        raise RuntimeError(
            f"refused: {resolved} is outside the configured sandbox root {root}; nothing "
            f"there is read, including its metadata"
        )
    expected = _resolve(path / MANIFEST_RELPATH)
    candidate = Path(manifest_path) if manifest_path else path / MANIFEST_RELPATH
    if manifest_path is not None and _resolve(candidate) != expected:
        # `--manifest` was a way to read any file on the host through `exec`'s own control
        # path: `_load` opened it before anything had been proven about it. A manifest that
        # is not THIS sandbox's manifest is not a manifest, so the option can only ever
        # name the in-tree one - and now it has to.
        raise RuntimeError(
            f"refused: {candidate} is not {path}'s own manifest; the manifest is read from "
            f"inside the sandbox ({MANIFEST_RELPATH}), never from a path handed in"
        )
    raw = read_metadata_file(path, MANIFEST_RELPATH)
    if raw is None:
        raise RuntimeError(
            f"refused: {path} carries no run manifest ({MANIFEST_RELPATH}) that is genuinely "
            f"its own; it was not provisioned by this tool, so it is not a sandbox to run "
            f"commands in"
        )
    data = json.loads(raw)
    sandbox = Sandbox(
        path=path,
        source=Path(data["source"]),
        head=data["head"],
        strip_commit=data["strip_commit"],
        removed=list(data["removed"]),
        redacted=dict(data["redacted"]),
        postcondition_clean=bool(data["postcondition_clean"]),
        residual=dict(data.get("residual", {})),
        denied=list(data.get("denied", [])),
        sandbox_root=root,
        nonce=str(data.get("nonce", "")),
    )
    verify_provenance(resolved, root, expected_nonce=sandbox.nonce or None)
    if not sandbox.postcondition_clean:
        raise RuntimeError(
            f"refused: {path} did not pass provisioning's own postcondition, so its tree is "
            f"not known to be free of answer-key content"
        )
    return sandbox


if __name__ == "__main__":
    raise SystemExit(main())
