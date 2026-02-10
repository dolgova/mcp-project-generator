# MCP Project Generator

## Why This Project Exists

“turning job descriptions into AI architecture artifacts”

“demonstrates senior/staff readiness”

“portfolio-driven MCP systems”

### Turning Any Job Description into an AI-Driven Architecture & Portfolio Project

This repository provides a **repeatable framework** and a **Python MCP server** for transforming any technical job description into:

- An AI + MCP project concept  
- A structured architecture case study  
- A senior-level technical portfolio artifact  

You can use it in three ways:

1. **Manual (prompt-only)** – Copy the prompt and template into ChatGPT (or another LLM) and paste a job description.
2. **MCP server with real LLM** – Run the included Python MCP server and let tools generate and save project specs directly from Cursor or another MCP host (requires `OPENAI_API_KEY`).
3. **MCP server in local test mode** – Run the server without `OPENAI_API_KEY` to generate deterministic stub specs that exercise the full pipeline without external API calls.

---

## Repository Structure

```
template/   → Universal MCP project document structure  
prompts/    → Ready-to-use generation prompt  
examples/   → Sample generated projects  
project_generator.py → LLM + file-writing logic  
server.py   → MCP server exposing project generation tools  
requirements.txt → Python dependencies  
generated_projects/ → (created at runtime) generated project folders  
```

---

## Setup

From the `mcp-project-generator` directory:

```bash
python -m venv .venv
.venv\Scripts\activate    # PowerShell / Windows
pip install -r requirements.txt
```

Set your OpenAI environment variables (PowerShell example) **for real LLM calls**:

```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:OPENAI_MODEL = "gpt-4o-mini"   # optional
```

If you **do not** set `OPENAI_API_KEY`, the server will run in a local **test mode**:

- No external API calls are made.
- Generated specs are clearly marked as test output but still written to `generated_projects/<slug>/project_spec.md`.

---

## Run the MCP server

```bash
python server.py
```

The server uses stdio transport (stdin/stdout) and exposes tools under the server id `mcp-project-generator`.

### Cursor MCP config

Add this server to Cursor’s MCP configuration (for example in `~/.cursor/mcp.json`). For best results, point Cursor at the Python inside this project’s virtualenv:

```json
{
  "mcpServers": {
    "mcp-project-generator": {
      "command": "C:\\Users\\dolgo\\Desktop\\ai_projects\\mcp-project-generator\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\dolgo\\Desktop\\ai_projects\\mcp-project-generator\\server.py"]
    }
  }
}
```

---

## Tools

### `generate_portfolio_project_from_text`

- **Arguments**:
  - `job_description` (string) – raw job description text.
  - `project_name` (optional string) – preferred project title.
- **Behavior**:
  - Uses `prompts/generate_mcp_project.txt` and `template/MCP_Project_Template.md`.
  - If `OPENAI_API_KEY` is set, calls the configured OpenAI model to generate a structured Markdown project spec.
  - If `OPENAI_API_KEY` is **not** set, runs in local test mode and generates a small deterministic stub spec (useful for wiring tests).
  - Writes the result to `generated_projects/<slug>/project_spec.md`.
  - Returns a human-readable summary plus the full Markdown content.

### `generate_portfolio_project_from_url`

- **Arguments**:
  - `url` (string) – publicly accessible job description URL.
  - `project_name` (optional string).
- **Behavior**:
  - Fetches and lightly cleans the page content as a job description.
  - Delegates to the same generator as `generate_portfolio_project_from_text`.
  - Saves and returns the spec in the same way.

---

## Example: Arista Technical Solutions Engineer project

The `examples/arista-technical-solutions-engineer.md` file shows a fully written project spec for:

- **Role**: Technical Solutions Engineer – Cloud, Hyperscalers and AI Networks.
- **Concept**: A “Network TAC AI Copilot” that uses MCP tools to:
  - Collect telemetry from AI / hyperscale fabrics (L1–L3, QoS/PFC, optics, SONiC, Linux).
  - Run structured diagnostics (e.g. `get_interface_errors`, `get_bgp_flaps`, `capture_packets`).
  - Produce TAC-style root cause analyses and customer-ready reports.

This serves as a reference for how to align an MCP project with a specific job description while clearly demonstrating networking depth, troubleshooting skill, and customer-facing communication.

---

## Manual prompt-only usage

If you prefer not to run the MCP server:

1. Copy a job description.
2. Open `prompts/generate_mcp_project.txt` and paste its contents into ChatGPT.
3. Paste the job description when prompted.
4. Use `template/MCP_Project_Template.md` as a reference for structure.
5. Save the generated architecture as a new project file in `examples/`.

---

## Goal

Help engineers demonstrate:

- Architecture thinking  
- AI-driven automation design  
- Business-aware engineering  
- Senior / Staff readiness  

---

## License

MIT
