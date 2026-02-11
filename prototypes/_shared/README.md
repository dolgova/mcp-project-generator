# Shared Copilot Utilities

Code shared across multiple MCP copilot prototypes (e.g. Arista TAC, future law-firm or generic TAC copilots).

## Intended contents (as prototypes are built)

- **`base_copilot.py`** – Optional: common FastMCP bootstrap or tool-registration helpers.
- **`rca_formatter.py`** – Format RCA output (root cause, remediation steps, customer summary) so all copilots return consistent, professional text.
- **Stub-loading helpers** – Load mock telemetry from JSON or dicts so copilots can run without real devices.

Until the first prototype is implemented, this folder is a placeholder. Each copilot can still be self-contained; move shared logic here when a second prototype is added.
