# app.py
# Interface Streamlit pour le chatbot IA avec memoire de conversation.
# Compatible Python 3.6+
#
# Pour lancer : streamlit run app.py

import sys
import os
import streamlit as st

# Ajouter le dossier src au path Python
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from chatbot import chat, verifier_cle_api
from memory import MemoireConversation

# ------------------------------------------------------------------
# Configuration de la page
# ------------------------------------------------------------------

st.set_page_config(
    page_title="Chatbot NSI",
    page_icon="robot",
    layout="centered"
)

# ------------------------------------------------------------------
# Titre et description
# ------------------------------------------------------------------

st.title("Chatbot NSI - Assistant IA")
st.caption("Pose tes questions sur le programme de Terminale NSI")

# ------------------------------------------------------------------
# Verifier la cle API
# ------------------------------------------------------------------

if not os.getenv("MISTRAL_API_KEY"):
    st.error(
        "Cle API Mistral manquante ! "
        "Cree un fichier .env avec MISTRAL_API_KEY=ta-cle-api-ici"
    )
    st.stop()

# ------------------------------------------------------------------
# Initialiser la memoire dans la session Streamlit
# ------------------------------------------------------------------

if "memoire" not in st.session_state:
    st.session_state.memoire = MemoireConversation(taille_max=10)

if "messages_affiches" not in st.session_state:
    st.session_state.messages_affiches = []

# ------------------------------------------------------------------
# Barre laterale avec statistiques et options
# ------------------------------------------------------------------

with st.sidebar:
    st.header("Options")

    # Bouton reinitialiser
    if st.button("Nouvelle conversation", use_container_width=True):
        st.session_state.memoire.reinitialiser()
        st.session_state.messages_affiches = []
        st.rerun()

    st.divider()

    # Statistiques
    st.subheader("Statistiques")
    stats = st.session_state.memoire.resume_stats()
    st.metric("Messages en memoire",  stats["messages_en_memoire"])
    st.metric("Questions posees",     stats["messages_utilisateur"])
    st.metric("Reponses recues",      stats["messages_assistant"])

    st.divider()

    # Exemples de questions
    st.subheader("Exemples de questions")
    exemples = [
        "Qu est-ce qu un algorithme ?",
        "Explique les arbres binaires",
        "C est quoi la complexite O(n) ?",
        "Difference entre liste et tuple ?",
        "Comment fonctionne le tri rapide ?",
        "Qu est-ce qu une base de donnees SQL ?",
    ]

    for exemple in exemples:
        if st.button(exemple, use_container_width=True):
            # Simuler un message utilisateur
            st.session_state.messages_affiches.append(
                {"role": "user", "content": exemple}
            )
            reponse = chat(exemple, st.session_state.memoire)
            st.session_state.messages_affiches.append(
                {"role": "assistant", "content": reponse}
            )
            st.rerun()

# ------------------------------------------------------------------
# Afficher l historique des messages
# ------------------------------------------------------------------

if not st.session_state.messages_affiches:
    st.info("Bonjour ! Je suis ton assistant NSI. Pose-moi une question sur le programme de Terminale.")

for msg in st.session_state.messages_affiches:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------------------------------------------------------------------
# Zone de saisie du message
# ------------------------------------------------------------------

if prompt := st.chat_input("Ta question..."):

    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages_affiches.append(
        {"role": "user", "content": prompt}
    )

    # Generer et afficher la reponse
    with st.chat_message("assistant"):
        with st.spinner("Reflexion en cours..."):
            reponse = chat(prompt, st.session_state.memoire)
        st.write(reponse)

    st.session_state.messages_affiches.append(
        {"role": "assistant", "content": reponse}
    )
