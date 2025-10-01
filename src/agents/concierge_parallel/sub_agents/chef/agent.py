"""chef_agent for finding good dish advise."""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-flash-lite"

chef_agent = LlmAgent(
    model=MODEL,
    name="chef_agent",
    description="Agente que pode pesquisar informações sobre receitas culinárias, técnicas de cozinha e "
                "preparação de pratos usando a Internet usando o Google Search.",
    instruction=prompt.chef_prompt(),
    tools=[google_search]
)

root_agent = chef_agent
