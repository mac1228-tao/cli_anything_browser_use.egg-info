# Browser-Use CLI Test Plan

## Test Inventory

- `test_core.py`: 10 unit tests planned
- `test_full_e2e.py`: 5 E2E tests planned

## Unit Test Plan

### Module: session.py
- `test_session_status` - Verify session status returns correct structure
- `test_session_save` - Verify session can be saved to disk
- `test_session_load` - Verify session can be loaded from disk
- `test_session_list` - Verify saved sessions can be listed
- `test_session_undo` - Verify undo stack works correctly
- `test_session_redo` - Verify redo stack works correctly
- `test_session_add_to_history` - Verify history is tracked

### Module: agent.py
- `test_agent_run_returns_dict` - Verify agent run returns expected dict structure

### Module: browser.py
- `test_browser_info` - Verify browser info returns expected structure
- `test_open_url_validation` - Verify URL validation

### Edge Cases
- Invalid URL handling
- Missing API key handling
- Browser not installed handling

## E2E Test Plan

### Realistic Workflow Scenarios

1. **Basic Task Execution**
   - Simulates: Running a simple browser automation task
   - Operations: agent run with simple task
   - Verified: Result contains task, model, steps fields

2. **Session Persistence**
   - Simulates: Saving and loading session state
   - Operations: session save, session list, session load
   - Verified: Session can be saved and restored

3. **Browser Control**
   - Simulates: Opening URL and getting info
   - Operations: browser open, browser info
   - Verified: Browser state is tracked

4. **Configuration Management**
   - Simulates: Setting and getting configuration
   - Operations: config set, config show
   - Verified: Configuration persists

5. **JSON Output Mode**
   - Simulates: Using CLI in agent mode
   - Operations: Any command with --json flag
   - Verified: Output is valid JSON

## Test Execution

Run tests with:
```bash
cd agent-harness
pip install -e .
CLI_ANYTHING_FORCE_INSTALLED=1 python3 -m pytest cli_anything/browser_use/tests/ -v
```

## Notes

- Browser-use requires Chromium to be installed for full E2E tests
- API key is required for LLM-based tasks
- Some tests may be skipped if dependencies are not available
