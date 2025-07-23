from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from .prompts import root_agent_instructions

MODEL = "gemini-2.5-flash-lite"

root_agent = LlmAgent(
    model=MODEL,
    name='simple_timeserver_agent',
    description="Agente que retorna o horário local.",
    instruction=root_agent_instructions(),
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='uv',
                args=[
                    "run",
                    "python3",
                    "-m",
                    "mcp_simple_timeserver"
                ],
            ),
        )
    ],
)
