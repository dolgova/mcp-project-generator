"""MCP server for generating MCP-based portfolio projects from job descriptions."""

from mcp.server.fastmcp import FastMCP

from project_generator import (
    fetch_job_description_from_url,
    generate_project_from_text,
)

mcp = FastMCP("mcp-project-generator")


@mcp.tool()
async def generate_portfolio_project_from_text(
    job_description: str,
    project_name: str | None = None,
) -> str:
    """Generate a portfolio-ready MCP project spec from a raw job description string.

    Requires OPENAI_API_KEY (and optionally OPENAI_MODEL) to be set in the environment.
    The generated project will also be written to generated_projects/<slug>/project_spec.md.
    """
    try:
        result = await generate_project_from_text(
            job_description=job_description,
            project_name=project_name,
            write_to_disk=True,
        )
    except Exception as e:
        return f"Portfolio project generation failed: {e}"

    lines = [
        f"Project name: {result.get('project_name')}",
        f"Slug: {result.get('slug')}",
    ]
    path = result.get("path")
    if path:
        lines.append(f"Saved project spec to: {path}")
    lines.append("")
    lines.append(result.get("markdown", ""))
    return "\n".join(lines)


@mcp.tool()
async def generate_portfolio_project_from_url(
    url: str,
    project_name: str | None = None,
) -> str:
    """Fetch a job description from a public URL and generate a portfolio-ready MCP project spec.

    This first fetches and cleans the text from the URL, then calls the same generator as
    generate_portfolio_project_from_text. Output is saved to generated_projects/<slug>/project_spec.md.
    """
    try:
        jd_text = await fetch_job_description_from_url(url)
    except Exception as e:
        return f"Failed to fetch job description from URL: {e}"

    if not jd_text:
        return "Fetched page appears to be empty or could not be parsed into text."

    return await generate_portfolio_project_from_text(
        job_description=jd_text,
        project_name=project_name,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")

