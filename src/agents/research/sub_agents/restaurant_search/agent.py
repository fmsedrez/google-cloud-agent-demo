"""restaurant_search_agent for finding restaurant using search tools"""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"

restaurant_search_agent = Agent(
    model=MODEL,
    name="restaurant_search_agent",
    instruction=prompt.restaurant_search_prompt(),
    tools=[google_search]
)
