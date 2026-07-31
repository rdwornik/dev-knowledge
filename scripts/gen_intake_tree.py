#!/usr/bin/env python
"""gen_intake_tree.py -- [#383] wave 1: the ADR-109 section 4 generality proof on docs/intake/.

THE SECOND GOVERNED SURFACE. ADR-109 section 4 (transcribing ADR-107 section 6.2) withholds
the fleet desired-state contract's claim to GENERALITY until the engine pattern is *shown* to
extend to a second surface -- "per-item frontmattered `.md` files with byte-exact identity, a
residue manifest, and a green regen-and-diff round-trip -- demonstrated by a committed
round-trip proof, not by argument". Surface 1 was BACKLOG.md <-> tasks/ (gen_task_tree.py,
[#433]/[#439]). This module is surface 2.

THE DERIVATION RUNS MONOLITH -> MANIFEST. `docs/intake/README.md` is the SOURCE OF TRUTH and
stays hand-authored; `docs/intake/manifest.json` is DERIVED from it. This is deliberately
surface 1 at its [#433] STEP 1-2 (split) stage, NOT its post-[#439] flipped state: ADR-109
section 4 requires the round-trip proof, not a source-of-truth flip, and flipping intake would
change the governance semantics of docs/intake/ (architect ruling 2026-07-31). Because the
manifest is derived and gated by regen-and-diff, there is no two-copy drift hazard -- a
hand-edited residue file is exactly the failure mode this direction avoids.

The pair, and what each half carries:
  * `docs/intake/*.md` -- the per-item frontmattered files. THEY ALREADY EXISTED (that is why
    ADR-109 section 4 names this surface as the cheapest candidate). This module never writes,
    moves, or restyles one, and never touches a `status:` value.
  * `docs/intake/manifest.json` -- the residue carrier, in the ADR-107 section 5 finding-6
    shape: ORDERING + NON-MEMBER RESIDUE + HASH + DIRECTION. Every non-item physical line of
    README.md, in order, interleaved with per-item node pointers. This is what makes the
    monolith reversible.

HONEST LIMIT, recorded here and in the manifest header and the ADR-109 section 4 discharge
amendment (architect ruling 2026-07-31 -- the generality claim must be honest about what was
shown). The derivation ratio is INVERTED relative to surface 1: on BACKLOG.md the task lines
were the MAJORITY and residue the minority; here ~28 of README.md's ~256 lines are
item-derived and the remaining ~228 are residue. Section 4's bar is a byte-exact round-trip
plus a residue manifest, NOT a derivation ratio -- so this discharges the clause -- but the
proof shows less of the item corpus than surface 1's did, and that is stated rather than
glossed. What the round-trip does NOT cover is enumerated in the manifest's `not_captured`.

CLI verbs:
  --write       README.md -> manifest.json. Re-derive the residue carrier. Run after any edit
                to README.md or to any intake doc's frontmatter/title.
  --roundtrip   in-memory lossless proof: parse README.md, reassemble, assert byte-equality.
  --check       regen-and-diff against disk (the ADR-109 section 4 green round-trip; armed as
                an audit.py ship-gate leg). See `_cmd_check`.

Reassembly is byte-identical BY CONSTRUCTION (the line model preserves every original physical
line verbatim and splits only on "\\n", so the join is exactly reversible) and ASSERTED at
parse time -- `parse_readme` REFUSES to return a model that does not reassemble to its own
input, the same self-checking contract as gen_task_tree.parse_backlog.

The per-item projection is NOT redefined here: `render_row` / `collect_intakes` are imported
from gen_intake_index, so one projection serves both the existing index hook and this
round-trip and the two cannot drift apart.

Loose top-level module BY DESIGN (mirrors gen_intake_index.py / gen_audit_index.py): no
codemap node, so editing it never forces an ARCHITECTURE codemap regen. Layer-2 read-only
(ADR-28/36): writes NOTHING except docs/intake/manifest.json under --write; drives no state in
any other repo and deletes nothing.

OUTPUT IS ASCII-ONLY (gotchas skill, last triggered 2026-07-10): README.md section 5 contains
"->" as U+2192, which is NOT in cp1252, so echoing raw source lines to a Windows console would
raise UnicodeEncodeError on exactly the error path that most needs a readable message. Drift
reports name what diverged; they never dump raw source lines. The manifest is likewise written
with ensure_ascii=True, so the artifact on disk is pure ASCII with LF endings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:  # importable as a script AND as a module
    sys.path.insert(0, str(_SCRIPTS_DIR))

from gen_intake_index import (  # noqa: E402  (path bootstrap must precede the import)
    _END_MARKER,
    _START_MARKER,
    collect_intakes,
    render_row,
)

_REPO_ROOT = _SCRIPTS_DIR.parent
_INTAKE_DIR = _REPO_ROOT / "docs" / "intake"
_SOURCE = _INTAKE_DIR / "README.md"
_MANIFEST = _INTAKE_DIR / "manifest.json"

SCHEMA_ID = "intake-residue-manifest/v1"

# An item row INSIDE the generated block. Scoped to the block deliberately: a doctrine line
# elsewhere in README.md that happened to share this shape must stay RESIDUE, never become a
# node. Mirrors gen_intake_index.render_row's output shape.
_ITEM_ROW_RE = re.compile(r"^- \[(?:#\d+|MISSING-ID)\]\(([^)]+)\)")

# The keys the monolith projection consumes. Every OTHER frontmatter key an intake doc carries
# is un-captured by the split and is enumerated in the manifest's `not_captured` (AC-4).
_PROJECTED_FM_KEYS = ("intake-id", "status")


@dataclass(frozen=True)
class Node:
    """One element of the ordered stream. Exactly one of the two kinds:

    kind="line" -> `value` is a residue line, carried VERBATIM (no trailing newline).
    kind="item" -> `value` is an intake filename; the line is re-derived from that file.
    """

    kind: str
    value: str


@dataclass(frozen=True)
class Model:
    """The lossless line model: every physical line of README.md, in order."""

    nodes: tuple[Node, ...]

    def reassemble(self, intake_dir: Path | None = None) -> str:
        """Rebuild the monolith text from residue + freshly-rendered item rows."""
        rows = _rows_by_filename(intake_dir)
        out: list[str] = []
        for node in self.nodes:
            if node.kind == "line":
                out.append(node.value)
            else:
                if node.value not in rows:
                    raise RuntimeError(
                        f"manifest references intake file '{node.value}', which is not on "
                        f"disk under docs/intake/ -- regenerate: "
                        f"python scripts/gen_intake_tree.py --write")
                out.append(rows[node.value])
        return "\n".join(out)


def _rows_by_filename(intake_dir: Path | None = None) -> dict[str, str]:
    """{filename: rendered index row} for every intake doc, via the SHARED projection."""
    return {
        filename: render_row(intake_id, filename, title)
        for _status, intake_id, filename, title in collect_intakes(intake_dir)
    }


def _status_by_filename(intake_dir: Path | None = None) -> dict[str, str]:
    """{filename: frontmatter status} for every intake doc.

    Status is a PROJECTED key that does NOT appear in the rendered row -- it determines the
    block's GROUPING, and the group headings are carried as residue. So a status-only change
    moves a row between groups in the generated block while leaving the row text and every
    residue line untouched, and reassembly alone cannot see it (codex-review HIGH, 2026-07-31,
    reproduced before fixing: a SEED -> ACCEPTED flip changed the generated block yet left the
    check green). Recording status per item node is what closes that hole.
    """
    return {filename: status for status, _id, filename, _title in collect_intakes(intake_dir)}


def parse_readme(text: str) -> Model:
    """Classify every physical line of README.md into the ordered node stream.

    Splits ONLY on "\\n" (never str.splitlines, whose extra Unicode line boundaries --
    \\x0b, \\x0c, U+2028, U+0085 -- would not round-trip), so "\\n".join is exactly the
    inverse. REFUSES to return a model that does not reassemble to its own input.
    """
    lines = text.split("\n")
    in_block = False
    nodes: list[Node] = []
    for line in lines:
        if line == _START_MARKER:
            in_block, nodes = True, [*nodes, Node("line", line)]
            continue
        if line == _END_MARKER:
            in_block, nodes = False, [*nodes, Node("line", line)]
            continue
        m = _ITEM_ROW_RE.match(line) if in_block else None
        nodes.append(Node("item", m.group(1)) if m else Node("line", line))

    model = Model(tuple(nodes))
    # Parse-time self-check, STATED FOR EXACTLY WHAT IT PROVES (codex-review HIGH,
    # 2026-07-31: the earlier docstring claimed this refused any model that "does not
    # reassemble to its own input", which was TAUTOLOGICAL for item nodes -- they were
    # checked by looking their own source line back up, so a row whose re-derivation
    # differed from disk still passed). This assertion covers the LINE MODEL only: residue is
    # verbatim and ordering is preserved, so a pure-residue rebuild must equal the input.
    # Whether an item node RE-DERIVES to its original row is a disk question, enforced at
    # emit time by `_cmd_write` and at gate time by `evaluate` -- not here.
    rebuilt = "\n".join(
        node.value if node.kind == "line" else _placeholder(node, lines) for node in model.nodes
    )
    if rebuilt != text:
        raise RuntimeError(
            "line model is not lossless -- refusing to return it (this is a bug in "
            "gen_intake_tree.parse_readme, not in the source document)")
    return model


def _placeholder(node: Node, lines: list[str]) -> str:
    """The ORIGINAL physical line an item node was parsed from -- used only by the parse-time
    losslessness assertion, so the line model is proven independently of disk re-derivation."""
    for line in lines:
        m = _ITEM_ROW_RE.match(line)
        if m and m.group(1) == node.value:
            return line
    raise RuntimeError(f"internal: no source line for item node {node.value!r}")


def _off_projection_keys(intake_dir: Path | None = None) -> dict[str, list[str]]:
    """{filename: [frontmatter keys present but NOT projected into the monolith]}.

    The AC-4 residue enumeration for the item side. Read-only; never rewrites frontmatter.
    """
    from gen_intake_index import _parse_frontmatter  # local: keeps the module's public API thin

    intake_dir = intake_dir if intake_dir is not None else _INTAKE_DIR
    out: dict[str, list[str]] = {}
    for p in sorted(intake_dir.glob("*.md")):
        if p.name == "README.md":
            continue
        fm = _parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        extra = sorted(k for k in fm if k not in _PROJECTED_FM_KEYS)
        if extra:
            out[p.name] = extra
    return out


def build_manifest(text: str, model: Model, intake_dir: Path | None = None) -> dict:
    """The residue-manifest object: ORDERING + NON-MEMBER RESIDUE + HASH + DIRECTION
    (the ADR-107 section 5 finding-6 residue-carrier type)."""
    item_nodes = [n for n in model.nodes if n.kind == "item"]
    line_nodes = [n for n in model.nodes if n.kind == "line"]
    total = len(model.nodes)
    statuses = _status_by_filename(intake_dir)
    return {
        "schema": SCHEMA_ID,
        # DIRECTION -- which side is source. See the module docstring: split-only, not flipped.
        "direction": "derived-from",
        "source": "docs/intake/README.md",
        "generator": "scripts/gen_intake_tree.py",
        # HASH -- tamper/staleness anchor over the exact source bytes.
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "honest_limit": {
            "statement": (
                "ADR-109 section 4 is discharged by a byte-exact round-trip plus a residue "
                "manifest, NOT by a derivation ratio. This surface's ratio is INVERTED "
                "relative to surface 1 (BACKLOG.md <-> tasks/), where task lines were the "
                "majority and residue the minority. Recorded so the generality claim is "
                "honest about what was shown."),
            "item_derived_lines": len(item_nodes),
            "residue_lines": len(line_nodes),
            "total_lines": total,
            "surface_1_comparison": "inverted -- surface 1 was majority item-derived",
        },
        # AC-4 -- everything the split does NOT capture.
        "not_captured": {
            "intake_document_bodies": (
                "The unstructured wave-prose inside each docs/intake/*.md is not part of the "
                "monolith and is not carried here. The split projects only the frontmatter "
                "keys listed in `projected_frontmatter_keys` plus the `# ` title. Bodies are "
                "deliberately NOT hashed: that would couple this manifest to every intake "
                "body edit and RED the gate on unrelated work, buying no round-trip strength."),
            "projected_frontmatter_keys": list(_PROJECTED_FM_KEYS),
            "off_projection_frontmatter_keys": _off_projection_keys(intake_dir),
            "derived_lines_carried_as_residue": (
                "The block's count line and its `### STATUS (n)` group headings are generated "
                "by gen_intake_index but are carried here VERBATIM as residue, not re-derived. "
                "A status-only change therefore moves a row between groups WITHOUT altering "
                "any row text or residue line, so reassembly alone cannot see it -- which is "
                "why each item node records its projected `status` and the item-set leg "
                "compares it against disk. That leg, not the residue, is what REDs --check on "
                "a status change; remedy is to regenerate README.md (python "
                "scripts/gen_intake_index.py --write) and then this carrier."),
        },
        # ORDERING + NON-MEMBER RESIDUE -- the stream itself. An item node records the
        # projected STATUS alongside the filename: status never appears in the row text (it
        # drives grouping, and headings are residue), so without it a status-only change is
        # invisible to reassembly -- see `_status_by_filename`.
        "nodes": [
            {"t": "line", "v": n.value} if n.kind == "line"
            else {"t": "item", "file": n.value, "status": statuses.get(n.value, "")}
            for n in model.nodes
        ],
    }


def manifest_to_model(manifest: dict) -> Model:
    """The inverse of build_manifest's `nodes` stream."""
    nodes: list[Node] = []
    for raw in manifest.get("nodes", []):
        if raw.get("t") == "line":
            nodes.append(Node("line", raw.get("v", "")))
        elif raw.get("t") == "item":
            nodes.append(Node("item", raw.get("file", "")))
        else:
            raise RuntimeError(f"unknown node type {raw.get('t')!r} in {_MANIFEST.name}")
    return Model(tuple(nodes))


def _dump(manifest: dict) -> str:
    """Deterministic, pure-ASCII, LF-terminated JSON text."""
    return json.dumps(manifest, indent=2, ensure_ascii=True, sort_keys=False) + "\n"


def _read_source() -> str:
    """README.md decoded STRICTLY -- data that gets round-tripped must fail LOUDLY on a bad
    byte rather than bake in a U+FFFD replacement (gotchas skill, the silent-corruption class)."""
    return _SOURCE.read_bytes().decode("utf-8")


def _cmd_write() -> int:
    if not _SOURCE.exists():
        print(f"error: {_SOURCE.name} not found", file=sys.stderr)
        return 2
    text = _read_source()
    model = parse_readme(text)
    manifest = build_manifest(text, model, None)
    # REFUSE to emit a carrier that fails its own round-trip (codex-review HIGH, 2026-07-31).
    # `parse_readme`'s assertion covers the line model only; this is the disk-side check, and
    # it must run BEFORE the write so a bad carrier is never persisted for `--check` to find.
    rebuilt = model.reassemble()
    if rebuilt != text:
        print("gen_intake_tree: REFUSING to write -- the parsed model does not re-derive "
              "README.md from the on-disk intake files", file=sys.stderr)
        print(_describe_divergence(text, rebuilt), file=sys.stderr)
        return 1
    _MANIFEST.write_text(_dump(manifest), encoding="utf-8", newline="\n")
    print(f"gen_intake_tree: wrote {_MANIFEST.relative_to(_REPO_ROOT).as_posix()} "
          f"({manifest['honest_limit']['item_derived_lines']} item node(s), "
          f"{manifest['honest_limit']['residue_lines']} residue line(s))")
    return 0


def _cmd_roundtrip() -> int:
    """In-memory lossless proof over the source: parse -> reassemble -> assert byte-equality."""
    if not _SOURCE.exists():
        print(f"error: {_SOURCE.name} not found", file=sys.stderr)
        return 2
    text = _read_source()
    rebuilt = parse_readme(text).reassemble()
    if rebuilt == text:
        print(f"gen_intake_tree: roundtrip OK -- {len(text.encode('utf-8'))} bytes "
              f"({len(text)} chars) reassembled byte-exactly")
        return 0
    print("gen_intake_tree: ROUNDTRIP FAILED -- reassembly does not equal the source",
          file=sys.stderr)
    print(_describe_divergence(text, rebuilt), file=sys.stderr)
    return 1


def _describe_divergence(expected: str, actual: str) -> str:
    """An ASCII-ONLY account of the first divergence. Never echoes source content: README.md
    carries U+2192, and stdout is cp1252 on Windows (gotchas skill)."""
    exp, act = expected.split("\n"), actual.split("\n")
    for i, (e, a) in enumerate(zip(exp, act), start=1):
        if e != a:
            return (f"  first divergence at line {i}: "
                    f"expected {len(e)} char(s), got {len(a)} char(s) "
                    f"(content withheld -- non-ASCII source, ASCII-only reporting)")
    if len(exp) != len(act):
        return f"  line count differs: source has {len(exp)}, reassembly has {len(act)}"
    return "  byte-length differs with no line-level divergence (trailing-newline class)"


REMEDY = "python scripts/gen_intake_tree.py --write"

OK, DRIFT, MALFORMED = "ok", "drift", "malformed"


def evaluate(intake_dir: Path | None = None) -> tuple[str, list[str]]:
    """THE regen-and-diff verdict (ADR-109 section 4's "green regen-and-diff round-trip"),
    as a PURE function -- no printing, no writing, no exit codes.

    Four independent legs, each a distinct failure mode:
      1. the carrier exists, parses as UTF-8 JSON, and declares this schema  -> MALFORMED
      2. it is not STALE vs README.md (regen-and-diff over the exact bytes)  -> DRIFT
      3. THE ROUND-TRIP -- README.md rebuilds from the node stream + the on-disk intake files
         BYTE-FOR-BYTE                                                       -> DRIFT
      4. `source_sha256` matches README.md's exact UTF-8 bytes               -> DRIFT

    Returns (verdict, reasons) where verdict is OK / DRIFT / MALFORMED and every reason is an
    ASCII sentence. SINGLE DEFINITION of the legs, shared by the CLI (`--check`) and the
    audit.py ship-gate leg, so the two can never drift into disagreeing about what coherent
    means -- the duplication this repo gates against.

    All reasons are ASCII: README.md carries U+2192 and Windows stdout is cp1252, so raw
    source content is never echoed (gotchas skill). Read-only.
    """
    intake_dir = intake_dir if intake_dir is not None else _INTAKE_DIR
    source, manifest_path = intake_dir / "README.md", intake_dir / "manifest.json"

    for name, path in (("README.md", source), ("manifest.json", manifest_path)):
        if not path.exists():
            return MALFORMED, [f"{name} is missing"]

    try:
        text = source.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return MALFORMED, ["README.md is not strict UTF-8"]

    try:
        manifest_text = manifest_path.read_bytes().decode("utf-8")
        manifest = json.loads(manifest_text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return MALFORMED, ["manifest.json is not valid UTF-8 JSON"]

    malformed = _malformed_reason(manifest)
    if malformed:
        return MALFORMED, [malformed]

    try:
        expected_manifest = _dump(build_manifest(text, parse_readme(text), intake_dir))
        model = manifest_to_model(manifest)
    except (OSError, UnicodeDecodeError, RuntimeError, TypeError, ValueError):
        return MALFORMED, ["source or manifest cannot be derived"]

    reasons: list[str] = []
    reasons += _item_set_divergences(manifest, intake_dir)
    if manifest_text != expected_manifest:
        reasons.append(
            f"manifest is stale versus README.md (expected {len(expected_manifest)} char(s), "
            f"got {len(manifest_text)} char(s));{_describe_divergence(expected_manifest, manifest_text)}")

    try:
        rebuilt = model.reassemble(intake_dir)
    except (OSError, UnicodeDecodeError, RuntimeError):
        reasons.append("round-trip cannot reassemble the manifest node stream from on-disk "
                       "intake files")
    else:
        if rebuilt != text:
            reasons.append(f"round-trip README.md divergence;{_describe_divergence(text, rebuilt)}")

    if manifest.get("source_sha256") != hashlib.sha256(text.encode("utf-8")).hexdigest():
        reasons.append("source_sha256 does not match README.md exact UTF-8 bytes")

    if reasons:
        return DRIFT, reasons
    return OK, [f"{len(manifest['nodes'])} node(s), {len(text.encode('utf-8'))} README.md byte(s)"]


def _cmd_check() -> int:
    """Read-only regen-and-diff CLI over `evaluate`. Exit 0 clean / 1 drift / 2
    missing-or-malformed. Every non-zero path names the remedy.

    Leg logic produced by Codex (gpt-5.6-terra) under the [#383] wave-1 producer lane;
    verified by CC, which refactored the four legs into the shared `evaluate` above so the
    CLI and the audit leg cannot diverge. See the arc audit artifact for builder-lane evidence.
    """
    verdict, reasons = evaluate()
    if verdict == OK:
        print(f"gen_intake_tree: check OK -- {reasons[0]}")
        return 0
    for reason in reasons:
        print(f"gen_intake_tree: check FAILED -- {reason}", file=sys.stderr)
    print(f"gen_intake_tree: remedy: run {REMEDY}", file=sys.stderr)
    return 2 if verdict == MALFORMED else 1


def _item_set_divergences(manifest: dict, intake_dir: Path | None = None) -> list[str]:
    """The ITEM-SET integrity leg: the carrier's item nodes must match `collect_intakes()`
    ONE-FOR-ONE -- non-empty, duplicate-free, same filenames, same projected statuses.

    Without this leg the gate can be satisfied by deleting exactly what it exists to prove
    (codex-review HIGH, 2026-07-31, reproduced before fixing: stripping every item row from
    the marker block and regenerating yields an all-residue carrier with ZERO item nodes that
    round-trips perfectly and reports GREEN). Reassembly alone cannot catch that, because a
    carrier with no item nodes is trivially self-consistent -- the same "a gate must not be
    satisfiable by removing its own subject" rule the `tasks/` gate carries.

    Also the only leg that sees a STATUS-only change (see `_status_by_filename`).
    """
    items = [n for n in manifest.get("nodes", []) if n.get("t") == "item"]
    on_disk = _status_by_filename(intake_dir)
    reasons: list[str] = []

    if not items:
        reasons.append(f"carrier has ZERO item nodes while {len(on_disk)} intake doc(s) are on "
                       f"disk -- the split is not represented at all")
        return reasons

    files = [n.get("file", "") for n in items]
    dupes = sorted({f for f in files if files.count(f) > 1})
    if dupes:
        reasons.append(f"duplicate item node(s): {', '.join(dupes)}")

    missing = sorted(set(on_disk) - set(files))
    extra = sorted(set(files) - set(on_disk))
    if missing:
        reasons.append(f"intake doc(s) on disk with no item node: {', '.join(missing)}")
    if extra:
        reasons.append(f"item node(s) with no intake doc on disk: {', '.join(extra)}")

    drifted = sorted(
        f"{n['file']} (carrier {n.get('status', '')!r} vs disk {on_disk[n['file']]!r})"
        for n in items
        if n.get("file") in on_disk and n.get("status", "") != on_disk[n["file"]]
    )
    if drifted:
        reasons.append(f"projected status drift: {'; '.join(drifted)}")
    return reasons


def _malformed_reason(manifest: object) -> str | None:
    """An ASCII reason string when the parsed manifest is structurally unusable, else None.
    Shared by the CLI and the audit leg so both classify malformation identically."""
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA_ID:
        return "manifest.json has missing or wrong schema"
    nodes = manifest.get("nodes")
    if not isinstance(nodes, list):
        return "manifest.json has no valid node stream"
    for node in nodes:
        if not isinstance(node, dict):
            return "manifest.json has a malformed node"
        if node.get("t") == "line" and isinstance(node.get("v"), str):
            continue
        if node.get("t") == "item" and isinstance(node.get("file"), str):
            continue
        return "manifest.json has an unknown or malformed node type"
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gen_intake_tree",
        description=("Split docs/intake/README.md into per-item nodes + a residue manifest "
                     "(ADR-109 section 4 generality proof)"))
    parser.add_argument("--write", action="store_true",
                        help="re-derive docs/intake/manifest.json from README.md")
    parser.add_argument("--roundtrip", action="store_true",
                        help="in-memory lossless proof over README.md")
    parser.add_argument("--check", action="store_true",
                        help="regen-and-diff against disk (default action)")
    args = parser.parse_args(argv)
    if args.write:
        return _cmd_write()
    if args.roundtrip:
        return _cmd_roundtrip()
    return _cmd_check()


if __name__ == "__main__":
    sys.exit(main())
