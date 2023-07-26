import os
from dotenv import load_dotenv
import requests
import io
from PIL import Image
import streamlit as st
from utils import footer

# Load environment variables
load_dotenv()

# Set up page config
st.set_page_config(
    page_title="Text to Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Set up the title and a brief description
st.title("Text to Image Generator 🎨")
st.markdown("Generate cool images from text using our AI model. Just type in the text and let the AI do the rest!")

st.sidebar.markdown("""
## Welcome to Text to Image Generator!

Ever wondered what 'a cat wearing a hat' looks like? Or maybe 'a robot playing the guitar'? Well, wonder no more!

Here at Text to Image Generator, we turn your wildest text descriptions into images. It's like having a personal artist at your fingertips, ready to bring your words to life.

So go ahead, type in a description and let our AI do the rest. It's like doodling, but with words. Enjoy!
""")


# Get API token and URL from environment variables
API_TOKEN = os.getenv('API_TOKEN')
API_URL = os.getenv('STABLE_DIFFUSION_API_URL')
headers = {"Authorization": f"Bearer {API_TOKEN}"}


# Function to send a POST request to the inference server
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


# Function to get image from inference server
def get_from_inference_server(Text):
    image_bytes = query({"inputs": Text, })
    # You can access the image with PIL.Image for example
    image = Image.open(io.BytesIO(image_bytes))
    return image


myText = st.text_input(label="Enter your text", placeholder="Write the text here", value='Man with hat')

# Button to generate image
if st.button('Generate Image'):
    with st.spinner('Generating your image...'):
        image = get_from_inference_server(myText)
    st.success('Image generated successfully!')
    st.image(image, caption=myText, use_column_width=False)

# Display footer
st.markdown(footer, unsafe_allow_html=True)
