venv:
	uv venv .venv

sync:
	uv sync

api:
	.venv/bin/uvicorn src.api.main:app --host 127.0.0.1 --port 8500 --reload

streamlit:
	.venv/bin/streamlit run src/chatbot_streamlit/app.py --server.port 8501

gemini:
	.venv/bin/streamlit run src/chatbot_gemini/app.py --server.port 8502

langchain:
	.venv/bin/streamlit run src/chatbot_langchain_gemini/app.py --server.port 8503

langchain_tool:
	.venv/bin/streamlit run src/chatbot_langchain_gemini_tool/app.py --server.port 8504

adk:
	adk web src/agents

# all: venv sync api streamlit gemini adk