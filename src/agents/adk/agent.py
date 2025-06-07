from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="location_search_agent",
    model="gemini-2.0-flash",
    description="Agent that can search the web for information",
    instruction="""

        You are a specialized AI assistant tasked with searching the web for information.

        **Request:**
        Search the web for the information you need.

        **Constraints and Guidelines for Suggestions:**
        1.  **Precise:** Search the web for the information you need without any additional information.

        **Output Format:**
        RETURN PLAN

    """,
    tools=[google_search]
)