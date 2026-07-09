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

copy_adc: ## Copy generated ADC credentials from temporary/sandbox path to standard user config path
	@mkdir -p $(HOME)/.config/gcloud
	@if [ -n "$$GOOGLE_APPLICATION_CREDENTIALS" ] && [ -f "$$GOOGLE_APPLICATION_CREDENTIALS" ]; then \
		cp "$$GOOGLE_APPLICATION_CREDENTIALS" "$(HOME)/.config/gcloud/application_default_credentials.json"; \
		echo "✓ Credentials copied from $$GOOGLE_APPLICATION_CREDENTIALS to ~/.config/gcloud/application_default_credentials.json"; \
	else \
		TEMP_ADC=$$(find /tmp -name "application_default_credentials.json" -type f 2>/dev/null | head -n 1); \
		if [ -n "$$TEMP_ADC" ] && [ -f "$$TEMP_ADC" ]; then \
			cp "$$TEMP_ADC" "$(HOME)/.config/gcloud/application_default_credentials.json"; \
			echo "✓ Credentials copied from $$TEMP_ADC to ~/.config/gcloud/application_default_credentials.json"; \
		else \
			echo "Error: No credentials file found in \$$GOOGLE_APPLICATION_CREDENTIALS or /tmp. Please run 'make gcloud_login' first."; \
			exit 1; \
		fi; \
	fi

gcloud_ai_enable: ## Enable Google Cloud AI services
	gcloud services enable aiplatform.googleapis.com

adk: ## Start ADK Server
	uv run adk web src/agents --port 8505

adk_api: ## Start ADK API Server
	uv run adk api src/agents --port 8506

toolbox: ## Start toolbox for prebuild bigquery
	./toolbox --prebuilt bigquery --stdio --enable-api