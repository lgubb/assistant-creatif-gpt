import os
from dotenv import load_dotenv
import requests
import csv 
from datetime import datetime

load_dotenv()  # Charge les variables d’environnement depuis .env

api_key = os.getenv("OPENAI_API_KEY")

theme = input("🎤 Entre un thème ou un style de chanson : ")

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "Tu es un assistant créatif musical qui propose des idées originales."},
        {"role": "user", "content": f"Propose-moi un titre original de chanson dans ce style : {theme}"}
    ],
    "temperature": 1
}
response = requests.post(url, headers=headers, json=payload)

for i in range(3):  # génère 3 idées
    print(f"\n🎬 Idée #{i+1}")
    
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        message = data["choices"][0]["message"]["content"]
        print("🎵", message.strip()) 
        with open ("idees_chansons.txt", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            f.write(f"[{timestamp}] {theme} | {message.strip()}\n")
        with open("idees_chansons.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, theme, message.strip()])


    else:
        print("❌ Erreur API :", response.status_code)
        print(response.text)

