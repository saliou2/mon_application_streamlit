import streamlit as st
from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd

# Injecter du CSS personnalisé pour changer le style de l'application
st.markdown(
    """
    <style>
    /* Changer la couleur de fond de l'application */
    .stApp {
        background-color: #8B4513;  /* Brown */
        color: white;  /* Couleur de la police */
    }

    /* Changer la couleur de fond des conteneurs */
    .st-bw, .st-cb, .st-ca, .st-cd, .st-ce, .st-cf, .st-cg, .st-ch, .st-ci, .st-cj, .st-ck, .st-cl, .st-cm, .st-cn, .st-co, .st-cp, .st-cq, .st-cr, .st-cs, .st-ct, .st-cu, .st-cv, .st-cw, .st-cx, .st-cy, .st-cz {
        background-color: #A0522D;  /* Un brun plus clair pour les conteneurs */
        color: white;  /* Couleur de la police */
    }

    /* Changer la couleur des titres */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }

    /* Changer la couleur du texte */
    p, div, span, a {
        color: white !important;
    }

    /* Changer la couleur des boutons */
    .stButton>button {
        background-color: #D2691E;  /* Couleur des boutons */
        color: white;  /* Couleur du texte des boutons */
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }

    /* Changer la couleur des inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #A0522D;
        color: white;
    }

    /* Changer la couleur des tableaux */
    .stDataFrame {
        background-color: #A0522D;
        color: white;
    }

    /* Style pour l'iframe */
    .responsive-iframe {
        width: 100%;
        height: 600px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre de l'application
st.title("Mon Application de Données")

st.write("""
Cette application vous permet de visualiser et de télécharger des données sur les animaux depuis CoinAfrique.
* **Bibliothèques Python utilisées :** pandas, streamlit, BeautifulSoup, requests
* **Source des données :** [CoinAfrique](https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons && https://sn.coinafrique.com/categorie/autres-animaux).
""")

# Fonction pour scraper les données
def scrape_page(url, source_name):
    res = get(url)
    soup = bs(res.text, 'html.parser')
    
    data = []
    containers = soup.find_all('div', class_='col s6 m4 l3')
    
    for container in containers:
        try:
            details = container.find('p', class_='ad__card-description').text.strip()
            prix = container.find('p', class_='ad__card-price').text.replace('CFA', '').strip()
            adresse = container.find('p', class_='ad__card-location').text.replace('location_on', '').strip()
            img_link = container.find('a', class_='card-image ad__card-image waves-block waves-light').img['src']
            
            dic = {
                'details': details,
                'prix': prix,
                'adresse': adresse,
                'img_link': img_link,
                'source': source_name  # Ajouter la source des données
            }
            data.append(dic)
        except AttributeError as e:
            st.warning(f"Erreur lors du scraping d'un élément : {e}")
            continue
    
    return pd.DataFrame(data)

# URLs des pages à scraper
url1 = "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons"
url2 = "https://sn.coinafrique.com/categorie/autres-animaux"

# Bouton pour scraper les données
if st.button("Scraper les données"):
    with st.spinner("Scraping en cours..."):  # Afficher un message de chargement
        try:
            # Scraper les données en spécifiant la source
            df1 = scrape_page(url1, source_name="Poules, Lapins et Pigeons")
            df2 = scrape_page(url2, source_name="Autres Animaux")
            
            # Concaténer les DataFrames
            df = pd.concat([df1, df2], ignore_index=True)
            
            # Sauvegarder les données dans un fichier CSV
            df.to_csv('data.csv', index=False)
            st.success("Données scrapées et sauvegardées avec succès!")
        except Exception as e:
            st.error(f"Une erreur s'est produite lors du scraping : {e}")

# Charger les données scrapées
try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    df = pd.DataFrame()  # DataFrame vide si aucun fichier n'existe

# Afficher les données avec un filtre par source
if not df.empty:
    st.write("Données scrapées :")
    
    # Ajouter un filtre par source
    sources = df['source'].unique()
    selected_sources = st.multiselect(
        "Filtrer par source :",
        options=sources,
        default=sources  # Par défaut, toutes les sources sont sélectionnées
    )
    
    # Filtrer les données en fonction des sources sélectionnées
    filtered_df = df[df['source'].isin(selected_sources)]
    
    # Afficher le tableau interactif
    st.dataframe(filtered_df)
else:
    st.warning("Aucune donnée n'a été scrapée pour le moment.")

# Bouton pour télécharger les données scrapées
if st.button("Télécharger les données scrapées"):
    try:
        with open('data.csv', 'rb') as f:
            st.download_button(
                label="Télécharger CSV",
                data=f,
                file_name='data.csv',
                mime='text/csv'
            )
    except FileNotFoundError:
        st.error("Aucune donnée n'a été scrapée pour le moment.")

# Section pour l'évaluation de l'application
st.title("Évaluation de l'application")

# Choix du formulaire d'évaluation
choix = st.radio(
    "Choisissez un formulaire d'évaluation :",
    options=["Formulaire d'évaluation Kobo", "Formulaire d'évaluation Google Forms"]
)

if choix == "Formulaire d'évaluation Kobo":
    st.header("Évaluation de l'application (Kobo)")
    # Remplacez l'URL par celle de votre formulaire Kobo
    kobo_form_url = "https://ee.kobotoolbox.org/i/dF8AYTGG"
    st.markdown(
        f"""
        <iframe class="responsive-iframe" src="{kobo_form_url}"></iframe>
        """, 
        unsafe_allow_html=True
    )
elif choix == "Formulaire d'évaluation Google Forms":
    st.header("Évaluation de l'application (Google Forms)")
    # Remplacez l'URL par celle de votre formulaire Google Forms
    google_form_url = "https://forms.google.com"
    st.markdown(
        f"""
        <iframe class="responsive-iframe" src="{google_form_url}"></iframe>
        """, 
        unsafe_allow_html=True
    )