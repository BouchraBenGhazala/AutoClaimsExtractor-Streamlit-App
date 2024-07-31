

import streamlit as st

st.set_page_config(layout="wide", page_title="Automobile Damage Detector", page_icon="🛠️")


st.markdown("<h2 style='color:#077d81;'>Automobile Damage Detector</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# Damage Detection 🛠️")
    st.markdown("This app uses AI to detect **car damages**, assess their **severity** and decide whether the damaged parts should be **replaced** or **repaired**.")


