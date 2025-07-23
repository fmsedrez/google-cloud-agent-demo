"""restaurant_concierge for providing restaurant recommendations and concierge services"""

from google.adk import Agent

from . import prompt

MODEL = "gemini-2.5-flash"

restaurant_concierge_agent = Agent(
    model=MODEL,
    name="restaurant_concierge_agent",
    description="Agente que pode fornecer recomendações de restaurantes, informações detalhadas e assistência com reservas.",
    instruction=prompt.restaurant_concierge_prompt(),
)
