"""Auto-TOC generator for large canonical docs (mirrors the codemap pattern).

Parses a markdown file's ## / ### headers and maintains a nested anchor-link
table of contents between <!-- TOC:START --> / <!-- TOC:END --> markers,
freshness-checked exactly as the codemap is (ADR-51).
"""
__version__ = "0.1.0"

from .generator import generate_toc
from .check import check_toc

__all__ = ["generate_toc", "check_toc", "__version__"]
