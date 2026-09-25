#!/usr/bin/env python
"""validate_hermetization.py -- ADR-101 section 3 refusal gate (#306).

A `language: system` local pre-commit hook, HUB-ONLY, **prospective-only**: it inspects
only ADDED paths (`git diff --cached --diff-filter=A`), so every existing file is
grandfathered and never checked (ADR-101 section 6 -- no retroactive rename over the
~130 subject-before-class + 4 class-less legacy files the date-index already
disambiguates). Two rules, both BLOCK (exit 1) on violation:

  Rule A (top-level seal, ADR-101 section 1/3): an added path that introduces
    (1) an unsanctioned Tier-1 top-level directory,
    (2) an unsanctioned Tier-1 top-level FILE (outside the sanctioned classes), or
    (3) a new Tier-2 `docs/<genre>/` folder
  -> BLOCK. The tree is hermetic: growing its top level is a deliberate, surfaced act
  (an ADR-101 amendment), never a drive-by folder -- directly fixing the #131 root cause.

  Rule C (home allowlist, operator ruling A of 2026-08-11; register
    `protocols/STANDING_RULINGS.md` K-1): an added path INSIDE a sanctioned Tier-1
    directory whose immediate home directory is not on the allowlist below
  -> BLOCK, with the message "new path outside allowlisted homes -- operator approval
  required". Rule A seals the TOP level and the `docs/<genre>/` level and stops there,
  which is exactly how `docs/ORGAN-INDEX.md` was born: a file loose at the `docs/` root
  introduces no new top-level entry and no new genre folder, so Rule A was silent by its
  own literal spec (the test asserting that silence is still in the suite, now paired with
  a Rule C assertion). Rule C is the leg that reads the rest of the path.

  Rule B (audit grammar, ADR-101 section 2 + ratification R3/R4): an added
  `docs/audits/*.md` whose name fails `<YYYY-MM-DD>-<class>[-<slug>]` with
    * <class> whole-token LONGEST-MATCH against the CLOSED 11-class enum (never
      split-on-first-hyphen -- the multi-word tokens require it, S3-3), and
    * the R4 casing rule (all-lowercase kebab-case everywhere; no UPPERCASE, no
      _underscore_, no CamelCase; sole carve-out: a literal `.` in the slug for a
      meaningful repo/version token like `.dev-knowledge` / `v3.4`, S3-1)
  -> BLOCK. This is the rule that fixes the corp-monorepo UPPERCASE `_AUDIT_`/`_BRIEF_`
  divergence the census found (R4).

**Name-SHAPE only, never date-accuracy** (ADR-101 section 3 / S3-4): the filename date is
validated as a SHAPE (\\d{4}-\\d{2}-\\d{2}) only -- `2026-13-99` passes the shape gate;
a misdated-content detector is a different tool that must diff the content-header date,
never `git log`.

**THE RULES ARE DATA** (operator amendment D5, 2026-09-06). Every set the three rules
consult -- sanctioned dirs, sanctioned root files and their globs, genres, the audit-class
enum, the naming regexes and the home patterns -- is loaded from
`ecosystem/fleet-shape-spec.yaml`. Before that ruling they were module literals derived
"FROM THE LIVE TAXONOMY" of THIS repo, which made the hub's own tree the fleet's spec by
default; the first consumer measured against it produced 78 out-of-pattern items with none
of them junk. The module names are unchanged, so this is a change of AUTHORITY, not of API.

**EACH RULE HAS A FLEET HALF AND A REPO-LOCAL HALF** (batch V, V-3; measured in
`docs/audits/2026-09-09-technical-seal-rule-attribution.md`). Making the rules DATA fixed
their authority but not their SCOPE: `rule_b_violation` and `rule_c_violation` were pure
functions of a path string, carried no repo identity, and therefore applied the hub's own
audit-class enum and the hub's own home tuple to every repository they were pointed at.
Run over the nine ratified fleet members that produced 308 of the fleet's 336 waivers -- a
seal measuring difference-from-the-hub's-tree rather than out-of-shape. The split each rule
now carries is the spec's own, not a new judgement:

    Rule B   FLEET      the YYYY-MM-DD- date shape and the R4 casing rule
             REPO-LOCAL the audit class enum -- the spec marks it
                        `audit_class_enum_scope: repo-local` and nothing read that marker
    Rule C   FLEET      the docs/ genre-tree rule -- `docs` is not a home, by design
             REPO-LOCAL the home tuple, which enumerates the hub's own subdirectories

A repository declares its repo-local halves in its OWN `.methodology.yaml` under
`shape_profile:` (`RepoProfile` / `profile_for_repo`), which is the register ADR-101
already sanctions at every root and two readers already parse -- no second convention. A
repo that declares nothing is policed by the fleet halves and by neither repo-local half.
**The hub's behaviour does not move:** every rule function defaults to `HUB_PROFILE`, so
every existing caller and this module's own gate keep their verdicts byte for byte.

Consumer carrier (floor/plugin) is the P6 rollout -- this gate is HUB-ONLY until then,
mirroring `roster-freshness`/`claude-rosters-freshness`/`audit-index-freshness`. The spec
being a data file rather than a literal is what makes that rollout carriable at all.
`seal_repo()` and the `report` sub-command are REPORT mode: they read one repository with
`git ls-files` and write nothing in it, which is the mode both fleet seal reports built by
hand as a throwaway harness because the module offered none.

Read-only (Layer-2, ADR-28/36): reads the staged name-status and the spec; writes NOTHING.
Fail-OPEN but LOUD on any git error -- a convention/hygiene gate must not brick every commit
on a near-impossible git failure. The spec itself is the ONE deliberate exception and goes
the other way: an absent or malformed spec raises `ShapeSpecError` at import, because a git
failure is an environment accident while a missing spec means the gate has no rules at all
(see `ShapeSpecError`). Bypass parity with peer hooks: `--no-verify`.
"""

from __future__ import annotations

import dataclasses
import fnmatch
import logging
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

import click
import yaml

logger = logging.getLogger(__name__)

# CLOUD-4 v2 (R2 §1.5 GO-b) — the canonical living-doc names come from the one registry.
try:
    from scripts import canonical_docs as _cdocs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoint
    import canonical_docs as _cdocs


# --- the SPEC: this gate's rules are DATA, not this module's literals ------------------
# Operator amendment D5 (2026-09-06, DECLARE-SITTING): "sanctioned dir set = fleet grammar,
# not the hub's tree snapshot; homes for `src/ eval/ models/`". Until that ruling the four
# sets below were module literals whose own docstrings said they were "DERIVED FROM THE LIVE
# TAXONOMY" of THIS repo -- so the hub's tree was the spec, and the first consumer measured
# against it produced 78 out-of-pattern items with zero of them junk (intake
# `docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md`). The values now come
# from `ecosystem/fleet-shape-spec.yaml`; the NAMES are unchanged and still module-level, so
# `scripts/batch_manifest.py`, `tests/test_canonical_docs.py` and every other importer keep
# working untouched.

SHAPE_SPEC_REL = "ecosystem/fleet-shape-spec.yaml"
DEFAULT_SHAPE_SPEC_PATH = Path(__file__).resolve().parent.parent / SHAPE_SPEC_REL


class ShapeSpecError(RuntimeError):
    """The shape spec is absent, unparseable, or not the declared `clauses:` shape.

    FAIL-CLOSED, and deliberately at odds with this module's git posture two paragraphs
    down. A git failure is an accident of the environment and the gate steps aside for it;
    a missing or malformed spec means the gate HAS NO RULES, and a tree seal that silently
    admits everything is worse than one that refuses to start. It also cannot happen by
    accident: the spec is a tracked file beside this module, so its absence is a repo
    integrity failure, not a routine condition.
    """


def load_shape_spec(path: Optional[Path] = None) -> dict[str, Any]:
    """Parse the fleet shape spec and return its `clauses:` mapping.

    Structural validation only, and on purpose: every clause below is consumed by a named
    derivation in this module, so a missing key surfaces as a `ShapeSpecError` naming the
    clause rather than as a `KeyError` five frames deeper. Library-first check: PyYAML is
    already a declared dependency read by `scripts/provider_registry.py` for exactly this
    job, so no parser is hand-rolled here.
    """
    p = Path(path) if path is not None else DEFAULT_SHAPE_SPEC_PATH
    if not p.exists():
        raise ShapeSpecError(f"fleet shape spec absent: {p}")
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ShapeSpecError(f"fleet shape spec unparseable ({p}): {exc}") from exc
    if not isinstance(data, dict):
        raise ShapeSpecError(f"fleet shape spec is not a YAML mapping: {p}")
    clauses = data.get("clauses")
    if not isinstance(clauses, dict):
        raise ShapeSpecError(f"fleet shape spec missing `clauses:` mapping: {p}")
    for name in ("root_allowlist", "genre_folders", "home_grammar", "naming_grammar"):
        if not isinstance(clauses.get(name), dict):
            raise ShapeSpecError(
                f"fleet shape spec missing the `{name}:` clause this gate reads: {p}")
    return clauses


def _clause_list(clauses: dict[str, Any], clause: str, key: str) -> list[str]:
    """One clause's list-of-strings payload, refused loudly if it is anything else."""
    value = clauses[clause].get(key)
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise ShapeSpecError(
            f"fleet shape spec clause `{clause}.{key}` is not a list of strings")
    return value


def _clause_str(clauses: dict[str, Any], clause: str, key: str) -> str:
    """One clause's string payload, refused loudly if it is anything else."""
    value = clauses[clause].get(key)
    if not isinstance(value, str):
        raise ShapeSpecError(f"fleet shape spec clause `{clause}.{key}` is not a string")
    return value


# One (accepts, rejects) sentinel pair per spec-supplied regex. THESE LIVE IN CODE, NOT IN
# THE SPEC, and that is the whole mechanism: a sentinel the spec supplied could be doctored
# to agree with a broken pattern, which would prove nothing.
#
# WHY THIS EXISTS (terra HIGH, 2026-09-07 adversarial round on this change): moving the
# naming grammar into YAML made a class of failure possible that a literal could not have.
# A pattern that is a valid regex but the WRONG regex -- `'^'` is the cheap example -- still
# compiles, so `_clause_str` is satisfied, and every casing/slug refusal silently becomes a
# pass. A tree seal that stops refusing is indistinguishable from a clean tree, so this
# failure would be invisible exactly where it matters. The proof below re-derives, at every
# load, that each pattern still refuses something it is supposed to refuse.
#
# HONEST LIMIT, stated rather than implied: this catches the SILENT-PASS class. It is not
# ReDoS protection -- a deliberately catastrophic pattern would stall here rather than at
# the call site, which moves the symptom without removing it. That threat needs commit
# access to the spec, and an actor with that could edit this module just as easily; the
# defence for it is review, not a regex analyser this gate cannot honestly claim to be.
_REGEX_SENTINELS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # key: (must MATCH, must NOT match)
    "filename_charset": (
        ("2026-09-07-technical-a-slug.md", "v3.4-notes.md"),
        ("2026-09-07-Technical.md", "2026_09_07-technical.md", "a b.md", "X.MD"),
    ),
    "slug": (
        ("a", "a-b-c", "v3.4-notes"),
        ("", "-lead", "trail-", "double--hyphen"),
    ),
    "date_prefix": (
        ("2026-09-07-technical.md",),
        ("technical-2026-09-07.md", "20260907-technical.md", "-2026-09-07-x.md"),
    ),
}


def _compile_checked(clauses: dict[str, Any], key: str) -> re.Pattern[str]:
    """Compile a spec-supplied regex and PROVE it still discriminates before returning it."""
    pattern = _clause_str(clauses, "naming_grammar", key)
    try:
        compiled = re.compile(pattern)
    except re.error as exc:
        raise ShapeSpecError(
            f"fleet shape spec `naming_grammar.{key}` is not a valid regex: {exc}") from exc
    accepts, rejects = _REGEX_SENTINELS[key]
    for sample in accepts:
        if not compiled.match(sample):
            raise ShapeSpecError(
                f"fleet shape spec `naming_grammar.{key}` refuses {sample!r}, which the "
                f"grammar admits -- the pattern is valid but wrong, and would refuse "
                f"conformant names")
    for sample in rejects:
        if compiled.match(sample):
            raise ShapeSpecError(
                f"fleet shape spec `naming_grammar.{key}` accepts {sample!r}, which the "
                f"grammar refuses -- the pattern is valid but wrong, and would let every "
                f"off-grammar name through as a silent pass")
    return compiled


SHAPE_SPEC = load_shape_spec()

# --- ADR-101 section 1 sanctioned sets -- DERIVED FROM THE SPEC, not from this tree ---
#
# CLOSED sets still: what changed is the AUTHORITY. Each name below is now the hub's
# instance of a clause in `ecosystem/fleet-shape-spec.yaml`, and growing one is an edit to
# that file (surfaced, reviewed, and carriable to a consumer) rather than an edit here.
# The per-member ADR-101 amendment provenance -- `.github` [#501], `.devcontainer` [#554],
# `tasks` [#433], `AGENTS.md` ADR-115, `README.md` ADR-114, and the 2026-08-26 revocation
# of `prompts/` -- travelled WITH the members into the spec's own comments. It was
# relocated rather than copied: a rationale kept in two files drifts, and the reader who
# finds one of those entries in git history now finds its reason beside the entry.

# Tier-1 -- sanctioned top-level directories (spec clause `root_allowlist.directories`).
SANCTIONED_TIER1_DIRS: frozenset[str] = frozenset(
    _clause_list(SHAPE_SPEC, "root_allowlist", "directories"))

# Tier-1 -- sanctioned top-level FILES (spec clause `root_allowlist.files`), UNIONED with
# the canonical living-doc names from the one registry. The join stays in code rather than
# moving into the spec so that no roster is restated in a second file: CLOUD-4 v2 (R2 §1.5
# GO-b) made ADR-101 §1's file enum and the ADR-38 canonical set provably the same strings,
# and listing them in YAML would undo exactly that.
SANCTIONED_TIER1_FILES: frozenset[str] = frozenset({
    *_cdocs.CANONICAL_MANDATORY,
    *_clause_list(SHAPE_SPEC, "root_allowlist", "files"),
})

# Tier-1 -- sanctioned top-level file GLOBS (spec clause `root_allowlist.file_globs`),
# fnmatch against the bare filename. NEW with the spec, and it closes a measured leak
# rather than adding a capability: the literal `.dev-knowledge.code-workspace` used to sit
# in the frozenset above, so the hub was refusing a consumer's own
# `.corp-monorepo.code-workspace` -- the fleet rule is a per-repo filename and the seal was
# carrying one repo's copy of it. Second of the four leak classes the corp-monorepo report
# measured.
SANCTIONED_TIER1_FILE_GLOBS: tuple[str, ...] = tuple(
    _clause_list(SHAPE_SPEC, "root_allowlist", "file_globs"))

# Tier-2 -- sanctioned docs/<genre>/ folders (spec clause `genre_folders.genres`).
SANCTIONED_GENRES: frozenset[str] = frozenset(
    _clause_list(SHAPE_SPEC, "genre_folders", "genres"))

# --- ADR-101 section 2 + R3: the CLOSED audit-class enum (spec `naming_grammar`) -------
# Whole-token LONGEST-MATCH (never split-on-first-hyphen). The spec carries this enum with
# an explicit `audit_class_enum_scope: repo-local` marker: it was adopted from "what three
# repos already write", which is hub-adjacent practice rather than a fleet ruling, and it
# over-blocked 28 correctly-named corp artifacts. Whether it becomes fleet vocabulary is an
# open question in the intake, recorded there rather than decided here.
AUDIT_CLASS_ENUM: frozenset[str] = frozenset(
    _clause_list(SHAPE_SPEC, "naming_grammar", "audit_class_enum"))

# Longest-match order: try the longest tokens first so `ecosystem-audit` wins over a
# hypothetical `ecosystem` split, and `conformance-nightly-digest` is matched whole.
_ENUM_BY_LEN = tuple(sorted(AUDIT_CLASS_ENUM, key=len, reverse=True))

# --- ADR-101 section 2 naming grammar -- compiled from the spec ------------------------
# SHAPE only, never date-accuracy (S3-4): `2026-13-99` passes. A misdated-content detector
# diffs the content header and is a different tool.
_DATE_SHAPE = _compile_checked(SHAPE_SPEC, "date_prefix")
_DATE_PREFIX_LEN = len("YYYY-MM-DD-")                       # 11 chars incl. trailing hyphen
# R4 casing: all-lowercase kebab-case + digits; `.` carve-out (repo/version tokens). Applied
# to the FULL filename (incl. the `.md` extension) so an uppercase `.MD` is caught too
# (codex-review 2026-07-11).
_LOWER_KEBAB_DOT = _compile_checked(SHAPE_SPEC, "filename_charset")
# A well-formed slug after the class: 1+ kebab segments of [a-z0-9.] joined by SINGLE
# hyphens -- rejects empty / leading- / trailing- / double-hyphen slugs (codex-review
# 2026-07-11). The `.` repo/version carve-out rides inside a segment.
_SLUG_RE = _compile_checked(SHAPE_SPEC, "slug")


# --- Rule C: the HOME allowlist (spec clause `home_grammar.patterns`) -----------------
# WAS "DERIVED FROM THE LIVE TAXONOMY" of this repo -- which is precisely the substitution
# operator amendment D5 ended. The patterns are now the fleet grammar, and the hub is one
# instance of it: `src/**`, `eval/**` and `models/**` are admitted here and exist in no
# directory of this repo. `test_rule_c_admits_every_tracked_path_in_the_live_repo` still
# asserts the other direction -- every tracked path the hub actually has is admitted -- so
# the spec cannot silently stop describing the tree it governs.
#
# Pattern grammar, deliberately three tokens wide so the set stays readable:
#   `a/b`   -- that literal home, exactly
#   `a/*`   -- any single immediate child of `a` is a home
#   `a/**`  -- any home at one-or-more levels below `a` (bundle / fixture / source trees)
#
# HONEST LIMIT, stated rather than left to be discovered: Rule C polices the HOME of an
# added file, and `**` homes admit arbitrary depth below them. A new sub-directory inside
# an already-open home (a new handoff bundle, a new test fixture tree, a package inside a
# source tree) is admitted by design -- those are the shapes a repo creates routinely and
# gating them would make the organ a nuisance rather than a seal. What it catches is a file
# whose home is a place the grammar has no convention for, which is the class
# `docs/ORGAN-INDEX.md` belonged to.
_HOME_PATTERNS: tuple[str, ...] = tuple(
    _clause_list(SHAPE_SPEC, "home_grammar", "patterns"))


# --- the REPO PROFILE: the seam the two hub-local rules were missing -------------------
# The spec ended the substitution of the hub's TREE for the fleet's grammar. This ends the
# substitution of the hub's VOCABULARY for the fleet's: which class tokens a repo's dated
# artifacts use, and which homes its sanctioned directories are organized into, are facts
# about that repo. A rule that reads them off the hub cannot measure a consumer's shape.
#
# Two profiles are constants because two cases are not declarations: `HUB_PROFILE` is the
# spec's own instance (the repo that CARRIES the spec is described by it), and
# `FLEET_PROFILE` is a repo that has declared nothing and is therefore policed by the
# fleet halves alone.

SHAPE_PROFILE_REL = ".methodology.yaml"
SHAPE_PROFILE_KEY = "shape_profile"


@dataclasses.dataclass(frozen=True)
class RepoProfile:
    """One repository's own vocabulary for the repo-local half of Rules B and C.

    `None` is the DECLARED ABSENCE of a vocabulary, never an empty one: an undeclared
    class enum switches the class leg off, while `frozenset()` would refuse every audit
    filename in the repo. The two readings differ by 194 items fleet-wide.
    """

    name: str
    audit_class_enum: Optional[frozenset[str]] = None
    home_patterns: Optional[tuple[str, ...]] = None


HUB_PROFILE = RepoProfile(
    name=".dev-knowledge",
    audit_class_enum=AUDIT_CLASS_ENUM,
    home_patterns=_HOME_PATTERNS,
)

FLEET_PROFILE = RepoProfile(name="<undeclared>")


@lru_cache(maxsize=None)
def _class_by_len(enum: frozenset[str]) -> tuple[str, ...]:
    """Longest-match order for one profile's enum -- the module-level `_ENUM_BY_LEN` rule,
    applied to whichever vocabulary the repo under test actually declares."""
    return tuple(sorted(enum, key=len, reverse=True))


def _declared_list(block: dict[str, Any], key: str, where: Path) -> Optional[list[str]]:
    """One optional list-of-strings key, or a refusal naming the file that carries it."""
    value = block.get(key)
    if value is None:
        return None
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise ShapeSpecError(
            f"`{SHAPE_PROFILE_KEY}.{key}` in {where} is not a list of strings -- a "
            f"declaration the reader cannot parse leaves the rule with no vocabulary, "
            f"and a seal that silently admits everything is worse than one that stops")
    return value


def profile_for_repo(repo_root: Any, name: Optional[str] = None) -> RepoProfile:
    """Resolve one repository's profile from its OWN `.methodology.yaml`.

    Three outcomes, in order. A repo that declares a `shape_profile:` block is policed by
    what it declares. A repo that carries the shape spec ITSELF is the spec's own instance
    and is policed by it -- which is how the hub stays governed without restating the enum
    in a second file (the convention this repo states as "never restate a roster"). Anything
    else is `FLEET_PROFILE`: the fleet halves, and neither repo-local half.

    FAIL-CLOSED on a malformed declaration, matching `ShapeSpecError`'s posture and for the
    same reason. An ABSENT declaration is a normal state and is not an error.
    """
    root = Path(repo_root)
    label = name or root.name
    declaration = root / SHAPE_PROFILE_REL
    block: Optional[dict[str, Any]] = None
    if declaration.exists():
        try:
            data = yaml.safe_load(declaration.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise ShapeSpecError(f"{declaration} is unparseable: {exc}") from exc
        if isinstance(data, dict):
            raw = data.get(SHAPE_PROFILE_KEY)
            if raw is not None and not isinstance(raw, dict):
                raise ShapeSpecError(
                    f"`{SHAPE_PROFILE_KEY}:` in {declaration} is not a mapping")
            block = raw
    if block is not None:
        enum = _declared_list(block, "audit_class_enum", declaration)
        homes = _declared_list(block, "home_patterns", declaration)
        return RepoProfile(
            name=label,
            audit_class_enum=frozenset(enum) if enum is not None else None,
            home_patterns=tuple(homes) if homes is not None else None,
        )
    if (root / SHAPE_SPEC_REL).exists():
        return dataclasses.replace(HUB_PROFILE, name=label)
    return dataclasses.replace(FLEET_PROFILE, name=label)


def _home_matches(home: str, pattern: str) -> bool:
    """One home vs one pattern under the three-token grammar above.

    `**` DOES NOT ADMIT A DOT-PREFIXED SEGMENT beneath it (terra HIGH, 2026-09-07). The
    finding: admitting `src/**`, `eval/**` and `models/**` per amendment D5 also admits
    `src/.github/workflows/`, so a dot-directory Rule A refuses at the root could be
    reintroduced one level down and the top-level seal would be silent about it. Dot-prefixed
    homes are exactly the ones ADR-59 governs by name, so an open depth-wildcard is the wrong
    instrument to admit them: the two the repo actually has --
    `ecosystem/.dev-knowledge/history` and `plugins/tier1-lifecycle/.claude-plugin` -- are
    admitted by EXPLICIT `*` patterns and are unaffected, which was measured over all 2991
    tracked paths before this leg was added. A dot home under a `**` tree therefore stays a
    surfaced act: name it with a literal or a `*` pattern.
    """
    hp = home.split("/")
    pp = pattern.split("/")
    if pp[-1] == "**":
        head = pp[:-1]
        if not (len(hp) > len(head) and hp[: len(head)] == head):
            return False
        return not any(seg.startswith(".") for seg in hp[len(head):])
    if len(hp) != len(pp):
        return False
    return all(p == "*" or p == h for h, p in zip(hp, pp))


#: `scripts/logs_retention.py` relocates a dated `logs/<STEM>-YYYY-MM-DD.<ext>` into a
#: `logs/YYYY-MM/` month bucket (`plan_moves`). That bucket is a GRAMMAR home, the same kind
#: of rule as `<allowed-home>/archive` below: the mover writes it on every SessionStart, so
#: refusing it made two hub organs contradict each other -- one performing a relocation the
#: other would not let anyone commit (operator ruling 2026-09-16: fix the gate, not the
#: mover; `[#785]` recorded the disagreement). The month is a REAL calendar month, `01`-`12`,
#: and only ONE level under `logs` -- `logs/misc/` and `logs/2026-09/sub/` stay surfaced acts.
#: `tests/test_validate_hermetization.py` asserts every destination `plan_moves` produces is
#: admitted, so the two organs cannot drift apart again without a RED.
_RETENTION_BUCKET_RE = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$")


def is_allowed_home(home: str, profile: RepoProfile = HUB_PROFILE) -> bool:
    """True iff `home` (a repo-relative POSIX directory) is an admissible home.

    THE FLEET HALF comes first and applies to every repo: `docs` itself is not a home. The
    spec states that absence as the rule this clause exists to state -- it is why
    `docs/ORGAN-INDEX.md` was relocated, and it is what caught both of Rule C's genuine
    fleet findings (`docs/2026-08-28-nb2-lane-b-packet.md`, `docs/tenrox-console-uploader.md`).

    THE REPO-LOCAL HALF is the pattern tuple, and a repo that declares none is not judged
    against another repo's: `home_patterns is None` admits every other home. That single
    branch is 72 of the fleet's 336 waivers -- class H1, "a sanctioned directory organized
    one level deeper than the hub organizes it".

    `<allowed-home>/archive` is a GRAMMAR rule rather than a literal. The spec states this
    one shape six times (`protocols/archive`, `templates/archive`, `tasks/archive`,
    `docs/decisions/archive`, `docs/intake/archive`, `docs/archive`), so the seventh
    instance -- corp-monorepo's `scripts/archive/` -- was out-of-pattern for no reason but
    the enumeration. The parent must itself be an admissible home, so this generalizes the
    shape without opening `<anything>/archive`.

    `logs/YYYY-MM` is the second grammar rule, and for the same reason: it is the home
    `logs_retention.py` writes, so admitting it by enumeration would need a new pattern every
    month. `logs` must itself be admitted, so a profile without it gains nothing here.
    """
    if home == "docs":
        return False
    patterns = profile.home_patterns
    if patterns is None:
        return True
    if any(_home_matches(home, pat) for pat in patterns):
        return True
    parts = home.split("/")
    if len(parts) >= 2 and parts[-1] == "archive":
        parent = "/".join(parts[:-1])
        return any(_home_matches(parent, pat) for pat in patterns)
    if (len(parts) == 2 and parts[0] == "logs" and _RETENTION_BUCKET_RE.match(parts[1])
            and any(_home_matches("logs", pat) for pat in patterns)):
        return True
    return False


# --- three clauses that named an organ and had none -----------------------------------
#
# MEASURED 2026-09-09 (`docs/audits/2026-09-09-technical-shape-spec-clause-readers.md`):
# 4 of the spec's 9 clauses were opened by an organ, and THREE named an asserting surface
# that never read them -- `required_docs`, `vscode` and `sorting`. A clause with a
# decorative locator is worse than an unasserted one: `asserted_by: null` is visible in the
# file and admitted as an honest gap, while a locator reads as enforced. The three readers
# below (and the `vscode`/`sorting` pair in `scripts/audit_checks/check_workspace_settings.py`)
# close that. `tests/test_fleet_shape_spec_readers.py` proves each one BEHAVIOURALLY -- it
# doctors the clause and asserts the verdict follows -- because a name-grep over this module
# would prove the clause is mentioned here, not that its value is consumed.
#
# All three are FAIL-CLOSED at load, on this module's stated posture: a spec that will not
# load means the gate has no rules, and a gate that silently admits everything is worse than
# one that refuses to start.

#: The six kinds (AMEND-SESSION-PLAN-001 §2), as a literal HERE rather than read from the
#: file this proves. Same mechanism as `_REGEX_SENTINELS` above: a set the spec supplied
#: could be doctored to agree with a broken spec and would establish nothing. A seventh kind
#: is an edit to both surfaces, which is the point.
KIND_ENUM: frozenset[str] = frozenset(
    {"source", "test", "data", "model", "eval", "tooling"})

#: The cite token a kind uses instead of copying a home the layout clause already states.
_SOURCE_HOME_CITE = "python_layout.source_home_by_layout"


def _python_layout(clauses: dict[str, Any]) -> dict[str, Any]:
    """Resolve the `python_layout` clause: which layout this repo declares, and its homes.

    The clause carries two layouts because both are in-pattern -- a packaged project keeps
    its code under `src/`, a flat governance repo keeps its organs in `scripts/` -- and the
    repo says which one it is. What is checked is the pair the clause cannot be trusted to
    keep consistent by itself: a declared layout the clause never defined, and a source or
    tests home the home grammar above refuses. Those two disagreeing is a spec that admits a
    shape its own seal would reject, which no consumer report could make sense of.
    """
    layout = _clause_str(clauses, "python_layout", "declared_layout")
    layouts = _clause_list(clauses, "python_layout", "source_layouts")
    if layout not in layouts:
        raise ShapeSpecError(
            f"fleet shape spec `python_layout.declared_layout` is {layout!r}, which is not "
            f"one of the declared `source_layouts` {sorted(layouts)}")
    by_layout = clauses["python_layout"].get("source_home_by_layout")
    if not isinstance(by_layout, dict) or not all(
            isinstance(v, str) for v in by_layout.values()):
        raise ShapeSpecError(
            "fleet shape spec `python_layout.source_home_by_layout` is not a mapping of "
            "layout to home")
    missing = sorted(set(layouts) - set(by_layout))
    if missing:
        raise ShapeSpecError(
            f"fleet shape spec `python_layout.source_home_by_layout` defines no home for "
            f"the declared layouts {missing}")
    source_home = by_layout[layout]
    tests_home = _clause_str(clauses, "python_layout", "tests_home")
    for role, home in (("source", source_home), ("tests", tests_home)):
        if not is_allowed_home(home):
            raise ShapeSpecError(
                f"fleet shape spec `python_layout` names {home!r} as the {role} home, which "
                f"the home grammar refuses -- the spec would admit a shape its own seal "
                f"rejects")
    return {"layout": layout, "source_home": source_home, "tests_home": tests_home,
            "source_home_by_layout": dict(by_layout)}


def _kind_homes(clauses: dict[str, Any], layout: dict[str, Any]) -> dict[str, str]:
    """Resolve `home_grammar.kinds` -- six kinds, ONE home each -- and the declaration.

    `source` carries a CITE into `python_layout` rather than a copy of the home, so the two
    clauses cannot drift into naming different source trees; resolving it here is what makes
    the cite load-bearing instead of documentation.
    """
    kinds = clauses["home_grammar"].get("kinds")
    if not isinstance(kinds, dict) or set(kinds) != KIND_ENUM:
        raise ShapeSpecError(
            f"fleet shape spec `home_grammar.kinds` carries {sorted(kinds) if isinstance(kinds, dict) else kinds!r}; "
            f"the grammar is the six kinds {sorted(KIND_ENUM)}")
    homes: dict[str, str] = {}
    for kind, home in kinds.items():
        if not isinstance(home, str) or not home:
            raise ShapeSpecError(
                f"fleet shape spec `home_grammar.kinds.{kind}` carries {home!r}; a kind "
                f"carries exactly one home")
        homes[kind] = layout["source_home"] if home == _SOURCE_HOME_CITE else home
    declared = _clause_list(clauses, "home_grammar", "declared_kinds")
    stray = sorted(set(declared) - KIND_ENUM)
    if stray or len(set(declared)) != len(declared):
        raise ShapeSpecError(
            f"fleet shape spec `home_grammar.declared_kinds` is {declared}; each member is "
            f"one of the six kinds, declared once (offending: {stray or 'a repeat'})")
    return homes


def _require_one_registry(clauses: dict[str, Any]) -> str:
    """`required_docs.source` and `root_allowlist.files_from` name the SAME registry.

    THE ONE READ THIS CLAUSE CAN CARRY. `required_docs` deliberately restates no roster --
    CLOUD-4 v2 made ADR-101 §1's file enum and the ADR-38 canonical set provably the same
    strings, and copying those names into YAML would undo it. So the clause holds a citation
    and nothing else, and the only thing an organ can check about a citation held twice is
    that the two copies agree. Two clauses citing one registry by two strings is a drift
    pair; one string checked at load is not.
    """
    source = _clause_str(clauses, "required_docs", "source")
    files_from = _clause_str(clauses, "root_allowlist", "files_from")
    if source != files_from:
        raise ShapeSpecError(
            f"fleet shape spec cites the canonical registry twice and disagrees: "
            f"`required_docs.source` is {source!r} and `root_allowlist.files_from` is "
            f"{files_from!r} -- both name the same registry")
    return source


#: The declared Python layout and its homes (spec clause `python_layout`).
PYTHON_LAYOUT: dict[str, Any] = _python_layout(SHAPE_SPEC)

#: kind -> its ONE home, with the `source` cite resolved (spec `home_grammar.kinds`).
KIND_HOMES: dict[str, str] = _kind_homes(SHAPE_SPEC, PYTHON_LAYOUT)

#: The kinds THIS repo declares it HAS (spec `home_grammar.declared_kinds`). Admission and
#: declaration are different acts: `models/` and `eval/` are admitted by the grammar and
#: exist in no directory here, which is why the existence half is scoped to this tuple.
DECLARED_KINDS: tuple[str, ...] = tuple(
    _clause_list(SHAPE_SPEC, "home_grammar", "declared_kinds"))

#: The one canonical-docs registry, proven to be cited identically by both clauses that
#: cite it (spec `required_docs.source` == `root_allowlist.files_from`).
REQUIRED_DOCS_REGISTRY: str = _require_one_registry(SHAPE_SPEC)


# --- pure classifiers (unit-tested directly; no git) ----------------------------------

def _posix_parts(path: str) -> list[str]:
    """Repo-relative path -> its components, normalized to forward slashes."""
    return path.replace("\\", "/").strip("/").split("/")


def rule_a_violation(path: str) -> Optional[str]:
    """Rule A (top-level seal). Return a BLOCK reason, or None if the added path is
    sanctioned by the top-level rules."""
    parts = _posix_parts(path)
    if len(parts) == 1:
        # A top-level file: must be a sanctioned class member, either by literal name or
        # by one of the spec's parameterized classes. The glob leg is what lets a per-repo
        # filename (`.corp-monorepo.code-workspace`) satisfy a fleet rule that used to be
        # written as one repo's literal.
        if parts[0] in SANCTIONED_TIER1_FILES:
            return None
        if any(fnmatch.fnmatch(parts[0], g) for g in SANCTIONED_TIER1_FILE_GLOBS):
            return None
        return (f"unsanctioned new top-level file '{parts[0]}' -- Tier-1 files are a "
                f"closed class (ADR-101 section 1); a genuinely new class is an "
                f"ADR-101 amendment, not a drive-by add")
    top = parts[0]
    if top not in SANCTIONED_TIER1_DIRS:
        return (f"unsanctioned new top-level directory '{top}/' -- Tier-1 dirs are a "
                f"closed set (ADR-101 section 1); surface a new top-level dir via an "
                f"ADR-101 amendment before creating it")
    if top == "docs" and len(parts) >= 3:
        genre = parts[1]
        if genre not in SANCTIONED_GENRES:
            return (f"unsanctioned new docs genre folder 'docs/{genre}/' -- Tier-2 genres "
                    f"are a closed set (ADR-101 section 1); a new artifact class nests "
                    f"under an existing genre or is surfaced via an ADR-101 amendment")
    return None


def rule_b_violation(path: str, profile: RepoProfile = HUB_PROFILE) -> Optional[str]:
    """Rule B (audit grammar + R4 casing). Applies ONLY to an added docs/audits/*.md.
    Return a BLOCK reason, or None.

    FLEET: the R4 casing rule and the date shape. Both travelled to a consumer intact --
    corp-monorepo runs the casing leg locally as its own `validate_audit_casing.py` -- and
    both stay armed for every repo, declared or not.

    REPO-LOCAL: the class enum. The spec carries `audit_class_enum_scope: repo-local` and
    no organ read it, so a vocabulary adopted from "what three repos already write"
    refused 194 correctly-named artifacts across the fleet, 28 of them in one repo that had
    already recorded the reason in its own waiver.
    """
    parts = _posix_parts(path)
    # Applicability is EXTENSION-CASE-INSENSITIVE so an uppercase `.MD` cannot dodge Rule B
    # by escaping the `.md` match (codex-review 2026-07-11); the casing rule below then
    # rejects the uppercase extension itself.
    if not (len(parts) == 3 and parts[0] == "docs" and parts[1] == "audits"
            and parts[2].lower().endswith(".md")):
        return None  # not an audit file -> Rule B is silent
    fname = parts[2]
    if fname.lower() == "readme.md":
        return None  # the generated index, not an audit artifact

    # R4 casing FIRST, on the FULL filename incl. extension (the corp UPPERCASE/underscore
    # divergence class + the .MD extension loophole).
    if not _LOWER_KEBAB_DOT.match(fname):
        return (f"casing: '{fname}' must be all-lowercase kebab-case everywhere incl. the "
                f".md extension (no UPPERCASE, no _underscore_, no CamelCase; only a `.` "
                f"inside the slug for a repo/version token) -- ADR-101 R4")
    stem = fname[: -len(".md")]  # fname is now guaranteed lowercase '.md'

    # Grammar: leading YYYY-MM-DD- (SHAPE only, never date-accuracy).
    if not _DATE_SHAPE.match(stem):
        return (f"grammar: '{fname}' must start with a <YYYY-MM-DD>- date shape "
                f"(ADR-101 section 2); name-shape only, date-accuracy is never checked")

    # Class: whole-token LONGEST-MATCH against the CLOSED enum. A degenerate <date>-<class>
    # passes; a class-then-slug requires a WELL-FORMED slug (no empty/leading-/double-hyphen).
    # The REPO-LOCAL leg. An undeclared repo is not policed by another repo's vocabulary,
    # and the slug leg goes with it: a slug is only well-formed RELATIVE to a class token.
    if profile.audit_class_enum is None:
        return None
    remainder = stem[_DATE_PREFIX_LEN:]
    for cls in _class_by_len(profile.audit_class_enum):
        if remainder == cls:
            return None  # degenerate <date>-<class>.md (recurring report, no slug)
        if remainder.startswith(cls + "-"):
            slug = remainder[len(cls) + 1:]
            if _SLUG_RE.match(slug):
                return None  # class-then-well-formed-slug
            return (f"slug: '{fname}' has a malformed slug after <class> '{cls}' "
                    f"(empty / leading- / trailing- / double-hyphen) -- ADR-101 section 2 "
                    f"kebab-case")
    return (f"class: '{fname}' has no <class> token after the date from the enum "
            f"{profile.name} declares (ADR-101 R3, whole-token longest-match): "
            f"{'/'.join(sorted(profile.audit_class_enum))}")


def rule_c_violation(path: str, profile: RepoProfile = HUB_PROFILE) -> Optional[str]:
    """Rule C (home allowlist). Return a BLOCK reason, or None.

    Scoped to paths whose top-level entry is ALREADY sanctioned: when it is not, Rule A
    refuses first and says something more useful about it, and two rules shouting about
    one path helps nobody. A top-level FILE is Rule A's territory entirely.
    """
    parts = _posix_parts(path)
    if len(parts) < 2:
        return None                       # top-level file -> Rule A owns it
    if parts[0] not in SANCTIONED_TIER1_DIRS:
        return None                       # Rule A already blocks, with a better message
    home = "/".join(parts[:-1])
    if is_allowed_home(home, profile):
        return None
    return (f"new path outside allowlisted homes -- operator approval required: "
            f"'{home}/' is not an admissible home for a new file. The homes are the ones "
            f"{profile.name} declares (`{SHAPE_PROFILE_KEY}.home_patterns`, or the fleet "
            f"spec's `home_grammar` for the repo that carries it); a genuinely new one is "
            f"an operator decision recorded as a ruling, not a drive-by add")


def classify(path: str, profile: RepoProfile = HUB_PROFILE) -> Optional[str]:
    """One added path -> the first BLOCK reason (Rule A, then B, then C), or None."""
    return (rule_a_violation(path)
            or rule_b_violation(path, profile)
            or rule_c_violation(path, profile))


def check(added_paths: list[str], profile: RepoProfile = HUB_PROFILE) -> list[str]:
    """Every added path -> the list of `path: reason` BLOCK strings (empty == clean)."""
    reasons: list[str] = []
    for p in added_paths:
        r = classify(p, profile)
        if r is not None:
            reasons.append(f"{p}: {r}")
    return reasons


# --- REPORT mode: one repository, read-only -------------------------------------------
# Both fleet seal reports state the same honest limit -- "the seal has no consumer mode and
# no --report flag; this run drove its rule functions from the hub" -- and each rebuilt the
# same throwaway harness to work around it. The harness is the artifact now.
#
# GRAIN, matching those two reports exactly so their numbers and this one are commensurable:
# Rule A per ITEM (a top-level file, a top-level directory, a docs/<genre>/), Rule B per
# FILE, Rule C per DISTINCT HOME. A path that trips Rule A is not counted again under B or
# C, mirroring `classify`'s own short-circuit.


@dataclasses.dataclass(frozen=True)
class SealReport:
    """One repository's out-of-pattern items, at the grain the seal reports declare."""

    repo_root: Path
    profile: RepoProfile
    head: str
    branch: str
    tracked: int
    rule_a_items: list[str]
    rule_b_files: list[str]
    rule_c_homes: list[str]

    @property
    def item_count(self) -> int:
        return len(self.rule_a_items) + len(self.rule_b_files) + len(self.rule_c_homes)


def _git_out(repo_root: Path, *args: str) -> str:
    """One read-only git read against another repository. Never writes, never checks out."""
    out = subprocess.run(["git", "-C", str(repo_root), *args],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed in {repo_root}: "
            f"{out.stderr.strip() or out.returncode}")
    return out.stdout


def seal_repo(repo_root: Any, profile: Optional[RepoProfile] = None,
              name: Optional[str] = None) -> SealReport:
    """Seal one repository READ-ONLY and return its out-of-pattern items.

    RETROSPECTIVE, and deliberately unlike the pre-commit gate: it reads every TRACKED
    path, where the gate reads only staged ADDs. That is the mode both seal reports ran in
    and the mode a first-contact consumer report needs -- but it means an existing file
    the prospective gate has never inspected appears here, which is why the hub's own
    ADR-101 section 6 grandfathered audit filenames are visible to this function and
    invisible to the gate.
    """
    root = Path(repo_root)
    resolved = profile if profile is not None else profile_for_repo(root, name=name)
    paths = [p for p in _git_out(root, "ls-files").splitlines() if p.strip()]
    a_items: list[str] = []
    b_files: list[str] = []
    c_homes: list[str] = []
    for p in paths:
        parts = _posix_parts(p)
        if rule_a_violation(p) is not None:
            if len(parts) == 1:
                item = parts[0]
            elif parts[0] not in SANCTIONED_TIER1_DIRS:
                item = parts[0]
            else:
                item = f"{parts[0]}/{parts[1]}"
            if item not in a_items:
                a_items.append(item)
            continue
        if rule_b_violation(p, resolved) is not None:
            b_files.append(p)
            continue
        if rule_c_violation(p, resolved) is not None:
            home = "/".join(parts[:-1])
            if home not in c_homes:
                c_homes.append(home)
    try:
        head = _git_out(root, "rev-parse", "--short", "HEAD").strip()
        branch = _git_out(root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    except RuntimeError:
        head, branch = "(no commits)", "(none)"
    return SealReport(repo_root=root, profile=resolved, head=head, branch=branch,
                      tracked=len(paths), rule_a_items=sorted(a_items),
                      rule_b_files=sorted(b_files), rule_c_homes=sorted(c_homes))


# --- git glue (fail-open-loud) --------------------------------------------------------

def staged_added_paths() -> list[str]:
    """Paths staged with status A (added). Prospective-only: MODIFIED existing files are
    grandfathered. `--no-renames` forces a rename to surface as delete+ADD so a rename that
    introduces a NEW unsanctioned pathname is policed too (codex-review 2026-07-11) -- a
    rename introduces a new pathname just as much as a plain add. Fail-open on git error."""
    out = subprocess.run(
        ["git", "diff", "--cached", "--diff-filter=A", "--no-renames", "--name-only"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or f"git exited {out.returncode}")
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def main() -> int:
    try:
        added = staged_added_paths()
    except (OSError, RuntimeError) as exc:
        # Fail OPEN but LOUD: a hermetization convention gate, not a safety control.
        print(f"validate_hermetization: WARNING -- could not read staged adds ({exc}); "
              f"hermetization check skipped", file=sys.stderr)
        return 0
    reasons = check(added)
    if reasons:
        print("validate_hermetization: refused -- ADR-101 hermetization violation(s):",
              file=sys.stderr)
        for r in reasons:
            print(f"  {r}", file=sys.stderr)
        print("  The tree is hermetic (ADR-101): a new top-level entry / docs genre, an "
              "off-grammar audit filename, or a file in a home the repo has no convention "
              "for, is a deliberate act -- not a drive-by add. Bypass (peer-hook parity): "
              "git commit --no-verify.",
              file=sys.stderr)
        return 1
    return 0


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """ADR-101 tree seal.

    With no sub-command this is the prospective pre-commit gate, unchanged: the hook is
    wired `pass_filenames: false` and passes no arguments, so the group callback IS the
    gate and `report` is additive.
    """
    if ctx.invoked_subcommand is None:
        ctx.exit(main())


@cli.command("report")
@click.argument("repo_root", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--name", default=None,
              help="Label for the repository (default: its directory name).")
@click.option("--items/--no-items", default=True, show_default=True,
              help="List every out-of-pattern item, not only the counts.")
def report_command(repo_root: Path, name: Optional[str], items: bool) -> None:
    """REPORT mode: seal one repository READ-ONLY and log its out-of-pattern items.

    Writes NOTHING in REPO_ROOT -- `git ls-files` and `git rev-parse` only.
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    report = seal_repo(repo_root, name=name)
    profile = report.profile
    logger.info("repo      %s  %s  %s  %d tracked",
                profile.name, report.head, report.branch, report.tracked)
    logger.info("profile   audit_class_enum=%s  home_patterns=%s",
                "declared" if profile.audit_class_enum is not None else "undeclared",
                "declared" if profile.home_patterns is not None else "undeclared")
    logger.info("items     %d   (A %d  B %d  C %d homes)", report.item_count,
                len(report.rule_a_items), len(report.rule_b_files),
                len(report.rule_c_homes))
    if items:
        for item in report.rule_a_items:
            logger.info("  A  %s", item)
        for path in report.rule_b_files:
            logger.info("  B  %s", path)
        for home in report.rule_c_homes:
            logger.info("  C  %s/", home)


if __name__ == "__main__":
    cli()
