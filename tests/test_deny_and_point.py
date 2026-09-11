"""Tests for scripts/hooks/deny_and_point.py -- the [#727] deny-and-point guard.

RED-FIRST (ADR-108 §B). Every test here was written and run BEFORE the module
existed; the whole file errors on collection until `deny_and_point.py` lands.

The row's Done-when names two tests explicitly and the filing lane added a third
concern, so the file is organised as those three obligations plus the wire:

  A. THE TRIP-TEST      a raw grep over a governed question is DENIED, and the
                        refusal NAMES the organ to run -- both halves asserted,
                        because a denial that only says no trains avoidance.
  B. UNAFFECTED         ordinary non-governed searching still runs, proven by a
                        plain string search that must be allowed.
  C. THE OVER-MATCH     the failure mode the row names in its own text --
     GUARD              "over-broad matching here wedges every session". Each
                        test here is a way the guard could wedge a session, and
                        each is pinned shut.
  D. THE WIRE           stdin JSON -> exit 2 + {"decision":"block"} on stdout,
                        the same protocol the ADR-77 guard uses.

The pure decision core takes its process set as an ARGUMENT, so the predicate is
testable without a store; the store read is exercised separately against the live
repo.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO / "scripts" / "hooks" / "deny_and_point.py"


def _load():
    spec = importlib.util.spec_from_file_location("deny_and_point", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


guard = _load()


#: A process set shaped like the real one, small enough to reason about. The
#: single-word stems are the MEASURED over-match hazards on the live tree
#: (`audit`, `check`, `save`, `ship`, `cli`, `registry`, `gitenv`, `_common`) --
#: they are in the fixture precisely so the tests can prove they are NOT denied
#: when someone greps for them as ordinary text.
PROCESSES = {
    "scripts/gen_task_tree.py": "script",
    "scripts/graph_queries.py": "script",
    "scripts/audit.py": "script",
    "scripts/check.py": "script",
    "scripts/cli.py": "script",
    "scripts/registry.py": "script",
    "scripts/gitenv.py": "script",
    "scripts/_common.py": "script",
    ".claude/commands/ship.md": "command",
    ".claude/commands/save.md": "command",
    ".claude/commands/boot-session.md": "command",
    ".claude/skills/verify/SKILL.md": "skill",
}


def _bash(command: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": command}}


def _ps(command: str) -> dict:
    return {"tool_name": "PowerShell", "tool_input": {"command": command}}


def _grep_tool(pattern: str, path: str | None = None) -> dict:
    ti: dict = {"pattern": pattern}
    if path is not None:
        ti["path"] = path
    return {"tool_name": "Grep", "tool_input": ti}


def _decide(payload: dict):
    return guard.decide(payload, PROCESSES)


def _denied(payload: dict) -> bool:
    return _decide(payload)[0] == "block"


# --------------------------------------------------------------------------- #
# A. The trip-test -- the denial AND the pointer                               #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("command", [
    'grep -rn "gen_task_tree" scripts/',
    "rg gen_task_tree",
    "grep -r scripts/graph_queries.py .",
    "find . -name gen_task_tree.py",
    'Select-String -Pattern "boot-session" -Path .claude/',
])
def test_a_raw_search_over_a_governed_question_is_DENIED(command):
    """The row's trip-test: 'a RED-first trip-test sends a raw grep'."""
    assert _denied(_bash(command)), f"not denied: {command}"


def test_the_refusal_NAMES_the_organ_to_run():
    """'with exception text naming the organ to run instead'.

    The denial is the cheap half; the pointer is the row.
    """
    _decision, reason = _decide(_bash('grep -rn "gen_task_tree" scripts/'))
    assert "file_purpose_graph.py" in reason
    assert "why" in reason
    assert "scripts/gen_task_tree.py" in reason, "the pointer must name the RESOLVED path"


def test_the_refusal_names_the_TRIGGER_organ_for_a_who_triggers_it_search():
    _decision, reason = _decide(_bash("rg graph_queries"))
    assert "graph_queries.py process-list" in reason


def test_every_organ_the_pointer_names_actually_EXISTS_on_disk():
    """AX9-1's own locator was half-wrong (`graph_queries.py why` does not exist).

    A refusal naming an organ that does not exist trains distrust of the pointer,
    which is the failure this row exists to end. So the pointer's targets are
    resolved against the real tree, not asserted in prose.
    """
    for relpath in guard.POINTER_ORGANS:
        assert (_REPO / relpath).exists(), f"pointer names a missing organ: {relpath}"


def test_the_pointer_passes_the_RESOLVED_PATH_to_the_test_selector():
    """Terra pre-merge pass 2, P1. `impacted_tests.py select` with no --changed derives
    its paths from the staged diff, so it answers a different question than the one
    that was denied -- or prints "no changed paths" and answers none."""
    _decision, reason = _decide(_bash("rg gen_task_tree"))
    assert "select --changed scripts/gen_task_tree.py" in reason


def test_the_pointer_names_the_form_of_process_list_that_RETURNS_ROWS():
    """Terra pre-merge pass 2, P1. Bare `process-list` prints aggregate counts and a
    refusal; `--render` emits the roster rows with each process's trigger. A pointer at
    the form that returns no rows cannot answer 'is there already an organ for this'."""
    _decision, reason = _decide(_bash("rg gen_task_tree"))
    assert "process-list --render" in reason


def test_every_command_the_refusal_NAMES_actually_runs_and_answers():
    """The strongest form of 'the pointer is the row': the invocations are EXTRACTED from
    the refusal text and executed. A pointer that does not run is a denial with extra
    steps, and prose cannot be trusted to stay true as the organs change."""
    _decision, reason = _decide(_bash("rg gen_task_tree"))
    invocations = [line.split("->", 1)[1].strip()
                   for line in reason.splitlines() if "->" in line and "python" in line]
    assert invocations, "the refusal names no runnable invocation"
    for cmd in invocations:
        argv = cmd.replace("uv run --locked python", sys.executable, 1).split()
        proc = subprocess.run(argv, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", cwd=str(_REPO))
        assert proc.returncode == 0, f"pointer failed: {cmd}\n{proc.stderr[-800:]}"
        assert proc.stdout.strip(), f"pointer answered nothing: {cmd}"


def test_the_refusal_states_the_declared_escape():
    """A refusal with no lawful way through is how a PreToolUse rule wedges."""
    _decision, reason = _decide(_bash('grep -rn "gen_task_tree" scripts/'))
    assert "raw-needed:" in reason


# --------------------------------------------------------------------------- #
# B. Ordinary searching is UNAFFECTED                                          #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("command", [
    'grep -n "def parse" scripts/',
    'grep -rn "TODO" .',
    'rg "raise ValueError"',
    'grep -c "" BACKLOG.md',
    "find . -name '*.yaml'",
])
def test_a_plain_string_search_still_runs(command):
    """The row's second named test: 'ordinary non-governed searching is
    unaffected, proven by a test that a plain string search still runs'."""
    assert not _denied(_bash(command)), f"over-blocked: {command}"


@pytest.mark.parametrize("command", [
    "uv run --locked python -m pytest -x",
    "git log --oneline -5",
    "ls scripts/",
    "cat scripts/gen_task_tree.py",
    "python scripts/gen_task_tree.py --emit-source",
])
def test_a_command_that_is_not_a_search_is_never_judged(command):
    assert not _denied(_bash(command)), f"non-search denied: {command}"


def test_a_tool_outside_the_matcher_is_never_judged():
    assert not _denied({"tool_name": "Read",
                        "tool_input": {"file_path": "scripts/gen_task_tree.py"}})


# --------------------------------------------------------------------------- #
# C. The over-match guard -- every way this could wedge a session               #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("stem", ["audit", "check", "save", "ship", "cli",
                                  "registry", "gitenv", "_common"])
def test_a_SINGLE_WORD_process_stem_searched_as_text_is_NOT_denied(stem):
    """MEASURED hazard, not a hypothetical: 12 of the live tree's 150 process
    stems are single English-ish words. `grep "check"` is a text search and
    denying it would wedge the session that most needs to search.
    """
    assert not _denied(_bash(f'grep -rn "{stem}" scripts/')), stem


@pytest.mark.parametrize("command", [
    "grep -n TODO scripts/gen_task_tree.py",
    'grep -rn "TODO" scripts/graph_queries.py',
    "rg TODO scripts/gen_task_tree.py",
    "grep -n raise .claude/commands/boot-session.md",
    "find scripts/ -name '*.py'",
    "grep -f patterns.txt scripts/",
])
def test_searching_INSIDE_a_governed_file_for_ordinary_text_is_NOT_denied(command):
    """Terra pre-merge pass 1, P1. The PATTERN is the governed question; the PATH is
    just where you look. Collecting every non-flag operand made
    `grep -n TODO scripts/gen_task_tree.py` a governed query because its TARGET is a
    process -- denying the most ordinary content search there is. `-f` is in the set
    because its operand is a pattern FILE, not a pattern.
    """
    assert not _denied(_bash(command)), f"over-blocked: {command}"


@pytest.mark.parametrize("command", [
    "grep -rn gen_task_tree scripts/graph_queries.py",
    "grep -e gen_task_tree scripts/",
    "grep --regexp=gen_task_tree scripts/",
])
def test_the_path_vs_pattern_split_does_not_become_an_escape(command):
    """The converse of the test above: the pattern is still judged wherever it sits."""
    assert _denied(_bash(command)), f"not denied: {command}"


def test_a_HEREDOC_BODY_is_DATA_not_a_command():
    """Found by DOGFOODING, not by review: the guard denied the very commit that
    documented it. A commit message passed through `git commit -F - <<'MSG'` quotes the
    denials it is recording, and the tokenizer read that prose as more command segments.

    A heredoc body is data. This is the same class as the pass-1 path/pattern finding --
    text that sits inside a search command without being the question -- arriving from the
    one angle no review had covered, because it only shows up when you use the thing.
    """
    body = ("git commit -F - <<'MSG'\n"
            "fix(hooks): notes\n"
            "  rg gen_task_tree            -> DENIED\n"
            "  grep -rn gen_task_tree s/   -> DENIED\n"
            "MSG")
    assert not _denied(_bash(body))


@pytest.mark.parametrize("delim,opened", [
    ("'END-MSG'", "END-MSG"),
    ("EOF_1", "EOF_1"),
    ('"X.Y"', "X.Y"),
    ("__END__", "__END__"),
])
def test_a_heredoc_DELIMITER_is_a_shell_word_not_an_identifier(delim, opened):
    """Terra pre-merge pass 9, P1. A delimiter may legally carry `-`, digits or dots, and
    an identifier-shaped regex left those bodies in the command stream -- so the guard
    read the DATA as a search and blocked a valid command. An over-block, which is the
    expensive direction for this guard."""
    cmd = f"cat <<{delim}\nrg gen_task_tree\n{opened}"
    assert not _denied(_bash(cmd)), f"heredoc body judged as a command: {delim}"


def test_a_HERE_STRING_is_not_a_heredoc():
    """`<<<` has no body, so nothing may be swallowed by mistaking it for one."""
    assert _denied(_bash('rg gen_task_tree <<<"some data"'))


def test_a_real_search_AFTER_a_heredoc_is_still_judged():
    """The converse: stripping the body must not swallow the rest of the line."""
    cmd = ("cat <<'EOF'\n"
           "some data\n"
           "EOF\n"
           "rg gen_task_tree")
    assert _denied(_bash(cmd))


def test_a_marker_inside_a_heredoc_body_does_not_open_the_escape():
    cmd = ("cat <<'EOF'\n"
           "# raw-needed: not a declaration, just text\n"
           "EOF\n"
           "rg gen_task_tree")
    assert _denied(_bash(cmd))


def test_the_word_grep_inside_an_ARGUMENT_is_not_a_search():
    """A search tool must be the HEAD of a segment, not a substring anywhere."""
    assert not _denied(_bash('git commit -m "add grep support to the selector"'))
    assert not _denied(_bash("echo 'we should rg for this later'"))


@pytest.mark.parametrize("command", [
    "command grep -rn gen_task_tree scripts/",
    "env FOO=1 rg gen_task_tree",
    "LC_ALL=C grep -rn gen_task_tree scripts/",
    "& rg gen_task_tree",
    "/usr/bin/grep -rn gen_task_tree scripts/",
    "time rg gen_task_tree",
    "xargs grep gen_task_tree",
])
def test_a_WRAPPED_search_is_still_a_search(command):
    """Terra pre-merge pass 3, P1. Only argv[0] was tested against the search-head set, so
    every ordinary invocation wrapper walked straight past the guard. These are common
    shell forms, not evasions -- an env prefix or a PowerShell `&` call operator is how
    people write commands -- so treating them as not-a-search is a plain hole.
    """
    assert _denied(_bash(command)), f"wrapper bypassed the guard: {command}"


@pytest.mark.parametrize("command", [
    'rg "gen_task_tree|TODO"',
    'grep -rEn "TODO|gen_task_tree" scripts/',
    r'grep -rn "TODO\|gen_task_tree" scripts/',
    "cat BACKLOG.md|grep gen_task_tree",
])
def test_a_quoted_regex_ALTERNATION_does_not_get_past_the_split(command):
    """Terra pre-merge pass 5, P1, and it has TWO layers.

    Layer 1: the command was split on `|` BEFORE tokenizing, so a quoted alternation
    produced an unterminated segment, shlex raised, and the whole command yielded no
    candidates -- allowing the search. Fixed by tokenizing first (shlex respects quotes)
    and splitting on operator TOKENS.

    Layer 2, which the split alone does not fix: `gen_task_tree|TODO` is one token and
    resolves to no process by exact match. A pattern's alternation branches are candidates
    too, or the whole class stays open after layer 1 is closed. The last case is the
    no-space pipe, which the old string split also missed.
    """
    assert _denied(_bash(command)), f"alternation bypassed the guard: {command}"


@pytest.mark.parametrize("pattern", [
    r"\bgen_task_tree\b",
    r"\<gen_task_tree\>",
    r"gen_task_tree\.py",
    "^gen_task_tree$",
    r"\bboot-session\b",
])
def test_ordinary_REGEX_SYNTAX_around_a_governed_name_still_resolves(pattern):
    """Terra pre-merge pass 10, P1. `\\b` word boundaries and `\\.` escaped literals are
    how people actually write these searches, and the edge-strip left the `b` behind, so
    the governed name no longer matched and the search was allowed."""
    assert _denied(_bash(f"rg '{pattern}'")), f"regex form bypassed the guard: {pattern}"


@pytest.mark.parametrize("pattern", [
    "./scripts/graph_queries.py",
    r".\scripts\graph_queries.py",
    r"scripts\graph_queries.py",
])
def test_a_DOT_RELATIVE_or_WINDOWS_path_still_names_the_same_process(pattern):
    """Terra pre-merge pass 12, and it was HALF right -- measured rather than accepted.

    `./scripts/...` already resolved: the edge strip removes a leading `./`. The BACKSLASH
    forms did not, because the store keys use `/` and only the leading separator was being
    stripped -- on a Windows repo with a PowerShell matcher, that is the everyday spelling.
    """
    assert _denied(_bash(f"rg '{pattern}'")), f"path form bypassed the guard: {pattern}"


def test_an_UNQUOTED_windows_path_survives_PowerShell_tokenization():
    r"""Terra pre-merge pass 16, P1. POSIX `shlex` treats a backslash as an escape, so an
    unquoted `scripts\graph_queries.py` tokenized to `scriptsgraph_queries.py` and resolved
    to nothing -- on `PowerShell`, one of this guard's own configured surfaces. The pass-12
    separator fix only reached backslashes that SURVIVED tokenization, i.e. quoted ones.

    The lexer mode is therefore chosen by tool: POSIX for `Bash`, where a backslash really
    IS an escape, and non-POSIX for `PowerShell`, where it is a path separator.
    """
    assert _denied(_ps(r"Select-String -Pattern scripts\graph_queries.py"))
    assert _denied(_ps(r"Select-String -Pattern .\scripts\graph_queries.py"))


def test_PowerShell_tokenization_does_not_over_block():
    assert not _denied(_ps('Select-String -Pattern "def parse" -Path scripts\\'))
    assert not _denied(_ps(r"Select-String -Pattern TODO -Path scripts\graph_queries.py"))
    assert not _denied(_ps("Get-ChildItem scripts/"))


@pytest.mark.parametrize("pattern", [r"\bcheck\b", r"\bTODO\b", r"\baudit\b"])
def test_regex_normalisation_does_not_widen_the_predicate(pattern):
    """The converse: normalising escapes must not promote a word that names no process.
    Two of these are measured single-word stems, so the bound is the one that matters."""
    assert not _denied(_bash(f"rg '{pattern}'")), f"over-blocked: {pattern}"


def test_alternation_branches_do_not_become_an_over_match():
    """The converse: splitting a pattern on `|` must not manufacture a denial from
    branches that name nothing. A single-word stem stays allowed inside one, too."""
    for command in ('rg "TODO|FIXME"', 'grep -rEn "check|audit|save" scripts/'):
        assert not _denied(_bash(command)), f"over-blocked: {command}"


@pytest.mark.parametrize("command", [
    "grep -egen_task_tree scripts/",
    "rg -egen_task_tree",
])
def test_an_ATTACHED_short_pattern_flag_is_understood(command):
    """Terra pre-merge pass 8, P1. `-ePATTERN` with no space is ordinary grep/rg syntax
    and the parser read the whole token as an unknown flag."""
    assert _denied(_bash(command)), f"attached -e bypassed the guard: {command}"


def test_an_attached_short_pattern_flag_carries_the_pattern_not_the_path():
    """Same split as everywhere else: -e attaches the PATTERN, and the path stays a path."""
    assert not _denied(_bash("grep -eTODO scripts/gen_task_tree.py"))
    assert not _denied(_bash("grep --exclude-dir=scripts -rn TODO ."))


def test_the_colon_attached_PowerShell_parameter_form_is_understood():
    """Terra pre-merge pass 4, P1. `-Pattern:<value>` is standard PowerShell, and the
    parser read the whole token as an unknown flag -- so the governed search passed."""
    assert _denied(_bash("Select-String -Pattern:gen_task_tree -Path:scripts/"))
    assert _denied(_bash("sls -Pattern:boot-session"))


def test_a_colon_attached_PATH_is_still_a_path():
    """The same split, in the other direction: -Path:<governed file> is where you look."""
    assert not _denied(_bash(
        'Select-String -Pattern:"def parse" -Path:scripts/gen_task_tree.py'))


@pytest.mark.parametrize("command", [
    "sudo -u root rg gen_task_tree",
    "env -u FOO rg gen_task_tree",
    "xargs -I {} grep gen_task_tree",
    "timeout -s KILL 5 rg gen_task_tree",
    "nice -n 10 rg gen_task_tree",
    "env -i rg gen_task_tree",
])
def test_a_wrappers_OWN_OPTIONS_do_not_hide_the_search(command):
    """Terra pre-merge pass 7, P1. Stripping wrapper NAMES was not enough: a wrapper's
    value-taking option left its VALUE sitting where the command head should be
    (`sudo -u root ...` -> head reads as `root`), so the search was never found.

    The last case is the converse hazard and is why the option tables are per-wrapper
    rather than one shared set: `env -i` takes NO value, so a shared table containing
    `-i` (which xargs does take a value for) would consume `rg` itself and lose the
    denial. Over-consumption fails open, which is the safe direction but still a hole.
    """
    assert _denied(_bash(command)), f"wrapper option hid the search: {command}"


def test_stripping_wrappers_does_not_turn_a_NON_search_into_one():
    """The converse: wrapper stripping must not promote an innocent command."""
    for command in ("env FOO=1 python scripts/gen_task_tree.py",
                    "command ls scripts/",
                    "time uv run --locked python -m pytest",
                    "env"):
        assert not _denied(_bash(command)), f"over-blocked: {command}"


def test_a_search_in_a_LATER_pipeline_segment_is_still_judged():
    """The converse of the test above -- the head rule must not become an escape."""
    assert _denied(_bash("cat BACKLOG.md | grep gen_task_tree"))


def test_a_pattern_naming_no_process_is_never_denied_however_it_is_searched():
    """The predicate's load-bearing half: a plain string search is UNDENIABLE
    unless the string IS a real process. This is what makes 'unaffected' a
    property of the predicate rather than a promise."""
    for command in ('grep -rn "zzz_not_a_process" scripts/',
                    "rg not_a_real_module_name",
                    "find . -name no_such_script.py"):
        assert not _denied(_bash(command)), command


def test_an_unparseable_command_is_ALLOWED():
    """Fail-open outside a confirmed governed search: a guard malfunction must
    never block normal work. Same asymmetry as the ADR-77 guard."""
    assert not _denied(_bash('grep -rn "unterminated'))


def test_an_empty_or_missing_payload_is_ALLOWED():
    assert not _denied({"tool_name": "Bash", "tool_input": {}})
    assert not _denied({})


def test_a_declared_escape_with_a_REASON_allows_the_search():
    """The bypass is one named thing, declared -- not a --no-verify reflex."""
    assert not _denied(_bash(
        'grep -rn "gen_task_tree" scripts/  # raw-needed: renaming every call site'))


@pytest.mark.parametrize("command", [
    "echo '# raw-needed: note' | rg gen_task_tree",
    'rg gen_task_tree "# raw-needed: in an argument"',
    "rg '# raw-needed: x' && rg gen_task_tree",
])
def test_the_escape_counts_only_as_a_REAL_trailing_COMMENT(command):
    """Terra pre-merge pass 6, P1. The marker was matched anywhere in the command text,
    so quoting it -- or echoing it through a pipe -- opened the escape without anyone
    declaring anything. A declared bypass that can be asserted from inside a quoted
    string is not a declaration."""
    assert _denied(_bash(command)), f"fake escape opened the guard: {command}"


def test_a_REAL_trailing_comment_still_escapes():
    assert not _denied(_bash(
        "grep -rn gen_task_tree scripts/ # raw-needed: renaming every call site"))
    assert not _denied(_bash(
        "cat BACKLOG.md | grep gen_task_tree  #raw-needed: one-off audit"))


@pytest.mark.parametrize("command", [
    "echo note # raw-needed: documentation\nrg gen_task_tree",
    "rg gen_task_tree # raw-needed: renaming\nrg graph_queries",
])
def test_an_escape_declared_on_ONE_LINE_does_not_cover_the_NEXT(command):
    """Terra pre-merge pass 13, P1. The escape was evaluated over the whole payload, so an
    earlier unrelated `# raw-needed:` comment switched the guard off for every command
    after it. A declaration covers the command it is written on, and nothing else."""
    assert _denied(_bash(command)), f"escape leaked across lines: {command}"


def test_an_escape_covers_the_SEGMENT_it_trails_not_the_whole_line():
    """Terra pre-merge pass 14, P1 -- the logical next notch after pass 13. A shell comment
    trails the command after the LAST separator, so `rg X; echo done # raw-needed: note`
    declares an escape for `echo done` and says nothing about the `rg`."""
    assert _denied(_bash("rg gen_task_tree; echo done # raw-needed: note"))
    assert _denied(_bash("rg gen_task_tree && echo ok # raw-needed: note"))


def test_the_escape_attaches_to_the_LAST_REAL_COMMAND_on_its_line():
    """THE RULE, stated because a pre-merge pass (15) read it differently and the reading
    matters more than the code here.

    A declaration attaches to the last real command on its own line. So a trailing separator
    before the comment changes nothing -- `rg X; # raw-needed: r` is the sanctioned form with
    a stray semicolon, and it grants no power `rg X # raw-needed: r` does not already grant.
    Where a REAL command follows the separator, the declaration is about THAT command and the
    earlier search stays governed; and a declaration on a different LINE attaches to nothing.

    The alternative reading -- a declaration trailing an empty segment is void, so deny --
    was rejected: it over-blocks a good-faith declaration, and over-blocking is the expensive
    failure this row names in its own text.
    """
    assert not _denied(_bash("rg gen_task_tree; # raw-needed: reason"))   # stray separator
    assert _denied(_bash("rg gen_task_tree;"))                            # no declaration
    assert _denied(_bash("rg gen_task_tree\n# raw-needed: reason"))       # wrong line
    assert _denied(_bash("rg gen_task_tree; echo done # raw-needed: r"))  # covers `echo`


def test_an_escape_trailing_the_SEARCH_itself_still_works():
    assert not _denied(_bash("echo done; rg gen_task_tree # raw-needed: renaming"))
    assert not _denied(_bash("cat BACKLOG.md | grep gen_task_tree # raw-needed: one-off"))


def test_each_line_may_declare_its_own_escape():
    assert not _denied(_bash(
        "rg gen_task_tree  # raw-needed: renaming\n"
        "rg graph_queries  # raw-needed: same arc"))


def test_a_bare_escape_marker_with_NO_reason_does_not_escape():
    assert _denied(_bash('grep -rn "gen_task_tree" scripts/  # raw-needed:'))
    assert _denied(_bash('grep -rn "gen_task_tree" scripts/  # raw-needed'))


# --------------------------------------------------------------------------- #
# C2. The cost ordering -- the store is read only when it can matter           #
# --------------------------------------------------------------------------- #

def test_a_non_search_command_never_opens_the_store(monkeypatch):
    """A PreToolUse hook pays its cost on EVERY call. Opening the persisted
    store costs ~0.4 s, so the predicate is ordered: parse first (no I/O), read
    the store only once a search head and a candidate token are both present.
    Pinned as a property rather than left as an intention."""
    opened = []
    monkeypatch.setattr(guard, "load_processes", lambda *a, **k: opened.append(1) or {})
    guard.decide_with_store(_bash("uv run --locked python -m pytest -x"))
    guard.decide_with_store(_bash('git commit -m "mentions grep"'))
    assert opened == [], "the store was opened for a command that cannot be denied"


def test_a_governed_search_DOES_open_the_store(monkeypatch):
    opened = []
    monkeypatch.setattr(guard, "load_processes",
                        lambda *a, **k: (opened.append(1), PROCESSES)[1])
    decision, _reason = guard.decide_with_store(_bash("rg gen_task_tree"))
    assert opened == [1]
    assert decision == "block"


def test_an_unreadable_store_ALLOWS_rather_than_wedging(monkeypatch):
    """A stale lockfile, a missing store or a fresh clone must never be able to
    block every search in a session."""
    def boom(*_a, **_k):
        raise OSError("no store here")
    monkeypatch.setattr(guard, "load_processes", boom)
    assert guard.decide_with_store(_bash("rg gen_task_tree"))[0] == "allow"


# --------------------------------------------------------------------------- #
# D. The Grep TOOL, and the wire protocol                                      #
# --------------------------------------------------------------------------- #

def test_the_Grep_tool_is_judged_by_its_pattern_field():
    assert _denied(_grep_tool("gen_task_tree", "scripts/"))
    assert _denied(_grep_tool("scripts/graph_queries.py"))


def test_the_Grep_tool_with_an_ordinary_pattern_is_allowed():
    assert not _denied(_grep_tool("def parse", "scripts/"))
    assert not _denied(_grep_tool("check"))


def _run(payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(_SCRIPT)],
        input=json.dumps(payload), capture_output=True,
        text=True, encoding="utf-8", errors="replace", cwd=str(_REPO))


def test_the_wire_denies_with_exit_2_and_a_block_decision():
    # Precondition, not a weakening: the deny path needs a persisted store to judge against,
    # and the guard ALLOWS when there is none (that is the fail-open posture, asserted above).
    # pre-commit rebuilds the store on every commit, so this skips only on a tree that has
    # never committed.
    if not guard.load_processes(_REPO):
        pytest.skip("no persisted store on this tree (pre-commit rebuilds it)")
    proc = _run(_bash("rg gen_task_tree"))
    assert proc.returncode == 2
    body = json.loads(proc.stdout)
    assert body["decision"] == "block"
    assert "file_purpose_graph.py" in body["reason"]


def test_the_wire_allows_an_ordinary_search_silently():
    proc = _run(_bash('grep -n "def parse" scripts/'))
    assert proc.returncode == 0
    assert proc.stdout.strip() == ""


def test_the_wire_allows_malformed_stdin():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT)], input="not json at all",
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(_REPO))
    assert proc.returncode == 0


def test_the_guard_output_is_ASCII_so_a_cp1252_console_cannot_crash_it():
    """A Windows console is cp1252; a non-cp1252 glyph on the refusal path turns
    a clean denial into an UnicodeEncodeError, exactly where the message matters
    most. Recorded gotcha, pinned here."""
    _decision, reason = _decide(_bash("rg gen_task_tree"))
    reason.encode("cp1252")


# --------------------------------------------------------------------------- #
# E. Against the LIVE store                                                    #
# --------------------------------------------------------------------------- #

def test_the_live_store_answers_with_the_repos_real_processes():
    processes = guard.load_processes(_REPO)
    if not processes:
        pytest.skip("no persisted store on this tree (pre-commit rebuilds it)")
    assert "scripts/graph_queries.py" in processes
    assert all(v in {"script", "command", "skill"} for v in processes.values())


def _wired_command() -> str:
    settings = json.loads((_REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
    for block in settings["hooks"]["PreToolUse"]:
        for hook in block["hooks"]:
            if "deny_and_point" in hook.get("command", ""):
                return hook["command"]
    raise AssertionError("deny_and_point is not wired into .claude/settings.json PreToolUse")


def test_the_guard_is_WIRED_on_the_tools_it_judges():
    settings = json.loads((_REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
    matchers = [b["matcher"] for b in settings["hooks"]["PreToolUse"]
                if any("deny_and_point" in h.get("command", "") for h in b["hooks"])]
    assert matchers == ["Bash|PowerShell|Grep"]
    assert _SCRIPT.exists()


def test_the_WIRED_COMMAND_ITSELF_denies_and_allows_as_configured():
    """The wired command is a shell wrapper, and a wrapper that does not run is a hook that
    does not exist -- while a wrapper that ERRORS is worse, because a PreToolUse hook reads a
    non-zero exit as DENY and would refuse every matched call ([#684]).

    A pre-merge review raised, twice, that the POSIX `if [ -f ... ]` form cannot run on
    Windows. It does run here -- Claude Code executes hook commands through Git Bash, measured
    by lane-w-684 -- but an argument is not a gate. So the property is EXECUTED: the exact
    string from settings.json is run, both branches, rather than reasoned about.
    """
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("no POSIX shell on PATH to execute the wired command with")
    if not guard.load_processes(_REPO):
        pytest.skip("no persisted store on this tree (pre-commit rebuilds it)")
    command = _wired_command()
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(_REPO)}

    def run(payload):
        return subprocess.run([bash, "-c", command], input=json.dumps(payload),
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", cwd=str(_REPO), env=env)

    denied = run(_bash("rg gen_task_tree"))
    assert denied.returncode == 2, denied.stderr[-500:]
    assert "file_purpose_graph.py" in json.loads(denied.stdout)["reason"]

    allowed = run(_bash('grep -n "def parse" scripts/'))
    assert allowed.returncode == 0, allowed.stderr[-500:]


def test_the_wired_command_FAILS_OPEN_when_the_project_dir_is_unset():
    """The reason the existence test is in the COMMAND and not in the module: a garbage
    script path means the module never loads, and python's own exit 2 would then read as
    DENY on every matched call -- [#684]'s defect, which W-2' is fixing on line 21 of this
    same file."""
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("no POSIX shell on PATH to execute the wired command with")
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
    proc = subprocess.run([bash, "-c", _wired_command()],
                          input=json.dumps(_bash("rg gen_task_tree")),
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=str(_REPO), env=env)
    assert proc.returncode == 0, (
        "an unset CLAUDE_PROJECT_DIR must ALLOW, never deny every matched call")


def test_the_guard_computes_no_edges_of_its_own():
    """ADR-118 §1: no organ computes an edge set of its own. This guard READS the
    persisted FPG-1 process set and derives nothing."""
    source = _SCRIPT.read_text(encoding="utf-8")
    for forbidden in ("import file_purpose_graph", "rebuild(", "os.walk", "rglob("):
        assert forbidden not in source, f"the guard derives its own answer: {forbidden}"
