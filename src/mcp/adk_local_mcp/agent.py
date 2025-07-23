from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from .prompts import root_agent_instructions

MODEL = "gemini-2.5-flash"
MCP_SERVER_SCRIPT = "src/mcp/adk_mcp_server.py"

root_agent = LlmAgent(
    model=MODEL,
    name='search_mcp_client_agent',
    description="Agente que pode pesquisar informações na Internet.",
    instruction=root_agent_instructions(),
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='python3',
                args=[MCP_SERVER_SCRIPT],
            )
        )
    ],
)
