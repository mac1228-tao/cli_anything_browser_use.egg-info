---
name: "cli-anything-browser-use"
description: "CLI harness for browser-use - AI-powered browser automation library"
---

# Browser-Use CLI

A command-line interface for browser-use, an AI-powered browser automation library that uses LLMs to autonomously interact with web pages.

## Installation

```bash
# Install browser-use
uv add browser-use

# Install Chromium
uvx browser-use install

# Install CLI
cd agent-harness
pip install -e .
```

## Commands

### Agent Commands
- `agent run <task>` - Run a browser automation task
- `agent history` - Show task execution history
- `agent undo [steps]` - Undo previous agent actions
- `agent redo [steps]` - Redo previously undone actions

### Browser Commands
- `browser open <url>` - Open a URL in browser
- `browser close` - Close browser session
- `browser info` - Show browser information
- `browser screenshot [-p PATH]` - Take a screenshot

### Session Commands
- `session save <name>` - Save current session
- `session load <name>` - Load a saved session
- `session list` - List all saved sessions
- `session status` - Show session status

### Config Commands
- `config show` - Show current configuration
- `config set <key> <value>` - Set a configuration value

## Options

- `--json` - Output as JSON for machine parsing

## Usage Examples

```bash
# Run a task
cli-anything-browser-use agent run "Search for latest AI news"

# Open URL
cli-anything-browser-use browser open https://example.com

# Get info in JSON format
cli-anything-browser-use --json browser info

# Save session
cli-anything-browser-use session save my-work
```

## Output Format

All commands support JSON output via `--json` flag:
```bash
cli-anything-browser-use --json agent run "Find the title"
```

Output includes:
- Task results and extracted content
- URLs visited during execution
- Step count and execution status

## Requirements

- Python 3.10+
- browser-use library
- Chromium browser
- API key (BROWSER_USE_API_KEY recommended)
