"""planner_agent for finding best experiences using search tools."""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-flash-lite"

planner_agent = LlmAgent(
    model=MODEL,
    name="planner_agent",
    description="Agente que pode pesquisar informações sobre as melhores opções de experiências para combinar com "
                "as preferências do usuário tornando a sua agenda mais agradável usando a Internet usando o Google Search.",
    instruction=prompt.planner_prompt(),
    tools=[google_search]
)

root_agent = planner_agent
