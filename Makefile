venv:
	uv venv .venv

sync:
	uv sync

api:
	.venv/bin/uvicorn src.api.main:app --host 127.0.0.1 --port 8500 --reload

streamlit:
	.venv/bin/streamlit run src/function_calling/app.py --server.port 8501

all: venv sync api 