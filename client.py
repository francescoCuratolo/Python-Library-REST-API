import requests
from typing import List

API_URL = "http://127.0.0.1:8000"  # indirizzo locale FastAPI

def mostra_catalogo() -> List[dict]:

    try:
        response = requests.get(f"{API_URL}/libri")
        response.raise_for_status()  # solleva errore se status != 200
        catalogo = response.json()   # assume che l'API ritorni JSON
        return catalogo
    except requests.exceptions.RequestException as e:
        print(f"Errore comunicazione con l'API: {e}")
        return []
    
def mostra_libri_noleggiati() -> List[dict]:

    try:
        response = requests.get(f"{API_URL}/libri-noleggiati")
        response.raise_for_status()
        catalogo = response.json()
        return catalogo
    except requests.exceptions.RequestException as e:
        print(f"Errore comunicazione con l'API: {e}")
        return []

def registra_utente(nome: str, cognome: str, email: str) -> dict | None:

    payload = {
        "nome": nome,
        "cognome": cognome,
        "email": email
    }

    try:
        response = requests.post(f"{API_URL}/utenti", json=payload)
        if response.status_code == 400:
            print("Errore: utente già registrato.")
            return None
        response.raise_for_status()

        utente_creato = response.json()
        return utente_creato
    except requests.exceptions.RequestException as e:
        print(f"Errore comunicazione con l'API: {e}")
        return None

def noleggia_libro(email: str, id_libro: int) -> dict | None:

    payload = {
        "email": email,
        "libro_id": id_libro
    }

    try:
        response = requests.post(f"{API_URL}/noleggia-libro", json=payload)
        if response.status_code == 400:
            errore = response.json().get("detail", 'Errore sconosciuto')
            print(f"Errore: {errore}")
            return None
        response.raise_for_status()
        
        noleggio = response.json()
        return noleggio
    except requests.exceptions.RequestException as e:
        print(f"Errore comunicazione con l'API: {e}")
        return None

def restituisci_libro(email: str, id_libro: int) -> dict | None:

    payload = {
        "email": email,
        "libro_id": id_libro
    }

    try:
        response = requests.post(f"{API_URL}/restituisci-libro", json=payload)
        if response.status_code == 400:
            errore = response.json().get("detail", 'Errore sconosciuto')
            print(f"Errore: {errore}")
            return None
        response.raise_for_status()
        
        restituzione = response.json()
        return restituzione
    except requests.exceptions.RequestException as e:
        print(f"Errore comunicazione con l'API: {e}")
        return None