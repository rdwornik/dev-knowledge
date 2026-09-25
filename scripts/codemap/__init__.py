"""Codemap generator for ARCHITECTURE.md auto-generation (ADR-51).

Per ADR-51 architecture-doc-convention and the codemap-generator
output specification (ADR-51 amendment, pending).
"""
__version__ = "0.1.0"

from .generator import generate_codemap
from .check import check_codemap

__all__ = ["generate_codemap", "check_codemap", "__version__"]
