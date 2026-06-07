"""generate_floor.py — child methodology-floor generator (ADR-78 O2 Bounded Hybrid).

Emits a child repo's `CLAUDE-FLOOR.md` + `CLAUDE-FLOOR.md.sha256` from the ratified
content set in `templates/child-methodology-floor.md.tmpl`, and refreshes the hub's
canonical floor-hash reference `templates/child-methodology-floor.sha256` (the currency
anchor the `/ship` staleness gate reads).

OPERATOR-INVOKED ONLY (ADR-73 rollout-moment). This generator must NEVER be wired to a
hook or a schedule, and never makes autonomous cross-repo writes: a child commits its own
floor (operator runs the generator with `--out-dir <child>`, then commits in the child
repo). Strict Layer-2 invariant — no runtime/scheduled cross-repo writes from the hub.

Determinism: the template content IS the shipped floor body, byte-for-byte. The floor is
written with LF newlines and hashed over LF-normalized UTF-8 bytes, so the sidecar hash is
stable across platforms (Windows `autocrlf` cannot break it) and a re-run from the same
template produces an identical hash.

Binding token-ceiling measure (operator-pinned 2026-06-07): the conservative
`ceil(len(text) / 3.5)` chars heuristic is THE gate (deterministic, dependency-free). A
real tokenizer, if installed, is informational only and is NOT consulted here. The refusal
threshold is 1,500 tokens (ADR-78 §4); trim content, never the rule.

F5 self-containment (ADR-72 / ADR-75 `methodology_surface` zone): the floor must carry no
hub-INTERNAL artifact references (backlog ids, LESSONS/JOURNAL/TOKEN-LOG, PROPOSALS,
handoff/transcript paths, HANDOFF_PROCESS, hub ADR numbers) and no external URLs. A single
LABELED, optional escape-hatch naming the `.dev-knowledge` hub is permitted (ADR-78
Decision 1) — that is a documentation pointer, not a load-bearing runtime reference.

Forward note (#136): when the obsolescence-pass doctrine lands in the hub PLAYBOOK, the
floor absorbs its one-liner at the NEXT regeneration of the template — the floor never runs
ahead of ratified hub doctrine.

Usage:
    python scripts/generate_floor.py check                  # validate only; no writes
    python scripts/generate_floor.py generate               # refresh hub hash ref + print
    python scripts/generate_floor.py generate --out-dir ../corp-sca-time-automation
"""

from __future__ import annotations

import hashlib
import math
import re
import sys
from pathlib import Path

import click

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

TEMPLATE_PATH = _REPO_ROOT / "templates" / "child-methodology-floor.md.tmpl"
# Hub canonical floor-hash reference (the /ship staleness gate's currency anchor).
HUB_CANONICAL_SHA = _REPO_ROOT / "templates" / "child-methodology-floor.sha256"

FLOOR_FILENAME = "CLAUDE-FLOOR.md"
SIDECAR_FILENAME = "CLAUDE-FLOOR.md.sha256"

# Binding ceiling + binding token measure (operator-pinned). See module docstring.
FLOOR_TOKEN_CEILING = 1500
_TOKEN_CHARS_PER_TOKEN = 3.5

# F5 blacklist — hub-internal artifact tokens that MUST NOT surface in the floor
# (ADR-75 methodology_surface zone, T1 boundary). The bare `.dev-knowledge` hub name is
# deliberately ABSENT: a labeled optional escape-hatch is permitted (ADR-78 Decision 1).
F5_BLACKLIST: list[tuple[str, re.Pattern[str]]] = [
    ("backlog-id", re.compile(r"\[#\d+\]")),
    ("LESSONS.md", re.compile(r"LESSONS\.md", re.IGNORECASE)),
    ("JOURNAL.md", re.compile(r"JOURNAL\.md", re.IGNORECASE)),
    ("TOKEN-LOG", re.compile(r"TOKEN-LOG", re.IGNORECASE)),
    ("PROPOSALS log", re.compile(r"logs/PROPOSALS", re.IGNORECASE)),
    ("handoffs path", re.compile(r"docs/handoffs", re.IGNORECASE)),
    ("transcripts path", re.compile(r"docs/decisions/transcripts", re.IGNORECASE)),
    ("HANDOFF_PROCESS", re.compile(r"HANDOFF_PROCESS", re.IGNORECASE)),
    ("hub ADR ref", re.compile(r"\bADR-\d+\b", re.IGNORECASE)),
]

_URL_RE = re.compile(r"https?://", re.IGNORECASE)


def normalize(text: str) -> str:
    """LF-normalize so hashing is stable across platforms (autocrlf-proof)."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def estimate_tokens(text: str) -> int:
    """Binding token estimate: ceil(chars / 3.5) over LF-normalized text."""
    return math.ceil(len(normalize(text)) / _TOKEN_CHARS_PER_TOKEN)


def floor_sha256(text: str) -> str:
    """sha256 hexdigest over LF-normalized UTF-8 bytes (matches sidecar + hub ref)."""
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()


def f5_hits(text: str) -> list[str]:
    """Labels of any hub-internal artifact tokens found in the floor (empty = clean)."""
    return [label for label, pat in F5_BLACKLIST if pat.search(text)]


def url_hits(text: str) -> list[str]:
    """External URLs found in the floor (zero-URL policy; empty = clean)."""
    return _URL_RE.findall(text)


def render_floor(template_path: Path = TEMPLATE_PATH) -> str:
    """Read the template and return the floor body (LF-normalized, single trailing NL)."""
    body = normalize(template_path.read_text(encoding="utf-8"))
    return body if body.endswith("\n") else body + "\n"


def validate(floor: str) -> list[str]:
    """Return a list of blocking issues for the floor body (empty = valid)."""
    issues: list[str] = []
    tokens = estimate_tokens(floor)
    if tokens > FLOOR_TOKEN_CEILING:
        issues.append(
            f"token ceiling exceeded: {tokens} > {FLOOR_TOKEN_CEILING} "
            f"(binding measure ceil(chars/{_TOKEN_CHARS_PER_TOKEN})) — trim content, never the rule"
        )
    leaks = f5_hits(floor)
    if leaks:
        issues.append(f"F5 self-containment violation — hub-internal token(s) present: {leaks}")
    urls = url_hits(floor)
    if urls:
        issues.append(f"zero-URL policy violation — external URL(s) present: {urls}")
    return issues


def _write_text_lf(path: Path, text: str) -> None:
    """Write text with LF newlines (no platform translation) so on-disk bytes match the hash."""
    path.write_text(normalize(text), encoding="utf-8", newline="\n")


@click.group()
def cli() -> None:
    """Child methodology-floor generator (ADR-78). Operator-invoked only."""


@cli.command("check")
@click.option("--template", "template", default=None,
              help="Override template path (default templates/child-methodology-floor.md.tmpl).")
def cmd_check(template: str | None) -> None:
    """Validate the floor (ceiling, F5, URLs); print hash + token count. NO writes.

    Exits 1 if the floor violates any binding rule — usable as a hub-side gate.
    """
    tpath = Path(template) if template else TEMPLATE_PATH
    floor = render_floor(tpath)
    issues = validate(floor)
    tokens = estimate_tokens(floor)
    digest = floor_sha256(floor)
    click.echo(f"template: {tpath}")
    click.echo(f"tokens (binding chars/{_TOKEN_CHARS_PER_TOKEN}): {tokens} / ceiling {FLOOR_TOKEN_CEILING}")
    click.echo(f"sha256 (LF-normalized): {digest}")
    if issues:
        for i in issues:
            click.echo(f"  FAIL: {i}", err=True)
        sys.exit(1)
    click.echo("floor valid (ceiling OK, F5 clean, no external URLs).")


@cli.command("generate")
@click.option("--out-dir", "out_dir", default=None,
              help="Child repo dir to write CLAUDE-FLOOR.md + .sha256 into. "
                   "Omit to only refresh the hub canonical hash reference + print.")
@click.option("--template", "template", default=None,
              help="Override template path (default templates/child-methodology-floor.md.tmpl).")
def cmd_generate(out_dir: str | None, template: str | None) -> None:
    """Emit the floor + sidecar (and refresh the hub canonical hash reference).

    Refuses if the floor violates the token ceiling, F5 self-containment, or the
    zero-URL policy. Deterministic: same template → same hash. With --out-dir, writes
    CLAUDE-FLOOR.md + CLAUDE-FLOOR.md.sha256 into that child repo (operator commits them
    THERE). Always refreshes the hub's templates/child-methodology-floor.sha256 anchor.
    """
    tpath = Path(template) if template else TEMPLATE_PATH
    floor = render_floor(tpath)
    issues = validate(floor)
    if issues:
        click.echo("REFUSED — floor failed validation:", err=True)
        for i in issues:
            click.echo(f"  - {i}", err=True)
        sys.exit(1)

    digest = floor_sha256(floor)

    # Always refresh the hub canonical hash reference (idempotent — stable per template).
    _write_text_lf(HUB_CANONICAL_SHA, digest + "\n")
    try:
        ref_label = HUB_CANONICAL_SHA.relative_to(_REPO_ROOT)
    except ValueError:
        ref_label = HUB_CANONICAL_SHA
    click.echo(f"hub canonical hash refreshed: {ref_label} = {digest}")

    if out_dir:
        out = Path(out_dir)
        if not out.is_dir():
            click.echo(f"REFUSED — --out-dir is not a directory: {out}", err=True)
            sys.exit(1)
        _write_text_lf(out / FLOOR_FILENAME, floor)
        _write_text_lf(out / SIDECAR_FILENAME, digest + "\n")
        click.echo(f"wrote {out / FLOOR_FILENAME}")
        click.echo(f"wrote {out / SIDECAR_FILENAME}")
        click.echo(f"tokens (binding): {estimate_tokens(floor)} / {FLOOR_TOKEN_CEILING}")
        click.echo("Next: review the two files in the child, reference the floor from the child's "
                   "CLAUDE.md, and commit them IN the child repo.")
    else:
        click.echo("(no --out-dir; child artifacts not written — hub reference refreshed only)")


if __name__ == "__main__":
    cli()
