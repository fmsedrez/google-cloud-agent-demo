"""Restaurant_Search: Restaurant finder based on user preferences, dining options, reviews, and recommendations."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.restaurant_concierge import restaurant_concierge_agent
from .sub_agents.restaurant_search import restaurant_search_agent

MODEL = "gemini-2.5-pro"

agent_coordinator = LlmAgent(
    name="agent_coordinator",
    model=MODEL,
    description=(
        "searching for restaurants based on user preferences, "
        "finding quality dining options, collecting detailed restaurant information, "
        "gathering customer reviews, comparing different establishments, "
        "and providing organized recommendations to help users "
        "make informed dining decisions"
    ),
    instruction=prompt.root_agent_instructions(),
    tools=[
        AgentTool(agent=restaurant_concierge_agent),
        AgentTool(agent=restaurant_search_agent),
    ],
)

root_agent = agent_coordinator
