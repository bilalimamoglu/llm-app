import os
from dotenv import load_dotenv
import requests
import io
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from utils import footer
import json
import base64

# Load environment variables
load_dotenv()

# Set up page config
st.set_page_config(
    page_title="Image Captioning",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Set up the title and a brief description
st.title("Image Captioning")
st.markdown("Capture the essence of your image with a caption!")

st.sidebar.markdown("""
## 🎉 Welcome to Image Captioning! 🎉

You know how they say a picture is worth a thousand words? Well, we're about to prove them wrong. 

Here, we believe that a picture is worth exactly one caption. No more, no less. 

So go ahead, upload an image or draw one if you're feeling artistic. Our state-of-the-art AI will then generate a caption that captures the essence of your image in a single sentence. 

It's like magic, but without the rabbits and hats. Enjoy!
""")


# Get API token and URL from environment variables
API_TOKEN = os.getenv('API_TOKEN')
API_URL = os.getenv('IMAGE_CAPTIONING_API_URL')
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Function to send a POST request to the inference server
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# Function to get caption from inference server
def get_caption_from_inference_server(image):
    image = image.convert("RGB")  # Convert image to RGB
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    response = query({"inputs": img_str.decode('utf-8'), })
    response_json = json.loads(response.decode('utf-8'))  # Decode byte string and parse JSON
    caption = response_json[0]['generated_text']  # Extract generated text
    return caption

# Select image source
image_source = st.radio("Select image source", ["Upload image", "Draw image"])

if image_source == "Upload image":
    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=400)
else:
    # Draw image
    st.markdown("Draw an image:")
    stroke_width = st.slider("Stroke width:", 1, 25, 10)
    stroke_color = st.color_picker("Stroke color:", '#e00')
    background_color = st.color_picker("Background color:", '#fff')

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=background_color,
        height=500,  # Adjust the height of the canvas
        width=1000,  # Adjust the width of the canvas
        drawing_mode="freedraw",
        key="canvas",
    )

    # Convert the drawn image to PIL Image
    if canvas_result.image_data is not None:
        drawn_image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        st.image(drawn_image, caption="Drawn Image", use_column_width=False)

# Button to generate caption
if st.button('Generate Caption'):
    with st.spinner('Generating your caption...'):
        if image_source == "Upload image" and uploaded_file is not None:
            caption = get_caption_from_inference_server(image)
        elif image_source == "Draw image" and canvas_result.image_data is not None:
            caption = get_caption_from_inference_server(drawn_image)
        else:
            st.warning("Please upload or draw an image first.")
            st.stop()
    st.success('Caption generated successfully!')
    st.markdown(f"<h2 style='text-align: center; color: white;'>{caption}</h2>", unsafe_allow_html=True)

# Display footer
st.markdown(footer,unsafe_allow_html=True)
