import streamlit as st

def render_setup_section():
    st.subheader("Configuration")

    col1, col2 = st.columns(2)
    with col1:
        openai_key = st.text_input("OpenAI API Key", type="password")
    with col2:
        society_key = st.text_input("Society.com Key", type="password", value="80daf7f2f783d639885951ffa6705e7d")

    return openai_key, society_key
