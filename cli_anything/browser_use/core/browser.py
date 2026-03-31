"""Browser commands for browser-use CLI."""

import asyncio
from typing import Any, Optional

from cli_anything.browser_use.core.session import Session
from cli_anything.browser_use.utils import browser_use_backend as backend


async def open_url(session: Session, url: str, headless: Optional[bool] = None) -> dict[str, Any]:
    """Open a URL in the browser."""
    try:
        browser_session = await backend.create_browser_session(headless)
        await browser_session.navigate(url)
        
        session.working_context = url
        
        return {
            "opened": True,
            "url": url,
            "title": "N/A",
        }
    except Exception as e:
        return {"error": str(e), "url": url}


async def close_browser(session: Session) -> dict[str, Any]:
    """Close the browser session."""
    try:
        await backend.close_browser()
        session.working_context = "browser-use"
        return {"closed": True}
    except Exception as e:
        return {"error": str(e)}


def get_info(session: Session) -> dict[str, Any]:
    """Get browser information."""
    info = backend.get_browser_info()
    info["session_context"] = session.working_context
    return info


async def take_screenshot(session: Session, path: str) -> dict[str, Any]:
    """Take a screenshot of the current page."""
    try:
        screenshot_path = await backend.take_screenshot(path)
        return {
            "screenshot": True,
            "path": screenshot_path,
        }
    except Exception as e:
        return {"error": str(e)}
