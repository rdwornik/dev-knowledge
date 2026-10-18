Review-only task. Do not edit any file. Below is a code diff to scripts/read_gate.py. Its stated intent: `agy_argv_refusal` must refuse an `--add-dir` operand that is not an ABSOLUTE path (a POSIX path starting with `/` or a Windows drive path like `C:\` or `C:/`); a relative operand must not count as having a directory.

Decide whether the diff delivers that intent. Final message: line 1 is exactly `APPROVE` or `REQUEST-CHANGES`; then, if REQUEST-CHANGES, name the defect (the line and why it is wrong, with an input that shows it) in at most 4 sentences.

DIFF:
diff --git a/scripts/read_gate.py b/scripts/read_gate.py
index a9e1e0f4..71a90db6 100644
--- a/scripts/read_gate.py
+++ b/scripts/read_gate.py
@@ -409,7 +409,18 @@ def agy_argv_refusal(argv: Sequence[str]) -> Optional[str]:
     path; otherwise a one-line refusal. The documented agy read entry point is
     `scripts/read_gate.py` (absolute path + `--add-dir`)."""
     items = list(argv)
-    has_dir = any(a == "--add-dir" or a.startswith("--add-dir=") for a in items)
+    def _abs_operand(v: str) -> bool:
+        return bool(re.search(r"(?:[A-Za-z]:[\\/]|/)", v))
+
+    has_dir = False
+    for i, a in enumerate(items):
+        if a == "--add-dir":
+            nxt = items[i + 1] if i + 1 < len(items) else ""
+            if nxt and not nxt.startswith("-") and _abs_operand(nxt):
+                has_dir = True
+        elif a.startswith("--add-dir="):
+            if _abs_operand(a[len("--add-dir="):]):
+                has_dir = True
     prompts: list[str] = []
     for i, a in enumerate(items):
         if a in _PRINT_FLAGS and i + 1 < len(items):
