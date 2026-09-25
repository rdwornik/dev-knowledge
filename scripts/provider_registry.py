#!/usr/bin/env python
"""provider_registry.py — the reader for `ecosystem/provider-registry.yaml`.

The registry is the declared source of truth for every provider, CLI and model string on the
repo's live surface (CLOUD-4 v2, cut from
`docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md` §3.3, GO verdict).

Two consumer classes, and the split is deliberate:

* **Runtime readers** — a Python organ that can load YAML imports from here and stops
  carrying its own literal. Today that is `scripts/changelog_sentinel.py` (seam S7), whose
  `_TOOLS` table is now derived rather than typed.
* **Checked sites** — a `.md` frontmatter key, a `.js` object literal, committed prose, a
  JSON config. None of those can read a YAML file at load time, so the coupling is a
  checker (`scripts/check_provider_registry.py`) rather than an import. That is the honest
  mechanism, not a weaker one: the value gets exactly one home and one gate either way.

Read-only. This module loads and answers; it writes nothing.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, NamedTuple

import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from pydantic import ValidationError  # noqa: E402

from ecosystem.schema.provider_registry import ProviderRegistry  # noqa: E402

REGISTRY_REL = "ecosystem/provider-registry.yaml"
DEFAULT_REGISTRY_PATH = _REPO_ROOT / "ecosystem" / "provider-registry.yaml"


class RegistryError(RuntimeError):
    """The registry is absent, unparseable, or not the declared two-collection shape.

    Raised rather than returned: a caller that silently degrades to a hardcoded default
    would re-create the exact drift this module exists to end. The one caller allowed to
    swallow it is a fail-soft hook, which does so explicitly at its own call site.
    """


class RateUnavailable(RegistryError):
    """No defensible price for a model — the file declares no rate card, the model has no row,
    or the row carries no `rates:` block (`[#751]`).

    A SUBCLASS OF `RegistryError` rather than a sibling, so a consumer that already handles
    "the registry could not answer" keeps working unchanged, while one that cares about the
    difference between "unpriced" and "unreadable" can catch this narrowly. It is raised and
    never returned as a zero: absent and free are different facts, and a total that cannot tell
    them apart is not a measurement.
    """


def load_registry(path: Path | None = None) -> dict[str, Any]:
    """Parse the registry, validate it against the declared schema, return the raw mapping.

    The two-collection guard below stays ahead of the schema on purpose: it produces the
    message the callers and their tests already depend on for the two coarse failures
    (absent file, missing collection), and it means a garbage file fails with "missing
    `models:` mapping" rather than with a pydantic traceback.

    Validation itself is `ecosystem/schema/provider_registry.ProviderRegistry` (LANE L1,
    2026-08-23). It runs HERE, in the loader, rather than in the seam checker — so every
    consumer gets it: the SessionStart sentinel (S7), the pre-commit agreement gate, and the
    suite all reach the file through this function and none of them has to opt in. A
    `ValidationError` is re-raised as `RegistryError` so the existing failure contract is
    unchanged: `main()` still exits 2, the fail-soft hook still goes quiet.

    Returns the RAW mapping, not the validated model. Deliberate, and it is a minimal-diff
    decision rather than a compromise: the eight accessors below already read the raw shape,
    and re-pointing them at attribute access would be a rewrite whose only gain is style.
    """
    p = Path(path) if path is not None else DEFAULT_REGISTRY_PATH
    if not p.exists():
        raise RegistryError(f"provider registry absent: {p}")
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise RegistryError(f"provider registry unparseable ({p}): {exc}") from exc
    if not isinstance(data, dict):
        raise RegistryError(f"provider registry is not a YAML mapping: {p}")
    for key in ("providers", "models"):
        if not isinstance(data.get(key), dict):
            raise RegistryError(f"provider registry missing `{key}:` mapping: {p}")
    try:
        ProviderRegistry.model_validate(data)
    except ValidationError as exc:
        raise RegistryError(f"provider registry fails its declared schema ({p}): {exc}") from exc
    return data


def council_aliases(path: Path | None = None) -> dict[str, str]:
    """`{council alias: provider id}` — the closed vocabulary `AI_COUNCIL_PROCESS` names.

    Providers the council does not panel (`council_alias: null`) are omitted. Uniqueness is
    guaranteed upstream by the schema, so a plain dict comprehension cannot lose a row here.
    """
    return {
        str(f["council_alias"]): pid
        for pid, f in providers(path).items()
        if f.get("council_alias")
    }


def role_admissions(path: Path | None = None) -> dict[tuple[str, str], dict[str, Any]]:
    """`{(model_id, role): verdict record}` for every recorded admission verdict.

    Empty for a model with no `role_admission:` block, which is the common and fully valid
    case — configuration is never gated on admission.
    """
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for mid, fields in models(path).items():
        for role, record in (fields.get("role_admission") or {}).items():
            out[(str(mid), str(role))] = dict(record or {})
    return out


def providers(path: Path | None = None) -> dict[str, Any]:
    """`{provider_id: fields}`."""
    return load_registry(path)["providers"]


def models(path: Path | None = None) -> dict[str, Any]:
    """`{model_id: fields}`."""
    return load_registry(path)["models"]


def version_commands(path: Path | None = None) -> dict[str, list[str]]:
    """`{tool_versions.yaml key: argv that prints the installed version}` — seam S7.

    Providers with no CLI on this repo's surface (`cli: null`) are omitted: an entry with no
    probe is not a probe. Keyed by `changelog_tool_key` so the result drops straight into
    `changelog_sentinel`'s lookup against `ecosystem/tool-versions.yaml`.
    """
    out: dict[str, list[str]] = {}
    for pid, fields in providers(path).items():
        argv = fields.get("version_command")
        key = fields.get("changelog_tool_key")
        if not argv or not key:
            continue
        if not isinstance(argv, list) or not all(isinstance(a, str) for a in argv):
            raise RegistryError(f"provider `{pid}`: version_command is not a list of strings")
        out[str(key)] = list(argv)
    return out


def changelog_source_urls(path: Path | None = None) -> dict[str, str]:
    """`{tool_versions.yaml key: changelog source url}` — the S8 identity half."""
    out: dict[str, str] = {}
    for fields in providers(path).values():
        key = fields.get("changelog_tool_key")
        url = fields.get("changelog_source_url")
        if key and url:
            out[str(key)] = str(url)
    return out


def models_for_role(role: str, path: Path | None = None) -> list[str]:
    """Every model id carrying `role`, in registry order."""
    return [mid for mid, f in models(path).items() if role in (f.get("roles") or [])]


def model_ids(path: Path | None = None) -> list[str]:
    """The closed vocabulary of model ids the repo is allowed to name."""
    return list(models(path).keys())


def roles(path: Path | None = None) -> dict[str, Any]:
    """`{role: spec}` — `[#691]`'s third collection, the role-keyed ORDERED fallback lists.

    Empty for a registry predating `[#691]`, which is why the key is read with `.get`: the
    collection is optional in the schema so every older registry still loads.
    """
    return load_registry(path).get("roles") or {}


def role_order(role: str, path: Path | None = None) -> list[dict[str, Any]]:
    """One role's DECLARED fallback list, in file order.

    DECLARED, not measured — the distinction AX21-2 turns on. `provider_router.rerank()` is what
    reorders this by measured pass rate per cost; this accessor hands back what the file says,
    and a caller presenting it as a measured ranking is the failure AX21-2 names.
    """
    spec = roles(path).get(role)
    if spec is None:
        raise RegistryError(
            f"role `{role}` is not in the registry; known roles: {sorted(roles(path))}"
        )
    return [dict(entry) for entry in spec.get("order") or []]


def is_admitted(entry: dict[str, Any]) -> bool:
    """Is this role entry ADMITTED — i.e. is it anything other than NOT ADMITTED?

    The predicate is written this way round on purpose. `Verdict` carries three members and
    only ONE of them is admission; `refused` and `unevaluated` are both NOT ADMITTED, and so is
    an absent `admission:` block. So the honest test is `verdict == "admitted"` and everything
    else — including silence — falls the other way.

    This is the function the Half A / Half B boundary rests on: every non-Claude entry in the
    shipped registry returns `False` here, and this lane recorded that state without measuring
    it. AX22-1's >= 8-of-10 measurement, which is what could turn any of them `True`, is Half B's.
    """
    admission = entry.get("admission")
    if not admission:
        return False
    return str(admission.get("verdict") or "") == "admitted"


def licences(path: Path | None = None) -> dict[str, str]:
    """`{provider_id: licence status}` — `[#691]` leg (c).

    A provider carrying NO `licence:` block resolves to `"unknown"`, never to `"permitted"`.
    The default is the conservative one because the whole point of the field is that an unruled
    licence is not a permission; defaulting the other way would make the field's absence grant
    exactly what its presence was added to withhold.
    """
    return {
        pid: ((fields.get("licence") or {}).get("status") or "unknown")
        for pid, fields in providers(path).items()
    }


def pins_by_path(path: Path | None = None) -> dict[str, list[tuple[str, str, str]]]:
    """`{repo-relative path: [(model_id, seam, format), ...]}` — the checker's work list."""
    out: dict[str, list[tuple[str, str, str]]] = {}
    for mid, fields in models(path).items():
        for pin in fields.get("pinned_at") or []:
            rel = str(pin["path"])
            out.setdefault(rel, []).append((mid, str(pin.get("seam", "")), str(pin.get("format", ""))))
    return out


def rate_card(path: Path | None = None) -> dict[str, Any]:
    """The `rate_card:` block — currency, unit, `as_of`, provenance, cache multipliers.

    Raises rather than returning `{}` when absent, on this module's standing rule: a caller
    that silently degraded to a default would invent the currency and the date, which are the
    two things a dollar figure cannot be read without.
    """
    card = load_registry(path).get("rate_card")
    if not isinstance(card, dict):
        raise RateUnavailable(
            f"{REGISTRY_REL} declares no `rate_card:` — there is no currency, no unit and no "
            f"date to read any price against, so nothing here can be costed"
        )
    return card


class ModelRate(NamedTuple):
    """One model's four per-unit prices, fully resolved — multipliers already applied.

    A `NamedTuple` RATHER THAN A `@dataclass`, and the reason is a measured trap rather than a
    style choice. `scripts/provider_router.py` loads this module by PATH under a synthetic
    module name and never registers it in `sys.modules` (`_sibling`, the shape `telemetry_emit`
    also uses). `dataclasses._process_class` resolves `sys.modules[cls.__module__]` while
    scanning annotations, gets `None`, and dies with `AttributeError: 'NoneType' object has no
    attribute '__dict__'` — 33 errors in `tests/test_provider_router.py`, none of them pointing
    at the dataclass. `NamedTuple` does no such lookup and loads correctly under both import
    paths. The loader is the thing that is wrong (PEP 451 registers before executing) and it is
    NOT fixed here: it is a shared helper this lane does not own. Reported instead.

    RESOLUTION HAPPENS HERE, not in the caller, because it is registry semantics: the fact
    "a cache write costs 1.25x input" belongs to the card that declares it. A cost reporter
    that applied the multipliers itself would be a second home for them, and the first thing
    to drift when the card changes.
    """

    model: str
    currency: str
    unit: str
    as_of: str
    input: float
    output: float
    cache_write: float
    cache_read: float
    #: Where this model's price came from, when it differs from the card's own source.
    source: str | None = None

    def usd(self, *, input_tokens: int = 0, output_tokens: int = 0,
            cache_write_tokens: int = 0, cache_read_tokens: int = 0) -> float:
        """Cost of a token count at these rates. The unit divisor is read from `unit` rather
        than assumed, so a card that ever quotes per-thousand fails loudly instead of
        under-reporting by a factor of a thousand."""
        if self.unit != "per_million_tokens":
            raise RateUnavailable(
                f"rate unit {self.unit!r} is not one this reader knows how to divide by — "
                f"refusing rather than guessing the scale")
        per_unit = 1_000_000
        return (input_tokens * self.input
                + output_tokens * self.output
                + cache_write_tokens * self.cache_write
                + cache_read_tokens * self.cache_read) / per_unit


def resolve_rate(model_id: str, path: Path | None = None) -> ModelRate:
    """The fully-resolved rate for one model, or `RateUnavailable` NAMING it.

    THE REFUSAL IS THE FEATURE. Three distinct absences reach this function — the file has no
    card, the model has no row, the row has no `rates:` — and all three raise. None returns a
    zero. A zero here is indistinguishable from a free model and propagates into a total that
    meets any budget while meaning nothing; naming the model instead lets a report say how much
    of its spend is unaccounted for, which is a fact a reader can act on.

    Every call re-reads the file. Deliberate, and it is what makes the lane contract's "resolved
    from that file at run time" true rather than nearly true: a module-level cache seeded once
    would survive an edit to the registry and keep reporting the old price.
    """
    card = rate_card(path)
    row = models(path).get(model_id)
    if row is None:
        raise RateUnavailable(
            f"model {model_id!r} is not declared in {REGISTRY_REL} — it cannot be priced, and "
            f"it is not free. Add a row (with `rates:` if its price is known) rather than "
            f"letting an unregistered id cost nothing")
    rates = row.get("rates")
    if not isinstance(rates, dict):
        raise RateUnavailable(
            f"model {model_id!r} is declared in {REGISTRY_REL} but carries no `rates:` block — "
            f"its price is unknown, which is not the same fact as zero")
    base_input = float(rates["input"])
    cache_write = rates.get("cache_write")
    cache_read = rates.get("cache_read")
    return ModelRate(
        model=model_id,
        currency=str(card["currency"]),
        unit=str(card["unit"]),
        as_of=str(card["as_of"]),
        input=base_input,
        output=float(rates["output"]),
        cache_write=(float(cache_write) if cache_write is not None
                     else base_input * float(card["cache_write_multiplier"])),
        cache_read=(float(cache_read) if cache_read is not None
                    else base_input * float(card["cache_read_multiplier"])),
        source=(str(rates["source"]) if rates.get("source") else None),
    )


def priced_models(path: Path | None = None) -> list[str]:
    """Every model id carrying a `rates:` block, sorted. The complement — every id in
    `models()` not in here — is the unpriced set, which is reported rather than assumed empty.
    """
    return sorted(mid for mid, row in models(path).items() if isinstance(row.get("rates"), dict))


def attribution_tokens(path: Path | None = None) -> dict[str, str]:
    """`{model_id: the literal string that model is attributed by on disk}`.

    Defaults to the id itself; `grok-l5` is the live counter-example (`grok L5` in prose).
    """
    return {mid: str(f.get("attribution_token") or mid) for mid, f in models(path).items()}
