"""Unit tests for browser-use CLI core modules."""

import json
import tempfile
from pathlib import Path

import pytest

from cli_anything.browser_use.core.session import Session
from cli_anything.browser_use.utils import browser_use_backend as backend


class TestSession:
    """Test session management."""

    def test_session_status(self):
        """Verify session status returns correct structure."""
        sess = Session()
        status = sess.status()
        
        assert "context" in status
        assert "history_length" in status
        assert status["history_length"] == 0

    def test_session_save_load(self, tmp_path):
        """Verify session can be saved and loaded."""
        # Override session dir
        sess = Session()
        sess._session_dir = tmp_path
        
        # Add some history
        sess.add_to_history({"type": "test", "data": "value"})
        
        # Save
        result = sess.save("test-session")
        assert result["saved"] is True
        
        # Create new session and load
        sess2 = Session()
        sess2._session_dir = tmp_path
        result = sess2.load("test-session")
        assert result["loaded"] is True
        assert len(sess2.history) == 1

    def test_session_list(self, tmp_path):
        """Verify saved sessions can be listed."""
        sess = Session()
        sess._session_dir = tmp_path
        sess.save("session1")
        sess.save("session2")
        
        result = sess.list_sessions()
        assert "sessions" in result
        assert len(result["sessions"]) >= 2

    def test_session_undo_redo(self):
        """Verify undo/redo functionality."""
        sess = Session()
        
        # Add actions
        sess.add_to_history({"action": 1})
        sess.add_to_history({"action": 2})
        sess.add_to_history({"action": 3})
        
        assert len(sess.history) == 3
        
        # Undo
        result = sess.undo(2)
        assert len(result["undone"]) == 2
        assert len(sess.history) == 1
        
        # Redo
        result = sess.redo(1)
        assert len(result["redone"]) == 1
        assert len(sess.history) == 2

    def test_session_add_to_history(self):
        """Verify history is tracked and redo is cleared."""
        sess = Session()
        sess.add_to_history({"action": "first"})
        sess.add_to_history({"action": "second"})
        
        assert len(sess.history) == 2
        assert len(sess.redo_stack) == 0


class TestBackend:
    """Test backend utilities."""

    def test_is_available(self):
        """Check if backend reports availability."""
        available, msg = backend.is_available()
        assert isinstance(available, bool)
        assert isinstance(msg, str)

    def test_config_operations(self):
        """Test configuration get/set."""
        # Set
        result = backend.set_config("test_key", "test_value")
        assert result["set"] is True
        
        # Get
        config = backend.get_config()
        assert "test_key" in config
        assert config["test_key"] == "test_value"


class TestCLI:
    """Test CLI command parsing."""

    def test_cli_help(self):
        """Verify CLI help works."""
        from click.testing import CliRunner
        from cli_anything.browser_use.browser_use_cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        
        assert result.exit_code == 0
        assert "Browser-Use CLI" in result.output

    def test_agent_help(self):
        """Verify agent subcommand help works."""
        from click.testing import CliRunner
        from cli_anything.browser_use.browser_use_cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ["agent", "--help"])
        
        assert result.exit_code == 0

    def test_browser_help(self):
        """Verify browser subcommand help works."""
        from click.testing import CliRunner
        from cli_anything.browser_use.browser_use_cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ["browser", "--help"])
        
        assert result.exit_code == 0

    def test_session_help(self):
        """Verify session subcommand help works."""
        from click.testing import CliRunner
        from cli_anything.browser_use.browser_use_cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ["session", "--help"])
        
        assert result.exit_code == 0

    def test_config_help(self):
        """Verify config subcommand help works."""
        from click.testing import CliRunner
        from cli_anything.browser_use.browser_use_cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "--help"])
        
        assert result.exit_code == 0
