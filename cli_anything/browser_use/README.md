# Browser-Use CLI

A command-line interface for browser-use, an AI-powered browser automation library.

## Installation

1. Install browser-use:
```bash
uv add browser-use
```

2. Install Chromium:
```bash
uvx browser-use install
```

3. Set up your API key:
```bash
# In .env file
BROWSER_USE_API_KEY=your-key
# Or use other providers:
# OPENAI_API_KEY=your-key
# ANTHROPIC_API_KEY=your-key
# GOOGLE_API_KEY=your-key
```

4. Install this CLI:
```bash
cd agent-harness
pip install -e .
```

## Usage

### One-shot Commands

```bash
# Run a browser automation task
cli-anything-browser-use agent run "Search for latest AI news"

# Open a URL
cli-anything-browser-use browser open https://example.com

# Get browser info
cli-anything-browser-use browser info

# Take a screenshot
cli-anything-browser-use browser screenshot -p screenshot.png

# Save session
cli-anything-browser-use session save my-session

# Load session
cli-anything-browser-use session load my-session

# Show configuration
cli-anything-browser-use config show
```

### Interactive REPL

```bash
# Start interactive mode (default)
cli-anything-browser-use
```

### JSON Output

All commands support `--json` for machine-readable output:
```bash
cli-anything-browser-use --json agent run "Search for news"
```

## Commands

### Agent Commands
- `agent run <task>` - Run a browser automation task
- `agent history` - Show task execution history
- `agent undo` - Undo previous agent actions
- `agent redo` - Redo previously undone actions

### Browser Commands
- `browser open <url>` - Open a URL in browser
- `browser close` - Close browser session
- `browser info` - Show browser information
- `browser screenshot` - Take a screenshot

### Session Commands
- `session save <name>` - Save current session
- `session load <name>` - Load a saved session
- `session list` - List all saved sessions
- `session status` - Show session status

### Config Commands
- `config show` - Show current configuration
- `config set <key> <value>` - Set a configuration value

## Requirements

- Python 3.10+
- browser-use library
- Chromium browser (installed via `uvx browser-use install`)
- API key for LLM provider (Browser Use Cloud recommended)
