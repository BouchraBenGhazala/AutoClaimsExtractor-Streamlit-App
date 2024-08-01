import streamlit as st
from PIL import Image
# from secret_key import openapi_key_sygma
from functions import *
import numpy as np

st.set_page_config(layout="wide", page_title="Car's Registration Card", page_icon="💳")

css = """
<style>
.uploaded-image {
    width: 400px !important;
    height: 250px !important;
    object-fit: cover;  /* to maintain aspect ratio */
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# Car's Registration Card 💳 ")
    st.markdown("This app uses AI to **automate the process of car's registration card management** by **extracting detailed information from car's registration card images** to streamline verification and record-keeping.")

# Load the prompt
with open('prompts/prompt_carte_grise.txt', 'r') as file: 
    prompt_carte_grise = file.read()

# Streamlit UI
st.markdown("<h2 style='color:#077d81;'>Car's Registration Card Information Extractor</h2>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload two images (front and back sides) of the driving license.", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if uploaded_files:
    if len(uploaded_files) == 2:
        images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]
        base64_images = [encode_image2(image) for image in images[:2]]

        # Get the image info
        with st.expander("Carte grise extracted information"):
            if images:
                with st.spinner("Processing..."):
                    cols = st.columns(2)
                    for col, uploaded_file, base64_image,image in zip(cols, uploaded_files, base64_images,images):
                        image_base64 = encode_image2(Image.open(uploaded_file))
                        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                        col.markdown(f'<img src="data:image/png;base64,{image_base64}" class="uploaded-image">', unsafe_allow_html=True)
                        # col.write(get_image_info_openai(base64_image, prompt_carte_grise))
                        col.write(get_image_info_gemini(cv_image, prompt_carte_grise))
    else:
        st.warning("Please upload two images!")
