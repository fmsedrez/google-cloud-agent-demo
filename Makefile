venv:
	uv venv .venv

sync:
	uv sync

api:
	.venv/bin/uvicorn src.gemini-demo.main:app --host 0.0.0.0 --port 8080 --reload

all: venv sync api 