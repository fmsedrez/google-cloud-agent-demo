from google.adk.agents import LlmAgent
from google.adk.agents import SequentialAgent, ParallelAgent

from .sub_agents.booker.agent import booker_agent
from .sub_agents.chef.agent import chef_agent
from .sub_agents.planner.agent import planner_agent
from .sub_agents.sommelie.agent import sommelie_agent
from .sub_agents.transport.agent import transport_agent

# Create a parallel agent for concurrent tasks
plan_parallel = ParallelAgent(
    name="ParallelPlanner",
    sub_agents=[booker_agent, planner_agent],  # These run in parallel
)

menu_sequence = SequentialAgent(
    name="menu_planner",
    sub_agents=[chef_agent, sommelie_agent],  # These run in sequence
)

# Create a summary agent to gather results
trip_summary = LlmAgent(
    name="TripSummaryAgent",
    model='gemini-2.5-pro',
    instruction="Resuma os detalhes fornecidos pelos agentes",
    output_key="trip_summary")

# Root agent acting as a Concierge coordinator sequential agent to orchestrate the full workflow
concierge_agent = SequentialAgent(
    name="ConciergeAgent",
    description="Atua como um planejador abrangente e serviço de concierge que coordena especialistas em transporte, gastronomia, hospedagem, experiências e harmonização",
    # Run tasks in a specific order, including the parallel step
    sub_agents=[
        plan_parallel,
        transport_agent,
        menu_sequence,
        trip_summary
    ]  # The coordinator manages these tools
)

root_agent = concierge_agent
