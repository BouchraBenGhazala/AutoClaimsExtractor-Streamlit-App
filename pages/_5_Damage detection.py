

import streamlit as st
from functions import get_damage_gemini, get_damages_gpt, get_damages_html
from streamlit.components.v1 import html
import io
import pandas as pd


st.set_page_config(layout="wide", page_title="Automobile Damage Detector", page_icon="🛠️")


st.markdown("<h2 style='color:#077d81;'>Automobile Damage Detector</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# Damage Detection 🛠️")
    st.markdown("This app uses AI to detect **car damages**, assess their **severity** and decide whether the damaged parts should be **replaced** or **repaired**.")


##########################

prix = pd.read_csv("demos/damage_detection/prix.csv")
prix_add = pd.read_csv("demos/damage_detection/prix_add.csv")
# target format: [{part_name: [severity1, severity2, severity3], ...}]
prix_add_dict = {}
for i in range(len(prix_add)):
    part = prix_add.iloc[i, 0]
    prix_add_dict[part] = [prix_add.iloc[i, 1], prix_add.iloc[i, 2], prix_add.iloc[i, 3]]
prix_dict = {}
for i in range(len(prix)):
    part = prix.iloc[i, 0]
    prix_dict[part] = [prix.iloc[i, 1], prix.iloc[i, 2], prix.iloc[i, 3]]


images = st.file_uploader("Upload images of a car to detect damages...", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

images_bytes = []


if images:
    with st.expander("Car images and damages detection"):
        nb_images = len(images)
        col1, col2 = st.columns(2)
        tabs = col1.tabs([f"Image {i+1}" for i in range(nb_images)])
        for i in range(nb_images):
            with tabs[i]:
                st.image(images[i], caption=f'Image {i+1}.', use_column_width=True)

        for image in images:
            images_bytes.append(image.read())

        # tab1, tab2, tab3 = st.tabs(["GPT-4", "Gemini Pro 1.0", "Gemini Pro 1.5"])
        tab1, tab2, tab3 = col2.tabs(["Model #1", "Model #2", "Model #3"])
        # tab2, tab3 = col2.tabs(["Model #1", "Model #2"])

        with tab1:
            with st.spinner():
                damaged_parts = get_damages_gpt(images_bytes)
            car_map_html = get_damages_html(damaged_parts, prix_dict, prix_add_dict)
            html(car_map_html, height=1000)

        for i in range(len(images_bytes)):
            images_bytes[i] = io.BytesIO(images_bytes[i])

        with tab2:
            with st.spinner():
                damaged_parts = get_damage_gemini(images_bytes, "gemini-1.5-flash")
            car_map_html = get_damages_html(damaged_parts, prix_dict, prix_add_dict)
            html(car_map_html, height=1000)

        with tab3:
            with st.spinner():
                damaged_parts = get_damage_gemini(images_bytes, "gemini-1.5-pro-latest")
            car_map_html = get_damages_html(damaged_parts, prix_dict, prix_add_dict)
            html(car_map_html, height=1000)

else:
    st.error("Please upload two images of the car's registration document.")