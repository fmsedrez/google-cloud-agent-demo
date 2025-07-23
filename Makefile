.PHONY: help

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

venv: ## Create a virtual environment
	uv venv .venv

sync: ## Syncronize the virtual environment with the requirements
	uv sync

source: ## Activate the virtual environment
	source .venv/bin/activate

gcloud_login: ## Login to Google Cloud
	gcloud auth application-default login --no-launch-browser

gcloud_ai_enable: ## Enable Google Cloud AI services
	gcloud services enable aiplatform.googleapis.com

api: ## Start the fastAPI server on port 8500
	.venv/bin/uvicorn src.api.main:app --host 127.0.0.1 --port 8500 --reload

streamlit: ## Start the Streamlit server on port 8501
	.venv/bin/streamlit run src/chatbot_streamlit/app.py --server.port 8501 --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false

gemini: ## Start the Gemini chatbot server on port 8502
	.venv/bin/streamlit run src/chatbot_gemini/app.py --server.port 8502 --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false

langchain: ## Start the Langchain chatbot server on port 8503
	.venv/bin/streamlit run src/chatbot_langchain_gemini/app.py --server.port 8503 --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false

langchain_tool: ## Start the Langchain chatbot with Gemini tool server on port 8504
	.venv/bin/streamlit run src/chatbot_langchain_gemini_tool/app.py --server.port 8504 --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false

adk: ## Start ADK Server
	uv run adk web src/agents --port 8505

adk_api: ## Start ADK API Server
	uv run adk api src/agents --port 8506

mcp_server: ## Start MCP Server
	uv run --directory src/mcp adk_mcp_server.py

mcp_client: ## Start MCP Client
	uv run adk web src/mcp --port 8507