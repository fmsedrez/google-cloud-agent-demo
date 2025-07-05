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
	.venv/bin/streamlit run src/chatbot_streamlit/app.py --server.port 8501

gemini: ## Inicia o servidor Gemini
	.venv/bin/streamlit run src/chatbot_gemini/app.py --server.port 8502

langchain: ## Inicia o servidor Langchain
	.venv/bin/streamlit run src/chatbot_langchain_gemini/app.py --server.port 8503

langchain_tool: ## Inicia o servidor Langchain Tool
	.venv/bin/streamlit run src/chatbot_langchain_gemini_tool/app.py --server.port 8504

adk:
	adk web src/agents
