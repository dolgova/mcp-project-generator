"""Project generator utilities for turning job descriptions into MCP-based portfolio projects.

This module:
- Loads prompt and template files from the local repo.
- Calls an LLM to generate a structured Markdown project spec.
- Optionally writes the spec to generated_projects/<slug>/project_spec.md.

By default this uses OpenAI's API. Set:
- OPENAI_API_KEY   (required for real LLM calls)
- OPENAI_MODEL     (optional, defaults to gpt-4o-mini)

If OPENAI_API_KEY is **not** set, the module falls back to a local \"test mode\" that
generates a simple, deterministic stub project spec. This allows end-to-end plumbing
tests (MCP tools, file writing, slugs, etc.) without any external API calls.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, Dict, Optional

import httpx

try:
    from openai import OpenAI  # type: ignore[import]
except Exception:  # pragma: no cover - library may not be installed yet
    OpenAI = None  # type: ignore[assignment]


BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
TEMPLATE_DIR = BASE_DIR / "template"
GENERATED_DIR = BASE_DIR / "generated_projects"


def _load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return path.read_text(encoding="utf-8")


def _slugify(name: str) -> str:
    name = name.strip().lower()
    if not name:
        return "portfolio-project"
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
    slug_chars = []
    prev_dash = False
    for ch in name.replace("_", "-").replace(" ", "-"):
        if ch.isalnum():
            slug_chars.append(ch.lower())
            prev_dash = False
        elif ch in "-.":
            if not prev_dash:
                slug_chars.append("-")
                prev_dash = True
        # ignore other characters
    slug = "".join(slug_chars).strip("-")
    return slug or "portfolio-project"


def _infer_title_from_markdown(markdown: str) -> Optional[str]:
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("#"):
            # Strip leading hashes and whitespace
            title = line.lstrip("#").strip()
            if title:
                return title
    return None


def _ensure_generated_dir() -> Path:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    return GENERATED_DIR


def _build_messages(job_description: str, project_name: Optional[str]) -> list[dict[str, str]]:
    prompt_text = _load_text(PROMPTS_DIR / "generate_mcp_project.txt")
    template_text = _load_text(TEMPLATE_DIR / "MCP_Project_Template.md")

    system_prompt = (
        "You are a Senior Solutions Architect and Technical Project Manager. "
        "You design MCP-based AI projects that demonstrate deep understanding of a given job "
        "description and the required skills. You always produce structured, professional "
        "Markdown following the provided template sections exactly."
    )

    user_parts = [
        "JOB DESCRIPTION:",
        job_description.strip(),
        "",
        "INSTRUCTIONS:",
        prompt_text.strip(),
        "",
        "TEMPLATE (STRUCTURE AND HEADINGS TO FOLLOW):",
        template_text.strip(),
    ]

    if project_name:
        user_parts.append("")
        user_parts.append(f"Use this working project name if it fits: {project_name.strip()}")

    user_content = "\n".join(user_parts)

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]


def _call_llm(job_description: str, project_name: Optional[str]) -> str:
    """Call the LLM or fall back to a local stub in test mode.

    If OPENAI_API_KEY is not set or the openai library is unavailable, we generate a
    small deterministic Markdown stub so the rest of the pipeline can be exercised
    without external dependencies.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        # Local stub: no external API calls. Keep it obviously marked as test output.
        jd_preview = job_description.strip()
        if len(jd_preview) > 600:
            jd_preview = jd_preview[:600] + " ..."

        title = project_name or "MCP Portfolio Project (Test Mode)"
        return (
            f"# {title}\n\n"
            "## Executive Purpose\n"
            "This is a **test-mode** project spec generated without calling an external LLM.\n"
            "It exists to verify MCP wiring, file generation, and prompt/template loading.\n\n"
            "## Domain & Knowledge Area\n"
            "Derived from the following job description snippet:\n\n"
            "```text\n"
            f"{jd_preview}\n"
            "```\n\n"
            "## Core MCP + AI Solution\n"
            "In a real run (with OPENAI_API_KEY set), this section would describe a full MCP\n"
            "architecture tailored to the role, including tools, data sources, and AI flows.\n\n"
            "## Portfolio Value\n"
            "This stub proves the generator pipeline works end-to-end (MCP tool → generator →\n"
            "file on disk) even when external LLM access is disabled.\n"
        )

    # Real LLM call path
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    client = OpenAI(api_key=api_key)
    messages = _build_messages(job_description, project_name)

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.4,
    )

    choice = response.choices[0]
    content = (choice.message.content or "").strip()
    if not content:
        raise RuntimeError("LLM returned an empty response.")
    return content


async def generate_project_from_text(
    job_description: str,
    project_name: Optional[str] = None,
    write_to_disk: bool = True,
) -> Dict[str, Any]:
    """Generate a portfolio project spec from a raw job description."""
    markdown = await asyncio.to_thread(_call_llm, job_description, project_name)

    inferred_title = _infer_title_from_markdown(markdown)
    final_name = project_name or inferred_title or "MCP Portfolio Project"
    slug = _slugify(final_name)

    folder_path: Optional[Path] = None
    if write_to_disk:
        root = _ensure_generated_dir()
        folder_path = root / slug
        folder_path.mkdir(parents=True, exist_ok=True)
        spec_path = folder_path / "project_spec.md"
        spec_path.write_text(markdown, encoding="utf-8")

    return {
        "project_name": final_name,
        "slug": slug,
        "path": str(folder_path) if folder_path is not None else None,
        "markdown": markdown,
    }


async def fetch_job_description_from_url(url: str) -> str:
    """Fetch and lightly clean a job description from a public URL."""
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        text = resp.text

    # Very lightweight cleanup: strip HTML tags crudely and collapse whitespace.
    # For v1 this is sufficient; can be improved later.
    import re

    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

