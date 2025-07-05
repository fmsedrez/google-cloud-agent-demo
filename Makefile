.PHONY: help

help: ## Exibe a ajuda
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

venv: ## Cria o ambiente virtual
	uv venv .venv

sync: ## Sincroniza as dependências
	uv sync

api: ## Inicia o servidor FastAPI
	.venv/bin/uvicorn src.api.main:app --host 127.0.0.1 --port 8500 --reload

streamlit: ## Inicia o servidor Streamlit
	.venv/bin/streamlit run src/chatbot_streamlit/app.py --server.port 8501 --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false

gemini: ## Inicia o servidor Gemini
	.venv/bin/streamlit run src/chatbot_gemini/app.py --server.port 8502 --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false

langchain: ## Inicia o servidor Langchain
	.venv/bin/streamlit run src/chatbot_langchain_gemini/app.py --server.port 8503 --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false

langchain_tool: ## Inicia o servidor Langchain Tool
	.venv/bin/streamlit run src/chatbot_langchain_gemini_tool/app.py --server.port 8504 --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false

adk: ## Inicia o servidor ADK
	adk web src/agents
