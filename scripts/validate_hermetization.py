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

Consumer carrier (floor/plugin) is the P6 rollout -- this gate is HUB-ONLY until then,
mirroring `roster-freshness`/`claude-rosters-freshness`/`audit-index-freshness`.

Read-only (Layer-2, ADR-28/36): reads the staged name-status; writes NOTHING. Fail-OPEN
but LOUD on any git error -- a convention/hygiene gate must not brick every commit on a
near-impossible git failure. Bypass parity with peer hooks: `--no-verify`.
"""

from __future__ import annotations

import re
import subprocess
import sys
from typing import Optional

# CLOUD-4 v2 (R2 §1.5 GO-b) — the canonical living-doc names come from the one registry.
try:
    from scripts import canonical_docs as _cdocs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoint
    import canonical_docs as _cdocs

# --- ADR-101 section 1 sanctioned sets (CLOSED; grow only by ADR-101 amendment) -------

# Tier-1 -- sanctioned top-level directories.
SANCTIONED_TIER1_DIRS: frozenset[str] = frozenset({
    ".claude", ".claude-plugin", ".vscode", "codex", "config", "deploy", "docs",
    "ecosystem", "logs", "plugins", "protocols", "scripts",
    # [#433] restructure strangler (ADR-101 amendment 2026-07-27): the DERIVED
    # per-task tree emitted from BACKLOG.md by scripts/gen_task_tree.py --
    # BACKLOG.md stays the source of truth until the flip arc.
    "tasks",
    "templates", "tests",
    # [#501] server-side recorder (ADR-101 amendment 2026-08-06): the GitHub Actions
    # REPORT-ONLY wall -- the one server-side observation organ, re-creating the
    # directory that `82227f08` deleted under [#255]. Report-only forever (private
    # repo, Free tier -- required checks are unavailable), so no gate lives here.
    ".github",
    # [#554] off-machine lane substrate (ADR-101 amendment 2026-08-18, operator
    # path-approval D6 at the batch GO): the devcontainer spec + its idempotent
    # provisioning script. Read by a container runtime (Codespaces / `devcontainer up`),
    # never by this repo's gate mesh -- it carries no organ and judges nothing, which is
    # what distinguishes it from the `.github/` sanction above.
    ".devcontainer",
    # `prompts` WAS here (operator path-approval 2026-08-25, lane-RL scope extension) and
    # is REVOKED by operator ruling 2026-08-26 -- root is sacred, and the docs disease is
    # cured by the consumer gate ([#595]), not by a sibling folder at the root. Dispatch
    # INPUTS keep their home and their byte-identity; the home moves under the genre tree
    # to `docs/audits/<date>-technical-<batch>-launch-contracts/` (see `_HOME_PATTERNS`).
    # The closed set therefore SHRINKS by one, which is the first contraction it has taken
    # -- recorded as the ADR-101 amendment of 2026-08-26 (the second one, which revokes
    # the first). Deliberately left as a comment rather than a silent deletion: a reader
    # who finds `prompts/` in the git history must be able to see why it is gone.
})

# Tier-1 -- sanctioned top-level FILES (the closed class members, ADR-101 section 1).
SANCTIONED_TIER1_FILES: frozenset[str] = frozenset({
    # living docs (UPPERCASE.md, the closed set) — CLOUD-4 v2 (R2 §1.5 GO-b): the seven names
    # come from `scripts/canonical_docs.py` rather than being retyped here. Membership is
    # unchanged, and the frozenset is still built at import time, so Rule A's cost is the
    # same. What changes is that ADR-101 §1's file enum and the ADR-38 canonical set now
    # provably name the same seven strings.
    *_cdocs.CANONICAL_MANDATORY,
    # dotfile / tool config
    ".gitignore", ".gitattributes", ".pre-commit-config.yaml",
    ".pre-commit-hooks.yaml", ".ruff.toml", ".worktreeinclude",
    ".dev-knowledge.code-workspace",
    # intake #12 section-9a ruling (SETTLED 2026-07-12): the hub carries its OWN
    # .methodology.yaml as a fleet member -- ADR-101 amendment 2026-07-13, [#328].
    ".methodology.yaml",
    # build / package manifests
    "package.json", "package-lock.json", "pyproject.toml",
    # uv toolchain (ADR-101 amendment 2026-07-27, [#432]/ADR-106): the committed
    # dependency lockfile + interpreter pin -- same class as package-lock.json.
    "uv.lock", ".python-version",
    # portable instruction layer (ADR-101 amendment 2026-08-25, ADR-115; execution
    # [#577]). DELIBERATELY a literal and NOT a member of _cdocs.CANONICAL_MANDATORY:
    # AGENTS.md is an UPPERCASE.md Tier-1 file but it is NOT an ADR-38 canonical
    # living doc -- no `last_reviewed` stamp, absent from FRESHNESS_FILES, no section
    # history. Adding it to CANONICAL_MANDATORY would silently enrol it in the
    # freshness gate and in every consumer's canonical-set conformance check.
    "AGENTS.md",
})

# Tier-2 -- sanctioned docs/<genre>/ folders. `runbooks` LEFT the set 2026-07-22
# (ADR-101 amendment: d.i REVERSED -- the one-member genre collapsed into protocols/).
SANCTIONED_GENRES: frozenset[str] = frozenset({
    "archive", "audits", "decisions", "handoffs", "intake",
})

# --- ADR-101 section 2 + R3: the CLOSED 11-class audit-class enum ----------------------
# Whole-token LONGEST-MATCH (never split-on-first-hyphen). On-disk forms per R2 (the enum
# adopts what three repos already write: `codex` not `codex-review`;
# `conformance-nightly-digest` not `conformance-digest`).
AUDIT_CLASS_ENUM: frozenset[str] = frozenset({
    # semantic
    "technical", "functional", "qa", "census", "verification",
    # recurring / automated (on-disk forms, R2)
    "ecosystem-audit", "conformance-nightly-digest", "changelog-review",
    # reviewer-origin (on-disk forms, R1/R2)
    "codex", "fresh-eyes",
    # incident
    "incident-evidence",
})

# Longest-match order: try the longest tokens first so `ecosystem-audit` wins over a
# hypothetical `ecosystem` split, and `conformance-nightly-digest` is matched whole.
_ENUM_BY_LEN = tuple(sorted(AUDIT_CLASS_ENUM, key=len, reverse=True))

_DATE_SHAPE = re.compile(r"^\d{4}-\d{2}-\d{2}-")           # SHAPE only (S3-4)
_DATE_PREFIX_LEN = len("YYYY-MM-DD-")                       # 11 chars incl. trailing hyphen
# R4 casing: all-lowercase kebab-case + digits; `.` carve-out (repo/version tokens). No
# uppercase, no underscore, no other charset. Applied to the FULL filename (incl. the `.md`
# extension) so an uppercase `.MD` extension is caught too (codex-review 2026-07-11).
_LOWER_KEBAB_DOT = re.compile(r"^[a-z0-9.-]+$")
# A well-formed slug after the class: 1+ kebab segments of [a-z0-9.] joined by SINGLE
# hyphens — rejects empty / leading- / trailing- / double-hyphen slugs (codex-review
# 2026-07-11). The `.` repo/version carve-out rides inside a segment.
_SLUG_RE = re.compile(r"^[a-z0-9.]+(-[a-z0-9.]+)*$")


# --- Rule C: the HOME allowlist (operator ruling A 2026-08-11; register K-1) ----------
# DERIVED FROM THE LIVE TAXONOMY, not invented: every pattern below is a home that tracked
# files already occupy at the time of writing, and `test_rule_c_admits_every_tracked_path`
# asserts exactly that against `git ls-files`. So the allowlist cannot silently diverge
# from the tree it describes -- if a pattern is dropped, that test reds rather than the
# gate quietly refusing legitimate work.
#
# Pattern grammar, deliberately three tokens wide so the set stays readable:
#   `a/b`   -- that literal home, exactly
#   `a/*`   -- any single immediate child of `a` is a home
#   `a/**`  -- any home at one-or-more levels below `a` (bundle / fixture trees)
#
# HONEST LIMIT, stated rather than left to be discovered: Rule C polices the HOME of an
# added file, and `**` homes admit arbitrary depth below them. A new sub-directory inside
# an already-open home (a new handoff bundle, a new test fixture tree) is admitted by
# design -- those are the shapes the repo creates routinely and gating them would make the
# organ a nuisance rather than a seal. What it catches is a file whose home is a place the
# repo has no convention for, which is the class `docs/ORGAN-INDEX.md` belonged to.
_HOME_PATTERNS: tuple[str, ...] = (
    # agent/runtime config
    ".claude", ".claude/*", ".claude/skills/*",
    ".claude-plugin",
    # [#554] / ADR-101 amendment 2026-08-18: the BARE literal, deliberately -- the
    # substrate is two files at ONE level (devcontainer.json + provision.sh), so a
    # sub-directory inside it stays a surfaced act rather than a `*`/`**` free pass.
    ".devcontainer",
    ".github/workflows",
    ".vscode",
    # source + tooling
    "codex",
    "config",
    "deploy", "deploy/lived_sandbox",
    "logs",
    "plugins/*", "plugins/*/*",
    "protocols", "protocols/archive",
    "scripts", "scripts/audit_checks", "scripts/codemap", "scripts/hooks", "scripts/toc",
    # `tasks/archive` -- the [#612] doc-rot row-body archival destination, admitted by
    # OPERATOR DECISION **D3**, carried in the night-batch-2 GO of 2026-08-28 ("the
    # archival destination is `tasks/archive/`, APPROVED"). Admitted as the BARE literal
    # and NOT `tasks/archive/*`: the tree is flat by construction (one record per row,
    # named for its row), so a sub-directory inside it stays a surfaced act -- the same
    # narrowness `.devcontainer` above is admitted under, and the same
    # `<parent>/archive` shape `protocols/archive`, `templates/archive`,
    # `docs/decisions/archive` and `docs/intake/archive` already carry. Rule A needs no
    # amendment: `tasks` is already a sanctioned Tier-1 directory, so this is a home
    # BELOW an existing sanction, not a new top-level class.
    "tasks", "tasks/archive",
    "templates", "templates/archive", "templates/claude-regions",
    "templates/handoff", "templates/handoff/*",
    "tests", "tests/fixtures", "tests/fixtures/**",
    # generated / declared ecosystem state (the organ index's home since 2026-08-12)
    "ecosystem", "ecosystem/schema", "ecosystem/*/history",
    # docs: GENRE trees only. `docs` itself is absent BY DESIGN -- that absence is the
    # rule this leg exists to state, and it is why the relocation was owed.
    "docs/archive",
    # `docs/audits/*` -- one home per BATCH LAUNCH-CONTRACT directory. Operator ruling
    # 2026-08-26 (ADR-101 amendment below the `prompts/` one) revoked the root `prompts/`
    # folder and relocated its convention under the genre tree as
    # `docs/audits/<date>-technical-<batch>-launch-contracts/`. The `*` is the same shape
    # the revoked `prompts/*` carried and for the same reason: the homes are the per-batch
    # directories one level down, and a deeper nesting stays a surfaced act.
    # HONEST LIMIT, stated rather than left to be found: the grammar has three tokens, so
    # `*` is the narrowest pattern that can express "one dir per batch". It admits ANY
    # immediate child directory of `docs/audits/`, not only the ruled name shape -- the
    # narrower convention lives in ADR-101 and PLAYBOOK Ch8 and is checked by nobody.
    "docs/audits", "docs/audits/*",
    "docs/decisions", "docs/decisions/archive",
    "docs/handoffs", "docs/handoffs/**",
    "docs/intake", "docs/intake/archive",
    # `prompts/*` WAS here and is REVOKED with its top-level entry above (operator ruling
    # 2026-08-26). Its replacement is `docs/audits/*` in the docs block above -- same
    # shape, same reasoning, inside the genre tree instead of at the root.
)


def _home_matches(home: str, pattern: str) -> bool:
    """One home vs one pattern under the three-token grammar above."""
    hp = home.split("/")
    pp = pattern.split("/")
    if pp[-1] == "**":
        head = pp[:-1]
        return len(hp) > len(head) and hp[: len(head)] == head
    if len(hp) != len(pp):
        return False
    return all(p == "*" or p == h for h, p in zip(hp, pp))


def is_allowed_home(home: str) -> bool:
    """True iff `home` (a repo-relative POSIX directory) is an admissible home."""
    return any(_home_matches(home, pat) for pat in _HOME_PATTERNS)


# --- pure classifiers (unit-tested directly; no git) ----------------------------------

def _posix_parts(path: str) -> list[str]:
    """Repo-relative path -> its components, normalized to forward slashes."""
    return path.replace("\\", "/").strip("/").split("/")


def rule_a_violation(path: str) -> Optional[str]:
    """Rule A (top-level seal). Return a BLOCK reason, or None if the added path is
    sanctioned by the top-level rules."""
    parts = _posix_parts(path)
    if len(parts) == 1:
        # A top-level file: must be a sanctioned class member.
        if parts[0] not in SANCTIONED_TIER1_FILES:
            return (f"unsanctioned new top-level file '{parts[0]}' -- Tier-1 files are a "
                    f"closed class (ADR-101 section 1); a genuinely new class is an "
                    f"ADR-101 amendment, not a drive-by add")
        return None
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


def rule_b_violation(path: str) -> Optional[str]:
    """Rule B (audit grammar + R4 casing). Applies ONLY to an added docs/audits/*.md.
    Return a BLOCK reason, or None."""
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
    remainder = stem[_DATE_PREFIX_LEN:]
    for cls in _ENUM_BY_LEN:
        if remainder == cls:
            return None  # degenerate <date>-<class>.md (recurring report, no slug)
        if remainder.startswith(cls + "-"):
            slug = remainder[len(cls) + 1:]
            if _SLUG_RE.match(slug):
                return None  # class-then-well-formed-slug
            return (f"slug: '{fname}' has a malformed slug after <class> '{cls}' "
                    f"(empty / leading- / trailing- / double-hyphen) -- ADR-101 section 2 "
                    f"kebab-case")
    return (f"class: '{fname}' has no CLOSED-enum <class> token after the date "
            f"(ADR-101 R3: technical/functional/qa/census/verification/ecosystem-audit/"
            f"conformance-nightly-digest/changelog-review/codex/fresh-eyes/"
            f"incident-evidence; whole-token longest-match)")


def rule_c_violation(path: str) -> Optional[str]:
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
    if is_allowed_home(home):
        return None
    return (f"new path outside allowlisted homes -- operator approval required: "
            f"'{home}/' is not an admissible home for a new file. The repo's homes are "
            f"derived from the live taxonomy (see _HOME_PATTERNS); a genuinely new one is "
            f"an operator decision recorded as a ruling, not a drive-by add")


def classify(path: str) -> Optional[str]:
    """One added path -> the first BLOCK reason (Rule A, then B, then C), or None."""
    return rule_a_violation(path) or rule_b_violation(path) or rule_c_violation(path)


def check(added_paths: list[str]) -> list[str]:
    """Every added path -> the list of `path: reason` BLOCK strings (empty == clean)."""
    reasons: list[str] = []
    for p in added_paths:
        r = classify(p)
        if r is not None:
            reasons.append(f"{p}: {r}")
    return reasons


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


if __name__ == "__main__":
    sys.exit(main())
