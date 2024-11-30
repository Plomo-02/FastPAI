import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from .vec_db import ChromaDB

logger = logging.getLogger(__name__)

# Carica le variabili d'ambiente
load_dotenv()

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("chain_app.log"), logging.StreamHandler()],
)

# Configura il prompt per la formattazione della query


# Configura il vectorstore Chroma
def initialize_chroma(docs):
    db = ChromaDB(docs)
    return db


# Classe per gestire le interazioni con OpenAI e Chroma
class LlamaChromaHandler:
    def __init__(self, vectorstore):
        self.client = OpenAI(
            base_url="https://api.aimlapi.com/v1",  # URL dell'API
            api_key=os.getenv("API_KEY"),  # Chiave API
        )
        self.vectorstore = vectorstore

    def send_response(self, query: str, result: str) -> str:
        """Invia una richiesta al modello OpenAI e restituisce solo un JSON strutturato."""
        user_content = f"""Richiesta originale dell'utente: {query}
                            Risposta dal database vettoriale: {result}"""

        response = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",  # Modello utilizzato
            messages=[
                {
                    "role": "system",
                    "content": """Sei un assistente esperto di comunicazione chiara e accessibile per i cittadini. Ricevi una risposta da un database vettoriale contenente dati come città, date, orari disponibili e altre informazioni, insieme alla richiesta originale dell'utente. Il tuo compito è:
        1. Valutare se la risposta dal database vettoriale è sufficientemente correlata con la richiesta dell'utente. 
            - Se lo è, formulare una risposta semplice, chiara, concisa e facilmente comprensibile da qualunque cittadino, mantenendo solo le informazioni più rilevanti.
            - Se non lo è, generare autonomamente una risposta pertinente basandoti solo sulla richiesta dell'utente.
        2. Identificare se la richiesta dell'utente riguarda solo un'informazione o un'intenzione di prenotare un servizio.

        Devi restituire solo un JSON nel seguente formato e nient'altro:
        {
        "info": "La tua risposta chiara e concisa all'utente.",
        "is_info": true/false  // true se la richiesta riguarda solo informazioni, false se riguarda una prenotazione.
        }""",
                },
                {"role": "user", "content": user_content},
            ],
            max_tokens=256,
        )
        return response.choices[0].message.content.strip()

    def send_request(self, prompt: str) -> str:
        """Invia una richiesta al modello OpenAI."""
        response = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",  # Modello utilizzato
            messages=[
                {
                    "role": "system",
                    "content": """Sei un assistente esperto di ricerca e Ricevi una richiesta utente e riformulala per essere adatta a una ricerca semantica per similarità in un database vettoriale (ChromaDB).
    Assicurati che la richiesta sia chiara, concisa e rappresenti al meglio l'intento originale dell'utente. rispondi esclusivamente con la richiesta senza scrivere.""",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=128,
        )
        return response.choices[0].message.content.strip()

    def process_query(self, input_text: str, city: str):
        try:
            # Fase 1: Formatta la query con il modello AI
            logger.info("Formattazione della query tramite OpenAI...")

            formatted_query = self.send_request(input_text)

            # Fase 2: Ricerca nel vectorstore
            logger.info("Esecuzione della ricerca su Chroma...")
            results = self.vectorstore.get_from_chroma(formatted_query, city)

            # Restituisci i risultati
            return {"results": results}
        except Exception as e:
            logger.error("Errore durante l'elaborazione della query: %s", e)
            raise

    def format_response(self, query, result):
        metadata_formatted = " ".join(f"{key} {value}" for key, value in result.items())
        llm_response = self.send_response(query, metadata_formatted)
        """
        implement the response formatting here, to obtain date e orari disponibili, e info 
        """
        date_orari = result.get("date_orari")
        need_to_do = result.get("need_to_do")
        result_json = {
            "llm_response": llm_response,
            "response": date_orari,
            "info": need_to_do,
        }
        return result_json


def clean_dict(data):
    if isinstance(data, dict):
        return {k: clean_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_dict(item) for item in data]
    elif isinstance(data, str):
        # Rimuove \n e spazi extra
        cleaned_str = data.replace("\n", "").strip()
        # Prova a caricare come JSON se possibile
        try:
            return json.loads(cleaned_str)
        except (json.JSONDecodeError, TypeError):
            return cleaned_str
    else:
        return data


# Funzione principale per eseguire la gestione
def run_handler(query: str, vectorstore: ChromaDB, city: str = None):
    try:
        logger.info("Avvio del handler...")

        # Crea la handler
        handler = LlamaChromaHandler(vectorstore=vectorstore)

        # Esegui la gestione della query
        city = city.lower()
        city = city.strip()
        result = handler.process_query(query, city)

        # Mostra i risultati
        metadata = result["results"][0].metadata

        output = handler.format_response(query, metadata)

        clean_output = clean_dict(output)

        return clean_output

    except Exception as e:
        logger.error(f"Errore durante l'esecuzione del handler: {e}")
        raise
