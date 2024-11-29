import logging
from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from transformers import pipeline

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Configurazione del modello Llama 3.1 tramite Hugging Face
def initialize_llama():
    try:
        logging.info("Inizializzazione del modello Llama 3.1...")
        llama_pipeline = pipeline(
            "text-generation",
            model="meta-llama/Llama-3.1",  # Sostituisci con il percorso del tuo modello
            device=0,  # Usa la GPU, metti -1 se vuoi usare la CPU
            max_length=256,
            temperature=0.7
        )
        llm = HuggingFacePipeline(pipeline=llama_pipeline)
        logging.info("Modello Llama 3.1 inizializzato con successo.")
        return llm
    except Exception as e:
        logging.error(f"Errore durante l'inizializzazione del modello Llama 3.1: {e}")
        raise

# Configurazione di Chroma
def initialize_chroma():
    try:
        logging.info("Inizializzazione del database Chroma...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        persist_directory = "./chroma_data"
        vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
        logging.info("Database Chroma inizializzato con successo.")
        return vectorstore
    except Exception as e:
        logging.error(f"Errore durante l'inizializzazione di Chroma: {e}")
        raise

# Funzione per prendere l'input, adattarlo e cercare su Chroma
def process_query(input_text, llm, vectorstore):
    try:
        logging.info("Formattazione della query con Llama 3.1...")
        # Formatta l'input con Llama 3.1
        formatted_query = llm(f"Formatta questa richiesta per una query vettoriale: {input_text}")
        
        # Rimuovi caratteri non necessari dalla risposta del modello
        formatted_query = formatted_query.strip()
        logging.info(f"Query formattata: {formatted_query}")
        
        # Esegui la ricerca su Chroma
        logging.info("Esecuzione della ricerca su Chroma...")
        results = vectorstore.similarity_search(formatted_query, k=3)
        logging.info("Ricerca completata con successo.")
        return results
    except Exception as e:
        logging.error(f"Errore durante l'elaborazione della query: {e}")
        raise

# Funzione principale
def run(query: str):
    try:
        logging.info("Avvio del processo principale...")
        
        # Inizializzazione
        llm = initialize_llama()
        vectorstore = initialize_chroma()

        # Processo della query
        search_results = process_query(query, llm, vectorstore)

        # Output dei risultati
        logging.info("Risultati della ricerca:")
        for result in search_results:
            logging.info(f" - Contenuto: {result['content']}")
            logging.info(f" - Metadata: {result['metadata']}")
    except Exception as e:
        logging.error(f"Errore nel processo principale: {e}")
        raise
