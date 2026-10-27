import sys
sys.path.insert(0,"scripts")
import subprocess, pathlib, journal_anchor
r=pathlib.Path(".").resolve()
print(journal_anchor.range_is_anchored(r,"origin/main..HEAD",(r/"JOURNAL.md").read_text(encoding="utf-8")))
