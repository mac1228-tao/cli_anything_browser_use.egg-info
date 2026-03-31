#!/usr/bin/env python3
"""Browser-Use CLI — A command-line interface for browser-use library.

This CLI provides browser automation using AI agents powered by LLMs.

Usage:
    # One-shot commands
    cli-anything-browser-use agent run "Search for latest news"
    cli-anything-browser-use browser open https://example.com
    cli-anything-browser-use --json agent run "Find the title"

    # Interactive REPL
    cli-anything-browser-use
"""

import sys
import json
import asyncio
import shlex
from typing import Optional

import click

from cli_anything.browser_use.core.session import Session
from cli_anything.browser_use.core import agent as agent_mod
from cli_anything.browser_use.core import browser as browser_mod
from cli_anything.browser_use.utils import browser_use_backend as backend

_session: Optional[Session] = None
_json_output = False
_repl_mode = False


def get_session() -> Session:
    global _session
    if _session is None:
        _session = Session()
    return _session


def output(data, message: str = ""):
    if _json_output:
        click.echo(json.dumps(data, indent=2, default=str))
    else:
        if message:
            click.echo(message)
        if isinstance(data, dict):
            _print_dict(data)
        elif isinstance(data, list):
            _print_list(data)
        else:
            click.echo(str(data))


def _print_dict(d: dict, indent: int = 0):
    prefix = "  " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            click.echo(f"{prefix}{k}:")
            _print_dict(v, indent + 1)
        elif isinstance(v, list):
            click.echo(f"{prefix}{k}:")
            _print_list(v, indent + 1)
        else:
            click.echo(f"{prefix}{k}: {v}")


def _print_list(items: list, indent: int = 0):
    prefix = "  " * indent
    for i, item in enumerate(items):
        if isinstance(item, dict):
            click.echo(f"{prefix}[{i}]")
            _print_dict(item, indent + 1)
        else:
            click.echo(f"{prefix}- {item}")


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RuntimeError as e:
            if _json_output:
                click.echo(json.dumps({"error": str(e), "type": "runtime_error"}))
            else:
                click.echo(f"Error: {e}", err=True)
            if not _repl_mode:
                sys.exit(1)
        except (ValueError, IndexError) as e:
            if _json_output:
                click.echo(json.dumps({"error": str(e), "type": type(e).__name__}))
            else:
                click.echo(f"Error: {e}", err=True)
            if not _repl_mode:
                sys.exit(1)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@click.group(invoke_without_command=True)
@click.option("--json", "use_json", is_flag=True, help="Output as JSON")
@click.pass_context
def cli(ctx, use_json):
    """Browser-Use CLI — AI-powered browser automation.

    Run without a subcommand to enter interactive REPL mode.
    """
    global _json_output
    _json_output = use_json

    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


@cli.group()
def agent():
    """Agent commands for running browser automation tasks."""
    pass


@agent.command("run")
@click.argument("task")
@click.option("--model", default="browser-use", help="LLM model to use")
@click.option("--max-steps", default=100, help="Maximum steps per task")
@click.option("--headless/--headed", default=None, help="Run browser headless or headed")
@handle_error
def agent_run(task, model, max_steps, headless):
    """Run a browser automation task."""
    sess = get_session()
    result = asyncio.run(agent_mod.run_task(sess, task, model, max_steps, headless))
    output(result, f"Task completed: {task[:50]}...")


@agent.command("history")
@handle_error
def agent_history():
    """Show task execution history."""
    sess = get_session()
    result = agent_mod.get_history(sess)
    output(result)


@agent.command("undo")
@click.argument("steps", default=1)
@handle_error
def agent_undo(steps):
    """Undo previous agent actions."""
    sess = get_session()
    result = agent_mod.undo(sess, steps)
    output(result, f"Undone {steps} step(s)")


@agent.command("redo")
@click.argument("steps", default=1)
@handle_error
def agent_redo(steps):
    """Redo previously undone agent actions."""
    sess = get_session()
    result = agent_mod.redo(sess, steps)
    output(result, f"Redone {steps} step(s)")


@cli.group()
def browser():
    """Browser session management commands."""
    pass


@browser.command("open")
@click.argument("url")
@click.option("--headless/--headed", default=None, help="Run browser headless or headed")
@handle_error
def browser_open(url, headless):
    """Open a URL in the browser."""
    sess = get_session()
    result = asyncio.run(browser_mod.open_url(sess, url, headless))
    output(result, f"Opened: {url}")


@browser.command("close")
@handle_error
def browser_close():
    """Close the current browser session."""
    sess = get_session()
    result = asyncio.run(browser_mod.close_browser(sess))
    output(result, "Browser closed")


@browser.command("info")
@handle_error
def browser_info():
    """Show current browser information."""
    sess = get_session()
    result = browser_mod.get_info(sess)
    output(result)


@browser.command("screenshot")
@click.option("--path", "-p", default="screenshot.png", help="Screenshot output path")
@handle_error
def browser_screenshot(path):
    """Take a screenshot of the current page."""
    sess = get_session()
    result = asyncio.run(browser_mod.take_screenshot(sess, path))
    output(result, f"Screenshot saved to: {path}")


@cli.group()
def session():
    """Session management commands."""
    pass


@session.command("save")
@click.argument("name")
@handle_error
def session_save(name):
    """Save the current session."""
    sess = get_session()
    result = sess.save(name)
    output(result, f"Session saved: {name}")


@session.command("load")
@click.argument("name")
@handle_error
def session_load(name):
    """Load a saved session."""
    sess = get_session()
    result = sess.load(name)
    output(result, f"Session loaded: {name}")


@session.command("list")
@handle_error
def session_list():
    """List all saved sessions."""
    sess = get_session()
    result = sess.list_sessions()
    output(result)


@session.command("status")
@handle_error
def session_status():
    """Show current session status."""
    sess = get_session()
    status = sess.status()
    output(status)


@cli.group()
def config():
    """Configuration management commands."""
    pass


@config.command("show")
@handle_error
def config_show():
    """Show current configuration."""
    result = backend.get_config()
    output(result)


@config.command("set")
@click.argument("key")
@click.argument("value")
@handle_error
def config_set(key, value):
    """Set a configuration value."""
    result = backend.set_config(key, value)
    output(result, f"Set {key} = {value}")


@cli.command()
@handle_error
def repl():
    """Start interactive REPL session."""
    from cli_anything.browser_use.utils.repl_skin import ReplSkin

    global _repl_mode
    _repl_mode = True

    skin = ReplSkin("browser-use", version="1.0.0")
    skin.print_banner()

    pt_session = skin.create_prompt_session()

    _repl_commands = {
        "agent": "run|history|undo|redo",
        "browser": "open|close|info|screenshot",
        "session": "save|load|list|status",
        "config": "show|set",
        "help": "Show this help",
        "quit": "Exit REPL",
    }

    while True:
        try:
            sess = get_session()
            context = sess.working_context if hasattr(sess, 'working_context') else "browser-use"

            line = skin.get_input(pt_session, context=context)
            if not line:
                continue
            if line.lower() in ("quit", "exit", "q"):
                skin.print_goodbye()
                break
            if line.lower() == "help":
                skin.help(_repl_commands)
                continue

            try:
                args = shlex.split(line)
            except ValueError:
                args = line.split()
            try:
                cli.main(args, standalone_mode=False)
            except SystemExit:
                pass
            except click.exceptions.UsageError as e:
                skin.warning(f"Usage error: {e}")
            except Exception as e:
                skin.error(f"{e}")

        except (EOFError, KeyboardInterrupt):
            skin.print_goodbye()
            break

    _repl_mode = False


def main():
    cli()


if __name__ == "__main__":
    main()
