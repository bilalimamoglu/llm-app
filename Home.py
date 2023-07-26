from utils import *
import streamlit as st

st.title("Welcome to Bilal's AI Playground")

st.header("About Me")
st.markdown("""
    Hi there! I'm Bilal Imamoglu, a passionate AI enthusiast and developer. I love exploring the capabilities of AI and creating innovative applications that leverage the power of machine learning. You can learn more about me [here](https://www.linkedin.com/in/bilalimamoglu/).
    """)

st.header("About the Apps")
st.markdown("""
    **ChatMaster**: ChatMaster is a state-of-the-art AI chatbot designed to engage you in dynamic and meaningful conversations. With a dash of sass and a pinch of sarcasm, ChatMaster makes every conversation lively, engaging, and downright entertaining. 

    **Text to Image Generator**: This app allows you to generate cool images from text using an AI model. Just type in the text and let the AI do the rest! It's a fun and creative way to visualize your thoughts and ideas.

    Feel free to explore these apps and have fun with AI!
    """)

st.header("Get Started")
st.markdown("""
    To get started, select the app you want to use from the menu in the sidebar. Enjoy exploring the capabilities of AI!
    """)

st.markdown(footer, unsafe_allow_html=True)
