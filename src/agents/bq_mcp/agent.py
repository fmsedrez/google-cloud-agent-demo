"""BigQuery agent using MCP (Model Context Protocol)."""

from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

from . import prompt

bigquery_toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
bigquery_toolset = bigquery_toolbox.load_toolset()
MODEL = "gemini-2.0-flash"
# MCP configuration for BigQuery
# Note: Requires MCP server configuration for BigQuery in your environment
bq_mcp_agent = Agent(
    model=MODEL,
    name="bq_mcp_agent",
    description="Agente especializado em análise de dados do BigQuery usando MCP (Model Context Protocol) para gerenciamento centralizado de ferramentas",
    instruction=prompt.bq_mcp_prompt(),
    tools=bigquery_toolset  # MCP toolset provides centralized database access
)
root_agent = bq_mcp_agent
# one good question: look in the thelook_ecommerce dataset in the bigquery-public-data project. What are the top-selling products?
