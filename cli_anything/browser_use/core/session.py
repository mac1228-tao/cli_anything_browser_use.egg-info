"""Session management for browser-use CLI."""

import json
import os
from pathlib import Path
from typing import Any, Optional


class Session:
    """Browser-Use CLI session management.
    
    Manages browser session state, history, and persistence.
    """

    def __init__(self):
        self.working_context = "browser-use"
        self.history = []
        self.undo_stack = []
        self.redo_stack = []
        self._session_dir = Path.home() / ".cli-anything-browser-use" / "sessions"
        self._session_dir.mkdir(parents=True, exist_ok=True)

    def status(self) -> dict[str, Any]:
        """Get current session status."""
        return {
            "context": self.working_context,
            "history_length": len(self.history),
            "undo_stack_length": len(self.undo_stack),
            "redo_stack_length": len(self.redo_stack),
            "session_dir": str(self._session_dir),
        }

    def save(self, name: str) -> dict[str, Any]:
        """Save session to disk."""
        session_file = self._session_dir / f"{name}.json"
        data = {
            "history": self.history,
            "undo_stack": self.undo_stack,
            "redo_stack": self.redo_stack,
        }
        with open(session_file, "w") as f:
            json.dump(data, f, indent=2)
        return {"saved": True, "path": str(session_file)}

    def load(self, name: str) -> dict[str, Any]:
        """Load session from disk."""
        session_file = self._session_dir / f"{name}.json"
        if not session_file.exists():
            raise FileNotFoundError(f"Session not found: {name}")
        with open(session_file) as f:
            data = json.load(f)
        self.history = data.get("history", [])
        self.undo_stack = data.get("undo_stack", [])
        self.redo_stack = data.get("redo_stack", [])
        return {"loaded": True, "name": name}

    def list_sessions(self) -> dict[str, Any]:
        """List all saved sessions."""
        sessions = []
        for f in self._session_dir.glob("*.json"):
            sessions.append({"name": f.stem, "path": str(f)})
        return {"sessions": sessions}

    def add_to_history(self, action: dict[str, Any]) -> None:
        """Add action to history and clear redo stack."""
        self.history.append(action)
        self.redo_stack.clear()

    def undo(self, steps: int = 1) -> dict[str, Any]:
        """Undo previous actions."""
        undone = []
        for _ in range(min(steps, len(self.history))):
            if self.history:
                action = self.history.pop()
                self.undo_stack.append(action)
                undone.append(action)
        return {"undone": undone}

    def redo(self, steps: int = 1) -> dict[str, Any]:
        """Redo previously undone actions."""
        redone = []
        for _ in range(min(steps, len(self.undo_stack))):
            if self.undo_stack:
                action = self.undo_stack.pop()
                self.history.append(action)
                redone.append(action)
        return {"redone": redone}
