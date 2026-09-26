#!/usr/bin/env python
"""carrier_landed_check.py -- an OPEN carrier whose `lands-via` already resolves on `main`,
flagged before the next handoff cut re-asks the same question (LANE-5B3-4-decision-debt).

THE GAP THIS CLOSES. P11's own reader (`gen_handoff.carriage_verdicts`) judges a decision
file's `carried-by:` value and nothing else -- a file stating the literal `OPEN` PASSES leg 1
by construction, on the understanding that leg 2 (naming it in a bundle's RESIDUAL.md) covers
the debt at cut time. Nothing between cuts ever asks the complementary question a human has to
carry in their head: *"this file said its home would be X once X landed -- has X landed?"*
Measured 2026-09-26 on the live transport: 58 of 215 decision files carry `carried-by: OPEN`,
and several already name a `lands-via` home that resolves on `main` today (an ADR merged, a
digest committed) with nobody having gone back to update the header. That is exactly the
"decided and unscheduled" blindness `decision_coverage.py` exists to remove, one door along:
there it is an accepted DECISION with no implementing row; here it is a CARRIER whose own
stated landing condition is already true.

ADVISORY, NEVER A GATE (ruling (a), pre-authorized). This organ prints and exits 0 always --
it names a CANDIDATE for a human (or the next lane touching that file) to verify and land,
because "a repo home is a claim" (this lane's contract): setting `carried-by:` to a path is an
assertion the file's own ruling reached that home, and only a reader who has read both texts
can confirm that, not a token match. Automating the write would risk asserting a landing the
prose never actually claims.

WHAT "MET" MEANS, and its one honest limit. `lands-via`'s value is prose, not a grammar --
"the WAVE5B-N3 lanes through the integrator; to-browser/DIGEST-WAVE5B-N3-<date>.md ..." names
an intention, several homes, or none at all. This organ reuses `gen_handoff`'s own carrier-token
extraction (`_carrier_tokens`) rather than inventing a second tokenizer that could disagree with
the one the carried-by leg already trusts, but NARROWS what counts as "met" to tokens that
resolve on `main` as a FILE (a git blob), not a directory (a git tree) -- unlike a `carried-by:`
value, where a bare directory is a legitimate claim ("the whole tree is the home"), a
`lands-via:` naming a directory is almost always a generic promise ("the next landing under
docs/audits/"), and `docs/audits/` resolves on `main` in every commit this repo has ever made.
MEASURED live, 2026-09-26: the unfiltered tokenizer flagged 12 files on exactly that
false-positive class, zero of them evidence that a SPECIFIC ruling landed. The blob-vs-tree
check (`_is_blob_on_main`, CORRECTED from an earlier extension-allowlist version -- see its own
docstring) cuts that class to zero without also silently dropping a genuinely-landed file whose
extension an allowlist did not happen to name. A "met" verdict is therefore *"at least one
specific file this text named now exists"* -- necessary evidence that the prediction came true,
never proof that the file's CONTENT carries this ruling (the same honest limit
`carriage_verdicts` itself states for `carried-by`). A `lands-via` with no file-shaped token (a
bare directory, or a narrative like "the operator's ratification") or none of whose tokens
resolve is `unmet`, not a false negative -- the debt is real and belongs in the contract's
RESIDUAL-CARRIERS block, not dropped here.

SCOPE: only files P11 itself reads as `CARRIAGE_OPEN` -- a file with no anchored `carried-by:`
key, or one whose value is UNRESOLVED prose, is a different defect this organ does not
duplicate (`gen_handoff`'s own rows 10/`p11_carriage` already judge those).

Library-first (O-12): stdlib `re` + `pathlib`; the git predicate and the transport walk are
`gen_handoff`'s own (`_resolves_on_main`, `carriage_verdicts`), reused rather than reimplemented
-- a second tokenizer or a second `git cat-file` wrapper is exactly how two carrier readers
drift apart from each other.

Usage:
    python scripts/carrier_landed_check.py check [--repo-root .] [--transport PATH]
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

import gen_handoff as gh  # noqa: E402

#: The `lands-via:` key, read from the same HEAD window `carried-by:` is anchored to
#: (`gen_handoff.CARRIAGE_HEAD_LINES`) -- measured 2026-09-26 across the live transport, the
#: key sits on the line immediately after `carried-by:` in every decision file that carries
#: one, so the same window that anchors one anchors the other.
_LANDS_VIA_RE = re.compile(r"^lands-via:[ \t]*(\S.*)$", re.MULTILINE)

def _is_blob_on_main(repo_root, token: str) -> bool:
    """True when `token` resolves on `main` AND names a FILE (a git blob), not a directory
    (a git tree).

    CORRECTED (Codex terra review round 2, LANE-5B3-4-decision-debt): the first version of
    this organ filtered candidate tokens by a small file-extension allowlist
    (`py|md|yaml|toml|json|sh|ps1`) to keep out bare-directory mentions -- unlike
    `gen_handoff._carrier_tokens` (which admits a bare directory as a legitimate `carried-by:`
    claim, "the whole tree is the home"), a `lands-via:` naming a directory is near-universally
    a GENERIC promise ("the next landing under docs/audits/"), and `docs/audits/` resolves on
    `main` in every commit this repo has ever made. MEASURED live, 2026-09-26: filtering by
    directory alone flagged 12 files on exactly that class. But the extension allowlist was the
    wrong instrument for that -- `gen_handoff._carrier_tokens` already only emits a bare
    (no-`/`) token when it ends in a recognized extension, so every path-shaped token it emits
    (anything containing `/`, e.g. `logs/result.jsonl`, `config/settings.ini`) is EXTENSION-FREE
    at that layer already; re-filtering it by a narrower allowlist here silently dropped a
    genuinely-landed file whose extension the list did not happen to name. Asking git directly
    whether the resolved object is a blob (not a tree) is the actual distinction this organ
    needs, and it is extension-agnostic by construction.
    """
    rel = token.rstrip("/")
    if not rel:
        return False
    ok, out = gh._git_status(Path(repo_root), "cat-file", "-t", f"main:{rel}")  # noqa: SLF001
    return ok and out.strip() == "blob"


@dataclass(frozen=True)
class LandedVerdict:
    """One `CARRIAGE_OPEN` decision file's landing check."""
    path: Path
    lands_via: "str | None"   # None: no anchored `lands-via:` key at all
    met: bool                 # a lands-via token resolves on `main`
    home: "str | None"        # the token that resolved, when met
    detail: str

    def render(self) -> str:
        return f"{self.path.name} ({self.detail})"


def lands_via_value(path) -> "str | None":
    """The anchored `lands-via:` value from the file head, or None when there is no such key."""
    try:
        head = "".join(Path(path).read_text(encoding="utf-8", errors="replace")
                       .splitlines(keepends=True)[:gh.CARRIAGE_HEAD_LINES])
    except OSError:
        return None
    m = _LANDS_VIA_RE.search(head)
    return m.group(1).strip() if m else None


def _open_carriers(transport, repo_root) -> list:
    """`CARRIAGE_OPEN` verdicts only -- the population this organ judges. Any other P11 kind
    (`resolves` / `no-key` / `unresolved`) is a different defect, judged elsewhere."""
    return [v for v in gh.carriage_verdicts(transport, repo_root) if v.kind == gh.CARRIAGE_OPEN]


def landed_verdicts(transport, repo_root) -> list[LandedVerdict]:
    """Every `CARRIAGE_OPEN` decision file, with whether its own `lands-via` has come true."""
    out: list[LandedVerdict] = []
    for v in _open_carriers(transport, repo_root):
        value = lands_via_value(v.path)
        if value is None:
            out.append(LandedVerdict(v.path, None, False, None,
                                     "no anchored `lands-via:` key -- predates the convention, "
                                     "not judgeable by this organ"))
            continue
        tokens = gh._carrier_tokens(value)  # noqa: SLF001 -- reused seam
        home = next((t for t in tokens if _is_blob_on_main(repo_root, t)), None)
        if home is not None:
            out.append(LandedVerdict(
                v.path, value, True, home,
                f"lands-via resolves on `main`: {home} -- carried-by still reads OPEN"))
        elif tokens:
            out.append(LandedVerdict(
                v.path, value, False, None,
                f"lands-via names {len(tokens)} candidate(s), none resolving on `main` as a "
                "file yet (a directory candidate resolving as a tree is not evidence a "
                "specific ruling landed): " + ", ".join(tokens)))
        else:
            out.append(LandedVerdict(
                v.path, value, False, None,
                "lands-via names no repo-path-shaped token at all -- a narrative condition "
                "(an act, a ratification, a merge) this organ cannot resolve"))
    return out


def landed_but_open(transport, repo_root) -> list[LandedVerdict]:
    """The advisory finding: `met and still OPEN`. Everything else is silent by design --
    `unmet` and `no-lands-via` are real facts about the population, printed by `check` for
    the record, but they are not the defect this organ exists to surface."""
    return [v for v in landed_verdicts(transport, repo_root) if v.met]


def main(argv: "list[str] | None" = None) -> int:
    parser = argparse.ArgumentParser(
        description="Advisory: an OPEN carrier whose own lands-via already resolves on main.")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="print landed-but-OPEN candidates (always exits 0)")
    check.add_argument("--repo-root", default=".", help="repo to read (default: cwd)")
    check.add_argument("--transport", default=None,
                       help="transport root (default: gen_handoff.transport_root())")
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve()
    transport = args.transport or gh.transport_root()
    if transport is None:
        print("carrier-landed-check: SKIPPED -- CLAUDE_PROMPTS_DIR is unresolved, nothing "
              "measured (a boundary is not a clean pass)")
        return 0
    # An explicit --transport that does not exist is the SAME boundary, not an empty
    # population: `_open_carriers`'s glob over a missing directory returns [] silently, which
    # would otherwise print "0 OPEN carrier(s) measured" -- indistinguishable from "the real
    # transport genuinely has none" (Codex terra review round 2, LANE-5B3-4-decision-debt).
    if not Path(transport).is_dir():
        print(f"carrier-landed-check: SKIPPED -- --transport {transport!r} does not exist, "
              "nothing measured (a boundary is not a clean pass)")
        return 0

    verdicts = landed_verdicts(transport, root)
    flagged = [v for v in verdicts if v.met]
    print(f"carrier-landed-check: {len(verdicts)} OPEN carrier(s) measured, "
          f"{len(flagged)} flagged landed-but-OPEN")
    for v in flagged:
        print(f"  - {v.render()}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
