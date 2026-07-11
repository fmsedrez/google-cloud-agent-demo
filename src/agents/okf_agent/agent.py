"""BigQuery agent using ADK built-in tools."""

from google.adk.agents import LlmAgent

from . import prompt

MODEL = "gemini-2.5-flash"

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
from google.auth.transport.requests import Request
if hasattr(application_default_credentials, "refresh"):
    try:
        application_default_credentials.refresh(Request())
    except Exception:
        pass

def create_file(path: str, content: str) -> str:
    """Creates a new file or overwrites an existing file with the given content.

    Args:
        path: The path to the file to create.
        content: The text content to write into the file.
    """
    import os
    try:
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully created file at: {path}"
    except Exception as e:
        return f"Error creating file at {path}: {str(e)}"


def list_directory(path: str = ".") -> list[str]:
    """Lists the contents of a directory.

    Args:
        path: The path of the directory to list. Defaults to the current directory.
    """
    import os
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Error listing directory {path}: {str(e)}"]


def view_file(path: str) -> str:
    """Reads and returns the contents of a file.

    Args:
        path: The path of the file to view.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error viewing file {path}: {str(e)}"


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
    instruction=prompt.prompt(),
    tools=[bigquery_toolset, create_file, list_directory, view_file]
)
root_agent = bq_tool_agent

# look in the bigquery-public-data.thelook_ecommerce dataset and build the okf for this data