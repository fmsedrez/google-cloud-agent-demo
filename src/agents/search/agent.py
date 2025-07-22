from google.adk.agents import Agent
from google.adk.tools import google_search

from .prompts import root_agent_instructions

MODEL = "gemini-2.5-flash-lite"

root_agent = Agent(
    name="search_agent",
    model=MODEL,
    description="Agente que pode pesquisar informações na web",
    instruction=root_agent_instructions(),
    tools=[google_search]
)
