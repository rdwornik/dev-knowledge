"""Synthetic-fixture builders for `tests/test_read_gate.py` -- no course text, nothing
checked in as a binary blob; every fixture is built from these functions at test run time
(DONE-ITEM 1/3: "generated in the test").
"""
from __future__ import annotations

import zipfile
from pathlib import Path


def build_minimal_pdf(text: str) -> bytes:
    """A minimal single-page PDF holding one `BT ... Tj ... ET` text line -- hand-built with
    a byte-accurate xref table, no PDF-writing library (this lane's one added dependency,
    `pdfplumber`, is a reader). Escapes `(`, `)` and `\\` per the PDF literal-string spec."""
    escaped = text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
    content = f"BT /F1 24 Tf 72 712 Td ({escaped}) Tj ET".encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> "
        b"/MediaBox [0 0 612 792] /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n"
        + content + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode("ascii") + body + b"\nendobj\n"
    xref_offset = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        out += f"{off:010d} 00000 n \n".encode("ascii")
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF"
    ).encode("ascii")
    return bytes(out)


def write_pdf_fixture(path: Path, text: str) -> Path:
    path.write_bytes(build_minimal_pdf(text))
    return path


def write_epub_fixture(path: Path, text: str) -> Path:
    """A minimal EPUB-shaped zip: one XHTML entry `extract_source_text` will find and strip
    tags from. Not a spec-complete EPUB (no OPF/NCX) -- the extractor only needs a zip
    containing `*.xhtml`/`*.html`/`*.htm`, so that is all this builds."""
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr(
            "content.xhtml",
            f"<html><body><p>{text}</p></body></html>",
        )
    return path


def write_text_fixture(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path
