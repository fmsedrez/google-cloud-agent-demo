from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

from . import prompt
from .sub_agents.booker.agent import booker_agent
from .sub_agents.chef.agent import chef_agent
from .sub_agents.planner.agent import planner_agent
from .sub_agents.sommelie.agent import sommelie_agent
from .sub_agents.transport.agent import transport_agent

# Convert specific agents to tools
transport_tool = agent_tool.AgentTool(agent=transport_agent)
sommelie_tool = agent_tool.AgentTool(agent=sommelie_agent)
planner_tool = agent_tool.AgentTool(agent=planner_agent)
chef_tool = agent_tool.AgentTool(agent=chef_agent)
booker_tool = agent_tool.AgentTool(agent=booker_agent)

# Root agent acting as a Concierge coordinator
concierge_agent = LlmAgent(
    model='gemini-2.5-pro',
    name="ConciergeAgent",
    description="Atua como um planejador abrangente e serviço de concierge que coordena especialistas em transporte, gastronomia, hospedagem, experiências e harmonização",
    instruction=prompt.concierge_prompt(),
    tools=[
        transport_tool,
        sommelie_tool,
        planner_tool,
        chef_tool,
        booker_tool
    ]  # The coordinator manages these tools
)

root_agent = concierge_agent
