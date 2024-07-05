import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client with your API key
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Initialize conversation history as an empty list
if 'conversation_history' not in st.session_state: #For memory storage
    st.session_state.conversation_history = []

# Streamlit UI setup
st.write("# ChatGPT Bot")

# System prompt input
system_prompt = st.text_input("System Prompt", "You are a helpful assistant.")

# Model parameters sidebar
st.sidebar.markdown("# Model Parameters")
model_options = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it", "gemma2-9b-it"]
model_name = st.sidebar.selectbox("Select Model", model_options, index=0)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
max_tokens = st.sidebar.number_input("Max Tokens", min_value=64, max_value=2048, value=1024, step=64)
top_p = st.sidebar.slider("Top P", 0.1, 1.0, 1.0, 0.1)

# Button to trigger chat completion
if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        
        # Append current user prompt to conversation history
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Include conversation history in messages
        messages_with_history = messages + st.session_state.conversation_history # Add memory of previous conversation
        
        for response in client.chat.completions.create(
            model=model_name,
            messages=messages_with_history,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        ):
            if response.choices and response.choices[0].delta.content:
                full_response += response.choices[0].delta.content
                message_placeholder.markdown(full_response)
                
        message_placeholder.markdown(full_response)