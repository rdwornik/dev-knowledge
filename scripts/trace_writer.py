#!/usr/bin/env python3
"""trace_writer.py — Lane h0: every dispatch leaves a readable trace under logs/prompts/.

WHY THIS EXISTS. A cloud/codespace dispatch (`protocols/STANDING_RULINGS.md` Q5, the
receipt gate) already produces every fact a trace needs: the contract it ran, the
generated runner (`dispatch-run.sh`), and `receipt.json`. None of those three land
anywhere a later reader can find them together — the receipt is pulled back to a temp
path and discarded, the runner is gitignored dispatch scaffolding, and the contract is
the only one already committed. This module writes the four into ONE readable file per
dispatch, plus the outcome and the model/effort tier, so a reader gets the whole story
without reassembling it from three ephemeral places.

NO NEW FORMAT (`LANE-h0-trace.md` "What NOT to do"). This is concatenation, not
distillation: each of the five parts is the source material, verbatim or lightly
labelled, never a computed summary. `receipt.json`'s own fields are reused as-is —
no field is renamed, dropped, or re-derived.

ONE DISPATCH, ONE FILE. The output path is `<out_dir>/<date>-<lane>.md`, so a second
call for the same (date, lane) pair overwrites rather than accumulating a sibling —
there is exactly one trace per dispatch by construction, not by a de-duplication step.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import click

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_OUT_DIR = _REPO_ROOT / "logs" / "prompts"


def _read(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def render_trace(*, lane: str, contract_text: str, skeleton_text: str,
                  receipt_text: str, outcome: str, model: str, effort: str) -> str:
    """The five-part trace body, in the order the contract names them.

    Pure string assembly on already-read text — no file I/O, so the shape is
    directly testable against fixture strings without a filesystem.
    """
    return (
        f"# Dispatch trace — {lane}\n\n"
        "## 1. Contract AS SENT\n\n"
        f"```markdown\n{contract_text.rstrip()}\n```\n\n"
        "## 2. Skeleton run\n\n"
        f"```bash\n{skeleton_text.rstrip()}\n```\n\n"
        "## 3. receipt.json\n\n"
        f"```json\n{receipt_text.rstrip()}\n```\n\n"
        "## 4. Outcome\n\n"
        f"{outcome.rstrip()}\n\n"
        "## 5. Model / effort\n\n"
        f"- model: {model}\n"
        f"- effort: {effort}\n"
    )


def write_trace(*, lane: str, contract_path: Path, skeleton_path: Path,
                 receipt_path: Path, outcome: str, model: str, effort: str,
                 out_dir: Path = _DEFAULT_OUT_DIR, on: date | None = None) -> Path:
    """Write the one trace file for this dispatch and return its path.

    `on` defaults to today; passed explicitly by tests so the filename is
    deterministic rather than depending on wall-clock date.
    """
    on = on or date.today()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    body = render_trace(
        lane=lane,
        contract_text=_read(contract_path),
        skeleton_text=_read(skeleton_path),
        receipt_text=_read(receipt_path),
        outcome=outcome,
        model=model,
        effort=effort,
    )
    out_path = out_dir / f"{on.isoformat()}-{lane}.md"
    out_path.write_text(body, encoding="utf-8", newline="\n")
    return out_path


@click.command()
@click.option("--lane", required=True, help="lane slug, e.g. lane-h0-trace")
@click.option("--contract", "contract_path", required=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--skeleton", "skeleton_path", required=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help="the generated runner, e.g. dispatch-run.sh")
@click.option("--receipt", "receipt_path", required=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--outcome", required=True,
              help="branch, commits, targeted tests -- free text")
@click.option("--model", required=True)
@click.option("--effort", required=True)
@click.option("--out-dir", default=str(_DEFAULT_OUT_DIR),
              type=click.Path(file_okay=False, path_type=Path))
def main(lane: str, contract_path: Path, skeleton_path: Path, receipt_path: Path,
          outcome: str, model: str, effort: str, out_dir: Path) -> None:
    """Write one dispatch trace under `logs/prompts/`."""
    path = write_trace(
        lane=lane, contract_path=contract_path, skeleton_path=skeleton_path,
        receipt_path=receipt_path, outcome=outcome, model=model, effort=effort,
        out_dir=out_dir,
    )
    click.echo(f"trace written: {path}")


if __name__ == "__main__":
    main()
