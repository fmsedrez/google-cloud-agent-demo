import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()

def fetch_gemini_response(user_query):
    # Use the session's model to generate a response
    response = st.session_state.chat_session.model.generate_content(user_query)
    print(f"Gemini's Response: {response}")
    return response.parts[0].text

def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role


st.set_page_config(
    page_title="Gemini Demo - Streamlit App", page_icon="💬", layout="centered"
)

st.title("Gemini Demo - Streamlit App")

gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key:
    st.session_state["API_KEY"] = gemini_api_key
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
    os.environ["API_KEY"] = gemini_api_key
    

api_key = st.sidebar.text_input(
    label="Gemini API Key",
    type="password",
    value=st.session_state["API_KEY"] if "API_KEY" in st.session_state else "",
    placeholder="...",
)
st.sidebar.header("Settings")

st.sidebar.markdown(
    "#### <a href='http://ai.google.dev/' style='color:light-blue;'>Powered by Gemini</a>",
    unsafe_allow_html=True,
)

if api_key:
    st.session_state["API_KEY"] = api_key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-pro-preview-06-05")
    os.environ["API_KEY"] = api_key
else:
    st.error("Please add your Gemini API key to continue.")
    st.stop()



if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


st.title("🤖 Chat with Gemini-Pro")

for msg in st.session_state.chat_session.history:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask Gemini-Pro...")
if user_input:
    st.chat_message("user").markdown(user_input)
    gemini_response = fetch_gemini_response(user_input)
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    st.session_state.chat_session.history.append(
        {"role": "user", "content": user_input}
    )
    st.session_state.chat_session.history.append(
        {"role": "model", "content": gemini_response}
    )
