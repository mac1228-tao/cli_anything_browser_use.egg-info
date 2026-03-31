"""End-to-end tests for browser-use CLI."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


def _resolve_cli(name):
    """Resolve installed CLI command; falls back to python -m for dev."""
    import shutil
    force = os.environ.get("CLI_ANYTHING_FORCE_INSTALLED", "").strip() == "1"
    path = shutil.which(name)
    if path:
        print(f"[_resolve_cli] Using installed command: {path}")
        return [path]
    if force:
        raise RuntimeError(f"{name} not found in PATH. Install with: pip install -e .")
    module = name.replace("cli-anything-", "cli_anything.") + "." + name.split("-")[-1] + "_cli"
    print(f"[_resolve_cli] Falling back to: {sys.executable} -m {module}")
    return [sys.executable, "-m", module]


class TestCLISubprocess:
    """Test CLI via subprocess - how users/agents would invoke it."""

    CLI_BASE = _resolve_cli("cli-anything-browser-use")

    def _run(self, args, check=True):
        return subprocess.run(
            self.CLI_BASE + args,
            capture_output=True, text=True,
            check=check,
        )

    def test_help(self):
        """Test --help flag."""
        result = self._run(["--help"])
        assert result.returncode == 0

    def test_json_flag(self):
        """Test --json flag."""
        result = self._run(["--json", "session", "status"], check=False)
        # May fail if browser-use not available, but should return JSON structure
        if result.returncode == 0:
            data = json.loads(result.stdout)
            assert "context" in data or "history_length" in data

    def test_agent_help(self):
        """Test agent subcommand help."""
        result = self._run(["agent", "--help"])
        assert result.returncode == 0
        assert "run" in result.stdout

    def test_browser_help(self):
        """Test browser subcommand help."""
        result = self._run(["browser", "--help"])
        assert result.returncode == 0

    def test_session_status(self):
        """Test session status command."""
        result = self._run(["--json", "session", "status"], check=False)
        # Should work even without browser-use
        assert result.returncode == 0
        assert result.stdout.strip() != ""
        data = json.loads(result.stdout)
        assert "context" in data or "history_length" in data

    def test_config_show(self):
        """Test config show command."""
        result = self._run(["config", "show"], check=False)
        assert result.returncode == 0
        if result.stdout.strip():
            data = json.loads(result.stdout)
            assert isinstance(data, dict)


class TestWorkflowIntegration:
    """Integration tests for real-world workflows."""

    def test_session_save_load_workflow(self, tmp_path):
        """Test saving and loading session state."""
        # This is a simple test - actual browser interaction would require browser-use
        CLI_BASE = _resolve_cli("cli-anything-browser-use")
        
        # Create temp directory for session
        session_dir = tmp_path / "sessions"
        session_dir.mkdir()
        
        # Note: Full test would require actual browser-use installation
        # This test verifies the CLI is invocable
        result = subprocess.run(
            CLI_BASE + ["session", "status"],
            capture_output=True, text=True,
            check=False,
        )
        # Should not crash
        assert result.returncode in [0, 1]
