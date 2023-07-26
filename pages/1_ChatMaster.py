import streamlit as st
from hugchat import hugchat
from dotenv import load_dotenv
import os
import time
from utils import footer
import random

load_dotenv()

TOKEN = os.getenv('HF_TOKEN')
HFCHAT = os.getenv('HFCHAT')

@st.cache_data()
def get_hugchat_model():
    return hugchat.ChatBot(cookies={'token': TOKEN, 'hfchat': HFCHAT})

def generate_response_hugchat(prompt):
    response = chatbot.chat(prompt)
    return response

def display_messages():
    for i in range(len(st.session_state['generated'])):
        with st.chat_message("user"):
            st.write(st.session_state['past'][i])
        with st.chat_message(name="ChatMaster", avatar='assistant'):
            st.write(st.session_state['generated'][i])

def handle_user_input():
    with st.form(key='my_form'):
        user_input = st.text_input("You: ", "", key="input")
        submit_button = st.form_submit_button(label='Send')

    if user_input and not user_input.isspace():
        if submit_button or user_input != st.session_state.get("last_input", ""):
            response = generate_response_hugchat(user_input)
            response = simulate_typing(response)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)
            st.session_state["last_input"] = user_input
            st.experimental_rerun()

def simulate_typing(response):
    full_response = ""
    message_placeholder = st.empty()
    for chunk in response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    return full_response

st.title('ChatMaster')
st.sidebar.title('Welcome to ChatMaster')

st.sidebar.markdown("""
Oh, look who's here! You've stumbled upon ChatMaster, the chatbot that's as thrilled to meet you as a cat is to take a bath. But don't worry, we're all about making your day a little less ordinary and a lot more... interesting. 

This documentation? It's your guide to navigating conversations with the most charmingly indifferent AI you'll ever meet. So, brace yourself, it's about to get excitingly mundane with ChatMaster!
""")

if 'generated' not in st.session_state:
    intro_text = random.choice(
        [
            "Hi, human! Is there anything I can help you with?",
            "Do you really need help?",
            "I'm at your service!",
            "Today I'm feeling like a chatbot, so I'm here to help you!",
            "Pretty cool, huh? I'm a chatbot!",
            "I'm a chatbot, but I'm not a bot. I'm a human.",
            "Badly need a chatbot? I'm here to help you!",
            "Don't you like Chatgpt? I'm better than that!",
            "Chatgpt is a good chatbot, but I'm better than that!",
            "People said Chatgpt is good. But they haven't met me yet!",
        ]
    )
    st.session_state['generated'] = [intro_text]

if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi ChatMaster!']

chatbot = get_hugchat_model()

display_messages()

handle_user_input()

if st.button('Start Over'):
    st.session_state.clear()
    st.experimental_rerun()

st.markdown(footer, unsafe_allow_html=True)
