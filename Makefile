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

adk: ## Start ADK Server
	uv run adk web src/agents --port 8505

adk_api: ## Start ADK API Server
	uv run adk api src/agents --port 8506