import os
from dotenv import load_dotenv
import operator
from typing import Annotated, Sequence, TypedDict
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from agents import tools, agents
from langchain_core.messages import AIMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import BaseMessage
import functools
from langchain_core.tools import tool

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from enum import Enum
from langgraph.graph import StateGraph, END

members = ["Calculator", "TextEditor", "Communicate"]

load_dotenv()


@tool(description="Get the current weather in a given location")
def get_weather(location: str) -> str:
    return "It's sunny."

def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role


st.set_page_config(
    page_title="Gemini Demo - Streamlit App", page_icon="💬", layout="centered"
)
st.title("Gemini Demo - Streamlit App")

st.sidebar.header("Settings")

model_options = ["gemini-2.5-flash-preview-05-20", "gemini-2.5-pro-preview-06-05"]
MODEL = st.sidebar.selectbox("Choose a Model", model_options, index=0)

MAX_HISTORY = st.sidebar.number_input(
    "Max History", min_value=1, max_value=10, value=2, step=1
)
CONTEXT_SIZE = st.sidebar.number_input(
    "Context Size", min_value=1024, max_value=16384, value=8192, step=1024
)


def clear_memory():
    st.session_state.chat_history = []
    st.session_state.memory = ConversationBufferMemory(return_messages=True)


if (
    "prev_context_size" not in st.session_state
    or st.session_state.prev_context_size != CONTEXT_SIZE
):
    clear_memory()
    st.session_state.prev_context_size = CONTEXT_SIZE

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

llm = ChatGoogleGenerativeAI(model=MODEL, streaming=True)
lm_with_tools = llm.bind_tools([get_weather])
system_prompt = """ You are a mathematical assistant.
        Use your tools to answer questions. If you do not have a tool to
        answer the question, say so. """
math_agent = agents.create_tool_agent(
    llm=lm_with_tools, tools=tools.math_toolkit, system_prompt=system_prompt
)
system_prompt = """ You are a text editor assistant.
        Use your tools to complete requests. If you do not have a tool to
       complete the request, say so. """
text_agent = agents.create_tool_agent(
    llm=lm_with_tools, tools=tools.text_toolkit, system_prompt=system_prompt
)

system_prompt_template = PromptTemplate(
    template=""" You are a talkative and helpful assistant that summarises agent history 
                      in response to the original user query below. 
                      SUMMARISE ALL THE OUTPUTS AND TOOLS USED in agent_history.
                      The agent history is as follows: 
                        \n{agent_history}\n""",
    input_variables=["agent_history"],
)
system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt_template)
prompt = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        MessagesPlaceholder(variable_name="messages"),
    ]
)
comms_agent = prompt | lm_with_tools


member_options = {member: member for member in members}

MemberEnum = Enum("MemberEnum", member_options)
from pydantic import BaseModel


class SupervisorOutput(BaseModel):
    next: MemberEnum = MemberEnum.Communicate


system_prompt = """You are a supervisor tasked with managing a conversation between the
    crew of workers:  {members}. Given the following user request, 
    and crew responses respond with the worker to act next.
    Each worker will perform a task and respond with their results and status. 
    When finished with the task, route to communicate to deliver the result to 
    user. Given the conversation and crew history below, who should act next?
    Select one of: {options} 
    \n{format_instructions}\n"""

supervisor_parser = JsonOutputParser(pydantic_object=SupervisorOutput)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_history"),
    ]
).partial(
    options=str(members),
    members=", ".join(members),
    format_instructions=supervisor_parser.get_format_instructions(),
)
supervisor_chain = prompt | lm_with_tools | supervisor_parser


def crew_nodes(state, crew_member, name):
    input = {
        "messages": [state["messages"][-1]],
        "agent_history": state["agent_history"],
    }
    result = crew_member.invoke(input)
    # add response to the agent history.
    return {
        "agent_history": [
            AIMessage(
                content=result["output"],
                additional_kwargs={"intermediate_steps": result["intermediate_steps"]},
                name=name,
            )
        ]
    }


def comms_node(state):

    input = {
        "messages": [state["messages"][-1]],
        "agent_history": state["agent_history"],
    }
    result = comms_agent.invoke(input)

    return {"messages": [result]}


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    agent_history: Annotated[Sequence[BaseMessage], operator.add]


workflow = StateGraph(AgentState)

math_node = functools.partial(crew_nodes, crew_member=math_agent, name="Calculator")
text_node = functools.partial(crew_nodes, crew_member=text_agent, name="TextEditor")
workflow.add_node("TextEditor", text_node)
workflow.add_node("Calculator", math_node)
workflow.add_node("Communicate", comms_node)
workflow.add_node("Supervisor", supervisor_chain)

workflow.set_entry_point("Supervisor")

workflow.add_edge("TextEditor", "Supervisor")
workflow.add_edge("Calculator", "Supervisor")

workflow.add_edge("Communicate", END)
workflow.add_conditional_edges("Supervisor", lambda x: x["next"], member_options)
graph = workflow.compile()

prompt_template = PromptTemplate(
    input_variables=["history", "human_input"],
    template="{history}\nUser: {human_input}\nAssistant:",
)


for msg in st.session_state.chat_history:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])


def trim_memory():
    while len(st.session_state.chat_history) > MAX_HISTORY * 2:
        st.session_state.chat_history.pop(0)
        if st.session_state.chat_history:
            st.session_state.chat_history.pop(0)


if prompt := st.chat_input("Say something"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.chat_history.append({"role": "user", "content": prompt})

    trim_memory()

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        for chunk in graph.stream({"human_input": prompt}):
            if isinstance(chunk, dict) and "text" in chunk:
                text_chunk = chunk["text"]
                full_response += text_chunk
                response_container.markdown(full_response)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": full_response}
    )

    trim_memory()
