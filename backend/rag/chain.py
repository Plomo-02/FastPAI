import os
import logging
from .vec_db import ChromaDB
from dotenv import load_dotenv
from openai import OpenAI

# Carica le variabili d'ambiente
load_dotenv()

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chain_app.log"),
        logging.StreamHandler()
    ]
)

# Configura il prompt per la formattazione della query
def create_prompt():
    return """
    Ricevi una richiesta utente e riformulala per essere adatta a una ricerca ottimale in un database vettoriale (ChromaDB).
    Assicurati che la query sia chiara, concisa e rappresenti al meglio l'intento originale dell'utente. rispondi esclusivamente con la query senza scrivere
    Richiesta originale: {input_text}
    """

# Configura il vectorstore Chroma
def initialize_chroma():
    db = ChromaDB()
    return db.vectorstore

# Classe per gestire le interazioni con OpenAI e Chroma
class LlamaChromaHandler:
    def __init__(self, vectorstore):
        self.client = OpenAI(
            base_url="https://api.aimlapi.com/v1",  # URL dell'API
            api_key=os.getenv("API_KEY"),          # Chiave API
        )
        self.vectorstore = vectorstore
        self.prompt_template = create_prompt()

    def send_request(self, prompt: str) -> str:
        """Invia una richiesta al modello OpenAI."""
        response = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",  # Modello utilizzato
            messages=[
                {"role": "system", "content": """Sei un assistente esperto di ricerca e Ricevi una richiesta utente e riformulala per essere adatta a una ricerca semantica per similarità in un database vettoriale (ChromaDB).
    Assicurati che la richiesta sia chiara, concisa e rappresenti al meglio l'intento originale dell'utente. rispondi esclusivamente con la richiesta senza scrivere."""},
                {"role": "user", "content": prompt}
            ],
            max_tokens=128
        )
        return response.choices[0].message.content.strip()

    def process_query(self, input_text: str):
        try:
            # Fase 1: Formatta la query con il modello AI
            logging.info("Formattazione della query tramite OpenAI...")
            #formatted_prompt = self.prompt_template.format(input_text=input_text)
            formatted_query = self.send_request(input_text)

            # Fase 2: Ricerca nel vectorstore
            logging.info("Esecuzione della ricerca su Chroma...")
            results = self.vectorstore.similarity_search(formatted_query, k=3)

            # Restituisci i risultati
            return {"results": results}
        except Exception as e:
            logging.error(f"Errore durante l'elaborazione della query: {e}")
            raise

# Funzione principale per eseguire la gestione
def run_handler(query: str):
    try:
        logging.info("Avvio del handler...")

        # Inizializza il vectorstore Chroma
        vectorstore = initialize_chroma()
        

        # Crea la handler
        handler = LlamaChromaHandler(vectorstore=vectorstore)

        # Esegui la gestione della query
        result = handler.process_query(query)

        # Mostra i risultati
        logging.info("Risultati del handler:")
        for item in result["results"]:
            logging.info(f" - item: {item}")
        
        return result
          
    except Exception as e:
        logging.error(f"Errore durante l'esecuzione del handler: {e}")
        raise

