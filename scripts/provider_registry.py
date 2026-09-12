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
from typing import Any, Optional

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


def load_registry(path: Optional[Path] = None) -> dict[str, Any]:
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


def council_aliases(path: Optional[Path] = None) -> dict[str, str]:
    """`{council alias: provider id}` — the closed vocabulary `AI_COUNCIL_PROCESS` names.

    Providers the council does not panel (`council_alias: null`) are omitted. Uniqueness is
    guaranteed upstream by the schema, so a plain dict comprehension cannot lose a row here.
    """
    return {
        str(f["council_alias"]): pid
        for pid, f in providers(path).items()
        if f.get("council_alias")
    }


def role_admissions(path: Optional[Path] = None) -> dict[tuple[str, str], dict[str, Any]]:
    """`{(model_id, role): verdict record}` for every recorded admission verdict.

    Empty for a model with no `role_admission:` block, which is the common and fully valid
    case — configuration is never gated on admission.
    """
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for mid, fields in models(path).items():
        for role, record in (fields.get("role_admission") or {}).items():
            out[(str(mid), str(role))] = dict(record or {})
    return out


def providers(path: Optional[Path] = None) -> dict[str, Any]:
    """`{provider_id: fields}`."""
    return load_registry(path)["providers"]


def models(path: Optional[Path] = None) -> dict[str, Any]:
    """`{model_id: fields}`."""
    return load_registry(path)["models"]


def version_commands(path: Optional[Path] = None) -> dict[str, list[str]]:
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


def changelog_source_urls(path: Optional[Path] = None) -> dict[str, str]:
    """`{tool_versions.yaml key: changelog source url}` — the S8 identity half."""
    out: dict[str, str] = {}
    for fields in providers(path).values():
        key = fields.get("changelog_tool_key")
        url = fields.get("changelog_source_url")
        if key and url:
            out[str(key)] = str(url)
    return out


def models_for_role(role: str, path: Optional[Path] = None) -> list[str]:
    """Every model id carrying `role`, in registry order."""
    return [mid for mid, f in models(path).items() if role in (f.get("roles") or [])]


def model_ids(path: Optional[Path] = None) -> list[str]:
    """The closed vocabulary of model ids the repo is allowed to name."""
    return list(models(path).keys())


def roles(path: Optional[Path] = None) -> dict[str, Any]:
    """`{role: spec}` — `[#691]`'s third collection, the role-keyed ORDERED fallback lists.

    Empty for a registry predating `[#691]`, which is why the key is read with `.get`: the
    collection is optional in the schema so every older registry still loads.
    """
    return load_registry(path).get("roles") or {}


def role_order(role: str, path: Optional[Path] = None) -> list[dict[str, Any]]:
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


def licences(path: Optional[Path] = None) -> dict[str, str]:
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


def pins_by_path(path: Optional[Path] = None) -> dict[str, list[tuple[str, str, str]]]:
    """`{repo-relative path: [(model_id, seam, format), ...]}` — the checker's work list."""
    out: dict[str, list[tuple[str, str, str]]] = {}
    for mid, fields in models(path).items():
        for pin in fields.get("pinned_at") or []:
            rel = str(pin["path"])
            out.setdefault(rel, []).append((mid, str(pin.get("seam", "")), str(pin.get("format", ""))))
    return out


def attribution_tokens(path: Optional[Path] = None) -> dict[str, str]:
    """`{model_id: the literal string that model is attributed by on disk}`.

    Defaults to the id itself; `grok-l5` is the live counter-example (`grok L5` in prose).
    """
    return {mid: str(f.get("attribution_token") or mid) for mid, f in models(path).items()}
