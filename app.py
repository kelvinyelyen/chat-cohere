import streamlit as st
import cohere
import os
from dotenv import load_dotenv


load_dotenv()

# Initialize the Cohere client with your API key
api_key = os.getenv('COHERE_API_KEY')
co = cohere.Client(api_key)

bot_name = "ElsieBot"

st.set_page_config(page_title=bot_name, page_icon="🤖", layout="centered")

def generate_response(prompt):
    try:
        if "your name" in prompt.lower():
            response_text = f"My name is {bot_name}."
        else:
            response = co.generate(
                model='command-xlarge-nightly',
                prompt=prompt,
                max_tokens=500,
                temperature=0.7,
                stop_sequences=[]
            )
            response_text = response.generations[0].text.strip()
        return response_text
    except Exception as e:
        return f"Error: {str(e)}"

st.title(bot_name)

# Initialize chat history and intro message flag
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'intro_displayed' not in st.session_state:
    st.session_state.intro_displayed = False

if not st.session_state.intro_displayed:
    intro_message = f"Hello! I'm {bot_name} 😊. What can I help you with today?"
    st.session_state.messages.append({"role": "assistant", "content": intro_message})
    st.session_state.intro_displayed = True

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Say something, I'm giving up on you"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response using Cohere API
    with st.spinner("Generating response..."):
        response = generate_response(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


# Lack of Continuity