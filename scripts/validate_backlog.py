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
  - a done task present (status:done / [x] / ~~strikethrough~~) — done tasks leave (ADR-65)
  - a user story with no "So that" line, or a story/task directly under ## Big picture

Warn-only: a user story with zero tasks.

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
_DONE_MARKER_RE = re.compile(r"status:\s*done|\[[xX]\]|~~")


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
    for s in stories:
        sloc = f'story "{s["name"][:48]}" line {s["line"]}'
        if not s["theme"] or s["theme"] == BIG_PICTURE:
            hard.append(f'user story not under a theme — {sloc}')
        if not s["sothat"]:
            hard.append(f'user story missing a "So that" line — {sloc}')
        if s["ntasks"] == 0:
            warn.append(f'user story with no tasks — {sloc}')
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
