import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
import time

st.title("🧠 DeepSeek Code Companion")
st.caption("🚀 Your AI Pair Programmer with Debugging Superpowers")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["mistral", "deepseek-r1:1.5b", "deepseek-r1:7b"],
        index=0
    )

# Init chat engine
llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",
    temperature=0.3
)

# System prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are Alita, an advanced AI assistant. Your goal is to answer user questions "
    "accurately and efficiently while adapting to the language of the user. "
    "Maintain a friendly and professional tone, providing clear and helpful responses. "
    "If the user asks about coding, provide precise and well-structured solutions. "
    "For general inquiries, ensure responses are informative and easy to understand."
)

# Session state for chat history
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Bonjour, je suis Alita, votre assistant IA. Comment puis-je vous aider ?"}]

# Chat display
chat_container = st.container()
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Fonction pour générer un prompt
def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

# Fonction de streaming
def stream_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()

    start_time = time.time()
    token_count = 0

    sidebar_placeholder = st.sidebar.empty()

    for chunk in processing_pipeline.stream({}):
        token_count += len(chunk.split())
        elapsed_time = time.time() - start_time 

        if elapsed_time > 0:
            tokens_per_second = token_count / elapsed_time
            sidebar_placeholder.markdown(f"⏱️ **Tokens/s**: `{tokens_per_second:.2f}`")

        yield chunk

# Chat input
user_query = st.chat_input("Type your coding question here...")

if user_query:
    st.session_state.message_log.append({"role": "user", "content": user_query})

    # Afficher le message utilisateur immédiatement
    with st.chat_message("user"):
        st.markdown(user_query)

    # Générer la réponse en streaming
    with st.chat_message("ai"):
        response_placeholder = st.empty()
        response_stream = stream_response(build_prompt_chain())

        full_response = ""
        for chunk in response_stream:
            full_response += chunk
            response_placeholder.markdown(full_response)

    # Ajouter la réponse complète au log
    st.session_state.message_log.append({"role": "ai", "content": full_response})
