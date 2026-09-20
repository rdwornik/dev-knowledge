#!/usr/bin/env python
"""generate_organ_index.py — emit ecosystem/organ-index.md, the machine-derived organ roster ([#132]).

WHAT THIS KILLS. "Operator-as-registry": the answer to *which organs exist, what fires
each one, and does it reach reality today* is currently supplied from the operator's
memory plus three hand-maintained prose surfaces (CLAUDE.md §7-§9, ARCHITECTURE Ch2, the
manifest roster). Each is accurate only until the next organ lands. This generator reads
the organ sources themselves and emits one index, on the established generator +
regen-and-diff-freshness-hook pattern (`gen_audit_index.py`, `gen_claude_rosters.py`,
`gen_methodology_roster.py`, `scripts/codemap/`, `scripts/toc/`).

ARCHITECTURE Ch2 already names this file as its verified source: *"the generated
`ecosystem/organ-index.md` (#132) is its verified source … When they disagree, trust the
index."* So the vocabulary here is Ch2's, deliberately, and not a second dialect.

RELOCATED 2026-08-12 (operator ruling A of 2026-08-11; register STANDING_RULINGS K-1):
the target moved from `docs/ORGAN-INDEX.md` to `ecosystem/organ-index.md`. `docs/` is a
Tier-2 GENRE tree (ADR-101 section 1) whose members live in `docs/<genre>/`, and this
file is neither an audit, a decision, a handoff, an intake nor an archive item — it is
generated ecosystem state, the same class as `ecosystem/organ-registry.yaml` (which it
reads) and `ecosystem/doc-counts.md` (which is also generated). It sat loose at the
`docs/` root, the only file that ever did. The name also drops to lowercase kebab-case,
matching every other member of `ecosystem/`:

  distribution  Ch2 "Layer"  — L0 (global ~/.claude) · hub · plugin · pre-commit
  status        Ch2 "Status" — ARMED · RETIRED · DECLARED

WHAT IT DOES NOT CARRY, stated so a reader does not infer coverage that is absent:
**failure posture**. Whether an organ fails closed, fails soft, or only proposes is a
judgement about its code, recoverable from neither a frontmatter block nor a hook id.
Ch2 carries it by hand and stays the source for that column. This index is exhaustive
about *what exists and what fires it*; it is silent about *what happens when it says no*.

SOURCES (the row's own list). Repo-tracked, so the output is a pure function of the
commit:
  .claude/agents/*.md · .claude/commands/*.md · .claude/skills/*/SKILL.md ·
  .claude/workflows/* · .claude/rules/*.md · .claude/settings.json (hooks +
  enabledPlugins) · .pre-commit-config.yaml · plugins/*/ (plugin.json, commands/,
  hooks/hooks.json) · deploy/manifest-v*.yaml (for the `deployed` annotation)

Plus one DECLARED source, `ecosystem/organ-registry.yaml`, which carries the user-level
(`~/.claude`, Ch2 layer L0) organs. **Why declared and not walked:** a live `~/.claude`
read would make the rendered bytes machine-dependent, and a regen-and-diff freshness gate
over machine-dependent bytes reds on every host but the one that last regenerated. The
registry keeps the gate deterministic and portable; `--probe-user-level` is the
non-gating diagnostic that reads the live `~/.claude` and reports drift against it. That
pair is this module's answer to the [#132] "absorbs #248" clause — see the registry file
header for the fork and which arm each half takes.

TRACKED FILES ONLY. Every collector filters its glob through `git ls-files`, because the
same machine-dependence argument applies one level down: an UNTRACKED
`.claude/commands/local.md` would render a `/local` row, and `--check` would then red on
every other checkout of the same commit. `.claude/settings.local.json` is excluded by this
rule rather than by a special case (it is untracked), which is the more honest form —
naming one file by hand would have left every other private scratch file leaking in. The
limit is stated in `tracked_files`: outside a git work tree there is no tracked set, so
filtering is disabled rather than emptying the index.

Loose top-level module BY DESIGN (mirrors gen_audit_index.py / gen_claude_rosters.py /
gen_methodology_roster.py): the codemap enumerates only `scripts/<pkg>/` dirs carrying an
`__init__.py`, so a loose module adds no codemap node and editing it never forces an
ARCHITECTURE.md codemap regen. Do NOT convert it to a package.

Deterministic: same committed inputs -> byte-identical output. The drift check depends on
it, so it is ASSERTED rather than claimed —
`test_render_never_reads_the_user_home` (emptied HOME) and
`test_an_untracked_source_file_does_not_change_the_generated_bytes` (a real git repo)
between them pin both machine-dependence routes.

EVERY structured source is shape-guarded and degrades to a VISIBLE `(unparsed)` /
`(absent)` row, never to an exception and never to a silent skip. That is not defensive
padding: `--check` owes its caller exit 0/1/2, and a traceback gives the pre-commit hook
neither a verdict nor a diff. The four cases that used to escape this — untracked files,
valid-but-wrong-shaped JSON/YAML, silently dropped registry entries, and an absent source
masked by another source's rows — came out of the terra review of 2026-08-11 and each is
pinned by the test that reproduced it.

Layer-2 read-only (ADR-28/36): reads repo state; writes NOTHING except the one generated
target under --write. `--check` and `--probe-user-level` write nothing at all.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_TARGET_REL = Path("ecosystem") / "organ-index.md"

_GENERATED_NOTE = "<!-- generated by generate_organ_index.py; do not edit by hand -->"

# The CLOSED organ-class vocabulary. "Covering all organ classes" (the row's Done-when) is
# measured against this tuple, so the predicate is checkable rather than impressionistic:
# every member gets a section in the rendered index, an empty one included.
ORGAN_CLASSES: tuple[str, ...] = (
    "agent", "command", "skill", "workflow", "rule",
    "session-hook", "git-hook", "plugin",
)

_CLASS_BLURB = {
    "agent": "subagents dispatched with their own context window",
    "command": "operator-invoked slash commands",
    "skill": "model-invoked skills (the model decides when to load one)",
    "workflow": "multi-agent workflow specifications",
    "rule": "always-on instruction files loaded into every session",
    "session-hook": "Claude Code lifecycle hooks (SessionStart / Stop / PreToolUse / …)",
    "git-hook": "git-stage gates declared in `.pre-commit-config.yaml`",
    "plugin": "installable plugins that carry organs of their own",
}

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
# A roster line names its organ before the em-dash separator or an opening parenthesis:
#   "/ship — merge the current branch…"  ->  "/ship"
#   "Stop: propose_closures (tier1…)"    ->  "Stop: propose_closures"
_ROSTER_NAME_RE = re.compile(r"^(.*?)(?:\s+[—-]\s|\s\()")
_MANIFEST_VERSION_RE = re.compile(r"^manifest-v(\d+)\.(\d+)\.(\d+)\.yaml$")
# The script a hook command invokes, used as the hook's display name: the last path-ish
# token ending in a known script extension.
_SCRIPT_TOKEN_RE = re.compile(r"([\w.-]+\.(?:py|ps1|js|sh))")
_EXT_RE = re.compile(r"\.(?:py|ps1|js|sh)$")

# Sentinel for "compute the tracked set yourself" — distinct from None, which means
# "there is no tracked set" (not a git work tree) and legitimately disables filtering.
_AUTO = object()

_STATUS_ARMED = "ARMED"
_STATUS_RETIRED = "RETIRED"
_STATUS_DECLARED = "DECLARED"
# THE ARMING VOCABULARY for hooks (lane-l3-organ-truth). A hook is ARMED only when the live
# config will actually fire it, MANUAL when its only stage is `manual` (it runs on demand or in
# the conductor, never at the git event), ABSENT when the config that would fire it is switched
# off. PRESENT IS NOT ARMED: the index used to stamp every hook it found ARMED, and 19 of 36
# commit hooks were set to `manual`, so the one surface that answers "what protects us" lied.
_STATUS_MANUAL = "MANUAL"
_STATUS_ABSENT = "ABSENT"
ARMING_STATUSES = (_STATUS_ARMED, _STATUS_MANUAL, _STATUS_ABSENT)
_UNPARSED = "(unparsed)"

# `manual_until: YYYY-MM-DD` is how a hook DECLARES the date its manual stage lapses. It is read
# as a token inside the hook's own block of `.pre-commit-config.yaml` (a key OR a comment: the
# YAML parser drops comments, so this is a text read scoped to ONE hook, not a config parse).
_HOOK_ID_LINE_RE = re.compile(r"^\s*-\s+id:\s*([^\s#]+)")
_MANUAL_UNTIL_RE = re.compile(r"manual_until:\s*[\"']?(\d{4}-\d{2}-\d{2})")


class Organ(NamedTuple):
    """One row of the index — the six columns the [#132] row names, in its order."""

    name: str
    cls: str
    trigger: str
    source: str
    distribution: str
    status: str


# --------------------------------------------------------------------------------------
# small readers (each degrades LOUDLY — a source it cannot parse yields a visible row or
# an explicit absence, never a silently shorter index)
# --------------------------------------------------------------------------------------

def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _frontmatter_field(text: str, field: str) -> str | None:
    """A top-level `field: value` scalar from a leading YAML frontmatter block, or None.

    Regex-simple by design, matching `gen_claude_rosters._frontmatter_field`: organ
    frontmatter here is flat, and a folded `description: >` block is read as empty rather
    than mis-joined (only `name`/`description` are consumed, and `description` is used
    solely for the RETIRED derivation below).
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None
    for line in m.group(1).splitlines():
        if line.startswith(f"{field}:"):
            return line[len(field) + 1:].strip() or None
    return None


def _status_from_description(description: str | None) -> str:
    """RETIRED iff the organ's own description says so — derived, never hand-flagged.

    `/override`'s frontmatter opens `RETIRED (ADR-85 amendment …)`, which is the organ
    declaring its own status at the source. Reading it here means a retirement recorded
    once shows up in the index without a second edit anywhere.
    """
    if description and description.strip().upper().startswith("RETIRED"):
        return _STATUS_RETIRED
    return _STATUS_ARMED


def _rel(path: Path, root: Path) -> str:
    """Repo-relative POSIX path — stable across platforms (the gate compares bytes)."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _script_name(command: str) -> str | None:
    """The script a hook command runs, e.g. `propose_closures.py`, or None."""
    hits = _SCRIPT_TOKEN_RE.findall(command)
    return hits[-1] if hits else None


def _mapping(obj: object) -> dict | None:
    """`obj` if it is a mapping, else None. Guards VALID documents of the WRONG SHAPE.

    `json.loads("[]")` and `yaml.safe_load("repos: [bad]")` both parse cleanly and then
    explode on the first `.get()`. A traceback out of `--check` is worse than a stale
    index: the hook's contract is exit 0/1/2, and a crash gives the caller neither a
    verdict nor a diff (terra review 2026-08-11, finding 2).
    """
    return obj if isinstance(obj, dict) else None


def _sequence(obj: object) -> list | None:
    """`obj` if it is a list/tuple, else None. A str is REJECTED deliberately — iterating
    one yields characters, which is how `organs: bad` silently became zero rows."""
    return list(obj) if isinstance(obj, (list, tuple)) else None


def tracked_files(root: Path) -> frozenset[str] | None:
    """Repo-relative POSIX paths git TRACKS, or None when `root` is not a git work tree.

    THE DETERMINISM BOUNDARY, and the reason this exists. The collectors glob the working
    tree; an UNTRACKED `.claude/commands/local.md` would otherwise render as a `/local`
    row, so the generated bytes would depend on one machine's private scratch files and
    `--check` would red on every other checkout of the same commit — the freshness gate
    would be unholdable, which is precisely what this module promises it is not. Caught by
    the terra review of 2026-08-11 (finding 1), reproduced live, fixed here.

    None means "cannot tell" and disables filtering rather than emptying the index: the
    synthetic trees the tests build are not repos, and a generator that returned nothing
    outside a git checkout would be a worse failure than the one it prevents. Stated as an
    honest limit rather than hidden — outside a work tree the untracked-file hazard above
    is back.
    """
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                             capture_output=True, text=True, encoding="utf-8", timeout=30)
    except (OSError, subprocess.SubprocessError):
        # SubprocessError covers TimeoutExpired. Bounded 2026-08-12 alongside the identical
        # gap terra finding 2 raised against the gen_audit_index twin: the same unbounded
        # wait, in the same function, inside the same pre-commit gate class.
        return None
    if out.returncode != 0:
        return None
    return frozenset(p.replace("\\", "/") for p in out.stdout.split("\0") if p)


def _is_tracked(path: Path, root: Path, tracked: frozenset[str] | None) -> bool:
    return tracked is None or _rel(path, root) in tracked


def _files(root: Path, rel_dir: str, pattern: str,
           tracked: frozenset[str] | None) -> list[Path]:
    """Sorted, TRACKED source files under `rel_dir` matching `pattern`."""
    return [p for p in sorted((root / rel_dir).glob(pattern))
            if _is_tracked(p, root, tracked)]


def _absent(cls: str, rel: str, distribution: str = "hub") -> Organ:
    """A visible row for a declared source that is not on disk.

    Without this, a vanished `.claude/agents/` produced an EMPTY collector result, and an
    empty result is invisible whenever another source (the L0 registry, the plugin) still
    populates that class — so the section rendered normally and the missing source left no
    trace. "Loud degradation" has to be per-SOURCE, not per-class (terra finding 4).
    """
    return Organ(f"({rel} — source absent)", cls, "(absent)", rel, distribution, "(absent)")


def _resolve(root: Path, tracked: object) -> frozenset[str] | None:
    return tracked_files(root) if tracked is _AUTO else tracked  # type: ignore[return-value]


# --------------------------------------------------------------------------------------
# collectors — one per organ source
# --------------------------------------------------------------------------------------

def collect_agents(root: Path, tracked: object = _AUTO) -> list[Organ]:
    tracked = _resolve(root, tracked)
    if not (root / ".claude" / "agents").is_dir():
        return [_absent("agent", ".claude/agents/")]
    out = []
    for p in _files(root, ".claude/agents", "*.md", tracked):
        text = _read(p) or ""
        name = _frontmatter_field(text, "name") or p.stem
        out.append(Organ(name, "agent", "subagent-dispatch", _rel(p, root), "hub",
                         _status_from_description(_frontmatter_field(text, "description"))))
    return out


def collect_commands(root: Path, tracked: object = _AUTO) -> list[Organ]:
    tracked = _resolve(root, tracked)
    if not (root / ".claude" / "commands").is_dir():
        return [_absent("command", ".claude/commands/")]
    out = []
    for p in _files(root, ".claude/commands", "*.md", tracked):
        text = _read(p) or ""
        name = _frontmatter_field(text, "name") or p.stem
        out.append(Organ(f"/{name}", "command", "operator-invoke", _rel(p, root), "hub",
                         _status_from_description(_frontmatter_field(text, "description"))))
    return out


def collect_skills(root: Path, tracked: object = _AUTO) -> list[Organ]:
    tracked = _resolve(root, tracked)
    if not (root / ".claude" / "skills").is_dir():
        return [_absent("skill", ".claude/skills/")]
    out = []
    for skill_md in _files(root, ".claude/skills", "*/SKILL.md", tracked):
        text = _read(skill_md) or ""
        name = _frontmatter_field(text, "name") or skill_md.parent.name
        out.append(Organ(name, "skill", "model-invoke", _rel(skill_md, root), "hub",
                         _status_from_description(_frontmatter_field(text, "description"))))
    return out


def collect_workflows(root: Path, tracked: object = _AUTO) -> list[Organ]:
    tracked = _resolve(root, tracked)
    if not (root / ".claude" / "workflows").is_dir():
        return [_absent("workflow", ".claude/workflows/")]
    return [Organ(p.name, "workflow", "operator (Workflow) or cloud Routine",
                  _rel(p, root), "hub", _STATUS_ARMED)
            for p in _files(root, ".claude/workflows", "*", tracked) if p.is_file()]


def collect_rules(root: Path, tracked: object = _AUTO) -> list[Organ]:
    tracked = _resolve(root, tracked)
    if not (root / ".claude" / "rules").is_dir():
        return [_absent("rule", ".claude/rules/")]
    return [Organ(p.stem, "rule", "context-load (every session)", _rel(p, root), "hub",
                  _STATUS_ARMED)
            for p in _files(root, ".claude/rules", "*.md", tracked)]


_SETTINGS_ABSENT = "absent"
_SETTINGS_BAD = "bad"


def _settings(root: Path) -> tuple[dict, str | None]:
    """(parsed .claude/settings.json, problem). `problem` is None when it parsed to a
    mapping, `_SETTINGS_ABSENT` when the file is not there, `_SETTINGS_BAD` when it is
    unreadable OR parses to something that is not a mapping (`[]`, `"x"`, `3`).

    The not-a-mapping case is the terra finding: it used to sail past the JSON decode and
    raise `AttributeError` on the first `.get()`, taking `--check` out through a traceback
    instead of its 0/1/2 contract.
    """
    text = _read(root / ".claude" / "settings.json")
    if text is None:
        return {}, _SETTINGS_ABSENT
    try:
        parsed = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return {}, _SETTINGS_BAD
    data = _mapping(parsed)
    return (data, None) if data is not None else ({}, _SETTINGS_BAD)


def collect_session_hooks(root: Path, tracked: object = _AUTO) -> list[Organ]:
    data, problem = _settings(root)
    rel = ".claude/settings.json"
    if problem == _SETTINGS_ABSENT:
        return [_absent("session-hook", rel)]
    if problem == _SETTINGS_BAD:
        return [Organ("(settings.json unparseable)", "session-hook", _UNPARSED, rel,
                      "hub", _UNPARSED)]
    # `disableAllHooks: true` switches every hook in this file off, so a hook that is merely
    # PRESENT there reaches nothing -- ABSENT, not ARMED.
    status = _STATUS_ABSENT if data.get("disableAllHooks") is True else _STATUS_ARMED
    return _hooks_from_mapping(data.get("hooks"), rel, "hub", status)


def _hooks_from_mapping(hooks: object, source: str, distribution: str,
                        status: str) -> list[Organ]:
    """Claude Code's `{event: [{matcher, hooks: [{command}]}]}` shape -> Organ rows.

    Name is `<Event>: <script>`; trigger is the event plus its matcher when one narrows
    it, which is the distinction Ch2's Trigger column makes by hand.

    EVERY nested level is shape-guarded and a wrong shape yields a VISIBLE `(unparsed)`
    row, never an exception and never a silent skip: `{"Stop": "bad"}` is valid JSON that
    used to raise on `group.get`, and a hook the index quietly omits is the exact claim
    this file exists to stop making.
    """
    mapping = _mapping(hooks)
    if mapping is None:
        return ([] if hooks is None else
                [Organ(f"({source}: hooks is not a mapping)", "session-hook", _UNPARSED,
                       source, distribution, _UNPARSED)])
    out = []
    for event in sorted(mapping, key=str):
        groups = _sequence(mapping[event])
        if groups is None:
            out.append(Organ(f"{event}: (not a hook list)", "session-hook", _UNPARSED,
                             source, distribution, _UNPARSED))
            continue
        for group in groups:
            g = _mapping(group)
            if g is None:
                out.append(Organ(f"{event}: (malformed hook group)", "session-hook",
                                 _UNPARSED, source, distribution, _UNPARSED))
                continue
            matcher = str(g.get("matcher") or "").strip()
            entries = _sequence(g.get("hooks")) or []
            for hook in entries:
                h = _mapping(hook)
                if h is None:
                    out.append(Organ(f"{event}: (malformed hook entry)", "session-hook",
                                     _UNPARSED, source, distribution, _UNPARSED))
                    continue
                command = str(h.get("command") or "")
                script = _script_name(command) or "(inline command)"
                trigger = f"{event} ({matcher})" if matcher else str(event)
                out.append(Organ(f"{event}: {script}", "session-hook", trigger, source,
                                 distribution, status))
    return out


def collect_git_hooks(root: Path, tracked: object = _AUTO) -> list[Organ]:  # noqa: ARG001
    """Every hook id in `.pre-commit-config.yaml`, with its stage as the trigger.

    Stage resolution mirrors pre-commit's own: a hook's explicit `stages:` wins, else the
    file's `default_stages:`, else pre-commit's built-in default. Rendering the resolved
    stage (rather than the declared one) is the point — a gate's trigger is what it does,
    not what it omits to say.
    """
    text = _read(root / ".pre-commit-config.yaml")
    rel = ".pre-commit-config.yaml"
    if text is None:
        return [_absent("git-hook", rel, "pre-commit")]
    bad = [Organ("(.pre-commit-config.yaml unparseable)", "git-hook", _UNPARSED, rel,
                 "pre-commit", _UNPARSED)]
    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError:
        return bad
    data = _mapping(parsed)
    if data is None:
        return bad
    default_stages = _sequence(data.get("default_stages")) or ["pre-commit"]
    manual_until = _manual_until_by_hook(text)
    repos = _sequence(data.get("repos"))
    if repos is None:
        return bad if data.get("repos") is not None else []
    out = []
    for repo in repos:
        r = _mapping(repo)
        if r is None:
            out.append(Organ("(malformed repo entry)", "git-hook", _UNPARSED, rel,
                             "pre-commit", _UNPARSED))
            continue
        origin = r.get("repo", "local")
        for hook in _sequence(r.get("hooks")) or []:
            h = _mapping(hook)
            if h is None:
                out.append(Organ("(malformed hook entry)", "git-hook", _UNPARSED, rel,
                                 "pre-commit", _UNPARSED))
                continue
            hid = h.get("id")
            if not hid:
                continue
            stages = _sequence(h.get("stages")) or default_stages
            source = rel if origin == "local" else f"{rel} → {origin}"
            out.append(Organ(str(hid), "git-hook", ", ".join(str(s) for s in stages),
                             source, "pre-commit",
                             _hook_arming(str(hid), stages, manual_until)))
    return sorted(out)


def _manual_until_by_hook(text: str) -> dict[str, str]:
    """`{hook id: 'YYYY-MM-DD'}` for every hook whose own block declares `manual_until:`.

    Scoped to ONE hook: a token attaches to the nearest preceding `- id:` line, so a header
    comment above the first hook (or a token in a sibling's block) never leaks across.
    """
    out: dict[str, str] = {}
    current: str | None = None
    for line in text.splitlines():
        m = _HOOK_ID_LINE_RE.match(line)
        if m:
            current = m.group(1)
            continue
        d = _MANUAL_UNTIL_RE.search(line)
        if d and current is not None:
            out.setdefault(current, d.group(1))
    return out


def _hook_arming(hook_id: str, stages: list, manual_until: dict[str, str]) -> str:
    """ARMED unless the hook's ONLY stage is `manual`; then MANUAL, dated if it declares one.

    A hook listing `manual` beside a real stage IS armed at that stage -- `manual` adds an
    on-demand way to run it, it does not switch the automatic one off.
    """
    if {str(s) for s in stages} == {"manual"}:
        until = manual_until.get(hook_id)
        return f"{_STATUS_MANUAL} until {until}" if until else _STATUS_MANUAL
    return _STATUS_ARMED


def _enabled_plugin_names(root: Path) -> set[str]:
    """Plugin names enabled in settings.json, stripped of their `@marketplace` suffix."""
    data, problem = _settings(root)
    if problem is not None:
        return set()
    enabled = _mapping(data.get("enabledPlugins")) or {}
    return {str(k).split("@", 1)[0] for k, v in enabled.items() if v}


def collect_plugins(root: Path, tracked: object = _AUTO) -> list[Organ]:
    """Each `plugins/<name>/` — the plugin itself plus the commands and hooks it carries.

    Status is DERIVED from settings.json `enabledPlugins` and INHERITED by everything the
    plugin ships: a disabled plugin's `/ship` is present on disk and reaches nothing, and
    an index that called it ARMED would be making exactly the claim this file exists to
    stop making.
    """
    tracked = _resolve(root, tracked)
    if not (root / "plugins").is_dir():
        return [_absent("plugin", "plugins/", "plugin")]
    enabled = _enabled_plugin_names(root)
    out: list[Organ] = []
    for plugin_json in _files(root, "plugins", "*/.claude-plugin/plugin.json", tracked):
        plugin_dir = plugin_json.parent.parent
        text = _read(plugin_json) or ""
        try:
            meta = _mapping(json.loads(text)) or {}
        except (json.JSONDecodeError, ValueError):
            meta = {}
        name = str(meta.get("name") or plugin_dir.name)
        version = str(meta.get("version") or "")
        status = _STATUS_ARMED if name in enabled else _STATUS_DECLARED
        trigger = ("enabled in .claude/settings.json" if status == _STATUS_ARMED
                   else "declared, not enabled here")
        if version:
            trigger = f"{trigger} (v{version})"
        out.append(Organ(name, "plugin", trigger, _rel(plugin_json, root), "plugin",
                         status))
        rel_dir = _rel(plugin_dir, root)
        for cmd in _files(root, f"{rel_dir}/commands", "*.md", tracked):
            ctext = _read(cmd) or ""
            cname = _frontmatter_field(ctext, "name") or cmd.stem
            cstatus = status if status != _STATUS_ARMED else _status_from_description(
                _frontmatter_field(ctext, "description"))
            out.append(Organ(f"/{cname}", "command", "operator-invoke", _rel(cmd, root),
                             "plugin", cstatus))
        hooks_json = plugin_dir / "hooks" / "hooks.json"
        htext = _read(hooks_json) if _is_tracked(hooks_json, root, tracked) else None
        if htext is not None:
            try:
                hdata = _mapping(json.loads(htext))
            except (json.JSONDecodeError, ValueError):
                hdata = None
            if hdata is None:
                out.append(Organ(f"({rel_dir}/hooks/hooks.json unparseable)",
                                 "session-hook", _UNPARSED, _rel(hooks_json, root),
                                 "plugin", _UNPARSED))
            else:
                # A hook of a plugin that is not enabled reaches nothing: ABSENT (the plugin
                # and its commands stay DECLARED -- they exist and can be enabled).
                hook_status = _STATUS_ARMED if status == _STATUS_ARMED else _STATUS_ABSENT
                out += _hooks_from_mapping(hdata.get("hooks"), _rel(hooks_json, root),
                                           "plugin", hook_status)
    return out


def collect_declared(root: Path) -> list[Organ]:
    """The `ecosystem/organ-registry.yaml` rows — the off-repo (L0) organs.

    A malformed row renders with `(unparsed)` in the field it is missing rather than being
    dropped: a registry entry that vanishes because of a typo is the failure mode this
    whole index exists to remove.
    """
    rel = "ecosystem/organ-registry.yaml"
    text = _read(root / rel)
    if text is None:
        return []
    bad = [Organ("(organ-registry.yaml unparseable)", "rule", _UNPARSED, rel, "L0",
                 _UNPARSED)]
    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError:
        return bad
    data = _mapping(parsed)
    if data is None:
        return bad
    rows = _sequence(data.get("organs"))
    if rows is None:
        # `organs: bad` used to iterate the STRING and skip every character in silence —
        # a registry that renders zero rows and says nothing (terra finding 3).
        return bad if data.get("organs") is not None else []
    out = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            out.append(Organ(f"(registry entry {i} is not a mapping)", "rule", _UNPARSED,
                             rel, "L0", _UNPARSED))
            continue
        cls = str(row.get("class") or _UNPARSED)
        out.append(Organ(
            str(row.get("name") or _UNPARSED),
            cls if cls in ORGAN_CLASSES else _UNPARSED,
            str(row.get("trigger") or _UNPARSED),
            str(row.get("source") or _UNPARSED),
            str(row.get("distribution") or "L0"),
            str(row.get("status") or _UNPARSED),
        ))
    return out


# --------------------------------------------------------------------------------------
# the `deployed` annotation
# --------------------------------------------------------------------------------------

def resolve_manifest_path(root: Path) -> Path | None:
    """The MAX-semver `deploy/manifest-v*.yaml`, or None. Mirrors
    `gen_methodology_roster.resolve_manifest_path`, but returns None instead of raising —
    this generator degrades to un-annotated rows rather than failing the gate."""
    candidates: list[tuple[tuple[int, ...], Path]] = []
    for p in sorted((root / "deploy").glob("manifest-v*.yaml")):
        m = _MANIFEST_VERSION_RE.match(p.name)
        if m:
            candidates.append((tuple(int(g) for g in m.groups()), p))
    if not candidates:
        return None
    candidates.sort()
    return candidates[-1][1]


def deployed_organ_names(root: Path) -> set[str]:
    """Organ names the current manifest declares deployable, from `roster[].line`.

    HONEST LIMIT, stated because the annotation looks stronger than it is: this is a
    NAME-TOKEN match against the leading segment of each active roster line, not a
    resolved artifact identity. A roster line re-worded to lead with different text
    silently drops its annotation. The `roster-freshness` hook already gates the roster
    against the manifest, so the drift window is roster-line PHRASING only — and the
    annotation is decoration on a row that is otherwise fully derived.

    One phrasing difference is real today and is absorbed rather than tolerated (see
    `_deployed_match`): the manifest writes the Tier-1 Stop hook as
    `Stop: propose_closures`, while the hook's own command names `propose_closures.py`.
    Matching also on the extension-stripped form keeps that row annotated.
    """
    path = resolve_manifest_path(root)
    if path is None:
        return set()
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return set()
    names: set[str] = set()
    for comp in data.get("components") or []:
        if comp.get("status") != "active":
            continue
        roster = comp.get("roster")
        if not isinstance(roster, dict):
            continue
        line = str(roster.get("line") or "").strip()
        if not line:
            continue
        m = _ROSTER_NAME_RE.match(line)
        names.add((m.group(1) if m else line).strip())
    return names


def _deployed_match(name: str, deployed: set[str]) -> bool:
    """Is this organ named by an active manifest roster line?

    Exact match first, then the extension-stripped form — the manifest names the Tier-1
    Stop hook `Stop: propose_closures` while the hook command names `propose_closures.py`,
    and an index that dropped the `deployed` mark over a `.py` would be reporting a
    distribution fact wrongly rather than reporting a phrasing difference.
    """
    return name in deployed or _EXT_RE.sub("", name) in deployed


# --------------------------------------------------------------------------------------
# assembly + render
# --------------------------------------------------------------------------------------

def collect_organs(root: Path = _REPO_ROOT) -> list[Organ]:
    """Every organ, from every source, with the `deployed` annotation applied.

    Order is the render order: class order per ORGAN_CLASSES, then name within a class.
    Deterministic by construction — every collector sorts, and nothing reads `~`.
    """
    # Resolved ONCE, then threaded through: one `git ls-files` per render keeps the cost
    # flat and, more importantly, keeps every collector on the same view of what is
    # tracked (a per-collector call could straddle a concurrent index change).
    tracked = tracked_files(root)
    organs: list[Organ] = []
    for collector in (collect_agents, collect_commands, collect_skills, collect_workflows,
                      collect_rules, collect_session_hooks, collect_git_hooks,
                      collect_plugins):
        organs += collector(root, tracked)
    organs += collect_declared(root)

    deployed = deployed_organ_names(root)
    annotated = [
        o._replace(distribution=f"{o.distribution} · deployed")
        if _deployed_match(o.name, deployed) else o
        for o in organs
    ]
    class_rank = {c: i for i, c in enumerate(ORGAN_CLASSES)}
    annotated.sort(key=lambda o: (class_rank.get(o.cls, len(ORGAN_CLASSES)), o.name,
                                  o.source))
    return annotated


def _cell(value: str) -> str:
    """Markdown-table-safe cell: a literal pipe would silently split the row."""
    return value.replace("|", "\\|")


def render_index(root: Path = _REPO_ROOT) -> str:
    organs = collect_organs(root)
    by_class: dict[str, list[Organ]] = {c: [] for c in ORGAN_CLASSES}
    for o in organs:
        by_class.setdefault(o.cls, []).append(o)

    coverage = " · ".join(f"{c} {len(by_class.get(c, []))}" for c in ORGAN_CLASSES)
    out = [
        "# Organ index — generated inventory of every organ in this repo",
        "",
        "> **What fires, from where, and does it reach reality today.** Machine-derived",
        "> from the organ sources themselves — `.claude/{agents,commands,skills,workflows,",
        "> rules}`, `.claude/settings.json`, `.pre-commit-config.yaml`, the",
        "> `tier1-lifecycle` plugin manifest — plus the DECLARED user-level (`L0`) rows in",
        "> `ecosystem/organ-registry.yaml`. Vocabulary is `ARCHITECTURE.md` Ch2's:",
        "> **distribution** is Ch2's Layer (`L0` · `hub` · `plugin` · `pre-commit`),",
        "> **status** is Ch2's Status (`ARMED` · `RETIRED` · `DECLARED`) plus, for hooks,",
        "> the arming truth read from the live config: `ARMED` fires at its stage today,",
        "> `MANUAL` is set to the manual stage only (with its `manual_until` date where one",
        "> is declared), `ABSENT` is present in a config that is switched off. A hook is",
        "> never `ARMED` on the strength of being listed. `· deployed` marks an organ the",
        "> current `deploy/manifest-v*.yaml` ships to consumers.",
        ">",
        "> **This index does NOT carry failure posture** (fail-closed / fail-soft /",
        "> propose-only). That is a judgement about an organ's code, derivable from no",
        "> frontmatter block or hook id; `ARCHITECTURE.md` Ch2 carries it by hand and stays",
        "> the source for it. Read this file for *what exists and what fires it*, Ch2 for",
        "> *what happens when it says no*.",
        ">",
        "> The `L0` rows are DECLARED, not walked: reading the operator's `~/.claude` live",
        "> would make these bytes machine-dependent and the freshness gate unholdable on",
        "> any other host. `python scripts/generate_organ_index.py --probe-user-level` is",
        "> the non-gating diagnostic that compares the registry against a live `~/.claude`.",
        ">",
        "> Do not hand-edit. Regenerate: `python scripts/generate_organ_index.py --write`",
        "",
        _GENERATED_NOTE,
        "",
        f"**{len(organs)} organs across {len(ORGAN_CLASSES)} classes.**",
        "",
        f"**Coverage:** {coverage}",
    ]
    for cls in ORGAN_CLASSES:
        rows = by_class.get(cls, [])
        out += ["", f"## {cls}", "", f"_{_CLASS_BLURB.get(cls, '')}_", ""]
        if not rows:
            out.append("_(no organ in this class)_")
            continue
        out += ["| Name | Class | Trigger | Source | Distribution | Status |",
                "|---|---|---|---|---|---|"]
        for o in rows:
            out.append(
                f"| `{_cell(o.name)}` | {_cell(o.cls)} | {_cell(o.trigger)} "
                f"| `{_cell(o.source)}` | {_cell(o.distribution)} | {_cell(o.status)} |")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------------------
# the arming claim, read BACK from a rendered index (lane-l3-organ-truth)
# --------------------------------------------------------------------------------------

_HOOK_CLASSES = ("git-hook", "session-hook")


def _arming_word(status: str) -> str:
    """`MANUAL until 2026-10-04` -> `MANUAL`: the verdict without its date."""
    return status.split()[0] if status.split() else ""


def index_arming_claims(text: str) -> dict[tuple[str, str, str], str]:
    """`{(class, name, source): status}` for every hook row of a RENDERED index.

    Read from the committed bytes, not recomputed, because the point is to hold what the index
    SAYS against what the config DOES. A row that does not split into the six columns is
    skipped (the freshness gate, not this reader, owns a malformed table).
    """
    claims: dict[tuple[str, str, str], str] = {}
    cls: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            cls = line[3:].strip()
            continue
        if cls not in _HOOK_CLASSES or not line.startswith("| `"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) != 6:
            continue
        name, source = cells[0].strip("`"), cells[3].strip("`")
        claims[(cls, name.replace("\\|", "|"), source.replace("\\|", "|"))] = cells[5]
    return claims


def arming_contradictions(root: Path) -> list[str] | None:
    """Every hook whose arming claim in the COMMITTED index differs from the live config.

    None when there is no index to hold (the caller decides what an absent ground truth
    means -- register ruling Z-G4 says FAIL, never skip). Otherwise one sentence per
    contradiction, each naming the hook, what the index claims and what the config says. A
    hook the live config no longer carries at all is a claim of ARMED against ABSENT.

    NOT CHECKED, stated so a green result is not over-read: a live hook the index OMITS (that
    is staleness, and `--check` owns it) and rows whose live status is `(unparsed)`.
    """
    text = _read(root / _TARGET_REL)
    if text is None:
        return None
    live = {(o.cls, o.name, o.source): o.status
            for o in collect_organs(root) if o.cls in _HOOK_CLASSES}
    out: list[str] = []
    for key, claimed in sorted(index_arming_claims(text).items()):
        cls, name, source = key
        actual = live.get(key)
        if actual is None:
            if _arming_word(claimed) == _STATUS_ARMED:
                out.append(f"{cls} `{name}` ({source}): the index says {claimed}, and the live "
                           f"config carries no such hook ({_STATUS_ABSENT})")
            continue
        if actual == _UNPARSED or _arming_word(claimed) == _arming_word(actual):
            continue
        out.append(f"{cls} `{name}` ({source}): the index says {claimed}, the live config "
                   f"says {actual}")
    return out


# --------------------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------------------

def _cmd_write(root: Path) -> int:
    target = root / _TARGET_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_index(root), encoding="utf-8", newline="\n")
    print(f"generate_organ_index: wrote {_TARGET_REL.as_posix()}")
    return 0


def _cmd_check(root: Path) -> int:
    """Regen-and-diff drift check. Exit 0 clean / 1 stale (+unified diff) / 2 target
    missing — the same three-way contract the peer generators' freshness hooks run."""
    target = root / _TARGET_REL
    rel = _TARGET_REL.as_posix()
    if not target.exists():
        print(f"error: {rel} not found — generate it: "
              f"python scripts/generate_organ_index.py --write", file=sys.stderr)
        return 2
    fresh = render_index(root)
    current = target.read_text(encoding="utf-8")
    if current == fresh:
        return 0
    diff = "".join(difflib.unified_diff(
        current.splitlines(keepends=True), fresh.splitlines(keepends=True),
        fromfile=f"{rel} (current)", tofile=f"{rel} (fresh)"))
    print(diff, file=sys.stderr)
    print(f"generate_organ_index: {rel} is stale vs the organ sources — regenerate: "
          f"python scripts/generate_organ_index.py --write", file=sys.stderr)
    return 1


def _live_user_level(home: Path) -> list[tuple[str, str]]:
    """[(name, source), …] read from a live `~/.claude` — commands, skills, agents, rules.

    Names are rendered the way the registry writes them (`/name` for a command) so the two
    sets compare directly. Read-only; a missing directory is simply absent.
    """
    base = home / ".claude"
    found: list[tuple[str, str]] = []
    for sub, fmt in (("commands", "/{}"), ("agents", "{}"), ("rules", "{}")):
        for p in sorted((base / sub).glob("*.md")):
            found.append((fmt.format(p.stem), f"~/.claude/{sub}/{p.name}"))
    for d in sorted((base / "skills").glob("*")):
        if (d / "SKILL.md").is_file():
            found.append((d.name, f"~/.claude/skills/{d.name}/"))
    return found


# The classes `_live_user_level` can actually inventory. A session hook is a command
# STRING inside `~/.claude/settings.json`, not a file the probe can enumerate, so
# comparing those rows would report every one of them as missing — false drift, which is
# worse than the silence it replaces.
_PROBEABLE_CLASSES = frozenset({"command", "agent", "rule", "skill"})


def _cmd_probe_user_level(root: Path, home: Path) -> int:
    """Diagnostic: live `~/.claude` vs the declared registry. Writes nothing, gates
    nothing, ALWAYS exits 0 — a machine-dependent reading has no place in a check."""
    declared = {o.name for o in collect_declared(root) if o.cls in _PROBEABLE_CLASSES}
    live = _live_user_level(home)
    live_names = {n for n, _ in live}

    print(f"generate_organ_index --probe-user-level (home: {home})")
    print("  read-only diagnostic; wired into no gate; writes nothing")
    undeclared = [(n, s) for n, s in live if n not in declared]
    absent = sorted(n for n in declared if n not in live_names)
    for name, source in undeclared:
        print(f"  undeclared: {name}  ({source}) — present in ~/.claude, "
              f"absent from ecosystem/organ-registry.yaml")
    for name in absent:
        print(f"  declared but absent: {name} — in the registry, not found under "
              f"{home / '.claude'}")
    if not undeclared and not absent:
        print("  no drift: every probeable ~/.claude organ matches the registry")
    print("  SCOPE: commands / agents / rules / skills only. Session hooks in "
          "~/.claude/settings.json are declared-only and NOT probed — they are command "
          "strings, not a file inventory, so this report says nothing about them.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="generate_organ_index",
        description="Generate/check ecosystem/organ-index.md (the machine-derived organ roster)")
    parser.add_argument("--write", action="store_true",
                        help="regenerate the index from the organ sources")
    parser.add_argument("--check", action="store_true",
                        help="check the index against the sources (default action)")
    parser.add_argument("--probe-user-level", action="store_true",
                        help="read-only drift report: live ~/.claude vs the declared "
                             "registry (writes nothing, always exits 0)")
    parser.add_argument("--repo-root", default=None,
                        help="repo root to operate on (defaults to this script's repo)")
    parser.add_argument("--home", default=None,
                        help="home directory for --probe-user-level (defaults to ~)")
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve() if args.repo_root else _REPO_ROOT
    if args.probe_user_level:
        home = Path(args.home).resolve() if args.home else Path.home()
        return _cmd_probe_user_level(root, home)
    if args.write:
        return _cmd_write(root)
    return _cmd_check(root)


if __name__ == "__main__":
    sys.exit(main())
