#!/usr/bin/env python
"""task_record.py — ADR-122 STEP 1: the pydantic model, the `task` library/CLI, and the
row/archive-record converter. A task is a typed record in git; every backlog view is a
projection (ADR-122 D1-D9).

LIBRARY-FIRST (O-12, common rules §3): pydantic is already a declared dependency
(`pyproject.toml`, ADR-109 §3 W2) — no new dependency for the model. The CLI is
`argparse` (stdlib), matching every other script organ in this repo (`gen_task_tree.py`,
`validate_backlog.py`); no CLI framework was evaluated because none of this repo's
existing script organs uses one and a second convention would cost more than it buys.

SCOPE — step 1 is CONTRACT + RECONCILIATION, explicitly NOT the flip (ADR-122
"Migration step 2: flip the source"). This module:
  * defines TaskRecord + its nested types, matching D1-D10 structurally;
  * defines ArchiveRecord for the OTHER step-1 corpus, `tasks/archive/*.md`
    (`scripts/archive_row_body.py`'s row-body-archival records — a different shape
    from a task row, and named separately in the ADR's step-1 exit criteria);
  * converts EITHER corpus, read-only, into these types — `convert_row` reuses
    `gen_task_tree.py`'s derivers (`derive_priority`, `derive_size`, `derive_title`,
    `derive_status`, `derive_serialize_group`, `derive_depends_on`, `derive_implements`)
    as the oracle for every field they already own, so this module cannot silently
    disagree with the source-of-truth deriver on a field both touch;
  * exposes a `task` CLI (`show`, `list --json`, `check`) over records — `new`/`set`/
    `close` are the WRITE path D9 names, and per the ADR's "Do not: flip the source of
    truth" they do not touch `tasks/`: they operate on a scratch JSON record file
    (`--record`), which is what step 1's job-tmp conversion run also produces. Wiring
    them to the live tree is step 2's job, not this module's.

WHAT THIS MODULE NEVER DOES: write into `tasks/`, delete a task file, or change
`BACKLOG.md`/`manifest.json`. Layer-2 posture (ADR-28/36) is unchanged.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, StrictStr, model_validator

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_TASKS_DIR = (_REPO_ROOT / "tasks").resolve()
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
import gen_task_tree as gtt  # noqa: E402

SCHEMA_VERSION = "1.0.0"


class TasksDirWriteRefused(Exception):
    """Raised by `_refuse_tasks_dir_write` — never caught internally, so a caller that
    forgets to check exit code still sees a loud traceback rather than a silent write."""


def _refuse_tasks_dir_write(path: Path) -> None:
    """D9's write verbs (`new`/`set`/`close`) exist for SCRATCH records only — step 1
    explicitly does not flip the source of truth (ADR-122 "Do not"), so no CLI write
    path may land inside the live `tasks/` tree, whatever `--record` names. Resolved
    against the real filesystem path (not just string-prefixed) so a `..`-relative or
    symlinked escape is still caught."""
    resolved = Path(path).resolve()
    if resolved == _TASKS_DIR or _TASKS_DIR in resolved.parents:
        raise TasksDirWriteRefused(
            f"task_record: REFUSED (nothing written) — {path} resolves inside {_TASKS_DIR}; "
            f"the task CLI's write verbs may not touch the live tasks/ tree (ADR-122 step 1 "
            f"does not flip the source of truth). Point --record at scratch/job-tmp instead.")


class _Contract(BaseModel):
    """We own this grammar — unknown keys are a spec error (mirrors
    `ecosystem/schema/desired_state.py::_Contract`, the one prior-art pydantic contract
    type in this repo)."""

    model_config = ConfigDict(frozen=True, extra="forbid")


# --- D2: acceptance is data ---------------------------------------------------------------

class VerifierKind(StrEnum):
    command = "command"
    review = "review"
    unresolved = "unresolved"


class CommandVerifier(_Contract):
    kind: Literal[VerifierKind.command] = VerifierKind.command
    argv: tuple[StrictStr, ...] = Field(min_length=1)
    cwd: StrictStr | None = None
    timeout_seconds: int | None = None
    expected_result: Literal["exit_zero", "exit_nonzero"] = "exit_zero"


class ReviewVerifier(_Contract):
    kind: Literal[VerifierKind.review] = VerifierKind.review
    rubric: StrictStr = Field(min_length=1)
    evidence_required: StrictStr = Field(min_length=1)
    reviewer_role: StrictStr = Field(min_length=1)


class UnresolvedVerifier(_Contract):
    """D2: an `unresolved` criterion cannot support a close — enforced at the record
    level (`TaskRecord._closure_needs_resolved_criteria`), not here, because a bare
    Verifier has no `closure` to check against."""

    kind: Literal[VerifierKind.unresolved] = VerifierKind.unresolved
    reason: StrictStr = Field(min_length=1)
    owner: StrictStr | None = None


Verifier = Annotated[
    CommandVerifier | ReviewVerifier | UnresolvedVerifier,
    Field(discriminator="kind"),
]


class Criterion(_Contract):
    id: StrictStr
    requirement: StrictStr
    verifier: Verifier

    @property
    def supports_close(self) -> bool:
        return not isinstance(self.verifier, UnresolvedVerifier)


# --- D3: links are data --------------------------------------------------------------------

class TaskProvenance(_Contract):
    intake: StrictStr | None = None
    adr: tuple[StrictStr, ...] = ()
    filed_by: StrictStr | None = None


class Routine(_Contract):
    consumer: StrictStr
    path: StrictStr


class KillCandidates(_Contract):
    """`{ids}` or `{none_reason}` — the body grammar's two shapes (`kill-candidates:
    none -- <reason>` vs a comma list of `#id`s), never both, never neither."""

    ids: tuple[StrictStr, ...] = ()
    none_reason: StrictStr | None = None

    @model_validator(mode="after")
    def _exactly_one_shape(self) -> KillCandidates:
        if self.ids and self.none_reason is not None:
            raise ValueError("kill_candidates: ids and none_reason are mutually exclusive")
        if not self.ids and self.none_reason is None:
            raise ValueError("kill_candidates: needs ids or none_reason")
        return self


# --- D4: lifecycle lives in the record -------------------------------------------------

class TaskStatus(StrEnum):
    open = "open"
    closed = "closed"
    retired = "retired"
    superseded = "superseded"
    deferred = "deferred"


_TERMINAL_STATUSES = frozenset({TaskStatus.closed, TaskStatus.retired, TaskStatus.superseded})


class ClosureRecord(_Contract):
    commit: StrictStr
    definition_digest: StrictStr
    results: tuple[StrictStr, ...] = ()


# --- D1 + D4 + D6 + D10: the record itself --------------------------------------------------

class TaskRecord(_Contract):
    schema_version: Literal["1.0.0"] = SCHEMA_VERSION
    id: StrictStr  # opaque "[#N]", byte-exact — never a normalized integer ([#424])
    title: StrictStr
    description: StrictStr = ""
    status: TaskStatus
    status_reason: StrictStr | None = None
    priority: StrictStr | None = None
    size: StrictStr | None = None
    theme_id: StrictStr | None = None  # D6: order is fields — "E4", not the prose heading
    story_id: StrictStr | None = None  # D6: "S11", not the prose heading
    rank: int | None = None
    criteria: tuple[Criterion, ...] = ()
    depends_on: tuple[StrictStr, ...] = ()  # raw tokens, never normalized ([#424])
    implements: tuple[StrictStr, ...] = ()
    provenance: TaskProvenance | None = None
    supersedes: StrictStr | None = None
    serialize_group: tuple[StrictStr, ...] = ()
    routine: Routine | None = None
    kill_candidates: KillCandidates | None = None
    closure: ClosureRecord | None = None
    # D10 / step-1 measurement carrier: unclassified leftover clause text (e.g. `refs`,
    # which D1-D9 names no typed field for) or, for a legacy prose Done-when, the sibling
    # kill-candidates value when it names ids rather than `none`. NOT part of D1-D9's
    # design — a step-1 exit criterion is "zero legacy_body carriers left in the
    # converted set", i.e. this field existing at all is the measured gap, not the goal.
    legacy_body: StrictStr | None = None

    @model_validator(mode="after")
    def _closure_needs_resolved_criteria(self) -> TaskRecord:
        if self.closure is not None:
            unresolved = [c.id for c in self.criteria if not c.supports_close]
            if unresolved:
                raise ValueError(
                    f"TaskRecord {self.id}: closure present but criteria "
                    f"{unresolved} are unresolved — D2: an unresolved criterion "
                    f"cannot support a close")
        return self

    @model_validator(mode="after")
    def _terminal_status_needs_reason_or_closure(self) -> TaskRecord:
        if self.status in _TERMINAL_STATUSES and self.closure is None and self.status_reason is None:
            raise ValueError(
                f"TaskRecord {self.id}: terminal status {self.status.value!r} needs "
                f"either a closure or a status_reason (ADR-107 §6.3: a retired/closed "
                f"record states why, not just that)")
        return self


# --- the OTHER step-1 corpus: tasks/archive/*.md row-body-archival records -------------

class ArchiveRecord(_Contract):
    """`scripts/archive_row_body.py`'s row-body-archival shape — narration relocated
    verbatim out of a live row body. A DIFFERENT record kind from TaskRecord (it has no
    status, no criteria — it is a citation target, not a task), named separately in
    ADR-122 step 1's exit criteria ("all 667 rows AND 86 archive records"). Step 1 does
    not build an event/clause-typed model for it (out of scope: TaskRecord's D1-D9 shape
    says nothing about archival annotations) — every archive record therefore carries
    its whole body as `legacy_body`, which is why the corpus-wide legacy_body count
    below is never zero and is reported as a named step-1 remainder, not a defect.
    """

    id: StrictStr
    row: StrictStr
    record: StrictStr
    schema_number: int
    events: int
    pointer: StrictStr
    legacy_body: StrictStr


_ARCHIVE_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n\n(.*)$", re.DOTALL)


def convert_archive_record(text: str) -> ArchiveRecord:
    """One `tasks/archive/<id>.md` file's text -> ArchiveRecord. Read-only; no file I/O
    here (the CLI/corpus runner does that), matching `desired_state.py`'s model-only
    posture."""
    m = _ARCHIVE_FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("convert_archive_record: no '---' frontmatter fence found")
    front = yaml.safe_load(m.group(1))
    body = m.group(2)
    return ArchiveRecord(
        id=str(front["id"]),
        row=str(front["row"]),
        record=str(front["record"]),
        schema_number=int(front["schema"]),
        events=int(front["events"]),
        pointer=str(front["pointer"]),
        legacy_body=body,
    )


# --- the live-row converter (D1-D9 over gen_task_tree.py's own body grammar) -----------

#: End-anchored the same way gen_task_tree's own clause regexes are: capture up to the
#: next ` · <word>` clause boundary or end of line. Body text does not itself contain
#: " · " outside a clause boundary in the observed corpus (validate_backlog's grammar
#: assumes the same thing for `Done when:`/`refs`/`depends-on`).
_DONE_WHEN_RE = re.compile(r"·\s*Done when:\s*(.+?)(?=\s+·\s+\S|$)", re.IGNORECASE | re.DOTALL)
_REFS_RE = re.compile(r"·\s*refs\s+(.+?)(?=\s+·\s+\S|$)", re.IGNORECASE | re.DOTALL)
_KILL_CANDIDATES_RE = re.compile(r"·\s*kill-candidates:\s*(.+?)(?=\s+·\s+\S|$)",
                                  re.IGNORECASE | re.DOTALL)
#: A trailing backtick-fenced shell command after a `--` separator is this repo's own
#: convention for an executable Done-when (see tasks/1076-*.md et al, this lane); when
#: present the criterion gets a real CommandVerifier instead of `unresolved`.
_TRAILING_COMMAND_RE = re.compile(r"--\s*`([^`]+)`\s*$")
_KILL_IDS_RE = re.compile(r"#\d+")
_THEME_ID_RE = re.compile(r"\[([A-Za-z]\d+)\]")
#: Generic clause splitter — same " · " boundary every clause regex above already
#: assumes. `parts[0]` is the leading band+title+narrative segment, never a clause.
_CLAUSE_SPLIT_RE = re.compile(r"\s·\s")
#: Clause prefixes already captured into a typed field or `criteria` above (codex
#: terra HIGH, this lane: a clause this repo's body grammar carries but D1-D9 names
#: no field for — e.g. `routine:`, `supersedes:`, `phase:`, `Source:` — must not be
#: silently dropped; it belongs in `legacy_body`, which is exactly what falling
#: through this allowlist produces).
_ALREADY_CAPTURED_PREFIXES = (
    "done when:", "refs", "kill-candidates:", "implements:", "depends-on:",
    "serialize-group:", "defer",
)


def _uncaptured_clauses(raw: str) -> list[str]:
    parts = [p.strip() for p in _CLAUSE_SPLIT_RE.split(raw)[1:]]
    return [p for p in parts if p and not p.lower().startswith(_ALREADY_CAPTURED_PREFIXES)]


def _extract_clause(pattern: re.Pattern[str], raw: str) -> str | None:
    m = pattern.search(raw)
    return m.group(1).strip() if m else None


def _split_command(command_text: str) -> tuple[str, ...] | None:
    """Best-effort argv split of a trailing backtick command. `shlex.split` on a
    compound shell expression (`&&`, `|`) does not model the whole pipeline — that is
    an accepted step-1 limit; the ORIGINAL text is still preserved verbatim as the
    criterion's `requirement`, so nothing is lost, only the parsed `argv` is partial."""
    try:
        parts = shlex.split(command_text)
    except ValueError:
        return None
    return tuple(parts) if parts else None


def _build_criterion(done_when_text: str) -> Criterion:
    cmd_match = _TRAILING_COMMAND_RE.search(done_when_text)
    if cmd_match:
        argv = _split_command(cmd_match.group(1))
        if argv:
            return Criterion(id="c1", requirement=done_when_text,
                              verifier=CommandVerifier(argv=argv))
    return Criterion(
        id="c1", requirement=done_when_text,
        verifier=UnresolvedVerifier(
            reason="legacy prose criterion — not yet classified as command/review "
                   "(ADR-122 operator question 2)"))


def convert_row(task_id: int, raw: str, *, theme: str | None, story: str | None,
                 frontmatter_status: str | None) -> TaskRecord:
    """One BACKLOG-grammar row body (`raw`, the exact `- [#id] ...` line) -> TaskRecord.

    `frontmatter_status` is the file's already-derived terminal status (`closed`,
    `retired`, `superseded`) when the caller has one — `gen_task_tree.derive_status`
    can only ever return `open`/`deferred` (it has no body grammar for a terminal
    status; see that function's own docstring), so a terminal status must come from
    the file's frontmatter, exactly as `gen_task_tree.emit_task_file_text`'s
    `status_override` parameter already documents.
    """
    title = gtt.derive_title(raw)
    priority = gtt.derive_priority(raw)
    size = gtt.derive_size(raw)
    serialize_group = gtt.derive_serialize_group(raw)
    depends_on_raw = gtt.derive_depends_on(raw)
    implements_raw = gtt.derive_implements(raw)

    if frontmatter_status is not None:
        status = TaskStatus(frontmatter_status)
    else:
        status = TaskStatus(gtt.derive_status(raw))

    done_when_text = _extract_clause(_DONE_WHEN_RE, raw)
    criteria: tuple[Criterion, ...] = ()
    if done_when_text:
        criteria = (_build_criterion(done_when_text),)

    refs_text = _extract_clause(_REFS_RE, raw)
    kc_text = _extract_clause(_KILL_CANDIDATES_RE, raw)
    kill_candidates: KillCandidates | None = None
    leftover_parts: list[str] = []
    if refs_text:
        leftover_parts.append(f"refs {refs_text}")
    if kc_text:
        if kc_text.lower().startswith("none"):
            reason = kc_text.split("--", 1)[1].strip() if "--" in kc_text else kc_text
            kill_candidates = KillCandidates(none_reason=reason or "no reason given")
        else:
            ids = tuple(_KILL_IDS_RE.findall(kc_text))
            if ids:
                kill_candidates = KillCandidates(ids=ids)
            else:
                leftover_parts.append(f"kill-candidates: {kc_text}")
    leftover_parts.extend(_uncaptured_clauses(raw))

    theme_id = None
    story_id = None
    if theme:
        m = _THEME_ID_RE.search(theme)
        theme_id = m.group(1) if m else theme
    if story:
        m = _THEME_ID_RE.search(story)
        story_id = m.group(1) if m else story

    status_reason = None
    if status in _TERMINAL_STATUSES:
        status_reason = "converted from a pre-step-1 body carrying a terminal frontmatter status"

    return TaskRecord(
        id=f"[#{task_id}]",
        title=title,
        description=title,
        status=status,
        status_reason=status_reason,
        priority=priority,
        size=size,
        theme_id=theme_id,
        story_id=story_id,
        criteria=criteria,
        depends_on=(depends_on_raw,) if depends_on_raw else (),
        implements=tuple(t.strip() for t in implements_raw.split(",")) if implements_raw else (),
        serialize_group=(serialize_group,) if serialize_group else (),
        kill_candidates=kill_candidates,
        legacy_body="; ".join(leftover_parts) if leftover_parts else None,
    )


# --- CLI (D9): show / list --json / check, over a scratch record — never the live tree -

def _cmd_show(args: argparse.Namespace) -> int:
    raw = Path(args.body_file).read_text(encoding="utf-8")
    rec = convert_row(int(args.id), raw, theme=args.theme, story=args.story,
                       frontmatter_status=args.frontmatter_status)
    print(rec.model_dump_json(indent=2))
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    try:
        data = json.loads(Path(args.record).read_text(encoding="utf-8"))
        TaskRecord.model_validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"task_record: check FAIL — {exc}", file=sys.stderr)
        return 1
    print("task_record: check ok")
    return 0


def _cmd_new(args: argparse.Namespace) -> int:
    """D9 `new` — writes a fresh scratch TaskRecord JSON at `--record`. NEVER `tasks/`:
    `_refuse_tasks_dir_write` refuses before anything is written, whatever path the
    caller names (a step-1 boundary, not a convention — ADR-122 "Do not: flip the
    source of truth")."""
    _refuse_tasks_dir_write(Path(args.record))
    rec = TaskRecord(id=args.id, title=args.title, status=TaskStatus(args.status),
                      kill_candidates=KillCandidates(none_reason=args.kill_candidates_none))
    out = Path(args.record)
    out.write_text(rec.model_dump_json(indent=2), encoding="utf-8")
    print(f"task_record: wrote {out}")
    return 0


def _cmd_set(args: argparse.Namespace) -> int:
    """D9 `set` — merges `--field key=value` pairs (JSON-valued) into an existing
    scratch record and re-validates. Refuses (exit 1, nothing written) on a bad merge
    or a `tasks/`-resolving path, matching every other write path in this repo's
    script organs (plan-then-write, refuse-before-write)."""
    _refuse_tasks_dir_write(Path(args.record))
    path = Path(args.record)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        for pair in args.field:
            key, _, value = pair.partition("=")
            data[key] = json.loads(value)
        rec = TaskRecord.model_validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"task_record: set REFUSED (nothing written) — {exc}", file=sys.stderr)
        return 1
    path.write_text(rec.model_dump_json(indent=2), encoding="utf-8")
    print(f"task_record: updated {path}")
    return 0


def _cmd_close(args: argparse.Namespace) -> int:
    """D9 `close` — sets status=closed with a ClosureRecord, refused (D2/D4) when any
    criterion is still unresolved. This is the CLI's own enforcement of the same
    invariant `TaskRecord._closure_needs_resolved_criteria` holds structurally.

    HONEST LIMIT (codex terra review, this lane): this verb records the closure's
    commit/digest citation — it does NOT itself execute a CommandVerifier or collect
    ReviewVerifier evidence, so a criterion whose command would actually fail can
    still be cited as closed. Step 1 builds the record shape and the structural
    refusal (an *unresolved* criterion cannot close, which is enforced); wiring a real
    command-execution/evidence-collection gate in front of `close` is step 2's job
    (the closure sweep, D4) — recorded here rather than silently assumed done.
    """
    _refuse_tasks_dir_write(Path(args.record))
    path = Path(args.record)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        data["status"] = "closed"
        data["closure"] = {"commit": args.commit, "definition_digest": args.definition_digest}
        rec = TaskRecord.model_validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"task_record: close REFUSED (nothing written) — {exc}", file=sys.stderr)
        return 1
    path.write_text(rec.model_dump_json(indent=2), encoding="utf-8")
    print(f"task_record: closed {path}")
    return 0


def _cmd_list(args: argparse.Namespace) -> int:
    try:
        records = [json.loads(Path(p).read_text(encoding="utf-8")) for p in args.record]
    except (OSError, json.JSONDecodeError) as exc:
        print(f"task_record: list FAIL — {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(records, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="task_record", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    show = sub.add_parser("show", help="convert one row body to a TaskRecord and print JSON")
    show.add_argument("--body-file", required=True)
    show.add_argument("--id", required=True)
    show.add_argument("--theme", default=None)
    show.add_argument("--story", default=None)
    show.add_argument("--frontmatter-status", default=None)
    show.set_defaults(func=_cmd_show)

    new = sub.add_parser("new", help="write a fresh scratch TaskRecord JSON (never tasks/)")
    new.add_argument("--record", required=True)
    new.add_argument("--id", required=True)
    new.add_argument("--title", required=True)
    new.add_argument("--status", default="open")
    new.add_argument("--kill-candidates-none", dest="kill_candidates_none", required=True)
    new.set_defaults(func=_cmd_new)

    set_ = sub.add_parser("set", help="merge --field key=value (JSON-valued) into a scratch record")
    set_.add_argument("--record", required=True)
    set_.add_argument("--field", action="append", default=[])
    set_.set_defaults(func=_cmd_set)

    close = sub.add_parser("close", help="close a scratch record (refused if any criterion is unresolved)")
    close.add_argument("--record", required=True)
    close.add_argument("--commit", required=True)
    close.add_argument("--definition-digest", dest="definition_digest", required=True)
    close.set_defaults(func=_cmd_close)

    check = sub.add_parser("check", help="validate a scratch record JSON file against TaskRecord")
    check.add_argument("--record", required=True)
    check.set_defaults(func=_cmd_check)

    lst = sub.add_parser("list", help="print a list of scratch record JSON files as one array")
    lst.add_argument("record", nargs="+")
    lst.add_argument("--json", action="store_true")
    lst.set_defaults(func=_cmd_list)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except TasksDirWriteRefused as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"task_record: {args.cmd} FAIL — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
