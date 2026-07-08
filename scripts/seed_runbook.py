#!/usr/bin/env python3
"""seed_runbook.py — hub-side handoff-runbook seeder (#164 leg b).

The operator runbook `docs/handoffs/README.md` is **generic across repos of the same handoff
version** — the same file-roles / walkthrough / run-loop / rationale, differing only by the
repo name in the H1. This seeder writes (or idempotently refreshes) a SINGLE target repo's
`docs/handoffs/README.md` FROM one canonical source (the hub's own runbook), so a repo's copy
never has to be hand-copied and cannot silently rot.

**Single-target by construction (operator rider).** One invocation seeds exactly ONE repo — the
onboarding chat for a repo runs it for *that* repo. There is no fleet-batch mode here; the
cross-repo consumer FAN-OUT is deliberately deferred to the per-repo Wave-1/Wave-2 onboarding
arcs (ADR-41), so a hub session never writes into a consumer's tree (the don't-touch-consumers
guardrail). This session ships the MECHANISM + a hermetic test; it seeds no consumer.

Idempotency + frontmatter (RF): equivalence is on the runbook BODY only. A target's own leading
YAML frontmatter (e.g. a hub `last_reviewed` review stamp) is PRESERVED on update and never
injected on a fresh seed — so re-seeding a repo whose body already matches is a no-op `current`,
and the hub self-seeding itself never strips its own review stamp. The source's frontmatter is
dropped (it is the source repo's metadata, not the seed's).

Layer-2 / read-only w.r.t. tracked spine: writes ONLY `<target>/docs/handoffs/README.md`. Run
it FROM (or FOR) the repo being seeded; do not point it at a consumer from the hub — that is the
deferred fan-out, not this tool's sanctioned use.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import click

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
# The canonical source: the hub's own operator runbook.
_SOURCE_README = _REPO_ROOT / "docs" / "handoffs" / "README.md"
# Where the runbook lives inside any repo.
_RUNBOOK_REL = Path("docs") / "handoffs" / "README.md"

# The one repo-specific token in the otherwise-generic runbook: the H1's repo name in backticks.
_TITLE_RE = re.compile(r"(?m)^(# Handoffs — operator runbook \()`[^`]*`(\))")
# A leading YAML frontmatter block (--- ... ---), captured so it can be split off / preserved.
_FRONTMATTER_RE = re.compile(r"\A(---\n.*?\n---\n)(.*)\Z", re.DOTALL)


def _split_frontmatter(text: str) -> tuple[str, str]:
    """(frontmatter_block, body). Empty frontmatter string when the file carries none."""
    m = _FRONTMATTER_RE.match(text)
    return (m.group(1), m.group(2)) if m else ("", text)


def generalize_body(source_text: str, repo_name: str) -> str:
    """The desired seeded BODY: the source runbook minus its (source-repo) frontmatter, with the
    H1 repo-name token swapped to `repo_name`. Everything else is generic and copied verbatim, so
    a body edit to the source propagates identically to every seeded repo."""
    _, body = _split_frontmatter(source_text)
    return _TITLE_RE.sub(lambda m: f"{m.group(1)}`{repo_name}`{m.group(2)}", body)


@dataclass(frozen=True)
class SeedResult:
    status: str   # 'current' (no change) | 'seeded' (was absent) | 'updated' (body drifted)
    path: Path    # the target runbook path
    wrote: bool   # whether a write actually happened (False for a --check dry-run or 'current')


def seed_runbook(target_root: Path, *, source_readme: Path = _SOURCE_README,
                 repo_name: str | None = None, write: bool = True) -> SeedResult:
    """Seed / refresh ONE target repo's `docs/handoffs/README.md` from `source_readme`.

    `repo_name` defaults to `target_root.name` (the hub dir `.dev-knowledge` keeps its dot, so a
    hub self-seed is a no-op `current`). `write=False` is a dry-run: it classifies without
    touching disk. Body-equivalence classification (frontmatter-agnostic):
      - target absent            -> 'seeded'  (write the body, no frontmatter injected)
      - target body == desired   -> 'current' (no write)
      - target body differs      -> 'updated' (rewrite the body, PRESERVING the target's own
                                    leading frontmatter)
    """
    target_root = Path(target_root)
    name = repo_name if repo_name is not None else target_root.name
    desired_body = generalize_body(source_readme.read_text(encoding="utf-8"), name)
    target = target_root / _RUNBOOK_REL

    if target.exists():
        existing_fm, existing_body = _split_frontmatter(target.read_text(encoding="utf-8"))
        if existing_body == desired_body:
            return SeedResult("current", target, wrote=False)
        status, new_text = "updated", existing_fm + desired_body
    else:
        status, new_text = "seeded", desired_body

    if write:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_text, encoding="utf-8", newline="\n")
    return SeedResult(status, target, wrote=write)


@click.command()
@click.option("--target-root", "target_root", required=True, type=click.Path(file_okay=False),
              help="the ONE repo to seed (its docs/handoffs/README.md is written)")
@click.option("--source", "source", default=None, type=click.Path(dir_okay=False),
              help="canonical source runbook; default the hub's docs/handoffs/README.md")
@click.option("--repo-name", default=None,
              help="repo display name for the H1; default the target dir name")
@click.option("--check", is_flag=True, default=False,
              help="dry-run: classify (seeded/updated/current) without writing; exit 1 if it would change")
def main(target_root: str, source: str | None, repo_name: str | None, check: bool) -> None:
    """Seed a single repo's handoff runbook from the canonical hub source."""
    src = Path(source) if source else _SOURCE_README
    res = seed_runbook(Path(target_root), source_readme=src, repo_name=repo_name, write=not check)
    verb = "would " if check else ""
    click.echo(f"[seed-runbook] {res.status}: {verb}{'write' if res.status != 'current' else 'leave'} {res.path}")
    if check and res.status != "current":
        sys.exit(1)


if __name__ == "__main__":
    main()
