"""transport_agent for finding good insights."""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-flash-lite"

transport_agent = LlmAgent(
    model=MODEL,
    name="transport_agent",
    description="Agente que pode pesquisar informações sobre as melhores formas de se deslocar até um destino na "
                "Internet usando o Google Search.",
    instruction=prompt.transport_prompt(),
    tools=[google_search]
)

root_agent = transport_agent
