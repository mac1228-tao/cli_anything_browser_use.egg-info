# Browser-Use Harness

## Overview

This harness provides a CLI interface to browser-use, an AI-powered browser automation library that uses LLMs to autonomously interact with web pages.

## Architecture Analysis

### Backend
- **Library**: `browser-use` Python package
- **Browser Control**: Playwright + CDP (Chrome DevTools Protocol)
- **LLM Integration**: Supports OpenAI, Anthropic, Google, and custom LLM providers

### Data Model
- **Sessions**: BrowserSession with state, history, and CDP connection
- **Tasks**: Agent tasks with history (AgentHistoryList)
- **Actions**: Navigation, clicks, input, extraction, etc.

### Command Groups
1. **agent** - Run browser automation tasks
2. **browser** - Browser session management
3. **session** - State persistence and history
4. **config** - Configuration management

## Backend Integration

The harness wraps the browser-use Python library:
- `BrowserSession` for browser lifecycle
- `Agent` for task execution
- Tools for DOM interaction

## Key Features
- REPL mode for interactive sessions
- JSON output for agent consumption
- Session persistence
- Task history with undo capability
