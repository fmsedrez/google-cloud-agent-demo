"""Academic_newresearch_agent for finding new research lines"""

from google.adk import Agent

from . import prompt

MODEL = "gemini-2.5-pro"

academic_newresearch_agent = Agent(
    model=MODEL,
    name="academic_newresearch_agent",
    instruction=prompt.ACADEMIC_NEWRESEARCH_PROMPT,
)
