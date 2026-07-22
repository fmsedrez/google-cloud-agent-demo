from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

# Unified Concierge agent with all specializations
concierge_agent = LlmAgent(
    model='gemini-2.5-pro',
    name="ConciergeAgent",
    description="Concierge inteligente especializado em transporte, gastronomia (chef), harmonização (sommelier), planejamento de experiências e hospedagem/reservas",
    instruction=prompt.concierge_prompt(),
    tools=[google_search]
)

root_agent = concierge_agent
