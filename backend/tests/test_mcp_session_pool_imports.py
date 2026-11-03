import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest


@pytest.mark.parametrize("error_name", ["McpError", "MCPError"])
def test_session_pool_imports_with_supported_mcp_error_name(error_name):
    script = dedent(
        f"""
        import importlib

        exceptions = importlib.import_module("mcp.shared.exceptions")
        error_type = getattr(exceptions, "McpError", None) or getattr(exceptions, "MCPError")
        for name in ("McpError", "MCPError"):
            if hasattr(exceptions, name):
                delattr(exceptions, name)
        setattr(exceptions, {error_name!r}, error_type)

        session_pool = importlib.import_module("deerflow.mcp.session_pool")
        assert session_pool.McpError is error_type
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        check=False,
        cwd=Path(__file__).parents[1],
        env=os.environ.copy(),
        text=True,
    )

    assert result.returncode == 0, result.stderr
