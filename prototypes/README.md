# MCP Copilot Prototypes

This folder contains **dedicated MCP servers** for domain-specific AI copilots (e.g. Arista TAC, law-firm infrastructure). Each prototype is a self-contained MCP server with its own tools, stubs, and optional shared utilities.

## Layout

- **`_shared/`** – Shared code used by multiple copilots (e.g. base MCP setup, RCA formatting). Add modules here as you build more prototypes.
- **`arista-tac-copilot/`** – (To be added) Arista TAC AI Copilot: telemetry + RCA tools for hyperscale/AI networking troubleshooting.

## Adding a new copilot

1. Create a new subfolder under `prototypes/`, e.g. `prototypes/my-copilot/`.
2. Add `server.py` (FastMCP), `tools/`, `stubs/`, and a local `README.md` + `requirements.txt`.
3. Reuse helpers from `_shared/` where useful (e.g. RCA formatter, stub loader).

The root of this repo remains the **JD → project spec generator** (prompts, template, `server.py`, `project_generator.py`). Prototypes are separate MCP servers for specific domains.
