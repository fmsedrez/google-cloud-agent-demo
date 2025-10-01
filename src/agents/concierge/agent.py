from google.adk.agents import LlmAgent

from . import prompt
from .sub_agents.booker.agent import booker_agent
from .sub_agents.chef.agent import chef_agent
from .sub_agents.planner.agent import planner_agent
from .sub_agents.sommelie.agent import sommelie_agent
from .sub_agents.transport.agent import transport_agent

# Root agent acting as a Concierge coordinator
concierge_agent = LlmAgent(
    model='gemini-2.5-pro',
    name="ConciergeAgent",
    description="Atua como um planejador abrangente e serviço de concierge que coordena especialistas em transporte, gastronomia, hospedagem, experiências e harmonização",
    instruction=prompt.concierge_prompt(),
    sub_agents=[
        transport_agent,
        sommelie_agent,
        planner_agent,
        chef_agent,
        booker_agent
    ]  # The coordinator manages these sub-agents
)

root_agent = concierge_agent
