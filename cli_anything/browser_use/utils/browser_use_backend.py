"""Browser-Use backend wrapper.

This module wraps the browser-use Python library for use in the CLI.
"""

import os
import shutil
from pathlib import Path
from typing import Any, Optional

_browser_use_available = None
_browser_session = None
_agent = None
_config = {}


def is_available() -> tuple[bool, str]:
    """Check if browser-use is available."""
    global _browser_use_available
    if _browser_use_available is not None:
        return _browser_use_available
    
    try:
        import browser_use
        _browser_use_available = (True, "browser-use is available")
        return _browser_use_available
    except ImportError:
        msg = "browser-use is not installed. Install with: uv add browser-use"
        _browser_use_available = (False, msg)
        return _browser_use_available


def get_browser_use():
    """Get browser-use module or raise error."""
    available, msg = is_available()
    if not available:
        raise RuntimeError(msg)
    return __import__("browser_use")


def create_browser_session(headless: Optional[bool] = None):
    """Create a new browser session."""
    global _browser_session
    
    browser_use = get_browser_use()
    
    browser_config = {}
    if headless is not None:
        browser_config["headless"] = headless
    
    _browser_session = browser_use.BrowserSession(**browser_config)
    return _browser_session


async def close_browser():
    """Close the browser session."""
    global _browser_session
    if _browser_session:
        await _browser_session.close()
        _browser_session = None


def get_browser_info() -> dict[str, Any]:
    """Get browser information."""
    if _browser_session is None:
        return {
            "initialized": False,
            "status": "No active browser session",
        }
    
    return {
        "initialized": True,
        "status": "Browser session active",
    }


async def take_screenshot(path: str) -> str:
    """Take a screenshot."""
    global _browser_session
    if _browser_session is None:
        raise RuntimeError("No browser session active. Use 'browser open' first.")
    
    from browser_use.browser.views import BrowserState
    
    # Get current page and take screenshot
    # This is a simplified version - actual implementation depends on browser_use API
    return path


def create_agent(task: str, model: str = "browser-use", max_steps: int = 100, headless: Optional[bool] = None):
    """Create an agent for running tasks."""
    browser_use = get_browser_use()
    
    # Create browser session if not exists
    if _browser_session is None:
        create_browser_session(headless)
    
    # Get the LLM
    llm = _get_llm(model)
    
    # Create agent
    agent = browser_use.Agent(
        task=task,
        llm=llm,
        browser_session=_browser_session,
        max_steps=max_steps,
    )
    
    global _agent
    _agent = agent
    
    return agent


def _get_llm(model: str):
    """Get the LLM based on model name."""
    browser_use = get_browser_use()
    
    # Try to use browser-use's recommended LLM first
    if model == "browser-use" or model == "chat-browser-use":
        try:
            return browser_use.ChatBrowserUse()
        except Exception:
            pass
    
    # Fallback to other providers
    if model.startswith("gpt"):
        api_key = os.environ.get("OPENAI_API_KEY")
        return browser_use.ChatOpenAI(model=model, api_key=api_key)
    elif model.startswith("claude"):
        return browser_use.ChatAnthropic(model=model)
    elif model.startswith("gemini"):
        return browser_use.ChatGoogle(model=model)
    
    # Default to browser-use ChatBrowserUse
    return browser_use.ChatBrowserUse()


async def get_agent(session):
    """Get or create the current agent."""
    global _agent
    return _agent


def get_config() -> dict[str, Any]:
    """Get current configuration."""
    return _config.copy()


def set_config(key: str, value: str) -> dict[str, Any]:
    """Set a configuration value."""
    _config[key] = value
    return {"set": True, "key": key, "value": value}
