#!/usr/bin/env python
"""fleet_analytics.py — [#384] L5a descriptive fleet analytics: hotspots, change coupling, rot.

Mines the fleet's OWN git history to answer three questions no static tool can:
  1. HOTSPOTS       — where does change pressure concentrate? (a power law in every codebase)
  2. CHANGE COUPLING— what silently co-changes? (learned TEMPORAL dependencies)
  3. ROT            — what has gone stale while other files still point at it?

This is the DESCRIPTIVE layer only (intake #16 §3 "L5a"). NO ML, NO predictive scoring —
L5b is explicitly gated on these frames showing signal volume. The SIEM ruling stands: this
READS event data (git history), it does not resurrect an ingestion pipeline.

Layer-2 / read-only contract (ADR-28/36): reads the hub + every registered sibling repo,
writes ONLY `.dev-knowledge/logs/FLEET-ANALYTICS.md` (gitignored), never mutates a child
file. Reporter, NOT a gate — deliberately NOT registered in `audit.ALL_CHECKS`, so it never
reddens the ship-gate; it only REUSES the LOCKED `Finding` shape as its output contract.
Fail-soft everywhere: ASCII-only output, `main()` always returns 0, an unreadable repo is
`unavailable`, never a crash.

Reuse (no second traversal): `audit.discover_repos()` (the one deterministic fleet
enumerator), `audit.load_state()`, `audit.Finding`, and `audit._git_location_env()` (the
DERIVED git-env scrub). Unlike `boundary_report.py` — which SKIPS the hub because the hub is
its diff baseline — this script MUST INCLUDE the hub as a mining target; `ecosystem/` holds
only the 5 consumers, so `enumerate_fleet()` prepends the hub explicitly.

Loose top-level script BY DESIGN: the codemap only walks `scripts/<pkg>/` dirs with an
`__init__.py`, so a loose module adds no codemap node and never forces an ARCHITECTURE.md
regen.

------------------------------------------------------------------------------------
TWO DELIBERATE, EVIDENCE-BACKED DEVIATIONS FROM THE LITERAL SPEC. Both are documented
here rather than shipped silently, because this repo's own §12 history (CLAUDE.md v2.44)
records the defect class of overriding a written spec on unstated judgment.

D1 — TOOL: `git log --numstat`, NOT PyDriller (intake §3 names PyDriller -> pandas).
  Measured on this fleet, 2026-07-22:
    - `git log --numstat` over the whole hub (2867 non-merge commits): 3.0 s.
      PyDriller's GitPython commit-object traversal is ~60x slower, and it is not installed.
    - PyDriller's one differentiating feature over a numstat parse is per-file CYCLOMATIC
      complexity via `lizard`, which returns None for markdown. This fleet is ~70% markdown
      (hub 1145 .md / 180 .py; ai-council 136/85; corp-monorepo 194/426), so that axis would
      be null for the majority of ranked files.
    - CodeScene — the model intake §3 ACTUALLY CITES — does not use cyclomatic complexity.
      It uses INDENTATION-based complexity, precisely because it is language-agnostic.
  So the deviation is FROM THE TOOL NAME, TOWARD THE CITED MODEL. Operator-ruled at the
  #384 plan gate.

D2 — COMPLEXITY UNIT: `weighted_lines = sum(1 + indent_units)` over non-blank lines, NOT
  CodeScene's `sum(indent_units)`.
  Reason: in a 1145-markdown corpus a flat 2000-line prose doc has sum(indent) == 0, so
  `score = revisions * 0 == 0` and it could NEVER rank however hot it runs. The `+1` per
  line makes the metric size-plus-depth: strictly monotone in size, with an indentation
  surcharge on top. In a docs-heavy corpus that is the honest thing to measure. This is a
  documented departure — do NOT read this column as CodeScene complexity.
------------------------------------------------------------------------------------

HONEST LIMITS (also rendered into the digest, which is what actually gets read):
  1. The rot frame's "dependency" is a TEXTUAL inbound reference, not a semantic one. A path
     mentioned in a changelog entry, inside a code fence, or in a "do not use X" warning
     counts identically to a live dependency.
  2. It is a LOWER BOUND by construction: only path-shaped tokens match. Python `import`s,
     package paths, and references by concept are invisible. This is deliberate
     precision-over-recall — matching bare stems against prose in a knowledge-base repo is a
     false-positive machine, and a module-path matcher would be exactly the repo-SHAPE
     presumption the live polyrepo brake forbids.
  3. Ambiguous basenames (measured: 71 in the hub — PROBES.md x56, HANDOFF_BOOT.md x54)
     resolve to their shortest unique path suffix; where no proper suffix is unique, only
     the full path counts, so those files are undercounted further.
  4. STALENESS IS NOT ROT. A stable, correct, finished file is indistinguishable from an
     abandoned one by git dates alone. This frame is a REVIEW QUEUE, NOT A VERDICT.
  5. `-w` catches whitespace-only edits, not trivial-but-textual ones (typos, date stamps).
  6. Cross-repo references are invisible: a hub protocol cited by corp-ops docs shows 0
     inbound in the hub's own scan. Highest-value v2 follow-up.
  7. Complexity is computed on CURRENT HEAD content, not historical — a file that was
     complex and got simplified reads at its simplified size.
  8. No comment stripping: comment syntax is language-specific, and a stripper would be a
     shape presumption. CodeScene's published model is whitespace-only too.
  9. A file with NO meaningful-edit record — only ever touched inside a wide commit, or
     never with more than `min_meaningful_churn` lines — is invisible to the rot frame
     entirely. Measured 44/1432 in the hub on first run, so this is not hypothetical; the
     count is surfaced per repo as `files_no_edit_record` rather than left silent.
 10. The rot frame cannot see further back than the repo is old. The hub's oldest meaningful
     edit is ~113 days, so at `min_age_days=180` it correctly reports zero rot — an absence
     of findings here means "too young to have rotted", NOT "audited clean".
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_LOGS_DIR = _REPO_ROOT / "logs"
_ANALYTICS_FILE = _LOGS_DIR / "FLEET-ANALYTICS.md"

# Reuse the LOCKED audit contract, the single deterministic fleet enumerator, and the
# DERIVED git-env scrub. See _scrubbed_git_env() for why we import rather than re-derive.
sys.path.insert(0, str(_SCRIPTS_DIR))
import audit  # noqa: E402

Finding = audit.Finding

_CHECK = "fleet_analytics"
_SCHEMA_VERSION = 1

_FM_RE = re.compile(r"^([a-z_]+):\s*(.*)$")

# Files whose co-change / reference signal is mechanical, not designed. `audit.py` rewrites
# every ecosystem/<n>/state.yaml on EVERY run, so without this exclude those 5 files
# co-change ~100% forever and own the entire coupling frame ([#384] R4).
_DEFAULT_EXCLUDE = (
    "**/ecosystem/*/state.yaml",
    "**/ecosystem/index.yaml",
    "logs/**",
    "**/package-lock.json",
    "**/poetry.lock",
    "**/*.lock",
    "**/*.min.js",
    "**/dist/**",
    "**/build/**",
    "**/node_modules/**",
    "**/.venv/**",
)

# Basenames so generic that even a repo-unique occurrence is unsafe to match in prose.
# These contribute their FULL PATH as a token and nothing shorter.
_BASENAME_STOPLIST = frozenset({
    "README.md", "__init__.py", "index.md", "index.html", "CLAUDE.md",
    "LICENSE", "LICENSE.md", "Makefile", "setup.py", "conftest.py", "__main__.py",
})

# A path-shaped token: optional dir components, then a name with a short extension.
_TOKEN_RE = re.compile(r"(?:[\w.\-]+[/\\])*[\w\-]+\.[A-Za-z0-9]{1,8}")


# ============================================================================
# Pure helpers (unit-tested directly; no git, no filesystem, no clock)
# ============================================================================

@dataclass(frozen=True)
class FileChange:
    path: str
    old_path: Optional[str]
    added: int
    deleted: int
    binary: bool


@dataclass(frozen=True)
class CommitRec:
    sha: str
    ts: int              # committer date -- matches what `--since` filters on
    author_ts: int
    subject: str
    changes: tuple[FileChange, ...]


@dataclass(frozen=True)
class IndentProfile:
    n_lines: int         # non-blank lines
    total_indent: int    # sum of indent units (the pure CodeScene quantity)
    max_indent: int
    mean_indent: float
    weighted_lines: int  # sum(1 + indent_units) -- the D2 deviation, what we actually rank


@dataclass
class Config:
    """Every threshold, in one place. Printed into the digest so a report is self-describing."""
    window_days: int = 365
    top_n: int = 15              # per-repo cut
    fleet_top: int = 25          # fleet roll-up cut
    max_commit_files: int = 30
    min_revisions: int = 5
    min_co: int = 5
    min_degree: float = 0.30
    min_jaccard: float = 0.20
    min_refs: int = 2
    min_age_days: int = 180
    tab_width: int = 4
    indent_unit: int = 4
    min_meaningful_churn: int = 3
    index_referrer_cut: int = 50
    max_file_bytes: int = 2_000_000
    exclude: tuple[str, ...] = _DEFAULT_EXCLUDE


def _safe(evidence: str) -> str:
    """Evidence is markdown-table-safe per the LOCKED Finding contract (no literal `|`)."""
    return evidence.replace("|", "/")


def excluded(path: str, patterns: tuple[str, ...]) -> bool:
    """True if `path` (repo-relative posix) matches any exclude glob.

    `**/x` also matches `x` at the root — fnmatch alone would require a leading component.
    """
    for pat in patterns:
        if fnmatch.fnmatch(path, pat):
            return True
        if pat.startswith("**/") and fnmatch.fnmatch(path, pat[3:]):
            return True
    return False


# ---------------------------------------------------------------------------
# The numstat parse
# ---------------------------------------------------------------------------

def parse_numstat_stream(raw: bytes) -> tuple[list[CommitRec], list[str]]:
    """Parse `git log --numstat -z` output -> (commits, parse_anomalies).

    Token grammar under `-z` (VERIFIED live against this repo, 2026-07-22):
      "\\x01<sha>\\x02<ct>\\x02<at>\\x02<subject>"  -> commit header
      "<adds>\\t<dels>\\t<path>"                    -> a normal change record
      "<adds>\\t<dels>\\t"  (path EMPTY)            -> a RENAME: the next TWO tokens are
                                                       (old_path, new_path)
      adds/dels == "-"                              -> a binary file
    `-z` is load-bearing: it eliminates the `{a => b}` and `a => b` rename forms AND
    core.quotepath escaping in one move. Without it all three are live bug surfaces (the
    brace form is real: 146 occurrences in 40 rename commits of this repo).

    NEVER raises on unexpected input — an unrecognized token is appended to the anomaly list
    and surfaced in the digest. A silent skip is precisely how a format assumption breaks
    without anyone noticing.
    """
    commits: list[CommitRec] = []
    anomalies: list[str] = []
    if not raw:
        return commits, anomalies

    tokens = raw.split(b"\0")
    cur: Optional[dict] = None
    changes: list[FileChange] = []
    i = 0

    def _flush() -> None:
        if cur is not None:
            commits.append(CommitRec(cur["sha"], cur["ts"], cur["at"], cur["subject"],
                                     tuple(changes)))

    while i < len(tokens):
        tok = tokens[i].decode("utf-8", "replace").lstrip("\n")
        i += 1
        if not tok:
            continue
        if tok.startswith("\x01"):
            _flush()
            changes = []
            parts = tok[1:].split("\x02", 3)
            if len(parts) != 4:
                anomalies.append(f"malformed header: {tok[:60]!r}")
                cur = None
                continue
            sha, ct, at, subject = parts
            try:
                cur = {"sha": sha, "ts": int(ct), "at": int(at), "subject": subject}
            except ValueError:
                anomalies.append(f"non-integer timestamp: {tok[:60]!r}")
                cur = None
            continue
        if cur is None:
            anomalies.append(f"record before any header: {tok[:60]!r}")
            continue

        fields = tok.split("\t", 2)
        if len(fields) != 3:
            anomalies.append(f"unrecognized record: {tok[:60]!r}")
            continue
        adds_s, dels_s, path = fields
        binary = adds_s == "-" or dels_s == "-"
        added = 0 if binary else _int_or_none(adds_s)
        deleted = 0 if binary else _int_or_none(dels_s)
        if added is None or deleted is None:
            anomalies.append(f"non-integer numstat: {tok[:60]!r}")
            continue

        old_path = None
        if path == "":
            # Rename: consume the next two tokens as (old, new).
            if i + 1 >= len(tokens):
                anomalies.append("truncated rename record at end of stream")
                continue
            old_path = tokens[i].decode("utf-8", "replace").lstrip("\n")
            path = tokens[i + 1].decode("utf-8", "replace").lstrip("\n")
            i += 2
            if not path:
                anomalies.append(f"rename with empty new path (old={old_path!r})")
                continue

        changes.append(FileChange(_posix(path), _posix(old_path) if old_path else None,
                                  added, deleted, binary))

    _flush()
    return commits, anomalies


def _int_or_none(s: str) -> Optional[int]:
    try:
        return int(s)
    except ValueError:
        return None


def _posix(p: str) -> str:
    """Normalize a path token to repo-relative posix. Strips a leading `./` PREFIX -- note
    `lstrip("./")` would strip leading `.` and `/` CHARACTERS, mangling dotfiles."""
    p = p.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p


def build_rename_alias(commits: list[CommitRec]) -> dict[str, str]:
    """old_path -> newer_path, from a NEWEST-FIRST commit list (git's natural walk order).

    Newest-first is load-bearing and makes this single-pass: when a rename is seen at commit
    C, every OLDER record already uses `old`, so recording alias[old] = new is enough.
    Building this oldest-first would need two passes.
    """
    alias: dict[str, str] = {}
    for c in commits:
        for ch in c.changes:
            if ch.old_path and ch.old_path != ch.path:
                alias.setdefault(ch.old_path, ch.path)
    return alias


def canonical_path(path: str, alias: dict[str, str], *, max_hops: int = 100) -> str:
    """Follow a rename chain a->b->c to its current name. Hop-capped and cycle-guarded."""
    seen = {path}
    cur = path
    for _ in range(max_hops):
        nxt = alias.get(cur)
        if nxt is None or nxt in seen:
            return cur
        seen.add(nxt)
        cur = nxt
    return cur


# ---------------------------------------------------------------------------
# Frame 1 — hotspots
# ---------------------------------------------------------------------------

def indent_profile(text: str, *, tab_width: int = 4, indent_unit: int = 4) -> IndentProfile:
    """Indentation-based complexity over file text (the CodeScene model, D2-modified).

    Blank / whitespace-only lines are skipped. Tabs expand to `tab_width` spaces. No comment
    stripping (see honest limit 8). `weighted_lines` is the D2 deviation and the quantity the
    hotspot score actually uses; `total_indent` is the pure CodeScene quantity, reported for
    comparison.
    """
    n_lines = 0
    total = 0
    mx = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        expanded = line.replace("\t", " " * tab_width)
        indent = (len(expanded) - len(expanded.lstrip(" "))) // indent_unit
        n_lines += 1
        total += indent
        mx = max(mx, indent)
    mean = (total / n_lines) if n_lines else 0.0
    return IndentProfile(n_lines=n_lines, total_indent=total, max_indent=mx,
                         mean_indent=round(mean, 3), weighted_lines=n_lines + total)


def revision_counts(commits: list[CommitRec], alias: dict[str, str], existing: set[str],
                    *, since_ts: Optional[int], cfg: Config) -> Counter:
    """path -> in-window revision count, over CANONICAL paths that still exist at HEAD.

    Alias resolution runs BEFORE the existence intersection: otherwise a renamed file loses
    its pre-rename revisions and reads as brand new.
    """
    revs: Counter = Counter()
    for c in commits:
        if since_ts is not None and c.ts < since_ts:
            continue
        touched = set()
        for ch in c.changes:
            p = canonical_path(ch.path, alias)
            if p in existing and not excluded(p, cfg.exclude):
                touched.add(p)
        for p in touched:
            revs[p] += 1
    return revs


def hotspot_frame(revs: Counter, profiles: dict[str, IndentProfile], *, cfg: Config):
    """Build the ranked hotspot frame: revisions x complexity, both percentile-normalized.

    Percentile rank (not min-max, not raw) because the two axes are incommensurable and both
    heavy-tailed — a raw product is dominated by whichever axis has the larger dynamic range.
    Percentile is scale-free and outlier-robust, which the fleet roll-up requires. It also
    cancels a repo's indent-width convention entirely, WHICH IS WHY RANKING MUST STAY
    WITHIN-REPO — do not "optimize" this to a fleet-wide rank.

    Percentile compresses (a file with 10x the revisions gains only a sliver of rank), so raw
    `revisions` and `weighted_lines` are always emitted beside the score for interpretation.
    """
    import pandas as pd

    rows = []
    for path, n in revs.items():
        prof = profiles.get(path)
        if prof is None or prof.weighted_lines == 0:
            continue  # binary / unreadable / empty -> no complexity axis, cannot be a hotspot
        if n < cfg.min_revisions:
            continue
        rows.append({"file": path, "revisions": n, "weighted_lines": prof.weighted_lines,
                     "max_indent": prof.max_indent, "total_indent": prof.total_indent})
    if not rows:
        return pd.DataFrame(columns=["file", "revisions", "weighted_lines", "max_indent",
                                     "total_indent", "rev_pct", "cx_pct", "score"])
    df = pd.DataFrame(rows)
    df["rev_pct"] = df["revisions"].rank(pct=True, method="average")
    df["cx_pct"] = df["weighted_lines"].rank(pct=True, method="average")
    df["score"] = (df["rev_pct"] * df["cx_pct"]).round(4)
    return df.sort_values(["score", "revisions"], ascending=False).reset_index(drop=True)


def concentration(values: list[int]) -> tuple[float, float]:
    """(top_decile_share, gini) over a revision distribution — substantiates "power law".

    Deliberately NOT a fitted Pareto alpha: an MLE alpha needs an arbitrary x_min tail cutoff
    and scipy, and the number would look authoritative while meaning little at n~1400.
    Concentration share and Gini are assumption-free and answer the actual question.
    """
    if not values:
        return 0.0, 0.0
    xs = sorted(values)
    n = len(xs)
    total = sum(xs)
    if total == 0:
        return 0.0, 0.0
    k = max(1, n // 10)
    top_share = sum(xs[-k:]) / total
    gini = sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(xs)) / (n * total)
    return round(top_share, 4), round(gini, 4)


# ---------------------------------------------------------------------------
# Frame 2 — change coupling
# ---------------------------------------------------------------------------

def commit_file_sets(commits: list[CommitRec], alias: dict[str, str], existing: set[str],
                     *, since_ts: Optional[int], cfg: Config
                     ) -> tuple[list[frozenset], int]:
    """(per-commit file sets, commits_skipped_wide).

    A commit touching more than `max_commit_files` is SKIPPED ENTIRELY, never truncated.
    Pairs grow quadratically — a 200-file mega-commit yields ~19,900 pairs, essentially all
    mechanical (mass rename, lint sweep, generated-doc regen) — and truncating to the first N
    would pick an arbitrary, alphabetically-biased subset: a silent, invisible distortion.
    Skipping is loud and countable. Measured breadth on this fleet (p95/p99/max):
    hub 6/11/66, corp-monorepo 15/59/444, ai-council 6/13/61 — so a cap of 30 admits ~99% of
    hub and ~97% of corp-monorepo commits while excluding the mass sweeps.
    """
    sets: list[frozenset] = []
    skipped = 0
    for c in commits:
        if since_ts is not None and c.ts < since_ts:
            continue
        touched = {canonical_path(ch.path, alias) for ch in c.changes}
        touched = {p for p in touched if p in existing and not excluded(p, cfg.exclude)}
        if len(touched) < 2:
            continue
        if len(touched) > cfg.max_commit_files:
            skipped += 1
            continue
        sets.append(frozenset(touched))
    return sets, skipped


def coupling_counts(file_sets: list[frozenset]) -> Counter:
    """(a, b) -> co-change count, `a < b`. A plain Counter — never a n x n matrix."""
    counts: Counter = Counter()
    for fs in file_sets:
        for a, b in combinations(sorted(fs), 2):
            counts[(a, b)] += 1
    return counts


def coupling_frame(counts: Counter, revs: Counter, *, cfg: Config):
    """Ranked coupling frame. Rank on CodeScene's degree, GATE on Jaccard.

    `degree_min = co / min(revs_a, revs_b)` is CodeScene's published form and is kept as the
    headline so numbers stay comparable to the literature. But it has a named failure mode:
    if A has 3 revisions, B has 300, and they co-changed 3 times, degree reads 100% —
    "inseparable" — when A is really a rarely-touched file that always rides along with a hot
    one. That IS the generated-file / config-file false positive.

    So admission additionally requires `jaccard = co / (revs_a + revs_b - co) >= min_jaccard`,
    which is symmetric and kills the lopsided case. Rank on one, gate on the other.
    """
    import pandas as pd

    cols = ["file_a", "file_b", "co_changes", "revs_a", "revs_b", "degree", "jaccard",
            "same_dir", "mechanical"]
    rows = []
    considered = 0
    for (a, b), co in counts.items():
        considered += 1
        ra, rb = revs.get(a, 0), revs.get(b, 0)
        if co < cfg.min_co or ra < cfg.min_revisions or rb < cfg.min_revisions:
            continue
        degree = co / min(ra, rb)
        union = ra + rb - co
        jaccard = (co / union) if union > 0 else 0.0
        if degree < cfg.min_degree or jaccard < cfg.min_jaccard:
            continue
        rows.append({
            "file_a": a, "file_b": b, "co_changes": co, "revs_a": ra, "revs_b": rb,
            "degree": round(degree, 4), "jaccard": round(jaccard, 4),
            # same_dir is a COLUMN, not a filter: a test_x.py <-> x.py pair is the healthiest
            # evidence the test convention is being followed, and its ABSENCE is the
            # interesting signal. Surface it; let the reader discount it.
            "same_dir": _parent(a) == _parent(b),
            # Fully mechanical lockstep -- kept but sorted below genuine coupling.
            "mechanical": (co == ra == rb),
        })
    if not rows:
        return pd.DataFrame(columns=cols), considered
    df = pd.DataFrame(rows)
    df = df.sort_values(["mechanical", "degree", "co_changes"], ascending=[True, False, False])
    return df.reset_index(drop=True), considered


def _parent(path: str) -> str:
    return path.rsplit("/", 1)[0] if "/" in path else ""


# ---------------------------------------------------------------------------
# Frame 3 — rot
# ---------------------------------------------------------------------------

def match_tokens(existing: set[str], *, stoplist: frozenset = _BASENAME_STOPLIST
                 ) -> dict[str, str]:
    """token -> canonical path. Full path always; a shorter suffix only if REPO-UNIQUE.

    Measured: 71 hub basenames are non-unique (PROBES.md x56, HANDOFF_BOOT.md x54,
    RESIDUAL.md x53, README.md x28), so bare-basename matching is not viable. Ambiguous names
    walk up path components until the shortest unique suffix is found; if no proper suffix is
    unique, only the full path counts. Stoplisted basenames contribute their full path only,
    even when unique — belt-and-braces for names mentioned generically in prose.
    """
    suffix_owners: dict[str, set[str]] = {}
    for path in existing:
        parts = path.split("/")
        for k in range(1, len(parts) + 1):
            suffix_owners.setdefault("/".join(parts[-k:]), set()).add(path)

    tokens: dict[str, str] = {}
    for path in existing:
        tokens[path] = path
        parts = path.split("/")
        start = 2 if parts[-1] in stoplist else 1
        for k in range(start, len(parts)):
            suf = "/".join(parts[-k:])
            if len(suffix_owners.get(suf, ())) == 1:
                tokens[suf] = path
                break
    return tokens


def extract_path_tokens(text: str) -> set[str]:
    """Distinct normalized path-shaped tokens in `text`. One regex pass, no per-file loop."""
    out = set()
    for m in _TOKEN_RE.finditer(text):
        t = m.group(0).replace("\\", "/")
        while t.startswith("./"):
            t = t[2:]
        if t:
            out.add(t)
    return out


def inbound_reference_counts(texts: dict[str, str], tokens: dict[str, str], *, cfg: Config
                             ) -> tuple[Counter, Counter, set[str]]:
    """(inbound_all, inbound_excl_indexes, index_referrers).

    O(total bytes), not O(n^2): each file is scanned ONCE for path-shaped tokens, then each
    token is an O(1) dict lookup against the prebuilt map. The naive nested-loop form would
    be 1432^2 substring scans over 24 MB.

    Counts DISTINCT REFERRERS, not mentions — one doc naming a path 40 times is one referrer.

    Index-file contamination (REGISTRY.md, generated rosters, TOCs list every file and would
    give everything a uniform +1) is handled by a STRUCTURAL rule, not a hand-list: any
    referrer naming more than `index_referrer_cut` distinct targets is an index referrer and
    is excluded from the ranked count. Self-maintaining; there is no allowlist to rot.
    """
    referrer_targets: dict[str, set[str]] = {}
    for src, text in texts.items():
        hits = set()
        for tok in extract_path_tokens(text):
            tgt = tokens.get(tok)
            if tgt is not None and tgt != src:
                hits.add(tgt)
        if hits:
            referrer_targets[src] = hits

    index_referrers = {s for s, tg in referrer_targets.items()
                       if len(tg) > cfg.index_referrer_cut}

    all_counts: Counter = Counter()
    excl_counts: Counter = Counter()
    for src, tg in referrer_targets.items():
        for tgt in tg:
            all_counts[tgt] += 1
            if src not in index_referrers:
                excl_counts[tgt] += 1
    return all_counts, excl_counts, index_referrers


def last_meaningful_ts(commits: list[CommitRec], alias: dict[str, str], existing: set[str],
                       *, cfg: Config) -> dict[str, int]:
    """path -> committer ts of its most recent MEANINGFUL edit (full history, no window).

    Meaningful = a non-merge commit (already excluded at the mine) that changed at least
    `min_meaningful_churn` lines of this file AND touched at most `max_commit_files` files
    overall. The churn floor also drops 0/0 records (mode-only changes, pure renames); the
    breadth cap encodes that a 200-file lint sweep or header normalization is not a
    meaningful edit to any single file.

    Full history on purpose: a file whose last meaningful edit predates the 365-day hotspot
    window has no in-window record at all, and rot is inherently about the long tail.
    """
    out: dict[str, int] = {}
    for c in commits:
        if len(c.changes) > cfg.max_commit_files:
            continue
        for ch in c.changes:
            if ch.binary or (ch.added + ch.deleted) < cfg.min_meaningful_churn:
                continue
            p = canonical_path(ch.path, alias)
            if p in existing and c.ts > out.get(p, 0):
                out[p] = c.ts
    return out


def rot_frame(last_ts: dict[str, int], refs_excl: Counter, refs_all: Counter,
              existing: set[str], *, now_ts: int, history_days: int, cfg: Config):
    """Ranked rot frame + the orphan count.

    The asymmetry that defines the frame: an UNREFERENCED stale file is dead weight or an
    intentional archive — harmless. A stale file that many files POINT AT is a live
    liability, because readers follow the pointer and get outdated information. So zero
    referrers is NOT rot; it is reported separately as `orphan_files`.

    Age is ranked within-repo on raw days, but `age_pct` (age / repo_history_days) is carried
    so a 1-year repo and a 10-year repo compare honestly in the fleet roll-up — repo age
    otherwise caps the metric.
    """
    import pandas as pd

    cols = ["file", "age_days", "age_pct", "inbound", "inbound_all", "age_rank",
            "ref_rank", "score"]
    rows = []
    orphans = 0
    for path in sorted(existing):
        if excluded(path, cfg.exclude):
            continue
        ts = last_ts.get(path)
        if ts is None:
            continue
        age_days = max(0, (now_ts - ts) // 86400)
        n_refs = refs_excl.get(path, 0)
        if n_refs == 0:
            if age_days >= cfg.min_age_days:
                orphans += 1
            continue
        if n_refs < cfg.min_refs or age_days < cfg.min_age_days:
            continue
        rows.append({"file": path, "age_days": int(age_days),
                     "age_pct": round(age_days / history_days, 4) if history_days else 0.0,
                     "inbound": n_refs, "inbound_all": refs_all.get(path, 0)})
    if not rows:
        return pd.DataFrame(columns=cols), orphans
    df = pd.DataFrame(rows)
    df["age_rank"] = df["age_days"].rank(pct=True, method="average")
    df["ref_rank"] = df["inbound"].rank(pct=True, method="average")
    df["score"] = (df["age_rank"] * df["ref_rank"]).round(4)
    return df.sort_values(["score", "inbound"], ascending=False).reset_index(drop=True), orphans


# ---------------------------------------------------------------------------
# Digest rendering
# ---------------------------------------------------------------------------

@dataclass
class RepoAnalytics:
    name: str
    status: str                      # pass | warn | unavailable
    note: str = ""
    commits: int = 0
    files: int = 0
    history_days: int = 0
    hotspots: object = None
    coupling: object = None
    rot: object = None
    diagnostics: dict = field(default_factory=dict)


def to_finding(r: RepoAnalytics) -> Finding:
    if r.status == "unavailable":
        return Finding(_CHECK, "unavailable", _safe(f"{r.name}: {r.note or 'unresolvable'}"))
    d = r.diagnostics
    return Finding(_CHECK, r.status, _safe(
        f"{r.name}: {r.commits} commits, {r.files} files; "
        f"{d.get('hotspots', 0)} hotspots, {d.get('couplings', 0)} coupled pairs, "
        f"{d.get('rot', 0)} rot candidates, {d.get('orphans', 0)} orphans"))


def _table(df, columns: list[str], limit: int, repo_col: Optional[str] = None) -> list[str]:
    """Render a DataFrame slice as a plain markdown table (ASCII, no padding)."""
    header = ([repo_col] if repo_col else []) + columns
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    if df is None or len(df) == 0:
        out.append("| " + " | ".join(["_none_"] + [""] * (len(header) - 1)) + " |")
        return out
    for _, row in df.head(limit).iterrows():
        cells = []
        if repo_col:
            cells.append(str(row.get("_repo", "")))
        for c in columns:
            v = row.get(c, "")
            cells.append(_safe(str(v)))
        out.append("| " + " | ".join(cells) + " |")
    return out


def build_digest(repos: list[RepoAnalytics], run_date: str, cfg: Config,
                 totals: dict) -> str:
    """The full markdown digest. ASCII-only; fleet-wide sections BEFORE per-repo detail."""
    import pandas as pd

    live = [r for r in repos if r.status != "unavailable"]

    def _fleet(attr: str):
        frames = []
        for r in live:
            df = getattr(r, attr)
            if df is not None and len(df):
                d = df.copy()
                d["_repo"] = r.name
                frames.append(d)
        return pd.concat(frames, ignore_index=True) if frames else None

    fh, fc, fr = _fleet("hotspots"), _fleet("coupling"), _fleet("rot")
    if fh is not None:
        fh = fh.sort_values("score", ascending=False)
    if fc is not None:
        fc = fc.sort_values(["mechanical", "degree"], ascending=[True, False])
    if fr is not None:
        fr = fr.sort_values("score", ascending=False)

    top_h = fh.iloc[0] if fh is not None and len(fh) else None

    L: list[str] = []
    L.append("---")
    L.append(f"run_date: {run_date}")
    L.append("generated_by: scripts/fleet_analytics.py")
    L.append(f"schema_version: {_SCHEMA_VERSION}")
    L.append(f"window_days: {cfg.window_days}")
    L.append(f"window_since: {totals.get('window_since', '?')}")
    L.append("rot_window: all-history")
    L.append(f"repos_total: {len(repos)}")
    L.append(f"repos_mined: {len(live)}")
    L.append(f"repos_unavailable: {len(repos) - len(live)}")
    L.append(f"commits_scanned: {totals.get('commits', 0)}")
    L.append(f"commits_skipped_wide: {totals.get('skipped_wide', 0)}")
    L.append(f"max_commit_files: {cfg.max_commit_files}")
    L.append(f"files_scanned: {totals.get('files', 0)}")
    L.append(f"parse_anomalies: {totals.get('anomalies', 0)}")
    L.append(f"hotspots_total: {0 if fh is None else len(fh)}")
    L.append(f"coupling_pairs_admitted: {0 if fc is None else len(fc)}")
    L.append(f"rot_candidates: {0 if fr is None else len(fr)}")
    L.append(f"orphan_files: {totals.get('orphans', 0)}")
    if top_h is not None:
        L.append(f"top_hotspot: {top_h['file']}")
        L.append(f"top_hotspot_repo: {top_h['_repo']}")
        L.append(f"top_hotspot_score: {top_h['score']}")
    L.append("---")
    L.append("")
    L.append(f"# Fleet analytics -- {run_date}")
    L.append("")
    L.append("L5a descriptive frames mined from git history ([#384], intake #16 section 3). "
             "This is a **reporter, not a gate** -- it never blocks a commit or a ship.")
    L.append("")
    L.append("The rot frame's \"dependency\" is a **textual** inbound reference, not a "
             "semantic one. Every frame here is a **review queue, not a verdict**.")
    L.append("")

    L.append("## Method and honest limits")
    L.append("")
    L.append("**Mined** with `git log --no-merges --numstat -z -M` per repo (read-only; the "
             "hub plus every registered sibling). **Hotspots** rank revisions x complexity, "
             "both percentile-normalized within-repo. **Complexity is indentation-based** "
             "(the CodeScene model -- language-agnostic, so it works on markdown), computed "
             "as `sum(1 + indent_units)` over non-blank lines at current HEAD.")
    L.append("")
    L.append("Limits, stated so no number here is over-read:")
    L.append("")
    L.append("1. A \"reference\" is a path-shaped string. A mention in a changelog, inside a "
             "code fence, or in a \"do not use X\" warning counts identically to a live "
             "dependency.")
    L.append("2. Reference counts are a **lower bound**: `import` statements, package paths, "
             "and references by concept are invisible. Deliberate precision-over-recall.")
    L.append("3. Ambiguous basenames resolve to their shortest unique path suffix; where no "
             "suffix is unique, only the full path counts -- those files are undercounted.")
    L.append("4. **Staleness is not rot.** A stable, correct, finished file looks identical "
             "to an abandoned one by git dates alone.")
    L.append("5. Whitespace-only edits are filtered by a churn floor, but trivial-but-textual "
             "ones (typos, date stamps) still read as meaningful.")
    L.append("6. **Cross-repo references are invisible** -- a hub protocol cited by corp-ops "
             "docs shows 0 inbound in the hub's own scan.")
    L.append("7. Complexity is measured on current HEAD, not historically.")
    L.append("")
    L.append("Thresholds this run: "
             f"`window_days={cfg.window_days}` (rot uses all history), "
             f"`min_revisions={cfg.min_revisions}`, `max_commit_files={cfg.max_commit_files}`, "
             f"`min_co={cfg.min_co}`, `min_degree={cfg.min_degree}`, "
             f"`min_jaccard={cfg.min_jaccard}`, `min_refs={cfg.min_refs}`, "
             f"`min_age_days={cfg.min_age_days}`, "
             f"`index_referrer_cut={cfg.index_referrer_cut}`.")
    L.append("")

    L.append("## Fleet roll-up")
    L.append("")
    L.append("| Repo | Status | Commits | Files | Hotspots | Coupled pairs | Rot | Orphans |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in repos:
        if r.status == "unavailable":
            L.append(f"| {r.name} | unavailable | - | - | - | - | - | - |")
            continue
        d = r.diagnostics
        L.append(f"| {r.name} | {r.status} | {r.commits} | {r.files} | "
                 f"{d.get('hotspots', 0)} | {d.get('couplings', 0)} | "
                 f"{d.get('rot', 0)} | {d.get('orphans', 0)} |")
    L.append("")

    L.append(f"## Hotspots (fleet top {cfg.fleet_top})")
    L.append("")
    L.append("Change frequency x complexity. `score` is the product of within-repo percentile "
             "ranks; `revisions` and `weighted_lines` are the raw values behind it.")
    L.append("")
    L.extend(_table(fh, ["file", "revisions", "weighted_lines", "max_indent", "score"],
                    cfg.fleet_top, repo_col="Repo"))
    L.append("")

    L.append(f"## Change coupling (fleet top {cfg.fleet_top})")
    L.append("")
    L.append("Files that change together -- temporal dependencies static analysis cannot see. "
             "`degree = co / min(revs)` (CodeScene's form, ranked on); `jaccard` is the "
             "symmetric gate that kills lopsided pairs. `mechanical` rows sort last.")
    L.append("")
    L.extend(_table(fc, ["file_a", "file_b", "co_changes", "revs_a", "revs_b", "degree",
                         "jaccard", "same_dir"], cfg.fleet_top, repo_col="Repo"))
    L.append("")

    L.append(f"## Rot candidates (fleet top {cfg.fleet_top})")
    L.append("")
    L.append("Stale files that other files still point at. Zero-referrer stale files are "
             "**orphans**, counted separately -- they are not rot.")
    L.append("")
    L.extend(_table(fr, ["file", "age_days", "age_pct", "inbound", "score"],
                    cfg.fleet_top, repo_col="Repo"))
    L.append("")

    L.append("## Per-repo detail")
    L.append("")
    for r in repos:
        L.append(f"### {r.name}")
        L.append("")
        if r.status == "unavailable":
            L.append(f"_unavailable: {_safe(r.note)}_")
            L.append("")
            continue
        d = r.diagnostics
        L.append(f"{r.commits} non-merge commits, {r.files} tracked files, "
                 f"{r.history_days} days of history.")
        L.append("")
        L.append(f"**Hotspots (top {cfg.top_n})**")
        L.append("")
        L.extend(_table(r.hotspots, ["file", "revisions", "weighted_lines", "score"], cfg.top_n))
        L.append("")
        L.append("**Change coupling (top 10)**")
        L.append("")
        L.extend(_table(r.coupling, ["file_a", "file_b", "co_changes", "degree", "jaccard"], 10))
        L.append("")
        L.append("**Rot candidates (top 10)**")
        L.append("")
        L.extend(_table(r.rot, ["file", "age_days", "inbound", "score"], 10))
        L.append("")
        L.append(f"_Concentration: top-decile revision share {d.get('top_decile', 0)}, "
                 f"Gini {d.get('gini', 0)}. Pairs considered {d.get('pairs_considered', 0)} "
                 f"-> admitted {d.get('couplings', 0)}. "
                 f"Wide commits skipped: {d.get('skipped_wide', 0)}. "
                 f"Index referrers excluded: {d.get('index_referrers', 0)}._")
        L.append("")

    L.append("## Distribution diagnostics")
    L.append("")
    L.append("| Repo | Top-decile rev share | Gini | Pairs considered | Pairs admitted | "
             "Wide commits skipped | Index referrers | Files unread | No edit record | "
             "Oldest edit (d) |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in live:
        d = r.diagnostics
        L.append(f"| {r.name} | {d.get('top_decile', 0)} | {d.get('gini', 0)} | "
                 f"{d.get('pairs_considered', 0)} | {d.get('couplings', 0)} | "
                 f"{d.get('skipped_wide', 0)} | {d.get('index_referrers', 0)} | "
                 f"{d.get('files_unread', 0)} | {d.get('files_no_edit_record', 0)} | "
                 f"{d.get('oldest_edit_days', 0)} |")
    L.append("")
    L.append("A Gini near 1.0 and a high top-decile share are what \"activity follows a power "
             "law\" actually means for that repo. No Pareto alpha is fitted -- see the source "
             "docstring for why.")
    L.append("")
    L.append("**Reading the rot column honestly:** *Oldest edit* caps what the rot frame can "
             f"possibly see. Where it is below `min_age_days={cfg.min_age_days}`, zero rot "
             "candidates means **the repo is too young to have rotted**, not that it was "
             "audited clean. *No edit record* counts files the rot frame cannot see at all -- "
             "only ever touched inside a wide commit, or never with more than "
             f"`min_meaningful_churn={cfg.min_meaningful_churn}` lines.")
    L.append("")

    L.append("## Anomalies")
    L.append("")
    anomalies = totals.get("anomaly_samples", [])
    if not anomalies:
        L.append("_None -- the `-z` numstat format assumption held for every repo._")
    else:
        for a in anomalies[:20]:
            L.append(f"- {_safe(a)}")
    L.append("")
    return "\n".join(L) + "\n"


def surface_line(analytics_file: Path = _ANALYTICS_FILE) -> str:
    """One-line ASCII summary read from the digest frontmatter. NEVER mines, never imports
    pandas -- this is the cheap path a SessionStart hook could call."""
    if not analytics_file.exists():
        return "[analytics] no report yet -- run scripts/fleet_analytics.py"
    fm: dict[str, str] = {}
    try:
        text = analytics_file.read_text(encoding="utf-8")
        in_fm = False
        for line in text.splitlines():
            if line.strip() == "---":
                if in_fm:
                    break
                in_fm = True
                continue
            if in_fm:
                m = _FM_RE.match(line)
                if m:
                    fm[m.group(1)] = m.group(2)
    except OSError:
        return "[analytics] report unreadable"
    return (f"[analytics] {fm.get('repos_mined', '?')} repos, "
            f"{fm.get('commits_scanned', '?')} commits ({fm.get('window_days', '?')}d): "
            f"top hotspot {fm.get('top_hotspot', '?')} "
            f"(score {fm.get('top_hotspot_score', '?')}); "
            f"{fm.get('coupling_pairs_admitted', '?')} coupled pairs; "
            f"{fm.get('rot_candidates', '?')} rot candidates "
            f"as of {fm.get('run_date', '?')}")


# ============================================================================
# Impure: git subprocesses, filesystem traversal, digest write
# ============================================================================

_SCRUB_CACHE: Optional[frozenset] = None


def _scrubbed_git_env() -> dict:
    """os.environ minus git's repo-LOCAL vars, so `cwd=`/`-C` actually selects the repo.

    An inherited GIT_DIR overrides BOTH `cwd=` and `git -C` — a validator then reads the
    hook's repo while labelling the result with the target's id. That bit this fleet live
    ([#355]). The name set is DERIVED from `git rev-parse --local-env-vars` (git's own
    canonical list) — never hand-written: the first hand-list here omitted 8 of git's 15.
    Scrubbed BY NAME, never `startswith("GIT_")` — a blanket strip would also drop
    GIT_CONFIG_GLOBAL / GIT_AUTHOR_* / GIT_SSH_COMMAND, which fails quietly.

    Reuses audit._git_location_env() rather than deriving a THIRD copy (audit.py:1542 and
    fleet_parity.py:504 already carry one each). Extracting a shared scripts/gitenv.py is
    filed as a follow-up.
    """
    global _SCRUB_CACHE
    if _SCRUB_CACHE is None:
        _SCRUB_CACHE = audit._git_location_env()
    return {k: v for k, v in os.environ.items() if k not in _SCRUB_CACHE}


def _git(args: list[str], cwd: Path, *, timeout: int = 180) -> tuple[int, bytes]:
    """Run git in `cwd` with a scrubbed env, returning (returncode, raw stdout BYTES).

    Bytes, not text: `text=True` inherits the cp1252 default on Windows and corrupts
    non-ASCII paths. Decoding happens at the parse boundary with errors="replace".
    """
    try:
        p = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                           env=_scrubbed_git_env(), timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return 1, b""
    return p.returncode, p.stdout


def mine_repo_log(root: Path) -> tuple[bytes, Optional[str]]:
    """Full-history non-merge numstat for one repo -> (raw bytes, error or None).

    ONE mine serves both windows: the hotspot/coupling frames filter to the 365-day window
    in memory, while rot needs full history. A second subprocess would buy nothing.

    NEVER add `--first-parent` here: combined with `--no-merges` it collapses each feature
    branch to its merge commit and then drops it, yielding a near-empty frame. Under this
    fleet's universal `--no-ff` policy every real commit is still reachable without it.
    """
    rc, _ = _git(["rev-parse", "--verify", "HEAD"], root)
    if rc != 0:
        return b"", "no HEAD (unborn or not a git repo)"
    rc, out = _git(["-c", "core.quotepath=false", "log", "--no-merges", "--numstat", "-z",
                    "-M", "--format=%x01%H%x02%ct%x02%at%x02%s"], root)
    if rc != 0:
        return b"", "git log failed"
    return out, None


def list_tracked(root: Path) -> set[str]:
    """Repo-relative posix paths tracked at HEAD."""
    rc, out = _git(["ls-files", "-z"], root)
    if rc != 0:
        return set()
    return {p.decode("utf-8", "replace").replace("\\", "/")
            for p in out.split(b"\0") if p}


def read_texts(root: Path, paths: set[str], *, cfg: Config) -> tuple[dict[str, str], int]:
    """Read every tracked text file once -> ({path: text}, n_unread).

    One read serves BOTH the complexity profile and the inbound-reference scan. Binary files
    (NUL in the first 8 KB) and oversize files are skipped and counted.
    """
    texts: dict[str, str] = {}
    unread = 0
    for rel in paths:
        fp = root / rel
        try:
            if not fp.is_file() or fp.stat().st_size > cfg.max_file_bytes:
                unread += 1
                continue
            raw = fp.read_bytes()
        except OSError:
            unread += 1
            continue
        if b"\0" in raw[:8192]:
            unread += 1
            continue
        texts[rel] = raw.decode("utf-8", "replace")
    return texts, unread


def _git_common_dir(path: Path) -> Optional[Path]:
    """The repo's shared git dir (worktrees of one repo share it). Fail-soft: None on error."""
    rc, out = _git(["rev-parse", "--git-common-dir"], path, timeout=10)
    if rc != 0:
        return None
    g = Path(out.decode("utf-8", "replace").strip())
    try:
        return (g if g.is_absolute() else (path / g)).resolve()
    except OSError:
        return None


def _is_hub(root: Path, repo_root: Path) -> bool:
    """Same logical repo as the hub (resolved path OR shared git-common-dir, so a worktree
    run still recognizes itself)."""
    try:
        if root.resolve() == repo_root.resolve():
            return True
    except OSError:
        pass
    a, b = _git_common_dir(root), _git_common_dir(repo_root)
    return a is not None and a == b


def _resolve_root(name: str) -> Optional[Path]:
    """On-disk root for a registered repo: its state.yaml `path:`, fallback
    `<repo_root.parent>/<name>` (mirrors audit/fleet_health). None if unresolvable."""
    st = audit.load_state(name)
    if st is not None and getattr(st, "path", None):
        p = Path(st.path)
        if p.exists():
            return p
    cand = _REPO_ROOT.parent / name
    return cand if cand.exists() else None


def _hub_name(repo_root: Path) -> str:
    """The hub's CANONICAL repo name, correct even when running from a linked worktree.

    `repo_root.name` would report the worktree directory ("l5a-analytics") and the digest
    would name a repo that does not exist in the fleet. The git common dir always points at
    the primary checkout's `.git`, so its parent is the real repo name. Fail-soft to the
    directory name if git is unavailable.
    """
    common = _git_common_dir(repo_root)
    if common is not None and common.name == ".git" and common.parent.name:
        return common.parent.name
    return repo_root.name


def enumerate_fleet(repo_root: Path = _REPO_ROOT) -> list[tuple[str, Optional[Path]]]:
    """(name, root) for every mining target, HUB FIRST.

    The hub is NOT registered in ecosystem/ (which holds only the 5 consumers), and unlike
    boundary_report — where the hub is the diff baseline and is deliberately skipped — the
    hub is a first-class mining target here. So it is prepended explicitly, and consumers
    that resolve to the same logical repo are deduped via _is_hub.
    """
    out: list[tuple[str, Optional[Path]]] = [(_hub_name(repo_root), repo_root)]
    for name in audit.discover_repos():
        root = _resolve_root(name)
        if root is not None and _is_hub(root, repo_root):
            continue
        out.append((name, root))
    return out


def analyze_repo(name: str, root: Optional[Path], cfg: Config, now_ts: int) -> RepoAnalytics:
    """Mine and frame one repo. Fail-soft: any failure -> status 'unavailable', never raises."""
    if root is None:
        return RepoAnalytics(name, "unavailable", note="path unresolvable")
    try:
        raw, err = mine_repo_log(root)
        if err:
            return RepoAnalytics(name, "unavailable", note=err)
        commits, anomalies = parse_numstat_stream(raw)
        existing = list_tracked(root)
        if not commits or not existing:
            return RepoAnalytics(name, "unavailable", note="no commits or no tracked files")

        alias = build_rename_alias(commits)
        since_ts = now_ts - cfg.window_days * 86400
        oldest = min(c.ts for c in commits)
        history_days = max(1, (now_ts - oldest) // 86400)

        texts, unread = read_texts(root, existing, cfg=cfg)
        profiles = {p: indent_profile(t, tab_width=cfg.tab_width, indent_unit=cfg.indent_unit)
                    for p, t in texts.items()}

        revs = revision_counts(commits, alias, existing, since_ts=since_ts, cfg=cfg)
        hs = hotspot_frame(revs, profiles, cfg=cfg)
        top_decile, gini = concentration(list(revs.values()))

        sets, skipped = commit_file_sets(commits, alias, existing, since_ts=since_ts, cfg=cfg)
        counts = coupling_counts(sets)
        cp, considered = coupling_frame(counts, revs, cfg=cfg)

        tokens = match_tokens(existing)
        refs_all, refs_excl, index_refs = inbound_reference_counts(texts, tokens, cfg=cfg)
        lts = last_meaningful_ts(commits, alias, existing, cfg=cfg)
        rt, orphans = rot_frame(lts, refs_excl, refs_all, existing,
                                now_ts=now_ts, history_days=history_days, cfg=cfg)

        return RepoAnalytics(
            name=name, status="pass", commits=len(commits), files=len(existing),
            history_days=history_days, hotspots=hs, coupling=cp, rot=rt,
            diagnostics={
                "hotspots": len(hs), "couplings": len(cp), "rot": len(rt),
                "orphans": orphans, "pairs_considered": considered,
                "skipped_wide": skipped, "top_decile": top_decile, "gini": gini,
                "index_referrers": len(index_refs), "files_unread": unread,
                # Rot's blind spot, made countable: files with no meaningful-edit record are
                # dropped from the rot frame silently unless we surface the count (limit 9).
                "files_no_edit_record": len(existing) - len(lts),
                "oldest_edit_days": max((now_ts - t) // 86400 for t in lts.values()) if lts else 0,
                "anomalies": anomalies,
            })
    except Exception as exc:  # fail-soft per repo -- one bad repo never kills the run
        return RepoAnalytics(name, "unavailable", note=f"{type(exc).__name__}: {exc}")


def run_report(repo_root: Path = _REPO_ROOT, *, today: Optional[str] = None,
               cfg: Optional[Config] = None) -> tuple[list[Finding], str]:
    """Mine the fleet and build the digest. Read-only; returns (findings, digest_text)."""
    cfg = cfg or Config()
    run_date = today or date.today().isoformat()
    now_ts = int(datetime.now(timezone.utc).timestamp())

    repos = [analyze_repo(n, r, cfg, now_ts) for n, r in enumerate_fleet(repo_root)]

    totals = {
        "commits": sum(r.commits for r in repos),
        "files": sum(r.files for r in repos),
        "skipped_wide": sum(r.diagnostics.get("skipped_wide", 0) for r in repos),
        "orphans": sum(r.diagnostics.get("orphans", 0) for r in repos),
        "anomalies": sum(len(r.diagnostics.get("anomalies", [])) for r in repos),
        "anomaly_samples": [f"{r.name}: {a}" for r in repos
                            for a in r.diagnostics.get("anomalies", [])],
        "window_since": date.fromtimestamp(now_ts - cfg.window_days * 86400).isoformat(),
    }
    return [to_finding(r) for r in repos], build_digest(repos, run_date, cfg, totals)


def _atomic_write(path: Path, text: str) -> None:
    """Process-unique temp + os.replace, so a concurrent reader never sees a half write
    (mirrors fleet_health._atomic_write). The digest is gitignored."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".analytics-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entry -- write the digest, print the surface line. ALWAYS returns 0 (a reporter
    never breaks its caller)."""
    ap = argparse.ArgumentParser(
        prog="fleet_analytics",
        description="L5a descriptive fleet analytics: hotspots, change coupling, rot ([#384])")
    ap.add_argument("--window-days", type=int, default=Config.window_days,
                    help="hotspot/coupling window in days (rot always uses full history)")
    ap.add_argument("--max-commit-files", type=int, default=Config.max_commit_files,
                    help="commits touching more files than this are skipped entirely")
    ap.add_argument("--top", type=int, default=Config.top_n, help="per-repo rows per frame")
    ap.add_argument("--surface", action="store_true",
                    help="print the cached surface line only; do not mine")
    args = ap.parse_args(argv)

    if args.surface:
        print(surface_line(_ANALYTICS_FILE))
        return 0

    try:
        cfg = Config(window_days=args.window_days, max_commit_files=args.max_commit_files,
                     top_n=args.top)
        _findings, digest = run_report(cfg=cfg)
        _atomic_write(_ANALYTICS_FILE, digest)
        print(surface_line(_ANALYTICS_FILE))
    except Exception as exc:  # fail-soft: a reporter never breaks the caller
        print(f"[analytics] reporter error (fail-soft): {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
