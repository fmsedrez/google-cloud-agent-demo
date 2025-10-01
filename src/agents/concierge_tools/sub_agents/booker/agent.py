"""booker_agent for finding and booking accommodations and reservations."""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-flash-lite"

booker_agent = LlmAgent(
    model=MODEL,
    name="booker_agent",
    description="Agente que pode pesquisar informações sobre hospedagens, hotéis, pousadas, restaurantes e opções de "
                "acomodação e reservas gastronômicas usando a Internet usando o Google Search.",
    instruction=prompt.booker_prompt(),
    tools=[google_search]
)

root_agent = booker_agent
