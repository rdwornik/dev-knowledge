#!/usr/bin/env python
"""lane_cost.py -- the lane's OTHER cost, in tokens and in money (`[#751]`).

`[#675]` bought the merge an itemised receipt in MINUTES. A lane's minutes are half of what it
spends; the other half is tokens, and until now nothing in this repo converted the token figures
the transcripts already carry into a number anyone could act on. `logs/TOKEN-LOG.md` holds a
hand-pasted weekly `ccusage` snapshot -- fleet-wide, by calendar week, last fed 2026-08-04 -- and
a weekly fleet total cannot answer "what did THIS lane cost" or "what did batch Y cost". This
module answers both, per lane and per model, and it does so from figures that already exist
rather than from a new instrument.

=================================================================================================
WHERE THE NUMBERS COME FROM, AND WHAT THAT MAKES THEM
=================================================================================================

TOKENS are read out of the Claude Code session transcripts under `~/.claude/projects/<slug>/
*.jsonl`. Every assistant turn carries `message.model` and `message.usage` with four counts --
`input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`. This
module reads them and adds nothing: no sampling, no estimation, no tokeniser. That is the
contract's "the transcripts' EXISTING token figures", and it is why this is a reader rather than
an instrument -- an instrument would need wiring at every call site and would measure only what
it was wired into, which is the complaint `merge_receipt` files against unrecorded steps.

MONEY is those counts times the rates declared in `ecosystem/provider-registry.yaml`, resolved
through `provider_registry.resolve_rate` on every call. **There is no rate literal in this
module**, and that is a property its tests enforce rather than a convention: the same tokens
priced against two registries must produce two different dollar figures, which no hard-coded or
cached table can satisfy.

=================================================================================================
THE HONEST LIMITS, stated so a figure from here is not over-read
=================================================================================================

  * **A CLIENT-SIDE ESTIMATE, not a bill.** These are list prices times counted tokens. They do
    not know about a subscription, a plan allowance, a discount, a partner route's separate
    pricing, or a failed request that was never charged. The right use is comparison -- this
    lane against that one, this batch against the last -- not reconciliation against an invoice.
  * **UNPRICED IS NOT FREE, and it is never summed in.** A model with no `rates:` row refuses
    (`RateUnavailable`) and lands in `unpriced()` carrying its full token count. Every rendering
    shows it. A reader must always be able to say how much of a total is missing, because a
    total that silently absorbed an unpriced model would be exactly the plausible-value failure
    `[#675]` was filed about.
  * **IT COSTS WHAT IT CAN SEE.** A background or subagent lane's transcript is filed under its
    LAUNCHING session's directory, not its own (`gen_handoff._worktree_is_owned` records the
    same fact for ownership). So a lane whose slug matches no project directory reports NO
    TRANSCRIPT -- explicitly, by name -- and never $0.00. Attributing an unfound lane to zero
    would make the cheapest lane in any report the one nobody could measure.
  * **A REPEATED TURN IS ONE TURN.** Transcripts carry the same assistant message on more than
    one line (measured on this host: adjacent lines with byte-identical `usage`). Summing them
    doubles the bill, and a doubled bill is indistinguishable from a busy day, so turns are
    de-duplicated on `message.id` (falling back to the record `uuid`).

=================================================================================================
WHY THE COST ROW IS ITS OWN LEDGER AND NOT A FIELD ON THE MERGE RECEIPT
=================================================================================================

The natural home for this is a `cost` block inside the `logs/MERGE-RECEIPTS.jsonl` row, written
by `merge_receipt.close`. It is NOT written there, and the reason is a recorded batch ruling
rather than a design preference: `scripts/merge_receipt.py` is `[#750]`'s SOLE-OWNED file for
batch Y ("`[#752]` is sequenced behind it on that file and does not open it until this lane's
branch has landed"), and `[#750]` is rewriting its completeness predicate concurrently with this
lane. Opening it here would be an undeclared third claim on a module being restructured.

So the cost lives in `logs/LANE-COSTS.jsonl`, keyed by the SAME slug, and `receipt` joins the
two into one view -- the lane receipt, carrying minutes AND tokens AND USD. The join is a read;
neither ledger writes the other. Both are append-only in the ADR-29/ADR-39 sense: `append_cost`
adds one line and never rewrites an earlier one.

The one-call seam that would fold this into the receipt row itself is written out as a proposed
diff in this lane's end-of-lane artifact, for `[#750]`'s owner or the integrator to take after
that branch lands. It is deliberately left proposed rather than applied.

=================================================================================================
CALL SURFACE
=================================================================================================

    uv run --locked python scripts/lane_cost.py lane   --slug lane-y-751-cost-in-money --batch Y
    uv run --locked python scripts/lane_cost.py close  --slug lane-y-751-cost-in-money --batch Y
    uv run --locked python scripts/lane_cost.py receipt --slug lane-y-751-cost-in-money
    uv run --locked python scripts/lane_cost.py report
    uv run --locked python scripts/lane_cost.py token-log --append
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Sequence

import click

# The dual package/script import shim: `from scripts import lane_cost` (repo root on sys.path)
# and `import lane_cost` (scripts/ on sys.path) are both supported entry points, and a bare
# sibling import breaks the first while looking like an absent module.
try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import provider_registry as pr
except ImportError:  # pragma: no cover
    import provider_registry as pr

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("lane-cost")

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent

#: The durable cost ledger. Committed, append-only, one JSON object per closed lane cost --
#: the `[#395]` naming (UPPERCASE-KEBAB, extension honest to the format) and the
#: `logs/MERGE-RECEIPTS.jsonl` / `logs/TOKEN-LOG.md` class.
COST_LEDGER_RELPATH = "logs/LANE-COSTS.jsonl"
#: The minutes ledger this one is joined against. Read only, never written here.
RECEIPT_LEDGER_RELPATH = "logs/MERGE-RECEIPTS.jsonl"
#: The fleet-wide weekly usage record this module can feed. See `token_log_entry`.
TOKEN_LOG_RELPATH = "logs/TOKEN-LOG.md"

#: Claude Code's session store. One directory per project cwd, one `.jsonl` per session.
DEFAULT_SESSIONS_ROOT = Path.home() / ".claude" / "projects"

#: A turn naming this model names no model: `<synthetic>` turns are harness-generated and carry
#: no vendor call. Counting them would invent a model row that can never be priced.
_NOT_A_MODEL = frozenset({"<synthetic>", "", "unknown"})


class CostError(RuntimeError):
    """A lane cost that cannot be read, computed or recorded."""


# --- token counts ------------------------------------------------------------------------

@dataclass(frozen=True)
class TokenUsage:
    """Four counts and the number of calls that produced them.

    CACHE TOKENS ARE FIRST-CLASS, not a footnote. On this repo's own transcripts cache reads
    outnumber fresh input tokens by orders of magnitude, so a usage record that folded them
    into `input_tokens` -- or dropped them, as `logs/TOKEN-LOG.md` does "for comparability" --
    would misstate the bill by more than the bill.
    """

    input_tokens: int = 0
    output_tokens: int = 0
    cache_write_tokens: int = 0
    cache_read_tokens: int = 0
    calls: int = 0

    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cache_write_tokens=self.cache_write_tokens + other.cache_write_tokens,
            cache_read_tokens=self.cache_read_tokens + other.cache_read_tokens,
            calls=self.calls + other.calls,
        )

    @property
    def total_tokens(self) -> int:
        return (self.input_tokens + self.output_tokens
                + self.cache_write_tokens + self.cache_read_tokens)

    def to_dict(self) -> dict:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_write_tokens": self.cache_write_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "calls": self.calls,
            "total_tokens": self.total_tokens,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TokenUsage":
        return cls(
            input_tokens=int(data.get("input_tokens", 0)),
            output_tokens=int(data.get("output_tokens", 0)),
            cache_write_tokens=int(data.get("cache_write_tokens", 0)),
            cache_read_tokens=int(data.get("cache_read_tokens", 0)),
            calls=int(data.get("calls", 0)),
        )


def _usage_from_turn(usage: dict) -> TokenUsage:
    """One turn's four counts, read under the transcript's own key names.

    The wire names are the API's (`cache_creation_input_tokens` / `cache_read_input_tokens`);
    this module's names say what they cost (`cache_write` / `cache_read`). The translation is
    here, once, so nothing downstream has to know the wire spelling.
    """
    return TokenUsage(
        input_tokens=int(usage.get("input_tokens") or 0),
        output_tokens=int(usage.get("output_tokens") or 0),
        cache_write_tokens=int(usage.get("cache_creation_input_tokens") or 0),
        cache_read_tokens=int(usage.get("cache_read_input_tokens") or 0),
        calls=1,
    )


def read_transcript_usage(path: Path, seen: Optional[set[str]] = None) -> dict[str, TokenUsage]:
    """`{model: usage}` for one `.jsonl` transcript.

    `seen` carries de-duplication ACROSS files when a caller passes one set for a whole lane:
    a session resumed into a second file replays turns, and a turn counted twice is spend
    invented twice.

    A malformed line is WARNED and skipped rather than fatal -- the same posture
    `merge_receipt.read_ledger` takes, and for the same reason: one bad line must not make
    every good one unreadable.
    """
    out: dict[str, TokenUsage] = {}
    if seen is None:
        seen = set()
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        logger.warning("transcript unreadable, skipped: %s (%s)", path, exc)
        return out
    for number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            logger.debug("%s line %d is not readable JSON and was skipped", path.name, number)
            continue
        if not isinstance(record, dict):
            continue
        message = record.get("message")
        if not isinstance(message, dict):
            continue
        usage = message.get("usage")
        if not isinstance(usage, dict):
            continue
        model = str(message.get("model") or "")
        if model in _NOT_A_MODEL:
            continue
        key = str(message.get("id") or record.get("uuid") or "")
        if key:
            if key in seen:
                continue
            seen.add(key)
        out[model] = out.get(model, TokenUsage()) + _usage_from_turn(usage)
    return out


def _normalise(text: str) -> str:
    """Project-directory spelling: every non-alphanumeric run becomes a single dash.

    Claude Code derives a project directory name from the cwd this way, so a lane slug is
    matched against the derived name rather than against the raw path.
    """
    return re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()


def _matches_segment(name: str, wanted: str) -> bool:
    """Does `wanted` appear in `name` as a whole DASH-BOUNDED segment run?

    THE FIX FOR A WIDENING, and the reason it is not `wanted in name`: plain containment makes
    a truncated `lane-y-75` match `lane-y-751` and price one lane's entire spend onto another.
    Both sides must land on a dash or a string edge, so the slug matches whole segments.

    WRITTEN OUT RATHER THAN AS A REGEX, deliberately. The equivalent `(?:^|-)…(?:-|$)` pattern
    is the same predicate, but it would be this module's SECOND `re.` call and
    `graph_queries.is_edge_computation_shape` counts two-regexes-plus-a-scan as a private edge
    computation -- a false positive here (a session store outside the repo is not the corpus,
    and a slug-to-directory match is none of the five kinds), but clearing it would mean adding
    a verdict row to the curated `EDGE_COMPUTATIONS` register, which is outside this lane's
    declared footprint. Four string comparisons cost nothing and read no worse.
    """
    return (name == wanted
            or name.startswith(f"{wanted}-")
            or name.endswith(f"-{wanted}")
            or f"-{wanted}-" in name)


def transcript_dirs(slug: str, sessions_root: Optional[Path] = None,
                    slug_dirs: Optional[Sequence[str]] = None) -> list[Path]:
    """Every session-store directory belonging to `slug`.

    MATCHED, NOT GUESSED, AND NEVER WIDENED. A directory qualifies when its normalised name
    CONTAINS the normalised slug. When nothing matches, the answer is an EMPTY LIST -- this
    function will not fall back to "every directory", because attributing the whole store to
    one lane is a worse error than reporting that the lane could not be found.

    `slug_dirs` names the directories outright, for the case the matcher cannot serve: a `--bg`
    lane's transcript is filed under its LAUNCHING session's cwd and carries no directory of
    its own, so the operator (or the integrator) supplies the name rather than this module
    inferring one it cannot know.
    """
    root = Path(sessions_root) if sessions_root is not None else DEFAULT_SESSIONS_ROOT
    if not root.is_dir():
        return []
    if slug_dirs:
        return [root / name for name in slug_dirs if (root / name).is_dir()]
    wanted = _normalise(slug)
    matched = sorted(d for d in root.iterdir() if d.is_dir() and _matches_segment(_normalise(d.name), wanted))
    if len(matched) > 1:
        #: NOT a refusal -- two directories can legitimately belong to one lane. But a slug
        #: that reaches more than one store is also how one lane's money lands on another's
        #: receipt, and the danger there is the SILENCE: the figure comes out confident. Name
        #: every directory that was summed so a wrong attribution is at least visible.
        logger.warning(
            "slug %r matched %d session directories and ALL of them were summed into one "
            "lane's cost: %s -- if these belong to different lanes, name the right one with "
            "--slug-dir", slug, len(matched), ", ".join(d.name for d in matched))
    return matched


def lane_usage(slug: str, sessions_root: Optional[Path] = None,
               slug_dirs: Optional[Sequence[str]] = None) -> dict[str, TokenUsage]:
    """`{model: usage}` for one lane, summed over every transcript it owns and de-duplicated
    across them."""
    seen: set[str] = set()
    out: dict[str, TokenUsage] = {}
    for directory in transcript_dirs(slug, sessions_root, slug_dirs):
        for transcript in sorted(directory.glob("*.jsonl")):
            for model, usage in read_transcript_usage(transcript, seen).items():
                out[model] = out.get(model, TokenUsage()) + usage
    return out


# --- money -------------------------------------------------------------------------------

@dataclass(frozen=True)
class ModelCost:
    """One model's spend on one lane. `usd is None` means UNPRICED, never zero."""

    model: str
    usage: TokenUsage
    usd: Optional[float] = None
    #: Why it could not be priced, in the reader's own words. Carried rather than recomputed
    #: so a reader of the ledger months later sees the reason the run saw.
    unpriced_reason: Optional[str] = None

    @property
    def is_priced(self) -> bool:
        return self.usd is not None

    def to_dict(self) -> dict:
        return {"model": self.model, "usage": self.usage.to_dict(),
                "usd": None if self.usd is None else round(self.usd, 6),
                "unpriced_reason": self.unpriced_reason}

    @classmethod
    def from_dict(cls, data: dict) -> "ModelCost":
        return cls(model=str(data["model"]), usage=TokenUsage.from_dict(data.get("usage", {})),
                   usd=data.get("usd"), unpriced_reason=data.get("unpriced_reason"))


def price_usage(model: str, usage: TokenUsage,
                registry_path: Optional[Path] = None) -> ModelCost:
    """Price one model's usage, or record WHY it could not be priced.

    The refusal is caught here and carried rather than raised onward, because a lane that ran
    one unpriced model still has a real, reportable cost for the rest. Swallowing it would be
    the failure; carrying it named is the requirement.
    """
    try:
        rate = pr.resolve_rate(model, registry_path)
    except pr.RateUnavailable as exc:
        return ModelCost(model=model, usage=usage, usd=None, unpriced_reason=str(exc))
    return ModelCost(model=model, usage=usage, usd=rate.usd(
        input_tokens=usage.input_tokens, output_tokens=usage.output_tokens,
        cache_write_tokens=usage.cache_write_tokens,
        cache_read_tokens=usage.cache_read_tokens))


@dataclass(frozen=True)
class LaneCost:
    """One lane's tokens and money, itemised per model. The cost half of the lane receipt."""

    slug: str
    batch: str
    models: tuple[ModelCost, ...] = ()
    measured: str = ""
    #: The registry's `as_of`, carried so a figure read next quarter says which card priced it.
    rates_as_of: str = ""
    currency: str = "USD"

    @property
    def usd(self) -> float:
        """PRICED spend only. Unpriced models are in `unpriced()` and are never summed here --
        a total that absorbed them would understate the lane while looking complete."""
        return sum(m.usd for m in self.models if m.usd is not None)

    def usage(self) -> TokenUsage:
        """Every token the lane spent, priced or not. The token total is honest even where the
        money total cannot be."""
        total = TokenUsage()
        for model in self.models:
            total = total + model.usage
        return total

    def unpriced(self) -> tuple[ModelCost, ...]:
        return tuple(m for m in self.models if not m.is_priced)

    def has_transcript(self) -> bool:
        """False when no transcript was found at all -- which is NOT the same as a lane that
        spent nothing, and is rendered differently."""
        return bool(self.models)

    def to_dict(self) -> dict:
        return {"slug": self.slug, "batch": self.batch, "measured": self.measured,
                "rates_as_of": self.rates_as_of, "currency": self.currency,
                "usd": round(self.usd, 6), "usage": self.usage().to_dict(),
                "models": [m.to_dict() for m in self.models]}

    @classmethod
    def from_dict(cls, data: dict) -> "LaneCost":
        return cls(slug=str(data["slug"]), batch=str(data.get("batch", "")),
                   models=tuple(ModelCost.from_dict(m) for m in data.get("models", [])),
                   measured=str(data.get("measured", "")),
                   rates_as_of=str(data.get("rates_as_of", "")),
                   currency=str(data.get("currency", "USD")))

    def render(self) -> str:
        if not self.has_transcript():
            return (f"lane {self.slug}  batch={self.batch or '-'}  NO TRANSCRIPT FOUND -- this "
                    f"lane's session store directory could not be located, so its cost is "
                    f"UNKNOWN rather than zero. A --bg lane's transcript is filed under its "
                    f"launching session; name it with --slug-dir.")
        usage = self.usage()
        lines = [
            f"lane {self.slug}  batch={self.batch or '-'}  "
            f"{self.currency} {self.usd:,.2f} over {usage.calls:,} call(s)  "
            f"[rates as_of {self.rates_as_of or '?'}]",
            f"  tokens: in {usage.input_tokens:,} / out {usage.output_tokens:,} / "
            f"cache-write {usage.cache_write_tokens:,} / cache-read "
            f"{usage.cache_read_tokens:,} / total {usage.total_tokens:,}",
        ]
        for model in sorted(self.models, key=lambda m: (-(m.usd or 0), m.model)):
            if model.is_priced:
                lines.append(f"  {model.model}: {self.currency} {model.usd:,.2f} "
                             f"({model.usage.total_tokens:,} tokens, "
                             f"{model.usage.calls:,} call(s))")
            else:
                lines.append(f"  {model.model}: UNPRICED -- {model.usage.total_tokens:,} "
                             f"tokens, {model.usage.calls:,} call(s), NOT in the total "
                             f"({model.unpriced_reason})")
        if self.unpriced():
            lines.append(f"  {len(self.unpriced())} model(s) unpriced: their tokens are counted "
                         f"above and their money is NOT in the {self.currency} total")
        return "\n".join(lines)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def lane_cost(slug: str, *, batch: str = "", sessions_root: Optional[Path] = None,
              slug_dirs: Optional[Sequence[str]] = None,
              registry_path: Optional[Path] = None) -> LaneCost:
    """One lane's cost, read from its transcripts and priced from the registry."""
    per_model = lane_usage(slug, sessions_root, slug_dirs)
    costs = tuple(price_usage(model, usage, registry_path)
                  for model, usage in sorted(per_model.items()))
    as_of = ""
    try:
        as_of = str(pr.rate_card(registry_path).get("as_of", ""))
    except pr.RegistryError as exc:
        logger.warning("no rate card -- every model will read as unpriced: %s", exc)
    return LaneCost(slug=slug, batch=batch, models=costs, measured=_now(), rates_as_of=as_of)


# --- the ledger, and the join onto the merge receipt ---------------------------------------

def cost_ledger_path(repo_root: Path) -> Path:
    return Path(repo_root) / COST_LEDGER_RELPATH


def append_cost(repo_root: Path, cost: LaneCost) -> None:
    """Append one cost row. APPEND-ONLY: one line added, never a line rewritten (ADR-29/39,
    the `logs/TOKEN-LOG.md` class)."""
    path = cost_ledger_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(cost.to_dict(), sort_keys=True) + "\n")


def read_cost_ledger(repo_root: Path) -> list[LaneCost]:
    """Every cost row, oldest first. A malformed line is warned and skipped."""
    path = cost_ledger_path(repo_root)
    if not path.exists():
        return []
    out: list[LaneCost] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            out.append(LaneCost.from_dict(json.loads(raw)))
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning("%s line %d is unreadable and was skipped: %s",
                           COST_LEDGER_RELPATH, number, exc)
    return out


def uncosted_reason(repo_root: Path, slug: str) -> Optional[str]:
    """WHY this slug's receipt carries no money, or None when it does.

    THE REASON IS RETURNED, NOT A BARE BOOLEAN -- the argument `merge_receipt.
    incompleteness_reason` makes, in this lane's currency: a receipt that reports minutes and
    is silent about tokens reads exactly like a cheap merge, and "no cost row" and "a cost row
    whose every model was unpriced" are different facts a reader must be able to tell apart.
    """
    rows = [c for c in read_cost_ledger(repo_root) if c.slug == slug]
    if not rows:
        return (f"no cost row for {slug!r} in {COST_LEDGER_RELPATH} -- the receipt reports "
                f"minutes and is silent about tokens, which reads exactly like a cheap merge. "
                f"Run `lane_cost.py close --slug {slug}`.")
    latest = rows[-1]
    if not latest.has_transcript():
        return (f"the cost row for {slug!r} found NO TRANSCRIPT, so its spend is unknown rather "
                f"than zero -- name the session directory with --slug-dir and re-close")
    if not any(m.is_priced for m in latest.models):
        return (f"every model on {slug!r}'s cost row is UNPRICED "
                f"({', '.join(m.model for m in latest.models)}) -- the row carries tokens but "
                f"no defensible money figure")
    return None


def is_costed(repo_root: Path, slug: str) -> bool:
    return uncosted_reason(repo_root, slug) is None


def _receipt_rows(repo_root: Path, slug: str) -> list[dict]:
    """The minutes ledger's rows for one slug, read as raw JSON.

    READ AS RAW DICTS, DELIBERATELY, rather than through `merge_receipt.Receipt`: this module
    needs three display fields, and importing a module another lane is concurrently rewriting
    would couple this ledger's reader to that module's in-flight shape.
    """
    path = Path(repo_root) / RECEIPT_LEDGER_RELPATH
    if not path.exists():
        return []
    out: list[dict] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and row.get("slug") == slug:
            out.append(row)
    return out


def receipt_view(repo_root: Path, slug: str) -> str:
    """THE LANE RECEIPT: minutes from `MERGE-RECEIPTS.jsonl`, tokens and USD from
    `LANE-COSTS.jsonl`, joined on the slug and rendered as one thing."""
    lines: list[str] = []
    receipts = _receipt_rows(repo_root, slug)
    if not receipts:
        lines.append(f"receipt {slug}: no row in {RECEIPT_LEDGER_RELPATH} (minutes unrecorded)")
    for row in receipts:
        wall = float(row.get("wall_seconds") or 0.0) / 60.0
        split = row.get("baseline_split_minutes") or {}
        lines.append(
            f"receipt {slug}  kind={row.get('kind', '?')}  batch={row.get('batch') or '-'}  "
            f"{wall:,.1f} min wall  "
            f"(tests {float(split.get('tests', 0.0)):,.1f} / residual "
            f"{float(split.get('residual_ceremony', 0.0)):,.1f})")
    rows = [c for c in read_cost_ledger(repo_root) if c.slug == slug]
    if not rows:
        lines.append(uncosted_reason(repo_root, slug) or "")
    else:
        lines.append(rows[-1].render())
    return "\n".join(line for line in lines if line)


# --- the per-batch / per-model report -------------------------------------------------------

@dataclass(frozen=True)
class BatchCostReport:
    """Done-when 3's answer: cost per batch AND cost per model, over the whole cost ledger."""

    #: EVERY line in the ledger, in file order, including superseded ones. The append-only
    #: record is kept whole here; the selection below is what the figures are built from.
    rows: tuple[LaneCost, ...] = ()
    currency: str = "USD"

    def resolved(self) -> tuple[LaneCost, ...]:
        """One row per slug, LAST WINS -- the same rule `uncosted_reason` applies with
        `rows[-1]`, lifted so the aggregate and the per-slug reader cannot disagree.

        TWO READERS OF ONE LEDGER MUST NOT MEAN DIFFERENT THINGS BY A DUPLICATE. Summing every
        row while the per-slug reader takes the last one gave the same file two incompatible
        answers, and because the ledger is append-only (ADR-29/ADR-39) there is no sanctioned
        repair: the superseded line cannot be deleted, so one retry would inflate the batch
        total and every future boot's `[cost]` line permanently.

        A retry is the NORMAL path, not a mistake -- a `--bg` lane's first honest close finds
        no transcript, and the operator re-closes with `--slug-dir`. Superseding in the reader
        fixes the arithmetic without moving one byte of the record.
        """
        latest: dict[str, LaneCost] = {}
        for row in self.rows:
            latest[row.slug] = row
        return tuple(latest.values())

    def measured(self) -> tuple[LaneCost, ...]:
        """The rows that actually measured something. EVERY FIGURE IS BUILT FROM THIS.

        A row whose transcript was never found carries `models=()`, so its `usd` is 0.0 -- and
        summing it silently converts "we do not know what this lane cost" into "this lane was
        free". `LaneCost.render()` already refuses that lie for a single lane; this is the
        same guard at the aggregate, where it was missing.
        """
        return tuple(r for r in self.resolved() if r.has_transcript())

    def unmeasured(self) -> tuple[LaneCost, ...]:
        """Lanes with a row but no measurement. REPORTED, never summed and never counted."""
        return tuple(r for r in self.resolved() if not r.has_transcript())

    def by_batch(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for row in self.measured():
            out[row.batch or "-"] = out.get(row.batch or "-", 0.0) + row.usd
        return out

    def by_model(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for row in self.measured():
            for model in row.models:
                if model.usd is not None:
                    out[model.model] = out.get(model.model, 0.0) + model.usd
        return out

    def tokens_by_model(self) -> dict[str, TokenUsage]:
        out: dict[str, TokenUsage] = {}
        for row in self.measured():
            for model in row.models:
                out[model.model] = out.get(model.model, TokenUsage()) + model.usage
        return out

    def unpriced_models(self) -> list[str]:
        return sorted({m.model for row in self.measured() for m in row.models if not m.is_priced})

    @property
    def usd(self) -> float:
        return sum(row.usd for row in self.measured())

    def render(self) -> str:
        """NEVER a bare total, and never `$0.00` over an empty ledger.

        An empty ledger is not a free batch -- it is no measurement, which is exactly the lie
        `merge_receipt` refuses for a 0.0-minute receipt. So the empty case says so in words
        and prints no figure at all.

        AN EMPTY ROW IS NOT A FREE LANE EITHER, which is the same principle one level down: a
        ledger holding nothing but transcript-less rows is still no measurement, and `n=` here
        counts MEASUREMENTS, never lines.
        """
        if not self.measured():
            unknown = (f" {len(self.unmeasured())} lane(s) have a row but NO measurement: "
                       f"{', '.join(r.slug for r in self.unmeasured())}."
                       if self.unmeasured() else "")
            return (f"cost: no measured cost receipts in {COST_LEDGER_RELPATH} -- the total is "
                    f"UNDEFINED, not zero.{unknown} Close a lane with "
                    f"`lane_cost.py close --slug <slug>`.")
        lines = [f"cost over n={len(self.measured())} lane receipt(s): "
                 f"{self.currency} {self.usd:,.2f}"]
        lines.append("  per batch:")
        for batch, usd in sorted(self.by_batch().items(), key=lambda kv: -kv[1]):
            lines.append(f"    {batch}: {self.currency} {usd:,.2f}")
        lines.append("  per model:")
        tokens = self.tokens_by_model()
        for model, usd in sorted(self.by_model().items(), key=lambda kv: -kv[1]):
            lines.append(f"    {model}: {self.currency} {usd:,.2f} "
                         f"({tokens[model].total_tokens:,} tokens, "
                         f"{tokens[model].calls:,} call(s))")
        unpriced = self.unpriced_models()
        if unpriced:
            lines.append(f"  UNPRICED and excluded from every figure above: "
                         f"{', '.join(unpriced)} -- their tokens are real and their money is "
                         f"unknown, so this total is a FLOOR")
        if self.unmeasured():
            lines.append(f"  UNMEASURED and excluded from n= and from every figure above: "
                         f"{', '.join(r.slug for r in self.unmeasured())} -- no transcript was "
                         f"found, so their spend is UNKNOWN rather than zero (re-close with "
                         f"--slug-dir); this total is a FLOOR")
        return "\n".join(lines)


def batch_report(repo_root: Path) -> BatchCostReport:
    return BatchCostReport(rows=tuple(read_cost_ledger(repo_root)))


def cost_health_line(repo_root: Path) -> Optional[str]:
    """The `[cost]` digest line for `fleet_health` -- per batch and per model, in one line.

    ONE FILE READ, no transcript scanning: SessionStart pays for this on every boot, and a
    digest line that walked the session store would make the boot cost scale with the history.
    Returns None over an empty ledger rather than a `$0.00` line nobody should believe.
    """
    report = batch_report(repo_root)
    if not report.measured():
        #: SILENT, not `$0.00`. A ledger of transcript-less rows is no measurement, and this
        #: line is printed at every SessionStart -- it is the widest audience an unmeasured
        #: zero could reach, so it is the last place to print one.
        return None
    batches = ", ".join(f"{b} ${usd:,.2f}" for b, usd
                        in sorted(report.by_batch().items(), key=lambda kv: -kv[1])[:3])
    models = ", ".join(f"{m} ${usd:,.2f}" for m, usd
                       in sorted(report.by_model().items(), key=lambda kv: -kv[1])[:3])
    line = (f"[cost] ${report.usd:,.2f} over {len(report.measured())} lane(s) / "
            f"batch: {batches} / model: {models}")
    unpriced = report.unpriced_models()
    if unpriced:
        line += f" / {len(unpriced)} model(s) UNPRICED (figures are a floor)"
    if report.unmeasured():
        line += f" / {len(report.unmeasured())} lane(s) UNMEASURED (excluded, not zeroed)"
    return line


# --- feeding logs/TOKEN-LOG.md ---------------------------------------------------------------

_TOKEN_LOG_HEADER_LINES = 4


def token_log_entry(report: BatchCostReport, *, on: Optional[str] = None) -> str:
    """One `logs/TOKEN-LOG.md` entry in that file's own established format.

    THE FORMAT IS THE FILE'S, NOT THIS MODULE'S -- a `## YYYY-MM-DD (...)` header, a delta
    line, a tokens line, then one line per model. A new shape would make eighteen months of
    entries incomparable with the first one written by a tool, which is the whole reason the
    file is fed rather than replaced.

    It states its METHOD in the header, beside the existing entries' `via ccusage --json`,
    because the two methods do not measure the same thing: `ccusage` is fleet-wide by calendar
    week and excludes cache tokens "for comparability"; this is per-lane, by cost receipt, and
    counts them. An entry that did not say which it was would invite a reader to diff two
    incomparable numbers and call the difference a trend.
    """
    day = on or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    usage_by_model = report.tokens_by_model()
    money_by_model = report.by_model()
    total = TokenUsage()
    for usage in usage_by_model.values():
        total = total + usage
    lines = [
        f"## {day} (delta: {len(report.measured())} lane receipt(s), via lane_cost.py -- "
        f"per-lane, cache tokens INCLUDED)",
        f"Delta: {len(report.by_batch())} batch(es), {total.calls:,} calls, "
        f"${report.usd:,.2f}",
        f"Tokens in+out: {(total.input_tokens + total.output_tokens):,} "
        f"(in: {total.input_tokens:,}, out: {total.output_tokens:,}) -- cache counted "
        f"separately below, NOT folded in",
        f"Cache: write {total.cache_write_tokens:,}, read {total.cache_read_tokens:,}",
    ]
    for model, usage in sorted(usage_by_model.items(),
                               key=lambda kv: -kv[1].total_tokens):
        usd = money_by_model.get(model)
        money = f"${usd:,.2f}" if usd is not None else "UNPRICED"
        lines.append(f"{model}: {money} (in: {usage.input_tokens:,}, "
                     f"out: {usage.output_tokens:,}, cache-read: {usage.cache_read_tokens:,})")
    lines.append("Method: scripts/lane_cost.py over logs/LANE-COSTS.jsonl; rates from "
                 "ecosystem/provider-registry.yaml. NOT comparable line-for-line with the "
                 "ccusage entries below -- different scope and different cache treatment.")
    return "\n".join(lines)


def append_token_log(repo_root: Path, entry: str) -> Path:
    """PREPEND the entry below the header, which is what "append" means for this file.

    `logs/TOKEN-LOG.md` is append-only (ADR-29/ADR-39) AND newest-first: a new entry goes in
    at the top, under the three-line preamble, and NO existing byte moves except by being
    pushed down. This function reads the file, splits ONCE at the end of the header, and
    writes header + new entry + the entire remaining text unchanged -- it never parses, never
    reformats and never rewrites an existing entry.
    """
    path = Path(repo_root) / TOKEN_LOG_RELPATH
    if not path.exists():
        raise CostError(f"{TOKEN_LOG_RELPATH} is absent -- refusing to create it here: whether "
                        f"this file exists at all is a recorded decision, not a side effect")
    existing = path.read_text(encoding="utf-8")
    lines = existing.split("\n")
    head, rest = lines[:_TOKEN_LOG_HEADER_LINES], lines[_TOKEN_LOG_HEADER_LINES:]
    path.write_text("\n".join(head + entry.split("\n") + [""] + rest),
                    encoding="utf-8", newline="\n")
    return path


# --- CLI -------------------------------------------------------------------------------------

def _root(ctx: click.Context) -> Path:
    return ctx.obj["root"]


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path),
              default=_REPO_ROOT, show_default=True)
@click.pass_context
def cli(ctx: click.Context, repo_root: Path) -> None:
    """Tokens and USD per lane and per model, from the transcripts and the registry."""
    ctx.ensure_object(dict)
    ctx.obj["root"] = Path(repo_root)


_slug_dir_option = click.option(
    "--slug-dir", "slug_dirs", multiple=True,
    help="Session-store directory name to read instead of matching on the slug. Needed for a "
         "--bg lane, whose transcript is filed under its launching session.")


@cli.command("lane")
@click.option("--slug", required=True)
@click.option("--batch", default="", help="Batch letter, for the per-batch report.")
@_slug_dir_option
@click.pass_context
def cmd_lane(ctx: click.Context, slug: str, batch: str, slug_dirs: tuple[str, ...]) -> None:
    """Compute and PRINT one lane's cost. Writes nothing."""
    click.echo(lane_cost(slug, batch=batch, slug_dirs=list(slug_dirs) or None).render())


@cli.command("close")
@click.option("--slug", required=True)
@click.option("--batch", default="")
@_slug_dir_option
@click.pass_context
def cmd_close(ctx: click.Context, slug: str, batch: str, slug_dirs: tuple[str, ...]) -> None:
    """Compute one lane's cost and APPEND it to the cost ledger."""
    cost = lane_cost(slug, batch=batch, slug_dirs=list(slug_dirs) or None)
    append_cost(_root(ctx), cost)
    click.echo(cost.render())


@cli.command("receipt")
@click.option("--slug", required=True)
@click.pass_context
def cmd_receipt(ctx: click.Context, slug: str) -> None:
    """THE LANE RECEIPT -- minutes, tokens and USD joined on the slug."""
    click.echo(receipt_view(_root(ctx), slug))


@cli.command("report")
@click.pass_context
def cmd_report(ctx: click.Context) -> None:
    """Cost per batch and per model over the whole cost ledger."""
    click.echo(batch_report(_root(ctx)).render())


@cli.command("token-log")
@click.option("--append", "do_append", is_flag=True,
              help="Write the entry into logs/TOKEN-LOG.md. Without it, print and write nothing.")
@click.pass_context
def cmd_token_log(ctx: click.Context, do_append: bool) -> None:
    """Render a TOKEN-LOG entry from the cost ledger, and optionally append it."""
    report = batch_report(_root(ctx))
    if not report.measured():
        raise click.ClickException(
            f"no MEASURED rows in {COST_LEDGER_RELPATH} -- an entry built from nothing, or "
            f"from rows whose transcripts were never found, would write a zero into an "
            f"append-only file that cannot be corrected afterwards")
    entry = token_log_entry(report)
    click.echo(entry)
    if do_append:
        path = append_token_log(_root(ctx), entry)
        click.echo(f"\nappended to {path}")


if __name__ == "__main__":
    cli()
