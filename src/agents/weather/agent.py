import python_weather
from google.adk.agents import Agent

from .prompts import root_agent_instructions

MODEL = "gemini-2.5-flash-lite"


async def get_weather(city: str) -> int:
    """Fetches the current temperature for a given city using the python_weather library."""
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)
        return weather.temperature


root_agent = Agent(
    name="weather_agent",
    model=MODEL,
    description="Agente usa API para buscar informações sobre o clima atual, previsões e condições meteorológicas.",
    instruction=root_agent_instructions(),
    tools=[get_weather]
)
