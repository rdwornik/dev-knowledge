---
last_reviewed: 2026-06-02
status: active
owner: robdwornik@gmail.com
---

# Architecture

<!-- scope: meta -->

Synthetic repo for testing the ADR-38 universal governance baseline + canonical
structure checks. ARCHITECTURE.md is mandatory for every repo (ADR-51 as amended
2026-05-23).

## Purpose

Exercise the audit checks against a conformant synthetic repo.

## Codemap

No real code (synthetic fixture).

## Layer Boundaries & Invariants

Fixture only — no executable layers.

## Key conventions

Match the `.dev-knowledge` canonical spine.

## Authority and governance

ADR-38 A6.

## Validators and enforcement

`audit.py` `check_canonical_structure`.
