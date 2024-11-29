import logging
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from chromadb import Settings as chroma_settings

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chroma_add.log"),
        logging.StreamHandler()
    ]
)

class ChromaDB:
    def __init__(self,persist_directory="./chroma_data"):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.setting = chroma_settings(is_persistent=True, anonymized_telemetry=False)
        self.vectorstore = Chroma(embedding_function=self.embeddings, persist_directory=persist_directory, client_settings=self.setting)


    # Inizializza il database Chroma
    # Aggiunge informazioni al database vettoriale
    def add_to_chroma(vectorstore, documents):
        try:
            logging.info("Aggiunta dei documenti al database Chroma...")
            texts = [doc["content"] for doc in documents]
            metadatas = [doc.get("metadata", {}) for doc in documents]
            
            # Aggiunge i documenti e i relativi metadati
            vectorstore.add_texts(texts=texts, metadatas=metadatas)
            logging.info(f"Aggiunti {len(documents)} documenti a Chroma.")
        except Exception as e:
            logging.error(f"Errore durante l'aggiunta di documenti a Chroma: {e}")
            raise


    def get_from_chroma(vectorstore, query):
        try:
            logging.info("Esecuzione della ricerca su Chroma...")
            results = vectorstore.similarity_search(query, k=2)
            logging.info("Ricerca completata con successo.")
            return results
        except Exception as e:
            logging.error(f"Errore durante l'elaborazione della query: {e}")
            raise



if __name__ == "__main__":
    try:
        
        vector_store = ChromaDB()
        print(vector_store.vectorstore)
    except Exception as e:
        logging.error(f"Errore nell'esecuzione del file: {e}")
