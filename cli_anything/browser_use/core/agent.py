"""Agent commands for browser-use CLI."""

import asyncio
from typing import Any, Optional

from cli_anything.browser_use.core.session import Session
from cli_anything.browser_use.utils import browser_use_backend as backend


async def _get_agent_session(session: Session):
    """Get or create browser session and agent."""
    agent = await backend.get_agent(session)
    return agent


def run_task(
    session: Session,
    task: str,
    model: str = "browser-use",
    max_steps: int = 100,
    headless: Optional[bool] = None,
) -> dict[str, Any]:
    """Run a browser automation task."""
    try:
        agent = asyncio.run(backend.create_agent(task, model, max_steps, headless))
        history = asyncio.run(agent.run())
        
        result = {
            "task": task,
            "model": model,
            "steps": history.number_of_steps() if hasattr(history, 'number_of_steps') else 0,
            "urls": history.urls() if hasattr(history, 'urls') else [],
            "final_result": history.final_result() if hasattr(history, 'final_result') else None,
            "success": history.is_done() if hasattr(history, 'is_done') else True,
        }
        
        session.add_to_history({
            "type": "agent_run",
            "task": task,
            "result": result,
        })
        
        return result
    except Exception as e:
        return {"error": str(e), "task": task}


def get_history(session: Session) -> dict[str, Any]:
    """Get task execution history."""
    return {
        "history": session.history,
        "undo_stack": session.undo_stack,
        "redo_stack": session.redo_stack,
    }


def undo(session: Session, steps: int = 1) -> dict[str, Any]:
    """Undo previous agent actions."""
    result = session.undo(steps)
    return {"undone": len(result.get("undone", [])), "steps": steps}


def redo(session: Session, steps: int = 1) -> dict[str, Any]:
    """Redo previously undone actions."""
    result = session.redo(steps)
    return {"redone": len(result.get("redone", [])), "steps": steps}
