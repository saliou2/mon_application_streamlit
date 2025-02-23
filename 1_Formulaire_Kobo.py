import streamlit as st

# Titre de la page
st.title("Formulaire d'évaluation Kobo")

# Intégrer le formulaire Kobo
kobo_form_url = "https://ee.kobotoolbox.org/i/dF8AYTGG"
st.markdown(
    f"""
    <iframe src="{kobo_form_url}" width="100%" height="600px"></iframe>
    """,
    unsafe_allow_html=True
)