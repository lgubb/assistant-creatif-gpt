import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import csv

# Charger la clé API
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Interface utilisateur
st.title("🎵 Assistant IA créatif")
theme = st.text_input("Entre un thème ou un style de chanson")

if st.button("Générer une idée"):
    if not theme:
        st.warning("Merci de saisir un thème.")
    else:
        # Préparer la requête GPT
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Tu es un assistant créatif musical."},
                {"role": "user", "content": f"Propose-moi un titre original de chanson dans ce style : {theme}"}
            ],
            "temperature": 0.9
        }

        # Appel API
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            idea = data["choices"][0]["message"]["content"].strip()

            # Afficher le résultat
            st.success(f"🎵 Idée : {idea}")

            # Sauvegarde .csv
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("idees_chansons.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, theme, idea])
        else:
            st.error("Erreur API : " + str(response.status_code))
