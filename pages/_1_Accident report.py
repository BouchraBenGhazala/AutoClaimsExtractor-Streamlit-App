import streamlit as st
import numpy as np
from PIL import Image
import io
from functions import *

st.set_page_config(layout="wide", page_title="Accident Report", page_icon="📋")


with st.sidebar:
    st.markdown("# Accident Report 📋")
    st.markdown("This app uses AI to **automate the process of accident reporting** by **extracting detailed information from accident report images** to streamline claims processing.")

#prompts
#prompts
prompt_infos = load_prompt('prompts/prompt_infos.txt')
prompt_vA = load_prompt('prompts/prompt_vehicule.txt')
prompt_vueA = load_prompt('prompts/prompt_vue.txt')
prompt_vB = load_prompt('prompts/prompt_vehicule.txt')
prompt_vueB = load_prompt('prompts/prompt_vue.txt')
prompt_casA = load_prompt('prompts/prompt_cases.txt')
prompt_casB = load_prompt('prompts/prompt_cases.txt')

# Streamlit UI
st.markdown("<h2 style='color:#077d81;'>Automobile Accident Report Information Extractor</h2>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload an image of the automobile accident report.", accept_multiple_files=False, type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    #process_constat():
    image = np.array(image)
    cropped_image = returnPartOfImg(image, 0, 0.17, 0, 0.6)  # infos constat
    base64_image = encode_image(cropped_image)
    # infos_constat = get_image_info_openai(base64_image, prompt_infos)
    infos_constat=get_image_info_gemini(cropped_image,prompt_infos)

    VoitureA = returnPartOfImg(image, 0.17, 0.6, 0, 0.32)
    base64_image_2 = encode_image(VoitureA)
    # infos_voiture_A = get_image_info_openai(base64_image_2, prompt_vA)
    infos_voiture_A = get_image_info_gemini(VoitureA,prompt_vA)

    VueA = returnPartOfImg(image, 0.62, 0.73, 0, 0.32)  # vue vehicule A
    base64_image_2_2 = encode_image(VueA)
    # infos_vue_A = get_image_info_openai(base64_image_2_2, prompt_vueA)
    infos_vue_A=get_image_info_gemini(VueA,prompt_vueA)

    VoitureB = returnPartOfImg(image, 0.17, 0.6, 0.7, 1)
    base64_image_3 = encode_image(VoitureB)
    # infos_voiture_B = get_image_info_openai(base64_image_3, prompt_vB)
    infos_voiture_B = get_image_info_gemini(VoitureB, prompt_vB)


    VueB = returnPartOfImg(image, 0.62, 0.72, 0.7, 1)  # vue vehicule B
    base64_image_3_2 = encode_image(VueB)
    # infos_vue_B = get_image_info_openai(base64_image_3_2, prompt_vueB)
    infos_vue_B = get_image_info_gemini(VueB, prompt_vueB)

    casA = returnPartOfImg(image, 0.17, 0.68, 0.3, 0.36)
    base64_image_4 = encode_image(casA)
    # infos_casA = get_image_info_openai(base64_image_4, prompt_casA)
    infos_casA = get_image_info_gemini(casA, prompt_casA)

    casB = returnPartOfImg(image, 0.17, 0.68, 0.64, 0.7)
    base64_image_5 = encode_image(casB)
    # infos_casB = get_image_info_openai(base64_image_5, prompt_casB)
    infos_casB = get_image_info_gemini(casB, prompt_casB)


    with st.expander("Accident report extracted information"):
        st.image(image)
        st.markdown("<h4 style='color:#077d81;'>Informations sur le constat</h2>", unsafe_allow_html=True)
        st.write(infos_constat)
        col1, col2 = st.columns(2)
        col1.markdown("<h4 style='color:#077d81;'>Informations sur le vehicule A</h2>", unsafe_allow_html=True)
        col1.write(infos_voiture_A)
        col1.markdown("<h4 style='color:#077d81;'>Informations sur la vue du vehicule A</h2>", unsafe_allow_html=True)
        col1.write(infos_vue_A)
        col1.markdown("<h4 style='color:#077d81;'>Informations sur les cases de A</h2>", unsafe_allow_html=True)
        col1.write(infos_casA)
        col2.markdown("<h4 style='color:#077d81;'>Informations sur le vehicule B</h2>", unsafe_allow_html=True)
        col2.write(infos_voiture_B)
        col2.markdown("<h4 style='color:#077d81;'>Informations sur la vue du vehicule B</h2>", unsafe_allow_html=True)
        col2.write(infos_vue_B)
        col2.markdown("<h4 style='color:#077d81;'>Informations sur les cases de B</h2>", unsafe_allow_html=True)
        col2.write(infos_casB)