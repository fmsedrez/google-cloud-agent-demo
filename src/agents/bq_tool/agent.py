"""BigQuery agent using ADK built-in tools."""

from google.adk.agents import LlmAgent

from . import prompt

MODEL = "gemini-2.0-flash"

from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
import google.auth

# Write modes define BigQuery access control of agent:
# ALLOWED: Tools will have full write capabilites.
# BLOCKED: Default mode. Effectively makes the tool read-only.
# PROTECTED: Only allows writes on temporary data for a given BigQuery session.
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)
# Initialize the tools to use the application default credentials.
application_default_credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(
    credentials=application_default_credentials
)
bigquery_toolset = BigQueryToolset(credentials_config=credentials_config, tool_filter=[
    'list_dataset_ids',
    'get_dataset_info',
    'list_table_ids',
    'get_table_info',
    'execute_sql',
])
bq_tool_agent = LlmAgent(
    model=MODEL,
    name="bq_tool_agent",
    description="Agente especializado em análise de dados do BigQuery usando ferramentas nativas do ADK",
    instruction=prompt.bq_tool_prompt(),
    tools=[bigquery_toolset]
)
root_agent = bq_tool_agent
# one good question: look in the thelook_ecommerce dataset in the bigquery-public-data project. What are the top-selling products?