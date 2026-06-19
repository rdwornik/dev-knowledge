#!/usr/bin/env python
"""Read-only narrow schema validator for BACKLOG.md (ADR-66 story-map hierarchy).

Layer-2 invariant: reads BACKLOG.md only; never writes, never orchestrates.

Structure (ADR-66):
    # .dev-knowledge BACKLOG
    ## Big picture            <- paragraph + theme backbone (no stories/tasks)
    ## <Theme>                <- backbone header
    ### <User story>          <- human goal
    So that <why>.            <- the why (required, immediately under the story)
    - [#id] [P1][M] <action> · Done when: <criterion> · refs <…>   <- task bullet

Hard-fail (exit 1) — objective structure only:
  - a task with no enclosing user story, or whose story has no enclosing theme
  - a task missing its [P][S|M|L] band, or missing "Done when:"
  - a missing or duplicate [#id]
  - a done task present — done tasks leave (ADR-65): a `status:done` suffix, a leading
    `[x]` checkbox, a struck bullet, an in-place `~~strikethrough~~`, or a bold
    `**RESOLVED`/`**DONE` marker on a task line
  - a user story with no "So that" line, or a story/task directly under ## Big picture
  - (#156 task-graph) a `· depends-on: #id` referencing an id that is not a live task
    (strict reference-existence — closed ids have left the file), or a cycle in the
    depends-on graph (direct A↔B, indirect A→B→C→A, or self A→A; the path is reported)

Warn-only:
  - a user story with zero tasks
  - (#187 dedup-on-entry) a newly-added task whose normalized-title token-overlap closely
    matches an existing task — a deterministic backstop (Jaccard over the action segment,
    no LLM, ADR-88 do-not-build). STATED LIMIT: will NOT catch low-title-overlap semantic
    dups; the primary dedup remains the architect/CC filing flow.

The optional `· serialize-group: <label>` clause (shared-mutable-resource mutual
exclusion) is surfaced in the OK summary, never a failure. A task may carry ≥1 such
clause — one per shared surface it collides on (multi-surface collision, #167) — and is
placed in EVERY named group. Parallel-safety is derived, not declared: two tasks co-run
iff no depends-on path links them and they share no group.

(No repo: rule — entries are implicitly .dev-knowledge; cross-repo work names repos in
task text under the Cross-repo theme. Monotonic/never-reused id is an assignment
discipline; only uniqueness is enforced statically.)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BIG_PICTURE = "Big picture"
BACKLOG = Path(__file__).resolve().parent.parent / "BACKLOG.md"

_THEME_RE = re.compile(r"^## (.+?)\s*$")
_STORY_RE = re.compile(r"^### (.+?)\s*$")
_TASK_RE = re.compile(r"^- \[#(\d+)\]\s*(.*)$")
_SOTHAT_RE = re.compile(r"^So that\b", re.IGNORECASE)
_PSIZE_RE = re.compile(r"\[P[1-3]\]\[(?:S|M|L)\]")
_DONEWHEN_RE = re.compile(r"Done when:", re.IGNORECASE)
# done-marker: a structured status suffix, a leading done-checkbox, or a struck bullet —
# NOT a bare [x]/~~/"status: done" anywhere in prose (which is legitimate task text).
_DONE_MARKER_RE = re.compile(r"·\s*status:\s*done\b|^- \[[xX]\]|^- ~~")
# in-place resolution marker on a task line — the ADR-65 done-items-LEAVE violation
# class (#83, pilot finding F2). A live task must never be struck through (~~...~~)
# or carry a bold **RESOLVED/**DONE marker; done tasks LEAVE the file. _DONE_MARKER_RE
# above only catches a fully-struck bullet ("- ~~") or "- [x]" — it missed the
# "[#id] ~~...~~ **RESOLVED**" shape the #79 stub exhibited (commit 052e311).
_INPLACE_RESOLVED_RE = re.compile(r"~~.+?~~|\*\*\s*(?:RESOLVED|DONE)\b")
# #156 task-graph fields. Clause-scoped: a `· depends-on:` / `· serialize-group:` clause
# is captured up to the next `·` or end-of-line, so #ids in `refs`/prose are NOT read as
# dependencies. The leading `·` is required — a bare "depends-on" in prose is not a clause.
_DEPENDS_CLAUSE_RE = re.compile(r"·\s*depends-on\s*:\s*([^·]*)")
# serialize-group (#167): delimiter-anchored + ASCII-token label. The label must be a
# single token `[A-Za-z0-9][A-Za-z0-9_-]*` butting the next `·` or end-of-line (the
# `(?=·|$)` anchor) — so a free-text mention of the keyword in a task body (or an example
# with trailing prose / a `<placeholder>`) cannot register as a phantom clause (the
# 2026-06-14 self-trip). finditer (not search) reads EVERY clause, so a task colliding on
# ≥2 surfaces is fully encoded. ASCII-only labels also can't carry a non-cp1252 glyph into
# the summary print (the crash that accompanied the self-trip).
_SERIALIZE_CLAUSE_RE = re.compile(r"·\s*serialize-group\s*:\s*([A-Za-z0-9][A-Za-z0-9_-]*)\s*(?=·|$)")
_DEPID_RE = re.compile(r"#(\d+)")
# #187 dedup-on-entry — deterministic near-duplicate backstop. Compares NORMALIZED-TITLE
# token-sets (the action segment before the first ` · ` clause, band-stripped, lowercased,
# stopworded) by Jaccard overlap; a pair >= _DUP_TITLE_THRESHOLD is a WARN (never a
# hard-fail — Layer-2-safe). STATED LIMIT: a token-overlap heuristic only — it does NOT
# catch low-title-overlap semantic dups (no LLM, ADR-88 do-not-build); the primary dedup
# remains the architect/CC filing flow. _DUP_MIN_TOKENS skips tiny titles (a 2-3 token
# title trivially Jaccard-matches and would be noise). Threshold tuned so the live BACKLOG
# is clean (no false positives on genuinely distinct items) — locked by a regression test.
_DUP_TITLE_THRESHOLD = 0.7
_DUP_MIN_TOKENS = 4
_TOKEN_RE = re.compile(r"[a-z0-9]+")
_TITLE_STOPWORDS = frozenset({
    "the", "and", "for", "with", "that", "this", "via", "per", "not", "into", "from",
    "are", "but", "its", "than", "then", "out", "all", "any", "one", "two", "use",
    "add", "new", "now", "can", "has", "had", "was", "will", "when", "what", "who",
})


def _parse_deps(rest):
    """Return the depends-on ids as BARE strings (e.g. ['23', '45']) — matches task['id']
    form so membership tests are not silently always-false. Only the depends-on clause is
    read; ids in refs/prose are ignored."""
    m = _DEPENDS_CLAUSE_RE.search(rest)
    return _DEPID_RE.findall(m.group(1)) if m else []


def _parse_serialize_groups(rest):
    """Return the serialize-group labels (list[str], possibly empty, order-preserving,
    deduped within a task). Each is a shared-mutable-resource mutual-exclusion label;
    surfaced, never a failure. A task may carry ≥1 clause (one per shared surface it
    collides on, #167); EVERY clause is read (finditer), and the clause is delimiter-
    anchored so prose mentions of the keyword don't register (see _SERIALIZE_CLAUSE_RE)."""
    out = []
    for m in _SERIALIZE_CLAUSE_RE.finditer(rest):
        if m.group(1) not in out:
            out.append(m.group(1))
    return out


# CARRIER-DOCTRINE TWIN (ADR-78): the #156 dep machinery (_DEPENDS_CLAUSE_RE / _DEPID_RE /
# _parse_deps + the two _check_dep_* fns below) is mirrored VERBATIM into the plugin floor
# plugins/tier1-lifecycle/scripts/validate_backlog.py — keep in sync by hand (tracked
# _DEPENDS_CLAUSE_RE twin-drift edge; a mechanical hub<->floor parity check is a queued ADR-88 follow-on).
def _check_dep_references(tasks):
    """Strict reference-existence: every depends-on id must be a live task id (#156)."""
    ids = {t["id"] for t in tasks}
    hard = []
    for t in tasks:
        loc = f'[#{t["id"]}] line {t["line"]}'
        for d in _parse_deps(t["rest"]):
            if d not in ids:
                hard.append(f'depends-on references non-existent id #{d} — {loc}')
    return hard


def _check_dep_cycles(tasks):
    """No-cycle: the depends-on graph must be acyclic — catches direct (A↔B), indirect
    (A→B→C→A), and self (A→A) cycles via a white/gray/black DFS (#156). Dangling ids are
    skipped here (owned by _check_dep_references) so this never KeyErrors."""
    ids = {t["id"] for t in tasks}
    line_of = {}
    adj = {}
    for t in tasks:
        adj.setdefault(t["id"], [])
        line_of.setdefault(t["id"], t["line"])
        for d in _parse_deps(t["rest"]):
            if d in ids:  # skip dangling — reference check reports those
                adj[t["id"]].append(d)

    hard = []
    color = dict.fromkeys(adj, 0)  # 0=white, 1=gray (on stack), 2=black (done)
    stack = []
    seen = set()

    def dfs(node):
        color[node] = 1
        stack.append(node)
        for nb in adj[node]:
            if color[nb] == 1:  # back-edge -> the stack slice [nb..node] is a cycle
                cycle = tuple(stack[stack.index(nb):])
                pivot = cycle.index(min(cycle, key=int))  # rotate to min id -> dedup rotations
                canon = cycle[pivot:] + cycle[:pivot]
                if canon not in seen:
                    seen.add(canon)
                    if len(canon) == 1:
                        hard.append(f'task #{canon[0]} depends on itself — '
                                    f'[#{canon[0]}] line {line_of[canon[0]]}')
                    else:
                        # ASCII arrow — '→' (U+2192) is not in cp1252 and raises
                        # UnicodeEncodeError on a Windows console, crashing the gate
                        # exactly on the cycle path that must print a clear message.
                        path = " -> ".join(f"#{n}" for n in canon) + f" -> #{canon[0]}"
                        hard.append(f'dependency cycle: {path}')
            elif color[nb] == 0:
                dfs(nb)
        stack.pop()
        color[node] = 2

    for node in sorted(adj, key=int):
        if color[node] == 0:
            dfs(node)
    return hard


def serialize_groups(tasks):
    """Map serialize-group label -> [task ids]. A task in ≥2 groups (multi-surface
    collision, #167) is placed in EACH. Informational (surfaced in main)."""
    groups = {}
    for t in tasks:
        for g in _parse_serialize_groups(t["rest"]):
            groups.setdefault(g, []).append(t["id"])
    return groups


def _title_tokens(rest):
    """Normalized-title token-set for #187 dedup: strip the [P][S|M|L] band, take the action
    segment (text before the first ` · ` clause — Done when:/refs/depends-on excluded),
    lowercase, tokenize on [a-z0-9]+, drop stopwords and <3-char tokens. Returns a set."""
    no_band = _PSIZE_RE.sub("", rest)
    action = no_band.split("·", 1)[0]
    return {w for w in _TOKEN_RE.findall(action.lower())
            if len(w) >= 3 and w not in _TITLE_STOPWORDS}


def _check_duplicate_titles(tasks):
    """Deterministic near-duplicate WARN (#187): two tasks whose normalized-title token-sets
    overlap >= _DUP_TITLE_THRESHOLD (Jaccard) are flagged. No LLM — a token-overlap heuristic
    with a STATED LIMIT (does NOT catch low-title-overlap semantic dups). Never a hard-fail;
    Layer-2-safe (reads only). O(n^2) over tasks — trivial at backlog scale."""
    toks = [(t, _title_tokens(t["rest"])) for t in tasks]
    warn = []
    for i in range(len(toks)):
        ti, si = toks[i]
        if len(si) < _DUP_MIN_TOKENS:
            continue
        for j in range(i + 1, len(toks)):
            tj, sj = toks[j]
            if len(sj) < _DUP_MIN_TOKENS:
                continue
            inter = len(si & sj)
            if not inter:
                continue
            jac = inter / len(si | sj)
            if jac >= _DUP_TITLE_THRESHOLD:
                warn.append(
                    f'possible duplicate: [#{ti["id"]}] (line {ti["line"]}) and '
                    f'[#{tj["id"]}] (line {tj["line"]}) share {round(jac * 100)}% title '
                    f'tokens — token-overlap heuristic (does not catch low-overlap semantic dups)')
    return warn


def parse(text):
    """Return (themes, stories, tasks)."""
    themes, stories, tasks = [], [], []
    cur_theme = None
    cur_story = None
    expect_sothat = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        t = _THEME_RE.match(raw)
        if t:
            cur_theme = t.group(1).strip()
            cur_story = None
            expect_sothat = False
            themes.append(cur_theme)
            continue
        s = _STORY_RE.match(raw)
        if s:
            cur_story = {"name": s.group(1).strip(), "theme": cur_theme, "line": lineno,
                         "sothat": False, "ntasks": 0}
            stories.append(cur_story)
            expect_sothat = True
            continue
        k = _TASK_RE.match(raw)
        if k:
            tasks.append({"id": k.group(1), "rest": k.group(2), "raw": raw, "line": lineno,
                          "story": cur_story, "theme": cur_theme})
            if cur_story:
                cur_story["ntasks"] += 1
            expect_sothat = False
            continue
        if expect_sothat and _SOTHAT_RE.match(raw.strip()):
            if cur_story:
                cur_story["sothat"] = True
            expect_sothat = False
            continue
        if raw.strip():
            expect_sothat = False
    return themes, stories, tasks


def validate(themes, stories, tasks):
    """Return (hard_fails, warnings)."""
    hard, warn = [], []
    big = themes.count(BIG_PICTURE)
    if big != 1:
        hard.append(f'expected exactly one "## {BIG_PICTURE}" section, found {big}')
    seen = {}
    for t in tasks:
        loc = f'[#{t["id"]}] line {t["line"]}'
        if t["story"] is None:
            hard.append(f'task not under a user story — {loc}')
        elif not t["story"]["theme"] or t["story"]["theme"] == BIG_PICTURE:
            hard.append(f'task\'s story has no enclosing theme — {loc}')
        if t["id"] in seen:
            hard.append(f'duplicate id {t["id"]}: lines {seen[t["id"]]} and {t["line"]}')
        else:
            seen[t["id"]] = t["line"]
        if not _PSIZE_RE.search(t["rest"]):
            hard.append(f'task missing [P][S|M|L] band — {loc}')
        if not _DONEWHEN_RE.search(t["rest"]):
            hard.append(f'task missing "Done when:" — {loc}')
        if _DONE_MARKER_RE.search(t["raw"]):
            hard.append(f'done task present (done tasks leave the file, ADR-65) — {loc}')
        if _INPLACE_RESOLVED_RE.search(t["raw"]):
            hard.append(f'in-place resolved/struck-through task (done tasks leave the file, ADR-65) — {loc}')
    for s in stories:
        sloc = f'story "{s["name"][:48]}" line {s["line"]}'
        if not s["theme"] or s["theme"] == BIG_PICTURE:
            hard.append(f'user story not under a theme — {sloc}')
        if not s["sothat"]:
            hard.append(f'user story missing a "So that" line — {sloc}')
        if s["ntasks"] == 0:
            warn.append(f'user story with no tasks — {sloc}')
    # #156 task-graph checks — run independently (a reference failure must not mask a real
    # cycle among the valid edges); reference-existence first by convention.
    hard += _check_dep_references(tasks)
    hard += _check_dep_cycles(tasks)
    # #187 dedup-on-entry — deterministic near-duplicate WARN (token-overlap, no LLM)
    warn += _check_duplicate_titles(tasks)
    return hard, warn


def main():
    if not BACKLOG.exists():
        print(f"validate_backlog: {BACKLOG} not found", file=sys.stderr)
        return 1
    themes, stories, tasks = parse(BACKLOG.read_text(encoding="utf-8"))
    hard, warn = validate(themes, stories, tasks)
    for w in warn:
        print(f"WARN  {w}")
    for h in hard:
        print(f"FAIL  {h}")
    if hard:
        print(f"validate_backlog: {len(hard)} hard-fail(s), {len(warn)} warning(s)")
        return 1
    n_themes = len([t for t in themes if t != BIG_PICTURE])
    print(f"validate_backlog: OK ({n_themes} themes, {len(stories)} stories, {len(tasks)} tasks, "
          f"{len(warn)} warning(s))")
    groups = serialize_groups(tasks)
    if groups:
        summary = "; ".join(f"{g} ({', '.join('#' + i for i in members)})"
                            for g, members in sorted(groups.items()))
        print(f"validate_backlog: serialize-groups — {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
