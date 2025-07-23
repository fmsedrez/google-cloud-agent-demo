import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from .prompts import root_agent_instructions

MODEL = "gemini-2.5-flash"

root_agent = LlmAgent(
    model=MODEL,
    name='search_mcp_client_agent',
    description="Agente que pode pesquisar informações na Internet.",
    instruction=root_agent_instructions(),
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='uv',
                args=["--directory",
                      os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"),
                      "run",
                      "adk_mcp_server.py"],
            )
        )
    ],
)
