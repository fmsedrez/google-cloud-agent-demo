venv:
	uv venv .venv

sync:
	uv sync

api:
	.venv/bin/uvicorn src.gemini-demo.main:app --host 0.0.0.0 --port 8080 --reload

streamlit:
	.venv/bin/streamlit run src/function_calling/app.py
all: venv sync api 