import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

BASE_URL = "https://anime-sama.pw"

def get_url():
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Erreur connexion :", e)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    link = soup.find("a", class_="btn-primary", string="Accéder à Anime-Sama")
    if not link:
        link = soup.find("a", class_="btn-primary")

    if not link or not link.get("href"):
        print("Lien introuvable")
        return None

    try:
        final_response = requests.get(link.get("href"), timeout=10, allow_redirects=True)
        final_response.raise_for_status()
        return final_response.url
    except requests.RequestException as e:
        print("Erreur redirection :", e)
        return None


def get_domaine():
    url = get_url()
    if not url:
        return None

    parsed = urlparse(url)
    hostname = parsed.hostname

    if not hostname:
        print("Hostname introuvable")
        return None

    return hostname.split(".")[-1]


