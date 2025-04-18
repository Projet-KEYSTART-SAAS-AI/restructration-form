import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("SOCIETE_API_KEY")

def fetch_infos_legales(siren):
    url = f"https://api.societe.com/api/v1/entreprise/{siren}/infoslegales"
    headers = {
        "X-Authorization": f"socapi {API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("infolegales", {})
    return {}

def fetch_latest_bilan(siren):
    url = f"https://api.societe.com/api/v1/entreprise/{siren}/bilans"
    headers = {
        "X-Authorization": f"socapi {API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        bilans = response.json().get("data", {}).get("bilans", [])
        return bilans[0] if bilans else {}
    return {}

def fetch_mandats(dirigeant_id):
    url = f"https://api.societe.com/api/v1/mandats/{dirigeant_id}"
    print(API_KEY)
    headers = {
        "X-Authorization": f"socapi {API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.text)  # ← Debug line
    if response.status_code == 200:
        return response.json().get("data", {}).get("mandats", [])
    return []
