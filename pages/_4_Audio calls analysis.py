import streamlit as st
import numpy as np
from PIL import Image
import io
from functions import *
import os

st.set_page_config(layout="wide", page_title="Audio calls Analysis", page_icon="🔊")

st.markdown("<h2 style='color:#077d81;'>Audio calls Analysis</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# Audio calls 🔊")
    st.markdown("This app uses AI to analyse **customer's calls**.")

audio = st.file_uploader("Upload the audio of the call in mp3 or wav type", type=["mp3", "wav"])

if audio:
    st.audio(audio, format='audio/wav')
    audio_bytes = audio.read()
    # test if the folder exists
    if not os.path.exists("temp_audio"):
        os.makedirs("temp_audio")
    audio_path = os.path.join("temp_audio", audio.name)
    audio_type = audio.type
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    with st.spinner():
        with st.expander("Phone call extracted information in Moroccan Darija"):
            dialog_darija, audio = get_transcription_gemini(audio_path, audio_type) 
            res_html_1 = dialog_darija.replace("\n", "<br>") 
            st.markdown("<p style='text-align: right;'>" + res_html_1 + "</p>", unsafe_allow_html=True) 

        with st.expander("Phone call extracted information in English"):
            dialog_french = get_translation_gemini(dialog_darija) 
            res_html_2 = dialog_french.replace("\n", "<br>") 
            st.markdown("<p style='text-align: left;'>" + res_html_2 + "</p>", unsafe_allow_html=True) 
        
        with st.expander("Summary"):
            summary = get_summary_gemini(dialog_darija) 
            st.write(summary)        
