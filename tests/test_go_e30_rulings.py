import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_go_e30_standing_rulings_are_carried():
    text = (ROOT / "protocols" / "STANDING_RULINGS.md").read_text(
        encoding="utf-8"
    )
    ay = re.search(r"^## AY\.", text, re.MULTILINE)
    az = re.search(r"^## AZ\. GO-E3\.0 R1-R14", text, re.MULTILINE)

    assert ay is not None
    assert az is not None
    assert az.start() > ay.start()

    section = re.split(r"^## ", text[az.start() + 3 :], maxsplit=1, flags=re.MULTILINE)[0]
    for number in range(1, 15):
        assert re.search(rf"^- \*\*R{number} ", section, re.MULTILINE)
    for required in ("to-cc/GO-E3.0.md", "grok-4.7", "e30-bootstrap"):
        assert required in section
    assert section.count("Carried by:") >= 14


def test_adr_130_go_e30_amendment_preserves_d3():
    path = ROOT / "docs" / "decisions" / "ADR-130-the-outer-loop-runs-in-code.md"
    text = path.read_text(encoding="utf-8")
    status = next(line for line in text.splitlines() if line.startswith("- **Status:**"))
    for required in ("Accepted", "D1, D2, D4, D5", "re-open", "D6", "E3.1"):
        assert required in status

    amendment = re.search(
        r"^## Amendment[^\n]*GO-E3\.0 R1[^\n]*\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert amendment is not None
    for required in (
        "python-statemachine 3.2.2",
        "DIGEST-E21-P1-SPIKE-2026-10-20",
        "[#669]",
        "D6",
    ):
        assert required in amendment.group(1)

    original_d3 = (
        "- **D3 — `[#669]`'s transitions on python-statemachine ==3.2.1 if the Q14a "
        "spike passes, else a stdlib table.** Not built here: the spike is `[#669]`'s "
        "step 0 (CHALLENGE M4); no dependency is added by this ADR's first step."
    )
    assert original_d3 in text.splitlines()
