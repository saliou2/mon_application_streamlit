import streamlit as st

# Titre de la page
st.title("Formulaire d'évaluation Google Forms")

# Intégrer le formulaire Google Forms
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe5JTa2F-MZlrG8z2gSBQ8ruCM8n1UicxmxD5ZZW-Y_c2qz2A/viewform?embedded=true"
st.markdown(
    f"""
    <iframe src="{google_form_url}" width="100%" height="600px"></iframe>
    """,
    unsafe_allow_html=True
)