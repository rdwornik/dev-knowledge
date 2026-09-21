"""Connection-test shim: point the User-scope `CLAUDE_PROMPTS_DIR` at the test's own transport.

On Windows `dispatch.windows_user_env` and `transport_report.windows_user_env` read the value from the
registry (HKCU\\Environment) and it wins over the process environment, so a test cannot redirect the
transport through `os.environ`. Without this shim `go_reader` and the lane-end report would read and
write the operator's REAL transport drive. Active only when `CT_TRANSPORT` is set; every other registry
read passes through. Loaded by putting this directory on `PYTHONPATH` of the moment's child processes.
"""
import os

try:
    import winreg
except ImportError:  # not Windows: the process environment is the only source, nothing to redirect
    winreg = None

if winreg is not None:
    _query = winreg.QueryValueEx

    def _query_value_ex(key, name):
        if name == "CLAUDE_PROMPTS_DIR" and os.environ.get("CT_TRANSPORT"):
            return os.environ["CT_TRANSPORT"], winreg.REG_SZ
        return _query(key, name)

    winreg.QueryValueEx = _query_value_ex
