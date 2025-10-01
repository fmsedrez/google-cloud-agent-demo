"""sommelie_agent for finding good armonizations."""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-flash-lite"

sommelie_agent = LlmAgent(
    model=MODEL,
    name="sommelie_agent",
    description="Agente que pode pesquisar informações sobre as melhores formas de harmonizar pratos com bebidas na "
                "Internet usando o Google Search.",
    instruction=prompt.sommelie_prompt(),
    tools=[google_search]
)

root_agent = sommelie_agent
